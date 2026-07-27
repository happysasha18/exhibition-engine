#!/usr/bin/env python3
"""EX-STORY-FILL / INV-107 — the edge half: a plot missing one line still speaks.

Thirteen matrix rows carry the requirement; the six function-level ones live here, plus the
function half of the one-work key row. The seven browser rows live in the site's tests/test_story.py.

The worker is the real baked `_worker.js`, imported into node with a KV stub (a Map that records
every put, its options, and every delete) and a scripted Anthropic. Each row drives a sequence of
real `handler.fetch(Request, env)` calls and reads the statuses, the model-call count and the KV
state that came out of them.

Run: .venv/bin/python tests/test_story_edge.py
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
import engine_build as build_site  # noqa: E402

SITE_URL = "https://synth.example.com"
NODE = shutil.which("node") or "/opt/homebrew/bin/node"
SCRATCHPAD = Path(tempfile.mkdtemp(prefix="story_edge_"))
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


ROWS = [
    "EX-STORY-FILL a plot missing one line serves the lines it carries",
    "EX-STORY-FILL the first entry for an id wins",
    "EX-STORY-FILL a short plot is cached the way a whole one is",
    "EX-STORY-FILL a plot that left no line is answered 502 and kept nowhere",
    "EX-STORY-FILL the lock stands while the model call is in flight (a second ask warms)",
    "EX-STORY-FILL the served exit deletes the lock it laid",
    "EX-STORY-FILL the throw and the no-line exit delete the lock too",
    "EX-STORY-FILL a request that met a standing lock deletes none",
    "EX-STORY-FILL a refusal and an unreadable answer are the empty class",
    "EX-STORY-FILL a bad status and a broken wire are the transient class",
    "EX-STORY-FILL the message keeps the plain `model <status>` shape",
    "EX-STORY-FILL a dead account raises the hour-long flag from this route",
    "EX-STORY-FILL an empty one-work answer is remembered for an hour",
    "EX-STORY-FILL the remembered refusal answers ahead of every fence and every model call",
    "EX-STORY-FILL past its hour the ask reaches the model again",
    "EX-STORY-FILL a portion's key carries no refusal record",
    "EX-STORY-FILL a one-work ask keys under its own shape",
    "EX-STORY-FILL the lock carries its expiry, the backstop for a worker that dies mid-call",
    "EX-STORY-FILL a call that outlived its expiry never takes away a later request's lock",
    "EX-STORY-FILL a work the edge holds no fragment for answers 404 ahead of every fence",
    "EX-EDGE-DEAD a retired model id stays transient — the hour's flag is for a dead ACCOUNT",
    "EX-EDGE-DEAD the story route's own dead flag never stops the language route",
    "EX-EDGE-DEAD the language route's own dead flag never stops the story route",
]

# ---------------------------------------------------------------- bake once, story on
TMP = Path(tempfile.mkdtemp(prefix="synth_story_edge_"))
build_site.OUT = TMP
build_site.build(SITE_URL, enable=["ai_story"])

WORKER_PATH = TMP / "_worker.js"
if not WORKER_PATH.exists():
    print(f"[FATAL] bake did not produce a worker at {WORKER_PATH}")
    sys.exit(1)

WORKER_SRC = WORKER_PATH.read_text(encoding="utf-8")

# the KV binding's baked name (EX_I18N in the engine, TLV_I18N in an instance)
m = re.search(r"env\.([A-Z][A-Z0-9_]*_I18N)\b", WORKER_SRC)
if not m:
    print("[FATAL] could not find the KV binding name in the baked worker")
    sys.exit(1)
BINDING = m.group(1)

# The ids the bake actually holds a fragment for — the story route answers 404 for any other. The
# bake replaces the whole placeholder span, so the fragments land as one JSON literal on its own line.
FRAGMENT_IDS = []
for line in WORKER_SRC.splitlines():
    if line.startswith("const STORY_FRAGMENTS = "):
        FRAGMENT_IDS = sorted(json.loads(line[len("const STORY_FRAGMENTS = "):].rstrip().rstrip(";")).keys())
        break
if len(FRAGMENT_IDS) < 3:
    print(f"[FATAL] the bake holds {len(FRAGMENT_IDS)} story fragments; the suite needs at least 3")
    sys.exit(1)
IDS = FRAGMENT_IDS[:6]
SOLO = IDS[0]

RUNNER = r"""
import { readFileSync } from 'fs';

