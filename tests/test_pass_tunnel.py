#!/usr/bin/env python3
"""PASS-API-V1 — the corridor instrument on the host's frame.
Run: python3 tests/test_pass_tunnel.py

Root: his word of 2026-08-18 08:52 after walking the live route — «переходы очень однообразные: у
тебя дофига эффектов и ты сделал все очень топорно» — and the charter's own vocabulary row for this
module: «tunnel | коридор | переход (mystery middle) | SURFACE | approved; псевдо-тоннель В24 cut —
the real corridor with interaction stays» (lab/CROSSING-HISTORY.md). The composer has named a
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
import datetime
import hashlib
import math
import json
import os
import re
import shutil
import subprocess
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
# THE RESHOOT PLAN.md ROW S-85 NAMES. The three instruments the shared seam move repaired are
# photographed again on the reading that now reaches them, under one path with the date and the
# commit of the run beside them, so the row's evidence can be found without reading this file.
RESHOOT = ROOT / "tests" / "captures" / "s05-reshoot"
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

# "PASS-TUNNEL neither door is cropped, and the file says why" — the real proof is a render, not a
# grep for the manifest's own text, so it stands with the DOORS loop below (which already renders
# both doors against a crop=1 reference) plus a red-on-bug row that reserves headroom in the actual
# fit() the shader uses and shows the render depart. See the DOORS loop and RED_ROWS[4].

# EVERY GEOMETRIC PARAMETER NAMES THE MEASUREMENT IT READS. His 19:13 word, lifted to the class at
# 19:21. This is the row that holds the whole class law for this instrument.
READS = [
    ("centreX", "motifs.radialCentre, and structure.radial.centre"),
    ("centreY", "motif — read on the other axis"),
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

# ------------------------------------------------------------------------------------------------
# IS THE RING A WIPE? THE THREE-PART TEST, ANSWERED ON THE REAL SHADER RATHER THAN ON ITS COMMENT.
# ------------------------------------------------------------------------------------------------
# The same test tests/test_pass_layer.py answers for its own boundary, answered here for the
# corridor's ring: the REAL, CURRENT fragment shader is extracted out of the BUILT file (never a
# hand-copied string — the array-of-literals `var FRAG = [...].join("\n")` this file writes its
# shaders in, scanned the way `test_pass_layer.py`'s `parse_concat_string` scans its own concatenated
# form), compiled in real headless-Chrome WebGL, and driven with controlled uniforms rather than
# through a full page — the boundary the ring answers to is computed from `uCam`/`uLean`/`uRing`/
# `uWipe` alone and never samples a texture, so a synthetic solid-colour pair is enough to drive it.
#
#   (a) THE BOUNDARY IS A LEVEL SET OF THE VANISHING POINT (`uCam.yz`, the pair's own measured
#       radial centre standing in for the manifest's `centreX`/`centreY` reads), not a fixed frame
#       coordinate: the ring is read at two different settings of `uCam.yz`, and at each one it lands
#       exactly where that setting says.
#   (c) THE STANDARD DEVIATION ORTHOGONAL TO THE DEPTH AXIS STAYS AT ZERO: eight points walked around
#       a circle of one radius about the vanishing point read one identical value apiece, at both
#       radii and at both centres — a true ring, not a shape that secretly answers to frame x/y.
#   (b) THE TWO IMAGES INTERACT: a point inside the ring's own antialiased band renders a colour
#       strictly between the two textures' own flat colours — a blend the boundary produces, not a
#       hard replacement of one work by the other.
#
# THE RED HALF mutates the boundary's own vanishing point read back to a fixed frame coordinate —
# `uCam.yz` replaced by the constant `vec2(0.5, 0.5)` — and the SAME measurement is retaken: the ring
# stops moving with the declared centre and (a)/(c) flip from a clean single value to a mixed one,
# exactly as test_pass_layer.py's own red row flips on the banned `vUV.x` form.


def _skip_ws_and_comments(text, i):
    n = len(text)
    while True:
        while i < n and text[i] in " \t\r\n,":
            i += 1
        if text[i:i + 2] == "//":
            while i < n and text[i] != "\n":
                i += 1
            continue
        break
    return i


def parse_join_array(text, start_idx):
    """`text[start_idx:]` holds `"…", "…", …` (each element possibly trailed by a `// comment` on its
    own line) up to a closing `].join("\\n");` — the shape this file's own `VERT`/`FRAG` are written
    in. A scanner rather than a pattern, so it reads exactly what the file's own array builds."""
    i, n = start_idx, len(text)
    parts = []
    while True:
        i = _skip_ws_and_comments(text, i)
        if text[i] == "]":
            i += 1
            break
        if text[i] != '"':
            raise ValueError("parse_join_array: unexpected char at %d: %r" % (i, text[i:i + 20]))
        i += 1
        buf = []
        while text[i] != '"':
            if text[i] == "\\":
                buf.append(text[i:i + 2])
                i += 2
                continue
            buf.append(text[i])
            i += 1
        i += 1
        parts.append("".join(buf))
    end = text.index(";", i)
    raw = "\n".join(json.loads('"' + p + '"') for p in parts)
    return raw, end + 1


