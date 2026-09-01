#!/usr/bin/env python3
"""EX-MEMORY §4.8 — the memory of a visit, and the return that is kin to the way out.
Run: python3 tests/test_pass_memory.py

Root: PASS-API-V1.md §4.8 (the edge record, the two refusals, what crosses the boundary), charter
shelf 16 (family drift within a visit, the pool re-rolling under cooldowns across visits), and the
unit brief docs/immersive/briefs/2026-08-17-U27-composed-full-route.md, stage 1 lane C, in the
tlvphotos tree.

WHAT THIS MEASURES.

  The record. One per edge and direction, keyed by the two work ids sorted, created as an edge first
  plays and held in the browser's own storage under the site's own key. It holds §4.8's nine names
  and nothing about the person.

  What crosses. Only the return reference — the family, the seed and the pass index. The composer
  refuses a fourth field, and tests/test_pass_composed.py holds that fence; what is held here is
  that the walk hands over those three and never builds a wider one.

  The two refusals, each named in plain words. An exact reversed replay of the recorded pass is
  refused; a backward plan sharing neither the family nor the pivot of it is refused. Both are
  measured end to end — the walk freezes no score onto the command and the visitor lands on the
  walk's own glide — and both redden the moment the check they stand on stops being called.

  The drift. A repeated edge inside a visit holds its family and shifts its shaping numbers inside
  the spans the instrument manifests publish. What the composer measured off the works never drifts,
  and neither do the doors: an effect still enters and leaves through its zero.

  The visit boundary. Beyond the visit window nothing crosses, the family that played is cooled and
  a second die is offered; where the die cannot move the family the cooled family plays, because a
  cooldown never empties a pool.

  The storage. A record survives a reload inside the window and the pass count runs on; a cleared
  storage walks with a fresh pool and says so on the diagnostic surface; a storage that will not
  open says so too, and the visitor lands in every one of those cases.

WHAT NEVER SHIPS. The lab's `build-edgememory-v1.py` enumerates every pair of the collection into
one file. That is exactly the class his word of 19:21 bans from the product path, and the first row
below holds that none of it reaches the bake.
"""
import json
import re
import sys
import tempfile
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
import engine_build as build_site  # noqa: E402
from headless import serve, Browser, chrome_available  # noqa: E402

SITE_URL = "https://synth.example.com"
FIXTURE = Path(__file__).resolve().parent / "fixture_pass_composed.json"

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


TMP = Path(tempfile.mkdtemp(prefix="synth_memory_"))
build_site.OUT = TMP
build_site.build(SITE_URL)
JS = (TMP / "exhibition.js").read_text(encoding="utf-8")
SRC = (ROOT / "engine" / "client" / "01a-pass.js").read_text(encoding="utf-8")

# ---------------------------------------------------------------- the bundle

check("EX-MEMORY the walk carries the edge record, and the lab's pair-scaled bake carries nowhere",
      "passEdgeRemember" in JS and "pass-edges" in JS and "edgememory" not in JS
      and not any(p.name.startswith("edgememory") for p in TMP.iterdir()),
      "the memory of a visit is built in the browser; the lab file that enumerates every pair is "
      "reference material and its data ships nowhere")

# The list was five numbers until 2026-08-18. Two of them — `reversalMean: 0.02` and
# `reversalWorst: 0.05` — turned the reversal reading into a yes or a no, and neither was ever
# measured. His word of 09:51 (any two photographs get a crossing) and of 08:47 (a number nobody
# measured goes) struck them, and what stands in their place is the distance itself: of the dice
# this edge is offered, the roll standing FURTHEST from the recorded pass's mirror plays. So this
# row now holds the three that remain in one record AND holds the two struck ones out of the file.
check("EX-MEMORY the numbers no measurement gives stand in one place, and the two struck ones are "
      "gone from the file",
      all(s in SRC for s in ("visitWindowSeconds: 1800", "cooldownSeconds: 86400",
                             "driftSpan: 0.25"))
      and "reversalMean" not in SRC and "reversalWorst" not in SRC
      and "function passMirrorDistance" in SRC,
      "a later pass tunes the whole list at once, so the list is one record and not constants "
      "spread through the file; and the reversal carries no number of its own — "
      "`passMirrorDistance` hands the distance over and the ranking reads it")

# ---------------------------------------------------------------- the walk, in a browser

BROWSER_ROWS = [
    "EX-MEMORY a first pass on an edge carries no memory, and the landing writes the edge record",
    "EX-MEMORY the record holds §4.8's own names and nothing about the person",
    "EX-MEMORY walking back hands the composer the return reference and nothing wider",
    "EX-MEMORY the backward passage is kin to the forward one and is not it played backwards",
    "EX-MEMORY held pass · a backward plan sharing neither the family nor the pivot still casts on "
    "its first and only die, and the mismatch is named on the surface",
    "EX-MEMORY ranking · a pass that reads as the recorded one reversed stands at no distance and "
    "ranks last of the dice",
    "EX-MEMORY a repeated edge inside a visit drifts: the family holds and the door breathes",
    "EX-MEMORY red-on-bug · the drift never touches a measured handle, a door or the clock",
    "EX-MEMORY across the visit boundary nothing crosses, the family is cooled and a second die is "
    "offered",
    "EX-MEMORY the record survives a reload inside the visit window and the pass count runs on",
    "EX-MEMORY a cleared storage walks with a fresh pool, says so, and the visitor still lands",
    "EX-MEMORY a storage that will not open says so, and the visitor still lands",
    "EX-MEMORY the store stays bounded: the youngest records stand and the rest go",
    "EX-MEMORY ?reset forgets the edges walked, the way it forgets everything else",
]


# §4.8'S JUDGE HANDS BACK A READING AND NEVER A YES OR A NO (2026-08-18). It answers
# {kin, distance, why}: `kin` is the plain fact of shared family or shared pivot, `distance` is how
# far this roll stands from the recorded pass's mirror with nothing where no reading applies, and
# `why` is the sentence that reaches the diagnostic surface. Every row below reads the reading
# through these two, so a row is never written against the shape of a refusal that is gone.
def _dist(v):
    return v.get("distance") if isinstance(v, dict) else None


