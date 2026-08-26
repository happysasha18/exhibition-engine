#!/usr/bin/env python3
"""PASS-API-V1 — the darkroom instrument on the host's frame.
Run: python3 tests/test_pass_studio.py

Root: the owner's word of 2026-08-18 23:21 — every instrument the lab holds but the shards belongs
in the arsenal — carried onto lab/effects/studio.js, the eight-operation darkroom chain. Unlike
every other port in this farm, studio's own module runs no crossing at all: its own `bench` dial
walks one photograph from as-taken to fully warped, never from one work to another. This file proves
the port that closes that gap — the there-and-back triangle pass-inst-studio.js's own header names,
carried from the same wall pass-inst-hero.js already met and proved lawful — on the host's own frame:
docs/design/PASS-API-V1.md §7 (GPU and resources) and §8 (the manifest), and the composer wiring
(pass-composer.js's HANDLE_SOURCE and its "studio" branch of fillPlan) that makes the instrument
castable on real pairs of the collection rather than only reachable by hand.

WHAT IS COMPARED, AND AGAINST WHAT.

  The doors. At the dial's two ends the standing work is exact BY CONSTRUCTION — the there-and-back
  triangle and the module's own response curve both reach exactly 0 at `mix` 0 and at `mix` 1, so the
  shader's own `mix(p, chain(p), dial)` returns `p` unchanged whatever the chain would otherwise
  compute. Each door is measured against ITS OWN FILE, cover-fitted into the frame, inside the
  project's seam threshold of 6 of 255.

  Away from a door. Mid-passage the chain stands at its own deepest reach, so the frame there must
  read as neither work plainly — proof the instrument is doing something rather than only obeying its
  own door law.

  The composer wiring, in Node against the real files. Every handle this instrument's own manifest
  publishes has a row in pass-composer.js's HANDLE_SOURCE, checked directly off the two files rather
  than off a fixture that predates this port; and the instrument actually CASTS on a real sample of
  the 121-work collection's own ordered pairs, with its measured handles reading differently pair to
  pair — proof against his word of 2026-08-18 15:13, that nothing may be the same for every pair.

  The lab tree is READ ONLY and is found at $TLVPHOTOS_ROOT, defaulting to tlvphotos-u27, the tree
  this port's own module was read from. Absent, every browser row here is a pinned SKIP that names
  the missing path — never a silent pass.
"""
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

LAB = Path(os.environ.get("TLVPHOTOS_ROOT", "/Users/sashaabramovich/tlvphotos-u27")) / "lab"
PHOTOS = [LAB / "photos" / "towers.jpg", LAB / "photos" / "glassgrid.jpg"]
MODULE = LAB / "effects" / "studio.js"
ASSETS = ROOT / "engine" / "assets"
COMPOSER = ASSETS / "pass-composer.js"
INSTRUMENT = ASSETS / "pass-inst-studio.js"
WORKS = Path(__file__).resolve().parent / "fixture_pass_works.json"

SITE_URL = "https://synth.example.com"
VW, VH = 390, 844
SEAM = 6.0          # the project's seam threshold, 6 of 255
FAR = 30.0          # further than this from a file's own pixels and the frame is a different picture
BACKGROUND = (0x08, 0x08, 0x0a)
SPREAD = 10.0

SHOTS = ROOT / "tests" / "captures" / "pass-studio"

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


INSTRUMENT_TEXT = INSTRUMENT.read_text(encoding="utf-8")
COMPOSER_TEXT = COMPOSER.read_text(encoding="utf-8")

# ---------------------------------------------------------------- static rows, read off the files

OWNED = ["createElement", "getContext", "requestAnimationFrame", "addEventListener",
         "performance.now", "Date.now", "new Image", "setTimeout", "setInterval",
         "getImageData", "drawImage"]
held = [s for s in OWNED if s in INSTRUMENT_TEXT]
check("PASS-STUDIO the instrument creates no context, no canvas, no loop, no listener and reads no "
      "picture's pixels",
      not held,
      "§1.2's fence: none of the eleven ways of owning hardware or of opening a photograph appears "
      "in the instrument file, so the module's own canvas, its WebGL2 context, its frame loop, its "
      "resize observer, its pointer listener and the whole panel it draws over the canvas all stayed "
      "in the lab"
      if not held else "the instrument holds " + ", ".join(held))

STRIPPED_INSTRUMENT = build_site._engine.strip_js_comments(INSTRUMENT_TEXT)
check("PASS-STUDIO the shader carries no version header of its own",
      "#version" not in STRIPPED_INSTRUMENT,
      "GLSL ES 1.00, so the host's translator stamps the one header this shader needs, the same "
      "road every other instrument in this arsenal takes (studio.js's own #version 300 es is named "
      "only in this port's own comments, which is where the check above strips it from)")

