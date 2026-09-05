#!/usr/bin/env python3
"""EX-WHISPER — the whisper law, standing life at rest (SPEC.md Requirement 37).

A work at rest breathes. This suite holds the two halves of that sentence: the band the breath
keeps, read off the voice itself, and the screenshot law, read off drawn frames.

WHERE THE NUMBERS COME FROM.

  R, a letter's full crossing travel. Requirement 37 criterion 1 carries a gap: no measured value
  for R exists. R here is the handle's own declared span, `max - min`, off the instrument's own
  manifest — the one place a handle's travel is already written down and already read, by
  `passHandleSpan` (engine/client/01a-pass.js:1358-1368) on the walk and by `bench.manifest` on the
  bench. It is read twice from two independent places in this file and typed in neither: the voice
  reads it through the host, and the rows below read it out of the site's own settings record.

  The screenshot law's own bar. Criterion 4 asks a frame at rest to differ from the canonical work
  by under 1 % of frame width in any pixel's displacement. Nothing in this tree measures a pixel's
  displacement, and Requirement 37's own gap line names what to follow instead — "the seam bench is
  the pattern they would follow". The bar the tree does hold frames to, and the one this
  instrument's own file quotes for exactly this question, is the charter's door bar of 6 of 255 over
  the canvas rect (`engine/assets/pass-inst-unfold.js:797-799`, beside DOOR_HOLD, where its comment
  asks in these very words how much may stand in the frame at a door "and it still BE the
  photograph"). The rows below read the bar out of that file rather than typing it, and they print
  what the run measured against it.

WHAT THE RUN FOUND ABOUT THIS MATTER, AND WHICH LETTER CARRIES THE BREATH.

  A work at rest stands at its door, which is the neutral pose this instrument publishes and the
  photograph standing whole. There `unfold` freezes every letter it declares but one: walked to both
  ends at the door, tilt, shade, depth, stagger, the panel count, the clock, the parquet's three and
  the field all move exactly 0.000 of 255 (measured 2026-09-05 on this bench, and row 6 below reads
  the hinge's two ends every run so the finding cannot rot). It is the instrument's own repair of
  2026-08-13, which made the sheet stand square at its door at any tilt and at any second. So the
  letter that carries a standing work's breath is the making axis — Requirement 37 criterion 6's own
  "final letter of the recipe", and Requirement 39 criterion 19's making-axis verb at micro-gain.

  How far that letter is granted to travel is what this run measures, rather than a fraction typed
  anywhere: the furthest the making axis opens while the drawn frame still stands inside the door bar
  of the work. That is this row's answer to criterion 1's recorded gap. R stays the handle's own
  declared span and the thirty-second names a ceiling; the door bar names the travel a standing work
  is actually granted; and the run prints both, because on this matter they are far apart.

WHAT IS NOT HERE. Criterion 5's nearest-self-similar-level comparison belongs to the crystal family
and reaches no letter of `unfold`; it is S-40's, the six families. Criterion 4's under-the-hand 3 %
is S-38's, held by tests/test_pass_hand.py's chart-law row.

NO CLOCK IS DRIVEN. Every row reads a value the code published or a frame the code drew. Nothing
here times a run, counts frames or measures a speed. The period is read as the three numbers the
voice itself publishes.

Run: python tests/test_pass_whisper.py
"""
import base64
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
import engine_build as build_site  # noqa: E402
from headless import serve, Browser, chrome_available  # noqa: E402

