#!/usr/bin/env python3
"""PASS-API-V1 — the box instrument on the host's frame.
Run: python3 tests/test_pass_boxfold.py

Root: the composer's own census. The box-fold road qualifies on the measurements for 4 670 ordered
pairs and plays for none of them, because `INSTRUMENT_OF_KIND.panel` in engine/assets/pass-composer.js
names no instrument at all and every one of those plans is declined for want of one — its own
`MISSING_INSTRUMENT` entry reads «an instrument that cuts on panels, for region_dissolve and
object_reveal». docs/design/PASS-API-V1.md §7 (GPU and resources), §8 (the manifest) and §9's
conformance rows 7, 9, 10, 13, 14, 15, 16 and 22 are what this file makes real, together with §7's
coverage law of 12:40. The lifecycle rows stay in tests/test_pass_api.py and are untouched.

THE FIVE CONDITIONS THE BOX IS PARDONED UNDER, and where each is measured here.

  lab/CROSSING-BRIEF.md convicts «the screen-as-cube-face turn» by name and returns the box to the
  keeper list in the same breath, under five conditions. The rows below measure the three the
  instrument answers whole and the one it answers with the composer; the fifth — faces carrying live
  pictures re-read every drawn frame — is the host's, and what is measured of it here is that this
  instrument caches no face and holds no texture of its own.

    · the fold on the departing work's own measured region line — «the crease, and whose number it
      is» below: with the crease on the work's line and with it back on the box's own edge, read
      mid-turn and read at the door;
    · a contact shadow on every edge — the handle rows, and the red-on-bug that takes it out;
    · the camera travelling with true perspective — the two-roads rows, which stand this port's
      inverted projection beside the module's own;
    · landing exactly — the door rows, and the box's own reading walked on the drawing buffer.

WHAT IS COMPARED, AND AGAINST WHAT.

  The doors. At the dial's two ends one whole work stands. Each is measured against ITS OWN FILE,
  cover-fitted into the frame and centre-cropped by the box's own crop — the frame is a window cut out
  of the middle of a bigger box, and that price is what the manifest's `framings` block publishes —
  inside the project's seam threshold of 6 of 255.

  THE TWO ROADS. Both draw with WebGL: the module carries its own context and its own fragment shader,
  so one sampler runs through one rasteriser on both sides and the residual between them is a
  difference of arithmetic rather than of samplers. The bar is therefore the project's own seam
  threshold and not one this suite invented. THE LAB MODULE IS SERVED WITH ONE LITERAL CHANGED and the
  row that reads it says so: its crop is levelled to the port's own, because the port grows the box by
  the room the crease's travel needs and the module never did — comparing at the module's crop would
  compare two differently sized boxes rather than two readings of one geometry.

  The coverage. This instrument declares that it writes none, because it fills the frame. That is
  measured rather than declared: the face map — the port's own judges' frame, which paints which face
  stands at each point of the frame — is read at every sampled pose and holds no unclaimed point. The
  placement it buys is read off the host's own `coverageWhyNo`.

  No empty frame. The rows below sample the pass at seven instants and once across a change of
  viewport, and each frame has to stand as a picture.

  The lab module is READ ONLY. Absent, every browser row here is a pinned SKIP that names the missing
  path — never a silent pass.
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

# The lab module and the two photographs stand in the MAIN tlvphotos worktree, which is where the
# suites of the ports before this one read them from too.
LAB = Path(os.environ.get("TLVPHOTOS_ROOT", "/Users/sashaabramovich/tlvphotos")) / "lab"
PHOTOS = [LAB / "photos" / "glassgrid.jpg", LAB / "photos" / "towers.jpg"]
MODULE = LAB / "effects" / "box.js"

SITE_URL = "https://synth.example.com"
VW, VH = 390, 844          # the phone frame lab/carrier-check.py measures on
SEAM = 6.0                 # the project's seam threshold, 6 of 255 (TRANSITION-STAGE-V0 §1)
FAR = 40.0                 # further than this from a file and it is a different work
BACKGROUND = (0x08, 0x08, 0x0a)
SPREAD = 10.0

# THE TWO ROADS' BAR. Both roads run one fragment shader over one rasteriser, so nothing but
# arithmetic stands between them: this port hands the shader each face's four screen corners where
# the module handed it four lines, and hands each inverse map as its three rows where the module
# handed a matrix. Neither changes a number. The bar is the project's own seam threshold of 6 of 255,
# and the readings stand in the evidence beside it. What makes it mean anything is the red-on-bug
# set: each proof reverts one rule this port states and moves the same number by a wide multiple.
ROADS = SEAM

# The box's own crop, and the two rooms it is made of: the room the turn needs, which is the module's
# own measured number, and the room the crease's travel onto the work's region line needs, which is
# this port's. A landed face stands the source cover-fit centre-cropped by their sum.
TURN_ROOM = 1.48
SEAM_ROOM = 0.42
CROP = TURN_ROOM + SEAM_ROOM

# The place the departing work's own region line stands at, and how much of the difference between
# its columns that split explains. Both are read off the work by lab/cut-lines.py; the numbers used
# here are the ones the module's own judged run measured on these two photographs
# (lab/data/effects-new-check.txt, «the fold on the work's seam»).
SEAM_AT = 0.599
SEAM_SCORE = 0.269

SHOTS = ROOT / "tests" / "captures" / "pass-boxfold"

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


# ================================================================================================
# PARDON CONDITION (i), REAL DATA — «the fold on the departing work's own measured region line».
#
# Everything above and below this block proves the INSTRUMENT's own three conditions by feeding it
# hand-typed handle values (`SEAM_AT`/`SEAM_SCORE`, the module's own judged-run numbers) through the
# browser fixture — real proof that the handle READS an outside measurement, never a frame constant,
# but no proof that the COMPOSER, given a real WorkRecord, ever actually HANDS it one. The
# 2026-08-19 audit found that second half unearned: the region-line reading was stripped before
# records reached the engine, and `pass-composer.js` handed `boxfold` a written zero on every cast —
# an un-pardoned instrument playing under a pardon nobody was still owed. It is now genuinely
# repaired (`pass-composer.js`'s own `wanted.seam`/`wanted.seamScore`, read off
# `structure.regions.line.{x,y}.{at,explains}`) but nothing asserted it: this section does.
#
# THE SEARCH IS OVER THE REAL 121-WORK FLEET, NEVER A HAND-PICKED PAIR (the standing rule this
# project holds every phase to). For each departing work in the fixture's own order, the real,
# exposed `genresFor` cheaply ranks every arriving work for a box-fold fit before the far more
# expensive full `passageFor` is ever called on the survivors — the same two-phase economy
# `dump_route_wire_fence.py` uses for its own 27-instrument hunt. `routeRole`/`routeFunction` travel
# on every request exactly as a live route step supplies them (a route step's own station always
# states both together, `engine/client/01a-pass.js:2010-2011`), restricted here to the roles shelf
# 17 actually grants a miracle — box-fold cannot be cast at all under a role with none. `cameraState`
# is left at its cold-visit `null`: `pass-composer.js` reads it onto the diagnostic echo alone
# (`grep cameraState engine/assets/pass-composer.js`) and touches no legality or handle decision
# with it, so a DOM-derived pose has nothing to add to a search over what the COMPOSER hands the
# instrument.
PARDON_I_COMPOSER = ROOT / "engine" / "assets" / "pass-composer.js"
PARDON_I_FIXTURE_COMPOSED = ROOT / "tests" / "fixture_pass_composed.json"
PARDON_I_FIXTURE_WORKS = ROOT / "tests" / "fixture_pass_works.json"
PARDON_I_SEAM_FLOOR = 0.20  # pass-inst-boxfold.js's own SEAM_FLOOR — the module's own gate

PARDON_I_ROW = ("PASS-BOXFOLD pardon (i) · a real, planner-composed pair hands the instrument a "
                "non-zero, above-floor seamScore reading off the departing work's own region line")
PARDON_I_RED_ROW = ("PASS-BOXFOLD pardon (i) red-on-bug · restoring the written zero drops the "
                     "same real pair's own seamScore back to it")

PARDON_I_DRIVER = r"""
"use strict";
const vm = require("vm");
const source = %(source)s;
const consts = %(consts)s;
const works = %(works)s;
const plants = %(plants)s;

let patched = source;
const missed = [];
for (const [from, to] of plants) {
  if (patched.indexOf(from) < 0) { missed.push(from); continue; }
  patched = patched.split(from).join(to);
}
if (missed.length) { console.log(JSON.stringify({missed: missed})); process.exit(0); }

let joined = null;
const sandbox = { window: { __PassComposer: (m) => { joined = m; } }, console: console };
vm.createContext(sandbox);
try {
  vm.runInContext(patched, sandbox, { filename: "pass-composer.js" });
} catch (e) {
  console.log(JSON.stringify({ error: String((e && e.stack) || e) }));
  process.exit(0);
}
if (!joined) { console.log(JSON.stringify({ error: "the module joined nothing" })); process.exit(0); }
const composer = joined.make(consts);

const ids = Object.keys(works);
// Only the two roles shelf 17 grants a miracle to — box-fold cannot be cast under any other.
const ROLE_FN = [["culmination", "dominant"], ["middle", "subdominant"], ["middle", "dominant"]];
const SEEDS = [0, 2, 4, 6];

