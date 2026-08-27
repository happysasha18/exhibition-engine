#!/usr/bin/env python3
"""PASS-API-V1 — the live-mirror instrument on the host's frame.
Run: python3 tests/test_pass_livemirror.py

Root: his word of 2026-08-18 08:52 after walking the live route — the transitions are all alike
because the lab holds twenty-three effect modules and the engine held six instruments — and his 08:58
«перенеси ВЕСЬ арсенал». lab/effects/livemirror.js is the module this file carries across.

HIS STANDING VERDICT ON THIS EFFECT is one line of lab/CROSSING-BRIEF.md's vocabulary table:
«livemirror | зеркальный сгиб | both | CELL | approved; fold lines must land on the work's own
structural lines». Every row below about WHERE the fold stands is that sentence measured.

WHAT IS COMPARED, AND AGAINST WHAT.

  The doors. At the dial's two ends one whole work stands, cover-fitted into the frame and cropped by
  nothing at all — this instrument's `framings` publishes 1 at both ends. Each door is measured
  against ITS OWN FILE inside the project's seam threshold of 6 of 255.

  THE TWO ROADS. Both draw with WebGL and both run one fragment shader over one rasteriser, so the
  residual between them is a difference of arithmetic rather than of samplers. The lab module is
  served EXACTLY as it stands: nothing of it is levelled for the comparison, because every number of
  the picture came across unchanged. The two places the roads cannot be identical by construction are
  named rather than hidden — the module wraps its own texture MIRRORED_REPEAT where this host binds
  CLAMP_TO_EDGE and the port writes that wrap into the shader, and the module takes one work where a
  cue carries an ordered pair.

  The coverage. This instrument declares that it writes none, because it fills the frame. That is
  measured rather than declared: the fold map — the judges' frame, which paints which mirrored panel
  stands at each point and where in the work it reads — is read at every sampled pose and holds no
  point with nothing to read.

  No empty frame. The rows below sample the pass at seven instants and once across a change of
  viewport, and each frame has to stand as a picture.

  The lab module is READ ONLY. Absent, every browser row here is a pinned SKIP that names the missing
  path — never a silent pass.

NO BYTE FENCE IS WRITTEN HERE. His word of 2026-08-18 08:47 strips that whole class from the
project, so this file measures what the instrument DRAWS and never what it weighs.
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
MODULE = LAB / "effects" / "livemirror.js"

SITE_URL = "https://synth.example.com"
VW, VH = 390, 844          # the phone frame lab/carrier-check.py measures on
SEAM = 6.0                 # the project's seam threshold, 6 of 255 (TRANSITION-STAGE-V0 §1)
FAR = 40.0                 # further than this from a file and it is a different work
BACKGROUND = (0x08, 0x08, 0x0a)
SPREAD = 10.0

# THE TWO ROADS' BAR. Both roads run one fragment shader over one rasteriser and this port changed no
# number of the picture, so the bar is the project's own seam threshold of 6 of 255. What makes it
# mean anything is the red-on-bug set: each proof reverts one rule this port states and moves the
# same number by a wide multiple.
ROADS = SEAM

# The port's own one number of the travel: how much of the hand the wholly mirrored frame stands for,
# and therefore where the two works exchange.
HOLD = 0.08
SHUT_IN = 0.5 - HOLD / 2

# The module's own resting channels, and the room the fold needs at the frame's edge — all three the
# module's own numbers, carried digit for digit.
GLINT_REST = 0.62
DEPTH_REST = 0.62
LINE_EDGE = 0.10

SHOTS = ROOT / "tests" / "captures" / "pass-livemirror"

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


def mirror_cue(stack=0, levels_own=None, **statics):
    """The cue, with a track for every one of the nine handles (§4.4b)."""
    P = {"axis": 2, "centreX": 0.5, "centreY": 0.5, "drift": 0,
         "glint": GLINT_REST, "shade": DEPTH_REST, "mask": 0}
    P.update(statics)
    nodes = {"l-mix": {"source": "progress"}, "l-clock": {"source": "time"}}
    tracks = {"mix": {"node": "l-mix"}, "clock": {"node": "l-clock"}}
    for k, v in P.items():
        nodes["l-" + k] = _static(v)
        tracks[k] = {"node": "l-" + k}
    return {
        "id": "mirror-main", "instrument": {"id": "livemirror", "api": 1},
        "voice": "letter", "roles": ["disassembly", "mystery", "assembly"],
        "levels": ["CELL"],
        "levelOwnership": levels_own or {"CELL": "owns"},
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


def mirror_score(under=False, **statics):
    cues = [mirror_cue(stack=0, **statics)]
    if under:
        cues = cues + [matter_cue(stack=1)]
    res = {"textures": 0, "textureSlots": 2, "framebuffers": 0, "pingPong": 0, "programs": 1,
           "passes": 1, "bytesEstimate": 0}
    return {
        "schema": 2,
        "intent": "the departing work folds onto its own mirror along a line the work itself "
                  "carries, the two works exchange while the frame is wholly mirrored and neither "
                  "is legible as itself, and the arriving work opens back out of the mirror "
                  "(lab/effects/livemirror.js:1-2, its own header)",
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
        "provenance": {"source": "lab/effects/livemirror.js's own declared defaults and constants",
                       "measuredAt": None, "by": "tests/test_pass_livemirror.py"},
    }


# ---------------------------------------------------------------- bake once
build_site.SITE_CONFIG = dict(build_site.SITE_CONFIG)
build_site.SITE_CONFIG["pass"] = {"visualLayer": "pass", "diagnostics": "on"}

TMP = Path(tempfile.mkdtemp(prefix="synth_passmirror_"))
build_site.OUT = TMP
build_site.build(SITE_URL)
LAYER = (TMP / "pass-layer.js").read_text(encoding="utf-8")
# THE INSTRUMENT'S OWN BUILT FILE — the real artifact a visitor is served, comments stripped. Since
# every instrument travels alone, the whole of this file is this instrument and nothing else.
PACK = (TMP / "pass-inst-livemirror.js").read_text(encoding="utf-8")
REGION = PACK
SOURCE = ROOT / "engine" / "assets" / "pass-inst-livemirror.js"
# The file as it stands in the tree, comments and all: the rows about what this instrument DECLARES
# read the built artifact, and the rows about what it SAYS read the source it is built from.
SOURCE_TEXT = SOURCE.read_text(encoding="utf-8")
LABTXT = MODULE.read_text(encoding="utf-8") if MODULE.exists() else ""

# ---------------------------------------------------------------- string rows

OWNED = ["createElement", "getContext", "requestAnimationFrame", "addEventListener",
         "performance.now", "Date.now", "new Image", "setTimeout", "setInterval"]
held = [s for s in OWNED if s in REGION]
check("PASS-LIVEMIRROR the instrument creates no element, no loop and no listener",
      not held,
      "§1.2's fence, read against the instrument's own built file: none of the nine ways of owning "
      "hardware appears there. The module raises its own canvas, takes a WebGL2 context on it, "
      "uploads a texture per picture, runs its own frame loop, observes its own mount for a resize "
      "and binds pointer and touch listeners across it; all of it stayed in the lab"
      if not held else "the instrument's region holds " + ", ".join(held))

HANDLES = ["mix", "clock", "axis", "centreX", "centreY", "drift", "glint", "shade", "mask"]
absent = [h for h in HANDLES if ("%s: { min" % h) not in REGION]
check("PASS-LIVEMIRROR every handle the instrument publishes is a handle a score can drive",
      not absent and len(HANDLES) == 9,
      "§4.4b: nine handles. The dial, the second, which fold, the two places the fold stands, the "
      "mirror's own life, the module's two resting channels and the judges' channel. The module's "
      "`photograph` param is published by neither, and the reason is the arity: a cue carries an "
      "ordered PAIR, so which picture stands is the host's business and not a handle"
      if not absent else "these are published nowhere: " + ", ".join(absent))

# THE MODULE'S OWN POINTER, GRIP AND EASING STAYED BEHIND. The module answers a hand across its
# mount, eases the line toward it on two time constants and brightens the seam while the hand moves;
# an instrument of this engine answers a score and nothing else, so a scored frame is the same frame
# on every screen.
POINTER = ["pointer", "grip", "lastMoveT", "stillAt", "bindStill"]
leaked = [s for s in POINTER if s in REGION]
check("PASS-LIVEMIRROR the module's pointer, its grip and its easing stayed in the lab",
      not leaked and all(s in LABTXT for s in POINTER),
      "the module's own `step` carries a grip that runs to 1 in 0.09 s under a hand and glides back "
      "in 0.8, a fold time constant of 0.055 + 0.30 x (1 - grip), and a seam that brightens for 1.6 "
      "s after the last move (livemirror.js:349-387). What came across is its `poseAt` — its pose "
      "under a HANDED second, with the grip let go and the easing bypassed — which is the pure "
      "function of the clock an instrument may keep"
      if not leaked else "the instrument's region holds " + ", ".join(leaked))

# THE ONE THING THAT HAD NO SHAPE IN THIS HOST. The module gets its mirrored continuation from the
# sampler; the host binds both works CLAMP_TO_EDGE and an instrument never sees the context, so the
# wrap is written into the shader as the triangle wave it is.
check("PASS-LIVEMIRROR the sampler's own mirrored wrap is written into the shader, because the host "
      "binds neither work that way",
      "MIRRORED_REPEAT" in LABTXT
      and "gl.MIRRORED_REPEAT" not in REGION
      and "vec2 mirrored(vec2 q){ return 1.0 - abs(mod(q, 2.0) - 1.0); }" in REGION
      and "gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE" in LAYER,
      "the module sets TEXTURE_WRAP_S and TEXTURE_WRAP_T to MIRRORED_REPEAT on its own texture "
      "(livemirror.js:190-191) and its own comment says the picture past its border «keeps "
      "mirroring (never stretches)». The host uploads both works itself and binds them "
      "CLAMP_TO_EDGE (pass-layer.js:110-111), where every sample past the border returns the border "
      "texel and the continuation smears. MIRRORED_REPEAT is a triangle wave on the coordinate and "
      "nothing else, so it is carried as arithmetic")

# HIS STANDING VERDICT, ANSWERED IN THE MANIFEST ITSELF. A fold line that wanders cannot land on a
# work's own line, so the module's wander rests at nothing and the place is a handle that names the
# measurement it reads.
check("PASS-LIVEMIRROR his standing verdict is answered: the fold's place is a handle that names "
      "its own measurement, and the module's wander rests at nothing",
      'drift: { min: 0, max: 1, def: 0,' in REGION
      and 'centreX: { min: 0, max: 1, def: 0.5,' in REGION
      and 'centreY: { min: 0, max: 1, def: 0.5,' in REGION
      and "structure.radial.centre" in REGION
      and "fold lines land on the work's own lines" in REGION,
      "lab/CROSSING-BRIEF.md's vocabulary table carries «livemirror | зеркальный сгиб | both | CELL "
      "| approved; fold lines must land on the work's own structural lines». The module places its "
      "line with a pointer and drifts it on two incommensurate sines when nobody holds it; here the "
      "place is `centreX`/`centreY`, reading the two works' own measured radial centres, and the "
      "wander is `drift`, resting at nothing. At `drift` 1 with both centres at a half the two "
      "sines are the module's own, amplitude for amplitude and phase for phase")

# Every constant the picture stands on, read out of the lab module and out of the built file.
CONSTANTS = [
    ("0.30 * Math.sin(t * 0.21 + 0.4)", "LINE_X = [0.30, 0.21, 0.4, 0.09, 0.37, 1.7]",
     "the fold line's own wander across the frame: two incommensurate sines, 0.30 at 0.21 rad/s and "
     "0.09 at 0.37, which is charter shelf 13's incommensurate-period instrument in the module's "
     "own hand"),
    ("0.26 * Math.sin(t * 0.163 + 2.1)", "LINE_Y = [0.26, 0.163, 2.1, 0.10, 0.29, 0.6]",
     "the same two sines down the frame, at 0.26/0.163 and 0.10/0.29, so the two axes never repeat "
     "together"),
    ("0.012 * Math.sin(tSec * 0.26)", "BREATH = [0.012, 0.26]",
     "the breathing zoom: twelve thousandths of the frame at 0.26 rad/s, which reads as the picture "
     "breathing rather than as a zoom being pulled"),
    ("1.0 - 0.62 * smoothstep(0.0, 0.60, max(over, 0.0))", "DEPTH_REST = 0.62",
     "how far each further mirrored copy past the work's own border falls into the dark, over the "
     "first six tenths of a frame past it, so the first fold stays the subject"),
    ("seam = drift ? 0.62 : 0", "GLINT_REST = 0.62",
     "the seam's own resting brightness, which is what the module carries when nobody is holding "
     "the line"),
    ("float cw = 0.0016;", "float cw = 0.0016;",
     "the bright core of the seam: sixteen ten-thousandths of the frame's own half-height"),
    ("exp(-(d * d) / (0.0052 * 0.0052)) - core", "exp(-(d * d) / (0.0052 * 0.0052)) - core",
     "the two dark hairlines flanking the core, so the line reads on a white wall as well as on a "
     "shadow"),
    ("exp(-(d * d) / (0.038 * 0.038))", "exp(-(d * d) / (0.038 * 0.038))",
     "the soft lift around the seam"),
    ("mix(1.0, 0.45, lum)", "mix(1.0, 0.45, lum)",
     "the seam's own gain against the luminance under it, so it never blows out into a white smear"),
    ("0.16 * pow(clamp(r, 0.0, 1.0), 2.4)", "0.16 * pow(clamp(r, 0.0, 1.0), 2.4)",
     "the vignette the fold carries, gated to nothing at the flat photograph"),
    ("vec2(0.7071067812, -0.7071067812)", "vec2(0.7071067812, -0.7071067812)",
     "the diagonal fold's own normal"),
    ("var LINE_EDGE = 0.10", "var LINE_EDGE = 0.10;",
     "the room the fold needs at the frame's own edge, named as the module's own: past a tenth of "
     "the frame the fold has almost nothing left to mirror and the travel goes slack"),
    ("(n - 0.5) / 255.0", "(n - 0.5) / 255.0",
     "the module's own half-level dither, so a wide soft gradient inside a mirrored panel does not "
     "band"),
]
missing_const = [(a, b) for a, b, _ in CONSTANTS if a not in LABTXT or b not in REGION]
check("PASS-LIVEMIRROR every constant the picture stands on is the module's own, read out of both "
      "files",
      not missing_const and bool(LABTXT),
      "thirteen numbers and shapes, each present in lab/effects/livemirror.js and in the built "
      "instrument: %s" % "; ".join(c for _, _, c in CONSTANTS)
      if not missing_const
      else "these do not stand in both files: %s" % missing_const)

check("PASS-LIVEMIRROR the port's own one number of the travel is named as the port's, and it is "
      "the only one",
      "var HOLD = 0.08;" in REGION and "THE PORT'S OWN ONE NUMBER OF THE TRAVEL" in SOURCE_TEXT
      and "HOLD" not in LABTXT,
      "the module takes ONE picture and its dial runs from the flat photograph to the fold, so the "
      "port had to say where the second work enters. It enters at the DEEP FOLD, the one stretch of "
      "this instrument's travel at which neither work is legible as itself, and eight hundredths of "
      "the hand is how wide that stretch is — half a second at the 6.5 s this engine runs a middle "
      "at. Every other number of the picture is the module's")

# ---------------------------------------------------------------- browser rows

BROWSER_ROWS = [
    "PASS-LIVEMIRROR §8     · the manifest declares its passes, its handles, its doors and its coverage",
    "PASS-LIVEMIRROR §8     · the level is CELL, carried from his own vocabulary table",
    "PASS-LIVEMIRROR the entry door is the departing work, cover-fitted and cropped by nothing",
    "PASS-LIVEMIRROR the exit door is the arriving work, cover-fitted and cropped by nothing",
    "PASS-LIVEMIRROR the two roads draw one frame: the port beside the lab module at six marks",
    "PASS-LIVEMIRROR the frame is never empty, and the fold is a picture at every mark",
    "PASS-LIVEMIRROR the fold map claims every point of the frame, which is the coverage it declares",
    "PASS-LIVEMIRROR §4.4b  · the fold, its place, the mirror's life and the two channels reach the PICTURE",
    "PASS-LIVEMIRROR the charter · the fold stands where it is placed, and moving the place moves the frame",
    "PASS-LIVEMIRROR the fold is WALKED on the drawing buffer at both doors, and what it read is published",
    "PASS-LIVEMIRROR a door the judges' channel spoils is refused on the real road, and the visitor still lands",
    "PASS-LIVEMIRROR the real transaction road: curtain up, one pass drawn, exactly one dock at the end",
    "PASS-LIVEMIRROR the instrument is lawful as the ground of a stack, and the host says so",
    "PASS-LIVEMIRROR the hand's own band across twenty-one equal marks, and the dial's own "
    "degenerate mark named",
    "PASS-LIVEMIRROR row 16 · the captures are kept as evidence",
]

RED_ROWS = [
    "PASS-LIVEMIRROR red-on-bug · the mirrored wrap removed: the picture smears past its own border",
    "PASS-LIVEMIRROR red-on-bug · the seam's own gate removed: the entry door leaves its own file",
    "PASS-LIVEMIRROR red-on-bug · the hand's two halves removed: the exit door is refused, folded",
    "PASS-LIVEMIRROR red-on-bug · the room at the frame's edge removed: the fold stands with nothing to mirror",
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


def nowhere(p):
    """The share of the fold map that names no mirrored panel. The map paints the panel a point
    stands in as red at a quarter, a half, three quarters or the whole, and where in the work that
    point reads as green and blue; a point with nothing to read would stay black in red. So this is
    the share of the frame this instrument's own claim of full coverage fails on."""
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
    """The whole file, cover-fitted into the frame. This instrument crops nothing at either door and
    its `framings` block publishes 1 at both, so the file itself is what a door is measured
    against."""
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
    the lab module exactly as it stands, the two photographs, and the page that stands the two roads
    of one frame side by side.

    A row proving a rule reds hands over a CHANGED instrument file and writes the record with the
    digest of the bytes actually served, which is what the build does. The source file on disk is
    never touched, so nothing has to be restored and no working tree can be left changed by a
    red-on-bug proof."""
    d = Path(tempfile.mkdtemp(prefix="synth_mirrorbench_"))
    pack = PACK if pack_text is None else pack_text
    shutil.copy2(TMP / "pass-layer.js", d / "pass-layer.js")
    for _inst in sorted(TMP.glob("pass-inst-*.js")):
        shutil.copy2(_inst, d / _inst.name)
    (d / "pass-inst-livemirror.js").write_text(pack, encoding="utf-8")
    record = json.loads((TMP / "config.json").read_text(encoding="utf-8"))
    record["pass"]["instruments"]["livemirror"]["digest"] = hashlib.sha256(
        pack.encode("utf-8")).hexdigest()
    (d / "config.json").write_text(json.dumps(record), encoding="utf-8")
    (d / "livemirror.js").write_text(LABTXT, encoding="utf-8")
    (d / "photos").mkdir()
    for p in PHOTOS:
        shutil.copy2(p, d / "photos" / p.name)
    shutil.copy2(ROOT / "tests" / "fixture_pass_livemirror.html", d / "index.html")
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
    """BOTH ROADS AT ONE DIAL. One number goes to the module's own `fold` handle and, through the
    port's own hand, to the instrument; the two are then standing at one pose."""
    r = js(br, "return window.__both(%r);" % at)
    br.evaluate("window.__mask(0); window.__show('host'); window.__hold(null); 0")
    br.sleep(0.45)
    ph = png(br, SHOTS / (tag + "-host.png"))
    br.evaluate("window.__show('module'); 0")
    br.sleep(0.35)
    pm = png(br, SHOTS / (tag + "-module.png"))
    br.evaluate("window.__show('host'); 0")
    return r, ph, pm