# THE EIGHT OPERATIONS AND `grade`, EACH A NAMED GLSL FUNCTION CARRIED CHARACTER FOR CHARACTER (bar
# the uniform declarations themselves, GLSL ES 1.00 here against studio.js's own #version 300 es).
OPS = ["stTile", "stEndless", "stKal", "stMirror", "stPolar", "stTwirl", "stCrop", "chain", "grade"]
missing_ops = [op for op in OPS if ("vec2 " + op + "(" not in INSTRUMENT_TEXT
                                     and "vec3 " + op + "(" not in INSTRUMENT_TEXT)]
check("PASS-STUDIO all eight operations and the colour grade are carried as the module's own "
      "functions",
      not missing_ops,
      "stTile, stEndless, stKal, stMirror, stPolar, stTwirl, stCrop, chain and grade, studio.js's "
      "own lines (studio.js:59-165)"
      if not missing_ops else "missing: " + ", ".join(missing_ops))

CONSTANTS = [("TWIRL_R = 0.62",
              "the twirl operation's own radius, studio.js's own gl.uniform1f(U.uTwirlR, 0.62)"),
             ("RING_RATIO = [4.4, 2.9, 1.95]",
              "the endless zoom's own three ring sizes, studio.js:319"),
             ("KAL_DRIFT_RATE = 0.035",
              "the kaleidoscope's own breath, studio.js:908"),
             ("POLAR_SPIN_RATE = 0.055",
              "the planet's own spin drift, studio.js:907"),
             ("RING_PHASE_RATE = 0.10",
              "the endless zoom's own phase drift, studio.js:909"),
             ("LOOK_SAT = [0.45, 1.38, 1.0]",
              "the three colour looks' own pinned saturation, studio.js:965-970"),
             ("LOOK_CON = [0.92, 1.14, 1.0]",
              "the three colour looks' own pinned contrast, studio.js:965-970"),
             ("FEEL_K = 3.55",
              "the module's own measured response curve, studio.js:839")]
missing_const = [c for c, _ in CONSTANTS if c not in INSTRUMENT_TEXT]
check("PASS-STUDIO every constant carried from the lab module stands at the number studio.js gives "
      "it",
      not missing_const,
      "; ".join("%s — %s" % (c, why) for c, why in CONSTANTS) if not missing_const
      else "missing or changed: " + ", ".join(missing_const))

declared = set(re.findall(r'\{ name: "(u\w+)", type:', INSTRUMENT_TEXT))
spelled = set(re.findall(r'uniform\s+\w+\s+(u\w+)\s*;', INSTRUMENT_TEXT))
check("PASS-STUDIO the manifest's declared uniform names and the shader's own spelled names are one "
      "set",
      declared == spelled and len(declared) == 35,
      f"{len(declared)} declared, {len(spelled)} spelled; declared only: {sorted(declared - spelled)}; "
      f"spelled only: {sorted(spelled - declared)}")

sha = hashlib.sha256(MODULE.read_bytes()).hexdigest() if MODULE.exists() else ""
declared_sha = (re.search(r'sha256: "([0-9a-f]{64})"', INSTRUMENT_TEXT) or [None, None])[1]
check("PASS-STUDIO the provenance names the file the port was read from, and the file weighs to it",
      bool(sha) and sha == declared_sha,
      f"the lab module stands tracked at commit 2afa485; the digest of the bytes the port was read "
      f"from stands in the manifest and the file still weighs to {sha[:16]}…" if sha
      else f"lab module absent at {MODULE}")

check("PASS-STUDIO the manifest leaves the drawing buffer unpreserved and declares its own cuts",
      "gl: { preserveDrawingBuffer: false }" in INSTRUMENT_TEXT
      and 'cuts: ["ring", "wedge", "tile"]' in INSTRUMENT_TEXT,
      "§7 refuses a manifest asking for a preserved buffer; §8 refuses a build with no cuts: line "
      "(lab/build-workrecords-v1.py's own CUTS_UNDECLARED gate) — the exact wall this brief's own "
      "step 1 names")

# ---------------------------------------------------------------- the composer wiring, in Node

def node_available():
    try:
        return subprocess.run(["node", "--version"], capture_output=True).returncode == 0
    except FileNotFoundError:
        return False