const scenario = JSON.parse(readFileSync(process.argv[2], 'utf8'));
const workerPath = process.argv[3];

// ---- KV stub: a Map that remembers every put's options and every delete ----
const kv = new Map();
const puts = [];
const dels = [];
const KV = {
  async get(k) { return kv.has(k) ? kv.get(k).v : null; },
  async put(k, v, opts) { kv.set(k, { v: v, opts: opts || {} }); puts.push({ k: k, opts: opts || {} }); },
  async delete(k) { kv.delete(k); dels.push(k); },
};
for (const k of Object.keys(scenario.seed || {})) kv.set(k, { v: scenario.seed[k], opts: {} });

// ---- the scripted narrator: one answer spec per model call, in order ----
let modelCalls = 0;
let release = null;                       // resolves the held call
const answers = scenario.answers || [];
let ai = 0;
globalThis.fetch = async function (url, init) {
  const u = typeof url === 'string' ? url : (url && url.url) || String(url);
  if (u.indexOf('api.anthropic.com') === -1) return new Response('{}', { status: 200 });
  modelCalls++;
  const spec = answers[ai++] || { kind: 'ok', lines: [] };
  if (spec.hold) await new Promise((res) => { release = res; });
  if (spec.kind === 'network') throw new TypeError('Failed to fetch');
  if (spec.kind === 'status') return new Response('{}', { status: spec.status });
  if (spec.kind === 'unreadable') {
    return new Response(JSON.stringify({ content: [{ type: 'text', text: 'not json at all' }] }),
                        { status: 200 });
  }
  if (spec.kind === 'refusal') {
    return new Response(JSON.stringify({ stop_reason: 'refusal', content: [] }), { status: 200 });
  }
  return new Response(JSON.stringify({
    content: [{ type: 'text', text: JSON.stringify({ lines: spec.lines || [] }) }],
  }), { status: 200 });
};

// a fixed version so an i18n request's stale-version fence never fires — the story-edge suite
// never cares about a real translation, only whether the LANGUAGE route reaches the model
const env = { ANTHROPIC_API_KEY: 'test-key', ASSETS: { async fetch() {
  return new Response(JSON.stringify({ version: '1', strings: {}, greet: {}, titles: {} }),
                      { status: 200 });
} } };
env[scenario.binding] = KV;

const worker = await import(workerPath);
const handler = worker.default;

function storyReq(step) {
  const body = {};
  for (const k of Object.keys(step.body || {})) body[k] = step.body[k];
  return new Request('https://synth.example.com/api/story', {
    method: 'POST',
    headers: {
      'content-type': 'application/json',
      'user-agent': step.ua || scenario.ua,
      'cf-connecting-ip': step.ip || '203.0.113.7',
    },
    body: JSON.stringify(body),
  });
}

// the LANGUAGE route's own request — used only to prove the two routes' dead flags are independent
function i18nReq(step) {
  const lang = step.lang || 'pl';
  const v = step.v || '1';
  return new Request('https://synth.example.com/api/i18n?lang=' + lang + '&v=' + v, {
    headers: {
      'user-agent': step.ua || scenario.ua,
      'cf-connecting-ip': step.ip || '203.0.113.7',
    },
  });
}

async function read(r) {
  return { status: r.status, body: await r.text(), retryAfter: r.headers.get('Retry-After') };
}

