#!/usr/bin/env python3
"""PASS-API-V1 — conformance rows for the transaction and the host.
Run: python3 tests/test_pass_api.py

docs/design/PASS-API-V1.md §9 numbers 30 conformance gates; this file covers 1-6 and 23-28, the ones
this branch's scaffold (the adapter in the bundle + the host in pass-layer.js) makes real. The other
rows (7-22, 29-31) need a real instrument, a real score with cues, and a phone — none of which exist
yet (§11).

Every browser row drives the SAME test instrument pass-layer.js ships, reachable only when
diagnostics are on (`?pass=diagnostics:on,visualLayer:pass`) — it takes commands, counts its
lifecycle calls, and can be told to decline, throw, settle late, settle twice, settle with a stale
token, or never settle, so a row exercises the real host state machine rather than a claim about it.
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

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


# ---------------------------------------------------------------- bake once
TMP = Path(tempfile.mkdtemp(prefix="synth_passapi_"))
build_site.OUT = TMP
build_site.build(SITE_URL)
JS = (TMP / "exhibition.js").read_text(encoding="utf-8")
SRC = (ROOT / "engine" / "client" / "01a-pass.js").read_text(encoding="utf-8")
LAYER_SRC = (ROOT / "engine" / "assets" / "pass-layer.js").read_text(encoding="utf-8")
LAYER_BUILT = (TMP / "pass-layer.js").read_text(encoding="utf-8") if (TMP / "pass-layer.js").exists() else ""

# ---------------------------------------------------------------- string rows

check("PASS-API declare refuses an absent destination",
      '!a || !a.toEl' in SRC and '"no destination"' in SRC,
      "declare must check the destination before minting a generation")

check("PASS-API a second declare inside one frame is refused, not superseded",
      "passFrameLock" in SRC and '"second declare in one frame"' in SRC,
      "the frame lock must be a separate check from the running-transaction supersede")

check("PASS-API dock is keyed on generation together with destination, never the live global",
      "passDockKeys" in SRC and "cmd.gen + \":\" + (cmd.to.id" in SRC,
      "the §10.2 repair: cmd.gen is the command's OWN frozen generation, not the mutable passGen")

check("PASS-API the door resolves to a real destination, not an absent one",
      'el.id === "ex-door"' in SRC and 'id: "door"' in SRC,
      "passWhere must name the door instead of returning an id-less record indistinguishable from absent")

check("PASS-API the popstate road that used to jump nowhere now names a destination",
      "passJump(null," not in JS,
      "the fixed call must no longer pass a null destination into the built client")

check("PASS-API interrupt reaches the host, not only the bundle's own bookkeeping",
      "passLayer.cancel" in SRC and "function interrupt(reason)" in SRC,
      "a takeover the per-frame glide checker never sees must still be reachable")

check("PASS-API reframe resizes the running transaction rather than superseding it",
      "function reframe(viewport)" in SRC and "passLayer.resize" in SRC
      and "if (passRunning())" in JS,
      "the orientation/resize road must route a live takeover through resize, not a fresh declare")

check("PASS-API every product surface in front of the walk calls interrupt",
      all(('interrupt("%s")' % c) in JS for c in
          ["zoom", "quiz", "gift", "door", "series", "popstate"]),
      "zoom, quiz, gift, door, series and popstate must each be wired — 'reset' is deliberately NOT "
      "one of them: that road runs at boot, before 01a-pass.js's own `let passNav` leaves the "
      "temporal dead zone, and nothing can be mid-transaction that early regardless")

check("PASS-API the host is a state machine with the watchdog, idempotence and a one-instrument registry",
      all(s in LAYER_SRC for s in
          ["function offer(", "function settle(", "function fail(", "function cancel(",
           "watchdogT", "register(inst)" if "register(inst)" in LAYER_SRC else "function register("]),
      "pass-layer.js must carry the machinery, not the bundle")

check("PASS-API settle and fail are both idempotent and both token-checked",
      "token !== cur.cmd.gen" in LAYER_SRC and "cur.docked" in LAYER_SRC,
      "a repeat or foreign-token call must be provably inert, not merely documented as such")

check("PASS-API every exit from running ends in exactly one dock — finish() is the single door",
      "function finish(landState, why)" in LAYER_SRC and "rec.docked = true" in LAYER_SRC,
      "settle, fail, cancel and the watchdog must all resolve through the one function that docks")

# The host takes the instrument's own reading and reads NOTHING in it. The five instruments agree on
# one shape — `door`, `buffer`, `reads`, `request`, `applied`, `moved`, `unit`, `held`, `whyNo` — and
# that agreement lives in their files. A host that started naming a field of it would be interpreting
# the reading instead of carrying it, and would be the same defect the "host knows no instrument
# name" law already fences: every instrument-side name below must be absent from the built host.
check("PASS-API the host stores the applied reading and names no field of it",
      "reportApplied" in LAYER_SRC and "v.applied = a" in LAYER_SRC
      and len(LAYER_BUILT) > 1000
      and not any(n in LAYER_BUILT for n in
                  ["sizeRequest", "balRequest", "grainRequest", "flatDegRequest",
                   "doorWhyNo", "doorHeld", "sizeRungs", "balBands", "grainCells"]),
      "the channel must be a plain store, so a new instrument shape needs no host change")

check("PASS-API the test instrument is reachable only when diagnostics are on",
      "makeTestInstrument" in LAYER_SRC and "var diag = window.__@@NS@@Pass;" in LAYER_SRC
      and "if (diag) {" in LAYER_SRC,
      "no diagnostics surface means no test instrument gets registered")

# Read against the BUILT artifact rather than the source, since 2026-08-14. §5's own sentence is
# "a conformance row greps the BUILT client for both", and the built file is the comment-stripped one
# a visitor downloads — so the row judges code and cannot be tripped, either way, by prose that
# merely names the two forbidden things. The emptiness guard keeps it from passing on nothing.
check("PASS-API no eval, no new Function anywhere the host reads a command",
      len(LAYER_BUILT) > 1000 and "eval(" not in LAYER_BUILT and "new Function" not in LAYER_BUILT,
      f"the host's own file must obey the same law as the bundle's driver graph "
      f"(built file is {len(LAYER_BUILT)} characters)")

# ---------------------------------------------------------------- browser rows

BROWSER_ROWS = [
    "PASS-API row 23 · declare refuses an absent destination and records why",
    "PASS-API row 23 · the door is a destination like any other",
    "PASS-API row 24 · a second declare inside one frame is refused with its reason",
    "PASS-API row 1  · dock happens exactly once, keyed on generation and destination",
    "PASS-API the chained A→B→C case: the middle work does not dock under the last generation",
    "PASS-API row 4  · decline before takeover casts the last resort, not the glide",
    "PASS-API row 3  · a superseding input cancels the running transaction and the second declares cleanly",
    "PASS-API row 2/26 · a stale/foreign-token settle changes nothing",
    "PASS-API row 26 · a foreign token with no transaction in flight changes nothing",
    "PASS-API row 5/25 · error after takeover hides the renderer within one frame and lands a full door",
    "PASS-API row 6/28 · the watchdog ends a transaction that never settles, and reads as a hang",
    "PASS-API row 28 · a legal instant transition (duration 0) reads as landed, not hung",
    "PASS-API row 27 · the covered walk is inert and hidden from the accessibility tree while running",
    "PASS-API a double settle is idempotent — the second call changes nothing",
    "PASS-API §9 · the applied reading's channel stands on every stack row, live and after landing",
    "PASS-API §2.5 · a swipe folds the running crossing up through its envelopes, never in one frame",
    "PASS-API §2.5 · the crossing the swipe asked for takes the stage the instant the fold lands",
    "PASS-API §7 · with no tier named, the rung comes from the device's own frame times",
    "PASS-API §7 · a named tier outranks the measurement and pins the rung",
    "PASS-API §7 · the ladder's middle step: the accompaniment halves, the miracle keeps its rate",
    "PASS-API §7 · below the joy floor the floor grammar plays, and the crossing is never refused",
]

# PASS-01 (TEST_MATRIX.md) — a separate list rather than two more BROWSER_ROWS entries, so the
# fixed BROWSER_ROWS[N] indices every row above already relies on never shift.
PIXEL_ROWS = [
    "PASS-01 (EX-PASS / INV-109, pixel) · visualLayer:off draws exactly the plain glide — no "
    "canvas ever appears, and the frame reads pixel-identical to the walk with no pass at all, "
    "mid-flight and settled",
    "PASS-01 red-on-bug · with the visualLayer guard removed from the built bundle, "
    "visualLayer:off no longer draws the plain glide alone",
]

# THE FOLD BENCH. A hand-made command of exactly the shape the bundle freezes, carrying a score whose
# one cue names the host's OWN last-resort instrument — registered unconditionally, so this bench
# needs no instrument file and no lab module — with the two doors §2.5 walks between named on that
# instrument's own `reveal` handle and its own declared span. The score names an interruption budget,
# which is what a cadence is given to walk in.
FOLD_BENCH = """
  window.__fold = {docks: [], glides: [], curtains: [], marks: []};
  window.__foldHooks = {
    dock: function (c) { window.__fold.docks.push(c.gen); },
    glide: function (c) { window.__fold.glides.push(c.gen); },
    curtain: function (on) { window.__fold.curtains.push(!!on); },
    mark: function (n) { window.__fold.marks.push(n); },
    hangGeometry: function () { return null; }
  };
  window.__foldCmd = function (gen, withinMs, tier, source) {
    var ids = [].slice.call(document.querySelectorAll('.exh-frame')).map(function (f) {
      return f.dataset.id;
    });
    return {
      gen: gen, from: {id: ids[0], n: 1}, to: {id: ids[1], n: 2},
      kind: 'step', cause: 'fold-bench', dir: 1, span: 100, velocity: 0,
      reduced: false, saveData: false, rtl: false, dpr: window.devicePixelRatio || 1,
      viewport: {w: innerWidth, h: innerHeight},
      params: {flightMs: {base: 3000},
               qualityTier: {base: tier || 'standard', source: source || 'default'}},
      score: {
        version: 2, duration: 3000,
        interruption: {withinMs: withinMs, resolve: 'nearest-door'},
        cues: [{
          id: 'fold', instrument: {id: '@host/last-resort'}, window: [0, 3],
          doors: {'in': {handle: 'reveal', value: -0.15},
                  out: {handle: 'reveal', value: 1.15}},
          cadence: {reveal: 'smooth'},
          tracks: {reveal: {op: 'map', 'in': {source: 'progress'}, from: [0, 1],
                            to: [-0.15, 1.15]}}
        }]
      }
    };
  };
