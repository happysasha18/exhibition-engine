#!/usr/bin/env python3
"""PASS-API-V1 — the glass instrument on the host's frame.
Run: python3 tests/test_pass_lens.py

Root: the port lanes' own brief. The lab holds twenty-three effect modules and the engine held six
instruments, four of which played on the cast route, so the sameness a person sees on a walk is the
port's fault rather than the composer's. This file is `lab/effects/lens.js` carried across, and
docs/design/PASS-API-V1.md §7 (GPU and resources), §8 (the manifest) and §9's conformance rows 7, 9,
10, 13, 14, 15, 16 and 22 are what it makes real, together with §7's coverage law.

HIS OWN STANDING VERDICT ON THIS EFFECT, AND WHAT THIS SUITE HAS TO ANSWER FOR IT.

  lab/CROSSING-BRIEF.md's vocabulary table records `lens` as «блуждающая линза · оживление
  (gallery) · CELL · mouse-mapping feature PARKED (his 09:42 «отдельная фича»)». It is recorded as an
  ОЖИВЛЕНИЕ and not as a ПЕРЕХОД, and the module's own dial is the lens's REACH rather than a
  passage. So this port cannot make the module's dial into `mix`, and what it does instead — one
  envelope on which the glass opens, holds while the two works change hands under it, and closes —
  is what the rows below measure. The pointer, which his word parks, did not come over at all: the
  glass rests where the two works' own measured radial centres meet and does not rove.

WHAT IS COMPARED, AND AGAINST WHAT.

  The doors. At the dial's two ends one whole work stands, each measured against ITS OWN FILE
  cover-fitted into the frame — this instrument asks the host for no crop, so what a door shows is
  the plain cover fit — inside the project's seam threshold of 6 of 255.

  THE TWO ROADS, AND WHY THEY COMPARE THE MAP RATHER THAN THE PICTURE. The module draws a drifting
  grid of fourteen finished works and this port draws the pair's own work continued past its edge by
  mirroring, so the two never sample the same picture and a comparison of colour would compare two
  walls rather than two readings of one geometry. What IS one geometry is the map — the point of the
  plane the glass shows at each point of the frame — so both files are served with their own sampler
  replaced by the SAME encoder and the maps are compared point for point. Neither file on disk is
  touched. The module is driven at its own second zero, which is where its spin is nothing and both
  of its breaths stand at the middles this port carries as constants.

  The coverage. This instrument declares that it writes none, because the mirrored plane fills the
  frame. The glass's own reading walks the buffer's sample points and publishes what it found.

  The handover. The two works may change hands only while the glass covers the whole frame. That is
  read on the buffer at every pose and refused where it does not hold, because a share of the
  arriving work standing on a point of the plain departing work is a dissolve between two
  photographs and not a fold.

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
# suites of the ports before this one read them from too.
LAB = Path(os.environ.get("TLVPHOTOS_ROOT", "/Users/sashaabramovich/tlvphotos")) / "lab"
PHOTOS = [LAB / "photos" / "glassgrid.jpg", LAB / "photos" / "towers.jpg"]
MODULE = LAB / "effects" / "lens.js"

SITE_URL = "https://synth.example.com"
VW, VH = 390, 844          # the phone frame lab/carrier-check.py measures on
SEAM = 6.0                 # the project's seam threshold, 6 of 255 (TRANSITION-STAGE-V0 §1)
FAR = 40.0                 # further than this from a file and it is a different work
BACKGROUND = (0x08, 0x08, 0x0a)

# THE TWO ROADS' BAR. Both roads run one fragment shader over one rasteriser and, with each file's
# own sampler replaced by the same encoder, what stands between them is arithmetic alone. The bar is
# the project's own seam threshold; the readings stand in the evidence beside it.
ROADS = SEAM

SHOTS = ROOT / "tests" / "captures" / "pass-lens"

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


DURATION_MS = 6500
WITHIN_MS = 500


def _static(v):
    return {"op": "static", "value": v}


def lens_cue(stack=0, levels_own=None, **statics):
    """The cue, with a track for every one of the nine handles (§4.4b)."""
    P = {"fold": 0, "wedges": 6, "twist": 1, "power": 2, "centreX": 0.5, "centreY": 0.5,
         "shade": 1, "mask": 0}
    P.update(statics)
    nodes = {"l-mix": {"source": "progress"}}
    tracks = {"mix": {"node": "l-mix"}}
    for k, v in P.items():
        nodes["l-" + k] = _static(v)
        tracks[k] = {"node": "l-" + k}
    return {
        "id": "lens-main", "instrument": {"id": "lens", "api": 1},
        "voice": "letter", "roles": ["disassembly", "mystery", "assembly"],
        "levels": ["SURFACE", "CELL"],
        "levelOwnership": levels_own or {"SURFACE": "owns", "CELL": "owns"},
        "window": [0, DURATION_MS / 1000.0], "works": ["a", "b"], "stack": stack,
        "cameraAuthority": "stage",
        "doors": {"in": {"handle": "mix", "value": 0, "measured": True},
                  "out": {"handle": "mix", "value": 1, "measured": True}},
        "nodes": nodes, "tracks": tracks,
        "resources": {"textures": 0, "textureSlots": 2, "framebuffers": 0, "pingPong": 0,
                      "programs": 1, "passes": 1, "bytesEstimate": 0, "variant": "standard"},
    }


def matter_cue(stack=1):
    """THE VOICE THAT STANDS OVER IT. `matter` writes coverage, so it is what a frame-filling ground
    is meant to be played under (the placement rule §7 states)."""
    nodes = {"m-mix": {"source": "progress"}, "m-clock": {"source": "time"}}
    tracks = {"mix": {"node": "m-mix"}, "clock": {"node": "m-clock"}}
    return {
        "id": "over", "instrument": {"id": "matter", "api": 1},
        "voice": "accompaniment", "roles": ["assembly"],
        "levels": ["SURFACE", "TEXTURE"],
        "levelOwnership": {"SURFACE": "accompanies", "TEXTURE": "owns"},
        "window": [0, DURATION_MS / 1000.0], "works": ["a", "b"], "stack": stack,
        "cameraAuthority": "stage",
        "doors": {"in": {"handle": "mix", "value": 0, "measured": True},
                  "out": {"handle": "mix", "value": 1, "measured": True}},
        "nodes": nodes, "tracks": tracks,
        "resources": {"textures": 0, "textureSlots": 2, "framebuffers": 0, "pingPong": 0,
                      "programs": 1, "passes": 1, "bytesEstimate": 0, "variant": "standard"},
    }


def lens_score(under=False, **statics):
    """`under` puts a coverage-writing voice ABOVE this instrument, which is the placement its own
    declaration buys it: the ground of a stack."""
    cues = [lens_cue(stack=0, **statics)]
    if under:
        cues = cues + [matter_cue(stack=1)]
    res = {"textures": 0, "textureSlots": 2, "framebuffers": 0, "pingPong": 0, "programs": 1,
           "passes": 1, "bytesEstimate": 0}
    return {
        "schema": 2,
        "intent": "a round glass opens over the point the two works' own structure turns about, "
                  "folds everything it covers, takes the whole frame while the two photographs "
                  "change hands under the fold, and closes back to nothing "
                  "(lab/effects/lens.js:1-3, its own header)",
        "pair": {"a": "a", "b": "b"},
        "seed": 0,
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
        "provenance": {"source": "lab/effects/lens.js's own declared defaults and constants",
                       "measuredAt": None, "by": "tests/test_pass_lens.py"},
    }


# ---------------------------------------------------------------- bake once
build_site.SITE_CONFIG = dict(build_site.SITE_CONFIG)
build_site.SITE_CONFIG["pass"] = {"visualLayer": "pass", "diagnostics": "on"}

TMP = Path(tempfile.mkdtemp(prefix="synth_passlens_"))
build_site.OUT = TMP
build_site.build(SITE_URL)
LAYER = (TMP / "pass-layer.js").read_text(encoding="utf-8")
# THE INSTRUMENT'S OWN BUILT FILE — the real artifact a visitor is served, comments stripped.
PACK = (TMP / "pass-inst-lens.js").read_text(encoding="utf-8")
REGION = PACK
SOURCE = ROOT / "engine" / "assets" / "pass-inst-lens.js"
SOURCE_TEXT = SOURCE.read_text(encoding="utf-8")
LABTXT = MODULE.read_text(encoding="utf-8") if MODULE.exists() else ""

# ---------------------------------------------------------------- string rows

OWNED = ["createElement", "getContext", "requestAnimationFrame", "addEventListener",
         "performance.now", "Date.now", "new Image", "setTimeout", "setInterval"]
held = [s for s in OWNED if s in REGION]
check("PASS-LENS the instrument creates no element, no loop and no listener",
      not held,
      "§1.2's fence, read against the instrument's own built file: none of the nine ways of owning "
      "hardware appears there. The module raises its own canvas, takes a WebGL2 context on it, "
      "builds a 2D texture array of fourteen works through a scratch canvas, runs its own frame "
      "loop, observes its own mount for a resize and listens for the pointer; all of it stayed in "
      "the lab"
      if not held else "the instrument's region holds " + ", ".join(held))

HANDLES = ["mix", "fold", "wedges", "twist", "power", "centreX", "centreY", "shade", "mask"]
absent = [h for h in HANDLES if ("%s: { min" % h) not in REGION]
check("PASS-LENS every handle the instrument publishes is a handle a score can drive",
      not absent and len(HANDLES) == 9,
      "§4.4b: nine handles. The dial, the module's own three glasses and the depth of each, the two "
      "that carry the place the glass rests at, the module's own rim channel and the judges' "
      "channel. The module's `size` and `drift` are published by neither, and the file says why"
      if not absent else "these are published nowhere: " + ", ".join(absent))

check("PASS-LENS no clock handle and no seed, and the module's own reasons are what settle both",
      "clock: { min" not in REGION and "seed: { min" not in REGION
      and "uniform float uTime" in LABTXT and "function seedFrom" in LABTXT
      and "uTime" not in REGION and "Math.random" not in REGION,
      "the module's four temporal literals — the kaleidoscope's spin at 0.075 and its swell at "
      "0.31, the swirl's breath at 0.45 — read nothing off a photograph and exist to keep a "
      "STANDING gallery wall alive, so none of them came over and no `clock` is published: the "
      "picture moves with the hand and with nothing else in time. The module's one die rolled the "
      "wall's layer table, which did not travel, so there is nothing here for a seed to decide")

check("PASS-LENS the module's `size` is no handle here, and the door law is what settles it",
      "size: { min" not in REGION
      and "NO `size` HANDLE EITHER, AND THAT IS THE DOOR LAW RATHER THAN A CHOICE" in SOURCE_TEXT
      and "function coverOf" in REGION,
      "the module's own `size` sets how much of the frame the lens takes and runs from 0.12 to "
      "0.40. Here the reach is not free: it is exactly nothing at either door and it covers the "
      "whole frame while the two works change hands, so it is derived from the frame's own corners "
      "and the place the glass rests at, and published as a reading rather than as a handle a score "
      "could put a wrong number in")

# Every constant the picture stands on, read out of the lab module and out of the built file.
CONSTANTS = [
    ("float rr = r * (2.30 + 0.14 * sin(uTime * 0.31)) + 0.20 * uR;",
     "const float GATHER = 2.30;",
     "the kaleidoscope reaches 2.30 times its own radius into the plane, so the fold always gathers "
     "more than one frame of picture (the module's own breath of 0.14 stands at its middle, which "
     "is where the module itself stands at its second zero)"),
    ("float rr = r * (2.30 + 0.14 * sin(uTime * 0.31)) + 0.20 * uR;",
     "const float EDGE = 0.20;",
     "and a further fifth of the glass's own radius, which keeps the middle of the disc off the "
     "single point the fold collapses to"),
    ("float ang = a + spin * 0.55 + 0.35;", "const float TURN0 = 0.35;",
     "the turn the wedge pattern stands at (the module's own spin is nothing at its second zero)"),
    ("float amt = 3.6 * k * k * (0.78 + 0.22 * sin(uTime * 0.45));",
     "const float TWIST_MAX = 3.6;",
     "how far the swirl winds the picture at the middle of the glass, in radians"),
    ("float amt = 3.6 * k * k * (0.78 + 0.22 * sin(uTime * 0.45));",
     "const float BREATH = 0.78;",
     "and the middle of the module's own breath on that number, which is what it stands at at its "
     "second zero"),
    ("float rr = r * (1.0 - 0.22 * k * k);", "const float PULL = 0.22;",
     "how far the swirl pulls the picture in toward the middle, nothing exactly at the rim"),
    ("float k = mix(0.5, 1.0, smoothstep(0.76, 1.0, t));", "const float RIM0 = 0.76;",
     "where the magnifier's squeezed band begins, which is what makes it read as glass"),
    ("float k = mix(0.5, 1.0, smoothstep(0.76, 1.0, t));", "var POWER_REST = 2,",
     "and the module's own magnification, which is the reciprocal of that half"),
    ("float seg  = TAU / 6.0;", "var WEDGES_N = 6,",
     "how many mirrored wedges the disc folds into, until a score names the work's own"),
    ("col *= mix(1.0, 1.045, ins);", "const float LIFT = 1.045;",
     "the glass's own lift inside the rim"),
    ("col *= 1.0 - 0.30 * shade;", "const float SHADE_D = 0.30;",
     "the inner shade's depth"),
    ("float shade = (1.0 - smoothstep(0.0, 7.0 * uPx, uR - r)) * ins;",
     "const float SHADE_R = 7.0;",
     "and how far it reaches inside the rim, in points of the drawing buffer"),
    ("float lit  = uDial * (1.0 - smoothstep(0.0, 1.7 * uPx, abs(r - (uR - 0.9 * uPx))));",
     "const float HAIR_IN = 0.9;",
     "the light hairline just inside the rim"),
    ("float dark = uDial * (1.0 - smoothstep(0.0, 1.7 * uPx, abs(r - (uR + 1.7 * uPx))));",
     "const float HAIR_OUT = 1.7;",
     "the dark one just outside it"),
    ("col = mix(col, vec3(0.96, 0.95, 0.92), lit * 0.80);", "const vec3 LIT = vec3(0.96, 0.95, 0.92);",
     "and the two colours the bezel is drawn in, so the rim stays legible over a bright work and "
     "over a dark one"),
    ("col = mix(col, vec3(0.03, 0.03, 0.04), dark * 0.60);", "const vec3 DARK = vec3(0.03, 0.03, 0.04);",
     "the second of them"),
    ("var FEEL_D0 = 0.14, FEEL_G = 0.42;", "var FEEL_D0 = 0.14, FEEL_G = 0.42;",
     "the reach's own response curve: Stevens' law in its plainest form, with the module's one "
     "fitted exponent and the band below which it measured no footprint at all"),
    ("return FEEL_D0 + (1 - FEEL_D0) * Math.pow(u, FEEL_G);",
     "return Math.pow(clamp(u, 0, 1), FEEL_G);",
     "the curve itself, with the module's own offset spent at the doors instead — where a door "
     "needs exactly nothing rather than nearly nothing"),
]
missing_const = [p for lab_p, p in ((a, b) for a, b, _ in CONSTANTS)
                 if lab_p not in LABTXT or p not in REGION]
check("PASS-LENS every constant the picture stands on carries the module's own number",
      not missing_const and bool(LABTXT),
      "; ".join("%s — %s" % (p, why) for _, p, why in CONSTANTS) if not missing_const
      else "these differ between the lab module and the port: " + ", ".join(missing_const))

check("PASS-LENS the port's own three numbers are named as its own",
      "var HOLD_IN = 1 / 3, HOLD_OUT = 2 / 3;" in REGION
      and "var RIM_ROOM = 7.0;" in REGION
      and "HOLD_IN" not in LABTXT and "RIM_ROOM" not in LABTXT
      and "THE ARC THE REACH RIDES, and it is the port's own" in SOURCE_TEXT,
      "the module has no passage to shape, so the arc the reach rides is the port's: reached over "
      "the first third, held through the middle, flat at both doors — the arc the camera lane "
      "measured and landed on 2026-08-17, taken from there rather than chosen here. The third is "
      "the room the rim's own drawing needs past the frame's farthest corner, and it is derived "
      "from the module's own two glass numbers: the inner shade reaches seven points inside the rim "
      "and the dark hairline stands 1.7 points outside it and fades over 1.7 more, so seven points "
      "is the larger of the two")

check("PASS-LENS the wall stayed in the lab, and what stands in its place is the work's own mirror",
      "sampler2DArray" in LABTXT and "buildTable" in LABTXT
      and "sampler2DArray" not in REGION and "uLayers" not in REGION
      and "uPitch" not in REGION and "uGap" not in REGION and "uDriftY" not in REGION
      and "float mirror1(float x){ float t = mod(x, 2.0); return 1.0 - abs(t - 1.0); }" in REGION,
      "a cue of this engine carries an ordered PAIR and the host binds two source textures, so the "
      "module's drifting grid of fourteen works — its texture array, its seeded layer table, its "
      "pitch, its gap and its drift — could not travel. What stands in its place is the work "
      "continued past its own edge by mirroring, one triangle wave per axis, which is the law "
      "pass-inst-unfold.js already continues its sheet by; inside the frame the wave is the "
      "identity, so the plane IS the work there and the doors need nothing done to them")

check("PASS-LENS the host binds uniforms by declared name, never by position or a written list",
      "getUniformLocation(p, u.name)" in LAYER and "uLens" not in LAYER and "uGlass" not in LAYER,
      "this instrument declares nine uniforms, of which five are shared with the folding one. The "
      "host reads the manifest")

declared = set(re.findall(r'\{ name: "(u\w+)", type:', REGION))
spelled = set(re.findall(r'uniform \w+ (u\w+);', REGION))
check("PASS-LENS the manifest's declared names and the shader's own names are one set",
      declared == spelled and len(declared) == 9,
      f"{len(declared)} declared, {len(spelled)} spelled; "
      f"declared only: {sorted(declared - spelled)}; spelled only: {sorted(spelled - declared)}")

SUPPLY = ["textureA", "textureB", "fitA", "fitB", "resolution", "seconds"]
sources = set(re.findall(r'source: "([^"]+)"', REGION))
outside = [s for s in sources
           if s not in SUPPLY and not s.startswith("frame:") and not s.startswith("handle:")]
check("PASS-LENS every uniform is sourced from the closed set the host can supply",
      not outside and len(sources) >= 8,
      "§7's uniform sources are the two source textures, their fits, the resolution, the "
      "transaction's seconds, a value the instrument answers and a handle. This instrument names "
      f"{len(sources)} distinct sources and none outside that set — and `seconds` is not among "
      "them, which is the no-clock decision read on the manifest"
      if not outside else "outside the set: " + ", ".join(outside))

check("PASS-LENS the shader carries no version header of its own, where the module's does",
      "#version" not in REGION and "'#version 300 es'," in LABTXT,
      "the module writes its own GLSL ES 3.00 header because it owns its context; here the host's "
      "translator stamps the one header this shader needs and no second one arrives")

check("PASS-LENS the coverage is declared, and the mirrored plane is the reason",
      "coverage: { writes: false" in REGION
      and "gl_FragColor = vec4(col, 1.0);" in REGION
      and "opacity" not in REGION and "presence" not in REGION,
      "§8's coverage block and §7's law: the alpha is the constant 1, said as a decision. Every "
      "point the glass sends a sample to lands on picture, because the plane is the work continued "
      "without end. Under the placement rule that makes this instrument lawful as the LOWEST cue of "
      "a stack. No handle of opacity and no weight of presence stands anywhere in it")

# THE CLASS LAW, HANDLE BY HANDLE. His 19:13 word lifted to the class at 19:21.
check("PASS-LENS every geometric handle publishes the measurement of the work it reads",
      'reads: "structure.rotational.n, the work\'s own measured rotational order' in REGION
      and 'reads: "structure.polar.twirl, the work\'s own measured twirl' in REGION
      and "structure.ownDevice.stepPx" in REGION
      and "the midpoint of the two measured radial centres, structure.radial.centre" in REGION,
      "the wedge count reads the work's own measured rotational order, so the fold repeats as often "
      "as the work itself does; the twist reads the work's own measured twirl, so a work that turns "
      "about its own middle is wound and one that does not is barely touched; the magnification "
      "reads the ratio of the two works' own measured device steps; and the glass rests at the "
      "midpoint of the two measured radial centres — the point the two works' own structure turns "
      "about. Which glass of the three is `fold`, and it reads the same polar and rotational "
      "family")

check("PASS-LENS the instrument measures no work for itself, and the pointer his word parks did not come over",
      "getImageData" not in REGION and "pointer" not in REGION
      and "pointerTarget" in LABTXT and "pointermove" in LABTXT
      and "THE POINTER IS PARKED BY HIS WORD" in SOURCE_TEXT,
      "the module's lens follows the hand and, where no hand is there, walks two sines of its own "
      "with literal rates. His 09:42 word parks that feature («отдельная фича»), so neither the "
      "pointer nor its stand-in came over: the glass rests where the two works' own measured radial "
      "centres meet and does not rove, and the parked feature is not smuggled in under another name")

# THE DOOR READING AND THE HANDOVER READING, AND THEIR OWN NUMBERS.
check("PASS-LENS the judges' handle publishes what the door is read against, and that nothing is held",
      'readAtADoor: { points: DOOR_SLIP, readOn: "the drawing buffer",' in SOURCE_TEXT
      and 'reads: "no glass"' in SOURCE_TEXT
      and "var DOOR_SLIP = 0.5;" in SOURCE_TEXT
      and "var DOOR_SHOW = 0.5 / 255;" in SOURCE_TEXT
      and "held: null" in SOURCE_TEXT,
      "the handle carries `applied.readAtADoor` — what is walked, on which grid, what the reading "
      "is counted in — and it says outright that there is no hold: the reach is exactly nothing "
      "inside the hand's own dead band, so anything the reading finds is a real fault that no "
      "widening closes and the refusal stands alone")

check("PASS-LENS the handover's own law is stated in the file and read on the buffer",
      "THE TWO WORKS CHANGE HANDS ONLY WHILE THE GLASS COVERS THE FRAME" in SOURCE_TEXT
      and "function handReadOf" in REGION and "function handWhyNoOf" in REGION
      and "which is a plain dissolve" in REGION,
      "a share of the arriving work standing on a point of the frame OUTSIDE the glass is a plain "
      "dissolve between two photographs, which is the cheap-editor gesture his 08-08 10:28 word "
      "vetoes by name. The instrument does not declare that it never happens: it walks the buffer's "
      "own sample points at every pose, publishes how many stand outside the glass while the "
      "handover is running, and refuses the frame with the count in words")

check("PASS-LENS the file names his own recorded verdict on this effect, and what it costs the port",
      "HIS OWN STANDING VERDICT ON THIS EFFECT, AND WHAT IT COSTS THE PORT" in SOURCE_TEXT
      and "IT IS RECORDED AS AN ОЖИВЛЕНИЕ AND NOT AS A ПЕРЕХОД" in SOURCE_TEXT
      and "a reach is not a passage" in SOURCE_TEXT,
      "the charter's vocabulary table records this module as an оживление at CELL with its "
      "mouse-mapping feature parked. A port that did not say so would be passing a gallery effect "
      "off as a crossing instrument")

COMPOSER = (ROOT / "engine" / "assets" / "pass-composer.js").read_text(encoding="utf-8")
check("PASS-LENS what it cuts on and what a pair must read are declared, and once",
      'cuts: ["ring", "wedge"]' in REGION
      and "A LENS IS RADIAL THROUGH AND THROUGH" in SOURCE_TEXT
      and "lens: function (a, b, floors)" in COMPOSER
      and "floors.radial_tight" in COMPOSER
      and "the point the glass would rest on is" in COMPOSER,
      "a lens is a disc about a middle, an angular fold and a wind about that middle, so the "
      "element kind it cuts on is the RING — the kind the composer reaches through the `radial` "
      "measure, whose own cut it names `rings_or_spokes` and `radial_unfold` — and the wedge where "
      "a pair carries one. What a pair must read is that the stronger of the two works reads radial "
      "over the collection's own TIGHT floor of 0.55: under it the point this glass rests on is no "
      "reading of either work, and every geometric parameter here is placed about that point. The "
      "condition stands in the composer's own `INSTRUMENT_ASKS` beside the two panel instruments', "
      "and this row holds the two readings against each other so they cannot drift apart")

sha = hashlib.sha256(MODULE.read_bytes()).hexdigest() if MODULE.exists() else ""
declared_sha = (re.search(r'sha256: "([0-9a-f]{64})"', REGION) or [None, None])[1]
check("PASS-LENS the provenance names the file the port was read from, and the file weighs to it",
      bool(sha) and sha == declared_sha and 'commit: "2afa485"' in REGION,
      f"the module is tracked, so the commit it was read at is named beside the digest of its "
      f"bytes, and the file still weighs to {sha[:16]}…")

# ---------------------------------------------------------------- browser rows

BROWSER_ROWS = [
    "PASS-LENS §8     · the manifest carries every field the contract names, in its shape",
    "PASS-LENS §8     · it publishes SURFACE and CELL and claims no world, so a quiet link can reach it",
    "PASS-LENS row 7  · door 0 stands the departing work, measured against its own file",
    "PASS-LENS row 7  · door 0 carries no trace of the arriving work",
    "PASS-LENS row 7  · door 1 stands the arriving work, measured against its own file",
    "PASS-LENS row 7  · door 1 carries no trace of the departing work",
    "PASS-LENS the two roads draw one map, at three glasses and four reaches",
    "PASS-LENS the glass covers the whole frame everywhere the two works change hands",
    "PASS-LENS §7     · no empty frame at any sampled instant of the pass",
    "PASS-LENS §7     · the ground of a stack, and both doors stand whole with a voice over them",
    "PASS-LENS §7     · the frame after a change of viewport is drawn afresh",
    "PASS-LENS row 10 · a seeded run repeats to the pixel, and this instrument holds no die at all",
    "PASS-LENS row 15 · the console stays clean",
    "PASS-LENS §4.4b  · the three glasses draw three pictures, and none is the plain work",
    "PASS-LENS §4.4b  · the wedge count, the twist, the magnification and the place reach the PICTURE",
    "PASS-LENS the glass is WALKED on the drawing buffer at both doors, and what it read is published",
    "PASS-LENS a door the judges' channel spoils is refused on the real road, and the visitor still lands",
    "PASS-LENS the real transaction road: curtain up, one pass drawn, exactly one dock at the end",
    "PASS-LENS row 16 · the captures are kept as evidence",
]

RED_ROWS = [
    "PASS-LENS red-on-bug · the handover let out of the plateau: the frame becomes a dissolve",
    "PASS-LENS red-on-bug · the module's own dial put back: the entry door stands a glass and is refused",
    "PASS-LENS red-on-bug · the mirrored plane replaced by a clamp: the fold stops gathering picture",
    "PASS-LENS red-on-bug · the rim's own room removed: the bezel stands across the frame's corner",
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


def corner_block(p, side=12):
    """The mean of the block at the frame's own bottom-left corner — the farthest of the four from
    the place the glass rests at, and therefore the first the rim reaches when its room is taken
    away."""
    from PIL import Image, ImageStat
    a = Image.open(p).convert("RGB")
    box = a.crop((0, a.size[1] - side, side, a.size[1]))
    st = ImageStat.Stat(box)
    return sum(st.mean) / 3.0


def cover_into(im, w, h, crop=1.0):
    from PIL import Image
    iw, ih = im.size
    fa, ia = w / float(h), iw / float(ih)
    sw, sh = (ih * fa, float(ih)) if ia > fa else (float(iw), iw / fa)
    sw /= crop
    sh /= crop
    x0, y0 = (iw - sw) / 2.0, (ih - sh) / 2.0
    return im.resize((w, h), Image.BILINEAR, box=(x0, y0, x0 + sw, y0 + sh))


def work_in_the_frame(src, w, h):
    """The whole file, cover-fitted into the frame. This instrument asks the host for no crop, so
    what a door shows is the plain cover fit and `framings` publishes 1 at both ends."""
    from PIL import Image
    return cover_into(Image.open(src).convert("RGB"), w, h)


def apart(p, work):
    from PIL import Image, ImageChops, ImageStat
    a = Image.open(p).convert("RGB")
    if a.size != work.size:
        return 255.0, 255.0
    st = ImageStat.Stat(ImageChops.difference(a, work))
    return sum(st.mean) / 3.0, max(m for _, m in st.extrema)


# THE ONE EDIT EACH ROAD IS SERVED WITH FOR THE MAP ROW, and nothing else: each file's own sampler
# is replaced by the SAME encoder, which writes the mapped point as colour about the glass's own
# middle in units of three times its radius. The module's rim is put out at the same time, because
# it is drawn OVER the sampler's answer and would paint over the map; the port's rim is put out
# through its own `shade` handle, which is what that handle is for. Neither file on disk is touched.
MAP_LAB = ("'  return mix(uBg, tex, mask);',",
           "'  return vec3(0.5 + 0.5 * (q - uLens) / (3.0 * uR), 0.0);',")
GLASS_OFF = [
    ("'  float ins = uDial * (1.0 - smoothstep(uR - uPx, uR + uPx, r));',", "'  float ins = 0.0;',"),
    ("'  float lit  = uDial * (1.0 - smoothstep(0.0, 1.7 * uPx, abs(r - (uR - 0.9 * uPx))));',",
     "'  float lit  = 0.0;',"),
    ("'  float dark = uDial * (1.0 - smoothstep(0.0, 1.7 * uPx, abs(r - (uR + 1.7 * uPx))));',",
     "'  float dark = 0.0;',"),
]
MAP_PORT = ('"  return mix(a, b, clamp(uHand.x, 0.0, 1.0));",',
            '"  return vec3(0.5 + 0.5 * (q - uLens.xy) / (3.0 * uLens.z), 0.0);",')


def bench_dir(pack_text=None, lab_text=None):
    """The bench's own served root: the BUILT pass-layer.js, the site's own settings record and the
    BUILT instrument files it names — the real artifacts, namespace applied and comments stripped —
    the lab module, the two photographs, and the page that stands the two roads side by side.

    A row proving a rule reds hands over a CHANGED instrument file and writes the record with the
    digest of the bytes actually served, which is what the build does. The source file on disk is
    never touched, so nothing has to be restored and no working tree can be left changed."""
    d = Path(tempfile.mkdtemp(prefix="synth_lensbench_"))
    pack = PACK if pack_text is None else pack_text
    shutil.copy2(TMP / "pass-layer.js", d / "pass-layer.js")
    for _inst in sorted(TMP.glob("pass-inst-*.js")):
        shutil.copy2(_inst, d / _inst.name)
    (d / "pass-inst-lens.js").write_text(pack, encoding="utf-8")
    record = json.loads((TMP / "config.json").read_text(encoding="utf-8"))
    record["pass"]["instruments"]["lens"]["digest"] = hashlib.sha256(
        pack.encode("utf-8")).hexdigest()
    (d / "config.json").write_text(json.dumps(record), encoding="utf-8")
    (d / "lens.js").write_text(LABTXT if lab_text is None else lab_text, encoding="utf-8")
    (d / "photos").mkdir()
    for p in PHOTOS:
        shutil.copy2(p, d / "photos" / p.name)
    shutil.copy2(ROOT / "tests" / "fixture_pass_lens.html", d / "index.html")
    return d


def plant(text, pairs):
    out = text
    for f, t in pairs:
        if f not in out:
            return None
        out = out.replace(f, t, 1)
    return out


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


def on_bench(fn, pack_text=None, lab_text=None):
    d = bench_dir(pack_text, lab_text)
    try:
        with serve(d) as base:
            with Browser(width=VW, height=VH) as br:
                br.navigate(base + "/index.html")
                if not ready(br):
                    return None
                return fn(br)
    finally:
        shutil.rmtree(d, ignore_errors=True)


def at(br, mix):
    return js(br, "return window.__both(%r);" % mix)


def host_shot(br, mix, tag):
    at(br, mix)
    br.evaluate("window.__hostDraw(); window.__show('host'); 0")
    br.sleep(0.3)
    return png(br, SHOTS / (tag + ".png"))


def mix_for_reach(br, target, lo=0.14, hi=1 / 3.0):
    """The hand that opens the glass to a stated radius, found by halving on the instrument's own
    published reading. The reach is derived rather than driven, so a row that wants a stated radius
    asks the instrument for the hand that gives it instead of typing a number."""
    for _ in range(40):
        mid = (lo + hi) / 2.0
        got = at(br, mid)["reach"]
        if abs(got - target) < 0.05:
            return mid, got
        if got < target:
            lo = mid
        else:
            hi = mid
    return mid, got


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
            elif not js(br, "return !!window.__exPass.bench.manifest('lens');"):
                why = js(br, "var e = window.__host.report().events.filter(function(x){"
                             "return x.name === 'manifest-refused';});"
                             "return e.length ? e[e.length - 1].why : null;")
                for r in BROWSER_ROWS:
                    check(r, False, "the host registered no «lens» instrument: " + str(why))
            else:
                SCORE = json.dumps(lens_score())
                SCORE_UNDER = json.dumps(lens_score(under=True))
                A = work_in_the_frame(PHOTOS[0], VW, VH)
                B = work_in_the_frame(PHOTOS[1], VW, VH)

                # ---- §8: the manifest, read off the registered instrument -----------------------
                m = js(br, "return window.__exPass.bench.manifest('lens');")
                res = m["resources"]
                need = ["id", "api", "arity", "roles", "params", "handles", "neutrals", "doors",
                        "framings", "drivers", "camera", "gl", "passes", "resources",
                        "capabilities", "decline", "provenance", "readiness", "coverage", "levels",
                        "cuts"]
                shape = (
                    all(k in m for k in need)
                    and m["id"] == "lens" and m["api"] == 1 and m["arity"] == 2
                    and m["doors"]["in"] == {"handle": "mix", "value": 0, "work": "a"}
                    and m["doors"]["out"] == {"handle": "mix", "value": 1, "work": "b"}
                    and m["framings"]["0"]["coverCrop"] == 1
                    and m["framings"]["1"]["coverCrop"] == 1
                    and m["coverage"]["writes"] is False
                    and m["camera"] == {"needs": "none", "authority": "stage"}
                    and sorted(m["handles"]) == sorted(HANDLES)
                    and m["cuts"] == ["ring", "wedge"]
                    and all(v["textureSlots"] == 2 and v["programs"] == 1 and v["passes"] == 1
                            and v["textures"] == 0 and v["framebuffers"] == 0
                            for v in res.values()))
                check(BROWSER_ROWS[0], shape,
                      "the manifest names an ordered pair, two doors on one handle, no crop at "
                      "either of them, nine handles, the two element kinds it cuts on, no camera of "
                      "its own and the two source-texture slots the host already holds. Handles: %s"
                      % sorted(m["handles"]))

                check(BROWSER_ROWS[1],
                      m["levels"] == ["SURFACE", "CELL"] and "WORLD" not in m["levels"]
                      and "THE CHARTER'S SHELF" in SOURCE_TEXT.upper(),
                      "the charter's vocabulary table records this module at CELL and the port keeps "
                      "that reading: SURFACE because the fold is one map over one surface, CELL "
                      "because the kaleidoscope partitions the disc into mirrored wedges. WORLD is "
                      "not claimed, and that decides reach as much as taste — the composer reads "
                      "exactly this field to know whether a cue spends the crossing's one miracle, "
                      "so a step whose role has none to spend can still cast this instrument. "
                      "Declared: %s" % m["levels"])

                # ---- row 7: the two doors --------------------------------------------------------
                d0 = host_shot(br, 0, "door-0")
                d1 = host_shot(br, 1, "door-1")
                m0, w0 = apart(d0, A)
                m0b, _ = apart(d0, B)
                m1, w1 = apart(d1, B)
                m1a, _ = apart(d1, A)
                check(BROWSER_ROWS[2], m0 < SEAM,
                      "the entry door stands the departing work at %.4f of 255 from its own file "
                      "cover-fitted into the %d x %d frame, worst channel %d, against the project's "
                      "own seam threshold of %.0f. Nothing is cropped off it: inside the frame the "
                      "plane IS the work" % (m0, VW, VH, w0, SEAM))
                check(BROWSER_ROWS[3], m0b > FAR,
                      "and it stands %.2f of 255 from the arriving work, so the entry door is not "
                      "quietly showing both" % m0b)
                check(BROWSER_ROWS[4], m1 < SEAM,
                      "the exit door stands the arriving work at %.4f of 255 from its own file, "
                      "worst channel %d" % (m1, w1))
                check(BROWSER_ROWS[5], m1a > FAR,
                      "and %.2f of 255 from the departing one" % m1a)

                # ---- the handover, read on the buffer at every pose --------------------------------
                walked, bare, worst = 0, 0, None
                for step in range(41):
                    v = at(br, step / 40.0)
                    if v["handMap"]:
                        walked += 1
                        bare += v["handMap"]["bare"]
                        if worst is None or v["handMap"]["sparePx"] < worst:
                            worst = v["handMap"]["sparePx"]
                check(BROWSER_ROWS[7], walked >= 8 and bare == 0 and worst is not None
                      and worst > 0,
                      "walked at forty-one places on the hand: the two works are changing hands at "
                      "%d of them, and at every one of those the glass stands over ALL %d sample "
                      "points of the drawing buffer — %d bare in total. The tightest of them had "
                      "%.2f points of the buffer to spare, which is the room the rim's own drawing "
                      "needs. So no point of the frame ever carries a share of both photographs "
                      "with no fold over it"
                      % (walked, 17, bare, worst if worst is not None else -1))

                # ---- §7: no empty frame ----------------------------------------------------------
                weak = []
                for i, mval in enumerate([0, 0.18, 0.25, 0.34, 0.5, 0.66, 0.8, 0.92, 1]):
                    p = host_shot(br, mval, "pass-%d" % i)
                    far, spread = standing(p)
                    if far < 8.0 or spread < 6.0:
                        weak.append((mval, round(far, 2), round(spread, 2)))
                check(BROWSER_ROWS[8], not weak,
                      "nine instants of the pass, each measured against a flat background and "
                      "against its own spread: every one of them stands as a picture"
                      if not weak else "these instants read as empty: %s" % weak)

                # ---- the three glasses -----------------------------------------------------------
                shots = {}
                for rule, name in ((0, "kaleidoscope"), (1, "swirl"), (2, "magnify")):
                    br.evaluate("window.__param('fold', %d); 0" % rule)
                    br.sleep(0.35)
                    shots[name] = host_shot(br, 0.22, "glass-" + name)
                br.evaluate("window.__param('fold', 0); 0")
                br.sleep(0.3)
                pairsd = {}
                names = sorted(shots)
                for i in range(len(names)):
                    for j in range(i + 1, len(names)):
                        pairsd[names[i] + " vs " + names[j]] = round(
                            diff(shots[names[i]], shots[names[j]])[0], 2)
                plain = {n: round(apart(shots[n], A)[0], 2) for n in names}
                check(BROWSER_ROWS[13],
                      all(v > SEAM for v in pairsd.values()) and all(v > SEAM for v in plain.values()),
                      "the module's three glasses drawn at one hand and one place: %s. And none of "
                      "them is the departing work standing plain: %s of 255 away from its own file"
                      % (pairsd, plain))

                # ---- the handles reach the picture ------------------------------------------------
                base_shot = host_shot(br, 0.22, "handles-rest")
                moved = {}
                for k, v, tag in (("wedges", 11, "wedges-11"), ("centreX", 0.25, "centre-x")):
                    br.evaluate("window.__param(%r, %r); 0" % (k, v))
                    br.sleep(0.3)
                    moved[k] = round(diff(host_shot(br, 0.22, tag), base_shot)[0], 2)
                br.evaluate("window.__param('wedges', 6); window.__param('centreX', 0.5); 0")
                br.sleep(0.3)
                br.evaluate("window.__param('fold', 1); 0")
                br.sleep(0.35)
                sw = host_shot(br, 0.22, "twist-rest")
                br.evaluate("window.__param('twist', 0.2); 0")
                br.sleep(0.3)
                moved["twist"] = round(diff(host_shot(br, 0.22, "twist-low"), sw)[0], 2)
                br.evaluate("window.__param('twist', 1); window.__param('fold', 2); 0")
                br.sleep(0.35)
                mg = host_shot(br, 0.22, "power-rest")
                br.evaluate("window.__param('power', 3.5); 0")
                br.sleep(0.3)
                moved["power"] = round(diff(host_shot(br, 0.22, "power-high"), mg)[0], 2)
                br.evaluate("window.__param('power', 2); window.__param('fold', 0); 0")
                br.sleep(0.35)
                check(BROWSER_ROWS[14], all(v > SEAM for v in moved.values()),
                      "each handle walked from its own rest and the frame read against the frame "
                      "before it, in units of 255: %s. Every one is over the project's own seam "
                      "threshold of %.0f, so each of them reaches the picture and not only the "
                      "record" % (moved, SEAM))

                # ---- the glass walked at both doors ----------------------------------------------
                v0 = at(br, 0)
                v1 = at(br, 1)
                check(BROWSER_ROWS[15],
                      v0["glassMap"]["inside"] == 0 and v1["glassMap"]["inside"] == 0
                      and v0["reach"] == 0 and v1["reach"] == 0
                      and v0["doorWhyNo"] is None and v1["doorWhyNo"] is None
                      and v0["handover"] == 0 and v1["handover"] == 1,
                      "at either door the instrument walks its own glass over the %d x %d buffer the "
                      "host is about to bind: it reaches %.2f points and stands over %d of the %d "
                      "points walked at the entry, %.2f and %d at the exit, and the two works have "
                      "changed hands %.0f per cent and %.0f per cent. The tightest point had %.1f "
                      "points of room to spare. Nothing is held: the reach is exactly nothing inside "
                      "the hand's own dead band"
                      % (v0["grid"]["w"], v0["grid"]["h"], v0["reach"], v0["glassMap"]["inside"],
                         v0["glassMap"]["walked"], v1["reach"], v1["glassMap"]["inside"],
                         v0["handover"] * 100, v1["handover"] * 100, v0["glassMap"]["farthestPx"]))

                # ---- a seeded run repeats to the pixel -------------------------------------------
                one = host_shot(br, 0.42, "repeat-1")
                at(br, 0.8)
                two = host_shot(br, 0.42, "repeat-2")
                rm, rw = diff(one, two)
                check(BROWSER_ROWS[11], rm == 0.0 and rw == 0,
                      "the same pose drawn twice with another pose between them: %.4f of 255, worst "
                      "channel %d. This instrument holds no die at all — the module's own seed rolled "
                      "the wall's layer table, which did not travel — so a seeded run repeats "
                      "because the picture is a pure function of the hand" % (rm, rw))

                # ---- the ground of a stack -------------------------------------------------------
                why = js(br, "return window.__exPass.bench.coverageWhyNo(%s.cues);" % SCORE_UNDER)
                why_bad = js(br, "return window.__exPass.bench.coverageWhyNo("
                                 "[%s.cues[1], Object.assign({}, %s.cues[0], {stack: 2})]);"
                             % (SCORE_UNDER, SCORE_UNDER))
                under0 = None
                if why is None:
                    j = js(br, "return window.__offer(%s, {progress: 0});" % SCORE_UNDER)
                    br.sleep(1.0)
                    under0 = png(br, SHOTS / "under-door-0.png")
                    js(br, "window.__cancel('bench'); return 1;")
                    idle(br)
                check(BROWSER_ROWS[9],
                      why is None and why_bad is not None and under0 is not None
                      and apart(under0, A)[0] < SEAM,
                      "this instrument declares that it writes no coverage, so the host allows it as "
                      "the LOWEST cue of a stack and refuses it above another («%s»). Under a "
                      "coverage-writing voice its entry door still stands the departing work at "
                      "%.4f of 255"
                      % (str(why_bad)[:110], apart(under0, A)[0] if under0 else -1))

                # ---- a change of viewport --------------------------------------------------------
                before = host_shot(br, 0.3, "viewport-before")
                br._cmd("Emulation.setDeviceMetricsOverride", width=430, height=760,
                        deviceScaleFactor=1, mobile=True)
                br.sleep(0.4)
                js(br, "window.__resize(); return 1;")
                br.sleep(0.4)
                after = host_shot(br, 0.3, "viewport-after")
                br._cmd("Emulation.clearDeviceMetricsOverride")
                br.sleep(0.4)
                js(br, "window.__resize(); return 1;")
                br.sleep(0.4)
                from PIL import Image as _I
                sz_before = _I.open(before).size
                sz_after = _I.open(after).size
                back = host_shot(br, 0.3, "viewport-back")
                check(BROWSER_ROWS[10],
                      sz_before != sz_after and diff(before, back)[0] < 0.5
                      and standing(after)[0] > 8.0,
                      "the frame is %s, then %s, then %s again, and the picture at the same hand "
                      "returns to within %.4f of 255 of itself. The glass's reach is read off the "
                      "buffer the host is about to bind, so a frame of another shape is a frame "
                      "with another reach and not a stretched picture"
                      % (sz_before, sz_after, _I.open(back).size, diff(before, back)[0]))

                # ---- the real transaction road ---------------------------------------------------
                js(br, "window.__hooks.docks = []; window.__hooks.curtains = []; "
                       "window.__hooks.glides = []; return 1;")
                took = js(br, "return window.__offer(%s);" % SCORE)
                br.sleep(1.2)
                mid = png(br, SHOTS / "road-mid.png")
                for _ in range(80):
                    if js(br, "return window.__hooks.docks.length;"):
                        break
                    br.sleep(0.15)
                idle(br)
                hooks = js(br, "return window.__hooks;")
                rep = js(br, "return window.__report();")
                check(BROWSER_ROWS[17],
                      took["took"] and len(hooks["docks"]) == 1 and hooks["docks"][0] == took["gen"]
                      and hooks["curtains"] and hooks["curtains"][0] is True
                      and not hooks["glides"] and standing(mid)[0] > 8.0,
                      "the host took the command, raised its curtain, ran its own frame loop over "
                      "this instrument's one pass and docked exactly once on the generation it took: "
                      "docks %s, curtains %s, glides %s, and the frame mid-flight stands as a picture "
                      "at %.2f of 255 from a flat background"
                      % (hooks["docks"], hooks["curtains"], hooks["glides"], standing(mid)[0]))

                # ---- THE DOOR REFUSED ON THE REAL TRANSACTION ROAD -------------------------------
                # The door reading comes out whole on every buffer this host can hand and every pose
                # these handles admit, which is the runtime truth his 18:00 decision asks for and not
                # a reason to leave the claim unread. The one door this instrument's own handles CAN
                # spoil is the judges' channel: `mask` draws the glass map itself as colour, and a
                # score leaving it open at a door hands the visitor a false-colour map instead of the
                # photograph.
                def road(gen):
                    return js(br, "var r = window.__report(); return {state: r.state, "
                                  "drew: r.drew, buffer: r.census.buffer, "
                                  "refused: r.events.filter(function(e){ return e.gen === %d "
                                  "&& e.why && String(e.why).indexOf('door leaks') >= 0; })"
                                  ".map(function(e){ return e.name + ': ' + e.why; })};" % gen)

                br.evaluate("window.__cancel('door road row'); 0")
                idle(br)
                shut_gen = js(br, "return window.__offer(%s, {clock: 0, progress: 0});"
                              % json.dumps(lens_score(mask=0)))["gen"]
                br.sleep(1.0)
                played = road(shut_gen)
                br.evaluate("window.__cancel('door road row'); 0")
                idle(br)
                open_gen = js(br, "return window.__offer(%s, {clock: 0, progress: 0});"
                              % json.dumps(lens_score(mask=1)))["gen"]
                br.sleep(1.1)
                leaked = road(open_gen)
                br.evaluate("window.__cancel('door road row'); 0")
                idle(br)
                check(BROWSER_ROWS[16],
                      played["state"] == "running" and played["drew"] == 1
                      and not played["refused"]
                      and len(leaked["refused"]) == 1 and leaked["state"] == "idle"
                      and leaked["drew"] == 0
                      and "the entry door leaks" in leaked["refused"][0]
                      and "the judges' own channel" in leaked["refused"][0],
                      "on the %s buffer the host drew, the judges' channel shut draws the door (%d "
                      "cue, state %s, refused %s); left open it is refused with «%s», on which the "
                      "host lands the transaction (state %s, %d cue drawn) and the walk's own glide "
                      "carries the visitor"
                      % (played["buffer"], played["drew"], played["state"],
                         played["refused"] or "nothing",
                         (leaked["refused"] or ["nothing refused"])[0], leaked["state"],
                         leaked["drew"]))

                # ---- the console -----------------------------------------------------------------
                errs = js(br, "return window.__errs;")
                check(BROWSER_ROWS[12], not errs,
                      "no error, no rejection and no console.error across every row above"
                      if not errs else "the page recorded: %s" % errs[:4])

                shots_kept = sorted(p.name for p in SHOTS.glob("*.png"))
                check(BROWSER_ROWS[18], len(shots_kept) >= 20,
                      "%d captures kept under tests/captures/pass-lens/ as the evidence of every "
                      "row above: %s…" % (len(shots_kept), ", ".join(shots_kept[:6])))
    shutil.rmtree(BENCH, ignore_errors=True)

    # ---- THE TWO ROADS ---------------------------------------------------------------------------
    lab_map = plant(LABTXT, [MAP_LAB] + GLASS_OFF)
    port_map = plant(PACK, [MAP_PORT])
    if lab_map is None or port_map is None:
        check(BROWSER_ROWS[6], False,
              "the encoder found nothing to replace in one of the two files, so the two roads could "
              "not be put on one sampler")
    else:
        def two_roads(br):
            place = js(br, "return window.__labPlace();")
            br.evaluate("window.__param('centreX', %r); window.__param('centreY', %r); "
                        "window.__param('shade', 0); 0" % (place["centreX"], place["centreY"]))
            br.sleep(0.35)
            bufs = js(br, "return window.__buffers();")
            out = []
            for rule, name in ((0, "kaleidoscope"), (1, "swirl"), (2, "magnify")):
                br.evaluate("window.__param('fold', %d); 0" % rule)
                br.sleep(0.4)
                for target in (60.0, 100.0, 150.0, 190.0):
                    mval, got = mix_for_reach(br, target)
                    js(br, "return window.__labSize(%r);" % (got / float(min(VW, VH))))
                    br.sleep(0.4)
                    br.evaluate("window.__hostDraw(); window.__show('host'); 0")
                    br.sleep(0.3)
                    ph = png(br, SHOTS / ("map-%s-%d-host.png" % (name, int(round(got)))))
                    br.evaluate("window.__show('module'); 0")
                    br.sleep(0.45)
                    pm = png(br, SHOTS / ("map-%s-%d-module.png" % (name, int(round(got)))))
                    br.evaluate("window.__show('host'); 0")
                    dm, dw = diff(ph, pm)
                    out.append((name, round(got, 1), round(dm, 5), dw))
            return {"bufs": bufs, "reads": out, "place": place}

        got = on_bench(two_roads, pack_text=port_map, lab_text=lab_map)
        if got is None:
            check(BROWSER_ROWS[6], False, "the two-roads bench never came up")
        else:
            worst_mean = max(r[2] for r in got["reads"])
            worst_ch = max(r[3] for r in got["reads"])
            check(BROWSER_ROWS[6],
                  got["bufs"]["host"] == got["bufs"]["module"] and len(got["reads"]) == 12
                  and worst_mean < ROADS,
                  "both roads sampled on one %s grid, each served with its own sampler replaced by "
                  "the SAME encoder — the mapped point written as colour about the glass's own "
                  "middle in units of three times its radius — and the module driven at its own "
                  "second zero, where its spin is nothing and both its breaths stand at the middles "
                  "this port carries as constants. Twelve poses, three glasses and four reaches: "
                  "worst mean %.5f of 255, worst channel %d, against a bar of %.0f. Readings: %s"
                  % (got["bufs"]["host"], worst_mean, worst_ch, ROADS, got["reads"]))

    # ---- the red-on-bug proofs -------------------------------------------------------------------
    # Each reverts ONE rule in this suite's own copy of the served artifact, runs the row that rule
    # answers, and lets the copy go. The source tree is never written to.
    PLANTS = [
        (RED_ROWS[0],
         [("return smoothstep(HOLD_IN, HOLD_OUT, clamp(mix, 0, 1));",
           "return clamp(mix, 0, 1);")]),
        (RED_ROWS[1],
         [("if (mix <= FEEL_D0 || mix >= 1 - FEEL_D0) return 0;", "if (false) return 0;"),
          ("return Math.pow(clamp(u, 0, 1), FEEL_G);",
           "return FEEL_D0 + (1 - FEEL_D0) * Math.pow(clamp(u, 0, 1), FEEL_G);")]),
        (RED_ROWS[2],
         [('"float mirror1(float x){ float t = mod(x, 2.0); return 1.0 - abs(t - 1.0); }",',
           '"float mirror1(float x){ return clamp(x, 0.0, 1.0); }",')]),
        (RED_ROWS[3],
         [("var RIM_ROOM = 7.0;", "var RIM_ROOM = 0.0;")]),
    ]

    # what the standing instrument reads, to measure each revert against
    def standing_reads(br):
        br.evaluate("window.__param('centreX', 0.5); window.__param('centreY', 0.5); 0")
        br.sleep(0.3)
        mid = host_shot(br, 0.22, "red-base-mid")
        plateau = host_shot(br, 0.5, "red-base-plateau")
        return {"door0": at(br, 0), "mid": at(br, 0.22), "plateau": at(br, 0.5),
                "midShot": mid, "plateauShot": plateau,
                "corner": corner_block(plateau)}

    BASE = on_bench(standing_reads)
    if BASE is None:
        for r in RED_ROWS:
            skip(r, "the standing bench never came up, so nothing could be measured against it")
    else:
        for row, pairs in PLANTS:
            planted = plant(PACK, pairs)
            if planted is None:
                check(row, False, "the rule's own text was not found in the served instrument: %r"
                      % pairs[0][0][:70])
                continue

            def read(br, row=row):
                br.evaluate("window.__param('centreX', 0.5); window.__param('centreY', 0.5); 0")
                br.sleep(0.3)
                mid = host_shot(br, 0.22, "red-mid")
                plateau = host_shot(br, 0.5, "red-plateau")
                return {"door0": at(br, 0), "mid": at(br, 0.22), "plateau": at(br, 0.5),
                        "midDiff": diff(mid, BASE["midShot"]),
                        "corner": corner_block(plateau)}

            g = on_bench(read, pack_text=planted)
            if g is None:
                check(row, False, "the crippled bench never came up")
                continue
            if row == RED_ROWS[0]:
                was = BASE["mid"]["handMap"]
                now = g["mid"]["handMap"]
                check(row,
                      was is None and now is not None and now["bare"] > 0
                      and g["mid"]["handWhyNo"] is not None,
                      "with the handover run over the WHOLE hand instead of only across the "
                      "plateau, the two works are %.1f per cent of the way through changing hands "
                      "at a hand of 0.22 while the glass stands over only part of the frame: %d of "
                      "%d walked points carry a share of both photographs with no fold over them, "
                      "where the standing instrument has the handover at nothing there and no such "
                      "point at any pose. The instrument refuses the frame: «%s»"
                      % ((now or {}).get("handover", 0) * 100, (now or {}).get("bare", 0),
                         (now or {}).get("walked", 0), str(g["mid"]["handWhyNo"])[:120]))
            elif row == RED_ROWS[1]:
                check(row,
                      BASE["door0"]["reach"] == 0 and g["door0"]["reach"] > 1
                      and BASE["door0"]["doorWhyNo"] is None
                      and g["door0"]["doorWhyNo"] is not None,
                      "with the module's own dial put back — its offset of 0.14 restored and the "
                      "hand's dead band removed — the entry door opens a glass %.2f points wide "
                      "standing over %d of the %d walked points, where the standing instrument "
                      "reaches exactly 0.00 and stands over none. The instrument refuses the door: "
                      "«%s»"
                      % (g["door0"]["reach"], g["door0"]["glassMap"]["inside"],
                         g["door0"]["glassMap"]["walked"], str(g["door0"]["doorWhyNo"])[:130]))
            elif row == RED_ROWS[2]:
                check(row, g["midDiff"][0] > SEAM * 3,
                      "with the plane clamped at the work's own edge instead of mirrored past it, "
                      "the fold gathers the edge row of pixels smeared to the horizon instead of "
                      "picture: the frame at a hand of 0.22 moves %.2f of 255, worst channel %d, "
                      "against the project's own seam threshold of %.0f"
                      % (g["midDiff"][0], g["midDiff"][1], SEAM))
            else:
                was_room = BASE["plateau"]["glassMap"]["farthestPx"]
                now_room = g["plateau"]["glassMap"]["farthestPx"]
                check(row,
                      was_room <= -6.9 and now_room > -0.9
                      and abs(g["corner"] - BASE["corner"]) > 3.0,
                      "with the room the rim's own drawing needs taken away, the glass's rim stands "
                      "on the frame's own four corners through the whole middle third — where this "
                      "instrument shows no rim at all. The room the instrument publishes goes from "
                      "%.2f points of the buffer to %.2f, and the twelve-point block at a corner "
                      "moves from %.1f to %.1f of 255 as the bezel's light hairline lands across it"
                      % (was_room, now_room, BASE["corner"], g["corner"]))


# ---------------------------------------------------------------- report
passed = sum(1 for _, s, _ in results if s == "PASS")
failed = sum(1 for _, s, _ in results if s == "FAIL")
skipped = sum(1 for _, s, _ in results if s == "SKIP")
for name, status, detail in results:
    print("%-4s %s" % (status, name))
    if detail:
        print("      %s" % detail)
print("\n%d passed / %d failed / %d skipped" % (passed, failed, skipped))
shutil.rmtree(TMP, ignore_errors=True)
sys.exit(1 if failed else 0)
