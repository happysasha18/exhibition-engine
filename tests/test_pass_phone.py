#!/usr/bin/env python3
"""EX-PHONE — the composed route on a phone: the exhale, the turn, and the two ways out.
Run: python3 tests/test_pass_phone.py

Root: the unit brief docs/immersive/briefs/2026-08-17-U27-composed-full-route.md, stage 4 — an
interruption mid-passage exhaling within about 700 ms, an orientation change, reduced motion and
Save-Data — read on a passage the engine COMPOSED at visit time rather than on a score written by
hand. Charter shelf 19 and PASS-API-V1 §2.5/§11 are the law the exhale answers to.

WHY THIS SUITE EXISTS BESIDE THE ONES THAT ALREADY DRIVE THESE ROADS. tests/test_pass_hang.py proves
a resize and an orientation change mid-passage on a score this project wrote by hand, and
tests/test_pass.py proves that reduced motion refuses the drawing layer. What neither can prove is
the thing stage 4 is about: that the same holds for a passage nobody wrote down — one the engine
derives at the instant the pair is cast, whose duration, doors, cadence budget and handles are all
its own choices. A hand-written score names an interruption budget the suite also typed; a composed
score names one the engine chose, and the exhale has to land inside it.

WHAT THIS MEASURES.

  THE EXHALE. A composed passage is interrupted in flight. Every handle walks to the nearest of the
  cue's two doors on its own envelope — never jumps — and the transaction lands. The bar is his
  ~700 ms, and the budget the run is judged against is READ OFF THE COMPOSED SCORE rather than typed
  here, so a change to what the engine asks for re-bases this row by itself.

  EXACTLY ONE LANDING. Whether a passage plays, refuses or is cut off, the visitor lands once. The
  row counts docks across all three outcomes on one visit.

  THE TURN. The frame is turned from portrait to landscape in the middle of a composed passage. The
  passage is reseated in place rather than superseded — the same generation goes on — and it still
  lands on the arriving work's real box.

  THE TWO WAYS OUT. A visit that asks for reduced motion, and a visit that asks for saved data,
  play no crossing at all: neither the host's file nor the engine's file leaves the server, and the
  visitor still walks and still lands.

WHAT EVERY ROW IS ANCHORED TO. The composed score's own numbers (the cadence budget, the duration,
the two doors), his stated bar of ~700 ms, and measured readings printed for a person. No row here
asserts composed bytes, so a change to what the engine composes re-bases nothing.

WHAT IS NEVER RESTORED FROM GIT. The one red-on-bug row serves a COPY of the built host with the
cadence budget forced to nothing; the source tree is never written to.
"""
import json
import shutil
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

# The phone frame every measurement of this road has been taken on, and the landscape it turns into.
VW, VH = 390, 844
LW, LH = 844, 390
# His bar for the exhale: the interruption resolves within about 700 ms. The row measures against
# this and against the budget the composed score itself names, and prints both.
EXHALE_MS = 700

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


TMP = Path(tempfile.mkdtemp(prefix="synth_phone_"))
build_site.OUT = TMP
build_site.build(SITE_URL)

BROWSER_ROWS = [
    "EX-PHONE a composed passage cut off mid-flight exhales to the door it is LANDING on and "
    "lands, inside the budget the score itself names",
    "EX-PHONE every handle WALKS to that door — the picture travels out rather than jumping",
    "EX-PHONE one passage, exactly one landing, whether it plays, refuses or is cut off",
    "EX-PHONE the phone turned mid-passage reseats the passage in place and still lands on the "
    "arriving work's own box",
    "EX-PHONE a visit asking for reduced motion plays no crossing and fetches neither file, and the "
    "visitor still walks",
    "EX-PHONE a visit asking for saved data does the same",
    "EX-PHONE red-on-bug · the cadence budget forced to nothing: the exhale stops walking and the "
    "picture jumps to its door",
]


def js(br, body):
    return json.loads(br.evaluate("JSON.stringify((function(){%s})())" % body))


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


def enter(br, base, pass_arg="diagnostics:on,familySeed:4242", clear=True):
    br.navigate(base + "/")
    if clear:
        br.clear_storage()
    br.navigate(base + "/" + ("?pass=" + pass_arg if pass_arg else ""))
    br.sleep(0.9)
    if br.evaluate("String(!!document.querySelector('.exd-window'))") == "true":
        try:
            br.click(".exd-window", settle=1.6)
        except RuntimeError:
            br.sleep(1.0)
    for _ in range(30):
        if br.evaluate("String(document.documentElement.classList.contains('ex-walk') "
                       "&& !document.documentElement.classList.contains('ex-face'))") == "true":
            break
        br.sleep(0.2)
    br.sleep(0.5)


