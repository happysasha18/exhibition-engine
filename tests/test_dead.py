#!/usr/bin/env python3
"""EX-EDGE-DEAD / INV-68 — The site outlives its model account.
Seven rows, one per SPEC "The site outlives its model account" entry.

EXPECTED FAIL today: DEAD-400, DEAD-STORY, DEAD-PLAIN-data, DEAD-PLAIN-payload, DEAD-DOUBLE
EXPECTED PASS today: DEAD-TRANSIENT, DEAD-LIVE

Run: .venv/bin/python tests/test_dead.py

Ported from an instance's tests/test_dead.py — adapted for the engine:
- import engine_build as build_site (the engine shim)
- SITE_URL is the synthetic site URL
- greetings.json lives at tests/fixture_content/data/greetings.json
- gen_greetings.py lives at scripts/gen_greetings.py (same relative path as an instance)
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
import engine_build as build_site  # noqa: E402

SITE_URL = "https://synth.example.com"
NODE = "/opt/homebrew/bin/node"
SCRATCHPAD = Path(tempfile.mkdtemp(prefix="engine_dead_"))

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


# ---------------------------------------------------------------- bake once (ai_i18n on to get worker + source)
TMP = Path(tempfile.mkdtemp(prefix="synth_dead_"))
build_site.OUT = TMP
build_site.build(SITE_URL, enable=["ai_i18n"])

WORKER_PATH = TMP / "_worker.js"
I18N_SRC_PATH = TMP / "i18n_source.json"

if not WORKER_PATH.exists() or not I18N_SRC_PATH.exists():
    print(f"[FATAL] bake did not produce worker or i18n_source — WORKER:{WORKER_PATH.exists()} I18N:{I18N_SRC_PATH.exists()}")
    sys.exit(1)

I18N_SRC = json.loads(I18N_SRC_PATH.read_text(encoding="utf-8"))
VERSION = str(I18N_SRC["version"])
I18N_SRC_BYTES = I18N_SRC_PATH.read_bytes()

# ---------------------------------------------------------------- build a valid translation body for the 200 scenario
# Satisfy validate(out, src): dir ltr, all string keys filled, more has {n}, greet arrays filled, titles map filled.
_VALID_STRINGS = {
    "ask": "what feels closer now?",
    "exit": "exit",
    "more": "{n} more",
    "q_more": "walk on?",
    "q_spent": "onward",
    "share_label": "share",
    "share_copied": "link copied",
    "series": "series",
    "room_back": "back",
    "enjoy": "enjoy",
    "quiz_ask": "where was this?",
    "quiz_submit": "submit",
    "quiz_win": "you have the eye.",
    "quiz_wrong": "not quite",
    "gift_ask": "did you like it?",
    "gift_yes": "yes",
    "gift_no": "not now",
    "gift_buy": "buy a print",
}
_VALID_GREET = {
    "night": ["Good night"],
    "morning": ["Good morning"],
    "day": ["Good afternoon"],
    "evening": ["Good evening"],
}
_VALID_TITLES = {tid: ttl for tid, ttl in (I18N_SRC.get("titles") or {}).items()}

VALID_PAYLOAD = {
    "dir": "ltr",
    **_VALID_STRINGS,
    "greet": _VALID_GREET,
    "titles": _VALID_TITLES,
}
# The Anthropic message envelope (what translate() reads from r.json()):
# msg.content = [{type:"text", text: JSON.stringify(payload_matching_shape())}]
# shape() uses: {strings:{...}, greet:{...}, titles:[{id,title},...]}
# But validate() is called on the FLATTENED result from translate():
#   flat = Object.assign({}, out.strings, {greet:out.greet, titles:{id:title,...}, dir:...})
# So shape() requires nested form but validate() checks flat form.
# The model answer must match shape() structure, then translate() flattens it.
_MODEL_ANSWER_STRINGS = {k: v for k, v in _VALID_STRINGS.items() if k != "more"}
_MODEL_ANSWER_STRINGS["more"] = "{n} more"
_MODEL_ANSWER = {
    "strings": _MODEL_ANSWER_STRINGS,
    "greet": _VALID_GREET,
    "titles": [{"id": tid, "title": ttl} for tid, ttl in _VALID_TITLES.items()],
}
VALID_MODEL_RESPONSE = {
    "content": [{"type": "text", "text": json.dumps(_MODEL_ANSWER)}],
    "stop_reason": "end_turn",
}

# ---------------------------------------------------------------- the node runner template
# Written to a temp .mjs file. The runner receives a scenario JSON via argv[2] and prints JSON result.
# Scenario fields:
#   anthropic_status: int (HTTP status from fake Anthropic) or "network_error"
#   seed_death_flag: bool (pre-seed "dead:model"="1" in KV)
#   lang: string (language for the i18n request)
#   clear_lock: bool (clear lock key before the request — used between consecutive calls)
#   second_call_lang: string (if set, make a second i18n call with this lang AFTER first)
#   story_call: bool (if set, call /api/story instead of /api/i18n)
RUNNER_TEMPLATE = r"""
import { readFileSync } from 'fs';

