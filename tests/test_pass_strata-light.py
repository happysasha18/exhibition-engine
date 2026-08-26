#!/usr/bin/env python3
"""PASS-API-V1 — the parting-by-light instrument on the host's frame.
Run: python3 tests/test_pass_strata-light.py

Root: his word of 2026-08-18 18:39 — every effect the lab holds belongs in the engine's arsenal,
with all its handles. This file makes real §7 (GPU and resources), §8 (the manifest) and §9's
conformance rows for `strata-light`, the lab module that parts a work along its own light.

WHAT IS COMPARED, AND AGAINST WHAT.

  The doors. At the dial's two ends one whole work stands, and each is measured against ITS OWN
  FILE — the picture cover-fitted into the frame, with no crop, which is the module's own framing
  (lab/data/module-contract.json, this module's `dial.framing`) — inside the project's seam
  threshold of 6 of 255. The doors are measured with BOTH accompanying voices singing loudly, since
  the module's own law is that the window 4u(1 − u) holds them to nothing at either end whatever a
  score gives them.

  The two roads. The lab module holds ONE work and its dial runs to an EMPTY frame; this instrument
  holds a PAIR and its dial runs from one whole work to the other. So the two roads share exactly
  one picture — the ENTRY DOOR, where both stand the departing work whole — and that door is
  compared PIXEL FOR PIXEL. Away from it the roads draw different pictures by construction, and
  what is compared there is what both roads COMPUTE: the response curve and both accompanying
  voices, read off the module's own `reading()` against the instrument's own `values()`, at five
  poses. Two roads of one number, never two guesses at one.

  The cell. The module reads a mask cell as the mean of the file's pixels inside it; this
  instrument reads the cell at its own centre, because a shader cannot average a cell in one fetch.
  That departure is MEASURED here rather than assumed — the share of cells the two readings put on
  the same side of the level is printed on both photographs.

  The lab tree is READ ONLY and is found at $TLVPHOTOS_LAB_ROOT, defaulting to the immersive
  worktree's lab. Absent, every browser row here is a pinned SKIP that names the missing path —
  never a silent pass.
"""
import base64
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
import engine_build as build_site  # noqa: E402
from headless import serve, Browser, chrome_available  # noqa: E402

LAB = Path(os.environ.get("TLVPHOTOS_LAB_ROOT", "/Users/sashaabramovich/tlvphotos-immersive/lab"))
# The two photographs lab/carrier-check.py itself compares on; they live in the main worktree, which
# the immersive one does not copy. Either root is read only here.
PHOTOS = [Path("/Users/sashaabramovich/tlvphotos/lab/photos/towers.jpg"),
          Path("/Users/sashaabramovich/tlvphotos/lab/photos/glassgrid.jpg")]
MODULE = LAB / "effects" / "strata-light.js"

SITE_URL = "https://synth.example.com"
VW, VH = 390, 844          # the phone frame lab/carrier-check.py measures on
CLOCK = 7.0                # the second the comparison holds at, as the carrier's own check does
SEAM = 6.0                 # the project's seam threshold, 6 of 255 (TRANSITION-STAGE-V0 §1)
SAME = 1.5                 # two roads of one frame: the carrier check's own bar
FAR = 40.0                 # further than this from a file and it is a different work
# A frame that stands as a picture. The canvas's own background is one flat colour, so a drawn frame
# is far from it and carries a spread of its own. Both numbers are read off the capture.
BACKGROUND = (0x08, 0x08, 0x0a)
SPREAD = 10.0
# Two numbers that come out of one and the same arithmetic on two roads agree to the last digit a
# double carries; this is the room left for the two roads having reached it through a JSON round
# trip rather than for the arithmetic differing.
EXACT = 1e-9

# Captures are kept rather than swept, because §9 row 16 asks for evidence for every landed
# instrument and evidence that is deleted is no evidence.
SHOTS = ROOT / "tests" / "captures" / "pass-strata-light"

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


# ---------------------------------------------------------------- the score this instrument plays
# AUTHORED HERE, and said to be authored here. lab/data/scores carries no per-pair score for this
# module, so everything below is either a number the module itself declares, a number the module's
# own `measure(image)` solves for a file, or a number this file chose and names as its own.
DURATION_MS = 3000
WITHIN_MS = 500

# THE VOICES, AUTHORED. The two PERIODS of each work are the numbers the lab's own assembler
# produced for the pair it ran on (lab/data/step4-check.txt: `layers[0].params.colourPeriod`
# 0.4732, `lightPeriod` 0.7478, `layers[1].params.colourPeriod` 1.05687, `lightPeriod` 1.66947) and
# the four PHASES are the assembler's own rule, «голоса стоят по четверти оборота врозь» — the four
# quarters of a turn. The two AMPLITUDES are THIS FILE'S OWN and are named as such under «Numbers to
# revisit»: the assembler solves each amplitude by measuring the voice on the real photograph, which
# is a measurement this file does not take, and the numbers here are raised so that moving one voice
# handle alone is visible on a screenshot at all.
VOICES = {"colourPeriodA": 0.4732, "colourPhaseA": 0.0, "colourAmpA": 0.35,
          "lightPeriodA": 0.7478, "lightPhaseA": 0.25, "lightAmpA": 0.30,
          "colourPeriodB": 1.05687, "colourPhaseB": 0.5, "colourAmpB": 0.35,
          "lightPeriodB": 1.66947, "lightPhaseB": 0.75, "lightAmpB": 0.30}

# The nineteen handles the manifest publishes.
HANDLES = ["mix", "clock", "levelA", "levelB", "cellsA", "cellsB",
           "colourPeriodA", "colourPhaseA", "colourAmpA",
           "lightPeriodA", "lightPhaseA", "lightAmpA",
           "colourPeriodB", "colourPhaseB", "colourAmpB",
           "lightPeriodB", "lightPhaseB", "lightAmpB", "mask", "presence"]


def strata_score(level_a=0.5, level_b=0.5, pair_a="a", pair_b="b", **statics):
    """The score, with a track for every one of the nineteen handles (§4.4b).

    `mix` reads the transaction's own progress and `clock` the second the host hands down. The two
    levels are the MODULE'S OWN `measure(image)` of the two files, read off the lab module running
    on the same page — the very number the module publishes for a score to carry. The two cell
    counts rest at the module's own MASK_CELLS of 128.
    """
    P = {"levelA": level_a, "levelB": level_b, "cellsA": 128, "cellsB": 128, "mask": 0}
    P.update(VOICES)
    P.update(statics)
    nodes = {"mixDrive": {"source": "progress"}, "clockDrive": {"source": "time"}}
    tracks = {"mix": {"node": "mixDrive"}, "clock": {"node": "clockDrive"}}
    for k, v in P.items():
        nodes[k + "Static"] = {"op": "static", "value": v}
        tracks[k] = {"node": k + "Static"}
    res = {v: {"textures": 0, "textureSlots": 2, "framebuffers": 0, "pingPong": 0, "programs": 1,
               "passes": 1, "bytesEstimate": 0, "variant": v}
           for v in ("lean", "standard", "rich")}
    return {
        "schema": 2,
        "intent": "the departing work parts along its own light — its bright half up out of the "
                  "frame and its dark half down — while the arriving work's two halves come in the "
                  "opposite way and close on each other (lab/effects/strata-light.js:1-10, its own "
                  "header)",
        "pair": {"a": pair_a, "b": pair_b},
        "seed": 0,
        "duration": DURATION_MS,
        "direction": "a-to-b",
        "interruption": {"withinMs": WITHIN_MS, "resolve": "nearest-door"},
        "failLand": "arrive",
        "camera": {"owner": "stage", "rests": "b",
                   "track": [{"at": "b", "pan": {"x": 0, "y": 0}, "logScale": 0,
                              "pitch": 0, "yaw": 0, "roll": 0, "fov": None, "owner": "stage"}]},
        "cues": [{
            "id": "strata-light-main",
            "instrument": {"id": "strata-light", "api": 1},
            "voice": "letter",
            "roles": ["disassembly", "mystery", "assembly"],
            "levels": ["CELL"],
            "window": [0, DURATION_MS / 1000.0],
            "works": ["a", "b"],
            "stack": 0,
            "cameraAuthority": "stage",
            "doors": {"in": {"handle": "mix", "value": 0, "measured": True},
                      "out": {"handle": "mix", "value": 1, "measured": True}},
            "nodes": nodes,
            "tracks": tracks,
            "resources": res["standard"],
        }],
        "quality": {v: {"renderScale": None, "cues": {"strata-light-main": {"resources": res[v]}}}
                    for v in ("lean", "standard", "rich")},
        "provenance": {"source": "lab/effects/strata-light.js's own declared defaults and "
                                 "constants, its own measure(image), and the voice numbers this "
                                 "suite authors",
                       "measuredAt": None, "by": "tests/test_pass_strata-light.py"},
    }


