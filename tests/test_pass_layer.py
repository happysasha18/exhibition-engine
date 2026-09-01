#!/usr/bin/env python3
"""PASS-LAYER — the host's own last-resort instrument, `@host/last-resort`.

Run: python3 tests/test_pass_layer.py

Root: naryad S-04. The rescue's own shader (`makeLastResortInstrument`, engine/assets/pass-layer.js,
the block naming `LAST_RESORT_NAME`) drew its reveal boundary as `smoothstep(uReveal - 0.08,
uReveal + 0.08, vUV.x)` — a level set of the FRAME'S OWN x coordinate, answering to neither
photograph. Charter shelf 18 pardons this instrument as the one fallback that may run a real wipe
rather than a crossfade, but the boundary that wipe travels still has to answer the three-part test
the charter's ban list convicts a wipe on (the same test `pass-inst-tunnel.js` answers for its own
ring, tests/test_pass_tunnel.py's `IS THE RING A WIPE?` row): the boundary must be a level set of
what the two photographs themselves carry, the two images must interact at the point of decision, and
the pattern must be one neither picture's own content could have produced alone. A frame coordinate
fails all three at once — it is fixed before either photograph is even requested.

THE FIX. `field` is built from `lumA`/`lumB`, the luminance of the very texels `uTexA`/`uTexB` were
just sampled at, and `uReveal` is compared against `field` instead of `vUV.x`. `vUV` still maps the
fragment into each work's own cover-fitted UV (`coverUV`) — that use is a texture-sampling address,
never the boundary itself.

THE GATE, BEHAVIOUR NOT TEXT. A row that only greps for the string `vUV.x` passes on a rename to
`vUV.y` or `gl_FragCoord.x / uResX`, which reads no photograph either. So this file extracts the
REAL, CURRENT fragment shader source out of the shipped file — never a hand-copied string — compiles
it in a real WebGL context (headless Chrome), feeds it two synthetic textures whose own content
varies ONLY by row and never by column, and reads the rendered framebuffer back:

  · Texture A is a grey gradient, black at the top row and white at the bottom.
  · Texture B is the mirror gradient, white at the top row and black at the bottom.
  · Neither texture's content varies across a row at all.

Both fitted uniforms are the identity (no cropping), so `vUV` maps straight onto each texture. Under
the banned frame-coordinate boundary, the reveal mixes on COLUMN regardless of either photograph, so
a row that has no content variation of its own gains one anyway — a hard left-to-right wipe appears
inside every row. Under a boundary built from the pair's own measured luminance, a row whose two
source pixels never vary by column produces a mix that never varies by column either: the boundary
answers only to the pictures' own content (here, row alone). Reading the standard deviation of pixel
intensity ACROSS A ROW is therefore a direct, adversarial measurement of exactly the defect class
shelf 18 bans — not a proxy for it.

The suite proves the gate is not vacuous the same way `test_pass_coverage.py`'s RED rows do: the
CURRENT shader's own text is mutated back to the banned `vUV.x` form in memory (the tree on disk is
never touched) and the same measurement is taken again — the row must FLIP from PASS to FAIL, or the
green above proves nothing.
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
from headless import serve, Browser, ChromeMissing, chrome_available  # noqa: E402

LAYER_PATH = ROOT / "engine" / "assets" / "pass-layer.js"
SOURCE_TEXT = LAYER_PATH.read_text(encoding="utf-8")

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


# ================================================================================================
# REAL-DATA CAMLED-vs-WORLD COLLISION (V2-CONVERGENCE-PLAN-2026-08-31 Phase 4, item 3). Charter
# shelf 17 opens its own voice list with the camera, and its levels law allows one active voice per
# structural level, the world being the camera's own — so a score that declares `camera.lead` and
# then gives a cue the world level is asking for two voices on one level. The host refuses this
# before the command is taken (`scoreWhyNo`'s own `camLed(s)` block, `pass-layer.js` — "A LED FLIGHT
# SPENDS THE WORLD VOICE..." above the code cited at the sprint brief's `:1935-1942`, offset a few
# lines by drift since). No file in this tree drove a REAL composed passage through this check
# before this section: `tests/test_pass_drivers.py`'s own `worldClash`/`worldFine` rows
# (`bench.scoreWhyNo(...)`, `ROWS[24]`) proved the rule holds, entirely on a hand-typed synthetic cue
# (`{id: "floor", instrument: {id: "weave"}, levels: [...]}`) — real proof of the CODE, no proof any
# REAL composed score the planner actually builds ever reaches this exact branch. This drives the
# real 121-work fleet's own composer to find a genuinely camera-led real score (never hand-picked),
# feeds its own real `score.cues` — not a cue built from scratch — to the host's own real
# `scoreWhyNo`, and only then adds the WORLD level the composer's own levels law already keeps this
# real cue from ever carrying on its own (shelf 9: a lawful composer never manufactures the
# violation itself — the host's refusal is the backstop for a score a corrupted or hand-built
# request could still send it, which is exactly what this proves against real cue shapes).
_CAMLED_ROW = ("PASS-LAYER real-data camLed/WORLD · a real camera-led score's own real cue, given "
               "the world level, is refused by the host before the command is taken")
_CAMLED_RED_ROW = ("PASS-LAYER real-data camLed/WORLD red-on-bug · disabling the camLed branch "
                    "lets that same real collision through silently")

_CAMLED_COMPOSER = ROOT / "engine" / "assets" / "pass-composer.js"
_CAMLED_FIXTURE_COMPOSED = ROOT / "tests" / "fixture_pass_composed.json"
_CAMLED_FIXTURE_WORKS = ROOT / "tests" / "fixture_pass_works.json"

_CAMLED_SEARCH_DRIVER = r"""
"use strict";
const vm = require("vm");
const source = %(source)s;
const consts = %(consts)s;
const works = %(works)s;