const out = { steps: [] };
const inflight = {};
for (const step of scenario.steps) {
  if (step.op === 'release') {
    if (release) { const f = release; release = null; f(); }
    await new Promise((r) => setTimeout(r, 30));
    out.steps.push({ op: 'release' });
  } else if (step.op === 'forget') {
    kv.delete(step.key);
    out.steps.push({ op: 'forget' });
  } else if (step.op === 'relock') {
    // the lock's minute ran out mid-call and a LATER request laid its own — the same key, another owner
    let hit = null;
    for (const k of kv.keys()) if (k.indexOf('lock:') === 0) hit = k;
    if (hit) kv.set(hit, { v: step.value, opts: {} });
    out.steps.push({ op: 'relock', key: hit });
  } else if (step.op === 'snapshot') {
    out.steps.push({ op: 'snapshot', keys: Array.from(kv.keys()), modelCalls: modelCalls,
                     dels: dels.slice() });
  } else if (step.op === 'start') {
    inflight[step.name] = handler.fetch(storyReq(step), env).then(read);
    await new Promise((r) => setTimeout(r, 30));
    out.steps.push({ op: 'start' });
  } else if (step.op === 'settle') {
    const got = await inflight[step.name];
    out.steps.push(Object.assign({ op: 'settle', modelCalls: modelCalls,
                                   keys: Array.from(kv.keys()) }, got));
  } else if (step.op === 'i18nreq') {
    const got = await read(await handler.fetch(i18nReq(step), env));
    out.steps.push(Object.assign({ op: 'i18nreq', modelCalls: modelCalls,
                                   keys: Array.from(kv.keys()) }, got));
  } else {
    const got = await read(await handler.fetch(storyReq(step), env));
    out.steps.push(Object.assign({ op: 'req', modelCalls: modelCalls,
                                   keys: Array.from(kv.keys()) }, got));
  }
}
out.puts = puts;
out.dels = dels;
out.modelCalls = modelCalls;
out.kv = Array.from(kv.entries()).map(([k, e]) => ({ k: k, v: e.v, opts: e.opts }));
console.log(JSON.stringify(out));
"""

RUNNER_PATH = SCRATCHPAD / "story_edge_runner.mjs"
RUNNER_PATH.write_text(RUNNER, encoding="utf-8")


def run(steps, answers=None, seed=None):
    """Drive the real worker through a sequence of story requests. Returns the runner's report."""
    scenario = {
        "binding": BINDING, "ua": UA,
        "steps": steps, "answers": answers or [], "seed": seed or {},
    }
    path = SCRATCHPAD / "scenario.json"
    path.write_text(json.dumps(scenario), encoding="utf-8")
    p = subprocess.run([NODE, str(RUNNER_PATH), str(path), str(WORKER_PATH)],
                       capture_output=True, text=True, timeout=120)
    if p.returncode != 0:
        raise RuntimeError(f"runner failed ({p.returncode}): {p.stderr[-2000:]}")
    return json.loads(p.stdout.strip().splitlines()[-1])


def ask(ids, ip, one=False, lang="pl", variant="A", **kw):
    body = {"ids": ids, "variant": variant, "lang": lang}
    if one:
        body["one"] = True
    step = {"op": "req", "body": body, "ip": ip}
    step.update(kw)
    return step


def whole(ids):
    return [{"id": i, "line": "a quiet line for " + i, "source": "facts"} for i in ids]


def cache_keys(keys):
    return [k for k in keys if k.startswith("s:") or k.startswith("s1:")]


def lock_keys(keys):
    return [k for k in keys if k.startswith("lock:")]


def neg_keys(keys):
    return [k for k in keys if k.startswith("neg:")]