# ---------------------------------------------------------------- bake once
build_site.SITE_CONFIG = dict(build_site.SITE_CONFIG)
build_site.SITE_CONFIG["pass"] = {"visualLayer": "pass", "diagnostics": "on"}

TMP = Path(tempfile.mkdtemp(prefix="synth_passstrata_"))
build_site.OUT = TMP
build_site.build(SITE_URL)
LAYER = (TMP / "pass-layer.js").read_text(encoding="utf-8")
# The instrument's own region of the BUILT file — the real artifact, comments stripped as it ships.
REGION = (TMP / "pass-inst-strata-light.js").read_text(encoding="utf-8")

# ---------------------------------------------------------------- string rows

OWNED = ["createElement", "getContext", "requestAnimationFrame", "addEventListener",
         "performance.now", "Date.now", "new Image", "setTimeout", "setInterval"]
held = [s for s in OWNED if s in REGION]
check("PASS-STRATA the instrument creates no context, no canvas, no loop and no listener",
      not held,
      "§1.2's fence, read against the instrument's own region of the file: none of the nine ways of "
      "owning hardware appears there, so the module's visible canvas, its six 2D contexts, its "
      "offscreen piece canvases and its grey twin all stayed in the lab"
      if not held else "the instrument's region holds " + ", ".join(held))

missing_h = [h for h in HANDLES if ("%s: { min" % h) not in REGION]
check("PASS-STRATA every handle the instrument publishes is a handle a score can drive",
      not missing_h,
      "§4.4b: nineteen handles — the dial, the handed second, a level and a mask grid per work, the "
      "module's six voice fields per work, and the judges' own channel"
      if not missing_h else "these are not published: " + ", ".join(missing_h))

check("PASS-STRATA nothing in the instrument reads a clock, which is the module's own law",
      "t: h.clock" in REGION and not re.search(r"st\.t\b", REGION) and "reduced" in REGION,
      "every position in this module is a pure function of the dial (strata-light.js:364-367), so "
      "the handed second reaches the pose and moves nothing; the handle is published because the "
      "module accepts one and a score owns the clock everywhere")

check("PASS-STRATA the manifest leaves the drawing buffer unpreserved",
      "gl: { preserveDrawingBuffer: false }" in REGION,
      "§7 refuses a manifest that asks for a preserved buffer; the redraw it would stand in for is "
      "the host's own frame loop")

LABTXT = MODULE.read_text(encoding="utf-8") if MODULE.exists() else ""
check("PASS-STRATA the shader carries no version header of its own",
      "#version" not in REGION and (not LABTXT or "#version" not in LABTXT),
      "so the host's translator stamps the one header this shader needs and no second one arrives")

# The response curve and the voice law, read out of the lab module and out of the built file. A port
# that re-derived either would differ here by a digit.
CURVE = [("var FEEL_C = 0.37, FEEL_K1 = -0.2, FEEL_K2 = 2.2;",
          "var FEEL_C = 0.37, FEEL_K1 = -0.2, FEEL_K2 = 2.2;",
          "the measured median of the felt change and the two fitted exponents"),
         ("return Math.abs(k) < 1e-6 ? x : (Math.exp(k * x) - 1) / (Math.exp(k) - 1);",
          "return Math.abs(k) < 1e-6 ? x : (Math.exp(k * x) - 1) / (Math.exp(k) - 1);",
          "the plain logarithm each side of the knee is"),
         ("return u <= 0.5 ? FEEL_C * feelLog(2 * u, FEEL_K1)",
          "return u <= 0.5 ? FEEL_C * feelLog(2 * u, FEEL_K1)",
          "and the hinge itself")]
off_curve = ([c for c, _, _ in CURVE if LABTXT and c not in LABTXT]
             + [c for _, c, _ in CURVE if c not in REGION])
check("PASS-STRATA the response curve is carried digit for digit out of the lab module",
      not off_curve,
      "; ".join("%s — %s" % (why, c) for c, _, why in CURVE) if not off_curve
      else "these differ: " + "; ".join(off_curve))

VOICE_LINE = "return a * Math.sin(2 * Math.PI * (u / p + (+phase || 0))) * 4 * u * (1 - u);"
check("PASS-STRATA both accompanying voices carry the module's own law, window and all",
      (not LABTXT or VOICE_LINE in LABTXT) and VOICE_LINE in REGION
      and "if (!(a > 0) || !(p > 0)) return 0;" in REGION,
      "one breath of a named period and a named phase, held to nothing at BOTH doors by the window "
      "4u(1 − u), and silent whenever the period or the amplitude is not positive — the very line "
      "the module carries (strata-light.js:288-291), and the line this instrument's own door "
      "reading is held against")

CONSTANTS = [("var MASK_CELLS = 128", "MASK_CELLS = 128",
              "the mask grid the module measures on, cells across the long side"),
             ("Math.min(0.9, Math.abs(v))", "LIGHT_CEILING = 0.9",
              "the module's own ceiling on the light voice"),
             ("0.2126 * d[i * 4] + 0.7152", "vec3(0.2126, 0.7152, 0.0722)",
              "the three weights the module reads luminance with")]
off_const = ([c for c, _, _ in CONSTANTS if LABTXT and c not in LABTXT]
             + [c for _, c, _ in CONSTANTS if c not in REGION])
check("PASS-STRATA every constant of the cut stands at the number the lab module gives it",
      not off_const,
      "; ".join("%s — %s" % (c, why) for _, c, why in CONSTANTS) if not off_const
      else "these differ: " + "; ".join(off_const))

declared = set(re.findall(r'\{ name: "(u\w+)", type:', REGION))
spelled = set(re.findall(r'uniform \w+ (u\w+);', REGION))
check("PASS-STRATA the manifest's declared names and the shader's own names are one set",
      declared == spelled and len(declared) == 12,
      f"{len(declared)} declared, {len(spelled)} spelled; "
      f"declared only: {sorted(declared - spelled)}; spelled only: {sorted(spelled - declared)}")