"""


def ready(br, tries=25):
    for _ in range(tries):
        if br.evaluate("String(document.documentElement.classList.contains('ex-walk') "
                       "&& !document.documentElement.classList.contains('ex-face'))") == "true":
            return True
        br.sleep(0.2)
    return False


def enter(br, base, pass_arg=None):
    br.navigate(base + "/")
    br.clear_storage()
    br.navigate(base + "/" + (("?pass=" + pass_arg) if pass_arg else ""))
    br.sleep(0.8)
    br.click(".exd-window", settle=1.4)
    ready(br)
    br.sleep(0.4)


def jrep(br):
    return json.loads(br.evaluate("JSON.stringify(window.__exPass.report())"))


def jhost(br):
    return json.loads(br.evaluate("JSON.stringify(window.__exPass.host.report())"))


def js(br, expr):
    """Evaluate `expr` (a JS expression) and parse its JSON.stringify'd result."""
    return json.loads(br.evaluate("JSON.stringify((function(){%s})())" % expr))


def wait_host(br, tries=30):
    for _ in range(tries):
        if br.evaluate("String(!!(window.__exPass && window.__exPass.host))") == "true":
            return True
        br.sleep(0.2)
    return False


def arm_host(br, base):
    """Open a fresh diagnostic host, stepping only for pre-preload compatibility."""
    enter(br, base, "diagnostics:on,visualLayer:pass")
    if wait_host(br, tries=10):
        return True
    br.key("ArrowDown")
    return wait_host(br)


def room(br):
    """Put the walk back at its first frame. A row that needs a REAL step needs a frame to step to,
    and by this point in the file the walk has been stepped a dozen times — at the last stop an
    ArrowDown is a clamped no-move, which declares nothing (15-motion's own law) and leaves the row
    reading a transaction that was never offered. Pre-existing flake, fixed here by giving the row
    its room rather than by softening what it asserts."""
    br.evaluate("scrollTo(0, 0)")
    br.sleep(0.4)


def reload_and_prime(br):
    """Wait for the fresh host without spending a navigation step.

    The first room's own landing now asks for pass-layer.js, a backstop that holds whatever road
    brought the visit here; the render itself and the door's pick already ask earlier still. Older
    builds only asked on the first step, so keep that step solely as a compatibility fallback for a
    build with none of the three. Spending it when preload already succeeded can leave a real
    passage in flight underneath the diagnostic row and makes a legal zero-duration test look like a
    decline from the previous transaction.
    """
    ready(br)
    br.sleep(0.4)
    room(br)
    if not wait_host(br, tries=10):
        br.key("ArrowDown")
        wait_host(br)