def extract_shader_array(text, var_name, after_idx=0):
    marker = "var %s = [" % var_name
    idx = text.index(marker, after_idx)
    return parse_join_array(text, idx + len(marker))


_TUN_FN_IDX = REGION.index("function tunnelInstrument()")
TUN_VERT_SRC, _tun_after_vert = extract_shader_array(REGION, "VERT", _TUN_FN_IDX)
TUN_FRAG_SRC, _tun_after_frag = extract_shader_array(REGION, "FRAG", _tun_after_vert)

_RING_W = _RING_H = 128
_RING_PAGE = """<!doctype html><html><head><meta charset="utf-8"></head><body>
<canvas id="c" width="%(w)d" height="%(h)d"></canvas>
<script>
function makeSolidTex(gl, r, g, b) {
  var t = gl.createTexture();
  gl.bindTexture(gl.TEXTURE_2D, t);
  gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, 1, 1, 0, gl.RGBA, gl.UNSIGNED_BYTE,
                new Uint8Array([r, g, b, 255]));
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.NEAREST);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
  return t;
}
window.__runTunnelFrag = function (vertSrc, fragSrc, u) {
  try {
    var canvas = document.getElementById("c");
    var gl = canvas.getContext("webgl") || canvas.getContext("experimental-webgl");
    if (!gl) return { error: "no webgl" };
    var vs = gl.createShader(gl.VERTEX_SHADER);
    gl.shaderSource(vs, vertSrc); gl.compileShader(vs);
    if (!gl.getShaderParameter(vs, gl.COMPILE_STATUS))
      return { error: "vert: " + gl.getShaderInfoLog(vs) };
    var fs = gl.createShader(gl.FRAGMENT_SHADER);
    gl.shaderSource(fs, fragSrc); gl.compileShader(fs);
    if (!gl.getShaderParameter(fs, gl.COMPILE_STATUS))
      return { error: "frag: " + gl.getShaderInfoLog(fs) };
    var prog = gl.createProgram();
    gl.attachShader(prog, vs); gl.attachShader(prog, fs); gl.linkProgram(prog);
    if (!gl.getProgramParameter(prog, gl.LINK_STATUS))
      return { error: "link: " + gl.getProgramInfoLog(prog) };
    gl.useProgram(prog);
    var quad = new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]);
    var buf = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, buf);
    gl.bufferData(gl.ARRAY_BUFFER, quad, gl.STATIC_DRAW);
    var loc = gl.getAttribLocation(prog, "aPos");
    gl.enableVertexAttribArray(loc);
    gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
    var texA = makeSolidTex(gl, u.colA[0], u.colA[1], u.colA[2]);
    var texB = makeSolidTex(gl, u.colB[0], u.colB[1], u.colB[2]);
    gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, texA);
    gl.activeTexture(gl.TEXTURE1); gl.bindTexture(gl.TEXTURE_2D, texB);
    function u1i(n, v) { gl.uniform1i(gl.getUniformLocation(prog, n), v); }
    function u1f(n, v) { gl.uniform1f(gl.getUniformLocation(prog, n), v); }
    function u2f(n, v) { gl.uniform2f(gl.getUniformLocation(prog, n), v[0], v[1]); }
    function u4f(n, v) { gl.uniform4f(gl.getUniformLocation(prog, n), v[0], v[1], v[2], v[3]); }
    u1i("uA", 0); u1i("uB", 1);
    u4f("uFitA", u.fitA); u4f("uFitB", u.fitB);
    u2f("uRes", [%(w)d, %(h)d]);
    u4f("uCam", u.cam); u4f("uLean", u.lean); u4f("uRing", u.ring);
    u2f("uWipe", u.wipe); u4f("uCrop", u.crop);
    u1f("uMask", u.mask); u1f("uSeam", u.seam);
    gl.viewport(0, 0, %(w)d, %(h)d);
    gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
    var px = new Uint8Array(%(w)d * %(h)d * 4);
    gl.readPixels(0, 0, %(w)d, %(h)d, gl.RGBA, gl.UNSIGNED_BYTE, px);
    return { pixels: Array.prototype.slice.call(px) };
  } catch (e) {
    return { error: String(e) };
  }
};
window.__ringBenchReady = true;
</script>
</body></html>""" % {"w": _RING_W, "h": _RING_H}

# THE RING'S OWN NUMBERS. `RL0` is the radius (in the shader's own leaned-and-scaled `rl` units, with
# `leanAmt` held at zero so `rl` is a pure Euclidean radius from the vanishing point) at which the
# boundary sits, `LOGB`/`Z0` are the depth axis' own log-base and start, and `WIPE_X` is the station
# that places the crossing there — all four picked once, in the open, rather than smuggled in as
# whatever the shader happens to do.
_RING_RL0 = 0.3
_RING_LOGB = 1.0
_RING_Z0 = 0.0
_RING_WIPE_X = _RING_Z0 - math.log(_RING_RL0) / _RING_LOGB
_RING_R_IN = 0.7 * _RING_RL0    # clearly on the near side of the crossing
_RING_R_OUT = 1.4 * _RING_RL0   # clearly on the far side