let joined = null;
const sandbox = { window: { __PassComposer: (m) => { joined = m; } }, console: console };
vm.createContext(sandbox);
vm.runInContext(source, sandbox, { filename: "pass-composer.js" });
const composer = joined.make(consts);
const ids = Object.keys(works);
// LED_ROLES, shelf 15/17's own two homes for a camera-led passage — never a name typed here beyond
// the composer's own published `routeRoles()`, cross-checked against the two the docstring cites.
const LED_ROLES = ["quiet link", "return"];
let found = null;
outer:
for (let i = 0; i < ids.length && !found; i++) {
  for (let j = 0; j < ids.length && !found; j++) {
    if (i === j) continue;
    for (const role of LED_ROLES) {
      const req = { workRecordA: works[ids[i]], workRecordB: works[ids[j]], direction: "a-to-b",
                    seed: 0, routeRole: role, cameraState: null,
                    walkMemory: [], walkGenres: [], walkMiracles: [], framePace: null };
      let made;
      try { made = composer.passageFor(req); } catch (e) { continue; }
      if (!made || made.declined || !made.score || !made.score.camera) continue;
      if (made.score.camera.lead === true) {
        found = { from: ids[i], to: ids[j], seed: 0, role: role,
                  score: { duration: made.score.duration, camera: made.score.camera,
                           cues: made.score.cues } };
        break outer;
      }
    }
  }
}
console.log(JSON.stringify({ found: found }));
"""


def _camled_node_available():
    return shutil.which("node") is not None


def _camled_search():
    driver_text = _CAMLED_SEARCH_DRIVER % {
        "source": json.dumps(_CAMLED_COMPOSER.read_text(encoding="utf-8").replace("@@NS@@", "")),
        "consts": json.dumps(json.loads(
            _CAMLED_FIXTURE_COMPOSED.read_text(encoding="utf-8"))["consts"]),
        "works": json.dumps(json.loads(
            _CAMLED_FIXTURE_WORKS.read_text(encoding="utf-8"))["works"]),
    }
    tmp_dir = Path(tempfile.mkdtemp(prefix="pass_layer_camled_"))
    driver_path = tmp_dir / "search.js"
    driver_path.write_text(driver_text, encoding="utf-8")
    proc = subprocess.run(["node", str(driver_path)], capture_output=True, text=True, timeout=120)
    if proc.returncode != 0:
        return {"error": (proc.stderr or "").strip()[-1200:]}
    lines = (proc.stdout or "").strip().splitlines()
    if not lines:
        return {"error": "the search driver said nothing"}
    return json.loads(lines[-1])


_CAMLED_BENCH_DRIVER = r"""
"use strict";
const fs = require("fs"), vm = require("vm");
let source = fs.readFileSync(process.argv[2], "utf8").replace(/@@NS@@/g, "");
const plantIt = process.argv[3] === "1";
const PLANT_FROM = "if (camLed(s)) {";
const PLANT_TO = "if (false) {";
if (plantIt) {
  if (source.indexOf(PLANT_FROM) < 0) { console.log(JSON.stringify({missed: true})); process.exit(0); }
  source = source.split(PLANT_FROM).join(PLANT_TO);
}
let host = null;
const sandbox = { window: { devicePixelRatio: 1, innerWidth: 390, innerHeight: 844,
                            __Pass: {}, __PassLayer: (h) => { host = h; } },
                  performance: { now: () => 0 }, console: console, document: undefined };
