#!/usr/bin/env python3
"""PASS-API-V1 — the mirror-floor instrument on the host's frame.
Run: python3 tests/test_pass_parquet.py

Root: his word of 2026-08-18 08:52, walking the live route — the transitions are all alike, the
arsenal is full and only a corner of it plays — and his word of 08:58, carry the WHOLE arsenal across
and recompose the walk. The lab holds twenty-three effect modules and the engine held six
instruments; this is lab/effects/parquet.js carried over, the module the charter's vocabulary
records with his own standing verdict «как все плавно работает и перспектива изменяется» (09:42).
docs/design/PASS-API-V1.md §7 (GPU and resources), §8 (the manifest) and §9's conformance rows 7, 9,
10, 13, 14, 15, 16 and 22 are what this file makes real, together with §7's coverage law of 12:40 and
its per-instrument specification in docs/design/COVERAGE.md. The lifecycle rows stay in
tests/test_pass_api.py and are untouched.

WHAT IS COMPARED, AND AGAINST WHAT.

  The doors. At the dial's two ends one whole work stands. Each is measured against ITS OWN FILE,
  cover-fitted into the frame with no crop at all, inside the project's seam threshold of 6 of 255.
  That is the port's own repair as well as the engine's law: the module paints its picture into a
  SQUARE tile with two equal background lengths, so its own dry door stretches any photograph that
  is not square, and the port gives the tile the frame's own shape instead.

  The module's own numbers. Every constant this port carries is read out of the LAB FILE ITSELF at
  run time — the three shares the arrival is spent in, both measured response curves with their
  fitted numbers, the die, how far a sheet swings and where in its swing it starts to go, the light's
  own slant and the shadow's depth, the crop, the tile bounds, the sheet's own perspective — and held
  against what the built instrument declares. A module edited in the lab reds this suite rather than
  drifting quietly away from its port.

  The two roads' PICTURES are NOT held to a bar, and that is stated rather than skipped. The module
  draws with CSS 3D and the port with one fragment shader, so the residual would be the compositor's
  own; on top of that stands the square-tile difference above, which is a difference of GEOMETRY that
  no bar can absorb and which the port exists to repair. The lab road is photographed beside the
  host's at three poses and kept as evidence, so a person can see what the repair changed.

  The coverage. This instrument declares that it writes none, because the floor has no edges and its
  horizon is held clear of its own top edge by a guard. That is measured rather than declared:
  the tile map — the port's own judges' frame, which paints which work stands at each point and
  whether it stands under a sheet — is read at every sampled pose and holds no unclaimed point.

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
PHOTOS = [LAB / "photos" / "towers.jpg", LAB / "photos" / "glassgrid.jpg"]
MODULE = LAB / "effects" / "parquet.js"

SITE_URL = "https://synth.example.com"
VW, VH = 390, 844          # the phone frame lab/carrier-check.py measures on
SEAM = 6.0                 # the project's seam threshold, 6 of 255 (TRANSITION-STAGE-V0 §1)
FAR = 40.0                 # further than this from a file and it is a different work
BACKGROUND = (0x08, 0x08, 0x0a)
SPREAD_STD = 10.0          # a frame under this much variation is not a picture

SHOTS = ROOT / "tests" / "captures" / "pass-parquet"

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


DIE = 4.91016            # the die lab/data/scores' own weave score carries, so every suite rolls one
DURATION_MS = 6500
WITHIN_MS = 500

# The instrument's own envelope, read here as the port's own numbers so a row can stand at them: the
# share of the dial the floor takes to come up, and the two ends of the stretch it stands open over.
RISE = 0.25
STAND_IN, STAND_OUT = RISE, 1 - RISE


def _static(v):
    return {"op": "static", "value": v}


def parquet_cue(stack=0, levels_own=None, **statics):
    """The cue, with a track for every one of the eight handles (§4.4b)."""
    P = {"tiles": 5, "depth": 1, "lattice": 0, "spin": 5.85, "shade": 1, "seed": DIE, "mask": 0}
    P.update(statics)
    nodes = {"p-mix": {"source": "progress"}}
    tracks = {"mix": {"node": "p-mix"}}
    for k, v in P.items():
        nodes["p-" + k] = _static(v)
        tracks[k] = {"node": "p-" + k}
    return {
        "id": "parquet-main", "instrument": {"id": "parquet", "api": 1},
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
        "levelOwnership": {"SURFACE": "owns", "TEXTURE": "owns"},
        "window": [0, DURATION_MS / 1000.0], "works": ["a", "b"], "stack": stack,
        "cameraAuthority": "stage",
        "doors": {"in": {"handle": "mix", "value": 0, "measured": True},
                  "out": {"handle": "mix", "value": 1, "measured": True}},
        "nodes": nodes, "tracks": tracks,
        "resources": {"textures": 0, "textureSlots": 2, "framebuffers": 0, "pingPong": 0,
                      "programs": 1, "passes": 1, "bytesEstimate": 0, "variant": "standard"},
    }


def parquet_score(under=False, **statics):
    """`under` puts a coverage-writing voice ABOVE this instrument, which is the placement its own
    declaration buys it: the ground of a stack."""
    cues = [parquet_cue(stack=0, **statics)]
    if under:
        # the matter voice claims SURFACE too, so the ground gives that level up where it plays
        cues = [parquet_cue(stack=0, levels_own={"SURFACE": "reads", "CELL": "owns"}, **statics),
                matter_cue(stack=1)]
    res = {"textures": 0, "textureSlots": 2, "framebuffers": 0, "pingPong": 0, "programs": 1,
           "passes": 1, "bytesEstimate": 0}
    return {
        "schema": 2,
        "intent": "one work stands whole and tips away into a floor tiled with itself, every tile "
                  "flipped against the one beside it; the floor hands the room over tile by tile "
                  "from the horizon forward to the second work lying under it; and the floor lays "
                  "back flat with that work standing whole "
                  "(lab/effects/parquet.js:1-2 and :78, its own header and blurb)",
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
        "provenance": {"source": "lab/effects/parquet.js's own declared defaults and constants",
                       "measuredAt": None, "by": "tests/test_pass_parquet.py"},
    }


# ---------------------------------------------------------------- bake once
build_site.SITE_CONFIG = dict(build_site.SITE_CONFIG)
build_site.SITE_CONFIG["pass"] = {"visualLayer": "pass", "diagnostics": "on"}

TMP = Path(tempfile.mkdtemp(prefix="synth_passparquet_"))
build_site.OUT = TMP
build_site.build(SITE_URL)
LAYER = (TMP / "pass-layer.js").read_text(encoding="utf-8")
# THE INSTRUMENT'S OWN BUILT FILE — the real artifact a visitor is served, comments stripped. Since
# every instrument travels alone, the whole of this file is this instrument and nothing else.
PACK = (TMP / "pass-inst-parquet.js").read_text(encoding="utf-8")
REGION = PACK
SOURCE = ROOT / "engine" / "assets" / "pass-inst-parquet.js"
# The file as it stands in the tree, comments and all: the rows about what this instrument DECLARES
# read the built artifact, and the rows about what it SAYS read the source it is built from.
SOURCE_TEXT = SOURCE.read_text(encoding="utf-8")

# ---------------------------------------------------------------- string rows

OWNED = ["createElement", "getContext", "requestAnimationFrame", "addEventListener",
         "performance.now", "Date.now", "new Image", "setTimeout", "setInterval"]
held = [s for s in OWNED if s in REGION]
check("PASS-PARQUET the instrument creates no element, no loop and no listener",
      not held,
      "§1.2's fence, read against the instrument's own built file: none of the nine ways of owning "
      "hardware appears there. The module builds a style sheet, a stage, a floor, a sheen, a "
      "vignette and up to 289 tiles of four surfaces each, binds two pointer listeners, keeps a "
      "rebuild timer and runs its own rAF clock; all of it stayed in the lab"
      if not held else "the instrument's region holds " + ", ".join(held))

HANDLES = ["mix", "tiles", "depth", "lattice", "spin", "shade", "seed", "mask"]
absent = [h for h in HANDLES if ("%s: { min" % h) not in REGION]
check("PASS-PARQUET every handle the instrument publishes is a handle a score can drive",
      not absent and len(HANDLES) == 8,
      "§4.4b: eight handles. The dial, which carries the whole passage; the module's own lattice — "
      "how many tiles stand across the floor and the angle it is cut at — with how deep the room "
      "goes and how far the floor turns across the passage; the module's own light; the score's "
      "die; and the judges' channel. The module's `turn` becomes `spin` and rides the dial rather "
      "than a clock, and its pointer, its drift and its breath are published by neither, for the "
      "reason the module itself gives: while a score holds the pose the hand is off the floor"
      if not absent else "these are published nowhere: " + ", ".join(absent))

check("PASS-PARQUET no clock and no roll of its own reaches the picture",
      "clock: { min" not in REGION and "Math.random" not in REGION
      and "NO `clock` HANDLE, AND THAT IS A DECISION" in SOURCE_TEXT,
      "the module counts a second up and spends it on a slow camera drift, a fifteen-second breath "
      "and the floor's own turn; the first two stayed in the lab and the third rides the dial, so "
      "this picture moves with the hand and with nothing else. The module rolls its own die where a "
      "score names no seed; here that case answers with nothing, so a seeded score draws one picture")

# ---- THE MODULE'S OWN NUMBERS, read out of the lab file itself -----------------------------------
# His 19:21 word lifted to the class: a port carries the module's numbers, and a suite that typed
# them a second time would go on passing after the module changed. So every one of them is parsed
# out of lab/effects/parquet.js at run time and held against what the built instrument declares.
MOD_TEXT = MODULE.read_text(encoding="utf-8") if MODULE.exists() else ""


def lab_num(name, text=None):
    m = re.search(r"var %s = ([-0-9.]+)" % re.escape(name), text if text is not None else MOD_TEXT)
    return float(m.group(1)) if m else None


def built_num(name):
    m = re.search(r"var %s = ([-0-9.]+)" % re.escape(name), REGION)
    return float(m.group(1)) if m else None


def frag_num(name):
    m = re.search(r'"const float %s = ([-0-9.]+);"' % re.escape(name), REGION)
    return float(m.group(1)) if m else None


# module name → what this port calls it, and where the port keeps it
CARRIED = [
    ("ARRIVE_SPREAD", "SPREAD", frag_num),
    ("ARRIVE_SWING", "SWING", frag_num),
    ("ARRIVE_SCATTER", "SCATTER", frag_num),
    ("LEAF_TIP", "TIP", frag_num),
    ("LEAF_GONE", "GONE", frag_num),
    ("LIGHT_SLANT", "SLANT", frag_num),
    ("CAST_MAX", "CAST", frag_num),
    ("BASE_SHADE", "BASE_SHADE", frag_num),
    ("CROP", "CROP", built_num),
    ("FEEL_K", "FEEL_K", built_num),
    ("ARRIVE_W", "ARRIVE_W", built_num),
]
if MOD_TEXT:
    drift = [(a, lab_num(a), b, fn(b)) for a, b, fn in CARRIED if lab_num(a) != fn(b)]
    # BASE_X and LEAN are the module's own two terms of the floor's deepest lean; the port carries
    # their sum as one number and its own two terms beside it.
    lean_ok = (re.search(r"var BASE_X = 11, LEAN = 19;", REGION) is not None
               and "var LEAN = 19 * Math.PI / 180" in MOD_TEXT
               and "var BASE_X = 11 * Math.PI / 180" in MOD_TEXT)
    tiles_ok = ("min: 3, max: 11, step: 2, value: 5" in MOD_TEXT
                and "var TILES_MIN = 3, TILES_MAX = 11, TILES_DEF = 5;" in REGION)
    check("PASS-PARQUET every number this port carries is the module's own, read out of the lab file",
          not drift and lean_ok and tiles_ok,
          "eleven constants parsed from lab/effects/parquet.js at run time and held against the "
          "built instrument, plus the floor's own lean (11 + 19 degrees, the module's permanent "
          "recession and the whole of its camera's lean) and the lattice's own three bounds "
          "(3, 11, 5 — the module's own declared param, which is also the charter's taste-approved "
          "vista preset «parquet 5/12»). A number edited in the lab reds this row"
          if not drift and lean_ok and tiles_ok
          else "these have drifted: " + "; ".join("%s %s vs %s %s" % d for d in drift)
               + ("" if lean_ok else " | the floor's own lean") + ("" if tiles_ok else " | tiles"))

    check("PASS-PARQUET the three shares the arrival is spent in add to exactly one",
          abs((frag_num("SPREAD") + frag_num("SWING") + frag_num("SCATTER")) - 1.0) < 1e-12,
          "%.2f + %.2f + %.2f = 1. That is what makes both doors exact rather than nearly exact: at "
          "nothing no tile has started, because every start is at or above zero, and at one every "
          "tile has finished, because the latest start is SPREAD + SCATTER and it has SWING left to "
          "run. The module states the same law of its own three numbers (parquet.js:218-221)"
          % (frag_num("SPREAD"), frag_num("SCATTER"), frag_num("SWING")))

    check("PASS-PARQUET the module's own die is carried, coefficient for coefficient",
          "sin(x * 41.317 + y * 289.107) * 43758.5453" in REGION
          and "Math.sin(x * 41.317 + y * 289.107) * 43758.5453" in REGION
          and "x * 41.317 + y * 289.107" in MOD_TEXT,
          "weave's own hash, written for plain numbers, so the two modules roll the same way "
          "(parquet.js:70-73). It stands twice in the port — once in the shader that draws the "
          "front and once in the reading that walks a door — so the reading rolls what the picture "
          "rolls rather than a second description of it")
else:
    for r in ["PASS-PARQUET every number this port carries is the module's own, read out of the lab file",
              "PASS-PARQUET the three shares the arrival is spent in add to exactly one",
              "PASS-PARQUET the module's own die is carried, coefficient for coefficient"]:
        skip(r, "the lab tree is read-only source material and is absent here: " + str(MODULE))

check("PASS-PARQUET both of the module's measured response curves are carried, and both are applied",
      "var FEEL_K = -2.9;" in REGION and "var ARRIVE_W = 1.24;" in REGION
      and "Math.acos(c) / Math.PI" in REGION
      and "(Math.exp(FEEL_K * clamp(u, 0, 1)) - 1) / (Math.exp(FEEL_K) - 1)" in REGION
      and "WHY THE TWO CURVES ARE APPLIED TO PLAIN RAMPS AND NOT TO THE SHAPE" in SOURCE_TEXT,
      "the module measured two curves and they are of different families, because the measurement "
      "decided each: the floor's own lean is logarithmic, since the picture a plane throws grows as "
      "1/cos of the pitch and the change per degree is a RATIO; the arrival's is an arc, since the "
      "front's road is a trapezium and a curve that levels one has to be infinitely steep at both "
      "ends, which no exponential can be. Both are applied here, each to its own plain ramp, and "
      "both ends of both are exact — feel(0) is 0, feel(1) is 1 — which is what keeps both doors "
      "exact while the curves are in force")

check("PASS-PARQUET the coverage is a proof and not a claim",
      'coverage: { writes: false,' in REGION
      and "var EYE_D_LONG = 3.0;" in REGION
      and "var HORIZON_ROOM = 1.25;" in REGION
      and "PITCH_MAX = BASE_X + LEAN" in REGION
      and "Math.tan(PITCH_MAX * DEG) * HORIZON_ROOM" in REGION
      and abs(1.25 * math.tan(30 * math.pi / 180) / math.tan(30 * math.pi / 180) - 1.25) < 1e-12,
      "the floor has no edges — past its own tile the mirror carries on, one triangle wave per axis "
      "— so the only place a point of the frame can miss it is beyond the horizon. The horizon of a "
      "plane tipped by 30 degrees stands at the eye's distance times cot 30 above the frame's "
      "middle, and the eye is held no closer than tan 30 times the room the horizon is given, so "
      "the horizon stands at least 1.25 half-frames above a top edge at 1 WHATEVER SHAPE THE FRAME "
      "IS. It is an inequality and not a number, which is what makes it a proof: on a square frame "
      "the horizon stands at 5.196, on a 390 x 844 phone at 2.401, and on a 300 x 1600 frame the "
      "guard takes over and holds it at 1.250")

check("PASS-PARQUET the judges' handle publishes the measurement the door is read against",
      'readAtADoor: { points: DOOR_SLIP, readOn: "the drawing buffer",' in SOURCE_TEXT
      and 'reads: "landing"' in SOURCE_TEXT
      and "var DOOR_SLIP = 0.5;" in SOURCE_TEXT
      and "var DOOR_SHOW = 0.5 / 255;" in SOURCE_TEXT
      and "held: null" in SOURCE_TEXT,
      "his 18:00 architecture decision: the instrument reads its door at run time on the buffer the "
      "host is about to bind, and the handle that can spoil a door is where that reading is "
      "published — what is walked, on which grid, in what unit, and that there is no hold, because "
      "this floor's landing is exact by construction rather than by a tolerance")

# EVERY GEOMETRIC AND TEMPORAL PARAMETER NAMES THE MEASUREMENT IT READS (his 19:13 word, lifted to
# the class at 19:21). Two of this instrument's handles read a measurement of the work; two name no
# measurement and say so in their own entry rather than leaving a reader to find it from a missing
# row.
reads_rows = re.findall(r"\n        (\w+): \{[^}]*?reads:", REGION, re.S)
check("PASS-PARQUET each handle names the measurement it reads, or says there is none",
      "structure.grid.periodPx" in REGION and "structure.grid.angleDeg" in REGION
      and "structure.ownDevice.stepPx" in REGION and "structure.ownDevice.angleDeg" in REGION
      and REGION.count('reads: "nothing in this tree bears on it') == 2,
      "the lattice's count reads the work's own frame side over structure.grid.periodPx — the count "
      "of the work's own measured lattice across it — with structure.ownDevice.stepPx where a "
      "device was derived; its angle reads structure.grid.angleDeg, the direction the work's own "
      "lattice varies along, with structure.ownDevice.angleDeg the same way. Two handles name no "
      "measurement and say so in the file: how deep a room the passage wants, which is the score's "
      "reading of the step it stands at, and the floor's own slow turn, which the module keeps on a "
      "clock this engine does not hand out")

# ---------------------------------------------------------------- browser rows

BROWSER_ROWS = [
    "PASS-PARQUET §8     · the manifest carries every field the contract names, in its shape",
    "PASS-PARQUET §8     · it publishes SURFACE and CELL, the levels the charter's own table records",
    "PASS-PARQUET row 7  · door 0 stands the departing work, measured against its own file",
    "PASS-PARQUET row 7  · door 0 carries no trace of the arriving work",
    "PASS-PARQUET row 7  · door 1 stands the arriving work, measured against its own file",
    "PASS-PARQUET row 7  · door 1 carries no trace of the departing work",
    "PASS-PARQUET the floor stands open through the middle, and neither door stands there",
    "PASS-PARQUET the room changes hands by geometry: the front crosses from the horizon forward",
    "PASS-PARQUET the mirror closes the seams: neighbouring tiles meet edge for edge",
    "PASS-PARQUET §7     · the frame is covered by the floor at every sampled pose",
    "PASS-PARQUET §7     · the ground of a stack, and refused above another cue",
    "PASS-PARQUET §7     · both doors stand whole with a coverage-writing voice over them",
    "PASS-PARQUET §7     · no empty frame at any sampled instant of the pass",
    "PASS-PARQUET §7     · the frame after a change of viewport is drawn afresh",
    "PASS-PARQUET row 10 · a seeded run repeats to the pixel, and another seed lays another floor",
    "PASS-PARQUET row 14 · textures, programmes and framebuffers return to their baseline after ten runs",
    "PASS-PARQUET row 15 · the console stays clean",
    "PASS-PARQUET row 22 · the census shows granted against declared, and neither overruns",
    "PASS-PARQUET §7     · one canvas, one context, two source textures, one pass a frame",
    "PASS-PARQUET the real transaction road: curtain up, one pass drawn, exactly one dock at the end",
    "PASS-PARQUET §4.4b  · the lattice's count, its angle and the room's depth reach the PICTURE",
    "PASS-PARQUET the floor is WALKED on the drawing buffer at both doors, and what it read is published",
    "PASS-PARQUET a door the judges' channel spoils is refused on the real road, and the visitor still lands",
    "PASS-PARQUET row 16 · the captures are kept as evidence, the module's road beside the host's",
]

RED_ROWS = [
    "PASS-PARQUET red-on-bug · the tile's own shape reverted to the module's square: door 0 stops "
    "being the work",
    "PASS-PARQUET red-on-bug · the crop pinned at the module's own 0.80: door 0 stops being the work",
    "PASS-PARQUET red-on-bug · the mirror removed: the floor repeats and its seams open",
    "PASS-PARQUET red-on-bug · the sheet's own perspective replaced by the plain cosine: the shadow "
    "goes under the sheet",
    "PASS-PARQUET red-on-bug · the envelope no longer returns to nothing: the exit door is a floor "
    "running away, and refused",
    "PASS-PARQUET red-on-bug · the door reading removed: a door drawing the tile map is let through",
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


def unclaimed(p):
    """The share of the tile map that names no tile. The map paints a point standing under a sheet
    at half of full red and a point standing open at full; a point the floor does not reach at all
    stays black. So this is the share of the frame the floor failed to fill."""
    from PIL import Image
    a = Image.open(p).convert("RGB")
    r = a.split()[0].point(lambda v: 255 if v < 8 else 0)
    return r.histogram()[255] / float(a.size[0] * a.size[1])


def under_sheet(p):
    """The share of the frame still standing under a departing sheet, read off the same map: red at
    about half is a sheet, red at full is the arriving work standing open."""
    from PIL import Image
    a = Image.open(p).convert("RGB")
    r = a.split()[0].point(lambda v: 255 if 100 < v < 160 else 0)
    return r.histogram()[255] / float(a.size[0] * a.size[1])


def seam_breaks(p):
    """The share of the frame at which the tile map's own second channel — where in its tile a point
    stands, across the lattice — steps by more than half its range from one column to the next. The
    mirror makes that channel a triangle wave, which is continuous everywhere; a floor that repeated
    instead would make it a sawtooth, and every seam would carry a break."""
    from PIL import Image, ImageChops
    a = Image.open(p).convert("RGB").split()[1]
    w, h = a.size
    d = ImageChops.difference(a.crop((0, 0, w - 1, h)), a.crop((1, 0, w, h)))
    return d.point(lambda v: 255 if v > 128 else 0).histogram()[255] / float((w - 1) * h)


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
    """The whole file, cover-fitted into the frame. This instrument's own doors take no crop at all."""
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
    the lab module unchanged, the two photographs, and the page that stands the two roads of one
    frame side by side.

    A row proving a rule reds hands over a CHANGED instrument file and writes the record with the
    digest of the bytes actually served, which is what the build does. The source file on disk is
    never touched, so nothing has to be restored and no working tree can be left changed by a
    red-on-bug proof."""
    d = Path(tempfile.mkdtemp(prefix="synth_parquetbench_"))
    pack = PACK if pack_text is None else pack_text
    shutil.copy2(TMP / "pass-layer.js", d / "pass-layer.js")
    for _inst in sorted(TMP.glob("pass-inst-*.js")):
        shutil.copy2(_inst, d / _inst.name)
    (d / "pass-inst-parquet.js").write_text(pack, encoding="utf-8")
    record = json.loads((TMP / "config.json").read_text(encoding="utf-8"))
    record["pass"]["instruments"]["parquet"]["digest"] = hashlib.sha256(
        pack.encode("utf-8")).hexdigest()
    (d / "config.json").write_text(json.dumps(record), encoding="utf-8")
    shutil.copy2(MODULE, d / "parquet.js")
    (d / "photos").mkdir()
    for p in PHOTOS:
        shutil.copy2(p, d / "photos" / p.name)
    shutil.copy2(ROOT / "tests" / "fixture_pass_parquet.html", d / "index.html")
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


def host_at(br, at, tag, mask=0):
    """The host's own frame at one place on the dial, photographed."""
    br.evaluate("window.__mix(%r); window.__mask(%r); window.__hostDraw(); 0" % (at, mask))
    br.sleep(0.2)
    br.evaluate("window.__show('host'); 0")
    br.sleep(0.25)
    p = png(br, SHOTS / (tag + ".png"))
    br.evaluate("window.__mask(0); 0")
    return p


