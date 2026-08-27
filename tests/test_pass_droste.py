#!/usr/bin/env python3
"""PASS-API-V1 — the droste instrument on the host's frame.
Run: python3 tests/test_pass_droste.py

Root: his word of 2026-08-18 08:52, after walking the live route — «переходы очень однообразные: у
тебя дофига эффектов и ты сделал все очень топорно». The lab holds 23 effect modules and the engine
held six instruments; this is one of them ported, so the composer has something more to cast. The
brief is docs/immersive/briefs/reports/lanes/PORT-common.md in the tlvphotos tree, and the artistic
law is lab/CROSSING-BRIEF.md, whose vocabulary table carries his own standing verdict on this effect:
«droste · внутрь себя · переход + vista · SURFACE · approved; conformal-with-rotation is its named
deep end».

WHAT THE INSTRUMENT DOES, so a reader of this file knows what the numbers below are about. The
photograph opens into a smaller copy of itself, and that copy into a smaller one again, without end;
the whole picture is sheared as it goes down, so lines running out of the middle wind into a spiral
and the eye falls along it toward a dark throat. Then a ring appears at the frame's own edge and
travels inward: outside it the copies belong to the arriving work, inside it to the departing one, so
the picture the visitor came in on shrinks ring by ring into the throat and vanishes at a point while
the other photograph closes in around it. Then the spiral unwinds, and what stands flat is the
arriving work.

WHAT IS COMPARED, AND AGAINST WHAT.

  The doors. At the dial's two ends one whole work stands, flat. Each is measured against ITS OWN
  FILE, cover-fitted into the frame and cropped by nothing at all — the spiral is a map of the frame
  onto itself and asks for no room beyond it — inside the project's seam threshold of 6 of 255.

  THE TWO ROADS. Both draw with WebGL2 and one fragment shader each, so the residual between them is
  a difference of arithmetic rather than of samplers. The module dives into ONE picture, so the two
  roads are compared exactly where one work stands on the frame: through the wind-in, where the
  departing work is alone, and through the wind-out, where the arriving one is.

  THE LAB MODULE IS SERVED WITH ITS SAMPLER LEVELLED, and the rows that read it say so. The host
  uploads one plain RGB texture per work, filtered linearly, with no mip chain and no anisotropy —
  one texture serving every instrument — while the module uploads its own sRGB texture, builds a mip
  chain over it and asks for anisotropy. Four literals of the served copy are changed so that both
  roads sample one way; not one line of the map or the finish is touched, and the file on disk is
  never written to.

  The handover. Mid-passage both works stand in one frame, and the arriving work's share — read off
  the instrument's own copy map, as colour — grows from nothing to whole across the middle third and
  nowhere else.

  The coverage. This instrument declares that it writes none, because it fills the frame. The alpha
  is the constant 1 in the served bytes, and the host's own placement rule is read for what that
  declaration buys: lowest of a stack, refused over a floor.

  No empty frame. The rows below sample the pass at seven instants and once across a change of
  viewport, and each frame has to stand as a picture.

  The lab module is READ ONLY. Absent, every browser row here is a pinned SKIP that names the missing
  path — never a silent pass.

NO PER-FILE BYTE FENCE IS WRITTEN HERE, and that is his word of 2026-08-18 08:47: the whole class is
being stripped from the project because it makes work rather than proving anything.
"""
import base64
import hashlib
import json
import os
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
# TWO WORKS BUILT AROUND A CENTRE, which is what this instrument asks a pair to read: a glass drum
# seen from below and a round tower, both of them concentric by construction.
PHOTOS = [LAB / "photos" / "glass-drum.jpg", LAB / "photos" / "round-tower.jpg"]
MODULE = LAB / "effects" / "droste.js"

SITE_URL = "https://synth.example.com"
VW, VH = 390, 844          # the phone frame lab/carrier-check.py measures on
SEAM = 6.0                 # the project's seam threshold, 6 of 255 (TRANSITION-STAGE-V0 §1)
FAR = 40.0                 # further than this from a file and it is a different picture
# WHAT MID-PASSAGE IS HELD TO, and why it is its own number. At a door the frame is one file and the
# bar is the project's seam of 6; away from a door the claim is only that the frame is NEITHER file,
# and a wound spiral of the arriving work standing where the flat photograph would stand can read as
# little as three times the seam from it while being plainly another picture. Three times the seam
# is what this asks for, and the readings stand beside it.
MID_FAR = 18.0
BACKGROUND = (0x08, 0x08, 0x0a)
SPREAD = 10.0
ROADS = SEAM

# The instrument's own three ported numbers, and the two the port added. Each is read out of both
# files by the constants row below rather than trusted here.
WIND_HOLD = 0.35           # how much of the passage the wind holds open at each end
SEAM_SHARE = 0.20          # the handover seam, as a share of one copy — the module's own dissolve
CLOCK = 2.7                # one second, handed to both roads

SHOTS = ROOT / "tests" / "captures" / "pass-droste"

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


DURATION_MS = 6500
WITHIN_MS = 500


def _static(v):
    return {"op": "static", "value": v}


def droste_cue(stack=0, **statics):
    """The cue, with a track for every one of the nine handles (§4.4b)."""
    P = {"size": 4, "turn": 0.32, "speed": 0.45, "centreX": 0.5, "centreY": 0.5,
         "shade": 1, "mask": 0}
    P.update(statics)
    nodes = {"d-mix": {"source": "progress"}, "d-clock": {"source": "time"}}
    tracks = {"mix": {"node": "d-mix"}, "clock": {"node": "d-clock"}}
    for k, v in P.items():
        nodes["d-" + k] = _static(v)
        tracks[k] = {"node": "d-" + k}
    return {
        "id": "droste-main", "instrument": {"id": "droste", "api": 1},
        "voice": "letter", "roles": ["disassembly", "mystery", "assembly"],
        "levels": ["SURFACE"],
        "levelOwnership": {"SURFACE": "owns"},
        "window": [0, DURATION_MS / 1000.0], "works": ["a", "b"], "stack": stack,
        "cameraAuthority": "stage",
        "doors": {"in": {"handle": "mix", "value": 0, "measured": True},
                  "out": {"handle": "mix", "value": 1, "measured": True}},
        "nodes": nodes, "tracks": tracks,
        "resources": {"textures": 0, "textureSlots": 2, "framebuffers": 0, "pingPong": 0,
                      "programs": 1, "passes": 1, "bytesEstimate": 0, "variant": "standard"},
    }


def droste_score(**statics):
    cues = [droste_cue(**statics)]
    res = {"textures": 0, "textureSlots": 2, "framebuffers": 0, "pingPong": 0, "programs": 1,
           "passes": 1, "bytesEstimate": 0}
    return {
        "schema": 2,
        "intent": "the photograph opens into a smaller copy of itself without end and the copies "
                  "wind away into a spiral; the arriving work closes in from the frame's own edge "
                  "ring by ring while the departing one falls into the throat and vanishes at a "
                  "point (lab/effects/droste.js:1-8, its own header)",
        "pair": {"a": "a", "b": "b"},
        "seed": 4.91016,
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
        "provenance": {"source": "lab/effects/droste.js's own declared defaults and constants",
                       "measuredAt": None, "by": "tests/test_pass_droste.py"},
    }


