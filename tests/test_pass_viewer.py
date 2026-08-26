#!/usr/bin/env python3
"""EX-VIEWER — charter shelf 16's fourth die: the visit's own memory of itself.
Run: python3 tests/test_pass_viewer.py

Root: charter shelf 16. The dice run in order — base weights, letter cooldowns, the day's weather,
THE VIEWER'S MEMORY, roll. The composer has carried all five for a while: `viewerBiasOf` is bounded
[0.7, 1.3] and the recurrence fold reads `seenWorks`. Nothing ever filled the fourth. `passRequestFor`
in engine/client/01a-pass.js built every other field the composer reads and never `viewerMemory`, so
on every real visit that step multiplied by exactly one: a family lingered over never warmed, one
skipped past never cooled, and a work met a second time was handed the same facet.

WHAT THIS MEASURES.

  The wire. A visit that stays with a work and one that walks away from it reach the composer with
  different memories, filled from what the walk already observes — the arrival at every landing, the
  letters that landing's own route row carries, and the span between that landing and the next
  declare. Nothing is invented for it: the dwell is judged against the duration of the crossing that
  delivered the work, which the walk had already frozen onto that command.

  The output. The two visits, alike in every other thing the composer reads — same pair, same
  records, same pinned visit seed, same walk memory, same hour — compose different crossings.

  The ephemerality. Seeds and determinism are the judging mode; ephemerality is the viewer mode.
  Nothing of the visit's memory of itself is written anywhere: it dies with the page, while the edge
  record beside it — which IS stored, by §4.8's own law — survives the same reload.

WHAT IT DOES NOT MEASURE. What the bias does inside the die. `viewerBiasOf`'s own bounds and the
recurrence fold are the composer's, and tests/test_pass_composed.py holds them; what is held here is
that the walk fills the field at all and that filling it reaches the picture.
"""
import json
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


TMP = Path(tempfile.mkdtemp(prefix="synth_viewer_"))
build_site.OUT = TMP
build_site.build(SITE_URL)
SRC = (ROOT / "engine" / "client" / "01a-pass.js").read_text(encoding="utf-8")

# ---------------------------------------------------------------- the bundle

check("EX-VIEWER the request carries the visit's own memory, filled at the one place the walk "
      "builds a request",
      "req.viewerMemory = viewer" in SRC and "function passViewerMemory" in SRC
      and "function passViewerArrived" in SRC and "function passViewerLeft" in SRC,
      "shelf 16's fourth step is filled beside `walkMemory`, on the same road and at the same place")

check("EX-VIEWER the dwell is judged against the crossing's own length and against no other number",
      "function passCrossingMsOf" in SRC
      and "dwell >= last.crossingMs ? passViewerLingered : passViewerSkipped" in SRC,
      "lingering and skipping are decided by comparing two things the visit itself produced")

check("EX-VIEWER the visit's memory of itself is written to no store",
      all(("sessionStorage" not in line and "localStorage" not in line)
          for line in SRC.splitlines()
          if any(n in line for n in ("passViewerSeen", "passViewerLingered", "passViewerSkipped",
                                     "passViewerStanding"))),
      "ephemerality is the viewer mode: the three lists live in the page and nowhere else")

# ---------------------------------------------------------------- the walk, in a browser

BROWSER_ROWS = [
    "EX-VIEWER a visit that lingers and one that skips reach the composer with opposite memories",
    "EX-VIEWER the memory reaches the die and moves it: two opposite memories compose differently",
    "EX-VIEWER nothing of the visit's own memory survives the page, while the edge record does",
]

# THE RECORDS ROUTE, exactly as the Worker answers it in production and as tests/test_pass_memory.py
# already serves it locally: `pass.works` left config.json, so the id → record map is a request of
# its own and the walk composes nothing until its first wave has landed.
RECORDS_ROUTE = "/api/pass/records"
RECORDS_CAP = 20
RECORDS_STORE = {}


def records_answer(raw_path):
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


# The picture layer of this suite. The route row a landing writes — and with it the letters this
# visit remembers — is written only for a passage that actually DREW, and what says one drew is the
# host's own report. A stub host stands in for the renderer so the reading is taken on every machine
# and not only on one with a working WebGL2 context. Nothing here draws and nothing here decides.
#
# IT REPORTS THE INSTRUMENT THE SCORE ACTUALLY NAMED, which is the one thing about it that has to be
# real here. The letters a visit remembers are the genre and the instruments of the passage that
# played, and they are the very ids the composer's die weighs on the next roll — a stub answering
# with a name of its own would have the visit remember a letter no pool contains, and the memory
# would then reach the die and touch nothing, for a reason belonging to the bench and not to the
# walk.
STUB = """
  if (!window.__exPassLayer) return {no: true};
  function named() {
    try { return String(window.__cmd.score.cues[0].instrument.id); } catch (e) { return 'stub'; }
  }
  window.__exPassLayer({
    offer: function () { return true; },
    report: function () { var id = named();
                          return {active: false, instrument: id,
                                  census: {buffer: '800x600', dpr: 1},
                                  stack: [{id: 'pivot', instrument: id, handles: {}}]}; },
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
  var no = window.__exPass.report().refusals.filter(function (x) { return x.what === 'declare'; });
  return {absent: false, got: !!cmd, hasScore: !!(cmd && cmd.score),
          request: row ? row.request : null,
          json: cmd && cmd.score ? JSON.stringify(cmd.score) : null,
          visit: window.__exPass.report().memory.visit,
          noWhy: no.length ? no[no.length - 1].why : null};
"""


