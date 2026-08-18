#!/usr/bin/env python3
"""PASS-API-V1 — the planet instrument on the host's frame.
Run: python3 tests/test_pass_planet.py

Root: his word of 2026-08-18 08:52 after walking the live route — «переходы очень однообразные: у
тебя дофига эффектов и ты сделал все очень топорно» — and his 08:58 «перенеси ВЕСЬ арсенал». The lab
holds 23 effect modules and the engine held six instruments; this is the port of lab/effects/planet.js,
whose own standing verdict in lab/CROSSING-BRIEF.md's vocabulary reads «approved; curl is the
раскладушка axis for radial works». docs/design/PASS-API-V1.md §7 (GPU and resources), §8 (the
manifest) and §9's conformance rows 7, 9, 10, 13, 14, 15, 16 and 22 are what this file makes real,
together with §7's coverage law of 12:40. The lifecycle rows stay in tests/test_pass_api.py.

WHAT THE INSTRUMENT DOES, so a reader knows what the rows below are about. The departing photograph
curls until its two ends meet and closes into a small round world standing in its own sky. The
arriving photograph rises out of that world's own centre — where the picture's rows collapse to a
point — and floods outward ring by ring until it owns the world. Then the world uncurls and the
arriving photograph stands flat. That shape is the charter's own shelf 8: «flat → world → flat», with
«B enters through the singular locus».

WHAT IS COMPARED, AND AGAINST WHAT.

  The doors. At the dial's two ends one whole work stands, cover-fitted into the frame and cropped by
  nothing at all — which is what lab/data/module-contract.json publishes for this module's own two
  doors — inside the project's seam threshold of 6 of 255.

  THE TWO ROADS. Both draw with WebGL and both run one fragment shader through one rasteriser, so the
  residual between them is a difference of arithmetic. The bar is therefore the project's own seam
  threshold and not one this suite invented. THE LAB MODULE IS SERVED WITH ITS TEXTURE FILTERING
  LEVELLED and the row that reads it says so: its mipmap chain and its anisotropic filtering are taken
  off, because the host's two source textures carry neither and an instrument may not upload a texture
  of its own. A row of its own measures what that missing chain costs, and it is a reading rather than
  a gate.

  Over the first quarter of the dial the whole frame belongs to the departing work, so the two roads
  are compared point for point over every pixel. Past that the arriving work owns part of the world,
  so the comparison is masked to the points the judges' channel says the departing work still owns —
  which is where the module has anything to say at all.

  The coverage. This instrument declares that it writes none. That is measured rather than declared:
  the judges' channel paints how much of the page's own colour stands at each point, and the greatest
  reading anywhere on the frame is what the row publishes.

  No empty frame. The rows below sample the pass at seven instants and once across a change of
  viewport, and each frame has to stand as a picture.

  The lab module is READ ONLY. Absent, every browser row here is a pinned SKIP that names the missing
  path — never a silent pass.

WHAT IS NEVER RESTORED FROM GIT. Every red-on-bug proof below serves a CHANGED copy of the instrument
to the browser and writes the site record with the digest of the bytes actually served. The source
tree is never written to.
"""
import base64
import hashlib
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

# The lab module and the photographs stand in the MAIN tlvphotos worktree, which is where the suites
# of the ports before this one read them from too.
LAB = Path(os.environ.get("TLVPHOTOS_ROOT", "/Users/sashaabramovich/tlvphotos")) / "lab"
PHOTOS = [LAB / "photos" / "tower-clouds.jpg", LAB / "photos" / "dark-tower-clouds.jpg"]
MODULE = LAB / "effects" / "planet.js"

SITE_URL = "https://synth.example.com"
VW, VH = 390, 844          # the phone frame lab/carrier-check.py measures on
SEAM = 6.0                 # the project's seam threshold, 6 of 255 (TRANSITION-STAGE-V0 §1)
FAR = 40.0                 # further than this from a file and it is a different work
BACKGROUND = (0x08, 0x08, 0x0a)
SPREAD = 10.0
ROADS = SEAM

# The module's own three photographs, read as the table it is (planet.js:28-37): how much of the
# frame the figure holds, how many rows are used, and the horizon's own gamma. The two named shares
# are the module's own sentence — «the building fills two thirds of the first frame and a fifth of
# the last» — and the middle row is the check.
FIG_LO, FIG_HI = 0.20, 0.667
CROP_LO, CROP_HI = 0.62, 0.98
GAMMA_LO, GAMMA_HI = 0.36, 0.76
CROP_MID, GAMMA_MID = 0.72, 0.50

SHOTS = ROOT / "tests" / "captures" / "pass-planet"

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


DIE = 4.91016            # the die lab/data/scores' own weave score carries, so every suite rolls one
DURATION_MS = 6500


def _static(v):
    return {"op": "static", "value": v}