sandbox.window.performance = sandbox.performance;
vm.createContext(sandbox);
try {
  vm.runInContext(source, sandbox, { filename: "pass-layer.js" });
} catch (e) {
  console.log(JSON.stringify({ error: String((e && e.stack) || e) }));
  process.exit(0);
}
const bench = sandbox.window.__Pass.bench;
if (!bench || typeof bench.scoreWhyNo !== "function") {
  console.log(JSON.stringify({ error: "the built host published no scoreWhyNo" }));
  process.exit(0);
}
const score = JSON.parse(process.argv[4]);
const baseline = bench.scoreWhyNo(score);
const collided = JSON.parse(JSON.stringify(score));
collided.cues[0].levels = (collided.cues[0].levels || []).concat(["WORLD"]);
const collision = bench.scoreWhyNo(collided);
console.log(JSON.stringify({ baseline: baseline, collision: collision, collidedCueId: collided.cues[0].id }));
"""


def _camled_bench_run(plant_it):
    tmp_dir = Path(tempfile.mkdtemp(prefix="pass_layer_camled_bench_"))
    driver_path = tmp_dir / "bench.js"
    driver_path.write_text(_CAMLED_BENCH_DRIVER, encoding="utf-8")
    proc = subprocess.run(["node", str(driver_path), str(LAYER_PATH), "1" if plant_it else "0",
                           json.dumps(_camled_score)],
                          capture_output=True, text=True, timeout=60)
    if proc.returncode != 0:
        return {"error": (proc.stderr or "").strip()[-1200:]}
    lines = (proc.stdout or "").strip().splitlines()
    if not lines:
        return {"error": "the bench driver said nothing"}
    return json.loads(lines[-1])


if not _camled_node_available():
    skip(_CAMLED_ROW, "node is not on this machine")
    skip(_CAMLED_RED_ROW, "node is not on this machine")
elif not (_CAMLED_COMPOSER.exists() and _CAMLED_FIXTURE_COMPOSED.exists()
          and _CAMLED_FIXTURE_WORKS.exists() and LAYER_PATH.exists()):
    skip(_CAMLED_ROW, "the composer, the host, or the real fixtures are not on this machine")
    skip(_CAMLED_RED_ROW, "no real led score to replant against")
else:
    _camled_found = _camled_search().get("found")
    if not isinstance(_camled_found, dict):
        skip(_CAMLED_ROW, "the real 121-work fleet's own search cast no camera-led score at all")
        skip(_CAMLED_RED_ROW, "no real led score found above to replant")
    else:
        _camled_score = _camled_found["score"]
        _camled_green = _camled_bench_run(plant_it=False)
        _base_ok = _camled_green.get("baseline") is None
        _collision_why = _camled_green.get("collision")
        _collision_ok = (isinstance(_collision_why, str)
                         and "world level" in _collision_why
                         and ("«" + _camled_green.get("collidedCueId", "") + "»") in _collision_why)
        check(_CAMLED_ROW,
              _base_ok and _collision_ok,
              "real led pair %s→%s (seed %s, role %s): the planner's own real score casts %s "
              "(cameraAuthority aside, levels=%s); scoreWhyNo reads it as-composed as %s, and with "
              "WORLD added onto that same real cue's own levels reads %s"
              % (_camled_found["from"], _camled_found["to"], _camled_found["seed"],
                 _camled_found["role"], [c["instrument"]["id"] for c in _camled_score["cues"]],
                 [c["levels"] for c in _camled_score["cues"]], json.dumps(_camled_green.get("baseline")),
                 json.dumps(_collision_why)))

        _camled_red = _camled_bench_run(plant_it=True)
        if _camled_red.get("missed"):
            skip(_CAMLED_RED_ROW, "the line this plant names is not in the shipped source")
        else:
            check(_CAMLED_RED_ROW,
                  _camled_red.get("collision") is None,
                  "" if _camled_red.get("collision") is None else
                  "even with the camLed branch disabled, the same real collision still reads: "
                  + json.dumps(_camled_red.get("collision")))


# ---------------------------------------------------------------- extracting the real shader source
def parse_concat_string(text, start_idx):
    """`text[start_idx:]` holds `"…" (+ "…")* ;` — the JS-source shape `VERT`/`FRAG` are written in
    throughout this file's instruments. Returns the decoded string and the index just past the `;`.
    A scanner rather than a pattern, so it reads exactly what the file's own `+` chain builds,
    including every `\\n` the shipped shader carries — never a hand-retyped copy of the GLSL."""
    i, n = start_idx, len(text)
    parts = []
    while i < n:
        while i < n and text[i] in " \t\r\n+":
            i += 1
        if i < n and text[i] == ";":
            i += 1
            break
        if i >= n or text[i] not in "\"'":
            raise ValueError("parse_concat_string: unexpected char at %d: %r" % (i, text[i:i + 20]))
        q = text[i]
        i += 1
        buf = []
        while i < n and text[i] != q:
            if text[i] == "\\":
                buf.append(text[i:i + 2])
                i += 2
                continue
            buf.append(text[i])
            i += 1
        i += 1
        parts.append("".join(buf))
    raw = "".join(parts)
    return json.loads('"' + raw + '"'), i


def extract_shader(text, var_name, after_idx=0):
    marker = "var %s = " % var_name
    idx = text.index(marker, after_idx)
    return parse_concat_string(text, idx + len(marker))


FN_IDX = SOURCE_TEXT.index("function makeLastResortInstrument()")
VERT_SRC, _after_vert = extract_shader(SOURCE_TEXT, "VERT", FN_IDX)
FRAG_SRC, _after_frag = extract_shader(SOURCE_TEXT, "FRAG", _after_vert)


def extract_function(text, name, after_idx=0):
    """Balanced-brace extraction of `function NAME(...) { ... }` — the REAL, current body, never a
    hand-copied string, the same principle `extract_shader` already carries for the shader text."""
    marker = "function %s(" % name
    idx = text.index(marker, after_idx)
    brace = text.index("{", idx)
    depth, i = 0, brace
    while i < len(text):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[idx:i + 1]
        i += 1
    raise ValueError("unbalanced braces for function %s" % name)


# THE ADDRESS, PROVED BY EXECUTION RATHER THAN BY GREP. `LAST_RESORT_NAME` is not decorative: two
# outside callers hardcode the literal "@host/last-resort" when they ask the registry for this
# instrument by id (engine/client/01a-pass.js and engine/assets/exhibition.js's "reduced-floor"
# cue, and this same file's own `lastResortCastInstrument`, all keyed on the constant). A grep for
# the string proves the text sits somewhere in the file; it does not prove the constant is what the
# RETURNED object's own `name` actually carries at runtime. So this runs the real, current
# `makeLastResortInstrument` in a real JS context and reads the object it actually returns.
NAME_DECL_IDX = SOURCE_TEXT.index("var LAST_RESORT_NAME")
NAME_DECL_END = SOURCE_TEXT.index(";", NAME_DECL_IDX) + 1
NAME_DECL = SOURCE_TEXT[NAME_DECL_IDX:NAME_DECL_END]
FIT_SRC = extract_function(SOURCE_TEXT, "fitCoverSpan")
MAKE_SRC = extract_function(SOURCE_TEXT, "makeLastResortInstrument", FN_IDX)


def last_resort_identity(name_decl):
    """Executes the real, current `makeLastResortInstrument` — built from `name_decl` (the constant
    declaration, real or mutated in memory) plus the shipped `fitCoverSpan` and the shipped function
    body itself — and reads back the returned instrument's own `name` and drawing program."""
    page = ("<!doctype html><html><head><meta charset=\"utf-8\"></head><body><script>\n"
            + name_decl + "\n" + FIT_SRC + "\n" + MAKE_SRC + "\n"
            + "window.__lastResort = function () {\n"
            + "  var inst = makeLastResortInstrument();\n"
            + "  return { name: inst.name, program: (inst.manifest.passes[0] || {}).program };\n"
            + "};\nwindow.__benchReady = true;\n</script></body></html>")
    d = Path(tempfile.mkdtemp(prefix="pass_layer_identity_"))
    (d / "index.html").write_text(page, encoding="utf-8")
    try:
        with serve(str(d)) as base, Browser() as br:
            br.navigate(base + "/")
            for _ in range(25):
                if br.evaluate("String(!!window.__benchReady)") == "true":
                    break
                br.sleep(0.1)
            return json.loads(br.evaluate("JSON.stringify(window.__lastResort())")), None
    except Exception as e:  # noqa: BLE001 — reported on the row that wants it
        return None, str(e)
    finally:
        shutil.rmtree(d, ignore_errors=True)