SITE_URL = "https://synth.example.com"
LAB = Path(__import__("os").environ.get("TLVPHOTOS_ROOT", "/Users/sashaabramovich/tlvphotos")) / "lab"
PHOTOS = [LAB / "photos" / "towers.jpg", LAB / "photos" / "glassgrid.jpg"]
MODULE = LAB / "effects" / "unfold.js"
VW, VH = 390, 844          # the phone frame lab/carrier-check.py measures on

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
    "EX-WHISPER row1 Requirement 37 c1 the band: the amplitude the voice plays is a thirty-second "
    "of the travel the instrument's own manifest declares for that letter, the two numbers read "
    "from two independent places and typed in neither",
    "EX-WHISPER row2 Requirement 37 c1 the period: its floor is at least eight seconds, the rubato "
    "makes it wander, and the period this instant lies inside the floor and the ceiling the voice "
    "publishes",
    "EX-WHISPER row3 Requirement 37 standing life at rest: with no pointer event ever dispatched "
    "the voice is running at full gain, two readings of it differ, and the letter it writes carries "
    "the breath and stays inside the band",
    "EX-WHISPER row4 Requirement 37 c13 micro-motion survives every state: under a press held "
    "still the gain reads a quarter and the letter still carries a breath",
    "EX-WHISPER row5 Requirement 37 c3 the hard cap: the caps the voice publishes are a sixth of "
    "each letter's declared travel, and every value it writes sits inside them",
    "EX-WHISPER row6 Requirement 37 c4 the screenshot law: at the work's own resting pose the "
    "hinge is frozen end to end, and the travel the making axis is granted moves the frame while "
    "keeping it inside the charter's own door bar of the work, the bar read out of the "
    "instrument's own file",
    "EX-WHISPER row7 Requirement 37 c4 the bar is not vacuous: the same letter walked to "
    "criterion 1's own ceiling stands outside it",
]

# ---------------------------------------------------------------- the two numbers, off the files
# The door bar, read out of the instrument's own source rather than typed here. Its comment at
# :797-799 states it for exactly this question — how much may stand in the frame at a door and it
# still BE the photograph.
INST_SRC = (ROOT / "engine" / "assets" / "pass-inst-unfold.js").read_text(encoding="utf-8")
_bar = re.search(r"The charter's own door bar is\s+//?\s*(\d+(?:\.\d+)?) of 255", INST_SRC) \
    or re.search(r"door bar is (\d+(?:\.\d+)?) of 255", INST_SRC.replace("\n", " ").replace("//", " "))
DOOR_BAR = float(_bar.group(1)) if _bar else None

if not chrome_available():
    for r in ROWS:
        skip(r, "chrome is not available on this machine")
elif DOOR_BAR is None:
    for r in ROWS:
        skip(r, "the charter's own door bar could not be read out of pass-inst-unfold.js")
elif [p for p in ([MODULE] + PHOTOS) if not p.exists()]:
    for r in ROWS:
        skip(r, "the lab module or its photographs are absent: "
                + ", ".join(str(p) for p in ([MODULE] + PHOTOS) if not p.exists()))