# WHAT THE INSTRUMENT DECLARES ABOUT THE PAIRS IT SUITS. His words of 2026-08-18 09:51, 09:53 and
# 10:15: any two photographs in the world get a crossing, and a measurement only RANKS which genre
# suits. So the row reads that the fit is published, that it names the reading it is taken from, and
# that nothing in this file can turn a pair away on a number.
FLOORS = ["minimum", "threshold", "atLeast", "declineBelow", "qualif", "notEnough"]
found_floor = [w for w in FLOORS if w in REGION]
# «floor» as a word rather than as the rounding both the shader and the script take: a `floor(` is
# arithmetic, a bare `floor` would be a bar a pair has to clear.
if re.search(r"\bfloor\b(?!\s*\()", REGION):
    found_floor.append("floor")
check("PASS-STRATA the cut and the fit are published, and the fit only ranks",
      'cuts: ["band"]' in REGION
      and 'suits: { reads: ["luminance.level"]' in REGION
      and "how:" in REGION and not found_floor
      and 'decline: ["one work only", "a source that never decoded"]' in REGION,
      "it cuts on the tonal zones — the band kind, which is what the composer's own "
      "tonal-and-spectral pivot cuts on — and it reads how far apart the two works stand on their "
      "own measured tone, `luminance.level` (the judge seat's standing correction of "
      "2026-08-18/19, moved off `palette.colourfulness` which reads the collection's own "
      "colourfulness ladder and never was a tone); the two things it declines are a half pair and "
      "a picture that never decoded, and no reading anywhere in the file can make a pair not "
      "qualify"
      if not found_floor else "the file carries a floor: " + ", ".join(found_floor))

# ---------------------------------------------------------------- browser rows

BROWSER_ROWS = [
    "PASS-STRATA §8     · the manifest carries every field the contract names, in its shape",
    "PASS-STRATA row 7  · door 0 stands the departing work, measured against its own file",
    "PASS-STRATA row 7  · door 0 carries no trace of the arriving work",
    "PASS-STRATA row 7  · door 1 stands the arriving work, measured against its own file",
    "PASS-STRATA row 7  · door 1 carries no trace of the departing work",
    "PASS-STRATA the two roads draw one and the same entry door, pixel for pixel",
    "PASS-STRATA the two roads agree on the response curve and on both voices, at five poses",
    "PASS-STRATA both doors are the file itself however loudly the two voices are told to sing",
    "PASS-STRATA nothing is ever faded: the coverage this instrument writes is 0 or 1 and never between",
    "PASS-STRATA §7     · no empty frame at any sampled instant of the pass",
    "PASS-STRATA §7     · the frame after a change of viewport is drawn, not a kept buffer",
    "PASS-STRATA row 10 · a seeded run repeats to the pixel",
    "PASS-STRATA row 14 · textures, programmes and framebuffers return to their baseline after ten runs",
    "PASS-STRATA row 15 · the console stays clean",
    "PASS-STRATA row 22 · the census shows granted against declared, and neither overruns",
    "PASS-STRATA §7     · a manifest asking for a preserved drawing buffer is refused, with its reason",
    "PASS-STRATA §7     · a uniform bound to a name the shader lacks is refused, with its reason",
    "PASS-STRATA §7     · one canvas, one context, two source textures, one pass a frame",
    "PASS-STRATA §7     · a shader already at GLSL ES 3.00 receives no second version header",
    "PASS-STRATA the real transaction road: curtain up, one pass drawn, exactly one dock at the end",
    "PASS-STRATA row 9  · one camera authority through a real pass, and the pose rests on the arrival",
    "PASS-STRATA §4.4b  · every handle but the handed second reaches the PICTURE",
    "PASS-STRATA the door is read on the DRAWING BUFFER, and the state applied is published",
    "PASS-STRATA the cell read at its centre against the module's own mean, measured on both files",
    "PASS-STRATA row 16 · the captures are kept as evidence",
]

RED_ROWS = [
    "PASS-STRATA red-on-bug · the voice's window removed: a door carries a breath the file does not",
]

missing = [str(p) for p in ([MODULE] + PHOTOS) if not p.exists()]


def png(br, path):
    d = br._cmd("Page.captureScreenshot", format="png", captureBeyondViewport=False)
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_bytes(base64.b64decode(d["data"]))
    return path


def diff(p, q):
    from PIL import Image, ImageChops, ImageStat
    a = Image.open(p).convert("RGB")
    c = Image.open(q).convert("RGB")
    if a.size != c.size:
        return 255.0, 255.0
    st = ImageStat.Stat(ImageChops.difference(a, c))
    return sum(st.mean) / 3.0, max(m for _, m in st.extrema)


def standing(p):
    """How far a capture stands from the canvas's own flat background, and how much spread it
    carries of its own. A frame that was never drawn is the background and has neither."""
    from PIL import Image, ImageChops, ImageStat
    a = Image.open(p).convert("RGB")
    flat = Image.new("RGB", a.size, BACKGROUND)
    st = ImageStat.Stat(ImageChops.difference(a, flat))
    own = ImageStat.Stat(a)
    return sum(st.mean) / 3.0, sum(own.stddev) / 3.0


def work_in_the_frame(src, w, h, zoom):
    """The work as the instrument seats it: cover-fit, then the centre crop the framing names — and
    this module's own framing names none, so `zoom` is 1 and the picture is the plain cover fit."""
    from PIL import Image
    im = Image.open(src).convert("RGB")
    iw, ih = im.size
    fa, ia = w / float(h), iw / float(ih)
    sw, sh = (ih * fa, float(ih)) if ia > fa else (float(iw), iw / fa)
    sw /= zoom
    sh /= zoom
    x0, y0 = (iw - sw) / 2.0, (ih - sh) / 2.0
    return im.resize((w, h), Image.BILINEAR, box=(x0, y0, x0 + sw, y0 + sh))


def chroma(p):
    """How much colour a capture carries, in channels of 255: the mean distance of its own points
    from grey. It is what a SATURATION voice moves, and it is the measure that voice is weighed on
    where the plain channel distance of a near-grey photograph cannot say much."""
    from PIL import Image, ImageChops, ImageStat
    a = Image.open(p).convert("RGB")
    grey = a.convert("L").convert("RGB")
    return sum(ImageStat.Stat(ImageChops.difference(a, grey)).mean) / 3.0


def apart(p, work):
    from PIL import Image, ImageChops, ImageStat
    a = Image.open(p).convert("RGB")
    if a.size != work.size:
        return 255.0, 255.0
    st = ImageStat.Stat(ImageChops.difference(a, work))
    return sum(st.mean) / 3.0, max(m for _, m in st.extrema)


def bench_dir(pack_text=None):
    """The bench's own served root: the BUILT pass-layer.js (the real artifact, namespace applied
    and comments stripped), every built instrument file, the site's own settings record, the lab
    module unchanged, the two photographs, and the page that stands the two roads side by side.

    A row proving a rule reds hands over a CHANGED instrument file and writes the record with the
    digest of the bytes actually served, which is what the build does. The source file on disk is
    never touched, so no working tree can be left changed by a red-on-bug proof."""
    d = Path(tempfile.mkdtemp(prefix="synth_stratabench_"))
    pack = REGION if pack_text is None else pack_text
    shutil.copy2(TMP / "pass-layer.js", d / "pass-layer.js")
    for _inst in sorted(TMP.glob("pass-inst-*.js")):
        shutil.copy2(_inst, d / _inst.name)
    (d / "pass-inst-strata-light.js").write_text(pack, encoding="utf-8")
    record = json.loads((TMP / "config.json").read_text(encoding="utf-8"))
    record["pass"]["instruments"]["strata-light"]["digest"] = hashlib.sha256(
        pack.encode("utf-8")).hexdigest()
    (d / "config.json").write_text(json.dumps(record), encoding="utf-8")
    shutil.copy2(MODULE, d / "strata-light.js")
    (d / "photos").mkdir()
    for p in PHOTOS:
        shutil.copy2(p, d / "photos" / p.name)
    shutil.copy2(ROOT / "tests" / "fixture_pass_strata-light.html", d / "index.html")
    return d