if not chrome_available():
    skip("PASS-LAYER the built-in answers to the exact address its outside callers hardcode",
         "no headless Chrome on this machine — EXPECTED, pinned skip, never a silent pass")
    skip("PASS-LAYER renaming the address in memory makes it invisible to those same callers",
         "no headless Chrome on this machine — EXPECTED, pinned skip, never a silent pass")
else:
    identity, ierr = last_resort_identity(NAME_DECL)
    if identity is None:
        check("PASS-LAYER the built-in answers to the exact address its outside callers hardcode",
              False, "the identity bench never ran: %s" % ierr)
    else:
        check("PASS-LAYER the built-in answers to the exact address its outside callers hardcode",
              identity.get("name") == "@host/last-resort"
              and identity.get("program") == "host-last-resort-wipe",
              "executing the REAL, current `makeLastResortInstrument` returns name=%r, "
              "manifest.passes[0].program=%r — the literal `@host/last-resort` is what "
              "engine/client/01a-pass.js's `reduced-floor` cue, engine/assets/exhibition.js and "
              "this file's own `lastResortCastInstrument` all hardcode when they ask the registry "
              "for this instrument by id" % (identity.get("name"), identity.get("program")))

    MUT_NAME_DECL = NAME_DECL.replace("@host/last-resort", "@host/renamed-resort", 1)
    if MUT_NAME_DECL == NAME_DECL:
        check("PASS-LAYER renaming the address in memory makes it invisible to those same callers",
              False, "the constant's own text was not found verbatim, so the mutant could not be "
                     "built off the shipped source")
    else:
        mut_identity, merr = last_resort_identity(MUT_NAME_DECL)
        if mut_identity is None:
            check("PASS-LAYER renaming the address in memory makes it invisible to those same callers",
                  False, "the mutant identity bench never ran: %s" % merr)
        else:
            check("PASS-LAYER renaming the address in memory makes it invisible to those same callers",
                  mut_identity.get("name") != "@host/last-resort",
                  "with `LAST_RESORT_NAME` mutated to \"@host/renamed-resort\" in memory, the same "
                  "execution returns name=%r — the outside callers above, which hardcode the "
                  "literal \"@host/last-resort\", would find no instrument registered there at all"
                  % mut_identity.get("name"))