const scenario = JSON.parse(process.argv[2]);
const workerPath = process.argv[3];
const i18nBytes = readFileSync(process.argv[4]);

// ---- KV stub (EX_I18N) ----
const kvMap = new Map();
const kvPuts = [];  // all puts recorded here

const EX_I18N = {
  async get(k) { return kvMap.has(k) ? kvMap.get(k) : null; },
  async put(k, v, opts) {
    kvMap.set(k, v);
    kvPuts.push({ k, v, opts: opts || {} });
  },
};

// ---- Pre-seed the death flag if requested ----
if (scenario.seed_death_flag) {
  kvMap.set('dead:model', '1');
}

// ---- Pre-seed budget at some safe value (not over cap) ----
const today = new Date().toISOString().slice(0, 10);
kvMap.set('budget:' + today, '0');

// ---- Model fetch counter ----
let modelFetchCount = 0;

// ---- Valid model response bytes ----
const validModelResponse = JSON.parse(process.argv[5]);

// ---- Stub globalThis.fetch ----
const realFetch = globalThis.fetch;
globalThis.fetch = async function(url, init) {
  const urlStr = typeof url === 'string' ? url : (url.url || String(url));
  if (urlStr.includes('api.anthropic.com')) {
    modelFetchCount++;
    if (scenario.anthropic_status === 'network_error') {
      throw new TypeError('Failed to fetch');
    }
    const status = scenario.anthropic_status || 200;
    if (status === 200) {
      return new Response(JSON.stringify(validModelResponse), {
        status: 200,
        headers: { 'Content-Type': 'application/json' },
      });
    }
    // Error responses (400, 401, 429, 500, etc.)
    const errBodies = {
      400: JSON.stringify({ type: 'error', error: { type: 'invalid_request_error', message: 'Your credit balance is too low' } }),
      401: JSON.stringify({ type: 'error', error: { type: 'authentication_error', message: 'Invalid API key' } }),
      429: JSON.stringify({ type: 'error', error: { type: 'rate_limit_error', message: 'Too many requests' } }),
      500: JSON.stringify({ type: 'error', error: { type: 'api_error', message: 'Internal server error' } }),
      529: JSON.stringify({ type: 'error', error: { type: 'overloaded_error', message: 'Overloaded' } }),
    };
    return new Response(errBodies[status] || '{}', {
      status: status,
      headers: { 'Content-Type': 'application/json' },
    });
  }
  // ASSETS fetch (i18n_source.json)
  return new Response(i18nBytes, {
    status: 200,
    headers: { 'Content-Type': 'application/json' },
  });
};

// ---- ASSETS stub ----
const ASSETS = {
  async fetch(url) {
    return new Response(i18nBytes, {
      status: 200,
      headers: { 'Content-Type': 'application/json' },
    });
  },
};

// ---- Env stub ----
const env = {
  EX_I18N,
  ANTHROPIC_API_KEY: 'test-key',
  ASSETS,
};

// ---- Import the worker ----
const worker = await import(workerPath);
const handler = worker.default;

// ---- Helper: make an i18n request ----
function makeI18nReq(lang, version) {
  return new Request(
    'https://synth.example.com/api/i18n?lang=' + lang + '&v=' + version,
    {
      headers: {
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
        'cf-connecting-ip': '1.2.3.4',
      },
    }
  );
}