def js(br, body):
    return json.loads(br.evaluate("JSON.stringify((function(){%s})())" % body))


def declare(br, a, b, cause):
    """One step declared programmatically. Two declares inside one animation frame are refused by
    law (§1.1), and a headless browser can hold a frame open far longer than a person's hand does,
    so a refusal for that one reason is waited out rather than read as an answer."""
    got = {}
    for _ in range(10):
        got = js(br, DECLARE % (a, b, cause))
        if got.get("absent") or got.get("got") or "one frame" not in (got.get("noWhy") or ""):
            return got
        br.sleep(0.3)
    return got


def wait_ready(br, budget=150):
    """The composer's own script and the first record wave, together: a step taken before either has
    landed composes nothing, and every reading downstream would be of a glide."""
    for _ in range(budget):
        got = js(br, "if (!window.__exPass) return {st: null, held: 0};"
                     "var r = window.__exPass.report();"
                     "return {st: r.composer.state, held: r.records.held,"
                     " waves: r.records.waves, inflight: r.records.inflight};")
        if (got.get("st") == "read" and (got.get("waves") or 0) > 0
                and (got.get("inflight") or 0) == 0 and (got.get("held") or 0) > 1):
            return True
        br.sleep(0.2)
    return False


def enter(br, base, pass_arg=None, clear=True):
    """A visitor who opens the door and stands in the walk. `clear` is what makes a visit a FIRST
    one: the edge store is the browser's, and a visit that inherits one is not a fresh visitor."""
    br.navigate(base + "/")
    if clear:
        br.clear_storage()
    br.navigate(base + "/" + (("?pass=" + pass_arg) if pass_arg else ""))
    br.sleep(0.8)
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


# THE THREE WORKS THIS SUITE WALKS are chosen by what they prove and never by taste: the first
# ordered triple of this hang whose BOTH crossings compose. A passage the composer declines for its
# own reasons carries no score to remember, no letters to warm or cool and no picture to compare,
# and a lane about the visit's memory would then be measuring nothing.
TRIPLE = """
  var ids = %s, out = null;
  for (var i = 0; i < ids.length && !out; i++) {
    for (var j = 0; j < ids.length && !out; j++) {
      for (var k = 0; k < ids.length && !out; k++) {
        if (i === j || j === k || i === k) continue;
        var A = document.querySelector('.exh-frame[data-id="' + ids[i] + '"]');
        var B = document.querySelector('.exh-frame[data-id="' + ids[j] + '"]');
        var C = document.querySelector('.exh-frame[data-id="' + ids[k] + '"]');
        if (!A || !B || !C) continue;
        var one = window.__exPass.passage(window.__exPass.request(A, B));
        var two = window.__exPass.passage(window.__exPass.request(B, C));
        if (one && one.score && two && two.score) out = [ids[i], ids[j], ids[k]];
      }
    }
  }
  return out || [];
"""

SEED = "diagnostics:on,familySeed:4242"


# THE QUESTION PUT TO EVERY EDGE THE HANG OFFERS. One request per ordered pair, built by the walk's
# own `passRequestFor`, composed twice through the composer's own entry with nothing changed between
# the two but the visit's memory of itself. The first edge whose two scores differ is the answer.
EDGES_JS = """
  var ids = %s, stay = %s, gone = %s, out = {tried: 0, edge: null};
  for (var i = 0; i < ids.length && !out.edge; i++) {
    for (var j = 0; j < ids.length && !out.edge; j++) {
      if (i === j) continue;
      var A = document.querySelector('.exh-frame[data-id="' + ids[i] + '"]');
      var B = document.querySelector('.exh-frame[data-id="' + ids[j] + '"]');
      if (!A || !B) continue;
      var req = window.__exPass.request(A, B);
      if (!req) continue;
      out.tried++;
      req.viewerMemory = stay;
      var one = window.__exPass.passage(req);
      req.viewerMemory = gone;
      var two = window.__exPass.passage(req);
      if (!one || !one.score || !two || !two.score) continue;
      var a = JSON.stringify(one.score), b = JSON.stringify(two.score);
      if (a !== b) {
        out.edge = {from: ids[i], to: ids[j], stayedBytes: a.length, leftBytes: b.length};
      }
    }
  }
  return out;
"""