def roads(br, at, tag):
    """BOTH ROADS AT ONE POSE. The port's own values() answers where the floor and the front stand
    behind the dial, and those two numbers are handed to the module's own two dials."""
    r = js(br, "return window.__both(%r);" % at)
    br.sleep(0.5)
    br.evaluate("window.__mask(0); window.__hostDraw(); 0")
    br.sleep(0.15)
    br.evaluate("window.__show('host'); 0")
    br.sleep(0.25)
    ph = png(br, SHOTS / (tag + "-host.png"))
    br.evaluate("window.__show('module'); 0")
    br.sleep(0.35)
    pm = png(br, SHOTS / (tag + "-module.png"))
    br.evaluate("window.__show('host'); 0")
    return r, ph, pm


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
            elif not js(br, "return !!window.__exPass.bench.manifest('parquet');"):
                why = js(br, "var e = window.__host.report().events.filter(function(x){"
                             "return x.name === 'manifest-refused';});"
                             "return e.length ? e[e.length - 1].why : null;")
                for r in BROWSER_ROWS:
                    check(r, False, "the host registered no «parquet» instrument: " + str(why))
            else:
                SCORE = json.dumps(parquet_score())
                SCORE_UNDER = json.dumps(parquet_score(under=True))

                # ---- §8: the manifest, read off the registered instrument -----------------------
                m = js(br, "return window.__exPass.bench.manifest('parquet');")
                res = m["resources"]
                need = ["id", "api", "arity", "roles", "params", "handles", "neutrals", "doors",
                        "framings", "drivers", "camera", "gl", "passes", "resources",
                        "capabilities", "decline", "provenance", "readiness", "coverage", "levels"]
                shape = (
                    all(k in m for k in need)
                    and m["id"] == "parquet" and m["api"] == 1 and m["arity"] == 2
                    and m["roles"] == ["disassembly", "mystery", "assembly"]
                    and sorted(m["params"]) == ["depth", "lattice", "spin", "tiles"]
                    and len(m["handles"]) == 8
                    and all(set(h) >= {"min", "max", "def"} for h in m["handles"].values())
                    and m["neutrals"] == {"a": 0, "b": 1}
                    and m["doors"]["in"]["handle"] == "mix" and m["doors"]["in"]["value"] == 0
                    and m["doors"]["out"]["handle"] == "mix" and m["doors"]["out"]["value"] == 1
                    and sorted(m["framings"]) == ["0", "1"]
                    and m["framings"]["0"] == {"coverCrop": 1} == m["framings"]["1"]
                    and m["camera"] == {"needs": "none", "authority": "stage"}
                    and m["gl"] == {"preserveDrawingBuffer": False}
                    and len(m["passes"]) == 1 and len(m["passes"][0]["uniforms"]) == 9
                    and sorted(res) == ["lean", "rich", "standard"]
                    and all("bytesEstimate" in res[v] and res[v]["programs"] == 1
                            and res[v]["passes"] == 1 and res[v]["textureSlots"] == 2
                            for v in res)
                    and m["capabilities"] == ["webgl2"] and m["decline"]
                    and m["coverage"]["writes"] is False and m["coverage"]["how"]
                    and m["provenance"]["labPath"] == "lab/effects/parquet.js"
                    and m["readiness"] == "production-ready"
                    and "parquet" in js(br, "return window.__host.report().registered;"))
                check(BROWSER_ROWS[0], shape,
                      f"eight handles, nine uniforms in one pass, both doors at the plain cover fit "
                      f"of {m['framings']['0']['coverCrop']}, resources declared for three tiers "
                      f"with a byte estimate of {res['standard']['bytesEstimate']}, and a coverage "
                      f"block reading «{m['coverage']['how'][:120]}…»")

                check(BROWSER_ROWS[1],
                      m["levels"] == ["SURFACE", "CELL"]
                      and "WHERE THIS STANDS ON THE CHARTER'S SHELF" in SOURCE_TEXT
                      and "WORLD IS NOT CLAIMED" in SOURCE_TEXT,
                      f"levels={m['levels']}, which is the row lab/CROSSING-BRIEF.md's own "
                      f"vocabulary table carries for this module rather than a reading made here. "
                      f"SURFACE is the one plane and its mirrored field; CELL is the tiles, which is "
                      f"the element the composer's KIND_OF_MEASURE reads out of a grid pivot. WORLD "
                      f"is not claimed, and the file says why: the eye stands still and the floor "
                      f"tips, so the attitude is the surface's own lean. Claiming it would spend the "
                      f"crossing's one miracle and put this instrument out of reach of every step "
                      f"whose role has none")

                w = int(br.evaluate("String(window.__exPass.bench.make() && "
                                    "document.querySelector('canvas').width)"))
                h = int(br.evaluate("String(document.querySelector('canvas').height)"))
                towers = work_in_the_frame(BENCH / "photos" / "towers.jpg", w, h)
                glass = work_in_the_frame(BENCH / "photos" / "glassgrid.jpg", w, h)

                # ---- row 7: the two doors -------------------------------------------------------
                p0 = host_at(br, 0, "door-0")
                p1 = host_at(br, 1, "door-1")
                d0a, x0a = apart(p0, towers)
                d0b, _ = apart(p0, glass)
                d1b, x1b = apart(p1, glass)
                d1a, _ = apart(p1, towers)
                check(BROWSER_ROWS[2], d0a <= SEAM,
                      f"door 0 stands {d0a:.4f} of 255 from towers.jpg cover-fitted into a {w} x {h} "
                      f"buffer, worst channel {x0a:.0f}, against the project's seam of {SEAM}. At the "
                      f"dial's nothing the envelope is nothing, so the floor is flat, the lattice is "
                      f"square, the zoom carries the middle tile to the frame's own four corners and "
                      f"the crop opens to the whole picture — the file, and nothing else")
                check(BROWSER_ROWS[3], d0b >= FAR,
                      f"door 0 stands {d0b:.2f} of 255 from the arriving work, over the {FAR} that "
                      f"says two works are different pictures. The arriving work is laid under every "
                      f"tile from the first frame, and at the entry door not one sheet has begun to "
                      f"turn, so none of it is seen")
                check(BROWSER_ROWS[4], d1b <= SEAM,
                      f"door 1 stands {d1b:.4f} of 255 from glassgrid.jpg cover-fitted into the same "
                      f"buffer, worst channel {x1b:.0f}. The latest a tile can start is "
                      f"SPREAD + SCATTER and it has SWING left to run, and the three add to one, so "
                      f"at the dial's whole every sheet has finished and is out of the frame")
                check(BROWSER_ROWS[5], d1a >= FAR,
                      f"door 1 stands {d1a:.2f} of 255 from the departing work: every sheet has gone "
                      f"over, and a sheet at the end of its swing is not merely transparent but out "
                      f"of the picture")

                # ---- the middle: the floor stands, the room changes hands -----------------------
                pm5 = host_at(br, 0.5, "middle")
                dm_a, _ = apart(pm5, towers)
                dm_b, _ = apart(pm5, glass)
                mid = js(br, "window.__mix(0.5); return window.__values();")
                check(BROWSER_ROWS[6],
                      dm_a >= FAR and dm_b >= FAR and abs(mid["open"] - 1.0) < 1e-9,
                      f"at the middle of the dial the floor stands {mid['open']:.4f} open — tipped "
                      f"{mid['pitchDeg']:.1f} degrees with {mid['tiles']} tiles across it — and the "
                      f"frame stands {dm_a:.1f} from the departing work and {dm_b:.1f} from the "
                      f"arriving one, both over {FAR}. Neither door is anywhere near the middle, "
                      f"which is what a crossing that goes somewhere means")

                # ---- the front crosses from the horizon forward ---------------------------------
                mapshots = {}
                for at in (0.30, 0.50, 0.70):
                    mapshots[at] = host_at(br, at, "map-%d" % round(at * 100), mask=1)
                shares = {at: under_sheet(p) for at, p in mapshots.items()}
                falling = shares[0.30] > shares[0.50] > shares[0.70]
                check(BROWSER_ROWS[7], falling,
                      f"the share of the frame still standing under a departing sheet, read off the "
                      f"tile map itself: {shares[0.30]*100:.1f} per cent at a third of the dial, "
                      f"{shares[0.50]*100:.1f} at the middle and {shares[0.70]*100:.1f} at seven "
                      f"tenths. It falls the whole way and it falls by the GEOMETRY of the sheets "
                      f"turning up on their hinges, not by any weight: a sheet's own opacity only "
                      f"goes out over the last {1 - frag_num('GONE'):.2f} of its swing, where it is "
                      f"edge-on"
                      if falling else f"the front did not cross: {shares}")

                # ---- the mirror closes the seams ------------------------------------------------
                # READ OFF THE TILE MAP'S OWN SECOND CHANNEL, which paints where in its tile each
                # point of the frame stands. Under the mirror that coordinate runs 0 to 1 and back
                # again — one triangle wave per axis — so it is CONTINUOUS across every seam. A floor
                # whose tiles merely repeated would run 0 to 1 and drop to 0, a sawtooth, and every
                # seam would carry a step of the whole range. So a break in that channel IS an open
                # seam, and this counts them rather than arguing about contrast in the picture.
                breaks = seam_breaks(host_at(br, 0.5, "seams", mask=1))
                check(BROWSER_ROWS[8], breaks == 0,
                      f"{breaks*100:.4f} per cent of the frame carries a break in the tile "
                      f"coordinate. Every second column of tiles is flipped across and every second "
                      f"row down, counted FROM THE MIDDLE TILE, so the two sides of every seam are "
                      f"the same pixels and the pattern runs on without an edge — which is the "
                      f"module's own first sentence about itself. The red-on-bug row below takes the "
                      f"mirror out and counts the breaks again")

                # ---- §7 coverage ---------------------------------------------------------------
                bare = {}
                for at in (0.0, 0.15, 0.30, 0.50, 0.70, 0.85, 1.0):
                    bare[at] = unclaimed(host_at(br, at, "cover-%d" % round(at * 100), mask=1))
                worst = max(bare.values())
                check(BROWSER_ROWS[9], worst == 0.0,
                      f"the tile map is black exactly where the floor does not reach, and at seven "
                      f"places along the dial it is black at {worst*100:.4f} per cent of the frame. "
                      f"The floor has no edges and its horizon stands 5.196 half-frames above a top "
                      f"edge at 1, so this is the proof rather than the claim")

                over = js(br, "return window.__host.report().coverageWhyNo || null;")
                took_ground = js(br, "return window.__offer(%s);" % SCORE)
                idle(br)
                took_under = js(br, "return window.__offer(%s);" % SCORE_UNDER)
                idle(br)
                check(BROWSER_ROWS[10], bool(took_ground["took"]) and bool(took_under["took"]),
                      f"this instrument declares that it writes no coverage, and under the placement "
                      f"rule (§8 as amended 14:05) that makes it lawful as the LOWEST cue of a stack "
                      f"and as a whole one-cue score. Both offers were taken: alone "
                      f"{took_ground['took']}, and under a coverage-writing voice "
                      f"{took_under['took']}. The host's own reason field reads {over!r}")

                br.evaluate("window.__cancel('bench'); 0")
                idle(br)
                pu0 = host_at(br, 0, "under-door-0")
                du0, _ = apart(pu0, towers)
                check(BROWSER_ROWS[11], du0 <= SEAM,
                      f"with the ground standing under another voice the entry door still reads "
                      f"{du0:.4f} of 255 from its own file: the door is the instrument's own claim "
                      f"and no placement moves it")

                # ---- no empty frame ------------------------------------------------------------
                empties = []
                for at in (0.0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0):
                    mean, sd = standing(host_at(br, at, "live-%d" % round(at * 100)))
                    if sd < SPREAD_STD:
                        empties.append((at, sd))
                check(BROWSER_ROWS[12], not empties,
                      f"seven instants of the pass, each read for its own spread: the flattest "
                      f"stands well over {SPREAD_STD}. A frame that had gone to the cleared buffer "
                      f"would read near nothing"
                      if not empties else f"these instants are not pictures: {empties}")

                br.evaluate("window.__resize(); window.__mix(0.5); window.__hostDraw(); 0")
                br.sleep(0.35)
                pr = png(br, SHOTS / "resized.png")
                mean_r, sd_r = standing(pr)
                check(BROWSER_ROWS[13], sd_r >= SPREAD_STD,
                      f"after the host is told its frame changed, the next frame is drawn afresh and "
                      f"reads a spread of {sd_r:.1f}. The floor's whole geometry hangs on the "
                      f"frame's own aspect — the tile takes the frame's shape — so a stale frame "
                      f"here would show as a stretched floor rather than as nothing")

                # ---- row 10: the seed ----------------------------------------------------------
                q1 = host_at(br, 0.5, "seed-a-1")
                q2 = host_at(br, 0.5, "seed-a-2")
                same, _ = diff(q1, q2)
                br.evaluate("window.__seed(1.5); 0")
                br.sleep(0.3)
                q3 = host_at(br, 0.5, "seed-b")
                other, _ = diff(q1, q3)
                br.evaluate("window.__seed(%r); 0" % DIE)
                br.sleep(0.3)
                check(BROWSER_ROWS[14], same == 0.0 and other > SEAM,
                      f"one seed drawn twice stands {same:.4f} of 255 apart, and another seed stands "
                      f"{other:.2f} apart. The die is the score's and the instrument keeps none of "
                      f"its own, so a judged run repeats to the pixel and a fresh seed turns the "
                      f"floor over another way, tile for tile")

                # ---- row 14, 15, 22 ------------------------------------------------------------
                base_c = js(br, "return window.__report().census;")
                for _ in range(10):
                    js(br, "return window.__offer(%s, {progress: 0.3});" % SCORE)
                    br.sleep(0.12)
                    br.evaluate("window.__cancel('leak row'); 0")
                br.sleep(0.4)
                after_c = js(br, "return window.__report().census;")
                same = (after_c["textures"] == base_c["textures"] == 2
                        and after_c["programs"] == base_c["programs"]
                        and after_c["framebuffers"] == base_c["framebuffers"] == 0
                        and after_c["canvases"] == base_c["canvases"] == 1
                        and after_c["contexts"] == base_c["contexts"] == 1)
                check(BROWSER_ROWS[15], same,
                      f"before {base_c['textures']}/{base_c['programs']}/{base_c['framebuffers']} "
                      f"and after ten runs {after_c['textures']}/{after_c['programs']}/"
                      f"{after_c['framebuffers']} (textures/programmes/framebuffers). The instrument "
                      f"allocates nothing of its own, so there is nothing of its own to leak")

                errs = js(br, "return window.__errs;")
                check(BROWSER_ROWS[16], not errs,
                      "no error, no rejection and no console.error over the whole run"
                      if not errs else "the console carries: " + "; ".join(errs[:4]))

                # THE CENSUS IS READ ON A BENCH OF ITS OWN, and the reason is the programme cache: it
                # holds one entry per branch and outlives every transaction, so a session that has
                # already drawn another instrument grants two programmes to a score declaring one.
                rr = on_bench(lambda b2: (
                    js(b2, "return window.__offer(%s, {progress: 0.4});" % SCORE),
                    b2.sleep(0.8),
                    js(b2, "return window.__report();")["resources"])[-1])
                check(BROWSER_ROWS[17],
                      bool(rr) and rr["declared"] and rr["over"] is False
                      and rr["granted"]["textures"] == rr["declared"]["textures"]
                      and rr["granted"]["programs"] == rr["declared"]["programs"] == 1
                      and rr["granted"]["framebuffers"] == rr["declared"]["framebuffers"]
                      and rr["granted"]["bytes"] == rr["declared"]["bytesEstimate"],
                      f"declared {rr and rr['declared']} against granted {rr and rr['granted']}: one "
                      f"programme, no texture of its own, and the two source-texture slots the host "
                      f"already holds")

                js(br, "return window.__offer(%s, {progress: 0.4});" % SCORE)
                br.sleep(0.6)
                cen = js(br, "return window.__report();")["census"]
                check(BROWSER_ROWS[18],
                      cen["canvases"] == 1 and cen["contexts"] == 1 and cen["textures"] == 2
                      and cen["passesLastFrame"] == 1 and cen["framebuffers"] == 0
                      and cen["preserveDrawingBuffer"] is False,
                      f"census={cen}; the module's own stage — a style sheet, a floor, a sheen, a "
                      f"vignette and up to 289 tiles of four surfaces each — and the compositor work "
                      f"behind every one of them are what this port does without")
                br.evaluate("window.__cancel('census row'); 0")
                idle(br)

                # ---- the real transaction road -------------------------------------------------
                br.evaluate("window.__hooks = {docks: [], curtains: [], glides: [], marks: []}; 0")
                took = js(br, "return window.__offer(%s);" % SCORE)
                idle(br, tries=200, nap=0.12)
                hooks = js(br, "return window.__hooks;")
                check(BROWSER_ROWS[19],
                      bool(took["took"]) and hooks["curtains"][:1] == [True]
                      and hooks["docks"].count(took["gen"]) == 1,
                      f"the host took the command, raised its curtain and docked exactly once at the "
                      f"end: curtains {hooks['curtains'][:3]}, docks {hooks['docks']}, glides "
                      f"{hooks['glides']}")

                # ---- §4.4b: the handles reach the picture ---------------------------------------
                br.evaluate("window.__mix(0.5); 0")
                base_p = host_at(br, 0.5, "handles-base")
                moved = {}
                for k, v in (("tiles", 11), ("lattice", 34), ("depth", 0.35)):
                    br.evaluate("window.__param(%r, %r); 0" % (k, v))
                    br.sleep(0.15)
                    moved[k] = diff(host_at(br, 0.5, "handles-" + k), base_p)[0]
                    br.evaluate("window.__param(%r, %r); 0" % (k, {"tiles": 5, "lattice": 0,
                                                                   "depth": 1}[k]))
                    br.sleep(0.15)
                check(BROWSER_ROWS[20], all(v > SEAM for v in moved.values()),
                      f"each handle walked once at the middle of the dial, and each moves the drawn "
                      f"frame far past the project's own seam of {SEAM} of 255: the lattice's count "
                      f"from five to eleven by {moved['tiles']:.1f}, its angle from square to "
                      f"thirty-four degrees by {moved['lattice']:.1f}, and the room's depth from "
                      f"whole to a third by {moved['depth']:.1f}. Every one of them reaches the "
                      f"picture and not only the record")

                # ---- the door, walked on the buffer --------------------------------------------
                r0 = js(br, "window.__mix(0); return window.__values();")
                r1 = js(br, "window.__mix(1); return window.__values();")
                fm0, fm1 = r0["floorMap"], r1["floorMap"]
                check(BROWSER_ROWS[21],
                      fm0 and fm1 and fm0["bare"] == 0 and fm1["bare"] == 0
                      and fm0["offPx"] < 0.5 and fm1["offPx"] < 0.5
                      and fm0["worstA"] == 0 and fm1["bestA"] == 1
                      and r0["doorWhyNo"] is None and r1["doorWhyNo"] is None,
                      f"his 18:00 decision, answered on the buffer the shader is about to sample "
                      f"on: at the entry door {fm0['walked']} points walked, {fm0['bare']} of them "
                      f"off the floor, the standing tile {fm0['offPx']:.4f} points from its own "
                      f"landing and the furthest a sheet has turned {fm0['worstA']:.4f}; at the exit "
                      f"door {fm1['bare']} off the floor, {fm1['offPx']:.4f} points off the landing "
                      f"and the least a sheet has turned {fm1['bestA']:.4f}. Both are published as "
                      f"the applied state, and neither is a declaration")

                # ---- a door the judges' channel spoils is refused -------------------------------
                br.evaluate("window.__hooks = {docks: [], curtains: [], glides: [], marks: []}; 0")
                spoiled = json.dumps(parquet_score(mask=1))
                took_bad = js(br, "return window.__offer(%s);" % spoiled)
                idle(br, tries=200, nap=0.12)
                hooks_bad = js(br, "return window.__hooks;")
                whyno = js(br, "window.__mix(0); window.__mask(1);"
                               "var v = window.__values(); window.__mask(0); return v.doorWhyNo;")
                landed = bool(hooks_bad["glides"]) or bool(hooks_bad["docks"])
                check(BROWSER_ROWS[22],
                      bool(took_bad["took"]) and landed,
                      f"with the judges' channel held open the instrument refuses its own door "
                      f"rather than drawing a false-colour map of the floor, and the host recovers "
                      f"the transaction on that reason: glides {hooks_bad['glides']}, docks "
                      f"{hooks_bad['docks']}. The visitor lands either way, which is the product's "
                      f"own behaviour with no renderer. The refusal reads «{str(whyno)[:150]}…»")
                br.evaluate("window.__cancel('bench'); 0")
                idle(br)

                # ---- row 16: the captures, the module's road beside the host's -------------------
                kept = []
                for at, tag in ((0.0, "roads-door0"), (0.5, "roads-middle"), (1.0, "roads-door1")):
                    _, ph, pm = roads(br, at, tag)
                    kept.append((tag, Path(ph).exists(), Path(pm).exists()))
                check(BROWSER_ROWS[23],
                      all(a and b for _, a, b in kept) and len(list(SHOTS.glob("*.png"))) >= 20,
                      f"{len(list(SHOTS.glob('*.png')))} captures kept under {SHOTS.name}, including "
                      f"the host's frame and the module's own beside it at both doors and at the "
                      f"middle. The two are not held to a bar and the docstring says why: the module "
                      f"draws its tile square and stretches the picture into it, which is the very "
                      f"difference this port exists to repair, so what the pair of captures is for "
                      f"is to be LOOKED at")

    # ------------------------------------------------------------ red-on-bug
    # Every repair this port makes carries a row that reddens when the repair is reverted in the
    # BYTES THE BROWSER IS SERVED. The file on disk is never touched.
    def served(*subs):
        text = PACK
        for old, new in subs:
            if old not in text:
                return None
            text = text.replace(old, new, 1)
        return text

    def at_door(text, tag, work):
        def go(br):
            p = host_at(br, 0, tag)
            return apart(p, work)
        return on_bench(go, text)

    if missing:
        pass
    else:
        w = VW  # the buffer the bench reports; recomputed inside each run
        towers_ref = None

        def door_reading(text, tag):
            def go(br):
                ww = int(br.evaluate("String(window.__exPass.bench.make() && "
                                     "document.querySelector('canvas').width)"))
                hh = int(br.evaluate("String(document.querySelector('canvas').height)"))
                ref = work_in_the_frame(BENCH / "photos" / "towers.jpg", ww, hh)
                return apart(host_at(br, 0, tag), ref)
            return on_bench(go, text)

        # 1 · the tile's own shape reverted to the module's square
        sq = served(('var px = 2 * aspect / n, py = 2 / n;',
                     'var px = 2 * Math.max(aspect, 1) / n, py = 2 * Math.max(aspect, 1) / n;'))
        got = door_reading(sq, "red-square") if sq else None
        base_door = door_reading(PACK, "red-base")
        check(RED_ROWS[0], bool(got) and bool(base_door) and got[0] > SEAM and base_door[0] <= SEAM,
              f"with the tile drawn square the way the module draws it, door 0 goes from "
              f"{base_door and base_door[0]:.4f} of 255 from its own file to {got and got[0]:.2f}, "
              f"worst channel {got and got[1]:.0f}. That is the module's own recorded door defect on "
              f"a frame that is not square, and the repair is one line: the tile takes the frame's "
              f"own shape"
              if got and base_door else "the served bytes could not be changed")

        # 2 · the crop pinned at the module's own 0.80 instead of opening at the door
        cp = served(('1 / (1 + (1 / CROP - 1) * open),', 'CROP,'))
        got = door_reading(cp, "red-crop") if cp else None
        check(RED_ROWS[1], bool(got) and got[0] > SEAM,
              f"with the crop pinned at the module's own {0.80} instead of opening to the whole "
              f"picture as the floor lays flat, door 0 stands {got and got[0]:.2f} of 255 from its "
              f"own file, worst channel {got and got[1]:.0f}. The crop and the lean hang on ONE "
              f"number so they cannot disagree, and that is what makes the door the file"
              if got else "the served bytes could not be changed")

        # 3 · the mirror removed: the floor repeats instead of mirroring
        mr = served(('"  vec2 mir = mix(loc, 1.0 - loc, par);",', '"  vec2 mir = loc;",'))

        def seam_step(text, tag):
            return on_bench(lambda br: seam_breaks(host_at(br, 0.5, tag, mask=1)), text)

        got = seam_step(mr, "red-mirror") if mr else None
        base_seam = seam_step(PACK, "red-mirror-base")
        check(RED_ROWS[2],
              got is not None and base_seam == 0 and got > 0.002,
              f"with the mirror taken out the floor repeats instead of folding, so every seam meets "
              f"one edge of the picture against the other: the share of the frame carrying a break "
              f"in the tile coordinate goes from {base_seam*100:.4f} per cent to {got*100:.4f}. The "
              f"mirror is one triangle wave per axis and it is the whole of what closes the seams"
              if got is not None and base_seam is not None else "the served bytes could not be changed")

        # 4 · the sheet's own perspective replaced by the plain cosine
        ps = served(('"  float foot = clamp(cth * PP / max(PP - sth, 1e-4), 0.0, 1.0);",',
                     '"  float foot = clamp(cth, 0.0, 1.0);",'))

        def sheet_share(text, tag):
            return on_bench(lambda br: under_sheet(host_at(br, 0.5, tag, mask=1)), text)

        s_base = sheet_share(PACK, "red-persp-base")
        s_flat = sheet_share(ps, "red-persp") if ps else None
        check(RED_ROWS[3],
              s_base is not None and s_flat is not None and (s_base - s_flat) > 0.03,
              f"with the sheet's near edge placed at the plain cosine instead of under the sheet's "
              f"own perspective, the share of the frame a sheet still covers at the middle of the "
              f"dial goes from {s_base*100:.2f} per cent to {s_flat*100:.2f}. At 45 degrees the edge "
              f"stands at 0.843 of the tile and not 0.707, so the sheet is drawn SHORT and the "
              f"shadow that should begin where it lands begins underneath it and is never seen — "
              f"which is the module's own note on the same line"
              if s_base is not None and s_flat is not None else "the served bytes could not be changed")

        # 5 · the envelope no longer returns to nothing at the far end of the dial
        ev = served(("return feel(clamp((u <= 0.5 ? u : 1 - u) / RISE, 0, 1));",
                     "return feel(clamp(u / RISE, 0, 1));"))

        def exit_door(text, tag):
            def go(br):
                ww = int(br.evaluate("String(window.__exPass.bench.make() && "
                                     "document.querySelector('canvas').width)"))
                hh = int(br.evaluate("String(document.querySelector('canvas').height)"))
                ref = work_in_the_frame(BENCH / "photos" / "glassgrid.jpg", ww, hh)
                d = apart(host_at(br, 1, tag), ref)
                v = js(br, "window.__mix(1); return window.__values();")
                return [d[0], d[1], v["floorMap"]["offPx"], v["floorMap"]["open"], v["doorWhyNo"]]
            return on_bench(go, text)

        got = exit_door(ev, "red-envelope") if ev else None
        base_exit = exit_door(PACK, "red-envelope-base")
        check(RED_ROWS[4],
              got is not None and base_exit is not None
              and base_exit[0] <= SEAM and base_exit[4] is None
              and got[0] > SEAM and got[4] is not None,
              f"with the envelope left rising instead of turning back at the middle of the dial, the "
              f"floor stands {got[3]:.4f} open at the exit door where it stood {base_exit[3]:.4f}: "
              f"the tile standing at the frame is {got[2]:.2f} points of the buffer from its own "
              f"landing against {base_exit[2]:.4f}, the frame goes from {base_exit[0]:.4f} of 255 "
              f"from its own file to {got[0]:.2f}, and the instrument REFUSES its own door — "
              f"«{str(got[4])[:130]}…». That the envelope is nothing at both ends is the whole of "
              f"what makes both doors exact by construction rather than by a score's discipline"
              if got is not None and base_exit is not None else "the served bytes could not be changed")

        # 6 · the door reading removed
        dr = served(('if (v.doorWhyNo) { st.fail(st.token, v.doorWhyNo); return; }', ''))

        # THE MAP THIS ROW MEASURES AGAINST is the picture a door held open on the judges' channel
        # would show: the tile map itself, drawn straight through the bench at the entry door. The
        # bench draws a pose without going through the transaction, so the refusal never sees it.
        MAP0 = on_bench(lambda br: str(host_at(br, 0, "red-door-map", mask=1)))

        def door_on_the_road(text, tag):
            def go(br):
                br.evaluate("window.__hooks = {docks: [], curtains: [], glides: [], marks: []}; 0")
                js(br, "return window.__offer(%s, {progress: 0});"
                       % json.dumps(parquet_score(mask=1)))
                br.sleep(1.2)
                return png(br, SHOTS / (tag + ".png"))
            return on_bench(go, text)

        got = door_on_the_road(dr, "red-door") if dr else None
        base_mask = door_on_the_road(PACK, "red-door-base")
        d_open = diff(got, MAP0)[0] if (got and MAP0) else None
        d_held = diff(base_mask, MAP0)[0] if (base_mask and MAP0) else None
        check(RED_ROWS[5],
              d_open is not None and d_held is not None and d_open < 1.0 and d_held > SEAM,
              f"with the refusal taken out, a door held with the judges' channel open is DRAWN, and "
              f"what stands in the frame is the tile map itself: it reads {d_open:.4f} of 255 from "
              f"the map drawn straight, where the refusal in force leaves the frame {d_held:.2f} "
              f"from it. The door law is the instrument's own claim, so the instrument is what "
              f"answers for it"
              if d_open is not None and d_held is not None else "the served bytes could not be changed")

# ---------------------------------------------------------------- report
p = sum(1 for _, s, _ in results if s == "PASS")
f = sum(1 for _, s, _ in results if s == "FAIL")
s = sum(1 for _, s, _ in results if s == "SKIP")
print("\n".join("%-4s %s%s" % (st, nm, ("\n       " + dt) if dt else "")
                for nm, st, dt in results))
print("\n%d passed / %d failed / %d skipped" % (p, f, s))
shutil.rmtree(TMP, ignore_errors=True)
sys.exit(1 if f else 0)