def _why(v):
    return (v.get("why") or "") if isinstance(v, dict) else ""


def js(br, body):
    return json.loads(br.evaluate("JSON.stringify((function(){%s})())" % body))


# BOTH THE COMPOSER'S OWN SCRIPT AND THE FIRST RECORD WAVE, TOGETHER (2026-08-19). Before today
# `pass.works` sat in `config.json` itself, so every record was already in hand the instant the page
# loaded, and a wait on the composer's own state was the whole of what a real step needed. Now a
# record wave is a request of its own (EX-PASS-RECORDS), landing on its own clock beside the
# composer's fetch, with no order between the two. A step or a declare taken before the wave lands
# composes nothing — the walk's own glide plays — and every row below that reads a passage, a family
# or a distance off a real crossing was reading a glide instead, at whatever generation and seed the
# walk happened to be on when the wave finally did land. `enter()` and every wait below it read both
# facts together, on every tick, until both hold or the budget (150 ticks, 30s — generous against
# this suite's own fresh Chrome launch under a loaded machine) runs out.
def wait_ready(br, budget=150):
    for _ in range(budget):
        got = js(br, "if (!window.__exPass) return {st: null, held: 0};"
                     "var r = window.__exPass.report();"
                     "return {st: r.composer.state, held: r.records.held,"
                     " waves: r.records.waves, inflight: r.records.inflight};")
        # HELD ALONE IS NOT READY (2026-08-19, after this suite came back 14/2 and then 16/0 on two
        # runs of the same tree). A first wave can hold every id it asked for while a second is still
        # on the wire, so a wait on the count alone lets a row read the walk mid-answer — which is
        # exactly the intermittent this suite showed. Ready is: the composer has landed, at least one
        # wave has been sent, and no wave is still in flight.
        if (got.get("st") == "read" and (got.get("waves") or 0) > 0
                and (got.get("inflight") or 0) == 0 and (got.get("held") or 0) > 1):
            return True
        br.sleep(0.2)
    return False


# EX-PASS-RECORDS (2026-08-19): `pass.works` left config.json — the site now carries `pass.records`
# (a route + a cap) and the id → record map is answered over that route instead, the way a Cloudflare
# Worker answers it in production (engine/assets/worker.js's `passRecordsRoute`). This suite serves
# the same contract locally through the harness's `answer` hook (tests/headless_harness.py's `serve`,
# threaded through by tests/headless.py) — RECORDS_STORE is filled by `put_records` below and read by
# `records_answer`, a MUTABLE dict shared by both so a hook bound into `serve(...)` before any id is
# known still sees records `put_records` writes afterward.
RECORDS_ROUTE = "/api/pass/records"
RECORDS_CAP = 20   # spread_size 10 + max_unfolds 2 × unfold_step 5 — the built-in defaults (build.py)
RECORDS_STORE = {}


def records_answer(raw_path):
    """The harness's `answer` hook for this suite: answers `GET /api/pass/records?ids=...` the way
    the Worker does — over-cap or empty is refused with 400, an id `RECORDS_STORE` does not carry is
    simply left out of the answer."""
    if not raw_path.startswith(RECORDS_ROUTE):
        return None
    ids = [i for i in parse_qs(urlparse(raw_path).query).get("ids", [""])[0].split(",") if i]
    if not ids or len(ids) > RECORDS_CAP:
        return (400, "text/plain", "bad request")
    out = {i: RECORDS_STORE[i] for i in ids if i in RECORDS_STORE}
    return (200, "application/json", json.dumps({"records": out}))