def planet_cue(stack=0, levels_own=None, **statics):
    """The cue, with a track for every one of the nine handles (§4.4b)."""
    P = {"clock": 0, "curl": 0.82, "depth": 0, "dip": 0.5, "turn": 0.5, "gather": FIG_HI,
         "shade": 1, "mask": 0}
    P.update(statics)
    nodes = {"p-mix": {"source": "progress"}}
    tracks = {"mix": {"node": "p-mix"}}
    for k, v in P.items():
        nodes["p-" + k] = _static(v)
        tracks[k] = {"node": "p-" + k}
    return {
        "id": "planet-main", "instrument": {"id": "planet", "api": 1},
        "voice": "letter", "roles": ["disassembly", "mystery", "assembly"],
        "levels": ["WORLD", "SURFACE"],
        "levelOwnership": levels_own or {"WORLD": "owns", "SURFACE": "owns"},
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


def planet_score(under=False, **statics):
    """`under` puts a coverage-writing voice ABOVE this instrument, which is the placement its own
    declaration buys it: the ground of a stack."""
    cues = [planet_cue(stack=0, **statics)]
    if under:
        cues = cues + [matter_cue(stack=1)]
    res = {"textures": 0, "textureSlots": 2, "framebuffers": 0, "pingPong": 0, "programs": 1,
           "passes": 1, "bytesEstimate": 0}
    return {
        "schema": 2,
        "intent": "the departing photograph curls into a small round world, the arriving one rises "
                  "out of that world's own centre and floods it ring by ring, and the world uncurls "
                  "into the arriving photograph standing flat (lab/effects/planet.js:1-20, its own "
                  "header, and the charter's shelf 8)",
        "pair": {"a": "a", "b": "b"},
        "seed": DIE,
        "duration": DURATION_MS,
        "direction": "a-to-b",
        "interruption": {"withinMs": 500, "resolve": "nearest-door"},
        "failLand": "arrive",
        "camera": {"owner": "stage", "rests": "b",
                   "track": [{"at": "b", "pan": {"x": 0, "y": 0}, "logScale": 0,
                              "pitch": 0, "yaw": 0, "roll": 0, "fov": None, "owner": "stage"}]},
        "cues": cues,
        "quality": {v: {"renderScale": None,
                        "cues": {c["id"]: {"resources": dict(res, variant=v)} for c in cues}}
                    for v in ("lean", "standard", "rich")},
        "provenance": {"source": "lab/effects/planet.js's own declared defaults and constants",
                       "measuredAt": None, "by": "tests/test_pass_planet.py"},
    }


# ---------------------------------------------------------------- bake once
build_site.SITE_CONFIG = dict(build_site.SITE_CONFIG)
build_site.SITE_CONFIG["pass"] = {"visualLayer": "pass", "diagnostics": "on"}

TMP = Path(tempfile.mkdtemp(prefix="synth_passplanet_"))
build_site.OUT = TMP
build_site.build(SITE_URL)
LAYER = (TMP / "pass-layer.js").read_text(encoding="utf-8")
# THE INSTRUMENT'S OWN BUILT FILE — the real artifact a visitor is served, comments stripped. Since
# every instrument travels alone, the whole of this file is this instrument and nothing else.
PACK = (TMP / "pass-inst-planet.js").read_text(encoding="utf-8")
REGION = PACK
SOURCE = ROOT / "engine" / "assets" / "pass-inst-planet.js"
# The file as it stands in the tree, comments and all: the rows about what this instrument DECLARES
# read the built artifact, and the rows about what it SAYS read the source it is built from.
SOURCE_TEXT = SOURCE.read_text(encoding="utf-8")
LABTXT = MODULE.read_text(encoding="utf-8") if MODULE.exists() else ""

# ---------------------------------------------------------------- string rows

OWNED = ["createElement", "getContext", "requestAnimationFrame", "addEventListener",
         "performance.now", "Date.now", "new Image", "setTimeout", "setInterval"]
held = [s for s in OWNED if s in REGION]
check("PASS-PLANET the instrument creates no element, no loop and no listener",
      not held,
      "§1.2's fence, read against the instrument's own built file: none of the nine ways of owning "
      "hardware appears there. The module raises its own canvas, takes a WebGL2 context on it, "
      "uploads its own textures with their mipmap chains, runs its own frame loop, observes its own "
      "mount for a resize and listens to the pointer; all of it stayed in the lab"
      if not held else "the instrument's region holds " + ", ".join(held))

HANDLES = ["mix", "clock", "curl", "depth", "dip", "turn", "gather", "shade", "mask"]
absent = [h for h in HANDLES if ("%s: { min" % h) not in REGION]
check("PASS-PLANET every handle the instrument publishes is a handle a score can drive",
      not absent and len(HANDLES) == 9,
      "§4.4b: nine handles. The dial, the score's own second, the module's own curl and its two "
      "hidden handles — the turn and the horizon — the choice between the two worlds this geometry "
      "draws, the figure's own share of the frame that the module read by hand out of its table, "
      "the world's finish and the judges' channel. The module's `photo` is published by neither, "
      "and the file says why: a cue carries an ordered pair, so which photographs stand is the "
      "host's" if not absent else "these are published nowhere: " + ", ".join(absent))

check("PASS-PLANET no seed handle is published, and the picture is what settles that",
      "seed: { min" not in REGION and "Math.random" not in LABTXT and "Math.random" not in REGION,
      "nothing in this picture is rolled: the module carries no die of its own and this port adds "
      "none, so a handle for one would be a handle a score could walk without moving the picture, "
      "which is noise in the score")

check("PASS-PLANET no clock of the instrument's own, and the module's two motions ride the score's",
      "extTime" in LABTXT and "clock: { min" in REGION
      and "clock * 0.052" in REGION and "clock * 0.115" in REGION,
      "the module counts its own second up in its own frame loop and takes an external one on the "
      "`clock` key; here that key is a handle and it is the only time this instrument knows. Both "
      "of the module's own motions ride it — the world's slow turn at 0.052 turns a second and the "
      "breath of the curl at 0.115 and 0.079 — so a driven walk repeats to the pixel and the world "
      "is still alive while it stands")

# Every constant the picture stands on, read out of the lab module and out of the built file.
CONSTANTS = [
    ("var ATM_REACH = 0.634;", "var ATM_REACH = 0.634;",
     "how far the sky wash reaches, derived from the frame's own farthest corner rather than "
     "chosen, so the world stands in its own light at any frame shape"),
    ("var TURN_REACH = 1.1;", "var TURN_REACH = 1.1;",
     "the turn's own reach, read off the pointer line it replaces"),
    ("var HORIZON_REACH = 0.5;", "var HORIZON_REACH = 0.5;",
     "and the horizon's, half a gamma either way"),
    ("var FEEL_K = 1.45;", "var FEEL_K = 1.45;",
     "the dial's own response curve: the one number fitted to the measured travel, where the "
     "picture curls fast at the start and slowly at the end"),
    ("var FEEL_H_C = 0.5, FEEL_H_K1 = 0.85, FEEL_H_K2 = 0.65;",
     "var FEEL_H_C = 0.5, FEEL_H_K1 = 0.85, FEEL_H_K2 = 0.65;",
     "the horizon's own two-piece logarithm, hinged at the middle because the middle is a door"),
    ("0.055 * (0.62 * Math.sin(lifeT * 0.115) + 0.38 * Math.sin(lifeT * 0.079))",
     "0.055 * (0.62 * Math.sin(clock * 0.115) + 0.38 * Math.sin(clock * 0.079))",
     "the breath: the world stays shut and the join opens by a few degrees"),
    ("clamp(1 - Math.pow(1 - clamp(curlBase + breath, 0, 1), 2.4), 0.006, 1)",
     "clamp(1 - Math.pow(1 - clamp01(curlBase + breath), 2.4), 0.006, 1)",
     "the curl's own easing: the first half is the bend, the second half closes the ring"),
    ("R * Math.min(1, (1 - Math.pow(1 - c, p)) * (1 + 0.35 * c))",
     "R * Math.min(1, (1 - Math.pow(1 - c, p)) * (1 + 0.35 * c))",
     "the radial thickness, whose hole shuts well before the ends meet"),
    ("var k = smoothstep(0.45, 0.78, c);", "var k = smoothstep(0.45, 0.78, c);",
     "when the framing stops holding the bowed band and pulls back to the whole world"),
    ("Math.min(W / (2 * hw), H / (2 * hh)) * 0.93",
     "Math.min(W / (2 * hw), H / (2 * hh)) * 0.93",
     "the disc is given nearly the whole short side and the wash takes the rest"),
    ("var far = smoothstep(0.62, 0.99, c);", "var far = smoothstep(0.62, 0.99, c);",
     "how solidly the picture is carried across the open wedge"),
    ("Math.max(Math.min(1.25 * R, 0.55 * Math.max(W, H) / S)",
     "Math.max(Math.min(1.25 * R, 0.55 * Math.max(W, H) / S)",
     "the wash's own floor, so a half-rolled strip keeps the reach it always had"),
    ("gl.uniform1f(U.uSeam, 0.14);", "var SEAM = 0.14;",
     "the narrowest cross-dissolve, so a shut ring has no cut down it either"),
    ("float fold(float x){ x = mod(abs(x), 2.0); return x > 1.0 ? 2.0 - x : x; }",
     "float fold(float x){ x = mod(abs(x), 2.0); return x > 1.0 ? 2.0 - x : x; }",
     "the fold past either end, so nothing streaks out of the join"),
    ("float blur = 1.0 + 14.0 * smoothstep(0.0, 0.12, lin);",
     "float blur = 1.0 + 14.0 * smoothstep(0.0, 0.12, lin);",
     "how far the picture is smeared into the open wedge"),
    ("float gv = uGamma * pow(max(t, 2e-3), uGamma - 1.0) * abs(uCrop.y - uCrop.x) / (uD * uS);",
     "float gv = uGamma * pow(max(t, 2e-3), uGamma - 1.0) * abs(uCrop.y - uCrop.x) / (uD * uS);",
     "the analytic derivative of the row coordinate — the module's anti-aliasing, and this port's "
     "footprint for the cut"),
    ("float shade = mix(1.0, mix(1.10, 0.74, smoothstep(0.18, 1.0, rn)), uWorld);",
     "float shade = mix(1.0, mix(1.10, 0.74, smoothstep(0.18, 1.0, rn)), fin);",
     "the radial curve of light, brightest a third of the way out"),
    ("0.13 * dot(d / r * min(r / uR, 1.15), vec2(-0.6, 0.8))",
     "0.13 * dot(d / r * min(r / uR, 1.15), vec2(-0.6, 0.8))",
     "one lamp, fixed to the stage rather than to the world, so the round thing reads round"),
    ("float dimOut = 0.74 * mix(1.0, 0.72, uFlip) * exp(-3.2 * outward);",
     "float dimOut = 0.74 * mix(1.0, 0.72, uFlip) * exp(-3.2 * outward);",
     "how the wash is dimmed outward, and held back where the world is inside out"),
    ("float dimIn  = 0.74 - 0.42 * smoothstep(0.0, 1.0, inward);",
     "float dimIn  = 0.74 - 0.42 * smoothstep(0.0, 1.0, inward);",
     "and inward, so a half-curled picture is not sitting on a black hole"),
    ("float rim  = 1.0 - smoothstep(0.0, 0.022, outward);",
     "float rim  = 1.0 - smoothstep(0.0, 0.022, outward);", "where the world's own edge stands"),
    ("float hole = smoothstep(0.0, 1.5 / (uD * uS), 1.0 - tr);",
     "float hole = smoothstep(0.0, 1.5 / (uD * uS), 1.0 - tr);",
     "and the hole in the middle of the roll"),
    ("float bell = smoothstep(0.0, clamp(0.35 * g, 0.05, 0.16), lin);",
     "float bell = smoothstep(0.0, clamp(0.35 * g, 0.05, 0.16), lin);",
     "how long the ends have to dissolve into the sky behind them"),
    ("float lod = mix(3.0, 7.0, outward);", "float lod = mix(3.0, 7.0, outward);",
     "how far the sky is smeared as it goes out"),
    ("float vSky = mix(0.93, 0.07, uFlip);", "float vSky = mix(0.93, 0.07, uFlip);",
     "which row of the picture the wash is read at"),
    ("gl.uniform3f(U.uBg, 0.031, 0.031, 0.036);", "vec3 DARK = vec3(0.031, 0.031, 0.036);",
     "what the very outside of the wash settles to"),
    ("res = pow(max(res, 0.0), vec3(mix(1.0, 1.12, uWorld)));",
     "col = pow(max(col, 0.0), vec3(mix(1.0, 1.12, fin)));",
     "the closing curve, which gives these pale flat skies some body"),
]
missing_const = [p for lab_p, p in ((a, b) for a, b, _ in CONSTANTS)
                 if lab_p not in LABTXT or p not in REGION]
check("PASS-PLANET every constant the picture stands on carries the module's own number",
      not missing_const and bool(LABTXT),
      "; ".join("%s — %s" % (p, why) for _, p, why in CONSTANTS) if not missing_const
      else "these differ between the lab module and the port: " + ", ".join(missing_const))

check("PASS-PLANET the port's own numbers are named as its own, and there are three",
      "var POLE_FROM = 0.25, POLE_TO = 0.75;" in REGION
      and "var CUT_ROOM = 0.02;" in REGION
      and "var WORLD_FLOOR = 0.20;" in REGION
      and "POLE_FROM" not in LABTXT and "CUT_ROOM" not in LABTXT and "WORLD_FLOOR" not in LABTXT,
      "the module curls ONE photograph and has no crossing to shape, so three numbers are this "
      "port's: where the arriving work rises — the middle half of the pass, which is the walk's own "
      "three phases, whose default in the client's register is [0.25, 0.5, 0.25]; how far past the "
      "picture's own rows the cut travels, so no row is left half blended at a door; and how "
      "strongly a work must read as a world before this crossing is worth playing on it")

# THE ONE DERIVATION THIS PORT MAKES, CHECKED AS ARITHMETIC. The module chose a crop and a gamma per
# photograph by hand and said why: how much of the frame the building fills. The instrument reads
# that share off the work instead, on the line through the two shares the module named. The module's
# own THIRD row was not used to fit either line, so it is a check — and the two lines place it at
# 0.329 and 0.363, one photograph read two independent ways.
fig_from_crop = FIG_LO + (CROP_MID - CROP_LO) * (FIG_HI - FIG_LO) / (CROP_HI - CROP_LO)
fig_from_gamma = FIG_LO + (GAMMA_MID - GAMMA_LO) * (FIG_HI - FIG_LO) / (GAMMA_HI - GAMMA_LO)
check("PASS-PLANET the crop and the horizon are read off the work, on the module's own table",
      "var FIG_LO = 0.20, FIG_HI = 0.667;" in REGION
      and "var CROP_LO = 0.62, CROP_HI = 0.98;" in REGION
      and "var GAMMA_LO = 0.36, GAMMA_HI = 0.76;" in REGION
      and "crop: [0.00, 0.98], gamma: 0.76" in LABTXT
      and "crop: [0.00, 0.72], gamma: 0.50" in LABTXT
      and "crop: [0.00, 0.62], gamma: 0.36" in LABTXT
      and "the building fills two thirds of the first frame and a fifth of the" in LABTXT
      and abs(fig_from_crop - fig_from_gamma) < 0.05,
      f"the module's table is three photographs, two of whose figure shares it names — two thirds "
      f"and a fifth — against a crop of 0.98 and 0.62 and a gamma of 0.76 and 0.36. Those are two "
      f"points, and the instrument reads a work's own measured figure share along the line through "
      f"them. The table's THIRD row fitted neither line, so it is the check: at a crop of "
      f"{CROP_MID} it stands at a figure share of {fig_from_crop:.3f} and at a gamma of "
      f"{GAMMA_MID} at {fig_from_gamma:.3f} — one photograph, two independent readings, agreeing to "
      f"{abs(fig_from_crop - fig_from_gamma):.3f}")

check("PASS-PLANET the host binds uniforms by declared name, never by position or a written list",
      "getUniformLocation(p, u.name)" in LAYER and "uGeom" not in LAYER and "uFlatPP" not in LAYER,
      "this instrument declares twelve uniforms, of which three are shared with every other "
      "instrument. The host reads the manifest")

declared = set(re.findall(r'\{ name: "(u\w+)", type:', REGION))
spelled = set(re.findall(r'uniform \w+ +(u\w+);', REGION))
check("PASS-PLANET the manifest's declared names and the shader's own names are one set",
      declared == spelled and len(declared) == 12,
      f"{len(declared)} declared, {len(spelled)} spelled; "
      f"declared only: {sorted(declared - spelled)}; spelled only: {sorted(spelled - declared)}. "
      f"The module handed its shader fourteen loose scalars; the host binds four types and no more, "
      f"so they travel four to a carrier and not one number changes")

SUPPLY = ["textureA", "textureB", "fitA", "fitB", "resolution", "seconds"]
sources = set(re.findall(r'source: "([^"]+)"', REGION))
outside = [s for s in sources
           if s not in SUPPLY and not s.startswith("frame:") and not s.startswith("handle:")]
check("PASS-PLANET every uniform is sourced from the closed set the host can supply",
      not outside and len(sources) >= 10,
      "§7's uniform sources are the two source textures, their fits, the resolution, the "
      f"transaction's seconds, a value the instrument answers and a handle. This instrument names "
      f"{len(sources)} distinct sources and none outside that set"
      if not outside else "outside the set: " + ", ".join(outside))

check("PASS-PLANET the shader carries no version header of its own, though the module's does",
      "#version" not in REGION and "#version 300 es" in LABTXT
      and "textureGrad" in REGION and "textureLod" in REGION
      and "gl_FragColor = vec4(col, 1.0);" in REGION,
      "the module writes the second version of the language and stamps its own header; every "
      "instrument of this engine hands the host a first-version source and lets the host's own "
      "translator stamp one, which is mechanical and touches no line of mathematics. Both roads end "
      "at the same compiled shader, and the second is the one the fleet takes — the host's own "
      "coverage law is read by finding each shader's output line, and a shader writing to an output "
      "of its own naming is a shader that law cannot read. The two filtered fetches this module "
      "depends on are second-version functions and they survive the translation untouched")

check("PASS-PLANET the manifest leaves the drawing buffer unpreserved",
      "gl: { preserveDrawingBuffer: false }" in REGION,
      "§7 refuses a manifest that asks for the buffer to be preserved; this instrument draws every "
      "frame the host hands it")

check("PASS-PLANET the coverage is declared, and the frame it fills is the reason",
      "coverage: { writes: false" in REGION
      and "gl_FragColor = vec4(col, 1.0);" in REGION
      and "opacity" not in REGION and "presence" not in REGION,
      "§8's coverage block and §7's law: the alpha is the constant 1, said as a decision. Outside "
      "the world's own rim the frame is not empty — it carries the sky of the work that owns the "
      "world, smeared wide and dimmed, and the reach of that wash is read off the frame itself. "
      "Under the placement rule that makes this instrument lawful as the LOWEST cue of a stack. No "
      "handle of opacity and no weight of presence stands anywhere in the instrument")

check("PASS-PLANET the two works meet at a hard cut and never at a dissolve",
      "float cov = clamp(0.5 + (uCut.x - row) / foot, 0.0, 1.0);" in REGION
      and "Coverage over a pixel's footprint, never transparency" in SOURCE_TEXT
      and "float foot = max(mix(uCut.y, gv, uWorld), 1e-6);" in REGION,
      "the charter bans the dead dissolve between two works, and this instrument's boundary is one "
      "row of the photograph with the share of a single point of the buffer as its only softening. "
      "In the world that row is a RING, because the world is the picture's rows wrapped round a "
      "circle; at the flat door it is the frame's own height. One law, two readings, and the same "
      "uWorld the sample coordinate is mixed on carries it between them")

check("PASS-PLANET every geometric handle publishes the measurement of the photograph it reads",
      'reads: "structure.polar.planet' in REGION
      and 'reads: "structure.polar.tunnel' in REGION
      and 'reads: "structure.horizon.y' in REGION
      and 'reads: "structure.radial.score' in REGION
      and "the share of the frame the work's own measured dominant object holds" in REGION,
      "his 19:13 word lifted to the class at 19:21. The curl reads how strongly the work already "
      "reads as a little world; which of the two worlds is drawn reads its own corridor reading; "
      "the horizon reads its own measured horizon; the turn reads its own radial score; and the "
      "crop reads the share of the frame its figure holds, which is the reading the module's own "
      "table of three photographs stands on")

check("PASS-PLANET the instrument measures no work for itself, and answers for the pair it is handed",
      "asks: asks," in SOURCE_TEXT and "asks: { reads:" in SOURCE_TEXT
      and "getImageData" not in REGION and "drawImage" not in REGION,
      "his word of 2026-08-18 09:01 — «просто пара приходит и ты смотришь какими инструментами ее "
      "вести». The instrument names the fields it reads and answers, for two work records, whether "
      "this crossing is worth playing on it and why in the works' own numbers. It reads no picture: "
      "measuring means drawing a work into a surface of its own and counting, and §1.2's fence "
      "leaves every surface to the host")

sha = hashlib.sha256(MODULE.read_bytes()).hexdigest() if MODULE.exists() else ""
declared_sha = (re.search(r'sha256: "([0-9a-f]{64})"', REGION) or [None, None])[1]
check("PASS-PLANET the provenance names the file the port was read from, and the file weighs to it",
      bool(sha) and sha == declared_sha and 'commit: "4952bfe"' in REGION,
      f"the module is tracked, so the commit it was read at is named beside the digest of its "
      f"bytes, and the file still weighs to {sha[:16]}…")

CONTRACT = LAB / "data" / "module-contract.json"
contract_says_world = False
if CONTRACT.exists():
    _row = json.loads(CONTRACT.read_text(encoding="utf-8"))["modules"].get("planet") or {}
    contract_says_world = _row.get("level") == "WORLD"
check("PASS-PLANET the two readings of this module's level are both recorded, and the shelf settles them",
      'levels: ["WORLD", "SURFACE"]' in REGION
      and "the vocabulary's SURFACE is the older and" in SOURCE_TEXT
      and contract_says_world,
      "lab/data/module-contract.json gives this module WORLD and the charter's vocabulary table "
      "gives it SURFACE. Shelf 8 names the sphere among its projection worlds and says a folded "
      "space is at most one per crossing and IS the miracle, which settles it: WORLD is declared "
      "and paid for — an instrument publishing it spends the crossing's one miracle — and SURFACE "
      "is kept because it is the level the CUT lives on")

# ---------------------------------------------------------------- the instrument as a pure function
NODE_ROWS = [
    "PASS-PLANET node   · both doors are exact by construction, on five grids",
    "PASS-PLANET node   · a door with the judges' channel open is refused, in the instrument's own numbers",
    "PASS-PLANET node   · a pair that reads as a world is taken, and one that does not is declined by name",
]

DRIVER = r"""
"use strict";
const fs = require("fs"), vm = require("vm");
const [modulePath] = process.argv.slice(2);
let source = fs.readFileSync(modulePath, "utf8").replace(/@@NS@@/g, "");
let joined = null;
const sandbox = {window: {__PassInstrument: (m) => { joined = m; }}, console};
vm.createContext(sandbox);
vm.runInContext(source, sandbox, {filename: "pass-inst-planet.js"});
if (!joined) { console.log(JSON.stringify({error: "the module joined nothing"})); process.exit(0); }
const I = joined.instrument;
const GRIDS = [[390, 844], [780, 1688], [195, 422], [1440, 900], [40, 60]];
function pose(mix, W, H, over) {
  return Object.assign({mix: mix, clock: 0, curl: 0.82, depth: 0, dip: 0.5, turn: 0.5,
                        gather: 0.667, shade: 1, mask: 0, reduced: false,
                        cssWidth: W, cssHeight: H, bufWidth: W, bufHeight: H,
                        aw: 900, ah: 450, bw: 900, bh: 450}, over || {});
}
const doors = [];
for (const [W, H] of GRIDS) {
  for (const mix of [0, 1]) {
    const v = I.values(pose(mix, W, H));
    doors.push({grid: [W, H], mix: mix, world: v.world, cut: v.cut[0], map: v.cutMap,
                whyNo: v.doorWhyNo, held: v.doorHeld, grids: v.doorGrid});
  }
}
const away = I.values(pose(0.5, 390, 844));
const open = I.values(pose(0, 390, 844, {mask: 1}));
const openOut = I.values(pose(1, 390, 844, {mask: 1}));
const world = {
  radial: {structure: {polar: {planet: 0.6733, tunnel: 0.4217, twirl: 0.1462},
                       horizon: {y: 0.6973}}},
  banded: {structure: {polar: {planet: 0.1102, tunnel: 0.0904, twirl: 0.0311},
                       horizon: {y: 0.4120}, banding: {score: 0.8807}}},
  spiral: {structure: {polar: {planet: 0.2400, tunnel: 0.1900, twirl: 0.5100},
                       horizon: {y: 0.5100}}},
  noHorizon: {structure: {polar: {planet: 0.8100, tunnel: 0.2000, twirl: 0.1000}}},
};
const asked = {
  bothWorlds: I.asks(world.radial, world.radial),
  oneWorld: I.asks(world.banded, world.radial),
  neither: I.asks(world.banded, world.banded),
  spiral: I.asks(world.spiral, world.spiral),
  noHorizon: I.asks(world.noHorizon, world.noHorizon),
  declared: I.manifest.asks,
};
console.log(JSON.stringify({doors: doors, away: {map: away.cutMap, grid: away.doorGrid},
                            open: open.doorWhyNo, openOut: openOut.doorWhyNo, asked: asked,
                            name: I.name, version: joined.version}));
"""

DRIVER_PATH = TMP / "planet-driver.js"
DRIVER_PATH.write_text(DRIVER, encoding="utf-8")


def node_available():
    try:
        return subprocess.run(["node", "--version"], capture_output=True).returncode == 0
    except Exception:
        return False


if not node_available():
    for r in NODE_ROWS:
        skip(r, "node is not installed (pinned expected skip)")
else:
    proc = subprocess.run(["node", str(DRIVER_PATH), str(SOURCE)],
                          capture_output=True, text=True, timeout=120)
    if proc.returncode != 0:
        for r in NODE_ROWS:
            skip(r, "the instrument would not load: " + (proc.stderr or "").strip()[-300:])
    else:
        got = json.loads(proc.stdout.strip().splitlines()[-1])
        d = got["doors"]
        bad = [x for x in d
               if x["world"] > 0.5 / 255 or x["map"] is None or x["map"]["wrong"] != 0
               or x["map"]["walked"] != 17 or x["whyNo"] is not None or x["held"] is not None
               or x["map"]["spareRows"] <= 0.01]
        check(NODE_ROWS[0],
              not bad and len(d) == 10 and got["away"]["map"] is None
              and got["away"]["grid"] is None,
              f"{len(d)} readings — both doors on five grids from 390x844 to 40x60 — and every one "
              f"walked {d[0]['map']['walked']} points of the buffer with {d[0]['map']['wrong']} "
              f"standing on the wrong work, the nearest of them {d[0]['map']['spareRows']:.4f} of "
              f"the picture's height clear of the cut. The world stands at {d[0]['world']:.1e} open "
              f"at the entry door and {d[1]['world']:.1e} at the exit: the dial's own window is a "
              f"sine at its zero at both ends and the cut stands past the picture's own rows at "
              f"both, so neither door is held by a tolerance. Away from a door nothing is read at "
              f"all"
              if not bad else f"these readings are not whole: {bad[:2]}")

        check(NODE_ROWS[1],
              isinstance(got["open"], str) and "the entry door leaks" in got["open"]
              and "the judges' own channel" in got["open"] and "390 x 844 buffer" in got["open"]
              and isinstance(got["openOut"], str) and "the exit door leaks" in got["openOut"],
              f"the one door this instrument's own handles can spoil is the judges' channel, and "
              f"the refusal is worded in this instrument's own measured numbers on the grid it was "
              f"measured on: «{got['open']}»")

        a = got["asked"]
        check(NODE_ROWS[2],
              a["bothWorlds"][0] is True and a["oneWorld"][0] is True
              and a["neither"][0] is False and a["spiral"][0] is False
              and a["noHorizon"][0] is False
              and a["declared"]["floor"] == 0.2
              and "structure.polar.planet" in a["declared"]["reads"],
              f"a pair whose departing work reads a sphere at 0.6733 with a measured horizon is "
              f"taken — «{a['bothWorlds'][1]}». A pair where only the ARRIVING work reads that way "
              f"is taken too, because a ground is the pair's — «{a['oneWorld'][1]}». A pair of works "
              f"that read as bands and not as worlds is declined — «{a['neither'][1]}». So is a pair "
              f"reading as a log-spiral, which is another instrument's world — «{a['spiral'][1]}» — "
              f"and so is one with no measured horizon, which has no ground and sky to become a "
              f"world — «{a['noHorizon'][1]}»")

# ---------------------------------------------------------------- browser rows

BROWSER_ROWS = [
    "PASS-PLANET §8     · the manifest carries every field the contract names, in its shape",
    "PASS-PLANET row 7  · door 0 stands the departing work, measured against its own file",
    "PASS-PLANET row 7  · door 0 carries no trace of the arriving work",
    "PASS-PLANET row 7  · door 1 stands the arriving work, measured against its own file",
    "PASS-PLANET row 7  · door 1 carries no trace of the departing work",
    "PASS-PLANET the two roads agree over the whole frame while the departing work owns it",
    "PASS-PLANET the two roads agree over the departing work's own points at the world's full opening",
    "PASS-PLANET the dial blends the sample coordinate and not the colour",
    "PASS-PLANET §7     · the frame is filled at every point of every sampled pose",
    "PASS-PLANET §7     · the ground of a stack, and refused above another cue",
    "PASS-PLANET §7     · both doors stand whole with a coverage-writing voice over them",
    "PASS-PLANET §7     · no empty frame at any sampled instant of the pass",
    "PASS-PLANET §7     · the frame after a change of viewport is drawn afresh",
    "PASS-PLANET row 10 · a driven run repeats to the pixel",
    "PASS-PLANET row 14 · textures, programmes and framebuffers return to their baseline after ten runs",
    "PASS-PLANET row 15 · the console stays clean",
    "PASS-PLANET row 22 · the census shows granted against declared, and neither overruns",
    "PASS-PLANET §7     · one canvas, one context, two source textures, one pass a frame",
    "PASS-PLANET §7     · a shader already at GLSL ES 3.00 receives no second version header",
    "PASS-PLANET the real transaction road: curtain up, one pass drawn, exactly one dock at the end",
    "PASS-PLANET row 9  · one camera authority through a real pass, and the pose rests on the arrival",
    "PASS-PLANET §4.4b  · the curl, the world, the horizon, the turn, the crop and the second reach the PICTURE",
    "PASS-PLANET the arriving work rises out of the world's own centre and floods it ring by ring",
    "PASS-PLANET a door the judges' channel spoils is refused on the real road, and the visitor still lands",
    "PASS-PLANET what the host's missing mipmap chain costs this picture, measured",
    "PASS-PLANET row 16 · the captures are kept as evidence",
]

RED_ROWS = [
    "PASS-PLANET red-on-bug · the window forced to a ramp: the exit door stands a curled world",
    "PASS-PLANET red-on-bug · the cut removed: the arriving work never arrives and the exit door is refused",
    "PASS-PLANET red-on-bug · the finish let onto the flat door: both doors part from their own files",
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


def diff_where(p, q, mapping, lo=100, hi=160):
    """The two roads compared over the points the judges' channel says the DEPARTING work owns. The
    map paints that work at half of full red and the arriving one at full, so the band below is the
    departing work's own share of the frame — its picture and the wash that belongs to it."""
    from PIL import Image, ImageChops
    a = Image.open(p).convert("RGB")
    c = Image.open(q).convert("RGB")
    m = Image.open(mapping).convert("RGB")
    if a.size != c.size or a.size != m.size:
        return 255.0, 255.0, 0.0
    red = m.split()[0]
    keep = red.point(lambda v: 255 if lo <= v <= hi else 0)
    d = ImageChops.difference(a, c)
    px, mask = d.load(), keep.load()
    total, worst, n = 0, 0, 0
    for y in range(a.size[1]):
        for x in range(a.size[0]):
            if mask[x, y]:
                r, g, b = px[x, y]
                total += r + g + b
                worst = max(worst, r, g, b)
                n += 1
    if not n:
        return 255.0, 255.0, 0.0
    return total / (3.0 * n), worst, n / float(a.size[0] * a.size[1])


def standing(p):
    from PIL import Image, ImageChops, ImageStat
    a = Image.open(p).convert("RGB")
    flat = Image.new("RGB", a.size, BACKGROUND)
    st = ImageStat.Stat(ImageChops.difference(a, flat))
    own = ImageStat.Stat(a)
    return sum(st.mean) / 3.0, sum(own.stddev) / 3.0


def page_colour(p):
    """The greatest share of the page's own colour standing at any point of the frame, off the
    judges' own blue channel. This is the one reading that could say this instrument's matter is
    absent, and it is what the coverage declaration is measured by."""
    from PIL import Image
    a = Image.open(p).convert("RGB")
    return max(i for i, count in enumerate(a.split()[2].histogram()) if count) / 255.0


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
    """The whole file, cover-fitted into the frame. Both doors of this instrument crop by nothing,
    which is what lab/data/module-contract.json publishes for the module's own two doors and what
    the `framings` block republishes here."""
    from PIL import Image
    return cover_into(Image.open(src).convert("RGB"), w, h, crop)


def apart(p, work):
    from PIL import Image, ImageChops, ImageStat
    a = Image.open(p).convert("RGB")
    if a.size != work.size:
        return 255.0, 255.0
    st = ImageStat.Stat(ImageChops.difference(a, work))
    return sum(st.mean) / 3.0, max(m for _, m in st.extrema)


# THE LAB MODULE AS THE BENCH SERVES IT. Its texture filtering is levelled to the host's and nothing
# else is touched: the host's two source textures are made with a LINEAR minification filter and no
# mipmap chain at all (pass-layer.js:106-118), and an instrument may not upload a texture of its own,
# so a comparison at the module's own filtering would compare two filters rather than two readings of
# one geometry. The file on disk is never touched.
LAB_LEVEL = [
    ("gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR_MIPMAP_LINEAR);",
     "gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);"),
    ("var maxAniso = aniso ? Math.min(4, gl.getParameter(aniso.MAX_TEXTURE_MAX_ANISOTROPY_EXT)) : 0;",
     "var maxAniso = 0;"),
    ("gl.generateMipmap(gl.TEXTURE_2D);", ""),
]


def levelled(text):
    for a, b in LAB_LEVEL:
        if a not in text:
            return None
        text = text.replace(a, b, 1)
    return text


def bench_dir(pack_text=None, lab_text=None):
    """The bench's own served root: the BUILT pass-layer.js, the site's own settings record and the
    BUILT instrument files it names — the real artifacts, namespace applied and comments stripped —
    the lab module with its filtering levelled, the two photographs, and the page that stands the two
    roads of one frame side by side.

    A row proving a rule reds hands over a CHANGED instrument file and writes the record with the
    digest of the bytes actually served, which is what the build does. The source file on disk is
    never touched, so nothing has to be restored and no working tree can be left changed."""
    d = Path(tempfile.mkdtemp(prefix="synth_planetbench_"))
    pack = PACK if pack_text is None else pack_text
    shutil.copy2(TMP / "pass-layer.js", d / "pass-layer.js")
    for _inst in sorted(TMP.glob("pass-inst-*.js")):
        shutil.copy2(_inst, d / _inst.name)
    (d / "pass-inst-planet.js").write_text(pack, encoding="utf-8")
    record = json.loads((TMP / "config.json").read_text(encoding="utf-8"))
    record["pass"]["instruments"]["planet"]["digest"] = hashlib.sha256(
        pack.encode("utf-8")).hexdigest()
    (d / "config.json").write_text(json.dumps(record), encoding="utf-8")
    (d / "planet.js").write_text(LABTXT if lab_text is None else lab_text, encoding="utf-8")
    (d / "photos").mkdir()
    for p in PHOTOS:
        shutil.copy2(p, d / "photos" / p.name)
    shutil.copy2(ROOT / "tests" / "fixture_pass_planet.html", d / "index.html")
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


def roads(br, at, tag, photo=0):
    """BOTH ROADS AT ONE POSE. The dial is the raw hand on both sides: the fixture hands the module
    the same raw window this instrument computes, and each applies the module's own response curve
    once, so handing one number to both is handing them one pose.

    `photo` is which of the two works the MODULE is asked to curl. The module carries one photograph
    and this instrument carries a pair, so at the exit door — where the arriving work stands — the
    module is handed that same work and the two roads are again one geometry over one picture."""
    js(br, "return window.__photo(%d) || 0;" % photo)
    r = js(br, "return window.__both(%r);" % at)
    br.sleep(0.45)
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


def cut_map(br, at, tag):
    js(br, "return window.__both(%r);" % at)
    br.sleep(0.3)
    br.evaluate("window.__mask(1); window.__hostDraw(); 0")
    br.sleep(0.15)
    br.evaluate("window.__show('host'); 0")
    br.sleep(0.25)
    p = png(br, SHOTS / ("map-" + tag + ".png"))
    br.evaluate("window.__mask(0); 0")
    return p


def host_shot(br, at, tag):
    js(br, "return window.__both(%r);" % at)
    br.sleep(0.3)
    br.evaluate("window.__mask(0); window.__hostDraw(); window.__show('host'); 0")
    br.sleep(0.3)
    return png(br, SHOTS / (tag + ".png"))


LAB_LEVELLED = levelled(LABTXT) if LABTXT else None
if LAB_LEVELLED is None and not missing:
    missing = ["the lab module no longer carries the three texture lines this bench levels"]

if not chrome_available():
    for r in BROWSER_ROWS + RED_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
elif missing:
    for r in BROWSER_ROWS + RED_ROWS:
        skip(r, "the lab tree is read-only source material and is absent here: " + missing[0])
else:
    shutil.rmtree(SHOTS, ignore_errors=True)
    SHOTS.mkdir(parents=True, exist_ok=True)
    BENCH = bench_dir(lab_text=LAB_LEVELLED)
    with serve(BENCH) as base:
        with Browser(width=VW, height=VH) as br:
            br.navigate(base + "/index.html")
            if not ready(br):
                for r in BROWSER_ROWS:
                    skip(r, "the bench never came up: "
                         + br.evaluate("JSON.stringify(window.__errs||[])"))
            elif not js(br, "return !!window.__exPass.bench.manifest('planet');"):
                why = js(br, "var e = window.__host.report().events.filter(function(x){"
                             "return x.name === 'manifest-refused';});"
                             "return e.length ? e[e.length - 1].why : null;")
                for r in BROWSER_ROWS:
                    check(r, False, "the host registered no «planet» instrument: " + str(why))
            else:
                SCORE = json.dumps(planet_score())
                SCORE_UNDER = json.dumps(planet_score(under=True))

                # ---- §8: the manifest, read off the registered instrument -----------------------
                m = js(br, "return window.__exPass.bench.manifest('planet');")
                res = m["resources"]
                need = ["id", "api", "arity", "roles", "params", "handles", "neutrals", "doors",
                        "framings", "drivers", "camera", "gl", "passes", "resources",
                        "capabilities", "decline", "provenance", "readiness", "coverage", "levels",
                        "asks"]
                shape = (
                    all(k in m for k in need)
                    and m["id"] == "planet" and m["api"] == 1 and m["arity"] == 2
                    and m["roles"] == ["disassembly", "mystery", "assembly"]
                    and m["levels"] == ["WORLD", "SURFACE"]
                    and sorted(m["params"]) == ["curl", "depth", "dip", "gather", "turn"]
                    and len(m["handles"]) == 9
                    and all(set(h) >= {"min", "max", "def"} for h in m["handles"].values())
                    and m["neutrals"] == {"a": 0, "b": 1}
                    and m["doors"]["in"]["handle"] == "mix" and m["doors"]["in"]["value"] == 0
                    and m["doors"]["out"]["handle"] == "mix" and m["doors"]["out"]["value"] == 1
                    and sorted(m["framings"]) == ["0", "1"]
                    and m["framings"]["0"] == {"coverCrop": 1.0} == m["framings"]["1"]
                    and m["camera"] == {"needs": "none", "authority": "stage"}
                    and m["gl"] == {"preserveDrawingBuffer": False}
                    and len(m["passes"]) == 1 and len(m["passes"][0]["uniforms"]) == 12
                    and sorted(res) == ["lean", "rich", "standard"]
                    and all("bytesEstimate" in res[v] and res[v]["programs"] == 1
                            and res[v]["passes"] == 1 and res[v]["textureSlots"] == 2
                            for v in res)
                    and m["capabilities"] == ["webgl2"] and m["decline"]
                    and m["coverage"]["writes"] is False and m["coverage"]["how"]
                    and m["asks"]["floor"] == 0.2 and m["asks"]["says"]
                    and m["provenance"]["labPath"] == "lab/effects/planet.js"
                    and m["provenance"]["commit"] == "4952bfe"
                    and m["readiness"] == "production-ready"
                    and "planet" in js(br, "return window.__host.report().registered;"))
                check(BROWSER_ROWS[0], shape,
                      f"nine handles, twelve uniforms in one pass, both doors at a cover crop of "
                      f"{m['framings']['0']['coverCrop']} — the module's own contract row publishes "
                      f"exactly that, «the flat end is the plain cover-fit of the same texture "
                      f"unit, so both doors frame the picture alike» — levels {m['levels']}, "
                      f"resources declared for three tiers, a coverage block reading "
                      f"«{m['coverage']['how'][:90]}…» and an `asks` block naming "
                      f"{m['asks']['reads']}")

                w = int(br.evaluate("String(window.__exPass.bench.make() && "
                                    "document.querySelector('canvas[aria-hidden]').width)"))
                h = int(br.evaluate("String(document.querySelector('canvas[aria-hidden]').height)"))
                bufs = js(br, "return window.__buffers();")
                fileA = work_in_the_frame(BENCH / "photos" / PHOTOS[0].name, w, h)
                fileB = work_in_the_frame(BENCH / "photos" / PHOTOS[1].name, w, h)

                # ---- the poses, on both roads ---------------------------------------------------
                # THE FIRST QUARTER is where the whole frame belongs to the departing work — the cut
                # stands under the picture's own foot until the pass is a quarter through — so these
                # are compared point for point. The world opens from nothing to 0.548 across them.
                DOORS = [("door-0", 0.0), ("door-1", 1.0)]
                CURLING = [("c1", 0.06), ("c2", 0.12), ("c3", 0.19), ("c4", 0.25)]
                OPENED = [("w1", 0.35), ("w2", 0.5)]
                shots, reads = {}, {}
                for tag, at in DOORS + CURLING + OPENED:
                    reads[tag], hp, mp = roads(br, at, tag, photo=1 if tag == "door-1" else 0)
                    shots[tag] = (hp, mp)

                for i, (door, own, other, ownn, othern) in enumerate((
                        ("door-0", fileA, fileB, PHOTOS[0].name, PHOTOS[1].name),
                        ("door-1", fileB, fileA, PHOTOS[1].name, PHOTOS[0].name))):
                    a, amx = apart(shots[door][0], own)
                    check(BROWSER_ROWS[1 + i * 2], a <= SEAM,
                          f"{door} against {ownn}, cover-fitted and cropped by nothing: mean "
                          f"{a:.4f} of 255 (threshold {SEAM}), worst channel {amx}. The world opens "
                          f"and shuts on one sine that is exactly nothing at both ends of the pass, "
                          f"and the cut stands past the picture's own rows at both, so a door is "
                          f"the photograph its source carries")
                    o, _ = apart(shots[door][0], other)
                    check(BROWSER_ROWS[2 + i * 2], o >= FAR,
                          f"{door} against {othern}: mean {o:.4f} of 255 (must exceed {FAR})")

                agree = [(t, ) + diff(*shots[t]) for t, _ in DOORS + CURLING]
                # door-1 is read against the module curling the ARRIVING work, which is the same
                # geometry over the other picture; every other pose is read against the departing one
                check(BROWSER_ROWS[5],
                      all(mn <= ROADS for _, mn, _ in agree)
                      and bufs["host"] == bufs["module"],
                      "; ".join(f"{t}: mean {mn:.4f} of 255 (bar {ROADS}), worst channel {mx}"
                                for t, mn, mx in agree)
                      + f". Both roads drew on a {bufs['host']} buffer, so one sampler ran through "
                        f"one rasteriser on both sides and what is left between them is arithmetic: "
                        f"this port packs the module's fourteen loose scalars four to a carrier, "
                        f"because the host binds four uniform types, and turns the row coordinate "
                        f"over once because the host uploads its textures unflipped. The module is "
                        f"served with its texture filtering levelled to the host's and nothing else "
                        f"changed")

                masked = []
                for tag, at in OPENED:
                    mp = cut_map(br, at, tag)
                    masked.append((tag, at) + diff_where(shots[tag][0], shots[tag][1], mp))
                check(BROWSER_ROWS[6],
                      all(mn <= ROADS for _, _, mn, _, _ in masked)
                      and all(share > 0.2 for _, _, _, _, share in masked),
                      "; ".join(f"at {at} the departing work owns {share * 100:.1f}% of the frame "
                                f"and the two roads stand {mn:.4f} of 255 apart over it, worst "
                                f"channel {mx}"
                                for _, at, mn, mx, share in masked)
                      + f" (bar {ROADS}). Past the first quarter the arriving work owns part of the "
                        f"world and the module has nothing to say about those points, so the "
                        f"comparison is masked to the points the judges' channel says the departing "
                        f"work still owns — which at the world's full opening is the whole geometry "
                        f"the module draws, read at world 1")

                # ---- the dial blends the coordinate, not the colour ------------------------------
                # lab/data/module-contract.json's own note on this module: blending two finished
                # colours makes the middle of the handle the average of its ends, which is a ghost —
                # two superimposed copies of one work. Measured there by lab/step5-dials-check.py as
                # 0.2506 for the colour blend against 25.9157 for the coordinate blend. The same
                # measurement here, on this instrument's own first quarter, where one work stands.
                half = host_shot(br, 0.125, "dial-middle")
                ends = host_shot(br, 0.0, "dial-end-0"), host_shot(br, 0.25, "dial-end-1")

                def average_of(p, q):
                    from PIL import Image, ImageChops
                    return ImageChops.blend(Image.open(p).convert("RGB"),
                                            Image.open(q).convert("RGB"), 0.5)
                avg = SHOTS / "dial-average.png"
                average_of(*ends).save(avg)
                ghost, ghost_max = diff(half, avg)
                check(BROWSER_ROWS[7], ghost > SEAM,
                      f"at the middle of the first quarter the frame stands {ghost:.4f} of 255 from "
                      f"the average of that quarter's two ends, worst channel {ghost_max}. A dial "
                      f"that blended two finished colours would read near nothing there, because "
                      f"the middle WOULD BE that average; this one mixes the sample coordinate each "
                      f"fetch reads, so the frame is one picture in sharp focus at every value of "
                      f"the handle. The module's own check reads 0.2506 for the colour blend "
                      f"against 25.9157 for the coordinate blend (module-contract.json, law 14)")

                # ---- §7: the frame is filled, read off the judges' own blue channel ---------------
                fills = []
                for tag, at in DOORS + CURLING + OPENED:
                    fills.append((tag, page_colour(cut_map(br, at, tag))))
                check(BROWSER_ROWS[8], all(s < 0.9 for _, s in fills),
                      "; ".join(f"{t}: at worst {s * 100:.1f}% of the page's own colour at any "
                                f"point" for t, s in fills)
                      + ". The judges' channel paints how much of the page's own colour stands at "
                        "each point of the frame, which is the one reading that could ever say this "
                        "instrument's matter is absent. Outside the world's rim the frame carries "
                        "the sky of the work that owns the world, smeared and dimmed, and the reach "
                        "of that wash is read off the frame's own farthest corner, so no point of "
                        "any stage is ever left to the page")
                br.evaluate("window.__mask(0); window.__show('host'); 0")

                # ---- §7: the placement its declaration buys --------------------------------------
                place = js(br, """
                  var b = window.__exPass.bench;
                  return {declared: b.coverageOf('planet'),
                          asGround: b.coverageWhyNo([
                            {id: 'ground', instrument: {id: 'planet', api: 1}, stack: 0},
                            {id: 'over', instrument: {id: 'matter', api: 1}, stack: 1}]),
                          asRoof: b.coverageWhyNo([
                            {id: 'floor', instrument: {id: 'weave', api: 1}, stack: 0},
                            {id: 'ground', instrument: {id: 'planet', api: 1}, stack: 1}])};
                """)
                took_stack = js(br, "return window.__offer(%s, {clock: 1.5, progress: 0.3});"
                                % SCORE_UNDER)
                br.sleep(0.4)
                br.evaluate("window.__cancel('placement row'); 0")
                idle(br)
                check(BROWSER_ROWS[9],
                      place["declared"] and place["declared"]["writes"] is False
                      and place["asGround"] is None
                      and isinstance(place["asRoof"], str) and "«planet»" in place["asRoof"]
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
                        (0.0, fileA, "%s, seated by this instrument at 1.0" % PHOTOS[0].name),
                        (1.0, work_in_the_frame(BENCH / "photos" / PHOTOS[1].name, w, h, over_crop),
                         "%s under the arriving voice's own crop of %s"
                         % (PHOTOS[1].name, over_crop))):
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
                      + ". A ground has to close its own frame at both ends or the cleared buffer "
                        "shows through the door the visitor lands on")

                # ---- §7: no empty frame ----------------------------------------------------------
                empties = []
                for at in (0.0, 0.15, 0.3, 0.5, 0.7, 0.85, 1.0):
                    js(br, "return window.__offer(%s, {clock: 1.5, progress: %r});" % (SCORE, at))
                    br.sleep(0.5)
                    p = png(br, SHOTS / ("instant-%03d.png" % round(at * 100)))
                    empties.append((at, ) + standing(p))
                    br.evaluate("window.__cancel('instant sweep'); 0")
                    idle(br)
                check(BROWSER_ROWS[11],
                      all(d >= FAR and s >= SPREAD for _, d, s in empties),
                      "; ".join(f"at {at}: {d:.2f} from the background, spread {s:.2f}"
                                for at, d, s in empties)
                      + f" (bars: {FAR} and {SPREAD}); sampled on the one-cue score, where this "
                        f"instrument is the whole frame")

                js(br, "return window.__offer(%s, {clock: 1.5, progress: 0.3});" % SCORE)
                br.sleep(0.5)
                br.set_viewport(VW - 80, VH - 120)
                br.sleep(0.6)
                p = png(br, SHOTS / "after-resize.png")
                sized = js(br, "return {w: document.querySelector('canvas[aria-hidden]').width, "
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
                      f"spread of {s:.2f}; the context keeps preserveDrawingBuffer={sized['pdb']}. "
                      f"The world's own scale is the frame's own two half-extents and the wash's "
                      f"reach is read off the frame's farthest corner, so the whole world is "
                      f"rebuilt at the new ratio rather than re-shown")

                # ---- the driven repeat -----------------------------------------------------------
                br.sleep(0.6)
                took = js(br, "return window.__offer(%s, {clock: 1.5, progress: 0.3});" % SCORE)
                br.sleep(1.2)
                first = png(br, SHOTS / "driven-1.png")
                rep1 = js(br, "return window.__report();")
                br.evaluate("window.__cancel('between runs'); 0")
                idle(br)
                js(br, "return window.__offer(%s, {clock: 1.5, progress: 0.3});" % SCORE)
                br.sleep(1.2)
                second = png(br, SHOTS / "driven-2.png")
                mn, mx = diff(first, second)
                check(BROWSER_ROWS[13], took["took"] and mn == 0.0 and mx == 0,
                      f"took={took['took']} two runs of one score at one pinned second: mean {mn} "
                      f"worst channel {mx}. Every number the shader reads comes from a handle, and "
                      f"the module's own two motions — the world's slow turn and the breath of the "
                      f"curl — ride the score's second rather than a clock of the instrument's own")

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
                      f"after ten runs={after['textures']}/{after['programs']}/"
                      f"{after['framebuffers']} (textures/programmes/framebuffers)")

                errs = json.loads(br.evaluate("JSON.stringify(window.__errs||[])"))
                check(BROWSER_ROWS[15], not errs, "; ".join(errs)[:300])

                # THE CENSUS IS READ ON A BENCH OF ITS OWN, and the reason is the programme cache:
                # it holds one entry per branch and outlives every transaction, so a session that has
                # already drawn another instrument grants two programmes to a score declaring one.
                r = on_bench(lambda b2: (
                    js(b2, "return window.__offer(%s, {clock: 1.0, progress: 0.4});" % SCORE),
                    b2.sleep(0.8),
                    js(b2, "return window.__report();")["resources"])[-1],
                    lab_text=LAB_LEVELLED)
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
                      f"census={cen}; the module's own canvas, its second context, its two textures "
                      f"with their mipmap chains and its own frame loop are what this port does "
                      f"without")
                br.evaluate("window.__cancel('census row'); 0")
                idle(br)

                r = js(br, """
                  var m = window.__exPass.bench.manifest('planet');
                  var plain = window.__exPass.bench.es3(m.passes[0].frag, false);
                  var already = window.__exPass.bench.es3('#version 300 es\\n' + m.passes[0].frag, false);
                  var count = function (s) { return s.split('#version').length - 1; };
                  return {source: count(m.passes[0].frag), stamped: count(plain),
                          untouched: count(already), head: plain.slice(0, 15),
                          out: plain.indexOf('out vec4 oColour;') >= 0,
                          grad: plain.indexOf('textureGrad') >= 0};
                """)
                check(BROWSER_ROWS[18],
                      r["source"] == 0 and r["stamped"] == 1 and r["untouched"] == 1
                      and r["head"].startswith("#version 300 es") and r["out"] and r["grad"],
                      f"the shader carries {r['source']} headers, the translator leaves it with "
                      f"{r['stamped']} and declares the output the host's coverage law reads "
                      f"({r['out']}), and a source that already carries a header comes back with "
                      f"{r['untouched']}. The module's own two filtered fetches survive the "
                      f"translation untouched ({r['grad']}), because what is compiled is the second "
                      f"version of the language either way")

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
                      f"handoffs={cam['handoffs']} tolerances={cam['tol']} — the world is drawn "
                      f"inside this instrument's own pass and it asks the host's camera for "
                      f"nothing, so the stage holds it for the whole pass")

                # ---- §4.4b: the handles reach the picture ----------------------------------------
                # READ AT THE MIDDLE OF THE PASS, where the world stands whole and every one of these
                # handles has somewhere to show.
                shot = {}
                for name, extra in (("base", {}), ("curl", {"curl": 0.35}),
                                    ("depth", {"depth": 1}), ("dip", {"dip": 0.0}),
                                    ("turn", {"turn": 0.9}), ("gather", {"gather": 0.2}),
                                    ("shade", {"shade": 0.0}), ("clock", {"clock": 9.0})):
                    js(br, "return window.__offer(%s, {clock: 1.5, progress: 0.5});"
                       % json.dumps(planet_score(**extra)))
                    br.sleep(0.7)
                    shot[name] = png(br, SHOTS / ("handle-" + name + ".png"))
                    br.evaluate("window.__cancel('handle row'); 0")
                    idle(br)
                moved = {k: diff(shot["base"], shot[k])
                         for k in ("curl", "depth", "dip", "turn", "gather", "shade", "clock")}
                check(BROWSER_ROWS[21],
                      all(mn > SEAM for mn, _ in moved.values()),
                      "; ".join(f"{k} moves the frame by {mn:.4f} of 255, worst channel {mx}"
                                for k, (mn, mx) in moved.items())
                      + f" (floor {SEAM}). A handle a score drives and the picture ignores is what "
                        f"§4.4b is about")

                # ---- THE CROSSING ITSELF ---------------------------------------------------------
                # The arriving work rises out of the world's own centre. Read three ways: it owns
                # nothing of the frame through the first quarter, it owns part of the world in the
                # middle, and it owns all of it by the last — and where it stands is a disc about the
                # centre and not a fade over the whole frame.
                def owned(p):
                    """The share of the frame the judges' channel gives the arriving work."""
                    from PIL import Image
                    a = Image.open(p).convert("RGB")
                    red = a.split()[0].histogram()
                    hot = sum(red[200:])
                    return hot / float(a.size[0] * a.size[1])
                rise = [(at, owned(cut_map(br, at, "rise-%03d" % round(at * 100))))
                        for at in (0.0, 0.25, 0.4, 0.5, 0.6, 0.75, 1.0)]
                shares = [s for _, s in rise]
                check(BROWSER_ROWS[22],
                      shares[0] < 0.001 and shares[1] < 0.001 and shares[-1] > 0.999
                      and shares[-2] > 0.999
                      and all(b >= a - 0.001 for a, b in zip(shares, shares[1:]))
                      and 0.05 < shares[3] < 0.95,
                      "; ".join(f"at {at}: the arriving work owns {s * 100:.1f}% of the frame"
                                for at, s in rise)
                      + ". It owns nothing through the first quarter, rises out of the world's own "
                        "centre through the middle half — which is the charter's own «B enters "
                        "through the singular locus» — and owns the whole frame from the last "
                        "quarter on. The share never goes backwards, so the handover is one "
                        "continuous travel of a single row of the photograph and never a cut")

                # ---- THE DOOR REFUSED ON THE REAL TRANSACTION ROAD -------------------------------
                def road(gen):
                    return js(br, "var r = window.__report(); return {state: r.state, "
                                  "drew: r.drew, buffer: r.census.buffer, "
                                  "applied: r.applied || null, "
                                  "refused: r.events.filter(function(e){ return e.gen === %d "
                                  "&& e.why && String(e.why).indexOf('door leaks') >= 0; })"
                                  ".map(function(e){ return e.name + ': ' + e.why; })};" % gen)

                br.evaluate("window.__cancel('door road row'); 0")
                idle(br)
                shut_gen = js(br, "return window.__offer(%s, {clock: 0, progress: 0});"
                              % json.dumps(planet_score(mask=0)))["gen"]
                br.sleep(1.0)
                played = road(shut_gen)
                br.evaluate("window.__cancel('door road row'); 0")
                idle(br)
                open_gen = js(br, "return window.__offer(%s, {clock: 0, progress: 0});"
                              % json.dumps(planet_score(mask=1)))["gen"]
                br.sleep(1.1)
                leaked = road(open_gen)
                br.evaluate("window.__cancel('door road row'); 0")
                idle(br)
                check(BROWSER_ROWS[23],
                      played["state"] == "running" and played["drew"] == 1
                      and not played["refused"]
                      and len(leaked["refused"]) == 1 and leaked["state"] == "idle"
                      and leaked["drew"] == 0
                      and "the entry door leaks" in leaked["refused"][0]
                      and "the judges' own channel" in leaked["refused"][0]
                      and ("%s buffer" % played["buffer"].replace("x", " x ")) in leaked["refused"][0],
                      "on the %s buffer the host drew, the judges' channel shut draws the door (%d "
                      "cue, state %s, refused %s); left open it is refused with «%s», on which the "
                      "host lands the transaction (state %s, %d cue drawn) and the walk's own glide "
                      "carries the visitor"
                      % (played["buffer"], played["drew"], played["state"],
                         played["refused"] or "nothing",
                         (leaked["refused"] or ["nothing refused"])[0], leaked["state"],
                         leaked["drew"]))

    shutil.rmtree(BENCH, ignore_errors=True)

    # ---- WHAT THE HOST'S MISSING MIPMAP CHAIN COSTS ----------------------------------------------
    # A reading and never a gate. The module uploads its own textures with a mipmap chain and
    # anisotropic filtering; the host's two source textures carry neither and an instrument may not
    # upload a texture of its own. So the same module is served twice — once as it stands and once
    # levelled to the host — and the difference between the two frames is what the host owes this
    # picture. Both are the MODULE, so nothing about this port is under test here.
    def module_shot(br, at, tag):
        js(br, "return window.__both(%r);" % at)
        br.sleep(0.4)
        br.evaluate("window.__show('module'); 0")
        br.sleep(0.45)
        return png(br, SHOTS / (tag + ".png"))

    with_chain = on_bench(lambda b: [module_shot(b, at, "chain-on-%03d" % round(at * 100))
                                     for at in (0.12, 0.25)], lab_text=LABTXT)
    without = on_bench(lambda b: [module_shot(b, at, "chain-off-%03d" % round(at * 100))
                                  for at in (0.12, 0.25)], lab_text=LAB_LEVELLED)
    if with_chain and without:
        cost = [diff(a, b) for a, b in zip(with_chain, without)]
        check(BROWSER_ROWS[24], True,
              "; ".join(f"at {at}: mean {mn:.4f} of 255, worst channel {mx}"
                        for at, (mn, mx) in zip((0.12, 0.25), cost))
              + ". That is the module against ITSELF with the chain taken off, so it is what the "
                "host's two source textures owe this picture and nothing about this port: one "
                "`generateMipmap` per upload and a minification filter to match "
                "(pass-layer.js:106-118, :434-445). The shader keeps the module's own two filtered "
                "fetches exactly as the module wrote them, so the day the host hands a chain this "
                "picture gains the module's own filtering with no edit here")
    else:
        skip(BROWSER_ROWS[24], "the bench never came up for the two-filter reading")

    kept = sorted(p.name for p in SHOTS.glob("*.png"))
    check(BROWSER_ROWS[25],
          len(kept) >= 40 and all((SHOTS / k).stat().st_size > 1000 for k in kept),
          f"{len(kept)} captures under {SHOTS.relative_to(ROOT)}: the eight poses on both roads, "
          f"their cut maps, the dial's own three readings, the two doors in a stack, the seven "
          f"sampled instants, the frame after a resize, the two driven runs, the eight handle runs, "
          f"the seven readings of the arriving work rising and the two filterings of the module")

    # ---- the red-on-bug rows -----------------------------------------------------------------
    # Each serves a CHANGED copy of the instrument to the browser with one rule reverted, and reads
    # the same number the rule was landed on.
    def door_gap(br, at, src):
        """One pose photographed and measured against the file the door names, cover-fitted into the
        buffer the host actually drew on — read off the canvas rather than assumed."""
        p = host_shot(br, at, "red-door-%03d" % round(at * 100))
        gw = int(br.evaluate("String(document.querySelector('canvas[aria-hidden]').width)"))
        gh = int(br.evaluate("String(document.querySelector('canvas[aria-hidden]').height)"))
        return apart(p, work_in_the_frame(src, gw, gh))

    def door_refusal(br, score):
        br.evaluate("window.__cancel('red row'); 0")
        idle(br)
        gen = js(br, "return window.__offer(%s, {clock: 0, progress: 1});" % score)["gen"]
        br.sleep(1.1)
        out = js(br, "var r = window.__report(); return {state: r.state, drew: r.drew, "
                     "refused: r.events.filter(function(e){ return e.gen === %d && e.why "
                     "&& String(e.why).indexOf('door leaks') >= 0; })"
                     ".map(function(e){ return e.why; })};" % gen)
        br.evaluate("window.__cancel('red row'); 0")
        idle(br)
        return out

    if chrome_available() and not missing:
        SCORE = json.dumps(planet_score())
        base = on_bench(lambda b: (door_gap(b, 1.0, PHOTOS[1]),
                                   door_refusal(b, SCORE)), lab_text=LAB_LEVELLED)

        # ---- 1. the window forced to a ramp ------------------------------------------------------
        bug = PACK.replace("function worldOf(dial) { return feel(windowOf(dial)); }",
                           "function worldOf(dial) { return feel(clamp01(dial)); }", 1)
        r1 = on_bench(lambda b: (door_gap(b, 1.0, PHOTOS[1]),
                                 door_refusal(b, SCORE)),
                      pack_text=bug, lab_text=LAB_LEVELLED)
        check(RED_ROWS[0],
              bug != PACK and base is not None and r1 is not None
              and base[0][0] <= SEAM and not base[1]["refused"]
              and r1[0][0] > SEAM and len(r1[1]["refused"]) == 1
              and "the world stands" in r1[1]["refused"][0],
              f"«flat → world → flat» is the charter's own shape for a projection world, and here "
              f"it is one sine over the pass, nothing at both ends. Forced to a straight ramp the "
              f"exit door stands a fully curled world: the frame goes from {base[0][0]:.4f} of 255 "
              f"from its own file to {r1[0][0]:.4f} (threshold {SEAM}), and the instrument's own "
              f"door reading refuses it — «{(r1[1]['refused'] or ['nothing'])[0][:140]}…»")

        # ---- 2. the cut removed ------------------------------------------------------------------
        bug = PACK.replace("float cov = clamp(0.5 + (uCut.x - row) / foot, 0.0, 1.0);",
                           "float cov = 0.0;", 1)
        r2 = on_bench(lambda b: (door_gap(b, 1.0, PHOTOS[1]),
                                 door_gap(b, 0.5, PHOTOS[1])),
                      pack_text=bug, lab_text=LAB_LEVELLED)
        check(RED_ROWS[1],
              bug != PACK and base is not None and r2 is not None
              and base[0][0] <= SEAM and r2[0][0] >= FAR,
              f"the cut is the whole crossing: one row of the photograph, travelling from under the "
              f"picture's foot to over its sky, with the arriving work below it. Removed, the "
              f"arriving work never arrives and the exit door stands the DEPARTING one — "
              f"{r2[0][0]:.4f} of 255 from the file the door names, against {base[0][0]:.4f} with "
              f"the cut standing and a bar of {FAR} for «a different work altogether»")

        # ---- 3. the finish let onto the flat door ------------------------------------------------
        bug = PACK.replace("float fin = uWorld * uShade;", "float fin = uShade;", 1)
        r3 = on_bench(lambda b: (door_gap(b, 0.0, PHOTOS[0]),
                                 door_gap(b, 1.0, PHOTOS[1])),
                      pack_text=bug, lab_text=LAB_LEVELLED)
        check(RED_ROWS[2],
              bug != PACK and base is not None and r3 is not None
              and base[0][0] <= SEAM and r3[0][0] > SEAM and r3[1][0] > SEAM,
              f"«at dial 0 every finishing term that has no meaning on a flat photograph — shading, "
              f"light, the wedge's own coverage weight, the closing gamma — stands at its own "
              f"identity» is the module's own contract row for its flat door. Let onto the door, "
              f"the entry stands {r3[0][0]:.4f} of 255 from its own file and the exit "
              f"{r3[1][0]:.4f}, against {base[0][0]:.4f} with the gate standing and a threshold of "
              f"{SEAM}")

shutil.rmtree(TMP, ignore_errors=True)

ran = {name for name, _, _ in results}
for name in BROWSER_ROWS + RED_ROWS + NODE_ROWS:
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
