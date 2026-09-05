#!/usr/bin/env python3
"""EX-STANDING — the standing work is drawn breathing on the walk (SPEC.md Requirement 37).

The whisper voice computes a breath (Requirement 37, `engine/assets/pass-hand.js`) and the gallery
conductor says whose it is (Requirement 39, `engine/client/08a-conductor.js`). Until
`engine/client/08b-standing.js` both stopped at a report, and a visitor walking the gallery met
neither. This suite reads the surface: what a person actually sees.

HOW A ROW READS IT. Two photographs of one work, taken at two moments of the work's own breath, and
the work's own box compared between them — the box the hang measured, which is the box a crossing is
seated in (Requirement 91's `hangGeometry`). The soloist's box moves; the box of a work the
conductor gave no seat is identical byte for byte. That is the whole reading, and it is a reading of
what was DRAWN.

NO CLOCK IS DRIVEN. No row times a run, counts frames or measures a speed. A row waits for a value
the code publishes — the breath's own reading between -1 and 1 — and photographs the page when that
value has arrived. The waiting is the same polling every browser suite in this tree already does.

WHERE THE NUMBERS COME FROM.

  The amplitude. Requirement 37 states the band as fractions of a letter's full crossing travel —
  criterion 1's thirty-second for the breath, criterion 3's sixth for the hard cap — and states the
  same ceiling again in the units a drawn frame has: criterion 4, "at rest, any frame shall differ
  from the canonical work by under 1 % of frame width in any pixel's displacement". So on a drawn
  frame the letter's travel is six percent of the frame's own width and the breath is a
  thirty-second of that. Row 5 reads those three fractions off the renderer's own report and
  reconstructs the amplitude from the box read independently out of the DOM, so neither the fraction
  nor the box is typed here.

  The bar for "a still at any instant is still the work". The charter's own door bar of 6 of 255 over
  the frame, read out of `engine/assets/pass-inst-unfold.js` — the same road `tests/test_pass_whisper.py`
  reads it by, and the one place in this tree that states in these words how much may stand in a
  frame and it still BE the photograph.

WHAT REDDENS THIS SUITE. The plant the row itself names: a renderer that ignores the voice. With the
breath's own reading replaced by nothing in `engine/client/08b-standing.js`, the two photographs of
the drawn work become identical — 0.0000 of 255 where a breathing work reads about 2 — and rows 1, 2
and 3 all go red on both forms.

WHAT THE FIXTURE CAN AND CANNOT SAY. The synthetic gallery hangs 64 px works, so the box is the same
on the phone form and on the desk form and the two rows read the same amplitude. Both forms are run
because the row asks for both; what differs between them is the walk around the work, not the work.

Run: python3 tests/test_pass_standing.py
"""
import base64
import json
import re
import shutil
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
import engine_build as build_site  # noqa: E402
from headless import serve, Browser, chrome_available  # noqa: E402

SITE_URL = "https://synth.example.com"
PHONE = (390, 844)     # the phone frame lab/carrier-check.py measures on
DESK = (1280, 900)     # the desk frame every other walk row reads

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


def wait_for(br, expr, timeout=8.0, step=0.05):
    end = time.time() + timeout
    val = None
    while time.time() < end:
        val = br.evaluate(expr)
        if val:
            return val
        br.sleep(step)
    return val


ROWS = [
    "EX-STANDING row1 the walk on the phone form: two photographs of the seated work at two moments "
    "of its own breath stand apart, and every other work in the same viewport is identical between "
    "the same two photographs",
    "EX-STANDING row2 the walk on the desk form: the same reading, on the frame the desk hangs",
    "EX-STANDING row3 Requirement 37 c4 the screenshot law: the breath walked from one end to the "
    "other moves the work, and moves it less than the charter's own door bar of the work, so a "
    "still taken at any instant of it is still the work — the bar read out of the instrument's own "
    "file",
    "EX-STANDING row4 Requirement 39 c15 to c17 the seating reaches the picture: the work the "
    "conductor voiced is the work being drawn and the only picture on the walk carrying a breath, "
    "and with a crossing in flight no picture carries one",
    "EX-STANDING row5 the band: the travel the renderer draws is criterion 1's thirty-second of "
    "criterion 3's sixth read on criterion 4's one percent of the box the hang measured, the box "
    "read a second way out of the document and the amplitude typed nowhere",
]