def fold_map(br, at, tag):
    js(br, "return window.__both(%r);" % at)
    br.evaluate("window.__mask(1); window.__show('host'); window.__hold(null); 0")
    br.sleep(0.4)
    p = png(br, SHOTS / ("map-" + tag + ".png"))
    br.evaluate("window.__mask(0); 0")
    return p


def host_at(br, hand, tag):
    """The host's frame at a named place of the HAND — which is what a door row and a handle row
    ask for, rather than the module's own dial.

    THE POSE IS HELD ON THE HOST'S OWN FRAME LOOP while it is photographed, and that is not
    superstition. The stage's context is created with `preserveDrawingBuffer: false` and the lab
    module's stage is hidden while the host's frame is being read, so a page that draws one frame
    and then stands still gives the compositor nothing to do and a capture returns whatever it last
    composited. Walked across twenty-one marks of the hand that showed up as eight consecutive marks
    photographing ONE frame and the ninth carrying all of their change at once — a band of 32 read
    off a travel that measures 2.3. Holding the pose puts it in the frame the capture takes, and it
    is the same drawPose a running transaction issues either way."""
    br.evaluate("window.__mask(0); window.__show('host'); window.__hold(%r); 0" % hand)
    br.sleep(0.4)
    return png(br, SHOTS / (tag + ".png"))


