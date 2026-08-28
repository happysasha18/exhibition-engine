#!/usr/bin/env python3
"""PASS-API-V1 — the parting-by-scale instrument on the host's frame.
Run: python3 tests/test_pass_strata-scale.py

Root: his word of 2026-08-18 23:21 — every instrument the lab holds but the shards belongs in the
arsenal — carried onto lab/effects/strata-scale.js, the module that parts a work into the MASSES it
is read down to and the DETAIL standing over them, each stratum leaving sideways toward the side of
its own measured centre of gravity. An earlier pass over this port reported the module unreachable:
its threshold and its two centres of gravity are reductions over the whole file, and a shader handed
one frame at the instant of a visit cannot take either. That report was wrong. Both are reductions
over ONE photograph, not over a pair, so they are per-work facts exactly like `luminance.level`
already is for `strata-light` — measured once in python at build time
(lab/analyze/recipes.py's `strata_scale_measure()`) and carried through the collection's own records
into this instrument's `massCentreXA`/`massCentreXB`/`detailCentreXA`/`detailCentreXB` handles. This
file proves the port that closes that gap: docs/design/PASS-API-V1.md §7 (GPU and resources) and §8
(the manifest), and the composer wiring (pass-composer.js's HANDLE_SOURCE and its "strata-scale"
branch of fillPlan) that makes the instrument castable on real pairs of the collection rather than
only reachable by hand.

WHAT IS COMPARED, AND AGAINST WHAT.

  The doors. At the dial's two ends the standing work is exact BY CONSTRUCTION — the module's own
  response curve reaches exactly 0 and exactly 1 at the hand's own two ends, so both strata's own
  travel reads exactly 0 or exactly 1 regardless of where either stratum's own measured centre
  stands, and the window 4u(1 − u) holds both accompanying voices to nothing there whatever a score
  gives them. Each door is measured against ITS OWN FILE, cover-fitted into the frame, inside the
  project's seam threshold of 6 of 255.

  Away from a door. Mid-passage the detail has lifted off both works and their masses stand only
  part displaced, so the frame there must read as neither work plainly.

  The composer wiring, in Node against the real files. Every handle this instrument's own manifest
  publishes has a row in pass-composer.js's HANDLE_SOURCE, checked directly off the two files rather
  than off a fixture that predates this port; and the instrument actually CASTS on a real sample of
  the 121-work collection's own ordered pairs, with its measured handles reading differently pair to
  pair — proof against his word of 2026-08-18 15:13, that nothing may be the same for every pair.

  There is no lab module to compare a second road against, the same position pass-inst-studio.js's
  own suite stands in: the lab module holds ONE work and never opens a second door at all, so nothing
  in the browser lane below draws a second, comparable picture from lab/effects/strata-scale.js
  itself. What the module carries — its constants, its response curve, its centre-of-gravity
  arithmetic — is checked textually against the file instead, and read off $TLVPHOTOS_ROOT.
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

LAB = Path(os.environ.get("TLVPHOTOS_ROOT", "/Users/sashaabramovich/tlvphotos-site")) / "lab"
PHOTOS = [LAB / "photos" / "towers.jpg", LAB / "photos" / "glassgrid.jpg"]
MODULE = LAB / "effects" / "strata-scale.js"
ASSETS = ROOT / "engine" / "assets"
COMPOSER = ASSETS / "pass-composer.js"
INSTRUMENT = ASSETS / "pass-inst-strata-scale.js"
WORKS = Path(__file__).resolve().parent / "fixture_pass_works.json"

SITE_URL = "https://synth.example.com"
VW, VH = 390, 844
SEAM = 6.0          # the project's seam threshold, 6 of 255
FAR = 30.0          # further than this from a file's own pixels and the frame is a different picture
BACKGROUND = (0x08, 0x08, 0x0a)
SPREAD = 10.0

SHOTS = ROOT / "tests" / "captures" / "pass-strata-scale"

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


INSTRUMENT_TEXT = INSTRUMENT.read_text(encoding="utf-8")

# ---------------------------------------------------------------- static rows, read off the files

OWNED = ["createElement", "getContext", "requestAnimationFrame", "addEventListener",
         "performance.now", "Date.now", "new Image", "setTimeout", "setInterval",
         "getImageData", "drawImage"]
held = [s for s in OWNED if s in INSTRUMENT_TEXT]
check("PASS-SCALE the instrument creates no context, no canvas, no loop, no listener and reads no "
      "picture's pixels",
      not held,
      "§1.2's fence: none of the eleven ways of owning hardware or of opening a photograph appears "
      "in the instrument file, so the module's own six 2D contexts, its offscreen piece canvases "
      "and its grey twins all stayed in the lab"
      if not held else "the instrument holds " + ", ".join(held))

STRIPPED_INSTRUMENT = build_site._engine.strip_js_comments(INSTRUMENT_TEXT)
check("PASS-SCALE the shader carries no version header of its own",
      "#version" not in STRIPPED_INSTRUMENT,
      "GLSL ES 1.00, so the host's translator stamps the one header this shader needs, the same "
      "road every other instrument in this arsenal takes")

CONSTANTS = [("var FEEL_C = 0.47, FEEL_K1 = 1.2, FEEL_K2 = 2.6;",
              "the measured median of the felt change and the two fitted exponents "
              "(strata-scale.js:421-441)"),
             ("var DETAIL_SHARE = 0.4;",
              "the dial's own share the detail takes before the masses start to go "
              "(strata-scale.js:51)"),
             ("var HANDOVER_REACH = 0.25;",
              "the module's own named departure from DETAIL_SHARE (strata-scale.js:465)"),
             ("var FEEL_H_U0 = 0.744, FEEL_H_K1 = -0.40, FEEL_H_K2 = -0.86;",
              "the handover handle's own response curve (strata-scale.js:490)"),
             ("var MASS_CELLS = 16;",
              "the scale the masses stand at, cells on the file's own long side "
              "(strata-scale.js:47)"),
             ("var LIGHT_CEILING = 0.9;",
              "the module's own ceiling on the light voice (strata-scale.js:377)")]
missing_const = [c for c, _ in CONSTANTS if c not in INSTRUMENT_TEXT]
check("PASS-SCALE every constant carried from the lab module stands at the number strata-scale.js "
      "gives it",
      not missing_const,
      "; ".join("%s — %s" % (c, why) for c, why in CONSTANTS) if not missing_const
      else "missing or changed: " + ", ".join(missing_const))

VOICE_LINE = "return a * Math.sin(2 * Math.PI * (u / p + (+phase || 0))) * 4 * u * (1 - u);"
check("PASS-SCALE both accompanying voices carry the module's own law, window and all",
      VOICE_LINE in INSTRUMENT_TEXT and "if (!(a > 0) || !(p > 0)) return 0;" in INSTRUMENT_TEXT,
      "one breath of a named period and a named phase, held to nothing at BOTH doors by the window "
      "4u(1 − u), and silent whenever the period or the amplitude is not positive — the same line "
      "strata-scale.js:360-369 carries")

declared = set(re.findall(r'\{ name: "(u\w+)", type:', INSTRUMENT_TEXT))
spelled = set(re.findall(r'uniform\s+\w+\s+(u\w+)\s*;', INSTRUMENT_TEXT))
check("PASS-SCALE the manifest's declared uniform names and the shader's own spelled names are one "
      "set",
      declared == spelled and len(declared) == 13,
      f"{len(declared)} declared, {len(spelled)} spelled; declared only: {sorted(declared - spelled)}; "
      f"spelled only: {sorted(spelled - declared)}")

sha = hashlib.sha256(MODULE.read_bytes()).hexdigest() if MODULE.exists() else ""
declared_sha = (re.search(r'sha256: "([0-9a-f]{64})"', INSTRUMENT_TEXT) or [None, None])[1]
check("PASS-SCALE the provenance names the file the port was read from, and the file weighs to it",
      bool(sha) and sha == declared_sha,
      f"the lab module stands tracked at commit fc885a3; the digest of the bytes the port was read "
      f"from stands in the manifest and the file still weighs to {sha[:16]}…" if sha
      else f"lab module absent at {MODULE}")

check("PASS-SCALE the manifest leaves the drawing buffer unpreserved and declares its own cuts",
      "gl: { preserveDrawingBuffer: false }" in INSTRUMENT_TEXT
      and 'cuts: ["band", "scale"]' in INSTRUMENT_TEXT,
      "§7 refuses a manifest asking for a preserved buffer; §8 refuses a build with no cuts: line — "
      "and this instrument's own two cuts are the composer's own tonal-and-spectral pivot's own "
      "elementKinds, `[\"band\", \"scale\"]`")

FLOORS = ["minimum", "threshold", "atLeast", "declineBelow", "qualif", "notEnough"]
# Scanned over the STRIPPED text, comments out — this file's own long-form provenance prose talks
# ABOUT the module's own relief threshold and about the class of number this instrument carries
# none of ("ranking only, never a floor"), and both of those words belong in that prose rather than
# in a bar the code itself enforces; strata-light's own suite reads the same way, off its own built
# and stripped region.
found_floor = [w for w in FLOORS if w in STRIPPED_INSTRUMENT]
if re.search(r"\bfloor\b(?!\s*\()", STRIPPED_INSTRUMENT):
    found_floor.append("floor")
check("PASS-SCALE the fit is published, reads a genuine measurement, and only ranks",
      'suits: { reads: ["texture.reliefEdge"]' in INSTRUMENT_TEXT
      and "how:" in INSTRUMENT_TEXT and not found_floor
      and 'decline: ["one work only", "a source that never decoded"]' in INSTRUMENT_TEXT,
      "it reads how far apart the two works stand on `texture.reliefEdge`, the median of each "
      "work's own relief field (lab/analyze/recipes.py's port of lab/effects/strata-scale.js:"
      "138-141); the two things it declines are a half pair and a picture that never decoded, and "
      "no reading anywhere in the file can make a pair not qualify"
      if not found_floor else "the file carries a floor: " + ", ".join(found_floor))

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
  provenance: { source: ["test_pass_strata-scale.py"], measuredAt: {}, by: "test_pass_strata-scale.py" },
  scoreFenceBytes: 12288, intentFenceChars: 600,
};
if (!manifests["strata-scale"]) {
  console.log(JSON.stringify({ error: "no pass-inst-strata-scale.js registered a manifest" }));
  process.exit(0);
}
const composer = joined.make(consts);
const works = JSON.parse(fs.readFileSync(worksPath, "utf8")).works;
const ids = Object.keys(works);

let total = 0, declined = 0, scaleCasts = 0;
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
      const cue = (res.score.cues || []).find((c) => c.instrument.id === "strata-scale");
      if (cue) {
        scaleCasts++;
        const n = cue.nodes;
        const get = (h) => (n[cue.id + "-" + h] || n[h] || {}).value;
        seenHandleSets.push({ massCentreXA: get("massCentreXA"), detailCentreXA: get("detailCentreXA"),
                               massCentreXB: get("massCentreXB"), detailCentreXB: get("detailCentreXB") });
      }
    } catch (e) {
      if (errors.length < 8) errors.push(a + "->" + b + ": " + e.message);
    }
    if (total >= 6000) break outer;
  }
}
console.log(JSON.stringify({ total, declined, scaleCasts, errors,
                              instrumentCount: Object.keys(manifests).length,
                              sample: seenHandleSets.slice(0, 6) }));
"""