check("PASS-LAYER no boundary in the shipped shader is drawn from the frame's own coordinate",
      "vUV.x" not in FRAG_SRC and "vUV.y" not in FRAG_SRC,
      "the extracted, currently-shipped FRAG source names neither component of `vUV` on its own — "
      "`vUV` appears only inside `coverUV(vUV, …)`, a texture-sampling address, never compared "
      "against `uReveal`")

check("PASS-LAYER the boundary is built from both textures' own sampled content",
      re.search(r"lumA\s*=\s*dot\(a,", FRAG_SRC) is not None
      and re.search(r"lumB\s*=\s*dot\(b,", FRAG_SRC) is not None
      and "smoothstep(uReveal - 0.08, uReveal + 0.08, field)" in FRAG_SRC,
      "`lumA`/`lumB` are read off `a`/`b`, the texels `uTexA`/`uTexB` were just sampled at, and "
      "`field` (not `vUV.x`) is what `uReveal` is compared against")

# The third count of the wipe's own three-part test — "IT READS AS A DISSOLVE LED BY THE PICTURES,
# NEVER AN EDGE TRAVELLING THE FRAME" — is proved below, once the real and reverted renders both
# exist, by a measurement neither a comment nor a grep can stand in for: see
# "PASS-LAYER the boundary the pair draws is not the straight line two linear photographs alone can
# make", after the red-on-bug revert. The other two counts are proved above: no frame coordinate
# feeds the boundary, and both `lumA` and `lumB` feed `field` before `uReveal` is ever read.