def _ring_uniforms(cx, cy, mask=1.0, d=1.0, wipe_y=0.0):
    return {
        "colA": [220, 60, 60], "colB": [60, 60, 220],
        "fitA": [1, 1, 0, 0], "fitB": [1, 1, 0, 0],
        "cam": [1.0, cx, cy, 1.0],
        "lean": [1.0, 0.0, 0.0, _RING_LOGB],
        "ring": [_RING_Z0, 0.0, 10.0, d],
        "wipe": [_RING_WIPE_X, wipe_y],
        "crop": [0.0, 0.0, 1.0, 1.0],
        "mask": mask, "seam": 0.1,
    }


def _ring_sample_points(cx, cy, r, n=8):
    """`n` points around a circle of physical radius `r` (in `rl` units) about (cx, cy), in the
    shader's own `vUv` space — `p = (uv - c) * 2`, so `uv = c + p / 2`."""
    pts = []
    for k in range(n):
        theta = 2 * math.pi * k / n
        pts.append((cx + (r * math.cos(theta)) / 2.0, cy + (r * math.sin(theta)) / 2.0))
    return pts


def _ring_pixel_at(pixels, ux, uy):
    # vUv.y runs 0 at the top of the buffer and 1 at the bottom (this file's own VERT, `0.5 -
    # aPos.y * 0.5`), while a read-back row 0 is the buffer's bottom row — so a `uv` is flipped
    # before it is turned into a row.
    px = max(0, min(_RING_W - 1, int(round(ux * _RING_W))))
    py = max(0, min(_RING_H - 1, int(round((1 - uy) * _RING_H))))
    o = (py * _RING_W + px) * 4
    return pixels[o], pixels[o + 1], pixels[o + 2]


def _ring_std(vals):
    m = sum(vals) / len(vals)
    return math.sqrt(sum((v - m) ** 2 for v in vals) / len(vals))


def run_ring_jobs(jobs):
    """`jobs`: a list of (vert_src, frag_src, uniforms). One browser, one page, run through every
    job in turn — the shader is real headless-Chrome WebGL each time, only the plumbing is shared."""
    d = Path(tempfile.mkdtemp(prefix="synth_tunring_"))
    (d / "index.html").write_text(_RING_PAGE, encoding="utf-8")
    out = []
    try:
        with serve(str(d)) as base:
            with Browser() as br:
                br.navigate(base + "/index.html")
                for _ in range(25):
                    if br.evaluate("String(!!window.__ringBenchReady)") == "true":
                        break
                    br.sleep(0.1)
                for vert_src, frag_src, u in jobs:
                    res = json.loads(br.evaluate(
                        "JSON.stringify(window.__runTunnelFrag(%s, %s, %s))"
                        % (json.dumps(vert_src), json.dumps(frag_src), json.dumps(u))))
                    out.append((res.get("pixels"), res.get("error")))
    finally:
        shutil.rmtree(d, ignore_errors=True)
    return out


_RING_CHECK = "PASS-TUNNEL the file answers the wipe's own three-part test on all three counts"
_RING_RED = ("PASS-TUNNEL red-on-bug · the ring's boundary reads a fixed frame coordinate instead "
             "of the pair's own measured centre")
_RING_CAM_FROM = "vec2 p = (uv - uCam.yz) * 2.0 * vec2(asp, 1.0) * uCam.w;"
_RING_CAM_TO = "vec2 p = (uv - vec2(0.5, 0.5)) * 2.0 * vec2(asp, 1.0) * uCam.w;"

if not chrome_available():
    skip(_RING_CHECK, "no headless Chrome on this machine — EXPECTED, pinned skip, never a "
                       "silent pass")
    skip(_RING_RED, "no headless Chrome on this machine — EXPECTED, pinned skip, never a "
                     "silent pass")
elif _RING_CAM_FROM not in TUN_FRAG_SRC:
    check(_RING_CHECK, False,
          "the boundary's own vanishing-point read was not found verbatim in the extracted shader, "
          "so the mutant could not be built off the shipped text")
    skip(_RING_RED, "the standing row above did not find its own anchor")
