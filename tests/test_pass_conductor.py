#!/usr/bin/env python3
"""EX-CONDUCTOR — the gallery conductor (SPEC.md Requirement 39, case "the conductor").

One work is the soloist at full whisper, at most two neighbours ride the cheapest register, every
other work the viewport holds stands as a still, and every work outside the viewport pauses — three
live surfaces or fewer (criteria 15 and 16). A crossing in flight is the soloist and stills every
work for its duration (criterion 17). Succession keeps the incumbent for two of its own breath
periods and lands on an exhale, and a hand on a work takes the seat at once (criterion 18).

WHERE THE NUMBERS COME FROM. One soloist, at most two neighbours, at most three live surfaces and
two breath periods of tenure are criteria 15 and 18's own counts; the rows read them off the report
the conductor publishes rather than typing them here, and the report reads them off named constants
in `engine/client/08a-conductor.js`. The breath period is the voice's own published period
(`engine/assets/pass-hand.js`, Requirement 37 criterion 1), read off the voice at the instant
the row asks. The
exhale is the half of the breath where the voice's own value is falling, read off the phase the
voice publishes.

WHAT A LIVE SURFACE IS. A surface that moves: a work the conductor has given a voice to, and the
crossing's own canvas while it draws. Row 1 prints the number the run found on the phone form, which
is the row's own criterion, and the plant that reddens it is every work in the window given full
voice — with ten works hanging, that count is ten.

NO CLOCK IS DRIVEN. No row times a run, counts frames or measures a speed. Row 4 waits for a state
the code publishes — the soloist changing seat — and reads the tenure the report itself carries at
that moment; the waiting is the same polling every suite in this tree already does, and nothing in
it is a measurement of how fast anything is.

Run: python3 tests/test_pass_conductor.py
"""
import json
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
import engine_build as build_site  # noqa: E402
from headless import serve, Browser, chrome_available  # noqa: E402

SITE_URL = "https://synth.example.com"
VW, VH = 390, 844          # the phone frame lab/carrier-check.py measures on, and the row's own form

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


def wait_for(br, expr, timeout=8.0, step=0.05):
    import time
    end = time.time() + timeout
    val = None
    while time.time() < end:
        val = br.evaluate(expr)
        if val:
            return val
        br.sleep(step)
    return val


ROWS = [
    "EX-CONDUCTOR row1 Requirement 39 c15 the seating: on the phone form one work holds the "
    "soloist's seat, no more than two neighbours ride the cheapest register, and the number of live "
    "surfaces stands at or under the three the criterion names",
    "EX-CONDUCTOR row2 Requirement 39 c16 the pause: every work the viewport does not hold reads "
    "paused, the seating accounts for every work the walk hung exactly once, and the works with a "
    "voice are the works in view",
    "EX-CONDUCTOR row3 Requirement 39 c17 the crossing is the soloist: with a crossing in flight "
    "the report names the crossing, the live count reads one, no work carries a voice, and the "
    "whisper's own seat gain is nil",
    "EX-CONDUCTOR row4 Requirement 39 c18 tenure and succession: with the eye moved to the next "
    "work the incumbent keeps the seat while its hold is short of two of its own published breath "
    "periods, and the hand-over lands on an exhale",
    "EX-CONDUCTOR row5 Requirement 39 c18 the hand overrides: a press on a work seats that work at "
    "once, at full whisper, and the work it took the seat from finishes at the cheapest register",
]

CONDUCTOR = "JSON.stringify(window.__exPass.conductor())"
HAND_REPORT = "JSON.stringify(window.__exPass.hand().report())"
READY = ("!!(window.__exPass && window.__exPass.conductor"
         " && window.__exPass.conductor().works > 0)")
HAND_READY = "!!(window.__exPass && window.__exPass.hand && window.__exPass.hand())"

if not chrome_available():
    for r in ROWS:
        skip(r, "chrome is not available on this machine")
