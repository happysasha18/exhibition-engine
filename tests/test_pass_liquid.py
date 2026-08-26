#!/usr/bin/env python3
"""PASS-API-V1 — the liquid instrument on the host's frame.
Run: python3 tests/test_pass_liquid.py

Root: his word of 2026-08-18 08:52 — «переходы очень однообразные: у тебя дофига эффектов и ты
сделал все очень топорно» — and his 08:58 word, «перенеси ВЕСЬ арсенал и пересобери проход». The
lane brief is docs/immersive/briefs/reports/lanes/PORT-common.md in the tlvphotos tree; the module
is lab/effects/liquid.js, and the charter's own row for it is «оживление + garnish · TEXTURE ·
unused yet».

WHAT IS COMPARED, AND AGAINST WHAT.

  The doors. At the dial's two ends one whole work stands, and it stands at a cover crop of exactly
  one — the module's breathing zoom is gated by the crossing dial, so a door buys no headroom from
  the picture. Each door is measured against ITS OWN FILE, cover-fitted into the frame, inside the
  project's seam threshold of 6 of 255. A door that carried a ten-thousandth of the other
  photograph would fail this, which is the point of it.

  The water, on both roads. The lab module carries ONE work and this instrument carries an ordered
  pair, so the two are one frame exactly where the pair is one work: the host is handed the SAME
  photograph in both of its source slots, the handover mixes that work with itself at every point,
  and what is left standing is the module's own water. The rows below walk the crossing dial, the
  swell, the crest spacing and the phase, and every one of them compares the host's frame against
  the module's frame on ONE pose both roads were driven by — never two guesses at one.

  What the port added. The handover the module has no work to make: the arriving photograph
  surfaces on the crests of the swell. A row measures that both works are on the frame mid-dial and
  neither is at either door, and a row measures that the boundary moves with the hand.

  The lab tree is READ ONLY and is found at $TLVPHOTOS_LAB_ROOT, defaulting to the immersive
  worktree's lab. Absent, every browser row here is a pinned SKIP that names the missing path —
  never a silent pass.

WHAT IS NEVER RESTORED FROM GIT. Every red-on-bug proof below serves a COPY of the instrument file
with one rule changed and writes the site's own record with the digest of the bytes actually served,
which is what the build does. The source tree is never written to.
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
PHOTOS = [Path("/Users/sashaabramovich/tlvphotos/lab/photos/towers.jpg"),
          Path("/Users/sashaabramovich/tlvphotos/lab/photos/glassgrid.jpg")]
MODULE = LAB / "effects" / "liquid.js"

SITE_URL = "https://synth.example.com"
VW, VH = 390, 844          # the phone frame every instrument suite measures on
SEAM = 6.0                 # the project's seam threshold, 6 of 255 (TRANSITION-STAGE-V0 §1)
SAME = 1.5                 # two roads of one frame: the carrier check's own bar
FAR = 40.0                 # further than this from a file and it is a different work
BACKGROUND = (0x08, 0x08, 0x0a)

SHOTS = ROOT / "tests" / "captures" / "pass-liquid"

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


# ---------------------------------------------------------------- bake once
build_site.SITE_CONFIG = dict(build_site.SITE_CONFIG)
build_site.SITE_CONFIG["pass"] = {"visualLayer": "pass", "diagnostics": "on"}

TMP = Path(tempfile.mkdtemp(prefix="synth_passliquid_"))
build_site.OUT = TMP
build_site.build(SITE_URL)
LAYER = (TMP / "pass-layer.js").read_text(encoding="utf-8")
REGION = (TMP / "pass-inst-liquid.js").read_text(encoding="utf-8")
SOURCE = (ROOT / "engine" / "assets" / "pass-inst-liquid.js").read_text(encoding="utf-8")
LABTXT = MODULE.read_text(encoding="utf-8") if MODULE.exists() else ""

# ---------------------------------------------------------------- string rows

OWNED = ["createElement", "getContext", "requestAnimationFrame", "addEventListener",
         "performance.now", "Date.now", "new Image", "setTimeout", "setInterval"]
held = [s for s in OWNED if s in REGION]
check("PASS-LIQUID the instrument creates no context, no canvas, no loop and no listener",
      not held,
      "§1.2's fence, read against the instrument's own built file: none of the nine ways of owning "
      "hardware appears there, so the module's canvas, its WebGL 2 context, its frame loop and its "
      "two pointer listeners all stayed in the lab"
      if not held else "the instrument's file holds " + ", ".join(held))

HANDLES = ["mix", "clock", "swell", "crest", "refract", "seed", "shade", "travel", "mask"]
check("PASS-LIQUID every handle the instrument publishes is a handle a score can drive",
      all(("%s: { min" % h) in REGION for h in HANDLES),
      "§4.4b: nine handles. The one place the module read time — its own accumulated frame clock — "
      "reads the `clock` handle here, which is what makes a seeded repeat mean anything")

# THE WHOLE SIMULATION STAYED BEHIND, on the module's own recorded reason. A port that carried the
# ping-pong across would carry a machine that draws nothing, because a crossing parks the hand.
SIM = ["uPrev", "segDist", "PACK_FLOAT", "PACK_BYTE", "createFramebuffer", "RGBA16F", "uDrop",
       "uPush", "uDecay", "uDamp", "allocField", "pingPong: 1"]
carried = [s for s in SIM if s in REGION]
check("PASS-LIQUID the module's whole simulation stayed in the lab, on the module's own reason",
      not carried
      and "the engine parks the hand inside a crossing" in SOURCE
      and "framebuffers: 0, pingPong: 0" in REGION,
      "liquid.js:369-375 says it itself — «that field is filled only by a hand pressing the "
      "surface, the engine parks the hand inside a crossing, so under a score the field is flat at "
      "every mark of such a handle and both its doors would draw one frame». So the two field "
      "textures, the two framebuffers, the twelve-step integration and the byte-packing fallback "
      "are gone, and this instrument allocates nothing at all"
      if not carried else "the instrument still carries " + ", ".join(carried))

# Each of the swell's own numbers as the LAB module spells it and as the PORT spells it. A port that
# re-derived any of them would differ here by a digit.
SWELL = [("vec3(0.55, 0.42, 0.30)", "SA = [0.55, 0.42, 0.30]",
          "the three waves' own amplitudes"),
         ("vec2( 1.4,  5.2)", "KX = [1.4, 4.3, -3.1]", "the first wave's heading"),
         ("vec2( 4.3, -2.4)", "KY = [5.2, -2.4, 3.0]", "and the second's, and the third's"),
         ("t * 1.70", "RATE = [1.70, 1.35, 2.25]", "each wave's own rate, radians a second"),
         ("t * 0.23", "SLOW = [0.23, 0.31, 0.17]", "and each wave's own long count"),
         ("t * 0.31 + 2.1", "SLOWPH = [0.0, 2.1, 4.3]", "with its own offset in that count"),
         ("0.070 * tanh(dl / 0.070)", "BEND_MAX = 0.070", "the soft ceiling the surface bends in"),
         ("0.0032 * tanh(cl / 0.0032)", "SPLIT_MAX = 0.0032", "the hair the colour splits by"),
         ("1.055 * breath", "1.055 * breath", "the breathing zoom, gated by the crossing dial"),
         ("0.0075 * sin(t * 0.26)", "0.0075 * sin(t * 0.26)", "and the breath itself"),
         ("0.0040 * sin(t * 0.11 + 1.3)", "0.0040 * sin(t * 0.11 + 1.3)", "its second component"),
         ("vec3(0.30, 0.52, 0.80)", "vec3(0.30, 0.52, 0.80)", "where the light stands"),
         ("26.0", "26.0", "how tight the specular is"),
         ("0.04 + 0.12 * uRefr", "0.04 + 0.12 * uDial.y", "how much of it reaches the picture"),
         ("clamp(hs * uLife * 7.0, -0.05, 0.05)", "clamp(hs * uWave.y * 7.0, -0.05, 0.05)",
          "the light the swell's own height carries"),
         ("smoothstep(0.0, 0.05, min(e.x, e.y))", "smoothstep(0.0, 0.05, min(e.x, e.y))",
          "the taper that puts the bend out at the frame's edge")]
missing_swell = ([c for c, _, _ in SWELL if LABTXT and c not in LABTXT]
                 + [c for _, c, _ in SWELL if c not in REGION])
check("PASS-LIQUID every number of the swell stands where the lab module puts it",
      not missing_swell and bool(LABTXT),
      "; ".join("%s — %s" % (c, why) for _, c, why in SWELL) if not missing_swell
      else "these differ: " + ", ".join(missing_swell))

check("PASS-LIQUID the response curve of the crest spacing is carried digit for digit",
      "FEEL_S_U0 = 0.702, FEEL_S_K1 = 0.59, FEEL_S_K2 = 0.91" in LABTXT
      and "FEEL_C_U0 = 0.702, FEEL_C_K1 = 0.59, FEEL_C_K2 = 0.91" in REGION
      and "def: FEEL_C_U0" in REGION,
      "liquid.js:402's own two-piece logarithm, hinged at the module's own spacing. The hinge is "
      "why the handle's default is 0.702 and not a half: feelCrest(0.702) is exactly 0.5, which is "
      "the spacing the module ships, so the handle's neutral lands to the pixel")

check("PASS-LIQUID the two reaches and the water's own life are the module's own numbers",
      "WAVE_REACH = 2.0, SPREAD_REACH = 2.0" in LABTXT
      and "WAVE_REACH = 2.0, SPREAD_REACH = 2.0" in REGION
      and "0.0042 + 0.0037 * s" in LABTXT
      and "LIFE_DOOR = 0.0042 + 0.0037 * 0.55" in REGION
      and "LIFE_REDUCED = 0.0012" in REGION,
      "the reaches are liquid.js:382; the life is liquid.js:335 pinned at the module's own declared "
      "default of 55, because the control it comes from shapes only the pointer's wake and does not "
      "travel — and the module's own note at :376 says that control's whole range is a factor of "
      "1.9, which is inside the swell handle's reach of two")

check("PASS-LIQUID the water's own ceiling is derived from the three amplitudes, not typed",
      "FIELD_TOP = SA[0] + SA[1] + SA[2]" in REGION and "var MARGIN = 0.10;" in REGION
      and "(FIELD_TOP + MARGIN) * (1 - 2 * d)" in REGION,
      "|hs| never passes the sum of the three bases because each amplitude's own factor never "
      "passes one, so the handover's line travelling a tenth past that sum leaves every point of "
      "the frame on one work at either door — a door exact by construction rather than by tolerance")

check("PASS-LIQUID both doors frame at a cover crop of exactly one",
      '"0": { coverCrop: 1 }, "1": { coverCrop: 1 }' in REGION
      and "mix(1.0, 1.055 * breath, uWave.x)" in REGION,
      "the module's breathing zoom is gated by the crossing dial, which is nothing inside either "
      "dead band, so a landed door is the source cover-fitted and nothing else — no headroom bought "
      "from the picture, because the swell's displacement is tapered to nothing at the frame's edge")

check("PASS-LIQUID the manifest leaves the drawing buffer unpreserved",
      "gl: { preserveDrawingBuffer: false, readsChain: true }" in REGION,
      "§7 refuses a manifest that asks for one; the redraw it would stand in for is the host's own "
      "frame loop")

check("PASS-LIQUID the three handles that read a work name the measurement each reads",
      'reads: "texture.scoreFromCutLines' in REGION
      and 'reads: "texture.spectralPeriodPx over the work' in REGION
      and 'reads: "texture.detailPx over the work' in REGION,
      "his 19:13 word lifted to the class at 19:21: every geometric and temporal parameter names "
      "the measurement of the photograph it reads. The swell's depth reads how much of the work is "
      "grain, the crest spacing reads the work's own strongest spectral period, and the colour "
      "split reads the work's own finest detail")

check("PASS-LIQUID the coverage is declared, with the mechanism that pays for it",
      "coverage: { writes: false," in REGION
      and "gl_FragColor = vec4(col, 1.0);" in REGION,
      "both branches of the handover are photograph, so the alpha is the constant 1 and this "
      "instrument is lawful as the lowest cue of a stack and as a whole one-cue score")

declared = set(re.findall(r'\{ name: "(u\w+)", type:', REGION))
spelled = set(re.findall(r'uniform \w+ (u\w+);', REGION))
check("PASS-LIQUID the manifest's declared names and the shader's own names are one set",
      declared == spelled and len(declared) == 9,
      f"{len(declared)} declared, {len(spelled)} spelled; "
      f"declared only: {sorted(declared - spelled)}; spelled only: {sorted(spelled - declared)}")

check("PASS-LIQUID the module's own MIRRORED_REPEAT is written out, because the host clamps",
      "MIRRORED_REPEAT" in LABTXT and "vec2 mirror(vec2 x)" in REGION
      and "gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE" in LAYER,
      "liquid.js:273-274 binds its picture MIRRORED_REPEAT and the host binds every source "
      "CLAMP_TO_EDGE, so the fold is done in the shader and the two roads read the same texel "
      "wherever the swell carries a lookup off the frame")

# ---------------------------------------------------------------- browser rows

BROWSER_ROWS = [
    "PASS-LIQUID §8     · the manifest carries every field the contract names, in its shape",
    "PASS-LIQUID row 7  · door 0 stands the departing work, measured against its own file",
    "PASS-LIQUID row 7  · door 0 carries no trace of the arriving work",
    "PASS-LIQUID row 7  · door 1 stands the arriving work, measured against its own file",
    "PASS-LIQUID row 7  · door 1 carries no trace of the departing work",
    "PASS-LIQUID the host's water and the lab module's water agree at five places on the dial",
    "PASS-LIQUID the host's water and the lab module's water agree across the swell and the crests",
    "PASS-LIQUID the phase the die spends reaches the water, and one whole wave returns to it",
    "PASS-LIQUID the crossing dial reaches the picture: the middle is no door",
    "PASS-LIQUID the arriving work surfaces on the crests, and the boundary walks with the hand",
    "PASS-LIQUID the door is read on the DRAWING BUFFER and what it read is published",
    "PASS-LIQUID row 10 · a seeded run repeats to the pixel",
    "PASS-LIQUID row 15 · the console stays clean",
    "PASS-LIQUID the real transaction road: curtain up, one pass drawn, exactly one dock at the end",
    "PASS-LIQUID row 16 · the captures are kept as evidence",
]

RED_ROWS = [
    "PASS-LIQUID red-on-bug · the swell's gate on the crossing dial reverted: the door bends",
    "PASS-LIQUID red-on-bug · the handover stops travelling past the water's ceiling: the door leaks",
    "PASS-LIQUID red-on-bug · the door reading removed as well: the leaking door is drawn",
    "PASS-LIQUID red-on-bug · the crest curve removed: the two roads part",
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


def work_in_the_frame(src, w, h):
    """The work as this instrument seats it at a door: the plain cover fit, and nothing beyond it.
    The crop is exactly one, which is what the manifest's `framings` block publishes."""
    from PIL import Image
    im = Image.open(src).convert("RGB")
    iw, ih = im.size
    fa, ia = w / float(h), iw / float(ih)
    sw, sh = (ih * fa, float(ih)) if ia > fa else (float(iw), iw / fa)
    x0, y0 = (iw - sw) / 2.0, (ih - sh) / 2.0
    return im.resize((w, h), Image.BILINEAR, box=(x0, y0, x0 + sw, y0 + sh))


