#!/usr/bin/env python3
"""PASS-API-V1 — the leaning instrument on the host's frame.
Run: python3 tests/test_pass_tilt.py

Root: his word of 2026-08-18 18:39 — «дозалей чтобы все эффекты были в арсенале, со всеми ручками».
lab/effects/tilt.js is carried across as engine/assets/pass-inst-tilt.js. docs/design/PASS-API-V1.md
§7 (GPU and resources), §8 (the manifest) and §9's conformance rows 7, 9, 10, 13, 14, 15, 16 and 22
are what this file makes real; the lifecycle rows stay in tests/test_pass_api.py and are untouched.

WHAT IS COMPARED, AND AGAINST WHAT.

  The doors. At the dial's two ends one whole work stands, upright and flat. Each is measured against
  ITS OWN FILE — the picture cover-fitted into the frame and pulled in by the headroom the
  counter-motion needs (the module's own CROP of 1.12, the number lab/data/module-contract-new.json
  records for this module's framing) — inside the project's seam threshold of 6 of 255.

  The five poses. The host's frame is compared against the LAB MODULE's own frame, on one pose both
  roads were driven by: the same dial, the same four params, the same die. Two roads of one frame,
  never two guesses at one. The five poses walk the dial from door to door, so the response curve and
  the whole travel of the lean are measured along their length rather than at the ends.

  The doors read on the buffer. The mask crosses over inside a band of the plane's rows one buffer
  point wide, and the front stands the module's own 0.03 beyond the plane's own edge, so the buffer's
  HEIGHT is what decides whether a door is whole. The rows state buffers either side of that and read
  what the instrument answers.

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
# The two photographs the material suite compares on; they live in the main worktree, which the
# immersive one does not copy. Either root is read only here.
PHOTOS = [Path("/Users/sashaabramovich/tlvphotos/lab/photos/towers.jpg"),
          Path("/Users/sashaabramovich/tlvphotos/lab/photos/glassgrid.jpg")]
MODULE = LAB / "effects" / "tilt.js"
SOURCE = ROOT / "engine" / "assets" / "pass-inst-tilt.js"

SITE_URL = "https://synth.example.com"
VW, VH = 390, 844          # the phone frame lab/carrier-check.py measures on
SEAM = 6.0                 # the project's seam threshold, 6 of 255 (TRANSITION-STAGE-V0 §1)
SAME = 1.5                 # two roads of one frame: the carrier check's own bar
FAR = 40.0                 # further than this from a file and it is a different work
# A frame that stands as a picture. The canvas's own background is one flat colour, so a drawn frame
# is far from it and carries a spread of its own. Both numbers are read off the capture.
BACKGROUND = (0x08, 0x08, 0x0a)
SPREAD = 10.0

# Captures are kept rather than swept, because §9 row 16 asks for evidence for every landed
# instrument and evidence that is deleted is no evidence.
SHOTS = ROOT / "tests" / "captures" / "pass-tilt"

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


# ---------------------------------------------------------------- the score this instrument plays
# AUTHORED HERE, and said to be authored here. lab/data/scores carries a template and a table for the
# woven instrument alone, so there is no per-pair score on file for this one. Everything below is
# either a number the module itself declares or a field the contract requires; nothing is measured in
# this file and nothing is invented as a measurement.
DIE = 4.91016            # the die lab/data/scores' own weave score carries, so both suites roll one
DURATION_MS = 3000
WITHIN_MS = 500


def tilt_score(pair_a="a", pair_b="b", **statics):
    """The score, with a track for every one of the ten handles (§4.4b).

    The four params rest at the module's own declared defaults (tilt.js:205-208): lean 0.72, horizon
    0.35, far-edge squeeze 0.55, front order 0.4. `columns` rests at the module's own pinned nine.
    The three judge channels rest where the module rests them — the shadow and the travel at 1, the
    coverage channel at nothing. `mix` reads the transaction's own progress.

    THERE IS NO `clock` TRACK because there is no clock handle: nothing in this module's picture moves
    with time (its own contract row says `clockMoves: false`), so the instrument publishes none.
    """
    P = {"tilt": 0.72, "horizon": 0.35, "squeeze": 0.55, "lead": 0.4, "columns": 9,
         "shade": 1, "travel": 1, "mask": 0, "seed": DIE}
    P.update(statics)
    nodes = {"mixDrive": {"source": "progress"}}
    tracks = {"mix": {"node": "mixDrive"}}
    for k, v in P.items():
        nodes[k + "Static"] = {"op": "static", "value": v}
        tracks[k] = {"node": k + "Static"}
    res = {v: {"textures": 0, "textureSlots": 2, "framebuffers": 0, "pingPong": 0, "programs": 1,
               "passes": 1, "bytesEstimate": 0, "variant": v}
           for v in ("lean", "standard", "rich")}
    return {
        "schema": 2,
        "intent": "the whole frame lies down into depth, its rows crowding toward the far edge, and "
                  "the second work stands on the same plane beyond the first with the line between "
                  "them riding forward to the eye until the frame is upright again "
                  "(lab/effects/tilt.js:1-19, its own header)",
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
            "id": "tilt-main",
            "instrument": {"id": "tilt", "api": 1},
            "voice": "letter",
            "roles": ["disassembly", "mystery", "assembly"],
            "levels": ["WORLD"],
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
        "quality": {v: {"renderScale": None, "cues": {"tilt-main": {"resources": res[v]}}}
                    for v in ("lean", "standard", "rich")},
        "provenance": {"source": "lab/effects/tilt.js's own declared defaults and constants",
                       "measuredAt": None, "by": "tests/test_pass_tilt.py"},
    }


# ---------------------------------------------------------------- bake once
build_site.SITE_CONFIG = dict(build_site.SITE_CONFIG)
build_site.SITE_CONFIG["pass"] = {"visualLayer": "pass", "diagnostics": "on"}

TMP = Path(tempfile.mkdtemp(prefix="synth_passtilt_"))
build_site.OUT = TMP
build_site.build(SITE_URL)
LAYER = (TMP / "pass-layer.js").read_text(encoding="utf-8")
# The instrument's own region of the BUILT file — the real artifact, comments stripped as it ships —
# which is what the ownership fence and every other string row below is read against. A row about the
# HOST reads LAYER; a row about this instrument's own mathematics reads REGION; a row about a reason
# the port WROTE DOWN reads SOURCE_TEXT, since the build strips comments out of what ships.
REGION = (TMP / "pass-inst-tilt.js").read_text(encoding="utf-8")
SOURCE_TEXT = SOURCE.read_text(encoding="utf-8")
LABTXT = MODULE.read_text(encoding="utf-8") if MODULE.exists() else ""

# ---------------------------------------------------------------- string rows

OWNED = ["createElement", "getContext", "requestAnimationFrame", "addEventListener",
         "performance.now", "Date.now", "new Image", "setTimeout", "setInterval"]
held = [s for s in OWNED if s in REGION]
check("PASS-TILT the instrument creates no context, no canvas, no loop and no listener",
      not held,
      "§1.2's fence, read against the instrument's own region of the file: none of the nine ways of "
      "owning hardware appears there, so the module's canvas, its WebGL 1 context, its frame loop "
      "and its resize listener all stayed in the lab"
      if not held else "the instrument's region holds " + ", ".join(held))

HANDLES = ["mix", "tilt", "horizon", "squeeze", "lead", "columns", "seed", "shade", "travel", "mask", "presence"]
check("PASS-TILT every handle the instrument publishes is a handle a score can drive",
      all(("%s: { min" % h) in REGION for h in HANDLES),
      "§4.4b: ten handles — the dial, the module's own four params, the one constant the port "
      "publishes (the column count), the score's die and the three judge channels")

# THE CLOCK HANDLE THAT IS NOT THERE, and the module's own record for it. This is a handle DROPPED
# rather than carried, so the row states both halves: nothing in the instrument reads a second, and
# the module's own contract row says its picture does not move with one.
LAB_FRAG = (re.search(r"var FRAG = \[(.*?)\]\.join", LABTXT, re.S) or ["", ""])[1]
check("PASS-TILT no clock handle is published, and the module's own record is why",
      "clock: { min" not in REGION and "handle:clock" not in REGION
      and 'source: "seconds"' not in REGION
      and "clockMoves: false" in SOURCE_TEXT
      and "extTime" in LABTXT and "uTime" not in LAB_FRAG and "uClock" not in LAB_FRAG,
      "the module takes a second through onParam('clock', …) and accumulates one in its own frame "
      "loop, and no uniform of its shader ever reads it — its `values()` is a pure function of the "
      "hand, which is what lab/data/module-contract-new.json states in one word as `clockMoves: "
      "false`. A handle a score can walk without moving the picture is noise in the score, so none "
      "is published and the row that every handle reaches the picture stays honest")

check("PASS-TILT the manifest leaves the drawing buffer unpreserved",
      "gl: { preserveDrawingBuffer: false }" in REGION,
      "the module asks its own context for a preserved buffer (tilt.js:242) and §7 refuses a "
      "manifest that asks for it; the redraw it stood in for is the host's own frame loop")

check("PASS-TILT the shader carries no version header of its own",
      "#version" not in REGION and "#version" not in LABTXT,
      "so the host's translator stamps the one header this shader needs and no second one arrives")

# The response curve, read out of the lab module and out of the built file. A port that re-derived it
# would differ here by a digit.
CURVE = [("FEEL_D0 = 0.05", "the dead band at either end, the module's own and its contract row's"),
         ("FEEL_C = 0.4", "the knee, at four tenths of one half"),
         ("FEEL_K1 = -0.9", "the exponent below the knee"),
         ("FEEL_K2 = 1.5", "and above it")]
missing_curve = ([c for c, _ in CURVE if c not in LABTXT]
                 + [c for c, _ in CURVE if c not in REGION])
check("PASS-TILT the response curve is carried digit for digit out of the lab module",
      not missing_curve
      and "(Math.exp(k * x) - 1) / (Math.exp(k) - 1)" in LABTXT
      and "(Math.exp(k * x) - 1) / (Math.exp(k) - 1)" in REGION,
      "; ".join("%s — %s" % (c, why) for c, why in CURVE) if not missing_curve
      else "these differ: " + ", ".join(missing_curve))

# Each constant as the LAB module spells it and as the PORT spells it. The two are the same string
# everywhere but one: the front's overtravel is a bare literal in the module and a NAMED constant in
# the port, because the door reading holds its own footprint against that very number and a number
# read in two places has to have one home.
CONSTANTS = [("TILT_MAX = 35", "TILT_MAX = 35",
              "the lean at its fullest, in degrees, at mid-passage"),
             ("CAM_FAR = 9.0", "CAM_FAR = 9.0",
              "the camera's far stand, in frame half-heights: the lean is nearly a shear"),
             ("CAM_NEAR = 2.6", "CAM_NEAR = 2.6",
              "and its near one, where the far rows crowd by one over the depth"),
             ("AMP = 0.05", "AMP = 0.05", "how far the counter-motion pushes the frame coordinate"),
             ("CROP = 1 + 2 * AMP + 0.02", "CROP = 1 + 2 * AMP + 0.02",
              "the standing crop, which is that push at both ends and a hair — the 1.12 the "
              "module's contract row records for its framing"),
             ("COLS = 9", "COLS = 9", "the columns carrying their own moment along the front"),
             ("clamp(P.lead, 0, 1) * 0.8", "clamp(num(st.lead, 0), 0, 1) * 0.8",
              "eight tenths of the order handle reaches a sixth of the plane"),
             ("0.34 * uGuard", "0.34 * uGuard", "the contact shadow at the front"),
             ("exp(-max(-d, 0.0) / 6.0)", "exp(-max(-d, 0.0) / 6.0)",
              "and how it decays into the far work"),
             ("smoothstep(0, 0.09, d) * smoothstep(1, 0.91, d)",
              "smoothstep(0, 0.09, d) * smoothstep(1, 0.91, d)",
              "the shadow's own window, gone at both doors"),
             ("1 + spread * 0.5 + 0.03", "var MARGIN = 0.03;",
              "the front travels 0.03 past the plane's own edge with the raggedness already inside "
              "its reach, named MARGIN in the port because the door reading is held against it")]
missing_const = ([c for c, _, _ in CONSTANTS if c not in LABTXT]
                 + [c for _, c, _ in CONSTANTS if c not in REGION]
                 + ([] if "1 + spread * 0.5 + MARGIN" in REGION else ["1 + spread * 0.5 + MARGIN"]))
check("PASS-TILT every constant stands at the number the lab module gives it",
      not missing_const,
      "; ".join("%s — %s" % (c, why) for c, _, why in CONSTANTS) if not missing_const
      else "these differ: " + ", ".join(missing_const))

# THE PINNED-NUMBER SWEEP. His 19:13 word lifted to the class at 19:21 — every geometric and temporal
# parameter derives from the work's own measured structure and names the measurement it reads — with
# his 15:13 word as the other half: a constant a record could have set is a static transition. So the
# instrument owes, for every number it still pins, the reason it is not a handle.
#
# THIS ROW IS NOT ANCHORED ON A COMMENT'S EXISTENCE, which would pass vacuously. It reads the
# instrument's own DECLARATIONS — every named constant the built artifact actually carries — and
# holds that set against the list the file reasons about, so a number typed into the file tomorrow
# without a reason reds this. Beside it, the four pinned numbers that bound a handle's own range are
# read where a COMPOSER can see them: on the handle's `applied` block and in `framings`, not in prose.
PINNED = {"TILT_MAX", "CAM_FAR", "CAM_NEAR", "AMP", "CROP", "COLS", "COLS_MIN", "COLS_MAX",
          "MARGIN", "ZOOM_CAP", "FEEL_D0", "FEEL_C", "FEEL_K1", "FEEL_K2"}
declared_const = set(re.findall(r"\b([A-Z][A-Z0-9_]{2,})\s*=\s*[-\d(]", REGION))
PINNED_BLOCK = (SOURCE_TEXT.split("WHAT STAYS PINNED, AND WHY EACH ONE DOES")[-1]
                .split("function fit(")[0])
unreasoned = sorted(n for n in declared_const if not re.search(r"\b%s\b" % n, PINNED_BLOCK))
published = ("degreesAtMidPassageWhenWhole: TILT_MAX" in REGION
             and "halfHeightsAtNothing: CAM_FAR, halfHeightsAtWhole: CAM_NEAR" in REGION
             and "frameUnitsAtMidPassage: AMP" in REGION
             and 'framings: { "0": { coverCrop: CROP }, "1": { coverCrop: CROP } }' in REGION
             and "columns: { min: COLS_MIN, max: COLS_MAX, def: COLS" in REGION)
check("PASS-TILT every number the instrument still pins carries the reason it is not a handle",
      declared_const == PINNED and not unreasoned and published,
      "fourteen named constants stand in the built artifact and every one of them is reasoned about "
      "by name. ONE of the module's constants became a handle — COLS, the nine columns the front "
      "breaks into, which is a count of divisions across the frame and the one thing here a work "
      "record measures. The rest are a handle's own published RANGE (CAM_FAR/CAM_NEAR on `squeeze`, "
      "AMP on `travel`, and CROP in `framings`, each read here where a composer sees it rather than "
      "in prose), the door law's own slack (MARGIN), a stop that never fires (ZOOM_CAP), the "
      "response curve measured on the module rather than on a pair (the four FEEL numbers), or the "
      "port's own two (COLS_MIN/COLS_MAX). TILT_MAX stays pinned because the module measured ONE "
      "point of that axis and no second one, so a ceiling handle would need a number nobody "
      "measured and a ceiling bounded at the measured point is `tilt` under a second name — and the "
      "reading behind it, the pair's own repeat, already reaches the picture through `squeeze`"
      if declared_const == PINNED and not unreasoned and published
      else "constants declared but never reasoned about: %s; declared set %s against the reasoned "
           "set %s; published on the handles: %s"
           % (unreasoned, sorted(declared_const), sorted(PINNED), published))

# THE MATRIX THE HOST CANNOT BIND, AND THE ROWS IT TRAVELS AS. §7's type vocabulary has no matrix, so
# the module's one mat3 uniform is carried as its three rows and the shader rebuilds it. The row reads
# the rebuild itself, because the footprint two lines below it names elements OF THAT MATRIX and a
# transposed rebuild would draw a different picture at every leaning pose.
check("PASS-TILT the plane's inverse travels as three rows and the shader rebuilds the module's own matrix",
      "uniform mat3 uInv;" in LABTXT
      and "mat3 uInv = mat3(uInv0.x, uInv1.x, uInv2.x," in REGION
      and "uInv0.y, uInv1.y, uInv2.y," in REGION
      and "uInv0.z, uInv1.z, uInv2.z);" in REGION
      and "uInv * vec3(sp, 1.0)" in LABTXT and "uInv * vec3(sp, 1.0)" in REGION
      and "(uInv[1].y * q.z - q.y * uInv[2].y)" in LABTXT
      and "(uInv[1].y * q.z - q.y * uInv[2].y)" in REGION,
      "GLSL's mat3 constructor takes its nine floats column by column and the module uploaded "
      "exactly these nine in exactly this order, so `uInv` inside the shader is the matrix the "
      "module bound — down to which element each of uInv[1] and uInv[2] names, which the pixel's own "
      "footprint reads")

check("PASS-TILT the instrument declares what it cuts on, and it is the strip and the field",
      'cuts: ["strip", "field"]' in REGION
      and "the handover front travels ROW BY ROW" in SOURCE_TEXT
      and "one surface carrying both works at once" in SOURCE_TEXT,
      "the front is a row of the plane travelling toward the eye, which is a strip cut and the same "
      "kind the composer's KIND_OF_MEASURE reads out of a banding pivot; and the plane itself is one "
      "surface carrying both works, so the whole frame is the element — the field kind the "
      "double-exposure instrument declares")

# WHAT A PAIR MUST READ IS WHAT A PAIR DOES READ. His words of 2026-08-18 09:51, 09:53 and 10:15: a
# measurement ranks which genre suits and never admits or rejects, and a reading of a PAIR carries no
# direction. The row therefore holds every floor OUT of the file and holds the `suits` block IN.
SUITS_BLOCK = (re.search(r"suits: \{.*?readiness:", REGION, re.S) or [""])[0]
check("PASS-TILT the instrument declares what it READS of a pair, and no floor and no direction",
      '"structure.polar.tunnel"' in REGION and '"structure.horizon.y"' in REGION
      and "asks:" not in REGION and "floor" not in SUITS_BLOCK
      and "minimum" not in SUITS_BLOCK and "threshold" not in SUITS_BLOCK
      and "the weaker of the two corridor" in SUITS_BLOCK
      and "crosses on it" in SUITS_BLOCK
      and "arriving" not in SUITS_BLOCK and "departing" not in SUITS_BLOCK
      and not re.search(r"\d", SUITS_BLOCK),
      "the whole frame is laid down as one plane going away into depth, so what it suits is a pair "
      "with depth to be revealed: the weaker of the two corridor readings is the fit, raised where "
      "both works stand a measured horizon of their own for the plane to turn about. A pair that "
      "reads no depth at all still crosses on it — the block carries no floor, no minimum, no "
      "threshold and no number at all, and the arithmetic lives in the composer's own "
      "INSTRUMENT_SUITS, which is the one place holding both work records")

# THE CARRIER HALF THAT DID NOT CROSS. The lab module's other face takes a canvas another module is
# drawing on and re-reads it every frame. This engine hands an instrument two decoded works and no
# second module's canvas, so that half cannot cross; the row asks that the file SAY so rather than
# drop it quietly or invent a substitute for it.
check("PASS-TILT the carrier half that could not cross is named in the file, with its reason",
      "THE CARRIER HALF DID NOT CROSS" in SOURCE_TEXT
      and "no second instrument's canvas" in SOURCE_TEXT
      and "carries the plain photographs of ctx.images" in SOURCE_TEXT
      and "ctx.sources" in LABTXT and "f.live" in LABTXT,
      "the module's own header names both roads and this port took the second: the module handed no "
      "source carries the plain photographs of ctx.images, «which is the same module with nothing "
      "playing on it». What is lost is exactly the leaning of a MOVING picture, and it is written "
      "into the file rather than left as a silence")

# EVERY GEOMETRIC HANDLE NAMES THE MEASUREMENT OF THE PHOTOGRAPH IT READS. His 19:13 word, lifted to
# the class at 19:21 — and where no measurement honestly stands behind a handle, the file says so
# rather than filling it with the nearest number to hand.
check("PASS-TILT every geometric handle publishes the measurement it reads, or says there is none",
      'reads: "structure.polar.tunnel' in REGION
      and 'reads: "structure.horizon.y' in REGION
      and "texture.spectralPeriodPx over structure.frameSide" in REGION
      and "the strip element sets" in REGION
      and "reads: null" in REGION
      and "How ragged a handover should read" in SOURCE_TEXT,
      "the LEAN reads structure.polar.tunnel, how strongly a work already reads as a corridor; the "
      "AXIS reads structure.horizon.y, the work's own measured horizon, which is the line the plane "
      "should turn about; the CROWDING reads texture.spectralPeriodPx over structure.frameSide, the "
      "repeat that decides how far the far rows may crowd before they stop resolving; the COLUMN "
      "COUNT reads the strip element sets. The front's own ORDER reads nothing — no measurement in a "
      "work record says how ragged a handover should be, and the handle says `reads: null` rather "
      "than naming a number nobody measured")

check("PASS-TILT the host binds uniforms by declared name, never by position or a written list",
      "getUniformLocation(p, u.name)" in LAYER and "gl.uniform1f(U.uFront" not in LAYER
      and "gl.uniform1f(U.uZoom" not in LAYER,
      "this instrument's sixteen uniforms include three the lab carrier's own fixed list never "
      "held; the host reads the manifest")

# Every uniform the manifest declares is a name the shader actually spells, and the other way about.
declared = set(re.findall(r'\{ name: "(u\w+)", type:', REGION))
spelled = set(re.findall(r'uniform \w+ (u\w+);', REGION))
check("PASS-TILT the manifest's declared names and the shader's own names are one set",
      declared == spelled,
      f"{len(declared)} declared, {len(spelled)} spelled; "
      f"declared only: {sorted(declared - spelled)}; spelled only: {sorted(spelled - declared)}")

# ---------------------------------------------------------------- browser rows

BROWSER_ROWS = [
    "PASS-TILT §8     · the manifest carries every field the contract names, in its shape",
    "PASS-TILT the level is WORLD, and the miracle that declaration spends is named",
    "PASS-TILT row 7  · door 0 stands the departing work, measured against its own file",
    "PASS-TILT row 7  · door 0 carries no trace of the arriving work",
    "PASS-TILT row 7  · door 1 stands the arriving work, measured against its own file",
    "PASS-TILT row 7  · door 1 carries no trace of the departing work",
    "PASS-TILT the host's frame and the lab module's frame agree at all five poses",
    "PASS-TILT §7     · no empty frame at any sampled instant of the pass",
    "PASS-TILT §7     · the frame after a change of viewport is drawn, not a kept buffer",
    "PASS-TILT row 10 · a seeded run repeats to the pixel",
    "PASS-TILT row 14 · textures, programmes and framebuffers return to their baseline after ten runs",
    "PASS-TILT row 15 · the console stays clean",
    "PASS-TILT row 22 · the census shows granted against declared, and neither overruns",
    "PASS-TILT §7     · a manifest asking for a preserved drawing buffer is refused, with its reason",
    "PASS-TILT §7     · a uniform bound to a name the shader lacks is refused, with its reason",
    "PASS-TILT §7     · one canvas, one context, two source textures, one pass a frame",
    "PASS-TILT §7     · a shader already at GLSL ES 3.00 receives no second version header",
    "PASS-TILT the real transaction road: curtain up, one pass drawn, exactly one dock at the end",
    "PASS-TILT row 9  · one camera authority through a real pass, and the pose rests on the arrival",
    "PASS-TILT §4.4b  · every published handle reaches the PICTURE",
    "PASS-TILT row 16 · the captures are kept as evidence",
    "PASS-TILT the door is read on the DRAWING BUFFER, and the column count applied is published",
    "PASS-TILT a door the judges' channel opens is refused on the real road, and the visitor still lands",
]

RED_ROWS = [
    "PASS-TILT red-on-bug · the door reading removed: a door the law cannot hold is drawn",
    "PASS-TILT red-on-bug · the plane's inverse rebuilt row by row: the two roads part company",
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
    """The work as the instrument seats it: cover-fit, then the centre crop the counter-motion is
    paid for with (the module's own CROP). The very same construction lab/carrier-check.py uses, so
    the two checks judge a door the same way."""
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
    """The bench's own served root: the BUILT pass-layer.js and the built instrument files (the real
    artifacts, namespace applied and comments stripped), the site's own settings record, the lab
    module unchanged, the two photographs, and the page that stands the two roads of one frame side
    by side.

    A row proving a rule reds hands over a CHANGED instrument file and writes the site's own record
    with the digest of the bytes actually served, which is what the build does. The source file on
    disk is never touched, so nothing has to be restored and no working tree can be left changed by a
    red-on-bug proof."""
    d = Path(tempfile.mkdtemp(prefix="synth_tiltbench_"))
    pack = REGION if pack_text is None else pack_text
    shutil.copy2(TMP / "pass-layer.js", d / "pass-layer.js")
    for _inst in sorted(TMP.glob("pass-inst-*.js")):
        shutil.copy2(_inst, d / _inst.name)
    (d / "pass-inst-tilt.js").write_text(pack, encoding="utf-8")
    record = json.loads((TMP / "config.json").read_text(encoding="utf-8"))
    record["pass"]["instruments"]["tilt"]["digest"] = hashlib.sha256(
        pack.encode("utf-8")).hexdigest()
    (d / "config.json").write_text(json.dumps(record), encoding="utf-8")
    shutil.copy2(MODULE, d / "tilt.js")
    (d / "photos").mkdir()
    for p in PHOTOS:
        shutil.copy2(p, d / "photos" / p.name)
    shutil.copy2(ROOT / "tests" / "fixture_pass_tilt.html", d / "index.html")
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
    SCORE_JSON = json.dumps(tilt_score())
    with serve(BENCH) as base:
        with Browser(width=VW, height=VH) as br:
            br.navigate(base + "/index.html")
            if not ready(br):
                for r in BROWSER_ROWS:
                    check(r, False, "the bench never came up: "
                         + br.evaluate("JSON.stringify(window.__errs||[])"))
            # An instrument the host refuses at registration draws nothing, so every row below it
            # would read as a crash. It reads as what it is instead: the whole set red, with the
            # host's own reason for the refusal.
            elif not js(br, "return !!window.__exPass.bench.manifest('tilt');"):
                why = js(br, "var e = window.__host.report().events.filter(function(x){"
                             "return x.name === 'manifest-refused';});"
                             "return e.length ? e[e.length - 1].why : null;")
                for r in BROWSER_ROWS:
                    check(r, False, "the host registered no «tilt» instrument: " + str(why))
            else:
                # ---- §8: the manifest, read off the registered instrument -----------------------
                m = js(br, "return window.__exPass.bench.manifest('tilt');")
                crop = m["framings"]["0"]["coverCrop"]
                res = m["resources"]
                need = ["id", "api", "arity", "roles", "levels", "cuts", "suits", "params",
                        "handles", "neutrals", "doors", "framings", "drivers", "camera", "gl",
                        "coverage", "passes", "resources", "capabilities", "decline", "provenance",
                        "readiness"]
                shape = (
                    all(k in m for k in need)
                    and m["id"] == "tilt" and m["api"] == 1 and m["arity"] == 2
                    and m["roles"] == ["disassembly", "mystery", "assembly"]
                    and m["cuts"] == ["strip", "field"]
                    and sorted(m["params"]) == ["horizon", "lead", "squeeze", "tilt"]
                    and len(m["handles"]) == 11
                    and sorted(m["handles"]) == sorted(HANDLES)
                    and all(set(h) >= {"min", "max", "def"} for h in m["handles"].values())
                    and m["neutrals"] == {"a": 0, "b": 1}
                    and m["doors"]["in"]["handle"] == "mix" and m["doors"]["in"]["value"] == 0
                    and m["doors"]["out"]["handle"] == "mix" and m["doors"]["out"]["value"] == 1
                    and sorted(m["framings"]) == ["0", "1"]
                    and m["framings"]["0"] == m["framings"]["1"]
                    and abs(crop - 1.12) < 1e-12
                    and m["camera"] == {"needs": "none", "authority": "stage"}
                    and m["gl"] == {"preserveDrawingBuffer": False}
                    and m["coverage"]["writes"] is True and m["coverage"]["how"]
                    and len(m["passes"]) == 1 and len(m["passes"][0]["uniforms"]) == 17
                    and sorted(res) == ["lean", "rich", "standard"]
                    and all("bytesEstimate" in res[v] and res[v]["programs"] == 1
                            and res[v]["passes"] == 1 and res[v]["textureSlots"] == 2
                            for v in res)
                    and m["capabilities"] == ["webgl2"] and m["decline"]
                    and m["provenance"]["labPath"] == "lab/effects/tilt.js"
                    and m["provenance"]["commit"] == "80bc046"
                    and m["readiness"] == "production-ready"
                    and "tilt" in js(br, "return window.__host.report().registered;"))
                check(BROWSER_ROWS[0], shape,
                      f"ten handles, sixteen uniforms in one pass, cuts on {m.get('cuts')}, both "
                      f"doors at a cover crop of {crop} — the counter-motion's own headroom, and the "
                      f"lean paid for by the camera rather than by a standing crop — resources "
                      f"declared for three tiers, and a coverage block reading "
                      f"«{m['coverage']['how']}»")

                # ---- the level, and the miracle it spends ---------------------------------------
                check(BROWSER_ROWS[1],
                      m["levels"] == ["WORLD"]
                      and "spendsTheMiracle" in SOURCE_TEXT
                      and "consumes the slot" in SOURCE_TEXT,
                      f"levels={m['levels']}, carried from lab/data/module-contract-new.json's own "
                      f"`tilt` row rather than derived. The composer's `spendsTheMiracle` reads this "
                      f"very line rather than any list of names, so declaring it has a price the "
                      f"file states: this instrument spends the crossing's one miracle, it never "
                      f"stacks, and a role given no miracle cannot be carried by it at all — which "
                      f"is right for a module whose whole act is the space the photographs live in "
                      f"lying down")

                # ---- the five poses: the host's frame beside the lab module's -------------------
                pairs = []
                for name, v in (("door-0", 0.0), ("q1", 0.25), ("mid", 0.5),
                                ("q3", 0.75), ("door-1", 1.0)):
                    br.evaluate("window.__mix(%r); 0" % v)
                    br.sleep(0.9)
                    br.evaluate("window.__hostDraw(); 0")
                    br.sleep(0.1)
                    br.evaluate("window.__show('host'); 0")
                    br.sleep(0.25)
                    ph = png(br, SHOTS / (name + "-host.png"))
                    br.evaluate("window.__show('module'); 0")
                    br.sleep(0.25)
                    pm = png(br, SHOTS / (name + "-module.png"))
                    pairs.append((name, ph, pm))

                shots = {n: h for n, h, _ in pairs}
                buf = js(br, "return window.__buffer();")
                w, h = int(buf[0]), int(buf[1])
                towers = work_in_the_frame(BENCH / "photos" / "towers.jpg", w, h, crop)
                glass = work_in_the_frame(BENCH / "photos" / "glassgrid.jpg", w, h, crop)

                for i, (door, own, other, ownn, othern) in enumerate((
                        ("door-0", towers, glass, "towers.jpg", "glassgrid.jpg"),
                        ("door-1", glass, towers, "glassgrid.jpg", "towers.jpg"))):
                    a, amx = apart(shots[door], own)
                    check(BROWSER_ROWS[2 + i * 2], a <= SEAM,
                          f"{door} against {ownn}: mean {a:.4f} of 255 (threshold {SEAM}), worst "
                          f"channel {amx} — the plane is flat, the camera's push-in is exactly 1 and "
                          f"the front stands beyond the plane's own edge, so the door is the source "
                          f"cover-fit and cropped by {crop} and nothing else")
                    o, _ = apart(shots[door], other)
                    check(BROWSER_ROWS[3 + i * 2], o >= FAR,
                          f"{door} against {othern}: mean {o:.4f} of 255 (must exceed {FAR})")

                agree = [(name, ) + diff(ph, pm) for name, ph, pm in pairs]
                check(BROWSER_ROWS[6], all(mn <= SAME for _, mn, _ in agree),
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
                check(BROWSER_ROWS[7],
                      all(d >= FAR and s >= SPREAD for _, d, s in empties),
                      "; ".join(f"at {at}: {d:.2f} from the background, spread {s:.2f}"
                                for at, d, s in empties)
                      + f" (bars: {FAR} and {SPREAD})")

                # The frame is redrawn at the new size rather than handed back from a kept buffer.
                js(br, "return window.__offer(%s, {clock: 1.5, progress: 0.5});" % SCORE_JSON)
                br.sleep(0.5)
                br.set_viewport(VW - 80, VH - 120)
                br.sleep(0.6)
                p = png(br, SHOTS / "after-resize.png")
                sized = js(br, "return {w: window.__buffer()[0], "
                               "buffer: window.__report().census.buffer, "
                               "pdb: window.__report().census.preserveDrawingBuffer};")
                d, s = standing(p)
                br.evaluate("window.__cancel('resize row'); 0")
                idle(br)
                br.set_viewport(VW, VH)
                br.sleep(0.4)
                check(BROWSER_ROWS[8],
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
                check(BROWSER_ROWS[9], took["took"] and mn == 0.0 and mx == 0,
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
                check(BROWSER_ROWS[10], same,
                      f"before={base_c['textures']}/{base_c['programs']}/{base_c['framebuffers']} "
                      f"after ten runs={after['textures']}/{after['programs']}/{after['framebuffers']} "
                      f"(textures/programmes/framebuffers); the programme cache holds one entry per "
                      f"branch and outlives every transaction")

                errs = json.loads(br.evaluate("JSON.stringify(window.__errs||[])"))
                check(BROWSER_ROWS[11], not errs, "; ".join(errs)[:200])

                # ---- the census against the declaration ------------------------------------------
                r = js(br, "return window.__report();")["resources"]
                check(BROWSER_ROWS[12],
                      r["declared"] and r["over"] is False
                      and r["granted"]["textures"] == r["declared"]["textures"]
                      and r["granted"]["framebuffers"] == r["declared"]["framebuffers"]
                      and r["granted"]["bytes"] == r["declared"]["bytesEstimate"],
                      f"declared={r['declared']} granted={r['granted']}")

                # ---- the two manifest refusals ---------------------------------------------------
                STUB = ("values:function(){return {inv0:[1,0,0,0],inv1:[0,1,0,0],inv2:[0,0,1,0],"
                        "zoom:1,front:1,spread:0,cols:9,off:0,guard:0};},"
                        "fit:function(){return [1,1,0,0];},"
                        "prepare:function(){return {take:false};}, start:function(){}, "
                        "frame:function(){}")
                r = js(br, """
                  var m = JSON.parse(JSON.stringify(window.__exPass.bench.manifest('tilt')));
                  m.gl.preserveDrawingBuffer = true;
                  var ok = window.__exPass.bench.register({name:'tilt-preserve', manifest:m, %s});
                  var evs = window.__host.report().events.filter(function(e){return e.name==='manifest-refused';});
                  return {ok: ok, why: evs.length ? evs[evs.length-1].why : null,
                          registered: window.__host.report().registered};
                """ % STUB)
                check(BROWSER_ROWS[13],
                      r["ok"] is False and r["why"] and "preserved" in r["why"]
                      and "tilt-preserve" not in r["registered"],
                      f"registered={r['ok']} why={r['why']}")

                r = js(br, """
                  var m = JSON.parse(JSON.stringify(window.__exPass.bench.manifest('tilt')));
                  m.passes[0].uniforms.push({name:'uPointer', type:'vec2', source:'pointer'});
                  var ok = window.__exPass.bench.register({name:'tilt-pointer', manifest:m, %s});
                  var evs = window.__host.report().events.filter(function(e){return e.name==='manifest-refused';});
                  return {ok: ok, why: evs.length ? evs[evs.length-1].why : null,
                          registered: window.__host.report().registered};
                """ % STUB)
                check(BROWSER_ROWS[14],
                      r["ok"] is False and r["why"] and "uPointer" in r["why"]
                      and "cannot supply" in r["why"] and "tilt-pointer" not in r["registered"],
                      f"registered={r['ok']} why={r['why']}")

                # ---- the hardware, counted where each thing is made ------------------------------
                js(br, "return window.__offer(%s, {clock: 1.0, progress: 0.4});" % SCORE_JSON)
                br.sleep(0.6)
                cen = js(br, "return window.__report();")["census"]
                check(BROWSER_ROWS[15],
                      cen["canvases"] == 1 and cen["contexts"] == 1 and cen["textures"] == 2
                      and cen["passesLastFrame"] == 1 and cen["framebuffers"] == 0
                      and cen["preserveDrawingBuffer"] is False
                      and int(br.evaluate("String(document.querySelectorAll('canvas').length)")) == 2,
                      f"census={cen}; the second canvas on the page is the lab module's own, which "
                      f"is the road being compared against and no part of the host")

                # ---- the version header, through the host's own translator -----------------------
                r = js(br, """
                  var m = window.__exPass.bench.manifest('tilt');
                  var plain = window.__exPass.bench.es3(m.passes[0].frag, false);
                  var already = window.__exPass.bench.es3('#version 300 es\\n' + m.passes[0].frag, false);
                  var count = function (s) { return s.split('#version').length - 1; };
                  return {source: count(m.passes[0].frag), stamped: count(plain),
                          untouched: count(already), head: plain.slice(0, 15)};
                """)
                check(BROWSER_ROWS[16],
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
                check(BROWSER_ROWS[17],
                      took["took"] and mid["state"] == "running" and mid["curtains"][:1] == [True]
                      and end["state"] == "idle" and len(end["docks"]) == 1
                      and end["curtains"][-1] is False and "docked" in end["events"],
                      f"mid={mid} end={end}")

                # ---- row 9: the camera through the whole pass ------------------------------------
                # This instrument claims no camera: the perspective it needs is inside its own
                # surface. The row reads the POSE, never the picture.
                cam = js(br, "var r = window.__report(); "
                             "return {camera: r.camera, rest: r.rest, handoffs: r.handoffs, "
                             "tol: r.camTolerances};")
                check(BROWSER_ROWS[18],
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
                # one handle each, at mid-passage, and are photographed — so a picture that did not
                # move is a handle the instrument is not reading.
                #
                # THE BAR IS EXACTLY NOTHING, and the row above it is why. Two runs of ONE seeded
                # score come back identical to the pixel — mean 0 of 255 at a worst channel of 0 —
                # so a frame that differs from the base at all differs because of the one handle
                # that moved, and no number anybody chose stands between the reading and the verdict.
                # A seam threshold would be the wrong bar here and would say something false: the
                # contact shadow is a band a dozen points wide along the front and the front's own
                # raggedness moves a few columns of it, so both reach the picture plainly and neither
                # moves a large SHARE of it. Every number is printed, so a reading that looks small
                # is on the record rather than hidden behind a bar that passed it.
                br.evaluate("window.__show('host'); 0")
                shot = {}
                MOVES = (("base", {}), ("base-again", {}),
                         ("tilt", {"tilt": 0.0}), ("horizon", {"horizon": 1.0}),
                         ("squeeze", {"squeeze": 0.0}), ("lead", {"lead": 1.0}),
                         ("columns", {"columns": 24}), ("shade", {"shade": 0.0}),
                         ("travel", {"travel": 0.0}), ("mask", {"mask": 1.0}),
                         ("seed", {"seed": 1.37}))
                for name, extra in MOVES:
                    js(br, "return window.__offer(%s, {clock: 1.5, progress: 0.5});"
                       % json.dumps(tilt_score(**extra)))
                    br.sleep(0.7)
                    shot[name] = png(br, SHOTS / ("handle-" + name + ".png"))
                    br.evaluate("window.__cancel('handle row'); 0")
                    idle(br)
                moved = {k: diff(shot["base"], shot[k]) for k, _ in MOVES[2:]}
                still = diff(shot["base"], shot["base-again"])
                check(BROWSER_ROWS[19],
                      still == (0.0, 0) and all(mn > 0 and mx >= 1 for mn, mx in moved.values()),
                      "the same score drawn twice moves the frame by %g of 255 at a worst channel "
                      "of %g, which is the bar every reading below stands against: "
                      % still
                      + "; ".join(f"{k} moves the frame by {mn:.4f} of 255 (worst channel {mx})"
                                  for k, (mn, mx) in moved.items())
                      + ". `mix` is measured by the five poses and the two doors above")

                # ---- THE GRID THE DOOR IS READ ON --------------------------------------------
                # The rows above read every door on the frame the suite runs at. The mask crosses
                # over inside a band of the plane's rows ONE BUFFER POINT wide — at a door the plane
                # is flat, so the projection's own Jacobian is exactly 1 — and the front stands the
                # module's own 0.03 beyond the plane's edge. So the buffer's HEIGHT is what decides
                # a door, and this row states buffers either side of that and reads what the
                # instrument answers, together with the whole column count it applied.
                def door_pose(mix=0, buf=None, **over):
                    p = {"mix": mix, "tilt": 0.72, "horizon": 0.35, "squeeze": 0.55, "lead": 0.4,
                         "columns": 9, "shade": 1, "travel": 1, "mask": 0, "seed": DIE,
                         "reduced": False, "cssWidth": VW, "cssHeight": VH}
                    if buf:
                        p["bufWidth"], p["bufHeight"] = int(buf[0]), int(buf[1])
                    p.update(over)
                    return p

                def values_of(p):
                    return js(br, "return window.__exPass.bench.values('tilt', %s);"
                              % json.dumps(p))

                SHORT = (390, 30)     # one buffer point covers more of the plane than the margin
                TALL = (390, 40)      # and one that does not
                on_css = values_of(door_pose())
                on_short = values_of(door_pose(buf=SHORT))
                on_tall = values_of(door_pose(buf=TALL))
                on_exit = values_of(door_pose(mix=1, buf=SHORT))
                away = values_of(door_pose(mix=0.5, buf=SHORT))
                judged = values_of(door_pose(mask=1.0))
                counted = values_of(door_pose(columns=9.6))
                check(BROWSER_ROWS[21],
                      on_css["doorWhyNo"] is None
                      and on_css["doorGrid"] == {"w": VW, "h": VH, "drawn": False}
                      and abs(on_css["doorFoot"] - 1.0 / VH) < 1e-9
                      and on_short["doorWhyNo"] and "390 x 30 buffer" in on_short["doorWhyNo"]
                      and "the entry door leaks" in on_short["doorWhyNo"]
                      and on_tall["doorWhyNo"] is None
                      and on_exit["doorWhyNo"] and "the exit door leaks" in on_exit["doorWhyNo"]
                      and away["doorWhyNo"] is None and away["doorGrid"] is None
                      and judged["doorWhyNo"]
                      and "judges' own channel" in judged["doorWhyNo"]
                      and counted["cols"] == 10 and abs(counted["colsRequest"] - 9.6) < 1e-9
                      and abs(counted["colsRounded"] - 0.4) < 1e-9,
                      "on the %d x %d CSS frame one point covers %.5f of the plane's own rows and "
                      "the door is whole; on a %d x %d buffer it covers %.5f and the instrument says "
                      "«%s»; on a %d x %d buffer it is whole again. The exit door reads the same law "
                      "from the other side («%s»). Away from a door nothing is read at all (grid "
                      "%s). With the judges' channel open the door says «%s». And the column count "
                      "the score asked for, %g, is applied as the whole %g it draws at."
                      % (VW, VH, on_css["doorFoot"], SHORT[0], SHORT[1], on_short["doorFoot"],
                         on_short["doorWhyNo"], TALL[0], TALL[1], on_exit["doorWhyNo"],
                         away["doorGrid"], judged["doorWhyNo"], counted["colsRequest"],
                         counted["cols"]))

                # ---- THE DOOR REFUSED ON THE REAL TRANSACTION ROAD ---------------------------
                # The row above reads the instrument's own record. This one puts a real command on
                # the real road: a score that opens the judges' channel is offered held at its entry
                # door, and the host has to land the visitor on the instrument's own reason rather
                # than draw a door that is a flat field instead of a photograph. The same frame with
                # the channel at rest draws.
                def road(gen):
                    return js(br, "var r = window.__report(); return {state: r.state, "
                                  "drew: r.drew, buffer: r.census.buffer, "
                                  "refused: r.events.filter(function(e){ return e.gen === %d "
                                  "&& e.why && String(e.why).indexOf('door leaks') >= 0; })"
                                  ".map(function(e){ return e.name + ': ' + e.why; })};" % gen)

                br.evaluate("window.__cancel('door road row'); 0")
                idle(br)
                rest_gen = js(br, "return window.__offer(%s, {clock: 0, progress: 0});"
                              % json.dumps(tilt_score()))["gen"]
                br.sleep(1.0)
                played = road(rest_gen)
                br.evaluate("window.__cancel('door road row'); 0")
                idle(br)
                open_gen = js(br, "return window.__offer(%s, {clock: 0, progress: 0});"
                              % json.dumps(tilt_score(mask=1.0)))["gen"]
                br.sleep(1.1)
                leaked = road(open_gen)
                br.evaluate("window.__cancel('door road row'); 0")
                idle(br)
                check(BROWSER_ROWS[22],
                      played["state"] == "running" and played["drew"] == 1
                      and not played["refused"]
                      and len(leaked["refused"]) == 1 and leaked["state"] == "idle"
                      and "the entry door leaks" in leaked["refused"][0]
                      and "judges' own channel" in leaked["refused"][0],
                      "with the judges' channel at rest the score draws (%d cue, state %s, refused "
                      "%s); with it open the same command is refused with «%s», on which the host "
                      "lands the transaction (state %s, %d cue drawn) and the walk's own glide "
                      "carries the visitor"
                      % (played["drew"], played["state"], played["refused"] or "nothing",
                         (leaked["refused"] or ["nothing refused"])[0], leaked["state"],
                         leaked["drew"]))

                kept = sorted(p.name for p in SHOTS.glob("*.png"))
                check(BROWSER_ROWS[20],
                      len(kept) >= 25 and all((SHOTS / k).stat().st_size > 1000 for k in kept),
                      f"{len(kept)} captures under {SHOTS.relative_to(ROOT)}: the five poses on both "
                      f"roads, the seven sampled instants, the frame after a resize, the two seeded "
                      f"runs and the eleven handle runs")

    shutil.rmtree(BENCH, ignore_errors=True)

    # ============================================================================================
    # THE RED-ON-BUG PROOFS. The lane's own rules reverted in the artifact the browser actually
    # loads. The pack served is changed and the host is re-stamped with the digest of the bytes it is
    # handed, which is what the build does; the file on disk is never touched, so no working tree can
    # be left changed by a proof.
    #
    # ONE · THE DOOR READING. Taken out, no instant is ever a door and the reading is never taken —
    # this instrument exactly as it stood before it read its doors at runtime, declaring both doors
    # whole in its manifest and never checking the frame it drew.
    def red_door(br):
        gen = js(br, "return window.__offer(%s, {clock: 0, progress: 0});"
                 % json.dumps(tilt_score(mask=1.0)))["gen"]
        br.sleep(1.2)
        r = js(br, "var r = window.__report(); return {state: r.state, drew: r.drew, "
                   "refused: r.events.filter(function(e){ return e.gen === %d && e.why "
                   "&& String(e.why).indexOf('door leaks') >= 0; }).length};" % gen)
        br.evaluate("window.__cancel('red one'); 0")
        return r

    door_base = on_bench(red_door)
    bug1 = REGION.replace("var want = mix === 0 ? 1 : (mix === 1 ? 0 : -1);", "var want = -1;", 1)
    door_bug = on_bench(red_door, pack_text=bug1)
    check(RED_ROWS[0],
          bug1 != REGION and door_base and door_bug
          and door_base["refused"] == 1 and door_base["state"] == "idle"
          and door_bug["refused"] == 0 and door_bug["state"] == "running"
          and door_bug["drew"] == 1,
          f"a score that opens the judges' channel at the entry door draws this instrument's own "
          f"coverage instead of a photograph. With the reading standing the host is told so "
          f"({door_base and door_base['refused']} refusal, state {door_base and door_base['state']}) "
          f"and the walk's own glide carries the visitor. With the door test taken out — no instant "
          f"is a door, the instrument as it stood before it read its doors at runtime — the same "
          f"command draws that door instead ({door_bug and door_bug['refused']} refusals, state "
          f"{door_bug and door_bug['state']}, {door_bug and door_bug['drew']} cue drawn), and "
          f"nothing anywhere says the frame it laid down was one whole work")

    # TWO · THE MATRIX REBUILD. The module binds its plane's inverse as one mat3 and §7 knows no
    # matrix type, so the port carries the three ROWS and rebuilds the matrix column by column inside
    # the shader. Rebuilt row by row instead, every leaning pose reads a transposed projection: the
    # doors still stand — a flat plane's map is diagonal and a diagonal matrix is its own transpose,
    # which is exactly why the doors cannot catch this — and the passage between them is a different
    # picture from the module's.
    def red_roads(br):
        br.evaluate("window.__mix(0.5); 0")
        br.sleep(0.9)
        br.evaluate("window.__hostDraw(); 0")
        br.sleep(0.15)
        br.evaluate("window.__show('host'); 0")
        br.sleep(0.3)
        ph = png(br, SHOTS / ("roads-host-%d.png" % len(list(SHOTS.glob("roads-host-*.png")))))
        br.evaluate("window.__show('module'); 0")
        br.sleep(0.3)
        pm = png(br, SHOTS / ("roads-module-%d.png" % len(list(SHOTS.glob("roads-module-*.png")))))
        mn, mx = diff(ph, pm)
        # the two doors, on the very same bench, so the row can say whether they would have caught it
        out = {"mid": [mn, mx]}
        for name, v in (("door-0", 0.0), ("door-1", 1.0)):
            br.evaluate("window.__mix(%r); 0" % v)
            br.sleep(0.8)
            br.evaluate("window.__hostDraw(); 0")
            br.sleep(0.15)
            br.evaluate("window.__show('host'); 0")
            br.sleep(0.3)
            a = png(br, SHOTS / ("roads-%s-host-%d.png"
                                 % (name, len(list(SHOTS.glob("roads-%s-host-*.png" % name))))))
            br.evaluate("window.__show('module'); 0")
            br.sleep(0.3)
            b = png(br, SHOTS / ("roads-%s-module-%d.png"
                                 % (name, len(list(SHOTS.glob("roads-%s-module-*.png" % name))))))
            out[name] = list(diff(a, b))
        return out

    roads_base = on_bench(red_roads)
    bug2 = REGION.replace("mat3 uInv = mat3(uInv0.x, uInv1.x, uInv2.x,",
                          "mat3 uInv = mat3(uInv0.x, uInv0.y, uInv0.z,", 1)
    bug2 = bug2.replace("uInv0.y, uInv1.y, uInv2.y,", "uInv1.x, uInv1.y, uInv1.z,", 1)
    bug2 = bug2.replace("uInv0.z, uInv1.z, uInv2.z);", "uInv2.x, uInv2.y, uInv2.z);", 1)
    roads_bug = on_bench(red_roads, pack_text=bug2)

    def road_at(rec, key):
        return rec[key][0] if rec else float("nan")

    check(RED_ROWS[1],
          bug2 != REGION and roads_base and roads_bug
          and roads_base["mid"][0] <= SAME and roads_bug["mid"][0] > SAME
          and roads_base["door-0"][0] <= SEAM and roads_bug["door-0"][0] <= SEAM,
          "with the matrix rebuilt column by column the two roads stand %.4f of 255 apart at "
          "mid-passage (bar %s); rebuilt row by row they stand %.4f apart. The doors catch none of "
          "it — %.4f against %.4f at door 0, and %.4f against %.4f at door 1 — because a flat "
          "plane's map is diagonal and a diagonal matrix is its own transpose, which is why this "
          "row reads the passage and not the ends"
          % (road_at(roads_base, "mid"), SAME, road_at(roads_bug, "mid"),
             road_at(roads_base, "door-0"), road_at(roads_bug, "door-0"),
             road_at(roads_base, "door-1"), road_at(roads_bug, "door-1")))

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
