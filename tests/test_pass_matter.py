#!/usr/bin/env python3
"""PASS-API-V1 — the matter instrument on the host's frame.
Run: python3 tests/test_pass_matter.py

Root: his word 2026-08-14 08:39 — continue the effect farm, and integrate only green conforming
instruments. The composed passage on the critical path needs a second instrument beside the woven
one, and `matter` is the pick because it carries disassembly and assembly, which the woven
instrument does not. docs/design/PASS-API-V1.md §7 (GPU and resources), §8 (the manifest) and §9's
conformance rows 7, 9, 10, 13, 14, 15, 16 and 22 are what this file makes real; the lifecycle rows
stay in tests/test_pass_api.py and are untouched.

WHAT IS COMPARED, AND AGAINST WHAT.

  The doors. At the dial's two ends one whole work stands. Each is measured against ITS OWN FILE —
  the picture cover-fitted into the frame and pulled in by the headroom the drag needs (the module's
  own ZOOM of 1.17) — inside the project's seam threshold of 6 of 255. A door that carried a
  ten-thousandth of the other photograph would fail this, which is the point of it.

  The five poses. The host's frame is compared against the LAB MODULE's own frame, on one pose both
  roads were driven by: the same dial, the same four params, the same die, the same second. Two
  roads of one frame, never two guesses at one. The five poses walk the dial from door to door, so
  the response curve is measured along its whole length rather than at its ends.

  No empty frame. The module asks its own context to preserve the drawing buffer (matter.js:250) and
  §7 refuses that. The flag stood in for a redraw: the module draws on demand and needs the frame
  that was already there handed back between two draws. The host draws every frame and redraws on
  resize, so the rows below sample the pass at seven instants and once across a change of viewport,
  and each frame has to stand as a picture.

  The lab tree is READ ONLY and is found at $TLVPHOTOS_LAB_ROOT, defaulting to the immersive
  worktree's lab. Absent, every browser row here is a pinned SKIP that names the missing path —
  never a silent pass.
"""
import base64
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
MODULE = LAB / "effects" / "matter.js"

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
# instrument and evidence that is deleted is no evidence. They stay on disk where the last run left
# them and outside the history, since every run writes eleven megabytes of them afresh.
SHOTS = ROOT / "tests" / "captures" / "pass-matter"

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
DIE = 4.91016            # the die lab/data/scores' own weave score carries, so both suites roll one
DURATION_MS = 3000
WITHIN_MS = 500


def matter_score(pair_a="a", pair_b="b", **statics):
    """The score, with a track for every one of the nine handles (§4.4b).

    The four params rest at the module's own declared defaults (matter.js:222-225): loosening 0.6,
    drift 0.45, gathering 0.3, grain 0.45. The two judge channels rest at 1, which is where the
    module holds them. `mix` reads the transaction's own progress and `clock` the second the host
    hands down — that second is the only place the module ever read time, and it read its own
    accumulated frame clock there (matter.js:321).
    """
    P = {"loosen": 0.6, "drift": 0.45, "gather": 0.3, "grain": 0.45,
         "shade": 1, "travel": 1, "seed": DIE}
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
        "intent": "the first work loosens into a material and the second gathers out of the same "
                  "material; a band of loose matter travels across the frame with one work whole "
                  "ahead of it and one whole behind (lab/effects/matter.js:1-5, its own header)",
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
            "id": "matter-main",
            "instrument": {"id": "matter", "api": 1},
            "voice": "letter",
            "roles": ["disassembly", "mystery", "assembly"],
            "levels": ["SURFACE", "TEXTURE"],
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
        "quality": {v: {"renderScale": None, "cues": {"matter-main": {"resources": res[v]}}}
                    for v in ("lean", "standard", "rich")},
        "provenance": {"source": "lab/effects/matter.js's own declared defaults and constants",
                       "measuredAt": None, "by": "tests/test_pass_matter.py"},
    }


# ---------------------------------------------------------------- bake once
build_site.SITE_CONFIG = dict(build_site.SITE_CONFIG)
build_site.SITE_CONFIG["pass"] = {"visualLayer": "pass", "diagnostics": "on"}