# ---------------------------------------------------------------- row 1-3: the answer is taken line by line
def row_partial():
    """A plot with one blank line, one bad provenance stamp, one id never asked for, and one id
    twice — the well-formed entries stand and are served, the first entry for an id wins, and the
    short plot is written to the cache the way a whole one is."""
    asked = IDS[:4]
    lines = [
        {"id": asked[0], "line": "the first work speaks", "source": "note"},
        {"id": asked[1], "line": "   ", "source": "facts"},            # blank — spoiled
        {"id": asked[2], "line": "the third work speaks", "source": "whisper"},   # bad stamp
        {"id": asked[3], "line": "the fourth work speaks", "source": "facts"},
        {"id": asked[3], "line": "a second line for the fourth", "source": "facts"},  # a repeat
        {"id": "notasked1234", "line": "a stranger", "source": "facts"},  # never asked for
    ]
    r = run([ask(asked, "203.0.113.11"), {"op": "snapshot"}], answers=[{"kind": "ok", "lines": lines}])
    step = r["steps"][0]
    served = None
    if step["status"] == 200:
        try:
            served = json.loads(step["body"])
        except Exception:
            served = None
    got = {str(l.get("id")): l.get("line") for l in (served or {}).get("lines", [])} if served else {}

    check(ROWS[0],
          step["status"] == 200 and set(got.keys()) == {asked[0], asked[3]},
          f"status {step['status']}, served ids {sorted(got.keys())} — expected the two well-formed "
          f"entries {sorted([asked[0], asked[3]])}")
    check(ROWS[1], got.get(asked[3]) == "the fourth work speaks",
          f"the id's line is {got.get(asked[3])!r} — the first entry for an id must win")
    cached = cache_keys(r["steps"][1]["keys"])
    body_cached = next((e["v"] for e in r["kv"] if e["k"] in cached), None)
    check(ROWS[2],
          len(cached) == 1 and body_cached == step["body"],
          f"cache keys {cached}; the stored body {'matches' if body_cached == step['body'] else 'differs from'} the served one")


def row_no_line():
    """Every entry spoiled: 502, and the key carries nothing afterwards."""
    asked = IDS[:3]
    lines = [{"id": i, "line": "", "source": "facts"} for i in asked]
    r = run([ask(asked, "203.0.113.12"), {"op": "snapshot"}], answers=[{"kind": "ok", "lines": lines}])
    step = r["steps"][0]
    keys = r["steps"][1]["keys"]
    check(ROWS[3], step["status"] == 502 and not cache_keys(keys),
          f"status {step['status']}, cache keys after {cache_keys(keys)} — a plot that left no line "
          f"is answered 502 and kept nowhere")


# ---------------------------------------------------------------- rows 4-7: the single-flight lock
def row_lock():
    asked = IDS[:3]
    r = run([
        {"op": "start", "name": "a", "body": {"ids": asked, "variant": "A", "lang": "pl"}, "ip": "203.0.113.13"},
        ask(asked, "203.0.113.14"),          # arrives mid-call — must warm
        {"op": "snapshot"},                  # the lock still stands, laid by A
        {"op": "release"},
        {"op": "settle", "name": "a"},
        {"op": "snapshot"},                  # A's exit took its lock away
    ], answers=[{"kind": "ok", "hold": True, "lines": whole(asked)}])

    second = r["steps"][1]
    mid = r["steps"][2]
    settled = r["steps"][4]
    after = r["steps"][5]
    check(ROWS[4],
          second["status"] == 503 and second["retryAfter"] and r["modelCalls"] == 1,
          f"the mid-call ask answered {second['status']} (Retry-After {second['retryAfter']}) with "
          f"{r['modelCalls']} model calls — one call serves the key while it is in flight")
    check(ROWS[5],
          settled["status"] == 200 and not lock_keys(after["keys"]),
          f"the held ask settled {settled['status']}; locks left behind: {lock_keys(after['keys'])}")
    check(ROWS[7],
          lock_keys(mid["keys"]) and r["dels"].count(lock_keys(mid["keys"])[0]) == 1,
          f"the lock was deleted {r['dels'].count(lock_keys(mid['keys'])[0]) if lock_keys(mid['keys']) else 0} "
          f"times — only the request that laid it may delete it")


