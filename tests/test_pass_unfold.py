#!/usr/bin/env python3
"""PASS-API-V1 — the unfold instrument on the host's frame.
Run: python3 tests/test_pass_unfold.py

Root: his word of 2026-08-17 17:06 — more spectacle, at speed — and the composer's own census, where
1 296 declined pairs name a panels instrument as the thing they lack (lab/data/sceneplans/index.json,
declinesByReason, the largest single entry after the missing stack ground). docs/design/PASS-API-V1.md
§7 (GPU and resources), §8 (the manifest) and §9's conformance rows 7, 9, 10, 13, 14, 15, 16 and 22
are what this file makes real, together with §7's coverage law of 12:40 and its per-instrument
specification in docs/design/COVERAGE.md. The lifecycle rows stay in tests/test_pass_api.py and are
untouched.

WHAT IS COMPARED, AND AGAINST WHAT.

  The doors. At the dial's two ends one whole work stands. Each is measured against ITS OWN FILE,
  cover-fitted into the frame with no crop at all — the module's own repair of 2026-08-13 made both
  doors the plain cover fit — inside the project's seam threshold of 6 of 255.

  The closed sheet. At the middle of the hand the sheet stands shut and the frame holds the single
  photograph the work was cut from: the file's own top-left quarter, cover-fitted. It is measured
  against that quarter, and the instant halfway through the exchange is measured against the two
  quarters averaged, because the exchange is a straight dissolve of two flat pictures.

  THE TWO ROADS, AND WHY THIS PORT'S BAR IS ITS OWN. Every instrument ported before this one came
  from a lab module that already held a WebGL context, so both roads ran one sampler through one
  rasteriser and agreed to 0.0000 of 255. This module draws with CSS 3D and the lab road here is the
  BROWSER'S OWN COMPOSITOR: its image downscaling, its edge antialiasing along seven panel faces, and
  its gradient rasterisation over four shades and three creases. The residual between the two roads is
  therefore a difference of samplers rather than a difference of mathematics, and the bars below are
  MEASURED (2026-08-17) and carry that reading. What makes them mean anything is the red-on-bug set:
  each of the four reverts one rule this port states and moves the same number by a wide multiple of
  the bar it is held to.

  The coverage. This instrument declares that it writes none, because it fills the frame. That is
  measured rather than declared: the panel map — the port's own judges' frame, which paints which
  panel stands at each point of the frame — is read at every sampled pose and holds no unclaimed
  point. The placement it buys is read off the host's own `coverageWhyNo`.

  No empty frame. The rows below sample the pass at seven instants and once across a change of
  viewport, and each frame has to stand as a picture.

  The lab module is READ ONLY. Absent, every browser row here is a pinned SKIP that names the missing
  path — never a silent pass.
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

# The lab module and the two photographs stand in the MAIN tlvphotos worktree, which is where the
# suite of the last port read them from too.
LAB = Path(os.environ.get("TLVPHOTOS_ROOT", "/Users/sashaabramovich/tlvphotos")) / "lab"
PHOTOS = [LAB / "photos" / "towers.jpg", LAB / "photos" / "glassgrid.jpg"]
MODULE = LAB / "effects" / "unfold.js"

SITE_URL = "https://synth.example.com"
VW, VH = 390, 844          # the phone frame lab/carrier-check.py measures on
CLOCK = 7.0                # the second the comparison holds at, as the carrier's own check does
SEAM = 6.0                 # the project's seam threshold, 6 of 255 (TRANSITION-STAGE-V0 §1)
FAR = 40.0                 # further than this from a file and it is a different work
BACKGROUND = (0x08, 0x08, 0x0a)
SPREAD = 10.0

# THE TWO ROADS' BARS, measured 2026-08-17 on this bench.
#
# FLAT_SAME — the four poses at which the sheet stands square: the two doors and the two faces of the
# closed sheet. Nothing is folded, nothing leans and nothing turns there, so the whole residual is the
# two roads' image scaling: the host samples the file with GL_LINEAR at the buffer's own size, the
# compositor scales the same file with its own filter. Measured at 0.6772, 0.6367, 1.0068 and 1.2215
# of 255, so this port meets the project's OWN two-roads bar of 1.5 at every square pose and takes no
# bar of its own there.
#
# FOLD_SAME — the four poses through the fold, and the one number this port sets for itself. On top of
# the scaling above, the compositor antialiases seven panel edges and rasterises seven gradients, and
# this shader draws each of them at one point with no coverage of its own; the worst single channel
# through the fold stands at 130 and lies along those edges. Measured at 4.0035, 3.1790, 1.2452 and
# 1.4344 of 255 on 2026-08-17, and set at 5.0 — the worst reading plus about a quarter.
#
# NEITHER BAR IS A SETTING THE PICTURE IS TUNED TO. The four red-on-bug proofs each break one rule of
# the port and move the same numbers by a wide multiple, and their readings stand beside the green
# ones in the evidence.
FLAT_SAME = 1.5
FOLD_SAME = 5.0

SHOTS = ROOT / "tests" / "captures" / "pass-unfold"

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


DIE = 4.91016            # the die lab/data/scores' own weave score carries, so every suite rolls one
DURATION_MS = 6500
WITHIN_MS = 500

# The instrument's own exchange: the share of the hand the closed sheet stands for, and the two ends
# of it. Read here as the port's own numbers so a row can stand at them.
HOLD = 0.08
SHUT_IN = 0.5 - HOLD / 2
SHUT_OUT = 0.5 + HOLD / 2


def _static(v):
    return {"op": "static", "value": v}


def unfold_cue(stack=0, levels_own=None, **statics):
    """The cue, with a track for every one of the eight handles (§4.4b)."""
    P = {"tilt": 0.5, "shade": 1, "depth": 0.5, "stagger": 0.34, "panels": 1, "mask": 0}
    P.update(statics)
    nodes = {"u-mix": {"source": "progress"}, "u-clock": {"source": "time"}}
    tracks = {"mix": {"node": "u-mix"}, "clock": {"node": "u-clock"}}
    for k, v in P.items():
        nodes["u-" + k] = _static(v)
        tracks[k] = {"node": "u-" + k}
    return {
        "id": "unfold-main", "instrument": {"id": "unfold", "api": 1},
        "voice": "letter", "roles": ["disassembly", "mystery", "assembly"],
        "levels": ["CELL", "CELL CONTENT"],
        "levelOwnership": levels_own or {"CELL": "owns", "CELL CONTENT": "owns"},
        "window": [0, DURATION_MS / 1000.0], "works": ["a", "b"], "stack": stack,
        "cameraAuthority": "stage",
        "doors": {"in": {"handle": "mix", "value": 0, "measured": True},
                  "out": {"handle": "mix", "value": 1, "measured": True}},
        "nodes": nodes, "tracks": tracks,
        "resources": {"textures": 0, "textureSlots": 2, "framebuffers": 0, "pingPong": 0,
                      "programs": 1, "passes": 1, "bytesEstimate": 0, "variant": "standard"},
    }


def matter_cue(stack=1):
    """THE VOICE THAT STANDS OVER IT. `matter` writes coverage — «1.0 - cov, the share of the arriving
    work at the travelling threshold» — so it is what a frame-filling ground is meant to be played
    under (COVERAGE.md §3, and the placement rule §7 states). Its own handles rest at the defaults its
    manifest publishes; the two this cue drives are the dial and the second."""
    nodes = {"m-mix": {"source": "progress"}, "m-clock": {"source": "time"}}
    tracks = {"mix": {"node": "m-mix"}, "clock": {"node": "m-clock"}}
    return {
        "id": "over", "instrument": {"id": "matter", "api": 1},
        "voice": "accompaniment", "roles": ["assembly"],
        "levels": ["SURFACE", "TEXTURE"],
        "levelOwnership": {"SURFACE": "owns", "TEXTURE": "owns"},
        "window": [0, DURATION_MS / 1000.0], "works": ["a", "b"], "stack": stack,
        "cameraAuthority": "stage",
        "doors": {"in": {"handle": "mix", "value": 0, "measured": True},
                  "out": {"handle": "mix", "value": 1, "measured": True}},
        "nodes": nodes, "tracks": tracks,
        "resources": {"textures": 0, "textureSlots": 2, "framebuffers": 0, "pingPong": 0,
                      "programs": 1, "passes": 1, "bytesEstimate": 0, "variant": "standard"},
    }


def unfold_score(under=False, **statics):
    """`under` puts a coverage-writing voice ABOVE this instrument, which is the placement its own
    declaration buys it: the ground of a stack."""
    cues = [unfold_cue(stack=0, **statics)]
    if under:
        cues = cues + [matter_cue(stack=1)]
    res = {"textures": 0, "textureSlots": 2, "framebuffers": 0, "pingPong": 0, "programs": 1,
           "passes": 1, "bytesEstimate": 0}
    return {
        "schema": 2,
        "intent": "one work stands whole and folds shut along its own mirrored panels until the "
                  "single photograph it was cut from stands alone; the two works exchange on that "
                  "photograph; and the second work opens out along the same seams "
                  "(lab/effects/unfold.js:1-21, its own header)",
        "pair": {"a": "a", "b": "b"},
        "seed": DIE,
        "duration": DURATION_MS,
        "direction": "a-to-b",
        "interruption": {"withinMs": WITHIN_MS, "resolve": "nearest-door"},
        "failLand": "arrive",
        "camera": {"owner": "stage", "rests": "b",
                   "track": [{"at": "b", "pan": {"x": 0, "y": 0}, "logScale": 0,
                              "pitch": 0, "yaw": 0, "roll": 0, "fov": None, "owner": "stage"}]},
        "cues": cues,
        "quality": {v: {"renderScale": None,
                        "cues": {c["id"]: {"resources": dict(res, variant=v)} for c in cues}}
                    for v in ("lean", "standard", "rich")},
        "provenance": {"source": "lab/effects/unfold.js's own declared defaults and constants",
                       "measuredAt": None, "by": "tests/test_pass_unfold.py"},
    }


# ---------------------------------------------------------------- bake once
build_site.SITE_CONFIG = dict(build_site.SITE_CONFIG)
build_site.SITE_CONFIG["pass"] = {"visualLayer": "pass", "diagnostics": "on"}

TMP = Path(tempfile.mkdtemp(prefix="synth_passunfold_"))
build_site.OUT = TMP
build_site.build(SITE_URL)
LAYER = (TMP / "pass-layer.js").read_text(encoding="utf-8")
# THE INSTRUMENT'S OWN BUILT FILE — the real artifact a visitor is served, comments stripped. Since
# every instrument travels alone, the whole of this file is this instrument and nothing else.
PACK = (TMP / "pass-inst-unfold.js").read_text(encoding="utf-8")
REGION = PACK
SOURCE = ROOT / "engine" / "assets" / "pass-inst-unfold.js"
# The file as it stands in the tree, comments and all: the rows about what this instrument DECLARES
# read the built artifact, and the rows about what it SAYS read the source it is built from.
SOURCE_TEXT = SOURCE.read_text(encoding="utf-8")

# ---------------------------------------------------------------- string rows

OWNED = ["createElement", "getContext", "requestAnimationFrame", "addEventListener",
         "performance.now", "Date.now", "new Image", "setTimeout", "setInterval"]
held = [s for s in OWNED if s in REGION]
check("PASS-UNFOLD the instrument creates no element, no loop and no listener",
      not held,
      "§1.2's fence, read against the instrument's own built file: none of the nine ways of owning "
      "hardware appears there. The module builds twenty-two elements — a stage, a tilt box, a sheet, "
      "a backing, four hinged panels, seven faces, four shades and three creases — binds two pointer "
      "listeners and runs its own rAF clock; all of it stayed in the lab"
      if not held else "the instrument's region holds " + ", ".join(held))

HANDLES = ["mix", "clock", "tilt", "shade", "depth", "stagger", "panels", "mask"]
absent = [h for h in HANDLES if ("%s: { min" % h) not in REGION]
check("PASS-UNFOLD every handle the instrument publishes is a handle a score can drive",
      not absent and len(HANDLES) == 8,
      "§4.4b: eight handles. The dial and the second the host hands down, the module's own five "
      "declared params, and the judges' channel. The module's `pace` is published by neither, for "
      "the reason the module itself gives: a handle a score can walk without moving the picture is "
      "noise in the score"
      if not absent else "these are published nowhere: " + ", ".join(absent))

check("PASS-UNFOLD the lean reads the handed-down second, and no clock or pointer of its own",
      "st.reduced ? 0 : st.t" in REGION and "t: h.clock" in REGION
      and "ctx.pointer" not in REGION and "BASE_PERIOD" not in REGION,
      "the module runs a fifteen-second breath on its own rAF clock and reads the pointer across its "
      "mount (unfold.js:424-462). Both are gone: the one place time reaches the picture is the sway "
      "that carries the lean, and it reads the `clock` handle, which is what makes the seeded repeat "
      "below mean anything")

check("PASS-UNFOLD the manifest leaves the drawing buffer unpreserved",
      "gl: { preserveDrawingBuffer: false }" in REGION,
      "§7 refuses a manifest that asks for the buffer to be preserved; this instrument draws every "
      "frame the host hands it")

LABTXT = MODULE.read_text(encoding="utf-8") if MODULE.exists() else ""

check("PASS-UNFOLD the shader carries no version header of its own",
      "#version" not in REGION,
      "so the host's translator stamps the one header this shader needs and no second one arrives")

# ================================================================================================
# THE MODULE THAT HAD NO SHADER. The measurement the port was asked for, standing as a row.
# ================================================================================================
lab_gl = [s for s in ("getContext", "createShader", "gl_FragColor", "precision ", "uniform ")
          if s in LABTXT]
check("PASS-UNFOLD the module holds no shader at all, and the shape this port gave it",
      bool(LABTXT) and not lab_gl
      and "transform-style:preserve-3d" in LABTXT and "perspective" in LABTXT
      and "bool lands(" in REGION and "vec3 stood(" in REGION
      and 'program: "unfold"' in REGION,
      "the module draws with CSS 3D — a perspective container, a sheet, four hinged panels and seven "
      "faces — and the browser's own compositor projects them, so it carried no context, no shader "
      "and no uniform for a port to lift. None of %s appears in it. A CSS 3D chain is affine in a "
      "panel's own two coordinates and the perspective divides once, so the map from a panel to the "
      "frame is a homography and is invertible: this port's shader solves the two-by-two system that "
      "says where on each panel a point of the frame falls, keeps the panels the point lands on, and "
      "takes the one nearest the eye. One pass, twelve uniforms, no second slot"
      % ", ".join(("getContext", "createShader", "gl_FragColor", "precision", "uniform"))
      if not lab_gl else "the module already holds " + ", ".join(lab_gl))


def numbers(text, pattern):
    m = re.search(pattern, text)
    return [float(x) for x in re.findall(r"-?\d+\.?\d*", m.group(1))] if m else []


lab_feel = numbers(LABTXT, r"FEEL_KNOTS = \[([^\]]+)\]")
port_feel = numbers(REGION, r"FEEL_KNOTS = \[([^\]]+)\]")
check("PASS-UNFOLD the response curve is carried digit for digit out of the lab module",
      len(lab_feel) == 21 and lab_feel == port_feel,
      f"the hand's own table at twenty-one equal marks ({len(port_feel)} numbers matched, half the "
      f"change standing at {port_feel[10] if len(port_feel) > 10 else None}). It is the inverse of "
      f"the picture's own measured travel, read on two works whose shapes pull opposite ways and "
      f"inverted a second time against the hand's own steps; the raw band before it was 5.19. The "
      f"port runs it once over each half of the hand, so equal movements are equal felt change on "
      f"both sides of the exchange")

# Every constant the picture stands on, read out of the lab module and out of the built file.
CONSTANTS = [
    ("MAXA = 84", "MAXA = 84", "degrees a panel swings before it stands edge-on"),
    ("EDGE = 1.16", "EDGE = 1.16",
     "the room the lean needs, and it is needed only while the sheet leans"),
    ("PULL = 1.8", "PULL = 1.8",
     "the room the corner needs on top of it, where both pairs turn at once"),
    ("PERSP_FLAT = 4.4, PERSP_DEEP = 2.6", "PERSP_FLAT = 4.4, PERSP_DEEP = 2.6",
     "how deep the fold is seen: the near end is where a panel would project across its neighbour"),
    ("HOME = 80", "HOME = 80", "when a turned panel is counted gone by the growth law"),
    ("MIRROR = 14", "MIRROR = 14",
     "how long a panel takes to take on its mirror, in degrees of its own turn"),
    ("rgba(0,0,0,.28)", "0.28", "the shade's own opening weight across a turning panel"),
    ("rgba(0,0,0,.30)", "0.30", "and across a panel turning the other way"),
    ("rgba(255,255,255,.85)", "0.85", "how bright a crease stands down its own middle"),
    ("0.10 * fR * rY", "0.10 * fR * rY", "the shade the standing panel catches"),
    ("0.97 * Math.pow(1 - cY, 0.8)", "0.97 * Math.pow(1 - cY, 0.8)",
     "and the shade the turning panel casts on itself"),
    ("0.93 * Math.pow(1 - cX, 0.8)", "0.93 * Math.pow(1 - cX, 0.8)", "the pair below it"),
    ("smooth((open - 0.004) / 0.05)", "smooth((open - 0.004) / 0.05)",
     "the backing goes out as soon as the sheet opens, so no seam can show a dark hairline"),
    ("4 * fold * (1 - fold)", "4 * fold * (1 - fold)",
     "the gate that rests the lean at both doors, at any tilt and any second of the clock"),
    ("Math.sin(ty * 0.31) * 1.6", "Math.sin(ty * 0.31) * 1.6", "the sway's own rate and reach"),
    ("Math.sin(ty * 0.23 + 1.1) * 7", "Math.sin(ty * 0.23 + 1.1) * 7", "and the second of them"),
    ("Math.sin(ty * 0.17 + 2.2) * 1.3", "Math.sin(ty * 0.17 + 2.2) * 1.3", "and the third"),
]
missing_const = [p for lab_p, p in ((a, b) for a, b, _ in CONSTANTS)
                 if lab_p not in LABTXT or p not in REGION]
check("PASS-UNFOLD every constant the picture stands on carries the module's own number",
      not missing_const and bool(LABTXT),
      "; ".join("%s — %s" % (p, why) for _, p, why in CONSTANTS) if not missing_const
      else "these differ between the lab module and the port: " + ", ".join(missing_const))

check("PASS-UNFOLD the port's own one number is named as its own, and it is the exchange",
      "var HOLD = 0.08;" in REGION and "HOLD" not in LABTXT
      and "SHUT_IN = 0.5 - HOLD / 2" in REGION,
      "the module takes one picture (lab/data/module-contract.json: needsTwoWorks false) and a cue "
      "carries two, so the port had to say where the second work enters. It enters at the closed "
      "sheet, the one instant at which both works stand as one flat full-frame picture. HOLD is how "
      "much of the hand that rest takes and is the only number here the module did not measure")

check("PASS-UNFOLD the host binds uniforms by declared name, never by position or a written list",
      "getUniformLocation(p, u.name)" in LAYER and "uTurn" not in LAYER and "uCrease" not in LAYER,
      "this instrument declares twelve uniforms, of which five are shared with the woven one. The "
      "host reads the manifest")

declared = set(re.findall(r'\{ name: "(u\w+)", type:', REGION))
spelled = set(re.findall(r'uniform \w+ (u\w+);', REGION))
check("PASS-UNFOLD the manifest's declared names and the shader's own names are one set",
      declared == spelled and len(declared) == 12,
      f"{len(declared)} declared, {len(spelled)} spelled; "
      f"declared only: {sorted(declared - spelled)}; spelled only: {sorted(spelled - declared)}")

check("PASS-UNFOLD the coverage is declared, and the frame it fills is the reason",
      "coverage: { writes: false" in REGION
      and "gl_FragColor = vec4(col, 1.0);" in REGION
      and "opacity" not in REGION and "presence" not in REGION,
      "§8's coverage block and §7's law: the alpha is the constant 1, said as a decision. The growth "
      "law grows the sheet by exactly what each turning panel gives up, so the standing picture "
      "covers the frame at every point of the travel. Under the placement rule that makes this "
      "instrument lawful as the LOWEST cue of a stack, which the census counts 1 320 declined plans "
      "waiting for. No handle of opacity and no weight of presence stands anywhere in the instrument")

sha = hashlib.sha256(MODULE.read_bytes()).hexdigest() if MODULE.exists() else ""
declared_sha = (re.search(r'sha256: "([0-9a-f]{64})"', REGION) or [None, None])[1]
check("PASS-UNFOLD the provenance names the file the port was read from, and the file weighs to it",
      bool(sha) and sha == declared_sha and 'commit: "4c7dfe4"' in REGION,
      f"the module is tracked, so the commit it was read at is named beside the digest of its bytes, "
      f"and the file still weighs to {sha[:16]}…")

# ---------------------------------------------------------------- browser rows

BROWSER_ROWS = [
    "PASS-UNFOLD §8     · the manifest carries every field the contract names, in its shape",
    "PASS-UNFOLD §8     · it publishes CELL and CELL CONTENT, and the reading is said to be derived",
    "PASS-UNFOLD row 7  · door 0 stands the departing work, measured against its own file",
    "PASS-UNFOLD row 7  · door 0 carries no trace of the arriving work",
    "PASS-UNFOLD row 7  · door 1 stands the arriving work, measured against its own file",
    "PASS-UNFOLD row 7  · door 1 carries no trace of the departing work",
    "PASS-UNFOLD the closed sheet stands the one photograph each work was cut from",
    "PASS-UNFOLD the two works exchange on that photograph, and on nothing folded",
    "PASS-UNFOLD the two roads agree at the four poses where the sheet stands square",
    "PASS-UNFOLD the two roads agree through the fold, at the compositor's own bar",
    "PASS-UNFOLD §7     · the frame is covered by panels at every sampled pose",
    "PASS-UNFOLD §7     · the ground of a stack, and refused above another cue",
    "PASS-UNFOLD §7     · both doors stand whole with a coverage-writing voice over them",
    "PASS-UNFOLD §7     · no empty frame at any sampled instant of the pass",
    "PASS-UNFOLD §7     · the frame after a change of viewport is drawn afresh",
    "PASS-UNFOLD row 10 · a seeded run repeats to the pixel",
    "PASS-UNFOLD row 14 · textures, programmes and framebuffers return to their baseline after ten runs",
    "PASS-UNFOLD row 15 · the console stays clean",
    "PASS-UNFOLD row 22 · the census shows granted against declared, and neither overruns",
    "PASS-UNFOLD §7     · one canvas, one context, two source textures, one pass a frame",
    "PASS-UNFOLD §7     · a shader already at GLSL ES 3.00 receives no second version header",
    "PASS-UNFOLD the real transaction road: curtain up, one pass drawn, exactly one dock at the end",
    "PASS-UNFOLD row 9  · one camera authority through a real pass, and the pose rests on the arrival",
    "PASS-UNFOLD §4.4b  · the tilt, the shade, the depth, the stagger and the panel count reach the PICTURE",
    "PASS-UNFOLD row 16 · the captures are kept as evidence",
    "PASS-UNFOLD the panel map is WALKED on the drawing buffer at both doors, and what it read is published",
    "PASS-UNFOLD a door the judges' channel spoils is refused on the real road, and the visitor still lands",
]

RED_ROWS = [
    "PASS-UNFOLD red-on-bug · the growth law removed: the frame stops being covered",
    "PASS-UNFOLD red-on-bug · the corner's own foreshortening removed: the bare triangle returns",
    "PASS-UNFOLD red-on-bug · the mirror taken on at once: door 0 stops being the work",
    "PASS-UNFOLD red-on-bug · the seating removed: the sheet stops being the file",
    "PASS-UNFOLD red-on-bug · the door reading removed: a door drawing the panel map is let through",
]

# THE MEASUREMENT READ AT A DOOR, published in the manifest. His 19:13 word, lifted to the class at
# 19:21: every geometric parameter names the measurement of the work it reads. This instrument's own
# door reading is its PANEL MAP, walked at the buffer's own sample points, and the handle that can
# spoil a door — the judges' channel — is where that is published, beside the flat guard the module's
# own half degree stands at and the reach the hold has in points of the grid.
check("PASS-UNFOLD the judges' handle publishes the measurement the door is read against",
      'readAtADoor: { points: DOOR_HOLD, readOn: "the drawing buffer",' in SOURCE_TEXT
      and 'reads: "flatDegRequest"' in SOURCE_TEXT
      and "var FLAT_DEG = 0.5;" in SOURCE_TEXT
      and "var DOOR_HOLD = 2;" in SOURCE_TEXT
      and "var DOOR_SHOW = 0.5 / 255;" in SOURCE_TEXT
      and "if (aY < flatDeg) aY = 0;" in SOURCE_TEXT,
      "the handle carries `applied.readAtADoor` — what is walked, on which grid, how far the hold "
      "reaches and where the module's own guard stays on the record — and the guard itself is a "
      "parameter of the pose, so a door can re-ask it in the grid's own units while the middle of "
      "a passage keeps the module's half degree")

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
    from PIL import Image, ImageChops, ImageStat
    a = Image.open(p).convert("RGB")
    flat = Image.new("RGB", a.size, BACKGROUND)
    st = ImageStat.Stat(ImageChops.difference(a, flat))
    own = ImageStat.Stat(a)
    return sum(st.mean) / 3.0, sum(own.stddev) / 3.0


def unclaimed(p):
    """The share of the panel map that names no panel. The map paints the standing panel at a quarter
    of full red, the turning one at a half, and the two below at three quarters and full; a point no
    panel covers stays black. So this is the share of the frame the growth law failed to fill."""
    from PIL import Image
    a = Image.open(p).convert("RGB")
    r = a.split()[0].point(lambda v: 255 if v < 8 else 0)
    return r.histogram()[255] / float(a.size[0] * a.size[1])


def cover_into(im, w, h, crop=1.0):
    from PIL import Image
    iw, ih = im.size
    fa, ia = w / float(h), iw / float(ih)
    sw, sh = (ih * fa, float(ih)) if ia > fa else (float(iw), iw / fa)
    sw /= crop
    sh /= crop
    x0, y0 = (iw - sw) / 2.0, (ih - sh) / 2.0
    return im.resize((w, h), Image.BILINEAR, box=(x0, y0, x0 + sw, y0 + sh))


def work_in_the_frame(src, w, h, crop=1.0):
    """The whole file, cover-fitted into the frame. This instrument's own doors take no crop at all;
    the argument is for reading a door another voice's manifest publishes a crop for."""
    from PIL import Image
    return cover_into(Image.open(src).convert("RGB"), w, h, crop)


