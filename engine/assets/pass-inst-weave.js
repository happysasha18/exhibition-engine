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
      "const float TAU = 6.28318530718;",
      "vec2 into(vec2 p, vec4 f){",
      "  return clamp((p - 0.5) * f.xy + 0.5 + f.zw, 0.0008, 0.9992);",
      "}",
      "vec3 texA(vec2 p){ return texture2D(uA, into(p, uFitA)).rgb; }",
      "vec3 texB(vec2 p){ return texture2D(uB, into(p, uFitB)).rgb; }",
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
      "  float nV = max(5.0, uNv * (1.0 - 0.25 * basket));",
      "  float nH = max(3.0, nV / max(aspect, 0.05));",
      "  float phV = uT * 0.31;",
      "  float phH = uT * 0.24 + 1.7;",
      "  float alive = smoothstep(0.0, 0.10, uDuty) * smoothstep(1.0, 0.90, uDuty);",
      "  float aV1 = TAU * (uv.y * 1.7 - uT * 0.090);",
      "  float aV2 = TAU * (uv.y * 3.1 + uT * 0.062 + 1.3);",
      "  float edgeV = alive * (0.34 * sin(aV1) + 0.17 * sin(aV2));",
      "  float dEdgeV = alive * TAU * (0.34 * 1.7 * cos(aV1) + 0.17 * 3.1 * cos(aV2));",
      "  float aH1 = TAU * (uv.x * 1.6 + uT * 0.081);",
      "  float aH2 = TAU * (uv.x * 2.9 - uT * 0.055 + 0.7);",
      "  float edgeH = alive * (0.34 * sin(aH1) + 0.17 * sin(aH2));",
      "  float dEdgeH = alive * TAU * (0.34 * 1.6 * cos(aH1) + 0.17 * 2.9 * cos(aH2));",
      "  float cV = warpV(uv.x, 2.0, phV) * nV + edgeV;",
      "  float cH = warpV(uv.y, 3.0, phH) * nH + edgeH;",
      "  float iv = floor(cV), fv = fract(cV);",
      "  float ih = floor(cH), fh = fract(cH);",
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
      "  float covV = sqcov(cV, dutyV, wV);",
      "  vec3 colV = mix(texB(uv + vec2(0.0, -offV)), texA(uv + vec2(0.0, offV)), covV);",
      "  float swV = max(4.0 * wV, min(0.12, 0.35 * min(dutyV, 1.0 - dutyV)));",
      "  float parV = step(0.5, mod(iv, 2.0));",
      "  float onBv = exp(-max(fv - dutyV, 0.0) / swV) * (1.0 - covV);",
      "  float onAv = exp(-max(dutyV - fv, 0.0) / swV) * covV;",
      "  colV *= 1.0 - 0.34 * guardV * mix(onBv, onAv, parV);",
      "  float covH = sqcov(cH, dutyH, wH);",
      "  vec3 colH = mix(texB(uv + vec2(-offH, 0.0)), texA(uv + vec2(offH, 0.0)), covH);",
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
      "  float fbv = fract(cV * 0.5), fbh = fract(cH * 0.5);",
      "  float grooveV = 1.0 - smoothstep(0.0, 0.05, min(fv, 1.0 - fv));",
      "  float grooveH = 1.0 - smoothstep(0.0, 0.05, min(fh, 1.0 - fh));",
      "  float diveV = 1.0 - smoothstep(0.0, 0.16, min(fbh, 1.0 - fbh));",
      "  float diveH = 1.0 - smoothstep(0.0, 0.16, min(fbv, 1.0 - fbv));",
      "  float shade = mix(0.55 * diveH + 0.30 * grooveH, 0.55 * diveV + 0.30 * grooveV, showV);",
      "  float shadeGate = smoothstep(0.0, 0.22, uDuty) * smoothstep(1.0, 0.78, uDuty);",
      "  col *= 1.0 - basket * shadeGate * min(shade, 0.62);",
      "  gl_FragColor = vec4(col, 1.0);",
      "}",
    ].join("\n");

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

    // The numbers of one frame: everything the shader gets beyond the seating of the two works is a
    // pure function of the pose. The host calls this; so does the lab's own carrier, from the same
    // source — which is why the two roads can be compared frame against frame.
    function values(st) {
      var ab = Math.abs(st.bal);
      var shaped = (st.bal < 0 ? -1 : 1) * smoothstep(0.08, 0.88, ab);
      var duty = 0.5 + 0.5 * shaped;
      var weave = 1 - smoothstep(0.14, 0.86, ab);
      return {
        duty: duty,
        amp: Math.min(AMP * weave * st.press, TRAVEL),
        nV: clamp(st.strips * st.nMul * clamp(st.cssWidth / 1000, 0.5, 1), 6, 64),
        rot: st.reduced ? 0 : rotForTime(st.t, st.axis),
      };
    }

    var manifest = {
      id: "weave", api: 1, arity: 2,
      roles: ["disassembly", "mystery", "assembly"],
      levels: ["SURFACE", "CELL"],
      params: { strips: [6, 64], axis: [0, 2], speed: [0.1, 2.5] },
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
      // THE BAND COUNT, AND WHAT THE INSTRUMENT DOES WITH THE NUMBER IT IS HANDED (measured
      // 2026-08-14). The handle published a floor of 8 while the number that reaches the shader is
      //     clamp(strips · nMul · clamp(cssWidth / 1000, 0.5, 1), 6, 64)
      // and the shader holds a floor of its own beneath that, max(5.0, uNv · (1 − 0.25 · basket)).
      // Three floors stood one behind another and none of them was published, so a composer asking
      // for the band family it had measured could not read what the frame would draw.
      //
      // WHAT WAS MEASURED. The composed passage's ground is its pair's band family: 480 px of a
      // 1440 px frame, three bands, vertical. The score asks for 3 and carries 8. On a 390 px phone
      // frame the width factor is 0.5, so a request of 3 and a request of 8 both come to rest on the
      // clamp at 6 and draw THE SAME FRAME: the banding measure the composition itself uses
      // (lab/cut-lines.py measure_banding) reads that frame's vertical family at a period of 65 px
      // with a strength of 0.25, and the frame's strongest reading is no longer a band family. At
      // three bands the same measure reads 130 px at 0.74 on the phone and 480 px at 0.82 on a
      // 1440 px frame — the pair's own number, at a strength standing with the two works' own.
      //
      // WHAT THE FLOOR PROTECTS: nothing that was found to break. The anti-aliasing half-width, the
      // living edge's wobble and the two shading terms are all in cell units and hold their
      // proportion at every count; the narrowest drawn band grows from 17 px at eight bands to 51 px
      // at three; and both doors stand exact at 3, 5, 6 and 8 bands on both axes, measured against a
      // whole white and a whole black work. The one number that changes class is the basket's, where
      // the shader takes a quarter off the count and its own floor of 5 then binds, and where the
      // row count carries a floor of 3 of its own (nH above).
      //
      // WHAT MOVED, AND WHAT DID NOT. The published floor moves from 8 to 6, the floor the
      // instrument applies on a frame 1000 px wide or wider, so the number the manifest publishes
      // and the number the frame draws are one number. Below 6 the two remaining floors are the lab
      // module's own mathematics carried here character for character — the clamp in values()
      // (weave.js:324) and the shader's max(5.0) (weave.js:73) — and the conformance rows hold this
      // frame against that module's frame point for point. Moving them here would fork this pack
      // from the source it is built from. So three bands stands outside what this instrument draws
      // today, and `applied` publishes the whole chain for a composer to read.
      handles: {
        mix: { min: 0, max: 1, def: 0 },
        clock: { min: 0, max: 14, def: 0 },
        strips: { min: 6, max: 64, def: 28,
                  applied: { floor: 6, ceiling: 64, timesHandle: "nMul",
                             frameWidth: { full: 1000, least: 0.5 },
                             drawnFloor: 5, basketTakes: 0.25 } },
        axis: { min: 0, max: 2, def: 2, kind: "enum", step: 1, names: AXES,
                banding: ["vertical", "horizontal"], turns: 2, turnPeriodS: 27 },
        speed: { min: 0.1, max: 2.5, def: 1 },
        seed: { min: 0, max: 8, def: 0 },
        nMul: { min: 0.62, max: 1.65, def: 1 },
        press: { min: 1, max: PRESS, def: 1 },
        bal: { min: -1, max: 1, def: 1, open: true },
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
      gl: { preserveDrawingBuffer: false },
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
      neutralPose: { bal: 1, nMul: 1, press: 1, strips: 28, axis: 2, cssWidth: 1000, t: 0, reduced: false },
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
          { name: "uSpeed", type: "float", source: "handle:speed" },
          { name: "uSeed", type: "float", source: "handle:seed" },
        ],
      }],
      // The instrument allocates NOTHING of its own: it spends the two source-texture slots the host
      // already holds and the one programme the host builds from this manifest.
      resources: { lean: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                           passes: 1, bytesEstimate: 0, variant: "lean" },
                   standard: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                               passes: 1, bytesEstimate: 0, variant: "standard" },
                   rich: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                           passes: 1, bytesEstimate: 0, variant: "rich" } },
      capabilities: ["webgl2"],
      decline: ["one work only", "a source that never decoded"],
      provenance: { labPath: "lab/effects/weave.js", commit: "547a100" },
      readiness: "production-ready",
    };

    var live = false;
    return {
      name: "weave",
      manifest: manifest,
      values: values,
      fit: fit,
      feel: feelOf,
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
      frame: function (st) {
        if (!live) return;
        var h = st.handles;
        var bal = typeof h.bal === "number" ? h.bal : 1 - 2 * feelOf(clamp(h.mix, 0, 1));
        st.draw({
          bal: bal,
          nMul: h.nMul, press: h.press,
          strips: h.strips, axis: h.axis, speed: h.speed, seed: h.seed,
          cssWidth: st.viewport.w, t: h.clock, reduced: st.reduced,
        });
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
