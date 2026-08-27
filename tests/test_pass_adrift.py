#!/usr/bin/env python3
"""PASS-API-V1 — the adrift instrument on the host's frame.
Run: python3 tests/test_pass_adrift.py

Root: his word 2026-08-14 08:39 — continue the effect farm, and integrate only green conforming
instruments. This instrument answers the 570 declined pairs whose pivot needs a cut on named
regions, and it publishes CELL CONTENT, the one structural level no landed instrument occupies.
docs/design/PASS-API-V1.md §7 (GPU and resources), §8 (the manifest) and §9's conformance rows 7, 9,
10, 13, 14, 15, 16 and 22 are what this file makes real, together with §7's coverage law of 12:40 and
its per-instrument specification in docs/design/COVERAGE.md. The lifecycle rows stay in
tests/test_pass_api.py and are untouched.

WHAT IS COMPARED, AND AGAINST WHAT.

  The doors. At the dial's two ends one whole work stands. Each is measured against ITS OWN FILE —
  the picture cover-fitted into the frame and pulled in by the headroom the drag needs (the module's
  own ZOOM of 1.17) — inside the project's seam threshold of 6 of 255.

  The two roads, on the silhouettes. The lab module fills the place a thing has left with a
  pyramid-inpainted ground plate carried in two extra textures; this port publishes that place as its
  own absence and lets the cue beneath draw it, which is the coverage law read on the same question.
  So the two roads draw the same picture wherever this instrument carries matter and differ exactly
  where it carries none. What is compared point for point is therefore the JUDGES' FRAME — the two
  silhouettes as colour, which the module already carries for reading a law off the picture. That
  frame holds no ground at all, so a difference in it is a difference in the mathematics: the travel,
  the turn, the shrink, the two measured thresholds, the response curves and the seating of each
  measured place. The doors are compared as pictures as well, since the plates are invisible there.

  The coverage. Measured on the host's own composition road rather than declared: the same instant is
  photographed with the instrument alone and with the woven instrument standing under it, and the
  share of the frame where the two differ is the absence it published. At both doors that share is
  zero and the door stands whole in the stack.

  No empty frame. The module asks its own context to preserve the drawing buffer (adrift.js:661) and
  §7 refuses that. The flag stood in for a redraw, so the rows below sample the pass at seven instants
  and once across a change of viewport, and each frame has to stand as a picture.

  The lab module is READ ONLY. It stands untracked in the tlvphotos worktree, so the manifest names
  no commit for it and a row weighs the file against the digest the manifest carries instead. Absent,
  every browser row here is a pinned SKIP that names the missing path — never a silent pass.
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

# The lab module lives in the MAIN tlvphotos worktree rather than the immersive one the three landed
# suites read: adrift.js stands only there, and untracked, on the day of this port.
LAB = Path(os.environ.get("TLVPHOTOS_ROOT", "/Users/sashaabramovich/tlvphotos")) / "lab"
PHOTOS = [LAB / "photos" / "towers.jpg", LAB / "photos" / "glassgrid.jpg"]
MODULE = LAB / "effects" / "adrift.js"

SITE_URL = "https://synth.example.com"
VW, VH = 390, 844          # the phone frame lab/carrier-check.py measures on
CLOCK = 7.0                # the second the comparison holds at, as the carrier's own check does
SEAM = 6.0                 # the project's seam threshold, 6 of 255 (TRANSITION-STAGE-V0 §1)
SAME = 1.5                 # two roads of one frame: the carrier check's own bar
FAR = 40.0                 # further than this from a file and it is a different work
BACKGROUND = (0x08, 0x08, 0x0a)
SPREAD = 10.0

SHOTS = ROOT / "tests" / "captures" / "pass-adrift"

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


DIE = 4.91016            # the die lab/data/scores' own weave score carries, so every suite rolls one
DURATION_MS = 6500
WITHIN_MS = 500


def _static(v):
    return {"op": "static", "value": v}


def adrift_cue(handles, stack=0, levels_own=None, **statics):
    """The cue, with a track for every one of the twenty-eight handles (§4.4b).

    `handles` is the record the fixture read off the lab module and the measurement script — the
    pair's own measured places, ground colours, thresholds, maxima, void shares and horizons. It is
    read out of the bench rather than written here a second time, so one set of numbers stands
    behind both roads.
    """
    P = dict(handles)
    P.update(statics)
    P["seed"] = DIE
    nodes = {"a-mix": {"source": "progress"}, "a-clock": {"source": "time"}}
    tracks = {"mix": {"node": "a-mix"}, "clock": {"node": "a-clock"}}
    for k, v in P.items():
        nodes["a-" + k] = _static(v)
        tracks[k] = {"node": "a-" + k}
    return {
        "id": "adrift-main", "instrument": {"id": "adrift", "api": 1},
        "voice": "letter", "roles": ["disassembly", "mystery", "assembly"],
        "levels": ["SURFACE", "CELL CONTENT"],
        "levelOwnership": levels_own or {"SURFACE": "owns", "CELL CONTENT": "owns"},
        "window": [0, DURATION_MS / 1000.0], "works": ["a", "b"], "stack": stack,
        "cameraAuthority": "stage",
        "doors": {"in": {"handle": "mix", "value": 0, "measured": True},
                  "out": {"handle": "mix", "value": 1, "measured": True}},
        "nodes": nodes, "tracks": tracks,
        "resources": {"textures": 0, "textureSlots": 2, "framebuffers": 0, "pingPong": 0,
                      "programs": 1, "passes": 1, "bytesEstimate": 0, "variant": "standard"},
    }


def weave_cue():
    """THE GROUND AT STACK 0. The woven instrument partitions the frame between its two ribbon sets
    and writes no coverage, so it is what a voice publishing an absence is meant to be played over
    (COVERAGE.md §2.2, and the placement rule §7 states)."""
    P = {"strips": 28, "axis": 2, "speed": 1, "seed": DIE, "nMul": 1, "press": 1}
    nodes = {"w-mix": {"source": "progress"}, "w-clock": {"source": "time"}}
    tracks = {"mix": {"node": "w-mix"}, "clock": {"node": "w-clock"}}
    for k, v in P.items():
        nodes["w-" + k] = _static(v)
        tracks[k] = {"node": "w-" + k}
    return {
        "id": "under", "instrument": {"id": "weave", "api": 1},
        "voice": "accompaniment", "roles": ["surface", "breath"],
        "levels": ["SURFACE", "CELL"],
        "levelOwnership": {"SURFACE": "owns", "CELL": "owns"},
        "window": [0, DURATION_MS / 1000.0], "works": ["a", "b"], "stack": 0,
        "cameraAuthority": "stage",
        "doors": {"in": {"handle": "mix", "value": 0, "measured": True},
                  "out": {"handle": "mix", "value": 1, "measured": True}},
        "nodes": nodes, "tracks": tracks,
        "resources": {"textures": 0, "textureSlots": 2, "framebuffers": 0, "pingPong": 0,
                      "programs": 1, "passes": 1, "bytesEstimate": 0, "variant": "standard"},
    }


def adrift_score(handles, under=False, **statics):
    cues = [adrift_cue(handles, stack=1 if under else 0,
                       levels_own={"SURFACE": "accompanies:under", "CELL CONTENT": "owns"}
                       if under else None, **statics)]
    if under:
        cues = [weave_cue()] + cues
    res = {"textures": 0, "textureSlots": 2, "framebuffers": 0, "pingPong": 0, "programs": 1,
           "passes": 1, "bytesEstimate": 0}
    return {
        "schema": 2,
        "intent": "one work's thing leaves alone across an emptiness that stays, the emptiness "
                  "itself then changes hands along a measured front, and the other work's thing "
                  "arrives out of the far side and settles into its own measured place "
                  "(lab/effects/adrift.js:7-13, its own header)",
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
        "provenance": {"source": "lab/effects/adrift.js's own declared defaults and constants, with "
                                 "the pair's measurements taken by lab/step1-motifs.py's measure()",
                       "measuredAt": None, "by": "tests/test_pass_adrift.py"},
    }


# ---------------------------------------------------------------- bake once
build_site.SITE_CONFIG = dict(build_site.SITE_CONFIG)
build_site.SITE_CONFIG["pass"] = {"visualLayer": "pass", "diagnostics": "on"}

TMP = Path(tempfile.mkdtemp(prefix="synth_passadrift_"))
build_site.OUT = TMP
build_site.build(SITE_URL)
LAYER = (TMP / "pass-layer.js").read_text(encoding="utf-8")
# THE INSTRUMENT'S OWN BUILT FILE — the real artifact a visitor is served, comments stripped. Since
# every instrument travels alone, the whole of this file is this instrument and nothing else.
PACK = (TMP / "pass-inst-adrift.js").read_text(encoding="utf-8")
REGION = PACK
SOURCE = ROOT / "engine" / "assets" / "pass-inst-adrift.js"
# The file as it stands in the tree, comments and all: the rows about what this instrument DECLARES
# read the built artifact, and the rows about what it SAYS read the source it is built from.
SOURCE_TEXT = SOURCE.read_text(encoding="utf-8")

# ---------------------------------------------------------------- string rows

OWNED = ["createElement", "getContext", "requestAnimationFrame", "addEventListener",
         "performance.now", "Date.now", "new Image", "setTimeout", "setInterval"]
held = [s for s in OWNED if s in REGION]
check("PASS-ADRIFT the instrument creates no context, no canvas, no loop and no listener",
      not held,
      "§1.2's fence, read against the instrument's own region of the file: none of the nine ways of "
      "owning hardware appears there, so the module's two canvases, its WebGL 1 context, its frame "
      "loop and its resize observer all stayed in the lab"
      if not held else "the instrument's region holds " + ", ".join(held))

HANDLES = ["mix", "clock", "flight", "horizon", "grain", "shrink", "seed", "shade", "travel", "mask",
           "homeAx", "homeAy", "homeBx", "homeBy", "voidAr", "voidAg", "voidAb",
           "voidBr", "voidBg", "voidBb", "thrA", "thrB", "maxA", "maxB",
           "voidShareA", "voidShareB", "seamA", "seamB", "presence"]
absent = [h for h in HANDLES if ("%s: { min" % h) not in REGION]
check("PASS-ADRIFT every handle the instrument publishes is a handle a score can drive",
      not absent,
      "§4.4b: twenty-eight handles. Ten carry the module's own dial, clock, params, die and judge "
      "channels; the other eighteen carry the pair's own measurements, which the module reads out of "
      "lab/data/motifs.json and off the two files at build and which this file may not read at all"
      if not absent else "these are published nowhere: " + ", ".join(absent))

check("PASS-ADRIFT the grain's drift reads the handed-down second and no clock of its own",
      "(st.reduced ? 0 : st.t) * 0.09" in REGION and "t: h.clock" in REGION,
      "adrift.js:854 read `t`, its own accumulated frame time; here it is the `clock` handle, which "
      "is what makes the seeded repeat below mean anything")

check("PASS-ADRIFT the manifest leaves the drawing buffer unpreserved",
      "gl: { preserveDrawingBuffer: false }" in REGION,
      "the module asks its own context for a preserved buffer (adrift.js:661) and §7 refuses a "
      "manifest that asks for it; the redraw it stood in for is the host's own frame loop")

LABTXT = MODULE.read_text(encoding="utf-8") if MODULE.exists() else ""

check("PASS-ADRIFT the shader carries no version header of its own",
      "#version" not in REGION and bool(LABTXT) and "#version" not in LABTXT,
      "so the host's translator stamps the one header this shader needs and no second one arrives")


def numbers(text, pattern):
    m = re.search(pattern, text)
    return [float(x) for x in re.findall(r"-?\d+\.?\d*", m.group(1))] if m else []


lab_mix = numbers(LABTXT, r"FEEL_MIX = \[([^\]]+)\]")
port_mix = numbers(REGION, r"FEEL_MIX = \[([^\]]+)\]")
lab_grain = numbers(LABTXT, r"var FEEL_GRAIN = \[([^\]]+)\]")
port_grain = numbers(REGION, r"var FEEL_GRAIN = \[([^\]]+)\]")
check("PASS-ADRIFT both response curves are carried digit for digit out of the lab module",
      len(lab_mix) == 21 and lab_mix == port_mix and len(lab_grain) == 21 and lab_grain == port_grain
      and "FEEL_D0 = 0.05" in REGION and "d0: 0.05" in LABTXT,
      f"the hand's own table at twenty-one shares ({len(port_mix)} numbers matched, half the change "
      f"standing at {port_mix[10] if len(port_mix) > 10 else None}) and the grain's table fitted on "
      f"the geometric ladder ({len(port_grain)} matched); the three handles the module measured as "
      f"already even carry no table here either, which is the module's own assertion rather than an "
      f"empty cell (adrift.js:360-364)")

# Every constant the picture stands on, read out of the lab module and out of the built file.
CONSTANTS = [
    ("DEPART = 0.47, ARRIVE = 0.53", "DEPART = 0.47, ARRIVE = 0.53",
     "the first thing is wholly gone by 0.47 and the second begins at 0.53, so six hundredths of the "
     "hand hold an emptiness belonging to neither work"),
    ("FRONT_FROM = 0.14, FRONT_TO = 0.86", "FRONT_FROM = 0.14, FRONT_TO = 0.86",
     "the field changes hands across the middle five and a half tenths"),
    ("FLIGHT_OF_VOID = 1.15", "FLIGHT_OF_VOID = 1.15",
     "how far a thing may travel, as a multiple of the pair's own smaller void share"),
    ("TURN_MAX = 0.42", "TURN_MAX = 0.42", "radians a thing turns across its whole crossing"),
    ("SHRINK_MAX = 0.72", "SHRINK_MAX = 0.72", "how far down the shrink handle may take its size"),
    ("DRAG = 0.06", "DRAG = 0.06", "how far the two grounds are dragged past each other"),
    ("ZOOM = 1 + 2 * DRAG + 0.05", "ZOOM = 1 + 2 * DRAG + 0.05",
     "the crop that pays for the drag, derived rather than chosen"),
    ("GRAIN_MIN = 5, GRAIN_MAX = 33", "GRAIN_MIN = 5, GRAIN_MAX = 33",
     "how coarse the ground's own grain may be, in cells across the frame's height"),
    ("SHUT = 0.86, SHUT_PAST = 0.9", "SHUT = 0.86, SHUT_PAST = 0.9",
     "the threshold is walked a whole shut past the density nothing in the work reaches"),
    ("SHADOW_PX = 4.5", "SHADOW_PX = 4.5", "a contact shadow rather than a drop shadow"),
    ("SEAM_FULL = 0.13", "SEAM_FULL = 0.13",
     "the strongest waterline any work carrying this motif reaches"),
    ("JITTER = 0.20", "JITTER = 0.20", "a fifth of the dissolving order is the score's own die"),
    ("LADDER = 0.6", "LADDER = 0.6", "six parts the plain ladder against four parts the grain"),
    ("grainA * 3.4", "GRAIN_FINE = 3.4", "the fine grain that shatters the front rides at 3.4"),
    ("0.15 + 3.9 * horizon", "0.15 + 3.9 * horizon",
     "the fingers' depth, in cells: a clean waterline at one end and a band four cells deep at the "
     "other"),
    ("* 0.09", "* 0.09", "the grain's own drift rate"),
]
missing_const = [p for lab_p, p in ((a, b) for a, b, _ in CONSTANTS)
                 if lab_p not in LABTXT or p not in REGION]
check("PASS-ADRIFT every constant the picture stands on carries the module's own number",
      not missing_const and bool(LABTXT),
      "; ".join("%s — %s" % (p, why) for _, p, why in CONSTANTS) if not missing_const
      else "these differ between the lab module and the port: " + ", ".join(missing_const))

check("PASS-ADRIFT the host binds uniforms by declared name, never by position or a written list",
      "getUniformLocation(p, u.name)" in LAYER and "uHomeA" not in LAYER and "uVoidA" not in LAYER,
      "the lab carrier's draw call names one instrument's six uniforms; this instrument declares "
      "twenty-two, of which five are shared with the woven one. The host reads the manifest")

declared = set(re.findall(r'\{ name: "(u\w+)", type:', REGION))
spelled = set(re.findall(r'uniform \w+ (u\w+);', REGION))
check("PASS-ADRIFT the manifest's declared names and the shader's own names are one set",
      declared == spelled,
      f"{len(declared)} declared, {len(spelled)} spelled; "
      f"declared only: {sorted(declared - spelled)}; spelled only: {sorted(spelled - declared)}")

# ================================================================================================
# THE FOUR TEXTURES. The measurement the port was asked for, standing as a row.
# ================================================================================================
lab_samplers = set(re.findall(r"uniform sampler2D (u\w+);", LABTXT))
port_samplers = set(re.findall(r"uniform sampler2D (u\w+);", REGION))
port_sources = sorted(re.findall(r'type: "sampler2D", source: "(\w+)"', REGION))
check("PASS-ADRIFT the module's four source textures are carried by the host's two",
      lab_samplers == {"uA", "uB", "uGA", "uGB"} and port_samplers == {"uA", "uB"}
      and "uGA" not in REGION and "uGB" not in REGION
      and port_sources == ["textureA", "textureB"],
      f"the lab module binds {sorted(lab_samplers)}: the two works and, at units 2 and 3, each work's "
      f"pyramid-inpainted ground plate (adrift.js:907-908). This port binds {sorted(port_samplers)} "
      f"and asks the host for no third slot. The plates fill the place a thing has left, and under "
      f"§7's coverage law that place is exactly where this instrument carries no matter: it is "
      f"published as the absence the cue beneath fills. The rows below measure that the doors stand "
      f"whole without the plates and that the absence appears where the plates used to")

check("PASS-ADRIFT the coverage is declared, and it rests on a quantity the shader computes",
      "coverage: {" in REGION and "writes: true" in REGION
      and "clamp(covHome - cov)" in REGION
      and "float a = mix(1.0 - hole, 1.0, uMask) * uPresence;" in REGION
      and "gl_FragColor = vec4(col * a, a);" in REGION
      and "opacity" not in REGION
      and "presence: { min: 0, max: 1, def: 1" in REGION,
      "§8's coverage block and §7's law: the alpha is 1 minus the difference between the silhouette "
      "where the measurement put it and the silhouette where the thing stands now — the shader's own "
      "coverage read twice, at the same construction. The colour is handed over premultiplied, which "
      "is the form the host blends (`ONE, ONE_MINUS_SRC_ALPHA`, pass-layer.js). "
      "THIS ROW BANNED THE WORD `presence` OUTRIGHT UNTIL 2026-08-25, alongside `opacity`, and the "
      "entry-door contract retired half of that (docs/design/ENTRY-DOOR.md). The opacity ban stands "
      "and always will: the ladder's clause (a) hands a plan no tool to fade one whole layer against "
      "another. `presence` is the opposite thing — the reserved dry every instrument that may stand "
      "OVER another now declares, saying whether the voice is in the frame at all, resting at whole "
      "and standing at nothing at both doors of an upper voice. A voice cannot join a running "
      "picture without it, which is what the seam check's own door rows measure. So the row now "
      "requires the declaration it used to forbid, and forbids what it always forbade")

sha = hashlib.sha256(MODULE.read_bytes()).hexdigest() if MODULE.exists() else ""
declared_sha = (re.search(r'sha256: "([0-9a-f]{64})"', REGION) or [None, None])[1]
check("PASS-ADRIFT the provenance names the file the port was read from, and the file weighs to it",
      bool(sha) and sha == declared_sha and "commit: null" in REGION,
      f"the lab module stands untracked in the tlvphotos worktree on the day of this port, so no "
      f"commit is named and none is invented; the digest of the bytes the port was read from stands "
      f"in its place and the file still weighs to {sha[:16]}…")

# ---------------------------------------------------------------- browser rows

BROWSER_ROWS = [
    "PASS-ADRIFT §8     · the manifest carries every field the contract names, in its shape",
    "PASS-ADRIFT §8     · it publishes CELL CONTENT, and the reading is said to be derived",
    "PASS-ADRIFT row 7  · door 0 stands the departing work, measured against its own file",
    "PASS-ADRIFT row 7  · door 0 carries no trace of the arriving work",
    "PASS-ADRIFT row 7  · door 1 stands the arriving work, measured against its own file",
    "PASS-ADRIFT row 7  · door 1 carries no trace of the departing work",
    "PASS-ADRIFT the two roads agree on both silhouettes at all five poses",
    "PASS-ADRIFT the door the two ground plates cost the lab module, measured on both roads",
    "PASS-ADRIFT the two things never stand on one point of the frame",
    "PASS-ADRIFT §7     · the coverage: the absence is published where the plates used to fill",
    "PASS-ADRIFT §7     · both doors stand whole inside a stack, with a cue beneath them",
    "PASS-ADRIFT §7     · no empty frame at any sampled instant of the pass",
    "PASS-ADRIFT §7     · the frame after a change of viewport is drawn, not a kept buffer",
    "PASS-ADRIFT row 10 · a seeded run repeats to the pixel",
    "PASS-ADRIFT row 14 · textures, programmes and framebuffers return to their baseline after ten runs",
    "PASS-ADRIFT row 15 · the console stays clean",
    "PASS-ADRIFT row 22 · the census shows granted against declared, and neither overruns",
    "PASS-ADRIFT §7     · one canvas, one context, two source textures, one pass a frame",
    "PASS-ADRIFT §7     · a shader already at GLSL ES 3.00 receives no second version header",
    "PASS-ADRIFT the real transaction road: curtain up, one pass drawn, exactly one dock at the end",
    "PASS-ADRIFT row 9  · one camera authority through a real pass, and the pose rests on the arrival",
    "PASS-ADRIFT §4.4b  · the flight, the horizon, the grain and the shrink reach the PICTURE",
    "PASS-ADRIFT §4.4b  · the pair's own measurements reach the PICTURE",
    "PASS-ADRIFT row 16 · the captures are kept as evidence",
    "PASS-ADRIFT the door is read on the DRAWING BUFFER: the front's crossover, and the silhouette pair it stands on",
    "PASS-ADRIFT a door no whole cell can close is refused on the real road, and the visitor still lands",
    "PASS-ADRIFT §6     · at a door the plane hands the buffer over whole: the two roads draw one picture",
]

RED_ROWS = [
    "PASS-ADRIFT red-on-bug · the coverage removed: the absence stops being published",
    "PASS-ADRIFT red-on-bug · the absence read as a product: the doors stop standing whole in a stack",
    "PASS-ADRIFT red-on-bug · the seating removed: the measured places land where nothing measured them",
    "PASS-ADRIFT red-on-bug · the shut removed: a ghost of the departing thing stands at door 1",
    "PASS-ADRIFT red-on-bug · the door reading removed: a door the buffer cannot keep whole is drawn",
]

# THE MEASUREMENT THE GRAIN IS READ AGAINST AT A DOOR, published in the manifest. His 19:13 word,
# lifted to the class at 19:21: every geometric parameter names the measurement of the work it reads.
# The grain's own reading is the handover front's crossover against the margin the front leaves at a
# door, on the drawing buffer — and the handle says so where a composer can read it. The margin is
# the shader's own 0.03, so it is named once in script and once in the shader and never twice over.
check("PASS-ADRIFT the grain handle publishes the measurement its door is read against",
      'heldWholeAtADoor: { cells: DOOR_HOLD, readOn: "the drawing buffer",' in SOURCE_TEXT
      and 'reads: "grainRequest"' in SOURCE_TEXT
      and "var FRONT_MARGIN = 0.03;" in SOURCE_TEXT
      and "var DOOR_HOLD = 2;" in SOURCE_TEXT
      and '"  float margin = 0.03 + 0.5 * (grainW + fine);",' in SOURCE_TEXT,
      "the handle carries `applied.heldWholeAtADoor` — what is read, on which grid, how far the "
      "hold reaches and where the request stays on the record — beside its own range, and the "
      "margin the reading is held against is the very 0.03 the shader's own `margin` is built on")

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


def apart_share(p, q, bar=8):
    """The share of the frame where two captures stand more than `bar` of 255 apart on any channel.
    This is how much of the frame one of them left to whatever was underneath."""
    from PIL import Image, ImageChops
    a = Image.open(p).convert("RGB")
    c = Image.open(q).convert("RGB")
    if a.size != c.size:
        return 1.0
    d = ImageChops.difference(a, c).convert("L").point(lambda v: 255 if v > bar else 0)
    h = d.histogram()
    return h[255] / float(a.size[0] * a.size[1])


def standing(p):
    from PIL import Image, ImageChops, ImageStat
    a = Image.open(p).convert("RGB")
    flat = Image.new("RGB", a.size, BACKGROUND)
    st = ImageStat.Stat(ImageChops.difference(a, flat))
    own = ImageStat.Stat(a)
    return sum(st.mean) / 3.0, sum(own.stddev) / 3.0


def channel_mean(p, i):
    from PIL import ImageStat, Image
    return ImageStat.Stat(Image.open(p).convert("RGB")).mean[i]


def overlap(p):
    """The strongest point at which BOTH silhouettes stand, read off the judges' frame: the first
    thing is the red channel and the second the green, so the smaller of the two at a point is how
    much they share it."""
    from PIL import Image, ImageChops
    a = Image.open(p).convert("RGB")
    r, g, _ = a.split()
    both = ImageChops.darker(r, g)
    return max(v for v, n in zip(range(256), both.histogram()) if n)


def work_in_the_frame(src, w, h, zoom):
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
    """The bench's own served root: the BUILT pass-layer.js, the site's own settings record and the
    BUILT instrument files it names — the real artifacts, namespace applied and comments stripped —
    the lab module unchanged, the two photographs, and the page that stands the two roads of one
    frame side by side.

    A row proving a rule reds hands over a CHANGED instrument file and writes the record with the
    digest of the bytes actually served, which is what the build does. The source file on disk is
    never touched, so nothing has to be restored and no working tree can be left changed by a
    red-on-bug proof."""
    d = Path(tempfile.mkdtemp(prefix="synth_adriftbench_"))
    pack = PACK if pack_text is None else pack_text
    shutil.copy2(TMP / "pass-layer.js", d / "pass-layer.js")
    for _inst in sorted(TMP.glob("pass-inst-*.js")):
        shutil.copy2(_inst, d / _inst.name)
    (d / "pass-inst-adrift.js").write_text(pack, encoding="utf-8")
    record = json.loads((TMP / "config.json").read_text(encoding="utf-8"))
    record["pass"]["instruments"]["adrift"]["digest"] = hashlib.sha256(
        pack.encode("utf-8")).hexdigest()
    (d / "config.json").write_text(json.dumps(record), encoding="utf-8")
    shutil.copy2(MODULE, d / "adrift.js")
    (d / "photos").mkdir()
    for p in PHOTOS:
        shutil.copy2(p, d / "photos" / p.name)
    shutil.copy2(ROOT / "tests" / "fixture_pass_adrift.html", d / "index.html")
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
            elif not js(br, "return !!window.__exPass.bench.manifest('adrift');"):
                why = js(br, "var e = window.__host.report().events.filter(function(x){"
                             "return x.name === 'manifest-refused';});"
                             "return e.length ? e[e.length - 1].why : null;")
                for r in BROWSER_ROWS:
                    check(r, False, "the host registered no «adrift» instrument: " + str(why))
            else:
                MEASURED = js(br, "return window.__measured();")
                HANDLES_MEASURED = MEASURED["handles"]
                SCORE = json.dumps(adrift_score(HANDLES_MEASURED))
                SCORE_UNDER = json.dumps(adrift_score(HANDLES_MEASURED, under=True))

                # ---- §8: the manifest, read off the registered instrument -----------------------
                m = js(br, "return window.__exPass.bench.manifest('adrift');")
                zoom = m["framings"]["0"]["coverCrop"]
                res = m["resources"]
                shape = (
                    m["id"] == "adrift" and m["api"] == 1 and m["arity"] == 2
                    and m["roles"] == ["disassembly", "mystery", "assembly"]
                    and sorted(m["params"]) == ["flight", "grain", "horizon", "shrink"]
                    and len(m["handles"]) == 29
                    and all(set(h) >= {"min", "max", "def"} for h in m["handles"].values())
                    and m["neutrals"] == {"a": 0, "b": 1}
                    and m["doors"]["in"]["handle"] == "mix" and m["doors"]["in"]["value"] == 0
                    and m["doors"]["out"]["handle"] == "mix" and m["doors"]["out"]["value"] == 1
                    and sorted(m["framings"]) == ["0", "1"]
                    and m["framings"]["0"] == m["framings"]["1"]
                    and abs(zoom - (1 + 2 * 0.06 + 0.05)) < 1e-12
                    and m["camera"] == {"needs": "none", "authority": "stage"}
                    and len(m["passes"]) == 1 and len(m["passes"][0]["uniforms"]) == 23
                    and sorted(res) == ["lean", "rich", "standard"]
                    and all("bytesEstimate" in res[v] and res[v]["programs"] == 1
                            and res[v]["passes"] == 1 and res[v]["textureSlots"] == 2
                            for v in res)
                    and m["capabilities"] == ["webgl2"] and m["decline"]
                    and m["coverage"]["writes"] is True and m["coverage"]["how"]
                    and m["provenance"]["labPath"] == "lab/effects/adrift.js"
                    and m["provenance"]["commit"] is None
                    and m["readiness"] == "production-ready"
                    and "adrift" in js(br, "return window.__host.report().registered;"))
                check(BROWSER_ROWS[0], shape,
                      f"twenty-eight handles, twenty-two uniforms in one pass, the crop {zoom} that "
                      f"the drag's headroom is paid for with, resources declared for three tiers "
                      f"with a byte estimate of {res['standard']['bytesEstimate']}, and a coverage "
                      f"block reading «{m['coverage']['how']}»")

                check(BROWSER_ROWS[1],
                      m["levels"] == ["SURFACE", "CELL CONTENT"]
                      and "CELL CONTENT" in m["levels"]
                      and "READ OFF THE MODULE'S OWN CONSTRUCTION" in
                      SOURCE.read_text(encoding="utf-8"),
                      f"levels={m['levels']}. Neither the vocabulary table nor module-contract.json "
                      f"carries a row for this module, so both are read off its own construction and "
                      f"said to be derived: the two things themselves are the content of a named "
                      f"region moving as a whole, which is CELL CONTENT and which no landed "
                      f"instrument publishes; the field of emptiness runs over the whole frame, "
                      f"which is SURFACE. TEXTURE is not claimed")

                br.evaluate("window.__clock(%r); 0" % CLOCK)
                br.sleep(0.9)

                # ---- the five poses, on the judges' frame and on the picture ---------------------
                pairs, doors = [], {}
                for name, v in (("door-0", 0.0), ("q1", 0.25), ("mid", 0.5),
                                ("q3", 0.75), ("door-1", 1.0)):
                    br.evaluate("window.__mix(%r); 0" % v)
                    br.sleep(0.6)
                    # the picture
                    br.evaluate("window.__mask(0); 0")
                    br.sleep(0.3)
                    br.evaluate("window.__hostDraw(); 0")
                    br.sleep(0.1)
                    br.evaluate("window.__show('host'); 0")
                    br.sleep(0.25)
                    ph = png(br, SHOTS / (name + "-host.png"))
                    br.evaluate("window.__show('module'); 0")
                    br.sleep(0.25)
                    pm = png(br, SHOTS / (name + "-module.png"))
                    doors[name] = (ph, pm)
                    # the judges' frame
                    br.evaluate("window.__mask(1); 0")
                    br.sleep(0.3)
                    br.evaluate("window.__hostDraw(); 0")
                    br.sleep(0.1)
                    br.evaluate("window.__show('host'); 0")
                    br.sleep(0.25)
                    mh = png(br, SHOTS / (name + "-mask-host.png"))
                    br.evaluate("window.__show('module'); 0")
                    br.sleep(0.25)
                    mm = png(br, SHOTS / (name + "-mask-module.png"))
                    pairs.append((name, mh, mm))
                br.evaluate("window.__mask(0); window.__show('host'); 0")

                w = int(br.evaluate("String(window.__exPass.bench.make() && "
                                    "document.querySelector('canvas').width)"))
                h = int(br.evaluate("String(document.querySelector('canvas').height)"))
                towers = work_in_the_frame(BENCH / "photos" / "towers.jpg", w, h, zoom)
                glass = work_in_the_frame(BENCH / "photos" / "glassgrid.jpg", w, h, zoom)

                for i, (door, own, other, ownn, othern) in enumerate((
                        ("door-0", towers, glass, "towers.jpg", "glassgrid.jpg"),
                        ("door-1", glass, towers, "glassgrid.jpg", "towers.jpg"))):
                    a, amx = apart(doors[door][0], own)
                    check(BROWSER_ROWS[2 + i * 2], a <= SEAM,
                          f"{door} against {ownn}: mean {a:.4f} of 255 (threshold {SEAM}), worst "
                          f"channel {amx}. The plates the lab module carries are invisible here: at "
                          f"a door the thing stands where the measurement put it and covers the "
                          f"place the plate fills")
                    o, _ = apart(doors[door][0], other)
                    check(BROWSER_ROWS[3 + i * 2], o >= FAR,
                          f"{door} against {othern}: mean {o:.4f} of 255 (must exceed {FAR})")

                agree = [(name, ) + diff(mh, mm) for name, mh, mm in pairs]
                check(BROWSER_ROWS[6], all(mn <= SAME for _, mn, _ in agree),
                      "; ".join(f"{n}: mean {mn:.4f} of 255 (threshold {SAME}), worst channel {mx}"
                                for n, mn, mx in agree)
                      + ". The judges' frame holds the two silhouettes as colour and no ground at "
                        "all, so this is the travel, the turn, the shrink, the two measured "
                        "thresholds, the response curves and the seating of each measured place, "
                        "compared point for point against the lab module")

                # THE PLATE'S OWN COST AT THE DOOR, measured rather than argued. The lab module's
                # plate replaces a REGION and not a set of points — the silhouette grown by two cells
                # of its 512-cell plate, so that the pale grid lines inside a window frame, which fall
                # UNDER the density threshold, are filled too (adrift.js:509-521). At a door the
                # silhouette's own coverage covers the points above the threshold and no more, so
                # every filled point below it stands in the lab module's door and not in the file.
                # Its own card names this cost and asks a port to publish it. This port carries no
                # plate, so its door is the file.
                plate = []
                for n, own in (("door-0", towers), ("door-1", glass)):
                    plate.append((n, apart(doors[n][0], own)[0], apart(doors[n][1], own)[0]))
                check(BROWSER_ROWS[7],
                      all(p <= SEAM and lab > p for _, p, lab in plate),
                      "; ".join(f"{n}: this port stands {p:.4f} of 255 from its own file, the lab "
                                f"module {lab:.4f}" for n, p, lab in plate)
                      + f" (threshold {SEAM}). Dropping the two plates costs the doors nothing and "
                        f"returns what they cost: at a door the thing stands where the measurement "
                        f"put it, so the place a plate fills is the place the thing covers")

                worst = [(n, overlap(mh)) for n, mh, _ in pairs]
                check(BROWSER_ROWS[8], all(v == 0 for _, v in worst),
                      "; ".join(f"{n}: {v} of 255" for n, v in worst)
                      + ". The first thing is the red channel of the judges' frame and the second the "
                        "green; the strongest point at which both stand is the smaller of the two. "
                        "It is zero everywhere because the two travels are disjoint in the hand by "
                        "construction — 0.47 against 0.53 — rather than by a setting")

                # ---- §7: the coverage, measured on the host's own composition road ---------------
                # The same instant twice: the instrument alone, and the instrument with the woven one
                # standing under it. Where the two differ is where this instrument handed the frame
                # over to the cue beneath.
                shares = []
                for at in (0.0, 0.25, 0.5, 0.75, 1.0):
                    js(br, "return window.__offer(%s, {clock: 1.5, progress: %r});" % (SCORE, at))
                    br.sleep(0.6)
                    alone = png(br, SHOTS / ("cover-alone-%03d.png" % round(at * 100)))
                    br.evaluate("window.__cancel('coverage row'); 0")
                    idle(br)
                    js(br, "return window.__offer(%s, {clock: 1.5, progress: %r});"
                       % (SCORE_UNDER, at))
                    br.sleep(0.6)
                    over = png(br, SHOTS / ("cover-over-%03d.png" % round(at * 100)))
                    br.evaluate("window.__cancel('coverage row'); 0")
                    idle(br)
                    shares.append((at, apart_share(alone, over), diff(alone, over)[0]))
                mid_share = max(s for at, s, _ in shares if 0 < at < 1)
                door_share = max(s for at, s, _ in shares if at in (0.0, 1.0))
                check(BROWSER_ROWS[9],
                      mid_share > 0.01 and door_share < 0.005,
                      "; ".join(f"at {at}: {s * 100:.2f}% of the frame handed to the cue beneath "
                                f"(mean {mn:.2f} of 255)" for at, s, mn in shares)
                      + f". The absence stands where the lab module's two ground plates used to "
                        f"fill — the place each thing has left — and it closes to nothing at both "
                        f"doors, where the two silhouette readings are the same expression at the "
                        f"same arguments")

                # ---- the doors, standing inside a stack ------------------------------------------
                stack_doors = []
                for at, work, name in ((0.0, towers, "towers.jpg"), (1.0, glass, "glassgrid.jpg")):
                    js(br, "return window.__offer(%s, {clock: 1.5, progress: %r});"
                       % (SCORE_UNDER, at))
                    br.sleep(0.7)
                    p = png(br, SHOTS / ("stack-door-%03d.png" % round(at * 100)))
                    br.evaluate("window.__cancel('stack door row'); 0")
                    idle(br)
                    stack_doors.append((at, name) + apart(p, work))
                check(BROWSER_ROWS[10],
                      all(mn <= SEAM for _, _, mn, _ in stack_doors),
                      "; ".join(f"door {at} against {n}: mean {mn:.4f} of 255 (threshold {SEAM}), "
                                f"worst channel {mx}" for at, n, mn, mx in stack_doors)
                      + ". A cue that publishes an absence has to close it at its own doors, or the "
                        "voice beneath it shows through the door the visitor lands on")

                # ---- §7: no empty frame, and the redraw the preserved buffer stood in for --------
                empties = []
                for at in (0.0, 0.15, 0.3, 0.5, 0.7, 0.85, 1.0):
                    js(br, "return window.__offer(%s, {clock: 1.5, progress: %r});"
                       % (SCORE_UNDER, at))
                    br.sleep(0.5)
                    p = png(br, SHOTS / ("instant-%03d.png" % round(at * 100)))
                    empties.append((at, ) + standing(p))
                    br.evaluate("window.__cancel('instant sweep'); 0")
                    idle(br)
                check(BROWSER_ROWS[11],
                      all(d >= FAR and s >= SPREAD for _, d, s in empties),
                      "; ".join(f"at {at}: {d:.2f} from the background, spread {s:.2f}"
                                for at, d, s in empties)
                      + f" (bars: {FAR} and {SPREAD}); sampled on the score that gives this voice "
                        f"the ground it asks for")

                js(br, "return window.__offer(%s, {clock: 1.5, progress: 0.5});" % SCORE_UNDER)
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
                check(BROWSER_ROWS[12],
                      d >= FAR and s >= SPREAD and sized["pdb"] is False,
                      f"after the viewport moved to {VW - 80}x{VH - 120} the buffer reads "
                      f"{sized['buffer']} and the frame stands {d:.2f} from the background with a "
                      f"spread of {s:.2f}; the context keeps preserveDrawingBuffer={sized['pdb']}")

                # ---- the seeded repeat -----------------------------------------------------------
                # The viewport moved twice just above, so the stage is given time to stand at its own
                # size again before a run is photographed against a second run of itself.
                br.sleep(0.6)
                took = js(br, "return window.__offer(%s, {clock: 1.5, progress: 0.5});" % SCORE)
                br.sleep(1.2)
                first = png(br, SHOTS / "seeded-1.png")
                rep1 = js(br, "return window.__report();")
                br.evaluate("window.__cancel('between runs'); 0")
                idle(br)
                js(br, "return window.__offer(%s, {clock: 1.5, progress: 0.5});" % SCORE)
                br.sleep(1.2)
                second = png(br, SHOTS / "seeded-2.png")
                mn, mx = diff(first, second)
                check(BROWSER_ROWS[13], took["took"] and mn == 0.0 and mx == 0,
                      f"took={took['took']} two runs of one seeded score: mean {mn} worst channel "
                      f"{mx}. Every number the shader reads comes from a handle or from the second "
                      f"the host hands down, including the grain's own drift")

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
                check(BROWSER_ROWS[14], same,
                      f"before={base_c['textures']}/{base_c['programs']}/{base_c['framebuffers']} "
                      f"after ten runs={after['textures']}/{after['programs']}/{after['framebuffers']} "
                      f"(textures/programmes/framebuffers). Two textures, and the two ground plates "
                      f"the lab module uploads beside them are not among them")

                errs = json.loads(br.evaluate("JSON.stringify(window.__errs||[])"))
                check(BROWSER_ROWS[15], not errs, "; ".join(errs)[:200])

                # THE CENSUS IS READ ON A BENCH OF ITS OWN, and the reason is the programme cache:
                # it holds one entry per branch and outlives every transaction, so a session that has
                # already drawn the woven instrument under this one grants two programmes to a score
                # declaring one. A fresh bench draws this instrument and nothing else, which is the
                # only reading in which the count means what the declaration says.
                r = on_bench(lambda b2: (
                    js(b2, "return window.__offer(%s, {clock: 1.0, progress: 0.4});" % SCORE),
                    b2.sleep(0.8),
                    js(b2, "return window.__report();")["resources"])[-1])
                check(BROWSER_ROWS[16],
                      r and r["declared"] and r["over"] is False
                      and r["granted"]["textures"] == r["declared"]["textures"]
                      and r["granted"]["programs"] == r["declared"]["programs"] == 1
                      and r["granted"]["framebuffers"] == r["declared"]["framebuffers"]
                      and r["granted"]["bytes"] == r["declared"]["bytesEstimate"],
                      f"declared={r and r['declared']} granted={r and r['granted']}")

                js(br, "return window.__offer(%s, {clock: 1.0, progress: 0.4});" % SCORE)
                br.sleep(0.6)
                cen = js(br, "return window.__report();")["census"]
                check(BROWSER_ROWS[17],
                      cen["canvases"] == 1 and cen["contexts"] == 1 and cen["textures"] == 2
                      and cen["passesLastFrame"] == 1 and cen["framebuffers"] == 0
                      and cen["preserveDrawingBuffer"] is False,
                      f"census={cen}; the lab module's four textures and its second canvas are what "
                      f"this port does without")
                br.evaluate("window.__cancel('census row'); 0")
                idle(br)

                r = js(br, """
                  var m = window.__exPass.bench.manifest('adrift');
                  var plain = window.__exPass.bench.es3(m.passes[0].frag, false);
                  var already = window.__exPass.bench.es3('#version 300 es\\n' + m.passes[0].frag, false);
                  var count = function (s) { return s.split('#version').length - 1; };
                  return {source: count(m.passes[0].frag), stamped: count(plain),
                          untouched: count(already), head: plain.slice(0, 15)};
                """)
                check(BROWSER_ROWS[18],
                      r["source"] == 0 and r["stamped"] == 1 and r["untouched"] == 1
                      and r["head"].startswith("#version 300 es"),
                      f"the module's own shader carries {r['source']} headers, the translator leaves "
                      f"it with {r['stamped']}, and a source that already carries one comes back "
                      f"with {r['untouched']}")

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
                      f"handoffs={cam['handoffs']} tolerances={cam['tol']} — the construction moves "
                      f"no point of view, so the stage holds the camera for the whole pass")

                # ---- §4.4b: the handles reach the picture ----------------------------------------
                shot = {}
                for name, extra in (("base", {}), ("flight", {"flight": 0.0}),
                                    ("horizon", {"horizon": 0.05}), ("grain", {"grain": 0.05}),
                                    ("shrink", {"shrink": 1.0}),
                                    ("place", {"homeAx": 0.2, "homeAy": 0.2}),
                                    ("thr", {"thrA": HANDLES_MEASURED["thrA"] * 1.6})):
                    js(br, "return window.__offer(%s, {clock: 1.5, progress: 0.3});"
                       % json.dumps(adrift_score(HANDLES_MEASURED, under=True, **extra)))
                    br.sleep(0.7)
                    shot[name] = png(br, SHOTS / ("handle-" + name + ".png"))
                    br.evaluate("window.__cancel('handle row'); 0")
                    idle(br)
                moved = {k: diff(shot["base"], shot[k])
                         for k in ("flight", "horizon", "grain", "shrink", "place", "thr")}
                check(BROWSER_ROWS[21],
                      all(mn > SEAM for k, (mn, _) in moved.items()
                          if k in ("flight", "horizon", "grain", "shrink")),
                      "; ".join(f"{k} moves the frame by {mn:.4f} of 255 (worst channel {mx})"
                                for k, (mn, mx) in moved.items()
                                if k in ("flight", "horizon", "grain", "shrink"))
                      + f"; the seam threshold is {SEAM}")
                check(BROWSER_ROWS[22],
                      all(mn > SEAM for k, (mn, _) in moved.items() if k in ("place", "thr")),
                      "; ".join(f"{k} moves the frame by {mn:.4f} of 255 (worst channel {mx})"
                                for k, (mn, mx) in moved.items() if k in ("place", "thr"))
                      + ". A measurement that reached no pixel would be a handle the score drives "
                        "and the picture ignores, which is what §4.4b is about: the thing's measured "
                        "place and the density its silhouette is cut at are the two the whole motif "
                        "stands on")

                kept = sorted(p.name for p in SHOTS.glob("*.png"))
                check(BROWSER_ROWS[23],
                      len(kept) >= 30 and all((SHOTS / k).stat().st_size > 1000 for k in kept),
                      f"{len(kept)} captures under {SHOTS.relative_to(ROOT)}: the five poses on both "
                      f"roads as pictures and as judges' frames, the coverage pairs, the two doors "
                      f"in a stack, the seven sampled instants, the frame after a resize, the two "
                      f"seeded runs and the seven handle runs")

                # ---- THE GRID THE DOOR IS READ ON --------------------------------------------
                # Every door row above reads its door on the frame this suite runs at. The shader
                # samples on the DRAWING BUFFER — the CSS frame times the device ratio times the
                # host's own resolution step, which walks DOWN a ladder as a device struggles — and
                # the handover front crosses over inside a band HALF THE FIELD'S SLOPE PER BUFFER
                # POINT wide. Under it the front's own margin at a door is exactly 0.03 whatever the
                # grain does, so the two numbers are commensurable and the buffer is what decides
                # which wins. This row reads three things off the instrument's own record: the front
                # on a buffer that keeps the door, the front on a shorter one where it does not and
                # the coarser whole cell the instrument holds there, and the SILHOUETTE PAIR, which
                # stands at its door's own numbers on every grid and is published rather than feared.
                mh = js(br, "return window.__measured();")["handles"]

                def door_pose(mix=0, buf=None, **over):
                    p = dict(mh)
                    p.update({"mix": mix, "seed": DIE, "t": 0, "reduced": False,
                              "cssWidth": VW, "cssHeight": VH})
                    p.update(over)
                    if buf:
                        p["bufWidth"], p["bufHeight"] = int(buf[0]), int(buf[1])
                    return p

                def values_of(p):
                    return js(br, "return window.__exPass.bench.values('adrift', %s);"
                              % json.dumps(p))

                def per_door_ms(p, n=2000):
                    return js(br, "var p = %s, b = window.__exPass.bench;"
                                  "for (var i = 0; i < 400; i++) b.values('adrift', p);"
                                  "var t0 = performance.now();"
                                  "for (var j = 0; j < %d; j++) b.values('adrift', p);"
                                  "return {ms: (performance.now() - t0) / %d};"
                                  % (json.dumps(p), n, n))["ms"]

                # the finest ground this instrument publishes, with the deepest fingers: the pose
                # whose front asks most of a grid
                FINE = {"grain": 1.0, "horizon": 1.0}
                HELD_BUF = (133, 288)   # one whole cell short of that ground
                NO_BUF = (116, 252)     # and short of anything within reach
                on_css = values_of(door_pose(**FINE))
                on_buf = values_of(door_pose(buf=HELD_BUF, **FINE))
                applied = on_buf["grain"][0]
                on_no = values_of(door_pose(buf=NO_BUF, **FINE))
                away = values_of(door_pose(mix=0.5, buf=NO_BUF, **FINE))
                exitdoor = values_of(door_pose(mix=1, buf=NO_BUF, **FINE))
                sil = on_css["doorSilhouette"]
                sil_out = values_of(door_pose(mix=1))["doorSilhouette"]
                whole_ms = per_door_ms(door_pose(**FINE))
                held_ms = per_door_ms(door_pose(buf=HELD_BUF, **FINE))
                check(BROWSER_ROWS[24],
                      on_css["doorWhyNo"] is None and on_css["doorHeld"] is None
                      and on_css["grainCells"] == 0
                      and on_css["doorGrid"] == {"w": VW, "h": VH, "drawn": False}
                      and on_buf["doorWhyNo"] is None
                      and ("%d x %d buffer" % HELD_BUF) in (on_buf["doorHeld"] or "")
                      and on_buf["grainCells"] == 1 and applied == on_buf["grainRequest"] - 1
                      and on_no["doorWhyNo"] is not None
                      and "no whole cell stands within 2 cells" in on_no["doorWhyNo"]
                      and "the entry door leaks" in on_no["doorWhyNo"]
                      and "silhouette is punched through this door" in on_no["doorWhyNo"]
                      and "the exit door leaks" in (exitdoor["doorWhyNo"] or "")
                      and away["doorWhyNo"] is None and away["doorGrid"] is None
                      and sil == {"travelled": 0, "scale": 1, "turn": 0, "offThreshold": 0,
                                  "drag": 0}
                      and sil_out == {"travelled": 0, "scale": 1, "turn": 0, "offThreshold": 0,
                                      "drag": 0},
                      "on the %d x %d CSS frame the finest ground says «%s»; on a %d x %d buffer it "
                      "says «%s» and steps %g whole cell to %.2f cells, keeping the request at "
                      "%.2f; on a %d x %d one no whole cell reaches: «%s». Away from a door it "
                      "reads nothing at all (grid %s). The silhouette pair stands at its door's own "
                      "numbers on both doors — entry %s, exit %s — which is why the alpha is a "
                      "whole 1 there and the front is the only thing a buffer can spoil. One door "
                      "instant costs %.4f ms whole and %.4f ms held, on this machine."
                      % (VW, VH, on_css["doorHeld"] or "nothing", HELD_BUF[0], HELD_BUF[1],
                         on_buf["doorHeld"] or "nothing", on_buf["grainCells"], applied,
                         on_buf["grainRequest"], NO_BUF[0], NO_BUF[1], on_no["doorWhyNo"],
                         away["doorGrid"], sil, sil_out, whole_ms, held_ms))

                # ---- THE DOOR REFUSED ON THE REAL TRANSACTION ROAD ---------------------------
                # The row above reads the instrument's own record. This one puts real commands on
                # the real road at a real buffer: the frame is taken to one no whole cell within
                # reach can close, the pass is offered held at its entry door, and the host has to
                # land the visitor on the instrument's own reason rather than punch the arriving
                # work's silhouette through the door as transparency. The same frame, one step
                # taller, draws.
                def road(gen):
                    return js(br, "var r = window.__report(); return {state: r.state, "
                                  "drew: r.drew, buffer: r.census.buffer, "
                                  "refused: r.events.filter(function(e){ return e.gen === %d "
                                  "&& e.why && String(e.why).indexOf('door leaks') >= 0; })"
                                  ".map(function(e){ return e.name + ': ' + e.why; })};" % gen)

                FINE_SCORE = json.dumps(adrift_score(mh, grain=1.0, horizon=1.0))
                br.evaluate("window.__cancel('door road row'); 0")
                idle(br)
                br.set_viewport(137, 296)
                br.sleep(0.9)
                fine_gen = js(br, "return window.__offer(%s, {clock: 0, progress: 0});"
                              % FINE_SCORE)["gen"]
                br.sleep(1.1)
                played = road(fine_gen)
                br.evaluate("window.__cancel('door road row'); 0")
                idle(br)
                br.set_viewport(NO_BUF[0], NO_BUF[1])
                br.sleep(0.9)
                leak_gen = js(br, "return window.__offer(%s, {clock: 0, progress: 0});"
                              % FINE_SCORE)["gen"]
                br.sleep(1.2)
                leaked = road(leak_gen)
                br.evaluate("window.__cancel('door road row'); 0")
                idle(br)
                br.set_viewport(VW, VH)
                br.sleep(0.9)
                check(BROWSER_ROWS[25],
                      played["buffer"] == "137x296"
                      and played["state"] == "running" and played["drew"] == 1
                      and not played["refused"]
                      and leaked["buffer"] == "%dx%d" % NO_BUF
                      and len(leaked["refused"]) == 1 and leaked["state"] == "idle"
                      and "the entry door leaks" in leaked["refused"][0]
                      and ("%d x %d buffer" % NO_BUF) in leaked["refused"][0]
                      and "no whole cell stands within 2 cells" in leaked["refused"][0],
                      "on a 137 x 296 buffer the finest ground draws (%d cue, state %s, refused "
                      "%s); on the %d x %d buffer one step shorter the same score is refused with "
                      "«%s», on which the host lands the transaction (state %s, %d cue on its last "
                      "frame — the frames before the resize settled drew the door the taller grid "
                      "kept whole) and the walk's own glide carries the visitor"
                      % (played["drew"], played["state"], played["refused"] or "nothing",
                         NO_BUF[0], NO_BUF[1],
                         (leaked["refused"] or ["nothing refused"])[0], leaked["state"],
                         leaked["drew"]))

                # ---- §6: THE PLANE AT A DOOR -------------------------------------------------
                # Every door row above reads a door against its own FILE, and a file is a picture
                # taken outside the browser. This row reads the SAME door twice inside it — once
                # driven straight on the bench (`__hostDraw`, which binds the instrument's own
                # seating and photographs the drawing buffer as it stands) and once on the real
                # transaction road (`__offer` held at the entry door) — and asks the two to be one
                # picture, which is what the whole suite's «two roads of one frame» means.
                #
                # BESIDE IT, THE GEOMETRY THAT DECIDES THE DIFFERENCE. The host's canvas carries
                # two sizes: the DRAWING BUFFER, which is the only thing the instrument seated a
                # work into, and the CSS BOX the browser paints that buffer across. They are the
                # same rectangle only while the canvas covers the frame. A passage that boxes the
                # canvas to a second cover fit of the same source — pass-layer.js's `planeApply`,
                # from `planeAt`'s `coverCss` — stretches the buffer by cssWidth/bufferWidth and
                # lets the viewport crop what runs past its edges, so the work is cover-fitted
                # TWICE and the door is no longer the work. `drawPose`'s `seated()` is what those
                # two are supposed to cancel through: it fades the instrument's own fit toward the
                # identity as `plane.door` reaches 1. They cancel only where the plane agrees the
                # door is a door, so this row reads the box rather than trusting the fade.
                #
                # The two numbers are separated on purpose: the pixels say THAT the door moved and
                # the box says BY WHAT, so a repair cannot make the row green by moving the door
                # somewhere else that also happens to look right.
                br.evaluate("window.__cancel('plane at a door row'); 0")
                idle(br)
                br.evaluate("window.__clock(1.5); window.__mix(0); window.__mask(0); 0")
                br.sleep(0.6)
                br.evaluate("window.__hostDraw(); 0")
                br.sleep(0.1)
                br.evaluate("window.__show('host'); 0")
                br.sleep(0.3)
                bench_road = png(br, SHOTS / "plane-door-bench.png")
                js(br, "return window.__offer(%s, {clock: 1.5, progress: 0});" % SCORE)
                br.sleep(0.7)
                real_road = png(br, SHOTS / "plane-door-real.png")
                # The host raises its own canvas position:fixed above everything; the lab module's
                # stands absolute inside #moduleStage. The fixed one is the frame a visitor sees.
                box = js(br, "var cs = document.querySelectorAll('canvas'), k = null;"
                             "for (var i = 0; i < cs.length; i++) "
                             "  if (getComputedStyle(cs[i]).position === 'fixed') k = cs[i];"
                             "if (!k) return null;"
                             "var r = k.getBoundingClientRect();"
                             "return {bufW: k.width, bufH: k.height, x: r.x, y: r.y,"
                             " w: r.width, h: r.height, frameW: window.innerWidth,"
                             " frameH: window.innerHeight};")
                br.evaluate("window.__cancel('plane at a door row'); 0")
                idle(br)
                roads_mn, roads_mx = diff(bench_road, real_road)
                covers = bool(box) and (abs(box["x"]) <= 1 and abs(box["y"]) <= 1
                                        and abs(box["w"] - box["frameW"]) <= 1
                                        and abs(box["h"] - box["frameH"]) <= 1)
                stretch = (box["w"] / float(box["bufW"])) if box and box["bufW"] else 0.0
                check(BROWSER_ROWS[26],
                      roads_mn <= SAME and covers,
                      f"the entry door drawn on the bench road and on the real transaction road "
                      f"stand {roads_mn:.4f} of 255 apart (bar {SAME}), worst channel {roads_mx}. "
                      f"The host's canvas holds a {box and box['bufW']}x{box and box['bufH']} "
                      f"drawing buffer inside a CSS box of "
                      f"{box and round(box['w'], 1)}x{box and round(box['h'], 1)} at "
                      f"({box and round(box['x'], 1)}, {box and round(box['y'], 1)}), in a frame of "
                      f"{box and box['frameW']}x{box and box['frameH']}: the buffer is painted "
                      f"{stretch:.4f} of a CSS pixel wide per buffer point, and whatever runs past "
                      f"the frame's edges is cropped away by the viewport rather than drawn. At a "
                      f"door the plane has to hand the buffer over whole — the work is seated once, "
                      f"by the instrument, on the grid the instrument was told about")

    shutil.rmtree(BENCH, ignore_errors=True)

    # ================================================================================================
    # THE RED-ON-BUG PROOFS. Each reverts one rule this port states, in the artifact the browser
    # actually loads, and reads the number that moved. The pack served is changed and the host is
    # re-stamped with the digest of the bytes it is handed, which is what the build does; the file on
    # disk is never touched, so no working tree can be left changed by a proof.
    # ================================================================================================
    def measure_coverage(br, score, score_under, at=0.5):
        js(br, "return window.__offer(%s, {clock: 1.5, progress: %r});" % (score, at))
        br.sleep(0.6)
        alone = png(br, SHOTS / ("red-alone-%03d.png" % round(at * 100)))
        br.evaluate("window.__cancel('red'); 0")
        idle(br)
        js(br, "return window.__offer(%s, {clock: 1.5, progress: %r});" % (score_under, at))
        br.sleep(0.6)
        over = png(br, SHOTS / ("red-over-%03d.png" % round(at * 100)))
        br.evaluate("window.__cancel('red'); 0")
        idle(br)
        return apart_share(alone, over)

    def scores(br):
        h = js(br, "return window.__measured();")["handles"]
        return json.dumps(adrift_score(h)), json.dumps(adrift_score(h, under=True)), h

    if missing or not chrome_available():
        pass
    else:
        # ---- 1. the coverage removed -------------------------------------------------------------
        def red_one(br):
            s, su, _ = scores(br)
            return measure_coverage(br, s, su)

        base_share = on_bench(red_one)
        bug = PACK.replace("float a = mix(1.0 - hole, 1.0, uMask) * uPresence;", "float a = 1.0;", 1)
        bug_share = on_bench(red_one, pack_text=bug)
        check(RED_ROWS[0],
              bug != PACK and base_share is not None and bug_share is not None
              and base_share > 0.01 and bug_share < 0.005,
              f"with the coverage as it stands, {base_share * 100:.2f}% of the frame at the middle "
              f"of the hand is handed to the cue beneath. With the alpha reverted to the constant "
              f"1.0 — every instrument's frame before 2026-08-14 12:40 — that share falls to "
              f"{bug_share * 100:.2f}%: the cue beneath is drawn and seen at no instant, which is "
              f"the finding of 10:47 that the law came from")

        # ---- 2. the absence read as a product ----------------------------------------------------
        # Read where it is sharpest: the SHARE of the door the instrument hands to the cue beneath.
        # A door has to close the absence completely, and the mean over a whole frame hides a thin
        # figure standing open along every silhouette edge.
        def red_two(br):
            s, su, _ = scores(br)
            share = measure_coverage(br, s, su, at=0.0)
            w = int(br.evaluate("String(document.querySelector('canvas').width)"))
            hh = int(br.evaluate("String(document.querySelector('canvas').height)"))
            return share, apart(SHOTS / "red-over-000.png",
                                work_in_the_frame(PHOTOS[0], w, hh, 1.17))[0]

        base_door = on_bench(red_two)
        bug = PACK.replace(
            "float holeA = clamp(clamp(0.5 + hdA / (hgA * h), 0.0, 1.0) - covA, 0.0, 1.0);",
            "float holeA = clamp(0.5 + hdA / (hgA * h), 0.0, 1.0) * (1.0 - covA);", 1)
        bug_door = on_bench(red_two, pack_text=bug)
        check(RED_ROWS[1],
              bug != PACK and base_door and bug_door
              and base_door[0] < 0.0005 and bug_door[0] > 0.002
              and base_door[1] <= SEAM,
              f"the absence is the clamped DIFFERENCE of the two silhouette readings, so at a door, "
              f"where the two are the same expression at the same arguments, it is exactly zero: "
              f"{base_door[0] * 100:.3f}% of the door is handed to the cue beneath and the door "
              f"stands {base_door[1]:.4f} of 255 from its own file. Read as the product "
              f"covHome·(1 − cov) instead, the two readings disagree wherever the silhouette's own "
              f"coverage is neither 0 nor 1 — every edge of it — and the voice beneath shows through: "
              f"{bug_door[0] * 100:.3f}% of the door handed away, and the door {bug_door[1]:.4f} of "
              f"255 from its own file")

        # ---- 3. the seating removed --------------------------------------------------------------
        def red_three(br):
            br.evaluate("window.__clock(%r); window.__mix(0.25); window.__mask(1); 0" % CLOCK)
            br.sleep(0.9)
            br.evaluate("window.__hostDraw(); 0")
            br.sleep(0.2)
            br.evaluate("window.__show('host'); 0")
            br.sleep(0.3)
            a = png(br, SHOTS / "red-seat-host.png")
            br.evaluate("window.__show('module'); 0")
            br.sleep(0.3)
            b = png(br, SHOTS / "red-seat-module.png")
            return diff(a, b)

        base_seat = on_bench(red_three)
        bug = PACK.replace("vec2 outOf(vec2 q, vec4 f){ return (q - 0.5 - f.zw) / f.xy + 0.5; }",
                           "vec2 outOf(vec2 q, vec4 f){ return q; }", 1)
        bug_seat = on_bench(red_three, pack_text=bug)
        check(RED_ROWS[2],
              bug != PACK and base_seat and bug_seat
              and base_seat[0] <= SAME and bug_seat[0] > SAME,
              f"a measured place is a share of the FILE and the frame shows a cover-fit of that file "
              f"pulled in by the crop, so the place is carried through the same seating the shader "
              f"samples by. With `outOf` standing, the two roads agree on both silhouettes at "
              f"{base_seat[0]:.4f} of 255. With it reverted to reading the measurement straight, the "
              f"things stand where nothing measured them: {bug_seat[0]:.4f} of 255, worst channel "
              f"{bug_seat[1]}, against a bar of {SAME}")

        # ---- 4. the shut removed -----------------------------------------------------------------
        def red_four(br):
            br.evaluate("window.__clock(%r); window.__mix(1); window.__mask(1); 0" % CLOCK)
            br.sleep(0.9)
            br.evaluate("window.__hostDraw(); 0")
            br.sleep(0.2)
            br.evaluate("window.__show('host'); 0")
            br.sleep(0.3)
            return channel_mean(png(br, SHOTS / "red-shut.png"), 0)

        base_shut = on_bench(red_four)
        bug = PACK.replace("SHUT = 0.86, SHUT_PAST = 0.9", "SHUT = 0.86, SHUT_PAST = 0.0", 1)
        bug_shut = on_bench(red_four, pack_text=bug)
        check(RED_ROWS[3],
              bug != PACK and base_shut is not None and bug_shut is not None
              and base_shut == 0.0 and bug_shut > 0.0,
              f"the threshold is walked a whole shut past the density nothing in the work reaches, "
              f"because a coverage read as 0.5 + d/(g·fp) is linearised at the point and a threshold "
              f"a hundredth above the maximum still reads a fifth of a point of coverage. At door 1 "
              f"the departing thing's silhouette reads {base_shut:.4f} of 255 with the shut standing "
              f"and {bug_shut:.4f} of 255 with it removed — a ghost of a thing that left, over the "
              f"whole of the arriving work")

        # ---- 5. the door reading removed ---------------------------------------------------------
        # The lane's own rule, reverted in the artifact the browser loads: the front's margin is
        # taken past any crossover a grid can produce, which is exactly the instrument as it stood
        # before it read its doors at runtime — declaring both doors whole and never checking. The
        # number that moves is what the HOST is told on a buffer the front cannot keep whole: with
        # the reading standing the transaction is refused and lands; with it removed the door is
        # drawn, and nothing anywhere says the alpha it drew was not a whole 1.
        def red_five(br):
            mh5 = js(br, "return window.__measured();")["handles"]
            br.set_viewport(116, 252)
            br.sleep(0.9)
            gen = js(br, "return window.__offer(%s, {clock: 0, progress: 0});"
                     % json.dumps(adrift_score(mh5, grain=1.0, horizon=1.0)))["gen"]
            br.sleep(1.2)
            r = js(br, "var r = window.__report(); return {state: r.state, drew: r.drew, "
                       "buffer: r.census.buffer, refused: r.events.filter(function(e){ "
                       "return e.gen === %d && e.why "
                       "&& String(e.why).indexOf('door leaks') >= 0; }).length};" % gen)
            br.evaluate("window.__cancel('red five'); 0")
            return r

        base_door_read = on_bench(red_five)
        bug = PACK.replace("var FRONT_MARGIN = 0.03;", "var FRONT_MARGIN = 1e9;", 1)
        bug_door_read = on_bench(red_five, pack_text=bug)
        check(RED_ROWS[4],
              bug != PACK and base_door_read and bug_door_read
              and base_door_read["refused"] == 1 and base_door_read["state"] == "idle"
              and bug_door_read["refused"] == 0 and bug_door_read["state"] == "running",
              f"on the {base_door_read and base_door_read['buffer']} buffer this pose's front "
              f"crosses over inside the frame. With the reading standing the host is told so "
              f"({base_door_read and base_door_read['refused']} refusal, state "
              f"{base_door_read and base_door_read['state']}, "
              f"{base_door_read and base_door_read['drew']} cue drawn) and the walk's own glide "
              f"carries the visitor. With the front's margin taken past anything a grid can produce "
              f"— the instrument as it stood before it read its doors at runtime — the same command "
              f"draws the door instead ({bug_door_read and bug_door_read['refused']} refusals, "
              f"state {bug_door_read and bug_door_read['state']}, "
              f"{bug_door_read and bug_door_read['drew']} cue drawn), and nothing anywhere says the "
              f"alpha it laid down was not a whole 1")

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