def put_records(base_dir, ids):
    """The settings record as the site writes it for the composed road: the collection's own
    constants and one record per work on the walk. The fixture's two records are re-keyed onto the
    works this bake hangs — what the composer reads is measurement, and the id is only its name."""
    cfg = json.loads((base_dir / "config.json").read_text(encoding="utf-8"))
    fix = json.loads(FIXTURE.read_text(encoding="utf-8"))
    src = [fix["works"][fix["pair"]["a"]], fix["works"][fix["pair"]["b"]]]
    works = {}
    for i, wid in enumerate(ids):
        rec = json.loads(json.dumps(src[i % 2]))
        rec["id"] = wid
        works[wid] = rec
    RECORDS_STORE.update(works)
    cfg["pass"] = dict(cfg.get("pass") or {}, visualLayer="pass", composer=fix["consts"],
                       records={"route": RECORDS_ROUTE, "cap": RECORDS_CAP})
    (base_dir / "config.json").write_text(
        json.dumps(cfg, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return works


# The picture layer of this suite. The record is written only for a passage that actually DREW, and
# what says one drew is the host's own report; a stub host stands in for the renderer so the walk's
# memory is measured on every machine and not only on one with a working WebGL2 context. Nothing
# here draws and nothing here decides: it reports one instrument and one live cue, which is exactly
# what the landing reads.
STUB = """
  if (!window.__exPassLayer) return {no: true};
  window.__exPassLayer({
    offer: function () { return true; },
    report: function () { return {active: false, instrument: 'stub',
                                  census: {buffer: '800x600', dpr: 1},
                                  stack: [{id: 'pivot', instrument: 'stub', handles: {}}]}; },
    cancel: function () {}, resize: function () {}
  });
  return {no: false};
"""

DECLARE = """
  var A = document.querySelector('.exh-frame[data-id="%s"]');
  var B = document.querySelector('.exh-frame[data-id="%s"]');
  if (!A || !B) return {absent: true};
  var cmd = window.__exPass.adapter.declare({fromEl: A, toEl: B, dir: 1, span: 100,
                                             kind: 'step', cause: '%s', velocity: 0});
  window.__cmd = cmd;
  var rows = window.__exPass.report().composer.passages;
  var row = rows.length ? rows[rows.length - 1] : null;
  var said = window.__exPass.report().refusals.filter(function (x) { return x.what === 'memory'; });
  var no = window.__exPass.report().refusals.filter(function (x) { return x.what === 'declare'; });
  return {absent: false, got: !!cmd, hasScore: !!(cmd && cmd.score),
          request: row ? row.request : null, memory: row ? row.memory : null,
          key: row ? row.key : null, declined: row ? row.declined : null,
          family: row ? row.family : null,
          trace: cmd && cmd.score ? window.__exPass.memory.trace(cmd.score) : null,
          json: cmd && cmd.score ? JSON.stringify(cmd.score) : null,
          why: said.length ? said[said.length - 1].why : null,
          noWhy: no.length ? no[no.length - 1].why : null};
"""

LAND = """
  var cmd = window.__cmd;
  if (!cmd) return {no: true};
  window.__exPass.adapter.dock(cmd);
  var r = window.__exPass.report();
  return {no: false, storage: r.memory.storage, edges: r.memory.edges};
"""


def declare(br, a, b, cause):
    """One step declared programmatically. Two declares inside one animation frame are refused by
    law (§1.1), and a headless browser can hold a frame open far longer than a person's hand does,
    so a refusal for that one reason is waited out rather than read as an answer."""
    for _ in range(10):
        got = js(br, DECLARE % (a, b, cause))
        if got.get("absent") or got.get("got") or "one frame" not in (got.get("noWhy") or ""):
            return got
        br.sleep(0.3)
    return got


def land(br, edge=None):
    """Dock the standing command, and — where the caller names the edge — wait until the walk has
    actually WRITTEN that edge's record before handing back.

    The record is what a second pass over the same edge reads: without it the walk has no memory of
    the first pass and rolls a fresh family, which is the row's own red. Docking starts the passage;
    the record is written where it lands, one clock later. Until 2026-08-19 the wait between the two
    was whatever the next statement happened to cost, and this suite came back green twice and red
    once over the same tree because of it. The row now waits for the fact it depends on."""
    got = js(br, LAND)
    if edge:
        for _ in range(40):
            rows = js(br, "return (window.__exPass.report().memory.edges || [])"
                          ".map(function(r){return r.edgeKey;});")
            if edge in (rows or []):
                break
            br.sleep(0.2)
        got = js(br, "var r = window.__exPass.report();"
                     "return {no: false, storage: r.memory.storage, edges: r.memory.edges};")
    return got


def enter(br, base, pass_arg=None, step=True, clear=True):
    """A visitor who opens the door and stands in the walk. `step` takes one real step, which is the
    only road that asks for the picture layer's file; `clear` is what makes a visit a FIRST one."""
    br.navigate(base + "/")
    if clear:
        br.clear_storage()
    br.navigate(base + "/" + (("?pass=" + pass_arg) if pass_arg else ""))
    br.sleep(0.8)
    # A visitor whose place the walk already remembers is put back in the walk and never meets the
    # door again, so the door is knocked on only where it stands.
    if br.evaluate("String(!!document.querySelector('.exd-window'))") == "true":
        try:
            br.click(".exd-window", settle=1.4)
        except RuntimeError:
            br.sleep(1.0)
    for _ in range(25):
        if br.evaluate("String(document.documentElement.classList.contains('ex-walk') "
                       "&& !document.documentElement.classList.contains('ex-face'))") == "true":
            break
        br.sleep(0.2)
    br.sleep(0.4)
    if step:
        # THE STEP WAITS ON THE COMPOSER AND THE RECORD WAVE TOGETHER, THE SAME AS THE STEP IT
        # STANDS IN FOR (2026-08-19). Pressing ArrowDown before either has landed composes nothing —
        # the walk's own glide plays — and every generation this visit spends afterward is one
        # generation off from what a reader downstream expects to find at that step.
        wait_ready(br)
        br.key("ArrowDown")
        for _ in range(30):
            if br.evaluate("String(!!(window.__exPass && window.__exPass.layer()))") == "true":
                break
            br.sleep(0.2)
        br.sleep(0.5)


# THE PAIR THIS SUITE WALKS IS CHOSEN BY WHAT IT PROVES, never by taste: the first pair of this
# hang whose BOTH directions compose. A passage the composer declines for its own reasons — this
# collection is synthetic and some pairs cast no actors one way about — carries no score to remember,
# no family to hold and no trace to reverse, and a lane about the memory of an edge would then be
# measuring nothing. The walk deals afresh on every entry, so the choice is made again after each.
PICK = """
  var ids = %s, out = null;
  for (var i = 0; i < ids.length && !out; i++) {
    for (var j = 0; j < ids.length && !out; j++) {
      if (i === j) continue;
      var A = document.querySelector('.exh-frame[data-id="' + ids[i] + '"]');
      var B = document.querySelector('.exh-frame[data-id="' + ids[j] + '"]');
      if (!A || !B) continue;
      var f = window.__exPass.passage(window.__exPass.request(A, B));
      var b = window.__exPass.passage(window.__exPass.request(B, A));
      if (f && f.score && b && b.score) out = [ids[i], ids[j]];
    }
  }
  return {pair: out};
"""


def shown_pair(br, recorded):
    got = js(br, "return {ids: [].slice.call(document.querySelectorAll('.exh-frame'))"
                 ".map(function (e) { return e.dataset.id; })};")["ids"]
    here = [w for w in got if w in recorded]
    pair = js(br, PICK % json.dumps(here))["pair"]
    return (pair or []), got


def same_pair(br, recorded, want):
    """The pair a later entry walks: the one the earlier entry walked, where this hang still shows
    both of its works."""
    got = js(br, "return {ids: [].slice.call(document.querySelectorAll('.exh-frame'))"
                 ".map(function (e) { return e.dataset.id; })};")["ids"]
    return want if (want[0] in got and want[1] in got) else []


if not chrome_available():
    for r in BROWSER_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
else:
    with serve(TMP, answer=records_answer) as base:
        with Browser(width=1280, height=900) as br:
            enter(br, base, "diagnostics:on,familySeed:4242")
            allworks = js(br, "return {ids: [].slice.call(document.querySelectorAll('.exh-frame'))"
                              ".map(function (e) { return e.dataset.id; })};")["ids"]
            recorded = list(put_records(TMP, allworks[:-1])) if len(allworks) >= 3 else []
            if len(recorded) < 2:
                for r in BROWSER_ROWS:
                    skip(r, f"the walk hung fewer than three works: {allworks[:4]}")
            else:
                enter(br, base, "diagnostics:on,familySeed:4242")
                wait_ready(br)
                pair, shown = shown_pair(br, recorded)
                stub = js(br, STUB)
                if len(pair) < 2 or stub.get("no"):
                    for r in BROWSER_ROWS:
                        skip(r, "this hang shows fewer than two recorded works"
                                if len(pair) < 2 else
                                "no picture layer door on this device: the walk asked for none")
                else:
                    A, B = pair[0], pair[1]
                    EDGE = "__".join(sorted([A, B]))

                    # 0 · the first pass, and the record the landing writes -------------------
                    first = declare(br, A, B, "first")
                    landed = land(br)
                    rec = [e for e in landed["edges"] if e["edgeKey"] == EDGE]
                    check(BROWSER_ROWS[0],
                          first["hasScore"] and first["request"]["sessionMemory"] is None
                          and len(rec) == 1 and rec[0]["passCount"] == 1
                          and bool(rec[0]["family"]) and bool(rec[0]["pivot"])
                          and rec[0]["previousScenePlanId"] is None
                          and rec[0]["traceCues"] > 0,
                          f"nothing crossed on the first pass; the record now reads "
                          f"{json.dumps(rec[0] if rec else None, ensure_ascii=False)[:300]}")

                    # 1 · the record's own names ---------------------------------------------
                    raw = js(br, "var s = localStorage.getItem('ex-pass-edges');"
                                 "return {store: s ? JSON.parse(s) : null};")["store"]
                    names = set()
                    for edge in (raw or {}).get("edges", {}).values():
                        for row in edge.values():
                            names |= set(row.keys())
                    named = {"edgeKey", "direction", "family", "pivot", "seed", "passCount",
                             "lastAt", "cooldown", "provenance"}
                    check(BROWSER_ROWS[1],
                          bool(raw) and raw.get("v") == 1 and names == named,
                          f"the stored record's own names: {sorted(names)}; §4.8 names "
                          f"{sorted(named)}")

                    # 2 · walking back: the return reference, and nothing wider ---------------
                    back = declare(br, B, A, "back")
                    crossed = back["request"]["sessionMemory"]
                    check(BROWSER_ROWS[2],
                          isinstance(crossed, dict)
                          and sorted(crossed.keys()) == ["family", "passIndex", "seed"]
                          and crossed["family"] == rec[0]["family"]
                          and crossed["seed"] == rec[0]["seed"]
                          and crossed["passIndex"] == rec[0]["passCount"],
                          f"what crossed: {json.dumps(crossed, ensure_ascii=False)}")

                    # 3 · kin, and other ------------------------------------------------------
                    judged = js(br, """
                      var rows = window.__exPass.passages();
                      var row = rows[rows.length - 1];
                      var all = window.__exPass.memory.all();
                      var before = all['%s'] ? (all['%s']['a-to-b'] || all['%s']['b-to-a']) : null;
                      return {verdict: window.__exPass.memory.judge(row, before) || null,
                              family: window.__exPass.memory.family(row.plan),
                              was: before ? before.family : null,
                              pivot: window.__exPass.memory.pivot(row.plan),
                              wasPivot: before ? before.pivot : null};
                    """ % (EDGE, EDGE, EDGE))
                    check(BROWSER_ROWS[3],
                          back["hasScore"] and _why(judged["verdict"]) == ""
                          and _dist(judged["verdict"]) is None
                          and (judged["family"] == judged["was"]
                               or judged["pivot"] == judged["wasPivot"])
                          and back["json"] != first["json"],
                          f"the way back holds the family «{judged['family']}» against the recorded "
                          f"«{judged['was']}» and plays a different score "
                          f"({len(back['json'] or '')} B against {len(first['json'] or '')} B); the "
                          f"walk's own reading of it carries no sentence and no distance: "
                          f"{judged['verdict']!r}")

                    # 4 · reading one · neither the family nor the pivot ----------------------
                    # The record is replaced by one no passage on this edge can be kin to. This was
                    # a refusal until 2026-08-18 and cost the visitor the whole crossing; his word
                    # of 09:51 — any two photographs in the world get a crossing, always — struck
                    # that out.
                    #
                    # UPDATED 2026-08-25 for the return-hysteresis rebuild (exhibition.js,
                    # `passComposeFor`'s `heldStart` pre-check, 2026-08-24 night audit): a return no
                    # longer races several scored dice against the recorded family/pivot. It replays
                    # the composer with the EXACT question the held pass was struck on (same seed,
                    # same walk-memory anchored at the edge's first pass) and takes that candidate
                    # directly the instant it legally casts, before any dice loop runs. The kinship
                    # ranking this row exercises still happens — `passEdgeJudge` still reads the held
                    # pass against the (now alien) recorded family/pivot and still says so on the
                    # diagnostic surface — but it no longer gates whether a second or third die gets
                    # rolled, because there IS no race for a held pass to lose. So this row now holds
                    # two things, not three: a score is frozen onto the command on the FIRST and only
                    # die (the held replay), and the mismatch is still said rather than swallowed.
                    js(br, """
                      var all = window.__exPass.memory.all();
                      var e = all['%s'];
                      var d = e['a-to-b'] ? 'a-to-b' : 'b-to-a';
                      window.__kept = JSON.parse(JSON.stringify(e[d]));
                      e[d].family = 'no_such_transform+no_such_axis';
                      e[d].pivot = {kind: 'no-such-pivot', measure: null, cut: null,
                                    transform: 'no_such_transform'};
                      e[d].lastAt = Date.now();
                      return {planted: e[d].family};
                    """ % EDGE)
                    alien = declare(br, B, A, "alien")
                    check(BROWSER_ROWS[4],
                          alien["got"] and alien["hasScore"] is True
                          and len(alien["memory"]["rolls"]) == 1
                          and any("shares neither the family" in (r.get("why") or "")
                                  for r in alien["memory"]["rolls"]),
                          f"the command carries {('a score' if alien['hasScore'] else 'no score')} "
                          f"after {len(alien['memory']['rolls'])} dice, and the alien record is "
                          f"named on the surface rather than charged to the visitor: "
                          f"{[(r.get('why') or '')[:90] for r in alien['memory']['rolls']]!r}")

                    # 5 · reading two · the recorded pass played backwards --------------------
                    # THIS WAS A REFUSAL UNTIL 2026-08-18 AND IS A RANKING NOW. His word of 09:51:
                    # any two photographs in the world get a crossing, always — so a pass that reads
                    # as the recorded one played backwards is no longer refused the crossing. It is
                    # measured: `judge` hands back a DISTANCE, and of the three dice this edge is
                    # offered the roll standing FURTHEST from the recorded pass's mirror plays. A
                    # mirror stands at a distance of about nothing, which is the shortest distance
                    # there is, so it ranks last — and a pass with no reading to take answers with
                    # no distance at all, which the walk's own scoring reads as the whole point.
                    # The row proves both readings on one pass, in the numbers the walk itself uses.
                    # THE MIRROR IS MADE EXACT BY CONSTRUCTION, and an earlier form of this row was
                    # not. That form planted the reverse of a trace read at one die and then chased
                    # that same die again across reloads, so it met a true mirror only where two
                    # passes composed at different pass indexes happened to agree cue for cue and
                    # handle for handle. The moment the walk began stating a step's ROLE (U27 stage
                    # 2) and the engine began choosing between several instruments that cut on one
                    # kind, they stopped agreeing — and the row went red on a checker nobody had
                    # touched. A row that cannot reproduce the condition it names guards nothing.
                    #
                    # So it composes the very pass it is about to judge, plants THAT pass's own
                    # trace reversed as the record, and asks the walk's own judge. The candidate is
                    # then the recorded pass run backwards to the last handle, which is exactly the
                    # condition §4.8 ranks lowest.
                    #
                    # WHY A ONE-CUE PASS LIES OUTSIDE THIS ROW'S REACH, and this is the second half
                    # the earlier form did not have (U27 stage 2, 2026-08-18). Making the mirror was
                    # never enough: the mirror also has to be DETECTABLE, and on a pass that is
                    # ALREADY its own mirror it is not. The charter's voice budget gives a quiet
                    # link exactly one move from the vocabulary, and a single cue spanning the whole
                    # passage with every handle standing at one value reads the same forwards and
                    # backwards — reversing it returns it unchanged. §4.8 ranks a replay last
                    # because a replay says the way back was not authored; a pass identical to its
                    # own reverse makes no claim about authorship either way, so the walk TAKES NO
                    # READING there, by the clause in `passMirrorDistance` that compares the record
                    # against its own mirror first and answers with nothing where the record is
                    # already its own. That is the product behaving as designed, and a row standing
                    # its reading on such a pass is asking the walk a question it never asks.
                    #
                    # So the row goes and FINDS an asymmetric pass — more than one cue, where a
                    # reversal is a real claim — walking the ordered pairs this hang shows at every
                    # role the walk can state a step to be, and stands the reading there. It also
                    # keeps a one-cue pass it met on the way and shows, measured rather than argued,
                    # that the walk answers nothing on it: that is the reach of this row stated in
                    # its own numbers. Where the whole hang offers no pass of more than one cue the
                    # row SKIPS and says so — a condition it cannot produce is a condition it cannot
                    # guard, and a green line there would be a lie.
                    #
                    # The record row 4 replaced with an alien one is put back first, so the composer
                    # reads this edge's real memory rather than the plant left standing above.
                    #
                    # The other half — that a refused pass freezes NO score onto the command and the
                    # visitor lands on the walk's own glide — travels the same road and is held by
                    # row 4 above, which drives it end to end.
                    mirror = js(br, """
                      var all = window.__exPass.memory.all();
                      var e = all['%s'];
                      if (e && window.__kept) {
                        var d = e['a-to-b'] ? 'a-to-b' : 'b-to-a';
                        e[d] = JSON.parse(JSON.stringify(window.__kept));
                      }
                      function rev(t) {
                        return {ms: t.ms, cues: t.cues.slice().reverse().map(function (c) {
                          var h = {};
                          Object.keys(c.h).forEach(function (n) { h[n] = [c.h[n][1], c.h[n][0]]; });
                          return {id: c.id, i: c.i, w: [1 - c.w[1], 1 - c.w[0]], h: h};
                        })};
                      }
                      function judgeAgainst(got, trace) {
                        return window.__exPass.memory.judge(got, {
                          family: window.__exPass.memory.family(got.plan),
                          pivot: window.__exPass.memory.pivot(got.plan),
                          provenance: {trace: trace}}) || null;
                      }
                      var ids = [].slice.call(document.querySelectorAll('.exh-frame'))
                                  .map(function (el) { return el.dataset.id; });
                      var roles = ['culmination', 'middle', 'entrance', 'return', 'quiet link'];
                      var tried = [], many = null, one = null;
                      for (var i = 0; i < ids.length && !many; i++) {
                        for (var j = 0; j < ids.length && !many; j++) {
                          if (i === j) continue;
                          var A = document.querySelector('.exh-frame[data-id="' + ids[i] + '"]');
                          var B = document.querySelector('.exh-frame[data-id="' + ids[j] + '"]');
                          var req = (A && B) ? window.__exPass.request(A, B) : null;
                          if (!req) continue;
                          for (var k = 0; k < roles.length && !many; k++) {
                            req.routeRole = roles[k];
                            var got = window.__exPass.passage(req);
                            if (!got || !got.score) continue;
                            var t = window.__exPass.memory.trace(got.score);
                            if (!t || !t.cues.length) continue;
                            tried.push({role: roles[k], cues: t.cues.length});
                            var cand = {role: roles[k], from: ids[i], to: ids[j], got: got, t: t};
                            if (t.cues.length > 1) many = cand;
                            else if (!one) one = cand;
                          }
                        }
                      }
                      if (!many) {
                        return {none: true, tried: tried.length,
                                widest: tried.reduce(function (m, r) {
                                  return Math.max(m, r.cues); }, 0),
                                // what the walk answers on the one-cue pass this hang does offer,
                                // which is the reason the row cannot stand here
                                oneCueVerdict: one ? judgeAgainst(one.got, rev(one.t)) : null};
                      }
                      return {none: false, cues: many.t.cues.length, role: many.role,
                              tried: tried.length,
                              kin: window.__exPass.memory.family(many.got.plan),
                              verdict: judgeAgainst(many.got, rev(many.t)),
                              // The same pass read against its OWN trace, unreversed: a pass is not
                              // a replay of itself, so no distance applies and the reading is empty.
                              forward: judgeAgainst(many.got, many.t),
                              // AND THE ROW'S OWN REACH, measured: a one-cue pass is its own mirror,
                              // so the walk takes no reading on it and this row could not stand there
                              oneCue: one ? one.t.cues.length : null,
                              oneCueRole: one ? one.role : null,
                              oneCueVerdict: one ? judgeAgainst(one.got, rev(one.t)) : null};
                    """ % EDGE)
                    if mirror.get("none"):
                        skip(BROWSER_ROWS[5],
                             f"every one of the {mirror.get('tried')} passes this hang composes "
                             f"carries a single cue (widest {mirror.get('widest')}), and a one-cue "
                             f"pass whose handles stand still IS its own mirror — the walk takes no "
                             f"reading on such a record on purpose, answering a distance of "
                             f"{_dist(mirror.get('oneCueVerdict'))!r}, so there is no reversal here "
                             f"to rank and nothing this row could prove")
                    else:
                        # the reach is only stated where a one-cue pass was actually met on the way;
                        # where the first pass composed already carried several cues there is no
                        # such measurement to report, and the row says nothing it did not measure
                        reach = (
                            f" The row's reach, measured on the way: the one-cue pass at the role "
                            f"«{mirror.get('oneCueRole')}» is its own mirror and the walk answers a "
                            f"distance of {_dist(mirror.get('oneCueVerdict'))!r} on it, which is "
                            f"why the reading is stood on a pass of more than one cue."
                            if mirror.get("oneCue") else
                            " No one-cue pass was met on the way: the first pass this hang composed "
                            "already carried several cues, so the reversal is a real claim on it.")
                        # WHAT THE WALK ITSELF DOES WITH THESE TWO NUMBERS, restated here in the
                        # walk's own arithmetic (`01a-pass.js`, the roll's score): a roll whose
                        # reading carries no distance is worth a whole point on the mirror reading,
                        # and a roll standing d away is worth min(1, d * 10). A mirror stands at
                        # about nothing, so it scores about nothing and every roll that is not a
                        # mirror outranks it. That is the rule the refusal was replaced by, and the
                        # row proves it on the two readings it took rather than by argument.
                        d_back = _dist(mirror.get("verdict"))
                        d_fwd = _dist(mirror.get("forward"))
                        mirror_rank = 0.0 if d_back is None else min(1.0, d_back * 10)
                        forward_rank = 1.0 if d_fwd is None else min(1.0, d_fwd * 10)
                        check(BROWSER_ROWS[5],
                              mirror.get("cues", 0) > 1
                              and d_back is not None and d_back < 0.05
                              and "played backwards" in _why(mirror.get("verdict"))
                              and d_fwd is None
                              and mirror_rank < forward_rank,
                              f"a pass of {mirror.get('cues')} cues at the role "
                              f"«{mirror.get('role')}» on the family «{mirror.get('kin')}», met as "
                              f"the record run backwards, stands {d_back!r} of the recorded pass's "
                              f"own range from it and is ranked at {mirror_rank:.4f} of the mirror "
                              f"reading's whole point: {_why(mirror.get('verdict'))[:180]!r}. The "
                              f"same pass met as the record run FORWARDS carries no distance at all "
                              f"({d_fwd!r}) and ranks at {forward_rank:.4f}, so the mirror is the "
                              f"last roll this walk will play and is never the refused one."
                              + reach
                              + f" {mirror.get('tried')} pass(es) composed to find one.")

                    # 6 · the drift ------------------------------------------------------------
                    # A fresh visit, so the two passes below are the first and the second of one
                    # edge inside one visit window.
                    enter(br, base, "diagnostics:on,familySeed:4242")
                    wait_ready(br)
                    pair2, _ = shown_pair(br, recorded)
                    js(br, STUB)
                    if len(pair2) < 2:
                        for r in BROWSER_ROWS[6:]:
                            skip(r, "this hang shows fewer than two recorded works")
                    else:
                        A, B = pair2[0], pair2[1]
                        EDGE = "__".join(sorted([A, B]))
                        one = declare(br, A, B, "drift-one")
                        land(br, EDGE)
                        two = declare(br, A, B, "drift-two")
                        drift = (two["memory"] or {}).get("drift")
                        check(BROWSER_ROWS[6],
                              two["hasScore"] and bool(drift) and drift["passes"] == 1
                              and len(drift["moved"]) > 0
                              and two["family"] == one["family"],
                              f"the second pass over this edge holds the family «{two['family']}» "
                              f"and moves {len(drift['moved']) if drift else 0} shaping number(s) "
                              f"at a reach of {drift['reach'] if drift else None}: "
                              + json.dumps(drift["moved"] if drift else None,
                                           ensure_ascii=False)[:260])

                        # 7 · what the drift never touches ---------------------------------
                        # Read off the score itself rather than off the drift's own account: every
                        # handle the composer measured off the works stands where it stood, every
                        # door still opens at 0 and closes at 1, and no clock moved.
                        held = js(br, """
                          var rows = window.__exPass.report().composer.passages;
                          var row = rows[rows.length - 1];
                          var moved = (row.memory && row.memory.drift)
                            ? Object.keys(row.memory.drift.moved) : [];
                          var bad = [], doors = [], spans = [];
                          (row.score ? row.score.cues : []).forEach(function (c) {
                            var instr = c.instrument.id;
                            Object.keys(c.tracks || {}).forEach(function (h) {
                              var slot = c.id + '.' + h;
                              var node = c.nodes[(c.tracks[h] || {}).node || (c.id + '-' + h)];
                              if (!node) return;
                              if (moved.indexOf(slot) < 0) return;
                              if (h === 'mix' || h === 'clock' || h === 'seed') bad.push(slot);
                              if (c.measuredHandles && c.measuredHandles[h] !== undefined) {
                                bad.push(slot);
                              }
                              var man = window.__exPass.report().composer;
                              spans.push(slot);
                            });
                            var mixNode = c.nodes[(c.tracks.mix || {}).node || (c.id + '-mix')];
                            if (mixNode && (mixNode.a !== 0 || mixNode.b !== 1)) doors.push(c.id);
                          });
                          return {bad: bad, doors: doors, moved: moved.length, spans: spans.length};
                        """)
                        check(BROWSER_ROWS[7],
                              held["moved"] > 0 and not held["bad"] and not held["doors"],
                              f"{held['moved']} number(s) drifted, none of them a measured handle, "
                              f"a door or a clock ({held['bad']}); every cue still enters at 0 and "
                              f"leaves at 1 ({held['doors'] or 'all of them'})")

                        # 8 · across the visit boundary ------------------------------------
                        old = js(br, """
                          var all = window.__exPass.memory.all();
                          var e = all['%s'];
                          var d = e['a-to-b'] ? 'a-to-b' : 'b-to-a';
                          var n = window.__exPass.memory.numbers;
                          e[d].lastAt = Date.now() - (n.visitWindowSeconds + 60) * 1000;
                          return {family: e[d].family, at: e[d].lastAt};
                        """ % EDGE)
                        stale = declare(br, A, B, "across")
                        m = stale["memory"] or {}
                        # A COOLDOWN RE-ROLLS THE DIE AND NEVER EMPTIES THE POOL — the lab
                        # builder's own law, and both halves of it are read here. What must hold
                        # unconditionally: nothing of the earlier pass crosses into the request,
                        # the family that played is named as cooling, the pass count starts again,
                        # and the crossing still plays. What holds CONDITIONALLY, and used to be
                        # asserted as though it were unconditional: another die is offered where the
                        # first one lands on the cooled family. It does not always land there —
                        # since the walk began stating a step's role (U27 stage 2) a step beyond the
                        # visit window is no longer a return, so its road is chosen from the curve's
                        # own register and usually carries a different family, and no second die is
                        # needed. The row therefore measures the law and prints which of the two
                        # branches this run took, instead of reddening on the branch it did not.
                        #
                        # THE OTHER BRANCH NO LONGER ASSERTS A DIE COUNT (2026-09-01, Phase 5).
                        # It used to read `len(rolls) == 1` where the cooled family did not come
                        # up — «the first clean die ends the race» — which was never the law this
                        # row names, only an incidental fact about the stopping rule that stood at
                        # the time. Phase 5 retired that stop: on an edge met outside the visit
                        # window `passEdgeJudge` has no recorded pass to read, so it answers kin
                        # for every candidate and null for every distance, and a stop asking for
                        # those would fire on die 0 of every such edge and collapse the race to a
                        # single die — which is the defect the 2026-08-25 sweep already repaired
                        # once (`tests/test_pass_roll.py` R11 proves it by construction). What the
                        # law actually says is read instead: the pool is never emptied, so a
                        # crossing still plays, and the race stays inside the dice the walk allows.
                        rolls = m.get("rolls") or []
                        dice = int(re.search(r"dice:\s*(\d+)", SRC).group(1))
                        cooled_came_up = any(r.get("why") and "still cooling" in r["why"]
                                             for r in rolls)
                        check(BROWSER_ROWS[8],
                              stale["hasScore"] and stale["request"]["sessionMemory"] is None
                              and m.get("cooled") == old["family"]
                              and m.get("passes") == 0
                              and 1 <= len(rolls) <= dice
                              and (len(rolls) > 1 if cooled_came_up else True),
                              f"nothing crossed; the family «{m.get('cooled')}» is cooling and the "
                              f"pass count starts again at {m.get('passes')}; the crossing still "
                              f"plays ({'a score' if stale['hasScore'] else 'no score'}). "
                              + (f"The first die landed on the cooled family, so another was "
                                 f"offered — {len(rolls)} in all, and a pool that was never "
                                 f"emptied" if cooled_came_up else
                                 f"The first die of {len(rolls)} carried the family "
                                 f"«{rolls[0].get('family') if rolls else None}», which is not the "
                                 f"cooled one, so no second die was owed — the race rolled "
                                 f"{len(rolls)} of the {dice} the walk allows"))

                        # 9 · the record survives a reload --------------------------------
                        enter(br, base, "diagnostics:on,familySeed:4242")
                        wait_ready(br)
                        pair3, _ = shown_pair(br, recorded)
                        js(br, STUB)
                        if len(pair3) < 2:
                            for r in BROWSER_ROWS[9:]:
                                skip(r, "this hang shows fewer than two recorded works")
                        else:
                            A, B = pair3[0], pair3[1]
                            EDGE = "__".join(sorted([A, B]))
                            declare(br, A, B, "before-reload")
                            land(br)
                            enter(br, base, "diagnostics:on,familySeed:4242", clear=False)
                            wait_ready(br)
                            after = same_pair(br, recorded, [A, B])
                            js(br, STUB)
                            if len(after) != 2:
                                skip(BROWSER_ROWS[9],
                                     "the reloaded walk hung another pair of works")
                            else:
                                again2 = declare(br, A, B, "after-reload")
                                landed2 = land(br)
                                rec2 = [e for e in landed2["edges"] if e["edgeKey"] == EDGE]
                                check(BROWSER_ROWS[9],
                                      landed2["storage"] == "read"
                                      and bool(again2["request"]["sessionMemory"])
                                      and len(rec2) >= 1
                                      and max(e["passCount"] for e in rec2) == 2,
                                      f"the storage reads {landed2['storage']!r}; the reference "
                                      f"that crossed after the reload: "
                                      f"{json.dumps(again2['request']['sessionMemory'])}; the "
                                      f"record now stands at pass "
                                      f"{max(e['passCount'] for e in rec2) if rec2 else None}")

                            # 10 · a cleared storage ---------------------------------------
                            enter(br, base, "diagnostics:on,familySeed:4242")
                            wait_ready(br)
                            pair4, _ = shown_pair(br, recorded)
                            js(br, STUB)
                            if len(pair4) < 2:
                                skip(BROWSER_ROWS[10], "this hang shows fewer than two recorded "
                                                       "works")
                            else:
                                cleared = declare(br, pair4[0], pair4[1], "cleared")
                                landedc = land(br)
                                check(BROWSER_ROWS[10],
                                      landedc["storage"] == "fresh"
                                      and cleared["request"]["sessionMemory"] is None
                                      and cleared["hasScore"],
                                      f"the storage reads {landedc['storage']!r} and nothing "
                                      f"crossed; the crossing still composed "
                                      f"({'a score' if cleared['hasScore'] else 'no score'})")

                            # 11 · a storage that will not open ----------------------------
                            with Browser(width=1280, height=900) as br2:
                                br2.navigate(base + "/")
                                br2.clear_storage()
                                br2.navigate(base + "/?pass=diagnostics:on")
                                br2.sleep(0.6)
                                br2.evaluate(
                                    "(function(){var real = localStorage.getItem.bind(localStorage);"
                                    "localStorage.getItem = function (k) {"
                                    "  if (String(k).indexOf('pass-edges') >= 0) {"
                                    "    throw new Error('denied'); }"
                                    "  return real(k); };})()")
                                br2.click(".exd-window", settle=1.4)
                                for _ in range(25):
                                    if br2.evaluate(
                                            "String(document.documentElement.classList"
                                            ".contains('ex-walk'))") == "true":
                                        break
                                    br2.sleep(0.2)
                                # THE WAIT COMES BEFORE THE KEY HERE TOO (2026-08-19), the same fix
                                # as `enter()`'s own step above: a key pressed before the composer
                                # and the record wave are both in hand composes nothing, and this
                                # row is precisely about the crossing still composing (`hasScore`)
                                # despite the closed storage, so the composer has to be given the
                                # chance to actually run first.
                                wait_ready(br2)
                                br2.key("ArrowDown")
                                pair5, _ = shown_pair(br2, recorded)
                                if len(pair5) < 2:
                                    skip(BROWSER_ROWS[11], "this hang shows fewer than two "
                                                           "recorded works")
                                else:
                                    shut = declare(br2, pair5[0], pair5[1], "shut")
                                    rep = js(br2, "var r = window.__exPass.report();"
                                                  "var said = r.refusals.filter(function (x) {"
                                                  "  return x.what === 'memory'; });"
                                                  "return {storage: r.memory.storage,"
                                                  " why: said.length ? said[0].why : null};")
                                    check(BROWSER_ROWS[11],
                                          rep["storage"] == "unavailable"
                                          and "storage is closed" in (rep["why"] or "")
                                          and shut["hasScore"],
                                          f"the storage reads {rep['storage']!r} and says "
                                          f"{(rep['why'] or '')[:90]!r}; the crossing still "
                                          f"composed "
                                          f"({'a score' if shut['hasScore'] else 'no score'})")

                            # 12 · the store stays bounded ---------------------------------
                            planted = js(br, """
                              var all = window.__exPass.memory.all();
                              var n = window.__exPass.memory.numbers;
                              var now = Date.now();
                              for (var i = 0; i < n.keep + 20; i++) {
                                all['planted-' + i + '__planted-' + i] = {'a-to-b': {
                                  edgeKey: 'planted-' + i + '__planted-' + i, direction: 'a-to-b',
                                  family: 'planted+planted', pivot: {kind: 'p', measure: null,
                                                                     cut: null, transform: 'p'},
                                  seed: 1, passCount: 1, lastAt: now - (i + 1) * 1000,
                                  cooldown: {seconds: n.cooldownSeconds,
                                             familyCooledUntil: now + n.cooldownSeconds * 1000},
                                  provenance: {planId: null, previousScenePlanId: null,
                                               trace: null}}};
                              }
                              return {planted: Object.keys(all).length, keep: n.keep};
                            """)
                            declare(br, pair4[0], pair4[1], "prune")
                            land(br)
                            after_put = js(br, "var s = localStorage.getItem('ex-pass-edges');"
                                               "var o = s ? JSON.parse(s) : {edges: {}};"
                                               "var n = 0;"
                                               "Object.keys(o.edges).forEach(function (k) {"
                                               "  n += Object.keys(o.edges[k]).length; });"
                                               "return {rows: n, bytes: s ? s.length : 0};")
                            check(BROWSER_ROWS[12],
                                  after_put["rows"] <= planted["keep"],
                                  f"{planted['planted']} edges were planted against a store that "
                                  f"keeps {planted['keep']}; the browser now holds "
                                  f"{after_put['rows']} record(s), weighing "
                                  f"{after_put['bytes']} B")

                            # 13 · ?reset forgets the edges walked ------------------------
                            # EX-RESET / INV-35: the museum forgets THIS browser, and forgetting is
                            # whole. The edges a visitor walked are as much of that as the tongue
                            # they read in. Reverting the one line that drops this key reddens here.
                            before_reset = js(br, "return {has: !!localStorage.getItem("
                                                  "'ex-pass-edges')};")
                            br.navigate(base + "/?reset")
                            br.sleep(1.0)
                            gone = js(br, "return {has: !!localStorage.getItem('ex-pass-edges')};")
                            check(BROWSER_ROWS[13],
                                  before_reset["has"] and not gone["has"],
                                  f"the browser held records before the wipe: "
                                  f"{before_reset['has']}; it holds them after: {gone['has']}")

import shutil  # noqa: E402
shutil.rmtree(TMP, ignore_errors=True)

passed = sum(1 for _, s, _ in results if s == "PASS")
failed = sum(1 for _, s, _ in results if s == "FAIL")
skipped = sum(1 for _, s, _ in results if s == "SKIP")
print()
for name, status, detail in results:
    line = f"{status}  {name}"
    if detail:
        line += f"   — {detail}"
    print(line)
print(f"\n{passed} passed / {failed} failed / {skipped} skipped")
sys.exit(1 if failed else 0)
