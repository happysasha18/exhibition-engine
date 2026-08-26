#!/usr/bin/env python3
"""PASS-API-V1 — the corridor instrument on the host's frame.
Run: python3 tests/test_pass_tunnel.py

Root: his word of 2026-08-18 08:52 after walking the live route — «переходы очень однообразные: у
тебя дофига эффектов и ты сделал все очень топорно» — and the charter's own vocabulary row for this
module: «tunnel | коридор | переход (mystery middle) | SURFACE | approved; псевдо-тоннель В24 cut —
the real corridor with interaction stays» (lab/CROSSING-BRIEF.md). The composer has named a
`corridor` among its three polar worlds since stage 0 and had no instrument to play it with; this is
that instrument. docs/design/PASS-API-V1.md §7 (GPU and resources), §8 (the manifest) and §9's
conformance rows 7, 9, 10, 13, 14, 15, 16 and 22 are what this file makes real, together with §7's
coverage law. The lifecycle rows stay in tests/test_pass_api.py and are untouched.

WHAT IS COMPARED, AND AGAINST WHAT.

  THE DOORS. At the dial's two ends one whole work stands, and it is measured against ITS OWN FILE
  cover-fitted into the frame with NO crop at all, inside the project's seam threshold of 6 of 255.
  A log-polar map answers every point of the plane, so this instrument asks the frame for no
  headroom — which is what its `framings` block publishes as a cover crop of 1 at both doors.

  THE TWO ROADS. Both draw with WebGL: the module carries its own context and its own fragment
  shader, so one sampler runs through one rasteriser on both sides and the residual between them is
  a difference of arithmetic rather than of samplers. The bar is therefore the project's own seam
  threshold and not one this suite invented. THE LAB MODULE IS SERVED WITH THREE LITERALS CHANGED and
  the row that reads it says so: its per-photograph crop table is set to the rectangle the port
  DERIVES from the pair's own measured centre, and its hand-picked mip level is set to nothing while
  the port's own tap spread is set to nothing in the same run — the host holds no mip chain for an
  instrument to read, so a comparison at two different filters would compare the filters and not the
  mathematics.

  THE THREE ACTS. The two roads are compared through the OPENING act, where the corridor is being
  built out of the departing work alone and the module has exactly the same picture to draw. What
  happens after that — the arriving work coming up the corridor — the module has no second work for,
  so it is measured on the frame itself: the ring's own radius, read off the instrument's numbers,
  and the frame's own travel.

  THE COVERAGE. This instrument declares that it writes none, because it fills the frame. That is
  measured rather than declared: every sampled instant stands away from the cleared buffer, and the
  placement the declaration buys is read off the host's own `coverageWhyNo`.

  The lab module is READ ONLY. Absent, every browser row here is a pinned SKIP that names the missing
  path — never a silent pass.
"""
import base64
import hashlib
import math
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
PHOTOS = [LAB / "photos" / "towers.jpg", LAB / "photos" / "glassgrid.jpg"]
MODULE = LAB / "effects" / "tunnel.js"

SITE_URL = "https://synth.example.com"
VW, VH = 390, 844          # the phone frame lab/carrier-check.py measures on
SEAM = 6.0                 # the project's seam threshold, 6 of 255 (TRANSITION-STAGE-V0 §1)
FAR = 40.0                 # further than this from a file and it is a different work
BACKGROUND = (0x08, 0x08, 0x0a)
SPREAD = 10.0
ROADS = SEAM

# The dial's own three acts, and the two marks between them, read the way the instrument reads them:
# the dead band is spent first, then the corridor opens over the first third.
FEEL_D0 = 0.05
ACT = 1.0 / 3.0
OPEN_DONE = FEEL_D0 + ACT * (1 - 2 * FEEL_D0)        # the corridor stands whole, the flood at zero
FLOOD_DONE = FEEL_D0 + 2 * ACT * (1 - 2 * FEEL_D0)   # the arriving work has washed past the eye

# The crop the port derives for a pair whose measured radial centres midpoint at the picture's own
# middle, and the module's own two sides it is held between.
CROP_MIN, CROP_MAX = 0.48, 0.56
CROP_AT_MIDDLE = [0.22, 0.22, 0.56, 0.56]

SHOTS = ROOT / "tests" / "captures" / "pass-tunnel"

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


DIE = 4.91016            # the die lab/data/scores' own weave score carries, so every suite rolls one
DURATION_MS = 6500
WITHIN_MS = 500
CLOCK = 3.2              # the second the fall is read at, pinned so one instant can be photographed


def _static(v):
    return {"op": "static", "value": v}