// ---- Helper: make a story request ----
function makeStoryReq() {
  // Pick some valid-shaped ids from the worker's STORY_FRAGMENTS if non-empty,
  // otherwise use a fake id that will 404 due to empty fragments.
  return new Request(
    'https://synth.example.com/api/story',
    {
      method: 'POST',
      headers: {
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
        'cf-connecting-ip': '1.2.3.4',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ ids: ['12345678901234'], variant: 'A', lang: 'pl' }),
    }
  );
}

// ---- Helper: clear the lock for a given lang+version ----
function clearLock(lang, version) {
  const key = 'lock:' + version + ':' + lang;
  kvMap.delete(key);
  // Also remove any record of it from kvPuts so assertions are clean
}

// ---- Run first call ----
const lang = scenario.lang || 'pl';
const version = process.argv[6];

// Clear lock before first call (safety)
clearLock(lang, version);

let firstRes, firstBody, firstStatus;
if (scenario.story_call) {
  firstRes = await handler.fetch(makeStoryReq(), env);
} else {
  firstRes = await handler.fetch(makeI18nReq(lang, version), env);
}
firstStatus = firstRes.status;
try { firstBody = await firstRes.json(); } catch(e) { firstBody = null; }

// ---- Optionally run a second call ----
let secondRes = null, secondBody = null, secondStatus = null;
const modelAfterFirst = modelFetchCount;
if (scenario.second_call_lang) {
  const lang2 = scenario.second_call_lang;
  clearLock(lang2, version);
  const res2 = await handler.fetch(makeI18nReq(lang2, version), env);
  secondStatus = res2.status;
  try { secondBody = await res2.json(); } catch(e) { secondBody = null; }
}

// ---- Collect results ----
// Find the death flag put: any put whose key contains "dead"
const deathFlagPuts = kvPuts.filter(p => p.k.includes('dead'));
// Find cache puts under the lang+version key (lang cache, not lock, not rl:, not budget:, not dead:)
const langCachePuts = kvPuts.filter(p => p.k === version + ':' + lang);
// The budget key after calls
const budgetKey = 'budget:' + today;
const budgetAfter = parseInt(kvMap.get(budgetKey) || '0', 10);

const output = {
  firstStatus,
  firstBody,
  secondStatus,
  secondBody,
  modelFetchCount,
  modelAfterFirst,
  deathFlagPuts,
  langCachePuts,
  budgetAfter,
  allPutKeys: kvPuts.map(p => p.k),
};