# ---------------------------------------------------------------- the behavioural bench
W = H = 64
REVEAL = 0.5
HALF = 0.08


def _grad_rgba(top, bottom):
    """W×H RGBA bytes, R=G=B constant across a row and ramping `top → bottom` down the rows, alpha
    255 throughout — content that varies by row and by row alone, so any column-wise variation the
    rendered frame shows can only have come from the boundary, never from either texture's own
    content."""
    out = bytearray(W * H * 4)
    for row in range(H):
        v = round(top + (bottom - top) * (row / (H - 1)))
        for col in range(W):
            o = (row * W + col) * 4
            out[o] = out[o + 1] = out[o + 2] = v
            out[o + 3] = 255
    return bytes(out)


TEX_A = _grad_rgba(0, 255)     # black at the top row, white at the bottom
TEX_B = _grad_rgba(255, 0)     # the mirror: white at the top row, black at the bottom

PAGE = """<!doctype html><html><head><meta charset="utf-8"></head><body>
<canvas id="c" width="%(w)d" height="%(h)d"></canvas>
<script>
function b64ToBytes(b64) {
  var bin = atob(b64), out = new Uint8Array(bin.length);
  for (var i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
  return out;
}
function makeTex(gl, bytes) {
  var t = gl.createTexture();
  gl.bindTexture(gl.TEXTURE_2D, t);
  gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, %(w)d, %(h)d, 0, gl.RGBA, gl.UNSIGNED_BYTE, bytes);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.NEAREST);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
  return t;
}
window.__runLastResort = function (vertSrc, fragSrc, aB64, bB64, reveal) {
  try {
    var canvas = document.getElementById("c");
    var gl = canvas.getContext("webgl") || canvas.getContext("experimental-webgl");
    if (!gl) return { error: "no webgl" };
    var vs = gl.createShader(gl.VERTEX_SHADER);
    gl.shaderSource(vs, vertSrc); gl.compileShader(vs);
    if (!gl.getShaderParameter(vs, gl.COMPILE_STATUS)) return { error: "vert: " + gl.getShaderInfoLog(vs) };
    var fs = gl.createShader(gl.FRAGMENT_SHADER);
    gl.shaderSource(fs, fragSrc); gl.compileShader(fs);
    if (!gl.getShaderParameter(fs, gl.COMPILE_STATUS)) return { error: "frag: " + gl.getShaderInfoLog(fs) };
    var prog = gl.createProgram();
    gl.attachShader(prog, vs); gl.attachShader(prog, fs); gl.linkProgram(prog);
    if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) return { error: "link: " + gl.getProgramInfoLog(prog) };
    gl.useProgram(prog);
    var quad = new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]);
    var buf = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, buf);
    gl.bufferData(gl.ARRAY_BUFFER, quad, gl.STATIC_DRAW);
    var loc = gl.getAttribLocation(prog, "aPos");
    gl.enableVertexAttribArray(loc);
    gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
    var texA = makeTex(gl, b64ToBytes(aB64));
    var texB = makeTex(gl, b64ToBytes(bB64));
    gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, texA);
    gl.activeTexture(gl.TEXTURE1); gl.bindTexture(gl.TEXTURE_2D, texB);
    gl.uniform1i(gl.getUniformLocation(prog, "uTexA"), 0);
    gl.uniform1i(gl.getUniformLocation(prog, "uTexB"), 1);
    gl.uniform4f(gl.getUniformLocation(prog, "uFitA"), 1, 1, 0, 0);
    gl.uniform4f(gl.getUniformLocation(prog, "uFitB"), 1, 1, 0, 0);
    gl.uniform1f(gl.getUniformLocation(prog, "uReveal"), reveal);
    gl.viewport(0, 0, %(w)d, %(h)d);
    gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
    var px = new Uint8Array(%(w)d * %(h)d * 4);
    gl.readPixels(0, 0, %(w)d, %(h)d, gl.RGBA, gl.UNSIGNED_BYTE, px);
    return { pixels: Array.prototype.slice.call(px) };
  } catch (e) {
    return { error: String(e) };
  }
};
window.__benchReady = true;
</script>
</body></html>""" % {"w": W, "h": H}