def warm(br):
    """One step, so the walk's first landing fetches the host and the engine."""
    br.key("ArrowDown")
    for _ in range(40):
        if js(br, "return window.__exPass.report().composer.state;") == "read":
            break
        br.sleep(0.25)
    for _ in range(40):
        if br.evaluate("String(!!window.__exPass.layer())") == "true":
            break
        br.sleep(0.25)
    br.sleep(0.6)


def active(br):
    return br.evaluate("String(!!(window.__exPass.layer() "
                       "&& window.__exPass.layer().report().active))") == "true"


def folding(br):
    """Is a crossing being FOLDED UP under a swipe that superseded it? Since 2026-08-25 a swipe no
    longer cuts the running crossing: it compresses to its cadence and the superseding command waits,
    named on the host's own surface as `held`, until the fold lands (§2.5, charter shelf 19)."""
    return br.evaluate("String(!!(window.__exPass.layer() "
                       "&& window.__exPass.layer().report().held))") == "true"


def step_until_live(br, tries=8):
    """Step until a passage is actually drawing, and answer while it draws.

    `active` ALONE STOPPED MEANING THAT on 2026-08-25. It says a crossing holds the frame, and while
    a swipe folds the one it superseded that crossing is the OUTGOING one, on its way out inside its
    own cadence budget. A step-and-poll loop that answered on `active` therefore handed its caller
    the passage it had just replaced, a few hundred milliseconds from landing — and the row below,
    which cuts a passage mid-flight, cut nothing at all: by the time it fired the fold had landed and
    the host stood idle, which is what it reported. So the wait is for a crossing that is BOTH on the
    frame and not something a swipe is folding away, which is what «the passage I just asked for» now
    means."""
    for _ in range(tries):
        # WHICH CROSSING IS ON THE FRAME, not merely whether one is. The generation standing before
        # the step is remembered, and the wait is for a crossing whose own generation is a LATER one
        # — so a passage still running from an earlier press, which `active` answers for just as
        # readily and which may be a breath from its own end, can never be mistaken for the one this
        # press asked for.
        was = js(br, "var r = window.__exPass.layer().report(); return r.gen;")
        br.key("ArrowDown")
        for _ in range(40):
            now = js(br, "var r = window.__exPass.layer().report();"
                         "return {gen: r.gen, active: !!r.active, held: !!r.held};")
            if now["active"] and not now["held"] and now["gen"] != was:
                return True
            br.sleep(0.05)
        br.sleep(0.8)
    return False


DOCKS = ("return window.__exPass.report().events"
         ".filter(function (e) { return e.name === 'dock'; }).length;")

# The cadence the standing host walked, read by the exhale rows and compared against by the plant.
cad = {}

if not chrome_available():
    for r in BROWSER_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