process.stdout.write(JSON.stringify(output) + '\n');
"""


def run_scenario(scenario_dict, lang="pl", second_call_lang=None, story_call=False):
    """Run the node runner with the given scenario. Returns parsed output dict or raises."""
    runner_path = SCRATCHPAD / "dead_runner_engine.mjs"
    # Write the runner (overwrite each time, same path)
    runner_path.write_text(RUNNER_TEMPLATE, encoding="utf-8")

    scenario = dict(scenario_dict)
    if second_call_lang:
        scenario["second_call_lang"] = second_call_lang
    if story_call:
        scenario["story_call"] = True
    if "lang" not in scenario:
        scenario["lang"] = lang

    cmd = [
        NODE,
        str(runner_path),
        json.dumps(scenario),
        str(WORKER_PATH),
        str(I18N_SRC_PATH),
        json.dumps(VALID_MODEL_RESPONSE),
        VERSION,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if proc.returncode != 0:
        raise RuntimeError(f"node runner failed (rc={proc.returncode}):\n{proc.stderr[:1000]}")
    line = proc.stdout.strip().split("\n")[-1]
    return json.loads(line)


# ---------------------------------------------------------------- ROW 1: DEAD-400 raises the hour flag
# Scenario: Anthropic returns 400 (low-balance).
# Expected after implementation: 200 with English body, death flag put, no lang cache put.
# Second call (different lang): model fetch count did NOT grow.
# EXPECTED FAIL today: 400 → translate() throws "model 400" → 502 "model unavailable"
def row1_dead400():
    try:
        r = run_scenario({"anthropic_status": 400, "seed_death_flag": False}, lang="pl", second_call_lang="de")
    except Exception as e:
        check("DEAD-400 a dead balance raises the hour flag",
              False, f"runner exception: {e}")
        return

    first_ok = r["firstStatus"] == 200
    # Check body looks like englishFrom (has dir:"ltr" and strings)
    fb = r["firstBody"] or {}
    body_english_shaped = (isinstance(fb, dict) and fb.get("dir") == "ltr"
                           and bool(fb.get("greet")) and bool(fb.get("titles")))
    # Death flag: any put with key containing "dead" and expirationTtl between 1800 and 7200
    flag_puts = [p for p in r["deathFlagPuts"]
                 if 1800 <= (p.get("opts") or {}).get("expirationTtl", 0) <= 7200]
    death_flag_put = len(flag_puts) > 0
    # Lang cache key (v:lang) was NOT put
    lang_cache_not_put = len(r["langCachePuts"]) == 0
    # Second call: model fetch count did not grow
    no_second_model_call = (r["modelFetchCount"] == r["modelAfterFirst"])

    cond = first_ok and body_english_shaped and death_flag_put and lang_cache_not_put and no_second_model_call
    detail = (
        f"firstStatus={r['firstStatus']} (want 200) "
        f"body_english_shaped={body_english_shaped} "
        f"death_flag_put={death_flag_put} (flag_puts={flag_puts}) "
        f"lang_cache_not_put={lang_cache_not_put} langCachePuts={r['langCachePuts']} "
        f"no_second_model_call={no_second_model_call} "
        f"modelFetchCount={r['modelFetchCount']} modelAfterFirst={r['modelAfterFirst']} "
        f"allPutKeys={r['allPutKeys']}"
    )
    check("DEAD-400 a dead balance raises the hour flag", cond, detail if not cond else "")


# ---------------------------------------------------------------- ROW 2: DEAD-TRANSIENT stays transient
# Scenarios: 429, 500, network_error → each answers 502 "model unavailable", NO death flag put.
# EXPECTED PASS today (today's shipped behaviour).
def row2_transient():
    all_pass = True
    details = []
    for scenario_name, sc in [
        ("429", {"anthropic_status": 429}),
        ("500", {"anthropic_status": 500}),
        ("network_error", {"anthropic_status": "network_error"}),
    ]:
        # Use distinct langs so lock isolation is clean
        lang = {"429": "fr", "500": "es", "network_error": "uk"}[scenario_name]
        try:
            r = run_scenario(sc, lang=lang)
        except Exception as e:
            details.append(f"{scenario_name}: runner exception: {e}")
            all_pass = False
            continue

        is_502 = r["firstStatus"] == 502
        no_death_flag = len(r["deathFlagPuts"]) == 0
        ok = is_502 and no_death_flag
        if not ok:
            all_pass = False
        details.append(
            f"{scenario_name}: status={r['firstStatus']} (want 502) "
            f"no_death_flag={no_death_flag} death_flag_puts={r['deathFlagPuts']}"
        )

    cond = all_pass
    check(
        "DEAD-TRANSIENT transient stays transient (429, 500, network throw → 502, no flag)",
        cond,
        "; ".join(details) if not cond else "",
    )


# ---------------------------------------------------------------- ROW 3: DEAD-STORY quiet behind the flag
# Pre-seed death flag, assert: (a) /api/story answers non-ok + zero model fetches;
# (b) with the flag seeded, /api/i18n also serves English with zero model fetches (the flag check).
# EXPECTED FAIL today: no flag check logic. STORY_FRAGMENTS is empty so story 404s early by
# coincidence, but the i18n route ignores the flag and tries the model (which 502s on a bad account).
# We assert both conditions; both must hold for PASS — today the i18n flag-check fails.
# NOTE from brief: "if the fragments are empty in this bake, the story route 404s early —
# assert the flag-standing scenario by the i18n route alone and note it in the checkpoint."
def row3_story_quiet():
    # Part A: /api/story with seeded flag — expect non-ok + zero model calls
    try:
        r_story = run_scenario({"anthropic_status": 200, "seed_death_flag": True, "lang": "pl"}, story_call=True)
    except Exception as e:
        check("DEAD-STORY the story goes quiet behind the flag", False, f"story runner exception: {e}")
        return

    story_non_ok = r_story["firstStatus"] != 200
    story_zero_model = r_story["modelFetchCount"] == 0

    # Part B: with the death flag seeded, /api/i18n should serve English with NO model fetch
    # (the flag check prevents the model call). Today this FAILS: the worker ignores the flag.
    # Use a 200-capable Anthropic stub — if the worker calls the model (ignoring the flag), it
    # will succeed and cache; the absence of a model call is what we want to assert.
    try:
        r_i18n = run_scenario({"anthropic_status": 200, "seed_death_flag": True, "lang": "ru"})
    except Exception as e:
        check("DEAD-STORY the story goes quiet behind the flag", False, f"i18n runner exception: {e}")
        return

    i18n_200 = r_i18n["firstStatus"] == 200
    # With the flag the model must NOT be called; today it IS called (no flag logic)
    i18n_zero_model = r_i18n["modelFetchCount"] == 0

    cond = story_non_ok and story_zero_model and i18n_200 and i18n_zero_model
    detail = (
        f"story: status={r_story['firstStatus']} non_ok={story_non_ok} "
        f"story_zero_model={story_zero_model} "
        f"(STORY_FRAGMENTS empty — 404 before flag check; correct by construction today) "
        f"| i18n behind flag: status={r_i18n['firstStatus']} i18n_200={i18n_200} "
        f"i18n_zero_model={i18n_zero_model} (FAIL: flag ignored, model called) "
        f"i18n modelFetchCount={r_i18n['modelFetchCount']} (want 0)"
    )
    check("DEAD-STORY the story goes quiet behind the flag", cond, detail if not cond else "")


# ---------------------------------------------------------------- ROW 4a: DEAD-PLAIN data check
# The contract as shipped (aligned 2026-07-10, senior): the reviewed line lives at
# tests/fixture_content/data/greetings.json langs.en.plain, and the bake emits it TOP-LEVEL in
# i18n_source.json as "plain" (beside "greet" — greet stays the daypart pools).
# The gen validator requires en.plain.
def row4a_plain_data():
    src_plain = I18N_SRC.get("plain")
    src_ok = isinstance(src_plain, str) and bool(src_plain.strip())
    hand = json.loads(
        (ROOT / "tests" / "fixture_content" / "data" / "greetings.json")
        .read_text(encoding="utf-8")
    )
    en_plain = ((hand.get("langs") or {}).get("en") or {}).get("plain")
    hand_ok = isinstance(en_plain, str) and bool(en_plain.strip())
    chk = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "gen_greetings.py"), "--check"],
        capture_output=True, text=True,
    )
    cond = src_ok and hand_ok and chk.returncode == 0
    detail = (
        f"i18n_source.plain={src_plain!r} greetings.en.plain={en_plain!r} "
        f"check_rc={chk.returncode} (want the reviewed line in BOTH homes + validator green)"
    )
    check("DEAD-PLAIN-data greetings source carries 'plain' field (shape check knows it)", cond, detail if not cond else "")


# ---------------------------------------------------------------- ROW 4b: DEAD-PLAIN payload behind the flag
# Behind the death flag, the i18n payload's greet must be the one plain line, no daypart variants.
# EXPECTED FAIL today: no flag logic; 400 → 502 today.
def row4b_plain_payload():
    try:
        r = run_scenario({"anthropic_status": 400, "seed_death_flag": False}, lang="it")
    except Exception as e:
        check("DEAD-PLAIN-payload behind flag the i18n greet is the plain line", False, f"runner exception: {e}")
        return

    fb = r["firstBody"] or {}
    # The contract as shipped (aligned 2026-07-10, senior): the client stays UNCHANGED (the spec's
    # own sentence — the payload is the whole story), so the plain line rides the daypart SHAPE:
    # every daypart pool is the SAME single plain line. No daypart flourish can survive that shape.
    is_200 = r["firstStatus"] == 200
    greet_val = fb.get("greet") if isinstance(fb, dict) else None
    plain = I18N_SRC.get("plain") or "hello"
    pools_ok = (isinstance(greet_val, dict)
                and set(greet_val.keys()) == {"night", "morning", "day", "evening"}
                and all(greet_val[p] == [plain] for p in greet_val))
    cond = is_200 and pools_ok
    detail = (
        f"firstStatus={r['firstStatus']} (want 200) greet={greet_val!r} "
        f"(want every daypart pool == [{plain!r}] — one plain line, zero flourish)"
    )
    check("DEAD-PLAIN-payload behind flag the i18n greet is the plain line", cond, detail if not cond else "")


# ---------------------------------------------------------------- ROW 5: DEAD-DOUBLE two deaths, one flag
# Two 400-dying calls (different langs, cleared locks) → ONE death-flag put (idempotent), both answered
# English, model fetch count grew by 2 (both calls committed), budget grew by 2.
# EXPECTED FAIL today: no flag logic; 400 → 502 twice.
def row5_double():
    runner_path = SCRATCHPAD / "dead_runner_engine_double.mjs"

    double_template = r"""