else:
    CENTRES = [(0.5, 0.5), (0.3, 0.3)]
    green_jobs = []
    for cx, cy in CENTRES:
        green_jobs.append((TUN_VERT_SRC, TUN_FRAG_SRC, _ring_uniforms(cx, cy)))
    # THE INTERACTION SAMPLE (count b): mask off, the corridor's own colour-grading finish gated to
    # nothing (`uRing.w = 0`, the same gate the shader's own `d` uses) so the antialiased band between
    # the two flat colours is read undisturbed, and the contact shade turned on (`uWipe.y = 1`) so
    # the ring's own coupling is live. The sample point sits inside the band the render above showed
    # holds a genuine blend.
    green_jobs.append((TUN_VERT_SRC, TUN_FRAG_SRC,
                        _ring_uniforms(0.5, 0.5, mask=0.0, d=0.0, wipe_y=1.0)))
    green_out = run_ring_jobs(green_jobs)

    errs = [e for _, e in green_out if e]
    if errs:
        check(_RING_CHECK, False, "the bench never rendered: " + "; ".join(errs)[:300])
        skip(_RING_RED, "the standing row above never rendered")
    else:
        def _ring_readings(pixels, cx, cy):
            vin = [_ring_pixel_at(pixels, ux, uy)[0]
                   for ux, uy in _ring_sample_points(cx, cy, _RING_R_IN)]
            vout = [_ring_pixel_at(pixels, ux, uy)[0]
                    for ux, uy in _ring_sample_points(cx, cy, _RING_R_OUT)]
            return vin, vout

        STD_TOL = 5.0
        SEP_MIN = 150.0

        def _ring_clean(vin, vout):
            return (_ring_std(vin) <= STD_TOL and _ring_std(vout) <= STD_TOL
                    and abs((sum(vin) / len(vin)) - (sum(vout) / len(vout))) >= SEP_MIN)

        readings = [_ring_readings(green_out[i][0], cx, cy) for i, (cx, cy) in enumerate(CENTRES)]
        # ONE POINT INSIDE THE RING'S OWN ANTIALIASED BAND (rl = 0.28, just short of the crossing at
        # rl0 = 0.3): `uv = centre + (rl/2, 0)`.
        blend_r, blend_g, blend_b = _ring_pixel_at(green_out[-1][0], 0.5 + 0.28 / 2.0, 0.5)
        blended = 70 <= blend_r <= 210

        clean_all = all(_ring_clean(vin, vout) for vin, vout in readings)
        check(_RING_CHECK,
              clean_all and blended,
              "; ".join(f"centre {cx, cy}: inner std {_ring_std(vin):.2f}, outer std "
                        f"{_ring_std(vout):.2f}, separation "
                        f"{abs((sum(vin) / len(vin)) - (sum(vout) / len(vout))):.1f}"
                        for (cx, cy), (vin, vout) in zip(CENTRES, readings))
              + f"; the ring's own antialiased band reads ({blend_r}, {blend_g}, {blend_b}), between "
                f"the two flat colours (220, 60, 60) and (60, 60, 220) rather than equal to either. "
                f"(a) the boundary is read exactly where each declared vanishing point says, at "
                f"both centres tried; (c) eight points walked around one radius about that centre "
                f"read one identical value apiece — a true ring; (b) the boundary blends the two "
                f"works rather than replacing one with the other")

        # ---- THE RED-ON-BUG PROOF: the vanishing-point read put back to a fixed frame coordinate --
        red_jobs = [(TUN_VERT_SRC, TUN_FRAG_SRC.replace(_RING_CAM_FROM, _RING_CAM_TO, 1),
                     _ring_uniforms(0.3, 0.3))]
        red_out = run_ring_jobs(red_jobs)
        if red_out[0][1]:
            check(_RING_RED, False, "the mutant bench never rendered: %s" % red_out[0][1])
        else:
            vin_r, vout_r = _ring_readings(red_out[0][0], 0.3, 0.3)
            hurt_clean = _ring_clean(vin_r, vout_r)
            check(_RING_RED,
                  not hurt_clean,
                  f"the SAME reading at the SAME declared centre (0.3, 0.3), with `uCam.yz` in the "
                  f"boundary's own read replaced by the constant `vec2(0.5, 0.5)`: inner std "
                  f"{_ring_std(vin_r):.2f}, outer std {_ring_std(vout_r):.2f}, separation "
                  f"{abs((sum(vin_r) / len(vin_r)) - (sum(vout_r) / len(vout_r))):.1f} — the ring "
                  f"stayed where the frame's own centre is rather than moving to the declared "
                  f"vanishing point, so the clean single-valued reading above breaks")

# "PASS-TUNNEL the judges' handle publishes what the door is read against, and that nothing is
# held" — the real proof reads the LIVE registered manifest's `handles.mask.applied.readAtADoor`
# (see the Chrome section, right after `m` is fetched) rather than grepping the source for the
# fields' own names, and a red-on-bug row (RED_ROWS[3]) mutates `DOOR_SLIP`/`DOOR_SHOW` in the built
# instrument and shows a door the real values pass gets refused under the mutated ones.

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
    "PASS-TUNNEL S-85   · the ring-join's width comes off the host, on the buffer the frame is drawn on",
]

RED_ROWS = [
    "PASS-TUNNEL red-on-bug · the derived crop replaced by the module's own typed rectangle",
    "PASS-TUNNEL red-on-bug · the wipe's own radius unbounded at the hole: the entry door reads "
    "the arriving work",
    "PASS-TUNNEL red-on-bug · the contact shade at the meeting ring removed",
    "PASS-TUNNEL red-on-bug · DOOR_SLIP/DOOR_SHOW tightened past what the real door clears",
    "PASS-TUNNEL red-on-bug · the fit the doors are cover-fitted by reserves headroom",
    "PASS-TUNNEL red-on-bug · S-85: the ring-join read back off the file's own retired number",
]