def hung(br):
    return js(br, "return [].slice.call(document.querySelectorAll('.exh-frame'))"
                  ".map(function (e) { return e.dataset.id; });")


def enter_until(br, base, want, tries=8):
    """The door deals a fresh spread on every open (his word of 2026-07-12), so which works a visit
    is shown is the door's business and not this suite's. A visit is opened until it is shown the
    three works this lane compares two visits on — because comparing two visits means comparing them
    on ONE edge, and an edge the second visit was never shown is no comparison at all."""
    last = []
    for _ in range(tries):
        enter(br, base, SEED)
        last = hung(br)
        if all(w in last for w in want):
            return True, last
    return False, last


def play(br, base, a, b, c, linger):
    """One whole visit, from a cleared door. It crosses A→B, lands it, stays with B for as long as
    the caller asks, and then declares B→C — which is where the dwell just spent is closed and the
    crossing that reads it is composed. What comes back is the memory the visit had built by then
    and the score it composed on it."""
    shown, ids = enter_until(br, base, [a, b, c])
    if not shown:
        return {"no": "the door never dealt all three of %s; it dealt %s" % ([a, b, c], ids)}
    if not wait_ready(br):
        return {"no": "the composer or the record wave never landed"}
    stub = js(br, STUB)
    if stub.get("no"):
        return {"no": "the walk opened no door for a picture layer"}
    first = declare(br, a, b, "viewer-first")
    if not first.get("hasScore"):
        return {"no": "the first crossing composed nothing: " + json.dumps(first)[:400]}
    js(br, "window.__exPass.adapter.dock(window.__cmd); return null;")
    standing = js(br, "return window.__exPass.report().memory.visit;")["standing"] or {}
    ms = standing.get("crossingMs") or 0
    if linger:
        # STAY WITH THE WORK LONGER THAN THE CROSSING THAT BROUGHT IT: the walk's own comparison,
        # read back off its own record rather than guessed at here, plus half a second for the round
        # trip that closes it.
        br.sleep(ms / 1000.0 + 0.5)
    second = declare(br, b, c, "viewer-second")
    return {"first": first, "second": second, "standing": standing,
            "visit": second.get("visit"), "score": second.get("json"),
            "request": second.get("request")}


if not chrome_available():
    for r in BROWSER_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