import { readFileSync } from 'fs';

const scenario = JSON.parse(process.argv[2]);
const workerPath = process.argv[3];
const i18nBytes = readFileSync(process.argv[4]);

const kvMap = new Map();
const kvPuts = [];

const EX_I18N = {
  async get(k) { return kvMap.has(k) ? kvMap.get(k) : null; },
  async put(k, v, opts) {
    kvMap.set(k, v);
    kvPuts.push({ k, v, opts: opts || {} });
  },
};

const today = new Date().toISOString().slice(0, 10);
kvMap.set('budget:' + today, '0');

let modelFetchCount = 0;
const validModelResponse = JSON.parse(process.argv[5]);
const version = process.argv[6];

const ASSETS = {
  async fetch(url) {
    return new Response(i18nBytes, {
      status: 200,
      headers: { 'Content-Type': 'application/json' },
    });
  },
};

globalThis.fetch = async function(url, init) {
  const urlStr = typeof url === 'string' ? url : (url.url || String(url));
  if (urlStr.includes('api.anthropic.com')) {
    modelFetchCount++;
    const status = scenario.anthropic_status || 400;
    const errBodies = {
      400: JSON.stringify({ type: 'error', error: { type: 'invalid_request_error', message: 'Your credit balance is too low' } }),
    };
    return new Response(errBodies[status] || '{}', {
      status: status,
      headers: { 'Content-Type': 'application/json' },
    });
  }
  return new Response(i18nBytes, { status: 200, headers: { 'Content-Type': 'application/json' } });
};