def render(vert_src, frag_src, tex_a, tex_b, reveal):
    """Runs the given VERT/FRAG pair in a real headless-Chrome WebGL context against the two fixed
    synthetic textures and returns the WxH RGBA framebuffer as a flat list of ints, or None with a
    detail string on failure."""
    import base64
    d = Path(tempfile.mkdtemp(prefix="pass_layer_bench_"))
    (d / "index.html").write_text(PAGE, encoding="utf-8")
    a_b64 = base64.b64encode(tex_a).decode("ascii")
    b_b64 = base64.b64encode(tex_b).decode("ascii")
    with serve(str(d)) as base, Browser() as br:
        br.navigate(base + "/")
        for _ in range(25):
            if br.evaluate("String(!!window.__benchReady)") == "true":
                break
            br.sleep(0.1)
        out = json.loads(br.evaluate(
            "JSON.stringify(window.__runLastResort(%s, %s, %s, %s, %s))"
            % (json.dumps(vert_src), json.dumps(frag_src), json.dumps(a_b64), json.dumps(b_b64),
               json.dumps(reveal))
        ))
    if "error" in out:
        return None, out["error"]
    return out["pixels"], None


def max_row_spread(pixels):
    """The largest, over every row, of (max R − min R) across that row's columns — R alone, since
    both synthetic textures are achromatic (R=G=B). Near zero means the mix at a row never depended
    on which column was asked; a real number means some column-wise force pushed pixels apart even
    though neither texture varies across a row at all."""
    worst = 0
    for row in range(H):
        lo, hi = 255, 0
        for col in range(W):
            r = pixels[(row * W + col) * 4]
            lo = min(lo, r)
            hi = max(hi, r)
        worst = max(worst, hi - lo)
    return worst


if not chrome_available():
    skip("PASS-LAYER the reveal answers the pair's own measured content, not the frame's column",
         "no headless Chrome on this machine — EXPECTED, pinned skip, never a silent pass")
    skip("PASS-LAYER reverting the fix back to `vUV.x` reddens the same measurement",
         "no headless Chrome on this machine — EXPECTED, pinned skip, never a silent pass")
    skip("PASS-LAYER the boundary the pair draws is not the straight line two linear photographs "
         "alone can make",
         "no headless Chrome on this machine — EXPECTED, pinned skip, never a silent pass")