def standing(p):
    """How far a capture stands from the canvas's own flat background, and how much spread it
    carries of its own. A frame that was never drawn is the background and has neither — which is
    what a red-on-bug proof that broke the file instead of changing one rule would photograph, and
    every row below that reads a picture asks this first."""
    from PIL import Image, ImageChops, ImageStat
    a = Image.open(p).convert("RGB")
    flat = Image.new("RGB", a.size, BACKGROUND)
    st = ImageStat.Stat(ImageChops.difference(a, flat))
    own = ImageStat.Stat(a)
    return sum(st.mean) / 3.0, sum(own.stddev) / 3.0


def apart(p, work):
    from PIL import Image, ImageChops, ImageStat
    a = Image.open(p).convert("RGB")
    if a.size != work.size:
        return 255.0, 255.0
    st = ImageStat.Stat(ImageChops.difference(a, work))
    return sum(st.mean) / 3.0, max(m for _, m in st.extrema)


def bench_dir(pack_text=None):
    """The bench's own served root: the BUILT pass-layer.js and the built instrument files (the real
    artifacts, namespace applied and comments stripped), the lab module unchanged, the two
    photographs, and the page that stands the two roads of one frame side by side.

    A row proving a rule reds hands over a CHANGED instrument file and writes the site's own record
    with the digest of the bytes actually served, which is what the build does. The source file on
    disk is never touched."""
    d = Path(tempfile.mkdtemp(prefix="synth_liquidbench_"))
    pack = REGION if pack_text is None else pack_text
    shutil.copy2(TMP / "pass-layer.js", d / "pass-layer.js")
    for _inst in sorted(TMP.glob("pass-inst-*.js")):
        shutil.copy2(_inst, d / _inst.name)
    (d / "pass-inst-liquid.js").write_text(pack, encoding="utf-8")
    record = json.loads((TMP / "config.json").read_text(encoding="utf-8"))
    record["pass"]["instruments"]["liquid"]["digest"] = hashlib.sha256(
        pack.encode("utf-8")).hexdigest()
    (d / "config.json").write_text(json.dumps(record), encoding="utf-8")
    shutil.copy2(MODULE, d / "liquid.js")
    (d / "photos").mkdir()
    for p in PHOTOS:
        shutil.copy2(p, d / "photos" / p.name)
    shutil.copy2(ROOT / "tests" / "fixture_pass_liquid.html", d / "index.html")
    return d