def tunnel_cue(stack=0, levels_own=None, **statics):
    """The cue, with a track for every one of the ten handles (§4.4b)."""
    P = {"clock": CLOCK, "centreX": 0.5, "centreY": 0.5, "depth": 0.26, "ribs": 0.5,
         "spokes": 10, "twist": 0.16, "seed": 0, "mask": 0}
    P.update(statics)
    nodes = {"t-mix": {"source": "progress"}}
    tracks = {"mix": {"node": "t-mix"}}
    for k, v in P.items():
        nodes["t-" + k] = _static(v)
        tracks[k] = {"node": "t-" + k}
    return {
        "id": "corridor", "instrument": {"id": "tunnel", "api": 1},
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


def tunnel_score(under=False, **statics):
    """`under` puts a coverage-writing voice ABOVE this instrument, which is the placement its own
    declaration buys it: the ground of a stack. The upper voice claims SURFACE too, so this one
    yields it there — the levels law allows one active voice per level."""
    if under:
        cues = [tunnel_cue(stack=0, levels_own={"SURFACE": "yields", "CELL": "owns"}, **statics),
                matter_cue(stack=1)]
    else:
        cues = [tunnel_cue(stack=0, **statics)]
    res = {"textures": 0, "textureSlots": 2, "framebuffers": 0, "pingPong": 0, "programs": 1,
           "passes": 1, "bytesEstimate": 0}
    return {
        "schema": 2,
        "intent": "the flat picture becomes a corridor the viewer falls down, the arriving work "
                  "opens out of the hole at its far end and comes up it, and the corridor closes "
                  "on that work standing whole (lab/effects/tunnel.js:1-3, its own header)",
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
        "provenance": {"source": "lab/effects/tunnel.js's own declared defaults and constants",
                       "measuredAt": None, "by": "tests/test_pass_tunnel.py"},
    }


# ---------------------------------------------------------------- bake once
build_site.SITE_CONFIG = dict(build_site.SITE_CONFIG)
build_site.SITE_CONFIG["pass"] = {"visualLayer": "pass", "diagnostics": "on"}

TMP = Path(tempfile.mkdtemp(prefix="synth_passtun_"))
build_site.OUT = TMP
build_site.build(SITE_URL)
LAYER = (TMP / "pass-layer.js").read_text(encoding="utf-8")
# THE INSTRUMENT'S OWN BUILT FILE — the real artifact a visitor is served, comments stripped. Since
# every instrument travels alone, the whole of this file is this instrument and nothing else.
PACK = (TMP / "pass-inst-tunnel.js").read_text(encoding="utf-8")
REGION = PACK
SOURCE = ROOT / "engine" / "assets" / "pass-inst-tunnel.js"
SOURCE_TEXT = SOURCE.read_text(encoding="utf-8")
LABTXT = MODULE.read_text(encoding="utf-8") if MODULE.exists() else ""

# ---------------------------------------------------------------- string rows

OWNED = ["createElement", "getContext", "requestAnimationFrame", "addEventListener",
         "performance.now", "Date.now", "new Image", "setTimeout", "setInterval"]
held = [s for s in OWNED if s in REGION]
check("PASS-TUNNEL the instrument creates no element, no loop and no listener",
      not held,
      "§1.2's fence, read against the instrument's own built file: none of the nine ways of owning "
      "hardware appears there. The module raises its own canvas, takes a WebGL2 context on it, "
      "uploads its own textures with a mip chain, runs its own frame loop, observes its own mount "
      "for a resize and binds a pointer and a touch listener to steer the fall; all of it stayed in "
      "the lab"
      if not held else "the instrument's region holds " + ", ".join(held))

HANDLES = ["mix", "clock", "centreX", "centreY", "depth", "ribs", "spokes", "twist", "seed", "mask"]
absent = [h for h in HANDLES if ("%s: { min" % h) not in REGION]
check("PASS-TUNNEL every handle the instrument publishes is a handle a score can drive",
      not absent and len(HANDLES) == 10,
      "§4.4b: ten handles. The dial, the second the fall is read at, the two that place the "
      "corridor's far point, the module's own three declared params — the fall's speed, the ring "
      "spacing and the angular repeats — the spiral shear, the score's die and the judges' channel. "
      "The module's `photo` param is published by neither, and the reason is that a cue carries an "
      "ordered pair: which pictures the corridor is built of is the cue's own two works"
      if not absent else "these are published nowhere: " + ", ".join(absent))

check("PASS-TUNNEL a clock IS published, and the picture is what settles that",
      "clock: { min" in REGION and "st.clock" in REGION and "z = Z0 + t * speed" in REGION,
      "the folding instrument publishes no clock because nothing in its picture moves with time. A "
      "corridor that did not fall would not be a corridor: the depth travelled is the module's own "
      "`Z0 + t * speedPerSec()`, the drift the fall wanders on is a pure function of the second, and "
      "so is the twist's own slow breath. So the handle is published and the picture reads it")

# Every constant the picture stands on, read out of the lab module and out of the built file.
CONSTANTS = [
    ("float mirrorU(float x){ float m = fract(x * 0.5); return abs(m * 2.0 - 1.0); }",
     "float mirrorU(float x){ float m = fract(x * 0.5); return abs(m * 2.0 - 1.0); }",
     "the seamless wrap across the picture: an even number of mirrored copies"),
    ("float edge = smoothstep(0.90, 1.0, abs(v * 2.0 - 1.0));",
     "float edge = smoothstep(1.0 - uSeam, 1.0, abs(v * 2.0 - 1.0));",
     "the ring join's own cross-fade with its neighbour, so the turn carries no jump — the module's "
     "own 0.90 travels here as `uSeam`, off the host's own `seams` reading (§8), so this join and "
     "kaleidoscope's crease and planet's wrap-seam round one shared shape instead of three typed "
     "numbers"),
    ("float leanF = max(1.0 + uLean * dot(dirp, uLeanDir), 0.22);",
     "float leanF = max(1.0 + uLean.z * dot(dirp, uLean.xy), 0.22);",
     "the lean: rings ride nearer on one side of the corridor and further on the other"),
    ("float depth = log(rl) / uLogB;", "float depth = log(rl) / uLean.w;",
     "the depth axis: the rings stand at even RATIOS of depth, one unit per ring"),
    ("float a2 = ang + uTwist * depth;", "float a2 = ang + uRing.y * depth;",
     "the spiral shear that turns the corridor into a vortex"),
    ("float dv  = th2 / (uLogB * rl * pxU);", "float fv  = 1.0 / (uLean.w * rl * pxU);",
     "the pixel's own footprint along the depth axis, in the crop's own units"),
    ("float duT = tw2 * uReps / (TAU * rl * pxU);",
     "float fuT = uRing.z / (TAU * rl * pxU);",
     "and across the corridor"),
    ("float duR = tw2 * abs(uTwist) * uReps / (TAU * uLogB * rl * pxU);",
     "float fuR = abs(uRing.y) * uRing.z / (TAU * uLean.w * rl * pxU);",
     "and the part of it the shear adds"),
    ("float fog = pow(smoothstep(0.004, 0.66, rl), 0.95);",
     "float fog = pow(smoothstep(0.004, 0.66, rl), 0.95);",
     "the far end sinking into a cold dark"),
    ("col = mix(col, mix(vec3(lum) * vec3(0.62, 0.76, 0.98), col, 0.45 + 0.55 * fog), d);",
     "col = mix(col, mix(vec3(lum) * vec3(0.62, 0.76, 0.98), col, 0.45 + 0.55 * fog), d);",
     "the cold tint the depth is read by"),
    ("col *= mix(1.0, smoothstep(0.0, 0.115, rl), d);",
     "col *= mix(1.0, smoothstep(0.0, 0.115, rl), d);",
     "the hole at the far end"),
    ("col += d * vec3(0.20, 0.26, 0.34) * 0.22 * exp(-rl * 55.0);",
     "col += d * vec3(0.20, 0.26, 0.34) * 0.22 * exp(-rl * 55.0);",
     "and the breath of light in it, so the hole reads as far away"),
    ("var FAR_REACH = 0.5, RIBS_REACH = 2.0;", "var FAR_REACH = 0.5, RIBS_REACH = 2.0;",
     "the two reaches the module publishes for the handles a score already drives it by"),
    ("var Z0 = 0.35;", "var Z0 = 0.35;", "the depth the fall starts at"),
    ("0.5 + 0.115 * Math.sin(t * 0.19) + 0.045 * Math.sin(t * 0.077)",
     "0.5 + 0.115 * Math.sin(t * 0.19) + 0.045 * Math.sin(t * 0.077)",
     "the wander of the fall, a pure function of the second"),
    ("var breath = 0.78 + 0.22 * Math.sin(clock * 0.147);",
     "var breath = 0.78 + 0.22 * Math.sin((t + seed) * 0.147);",
     "the twist's own slow breath, with the pair's die on its phase"),
]
missing_const = [p for lab_p, p in ((a, b) for a, b, _ in CONSTANTS)
                 if lab_p not in LABTXT or p not in REGION]
check("PASS-TUNNEL every constant the picture stands on carries the module's own number",
      not missing_const and bool(LABTXT),
      "; ".join("%s — %s" % (p, why) for _, p, why in CONSTANTS) if not missing_const
      else "these differ between the lab module and the port: " + ", ".join(missing_const))

check("PASS-TUNNEL the per-photograph crop table did not cross, and what replaces it is a derivation",
      "0.26, 0.02, 0.48, 0.48" in LABTXT and "0.26, 0.02" not in REGION
      and "0.22, 0.10" not in REGION
      and "var CROP_MIN = 0.48, CROP_MAX = 0.56;" in REGION
      and "function cropOf(cx, cy)" in REGION
      and "2 * Math.min(Math.min(cx, 1 - cx), Math.min(cy, 1 - cy))" in REGION,
      "the module carries `CROPS = [[0.26, 0.02, 0.48, 0.48], [0.22, 0.10, 0.56, 0.56]]`, two "
      "rectangles typed by hand for two named photographs, which is exactly what his 19:13 word "
      "lifted to the class at 19:21 forbids. What crossed is the SPAN those two rectangles stand in "
      "— 0.48 and 0.56 of the picture's side — and what replaces the table is a derivation: the "
      "crop stands about the pair's own measured radial centre and takes the largest square that "
      "fits inside the picture around it, held inside that span")

check("PASS-TUNNEL the dive's own smear and its field-of-view nudge rest where the module rests them",
      "uBlur" in LABTXT and "uBlur" not in REGION
      and "0.055 * a01" in LABTXT and "accel" not in REGION,
      "both are the module's answer to a PRESS of the pointer, through its own dive multiplier, and "
      "both are nothing whenever nobody is pressing — which the module's own scored road already "
      "rests them at. A scored corridor has no hand, so they are carried as the resting values and "
      "no uniform spends a slot on them")

# THE HOST NOW BUILDS A CHAIN, AND THIS INSTRUMENT STILL DOES NOT ASK FOR IT. When the port was
# written the host built none and the row said so. `beauty` made the host build one on 2026-08-18
# and hand it to any instrument declaring `gl.readsChain`, so the row's premise moved and the row
# holds what stands instead: the host has a chain, this manifest does NOT ask for it, and the
# reason is measured rather than assumed. The five taps on a rotated cross ARE this port's answer
# to the same minification the chain answers, so a chained copy underneath them is the same job
# done twice — and it parts the two roads: measured at the merge, with the flag declared the
# corridor's third opening stands 8.38 of 255 from the module against a bar of 6, where it agrees
# at 1.79 without it.
check("PASS-TUNNEL the mip chain could not cross, and the measurement that fed it did",
      "generateMipmap" in LABTXT and "generateMipmap" not in REGION
      and "textureLod" in LABTXT and "textureLod" not in REGION
      and "const float FOOT_MAX = 0.3333;" in REGION
      and "vec3 pickF(vec2 t, vec2 foot, float which, vec2 flat0){" in REGION
      and "makeTex" in LAYER and "generateMipmap" in LAYER
      and "gl.readsChain" in LAYER and "readsChain" not in REGION,
      "the module uploads its own texture and builds a mip chain on it, then picks the level by "
      "hand because `fract()` breaks the automatic derivatives. An instrument may not upload a "
      "texture, so the level choice could not cross; the three footprint expressions crossed "
      "unchanged and are spent on five taps over that footprint instead. The host now builds a "
      "chain and hands it to any instrument declaring `gl.readsChain`, and this one deliberately "
      "does not: the taps are already its answer to that minification, and declaring the flag "
      "parts the two roads")

check("PASS-TUNNEL the host binds uniforms by declared name, never by position or a written list",
      "getUniformLocation(p, u.name)" in LAYER and "uRing" not in LAYER and "uCrop" not in LAYER,
      "this instrument declares twelve uniforms, of which five are shared with the folding one. The "
      "host reads the manifest")

declared = dict((m.group(1), m.group(2))
                for m in re.finditer(r'\{ name: "(u\w+)", type: "(\w+)"', REGION))
spelled = dict((m.group(2), m.group(1))
               for m in re.finditer(r'uniform (\w+) (u\w+);', REGION))
check("PASS-TUNNEL the manifest's declared names and the shader's own names are one set",
      set(declared) == set(spelled) and len(declared) == 12,
      f"{len(declared)} declared, {len(spelled)} spelled; "
      f"declared only: {sorted(set(declared) - set(spelled))}; "
      f"spelled only: {sorted(set(spelled) - set(declared))}")

# AND THEIR WIDTHS ARE ONE SET TOO, which is a separate question and cost this port a whole run.
# The host picks its binding call off the DECLARED type (pass-layer.js's own `bindUniform`), and GL
# refuses a four-wide call on a two-wide uniform without raising anything a script can catch: the
# uniform simply stays at zero and the picture is wrong in a way no name check can see.
wrong_width = sorted("%s declared %s, spelled %s" % (n, declared[n], spelled[n])
                     for n in declared if n in spelled and declared[n] != spelled[n])
check("PASS-TUNNEL every carrier is as wide where it is declared as where it is spelled",
      not wrong_width,
      "; ".join("%s %s" % (n, declared[n]) for n in sorted(declared))
      + ". The host reads the declared type to choose which of gl.uniform1i/1f/2f/4f it calls, so a "
        "carrier declared four wide and spelled two wide binds NOTHING — GL refuses the call, no "
        "script sees an error, and the shader reads zeros. This port shipped exactly that fault for "
        "one run: `uWipe` carried the station the arriving work stands beyond, and at zero every "
        "point of the corridor stood beyond it, so both doors drew the same work"
      if not wrong_width else "these disagree: " + "; ".join(wrong_width))

SUPPLY = ["textureA", "textureB", "fitA", "fitB", "resolution", "seconds"]
sources = set(re.findall(r'source: "([^"]+)"', REGION))
outside = [s for s in sources
           if s not in SUPPLY and not s.startswith("frame:") and not s.startswith("handle:")]
check("PASS-TUNNEL every uniform is sourced from the closed set the host can supply",
      not outside and len(sources) >= 8,
      "§7's uniform sources are the two source textures, their fits, the resolution, the "
      "transaction's seconds, a value the instrument answers and a handle. This instrument names "
      f"{len(sources)} distinct sources and none outside that set"
      if not outside else "outside the set: " + ", ".join(outside))

check("PASS-TUNNEL the shader carries no version header of its own",
      "#version" not in REGION and "#version 300 es" in LABTXT,
      "the module ships GLSL ES 3.00 with its own header because it reads an explicit mip level and "
      "builds its triangle out of the vertex index. Neither survives the crossing — the host holds "
      "no mip chain and hands its own triangle in on `aPos` — so the shader is written in the "
      "dialect every other instrument here is written in and the host's translator stamps the one "
      "header it needs")

check("PASS-TUNNEL the manifest leaves the drawing buffer unpreserved",
      "gl: { preserveDrawingBuffer: false }" in REGION
      and "preserveDrawingBuffer: false" in LABTXT,
      "§7 refuses a manifest that asks for the buffer to be preserved; this instrument draws every "
      "frame the host hands it, which is what the module does too")

check("PASS-TUNNEL the coverage is declared, and the map it draws is the reason",
      "coverage: { writes: false" in REGION
      and "gl_FragColor = vec4(col, 1.0);" in REGION
      and "opacity" not in REGION and "presence" not in REGION,
      "§8's coverage block and §7's law: the alpha is the constant 1, said as a decision. A "
      "log-polar map is defined at every point of the plane, so every point of the frame stands on "
      "some ring of the corridor at every place of the fall and this instrument has no absence to "
      "publish. Under the placement rule that makes it lawful as the LOWEST cue of a stack. No "
      "handle of opacity and no weight of presence stands anywhere in the instrument")

check("PASS-TUNNEL neither door is cropped, and the file says why",
      'framings: { "0": { coverCrop: 1 }, "1": { coverCrop: 1 } }' in SOURCE_TEXT
      and "asks the frame for no headroom" in SOURCE_TEXT,
      "the folding instrument has to publish a cover crop of 1.90 because a box turning about its "
      "own centre retreats from the frame's corners and the frame has to be a window in the middle "
      "of a bigger box. A corridor has no such fault: the map answers every point, so a door here "
      "is the source cover-fitted and nothing else, and the visitor loses no picture to the passage")

# EVERY GEOMETRIC PARAMETER NAMES THE MEASUREMENT IT READS. His 19:13 word, lifted to the class at
# 19:21. This is the row that holds the whole class law for this instrument.
READS = [
    ("centreX", "structure.radial.centre"),
    ("centreY", "structure.radial.centre, read on the other axis"),
    ("depth", "structure.polar.tunnel"),
    ("ribs", "structure.ownDevice.count"),
    ("spokes", "structure.rotational.n"),
    ("twist", "structure.polar.twirl"),
]
unread = [h for h, m in READS if ('%s: { min' % h) not in REGION or m not in REGION]
check("PASS-TUNNEL every geometric parameter publishes the measurement of the work it derives from",
      not unread,
      "; ".join("`%s` reads %s" % (h, m) for h, m in READS)
      + ". The vanishing point the corridor falls toward is the pair's own measured radial centre; "
        "how far the fall travels is the departing work's own corridor reading; the ring spacing is "
        "that work's own measured ring repeat; the angular repeats are its own measured turn; the "
        "spiral shear is its own measured twirl. Not one of the six is a number typed here"
      if not unread else "these name no measurement: " + ", ".join(unread))

check("PASS-TUNNEL the file answers the wipe's own three-part test on all three counts",
      "IS THE RING A WIPE? THE THREE-PART TEST, ANSWERED ON ALL THREE COUNTS" in SOURCE_TEXT
      and "THE BOUNDARY IS THE CORRIDOR'S OWN RING" in SOURCE_TEXT
      and "THE TWO IMAGES INTERACT ALONG THE WHOLE PASSAGE" in SOURCE_TEXT
      and "IT READS AS FALLING DOWN A CORRIDOR" in SOURCE_TEXT,
      "the charter's ban list convicts a wipe only where ALL THREE counts convict, and a boundary "
      "that travels across a frame has to answer that test out loud. The boundary is the level set "
      "of a depth axis every parameter of which is a reading of the photographs; the two works are "
      "the near and the far halves of one corridor and meet at a ring carrying a contact shade; and "
      "what arrives is a place further down the corridor, reached by travelling")

check("PASS-TUNNEL the judges' handle publishes what the door is read against, and that nothing is held",
      'readAtADoor: { points: DOOR_SLIP, readOn: "the drawing buffer",' in SOURCE_TEXT
      and 'reads: "flatness"' in SOURCE_TEXT
      and "var DOOR_SLIP = 0.5;" in SOURCE_TEXT
      and "var DOOR_SHOW = 0.5 / 255;" in SOURCE_TEXT
      and "held: null" in SOURCE_TEXT
      and "AND THERE IS NOTHING HERE TO HOLD" in SOURCE_TEXT,
      "the handle carries `applied.readAtADoor` — what is walked, on which grid, what the reading is "
      "counted in — and it says outright that there is no hold. A corridor's flat door is exact by "
      "construction and not by a tolerance: the dead band spends the hand and the dial is exactly "
      "nothing inside it, so anything the reading finds is a real fault that no widening closes")

sha = hashlib.sha256(MODULE.read_bytes()).hexdigest() if MODULE.exists() else ""
declared_sha = (re.search(r'sha256: "([0-9a-f]{64})"', REGION) or [None, None])[1]
check("PASS-TUNNEL the provenance names the file the port was read from, and the file weighs to it",
      bool(sha) and sha == declared_sha and 'commit: "fc885a3"' in REGION,
      f"the module is tracked, so the commit it was read at is named beside the digest of its bytes, "
      f"and the file still weighs to {sha[:16]}…")

# ---------------------------------------------------------------- browser rows

BROWSER_ROWS = [
    "PASS-TUNNEL §8     · the manifest carries every field the contract names, in its shape",
    "PASS-TUNNEL §8     · it publishes SURFACE and CELL, and the charter's own row is the source",
    "PASS-TUNNEL row 7  · door 0 stands the departing work, measured against its own file uncropped",
    "PASS-TUNNEL row 7  · door 0 carries no trace of the arriving work",
    "PASS-TUNNEL row 7  · door 1 stands the arriving work, measured against its own file uncropped",
    "PASS-TUNNEL row 7  · door 1 carries no trace of the departing work",
    "PASS-TUNNEL the two roads agree at the flat door and at five places as the corridor opens",
    "PASS-TUNNEL the arriving work comes up the corridor, and the ring it opens as only grows",
    "PASS-TUNNEL §7     · no empty frame at any sampled instant of the pass",
    "PASS-TUNNEL §7     · the ground of a stack, and refused above another cue",
    "PASS-TUNNEL §7     · both doors stand whole with a coverage-writing voice over them",
    "PASS-TUNNEL §7     · the frame after a change of viewport is drawn afresh",
    "PASS-TUNNEL row 10 · a seeded run repeats to the pixel",
    "PASS-TUNNEL row 14 · textures, programmes and framebuffers return to their baseline after ten runs",
    "PASS-TUNNEL row 15 · the console stays clean",
    "PASS-TUNNEL row 22 · the census shows granted against declared, and neither overruns",
    "PASS-TUNNEL §4.4b  · the six measured handles reach the PICTURE and not only the record",
    "PASS-TUNNEL the real transaction road: curtain up, one pass drawn, exactly one dock at the end",
    "PASS-TUNNEL the corridor is WALKED on the drawing buffer at both doors, and what it read is published",
    "PASS-TUNNEL a door the judges' channel spoils is refused on the real road, and the visitor still lands",
    "PASS-TUNNEL row 16 · the captures are kept as evidence",
]

RED_ROWS = [
    "PASS-TUNNEL red-on-bug · the derived crop replaced by the module's own typed rectangle",
    "PASS-TUNNEL red-on-bug · the wipe's own radius unbounded at the hole: the entry door reads "
    "the arriving work",
    "PASS-TUNNEL red-on-bug · the contact shade at the meeting ring removed",
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
    """The whole file, cover-fitted into the frame and cropped by nothing at all — which is what this
    instrument's own `framings` block publishes for both doors."""
    from PIL import Image
    return cover_into(Image.open(src).convert("RGB"), w, h, crop)


def apart(p, work):
    from PIL import Image, ImageChops, ImageStat
    a = Image.open(p).convert("RGB")
    if a.size != work.size:
        return 255.0, 255.0
    st = ImageStat.Stat(ImageChops.difference(a, work))
    return sum(st.mean) / 3.0, max(m for _, m in st.extrema)


# THE LAB MODULE AS THE BENCH SERVES IT, and the port beside it, each with one literal changed.
#   · the module's per-photograph crop table becomes the rectangle the port DERIVES for a pair whose
#     measured centres midpoint at the picture's middle. That rectangle is symmetric about the
#     picture's centre, so the module reading its rows bottom-up and the host reading them top-down
#     land on one and the same piece of picture.
#   · the module's hand-picked mip level becomes nothing, and the port's own tap spread becomes
#     nothing in the same run. The host holds no mip chain, so a comparison at two different filters
#     would compare the filters rather than the mathematics.
# The files on disk are never touched.
LAB_CROP_FROM = "var CROPS = [[0.26, 0.02, 0.48, 0.48], [0.22, 0.10, 0.56, 0.56]];"
LAB_CROP_TO = ("var CROPS = [[%s, %s, %s, %s], [%s, %s, %s, %s]];"
               % tuple(CROP_AT_MIDDLE * 2))
LAB_LOD_FROM = "    '  float lod = clamp(log2(max(max(dv, duT), duR) + 1e-6) - 0.60, 0.0, 11.0);',"
LAB_LOD_TO = "    '  float lod = 0.0;',"
# AND THE WALL'S OWN ROW COORDINATE TURNED OVER. The module uploads its texture bottom-up
# (UNPACK_FLIP_Y_WEBGL) and the host uploads both works top-down, so one and the same crop rectangle
# names two vertically mirrored pieces of picture. The module's flat door already carries its own
# flip and agrees with the port's to a hundredth of a level; this is the same flip for its WALL, so
# the two roads wrap one piece of one photograph around one corridor.
LAB_FLIP_FROM = "    '  return textureLod(uTex, mix(gFlat, uCrop.xy + t * uCrop.zw, gDial), lod * gDial).rgb;',"
LAB_FLIP_TO = "    '  return textureLod(uTex, mix(gFlat, uCrop.xy + vec2(t.x, 1.0 - t.y) * uCrop.zw, gDial), lod * gDial).rgb;',"
PORT_TAPS_FROM = '"const float FOOT_MAX = 0.3333;",'
PORT_TAPS_TO = '"const float FOOT_MAX = 0.0;",'


def lab_levelled():
    out = LABTXT.replace(LAB_CROP_FROM, LAB_CROP_TO, 1).replace(LAB_LOD_FROM, LAB_LOD_TO, 1)
    return out.replace(LAB_FLIP_FROM, LAB_FLIP_TO, 1)


def bench_dir(pack_text=None, level=False):
    """The bench's own served root: the BUILT pass-layer.js, the site's own settings record and the
    BUILT instrument files it names — the real artifacts, namespace applied and comments stripped —
    the lab module with its two literals levelled, the two photographs, and the page that stands the
    two roads of one frame side by side.

    A row proving a rule reds hands over a CHANGED instrument file and writes the record with the
    digest of the bytes actually served, which is what the build does. The source file on disk is
    never touched, so nothing has to be restored."""
    d = Path(tempfile.mkdtemp(prefix="synth_tunbench_"))
    pack = PACK if pack_text is None else pack_text
    if level:
        pack = pack.replace(PORT_TAPS_FROM, PORT_TAPS_TO, 1)
    shutil.copy2(TMP / "pass-layer.js", d / "pass-layer.js")
    for _inst in sorted(TMP.glob("pass-inst-*.js")):
        shutil.copy2(_inst, d / _inst.name)
    (d / "pass-inst-tunnel.js").write_text(pack, encoding="utf-8")
    record = json.loads((TMP / "config.json").read_text(encoding="utf-8"))
    record["pass"]["instruments"]["tunnel"]["digest"] = hashlib.sha256(
        pack.encode("utf-8")).hexdigest()
    (d / "config.json").write_text(json.dumps(record), encoding="utf-8")
    (d / "tunnel.js").write_text(lab_levelled(), encoding="utf-8")
    (d / "photos").mkdir()
    for p in PHOTOS:
        shutil.copy2(p, d / "photos" / p.name)
    shutil.copy2(ROOT / "tests" / "fixture_pass_tunnel.html", d / "index.html")
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


def on_bench(fn, pack_text=None, level=False):
    d = bench_dir(pack_text, level)
    try:
        with serve(d) as base:
            with Browser(width=VW, height=VH) as br:
                br.navigate(base + "/index.html")
                if not ready(br):
                    return None
                return fn(br)
    finally:
        shutil.rmtree(d, ignore_errors=True)


def offer_shot(br, score, at, tag, tries=3):
    """One instant of a real transaction, photographed. Retried where the frame comes back blank:
    the host may still be raising its curtain, and several lanes share this machine's two browsers,
    so a first frame that misses is the harness's own timing rather than the instrument's."""
    last = None
    for k in range(tries):
        js(br, "return window.__offer(%s, {clock: %r, progress: %r});" % (score, CLOCK, at))
        br.sleep(0.6 + 0.4 * k)
        last = png(br, SHOTS / (tag + ".png"))
        d, sp = standing(last)
        br.evaluate("window.__cancel('%s'); 0" % tag)
        idle(br)
        if d >= FAR and sp >= SPREAD:
            return last, d, sp
    return last, d, sp


def host_shot(br, at, tag):
    """One pose, drawn by the host through the same drawPose a running transaction takes."""
    v = js(br, "return window.__both(%r);" % at)
    br.sleep(0.25)
    br.evaluate("window.__hostDraw(); window.__show('host'); 0")
    br.sleep(0.3)
    return v, png(br, SHOTS / (tag + ".png"))


def roads(br, at, tag):
    """BOTH ROADS AT ONE POSE. The port's own dial at this mark is handed straight to the module's
    own crossing dial, so the two stand at ONE corridor rather than at two readings of one hand."""
    v = js(br, "return window.__both(%r);" % at)
    br.evaluate("window.__corridor(%r); 0" % v["corridor"])
    br.sleep(0.45)
    br.evaluate("window.__hostDraw(); 0")
    br.sleep(0.15)
    br.evaluate("window.__show('host'); 0")
    br.sleep(0.25)
    ph = png(br, SHOTS / (tag + "-host.png"))
    br.evaluate("window.__show('module'); 0")
    br.sleep(0.35)
    pm = png(br, SHOTS / (tag + "-module.png"))
    br.evaluate("window.__show('host'); 0")
    return v, ph, pm


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
            elif not js(br, "return !!window.__exPass.bench.manifest('tunnel');"):
                why = js(br, "var e = window.__host.report().events.filter(function(x){"
                             "return x.name === 'manifest-refused';});"
                             "return e.length ? e[e.length - 1].why : null;")
                for r in BROWSER_ROWS:
                    check(r, False, "the host registered no «tunnel» instrument: " + str(why))
            else:
                SCORE = json.dumps(tunnel_score())
                SCORE_UNDER = json.dumps(tunnel_score(under=True))

                # ---- §8: the manifest, read off the registered instrument -----------------------
                m = js(br, "return window.__exPass.bench.manifest('tunnel');")
                res = m["resources"]
                need = ["id", "api", "arity", "roles", "params", "handles", "neutrals", "doors",
                        "framings", "drivers", "camera", "gl", "passes", "resources",
                        "capabilities", "decline", "provenance", "readiness", "coverage", "levels"]
                shape = (
                    all(k in m for k in need)
                    and m["id"] == "tunnel" and m["api"] == 1 and m["arity"] == 2
                    and m["roles"] == ["disassembly", "mystery", "assembly"]
                    and sorted(m["params"]) == ["depth", "ribs", "spokes", "twist"]
                    and len(m["handles"]) == 10
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
                    and m["provenance"]["labPath"] == "lab/effects/tunnel.js"
                    and m["provenance"]["commit"] == "fc885a3"
                    and m["readiness"] == "production-ready"
                    and "tunnel" in js(br, "return window.__host.report().registered;"))
                check(BROWSER_ROWS[0], shape,
                      f"ten handles, twelve uniforms in one pass, both doors at a cover crop of "
                      f"{m['framings']['0']['coverCrop']} — no headroom asked of the frame at all — "
                      f"resources declared for three tiers with a byte estimate of "
                      f"{res['standard']['bytesEstimate']}, and a coverage block reading "
                      f"«{m['coverage']['how']}»")

                check(BROWSER_ROWS[1],
                      m["levels"] == ["SURFACE", "CELL"]
                      and "WHERE THIS STANDS ON THE CHARTER'S SHELF" in SOURCE_TEXT
                      and "SURFACE" in SOURCE_TEXT and "spends no crossing's miracle" in SOURCE_TEXT,
                      f"levels={m['levels']}, and the source of that reading is his own standing "
                      f"verdict on this module in lab/CROSSING-BRIEF.md's vocabulary table, which "
                      f"carries the level in the same row: SURFACE. Shelf 17's levels law keeps "
                      f"WORLD for the camera and gives SURFACE «floor, cylinder, ribbon», so a "
                      f"corridor is a surface — which is why this instrument spends no crossing's "
                      f"one miracle and a quiet link may play it as readily as a culmination. CELL "
                      f"is the rings, which is where the two works meet. CELL CONTENT, TEXTURE and "
                      f"LIGHT-COLOUR are not claimed")

                w = int(br.evaluate("String(window.__exPass.bench.make() && "
                                    "document.querySelector('canvas[aria-hidden]').width)"))
                h = int(br.evaluate("String(document.querySelector('canvas[aria-hidden]').height)"))
                bufs = js(br, "return window.__buffers();")
                towers = work_in_the_frame(BENCH / "photos" / "towers.jpg", w, h)
                glass = work_in_the_frame(BENCH / "photos" / "glassgrid.jpg", w, h)

                # ---- the doors, and the opening act on both roads --------------------------------
                DOORS = [("door-0", 0.0), ("door-1", 1.0)]
                OPEN = [("o1", 0.10), ("o2", 0.17), ("o3", 0.24), ("o4", 0.30),
                        ("o5", round(OPEN_DONE, 4))]
                # THE DOORS, on the artifact a visitor is actually served — nothing levelled.
                shots, reads = {}, {}
                for tag, at in DOORS:
                    reads[tag], shots[tag] = host_shot(br, at, tag)

                for i, (door, own, other, ownn, othern) in enumerate((
                        ("door-0", towers, glass, "towers.jpg", "glassgrid.jpg"),
                        ("door-1", glass, towers, "glassgrid.jpg", "towers.jpg"))):
                    a, amx = apart(shots[door], own)
                    check(BROWSER_ROWS[2 + i * 2], a <= SEAM,
                          f"{door} against {ownn}, cover-fitted and cropped by nothing: mean "
                          f"{a:.4f} of 255 (threshold {SEAM}), worst channel {amx}. Inside the dead "
                          f"band the dial is exactly nothing, so the sample coordinate the shader "
                          f"reads at is the plain cover-fit point and the taps spread over nothing "
                          f"— one fetch of one point, which is the picture the file carries")
                    o, _ = apart(shots[door], other)
                    check(BROWSER_ROWS[3 + i * 2], o >= FAR,
                          f"{door} against {othern}: mean {o:.4f} of 255 (must exceed {FAR})")

                # ---- the arriving work comes up the corridor -------------------------------------
                # The module carries one photograph, so this act is measured on the frame itself:
                # the ring's own radius, solved out of the instrument's published numbers, and how
                # far the frame travels while it grows.
                mids = []
                first = None
                for k, at in enumerate([round(OPEN_DONE + (FLOOD_DONE - OPEN_DONE) * i / 6.0, 4)
                                        for i in range(7)]):
                    v, p = host_shot(br, at, "flood-%d" % k)
                    rl = math.exp((v["ring"][0] - v["wipe"][0]) * v["lean"][3])
                    if first is None:
                        first = p
                    mids.append((at, v["flood"], rl, diff(first, p)[0]))
                grows = all(mids[i][2] > mids[i - 1][2] for i in range(1, len(mids)))
                # THE FRAME'S OWN TRAVEL IS READ FROM THE START OF THE ACT AND NOT STEP BY STEP. The
                # ring opens INSIDE the hole the module blacks out at the far end — that is the
                # design, the arriving work coming out of the darkness — so its first marks change
                # almost nothing and a step-to-step bar would be a bar on the darkness. What has to
                # hold is that the picture never turns back and that the act carries the frame the
                # whole way from one work to the other.
                travels = all(mids[i][3] >= mids[i - 1][3] for i in range(1, len(mids)))
                arrives = mids[-1][3] >= FAR
                check(BROWSER_ROWS[7], grows and travels and arrives,
                      "; ".join(f"at {at} flood {fl:.3f}: the ring stands at {rl:.4f} of the "
                                f"frame's half-height, the frame {st:.2f} of 255 on from where the "
                                f"act began"
                                for at, fl, rl, st in mids)
                      + ". The arriving work stands beyond a station in the corridor's own depth "
                        "and the station travels toward the eye, so on the frame it is a ring "
                        "opening out of the hole the module blacks out and growing past the "
                        f"corner. The radius grows in even RATIOS, which is the corridor's own "
                        f"law — the rings stand at even ratios of depth — the picture never turns "
                        f"back, and by the end of the act the frame stands {mids[-1][3]:.2f} of 255 "
                        f"from where it began, which is a different photograph (bar {FAR})")

                # ---- §7: no empty frame ----------------------------------------------------------
                empties = []
                for at in (0.0, 0.15, 0.3, 0.5, 0.7, 0.85, 1.0):
                    _, d0, s0 = offer_shot(br, SCORE, at, "instant-%03d" % round(at * 100))
                    empties.append((at, d0, s0))
                check(BROWSER_ROWS[8],
                      all(d >= FAR and s >= SPREAD for _, d, s in empties),
                      "; ".join(f"at {at}: {d:.2f} from the background, spread {s:.2f}"
                                for at, d, s in empties)
                      + f" (bars: {FAR} and {SPREAD}); sampled on the one-cue score, where this "
                        f"instrument is the whole frame. This is the coverage declaration measured "
                        f"rather than argued: a log-polar map answers every point of the plane")

                # ---- §7: the placement its declaration buys --------------------------------------
                place = js(br, """
                  var b = window.__exPass.bench;
                  return {declared: b.coverageOf('tunnel'),
                          asGround: b.coverageWhyNo([
                            {id: 'ground', instrument: {id: 'tunnel', api: 1}, stack: 0},
                            {id: 'over', instrument: {id: 'matter', api: 1}, stack: 1}]),
                          asRoof: b.coverageWhyNo([
                            {id: 'floor', instrument: {id: 'weave', api: 1}, stack: 0},
                            {id: 'ground', instrument: {id: 'tunnel', api: 1}, stack: 1}])};
                """)
                took_stack = js(br, "return window.__offer(%s, {clock: %r, progress: 0.3});"
                                % (SCORE_UNDER, CLOCK))
                br.sleep(0.4)
                br.evaluate("window.__cancel('placement row'); 0")
                idle(br)
                check(BROWSER_ROWS[9],
                      place["declared"] and place["declared"]["writes"] is False
                      and place["asGround"] is None
                      and isinstance(place["asRoof"], str) and "«tunnel»" in place["asRoof"]
                      and took_stack["took"],
                      f"the host reads this instrument's declaration as writes="
                      f"{place['declared']['writes']} and places it by it. Laid lowest with a "
                      f"coverage-writing voice above, the stack is lawful and the host takes the "
                      f"score. Laid over a floor that is itself lawful, it is refused by name: "
                      f"«{place['asRoof']}»")

                over_crop = js(br, "return window.__exPass.bench.manifest('matter')"
                                   ".framings['1'].coverCrop;")
                stack_doors = []
                for at, work, name in (
                        (0.0, towers, "towers.jpg, seated by this instrument with no crop"),
                        (1.0, work_in_the_frame(BENCH / "photos" / "glassgrid.jpg", w, h,
                                                over_crop),
                         "glassgrid.jpg under the arriving voice's own crop of %s" % over_crop)):
                    p, _, _ = offer_shot(br, SCORE_UNDER, at,
                                         "stack-door-%03d" % round(at * 100))
                    stack_doors.append((at, name) + apart(p, work))
                check(BROWSER_ROWS[10],
                      all(mn <= SEAM for _, _, mn, _ in stack_doors),
                      "; ".join(f"door {at} against {n}: mean {mn:.4f} of 255 (threshold {SEAM}), "
                                f"worst channel {mx}" for at, n, mn, mx in stack_doors)
                      + ". A ground has to close its own frame at both ends or the cleared buffer "
                        "shows through the door the visitor lands on")

                br.set_viewport(VW - 80, VH - 120)
                br.sleep(0.8)
                br.evaluate("window.__resize(); 0")
                br.sleep(0.3)
                _, d, s = offer_shot(br, SCORE, 0.3, "after-resize")
                sized = js(br, "return {w: document.querySelector('canvas[aria-hidden]').width, "
                               "buffer: window.__report().census.buffer, "
                               "pdb: window.__report().census.preserveDrawingBuffer};")
                br.set_viewport(VW, VH)
                br.sleep(0.5)
                br.evaluate("window.__resize(); 0")
                br.sleep(0.3)
                check(BROWSER_ROWS[11],
                      d >= FAR and s >= SPREAD and sized["pdb"] is False,
                      f"after the viewport moved to {VW - 80}x{VH - 120} the buffer reads "
                      f"{sized['buffer']} and the frame stands {d:.2f} from the background with a "
                      f"spread of {s:.2f}; the context keeps preserveDrawingBuffer={sized['pdb']}. "
                      f"The corridor's whole map reads the frame's own ratio and the footprint the "
                      f"taps are spread over reads the buffer's own height, so both are rebuilt at "
                      f"the new grid rather than re-shown")

                # ---- the seeded repeat -----------------------------------------------------------
                br.sleep(0.6)
                took = js(br, "return window.__offer(%s, {clock: %r, progress: 0.3});"
                          % (SCORE, CLOCK))
                br.sleep(1.2)
                first = png(br, SHOTS / "seeded-1.png")
                rep1 = js(br, "return window.__report();")
                br.evaluate("window.__cancel('between runs'); 0")
                idle(br)
                js(br, "return window.__offer(%s, {clock: %r, progress: 0.3});" % (SCORE, CLOCK))
                br.sleep(1.2)
                second = png(br, SHOTS / "seeded-2.png")
                mn, mx = diff(first, second)
                check(BROWSER_ROWS[12], took["took"] and mn == 0.0 and mx == 0,
                      f"took={took['took']} two runs of one seeded score at one pinned second: mean "
                      f"{mn} worst channel {mx}. Every number the shader reads comes from a handle, "
                      f"and the die that sets the drift's phase is the score's — the instrument "
                      f"rolls none of its own, so a seeded run repeats to the pixel while a fresh "
                      f"seed sends the corridor wandering somewhere else")

                # ---- ten runs, and the baseline --------------------------------------------------
                base_c = rep1["census"]
                for _ in range(10):
                    js(br, "return window.__offer(%s, {clock: %r, progress: 0.3});" % (SCORE, CLOCK))
                    br.sleep(0.12)
                    br.evaluate("window.__cancel('leak row'); 0")
                br.sleep(0.4)
                after = js(br, "return window.__report();")["census"]
                same = (after["textures"] == base_c["textures"] == 2
                        and after["programs"] == base_c["programs"]
                        and after["framebuffers"] == base_c["framebuffers"] == 0
                        and after["canvases"] == base_c["canvases"] == 1
                        and after["contexts"] == base_c["contexts"] == 1)
                check(BROWSER_ROWS[13], same,
                      f"before={base_c['textures']}/{base_c['programs']}/{base_c['framebuffers']} "
                      f"after ten runs={after['textures']}/{after['programs']}/"
                      f"{after['framebuffers']} (textures/programmes/framebuffers)")

                errs = json.loads(br.evaluate("JSON.stringify(window.__errs||[])"))
                check(BROWSER_ROWS[14], not errs, "; ".join(errs)[:300])

                # ---- §4.4b: the measured handles reach the PICTURE -------------------------------
                # Each of the six is walked from one end of its own published range to the other at
                # one mark of the dial, and the frame has to move by a wide multiple of the seam. A
                # handle that names a measurement and does not reach the picture would be a number
                # nobody sees.
                MID = round((OPEN_DONE + FLOOD_DONE) / 2, 4)
                js(br, "return window.__both(%r);" % MID)
                walks = []
                for key, lo, hi in (("centreX", 0.2, 0.8), ("centreY", 0.2, 0.8),
                                    ("depth", 0.05, 0.95), ("ribs", 0.1, 0.9),
                                    ("spokes", 4, 18), ("twist", 0.0, 1.0)):
                    br.evaluate("window.__param(%r, %r); 0" % (key, lo))
                    br.sleep(0.35)
                    _, a = host_shot(br, MID, "handle-%s-lo" % key)
                    br.evaluate("window.__param(%r, %r); 0" % (key, hi))
                    br.sleep(0.35)
                    _, b2 = host_shot(br, MID, "handle-%s-hi" % key)
                    walks.append((key, lo, hi) + diff(a, b2))
                    br.evaluate("window.__param(%r, %r); 0"
                                % (key, {"centreX": 0.5, "centreY": 0.5, "depth": 0.26,
                                         "ribs": 0.5, "spokes": 10, "twist": 0.16}[key]))
                    br.sleep(0.3)
                check(BROWSER_ROWS[16], all(mn > SEAM for _, _, _, mn, _ in walks),
                      "; ".join(f"`{k}` {lo} to {hi}: {mn:.2f} of 255, worst channel {mx}"
                                for k, lo, hi, mn, mx in walks)
                      + f" (bar {SEAM}). Every one of the six names a measurement of the "
                        f"photographs, and every one of them moves the picture")

                # ---- the real transaction road ---------------------------------------------------
                br.evaluate("window.__cancel('road row'); 0")
                idle(br)
                road_gen = js(br, "return window.__offer(%s, {clock: %r, progress: 0.4});"
                              % (SCORE, CLOCK))
                br.sleep(0.9)
                mid_road = js(br, "var r = window.__report(); return {state: r.state, drew: r.drew, "
                                  "curtains: window.__hooks.curtains.slice(), "
                                  "docks: window.__hooks.docks.slice()};")
                js(br, "return window.__offer(%s, {clock: %r, progress: 1});" % (SCORE, CLOCK))
                br.sleep(1.4)
                end_road = js(br, "return {docks: window.__hooks.docks.slice(), "
                                  "state: window.__report().state};")
                br.evaluate("window.__cancel('road row'); 0")
                idle(br)
                check(BROWSER_ROWS[17],
                      road_gen["took"] and mid_road["state"] == "running"
                      and mid_road["drew"] == 1 and mid_road["curtains"]
                      and mid_road["curtains"][0] is True
                      and end_road["docks"].count(end_road["docks"][-1]) == 1,
                      f"the host took the offer, raised its curtain ({mid_road['curtains']}), drew "
                      f"{mid_road['drew']} pass a frame while running, and docked exactly once at "
                      f"the end (docks {end_road['docks']}, state {end_road['state']})")

                # ---- the door, WALKED on the buffer ----------------------------------------------
                walked, grids = [], []
                for vw2, vh2 in ((VW, VH), (320, 720), (500, 500)):
                    br.set_viewport(vw2, vh2)
                    br.sleep(0.8)
                    br.evaluate("window.__resize(); 0")
                    br.sleep(0.4)
                    gw = int(br.evaluate(
                        "String(document.querySelector('canvas[aria-hidden]').width)"))
                    gh = int(br.evaluate(
                        "String(document.querySelector('canvas[aria-hidden]').height)"))
                    grids.append((gw, gh))
                    for at in (0.0, 1.0):
                        v = js(br, "window.__mix(%r); return window.__values();" % at)
                        walked.append((at, (gw, gh), v))
                br.set_viewport(VW, VH)
                br.sleep(0.4)
                away = js(br, "window.__mix(%r); return window.__values();" % MID)
                one = walked[0][2]["doorMap"]

                def whole(at, g, v):
                    return (v["doorMap"] and v["doorMap"]["walked"] >= 26
                            and v["doorMap"]["offPx"] < 0.5 and v["doorMap"]["wrong"] == 0
                            and v["doorMap"]["dial"] == 0 and v["doorWhyNo"] is None
                            and v["doorGrid"]["w"] == g[0] and v["doorGrid"]["h"] == g[1]
                            and v["doorGrid"]["drawn"] is True)

                broke = [(at, g, v["doorMap"], v["doorGrid"], v["doorWhyNo"])
                         for at, g, v in walked if not whole(at, g, v)]
                check(BROWSER_ROWS[18],
                      not broke
                      and away["doorMap"] is None and away["doorWhyNo"] is None
                      and away["doorHeld"] is None,
                      "his 18:00 decision, answered on the buffer: at every door on every grid this "
                      "host handed, the instrument walked its own sample coordinate at the buffer's "
                      "own sample points and published what it read. %d readings across grids from "
                      "%s to %s, each walking %d points, every one of them standing %.2e points "
                      "from the door work's own cover fit with the dial at %s and %d of them "
                      "reading the other work. Away from a door the reading is not taken at all "
                      "(doorGrid=%s), and nothing is held: a corridor's flat door is exact by "
                      "construction, so a fault this reading finds is refused rather than closed. "
                      "The reading at the entry door on %s: %s"
                      % (len(walked), "%dx%d" % grids[0], "%dx%d" % grids[2],
                         one["walked"], one["offPx"], one["dial"], one["wrong"],
                         away["doorGrid"], "%dx%d" % grids[0], one)
                      if not broke else "these readings are not whole: %s" % (broke, ))

                # ---- THE DOOR REFUSED ON THE REAL TRANSACTION ROAD -------------------------------
                def road(gen):
                    return js(br, "var r = window.__report(); return {state: r.state, "
                                  "drew: r.drew, buffer: r.census.buffer, "
                                  "refused: r.events.filter(function(e){ return e.gen === %d "
                                  "&& e.why && String(e.why).indexOf('door leaks') >= 0; })"
                                  ".map(function(e){ return e.name + ': ' + e.why; })};" % gen)

                br.evaluate("window.__cancel('door road row'); 0")
                idle(br)
                shut_gen = js(br, "return window.__offer(%s, {clock: %r, progress: 0});"
                              % (json.dumps(tunnel_score(mask=0)), CLOCK))["gen"]
                br.sleep(1.0)
                played = road(shut_gen)
                br.evaluate("window.__cancel('door road row'); 0")
                idle(br)
                open_gen = js(br, "return window.__offer(%s, {clock: %r, progress: 0});"
                              % (json.dumps(tunnel_score(mask=1)), CLOCK))["gen"]
                br.sleep(1.1)
                leaked = road(open_gen)
                br.evaluate("window.__cancel('door road row'); 0")
                idle(br)
                check(BROWSER_ROWS[19],
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

                kept = sorted(p.name for p in SHOTS.glob("*.png"))
                check(BROWSER_ROWS[20],
                      len(kept) >= 30 and all((SHOTS / k).stat().st_size > 1000 for k in kept),
                      f"{len(kept)} captures under {SHOTS.relative_to(ROOT)}: the seven poses on "
                      f"both roads, the seven marks of the arriving work's own act, the seven "
                      f"sampled instants, the two doors in a stack, the frame after a resize, the "
                      f"two seeded runs and the twelve handle walks")

    shutil.rmtree(BENCH, ignore_errors=True)

    # ================================================================================================
    # THE TWO BENCHES OF THEIR OWN, run once the session above has closed its browser. This machine
    # holds two headless browsers at a time and several lanes share it, so a second browser raised
    # INSIDE a running session starves both and the screenshot channel times out — which is a fact
    # about the machine and not about the instrument. Both of these need a bench of their own: the
    # first because the two filters have to be levelled in the served bytes, the second because the
    # host's programme cache holds one entry per branch and outlives every transaction, so a session
    # that has already drawn grants two programmes to a score declaring one.
    # ================================================================================================
    SCORE = json.dumps(tunnel_score())

    def two_roads(b2):
        out = {}
        for tag, at in [("door-0", 0.0)] + OPEN:
            v, hp, mp = roads(b2, at, tag)
            out[tag] = [v["flood"]] + list(diff(hp, mp))
        out["_buffers"] = js(b2, "return window.__buffers();")
        return out

    two = on_bench(two_roads, level=True)
    agree = [] if not two else [(t, ) + tuple(two[t][1:])
                                for t, _ in [("door-0", 0.0)] + OPEN]
    check(BROWSER_ROWS[6],
          bool(two) and all(mn <= ROADS for _, mn, _ in agree)
          and two["_buffers"]["host"] == two["_buffers"]["module"]
          and all(two[t][0] == 0 for t, _ in [("door-0", 0.0)] + OPEN),
          "; ".join(f"{t}: mean {mn:.4f} of 255 (bar {ROADS}), worst channel {mx}"
                    for t, mn, mx in agree)
          + f". Both roads drew on a {two and two['_buffers']['host']} buffer, so one sampler ran "
            f"through one rasteriser on both sides and what is left between them is arithmetic. The "
            f"six poses are the flat door and five marks through the OPENING act, where the "
            f"corridor is built out of the departing work alone and the module has the same picture "
            f"to draw — the flood stands at nothing at every one of them. The module is served with "
            f"its crop table set to the rectangle this port derives and its mip level levelled with "
            f"the port's own taps, and nothing else changed"
          if two else "the levelled bench never came up")

    r = on_bench(lambda b2: (
        js(b2, "return window.__offer(%s, {clock: %r, progress: 0.4});" % (SCORE, CLOCK)),
        b2.sleep(0.8),
        js(b2, "return window.__report();")["resources"])[-1])
    check(BROWSER_ROWS[15],
          r and r["declared"] and r["over"] is False
          and r["granted"]["textures"] == r["declared"]["textures"]
          and r["granted"]["programs"] == r["declared"]["programs"] == 1
          and r["granted"]["framebuffers"] == r["declared"]["framebuffers"] == 0
          and r["granted"]["bytes"] == r["declared"]["bytesEstimate"],
          f"declared={r and r['declared']} granted={r and r['granted']}: one programme, one pass a "
          f"frame and no framebuffer of its own")

    # ================================================================================================
    # THE RED-ON-BUG PROOFS. Each reverts one rule this port states, in the artifact the browser
    # actually loads, and reads the number that moved. The pack served is changed and the host is
    # re-stamped with the digest of the bytes it is handed, which is what the build does; the file on
    # disk is never touched, so no working tree can be left changed by a proof.
    # ================================================================================================
    MID_AT = round((OPEN_DONE + FLOOD_DONE) / 2, 4)

    def frame_at(br, at, tag):
        return host_shot(br, at, tag)[1]

    def door_read(br, tag="red-door"):
        v = js(br, "window.__mix(0); return window.__values();")
        p = frame_at(br, 0.0, tag)
        ww = int(br.evaluate("String(document.querySelector('canvas[aria-hidden]').width)"))
        hh = int(br.evaluate("String(document.querySelector('canvas[aria-hidden]').height)"))
        return {"apart": apart(p, work_in_the_frame(PHOTOS[0], ww, hh))[0],
                "wrong": v["doorMap"]["wrong"] if v["doorMap"] else None,
                "whyNo": v["doorWhyNo"]}

    # ---- 1. the derived crop replaced by the module's own typed rectangle ------------------------
    # His 19:13 word lifted to the class at 19:21, reverted in the artifact the browser loads: the
    # piece of the picture the corridor's wall carries goes back to the rectangle the module types
    # for a photograph it names, and stops reading the pair's own measured centre. The number that
    # moves is the frame itself.
    def open_frame(br, tag):
        br.evaluate("window.__param('centreX', 0.3); window.__param('centreY', 0.3); 0")
        br.sleep(0.4)
        return frame_at(br, MID_AT, tag)

    base_crop = on_bench(lambda b: open_frame(b, "red-crop-standing"))
    bug = PACK.replace("var side = clamp(room, CROP_MIN, CROP_MAX);",
                       "var side = 0.48; cx = 0.5; cy = 0.26;", 1)
    bug_crop = on_bench(lambda b: open_frame(b, "red-crop-reverted"), pack_text=bug)
    crop_gap = None if (base_crop is None or bug_crop is None) else diff(base_crop, bug_crop)
    check(RED_ROWS[0],
          bug != PACK and crop_gap is not None and crop_gap[0] > SEAM,
          f"the wall's own rectangle stands about the pair's measured radial centre and takes the "
          f"largest square that fits inside the picture around it. Put back to the module's own "
          f"first typed rectangle — the one written by hand for a photograph it names — the frame "
          f"moves {crop_gap[0]:.2f} of 255 with a worst channel of {crop_gap[1]}, against the "
          f"project's seam threshold of {SEAM}. So the measurement reaches the picture and is not "
          f"only written on the manifest"
          if crop_gap else "the proof did not run")

    # ---- 2. the wipe's depth unbounded at the hole ------------------------------------------------
    # The depth axis runs away without bound at the vanishing point, so the station could never stand
    # beyond ALL of it. Reading the wipe's own depth at the hole's own radius is what bounds it and
    # what makes the entry door exact. Take the bound off and the hole at the far end reads the
    # ARRIVING work at the entry door, where the door's own law asks for the departing one — and the
    # instrument refuses the door in its own words.
    base_door = on_bench(lambda b: door_read(b, "red-door-standing"))
    bug = PACK.replace("float rlw = max(rl, HOLE);", "float rlw = rl;", 1).replace(
        "var rlw = Math.max(rl, HOLE);", "var rlw = rl;", 1)
    bug_door = on_bench(lambda b: door_read(b, "red-door-reverted"), pack_text=bug)
    check(RED_ROWS[1],
          bug != PACK and base_door and bug_door
          and base_door["wrong"] == 0 and base_door["whyNo"] is None
          and base_door["apart"] <= SEAM
          and bug_door["wrong"] and bug_door["whyNo"]
          and "read the arriving work" in bug_door["whyNo"],
          f"with the bound standing, the entry door reads {base_door['wrong']} of its walked points "
          f"on the arriving work and stands {base_door['apart']:.4f} of 255 from the departing "
          f"work's own file. With it taken off, {bug_door['wrong']} of those points read the "
          f"arriving work and the instrument refuses the door: «{bug_door['whyNo']}»"
          if bug_door else "the proof did not run")

    # ---- 3. the contact shade at the meeting ring removed -----------------------------------------
    # The second count of the charter's own wipe test asks whether the two images interact. They meet
    # at a ring of the corridor that carries a contact shade, read in points of the drawing buffer,
    # the way the folding instrument's crease does. Switched off, the frame at the meeting parts by a
    # wide multiple of the seam.
    base_shade = on_bench(lambda b: frame_at(b, MID_AT, "red-shade-standing"))
    bug = PACK.replace("col *= 1.0 - RING_SHADE * uWipe.y * exp(-abs(ringPx) / RING_REACH);",
                       "col *= 1.0;", 1)
    bug_shade = on_bench(lambda b: frame_at(b, MID_AT, "red-shade-reverted"),
                         pack_text=bug)
    shade_gap = None if (base_shade is None or bug_shade is None) else diff(base_shade, bug_shade)
    check(RED_ROWS[2],
          bug != PACK and shade_gap is not None and shade_gap[1] > SEAM,
          f"the two works meet at a ring of the corridor and the ring carries a contact shade, read "
          f"in points of the drawing buffer so it is the same physical edge whatever the fall is "
          f"doing to the geometry. Switched off in the served bytes the frame parts by "
          f"{shade_gap[0]:.2f} of 255 with a worst channel of {shade_gap[1]}, against the project's "
          f"seam threshold of {SEAM}. That shade is what answers the second count of the charter's "
          f"own wipe test: the two images interact at the boundary rather than one simply replacing "
          f"the other"
          if shade_gap else "the proof did not run")


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