# ROWS THAT RUN INSIDE THE MAIN BENCH BLOCK BUT ARE NOT ADDRESSED BY INDEX (BROWSER_ROWS[n]) — named
# checks the two skip branches below and the bottom's "never ran" sweep must still cover, so an
# absent Chrome or an absent lab tree never leaves them silently missing from the report.
EXTRA_ROWS = [
    "PASS-TUNNEL the judges' handle publishes what the door is read against, and that nothing is "
    "held",
    "PASS-TUNNEL neither door is cropped, and the file says why",
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


def reshoot(src, name, note):
    """One frame of the S-85 reshoot, kept under the row's own path with the run's date and commit.
    The note is written beside the frames rather than into them, so a reader can see WHICH reading
    each shot stands on and on which buffer without opening a test file."""
    RESHOOT.mkdir(parents=True, exist_ok=True)
    dst = RESHOOT / ("tunnel-" + name + ".png")
    shutil.copy2(src, dst)
    note = dict(note)
    note["at"] = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    try:
        note["commit"] = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"],
                                        capture_output=True, text=True,
                                        timeout=20).stdout.strip() or None
    except Exception:
        note["commit"] = None
    (RESHOOT / "tunnel.json").write_text(json.dumps(note, indent=1), encoding="utf-8")
    return dst


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


# ---------------------------------------------------------------- the composer's own world-fold list
# THE WORLD SURFACES `spendsTheMiracle` DERIVES — engine/assets/pass-composer.js's own
# `WORLD_FOLD_INSTRUMENTS`, which does NOT name tunnel. Read by REAL code execution in node rather
# than by grepping the manifest's own prose beside it, the same `vm.createContext`/`vm.runInContext`
# idiom test_pass_composed.py's own DRIVER uses: the real module is loaded in a sandboxed VM off a
# fake `window.__PassComposer`, `PLANTS` names literal substitutions to make in the source text
# before it loads — never touching the file on disk — and `composer.worldFoldInstruments` is read
# off the object the real `make()` returns.
COMPOSER_SRC = ROOT / "engine" / "assets" / "pass-composer.js"
COMPOSED_FIXTURE = ROOT / "tests" / "fixture_pass_composed.json"

WORLD_FOLD_DRIVER = r"""
"use strict";
const fs = require("fs"), vm = require("vm");
const [modulePath, fixturePath] = process.argv.slice(2);
const plants = JSON.parse(process.env.PLANTS || "[]");
let source = fs.readFileSync(modulePath, "utf8").replace(/@@NS@@/g, "");
for (const [from, to] of plants) {
  if (source.indexOf(from) < 0) {
    console.log(JSON.stringify({error: "the plant found nothing to change: " + from}));
    process.exit(0);
  }
  source = source.split(from).join(to);
}
let joined = null;
const sandbox = {window: {__PassComposer: (m) => { joined = m; }}, console};
vm.createContext(sandbox);
vm.runInContext(source, sandbox, {filename: "pass-composer.js"});
if (!joined) {
  console.log(JSON.stringify({error: "the module joined nothing"}));
  process.exit(0);
}
const fix = JSON.parse(fs.readFileSync(fixturePath, "utf8"));
const composer = joined.make(fix.consts);
console.log(JSON.stringify({worldFoldInstruments: composer.worldFoldInstruments}));
"""


def node_available():
    try:
        return subprocess.run(["node", "--version"], capture_output=True).returncode == 0
    except Exception:
        return False


def run_world_fold_driver(plants=()):
    if not node_available():
        return {"error": "no node on this machine"}
    d = Path(tempfile.mkdtemp(prefix="synth_tunworldfold_"))
    driver_path = d / "world-fold-driver.js"
    driver_path.write_text(WORLD_FOLD_DRIVER, encoding="utf-8")
    env = dict(os.environ, PLANTS=json.dumps(list(plants)))
    try:
        proc = subprocess.run(["node", str(driver_path), str(COMPOSER_SRC), str(COMPOSED_FIXTURE)],
                              capture_output=True, text=True, env=env, timeout=120)
        if proc.returncode != 0:
            return {"error": (proc.stderr or "").strip()[-400:]}
        return json.loads(proc.stdout.strip().splitlines()[-1])
    finally:
        shutil.rmtree(d, ignore_errors=True)


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
    for r in BROWSER_ROWS + RED_ROWS + EXTRA_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
elif missing:
    for r in BROWSER_ROWS + RED_ROWS + EXTRA_ROWS:
        skip(r, "the lab tree is read-only source material and is absent here: " + missing[0])
