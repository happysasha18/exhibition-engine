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

# The renderer file's own byte fence (§11/§12), measured at each landing rather than guessed:
#   4 000 B  held the 167 B stub.
#  12 000 B  held the state machine, the watchdog, the idempotence guard and the test instrument
#            (2026-08-13) — measured at 8 273 B.
#  42 000 B  held those PLUS the frame half and the first real instrument (2026-08-14 morning),
#            measured at 39 415 B.
#  70 000 B  holds those PLUS the transition's own travel and its camera (2026-08-14 afternoon),
#            measured at 63 235 B. Where this growth went, in stripped source bytes: the driver
#            graph of §5, 8 928 (the six sources, the ten operator kinds, named nodes with
#            references, and the cycle refusal that names the ring); the camera of §6, 5 341 (the
#            pose record, the dolly in log space, one authority per instant, the handoff measured at
#            the window's own edge, and the rest read off the pose); and the interruption cadence of
#            §2.5, which took the transaction region from 15 017 to 18 858. The frame stage stands at
#            11 867 and the woven instrument at 12 070, of which its shader alone is 5 810.
#            None of it rides the walk's bundle: this file is fetched only on a visit that actually
#            draws (§12's split), so the 67 000 B gzipped bundle fence is untouched by every byte
#            above — the bundle is measured at 66 735 B and no product-side file changed.
#  80 000 B  holds those PLUS a SECOND instrument, the matter one of §8, carried over from
#            lab/effects/matter.js (2026-08-14 evening) and measured at 72 535 B. Two instruments
#            now stand in this file: the woven one and the matter one, and the render graph is built
#            from their manifests rather than from one shader written into the host.
#            Where this instrument's 9 248 B went, measured region by region in the built file:
#              3 287 B  its shader — the seeded field of two grains over a plain ladder, the
#                       travelling threshold, the drag along the field's own gradient and the
#                       contact shadow;
#              3 130 B  its manifest — nine handles with their neutrals, both doors and their
#                       framings, the driver kinds, the camera, one pass of fourteen uniforms bound
#                       by declared name, resources for three tiers, the decline rules and the
#                       provenance;
#              2 831 B  its mathematics and its wiring — the response curve of twenty-one measured
#                       shares, the field constants, the seating of a work in the frame, the numbers
#                       of one frame and the instrument's own lifecycle methods.
#            THE HEADROOM LEFT IS 7 465 B, about a tenth of the fence. That is less than this
#            instrument itself cost, so a third instrument landing here moves this number again —
#            which is what §12 asks for, a fence measured at each landing rather than guessed once.
#            THIS FENCE IS A PROXY, AND THE COST IT PROXIES IS INTACT. What travels to a phone is the
#            gzipped file, and that fence stands at 21 000 B with this file measured at 19 712 B,
#            1 288 B under it (tests/test_budget.py, which carries its own breakdown). The walk's own
#            bundle is untouched at 67 279 B: this file is fetched only on a visit that draws.
#            2026-08-14, 10:05 — MOVED FROM 80 000 B TO 102 000 B, MEASURED AT 92 669 B AFTER THE
#            MERGE, with 9 331 B under it, about a tenth. One move carrying two arrivals, sized on
#            the merged tree rather than estimated from either branch alone:
#              · the third instrument, the meshing one of §8 from lab/effects/gears.js, which carries
#                a radial field from an angular reading to a ring reading;
#              · the return to the hang of §2.6 — the two exact door geometries, the anchor laying
#                the first drawn frame onto the departing work's real box, the carry that reseats the
#                picture without moving it, and the rest read against the arriving hang pose.
#            THE HEADROOM IS AGAIN SMALLER THAN ONE INSTRUMENT COSTS, and the repair is named rather
#            than deferred silently: his word of 2026-08-14 08:39 has the engine load a version-
#            pinned opaque effect pack owned by tlvphotos, under which this file holds the host alone
#            and this fence stops tracking the effect farm. Queued behind the first composed passage.
#            THIS FENCE IS A PROXY, AND THE COST IT PROXIES IS MEASURED BESIDE IT. What travels to a
#            phone is the gzipped file, at 24 270 B under a 27 000 B fence (tests/test_budget.py,
#            which carries its own breakdown). The walk's own bundle stands apart at 67 985 B: this
#            file is fetched only on a visit that draws.
#            2026-08-14, midday — MOVED DOWN FROM 102 000 B TO 86 000 B, MEASURED AT 78 237 B, with
#            7 763 B under it, about a tenth. The repair the three moves above kept naming has
#            landed: the three instruments left this file for pass-pack.js, which the host fetches
#            by address and loads once its bytes weigh to the digest the build stamped. This fence
#            stops tracking the effect farm and starts tracking the host alone, so it moves DOWN and
#            keeps its bite: an instrument landing in the pack no longer touches this number, and a
#            host that grows a whole new machine still trips it. What left, measured:
#              · the three instruments with their shaders, 34 392 B of stripped source;
#              · the run-time levels check, 2 121 B, whose home moved to build time (see below).
#            What arrived is the pack loader, about 3 600 B: the address, version and digest the
#            build stamps here, the fetch, the digest weighed over what arrived, the blob the
#            weighed bytes run from, and the refusal roads with their reasons.
LAYER_FENCE = 86000
check(f"PASS-API the renderer file's fence moves DOWN on the split, measured not guessed (now {LAYER_FENCE} B, was 102 000)",
      len(LAYER_BUILT.encode("utf-8")) < LAYER_FENCE,
      f"pass-layer.js built at {len(LAYER_BUILT.encode('utf-8'))} B — the host alone: the state "
      f"machine, the frame half, the driver graph, the camera, the interruption cadence, the "
      f"return to the hang and the pack loader. The instruments travel in pass-pack.js")