TMP = Path(tempfile.mkdtemp(prefix="synth_passmatter_"))
build_site.OUT = TMP
build_site.build(SITE_URL)
LAYER = (TMP / "pass-layer.js").read_text(encoding="utf-8")
# The instrument's own region of the BUILT file — the real artifact, comments stripped as it ships —
# which is what the ownership fence and every other string row below are read against.
# Since 2026-08-14 the instruments ship in their OWN built file, which the host fetches by address,
# version and digest. A row about the HOST reads LAYER; a row about this instrument's own mathematics
# reads its region of PACK.
PACK = (TMP / "pass-pack.js").read_text(encoding="utf-8")
REGION = PACK.split("function matterInstrument()")[1].split("function gearsInstrument()")[0]

# ---------------------------------------------------------------- string rows

OWNED = ["createElement", "getContext", "requestAnimationFrame", "addEventListener",
         "performance.now", "Date.now", "new Image", "setTimeout", "setInterval"]
held = [s for s in OWNED if s in REGION]
check("PASS-MATTER the instrument creates no context, no canvas, no loop and no listener",
      not held,
      "§1.2's fence, read against the instrument's own region of the file: none of the nine ways of "
      "owning hardware appears there, so the module's canvas, its WebGL 1 context, its frame loop "
      "and its resize listener all stayed in the lab"
      if not held else "the instrument's region holds " + ", ".join(held))

check("PASS-MATTER every handle the instrument publishes is a handle a score can drive",
      all(("%s: { min" % h) in REGION for h in
          ["mix", "clock", "loosen", "drift", "gather", "grain", "seed", "shade", "travel"]),
      "§4.4b: nine handles, and the drift of the field reads the `clock` handle rather than the "
      "frame clock the module accumulated for itself (matter.js:398-405)")

check("PASS-MATTER the field's drift reads the handed-down second and no clock of its own",
      "(st.reduced ? 0 : st.t) * 0.11 * clamp(st.drift, 0, 1)" in REGION
      and "t: h.clock" in REGION,
      "matter.js:321 read `t`, its own accumulated frame time; here it is the `clock` handle, which "
      "is what makes the seeded repeat below mean anything")

check("PASS-MATTER the manifest leaves the drawing buffer unpreserved",
      "gl: { preserveDrawingBuffer: false }" in REGION,
      "the module asks its own context for a preserved buffer (matter.js:250) and §7 refuses a "
      "manifest that asks for it; the redraw it stood in for is the host's own frame loop")

check("PASS-MATTER the shader carries no version header of its own",
      "#version" not in REGION and "#version" not in MODULE.read_text(encoding="utf-8"),
      "so the host's translator stamps the one header this shader needs and no second one arrives")

# The response curve and the field constants, read out of the lab module and out of the built file.
# A port that re-derived either would differ here by a digit.
LABTXT = MODULE.read_text(encoding="utf-8")


def numbers(text, pattern):
    m = re.search(pattern, text)
    return [float(x) for x in re.findall(r"-?\d+\.?\d*", m.group(1))] if m else []


lab_q = numbers(LABTXT, r"FEEL_Q = \[([^\]]+)\]")
port_q = numbers(REGION, r"FEEL_Q = \[([^\]]+)\]")
check("PASS-MATTER the response curve is carried digit for digit out of the lab module",
      len(lab_q) == 21 and lab_q == port_q
      and "FEEL_D0 = 0.05" in LABTXT and "FEEL_D0 = 0.05" in REGION,
      f"twenty-one shares and the dead band, unchanged: {len(port_q)} numbers matched, first "
      f"{port_q[1] if len(port_q) > 1 else None}, last held {port_q[-1] if port_q else None} — the "
      f"module's own card asks a port to hand the same mix-to-feel mapping through (matter.md §11.3)")

CONSTANTS = [("GRAIN_MIN = 4", "the coarse grain's near end, in cells across the frame's height"),
             ("GRAIN_MAX = 34", "and its far end — past forty a cell is smaller than a window bay"),
             ("GRAIN_FINE = 3.0", "the fine grain rides at three times the coarse one"),
             ("AMP = 0.07", "how far the picture is dragged at the fullest loosening"),
             ("LADDER = 0.6", "six parts plain ladder against four parts grain"),
             ("0.04 + 0.26 * clamp", "the gathering's own range, the band's width"),
             ("0.5 + 0.10", "the threshold travels a tenth past either end of the field")]