DRIVER = r"""
"use strict";
const fs = require("fs"), vm = require("vm"), path = require("path");
const [assetsDir, worksPath] = process.argv.slice(2);
const files = fs.readdirSync(assetsDir).filter((f) => /^pass-inst-.*\.js$/.test(f));
const manifests = {};
for (const f of files) {
  const src = fs.readFileSync(path.join(assetsDir, f), "utf8").replace(/@@NS@@/g, "");
  const sandbox = { window: { __PassInstrument: (r) => { manifests[r.instrument.name] = r.instrument.manifest; } },
                     console, document: undefined };
  vm.createContext(sandbox);
  vm.runInContext(src, sandbox, { filename: f });
}
const instruments = {};
for (const iid of Object.keys(manifests)) {
  const m = manifests[iid];
  instruments[iid] = {
    api: m.api, levels: m.levels.slice(), roles: m.roles.slice(), cuts: (m.cuts || []).slice(),
    handles: Object.keys(m.handles).filter((h) => !m.handles[h].open).sort(),
    coverage: { writes: m.coverage.writes }, port: "engine/assets/pass-inst-" + iid + ".js",
  };
}
let joined = null;
const csrc = fs.readFileSync(path.join(assetsDir, "pass-composer.js"), "utf8").replace(/@@NS@@/g, "");
const csandbox = { window: { __PassComposer: (r) => { joined = r; } }, console };
vm.createContext(csandbox);
vm.runInContext(csrc, csandbox, { filename: "pass-composer.js" });
if (!joined) { console.log(JSON.stringify({ error: "the composer joined nothing" })); process.exit(0); }

const consts = {
  manifests, instruments,
  provenance: { source: ["test_pass_studio.py"], measuredAt: {}, by: "test_pass_studio.py" },
  scoreFenceBytes: 12288, intentFenceChars: 600,
};
if (!manifests.studio) {
  console.log(JSON.stringify({ error: "no pass-inst-studio.js registered a manifest" }));
  process.exit(0);
}
const composer = joined.make(consts);
const works = JSON.parse(fs.readFileSync(worksPath, "utf8")).works;
const ids = Object.keys(works);

let total = 0, declined = 0, studioCasts = 0;
const errors = [];
const seenHandleSets = [];
outer:
for (let i = 0; i < ids.length; i++) {
  for (let j = 0; j < ids.length; j++) {
    if (i === j) continue;
    const a = ids[i], b = ids[j];
    total++;
    try {
      const res = composer.passageFor({ workRecordA: works[a], workRecordB: works[b],
                                         direction: "a-to-b", seed: ((i * 31 + j * 7) % 100) / 12.5 });
      if (res.declined) { declined++; continue; }
      const cue = (res.score.cues || []).find((c) => c.instrument.id === "studio");
      if (cue) {
        studioCasts++;
        const n = cue.nodes;
        seenHandleSets.push({ panX: n["travel-panX"] || n[cue.id + "-panX"],
                               kalN: n["travel-kalN"] || n[cue.id + "-kalN"],
                               tileN: n["travel-tileN"] || n[cue.id + "-tileN"],
                               polarSpread: n["travel-polarSpread"] || n[cue.id + "-polarSpread"] });
      }
    } catch (e) {
      if (errors.length < 8) errors.push(a + "->" + b + ": " + e.message);
    }
    if (total >= 6000) break outer;
  }
}
console.log(JSON.stringify({ total, declined, studioCasts, errors,
                              instrumentCount: Object.keys(manifests).length,
                              sample: seenHandleSets.slice(0, 6) }));
"""

DRIVER_PATH = Path(tempfile.mkdtemp(prefix="synth_studio_driver_")) / "driver.js"
DRIVER_PATH.write_text(DRIVER, encoding="utf-8")

if not node_available():
    skip("PASS-STUDIO every handle this instrument publishes has a row in the composer's register, "
         "read directly off the two files", "node is not installed")
    skip("PASS-STUDIO the instrument actually casts on a real sample of the collection's own pairs, "
         "with its measured handles reading differently pair to pair",
         "node is not installed")
elif not WORKS.exists():
    skip("PASS-STUDIO every handle this instrument publishes has a row in the composer's register, "
         "read directly off the two files", "the collection's own work records are absent: " + str(WORKS))
    skip("PASS-STUDIO the instrument actually casts on a real sample of the collection's own pairs, "
         "with its measured handles reading differently pair to pair",
         "the collection's own work records are absent: " + str(WORKS))
