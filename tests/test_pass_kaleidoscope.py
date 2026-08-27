#!/usr/bin/env python3
"""PASS-API-V1 — the kaleidoscope instrument on the host's frame.
Run: python3 tests/test_pass_kaleidoscope.py

Root: his word of 2026-08-18 08:52 after walking the live route — «переходы очень однообразные: у
тебя дофига эффектов и ты сделал все очень топорно» — and the port brief every lane works to,
docs/immersive/briefs/reports/lanes/PORT-common.md in the tlvphotos tree. The composer's own census
(S1-D-report, «2 · An opaque instrument on ring and band cuts») names the hole this closes: a `ring`
cut has no instrument that FILLS THE FRAME, so a pair whose ground is the radial measure has no
ground to stand a stack on. docs/design/PASS-API-V1.md §7 (GPU and resources), §8 (the manifest) and
§9's conformance rows 7, 9, 10, 13, 14, 15, 16 and 22 are what this file makes real, together with
§7's coverage law. The lifecycle rows stay in tests/test_pass_api.py and are untouched.

HIS THREE STANDING WORDS ON THIS EFFECT, and where each is measured here. The charter's vocabulary
table (lab/CROSSING-BRIEF.md) reads «approved; wedge seams need retouch (В9); rings>2 washes to
milk».

  · APPROVED — so the mathematics is carried digit for digit, and the constants row below reads BOTH
    files for every number the picture stands on.
  · THE WEDGE SEAMS NEED RETOUCH — the crease row walks the frame ACROSS the fold's own edges, at the
    angles the fold puts them at, and reads how hard the crease stands; the red-on-bug row takes the
    retouch out and the same reading climbs.
  · RINGS OVER 2 WASH TO MILK — the ceiling row reads the published span, and its red-on-bug row
    raises the ceiling to the module's own 5 and measures the frame going pale.

WHAT IS COMPARED, AND AGAINST WHAT.

  The doors. At the dial's two ends one whole work stands, cover-fitted with NO CROP AT ALL — this
  instrument buys its coverage without taking a bite out of the picture, which is what separates it
  from the folding instrument's crop of 1.90. Each door is measured against its own file inside the
  project's seam threshold of 6 of 255.

  THE TWO ROADS. Both draw with WebGL: the module carries its own context and its own fragment
  shader, so one sampler runs through one rasteriser on both sides. The lab module is served with
  FOUR literals changed and the row that reads it says which and why — two are this host's own
  binding (it builds no mip chain and asks for no anisotropy, so a module sampling through a chain
  the host never builds would be compared as a different SAMPLER rather than as a different reading
  of one geometry), and two are the module's own anchor numbers, chosen by eye for its own two
  photographs, pinned to the centre this port reads from the work. The file on disk is never touched.

  The coverage. This instrument declares that it writes none, because every point of the frame reads
  one point of one photograph at every value of the dial. That is measured rather than declared: the
  instrument's own reading walks its sample point over the buffer and no walked point reads outside
  the work at any sampled pose.

  No empty frame. The rows below sample the pass at seven instants and once across a change of
  viewport, and each frame has to stand as a picture.

  The lab module is READ ONLY. Absent, every browser row here is a pinned SKIP that names the missing
  path — never a silent pass.
"""
import base64
import hashlib
import json
import math
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
PHOTOS = [LAB / "photos" / "glass-drum.jpg", LAB / "photos" / "round-tower.jpg"]
MODULE = LAB / "effects" / "kaleidoscope.js"

SITE_URL = "https://synth.example.com"
VW, VH = 390, 844          # the phone frame lab/carrier-check.py measures on
SEAM = 6.0                 # the project's seam threshold, 6 of 255 (TRANSITION-STAGE-V0 §1)
FAR = 40.0                 # further than this from a file and it is a different work
BACKGROUND = (0x08, 0x08, 0x0a)
SPREAD = 10.0

# THE TWO ROADS' BAR. Both roads run one fragment shader over one rasteriser, so what stands between
# them is arithmetic and the crease's own retouch — a band a point and a half wide along each fold
# line, which is a thousandth of the frame. The bar is the project's own seam threshold of 6 of 255.
ROADS = SEAM

# BOTH DOORS ARE THE PLAIN COVER FIT. The module's own flat door is exactly that
# (kaleidoscope.js:376-388) and lab/data/module-contract.json publishes it as `coverCrop: 1.0`; the
# port takes no crop either, because the fold reads the picture through the mirror rather than past
# its edge and nothing has to be held in reserve.
CROP = 1.0

# The centre both roads stand at. The port reads it from the two works' own measured radial centres;
# the served module has its two eye-chosen anchors pinned to it, so the two roads fold about ONE
# point. The middle of the frame is what a pair of centred radial works hands in.
CENTRE = (0.5, 0.5)

SHOTS = ROOT / "tests" / "captures" / "pass-kaleidoscope"

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


DURATION_MS = 6500
WITHIN_MS = 500


def _static(v):
    return {"op": "static", "value": v}