const env = { EX_I18N, ANTHROPIC_API_KEY: 'test-key', ASSETS };

const worker = await import(workerPath);
const handler = worker.default;

function makeReq(lang) {
  return new Request(
    'https://synth.example.com/api/i18n?lang=' + lang + '&v=' + version,
    {
      headers: {
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
        'cf-connecting-ip': '1.2.3.4',
      },
    }
  );
}

// Call 1: lang=pl
kvMap.delete('lock:' + version + ':pl');
const res1 = await handler.fetch(makeReq('pl'), env);
const status1 = res1.status;
let body1 = null;
try { body1 = await res1.json(); } catch(e) {}
const modelAfter1 = modelFetchCount;

// Call 2: lang=de (different lang → no cache hit)
kvMap.delete('lock:' + version + ':de');
const res2 = await handler.fetch(makeReq('de'), env);
const status2 = res2.status;
let body2 = null;
try { body2 = await res2.json(); } catch(e) {}

const today2 = new Date().toISOString().slice(0, 10);
const budgetAfter = parseInt(kvMap.get('budget:' + today2) || '0', 10);
const deathFlagPuts = kvPuts.filter(p => p.k.includes('dead'));
const uniqueDeathFlagKeys = [...new Set(deathFlagPuts.map(p => p.k))];

const output = {
  status1, body1, status2, body2,
  modelFetchCount, modelAfter1,
  budgetAfter,
  deathFlagPuts,
  uniqueDeathFlagKeys,
  allPutKeys: kvPuts.map(p => p.k),
};