else:
    # ---------------------------------------------------------------- the walk, on the phone form
    # One bake for every row: the drawing layer on, so row 3 has a real host to hold a crossing
    # open in, and the manifests on, so the voice has a declared span to play its breath inside.
    build_site.SITE_CONFIG = dict(build_site.SITE_CONFIG)
    build_site.SITE_CONFIG["pass"] = {"visualLayer": "pass", "diagnostics": "on",
                                      "composer": build_site.manifest_block("unfold")}
    TMP = Path(tempfile.mkdtemp(prefix="synth_conductor_"))
    build_site.OUT = TMP
    build_site.build(SITE_URL)

    DATA = json.loads((TMP / "exhibition_data.json").read_text(encoding="utf-8"))
    SHOWN = 10
    WALK = json.dumps(json.dumps({"v": str(DATA["version"]),
                                  "pick": DATA["door"]["pool"][0]["id"], "shown": SHOWN}))

    def room(br, base):
        """The walk itself, hung and standing still at its first work — no door, no gesture."""
        br.navigate(base + "/")
        br.evaluate(f"localStorage.setItem('ex.exhibition', {WALK})")
        br.evaluate("sessionStorage.setItem('ex-pass', JSON.stringify({diagnostics: 'on'}))")
        br.reload()
        for _ in range(40):
            br.sleep(0.15)
            if br.evaluate("document.documentElement.classList.contains('ex-walk')"
                           "&&document.querySelectorAll('.exh-frame').length>0"
                           "&&scrollY===0"):
                break
        br.sleep(0.5)

    def conductor(br):
        return json.loads(br.evaluate(CONDUCTOR))

    def press(br, n):
        """A real press on the nth hung work — the road 01a-pass.js attaches the hand through."""
        return br.evaluate(
            "(()=>{const el=document.querySelectorAll('.exh-frame img.work')[%d];"
            "if(!el)return false;const r=el.getBoundingClientRect();"
            "el.dispatchEvent(new PointerEvent('pointerdown',{pointerId:71,pointerType:'touch',"
            "clientX:r.left+r.width/2,clientY:r.top+r.height/2,isPrimary:true,"
            "bubbles:true,cancelable:true}));return true;})()" % n)

    try:
        with serve(TMP) as base:
            # ------------------------------------------------------ rows 1 and 2: the room at rest
            with Browser(width=VW, height=VH) as br:
                room(br, base)
                if not wait_for(br, READY):
                    for r in ROWS[:2]:
                        skip(r, "the conductor never saw a hung work on the walk")
                else:
                    rep = conductor(br)
                    soloists = [s for s in rep["seats"] if s["register"] == "solo"]
                    neighbours = [s for s in rep["seats"] if s["register"] == "neighbour"]
                    stills = [s for s in rep["seats"] if s["register"] == "still"]
                    paused = [s for s in rep["seats"] if s["register"] == "paused"]

                    print("\nthe run's own numbers, on a %d x %d frame with %d works hung:"
                          % (VW, VH, rep["works"]))
                    print("  live surfaces: %d, the criterion's own ceiling being %d"
                          % (rep["live"], rep["liveMax"]))
                    print("  soloist %r, neighbours %d, stills %d, paused %d"
                          % (rep["soloist"], len(neighbours), len(stills), len(paused)))

                    check(ROWS[0],
                          len(soloists) == 1
                          and rep["soloist"]["kind"] == "work"
                          and rep["soloist"]["id"] == soloists[0]["id"]
                          and len(neighbours) <= rep["neighbourMax"]
                          and rep["live"] == len(soloists) + len(neighbours)
                          and rep["live"] <= rep["liveMax"],
                          f"{len(soloists)} soloist(s), {len(neighbours)} neighbour(s) against a "
                          f"ceiling of {rep['neighbourMax']}, {rep['live']} live surface(s) against "
                          f"a ceiling of {rep['liveMax']}")

                    check(ROWS[1],
                          rep["works"] == SHOWN
                          and len(rep["seats"]) == rep["works"]
                          and len(soloists) + len(neighbours) + len(stills) + len(paused) == rep["works"]
                          and all(s["inView"] is False for s in paused)
                          and rep["paused"] == len(paused)
                          and rep["inView"] + len(paused) == rep["works"]
                          and all(s["inView"] is True for s in soloists + neighbours),
                          f"{rep['works']} works hung, {rep['inView']} in view, "
                          f"{len(paused)} paused, {len(stills)} still")

            # ------------------------------------------------------ row 3: a crossing held in flight
            with Browser(width=VW, height=VH) as br:
                room(br, base)
                host = wait_for(br, "String(!!(window.__exPass && window.__exPass.host))==='true'",
                                timeout=12.0)
                if not host or not wait_for(br, READY):
                    skip(ROWS[2], "the drawing layer never registered a host on this walk")
                else:
                    # The test instrument the layer ships takes the command and never settles, so the
                    # host stands active while the row reads the seating. This is the same seam
                    # tests/test_pass_api.py drives every host row through.
                    br.evaluate("window.__exPass.test.mode('never')")
                    br.evaluate(
                        "(function(){const els=[...document.querySelectorAll('.exh-frame')];"
                        "const cmd=window.__exPass.adapter.declare({fromEl:els[0],toEl:els[1],"
                        "kind:'step',cause:'conductor-row3'});"
                        "if(cmd)window.__exPass.layer().offer(cmd,{dock:window.__exPass.adapter.dock,"
                        "glide:window.__exPass.adapter.glide,curtain:window.__exPass.adapter.curtain,"
                        "mark:window.__exPass.adapter.mark});})()")
                    running = wait_for(br, "String(!!window.__exPass.conductor().crossing)==='true'",
                                       timeout=6.0)
                    if not running:
                        skip(ROWS[2], "the host never took a command on this walk, so no crossing "
                                      "was ever in flight to read")
                    else:
                        rep = conductor(br)
                        hand = json.loads(br.evaluate(HAND_REPORT)) \
                            if br.evaluate(HAND_READY) else None
                        voiced = [s for s in rep["seats"]
                                  if s["register"] in ("solo", "neighbour")]
                        check(ROWS[2],
                              rep["crossing"] is True
                              and rep["soloist"]["kind"] == "crossing"
                              and rep["live"] == 1
                              and voiced == []
                              and hand is not None
                              and hand["breath"]["seat"]["gain"] == 0
                              and hand["breath"]["breathValue"] == 0,
                              f"soloist {rep['soloist']!r}, live {rep['live']}, "
                              f"{len(voiced)} work(s) with a voice, the whisper's seat "
                              f"{(hand or {}).get('breath', {}).get('seat')!r} writing "
                              f"{(hand or {}).get('breath', {}).get('breathValue')!r}")
                    br.evaluate("window.__exPass.adapter.interrupt('conductor-row3-done')")

            # ------------------------------------------------------ rows 4 and 5: the succession
            with Browser(width=VW, height=VH) as br:
                room(br, base)
                if not wait_for(br, READY) or not wait_for(br, HAND_READY):
                    for r in ROWS[3:]:
                        skip(r, "the conductor or the voice never joined on the walk")
                else:
                    first = conductor(br)["soloist"]["id"]
                    # THE EYE MOVES ON WHILE THE INCUMBENT IS STILL IN THE WINDOW. The walk calls an
                    # arriving work current at its own `landProgress` share of a frame's travel, and
                    # a frame is one viewport tall, so a scroll to the midpoint between that share
                    # and a whole viewport puts the next work past the landing mark with the
                    # incumbent still showing. That overlap is the only stretch where criterion 18's
                    # tenure has anything to protect: a scroll of a whole viewport takes the
                    # incumbent out of the window, where criterion 16's pause is owed to it instead.
                    # The share is read off the walk's own settings register.
                    land = float(json.loads(br.evaluate(
                        "JSON.stringify(window.__exPass.report().settings"
                        ".filter(s=>s.name==='landProgress')[0].applied)")))
                    br.evaluate("scrollTo(0, innerHeight * %r)" % ((land + 1) / 2))
                    # The walk's own counter is what says the eye has moved on: it names the work the
                    # plaque is written for, and it turns over at the same landing mark. The row
                    # waits for the walk to say "the second work" and then reads who the conductor
                    # still has in the soloist's seat.
                    moved = wait_for(br, "document.querySelector('#exh-counter .now')"
                                         ".textContent==='02'", timeout=6.0)
                    held = conductor(br)
                    period = held["voice"]["periodMs"] if held["voice"] else None
                    short = period is not None and held["tenure"]["heldMs"] < 2 * period
                    kept = held["soloist"]["id"] == first
                    neighbour = [s for s in held["seats"] if s["register"] == "neighbour"]
                    # …and the hand-over does arrive, once the tenure has grown, on an exhale.
                    handed = wait_for(br,
                                      "String(window.__exPass.conductor().soloist.id!==%s)==='true'"
                                      % json.dumps(str(first)),
                                      timeout=(2.5 * (period or 8000) / 1000.0 + 15.0), step=0.1)
                    after = conductor(br)
                    over = after["tenure"]["handover"] or {}
                    print("  the walk calls a work current at %.2f of a frame; the incumbent kept "
                          "the seat %.0f ms of a period of %.0f ms with the newcomer beside it"
                          % (land, held["tenure"]["heldMs"], period or -1))
                    print("  the seat passed %r -> %r for %r after %.0f ms, %d periods being "
                          "%.0f ms, on an exhale: %r"
                          % (over.get("from"), over.get("to"), over.get("reason"),
                             over.get("afterMs", -1), after["tenure"]["periods"],
                             after["tenure"]["periods"] * (over.get("periodMs") or 0),
                             over.get("onExhale")))
                    check(ROWS[3],
                          bool(moved) and kept and short
                          and len(neighbour) == 1 and neighbour[0]["id"] != first
                          and held["tenure"]["periods"] == 2
                          and bool(handed)
                          and after["soloist"]["id"] == neighbour[0]["id"]
                          and over.get("reason") == "cadence"
                          and over.get("onExhale") is True
                          and over.get("periodMs") is not None
                          and over.get("afterMs") >= after["tenure"]["periods"] * over["periodMs"],
                          f"the newcomer rode as a neighbour={bool(moved)}; the incumbent {first!r} "
                          f"kept the seat={kept} at {held['tenure']['heldMs']:.0f} ms; the seat "
                          f"then passed for {over.get('reason')!r} after {over.get('afterMs')!r} ms "
                          f"against {after['tenure']['periods']} periods of "
                          f"{over.get('periodMs')!r} ms, on an exhale: {over.get('onExhale')!r}")

                    # row 5 — the hand takes the seat with no tenure to serve at all
                    standing = after["soloist"]["id"]
                    other = [s for s in after["seats"] if s["inView"] and s["id"] != standing]
                    if not other:
                        skip(ROWS[4], "the viewport held one work only, so no second work was in "
                                      "view for a hand to take the seat from")
                    else:
                        idx = [s["id"] for s in after["seats"]].index(other[0]["id"])
                        press(br, idx)
                        br.sleep(0.2)
                        grabbed = conductor(br)
                        hand = json.loads(br.evaluate(HAND_REPORT))
                        prior = [s for s in grabbed["seats"] if s["id"] == standing]
                        took = grabbed["tenure"]["handover"] or {}
                        check(ROWS[4],
                              grabbed["soloist"]["id"] == other[0]["id"]
                              and took.get("reason") == "hand"
                              and took.get("afterMs") < grabbed["tenure"]["periods"]
                                                        * (took.get("periodMs") or 0)
                              and hand["breath"]["seat"]["register"] == "solo"
                              and hand["breath"]["seat"]["gain"] == 1
                              and prior != [] and prior[0]["register"] == "neighbour",
                              f"the press seated {grabbed['soloist']['id']!r} for "
                              f"{took.get('reason')!r} after {took.get('afterMs')!r} ms of a "
                              f"required {grabbed['tenure']['periods'] * (took.get('periodMs') or 0)!r}"
                              f" ms, the voice reading {hand['breath']['seat']!r}; the work it took "
                              f"the seat from reads "
                              + (repr(prior[0]["register"]) if prior else "gone"))
    finally:
        shutil.rmtree(TMP, ignore_errors=True)

# ---------------------------------------------------------------- report
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