# ---------------------------------------------------------------- bake once
build_site.SITE_CONFIG = dict(build_site.SITE_CONFIG)
build_site.SITE_CONFIG["pass"] = {"visualLayer": "pass", "diagnostics": "on"}

TMP = Path(tempfile.mkdtemp(prefix="synth_passdroste_"))
build_site.OUT = TMP
build_site.build(SITE_URL)
# THE INSTRUMENT'S OWN BUILT FILE — the real artifact a visitor is served, comments stripped. Since
# every instrument travels alone, the whole of this file is this instrument and nothing else.
PACK = (TMP / "pass-inst-droste.js").read_text(encoding="utf-8")
REGION = PACK
SOURCE = ROOT / "engine" / "assets" / "pass-inst-droste.js"
# The file as it stands in the tree, comments and all: the rows about what this instrument DECLARES
# read the built artifact, and the rows about what it SAYS read the source it is built from.
SOURCE_TEXT = SOURCE.read_text(encoding="utf-8")
LABTXT = MODULE.read_text(encoding="utf-8") if MODULE.exists() else ""

# ---------------------------------------------------------------- string rows

OWNED = ["createElement", "getContext", "requestAnimationFrame", "addEventListener",
         "performance.now", "Date.now", "new Image", "setTimeout", "setInterval"]
held = [s for s in OWNED if s in REGION]
check("PASS-DROSTE the instrument creates no element, no loop and no listener",
      not held,
      "§1.2's fence, read against the instrument's own built file: none of the nine ways of owning "
      "hardware appears there. The module raises its own canvas, takes a WebGL2 context on it, "
      "uploads two textures with their mip chains, runs its own frame loop, observes its own mount "
      "for a resize and listens for the pointer; all of it stayed in the lab"
      if not held else "the instrument's region holds " + ", ".join(held))

HANDLES = ["mix", "clock", "size", "turn", "speed", "centreX", "centreY", "shade", "mask"]
absent = [h for h in HANDLES if ("%s: { min" % h) not in REGION]
check("PASS-DROSTE every handle the instrument publishes is a handle a score can drive",
      not absent and len(HANDLES) == 9,
      "§4.4b: nine handles. The dial, the second the host hands down, the module's own three "
      "declared params a pair can stand — how many copies, how far they wind, how fast the dive "
      "falls — the two that carry the throat's own place, the darkening the module keeps to itself, "
      "and the judges' channel. The module's `picture` param is published by neither name, and the "
      "file says why: a cue carries an ordered pair, so which work stands where is the passage's "
      "own question and the ring answers it"
      if not absent else "these are published nowhere: " + ", ".join(absent))

check("PASS-DROSTE no die is published, and the picture is what settles it",
      "seed: { min" not in REGION and "Math.random" not in LABTXT
      and "Math.random" not in REGION,
      "nothing in this picture is rolled: the centre's wander, the breathing bend, the dive and the "
      "turn are closed forms of the handed second, so a seeded run repeats to the point and a die "
      "would be a handle a score could walk without moving anything. The module rolls nothing "
      "either, which is what makes this a reading of the picture rather than a preference")

# Every constant the picture stands on, read out of the lab module and out of the built file. The
# left column is the module's own text; the right is what the built instrument must carry.
CONSTANTS = [
    ("Math.log(Math.pow(40, 1 / copies))", "Math.log(Math.pow(DIVE_SPAN, 1 / copies))",
     "one repeat is the log of the fortieth root taken `copies` times, so the whole dive is one "
     "fall of forty whatever the count"),
    ("smoothstep(0.40, 0.60, f)", "smoothstep(0.40, 0.60, f)",
     "the dissolve between one copy and the next, a fifth of a copy wide"),
    ("float e = (f - 0.5) / 0.12;", "float e = (f - 0.5) / 0.12;",
     "the dark rim on the seam, and where it stands"),
    ("float rim = 1.0 - 0.55 * exp(-e * e);", "float rim = 1.0 - 0.55 * exp(-e * e);",
     "how deep that rim goes"),
    ("smoothstep(0.0, 0.22, r)", "smoothstep(0.0, 0.22, r)", "how far the well reaches out"),
    ("0.55 * smoothstep(0.34, 0.96, length(vp))", "0.55 * smoothstep(0.34, 0.96, length(vp))",
     "the corners falling away, so the eye stays on the sharp turns"),
    ("0.50 * smoothstep(0.75, 1.70, r)", "0.50 * smoothstep(0.75, 1.70, r)",
     "the far side sinking where the throat stands out at an edge"),
    ("uniform1f(U.uWell, 0.05)", "var WELL = 0.05;", "how dark the throat goes"),
    ("pow(lin, vec3(1.0 / 2.2))", "pow(lin, vec3(1.0 / 2.2))", "the module's own gamma"),
    ("mix(1.0, 1.14, d) + 0.5", "mix(1.0, 1.14, d) + 0.5", "the bite the dissolve takes away"),
    ("mix(1.0, 1.20, d)", "mix(1.0, 1.20, d)", "the lift of colour"),
    ("1.15) * 1.75", "1.15) * 1.75", "the turn's own response curve and its reach in radians"),
    ("1.35) * 0.95", "1.35) * 0.95", "the dive's own response curve and its reach"),
    ("0.16 * Math.sin(", "0.16 * Math.sin(", "the throat's wander, first period"),
    ("0.05 * Math.sin(t * 0.31)", "0.05 * Math.sin(t * 0.31)", "its second"),
    ("0.12 * Math.cos(t * 0.083)", "0.12 * Math.cos(t * 0.083)", "its third, up the frame"),
    ("1.0 + 0.62 * Math.sin(t * 0.14)", "1.0 + 0.62 * Math.sin(t * 0.14)", "the breathing bend"),
    ("(0.62 / 0.14) * (1 - Math.cos(t * 0.14))", "(0.62 / 0.14) * (1 - Math.cos(t * 0.14))",
     "the turn, integrated in closed form against that bend"),
    ("var CENTRE_REACH = 0.5;", "var CENTRE_REACH = 0.5;", "a named throat's own reach"),
    ("max(dot(p, p), 1e-14)", "max(dot(p, p), 1e-14)",
     "the guard at the throat's singular point, which is also where the ring's travel ends"),
]
missing_const = [(a, b) for a, b, _ in CONSTANTS if a not in LABTXT or b not in REGION]
check("PASS-DROSTE every number the picture stands on is the module's own, digit for digit",
      LABTXT and not missing_const,
      "%d constants read out of lab/effects/droste.js and out of the built instrument: %s"
      % (len(CONSTANTS), "; ".join(why for _, _, why in CONSTANTS))
      if not missing_const else "these did not match: %s" % missing_const)