process.stdout.write(JSON.stringify(output) + '\n');
"""

    runner_path.write_text(double_template, encoding="utf-8")
    cmd = [
        NODE, str(runner_path),
        json.dumps({"anthropic_status": 400}),
        str(WORKER_PATH), str(I18N_SRC_PATH),
        json.dumps(VALID_MODEL_RESPONSE),
        VERSION,
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if proc.returncode != 0:
            check("DEAD-DOUBLE two deaths one flag", False, f"node rc={proc.returncode}: {proc.stderr[:400]}")
            return
        r = json.loads(proc.stdout.strip().split("\n")[-1])
    except Exception as e:
        check("DEAD-DOUBLE two deaths one flag", False, f"exception: {e}")
        return

    both_200 = r["status1"] == 200 and r["status2"] == 200
    # Both bodies should look like englishFrom
    b1, b2 = r.get("body1") or {}, r.get("body2") or {}
    both_english = (isinstance(b1, dict) and b1.get("dir") == "ltr"
                    and isinstance(b2, dict) and b2.get("dir") == "ltr")
    # Exactly one unique death flag key (idempotent)
    one_flag = len(r["uniqueDeathFlagKeys"]) == 1
    # The contract as shipped (aligned 2026-07-10, senior): back-to-back calls are SEQUENTIAL here,
    # so the FIRST death raises the flag and the SECOND call is fenced BEFORE the model — it makes
    # no fetch and charges nothing. Only the one dying call is committed and charged. (True
    # concurrency — two calls in flight before either flag-write — both charge; the KV write stays
    # idempotent either way, which is the fact the spec sentence pins.)
    fenced_second = r["modelFetchCount"] == 1 and r["modelAfter1"] == 1
    budget_one = r["budgetAfter"] == 1

    cond = both_200 and both_english and one_flag and fenced_second and budget_one
    detail = (
        f"status1={r['status1']} status2={r['status2']} (want both 200) "
        f"both_english={both_english} "
        f"uniqueDeathFlagKeys={r['uniqueDeathFlagKeys']} (want exactly 1) "
        f"modelFetchCount={r['modelFetchCount']} (want 1 — the 2nd call is fenced pre-model) "
        f"budgetAfter={r['budgetAfter']} (want 1) "
        f"allPutKeys={r['allPutKeys']}"
    )
    check("DEAD-DOUBLE two deaths one flag", cond, detail if not cond else "")


# ---------------------------------------------------------------- ROW 6: DEAD-LIVE a live account untouched
# Scenario: 200-valid → translation returned, cached under lang+version key, NO death flag.
# EXPECTED PASS today.
def row6_live():
    try:
        r = run_scenario({"anthropic_status": 200, "seed_death_flag": False}, lang="pl")
    except Exception as e:
        check("DEAD-LIVE a live account is untouched", False, f"runner exception: {e}")
        return

    is_200 = r["firstStatus"] == 200
    fb = r["firstBody"] or {}
    body_ok = isinstance(fb, dict) and fb.get("dir") == "ltr" and bool(fb.get("greet"))
    # Lang cache key (version:pl) was put
    lang_cached = len(r["langCachePuts"]) > 0
    # No death flag
    no_death_flag = len(r["deathFlagPuts"]) == 0

    cond = is_200 and body_ok and lang_cached and no_death_flag
    detail = (
        f"firstStatus={r['firstStatus']} (want 200) "
        f"body_ok={body_ok} (dir={fb.get('dir') if isinstance(fb,dict) else '?'}) "
        f"lang_cached={lang_cached} langCachePuts={r['langCachePuts']} "
        f"no_death_flag={no_death_flag} deathFlagPuts={r['deathFlagPuts']}"
    )
    check("DEAD-LIVE a live account is untouched", cond, detail if not cond else "")


# ---------------------------------------------------------------- run all rows
row1_dead400()
row2_transient()
row3_story_quiet()
row4a_plain_data()
row4b_plain_payload()
row5_double()
row6_live()

shutil.rmtree(TMP, ignore_errors=True)

fails = [r for r in results if r[1] == "FAIL"]
skips = [r for r in results if r[1] == "SKIP"]
for name, st, detail in results:
    print(f"[{st}] {name}" + (f"  — {detail}" if detail and st != "PASS" else ""))
print(f"\n{len(results)} rows: {len(results)-len(fails)-len(skips)} pass, "
      f"{len(fails)} fail, {len(skips)} skip")
sys.exit(1 if fails else 0)