def row_lock_on_failure():
    """A throw and a no-line answer each take their own lock away."""
    a, b = IDS[:3], IDS[3:6] or IDS[:2]
    r = run([
        ask(a, "203.0.113.15"),
        {"op": "snapshot"},
        ask(b, "203.0.113.16"),
        {"op": "snapshot"},
    ], answers=[
        {"kind": "status", "status": 500},                                   # the throw
        {"kind": "ok", "lines": [{"id": i, "line": "", "source": "facts"} for i in b]},  # no line
    ])
    thrown, after_throw, empty, after_empty = r["steps"]
    check(ROWS[6],
          thrown["status"] == 502 and not lock_keys(after_throw["keys"])
          and empty["status"] == 502 and not lock_keys(after_empty["keys"]),
          f"the throw answered {thrown['status']} leaving locks {lock_keys(after_throw['keys'])}; "
          f"the no-line answer {empty['status']} leaving locks {lock_keys(after_empty['keys'])}")


# ---------------------------------------------------------------- rows 8-11: the two ways a call ends
def row_classes():
    """The class decides whether a one-work ask's failure is remembered: the empty class leaves a
    refusal record, the transient class leaves none."""
    cases = [
        ("refusal", {"kind": "refusal"}, True),
        ("unreadable", {"kind": "unreadable"}, True),
        ("bad status", {"kind": "status", "status": 500}, False),
        ("broken wire", {"kind": "network"}, False),
    ]
    empty_ok, transient_ok, detail = True, True, []
    for i, (name, answer, wants_record) in enumerate(cases):
        r = run([ask([SOLO], f"203.0.113.{20 + i}", one=True), {"op": "snapshot"}], answers=[answer])
        recorded = bool(neg_keys(r["steps"][1]["keys"]))
        detail.append(f"{name}: 502={r['steps'][0]['status'] == 502} record={recorded}")
        if wants_record and not recorded:
            empty_ok = False
        if not wants_record and recorded:
            transient_ok = False
    check(ROWS[8], empty_ok, "; ".join(detail))
    # The transient half is only meaningful BESIDE a live empty half: with no record written at all,
    # "the transient class leaves none" would pass on nothing (a vacuous green).
    check(ROWS[9], transient_ok and empty_ok, "; ".join(detail))

    # Read the STORY route's own answer-reader alone: the i18n route carries a byte-identical throw,
    # so grepping the whole worker would pass on a sibling's code (an anchor on nothing).
    body = WORKER_SRC[WORKER_SRC.find("async function narrate("):]
    body = body[:body.find("\nfunction storyShape(")]
    shape_ok = '"model " + r.status' in body
    no_class_in_message = not re.search(r'"model \w+ " \+ r\.status', body)
    # the class travels on its own field, so the message the dead-account read is anchored on stays plain
    class_field = re.search(r"\.cls\s*=|cls:\s*\"(empty|transient)\"|classed\(", body)
    check(ROWS[10], shape_ok and no_class_in_message and bool(class_field),
          "the reader's non-ok throw must keep the plain `model <status>` message the dead-account "
          "read is anchored on, and carry its class in its own field")


def row_dead_flag():
    """A 4xx other than 429 from the story route raises the hour-long dead flag (INV-68), under a
    key that carries this route's own name — the story route's flag, not the whole edge's."""
    asked = IDS[:3]
    r = run([ask(asked, "203.0.113.30"), {"op": "snapshot"}], answers=[{"kind": "status", "status": 401}])
    keys = r["steps"][1]["keys"]
    flag = next((e for e in r["kv"] if e["k"] == "dead:model:story"), None)
    check(ROWS[11],
          r["steps"][0]["status"] == 502 and "dead:model:story" in keys
          and flag and flag["opts"].get("expirationTtl") == 3600,
          f"status {r['steps'][0]['status']}, dead flag {'raised' if 'dead:model:story' in keys else 'absent'}"
          f"{'' if not flag else ', ttl ' + str(flag['opts'].get('expirationTtl'))}")