PORTS_OWN = [
    ("var WIND_HOLD = 0.35;", "how much of the passage the wind holds open at each end"),
    ("var SEAM_SHARE = 0.20;", "the handover's own seam, a share of one copy"),
    ("var rRing = rHi + (rLo - rHi) * hand;",
     "the ring travels evenly in the RADIUS and not in the logarithm the picture is written in"),
]
own_missing = [c for c, _ in PORTS_OWN if c not in REGION]
# BEHAVIOUR NOT TEXT. A grep of "THE PORT'S OWN NUMBER"/"IT TRAVELS IN THE RADIUS" beside the
# formula proves only that the heading and the formula sit in the same file — a defect could stand
# right beside them and the row would still pass. That the ring travels in the RADIUS and not in
# the LOGARITHM the picture is written in is a claim about rendered pixels, and it is proved on
# rendered pixels: RED_ROWS[3] below reverts exactly this line to the logarithm and reads how far
# the frame's own share of the two works moves at the middle of the handover. This row keeps only
# what it can check without a browser — that the module's own numbers actually reached the built
# file.
check("PASS-DROSTE the port's own numbers stand in the built file, and the ring's own travel is proved on the picture",
      not own_missing,
      "the module has no passage and no doors, so what nothing in it measured had to be decided "
      "here: %s. The seam is the module's own dissolve width read back as a number; the hold and "
      "the travel are the two real choices. That the travel is walked in the radius rather than "
      "the logarithm is read on the rendered frame in RED_ROWS[3] further below, not grepped here"
      % "; ".join("%s — %s" % (c, why) for c, why in PORTS_OWN)
      if not own_missing else "missing from the built file: %s" % own_missing)

# BEHAVIOUR NOT TEXT. A grep of "HOW ONE PHOTOGRAPH BECAME TWO" proves only that the heading is in
# the file. What actually proves the module's one-picture choice became this port's ordered pair is
# the manifest's own `arity` (fetched off the running instrument, BROWSER_ROWS[0] below) and the two
# doors standing on their own files (BROWSER_ROWS further below) — not a citation of the heading
# that introduces them.
check("PASS-DROSTE the module's own single picture becomes an ordered pair, and the doors below say how",
      "picture" in LABTXT and "'first', 'second'" in LABTXT.replace('"', "'")
      and "picture" not in HANDLES,
      "the module picks the first or the second photograph and never draws the other; this port "
      "declares no `picture` handle at all — read off HANDLES rather than grepped — and instead "
      "carries the ordered pair as its manifest's own arity of 2 (BROWSER_ROWS[0]), so a cue of "
      "this engine owes a door at each end. The two works meet on a ring about the work's own "
      "centre, at the seam the module's own arithmetic already draws, and the ring travels one way "
      "and completes — so nothing is retraced and both doors are exact by construction rather than "
      "by tolerance, which the door rows below measure rather than this one")

check("PASS-DROSTE the shader is written in the one dialect the fleet is written in",
      REGION.count("#version") == 0 and "textureGrad" in REGION
      and "gl_FragColor = vec4(col, 1.0);" in REGION
      and "attribute vec2 aPos;" in REGION
      and "#version 300 es" in LABTXT,
      "the module carries its own «#version 300 es» header and the host hands a source that has one "
      "through untouched, so keeping it would have compiled — but the fleet's own rows read these "
      "files as one fleet in one dialect, and an instrument speaking a second one makes every such "
      "row answer for a difference that means nothing. The header is left to the host's own "
      "translator. `textureGrad` — the module's exact derivatives of the read position, so the "
      "sampler picks a sane footprint across the ring where the pattern wraps — needs the second "
      "version of the language and survives the stamping unchanged")

missing = [str(p) for p in ([MODULE] + PHOTOS) if not p.exists()]

BROWSER_ROWS = [
    "PASS-DROSTE §8     · the manifest, read off the registered instrument",
    "PASS-DROSTE the charter's shelf: SURFACE, and rings are what it cuts on",
    "PASS-DROSTE door 0 is the departing work's own file, standing flat",
    "PASS-DROSTE door 0 stands far from the arriving work",
    "PASS-DROSTE door 1 is the arriving work's own file, standing flat",
    "PASS-DROSTE door 1 stands far from the departing work",
    "PASS-DROSTE the two roads agree wherever one work stands on the frame",
    "PASS-DROSTE the handover: mid-passage both works stand in one frame, and the ring travels inward",
    "PASS-DROSTE §7     · it fills the frame, and the host places it by that declaration",
    "PASS-DROSTE §4.4b  · the copies, the wind, the dive, the throat and the darkening reach the PICTURE",
    "PASS-DROSTE §7     · no empty frame at seven instants, nor across a change of viewport",
    "PASS-DROSTE the ring is WALKED on the drawing buffer at both doors, and what it read is published",
    "PASS-DROSTE a door the judges' channel spoils is refused on the real road, and the visitor still lands",
    "PASS-DROSTE the real transaction road: curtain up, one pass drawn, exactly one dock at the end",
    "PASS-DROSTE §7     · one canvas, one context, two source textures, one pass a frame",
    "PASS-DROSTE row 9  · one camera authority through a real pass, and the pose rests on the arrival",
    "PASS-DROSTE two runs of one score draw one picture, to the point",
    "PASS-DROSTE the console stayed quiet",
    "PASS-DROSTE row 16 · the captures are kept as evidence",
]

RED_ROWS = [
    "PASS-DROSTE red-on-bug · the ring's reach taken off the frame's own corners: the entry door leaks and is refused",
    "PASS-DROSTE red-on-bug · the ring's travel removed: the arriving work never arrives, and the door is refused",
    "PASS-DROSTE red-on-bug · the wind's gate on the finish removed: the entry door stops being the file",
    "PASS-DROSTE red-on-bug · the ring walked in the logarithm: the handover is over before the middle",
]


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


def arriving_share(p):
    """The share of the frame the ARRIVING work carries, read off the copy map. The map paints that
    share into the red channel at every point, so the channel's own mean is the answer."""
    from PIL import Image, ImageStat
    a = Image.open(p).convert("RGB")
    return ImageStat.Stat(a.split()[0]).mean[0] / 255.0


def cover_into(im, w, h):
    from PIL import Image
    iw, ih = im.size
    fa, ia = w / float(h), iw / float(ih)
    sw, sh = (ih * fa, float(ih)) if ia > fa else (float(iw), iw / fa)
    x0, y0 = (iw - sw) / 2.0, (ih - sh) / 2.0
    return im.resize((w, h), Image.BILINEAR, box=(x0, y0, x0 + sw, y0 + sh))


def work_in_the_frame(src, w, h):
    """The whole file, cover-fitted into the frame. Neither door crops: the spiral is a map of the
    frame onto itself and asks for no room beyond it, which is what `framings` publishes."""
    from PIL import Image
    return cover_into(Image.open(src).convert("RGB"), w, h)


def apart(p, work):
    from PIL import Image, ImageChops, ImageStat
    a = Image.open(p).convert("RGB")
    if a.size != work.size:
        return 255.0, 255.0
    st = ImageStat.Stat(ImageChops.difference(a, work))
    return sum(st.mean) / 3.0, max(m for _, m in st.extrema)


# THE LAB MODULE AS THE BENCH SERVES IT: its sampler levelled to the host's, and nothing else. The
# host uploads one plain RGB texture per work, filtered linearly, with no mip chain and no
# anisotropy — one texture serving every instrument — while the module uploads an sRGB texture,
# mips it and asks for anisotropy. So the served copy is given the host's own texture state, and its
# two reads are wrapped in the exact inverse of the transfer its sampler used to undo for free. Not
# one line of the map or the finish is touched. The file on disk is never written to.
LAB_LEVEL = [
    ("gl.SRGB8_ALPHA8", "gl.RGBA"),
    ("gl.LINEAR_MIPMAP_LINEAR", "gl.LINEAR"),
    ("var anisoMax = aniso ? Math.min(8, gl.getParameter(aniso.MAX_TEXTURE_MAX_ANISOTROPY_EXT)) : 0;",
     "var anisoMax = 0;"),
    ("    'precision highp float;',",
     "    'precision highp float;',\n"
     "    'vec3 toLin(vec3 c){ return mix(c / 12.92, pow((c + 0.055) / 1.055, vec3(2.4)),"
     " step(vec3(0.04045), c)); }',\n"
     "    'vec4 tgLin(sampler2D t, vec2 uv, vec2 gx, vec2 gy){ vec4 c = textureGrad(t, uv, gx, gy);"
     " return vec4(toLin(c.rgb), c.a); }',"),
    ("textureGrad(uTex,", "tgLin(uTex,"),
]