else:
    # ------------------------------------------------------------ bench A: the walk, and the voice
    build_site.SITE_CONFIG = dict(build_site.SITE_CONFIG)
    build_site.SITE_CONFIG["pass"] = {"composer": build_site.manifest_block("unfold")}
    WALK_TMP = Path(tempfile.mkdtemp(prefix="synth_whisper_walk_"))
    build_site.OUT = WALK_TMP
    build_site.build(SITE_URL)

    DATA = json.loads((WALK_TMP / "exhibition_data.json").read_text(encoding="utf-8"))
    WALK = json.dumps(json.dumps({"v": str(DATA["version"]),
                                  "pick": DATA["door"]["pool"][0]["id"], "shown": 10}))

    # R, read from the site's own settings record — the file the walk is served, and a different
    # road from the one the voice itself takes through `passHandleSpan`.
    _record = json.loads((WALK_TMP / "config.json").read_text(encoding="utf-8"))
    _handles = _record["pass"]["composer"]["manifests"]["unfold"]["handles"]
    R_TILT = float(_handles["tilt"]["max"]) - float(_handles["tilt"]["min"])
    R_MIX = float(_handles["mix"]["max"]) - float(_handles["mix"]["min"])

    HAND_READY = "!!(window.__exPass && window.__exPass.hand && window.__exPass.hand())"

    def hand_report(br):
        return json.loads(br.evaluate("JSON.stringify(window.__exPass.hand().report())"))

    def room(br, base):
        br.navigate(base + "/")
        br.evaluate(f"localStorage.setItem('ex.exhibition', {WALK})")
        br.evaluate("localStorage.setItem('ex-tempo','0.2')")
        br.evaluate("sessionStorage.setItem('ex-pass', JSON.stringify({diagnostics: 'on'}))")
        br.reload()
        for _ in range(40):
            br.sleep(0.15)
            if br.evaluate("document.documentElement.classList.contains('ex-walk')"
                           "&&document.querySelectorAll('.exh-frame').length>0"
                           "&&scrollY===0"):
                break
        br.sleep(0.3)

    WORK = ".exh-frame img.work"

    def fire(br, kind_of_event, pointer_kind, nx=0.5, ny=0.5, pointer_id=41):
        return br.evaluate(
            "(()=>{const el=document.querySelector(%s);if(!el)return false;"
            "const r=el.getBoundingClientRect();"
            "el.dispatchEvent(new PointerEvent(%s,{pointerId:%s,pointerType:%s,"
            "clientX:r.left+r.width*%s,clientY:r.top+r.height*%s,isPrimary:true,"
            "bubbles:true,cancelable:true}));return true;})()"
            % (json.dumps(WORK), json.dumps(kind_of_event), pointer_id,
               json.dumps(pointer_kind), nx, ny))

    try:
        with serve(WALK_TMP) as base:
            # rows 1, 2, 3, 5 — the voice with no hand anywhere near it
            with Browser(width=1280, height=900) as br:
                room(br, base)
                if not wait_for(br, HAND_READY):
                    for r in ROWS[:5]:
                        skip(r, "the hand layer never joined on the walk")
                    rest = None
                else:
                    rest = hand_report(br)
                    rest2 = hand_report(br)

                    amp = rest["breath"]["breathAmplitude"]
                    check(ROWS[0],
                          rest["breath"]["handle"] == "mix"
                          and abs(amp - R_MIX / 32) < 1e-12,
                          f"the voice plays {amp!r} on {rest['breath']['handle']!r}; the settings "
                          f"record declares a travel of {R_MIX!r} for that letter, a thirty-second "
                          f"of which is {R_MIX / 32!r}")

                    per = rest["breath"]["period"]
                    check(ROWS[1],
                          per["minMs"] >= 8000
                          and per["maxMs"] > per["minMs"]
                          and per["minMs"] <= per["periodMs"] <= per["maxMs"],
                          f"floor {per['minMs']} ms, ceiling {per['maxMs']} ms, rubato "
                          f"{per['rubato']!r}, this instant {per['periodMs']:.1f} ms")

                    v1, v2 = rest["breath"]["breathValue"], rest2["breath"]["breathValue"]
                    x1 = rest["chart"]["unfold"]["x"]
                    check(ROWS[2],
                          rest["breath"]["running"] is True
                          and rest["breath"]["gain"] == 1
                          and rest["verb"] is None
                          and v1 != v2
                          and x1["handle"] == "mix"
                          and abs(x1["value"] - v1) < 1e-12
                          and abs(x1["value"]) <= amp + 1e-12,
                          f"running={rest['breath']['running']} gain={rest['breath']['gain']} "
                          f"verb={rest['verb']!r} two readings {v1!r} then {v2!r}; the letter "
                          f"carries {x1['value']!r} inside a band of {amp!r}")

                    caps = (rest["breath"]["cap"], rest["tilt"]["cap"])
                    ch = rest["chart"]["unfold"]
                    check(ROWS[4],
                          abs(caps[0] - R_MIX / 6) < 1e-12
                          and abs(caps[1] - R_TILT / 6) < 1e-12
                          and abs(ch["x"]["value"]) <= caps[0] + 1e-12
                          and abs(ch["y"]["value"]) <= caps[1] + 1e-12
                          # the eighth the lean is allowed and the thirty-second the breath is
                          # allowed ride one letter and add under the sixth — criteria 1, 2 and 3
                          # read together on one travel
                          and R_MIX / 8 + R_MIX / 32 <= R_MIX / 6,
                          f"caps {caps!r} against a sixth of {R_MIX!r} and {R_TILT!r}; "
                          f"the letters carry {ch['x']['value']!r} and {ch['y']['value']!r}")

            # row 4 — the press held still: the gain drops to a quarter and the breath goes on
            with Browser(width=1280, height=900) as br:
                room(br, base)
                if not wait_for(br, HAND_READY):
                    skip(ROWS[3], "the hand layer never joined on the walk")
                else:
                    fire(br, "pointerover", "touch")
                    fire(br, "pointerdown", "touch")
                    held = wait_for(br,
                                    "(()=>window.__exPass.hand().report().hold.active===true)()",
                                    timeout=4.0)
                    r4 = hand_report(br)
                    r4b = hand_report(br)
                    check(ROWS[3],
                          bool(held)
                          and abs(r4["breath"]["gain"] - 0.25) < 1e-9
                          and r4["breath"]["running"] is True
                          and r4["breath"]["breathValue"] != r4b["breath"]["breathValue"],
                          f"held={held} gain={r4['breath']['gain']!r} running={r4['breath']['running']} "
                          f"two readings under the press {r4['breath']['breathValue']!r} then "
                          f"{r4b['breath']['breathValue']!r}")
    finally:
        shutil.rmtree(WALK_TMP, ignore_errors=True)

    # ------------------------------------------------------------ bench B: the drawn standing work
    build_site.SITE_CONFIG = dict(build_site.SITE_CONFIG)
    build_site.SITE_CONFIG["pass"] = {"visualLayer": "pass", "diagnostics": "on"}
    DRAW_TMP = Path(tempfile.mkdtemp(prefix="synth_whisper_draw_"))
    build_site.OUT = DRAW_TMP
    build_site.build(SITE_URL)

    BENCH = Path(tempfile.mkdtemp(prefix="synth_whisper_bench_"))
    shutil.copy2(DRAW_TMP / "pass-layer.js", BENCH / "pass-layer.js")
    for _inst in sorted(DRAW_TMP.glob("pass-inst-*.js")):
        shutil.copy2(_inst, BENCH / _inst.name)
    shutil.copy2(DRAW_TMP / "config.json", BENCH / "config.json")
    shutil.copy2(MODULE, BENCH / "unfold.js")
    (BENCH / "photos").mkdir()
    for _p in PHOTOS:
        shutil.copy2(_p, BENCH / "photos" / _p.name)
    shutil.copy2(ROOT / "tests" / "fixture_pass_unfold.html", BENCH / "index.html")
    SHOTS = Path(tempfile.mkdtemp(prefix="synth_whisper_shots_"))

    def png(br, name):
        d = br._cmd("Page.captureScreenshot", format="png", captureBeyondViewport=False)
        p = SHOTS / name
        p.write_bytes(base64.b64decode(d["data"]))
        return p

    def apart(p, q):
        """Mean channel distance between two frames, of 255 — the idiom every instrument suite in
        this tree already carries for "is this frame that work"."""
        from PIL import Image, ImageChops, ImageStat
        a = Image.open(p).convert("RGB")
        c = Image.open(q).convert("RGB")
        if a.size != c.size:
            return 255.0
        return sum(ImageStat.Stat(ImageChops.difference(a, c)).mean) / 3.0

    try:
        with serve(BENCH) as base:
            with Browser(width=VW, height=VH) as br:
                br.navigate(base + "/index.html")
                if not wait_for(br, "String(!!window.__ready)==='true'", timeout=40.0):
                    for r in ROWS[5:]:
                        skip(r, "the pass bench never became ready")
                else:
                    man = json.loads(br.evaluate(
                        "JSON.stringify((function(){var m=window.__exPass.bench.manifest('unfold');"
                        "return {handles:m.handles,neutral:m.neutralPose};})())"))
                    span_mix = float(man["handles"]["mix"]["max"]) - float(man["handles"]["mix"]["min"])
                    rest_tilt = float(man["neutral"]["tilt"])
                    door_mix = float(man["neutral"]["mix"])
                    br.evaluate("window.__show('host'); 0")
                    br.sleep(0.3)

                    def draw(name, mix, tilt):
                        br.evaluate("window.__drawWith(%s); 0"
                                    % json.dumps({"mix": mix, "tilt": tilt, "t": 0}))
                        br.sleep(0.35)
                        return png(br, name)

                    # THE CANONICAL WORK: the neutral pose the instrument itself publishes, which is
                    # its entry door — the photograph standing whole.
                    door = draw("door.png", door_mix, rest_tilt)

                    # THE HINGE IS FROZEN HERE, and this is the reading that says so: the letter U3
                    # gave the voice, walked from one end of its declared travel to the other at the
                    # resting pose, moves the frame by nothing at all.
                    hinge_lo = apart(door, draw("hinge-lo.png", door_mix,
                                                float(man["handles"]["tilt"]["min"])))
                    hinge_hi = apart(door, draw("hinge-hi.png", door_mix,
                                                float(man["handles"]["tilt"]["max"])))

                    # HOW FAR THE BREATH IS GRANTED TO TRAVEL. The furthest the making axis opens
                    # while the drawn frame still stands inside the door bar of the work: a
                    # bisection on the drawn frame, twelve halvings from the letter's own declared
                    # travel down. Nothing is timed; each step reads one frame that was drawn.
                    lo, hi = door_mix, door_mix + span_mix
                    for _ in range(12):
                        midpoint = (lo + hi) / 2.0
                        if apart(door, draw("bisect.png", midpoint, rest_tilt)) < DOOR_BAR:
                            lo = midpoint
                        else:
                            hi = midpoint
                    granted = lo - door_mix
                    at_peak = draw("peak.png", door_mix + granted, rest_tilt)
                    d_peak = apart(door, at_peak)

                    # THE CEILING criterion 1 names, drawn on the same letter: a thirty-second of the
                    # declared travel.
                    ceiling = span_mix / 32
                    d_ceiling = apart(door, draw("ceiling.png", door_mix + ceiling, rest_tilt))

                    print("\nthe run's own numbers, on a %d x %d frame:" % (VW, VH))
                    print("  the charter's door bar, read out of pass-inst-unfold.js: %.1f of 255"
                          % DOOR_BAR)
                    print("  the hinge walked end to end at the resting pose: %.3f and %.3f of 255"
                          % (hinge_lo, hinge_hi))
                    print("  the travel the making axis is granted at rest: %.6f of a declared %.4f,"
                          " its frame standing %.3f of 255 from the work"
                          % (granted, span_mix, d_peak))
                    print("  criterion 1's own ceiling on that letter, a thirty-second of %.4f"
                          " = %.6f: %.3f of 255 from the work" % (span_mix, ceiling, d_ceiling))

                    check(ROWS[5],
                          hinge_lo == 0.0 and hinge_hi == 0.0
                          and granted > 0
                          and granted <= ceiling
                          and d_peak < DOOR_BAR
                          and d_peak > 0,
                          f"the hinge moves {hinge_lo:.3f} and {hinge_hi:.3f} of 255 end to end at "
                          f"the door; the making axis is granted {granted:.6f} of a declared "
                          f"{span_mix} travel, under criterion 1's ceiling of {ceiling:.6f}, and "
                          f"its frame stands {d_peak:.3f} of 255 from the work, the bar being "
                          f"{DOOR_BAR}")

                    check(ROWS[6],
                          d_ceiling >= DOOR_BAR,
                          f"the same letter walked to criterion 1's own ceiling stands "
                          f"{d_ceiling:.3f} of 255 from the work, the bar being {DOOR_BAR}")

                    errs = json.loads(br.evaluate("JSON.stringify(window.__errs||[])"))
                    if errs:
                        print("  the bench reported: %r" % (errs,))
    finally:
        shutil.rmtree(DRAW_TMP, ignore_errors=True)
        shutil.rmtree(BENCH, ignore_errors=True)
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
