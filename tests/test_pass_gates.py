#!/usr/bin/env python3
"""PASS-API-V1 — the gate instrument on the host's frame.
Run: python3 tests/test_pass_gates.py

Root: his word of 2026-08-18 08:52 and 08:58 — «перенеси ВЕСЬ арсенал и пересобери проход». The lab
holds a gate module built from a MOTIF rather than from a shape: two masses of the departing work
facing each other across a slot of emptiness, the slot parting, and the arriving work already
standing behind it. This file is that module landed as an engine instrument and proved on the host's
own frame. docs/design/PASS-API-V1.md §7 (GPU and resources), §8 (the manifest) and §9's conformance
rows 7, 9, 10, 13, 14, 15, 16 and 22 are what it makes real; the lifecycle rows stay in
tests/test_pass_api.py and are untouched.

WHAT IS COMPARED, AND AGAINST WHAT.

  The doors. At the dial's two ends one whole work stands. Each is measured against ITS OWN FILE —
  the picture cover-fitted into the frame and pulled in by the headroom the squeeze and the drift
  need (the module's own ZOOM of 1.27) — inside the project's seam threshold of 6 of 255. A door
  that carried a ten-thousandth of the other photograph would fail this, which is the point of it.

  The five poses. The host's frame is compared against the LAB MODULE's own frame, on one pose both
  roads were driven by: the same dial, the same five params, the same die, the same second, and the
  same reading of the departing work's own gate. Two roads of one frame, never two guesses at one.

  The gate itself. The module measures the departing photograph at creation with the collection's own
  busy-field instrument; an instrument file may not open a picture, so the port takes that reading as
  three handles. The fixture reads the module's own numbers back out of it and hands them to the
  port, so both roads stand on ONE measurement of ONE photograph.

  The lab tree is READ ONLY and is found at $TLVPHOTOS_ROOT, defaulting to the main worktree — the
  gate module stands only there, and untracked, on the day of this port. Absent, every browser row
  here is a pinned SKIP that names the missing path — never a silent pass.
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

LAB = Path(os.environ.get("TLVPHOTOS_ROOT", "/Users/sashaabramovich/tlvphotos")) / "lab"
PHOTOS = [LAB / "photos" / "towers.jpg", LAB / "photos" / "glassgrid.jpg"]
MODULE = LAB / "effects" / "gates.js"

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

# Captures are kept rather than swept, because §9 row 16 asks for evidence for every landed
# instrument and evidence that is deleted is no evidence.
SHOTS = ROOT / "tests" / "captures" / "pass-gates"

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


# ---------------------------------------------------------------- the score this instrument plays
# AUTHORED HERE, and said to be authored here. lab/data/scores carries a template and a table for the
# woven instrument alone, so there is no per-pair score on file for this one. Everything below is
# either a number the module itself declares or a field the contract requires; nothing is measured in
# this file and nothing is invented as a measurement. The three slot handles are handed in by the
# caller, read off the module's own measurement of the departing photograph.
DIE = 4.91016            # the die lab/data/scores' own weave score carries, so every suite rolls one
DURATION_MS = 3000
WITHIN_MS = 500

DEFAULTS = {"jamb": 0.55, "teeth": 9, "swing": 0.35, "press": 0.65, "lead": 0.5,
            "slotAxis": 1, "slotPlace": 0.5, "slotHalf": 0.08,
            "shade": 1, "travel": 1, "mask": 0, "seed": DIE}


def gates_score(**statics):
    """The score, with a track for every handle the manifest publishes but the open one (§4.4b).

    The five params rest at the module's own declared defaults (gates.js:436-440): jamb 0.55, teeth 9,
    swing 0.35, press 0.65, lead 0.5. The two judge channels rest at 1, which is where the module
    holds them. `mix` reads the transaction's own progress and `clock` the second the host hands
    down — that second is the only place the module ever read time, and it read its own accumulated
    frame clock there (gates.js:577). `dial` is the manifest's OPEN handle and carries no track, so
    the instrument derives the travelled number from `mix` through its own measured curve.
    """
    P = dict(DEFAULTS)
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
        "intent": "two masses of the departing work part along the work's own slot of emptiness and "
                  "travel out of the frame, and the arriving work stands behind them from the first "
                  "crack of the opening (lab/effects/gates.js:1-18, its own header)",
        "pair": {"a": "a", "b": "b"},
        "seed": DIE,
        "duration": DURATION_MS,
        "direction": "a-to-b",
        "interruption": {"withinMs": WITHIN_MS, "resolve": "nearest-door"},
        "failLand": "arrive",
        "camera": {"owner": "stage", "rests": "b",
                   "track": [{"at": "b", "pan": {"x": 0, "y": 0}, "logScale": 0,
                              "pitch": 0, "yaw": 0, "roll": 0, "fov": None, "owner": "stage"}]},
        "cues": [{
            "id": "gates-main",
            "instrument": {"id": "gates", "api": 1},
            "voice": "letter",
            "roles": ["disassembly", "mystery", "assembly"],
            "levels": ["CELL", "CELL CONTENT"],
            "levelOwnership": {"CELL": "owns", "CELL CONTENT": "owns"},
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
        "quality": {v: {"renderScale": None, "cues": {"gates-main": {"resources": res[v]}}}
                    for v in ("lean", "standard", "rich")},
        "provenance": {"source": "lab/effects/gates.js's own declared defaults and constants",
                       "measuredAt": None, "by": "tests/test_pass_gates.py"},
    }


# ---------------------------------------------------------------- bake once
build_site.SITE_CONFIG = dict(build_site.SITE_CONFIG)
build_site.SITE_CONFIG["pass"] = {"visualLayer": "pass", "diagnostics": "on"}

TMP = Path(tempfile.mkdtemp(prefix="synth_passgates_"))
build_site.OUT = TMP
build_site.build(SITE_URL)
LAYER = (TMP / "pass-layer.js").read_text(encoding="utf-8")
# The instrument's own region of the BUILT file — the real artifact, comments stripped as it ships —
# which is what the ownership fence and every other string row below is read against.
REGION = (TMP / "pass-inst-gates.js").read_text(encoding="utf-8")
SOURCE_TEXT = (ROOT / "engine" / "assets" / "pass-inst-gates.js").read_text(encoding="utf-8")
LABTXT = MODULE.read_text(encoding="utf-8") if MODULE.exists() else ""

# ---------------------------------------------------------------- string rows

OWNED = ["createElement", "getContext", "requestAnimationFrame", "addEventListener",
         "performance.now", "Date.now", "new Image", "setTimeout", "setInterval",
         "getImageData", "drawImage"]
held = [s for s in OWNED if s in REGION]
check("PASS-GATES the instrument creates no context, no canvas, no loop, no listener and no read of "
      "a picture's pixels",
      not held,
      "§1.2's fence, read against the instrument's own region of the built file: none of the eleven "
      "ways of owning hardware or of opening a photograph appears there, so the module's canvas, its "
      "WebGL 1 context, its frame loop, its resize observer and the whole build-time busy-field "
      "instrument — which draws the source into a canvas of its own and reads the pixels back "
      "(gates.js:288-355) — all stayed in the lab"
      if not held else "the instrument's region holds " + ", ".join(held))

HANDLES = ["mix", "clock", "dial", "jamb", "teeth", "swing", "press", "lead",
           "slotAxis", "slotPlace", "slotHalf", "seed", "shade", "travel", "mask"]
absent = [h for h in HANDLES if ("%s: {" % h) not in REGION]
check("PASS-GATES every handle the instrument publishes is a handle a score can drive",
      not absent,
      "§4.4b: fifteen handles — the module's five declared params, its one travelling number, the "
      "second the host hands down, its die, two of its three judge channels, the open dial its third "
      "judge channel became, the three that carry the departing work's own measured gate, and the "
      "fleet's own `mask`, which is the one handle here the module has no counterpart for"
      if not absent else "these are published nowhere: " + ", ".join(absent))

check("PASS-GATES the arriving work's drift reads the handed-down second and no clock of its own",
      "DRIFT_MAX * Math.sin(TAU * (st.t || 0) / 9) * 4 * d * (1 - d)" in REGION
      and "t: h.clock" in REGION,
      "gates.js:577 read `t`, its own accumulated frame time; here it is the `clock` handle, which "
      "is what makes the seeded repeat below mean anything")

check("PASS-GATES the manifest leaves the drawing buffer unpreserved",
      "gl: { preserveDrawingBuffer: false }" in REGION,
      "the module asks its own context for a preserved buffer (gates.js:469) and §7 refuses a "
      "manifest that asks for it; the redraw it stood in for is the host's own frame loop")

check("PASS-GATES the shader carries no version header of its own",
      "#version" not in REGION and bool(LABTXT) and "#version" not in LABTXT,
      "so the host's translator stamps the one header this shader needs and no second one arrives")


def frag_lines(txt):
    """Every line of a FRAG array, read as the strings the file actually joins — a scanner rather
    than a pattern, because both files carry apostrophes inside their comments."""
    m = re.search(r"var FRAG = \[", txt)
    if not m:
        return []
    i, n, out = m.end(), len(txt), []
    while i < n:
        c = txt[i]
        if c in "'\"":
            q, i, buf = c, i + 1, []
            while i < n and txt[i] != q:
                if txt[i] == "\\":
                    buf.append(txt[i + 1])
                    i += 2
                    continue
                buf.append(txt[i])
                i += 1
            i += 1
            out.append("".join(buf))
        elif txt[i:i + 2] == "//":
            i = txt.find("\n", i)
            if i < 0:
                break
        elif c == "]":
            break
        else:
            i += 1
    return out


# THE TWO LINES THE FLEET'S JUDGES' CHANNEL ADDS, and the only two in the shader that are not the
# lab module's. The row below takes them out and holds the remainder against the module character for
# character, so a third added line — or one of the module's own quietly rewritten — reddens it.
FLEET_MASK = ["uniform float uMask;",
              "  col = mix(col, vec3(covL, covR, 0.0), uMask);"]
lab_frag = frag_lines(LABTXT)
port_frag = frag_lines(SOURCE_TEXT)
port_own = [line for line in port_frag if line not in FLEET_MASK]
frag_same = (bool(lab_frag) and lab_frag == port_own
             and all(a in port_frag for a in FLEET_MASK)
             and len(port_frag) == len(lab_frag) + 2)
check("PASS-GATES the shader is the lab module's own, character for character, but for the two lines "
      "the fleet's judges' channel adds",
      frag_same,
      f"{len(port_own)} of the module's own lines, none of them rewritten, and exactly two added: "
      f"«{FLEET_MASK[0]}» and «{FLEET_MASK[1]}». Every other port in this farm had to redo one line "
      f"besides — the frame's aspect, which a lab module computes from its own drawing buffer and an "
      f"instrument has to derive from the size the host binds. This shader never reads an aspect: it "
      f"works in the frame's own uv from end to end, so not one character of the module's own moved"
      if frag_same else
      f"lab {len(lab_frag)} lines, port {len(port_frag)} of which {len(port_own)} are not the fleet's "
      f"two; first difference at "
      f"{next((i for i, (a, b) in enumerate(zip(lab_frag, port_own)) if a != b), 'the length')}")


def numbers(text, pattern):
    m = re.search(pattern, text)
    return [float(x) for x in re.findall(r"-?\d+\.?\d*", m.group(1))] if m else []


lab_q = numbers(LABTXT, r"FEEL_Q = \[([^\]]+)\]")
port_q = numbers(REGION, r"FEEL_Q = \[([^\]]+)\]")
check("PASS-GATES the response curve is carried digit for digit out of the lab module",
      len(lab_q) == 21 and lab_q == port_q
      and "FEEL_D0 = 0.055" in LABTXT and "FEEL_D0 = 0.055" in REGION,
      f"twenty-one shares and the dead band of 0.055, unchanged: {len(port_q)} numbers matched, half "
      f"the change standing at {port_q[10] if len(port_q) > 10 else None}. The dead bands are what "
      f"make a door a door to the pixel — the dial stands at exactly 0 across the first band and at "
      f"exactly 1 across the last (gates.js:531-534)")

# Each constant as the LAB module spells it and as the PORT spells it.
CONSTANTS = [("PRESS_MAX = 0.12", "PRESS_MAX = 0.12",
              "how far the arriving work is squeezed into the slot, in frame units"),
             ("DRIFT_MAX = 0.03", "DRIFT_MAX = 0.03",
              "and how far it drifts along the slot on the handed second"),
             ("ZOOM = 1 + 2 * PRESS_MAX + 0.03", "ZOOM = 1 + 2 * PRESS_MAX + 0.03",
              "the crop those two are paid for with, derived from them rather than chosen"),
             ("MOTIF_BAND = 0.16", "MOTIF_BAND = 0.16",
              "the collection's own central band, 0.42 to 0.58 of the frame, said as a width"),
             ("SLOT_MIN = 0.02, SLOT_MAX = 0.30", "SLOT_MIN = 0.02, SLOT_MAX = 0.30",
              "and the bounds a slot's own width is held inside")]
missing_const = ([c for c, _, _ in CONSTANTS if c not in LABTXT]
                 + [c for _, c, _ in CONSTANTS if c not in REGION])
check("PASS-GATES every constant of the picture stands at the number the lab module gives it",
      not missing_const,
      "; ".join("%s — %s" % (c, why) for c, _, why in CONSTANTS) if not missing_const
      else "these differ: " + ", ".join(missing_const))

# THE MEASURING WALK STAYED BEHIND, AND SO DID ITS FLOOR. `GATE_FLOOR` is the collection's quarter
# rule and belongs to the walk that decides whether a source has a gate at all (gates.js:269-273).
# That walk cannot cross §1.2's fence, so neither does its floor: no reading of a pair can make this
# instrument refuse a crossing, which is his word of 2026-08-18 09:51 and 10:15.
FLOORS = ["GATE_FLOOR", "SLOT_LEVEL", "busyProfiles", "slotOn", "readBand", "gateOf", "toLinear"]
crossed = [f for f in FLOORS if f in REGION]
check("PASS-GATES the collection's own floor stayed behind with the instrument that needed it",
      not crossed and "GATE_FLOOR" in LABTXT,
      "the module's quarter rule of 0.265 decides whether a SOURCE carries a gate, and it is one step "
      "of a walk that opens the photograph and reads its pixels. None of the seven names of that walk "
      "crosses into the instrument, so nothing here can turn a pair away: a pair whose record says "
      "nothing about a gate is played with the slot standing in the middle of the frame at the "
      "motif's own band width, which is the module's own reading for such a source"
      if not crossed else "the walk crossed: " + ", ".join(crossed))

check("PASS-GATES the three slot handles publish where their measurement is seated, and what they "
      "rest at",
      'seatedThroughTheHostsOwnFit: true, reads: "slotInFile"' in REGION
      and 'seatedThroughTheHostsOwnFit: true, reads: "halfInFile"' in REGION
      and 'slotAxis: { min: 0, max: 1, def: 1, level: "CELL" }' in REGION
      and "def: MOTIF_BAND / 2" in REGION,
      "his 19:13 word lifted to the class at 19:21: every geometric parameter names the measurement "
      "of the work it reads. These three carry the departing work's own gate — the axis it stands "
      "on, its place as a share of the FILE and half its own width — and each publishes that its "
      "value is seated through the host's own fit before it reaches the frame, beside the name the "
      "request stays on the record under. Their defaults are the module's own naive reading "
      "(gates.js:399-400): upright, the middle of the frame, half the motif's own band. THE AXIS "
      "LITERAL GAINED A LEVEL on 2026-08-25, with the sweep that made every handle in the fleet "
      "declare the structural level it drives; the slot is a CELL reading and the row follows it "
      "there, holding every number it always held")

check("PASS-GATES the host binds uniforms by declared name, never by position or a written list",
      "getUniformLocation(p, u.name)" in LAYER and "gl.uniform1f(U.uSlot" not in LAYER
      and "gl.uniform2f(U.uOpen" not in LAYER,
      "the host reads the manifest; not one of this instrument's sixteen uniform names is written "
      "into it")

declared = set(re.findall(r'\{ name: "(u\w+)", type:', REGION))
spelled = set(re.findall(r'uniform \w+ (u\w+);', REGION))
check("PASS-GATES the manifest's declared names and the shader's own names are one set",
      declared == spelled and len(declared) == 16,
      f"{len(declared)} declared, {len(spelled)} spelled; "
      f"declared only: {sorted(declared - spelled)}; spelled only: {sorted(spelled - declared)}")

sha = hashlib.sha256(MODULE.read_bytes()).hexdigest() if MODULE.exists() else ""
declared_sha = (re.search(r'sha256: "([0-9a-f]{64})"', REGION) or [None, None])[1]
check("PASS-GATES the provenance names the file the port was read from, and the file weighs to it",
      bool(sha) and sha == declared_sha and "commit: null" in REGION,
      f"the lab module stands untracked in the tlvphotos worktree on the day of this port, so no "
      f"commit is named and none is invented; the digest of the bytes the port was read from stands "
      f"in its place and the file still weighs to {sha[:16]}…")

# ---------------------------------------------------------------- browser rows

BROWSER_ROWS = [
    "PASS-GATES §8     · the manifest carries every field the contract names, in its shape",
    "PASS-GATES §8     · it publishes CELL and CELL CONTENT, and the reading is said to be derived",
    "PASS-GATES row 7  · door 0 stands the departing work, measured against its own file",
    "PASS-GATES row 7  · door 0 carries no trace of the arriving work",
    "PASS-GATES row 7  · door 1 stands the arriving work, measured against its own file",
    "PASS-GATES row 7  · door 1 carries no trace of the departing work",
    "PASS-GATES the host's frame and the lab module's frame agree at all five poses",
    "PASS-GATES §7     · no empty frame at any sampled instant of the pass",
    "PASS-GATES §7     · the frame after a change of viewport is drawn, not a kept buffer",
    "PASS-GATES row 10 · a seeded run repeats to the pixel",
    "PASS-GATES row 14 · textures, programmes and framebuffers return to their baseline after ten runs",
    "PASS-GATES row 15 · the console stays clean",
    "PASS-GATES row 22 · the census shows granted against declared, and neither overruns",
    "PASS-GATES §7     · a manifest asking for a preserved drawing buffer is refused, with its reason",
    "PASS-GATES §7     · a uniform bound to a name the shader lacks is refused, with its reason",
    "PASS-GATES §7     · one canvas, one context, two source textures, one pass a frame",
    "PASS-GATES §7     · a shader already at GLSL ES 3.00 receives no second version header",
    "PASS-GATES the real transaction road: curtain up, one pass drawn, exactly one dock at the end",
    "PASS-GATES row 9  · one camera authority through a real pass, and the pose rests on the arrival",
    "PASS-GATES §4.4b  · the jamb, the teeth, the swing, the press and the lead reach the PICTURE",
    "PASS-GATES §4.4b  · the departing work's own measured gate reaches the PICTURE",
    "PASS-GATES the doors are read on the DRAWING BUFFER, and both stand whole on every grid asked",
    "PASS-GATES row 16 · the captures are kept as evidence",
    "PASS-GATES §4.4b  · the fleet's judges' channel draws this instrument's own cut, and rests at nothing",
    "PASS-GATES the pinned numbers of the sweep are live, and bind at the numbers they are named at",
]

RED_ROWS = [
    "PASS-GATES red-on-bug · the teeth left biting at the far door: the exit door stops being one work",
    "PASS-GATES red-on-bug · the seating removed: the measured slot lands where nothing measured it",
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
    """The work as the instrument seats it: cover-fit, then the centre crop the squeeze is paid for
    with (the module's own ZOOM). The very same construction lab/carrier-check.py uses, so the two
    checks judge a door the same way."""
    from PIL import Image
    im = Image.open(src).convert("RGB")
    iw, ih = im.size
    fa, ia = w / float(h), iw / float(ih)
    sw, sh = (ih * fa, float(ih)) if ia > fa else (float(iw), iw / fa)
    sw /= zoom
    sh /= zoom
    x0, y0 = (iw - sw) / 2.0, (ih - sh) / 2.0
    return im.resize((w, h), Image.BILINEAR, box=(x0, y0, x0 + sw, y0 + sh))


def channels(p):
    """Each channel's lowest and highest value over a capture — how a frame that is a CUT MAP is told
    from a frame that is the photographs."""
    from PIL import Image, ImageStat
    return ImageStat.Stat(Image.open(p).convert("RGB")).extrema


def apart(p, work):
    from PIL import Image, ImageChops, ImageStat
    a = Image.open(p).convert("RGB")
    if a.size != work.size:
        return 255.0, 255.0
    st = ImageStat.Stat(ImageChops.difference(a, work))
    return sum(st.mean) / 3.0, max(m for _, m in st.extrema)


def bench_dir(pack_text=None):
    """The bench's own served root: the BUILT pass-layer.js (the real artifact, namespace applied and
    comments stripped), the lab module unchanged, the two photographs, and the page that stands the
    two roads of one frame side by side.

    A row proving a rule reds hands over a CHANGED instrument file and writes the site's own record
    with the digest of the bytes actually served, which is what the build does. The source file on
    disk is never touched, so nothing has to be restored and no working tree can be left changed by a
    red-on-bug proof."""
    d = Path(tempfile.mkdtemp(prefix="synth_gatesbench_"))
    pack = REGION if pack_text is None else pack_text
    shutil.copy2(TMP / "pass-layer.js", d / "pass-layer.js")
    for _inst in sorted(TMP.glob("pass-inst-*.js")):
        shutil.copy2(_inst, d / _inst.name)
    (d / "pass-inst-gates.js").write_text(pack, encoding="utf-8")
    record = json.loads((TMP / "config.json").read_text(encoding="utf-8"))
    record["pass"]["instruments"]["gates"]["digest"] = hashlib.sha256(
        pack.encode("utf-8")).hexdigest()
    (d / "config.json").write_text(json.dumps(record), encoding="utf-8")
    shutil.copy2(MODULE, d / "gates.js")
    (d / "photos").mkdir()
    for p in PHOTOS:
        shutil.copy2(p, d / "photos" / p.name)
    shutil.copy2(ROOT / "tests" / "fixture_pass_gates.html", d / "index.html")
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
    GATE = None
    with serve(BENCH) as base:
        with Browser(width=VW, height=VH) as br:
            br.navigate(base + "/index.html")
            if not ready(br):
                for r in BROWSER_ROWS:
                    check(r, False, "the bench never came up: "
                         + br.evaluate("JSON.stringify(window.__errs||[])"))
            elif not js(br, "return !!window.__exPass.bench.manifest('gates');"):
                why = js(br, "var e = window.__host.report().events.filter(function(x){"
                             "return x.name === 'manifest-refused';});"
                             "return e.length ? e[e.length - 1].why : null;")
                for r in BROWSER_ROWS:
                    check(r, False, "the host registered no «gates» instrument: " + str(why))
            else:
                # ---- §8: the manifest, read off the registered instrument -----------------------
                m = js(br, "return window.__exPass.bench.manifest('gates');")
                zoom = m["framings"]["0"]["coverCrop"]
                res = m["resources"]
                shape = (
                    m["id"] == "gates" and m["api"] == 1 and m["arity"] == 2
                    and m["roles"] == ["disassembly", "mystery", "assembly"]
                    and sorted(m["params"]) == ["jamb", "lead", "press", "swing", "teeth"]
                    and len(m["handles"]) == 15
                    and all(set(h) >= {"min", "max", "def"} for h in m["handles"].values())
                    and m["handles"]["dial"].get("open") is True
                    and m["neutrals"] == {"a": 0, "b": 1}
                    and m["doors"]["in"]["handle"] == "mix" and m["doors"]["in"]["value"] == 0
                    and m["doors"]["out"]["handle"] == "mix" and m["doors"]["out"]["value"] == 1
                    and sorted(m["framings"]) == ["0", "1"]
                    and m["framings"]["0"] == m["framings"]["1"]
                    and abs(zoom - (1 + 2 * 0.12 + 0.03)) < 1e-12
                    and m["camera"] == {"needs": "none", "authority": "stage"}
                    and m["cuts"] == ["panel"]
                    and m["coverage"]["writes"] is False
                    and sorted(m["suits"]["reads"]) == ["motifs.gateGap", "motifs.measured"]
                    and len(m["passes"]) == 1 and len(m["passes"][0]["uniforms"]) == 16
                    and sorted(res) == ["lean", "rich", "standard"]
                    and all("bytesEstimate" in res[v] and res[v]["programs"] == 1
                            and res[v]["passes"] == 1 and res[v]["textureSlots"] == 2
                            for v in res)
                    and m["capabilities"] == ["webgl2"] and m["decline"]
                    and m["provenance"]["labPath"] == "lab/effects/gates.js"
                    and m["provenance"]["commit"] is None
                    and m["readiness"] == "production-ready"
                    and "gates" in js(br, "return window.__host.report().registered;"))
                check(BROWSER_ROWS[0], shape,
                      f"fifteen handles of which one is open, sixteen uniforms in one pass, the crop "
                      f"{zoom} the squeeze and the drift are paid for with, a cut on {m['cuts']}, an "
                      f"alpha that is the constant 1 (coverage.writes={m['coverage']['writes']}, so a "
                      f"cue of this instrument may stand at the bottom of a stack), and a `suits` "
                      f"block reading {m['suits']['reads']} — the very two readings the composer "
                      f"already carries for this motif")

                check(BROWSER_ROWS[1],
                      m["levels"] == ["CELL", "CELL CONTENT"]
                      and "carries a `gates` row" in SOURCE_TEXT
                      and "gates.js:176-177" in SOURCE_TEXT
                      and "gates.js:192-194" in SOURCE_TEXT
                      and "SURFACE is NOT claimed" in SOURCE_TEXT,
                      "neither module-contract file carries a `gates` row, so no level is published "
                      "for this module anywhere and both are read off its own header, at the lines "
                      "named in the port: CELL because «each is a rigid half of the departing work "
                      "sliding out of the frame» (gates.js:176-177), CELL CONTENT because the content "
                      "inside the cut moves in its own right on both sides of it — the leaf's "
                      "projective turn (gates.js:178-180) and the arriving work's squeeze "
                      "(gates.js:192-194). SURFACE is not claimed and the port says why")

                GATE = js(br, "return window.__gate();")
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
                    check(BROWSER_ROWS[2 + i * 2], a <= SEAM,
                          f"{door} against {ownn}: mean {a:.4f} of 255 (threshold {SEAM}), worst "
                          f"channel {amx}")
                    o, _ = apart(shots[door], other)
                    check(BROWSER_ROWS[3 + i * 2], o >= FAR,
                          f"{door} against {othern}: mean {o:.4f} of 255 (must exceed {FAR})")

                agree = [(name, ) + diff(ph, pm) for name, ph, pm in pairs]
                check(BROWSER_ROWS[6], all(mn <= SAME for _, mn, _ in agree),
                      "; ".join(f"{n}: mean {mn:.4f} of 255 (threshold {SAME}), worst channel {mx}"
                                for n, mn, mx in agree)
                      + f"; both roads stand on ONE reading of the departing work's own gate — the "
                      f"module measured it and the port took it as three handles: axis "
                      f"{GATE['measured']['axis']}, place {GATE['measured']['inFile']} of the file, "
                      f"half {GATE['measured']['halfInFile']}, measured "
                      f"{GATE['measured']['measured']}, from «{GATE['measured']['from']}»")

                # ---- §7: no empty frame, and the redraw the preserved buffer stood in for -------
                SCORE_JSON = json.dumps(gates_score(**{
                    "slotAxis": 1 if GATE["measured"]["axis"] == "upright" else 0,
                    "slotPlace": GATE["measured"]["inFile"],
                    "slotHalf": GATE["measured"]["halfInFile"]}))
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
                check(BROWSER_ROWS[7],
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
                check(BROWSER_ROWS[8],
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
                check(BROWSER_ROWS[9], took["took"] and mn == 0.0 and mx == 0,
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
                check(BROWSER_ROWS[10], same,
                      f"before={base_c['textures']}/{base_c['programs']}/{base_c['framebuffers']} "
                      f"after ten runs={after['textures']}/{after['programs']}/{after['framebuffers']} "
                      f"(textures/programmes/framebuffers)")

                errs = json.loads(br.evaluate("JSON.stringify(window.__errs||[])"))
                check(BROWSER_ROWS[11], not errs, "; ".join(errs)[:200])

                r = js(br, "return window.__report();")["resources"]
                check(BROWSER_ROWS[12],
                      r["declared"] and r["over"] is False
                      and r["granted"]["textures"] == r["declared"]["textures"]
                      and r["granted"]["framebuffers"] == r["declared"]["framebuffers"]
                      and r["granted"]["bytes"] == r["declared"]["bytesEstimate"],
                      f"declared={r['declared']} granted={r['granted']}")

                # ---- the two manifest refusals ---------------------------------------------------
                STUB = ("values:function(){return {vert:1,slot:0.5,open:[0,0],bite:0,teeth:9,"
                        "swing:0,press:0,drift:0,guard:0};},"
                        "fit:function(){return [1,1,0,0];},"
                        "prepare:function(){return {take:false};}, start:function(){},"
                        "frame:function(){}")
                r = js(br, """
                  var m = JSON.parse(JSON.stringify(window.__exPass.bench.manifest('gates')));
                  m.gl.preserveDrawingBuffer = true;
                  var ok = window.__exPass.bench.register({name:'gates-preserve', manifest:m, %s});
                  var evs = window.__host.report().events.filter(function(e){return e.name==='manifest-refused';});
                  return {ok: ok, why: evs.length ? evs[evs.length-1].why : null,
                          registered: window.__host.report().registered};
                """ % STUB)
                check(BROWSER_ROWS[13],
                      r["ok"] is False and r["why"] and "preserved" in r["why"]
                      and "gates-preserve" not in r["registered"],
                      f"registered={r['ok']} why={r['why']}")

                r = js(br, """
                  var m = JSON.parse(JSON.stringify(window.__exPass.bench.manifest('gates')));
                  m.passes[0].uniforms.push({name:'uPointer', type:'vec2', source:'pointer'});
                  var ok = window.__exPass.bench.register({name:'gates-pointer', manifest:m, %s});
                  var evs = window.__host.report().events.filter(function(e){return e.name==='manifest-refused';});
                  return {ok: ok, why: evs.length ? evs[evs.length-1].why : null,
                          registered: window.__host.report().registered};
                """ % STUB)
                check(BROWSER_ROWS[14],
                      r["ok"] is False and r["why"] and "uPointer" in r["why"]
                      and "cannot supply" in r["why"] and "gates-pointer" not in r["registered"],
                      f"registered={r['ok']} why={r['why']}")

                # ---- the hardware, counted where each thing is made ------------------------------
                js(br, "return window.__offer(%s, {clock: 1.0, progress: 0.4});" % SCORE_JSON)
                br.sleep(0.6)
                cen = js(br, "return window.__report();")["census"]
                check(BROWSER_ROWS[15],
                      cen["canvases"] == 1 and cen["contexts"] == 1 and cen["textures"] == 2
                      and cen["passesLastFrame"] == 1 and cen["framebuffers"] == 0
                      and cen["preserveDrawingBuffer"] is False
                      and int(br.evaluate("String(document.querySelectorAll('canvas').length)")) == 2,
                      f"census={cen}; the second canvas on the page is the lab module's own, which is "
                      f"the road being compared against and no part of the host")

                # ---- the version header, through the host's own translator -----------------------
                r = js(br, """
                  var m = window.__exPass.bench.manifest('gates');
                  var plain = window.__exPass.bench.es3(m.passes[0].frag, false);
                  var already = window.__exPass.bench.es3('#version 300 es\\n' + m.passes[0].frag, false);
                  var count = function (s) { return s.split('#version').length - 1; };
                  return {source: count(m.passes[0].frag), stamped: count(plain),
                          untouched: count(already), head: plain.slice(0, 15)};
                """)
                check(BROWSER_ROWS[16],
                      r["source"] == 0 and r["stamped"] == 1 and r["untouched"] == 1
                      and r["head"].startswith("#version 300 es"),
                      f"the module's own shader carries {r['source']} headers, the translator leaves "
                      f"it with {r['stamped']}, and a source that already carries one comes back with "
                      f"{r['untouched']}")

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
                check(BROWSER_ROWS[17],
                      took["took"] and mid["state"] == "running" and mid["curtains"][:1] == [True]
                      and end["state"] == "idle" and len(end["docks"]) == 1
                      and end["curtains"][-1] is False and "docked" in end["events"],
                      f"mid={mid} end={end}")

                cam = js(br, "var r = window.__report(); "
                             "return {camera: r.camera, rest: r.rest, handoffs: r.handoffs, "
                             "tol: r.camTolerances};")
                check(BROWSER_ROWS[18],
                      cam["camera"] and cam["camera"]["owner"] == "stage"
                      and cam["handoffs"] == []
                      and cam["rest"] and cam["rest"]["rested"] is True
                      and cam["rest"]["off"] <= cam["tol"]["rest"],
                      f"owner={cam['camera'] and cam['camera']['owner']} rest={cam['rest']} "
                      f"handoffs={cam['handoffs']} tolerances={cam['tol']} — the manifest asks for no "
                      f"camera, so the stage holds it for the whole pass")

                # ---- §4.4b: the handles reach the picture ----------------------------------------
                # A handle read back off the diagnostic surface proves the GRAPH evaluated it. It says
                # nothing about whether the instrument obeyed it. These runs differ by exactly one
                # handle each and are photographed at MID-PASSAGE, where the gate stands part open, so
                # a picture that did not move is a handle the instrument is not reading.
                br.evaluate("window.__cancel('before the handle rows'); 0")
                idle(br)
                br.evaluate("window.__show('host'); window.__mix(0.5); 0")
                br.sleep(0.5)

                def drew(name, over):
                    br.evaluate("window.__hostDraw(%s); 0" % json.dumps(over))
                    br.sleep(0.25)
                    return png(br, SHOTS / ("handle-" + name + ".png"))

                base_shot = drew("base", {})
                # THE BAR, AND WHY IT IS THE WORST POINT RATHER THAN THE MEAN. The seam threshold of
                # 6 of 255 says when two frames are the SAME PICTURE, and it is read here at the
                # strongest point a handle moved rather than averaged over the frame — because three
                # of these handles act on a part of the frame rather than on all of it. The squeeze
                # touches only the arriving work, which at mid-passage holds about half the frame, and
                # a real displacement there comes out as a small whole-frame mean. What makes the
                # worst point an honest bar and not a loose one is the row below it: the same pose
                # drawn twice is bit-identical, so every channel of movement measured here is the one
                # handle that was moved and nothing else.
                still = diff(base_shot, drew("base-again", {}))
                params_moved = {k: diff(base_shot, drew(k, {k: v})) for k, v in
                                (("jamb", 0.0), ("teeth", 24), ("swing", 1.0),
                                 ("press", 0.0), ("lead", 0.0))}
                check(BROWSER_ROWS[19],
                      still == (0.0, 0)
                      and all(mx > SEAM for _, mx in params_moved.values()),
                      "; ".join(f"{k} moves the frame by {mn:.4f} of 255 on the mean and {mx} at its "
                                f"strongest point" for k, (mn, mx) in params_moved.items())
                      + f"; the same pose drawn twice moves it by {still[0]} at {still[1]}, so nothing "
                      f"here is drift. The bar is the seam threshold of {SEAM} read at the strongest "
                      f"point: the squeeze acts on the arriving work alone and comes out small on a "
                      f"whole-frame mean while moving {params_moved['press'][1]} channels where it "
                      f"acts")

                gate_moved = {k: diff(base_shot, drew(k, {k: v})) for k, v in
                              (("slotPlace", 0.25), ("slotHalf", 0.30), ("slotAxis", 0))}
                check(BROWSER_ROWS[20],
                      all(mx > SEAM for _, mx in gate_moved.values()),
                      "; ".join(f"{k} moves the frame by {mn:.4f} of 255 on the mean and {mx} at its "
                                f"strongest point" for k, (mn, mx) in gate_moved.items())
                      + "; the slot's place moves where the gate opens, its width moves how long the "
                        "two leaves part along a straight edge before the jamb breaks into teeth, and "
                        "its axis turns a gate that opens sideways into one that parts up and down")

                # ---- THE FLEET'S JUDGES' CHANNEL -------------------------------------------------
                # Two things are asked of it, and the first matters more than the second. It has to
                # REST AT NOTHING: a score that never names the channel must draw the module's own
                # frame to the bit, because this is the one handle the lab module has no counterpart
                # for and every two-road comparison above would be worthless if it moved the picture
                # on its own. And standing, it has to draw THE CUT — the two leaves and the opening
                # between them — rather than a tinted photograph, which is what the blue channel
                # answers: the cut map writes none at all, and the photographs cannot help it.
                off_shot = drew("mask-off", {"mask": 0})
                on_shot = drew("mask-on", {"mask": 1})
                rests = diff(base_shot, off_shot)
                moved_mask = diff(base_shot, on_shot)
                ch = channels(on_shot)
                check(BROWSER_ROWS[23],
                      rests == (0.0, 0) and moved_mask[1] > SEAM
                      and ch[2][1] == 0 and ch[0][1] == 255 and ch[1][1] == 255,
                      f"resting at nothing it moves the frame by {rests[0]} at {rests[1]}, so the "
                      f"module's own picture is drawn to the bit. Standing, it moves the frame by "
                      f"{moved_mask[0]:.4f} of 255 on the mean and {moved_mask[1]} at its strongest "
                      f"point, and the frame it draws runs red to {ch[0][1]} where the leaf opening "
                      f"toward the low end of the gate's axis stands, green to {ch[1][1]} where the "
                      f"other one stands, and blue to {ch[2][1]} — no blue anywhere, which is what "
                      f"says this frame is the cut and not the photographs")

                # ---- THE DOORS, READ ON THE DRAWING BUFFER ---------------------------------------
                # The rows above read the doors as PICTURES on the frame the suite runs at. This row
                # reads the instrument's own reading of them, on the grid the shader samples on and on
                # grids the suite hands it — including one far coarser than any device draws. Both
                # doors hold on every one of them, and the reason is algebra rather than tolerance:
                # at the entry door both openings are exactly 0, so the mask's two halves are one
                # number and its own negation about a half and they sum to 1 at every sample; at the
                # exit door the teeth close and both leaves have opened by the full reach, so the
                # first sample centre of any buffer — which stands at half a sample — falls outside
                # both leaves. The row also states that away from a door nothing is read at all.
                GRIDS = [(VW, VH), (780, 1688), (24, 40), (7, 11)]
                door_reads = []
                for gw, gh in GRIDS:
                    for at, label in ((0, "entry"), (1, "exit")):
                        v = js(br, "return window.__values(%s);"
                               % json.dumps({"mix": at, "bufWidth": gw, "bufHeight": gh}))
                        door_reads.append((gw, gh, label, v))
                away = js(br, "return window.__values(%s);" % json.dumps({"mix": 0.5}))
                doors_whole = (all(v["doorSteps"] == 0 and v["doorWhyNo"] is None
                                   and v["doorGrid"] == {"w": gw, "h": gh, "drawn": True}
                                   for gw, gh, _, v in door_reads)
                               and away["doorGrid"] is None and away["doorWhyNo"] is None
                               and away["doorSteps"] is None)
                check(BROWSER_ROWS[21], doors_whole,
                      "; ".join(f"the {lab} door on a {gw} x {gh} buffer: "
                                f"{v['doorSamples']} samples read across the gate's own axis, worst "
                                f"departure {v['doorWorst']}, {v['doorSteps']} whole channel steps of "
                                f"255"
                                for gw, gh, lab, v in door_reads)
                      + f"; away from a door nothing is read (grid {away['doorGrid']}). The departure "
                        f"is counted in the frame's own eight-bit steps, which is a ceiling of what "
                        f"the buffer can show rather than an estimate of it, so no threshold of this "
                        f"instrument's own choosing stands anywhere in the reading")

                # ---- THE PINNED NUMBERS OF THE SWEEP, MEASURED -----------------------------------
                # His 15:13 word on static parameters and his 19:13/19:21 words making the derivation
                # the law: a number a record could set belongs on a handle, and a number no
                # measurement reaches stays pinned and is NAMED. The instrument carries that sweep as
                # a block; this row is what keeps the block from becoming prose. It drives the two
                # clamps the sweep calls its live ones and reads back that each binds at exactly the
                # number it is named at — so either number moving in the file reddens this.
                #
                # The two are SECOND clamps, applied after the host's fit has carried the slot from
                # the file into the frame. The bench pair seats the departing work at about 0.36 along
                # the gate's axis, so the fit magnifies distance from the middle: a slot at 0.30 of the
                # FILE wants to stand at −0.05 of the frame and a slot at 0.70 wants 1.05, both outside
                # it, and a width of 0.30 of the file wants 0.82 of the frame.
                def slot_of(over):
                    return js(br, "return window.__values(%s);" % json.dumps(over))

                low = slot_of({"slotPlace": 0.30})
                high = slot_of({"slotPlace": 0.70})
                wide = slot_of({"slotHalf": 0.30})
                thin = slot_of({"slotHalf": 0.02})
                k = low["seating"]
                floor_dead = abs(thin["half"] - 0.02 / k) < 1e-9 and thin["half"] > 0.02
                check(BROWSER_ROWS[24],
                      low["slot"] == 0.06 and high["slot"] == 0.94 and wide["half"] == 0.30
                      and floor_dead,
                      f"seated at {k:.4f} along the gate's axis: a slot at 0.30 of the file wants "
                      f"{(0.30 - 0.5) / k + 0.5:.4f} of the frame and is held at {low['slot']}; one at "
                      f"0.70 wants {(0.70 - 0.5) / k + 0.5:.4f} and is held at {high['slot']}; a width "
                      f"of 0.30 of the file wants {0.30 / k:.4f} and is held at {wide['half']}. AND THE "
                      f"THIRD CLAMP CANNOT BIND, which the sweep says out loud rather than leaving to "
                      f"be found: the seating scale is a cover fit divided by ZOOM, so it is always "
                      f"below 1 and can only WIDEN a seated slot — the thinnest width the handle "
                      f"allows, 0.02, seats to {thin['half']:.4f} and never meets its own floor. It is "
                      f"kept because it is the lab module's own line (gates.js:519) and it decides "
                      f"nothing"
                      + (f"; a record could set none of the three — no reading says how near an edge a "
                         f"slot may stand or how wide it may be, and driving the width from voidShare "
                         f"would re-make the confusion the module's own `facing` term was added to fix"))

                kept = sorted(p.name for p in SHOTS.glob("*.png"))
                check(BROWSER_ROWS[22],
                      len(kept) >= 20 and all((SHOTS / k).stat().st_size > 1000 for k in kept),
                      f"{len(kept)} captures under {SHOTS.relative_to(ROOT)}: the five poses on both "
                      f"roads, the seven sampled instants, the frame after a resize, the two seeded "
                      f"runs and the twelve handle runs")

    shutil.rmtree(BENCH, ignore_errors=True)

    # ============================================================================================
    # THE RED-ON-BUG PROOFS. One of the module's own repairs reverted at a time, in the artifact the
    # browser actually loads. The pack served is changed and the host is re-stamped with the digest
    # of the bytes it is handed, which is what the build does; the file on disk is never touched, so
    # no working tree can be left changed by a proof.

    def exit_door_reader(tag):
        """The exit door, drawn and read: the picture the instrument lays down at `mix` 1, and the
        instrument's own reading of that same door on the buffer it drew it on."""
        def read(br):
            br.evaluate("window.__mix(1); window.__show('host'); 0")
            br.sleep(0.7)
            br.evaluate("window.__hostDraw(); 0")
            br.sleep(0.3)
            v = js(br, "return window.__values();")
            w = int(br.evaluate("String((document.querySelector('canvas[aria-hidden]') || "
                                "document.querySelector('canvas')).width)"))
            h = int(br.evaluate("String((document.querySelector('canvas[aria-hidden]') || "
                                "document.querySelector('canvas')).height)"))
            return {"steps": v["doorSteps"], "why": v["doorWhyNo"], "w": w, "h": h,
                    "png": png(br, SHOTS / ("red-exit-%s.png" % tag))}
        return read

    # RED 1 — THE TEETH LEFT BITING AT THE FAR DOOR. `smoothstep(1, 0.85, d)` closes the bite as the
    # dial reaches its end, which is what makes both leaves clear the frame exactly (gates.js:565-569).
    # Reverted, a tooth that opens less than its neighbours leaves a strip of the DEPARTING work
    # standing in a door whose law says one whole arriving work.
    bug1 = REGION.replace("* smoothstep(1, 0.85, d)", "* 1.0", 1)
    base1 = on_bench(exit_door_reader("repair-standing"))
    red1 = on_bench(exit_door_reader("bite-left-open"), pack_text=bug1)
    if base1 and red1:
        glass1 = work_in_the_frame(PHOTOS[1], base1["w"], base1["h"], 1 + 2 * 0.12 + 0.03)
        ok_mean, _ = apart(base1["png"], glass1)
        bad_mean, bad_max = apart(red1["png"], glass1)
        moved1 = diff(base1["png"], red1["png"])
    else:
        ok_mean = bad_mean = bad_max = None
        moved1 = (None, None)
    check(RED_ROWS[0],
          bug1 != REGION and base1 and red1
          and base1["steps"] == 0 and base1["why"] is None
          and red1["steps"] > 0 and red1["why"] and "the exit door leaks" in red1["why"]
          and ok_mean is not None and ok_mean <= SEAM
          and moved1[1] is not None and moved1[1] > SEAM,
          f"with the repair standing the exit door reads {base1 and base1['steps']} whole channel "
          f"steps of the wrong work and stands {ok_mean if ok_mean is None else round(ok_mean, 4)} "
          f"of 255 from glassgrid.jpg. With the bite left open at the far door a tooth that opens "
          f"less than its neighbours leaves a strip of the DEPARTING work standing in that door: the "
          f"drawn frame moves by {moved1[0] if moved1[0] is None else round(moved1[0], 4)} of 255 on "
          f"the mean and {moved1[1]} at its strongest point. AND THIS IS WHY THE INSTRUMENT READS ITS "
          f"OWN DOORS. Against its own file that leaking door stands "
          f"{bad_mean if bad_mean is None else round(bad_mean, 4)} of 255 away at a worst channel of "
          f"{bad_max} — UNDER the project's seam bar of {SEAM}, so the picture rows above would have "
          f"called it one whole work. The instrument's own reading did not: it reported "
          f"{red1 and red1['steps']} whole channel steps and refused, «{red1 and red1['why']}»")

    # RED 2 — THE SEATING REMOVED. The slot's place and width are shares of the FILE, and the file is
    # cover-fitted into the frame and pulled in by ZOOM before it reaches it, so both are carried
    # through that same fit (gates.js:514-521). With the fit's own scale forced to 1 the gate opens
    # where nothing measured it: the same pose draws a different frame.
    def read_mid(br):
        br.evaluate("window.__show('host'); window.__mix(0.5); 0")
        br.sleep(0.7)
        br.evaluate("window.__hostDraw(%s); 0" % json.dumps({"slotPlace": 0.3}))
        br.sleep(0.3)
        v = js(br, "return window.__values(%s);" % json.dumps({"slotPlace": 0.3}))
        return {"slot": v["slot"], "half": v["half"], "seating": v["seating"],
                "png": png(br, SHOTS / ("red-seat-%d.png" % round(1000 * v["seating"])))}

    bug2 = REGION.replace("var k = vert ? f[0] : f[1];", "var k = 1;", 1)
    base2 = on_bench(read_mid)
    red2 = on_bench(read_mid, pack_text=bug2)
    moved2 = diff(base2["png"], red2["png"]) if (base2 and red2) else (None, None)
    check(RED_ROWS[1],
          bug2 != REGION and base2 and red2
          and abs(base2["seating"] - 1) > 1e-6 and abs(red2["seating"] - 1) < 1e-12
          and moved2[0] is not None and moved2[0] > SEAM,
          f"the departing work is seated into this frame at {base2 and round(base2['seating'], 4)} "
          f"along the gate's own axis, so a slot standing at 0.3 of the FILE lands at "
          f"{base2 and round(base2['slot'], 4)} of the frame with a half-width of "
          f"{base2 and round(base2['half'], 4)}. With the seating removed the same request lands at "
          f"{red2 and round(red2['slot'], 4)} with a half-width of {red2 and round(red2['half'], 4)} "
          f"— the file's own share read as if it were the frame's — and the frame moves by "
          f"{moved2[0] if moved2[0] is None else round(moved2[0], 4)} of 255 (worst channel "
          f"{moved2[1]}), against a seam threshold of {SEAM}")

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
