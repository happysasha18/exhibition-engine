#!/usr/bin/env python3
"""PASS-API-V1 — the grid-and-colour instrument on the host's frame.
Run: python3 tests/test_pass_grid-colour.py

Root: his word of 2026-08-18 18:39 — «дозалей чтобы все эффекты были в арсенале, со всеми ручками».
lab/effects/grid-colour.js is the richest module the lab holds: four cuts, two travelling
structures, two accompanying voices and a colour that is the material rather than a coat over it.
docs/design/PASS-API-V1.md §7 (GPU and resources), §8 (the manifest) and §9's conformance rows 7, 9,
10, 13, 14, 15, 16 and 22 are what this file makes real; the lifecycle rows stay in
tests/test_pass_api.py and are untouched.

WHAT IS COMPARED, AND AGAINST WHAT.

  The doors. At the dial's two ends one whole work stands. Each is measured against ITS OWN FILE —
  the picture cover-fitted into the frame, which is the framing this instrument publishes at both
  ends — inside the project's seam threshold of 6 of 255. A door that carried a ten-thousandth of
  the other photograph would fail this, which is the point of it. Both doors are read on all four
  cuts, because a cut is what a door is made of here.

  The two roads. The lab module is a ONE-WORK module: a crossing plays it as two layers, the
  departing work's running `out` and the arriving work's running `in`. The fixture stands exactly
  those two layers on their own canvases and the host draws the same crossing in one pass, so the
  comparison is two roads of one frame rather than two guesses at one.

  AND THE ONE PLACE THE TWO ROADS ARE DRIVEN APART, said here rather than hidden. The module carries
  four measured constants for the far end of its own response curve, one per cut, and its own header
  names deriving them per frame as the honest next unit — «the module must DERIVE `live` from its
  own piece table at build time … instead of carrying four measured constants». The port derives it,
  which is what makes its far door exact by construction instead of by the module's own
  `if (hand >= 1) return;`. So:
    · on the strip and the tile cut at a frame where the module's own measured 0.525 already clears
      the picture, the two curves are the same curve and the two roads are compared at one HAND,
      inside the carrier check's own bar of 1.5 of 255;
    · on the ring cut the module's own 0.975 does not clear the frame's corners, so the two roads
      are stood at one RAW DIAL — each reached with its own road's hand — and compared inside the
      project's seam of 6 of 255, the palette gap the hand gap opens being reported with the row.

  The colour bands. The module measures a work's five colours on a grid of the file quantised to a
  colour cube; a shader has no build step and no histogram, so the port reads five colours off the
  work at five places of it. The two roads therefore cut different bands out of one photograph, and
  the row that stands for this cut asks what the CUT must be true of on its own road rather than
  pretending the two palettes agree.

  The lab tree is READ ONLY and is found at $TLVPHOTOS_LAB_ROOT, defaulting to the immersive
  worktree's lab. Absent, every browser row here is a pinned SKIP that names the missing path —
  never a silent pass.
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

LAB = Path(os.environ.get("TLVPHOTOS_LAB_ROOT", "/Users/sashaabramovich/tlvphotos-immersive/lab"))
PHOTOS = [Path("/Users/sashaabramovich/tlvphotos/lab/photos/towers.jpg"),
          Path("/Users/sashaabramovich/tlvphotos/lab/photos/glassgrid.jpg")]
MODULE = LAB / "effects" / "grid-colour.js"

SITE_URL = "https://synth.example.com"
VW, VH = 390, 844          # the phone frame lab/carrier-check.py measures on
# THE FRAME THE TWO ROADS ARE COMPARED ON. On a frame this shape the module's own measured far end
# of 0.525 already carries the last strip and the last tile out, so the port's derivation asks for
# nothing more and the two roads run one and the same arithmetic. The number is read rather than
# chosen: the row prints the derived far end beside the module's own constant.
AW, AH = 900, 600
CLOCK = 7.0                # the second handed down; this instrument spends none of it
SEAM = 6.0                 # the project's seam threshold, 6 of 255 (TRANSITION-STAGE-V0 §1)
SAME = 1.5                 # two roads of one frame: the carrier check's own bar
FAR = 40.0                 # further than this from a file and it is a different work
BACKGROUND = (0x05, 0x05, 0x07)   # this page's own ground, which shows where the cut is open
SPREAD = 10.0

SHOTS = ROOT / "tests" / "captures" / "pass-grid-colour"

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


# ---------------------------------------------------------------- the module's own response curve
# Carried here so this file can put the two roads at one RAW DIAL: the module reaches a raw dial
# through its own constant far end and the port through the one it derives on the frame it draws.
# Every number is the module's (grid-colour.js:236-241) and nothing here is fitted.
FEEL = {
    "stripes": {"live": 0.525, "c": 0.30, "k1": 0.2, "k2": 2.2},
    "rings":   {"live": 0.975, "c": 0.24, "k1": -0.6, "k2": 2.8},
    "tiles":   {"live": 0.525, "c": 0.28, "k1": -0.4, "k2": 2.4},
    "bands":   {"live": 0.550, "c": 0.32, "k1": 0.0, "k2": 3.2},
}
KINDS = ["stripes", "rings", "tiles", "bands"]


def feel_log(x, k):
    return x if abs(k) < 1e-6 else (math.exp(k * x) - 1) / (math.exp(k) - 1)


def feel_inv(kind, y):
    """The hand at which this kind's own curve stands at `y` — the module's `feel` read backwards."""
    F = FEEL[kind]
    y = min(1.0, max(0.0, y))
    if y <= F["c"]:
        if abs(F["k1"]) < 1e-6:
            return (y / F["c"]) / 2
        return math.log(1 + (y / F["c"]) * (math.exp(F["k1"]) - 1)) / F["k1"] / 2
    z = (y - F["c"]) / (1 - F["c"])
    if abs(F["k2"]) < 1e-6:
        return (z + 1) / 2
    return (math.log(1 + z * (math.exp(F["k2"]) - 1)) / F["k2"] + 1) / 2


# ---------------------------------------------------------------- the score this instrument plays
# AUTHORED HERE, and said to be authored here. lab/data/scores carries no per-pair score for this
# module, so everything below is either a number the module itself declares or a field the contract
# requires; nothing is measured in this file and nothing is invented as a measurement.
DURATION_MS = 3000
WITHIN_MS = 500

HANDLES = ["mix", "clock", "kindA", "kindB", "countFrom", "countTo", "angleFrom", "angleTo",
           "countBeatIn", "countBeatOut", "angleBeatIn", "angleBeatOut", "stagger", "lead",
           "colourPeriod", "colourPhase", "colourAmp", "lightPeriod", "lightPhase", "lightAmp",
           "arrival", "shade", "mask"]

# The base every handle row moves ONE step off. Both travelling structures travel, both voices
# sound, both beats are windows rather than the whole handle, and the arriving work is brought in
# by the CARRIED mode — the one of the charter's five this module knows — so it rides behind the
# departing work on the one line instead of hiding under it, and everything that belongs to it has
# somewhere to show.
BASE = {"kindA": 0, "kindB": 0, "countFrom": 6, "countTo": 18, "angleFrom": 0, "angleTo": 60,
        "countBeatIn": 0.1, "countBeatOut": 0.9, "angleBeatIn": 0.1, "angleBeatOut": 0.9,
        "stagger": 0.1, "lead": 0,
        "colourPeriod": 0.7, "colourPhase": 0.2, "colourAmp": 0.35,
        "lightPeriod": 0.9, "lightPhase": 0.3, "lightAmp": 0.35,
        "arrival": 1, "shade": 1, "mask": 0}


def grid_score(pair_a="a", pair_b="b", **statics):
    """The score, with a track for every one of the twenty-three handles (§4.4b)."""
    P = dict(BASE)
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
        "intent": "the first work comes apart along its own measured grid and leaves along its own "
                  "lines while its palette drains out of it; the second comes in along its own, "
                  "arriving grey and filling with colour a beat before its shapes land "
                  "(lab/effects/grid-colour.js:1-89, its own header)",
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
            "id": "grid-colour-main",
            "instrument": {"id": "grid-colour", "api": 1},
            "voice": "letter",
            "roles": ["disassembly", "mystery", "assembly"],
            "levels": ["CELL", "LIGHT-COLOUR"],
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
        "quality": {v: {"renderScale": None, "cues": {"grid-colour-main": {"resources": res[v]}}}
                    for v in ("lean", "standard", "rich")},
        "provenance": {"source": "lab/effects/grid-colour.js's own declared defaults and constants",
                       "measuredAt": None, "by": "tests/test_pass_grid-colour.py"},
    }


# ---------------------------------------------------------------- bake once
build_site.SITE_CONFIG = dict(build_site.SITE_CONFIG)
build_site.SITE_CONFIG["pass"] = {"visualLayer": "pass", "diagnostics": "on"}

TMP = Path(tempfile.mkdtemp(prefix="synth_passgrid_"))
build_site.OUT = TMP
build_site.build(SITE_URL)
LAYER = (TMP / "pass-layer.js").read_text(encoding="utf-8")
REGION = (TMP / "pass-inst-grid-colour.js").read_text(encoding="utf-8")

# ---------------------------------------------------------------- string rows

OWNED = ["createElement", "getContext", "requestAnimationFrame", "addEventListener",
         "performance.now", "Date.now", "new Image", "setTimeout", "setInterval"]
held = [s for s in OWNED if s in REGION]
check("PASS-GRID the instrument creates no context, no canvas, no loop and no listener",
      not held,
      "§1.2's fence, read against the instrument's own region of the built file: none of the nine "
      "ways of owning hardware appears there, so the module's two canvases per layer, its 2D "
      "context, its grey twin, its band surfaces and its draw-on-change all stayed in the lab"
      if not held else "the instrument's region holds " + ", ".join(held))

missing_handles = [h for h in HANDLES if ("%s: { min" % h) not in REGION]
check("PASS-GRID every handle the instrument publishes is a handle a score can drive",
      not missing_handles and len(HANDLES) == 23
      and "presence: { min: 0, max: 1, def: 1" in REGION,
      "§4.4b: twenty-three handles — the module's own two declared params (the cut, once per layer), "
      "the two structures the dial travels between with the beat each travels inside, the stagger, "
      "the palette's lead, the six fields of the two accompanying voices, the arrival mode, and the "
      "dial, the second and the two judges' channels"
      if not missing_handles else "these are not published: " + ", ".join(missing_handles))

check("PASS-GRID the manifest leaves the drawing buffer unpreserved",
      "gl: { preserveDrawingBuffer: false }" in REGION,
      "§7 refuses a manifest that asks for a preserved buffer; the module drew on a parameter "
      "change and on a resize and nothing else, and the host's own frame loop is what that stood "
      "in for")

check("PASS-GRID the shader carries no version header of its own",
      "#version" not in REGION and "#version" not in MODULE.read_text(encoding="utf-8"),
      "so the host's translator stamps the one header this shader needs and no second one arrives")

LABTXT = MODULE.read_text(encoding="utf-8")

# Each constant as the LAB module spells it and as the PORT spells it. A port that retyped any of
# them would differ here by a digit.
CONSTANTS = [
    ("var LEAD_IN = 0.15;", "var LEAD_IN = 0.15;",
     "how early the arriving palette is full, in dial"),
    ("var FALLBACK_COUNT = 24;", "var FALLBACK_COUNT = 24;",
     "the count a work whose record carries no measured slice hands over"),
    ("var BAND_COUNT = 5;", "const int BANDS = 5;",
     "how many colours make the bands cut — what a work's measured palette carries"),
    ("stripes: { live: 0.525, c: 0.30, k1: 0.2, k2: 2.2 }",
     "stripes: { live: 0.525, c: 0.30, k1: 0.2, k2: 2.2 }",
     "the strip cut's own measured response profile"),
    ("rings:   { live: 0.975, c: 0.24, k1: -0.6, k2: 2.8 }",
     "rings:   { live: 0.975, c: 0.24, k1: -0.6, k2: 2.8 }",
     "the ring cut's — one curve per kind, which is the module's own finding"),
    ("tiles:   { live: 0.525, c: 0.28, k1: -0.4, k2: 2.4 }",
     "tiles:   { live: 0.525, c: 0.28, k1: -0.4, k2: 2.4 }", "the tile cut's"),
    ("bands:   { live: 0.550, c: 0.32, k1: 0.0, k2: 3.2 }",
     "bands:   { live: 0.550, c: 0.32, k1: 0.0, k2: 3.2 }", "the colour cut's"),
    ("0.2126 * a[i] + 0.7152 * a[i + 1] + 0.0722 * a[i + 2]",
     "const vec3 LUMA = vec3(0.2126, 0.7152, 0.0722);",
     "the luminance the grey twin is written at"),
    ("4 * u * (1 - u)", "4 * u * (1 - u)",
     "the window that holds a voice to nothing at either door"),
]
missing_const = ([c for c, _, _ in CONSTANTS if c not in LABTXT]
                 + [c for _, c, _ in CONSTANTS if c not in REGION])
check("PASS-GRID every constant stands at the number the lab module gives it",
      not missing_const,
      "; ".join("%s — %s" % (c, why) for c, _, why in CONSTANTS) if not missing_const
      else "these differ: " + ", ".join(missing_const))

check("PASS-GRID the host binds uniforms by declared name, never by position or a written list",
      "getUniformLocation(p, u.name)" in LAYER and "gl.uniform4fv(U.uCutA" not in LAYER,
      "every one of this instrument's seventeen uniforms is bound from the manifest; the host holds "
      "no list of its names")

declared = set(re.findall(r'\{ name: "(u\w+)", type:', REGION))
spelled = set(re.findall(r'uniform \w+ (u\w+);', REGION))
check("PASS-GRID the manifest's declared names and the shader's own names are one set",
      declared == spelled and len(declared) == 18,
      f"{len(declared)} declared, {len(spelled)} spelled; "
      f"declared only: {sorted(declared - spelled)}; spelled only: {sorted(spelled - declared)}")

# WHAT IT CUTS ON AND WHAT IT SUITS — and neither of them a floor. His words of 2026-08-18 09:51,
# 09:53 and 10:15: any two photographs in the world get a crossing, and a measurement only ranks
# which genre suits. So `suits` may name what it READS and what a whole fit and a fit of nothing
# mean, and it may not carry a floor, a minimum, a threshold or a refusal.
FLOORS = ["floor:", "minimum:", "threshold:", "requires", "must read", "refuse"]
suits_txt = REGION[REGION.find("suits: {"):REGION.find("readiness:")] if "suits: {" in REGION else ""
floors_found = [w for w in FLOORS if w in suits_txt]
check("PASS-GRID the manifest publishes what it cuts on and what it suits, and the suit is a "
      "ranking rather than a floor",
      'cuts: ["strip", "ring", "tile", "band"]' in REGION
      and "suits: { reads:" in REGION and "structure.ownDevice.stepPx" in suits_txt
      and "structure.grid.periodPx" in suits_txt and not floors_found
      and "plays" in suits_txt and "ranks higher" in suits_txt,
      "four kinds, one per cut the module plays, all four in §8's own vocabulary; the suit reads "
      "each work's own lattice step and angle and the confidence they were recovered with, and it "
      "says in its own sentence that a fit of nothing still plays"
      if not floors_found else "the suit carries a floor: " + ", ".join(floors_found))

# ---------------------------------------------------------------- browser rows

BROWSER_ROWS = [
    "PASS-GRID §8     · the manifest carries every field the contract names, in its shape",
    "PASS-GRID row 7  · door 0 stands the departing work, measured against its own file",
    "PASS-GRID row 7  · door 0 carries no trace of the arriving work",
    "PASS-GRID row 7  · door 1 stands the arriving work, measured against its own file",
    "PASS-GRID row 7  · door 1 carries no trace of the departing work",
    "PASS-GRID row 7  · both doors stand whole on all four cuts",
    "PASS-GRID the two roads agree on the STRIP cut, where the module's own curve already clears",
    "PASS-GRID the two roads agree on the TILE cut, where the module's own curve already clears",
    "PASS-GRID the two roads agree on the RING cut at one raw dial, the derived far end apart",
    "PASS-GRID the BAND cut cuts the frame by the work's own colour, and the palette is the half "
    "that could not cross",
    "PASS-GRID §7     · no empty frame at any sampled instant of the pass",
    "PASS-GRID §7     · the frame after a change of viewport is drawn, not a kept buffer",
    "PASS-GRID row 10 · a seeded run repeats to the pixel",
    "PASS-GRID §4.4b  · every handle the manifest publishes reaches the picture",
    "PASS-GRID the real transaction road: curtain up, one pass drawn, exactly one dock at the end",
    "PASS-GRID row 9  · one camera authority through a real pass, and the pose rests on the arrival",
    "PASS-GRID row 14 · textures, programmes and framebuffers return to their baseline after ten runs",
    "PASS-GRID row 15 · the console stays clean",
    "PASS-GRID row 22 · the census shows granted against declared, and neither overruns",
    "PASS-GRID §7     · a manifest asking for a preserved drawing buffer is refused, with its reason",
    "PASS-GRID §7     · a uniform bound to a name the shader lacks is refused, with its reason",
    "PASS-GRID §7     · one canvas, one context, two source textures, one pass a frame",
    "PASS-GRID §7     · a shader already at GLSL ES 3.00 receives no second version header",
    "PASS-GRID the door is read on the DRAWING BUFFER, and the clearance is published",
    "PASS-GRID a door no dial can close is refused on the real road, and the visitor still lands",
    "PASS-GRID §7     · the coverage is published, and the frame is genuinely bare between the pieces",
    "PASS-GRID row 16 · the captures are kept as evidence",
    "PASS-GRID all four cuts play: strips, rings, tiles and the work's own colour areas each draw "
    "a different frame",
    "PASS-GRID the module's one law, measured on all four cuts: a piece is exactly out of the frame "
    "at dial 1 and no earlier",
]

RED_ROWS = [
    "PASS-GRID red-on-bug · the curve's far end reverted to the module's four constants: the exit "
    "door on the strip cut still stands the departing work",
    "PASS-GRID red-on-bug · a ring's reach reverted to one reach for all rings (the module's own "
    "12.08 regression): the arriving work is unreadable early in the dial",
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
    """How far a capture stands from this page's own flat ground, and how much spread it carries of
    its own. A frame that was never drawn is that ground and has neither."""
    from PIL import Image, ImageChops, ImageStat
    a = Image.open(p).convert("RGB")
    flat = Image.new("RGB", a.size, BACKGROUND)
    st = ImageStat.Stat(ImageChops.difference(a, flat))
    own = ImageStat.Stat(a)
    return sum(st.mean) / 3.0, sum(own.stddev) / 3.0


def bare_mask(p):
    """Which points of a frame no piece stands on, read as the page's own ground showing through.
    It is the CUT itself with the rasteriser taken out of it: no resampling, no grey twin, no
    filtering — only where the geometry put the pieces."""
    from PIL import Image
    im = Image.open(p).convert("RGB")
    d = im.load()
    w, h = im.size
    return [1 if (abs(d[x, y][0] - BACKGROUND[0]) + abs(d[x, y][1] - BACKGROUND[1])
                  + abs(d[x, y][2] - BACKGROUND[2])) < 24 else 0
            for y in range(h) for x in range(w)]


def geometry_apart(p, q):
    a, b = bare_mask(p), bare_mask(q)
    return sum(1 for x, y in zip(a, b) if x != y) / float(len(a))


def hairline_share(kind, count, w, h, spanU, radius):
    """How much of the frame the module's OWN HAIRLINE can account for. It grows every piece by one
    point at each edge so no seam opens between two clip paths (grid-colour.js: `a0 = k*step - 1;
    a1 = (k + 1) * step + 1`, and the same at every other cut), so the two roads may put a point on
    different sides of an edge along a band two points wide at every edge of the cut. This is that
    band's own share of the frame, taken with each edge at its longest — the frame's own diagonal
    for a straight cut, the circle's own circumference for a ring."""
    diag = math.hypot(w, h)
    if kind == "rings":
        step = radius / count
        return sum(2 * math.pi * (k * step) * 2 for k in range(int(count) + 2)) / (w * h)
    step = spanU / count
    edges = w / step + 1 + ((h / step + 1) if kind == "tiles" else 0)
    return edges * diag * 2 / (w * h)