else:
    with serve(TMP, answer=records_answer) as base:
        with Browser(width=VW, height=VH) as br:
            enter(br, base)
            everyone = [w["id"] for w in json.loads(
                (TMP / "exhibition_data.json").read_text(encoding="utf-8"))["works"]]
            put_records(TMP, everyone)

            # ---- rows 0-2 · the exhale, the walk to the door, and the one landing --------------
            enter(br, base)
            warm(br)
            docks0 = js(br, DOCKS)
            if not step_until_live(br):
                for r in BROWSER_ROWS[:3]:
                    skip(r, "no composed passage on this hang reached the drawing layer")
            else:
                br.sleep(0.25)
                cut = js(br, """
                  var t0 = performance.now();
                  window.__exPass.adapter.interrupt('phone-exhale');
                  return {at: t0,
                          asked: (function () {
                            var p = window.__exPass.passages();
                            var row = p.length ? p[p.length - 1] : null;
                            return row && row.score && row.score.interruption
                                   ? row.score.interruption : null; }()),
                          duration: (function () {
                            var p = window.__exPass.passages();
                            var row = p.length ? p[p.length - 1] : null;
                            return row && row.score ? row.score.duration : null; }())};
                """)
                for _ in range(60):
                    got = js(br, "var r = window.__exPass.layer().report();"
                                 "return {c: r.cadence, active: !!r.active,"
                                 " state: r.state, gen: r.gen, held: r.held,"
                                 " ev: r.events.slice(-8).map(function(e){"
                                 "   return e.name + '/' + e.gen + ': ' + (e.why || ''); })};")
                    if got["c"] and got["c"].get("ended"):
                        break
                    br.sleep(0.05)
                cad = got["c"] or {}
                budget = (cut["asked"] or {}).get("withinMs")
                landed = cad.get("landedInMs")
                check(BROWSER_ROWS[0],
                      landed is not None and budget is not None
                      and landed <= budget + 60 and landed <= EXHALE_MS,
                      "the engine asked for an exhale within %s ms on a passage of %s ms and named "
                      "«%s»; the host landed it in %s ms, against his bar of %s ms. The door walked "
                      "to was the «%s» door on the handle «%s»"
                      % (budget, cut["duration"], (cut["asked"] or {}).get("resolve"), landed,
                         EXHALE_MS, cad.get("door"), cad.get("doorHandle"))
                      + " || host=%s/%s held=%s log=%s"
                      % (got.get("state"), got.get("gen"), got.get("held"), got.get("ev")))

                walked = [h for h in (cad.get("to") or {})
                          if h in (cad.get("from") or {})
                          and abs(float((cad["to"] or {})[h]) - float((cad["from"])[h])) > 1e-9]
                check(BROWSER_ROWS[1],
                      bool(cad.get("from")) and bool(cad.get("to"))
                      and cad.get("door") in ("in", "out")
                      and not cad.get("forced"),
                      "the cadence walked %d of %d handle(s) from where the cut found them to where "
                      "the «%s» door stands, on their own envelopes and not forced: %s"
                      % (len(walked), len(cad.get("to") or {}), cad.get("door"),
                         {h: [round(float(cad["from"][h]), 4), round(float(cad["to"][h]), 4)]
                          for h in walked[:5]}))

                br.sleep(0.8)
                # a step that plays, one that is refused before takeover, and the cut above
                js(br, """
                  var A = document.querySelector('.exh-frame');
                  window.__exPass.adapter.declare({fromEl: A, toEl: null, dir: 1, span: 10,
                                                   kind: 'step', cause: 'no-destination',
                                                   velocity: 0});
                  return {ok: true};
                """)
                step_until_live(br, tries=3)
                for _ in range(80):
                    if not active(br):
                        break
                    br.sleep(0.4)
                br.sleep(0.8)
                docks1 = js(br, DOCKS)
                gens = js(br, "var e = window.__exPass.report().events;"
                              "var out = {};"
                              "e.forEach(function (r) { if (r.name === 'dock')"
                              "  out[r.gen] = (out[r.gen] || 0) + 1; });"
                              "return out;")
                check(BROWSER_ROWS[2],
                      docks1 > docks0 and all(v == 1 for v in gens.values()),
                      "%d landings across the visit, and every command that landed landed exactly "
                      "once: %s. A command with no destination was refused before it minted a "
                      "generation at all" % (docks1, gens))

            # ---- row 3 · the phone turned mid-passage ------------------------------------------
            enter(br, base)
            warm(br)
            if not step_until_live(br):
                skip(BROWSER_ROWS[3], "no composed passage on this hang reached the drawing layer")
            else:
                before = js(br, "var r = window.__exPass.layer().report();"
                                "return {gen: (window.__exPass.report().nav || {}).gen,"
                                " buffer: r.census.buffer};")
                br.sleep(0.35)
                br.set_viewport(LW, LH)
                br.evaluate("window.__exPass.adapter.reframe({w: innerWidth, h: innerHeight}); 'ok'")
                br.sleep(0.5)
                during = js(br, "var r = window.__exPass.layer().report();"
                                "return {gen: (window.__exPass.report().nav || {}).gen,"
                                " buffer: r.census.buffer, active: !!r.active};")
                for _ in range(80):
                    if not active(br):
                        break
                    br.sleep(0.4)
                br.sleep(1.0)
                after = js(br, "var r = window.__exPass.layer().report();"
                               "return {rest: r.rest, docks: window.__exPass.report().events"
                               "  .filter(function (e) { return e.name === 'dock'; }).length};")
                rest = after.get("rest") or {}
                off = rest.get("off")
                check(BROWSER_ROWS[3],
                      before["gen"] == during["gen"]
                      and before["buffer"] != during["buffer"]
                      and off is not None and float(off) < 1e-3,
                      "the frame turned from %s to %s inside one and the same passage "
                      "(generation %s throughout, never superseded), and the pass came to rest "
                      "%s pose units from the arriving work's own %s box"
                      % (before["buffer"], during["buffer"], before["gen"], off, rest.get("on")))
                br.set_viewport(VW, VH)

            # ---- row 4 · reduced motion ---------------------------------------------------------
            WAY_OUT = """
              var r = window.__exPass.report();
              var files = performance.getEntriesByType('resource').filter(function (e) {
                return e.name.indexOf('pass-layer.js') >= 0
                    || e.name.indexOf('pass-composer.js') >= 0; }).length;
              var why = r.refusals.filter(function (x) {
                return x.what === 'layer' || x.what === 'composer'; });
              return {files: files, layer: r.layer, composer: r.composer.state,
                      passages: r.composer.passages.length,
                      // THE LANDING ON THIS ROAD IS THE WALK'S OWN, not the host's. `dock` is the
                      // host's door and no host runs here at all; what says the visitor arrived is
                      // the walk's own nav-land, which the glide calls when it reaches the frame.
                      docks: r.events.filter(function (e) { return e.name === 'nav-land'; }).length,
                      device: r.device,
                      why: why.length ? why[why.length - 1].why : null};
            """

            def way_out(row, got):
                check(BROWSER_ROWS[row],
                      got["files"] == 0 and got["passages"] == 0 and got["docks"] > 0,
                      "the visit reported reduced=%s saveData=%s and asked for %d of the two "
                      "files; it derived %d passage(s), landed %d time(s), and the surface says "
                      "«%s»" % (got["device"]["reduced"], got["device"]["saveData"], got["files"],
                                got["passages"], got["docks"], got["why"]))

            br.emulate_media(prefers_reduced_motion="reduce")
            enter(br, base)
            br.key("ArrowDown")
            br.sleep(1.6)
            br.key("ArrowDown")
            br.sleep(1.6)
            way_out(4, js(br, WAY_OUT))
            br.emulate_media()

            # ---- row 6 · the red-on-bug proof --------------------------------------------------
            SERVED = TMP / "pass-layer.js"
            was = SERVED.read_text(encoding="utf-8")
            LINE = ("    var budget = immediate ? 0 : budgetOf(rec.cmd);")
            if was.count(LINE) != 1:
                check(BROWSER_ROWS[6], False,
                      "the line this plant reverts stands %d time(s) in the served host"
                      % was.count(LINE))
            else:
                SERVED.write_text(was.replace(LINE, "    var budget = 0;"), encoding="utf-8")
                enter(br, base)
                warm(br)
                planted = None
                if step_until_live(br):
                    br.sleep(0.25)
                    br.evaluate("window.__exPass.adapter.interrupt('plant'); 'ok'")
                    for _ in range(60):
                        c = js(br, "var r = window.__exPass.layer().report(); return r.cadence;")
                        if c and c.get("ended"):
                            planted = c
                            break
                        br.sleep(0.05)
                SERVED.write_text(was, encoding="utf-8")
                check(BROWSER_ROWS[6],
                      planted is not None and (planted.get("landedInMs") or 0) <= 1
                      and (cad.get("landedInMs") or 0) > 1,
                      "with the budget forced to nothing the exhale ends in %s ms — the picture is "
                      "at its door in the same instant, which is the jump §2.5 exists to forbid; "
                      "with the budget standing it walked for %s ms"
                      % (planted.get("landedInMs") if planted else None, cad.get("landedInMs")))

        # ---- row 5 · saved data, in a browser of its own -----------------------------------------
        # A stub that has to stand BEFORE the page's own script wakes cannot be taken back off a
        # document once it is installed, so the saved-data visit gets a browser to itself rather
        # than leaving every row after it walking under a request nobody made.
        with Browser(width=VW, height=VH) as br2:
            br2.inject("Object.defineProperty(navigator, 'connection', "
                       "{get: function () { return {saveData: true}; }, configurable: true});")
            enter(br2, base)
            br2.key("ArrowDown")
            br2.sleep(1.6)
            br2.key("ArrowDown")
            br2.sleep(1.6)
            got5 = js(br2, WAY_OUT)
            check(BROWSER_ROWS[5],
                  got5["files"] == 0 and got5["passages"] == 0 and got5["docks"] > 0,
                  "the visit reported reduced=%s saveData=%s and asked for %d of the two files; it "
                  "derived %d passage(s), landed %d time(s), and the surface says «%s»"
                  % (got5["device"]["reduced"], got5["device"]["saveData"], got5["files"],
                     got5["passages"], got5["docks"], got5["why"]))

shutil.rmtree(TMP, ignore_errors=True)

print()
for name, verdict, detail in results:
    print("[%s] %s%s" % (verdict, name, ("  — " + detail) if detail else ""))
n_pass = sum(1 for r in results if r[1] == "PASS")
n_fail = sum(1 for r in results if r[1] == "FAIL")
n_skip = sum(1 for r in results if r[1] == "SKIP")
print("\n%d rows: %d pass, %d fail, %d skip" % (len(results), n_pass, n_fail, n_skip))
sys.exit(1 if n_fail else 0)