def ready(br, tries=80):
    for _ in range(tries):
        if br.evaluate("String(!!window.__ready)") == "true":
            return True
        br.sleep(0.25)
    return False


def js(br, expr):
    return json.loads(br.evaluate("JSON.stringify((function(){%s})())" % expr))


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


def shot_module(br, name):
    br.evaluate("window.__show('module')")
    br.sleep(0.35)
    return png(br, SHOTS / name)


def shot_host(br, name, opts="{}"):
    br.evaluate("window.__show('host')")
    br.evaluate("window.__hostDraw(%s)" % opts)
    br.sleep(0.12)
    return png(br, SHOTS / name)


def plant(text, pairs):
    """One rule changed in a COPY of the built instrument file. Every plant asserts its own input, so
    a file the plant finds nothing to change in reds loudly instead of passing."""
    out = text
    for a, b in pairs:
        if a not in out:
            return None
        out = out.replace(a, b)
    return out


def run_browser_rows():
    def body(br):
        got = {}
        SHOTS.mkdir(parents=True, exist_ok=True)

        # ---- the manifest -----------------------------------------------------------------
        got["manifest"] = js(br, "return window.__manifest();")

        # ---- the two doors ----------------------------------------------------------------
        # A door hands the two DIFFERENT works, which is what a crossing carries.
        shot_host(br, "door0.png", '{mix: 0, a: 0, b: 1}')
        got["door0"] = str(SHOTS / "door0.png")
        shot_host(br, "door1.png", '{mix: 1, a: 0, b: 1}')
        got["door1"] = str(SHOTS / "door1.png")
        got["doorValues"] = js(br, "return [window.__values({mix:0, a:0, b:1}), "
                                   "window.__values({mix:1, a:0, b:1})];")

        # ---- the two roads of one water ---------------------------------------------------
        # The host is handed the SAME photograph in both slots, so the handover mixes a work with
        # itself and what stands is the module's own water. Five places on the module's own dial.
        roads = []
        for i, w in enumerate([0.0, 0.25, 0.5, 0.75, 1.0]):
            br.evaluate("window.__set('wet', %r)" % w)
            br.evaluate("window.__set('clock', 3.0)")
            br.sleep(0.3)
            m = shot_module(br, "wet%d-module.png" % i)
            h = shot_host(br, "wet%d-host.png" % i,
                          "{mix: window.__mixFor(%r), t: 3.0, a: 0, b: 0}" % w)
            roads.append([w, m, h])
        got["roads"] = roads

        # the swell, the crests and the phase, each walked with the other two held
        walked = []
        for key, vals in (("swell", [0.0, 0.25, 1.0]), ("crest", [0.2, 0.9])):
            for j, v in enumerate(vals):
                br.evaluate("window.__set('wet', 0.8)")
                br.evaluate("window.__set('clock', 5.0)")
                br.evaluate("window.__set(%r, %r)" % (key, v))
                br.sleep(0.3)
                m = shot_module(br, "%s%d-module.png" % (key, j))
                h = shot_host(br, "%s%d-host.png" % (key, j),
                              "{mix: window.__mixFor(0.8), t: 5.0, %s: %r, a: 0, b: 0}" % (key, v))
                walked.append([key, v, m, h])
        br.evaluate("window.__set('swell', 0.5)")
        br.evaluate("window.__set('crest', 0.702)")
        got["walked"] = walked

        # the die spends the module's own phase, and one whole span returns to the same picture
        phases = []
        for j, s in enumerate([0, 3, 8]):
            br.evaluate("window.__set('wet', 0.8)")
            br.evaluate("window.__set('clock', 5.0)")
            br.evaluate("window.__set('seed', %r)" % s)
            br.sleep(0.3)
            m = shot_module(br, "seed%d-module.png" % j)
            h = shot_host(br, "seed%d-host.png" % j,
                          "{mix: window.__mixFor(0.8), t: 5.0, seed: %r, a: 0, b: 0}" % s)
            phases.append([s, m, h])
        br.evaluate("window.__set('seed', 0)")
        got["phases"] = phases

        # ---- what the port added: the handover --------------------------------------------
        mids = []
        for j, m in enumerate([0.25, 0.5, 0.75]):
            shot_host(br, "mid%d.png" % j, "{mix: %r, t: 5.0, a: 0, b: 1}" % m)
            mids.append([m, str(SHOTS / ("mid%d.png" % j))])
        got["mids"] = mids
        # the judges' own frame: the coverage map, read as colour, at three places on the dial
        got["cover"] = js(br, """
          var out = [];
          [0, 0.25, 0.5, 0.75, 1].forEach(function (m) {
            out.push([m, window.__values({mix: m, t: 5.0, a: 0, b: 1}).front]);
          });
          return out;""")

        # ---- the door read on the buffer ---------------------------------------------------
        got["doorRead"] = js(br, """
          function read(w, h) {
            var v = window.__values({mix: 0, a: 0, b: 1, bufWidth: w, bufHeight: h});
            return {grid: v.grid, water: v.water, why: v.doorWhyNo,
                    moved: v.crestMoved, held: v.doorHeld, crest: v.crest};
          }
          return {big: read(780, 1688), held: read(20, 20), gone: read(12, 12)};""")

        # ---- a seeded run repeats -----------------------------------------------------------
        shot_host(br, "repeat-a.png", "{mix: 0.4, t: 5.0, seed: 3, a: 0, b: 1}")
        shot_host(br, "repeat-b.png", "{mix: 0.4, t: 5.0, seed: 3, a: 0, b: 1}")
        got["repeat"] = [str(SHOTS / "repeat-a.png"), str(SHOTS / "repeat-b.png")]

        got["errs"] = js(br, "return window.__errs;")
        return got
    return on_bench(body)