else:
    shutil.rmtree(SHOTS, ignore_errors=True)
    SHOTS.mkdir(parents=True, exist_ok=True)
    BENCH = bench_dir()
    with serve(BENCH) as base:
        with Browser(width=VW, height=VH) as br:
            br.navigate(base + "/index.html")
            if not ready(br):
                for r in BROWSER_ROWS + EXTRA_ROWS:
                    check(r, False, "the bench never came up: "
                         + br.evaluate("JSON.stringify(window.__errs||[])"))
            elif not js(br, "return !!window.__exPass.bench.manifest('tunnel');"):
                why = js(br, "var e = window.__host.report().events.filter(function(x){"
                             "return x.name === 'manifest-refused';});"
                             "return e.length ? e[e.length - 1].why : null;")
                for r in BROWSER_ROWS + EXTRA_ROWS:
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

                # THE JUDGES' HANDLE'S OWN FIELDS, READ OFF THE LIVE REGISTERED MANIFEST rather than
                # grepped out of the source. `readAtADoor` is what the door reads the mask handle
                # against: the drawing buffer, counted in "flatness", with nothing held.
                rad = m["handles"]["mask"]["applied"]["readAtADoor"]
                check("PASS-TUNNEL the judges' handle publishes what the door is read against, and "
                      "that nothing is held",
                      rad["points"] == 0.5 and rad["readOn"] == "the drawing buffer"
                      and rad["reads"] == "flatness" and rad["held"] is None,
                      f"the live manifest's handles.mask.applied.readAtADoor reads {rad} — a "
                      f"half-point tolerance on the drawing buffer, counted in flatness, with no "
                      f"hold. A corridor's flat door is exact by construction and not by a "
                      f"tolerance: the dead band spends the hand and the dial is exactly nothing "
                      f"inside it, so anything the reading finds is a real fault that no widening "
                      f"closes. RED_ROWS[3] mutates the two constants this points value and this "
                      f"door's own mask threshold are read from and shows a door the real values "
                      f"pass gets refused under the mutated ones")

                # THE OTHER HALF OF THIS ROW IS NOT A TEXT MATCH FOR "spends no crossing's miracle" —
                # it is pass-composer.js's own `WORLD_FOLD_INSTRUMENTS` derivation, read by REAL code
                # execution in node (the same `vm.createContext`/`vm.runInContext` idiom
                # test_pass_composed.py's own DRIVER uses), asserting "tunnel" is absent from the
                # live list `spendsTheMiracle` reads, and then mutating the built
                # composer's own predicate to drop the surface requirement and showing the returned
                # `worldFoldInstruments` now carries it — a real execution proof that the composer's
                # list is what decides this, not a grep for a sentence beside it.
                world_fold_base = run_world_fold_driver()
                world_fold_mutated = run_world_fold_driver(plants=[(
                    'return !!surface && (m.levels || []).indexOf("WORLD") >= 0;',
                    'return iid === "tunnel" || (!!surface && (m.levels || []).indexOf("WORLD") >= 0);')])
                world_fold_ok = (
                    node_available()
                    and "error" not in world_fold_base
                    and "tunnel" not in world_fold_base.get("worldFoldInstruments", [])
                    and "error" not in world_fold_mutated
                    and "tunnel" in world_fold_mutated.get("worldFoldInstruments", []))
                check(BROWSER_ROWS[1],
                      m["levels"] == ["SURFACE", "CELL"] and world_fold_ok,
                      f"levels={m['levels']}, and the source of that reading is his own standing "
                      f"verdict on this module in lab/CROSSING-HISTORY.md's vocabulary table, which "
                      f"carries the level in the same row: SURFACE. Shelf 17's levels law keeps "
                      f"WORLD for the camera and gives SURFACE «floor, cylinder, ribbon», so a "
                      f"corridor is a surface — which is why this instrument spends no crossing's "
                      f"one miracle and a quiet link may play it as readily as a culmination. CELL "
                      f"is the rings, which is where the two works meet. CELL CONTENT, TEXTURE and "
                      f"LIGHT-COLOUR are not claimed. The real composer, run in node, carries "
                      f"worldFoldInstruments={world_fold_base.get('worldFoldInstruments')} — "
                      f"«tunnel» absent — and with the derived predicate planted to admit it, carries "
                      f"worldFoldInstruments={world_fold_mutated.get('worldFoldInstruments')}"
                      if node_available() else
                      "levels=%s; no node on this machine to run the composer's own derivation — "
                      "EXPECTED, pinned fail rather than a silent pass" % m["levels"])

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

                door_apart = {}
                for i, (door, own, other, ownn, othern) in enumerate((
                        ("door-0", towers, glass, "towers.jpg", "glassgrid.jpg"),
                        ("door-1", glass, towers, "glassgrid.jpg", "towers.jpg"))):
                    a, amx = apart(shots[door], own)
                    door_apart[door] = (a, amx, ownn)
                    check(BROWSER_ROWS[2 + i * 2], a <= SEAM,
                          f"{door} against {ownn}, cover-fitted and cropped by nothing: mean "
                          f"{a:.4f} of 255 (threshold {SEAM}), worst channel {amx}. Inside the dead "
                          f"band the dial is exactly nothing, so the sample coordinate the shader "
                          f"reads at is the plain cover-fit point and the taps spread over nothing "
                          f"— one fetch of one point, which is the picture the file carries")
                    o, _ = apart(shots[door], other)
                    check(BROWSER_ROWS[3 + i * 2], o >= FAR,
                          f"{door} against {othern}: mean {o:.4f} of 255 (must exceed {FAR})")

                # "PASS-TUNNEL neither door is cropped, and the file says why" — the render just
                # taken IS the proof: both doors already stand within the seam of a plain crop=1
                # cover fit. RED_ROWS[4], in the tail RED-ON-BUG section below, mutates the actual
                # code path that decides the crop applied at a door — this instrument's own `fit()`,
                # not the manifest's declared `coverCrop` text, which nothing in this file or in
                # pass-composer.js ever reads back out at render time — and shows the same door
                # depart from this same reference once it reserves headroom.
                check("PASS-TUNNEL neither door is cropped, and the file says why",
                      door_apart["door-0"][0] <= SEAM and door_apart["door-1"][0] <= SEAM,
                      f"door-0 against towers.jpg: mean {door_apart['door-0'][0]:.4f} of 255; "
                      f"door-1 against glassgrid.jpg: mean {door_apart['door-1'][0]:.4f} of 255 "
                      f"(threshold {SEAM}), both cover-fitted and cropped by nothing. A log-polar "
                      f"map answers every point of the plane, so this instrument asks the frame for "
                      f"no headroom — RED_ROWS[4] mutates the actual `fit()` this render is taken "
                      f"through to reserve some and shows the same door depart from this same "
                      f"crop=1 reference")

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

                # ---- S-85 · the seam is the HOST'S number, on the buffer this frame is drawn on --
                # PLAN.md row S-85, and the owner's decision of 2026-09-03: the equality stands at
                # the buffer the frame is drawn at, because that is the frame a visitor's eye meets.
                # Until this row the bench handed no `seams` at all, so every frame ever photographed
                # here stood on `RING_JOIN_FALLBACK` — the number this file kept from before the
                # shared move — and the move itself was never once shot. The bench hands it now, and
                # what is proved is an EQUIVALENCE rather than a bare equality: the picture moves if
                # and only if the number does. Three shots at one pose on one buffer — the host's own
                # answer, that same number typed in by this row, and the file's retired one.
                seam_host = js(br, "return window.__seams();")["ring"]
                seam_old = float(re.search(r"var RING_JOIN_FALLBACK = ([0-9.]+);", PACK).group(1))
                seam_scale = js(br, "var c = document.querySelector('canvas[aria-hidden]');"
                                    "return c ? c.width / Math.max(window.innerWidth, 1) : null;")

                def seam_shot(pin, tag):
                    br.evaluate("window.__seamPin(%s); 0" % pin)
                    br.sleep(0.1)
                    out = host_shot(br, 0.5, tag)[1]
                    return out

                s_host = seam_shot("undefined", "s85-host")
                s_hand = seam_shot(json.dumps({"ring": seam_host}), "s85-by-hand")
                s_old = seam_shot(json.dumps({"ring": seam_old}), "s85-retired")
                br.evaluate("window.__seamPin(undefined); 0")
                d_hand = diff(s_host, s_hand)[0]
                d_old, x_old = diff(s_host, s_old)
                same_number = abs(seam_host - seam_old) < 1e-12
                reshoot(s_host, "host", {"instrument": "tunnel",
                                         "seam": {"kind": "ring", "unit": "a share of one repeat's "
                                                  "own span"},
                                         "bufferPointsPerCssPixel": seam_scale,
                                         "hostAnswers": seam_host, "fileRetired": seam_old,
                                         "apartOf255": round(d_old, 4),
                                         "shots": ["tunnel-host.png", "tunnel-retired.png"]})
                reshoot(s_old, "retired", {"instrument": "tunnel",
                                           "seam": {"kind": "ring", "unit": "a share of one "
                                                    "repeat's own span"},
                                           "bufferPointsPerCssPixel": seam_scale,
                                           "hostAnswers": seam_host, "fileRetired": seam_old,
                                           "apartOf255": round(d_old, 4),
                                           "shots": ["tunnel-host.png", "tunnel-retired.png"]})
                check(BROWSER_ROWS[21],
                      d_hand == 0.0 and ((d_old == 0.0) == same_number),
                      f"on the buffer this frame is drawn on — {seam_scale} buffer point(s) per CSS "
                      f"pixel — §8's `seams` block answers this instrument's ring-join with "
                      f"{seam_host}, and the number its own file falls back to before any host has "
                      f"answered is {seam_old}. Handed that same width by hand the frame is the "
                      f"host's frame to the pixel ({d_hand} of 255), so the width is the WHOLE of "
                      f"what the host hands and the picture is a function of it; handed the file's "
                      f"retired number instead the frame stands {d_old:.2f} of 255 away (worst "
                      f"channel {x_old}). The picture moves exactly when the number does, which is "
                      f"what makes the seam the host's to answer and no longer this file's to keep. "
                      f"The reshoot stands under {RESHOOT.relative_to(ROOT)}")

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

    # ---- 4. DOOR_SLIP/DOOR_SHOW tightened past what the real door clears --------------------------
    # Both constants are read inside `doorWhyNoOf`'s own three branches. A door the real values pass
    # cleanly (the entry door at mix=0: no measured slip, no wrong work, mask resting at its own
    # default of 0) is refused once either threshold is tightened past what that door actually
    # measures — DOOR_SLIP taken negative refuses on ANY measured slip at all, and DOOR_SHOW taken
    # negative refuses on the mask resting at 0 — which is what proves the two constants actually
    # gate the door's own accept/refuse decision rather than sitting beside it unread.
    base_slip = on_bench(lambda b: door_read(b, "red-slip-standing"))
    bug = PACK.replace("var DOOR_SLIP = 0.5;", "var DOOR_SLIP = -1;", 1)
    bug_slip = on_bench(lambda b: door_read(b, "red-slip-reverted"), pack_text=bug)
    bug = PACK.replace("var DOOR_SHOW = 0.5 / 255;", "var DOOR_SHOW = -1;", 1)
    bug_show = on_bench(lambda b: door_read(b, "red-show-reverted"), pack_text=bug)
    check(RED_ROWS[3],
          base_slip and bug_slip and bug_show
          and base_slip["whyNo"] is None
          and bug_slip["whyNo"] is not None and "door leaks" in bug_slip["whyNo"]
          and bug_show["whyNo"] is not None and "door leaks" in bug_show["whyNo"],
          f"with the real constants, the entry door reads clean: whyNo={base_slip['whyNo']}. With "
          f"`DOOR_SLIP` taken to -1 in the served bytes, the same door is refused: "
          f"«{bug_slip['whyNo'] if bug_slip else None}». With `DOOR_SHOW` taken to -1 instead, the "
          f"same door is refused on the judges' channel resting at its own default: "
          f"«{bug_show['whyNo'] if bug_show else None}». So both constants actually decide the door "
          f"rather than sitting unread beside the manifest's own words about them"
          if (base_slip and bug_slip and bug_show) else "the proof did not run")

    # ---- 5. the fit the doors are cover-fitted by reserves headroom -------------------------------
    # `manifest.framings` is never read back out at render time — not by this file, not by
    # pass-composer.js — so the code path that actually decides a door's crop is this instrument's
    # own `fit()`. Made to reserve headroom the way Python's own `cover_into(..., crop=0.85)` does,
    # the same door (mix=0, against towers.jpg cover-fitted with no crop) now departs from that
    # reference by a wide multiple of the seam.
    bug = PACK.replace(
        "    function fit(iw, ih, w, h) {\n"
        "      var fa = w / Math.max(h, 1);\n"
        "      var ia = iw / Math.max(ih, 1);\n"
        "      if (ia > fa) return [fa / ia, 1, 0, 0];\n"
        "      return [1, ia / fa, 0, 0];\n"
        "    }",
        "    function fit(iw, ih, w, h) {\n"
        "      var fa = w / Math.max(h, 1);\n"
        "      var ia = iw / Math.max(ih, 1);\n"
        "      if (ia > fa) return [fa / ia / 0.85, 1 / 0.85, 0, 0];\n"
        "      return [1 / 0.85, ia / fa / 0.85, 0, 0];\n"
        "    }", 1)

    def door0_frame(br, tag):
        br.evaluate("window.__mix(0); 0")
        return frame_at(br, 0.0, tag)

    base_fit = on_bench(lambda b: door0_frame(b, "red-fit-standing"))
    bug_fit = on_bench(lambda b: door0_frame(b, "red-fit-reverted"), pack_text=bug)
    fit_gap = None if (base_fit is None or bug_fit is None) else apart(base_fit, towers)
    bug_gap = None if bug_fit is None else apart(bug_fit, towers)
    check(RED_ROWS[4],
          bug != PACK and fit_gap is not None and bug_gap is not None
          and fit_gap[0] <= SEAM and bug_gap[0] > SEAM,
          f"door-0 against towers.jpg cover-fitted with no crop: mean {fit_gap[0] if fit_gap else '?'} "
          f"of 255 with the real `fit()` (threshold {SEAM}). With `fit()` reserving headroom the way "
          f"`cover_into(..., crop=0.85)` does, the same door against the same reference now stands "
          f"{bug_gap[0] if bug_gap else '?'} of 255 apart. So the crop=1 claim is carried by the "
          f"function that actually draws the door, not by the manifest's own declared number"
          if (fit_gap and bug_gap) else "the proof did not run")

    # ---- 6. S-85 · the ring-join read back off the file's own retired number ----------------------
    # The plant PLAN.md row S-85 names: leave the width read from the old constant. The instrument's
    # own line takes the host's answer where one arrives and stands on `RING_JOIN_FALLBACK` where
    # none does; reverted in the served bytes it stands on the constant whatever the host answers,
    # which is the state the shared move was built to end. On the buffer this bench draws at, the two
    # numbers are not the same number, so the equality the row above holds breaks and the frame moves.
    base_seam = on_bench(lambda b: frame_at(b, 0.5, "red-seam-standing"))
    bug = PACK.replace(
        'var seam = (st.seam && typeof st.seam.ring === "number") ? st.seam.ring '
        ': RING_JOIN_FALLBACK;',
        'var seam = RING_JOIN_FALLBACK;', 1)
    bug_seam = on_bench(lambda b: frame_at(b, 0.5, "red-seam-reverted"), pack_text=bug)
    seam_gap = None if (base_seam is None or bug_seam is None) else diff(base_seam, bug_seam)
    check(RED_ROWS[5],
          bug != PACK and seam_gap is not None and seam_gap[0] > 0,
          f"with the instrument's own read reverted to the number its file kept from before the "
          f"shared move, the same pose on the same buffer parts by {seam_gap[0]:.4f} of 255 (worst "
          f"channel {seam_gap[1]}) from the shipped frame — so the row above is held up by the "
          f"host's answer actually reaching the picture and not by the two numbers happening to "
          f"agree" if seam_gap is not None else
          f"the proof did not run (planted={bug != PACK})")


shutil.rmtree(TMP, ignore_errors=True)

ran = {name for name, _, _ in results}
for name in BROWSER_ROWS + RED_ROWS + EXTRA_ROWS:
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