def quarter_in_the_frame(src, w, h):
    """The single photograph the work was cut from: the file's own top-left quarter, cover-fitted.
    The quarter carries the file's own aspect, so the sheet grown to two and cropped to its standing
    panel is the same picture as this crop cover-fitted."""
    from PIL import Image
    im = Image.open(src).convert("RGB")
    iw, ih = im.size
    return cover_into(im.crop((0, 0, iw // 2, ih // 2)), w, h)


def apart(p, work):
    from PIL import Image, ImageChops, ImageStat
    a = Image.open(p).convert("RGB")
    if a.size != work.size:
        return 255.0, 255.0
    st = ImageStat.Stat(ImageChops.difference(a, work))
    return sum(st.mean) / 3.0, max(m for _, m in st.extrema)


def bench_dir(pack_text=None):
    """The bench's own served root: the BUILT pass-layer.js, the site's own settings record and the
    BUILT instrument files it names — the real artifacts, namespace applied and comments stripped —
    the lab module unchanged, the two photographs, and the page that stands the two roads of one
    frame side by side.

    A row proving a rule reds hands over a CHANGED instrument file and writes the record with the
    digest of the bytes actually served, which is what the build does. The source file on disk is
    never touched, so nothing has to be restored and no working tree can be left changed by a
    red-on-bug proof."""
    d = Path(tempfile.mkdtemp(prefix="synth_unfoldbench_"))
    pack = PACK if pack_text is None else pack_text
    shutil.copy2(TMP / "pass-layer.js", d / "pass-layer.js")
    for _inst in sorted(TMP.glob("pass-inst-*.js")):
        shutil.copy2(_inst, d / _inst.name)
    (d / "pass-inst-unfold.js").write_text(pack, encoding="utf-8")
    record = json.loads((TMP / "config.json").read_text(encoding="utf-8"))
    record["pass"]["instruments"]["unfold"]["digest"] = hashlib.sha256(
        pack.encode("utf-8")).hexdigest()
    (d / "config.json").write_text(json.dumps(record), encoding="utf-8")
    shutil.copy2(MODULE, d / "unfold.js")
    (d / "photos").mkdir()
    for p in PHOTOS:
        shutil.copy2(p, d / "photos" / p.name)
    shutil.copy2(ROOT / "tests" / "fixture_pass_unfold.html", d / "index.html")
    return d


def ready(br, tries=120):
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


def roads(br, at, tag):
    """BOTH ROADS AT ONE POSE. The port's own values() answers the raw fold behind the dial, the
    module is rebuilt on the work whose sheet the port stands at that instant, and that same raw fold
    is handed to it — so the two roads stand at ONE fold rather than at two readings of one dial."""
    r = js(br, "return window.__both(%r);" % at)
    br.sleep(0.55)
    br.evaluate("window.__mask(0); window.__hostDraw(); 0")
    br.sleep(0.15)
    br.evaluate("window.__show('host'); 0")
    br.sleep(0.25)
    ph = png(br, SHOTS / (tag + "-host.png"))
    br.evaluate("window.__show('module'); 0")
    br.sleep(0.3)
    pm = png(br, SHOTS / (tag + "-module.png"))
    br.evaluate("window.__show('host'); 0")
    return r, ph, pm


def panel_map(br, at, tag):
    js(br, "return window.__both(%r);" % at)
    br.sleep(0.35)
    br.evaluate("window.__mask(1); window.__hostDraw(); 0")
    br.sleep(0.15)
    br.evaluate("window.__show('host'); 0")
    br.sleep(0.25)
    p = png(br, SHOTS / ("map-" + tag + ".png"))
    br.evaluate("window.__mask(0); 0")
    return p


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
            elif not js(br, "return !!window.__exPass.bench.manifest('unfold');"):
                why = js(br, "var e = window.__host.report().events.filter(function(x){"
                             "return x.name === 'manifest-refused';});"
                             "return e.length ? e[e.length - 1].why : null;")
                for r in BROWSER_ROWS:
                    check(r, False, "the host registered no «unfold» instrument: " + str(why))
            else:
                SCORE = json.dumps(unfold_score())
                SCORE_UNDER = json.dumps(unfold_score(under=True))

                # ---- §8: the manifest, read off the registered instrument -----------------------
                m = js(br, "return window.__exPass.bench.manifest('unfold');")
                res = m["resources"]
                need = ["id", "api", "arity", "roles", "params", "handles", "neutrals", "doors",
                        "framings", "drivers", "camera", "gl", "passes", "resources",
                        "capabilities", "decline", "provenance", "readiness", "coverage", "levels"]
                shape = (
                    all(k in m for k in need)
                    and m["id"] == "unfold" and m["api"] == 1 and m["arity"] == 2
                    and m["roles"] == ["disassembly", "mystery", "assembly"]
                    and sorted(m["params"]) == ["depth", "panels", "shade", "stagger", "tilt"]
                    and len(m["handles"]) == 8
                    and all(set(h) >= {"min", "max", "def"} for h in m["handles"].values())
                    and m["neutrals"] == {"a": 0, "b": 1}
                    and m["doors"]["in"]["handle"] == "mix" and m["doors"]["in"]["value"] == 0
                    and m["doors"]["out"]["handle"] == "mix" and m["doors"]["out"]["value"] == 1
                    and sorted(m["framings"]) == ["0", "1"]
                    and m["framings"]["0"] == {"coverCrop": 1} == m["framings"]["1"]
                    and m["camera"] == {"needs": "none", "authority": "stage"}
                    and m["gl"] == {"preserveDrawingBuffer": False}
                    and len(m["passes"]) == 1 and len(m["passes"][0]["uniforms"]) == 12
                    and sorted(res) == ["lean", "rich", "standard"]
                    and all("bytesEstimate" in res[v] and res[v]["programs"] == 1
                            and res[v]["passes"] == 1 and res[v]["textureSlots"] == 2
                            for v in res)
                    and m["capabilities"] == ["webgl2"] and m["decline"]
                    and m["coverage"]["writes"] is False and m["coverage"]["how"]
                    and m["provenance"]["labPath"] == "lab/effects/unfold.js"
                    and m["provenance"]["commit"] == "4c7dfe4"
                    and m["readiness"] == "production-ready"
                    and "unfold" in js(br, "return window.__host.report().registered;"))
                check(BROWSER_ROWS[0], shape,
                      f"eight handles, twelve uniforms in one pass, both doors at the plain cover "
                      f"fit of {m['framings']['0']['coverCrop']}, resources declared for three tiers "
                      f"with a byte estimate of {res['standard']['bytesEstimate']}, and a coverage "
                      f"block reading «{m['coverage']['how']}»")

                check(BROWSER_ROWS[1],
                      m["levels"] == ["CELL", "CELL CONTENT"]
                      and "WHERE THIS STANDS ON THE CHARTER'S SHELF" in
                      SOURCE.read_text(encoding="utf-8"),
                      f"levels={m['levels']}. CELL is carried from the module's own row in "
                      f"lab/data/module-contract.json rather than re-decided; CELL CONTENT is read "
                      f"off the construction and said to be derived — each panel shows its own "
                      f"quarter while it lies flat and the mirror of the closing quarter once it has "
                      f"turned, which is a named region's content changing inside the region. The "
                      f"census records CELL CONTENT as held by no landed instrument. SURFACE is not "
                      f"claimed")

                br.evaluate("window.__clock(%r); 0" % CLOCK)
                br.sleep(0.7)

                w = int(br.evaluate("String(window.__exPass.bench.make() && "
                                    "document.querySelector('canvas').width)"))
                h = int(br.evaluate("String(document.querySelector('canvas').height)"))
                towers = work_in_the_frame(BENCH / "photos" / "towers.jpg", w, h)
                glass = work_in_the_frame(BENCH / "photos" / "glassgrid.jpg", w, h)
                qtowers = quarter_in_the_frame(BENCH / "photos" / "towers.jpg", w, h)
                qglass = quarter_in_the_frame(BENCH / "photos" / "glassgrid.jpg", w, h)

                # ---- the poses, on both roads ---------------------------------------------------
                FLAT = [("door-0", 0.0), ("shut-a", SHUT_IN), ("shut-b", SHUT_OUT), ("door-1", 1.0)]
                FOLD = [("q1", 0.20), ("q2", 0.32), ("q3", 0.68), ("q4", 0.80)]
                shots, reads = {}, {}
                for tag, at in FLAT + FOLD:
                    reads[tag], hp, mp = roads(br, at, tag)
                    shots[tag] = (hp, mp)

                for i, (door, own, other, ownn, othern) in enumerate((
                        ("door-0", towers, glass, "towers.jpg", "glassgrid.jpg"),
                        ("door-1", glass, towers, "glassgrid.jpg", "towers.jpg"))):
                    a, amx = apart(shots[door][0], own)
                    check(BROWSER_ROWS[2 + i * 2], a <= SEAM,
                          f"{door} against {ownn}: mean {a:.4f} of 255 (threshold {SEAM}), worst "
                          f"channel {amx}. The module's repair of 2026-08-13 made the sheet the file "
                          f"COVER-fitted and put the room the lean needs on a gate that stands at "
                          f"nothing at either end, so a door is the file with no crop and no upscale")
                    o, _ = apart(shots[door][0], other)
                    check(BROWSER_ROWS[3 + i * 2], o >= FAR,
                          f"{door} against {othern}: mean {o:.4f} of 255 (must exceed {FAR})")

                shut = [("shut-a", qtowers, "towers.jpg"), ("shut-b", qglass, "glassgrid.jpg")]
                shut_read = [(t, ) + apart(shots[t][0], q) + (n, ) for t, q, n in shut]
                check(BROWSER_ROWS[6],
                      all(mn <= SEAM for _, mn, _, _ in shut_read),
                      "; ".join(f"{t} against the top-left quarter of {n}: mean {mn:.4f} of 255 "
                                f"(threshold {SEAM}), worst channel {mx}"
                                for t, mn, mx, n in shut_read)
                      + ". At the far door of the fold the growth stands at exactly two and the "
                        "frame's edge falls on the standing panel's own hinges, so the frame is that "
                        "one quarter at exactly the framing the whole work stood at")

                # THE EXCHANGE ITSELF. At the middle of the hand the two quarters stand at half each,
                # so the frame is their average — which is what a dissolve of two flat pictures is.
                from PIL import Image, ImageChops
                js(br, "return window.__both(0.5);")
                br.sleep(0.5)
                br.evaluate("window.__mask(0); window.__hostDraw(); window.__show('host'); 0")
                br.sleep(0.3)
                midp = png(br, SHOTS / "exchange-mid.png")
                blend = ImageChops.blend(qtowers, qglass, 0.5)
                bmn, bmx = apart(midp, blend)
                da, _ = apart(midp, qtowers)
                db, _ = apart(midp, qglass)
                check(BROWSER_ROWS[7],
                      bmn <= SEAM and da > SEAM and db > SEAM,
                      f"the frame at the middle of the hand stands {bmn:.4f} of 255 from the two "
                      f"quarters averaged (threshold {SEAM}, worst channel {bmx}), {da:.4f} from the "
                      f"first alone and {db:.4f} from the second. The sheet has stood shut since "
                      f"{SHUT_IN} of the hand and stays shut until {SHUT_OUT}, so the whole exchange "
                      f"happens on one flat picture and nothing is folded while it does")

                flat_agree = [(t, ) + diff(*shots[t]) for t, _ in FLAT]
                check(BROWSER_ROWS[8], all(mn <= FLAT_SAME for _, mn, _ in flat_agree),
                      "; ".join(f"{t}: mean {mn:.4f} of 255 (bar {FLAT_SAME}), worst channel {mx}"
                                for t, mn, mx in flat_agree)
                      + ". At these four poses the sheet stands square, nothing turns and nothing "
                        "leans, so what is left between the two roads is the two samplers: the host "
                        "reads the file with GL_LINEAR at the buffer's own size and the compositor "
                        "scales the same file with its own filter")

                fold_agree = [(t, reads[t]["fold"]) + diff(*shots[t]) for t, _ in FOLD]
                check(BROWSER_ROWS[9], all(mn <= FOLD_SAME for _, _, mn, _ in fold_agree),
                      "; ".join(f"{t} at raw fold {f:.4f}: mean {mn:.4f} of 255 (bar {FOLD_SAME}), "
                                f"worst channel {mx}" for t, f, mn, mx in fold_agree)
                      + ". Through the fold the compositor also antialiases seven panel edges and "
                        "rasterises seven gradients, and this shader draws each of them at one point "
                        "with no coverage of its own. The four red-on-bug proofs below move this "
                        "same number by a wide multiple of the bar")

                # ---- §7: the frame is covered, read off the panel map ----------------------------
                maps = []
                for tag, at in FLAT + FOLD:
                    maps.append((tag, unclaimed(panel_map(br, at, tag))))
                check(BROWSER_ROWS[10], all(s == 0.0 for _, s in maps),
                      "; ".join(f"{t}: {s * 100:.4f}% unclaimed" for t, s in maps)
                      + ". The panel map paints which panel stands at each point of the frame and "
                        "leaves black exactly where none does. It is black nowhere, which is the "
                        "growth law measured on the picture rather than argued: what a panel gives "
                        "up by turning, the sheet takes back by growing")
                br.evaluate("window.__mask(0); window.__show('host'); 0")

                # ---- §7: the placement its declaration buys --------------------------------------
                # THE ROOF CASE IS READ OVER A FLOOR THAT IS ITSELF LAWFUL, so the reason that comes
                # back is this instrument's own. The woven instrument fills the frame too, so it may
                # stand lowest; laid over it, this one is refused by name.
                place = js(br, """
                  var b = window.__exPass.bench;
                  return {declared: b.coverageOf('unfold'),
                          asGround: b.coverageWhyNo([
                            {id: 'ground', instrument: {id: 'unfold', api: 1}, stack: 0},
                            {id: 'over', instrument: {id: 'matter', api: 1}, stack: 1}]),
                          asRoof: b.coverageWhyNo([
                            {id: 'floor', instrument: {id: 'weave', api: 1}, stack: 0},
                            {id: 'ground', instrument: {id: 'unfold', api: 1}, stack: 1}])};
                """)
                took_stack = js(br, "return window.__offer(%s, {clock: 1.5, progress: 0.3});"
                                % SCORE_UNDER)
                br.sleep(0.4)
                br.evaluate("window.__cancel('placement row'); 0")
                idle(br)
                check(BROWSER_ROWS[11],
                      place["declared"] and place["declared"]["writes"] is False
                      and place["asGround"] is None
                      and isinstance(place["asRoof"], str) and "«unfold»" in place["asRoof"]
                      and took_stack["took"],
                      f"the host reads this instrument's declaration as writes="
                      f"{place['declared']['writes']} and places it by it. Laid lowest with a "
                      f"coverage-writing voice above, the stack is lawful and the host takes the "
                      f"score. Laid over a floor that is itself lawful, it is refused by name: "
                      f"«{place['asRoof']}». The ground is what 1 320 declined plans are counted "
                      f"waiting for")

                # EACH END OF THE STACK BELONGS TO THE VOICE THAT DECLARED IT. At the near door the
                # voice above carries no matter at all — `matter` writes an alpha of 0 across the
                # whole frame at its own `mix` of 0 (COVERAGE.md §3.3) — so the frame is this
                # instrument's whole work, which is what a ground is for. At the far door that voice
                # is opaque and the door is its own: `texB` whole under the crop its manifest
                # publishes. Both ends are measured against the work each of them actually stands.
                over_crop = js(br, "return window.__exPass.bench.manifest('matter')"
                                   ".framings['1'].coverCrop;")
                stack_doors = []
                for at, work, name in (
                        (0.0, towers, "towers.jpg, seated by this instrument"),
                        (1.0, work_in_the_frame(BENCH / "photos" / "glassgrid.jpg", w, h,
                                                over_crop),
                         "glassgrid.jpg under the arriving voice's own crop of %s" % over_crop)):
                    js(br, "return window.__offer(%s, {clock: 1.5, progress: %r});"
                       % (SCORE_UNDER, at))
                    br.sleep(0.7)
                    p = png(br, SHOTS / ("stack-door-%03d.png" % round(at * 100)))
                    br.evaluate("window.__cancel('stack door row'); 0")
                    idle(br)
                    stack_doors.append((at, name) + apart(p, work))
                check(BROWSER_ROWS[12],
                      all(mn <= SEAM for _, _, mn, _ in stack_doors),
                      "; ".join(f"door {at} against {n}: mean {mn:.4f} of 255 (threshold {SEAM}), "
                                f"worst channel {mx}" for at, n, mn, mx in stack_doors)
                      + ". A ground has to close its own frame at both ends or the cleared buffer "
                        "shows through the door the visitor lands on; here the near door is this "
                        "instrument's whole work through a transparent voice, and the far door is "
                        "that voice standing opaque on its own declared framing")

                # ---- §7: no empty frame, and the redraw the preserved buffer stood in for --------
                empties = []
                for at in (0.0, 0.15, 0.3, 0.5, 0.7, 0.85, 1.0):
                    js(br, "return window.__offer(%s, {clock: 1.5, progress: %r});" % (SCORE, at))
                    br.sleep(0.5)
                    p = png(br, SHOTS / ("instant-%03d.png" % round(at * 100)))
                    empties.append((at, ) + standing(p))
                    br.evaluate("window.__cancel('instant sweep'); 0")
                    idle(br)
                check(BROWSER_ROWS[13],
                      all(d >= FAR and s >= SPREAD for _, d, s in empties),
                      "; ".join(f"at {at}: {d:.2f} from the background, spread {s:.2f}"
                                for at, d, s in empties)
                      + f" (bars: {FAR} and {SPREAD}); sampled on the one-cue score, where this "
                        f"instrument is the whole frame")

                js(br, "return window.__offer(%s, {clock: 1.5, progress: 0.3});" % SCORE)
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
                check(BROWSER_ROWS[14],
                      d >= FAR and s >= SPREAD and sized["pdb"] is False,
                      f"after the viewport moved to {VW - 80}x{VH - 120} the buffer reads "
                      f"{sized['buffer']} and the frame stands {d:.2f} from the background with a "
                      f"spread of {s:.2f}; the context keeps preserveDrawingBuffer={sized['pdb']}. "
                      f"The sheet is cut from the seating the host recomputes at the new size, so "
                      f"the panels are re-solved rather than re-shown")

                # ---- the seeded repeat -----------------------------------------------------------
                br.sleep(0.6)
                took = js(br, "return window.__offer(%s, {clock: 1.5, progress: 0.3});" % SCORE)
                br.sleep(1.2)
                first = png(br, SHOTS / "seeded-1.png")
                rep1 = js(br, "return window.__report();")
                br.evaluate("window.__cancel('between runs'); 0")
                idle(br)
                js(br, "return window.__offer(%s, {clock: 1.5, progress: 0.3});" % SCORE)
                br.sleep(1.2)
                second = png(br, SHOTS / "seeded-2.png")
                mn, mx = diff(first, second)
                check(BROWSER_ROWS[15], took["took"] and mn == 0.0 and mx == 0,
                      f"took={took['took']} two runs of one seeded score: mean {mn} worst channel "
                      f"{mx}. Every number the shader reads comes from a handle or from the second "
                      f"the host hands down, and the module's own fifteen-second breath is gone")

                # ---- ten runs, and the baseline --------------------------------------------------
                base_c = rep1["census"]
                for _ in range(10):
                    js(br, "return window.__offer(%s, {clock: 2.0, progress: 0.3});" % SCORE)
                    br.sleep(0.12)
                    br.evaluate("window.__cancel('leak row'); 0")
                br.sleep(0.4)
                after = js(br, "return window.__report();")["census"]
                same = (after["textures"] == base_c["textures"] == 2
                        and after["programs"] == base_c["programs"]
                        and after["framebuffers"] == base_c["framebuffers"] == 0
                        and after["canvases"] == base_c["canvases"] == 1
                        and after["contexts"] == base_c["contexts"] == 1)
                check(BROWSER_ROWS[16], same,
                      f"before={base_c['textures']}/{base_c['programs']}/{base_c['framebuffers']} "
                      f"after ten runs={after['textures']}/{after['programs']}/{after['framebuffers']} "
                      f"(textures/programmes/framebuffers)")

                errs = json.loads(br.evaluate("JSON.stringify(window.__errs||[])"))
                check(BROWSER_ROWS[17], not errs, "; ".join(errs)[:200])

                # THE CENSUS IS READ ON A BENCH OF ITS OWN, and the reason is the programme cache:
                # it holds one entry per branch and outlives every transaction, so a session that has
                # already drawn another instrument grants two programmes to a score declaring one.
                r = on_bench(lambda b2: (
                    js(b2, "return window.__offer(%s, {clock: 1.0, progress: 0.4});" % SCORE),
                    b2.sleep(0.8),
                    js(b2, "return window.__report();")["resources"])[-1])
                check(BROWSER_ROWS[18],
                      r and r["declared"] and r["over"] is False
                      and r["granted"]["textures"] == r["declared"]["textures"]
                      and r["granted"]["programs"] == r["declared"]["programs"] == 1
                      and r["granted"]["framebuffers"] == r["declared"]["framebuffers"]
                      and r["granted"]["bytes"] == r["declared"]["bytesEstimate"],
                      f"declared={r and r['declared']} granted={r and r['granted']}")

                js(br, "return window.__offer(%s, {clock: 1.0, progress: 0.4});" % SCORE)
                br.sleep(0.6)
                cen = js(br, "return window.__report();")["census"]
                check(BROWSER_ROWS[19],
                      cen["canvases"] == 1 and cen["contexts"] == 1 and cen["textures"] == 2
                      and cen["passesLastFrame"] == 1 and cen["framebuffers"] == 0
                      and cen["preserveDrawingBuffer"] is False,
                      f"census={cen}; the module's own twenty-two DOM elements and the compositor "
                      f"work behind each of them are what this port does without")
                br.evaluate("window.__cancel('census row'); 0")
                idle(br)

                r = js(br, """
                  var m = window.__exPass.bench.manifest('unfold');
                  var plain = window.__exPass.bench.es3(m.passes[0].frag, false);
                  var already = window.__exPass.bench.es3('#version 300 es\\n' + m.passes[0].frag, false);
                  var count = function (s) { return s.split('#version').length - 1; };
                  return {source: count(m.passes[0].frag), stamped: count(plain),
                          untouched: count(already), head: plain.slice(0, 15)};
                """)
                check(BROWSER_ROWS[20],
                      r["source"] == 0 and r["stamped"] == 1 and r["untouched"] == 1
                      and r["head"].startswith("#version 300 es"),
                      f"the shader carries {r['source']} headers, the translator leaves it with "
                      f"{r['stamped']}, and a source that already carries one comes back with "
                      f"{r['untouched']}")

                # ---- curtain up, one pass drawn, exactly one dock --------------------------------
                br.evaluate("window.__cancel('before the whole pass'); 0")
                idle(br, nap=0.05)
                br.evaluate("window.__hooks.docks.length = 0; window.__hooks.curtains.length = 0; 0")
                took = js(br, "return window.__offer(%s, {});" % SCORE)
                br.sleep(0.5)
                mid = js(br, "return {state: window.__report().state, "
                             "curtains: window.__hooks.curtains.slice()};")
                idle(br)
                end = js(br, "return {state: window.__report().state, docks: window.__hooks.docks.slice(), "
                             "curtains: window.__hooks.curtains.slice(), "
                             "events: window.__report().events.map(function(e){return e.name;}).slice(-6)};")
                check(BROWSER_ROWS[21],
                      took["took"] and mid["state"] == "running" and mid["curtains"][:1] == [True]
                      and end["state"] == "idle" and len(end["docks"]) == 1
                      and end["curtains"][-1] is False and "docked" in end["events"],
                      f"mid={mid} end={end}")

                cam = js(br, "var r = window.__report(); "
                             "return {camera: r.camera, rest: r.rest, handoffs: r.handoffs, "
                             "tol: r.camTolerances};")
                check(BROWSER_ROWS[22],
                      cam["camera"] and cam["camera"]["owner"] == "stage"
                      and cam["handoffs"] == []
                      and cam["rest"] and cam["rest"]["rested"] is True
                      and cam["rest"]["off"] <= cam["tol"]["rest"],
                      f"owner={cam['camera'] and cam['camera']['owner']} rest={cam['rest']} "
                      f"handoffs={cam['handoffs']} tolerances={cam['tol']} — the fold moves no point "
                      f"of view, so the stage holds the camera for the whole pass")

                # ---- §4.4b: the handles reach the picture ----------------------------------------
                shot = {}
                for name, extra in (("base", {}), ("tilt", {"tilt": 0.0}), ("shade", {"shade": 0.0}),
                                    ("depth", {"depth": 1.0}), ("stagger", {"stagger": 0.0}),
                                    ("panels", {"panels": 0})):
                    js(br, "return window.__offer(%s, {clock: 1.5, progress: 0.3});"
                       % json.dumps(unfold_score(**extra)))
                    br.sleep(0.7)
                    shot[name] = png(br, SHOTS / ("handle-" + name + ".png"))
                    br.evaluate("window.__cancel('handle row'); 0")
                    idle(br)
                moved = {k: diff(shot["base"], shot[k])
                         for k in ("tilt", "shade", "depth", "stagger", "panels")}
                check(BROWSER_ROWS[23],
                      all(mn > SEAM for mn, _ in moved.values()),
                      "; ".join(f"{k} moves the frame by {mn:.4f} of 255 (worst channel {mx})"
                                for k, (mn, mx) in moved.items())
                      + f"; the seam threshold is {SEAM}. A handle a score drives and the picture "
                        f"ignores is what §4.4b is about")

                kept = sorted(p.name for p in SHOTS.glob("*.png"))
                check(BROWSER_ROWS[24],
                      len(kept) >= 35 and all((SHOTS / k).stat().st_size > 1000 for k in kept),
                      f"{len(kept)} captures under {SHOTS.relative_to(ROOT)}: the eight poses on "
                      f"both roads, their eight panel maps, the exchange at its middle, the two "
                      f"doors in a stack, the seven sampled instants, the frame after a resize, the "
                      f"two seeded runs and the six handle runs")

                # ---- THE PANEL MAP, WALKED ON THE BUFFER --------------------------------------
                # The rows above photograph the map and read it as colour. This one asks the
                # INSTRUMENT what it read for itself at the instant it was about to draw, on the
                # grid the shader samples on. The growth law's promise — that no point of the frame
                # is left with no panel standing on it — is a claim about a GRID, and it is now
                # walked at the buffer's own sample points instead of being declared: the four
                # corners, where the law has the least to spare, the midpoints of the four edges,
                # and the nine points where the panels' own seams cross at a door. What comes back
                # is published, so a later change to the fold, the stagger or the growth law reddens
                # here whatever the pictures do.
                def door_pose(mix=0, buf=None, **over):
                    p = {"mix": mix, "tilt": 0.5, "shade": 1, "depth": 0.5, "stagger": 0.34,
                         "panels": 1, "mask": 0, "t": 0, "reduced": False,
                         "cssWidth": VW, "cssHeight": VH}
                    p.update(over)
                    if buf:
                        p["bufWidth"], p["bufHeight"] = int(buf[0]), int(buf[1])
                    return p

                def values_of(p):
                    return js(br, "return window.__exPass.bench.values('unfold', %s);"
                              % json.dumps(p))

                def per_door_ms(p, n=2000):
                    return js(br, "var p = %s, b = window.__exPass.bench;"
                                  "for (var i = 0; i < 400; i++) b.values('unfold', p);"
                                  "var t0 = performance.now();"
                                  "for (var j = 0; j < %d; j++) b.values('unfold', p);"
                                  "return {ms: (performance.now() - t0) / %d};"
                                  % (json.dumps(p), n, n))["ms"]

                grids = [(VW, VH), (VW * 2, VH * 2), (195, 422), (1440, 900), (40, 60)]
                maps = {}
                for mixv in (0, 1):
                    for panels in (1, 0):
                        for g in grids:
                            maps[(mixv, panels, g)] = values_of(
                                door_pose(mix=mixv, panels=panels, buf=g))
                away = values_of(door_pose(mix=0.5, buf=grids[0]))
                on_css = values_of(door_pose())
                worst = [k for k, v in maps.items()
                         if v["panelMap"] is None or v["panelMap"]["bare"] != 0
                         or v["panelMap"]["scale"] != 1 or v["panelMap"]["turnPx"] != 0
                         or v["panelMap"]["seamPx"] != 1
                         or v["panelMap"]["walked"] != 17
                         or v["doorWhyNo"] is not None]
                ms = per_door_ms(door_pose(buf=grids[1]))
                check(BROWSER_ROWS[25],
                      not worst and len(maps) == 20
                      and on_css["doorGrid"] == {"w": VW, "h": VH, "drawn": False}
                      and maps[(0, 1, grids[0])]["doorGrid"] == {"w": VW, "h": VH, "drawn": True}
                      and maps[(0, 1, grids[0])]["panelMap"]["panels"] == 4
                      and maps[(0, 0, grids[0])]["panelMap"]["panels"] == 2
                      and away["panelMap"] is None and away["doorGrid"] is None,
                      "%d readings — both doors, both panel counts, five grids from %s to %s — and "
                      "every one of them walked %d points of the buffer with %d bare, the growth "
                      "law's own scale at %g, the seam at %g point of the grid and neither pair out "
                      "of the sheet's plane. Away from a door nothing is read at all (grid %s). One "
                      "door instant costs %.4f ms on this machine. The panel map at the entry door "
                      "on %s: %s"
                      % (len(maps), "%dx%d" % grids[0], "%dx%d" % grids[4],
                         maps[(0, 1, grids[0])]["panelMap"]["walked"],
                         maps[(0, 1, grids[0])]["panelMap"]["bare"],
                         maps[(0, 1, grids[0])]["panelMap"]["scale"],
                         maps[(0, 1, grids[0])]["panelMap"]["seamPx"],
                         away["doorGrid"], ms, "%dx%d" % grids[1],
                         maps[(0, 1, grids[1])]["panelMap"]))

                # ---- THE DOOR REFUSED ON THE REAL TRANSACTION ROAD ---------------------------
                # The map above comes out whole on every buffer this host can hand and every pose
                # these handles admit — at a door the fold is exactly 0, the sheet lies flat and the
                # growth law's scale is exactly 1 — which is the runtime truth this lane was asked
                # for and not a reason to leave the claim unread. The one door this instrument's own
                # handles CAN spoil is the judges' channel: `mask` draws the panel map itself as
                # colour, which is what it is for, and a score that leaves it open at a door hands
                # the visitor a false-colour map of the panels instead of the photograph. This row
                # puts that on the real road and asks the host to land the visitor on the reason.
                def road(gen):
                    return js(br, "var r = window.__report(); return {state: r.state, "
                                  "drew: r.drew, buffer: r.census.buffer, "
                                  "refused: r.events.filter(function(e){ return e.gen === %d "
                                  "&& e.why && String(e.why).indexOf('door leaks') >= 0; })"
                                  ".map(function(e){ return e.name + ': ' + e.why; })};" % gen)

                br.evaluate("window.__cancel('door road row'); 0")
                idle(br)
                shut_gen = js(br, "return window.__offer(%s, {clock: 0, progress: 0});"
                              % json.dumps(unfold_score(mask=0)))["gen"]
                br.sleep(1.0)
                played = road(shut_gen)
                br.evaluate("window.__cancel('door road row'); 0")
                idle(br)
                open_gen = js(br, "return window.__offer(%s, {clock: 0, progress: 0});"
                              % json.dumps(unfold_score(mask=1)))["gen"]
                br.sleep(1.1)
                leaked = road(open_gen)
                br.evaluate("window.__cancel('door road row'); 0")
                idle(br)
                check(BROWSER_ROWS[26],
                      played["state"] == "running" and played["drew"] == 1
                      and not played["refused"]
                      and len(leaked["refused"]) == 1 and leaked["state"] == "idle"
                      and leaked["drew"] == 0
                      and "the entry door leaks" in leaked["refused"][0]
                      and "the judges' own channel" in leaked["refused"][0]
                      and ("%s buffer" % played["buffer"].replace("x", " x ")) in leaked["refused"][0],
                      "on the %s buffer the host drew, the judges' channel shut draws the door (%d "
                      "cue, state %s, refused %s); left open it is refused with «%s», on which the "
                      "host lands the transaction (state %s, %d cue drawn) and the walk's own glide "
                      "carries the visitor"
                      % (played["buffer"], played["drew"], played["state"],
                         played["refused"] or "nothing",
                         (leaked["refused"] or ["nothing refused"])[0], leaked["state"],
                         leaked["drew"]))

    shutil.rmtree(BENCH, ignore_errors=True)

    # ================================================================================================
    # THE RED-ON-BUG PROOFS. Each reverts one rule this port states, in the artifact the browser
    # actually loads, and reads the number that moved. The pack served is changed and the host is
    # re-stamped with the digest of the bytes it is handed, which is what the build does; the file on
    # disk is never touched, so no working tree can be left changed by a proof.
    # ================================================================================================
    def worst_unclaimed(br, ats, params=None):
        out = []
        br.evaluate("window.__clock(%r); 0" % CLOCK)
        for k, v in (params or {}).items():
            br.evaluate("window.__param(%s, %r); 0" % (json.dumps(k), v))
        br.sleep(0.5)
        for at in ats:
            out.append(unclaimed(panel_map(br, at, "red-%03d" % round(at * 100))))
        return max(out)

    def road_gap(br, at):
        br.evaluate("window.__clock(%r); 0" % CLOCK)
        br.sleep(0.5)
        _, hp, mp = roads(br, at, "red-road")
        return diff(hp, mp)[0]

    def door_gap(br):
        br.evaluate("window.__clock(%r); 0" % CLOCK)
        br.sleep(0.5)
        _, hp, _ = roads(br, 0.0, "red-door")
        w = int(br.evaluate("String(document.querySelector('canvas').width)"))
        hh = int(br.evaluate("String(document.querySelector('canvas').height)"))
        return apart(hp, work_in_the_frame(PHOTOS[0], w, hh))[0]

    if missing or not chrome_available():
        pass
    else:
        # ---- 1. the growth law removed -----------------------------------------------------------
        MID = [0.2, 0.32, 0.68, 0.8]
        base_fill = on_bench(lambda b: worst_unclaimed(b, MID))
        bug = PACK.replace("float sc = room * max(max(aspect / (2.0 * extX), 1.0 / (2.0 * extY)), 1.0);",
                           "float sc = room;", 1)
        bug_fill = on_bench(lambda b: worst_unclaimed(b, MID), pack_text=bug)
        check(RED_ROWS[0],
              bug != PACK and base_fill is not None and bug_fill is not None
              and base_fill == 0.0 and bug_fill > 0.01,
              f"the growth law grows the sheet until what still stands covers the frame, with the "
              f"lean's room on top. With it standing, the panel map is unclaimed at "
              f"{base_fill * 100:.4f}% of the frame at the worst of the four folded poses. With the "
              f"growth taken out and the sheet left at its own size, {bug_fill * 100:.2f}% of the "
              f"frame is bare — which is the whole reason a fading panel was never the answer: a "
              f"panel leaves the frame by turning, at full strength")

        # ---- 2. the corner's own foreshortening removed -------------------------------------------
        # READ WHERE THE MODULE ITSELF MEASURED IT: the eye at its nearest and both pairs turning
        # together, which is `depth` at 1 and `stagger` at nothing.
        BOTH_TURN = [0.28, 0.34, 0.4]
        NEAR = {"depth": 1.0, "stagger": 0.0}
        base_corner = on_bench(lambda b: worst_unclaimed(b, BOTH_TURN, NEAR))
        bug = PACK.replace("float corner = deep / (deep + sY + (CH / CW) * sX);",
                           "float corner = 1.0;", 1)
        bug_corner = on_bench(lambda b: worst_unclaimed(b, BOTH_TURN, NEAR), pack_text=bug)
        check(RED_ROWS[1],
              bug != PACK and base_corner is not None and bug_corner is not None
              and base_corner == 0.0 and bug_corner > 0.001,
              f"a turned panel is counted for what it covers on the SCREEN, where the plain cosine "
              f"counts what a flat drawing would cover: the far corner is carried away by both turns "
              f"at once and is "
              f"drawn smaller. Counting the plain cosine there opened a triangle of bare frame, and "
              f"the module records the reading it opened at (0.9653 of the frame filled). With the "
              f"corner's own foreshortening standing, nothing is unclaimed at either pose "
              f"({base_corner * 100:.4f}%); with it held at 1, {bug_corner * 100:.4f}% is bare")

        # ---- 3. the mirror taken on at once -------------------------------------------------------
        base_door = on_bench(door_gap)
        bug = PACK.replace("uLean.w);", "1.0);", 3)
        bug_door = on_bench(door_gap, pack_text=bug)
        check(RED_ROWS[2],
              bug != PACK and base_door is not None and bug_door is not None
              and base_door <= SEAM and bug_door > SEAM,
              f"each panel carries ITS OWN quarter of the work while it lies flat and takes on the "
              f"mirror over its first fourteen degrees of turn, so the near door is the work as the "
              f"file carries it. Before that repair every panel carried the same region and door 0 "
              f"stood a picture REBUILT from the top-left quarter; the arsenal read 10.83 and 42.46 "
              f"of 255 against a bar of 6.0. With the swap standing, door 0 is {base_door:.4f} of "
              f"255 from its own file; with the mirror taken on at once it is {bug_door:.4f}")

        # ---- 4. the seating removed ---------------------------------------------------------------
        base_seat = on_bench(lambda b: road_gap(b, 0.32))
        bug = PACK.replace("vec2 SZ = vec2(aspect / max(fit.x, 1e-4), 1.0 / max(fit.y, 1e-4));",
                           "vec2 SZ = vec2(aspect, 1.0);", 1)
        bug_seat = on_bench(lambda b: road_gap(b, 0.32), pack_text=bug)
        check(RED_ROWS[3],
              bug != PACK and base_seat is not None and bug_seat is not None
              and base_seat <= FOLD_SAME and bug_seat > FOLD_SAME,
              f"the sheet the panels are cut from is the file COVER-fitted over the frame, which is "
              f"exactly the seating the host computes and hands down; the shader recovers the "
              f"sheet's own width and height from it. With the seating standing, the two roads agree "
              f"at {base_seat:.4f} of 255 through the fold; with the sheet read as the frame instead "
              f"they part at {bug_seat:.4f}, against a bar of {FOLD_SAME}")

        # ---- 5. the door reading removed ---------------------------------------------------------
        # The lane's own rule, reverted in the artifact the browser loads: the bar under which a
        # reading cannot be a leak is taken past 1, so nothing the reading finds ever refuses — the
        # instrument as it stood before it read its doors at runtime, declaring both doors whole and
        # never checking. The number that moves is what the HOST is told: with the reading standing,
        # a door drawing the panel map instead of the photograph is refused and the transaction
        # lands; with it removed the same command draws that map to the visitor.
        def red_five(br):
            gen = js(br, "return window.__offer(%s, {clock: 0, progress: 0});"
                     % json.dumps(unfold_score(mask=1)))["gen"]
            br.sleep(1.2)
            r = js(br, "var r = window.__report(); return {state: r.state, drew: r.drew, "
                       "buffer: r.census.buffer, refused: r.events.filter(function(e){ "
                       "return e.gen === %d && e.why "
                       "&& String(e.why).indexOf('door leaks') >= 0; }).length};" % gen)
            br.evaluate("window.__cancel('red five'); 0")
            return r

        base_door_read = on_bench(red_five)
        bug = PACK.replace("var DOOR_SHOW = 0.5 / 255;", "var DOOR_SHOW = 2;", 1)
        bug_door_read = on_bench(red_five, pack_text=bug)
        check(RED_ROWS[4],
              bug != PACK and base_door_read and bug_door_read
              and base_door_read["refused"] == 1 and base_door_read["state"] == "idle"
              and base_door_read["drew"] == 0
              and bug_door_read["refused"] == 0 and bug_door_read["state"] == "running"
              and bug_door_read["drew"] == 1,
              f"with the judges' channel open at the entry door on the "
              f"{base_door_read and base_door_read['buffer']} buffer, the reading tells the host so "
              f"({base_door_read and base_door_read['refused']} refusal, state "
              f"{base_door_read and base_door_read['state']}, "
              f"{base_door_read and base_door_read['drew']} cue drawn) and the walk's own glide "
              f"carries the visitor. With the bar taken past anything the reading can find, the "
              f"same command draws the panel map to the visitor instead "
              f"({bug_door_read and bug_door_read['refused']} refusals, state "
              f"{bug_door_read and bug_door_read['state']}, "
              f"{bug_door_read and bug_door_read['drew']} cue drawn)")

shutil.rmtree(TMP, ignore_errors=True)

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