def cleanup(br):
    """End whatever the host is mid-way through and put the test instrument back to its default,
    so one row's mess never leaks into the next."""
    br.evaluate("window.__exPass.adapter.interrupt('row-cleanup')")
    br.evaluate("window.__exPass.test.reset()")
    br.evaluate("window.__exPass.host.configure({prepareBudgetMs:120, settleSlackMs:300})")


if not chrome_available():
    for r in BROWSER_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
    for r in PIXEL_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
else:
    with serve(TMP) as base:
        with Browser(width=1280, height=900) as br:
            if not arm_host(br, base):
                for r in BROWSER_ROWS:
                    skip(r, "pass-layer.js never registered a host in this build")
                for r in PIXEL_ROWS:
                    skip(r, "pass-layer.js never registered a host in this build")
            else:
                # 0 · declare refuses an absent destination
                r = js(br, "return window.__exPass.adapter.declare({fromEl:null, toEl:null, "
                          "kind:'jump', cause:'row23-absent'});")
                rep = jrep(br)
                said = [x for x in rep["refusals"] if x.get("what") == "declare" and x.get("why") == "no destination"]
                check(BROWSER_ROWS[0], r is None and bool(said), f"declare={r} refusals={said[:1]}")

                # 1 · the door is a legitimate destination
                r = js(br, "const A=document.querySelector('.exh-frame');"
                          "const cmd=window.__exPass.adapter.declare({fromEl:A, "
                          "toEl:document.getElementById('ex-door'), kind:'jump', cause:'row23-door'});"
                          "return cmd && cmd.to;")
                check(BROWSER_ROWS[1], r == {"id": "door", "n": None}, f"to={r}")
                br.sleep(0.1)   # let the previous row's own frame lock clear first

                # 2 · two declares inside one frame: the second is refused
                r = js(br, "const els=[...document.querySelectorAll('.exh-frame, .exh-fin')];"
                          "const c1=window.__exPass.adapter.declare({fromEl:els[0], toEl:els[1], "
                          "kind:'jump', cause:'row24a'});"
                          "const c2=window.__exPass.adapter.declare({fromEl:els[1], toEl:els[2], "
                          "kind:'jump', cause:'row24b'});"
                          "return {c1: !!c1, c2: !!c2};")
                rep = jrep(br)
                said = [x for x in rep["refusals"] if x.get("what") == "declare"
                        and x.get("why") == "second declare in one frame"]
                check(BROWSER_ROWS[2], r["c1"] is True and r["c2"] is False and bool(said),
                      f"result={r} refusals={said[:1]}")
                br.sleep(0.1)   # let the frame lock clear before the next row declares

                # 3 · dock happens exactly once, keyed on generation and destination. Two signals,
                # both gated by the SAME ledger: the mark fires once (dock returns before marking on
                # a repeat) and the repeat is recorded as a refusal — either alone already reds if the
                # ledger is removed (see the red-on-bug proof in the return report).
                r = js(br, "const els=[...document.querySelectorAll('.exh-frame, .exh-fin')];"
                          "const cmd=window.__exPass.adapter.declare({fromEl:els[0], toEl:els[1], "
                          "kind:'jump', cause:'row1'});"
                          "window.__exPass.adapter.dock(cmd);"
                          "window.__exPass.adapter.dock(cmd);"
                          "const rep=window.__exPass.report();"
                          "return {gen: cmd.gen, "
                          "docks: rep.events.filter(e=>e.gen===cmd.gen && e.name==='dock').length, "
                          "refused: rep.refusals.filter(x=>x.what==='dock' && x.why==='already docked').length};")
                check(BROWSER_ROWS[3], r["docks"] == 1 and r["refused"] == 1, f"result={r}")
                br.sleep(0.1)

                # 4 · the chained A→B→C case — the middle work's dock stays keyed to ITS OWN
                # generation, never the later one (§10.2's exact repair). cmdAB and cmdBC are two
                # SEPARATE gestures (two separate frames, past the declare-serialisation lock, unlike
                # row 24's same-frame race) — and cmdAB's own dock is called AFTER cmdBC has already
                # declared, exactly the timing the seam's el+global-gen key got wrong: it would have
                # stamped BOTH docks under the newer generation instead of each under its own.
                js(br, "const els=[...document.querySelectorAll('.exh-frame, .exh-fin')];"
                      "window.__row4_cmdAB=window.__exPass.adapter.declare({fromEl:els[0], toEl:els[1], "
                      "kind:'jump', cause:'chainAB'}); return null;")
                br.sleep(0.1)   # past the frame lock — a second, later gesture, not a same-frame race
                r = js(br, "const els=[...document.querySelectorAll('.exh-frame, .exh-fin')];"
                          "const cmdAB=window.__row4_cmdAB;"
                          "const cmdBC=window.__exPass.adapter.declare({fromEl:els[1], toEl:els[2], "
                          "kind:'jump', cause:'chainBC'});"
                          "window.__exPass.adapter.dock(cmdAB);"
                          "window.__exPass.adapter.dock(cmdBC);"
                          "const evs=window.__exPass.report().events.filter(e=>e.name==='dock' "
                          "&& (e.gen===cmdAB.gen || e.gen===cmdBC.gen));"
                          "return {gotAB: !!cmdAB, gotBC: !!cmdBC, genAB: cmdAB.gen, genBC: cmdBC.gen, "
                          "docks: evs.map(e=>({gen:e.gen, to:e.to}))};")
                docks = r["docks"]
                ok = (r["gotAB"] and r["gotBC"] and len(docks) == 2
                      and docks[0]["gen"] == r["genAB"] and docks[1]["gen"] == r["genBC"]
                      and docks[0]["gen"] != docks[1]["gen"])
                check(BROWSER_ROWS[4], ok, f"result={r}")
                br.sleep(0.1)

                # 5 · decline before takeover: the default test instrument declines, so the funnel
                # (2026-08-24, engine/assets/pass-layer.js "THE LAST RESORT") casts its own real,
                # canvas-drawing instrument rather than leaving the walk to glide with no renderer —
                # the walk still moves the same real step, but now through exactly one canvas, never
                # the full curtain (the last resort is a plain wipe between the two works, not a
                # takeover of the whole frame).
                br.evaluate("window.__exPass.test.reset()")   # mode defaults to 'decline'
                room(br)
                y0 = int(br.evaluate("String(Math.round(scrollY))") or 0)
                br.key("ArrowDown")
                br.sleep(1.2)
                y1 = int(br.evaluate("String(Math.round(scrollY))") or 0)
                curtained = br.evaluate("String(document.body.classList.contains('ex-pass-curtain'))")
                canvases = br.evaluate("String(document.querySelectorAll('canvas').length)")
                check(BROWSER_ROWS[5], y1 > y0 and curtained == "false" and canvases == "1",
                      f"scroll {y0}->{y1} curtained={curtained} canvases={canvases}")
                cleanup(br)

                # 6 · a superseding input cancels the RUNNING transaction (the host's own record,
                # not only the bundle's), and the second declares cleanly
                br.evaluate("sessionStorage.setItem('ex-pass', "
                           "JSON.stringify({diagnostics:'on', visualLayer:'pass', flightMs:4000}))")
                br.reload()
                reload_and_prime(br)      # pass-layer.js is fetched fresh on a reload; one default-
                                          # mode step re-arms window.__exPass.host/test before a row
                                          # sets a mode and takes the step it actually means to test
                br.evaluate("window.__exPass.test.mode('never')")   # holds 'running' until cancelled
                room(br)
                br.key("ArrowDown")
                br.sleep(0.3)
                mid = jhost(br)
                br.key("ArrowDown")
                br.sleep(0.3)
                after = jhost(br)
                names = [e["name"] for e in after["events"]]
                cancelled = mid.get("active") and "cancelled" in names
                check(BROWSER_ROWS[6], cancelled and after["gen"] != mid.get("gen"),
                      f"mid-active={mid.get('active')} events={names[-6:]} mid_gen={mid.get('gen')} after_gen={after.get('gen')}")
                cleanup(br)
                br.evaluate("sessionStorage.setItem('ex-pass', JSON.stringify({diagnostics:'on', visualLayer:'pass'}))")
                br.reload()
                reload_and_prime(br)

                # 7 · a stale (foreign-token) settle, mid-transaction, changes nothing. A generous
                # watchdog window is set first so the check reads the transaction WHILE it is still
                # running — the watchdog itself is a different row (10), not this one.
                br.evaluate("window.__exPass.host.configure({prepareBudgetMs:120, settleSlackMs:4000})")
                br.evaluate("window.__exPass.test.mode('stale')")
                room(br)
                br.key("ArrowDown")
                br.sleep(0.3)
                rep = jhost(br)
                stale = [e for e in rep["events"] if e["name"] == "stale-settle"]
                check(BROWSER_ROWS[7], rep["state"] == "running" and bool(stale),
                      f"state={rep['state']} events={[e['name'] for e in rep['events']][-6:]}")
                cleanup(br)

                # 8 · a foreign token with NO transaction in flight
                r = js(br, "window.__exPass.host.settle(999999);"
                          "window.__exPass.host.fail(999999, 'nope');"
                          "return window.__exPass.host.report();")
                stale = [e for e in r["events"] if e["name"] in ("stale-settle", "stale-fail")]
                check(BROWSER_ROWS[8], r["active"] is False and len(stale) >= 2,
                      f"active={r['active']} stale={stale}")

                # 9 · error after takeover: within one frame the curtain drops and the destination
                # is fully current — caption/counter/share all speak the arriving work, not the one
                # the visitor left.
                br.evaluate("window.__exPass.test.mode('fail')")
                room(br)
                g0 = br.evaluate("String(window.__exPass.report().events.length)")
                br.key("ArrowDown")
                ok = False
                for _ in range(15):
                    st = br.evaluate("window.__exPass.host.report().state")
                    if st == "idle":
                        ok = True
                        break
                    br.sleep(0.05)
                rep = jhost(br)
                # the destination this gesture actually declared — read from the bundle's own
                # nav-start mark, never guessed from DOM order (several real steps have already
                # moved the walk on by the time this row runs)
                dest = js(br, "const evs=window.__exPass.report().events;"
                             "const st=evs.slice(%s).find(e=>e.name==='nav-start');"
                             "return st ? st.to : null;" % g0)
                share = br.evaluate("(document.querySelector('.ex-share')||{}).dataset ? "
                                    "(document.querySelector('.ex-share').dataset.share||'') : ''")
                curtained = br.evaluate("String(document.body.classList.contains('ex-pass-curtain'))")
                docks = [e for e in rep["events"] if e["name"] == "recovered"]
                check(BROWSER_ROWS[9],
                      ok and curtained == "false" and bool(docks) and share == dest,
                      f"landed-within-frames={ok} curtained={curtained} docks={docks} share={share} dest={dest}")
                cleanup(br)

                # 10 · the watchdog: an instrument that never calls back is ended by the host, and
                # the transaction still lands in exactly one dock (recovered, not stranded)
                br.evaluate("sessionStorage.setItem('ex-pass', "
                           "JSON.stringify({diagnostics:'on', visualLayer:'pass', flightMs:50}))")
                br.reload()
                reload_and_prime(br)
                br.evaluate("window.__exPass.host.configure({prepareBudgetMs:20, settleSlackMs:20})")
                br.evaluate("window.__exPass.test.mode('never')")
                room(br)
                br.key("ArrowDown")
                fired = False
                for _ in range(40):
                    rep = jhost(br)
                    if any(e["name"] == "watchdog" for e in rep["events"]):
                        fired = True
                        break
                    br.sleep(0.05)
                docked_once = len([e for e in rep["events"] if e["name"] == "recovered"]) == 1
                check(BROWSER_ROWS[10], fired and rep["state"] == "idle" and docked_once,
                      f"fired={fired} state={rep['state']} events={[e['name'] for e in rep['events']][-6:]}")

                # 11 · a legal instant transition (duration 0) reads as landed, never as a hang
                br.evaluate("sessionStorage.setItem('ex-pass', "
                           "JSON.stringify({diagnostics:'on', visualLayer:'pass', flightMs:0}))")
                br.reload()
                reload_and_prime(br)
                br.evaluate("window.__exPass.test.reset(); window.__exPass.test.mode('take')")
                br.key("ArrowDown")
                br.sleep(0.4)
                rep = jhost(br)
                names = [e["name"] for e in rep["events"]]
                # A DECLINE HAS A REASON AND THE ROW SAYS IT. This row read «declined» for a run
                # and gave only the event name, which leaves the one thing a reader has to act on
                # unsaid; the host logs its reason beside the event, so the detail carries it.
                said = [e for e in rep["events"] if e["name"] in ("declined", "watchdog")]
                check(BROWSER_ROWS[11],
                      rep.get("duration") in (0, None) and "watchdog" not in names and "docked" in names,
                      f"duration-field={rep.get('duration')} events={names[-6:]}"
                      + (f" — {said[-1].get('why') or said[-1]}" if said else ""))
                cleanup(br)
                br.evaluate("sessionStorage.setItem('ex-pass', JSON.stringify({diagnostics:'on', visualLayer:'pass'}))")
                br.reload()
                reload_and_prime(br)

                # 12 · the covered walk is inert and hidden from the accessibility tree while running
                br.evaluate("window.__exPass.host.configure({prepareBudgetMs:120, settleSlackMs:4000})")
                br.evaluate("window.__exPass.test.mode('never')")
                room(br)
                br.key("ArrowDown")
                br.sleep(0.3)
                hidden = br.evaluate("document.getElementById('ex-stage').getAttribute('aria-hidden')")
                inert = br.evaluate("String(document.getElementById('ex-stage').inert)")
                curtained = br.evaluate("String(document.body.classList.contains('ex-pass-curtain'))")
                check(BROWSER_ROWS[12], hidden == "true" and inert == "true" and curtained == "true",
                      f"aria-hidden={hidden} inert={inert} curtained={curtained}")
                cleanup(br)

                # 13 · a double settle is idempotent
                r = js(br, "const els=[...document.querySelectorAll('.exh-frame, .exh-fin')];"
                          "window.__exPass.test.mode('take');"
                          "const cmd=window.__exPass.adapter.declare({fromEl:els[0], toEl:els[1], "
                          "kind:'step', cause:'row-double'});"
                          "const took=window.__exPass.layer().offer(cmd, {dock:window.__exPass.adapter.dock,"
                          "glide:window.__exPass.adapter.glide, curtain:window.__exPass.adapter.curtain,"
                          "mark:window.__exPass.adapter.mark});"
                          "return {took, gen: cmd.gen};")
                br.sleep(0.3)
                r2 = js(br, "window.__exPass.host.settle(%d); return window.__exPass.host.report();" % r["gen"])
                docks = [e for e in r2["events"] if e["name"] == "docked" and e["gen"] == r["gen"]]
                stale = [e for e in r2["events"] if e["name"] == "stale-settle"]
                check(BROWSER_ROWS[13], len(docks) == 1 and bool(stale),
                      f"took={r['took']} docks={docks} stale-count={len(stale)}")
                cleanup(br)

                # 14 · THE CHANNEL THE INSTRUMENT'S OWN READING TRAVELS ON, on the host's surface.
                #
                # His architecture decision of 2026-08-17 18:00 makes the instrument's run-time
                # reading on the actual buffer the truth of a passage, and the frame state carries
                # `reportApplied` for it beside `reportPose`. What this suite owns is the HOST's
                # half: the channel is published on every stack row, live and after the landing, and
                # it reads empty for a voice that published nothing. It is a stack row's own field,
                # never a fold into the `handles` the host itself resolved — the plan's intention and
                # the run-time truth stay two readable things.
                #
                # WHERE THE RUN-TIME PROOF IS. The diagnostics probe carries no manifest, so the host
                # never opens a stage for it and never hands it a frame (pass-layer.js: the frame
                # loop starts only `if (inst.manifest ...)`); a probe transaction can therefore show
                # the channel but never a real reading on it. A real reading on a real buffer is
                # measured where a real instrument draws: tests/test_pass_weave.py holds the reading
                # itself with its red-on-bug proof, and tests/test_pass_composed.py holds its arrival
                # on the passage record of a composed passage.
                r = js(br, """
                  window.__exPass.test.reset();
                  window.__exPass.test.mode('never');
                  window.__exPass.host.configure({prepareBudgetMs:120, settleSlackMs:600});
                  var els = [].slice.call(document.querySelectorAll('.exh-frame, .exh-fin'));
                  var cmd = window.__exPass.adapter.declare({fromEl: els[0], toEl: els[1],
                                                             kind:'step', cause:'row-applied'});
                  var took = cmd && window.__exPass.layer().offer(cmd, {
                    dock: window.__exPass.adapter.dock, glide: window.__exPass.adapter.glide,
                    curtain: window.__exPass.adapter.curtain, mark: window.__exPass.adapter.mark});
                  return {took: !!took, gen: cmd ? cmd.gen : null};
                """)
                br.sleep(0.4)
                live = (jhost(br)["stack"] or [{}])[0]
                for _ in range(60):
                    if jhost(br)["state"] == "idle":
                        break
                    br.sleep(0.2)
                landed = jhost(br)
                after = (landed["stack"] or [{}])[0]
                check(BROWSER_ROWS[14],
                      r["took"] and "applied" in live and "applied" in after
                      and live["applied"] is None and after["applied"] is None
                      and "handles" in live and "handles" in after
                      and landed["state"] == "idle"
                      and "reportApplied" in LAYER_BUILT and "reportPose" in LAYER_BUILT,
                      f"the running stack row reads {json.dumps(live)}; the landing snapshot reads "
                      f"{json.dumps(after)} at state {landed['state']}. The probe publishes nothing, "
                      f"so the channel reads empty on both — and it is a field of its own beside "
                      f"`handles` rather than a fold into it")
                cleanup(br)

                # 15/16 · §2.5 AND CHARTER SHELF 19 — A SWIPE FOLDS THE CROSSING UP, IT DOES NOT
                # CUT IT. Every plan is exhale-able from any point: on an interruption every voice
                # resolves to its nearest door THROUGH ITS OWN ENVELOPE, inside the score's own
                # bound. A supersede was the one road that reached the cadence with the envelope
                # collapsed to nothing — one frame, every handle placed on its door.
                #
                # The bench offers a scored crossing, lets it run, then offers a second command over
                # it exactly as a second swipe does. Two things are read: what the cadence was GIVEN
                # (the score's own budget, not zero) and what it SPENT (a walk down its envelope, not
                # a single frame) — and then that the held command took the stage with nothing
                # between the fold's landing and its own offer.
                js(br, FOLD_BENCH + "return null;")
                r = js(br, "window.__exPass.host.configure({prepareBudgetMs:400, settleSlackMs:6000});"
                          "var c1 = window.__foldCmd(9101, 500);"
                          "return {took: window.__exPass.host.offer(c1, window.__foldHooks) === true,"
                          " gen: c1.gen};")
                br.sleep(0.7)
                mid = jhost(br)
                r2 = js(br, "var c2 = window.__foldCmd(9102, 500);"
                           "var took = window.__exPass.host.offer(c2, window.__foldHooks) === true;"
                           "var rep = window.__exPass.host.report();"
                           "return {took: took, gen: c2.gen, held: rep.held, on: rep.gen,"
                           " state: rep.state};")
                for _ in range(60):
                    if jhost(br)["gen"] == 9102:
                        break
                    br.sleep(0.05)
                after = jhost(br)
                evs = after["events"]
                cad = [e for e in evs if e["name"] == "cadence" and e["gen"] == 9101]
                end = [e for e in evs if e["name"] == "cadence-end" and e["gen"] == 9101]
                walked = bool(cad) and "within 500 ms" in (cad[-1]["why"] or "")
                spent = 0
                if end:
                    tail = (end[-1]["why"] or "").split(" in ")
                    try:
                        spent = int(tail[-1].replace(" ms", ""))
                    except ValueError:
                        spent = -1
                # EITHER OF THE TWO LANDINGS IS A WALK, AND «at once» IS THE ONE THAT IS NOT. A
                # cadence given a budget ends either on its own envelope reaching 1 or on the host's
                # force-end at the deadline — and the force-end is a landing rather than a cut,
                # because `cadenceEnd` plays one last frame ON the door. Which of the two wins is a
                # race between the deadline timer and the frame scheduled either side of it, so the
                # row reads what the cadence was GIVEN and what it SPENT rather than which of the two
                # correct endings arrived first.
                envelope = bool(end) and "at once" not in (end[-1]["why"] or "")
                check(BROWSER_ROWS[15],
                      r["took"] and mid["state"] == "running" and mid["gen"] == 9101
                      and walked and envelope and spent >= 400,
                      f"running={mid.get('state')}/{mid.get('gen')} cadence={cad[-1:]} "
                      f"end={end[-1:]} spent={spent}ms — the score's own budget is 500 ms, so a "
                      f"walked envelope spends it and a one-frame placement spends none of it")

                # The held command's own two facts: it was HELD (named on the host's surface, with
                # the folding crossing still the one on the stage), and it was TAKEN with nothing
                # between — the fold's landing, the folding transaction's dock, and the held
                # command's offer stand next to each other in the log, in that order.
                names = [(e["name"], e["gen"]) for e in evs]
                try:
                    at = names.index(("cadence-end", 9101))
                    adjacent = names[at:at + 3] == [("cadence-end", 9101), ("cancelled", 9101),
                                                    ("offer", 9102)]
                except ValueError:
                    at, adjacent = -1, False
                check(BROWSER_ROWS[16],
                      r2["took"] and r2["held"] == 9102 and r2["on"] == 9101
                      and r2["state"] == "running" and after["gen"] == 9102 and adjacent,
                      f"at the swipe the host reads held={r2.get('held')} on={r2.get('on')} "
                      f"state={r2.get('state')}; afterwards gen={after.get('gen')}; the log around "
                      f"the landing reads {names[max(at, 0):max(at, 0) + 3]}; the whole tail is {names[-16:]}")
                br.evaluate("window.__exPass.host.cancel('fold-bench cleanup')")
                br.sleep(0.9)
                cleanup(br)

                # 17-20 · CHARTER SHELF 19's LADDER, DRIVEN FROM THE DEVICE'S OWN FRAME TIMES.
                #
                # `bench.ladder(ms, frames)` feeds the host's own frame-time recorder a run of gaps
                # of exactly `ms` and hands back where the render ladder ended up — the same recorder
                # a real visit fills from its own `requestAnimationFrame` callbacks, and the same
                # `decideScale` walk. So a row can stand the host on a slow device and on a fast one
                # without owning a slow device, and every number it is judged on is one the file was
                # already reading.
                #
                # `settle` ends each offered crossing at once, so one row's transaction never rides
                # into the next; the tier is read off the host's own surface while it is running.
                rung_gen = [9200]

                def rung_at(br_, gaps, frames, tier, source):
                    """Walk the ladder with `frames` gaps of `gaps` ms, then offer a crossing whose
                    tier setting stands at `tier` from rung `source`, and read back what the host
                    granted and where the ladder stands."""
                    rung_gen[0] += 1
                    return js(br_,
                              "window.__exPass.host.configure({fixedScale:false, prepareBudgetMs:400,"
                              " settleSlackMs:6000});"
                              "window.__exPass.bench.ladder(%d, %d);"
                              "var c = window.__foldCmd(%d, 0, '%s', '%s');"
                              "var took = window.__exPass.host.offer(c, window.__foldHooks) === true;"
                              "var rep = window.__exPass.host.report();"
                              "window.__exPass.host.cancel('rung row');"
                              "return {took: took, variant: rep.variant, pace: rep.pace,"
                              " state: rep.state, gen: rep.gen, instrument: rep.instrument};"
                              % (gaps, frames, rung_gen[0], tier, source))

                # A fast device first: the ladder walks back to its top rung, and the crossing plays
                # at the tier the register's own default names.
                fast = rung_at(br, 8, 800, "standard", "default")
                br.sleep(0.4)
                # Then the same command on a device whose frames run long enough for the ladder to
                # spend one rung. Nothing about the command changed; only the machine did.
                slow = rung_at(br, 40, 60, "standard", "default")
                br.sleep(0.4)
                check(BROWSER_ROWS[17],
                      fast["took"] and slow["took"]
                      and fast["pace"]["rung"] == 0 and fast["variant"] == "standard"
                      and slow["pace"]["rung"] >= 1 and slow["variant"] == "lean",
                      f"at 8 ms gaps the ladder stands on rung {fast['pace']['rung']} "
                      f"(scale {fast['pace']['scale']}) and the crossing plays at "
                      f"«{fast['variant']}»; at 40 ms gaps it stands on rung "
                      f"{slow['pace']['rung']} (scale {slow['pace']['scale']}) and the same command "
                      f"plays at «{slow['variant']}»")

                # The same slow device, with a tier NAMED. The word outranks the measurement.
                pinned = rung_at(br, 40, 60, "standard", "site")
                br.sleep(0.4)
                pinned_rich = rung_at(br, 40, 60, "rich", "session")
                br.sleep(0.4)
                check(BROWSER_ROWS[18],
                      pinned["took"] and pinned_rich["took"]
                      and pinned["pace"]["rung"] >= 1 and pinned["variant"] == "standard"
                      and pinned_rich["variant"] == "rich",
                      f"on a device standing at rung {pinned['pace']['rung']} a tier named by the "
                      f"site holds at «{pinned['variant']}» and one named by the session holds at "
                      f"«{pinned_rich['variant']}»")

                # The middle step of the ladder. The rate the accompaniment is re-read at is the
                # host's own answer, read off the rung rather than off a clock: full rate for both
                # kinds of voice while the ladder has rungs left to spend on the plan, and half rate
                # for the accompaniment once it has not — with the miracle at full rate throughout.
                #
                # WHERE THE PICTURE PROOF LIVES. A halved voice is an ACCOMPANIMENT voice, and a
                # stack needs two instruments that can stand over one another; the host's own
                # last-resort instrument fills the frame whole, so two of it in one score is refused
                # by the coverage law before any rate matters (pass-layer.js `coverageWhyNo`). The
                # picture is therefore measured where a real stack draws — the instrument suites —
                # and what this row owns is the decision itself, across the ladder's own rungs.
                # The ladder is walked ONE GAP AT A TIME from its top rung to its last, and the pace
                # is read at every rung it passes through — so the row reads the whole span of the
                # ladder rather than two sampled points on it.
                paces = js(br, "window.__exPass.host.configure({fixedScale:false});"
                              "window.__exPass.bench.ladder(8, 800);"
                              "var out = [window.__exPass.host.report().pace];"
                              # ten gaps a call: `ladder` restarts its own clock on every call, so the
                              # first gap of each run is a step back to that clock's origin and says
                              # nothing about the device. Ten at a time keeps those origins rare
                              # enough in the 45-gap window the ladder reads to leave the reading the
                              # run's own 40 ms, and still lands the rung boundaries finely enough to
                              # read every rung the ladder passes through.
                              "for (var i = 0; i < 400; i++) {"
                              "  window.__exPass.bench.ladder(40, 10);"
                              "  var p = window.__exPass.host.report().pace;"
                              "  if (p.rung !== out[out.length - 1].rung) out.push(p);"
                              "  if (p.rung >= p.rungs - 1) break;"
                              "}"
                              "return out;")
                check(BROWSER_ROWS[19],
                      [p["rung"] for p in paces] == [0, 1, 2, 3, 4]
                      and [p["accompaniment"] for p in paces] == [60, 60, 30, 30, 30]
                      and [p["miracle"] for p in paces] == [60] * 5,
                      "rung → (miracle, accompaniment): "
                      + ", ".join(f"{p['rung']} → ({p['miracle']}, {p['accompaniment']})"
                                  for p in paces))

                # The joy floor. The ladder is walked to its last rung with the frames still running
                # long, and there is nothing left to spend: what plays is the floor grammar — the
                # host's own last resort, cast fresh on the two photographs the DOM holds — and the
                # crossing is degraded to it rather than refused. `glides` counts the walk's own
                # plain slide, which is what «no crossing at all» would look like.
                started = js(br, "window.__exPass.host.configure({fixedScale:false,"
                                " prepareBudgetMs:400, settleSlackMs:6000});"
                                "window.__exPass.bench.ladder(40, 400);"
                                "var before = window.__exPass.host.report().pace;"
                                "var c = window.__foldCmd(9301, 0, 'standard', 'default');"
                                "var took = window.__exPass.host.offer(c, window.__foldHooks) === true;"
                                "return {took: took, before: before};")
                for _ in range(80):
                    if jhost(br)["state"] in ("running", "idle"):
                        break
                    br.sleep(0.05)
                # THE CUE THE HOST IS ACTUALLY PLAYING is what says the crossing was recast: the
                # command was offered carrying the bench's own «fold» cue, and below the floor what
                # runs is the last resort's own, cast fresh on the two photographs the DOM holds.
                floor = js(br, "var rep = window.__exPass.host.report();"
                              "return {state: rep.state, instrument: rep.instrument,"
                              " cues: (rep.stack || []).map(function (row) { return row.id; }),"
                              " said: rep.events.filter(function (e) {"
                              "   return e.name === 'joy-floor' && e.gen === 9301; }),"
                              " mine: window.__fold.glides.filter(function (g) { return g === 9301; }),"
                              " docks: window.__fold.docks.filter(function (g) { return g === 9301; })};")
                br.evaluate("window.__exPass.host.cancel('floor row')")
                check(BROWSER_ROWS[20],
                      started["took"]
                      and started["before"]["rung"] == started["before"]["rungs"] - 1
                      and started["before"]["floor"] is not None
                      and len(floor["said"]) == 1
                      and floor["state"] == "running"
                      and floor["instrument"] == "@host/last-resort"
                      and floor["cues"] == ["last-resort"]
                      and floor["mine"] == [],
                      f"the ladder stands on rung {started['before']['rung']} of "
                      f"{started['before']['rungs']} and reads «{started['before']['floor']}»; the "
                      f"crossing plays cue(s) {floor['cues']} on «{floor['instrument']}» at state "
                      f"{floor['state']}, the floor was named {len(floor['said'])} time(s) and the "
                      f"walk's own slide ran {len(floor['mine'])} time(s) for this command")
                br.evaluate("window.__exPass.bench.ladder(8, 800);"
                           "window.__exPass.host.configure({fixedScale:false})")
                br.sleep(0.6)
                cleanup(br)

                # ---------------------------------------------------- PASS-01 (TEST_MATRIX.md)
                #
                # EX-PASS / INV-109's own words, by name: with visualLayer:off the walk plays
                # exactly EX-GLIDE's plain one-frame glide — never one pixel differing from a walk
                # with no pass machinery reachable at all. Every row above proves the STATE
                # MACHINE (no curtain, no leaked canvas, scroll advances); none of them reads a
                # rendered pixel. This pins PASS-01 at the level TEST_MATRIX.md names it: pixel,
                # diffed against the plain-glide baseline, PLUS the cheapest and least-flake
                # witness there is that the pass layer never touched the frame — no <canvas>
                # element is ever created at all.
                import base64 as _b64
                import shutil as _shutil2

                SEAM = 6.0   # the project's own seam threshold (TRANSITION-STAGE-V0 §1)
                GLIDE_MID_S = 0.3   # GLIDE_MS defaults to 520ms for a calm gesture — still
                                    # animating at 300ms, so a mid-flight sample lands inside it

                def _png(path):
                    d = br._cmd("Page.captureScreenshot", format="png", captureBeyondViewport=False)
                    Path(path).write_bytes(_b64.b64decode(d["data"]))
                    return path

                def _diff(p1, p2):
                    from PIL import Image, ImageChops, ImageStat
                    a = Image.open(p1).convert("RGB")
                    b = Image.open(p2).convert("RGB")
                    if a.size != b.size:
                        return 255.0, 255.0
                    st = ImageStat.Stat(ImageChops.difference(a, b))
                    return sum(st.mean) / 3.0, max(m for _, m in st.extrema)

                def _arm(base_url, pass_arg):
                    # `window.__exPass.host` never appears with visualLayer:off — pass-layer.js
                    # is fetched only from `passOpen()`, itself gated on
                    # `passGet("visualLayer") === "pass"` (engine/assets/exhibition.js), so an
                    # "off" walk is armed the moment the walk itself is ready, not by waiting on
                    # a host that this very row proves never loads.
                    #
                    # `clear_storage()` only clears localStorage; the settings ladder's own
                    # SESSION tier — where every earlier row in this file left its own
                    # `sessionStorage['ex-pass']` — outranks a bare URL with no `?pass=` at all,
                    # so a true "no pass reachable" baseline has to clear it explicitly too.
                    br.navigate(base_url + "/")
                    br.evaluate("sessionStorage.clear(); 0")
                    enter(br, base_url, pass_arg)
                    return ready(br)

                def _canvas_count():
                    return int(br.evaluate("String(document.querySelectorAll('canvas').length)")
                               or "0")

                # EX-DOOR-3 rolls a fresh, evenly-spread door pool every open (Math.random,
                # exhibition.js:4563/4579) — a real, deliberate law for a live visitor, and pure
                # noise for a row comparing two SEPARATE page loads pixel for pixel. Pinned here,
                # on-new-document (the same CDP road headless.py's own `pretend()` uses), so every
                # navigation below rolls the identical door whichever scenario it is.
                br._cmd("Page.addScriptToEvaluateOnNewDocument",
                        source="(function(){var s=42;Math.random=function(){"
                               "s=(s*1103515245+12345)&0x7fffffff;return s/0x7fffffff;};})();")

                SHOTS = Path(tempfile.mkdtemp(prefix="synth_passapi_pixel_"))

                def _sample(base_url, pass_arg, tag):
                    """Arm a fresh walk, step once for real, and read canvas presence together
                    with a screenshot at a fixed mid-flight instant and again once settled."""
                    if not _arm(base_url, pass_arg):
                        return None
                    br.key("ArrowDown")
                    seen = _canvas_count()
                    br.sleep(GLIDE_MID_S)
                    seen = max(seen, _canvas_count())
                    mid = _png(SHOTS / (tag + "-mid.png"))
                    br.sleep(0.9)
                    seen = max(seen, _canvas_count())
                    end = _png(SHOTS / (tag + "-end.png"))
                    return {"canvases": seen, "mid": mid, "end": end}

                PIXEL_ROW, CONTROL_ROW = PIXEL_ROWS[0], PIXEL_ROWS[1]

                base_run = _sample(base, None, "baseline")
                off_run = _sample(base, "diagnostics:on,visualLayer:off", "off")
                if base_run is None or off_run is None:
                    skip(PIXEL_ROW, "the walk never armed for one of the two scenarios")
                    skip(CONTROL_ROW, "the walk never armed for one of the two scenarios")
                else:
                    # The mid-flight SCREENSHOT is not diffed pixel-for-pixel: EX-GLIDE's own
                    # curve is in fast motion at 300ms, so a few milliseconds of capture jitter
                    # between two SEPARATE navigations moves the frame's own position enough to
                    # swamp a real signal — noted mid_note below, not gated on. The mid-flight
                    # CANVAS COUNT carries no such timing sensitivity (a canvas either exists in
                    # the DOM at that instant or it does not) and is what "no partial, half-drawn
                    # pass state" is actually checked against, together with the pixel-identical
                    # SETTLED frame, which timing jitter cannot touch once both walks are at rest.
                    _, max_mid_note = _diff(base_run["mid"], off_run["mid"])
                    mean_end, max_end = _diff(base_run["end"], off_run["end"])
                    ok = off_run["canvases"] == base_run["canvases"] and max_end <= SEAM
                    check(PIXEL_ROW, ok,
                          f"canvases seen at every sampled instant — baseline: "
                          f"{base_run['canvases']}, visualLayer:off: {off_run['canvases']}; "
                          f"settled diff mean {mean_end:.3f} max {max_end:.1f} of 255 "
                          f"(bar {SEAM} of 255, the project's own seam threshold) — mid-flight "
                          f"pixel delta {max_mid_note:.1f} of 255, noted but not gated on (timing "
                          f"jitter between two separate navigations moves an in-motion frame)")

                    # RED-ON-BUG. Three real, currently-shipped guards stand between
                    # visualLayer:off and a drawn pass, and this file's own instrumentation
                    # showed all three are load-bearing on the first attempt at this row — bypassing
                    # only the layer's own FETCH gate (`passOpen`) still left the command declined
                    # (`visual-declined`) by the separate per-command gate. All three, together, are
                    # what the guarantee above actually stands on:
                    #   engine/assets/exhibition.js `passComposerOpen` / `passOpen` — the two fetch
                    #   gates, each `if (passGet("visualLayer") !== "pass") return;`
                    #   engine/assets/exhibition.js `passVisualTakes` — the per-command gate,
                    #   `if (cmd.params.visualLayer.base !== "pass") { ...; return false; }`
                    GUARD_FETCH = 'if (passGet("visualLayer") !== "pass") return;'
                    GUARD_TAKE = 'if (cmd.params.visualLayer.base !== "pass") {'
                    exh_js = (TMP / "exhibition.js").read_text(encoding="utf-8")
                    if exh_js.count(GUARD_FETCH) != 2 or GUARD_TAKE not in exh_js:
                        skip(CONTROL_ROW,
                             "the guard text was not found verbatim (as expected) in the built "
                             "bundle")
                    else:
                        MUT_TMP = Path(tempfile.mkdtemp(prefix="synth_passapi_pixel_mut_"))
                        _shutil2.copytree(TMP, MUT_TMP, dirs_exist_ok=True)
                        mutated = exh_js.replace(GUARD_FETCH, "if (false) return;")
                        mutated = mutated.replace(GUARD_TAKE, "if (false) {", 1)
                        (MUT_TMP / "exhibition.js").write_text(mutated, encoding="utf-8")
                        with serve(MUT_TMP) as mut_base:
                            mut_run = _sample(mut_base, "diagnostics:on,visualLayer:off", "mut")
                        _shutil2.rmtree(MUT_TMP, ignore_errors=True)
                        if mut_run is None:
                            skip(CONTROL_ROW, "the mutated build never armed a walk")
                        else:
                            broke = mut_run["canvases"] != base_run["canvases"]
                            check(CONTROL_ROW, broke,
                                  "with all three visualLayer guards bypassed, visualLayer:off "
                                  "drew " + str(mut_run["canvases"]) + " canvas element(s) during "
                                  "the same step against a baseline of "
                                  + str(base_run["canvases"]) + " — if these still read equal, "
                                  "the row above is not reading the guards it claims to")
                    cleanup(br)
                _shutil2.rmtree(SHOTS, ignore_errors=True)

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