# The door bar, read out of the instrument's own source rather than typed here — the same read
# tests/test_pass_whisper.py takes, for the same question.
INST_SRC = (ROOT / "engine" / "assets" / "pass-inst-unfold.js").read_text(encoding="utf-8")
_bar = re.search(r"The charter's own door bar is\s+//?\s*(\d+(?:\.\d+)?) of 255", INST_SRC) \
    or re.search(r"door bar is (\d+(?:\.\d+)?) of 255", INST_SRC.replace("\n", " ").replace("//", " "))
DOOR_BAR = float(_bar.group(1)) if _bar else None

try:
    from PIL import Image, ImageChops, ImageStat  # noqa: F401
    HAVE_PIL = True
except ImportError:
    HAVE_PIL = False

if not chrome_available():
    for r in ROWS:
        skip(r, "chrome is not available on this machine")
elif not HAVE_PIL:
    for r in ROWS:
        skip(r, "Pillow is absent, so no frame can be read")
elif DOOR_BAR is None:
    for r in ROWS:
        skip(r, "the charter's own door bar could not be read out of pass-inst-unfold.js")
else:
    # One bake for every row: the drawing layer on, so row 4 has a real host to hold a crossing open
    # in, and the manifests on, so the voice has a declared span behind the breath it publishes.
    build_site.SITE_CONFIG = dict(build_site.SITE_CONFIG)
    build_site.SITE_CONFIG["pass"] = {"visualLayer": "pass", "diagnostics": "on",
                                      "composer": build_site.manifest_block("unfold")}
    TMP = Path(tempfile.mkdtemp(prefix="synth_standing_"))
    build_site.OUT = TMP
    build_site.build(SITE_URL)
    SHOTS = Path(tempfile.mkdtemp(prefix="synth_standing_shots_"))

    DATA = json.loads((TMP / "exhibition_data.json").read_text(encoding="utf-8"))
    SHOWN = 10
    WALK = json.dumps(json.dumps({"v": str(DATA["version"]),
                                  "pick": DATA["door"]["pool"][0]["id"], "shown": SHOWN}))

    READY = ("!!(window.__exPass && window.__exPass.standing"
             " && window.__exPass.standing().drawing)")

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
        br.sleep(0.6)

    def standing(br):
        return json.loads(br.evaluate("JSON.stringify(window.__exPass.standing())"))

    def boxes(br):
        """Every hung work's own picture box, read out of the document — a second road to the
        geometry the renderer takes through `hangGeometry`.

        The breath the renderer is drawing is a scale, and a scale is inside a bounding rectangle,
        so a picture carrying one would measure its own breath back. The breath is lifted off and put
        straight back inside the same task, with the rectangle read between — the compositor is never
        handed the moment in between, and what comes back is the box the walk hung, which is exactly
        the box `hangGeometry` reads when the renderer takes a work."""
        return json.loads(br.evaluate(
            "JSON.stringify(Object.fromEntries([...document.querySelectorAll('.exh-frame')]"
            ".map(f=>{const im=f.querySelector('img.work');const s=im.style.scale;"
            "im.style.scale='';const r=im.getBoundingClientRect().toJSON();"
            "im.style.scale=s;return [f.dataset.id, r];})))"))

    def scales(br):
        """What breath each picture on the walk is carrying this instant, by work."""
        return json.loads(br.evaluate(
            "JSON.stringify(Object.fromEntries([...document.querySelectorAll('.exh-frame')]"
            ".map(f=>[f.dataset.id, f.querySelector('img.work').style.scale||''])))"))

    def png(br, name):
        d = br._cmd("Page.captureScreenshot", format="png", captureBeyondViewport=False)
        p = SHOTS / name
        p.write_bytes(base64.b64decode(d["data"]))
        return p

    # THE TWO MOMENTS ARE THE BREATH'S OWN TWO ENDS, where its curve is flattest and a reading is
    # therefore not a race: the crest and the trough. Nothing is timed — the row reads the value the
    # renderer publishes and stops when it has arrived.
    CREST, TROUGH, END_TOL = 1.0, -1.0, 0.03

    def at_unit(br, target, tol=END_TOL, limit=14.0):
        end = time.time() + limit
        got = None
        while time.time() < end:
            got = float(br.evaluate("String(window.__exPass.standing().unit)"))
            if abs(got - target) < tol:
                return got
            br.sleep(0.05)
        return None

    def apart(pa, pb, box, vw):
        """Mean channel distance of 255 inside one work's own box — the idiom every instrument suite
        in this tree already carries for «is this frame that work»."""
        ia, ib = Image.open(pa).convert("RGB"), Image.open(pb).convert("RGB")
        if ia.size != ib.size:
            return 255.0
        sc = ia.width / float(vw)
        cut = (int(box["x"] * sc), int(box["y"] * sc),
               int((box["x"] + box["width"]) * sc), int((box["y"] + box["height"]) * sc))
        return sum(ImageStat.Stat(ImageChops.difference(ia.crop(cut), ib.crop(cut))).mean) / 3.0

    def walk_form(br, base, tag, vw):
        """Two photographs of one walk at the two ends of the seated work's own breath, and the
        distance each work in view stands from itself between them."""
        room(br, base)
        if not wait_for(br, READY, timeout=12.0):
            return None
        rep = standing(br)
        seats = json.loads(br.evaluate("JSON.stringify(window.__exPass.conductor().seats)"))
        bx = boxes(br)
        solo = rep["drawing"]
        if solo is None or solo not in bx:
            return None
        # THE PAGE IS PHOTOGRAPHED UNTIL IT HAS SETTLED, and the settling is read rather than waited
        # out by a clock. A picture given a breath is composited on its own layer from that frame on,
        # and the first rasterings after that promotion differ from the later ones by up to 3 of 255
        # — a difference of the promotion, not of the breath. So the drawn work is photographed at
        # the SAME point of its breath over and over until three of those photographs running are
        # identical. The settling comes in stages, so one identical pair is not yet stillness; three
        # running is. After that a photograph pair costs nothing of its own.
        prev, crest, u_hi, same = None, None, None, 0
        for i in range(9):
            u_hi = at_unit(br, CREST)
            crest = png(br, "%s-crest-%d.png" % (tag, i))
            same = (same + 1) if (prev is not None
                                  and apart(prev, crest, bx[solo], vw) == 0.0) else 0
            prev = crest
            if same >= 2:
                break
        u_lo = at_unit(br, TROUGH)
        trough = png(br, tag + "-trough.png")
        moved = {s["id"]: apart(crest, trough, bx[s["id"]], vw)
                 for s in seats if s["inView"] and bx[s["id"]]["width"] > 0}
        # AND THE FLOOR IS BRACKETED ACROSS THE VERY STRETCH THE READING COVERS: the drawn work is
        # photographed once more at the SAME end of its breath the first photograph was taken at.
        # What that pair reads is the width of the window a row waits inside — the two photographs
        # are at the same end of the curve but not at the same point of it — and everything else a
        # photograph pair costs over that stretch. The reading below is the two ENDS of the same
        # breath, and it has to stand above this. A renderer that ignored the voice would put both
        # readings at the same number, which is what reddens the row.
        at_unit(br, CREST)
        floor = apart(crest, png(br, tag + "-crest-again.png"), bx[solo], vw)
        return {"rep": rep, "seats": seats, "boxes": bx, "moved": moved, "floor": floor,
                "settled": same >= 2, "units": (u_hi, u_lo), "shots": (crest, trough)}

    try:
        with serve(TMP) as base:
            # ------------------------------------------------ rows 1, 3 and 5: the walk on a phone
            with Browser(width=PHONE[0], height=PHONE[1]) as br:
                got = walk_form(br, base, "phone", PHONE[0])
                if not got:
                    for r in (ROWS[0], ROWS[2], ROWS[4]):
                        skip(r, "the standing renderer never drew a work on the walk")
                else:
                    solo = got["rep"]["drawing"]
                    others = {k: v for k, v in got["moved"].items() if k != solo}
                    print("\nthe run's own numbers, on a %d x %d frame with %d works hung:"
                          % (PHONE + (len(got["seats"]),)))
                    print("  the breath read at the two photographs: %r and %r"
                          % got["units"])
                    print("  the work being drawn, %s, stands %.4f of 255 from itself between them,"
                          " against a floor of %r bracketed on the same work at one point of its breath"
                          % (solo, got["moved"].get(solo, -1), got["floor"]))
                    for k, v in sorted(others.items()):
                        print("  the work %s, which the conductor gave no voice, stands %.4f of 255"
                              % (k, v))
                    check(ROWS[0],
                          got["units"][0] is not None and got["units"][1] is not None
                          and solo is not None
                          and got["settled"]
                          and got["moved"].get(solo, 0) > got["floor"]
                          and others != {}
                          and all(v == 0.0 for v in others.values()),
                          f"the breath read {got['units']!r}; the drawn work {solo!r} stands "
                          f"{got['moved'].get(solo)!r} of 255 from itself against a floor of "
                          f"{got['floor']!r}, the {len(others)} unvoiced work(s) in view standing "
                          f"{sorted(others.values())!r}")

                    # row 3 — the whole swing of the breath, end to end, inside the charter's bar
                    swing = got["moved"].get(solo, -1)
                    print("  the charter's door bar, read out of pass-inst-unfold.js: %.1f of 255"
                          % DOOR_BAR)
                    check(ROWS[2],
                          swing > 0 and swing < DOOR_BAR,
                          f"the breath walked end to end moves the work {swing!r} of 255, the bar "
                          f"being {DOOR_BAR}")

                    # row 5 — the band, reconstructed from the fractions and the box
                    law = got["rep"]["law"]
                    frame = got["rep"]["frame"]
                    want = (got["boxes"][solo]["width"]
                            * law["stillOfFrameWidth"] * law["capOfTravel"] / law["breathOfTravel"])
                    scale_hi = float(json.loads(br.evaluate(
                        "JSON.stringify(String(window.__exPass.standing().scale||''))")) or 1)
                    print("  the box the document reads for %s is %.4f wide; the amplitude the "
                          "renderer draws is %.6f px against %.6f px rebuilt from the fractions"
                          % (solo, got["boxes"][solo]["width"], frame["amplitudePx"], want))
                    check(ROWS[4],
                          law["stillOfFrameWidth"] == 0.01
                          and law["capOfTravel"] == 6 and law["breathOfTravel"] == 32
                          and abs(frame["amplitudePx"] - want) < 1e-9
                          and frame["reachPx"] > frame["amplitudePx"]
                          and frame["amplitudePx"]
                          < got["boxes"][solo]["width"] * law["stillOfFrameWidth"]
                          and abs(scale_hi - 1) * frame["reachPx"] <= frame["amplitudePx"] + 1e-9,
                          f"the fractions read {law!r}; the amplitude drawn is "
                          f"{frame['amplitudePx']!r} px against {want!r} px rebuilt from the box "
                          f"the document reads, criterion 4's own ceiling on that box being "
                          f"{got['boxes'][solo]['width'] * law['stillOfFrameWidth']!r} px; the "
                          f"scale standing on the picture is {scale_hi!r}")

            # ------------------------------------------------------------ row 2: the walk on a desk
            with Browser(width=DESK[0], height=DESK[1]) as br:
                got = walk_form(br, base, "desk", DESK[0])
                if not got:
                    skip(ROWS[1], "the standing renderer never drew a work on the walk")
                else:
                    solo = got["rep"]["drawing"]
                    others = {k: v for k, v in got["moved"].items() if k != solo}
                    print("\nthe run's own numbers, on a %d x %d frame:" % DESK)
                    print("  the breath read at the two photographs: %r and %r" % got["units"])
                    print("  the work being drawn, %s, stands %.4f of 255 from itself between them,"
                          " against a floor of %r bracketed on the same work at one point of its breath"
                          % (solo, got["moved"].get(solo, -1), got["floor"]))
                    for k, v in sorted(others.items()):
                        print("  the work %s, which the conductor gave no voice, stands %.4f of 255"
                              % (k, v))
                    check(ROWS[1],
                          got["units"][0] is not None and got["units"][1] is not None
                          and solo is not None
                          and got["settled"]
                          and got["moved"].get(solo, 0) > got["floor"]
                          and others != {}
                          and all(v == 0.0 for v in others.values()),
                          f"the breath read {got['units']!r}; the drawn work {solo!r} stands "
                          f"{got['moved'].get(solo)!r} of 255 from itself against a floor of "
                          f"{got['floor']!r}, the {len(others)} unvoiced work(s) in view standing "
                          f"{sorted(others.values())!r}")

            # ----------------------------------------------- row 4: the seating reaches the picture
            with Browser(width=PHONE[0], height=PHONE[1]) as br:
                room(br, base)
                host = wait_for(br, "String(!!(window.__exPass && window.__exPass.host))==='true'",
                                timeout=12.0)
                if not host or not wait_for(br, READY, timeout=12.0):
                    skip(ROWS[3], "the drawing layer never registered a host on this walk")
                else:
                    rep = standing(br)
                    voiced = json.loads(br.evaluate(
                        "JSON.stringify(window.__exPass.conductor().seats"
                        ".filter(s=>s.register==='solo'||s.register==='neighbour')"
                        ".map(s=>s.id))"))
                    carrying = [k for k, v in scales(br).items() if v]
                    # The test instrument the layer ships takes the command and never settles, so the
                    # host stands active while the row reads the walk. The same seam every host row
                    # in this tree drives a held crossing through.
                    br.evaluate("window.__exPass.test.mode('never')")
                    br.evaluate(
                        "(function(){const els=[...document.querySelectorAll('.exh-frame')];"
                        "const cmd=window.__exPass.adapter.declare({fromEl:els[0],toEl:els[1],"
                        "kind:'step',cause:'standing-row4'});"
                        "if(cmd)window.__exPass.layer().offer(cmd,{dock:window.__exPass.adapter.dock,"
                        "glide:window.__exPass.adapter.glide,curtain:window.__exPass.adapter.curtain,"
                        "mark:window.__exPass.adapter.mark});})()")
                    # THE READING IS ONE INSTANT'S. A held crossing on this bake is over in a
                    # fraction of a second, so the crossing, the renderer's report and what each
                    # picture is carrying are read in ONE expression — a state read between them
                    # would report a walk that had already come back to rest.
                    in_flight = wait_for(
                        br,
                        "(function(){var c=window.__exPass.conductor().crossing;if(!c)return '';"
                        "return JSON.stringify({crossing:c,standing:window.__exPass.standing(),"
                        "carrying:[...document.querySelectorAll('.exh-frame')]"
                        ".filter(f=>f.querySelector('img.work').style.scale)"
                        ".map(f=>f.dataset.id)});})()",
                        timeout=6.0)
                    if not in_flight:
                        skip(ROWS[3], "the host never took a command on this walk, so no crossing "
                                      "was ever in flight to read")
                    else:
                        during = json.loads(in_flight)
                        print("\n  at rest the conductor voiced %r and the walk carried a breath on "
                              "%r; with a crossing in flight the renderer draws %r and the walk "
                              "carries %r"
                              % (voiced, carrying, during["standing"]["drawing"],
                                 during["carrying"]))
                        check(ROWS[3],
                              rep["drawing"] in voiced
                              and carrying == [rep["drawing"]]
                              and during["crossing"] is True
                              and during["standing"]["drawing"] is None
                              and during["standing"]["unit"] == 0
                              and during["carrying"] == [],
                              f"at rest the renderer drew {rep['drawing']!r} of the voiced "
                              f"{voiced!r} and the walk carried a breath on {carrying!r}; under a "
                              f"crossing it draws {during['standing']['drawing']!r} reading "
                              f"{during['standing']['unit']!r}, the walk carrying "
                              f"{during['carrying']!r}")
                    br.evaluate("window.__exPass.adapter.interrupt('standing-row4-done')")
    finally:
        shutil.rmtree(TMP, ignore_errors=True)
        shutil.rmtree(SHOTS, ignore_errors=True)

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
