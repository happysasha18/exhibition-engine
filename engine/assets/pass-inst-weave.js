/*!pass-inst-weave.js*/
// One instrument, travelling as its own file (PASS-API-V1 §7/§8, his word of 2026-08-14 08:39: the
// engine knows no effect name and loads version-pinned opaque effect files).
//
// WHAT THIS FILE IS. One instrument and the mathematics it draws by: a name, a manifest declaring
// its passes, its uniforms with the source each is bound from, its handles and its doors, and the
// pure functions that answer the numbers of one frame. The manifest's declared names are the whole
// interface — the host binds by them and refuses at registration anything it cannot supply.
//
// WHAT THIS FILE MAY NOT DO. It reads no wall clock, holds no listener, creates no WebGL context,
// loads no picture and touches no DOM (§1.2's fence). The host owns the canvas, the context, the
// frame loop, the clock, the camera and the transaction; the instrument owns the picture.
//
// HOW IT REACHES THE HOST, AND WHY IT TRAVELS ALONE. The site's own settings record gives every
// instrument an address, a version and a digest, keyed by the instrument's own name. A score's cue
// names an instrument; the host looks that name up in the record and fetches that one file, weighs
// its bytes against the digest it was told, evaluates the bytes it weighed, and reads the record
// handed to the join function below. A version or a digest that fails to match is refused with its
// reason and the walk's own glide runs.
//
// One file for the whole farm would make a visit pay for twenty-five instruments to see one
// crossing, and it would make one byte fence answer for a number nobody can act on. One file per
// instrument makes the fence the honest unit — one instrument, one number — and makes a visit pay
// for the passage it is actually walking.
//
// OWNERSHIP. This instrument was carried over from lab/effects/. The artistic instruments and their
// manifests belong to tlvphotos, which builds these files from its own sources; the engine's copies
// are what ships until that handover lands. The contract this file answers to is §7 and §8 of
// docs/design/PASS-API-V1.md, and the record that names it is the site's own `pass` block.
(function () {
  var join = window.__@@NS@@PassInstrument;
  if (typeof join !== "function") return;

  // THIS FILE'S OWN VERSION, and the one home of that fact. The build reads this literal out of the
  // source and writes it into the site's record beside the digest, so the version a file declares
  // and the version a host was told to load cannot drift apart without the build noticing.
  var INSTRUMENT_VERSION = "1.0.0";

  // ================================================================================================
  // THE WOVEN INSTRUMENT (§8) — lab/effects/weave.js carried across
  // ================================================================================================
  // What came over: the shader, the seating of a work in the frame (coverFit), the response curve
  // (feelOf), the turn of the weave (rotForTime) and the numbers of one frame (frameValuesOf). Not
  // one number changed; this is the same mathematics, standing on the host's frame.
  //
  // What stayed behind: its own canvas, its own WebGL 1 context, its own frame loop, its pointer and
  // resize listeners, its 2D fallback and its own clock. The instrument here reads no wall clock,
  // holds no listener, creates no context and loads no picture (§1.2's fence).
  function weaveInstrument() {
    var VERT = [
      "attribute vec2 aPos;",
      "varying vec2 vUv;",
      "void main(){ vUv = vec2(aPos.x * 0.5 + 0.5, 0.5 - aPos.y * 0.5); gl_Position = vec4(aPos, 0.0, 1.0); }",
    ].join("\n");

    var FRAG = [
      "precision highp float;",
      "varying vec2 vUv;",
      "uniform sampler2D uA;",
      "uniform sampler2D uB;",
      "uniform vec4 uFitA;",
      "uniform vec4 uFitB;",
      "uniform vec2 uRes;",
      "uniform float uT;",
      "uniform float uNv;",
      "uniform float uDuty;",
      "uniform float uAmp;",
      "uniform float uRot;",
      "uniform float uSpeed;",
      "uniform float uSeed;",
      // THE WAVE THE WORK ITSELF CARRIES: its depth in cells, its own spatial frequency along the
      // ribbon in cycles across the frame side it runs on, and how fast it travels in cycles a
      // second. All three are handles a score drives from the photograph's own measured structure,
      // and all three are nothing for a work that carries no wave.
      "uniform vec4 uWave;",
      // HOW FAR UNDER A DIPPING RIBBON LIES, read as a coarser copy of the picture rather than only
      // as a darker one. Depth was drawn here as shade alone, so in a basket the ribbon passing
      // UNDER a crossing one came out exactly as sharp as the one on top — and two equally sharp
      // pieces side by side read as tiles laid next to each other rather than as cloth, which is
      // the one stretch of this instrument a photographed round called blocky. A thing further from
      // the eye is also softer, so the dip now carries a level of the picture's own chain as well.
      // At nothing the level is exactly 0 at every point and the frame is the one drawn before.
      "uniform float uDepth;",
      "const float TAU = 6.28318530718;",
      // How many levels of the picture's own chain a full dip reads down by. Two levels is a
      // quarter of the resolution, which at this instrument's band widths is the softness of a
      // thing one ribbon's thickness further away rather than a blur.
      "const float DEPTH_LOD = 2.0;",
      // THE WAVE'S OWN SHAPE, and the one part of it that is not read from the work. A single sine
      // is a corrugation and reads as a stock effect; the wave carries an overtone, and the two are
      // incommensurate so the irregularity never settles into a repeating figure — the rubato law's
      // third instrument, spent once here and nowhere else on this lattice. Two thirds of the depth
      // stands in the fundamental and one third in the overtone, the overtone runs at 1.8235 of the
      // fundamental and drifts at 0.6889 of its rate the other way. These four are the proportions
      // of the wave lab/effects/weave.js drew at 32a013a, kept as SHAPE while its size, its period
      // and its speed became the work's own reading.
      "const float WLOW = 0.66666667;",
      "const float WHIGH = 0.33333333;",
      "const float WOVER = 1.82352941;",
      "const float WBEAT = 0.68888889;",
      "vec2 into(vec2 p, vec4 f){",
      "  return clamp((p - 0.5) * f.xy + 0.5 + f.zw, 0.0008, 0.9992);",
      "}",
      "vec3 texA(vec2 p){ return texture2D(uA, into(p, uFitA)).rgb; }",
      "vec3 texB(vec2 p){ return texture2D(uB, into(p, uFitB)).rgb; }",
      // The same two readings, at a named level of the picture's own chain. The host uploads that
      // chain and filters between its levels, so a fractional level is a real reading and not a
      // step. Level 0 is the sharpest copy, which is what `texA`/`texB` above always answer.
      "vec3 texAd(vec2 p, float l){ return textureLod(uA, into(p, uFitA), l).rgb; }",
      "vec3 texBd(vec2 p, float l){ return textureLod(uB, into(p, uFitB), l).rgb; }",
      "float sqI(float t, float d){ return floor(t) * d + min(fract(t), d); }",
      "float sqcov(float x, float d, float w){",
      "  w = max(w, 1e-5);",
      "  if (d >= 1.0) return 1.0;",
      "  if (d <= 0.0) return 0.0;",
      "  return clamp((sqI(x + w, d) - sqI(x - w, d)) / (2.0 * w), 0.0, 1.0);",
      "}",
      "float hash21(vec2 p){ return fract(sin(dot(p, vec2(41.317, 289.107))) * 43758.5453); }",
      "float warpV(float x, float k, float ph){ return x + 0.42 * sin(k * TAU * x + ph) / (k * TAU); }",
      "float warpD(float x, float k, float ph){ return 1.0 + 0.42 * cos(k * TAU * x + ph); }",
      "void main(){",
      "  vec2 uv = vUv;",
      "  float aspect = uRes.x / max(uRes.y, 1.0);",
      "  float av = clamp(2.0 - 2.0 * uRot, 0.0, 1.0);",
      "  float ah = clamp(2.0 * uRot, 0.0, 1.0);",
      "  float basket = min(av, ah);",
      "  float nV = max(3.0, uNv * (1.0 - 0.25 * basket));",
      "  float nH = max(3.0, nV / max(aspect, 0.05));",
      "  float phV = uT * 0.31;",
      "  float phH = uT * 0.24 + 1.7;",
      // THE RIBBON EDGE, STRAIGHT BY DEFAULT AND WAVED WHERE THE WORK CARRIES A WAVE (his 19:13
      // word, and the charter's THE INSTRUMENT'S GEOMETRY IS READ FROM THE WORK). `uWave.x` is the
      // depth of the wave in cells and it is the whole switch: at nothing every term below is
      // exactly zero, `cV` is `warpV(uv.x) * nV` and `wV` is the plain footprint — the two lines
      // this instrument drew before 32a013a, recovered by arithmetic rather than by a second code
      // path, so a work with no measured wave draws the pre-wave frame and not a near neighbour of
      // it. The frequency and the drift ride the same switch and cost nothing when it is shut.
      "  float wAmp = uWave.x;",
      "  float wK = uWave.y;",
      "  float wR = uWave.z;",
      "  float alive = wAmp * smoothstep(0.0, 0.10, uDuty) * smoothstep(1.0, 0.90, uDuty);",
      "  float aV1 = TAU * (uv.y * wK - uT * wR);",
      "  float aV2 = TAU * (uv.y * wK * WOVER + uT * wR * WBEAT + 1.3);",
      "  float edgeV = alive * (WLOW * sin(aV1) + WHIGH * sin(aV2));",
      "  float dEdgeV = alive * TAU * wK * (WLOW * cos(aV1) + WHIGH * WOVER * cos(aV2));",
      "  float aH1 = TAU * (uv.x * wK + uT * wR);",
      "  float aH2 = TAU * (uv.x * wK * WOVER - uT * wR * WBEAT + 0.7);",
      "  float edgeH = alive * (WLOW * sin(aH1) + WHIGH * sin(aH2));",
      "  float dEdgeH = alive * TAU * wK * (WLOW * cos(aH1) + WHIGH * WOVER * cos(aH2));",
      "  float cV = warpV(uv.x, 2.0, phV) * nV + edgeV;",
      "  float cH = warpV(uv.y, 3.0, phH) * nH + edgeH;",
      "  float iv = floor(cV), fv = fract(cV);",
      "  float ih = floor(cH), fh = fract(cH);",
      // WHERE A RIBBON DIPS UNDER THE CROSSING ONE. These two numbers were read at the end of this
      // shader and used for shade alone; they are read here instead, so the same measured dip can
      // carry the level the picture is read at as well as the darkness it is drawn with. Nothing
      // about either number changed — the terms below are the ones that stood at the end.
      "  float fbv = fract(cV * 0.5), fbh = fract(cH * 0.5);",
      "  float diveV = 1.0 - smoothstep(0.0, 0.16, min(fbh, 1.0 - fbh));",
      "  float diveH = 1.0 - smoothstep(0.0, 0.16, min(fbv, 1.0 - fbv));",
      // The wandering edge tilts the cell coordinate across the OTHER axis too, so its own slope
      // joins the pixel footprint — without it a waved edge sparkles. The term is the wave's own
      // slope, so at a straight edge it is exactly 0 and the footprint is the pre-wave one.
      "  float wV = 0.5 * (nV * warpD(uv.x, 2.0, phV) / uRes.x + abs(dEdgeV) / uRes.y);",
      "  float wH = 0.5 * (nH * warpD(uv.y, 3.0, phH) / uRes.y + abs(dEdgeH) / uRes.x);",
      "  float ph = uT * uSpeed * 0.17;",
      "  float offV = uAmp * sin(TAU * (ph + (iv + 0.5) / nV * 1.5 + 0.35 * hash21(vec2(iv, uSeed))));",
      "  float offH = uAmp * sin(TAU * (ph * 0.86 + (ih + 0.5) / nH * 1.5 + 0.31 + 0.35 * hash21(vec2(uSeed, ih))));",
      "  float push = 2.0 * basket * uDuty * (1.0 - uDuty);",
      "  float dutyV = clamp(uDuty + push, 0.0, 1.0);",
      "  float dutyH = clamp(uDuty - push, 0.0, 1.0);",
      "  float guardV = smoothstep(0.0, 0.12, dutyV) * smoothstep(1.0, 0.88, dutyV);",
      "  float guardH = smoothstep(0.0, 0.12, dutyH) * smoothstep(1.0, 0.88, dutyH);",
      // The level each set is read at: its own dip, gated by the same two things the shade is
      // gated by — the basket, since a ribbon can only pass under another where two sets exist, and
      // the door gate, so a whole work standing at either door is read at its sharpest copy. The
      // reach is DEPTH_LOD levels of the chain at a full dip, and `uDepth` at nothing shuts it.
      "  float depthGate = uDepth * basket * smoothstep(0.0, 0.22, uDuty) * smoothstep(1.0, 0.78, uDuty);",
      "  float lodV = DEPTH_LOD * depthGate * diveV;",
      "  float lodH = DEPTH_LOD * depthGate * diveH;",
      "  float covV = sqcov(cV, dutyV, wV);",
      "  vec3 colV = mix(texBd(uv + vec2(0.0, -offV), lodV), texAd(uv + vec2(0.0, offV), lodV), covV);",
      "  float swV = max(4.0 * wV, min(0.12, 0.35 * min(dutyV, 1.0 - dutyV)));",
      "  float parV = step(0.5, mod(iv, 2.0));",
      "  float onBv = exp(-max(fv - dutyV, 0.0) / swV) * (1.0 - covV);",
      "  float onAv = exp(-max(dutyV - fv, 0.0) / swV) * covV;",
      "  colV *= 1.0 - 0.34 * guardV * mix(onBv, onAv, parV);",
      "  float covH = sqcov(cH, dutyH, wH);",
      "  vec3 colH = mix(texBd(uv + vec2(-offH, 0.0), lodH), texAd(uv + vec2(offH, 0.0), lodH), covH);",
      "  float swH = max(4.0 * wH, min(0.12, 0.35 * min(dutyH, 1.0 - dutyH)));",
      "  float parH = step(0.5, mod(ih, 2.0));",
      "  float onBh = exp(-max(fh - dutyH, 0.0) / swH) * (1.0 - covH);",
      "  float onAh = exp(-max(dutyH - fh, 0.0) / swH) * covH;",
      "  colH *= 1.0 - 0.34 * guardH * mix(onBh, onAh, parH);",
      "  float bv = floor(iv * 0.5), bh = floor(ih * 0.5);",
      "  float pV = av / max(av + ah, 1e-4);",
      "  float parity = step(mod(bv + bh, 2.0), 0.5);",
      "  float chooseB = clamp(parity + (2.0 * uDuty - 1.0), 0.0, 1.0);",
      "  float choose = mix(pV, chooseB, basket);",
      "  float ord = mix(0.5 * ((bv * 2.0 + 1.0) / nV + (bh * 2.0 + 1.0) / nH),",
      "                  hash21(vec2(bv, bh) + uSeed), 0.4);",
      "  float showV = step(ord * 0.996 + 0.002, choose);",
      "  vec3 col = mix(colH, colV, showV);",
      "  float grooveV = 1.0 - smoothstep(0.0, 0.05, min(fv, 1.0 - fv));",
      "  float grooveH = 1.0 - smoothstep(0.0, 0.05, min(fh, 1.0 - fh));",
      "  float shade = mix(0.55 * diveH + 0.30 * grooveH, 0.55 * diveV + 0.30 * grooveV, showV);",
      "  float shadeGate = smoothstep(0.0, 0.22, uDuty) * smoothstep(1.0, 0.78, uDuty);",
      "  col *= 1.0 - basket * shadeGate * min(shade, 0.62);",
      "  gl_FragColor = vec4(col, 1.0);",
      "}",
    ].join("\n");

    var TAU = Math.PI * 2;

    function smoothstep(a, b, x) {
      var t = (x - a) / (b - a);
      t = t < 0 ? 0 : t > 1 ? 1 : t;
      return t * t * (3 - 2 * t);
    }
    function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }

    // How far a ribbon may slide along its own axis, as a fraction of the frame. Every sample the
    // shader takes is the frame coordinate pushed by at most TRAVEL, so the cover-fit is pulled in by
    // TRAVEL at each end: ZOOM is derived from TRAVEL and is not a free number.
    var AMP = 0.10, PRESS = 1.30, TRAVEL = AMP * PRESS, ZOOM = 1 + 2 * TRAVEL + 0.03;

    // cover-fit a work into the frame, then pull in by the travel headroom. The host hands the
    // source's own dimensions, so the instrument never touches an image object.
    function fit(iw, ih, w, h) {
      var fa = w / Math.max(h, 1);
      var ia = iw / Math.max(ih, 1);
      var sx, sy;
      if (ia > fa) { sx = fa / ia; sy = 1; } else { sx = 1; sy = ia / fa; }
      return [sx / ZOOM, sy / ZOOM, 0, 0];
    }

    var AXES = ["up and down", "side to side", "both"];
    function axisNameOf(axis) {
      if (typeof axis === "number") return AXES[clamp(Math.round(axis), 0, 2)];
      return AXES.indexOf(axis) >= 0 ? axis : "both";
    }
    function rotForTime(time, axis) {
      var a = axisNameOf(axis);
      if (a === "up and down") return 0;
      if (a === "side to side") return 1;
      var p = (time / 27) % 1;
      if (p < 0) p += 1;
      return 0.5 * smoothstep(0.06, 0.16, p) + 0.5 * smoothstep(0.28, 0.38, p)
        - 0.5 * smoothstep(0.56, 0.66, p) - 0.5 * smoothstep(0.78, 0.88, p);
    }

    // THE RESPONSE CURVE (darkroom draft D2): equal movements of the hand produce equal felt change.
    // A two-piece exponential hinged at the median of the felt change of one half, mirrored about the
    // middle because a whole work stands at either end. The dead bands at either end are what make
    // both doors exact: at mix 0 the duty is a whole 1 and at mix 1 a whole 0.
    var FEEL_D0 = 0.06, FEEL_C = 0.43, FEEL_K1 = -1.6, FEEL_K2 = 1.8;
    function feelLog(x, k) {
      return Math.abs(k) < 1e-6 ? x : (Math.exp(k * x) - 1) / (Math.exp(k) - 1);
    }
    function feelKnee(u) {
      return u <= 0.5 ? FEEL_C * feelLog(2 * u, FEEL_K1)
                      : FEEL_C + (1 - FEEL_C) * feelLog(2 * u - 1, FEEL_K2);
    }
    function feelOf(u) {
      var f = u <= 0.5 ? 0.5 * feelKnee(2 * u) : 1 - 0.5 * feelKnee(2 - 2 * u);
      return FEEL_D0 + (1 - 2 * FEEL_D0) * f;
    }

    // ---- THE RESPONSE CURVES, MEASURED ON THIS INSTRUMENT'S OWN FRAME ----------------------------
    // The charter's law: equal movement of the hand, equal felt change. Until 2026-08-17 this
    // instrument carried one measured curve — `feelOf` above — and spent it on one handle, the
    // crossing's own progress, so equal steps of every other handle were not equal felt change.
    // These are the curves for the rest.
    //
    // HOW THEY WERE MEASURED. At forty-one places along the raw handle the frame is drawn twice,
    // four thousandths of the handle's own range apart, and the distance between those two frames
    // is the picture's RATE of change there. The rate is integrated along the handle and the
    // running total inverted against the hand's own twenty-one equal marks. Reading the distance
    // between consecutive COARSE steps instead saturates — past a step of a few tens of 255 two
    // frames of one photograph differ by about as much however far apart they stand — so the small
    // probe is what keeps the reading a rate. All four were read at a woven middle on a 390 x 844
    // buffer.
    //
    // WHAT THE MEASUREMENT FOUND, AND IT IS WORTH SAYING PLAINLY: this fabric's handles are close
    // to the law already. The widest felt change against the narrowest runs from 1.034 to 1.538
    // across the four, where the unfold's own raw fold measured 5.19 before its curve and its
    // stagger 12.728 before one of these. So the curves below are published rather than applied,
    // and what they buy is small and now on the record instead of assumed either way.
    //
    // WHY NONE OF THEM IS APPLIED HERE. A curve belongs on a handle whose value is a POSITION on a
    // scale. Not one of these four is: `nMul` multiplies a measured band count, `speed` is a rate,
    // `press` is a pressure in the module's own units and `wave` is a depth in cells read from the
    // work. A composer places each of them from a measurement, so applying a curve here would
    // corrupt the very number it was asked for. The curves are published beside their ranges and
    // the placing stays with whoever owns the request.
    var CURVES = {
      // band 1.390 before, 1.079 after
      nMul: [0, 0.046, 0.0889, 0.1312, 0.1763, 0.2253, 0.2731, 0.3204, 0.3694, 0.421, 0.4724, 0.5238,
               0.5741, 0.6264, 0.6784, 0.7306, 0.7835, 0.8368, 0.8903, 0.9445, 1],
      // band 1.034 before, 1.006 after
      press: [0, 0.0499, 0.0998, 0.1495, 0.199, 0.2486, 0.2981, 0.3474, 0.3968, 0.4463, 0.4961, 0.5459,
                0.5958, 0.6459, 0.6961, 0.7467, 0.7973, 0.848, 0.8987, 0.9495, 1],
      // band 1.538 before, 1.147 after. The travel this handle moves is PERIODIC — it is a rate,
      // and at the second the walk was read at it carries about three whole turns of the strips'
      // own sine — so its curve describes one instant of the clock and not the handle's whole life.
      speed: [0, 0.0471, 0.1034, 0.1557, 0.1989, 0.2455, 0.3006, 0.3505, 0.3977, 0.4497, 0.5019, 0.5498,
                0.5959, 0.6468, 0.6957, 0.747, 0.8006, 0.8509, 0.8967, 0.9468, 1],
      // band 1.367 before, 1.074 after
      wave: [0, 0.0548, 0.1048, 0.1531, 0.2009, 0.2511, 0.3025, 0.352, 0.4015, 0.4519, 0.5018, 0.5516,
               0.602, 0.6519, 0.702, 0.7515, 0.801, 0.8508, 0.9004, 0.9507, 1],
    };
    var CURVE_BANDS = { nMul: [1.39, 1.079], press: [1.034, 1.006], speed: [1.538, 1.147],
                        wave: [1.367, 1.074] };
    var CURVE_MEASURED_ON = "the drawn frame's own rate of change, read at forty-one places along "
                          + "the raw handle across a probe of four thousandths of its range, at a "
                          + "woven middle on a 390 x 844 buffer";

    // ---- THE WAVE THE WORK ITSELF CARRIES ---------------------------------------------------------
    // His 2026-08-13 11:20 word put a wave on this ribbon edge because frames between 0.35 and 0.50
    // read as flat vertical blinds; his 2026-08-17 19:13 word called that wave a regression and
    // carried the resolution in the same sentence — a wavy cut plays only where the work itself
    // carries the wave, and there introducing the wave is the beauty. Both hold at once exactly one
    // way: THE STRAIGHT RIBBON IS THE DEFAULT and the wave is a parameter the photograph's own
    // measured structure drives.
    //
    // WHAT EACH OF THE THREE READS, which is the class law of his 19:21 word — every geometric and
    // temporal parameter names the measurement it reads:
    //   · THE DEPTH, `wave`, in cells. The gate is `texture.type`, the collection's own texture
    //     vocabulary, at «рябь» — a ripple, which that vocabulary defines as a periodic band in the
    //     spectrum and which fires on nine of the hundred and twenty-one works
    //     (lab/step1-tone-texture.py:139, :380). Where it does not fire the work carries no measured
    //     wave and this handle is 0. Where it does, the depth is scaled from
    //     `1 - texture.localStraightness` — the agreement of the doubled-angle edge field inside a
    //     fifteen-point neighbourhood (lab/step1-tone-texture.py:297-305), which is the one measured
    //     number in this collection that says how far a work's own lines depart from straight.
    //   · THE PERIOD, `wavePeriod`, as a fraction of the frame side the wave runs along. Read from
    //     `texture.spectralPeriodPx` over the work's own frame side — the wavelength of the very
    //     spectral band the ripple gate fires on. That reading saturates at its own lowest bin on
    //     most of the collection, so a work standing at the ceiling carries no usable wavelength and
    //     the gate above is what keeps it from reaching this handle at all.
    //   · THE DRIFT, `waveDrift`, in cycles a second. How far the wave travels along its own ribbon
    //     in a second, as a share of its own period, so it reads the SAME measurement as the period
    //     and carries no clock of its own. It is nothing when the depth is nothing.
    // The wave's DIRECTION is not a fourth handle. The edge undulates along the ribbon's own length,
    // and which way the ribbons run is already the `axis` handle, which already names its own
    // measurement (the banding axis cut-lines.json recorded). A wave that ran across the ribbons
    // instead would be a second lattice on one level, which the levels law does not allow.
    //
    // THE CEILING is the depth lab/effects/weave.js drew at 32a013a — 0.34 of a cell in the
    // fundamental and 0.17 in the overtone, half a cell together. Past half a cell an edge reaches
    // its neighbour's own middle and the fabric stops reading as ribbons at all.
    var WAVE_MAX = 0.51;
    // The period the handle rests at where a score turns the depth up and says nothing about the
    // period: the one lab/effects/weave.js drew at 32a013a, 1.7 cycles across the frame side, said
    // here in the unit a measurement arrives in.
    var WAVE_PERIOD_DEF = 1 / 1.7;
    var WAVE_PERIOD_MIN = 0.08, WAVE_PERIOD_MAX = 2, WAVE_DRIFT_MAX = 0.5;
    // The straight edge, said once as a value rather than as an absence, so every road that asks for
    // a pose without naming the wave gets the same numbers and the pre-wave frame with them.
    var WAVE_STRAIGHT = [0, 1 / WAVE_PERIOD_DEF, 0, 0];
    function waveOf(st) {
      var amp = typeof st.wave === "number" ? clamp(st.wave, 0, WAVE_MAX) : 0;
      if (!(amp > 0)) return WAVE_STRAIGHT.slice();
      var per = typeof st.wavePeriod === "number"
        ? clamp(st.wavePeriod, WAVE_PERIOD_MIN, WAVE_PERIOD_MAX) : WAVE_PERIOD_DEF;
      var drift = typeof st.waveDrift === "number"
        ? clamp(st.waveDrift, -WAVE_DRIFT_MAX, WAVE_DRIFT_MAX) : 0;
      return [amp, 1 / per, drift, 0];
    }

    // The numbers of one frame: everything the shader gets beyond the seating of the two works is a
    // pure function of the pose. The host calls this; so does the lab's own carrier, from the same
    // source — which is why the two roads can be compared frame against frame.
    //
    // The balance is a parameter here rather than read straight off the pose, because the hold in
    // `values` below asks this same function for the same pose at the balance the door's own law
    // stands at. Nothing else about it moved: at the balance it is handed it answers, number for
    // number, what it answered before.
    function posed(st, balAsked) {
      var bal = balAsked;
      var ab = Math.abs(bal);
      var shaped = (bal < 0 ? -1 : 1) * smoothstep(0.08, 0.88, ab);
      var duty = 0.5 + 0.5 * shaped;
      var weave = 1 - smoothstep(0.14, 0.86, ab);
      return {
        duty: duty,
        amp: Math.min(AMP * weave * st.press, TRAVEL),
        nV: clamp(st.strips * st.nMul * clamp(st.cssWidth / 1000, 0.5, 1), 3, 64),
        // WHERE THE FABRIC'S GRAIN STANDS. A score that names `turn` places it directly, so the
        // grain can travel from the departing work's own band direction to the arriving work's
        // across a passage. A score that names none leaves the axis handle and its 27 s clock
        // exactly as they stood, which is what every earlier score and every conformance row reads.
        rot: st.reduced ? 0
           : (typeof st.turn === "number" ? clamp(st.turn, 0, 1) : rotForTime(st.t, st.axis)),
        // How far under a dipping ribbon reads. Nothing where no score names it, which is the frame
        // this instrument drew before the picture's chain of smaller copies existed.
        depth: typeof st.depth === "number" ? clamp(st.depth, 0, 1) : 0,
        wave: waveOf(st),
        // read on the diagnostic surface, bound to no uniform: what the handle came to
        bal: bal,
      };
    }

    // ---- THE DOOR THE INSTRUMENT READS FOR ITSELF ------------------------------------------------
    // His 18:00 architecture decision, carried in the U27 brief: the instrument reads its doors at
    // runtime on the actual buffer, and the report it hands back is the runtime truth; what the
    // manifest declares is only the claim. The meshing instrument answered that first
    // (pass-inst-gears.js, THE DOOR THE INSTRUMENT READS FOR ITSELF); this is the same law read in
    // the fabric's own units.
    //
    // WHAT A DOOR ASKS OF THIS INSTRUMENT. At the entry door the frame is the departing work whole
    // and at the exit door the arriving one, both matching the hanging picture point for point. Two
    // numbers carry that here and no others:
    //   · THE DUTY, a whole 1 at the entry door and a whole 0 at the exit. `sqcov` answers exactly
    //     1 at a duty of 1 and exactly 0 at a duty of 0 (its own first two lines), so at a whole
    //     duty both ribbon sets read ONE work at every point and the fabric is that work.
    //   · THE RIBBONS' TRAVEL, exactly 0. At a whole duty the frame is one work, but a ribbon that
    //     still slides carries that work off the hang by `amp` of the frame.
    // Both come from `bal`, and `bal` is an OPEN handle: a score that drives it lands a door at
    // whatever balance its own track says. The dial's own road cannot miss — the response curve's
    // dead band puts the balance at 0.88 at either door, which is exactly where the duty's own
    // smoothstep closes — but a driven balance can, and then the door draws the OTHER photograph at
    // full strength over the share of every band the duty leaves open. That is the leak this reads.
    //
    // WHICH INSTANT IS A DOOR. The manifest's own `doors` block names the handle and the value:
    // `mix` at 0 is the entry door and `mix` at 1 the exit. So the door is read off `mix` and the
    // state it is judged on is `bal`, which is exactly the pair the manifest publishes.
    //
    // ON WHICH GRID. The DRAWING BUFFER the host binds as `uRes` — the CSS frame times the device
    // ratio times the host's own resolution step. It is the grid the shader samples on, it is not
    // known when a plan is serialised, and it moves while a pass plays. It is also the grid the
    // fabric's own anti-aliasing half-widths are computed on (`wV`, `wH` in FRAG read `uRes`), so a
    // leak is decided there and nowhere else. The reading falls back to the CSS frame where the
    // host hands no buffer, and says which of the two it used.
    //
    // WHY A SHARE AND NOT A SENTENCE ABOUT DUTY. The share the duty leaves open is a share of EVERY
    // band, so what it costs on the frame is that share of the frame's own width — and whether any
    // sample lands inside it is a question about the grid. At a balance of 0.87 the open share is
    // 0.00036 of a band: 0.28 of a pixel on a 780 wide buffer, where no sample can land, and 1.4
    // pixels on a 4000 wide one, where several do. So the same balance is a whole door on one
    // buffer and a leak on the next, which is precisely why this is read at runtime.
    var DOOR_HOLD = 2;   // how far the hold reaches, in whole bands of the fabric
    // How far the ribbons may stand off the hang and the door still be the hanging picture: half a
    // point of the grid the shader samples on, which is the width inside which a sample stays in
    // the buffer pixel it started in.
    var DOOR_SLIP = 0.5;
    // How much of the other work a door may draw and still BE the hanging picture: half a level of
    // 255, which is under what the frame itself can carry. The charter's own door bar is 6 of 255
    // over the canvas rect (the tolerance every suite here already uses); half a level is an eighth
    // of that at one point, so a reading under it cannot be a leak anybody could photograph.
    var DOOR_SHOW = 0.5 / 255;
    // How many points of the grid one walk reads along each axis. The open share stands in every
    // band of the set, so a walk that visits one point in every few finds it as surely as a walk
    // that visits all of them, and a door instant costs a bounded number of samples whatever the
    // buffer grows to.
    var DOOR_WALK = 256;

    // THE BALANCE EITHER DOOR'S OWN LAW STANDS AT. The duty's smoothstep closes at 0.88 of the
    // balance, which is where the response curve's dead band already puts it, so the hold moves to
    // the door's own number rather than to one invented here.
    var BAL_WHOLE = 0.88;

    // The grid the door is read on, and which of the two it is. `drawn` says which one the sentence
    // below names, since a reader told «a 780 x 1688 frame» would look for a device that has none.
    function doorGridOf(st) {
      var bw = Math.round(st.bufWidth), bh = Math.round(st.bufHeight);
      if (bw >= 1 && bh >= 1) return { w: bw, h: bh, drawn: true };
      return { w: Math.round(st.cssWidth), h: Math.round(st.cssHeight), drawn: false };
    }

    // The shader's own `sqcov` at one point, carried across from FRAG above line for line.
    function sqI(t, d) { return Math.floor(t) * d + Math.min(t - Math.floor(t), d); }
    function sqcov(x, d, w) {
      w = Math.max(w, 1e-5);
      if (d >= 1) return 1;
      if (d <= 0) return 0;
      return clamp((sqI(x + w, d) - sqI(x - w, d)) / (2 * w), 0, 1);
    }
    function warpV(x, k, ph) { return x + 0.42 * Math.sin(k * TAU * x + ph) / (k * TAU); }
    function warpD(x, k, ph) { return 1 + 0.42 * Math.cos(k * TAU * x + ph); }

    // ONE RIBBON SET, READ ACROSS THE BUFFER IT IS DRAWN ON. The set's own cell coordinate is
    // walked at the buffer's own sample points along the axis the cells run across, at three places
    // along the other axis — where the living edge's own wobble stands lowest, at nothing, and
    // highest — because that wobble is a phase shift of the cell coordinate and those three phases
    // bracket every row the set is drawn on. Everything here has its counterpart in FRAG and nothing
    // is simplified.
    function setLeak(want, duty, n, ph, kWarp, across, along, edges) {
      var step = Math.max(1, Math.floor(across / DOOR_WALK));
      var pts = 0, walked = 0, worst = 0, i, e, x, base, wd, off;
      for (i = 0; i < across; i += step) {
        x = (i + 0.5) / across;
        base = warpV(x, kWarp, ph) * n;
        wd = n * warpD(x, kWarp, ph) / across;
        for (e = 0; e < edges.length; e++) {
          off = Math.abs(sqcov(base + edges[e].v, duty,
                               0.5 * (wd + Math.abs(edges[e].d) / along)) - want);
          walked++;
          if (off >= DOOR_SHOW) { pts++; if (off > worst) worst = off; }
        }
      }
      return { pts: pts, walked: walked, worst: worst };
    }

    // THE LIVING EDGE at one place along the axis it runs on: its own value and its own slope, both
    // carried from FRAG. `alive` is nothing at a whole duty, which is why a whole door reads no edge
    // at all.
    // FRAG's own four wave-shape constants, carried here digit for digit so the reading below and
    // the frame the shader draws cannot drift apart.
    var WLOW = 0.66666667, WHIGH = 0.33333333, WOVER = 1.82352941, WBEAT = 0.68888889;
    function edgeAt(u, t, alive, k, r, sg, ph2) {
      var a1 = TAU * (u * k + sg * t * r);
      var a2 = TAU * (u * k * WOVER - sg * t * r * WBEAT + ph2);
      return { v: alive * (WLOW * Math.sin(a1) + WHIGH * Math.sin(a2)),
               d: alive * TAU * k * (WLOW * Math.cos(a1) + WHIGH * WOVER * Math.cos(a2)) };
    }

    // THE DOOR, MEASURED. Null everywhere but at a door, since away from the doors a fabric woven of
    // both works is the picture rather than a fault. `want` is what each ribbon set's own coverage
    // must be at every point: 1 at the entry door, where the frame is the departing work whole, and
    // 0 at the exit door, where it is the arriving one.
    //
    // THE CHEAP GATE FIRST, and what it is. A duty short of whole leaves a share of every band open
    // to the other work, and the anti-aliasing spreads that share across the sample points nearest
    // the band's own edge — so the deepest the frame can dip is about that share times the number of
    // buffer points ONE BAND is drawn across. That estimate costs two divisions, it is the same
    // number the walk below then measures exactly, and under half a level of 255 there is nothing on
    // the frame to find. So a whole door pays two divisions and a leaking one pays the walk.
    function doorReadOf(v, st) {
      var want = st.mix === 0 ? 1 : (st.mix === 1 ? 0 : -1);
      if (want < 0) return null;
      var g = doorGridOf(st), W = g.w, H = g.h;
      if (!(W >= 1) || !(H >= 1)) return null;
      var aspect = W / Math.max(H, 1);
      // the two ribbon sets as the shader builds them: the basket's own share, the count each set is
      // drawn at ON THIS BUFFER, and the duty each is pushed to
      var av = clamp(2 - 2 * v.rot, 0, 1), ah = clamp(2 * v.rot, 0, 1);
      var basket = Math.min(av, ah);
      var nV = Math.max(3, v.nV * (1 - 0.25 * basket));
      var nH = Math.max(3, nV / Math.max(aspect, 0.05));
      var push = 2 * basket * v.duty * (1 - v.duty);
      var dutyV = clamp(v.duty + push, 0, 1), dutyH = clamp(v.duty - push, 0, 1);
      // the share of every band each set leaves to the other work, what that share costs in whole
      // bands — the unit the hold below walks in — and how deep it can dip the frame
      var openV = want ? 1 - dutyV : dutyV, openH = want ? 1 - dutyH : dutyH;
      // HOW DEEP THAT SHARE CAN DIP THE FRAME. `sqcov` averages its cell over the anti-aliasing
      // window of half-width w, so where a band's open share falls entirely inside one window the
      // frame dips by about that share over 2w — and 2w is the band's own count over the buffer's
      // points across, narrowed by the width warp, whose own floor is 1 − 0.42. Taking that floor
      // makes this the DEEPEST dip the set can draw, so a reading under half a level of 255 here is
      // a door no photograph can show a leak on.
      var dipV = openV * (W / nV) / (1 - 0.42), dipH = openH * (H / nH) / (1 - 0.42);
      var read = { grid: g, want: want, nV: nV, nH: nH, dutyV: dutyV, dutyH: dutyH,
                   openV: openV, openH: openH, open: dipV >= dipH ? openV : openH,
                   bands: Math.max(openV * nV, openH * nH),
                   travelPx: v.amp * Math.max(W, H),
                   dip: Math.max(dipV, dipH), pts: 0, walked: 0, worst: 0,
                   set: dipV >= dipH ? "columns" : "rows" };
      // THE DECISION IS THE DIP ABOVE; THE WALK BELOW IS THE REPORT. A whole door pays two
      // divisions and stops here. A door the dip already condemns is then walked, so the refusal
      // carries a measured depth on the grid rather than an estimate of one — and the walk is
      // bounded, because the open share stands in EVERY band and one band in a hundred is as
      // eloquent as all of them.
      if (read.dip < DOOR_SHOW && read.travelPx < DOOR_SLIP) return read;
      // The living edge on the buffer being drawn, at the wave the WORK asked for. A straight edge
      // makes every term of this nothing, which is why a work with no wave costs this reading the
      // same two divisions it cost before the wave existed.
      var wv = v.wave || WAVE_STRAIGHT;
      var alive = wv[0] * smoothstep(0, 0.10, v.duty) * smoothstep(1, 0.90, v.duty);
      var wK = wv[1], wR = wv[2];
      var phV = st.t * 0.31, phH = st.t * 0.24 + 1.7;
      var rows = [edgeAt(0.5 / H, st.t, alive, wK, wR, -1, 1.3),
                  edgeAt(0.5, st.t, alive, wK, wR, -1, 1.3),
                  edgeAt((H - 0.5) / H, st.t, alive, wK, wR, -1, 1.3)];
      var cols = [edgeAt(0.5 / W, st.t, alive, wK, wR, 1, 0.7),
                  edgeAt(0.5, st.t, alive, wK, wR, 1, 0.7),
                  edgeAt((W - 0.5) / W, st.t, alive, wK, wR, 1, 0.7)];
      var byCol = setLeak(want, dutyV, nV, phV, 2, W, H, rows);
      var byRow = setLeak(want, dutyH, nH, phH, 3, H, W, cols);
      read.pts = byCol.pts + byRow.pts;
      read.walked = byCol.walked + byRow.walked;
      if (byCol.worst >= byRow.worst) { read.worst = byCol.worst; read.set = "columns"; read.open = openV; }
      else { read.worst = byRow.worst; read.set = "rows"; read.open = openH; }
      return read;
    }

    // THE REFUSAL, worded the way the host's own manifest refusals read: what is wrong, in this
    // instrument's own measured numbers, on the grid it was measured on.
    function doorWhyNoOf(read, v) {
      if (!read) return null;
      var slid = read.travelPx >= DOOR_SLIP;
      if (read.dip < DOOR_SHOW && !slid) return null;
      var g = read.grid, door = read.want ? "the entry" : "the exit";
      var why = door + " door leaks: at a balance of " + v.bal.toFixed(6) + " the fabric leaves "
              + read.open.toFixed(6) + " of every band of its "
              + (read.set === "columns" ? "columns" : "rows") + " to the "
              + (read.want ? "arriving" : "departing") + " work";
      if (read.pts) {
        why += " and draws it at " + read.worst.toFixed(6) + " on " + read.pts + " of the "
             + read.walked + " points this reading walked across a "
             + g.w + " x " + g.h + (g.drawn ? " buffer" : " frame");
      } else {
        why += " on a " + g.w + " x " + g.h + (g.drawn ? " buffer" : " frame");
      }
      if (slid) {
        why += ", and its ribbons stand " + read.travelPx.toFixed(2)
             + " points of that grid off the hang";
      }
      return why + ", where " + door + " door's own law asks for the "
           + (read.want ? "departing" : "arriving") + " work at every point";
    }

    // THE NUMBERS OF ONE FRAME, WITH ITS DOOR HELD WHOLE ON THE BUFFER BEING DRAWN. Away from a door
    // this is `posed` and nothing more: the reading is taken nowhere else and no balance moves. At a
    // door whose balance leaks on the buffer being drawn, the instrument moves to the balance the
    // door's own law stands at — the fabric's own whole band, which is the only place `sqcov`
    // answers a whole work — and answers with that pose. What the score asked for and what was
    // applied are both on the record: `bal` is the balance drawn, `balRequest` is the one handed in,
    // `balBands` says how many whole bands of fabric the two stand apart, and `doorHeld` carries the
    // leak the request would have drawn, in its own words.
    //
    // HOW FAR «NEAR» REACHES, and why it is two bands. The share the duty leaves open is a share of
    // every band, so the honest unit of the distance between a balance and a whole door is the
    // number of BANDS that share adds up to. Two bands of a fabric that draws between three and
    // sixty-four is a hair of the frame — at the twenty-eight bands the handle rests at it is a
    // balance of 0.80 and closer, which is inside the response curve's own dead band's neighbourhood
    // and reads as the same door. Beyond it the fabric is genuinely woven of both works, a door
    // holding a quarter of the other photograph is not a door, and a guard that never refuses proves
    // nothing.
    //
    // WHY THE MOVE COSTS THE PICTURE NOTHING AT THE DOOR ITSELF. At a door the frame is one whole
    // work by the same law being kept, so no ribbon of either set is on screen to show which balance
    // drew it; and the travel dies at 0.86 of the balance, below the whole door's own 0.88, so the
    // held pose carries no slide either.
    function values(st) {
      var v = posed(st, st.bal);
      v.balRequest = st.bal;
      v.balBands = 0;
      v.doorHeld = null;
      var read = doorReadOf(v, st);
      var no = doorWhyNoOf(read, v);
      v.doorGrid = read ? read.grid : null;
      v.bandsDrawn = read ? read.nV : null;
      v.doorBands = read ? read.bands : null;
      if (!no) { v.doorWhyNo = null; return v; }
      if (read.bands <= DOOR_HOLD) {
        var w = posed(st, read.want ? BAL_WHOLE : -BAL_WHOLE);
        var wRead = doorReadOf(w, st);
        if (!doorWhyNoOf(wRead, w)) {
          w.balRequest = st.bal;
          w.balBands = read.bands;
          w.doorHeld = no;
          w.doorWhyNo = null;
          w.doorGrid = wRead.grid;
          w.bandsDrawn = wRead.nV;
          w.doorBands = wRead.bands;
          return w;
        }
      }
      v.doorWhyNo = no + ", and no whole band stands within " + DOOR_HOLD
                  + " bands of the balance handed in";
      return v;
    }

    var manifest = {
      id: "weave", api: 1, arity: 2,
      roles: ["disassembly", "mystery", "assembly"],
      // CELL, AND THAT IS THE WHOLE OF IT. The ribbons are the cells: `strips` is how many there
      // are, `axis` which way they run, `nMul` their count multiplier, and the three wave handles
      // shape the ribbon edge itself.
      //
      // SURFACE STOOD BESIDE IT AND WAS A FALSE DECLARATION. The woven fabric does cover the frame,
      // which is what the claim rested on, but covering the frame is not driving a level: of the
      // handles below not one moves the picture plane as a whole — they move the ribbons, or they
      // drive no structural level at all. Since every handle now declares the level it drives, a
      // level this instrument occupies but never moves is a claim it cannot keep, and keeping it
      // cost something real: an owner holds a level to the exclusion of every other cue, so
      // claiming SURFACE here silenced whichever voice actually drove it.
      levels: ["CELL"],
      // WHAT THIS INSTRUMENT CUTS ON, ADDED 2026-08-31 (cause A, item 5 — the reconciliation).
      // This file never declared the key; the composer's own `INSTRUMENTS.cuts` carried «strip»
      // with no line here to answer for it. This instrument's own fit function
      // (`INSTRUMENT_SUITS.weave`) reads the pair's `banding` measure, which `KIND_OF_MEASURE`
      // reads as `strip`, and the seam note just below calls the cells themselves «the ribbons».
      cuts: ["strip"],
      // WHERE THIS INSTRUMENT HAS A SEAM (§8's `seams` block, pass-layer.js). The cells are the
      // ribbons, and within one ribbon the frame carries the departing work up to the ribbon's own
      // `dutyV`/`dutyH` mark and the arriving work past it — the boundary `covV = sqcov(cV, dutyV,
      // wV)` reads, and `colV = mix(texBd(...), texAd(...), covV)` draws. `sqcov` does not step at
      // that mark; it runs an antialiasing window of half-width `wV`/`wH` across it, and that width
      // is built to answer the screen grid rather than an artistic choice: "The wandering edge tilts
      // the cell coordinate across the OTHER axis too, so its own slope joins the pixel footprint —
      // without it a waved edge sparkles" (the comment standing over `wV = 0.5 * (nV * warpD(...) /
      // uRes.x + abs(dEdgeV) / uRes.y)`), which reads `uRes` directly and is the same footprint a
      // plain antialiased edge would need to keep from sparkling. That is a HAIRLINE case and not a
      // HANDOVER ZONE: the width is sized to the drawing buffer's own points, not to a fraction of
      // the ribbon's length, and it exists to keep the moving edge from aliasing rather than to blend
      // two pieces over a deliberate span. `of` names no handle: `wV`/`wH` are carried in cell units
      // that grow with `nV`/`nH` only so the footprint STAYS the same width in points of the buffer
      // however many ribbons the `strips` handle asks for — the seam's own width in the unit this
      // entry publishes does not move with the count.
      seams: [{ kind: "line", of: null, unit: "points of the drawing buffer" }],
      params: { strips: [3, 64], axis: [0, 2], speed: [0.1, 2.5] },
      // EVERY handle a score can drive (§4.4b). `mix` is the dial; `clock` is the second the host
      // hands down; the other four were the module's own params and its own die, and they are
      // published here so no handle keeps a clock or a roll of its own.
      //
      // THE THREE THAT ANSWERED TO NO TRACK, brought across 2026-08-14. The module ran these on its
      // own eased clock, so under a scored run they kept moving on wall time and one seed gave a
      // different picture (§4.4b names exactly this defect):
      //   · `nMul` — THE STRIP-COUNT BREATH. The module drifts it as 1 + 0.35·sin(t·0.021·TAU + 1.1)
      //     when nobody drives, and the hand reaches 0.62 … 1.65 across the frame (weave.js:452,
      //     :443). Those two ends are the module's own, so they are the range here.
      //   · `press` — THE PRESS RESPONSE. It eases toward PRESS = 1.30 held down and back to 1 let
      //     go (weave.js:236, :466). Resting at 1 is what the module itself does under a parked
      //     pointer, so 1 is the default and 1.30 the far end.
      //   · `bal` — THE BALANCE ITSELF, which the module drifts as 0.97·sin(t·0.030·TAU)³ when no
      //     dial holds it (weave.js:450–451). It is OPEN: a score that names no track for it leaves
      //     the instrument deriving the balance from `mix` through the response curve, exactly as
      //     the module lets its own dial win over the drift (weave.js:459). Nothing falls back, so
      //     nothing is recorded as a fallback.
      //
      // THE RIBBON AXIS IS THREE NAMED STATES (2026-08-14). The entry carried min 0, max 2, def 2 —
      // the shape of a continuous range — while the handle maps onto the three names in AXES and
      // rounds anything between them to the nearest one (axisNameOf above). It now says which kind
      // it is, what each value is called, which band direction each one stands for, and which of
      // them answers the clock.
      //
      // THE TWO VOCABULARIES AGREE, AND THE SHADER IS WHERE THAT WAS READ. At axis 0 rotForTime
      // holds uRot at 0, so av is 1, ah is 0, basket is 0 and showV is 1: the frame draws the column
      // set, whose cell coordinate cV reads uv.x. Columns are the frame's VERTICAL bands and their
      // travel is along y, which is what "up and down" names. At axis 1 uRot holds at 1, showV is 0
      // and the frame draws the row set, whose cH reads uv.y: horizontal bands travelling along x.
      // The banding measurement encodes the same pair the same way — "axis: 0 vertical, 1
      // horizontal" (lab/build-sceneplan-v1.py:1475, legend at :1491) — and the lab module's own
      // uniform carries the same reading (lab/effects/weave.js:29). So a measured vertical family
      // reaches this handle as 0 and is drawn vertical, and `banding` below publishes that
      // correspondence instead of leaving it to be read out of a shader.
      //
      // ONLY THE THIRD VALUE TURNS. rotForTime returns a constant 0 for "up and down" and a constant
      // 1 for "side to side"; for "both" it walks a 27 second turn between them, holding 3.2 s and
      // 4.9 s at the two ends. Left at the default of 2 under a band family measured as standing one
      // way, the passage's own ground turns on a clock nothing measured, which is what `turns` and
      // `turnPeriodS` are here to say. The `clock` handle's range tops out at 14 s, so one pass
      // covers about half of that turn.
      //
      // THE BAND-COUNT FLOOR, AND WHAT IT PUBLISHES (2026-08-14, the lowered floors carried across
      // from lab/effects/weave.js at 148affb, where the same block stands as THE BAND-COUNT FLOOR).
      // The four gates between the handle and the shader all read 3, and they are: the declared
      // param range (`params.strips` above), the handle range published here, the frame number clamp
      //     clamp(strips · nMul · clamp(cssWidth / 1000, 0.5, 1), 3, 64)     — values() above
      // and the shader floor beneath it, max(3.0, uNv · (1 − 0.25 · basket)). They stood at 8, 8, 6
      // and 5, one behind another and none of them published, so a handle of 3, 4, 5, 6 or 8 all
      // drew six bands and a composer asking for the band family it had measured could not read what
      // the frame would draw.
      //
      // WHY THREE AND NOT LOWER. Three is the smallest band count the project's own banding measure
      // can confirm: measure_banding skips the first three bins of the column spectrum
      // (lab/cut-lines.py:172, min_k = 3), and three bands in a frame IS that first bin. At two bands
      // and below the measure reports whatever else it finds and the reading carries no meaning, so a
      // floor under three would put the instrument where no check of ours can judge it. Below three
      // the frame also stops being a weave in the eye: at two cells with the balance at the middle
      // each photograph holds a half of the frame, and the strip travel (AMP, a tenth of the frame)
      // is a third of a cell, which reads as two pictures sliding rather than as strips woven.
      //
      // WHY THREE AND NOT HIGHER. The composition asks for three bands because the worked pair shares
      // a vertical family of period 480 px in a 1440 px frame, and 1440 / 3 = 480: at a handle of 3
      // on a wide frame the instrument draws the pair's own period exactly.
      //
      // THE PUBLISHED LIMITS, measured at the pair's own seed on 2026-08-14 and recorded in
      // docs/immersive/evidence/2026-08-14-weavefloor-deterministic.md (the module) and
      // docs/design/evidence/2026-08-14-engine-weavefloor.md (this instrument):
      //   · the range of the handle is 3..64, and all four gates agree on both ends;
      //   · a handle of N on a frame at least 1000 px wide draws N bands; below 1000 px the count is
      //     scaled by cssWidth / 1000 and held at half, so a 390 px phone draws N / 2 and a handle of
      //     6 is what puts three bands on a phone;
      //   · at three drawn bands the peak lands on the frame's own third: 480 px on 1440 wide and
      //     130 px on 390 wide, by the composition's own banding measure;
      //   · the floor buys REACHABILITY, not strength. At three drawn bands the band family measures
      //     0.36 to 0.42, under the module bar of 0.5 and far under the pair's own 0.8437, and the
      //     engine-side 0.82 once quoted here is RETIRED — fourteen seeded readings across three
      //     frames found no reading near it, the strongest vertical family anywhere being 0.5342.
      //
      // WHAT THE FLOOR PROTECTS: nothing that was found to break. The anti-aliasing half-width, the
      // living edge's wobble and the two shading terms are all in cell units and hold their
      // proportion at every count; the narrowest drawn band grows from 17 px at eight bands to 51 px
      // at three; and both doors stand exact at 3, 5, 6 and 8 bands on both axes, measured against a
      // whole white and a whole black work. The one number that changes class is the basket's, where
      // the shader takes a quarter off the count and its own floor of 3 then binds, and where the row
      // count carries a floor of 3 of its own (nH above).
      //
      // ONE NUMBER, NOT THREE. The published handle floor, the number the frame draws and the shader
      // floor now say the same 3, so what the manifest publishes and what the frame draws are one
      // number at three bands as at six, and `applied` publishes the whole chain for a composer to
      // read. Every one of these gates is the lab module's own, carried here character for character;
      // the conformance rows hold this frame against that module's frame point for point.
      handles: {
        // `mix` is the crossing's own dial and `clock` the module's own time; neither drives a
        // structural level of the picture.
        mix: { min: 0, max: 1, def: 0, level: null },
        clock: { min: 0, max: 14, def: 0, level: null },
        strips: { min: 3, max: 64, def: 28,
                  applied: { floor: 3, ceiling: 64, timesHandle: "nMul",
                             frameWidth: { full: 1000, least: 0.5 },
                             drawnFloor: 3, basketTakes: 0.25 },
                  level: "CELL" },
        axis: { min: 0, max: 2, def: 2, kind: "enum", step: 1, names: AXES,
                banding: ["vertical", "horizontal"], turns: 2, turnPeriodS: 27, level: "CELL" },
        // WHERE THE GRAIN STANDS, AS A PLACE RATHER THAN AS A CLOCK. `axis` names three states and
        // only the third moves, on a 27 s walk nothing measured — which is what the entry above says
        // in its own words. A pair whose two band families CROSS has a passage written into it: the
        // fabric can enter standing on the departing work's own lines and leave standing on the
        // arriving work's. That is a place travelling between two measurements, and it needs a
        // continuous handle to travel on. 0 is the vertical band family, 1 the horizontal — the same
        // pair `axis.banding` publishes and the same pair `uRot` has always carried.
        //
        // It is OPEN, like `bal`: a score naming no track for it leaves `axis` and its clock exactly
        // as they stood, so every score written before this handle existed draws the frame it always
        // drew. Nothing falls back, so nothing is recorded as a fallback.
        turn: { min: 0, max: 1, def: 0, open: true,
                reads: "structure.banding.axis of each work — 0 where the family stands vertical "
                     + "and 1 where it lies horizontal; a passage between two crossing families "
                     + "travels this handle from the departing work's reading to the arriving "
                     + "work's, and a pair sharing one direction holds it still",
                applied: { verticalAt: 0, horizontalAt: 1, basketAt: 0.5,
                           whenAbsent: "the axis handle and its own 27 s turn" },
                // OPEN, so it drives no structural level of its own: a score naming no track for it
                // leaves the axis and its 27 s clock exactly as they stood.
                level: null },
        // HOW FAR UNDER A DIPPING RIBBON LIES. Depth was drawn as shade alone and a ribbon passing
        // under a crossing one came out as sharp as the one on top, so a basket read as tiles laid
        // side by side rather than as cloth. The dip now also carries a level of the picture's own
        // chain of smaller copies, which the host uploads. It rests at nothing, so a score naming
        // no track for it draws the frame this instrument has always drawn, and it can only reach
        // the frame where two ribbon sets exist — a single-direction weave has nothing to pass
        // under, and both doors stand at the sharpest copy by the same gate the shade uses.
        // Same class as the ribbon edge's own wave handles below: a property of the fabric's own
        // lattice, not of either photograph, so it is CELL.
        depth: { min: 0, max: 1, def: 0,
                 reads: "nothing of the work: it is a property of the FABRIC, the same class as the "
                      + "ribbon edge's own two waves and the contact shadow's own reach, and it is "
                      + "the material speaking rather than the photograph",
                 applied: { levelsAtAFullDip: 2, sharpAt: 0, needsBasket: true,
                            gate: "the same door gate the shade is held by" },
                 level: "CELL" },
        // A rate rather than a position, but what it moves is the strips' own travel — a period of
        // the lattice — so it is CELL.
        speed: { min: 0.1, max: 2.5, def: 1,
                 curve: { knots: CURVES.speed, band: CURVE_BANDS.speed, applied: false,
                          measuredOn: CURVE_MEASURED_ON },
                 level: "CELL" },
        seed: { min: 0, max: 8, def: 0, level: null },
        // THE THREE THAT CARRY THE WAVE, and the reason they are handles rather than numbers in a
        // shader. Until 2026-08-17 the ribbon edge waved on eleven literals that read nothing off
        // the photograph, on every work alike; the band count on this same instrument was measured
        // from the work, which is what the difference looks like. Each of these three now says
        // which measurement it is driven from, and all three rest at the straight edge — `wave` at
        // 0 is the whole switch and the other two cost nothing while it is shut.
        //
        // All three shape the ribbon edge itself — the repeating unit — so they stand with the
        // strip handles above rather than with the judge channels: CELL.
        wave: { min: 0, max: WAVE_MAX, def: 0, unit: "cells",
                reads: "texture.type at «рябь» as the gate, and 1 - texture.localStraightness as "
                     + "the depth; a work whose texture is not a ripple drives this to 0 and the "
                     + "ribbon edge is a straight line",
                curve: { knots: CURVES.wave, band: CURVE_BANDS.wave, applied: false,
                         measuredOn: CURVE_MEASURED_ON },
                applied: { straightAt: 0, ceiling: WAVE_MAX,
                           shape: { fundamental: WLOW, overtone: WHIGH,
                                    overtoneTimes: WOVER, overtoneDriftTimes: -WBEAT } },
                level: "CELL" },
        wavePeriod: { min: WAVE_PERIOD_MIN, max: WAVE_PERIOD_MAX, def: WAVE_PERIOD_DEF,
                      unit: "a fraction of the frame side the wave runs along",
                      reads: "texture.spectralPeriodPx over the work's own frame side — the "
                           + "wavelength of the spectral band the ripple gate fires on; the shader "
                           + "takes its reciprocal",
                      level: "CELL" },
        waveDrift: { min: -WAVE_DRIFT_MAX, max: WAVE_DRIFT_MAX, def: 0,
                     unit: "cycles a second",
                     reads: "the same texture.spectralPeriodPx, as a share of the wave's own "
                          + "period travelled in a second; nothing while the depth is nothing",
                     level: "CELL" },
        // Multiplies the strip count — the lattice's own band count: CELL.
        nMul: { min: 0.62, max: 1.65, def: 1,
                 curve: { knots: CURVES.nMul, band: CURVE_BANDS.nMul, applied: false,
                          measuredOn: CURVE_MEASURED_ON },
                 level: "CELL" },
        // The strips' own slide amplitude — a size of the lattice's own travel: CELL.
        press: { min: 1, max: PRESS, def: 1,
                 curve: { knots: CURVES.press, band: CURVE_BANDS.press, applied: false,
                          measuredOn: CURVE_MEASURED_ON },
                 level: "CELL" },
        // THE MEASUREMENT THIS HANDLE IS READ AGAINST AT A DOOR, published beside its range the way
        // the meshing instrument publishes its own. `heldWholeAtADoor` says what is read (the share
        // of every band the fabric leaves to the other work), on which grid (the drawing buffer the
        // host binds, with the CSS frame where it hands none), how far the hold reaches (two whole
        // bands of the fabric) and where the request the score handed in stays on the record.
        bal: { min: -1, max: 1, def: 1, open: true,
               applied: { heldWholeAtADoor: { bands: DOOR_HOLD, readOn: "the drawing buffer",
                                              reads: "balRequest",
                                              measures: "the share of every band the fabric leaves "
                                                      + "to the other work" } },
               // OPEN, so it drives no structural level of its own: a score naming no track for it
               // leaves the balance derived from `mix` through the response curve.
               level: null },
      },
      neutrals: { a: 0, b: 1 },
      doors: { in: { handle: "mix", value: 0, work: "a" },
               out: { handle: "mix", value: 1, work: "b" } },
      // Both doors frame alike, so one record covers them: the constant centre crop the strips'
      // travel pays for (ZOOM above; module-contract.json publishes the same 1.29).
      framings: { "0": { coverCrop: ZOOM }, "1": { coverCrop: ZOOM } },
      drivers: ["progress", "cueProgress", "time", "velocity", "capability", "noise", "static",
                "curve", "spline", "map", "add", "multiply", "mix", "clamp", "hold", "segment",
                "ramp", "slew", "oscillate", "node"],
      camera: { needs: "none", authority: "stage" },
      // THIS INSTRUMENT READS THE PICTURE AT A NAMED LEVEL of its chain of smaller copies, so the
      // host hands it the filter that walks the chain for the length of its own draw. Every
      // instrument that declares nothing here reads the sharpest copy exactly as it always did.
      gl: { preserveDrawingBuffer: false, readsChain: true },
      // THE COVERAGE LAW (§7), and this instrument's answer to it: it has no absence to publish.
      // Its two ribbon sets partition the frame — `showV` is 0 or 1 at every point and
      // `col = mix(colH, colV, showV)` takes one set or the other — and inside each set `covV`
      // chooses between work A and work B, so both branches of every mix are picture. The union of
      // the sets is the frame and no point is left unclaimed, which is why it carries the passage's
      // ground: it is the cue with nothing drawn beneath it but the cleared buffer.
      //
      // The grooves are NOT an absence. `grooveV`/`diveV` and their partners reach the picture only
      // through the multiply on `col`; writing them into the alpha would punch the fabric with a
      // hole at every ribbon edge and the cleared buffer would show through.
      coverage: { writes: false,
                  how: "the fabric partitions the frame between its two ribbon sets, so no point "
                     + "of the frame is left unclaimed and the alpha is the constant 1" },
      // The neutral pose is the ENTRY DOOR — `mix` at 0, the value the `doors` block above names —
      // so the frame keys the host reads off it at registration include the door's own record.
      neutralPose: { mix: 0, bal: 1, nMul: 1, press: 1, strips: 28, axis: 2, depth: 0,
                     wave: 0, wavePeriod: WAVE_PERIOD_DEF, waveDrift: 0,
                     cssWidth: 1000, cssHeight: 1000, t: 0, reduced: false },
      passes: [{
        program: "weave", vert: VERT, frag: FRAG, position: "aPos",
        uniforms: [
          { name: "uA", type: "sampler2D", source: "textureA" },
          { name: "uB", type: "sampler2D", source: "textureB" },
          { name: "uFitA", type: "vec4", source: "fitA" },
          { name: "uFitB", type: "vec4", source: "fitB" },
          { name: "uRes", type: "vec2", source: "resolution" },
          { name: "uT", type: "float", source: "seconds" },
          { name: "uNv", type: "float", source: "frame:nV" },
          { name: "uDuty", type: "float", source: "frame:duty" },
          { name: "uAmp", type: "float", source: "frame:amp" },
          { name: "uRot", type: "float", source: "frame:rot" },
          { name: "uWave", type: "vec4", source: "frame:wave" },
          { name: "uDepth", type: "float", source: "frame:depth" },
          { name: "uSpeed", type: "float", source: "handle:speed" },
          { name: "uSeed", type: "float", source: "handle:seed" },
        ],
      }],
      // The instrument allocates NOTHING of its own: it spends the two source-texture slots the host
      // already holds and the one programme the host builds from this manifest.
      // `bytesEstimate` is DERIVED. Two texture reads at this manifest's own reference frame
      // (`cssWidth`/`cssHeight` above, 1000×1000 CSS px), sized per variant off two facts
      // already read elsewhere on this road: the render ladder's own floor scale (pass-layer.js
      // `STEPS`, 0.50) for `lean`, the native frame for `standard`, and the device pixel ratio
      // ceiling (`DPR_CAP`, 2) for `rich` — at four bytes a pixel (RGBA8, a fact of the format),
      // doubled for the two
      // texture slots this instrument reads, times 4/3 for the mip pyramid a chain
      // read costs (`gl.readsChain`). The rest is CAPABILITY: 0 own textures, 0 own
      // framebuffers, 1 programme, 1 pass — a single-pass compositor that spends only
      // the two source slots the host already holds.
      resources: { lean: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0,
                   programs: 1, passes: 1, bytesEstimate: 2666755, variant: "lean" },
                   standard: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0,
                               programs: 1, passes: 1, bytesEstimate: 10666755,
                               variant: "standard" },
                   rich: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                           passes: 1, bytesEstimate: 42666755, variant: "rich" } },
      capabilities: ["webgl2"],
      decline: ["one work only", "a source that never decoded"],
      provenance: { labPath: "lab/effects/weave.js", commit: "148affb" },
      // HOW WELL THIS INSTRUMENT SUITS A PAIR (2026-08-18, his word of 09:51 and its sharpening at
      // 09:53). An instrument no longer answers WHETHER it takes a pair — it answers how well it
      // suits one, so a poor fit is still playable and still explains itself. The arithmetic runs in
      // the composer, which is the one place holding both records; what stands here is the
      // instrument's own statement of WHAT IT READS, which is the fact this file owns.
      //
      // THE SHAPE, for the ports in flight: `suits.reads` names the measurements, by their path in
      // a work record, and `suits.how` says in one sentence what a whole fit and a fit of nothing
      // mean for this instrument. A fit of nothing is never a refusal — it ranks last and plays
      // where nothing ranks higher.
      suits: { reads: ["structure.banding.score"],
               how: "the ribbons run along a band family, so it suits a pair that both works band, "
                  + "and the weaker of the two readings is the fit — a fabric is only as woven as "
                  + "its thinner end" },
      readiness: "production-ready",
    };

    var live = false;
    return {
      name: "weave",
      manifest: manifest,
      values: values,
      fit: fit,
      feel: feelOf,
      // WHAT THIS INSTRUMENT'S `feel` PROMISES (Phase 7, item 3b): monotone, but not door to door —
      // `feelOf` bakes its own dead band into the OUTPUT rather than holding flat at the input's
      // edge (comment above), so it reads 0.06 at mix 0 and 0.94 at mix 1 by construction, and the
      // ends law is asked of THESE numbers rather than of 0 and 1. `feelEnds` publishes them so the
      // roll call reads the instrument's own claim instead of assuming the fleet's usual door.
      // Continuity is a separate question: `feelOf` hinges its own two pieces at FEEL_C = 0.43, off
      // the middle, so the roll call below reads a real speed step at the join. Declared here so
      // the roll call reaches it and reports what it finds; repairing the hinge is core logic and
      // outside this phase's write-set (curve declaration only for the fleet's remaining
      // instruments).
      feelClass: "monotone",
      feelEnds: [feelOf(0), feelOf(1)],
      prepare: function (o) {
        if (!o.sources) return { take: false, why: "the woven instrument needs both works" };
        if (!o.cue) return { take: false, why: "no cue names it" };
        return { take: true };
      },
      start: function () { live = true; },
      // The pose the shader draws. Every number in it now comes from a handle a score can drive, so
      // a seeded run repeats to the pixel with every voice scored. `bal` is the one open handle: a
      // score that drives it directly carries the module's own drift, and a score that says nothing
      // about it leaves the balance derived from the dial through the response curve, which is how
      // the module itself resolves the same pair.
      //
      // The remaining voices ride these handles rather than constants: the two width breaths at
      // their own unaligned rates (0.31 and 0.24 + 1.7 rad) and the 27 s turn with its unequal holds
      // of 3.2 s and 4.9 s read `clock`; the strips' travel reads `clock` and `speed` together
      // (speed × 0.17, the horizontal at 0.86 of it + 0.31 turn); the over/under order reads `seed`.
      // Their rates stay inside the shader and inside rotForTime, where their author put them.
      //
      // A DOOR THIS INSTRUMENT CANNOT KEEP WHOLE IS REFUSED RATHER THAN DRAWN. The door law is the
      // instrument's own claim (the manifest's own `doors` block), so the instrument is what answers
      // for it: at either door it reads its own fabric on the buffer the host is about to bind and,
      // where the balance handed in leaves a share of every band to the other work that no whole
      // band of the hold can close, it hands the host the reason with the measured share in it
      // instead of drawing a door that is two photographs at once. The host recovers the transaction
      // on that reason and the walk's own glide carries the visitor, which is the product's own
      // behaviour with no renderer.
      frame: function (st) {
        if (!live) return;
        var h = st.handles;
        var bal = typeof h.bal === "number" ? h.bal : 1 - 2 * feelOf(clamp(h.mix, 0, 1));
        var pose = {
          bal: bal, mix: h.mix,
          nMul: h.nMul, press: h.press,
          strips: h.strips, axis: h.axis, speed: h.speed, seed: h.seed, turn: h.turn,
          depth: h.depth,
          // The wave the work carries, straight to the pose. A score that names none of the three
          // leaves the edge straight, which is the pre-wave frame.
          wave: h.wave, wavePeriod: h.wavePeriod, waveDrift: h.waveDrift,
          cssWidth: st.viewport.w, cssHeight: st.viewport.h, t: h.clock, reduced: st.reduced,
          // THE GRID THE SHADER WILL SAMPLE ON, carried into the pose so the door is read on the
          // buffer the host is about to bind as `uRes` rather than on the CSS frame around it. The
          // host settles it from the device ratio and its own resolution step, so it moves while a
          // pass plays and each door is read on the grid standing at that door's own instant.
          bufWidth: st.viewport.bufferW, bufHeight: st.viewport.bufferH,
        };
        // AT A DOOR THE INSTRUMENT SAYS WHAT IT APPLIED, and says it before it refuses. The reading
        // is taken on the buffer this frame is drawn on, so it is the run-time truth his 18:00
        // decision asks for rather than the balance the score asked for. The host stores it and
        // reads nothing in it; the walk finds it on the passage record the request came from.
        if (h.mix === 0 || h.mix === 1) {
          var v = values(pose);
          if (st.reportApplied) {
            st.reportApplied({
              door: h.mix === 0 ? "in" : "out",
              buffer: [pose.bufWidth, pose.bufHeight],
              reads: "bal", request: v.balRequest, applied: v.bal,
              moved: v.balBands, unit: "bands",
              held: v.doorHeld, whyNo: v.doorWhyNo,
            });
          }
          if (v.doorWhyNo) { st.fail(st.token, v.doorWhyNo); return; }
        }
        st.draw(pose);
        if (st.progress >= 1 && !st.pinned) st.settle(st.token);
      },
      resize: function () {},
      cancel: function () {},
      dispose: function () { live = false; },
      contextLost: function () { live = false; },
      contextRestored: function () {},
    };
  }

  // ---- what this file declares --------------------------------------------------------------
  // The host registers this instrument under the name its own manifest carries, and refuses it when
  // that name disagrees with the name whose address this file was fetched from, when its version
  // disagrees, or when its manifest asks for something the host cannot supply.
  join({
    version: INSTRUMENT_VERSION,
    instrument: weaveInstrument(),
  });
})();