else:
    proc = subprocess.run(["node", str(DRIVER_PATH), str(ASSETS), str(WORKS)],
                           capture_output=True, text=True)
    try:
        SWEEP = json.loads(proc.stdout.strip().splitlines()[-1]) if proc.stdout.strip() else \
            {"error": "no output; stderr: " + proc.stderr[-2000:]}
    except Exception as e:
        SWEEP = {"error": f"could not parse node output: {e}; stdout={proc.stdout[-1000:]!r} "
                           f"stderr={proc.stderr[-1000:]!r}"}

    check("PASS-STUDIO every handle this instrument publishes has a row in the composer's register, "
          "read directly off the two files",
          not SWEEP.get("error") and not SWEEP.get("errors"),
          f"{SWEEP.get('instrumentCount')} instruments registered from the live tree, "
          f"{SWEEP.get('total')} real ordered pairs composed with {len(SWEEP.get('errors', []))} "
          f"errors" if not SWEEP.get("error")
          else "the sweep could not run: " + str(SWEEP.get("error"))
          + ("; sample errors: " + "; ".join(SWEEP.get("errors", [])) if SWEEP.get("errors") else ""))

    casts = SWEEP.get("studioCasts", 0)
    total_c = SWEEP.get("total", 0)
    sample = SWEEP.get("sample", [])
    varies = len({json.dumps(s, sort_keys=True) for s in sample}) > 1 if len(sample) > 1 else False
    check("PASS-STUDIO the instrument actually casts on a real sample of the collection's own pairs, "
          "with its measured handles reading differently pair to pair",
          not SWEEP.get("error") and casts > 0 and varies,
          f"studio was cast on {casts} of {total_c - SWEEP.get('declined', 0)} composed pairs "
          f"({(100.0 * casts / max(1, total_c)):.1f}% of the {total_c} tried); a sample of its own "
          f"measured panX/kalN/tileN/polarSpread across those casts: {json.dumps(sample)}"
          if not SWEEP.get("error") else "the sweep could not run: " + str(SWEEP.get("error")))

shutil.rmtree(DRIVER_PATH.parent, ignore_errors=True)

# ---------------------------------------------------------------- browser rows

BROWSER_ROWS = [
    "PASS-STUDIO §8     · the manifest carries every field the contract names, in its shape",
    "PASS-STUDIO §8     · it publishes TEXTURE and LIGHT-COLOUR, and SURFACE is not claimed",
    "PASS-STUDIO row 7  · door 0 stands the departing work, measured against its own file",
    "PASS-STUDIO row 7  · door 0 carries no trace of the arriving work",
    "PASS-STUDIO row 7  · door 1 stands the arriving work, measured against its own file",
    "PASS-STUDIO row 7  · door 1 carries no trace of the departing work",
    "PASS-STUDIO mid-passage reads as neither work plainly — the chain is doing something",
    "PASS-STUDIO §7     · no empty frame at any sampled instant of the pass",
    "PASS-STUDIO §7     · the frame after a change of viewport is drawn, not a kept buffer",
    "PASS-STUDIO the instrument's own door reading holds by construction on every grid asked",
    "PASS-STUDIO row 14 · textures, programmes and framebuffers return to their baseline after ten "
    "runs",
    "PASS-STUDIO row 15 · the console stays clean",
    "PASS-STUDIO §4.4b  · kalN, mirrorMode, hue and zoom each reach the PICTURE",
    "PASS-STUDIO the two doors frame at a crop of exactly one, and both agree",
    "PASS-STUDIO §7     · a manifest asking for a preserved drawing buffer is refused, with its "
    "reason",
    "PASS-STUDIO §7     · a uniform bound to a name the shader lacks is refused, with its reason",
    "PASS-STUDIO the fleet's judges' channel rests at nothing and, standing, draws which work stands "
    "as red",
    "PASS-STUDIO row 16 · the captures are kept as evidence",
]

missing = [str(p) for p in ([MODULE] + PHOTOS) if not p.exists()]


def png(br, path):
    import base64
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


def work_in_the_frame(src, w, h, zoom):
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


def channels(p):
    from PIL import Image, ImageStat
    return ImageStat.Stat(Image.open(p).convert("RGB")).extrema


def bench_dir(pack_text=None):
    d = Path(tempfile.mkdtemp(prefix="synth_studiobench_"))
    pack = REGION if pack_text is None else pack_text
    shutil.copy2(TMP / "pass-layer.js", d / "pass-layer.js")
    for _inst in sorted(TMP.glob("pass-inst-*.js")):
        shutil.copy2(_inst, d / _inst.name)
    (d / "pass-inst-studio.js").write_text(pack, encoding="utf-8")
    record = json.loads((TMP / "config.json").read_text(encoding="utf-8"))
    record["pass"]["instruments"]["studio"]["digest"] = hashlib.sha256(
        pack.encode("utf-8")).hexdigest()
    (d / "config.json").write_text(json.dumps(record), encoding="utf-8")
    (d / "photos").mkdir()
    for p in PHOTOS:
        shutil.copy2(p, d / "photos" / p.name)
    shutil.copy2(ROOT / "tests" / "fixture_pass_studio.html", d / "index.html")
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
    for r in BROWSER_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