# ---------------------------------------------------------------- rows 12-15: the refusal record
def row_retired_model():
    """The flag darkens every language for an hour, so what raises it is named member by member: the
    low-balance 400 and a revoked key's 401/403. A 404 names a model id retired out from under the
    bundle — a fault the daily call cap catches — and must leave the flag alone."""
    asked = IDS[:3]
    r404 = run([ask(asked, "203.0.113.90"), {"op": "snapshot"}],
               answers=[{"kind": "status", "status": 404}])
    r403 = run([ask(asked, "203.0.113.91"), {"op": "snapshot"}],
               answers=[{"kind": "status", "status": 403}])
    check(ROWS[20],
          r404["steps"][0]["status"] == 502 and "dead:model:story" not in r404["steps"][1]["keys"]
          and "dead:model:story" in r403["steps"][1]["keys"],
          f"a 404 answered {r404['steps'][0]['status']} and "
          f"{'raised' if 'dead:model:story' in r404['steps'][1]['keys'] else 'left'} the flag; a 403 "
          f"{'raised' if 'dead:model:story' in r403['steps'][1]['keys'] else 'left'} it")


def row_record():
    ip = "203.0.113.40"
    r = run([
        ask([SOLO], ip, one=True),           # the model refuses — the empty class
        {"op": "snapshot"},
        ask([SOLO], ip, one=True),           # meets the record: 502, no model call, no rate slot
        {"op": "snapshot"},
    ], answers=[{"kind": "refusal"}, {"kind": "ok", "lines": whole([SOLO])}])

    first, after_first, second, after_second = r["steps"]
    record = next((e for e in r["kv"] if e["k"].startswith("neg:")), None)
    check(ROWS[12],
          first["status"] == 502 and record and record["opts"].get("expirationTtl") == 3600,
          f"status {first['status']}, record {'present' if record else 'absent'}"
          f"{'' if not record else ', ttl ' + str(record['opts'].get('expirationTtl'))}")

    rate_before = next((e["v"] for e in r["kv"] if e["k"].startswith("rl:")), None)
    rate_puts = [p for p in r["puts"] if p["k"].startswith("rl:")]
    check(ROWS[13],
          second["status"] == 502 and after_second["modelCalls"] == after_first["modelCalls"]
          and len(rate_puts) <= 1,
          f"status {second['status']}, model calls {after_first['modelCalls']}→"
          f"{after_second['modelCalls']}, rate slots spent {len(rate_puts)} (counter {rate_before})")

    # past the hour the record is gone and the next ask reaches the model
    r2 = run([
        ask([SOLO], "203.0.113.41", one=True),
        {"op": "forget", "key": (record or {}).get("k", "neg:none")},
        ask([SOLO], "203.0.113.41", one=True),
    ], answers=[{"kind": "refusal"}, {"kind": "ok", "lines": whole([SOLO])}])
    check(ROWS[14],
          r2["steps"][2]["status"] == 200 and r2["modelCalls"] == 2,
          f"past its hour the ask answered {r2['steps'][2]['status']} after {r2['modelCalls']} model calls")


def row_portion_no_record():
    """A portion whose plot came back empty stays owed: no record, and its re-ask reaches the model."""
    asked = IDS[:3]
    ip = "203.0.113.50"
    r = run([
        ask(asked, ip),
        {"op": "snapshot"},
        ask(asked, ip),
        {"op": "snapshot"},
    ], answers=[{"kind": "refusal"}, {"kind": "ok", "lines": whole(asked)}])
    check(ROWS[15],
          not neg_keys(r["steps"][1]["keys"]) and r["steps"][2]["status"] == 200
          and r["modelCalls"] == 2,
          f"records after the empty portion: {neg_keys(r['steps'][1]['keys'])}; the re-ask answered "
          f"{r['steps'][2]['status']} after {r['modelCalls']} model calls")