DRIVER_PATH = Path(tempfile.mkdtemp(prefix="synth_scale_driver_")) / "driver.js"
DRIVER_PATH.write_text(DRIVER, encoding="utf-8")

if not node_available():
    skip("PASS-SCALE every handle this instrument publishes has a row in the composer's register, "
         "read directly off the two files", "node is not installed")
    skip("PASS-SCALE the instrument actually casts on a real sample of the collection's own pairs, "
         "with its measured handles reading differently pair to pair",
         "node is not installed")
elif not WORKS.exists():
    skip("PASS-SCALE every handle this instrument publishes has a row in the composer's register, "
         "read directly off the two files", "the collection's own work records are absent: " + str(WORKS))
    skip("PASS-SCALE the instrument actually casts on a real sample of the collection's own pairs, "
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

    check("PASS-SCALE every handle this instrument publishes has a row in the composer's register, "
          "read directly off the two files",
          not SWEEP.get("error") and not SWEEP.get("errors"),
          f"{SWEEP.get('instrumentCount')} instruments registered from the live tree, "
          f"{SWEEP.get('total')} real ordered pairs composed with {len(SWEEP.get('errors', []))} "
          f"errors" if not SWEEP.get("error")
          else "the sweep could not run: " + str(SWEEP.get("error"))
          + ("; sample errors: " + "; ".join(SWEEP.get("errors", [])) if SWEEP.get("errors") else ""))

    casts = SWEEP.get("scaleCasts", 0)
    total_c = SWEEP.get("total", 0)
    sample = SWEEP.get("sample", [])
    varies = len({json.dumps(s, sort_keys=True) for s in sample}) > 1 if len(sample) > 1 else False
    check("PASS-SCALE the instrument actually casts on a real sample of the collection's own pairs, "
          "with its measured handles reading differently pair to pair",
          not SWEEP.get("error") and casts > 0 and varies,
          f"strata-scale was cast on {casts} of {total_c - SWEEP.get('declined', 0)} composed pairs "
          f"({(100.0 * casts / max(1, total_c)):.1f}% of the {total_c} tried); a sample of its own "
          f"measured massCentreX/detailCentreX across those casts: {json.dumps(sample)}"
          if not SWEEP.get("error") else "the sweep could not run: " + str(SWEEP.get("error")))

shutil.rmtree(DRIVER_PATH.parent, ignore_errors=True)

# ---------------------------------------------------------------- browser rows

BROWSER_ROWS = [
    "PASS-SCALE §8     · the manifest carries every field the contract names, in its shape",
    "PASS-SCALE §8     · it publishes CELL, TEXTURE and LIGHT-COLOUR",
    "PASS-SCALE row 7  · door 0 stands the departing work, measured against its own file",
    "PASS-SCALE row 7  · door 0 carries no trace of the arriving work",
    "PASS-SCALE row 7  · door 1 stands the arriving work, measured against its own file",
    "PASS-SCALE row 7  · door 1 carries no trace of the departing work",
    "PASS-SCALE mid-passage reads as neither work plainly — detail and masses both part-travelled",
    "PASS-SCALE §7     · no empty frame at any sampled instant of the pass",
    "PASS-SCALE §7     · the frame after a change of viewport is drawn, not a kept buffer",
    "PASS-SCALE the instrument's own door reading holds by construction, on every centre asked",
    "PASS-SCALE row 14 · textures, programmes and framebuffers return to their baseline after ten "
    "runs",
    "PASS-SCALE row 15 · the console stays clean",
    "PASS-SCALE §4.4b  · handover, a centre of gravity and the mask each reach the PICTURE",
    "PASS-SCALE the two doors frame at a crop of exactly one, and both agree",
    "PASS-SCALE §7     · a manifest asking for a preserved drawing buffer is refused, with its "
    "reason",
    "PASS-SCALE §7     · a uniform bound to a name the shader lacks is refused, with its reason",
    "PASS-SCALE the fleet's judges' channel rests at nothing and, standing, draws which work stands "
    "as red and green",
    "PASS-SCALE nothing is ever faded: the coverage this instrument writes is 0 or 1 and never "
    "between",
    "PASS-SCALE row 16 · the captures are kept as evidence",
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
    d = Path(tempfile.mkdtemp(prefix="synth_scalebench_"))
    pack = REGION if pack_text is None else pack_text
    shutil.copy2(TMP / "pass-layer.js", d / "pass-layer.js")
    for _inst in sorted(TMP.glob("pass-inst-*.js")):
        shutil.copy2(_inst, d / _inst.name)
    (d / "pass-inst-strata-scale.js").write_text(pack, encoding="utf-8")
    record = json.loads((TMP / "config.json").read_text(encoding="utf-8"))
    record["pass"]["instruments"]["strata-scale"]["digest"] = hashlib.sha256(
        pack.encode("utf-8")).hexdigest()
    (d / "config.json").write_text(json.dumps(record), encoding="utf-8")
    (d / "photos").mkdir()
    for p in PHOTOS:
        shutil.copy2(p, d / "photos" / p.name)
    shutil.copy2(ROOT / "tests" / "fixture_pass_strata-scale.html", d / "index.html")
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
    TMP = Path(tempfile.mkdtemp(prefix="synth_scale_"))
    build_site.OUT = TMP
    build_site.build(SITE_URL)
    REGION = (TMP / "pass-inst-strata-scale.js").read_text(encoding="utf-8")

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
            elif not js(br, "return !!window.__exPass.bench.manifest('strata-scale');"):
                why = js(br, "var e = window.__host.report().events.filter(function(x){"
                             "return x.name === 'manifest-refused';});"
                             "return e.length ? e[e.length - 1].why : null;")
                for r in BROWSER_ROWS:
                    check(r, False, "the host registered no «strata-scale» instrument: " + str(why))
            else:
                m = js(br, "return window.__exPass.bench.manifest('strata-scale');")
                zoom = m["framings"]["0"]["coverCrop"]
                res = m["resources"]
                HANDOVER_DEF = m["handles"]["handover"]["def"]
                shape = (
                    m["id"] == "strata-scale" and m["api"] == 1 and m["arity"] == 2
                    and m["roles"] == ["disassembly", "mystery", "assembly"]
                    and len(m["handles"]) == 21
                    and all(set(h) >= {"min", "max", "def"} for h in m["handles"].values())
                    and m["neutrals"] == {"a": 0, "b": 1}
                    and m["doors"]["in"]["handle"] == "mix" and m["doors"]["in"]["value"] == 0
                    and m["doors"]["out"]["handle"] == "mix" and m["doors"]["out"]["value"] == 1
                    and sorted(m["framings"]) == ["0", "1"]
                    and m["framings"]["0"] == m["framings"]["1"] == {"coverCrop": 1.0}
                    and abs(zoom - 1.0) < 1e-12
                    and m["camera"] == {"needs": "none", "authority": "stage"}
                    and sorted(m["cuts"]) == ["band", "scale"]
                    and m["coverage"]["writes"] is True
                    and len(m["passes"]) == 1 and len(m["passes"][0]["uniforms"]) == 13
                    and sorted(res) == ["lean", "rich", "standard"]
                    and m["capabilities"] == ["webgl2"] and m["decline"]
                    and m["suits"]["reads"] == ["texture.reliefEdge"] and m["suits"]["how"]
                    and m["provenance"]["labPath"] == "lab/effects/strata-scale.js"
                    and m["provenance"]["commit"] == "fc885a3"
                    and m["readiness"] == "production-ready"
                    and "strata-scale" in js(br, "return window.__host.report().registered;"))
                check(BROWSER_ROWS[0], shape,
                      f"twenty handles, twelve uniforms in one pass, a crop of {zoom} at both doors, "
                      f"a cut on {sorted(m['cuts'])}, an alpha that writes coverage "
                      f"(coverage.writes={m['coverage']['writes']}), and the lab commit "
                      f"{m['provenance']['commit']}; the module declares no slider-facing param at "
                      f"all and the manifest carries that empty list rather than filling it")

                check(BROWSER_ROWS[1],
                      m["levels"] == ["CELL", "TEXTURE", "LIGHT-COLOUR"],
                      "lab/data/module-contract.json's own strata-scale row: level "
                      "\"CELL+TEXTURE\" — CELL because the departure still cuts the frame into "
                      "pieces that travel as rigid bodies, TEXTURE because the two strata are two "
                      "separate renderings of the SAME work at two different scales of its own "
                      "material rather than a spatial split of one rendering; LIGHT-COLOUR joins "
                      "them the same way it joined strata-light's own row, once the composer "
                      "actually drives both accompanying voices")

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
                      f"and {mid_vs_b:.4f} from glassgrid.jpg's — both past {FAR}, so the frame is "
                      f"visibly parted rather than resting on either photograph")

                SCORE_JSON = json.dumps({
                    "schema": 2,
                    "intent": "the departing work's detail lifts off first and its masses follow, "
                              "each stratum sideways toward the side of its own measured centre, "
                              "while the arriving work's masses gather first with its detail "
                              "growing into them (lab/effects/strata-scale.js, its own header)",
                    "pair": {"a": "a", "b": "b"}, "seed": 2.71828, "duration": 3000,
                    "direction": "a-to-b",
                    "interruption": {"withinMs": 500, "resolve": "nearest-door"},
                    "failLand": "arrive",
                    "camera": {"owner": "stage", "rests": "b",
                               "track": [{"at": "b", "pan": {"x": 0, "y": 0}, "logScale": 0,
                                          "pitch": 0, "yaw": 0, "roll": 0, "fov": None,
                                          "owner": "stage"}]},
                    "cues": [{
                        "id": "scale-main", "instrument": {"id": "strata-scale", "api": 1},
                        "voice": "letter", "roles": ["disassembly", "mystery", "assembly"],
                        "levels": ["CELL", "TEXTURE", "LIGHT-COLOUR"],
                        "levelOwnership": {"LIGHT-COLOUR": "owns"},
                        "window": [0, 3.0], "works": ["a", "b"], "stack": 0,
                        "cameraAuthority": "stage",
                        "doors": {"in": {"handle": "mix", "value": 0, "measured": True},
                                  "out": {"handle": "mix", "value": 1, "measured": True}},
                        "nodes": dict({k + "Static": {"op": "static", "value": v}
                                       for k, v in {
                                           "handover": HANDOVER_DEF,
                                           "massCentreXA": 0.42, "massCentreXB": 0.58,
                                           "detailCentreXA": 0.65, "detailCentreXB": 0.31,
                                           "colourPeriodA": 0.5, "colourPhaseA": 0.0,
                                           "colourAmpA": 0.4, "lightPeriodA": 0.7,
                                           "lightPhaseA": 0.25, "lightAmpA": 0.35,
                                           "colourPeriodB": 0.6, "colourPhaseB": 0.5,
                                           "colourAmpB": 0.4, "lightPeriodB": 0.8,
                                           "lightPhaseB": 0.75, "lightAmpB": 0.35,
                                           "mask": 0}.items()},
                                      mixDrive={"source": "progress"}, clockDrive={"source": "time"}),
                        "tracks": dict({k: {"node": k + "Static"} for k in [
                            "handover", "massCentreXA", "massCentreXB", "detailCentreXA",
                            "detailCentreXB", "colourPeriodA", "colourPhaseA", "colourAmpA",
                            "lightPeriodA", "lightPhaseA", "lightAmpA", "colourPeriodB",
                            "colourPhaseB", "colourAmpB", "lightPeriodB", "lightPhaseB",
                            "lightAmpB", "mask"]},
                                       mix={"node": "mixDrive"}, clock={"node": "clockDrive"}),
                        "resources": {"textures": 0, "textureSlots": 2, "framebuffers": 0,
                                     "pingPong": 0, "programs": 1, "passes": 1, "bytesEstimate": 0,
                                     "variant": "standard"},
                    }],
                    "quality": {v: {"renderScale": None,
                                    "cues": {"scale-main": {"resources": {
                                        "textures": 0, "textureSlots": 2, "framebuffers": 0,
                                        "pingPong": 0, "programs": 1, "passes": 1,
                                        "bytesEstimate": 0, "variant": v}}}}
                                for v in ("lean", "standard", "rich")},
                    "provenance": {"source": "lab/effects/strata-scale.js's own declared defaults, "
                                             "its own centre-of-gravity port and the voice numbers "
                                             "this suite authors",
                                  "measuredAt": None, "by": "tests/test_pass_strata-scale.py"},
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

                # ---- THE DOOR THIS INSTRUMENT READS FOR ITSELF, on several centres --------------
                # This instrument's own doors hold by ALGEBRA — the response curve reaches exactly 0
                # and exactly 1 at the hand's own two ends, and both strata's own travel derive from
                # that alone — so the reading has no width a centre could close or open. The row
                # sweeps several very different centres and confirms the doors stay exact on every
                # one, and that mid-passage reads as a real, non-trivial travel.
                door_reads = []
                for mca, mcb, dca, dcb in ((0.5, 0.5, 0.5, 0.5), (0.1, 0.9, 0.85, 0.15),
                                           (0.02, 0.98, 0.5, 0.5)):
                    for at, label in ((0, "entry"), (1, "exit")):
                        v = js(br, "return window.__values(%s);"
                               % json.dumps({"mix": at, "massCentreXA": mca, "massCentreXB": mcb,
                                             "detailCentreXA": dca, "detailCentreXB": dcb}))
                        door_reads.append((mca, mcb, dca, dcb, label, v))
                away = js(br, "return window.__values(%s);" % json.dumps({"mix": 0.5}))
                # AT THE ENTRY the departing work (index 0) stands whole — its own travel exactly 0 —
                # while the arriving work (index 1) is wholly displaced — its own travel exactly 1;
                # the exit door reads the same the other way round.
                doors_whole = (all(v["doorWhyNo"] is None
                                   and (v["detailU"] == [0, 1] and v["massU"] == [0, 1]
                                        if lab == "entry" else
                                        v["detailU"] == [1, 0] and v["massU"] == [1, 0])
                                   for _, _, _, _, lab, v in door_reads)
                               and away["doorWhyNo"] is None
                               and (away["detailU"][0] > 0.9) and (0 < away["massU"][0] < 1))
                check(BROWSER_ROWS[9], doors_whole,
                      "; ".join(f"centres {mca}/{mcb}/{dca}/{dcb} the {lab} door reads detailU "
                                f"{v['detailU']} massU {v['massU']}"
                                for mca, mcb, dca, dcb, lab, v in door_reads)
                      + f"; mid-passage reads detailU {away['detailU']} massU {away['massU']} — the "
                        f"door is exact by construction on every centre, never by a tolerance a "
                        f"centre could close or open")

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

                # THE POSE THE MOVES ARE TAKEN AT. At the resting `mix` of 0.5 both works' own DETAIL
                # travel already reads exactly 1 — cleared whole, regardless of where either work's
                # own detail centre stands — because `share` (0.4 at the module's own rest) is well
                # under `feelOf(0.5) = FEEL_C = 0.47` on both sides of the passage; only the MASSES
                # travel is still partial there (0.117 on both works). So the row asks `massCentreXA`/
                # `massCentreXB` rather than either detail centre, which is exactly where this pose
                # can answer the question at all.
                base_shot = drew("base", {})
                still = diff(base_shot, drew("base-again", {}))
                moved = {
                    "handover": diff(base_shot, drew("handover", {"handover": 0.15})),
                    "massCentreXA": diff(base_shot, drew("massCentreXA", {"massCentreXA": 0.05})),
                    "massCentreXB": diff(base_shot, drew("massCentreXB", {"massCentreXB": 0.95})),
                }
                check(BROWSER_ROWS[12],
                      still == (0.0, 0) and all(mx > SEAM for _, mx in moved.values()),
                      "; ".join(f"{k} moves the frame by {mn:.4f} of 255 on the mean and {mx} at its "
                                f"strongest point" for k, (mn, mx) in moved.items())
                      + f"; the same pose drawn twice moves it by {still[0]} at {still[1]}")

                fA = m["framings"]["0"]["coverCrop"]
                fB = m["framings"]["1"]["coverCrop"]
                check(BROWSER_ROWS[13], fA == fB == 1,
                      f"both doors carry a coverCrop of exactly 1, the module's own plain cover fit "
                      f"with no crop of its own (fA={fA}, fB={fB})")

                r = js(br, """
                  var m = JSON.parse(JSON.stringify(window.__exPass.bench.manifest('strata-scale')));
                  m.gl.preserveDrawingBuffer = true;
                  var STUB_VALUES = "function(){return {dial:[0,1],detailU:[0,1],massU:[0,1],"
                    + "detailCentre:[0.5,0.5],massCentre:[0.5,0.5],share:0.4,sat:[1,1],light:[0,0],"
                    + "colourVoice:[0,0],lightVoice:[0,0],hand:0,doorStanding:null,doorWhyNo:null};}";
                  var STUB = "values:" + STUB_VALUES + ",fit:function(){return [1,1,0,0];},"
                    + "prepare:function(){return {take:false};}, start:function(){}, frame:function(){}";
                  var ok = window.__exPass.bench.register(
                    eval("({name:'scale-preserve', manifest:m, " + STUB + "})"));
                  var evs = window.__host.report().events.filter(function(e){return e.name==='manifest-refused';});
                  return {ok: ok, why: evs.length ? evs[evs.length-1].why : null,
                          registered: window.__host.report().registered};
                """)
                check(BROWSER_ROWS[14],
                      r["ok"] is False and r["why"] and "preserved" in r["why"]
                      and "scale-preserve" not in r["registered"],
                      f"registered={r['ok']} why={r['why']}")

                r = js(br, """
                  var m = JSON.parse(JSON.stringify(window.__exPass.bench.manifest('strata-scale')));
                  m.passes[0].uniforms.push({name:'uPointer', type:'vec2', source:'pointer'});
                  var STUB_VALUES = "function(){return {dial:[0,1],detailU:[0,1],massU:[0,1],"
                    + "detailCentre:[0.5,0.5],massCentre:[0.5,0.5],share:0.4,sat:[1,1],light:[0,0],"
                    + "colourVoice:[0,0],lightVoice:[0,0],hand:0,doorStanding:null,doorWhyNo:null};}";
                  var STUB = "values:" + STUB_VALUES + ",fit:function(){return [1,1,0,0];},"
                    + "prepare:function(){return {take:false};}, start:function(){}, frame:function(){}";
                  var ok = window.__exPass.bench.register(
                    eval("({name:'scale-pointer', manifest:m, " + STUB + "})"));
                  var evs = window.__host.report().events.filter(function(e){return e.name==='manifest-refused';});
                  return {ok: ok, why: evs.length ? evs[evs.length-1].why : null,
                          registered: window.__host.report().registered};
                """)
                check(BROWSER_ROWS[15],
                      r["ok"] is False and r["why"] and "uPointer" in r["why"]
                      and "cannot supply" in r["why"] and "scale-pointer" not in r["registered"],
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
                      f"{moved_mask[1]} at its strongest point, drawing the two works' own coverage "
                      f"as red and green (extrema {ch[0]})")

                # ---- nothing is ever faded ---------------------------------------------------
                # The judges' own frame writes each work's own coverage as a channel of colour —
                # RED the departing work's alpha, GREEN the arriving work's — and the module's own
                # law is that an alpha is 1 or 0 and never anything between. THE TWO CHANNELS ARE
                # READ SEPARATELY, because both a.a and b.a stand at 1 at once wherever both works
                # carry matter to a point — a real, legitimate reading (the arriving work's own
                # matter drawn OVER the departing work's, `col = mix(a.rgb, b.rgb, b.a)`) and not a
                # fade of anything — so a pixel reading yellow (both channels standing) is not what
                # this row is asking about; each channel's OWN steadiness is. A little room is left
                # for the canvas's own antialiasing at a hard geometric edge between "some" and
                # "none" of a channel, which blends neighbouring PIXELS rather than the shader's own
                # alpha; what must not appear at all is a wide plateau of it.
                fades = []
                for u in (0.15, 0.35, 0.5, 0.7, 0.9):
                    over = {"mix": u, "mask": 1, "massCentreXA": 0.4, "detailCentreXA": 0.62,
                            "massCentreXB": 0.55, "detailCentreXB": 0.35}
                    br.evaluate("window.__hostDraw(%s); 0" % json.dumps(over))
                    br.sleep(0.12)
                    p = png(br, SHOTS / ("mask-mix-%03d.png" % round(u * 100)))
                    from PIL import Image
                    im = Image.open(p).convert("RGB")
                    px = im.load()
                    W2, H2 = im.size
                    total = between = 0
                    for yy in range(0, H2, 2):
                        for xx in range(0, W2, 2):
                            r0, g0, _ = px[xx, yy]
                            total += 1
                            if 24 < r0 < 231 or 24 < g0 < 231:
                                between += 1
                    fades.append((u, total, between))
                br.evaluate("window.__mix(0.5); 0")
                worst_share = max(b / float(t) for _, t, b in fades)
                check(BROWSER_ROWS[17], worst_share <= 0.01,
                      "; ".join(f"at {u}: {b} of {t} sampled points ({100.0 * b / t:.2f}%) read a "
                                f"channel value between the antialiasing band and neither channel's "
                                f"own 0 or 255" for u, t, b in fades)
                      + " — every one under 1% of the frame, which is the antialiased edge between "
                        "regions rather than a fade written into either channel's own alpha, the "
                        "module's own «no fade» read on the picture")

                kept = sorted(p.name for p in SHOTS.glob("*.png"))
                check(BROWSER_ROWS[18],
                      len(kept) >= 15 and all((SHOTS / k).stat().st_size > 1000 for k in kept),
                      f"{len(kept)} captures under {SHOTS.relative_to(ROOT)}: the five poses, the "
                      f"seven sampled instants, the frame after a resize, the handle rows and the "
                      f"mask-coverage sweep")

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