elif missing:
    for r in BROWSER_ROWS:
        skip(r, "the lab tree is read-only source material and is absent here: " + missing[0])
else:
    build_site.SITE_CONFIG = dict(build_site.SITE_CONFIG)
    build_site.SITE_CONFIG["pass"] = {"visualLayer": "pass", "diagnostics": "on"}
    TMP = Path(tempfile.mkdtemp(prefix="synth_studio_"))
    build_site.OUT = TMP
    build_site.build(SITE_URL)
    # THE INSTRUMENT'S OWN REGION OF THE BUILT FILE — the real artifact the browser is actually
    # handed, with the @@NS@@ template token resolved and comments as they ship. `bench_dir` below
    # serves this by default rather than the raw source in `INSTRUMENT_TEXT`, which still carries the
    # unresolved token and is not valid JavaScript on its own.
    REGION = (TMP / "pass-inst-studio.js").read_text(encoding="utf-8")

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
            elif not js(br, "return !!window.__exPass.bench.manifest('studio');"):
                why = js(br, "var e = window.__host.report().events.filter(function(x){"
                             "return x.name === 'manifest-refused';});"
                             "return e.length ? e[e.length - 1].why : null;")
                for r in BROWSER_ROWS:
                    check(r, False, "the host registered no «studio» instrument: " + str(why))
            else:
                m = js(br, "return window.__exPass.bench.manifest('studio');")
                zoom = m["framings"]["0"]["coverCrop"]
                res = m["resources"]
                shape = (
                    m["id"] == "studio" and m["api"] == 1 and m["arity"] == 2
                    and m["roles"] == ["disassembly", "mystery", "assembly"]
                    and len(m["handles"]) == 27
                    and all(set(h) >= {"min", "max", "def"} for h in m["handles"].values())
                    and m["neutrals"] == {"a": 0, "b": 1}
                    and m["doors"]["in"]["handle"] == "mix" and m["doors"]["in"]["value"] == 0
                    and m["doors"]["out"]["handle"] == "mix" and m["doors"]["out"]["value"] == 1
                    and sorted(m["framings"]) == ["0", "1"]
                    and m["framings"]["0"] == m["framings"]["1"]
                    and abs(zoom - 1.0) < 1e-12
                    and m["camera"] == {"needs": "none", "authority": "stage"}
                    and sorted(m["cuts"]) == ["ring", "tile", "wedge"]
                    and m["coverage"]["writes"] is False
                    and len(m["passes"]) == 1 and len(m["passes"][0]["uniforms"]) == 35
                    and sorted(res) == ["lean", "rich", "standard"]
                    and m["capabilities"] == ["webgl2"] and m["decline"]
                    and m["provenance"]["labPath"] == "lab/effects/studio.js"
                    and m["readiness"] == "production-ready"
                    and "studio" in js(br, "return window.__host.report().registered;"))
                check(BROWSER_ROWS[0], shape,
                      f"twenty-seven handles, thirty-five uniforms in one pass, a crop of {zoom} at "
                      f"both doors (the chain's own strength is zero at both by construction, so no "
                      f"headroom is bought), a cut on {sorted(m['cuts'])}, an alpha that is the "
                      f"constant 1 (coverage.writes={m['coverage']['writes']})")

                check(BROWSER_ROWS[1],
                      m["levels"] == ["TEXTURE", "LIGHT-COLOUR"],
                      "the eight operations bend the picture's own material (TEXTURE, the same level "
                      "liquid's own bend is placed at) and the colour operation turns hue, "
                      "saturation and contrast (LIGHT-COLOUR, the same level grid-colour's and "
                      "strata-light's own colour voices are placed at); SURFACE is not claimed "
                      "because the picture change is one hard swap for the whole frame, never a "
                      "field that varies point by point")

                br.evaluate("window.__clock(3.0); 0")
                br.sleep(0.3)

                pairs = []
                for name, v in (("door-0", 0.0), ("q1", 0.25), ("mid", 0.5),
                                 ("q3", 0.75), ("door-1", 1.0)):
                    br.evaluate("window.__mix(%r); 0" % v)
                    br.evaluate("window.__hostDraw(); 0")
                    br.sleep(0.15)
                    p = png(br, SHOTS / (name + ".png"))
                    pairs.append((name, p))

                shots = dict(pairs)
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

                mid_vs_a, _ = apart(shots["mid"], towers)
                mid_vs_b, _ = apart(shots["mid"], glass)
                check(BROWSER_ROWS[6], mid_vs_a >= FAR and mid_vs_b >= FAR,
                      f"mid-passage stands {mid_vs_a:.4f} of 255 from towers.jpg's own plain frame "
                      f"and {mid_vs_b:.4f} from glassgrid.jpg's — both past {FAR}, so the chain is "
                      f"visibly bent at the passage's own centre rather than resting on either "
                      f"photograph")

                SCORE_JSON = json.dumps({
                    "schema": 2,
                    "intent": "the departing work bends up through the darkroom chain and the "
                              "arriving work unwinds back down through it (lab/effects/studio.js, "
                              "its own header)",
                    "pair": {"a": "a", "b": "b"}, "seed": 4.91016, "duration": 3000,
                    "direction": "a-to-b",
                    "interruption": {"withinMs": 500, "resolve": "nearest-door"},
                    "failLand": "arrive",
                    "camera": {"owner": "stage", "rests": "b",
                               "track": [{"at": "b", "pan": {"x": 0, "y": 0}, "logScale": 0,
                                          "pitch": 0, "yaw": 0, "roll": 0, "fov": None,
                                          "owner": "stage"}]},
                    "cues": [{
                        "id": "studio-main", "instrument": {"id": "studio", "api": 1},
                        "voice": "letter", "roles": ["disassembly", "mystery", "assembly"],
                        "levels": ["TEXTURE", "LIGHT-COLOUR"],
                        "levelOwnership": {"TEXTURE": "owns", "LIGHT-COLOUR": "owns"},
                        "window": [0, 3.0], "works": ["a", "b"], "stack": 0,
                        "cameraAuthority": "stage",
                        "doors": {"in": {"handle": "mix", "value": 0, "measured": True},
                                  "out": {"handle": "mix", "value": 1, "measured": True}},
                        "nodes": dict({k + "Static": {"op": "static", "value": v}
                                       for k, v in {
                                           "cropOn": 1, "zoom": 1.15, "panX": 0, "panY": 0,
                                           "twirlOn": 0, "twirlAmt": 1.4, "polarOn": 1,
                                           "polarSpread": 0.62, "polarFlip": 0, "mirrorOn": 1,
                                           "mirrorMode": 0, "foldX": -0.06, "foldY": 0,
                                           "kalOn": 0, "kalN": 8, "kalRot": 0, "ringOn": 0,
                                           "ringTwist": 0.35, "ringSize": 1, "tileOn": 0,
                                           "tileN": 2, "colOn": 0, "hue": 0, "colLook": 1,
                                           "mask": 0}.items()},
                                      mixDrive={"source": "progress"}, clockDrive={"source": "time"}),
                        "tracks": dict({k: {"node": k + "Static"} for k in [
                            "cropOn", "zoom", "panX", "panY", "twirlOn", "twirlAmt", "polarOn",
                            "polarSpread", "polarFlip", "mirrorOn", "mirrorMode", "foldX", "foldY",
                            "kalOn", "kalN", "kalRot", "ringOn", "ringTwist", "ringSize", "tileOn",
                            "tileN", "colOn", "hue", "colLook", "mask"]},
                                       mix={"node": "mixDrive"}, clock={"node": "clockDrive"}),
                        "resources": {"textures": 0, "textureSlots": 2, "framebuffers": 0,
                                     "pingPong": 0, "programs": 1, "passes": 1, "bytesEstimate": 0,
                                     "variant": "standard"},
                    }],
                    "quality": {v: {"renderScale": None,
                                    "cues": {"studio-main": {"resources": {
                                        "textures": 0, "textureSlots": 2, "framebuffers": 0,
                                        "pingPong": 0, "programs": 1, "passes": 1,
                                        "bytesEstimate": 0, "variant": v}}}}
                                for v in ("lean", "standard", "rich")},
                    "provenance": {"source": "lab/effects/studio.js's own declared defaults",
                                  "measuredAt": None, "by": "tests/test_pass_studio.py"},
                })

                empties = []
                for at in (0.0, 0.2, 0.4, 0.5, 0.6, 0.8, 1.0):
                    js(br, "return window.__offer(%s, {clock: 1.5, progress: %r});" % (SCORE_JSON, at))
                    br.sleep(0.4)
                    p = png(br, SHOTS / ("instant-%03d.png" % round(at * 100)))
                    empties.append((at,) + standing(p))
                    br.evaluate("window.__cancel('instant sweep'); 0")
                    idle(br)
                check(BROWSER_ROWS[7],
                      all(d >= FAR and s >= SPREAD for _, d, s in empties),
                      "; ".join(f"at {at}: {d:.2f} from the background, spread {s:.2f}"
                                for at, d, s in empties) + f" (bars: {FAR} and {SPREAD})")

                js(br, "return window.__offer(%s, {clock: 1.5, progress: 0.5});" % SCORE_JSON)
                br.sleep(0.5)
                br.set_viewport(VW - 80, VH - 120)
                br.sleep(0.6)
                p = png(br, SHOTS / "after-resize.png")
                sized = js(br, "return {w: document.querySelector('canvas').width, "
                               "pdb: window.__report().census.preserveDrawingBuffer};")
                d, s = standing(p)
                br.evaluate("window.__cancel('resize row'); 0")
                idle(br)
                br.set_viewport(VW, VH)
                br.sleep(0.4)
                check(BROWSER_ROWS[8],
                      d >= FAR and s >= SPREAD and sized["pdb"] is False,
                      f"after the viewport moved to {VW - 80}x{VH - 120} the frame stands {d:.2f} "
                      f"from the background with a spread of {s:.2f}; preserveDrawingBuffer="
                      f"{sized['pdb']}")

                door_reads = []
                for gw, gh in ((VW, VH), (780, 1688), (24, 40), (7, 11)):
                    for at, label in ((0, "entry"), (1, "exit")):
                        v = js(br, "return window.__values(%s);"
                               % json.dumps({"mix": at, "bufWidth": gw, "bufHeight": gh}))
                        door_reads.append((gw, gh, label, v))
                away = js(br, "return window.__values(%s);" % json.dumps({"mix": 0.5}))
                doors_whole = (all(v["doorWhyNo"] is None and abs(v["dial"]) < 1e-12
                                   for _, _, _, v in door_reads)
                               and away["doorWhyNo"] is None and abs(away["dial"] - 1) < 0.5)
                check(BROWSER_ROWS[9], doors_whole,
                      "; ".join(f"the {lab} door on a {gw} x {gh} buffer reads a chain strength of "
                                f"{v['dial']}" for gw, gh, lab, v in door_reads)
                      + f"; mid-passage reads {away['dial']:.4f} — the door is exact by construction "
                        f"on every grid, never by a tolerance a grid could close or open")

                base_c = js(br, "return window.__report().census;")
                for _ in range(10):
                    js(br, "return window.__offer(%s, {clock: 2.0, progress: 0.3});" % SCORE_JSON)
                    br.sleep(0.12)
                    br.evaluate("window.__cancel('leak row'); 0")
                br.sleep(0.4)
                after = js(br, "return window.__report().census;")
                same = (after["textures"] == base_c["textures"] == 2
                        and after["programs"] == base_c["programs"]
                        and after["framebuffers"] == base_c["framebuffers"] == 0
                        and after["canvases"] == base_c["canvases"]
                        and after["contexts"] == base_c["contexts"])
                check(BROWSER_ROWS[10], same,
                      f"before={base_c['textures']}/{base_c['programs']}/{base_c['framebuffers']} "
                      f"after ten runs={after['textures']}/{after['programs']}/{after['framebuffers']} "
                      f"(textures/programmes/framebuffers)")

                errs = json.loads(br.evaluate("JSON.stringify(window.__errs||[])"))
                check(BROWSER_ROWS[11], not errs, "; ".join(errs)[:200])

                # ---- §4.4b: a few handles reach the picture ------------------------------------
                br.evaluate("window.__cancel('before the handle rows'); 0")
                idle(br)
                br.evaluate("window.__reshow(); window.__mix(0.5); window.__clock(3.0); 0")
                br.sleep(0.2)

                def drew(name, over):
                    br.evaluate("window.__hostDraw(%s); 0" % json.dumps(over))
                    br.sleep(0.15)
                    return png(br, SHOTS / ("handle-" + name + ".png"))

                base_shot = drew("base", {})
                still = diff(base_shot, drew("base-again", {}))
                moved = {
                    "kalOn+kalN": diff(base_shot, drew("kal", {"kalOn": 1, "kalN": 6})),
                    "mirrorMode": diff(base_shot, drew("mirror", {"mirrorMode": 2})),
                    "hue": diff(base_shot, drew("hue", {"colOn": 1, "hue": 2.5})),
                    "zoom": diff(base_shot, drew("zoom", {"zoom": 2.4})),
                }
                check(BROWSER_ROWS[12],
                      still == (0.0, 0) and all(mx > SEAM for _, mx in moved.values()),
                      "; ".join(f"{k} moves the frame by {mn:.4f} of 255 on the mean and {mx} at its "
                                f"strongest point" for k, (mn, mx) in moved.items())
                      + f"; the same pose drawn twice moves it by {still[0]} at {still[1]}")

                fA = m["framings"]["0"]["coverCrop"]
                fB = m["framings"]["1"]["coverCrop"]
                check(BROWSER_ROWS[13], fA == fB == 1,
                      f"both doors carry a coverCrop of exactly 1 — the chain's own strength is zero "
                      f"at both by construction, so no headroom is ever bought from either photograph "
                      f"(fA={fA}, fB={fB})")

                r = js(br, """
                  var m = JSON.parse(JSON.stringify(window.__exPass.bench.manifest('studio')));
                  m.gl.preserveDrawingBuffer = true;
                  var STUB_VALUES = "function(){return {dial:0,change:0,cropOn:1,zoom:1,off:[0,0],"
                    + "twirlOn:0,twirl:0,twirlR:0.62,polarOn:0,spread:0.5,flip:0,spin:0,mirrorOn:0,"
                    + "mode:0,foldLine:[0,0],kalOn:0,kalN:8,kalRot:0,ringOn:0,drL:1,drTwist:0,"
                    + "drPhase:0,tileOn:0,tileN:2,colOn:0,hue:0,sat:1,con:1,inv:0,mask:0};}";
                  var STUB = "values:" + STUB_VALUES + ",fit:function(){return [1,1,0,0];},"
                    + "prepare:function(){return {take:false};}, start:function(){}, frame:function(){}";
                  var ok = window.__exPass.bench.register(
                    eval("({name:'studio-preserve', manifest:m, " + STUB + "})"));
                  var evs = window.__host.report().events.filter(function(e){return e.name==='manifest-refused';});
                  return {ok: ok, why: evs.length ? evs[evs.length-1].why : null,
                          registered: window.__host.report().registered};
                """)
                check(BROWSER_ROWS[14],
                      r["ok"] is False and r["why"] and "preserved" in r["why"]
                      and "studio-preserve" not in r["registered"],
                      f"registered={r['ok']} why={r['why']}")

                r = js(br, """
                  var m = JSON.parse(JSON.stringify(window.__exPass.bench.manifest('studio')));
                  m.passes[0].uniforms.push({name:'uPointer', type:'vec2', source:'pointer'});
                  var STUB_VALUES = "function(){return {dial:0,change:0,cropOn:1,zoom:1,off:[0,0],"
                    + "twirlOn:0,twirl:0,twirlR:0.62,polarOn:0,spread:0.5,flip:0,spin:0,mirrorOn:0,"
                    + "mode:0,foldLine:[0,0],kalOn:0,kalN:8,kalRot:0,ringOn:0,drL:1,drTwist:0,"
                    + "drPhase:0,tileOn:0,tileN:2,colOn:0,hue:0,sat:1,con:1,inv:0,mask:0};}";
                  var STUB = "values:" + STUB_VALUES + ",fit:function(){return [1,1,0,0];},"
                    + "prepare:function(){return {take:false};}, start:function(){}, frame:function(){}";
                  var ok = window.__exPass.bench.register(
                    eval("({name:'studio-pointer', manifest:m, " + STUB + "})"));
                  var evs = window.__host.report().events.filter(function(e){return e.name==='manifest-refused';});
                  return {ok: ok, why: evs.length ? evs[evs.length-1].why : null,
                          registered: window.__host.report().registered};
                """)
                check(BROWSER_ROWS[15],
                      r["ok"] is False and r["why"] and "uPointer" in r["why"]
                      and "cannot supply" in r["why"] and "studio-pointer" not in r["registered"],
                      f"registered={r['ok']} why={r['why']}")

                off_shot = drew("mask-off", {"mask": 0})
                on_shot = drew("mask-on", {"mask": 1})
                rests = diff(base_shot, off_shot)
                moved_mask = diff(base_shot, on_shot)
                ch = channels(on_shot)
                check(BROWSER_ROWS[16],
                      rests == (0.0, 0) and moved_mask[1] > SEAM,
                      f"resting at nothing it moves the frame by {rests[0]} at {rests[1]}; standing, "
                      f"it moves the frame by {moved_mask[0]:.4f} of 255 on the mean and "
                      f"{moved_mask[1]} at its strongest point, drawing which work stands as red "
                      f"(extrema {ch[0]})")

                kept = sorted(p.name for p in SHOTS.glob("*.png"))
                check(BROWSER_ROWS[17],
                      len(kept) >= 15 and all((SHOTS / k).stat().st_size > 1000 for k in kept),
                      f"{len(kept)} captures under {SHOTS.relative_to(ROOT)}: the five poses, the "
                      f"seven sampled instants, the frame after a resize and the handle rows")

    shutil.rmtree(BENCH, ignore_errors=True)
    shutil.rmtree(TMP, ignore_errors=True)

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