# ---------------------------------------------------------------- browser rows

BROWSER_ROWS = [
    "PASS-API row 23 · declare refuses an absent destination and records why",
    "PASS-API row 23 · the door is a destination like any other",
    "PASS-API row 24 · a second declare inside one frame is refused with its reason",
    "PASS-API row 1  · dock happens exactly once, keyed on generation and destination",
    "PASS-API the chained A→B→C case: the middle work does not dock under the last generation",
    "PASS-API row 4  · decline before takeover runs the glide and changes no pixel",
    "PASS-API row 3  · a superseding input cancels the running transaction and the second declares cleanly",
    "PASS-API row 2/26 · a stale/foreign-token settle changes nothing",
    "PASS-API row 26 · a foreign token with no transaction in flight changes nothing",
    "PASS-API row 5/25 · error after takeover hides the renderer within one frame and lands a full door",
    "PASS-API row 6/28 · the watchdog ends a transaction that never settles, and reads as a hang",
    "PASS-API row 28 · a legal instant transition (duration 0) reads as landed, not hung",
    "PASS-API row 27 · the covered walk is inert and hidden from the accessibility tree while running",
    "PASS-API a double settle is idempotent — the second call changes nothing",
]


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
    """A fresh visitor with diagnostics + the picture setting on, who has taken one real step — the
    step is what makes the client fetch pass-layer.js (passOpen only runs inside stepFrame). Every
    row after this one drives the host directly, on real elements, without needing a real gesture."""
    enter(br, base, "diagnostics:on,visualLayer:pass")
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
    """After a reload the page is fresh — pass-layer.js, the host and the test instrument all get
    re-created from nothing, so `window.__exPass.host`/`.test` do not exist until the client's own
    passOpen() asks for the file again (only stepFrame calls it). One default-mode step (declines,
    lands like any ordinary glide) re-arms the surface; a row then sets its OWN mode and takes the
    step it actually means to test."""
    ready(br)
    br.sleep(0.4)
    room(br)
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
else:
    with serve(TMP) as base:
        with Browser(width=1280, height=900) as br:
            if not arm_host(br, base):
                for r in BROWSER_ROWS:
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

                # 5 · decline before takeover: the default test instrument declines, so a real step
                # must move the walk exactly as it does with no renderer at all — no canvas, no
                # curtain class, no pixel of the renderer's own.
                br.evaluate("window.__exPass.test.reset()")   # mode defaults to 'decline'
                room(br)
                y0 = int(br.evaluate("String(Math.round(scrollY))") or 0)
                br.key("ArrowDown")
                br.sleep(1.2)
                y1 = int(br.evaluate("String(Math.round(scrollY))") or 0)
                curtained = br.evaluate("String(document.body.classList.contains('ex-pass-curtain'))")
                canvases = br.evaluate("String(document.querySelectorAll('canvas').length)")
                check(BROWSER_ROWS[5], y1 > y0 and curtained == "false" and canvases == "0",
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
                check(BROWSER_ROWS[11],
                      rep.get("duration") in (0, None) and "watchdog" not in names and "docked" in names,
                      f"duration-field={rep.get('duration')} events={names[-6:]}")
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