def kal_cue(stack=0, levels_own=None, **statics):
    """The cue, with a track for every one of the ten handles (§4.4b)."""
    P = {"clock": 0, "centreX": CENTRE[0], "centreY": CENTRE[1], "wedges": 8, "twist": 0.55,
         "rings": 1, "reach": 0.30, "shade": 1, "mask": 0}
    P.update(statics)
    nodes = {"k-mix": {"source": "progress"}}
    tracks = {"mix": {"node": "k-mix"}}
    for k, v in P.items():
        nodes["k-" + k] = _static(v)
        tracks[k] = {"node": "k-" + k}
    return {
        "id": "kal-main", "instrument": {"id": "kaleidoscope", "api": 1},
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
    is meant to be played under (COVERAGE.md §3, and the placement rule §7 states)."""
    nodes = {"m-mix": {"source": "progress"}, "m-clock": {"source": "time"}}
    tracks = {"mix": {"node": "m-mix"}, "clock": {"node": "m-clock"}}
    return {
        "id": "over", "instrument": {"id": "matter", "api": 1},
        "voice": "accompaniment", "roles": ["assembly"],
        "levels": ["SURFACE", "TEXTURE"],
        "levelOwnership": {"SURFACE": "reads", "TEXTURE": "owns"},
        "window": [0, DURATION_MS / 1000.0], "works": ["a", "b"], "stack": stack,
        "cameraAuthority": "stage",
        "doors": {"in": {"handle": "mix", "value": 0, "measured": True},
                  "out": {"handle": "mix", "value": 1, "measured": True}},
        "nodes": nodes, "tracks": tracks,
        "resources": {"textures": 0, "textureSlots": 2, "framebuffers": 0, "pingPong": 0,
                      "programs": 1, "passes": 1, "bytesEstimate": 0, "variant": "standard"},
    }


def kal_score(under=False, **statics):
    """`under` puts a coverage-writing voice ABOVE this instrument, which is the placement its own
    declaration buys it: the ground of a stack."""
    cues = [kal_cue(stack=0, **statics)]
    if under:
        cues = cues + [matter_cue(stack=1)]
    res = {"textures": 0, "textureSlots": 2, "framebuffers": 0, "pingPong": 0, "programs": 1,
           "passes": 1, "bytesEstimate": 0}
    return {
        "schema": 2,
        "intent": "one slice of the departing photograph is repeated round the work's own measured "
                  "centre and mirrored at every edge; the rosette deepens to the middle of the "
                  "passage, the two works exchange under its deepest fold, and it closes onto the "
                  "arriving photograph standing whole (lab/effects/kaleidoscope.js)",
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
        "provenance": {"source": "lab/effects/kaleidoscope.js's own declared defaults and constants",
                       "measuredAt": None, "by": "tests/test_pass_kaleidoscope.py"},
    }


# ---------------------------------------------------------------- bake once
build_site.SITE_CONFIG = dict(build_site.SITE_CONFIG)
build_site.SITE_CONFIG["pass"] = {"visualLayer": "pass", "diagnostics": "on"}

TMP = Path(tempfile.mkdtemp(prefix="synth_passkal_"))
build_site.OUT = TMP
build_site.build(SITE_URL)
LAYER = (TMP / "pass-layer.js").read_text(encoding="utf-8")
# THE INSTRUMENT'S OWN BUILT FILE — the real artifact a visitor is served, comments stripped. Since
# every instrument travels alone, the whole of this file is this instrument and nothing else.
PACK = (TMP / "pass-inst-kaleidoscope.js").read_text(encoding="utf-8")
REGION = PACK
SOURCE = ROOT / "engine" / "assets" / "pass-inst-kaleidoscope.js"
# The file as it stands in the tree, comments and all: the rows about what this instrument DECLARES
# read the built artifact, and the rows about what it SAYS read the source it is built from.
SOURCE_TEXT = SOURCE.read_text(encoding="utf-8")
LABTXT = MODULE.read_text(encoding="utf-8") if MODULE.exists() else ""

# ---------------------------------------------------------------- string rows

OWNED = ["createElement", "getContext", "requestAnimationFrame", "addEventListener",
         "performance.now", "Date.now", "new Image", "setTimeout", "setInterval"]
held = [s for s in OWNED if s in REGION]
check("PASS-KAL the instrument creates no element, no loop and no listener",
      not held,
      "§1.2's fence, read against the instrument's own built file: none of the nine ways of owning "
      "hardware appears there. The module raises its own canvas, takes a WebGL context on it, "
      "uploads two textures with their mip chains, runs its own frame loop, observes its own mount "
      "for a resize and binds the pointer; all of it stayed in the lab"
      if not held else "the instrument's region holds " + ", ".join(held))

HANDLES = ["mix", "clock", "centreX", "centreY", "wedges", "twist", "rings", "reach",
           "shade", "mask"]
absent = [h for h in HANDLES if ("%s: { min" % h) not in REGION]
check("PASS-KAL every handle the instrument publishes is a handle a score can drive",
      not absent and len(HANDLES) == 10,
      "§4.4b: ten handles. The dial, the second the host hands down, the two that place the fold's "
      "centre, the module's four declared parameters a pair can stand, the finish's own weight and "
      "the judges' channel"
      if not absent else "these are published nowhere: " + ", ".join(absent))

check("PASS-KAL no die is published, and the picture is what settles it",
      "seed: { min" not in REGION and "Math.random" not in REGION and "Math.random" not in LABTXT,
      "the module holds no die of its own and this instrument adds none, so a `seed` handle would "
      "be a handle a score could walk without moving the picture, which §4.4b calls noise in the "
      "score. A seeded run repeats to the pixel because there is nothing to seed")

check("PASS-KAL no turn handle is published, and the module's own reasoning is why",
      "turn: { min" not in REGION
      and "THE TRAVEL IS ONE SYMMETRY STEP" in LABTXT
      and "its two\n      // doors are the same frame pixel for pixel" in SOURCE_TEXT,
      "the module opened a `turn` handle and wrote in the same breath that its travel is exactly one "
      "symmetry step of the fold, so its two doors are the same frame pixel for pixel. The turn a "
      "passage needs is already in the picture — the closed-form `rotOf` rides the `clock` handle — "
      "and a second handle whose two ends coincide would name no measurement of any work")

# Every constant the picture stands on, read out of the lab module and out of the built file.
CONSTANTS = [
    ("const float TAU = 6.28318530718;", "const float TAU = 6.28318530718;",
     "the turn the wedges divide"),
    ("const float R0  = 1.25;", "const float R0  = 1.25;",
     "the radius that holds one whole radial repeat"),
    ("float seg = TAU / u_wedges;", "float seg = TAU / uFold.z;",
     "the wedge: one slice of the turn, and the fold's own period"),
    ("rr = sqrt(rr * rr + 0.0016);", "rr = sqrt(rr * rr + 0.0016);",
     "the soft floor at the centre: the fold never collapses to a point"),
    ("0.170 * Math.sin(t * 0.0617) + 0.080 * Math.sin(t * 0.1631 + 1.7)",
     "0.170 * Math.sin(t * 0.0617) + 0.080 * Math.sin(t * 0.1631 + 1.7)",
     "the sample point's own wander, across the picture"),
    ("0.145 * Math.sin(t * 0.0472) + 0.062 * Math.sin(t * 0.1187 + 2.4)",
     "0.145 * Math.sin(t * 0.0472) + 0.062 * Math.sin(t * 0.1187 + 2.4)",
     "and up it"),
    ("0.26 * Math.sin(t * 0.0431 + 1.1)", "0.26 * Math.sin(t * 0.0431 + 1.1)",
     "the sample width's own breath"),
    ("var ROT_RATE = 0.030, ROT_AMP = 0.014, ROT_W = 0.0271;",
     "var ROT_RATE = 0.030, ROT_AMP = 0.014, ROT_W = 0.0271;",
     "the turn's own rate, its swing and the period of that swing"),
    ("ROT_RATE * t + (ROT_AMP / ROT_W) * (1.0 - Math.cos(ROT_W * t))",
     "ROT_RATE * t + (ROT_AMP / ROT_W) * (1.0 - Math.cos(ROT_W * t))",
     "the turn in closed form, so a driven second reads the same turn whichever moment drew it"),
    ("mix(1.0, 1.24, u_fold)", "mix(1.0, 1.24, g)",
     "the finish's gamma, at the first power at a door"),
    ("vec3(0.299, 0.587, 0.114)", "vec3(0.299, 0.587, 0.114)",
     "the luminance the desaturate-and-boost mix is taken about"),
    ("mix(1.0, 1.12, u_fold)", "mix(1.0, 1.12, g)",
     "and the boost itself, at its own colour at a door"),
    ("mix(1.0, 0.34, smoothstep(0.40, 1.0, rn))", "mix(1.0, 0.34, smoothstep(0.40, 1.0, rn))",
     "the vignette that seats the figure on the dark page"),
    ("float rn = r / (0.5 * length(u_res) / m);", "float rn = r / (0.5 * length(uRes) / m);",
     "read so that 1.0 is the corner, at any shape of frame"),
    ("float t  = r / R0 * u_rings;", "float t  = r / R0 * uRing.x;",
     "the radial repeat: the wedge tiles outward into rings"),
]
missing_const = [p for lab_p, p in ((a, b) for a, b, _ in CONSTANTS)
                 if lab_p not in LABTXT or p not in REGION]
check("PASS-KAL every constant the picture stands on carries the module's own number",
      not missing_const and bool(LABTXT),
      "; ".join("%s — %s" % (p, why) for _, p, why in CONSTANTS) if not missing_const
      else "these differ between the lab module and the port: " + ", ".join(missing_const))

check("PASS-KAL the vista preset his taste approved is what the three parameters rest at",
      "var WEDGES_MIN = 3, WEDGES_MAX = 24, WEDGES_DEF = 8;" in REGION
      and "var TWIST_MIN = -1.2, TWIST_MAX = 1.2, TWIST_DEF = 0.55;" in REGION
      and "var RINGS_MIN = 1, RINGS_MAX = 2, RINGS_DEF = 1;" in REGION
      and "value: 8 }" in LABTXT and "value: 0.55 }" in LABTXT,
      "«kaleidoscope 8/.55/repeats 1» — the vista preset the charter records against his word of "
      "2026-08-08 11:39, and the module's own declared defaults besides")

check("PASS-KAL his ceiling on the radial repeat is applied, and it is named as his",
      "var RINGS_MIN = 1, RINGS_MAX = 2, RINGS_DEF = 1;" in REGION
      and "max: 5, step: 0.05" in LABTXT
      and "rings>2 washes to milk" in SOURCE_TEXT
      and "ceiling: RINGS_MAX" in REGION,
      "the module publishes its radial repeat up to 5; his standing verdict in the charter's "
      "vocabulary table is «rings>2 washes to milk», so this instrument publishes it up to 2 and the "
      "manifest says whose number that is")

check("PASS-KAL the crease's retouch is his В9 word, answered in points of the drawing buffer",
      "var SOFT_POINTS = 1.5;" in REGION
      and "SOFT_POINTS" not in LABTXT
      and "return a >= e ? a : (x * x + e * e) / (2.0 * max(e, 1e-9));" in REGION
      and "wedge seams need retouch" in SOURCE_TEXT
      and "uSoft.x / max(r, 1e-4)" in REGION,
      "the fold is continuous across a wedge edge and the module says so rightly; what it is not is "
      "SMOOTH, and the sign flip in its own derivative turns the photograph's texture along a hard "
      "line the eye reads as a crease. `softAbs` rounds that corner over a width read in POINTS of "
      "the drawing buffer — divided by the radius, so the width on the frame is the same at every "
      "radius — and past the softening it is the absolute value to the last bit")

check("PASS-KAL the mirror the host does not bind is done here, in arithmetic",
      "vec2 mirrorInto(vec2 uv){ return 1.0 - abs(mod(uv, 2.0) - 1.0); }" in REGION
      and "gl.CLAMP_TO_EDGE" in LAYER
      and "MIRRORED_REPEAT" in LABTXT and "MIRRORED_REPEAT" not in REGION,
      "the module binds its own textures MIRRORED_REPEAT and the wedge leans on it: the sample point "
      "wanders well outside the picture and the hardware mirrors it back in. This host binds "
      "CLAMP_TO_EDGE, under which the same point would smear the picture's outermost row of texels "
      "across the whole outer ring. So the wrap is done here, by the arithmetic the wrap mode "
      "performs, and the sampler is never asked for a point outside the picture at all")

# THE CHAIN IS HALF CLOSED SINCE THE PORT WAS WRITTEN. The row held that the host builds no chain
# and that the fact is written down rather than lost. The host now BUILDS one and hands it to any
# instrument declaring `gl.readsChain`, which this manifest does, so the row holds what stands: the
# host's chain, the instrument's declaration, and the module's own explicit level choice still not
# carried — because choosing a level is the module's arithmetic and the walking filter is the
# host's answer to the same aliasing.
check("PASS-KAL the mip chain is asked for by name, and the module's own level choice is not "
      "quietly carried",
      "THE MIP CHAIN" in SOURCE_TEXT
      and "textureGrad" in LABTXT and "textureGrad" not in REGION
      and "generateMipmap" in LABTXT and "generateMipmap" in LAYER
      and "readsChain: true" in REGION and "gl.readsChain" in LAYER,
      "the module builds a mip chain and asks for anisotropy, and its whole gradient estimate exists "
      "to pick a level that does not jump at a fold line. That estimate is not carried — an "
      "instrument may not upload a texture and the level choice is the module's own arithmetic — but "
      "what the missing chain cost, aliasing in the outer rings at a deep sample width, is answered: "
      "the host builds the chain and this manifest asks for it by name")

check("PASS-KAL the host binds uniforms by declared name, never by position or a written list",
      "getUniformLocation(p, u.name)" in LAYER and "uFold" not in LAYER and "uSoft" not in LAYER,
      "this instrument declares eleven uniforms, of which five are shared with the woven one. The "
      "host reads the manifest")

declared = set(re.findall(r'\{ name: "(u\w+)", type:', REGION))
spelled = set(re.findall(r'uniform \w+ (u\w+);', REGION))
check("PASS-KAL the manifest's declared names and the shader's own names are one set",
      declared == spelled and len(declared) == 11,
      f"{len(declared)} declared, {len(spelled)} spelled; "
      f"declared only: {sorted(declared - spelled)}; spelled only: {sorted(spelled - declared)}")

SUPPLY = ["textureA", "textureB", "fitA", "fitB", "resolution", "seconds"]
sources = set(re.findall(r'source: "([^"]+)"', REGION))
outside = [s for s in sources
           if s not in SUPPLY and not s.startswith("frame:") and not s.startswith("handle:")]
check("PASS-KAL every uniform is sourced from the closed set the host can supply",
      not outside and len(sources) >= 10,
      "§7's uniform sources are the two source textures, their fits, the resolution, the "
      "transaction's seconds, a value the instrument answers and a handle. This instrument names "
      f"{len(sources)} distinct sources and none outside that set"
      if not outside else "outside the set: " + ", ".join(outside))

check("PASS-KAL the shader carries no version header of its own",
      "#version" not in REGION and "#version 300 es" in LABTXT,
      "the module ships GLSL ES 3.00 with its own header; this instrument is written the way every "
      "other in this tree is, so the host's own translator stamps the one header it needs and no "
      "second one arrives")

check("PASS-KAL the manifest leaves the drawing buffer unpreserved",
      "gl: { preserveDrawingBuffer: false, readsChain: true }" in REGION,
      "§7 refuses a manifest that asks for the buffer to be preserved; this instrument draws every "
      "frame the host hands it")

check("PASS-KAL the coverage is declared, and it costs the picture nothing",
      "coverage: { writes: false" in REGION
      and "gl_FragColor = vec4(col, 1.0);" in REGION
      and 'framings: { "0": { coverCrop: 1 }, "1": { coverCrop: 1 } }' in REGION
      and "opacity" not in REGION and "presence" not in REGION,
      "§8's coverage block and §7's law: the alpha is the constant 1, said as a decision, because "
      "every point of the frame reads one point of one photograph at every value of the dial. Under "
      "the placement rule that makes this instrument lawful as the LOWEST cue of a stack — and "
      "unlike every other ground in this collection it takes no bite out of the work to be so: both "
      "doors publish a cover crop of 1, which is what lab/data/module-contract.json already records "
      "for this module. No handle of opacity and no weight of presence stands anywhere in it")

check("PASS-KAL the instrument declares what it cuts on, and it is the ring",
      'cuts: ["ring"]' in REGION and "NOT `wedge`" in SOURCE_TEXT,
      "the wedge tiles outward into mirrored RINGS about the work's own measured centre, and the "
      "ring is the element the composer's `radial` measure cuts on. The wedge kind is not claimed: "
      "the composer's wedge is the pivot of a shared rotational order drawn from a work's own "
      "measured wedge set, and the wedges this instrument makes are the fold's own symmetry rather "
      "than an element set a pair could be cast from")

# WHAT A PAIR MUST READ IS NOW WHAT A PAIR DOES READ. An `asks` block stood here naming two floors
# and a direction — both works over the collection's cut-line floor, the ARRIVING work over the
# tight floor with its subtype on rings. All three faults are his own words: a measurement ranks and
# never decides whether a pair qualifies (2026-08-18 09:51, 09:53), the collection's floors were
# struck from the composer the same morning so both names pointed at nothing, and a reading of a
# PAIR carries no direction, so a condition on the arriving work alone would have cast an edge one
# way and refused it the other. Every reading survives as the ranking it was: the row holds the
# floors OUT of the file and holds the `suits` block in.
SUITS_BLOCK = (re.search(r"suits:.*?levels:", REGION, re.S) or [""])[0]
check("PASS-KAL the instrument declares what it READS of a pair, and no floor and no direction",
      '"structure.radial.score"' in REGION and '"structure.radial.subType"' in REGION
      and 'floor: "radial"' not in REGION and 'floor: "radial_tight"' not in REGION
      and "asks:" not in REGION
      and "the weaker of the two readings " in SUITS_BLOCK
      and "arriving" not in SUITS_BLOCK and "departing" not in SUITS_BLOCK
      and bool(SUITS_BLOCK) and not re.search(r"\d\.\d", SUITS_BLOCK),
      "the wedge tiles outward into mirrored rings about the work's own centre, so it suits a pair "
      "BOTH of whose works read radial — the weaker of the two readings is the fit, because a fold "
      "opening a structure only one work carries is laid on rather than found — and it suits it more "
      "where the pair's own subtype is rings, since rings are what open into a rosette and spokes "
      "turn instead. No number is copied here: the arithmetic lives in the composer's own "
      "`INSTRUMENT_SUITS`, which is the one place holding both work records")

# THE FOLD'S CENTRE, AND THE MEASUREMENT IT READS. His 19:13 word, lifted to the class at 19:21:
# every geometric parameter names the measurement of the work it reads.
check("PASS-KAL every geometric handle publishes the measurement it reads",
      'reads: "structure.radial.centre' in REGION
      and "structure.polar.twirl" in REGION
      and "structure.ownDevice.count" in REGION
      and "structure.ownDevice.stepPx" in REGION
      and "the work's own measured rotational order" in REGION,
      "the fold's CENTRE reads structure.radial.centre, the point the works turn about; its LEAN "
      "reads structure.polar.twirl, how strongly the work's own making reads as a twirl; its RADIAL "
      "REPEAT reads structure.ownDevice.count, the repeats the work itself carries; its SAMPLE WIDTH "
      "reads structure.ownDevice.stepPx over the work's own frame side; and its WEDGE COUNT reads "
      "the work's own measured rotational order")

check("PASS-KAL the one measurement this collection does not carry is named as a gap, not filled",
      "CARRIES NONE the fold stands at 8" in REGION
      and "a gap in the record rather than a number this file invented" in REGION,
      "a rotational order is recorded for a work that carries one and 3 of the collection's 121 do, "
      "so the wedge count usually has no measurement to read. The fold then stands at 8 — the vista "
      "preset his taste approved and the module's own default — and the manifest says so out loud "
      "rather than passing a made-up number off as the work's own")

check("PASS-KAL the instrument measures no work for itself",
      "getImageData" not in REGION and "readPixels" not in REGION
      and "an instrument loads no\n    // file" in SOURCE_TEXT,
      "§1.2's fence leaves every surface to the host, so every number about a work arrives as a "
      "handle. The one fact this instrument does recover for itself — each file's own aspect — is "
      "recovered from the SEATING the host binds and not from the file, and the file says how")

# THE DOOR READING, AND ITS OWN NUMBERS.
check("PASS-KAL the judges' handle publishes what the door is read against, and that nothing is held",
      'readAtADoor: { points: DOOR_SLIP, readOn: "the drawing buffer",' in SOURCE_TEXT
      and 'reads: "the sample point"' in SOURCE_TEXT
      and "var DOOR_SLIP = 0.5;" in SOURCE_TEXT
      and "var DOOR_SHOW = 0.5 / 255;" in SOURCE_TEXT
      and "held: null" in SOURCE_TEXT
      and "AND THERE IS NOTHING HERE TO HOLD" in SOURCE_TEXT,
      "the handle carries `applied.readAtADoor` — what is walked, on which grid, what the reading is "
      "counted in — and it says outright that there is no hold. The fold at a door is `sin(pi * 0)`, "
      "which is nothing exactly and not nearly, so anything the reading finds is a real fault that "
      "no widening closes and the refusal stands alone")

CONTRACT = LAB / "data" / "module-contract.json"
CONTRACT_ROW = (json.loads(CONTRACT.read_text(encoding="utf-8"))["modules"].get("kaleidoscope")
                if CONTRACT.exists() else None)
check("PASS-KAL the crossing's own shape is named as the port's, and the exchange's width is derived",
      "var SWAP_UNDER = 0.9;" in REGION
      and "var SWAP_HALF = 0.5 - Math.asin(SWAP_UNDER) / Math.PI;" in REGION
      and bool(CONTRACT_ROW) and CONTRACT_ROW["dial"]["polarity"] == "one-sided"
      and CONTRACT_ROW["dial"]["framing"]["coverCrop"] == 1.0
      and CONTRACT_ROW["level"] == "CELL",
      "lab/data/module-contract.json records this module's dial as ONE-SIDED, resting at the fold "
      "with the flat photograph as its only door: it opens and stays there. A passage of this engine "
      "has two doors with a photograph standing whole at each, so the fold has to open and close "
      "inside one hand — one sine over the whole passage, which is charter shelf 5's mystery middle "
      "read straight. The exchange runs exactly across the stretch where that fold stands over nine "
      "tenths of its whole, which is shelf 5's CONJUROR, and its half-width is arithmetic off the "
      "window rather than a number anybody chose")

sha = hashlib.sha256(MODULE.read_bytes()).hexdigest() if MODULE.exists() else ""
declared_sha = (re.search(r'sha256: "([0-9a-f]{64})"', REGION) or [None, None])[1]
check("PASS-KAL the provenance names the file the port was read from, and the file weighs to it",
      bool(sha) and sha == declared_sha and 'commit: "4c7dfe4"' in REGION,
      f"the module is tracked, so the commit it was read at is named beside the digest of its bytes, "
      f"and the file still weighs to {sha[:16]}…")

# ---------------------------------------------------------------- browser rows

BROWSER_ROWS = [
    "PASS-KAL §8     · the manifest carries every field the contract names, in its shape",
    "PASS-KAL §8     · it publishes SURFACE and CELL, and the reading is said to be derived",
    "PASS-KAL row 7  · door 0 stands the departing work, measured against its own file",
    "PASS-KAL row 7  · door 0 carries no trace of the arriving work",
    "PASS-KAL row 7  · door 1 stands the arriving work, measured against its own file",
    "PASS-KAL row 7  · door 1 carries no trace of the departing work",
    "PASS-KAL the two roads agree at the door and at four depths of the fold",
    "PASS-KAL §7     · no walked point reads outside the work at any sampled pose",
    "PASS-KAL §7     · the ground of a stack, and refused above another cue",
    "PASS-KAL §7     · both doors stand whole with a coverage-writing voice over them",
    "PASS-KAL §7     · no empty frame at any sampled instant of the pass",
    "PASS-KAL §7     · the frame after a change of viewport is drawn afresh",
    "PASS-KAL row 10 · a driven run repeats to the pixel",
    "PASS-KAL row 14 · textures, programmes and framebuffers return to their baseline after ten runs",
    "PASS-KAL row 15 · the console stays clean",
    "PASS-KAL row 22 · the census shows granted against declared, and neither overruns",
    "PASS-KAL §7     · one canvas, one context, two source textures, one pass a frame",
    "PASS-KAL the real transaction road: curtain up, one pass drawn, exactly one dock at the end",
    "PASS-KAL row 9  · one camera authority through a real pass, and the pose rests on the arrival",
    "PASS-KAL §4.4b  · the wedges, the lean, the repeats, the centre and the second reach the PICTURE",
    "PASS-KAL the exchange stands under the deepest fold, and nowhere near a door",
    "PASS-KAL the sample point is WALKED on the drawing buffer at both doors, and what it read is published",
    "PASS-KAL a door the judges' channel spoils is refused on the real road, and the visitor still lands",
    "PASS-KAL his В9 word · the fold's own creases are retouched, and the retouch is measured across them",
    "PASS-KAL row 16 · the captures are kept as evidence",
]

RED_ROWS = [
    "PASS-KAL red-on-bug · the mirror removed: the picture's own edge smears across the outer rings",
    "PASS-KAL red-on-bug · the crease's retouch removed: the fold's own edges stand hard again",
    "PASS-KAL red-on-bug · his ceiling on the repeats removed: a score reaches past what he allowed",
    "PASS-KAL red-on-bug · the finish's gating on the fold removed: the door stops being its own file",
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


def smeared(p, q):
    """The SHARE of the frame's own points standing further apart than the project's seam. What a
    wrap costs is a region — inside the picture the two frames are identical and outside it they are
    unrelated — so a mean over the whole frame is the wrong reading of it."""
    from PIL import Image, ImageChops
    d = ImageChops.difference(Image.open(p).convert("RGB"), Image.open(q).convert("RGB"))
    h = d.convert("L").histogram()
    return sum(h[int(SEAM) + 1:]) / float(sum(h))


def paleness(p):
    """How far the frame has washed to milk: its own spread, averaged over the three channels. A
    rosette that has averaged the photograph away has almost none."""
    from PIL import Image, ImageStat
    st = ImageStat.Stat(Image.open(p).convert("RGB"))
    return sum(st.stddev) / 3.0


def cover_into(im, w, h, crop=1.0):
    from PIL import Image
    iw, ih = im.size
    fa, ia = w / float(h), iw / float(ih)
    sw, sh = (ih * fa, float(ih)) if ia > fa else (float(iw), iw / fa)
    sw /= crop
    sh /= crop
    x0, y0 = (iw - sw) / 2.0, (ih - sh) / 2.0
    return im.resize((w, h), Image.BILINEAR, box=(x0, y0, x0 + sw, y0 + sh))


def work_in_the_frame(src, w, h, crop=CROP):
    """The whole file, cover-fitted into the frame. Both doors of this instrument are the plain cover
    fit, which is what its `framings` block publishes."""
    from PIL import Image
    return cover_into(Image.open(src).convert("RGB"), w, h, crop)


def apart(p, work):
    from PIL import Image, ImageChops, ImageStat
    a = Image.open(p).convert("RGB")
    if a.size != work.size:
        return 255.0, 255.0
    st = ImageStat.Stat(ImageChops.difference(a, work))
    return sum(st.mean) / 3.0, max(m for _, m in st.extrema)


def _lum_at(px, W, H, x, y):
    """One point of the frame, read between its samples, so a reading a couple of points wide is not
    quantised into the grid it is walking."""
    x = min(max(x, 0.0), W - 1.001)
    y = min(max(y, 0.0), H - 1.001)
    x0, y0 = int(x), int(y)
    fx, fy = x - x0, y - y0
    out = 0.0
    for dx, dy, wgt in ((0, 0, (1 - fx) * (1 - fy)), (1, 0, fx * (1 - fy)),
                        (0, 1, (1 - fx) * fy), (1, 1, fx * fy)):
        c = px[x0 + dx, y0 + dy]
        out += wgt * (0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2])
    return out


def crease_hardness(path, wedges=8, reach_px=1.0, r0=0.12, r1=0.45, step=1.0):
    """THE KINK AT THE FOLD'S OWN EDGE, read ACROSS it, with the picture's own roughness beside it.

    The rosette is centred on the frame's own centre, so with the lean at nothing and the turn at
    nothing the fold's edges are rays at every half-wedge of angle. At many radii along each of them
    the luminance is read at the crease and at two points the same short distance to either side
    ALONG THE ARC, and the second difference of those three is the kink a hard fold leaves. The same
    three-point reading is taken at the MIDDLE of each wedge, where no crease stands, because the
    crease's own kink means nothing without the picture's own roughness to read it against.

    Returns (the kink at the creases, the same reading away from them)."""
    from PIL import Image
    im = Image.open(path).convert("RGB")
    W, H = im.size
    px = im.load()
    m = min(W, H)
    seg = 2 * math.pi / wedges
    on, off = [], []
    r = r0 * m
    while r <= r1 * m:
        da = reach_px / r
        for k in range(2 * wedges):
            for angle, bucket in ((k * seg / 2.0, on), (k * seg / 2.0 + seg / 4.0, off)):
                three = []
                for j in (-1, 0, 1):
                    a = angle + j * da
                    x = W / 2.0 + r * math.cos(a)
                    y = H / 2.0 - r * math.sin(a)
                    if not (0 <= x < W - 1 and 0 <= y < H - 1):
                        three = []
                        break
                    three.append(_lum_at(px, W, H, x, y))
                if len(three) == 3:
                    bucket.append(abs(three[0] + three[2] - 2 * three[1]))
        r += step
    return (sum(on) / max(len(on), 1), sum(off) / max(len(off), 1))


# THE LAB MODULE AS THE BENCH SERVES IT. Four literals are changed and nothing else. Two of them are
# THIS HOST'S OWN BINDING rather than a choice of this suite's — the host builds no mip chain and
# asks for no anisotropy (pass-layer.js's own `makeTex`), so a module sampling through a chain the
# host never builds would be compared as a different SAMPLER rather than as a different reading of
# one geometry. Two of them are the module's own two anchor numbers, chosen by eye for its own two
# photographs, pinned to the centre this port reads from the work. The file on disk is never touched.
LAB_EDITS = [
    ("        gl.generateMipmap(gl.TEXTURE_2D);\n", ""),
    ("gl.LINEAR_MIPMAP_LINEAR", "gl.LINEAR"),
    ("Math.min(8, max)", "1"),
    ("function homeX() { return 0.47 - 0.12 * mixNow; }",
     "function homeX() { return %s; }" % CENTRE[0]),
    ("function homeY() { return 0.64 - 0.28 * mixNow; }",
     "function homeY() { return %s; }" % (1 - CENTRE[1])),
]


def lab_served():
    t = LABTXT
    for a, b in LAB_EDITS:
        t = t.replace(a, b, 1)
    return t


def bench_dir(pack_text=None):
    """The bench's own served root: the BUILT pass-layer.js, the site's own settings record and the
    BUILT instrument files it names — the real artifacts, namespace applied and comments stripped —
    the lab module as described above, the two photographs, and the page that stands the two roads of
    one frame side by side.

    A row proving a rule reds hands over a CHANGED instrument file and writes the record with the
    digest of the bytes actually served, which is what the build does. The source file on disk is
    never touched, so nothing has to be restored and no working tree can be left changed by a
    red-on-bug proof."""
    d = Path(tempfile.mkdtemp(prefix="synth_kalbench_"))
    pack = PACK if pack_text is None else pack_text
    shutil.copy2(TMP / "pass-layer.js", d / "pass-layer.js")
    for _inst in sorted(TMP.glob("pass-inst-*.js")):
        shutil.copy2(_inst, d / _inst.name)
    (d / "pass-inst-kaleidoscope.js").write_text(pack, encoding="utf-8")
    record = json.loads((TMP / "config.json").read_text(encoding="utf-8"))
    record["pass"]["instruments"]["kaleidoscope"]["digest"] = hashlib.sha256(
        pack.encode("utf-8")).hexdigest()
    (d / "config.json").write_text(json.dumps(record), encoding="utf-8")
    (d / "kaleidoscope.js").write_text(lab_served(), encoding="utf-8")
    (d / "photos").mkdir()
    for p in PHOTOS:
        shutil.copy2(p, d / "photos" / p.name)
    shutil.copy2(ROOT / "tests" / "fixture_pass_kaleidoscope.html", d / "index.html")
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
    """BOTH ROADS AT ONE POSE. The hand is the raw dial on the port's side; the module is handed the
    fold that hand stands at, which is the one number the two roads have to share."""
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


def host_shot(br, at, tag, **params):
    for k, v in params.items():
        br.evaluate("window.__param(%s, %r); 0" % (json.dumps(k), v))
    js(br, "return window.__both(%r);" % at)
    br.sleep(0.3)
    br.evaluate("window.__mask(0); window.__hostDraw(); window.__show('host'); 0")
    br.sleep(0.3)
    return png(br, SHOTS / (tag + ".png"))


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
                    check(r, False, "the bench never came up: "
                         + br.evaluate("JSON.stringify(window.__errs||[])"))
            elif not js(br, "return !!window.__exPass.bench.manifest('kaleidoscope');"):
                why = js(br, "var e = window.__host.report().events.filter(function(x){"
                             "return x.name === 'manifest-refused';});"
                             "return e.length ? e[e.length - 1].why : null;")
                for r in BROWSER_ROWS:
                    check(r, False, "the host registered no «kaleidoscope» instrument: " + str(why))
            else:
                SCORE = json.dumps(kal_score())
                SCORE_UNDER = json.dumps(kal_score(under=True))

                # ---- §8: the manifest, read off the registered instrument -----------------------
                m = js(br, "return window.__exPass.bench.manifest('kaleidoscope');")
                res = m["resources"]
                need = ["id", "api", "arity", "roles", "cuts", "suits", "params", "handles",
                        "neutrals", "doors", "framings", "drivers", "camera", "gl", "passes",
                        "resources", "capabilities", "decline", "provenance", "readiness",
                        "coverage", "levels"]
                shape = (
                    all(k in m for k in need)
                    and m["id"] == "kaleidoscope" and m["api"] == 1 and m["arity"] == 2
                    and m["roles"] == ["disassembly", "mystery", "assembly"]
                    and m["cuts"] == ["ring"]
                    and sorted(m["params"]) == ["reach", "rings", "twist", "wedges"]
                    and len(m["handles"]) == 10
                    and all(set(h) >= {"min", "max", "def"} for h in m["handles"].values())
                    and m["handles"]["rings"]["max"] == 2
                    and m["neutrals"] == {"a": 0, "b": 1}
                    and m["doors"]["in"]["handle"] == "mix" and m["doors"]["in"]["value"] == 0
                    and m["doors"]["out"]["handle"] == "mix" and m["doors"]["out"]["value"] == 1
                    and sorted(m["framings"]) == ["0", "1"]
                    and m["framings"]["0"] == {"coverCrop": 1} == m["framings"]["1"]
                    and m["camera"] == {"needs": "none", "authority": "stage"}
                    and m["gl"] == {"preserveDrawingBuffer": False, "readsChain": True}
                    and len(m["passes"]) == 1 and len(m["passes"][0]["uniforms"]) == 11
                    and sorted(res) == ["lean", "rich", "standard"]
                    and all("bytesEstimate" in res[v] and res[v]["programs"] == 1
                            and res[v]["passes"] == 1 and res[v]["textureSlots"] == 2
                            for v in res)
                    and m["capabilities"] == ["webgl2"] and m["decline"]
                    and m["coverage"]["writes"] is False and m["coverage"]["how"]
                    and m["provenance"]["labPath"] == "lab/effects/kaleidoscope.js"
                    and m["provenance"]["commit"] == "4c7dfe4"
                    and m["readiness"] == "production-ready"
                    and "kaleidoscope" in js(br, "return window.__host.report().registered;"))
                check(BROWSER_ROWS[0], shape,
                      f"ten handles, eleven uniforms in one pass, cuts on {m.get('cuts')}, both "
                      f"doors at a cover crop of {m['framings']['0']['coverCrop']} — nothing is "
                      f"trimmed to buy the coverage — resources declared for three tiers, and a "
                      f"coverage block reading «{m['coverage']['how']}»")

                check(BROWSER_ROWS[1],
                      m["levels"] == ["SURFACE", "CELL"]
                      and "WHERE THIS STANDS ON THE CHARTER'S SHELF" in SOURCE_TEXT
                      and "NO WORLD IS CLAIMED" in SOURCE_TEXT,
                      f"levels={m['levels']}, and the two records answer differently so both are "
                      f"carried: SURFACE is his own standing verdict in the charter's vocabulary "
                      f"table — the whole frame's coordinate is remapped at once — and CELL is "
                      f"lab/data/module-contract.json's own row for this module, the wedge being a "
                      f"cell. NO WORLD is claimed, and it is a decision with a consequence: this "
                      f"instrument spends no miracle, so a quiet link, an entrance and a return can "
                      f"still be carried by it, which is what keeps the ring cut answered at every "
                      f"role rather than at two")

                w = int(br.evaluate("String(window.__exPass.bench.make() && "
                                    "document.querySelector('canvas[aria-hidden]').width)"))
                h = int(br.evaluate("String(document.querySelector('canvas[aria-hidden]').height)"))
                bufs = js(br, "return window.__buffers();")
                drum = work_in_the_frame(BENCH / "photos" / "glass-drum.jpg", w, h)
                tower = work_in_the_frame(BENCH / "photos" / "round-tower.jpg", w, h)

                # ---- the poses, on both roads ---------------------------------------------------
                br.evaluate("window.__centre(%r, %r); window.__clock(0); 0" % CENTRE)
                DOORS = [("door-0", 0.0), ("door-1", 1.0)]
                # the rising side of the hand, where the exchange has not begun: there work A alone
                # stands and the module's own single aspect correction is the pair's, so the two
                # roads are comparable pose for pose
                FOLD = [("f1", 0.08), ("f2", 0.16), ("f3", 0.24), ("f4", 0.32)]
                shots, reads = {}, {}
                for tag, at in DOORS + FOLD:
                    reads[tag], hp, mp = roads(br, at, tag)
                    shots[tag] = (hp, mp)

                for i, (door, own, other, ownn, othern) in enumerate((
                        ("door-0", drum, tower, "glass-drum.jpg", "round-tower.jpg"),
                        ("door-1", tower, drum, "round-tower.jpg", "glass-drum.jpg"))):
                    a, amx = apart(shots[door][0], own)
                    check(BROWSER_ROWS[2 + i * 2], a <= SEAM,
                          f"{door} against {ownn} at the plain cover fit: mean {a:.4f} of 255 "
                          f"(threshold {SEAM}), worst channel {amx}. The fold is one sine over the "
                          f"whole hand and it is at its own zero at both ends, so the sample "
                          f"coordinate is the plain cover fit and every term of the finish — the "
                          f"gamma, the boost and the vignette — stands at its own identity")
                    b, _ = apart(shots[door][0], other)
                    check(BROWSER_ROWS[3 + i * 2], b >= FAR,
                          f"{door} against {othern}: mean {b:.4f} of 255, which has to be far "
                          f"(threshold {FAR}); the exchange stands under the deepest fold and is "
                          f"nothing at one door and whole at the other")

                # ---- the two roads --------------------------------------------------------------
                worst, worst_at, worst_max = 0.0, None, 0.0
                for tag, _ in [("door-0", 0)] + FOLD:
                    d, dmx = diff(shots[tag][0], shots[tag][1])
                    if d > worst:
                        worst, worst_at, worst_max = d, tag, dmx
                check(BROWSER_ROWS[6], worst <= ROADS,
                      f"worst of the five poses is {worst:.4f} of 255 at {worst_at} (threshold "
                      f"{ROADS}), worst channel {worst_max}. The two roads run one fragment shader "
                      f"over one rasteriser, so what stands between them is the arithmetic and the "
                      f"crease's own retouch — a band a point and a half wide along each fold line. "
                      f"Buffers: host {bufs['host']}, module {bufs['module']}")

                # ---- the coverage: no walked point reads outside the work -------------------------
                bare_seen = []
                for tag, at in DOORS + FOLD + [("mid", 0.5), ("late", 0.75)]:
                    v = js(br, "return window.__both(%r);" % at)
                    sm = v.get("sampleMap")
                    if sm is not None:
                        bare_seen.append((tag, sm["bare"], sm["walked"]))
                check(BROWSER_ROWS[7], all(b == 0 for _, b, _ in bare_seen) and bare_seen,
                      "the instrument's own reading walks its sample point at the buffer's own "
                      "sample points and no walked point reads outside the work at any door: "
                      + "; ".join(f"{t} {b} of {n} outside" for t, b, n in bare_seen))

                # ---- the placement law -----------------------------------------------------------
                ground = js(br, "return window.__exPass.bench.coverageWhyNo(%s);"
                            % json.dumps([kal_cue(stack=0)]))
                over = js(br, "return window.__exPass.bench.coverageWhyNo(%s);"
                          % json.dumps([matter_cue(stack=0), kal_cue(stack=1)]))
                under = js(br, "return window.__exPass.bench.coverageWhyNo(%s);"
                           % json.dumps([kal_cue(stack=0), matter_cue(stack=1)]))
                check(BROWSER_ROWS[8], ground is None and under is None and bool(over),
                      f"a one-cue score and the ground of a stack are lawful; laid over a cue that "
                      f"writes coverage the host refuses with «{over}». That placement is what "
                      f"declaring `coverage.writes: false` buys, and it is the whole reason a ring "
                      f"cut wanted this instrument")

                # ---- both doors under a coverage-writing voice ------------------------------------
                took = js(br, "return window.__offer(%s, {progress: 0});" % SCORE_UNDER)
                br.sleep(0.8)
                br.evaluate("window.__show('host'); 0")
                br.sleep(0.3)
                p0 = png(br, SHOTS / "under-door-0.png")
                js(br, "window.__host.configure({progressPin: 1}); return 1;")
                br.sleep(0.8)
                p1 = png(br, SHOTS / "under-door-1.png")
                a0, _ = apart(p0, drum)
                a1, _ = apart(p1, tower)
                js(br, "window.__cancel('bench'); return 1;")
                idle(br)
                check(BROWSER_ROWS[9], took["took"] and a0 <= FAR and a1 <= FAR,
                      f"with the material instrument playing above it, door 0 stands {a0:.2f} of 255 "
                      f"from glass-drum.jpg and door 1 {a1:.2f} from round-tower.jpg. The voice "
                      f"above writes its own coverage, so the frame is this instrument's picture "
                      f"where that voice carries nothing")

                # ---- no empty frame --------------------------------------------------------------
                empties = []
                for i, at in enumerate([0.0, 0.12, 0.25, 0.4, 0.5, 0.7, 1.0]):
                    p = host_shot(br, at, "live-%d" % i)
                    mean, spread = standing(p)
                    if mean <= 1.0 or spread < SPREAD:
                        empties.append((at, round(mean, 2), round(spread, 2)))
                check(BROWSER_ROWS[10], not empties,
                      "seven instants of the pass, each standing as a picture rather than as the "
                      "cleared buffer" if not empties else "these stood empty: " + str(empties))

                # ---- a change of viewport ---------------------------------------------------------
                before = host_shot(br, 0.5, "resize-before")
                br._cmd("Emulation.setDeviceMetricsOverride", width=844, height=390,
                        deviceScaleFactor=1, mobile=False)
                br.sleep(0.3)
                js(br, "window.__resize(); return 1;")
                br.sleep(0.4)
                after = host_shot(br, 0.5, "resize-after")
                from PIL import Image as _Im
                sz = _Im.open(after).size
                mean_a, spread_a = standing(after)
                br._cmd("Emulation.clearDeviceMetricsOverride")
                br.sleep(0.3)
                js(br, "window.__resize(); return 1;")
                br.sleep(0.4)
                check(BROWSER_ROWS[11], sz == (844, 390) and mean_a > 1.0 and spread_a >= SPREAD,
                      f"the frame is redrawn at {sz} and stands as a picture (mean {mean_a:.2f}, "
                      f"spread {spread_a:.2f}); the crease's own softening is read in points of the "
                      f"buffer, so it follows the grid rather than a number frozen at a bake")

                # ---- a driven run repeats ----------------------------------------------------------
                one = host_shot(br, 0.42, "repeat-a")
                br.evaluate("window.__clock(3.5); 0")
                br.sleep(0.2)
                host_shot(br, 0.42, "repeat-elsewhere")
                br.evaluate("window.__clock(0); 0")
                br.sleep(0.2)
                two = host_shot(br, 0.42, "repeat-b")
                dm, dx = diff(one, two)
                check(BROWSER_ROWS[12], dm == 0.0 and dx == 0.0,
                      f"the same hand and the same second, drawn twice with a walk elsewhere "
                      f"between: mean {dm}, worst channel {dx}. The module's own wander, breath and "
                      f"turn are pure functions of the second the host hands down, and nothing here "
                      f"rolls a die")

                # ---- the census --------------------------------------------------------------------
                base_census = js(br, "return window.__report().census;")
                for _ in range(10):
                    js(br, "return window.__offer(%s, {progress: 0.5});" % SCORE)
                    br.sleep(0.25)
                    js(br, "window.__cancel('bench'); return 1;")
                    idle(br)
                after_census = js(br, "return window.__report().census;")
                grew = {k: (base_census.get(k), after_census.get(k))
                        for k in ("textures", "framebuffers", "canvases")
                        if after_census.get(k) != base_census.get(k)}
                check(BROWSER_ROWS[13], not grew,
                      f"ten offers and ten cancels: census {after_census}"
                      if not grew else "these grew: " + str(grew))

                errs = js(br, "return window.__errs;")
                check(BROWSER_ROWS[14], not errs, "the console carried: " + str(errs))

                rep = js(br, "return window.__report();")
                check(BROWSER_ROWS[15],
                      isinstance(rep.get("census"), dict) and rep["census"]["canvases"] <= 1,
                      f"census {rep['census']}, granted {rep.get('grant')}")

                check(BROWSER_ROWS[16],
                      rep["census"]["canvases"] == 1 and rep["census"].get("textures", 0) <= 2
                      and rep["census"].get("framebuffers", 0) == 0,
                      f"one canvas, no framebuffer of this instrument's own and at most the two "
                      f"source textures the host holds: {rep['census']}")

                # ---- the real transaction road -------------------------------------------------
                js(br, "window.__hooks.docks = []; window.__hooks.curtains = []; "
                       "window.__hooks.glides = []; return 1;")
                took = js(br, "return window.__offer(%s);" % SCORE)
                br.sleep(0.4)
                mid = js(br, "return window.__report();")
                for _ in range(80):
                    if js(br, "return window.__hooks.docks.length;"):
                        break
                    br.sleep(0.15)
                hooks = js(br, "return window.__hooks;")
                idle(br)
                check(BROWSER_ROWS[17],
                      took["took"] and hooks["curtains"] and hooks["curtains"][0] is True
                      and hooks["docks"].count(took["gen"]) == 1 and not hooks["glides"],
                      f"took={took}, curtains={hooks['curtains']}, docks={hooks['docks']}, "
                      f"glides={hooks['glides']}; mid-pass state {mid.get('state')}")

                check(BROWSER_ROWS[18],
                      mid.get("cameraOwner", "stage") == "stage",
                      f"the instrument asks the host's camera for nothing (`camera.needs: none`), so "
                      f"the stage keeps the authority through the pass: {mid.get('cameraOwner')}")

                # ---- §4.4b: every handle reaches the picture ---------------------------------------
                br.evaluate("window.__clock(0); window.__centre(%r, %r); 0" % CENTRE)
                basep = host_shot(br, 0.5, "handle-base",
                                  wedges=8, twist=0.55, rings=1, reach=0.30)
                moves = {}
                for k, v, tag in (("wedges", 18, "handle-wedges"), ("twist", -0.9, "handle-twist"),
                                  ("rings", 2, "handle-rings"), ("reach", 0.14, "handle-reach")):
                    p = host_shot(br, 0.5, tag, **{k: v})
                    moves[k] = round(diff(basep, p)[0], 3)
                    host_shot(br, 0.5, "handle-back",
                              **{k: {"wedges": 8, "twist": 0.55, "rings": 1, "reach": 0.30}[k]})
                js(br, "window.__centre(0.30, 0.72); return 1;")
                pc = host_shot(br, 0.5, "handle-centre")
                moves["centre"] = round(diff(basep, pc)[0], 3)
                js(br, "window.__centre(%r, %r); return 1;" % CENTRE)
                br.evaluate("window.__clock(6.0); 0")
                pt = host_shot(br, 0.5, "handle-clock")
                moves["clock"] = round(diff(basep, pt)[0], 3)
                br.evaluate("window.__clock(0); 0")
                thin = [k for k, v in moves.items() if v < SEAM]
                check(BROWSER_ROWS[19], not thin,
                      f"each handle moves the frame by more than the project's own seam of {SEAM} of "
                      f"255: {moves}" if not thin
                      else f"these did not reach the picture: {thin} ({moves})")

                # ---- the exchange stands under the deepest fold -------------------------------------
                wets = js(br, "var o = {}; [0, 0.2, 0.3564, 0.5, 0.6436, 0.8, 1].forEach("
                              "function (u) { o[String(u)] = window.__wet(u); }); return o;")
                folds = js(br, "var o = {}; [0, 0.2, 0.3564, 0.5, 0.6436, 0.8, 1].forEach("
                               "function (u) { o[String(u)] = window.__fold(u); }); return o;")
                shut = wets["0"] == 0 and wets["1"] == 1 and wets["0.2"] == 0 and wets["0.8"] == 1
                deep = folds["0"] == 0 and folds["1"] == 0 and folds["0.5"] == 1
                check(BROWSER_ROWS[20], shut and deep,
                      f"the exchange stands at {wets} and the fold at {folds}: the two photographs "
                      f"exchange only across the stretch where the fold stands over nine tenths of "
                      f"its whole — charter shelf 5's conjuror, and its half-width is arithmetic off "
                      f"the window — while at either door the fold is nothing exactly and one work "
                      f"stands alone")

                # ---- the door, walked on the buffer --------------------------------------------------
                reads0 = js(br, "return window.__both(0);")
                reads1 = js(br, "return window.__both(1);")
                sm0, sm1 = reads0.get("sampleMap"), reads1.get("sampleMap")
                check(BROWSER_ROWS[21],
                      sm0 and sm1 and sm0["walked"] >= 17 and sm1["walked"] >= 17
                      and sm0["offPx"] < 0.5 and sm1["offPx"] < 0.5
                      and sm0["bare"] == 0 and sm1["bare"] == 0
                      and reads0["doorWhyNo"] is None and reads1["doorWhyNo"] is None
                      and reads0["doorHeld"] is None,
                      f"door 0 walked {sm0['walked']} points of the buffer and the furthest sample "
                      f"stands {sm0['offPx']:.6f} points from its flat place with {sm0['bare']} "
                      f"outside the work and {sm0['other']:.6f} of the other work in the frame; door "
                      f"1 {sm1['offPx']:.6f} points, {sm1['bare']} outside, {sm1['other']:.6f}. "
                      f"Nothing is held: the fold at a door is a sine at its own zero")

                # ---- a door the judges' channel spoils is refused --------------------------------
                js(br, "window.__hooks.docks = []; window.__hooks.glides = []; return 1;")
                spoilt = json.dumps(kal_score(mask=1))
                took = js(br, "return window.__offer(%s, {progress: 0});" % spoilt)
                br.sleep(0.8)
                repo = js(br, "return window.__report();")
                applied = None
                for v in (repo.get("stack") or []):
                    if v.get("applied"):
                        applied = v["applied"]
                why = repo.get("lastFailWhy") or repo.get("failWhy")
                if why is None:
                    for e in (repo.get("events") or []):
                        if e.get("name") in ("fail", "instrument-fail", "recover"):
                            why = e.get("why")
                js(br, "window.__cancel('bench'); return 1;")
                idle(br)
                check(BROWSER_ROWS[22],
                      bool(applied) and applied.get("whyNo")
                      and "judges" in str(applied.get("whyNo")),
                      f"the instrument reported what it applied before it refused, and the refusal "
                      f"reads «{(applied or {}).get('whyNo')}». The host recovers on that reason and "
                      f"the walk's own glide carries the visitor. Applied record: {applied}; "
                      f"host's own why: {why}")

                # ---- his В9 word: the creases, measured ACROSS them -------------------------------
                br.evaluate("window.__clock(0); window.__centre(%r, %r); 0" % CENTRE)
                creasep = host_shot(br, 0.5, "creases", wedges=8, twist=0, rings=1, reach=0.30)
                on_c, off_c = crease_hardness(creasep)
                host_shot(br, 0.5, "creases-back", twist=0.55)
                check(BROWSER_ROWS[23], on_c <= off_c * 1.20,
                      f"the frame is walked ACROSS each of the fold's sixteen own edges — at the "
                      f"angles the fold puts them at, the lean at nothing and the turn at nothing — "
                      f"and the kink there reads {on_c:.2f} of 255 against {off_c:.2f} at the middle "
                      f"of the wedges, where no crease stands. A retouched fold reads no harder than "
                      f"the picture's own roughness; the red-on-bug row below takes the retouch out "
                      f"and the same reading climbs")

                shot_count = len(list(SHOTS.glob("*.png")))
                check(BROWSER_ROWS[24], shot_count >= 20,
                      f"{shot_count} captures under {SHOTS.relative_to(ROOT)}")

    shutil.rmtree(BENCH, ignore_errors=True)

    # ---------------------------------------------------------------- red-on-bug
    # Every proof below runs a COPY of the instrument's built bytes with ONE rule reverted, served to
    # a real browser with the record's digest rewritten to the bytes actually served. The source file
    # on disk is never written to.

    # 1 · THE MIRROR REMOVED. The wrap this host binds is CLAMP_TO_EDGE, so without the arithmetic
    # mirror the sample point that wanders past the picture reads its outermost row of texels and the
    # outer rings become a smear of edge colour.
    NO_MIRROR = PACK.replace(
        "vec2 mirrorInto(vec2 uv){ return 1.0 - abs(mod(uv, 2.0) - 1.0); }",
        "vec2 mirrorInto(vec2 uv){ return uv; }", 1)

    # 2 · THE CREASE'S RETOUCH REMOVED — his В9 word reverted to the module's own hard fold.
    NO_SOFT = PACK.replace("var SOFT_POINTS = 1.5;", "var SOFT_POINTS = 0;", 1)

    # 3 · HIS CEILING ON THE RADIAL REPEAT REMOVED, back to the module's own 5.
    NO_CAP = PACK.replace("RINGS_MAX = 2", "RINGS_MAX = 5", 1)

    # 4 · THE FINISH'S GATING ON THE FOLD REMOVED: every term of the finish stands at full strength
    # whatever the fold is doing, so a door stops being the photograph its file carries.
    NO_GATE = PACK.replace("var finish = clamp(num(st.shade, 1), 0, 1) * fold;",
                           "var finish = clamp(num(st.shade, 1), 0, 1);", 1)

    planted = {"mirror": NO_MIRROR != PACK, "soft": NO_SOFT != PACK,
               "cap": NO_CAP != PACK, "gate": NO_GATE != PACK}
    if not all(planted.values()):
        for r in RED_ROWS:
            check(r, False, "a red-on-bug proof could not plant its change: " + str(planted))
    else:
        def shot_at(br, at, tag, **params):
            return host_shot(br, at, tag, **params)

        def one_pose(br, at, tag, centre=CENTRE, **params):
            br.evaluate("window.__clock(0); window.__centre(%r, %r); 0" % centre)
            return shot_at(br, at, tag, **params)

        # WHERE THE WEDGE REALLY LEAVES THE PICTURE. A rosette read from the middle of a work barely
        # asks the wrap for anything: the sample point runs a twentieth of the picture past its edge
        # at the corners and no further. A pair of works whose measured radial centre sits off the
        # middle — [0.35, 0.35] is what the collection's own record carries for the first work of the
        # gallery — reads a third of the picture's width outside it, and that is the pose the mirror
        # is there for. So the mirror's proof stands at a MEASURED centre rather than at the middle.
        OFF_CENTRE = (0.30, 0.35)

        # the shipped readings the four proofs are measured against
        def shipped(br):
            out = {}
            out["deep"] = one_pose(br, 0.5, "red-base-deep", centre=OFF_CENTRE, wedges=8,
                                   twist=0.55, rings=2, reach=0.5)
            out["crease"] = one_pose(br, 0.5, "red-base-crease", wedges=8, twist=0, rings=1,
                                     reach=0.30)
            # THE SHIPPED FILE AT THE CEILING, AND ASKED PAST IT. Both have to be the same frame:
            # the clamp is what his verdict costs a score that asks for more.
            out["milk"] = one_pose(br, 0.5, "red-base-milk", wedges=8, twist=0.55, rings=2,
                                   reach=0.30)
            out["milk5"] = one_pose(br, 0.5, "red-base-milk5", wedges=8, twist=0.55, rings=5,
                                    reach=0.30)
            out["door"] = one_pose(br, 0.0, "red-base-door", wedges=8, twist=0.55, rings=1,
                                   reach=0.30)
            return out

        BASE = on_bench(shipped)
        if BASE is None:
            for r in RED_ROWS:
                check(r, False, "the bench never came up for the red-on-bug baselines")
        else:
            _on, _off = crease_hardness(BASE["crease"])
            base_crease = _on / max(_off, 1e-9)

            def probe_mirror(br):
                return one_pose(br, 0.5, "red-mirror", centre=OFF_CENTRE, wedges=8, twist=0.55,
                                rings=2, reach=0.5)
            p = on_bench(probe_mirror, NO_MIRROR)
            if p is None:
                check(RED_ROWS[0], False, "the bench never came up")
            else:
                dm, dx = diff(BASE["deep"], p)
                share = smeared(BASE["deep"], p)
                check(RED_ROWS[0], share >= 0.05,
                      f"with the arithmetic mirror taken out, {share * 100:.1f} per cent of the "
                      f"frame's own points stand further than the project's seam of {SEAM} of 255 "
                      f"from the shipped frame (mean {dm:.2f}, worst channel {dx}), against a bar of "
                      f"5 per cent. What the wrap costs is a REGION and not a level: the host's "
                      f"CLAMP_TO_EDGE answers every point the wedge takes past the picture with its "
                      f"outermost row of texels, so where the fold stays inside the work the two "
                      f"frames are identical and where it leaves it they are unrelated")

            def probe_soft(br):
                return one_pose(br, 0.5, "red-soft", wedges=8, twist=0, rings=1, reach=0.30)
            p = on_bench(probe_soft, NO_SOFT)
            if p is None:
                check(RED_ROWS[1], False, "the bench never came up")
            else:
                hard_on, hard_off = crease_hardness(p)
                check(RED_ROWS[1], hard_on / max(hard_off, 1e-9) > base_crease * 1.10,
                      f"walking the frame ACROSS the fold's own sixteen edges, the kink at the "
                      f"creases stands {hard_on / max(hard_off, 1e-9):.2f} times the picture's own "
                      f"roughness with the retouch reverted, against {base_crease:.2f} times with it "
                      f"standing ({hard_on:.2f} against {hard_off:.2f} of 255) — his В9 word, "
                      f"measured on the creases themselves rather than on the frame at large")

            def probe_cap(br):
                return one_pose(br, 0.5, "red-cap", wedges=8, twist=0.55, rings=5, reach=0.30)
            p = on_bench(probe_cap, NO_CAP)
            if p is None:
                check(RED_ROWS[2], False, "the bench never came up")
            else:
                clamped, _ = diff(BASE["milk"], BASE["milk5"])
                loose, loosex = diff(BASE["milk"], p)
                check(RED_ROWS[2], clamped == 0.0 and loose > SEAM,
                      f"the shipped file answers a score asking for five repeats with the two his "
                      f"verdict allows — the same frame to the pixel ({clamped} of 255) — while with "
                      f"the ceiling raised to the module's own 5 the same request stands "
                      f"{loose:.2f} of 255 away (worst channel {loosex}). That is his «rings>2» word "
                      f"reaching the picture: what a score may ask for is bounded, and the bound is "
                      f"live rather than declared. WHAT FIVE REPEATS LOOK LIKE on this host is a "
                      f"reading and not a gate — see the report: with no mip chain bound they alias "
                      f"rather than wash, the frame's own spread standing "
                      f"{paleness(p):.2f} of 255 against {paleness(BASE['milk']):.2f} at two")

            def probe_gate(br):
                return one_pose(br, 0.0, "red-gate", wedges=8, twist=0.55, rings=1, reach=0.30)
            p = on_bench(probe_gate, NO_GATE)
            if p is None:
                check(RED_ROWS[3], False, "the bench never came up")
            else:
                from PIL import Image as _I
                sz = _I.open(p).size
                own = work_in_the_frame(PHOTOS[0], sz[0], sz[1])
                a, _ = apart(p, own)
                b, _ = apart(BASE["door"], own)
                check(RED_ROWS[3], a > SEAM and b <= SEAM,
                      f"with the finish's gating on the fold reverted, door 0 stands {a:.2f} of 255 "
                      f"from glass-drum.jpg against {b:.2f} shipped, on a bar of {SEAM}: the gamma, "
                      f"the boost and the vignette stand at full strength where the door's own law "
                      f"asks for the photograph its file carries")

# ---------------------------------------------------------------- report
fails = [r for r in results if r[1] == "FAIL"]
skips = [r for r in results if r[1] == "SKIP"]
for name, verdict, detail in results:
    print(f"[{verdict}] {name}")
    if detail:
        print(f"        {detail}")
print(f"\n{len(results) - len(fails) - len(skips)} passed / {len(fails)} failed / "
      f"{len(skips)} skipped")
sys.exit(1 if fails else 0)