missing_const = [c for c, _ in CONSTANTS if c not in LABTXT or c not in REGION]
check("PASS-MATTER every field constant stands at the number the lab module gives it",
      not missing_const,
      "; ".join("%s — %s" % (c, why) for c, why in CONSTANTS) if not missing_const
      else "these differ: " + ", ".join(missing_const))

check("PASS-MATTER the host binds uniforms by declared name, never by position or a written list",
      "getUniformLocation(p, u.name)" in LAYER and "gl.uniform1f(U.uTau" not in LAYER
      and "gl.uniform1f(U.uGrainA" not in LAYER,
      "nine of this instrument's fourteen uniforms have no place in the lab carrier's own fixed "
      "list (matter.md §9.1); the host reads the manifest")

# Every uniform the manifest declares is a name the shader actually spells, and the other way about.
declared = set(re.findall(r'\{ name: "(u\w+)", type:', REGION))
spelled = set(re.findall(r'uniform \w+ (u\w+);', REGION))
check("PASS-MATTER the manifest's declared names and the shader's own names are one set",
      declared == spelled and len(declared) == 14,
      f"{len(declared)} declared, {len(spelled)} spelled; "
      f"declared only: {sorted(declared - spelled)}; spelled only: {sorted(spelled - declared)}")

# ---------------------------------------------------------------- browser rows