def levelled_module(text):
    for src, dst in LAB_LEVEL:
        if src not in text:
            return None
        text = text.replace(src, dst)
    return text


LABSERVED = levelled_module(LABTXT) if LABTXT else None


def bench_dir(pack_text=None):
    """The bench's own served root: the BUILT pass-layer.js, the site's own settings record and the
    BUILT instrument files it names — the real artifacts, namespace applied and comments stripped —
    the lab module with its sampler levelled, the two photographs, and the page that stands the two
    roads of one frame side by side.

    A row proving a rule reds hands over a CHANGED instrument file and writes the record with the
    digest of the bytes actually served, which is what the build does. The source file on disk is
    never touched, so nothing has to be restored and no working tree can be left changed by a
    red-on-bug proof."""
    d = Path(tempfile.mkdtemp(prefix="synth_drostebench_"))
    pack = PACK if pack_text is None else pack_text
    shutil.copy2(TMP / "pass-layer.js", d / "pass-layer.js")
    for _inst in sorted(TMP.glob("pass-inst-*.js")):
        shutil.copy2(_inst, d / _inst.name)
    (d / "pass-inst-droste.js").write_text(pack, encoding="utf-8")
    record = json.loads((TMP / "config.json").read_text(encoding="utf-8"))
    record["pass"]["instruments"]["droste"]["digest"] = hashlib.sha256(
        pack.encode("utf-8")).hexdigest()
    (d / "config.json").write_text(json.dumps(record), encoding="utf-8")
    (d / "droste.js").write_text(LABSERVED, encoding="utf-8")
    (d / "photos").mkdir()
    for p in PHOTOS:
        shutil.copy2(p, d / "photos" / p.name)
    shutil.copy2(ROOT / "tests" / "fixture_pass_droste.html", d / "index.html")
    return d


def ready(br, tries=120):
    for _ in range(tries):
        if br.evaluate("String(!!window.__ready)") == "true":
            return True
        br.sleep(0.25)
    return False


def js(br, expr):
    return json.loads(br.evaluate("JSON.stringify((function(){%s})())" % expr))


def drawn(br, tries=40, nap=0.05):
    """WAIT FOR THE FRAME RATHER THAN FOR A CLOCK, and for the curtain with it. A fixed sleep after
    an offer measures the machine as much as the picture, and this machine is shared with several
    other suites at once: the first offer of a session builds the programme and arms both sources,
    and under load it can take longer than any sleep worth writing. Two things have to be true
    before a screenshot means anything — the host has laid a cue down, and its own canvas is the
    thing on screen — so both are read, and what was read comes back for a row to print."""
    seen = None
    for _ in range(tries):  # noqa: B007
        seen = js(br, "var c = document.querySelector('canvas[aria-hidden]');"
                      "var r = window.__report();"
                      "return {state: r.state, drew: r.drew, "
                      "shown: !!c && c.style.visibility === 'visible'};")
        if (seen["drew"] or 0) >= 1 and seen["shown"] and seen["state"] == "running":
            br.sleep(0.1)
            return seen
        br.sleep(nap)
    return seen


def instant(br, score, at, path, tries=2):
    """ONE INSTANT OF A REAL PASS, PHOTOGRAPHED WHILE IT IS STILL A PASS. A pinned run never reaches
    its own last door, so it never settles, and the host's own watchdog lands it once its duration
    and slack are spent — after which the curtain is down and a screenshot is of the page and not of
    the picture. That is the host doing its job, not the instrument failing at one; a visitor's pass
    is never pinned. So the shot is taken as soon as the host has drawn and its canvas is up, and
    where it still arrives after the landing the instant is offered once more. What was read comes
    back with it."""
    for _ in range(tries):
        js(br, "return window.__offer(%s, {clock: 1.5, progress: %r});" % (score, at))
        w = drawn(br)
        p = png(br, path)
        st = standing(p)
        br.evaluate("window.__cancel('instant sweep'); 0")
        idle(br)
        if st[1] > 0:
            return st, w
    return st, w


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


def roads(br, at, tag, work):
    """BOTH ROADS AT ONE POSE. The module has no passage of its own, so it is handed what the port
    DERIVED from the dial — the wind, the second and the throat's own place across the frame — and
    computes the dive, the turn, the wander and the bend from that second by the same closed form
    the port does. `work` names which photograph the module dives into, since it draws one and the
    port draws both."""
    js(br, "return window.__work(%r);" % work)
    r = js(br, "return window.__both(%r, %r);" % (at, CLOCK))
    br.sleep(0.45)
    br.evaluate("window.__hostDraw(); 0")
    br.sleep(0.15)
    br.evaluate("window.__show('host'); 0")
    br.sleep(0.25)
    ph = png(br, SHOTS / (tag + "-host.png"))
    br.evaluate("window.__show('module'); 0")
    br.sleep(0.3)
    pm = png(br, SHOTS / (tag + "-module.png"))
    br.evaluate("window.__show('host'); 0")
    return r, ph, pm


def host_shot(br, tag, over=None):
    br.evaluate("window.__hostDraw(%s); window.__show('host'); 0" % json.dumps(over or {}))
    br.sleep(0.3)
    return png(br, SHOTS / (tag + ".png"))


def copy_map(br, at, tag):
    p = host_shot(br, "map-" + tag, {"mix": at, "clock": CLOCK, "mask": 1})
    return arriving_share(p)


if not chrome_available():
    for r in BROWSER_ROWS + RED_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
elif missing:
    for r in BROWSER_ROWS + RED_ROWS:
        skip(r, "the lab tree is read-only source material and is absent here: " + missing[0])