def covered_share(p):
    """How much of the frame a piece stands on, read off the cut map's own third channel: the
    shader writes `cover` there, and the ground behind the canvas carries 7 of 255."""
    from PIL import Image
    a = Image.open(p).convert("RGB")
    b = list(a.getdata(2))
    return sum(1 for v in b if v >= 128) / float(len(b))


def layer_share(p):
    """How much of the frame each of the two layers stands on, read off the cut map. The shader
    writes WHICH layer owns a point in the first channel — half of it for the departing work, the
    whole of it for the arriving one — and whether anything stands there at all in the third, so a
    layer's own share is countable without the photographs being in the way."""
    from PIL import Image
    im = Image.open(p).convert("RGB")
    px = list(im.getdata())
    n = float(len(px))
    return (sum(1 for r, _, b in px if b >= 128 and 96 <= r <= 160) / n,
            sum(1 for r, _, b in px if b >= 128 and r > 160) / n)


def work_in_the_frame(src, w, h):
    """The work as the instrument seats it: the plain cover fit, which is the framing this
    instrument publishes at both doors."""
    from PIL import Image
    im = Image.open(src).convert("RGB")
    iw, ih = im.size
    fa, ia = w / float(h), iw / float(ih)
    sw, sh = (ih * fa, float(ih)) if ia > fa else (float(iw), iw / fa)
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
    """The bench's own served root: the BUILT pass-layer.js (the real artifact, namespace applied
    and comments stripped), the lab module unchanged, the photographs, and the page that stands the
    host's one pass beside the module's own two layers.

    A row proving a rule reds hands over a CHANGED instrument file and writes the site's own record
    with the digest of the bytes actually served, which is what the build does. The source file on
    disk is never touched, so nothing has to be restored and no working tree can be left changed by
    a red-on-bug proof."""
    d = Path(tempfile.mkdtemp(prefix="synth_gridbench_"))
    pack = REGION if pack_text is None else pack_text
    shutil.copy2(TMP / "pass-layer.js", d / "pass-layer.js")
    for _inst in sorted(TMP.glob("pass-inst-*.js")):
        shutil.copy2(_inst, d / _inst.name)
    (d / "pass-inst-grid-colour.js").write_text(pack, encoding="utf-8")
    record = json.loads((TMP / "config.json").read_text(encoding="utf-8"))
    record["pass"]["instruments"]["grid-colour"]["digest"] = hashlib.sha256(
        pack.encode("utf-8")).hexdigest()
    (d / "config.json").write_text(json.dumps(record), encoding="utf-8")
    shutil.copy2(MODULE, d / "grid-colour.js")
    (d / "photos").mkdir()
    for p in PHOTOS:
        shutil.copy2(p, d / "photos" / p.name)
    shutil.copy2(ROOT / "tests" / "fixture_pass_grid-colour.html", d / "index.html")
    return d