def row_one_work_key():
    """A one-work ask and a portion that happens to hold that same single work keep separate
    entries — the marked ask never serves the portion's plot, and neither serves the other's."""
    r = run([
        ask([SOLO], "203.0.113.60", one=True),
        ask([SOLO], "203.0.113.60"),           # the same id, unmarked — a portion of one
        {"op": "snapshot"},
    ], answers=[
        {"kind": "ok", "lines": [{"id": SOLO, "line": "the one-work line", "source": "facts"}]},
        {"kind": "ok", "lines": [{"id": SOLO, "line": "the portion line", "source": "facts"}]},
    ])
    one_body, portion_body = r["steps"][0], r["steps"][1]
    keys = cache_keys(r["steps"][2]["keys"])
    served_apart = (one_body["status"] == 200 and portion_body["status"] == 200
                    and "the one-work line" in one_body["body"]
                    and "the portion line" in portion_body["body"])
    check(ROWS[16], len(keys) == 2 and served_apart and r["modelCalls"] == 2,
          f"cache keys {len(keys)} ({keys}), model calls {r['modelCalls']}; the marked ask and the "
          f"one-work portion must not share a key")


def row_lock_expiry():
    """The lock's expiry is the backstop for a worker that dies with the call in flight — and a call
    that outlived that expiry must never take away the lock a LATER request laid."""
    asked = IDS[:3]
    r = run([
        {"op": "start", "name": "a", "body": {"ids": asked, "variant": "A", "lang": "pl"},
         "ip": "203.0.113.70"},
        {"op": "relock", "value": "a-later-request"},
        {"op": "release"},
        {"op": "settle", "name": "a"},
        {"op": "snapshot"},
    ], answers=[{"kind": "ok", "hold": True, "lines": whole(asked)}])

    lock_put = next((p for p in r["puts"] if p["k"].startswith("lock:")), None)
    check(ROWS[17], lock_put and lock_put["opts"].get("expirationTtl") == 60,
          f"the lock was laid with options {lock_put['opts'] if lock_put else None} — with no expiry a "
          f"worker that dies mid-call wedges the key for good")

    survivor = next((e for e in r["kv"] if e["k"].startswith("lock:")), None)
    check(ROWS[18],
          r["steps"][3]["status"] == 200 and survivor and survivor["v"] == "a-later-request",
          f"the held ask settled {r['steps'][3]['status']} and the standing lock reads "
          f"{survivor['v'] if survivor else None!r} — the later request's lock must survive")


def row_unknown_work():
    """A work the edge holds no fragment for is refused ahead of every fence and every model call."""
    r = run([ask(["nosuchwork01"], "203.0.113.80", one=True), {"op": "snapshot"}],
            answers=[{"kind": "ok", "lines": []}])
    step, snap = r["steps"]
    rate_puts = [p for p in r["puts"] if p["k"].startswith("rl:")]
    check(ROWS[19],
          step["status"] == 404 and snap["modelCalls"] == 0 and not rate_puts,
          f"status {step['status']}, model calls {snap['modelCalls']}, rate slots spent "
          f"{len(rate_puts)} — an unknown work costs neither money nor a slot, at every rung")


def dead_keys(keys):
    return [k for k in keys if k.startswith("dead:model")]