else:
    with serve(TMP, answer=records_answer) as base:
        with Browser(width=1280, height=900) as br:
            enter(br, base, SEED)
            allworks = js(br, "return {ids: [].slice.call(document.querySelectorAll('.exh-frame'))"
                              ".map(function (e) { return e.dataset.id; })};")["ids"]
            recorded = list(put_records(TMP, allworks[:-1])) if len(allworks) >= 4 else []
            if len(recorded) < 3:
                for r in BROWSER_ROWS:
                    skip(r, f"the walk hung fewer than four works: {allworks[:5]}")
            else:
                enter(br, base, SEED)
                wait_ready(br)
                triple = js(br, TRIPLE % json.dumps(recorded))
                if len(triple) < 3:
                    for r in BROWSER_ROWS:
                        skip(r, "no ordered triple of this hang composes both of its crossings")
                else:
                    A, B, C = triple[0], triple[1], triple[2]

                    # THE TWO VISITS. Alike in every single thing the composer reads — the same
                    # three works, the same records, the same pinned visit seed, the same walk
                    # memory (both played A→B and nothing else), the same hour — and different in
                    # exactly one: how long the person stayed with B.
                    stayed = play(br, base, A, B, C, linger=True)
                    left = play(br, base, A, B, C, linger=False)

                    if stayed.get("no") or left.get("no"):
                        why = stayed.get("no") or left.get("no")
                        for r in BROWSER_ROWS:
                            skip(r, "a visit could not be driven end to end on this hang: " + why)
                    else:
                        sv = stayed["visit"] or {}
                        lv = left["visit"] or {}
                        letters = (stayed["standing"] or {}).get("letters") or []
                        check(BROWSER_ROWS[0],
                              bool(letters)
                              and sv.get("lingered") == letters and sv.get("skipped") == []
                              and lv.get("skipped") == letters and lv.get("lingered") == []
                              and sv.get("seenWorks") == lv.get("seenWorks")
                              and B in (sv.get("seenWorks") or [])
                              and (stayed["request"] or {}).get("viewerMemory") is not None
                              and (left["request"] or {}).get("viewerMemory") is not None,
                              f"the crossing that landed carried the letters {letters}; the visit "
                              f"that stayed remembers lingered={sv.get('lingered')} "
                              f"skipped={sv.get('skipped')}, the visit that left remembers "
                              f"lingered={lv.get('lingered')} skipped={lv.get('skipped')}, and both "
                              f"were shown {sv.get('seenWorks')}")

                        # DOES THE MEMORY REACH THE DIE, AND MOVE IT? The two memories are in hand
                        # and the row above has already shown they are opposites. What is asked here
                        # is whether handing one or the other to the composer changes what it
                        # composes — put to the composer's own entry, on the very requests the walk
                        # builds, with nothing in between.
                        #
                        # IT IS ASKED OF THE WHOLE HANG AND NOT OF ONE EDGE, and that is the repair
                        # this row needed. It used to drive two visits over a single edge and compare
                        # the score bytes, and whether a bounded bias flips a cast depends on what
                        # else stands in that edge's own pool: the same row passed on the pair
                        # synth-21 to synth-14 and failed on synth-16 to synth-05 in two runs of an
                        # identical engine an hour apart, because the door deals a fresh spread on
                        # every open. A row whose answer is decided by which pair was dealt proves
                        # nothing either way. So the question is put to every edge this hang offers
                        # and what it asserts is that the memory moves at least one of them — an
                        # existence, which is what "the die is moved" means and which no deal can
                        # turn into an accident. The edge that moved is named.
                        moved = js(br, EDGES_JS % (json.dumps(recorded), json.dumps(sv),
                                                   json.dumps(lv)))
                        check(BROWSER_ROWS[1],
                              bool(moved["edge"]),
                              f"the two memories put to the composer's own entry over the edges this "
                              f"hang offers: the visit that stayed and the visit that left compose "
                              f"different crossings on {moved['edge']}. Everything but the memory is "
                              f"held identical — the same request the walk builds, the same records, "
                              f"the same pinned visit seed"
                              if moved["edge"] else
                              f"the two memories were put to the composer's own entry over every "
                              f"edge this hang offers and not one composed differently. The memories "
                              f"themselves are opposite (the row above holds that), so either the "
                              f"bias never reaches the die or nothing in any of these pools stands "
                              f"close enough for it to move")

                        # THE EPHEMERALITY, read as the difference between two memories standing
                        # side by side. The edge record IS stored — §4.8's own law — and survives a
                        # reload inside the visit window; the visit's memory of itself is this
                        # page's alone and starts over with it. One reload separates them.
                        before = js(br, "var r = window.__exPass.report();"
                                        "return {visit: r.memory.visit,"
                                        " edges: (r.memory.edges || []).map(function (e) {"
                                        "   return e.edgeKey; })};")
                        br.reload()
                        for _ in range(30):
                            if br.evaluate("String(!!window.__exPass)") == "true":
                                break
                            br.sleep(0.2)
                        br.sleep(0.6)
                        # The edge store is read from the browser on demand, so it is ASKED for
                        # before the surface is read — otherwise the row would be reading a page
                        # that has not yet opened the store rather than a store that lost its rows.
                        after = js(br, "window.__exPass.memory.all();"
                                       "var r = window.__exPass.report();"
                                       "var keys = [];"
                                       "try { keys = Object.keys(window.sessionStorage)"
                                       "  .concat(Object.keys(window.localStorage)); } catch (e) {}"
                                       "return {visit: r.memory.visit,"
                                       " edges: (r.memory.edges || []).map(function (e) {"
                                       "   return e.edgeKey; }),"
                                       " stores: keys};")
                        kept = [k for k in before["edges"] if k in after["edges"]]
                        check(BROWSER_ROWS[2],
                              bool(before["visit"]["seenWorks"])
                              and after["visit"]["seenWorks"] == []
                              and after["visit"]["lingered"] == []
                              and after["visit"]["skipped"] == []
                              and after["visit"]["standing"] is None
                              and bool(kept),
                              f"before the reload the visit remembered {before['visit']} and the "
                              f"browser held the edge(s) {before['edges']}; after it the visit "
                              f"remembers {after['visit']} and the browser still holds {kept}. The "
                              f"stores this page opened are {after['stores']}")

# ---------------------------------------------------------------- report
import shutil  # noqa: E402

shutil.rmtree(TMP, ignore_errors=True)

passed = sum(1 for _, s, _ in results if s == "PASS")
failed = sum(1 for _, s, _ in results if s == "FAIL")
skipped = sum(1 for _, s, _ in results if s == "SKIP")
print()
for name, status, detail in results:
    line = f"{status}  {name}"
    if status != "PASS" and detail:
        line += f"   — {detail}"
    print(line)
print(f"\n{passed} passed / {failed} failed / {skipped} skipped")
sys.exit(1 if failed else 0)