def ready(br, tries=80):
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


# The record both roads are set up from. Every field is a handle the manifest publishes.
def cfg(**over):
    c = {"kindA": 0, "kindB": 0, "countFrom": 8, "countTo": 8, "angleFrom": 0, "angleTo": 0,
         "countBeat": [0, 1], "angleBeat": [0, 1], "stagger": 0, "lead": 0.15,
         "colourPeriod": 0, "colourPhase": 0, "colourAmp": 0,
         "lightPeriod": 0, "lightPhase": 0, "lightAmp": 0,
         "arrival": 0, "shade": 1, "mask": 0, "pair": [0, 1]}
    c.update(over)
    return c


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
    SCORE_JSON = json.dumps(grid_score())
    with serve(BENCH) as base:
        with Browser(width=VW, height=VH) as br:
            br.navigate(base + "/index.html")
            if not ready(br):
                for r in BROWSER_ROWS:
                    check(r, False, "the bench never came up: "
                         + br.evaluate("JSON.stringify(window.__errs||[])"))
            elif not js(br, "return !!window.__exPass.bench.manifest('grid-colour');"):
                why = js(br, "var e = window.__host.report().events.filter(function(x){"
                             "return x.name === 'manifest-refused';});"
                             "return e.length ? e[e.length - 1].why : null;")
                for r in BROWSER_ROWS:
                    check(r, False, "the host registered no «grid-colour» instrument: " + str(why))
            else:
                # ---- §8: the manifest, read off the registered instrument -----------------------
                m = js(br, "return window.__exPass.bench.manifest('grid-colour');")
                res = m["resources"]
                shape = (
                    m["id"] == "grid-colour" and m["api"] == 1 and m["arity"] == 2
                    and m["roles"] == ["disassembly", "mystery", "assembly"]
                    and m["levels"] == ["CELL", "LIGHT-COLOUR"]
                    and m["cuts"] == ["strip", "ring", "tile", "band"]
                    and len(m["handles"]) == 24
                    and all(set(h) >= {"min", "max", "def"} for h in m["handles"].values())
                    and m["neutrals"] == {"a": 0, "b": 1}
                    and m["doors"]["in"]["handle"] == "mix" and m["doors"]["in"]["value"] == 0
                    and m["doors"]["out"]["handle"] == "mix" and m["doors"]["out"]["value"] == 1
                    and sorted(m["framings"]) == ["0", "1"]
                    and m["framings"]["0"] == {"coverCrop": 1}
                    and m["framings"]["1"] == {"coverCrop": 1}
                    and m["camera"] == {"needs": "none", "authority": "stage"}
                    and m["coverage"]["writes"] is True
                    and m["applied"]["flow"]["departing"] == "out"
                    and m["applied"]["flow"]["arriving"] == "in"
                    and len(m["passes"]) == 1 and len(m["passes"][0]["uniforms"]) == 18
                    and sorted(res) == ["lean", "rich", "standard"]
                    and all("bytesEstimate" in res[v] and res[v]["programs"] == 1
                            and res[v]["passes"] == 1 and res[v]["textureSlots"] == 2
                            for v in res)
                    and m["capabilities"] == ["webgl2"] and m["decline"]
                    and m["provenance"]["labPath"] == "lab/effects/grid-colour.js"
                    and m["provenance"]["commit"] == "5cf8968"
                    and m["suits"]["reads"] and m["suits"]["how"]
                    and m["readiness"] == "production-ready"
                    and "grid-colour" in js(br, "return window.__host.report().registered;"))
                check(BROWSER_ROWS[0], shape,
                      f"twenty-three handles, seventeen uniforms in one pass, the plain cover fit at "
                      f"both doors, four cuts declared, coverage written where the cut is open, the "
                      f"pair's own order spent on the module's `flow`, and the lab commit "
                      f"{m['provenance']['commit']}")

                br.evaluate("window.__show('host'); 0")
                js(br, "return window.__setup(%s);" % json.dumps(cfg()))
                br.sleep(0.5)
                w = int(br.evaluate("String(window.__exPass.bench.make() && "
                                    "document.querySelector('canvas').width)"))
                h = int(br.evaluate("String(document.querySelector('canvas').height)"))
                towers = work_in_the_frame(BENCH / "photos" / "towers.jpg", w, h)
                glass = work_in_the_frame(BENCH / "photos" / "glassgrid.jpg", w, h)

                # ---- the doors, on the strip cut ------------------------------------------------
                door_shot = {}
                for name, v in (("door-0", 0.0), ("door-1", 1.0)):
                    js(br, "return window.__hostDraw({mix: %r});" % v)
                    br.sleep(0.25)
                    door_shot[name] = png(br, SHOTS / (name + "-host.png"))
                for i, (door, own, other, ownn, othern) in enumerate((
                        ("door-0", towers, glass, "towers.jpg", "glassgrid.jpg"),
                        ("door-1", glass, towers, "glassgrid.jpg", "towers.jpg"))):
                    a, amx = apart(door_shot[door], own)
                    check(BROWSER_ROWS[1 + i * 2], a <= SEAM,
                          f"{door} against {ownn}: mean {a:.4f} of 255 (threshold {SEAM}), worst "
                          f"channel {amx}")
                    o, _ = apart(door_shot[door], other)
                    check(BROWSER_ROWS[2 + i * 2], o >= FAR,
                          f"{door} against {othern}: mean {o:.4f} of 255 (must exceed {FAR})")

                # ---- both doors on all four cuts ------------------------------------------------
                # A cut is what a door is made of here, so a door read on one cut says nothing about
                # the other three. Each is read on a travelling grid and a spread stagger, so the
                # far end of each kind's own curve is asked for the hardest case it has.
                cut_reads = []
                for ki, kn in enumerate(KINDS):
                    js(br, "return window.__setup(%s);"
                       % json.dumps(cfg(kindA=ki, kindB=ki, countFrom=5, countTo=13,
                                        angleFrom=0, angleTo=40, stagger=0.3)))
                    br.sleep(0.35)
                    row = []
                    for door, v, own, ownn in (("0", 0.0, towers, "towers.jpg"),
                                               ("1", 1.0, glass, "glassgrid.jpg")):
                        js(br, "return window.__hostDraw({mix: %r});" % v)
                        br.sleep(0.25)
                        p = png(br, SHOTS / ("cut-%s-door-%s.png" % (kn, door)))
                        mn, mx = apart(p, own)
                        row.append((door, ownn, mn, mx))
                    cut_reads.append((kn, row))
                check(BROWSER_ROWS[5],
                      all(mn <= SEAM for _, row in cut_reads for _, _, mn, _ in row),
                      "; ".join("%s door %s against %s: mean %.4f (worst channel %d)"
                                % (kn, d, o, mn, mx)
                                for kn, row in cut_reads for d, o, mn, mx in row)
                      + f" — threshold {SEAM}, each read on a grid travelling from 5 pieces to 13 "
                      f"and from upright to 40 degrees with the departures spread over 0.3 of the "
                      f"handle")

                # ---- all four cuts play, and each of them is its own cut -------------------------
                # A door is the same photograph whichever cut it was made of, so the rows above
                # cannot tell four cuts from one. This one stands them beside each other AWAY from a
                # door, where a cut is all there is to see: one count, one angle, one instant of the
                # handle, and nothing changed between the four but the kind. Four cuts drawing one
                # frame would be three kinds declared and never wired.
                cut_frames = {}
                for ki, kn in enumerate(KINDS):
                    js(br, "return window.__setup(%s);" % json.dumps(cfg(kindA=ki, kindB=ki)))
                    br.sleep(0.35)
                    js(br, "return window.__hostDraw({mix: 0.4});")
                    br.sleep(0.25)
                    cut_frames[kn] = png(br, SHOTS / ("plays-%s.png" % kn))
                plays = [(x, y, diff(cut_frames[x], cut_frames[y])[0])
                         for i, x in enumerate(KINDS) for y in KINDS[i + 1:]]
                check(BROWSER_ROWS[27],
                      all(m > SEAM for _, _, m in plays),
                      "at four tenths of the handle, on one count of eight and one upright angle: "
                      + "; ".join("%s against %s: %.2f of 255" % (x, y, m) for x, y, m in plays)
                      + f" — every one of the six pairs over the seam of {SEAM}, so the strips, the "
                      f"annuli about the middle, the chequer and the areas of the work's own colour "
                      f"are four cuts and not one cut named four ways")

                # ---- the module's one law, measured ----------------------------------------------
                # «EVERY PIECE TRAVELS ITS OWN LINE UNTIL IT IS EXACTLY OUT OF THE FRAME AT DIAL 1,
                # AND NO FURTHER» — grid-colour.js's own heading, MOTION, one law in three readings,
                # and the one law this instrument is built to keep. It has two halves and this reads
                # both off the cut map's own layer channel rather than off any number the instrument
                # publishes about itself: at the exit door the departing work holds NO point of the
                # frame, and a hair before its own line runs out it still holds some. The second half
                # is what says the travel is the line's own length and nothing more — a reach any
                # longer would carry the pieces out early and leave the frame bare before its time.
                #
                # ON THE COLOUR CUT the second half is PRINTED rather than asked for, and the
                # instrument says why in its own words: a band's line is its own hue, which only the
                # picture knows, so the clearing dial is taken over the worst direction a hue could
                # name. That is a bound over every possible palette and not the dial at which the
                # five colours this work happens to carry actually clear.
                law = []
                for ki, kn in enumerate(KINDS):
                    js(br, "return window.__setup(%s);"
                       % json.dumps(cfg(kindA=ki, kindB=ki, mask=1)))
                    br.sleep(0.35)
                    v = js(br, "return window.__values({mix: 1});")
                    js(br, "return window.__hostDraw({mix: 0});")
                    br.sleep(0.25)
                    home = layer_share(png(br, SHOTS / ("law-%s-home.png" % kn)))[0]
                    js(br, "return window.__hostDraw({mix: 1});")
                    br.sleep(0.25)
                    gone = layer_share(png(br, SHOTS / ("law-%s-door.png" % kn)))[0]
                    hair = feel_inv(kn, 0.97 * v["needA"] / max(v["liveA"], 1e-9))
                    js(br, "return window.__hostDraw({mix: %r});" % hair)
                    br.sleep(0.25)
                    still = layer_share(png(br, SHOTS / ("law-%s-hair.png" % kn)))[0]
                    law.append((kn, home, gone, still, hair, v["needA"] * v["reachA"],
                                v["reachA"], -v["shortA"]))
                check(BROWSER_ROWS[28],
                      all(hm > 0.995 for _, hm, _, _, _, _, _, _ in law)
                      and all(gn == 0.0 for _, _, gn, _, _, _, _, _ in law)
                      # NOT NOTHING is the whole of the second half, and the bar is exactly that:
                      # at a hundredth short of its own line the piece has NOT cleared. How much of
                      # the frame is left standing is the cut's own business and no threshold's — a
                      # strip leaves a band of the frame behind it and a ring leaves the disc at the
                      # pole with four corner slivers, which is three hundredths against five
                      # ten-thousandths. A reach any longer than the line would empty the frame here
                      # and read 0, which is what this catches.
                      and all(st > 0 for kn, _, _, st, _, _, _, _ in law if kn != "bands"),
                      "; ".join(
                          "the %s cut carries the departing work over %.4f of the frame at dial 0, "
                          "%.4f at dial 1 and %.6f at a hand of %.4f, which is the last hundredth of "
                          "the %.0f points its own line has to cross out of the %.0f that line "
                          "reaches (%.0f points to spare)"
                          % (kn, hm, gn, st, hr, need, reach, spare)
                          for kn, hm, gn, st, hr, need, reach, spare in law)
                      + " — out of the frame at dial 1 exactly on all four, and still standing a "
                      "hair before it on the three whose line the geometry knows. On the colour cut "
                      "that last reading is printed and not asked for, because a band's line is its "
                      "own hue and the dial is derived over the worst direction a hue could name")

                # ---- the two roads --------------------------------------------------------------
                # The module's own far end stands only where this frame's geometry does not need
                # more of the dial. On a frame this shape it does not, for the strip and the tile.
                br.set_viewport(AW, AH)
                br.sleep(0.9)
                js(br, "window.__resize(); return 1;")
                br.sleep(0.5)

                def two_roads(kind_ix, hands, tag):
                    """One pose on both roads. The port is driven by `mix`; the module's two layers
                    are driven to the RAW DIAL the port stands at, each through its own road's own
                    curve, so the geometry compared is one geometry."""
                    js(br, "return window.__setup(%s);"
                       % json.dumps(cfg(kindA=kind_ix, kindB=kind_ix)))
                    br.sleep(0.4)
                    kn = KINDS[kind_ix]
                    out = []
                    for v in hands:
                        vals = js(br, "return window.__values({mix: %r});" % v)
                        hA = feel_inv(kn, vals["dialA"] / FEEL[kn]["live"])
                        hB = feel_inv(kn, vals["dialB"] / FEEL[kn]["live"])
                        js(br, "window.__hands(%r, %r); return 1;" % (hA, hB))
                        js(br, "return window.__hostDraw({mix: %r});" % v)
                        br.sleep(0.35)
                        br.evaluate("window.__show('host'); 0")
                        br.sleep(0.2)
                        ph = png(br, SHOTS / ("%s-%s-%03d-host.png" % (tag, kn, round(v * 100))))
                        br.evaluate("window.__show('module'); 0")
                        br.sleep(0.25)
                        pm = png(br, SHOTS / ("%s-%s-%03d-module.png" % (tag, kn, round(v * 100))))
                        mn, mx = diff(ph, pm)
                        out.append({"mix": v, "mean": mn, "worst": mx, "hA": hA, "hB": hB,
                                    "livePort": vals["liveA"], "liveMod": FEEL[kn]["live"],
                                    "dialA": vals["dialA"], "count": vals["count"],
                                    "geom": geometry_apart(ph, pm),
                                    "bound": hairline_share(kn, vals["count"], AW, AH,
                                                            vals["spanA"][0], vals["radiusA"])})
                    return out

                # TWO RASTERISERS OF ONE GEOMETRY. The module draws on a 2D canvas — its own
                # downscale of the file, its own 8-bit grey twin laid over the picture at the
                # piece's own opacity — and this port samples a texture on the GPU in float. Two
                # rasterisers of one construction cannot agree to a channel, so the frames are
                # compared at the project's own seam of 6 of 255 rather than at the carrier check's
                # 1.5, which is the bar for two GPU roads. WHAT IS COMPARED AT THE CARRIER'S OWN
                # STRICTNESS is the CUT: which points of the frame a piece stands on, read off the
                # ground showing through, with no resampling anywhere in it. That reading is held
                # against the module's own hairline — the one point it grows every piece by at each
                # edge — which is the only thing that can honestly part the two.
                for row_ix, kind_ix in ((6, 0), (7, 2)):
                    kn = KINDS[kind_ix]
                    r = two_roads(kind_ix, [0.2, 0.45, 0.7], "roads")
                    same_curve = all(abs(x["livePort"] - x["liveMod"]) < 1e-9 for x in r)
                    same_hand = all(abs(x["hA"] - x["mix"]) < 1e-6 for x in r)
                    check(BROWSER_ROWS[row_ix],
                          same_curve and same_hand and all(x["mean"] <= SEAM for x in r)
                          and all(x["geom"] < x["bound"] for x in r),
                          "; ".join("mix %.2f: the frames stand %.4f of 255 apart (worst channel "
                                    "%d) and the two roads disagree about whether a piece stands on "
                                    "%.4f of the frame, inside the %.4f the module's own hairline "
                                    "accounts for"
                                    % (x["mix"], x["mean"], x["worst"], x["geom"], x["bound"])
                                    for x in r)
                          + f" — the frames at the project's seam of {SEAM}, the cut at the "
                          f"hairline's own share. On this {AW}x{AH} frame the port derives the "
                          f"{kn} curve's far end at {r[0]['livePort']:.6f}, which is the module's "
                          f"own measured {r[0]['liveMod']}, so the two roads run one arithmetic and "
                          f"are driven at one hand"
                          + ("" if same_curve else " — THEY ARE NOT: the derivation asked for more"))

                # THE RING CUT. The module's own 0.975 leaves the outward rings covering the frame's
                # four corners at the far door, so the port's derivation carries the curve to 1 and
                # the two curves are different curves. The roads are therefore stood at one RAW
                # DIAL, which each reaches with its own hand — and the hand gap is a palette gap,
                # because the palette rides the hand's own axis. Both are printed.
                r = two_roads(1, [0.25, 0.5, 0.75], "roads")
                gap = max(abs(x["hA"] - x["mix"]) for x in r)
                check(BROWSER_ROWS[8],
                      all(x["mean"] <= SEAM for x in r)
                      and all(x["geom"] < x["bound"] for x in r)
                      and all(x["livePort"] > x["liveMod"] for x in r),
                      "; ".join("raw dial %.4f: the port reaches it at a hand of %.4f and the "
                                "module at %.4f, the frames stand %.4f of 255 apart (worst channel "
                                "%d) and the two roads disagree about whether a piece stands on "
                                "%.4f of the frame, inside the %.4f the hairline accounts for"
                                % (x["dialA"], x["mix"], x["hA"], x["mean"], x["worst"],
                                   x["geom"], x["bound"])
                                for x in r)
                      + f" — threshold {SEAM}. The port carries the ring curve's far end to "
                      f"{r[0]['livePort']:.4f} where the module measured {r[0]['liveMod']}, because "
                      f"at {r[0]['liveMod']} an outward ring's inner edge still stands inside the "
                      f"frame's corner radius. The widest hand gap that opens is {gap:.4f}, and it "
                      f"is a palette gap of the same size, since the palette rides the hand")

                br.set_viewport(VW, VH)
                br.sleep(0.8)
                js(br, "window.__resize(); return 1;")
                br.sleep(0.4)

                # THE BAND CUT. Its palette is the half that could not cross, so this row asks what
                # the CUT must be true of on its own road rather than pretending the two agree.
                js(br, "return window.__setup(%s);" % json.dumps(cfg(kindA=3, kindB=3, mask=1)))
                br.sleep(0.4)
                br.evaluate("window.__show('host'); 0")
                band_cov = []
                for v in (0.0, 0.35, 0.65, 1.0):
                    js(br, "return window.__hostDraw({mix: %r});" % v)
                    br.sleep(0.3)
                    p = png(br, SHOTS / ("bands-map-%03d.png" % round(v * 100)))
                    band_cov.append((v, covered_share(p)))
                js(br, "return window.__setup(%s);" % json.dumps(cfg(kindA=3, kindB=3)))
                br.sleep(0.35)
                js(br, "return window.__hostDraw({mix: 0.5});")
                br.sleep(0.3)
                br.evaluate("window.__show('host'); 0")
                br.sleep(0.2)
                band_mid = png(br, SHOTS / "bands-mid-host.png")
                js(br, "window.__hands(0.5, 0.5); return 1;")
                br.sleep(0.35)
                br.evaluate("window.__show('module'); 0")
                br.sleep(0.25)
                band_mod = png(br, SHOTS / "bands-mid-module.png")
                br.evaluate("window.__show('host'); 0")
                band_road = diff(band_mid, band_mod)[0]
                mid_far = [apart(band_mid, towers)[0], apart(band_mid, glass)[0]]
                check(BROWSER_ROWS[9],
                      band_cov[0][1] > 0.995 and band_cov[-1][1] > 0.995
                      and all(0.05 < s < 0.98 for _, s in band_cov[1:-1])
                      and min(mid_far) >= FAR,
                      "the cut map's own coverage channel reads "
                      + "; ".join("mix %.2f: %.3f of the frame claimed" % (v, s)
                                  for v, s in band_cov)
                      + f" — whole at both doors and a real cut in between, and the frame in "
                      f"between stands {mid_far[0]:.2f} from towers.jpg and {mid_far[1]:.2f} from "
                      f"glassgrid.jpg. Against the module's own road the same pose reads "
                      f"{band_road:.2f} of 255 apart, and that is the palette: the module measures "
                      f"a work's five colours on a 128-cell grid of the file quantised to a colour "
                      f"cube, and a shader has no build step, so this port reads five colours off "
                      f"the work at five places of it. The two roads cut different bands out of one "
                      f"photograph, and this row does not pretend otherwise")

                js(br, "return window.__setup(%s);" % json.dumps(cfg()))
                br.sleep(0.35)
                br.evaluate("window.__show('host'); 0")

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
                check(BROWSER_ROWS[10],
                      all(d >= FAR and s >= SPREAD for _, d, s in empties),
                      "; ".join(f"at {at}: {d:.2f} from the ground, spread {s:.2f}"
                                for at, d, s in empties)
                      + f" (bars: {FAR} and {SPREAD}). The frame IS bare between the pieces here, "
                      f"which is this cut's own coverage; what these read is that a picture stands "
                      f"at every one of the instants and none of them is the ground alone")

                js(br, "return window.__offer(%s, {clock: 1.5, progress: 0.5});" % SCORE_JSON)
                br.sleep(0.5)
                br.set_viewport(VW - 80, VH - 120)
                br.sleep(0.7)
                p = png(br, SHOTS / "after-resize.png")
                sized = js(br, "return {w: document.querySelector('canvas').width, "
                               "buffer: window.__report().census.buffer, "
                               "pdb: window.__report().census.preserveDrawingBuffer};")
                d, s = standing(p)
                br.evaluate("window.__cancel('resize row'); 0")
                idle(br)
                br.set_viewport(VW, VH)
                br.sleep(0.5)
                check(BROWSER_ROWS[11],
                      d >= FAR and s >= SPREAD and sized["pdb"] is False,
                      f"after the viewport moved to {VW - 80}x{VH - 120} the buffer reads "
                      f"{sized['buffer']} and the frame stands {d:.2f} from the ground with a "
                      f"spread of {s:.2f}; the context keeps preserveDrawingBuffer={sized['pdb']}")

                # ---- the seeded repeat ----------------------------------------------------------
                took = js(br, "return window.__offer(%s, {clock: 1.5, progress: 0.5});" % SCORE_JSON)
                br.sleep(0.9)
                first = png(br, SHOTS / "seeded-1.png")
                rep1 = js(br, "return window.__report();")
                br.evaluate("window.__cancel('between runs'); 0")
                idle(br)
                js(br, "return window.__offer(%s, {clock: 3.5, progress: 0.5});" % SCORE_JSON)
                br.sleep(0.9)
                second = png(br, SHOTS / "seeded-2.png")
                mn, mx = diff(first, second)
                check(BROWSER_ROWS[12], took["took"] and mn == 0.0 and mx == 0,
                      f"took={took['took']} two runs of one score, at two different seconds of the "
                      f"handed clock: mean {mn} worst channel {mx}. This module rolls no die at all "
                      f"and spends none of the second it is handed, so the two frames are one frame")

                # ---- §4.4b: every handle reaches the picture ------------------------------------
                # A handle read back off the diagnostic surface proves the GRAPH evaluated it and
                # says nothing about whether the instrument obeyed it. Each run below differs from
                # the base by exactly one handle and is photographed, so a picture that did not move
                # is a handle the instrument is not reading. `clock` is the one handle that is
                # expected NOT to move the frame, and its manifest entry says so in advance — this
                # module's every position and every saturation is a pure function of its own dial.
                #
                # WHAT IS READ, AND WHY IT IS THE GREATEST CHANGE RATHER THAN THE MEAN. This
                # instrument's handles are of two sizes: one moves the whole cut and the other moves
                # the COLOUR of the part of the frame it owns. A palette lead that fills the
                # arriving work a beat earlier changes the saturation of the band that work has
                # reached and nothing else, so it moves the mean of a whole frame by a fraction of a
                # level while moving points of it by tens. The mean would therefore rank the handles
                # by how loud they are, which is not what this row is about. What it reads is the
                # greatest change at any point, against the project's own seam of 6 of 255, and it
                # prints the mean beside it. The floor under both is exact: a pose drawn twice
                # unchanged moves the frame by nothing at all, which row 10 above measures at 0.0000
                # mean and 0 worst channel.
                br.evaluate("window.__cancel('before the handle sweep'); 0")
                idle(br)
                br.evaluate("window.__show('host'); window.__exPass.bench.make(); 0")
                br.sleep(0.3)
                js(br, "return window.__setup(%s);"
                   % json.dumps(cfg(countFrom=BASE["countFrom"], countTo=BASE["countTo"],
                                    angleFrom=BASE["angleFrom"], angleTo=BASE["angleTo"],
                                    countBeat=[BASE["countBeatIn"], BASE["countBeatOut"]],
                                    angleBeat=[BASE["angleBeatIn"], BASE["angleBeatOut"]],
                                    stagger=BASE["stagger"], lead=BASE["lead"],
                                    colourPeriod=BASE["colourPeriod"],
                                    colourPhase=BASE["colourPhase"], colourAmp=BASE["colourAmp"],
                                    lightPeriod=BASE["lightPeriod"], lightPhase=BASE["lightPhase"],
                                    lightAmp=BASE["lightAmp"], arrival=BASE["arrival"],
                                    kindA=BASE["kindA"], kindB=BASE["kindB"],
                                    shade=BASE["shade"], mask=BASE["mask"])))
                br.sleep(0.4)
                # THE POSE THE SWEEP STANDS AT. Six tenths of the handle rather than half of it, and
                # deliberately: at half the handle the two layers stand at one and the same dial —
                # the plain reverse walks one line from both ends — so the arriving work is exactly
                # behind the departing one and nothing that belongs to it could show. Off-centre,
                # both layers are travelling and both are in the frame.
                AT = 0.6
                MOVES = {"mix": 0.3, "kindA": 2, "kindB": 1, "countFrom": 20, "countTo": 4,
                         "angleFrom": 55, "angleTo": 5, "countBeatIn": 0.45, "countBeatOut": 0.55,
                         "angleBeatIn": 0.45, "angleBeatOut": 0.55, "stagger": 0.7, "lead": 0.85,
                         "colourPeriod": 0.25, "colourPhase": 0.7, "colourAmp": 0.9,
                         "lightPeriod": 0.3, "lightPhase": 0.8, "lightAmp": 0.9,
                         "arrival": 0, "shade": 0, "mask": 1, "clock": 9.0}
                js(br, "return window.__hostDraw({mix: %r});" % AT)
                br.sleep(0.3)
                hbase = png(br, SHOTS / "handle-base.png")
                moved, still = {}, {}
                for k in HANDLES:
                    over = {"mix": AT}
                    over[k] = MOVES[k]
                    js(br, "return window.__hostDraw(%s);" % json.dumps(over))
                    br.sleep(0.25)
                    q = png(br, SHOTS / ("handle-" + k + ".png"))
                    (still if k == "clock" else moved)[k] = diff(hbase, q)
                check(BROWSER_ROWS[13],
                      all(mx > SEAM and mn > 0 for mn, mx in moved.values())
                      and still["clock"] == (0.0, 0),
                      "; ".join("%s moves a point of the frame by %d of 255 (mean %.4f)"
                                % (k, v[1], v[0])
                                for k, v in sorted(moved.items(), key=lambda x: x[1][1]))
                      + f"; the seam is {SEAM}. `clock` moves it by {still['clock'][1]} at every "
                      f"point, which is what its own manifest entry declares in advance")

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
                             "handles: window.__report().handles, "
                             "events: window.__report().events.map(function(e){return e.name;}).slice(-6)};")
                got_tracks = sorted((end["handles"] or {}).keys()) if end["handles"] else []
                check(BROWSER_ROWS[14],
                      took["took"] and mid["state"] == "running" and mid["curtains"][:1] == [True]
                      and end["state"] == "idle" and len(end["docks"]) == 1
                      and end["curtains"][-1] is False and "docked" in end["events"],
                      f"mid={mid['state']} docks={end['docks']} events={end['events']}; the host "
                      f"resolved {len(got_tracks)} handle tracks off the score's own graph")

                cam = js(br, "var r = window.__report(); "
                             "return {camera: r.camera, rest: r.rest, handoffs: r.handoffs, "
                             "tol: r.camTolerances};")
                check(BROWSER_ROWS[15],
                      cam["camera"] and cam["camera"]["owner"] == "stage"
                      and cam["handoffs"] == []
                      and cam["rest"] and cam["rest"]["rested"] is True
                      and cam["rest"]["off"] <= cam["tol"]["rest"],
                      f"owner={cam['camera'] and cam['camera']['owner']} rest={cam['rest']} "
                      f"handoffs={cam['handoffs']} — the manifest asks for no camera, so the stage "
                      f"holds it for the whole pass")

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
                check(BROWSER_ROWS[16], same,
                      f"before={base_c['textures']}/{base_c['programs']}/{base_c['framebuffers']} "
                      f"after ten runs={after['textures']}/{after['programs']}/{after['framebuffers']} "
                      f"(textures/programmes/framebuffers)")

                errs = json.loads(br.evaluate("JSON.stringify(window.__errs||[])"))
                check(BROWSER_ROWS[17], not errs, "; ".join(errs)[:300])

                r = js(br, "return window.__report();")["resources"]
                check(BROWSER_ROWS[18],
                      r["declared"] and r["over"] is False
                      and r["granted"]["textures"] == r["declared"]["textures"]
                      and r["granted"]["framebuffers"] == r["declared"]["framebuffers"]
                      and r["granted"]["bytes"] == r["declared"]["bytesEstimate"],
                      f"declared={r['declared']} granted={r['granted']}")

                # ---- the two manifest refusals ---------------------------------------------------
                STUB = ("values:function(){return {cutA:[0,0,1,0],cutB:[0,0,1,0],"
                        "gridA:[10,1,0,8],gridB:[10,1,0,8],spanA:[1,1,1,1],spanB:[1,1,1,1],"
                        "voiceA:[1,0],voiceB:[1,0],"
                        "seamLine:1.5,seamRing:1.5,seamTile:1.5};},"
                        "fit:function(){return [1,1,0,0];},"
                        "prepare:function(){return {take:false};}, start:function(){}, "
                        "frame:function(){}")
                r = js(br, """
                  var m = JSON.parse(JSON.stringify(window.__exPass.bench.manifest('grid-colour')));
                  m.gl.preserveDrawingBuffer = true;
                  var ok = window.__exPass.bench.register({name:'grid-preserve', manifest:m, %s});
                  var evs = window.__host.report().events.filter(function(e){return e.name==='manifest-refused';});
                  return {ok: ok, why: evs.length ? evs[evs.length - 1].why : null,
                          registered: window.__host.report().registered};
                """ % STUB)
                check(BROWSER_ROWS[19],
                      r["ok"] is False and r["why"] and "preserved" in r["why"]
                      and "grid-preserve" not in r["registered"],
                      f"registered={r['ok']} why={r['why']}")

                r = js(br, """
                  var m = JSON.parse(JSON.stringify(window.__exPass.bench.manifest('grid-colour')));
                  m.passes[0].uniforms.push({name:'uPointer', type:'vec2', source:'pointer'});
                  var ok = window.__exPass.bench.register({name:'grid-pointer', manifest:m, %s});
                  var evs = window.__host.report().events.filter(function(e){return e.name==='manifest-refused';});
                  return {ok: ok, why: evs.length ? evs[evs.length - 1].why : null,
                          registered: window.__host.report().registered};
                """ % STUB)
                check(BROWSER_ROWS[20],
                      r["ok"] is False and r["why"] and "uPointer" in r["why"]
                      and "cannot supply" in r["why"] and "grid-pointer" not in r["registered"],
                      f"registered={r['ok']} why={r['why']}")

                js(br, "return window.__offer(%s, {clock: 1.0, progress: 0.4});" % SCORE_JSON)
                br.sleep(0.6)
                cen = js(br, "return window.__report();")["census"]
                check(BROWSER_ROWS[21],
                      cen["canvases"] == 1 and cen["contexts"] == 1 and cen["textures"] == 2
                      and cen["passesLastFrame"] == 1 and cen["framebuffers"] == 0
                      and cen["preserveDrawingBuffer"] is False
                      and int(br.evaluate("String(document.querySelectorAll('canvas').length)")) == 3,
                      f"census={cen}; the two further canvases on the page are the lab module's own "
                      f"two layers, which are the road being compared against and no part of the host")
                br.evaluate("window.__cancel('census row'); 0")
                idle(br)

                r = js(br, """
                  var m = window.__exPass.bench.manifest('grid-colour');
                  var plain = window.__exPass.bench.es3(m.passes[0].frag, false);
                  var already = window.__exPass.bench.es3('#version 300 es\\n' + m.passes[0].frag, false);
                  var count = function (s) { return s.split('#version').length - 1; };
                  return {source: count(m.passes[0].frag), stamped: count(plain),
                          untouched: count(already), head: plain.slice(0, 15)};
                """)
                check(BROWSER_ROWS[22],
                      r["source"] == 0 and r["stamped"] == 1 and r["untouched"] == 1
                      and r["head"].startswith("#version 300 es"),
                      f"the module's own road carries {r['source']} headers, the translator leaves "
                      f"it with {r['stamped']}, and a source that already carries one comes back "
                      f"with {r['untouched']}")

                # ---- THE GRID THE DOOR IS READ ON ------------------------------------------------
                # The rows above read every door on the frame the suite runs at. The clearance a
                # door needs is read on the picture as the host SEATS it, which is a function of the
                # buffer; this row states one pair whose door the buffer keeps and one whose it
                # cannot, and asks three things of the instrument: that it reads the buffer it is
                # about to draw on, that it publishes the clearance it applied, and that it says
                # nothing at all away from a door.
                def door_pose(**over):
                    p = {"mix": 0, "clock": 0, "kindA": 0, "kindB": 0, "countFrom": 8, "countTo": 8,
                         "angleFrom": 0, "angleTo": 0, "countBeatIn": 0, "countBeatOut": 1,
                         "angleBeatIn": 0, "angleBeatOut": 1, "stagger": 0, "lead": 0.15,
                         "colourPeriod": 0, "colourPhase": 0, "colourAmp": 0,
                         "lightPeriod": 0, "lightPhase": 0, "lightAmp": 0,
                         "arrival": 0, "shade": 1, "mask": 0, "reduced": False,
                         "cssWidth": VW, "cssHeight": VH,
                         "aw": 1080, "ah": 1080, "bw": 1200, "bh": 899}
                    p.update(over)
                    return p

                def values_of(p):
                    return js(br, "return window.__exPass.bench.values('grid-colour', %s);"
                              % json.dumps(p))

                on_css = values_of(door_pose())
                on_buf = values_of(door_pose(bufWidth=780, bufHeight=1688))
                away = values_of(door_pose(mix=0.5, bufWidth=780, bufHeight=1688))
                masked = values_of(door_pose(mask=1))
                # the clearance the far end of the curve is made of, read on four cuts and on a
                # spread stagger, and never negative — which is the proof beside `needOf`
                clears = []
                for ki, kn in enumerate(KINDS):
                    for stg in (0, 0.6):
                        q = values_of(door_pose(mix=1, kindA=ki, kindB=ki, stagger=stg,
                                                angleFrom=37, angleTo=37,
                                                bufWidth=780, bufHeight=1688))
                        clears.append((kn, stg, q["shortA"], q["liveA"], q["doorWhyNo"]))
                check(BROWSER_ROWS[23],
                      on_css["doorWhyNo"] is None and on_css["doorHeld"] is None
                      and on_css["doorGrid"] == {"w": VW, "h": VH, "drawn": False}
                      and on_buf["doorGrid"] == {"w": 780, "h": 1688, "drawn": True}
                      and on_buf["doorWhyNo"] is None
                      and abs(on_buf["reachA"] / on_css["reachA"] - 2.0) < 1e-9
                      and away["doorGrid"] is None and away["doorWhyNo"] is None
                      and all(s <= 0 and w is None for _, _, s, _, w in clears)
                      and masked["doorWhyNo"] and "judges' own channel" in masked["doorWhyNo"],
                      "on the %d x %d CSS frame the entry door reads «%s» and a piece's line "
                      "reaches %.2f points; on the 780 x 1688 buffer the same frame is drawn on it "
                      "reaches %.2f, exactly twice, because the reading is taken on the grid the "
                      "shader samples. Away from a door it reads nothing at all (grid %s). The "
                      "clearance the exit door is made of, read on that buffer at 37 degrees: %s. "
                      "The judges' channel left open at a door is refused with «%s»"
                      % (VW, VH, on_css["doorWhyNo"] or "nothing", on_css["reachA"],
                         on_buf["reachA"], away["doorGrid"],
                         "; ".join("%s at stagger %g: %.1f points to spare, far end %.4f"
                                   % (k, s, -sh, lv) for k, s, sh, lv, _ in clears),
                         (masked["doorWhyNo"] or "nothing")[:110]))

                # ---- THE DOOR REFUSED ON THE REAL TRANSACTION ROAD -------------------------------
                # The row above reads the instrument's own record. This one puts a real command on
                # the real road: a score that leaves the judges' own channel open at a door asks the
                # instrument to draw the CUT MAP where the door's law asks for a photograph, and the
                # host has to land the visitor on the instrument's own reason rather than draw it.
                # The same score with the channel shut draws. It is the one of this instrument's
                # four door readings a score can actually spoil — the other three are exact by the
                # construction beside `needOf`, and the row above reads all four.
                def road(gen):
                    return js(br, "var r = window.__report(); return {state: r.state, "
                                  "drew: r.drew, buffer: r.census.buffer, "
                                  "refused: r.events.filter(function(e){ return e.gen === %d "
                                  "&& e.why && String(e.why).indexOf('door leaks') >= 0; })"
                                  ".map(function(e){ return e.name + ': ' + e.why; })};" % gen)

                ok_gen = js(br, "return window.__offer(%s, {clock: 0, progress: 0});"
                            % json.dumps(grid_score(kindA=3, kindB=3, mask=0)))["gen"]
                br.sleep(1.0)
                played = road(ok_gen)
                br.evaluate("window.__cancel('door road row'); 0")
                idle(br)
                leak_gen = js(br, "return window.__offer(%s, {clock: 0, progress: 0});"
                              % json.dumps(grid_score(kindA=3, kindB=3, mask=1)))["gen"]
                br.sleep(1.1)
                leaked = road(leak_gen)
                br.evaluate("window.__cancel('door road row'); 0")
                idle(br)
                check(BROWSER_ROWS[24],
                      played["state"] == "running" and played["drew"] == 1
                      and not played["refused"]
                      and len(leaked["refused"]) == 1 and leaked["state"] == "idle"
                      and "the entry door leaks" in leaked["refused"][0]
                      and "judges' own channel" in leaked["refused"][0],
                      "on the %s buffer the colour cut between the two photographs draws (%d cue, "
                      "state %s, refused %s); with the judges' channel left open at the same door "
                      "the same score is refused with «%s», on which the host lands the transaction "
                      "(state %s, %d cue drawn) and the walk's own glide carries the visitor"
                      % (played["buffer"], played["drew"], played["state"],
                         played["refused"] or "nothing",
                         (leaked["refused"] or ["nothing refused"])[0][:230], leaked["state"],
                         leaked["drew"]))

                # ---- the coverage, read off the frame it publishes -------------------------------
                # The rows above put real transactions on the road, and a landing takes the host's
                # own curtain down — so the stage is asked for again here, the way every other
                # bench reading on this page asks for it.
                js(br, "return window.__setup(%s);" % json.dumps(cfg(mask=1)))
                br.sleep(0.35)
                br.evaluate("window.__show('host'); 0")
                cov = []
                for v in (0.0, 0.3, 0.5, 0.7, 1.0):
                    js(br, "return window.__hostDraw({mix: %r});" % v)
                    br.sleep(0.25)
                    p = png(br, SHOTS / ("cover-%03d.png" % round(v * 100)))
                    cov.append((v, covered_share(p)))
                check(BROWSER_ROWS[25],
                      cov[0][1] > 0.995 and cov[-1][1] > 0.995
                      and all(0.05 < s < 0.98 for _, s in cov[1:-1]),
                      "the coverage this instrument publishes, read off the frame: "
                      + "; ".join("mix %.2f: %.3f of the frame claimed by a piece" % (v, s)
                                  for v, s in cov)
                      + " — whole at both doors and genuinely open in between, which is this cut's "
                      "own law: what leaves the eye leaves the frame, and nothing is ever faded")

                kept = sorted(p.name for p in SHOTS.glob("*.png"))
                check(BROWSER_ROWS[26],
                      len(kept) >= 40 and all((SHOTS / k).stat().st_size > 1000 for k in kept),
                      f"{len(kept)} captures under {SHOTS.relative_to(ROOT)}: both doors on all four "
                      f"cuts, the two roads at three poses on three of them, the seven sampled "
                      f"instants, the frame after a resize, the two seeded runs, the twenty-three "
                      f"handle runs and the coverage maps")

    shutil.rmtree(BENCH, ignore_errors=True)

    # ============================================================================================
    # THE RED-ON-BUG PROOFS. The rule each row guards is reverted in the artifact the browser
    # actually loads; the pack served is changed and the host is re-stamped with the digest of the
    # bytes it is handed, which is what the build does. The file on disk is never touched, so no
    # working tree can be left changed by a proof.

    # ONE. The curve's far end reverted to the module's four measured constants — this instrument
    # exactly as the module stands, with the derivation its own header asks for taken back out. On
    # this phone frame the strip cut needs 0.624 of the raw dial for its last strip to cross the
    # frame and the module carries 0.525, so with the constant back in the departing work is still
    # standing across the frame at the exit door.
    def red_live(br):
        js(br, "return window.__setup(%s);" % json.dumps(cfg(kindA=0, kindB=0)))
        br.sleep(0.5)
        br.evaluate("window.__show('host'); 0")
        js(br, "return window.__hostDraw({mix: 1});")
        br.sleep(0.4)
        p = png(br, SHOTS / ("red-live-" + str(id(br)) + ".png"))
        v = js(br, "return window.__values({mix: 1});")
        return {"shot": str(p), "live": v["liveA"], "need": v["needA"]}

    base_live = on_bench(red_live)
    bug = REGION.replace(
        "var liveA = Math.max((FEEL[kindA] || FEEL.stripes).live, nA.live);",
        "var liveA = (FEEL[kindA] || FEEL.stripes).live;", 1)
    bug_live = on_bench(red_live, pack_text=bug)
    if base_live and bug_live:
        from PIL import Image as _Im0
        glass_vw = work_in_the_frame(PHOTOS[1], *_Im0.open(base_live["shot"]).size)
        good = apart(base_live["shot"], glass_vw)[0]
        bad = apart(bug_live["shot"], glass_vw)[0]
    else:
        good = bad = None
    check(RED_ROWS[0],
          bug != REGION and base_live and bug_live and good is not None
          and good <= SEAM and bad > SEAM,
          f"with the far end derived on the frame it draws, the strip cut's exit door stands "
          f"{good if good is None else round(good, 4)} of 255 from glassgrid.jpg — the arriving "
          f"work whole. With the module's own four measured constants back in "
          f"(far end {bug_live and round(bug_live['live'], 4)} against the "
          f"{base_live and round(base_live['need'], 4)} of the raw dial this frame's own geometry "
          f"needs) the same door stands {bad if bad is None else round(bad, 4)} from it, over the "
          f"seam of {SEAM}: the last strip has crossed only part of the frame and the departing "
          f"work is still standing in it")

    # TWO. A ring's reach reverted to ONE REACH FOR ALL RINGS — the state the module records as its
    # own until 12.08, and the regression its header names by name: «a small ring is through the
    # pole in a fifth of the dial while a large one blows its scale up and smears magnified pixels
    # over the whole frame; that was the state until 12.08 and it is what made the arriving work on
    # the по-устройству pair unreadable».
    def red_reach(br):
        js(br, "return window.__setup(%s);" % json.dumps(cfg(kindA=1, kindB=1, mask=1)))
        br.sleep(0.5)
        br.evaluate("window.__show('host'); 0")
        out = {}
        for name, v in (("early", 0.2), ("far", 1.0)):
            js(br, "return window.__hostDraw({mix: %r});" % v)
            br.sleep(0.35)
            out[name] = str(png(br, SHOTS / ("red-reach-%s-%s.png" % (name, id(br)))))
        out["disc"] = js(br, "return window.__values({mix: 0.2});")["dialA"]
        return out

    base_reach = on_bench(red_reach)
    bug2 = REGION.replace(
        "float reach = dirn < 0.0 ? rm : max(0.0, rm * ((halfD + stp) / max(r0, 1e-6) - 1.0));",
        "float reach = rMax;", 1)
    bug_reach = on_bench(red_reach, pack_text=bug2)

    def middle_covered(p):
        """Whether a piece still stands at the frame's own middle, read off the cut map's own
        coverage channel over the sixty points about the centre. It is where the INNERMOST piece is
        — the disc, whose line has one end only, the pole — and it is the one place the two readings
        of a ring's reach part company at once."""
        from PIL import Image
        im = Image.open(p).convert("RGB")
        w, h = im.size
        box = im.crop((w // 2 - 30, h // 2 - 30, w // 2 + 30, h // 2 + 30))
        b = list(box.getdata(2))
        return sum(1 for v in b if v >= 128) / float(len(b))

    if base_reach and bug_reach:
        good2 = middle_covered(base_reach["early"])
        bad2 = middle_covered(bug_reach["early"])
        far_good = middle_covered(base_reach["far"])
    else:
        good2 = bad2 = far_good = None
    check(RED_ROWS[1],
          bug2 != REGION and base_reach and bug_reach and good2 is not None
          and good2 > 0.99 and bad2 < 0.01,
          f"a fifth of the way along the handle — a raw dial of "
          f"{base_reach and round(base_reach['disc'], 4)} — the innermost piece is a disc, and a "
          f"disc travels its OWN middle radius, so it is only through the pole at dial 1 exactly: "
          f"with each ring's reach read off its own radius the disc still covers "
          f"{good2 if good2 is None else round(good2, 4)} of the sixty points about the frame's "
          f"middle. With ONE reach in points for every ring alike — the module's own state until "
          f"12.08, and the regression its own header names — the disc has already gone through the "
          f"pole and the same points are covered "
          f"{bad2 if bad2 is None else round(bad2, 4)}. The far door is untouched by the change "
          f"({far_good if far_good is None else round(far_good, 4)} covered at the exit door on the "
          f"repaired road), which is why a door row alone would never have caught this")

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