else:
    hurt_pixels = None
    pixels, err = render(VERT_SRC, FRAG_SRC, TEX_A, TEX_B, REVEAL)
    if pixels is None:
        check("PASS-LAYER the reveal answers the pair's own measured content, not the frame's column",
              False, "the bench never rendered: %s" % err)
    else:
        spread = max_row_spread(pixels)
        check("PASS-LAYER the reveal answers the pair's own measured content, not the frame's column",
              spread <= 4,
              "two textures whose content varies only by row (never by column) were mixed at "
              "uReveal=%.2f; the worst row's own column-to-column spread is %d of 255 — a boundary "
              "built from `field` (the pair's own sampled luminance) cannot invent a column-wise "
              "difference where neither photograph carries one" % (REVEAL, spread))

    # THE RED-ON-BUG PROOF: the shipped shader's own text, mutated in memory back to the banned form,
    # must make this exact measurement fail — otherwise the green above is a text coincidence rather
    # than a behavioural gate. The tree on disk is never touched.
    NEW_TAIL = ("  float lumA = dot(a, vec3(0.2126, 0.7152, 0.0722));\n"
                "  float lumB = dot(b, vec3(0.2126, 0.7152, 0.0722));\n"
                "  float field = 0.5 * (lumA + (1.0 - lumB));\n"
                "  float w = smoothstep(uReveal - 0.08, uReveal + 0.08, field);\n")
    OLD_TAIL = "  float w = smoothstep(uReveal - 0.08, uReveal + 0.08, vUV.x);\n"
    if NEW_TAIL not in FRAG_SRC:
        check("PASS-LAYER reverting the fix back to `vUV.x` reddens the same measurement",
              False, "the fixed form was not found verbatim in the extracted shader, so the mutant "
                     "could not be built off the shipped text")
    else:
        HURT_FRAG = FRAG_SRC.replace(NEW_TAIL, OLD_TAIL, 1)
        hurt_pixels, hurt_err = render(VERT_SRC, HURT_FRAG, TEX_A, TEX_B, REVEAL)
        if hurt_pixels is None:
            check("PASS-LAYER reverting the fix back to `vUV.x` reddens the same measurement",
                  False, "the mutant bench never rendered: %s" % hurt_err)
        else:
            hurt_spread = max_row_spread(hurt_pixels)
            check("PASS-LAYER reverting the fix back to `vUV.x` reddens the same measurement",
                  hurt_spread > 60,
                  "the same two row-only textures, the same uReveal=%.2f, with `field` replaced by "
                  "`vUV.x` in memory: the worst row's column-to-column spread jumps to %d of 255 — "
                  "a hard left-to-right wipe appears inside a row that carries no column variation "
                  "of its own, which is the defect class shelf 18 bans and the row above proves gone"
                  % (REVEAL, hurt_spread))

    # THE DISSOLVE CLAIM, THE WIPE'S THIRD COUNT: "it reads as a dissolve led by the pictures, never
    # an edge travelling the frame." Column 0 of the two renders above already carries one pixel per
    # source row (row-only content, proved column-invariant above), so its row profile IS the shape
    # the boundary drew. A boundary built from a fixed weight over two LINEAR gradients (what
    # `vUV.x` reduces mixing to, once the column itself is held fixed) can only ever produce another
    # straight line down that column — no single weight bends two lines into a curve. A boundary that
    # is a level set of the pair's own measured field is under no such constraint.
    def line_residual(profile):
        n = len(profile)
        xs = list(range(n))
        mean_x = sum(xs) / n
        mean_y = sum(profile) / n
        sxx = sum((x - mean_x) ** 2 for x in xs)
        sxy = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, profile))
        slope = sxy / sxx if sxx else 0.0
        intercept = mean_y - slope * mean_x
        return (sum((y - (slope * x + intercept)) ** 2 for x, y in zip(xs, profile)) / n) ** 0.5

    if pixels is None or hurt_pixels is None:
        check("PASS-LAYER the boundary the pair draws is not the straight line two linear "
              "photographs alone can make",
              False, "one of the two renders above never ran, so no profile could be compared")
    else:
        profile_real = [pixels[(row * W + 0) * 4] for row in range(H)]
        profile_mut = [hurt_pixels[(row * W + 0) * 4] for row in range(H)]
        resid_real = line_residual(profile_real)
        resid_mut = line_residual(profile_mut)
        check("PASS-LAYER the boundary the pair draws is not the straight line two linear "
              "photographs alone can make",
              resid_real > 15 and resid_mut < 5,
              "down column 0, row by row: the real boundary's own profile departs from its best-fit "
              "straight line by %.1f of 255 (an S-curve, because `field` crosses `uReveal` "
              "part-way down and bends the mix there); with `field` replaced by `vUV.x` the same "
              "column — now mixed at one fixed weight over the same two linear gradients — departs "
              "from a straight line by only %.1f of 255, which is what a level set of the pair's "
              "own content can do that a frame coordinate cannot"
              % (resid_real, resid_mut))

passed = sum(1 for _, s, _ in results if s == "PASS")
failed = sum(1 for _, s, _ in results if s == "FAIL")
skipped = sum(1 for _, s, _ in results if s == "SKIP")
print()
for name, status, detail in results:
    line = "%s  %s" % (status, name)
    if detail:
        line += "   — %s" % detail
    print(line)
print("\n%d passed / %d failed / %d skipped" % (passed, failed, skipped))
sys.exit(1 if failed else 0)