elif LABSERVED is None:
    for r in BROWSER_ROWS + RED_ROWS:
        skip(r, "the lab module no longer carries the four literals the bench levels its sampler "
                "with; the leveling has to be re-read before the two roads mean anything")
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
            elif not js(br, "return !!window.__exPass.bench.manifest('droste');"):
                why = js(br, "var e = window.__host.report().events.filter(function(x){"
                             "return x.name === 'manifest-refused';});"
                             "return e.length ? e[e.length - 1].why : null;")
                for r in BROWSER_ROWS:
                    check(r, False, "the host registered no «droste» instrument: " + str(why))
            else:
                SCORE = json.dumps(droste_score())

                # ---- §8: the manifest, read off the registered instrument -----------------------
                m = js(br, "return window.__exPass.bench.manifest('droste');")
                res = m["resources"]
                need = ["id", "api", "arity", "roles", "params", "handles", "neutrals", "doors",
                        "framings", "drivers", "camera", "gl", "passes", "resources",
                        "capabilities", "decline", "provenance", "readiness", "coverage", "levels",
                        "cuts", "asks"]
                shape = (
                    all(k in m for k in need)
                    and m["id"] == "droste" and m["api"] == 1 and m["arity"] == 2
                    and m["roles"] == ["disassembly", "mystery", "assembly"]
                    and sorted(m["params"]) == ["centreX", "centreY", "size", "speed", "turn"]
                    and len(m["handles"]) == 9
                    and all(set(h) >= {"min", "max", "def"} for h in m["handles"].values())
                    and m["neutrals"] == {"a": 0, "b": 1}
                    and m["doors"]["in"]["handle"] == "mix" and m["doors"]["in"]["value"] == 0
                    and m["doors"]["out"]["handle"] == "mix" and m["doors"]["out"]["value"] == 1
                    and sorted(m["framings"]) == ["0", "1"]
                    and m["framings"]["0"] == {"coverCrop": 1} == m["framings"]["1"]
                    and m["camera"] == {"needs": "none", "authority": "stage"}
                    # `readsChain` was declared at the merge (2026-08-18): the dive minifies hard
                    # near the throat and the host binds one plain texture per work, so the deep
                    # copies alias where a chain of smaller copies would have resolved them. The
                    # flag asks the host for that chain, and `textureGrad` already carries the
                    # derivatives to walk it with.
                    and m["gl"] == {"preserveDrawingBuffer": False, "readsChain": True}
                    and len(m["passes"]) == 1 and len(m["passes"][0]["uniforms"]) == 10
                    and sorted(res) == ["lean", "rich", "standard"]
                    and all("bytesEstimate" in res[v] and res[v]["programs"] == 1
                            and res[v]["passes"] == 1 and res[v]["textureSlots"] == 2
                            for v in res)
                    and m["capabilities"] == ["webgl2"] and m["decline"]
                    and m["coverage"]["writes"] is False and m["coverage"]["how"]
                    and m["provenance"]["labPath"] == "lab/effects/droste.js"
                    and m["readiness"] == "production-ready"
                    and "droste" in js(br, "return window.__host.report().registered;"))
                check(BROWSER_ROWS[0], shape,
                      f"nine handles, ten uniforms in one pass, both doors at a cover crop of "
                      f"{m['framings']['0']['coverCrop']} — the spiral takes no room beyond the "
                      f"frame — resources declared for three tiers with a byte estimate of "
                      f"{res['standard']['bytesEstimate']}, and a coverage block reading "
                      f"«{m['coverage']['how']}»")

                check(BROWSER_ROWS[1],
                      m["levels"] == ["SURFACE"] and m["cuts"] == ["ring"]
                      and m["asks"]["measure"] == "radial"
                      and m["asks"]["floor"] == "radial_tight",
                      f"levels={m['levels']}, cuts={m['cuts']}, read off the manifest "
                      f"bench.manifest() actually hands back rather than grepped off a comment "
                      f"citing the charter's shelf. The level is his own standing "
                      f"verdict in the vocabulary table of lab/CROSSING-BRIEF.md — «droste · внутрь "
                      f"себя · переход + vista · SURFACE» — and the cut is what the picture is made "
                      f"of: the copies are annuli about the work's own measured centre and the two "
                      f"works exchange on one of them. What a pair must read stands on the manifest "
                      f"in the instrument's own words: «{m['asks']['says'][:210]}…»")

                w = int(br.evaluate("String(window.__exPass.bench.make() && "
                                    "document.querySelector('canvas[aria-hidden]').width)"))
                h = int(br.evaluate("String(document.querySelector('canvas[aria-hidden]').height)"))
                bufs = js(br, "return window.__buffers();")
                drum = work_in_the_frame(BENCH / "photos" / "glass-drum.jpg", w, h)
                tower = work_in_the_frame(BENCH / "photos" / "round-tower.jpg", w, h)

                # ---- the poses, on both roads ---------------------------------------------------
                # THE TWO ROADS ARE COMPARED WHERE ONE WORK STANDS. Through the wind-in the ring has
                # not started and the departing work is alone on the frame; through the wind-out it
                # has finished and the arriving work is. Between them both works stand at once,
                # which the module has no way to draw, so the handover is measured on its own terms
                # two rows down.
                A_SIDE = [("in-000", 0.0), ("in-010", 0.10), ("in-020", 0.20), ("in-030", 0.30),
                          ("in-035", 0.35)]
                B_SIDE = [("out-065", 0.65), ("out-075", 0.75), ("out-090", 0.90),
                          ("out-100", 1.0)]
                shots, reads = {}, {}
                for tag, at in A_SIDE:
                    reads[tag], hp, mp = roads(br, at, tag, "a")
                    shots[tag] = (hp, mp)
                for tag, at in B_SIDE:
                    reads[tag], hp, mp = roads(br, at, tag, "b")
                    shots[tag] = (hp, mp)

                for i, (door, own, other, ownn, othern) in enumerate((
                        ("in-000", drum, tower, "glass-drum.jpg", "round-tower.jpg"),
                        ("out-100", tower, drum, "round-tower.jpg", "glass-drum.jpg"))):
                    a, amx = apart(shots[door][0], own)
                    check(BROWSER_ROWS[2 + i * 2], a <= SEAM,
                          f"{door} against {ownn}, cover-fitted and uncropped: mean {a:.4f} of 255 "
                          f"(threshold {SEAM}), worst channel {amx}. The wind is a product of two "
                          f"smooth steps at its own zero at both ends, so every term of the "
                          f"spiral's finish is gated out; the ring stands a whole seam beyond the "
                          f"frame's farthest corner at one door and past the throat's own singular "
                          f"point at the other; and the door encodes with the exact inverse of the "
                          f"transfer "
                          f"the fetch undid, so what the frame carries is the file's own bytes")
                    o, _ = apart(shots[door][0], other)
                    check(BROWSER_ROWS[3 + i * 2], o >= FAR,
                          f"{door} against {othern}: mean {o:.4f} of 255 (must exceed {FAR})")

                agree = [(t, ) + diff(*shots[t]) for t, _ in A_SIDE + B_SIDE]
                check(BROWSER_ROWS[6],
                      all(mn <= ROADS for _, mn, _ in agree)
                      and bufs["host"] == bufs["module"],
                      "; ".join(f"{t}: mean {mn:.4f} of 255 (bar {ROADS}), worst channel {mx}"
                                for t, mn, mx in agree)
                      + f". Both roads drew on a {bufs['host']} buffer. The module is handed the "
                        f"wind the port computed and the very second the port used, and works out "
                        f"the dive, the turn, the wander and the bend from that second by the same "
                        f"closed form; its sampler is levelled to the host's — a plain RGB texture, "
                        f"linear filtering, no mip chain, no anisotropy, and the file's own "
                        f"transfer undone in the shader instead of by the sampler — and nothing "
                        f"else about it is touched")

                # ---- the handover, on the instrument's own terms ---------------------------------
                MIDS = [("h-040", 0.40), ("h-050", 0.50), ("h-060", 0.60)]
                mid_shots = {}
                for tag, at in MIDS:
                    mid_shots[tag] = host_shot(br, tag, {"mix": at, "clock": CLOCK})
                both_at = [(t, apart(mid_shots[t], drum)[0], apart(mid_shots[t], tower)[0])
                           for t, _ in MIDS]
                ladder = [(at, copy_map(br, at, "%03d" % round(at * 100)))
                          for at in (0.0, 0.35, 0.42, 0.5, 0.58, 0.65, 1.0)]
                shares = [s for _, s in ladder]
                check(BROWSER_ROWS[7],
                      all(da >= MID_FAR and db >= MID_FAR for _, da, db in both_at)
                      and shares[0] <= 0.01 and shares[1] <= 0.01
                      and shares[-1] >= 0.99 and shares[-2] >= 0.99
                      and all(shares[i] < shares[i + 1] for i in range(1, 5)),
                      "the arriving work's share of the frame, read off the copy map: "
                      + "; ".join(f"mix {at}: {s * 100:.2f}%" for at, s in ladder)
                      + ". It is nothing until the spiral stands open and whole before it closes, "
                        "so the two works exchange INSIDE the spiral and never on the flat, and the "
                        "ring travels one way. Mid-passage the frame stands far from both files — "
                      + "; ".join(f"{t}: {da:.1f} from the first, {db:.1f} from the second"
                                  for t, da, db in both_at)
                      + f" (bar {MID_FAR}) — which is what two photographs wound into one spiral "
                        f"looks "
                        f"like on a measurement")

                # ---- §7: the placement its declaration buys --------------------------------------
                place = js(br, """
                  var b = window.__exPass.bench;
                  return {declared: b.coverageOf('droste'),
                          asGround: b.coverageWhyNo([
                            {id: 'ground', instrument: {id: 'droste', api: 1}, stack: 0},
                            {id: 'over', instrument: {id: 'matter', api: 1}, stack: 1}]),
                          asRoof: b.coverageWhyNo([
                            {id: 'floor', instrument: {id: 'weave', api: 1}, stack: 0},
                            {id: 'ground', instrument: {id: 'droste', api: 1}, stack: 1}])};
                """)
                check(BROWSER_ROWS[8],
                      place["declared"] and place["declared"]["writes"] is False
                      and place["asGround"] is None
                      and isinstance(place["asRoof"], str) and "«droste»" in place["asRoof"]
                      and "gl_FragColor = vec4(col, 1.0);" in REGION,
                      f"the alpha is the constant 1 in the served bytes and the declaration says "
                      f"so, so the host places it by that: lowest of a stack with a "
                      f"coverage-writing voice above, the placement is lawful; laid over a floor "
                      f"that is itself lawful it is refused by name — «{place['asRoof']}». The ring "
                      f"cut had no instrument that could stand as a ground before this one, the "
                      f"meshing instrument being the only other that cuts on rings and writing "
                      f"coverage")

                # ---- §4.4b: the handles reach the picture ----------------------------------------
                # READ AT THE MIDDLE OF THE PASSAGE, where the spiral stands open and the ring is
                # crossing the frame, because that is the only place every one of these has
                # somewhere to show: at a door the wind gates the whole finish out by design.
                base_over = {"mix": 0.5, "clock": CLOCK}
                shot = {"base": host_shot(br, "handle-base", base_over)}
                for name, extra in (("size", {"size": 2}), ("turn", {"turn": 0.95}),
                                    ("speed", {"speed": 0.95}), ("centreX", {"centreX": 0.85}),
                                    ("centreY", {"centreY": 0.85}), ("shade", {"shade": 0.0}),
                                    ("clock", {"clock": CLOCK * 2}), ("mix", {"mix": 0.58})):
                    over = dict(base_over)
                    over.update(extra)
                    shot[name] = host_shot(br, "handle-" + name, over)
                moved = {k: diff(shot["base"], shot[k])
                         for k in ("size", "turn", "speed", "centreX", "centreY", "shade",
                                   "clock", "mix")}
                check(BROWSER_ROWS[9],
                      all(mn > SEAM for mn, _ in moved.values()),
                      "; ".join(f"{k} moves the frame by {mn:.4f} of 255, worst channel {mx}"
                                for k, (mn, mx) in moved.items())
                      + f" (floor {SEAM}). A handle a score drives and the picture ignores is what "
                        f"§4.4b is about; `speed` is read at a handed second rather than at zero, "
                        f"where a dive of any rate has gone nowhere yet")

                # ---- §7: no empty frame, and across a resize --------------------------------------
                empties, saw = [], []
                br.evaluate("window.__cancel('before the instant sweep'); 0")
                idle(br)
                for at in (0.0, 0.15, 0.3, 0.5, 0.7, 0.85, 1.0):
                    st, w = instant(br, SCORE, at,
                                    SHOTS / ("instant-%03d.png" % round(at * 100)))
                    saw.append((at, w))
                    empties.append((at, ) + st)
                js(br, "return window.__offer(%s, {clock: 1.5, progress: 0.5});" % SCORE)
                drawn(br, nap=0.05)
                br.set_viewport(VW - 80, VH - 120)
                br.sleep(0.6)
                p = png(br, SHOTS / "after-resize.png")
                sized = js(br, "return {w: document.querySelector('canvas[aria-hidden]').width, "
                               "buffer: window.__report().census.buffer, "
                               "pdb: window.__report().census.preserveDrawingBuffer};")
                rd, rs = standing(p)
                br.evaluate("window.__cancel('resize row'); 0")
                idle(br)
                br.set_viewport(VW, VH)
                br.sleep(0.4)
                check(BROWSER_ROWS[10],
                      all(d >= FAR and s >= SPREAD for _, d, s in empties)
                      and rd >= FAR and rs >= SPREAD and sized["pdb"] is False,
                      "; ".join(f"at {at}: {d:.2f} from the background, spread {s:.2f}"
                                for at, d, s in empties)
                      + " — each read once the host had laid its cue down and its own canvas was "
                        "what stood on screen: "
                      + "; ".join(f"{at}: {w}" for at, w in saw)
                      + f" (bars: {FAR} and {SPREAD}). After the viewport moved to "
                        f"{VW - 80}x{VH - 120} the buffer reads {sized['buffer']} and the frame "
                        f"stands {rd:.2f} from the background with a spread of {rs:.2f}; the "
                        f"context keeps preserveDrawingBuffer={sized['pdb']}. The ring's own two "
                        f"ends are read off the frame's corners and the buffer's own point, so both "
                        f"are rebuilt at the new grid rather than carried over")

                # ---- THE RING, WALKED ON THE DRAWING BUFFER --------------------------------------
                # The rows above photograph the copy map and read it as colour. This one asks the
                # INSTRUMENT what it read for itself at the instant it was about to draw, on the
                # grid the shader samples on: how much of the other work stood at any of the
                # buffer's own sample points, and how much room in copies of the dive the tightest
                # of them had to spare.
                def door_pose(mix=0, buf=None, **over):
                    p = {"mix": mix, "clock": CLOCK, "size": 4, "turn": 0.32, "speed": 0.45,
                         "centreX": 0.5, "centreY": 0.5, "shade": 1, "mask": 0, "reduced": False,
                         "cssWidth": VW, "cssHeight": VH}
                    p.update(over)
                    if buf:
                        p["bufWidth"], p["bufHeight"] = int(buf[0]), int(buf[1])
                    return p

                def values_of(p):
                    return js(br, "return window.__exPass.bench.values('droste', %s);"
                              % json.dumps(p))

                grids = [(VW, VH), (VW * 2, VH * 2), (195, 422), (1440, 900), (40, 60)]
                walked = {}
                for mixv in (0, 1):
                    for sz in (2, 6):
                        for g in grids:
                            walked[(mixv, sz, g)] = values_of(
                                door_pose(mix=mixv, size=sz, buf=g))
                away = values_of(door_pose(mix=0.5, buf=grids[0]))
                on_css = values_of(door_pose())
                wrong = [k for k, v in walked.items()
                         if v["ringMap"] is None or v["ringMap"]["worst"] > 0
                         or v["ringMap"]["walked"] != 18 or v["ringMap"]["spareCopies"] <= 0
                         or v["doorWhyNo"] is not None or v["doorHeld"] is not None
                         or v["wind"] != 0]
                one = walked[(0, 2, grids[0])]["ringMap"]
                check(BROWSER_ROWS[11],
                      not wrong and len(walked) == 20
                      and on_css["doorGrid"] == {"w": VW, "h": VH, "drawn": False, "given": True}
                      and walked[(0, 2, grids[0])]["doorGrid"] == {"w": VW, "h": VH, "drawn": True,
                                                                   "given": True}
                      and away["ringMap"] is None and away["doorGrid"] is None,
                      "%d readings — both doors, the fewest copies and the most, five grids from %s "
                      "to %s — and every one of them walked %d points of the buffer with the other "
                      "work standing at %g of the frame's own colour at the worst of them, the "
                      "tightest with %.4f of a copy to spare, against a bar of half a level of 255. "
                      "Away from a door nothing is read at all (grid %s), and nothing is ever held: "
                      "the ring's two ends are computed from the frame the shader draws on, so a "
                      "fault this reading finds is refused rather than closed. The reading at the "
                      "entry door on %s: %s"
                      % (len(walked), "%dx%d" % grids[0], "%dx%d" % grids[4],
                         one["walked"], one["worst"], one["spareCopies"],
                         away["doorGrid"], "%dx%d" % grids[1],
                         walked[(0, 2, grids[1])]["ringMap"]))

                # ---- THE DOOR REFUSED ON THE REAL TRANSACTION ROAD -------------------------------
                # The reading above comes out whole on every buffer this host can hand and every
                # pose these handles admit, which is the runtime truth his 18:00 decision asks for
                # and not a reason to leave the claim unread. The one door this instrument's own
                # handles CAN spoil is the judges' channel: `mask` draws the copy map itself as
                # colour, and a score that leaves it open at a door hands the visitor a false-colour
                # map instead of the photograph.
                def road(gen):
                    return js(br, "var r = window.__report(); return {state: r.state, "
                                  "drew: r.drew, buffer: r.census.buffer, "
                                  "refused: r.events.filter(function(e){ return e.gen === %d "
                                  "&& e.why && String(e.why).indexOf('door leaks') >= 0; })"
                                  ".map(function(e){ return e.name + ': ' + e.why; })};" % gen)

                br.evaluate("window.__cancel('door road row'); 0")
                idle(br)
                shut_gen = js(br, "return window.__offer(%s, {clock: 0, progress: 0});"
                              % json.dumps(droste_score(mask=0)))["gen"]
                drawn(br)
                played = road(shut_gen)
                br.evaluate("window.__cancel('door road row'); 0")
                idle(br)
                open_gen = js(br, "return window.__offer(%s, {clock: 0, progress: 0});"
                              % json.dumps(droste_score(mask=1)))["gen"]
                idle(br)
                leaked = road(open_gen)
                br.evaluate("window.__cancel('door road row'); 0")
                idle(br)
                check(BROWSER_ROWS[12],
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

                # ---- curtain up, one pass drawn, exactly one dock --------------------------------
                br.evaluate("window.__cancel('before the whole pass'); 0")
                idle(br, nap=0.05)
                br.evaluate("window.__hooks.docks.length = 0; window.__hooks.curtains.length = 0; 0")
                took = js(br, "return window.__offer(%s, {});" % SCORE)
                br.sleep(0.5)
                mid = js(br, "return {state: window.__report().state, "
                             "curtains: window.__hooks.curtains.slice()};")
                idle(br)
                end = js(br, "return {state: window.__report().state, "
                             "docks: window.__hooks.docks.slice(), "
                             "curtains: window.__hooks.curtains.slice(), "
                             "events: window.__report().events.map(function(e){return e.name;})"
                             ".slice(-6)};")
                check(BROWSER_ROWS[13],
                      took["took"] and mid["state"] == "running" and mid["curtains"][:1] == [True]
                      and end["state"] == "idle" and len(end["docks"]) == 1
                      and end["curtains"][-1] is False and "docked" in end["events"],
                      f"mid={mid} end={end}")

                # READ OFF THE PASS THAT JUST DOCKED, since the camera's rest is measured at the
                # landing and a pass held at a pinned progress has not reached one.
                cam = js(br, "var r = window.__report(); "
                             "return {camera: r.camera, rest: r.rest, handoffs: r.handoffs, "
                             "tol: r.camTolerances};")
                check(BROWSER_ROWS[15],
                      cam["camera"] and cam["camera"]["owner"] == "stage"
                      and cam["handoffs"] == []
                      and cam["rest"] and cam["rest"]["rested"] is True
                      and cam["rest"]["off"] <= cam["tol"]["rest"],
                      f"owner={cam['camera'] and cam['camera']['owner']} rest={cam['rest']} "
                      f"handoffs={cam['handoffs']} tolerances={cam['tol']} — the dive is the "
                      f"instrument's own motion inside its own pass and it asks the host's camera "
                      f"for nothing, so the stage holds it for the whole pass")

                js(br, "return window.__offer(%s, {clock: 1.0, progress: 0.4});" % SCORE)
                drawn(br)
                cen = js(br, "return window.__report();")["census"]
                check(BROWSER_ROWS[14],
                      cen["canvases"] == 1 and cen["contexts"] == 1 and cen["textures"] == 2
                      and cen["passesLastFrame"] == 1 and cen["framebuffers"] == 0
                      and cen["preserveDrawingBuffer"] is False,
                      f"census={cen}; the module's own canvas, its second context, its two textures "
                      f"with their mip chains and its own frame loop are what this port does "
                      f"without")

                br.evaluate("window.__cancel('census row'); 0")
                idle(br)

                # ---- one score, twice -----------------------------------------------------------
                br.sleep(0.5)
                took2 = js(br, "return window.__offer(%s, {clock: 1.5, progress: 0.4});" % SCORE)
                drawn(br)
                first = png(br, SHOTS / "repeat-1.png")
                br.evaluate("window.__cancel('between runs'); 0")
                idle(br)
                js(br, "return window.__offer(%s, {clock: 1.5, progress: 0.4});" % SCORE)
                drawn(br)
                second = png(br, SHOTS / "repeat-2.png")
                rmn, rmx = diff(first, second)
                br.evaluate("window.__cancel('repeat row'); 0")
                idle(br)
                check(BROWSER_ROWS[16], took2["took"] and rmn == 0.0 and rmx == 0,
                      f"took={took2['took']} two runs of one score at one pinned second: mean {rmn} "
                      f"worst channel {rmx}. Every number the shader reads is a closed form of a "
                      f"handle, and nothing here is rolled")

                errs = json.loads(br.evaluate("JSON.stringify(window.__errs||[])"))
                check(BROWSER_ROWS[17], not errs, "; ".join(errs)[:300])

                kept = sorted(p.name for p in SHOTS.glob("*.png"))
                check(BROWSER_ROWS[18],
                      len(kept) >= 30 and all((SHOTS / k).stat().st_size > 1000 for k in kept),
                      f"{len(kept)} captures under {SHOTS.relative_to(ROOT)}: the nine poses on "
                      f"both roads, the seven copy maps, the three mid-passage frames, the nine "
                      f"handle frames, the seven sampled instants, the frame after a resize and the "
                      f"two runs of one score")

    shutil.rmtree(BENCH, ignore_errors=True)

    # ================================================================================================
    # THE RED-ON-BUG PROOFS. Each reverts one rule this port states, in the artifact the browser
    # actually loads, and reads the number that moved. The pack served is changed and the host is
    # re-stamped with the digest of the bytes it is handed, which is what the build does; the file on
    # disk is never touched, so no working tree can be left changed by a proof.
    # ================================================================================================
    def share_ladder(br):
        return [copy_map(br, at, "red-%03d" % round(at * 100)) for at in (0.42, 0.5, 0.58)]

    def door_read(br, mixv):
        ww = int(br.evaluate("String(window.__exPass.bench.make() && "
                             "document.querySelector('canvas[aria-hidden]').width)"))
        hh = int(br.evaluate("String(document.querySelector('canvas[aria-hidden]').height)"))
        p = host_shot(br, "red-door-%d" % mixv, {"mix": mixv, "clock": CLOCK})
        v = js(br, "return window.__values({mix: %d, clock: %r});" % (mixv, CLOCK))
        return {"apart": apart(p, work_in_the_frame(PHOTOS[mixv], ww, hh))[0],
                "worst": v["ringMap"]["worst"] if v["ringMap"] else None,
                "whyNo": v["doorWhyNo"]}

    def entry_door(br):
        return door_read(br, 0)

    def exit_door(br):
        return door_read(br, 1)

    # ---- 1. the ring's outer end taken off the frame's own corners -------------------------------
    # The ring starts beyond the farthest corner of THIS frame, measured from the throat the frame
    # is actually drawn with — the wander included — because that is what makes the entry door whole
    # on any frame ratio and at any place the throat has wandered to. Reverted to a literal, the
    # corners of a tall frame stand outside a ring that was supposed to be outside them, and the
    # arriving work is already on the frame at a door that owes the departing one.
    base_in = on_bench(entry_door)
    bug = PACK.replace("var reach = reachOf(cx, cy, aspect);", "var reach = 0.5;", 1)
    bug_in = on_bench(entry_door, pack_text=bug)
    check(RED_ROWS[0],
          bug != PACK and base_in and bug_in
          and base_in["worst"] == 0 and base_in["whyNo"] is None and base_in["apart"] <= SEAM
          and bug_in["worst"] > 0
          and bug_in["whyNo"] and "the entry door leaks" in bug_in["whyNo"],
          f"with the reach read off the frame's own corners, the entry door carries "
          f"{base_in['worst']} of the arriving work anywhere on the buffer and stands "
          f"{base_in['apart']:.4f} of 255 from the departing work's own file. With it reverted to a "
          f"literal, the reading measures {bug_in['worst']:.6f} of the arriving work at the worst "
          f"of the points it walks and the door is refused: «{bug_in['whyNo']}». The frame then "
          f"stands {bug_in['apart']:.4f} of 255 from that file, which is the corners alone and why "
          f"the reading is what this row stands on")

    # ---- 2. the ring's travel removed -----------------------------------------------------------
    # The ring is the whole of the handover. Pinned at the end it starts from, the arriving work
    # never arrives: the exit door is the departing work, and the instrument's own reading refuses
    # a door it cannot keep whole.
    base_exit = on_bench(exit_door)
    bug = PACK.replace("var rRing = rHi + (rLo - rHi) * hand;", "var rRing = rHi;", 1)
    bug_exit = on_bench(exit_door, pack_text=bug)
    check(RED_ROWS[1],
          bug != PACK and base_exit and bug_exit
          and base_exit["apart"] <= SEAM and base_exit["worst"] == 0
          and base_exit["whyNo"] is None
          and bug_exit["apart"] > FAR and bug_exit["worst"] > 0.5
          and bug_exit["whyNo"] and "the exit door leaks" in bug_exit["whyNo"],
          f"with the travel standing, the exit door is {base_exit['apart']:.4f} of 255 from the "
          f"arriving work's own file and the instrument reads {base_exit['worst']} of the other "
          f"work anywhere on the buffer. With the ring pinned where it starts, the same door stands "
          f"{bug_exit['apart']:.4f} of 255 from that file and the reading measures "
          f"{bug_exit['worst']:.6f} of the departing work, on which it refuses the door: "
          f"«{bug_exit['whyNo']}»")

    # ---- 3. the wind's gate on the finish removed -----------------------------------------------
    # Everything the spiral's finish does — the dark rim on the seam, the well at the throat, the
    # two sinks — rides the wind and is nothing at both doors. Ungated, the flat photograph standing
    # at the entry door carries the spiral's own darkening, and stops being the file.
    bug = PACK.replace("float dS = d * uForm.w;", "float dS = uForm.w;", 1)
    bug_entry = on_bench(entry_door, pack_text=bug)
    check(RED_ROWS[2],
          bug != PACK and base_in is not None and bug_entry is not None
          and base_in["apart"] <= SEAM and bug_entry["apart"] > SEAM,
          f"with the gate standing, the entry door is {base_in['apart']:.4f} of 255 from the "
          f"departing work's own file; with the finish ungated it stands "
          f"{bug_entry['apart']:.4f} of 255 from it, against the project's own seam threshold of "
          f"{SEAM}. A door is the photograph or it is not the door")

    # ---- 4. the ring walked in the logarithm the picture is written in ---------------------------
    # The arithmetically obvious travel, and the one this port measured and did not take: the frame's
    # area sits almost entirely at the rim, so a ring walking evenly in log radius hands over most of
    # the frame in the first breath of the handover and spends the rest of it inside a disc a hand's
    # breadth across. Read where it shows: the share of the frame the arriving work holds at the
    # three quarters of the middle third.
    base_share = on_bench(share_ladder)
    bug = PACK.replace("var rRing = rHi + (rLo - rHi) * hand;",
                       "var rRing = Math.exp(Math.log(rHi) "
                       "+ (Math.log(rLo) - Math.log(rHi)) * hand);", 1)
    bug_share = on_bench(share_ladder, pack_text=bug)
    check(RED_ROWS[3],
          bug != PACK and base_share is not None and bug_share is not None
          and base_share[1] < 0.5 and bug_share[1] > 0.9
          and bug_share[0] - base_share[0] > 0.3,
          f"walking the ring in the radius, the arriving work holds "
          f"{', '.join(f'{s * 100:.1f}%' for s in base_share)} of the frame at the three quarters "
          f"of the middle third — the two photographs share the frame across the whole of it. "
          f"Walking it in the logarithm they hold "
          f"{', '.join(f'{s * 100:.1f}%' for s in bug_share)}: the handover is over before the "
          f"middle of the middle, and the departing work spends the rest of the passage as a speck. "
          f"Both doors stay whole either way, which is why this is read on the picture and not on "
          f"the door")


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
