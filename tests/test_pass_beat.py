#!/usr/bin/env python3
"""PASS-API-V1 — the interfering instrument on the host's frame.
Run: python3 tests/test_pass_beat.py

Root: his word of 2026-08-18 08:58 — «перенеси ВЕСЬ арсенал и пересобери проход». The lab holds
23 effect modules and the engine held far fewer instruments, so the sameness a visitor sees on the
route is the port's fault. This file carries `lab/effects/beat.js` across and proves it.
docs/design/PASS-API-V1.md §7 (GPU and resources), §8 (the manifest) and §9's conformance rows 7, 9,
10, 13, 14, 15, 16 and 22 are what this file makes real; the lifecycle rows stay in
tests/test_pass_api.py and are untouched.

WHAT IS COMPARED, AND AGAINST WHAT.

  The doors. At the dial's two ends one whole work stands. Each is measured against ITS OWN FILE —
  the picture cover-fitted into the frame and pulled in by the headroom the counter-motion needs
  (the module's own ZOOM of 1.14, which its contract row publishes) — inside the project's seam
  threshold of 6 of 255. A door that carried a ten-thousandth of the other photograph would fail
  this, which is the point of it.

  The five poses. The host's frame is compared against the LAB MODULE's own frame, on one pose both
  roads were driven by: the same dial, the same five params, the same die, the same second. Two
  roads of one frame, never two guesses at one. The five poses walk the dial from door to door, so
  the response curve is measured along its whole length rather than at its ends.

  The shader. Every line of the module's own fragment shader is read out of the lab file and looked
  for, verbatim, in the built instrument. Three lines are known to differ and are named with their
  reasons; a fourth difference would redden this row.

  No empty frame. The module asks its own context to preserve the drawing buffer (beat.js:295) and
  §7 refuses that. The flag stood in for a redraw: the module draws on demand and needs the frame
  that was already there handed back between two draws. The host draws every frame and redraws on
  resize, so the rows below sample the pass at seven instants and once across a change of viewport,
  and each frame has to stand as a picture.

  The lab tree is READ ONLY and is found at $TLVPHOTOS_LAB_ROOT, defaulting to the immersive
  worktree's lab. Absent, every browser row here is a pinned SKIP that names the missing path —
  never a silent pass.
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

LAB = Path(os.environ.get("TLVPHOTOS_LAB_ROOT", "/Users/sashaabramovich/tlvphotos-immersive/lab"))
# The two photographs lab/carrier-check.py itself compares on; they live in the main worktree, which
# the immersive one does not copy. Either root is read only here.
PHOTOS = [Path("/Users/sashaabramovich/tlvphotos/lab/photos/towers.jpg"),
          Path("/Users/sashaabramovich/tlvphotos/lab/photos/glassgrid.jpg")]
MODULE = LAB / "effects" / "beat.js"

SITE_URL = "https://synth.example.com"
VW, VH = 390, 844          # the phone frame lab/carrier-check.py measures on
CLOCK = 7.0                # the second the comparison holds at, as the carrier's own check does
SEAM = 6.0                 # the project's seam threshold, 6 of 255 (TRANSITION-STAGE-V0 §1)
SAME = 1.5                 # two roads of one frame: the carrier check's own bar
FAR = 40.0                 # further than this from a file and it is a different work
# A frame that stands as a picture. The canvas's own background is one flat colour, so a drawn frame
# is far from it and carries a spread of its own. Both numbers are read off the capture.
BACKGROUND = (0x08, 0x08, 0x0a)
SPREAD = 10.0

ZOOM = 1 + 2 * 0.055 + 0.03      # the module's own crop, from its own AMP

# Captures are kept rather than swept, because §9 row 16 asks for evidence for every landed
# instrument and evidence that is deleted is no evidence.
SHOTS = ROOT / "tests" / "captures" / "pass-beat"

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


# ---------------------------------------------------------------- the score this instrument plays
# AUTHORED HERE, and said to be authored here. lab/data/scores carries a template and a table for
# the woven instrument alone, so there is no per-pair score on file for this one. Everything below
# is either a number the module itself declares or a field the contract requires; nothing is
# measured in this file and nothing is invented as a measurement.
DIE = 4.91016            # the die lab/data/scores' own weave score carries, so the suites roll one
TILT = 9                 # the angle the lab module pins (beat.js, BEAT_TILT) and the handle's rest
TILT_MIN, TILT_MAX = 1, 90       # the two ends the port publishes that angle between
P_MIN, P_MAX = 0.025, 0.33       # the module's own period span, in frame heights (beat.js)
DURATION_MS = 3000
WITHIN_MS = 500


def beat_score(pair_a="a", pair_b="b", **statics):
    """The score, with a track for every one of the eleven handles (§4.4b).

    The five params rest at the module's own declared defaults (beat.js:260-266): first period 0.14,
    second period 0.42, phase 0, beat contrast 0.82, lobe order 0.6. The three channels rest where
    the module rests them — the two judges' handles at 1 and the fleet's mask at 0. `mix` reads the
    transaction's own progress and `clock` the second the host hands down; that second is the only
    place the module ever read time, and it read its own accumulated frame clock there (beat.js:407).
    """
    P = {"periodA": 0.14, "periodB": 0.42, "phase": 0, "contrast": 0.82, "lead": 0.6,
         "beatTilt": TILT, "shade": 1, "travel": 1, "mask": 0, "seed": DIE}
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
        "intent": "two photographs are read as wave fields whose periods travel toward each other "
                  "and pass; where the two waves add the frame shows one work and where they "
                  "cancel the other, so the crossing happens in large slow lobes born of the two "
                  "works' own rhythms (lab/effects/beat.js:1-12, its own header)",
        "pair": {"a": pair_a, "b": pair_b},
        "seed": DIE,
        "duration": DURATION_MS,
        "direction": "a-to-b",
        "interruption": {"withinMs": WITHIN_MS, "resolve": "nearest-door"},
        "failLand": "arrive",
        "camera": {"owner": "stage", "rests": "b",
                   "track": [{"at": "b", "pan": {"x": 0, "y": 0}, "logScale": 0,
                              "pitch": 0, "yaw": 0, "roll": 0, "fov": None, "owner": "stage"}]},
        "cues": [{
            "id": "beat-main",
            "instrument": {"id": "beat", "api": 1},
            "voice": "letter",
            "roles": ["disassembly", "mystery", "assembly"],
            "levels": ["SURFACE"],
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
        "quality": {v: {"renderScale": None, "cues": {"beat-main": {"resources": res[v]}}}
                    for v in ("lean", "standard", "rich")},
        "provenance": {"source": "lab/effects/beat.js's own declared defaults and constants",
                       "measuredAt": None, "by": "tests/test_pass_beat.py"},
    }


# ---------------------------------------------------------------- bake once
build_site.SITE_CONFIG = dict(build_site.SITE_CONFIG)
build_site.SITE_CONFIG["pass"] = {"visualLayer": "pass", "diagnostics": "on"}

TMP = Path(tempfile.mkdtemp(prefix="synth_passbeat_"))
build_site.OUT = TMP
build_site.build(SITE_URL)
LAYER = (TMP / "pass-layer.js").read_text(encoding="utf-8")
# The instrument's own region of the BUILT file — the real artifact, comments stripped as it ships —
# which is what the ownership fence and every other string row below are read against. A row about
# the HOST reads LAYER; a row about this instrument's own mathematics reads its own file.
REGION = (TMP / "pass-inst-beat.js").read_text(encoding="utf-8")

# ---------------------------------------------------------------- string rows

OWNED = ["createElement", "getContext", "requestAnimationFrame", "addEventListener",
         "performance.now", "Date.now", "new Image", "setTimeout", "setInterval"]
held = [s for s in OWNED if s in REGION]
check("PASS-BEAT the instrument creates no context, no canvas, no loop and no listener",
      not held,
      "§1.2's fence, read against the instrument's own region of the file: none of the nine ways of "
      "owning hardware appears there, so the module's canvas, its WebGL 1 context, its frame loop "
      "and its resize listener all stayed in the lab"
      if not held else "the instrument's region holds " + ", ".join(held))

HANDLES = ["mix", "clock", "periodA", "periodB", "phase", "contrast", "lead", "beatTilt", "seed",
           "shade", "travel", "mask", "presence"]
check("PASS-BEAT every handle the instrument publishes is a handle a score can drive",
      all(("%s: { min" % h) in REGION for h in HANDLES),
      "§4.4b: twelve handles — the dial, the second, the module's own five declared params, the "
      "tilt the module pinned and this port publishes, its die, its two judge channels and the "
      "fleet's mask. The module's `photo` param does not cross: a cue carries an ORDERED pair and "
      "owes a door at each end, so which work stands where is the passage's question and never a "
      "handle")

# HIS 19:13 WORD, LIFTED TO THE CLASS AT 19:21: every geometric parameter derives from the work's
# own measured structure. The module pinned the angle its two gratings interfere at; the port
# publishes it and names, where a composer can read it, which reading of a work record fills it.
# A RANGE OF 0…1 IS A PLACE AND NOT A LENGTH. The composer holds the two works' own measured
# periods as spectralPeriodPx / frameSide — already a share of a frame — and cannot map that onto a
# handle whose range says nothing about what its ends mean. The span travels with the handle, BY
# REFERENCE to the two constants the mapping itself uses, so this file and a composer cannot come to
# hold different numbers for the ends. The row reads the reference rather than the digits, which is
# what makes it a one-home row: retyping 0.025 here would create the second home it exists to stop.
check("PASS-BEAT the two period handles publish the span in frame heights their values mean",
      "frameHeights: [P_MIN, P_MAX]," in REGION
      and REGION.count("frameHeights: [P_MIN, P_MAX],") == 2
      and 'paths: ["texture.spectralPeriodPx", "frameSide"],' in REGION
      and REGION.count('paths: ["texture.spectralPeriodPx", "frameSide"],') == 2
      and 'of: "the departing work"' in REGION and 'of: "the arriving work"' in REGION
      and "var P_MIN = 0.025, P_MAX = 0.33;" in REGION
      and "return P_MIN + (P_MAX - P_MIN) * clamp(v, 0, 1);" in REGION,
      "both handles carry `frameHeights` by reference to the very constants `periodOf` maps "
      "through, and each names which work it reads and by which paths — so a fill can place a "
      "measured period on the handle without a number being retyped anywhere")

check("PASS-BEAT the tilt the module pinned is published and names the measurement that fills it",
      "var TILT_MIN = 1, TILT_MAX = 90;" in REGION
      and "beatTilt: { min: TILT_MIN, max: TILT_MAX, def: BEAT_TILT" in REGION
      and 'paths: ["structure.ownDevice.angleDeg",' in REGION
      and '"structure.grid.angleDeg"]' in REGION
      and "var BEAT_TILT = 9;" in REGION,
      "the handle carries `reads` — of which works, by which paths, and how the two are put "
      "together — beside its own range, and rests at the module's own nine degrees so a score that "
      "names no track for it draws the module's own frame. The two paths are the order the "
      "composer's own `latticeAngleDeg` already reads them in")

check("PASS-BEAT the two fields' drift reads the handed-down second and no clock of its own",
      "var drift = (st.reduced ? 0 : num(st.t, 0)) * 0.035;" in REGION
      and "t: h.clock" in REGION
      and "raf" not in REGION,
      "beat.js:407 read `t`, its own accumulated frame time; here it is the `clock` handle, which "
      "is what makes the seeded repeat below mean anything")

check("PASS-BEAT the die arrives already folded and is rolled nowhere in the instrument",
      'source: "handle:seed"' in REGION and "Math.random" not in REGION
      and "seedFrom" not in REGION,
      "the module folded its die at creation with `seedFrom` and rolled a fresh one where a score "
      "named none (beat.js:210-215); the handle arrives folded here, exactly as the meshing and the "
      "material instruments take theirs, so nothing in this file rolls anything")

check("PASS-BEAT the manifest leaves the drawing buffer unpreserved",
      "gl: { preserveDrawingBuffer: false }" in REGION,
      "the module asks its own context for a preserved buffer (beat.js:295) and §7 refuses a "
      "manifest that asks for it; the redraw it stood in for is the host's own frame loop")

LABTXT = MODULE.read_text(encoding="utf-8") if MODULE.exists() else ""

check("PASS-BEAT the shader carries no version header of its own",
      "#version" not in REGION and (not LABTXT or "#version" not in LABTXT),
      "so the host's translator stamps the one header this shader needs and no second one arrives")


def numbers(text, pattern):
    m = re.search(pattern, text)
    return [float(x) for x in re.findall(r"-?\d+\.?\d*", m.group(1))] if m else []


lab_q = numbers(LABTXT, r"FEEL_Q = \[([^\]]+)\]")
port_q = numbers(REGION, r"FEEL_Q = \[([^\]]+)\]")
check("PASS-BEAT the response curve is carried digit for digit out of the lab module",
      len(lab_q) == 21 and lab_q == port_q
      and "FEEL_D0 = 0.055" in LABTXT and "FEEL_D0 = 0.055" in REGION,
      f"twenty-one shares and the dead band of 0.055 the module's contract row publishes, "
      f"unchanged: {len(port_q)} numbers matched, first {port_q[1] if len(port_q) > 1 else None}, "
      f"last held {port_q[-1] if port_q else None}")

# Each constant as the LAB module spells it and as the PORT spells it. Most are the same string; the
# ones that differ do so for one reason each and the row says which.
CONSTANTS = [
    ("var BEAT_TILT = 9;", "var BEAT_TILT = 9;",
     "the second grating's angle off the first — the number that keeps the two wave vectors apart "
     "where the two periods cross, so the frame holds a few large lobes instead of flipping whole"),
    ("var AMP = 0.055;", "var AMP = 0.055;", "how far the content travels, in frame heights"),
    ("var ZOOM = 1 + 2 * AMP + 0.03;", "var ZOOM = 1 + 2 * AMP + 0.03;",
     "and the crop that pays for it — 1.14, the number the contract row publishes"),
    ("var P_MIN = 0.025, P_MAX = 0.33;", "var P_MIN = 0.025, P_MAX = 0.33;",
     "the two ends of the period range: a fortieth of the frame to a third of it"),
    ("clamp(P.lead, 0, 1) * 0.9", "clamp(num(st.lead, 0), 0, 1) * 0.9",
     "the lobes' moments spread by nine tenths of the threshold's range; the handle is read off the "
     "pose here instead of the module's closure"),
    ("var reach = 1 + spread * 0.5 + 0.04;", "var reach = 1 + spread * 0.5 + MARGIN;",
     "how far past the field's range the threshold travels — a bare literal in the module and a "
     "NAMED constant in the port, because the door reading holds its own crossover against that "
     "very number and a number read in two places has to have one home"),
    ("var tau = -reach + 2 * reach * d;", "var tau = -reach + 2 * reach * d;",
     "the travelling threshold itself"),
    ("var travel = AMP * 4 * d * (1 - d);", "var travel = AMP * 4 * d * (1 - d);",
     "the counter-motion, widest in the middle and nothing at either door"),
    ("clamp(P.phase, 0, 1) * 0.25", "clamp(num(st.phase, 0), 0, 1) * 0.25",
     "a quarter of a cycle each way, which is half a cycle of the DIFFERENCE the envelope reads"),
    ("t * 0.035", "num(st.t, 0)) * 0.035",
     "the two fields drift into each other at this rate per second"),
    ("smoothstep(0, 0.09, d) * smoothstep(1, 0.91, d)",
     "smoothstep(0, 0.09, d) * smoothstep(1, 0.91, d)",
     "the contact shadow's gate: nothing at either door, where one work stands whole"),
]
missing_const = ([c for c, _, _ in CONSTANTS if LABTXT and c not in LABTXT]
                 + [c for _, c, _ in CONSTANTS if c not in REGION]
                 + ([] if "var MARGIN = 0.04;" in REGION else ["var MARGIN = 0.04;"]))
check("PASS-BEAT every constant stands at the number the lab module gives it",
      not missing_const and bool(LABTXT),
      "; ".join("%s — %s" % (c, why) for c, _, why in CONSTANTS) if not missing_const and LABTXT
      else "these differ: " + ", ".join(missing_const or ["the lab module is absent"]))

# THE SHADER, LINE FOR LINE. The module's own fragment shader is an array of string literals; every
# one of them is looked for verbatim in the built instrument. Three lines are known to differ and
# they are listed here with their reasons — a fourth difference reddens this row rather than passing
# unnoticed, which is what «carried character for character» has to mean to be worth saying.
CHANGED = {
    "uniform float uAspect;":
        "the module hands the frame's aspect in as its own uniform, computed from the drawing "
        "buffer it owned; the host owns the buffer here and already binds its size, so the aspect "
        "is derived from `uRes` inside the shader",
    "  gl_FragColor = vec4(col, 1.0);":
        "the module had no stack to lie under and wrote a flat alpha; §7's coverage law asks for "
        "the arriving work's own share, which is the mask the shader already built: `1.0 - cov`",
}
# THE FIFTH ADDED LINE AND THE FOURTH'S NEW SHAPE arrived with the entry-door contract on
# 2026-08-25 (docs/design/ENTRY-DOOR.md). `uPresence` is the reserved dry every instrument that may
# stand OVER another now declares: at nothing it draws no pixel anywhere, so a voice can join a
# running picture without replacing it, and at whole — where it rests — it draws exactly what it
# always drew. The alpha the port already wrote is gated by it, which is the whole of the change to
# this shader's mathematics: nothing else in the line moved.
ADDED = ["  float uAspect = uRes.x / max(uRes.y, 1.0);",
         "uniform float uMask;",
         "  col = mix(col, vec3(cov), uMask);",
         "uniform float uPresence;",
         "  gl_FragColor = vec4(col, (1.0 - cov) * uPresence);"]
lab_frag = re.search(r"var FRAG = \[(.*?)\]\.join", LABTXT, re.S) if LABTXT else None
lab_lines = []
for _raw in (lab_frag.group(1).split("\n") if lab_frag else []):
    # Each element of the module's shader array is one string literal, sometimes trailed by a
    # comment of its own. The match is anchored at the leading quote and stops at the first
    # unescaped closing one, so a comment carrying an apostrophe cannot swallow the next line.
    _m = re.match(r"'((?:[^'\\]|\\.)*)'", _raw.strip())
    if _m:
        lab_lines.append(_m.group(1).replace("\\'", "'"))
carried = [ln for ln in lab_lines if ln not in CHANGED]
lost = [ln for ln in carried if ln not in REGION]
absent_add = [ln for ln in ADDED if ln not in REGION]
check("PASS-BEAT every line of the module's own shader is carried verbatim but the three named",
      bool(lab_lines) and not lost and not absent_add,
      f"{len(carried)} of the module's {len(lab_lines)} shader lines stand in the built instrument "
      f"unchanged; the two that do not are «" + "», «".join(CHANGED) + "» — "
      + "; ".join(CHANGED.values()) + f" — and the five lines that replace them are all present"
      if lab_lines and not lost and not absent_add
      else f"lines the port lost: {lost}; lines the port never added: {absent_add}")

# THE MEASUREMENT THE PERIODS ARE READ AGAINST AT A DOOR, published in the manifest. His 19:13 word,
# lifted to the class at 19:21: every geometric parameter names the measurement of the work it reads.
check("PASS-BEAT the handle that sets the field's steepness publishes its door's own measurement",
      'heldWholeAtADoor: { gratings: DOOR_HOLD,' in REGION
      and 'reads: "periodRequestA"' in REGION
      and "var MARGIN = 0.04;" in REGION
      and "var DOOR_HOLD = 2;" in REGION,
      "the handle carries `applied.heldWholeAtADoor` — what is read, on which grid, how far the "
      "hold reaches and where the request stays on the record — beside its own range")

SUITS = REGION.split("suits: {")[1].split("readiness")[0] if "suits: {" in REGION else ""
check("PASS-BEAT the manifest publishes what this instrument cuts on and how a pair suits it",
      'cuts: ["strip", "scale"]' in REGION
      and 'reads: ["texture.spectralPeriodPx", "frameSide"]' in REGION
      and bool(SUITS) and "floor" not in SUITS and "refus" not in SUITS
      and "minimum" not in SUITS and "threshold" not in SUITS,
      "his word of 2026-08-18 09:51 and 09:53 and charter shelf 10: near-matched rhythms RANK this "
      "shelf high for a pair and never admit it, so the block reads and never refuses — no floor, "
      "no minimum and no word that could turn a pair away stands in it")

check("PASS-BEAT the host binds uniforms by declared name, never by position or a written list",
      "getUniformLocation(p, u.name)" in LAYER and "gl.uniform1f(U.uTau" not in LAYER
      and "gl.uniform2f(U.uKA" not in LAYER,
      "the host reads the manifest; no list of this instrument's names is written into it")

# Every uniform the manifest declares is a name the shader actually spells, and the other way about.
declared = set(re.findall(r'\{ name: "(u\w+)", type:', REGION))
spelled = set(re.findall(r'uniform \w+ (u\w+);', REGION))
check("PASS-BEAT the manifest's declared names and the shader's own names are one set",
      declared == spelled and len(declared) == 17,
      f"{len(declared)} declared, {len(spelled)} spelled; "
      f"declared only: {sorted(declared - spelled)}; spelled only: {sorted(spelled - declared)}")

# ---------------------------------------------------------------- browser rows

BROWSER_ROWS = [
    "PASS-BEAT §8     · the manifest carries every field the contract names, in its shape",
    "PASS-BEAT row 7  · door 0 stands the departing work, measured against its own file",
    "PASS-BEAT row 7  · door 0 carries no trace of the arriving work",
    "PASS-BEAT row 7  · door 1 stands the arriving work, measured against its own file",
    "PASS-BEAT row 7  · door 1 carries no trace of the departing work",
    "PASS-BEAT the host's frame and the lab module's frame agree at all five poses",
    "PASS-BEAT §7     · no empty frame at any sampled instant of the pass",
    "PASS-BEAT §7     · the frame after a change of viewport is drawn, not a kept buffer",
    "PASS-BEAT row 10 · a seeded run repeats to the pixel",
    "PASS-BEAT row 14 · textures, programmes and framebuffers return to their baseline after ten runs",
    "PASS-BEAT row 15 · the console stays clean",
    "PASS-BEAT row 22 · the census shows granted against declared, and neither overruns",
    "PASS-BEAT §7     · a manifest asking for a preserved drawing buffer is refused, with its reason",
    "PASS-BEAT §7     · a uniform bound to a name the shader lacks is refused, with its reason",
    "PASS-BEAT §7     · one canvas, one context, two source textures, one pass a frame",
    "PASS-BEAT §7     · a shader already at GLSL ES 3.00 receives no second version header",
    "PASS-BEAT the real transaction road: curtain up, one pass drawn, exactly one dock at the end",
    "PASS-BEAT row 9  · one camera authority through a real pass, and the pose rests on the arrival",
    "PASS-BEAT §4.4b  · the five declared params and the published tilt each reach the PICTURE",
    "PASS-BEAT §4.4b  · the die, the two judge channels and the fleet's mask each reach the PICTURE",
    "PASS-BEAT §4.4b  · the handed-down second moves the two fields, and a pinned second repeats",
    "PASS-BEAT row 16 · the captures are kept as evidence",
    "PASS-BEAT the span the period handles publish is the span the instrument actually draws through",
    "PASS-BEAT the door is read on the DRAWING BUFFER, and the grating the door is held at is published",
    "PASS-BEAT a door no whole grating can close is refused on the real road, and the visitor still lands",
]

RED_ROWS = [
    "PASS-BEAT red-on-bug · the door reading removed: a door the buffer cannot keep whole is drawn",
    "PASS-BEAT red-on-bug · the phase pushed both fields one way: the phase handle stops reaching",
    "PASS-BEAT red-on-bug · the tilt pinned back to the module's constant: the pair stops setting it",
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
    """How far a capture stands from the canvas's own flat background, and how much spread it
    carries of its own. A frame that was never drawn is the background and has neither."""
    from PIL import Image, ImageChops, ImageStat
    a = Image.open(p).convert("RGB")
    flat = Image.new("RGB", a.size, BACKGROUND)
    st = ImageStat.Stat(ImageChops.difference(a, flat))
    own = ImageStat.Stat(a)
    return sum(st.mean) / 3.0, sum(own.stddev) / 3.0


def work_in_the_frame(src, w, h, zoom):
    """The work as the instrument seats it: cover-fit, then the centre crop the counter-motion is
    paid for with (the module's own ZOOM). The very same construction lab/carrier-check.py uses, so
    the two checks judge a door the same way."""
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
    """The bench's own served root: the BUILT pass-layer.js (the real artifact, namespace applied
    and comments stripped), the lab module unchanged, the two photographs, and the page that stands
    the two roads of one frame side by side.

    A row proving a rule reds hands over a CHANGED instrument file and writes the site's own record
    with the digest of the bytes actually served, which is what the build does. The source file on
    disk is never touched, so nothing has to be restored and no working tree can be left changed by
    a red-on-bug proof."""
    d = Path(tempfile.mkdtemp(prefix="synth_beatbench_"))
    pack = REGION if pack_text is None else pack_text
    shutil.copy2(TMP / "pass-layer.js", d / "pass-layer.js")
    # Each instrument travels as its own file and the host learns every address from the site's own
    # settings record, so the bench root serves that record and the files it names — the same files
    # a visitor is served, unaltered.
    for _inst in sorted(TMP.glob("pass-inst-*.js")):
        shutil.copy2(_inst, d / _inst.name)
    (d / "pass-inst-beat.js").write_text(pack, encoding="utf-8")
    record = json.loads((TMP / "config.json").read_text(encoding="utf-8"))
    record["pass"]["instruments"]["beat"]["digest"] = hashlib.sha256(
        pack.encode("utf-8")).hexdigest()
    (d / "config.json").write_text(json.dumps(record), encoding="utf-8")
    shutil.copy2(MODULE, d / "beat.js")
    (d / "photos").mkdir()
    for p in PHOTOS:
        shutil.copy2(p, d / "photos" / p.name)
    shutil.copy2(ROOT / "tests" / "fixture_pass_beat.html", d / "index.html")
    return d


def ready(br, tries=60):
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
    SCORE_JSON = json.dumps(beat_score())
    with serve(BENCH) as base:
        with Browser(width=VW, height=VH) as br:
            br.navigate(base + "/index.html")
            if not ready(br):
                for r in BROWSER_ROWS:
                    skip(r, "the bench never came up: "
                         + br.evaluate("JSON.stringify(window.__errs||[])"))
            elif not js(br, "return !!window.__exPass.bench.manifest('beat');"):
                why = js(br, "var e = window.__host.report().events.filter(function(x){"
                             "return x.name === 'manifest-refused';});"
                             "return e.length ? e[e.length - 1].why : null;")
                for r in BROWSER_ROWS:
                    check(r, False, "the host registered no «beat» instrument: " + str(why))
            else:
                # ---- §8: the manifest, read off the registered instrument -----------------------
                m = js(br, "return window.__exPass.bench.manifest('beat');")
                zoom = m["framings"]["0"]["coverCrop"]
                res = m["resources"]
                shape = (
                    m["id"] == "beat" and m["api"] == 1 and m["arity"] == 2
                    and m["roles"] == ["disassembly", "mystery", "assembly"]
                    and m["levels"] == ["SURFACE"]
                    and m["cuts"] == ["strip", "scale"]
                    and sorted(m["params"]) == ["beatTilt", "contrast", "lead", "periodA",
                                                "periodB", "phase"]
                    and len(m["handles"]) == 13
                    and m["handles"]["beatTilt"]["def"] == TILT
                    and m["handles"]["beatTilt"]["min"] == TILT_MIN
                    and m["handles"]["beatTilt"]["max"] == TILT_MAX
                    and m["handles"]["beatTilt"]["reads"]["paths"] == [
                        "structure.ownDevice.angleDeg", "structure.grid.angleDeg"]
                    and m["handles"]["periodA"]["frameHeights"] == [P_MIN, P_MAX]
                    and m["handles"]["periodB"]["frameHeights"] == [P_MIN, P_MAX]
                    and m["handles"]["periodA"]["reads"]["of"] == "the departing work"
                    and m["handles"]["periodB"]["reads"]["of"] == "the arriving work"
                    and all(set(h) >= {"min", "max", "def"} for h in m["handles"].values())
                    and m["neutrals"] == {"a": 0, "b": 1}
                    and m["doors"]["in"]["handle"] == "mix" and m["doors"]["in"]["value"] == 0
                    and m["doors"]["out"]["handle"] == "mix" and m["doors"]["out"]["value"] == 1
                    and sorted(m["framings"]) == ["0", "1"]
                    and m["framings"]["0"] == m["framings"]["1"]
                    and abs(zoom - ZOOM) < 1e-12
                    and m["camera"] == {"needs": "none", "authority": "stage"}
                    and m["coverage"]["writes"] is True
                    and len(m["passes"]) == 1 and len(m["passes"][0]["uniforms"]) == 17
                    and sorted(res) == ["lean", "rich", "standard"]
                    and all("bytesEstimate" in res[v] and res[v]["programs"] == 1
                            and res[v]["passes"] == 1 and res[v]["textureSlots"] == 2
                            for v in res)
                    and m["capabilities"] == ["webgl2"] and m["decline"]
                    and m["provenance"]["labPath"] == "lab/effects/beat.js"
                    and m["provenance"]["commit"] == "e0f1b91"
                    and m["suits"]["reads"] == ["texture.spectralPeriodPx", "frameSide"]
                    and m["suits"]["how"]
                    and m["readiness"] == "production-ready"
                    and "beat" in js(br, "return window.__host.report().registered;"))
                check(BROWSER_ROWS[0], shape,
                      f"twelve handles, sixteen uniforms in one pass, the crop {zoom} the "
                      f"counter-motion's headroom is paid for with, cuts {m.get('cuts')}, resources "
                      f"declared for three tiers with a byte estimate of "
                      f"{res['standard']['bytesEstimate']}, and the lab commit "
                      f"{m['provenance']['commit']}")

                br.evaluate("window.__clock(%r); 0" % CLOCK)
                br.sleep(0.9)

                # ---- the five poses: the host's frame beside the lab module's -------------------
                pairs = []
                for name, v in (("door-0", 0.0), ("q1", 0.25), ("mid", 0.5),
                                ("q3", 0.75), ("door-1", 1.0)):
                    br.evaluate("window.__mix(%r); 0" % v)
                    br.sleep(0.9)
                    br.evaluate("window.__hostDraw(); 0")
                    br.sleep(0.1)
                    br.evaluate("window.__show('host'); 0")
                    br.sleep(0.2)
                    ph = png(br, SHOTS / (name + "-host.png"))
                    br.evaluate("window.__show('module'); 0")
                    br.sleep(0.2)
                    pm = png(br, SHOTS / (name + "-module.png"))
                    pairs.append((name, ph, pm))

                shots = {n: h for n, h, _ in pairs}
                w = int(br.evaluate("String(window.__exPass.bench.make() && "
                                    "document.querySelector('canvas').width)"))
                h = int(br.evaluate("String(document.querySelector('canvas').height)"))
                towers = work_in_the_frame(BENCH / "photos" / "towers.jpg", w, h, zoom)
                glass = work_in_the_frame(BENCH / "photos" / "glassgrid.jpg", w, h, zoom)

                for i, (door, own, other, ownn, othern) in enumerate((
                        ("door-0", towers, glass, "towers.jpg", "glassgrid.jpg"),
                        ("door-1", glass, towers, "glassgrid.jpg", "towers.jpg"))):
                    a, amx = apart(shots[door], own)
                    check(BROWSER_ROWS[1 + i * 2], a <= SEAM,
                          f"{door} against {ownn}: mean {a:.4f} of 255 (threshold {SEAM}), worst "
                          f"channel {amx}")
                    o, _ = apart(shots[door], other)
                    check(BROWSER_ROWS[2 + i * 2], o >= FAR,
                          f"{door} against {othern}: mean {o:.4f} of 255 (must exceed {FAR})")

                agree = [(name, ) + diff(ph, pm) for name, ph, pm in pairs]
                check(BROWSER_ROWS[5], all(mn <= SAME for _, mn, _ in agree),
                      "; ".join(f"{n}: mean {mn:.4f} of 255 (threshold {SAME}), worst channel {mx}"
                                for n, mn, mx in agree))

                # ---- §7: no empty frame, and the redraw the preserved buffer stood in for -------
                br.evaluate("window.__show('host'); 0")
                empties = []
                for at in (0.0, 0.15, 0.3, 0.5, 0.7, 0.85, 1.0):
                    js(br, "return window.__offer(%s, {clock: 1.5, progress: %r});"
                       % (SCORE_JSON, at))
                    br.sleep(0.5)
                    p = png(br, SHOTS / ("instant-%03d.png" % round(at * 100)))
                    empties.append((at, ) + standing(p))
                    br.evaluate("window.__cancel('instant sweep'); 0")
                    idle(br)
                check(BROWSER_ROWS[6],
                      all(d >= FAR and s >= SPREAD for _, d, s in empties),
                      "; ".join(f"at {at}: {d:.2f} from the background, spread {s:.2f}"
                                for at, d, s in empties)
                      + f" (bars: {FAR} and {SPREAD})")

                js(br, "return window.__offer(%s, {clock: 1.5, progress: 0.5});" % SCORE_JSON)
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
                check(BROWSER_ROWS[7],
                      d >= FAR and s >= SPREAD and sized["pdb"] is False,
                      f"after the viewport moved to {VW - 80}x{VH - 120} the buffer reads "
                      f"{sized['buffer']} and the frame stands {d:.2f} from the background with a "
                      f"spread of {s:.2f}; the context keeps preserveDrawingBuffer={sized['pdb']}")

                # ---- the seeded repeat -----------------------------------------------------------
                took = js(br, "return window.__offer(%s, {clock: 1.5, progress: 0.5});" % SCORE_JSON)
                br.sleep(0.9)
                first = png(br, SHOTS / "seeded-1.png")
                rep1 = js(br, "return window.__report();")
                br.evaluate("window.__cancel('between runs'); 0")
                idle(br)
                js(br, "return window.__offer(%s, {clock: 1.5, progress: 0.5});" % SCORE_JSON)
                br.sleep(0.9)
                second = png(br, SHOTS / "seeded-2.png")
                mn, mx = diff(first, second)
                check(BROWSER_ROWS[8], took["took"] and mn == 0.0 and mx == 0,
                      f"took={took['took']} two runs of one seeded score: mean {mn} worst channel {mx}")

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
                check(BROWSER_ROWS[9], same,
                      f"before={base_c['textures']}/{base_c['programs']}/{base_c['framebuffers']} "
                      f"after ten runs={after['textures']}/{after['programs']}/{after['framebuffers']} "
                      f"(textures/programmes/framebuffers)")

                errs = json.loads(br.evaluate("JSON.stringify(window.__errs||[])"))
                check(BROWSER_ROWS[10], not errs, "; ".join(errs)[:200])

                # ---- the census against the declaration ------------------------------------------
                r = js(br, "return window.__report();")["resources"]
                check(BROWSER_ROWS[11],
                      r["declared"] and r["over"] is False
                      and r["granted"]["textures"] == r["declared"]["textures"]
                      and r["granted"]["framebuffers"] == r["declared"]["framebuffers"]
                      and r["granted"]["bytes"] == r["declared"]["bytesEstimate"],
                      f"declared={r['declared']} granted={r['granted']}")

                # ---- the two manifest refusals ---------------------------------------------------
                STUB = ("{dial:0,tau:-1.06,spread:0.54,kA:[0,14.7],kB:[1.02,6.45],"
                        "lobes:7,periodA:0.0677,periodB:0.1531,phase:[0,0],dphase:0,"
                        "contrast:0.82,off:0,guard:0}")
                r = js(br, """
                  var m = JSON.parse(JSON.stringify(window.__exPass.bench.manifest('beat')));
                  m.gl.preserveDrawingBuffer = true;
                  var ok = window.__exPass.bench.register({name:'beat-preserve', manifest:m,
                      values:function(){return %s;},
                      fit:function(){return [1,1,0,0];},
                      prepare:function(){return {take:false};}, start:function(){}, frame:function(){}});
                  var evs = window.__host.report().events.filter(function(e){return e.name==='manifest-refused';});
                  return {ok: ok, why: evs.length ? evs[evs.length-1].why : null,
                          registered: window.__host.report().registered};
                """ % STUB)
                check(BROWSER_ROWS[12],
                      r["ok"] is False and r["why"] and "preserved" in r["why"]
                      and "beat-preserve" not in r["registered"],
                      f"registered={r['ok']} why={r['why']}")

                r = js(br, """
                  var m = JSON.parse(JSON.stringify(window.__exPass.bench.manifest('beat')));
                  m.passes[0].uniforms.push({name:'uPointer', type:'vec2', source:'pointer'});
                  var ok = window.__exPass.bench.register({name:'beat-pointer', manifest:m,
                      values:function(){return %s;},
                      fit:function(){return [1,1,0,0];},
                      prepare:function(){return {take:false};}, start:function(){}, frame:function(){}});
                  var evs = window.__host.report().events.filter(function(e){return e.name==='manifest-refused';});
                  return {ok: ok, why: evs.length ? evs[evs.length-1].why : null,
                          registered: window.__host.report().registered};
                """ % STUB)
                check(BROWSER_ROWS[13],
                      r["ok"] is False and r["why"] and "uPointer" in r["why"]
                      and "cannot supply" in r["why"] and "beat-pointer" not in r["registered"],
                      f"registered={r['ok']} why={r['why']}")

                # ---- the hardware, counted where each thing is made ------------------------------
                js(br, "return window.__offer(%s, {clock: 1.0, progress: 0.4});" % SCORE_JSON)
                br.sleep(0.6)
                cen = js(br, "return window.__report();")["census"]
                check(BROWSER_ROWS[14],
                      cen["canvases"] == 1 and cen["contexts"] == 1 and cen["textures"] == 2
                      and cen["passesLastFrame"] == 1 and cen["framebuffers"] == 0
                      and cen["preserveDrawingBuffer"] is False
                      and int(br.evaluate("String(document.querySelectorAll('canvas').length)")) == 2,
                      f"census={cen}; the second canvas on the page is the lab module's own, which "
                      f"is the road being compared against and no part of the host")

                # ---- the version header, through the host's own translator -----------------------
                r = js(br, """
                  var m = window.__exPass.bench.manifest('beat');
                  var plain = window.__exPass.bench.es3(m.passes[0].frag, false);
                  var already = window.__exPass.bench.es3('#version 300 es\\n' + m.passes[0].frag, false);
                  var count = function (s) { return s.split('#version').length - 1; };
                  return {source: count(m.passes[0].frag), stamped: count(plain),
                          untouched: count(already),
                          head: plain.slice(0, 15)};
                """)
                check(BROWSER_ROWS[15],
                      r["source"] == 0 and r["stamped"] == 1 and r["untouched"] == 1
                      and r["head"].startswith("#version 300 es"),
                      f"the module's own shader carries {r['source']} headers, the translator leaves "
                      f"it with {r['stamped']}, and a source that already carries one comes back "
                      f"with {r['untouched']}")

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
                             "events: window.__report().events.map(function(e){return e.name;}).slice(-6)};")
                check(BROWSER_ROWS[16],
                      took["took"] and mid["state"] == "running" and mid["curtains"][:1] == [True]
                      and end["state"] == "idle" and len(end["docks"]) == 1
                      and end["curtains"][-1] is False and "docked" in end["events"],
                      f"mid={mid} end={end}")

                # ---- row 9: the camera through the whole pass ------------------------------------
                cam = js(br, "var r = window.__report(); "
                             "return {camera: r.camera, rest: r.rest, handoffs: r.handoffs, "
                             "tol: r.camTolerances};")
                check(BROWSER_ROWS[17],
                      cam["camera"] and cam["camera"]["owner"] == "stage"
                      and cam["handoffs"] == []
                      and cam["rest"] and cam["rest"]["rested"] is True
                      and cam["rest"]["off"] <= cam["tol"]["rest"],
                      f"owner={cam['camera'] and cam['camera']['owner']} rest={cam['rest']} "
                      f"handoffs={cam['handoffs']} tolerances={cam['tol']} — the manifest asks for "
                      f"no camera, so the stage holds it for the whole pass")

                # ---- §4.4b: the handles reach the picture ----------------------------------------
                # A handle read back off the diagnostic surface proves the GRAPH evaluated it. It
                # says nothing about whether the instrument obeyed it. These runs differ by exactly
                # one handle each and are photographed, so a picture that did not move is a handle
                # the instrument is not reading.
                br.evaluate("window.__show('host'); 0")

                def handle_shot(name, extra, clock=1.5, at=0.5):
                    js(br, "return window.__offer(%s, {clock: %r, progress: %r});"
                       % (json.dumps(beat_score(**extra)), clock, at))
                    br.sleep(0.7)
                    p = png(br, SHOTS / ("handle-" + name + ".png"))
                    br.evaluate("window.__cancel('handle row'); 0")
                    idle(br)
                    return p

                base_shot = handle_shot("base", {})
                # EACH HANDLE WALKED FROM ITS OWN LO DOOR TO ITS OWN HI DOOR, which is the very
                # measurement the module's contract row publishes for it
                # (lab/data/module-contract-new.json, `beat`.measured.handles.<k>.doorDistance: the
                # two ends of a handle and the distance between the frames they draw). Walking from
                # a default to one end instead reads the half of that distance the default happens
                # to stand on, and for the two periods at mid-passage that half is a change
                # concentrated in one broad band — a worst channel of 228 sitting under a mean of
                # 4.9 — which the mean of the whole frame under-reports. The doors are the handle's
                # own statement of its range and no number is chosen here.
                PARAM_DOORS = {"periodA": (0, 1), "periodB": (0, 1), "phase": (0, 1),
                               "contrast": (0, 1), "lead": (0, 1),
                               # the tilt the module pinned: a right angle apart against nearly
                               # collinear is the widest this handle reaches, and it is the row
                               # that says the published angle is wired to the picture rather
                               # than only declared in the manifest
                               "beatTilt": (TILT_MIN, TILT_MAX)}
                moved = {}
                for k, (lo, hi) in PARAM_DOORS.items():
                    moved[k] = diff(handle_shot(k + "-lo", {k: lo}),
                                    handle_shot(k + "-hi", {k: hi}))
                check(BROWSER_ROWS[18],
                      all(mn > SEAM for mn, _ in moved.values()),
                      "; ".join(f"{k} between its own two doors moves the frame by {mn:.4f} of 255 "
                                f"(worst channel {mx})" for k, (mn, mx) in moved.items())
                      + f"; the seam threshold is {SEAM}")

                # The die and the three channels. The die rolls the four-tenths of each lobe's own
                # moment that is chance, so it moves a share of the frame rather than all of it; the
                # two judges' handles switch off the contact shadow and the counter-motion, which
                # live at the boundary; and the mask paints the coverage in place of the picture.
                # Each is asked for the movement it actually claims: the mask for the whole frame,
                # the other three for a frame that is not the one they rest at.
                chan = {k: diff(base_shot, handle_shot(k, {k: v}))
                        for k, v in (("seed", DIE + 3.0), ("shade", 0), ("travel", 0), ("mask", 1))}
                check(BROWSER_ROWS[19],
                      all(mx > 0 and mn > 0 for mn, mx in chan.values())
                      and chan["mask"][0] > SEAM,
                      "; ".join(f"{k} moves the frame by {mn:.4f} of 255 (worst channel {mx})"
                                for k, (mn, mx) in chan.items())
                      + f"; the mask is held to the seam of {SEAM} and the other three to a frame "
                      f"that moved at all, which is what a boundary-width channel claims")

                # The clock. The two fields drift into each other on the handed second, so another
                # second is another frame; the same second twice is the same frame to the pixel.
                clock_a = handle_shot("clock-a", {}, clock=1.5)
                clock_b = handle_shot("clock-b", {}, clock=6.1)
                clock_a2 = handle_shot("clock-a2", {}, clock=1.5)
                cmn, cmx = diff(clock_a, clock_b)
                rmn, rmx = diff(clock_a, clock_a2)
                check(BROWSER_ROWS[20], cmn > SEAM and rmn == 0.0 and rmx == 0,
                      f"the second moved from 1.5 to 6.1 and the frame moved {cmn:.4f} of 255 "
                      f"(worst channel {cmx}); the same second twice reads {rmn} — the module's own "
                      f"contract row measures 33.43 for that same second")

                # ---- THE GRID THE DOOR IS READ ON --------------------------------------------
                # The rows above read every door on the frame the suite runs at. The shader samples
                # on the DRAWING BUFFER — the CSS frame times the device ratio times the host's own
                # resolution step — and the mask's crossover is HALF THE FIELD'S SLOPE PER BUFFER
                # ROW wide, so the buffer is the grid that decides a door. This row states one pair
                # of periods the CSS frame calls whole and a short buffer does not, and asks three
                # things of the instrument: that it sees what the buffer has, that it steps to the
                # nearest coarser whole grating whose door is whole THERE, and that the score's own
                # request stays on the record beside the periods applied.
                #
                # THE PERIODS ARE READ AT THE RAW SUM'S OWN END OF THE CONTRAST HANDLE, and that is
                # the physics rather than a convenience: at contrast 1 the cut belongs to the slow
                # envelope, whose slope is the DIFFERENCE of the two wave vectors and is small; at
                # contrast 0 it belongs to the raw sum of two fine gratings, which is the steepest
                # this field ever gets. So the door's own edge case lives at contrast 0, and that is
                # where it is stated.
                FINE = 0.06                      # both fields at 23.1 gratings across the height
                APPLIED = 0.0670637              # the same fields at 22, which the hold steps to

                def door_pose(pa, pb=None, mix=0, buf=None, over=None):
                    p = {"mix": mix, "periodA": pa, "periodB": pa if pb is None else pb,
                         "phase": 0, "contrast": 0.0, "lead": 0.6, "beatTilt": TILT,
                         "shade": 1, "travel": 1, "mask": 0, "seed": DIE, "t": 0, "reduced": False,
                         "cssWidth": VW, "cssHeight": VH}
                    if buf:
                        p["bufWidth"], p["bufHeight"] = int(buf[0]), int(buf[1])
                    p.update(over or {})
                    return p

                def values_of(p):
                    return js(br, "return window.__exPass.bench.values('beat', %s);"
                              % json.dumps(p))

                def per_door_ms(p, n=2000):
                    return js(br, "var p = %s, b = window.__exPass.bench;"
                                  "for (var i = 0; i < 400; i++) b.values('beat', p);"
                                  "var t0 = performance.now();"
                                  "for (var j = 0; j < %d; j++) b.values('beat', p);"
                                  "return {ms: (performance.now() - t0) / %d};"
                                  % (json.dumps(p), n, n))["ms"]

                # THE SPAN PUBLISHED AGAINST THE SPAN DRAWN. The manifest row above read the two
                # ends off the declaration; this asks the instrument's own `values` what it draws at
                # each end of the handle, so a published span that drifted from `periodOf`'s own
                # mapping would redden here rather than quietly send a fill's measured period to the
                # wrong place. Both poses stand at a door and neither is held, so what comes back is
                # the mapping and nothing else.
                lo_end = values_of(door_pose(0, 0))
                hi_end = values_of(door_pose(1, 1))
                check(BROWSER_ROWS[22],
                      abs(lo_end["periodA"] - P_MIN) < 1e-12
                      and abs(lo_end["periodB"] - P_MIN) < 1e-12
                      and abs(hi_end["periodA"] - P_MAX) < 1e-12
                      and abs(hi_end["periodB"] - P_MAX) < 1e-12
                      and lo_end["periodGratings"] == 0 and hi_end["periodGratings"] == 0
                      and lo_end["doorWhyNo"] is None and hi_end["doorWhyNo"] is None,
                      f"the handles at 0 draw periods of {lo_end['periodA']} and "
                      f"{lo_end['periodB']} frame heights and at 1 draw {hi_end['periodA']} and "
                      f"{hi_end['periodB']}, which is exactly the {P_MIN}…{P_MAX} the two handles "
                      f"publish as `frameHeights` — so a fill holding a work's own "
                      f"spectralPeriodPx / frameSide can place it on this handle and know where it "
                      f"lands. Neither end is held and neither leaks")

                BUF_W, BUF_H = 390, 250          # a buffer one whole grating short of the request
                NO_W, NO_H = 390, 220            # and one no whole grating within reach can close
                on_css = values_of(door_pose(FINE))
                on_buf = values_of(door_pose(FINE, buf=(BUF_W, BUF_H)))
                on_applied = values_of(door_pose(APPLIED, buf=(BUF_W, BUF_H)))
                away = values_of(door_pose(FINE, mix=0.5, buf=(NO_W, NO_H)))
                exitdoor = values_of(door_pose(FINE, mix=1, buf=(BUF_W, BUF_H)))
                whole_ms = per_door_ms(door_pose(FINE))
                held_ms = per_door_ms(door_pose(FINE, buf=(BUF_W, BUF_H)))
                check(BROWSER_ROWS[23],
                      on_css["doorWhyNo"] is None and on_css["doorHeld"] is None
                      and on_css["periodGratings"] == 0
                      and on_css["doorGrid"] == {"w": VW, "h": VH, "drawn": False}
                      and on_buf["doorWhyNo"] is None
                      and ("%d x %d buffer" % (BUF_W, BUF_H)) in (on_buf["doorHeld"] or "")
                      and abs(1 / on_buf["periodA"] - 22) < 1e-6
                      and abs(1 / on_buf["periodB"] - 22) < 1e-6
                      and 0 < on_buf["periodGratings"] < 2
                      and on_buf["doorGrid"] == {"w": BUF_W, "h": BUF_H, "drawn": True}
                      and on_applied["doorHeld"] is None and on_applied["doorWhyNo"] is None
                      and away["doorHeld"] is None and away["doorWhyNo"] is None
                      and away["doorGrid"] is None
                      and ("%d x %d buffer" % (BUF_W, BUF_H)) in (exitdoor["doorHeld"] or "")
                      and "the exit door leaks" in (exitdoor["doorHeld"] or ""),
                      "on the %d x %d CSS frame the periods the score holds say «%s»; on the %d x "
                      "%d buffer that frame is drawn on they say «%s», step %.4f of a whole grating "
                      "to %.4f gratings across the height and keep the request at %.4f. The applied "
                      "grating read again on that buffer: «%s». Away from a door it reads nothing "
                      "at all (grid %s). One door instant costs %.4f ms whole and %.4f ms held, on "
                      "this machine."
                      % (VW, VH, on_css["doorHeld"] or "nothing", BUF_W, BUF_H,
                         on_buf["doorHeld"] or "nothing", on_buf["periodGratings"],
                         1 / on_buf["periodA"], 1 / on_buf["periodRequestA"],
                         on_applied["doorHeld"] or "nothing", away["doorGrid"],
                         whole_ms, held_ms))

                # ---- THE DOOR REFUSED ON THE REAL TRANSACTION ROAD ---------------------------
                # The row above reads the instrument's own record. This one puts a real command on
                # the real road at a real buffer: the frame is taken to one no whole grating within
                # reach can close, the pass is offered held at its entry door, and the host has to
                # land the visitor on the instrument's own reason rather than draw a door that is
                # two works at once. The same frame with the score's own periods draws.
                def road(gen):
                    return js(br, "var r = window.__report(); return {state: r.state, "
                                  "drew: r.drew, buffer: r.census.buffer, "
                                  "refused: r.events.filter(function(e){ return e.gen === %d "
                                  "&& e.why && String(e.why).indexOf('door leaks') >= 0; })"
                                  ".map(function(e){ return e.name + ': ' + e.why; })};" % gen)

                br.evaluate("window.__cancel('door road row'); 0")
                idle(br)
                br.set_viewport(NO_W, NO_H)
                br.sleep(0.8)
                own_gen = js(br, "return window.__offer(%s, {clock: 0, progress: 0});"
                             % json.dumps(beat_score()))["gen"]
                br.sleep(1.0)
                played = road(own_gen)
                br.evaluate("window.__cancel('door road row'); 0")
                idle(br)
                leak_gen = js(br, "return window.__offer(%s, {clock: 0, progress: 0});"
                              % json.dumps(beat_score(periodA=FINE, periodB=FINE,
                                                      contrast=0.0)))["gen"]
                br.sleep(1.1)
                leaked = road(leak_gen)
                br.evaluate("window.__cancel('door road row'); 0")
                idle(br)
                br.set_viewport(VW, VH)
                br.sleep(0.8)
                check(BROWSER_ROWS[24],
                      played["buffer"] == "%dx%d" % (NO_W, NO_H)
                      and played["state"] == "running" and played["drew"] == 1
                      and not played["refused"]
                      and len(leaked["refused"]) == 1 and leaked["state"] == "idle"
                      and "the entry door leaks" in leaked["refused"][0]
                      and ("%d x %d buffer" % (NO_W, NO_H)) in leaked["refused"][0]
                      and "no whole grating stands within 2 gratings" in leaked["refused"][0],
                      "on a %d x %d buffer the score's own periods draw (%d cue, state %s, refused "
                      "%s) and the raw sum of two fine gratings is refused with «%s», on which the "
                      "host lands the transaction (state %s, %d cue drawn) and the walk's own glide "
                      "carries the visitor"
                      % (NO_W, NO_H, played["drew"], played["state"],
                         played["refused"] or "nothing",
                         (leaked["refused"] or ["nothing refused"])[0], leaked["state"],
                         leaked["drew"]))

                kept = sorted(p.name for p in SHOTS.glob("*.png"))
                check(BROWSER_ROWS[21],
                      len(kept) >= 25 and all((SHOTS / k).stat().st_size > 1000 for k in kept),
                      f"{len(kept)} captures under {SHOTS.relative_to(ROOT)}: the five poses on both "
                      f"roads, the seven sampled instants, the frame after a resize, the two seeded "
                      f"runs and the handle runs")

    shutil.rmtree(BENCH, ignore_errors=True)

    # ============================================================================================
    # THE RED-ON-BUG PROOFS. The rule each row guards is reverted in the artifact the browser
    # actually loads; the pack served is changed and the host is re-stamped with the digest of the
    # bytes it is handed, which is what the build does. The file on disk is never touched, so no
    # working tree can be left changed by a proof.

    # ONE. The door test in `doorReadOf` is taken out, so no instant is ever a door and the reading
    # is never taken — this instrument exactly as it stood before it read its doors at runtime,
    # declaring both doors whole in its manifest and never checking the frame it drew.
    def red_door(br):
        br.set_viewport(390, 220)
        br.sleep(0.9)
        gen = js(br, "return window.__offer(%s, {clock: 0, progress: 0});"
                 % json.dumps(beat_score(periodA=0.06, periodB=0.06, contrast=0.0)))["gen"]
        br.sleep(1.2)
        r = js(br, "var r = window.__report(); return {state: r.state, drew: r.drew, "
                   "buffer: r.census.buffer, refused: r.events.filter(function(e){ "
                   "return e.gen === %d && e.why "
                   "&& String(e.why).indexOf('door leaks') >= 0; }).length};" % gen)
        br.evaluate("window.__cancel('red one'); 0")
        return r

    base_read = on_bench(red_door)
    bug = REGION.replace("var want = st.mix === 0 ? 1 : (st.mix === 1 ? 0 : -1);",
                         "var want = -1;", 1)
    bug_read = on_bench(red_door, pack_text=bug)
    check(RED_ROWS[0],
          bug != REGION and base_read and bug_read
          and base_read["refused"] == 1 and base_read["state"] == "idle"
          and bug_read["refused"] == 0 and bug_read["state"] == "running"
          and bug_read["drew"] == 1,
          f"on the {base_read and base_read['buffer']} buffer two gratings this fine cross this "
          f"instrument's own mask over inside the frame. With the reading standing the host is told "
          f"so ({base_read and base_read['refused']} refusal, state "
          f"{base_read and base_read['state']}) and the walk's own glide carries the visitor. With "
          f"the door test taken out — no instant is a door, the instrument as it stood before it "
          f"read its doors at runtime — the same command draws that door instead "
          f"({bug_read and bug_read['refused']} refusals, state {bug_read and bug_read['state']}, "
          f"{bug_read and bug_read['drew']} cue drawn), and nothing anywhere says the frame it laid "
          f"down was one whole work")

    # TWO. The module's own repair of the phase (beat.js:396-403): the handle pushes the first field
    # FORWARD and the second BACK, so what moves is the DIFFERENCE of the two fields — which is what
    # the beat's envelope is a function of. Pushed both the same way the envelope does not move at
    # all, and the module's own note records that as measured: half a channel. This row reverts the
    # sign and asks the picture.
    def red_phase(br):
        br.evaluate("window.__show('host'); 0")
        out = {}
        for name, ph in (("rest", 0), ("moved", 0.5)):
            js(br, "return window.__offer(%s, {clock: 1.5, progress: 0.5});"
               % json.dumps(beat_score(phase=ph)))
            br.sleep(0.7)
            out[name] = png(br, SHOTS / ("red-phase-" + name + ".png"))
            br.evaluate("window.__cancel('red phase'); 0")
            idle(br)
        return {"mean": diff(out["rest"], out["moved"])[0]}

    base_ph = on_bench(red_phase)
    bug2 = REGION.replace("var phases = [ph + drift, -ph - drift];",
                          "var phases = [ph + drift, ph - drift];", 1)
    bug_ph = on_bench(red_phase, pack_text=bug2)
    check(RED_ROWS[1],
          bug2 != REGION and base_ph and bug_ph
          and base_ph["mean"] > SEAM and bug_ph["mean"] <= SEAM,
          f"with the phase pushing the two fields apart the handle moves the frame by "
          f"{base_ph and base_ph['mean']:.4f} of 255; pushed both fields the same way — the module's "
          f"own arrangement before its repair — the envelope, which is a function of the DIFFERENCE "
          f"of the two fields, does not move and the same handle moves the frame by "
          f"{bug_ph and bug_ph['mean']:.4f}, under the seam of {SEAM}")

    # THREE. The tilt is pinned back to the module's own constant, which is what the port would be
    # had it published the handle in its manifest and never wired it — the failure a manifest alone
    # cannot catch, since the composer would read a declared handle, fill it from the pair's own
    # lattice angles and drive a number the picture never sees. The row walks the handle between its
    # own two ends and asks the frame.
    def red_tilt(br):
        br.evaluate("window.__show('host'); 0")
        out = {}
        for name, tv in (("lo", TILT_MIN), ("hi", TILT_MAX)):
            js(br, "return window.__offer(%s, {clock: 1.5, progress: 0.5});"
               % json.dumps(beat_score(beatTilt=tv)))
            br.sleep(0.7)
            out[name] = png(br, SHOTS / ("red-tilt-" + name + ".png"))
            br.evaluate("window.__cancel('red tilt'); 0")
            idle(br)
        return {"mean": diff(out["lo"], out["hi"])[0]}

    base_tilt = on_bench(red_tilt)
    bug3 = REGION.replace("var w = wavesAt(pp, aspect, tilt);",
                          "var w = wavesAt(pp, aspect, BEAT_TILT);", 1)
    bug_tilt = on_bench(red_tilt, pack_text=bug3)
    check(RED_ROWS[2],
          bug3 != REGION and base_tilt and bug_tilt
          and base_tilt["mean"] > SEAM and bug_tilt["mean"] == 0.0,
          f"walked between its two ends the published tilt moves the frame by "
          f"{base_tilt and base_tilt['mean']:.4f} of 255; pinned back to the module's own nine "
          f"degrees the same walk moves it by {bug_tilt and bug_tilt['mean']:.4f} — the handle "
          f"would still stand in the manifest, the composer would still fill it from the two "
          f"works' lattice angles, and the picture would never see it")

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