def ready(br, tries=60):
    for _ in range(tries):
        if br.evaluate("String(!!window.__ready)") == "true":
            return True
        br.sleep(0.25)
    return False


def js(br, expr):
    return json.loads(br.evaluate("JSON.stringify((function(){%s})())" % expr))


def idle(br, tries=60, nap=0.1):
    for _ in range(tries):
        if js(br, "return window.__report().state;") == "idle":
            return True
        br.sleep(nap)
    return False


def on_bench(fn, pack_text=None):
    """One reading, taken on a bench of its own: a served root, a fresh browser, and the instrument
    file this call names. Held apart so a red-on-bug proof and the run it is compared against differ
    in exactly one thing — the bytes the host was handed."""
    d = bench_dir(pack_text)
    try:
        with serve(d) as base:
            with Browser(width=VW, height=VH) as br:
                br.navigate(base + "/index.html")
                if not ready(br):
                    return None
                return fn(br)
    finally:
        shutil.rmtree(d, ignore_errors=True)


if not chrome_available():
    for r in BROWSER_ROWS + RED_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
elif missing:
    for r in BROWSER_ROWS + RED_ROWS:
        skip(r, "the lab tree is read-only source material and is absent here: " + missing[0])
else:
    shutil.rmtree(SHOTS, ignore_errors=True)
    SHOTS.mkdir(parents=True, exist_ok=True)
    BENCH = bench_dir()
    with serve(BENCH) as base:
        with Browser(width=VW, height=VH) as br:
            br.navigate(base + "/index.html")
            if not ready(br):
                for r in BROWSER_ROWS:
                    skip(r, "the bench never came up: "
                         + br.evaluate("JSON.stringify(window.__errs||[])"))
            elif not js(br, "return !!window.__exPass.bench.manifest('strata-light');"):
                why = js(br, "var e = window.__host.report().events.filter(function(x){"
                             "return x.name === 'manifest-refused';});"
                             "return e.length ? e[e.length - 1].why : null;")
                for r in BROWSER_ROWS:
                    check(r, False, "the host registered no «strata-light» instrument: " + str(why))
            else:
                # THE TWO LEVELS, READ OFF THE MODULE'S OWN MEASUREMENT. `measure(image)` is the
                # module's own published number and the one a score is meant to carry, so every
                # score below parts each work at exactly the level the module solves for it.
                LEVEL = js(br, "return window.__level();")
                SCORE_JSON = json.dumps(strata_score(LEVEL["a"], LEVEL["b"]))

                # ---- §8: the manifest, read off the registered instrument -----------------------
                m = js(br, "return window.__exPass.bench.manifest('strata-light');")
                res = m["resources"]
                shape = (
                    m["id"] == "strata-light" and m["api"] == 1 and m["arity"] == 2
                    and m["roles"] == ["disassembly", "mystery", "assembly"]
                    # LIGHT-COLOUR joined CELL on 2026-08-18 (pass-inst-strata-light.js:403):
                    # shelf 17's levels law, once the colour and light voices are actually driven
                    # (pass-composer.js's "strata-light" branch of `fillPlan`) rather than resting
                    # unmeasured at every pair, gives that level one active voice and this manifest
                    # has to say it occupies it or the composer's own level-ownership resolution
                    # would never see a second cue that also claims it.
                    and m["levels"] == ["CELL", "LIGHT-COLOUR"] and m["cuts"] == ["band"]
                    and m["params"] == {}
                    and len(m["handles"]) == 20
                    and all(set(h) >= {"min", "max", "def"} for h in m["handles"].values())
                    and sorted(m["handles"]) == sorted(HANDLES)
                    and m["neutrals"] == {"a": 0, "b": 1}
                    and m["doors"]["in"]["handle"] == "mix" and m["doors"]["in"]["value"] == 0
                    and m["doors"]["out"]["handle"] == "mix" and m["doors"]["out"]["value"] == 1
                    and sorted(m["framings"]) == ["0", "1"]
                    and m["framings"]["0"] == m["framings"]["1"] == {"coverCrop": 1.0}
                    and m["camera"] == {"needs": "none", "authority": "stage"}
                    and m["coverage"]["writes"] is True
                    and len(m["passes"]) == 1 and len(m["passes"][0]["uniforms"]) == 12
                    and sorted(res) == ["lean", "rich", "standard"]
                    and all("bytesEstimate" in res[v] and res[v]["programs"] == 1
                            and res[v]["passes"] == 1 and res[v]["textureSlots"] == 2
                            for v in res)
                    and m["capabilities"] == ["webgl2"] and m["decline"]
                    and m["suits"]["reads"] == ["luminance.level"] and m["suits"]["how"]
                    and m["provenance"]["labPath"] == "lab/effects/strata-light.js"
                    and m["provenance"]["commit"] == "468f491"
                    and m["readiness"] == "production-ready"
                    and "strata-light" in js(br, "return window.__host.report().registered;"))
                check(BROWSER_ROWS[0], shape,
                      f"nineteen handles, eleven uniforms in one pass, the plain cover fit "
                      f"{m['framings']['0']} the module's own framing names, the band cut, the "
                      f"tonal fit, resources declared for three tiers, and the lab commit "
                      f"{m['provenance']['commit']}; the module declares no slider-facing param at "
                      f"all and the manifest carries that empty list rather than filling it")

                br.evaluate("window.__clock(%r); 0" % CLOCK)
                br.sleep(0.6)

                # ---- the doors, with BOTH voices singing --------------------------------------
                # The module's own law is that the window 4u(1 − u) holds every voice to nothing at
                # either end of the dial whatever a score gives it, so the doors are measured with
                # the voices at their loudest rather than at rest — which is the harder question.
                br.evaluate("window.__show('host'); 0")
                shots = {}
                for name, v in (("door-0", 0.0), ("door-1", 1.0)):
                    br.evaluate("window.__part(%r); 0" % v)
                    br.sleep(0.2)
                    js(br, "return window.__hostDraw(%s);" % json.dumps(VOICES))
                    br.sleep(0.2)
                    shots[name] = png(br, SHOTS / (name + "-host.png"))

                w = int(br.evaluate("String(document.querySelector('canvas').width)"))
                h = int(br.evaluate("String(document.querySelector('canvas').height)"))
                towers = work_in_the_frame(BENCH / "photos" / "towers.jpg", w, h, 1.0)
                glass = work_in_the_frame(BENCH / "photos" / "glassgrid.jpg", w, h, 1.0)

                voiced = []
                for i, (door, own, other, ownn, othern) in enumerate((
                        ("door-0", towers, glass, "towers.jpg", "glassgrid.jpg"),
                        ("door-1", glass, towers, "glassgrid.jpg", "towers.jpg"))):
                    a, amx = apart(shots[door], own)
                    voiced.append((door, a))
                    check(BROWSER_ROWS[1 + i * 2], a <= SEAM,
                          f"{door} against {ownn}, with both voices at full amplitude: mean "
                          f"{a:.4f} of 255 (threshold {SEAM}), worst channel {amx}")
                    o, _ = apart(shots[door], other)
                    check(BROWSER_ROWS[2 + i * 2], o >= FAR,
                          f"{door} against {othern}: mean {o:.4f} of 255 (must exceed {FAR})")
                check(BROWSER_ROWS[7], all(a <= SEAM for _, a in voiced),
                      "; ".join(f"{d}: {a:.4f} of 255 from its own file" for d, a in voiced)
                      + f" (threshold {SEAM}) — every one of the four voice fields of both works "
                      f"was at its full amplitude for these two captures, and the window 4u(1 − u) "
                      f"is exactly zero at both ends of the dial, so a door is exactly the picture "
                      f"the file carries")

                # ---- the two roads at the entry door, pixel for pixel --------------------------
                # The module holds ONE work and the instrument holds a PAIR, so the two roads share
                # exactly one picture: the entry door, where both stand the departing work whole.
                br.evaluate("window.__part(0); 0")
                br.sleep(0.3)
                js(br, "return window.__hostDraw();")
                br.sleep(0.2)
                br.evaluate("window.__show('host'); 0")
                br.sleep(0.25)
                ph = png(br, SHOTS / "roads-host.png")
                br.evaluate("window.__show('module'); 0")
                br.sleep(0.25)
                pm = png(br, SHOTS / "roads-module.png")
                rmn, rmx = diff(ph, pm)
                check(BROWSER_ROWS[5], rmn <= SAME,
                      f"the host's entry door beside the lab module at its own dial 0: mean "
                      f"{rmn:.4f} of 255 (threshold {SAME}), worst channel {rmx}. Away from this "
                      f"door the two roads draw different pictures by construction — the module "
                      f"parts one work into an empty frame, this instrument parts a pair into each "
                      f"other — so what the next row compares there is what both roads COMPUTE")

                # ---- the two roads on the numbers, at five poses ------------------------------
                # The module's own `reading()` publishes `light` and `colourVoice` at its own dial,
                # which is the raw hand through the module's own response curve. The instrument's
                # own `values()` publishes the same two for the departing work. Both roads are
                # driven by one and the same set of voice numbers, so the two must agree to the last
                # digit — and agreeing proves the response curve AND the voice law crossed whole.
                for k, v in (("colourPeriod", VOICES["colourPeriodA"]),
                             ("colourPhase", VOICES["colourPhaseA"]),
                             ("colourAmp", VOICES["colourAmpA"]),
                             ("lightPeriod", VOICES["lightPeriodA"]),
                             ("lightPhase", VOICES["lightPhaseA"]),
                             ("lightAmp", VOICES["lightAmpA"])):
                    br.evaluate("window.__param(%s, %r); 0" % (json.dumps(k), v))
                br.sleep(0.2)
                agree = []
                for u in (0.0, 0.25, 0.5, 0.75, 1.0):
                    br.evaluate("window.__part(%r); 0" % u)
                    br.sleep(0.1)
                    lab = js(br, "return window.__reading();")
                    port = js(br, "return window.__hostValues(%s);"
                              % json.dumps(dict(VOICES, mix=u)))
                    agree.append((u, abs(lab["colourVoice"] - port["colourVoice"][0]),
                                  abs(lab["light"] - port["lightVoice"][0]),
                                  lab["colourVoice"], lab["light"]))
                check(BROWSER_ROWS[6], all(c <= EXACT and l <= EXACT for _, c, l, _, _ in agree),
                      "; ".join(f"at {u}: the module says colour {cv:.6f} light {lv:.6f}, the "
                                f"instrument differs by {c:.3e} and {l:.3e}"
                                for u, c, l, cv, lv in agree)
                      + f" (both must stand inside {EXACT}) — one and the same response curve and "
                      f"one and the same voice law, computed twice")

                # ---- nothing is ever faded ---------------------------------------------------
                # The judges' `mask` channel writes each work's own coverage as colour, so this row
                # reads on the PICTURE whether the alpha this instrument writes is ever anything but
                # wholly off or wholly on. The module's own law: alpha inside a piece is 1 and
                # outside it 0, never anything in between.
                br.evaluate("window.__show('host'); 0")
                fades = []
                for u in (0.15, 0.35, 0.5, 0.7, 0.9):
                    fades.append((u, js(br, "return window.__drawAndRead(%s);"
                                        % json.dumps(dict(VOICES, mix=u, mask=1)))))
                br.sleep(0.2)
                png(br, SHOTS / "mask-mid.png")
                # A capture's own edges are resampled by the screenshot, so the reading is taken
                # from the canvas itself rather than from a picture of it.
                worst = max(f["between"] / float(f["points"]) for _, f in fades)
                check(BROWSER_ROWS[8], worst == 0.0,
                      "; ".join(f"at {u}: {f['red']} points claimed by the departing work, "
                                f"{f['green']} by the arriving one, {f['none']} by neither, and "
                                f"{f['between']} standing between"
                                for u, f in fades)
                      + " — every point of every frame is wholly claimed or wholly clear, which is "
                        "the module's own «no fade» read on the picture")

                # ---- §7: no empty frame, and the redraw the preserved buffer stood in for -------
                empties = []
                for at in (0.0, 0.15, 0.3, 0.5, 0.7, 0.85, 1.0):
                    js(br, "return window.__offer(%s, {clock: 1.5, progress: %r});"
                       % (SCORE_JSON, at))
                    br.sleep(0.5)
                    p = png(br, SHOTS / ("instant-%03d.png" % round(at * 100)))
                    empties.append((at, ) + standing(p))
                    br.evaluate("window.__cancel('instant sweep'); 0")
                    idle(br)
                check(BROWSER_ROWS[9],
                      all(d >= FAR and s >= SPREAD for _, d, s in empties),
                      "; ".join(f"at {at}: {d:.2f} from the background, spread {s:.2f}"
                                for at, d, s in empties)
                      + f" (bars: {FAR} and {SPREAD}). Between the doors this instrument publishes "
                      f"an ABSENCE where neither work's matter has reached, which a stack fills "
                      f"from beneath; here it plays alone, so that absence is the cleared buffer "
                      f"and the frame still has to stand as a picture")

                js(br, "return window.__offer(%s, {clock: 1.5, progress: 0.5});" % SCORE_JSON)
                br.sleep(0.5)
                br.set_viewport(VW - 80, VH - 120)
                br.sleep(0.6)
                p = png(br, SHOTS / "after-resize.png")
                sized = js(br, "return {w: document.querySelector('canvas').width, "
                               "buffer: window.__report().census.buffer, "
                               "pdb: window.__report().census.preserveDrawingBuffer};")
                d, s = standing(p)
                br.evaluate("window.__cancel('resize row'); 0")
                idle(br)
                br.set_viewport(VW, VH)
                br.sleep(0.4)
                check(BROWSER_ROWS[10],
                      d >= FAR and s >= SPREAD and sized["pdb"] is False,
                      f"after the viewport moved to {VW - 80}x{VH - 120} the buffer reads "
                      f"{sized['buffer']} and the frame stands {d:.2f} from the background with a "
                      f"spread of {s:.2f}; the context keeps preserveDrawingBuffer={sized['pdb']}")

                # ---- the seeded repeat -----------------------------------------------------------
                took = js(br, "return window.__offer(%s, {clock: 1.5, progress: 0.5});" % SCORE_JSON)
                br.sleep(0.9)
                first = png(br, SHOTS / "seeded-1.png")
                rep1 = js(br, "return window.__report();")
                br.evaluate("window.__cancel('between runs'); 0")
                idle(br)
                js(br, "return window.__offer(%s, {clock: 1.5, progress: 0.5});" % SCORE_JSON)
                br.sleep(0.9)
                second = png(br, SHOTS / "seeded-2.png")
                mn, mx = diff(first, second)
                check(BROWSER_ROWS[11], took["took"] and mn == 0.0 and mx == 0,
                      f"took={took['took']} two runs of one score: mean {mn} worst channel {mx}. "
                      f"There is no die in this module and no clock reaches its picture, so a "
                      f"repeat is exact by construction rather than by a seed being honoured")

                # ---- ten runs, and the baseline --------------------------------------------------
                base_c = rep1["census"]
                for _ in range(10):
                    js(br, "return window.__offer(%s, {clock: 2.0, progress: 0.3});" % SCORE_JSON)
                    br.sleep(0.12)
                    br.evaluate("window.__cancel('leak row'); 0")
                br.sleep(0.4)
                after = js(br, "return window.__report();")["census"]
                same = (after["textures"] == base_c["textures"] == 2
                        and after["programs"] == base_c["programs"]
                        and after["framebuffers"] == base_c["framebuffers"] == 0
                        and after["canvases"] == base_c["canvases"] == 1
                        and after["contexts"] == base_c["contexts"] == 1)
                check(BROWSER_ROWS[12], same,
                      f"before={base_c['textures']}/{base_c['programs']}/{base_c['framebuffers']} "
                      f"after ten runs={after['textures']}/{after['programs']}/{after['framebuffers']} "
                      f"(textures/programmes/framebuffers)")

                errs = json.loads(br.evaluate("JSON.stringify(window.__errs||[])"))
                check(BROWSER_ROWS[13], not errs, "; ".join(errs)[:300])

                r = js(br, "return window.__report();")["resources"]
                check(BROWSER_ROWS[14],
                      r["declared"] and r["over"] is False
                      and r["granted"]["textures"] == r["declared"]["textures"]
                      and r["granted"]["framebuffers"] == r["declared"]["framebuffers"]
                      and r["granted"]["bytes"] == r["declared"]["bytesEstimate"],
                      f"declared={r['declared']} granted={r['granted']}")

                # ---- the two manifest refusals ---------------------------------------------------
                STUB = ("values:function(){return {dial:[0,1],level:[0.5,0.5],cells:[128,128],"
                        "sat:[1,1],light:[0,0],colourVoice:[0,0],lightVoice:[0,0],hand:0,"
                        "doorGrid:null,doorStanding:null,doorWhyNo:null};},"
                        "fit:function(){return [1,1,0,0];},"
                        "prepare:function(){return {take:false};}, start:function(){}, "
                        "frame:function(){}")
                r = js(br, """
                  var m = JSON.parse(JSON.stringify(window.__exPass.bench.manifest('strata-light')));
                  m.gl.preserveDrawingBuffer = true;
                  var ok = window.__exPass.bench.register({name:'strata-preserve', manifest:m, %s});
                  var evs = window.__host.report().events.filter(function(e){return e.name==='manifest-refused';});
                  return {ok: ok, why: evs.length ? evs[evs.length - 1].why : null,
                          registered: window.__host.report().registered};
                """ % STUB)
                check(BROWSER_ROWS[15],
                      r["ok"] is False and r["why"] and "preserved" in r["why"]
                      and "strata-preserve" not in r["registered"],
                      f"registered={r['ok']} why={r['why']}")

                r = js(br, """
                  var m = JSON.parse(JSON.stringify(window.__exPass.bench.manifest('strata-light')));
                  m.passes[0].uniforms.push({name:'uPointer', type:'vec2', source:'pointer'});
                  var ok = window.__exPass.bench.register({name:'strata-pointer', manifest:m, %s});
                  var evs = window.__host.report().events.filter(function(e){return e.name==='manifest-refused';});
                  return {ok: ok, why: evs.length ? evs[evs.length - 1].why : null,
                          registered: window.__host.report().registered};
                """ % STUB)
                check(BROWSER_ROWS[16],
                      r["ok"] is False and r["why"] and "uPointer" in r["why"]
                      and "cannot supply" in r["why"] and "strata-pointer" not in r["registered"],
                      f"registered={r['ok']} why={r['why']}")

                # ---- the hardware, counted where each thing is made ------------------------------
                js(br, "return window.__offer(%s, {clock: 1.0, progress: 0.4});" % SCORE_JSON)
                br.sleep(0.6)
                cen = js(br, "return window.__report();")["census"]
                check(BROWSER_ROWS[17],
                      cen["canvases"] == 1 and cen["contexts"] == 1 and cen["textures"] == 2
                      and cen["passesLastFrame"] == 1 and cen["framebuffers"] == 0
                      and cen["preserveDrawingBuffer"] is False,
                      f"census={cen}; the module's own two canvases, its six 2D contexts and one "
                      f"offscreen canvas per travelling piece all stayed in the lab")

                # ---- the version header, through the host's own translator -----------------------
                r = js(br, """
                  var m = window.__exPass.bench.manifest('strata-light');
                  var plain = window.__exPass.bench.es3(m.passes[0].frag, false);
                  var already = window.__exPass.bench.es3('#version 300 es\\n' + m.passes[0].frag, false);
                  var count = function (s) { return s.split('#version').length - 1; };
                  return {source: count(m.passes[0].frag), stamped: count(plain),
                          untouched: count(already), head: plain.slice(0, 15)};
                """)
                check(BROWSER_ROWS[18],
                      r["source"] == 0 and r["stamped"] == 1 and r["untouched"] == 1
                      and r["head"].startswith("#version 300 es"),
                      f"the module's own shader carries {r['source']} headers, the translator "
                      f"leaves it with {r['stamped']}, and a source that already carries one comes "
                      f"back with {r['untouched']}")

                # ---- curtain up, one pass drawn, exactly one dock --------------------------------
                br.evaluate("window.__cancel('before the whole pass'); 0")
                idle(br, nap=0.05)
                br.evaluate("window.__hooks.docks.length = 0; window.__hooks.curtains.length = 0; 0")
                took = js(br, "return window.__offer(%s, {});" % SCORE_JSON)
                br.sleep(0.5)
                mid = js(br, "return {state: window.__report().state, "
                             "curtains: window.__hooks.curtains.slice()};")
                idle(br)
                end = js(br, "return {state: window.__report().state, docks: window.__hooks.docks.slice(), "
                             "curtains: window.__hooks.curtains.slice(), "
                             "events: window.__report().events.map(function(e){return e.name;}).slice(-6)};")
                check(BROWSER_ROWS[19],
                      took["took"] and mid["state"] == "running" and mid["curtains"][:1] == [True]
                      and end["state"] == "idle" and len(end["docks"]) == 1
                      and end["curtains"][-1] is False and "docked" in end["events"],
                      f"mid={mid} end={end}")

                cam = js(br, "var r = window.__report(); "
                             "return {camera: r.camera, rest: r.rest, handoffs: r.handoffs, "
                             "tol: r.camTolerances};")
                check(BROWSER_ROWS[20],
                      cam["camera"] and cam["camera"]["owner"] == "stage"
                      and cam["handoffs"] == []
                      and cam["rest"] and cam["rest"]["rested"] is True
                      and cam["rest"]["off"] <= cam["tol"]["rest"],
                      f"owner={cam['camera'] and cam['camera']['owner']} rest={cam['rest']} "
                      f"handoffs={cam['handoffs']} — the manifest asks for no camera, so the stage "
                      f"holds it for the whole pass")

                # ---- §4.4b: every handle reaches the picture -------------------------------------
                # A handle read back off the diagnostic surface proves the GRAPH evaluated it. It
                # says nothing about whether the instrument obeyed it. These runs differ by exactly
                # one handle each and are photographed, so a picture that did not move is a handle
                # the instrument is not reading. `clock` is the one handle deliberately left out and
                # the reason is the module's own: every position in it is a pure function of the
                # dial, so the handed second moves nothing on screen and a handle row asking it to
                # would be asking the module to break its own law.
                # THE POSE THE MOVES ARE TAKEN AT, and why it is 0.6 rather than the middle. Every
                # voice is a sine, so at some poses a voice's own handle moves it across a zero of
                # that sine and the frame barely changes — which would say nothing about whether the
                # instrument reads the handle. The pose and the twelve moved values below were
                # solved for on the module's own arithmetic: at `mix` 0.6 the smallest of the twelve
                # moves still carries its voice a quarter of the way across its own range, which is
                # the point of the passage where this row asks the hardest question rather than the
                # easiest. Both works have matter in the frame there.
                br.evaluate("window.__show('host'); 0")
                MID = 0.6
                MOVES = {"levelA": 0.15, "levelB": 0.85, "cellsA": 16, "cellsB": 16,
                         "colourPeriodA": 0.05, "colourPhaseA": 0.15, "colourAmpA": 1.0,
                         "lightPeriodA": 0.4, "lightPhaseA": 0.7, "lightAmpA": 1.0,
                         "colourPeriodB": 0.2, "colourPhaseB": 0.0, "colourAmpB": 1.0,
                         "lightPeriodB": 0.6, "lightPhaseB": 0.05, "lightAmpB": 1.0,
                         "mask": 1, "mix": 0.2}
                shot = {}
                js(br, "return window.__hostDraw(%s);" % json.dumps(dict(VOICES, mix=MID)))
                br.sleep(0.2)
                shot["base"] = png(br, SHOTS / "handle-base.png")
                for k, v in sorted(MOVES.items()):
                    over = dict(VOICES, mix=MID)
                    over[k] = v
                    js(br, "return window.__hostDraw(%s);" % json.dumps(over))
                    br.sleep(0.15)
                    shot[k] = png(br, SHOTS / ("handle-" + k + ".png"))
                moved = {k: diff(shot["base"], shot[k]) for k in MOVES}
                # THE SIX COLOUR-VOICE HANDLES ARE WEIGHED ON THE COLOUR THEY MOVE, and that is not
                # a softer bar — it is the right measure, and it is a harder question. A colour
                # voice moves a piece's SATURATION, and the two photographs this suite runs on stand
                # 10.82 and 6.73 of 255 from grey in the mean; on them the WHOLE colour voice — a
                # piece carried from its full colour to grey — could not move a frame's mean channel
                # by six however faithfully the instrument read the handle. That is the lab's own
                # recorded behaviour rather than a weakness of the port: its assembler measures each
                # voice on the real photograph and MUTES a voice the work cannot sing, «голоса,
                # которых работа спеть не может» (lab/step4-assembler.js).
                #
                # So each of the six is asked the question its own voice answers: the frame's
                # DISTANCE FROM GREY has to move, and it has to move the WAY the instrument's own
                # `values()` says that work's saturation moved. An unmoved pose photographs byte for
                # byte the same — the repeat row above proves it on this very bench — so a shift of
                # nothing is a handle the instrument never read, and a shift the wrong way is a
                # handle it read backwards.
                COLOUR_H = ["colourPeriodA", "colourPhaseA", "colourAmpA",
                            "colourPeriodB", "colourPhaseB", "colourAmpB"]
                base_c = chroma(shot["base"])
                base_v = js(br, "return window.__hostValues(%s);"
                            % json.dumps(dict(VOICES, mix=MID)))
                chrom = {}
                for k in COLOUR_H:
                    w = 0 if k.endswith("A") else 1
                    over = dict(VOICES, mix=MID)
                    over[k] = MOVES[k]
                    vm = js(br, "return window.__hostValues(%s);" % json.dumps(over))
                    chrom[k] = (chroma(shot[k]) - base_c, vm["sat"][w] - base_v["sat"][w])
                still = ([k for k, (mn, _) in moved.items()
                          if k not in COLOUR_H and mn <= SEAM]
                         + [k for k in COLOUR_H
                            if chrom[k][0] == 0.0 or chrom[k][0] * chrom[k][1] < 0])
                check(BROWSER_ROWS[21], not still,
                      "; ".join(f"{k} moves the frame by {mn:.4f} of 255"
                                for k, (mn, _) in sorted(moved.items()) if k not in COLOUR_H)
                      + " | the six colour-voice handles, weighed on the colour they move: "
                      + "; ".join(f"{k} moves that work's saturation by {ds:+.4f} and the frame "
                                  f"{dc:+.4f} of 255 from grey (its plain channel move is "
                                  f"{moved[k][0]:.4f})" for k, (dc, ds) in chrom.items())
                      + f" | the base frame stands {base_c:.4f} of 255 from grey; the seam "
                      f"threshold is {SEAM} for the twelve, and `clock` is left out because the "
                      f"module's own law is that nothing in it reads a second"
                      if not still else "these handles move nothing, or move the wrong way: "
                      + ", ".join(still))

                # ---- THE DOOR THE INSTRUMENT READS FOR ITSELF ------------------------------------
                # This instrument's doors are exact on any grid — its mask crosses over nowhere and
                # its strata travel by whole frame heights — so nothing here is ever walked back and
                # the reading is a state published rather than a range guarded. What the reading is
                # FOR is the one thing that can still break a door: the two accompanying voices. The
                # row states that the buffer reaches the reading, that the state is on the record,
                # that the reading is taken at a door and nowhere else, and that with the voices at
                # full amplitude the reading is still exactly nothing.
                def door_pose(mix, buf=None, over=None):
                    p = dict(VOICES)
                    p.update({"mix": mix, "levelA": LEVEL["a"], "levelB": LEVEL["b"],
                              "cellsA": 128, "cellsB": 128, "mask": 0, "t": 0, "reduced": False,
                              "cssWidth": VW, "cssHeight": VH})
                    if buf:
                        p["bufWidth"], p["bufHeight"] = int(buf[0]), int(buf[1])
                    p.update(over or {})
                    return p

                def values_of(p):
                    return js(br, "return window.__exPass.bench.values('strata-light', %s);"
                              % json.dumps(p))

                BUF = (780, 1688)
                on_css = values_of(door_pose(0))
                on_buf = values_of(door_pose(0, buf=BUF))
                exitdoor = values_of(door_pose(1, buf=BUF))
                away = values_of(door_pose(0.5, buf=BUF))
                tiny = values_of(door_pose(0, buf=(64, 32), over={"cellsA": 512, "cellsB": 512}))
                check(BROWSER_ROWS[22],
                      on_css["doorGrid"] == {"w": VW, "h": VH, "drawn": False}
                      and on_buf["doorGrid"] == {"w": BUF[0], "h": BUF[1], "drawn": True}
                      and on_buf["doorStanding"] == 0 and exitdoor["doorStanding"] == 1
                      and away["doorGrid"] is None and away["doorStanding"] is None
                      and on_buf["doorWhyNo"] is None and exitdoor["doorWhyNo"] is None
                      and tiny["doorWhyNo"] is None
                      and on_buf["dial"] == [0, 1] and exitdoor["dial"] == [1, 0]
                      and on_buf["colourVoice"] == [0, 0] and on_buf["lightVoice"] == [0, 0]
                      and exitdoor["colourVoice"] == [0, 0] and exitdoor["lightVoice"] == [0, 0],
                      "on the %d x %d CSS frame the reading names that frame; on the %d x %d buffer "
                      "the frame is drawn on it names the buffer, says the DEPARTING work is the "
                      "one standing, and reads both of its voices at exactly %s and %s with every "
                      "voice field at full amplitude. The exit door says the same of the arriving "
                      "work (dial %s). Away from a door it reads nothing at all (grid %s). On a "
                      "%d x %d buffer at %g cells — a cell finer than a point of the buffer — the "
                      "door still stands whole, because no grid decides this instrument's doors."
                      % (VW, VH, BUF[0], BUF[1], on_buf["colourVoice"], on_buf["lightVoice"],
                         exitdoor["dial"], away["doorGrid"], 64, 32, 512))

                # ---- THE CELL, MEASURED RATHER THAN ASSUMED -------------------------------------
                # The module reads a mask cell as the MEAN of the file's pixels inside it; this
                # instrument reads the cell at its own centre. Both grids are built with the
                # module's own arithmetic and cut at the module's own measured level; only the
                # reading of a cell differs. The row states that the departure is bounded — the two
                # readings put the same cells on the same side of the level for the great body of
                # the mask — and PRINTS the share rather than assuming one.
                def module_grid(path, cells):
                    """The module's own lumGrid arithmetic: `cells` on the file's long side and the
                    short side in proportion (lab/effects/strata-light.js:59-66)."""
                    from PIL import Image
                    iw, ih = Image.open(path).size
                    if iw >= ih:
                        return [cells, max(1, round(cells * ih / float(iw)))]
                    return [max(1, round(cells * iw / float(ih))), cells]

                cellrows, off_grid = [], []
                for which, path in (("a", BENCH / "photos" / "towers.jpg"),
                                    ("b", BENCH / "photos" / "glassgrid.jpg")):
                    for cells in (128, 32):
                        r = js(br, "return window.__cellAgreement(%r, %d);" % (which, cells))
                        cellrows.append((which, cells, r))
                        if r["grid"] != module_grid(path, cells):
                            off_grid.append("%s at %d: %s against the module's own %s"
                                            % (which, cells, r["grid"],
                                               module_grid(path, cells)))
                        if abs(r["level"] - LEVEL[which]) > 1e-12:
                            off_grid.append("%s parts at %r, not at the module's own %r"
                                            % (which, r["level"], LEVEL[which]))
                check(BROWSER_ROWS[23], not off_grid and len(cellrows) == 4,
                      "; ".join(f"{w} at {c} cells (grid {r['grid'][0]}x{r['grid'][1]}, level "
                                f"{r['level']:.4f}): {r['agree']} of {r['cells']} cells "
                                f"({100.0 * r['agree'] / r['cells']:.2f}%) fall on the same side "
                                f"of the level as the module's own mean puts them"
                                for (w, c, r) in cellrows)
                      + " — the departure the port records, measured on the two photographs this "
                        "suite runs on rather than assumed. Both grids are the module's own shape "
                        "and both are cut at the module's own measured level, which is what this "
                        "row asserts; the share is a READING and no bar, since a cell the two "
                        "roads read differently is a cell of the mask stepping one place and never "
                        "a pair turned away"
                      if not off_grid else "; ".join(off_grid))

                kept = sorted(p.name for p in SHOTS.glob("*.png"))
                check(BROWSER_ROWS[24],
                      len(kept) >= 25 and all((SHOTS / k).stat().st_size > 1000 for k in kept),
                      f"{len(kept)} captures under {SHOTS.relative_to(ROOT)}: the two doors on both "
                      f"roads, the mask channel at the middle, the seven sampled instants, the "
                      f"frame after a resize, the two repeated runs and the seventeen handle runs")

    shutil.rmtree(BENCH, ignore_errors=True)

    # ============================================================================================
    # THE RED-ON-BUG PROOF. The repair reverted in the artifact the browser actually loads: the
    # window 4u(1 − u) is taken out of the accompanying voice, which is the one thing that holds
    # both voices to nothing at both doors. With it standing, a door is exactly the picture the file
    # carries however loudly a score sings; with it gone, the light voice — whose phase is a quarter
    # of a turn, so its sine stands at its own maximum at the entry door — writes the whole standing
    # frame lighter, and the instrument's own door reading says so and refuses rather than drawing
    # it. The pack served is changed and the host is re-stamped with the digest of the bytes it is
    # handed, which is what the build does; the file on disk is never touched.
    def red_one(br):
        gen = js(br, "return window.__offer(%s, {clock: 0, progress: 0});"
                 % json.dumps(strata_score(0.5, 0.5)))["gen"]
        br.sleep(1.1)
        r = js(br, "var r = window.__report(); return {state: r.state, drew: r.drew, "
                   "refused: r.events.filter(function(e){ return e.gen === %d && e.why "
                   "&& String(e.why).indexOf('door leaks') >= 0; })"
                   ".map(function(e){ return String(e.why); })};" % gen)
        # and what the door reads on its own, apart from the road
        r["read"] = js(br, "return window.__exPass.bench.values('strata-light', %s);"
                       % json.dumps(dict(VOICES, mix=0, levelA=0.5, levelB=0.5, cellsA=128,
                                         cellsB=128, mask=0, t=0, reduced=False,
                                         cssWidth=VW, cssHeight=VH)))
        br.evaluate("window.__cancel('red one'); 0")
        return r

    base_read = on_bench(red_one)
    bug = REGION.replace(
        "return a * Math.sin(2 * Math.PI * (u / p + (+phase || 0))) * 4 * u * (1 - u);",
        "return a * Math.sin(2 * Math.PI * (u / p + (+phase || 0)));", 1)
    bug_read = on_bench(red_one, pack_text=bug)
    check(RED_ROWS[0],
          bug != REGION and base_read and bug_read
          and not base_read["refused"] and base_read["state"] == "running"
          and base_read["read"]["lightVoice"] == [0, 0]
          and base_read["read"]["doorWhyNo"] is None
          and len(bug_read["refused"]) >= 1 and bug_read["state"] == "idle"
          and "the entry door leaks" in bug_read["refused"][0]
          and bug_read["read"]["lightVoice"][0] != 0
          and bug_read["read"]["doorWhyNo"],
          f"with the window standing the entry door reads both voices at "
          f"{base_read and base_read['read']['colourVoice']} and "
          f"{base_read and base_read['read']['lightVoice']}, the door is whole and the pass runs "
          f"(state {base_read and base_read['state']}, {base_read and len(base_read['refused'])} "
          f"refusals). With the window taken out of the voice — the module's own line, less its own "
          f"window — the same door reads a light voice of "
          f"{bug_read and bug_read['read']['lightVoice'][0]} and the instrument refuses it with "
          f"«{(bug_read and bug_read['refused'] or ['nothing refused'])[0][:220]}», on which the "
          f"host lands the transaction (state {bug_read and bug_read['state']}) and the walk's own "
          f"glide carries the visitor")

shutil.rmtree(TMP, ignore_errors=True)

# A row that never ran is no pass. Anything declared above and never reached is recorded here with
# that as its reason, so a run cut short reads as a red rather than as a shorter green suite.
ran = {name for name, _, _ in results}
for name in BROWSER_ROWS + RED_ROWS:
    if name not in ran:
        check(name, False, "the row never ran")

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
