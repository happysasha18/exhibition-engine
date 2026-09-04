#!/usr/bin/env python3
"""PASS-API-V1 — the waterline instrument on the host's frame.
Run: python3 tests/test_pass_waterline.py

Root: his word of 2026-08-18 18:39 — every effect the lab holds belongs in the engine's arsenal,
with all its handles. This suite is the waterline lane's own proof.
docs/design/PASS-API-V1.md §7 (GPU and resources), §8 (the manifest) and §9's conformance rows 7, 9,
10, 13, 14, 15, 16 and 22 are what this file makes real; the lifecycle rows stay in
tests/test_pass_api.py and are untouched.

WHAT IS COMPARED, AND AGAINST WHAT.

  The doors. At the dial's two ends one whole work stands. Each is measured against ITS OWN FILE —
  the picture cover-fitted into the frame and pulled in by the headroom the counter-motion and the
  swell need between them (the module's own ZOOM of 1.18) — inside the project's seam threshold of
  6 of 255. A door that carried a ten-thousandth of the other photograph would fail this.

  The five poses. The host's frame is compared against the LAB MODULE's own frame, on one pose both
  roads were driven by: the same dial, the same five params, the same channels, the same two
  measured seams, the same die, the same second. Two roads of one frame, never two guesses at one.

  THE DERIVATION, WHICH IS WHAT THIS INSTRUMENT IS FOR. The waterline is no number of the module's
  own: it is the departing work's own measured `seam_y` carried into the frame through the seating
  the host applied. Two rows read that, and both compute what the line OUGHT to be here — in this
  file, out of the measured seam and the published crop — rather than asking the instrument:

    · on the picture. The judges' `comb` channel changes the water and nothing above it, so two
      frames differing only in it are identical to the pixel above the line and the topmost row that
      moves IS the waterline. It is read at a dial where the water stands fully open AND the line
      still rests on the departing work's own seam, which is the only stretch of the dial where the
      derivation can be measured on a frame at all (the module's own OPEN_IN < LINE_HOLD).
    · at the middle. Wherever the two seams stand, the line crosses the frame's centre at the mark
      where half the frame has changed hands.

  No empty frame. The module asks its own context to preserve the drawing buffer (waterline.js:407)
  and §7 refuses that. The flag stood in for a redraw: the module draws on demand and under reduced
  motion draws once and stops. The host draws every frame and redraws on resize, so the rows below
  sample the pass at seven instants and once across a change of viewport.

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
MODULE = LAB / "effects" / "waterline.js"

SITE_URL = "https://synth.example.com"
VW, VH = 390, 844          # the phone frame lab/carrier-check.py measures on
CLOCK = 7.0                # the second the comparison holds at, as the carrier's own check does
SEAM_BAR = 6.0             # the project's seam threshold, 6 of 255 (TRANSITION-STAGE-V0 §1)
SAME = 1.5                 # two roads of one frame: the carrier check's own bar
FAR = 40.0                 # further than this from a file and it is a different work
# A frame that stands as a picture. The canvas's own background is one flat colour, so a drawn frame
# is far from it and carries a spread of its own. Both numbers are read off the capture.
BACKGROUND = (0x08, 0x08, 0x0a)
SPREAD = 10.0

# THE TWO WORKS' OWN MEASURED MIRROR LINES, and the seating they are carried through. Measured by
# the project's own `measure()` in lab/step1-motifs.py, run on these two files; `seam_horizon`
# beside each is the strength the composer ranks a pair by, and it reproduces the two numbers the
# drifting instrument's own fixture already carries for the same two photographs.
SEAM_A, SEAM_B = 0.2988, 0.5703
SEAM_HORIZON_A, SEAM_HORIZON_B = 0.0882, 0.0016
# The module's own crop, derived from AMP and RIP and no free number of its own.
ZOOM = 1 + 2 * (0.055 + 0.020) + 0.03
# Both photographs are wider than a 390 x 844 frame, so a cover fit leaves the height whole and the
# crop is the whole of the y seating. This is `fit`'s own arithmetic, written out here so the rows
# below hold the instrument against a number it did not supply.
FIT_Y = 1.0 / ZOOM


def seam_in_frame(seam):
    v = 0.5 + (seam - 0.5) / FIT_Y
    return min(0.94, max(0.06, v))


LINE_A, LINE_B = seam_in_frame(SEAM_A), seam_in_frame(SEAM_B)

# Captures are kept rather than swept, because §9 row 16 asks for evidence for every landed
# instrument and evidence that is deleted is no evidence.
SHOTS = ROOT / "tests" / "captures" / "pass-waterline"

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


# ---------------------------------------------------------------- the score this instrument plays
# AUTHORED HERE, and said to be authored here. lab/data/scores carries a template and a table for
# the woven instrument alone, so there is no per-pair score on file for this one. Everything below
# is either a number the module itself declares or a field the contract requires; the only measured
# numbers are the two seams above, and they were measured by the project's own script.
DIE = 4.91016            # the die lab/data/scores' own weave score carries, so both suites roll one
DURATION_MS = 3000
WITHIN_MS = 500

HANDLE_DEFAULTS = {"line": 0.5, "depth": 0.3, "swell": 0.45, "lead": 0.62, "order": 0.2,
                   # the two the port publishes that the module holds as constants; at these two
                   # values they ARE those constants
                   "settle": 1, "tideCells": 0.5,
                   "shade": 1, "shadeEdge": 1, "shadeLine": 1, "travel": 1, "comb": 1, "raw": 0,
                   "seamA": SEAM_A, "seamB": SEAM_B, "seed": DIE}


def waterline_score(pair_a="a", pair_b="b", **statics):
    """The score, with a track for every one of the sixteen handles (§4.4b).

    The five params rest at the module's own declared defaults (waterline.js:344-350): the
    waterline at 0.5, the reflection at 0.3, the swell at 0.45, the water ahead at 0.62 and the
    tide order at 0.2. The six judges' channels rest where the module holds them. `mix` reads the
    transaction's own progress and `clock` the second the host hands down — that second is the only
    place the module ever read time, and it read its own accumulated frame clock there
    (waterline.js:562-569). `seamA`/`seamB` carry the two works' own measured mirror lines.
    """
    P = dict(HANDLE_DEFAULTS)
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
        "intent": "the mirror seam of a work read as a real horizon: sky above, its own reflection "
                  "below, the line travelling from one work's measured seam to the other's, and the "
                  "water carrying the arriving work long before the sky does "
                  "(lab/effects/waterline.js:1-25, its own header)",
        "pair": {"a": pair_a, "b": pair_b},
        "seed": DIE,
        "duration": DURATION_MS,
        "direction": "a-to-b",
        "interruption": {"withinMs": WITHIN_MS, "resolve": "nearest-door"},
        "failLand": "arrive",
        "camera": {"owner": "stage", "rests": "b",
                   "track": [{"at": "b", "pan": {"x": 0, "y": 0}, "logScale": 0,
                              "pitch": 0, "yaw": 0, "roll": 0, "fov": None, "owner": "stage"}]},
        "cues": [{
            "id": "waterline-main",
            "instrument": {"id": "waterline", "api": 1},
            "voice": "letter",
            "roles": ["disassembly", "mystery", "assembly"],
            "levels": ["WORLD", "SURFACE"],
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
        "quality": {v: {"renderScale": None, "cues": {"waterline-main": {"resources": res[v]}}}
                    for v in ("lean", "standard", "rich")},
        "provenance": {"source": "lab/effects/waterline.js's own declared defaults and constants, "
                                 "with the two seams measured by lab/step1-motifs.py",
                       "measuredAt": None, "by": "tests/test_pass_waterline.py"},
    }


# ---------------------------------------------------------------- bake once
build_site.SITE_CONFIG = dict(build_site.SITE_CONFIG)
build_site.SITE_CONFIG["pass"] = {"visualLayer": "pass", "diagnostics": "on"}

TMP = Path(tempfile.mkdtemp(prefix="synth_passwaterline_"))
build_site.OUT = TMP
build_site.build(SITE_URL)
LAYER = (TMP / "pass-layer.js").read_text(encoding="utf-8")
# The instrument's own region of the BUILT file — the real artifact, comments stripped as it ships.
# A row about the HOST reads LAYER; a row about this instrument's own mathematics reads REGION.
REGION = (TMP / "pass-inst-waterline.js").read_text(encoding="utf-8")

# ---------------------------------------------------------------- string rows

OWNED = ["createElement", "getContext", "requestAnimationFrame", "addEventListener",
         "performance.now", "Date.now", "new Image", "setTimeout", "setInterval"]
held = [s for s in OWNED if s in REGION]
check("PASS-WATERLINE the instrument creates no context, no canvas, no loop and no listener",
      not held,
      "§1.2's fence, read against the instrument's own region of the file: none of the nine ways of "
      "owning hardware appears there, so the module's canvas, its WebGL 1 context, its frame loop "
      "and its resize listener all stayed in the lab"
      if not held else "the instrument's region holds " + ", ".join(held))

HANDLES = ["mix", "clock", "line", "depth", "swell", "lead", "order", "settle", "tideCells",
           "seed", "shade", "shadeEdge", "shadeLine", "travel", "comb", "raw", "seamA", "seamB"]
missing_h = [h for h in HANDLES if ("%s: { min" % h) not in REGION]
check("PASS-WATERLINE every handle the module carries is a handle a score can drive",
      not missing_h,
      "§4.4b: eighteen handles — the dial, the clock, the module's five declared params, the two "
      "the port publishes that the module held as constants, its die, its six judges' channels and "
      "the two works' own measured mirror lines. The module's `photo` handle is the one that could "
      "not cross: the host owns which two works stand in the pair and hands the instrument two "
      "textures rather than a list to choose from"
      if not missing_h else "these are not published: " + ", ".join(missing_h))

# THE PINNED NUMBERS THE PORT LIFTED, and the ones it left pinned with a reason. His 15:13 word
# bans a static transition and his 19:13/19:21 words make the derivation the law, so a number the
# works' own records could set is a parameter. Both handles below stand at exactly the module's own
# constant at their own default, which is what keeps the two roads comparable at all.
check("PASS-WATERLINE the two constants a record can set are handles, and stand at the module's "
      "own number at their default",
      'settle: { min: 0, max: 1, def: 1, level: "SURFACE" }' in REGION
      and "tideCells: { min: 0, max: 1, def: 0.5," in REGION
      and "var CELL_SPAN = 1.0;" in REGION
      and "cells: [CELLS_X * cell, CELLS_Q * cell]" in REGION
      and "clamp(st.travel, 0, 1) * clamp(st.settle, 0, 1)" in REGION
      and 'name: "uCells", type: "vec2", source: "frame:cells"' in REGION,
      "the counter-motion reached the picture at AMP alone with only a judges' channel over it, so "
      "every pair in the world settled by the same distance — `settle` carries the share of it the "
      "pair asks for, and AMP stays pinned because the cover crop is derived from it. The tide's "
      "two patch counts were literals substituted into the shader — `tideCells` carries them "
      "together in octaves about the module's own 19 and 8, which is the one number here whose "
      "unit matches a record's exactly. RIP and SWAY are already scaled by the MEASURED `swell` "
      "handle through uSway and uComb, so neither was static and neither moved")

check("PASS-WATERLINE the water reads the handed-down second and no clock of its own",
      "time: st.reduced ? 0 : (Number(st.t) || 0)" in REGION and "t: h.clock" in REGION,
      "waterline.js:562-569 accumulated its own frame time; here every wave train reads the `clock` "
      "handle through `values`, which is what makes the seeded repeat below mean anything")

check("PASS-WATERLINE the manifest leaves the drawing buffer unpreserved",
      "gl: { preserveDrawingBuffer: false }" in REGION,
      "the module asks its own context for a preserved buffer (waterline.js:407) and §7 refuses a "
      "manifest that asks for it; the redraw it stood in for is the host's own frame loop")

LABTXT = MODULE.read_text(encoding="utf-8") if MODULE.exists() else ""

check("PASS-WATERLINE the shader carries no version header of its own",
      "#version" not in REGION and (not LABTXT or "#version" not in LABTXT),
      "so the host's translator stamps the one header this shader needs and no second one arrives")


def numbers(text, pattern):
    m = re.search(pattern, text)
    return [float(x) for x in re.findall(r"-?\d+\.?\d*", m.group(1))] if m else []


CURVE_NAMES = ["dial", "line", "depth", "swell", "lead", "order"]
curve_off = []
for cname in CURVE_NAMES:
    lab_q = numbers(LABTXT, cname + r": \[([^\]]+)\]")
    port_q = numbers(REGION, cname + r": \[([^\]]+)\]")
    if len(port_q) != 21 or lab_q != port_q:
        curve_off.append("%s (%d lab, %d port)" % (cname, len(lab_q), len(port_q)))
check("PASS-WATERLINE all six measured response curves are carried digit for digit",
      not curve_off and "DIAL_D0 = 0.055" in LABTXT and "DIAL_D0 = 0.055" in REGION,
      "six curves at twenty-one knots each and the dead band of 0.055 at both ends of the dial, "
      "unchanged: lab/waterline-check.py --fit wrote them from the rate measured through the "
      "judges' `raw` channel, and the port re-derives nothing"
      if not curve_off else "these differ: " + ", ".join(curve_off))

# Each constant as the LAB module spells it and as the PORT spells it. The three that differ are
# the three the port had to give a name to, because the door reading below is arithmetic on them
# and a number read in two places has to have one home.
CONSTANTS = [
    ("AMP = 0.055", "AMP = 0.055", "the counter-motion, frame heights at its widest"),
    ("RIP = 0.020", "RIP = 0.020", "how far the swell combs the reflection sideways"),
    ("SWAY = 0.005", "SWAY = 0.005", "how far the waterline itself wavers"),
    ("ZOOM = 1 + 2 * (AMP + RIP) + 0.03", "ZOOM = 1 + 2 * (AMP + RIP) + 0.03",
     "the crop, DERIVED from the two travels above and no free number"),
    ("DIE_W = 0.40", "DIE_W = 0.40", "six parts the ladder, four parts the score's die"),
    ("CELLS_X = 19.0", "CELLS_X = 19.0", "the tide line's patches across the frame"),
    ("CELLS_Q = 8.0", "CELLS_Q = 8.0", "and down the ladder"),
    ("SHADE_FRONT = 0.30", "SHADE_FRONT = 0.30", "the contact shadow at the arriving work's edge"),
    ("SHADE_REACH = 6.0", "SHADE_REACH = 6.0", "and how many pixels it decays over"),
    ("SHADE_LINE = 0.26", "SHADE_LINE = 0.26", "the contact shadow under the waterline"),
    ("LINE_REACH = 10.0", "LINE_REACH = 10.0", "and its own reach"),
    ("DARK_DEEP = 0.16", "DARK_DEEP = 0.16", "how much darker the water gets toward the near edge"),
    ("DARK_BASE = 0.05", "DARK_BASE = 0.05", "and how dark it is at the line"),
    ("HAZE = 0.12", "HAZE = 0.12", "how much colour the water loses in the depth"),
    ("LINE_LIFT = 0.15", "LINE_LIFT = 0.15",
     "how far the `line` handle may carry the waterline off its own place"),
    ("LINE_HOLD = 0.22", "LINE_HOLD = 0.22",
     "how much of the dial the line stands still on the departing work's own seam"),
    ("OPEN_IN = 0.12", "OPEN_IN = 0.12",
     "how much of the dial the water takes to rise, and it is SMALLER than LINE_HOLD on purpose"),
    ("GUARD_IN = 0.10", "GUARD_IN = 0.10", "and the two contact shadows to come up"),
    ("DEP_LO = 0.75, DEP_HI = 2.25", "DEP_LO = 0.75, DEP_HI = 2.25",
     "the mirror's scale, crowded folds to one long fold"),
    ("* 1.10", "var SPREAD_MAX = 1.10;",
     "how far apart the patches' own moments are set at the far end of the tide order, named in "
     "the port because the door reading is arithmetic on it"),
    ("0.5 * spread + 0.05", "var MARGIN = 0.05;",
     "how far past the field's own range the threshold reaches, which is the number that makes the "
     "dead bands dead — named in the port for the same reason"),
    ("mix(1.04, uLine, uOpen)", "var BASE_OUT = 1.04;",
     "where the waterline stands with the water drained out, below the bottom edge of the frame"),
]
missing_const = ([c for c, _, _ in CONSTANTS if LABTXT and c not in LABTXT]
                 + [c for _, c, _ in CONSTANTS if c not in REGION]
                 + ([] if "0.5 * spread + MARGIN" in REGION else ["0.5 * spread + MARGIN"])
                 + ([] if "* SPREAD_MAX" in REGION else ["* SPREAD_MAX"])
                 + ([] if "mix(1.04, uLine, uOpen)" in REGION else ["the shader's own 1.04"]))
check("PASS-WATERLINE every constant stands at the number the lab module gives it",
      not missing_const,
      "; ".join("%s — %s" % (c, why) for c, _, why in CONSTANTS) if not missing_const
      else "these differ: " + ", ".join(missing_const))

check("PASS-WATERLINE the host binds uniforms by declared name, never by position or a written list",
      "getUniformLocation(p, u.name)" in LAYER and "gl.uniform1f(U.uLine" not in LAYER
      and "gl.uniform1f(U.uTau" not in LAYER,
      "the module's own draw names its eighteen uniforms literally (waterline.js:519-545); the host "
      "reads the manifest and no list of names is written into it")

declared = set(re.findall(r'\{ name: "(u\w+)", type:', REGION))
spelled = set(re.findall(r'uniform \w+ (u\w+);', REGION))
check("PASS-WATERLINE the manifest's declared names and the shader's own names are one set",
      declared == spelled and len(declared) == 20,
      f"{len(declared)} declared, {len(spelled)} spelled. The module's own `uAspect` is the one "
      f"uniform that did not come over — the host owns the buffer and already binds its size, so "
      f"the aspect is derived from `uRes` inside the shader — and `uCells` is the one the port "
      f"added, because the module substitutes its two cell counts into the source as literals and "
      f"a count a record can set may not be a literal; "
      f"declared only: {sorted(declared - spelled)}; spelled only: {sorted(spelled - declared)}")

check("PASS-WATERLINE the manifest publishes what it cuts on and what it reads of a pair, and "
      "nothing that can refuse one",
      'cuts: ["band"]' in REGION
      and '"motifs.measured"' in REGION and '"structure.horizon.y"' in REGION
      and 'seamA: { min: 0, max: 1, def: 0.5, level: "WORLD" }' in REGION
      and 'seamB: { min: 0, max: 1, def: 0.5, level: "WORLD" }' in REGION,
      "the waterline parts the frame into two BANDS and the crossing travels through the line "
      "between them; the reading it publishes is the motif list that carries the seam and the "
      "work's own measured horizon, and it RANKS only — a pair carrying no measured seam rests on "
      "the handles' own default of 0.5, which is the frame's own middle and the module's own "
      "fallback, so such a pair plays rather than being turned away. THE TWO SEAM LITERALS GAINED A "
      "LEVEL on 2026-08-25, with the sweep that made every handle in the fleet declare the "
      "structural level it drives — the seam is where the frame parts into its two bands, which is "
      "a WORLD reading — and the row follows them there while holding every number and every "
      "default it always held")

# ---------------------------------------------------------------- browser rows

BROWSER_ROWS = [
    "PASS-WATERLINE §8     · the manifest carries every field the contract names, in its shape",
    "PASS-WATERLINE row 7  · door 0 stands the departing work, measured against its own file",
    "PASS-WATERLINE row 7  · door 0 carries no trace of the arriving work",
    "PASS-WATERLINE row 7  · door 1 stands the arriving work, measured against its own file",
    "PASS-WATERLINE row 7  · door 1 carries no trace of the departing work",
    "PASS-WATERLINE the host's frame and the lab module's frame agree at all five poses",
    "PASS-WATERLINE §7     · no empty frame at any sampled instant of the pass",
    "PASS-WATERLINE §7     · the frame after a change of viewport is drawn, not a kept buffer",
    "PASS-WATERLINE row 10 · a seeded run repeats to the pixel",
    "PASS-WATERLINE row 14 · textures, programmes and framebuffers return to their baseline after ten runs",
    "PASS-WATERLINE row 15 · the console stays clean",
    "PASS-WATERLINE row 22 · the census shows granted against declared, and neither overruns",
    "PASS-WATERLINE §7     · a manifest asking for a preserved drawing buffer is refused, with its reason",
    "PASS-WATERLINE §7     · a uniform bound to a name the shader lacks is refused, with its reason",
    "PASS-WATERLINE §7     · one canvas, one context, two source textures, one pass a frame",
    "PASS-WATERLINE §7     · a shader already at GLSL ES 3.00 receives no second version header",
    "PASS-WATERLINE the real transaction road: curtain up, one pass drawn, exactly one dock at the end",
    "PASS-WATERLINE row 9  · one camera authority through a real pass, and the pose rests on the arrival",
    "PASS-WATERLINE §4.4b  · every one of the sixteen driven handles reaches the PICTURE",
    "PASS-WATERLINE row 16 · the captures are kept as evidence",
    "PASS-WATERLINE the waterline stands on the departing work's own measured seam, ON THE PICTURE",
    "PASS-WATERLINE the line crosses the frame's centre at the mark where the works change places",
    "PASS-WATERLINE the door is read on the DRAWING BUFFER, and both doors are whole on every "
    "buffer a browser can hand",
    "PASS-WATERLINE a pair carrying no measured seam plays, with the line at the frame's own middle",
]

RED_ROWS = [
    "PASS-WATERLINE red-on-bug · the lift read against the middle of the range: the line leaves "
    "the seam at the handle's own default",
    "PASS-WATERLINE red-on-bug · the seam not carried through the seating: the line stands where "
    "the FILE puts it and not where the FRAME does",
    "PASS-WATERLINE red-on-bug · the travel un-hinged: the line no longer crosses the centre at "
    "the dial's own middle",
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


def rows_that_move(p, q, bar=6):
    """Every row of the frame on which the two captures differ by more than `bar` of 255 anywhere,
    and the height they were read on. The `comb` channel changes the water and nothing above it, so
    this is where the waterline is."""
    from PIL import Image, ImageChops
    a = Image.open(p).convert("RGB")
    c = Image.open(q).convert("RGB")
    if a.size != c.size:
        return [], 0
    d = ImageChops.difference(a, c).convert("L")
    w, h = d.size
    px = d.load()
    out = []
    for y in range(h):
        for x in range(w):
            if px[x, y] > bar:
                out.append(y)
                break
    return out, h


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
    """The work as the instrument seats it: cover-fit, then the centre crop the two travels are
    paid for with (the module's own ZOOM)."""
    from PIL import Image
    im = Image.open(src).convert("RGB")
    iw, ih = im.size
    fa, ia = w / float(h), iw / float(ih)
    sw, sh = (ih * fa, float(ih)) if ia > fa else (float(iw), iw / fa)
    sw /= zoom
    sh /= zoom
    x0, y0 = (iw - sw) / 2.0, (ih - sh) / 2.0
    return im.resize((w, h), Image.BILINEAR, box=(x0, y0, x0 + sw, y0 + sh))


def apart(p, work):
    from PIL import Image, ImageChops, ImageStat
    a = Image.open(p).convert("RGB")
    if a.size != work.size:
        return 255.0, 255.0
    st = ImageStat.Stat(ImageChops.difference(a, work))
    return sum(st.mean) / 3.0, max(m for _, m in st.extrema)


def bench_dir(pack_text=None):
    """The bench's own served root: the BUILT pass-layer.js, every built instrument file, the lab
    module unchanged, the two photographs, and the page that stands the two roads of one frame side
    by side.

    A row proving a rule reds hands over a CHANGED instrument file and writes the site's own record
    with the digest of the bytes actually served, which is what the build does. The source file on
    disk is never touched, so nothing has to be restored and no working tree can be left changed by
    a red-on-bug proof."""
    d = Path(tempfile.mkdtemp(prefix="synth_waterlinebench_"))
    pack = REGION if pack_text is None else pack_text
    shutil.copy2(TMP / "pass-layer.js", d / "pass-layer.js")
    for _inst in sorted(TMP.glob("pass-inst-*.js")):
        shutil.copy2(_inst, d / _inst.name)
    (d / "pass-inst-waterline.js").write_text(pack, encoding="utf-8")
    record = json.loads((TMP / "config.json").read_text(encoding="utf-8"))
    record["pass"]["instruments"]["waterline"]["digest"] = hashlib.sha256(
        pack.encode("utf-8")).hexdigest()
    (d / "config.json").write_text(json.dumps(record), encoding="utf-8")
    shutil.copy2(MODULE, d / "waterline.js")
    (d / "photos").mkdir()
    for p in PHOTOS:
        shutil.copy2(p, d / "photos" / p.name)
    shutil.copy2(ROOT / "tests" / "fixture_pass_waterline.html", d / "index.html")
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
    SCORE_JSON = json.dumps(waterline_score())
    with serve(BENCH) as base:
        with Browser(width=VW, height=VH) as br:
            br.navigate(base + "/index.html")
            if not ready(br):
                for r in BROWSER_ROWS:
                    check(r, False, "the bench never came up: "
                         + br.evaluate("JSON.stringify(window.__errs||[])"))
            elif not js(br, "return !!window.__exPass.bench.manifest('waterline');"):
                why = js(br, "var e = window.__host.report().events.filter(function(x){"
                             "return x.name === 'manifest-refused';});"
                             "return e.length ? e[e.length - 1].why : null;")
                for r in BROWSER_ROWS:
                    check(r, False, "the host registered no «waterline» instrument: " + str(why))
            else:
                # ---- §8: the manifest, read off the registered instrument -----------------------
                m = js(br, "return window.__exPass.bench.manifest('waterline');")
                zoom = m["framings"]["0"]["coverCrop"]
                res = m["resources"]
                shape = (
                    m["id"] == "waterline" and m["api"] == 1 and m["arity"] == 2
                    and m["roles"] == ["disassembly", "mystery", "assembly"]
                    and m["levels"] == ["WORLD", "SURFACE"]
                    and m["cuts"] == ["band"]
                    and sorted(m["params"]) == ["depth", "lead", "line", "order", "settle",
                                                "swell", "tideCells"]
                    and len(m["handles"]) == 18
                    and m["handles"]["settle"]["def"] == 1
                    and m["handles"]["tideCells"]["def"] == 0.5
                    and all(set(h) >= {"min", "max", "def"} for h in m["handles"].values())
                    and m["neutrals"] == {"a": 0, "b": 1}
                    and m["doors"]["in"]["handle"] == "mix" and m["doors"]["in"]["value"] == 0
                    and m["doors"]["out"]["handle"] == "mix" and m["doors"]["out"]["value"] == 1
                    and sorted(m["framings"]) == ["0", "1"]
                    and m["framings"]["0"] == m["framings"]["1"]
                    and abs(zoom - ZOOM) < 1e-12
                    and m["camera"] == {"needs": "none", "authority": "stage"}
                    and m["coverage"]["writes"] is False
                    and len(m["passes"]) == 1 and len(m["passes"][0]["uniforms"]) == 20
                    and sorted(res) == ["lean", "rich", "standard"]
                    and all("bytesEstimate" in res[v] and res[v]["programs"] == 1
                            and res[v]["passes"] == 1 and res[v]["textureSlots"] == 2
                            for v in res)
                    and m["capabilities"] == ["webgl2"] and m["decline"]
                    and m["suits"]["reads"] == ["motifs.measured", "structure.horizon.y"]
                    and m["provenance"]["labPath"] == "lab/effects/waterline.js"
                    and m["provenance"]["commit"] == "60ef8f3"
                    and m["readiness"] == "production-ready"
                    and "waterline" in js(br, "return window.__host.report().registered;"))
                check(BROWSER_ROWS[0], shape,
                      f"eighteen handles, twenty uniforms in one pass, the crop {zoom} the "
                      f"counter-motion and the swell are paid for with, the cut «band», the two "
                      f"levels WORLD and SURFACE read off the module's own header, an alpha of a "
                      f"constant 1 (coverage.writes={m['coverage']['writes']}), resources for three "
                      f"tiers and the lab commit {m['provenance']['commit']}")

                br.evaluate("window.__clock(%r); 0" % CLOCK)
                br.sleep(0.9)

                # ---- the five poses: the host's frame beside the lab module's -------------------
                pairs = []
                for name, v in (("door-0", 0.0), ("q1", 0.25), ("mid", 0.5),
                                ("q3", 0.75), ("door-1", 1.0)):
                    br.evaluate("window.__mix(%r); 0" % v)
                    br.sleep(0.9)
                    br.evaluate("window.__hostDraw(); 0")
                    br.sleep(0.1)
                    br.evaluate("window.__show('host'); 0")
                    br.sleep(0.2)
                    ph = png(br, SHOTS / (name + "-host.png"))
                    br.evaluate("window.__show('module'); 0")
                    br.sleep(0.2)
                    pm = png(br, SHOTS / (name + "-module.png"))
                    pairs.append((name, ph, pm))

                shots = {n: h for n, h, _ in pairs}
                w = int(br.evaluate("String(window.__exPass.bench.make() && "
                                    "document.querySelector('canvas').width)"))
                h = int(br.evaluate("String(document.querySelector('canvas').height)"))
                towers = work_in_the_frame(BENCH / "photos" / "towers.jpg", w, h, zoom)
                glass = work_in_the_frame(BENCH / "photos" / "glassgrid.jpg", w, h, zoom)

                for i, (door, own, other, ownn, othern) in enumerate((
                        ("door-0", towers, glass, "towers.jpg", "glassgrid.jpg"),
                        ("door-1", glass, towers, "glassgrid.jpg", "towers.jpg"))):
                    a, amx = apart(shots[door], own)
                    check(BROWSER_ROWS[1 + i * 2], a <= SEAM_BAR,
                          f"{door} against {ownn}: mean {a:.4f} of 255 (threshold {SEAM_BAR}), "
                          f"worst channel {amx} — the water has drained out under the bottom edge, "
                          f"both contact shadows and the counter-motion are exactly nothing, and "
                          f"the travelling threshold stands a whole margin outside everything the "
                          f"field reads")
                    o, _ = apart(shots[door], other)
                    check(BROWSER_ROWS[2 + i * 2], o >= FAR,
                          f"{door} against {othern}: mean {o:.4f} of 255 (must exceed {FAR})")

                agree = [(name, ) + diff(ph, pm) for name, ph, pm in pairs]
                check(BROWSER_ROWS[5], all(mn <= SAME for _, mn, _ in agree),
                      "; ".join(f"{n}: mean {mn:.4f} of 255 (threshold {SAME}), worst channel {mx}"
                                for n, mn, mx in agree))

                # ---- §7: no empty frame, and the redraw the preserved buffer stood in for -------
                br.evaluate("window.__show('host'); 0")
                empties = []
                for at in (0.0, 0.15, 0.3, 0.5, 0.7, 0.85, 1.0):
                    js(br, "return window.__offer(%s, {clock: 1.5, progress: %r});"
                       % (SCORE_JSON, at))
                    br.sleep(0.5)
                    p = png(br, SHOTS / ("instant-%03d.png" % round(at * 100)))
                    empties.append((at, ) + standing(p))
                    br.evaluate("window.__cancel('instant sweep'); 0")
                    idle(br)
                check(BROWSER_ROWS[6],
                      all(d >= FAR and s >= SPREAD for _, d, s in empties),
                      "; ".join(f"at {at}: {d:.2f} from the background, spread {s:.2f}"
                                for at, d, s in empties)
                      + f" (bars: {FAR} and {SPREAD})")

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
                check(BROWSER_ROWS[7],
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
                check(BROWSER_ROWS[8], took["took"] and mn == 0.0 and mx == 0,
                      f"took={took['took']} two runs of one seeded score: mean {mn} worst channel {mx}")

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
                check(BROWSER_ROWS[9], same,
                      f"before={base_c['textures']}/{base_c['programs']}/{base_c['framebuffers']} "
                      f"after ten runs={after['textures']}/{after['programs']}/{after['framebuffers']} "
                      f"(textures/programmes/framebuffers)")

                # ---- the census against the declaration ------------------------------------------
                r = js(br, "return window.__report();")["resources"]
                check(BROWSER_ROWS[11],
                      r["declared"] and r["over"] is False
                      and r["granted"]["textures"] == r["declared"]["textures"]
                      and r["granted"]["framebuffers"] == r["declared"]["framebuffers"]
                      and r["granted"]["bytes"] == r["declared"]["bytesEstimate"],
                      f"declared={r['declared']} granted={r['granted']}")

                # ---- the two manifest refusals ---------------------------------------------------
                # THE STAND-IN `values` THESE TWO ROWS REGISTER WITH, and it has to answer EVERY
                # `frame:` name the manifest declares. The host learns which frame keys exist by
                # taking the keys of one call on the neutral pose (pass-layer.js:320-321) and walks
                # the uniforms in declared order, so a stub missing one key is refused at THAT name
                # and the row's own name is never reached — the second row below would then pass on
                # a refusal about the wrong uniform, which is a row proving nothing.
                NEUTRAL = ("{dial:0,line:1.04,lineA:0.5,lineB:0.5,way:0,tau:-0.05,lead:0.62,"
                           "spread:0.154,dep:1.2,swell:0.45,comb:0.45,open:0,off:0,guardE:0,"
                           "guardL:0,time:0,cells:[19,8],seamPts:1.5}")
                r = js(br, """
                  var m = JSON.parse(JSON.stringify(window.__exPass.bench.manifest('waterline')));
                  m.gl.preserveDrawingBuffer = true;
                  var ok = window.__exPass.bench.register({name:'waterline-preserve', manifest:m,
                      values:function(){return %s;},
                      fit:function(){return [1,1,0,0];},
                      prepare:function(){return {take:false};}, start:function(){}, frame:function(){}});
                  var evs = window.__host.report().events.filter(function(e){return e.name==='manifest-refused';});
                  return {ok: ok, why: evs.length ? evs[evs.length-1].why : null,
                          registered: window.__host.report().registered};
                """ % NEUTRAL)
                check(BROWSER_ROWS[12],
                      r["ok"] is False and r["why"] and "preserved" in r["why"]
                      and "waterline-preserve" not in r["registered"],
                      f"registered={r['ok']} why={r['why']}")

                r = js(br, """
                  var m = JSON.parse(JSON.stringify(window.__exPass.bench.manifest('waterline')));
                  m.passes[0].uniforms.push({name:'uPointer', type:'vec2', source:'pointer'});
                  var ok = window.__exPass.bench.register({name:'waterline-pointer', manifest:m,
                      values:function(){return %s;},
                      fit:function(){return [1,1,0,0];},
                      prepare:function(){return {take:false};}, start:function(){}, frame:function(){}});
                  var evs = window.__host.report().events.filter(function(e){return e.name==='manifest-refused';});
                  return {ok: ok, why: evs.length ? evs[evs.length-1].why : null,
                          registered: window.__host.report().registered};
                """ % NEUTRAL)
                check(BROWSER_ROWS[13],
                      r["ok"] is False and r["why"] and "uPointer" in r["why"]
                      and "cannot supply" in r["why"] and "waterline-pointer" not in r["registered"],
                      f"registered={r['ok']} why={r['why']}")

                # ---- the hardware, counted where each thing is made ------------------------------
                js(br, "return window.__offer(%s, {clock: 1.0, progress: 0.4});" % SCORE_JSON)
                br.sleep(0.6)
                cen = js(br, "return window.__report();")["census"]
                check(BROWSER_ROWS[14],
                      cen["canvases"] == 1 and cen["contexts"] == 1 and cen["textures"] == 2
                      and cen["passesLastFrame"] == 1 and cen["framebuffers"] == 0
                      and cen["preserveDrawingBuffer"] is False
                      and int(br.evaluate("String(document.querySelectorAll('canvas').length)")) == 2,
                      f"census={cen}; the second canvas on the page is the lab module's own, which "
                      f"is the road being compared against and no part of the host")

                # ---- the version header, through the host's own translator -----------------------
                r = js(br, """
                  var m = window.__exPass.bench.manifest('waterline');
                  var plain = window.__exPass.bench.es3(m.passes[0].frag, false);
                  var already = window.__exPass.bench.es3('#version 300 es\\n' + m.passes[0].frag, false);
                  var count = function (s) { return s.split('#version').length - 1; };
                  return {source: count(m.passes[0].frag), stamped: count(plain),
                          untouched: count(already), head: plain.slice(0, 15)};
                """)
                check(BROWSER_ROWS[15],
                      r["source"] == 0 and r["stamped"] == 1 and r["untouched"] == 1
                      and r["head"].startswith("#version 300 es"),
                      f"the module's own shader carries {r['source']} headers, the translator leaves "
                      f"it with {r['stamped']}, and a source that already carries one comes back "
                      f"with {r['untouched']}")

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
                check(BROWSER_ROWS[16],
                      took["took"] and mid["state"] == "running" and mid["curtains"][:1] == [True]
                      and end["state"] == "idle" and len(end["docks"]) == 1
                      and end["curtains"][-1] is False and "docked" in end["events"],
                      f"mid={mid} end={end}")

                cam = js(br, "var r = window.__report(); "
                             "return {camera: r.camera, rest: r.rest, handoffs: r.handoffs, "
                             "tol: r.camTolerances};")
                check(BROWSER_ROWS[17],
                      cam["camera"] and cam["camera"]["owner"] == "stage"
                      and cam["handoffs"] == []
                      and cam["rest"] and cam["rest"]["rested"] is True
                      and cam["rest"]["off"] <= cam["tol"]["rest"],
                      f"owner={cam['camera'] and cam['camera']['owner']} rest={cam['rest']} "
                      f"handoffs={cam['handoffs']} tolerances={cam['tol']} — the manifest asks for "
                      f"no camera, so the stage holds it for the whole pass")

                # ---- §4.4b: every handle reaches the picture -------------------------------------
                # A handle read back off the diagnostic surface proves the GRAPH evaluated it. It
                # says nothing about whether the instrument obeyed it. These runs differ by exactly
                # one handle each and are photographed, so a picture that did not move is a handle
                # the instrument is not reading. The bar is the project's own seam threshold read on
                # the WORST channel rather than on the mean: two of these handles — the two contact
                # shadows — move a band a few pixels deep by design, and a mean over the whole frame
                # would call a real movement nothing.
                br.evaluate("window.__show('host'); 0")
                MOVES = (("line", {"line": 1.0}), ("depth", {"depth": 1.0}),
                         ("swell", {"swell": 1.0}), ("lead", {"lead": 0.0}),
                         ("order", {"order": 1.0}), ("travel", {"travel": 0.0}),
                         ("settle", {"settle": 0.0}), ("tideCells", {"tideCells": 1.0}),
                         ("shade", {"shade": 0.0}), ("shadeEdge", {"shadeEdge": 0.0}),
                         ("shadeLine", {"shadeLine": 0.0}), ("comb", {"comb": 0.0}),
                         ("raw", {"raw": 1.0}), ("seamA", {"seamA": 0.85}),
                         ("seamB", {"seamB": 0.05}), ("seed", {"seed": 1.37}))
                shot = {}
                for name, extra in (("base", {}), ) + MOVES:
                    js(br, "return window.__offer(%s, {clock: 1.5, progress: 0.5});"
                       % json.dumps(waterline_score(**extra)))
                    br.sleep(0.7)
                    shot[name] = png(br, SHOTS / ("handle-" + name + ".png"))
                    br.evaluate("window.__cancel('handle row'); 0")
                    idle(br)
                moved = {k: diff(shot["base"], shot[k]) for k, _ in MOVES}
                check(BROWSER_ROWS[18],
                      all(mx > SEAM_BAR for _, mx in moved.values()),
                      "; ".join(f"{k} moves the frame by {mx} of 255 at its worst channel "
                                f"(mean {mn:.4f})" for k, (mn, mx) in moved.items())
                      + f"; the seam threshold is {SEAM_BAR}")

                # ---- THE DERIVATION, ON THE PICTURE ---------------------------------------------
                # The waterline is the departing work's own measured `seam_y` carried into the frame
                # through the seating the host applied. What it OUGHT to be here is computed at the
                # top of this file out of the measured seam and the published crop — the instrument
                # is never asked — and this row finds the line the frame actually drew.
                #
                # HOW THE LINE IS FOUND. The judges' `comb` channel changes the water and nothing
                # above it: it rides `water` in the shader, so above the line the two frames are the
                # same to the pixel. The topmost row that moves is therefore the waterline itself.
                #
                # WHERE ON THE DIAL. Between the module's own OPEN_IN and LINE_HOLD the water stands
                # fully open AND the line still rests on the departing work's own seam, and that is
                # the only stretch of the dial where this can be read at all. The mix that lands the
                # dial there is found by asking the instrument's own `values` — the dial is what the
                # measured curve makes of the hand, and this file does not re-derive that curve.
                lo, hi = 0.0, 1.0
                for _ in range(40):
                    m0 = 0.5 * (lo + hi)
                    dv = js(br, "return window.__values({mix: %r}).values.dial;" % m0)
                    if dv < 0.17:
                        lo = m0
                    else:
                        hi = m0
                at = 0.5 * (lo + hi)
                seen = js(br, "return window.__values({mix: %r});" % at)["values"]
                for cv in (1.0, 0.0):
                    js(br, "return window.__offer(%s, {clock: 3.0, progress: %r});"
                       % (json.dumps(waterline_score(comb=cv)), at))
                    br.sleep(0.8)
                    png(br, SHOTS / ("line-comb-%d.png" % int(cv * 10)))
                    br.evaluate("window.__cancel('line row'); 0")
                    idle(br)
                rows, hgt = rows_that_move(SHOTS / "line-comb-10.png", SHOTS / "line-comb-0.png")
                want_row = LINE_A * hgt
                top = rows[0] if rows else -1
                check(BROWSER_ROWS[20],
                      hgt > 0 and rows and top >= want_row - 2 and top <= want_row + 8
                      and abs(seen["line"] - LINE_A) < 1e-6 and seen["open"] == 1.0
                      and seen["way"] == 0.0,
                      f"the departing work's own measured seam is {SEAM_A} down the FILE; seated "
                      f"through the crop of {ZOOM} the frame puts it at {LINE_A:.6f}, which on a "
                      f"{hgt}-point buffer is row {want_row:.1f}. At a mix of {at:.4f} the dial "
                      f"stands at {seen['dial']:.4f} — the water fully open ({seen['open']}) and "
                      f"the line still resting on that seam ({seen['way']} of the way travelled) — "
                      f"and the topmost row of the frame that the `comb` channel moves is {top}. "
                      f"Above it the two frames are the same to the pixel, which is what makes the "
                      f"line findable at all; the instrument's own reading of the line is "
                      f"{seen['line']:.6f}")

                # ---- THE HINGE ------------------------------------------------------------------
                # Whatever the two seams are, the line crosses the frame's centre at the mark where
                # half the frame has changed hands. Read twice: with the measured curve out of the
                # way (`raw`), where the dial IS the hand and the mark is exactly the middle, and
                # with it standing, where the mark is wherever the curve puts the dial at 0.5.
                straight = js(br, "return window.__values({mix: 0.5, raw: 1}).values;")
                lo, hi = 0.0, 1.0
                for _ in range(40):
                    m0 = 0.5 * (lo + hi)
                    dv = js(br, "return window.__values({mix: %r}).values.dial;" % m0)
                    if dv < 0.5:
                        lo = m0
                    else:
                        hi = m0
                curved = js(br, "return window.__values({mix: %r});" % (0.5 * (lo + hi)))["values"]
                check(BROWSER_ROWS[21],
                      abs(straight["line"] - 0.5) < 1e-9 and abs(curved["line"] - 0.5) < 1e-6
                      and abs(straight["lineA"] - LINE_A) < 1e-9
                      and abs(straight["lineB"] - LINE_B) < 1e-9,
                      f"the two seams are seated at {LINE_A:.6f} and {LINE_B:.6f}, which are "
                      f"nowhere near the centre and are not symmetric about it. With the curves out "
                      f"of the way the line at the dial's own middle reads "
                      f"{straight['line']:.9f}; with the measured curve standing, the dial reaches "
                      f"0.5 at a mix of {0.5 * (lo + hi):.6f} and the line reads "
                      f"{curved['line']:.9f}. The travel is hinged at the middle so that the share "
                      f"of the way come there is exactly the share at which the line sits on 0.5")

                # ---- THE DOOR, READ ON THE BUFFER BEING DRAWN ------------------------------------
                # The rows above read every door on the frame the suite runs at. The shader samples
                # on the DRAWING BUFFER and the mask crosses over inside half the field's own slope
                # per buffer point, so the buffer is the grid that decides a door. This row reads
                # that crossover against the margin the threshold stands beyond the field, on the
                # real buffer and on two synthetic ones, and states where the two would meet.
                buf = js(br, "return window.__buffer();")
                real0 = js(br, "return window.__values({mix: 0, order: 1, lead: 0, "
                               "bufWidth: %d, bufHeight: %d}).values;" % (buf["w"], buf["h"]))
                real1 = js(br, "return window.__values({mix: 1, order: 1, lead: 0, "
                               "bufWidth: %d, bufHeight: %d}).values;" % (buf["w"], buf["h"]))
                tiny = js(br, "return window.__values({mix: 1, order: 1, lead: 0, "
                              "bufWidth: 390, bufHeight: 16}).values;")
                tinier = js(br, "return window.__values({mix: 1, order: 1, lead: 0, "
                                "bufWidth: 390, bufHeight: 15}).values;")
                away = js(br, "return window.__values({mix: 0.5, bufWidth: %d, bufHeight: %d})"
                              ".values;" % (buf["w"], buf["h"]))
                applied = js(br, "var s = window.__report().stack; "
                                 "return s && s.length ? s[0].applied : null;")
                check(BROWSER_ROWS[22],
                      real0["doorWhole"] is True and real1["doorWhole"] is True
                      and abs(real1["doorMargin"] - 0.05) < 1e-12
                      and real0["doorMargin"] >= real1["doorMargin"]
                      and real0["doorGrid"] == {"w": buf["w"], "h": buf["h"], "drawn": True}
                      and away["doorGrid"] is None and away["doorWhole"] is None
                      and tiny["doorWhole"] is True and tinier["doorWhole"] is False,
                      f"on the {buf['w']} x {buf['h']} buffer the frame is drawn on, with the tide "
                      f"order at its widest and the lead shut — the handles that make the field "
                      f"steepest — the mask crosses over inside {real1['doorCross']:.6f} of the "
                      f"field against a margin of {real1['doorMargin']:.6f} at the exit door and "
                      f"{real0['doorMargin']:.6f} at the entry door. The exit margin is exactly the "
                      f"module's own {0.05} in `reach`, whatever the handles are, because the "
                      f"ladder reaches 1 at the top of the frame. The two meet at a buffer 16 "
                      f"points tall (whole at 16: {tiny['doorWhole']}, not at 15: "
                      f"{tinier['doorWhole']}), which no browser hands, so both doors are whole by "
                      f"construction on every buffer this instrument can be drawn on and there is "
                      f"nothing to refuse. Away from a door nothing is read at all "
                      f"(grid {away['doorGrid']}). What the instrument published at the door it "
                      f"last drew: {applied}")

                # ---- A PAIR THAT MEASURED NO SEAM ----------------------------------------------
                # His words of 2026-08-18 09:51 and 10:15: any two photographs in the world get a
                # crossing, and a measurement only ranks which genre suits. A pair whose works carry
                # no measured waterline rests both handles on their own default, which is the frame's
                # own middle and the module's own fallback — and the crossing plays there.
                br.evaluate("window.__cancel('blind pair row'); 0")
                idle(br)
                br.evaluate("window.__hooks.docks.length = 0; 0")
                blind = js(br, "return window.__offer(%s, {});"
                           % json.dumps(waterline_score(seamA=0.5, seamB=0.5)))
                br.sleep(0.5)
                blind_mid = js(br, "return window.__report().state;")
                idle(br)
                blind_end = js(br, "return {state: window.__report().state, "
                                   "docks: window.__hooks.docks.slice()};")
                blind_v = js(br, "return window.__values({mix: 0.5, seamA: 0.5, seamB: 0.5})"
                                 ".values;")
                check(BROWSER_ROWS[23],
                      blind["took"] and blind_mid == "running" and blind_end["state"] == "idle"
                      and len(blind_end["docks"]) == 1
                      and abs(blind_v["lineA"] - 0.5) < 1e-12
                      and abs(blind_v["lineB"] - 0.5) < 1e-12
                      and abs(blind_v["line"] - 0.5) < 1e-12,
                      f"with both seams at the handles' own default the line stands at "
                      f"{blind_v['line']} — the frame's own middle — at every mark of the dial, and "
                      f"the pass runs to its landing all the same "
                      f"({blind_end['state']}, {len(blind_end['docks'])} dock). Nothing in this "
                      f"instrument turns such a pair away")

                errs = json.loads(br.evaluate("JSON.stringify(window.__errs||[])"))
                check(BROWSER_ROWS[10], not errs, "; ".join(errs)[:300])

                kept = sorted(p.name for p in SHOTS.glob("*.png"))
                check(BROWSER_ROWS[19],
                      len(kept) >= 30 and all((SHOTS / k).stat().st_size > 1000 for k in kept),
                      f"{len(kept)} captures under {SHOTS.relative_to(ROOT)}: the five poses on both "
                      f"roads, the seven sampled instants, the frame after a resize, the two seeded "
                      f"runs, the seventeen handle runs and the two frames the waterline is found "
                      f"between")

    shutil.rmtree(BENCH, ignore_errors=True)

    # ============================================================================================
    # THE RED-ON-BUG PROOFS. Each reverts ONE repair in the artifact the browser actually loads and
    # names what reddens. The pack served is changed and the host is re-stamped with the digest of
    # the bytes it is handed, which is what the build does; the file on disk is never touched, so no
    # working tree can be left changed by a proof.
    #
    # WHAT IS READ. The three numbers the two derivation rows above stand on, taken from the
    # instrument's own `values` on the same two poses those rows use: where the line stands at the
    # handle's own default, and where it stands at the dial's own middle. The picture rows above
    # bind those numbers to the frame; these rows bind them to the derivation.
    def read_three(br):
        lo, hi = 0.0, 1.0
        for _ in range(40):
            m0 = 0.5 * (lo + hi)
            if js(br, "return window.__values({mix: %r}).values.dial;" % m0) < 0.17:
                lo = m0
            else:
                hi = m0
        rest = js(br, "return window.__values({mix: %r}).values;" % (0.5 * (lo + hi)))
        mid = js(br, "return window.__values({mix: 0.5, raw: 1}).values;")
        return {"atSeam": rest["line"], "way": rest["way"], "open": rest["open"],
                "lineA": rest["lineA"], "atMiddle": mid["line"]}

    base_read = on_bench(read_three)

    BUGS = [
        (RED_ROWS[0],
         'var rest = curveOf("line", 0.5, st.raw);',
         'var rest = 0.5;',
         "atSeam",
         "the lift is read against the middle of the handle's RANGE instead of against the "
         "handle's own default, which is the state the module itself repaired"),
        (RED_ROWS[1],
         "return clamp(0.5 + (clamp(seam, 0, 1) - 0.5) / Math.max(fy, 1e-4), 0.06, 0.94);",
         "return clamp(clamp(seam, 0, 1), 0.06, 0.94);",
         "atSeam",
         "the measured seam is taken as a place in the FRAME instead of a place in the FILE "
         "carried through the seating the host applied"),
        (RED_ROWS[2],
         "var wMid = Math.abs(span) < 1e-4 ? 0.5 : clamp((mid - la) / span, 0.02, 0.98);",
         "var wMid = 0.5;",
         "atMiddle",
         "the travel is un-hinged: half the way is come at the dial's own middle whatever the two "
         "seams are"),
    ]
    for row, was, now, key, why in BUGS:
        want = LINE_A if key == "atSeam" else 0.5
        bug = REGION.replace(was, now, 1)
        bug_read = on_bench(read_three, pack_text=bug) if bug != REGION else None
        ok = (bug != REGION and base_read and bug_read
              and abs(base_read[key] - want) < 1e-6
              and abs(bug_read[key] - want) > 1e-3)
        check(row, ok,
              f"{why}. With the repair standing the instrument reads {key} at "
              f"{base_read and base_read[key]}, which is the {want:.6f} this file computed for "
              f"itself out of the measured seam {SEAM_A} and the published crop {ZOOM}. With the "
              f"repair reverted the same pose reads {bug_read and bug_read[key]}, off by "
              f"{abs((bug_read or {}).get(key, 0) - want):.6f} of the frame's own height — "
              f"{abs((bug_read or {}).get(key, 0) - want) * VH:.1f} points of the frame this suite "
              f"runs at")

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