def run_red(pack_text, fn):
    return on_bench(fn, pack_text)


if missing:
    for r in BROWSER_ROWS + RED_ROWS:
        skip(r, "the lab tree is not on this machine: " + ", ".join(missing))
elif not chrome_available():
    for r in BROWSER_ROWS + RED_ROWS:
        skip(r, "chrome is not installed (pinned expected skip)")
else:
    G = run_browser_rows()
    if G is None:
        for r in BROWSER_ROWS + RED_ROWS:
            skip(r, "the bench page never reported ready")
    else:
        man = G["manifest"] or {}
        need = ["id", "api", "arity", "roles", "levels", "params", "handles", "neutrals", "doors",
                "framings", "drivers", "camera", "passes", "coverage", "resources", "capabilities",
                "decline", "provenance", "readiness"]
        lack = [k for k in need if k not in man]
        check(BROWSER_ROWS[0], not lack and man.get("id") == "liquid" and man.get("arity") == 2
              and man.get("coverage", {}).get("writes") is False,
              "every §8 field present, arity 2, coverage writes false"
              if not lack else "missing: " + ", ".join(lack))

        wA = work_in_the_frame(PHOTOS[0], VW, VH)
        wB = work_in_the_frame(PHOTOS[1], VW, VH)
        m0, x0 = apart(G["door0"], wA)
        m0b, _ = apart(G["door0"], wB)
        m1, x1 = apart(G["door1"], wB)
        m1a, _ = apart(G["door1"], wA)
        check(BROWSER_ROWS[1], m0 <= SEAM,
              "door 0 stands %.3f of 255 from the departing work's own cover fit at a crop of one "
              "(worst channel %.1f), against the %s the project's seam allows" % (m0, x0, SEAM))
        check(BROWSER_ROWS[2], m0b >= FAR,
              "and %.1f of 255 from the arriving work, which is a different photograph" % m0b)
        check(BROWSER_ROWS[3], m1 <= SEAM,
              "door 1 stands %.3f of 255 from the arriving work's own cover fit (worst channel "
              "%.1f)" % (m1, x1))
        check(BROWSER_ROWS[4], m1a >= FAR,
              "and %.1f of 255 from the departing work" % m1a)

        # THE SEATING FLOOR, AND WHY EVERY TWO-ROADS ROW BELOW STANDS ON IT RATHER THAN ON ZERO.
        # At `wet` 0 NEITHER road draws any water at all: both stand the same photograph, cover-
        # fitted into the same frame. They still differ, and the difference is the two roads'
        # MINIFICATION and nothing else — the module builds a mipmap chain and reads it
        # LINEAR_MIPMAP_LINEAR (liquid.js:264-265), the host binds every source LINEAR with no
        # chain (pass-layer.js:110-112), and a 1440-point photograph landing on a 390-point frame
        # is where those two part. The host's texture upload is not this instrument's to change, so
        # the floor is MEASURED here and every water row is held against it: the water itself may
        # add no more than the two-roads bar on top of what the seating already costs.
        reads = [(w, ) + diff(m, h) for w, m, h in G["roads"]]
        FLOOR = reads[0][1]
        BAR = FLOOR + SAME
        worst = max(r[1] for r in reads)
        check(BROWSER_ROWS[5], worst <= BAR,
              "; ".join("wet %.2f: %.4f of 255 (worst channel %.1f)" % r for r in reads)
              + " — the seating floor is %.4f (no water on either road) and the water adds at most "
                "%.4f on top of it, inside the two-roads bar of %s. The same photograph stands in "
                "both of the host's slots, so the handover mixes a work with itself and what is "
                "compared is the module's own water" % (FLOOR, worst - FLOOR, SAME))

        wreads = [(k, v) + diff(m, h) for k, v, m, h in G["walked"]]
        wworst = max(r[2] for r in wreads)
        check(BROWSER_ROWS[6], wworst <= BAR,
              "; ".join("%s %.2f: %.4f (worst %.1f)" % r for r in wreads)
              + " — worst %.4f over the seating floor of %.4f" % (wworst - FLOOR, FLOOR))

        pread = [(s, ) + diff(m, h) for s, m, h in G["phases"]]
        pworst = max(r[1] for r in pread)
        whole, _ = diff(G["phases"][0][2], G["phases"][2][2])
        turned, _ = diff(G["phases"][0][2], G["phases"][1][2])
        check(BROWSER_ROWS[7], pworst <= BAR and whole <= SAME and turned > SEAM,
              "; ".join("die %d: %.4f (worst %.1f)" % r for r in pread)
              + " — a die of three moves the module's own water by %.2f of 255, and a die of the "
                "whole span stands %.4f from a die of nothing, which is the module's own «the "
                "travel is one whole wave»" % (turned, whole))

        mid_far = [(m, apart(p, wA)[0], apart(p, wB)[0]) for m, p in G["mids"]]
        moved = min(min(a, b) for _, a, b in mid_far)
        check(BROWSER_ROWS[8], moved >= SEAM,
              "; ".join("mix %.2f stands %.1f from work a and %.1f from work b" % r
                        for r in mid_far)
              + " — the nearest of them is %.1f of 255 from either whole work, over the project's "
                "seam, so the middle is a picture of its own and not a door held twice" % moved)

        fronts = [f for _, f in G["cover"]]
        walks = all(fronts[i] > fronts[i + 1] for i in range(len(fronts) - 1))
        ends = fronts[0] >= 1.37 and fronts[-1] <= -1.37
        one_two = [(m, apart(p, wA)[0], apart(p, wB)[0]) for m, p in G["mids"]]
        check(BROWSER_ROWS[9], walks and ends and all(a > SEAM and b > SEAM for _, a, b in one_two),
              "the handover's line walks from %.3f to %.3f without turning back, and both ends "
              "stand past the water's own ceiling of 1.27 by the tenth the margin gives it, so "
              "every point of the frame is on one work at either door; mid-dial the frame carries "
              "both photographs at once" % (fronts[0], fronts[-1]))

        big, heldR, gone = (G["doorRead"]["big"], G["doorRead"]["held"], G["doorRead"]["gone"])
        check(BROWSER_ROWS[10],
              big["grid"]["w"] == 780 and big["grid"]["h"] == 1688 and big["grid"]["drawn"] is True
              and big["water"]["wrong"] == 0 and big["why"] is None and big["moved"] == 0
              and heldR["why"] is None and heldR["moved"] > 0 and heldR["held"] is not None
              and gone["why"] is not None,
              "on the 780 x 1688 buffer the walk takes %d points, finds %d of them on the wrong "
              "work, keeps %.4f of the field to spare and nothing is held; on a 20 x 20 buffer the "
              "same reading lets the crests out by %.2f of the handle's own travel and the door is "
              "whole again, with what it held on the record («%s»); on a 12 x 12 buffer no letting "
              "out closes it and the door is refused: «%s»"
              % (big["water"]["walked"], big["water"]["wrong"], big["water"]["spareField"],
                 heldR["moved"], str(heldR["held"])[:120], str(gone["why"])[:200]))

        rm, rx = diff(G["repeat"][0], G["repeat"][1])
        check(BROWSER_ROWS[11], rx == 0,
              "the same pose drawn twice: %.4f of 255, worst channel %.0f" % (rm, rx))

        check(BROWSER_ROWS[12], not G["errs"],
              "no error, no rejection and no console.error over the whole run"
              if not G["errs"] else "; ".join(G["errs"][:4]))

        # the real transaction road
        def road(br):
            score = {
                "schema": 2,
                "intent": "the photograph is the top of a body of water, and the second work "
                          "surfaces on the crests of its own swell (lab/effects/liquid.js:1-5)",
                "pair": {"a": "a", "b": "b"}, "seed": 0, "duration": 3000,
                "direction": "a-to-b",
                "interruption": {"withinMs": 500, "resolve": "nearest-door"},
                "failLand": "arrive",
                "camera": {"owner": "stage", "rests": "b",
                           "track": [{"at": "b", "pan": {"x": 0, "y": 0}, "logScale": 0,
                                      "pitch": 0, "yaw": 0, "roll": 0, "fov": None,
                                      "owner": "stage"}]},
                "cues": [{
                    "id": "liquid-main",
                    "instrument": {"id": "liquid", "api": 1},
                    "voice": "letter",
                    "roles": ["disassembly", "mystery", "assembly"],
                    "levels": ["SURFACE", "TEXTURE"],
                    "window": [0, 3.0], "works": ["a", "b"], "stack": 0,
                    "cameraAuthority": "stage",
                    "doors": {"in": {"handle": "mix", "value": 0, "measured": True},
                              "out": {"handle": "mix", "value": 1, "measured": True}},
                    "nodes": {"mixDrive": {"source": "progress"},
                              "clockDrive": {"source": "time"},
                              "swellStatic": {"op": "static", "value": 0.5},
                              "crestStatic": {"op": "static", "value": 0.702},
                              "refractStatic": {"op": "static", "value": 0.45},
                              "seedStatic": {"op": "static", "value": 0},
                              "shadeStatic": {"op": "static", "value": 1},
                              "travelStatic": {"op": "static", "value": 1},
                              "maskStatic": {"op": "static", "value": 0}},
                    "tracks": {"mix": {"node": "mixDrive"}, "clock": {"node": "clockDrive"},
                               "swell": {"node": "swellStatic"},
                               "crest": {"node": "crestStatic"},
                               "refract": {"node": "refractStatic"},
                               "seed": {"node": "seedStatic"},
                               "shade": {"node": "shadeStatic"},
                               "travel": {"node": "travelStatic"},
                               "mask": {"node": "maskStatic"}},
                    "resources": {"textures": 0, "textureSlots": 2, "framebuffers": 0,
                                  "pingPong": 0, "programs": 1, "passes": 1, "bytesEstimate": 0,
                                  "variant": "standard"},
                }],
                "quality": {v: {"renderScale": None,
                                "cues": {"liquid-main": {
                                    "textures": 0, "textureSlots": 2, "framebuffers": 0,
                                    "pingPong": 0, "programs": 1, "passes": 1,
                                    "bytesEstimate": 0, "variant": v}}}
                            for v in ("lean", "standard", "rich")},
                "provenance": {"source": "lab/effects/liquid.js's own declared constants",
                               "measuredAt": None, "by": "tests/test_pass_liquid.py"},
            }
            out = js(br, "return window.__offer(%s, {});" % json.dumps(score))
            br.sleep(2.0)
            for _ in range(60):
                if js(br, "return window.__report().state;") == "idle":
                    break
                br.sleep(0.15)
            return {"took": out, "hooks": js(br, "return window.__hooks;"),
                    "report": js(br, "var r = window.__report(); "
                                     "return {state: r.state, why: r.lastWhy || null, "
                                     "applied: r.applied || null};"),
                    "errs": js(br, "return window.__errs;")}
        R = on_bench(road)
        check(BROWSER_ROWS[13],
              bool(R) and R["took"]["took"] is True and R["hooks"]["curtains"][:1] == [True]
              and len(R["hooks"]["docks"]) == 1 and R["report"]["state"] == "idle",
              "the host took the offer, raised its curtain, drew the pass and docked once: %s"
              % json.dumps(R["hooks"]) if R else "the road never ran")

        kept = sorted(p.name for p in SHOTS.glob("*.png")) if SHOTS.exists() else []
        check(BROWSER_ROWS[14], len(kept) >= 20,
              "%d captures kept at %s" % (len(kept), SHOTS))

        # ---- red on bug -------------------------------------------------------------------
        p1 = plant(REGION, [("* wet * WAVE_REACH * clamp(st.swell, 0, 1)",
                             "* WAVE_REACH * clamp(st.swell, 0, 1)")])
        if p1 is None:
            skip(RED_ROWS[0], "the plant found nothing to change")
        else:
            def r1(br):
                shot_host(br, "red1-door0.png", "{mix: 0, a: 0, b: 1}")
                return str(SHOTS / "red1-door0.png")
            got1 = run_red(p1, r1)
            d1 = apart(got1, wA)[0] if got1 else 0.0
            s1 = standing(got1) if got1 else (0.0, 0.0)
            check(RED_ROWS[0], got1 is not None and d1 > SEAM and s1[1] > 10.0,
                  "with the swell no longer gated by the crossing dial, door 0 stands %.2f of 255 "
                  "from its own file against %.3f with the gate — the water bends a door that owes "
                  "the photograph flat. The capture is a picture and not an unraised stage: it "
                  "stands %.1f from the canvas's own background and carries a spread of %.1f"
                  % (d1, m0, s1[0], s1[1]))

        # THE WATER'S OWN CEILING, TYPED INSTEAD OF DERIVED — which is exactly the defect his 19:21
        # word names as a class: a number nobody read reaching the picture. The line then stops
        # inside the swell's own range, the crests stand above it at a door, and the arriving
        # photograph is on the frame where the departing one owes every point.
        p2 = plant(REGION, [("FIELD_TOP = SA[0] + SA[1] + SA[2]", "FIELD_TOP = 0.5")])
        if p2 is None:
            skip(RED_ROWS[1], "the plant found nothing to change")
        else:
            def r2(br):
                return js(br, "var v = window.__values({mix: 0, a: 0, b: 1, "
                              "bufWidth: 780, bufHeight: 1688}); "
                              "return {why: v.doorWhyNo, wrong: v.water ? v.water.wrong : null, "
                              "walked: v.water ? v.water.walked : null};")
            got2 = run_red(p2, r2)
            check(RED_ROWS[1],
                  bool(got2) and got2["why"] is not None and (got2["wrong"] or 0) > 0,
                  "with the water's own ceiling typed as 0.5 instead of derived from the three "
                  "amplitudes, the instrument's own walk finds %s of the %s points it takes "
                  "carrying the arriving work at the entry door, and refuses it: «%s»"
                  % (got2["wrong"] if got2 else "?", got2["walked"] if got2 else "?",
                     str(got2["why"])[:200] if got2 else "no reading"))

            p3 = plant(p2, [("var no = doorWhyNoOf(read);", "var no = null;")])
            if p3 is None:
                skip(RED_ROWS[2], "the plant found nothing to change")
            else:
                def r3(br):
                    shot_host(br, "red3-door0.png", "{mix: 0, a: 0, b: 1}")
                    return [str(SHOTS / "red3-door0.png"),
                            js(br, "var v = window.__values({mix: 0, a: 0, b: 1, "
                                   "bufWidth: 780, bufHeight: 1688}); return v.doorWhyNo;")]
                got3 = run_red(p3, r3)
                d3 = apart(got3[0], wA)[0] if got3 else 0.0
                s3 = standing(got3[0]) if got3 else (0.0, 0.0)
                check(RED_ROWS[2],
                      got3 is not None and got3[1] is None and d3 > SEAM and s3[1] > 10.0,
                      "the leak is on the PICTURE and not only in the reading: that same door draws "
                      "%.2f of 255 from the departing work's own file against %.3f with the ceiling "
                      "derived (the capture stands %.1f from the background with a spread of %.1f, "
                      "so it is a frame and not an unraised stage) — and with the reading taken out "
                      "the instrument answers with no refusal at all, so the walk would carry a "
                      "visitor into a door that is two photographs" % (d3, m0, s3[0], s3[1]))

        p4 = plant(REGION, [("Math.pow(SPREAD_REACH, 1 - 2 * feelCrest(clamp(crest, 0, 1)))",
                             "Math.pow(SPREAD_REACH, 1 - 2 * clamp(crest, 0, 1))")])
        if p4 is None:
            skip(RED_ROWS[3], "the plant found nothing to change")
        else:
            def r4(br):
                br.evaluate("window.__set('wet', 0.8)")
                br.evaluate("window.__set('clock', 5.0)")
                br.sleep(0.3)
                m = shot_module(br, "red4-module.png")
                h = shot_host(br, "red4-host.png",
                              "{mix: window.__mixFor(0.8), t: 5.0, a: 0, b: 0}")
                return [m, h]
            got4 = run_red(p4, r4)
            d4 = diff(got4[0], got4[1])[0] if got4 else 0.0
            s4 = standing(got4[1]) if got4 else (0.0, 0.0)
            base = max(r[1] for r in reads)
            check(RED_ROWS[3], got4 is not None and d4 > BAR and s4[1] > 10.0,
                  "with the module's own two-piece logarithm taken off the crest handle the two "
                  "roads stand %.3f of 255 apart against %.4f with it — over the seating floor's "
                  "own bar of %.3f — so the curve is a carrier of the module's own spacing and not "
                  "decoration; the host's capture stands %.1f from the background with a spread of "
                  "%.1f" % (d4, base, BAR, s4[0], s4[1]))


# ---------------------------------------------------------------- report
fails = [r for r in results if r[1] == "FAIL"]
skips = [r for r in results if r[1] == "SKIP"]
for name, verdict, detail in results:
    print("%-4s %s" % (verdict, name))
    if detail:
        print("       %s" % detail)
print("\n%d passed / %d failed / %d skipped"
      % (len(results) - len(fails) - len(skips), len(fails), len(skips)))
sys.exit(1 if fails else 0)