def grab(br, hand, tag):
    """The host's own drawing buffer at a named place of the hand, read with no compositor between.
    A screenshot reads what the page last COMPOSITED, and a page whose only moving pixels sit inside
    a hidden element gives the compositor leave to coalesce; this copies the stage into a plain 2D
    canvas in the same task the pose was drawn in, so what comes back is the frame the instrument
    produced and not the frame the screen last showed."""
    url = br.evaluate("window.__grab(%r)" % hand)
    if url.startswith('"'):
        url = json.loads(url)
    p = SHOTS / (tag + ".png")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(base64.b64decode(url.split(",", 1)[1]))
    return p


def host_shot(br, at, tag):
    js(br, "return window.__both(%r);" % at)
    br.evaluate("window.__mask(0); window.__show('host'); window.__hold(null); 0")
    br.sleep(0.4)
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
            elif not js(br, "return !!window.__exPass.bench.manifest('livemirror');"):
                why = js(br, "var e = window.__host.report().events.filter(function(x){"
                             "return x.name === 'manifest-refused';});"
                             "return e.length ? e[e.length - 1].why : null;")
                for r in BROWSER_ROWS:
                    check(r, False, "the host registered no «livemirror» instrument: " + str(why))
            else:
                SCORE = json.dumps(mirror_score())
                SCORE_UNDER = json.dumps(mirror_score(under=True))

                # ---- §8: the manifest, read off the registered instrument -----------------------
                m = js(br, "return window.__exPass.bench.manifest('livemirror');")
                res = m["resources"]
                need = ["id", "api", "arity", "roles", "params", "handles", "neutrals", "doors",
                        "framings", "drivers", "camera", "gl", "passes", "resources",
                        "capabilities", "decline", "provenance", "readiness", "coverage", "levels"]
                shape = (
                    all(k in m for k in need)
                    and m["id"] == "livemirror" and m["api"] == 1 and m["arity"] == 2
                    and m["roles"] == ["disassembly", "mystery", "assembly"]
                    and sorted(m["params"]) == ["axis", "centreX", "centreY", "drift", "glint",
                                                "shade"]
                    and len(m["handles"]) == 9
                    and all(set(h) >= {"min", "max", "def"} for h in m["handles"].values())
                    and m["neutrals"] == {"a": 0, "b": 1}
                    and m["doors"]["in"]["handle"] == "mix" and m["doors"]["in"]["value"] == 0
                    and m["doors"]["out"]["handle"] == "mix" and m["doors"]["out"]["value"] == 1
                    and sorted(m["framings"]) == ["0", "1"]
                    and m["framings"]["0"] == {"coverCrop": 1} == m["framings"]["1"]
                    and m["camera"] == {"needs": "none", "authority": "stage"}
                    and m["gl"] == {"preserveDrawingBuffer": False}
                    and len(m["passes"]) == 1 and len(m["passes"][0]["uniforms"]) == 8
                    and sorted(res) == ["lean", "rich", "standard"]
                    and all("bytesEstimate" in res[v] and res[v]["programs"] == 1
                            and res[v]["passes"] == 1 and res[v]["textureSlots"] == 2
                            for v in res)
                    and m["capabilities"] == ["webgl2"] and m["decline"]
                    and m["coverage"]["writes"] is False and m["coverage"]["how"]
                    and m["provenance"]["labPath"] == "lab/effects/livemirror.js"
                    and m["provenance"]["commit"] == "fc885a3"
                    and m["readiness"] == "production-ready"
                    and "livemirror" in js(br, "return window.__host.report().registered;"))
                check(BROWSER_ROWS[0], shape,
                      f"nine handles, eight uniforms in one pass, both doors at a cover crop of "
                      f"{m['framings']['0']['coverCrop']} — this instrument crops nothing, because "
                      f"the module cover-fits its file over its mount and the breathing zoom is "
                      f"gated by the dial — resources declared for three tiers with a byte estimate "
                      f"of {res['standard']['bytesEstimate']}, and a coverage block reading "
                      f"«{m['coverage']['how']}»")

                check(BROWSER_ROWS[1],
                      m["levels"] == ["CELL"] and m["register"] == "spectacle"
                      and "WHERE THIS STANDS ON THE CHARTER'S SHELF" in SOURCE_TEXT,
                      f"levels={m['levels']}, register={m['register']!r}. The reading is CARRIED and "
                      f"not re-decided: lab/CROSSING-BRIEF.md's vocabulary table records this "
                      f"module's level as CELL, and that row is his own standing verdict. WORLD is "
                      f"not claimed and that is the whole difference between this instrument and "
                      f"the box — no space is folded and no eye travels, so this one spends no "
                      f"miracle and is reachable at a quiet link and at a return, where the box may "
                      f"not stand at all")

                w = int(br.evaluate("String(window.__exPass.bench.make() && "
                                    "document.querySelector('canvas[aria-hidden]').width)"))
                h = int(br.evaluate("String(document.querySelector('canvas[aria-hidden]').height)"))
                bufs = js(br, "return window.__buffers();")
                glass = work_in_the_frame(BENCH / "photos" / "glassgrid.jpg", w, h)
                towers = work_in_the_frame(BENCH / "photos" / "towers.jpg", w, h)

                # ---- the two doors --------------------------------------------------------------
                d0 = host_at(br, 0.0, "door-0")
                v0 = js(br, "return window.__values(0);")
                m0, x0 = apart(d0, glass)
                check(BROWSER_ROWS[2], m0 < SEAM and not v0["doorWhyNo"],
                      f"the entry door stands {m0:.4f} of 255 from glassgrid.jpg cover-fitted into "
                      f"the {w} x {h} frame, worst channel {x0:.0f}, against a bar of {SEAM}. At "
                      f"the door the dial is exactly {v0['fold'][2]} and every term of the fold — "
                      f"the reflected coordinate, the breathing zoom, the depth the mirrored copies "
                      f"fall into, the seam and the vignette — is gated to its own identity by it, "
                      f"so what the shader draws is the plain cover fit with the module's own "
                      f"half-level dither over it")

                d1 = host_at(br, 1.0, "door-1")
                v1 = js(br, "return window.__values(1);")
                m1, x1 = apart(d1, towers)
                check(BROWSER_ROWS[3], m1 < SEAM and not v1["doorWhyNo"],
                      f"the exit door stands {m1:.4f} of 255 from towers.jpg cover-fitted into the "
                      f"same frame, worst channel {x1:.0f}, against a bar of {SEAM}. The exchange "
                      f"stands at {v1['fold'][3]} there, so the frame is the arriving work alone "
                      f"and the departing one is never sampled")

                # ---- the two roads --------------------------------------------------------------
                MARKS = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
                road_reads = []
                for at in MARKS:
                    r, ph, pm = roads(br, at, "dial-%s" % str(at).replace(".", "p"))
                    mean, worst = diff(ph, pm)
                    road_reads.append((at, mean, worst))
                worst_road = max(r[1] for r in road_reads)
                check(BROWSER_ROWS[4],
                      worst_road < ROADS and bufs["host"] == bufs["module"],
                      "the port and lab/effects/livemirror.js, drawn at one pose and photographed "
                      "on one grid (%s): %s — the widest %.4f of 255 against a bar of %.1f. Both "
                      "roads run one fragment shader over one rasteriser and this port changed no "
                      "number of the picture; what stands between them is the mirrored wrap, which "
                      "the module gets from its sampler and the port writes as arithmetic"
                      % (bufs["host"],
                         ", ".join("dial %.1f: %.4f (worst channel %.0f)" % r for r in road_reads),
                         worst_road, ROADS))

                # ---- the frame is a picture ------------------------------------------------------
                stands = []
                for at in [0.0, 0.15, 0.3, 0.5, 0.7, 0.85, 1.0]:
                    p = host_shot(br, at, "stand-%s" % str(at).replace(".", "p"))
                    stands.append((at,) + standing(p))
                br.evaluate("window.__resize(); 0")
                br.sleep(0.4)
                p = host_shot(br, 0.5, "stand-resize")
                stands.append(("resize",) + standing(p))
                check(BROWSER_ROWS[5],
                      all(s[1] > SPREAD and s[2] > SPREAD for s in stands),
                      "eight frames, each measured against the flat stage colour and against its "
                      "own spread: %s. Nothing here is an empty box, and the deepest fold is as "
                      "much a picture as the flat photograph"
                      % ", ".join("%s: %.1f from flat, spread %.1f" % s for s in stands))

                # ---- the coverage, measured ------------------------------------------------------
                maps = []
                for at in [0.0, 0.25, 0.5, 0.75, 1.0]:
                    p = fold_map(br, at, str(at).replace(".", "p"))
                    maps.append((at, nowhere(p)))
                check(BROWSER_ROWS[6], all(mm[1] == 0.0 for mm in maps),
                      "the fold map at five marks of the dial: %s of the frame with nothing to "
                      "read. A reflection is a map ONTO the work rather than a rearrangement of "
                      "pieces of it, and the mirrored wrap carries whatever falls past the work's "
                      "border back into it, so the coverage this instrument declares costs it no "
                      "crop at all"
                      % ", ".join("dial %.2f: %.4f%%" % (a, s * 100) for a, s in maps))

                # ---- every handle reaches the picture --------------------------------------------
                # Each handle is walked from one end of its own published range to the other at one
                # place of the hand, and the frame has to move by more than the project's own seam.
                br.evaluate("window.__param('drift', 1); 0")
                br.sleep(0.35)
                moves = []

                def handle_move(key, lo, hi, tag, rebuild=False):
                    br.evaluate("window.__param(%r, %r); 0" % (key, lo))
                    br.sleep(0.4 if rebuild else 0.2)
                    a = host_shot(br, 1.0, "handle-%s-lo" % tag)
                    br.evaluate("window.__param(%r, %r); 0" % (key, hi))
                    br.sleep(0.4 if rebuild else 0.2)
                    b = host_shot(br, 1.0, "handle-%s-hi" % tag)
                    return (key,) + diff(a, b)

                moves.append(handle_move("axis", 0, 3, "axis", rebuild=True))
                br.evaluate("window.__param('axis', 2); 0")
                br.sleep(0.4)
                moves.append(handle_move("centreX", 0.15, 0.85, "centrex"))
                br.evaluate("window.__param('centreX', 0.5); 0")
                moves.append(handle_move("centreY", 0.15, 0.85, "centrey"))
                br.evaluate("window.__param('centreY', 0.5); 0")
                moves.append(handle_move("glint", 0, 1, "glint"))
                br.evaluate("window.__param('glint', %r); 0" % GLINT_REST)
                # THE ONE HANDLE THAT NEEDS A POSE OF ITS OWN, and the reason is a measurement. The
                # depth a further mirrored copy falls into can only be read where a further copy
                # STANDS, and a fold at the middle of the frame makes none: reflected about a line
                # at a half, every sample lands back inside the work. A copy first stands when the
                # fold is nearer an edge than the frame's own middle, so this walk is taken with
                # the wander parked and the flat fold at 0.15, which is where the module's own
                # `over` term first has anything to weigh.
                br.evaluate("window.__param('drift', 0); window.__param('centreY', 0.15); 0")
                br.sleep(0.45)
                moves.append(handle_move("shade", 0, 1, "shade"))
                br.evaluate("window.__param('shade', %r); window.__param('centreY', 0.5); 0"
                            % DEPTH_REST)
                br.evaluate("window.__clock(6.4); 0")
                br.sleep(0.3)
                moves.append(handle_move("drift", 0, 1, "drift", rebuild=True))
                br.evaluate("window.__param('drift', 1); window.__clock(0); 0")
                br.sleep(0.4)
                check(BROWSER_ROWS[7], all(mv[1] > SEAM for mv in moves),
                      "each handle walked from one end of its own published range to the other at "
                      "the deep fold, and the frame read against itself: %s. A bar of %.1f of 255 "
                      "is the project's own seam, so every one of these reaches the picture and not "
                      "only the record"
                      % (", ".join("%s: %.1f of 255 (worst channel %.0f)" % mv for mv in moves),
                         SEAM))

                # ---- his verdict, on the frame ---------------------------------------------------
                br.evaluate("window.__param('drift', 0); window.__param('axis', 0); 0")
                br.sleep(0.45)
                place = []
                for at, tag in [(0.28, "line-a"), (0.5, "line-b"), (0.72, "line-c")]:
                    br.evaluate("window.__param('centreX', %r); 0" % at)
                    br.sleep(0.2)
                    place.append((at, host_shot(br, 1.0, tag)))
                sep = [(place[i][0], place[j][0]) + diff(place[i][1], place[j][1])
                       for i, j in [(0, 1), (1, 2), (0, 2)]]
                vals = js(br, "window.__param('centreX', 0.28);"
                              "return window.__values(%r);" % SHUT_IN)
                check(BROWSER_ROWS[8],
                      all(s[2] > SEAM for s in sep)
                      and abs(vals["fold"][0] - 0.28) < 1e-9 and vals["lineHeld"] is None,
                      "the fold placed at three lines of the frame, each pair read against the "
                      "other: %s. With the wander at nothing the line stands exactly where it is "
                      "placed — the instrument's own reading answers %.6f for a place of 0.28, held "
                      "by nothing — which is his standing verdict on this effect kept rather than "
                      "declared"
                      % (", ".join("%.2f against %.2f: %.1f of 255" % (a, b, mn)
                                   for a, b, mn, _ in sep), vals["fold"][0]))

                # ---- the door, WALKED ------------------------------------------------------------
                br.evaluate("window.__param('centreX', 0.5); window.__param('drift', 0); 0")
                br.sleep(0.3)
                walked = js(br, "return [window.__values(0), window.__values(1)];")
                ok = (walked[0]["foldMap"] and walked[1]["foldMap"]
                      and walked[0]["foldMap"]["walked"] >= 26
                      and walked[0]["foldMap"]["movedPx"] == 0
                      and walked[1]["foldMap"]["movedPx"] == 0
                      and walked[0]["foldMap"]["outside"] == 0
                      and walked[1]["foldMap"]["outside"] == 0
                      and walked[0]["foldMap"]["seated"] is True
                      and not walked[0]["doorWhyNo"] and not walked[1]["doorWhyNo"])
                check(BROWSER_ROWS[9], ok,
                      "his 18:00 architecture decision, read in this instrument's own unit — the "
                      "sample's own travel. At each door the instrument walks its own fold map on "
                      "the buffer the host is about to bind: %d points at the entry door and %d at "
                      "the exit, the furthest moved by %.6f and %.6f points of a %s buffer, %d and "
                      "%d of them reading past the work's own border, on the seating the host hands "
                      "down. Both doors are held whole and neither is refused"
                      % (walked[0]["foldMap"]["walked"], walked[1]["foldMap"]["walked"],
                         walked[0]["foldMap"]["movedPx"], walked[1]["foldMap"]["movedPx"],
                         walked[0]["doorGrid"] and "%dx%d" % (walked[0]["doorGrid"]["w"],
                                                              walked[0]["doorGrid"]["h"]),
                         walked[0]["foldMap"]["outside"], walked[1]["foldMap"]["outside"]))

                # ---- a door the judges' channel spoils -------------------------------------------
                # THE ONE DOOR THIS INSTRUMENT'S OWN HANDLES CAN SPOIL. The hand puts the dial at
                # exactly nothing at both ends and the cover fit leaves no sample outside the work,
                # so the first three clauses of the door law come out whole on every pose these
                # handles admit — which is the runtime truth, not a reason to leave the claim
                # unread. `mask` is the fourth: it draws the fold map itself as colour, and a score
                # that leaves it open at a door hands the visitor a false-colour map of the mirrored
                # panels instead of the photograph.
                # The bench's own frame loop is let go first: from here on the HOST runs its own,
                # and two loops drawing into one stage would photograph each other's frames.
                br.evaluate("window.__release(); 0")
                br.sleep(0.2)

                def road(gen):
                    return js(br, "var r = window.__report(); return {state: r.state, "
                                  "drew: r.drew, buffer: r.census.buffer, "
                                  "refused: r.events.filter(function(e){ return e.gen === %d "
                                  "&& e.why && String(e.why).indexOf('door leaks') >= 0; })"
                                  ".map(function(e){ return e.name + ': ' + e.why; })};" % gen)

                br.evaluate("window.__cancel('door road row'); 0")
                idle(br)
                shut_gen = js(br, "return window.__offer(%s, {clock: 0, progress: 0});"
                              % json.dumps(mirror_score(mask=0)))["gen"]
                br.sleep(1.0)
                played = road(shut_gen)
                br.evaluate("window.__cancel('door road row'); 0")
                idle(br)
                open_gen = js(br, "return window.__offer(%s, {clock: 0, progress: 0});"
                              % json.dumps(mirror_score(mask=1)))["gen"]
                br.sleep(1.1)
                leaked = road(open_gen)
                br.evaluate("window.__cancel('door road row'); 0")
                idle(br)
                check(BROWSER_ROWS[10],
                      played["state"] == "running" and played["drew"] == 1
                      and not played["refused"]
                      and len(leaked["refused"]) == 1 and leaked["state"] == "idle"
                      and leaked["drew"] == 0
                      and "the entry door leaks" in leaked["refused"][0]
                      and "the judges' own channel" in leaked["refused"][0]
                      and "fold map" in leaked["refused"][0],
                      "on the %s buffer the host drew, the judges' channel shut draws the door (%d "
                      "cue, state %s, refused %s); left open it is refused with «%s», on which the "
                      "host lands the transaction (state %s, %d cue drawn) and the walk's own glide "
                      "carries the visitor"
                      % (played["buffer"], played["drew"], played["state"],
                         played["refused"] or "nothing",
                         (leaked["refused"] or ["nothing refused"])[0], leaked["state"],
                         leaked["drew"]))

                # ---- the real transaction road ---------------------------------------------------
                br.evaluate("window.__hooks = {docks: [], curtains: [], glides: [], marks: []}; 0")
                got = js(br, "return window.__offer(%s);" % SCORE)
                br.sleep(0.6)
                mid = js(br, "return window.__report();")
                idle(br, tries=200)
                hooks = js(br, "return window.__hooks;")
                rep = js(br, "return window.__report();")
                check(BROWSER_ROWS[11],
                      got["took"] and mid["state"] in ("running", "settling", "idle")
                      and hooks["curtains"] and hooks["curtains"][0] is True
                      and len(hooks["docks"]) == 1 and rep["state"] == "idle"
                      and rep["census"]["passesLastFrame"] == 1,
                      "one offer of a real score: the curtain went up %s, the host drew %d pass a "
                      "frame, and exactly one dock closed it (%s). No glide was needed: %s"
                      % (hooks["curtains"], rep["census"]["passesLastFrame"], hooks["docks"],
                         hooks["glides"]))

                # ---- the placement its coverage buys it -------------------------------------------
                cov = js(br, "return window.__exPass.bench.coverageOf('livemirror');")
                lawful = js(br, "return window.__exPass.bench.coverageWhyNo(%s);"
                                % json.dumps(mirror_score(under=True)["cues"]))
                alone = js(br, "return window.__exPass.bench.coverageWhyNo(%s);"
                               % json.dumps(mirror_score()["cues"]))
                over = js(br, "return window.__exPass.bench.coverageWhyNo(%s);"
                              % json.dumps([matter_cue(stack=0), mirror_cue(stack=1)]))
                check(BROWSER_ROWS[12],
                      cov["writes"] is False and lawful is None and alone is None and over,
                      "the instrument declares `coverage.writes: false`, so the host's own "
                      "placement law makes it lawful as the LOWEST cue of a stack (%s) and as a "
                      "whole one-cue score (%s), and refuses a stack whose ground writes coverage "
                      "under it: «%s». That is the ground the composer's census counts 1 320 "
                      "declined plans waiting on"
                      % (lawful, alone, str(over)[:160]))

                # ---- the hand's own band ---------------------------------------------------------
                # The charter's law: equal movement of the hand, equal felt change. The module
                # states its own dial's curve as the IDENTITY and gives the reading behind it; this
                # reads the PORT's hand, which is two halves of that dial with an exchange between,
                # at the same twenty-one equal marks the pack's other instruments use.
                br.evaluate("window.__release(); window.__mask(0); 0")
                br.sleep(0.2)
                band_shots = []
                for i in range(21):
                    band_shots.append(grab(br, i / 20.0, "band-%02d" % i))
                steps = [diff(band_shots[i], band_shots[i + 1])[0] for i in range(20)]
                dials = [js(br, "return window.__values(%r).fold;" % (i / 20.0))[2]
                         for i in range(21)]
                # TWO STRETCHES OF THE HAND ARE READ APART FROM THE REST, and both by a rule stated
                # before the numbers were seen rather than by picking a step that spoiled a band.
                #
                #   · THE EXCHANGE. The hold runs from 0.46 to 0.54 of the hand, so the steps that
                #     straddle it carry two photographs crossing rather than one folding, and a
                #     dissolve between two different works is a wide channel distance whatever the
                #     curve does.
                #   · THE DIAL'S OWN DEGENERATE MARK, which is the module's construction and this
                #     port's finding about it. The reflected side of the frame reads the work at
                #     `uv + (reflect(uv) - uv) * dial`, whose scale along the folded axis is
                #     `1 - 2 * dial`. At a dial of a half that scale is NOTHING: the whole reflected
                #     side reads one column of the work, stretched across it, and the frame's change
                #     there is a property of the squeeze rather than of the hand. Where the scale
                #     stands under three tenths — a dial between 0.35 and 0.65 — the marks are read
                #     apart and named.
                cross = [i for i in range(20) if not (i / 20.0 >= 0.54 or (i + 1) / 20.0 <= 0.46)]
                flat = [i for i in range(20)
                        if abs(1 - 2 * dials[i]) < 0.3 or abs(1 - 2 * dials[i + 1]) < 0.3]
                apart_i = sorted(set(cross) | set(flat))
                own = [s for i, s in enumerate(steps) if i not in apart_i]
                band = max(own) / min(own)
                check(BROWSER_ROWS[13], band < 2.5 and min(steps) > 1.0,
                      "the frame drawn at twenty-one equal marks of the hand and the distance "
                      "between neighbouring frames read. The fold's own %d steps: widest %.1f of "
                      "255, narrowest %.1f, a band of %.3f against a bar of 2.5, and no mark of the "
                      "hand leaves the frame standing still (the narrowest step of all twenty is "
                      "%.1f). The module states its own dial's curve as the IDENTITY and gives the "
                      "reading behind it — 29.9 channels at the slowest step against 42.9 at the "
                      "fastest, a band of 1.43, because the dial walks the SAMPLING POINT and the "
                      "distance travelled is linear in it — and this reads the PORT's hand, which "
                      "is that dial run once over each half. Read apart, by the rule stated in the "
                      "file: the exchange %s and the dial's own degenerate mark %s, where the "
                      "reflected side's scale 1 - 2 x dial falls under three tenths and the frame "
                      "is one column of the work stretched across half of it. All twenty: %s"
                      % (len(own), max(own), min(own), band, min(steps),
                         [round(steps[i], 1) for i in cross],
                         [round(steps[i], 1) for i in flat],
                         ", ".join("%.1f" % s for s in steps)))

                shots = sorted(SHOTS.glob("*.png"))
                check(BROWSER_ROWS[14], len(shots) >= 40,
                      "%d captures under tests/captures/pass-livemirror: both doors, six marks of "
                      "the two roads with the module beside the port at each, eight standing "
                      "frames, five fold maps, the handle walks, the three placed lines and "
                      "twenty-one marks of the hand" % len(shots))

    # ---------------------------------------------------------------- red on bug
    # Each proof reverts ONE rule this port states, in the BYTES THE BROWSER IS SERVED, and the same
    # number has to move. The file on disk is never touched.

    def red(name, frm, to, fn, why):
        if frm not in PACK:
            check(name, False, "the proof found nothing to revert: " + frm)
            return
        out = on_bench(fn, PACK.replace(frm, to, 1))
        if out is None:
            check(name, False, "the bench never came up under the reverted rule")
            return
        check(name, out[0], why % out[1:])

    # 1 · the mirrored wrap, which is the module's own «never stretches»
    def no_wrap(br):
        br.evaluate("window.__param('drift', 0); window.__param('axis', 0);"
                    "window.__param('centreX', 0.16); 0")
        br.sleep(0.45)
        js(br, "return window.__both(1);")
        br.sleep(0.35)
        br.evaluate("window.__mask(0); window.__hostDraw(); window.__show('host'); 0")
        br.sleep(0.3)
        p = png(br, SHOTS / "red-nowrap-host.png")
        br.evaluate("window.__show('module'); 0")
        br.sleep(0.35)
        q = png(br, SHOTS / "red-nowrap-module.png")
        mean, worst = diff(p, q)
        return (mean > ROADS * 3, mean, worst)

    red(RED_ROWS[0],
        "  vec2 mst = clamp(mirrored(st), 0.0, 1.0);",
        "  vec2 mst = clamp(st, 0.0, 1.0);",
        no_wrap,
        "with the wrap reverted to the host's own clamp the picture past the work's border stops "
        "mirroring and smears the border texel instead, which is the one thing the module's own "
        "comment forbids: the two roads stand %.2f of 255 apart, worst channel %.0f, against a "
        "two-roads bar of 6.0")

    # 2 · the seam's own gate on the dial
    def seam_ungated(br):
        d = host_at(br, 0.0, "red-seam-door")
        w = int(br.evaluate("String(document.querySelector('canvas[aria-hidden]').width)"))
        hh = int(br.evaluate("String(document.querySelector('canvas[aria-hidden]').height)"))
        file_ = work_in_the_frame(PHOTOS[0], w, hh)
        mean, worst = apart(d, file_)
        return (worst > 60 and mean > 3.0, mean, worst)

    red(RED_ROWS[1],
        "  float sm = uForm.y * dial;",
        "  float sm = uForm.y;",
        seam_ungated,
        "the seam, the depth fade and the vignette belong to the fold alone and none of them stands "
        "at the flat door, so each is gated to its own identity by the dial. With the seam's gate "
        "removed the entry door draws two bright lines across the departing work and stands %.2f of "
        "255 from its own file at a worst channel of %.0f, against 0.36 and 10 with the gate in "
        "place. IT IS READ ON THE WORST CHANNEL AND NOT ON THE MEAN, and that is the fault's own "
        "shape rather than a bar chosen to pass: a seam is a LINE, sixteen ten-thousandths of the "
        "frame wide at its core, so a mean over the whole frame divides a fully blown-out line by "
        "the frame that does not carry it. The mean moves by a factor of twelve and the worst "
        "channel by ten, and the frame is plainly not the photograph")

    # 3 · the hand's own two halves
    def hand_flat(br):
        v = js(br, "return window.__values(1);")
        d = host_at(br, 1.0, "red-hand-door")
        w = int(br.evaluate("String(document.querySelector('canvas[aria-hidden]').width)"))
        hh = int(br.evaluate("String(document.querySelector('canvas[aria-hidden]').height)"))
        file_ = work_in_the_frame(PHOTOS[1], w, hh)
        mean, _ = apart(d, file_)
        moved = (v.get("foldMap") or {}).get("movedPx", 0)
        return (bool(v["doorWhyNo"]) and moved > 2, moved, mean, (v["doorWhyNo"] or "")[:150])

    red(RED_ROWS[2],
        "      var dial = hand <= 0.5\n        ? feelOf(clamp01(hand / SHUT_IN))\n"
        "        : feelOf(1 - clamp01((hand - SHUT_OUT) / (1 - SHUT_OUT)));",
        "      var dial = feelOf(hand);",
        hand_flat,
        "the hand runs the fold in over the first forty-six hundredths, holds the wholly mirrored "
        "frame for eight and opens it out over the last forty-six, so the dial stands at nothing at "
        "BOTH ends. With the second half removed the exit door is the arriving work fully folded "
        "onto its own mirror: the fold moves a sample %.2f points of the buffer off its own place "
        "and the frame stands %.2f of 255 from its own file, and the instrument refuses the door — "
        "«%s»")

    # 4 · the room the fold needs at the frame's own edge
    def edge_gone(br):
        br.evaluate("window.__param('drift', 0); window.__param('axis', 0);"
                    "window.__param('centreX', 0.01); 0")
        br.sleep(0.45)
        v = js(br, "return window.__values(%r);" % SHUT_IN)
        p = host_at(br, SHUT_IN, "red-edge")
        return (v["lineHeld"] is None and abs(v["fold"][0] - 0.01) < 1e-9,
                v["fold"][0], standing(p)[1])

    red(RED_ROWS[3],
        "      var atX = clamp(wantX, LINE_EDGE, 1 - LINE_EDGE);",
        "      var atX = wantX;",
        edge_gone,
        "the module names a tenth of the frame as the room a fold needs — «with less than a tenth "
        "of the frame beyond it the fold has almost nothing left to mirror and the travel goes "
        "slack before it goes dead». With the room removed a score naming a place of 0.01 gets it: "
        "the line stands at %.4f with nothing held and the frame's own spread falls to %.1f, "
        "against a line held at 0.1000 and the hold on the record when the room stands")

shutil.rmtree(TMP, ignore_errors=True)

# ---------------------------------------------------------------- report
bad = [r for r in results if r[1] == "FAIL"]
print("\n%s\n" % __doc__.strip().splitlines()[0])
for name, mark, detail in results:
    print("%-6s %s" % (mark, name))
    if detail:
        print("       %s" % detail)
print("\n%d passed / %d failed / %d skipped"
      % (sum(1 for r in results if r[1] == "PASS"), len(bad),
         sum(1 for r in results if r[1] == "SKIP")))
sys.exit(1 if bad else 0)
