#!/usr/bin/env python3
"""The overlay instrument, proved on the frame it draws — pass-inst-overlay.js.

WHAT THIS SUITE HOLDS THE PORT TO, and why each bar is the project's own rather than one this file
invented:

  · BOTH DOORS ARE THE PHOTOGRAPH. At either end of the dominance travel the frame is one work
    standing whole, cover-fitted with no crop of its own, inside the project's seam threshold of 6 of
    255 — and standing further than 40 of 255 from the other work, which is the distance past which
    this project calls a frame another work.
  · THE TWO ROADS ARE ONE ARITHMETIC. The lab module carries its own WebGL context and its own
    fragment shader, so the port and the module run one sampler through one rasteriser and the
    residual between them is a difference of arithmetic rather than of samplers. They are stood side
    by side on a SQUARE frame with two SQUARE works, which is exactly where the one thing the port
    decided differently — the seating — costs nothing, so what the row compares is the mathematics.
  · THE INSTRUMENT READS ITS OWN DOORS. His 18:00 architecture decision. Every refusal this
    instrument can make is exercised and its wording read.
  · EVERY GEOMETRIC PARAMETER NAMES A MEASUREMENT. His 19:13 word lifted to the class at 19:21. The
    rows read the `reads:` line each handle publishes and then move the handle and read the frame.
  · THE RED-ON-BUG SET. Each proof reverts one rule this port states, in the bytes the browser is
    served and never in the file on disk, and moves a number this suite already reads by a wide
    multiple.
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
# suites of the ports before this one read them from too.
LAB = Path(os.environ.get("TLVPHOTOS_ROOT", "/Users/sashaabramovich/tlvphotos")) / "lab"
# TWO SQUARE WORKS, AND THAT IS THE ROW ABOUT THE TWO ROADS SPEAKING. The module maps the frame onto
# a square and reads a work across it whatever that work's own shape is; the port asks the host for
# the seating instead, so the two part on any work that is not square. On square works they are one
# arithmetic, which is what lets the comparison be about the mathematics — and the parting itself is
# read by its own red-on-bug row below, on the phone frame, against the file.
PHOTOS = [LAB / "photos" / "towers.jpg", LAB / "photos" / "cluster.jpg"]
MODULE = LAB / "effects" / "overlay.js"

SITE_URL = "https://synth.example.com"
VW, VH = 390, 844          # the phone frame lab/carrier-check.py measures on
SQ = 900                   # the square frame the two roads are stood side by side on
SEAM = 6.0                 # the project's seam threshold, 6 of 255 (TRANSITION-STAGE-V0 §1)
FAR = 40.0                 # further than this from a file and it is a different work
BACKGROUND = (0x08, 0x08, 0x0a)
SPREAD = 10.0
ROADS = SEAM               # the two-roads bar IS the project's bar, not one this suite made up

# The module's own measured law for the region: the share of the frame standing at presence p is p
# itself, within three parts in a hundred, whatever second of the clock it is (overlay.js:224-228).
# The module read that over a SQUARE frame; this row reads it over the phone frame, where the frame
# takes a tall slice of the field rather than a square one and the two ends of the travel lean by
# about four parts in a hundred. Five is the bar here and the measured spread stands in the row.
SHARE_SLACK = 0.05

# The two field defaults, which are the module's own base wavenumbers read back as periods. At these
# the port draws the module's own two fields, arithmetic for arithmetic.
MIX_PERIOD = 1 / 3.7
REGION_PERIOD = 1 / 7.3

SHOTS = ROOT / "tests" / "captures" / "pass-overlay"

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


DURATION_MS = 6500


def _static(v):
    return {"op": "static", "value": v}


def overlay_cue(stack=0, **statics):
    """The cue, with a track for every one of the thirteen handles (§4.4b)."""
    P = {"exposure": 1, "presence": 1, "blend": 0, "scale": 1, "turn": 0, "arrival": 0,
         "mixPeriod": MIX_PERIOD, "mixTurn": 0,
         "regionPeriod": REGION_PERIOD, "regionTurn": 0, "mask": 0}
    P.update(statics)
    nodes = {"o-mix": {"source": "progress"}, "o-clock": {"source": "time"}}
    tracks = {"mix": {"node": "o-mix"}, "clock": {"node": "o-clock"}}
    for k, v in P.items():
        nodes["o-" + k] = _static(v)
        tracks[k] = {"node": "o-" + k}
    return {
        "id": "overlay-main", "instrument": {"id": "overlay", "api": 1},
        "voice": "letter", "roles": ["disassembly", "mystery", "assembly"],
        "levels": ["LIGHT-COLOUR"],
        "levelOwnership": {"LIGHT-COLOUR": "owns"},
        "window": [0, DURATION_MS / 1000.0], "works": ["a", "b"], "stack": stack,
        "cameraAuthority": "stage",
        "doors": {"in": {"handle": "mix", "value": 0, "measured": True},
                  "out": {"handle": "mix", "value": 1, "measured": True}},
        "nodes": nodes, "tracks": tracks,
        "resources": {"textures": 0, "textureSlots": 2, "framebuffers": 0, "pingPong": 0,
                      "programs": 1, "passes": 1, "bytesEstimate": 0, "variant": "standard"},
    }


def weave_cue(stack=0):
    """THE GROUND THIS INSTRUMENT IS MEANT TO STAND ON. `weave` fills the frame, so it is what the
    placement rule asks for under a cue that writes coverage (§8 as amended 14:05)."""
    nodes = {"w-mix": {"source": "progress"}, "w-clock": {"source": "time"}}
    tracks = {"mix": {"node": "w-mix"}, "clock": {"node": "w-clock"}}
    return {
        "id": "ground", "instrument": {"id": "weave", "api": 1},
        "voice": "letter", "roles": ["disassembly", "mystery", "assembly"],
        "levels": ["SURFACE", "CELL"],
        "levelOwnership": {"SURFACE": "owns", "CELL": "owns"},
        "window": [0, DURATION_MS / 1000.0], "works": ["a", "b"], "stack": stack,
        "cameraAuthority": "stage",
        "doors": {"in": {"handle": "mix", "value": 0, "measured": True},
                  "out": {"handle": "mix", "value": 1, "measured": True}},
        "nodes": nodes, "tracks": tracks,
        "resources": {"textures": 0, "textureSlots": 2, "framebuffers": 0, "pingPong": 0,
                      "programs": 1, "passes": 1, "bytesEstimate": 0, "variant": "standard"},
    }


def overlay_score(over=False, **statics):
    """`over` puts this instrument where its own declaration places it: above a frame-filling
    ground. Alone it is a one-cue score, which the placement rule exempts."""
    cues = [overlay_cue(stack=1 if over else 0, **statics)]
    if over:
        cues = [weave_cue(stack=0)] + cues
    res = {"textures": 0, "textureSlots": 2, "framebuffers": 0, "pingPong": 0,
           "programs": 1, "passes": 1, "bytesEstimate": 0}
    return {
        "api": 1, "id": "overlay-bench", "durationMs": DURATION_MS,
        "seed": 20260808, "intent": "the double exposure, stood on the bench",
        "camera": {"authority": "stage",
                   "keys": [{"t": 0, "at": 0, "pan": {"x": 0, "y": 0}, "logScale": 0,
                             "pitch": 0, "yaw": 0, "roll": 0, "fov": None, "owner": "stage"}]},
        "cues": cues,
        "quality": {v: {"renderScale": None,
                        "cues": {c["id"]: {"resources": dict(res, variant=v)} for c in cues}}
                    for v in ("lean", "standard", "rich")},
        "provenance": {"source": "lab/effects/overlay.js's own declared defaults and constants",
                       "measuredAt": None, "by": "tests/test_pass_overlay.py"},
    }


# ---------------------------------------------------------------- bake once
build_site.SITE_CONFIG = dict(build_site.SITE_CONFIG)
build_site.SITE_CONFIG["pass"] = {"visualLayer": "pass", "diagnostics": "on"}

TMP = Path(tempfile.mkdtemp(prefix="synth_passoverlay_"))
build_site.OUT = TMP
build_site.build(SITE_URL)
LAYER = (TMP / "pass-layer.js").read_text(encoding="utf-8")
# THE INSTRUMENT'S OWN BUILT FILE — the real artifact a visitor is served, comments stripped. Since
# every instrument travels alone, the whole of this file is this instrument and nothing else.
PACK = (TMP / "pass-inst-overlay.js").read_text(encoding="utf-8")
REGION = PACK
SOURCE = ROOT / "engine" / "assets" / "pass-inst-overlay.js"
# The file as it stands in the tree, comments and all: the rows about what this instrument DECLARES
# read the built artifact, and the rows about what it SAYS read the source it is built from.
SOURCE_TEXT = SOURCE.read_text(encoding="utf-8")
LABTXT = MODULE.read_text(encoding="utf-8") if MODULE.exists() else ""

# ---------------------------------------------------------------- string rows

OWNED = ["createElement", "getContext", "requestAnimationFrame", "addEventListener",
         "performance.now", "Date.now", "new Image", "setTimeout", "setInterval"]
held = [s for s in OWNED if s in REGION]
check("PASS-OVERLAY the instrument creates no element, no loop and no listener",
      not held,
      "§1.2's fence, read against the instrument's own built file: none of the nine ways of owning "
      "hardware appears there. The module raises its own canvas, takes a WebGL2 context on it, "
      "uploads two textures with their mipmap chains, runs its own frame loop, observes its own "
      "mount for a resize and listens for the pointer across it; all of it stayed in the lab"
      if not held else "the instrument's region holds " + ", ".join(held))

HANDLES = ["mix", "clock", "exposure", "presence", "blend", "scale", "turn", "arrival",
           "mixPeriod", "mixTurn", "regionPeriod", "regionTurn", "mask"]
absent = [h for h in HANDLES if ("%s: { min" % h) not in REGION]
check("PASS-OVERLAY every handle the instrument publishes is a handle a score can drive",
      not absent and len(HANDLES) == 13,
      "§4.4b: thirteen handles. The dial the doors stand on, the second the host hands down, the "
      "module's own exposure and presence, its blend rule, its top scale and its named arrival, the "
      "counter-turn its pointer used to drive, the four that carry the two works' own lattices, and "
      "the judges' channel. The module's `pair` is published by neither, and the file says why: a "
      "cue carries an ordered pair, so there is no third picture left to choose between"
      if not absent else "these are published nowhere: " + ", ".join(absent))

check("PASS-OVERLAY the module's own hunt and its pointer are gone, and the second comes from a "
      "handle",
      "pointer" not in REGION and "0.0763" not in REGION and "0.0331" not in REGION
      and "0.16 * Math.sin(t * 0.0763)" in LABTXT
      and 'source: "seconds"' in REGION and "t: st.reduced ? 0 : h.clock" in REGION,
      "left alone the module walked its own dominance by 0.16 sin(t·0.0763) + 0.09 sin(t·0.0331 + "
      "2.1) and read the pointer across its mount for dominance and for the top layer's turn "
      "(overlay.js:536-545). A handle that walks itself makes a seeded score draw two different "
      "pictures (§4.4b), so neither came over; the one place time reaches the picture is the two "
      "layers' breath and the two fields' drift, and both read the `clock` handle")

# Every constant the picture stands on, read out of the lab module and out of the built file.
CONSTANTS = [
    ("'screen':     { pre: [0.56, 0.42, 1.06, 1.10], post: [1.00, 1.40, 1.10, 0.45] },",
     "{ pre: [0.56, 0.42, 1.06, 1.10], post: [1.00, 1.40, 1.10, 0.45] },",
     "screen's own tone: both source pictures are bright, so the two layers are held back going in"),
    ("'multiply':   { pre: [1.00, 1.00, 1.00, 1.00], post: [1.90, 1.16, 1.00, 0.42] },",
     "{ pre: [1.00, 1.00, 1.00, 1.00], post: [1.90, 1.16, 1.00, 0.42] },",
     "multiply comes out too dark and is lifted by 1.90 on the way out"),
    ("'light difference': { pre: [1.00, 1.00, 1.00, 1.00], post: [1.55, 1.10, 1.70, 0.34] }",
     "{ pre: [1.00, 1.00, 1.00, 1.00], post: [1.55, 1.10, 1.70, 0.34] },",
     "the one rule that stands far from both works without inverting colour, added 13.08: it comes "
     "out dark and thin in colour, so gain lifts the light and saturation gives the works' own "
     "colour its weight again"),
    ("var EDGE = 0.045;", "var EDGE = 0.045, SPREAD = 0.46;",
     "the softness of the region's edge, a fixed width that does not grow with presence"),
    ("const float SPREAD = 0.46;", "const float SPREAD = 0.46;",
     "what pulls the presence field's own depths flat, so the share standing at presence p is p"),
    ("float level = 4.0 * uMix * (1.0 - uMix);", "var level = 4 * dom * (1 - dom);",
     "how level the two works stand, which is half of the one envelope every axis hangs on"),
    ("float rA = 0.0135 * t * cw;", "0.0135 * t * cw",
     "the bottom layer's own turn, slow and one way"),
    ("float rB = (-0.0262 * t + uRotOff) * cw;", "(-0.0262 * t + turnOff) * cw",
     "the top layer's own turn, faster and the other way"),
    ("1.0 + (0.02 + 0.085 * sin(t * 0.0721)) * cw", "1 + (0.02 + 0.085 * Math.sin(t * 0.0721)) * cw",
     "the bottom layer's scale breath"),
    ("(1.0 + 0.11 * sin(t * 0.0487 + 1.7) * cw) * uTopScale",
     "(1 + 0.11 * Math.sin(t * 0.0487 + 1.7) * cw) * scale",
     "the top layer's scale breath, times the top scale"),
    ("0.60 * sin((p.x + p.y) * 5.3 - t * 0.061)", "0.60 * sin((pm.x + pm.y) * 5.3 - t * 0.061)",
     "the mix field's second wave, on its own period"),
    ("0.55 * sin((p.y - p.x) * 11.7 + t * 0.029)", "0.55 * sin((pr.y - pr.x) * 11.7 + t * 0.029)",
     "the presence field's second wave, on periods that share nothing with the mix field's"),
    ("float lean = mix(0.26 * level, 0.55 * uMix, uArrive);", "arrive ? 0.55 * dom : 0.26 * level",
     "how far the field may lean the frame either way, and the interfered arrival's own envelope"),
    ("float k = 0.80;", "float k = 0.80;",
     "the shoulder highlights roll off toward instead of clipping to"),
    ("col *= 1.0 - 0.20 * cw * smoothstep(0.25, 0.64, r);",
     "col *= 1.0 - 0.20 * cw * smoothstep(0.25, 0.64, r);",
     "the corner shading, arriving with the composite on the one envelope"),
    ("col += cw * (n - 0.5) / 255.0;", "col += cw * (n - 0.5) / 255.0;",
     "the dither, a pure function of the pixel's own place, which is why a run repeats with no seed"),
    ("var FEEL_S = 0.65, FEEL_MIX_K = 1.65, FEEL_PRES_S = 0.91, FEEL_PRES_D = 0.02;",
     "var FEEL_S = 0.65, FEEL_MIX_K = 1.65, FEEL_PRES_S = 0.91, FEEL_PRES_D = 0.02;",
     "the three measured response curves, digit for digit: the exposure's S on each stage, the "
     "dominance logarithm mirrored about the middle, and the presence S with its dead band"),
    ("return a / (a + b);", "return a / (a + b);",
     "the plain S itself, which fixes 0, a half and 1 by construction"),
]
missing_const = [p for lab_p, p in ((a, b) for a, b, _ in CONSTANTS)
                 if lab_p not in LABTXT or p not in REGION]
check("PASS-OVERLAY every constant the picture stands on carries the module's own number",
      not missing_const and bool(LABTXT),
      "; ".join("%s — %s" % (p, why) for _, p, why in CONSTANTS) if not missing_const
      else "these do not stand on both sides: " + ", ".join(missing_const))

# The three the port decided for itself, each named as the port's own.
OWN = [
    ("float m = max(uRes.x, uRes.y);",
     "THE SEATING IS ASKED OF THE HOST. The module's own line reads the frame and pulls back on one "
     "taller than wide, drawing the file smaller than a cover fit there — lab/data/"
     "module-contract.json says so in its own words. The host already computes a seating from each "
     "work's own two sides, so it is asked for, and both doors are the plain cover fit at every "
     "frame shape"),
    ("vec2 mir(vec2 q){ vec2 t = mod(q, 2.0); return 1.0 - abs(t - 1.0); }",
     "THE MIRROR IS WRITTEN IN THE SHADER. The module binds its own textures MIRRORED_REPEAT; the "
     "host binds its two source slots CLAMP_TO_EDGE, which would smear an edge texel across "
     "everything the turn and the scale breath carry past the frame"),
    ("vec3 flatOf(sampler2D tex, vec4 fit){",
     "THE ARRIVING WORK'S FLATTEST LEVEL IS READ AT A LATTICE. The module reads the last step of "
     "its own mipmap chain; the host builds none, so the same quantity is read at twenty-five "
     "places, each row shifted by the golden fraction so the lattice cannot fall into step with a "
     "work that carries a lattice of its own"),
]
own_missing = [s for s, _ in OWN if s not in REGION]
check("PASS-OVERLAY the three things the port decided for itself are named as the port's own",
      not own_missing
      and "MIRRORED_REPEAT" in LABTXT and "generateMipmap" in LABTXT
      and "mix(hi, mix(lo, hi, 0.62), step(uRes.x, uRes.y))" in LABTXT
      and "generateMipmap" not in REGION and "MIRRORED_REPEAT" not in REGION,
      " | ".join(why for _, why in OWN) if not own_missing
      else "these are not in the built file: " + ", ".join(own_missing))

DECL = set(re.findall(r'\{ name: "(u\w+)", type:', REGION))
SPELT = set(re.findall(r'uniform \w+ (u\w+);', REGION))
check("PASS-OVERLAY every uniform the manifest declares is a uniform the shader spells, and no other",
      DECL == SPELT and len(DECL) == 14,
      "the host looks every location up by the name the manifest declares and never by position "
      "(§7), so the two sets have to be one set: %d names, and they agree" % len(DECL)
      if DECL == SPELT else "declared but not spelled: %s; spelled but not declared: %s"
      % (sorted(DECL - SPELT), sorted(SPELT - DECL)))

SOURCES = set(re.findall(r'type: "\w+", source: "([^"]+)"', REGION))
CLOSED = {"textureA", "textureB", "fitA", "fitB", "resolution", "seconds"}
outside = sorted(s for s in SOURCES
                 if s not in CLOSED and not s.startswith("frame:") and not s.startswith("handle:"))
check("PASS-OVERLAY every uniform is sourced from inside the host's own closed set",
      not outside and SOURCES,
      "the two source textures, their seatings, the resolution, the transaction's seconds, a value "
      "the instrument answers or a handle — anything else is refused at registration (§7). This "
      "instrument asks for %s" % ", ".join(sorted(SOURCES))
      if not outside else "outside the set: " + ", ".join(outside))

check("PASS-OVERLAY the shader carries no version header of its own and asks the host for none",
      "#version" not in REGION and "#version 300 es" in LABTXT
      and REGION.count('"precision highp float;"') == 1,
      "the module ships GLSL ES 3.00 with its own header; the port is written at ES 1.00 and the "
      "host's own translator stamps the header exactly once, which is the road every landed "
      "instrument takes. A source carrying its own header would receive no translation at all, and "
      "the two would then be two dialects rather than one")

check("PASS-OVERLAY the drawing buffer is not asked to be preserved, and the module's own context "
      "stayed behind",
      "gl: { preserveDrawingBuffer: false }" in REGION
      and "premultipliedAlpha: false" in LABTXT and "premultipliedAlpha" not in REGION,
      "the module takes its own WebGL2 context with alpha on and premultiplication off, because a "
      "canvas that has to carry nothing outside the region cannot be opaque. The port writes the "
      "same absence as the alpha the HOST blends by, so no context of its own is needed and none is "
      "asked for")

check("PASS-OVERLAY the coverage is declared, justified, and written as the alpha the host blends by",
      "coverage: { writes: true," in REGION
      and "gl_FragColor = vec4(col, stands);" in REGION
      and "opacity" not in REGION and "premultipl" not in REGION,
      "§7's coverage law. This instrument's matter is absent wherever presence stands below whole: "
      "a place is inside the exposure's region or outside it, and outside it nothing at all is "
      "written. The alpha is the region's own membership, straight and never premultiplied — a "
      "shader emitting rgb·a would write black across its field in a one-cue score, which is the "
      "case the host's own comment names")

READS = ["scale", "turn", "mixPeriod", "mixTurn", "regionPeriod", "regionTurn"]
unread = [h for h in READS
          if not re.search(r'%s: \{[^}]*?reads:' % h, REGION, re.S)]
check("PASS-OVERLAY every geometric handle publishes the measurement of the photograph it reads",
      not unread
      and "structure.ownDevice.stepPx" in REGION and "structure.grid.periodPx" in REGION
      and "structure.ownDevice.angleDeg" in REGION and "structure.grid.angleDeg" in REGION,
      "his 19:13 word lifted to the class at 19:21. The mix field takes the DEPARTING work's own "
      "cutting step and the angle it was cut at, so the field that decides which places of the "
      "frame lean to which work leans along that work's own structure; the presence region takes the "
      "ARRIVING work's, so the exposure grows along the structure of the work it resolves into; the "
      "top scale takes the ratio of the two steps and the counter-turn the angle between the two "
      "lattices, which is charter shelf 10's own reading — the third picture is the two works' "
      "interference, and near-matched rhythms are what yield the beats"
      if not unread else "these publish no measurement: " + ", ".join(unread))

check("PASS-OVERLAY the three handles that carry a position carry the module's measured curve, and "
      "the ones that carry a quantity carry none",
      all(re.search(r'%s: \{[^}]*?curve: \{[^}]*?applied: true' % h, REGION, re.S)
          for h in ("mix", "exposure", "presence"))
      and not any(re.search(r'%s: \{[^}]*?curve:' % h, REGION, re.S) for h in READS),
      "a curve belongs on a handle whose value is a POSITION on a scale — the hand asks «how far "
      "along» and the instrument owes it equal change per equal step. A handle whose value is a "
      "QUANTITY in its own unit carries none, because a curve on it would corrupt the very "
      "measurement it carries: a composer that has measured the work's cutting step and asks for it "
      "must get it. Bands, measured: dominance 6.34 to 1.84, the exposure's colour stage 3.45 to "
      "1.62, presence 2.77 to 1.51")

check("PASS-OVERLAY the instrument measures no work for itself, and the door reading takes no grid",
      "getImageData" not in REGION and "readPixels" not in REGION
      and "the field's own DEEPEST possible place" in SOURCE_TEXT,
      "measuring a work means drawing it into a surface of its own and counting, which §1.2 forbids "
      "— so every measurement of a photograph reaches this instrument as a handle. Its own door is "
      "read the other way: the presence field is three waves whose sum is bounded by 1 and reaches "
      "it, so the deepest place the field can put anywhere in the frame is known in closed form, "
      "and reading there is stronger than walking a grid — a walk can step over the very point a "
      "grid would show")

LABSHA = hashlib.sha256(MODULE.read_bytes()).hexdigest() if MODULE.exists() else ""
check("PASS-OVERLAY the provenance weighs to the file it was carried from",
      bool(LABSHA) and LABSHA in REGION and 'commit: "a24594c"' in REGION
      and 'labPath: "lab/effects/overlay.js"' in REGION,
      "sha256 %s — the module as it stands in the read-only tree, weighed here rather than trusted"
      % LABSHA[:16])

# ---------------------------------------------------------------- browser rows

BROWSER_ROWS = [
    "PASS-OVERLAY §8     · the manifest declares what the host binds, and the host registers it",
    "PASS-OVERLAY the charter · the level claimed is LIGHT-COLOUR, and it is the only voice on it",
    "PASS-OVERLAY row 7  · both doors are their own work, cover-fitted, and neither is the other work",
    "PASS-OVERLAY the two roads of one frame agree at six places through the dominance travel",
    "PASS-OVERLAY the region is READ on the drawing buffer at both doors, and what it read is published",
    "PASS-OVERLAY every door this instrument can spoil is refused, in words a person could read",
    "PASS-OVERLAY the share of the frame the exposure stands on is the share presence names",
    "PASS-OVERLAY §7     · the placement its coverage buys it: a roof, never a floor",
    "PASS-OVERLAY §4.4b  · every handle reaches the PICTURE, and each by its own measurement",
    "PASS-OVERLAY §7     · no empty frame at any sampled instant of the pass",
    "PASS-OVERLAY row 10 · a seeded run repeats to the pixel",
    "PASS-OVERLAY row 15 · the console stays clean",
    "PASS-OVERLAY §7     · one canvas, one context, two source textures, one pass a frame",
    "PASS-OVERLAY the real transaction road: curtain up, one pass drawn, exactly one dock at the end",
    "PASS-OVERLAY a door the judges' channel spoils is refused on the real road, and the visitor still lands",
    "PASS-OVERLAY row 16 · the captures are kept as evidence",
]

RED_ROWS = [
    "PASS-OVERLAY red-on-bug · the door's own hold removed: both doors are refused for a hole in the region",
    "PASS-OVERLAY red-on-bug · the mirror removed: the two roads part where a layer runs past the work's edge",
    "PASS-OVERLAY red-on-bug · the seating given back to the module's own line: the door stops being the file",
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
    from PIL import Image, ImageChops, ImageStat
    a = Image.open(p).convert("RGB")
    flat = Image.new("RGB", a.size, BACKGROUND)
    st = ImageStat.Stat(ImageChops.difference(a, flat))
    own = ImageStat.Stat(a)
    return sum(st.mean) / 3.0, sum(own.stddev) / 3.0


def red_share(p):
    """The share of the frame the exposure stands on, read off the instrument's own map. With the
    judges' channel open the red channel IS `stands` — 1 inside the region, 0 outside it, and
    between the two only across the region's own edge — so the mean of that channel is the share."""
    from PIL import Image, ImageStat
    a = Image.open(p).convert("RGB")
    return ImageStat.Stat(a.split()[0]).mean[0] / 255.0


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
    """The whole file, cover-fitted into the frame with no crop of its own. Each work is seated into
    the module's own unit square by its own two sides and the square covers the frame's longer side,
    so a door is the plain cover fit at every frame shape — which is what the doors' own `framings`
    block publishes."""
    from PIL import Image
    return cover_into(Image.open(src).convert("RGB"), w, h, crop)


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
    the lab module exactly as it stands on disk, the two photographs, and the page that stands the
    two roads of one frame side by side.

    A row proving a rule reds hands over a CHANGED instrument file and writes the record with the
    digest of the bytes actually served, which is what the build does. The source file on disk is
    never touched, so nothing has to be restored and no working tree can be left changed by a
    red-on-bug proof."""
    d = Path(tempfile.mkdtemp(prefix="synth_ovbench_"))
    pack = PACK if pack_text is None else pack_text
    shutil.copy2(TMP / "pass-layer.js", d / "pass-layer.js")
    for _inst in sorted(TMP.glob("pass-inst-*.js")):
        shutil.copy2(_inst, d / _inst.name)
    (d / "pass-inst-overlay.js").write_text(pack, encoding="utf-8")
    record = json.loads((TMP / "config.json").read_text(encoding="utf-8"))
    record["pass"]["instruments"]["overlay"]["digest"] = hashlib.sha256(
        pack.encode("utf-8")).hexdigest()
    (d / "config.json").write_text(json.dumps(record), encoding="utf-8")
    (d / "overlay.js").write_text(LABTXT, encoding="utf-8")
    (d / "photos").mkdir()
    for p in PHOTOS:
        shutil.copy2(p, d / "photos" / p.name)
    shutil.copy2(ROOT / "tests" / "fixture_pass_overlay.html", d / "index.html")
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


def on_bench(fn, pack_text=None, w=VW, h=VH):
    d = bench_dir(pack_text)
    try:
        with serve(d) as base:
            with Browser(width=w, height=h) as br:
                br.navigate(base + "/index.html")
                if not ready(br):
                    return None
                return fn(br)
    finally:
        shutil.rmtree(d, ignore_errors=True)


# WHICH HANDLES REACH WHICH ROAD. The five on the right carry the two works' own lattices and the
# module has no counterpart for them, so they are set on the pose alone; the rest are set on both
# roads at once, through the module's own onParam and the port's own pose in one call.
PORT_ONLY = {"turn", "mixPeriod", "mixTurn", "regionPeriod", "regionTurn"}
RESTS = {"blend": 0, "scale": 1, "arrival": 0, "presence": 1, "exposure": 1, "turn": 0,
         "mixPeriod": MIX_PERIOD, "mixTurn": 0,
         "regionPeriod": REGION_PERIOD, "regionTurn": 0}


def set_handle(br, k, v):
    if k == "exposure":
        br.evaluate("window.__dial(%r); 0" % v)
    elif k == "mask":
        br.evaluate("window.__mask(%r); 0" % v)
    elif k in PORT_ONLY:
        js(br, "return window.__port(%r, %r);" % (k, v))
    else:
        js(br, "return window.__param(%r, %r);" % (k, v))


def host_shot(br, at, tag, **params):
    for k, v in params.items():
        set_handle(br, k, v)
    js(br, "return window.__both(%r);" % at)
    br.sleep(0.3)
    br.evaluate("window.__hostDraw(); window.__show('host'); 0")
    br.sleep(0.3)
    return png(br, SHOTS / (tag + ".png"))


def roads(br, at, tag):
    """BOTH ROADS AT ONE POSE. The dominance handle is the raw hand on both sides: the module applies
    its own curve to it and so does the port, so handing one number to both is handing them one
    pose."""
    r = js(br, "return window.__both(%r);" % at)
    br.sleep(0.45)
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


def road_gap(br, at, tag="gap"):
    _, ph, pm = roads(br, at, tag)
    return diff(ph, pm)


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
            elif not js(br, "return !!window.__exPass.bench.manifest('overlay');"):
                why = js(br, "var e = window.__host.report().events.filter(function(x){"
                             "return x.name === 'manifest-refused';});"
                             "return e.length ? e[e.length - 1].why : null;")
                for r in BROWSER_ROWS:
                    check(r, False, "the host registered no «overlay» instrument: " + str(why))
            else:
                SCORE = json.dumps(overlay_score())
                SCORE_OVER = json.dumps(overlay_score(over=True))

                # ---- §8: the manifest, read off the registered instrument -----------------------
                m = js(br, "return window.__exPass.bench.manifest('overlay');")
                res = m["resources"]
                need = ["id", "api", "arity", "roles", "params", "handles", "neutrals", "doors",
                        "framings", "drivers", "camera", "gl", "passes", "resources",
                        "capabilities", "decline", "provenance", "readiness", "coverage", "levels"]
                shape = (
                    all(k in m for k in need)
                    and m["id"] == "overlay" and m["api"] == 1 and m["arity"] == 2
                    and m["roles"] == ["disassembly", "mystery", "assembly"]
                    and len(m["handles"]) == 13
                    and all(set(h) >= {"min", "max", "def"} for h in m["handles"].values())
                    and m["neutrals"] == {"a": 0, "b": 1}
                    and m["doors"]["in"]["handle"] == "mix" and m["doors"]["in"]["value"] == 0
                    and m["doors"]["out"]["handle"] == "mix" and m["doors"]["out"]["value"] == 1
                    and sorted(m["framings"]) == ["0", "1"]
                    and m["framings"]["0"] == {"coverCrop": 1} == m["framings"]["1"]
                    and m["camera"] == {"needs": "none", "authority": "stage"}
                    and m["gl"] == {"preserveDrawingBuffer": False}
                    and len(m["passes"]) == 1 and len(m["passes"][0]["uniforms"]) == 14
                    and sorted(res) == ["lean", "rich", "standard"]
                    and all("bytesEstimate" in res[v] and res[v]["programs"] == 1
                            and res[v]["passes"] == 1 and res[v]["textureSlots"] == 2
                            for v in res)
                    and m["capabilities"] == ["webgl2"] and m["decline"]
                    and m["coverage"]["writes"] is True and m["coverage"]["how"]
                    and m["provenance"]["labPath"] == "lab/effects/overlay.js"
                    and m["provenance"]["commit"] == "a24594c"
                    and m["readiness"] == "production-ready"
                    and "overlay" in js(br, "return window.__host.report().registered;"))
                check(BROWSER_ROWS[0], shape,
                      f"thirteen handles, fourteen uniforms in one pass, both doors at a cover crop "
                      f"of {m['framings']['0']['coverCrop']} — the plain cover fit, no crop and no "
                      f"upscale — resources declared for three tiers, and a coverage block that "
                      f"declares writes={m['coverage']['writes']}")

                others = js(br, "var b = window.__exPass.bench, o = {};"
                                "window.__host.report().registered.forEach(function (n) {"
                                "  o[n] = (b.manifest(n) || {}).levels || null; });"
                                "return o;")
                mine = [n for n, lv in others.items() if lv and "LIGHT-COLOUR" in lv]
                check(BROWSER_ROWS[1],
                      m["levels"] == ["LIGHT-COLOUR"] and mine == ["overlay"],
                      f"lab/data/module-contract.json records this module's level as LIGHT-COLOUR "
                      f"and the vocabulary table of lab/CROSSING-BRIEF.md carries the same word "
                      f"beside his standing verdict, so the reading is carried rather than "
                      f"re-decided. The charter's levels law allows one voice per level, and of the "
                      f"instruments registered here — {json.dumps(others, sort_keys=True)} — this is "
                      f"the only one that claims it")

                # ---- row 7: both doors are their own work, cover-fitted -------------------------
                bufs = js(br, "return window.__buffers();")
                w, h = bufs["host"]
                A = work_in_the_frame(BENCH / "photos" / PHOTOS[0].name, w, h)
                B = work_in_the_frame(BENCH / "photos" / PHOTOS[1].name, w, h)
                door_rows, worst_own, best_other = [], 0.0, 1e9
                for tag, at, own, other, own_n in (("door-0", 0.0, A, B, PHOTOS[0].name),
                                                   ("door-1", 1.0, B, A, PHOTOS[1].name)):
                    p = host_shot(br, at, tag)
                    d_own, mx_own = apart(p, own)
                    d_other, _ = apart(p, other)
                    worst_own = max(worst_own, d_own)
                    best_other = min(best_other, d_other)
                    door_rows.append("%s stands %.4f of 255 from %s cover-fitted into the %d x %d "
                                     "buffer (worst channel %d) and %.2f from the other work"
                                     % (tag, d_own, own_n, w, h, mx_own, d_other))
                check(BROWSER_ROWS[2], worst_own <= SEAM and best_other >= FAR,
                      "; ".join(door_rows) + ". The bar is the project's own seam threshold of %s of "
                      "255, and the other work has to stand past %s, which is the distance this "
                      "project calls a frame another work" % (SEAM, FAR))

                # ---- the region, read on the buffer at both doors -------------------------------
                grids = [(390, 844), (780, 1688), (195, 422), (1440, 900), (40, 60)]
                reads, bad = [], []
                for at in (0, 1):
                    for gw, gh in grids:
                        v = js(br, "var p = window.__pose(); p.mix = %d;"
                                   "p.bufWidth = %d; p.bufHeight = %d;"
                                   "return window.__values(p);" % (at, gw, gh))
                        ok = (v["doorWhyNo"] is None and v["doorHeld"]
                              and abs(v["presenceApplied"] - 1) < 1e-12
                              and abs(v["standsWorst"] - 1) < 1e-12
                              and abs(v["presenceRequest"] - 0.98) < 1e-9
                              and v["doorGrid"] == {"w": gw, "h": gh, "drawn": True, "given": True})
                        reads.append(v)
                        if not ok:
                            bad.append("door %d on %dx%d: %s" % (at, gw, gh, json.dumps(v)))
                away = js(br, "var p = window.__pose(); p.mix = 0.5; return window.__values(p);")
                check(BROWSER_ROWS[4],
                      not bad and away["doorGrid"] is None and away["doorWhyNo"] is None,
                      f"twenty readings — two doors over five grids — each taken on the buffer the "
                      f"shader is about to sample on. At every one the presence curve's own dead "
                      f"band hands the instrument {reads[0]['presenceRequest']:.4f} where a score "
                      f"asked for whole, the field's deepest possible place would carry "
                      f"{1 - 0.028:.4f} of a point there, and the hold closes it: applied "
                      f"{reads[0]['presenceApplied']}, thinnest place {reads[0]['standsWorst']}, "
                      f"held {1 - reads[0]['presenceRequest']:.4f} of the frame. Away from a door "
                      f"nothing is read and no guard moves"
                      if not bad else "; ".join(bad[:3]))

                # ---- every refusal this instrument can make -------------------------------------
                def whyno(**over):
                    q = ";".join("p.%s = %r" % (k, v) for k, v in over.items())
                    return js(br, "var p = window.__pose(); %s; return window.__values(p);" % q)

                r_exp = whyno(mix=1, exposure=0.5)
                r_pres = whyno(mix=0, presence=0.6)
                r_mask = whyno(mix=0, mask=1)
                r_ok = whyno(mix=0)
                check(BROWSER_ROWS[5],
                      r_ok["doorWhyNo"] is None
                      and r_exp["doorWhyNo"] and "the exposure stands at" in r_exp["doorWhyNo"]
                      and "composited by" in r_exp["doorWhyNo"]
                      and r_pres["doorWhyNo"] and "per cent of the frame" in r_pres["doorWhyNo"]
                      and "carries nothing at all" in r_pres["doorWhyNo"]
                      and r_mask["doorWhyNo"] and "judges' own channel" in r_mask["doorWhyNo"],
                      "three faults, three sentences, each in this instrument's own measured "
                      "numbers. (1) «%s» (2) «%s» (3) «%s»"
                      % (r_exp["doorWhyNo"], r_pres["doorWhyNo"], r_mask["doorWhyNo"]))

                # ---- the share of the frame the exposure stands on ------------------------------
                shares, share_bad = [], []
                for want in (0.25, 0.5, 0.75, 1.0):
                    js(br, "return window.__param('presence', %r);" % want)
                    v = js(br, "var p = window.__pose(); p.mix = 0.5; return window.__values(p);")
                    js(br, "return window.__both(0.5);")
                    br.evaluate("window.__mask(1); window.__hostDraw(); window.__show('host'); 0")
                    br.sleep(0.3)
                    p = png(br, SHOTS / ("region-%s.png" % want))
                    got = red_share(p)
                    shares.append((want, v["presenceApplied"], got))
                    if abs(got - v["presenceApplied"]) > SHARE_SLACK:
                        share_bad.append("presence %s: applied %.4f, the frame carries %.4f"
                                         % (want, v["presenceApplied"], got))
                js(br, "return window.__param('presence', 1);")
                br.evaluate("window.__mask(0); 0")
                check(BROWSER_ROWS[6], not share_bad,
                      "read off the instrument's own map, where the red channel IS the region's "
                      "membership: " + "; ".join("presence %s applied as %.4f stands on %.4f of the "
                                                 "frame" % s for s in shares)
                      + ". The module's own measured law is that the share standing at presence p is "
                        "p itself within three parts in a hundred, and it holds here because the "
                        "field's own depths are pulled flat by SPREAD"
                      if not share_bad else "; ".join(share_bad))

                # ---- the placement its coverage buys it ----------------------------------------
                cov = js(br, "return window.__exPass.bench.coverageOf('overlay');")
                floor_why = js(br, "return window.__exPass.bench.coverageWhyNo(%s);"
                                   % json.dumps([overlay_cue(stack=0), weave_cue(stack=1)]))
                roof_why = js(br, "return window.__exPass.bench.coverageWhyNo(%s);"
                                  % json.dumps([weave_cue(stack=0), overlay_cue(stack=1)]))
                alone_why = js(br, "return window.__exPass.bench.coverageWhyNo(%s);"
                                   % json.dumps([overlay_cue(stack=0)]))
                check(BROWSER_ROWS[7],
                      cov and cov["writes"] is True
                      and floor_why and "overlay" in floor_why and roof_why is None
                      and alone_why is None,
                      f"laid lowest under a frame-filling voice the host refuses the whole score by "
                      f"name — «{floor_why}» — because the lowest cue meets blending disabled and "
                      f"its gaps would show the cleared buffer. Laid OVER that same ground it is "
                      f"lawful, which is the placement his В22 asks for: a double-exposure moment "
                      f"mixed into a transport middle. Alone it is a one-cue score, which the rule "
                      f"exempts")

                # ---- every handle reaches the picture -------------------------------------------
                base = host_shot(br, 0.5, "handles-base")
                # WHICH ROAD EACH HANDLE IS READ ON. Seven of them move the frame's own colour and
                # are read there. The two that carry the ARRIVING work's lattice move only where the
                # exposure's region stands, and a bench draw lays one cue onto a cleared buffer with
                # blending disabled — so the alpha those two write is never read, and reading them
                # on the colour would read nothing whatever they did. They are read on the
                # instrument's own map instead, where the region's membership IS the red channel;
                # that is the same alpha the host blends by when this instrument stands over a cue,
                # and it is the only place their work can show.
                REACH = [
                    ("blend", 1, 0.5, 1, 0, "the rule the two works meet under: screen against "
                                            "difference"),
                    ("scale", 1.4, 0.5, 1, 0, "how large the arriving work stands against the "
                                              "departing one — the ratio of the two works' cutting "
                                              "steps"),
                    ("turn", 60, 0.5, 1, 0, "the angle between the two works' lattices, which is "
                                            "what decides whether they beat into a moiré"),
                    ("arrival", 1, 0.8, 1, 0, "the interfered arrival: the lean keeps growing to "
                                             "the wet end instead of closing at it"),
                    ("exposure", 0.4, 0.5, 1, 0, "how far the composite reaches, with the arriving "
                                                 "work's colour ahead of its forms"),
                    ("mixPeriod", 0.1, 0.5, 1, 0, "the departing work's own cutting step, which "
                                                  "the mix field is laid on"),
                    ("mixTurn", 90, 0.5, 1, 0, "the angle that step was cut at"),
                    ("regionPeriod", 0.05, 0.5, 0.5, 1, "the arriving work's own step, which the "
                                                        "exposure's region grows along"),
                    ("regionTurn", 90, 0.5, 0.5, 1, "the angle that step was cut at"),
                ]
                moved, reach_bad, refs = [], [], {}
                for k, v, at, pres, msk, why in REACH:
                    set_handle(br, "presence", pres)
                    set_handle(br, "mask", msk)
                    if (at, pres, msk) not in refs:
                        refs[(at, pres, msk)] = host_shot(
                            br, at, "reach-rest-%s-%s-%s" % (at, pres, msk))
                    p = host_shot(br, at, "reach-" + k, **{k: v})
                    set_handle(br, k, RESTS[k])
                    d, _ = diff(p, refs[(at, pres, msk)])
                    moved.append("%s moves the frame %.2f of 255%s (%s)"
                                 % (k, d, " on the instrument's own map" if msk else "", why))
                    if d <= SEAM:
                        reach_bad.append("%s moved the frame only %.4f of 255" % (k, d))
                set_handle(br, "presence", 1)
                set_handle(br, "mask", 0)
                check(BROWSER_ROWS[8], not reach_bad,
                      "; ".join(moved) + ". Each read against %s of 255, the project's own seam "
                      "threshold — a handle that cannot move the frame past it is noise in a score"
                      % SEAM
                      if not reach_bad else "; ".join(reach_bad))

                # ---- the port-only handles reach the picture through the FIELDS, not by chance ---
                # (folded into the row above; the two region handles are read at half presence,
                #  because at whole presence the region covers the frame and its own shape cannot
                #  show — which is itself the coverage law holding.)

                # ---- no empty frame -------------------------------------------------------------
                empties, thin = [], []
                for at in (0.0, 0.15, 0.3, 0.5, 0.7, 0.85, 1.0):
                    p = host_shot(br, at, "standing-%s" % at)
                    d, sd = standing(p)
                    empties.append((at, d, sd))
                    if d < FAR or sd < SPREAD:
                        thin.append("at %s the frame stands %.2f from the ground with a spread of "
                                    "%.2f" % (at, d, sd))
                check(BROWSER_ROWS[9], not thin,
                      "seven instants of the travel, each read against the host's own cleared "
                      "buffer: " + ", ".join("%.2f/%.2f at %s" % (d, sd, at)
                                             for at, d, sd in empties)
                      if not thin else "; ".join(thin))

                # ---- a seeded run repeats to the pixel ------------------------------------------
                one = host_shot(br, 0.42, "repeat-1")
                js(br, "return window.__both(0.9);")
                two = host_shot(br, 0.42, "repeat-2")
                d2, mx2 = diff(one, two)
                check(BROWSER_ROWS[10], d2 == 0.0 and mx2 == 0,
                      f"the same pose walked away from and returned to draws the same pixels: "
                      f"{d2} of 255, worst channel {mx2}. The module rolls no die at all — every "
                      f"value in a frame is a pure function of the second handed in and the handles, "
                      f"and the one hash in the shader is the dither, which is a pure function of "
                      f"the pixel's own place")

                # ---- the real transaction road --------------------------------------------------
                took = js(br, "return window.__offer(%s);" % SCORE)
                landed = idle(br)
                rep = js(br, "return window.__report();")
                hooks = js(br, "return window.__hooks;")
                check(BROWSER_ROWS[13],
                      took["took"] and landed and hooks["curtains"][:1] == [True]
                      and hooks["docks"].count(took["gen"]) == 1
                      and rep["census"]["passesLastFrame"] in (0, 1),
                      f"a hand-made command of the shape the bundle freezes, offered to the real "
                      f"host: it took it, raised its curtain, ran its own frame loop and docked once "
                      f"at gen {took['gen']}. Curtains {hooks['curtains']}, docks {hooks['docks']}, "
                      f"glides {hooks['glides']}")

                census = rep["census"]
                check(BROWSER_ROWS[12],
                      census["canvases"] == 1 and census["contexts"] == 1
                      and census["textures"] == 2 and census["programs"] >= 1,
                      f"one canvas, one context and two source textures for every pair, forever: "
                      f"{json.dumps({k: census[k] for k in ('canvases', 'contexts', 'textures', 'programs')})}. "
                      f"The module raised a canvas and a context of its own and uploaded two "
                      f"textures with their mipmap chains for every visit; this instrument "
                      f"allocates nothing at all")

                # ---- a door the judges' channel spoils is refused on the real road ---------------
                br.evaluate("window.__cancel('bench'); 0")
                idle(br)
                spoiled = json.dumps(overlay_score(mask=1))
                took2 = js(br, "return window.__offer(%s);" % spoiled)
                landed2 = idle(br)
                rep2 = js(br, "return window.__report();")
                # THE REASON IS READ WHEREVER THE HOST PUT IT. The instrument publishes it twice —
                # through `reportApplied`, which the host stores and reads nothing in, and through
                # `fail`, which the host logs — so the row looks over the whole report rather than
                # guessing which shelf it landed on.
                blob = json.dumps(rep2)
                why2 = next((s for s in re.findall(r'"([^"]*judges[^"]*)"', blob)), "")
                check(BROWSER_ROWS[14],
                      took2["took"] and landed2 and rep2["state"] == "idle"
                      and "judges' own channel" in blob,
                      f"the host recovers the transaction on the instrument's own reason and the "
                      f"walk's own glide carries the visitor, which is the product's behaviour with "
                      f"no renderer at all. The reason it landed on: «{why2}»")

                errs = js(br, "return window.__errs;")
                check(BROWSER_ROWS[11], not errs,
                      "no page error, no rejection and nothing on console.error through every row "
                      "above" if not errs else "; ".join(str(e) for e in errs[:4]))

                shots = sorted(SHOTS.glob("*.png"))
                check(BROWSER_ROWS[15],
                      len(shots) >= 25 and all(p.stat().st_size > 1000 for p in shots),
                      f"{len(shots)} frames kept under tests/captures/pass-overlay — both doors, "
                      f"the travel, the region at four presences, every handle's reach and the two "
                      f"roads side by side")

    # ---- the two roads, on the square frame where the seating costs nothing ---------------------
    # THE ONE FRAME THE TWO ROADS ARE ONE ARITHMETIC ON. The module maps the frame onto a square and
    # reads a work across it whatever its shape; the port seats each work by its own two sides. On a
    # square frame with square works the two are the same map, so what this row compares is the
    # mathematics and nothing else. The clock stands at nothing, where both layers' scale breaths are
    # above 1 and neither work is minified — so the module's mipmap chain and the host's unmipped
    # slots read the same texels.
    def two_roads(br):
        out, worst = [], (0.0, 0)
        for at in (0.10, 0.25, 0.40, 0.55, 0.70, 0.90):
            _, ph, pm = roads(br, at, "roads-%s" % at)
            d, mx = diff(ph, pm)
            out.append((at, d, mx))
            if d > worst[0]:
                worst = (d, mx)
        return {"rows": out, "worst": worst, "buffers": js(br, "return window.__buffers();")}

    tr = on_bench(two_roads, w=SQ, h=SQ)
    check(BROWSER_ROWS[3],
          tr is not None and tr["buffers"]["host"] == tr["buffers"]["module"]
          and all(d <= ROADS for _, d, _ in tr["rows"]),
          (f"six places through the dominance travel on a {SQ} x {SQ} frame with two square works, "
           f"both roads sampled on one {tr['buffers']['host']} buffer: "
           + ", ".join("%.4f of 255 at %s" % (d, at) for at, d, _ in tr["rows"])
           + f". Worst {tr['worst'][0]:.4f} of 255 with a worst channel of {tr['worst'][1]}, against "
             f"the project's own seam threshold of {ROADS}. Both roads run one fragment shader "
             f"through one rasteriser, so the residual is a difference of arithmetic")
          if tr else "the square bench never came up")

    # ---- red-on-bug ------------------------------------------------------------------------------
    # 1. the door's own hold removed
    def door_state(br):
        a = js(br, "var p = window.__pose(); p.mix = 0; return window.__values(p);")
        b = js(br, "var p = window.__pose(); p.mix = 1; return window.__values(p);")
        js(br, "return window.__offer(%s);" % json.dumps(overlay_score()))
        idle(br)
        # WHAT THE REAL ROAD SAYS. The instrument publishes the same sentence twice and the two mean
        # opposite things: under `held` it is the fault the hold CLOSED, under `whyNo` the fault it
        # refused the door for. So the run-time proof reads the field and not the words — the
        # visitor lands either way, and a row that read the landing would pass on the defect.
        rep = json.dumps(js(br, "return window.__report();"))
        return {"in": a["doorWhyNo"], "out": b["doorWhyNo"],
                "held": a["doorHeld"], "applied": a["presenceApplied"],
                "worst": a["standsWorst"],
                "refused": bool(re.search(r'"whyNo": ?"', rep))}

    base_hold = on_bench(door_state)
    bug = PACK.replace("if (request >= 1 - DOOR_HOLD && request < 1) {",
                       "if (false) {", 1)
    bug_hold = on_bench(door_state, pack_text=bug)
    check(RED_ROWS[0],
          bug != PACK and base_hold and bug_hold
          and base_hold["in"] is None and base_hold["out"] is None
          and base_hold["refused"] is False
          and bug_hold["in"] and "carries nothing at all" in bug_hold["in"]
          and bug_hold["out"] and bug_hold["refused"] is True,
          f"the presence curve carries a dead band of two hundredths at either end — the module's "
          f"own measured stretch where the frame does not move at all — so a score asking for whole "
          f"presence is handed 0.98 and the field's deepest possible "
          f"place would carry {1 - 0.028:.4f} of a whole point instead of 1. Standing, the hold "
          f"closes it: applied {base_hold['applied']}, thinnest place {base_hold['worst']}, both "
          f"doors whole, and a real command runs with no refusal anywhere in the host's report. "
          f"Taken out of the served instrument, both doors are refused — "
          f"«{(bug_hold['in'] or '')[:150]}…» — and that sentence stands in the host's own report "
          f"after the same command. What the hold buys is exactly this: the dead band is by "
          f"measurement the stretch that moves nothing a person can see, so closing it at a door "
          f"changes no pixel and makes the door exact")

    # 2. the mirror removed
    def mirror_gap(br):
        # THE PLACE THE MIRROR HAS THE MOST TO SAY. At its smallest scale the top layer reads a
        # quarter again past the work's own edge each way, and at a dominance of 0.85 that layer is
        # most of what the frame carries; the clock at its own far end puts the turn and both drifts
        # at their widest, so what runs past the edge is the whole of what the two roads differ over.
        js(br, "return window.__param('scale', 0.65);")
        br.evaluate("window.__clock(14); 0")
        return road_gap(br, 0.85, "mirror")

    base_mir = on_bench(mirror_gap, w=SQ, h=SQ)
    bug = PACK.replace("vec2 mir(vec2 q){ vec2 t = mod(q, 2.0); return 1.0 - abs(t - 1.0); }",
                       "vec2 mir(vec2 q){ return clamp(q, 0.0, 1.0); }", 1)
    bug_mir = on_bench(mirror_gap, pack_text=bug, w=SQ, h=SQ)
    check(RED_ROWS[1],
          bug != PACK and base_mir and bug_mir
          and base_mir[0] <= ROADS and bug_mir[0] > ROADS * 3,
          f"the top layer at a scale of 0.65 reads a quarter again past the work's own edge each "
          f"way, which is where the module's MIRRORED_REPEAT and the port's own triangle wave have "
          f"something to say. With the mirror standing the two roads agree at "
          f"{base_mir[0]:.4f} of 255; with it reverted to the clamp the host's own texture setting "
          f"would give, they part at {bug_mir[0]:.4f} of 255 with a worst channel of {bug_mir[1]}, "
          f"against the project's own threshold of {ROADS}")

    # 3. the seating given back to the module's own line
    def door_from_file(br):
        bufs = js(br, "return window.__buffers();")
        w, h = bufs["host"]
        p = host_shot(br, 0.0, "seating")
        return apart(p, work_in_the_frame(PHOTOS[0], w, h)) + (w, h)

    base_seat = on_bench(door_from_file)
    bug = PACK.replace("float m = max(uRes.x, uRes.y);",
                       "float lo = min(uRes.x, uRes.y), hi = max(uRes.x, uRes.y);"
                       "float m = mix(hi, mix(lo, hi, 0.62), step(uRes.x, uRes.y));", 1)
    bug_seat = on_bench(door_from_file, pack_text=bug)
    check(RED_ROWS[2],
          bug != PACK and base_seat and bug_seat
          and base_seat[0] <= SEAM and bug_seat[0] > SEAM * 3,
          f"on the {base_seat[2]} x {base_seat[3]} phone buffer the entry door stands "
          f"{base_seat[0]:.4f} of 255 from its own file cover-fitted, worst channel {base_seat[1]}. "
          f"With the module's own line given back — which pulls a frame taller than wide back to "
          f"lo + 0.62·(hi − lo) and draws the file smaller than a cover fit, with the work's own "
          f"mirrored continuation filling what is left — the same door stands {bug_seat[0]:.4f} of "
          f"255 from the file. That is the parting lab/data/module-contract.json records in its own "
          f"words, measured")


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
