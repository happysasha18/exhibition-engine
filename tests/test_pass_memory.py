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
import sys
import tempfile
from pathlib import Path

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

check("EX-MEMORY the four numbers no measurement gives stand in one place, at the values the lab "
      "recorded",
      all(s in SRC for s in ("visitWindowSeconds: 1800", "cooldownSeconds: 86400",
                             "driftSpan: 0.25", "reversalMean: 0.02", "reversalWorst: 0.05")),
      "a later pass tunes the whole list at once, so the list is one record and not five constants "
      "spread through the file")

# ---------------------------------------------------------------- the walk, in a browser

BROWSER_ROWS = [
    "EX-MEMORY a first pass on an edge carries no memory, and the landing writes the edge record",
    "EX-MEMORY the record holds §4.8's own names and nothing about the person",
    "EX-MEMORY walking back hands the composer the return reference and nothing wider",
    "EX-MEMORY the backward passage is kin to the forward one and is not it played backwards",
    "EX-MEMORY refusal · a backward plan sharing neither the family nor the pivot never plays",
    "EX-MEMORY refusal · a pass that reads as the recorded one reversed never plays",
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


def js(br, body):
    return json.loads(br.evaluate("JSON.stringify((function(){%s})())" % body))


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
    cfg["pass"] = dict(cfg.get("pass") or {}, visualLayer="pass", composer=fix["consts"],
                       works=works)
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


def land(br):
    return js(br, LAND)


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
    with serve(TMP) as base:
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
                for _ in range(30):
                    if js(br, "return {s: window.__exPass.report().composer.state};")["s"] == "read":
                        break
                    br.sleep(0.2)
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
                          back["hasScore"] and judged["verdict"] is None
                          and (judged["family"] == judged["was"]
                               or judged["pivot"] == judged["wasPivot"])
                          and back["json"] != first["json"],
                          f"the way back holds the family «{judged['family']}» against the recorded "
                          f"«{judged['was']}» and plays a different score "
                          f"({len(back['json'] or '')} B against {len(first['json'] or '')} B); the "
                          f"walk's own verdict on it: {judged['verdict']!r}")

                    # 4 · refusal one · neither the family nor the pivot ----------------------
                    # The record is replaced by one no passage on this edge can be kin to. The walk
                    # must freeze no score onto the command and name why, so the visitor lands on
                    # the walk's own glide. Reverting the kinship check reddens this row.
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
                          alien["got"] and alien["hasScore"] is False
                          and "shares neither the family" in (alien["why"] or "")
                          and alien["memory"]["refused"] is not None
                          and len(alien["memory"]["rolls"]) > 1,
                          f"the command carries {('a score' if alien['hasScore'] else 'no score')} "
                          f"after {len(alien['memory']['rolls'])} dice; the reason on the surface: "
                          f"{(alien['why'] or '')[:170]!r}")

                    # 5 · refusal two · the recorded pass played backwards --------------------
                    # The trace of a pass that has just been composed is planted onto the record
                    # REVERSED, and the same pass is composed again after a reload at the same die,
                    # so the walk meets a pass that is the recorded one run backwards. The die is
                    # made of the visit's own seed, the pass index and the edge key, so the reload
                    # is pinned by `familySeed` and the pass index is walked back up to the one the
                    # trace was read at.
                    target = js(br, """
                      var all = window.__exPass.memory.all();
                      var e = all['%s'];
                      var d = e['a-to-b'] ? 'a-to-b' : 'b-to-a';
                      e[d] = window.__kept;
                      return {seed: null};
                    """ % EDGE)
                    # THE DIE THIS ROW HAS TO MEET AGAIN IS ROLLED AT A PASS INDEX, so the probe is
                    # taken at a HIGH one: a reloaded visit starts its own count at zero and walks
                    # up, and an index it has already passed can never come round again.
                    for _ in range(30):
                        js(br, """
                          var A = document.querySelector('.exh-frame[data-id="%s"]');
                          window.__exPass.adapter.declare({fromEl: null, toEl: A, dir: 1, span: 0,
                            kind: 'jump', cause: 'advance', velocity: 0});
                          return {done: true};
                        """ % A)
                        br.sleep(0.12)
                    probe = declare(br, B, A, "probe")
                    probe_dice = (probe.get("memory") or {}).get("rolls") or []
                    want_seed = probe_dice[0]["seed"] if probe_dice else None
                    trace = probe["trace"]
                    if not trace or want_seed is None or len(probe_dice) != 1:
                        skip(BROWSER_ROWS[5],
                             "the probe pass carried no trace to reverse"
                             if (not trace or want_seed is None) else
                             f"the probe crossing was offered {len(probe_dice)} dice, so its trace "
                             f"and its first die belong to different passes")
                    else:
                        js(br, """
                          var all = window.__exPass.memory.all();
                          var e = all['%s'];
                          var d = e['a-to-b'] ? 'a-to-b' : 'b-to-a';
                          var t = %s;
                          var rev = {ms: t.ms, cues: t.cues.slice().reverse().map(function (c) {
                            var h = {};
                            Object.keys(c.h).forEach(function (n) { h[n] = [c.h[n][1], c.h[n][0]]; });
                            return {id: c.id, i: c.i, w: [1 - c.w[1], 1 - c.w[0]], h: h};
                          })};
                          e[d].provenance.trace = rev;
                          e[d].lastAt = Date.now();
                          localStorage.setItem('ex-pass-edges',
                                               JSON.stringify({v: 1, edges: all}));
                          return {planted: rev.cues.length};
                        """ % (EDGE, json.dumps(trace)))
                        # The walk deals its works afresh on every entry, so the reloaded visit is
                        # opened until it hangs both works of this edge again.
                        again = []
                        for _ in range(5):
                            enter(br, base, "diagnostics:on,familySeed:4242", clear=False)
                            for _ in range(30):
                                if js(br, "return {s: window.__exPass.report().composer.state};"
                                      )["s"] == "read":
                                    break
                                br.sleep(0.2)
                            again = same_pair(br, recorded, [A, B])
                            if len(again) == 2:
                                break
                        js(br, STUB)
                        # THE DIE IS MADE OF THE VISIT'S SEED, THE PASS INDEX AND THE EDGE KEY, so
                        # the same step declared again after a pinned reload walks back up to the
                        # same die. The step is declared until the die the trace was read at comes
                        # round; nothing is landed on the way, so no record moves under the walk.
                        rev, aligned = None, False
                        if len(again) == 2:
                            for _ in range(60):
                                rev = declare(br, B, A, "reversed")
                                # The FIRST die of the crossing, which is the one the trace was
                                # read at; a crossing whose first die is refused rolls another, and
                                # the request then carries that one instead.
                                dice = (rev.get("memory") or {}).get("rolls") or []
                                seed = dice[0]["seed"] if dice else None
                                if seed is not None and abs(seed - want_seed) < 1e-9:
                                    aligned = True
                                    break
                        if not aligned:
                            skip(BROWSER_ROWS[5],
                                 "the reloaded walk hung this edge's two works again but never came "
                                 "back to the die the trace was read at"
                                 if len(again) == 2 else
                                 "five reloaded visits hung another pair of works, so the recorded "
                                 "pass could not be met again")
                        else:
                            read = js(br, """
                              var all = window.__exPass.memory.all();
                              var e = all['%s'] || {};
                              var rec = e['a-to-b'] || e['b-to-a'] || null;
                              var cmd = window.__cmd;
                              var t = cmd && cmd.score
                                ? window.__exPass.memory.trace(cmd.score) : null;
                              return {verdict: (t && rec)
                                        ? (window.__exPass.memory.reversed(
                                             t, rec.provenance.trace) || null) : null,
                                      seedNow: cmd && cmd.score ? cmd.score.seed : null,
                                      nowFirst: t ? t.cues[0] : null,
                                      beforeLast: (rec && rec.provenance.trace)
                                        ? rec.provenance.trace.cues[
                                            rec.provenance.trace.cues.length - 1] : null};
                            """ % EDGE)
                            # The pass that reads as the recorded one reversed is the one that
                            # never plays. The walk meets it on the die it was planted for, names
                            # it, and either finds another die whose pass is no replay or keeps its
                            # own glide; what it may never do is play the replay.
                            said = [r for r in (rev["memory"] or {}).get("rolls") or []
                                    if "played backwards" in (r.get("why") or "")]
                            check(BROWSER_ROWS[5],
                                  bool(said) and read["verdict"] is None,
                                  f"the die {want_seed} composed the recorded pass run backwards "
                                  f"and was refused: {(said[0]['why'] if said else None)!r}; what "
                                  f"played instead carries "
                                  f"{('a score' if rev['hasScore'] else 'no score')} and reads as "
                                  f"a replay: {read['verdict'] is not None}")

                    # 6 · the drift ------------------------------------------------------------
                    # A fresh visit, so the two passes below are the first and the second of one
                    # edge inside one visit window.
                    enter(br, base, "diagnostics:on,familySeed:4242")
                    for _ in range(30):
                        if js(br, "return {s: window.__exPass.report().composer.state};"
                              )["s"] == "read":
                            break
                        br.sleep(0.2)
                    pair2, _ = shown_pair(br, recorded)
                    js(br, STUB)
                    if len(pair2) < 2:
                        for r in BROWSER_ROWS[6:]:
                            skip(r, "this hang shows fewer than two recorded works")
                    else:
                        A, B = pair2[0], pair2[1]
                        EDGE = "__".join(sorted([A, B]))
                        one = declare(br, A, B, "drift-one")
                        land(br)
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
                        check(BROWSER_ROWS[8],
                              stale["hasScore"] and stale["request"]["sessionMemory"] is None
                              and m.get("cooled") == old["family"]
                              and len(m.get("rolls") or []) > 1
                              and m.get("passes") == 0,
                              f"nothing crossed; the family «{m.get('cooled')}» is cooling and "
                              f"{len(m.get('rolls') or [])} dice were offered; the crossing still "
                              f"plays ({'a score' if stale['hasScore'] else 'no score'}) — a "
                              f"cooldown never empties a pool")

                        # 9 · the record survives a reload --------------------------------
                        enter(br, base, "diagnostics:on,familySeed:4242")
                        for _ in range(30):
                            if js(br, "return {s: window.__exPass.report().composer.state};"
                                  )["s"] == "read":
                                break
                            br.sleep(0.2)
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
                            for _ in range(30):
                                if js(br, "return {s: window.__exPass.report().composer.state};"
                                      )["s"] == "read":
                                    break
                                br.sleep(0.2)
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
                            for _ in range(30):
                                if js(br, "return {s: window.__exPass.report().composer.state};"
                                      )["s"] == "read":
                                    break
                                br.sleep(0.2)
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
                                br2.key("ArrowDown")
                                for _ in range(30):
                                    if js(br2, "return {s: window.__exPass ? "
                                               "window.__exPass.report().composer.state : null};"
                                          )["s"] == "read":
                                        break
                                    br2.sleep(0.2)
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
                                               "return {rows: n};")
                            check(BROWSER_ROWS[12],
                                  after_put["rows"] <= planted["keep"],
                                  f"{planted['planted']} edges were planted against a store that "
                                  f"keeps {planted['keep']}; the browser now holds "
                                  f"{after_put['rows']} record(s)")

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