let found = null;
outer:
for (let i = 0; i < ids.length && !found; i++) {
  const from = ids[i];
  // PHASE A, CHEAP: rank every arriving work for a box-fold fit before the expensive call below.
  const candidates = [];
  for (let j = 0; j < ids.length; j++) {
    if (i === j) continue;
    let g;
    try { g = composer.genresFor(works[from], works[ids[j]]); } catch (e) { continue; }
    const bf = (g.genres || []).filter((x) => x.id === "box-fold")[0];
    if (bf && bf.fit > 0) candidates.push(ids[j]);
  }
  // PHASE B: only the survivors of phase A ever reach the real, full planner.
  for (let ci = 0; ci < candidates.length && !found; ci++) {
    const to = candidates[ci];
    for (const [role, fn] of ROLE_FN) {
      for (const seed of SEEDS) {
        const req = { workRecordA: works[from], workRecordB: works[to], direction: "a-to-b",
                      seed: seed, routeRole: role, routeFunction: fn, cameraState: null,
                      walkMemory: [], walkGenres: [], walkMiracles: [], framePace: null };
        let made;
        try { made = composer.passageFor(req); } catch (e) { continue; }
        if (!made || made.declined || !made.plan) continue;
        const cues = made.plan.cues || [];
        const box = cues.filter((c) => c.instrument.id === "boxfold")[0];
        if (!box) continue;
        const mh = box.measuredHandles || {};
        const seamScore = mh.seamScore && mh.seamScore.v;
        const seamAt = mh.seam && mh.seam.v;
        if (typeof seamScore === "number") {
          found = { from: from, to: to, seed: seed, role: role, fn: fn,
                    seamAt: seamAt, seamScore: seamScore };
          break outer;
        }
      }
    }
  }
}
console.log(JSON.stringify({ found: found }));
"""


def _pardon_i_node_available():
    return shutil.which("node") is not None


if not _pardon_i_node_available():
    skip(PARDON_I_ROW, "node is not on this machine")
    skip(PARDON_I_RED_ROW, "node is not on this machine")
elif not (PARDON_I_COMPOSER.exists() and PARDON_I_FIXTURE_COMPOSED.exists()
          and PARDON_I_FIXTURE_WORKS.exists()):
    skip(PARDON_I_ROW, "the composer or its fixtures are not on this machine")
    skip(PARDON_I_RED_ROW, "no real pair to replant")
else:
    _pardon_i_source = PARDON_I_COMPOSER.read_text(encoding="utf-8").replace("@@NS@@", "")
    _pardon_i_fix_composed = json.loads(PARDON_I_FIXTURE_COMPOSED.read_text(encoding="utf-8"))
    _pardon_i_fix_works = json.loads(PARDON_I_FIXTURE_WORKS.read_text(encoding="utf-8"))
    _pardon_i_tmp = Path(tempfile.mkdtemp(prefix="pass_boxfold_pardon_"))

    def _run_pardon_i(plants=None):
        driver_text = PARDON_I_DRIVER % {
            "source": json.dumps(_pardon_i_source),
            "consts": json.dumps(_pardon_i_fix_composed["consts"]),
            "works": json.dumps(_pardon_i_fix_works["works"]),
            "plants": json.dumps(plants or []),
        }
        driver_path = _pardon_i_tmp / "driver.js"
        driver_path.write_text(driver_text, encoding="utf-8")
        proc = subprocess.run(["node", str(driver_path)], capture_output=True, text=True,
                              timeout=120)
        if proc.returncode != 0:
            return {"error": (proc.stderr or "").strip()[-1200:]}
        lines = (proc.stdout or "").strip().splitlines()
        if not lines:
            return {"error": "the driver said nothing"}
        return json.loads(lines[-1])

    _pardon_i_green = _run_pardon_i()
    _pardon_i_found = (_pardon_i_green.get("found")
                       if isinstance(_pardon_i_green, dict) else None)
    check(PARDON_I_ROW,
          isinstance(_pardon_i_found, dict)
          and isinstance(_pardon_i_found.get("seamScore"), (int, float))
          and _pardon_i_found["seamScore"] >= PARDON_I_SEAM_FLOOR,
          ("real pair %s→%s (seed %s, role %s/%s): seam=%s seamScore=%s against the module's own "
           "floor of %s"
           % (_pardon_i_found.get("from"), _pardon_i_found.get("to"), _pardon_i_found.get("seed"),
              _pardon_i_found.get("role"), _pardon_i_found.get("fn"), _pardon_i_found.get("seamAt"),
              _pardon_i_found.get("seamScore"), PARDON_I_SEAM_FLOOR)
           if isinstance(_pardon_i_found, dict) else
           "the real 121-work fleet's own genresFor/passageFor search cast box-fold on no real "
           "pair at all: " + json.dumps(_pardon_i_green)))

    if not isinstance(_pardon_i_found, dict):
        skip(PARDON_I_RED_ROW, "no real pair found above to replant")
    else:
        _pardon_i_plant = [[
            "wanted.seamScore = flt(r4(clamp01(seamHow)));",
            "wanted.seamScore = flt(0);",
        ]]
        _pardon_i_red = _run_pardon_i(plants=_pardon_i_plant)
        if _pardon_i_red.get("missed"):
            skip(PARDON_I_RED_ROW, "the line this plant names is not in the shipped source")
        else:
            _pardon_i_red_found = (_pardon_i_red.get("found")
                                   if isinstance(_pardon_i_red, dict) else None)
            _pardon_i_same_pair = (
                isinstance(_pardon_i_red_found, dict)
                and _pardon_i_red_found.get("from") == _pardon_i_found.get("from")
                and _pardon_i_red_found.get("to") == _pardon_i_found.get("to")
                and _pardon_i_red_found.get("seed") == _pardon_i_found.get("seed"))
            check(PARDON_I_RED_ROW,
                  _pardon_i_same_pair and _pardon_i_red_found.get("seamScore") == 0,
                  "the same search, deterministic and unaffected by this plant (it touches only "
                  "the handle's own numeric value, never which pair or bundle wins), found %s→%s "
                  "again; shipped seamScore=%s, planted back to the written zero seamScore=%s"
                  % (_pardon_i_red_found.get("from") if isinstance(_pardon_i_red_found, dict)
                     else None,
                     _pardon_i_red_found.get("to") if isinstance(_pardon_i_red_found, dict)
                     else None,
                     _pardon_i_found.get("seamScore"),
                     _pardon_i_red_found.get("seamScore") if isinstance(_pardon_i_red_found, dict)
                     else None))


DIE = 4.91016            # the die lab/data/scores' own weave score carries, so every suite rolls one
DURATION_MS = 6500
WITHIN_MS = 500


def _static(v):
    return {"op": "static", "value": v}


def box_cue(stack=0, levels_own=None, **statics):
    """The cue, with a track for every one of the twelve handles (§4.4b)."""
    P = {"axis": 0, "depth": 0.9, "dip": 0.5, "lead": 0.5, "fingers": 7,
         "seam": SEAM_AT, "seamScore": SEAM_SCORE, "shade": 1, "travel": 1,
         "seed": DIE, "mask": 0}
    P.update(statics)
    nodes = {"b-mix": {"source": "progress"}}
    tracks = {"mix": {"node": "b-mix"}}
    for k, v in P.items():
        nodes["b-" + k] = _static(v)
        tracks[k] = {"node": "b-" + k}
    return {
        "id": "box-main", "instrument": {"id": "boxfold", "api": 1},
        "voice": "letter", "roles": ["disassembly", "mystery", "assembly"],
        "levels": ["WORLD", "CELL"],
        "levelOwnership": levels_own or {"WORLD": "owns", "CELL": "owns"},
        "window": [0, DURATION_MS / 1000.0], "works": ["a", "b"], "stack": stack,
        "cameraAuthority": "own",
        "doors": {"in": {"handle": "mix", "value": 0, "measured": True},
                  "out": {"handle": "mix", "value": 1, "measured": True}},
        "nodes": nodes, "tracks": tracks,
        "resources": {"textures": 0, "textureSlots": 2, "framebuffers": 0, "pingPong": 0,
                      "programs": 1, "passes": 1, "bytesEstimate": 0, "variant": "standard"},
    }


def matter_cue(stack=1):
    """THE VOICE THAT STANDS OVER IT. `matter` writes coverage, so it is what a frame-filling ground
    is meant to be played under (COVERAGE.md §3, and the placement rule §7 states). Its own handles
    rest at the defaults its manifest publishes; the two this cue drives are the dial and the
    second."""
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


def box_score(under=False, **statics):
    """`under` puts a coverage-writing voice ABOVE this instrument, which is the placement its own
    declaration buys it: the ground of a stack."""
    cues = [box_cue(stack=0, **statics)]
    if under:
        cues = cues + [matter_cue(stack=1)]
    res = {"textures": 0, "textureSlots": 2, "framebuffers": 0, "pingPong": 0, "programs": 1,
           "passes": 1, "bytesEstimate": 0}
    return {
        "schema": 2,
        "intent": "the frame is one face of a box that turns a quarter with true perspective, its "
                  "fold standing on the departing work's own region line, and the arriving face "
                  "lands exactly (lab/effects/box.js:1-110, its own header)",
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
        "provenance": {"source": "lab/effects/box.js's own declared defaults and constants",
                       "measuredAt": None, "by": "tests/test_pass_boxfold.py"},
    }


# ---------------------------------------------------------------- bake once
build_site.SITE_CONFIG = dict(build_site.SITE_CONFIG)
build_site.SITE_CONFIG["pass"] = {"visualLayer": "pass", "diagnostics": "on"}

TMP = Path(tempfile.mkdtemp(prefix="synth_passbox_"))
build_site.OUT = TMP
build_site.build(SITE_URL)
LAYER = (TMP / "pass-layer.js").read_text(encoding="utf-8")
# THE INSTRUMENT'S OWN BUILT FILE — the real artifact a visitor is served, comments stripped. Since
# every instrument travels alone, the whole of this file is this instrument and nothing else.
PACK = (TMP / "pass-inst-boxfold.js").read_text(encoding="utf-8")
REGION = PACK
SOURCE = ROOT / "engine" / "assets" / "pass-inst-boxfold.js"
# The file as it stands in the tree, comments and all: the rows about what this instrument DECLARES
# read the built artifact, and the rows about what it SAYS read the source it is built from.
SOURCE_TEXT = SOURCE.read_text(encoding="utf-8")
LABTXT = MODULE.read_text(encoding="utf-8") if MODULE.exists() else ""

# ---------------------------------------------------------------- string rows

OWNED = ["createElement", "getContext", "requestAnimationFrame", "addEventListener",
         "performance.now", "Date.now", "new Image", "setTimeout", "setInterval"]
held = [s for s in OWNED if s in REGION]
check("PASS-BOXFOLD the instrument creates no element, no loop and no listener",
      not held,
      "§1.2's fence, read against the instrument's own built file: none of the nine ways of owning "
      "hardware appears there. The module raises its own canvas, takes a WebGL context on it with "
      "the drawing buffer preserved, uploads two textures, runs its own frame loop and observes its "
      "own mount for a resize; all of it stayed in the lab"
      if not held else "the instrument's region holds " + ", ".join(held))

HANDLES = ["mix", "axis", "depth", "dip", "lead", "fingers", "seam", "seamScore",
           "shade", "travel", "seed", "mask"]
absent = [h for h in HANDLES if ("%s: { min" % h) not in REGION]
check("PASS-BOXFOLD every handle the instrument publishes is a handle a score can drive",
      not absent,
      "§4.4b: twelve handles. The dial, the module's own five declared params a pair can stand, the "
      "two that carry the crease's place and its gate, the module's two judge channels, the score's "
      "die and the judges' channel. The module's `faces` is published by neither, and the file says "
      "why: a cue carries an ordered pair, so two works are what stand on the faces"
      if not absent else "these are published nowhere: " + ", ".join(absent))

check("PASS-BOXFOLD no clock handle is published, and the picture is what settles that",
      "clock: { min" not in REGION and "t += dt" in LABTXT
      and "uniform float uTime" not in REGION and "source: \"seconds\"" not in REGION,
      "the module counts a second of its own up in its own frame loop (`t += dt`) and no uniform "
      "ever reads it: nothing in this picture moves with time, only with the hand. A handle a score "
      "can walk without moving the picture is noise in the score, so none is published, and the "
      "seeded repeat below is the same fact read on the frame")

# Every constant the picture stands on, read out of the lab module and out of the built file.
CONSTANTS = [
    ("var BOX_CROP = 1.48;", "var BOX_CROP = 1.48;",
     "the room the turn needs: a crop of 1.34 leaks a background wedge of 2.1 per cent of the frame "
     "at eighteen degrees into the turn, and 1.48 leaks nothing"),
    ("var CAM_FAR = 8.0, CAM_NEAR = 3.0, DIP_MAX = 0.12;",
     "var CAM_FAR = 8.0, CAM_NEAR = 3.0, DIP_MAX = 0.12;",
     "the camera's own range in box half-widths, and how far the eye rides up through a quarter"),
    ("var EASE_P = 1.9;", "var EASE_P = 1.9;",
     "the turn's rate inside a quarter: nothing at each landing, a third again the mean in the "
     "middle"),
    ("var AMP = 0.05;", "var AMP = 0.05;", "how far a face's picture travels inside one quarter"),
    ("var FING_MAX = 0.09;", "var FING_MAX = 0.09;", "how deep the finger joint bites"),
    ("var FING_N = 7;", "var FING_N = 7;",
     "how many fingers stand along the crease, until a score names the work's own"),
    ("var SEAM_FLOOR = 0.20;", "var SEAM_FLOOR = 0.20;",
     "how far a work must fall into two regions before its best line counts as a seam at all"),
    ("var FEEL_D0 = 0.05;", "var FEEL_D0 = 0.05;",
     "the dead bands at either end of the hand, where the box stands exactly landed"),
    ("Math.pow(clamp(f, 0, 1), EASE_P)", "Math.pow(clamp(f, 0, 1), EASE_P)",
     "the quarter's own response, applied to the raw travel"),
    ("hash11(float n){ return fract(sin(n * 127.1) * 43758.5453); }",
     "hash11(float n){ return fract(sin(n * 127.1) * 43758.5453); }",
     "the joint's own die, hashed per finger"),
    ("clamp((p - 0.5) * f.xy + 0.5 + f.zw, 0.0008, 0.9992)",
     "clamp((p - 0.5) * f.xy + 0.5 + f.zw, 0.0008, 0.9992)",
     "how a face reads its source: the cover fit over the whole face, held off its own edge"),
    ("vec3(0.031, 0.031, 0.039)", "vec3(0.031, 0.031, 0.039)",
     "what the box stands against where neither face reaches"),
    ("smoothstep(0, 0.09, G.f) * smoothstep(1, 0.91, G.f)",
     "smoothstep(0, 0.09, jj.f) * smoothstep(1, 0.91, jj.f)",
     "the contact shadow's gate, out at every landing"),
    ("0.34 * uGuard * lit * exp(-far / 9.0)", "SHADE * uTurn.w * lit * exp(-far / REACH)",
     "and the shadow itself, at a depth of 0.34 decaying over nine points of the buffer"),
    ("mix(fi / max(uFingN - 1.0, 1.0), hash11(fi + uSeed), 0.4)",
     "mix(fi / max(uJoint.y - 1.0, 1.0), hash11(fi + uSeed), DIE)",
     "six parts a ladder along the crease and four parts the score's die"),
    ("var s = Math.sin(n) * 43758.5453;", "var s = Math.sin(n) * 43758.5453;",
     "how the score's own seed becomes the joint's die"),
]
missing_const = [p for lab_p, p in ((a, b) for a, b, _ in CONSTANTS)
                 if lab_p not in LABTXT or p not in REGION]
check("PASS-BOXFOLD every constant the picture stands on carries the module's own number",
      not missing_const and bool(LABTXT),
      "; ".join("%s — %s" % (p, why) for _, p, why in CONSTANTS) if not missing_const
      else "these differ between the lab module and the port: " + ", ".join(missing_const))

check("PASS-BOXFOLD the port's own one number is named as its own, and it is the room the crease needs",
      "var SEAM_ROOM = 0.42;" in REGION and "SEAM_ROOM" not in LABTXT
      and "var SEAM_REACH = 0.25;" in REGION
      and "var CROP = BOX_CROP + SEAM_ROOM;" in REGION,
      "the module measured its crop for the TURN ALONE and moved the crease onto the departing "
      "work's own region line afterwards without reading the crop again, so carrying its camera's "
      "slide over a box built for no slide opens the frame's corners. SEAM_ROOM is what closes them "
      "and it is the only number here the module did not measure; SEAM_REACH is the measurement's "
      "own search window — cut-lines.py looks for the line in the middle half of the work — which is "
      "what bounds the travel the room has to pay for")

check("PASS-BOXFOLD the host binds uniforms by declared name, never by position or a written list",
      "getUniformLocation(p, u.name)" in LAYER and "uQuad" not in LAYER and "uInv" not in LAYER,
      "this instrument declares twenty-one uniforms, of which five are shared with the woven one. "
      "host reads the manifest")

declared = set(re.findall(r'\{ name: "(u\w+)", type:', REGION))
spelled = set(re.findall(r'uniform \w+ (u\w+);', REGION))
check("PASS-BOXFOLD the manifest's declared names and the shader's own names are one set",
      declared == spelled,
      f"{len(declared)} declared, {len(spelled)} spelled; "
      f"declared only: {sorted(declared - spelled)}; spelled only: {sorted(spelled - declared)}")

SUPPLY = ["textureA", "textureB", "fitA", "fitB", "resolution", "seconds"]
sources = set(re.findall(r'source: "([^"]+)"', REGION))
outside = [s for s in sources
           if s not in SUPPLY and not s.startswith("frame:") and not s.startswith("handle:")]
check("PASS-BOXFOLD every uniform is sourced from the closed set the host can supply",
      not outside and len(sources) >= 10,
      "§7's uniform sources are the two source textures, their fits, the resolution, the "
      "transaction's seconds, a value the instrument answers and a handle. This instrument names "
      f"{len(sources)} distinct sources and none outside that set"
      if not outside else "outside the set: " + ", ".join(outside))

check("PASS-BOXFOLD the shader carries no version header of its own",
      "#version" not in REGION,
      "so the host's translator stamps the one header this shader needs and no second one arrives")

check("PASS-BOXFOLD the manifest leaves the drawing buffer unpreserved, where the module asked for it",
      "gl: { preserveDrawingBuffer: false }" in REGION
      and "preserveDrawingBuffer: true" in LABTXT,
      "§7 refuses a manifest that asks for the buffer to be preserved, and the module asks for it by "
      "name; this instrument draws every frame the host hands it")

check("PASS-BOXFOLD the coverage is declared, and the frame it fills is the reason",
      "coverage: { writes: false" in REGION
      and "gl_FragColor = vec4(col, 1.0);" in REGION
      and "opacity" not in REGION and "presence" not in REGION,
      "§8's coverage block and §7's law: the alpha is the constant 1, said as a decision. The box is "
      "built larger than the frame by the room the turn needs plus the room the crease's travel "
      "needs, so the two visible faces cover the frame at every point of the turn. Under the "
      "placement rule that makes this instrument lawful as the LOWEST cue of a stack. No handle of "
      "opacity and no weight of presence stands anywhere in the instrument")

# THE CREASE, AND THE MEASUREMENT IT READS. His 19:13 word, lifted to the class at 19:21: every
# geometric parameter names the measurement of the work it reads. For this instrument the crease's
# own PLACE is that parameter, and it is the half of the charter's boundary test that asks whose
# structure draws the boundary.
check("PASS-BOXFOLD the crease's own handle publishes the measurement it reads",
      'reads: "structure.regions from lab/cut-lines.py' in REGION
      and "structure.regions.line.<axis>.explains from the same file" in REGION
      and 'applied: { floor: SEAM_FLOOR }' in REGION
      and "structure.grid.countFrom over the departing work's own frame side" in REGION,
      # THE GATE'S OWN FIELD WAS NAMED WRONG until 2026-08-26 and this row carried the wrong name
      # with it. The handle published `structure.regions.score`, which the record does carry, but
      # `SEAM_FLOOR` was calibrated against the per-axis `line.<axis>.explains` reading and against
      # no other — the floor's own table lists four works explaining 0.89, 0.48, 0.28 and 0.03,
      # which are those readings, while `score` on the fixture's own first work stands at 0.7401
      # against a line explaining 0.6054. The floor did not move; the name did. (A tally over the
      # collection stood in this sentence too and is gone: it is the one thing the standing rules
      # forbid a row to argue from.)
      "the fold's PLACE is `seam`, reading structure.regions — the line along the turn's own "
      "direction that best splits the departing work's columns into two groups; its gate is "
      "`seamScore`, reading how much of that difference the line explains, against the module's "
      "own floor of 0.20. The fold's SHAPE is "
      "`fingers`, reading the same measured repeat grid-colour derives its count from. Both halves "
      "of the boundary are the work's, which is the whole of the charter's pardon")

# BEHAVIOUR NOT TEXT. A grep of the sentence explaining why this file may not measure a work for
# itself proves only that the sentence sits in the file — a defect could stand right beside it and
# the row would still pass. What actually keeps the instrument from measuring anything is that none
# of the APIs measuring would require are anywhere in the built file; that absence is what is read.
FENCE = ["createElement", "getContext", "requestAnimationFrame", "addEventListener",
         "performance.now", "Date.now", "new Image", "setTimeout", "setInterval",
         "getImageData", "readPixels"]
held = [s for s in FENCE if s in REGION]
check("PASS-BOXFOLD the instrument measures no work for itself, and says why",
      not held and "seamOf" not in REGION,
      "§1.2's fence, read against the built file: none of the ways of drawing a work into a "
      "surface of its own and counting it appears there, so the seam this instrument plays on can "
      "only ever be a handle a score hands in — never a number this file took for itself"
      if not held else "the instrument's file holds " + ", ".join(held))

# THE DOOR READING, AND ITS OWN NUMBERS. The manifest's own contract (`applied.readAtADoor` on the
# `mask` handle) and the five-pardon-condition split are both read back off the RUNNING instrument
# further down, where the browser has already walked the real door boundary and measured the other
# four conditions — a manifest-vs-comment text match can never catch either drifting from what the
# runtime actually does, since both would be read out of one file by such a match. See
# "PASS-BOXFOLD the judges' handle's published door contract is the boundary just measured" and
# "PASS-BOXFOLD the five pardon conditions divide the way the file says, and the split is real",
# both in the browser rows below.

sha = hashlib.sha256(MODULE.read_bytes()).hexdigest() if MODULE.exists() else ""
declared_sha = (re.search(r'sha256: "([0-9a-f]{64})"', REGION) or [None, None])[1]
check("PASS-BOXFOLD the provenance names the file the port was read from, and the file weighs to it",
      bool(sha) and sha == declared_sha and 'commit: "11e2db4"' in REGION,
      f"the module is tracked, so the commit it was read at is named beside the digest of its bytes, "
      f"and the file still weighs to {sha[:16]}…")

# ---------------------------------------------------------------- browser rows

BROWSER_ROWS = [
    "PASS-BOXFOLD §8     · the manifest carries every field the contract names, in its shape",
    "PASS-BOXFOLD §8     · it publishes WORLD and CELL, and the reading is said to be derived",
    "PASS-BOXFOLD row 7  · door 0 stands the departing work, measured against its own file",
    "PASS-BOXFOLD row 7  · door 0 carries no trace of the arriving work",
    "PASS-BOXFOLD row 7  · door 1 stands the arriving work, measured against its own file",
    "PASS-BOXFOLD row 7  · door 1 carries no trace of the departing work",
    "PASS-BOXFOLD the two roads agree at the doors and at six places through the turn",
    "PASS-BOXFOLD §7     · the frame is covered by the two faces at every sampled pose",
    "PASS-BOXFOLD §7     · the ground of a stack, and refused above another cue",
    "PASS-BOXFOLD §7     · both doors stand whole with a coverage-writing voice over them",
    "PASS-BOXFOLD §7     · no empty frame at any sampled instant of the pass",
    "PASS-BOXFOLD §7     · the frame after a change of viewport is drawn afresh",
    "PASS-BOXFOLD row 10 · a seeded run repeats to the pixel",
    "PASS-BOXFOLD row 14 · textures, programmes and framebuffers return to their baseline after ten runs",
    "PASS-BOXFOLD row 15 · the console stays clean",
    "PASS-BOXFOLD row 22 · the census shows granted against declared, and neither overruns",
    "PASS-BOXFOLD §7     · one canvas, one context, two source textures, one pass a frame",
    "PASS-BOXFOLD §7     · a shader already at GLSL ES 3.00 receives no second version header",
    "PASS-BOXFOLD the real transaction road: curtain up, one pass drawn, exactly one dock at the end",
    "PASS-BOXFOLD row 9  · one camera authority through a real pass, and the pose rests on the arrival",
    "PASS-BOXFOLD §4.4b  · the axis, the perspective, the dip, the joint and the shadow reach the PICTURE",
    "PASS-BOXFOLD the charter · the fold stands on the work's region line, and moving it back moves the frame",
    "PASS-BOXFOLD the box is WALKED on the drawing buffer at both doors, and what it read is published",
    "PASS-BOXFOLD a door the judges' channel spoils is refused on the real road, and the visitor still lands",
    "PASS-BOXFOLD row 16 · the captures are kept as evidence",
    "PASS-BOXFOLD the judges' handle's published door contract is the boundary just measured",
    "PASS-BOXFOLD the five pardon conditions divide the way the file says, and the split is real",
]

# THE DOOR ROWS ABOVE ALL STAND AT `axis` 0 — the crease upright — because `box_cue`'s and
# `fixture_pass_boxfold.html`'s own default pose does, and every door row in this file has since it
# was written. The handle has TWO values, both of them enum steps a score drives (`axis: {min: 0,
# max: 1, kind: "enum", step: 1}`), and the composer drives the other one on every real bundle whose
# pivot reads a banding axis running the other way. This row stands the same two doors at `axis` 1.
#
# WHAT IT CAUGHT (2026-09-02). With the crease FLAT, `posed`'s own `pt` puts the face's two axes on
# the screen the other way round — `s`, across the turn's plane, runs UP the frame and `t`, along the
# crease, runs ACROSS it — and the shader pasted the picture onto the face by one fixed rule
# regardless, so a landed face stood the work REFLECTED ABOUT ITS OWN ANTI-DIAGONAL. Every row above
# passed through it: the box's own door reading walks its faces' CORNERS over the buffer and never
# asks where inside the source a face reads, the two-roads rows compare this port against the lab
# module which pastes it the same way, and no door row was ever taken at this axis. The walk's own
# DOM read it at 34 of 255 on the mean and 176 on the worst channel at both real doors
# (`tests/test_pass_hang.py`'s real-pair rows), which is what sent it here.
FLAT_DOOR_ROW = ("PASS-BOXFOLD row 7  · with the crease lying FLAT, both doors still stand the work "
                 "the right way up, measured against their own files")
FLAT_DOOR_RED_ROW = ("PASS-BOXFOLD red-on-bug · pasting the picture on the face by one fixed rule "
                     "mirrors both flat-crease doors about the anti-diagonal")

RED_ROWS = [
    "PASS-BOXFOLD red-on-bug · the room the crease's travel needs removed: the frame stops being covered",
    "PASS-BOXFOLD red-on-bug · the landing window removed: the entry door is refused, off its own landing",
    "PASS-BOXFOLD red-on-bug · the contact shadow removed: the two roads part where the crease lies",
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
    """The share of the face map that names no face. The map paints the departing face at half of
    full red and the arriving one at full; a point neither face covers stays black. So this is the
    share of the frame the crop failed to fill."""
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


def work_in_the_frame(src, w, h, crop=CROP):
    """The whole file, cover-fitted into the frame and centre-cropped by the box's own crop. The
    frame is a window cut out of the middle of a bigger box, and the crop is what the doors' own
    `framings` block publishes."""
    from PIL import Image
    return cover_into(Image.open(src).convert("RGB"), w, h, crop)


def apart(p, work):
    from PIL import Image, ImageChops, ImageStat
    a = Image.open(p).convert("RGB")
    if a.size != work.size:
        return 255.0, 255.0
    st = ImageStat.Stat(ImageChops.difference(a, work))
    return sum(st.mean) / 3.0, max(m for _, m in st.extrema)


# THE LAB MODULE AS THE BENCH SERVES IT. One literal is changed and nothing else: its crop is
# levelled to the port's own. The port grows the box by the room the crease's travel needs and the
# module never did, so a comparison at the module's own crop would compare two differently sized
# boxes rather than two readings of one geometry. The file on disk is never touched.
LAB_CROP_FROM = "var BOX_CROP = 1.48;"
LAB_CROP_TO = "var BOX_CROP = %s;" % CROP


def bench_dir(pack_text=None):
    """The bench's own served root: the BUILT pass-layer.js, the site's own settings record and the
    BUILT instrument files it names — the real artifacts, namespace applied and comments stripped —
    the lab module with its crop levelled, the two photographs, and the page that stands the two
    roads of one frame side by side.

    A row proving a rule reds hands over a CHANGED instrument file and writes the record with the
    digest of the bytes actually served, which is what the build does. The source file on disk is
    never touched, so nothing has to be restored and no working tree can be left changed by a
    red-on-bug proof."""
    d = Path(tempfile.mkdtemp(prefix="synth_boxbench_"))
    pack = PACK if pack_text is None else pack_text
    shutil.copy2(TMP / "pass-layer.js", d / "pass-layer.js")
    for _inst in sorted(TMP.glob("pass-inst-*.js")):
        shutil.copy2(_inst, d / _inst.name)
    (d / "pass-inst-boxfold.js").write_text(pack, encoding="utf-8")
    record = json.loads((TMP / "config.json").read_text(encoding="utf-8"))
    record["pass"]["instruments"]["boxfold"]["digest"] = hashlib.sha256(
        pack.encode("utf-8")).hexdigest()
    (d / "config.json").write_text(json.dumps(record), encoding="utf-8")
    (d / "box.js").write_text(LABTXT.replace(LAB_CROP_FROM, LAB_CROP_TO, 1), encoding="utf-8")
    (d / "photos").mkdir()
    for p in PHOTOS:
        shutil.copy2(p, d / "photos" / p.name)
    shutil.copy2(ROOT / "tests" / "fixture_pass_boxfold.html", d / "index.html")
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


def crease(br, at=SEAM_AT, score=SEAM_SCORE):
    return js(br, "return window.__crease(%r, %r);" % (at, score))


def roads(br, at, tag):
    """BOTH ROADS AT ONE POSE. The dial is the raw hand on both sides: the module applies its own
    dead bands and its own quarter curve to it, and so does the port, so handing one number to both
    is handing them one pose."""
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


def face_map(br, at, tag):
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


def _bench_grid(br):
    c = "document.querySelector('canvas[aria-hidden]')"
    return (int(br.evaluate("String(%s.width)" % c)), int(br.evaluate("String(%s.height)" % c)))


def flat_doors(br, w, h):
    """BOTH DOORS WITH THE CREASE LYING FLAT, each against its own file.

    `axis` is an enum handle of two steps and a score drives both; every other door row in this file
    stands at the first. This walks the second and reads the same comparison — the door against the
    whole source file, cover-fitted into the frame and centre-cropped by the box's own crop, which is
    what the `framings` block publishes and which the crease's own direction cannot change: with the
    crease flat the box's two half-extents change places with each other AND so does the frame's own
    pair, so the frame still sees exactly the middle 1/CROP of the face either way.

    The axis is put back where it was found, so nothing downstream reads a bench this row moved."""
    crease(br)
    br.evaluate("window.__param('axis', 1); 0")
    br.sleep(0.45)
    out = {}
    for tag, at, src in (("flat-door-0", 0.0, PHOTOS[0]), ("flat-door-1", 1.0, PHOTOS[1])):
        out[tag] = apart(host_shot(br, at, tag), work_in_the_frame(src, w, h))
    br.evaluate("window.__param('axis', 0); 0")
    br.sleep(0.35)
    return out


if not chrome_available():
    for r in BROWSER_ROWS + RED_ROWS + [FLAT_DOOR_ROW, FLAT_DOOR_RED_ROW]:
        skip(r, "Chrome not installed (pinned expected skip)")
elif missing:
    for r in BROWSER_ROWS + RED_ROWS + [FLAT_DOOR_ROW, FLAT_DOOR_RED_ROW]:
        skip(r, "the lab tree is read-only source material and is absent here: " + missing[0])
else:
    shutil.rmtree(SHOTS, ignore_errors=True)
    SHOTS.mkdir(parents=True, exist_ok=True)
    BENCH = bench_dir()
    with serve(BENCH) as base:
        with Browser(width=VW, height=VH) as br:
            br.navigate(base + "/index.html")
            if not ready(br):
                for r in BROWSER_ROWS + [FLAT_DOOR_ROW]:
                    check(r, False, "the bench never came up: "
                         + br.evaluate("JSON.stringify(window.__errs||[])"))
            elif not js(br, "return !!window.__exPass.bench.manifest('boxfold');"):
                why = js(br, "var e = window.__host.report().events.filter(function(x){"
                             "return x.name === 'manifest-refused';});"
                             "return e.length ? e[e.length - 1].why : null;")
                for r in BROWSER_ROWS + [FLAT_DOOR_ROW]:
                    check(r, False, "the host registered no «box» instrument: " + str(why))
            else:
                SCORE = json.dumps(box_score())
                SCORE_UNDER = json.dumps(box_score(under=True))

                # ---- §8: the manifest, read off the registered instrument -----------------------
                m = js(br, "return window.__exPass.bench.manifest('boxfold');")
                res = m["resources"]
                need = ["id", "api", "arity", "roles", "params", "handles", "neutrals", "doors",
                        "framings", "drivers", "camera", "gl", "passes", "resources",
                        "capabilities", "decline", "provenance", "readiness", "coverage", "levels"]
                shape = (
                    all(k in m for k in need)
                    and m["id"] == "boxfold" and m["api"] == 1 and m["arity"] == 2
                    and m["roles"] == ["disassembly", "mystery", "assembly"]
                    and sorted(m["params"]) == ["axis", "depth", "dip", "fingers", "lead"]
                    and len(m["handles"]) == 12
                    and all(set(h) >= {"min", "max", "def"} for h in m["handles"].values())
                    and m["neutrals"] == {"a": 0, "b": 1}
                    and m["doors"]["in"]["handle"] == "mix" and m["doors"]["in"]["value"] == 0
                    and m["doors"]["out"]["handle"] == "mix" and m["doors"]["out"]["value"] == 1
                    and sorted(m["framings"]) == ["0", "1"]
                    and m["framings"]["0"] == {"coverCrop": CROP} == m["framings"]["1"]
                    and m["camera"] == {"needs": "none", "authority": "own"}
                    and m["surface"] == {"type": "two-face-fold", "anchor": "measured-hang",
                                         "tessellation": {"faces": 2}, "cameraAuthority": "own",
                                         "entry": {"mix": 0, "work": "a", "pose": "flat"},
                                         "exit": {"mix": 1, "work": "b", "pose": "flat"}}
                    and m["gl"] == {"preserveDrawingBuffer": False}
                    and len(m["passes"]) == 1 and len(m["passes"][0]["uniforms"]) == 21
                    and sorted(res) == ["lean", "rich", "standard"]
                    and all("bytesEstimate" in res[v] and res[v]["programs"] == 1
                            and res[v]["passes"] == 1 and res[v]["textureSlots"] == 2
                            for v in res)
                    and m["capabilities"] == ["webgl2"] and m["decline"]
                    and m["coverage"]["writes"] is False and m["coverage"]["how"]
                    and m["provenance"]["labPath"] == "lab/effects/box.js"
                    and m["provenance"]["commit"] == "11e2db4"
                    and m["readiness"] == "production-ready"
                    and "boxfold" in js(br, "return window.__host.report().registered;"))
                check(BROWSER_ROWS[0], shape,
                      f"twelve handles, twenty-one uniforms in one pass, both doors at a cover crop of "
                      f"{m['framings']['0']['coverCrop']} — the room the turn needs plus the room "
                      f"the crease's travel needs — resources declared for three tiers with a byte "
                      f"estimate of {res['standard']['bytesEstimate']}, and a coverage block reading "
                      f"«{m['coverage']['how']}»")

                check(BROWSER_ROWS[1],
                      m["levels"] == ["WORLD", "CELL"]
                      and all(h.get("level") not in ("CELL CONTENT", "TEXTURE", "LIGHT-COLOUR")
                              for h in m["handles"].values()),
                      f"levels={m['levels']}, read off the manifest bench.manifest() actually hands "
                      f"back rather than grepped off a comment citing the charter's shelf. No handle "
                      f"anywhere in it claims CELL CONTENT, TEXTURE or LIGHT-COLOUR either. WORLD: "
                      f"the flat frame becomes one face of a solid standing in a space, seen through "
                      f"a real projection, with the eye riding up through the turn — the two roads' "
                      f"own inverted-projection residual further below is what proves that whole, "
                      f"not this row. CELL: the two faces, meeting at a finger joint, which is the "
                      f"panel a `regions` pivot asks for")

                w = int(br.evaluate("String(window.__exPass.bench.make() && "
                                    "document.querySelector('canvas[aria-hidden]').width)"))
                h = int(br.evaluate("String(document.querySelector('canvas[aria-hidden]').height)"))
                bufs = js(br, "return window.__buffers();")
                glass = work_in_the_frame(BENCH / "photos" / "glassgrid.jpg", w, h)
                towers = work_in_the_frame(BENCH / "photos" / "towers.jpg", w, h)

                # ---- the poses, on both roads ---------------------------------------------------
                crease(br)
                DOORS = [("door-0", 0.0), ("door-1", 1.0)]
                TURN = [("q1", 0.14), ("q2", 0.28), ("q3", 0.42), ("q4", 0.58), ("q5", 0.72),
                        ("q6", 0.86)]
                shots, reads = {}, {}
                for tag, at in DOORS + TURN:
                    reads[tag], hp, mp = roads(br, at, tag)
                    shots[tag] = (hp, mp)

                for i, (door, own, other, ownn, othern) in enumerate((
                        ("door-0", glass, towers, "glassgrid.jpg", "towers.jpg"),
                        ("door-1", towers, glass, "towers.jpg", "glassgrid.jpg"))):
                    a, amx = apart(shots[door][0], own)
                    check(BROWSER_ROWS[2 + i * 2], a <= SEAM,
                          f"{door} against {ownn} at the cover crop of {CROP}: mean {a:.4f} of 255 "
                          f"(threshold {SEAM}), worst channel {amx}. Everything that moves through a "
                          f"quarter — the turn, the camera's dip, the crease's slide, the "
                          f"counter-motion, the joint's bite and the contact shadow — rides one sine "
                          f"over the quarter and is nothing at its ends, so a landed face is the "
                          f"picture its source carries")
                    o, _ = apart(shots[door][0], other)
                    check(BROWSER_ROWS[3 + i * 2], o >= FAR,
                          f"{door} against {othern}: mean {o:.4f} of 255 (must exceed {FAR})")

                agree = [(t, ) + diff(*shots[t]) for t, _ in DOORS + TURN]
                check(BROWSER_ROWS[6],
                      all(mn <= ROADS for _, mn, _ in agree)
                      and bufs["host"] == bufs["module"],
                      "; ".join(f"{t}: mean {mn:.4f} of 255 (bar {ROADS}), worst channel {mx}"
                                for t, mn, mx in agree)
                      + f". Both roads drew on a {bufs['host']} buffer, so one sampler ran through "
                        f"one rasteriser on both sides and what is left between them is arithmetic: "
                        f"this port hands the shader each face's four screen corners where the "
                        f"module handed four lines, and each inverse map as its three rows where the "
                        f"module handed a matrix, because the host binds neither a matrix nor an "
                        f"array of lines. The module is served with its crop levelled to the port's "
                        f"own and nothing else changed")

                # ---- the same two doors, with the crease lying FLAT ------------------------------
                flat = flat_doors(br, w, h)
                check(FLAT_DOOR_ROW,
                      all(mn <= SEAM for mn, _ in flat.values()),
                      "; ".join(f"{t} against its own file at the cover crop of {CROP}: mean "
                                f"{mn:.4f} of 255 (threshold {SEAM}), worst channel {mx}"
                                for t, (mn, mx) in sorted(flat.items()))
                      + ". Which way the crease lies decides which of the face's own two axes runs "
                        "across the frame and which runs up it; the picture is pasted onto the face "
                        "by that same decision, so a landed face stands the work the right way up "
                        "either way. Pasted by one fixed rule instead, both of these doors stand it "
                        "mirrored about its own anti-diagonal, which the red-on-bug row below reads")

                # ---- §7: the frame is covered, read off the face map ------------------------------
                maps = []
                for tag, at in DOORS + TURN:
                    maps.append((tag, unclaimed(face_map(br, at, tag))))
                check(BROWSER_ROWS[7], all(s == 0.0 for _, s in maps),
                      "; ".join(f"{t}: {s * 100:.4f}% unclaimed" for t, s in maps)
                      + ". The face map paints which face stands at each point of the frame and "
                        "leaves black exactly where neither does. It is black nowhere, which is the "
                        "crop measured on the picture rather than argued: the box is built larger "
                        "than the frame by the room the turn needs plus the room the crease's "
                        "travel needs")
                br.evaluate("window.__mask(0); window.__show('host'); 0")

                # ---- §7: the placement its declaration buys --------------------------------------
                # THE ROOF CASE IS READ OVER A FLOOR THAT IS ITSELF LAWFUL, so the reason that comes
                # back is this instrument's own. The woven instrument fills the frame too, so it may
                # stand lowest; laid over it, this one is refused by name.
                place = js(br, """
                  var b = window.__exPass.bench;
                  return {declared: b.coverageOf('boxfold'),
                          asGround: b.coverageWhyNo([
                            {id: 'ground', instrument: {id: 'boxfold', api: 1}, stack: 0},
                            {id: 'over', instrument: {id: 'matter', api: 1}, stack: 1}]),
                          asRoof: b.coverageWhyNo([
                            {id: 'floor', instrument: {id: 'weave', api: 1}, stack: 0},
                            {id: 'ground', instrument: {id: 'boxfold', api: 1}, stack: 1}])};
                """)
                took_stack = js(br, "return window.__offer(%s, {clock: 1.5, progress: 0.3});"
                                % SCORE_UNDER)
                br.sleep(0.4)
                br.evaluate("window.__cancel('placement row'); 0")
                idle(br)
                check(BROWSER_ROWS[8],
                      place["declared"] and place["declared"]["writes"] is False
                      and place["asGround"] is None
                      and isinstance(place["asRoof"], str) and "«boxfold»" in place["asRoof"]
                      and took_stack["took"],
                      f"the host reads this instrument's declaration as writes="
                      f"{place['declared']['writes']} and places it by it. Laid lowest with a "
                      f"coverage-writing voice above, the stack is lawful and the host takes the "
                      f"score. Laid over a floor that is itself lawful, it is refused by name: "
                      f"«{place['asRoof']}»")

                # EACH END OF THE STACK BELONGS TO THE VOICE THAT DECLARED IT. At the near door the
                # voice above carries no matter at all — `matter` writes an alpha of 0 across the
                # whole frame at its own `mix` of 0 — so the frame is this instrument's whole work,
                # which is what a ground is for. At the far door that voice is opaque and the door is
                # its own: `texB` whole under the crop its manifest publishes.
                over_crop = js(br, "return window.__exPass.bench.manifest('matter')"
                                   ".framings['1'].coverCrop;")
                stack_doors = []
                for at, work, name in (
                        (0.0, glass, "glassgrid.jpg, seated by this instrument at %s" % CROP),
                        (1.0, work_in_the_frame(BENCH / "photos" / "towers.jpg", w, h, over_crop),
                         "towers.jpg under the arriving voice's own crop of %s" % over_crop)):
                    js(br, "return window.__offer(%s, {clock: 1.5, progress: %r});"
                       % (SCORE_UNDER, at))
                    br.sleep(0.7)
                    p = png(br, SHOTS / ("stack-door-%03d.png" % round(at * 100)))
                    br.evaluate("window.__cancel('stack door row'); 0")
                    idle(br)
                    stack_doors.append((at, name) + apart(p, work))
                check(BROWSER_ROWS[9],
                      all(mn <= SEAM for _, _, mn, _ in stack_doors),
                      "; ".join(f"door {at} against {n}: mean {mn:.4f} of 255 (threshold {SEAM}), "
                                f"worst channel {mx}" for at, n, mn, mx in stack_doors)
                      + ". A ground has to close its own frame at both ends or the cleared buffer "
                        "shows through the door the visitor lands on")

                # ---- §7: no empty frame, and the redraw the preserved buffer stood in for --------
                empties = []
                for at in (0.0, 0.15, 0.3, 0.5, 0.7, 0.85, 1.0):
                    js(br, "return window.__offer(%s, {clock: 1.5, progress: %r});" % (SCORE, at))
                    br.sleep(0.5)
                    p = png(br, SHOTS / ("instant-%03d.png" % round(at * 100)))
                    empties.append((at, ) + standing(p))
                    br.evaluate("window.__cancel('instant sweep'); 0")
                    idle(br)
                check(BROWSER_ROWS[10],
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
                check(BROWSER_ROWS[11],
                      d >= FAR and s >= SPREAD and sized["pdb"] is False,
                      f"after the viewport moved to {VW - 80}x{VH - 120} the buffer reads "
                      f"{sized['buffer']} and the frame stands {d:.2f} from the background with a "
                      f"spread of {s:.2f}; the context keeps preserveDrawingBuffer={sized['pdb']}. "
                      f"The box's own half-sides are the frame's own two half-extents grown by the "
                      f"crop, so the whole solid is rebuilt at the new ratio rather than re-shown")

                # ---- the seeded repeat -----------------------------------------------------------
                br.sleep(0.6)
                took = js(br, "return window.__offer(%s, {clock: 1.5, progress: 0.3});" % SCORE)
                br.sleep(1.2)
                first = png(br, SHOTS / "seeded-1.png")
                rep1 = js(br, "return window.__report();")
                br.evaluate("window.__cancel('between runs'); 0")
                idle(br)
                js(br, "return window.__offer(%s, {clock: 1.5, progress: 0.3});" % SCORE)
                br.sleep(1.2)
                second = png(br, SHOTS / "seeded-2.png")
                mn, mx = diff(first, second)
                check(BROWSER_ROWS[12], took["took"] and mn == 0.0 and mx == 0,
                      f"took={took['took']} two runs of one seeded score: mean {mn} worst channel "
                      f"{mx}. Every number the shader reads comes from a handle, and the die that "
                      f"orders the joint's fingers is the score's — the module rolled its own where "
                      f"a score named none, and this instrument answers with nothing instead")

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
                check(BROWSER_ROWS[13], same,
                      f"before={base_c['textures']}/{base_c['programs']}/{base_c['framebuffers']} "
                      f"after ten runs={after['textures']}/{after['programs']}/"
                      f"{after['framebuffers']} (textures/programmes/framebuffers)")

                errs = json.loads(br.evaluate("JSON.stringify(window.__errs||[])"))
                check(BROWSER_ROWS[14], not errs, "; ".join(errs)[:300])

                # THE CENSUS IS READ ON A BENCH OF ITS OWN, and the reason is the programme cache:
                # it holds one entry per branch and outlives every transaction, so a session that has
                # already drawn another instrument grants two programmes to a score declaring one.
                r = on_bench(lambda b2: (
                    js(b2, "return window.__offer(%s, {clock: 1.0, progress: 0.4});" % SCORE),
                    b2.sleep(0.8),
                    js(b2, "return window.__report();")["resources"])[-1])
                check(BROWSER_ROWS[15],
                      r and r["declared"] and r["over"] is False
                      and r["granted"]["textures"] == r["declared"]["textures"]
                      and r["granted"]["programs"] == r["declared"]["programs"] == 1
                      and r["granted"]["framebuffers"] == r["declared"]["framebuffers"]
                      and r["granted"]["bytes"] == r["declared"]["bytesEstimate"],
                      f"declared={r and r['declared']} granted={r and r['granted']}")

                js(br, "return window.__offer(%s, {clock: 1.0, progress: 0.4});" % SCORE)
                br.sleep(0.6)
                cen = js(br, "return window.__report();")["census"]
                check(BROWSER_ROWS[16],
                      cen["canvases"] == 1 and cen["contexts"] == 1 and cen["textures"] == 2
                      and cen["passesLastFrame"] == 1 and cen["framebuffers"] == 0
                      and cen["preserveDrawingBuffer"] is False,
                      f"census={cen}; the module's own canvas, its second context, its two textures "
                      f"and its own frame loop are what this port does without")
                br.evaluate("window.__cancel('census row'); 0")
                idle(br)

                r = js(br, """
                  var m = window.__exPass.bench.manifest('boxfold');
                  var plain = window.__exPass.bench.es3(m.passes[0].frag, false);
                  var already = window.__exPass.bench.es3('#version 300 es\\n' + m.passes[0].frag, false);
                  var count = function (s) { return s.split('#version').length - 1; };
                  return {source: count(m.passes[0].frag), stamped: count(plain),
                          untouched: count(already), head: plain.slice(0, 15)};
                """)
                check(BROWSER_ROWS[17],
                      r["source"] == 0 and r["stamped"] == 1 and r["untouched"] == 1
                      and r["head"].startswith("#version 300 es"),
                      f"the shader carries {r['source']} headers, the translator leaves it with "
                      f"{r['stamped']}, and a source that already carries one comes back with "
                      f"{r['untouched']}")

                # ---- curtain up, one pass drawn, exactly one dock --------------------------------
                br.evaluate("window.__cancel('before the whole pass'); 0")
                idle(br, nap=0.05)
                br.evaluate("window.__hooks.docks.length = 0; window.__hooks.curtains.length = 0; 0")
                took = js(br, "return window.__offer(%s, {});" % SCORE)
                br.sleep(0.5)
                mid = js(br, "var r = window.__report(); return {state: r.state, "
                             "curtains: window.__hooks.curtains.slice(), camera: r.camera};")
                idle(br)
                end = js(br, "return {state: window.__report().state, "
                             "docks: window.__hooks.docks.slice(), "
                             "curtains: window.__hooks.curtains.slice(), "
                             "events: window.__report().events.map(function(e){return e.name;})"
                             ".slice(-6)};")
                check(BROWSER_ROWS[18],
                      took["took"] and mid["state"] == "running" and mid["curtains"][:1] == [True]
                      and end["state"] == "idle" and len(end["docks"]) == 1
                      and end["curtains"][-1] is False and "docked" in end["events"],
                      f"mid={mid} end={end}")

                cam = js(br, "var r = window.__report(); "
                             "return {camera: r.camera, rest: r.rest, handoffs: r.handoffs, "
                             "tol: r.camTolerances};")
                check(BROWSER_ROWS[19],
                      cam["camera"] and cam["camera"]["owner"] == "stage"
                      and mid["camera"] and mid["camera"]["owner"] == "cue:box-main"
                      and (abs(mid["camera"]["pose"]["panX"]) > 0.0001
                           or abs(mid["camera"]["pose"]["panY"]) > 0.0001)
                      and cam["handoffs"] and all(h["within"] for h in cam["handoffs"])
                      and any(h["from"] == "cue:box-main" and h["to"] == "stage"
                              for h in cam["handoffs"])
                      and cam["rest"] and cam["rest"]["rested"] is True
                      and cam["rest"]["off"] <= cam["tol"]["rest"],
                      f"middle={mid['camera']} owner={cam['camera'] and cam['camera']['owner']} "
                      f"rest={cam['rest']} handoffs={cam['handoffs']} tolerances={cam['tol']} — "
                      f"the box publishes the pan its measured crease uses, the host applies that "
                      f"pose through the owned window, every handoff is continuous, and the zeroed "
                      f"door pose reaches rest")

                # ---- §4.4b: the handles reach the picture ----------------------------------------
                # READ AT THE MIDDLE OF THE HAND, and the reason is where the crease is. Over the
                # first sixth of the turn the crease stands outside the frame — the box's own edge
                # is a whole crop's width out — so nothing that lives ON the crease can be read
                # there. At the middle of the hand the crease crosses the frame and every one of
                # these handles has somewhere to show.
                shot = {}
                for name, extra in (("base", {}), ("axis", {"axis": 1}), ("depth", {"depth": 0.0}),
                                    ("dip", {"dip": 0.0}), ("lead", {"lead": 0.0}),
                                    ("fingers", {"fingers": 14}), ("shade", {"shade": 0.0}),
                                    ("travel", {"travel": 0.0}), ("seed", {"seed": 1.13})):
                    js(br, "return window.__offer(%s, {clock: 1.5, progress: 0.5});"
                       % json.dumps(box_score(**extra)))
                    br.sleep(0.7)
                    shot[name] = png(br, SHOTS / ("handle-" + name + ".png"))
                    br.evaluate("window.__cancel('handle row'); 0")
                    idle(br)
                moved = {k: diff(shot["base"], shot[k])
                         for k in ("axis", "depth", "dip", "lead", "fingers", "shade", "travel",
                                   "seed")}
                # TWO KINDS OF HANDLE, READ TWO WAYS. The turn's own four — which way the box turns,
                # how deep the perspective is, how far the eye rides and how far each face's picture
                # travels — move the WHOLE frame, and the mean of the frame is what reads them. The
                # four that live ON THE CREASE — the joint's depth, its count, the die that orders it
                # and the contact shadow — are a hairline along one edge by construction, so they are
                # read where they lie, on the worst channel, exactly as the module's own judged run
                # reads its shadow at «40.0 channels off the frame where it lies». Both are held to
                # the project's own seam threshold in their own reading.
                WIDE = ("axis", "depth", "dip", "travel")
                check(BROWSER_ROWS[20],
                      all((mn if k in WIDE else mx) > SEAM for k, (mn, mx) in moved.items()),
                      "; ".join(f"{k} moves the frame by {mn:.4f} of 255, worst channel {mx} "
                                f"({'the frame' if k in WIDE else 'where it lies'}, floor {SEAM})"
                                for k, (mn, mx) in moved.items())
                      + ". A handle a score drives and the picture ignores is what §4.4b is about")

                # ---- THE CHARTER'S OWN TEST: whose structure draws the boundary -------------------
                # The pardon is one clause and it has two halves, the boundary's shape and its place.
                # This is the place: with the crease on the departing work's own region line and with
                # it back on the box's own edge, read mid-turn and read at the door. The module's own
                # judged run reads 70.11 channels mid-turn and 0.00065 at the door; the numbers here
                # are this port's own, on this frame.
                crease(br, SEAM_AT, SEAM_SCORE)
                on_line = [host_shot(br, at, "crease-on-%03d" % round(at * 100))
                           for at in (0.0, 0.38, 0.5, 0.62, 1.0)]
                crease(br, SEAM_AT, 0.0)
                on_edge = [host_shot(br, at, "crease-off-%03d" % round(at * 100))
                           for at in (0.0, 0.38, 0.5, 0.62, 1.0)]
                crease_moved = [diff(a, b)[0] for a, b in zip(on_line, on_edge)]
                crease(br, SEAM_AT, SEAM_SCORE)
                seam_read = js(br, "window.__mix(0.5); return window.__values();")
                check(BROWSER_ROWS[21],
                      crease_moved[0] <= 0.02 and crease_moved[4] <= 0.02
                      and min(crease_moved[1:4]) > 1.0
                      and seam_read["seamMeasured"] is True
                      and abs(seam_read["seamAt"] - SEAM_AT) < 1e-9,
                      f"the departing work falls into two regions at {SEAM_AT} across the frame, and "
                      f"that split explains {SEAM_SCORE} of how its columns differ — over the "
                      f"module's own floor of 0.20, so it counts as a seam and the fold is placed on "
                      f"it. Putting the crease back on the box's own edge moves the frame by "
                      + ", ".join("%.4f" % x for x in crease_moved[1:4])
                      + f" of 255 through the turn and by {crease_moved[0]:.5f} and "
                        f"{crease_moved[4]:.5f} at the two doors. The module's own judged run reads "
                        f"70.11 mid-turn and 0.00065 at the door (lab/data/effects-new-check.txt). "
                        f"That is the charter's own test answered by measurement: what draws the "
                        f"boundary is the work, and what the solid does is fold along it")

                # ---- THE BOX, WALKED ON THE BUFFER -----------------------------------------------
                # The rows above photograph the face map and read it as colour. This one asks the
                # INSTRUMENT what it read for itself at the instant it was about to draw, on the grid
                # the shader samples on: how many of the buffer's own sample points stood with no
                # face on them, how much frame the tightest of them had to spare, and how far the
                # standing face stands from its own landing.
                def door_pose(mix=0, buf=None, **over):
                    p = {"mix": mix, "axis": 0, "depth": 0.9, "dip": 0.5, "lead": 0.5,
                         "fingers": 7, "seam": SEAM_AT, "seamScore": SEAM_SCORE, "shade": 1,
                         "travel": 1, "seed": DIE, "mask": 0, "reduced": False,
                         "cssWidth": VW, "cssHeight": VH}
                    p.update(over)
                    if buf:
                        p["bufWidth"], p["bufHeight"] = int(buf[0]), int(buf[1])
                    return p

                def values_of(p):
                    return js(br, "return window.__exPass.bench.values('boxfold', %s);" % json.dumps(p))

                grids = [(VW, VH), (VW * 2, VH * 2), (195, 422), (1440, 900), (40, 60)]
                walked = {}
                for mixv in (0, 1):
                    for axisv in (0, 1):
                        for g in grids:
                            walked[(mixv, axisv, g)] = values_of(
                                door_pose(mix=mixv, axis=axisv, buf=g))
                away = values_of(door_pose(mix=0.5, buf=grids[0]))
                on_css = values_of(door_pose())
                wrong = [k for k, v in walked.items()
                         if v["boxMap"] is None or v["boxMap"]["bare"] != 0
                         or v["boxMap"]["walked"] != 17 or v["boxMap"]["offPx"] >= 0.5
                         or v["boxMap"]["sparePx"] <= 0 or v["boxMap"]["crop"] != CROP
                         or v["doorWhyNo"] is not None or v["doorHeld"] is not None]
                one = walked[(0, 0, grids[0])]["boxMap"]
                check(BROWSER_ROWS[22],
                      not wrong and len(walked) == 20
                      and on_css["doorGrid"] == {"w": VW, "h": VH, "drawn": False, "given": True}
                      and walked[(0, 0, grids[0])]["doorGrid"] == {"w": VW, "h": VH, "drawn": True,
                                                                   "given": True}
                      and away["boxMap"] is None and away["doorGrid"] is None,
                      "%d readings — both doors, both axes, five grids from %s to %s — and every one "
                      "of them walked %d points of the buffer with %d bare, the tightest of them "
                      "with %.2f points of frame to spare and the standing face %.2e points from "
                      "its own landing, against a bar of half a point. Away from a door nothing is "
                      "read at all (grid %s), and nothing is ever held: a box's landing is exact by "
                      "construction, so a fault this reading finds is refused rather than closed. "
                      "The reading at the entry door on %s: %s"
                      % (len(walked), "%dx%d" % grids[0], "%dx%d" % grids[4],
                         one["walked"], one["bare"], one["sparePx"], one["offPx"],
                         away["doorGrid"], "%dx%d" % grids[1],
                         walked[(0, 0, grids[1])]["boxMap"]))

                # ---- THE JUDGES' HANDLE'S PUBLISHED DOOR CONTRACT, HELD AGAINST THE BOUNDARY JUST
                # ---- MEASURED, NOT AGAINST ITS OWN SOURCE TEXT -----------------------------------
                # A grep of the manifest's own field names beside the shader's declared numbers
                # proves only that both strings sit in the file. What the manifest actually promises
                # is a NUMBER — `points`, on the drawing buffer, against `landing`, with nothing
                # held — and that number is read here off the live manifest and set against the
                # twenty readings the search just took.
                contract = m["handles"]["mask"]["applied"]["readAtADoor"]
                worst_off = max(v["boxMap"]["offPx"] for v in walked.values())
                check(BROWSER_ROWS[25],
                      contract["points"] == 0.5
                      and contract["readOn"] == "the drawing buffer"
                      and contract["reads"] == "landing"
                      and contract["held"] is None
                      and all(v["boxMap"]["offPx"] < contract["points"] for v in walked.values())
                      and one["offPx"] < contract["points"],
                      f"the manifest publishes applied.readAtADoor={contract} on the judges' handle. "
                      f"Its own `points`, {contract['points']}, is the same bound every one of the "
                      f"{len(walked)} readings above stayed under — the worst of them at "
                      f"{worst_off:.2e} points — and the red-on-bug row below that removes the "
                      f"landing window shows what crossing it means: the same reading refuses the "
                      f"door the instant offPx reaches it. So the number the manifest promises is "
                      f"the number the door is actually held to, not a second copy that could read "
                      f"anything at all")

                # ---- THE DOOR REFUSED ON THE REAL TRANSACTION ROAD -------------------------------
                # The reading above comes out whole on every buffer this host can hand and every pose
                # these handles admit, which is the runtime truth this lane was asked for and not a
                # reason to leave the claim unread. The one door this instrument's own handles CAN
                # spoil is the judges' channel: `mask` draws the face map itself as colour, and a
                # score that leaves it open at a door hands the visitor a false-colour map of the two
                # faces instead of the photograph.
                def road(gen):
                    return js(br, "var r = window.__report(); return {state: r.state, "
                                  "drew: r.drew, buffer: r.census.buffer, "
                                  "refused: r.events.filter(function(e){ return e.gen === %d "
                                  "&& e.why && String(e.why).indexOf('door leaks') >= 0; })"
                                  ".map(function(e){ return e.name + ': ' + e.why; })};" % gen)

                br.evaluate("window.__cancel('door road row'); 0")
                idle(br)
                shut_gen = js(br, "return window.__offer(%s, {clock: 0, progress: 0});"
                              % json.dumps(box_score(mask=0)))["gen"]
                br.sleep(1.0)
                played = road(shut_gen)
                br.evaluate("window.__cancel('door road row'); 0")
                idle(br)
                open_gen = js(br, "return window.__offer(%s, {clock: 0, progress: 0});"
                              % json.dumps(box_score(mask=1)))["gen"]
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

                # ---- THE FIVE PARDON CONDITIONS, HELD AGAINST THE MEASUREMENTS ALREADY TAKEN -----
                # A grep of the file's own heading and its "three whole, one with the composer, one
                # with the host" sentence proves only that the sentence is there. Each of the five
                # already has a real measurement standing behind it, taken earlier in this same run;
                # this row reads those five back rather than the prose that describes them.
                check(BROWSER_ROWS[26],
                      # 1. THE FOLD ON THE WORK'S OWN LINE — with the composer: `seam` is a handle
                      # reading an outside measurement, and moving the crease off that line moves
                      # the frame (the charter row above, `seam_read`/`crease_moved`).
                      m["handles"]["seam"]["reads"].startswith("structure.regions from lab/cut-lines.py")
                      and seam_read["seamMeasured"] is True
                      and min(crease_moved[1:4]) > 1.0
                      # 2. THE FACES CARRY LIVE PICTURES RE-READ EVERY FRAME — the host's: this
                      # instrument is never seen holding more than the host's own two source
                      # textures, at census taken at the start and after ten runs.
                      and cen["textures"] == 2 == base_c["textures"] == after["textures"]
                      and cen["framebuffers"] == 0 == base_c["framebuffers"] == after["framebuffers"]
                      # 3. A CONTACT SHADOW ON EVERY EDGE — whole: `shade` moves the frame where the
                      # shadow lies, read on the worst channel exactly as BROWSER_ROWS[20] reads it
                      # (it is one of the four handles that live ON THE CREASE, not one of WIDE's
                      # four that move the whole frame).
                      and moved["shade"][1] > SEAM
                      # 4. THE CAMERA TRAVELS WITH TRUE PERSPECTIVE — whole: the two roads' own
                      # inverted projection agrees with the module's at both doors and six turns,
                      # while the instrument supplies the host with its measured pan.
                      and all(mn <= ROADS for _, mn, _ in agree)
                      and cam["camera"]["owner"] == "stage"
                      and cam["handoffs"] and all(h["within"] for h in cam["handoffs"])
                      # 5. IT LANDS EXACTLY — whole: the walk above found no fault to refuse.
                      and not wrong,
                      f"the fold's place is `seam`, reading an outside measurement "
                      f"({m['handles']['seam']['reads'][:44]}…); moving the crease off it moves the "
                      f"frame by {min(crease_moved[1:4]):.4f} of 255 at the least — the composer's "
                      f"own half. The census never shows more than the host's own two textures and "
                      f"zero framebuffers ({cen['textures']}/{cen['framebuffers']} at start, "
                      f"{after['textures']}/{after['framebuffers']} after ten runs) — the host's "
                      f"half. `shade` moves the frame by {moved['shade'][1]} worst channel where the "
                      f"shadow lies, the two roads' own perspective agrees to "
                      f"{max(mn for _, mn, _ in agree):.4f} of 255 worst case while its own camera "
                      f"pose is applied by the host, and the door walk above found nothing to refuse — "
                      f"the instrument's own three, whole")

                kept = sorted(p.name for p in SHOTS.glob("*.png"))
                check(BROWSER_ROWS[24],
                      len(kept) >= 40 and all((SHOTS / k).stat().st_size > 1000 for k in kept),
                      f"{len(kept)} captures under {SHOTS.relative_to(ROOT)}: the eight poses on "
                      f"both roads, their eight face maps, the ten crease readings, the two doors in "
                      f"a stack, the seven sampled instants, the frame after a resize, the two "
                      f"seeded runs and the nine handle runs")

    shutil.rmtree(BENCH, ignore_errors=True)

    # ================================================================================================
    # THE RED-ON-BUG PROOFS. Each reverts one rule this port states, in the artifact the browser
    # actually loads, and reads the number that moved. The pack served is changed and the host is
    # re-stamped with the digest of the bytes it is handed, which is what the build does; the file on
    # disk is never touched, so no working tree can be left changed by a proof.
    # ================================================================================================
    def worst_unclaimed(br, ats, at_seam=SEAM_AT, score=SEAM_SCORE):
        crease(br, at_seam, score)
        br.sleep(0.4)
        return max(unclaimed(face_map(br, at, "red-%03d" % round(at * 100))) for at in ats)

    def door_gap(br):
        crease(br)
        br.sleep(0.4)
        _, hp, _ = roads(br, 0.0, "red-door")
        ww = int(br.evaluate("String(document.querySelector('canvas[aria-hidden]').width)"))
        hh = int(br.evaluate("String(document.querySelector('canvas[aria-hidden]').height)"))
        v = js(br, "window.__mix(0); return window.__values();")
        return {"apart": apart(hp, work_in_the_frame(PHOTOS[0], ww, hh))[0],
                "offPx": v["boxMap"]["offPx"] if v["boxMap"] else None,
                "whyNo": v["doorWhyNo"]}

    def road_gap(br, at):
        crease(br)
        br.sleep(0.4)
        _, hp, mp = roads(br, at, "red-road")
        return list(diff(hp, mp))

    # ---- 1. the room the crease's travel needs, removed ----------------------------------------
    # The port's own one number, reverted in the artifact the browser loads: the box goes back to the
    # room the TURN alone needs, which is what the module carries, and the camera goes on sliding to
    # put the crease on the work's own line. The number that moves is the share of the frame no face
    # stands on — the very leak the room exists to close.
    MID = [0.3, 0.4, 0.5, 0.6, 0.7]
    base_fill = on_bench(lambda b: worst_unclaimed(b, MID, 0.75, 1.0))
    bug = PACK.replace("var SEAM_ROOM = 0.42;", "var SEAM_ROOM = 0;", 1)
    bug_fill = on_bench(lambda b: worst_unclaimed(b, MID, 0.75, 1.0), pack_text=bug)
    check(RED_ROWS[0],
          bug != PACK and base_fill is not None and bug_fill is not None
          and base_fill == 0.0 and bug_fill > 0.005,
          f"the box is built larger than the frame by the room the turn needs plus the room the "
          f"crease's travel needs. With the second room standing, the face map is unclaimed at "
          f"{base_fill * 100:.4f}% of the frame at the worst of five poses through the turn, with "
          f"the crease at the far end of the measurement's own window. With it taken out and the "
          f"camera still sliding, {bug_fill * 100:.2f}% of the frame stands with no face on it — "
          f"which at the bottom of a stack is the cleared buffer showing through a picture that told "
          f"the host it had no absence to publish")

    # ---- 2. the landing window removed ---------------------------------------------------------
    # Everything that moves through a quarter rides one sine over the quarter, and it is that sine at
    # its own zero which makes every landing exact. Take it off the crease's slide and the camera
    # arrives at the door still displaced: the door stops being the file, the instrument's own
    # reading measures the standing face off its landing, and the door is refused.
    base_door = on_bench(door_gap)
    bug = PACK.replace("var w = (seam.at - 0.5) * 2 * win;", "var w = (seam.at - 0.5) * 2;", 1)
    bug_door = on_bench(door_gap, pack_text=bug)
    check(RED_ROWS[1],
          bug != PACK and base_door and bug_door
          and base_door["apart"] <= SEAM and base_door["offPx"] < 0.5
          and base_door["whyNo"] is None
          and bug_door["apart"] > SEAM and bug_door["offPx"] >= 0.5
          and bug_door["whyNo"] and "away from its own landing" in bug_door["whyNo"],
          f"with the window standing, door 0 is {base_door['apart']:.4f} of 255 from its own file "
          f"and the instrument reads the standing face {base_door['offPx']:.2e} points from its "
          f"landing. With the window taken off the crease's slide the same door stands "
          f"{bug_door['apart']:.4f} of 255 from that file and the reading measures "
          f"{bug_door['offPx']:.2f} points of travel, on which it refuses the door: "
          f"«{bug_door['whyNo']}»")

    # ---- 3. the contact shadow removed ----------------------------------------------------------
    # The charter's third condition, reverted in the served bytes: the shadow that reads on every
    # edge is switched off in the port and left standing in the module, so the two roads part by
    # exactly what the shadow is worth on the frame where it lies.
    base_shadow = on_bench(lambda b: road_gap(b, 0.5))
    bug = PACK.replace("col *= 1.0 - SHADE * uTurn.w * lit * exp(-far / REACH);",
                       "col *= 1.0;", 1)
    bug_shadow = on_bench(lambda b: road_gap(b, 0.5), pack_text=bug)
    check(RED_ROWS[2],
          bug != PACK and base_shadow is not None and bug_shadow is not None
          and base_shadow[0] <= ROADS and base_shadow[1] <= SEAM
          and bug_shadow[1] > SEAM,
          f"a contact shadow reading on every edge is the third of the five conditions the charter "
          f"pardons the box under, and it is a hairline along one edge — so the two roads are read "
          f"where it lies, on the worst channel, as well as over the whole frame. With it standing "
          f"they agree at {base_shadow[0]:.4f} of 255 mid-turn with a worst channel of "
          f"{base_shadow[1]}; with it taken out of the served instrument and left standing in the "
          f"module they part at {bug_shadow[0]:.4f} of 255 with a worst channel of {bug_shadow[1]}, "
          f"against the project's own seam threshold of {SEAM}. The module's own judged run reads "
          f"the shadow as worth 40.0 channels of the frame where it lies")

    # ---- 4. the picture pasted on the face by one fixed rule -------------------------------------
    # The face's own square is (s, t) — `s` across the turn's plane, `t` along the crease — and
    # `posed`'s `pt` lays those two on the SCREEN by which way the crease lies. The picture has to be
    # pasted onto the face by the same decision, or a landed face stands the work turned. Reverted in
    # the served bytes to the one fixed rule this file carried until 2026-09-02, and the number that
    # moves is both flat-crease doors against their own files.
    FLAT_SWAP = '"  vec2 scA = uFlat > 0.5 ? stA.yx : stA;",'
    base_flat = on_bench(lambda b: flat_doors(b, *_bench_grid(b)))
    bug = PACK.replace(FLAT_SWAP, '"  vec2 scA = stA;",', 1)
    bug = bug.replace('"  vec2 scB = uFlat > 0.5 ? stB.yx : stB;",', '"  vec2 scB = stB;",', 1)
    bug_flat = on_bench(lambda b: flat_doors(b, *_bench_grid(b)), pack_text=bug)
    check(FLAT_DOOR_RED_ROW,
          bug != PACK and base_flat is not None and bug_flat is not None
          and all(mn <= SEAM for mn, _ in base_flat.values())
          and all(mn > SEAM for mn, _ in bug_flat.values()),
          "with the pasting following the crease, "
          + "; ".join(f"{t} stands {mn:.4f} of 255 from its own file"
                      for t, (mn, _) in sorted(base_flat.items()))
          + "; with it pasted by one fixed rule instead, "
          + "; ".join(f"{t} stands {mn:.4f} of 255 (worst channel {mx})"
                      for t, (mn, mx) in sorted(bug_flat.items()))
          + f", against the project's own seam threshold of {SEAM}. What the second reading is, "
            "said exactly: the work reflected about its own anti-diagonal — the frame's top-left "
            "corner reading the source's bottom-right and its bottom-right reading the source's "
            "top-left, the other two standing still — which is a mirrored photograph and not the "
            "work at all")


shutil.rmtree(TMP, ignore_errors=True)

ran = {name for name, _, _ in results}
for name in BROWSER_ROWS + RED_ROWS + [FLAT_DOOR_ROW, FLAT_DOOR_RED_ROW]:
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