# ---------------------------------------------------------- cross-route dead-flag isolation
def row_story_dead_leaves_i18n():
    """A dead-class status the STORY route provokes raises the story flag alone: a further story
    ask meets that flag at once (no model call), while a LANGUAGE ask in the same hour still
    reaches the model — the story route's own trouble never darkens every language."""
    asked = IDS[:3]
    r = run([
        ask(asked, "203.0.113.95"),                                      # dies with a 401 — dead class
        {"op": "snapshot"},
        ask(asked, "203.0.113.96"),                                      # meets the flag: silence
        {"op": "i18nreq", "lang": "de", "v": "1", "ip": "203.0.113.97"},  # the language route
    ], answers=[{"kind": "status", "status": 401}])
    died, after_die, blocked, lang_call = r["steps"]
    check(ROWS[21],
          died["status"] == 502 and dead_keys(after_die["keys"]) == ["dead:model:story"]
          and blocked["status"] == 404 and blocked["modelCalls"] == after_die["modelCalls"]
          and lang_call["modelCalls"] == after_die["modelCalls"] + 1,
          f"the dying story call answered {died['status']} and raised {dead_keys(after_die['keys'])}; "
          f"the next story ask answered {blocked['status']} with {blocked['modelCalls']} model calls "
          f"(unchanged from {after_die['modelCalls']}); the language ask reached the model "
          f"({lang_call['modelCalls']} model calls, up from {after_die['modelCalls']})")


def row_i18n_dead_leaves_story():
    """A dead-class status the LANGUAGE route provokes raises the i18n flag alone: a further ask
    in that language meets the flag (the baked English day, no model call), while a STORY ask in
    the same hour still reaches the model — the language route's own trouble never silences
    the told story."""
    asked = IDS[:3]
    r = run([
        {"op": "i18nreq", "lang": "fr", "v": "1", "ip": "203.0.113.98"},  # dies with a 400 — dead class
        {"op": "snapshot"},
        {"op": "i18nreq", "lang": "fr", "v": "1", "ip": "203.0.113.98"},  # meets the flag: English day
        ask(asked, "203.0.113.99"),                                      # the story route
    ], answers=[{"kind": "status", "status": 400}, {"kind": "ok", "lines": whole(asked)}])
    died, after_die, blocked, story_call = r["steps"]
    check(ROWS[22],
          died["status"] == 200 and dead_keys(after_die["keys"]) == ["dead:model:i18n"]
          and blocked["status"] == 200 and blocked["modelCalls"] == after_die["modelCalls"]
          and story_call["status"] == 200 and story_call["modelCalls"] == after_die["modelCalls"] + 1,
          f"the dying language call answered {died['status']} and raised {dead_keys(after_die['keys'])}; "
          f"the repeat language ask answered {blocked['status']} with {blocked['modelCalls']} model "
          f"calls (unchanged from {after_die['modelCalls']}); the story ask answered "
          f"{story_call['status']} and reached the model ({story_call['modelCalls']} model calls, up "
          f"from {after_die['modelCalls']})")


# ---------------------------------------------------------------- run
if not Path(NODE).exists():
    for name in ROWS:
        skip(name, f"node not found at {NODE}")
else:
    for fn in (row_partial, row_no_line, row_lock, row_lock_on_failure, row_classes,
               row_dead_flag, row_record, row_portion_no_record, row_one_work_key,
               row_lock_expiry, row_unknown_work, row_retired_model,
               row_story_dead_leaves_i18n, row_i18n_dead_leaves_story):
        try:
            fn()
        except Exception as e:                       # a row that cannot run is a red row, never a silent pass
            check(f"{fn.__name__} could not run", False, f"{type(e).__name__}: {e}")

shutil.rmtree(TMP, ignore_errors=True)
shutil.rmtree(SCRATCHPAD, ignore_errors=True)

fails = [r for r in results if r[1] == "FAIL"]
skips = [r for r in results if r[1] == "SKIP"]
for name, st, detail in results:
    print(f"[{st}] {name}" + (f"  — {detail}" if detail and st != "PASS" else ""))
print(f"\n{len(results)} rows: {len(results)-len(fails)-len(skips)} pass, "
      f"{len(fails)} fail, {len(skips)} skip")
sys.exit(1 if fails else 0)
