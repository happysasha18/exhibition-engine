/*!darkroom-measure.js*/
// Browser port of three analysers from tlvphotos/lab/analyze/recipes.py: busyness (:653),
// edge_map (:591-594, a 3x3 Sobel) and best_axis (:100-125) with chance_diff (:64-79) and
// mirror_corr (:85-98) beside it. Pure arithmetic over an ImageData-shaped {width, height, data}
// object — no canvas work here; a later unit calls getImageData and hands the prepared frame in.
//
// Not ported: the frame preparation at recipes.py:600-606 (decode, to_gray, normalise, the
// SMALL resize) and find_centre — both need a decoder this file does not have and does not need.
//
// chance_diff samples 20000 random pixel pairs from a seeded numpy Generator; matching that
// bit-for-bit would mean re-implementing PCG64 for no gain (the seed only makes recipes.py's own
// approximation reproducible, not exact). Its target is the true population mean absolute
// difference between two pixels of the frame — chance_diff's random sample is already just an
// estimate of that number — so this port computes it exactly via the standard closed form
// (sort ascending, MD = 2/n^2 * sum((2*i - n - 1) * x[i])) instead of drawing a sample. Measured
// against recipes.py's own sampled answer on real frames, the gap is under 1 unit on a 0..255
// scale (tests/test_darkroom_measure.py TOL_CHANCE) — the sampling noise recipes.py's own
// approximation already carries.

function clampIndex(v, n) {
  return v < 0 ? 0 : (v >= n ? n - 1 : v);
}

// One 1-D pass of the [-1, 0, 1] derivative kernel, boundary-clamped (scipy's default "reflect"
// mode duplicates the edge pixel for a 3-tap kernel, same as clamping).
function sobelDerivative(data, w, h, axis) {
  var out = new Float64Array(w * h);
  if (axis === "x") {
    for (var y = 0; y < h; y++) {
      var row = y * w;
      for (var x = 0; x < w; x++) {
        out[row + x] = data[row + clampIndex(x + 1, w)] - data[row + clampIndex(x - 1, w)];
      }
    }
  } else {
    for (var y2 = 0; y2 < h; y2++) {
      var yp = clampIndex(y2 + 1, h) * w, ym = clampIndex(y2 - 1, h) * w, row2 = y2 * w;
      for (var x2 = 0; x2 < w; x2++) {
        out[row2 + x2] = data[yp + x2] - data[ym + x2];
      }
    }
  }
  return out;
}

// One 1-D pass of the [1, 2, 1] smoothing kernel, same boundary handling.
function sobelSmooth(data, w, h, axis) {
  var out = new Float64Array(w * h);
  if (axis === "x") {
    for (var y = 0; y < h; y++) {
      var row = y * w;
      for (var x = 0; x < w; x++) {
        out[row + x] = data[row + clampIndex(x - 1, w)] + 2 * data[row + x]
          + data[row + clampIndex(x + 1, w)];
      }
    }
  } else {
    for (var y2 = 0; y2 < h; y2++) {
      var yp = clampIndex(y2 + 1, h) * w, ym = clampIndex(y2 - 1, h) * w, row2 = y2 * w;
      for (var x2 = 0; x2 < w; x2++) {
        out[row2 + x2] = data[ym + x2] + 2 * data[row2 + x2] + data[yp + x2];
      }
    }
  }
  return out;
}

// recipes.py:591-594 — gx = sobel(g, axis=1)/4, gy = sobel(g, axis=0)/4, edge = hypot(gx, gy).
// scipy's sobel(axis=1) is derivative-in-x then smooth-in-y; sobel(axis=0) is derivative-in-y
// then smooth-in-x — the two passes each direction takes.
function edgeMap(frame) {
  var w = frame.width, h = frame.height, data = frame.data;
  var gx = sobelSmooth(sobelDerivative(data, w, h, "x"), w, h, "y");
  var gy = sobelSmooth(sobelDerivative(data, w, h, "y"), w, h, "x");
  var out = new Float64Array(w * h);
  for (var i = 0; i < out.length; i++) {
    var a = gx[i] / 4.0, b = gy[i] / 4.0;
    out[i] = Math.sqrt(a * a + b * b);
  }
  return { width: w, height: h, data: out };
}

// recipes.py:653 — busy = float((edge > 28.0).mean()); threshold quoted from that line.
function busyness(frame) {
  var edge = edgeMap(frame).data;
  var count = 0;
  for (var i = 0; i < edge.length; i++) {
    if (edge[i] > 28.0) count++;
  }
  return count / edge.length;
}

// recipes.py:64-79 — see the file header note on the exact-vs-sampled gap this closes.
function chanceDiff(frame) {
  var x = Array.prototype.slice.call(frame.data).sort(function (a, b) { return a - b; });
  var n = x.length;
  var sum = 0;
  for (var i = 0; i < n; i++) {
    sum += (2 * (i + 1) - n - 1) * x[i];
  }
  return (2.0 / (n * n)) * sum;
}

// recipes.py:85-98 — Pearson correlation between two same-length regions.
function mirrorCorr(a, b) {
  var n = a.length;
  var ma = 0, mb = 0;
  for (var i = 0; i < n; i++) { ma += a[i]; mb += b[i]; }
  ma /= n; mb /= n;
  var saa = 0, sbb = 0, sab = 0;
  for (var i = 0; i < n; i++) {
    var da = a[i] - ma, db = b[i] - mb;
    saa += da * da; sbb += db * db; sab += da * db;
  }
  var d = Math.sqrt(saa * sbb);
  if (d < 1e-9) return 0.0;
  var v = sab / d;
  return v < -1 ? -1 : (v > 1 ? 1 : v);
}

// recipes.py:100-125 — best mirror axis position along `axis` (0 = rows, 1 = cols). `base` is
// the chance-mismatch charge for pixels with no fold partner (recipes.py passes chance_diff(g)).
function bestAxis(frame, axis, base, lo, hi, step) {
  lo = lo === undefined ? 0.30 : lo;
  hi = hi === undefined ? 0.70 : hi;
  step = step === undefined ? 1 : step;
  var w = frame.width, h = frame.height, data = frame.data;
  var H, W, G;
  if (axis === 1) {
    H = h; W = w; G = data;   // already row-major H x W, row stride W
  } else {
    H = w; W = h;
    G = new Float64Array(H * W);
    for (var y = 0; y < h; y++) {           // transpose once: G[i,j] = g[j,i]
      for (var x = 0; x < w; x++) {
        G[x * W + y] = data[y * w + x];
      }
    }
  }
  var total = H * W;
  var bestScore = -1.0, bestPos = 0.5;
  var cLo = Math.floor(lo * W), cHi = Math.floor(hi * W);
  for (var c = cLo; c <= cHi; c += step) {
    var m = Math.min(c, W - c);
    if (m < 8) continue;
    var cost = 0;
    for (var i = 0; i < H; i++) {
      var rowBase = i * W;
      for (var k = 0; k < m; k++) {
        cost += Math.abs(G[rowBase + c - m + k] - G[rowBase + c + m - 1 - k]);
      }
    }
    var nCov = 2 * m * H;
    cost += (total - nCov) * base;
    var s = 1.0 - cost / (total * 255.0);
    if (s > bestScore) { bestScore = s; bestPos = c / W; }
  }
  return { score: bestScore, position: bestPos };
}