BROWSER_ROWS = [
    "PASS-MATTER §8     · the manifest carries every field the contract names, in its shape",
    "PASS-MATTER row 7  · door 0 stands the departing work, measured against its own file",
    "PASS-MATTER row 7  · door 0 carries no trace of the arriving work",
    "PASS-MATTER row 7  · door 1 stands the arriving work, measured against its own file",
    "PASS-MATTER row 7  · door 1 carries no trace of the departing work",
    "PASS-MATTER the host's frame and the lab module's frame agree at all five poses",
    "PASS-MATTER §7     · no empty frame at any sampled instant of the pass",
    "PASS-MATTER §7     · the frame after a change of viewport is drawn, not a kept buffer",
    "PASS-MATTER row 10 · a seeded run repeats to the pixel",
    "PASS-MATTER row 14 · textures, programmes and framebuffers return to their baseline after ten runs",
    "PASS-MATTER row 15 · the console stays clean",
    "PASS-MATTER row 22 · the census shows granted against declared, and neither overruns",
    "PASS-MATTER §7     · a manifest asking for a preserved drawing buffer is refused, with its reason",
    "PASS-MATTER §7     · a uniform bound to a name the shader lacks is refused, with its reason",
    "PASS-MATTER §7     · one canvas, one context, two source textures, one pass a frame",
    "PASS-MATTER §7     · a shader already at GLSL ES 3.00 receives no second version header",
    "PASS-MATTER the real transaction road: curtain up, one pass drawn, exactly one dock at the end",
    "PASS-MATTER row 9  · one camera authority through a real pass, and the pose rests on the arrival",
    "PASS-MATTER §4.4b  · the gathering, the grain and the loosening reach the PICTURE",
    "PASS-MATTER row 16 · the captures are kept as evidence",
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
    """The work as the instrument seats it: cover-fit, then the centre crop the drag is paid for
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


def apart(p, work):
    from PIL import Image, ImageChops, ImageStat
    a = Image.open(p).convert("RGB")
    if a.size != work.size:
        return 255.0, 255.0
    st = ImageStat.Stat(ImageChops.difference(a, work))
    return sum(st.mean) / 3.0, max(m for _, m in st.extrema)


def bench_dir():
    """The bench's own served root: the BUILT pass-layer.js (the real artifact, namespace applied
    and comments stripped), the lab module unchanged, the two photographs, and the page that stands
    the two roads of one frame side by side."""
    d = Path(tempfile.mkdtemp(prefix="synth_matterbench_"))
    shutil.copy2(TMP / "pass-layer.js", d / "pass-layer.js")
    # The host fetches its pack by address and weighs its bytes, so the bench root serves the
    # built pack beside the built host: the same two files a visitor gets, unaltered.
    shutil.copy2(TMP / "pass-pack.js", d / "pass-pack.js")
    shutil.copy2(MODULE, d / "matter.js")
    (d / "photos").mkdir()
    for p in PHOTOS:
        shutil.copy2(p, d / "photos" / p.name)
    shutil.copy2(ROOT / "tests" / "fixture_pass_matter.html", d / "index.html")
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


if not chrome_available():
    for r in BROWSER_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
elif missing:
    for r in BROWSER_ROWS:
        skip(r, "the lab tree is read-only source material and is absent here: " + missing[0])
else:
    shutil.rmtree(SHOTS, ignore_errors=True)
    SHOTS.mkdir(parents=True, exist_ok=True)
    BENCH = bench_dir()
    SCORE_JSON = json.dumps(matter_score())
    with serve(BENCH) as base:
        with Browser(width=VW, height=VH) as br:
            br.navigate(base + "/index.html")
            if not ready(br):
                for r in BROWSER_ROWS:
                    skip(r, "the bench never came up: "
                         + br.evaluate("JSON.stringify(window.__errs||[])"))
            # An instrument the host refuses at registration draws nothing, so every row below it
            # would read as a crash. It reads as what it is instead: the whole set red, with the
            # host's own reason for the refusal.
            elif not js(br, "return !!window.__exPass.bench.manifest('matter');"):
                why = js(br, "var e = window.__host.report().events.filter(function(x){"
                             "return x.name === 'manifest-refused';});"
                             "return e.length ? e[e.length - 1].why : null;")
                for r in BROWSER_ROWS:
                    check(r, False, "the host registered no «matter» instrument: " + str(why))
            else:
                # ---- §8: the manifest, read off the registered instrument -----------------------
                m = js(br, "return window.__exPass.bench.manifest('matter');")
                zoom = m["framings"]["0"]["coverCrop"]
                res = m["resources"]
                shape = (
                    m["id"] == "matter" and m["api"] == 1 and m["arity"] == 2
                    and m["roles"] == ["disassembly", "mystery", "assembly"]
                    and sorted(m["params"]) == ["drift", "gather", "grain", "loosen"]
                    and len(m["handles"]) == 9
                    and all(set(h) >= {"min", "max", "def"} for h in m["handles"].values())
                    and m["neutrals"] == {"a": 0, "b": 1}
                    and m["doors"]["in"]["handle"] == "mix" and m["doors"]["in"]["value"] == 0
                    and m["doors"]["out"]["handle"] == "mix" and m["doors"]["out"]["value"] == 1
                    and sorted(m["framings"]) == ["0", "1"]
                    and m["framings"]["0"] == m["framings"]["1"]
                    and abs(zoom - (1 + 2 * 0.07 + 0.03)) < 1e-12
                    and m["camera"] == {"needs": "none", "authority": "stage"}
                    and len(m["passes"]) == 1 and len(m["passes"][0]["uniforms"]) == 14
                    and sorted(res) == ["lean", "rich", "standard"]
                    and all("bytesEstimate" in res[v] and res[v]["programs"] == 1
                            and res[v]["passes"] == 1 and res[v]["textureSlots"] == 2
                            for v in res)
                    and m["capabilities"] == ["webgl2"] and m["decline"]
                    and m["provenance"]["labPath"] == "lab/effects/matter.js"
                    and m["provenance"]["commit"] == "e0f1b91"
                    and m["readiness"] == "production-ready"
                    and "matter" in js(br, "return window.__host.report().registered;"))
                check(BROWSER_ROWS[0], shape,
                      f"nine handles, fourteen uniforms in one pass, the crop {zoom} that the drag's "
                      f"headroom is paid for with, resources declared for three tiers with a byte "
                      f"estimate of {res['standard']['bytesEstimate']}, and the lab commit "
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
                # The pass is pinned at each instant in turn and photographed. A frame that was
                # never drawn would be the canvas's own flat background, which has no spread and no
                # distance from itself.
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

                # The frame is redrawn at the new size rather than handed back from a kept buffer.
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
                      f"(textures/programmes/framebuffers); the programme cache holds one entry per "
                      f"branch and outlives every transaction")

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
                r = js(br, """
                  var m = JSON.parse(JSON.stringify(window.__exPass.bench.manifest('matter')));
                  m.gl.preserveDrawingBuffer = true;
                  var ok = window.__exPass.bench.register({name:'matter-preserve', manifest:m,
                      values:function(){return {dial:0,grainA:4,grainB:12,ladder:0.6,gather:0.04,
                          tau:0,drift:[0,0],loosen:0,guard:0};},
                      fit:function(){return [1,1,0,0];},
                      prepare:function(){return {take:false};}, start:function(){}, frame:function(){}});
                  var evs = window.__host.report().events.filter(function(e){return e.name==='manifest-refused';});
                  return {ok: ok, why: evs.length ? evs[evs.length-1].why : null,
                          registered: window.__host.report().registered};
                """)
                check(BROWSER_ROWS[12],
                      r["ok"] is False and r["why"] and "preserved" in r["why"]
                      and "matter-preserve" not in r["registered"],
                      f"registered={r['ok']} why={r['why']}")

                r = js(br, """
                  var m = JSON.parse(JSON.stringify(window.__exPass.bench.manifest('matter')));
                  m.passes[0].uniforms.push({name:'uPointer', type:'vec2', source:'pointer'});
                  var ok = window.__exPass.bench.register({name:'matter-pointer', manifest:m,
                      values:function(){return {dial:0,grainA:4,grainB:12,ladder:0.6,gather:0.04,
                          tau:0,drift:[0,0],loosen:0,guard:0};},
                      fit:function(){return [1,1,0,0];},
                      prepare:function(){return {take:false};}, start:function(){}, frame:function(){}});
                  var evs = window.__host.report().events.filter(function(e){return e.name==='manifest-refused';});
                  return {ok: ok, why: evs.length ? evs[evs.length-1].why : null,
                          registered: window.__host.report().registered};
                """)
                check(BROWSER_ROWS[13],
                      r["ok"] is False and r["why"] and "uPointer" in r["why"]
                      and "cannot supply" in r["why"] and "matter-pointer" not in r["registered"],
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
                  var m = window.__exPass.bench.manifest('matter');
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
                # This instrument claims no camera: its manifest asks for none and its cue leaves the
                # authority with the stage. The row reads the POSE, never the picture.
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
                # says nothing about whether the instrument obeyed it. These four runs differ by
                # exactly one handle each and are photographed, so a picture that did not move is a
                # handle the instrument is not reading.
                br.evaluate("window.__show('host'); 0")
                shot = {}
                for name, extra in (("base", {}), ("gather", {"gather": 1.0}),
                                    ("grain", {"grain": 1.0}), ("loosen", {"loosen": 0.0})):
                    js(br, "return window.__offer(%s, {clock: 1.5, progress: 0.5});"
                       % json.dumps(matter_score(**extra)))
                    br.sleep(0.7)
                    shot[name] = png(br, SHOTS / ("handle-" + name + ".png"))
                    br.evaluate("window.__cancel('handle row'); 0")
                    idle(br)
                moved = {k: diff(shot["base"], shot[k]) for k in ("gather", "grain", "loosen")}
                check(BROWSER_ROWS[18],
                      all(mn > SEAM for mn, _ in moved.values()),
                      "; ".join(f"{k} moves the frame by {mn:.4f} of 255 (worst channel {mx})"
                                for k, (mn, mx) in moved.items())
                      + f"; the seam threshold is {SEAM}")

                kept = sorted(p.name for p in SHOTS.glob("*.png"))
                check(BROWSER_ROWS[19],
                      len(kept) >= 20 and all((SHOTS / k).stat().st_size > 1000 for k in kept),
                      f"{len(kept)} captures under {SHOTS.relative_to(ROOT)}: the five poses on both "
                      f"roads, the seven sampled instants, the frame after a resize, the two seeded "
                      f"runs and the four handle runs")

    shutil.rmtree(BENCH, ignore_errors=True)

shutil.rmtree(TMP, ignore_errors=True)

# A row that never ran is no pass. Anything declared above and never reached is recorded here with
# that as its reason, so a run cut short reads as a red rather than as a shorter green suite.
ran = {name for name, _, _ in results}
for name in BROWSER_ROWS:
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
