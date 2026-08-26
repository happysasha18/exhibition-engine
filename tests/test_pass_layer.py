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

check("PASS-LAYER the last-resort shader still exists at the address the naryad names",
      "LAST_RESORT_NAME = \"@host/last-resort\"" in SOURCE_TEXT
      and "host-last-resort-wipe" in SOURCE_TEXT,
      "engine/assets/pass-layer.js carries `makeLastResortInstrument`, registered under "
      "`@host/last-resort` and drawing program `host-last-resort-wipe`")

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

check("PASS-LAYER the file answers the wipe's own three-part test on all three counts",
      "THE THREE-PART TEST, ANSWERED ON ALL" in SOURCE_TEXT
      and "THE BOUNDARY IS A LEVEL SET OF WHAT THE TWO PHOTOGRAPHS THEMSELVES CARRY" in SOURCE_TEXT
      and "THE TWO IMAGES INTERACT AT EVERY FRAGMENT" in SOURCE_TEXT
      and "IT READS AS A DISSOLVE LED BY THE PICTURES" in SOURCE_TEXT,
      "the charter's ban list convicts a wipe only where all three counts convict, and a boundary "
      "that travels across a frame has to answer that test out loud, the way pass-inst-tunnel.js "
      "does for its own ring")

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
else:
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
