/*!pass-pack.js*/
// The effect pack — the instruments themselves, shipped as one file the host loads by address,
// version and digest (PASS-API-V1 §7/§8, his word of 2026-08-14 08:39: the engine knows no effect
// name and loads a version-pinned opaque pack).
//
// WHAT THIS FILE IS. A list of instruments and the mathematics each one draws by. Every instrument
// here is a plain record: a name, a manifest declaring its passes, its uniforms with the source
// each is bound from, its handles and its doors, and the pure functions that answer the numbers of
// one frame. The manifest's declared names are the whole interface — the host binds by them and
// refuses at registration anything it cannot supply.
//
// WHAT THIS FILE MAY NOT DO. It reads no wall clock, holds no listener, creates no WebGL context,
// loads no picture and touches no DOM (§1.2's fence). The host owns the canvas, the context, the
// frame loop, the clock, the camera and the transaction; the pack owns the picture.
//
// HOW IT REACHES THE HOST. The host fetches this file, weighs its bytes against the digest the
// build stamped, evaluates the bytes it weighed, and reads the record handed to the join function
// below. A version or a digest that fails to match is refused with its reason and the walk's own
// glide runs instead, which is what a visit with no pack has always looked like.
//
// OWNERSHIP. The three instruments standing here today were carried over from lab/effects/. The
// artistic pack and its manifests belong to tlvphotos, which builds this file from its own
// instrument sources; the engine's copy is the pack that ships until that handover lands. See the
// handover note in docs/design/ for the file's shape and its build inputs.
(function () {
  var join = window.__@@NS@@PassPack;
  if (typeof join !== "function") return;

  // THE PACK'S OWN VERSION, and the one home of that fact. The build reads this literal out of the
  // source and stamps it into the host beside the digest, so the number a pack declares and the
  // number a host was told to load cannot drift apart without the build noticing.
  var PACK_VERSION = "1.0.0";

  var TAU = Math.PI * 2;

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
      params: { strips: [8, 64], axis: [0, 2], speed: [0.1, 2.5] },
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
      handles: {
        mix: { min: 0, max: 1, def: 0 },
        clock: { min: 0, max: 14, def: 0 },
        strips: { min: 8, max: 64, def: 28 },
        axis: { min: 0, max: 2, def: 2 },
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

  // ================================================================================================
  // THE MATTER INSTRUMENT (§8) — lab/effects/matter.js carried across
  // ================================================================================================
  // What the visitor sees: the departing work loosens into a material — grain dragged along a seeded
  // field — and the arriving work condenses out of that same material. A band of loosened matter
  // travels across the frame with one work whole ahead of it and the other whole behind. It stands
  // beside the woven instrument because it carries disassembly and assembly, which the woven one
  // does not.
  //
  // What came over: the shader, the seating of a work in the frame (fit), the response curve (feel),
  // the field constants and the numbers of one frame (values). Not one number changed.
  //
  // What stayed behind: its own canvas, its own WebGL 1 context, its own frame loop, its resize
  // listener and its own accumulated clock. The instrument here reads no wall clock, holds no
  // listener, creates no context and loads no picture (§1.2's fence).
  //
  // THREE THINGS THE PORT HAD TO ANSWER, named in the module's own card
  // (docs/immersive/effects/matter.md §11):
  //   · THE UNIFORM SET. The lab carrier's draw call names one instrument's six uniforms literally,
  //     and nine of this module's fourteen have no place in that list. The host binds by the name
  //     each uniform declares in the manifest below, so the set is the instrument's own.
  //   · THE PRESERVED DRAWING BUFFER. The module asks its own context for one (matter.js:250), and
  //     §7 refuses a manifest that asks for it. What the flag stood in for is a redraw: the module
  //     draws on demand — from onParam, from resize — and between two such draws the browser has to
  //     hand back the frame that was already there. The host draws every frame of a running
  //     transaction and redraws on every resize, so the frame the compositor shows is one this
  //     instrument drew for it. The row «no empty frame at any sampled instant» measures that,
  //     across a resize as well as across the pass.
  //   · THE VERSION HEADER. This module's shader carries none, so the host's translator stamps the
  //     one it needs and no second one arrives.
  //
  // ASPECT. The module reads the frame's aspect from a uniform of its own that the host does not
  // supply. It is the ratio of the two numbers the host already binds as `resolution`, so it is
  // computed from those inside the shader and every use of it reads the same number as before.
  function matterInstrument() {
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
      "uniform float uGrainA;",      // the coarse grain of the material, cells per frame height
      "uniform float uGrainB;",      // and the fine grain over it
      "uniform vec2 uDrift;",        // where the material has drifted to, in cells
      "uniform float uLadder;",      // how much of the field is the plain ladder across the frame
      "uniform float uTau;",
      "uniform float uLoosen;",      // how far the picture is dragged, frame heights
      "uniform float uGather;",      // how wide the loosened band is, in field units
      "uniform float uSeed;",
      "uniform float uGuard;",
      "float h11(vec2 i){ return fract(sin(dot(i, vec2(41.317, 289.107)) + uSeed) * 43758.5453); }",
      // value noise with its own exact gradient: the material's grain, and the direction it drags
      "vec3 vnoise(vec2 p){",
      "  vec2 i = floor(p), f = fract(p);",
      "  float a = h11(i), b = h11(i + vec2(1.0, 0.0));",
      "  float c = h11(i + vec2(0.0, 1.0)), d = h11(i + vec2(1.0, 1.0));",
      "  vec2 u = f * f * (3.0 - 2.0 * f);",
      "  vec2 du = 6.0 * f * (1.0 - f);",
      "  float k = a - b - c + d;",
      "  float v = a + (b - a) * u.x + (c - a) * u.y + k * u.x * u.y;",
      "  float vx = ((b - a) + k * u.y) * du.x;",
      "  float vy = ((c - a) + k * u.x) * du.y;",
      "  return vec3(v, vx, vy);",
      "}",
      "vec2 into(vec2 p, vec4 f){",
      "  return clamp((p - 0.5) * f.xy + 0.5 + f.zw, 0.0008, 0.9992);",
      "}",
      "void main(){",
      "  vec2 uv = vUv;",
      "  float aspect = uRes.x / max(uRes.y, 1.0);",
      "  vec2 p = vec2(uv.x * aspect, uv.y);",
      "  float h = 1.0 / max(uRes.y, 1.0);",
      // THE FIELD: two grains of matter over a plain ladder across the frame. The ladder gives the
      // crossing its direction, the grain gives it its material.
      "  vec3 n1 = vnoise(p * uGrainA + uDrift);",
      "  vec3 n2 = vnoise(p * uGrainB - uDrift * 1.7);",
      "  float ladder = uv.x;",
      "  float F = uLadder * ladder + (1.0 - uLadder) * (0.62 * n1.x + 0.38 * n2.x);",
      "  vec2 gF = vec2(uLadder / max(aspect, 0.05), 0.0)",
      "          + (1.0 - uLadder) * (0.62 * n1.yz * uGrainA + 0.38 * n2.yz * uGrainB);",
      "  float grad = max(length(gF), 1e-5);",
      "  float d = (F - uTau) / (grad * h);",
      "  float cov = clamp(0.5 + d, 0.0, 1.0);",
      // THE LOOSENING. Strongest at the front — where the field stands nearest the threshold — and
      // gone on both sides of it, so a band of loose matter travels and the rest of the frame is the
      // picture standing still. The drag runs along the field's own gradient, and across it the two
      // works are dragged against each other.
      "  float near = exp(-((F - uTau) * (F - uTau)) / max(uGather * uGather, 1e-6));",
      "  vec2 flow = gF / grad;",
      "  vec2 across = vec2(-flow.y, flow.x);",
      "  vec2 pull = (flow * (0.6 + 0.4 * n1.x) + across * 0.8) * uLoosen * near;",
      "  vec2 pullA = vec2(pull.x / max(aspect, 0.05), pull.y);",
      "  vec2 pullB = vec2((flow.x * (0.6 + 0.4 * n2.x) - across.x * 0.8) / max(aspect, 0.05),",
      "                    flow.y * (0.6 + 0.4 * n2.x) - across.y * 0.8) * uLoosen * near;",
      "  vec3 colA = texture2D(uA, into(uv + pullA, uFitA)).rgb;",
      "  vec3 colB = texture2D(uB, into(uv + pullB, uFitB)).rgb;",
      "  vec3 col = mix(colB, colA, cov);",
      "  col *= 1.0 - 0.32 * uGuard * cov * exp(-max(d, 0.0) / 7.0);",
      "  gl_FragColor = vec4(col, 1.0);",
      "}",
    ].join("\n");

    function smoothstep(a, b, x) {
      var t = (x - a) / (b - a);
      t = t < 0 ? 0 : t > 1 ? 1 : t;
      return t * t * (3 - 2 * t);
    }
    function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }

    // HOW COARSE THE MATERIAL IS, in cells across the frame's height, at either end of the `grain`
    // handle (matter.js:191). The fine grain rides at three times the coarse one, which is what
    // gives the front its crumb.
    var GRAIN_MIN = 4, GRAIN_MAX = 34, GRAIN_FINE = 3.0;
    // How far the picture is dragged at the fullest loosening, in frame heights, and the crop that
    // pays for it (matter.js:195-196). ZOOM is derived from AMP and is no free number.
    var AMP = 0.07, ZOOM = 1 + 2 * AMP + 0.03;
    // Six parts plain ladder against four parts grain (matter.js:205). At four parts ladder the
    // field has no direction, the loosened band is the whole frame, and the picture reads as marble.
    var LADDER = 0.6;

    // cover-fit a work into the frame, then pull in by the drag's own headroom. The host hands the
    // source's own dimensions, so the instrument never touches an image object.
    function fit(iw, ih, w, h) {
      var fa = w / Math.max(h, 1);
      var ia = iw / Math.max(ih, 1);
      var sx, sy;
      if (ia > fa) { sx = fa / ia; sy = 1; } else { sx = 1; sy = ia / fa; }
      return [sx / ZOOM, sy / ZOOM, 0, 0];
    }

    // THE RESPONSE CURVE, MEASURED (matter.js:267-307, the module's re-fit of 2026-08-13): equal
    // movements of the hand, equal felt change. The rate of change of the picture per unit of the
    // raw threshold was measured with the curve taken out, that rate integrated, and this is the
    // inverse of the integral at twenty-one evenly spaced shares with straight lines between them.
    // The two-piece logarithm the module carried before it cannot hold this handle: the field's own
    // values crowd the middle and thin to nothing at both ends, so the curve stands nearly vertical
    // at both ends and nearly flat across the middle. Carried here digit for digit; the port
    // re-derives nothing.
    var FEEL_D0 = 0.05;
    var FEEL_Q = [0, 0.1994, 0.2488, 0.2852, 0.3168, 0.3454, 0.372, 0.3972, 0.4215, 0.4454,
                  0.469, 0.4925, 0.5162, 0.5405, 0.5657, 0.5923, 0.621, 0.653, 0.6902,
                  0.7388, 1];
    function feelOf(u) {
      var x = clamp((u - FEEL_D0) / (1 - 2 * FEEL_D0), 0, 1);
      var s = x * (FEEL_Q.length - 1), i = Math.min(FEEL_Q.length - 2, Math.floor(s));
      return FEEL_Q[i] + (FEEL_Q[i + 1] - FEEL_Q[i]) * (s - i);
    }

    // The numbers of one frame: everything the shader gets beyond the seating of the two works is a
    // pure function of the pose (matter.js:309-329). The threshold travels a tenth past either end
    // of the field and no further — past the field's own range every point stands on one side and
    // the work is whole, which is what makes both doors exact.
    function values(st) {
      var d = feelOf(clamp(st.mix, 0, 1));
      var grainA = GRAIN_MIN + (GRAIN_MAX - GRAIN_MIN) * clamp(st.grain, 0, 1);
      var reach = 0.5 + 0.10;
      var drift = (st.reduced ? 0 : st.t) * 0.11 * clamp(st.drift, 0, 1);
      return {
        dial: d, grainA: grainA, grainB: grainA * GRAIN_FINE, ladder: LADDER,
        gather: 0.04 + 0.26 * clamp(st.gather, 0, 1),
        tau: 0.5 - reach + 2 * reach * d,
        drift: [drift, drift * 0.6],
        loosen: st.travel * AMP * clamp(st.loosen, 0, 1) * 4 * d * (1 - d),
        guard: st.shade * smoothstep(0, 0.09, d) * smoothstep(1, 0.91, d),
      };
    }

    var manifest = {
      id: "matter", api: 1, arity: 2,
      // The module's own header ties it to the release envelope's disassembly–mystery–reassembly
      // class: the first work comes apart into the material and the second gathers out of it.
      roles: ["disassembly", "mystery", "assembly"],
      // READ OFF THE MODULE'S OWN CONSTRUCTION. The vocabulary table publishes no level for this
      // module (lab/CROSSING-BRIEF.md carries no `matter` row), so these two are derived and said to
      // be derived: one field runs over the whole frame at SURFACE, and its grain is the TEXTURE.
      levels: ["SURFACE", "TEXTURE"],
      params: { loosen: [0, 1], drift: [0, 1], gather: [0, 1], grain: [0, 1] },
      // EVERY handle a score can drive (§4.4b). `mix` is the dial and `clock` is the second the host
      // hands down; the four below them are the module's declared params; `seed` is its die; and
      // `shade` and `travel` are the two judge channels the module keeps for measuring a law on the
      // picture — the frame with the contact shadow against the frame without it, and the same for
      // the drag. They rest at 1, which is what the module does with them.
      //
      // NO HANDLE HERE KEEPS A CLOCK OF ITS OWN. The one place the module reads time is the drift of
      // the field, `t * 0.11 * drift` (matter.js:321), where `t` was its own accumulated frame time.
      // It reads the `clock` handle instead, so a seeded score repeats to the pixel.
      handles: {
        mix: { min: 0, max: 1, def: 0 },
        clock: { min: 0, max: 14, def: 0 },
        loosen: { min: 0, max: 1, def: 0.6 },
        drift: { min: 0, max: 1, def: 0.45 },
        gather: { min: 0, max: 1, def: 0.3 },
        grain: { min: 0, max: 1, def: 0.45 },
        seed: { min: 0, max: 8, def: 0 },
        shade: { min: 0, max: 1, def: 1 },
        travel: { min: 0, max: 1, def: 1 },
      },
      // The dial's two ends. At 0 the threshold stands a tenth below the field's whole range, so
      // every point covers on A; at 1 it stands a tenth above it and every point covers on B. The
      // drag and the contact shadow are both nothing there, so each door is one work and nothing
      // else. Neither is published in module-contract.json, which carries no `matter` entry — both
      // are read off the module's own geometry and the conformance rows measure them.
      neutrals: { a: 0, b: 1 },
      doors: { in: { handle: "mix", value: 0, work: "a" },
               out: { handle: "mix", value: 1, work: "b" } },
      // Both doors frame alike: the crop the drag's headroom is paid for with is a constant, while
      // the drag itself dies at both ends.
      framings: { "0": { coverCrop: ZOOM }, "1": { coverCrop: ZOOM } },
      drivers: ["progress", "cueProgress", "time", "velocity", "capability", "noise", "static",
                "curve", "spline", "map", "add", "multiply", "mix", "clamp", "hold", "segment",
                "ramp", "slew", "oscillate", "node"],
      camera: { needs: "none", authority: "stage" },
      gl: { preserveDrawingBuffer: false },
      neutralPose: { mix: 0, loosen: 0.6, drift: 0.45, gather: 0.3, grain: 0.45,
                     seed: 0, shade: 1, travel: 1, t: 0, reduced: false },
      passes: [{
        program: "matter", vert: VERT, frag: FRAG, position: "aPos",
        uniforms: [
          { name: "uA", type: "sampler2D", source: "textureA" },
          { name: "uB", type: "sampler2D", source: "textureB" },
          { name: "uFitA", type: "vec4", source: "fitA" },
          { name: "uFitB", type: "vec4", source: "fitB" },
          { name: "uRes", type: "vec2", source: "resolution" },
          { name: "uGrainA", type: "float", source: "frame:grainA" },
          { name: "uGrainB", type: "float", source: "frame:grainB" },
          { name: "uDrift", type: "vec2", source: "frame:drift" },
          { name: "uLadder", type: "float", source: "frame:ladder" },
          { name: "uTau", type: "float", source: "frame:tau" },
          { name: "uLoosen", type: "float", source: "frame:loosen" },
          { name: "uGather", type: "float", source: "frame:gather" },
          { name: "uGuard", type: "float", source: "frame:guard" },
          { name: "uSeed", type: "float", source: "handle:seed" },
        ],
      }],
      // The instrument allocates nothing of its own: it spends the two source-texture slots the host
      // already holds and the one programme the host builds from this manifest.
      resources: { lean: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                           passes: 1, bytesEstimate: 0, variant: "lean" },
                   standard: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                               passes: 1, bytesEstimate: 0, variant: "standard" },
                   rich: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                           passes: 1, bytesEstimate: 0, variant: "rich" } },
      capabilities: ["webgl2"],
      decline: ["one work only", "a source that never decoded"],
      provenance: { labPath: "lab/effects/matter.js", commit: "e0f1b91" },
      readiness: "production-ready",
    };

    var live = false;
    return {
      name: "matter",
      manifest: manifest,
      values: values,
      fit: fit,
      feel: feelOf,
      prepare: function (o) {
        if (!o.sources) return { take: false, why: "the matter instrument needs both works" };
        if (!o.cue) return { take: false, why: "no cue names it" };
        return { take: true };
      },
      start: function () { live = true; },
      // The pose the shader draws. Every number in it comes from a handle a score can drive, and the
      // field's drift reads the second the host hands down, so a seeded run repeats to the pixel.
      frame: function (st) {
        if (!live) return;
        var h = st.handles;
        st.draw({
          mix: h.mix, loosen: h.loosen, drift: h.drift, gather: h.gather, grain: h.grain,
          shade: h.shade, travel: h.travel, seed: h.seed, t: h.clock, reduced: st.reduced,
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

  // ================================================================================================
  // THE MESHING INSTRUMENT (§8) — lab/effects/gears.js carried across
  // ================================================================================================
  // TWO WHEELS, MESHING. Their centres stand off the frame on either side, so what the eye sees is
  // the line where the two rims meet — a row of interlocking teeth running down the picture — and the
  // crossing is that line rolling across the frame, one work riding each wheel.
  //
  // What came over: the shader, the seating of a work in the frame (coverFit), the response curve
  // (the measured inverse FEEL_Q), the ladder of small whole ratios, and the numbers of one frame
  // (values). What stayed behind: its own canvas, its own WebGL 1 context, its own frame loop, its
  // resize listener and its own clock. The instrument here reads no wall clock, holds no listener,
  // creates no context and loads no picture (§1.2's fence).
  //
  // THE FOUR THINGS THE MODULE'S CARD ASKED A PORT TO PROVE (docs/immersive/effects/gears.md §11),
  // and where each stands here.
  //   1. The uniform set is bound BY DECLARED NAME from the manifest below — nineteen names, of
  //      which only six are shared with the woven instrument. The host reads the manifest; no list
  //      of names is written into the host.
  //   2. `preserveDrawingBuffer` is off. The lab module asked for it at gears.js:276 and drew only
  //      on a parameter change, on a resize and on its own frame loop, so the preserved buffer was
  //      standing in for the frames it did not draw. THE REDRAW IT STOOD IN FOR IS CARRIED: this
  //      instrument draws on EVERY frame the host hands it, including a reduced-motion run, where
  //      the module rendered once and stopped. Reduced motion stops the wheels' drive and never the
  //      drawing.
  //   3. The `ratio` handle steps through the module's own ladder of small whole pairs and is never
  //      interpolated. A tooth count is a whole number by the time it reaches the shader, so a tooth
  //      of one wheel always meets a gap of the other and the mesh closes on itself.
  //   4. The shader carries no version header of its own, so the host's translator stamps exactly
  //      one. A row counts them.
  //
  // ONE LINE OF THE SHADER IS NOT THE MODULE'S. The lab module hands the frame's aspect in as its
  // own uniform, computed from the drawing buffer it owns. The host owns the buffer here and already
  // binds its size as `uRes`, so the aspect is derived from `uRes` inside the shader. The mathematics
  // then reads the buffer the host actually drew into, whatever the resolution ladder has done to it.
  // Every other line of the shader is the module's own, character for character.
  function gearsInstrument() {
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
      "uniform vec2 uCA;",            // the first wheel's centre, frame half-heights
      "uniform vec2 uCB;",            // the second wheel's
      "uniform float uR1;",           // their pitch radii
      "uniform float uR2;",
      "uniform float uN1;",           // and their tooth counts, which stand in the same ratio
      "uniform float uN2;",
      "uniform float uAmp;",          // how far a tooth stands out of the pitch circle
      "uniform float uPh;",           // where the teeth stand along the rims: the wheels' own turn
      "uniform float uFlank;",        // how upright a tooth's flank is
      "uniform float uSpread;",       // how far apart the teeth's own moments are set
      "uniform float uSeed;",
      "uniform float uOff;",          // counter-motion, tangential, frame heights
      "uniform float uGuard;",
      "const float PI = 3.14159265359;",
      "const float TAU = 6.28318530718;",

      "float hash11(float n){ return fract(sin(n * 127.1) * 43758.5453); }",

      // A TOOTH, not a wave. A cosine gives a boundary that curves the whole way and reads as a
      // blob; a tooth stands out to its full height, holds there across its own top, and drops on
      // a flank. uFlank is how much of a tooth is flank — the clamp does the holding.
      "float tooth(float x){ return clamp(sin(x) / uFlank, -1.0, 1.0); }",
      "float toothD(float x){ return abs(sin(x)) < uFlank ? cos(x) / uFlank : 0.0; }",

      "vec2 into(vec2 p, vec4 f){",
      "  return clamp((p - 0.5) * f.xy + 0.5 + f.zw, 0.0008, 0.9992);",
      "}",

      "void main(){",
      "  vec2 uv = vUv;",
      // the aspect of the buffer the host drew into, read from the size the host binds
      "  float uAspect = uRes.x / max(uRes.y, 1.0);",
      // the frame in half-heights: x across, y up
      "  vec2 p = vec2((uv.x - 0.5) * 2.0 * uAspect, (0.5 - uv.y) * 2.0);",
      "  float h = 2.0 / max(uRes.y, 1.0);",

      // EACH WHEEL, AS A RIM. The point stands somewhere out from each centre; the rim it is being
      // held against is the pitch circle with the teeth standing on it, and how far INSIDE that rim
      // the point lies is what decides whose the point is.
      "  vec2 dA = p - uCA;   float rA = max(length(dA), 1e-5);",
      "  vec2 dB = p - uCB;   float rB = max(length(dB), 1e-5);",
      "  vec2 uAv = dA / rA;  vec2 nA = vec2(-uAv.y, uAv.x);",
      "  vec2 uBv = dB / rB;",
      // the angle round each wheel, both counted from the ray that runs to the point where the two
      // rims meet — so ONE arc length, one pitch, and the two sets of teeth cannot drift apart
      "  float thA = atan(dA.y, dA.x);",
      "  float thB = atan(dB.y, -dB.x);",
      "  float wA = uN1 * thA + uPh;",
      "  float wB = uN2 * thB + uPh;",
      // the second wheel's teeth are the first's turned inside out: where one stands, the other is
      // a gap, which is what meshing is
      "  float RA = uR1 + uAmp * tooth(wA);",
      "  float RB = uR2 - uAmp * tooth(wB);",

      // WHICH WEDGE OF WHICH WHEEL, and when that tooth hands over: six parts a ladder down the
      // line where the two rims meet, four parts the score's die.
      "  float ti = floor(wA / TAU);",
      "  float ladder = clamp(0.5 + 0.5 * p.y, 0.0, 1.0);",
      "  float ord = mix(ladder, hash11(ti + uSeed), 0.4);",

      "  float M = (RA - rA) - (RB - rB) + uSpread * (ord - 0.5);",
      // the field's own gradient, exactly: the rims' own turning plus the two radial directions
      "  vec2 gB = vec2(dB.y, -dB.x) / (rB * rB);",
      "  vec2 gM = uAmp * toothD(wA) * uN1 * nA / rA",
      "          + uAmp * toothD(wB) * uN2 * gB",
      "          - uAv + uBv;",
      "  float grad = max(length(gM), 1e-5);",
      "  float d = M / (grad * h);",
      "  float cov = clamp(0.5 + d, 0.0, 1.0);",

      // the two works sweep along their own rims, against each other at the mesh — the flanks of
      // two meshing teeth slide past one another, and this is that slide
      "  vec2 tA = vec2(nA.x / max(uAspect, 0.05), -nA.y);",
      "  vec2 tB = vec2(-uBv.y / max(uAspect, 0.05), uBv.x);",
      "  vec3 colA = texture2D(uA, into(uv + tA * uOff, uFitA)).rgb;",
      "  vec3 colB = texture2D(uB, into(uv - tB * uOff * (uN1 / max(uN2, 1.0)), uFitB)).rgb;",
      "  vec3 col = mix(colB, colA, cov);",

      "  col *= 1.0 - 0.32 * uGuard * (1.0 - cov) * exp(-max(-d, 0.0) / 7.0);",
      "  gl_FragColor = vec4(col, 1.0);",
      "}",
    ].join("\n");

    function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
    function smoothstep(a, b, x) {
      var t = (x - a) / (b - a);
      t = t < 0 ? 0 : t > 1 ? 1 : t;
      return t * t * (3 - 2 * t);
    }

    // THE SMALL WHOLE RATIOS the handle walks. A gear pair is only a gear pair when the two counts
    // stand in a ratio of small whole numbers — that is what makes the mesh close on itself — so the
    // handle does not slide through the reals: it steps through this ladder. The `ratio` handle is a
    // place on the ladder and is rounded to a rung before any count is taken from it.
    var RATIOS = [[1, 1], [3, 4], [2, 3], [1, 2], [2, 5], [1, 3], [1, 4]];

    // THE TANGENTIAL SWEEP, in frame heights, and the crop that pays for it. The sweep is bounded
    // and the wheels' own turning is unbounded — the teeth go round for as long as the clock runs,
    // while the pictures only lean into the sweep — so the crop stays small.
    var AMP = 0.05;
    var ZOOM = 1 + 2 * AMP + 0.03;

    // How tall a tooth stands against its own pitch. A real gear tooth stands about a third of its
    // pitch out of the pitch circle on each side; below about a tenth the mesh reads as a wavy line
    // and above about a half the teeth are longer than they are wide and read as a comb.
    var TOOTH_MIN = 0.12, TOOTH_MAX = 0.40;

    // THE MEASURED RESPONSE CURVE, carried over digit for digit (gears.js:329-337). How far the
    // picture moves per unit of the raw travel was measured with the curve taken out of the module,
    // that rate integrated, and this is the inverse of the integral at twenty-one evenly spaced
    // shares, with straight lines between them. Half the whole change stands at 0.28 of the travel,
    // which is why no two-piece logarithm fits it.
    var FEEL_D0 = 0.05;
    var FEEL_Q = [0, 0.0272, 0.0544, 0.0815, 0.1084, 0.1348, 0.1608, 0.1869, 0.214, 0.244,
                  0.2807, 0.3286, 0.3865, 0.4545, 0.545, 0.6185, 0.6926, 0.7607, 0.8211,
                  0.8897, 1];
    function feelOf(u) {
      var x = clamp((u - FEEL_D0) / (1 - 2 * FEEL_D0), 0, 1);
      var s = x * (FEEL_Q.length - 1), i = Math.min(FEEL_Q.length - 2, Math.floor(s));
      return FEEL_Q[i] + (FEEL_Q[i + 1] - FEEL_Q[i]) * (s - i);
    }

    // cover-fit a work into the frame, then pull in by the travel headroom. The host hands the
    // source's own dimensions, so the instrument never touches an image object.
    function fit(iw, ih, w, h) {
      var fa = w / Math.max(h, 1);
      var ia = iw / Math.max(ih, 1);
      var sx, sy;
      if (ia > fa) { sx = fa / ia; sy = 1; } else { sx = 1; sy = ia / fa; }
      return [sx / ZOOM, sy / ZOOM, 0, 0];
    }

    function ratioAt(v) { return RATIOS[Math.round(clamp(v, 0, 1) * (RATIOS.length - 1))]; }

    // ---- WHERE THE RIMS MEET AT A DOOR, SOLVED RATHER THAN APPROXIMATED ---------------------------
    // At a door one whole work stands, which asks that the mask cover the whole frame: at door 0
    // every point of the frame lies inside the first wheel's rim, at door 1 every point lies inside
    // the second's. The module holds that by standing the meeting line beyond the frame's own edge
    // by `2·amp + spread/4 + 0.08`, which is the right margin for ONE wheel size — the module's own
    // R_BASE of 4.5, where the two rims are nearly straight across the frame and the field grows as
    // twice the distance from the meeting line.
    //
    // The port lets the wheel size travel, because that is what carries the pair's own reading from
    // angular to ring. At a small size the rims are no longer straight: the field is a function of
    // the ANGLE about the pair, it reaches its full depth only far from the pair, and the module's
    // margin leaves teeth of the far work standing in the frame's corners. So the condition itself
    // is solved instead of approximated.
    //
    // The condition, written out. Away from the teeth the mask's field is
    //     G(p) = R1 − R2 + |p − cB| − |p − cA|,
    // and the teeth and the spread move it by at most `2·amp + spread/2`. G is monotone over the
    // frame, so its extremes stand at the frame's four corners. Door 0 asks that the smallest G over
    // those corners stand above that much, door 1 that the largest stand below it. G improves as the
    // pair is carried further out, so a bisection on the reach finds the smallest reach that answers
    // both doors. The walk is a fixed count of steps and reads no clock, so a seeded run repeats.
    var DOOR_SLACK = 0.02;   // half-heights; the mask crosses over within about half a point of the
                             // boundary, and this stands well clear of that on any frame the host runs
    function gAt(px, py, cA, cB, R1, R2) {
      var ax = px - cA[0], ay = py - cA[1], bx = px - cB[0], by = py - cB[1];
      return R1 - R2 + Math.sqrt(bx * bx + by * by) - Math.sqrt(ax * ax + ay * ay);
    }
    // The smallest and largest G over the frame's four corners, with the pair standing at `xc`.
    function gEdge(xc, ox, oy, R1, R2, aspect) {
      var cA = [xc - R1 + ox, oy], cB = [xc + R2 + ox, oy];
      var lo = Infinity, hi = -Infinity, i, j, g;
      for (i = -1; i <= 1; i += 2) {
        for (j = -1; j <= 1; j += 2) {
          g = gAt(i * aspect, j, cA, cB, R1, R2);
          if (g < lo) lo = g;
          if (g > hi) hi = g;
        }
      }
      return { lo: lo, hi: hi };
    }
    function doorsHold(reach, ox, oy, R1, R2, aspect, need) {
      return gEdge(reach, ox, oy, R1, R2, aspect).lo > need
          && gEdge(-reach, ox, oy, R1, R2, aspect).hi < -need;
    }
    function reachFor(aspect, ox, oy, R1, R2, amp, spread) {
      var need = 2 * amp + 0.5 * spread + DOOR_SLACK;
      // the module's own margin first, widened by however far the centre has been carried across
      var base = aspect + 2 * amp + spread * 0.25 + 0.08 + Math.abs(ox);
      if (doorsHold(base, ox, oy, R1, R2, aspect, need)) return base;
      var lo = base, hi = base, i;
      for (i = 0; i < 48 && !doorsHold(hi, ox, oy, R1, R2, aspect, need); i++) {
        lo = hi;
        hi = hi * 2 + 1;
      }
      for (i = 0; i < 48; i++) {
        var mid = 0.5 * (lo + hi);
        if (doorsHold(mid, ox, oy, R1, R2, aspect, need)) hi = mid; else lo = mid;
      }
      return hi;
    }

    // THE NUMBERS OF ONE FRAME. Everything the shader gets beyond the seating of the two works is a
    // pure function of the pose. This is the module's own `values()` with three of its constants
    // published as handles: the pair's own size (the module's R_BASE), the tooth pitch (the module's
    // `teeth`, said as the band period it makes) and the pair's centre (the module pins it to the
    // middle of the frame's height).
    function values(st) {
      var aspect = Math.max(st.cssWidth, 1) / Math.max(st.cssHeight, 1);
      var d = clamp(st.dial, 0, 1);
      var rr = ratioAt(st.ratio);

      // THE PAIR. The two works' repeat counts stand as the ratio of the two WHEELS — equal tooth
      // pitch, counts and radii in one and the same small whole ratio, so the mesh closes on itself
      // and a tooth of one always meets a gap of the other. The pitch is the band period the score
      // holds, said in frame half-heights; the counts follow from it and from the pair's size,
      // rounded to whole teeth so the closing is exact.
      var pitch = clamp(2 * st.bandPeriod, 0.04, 2.0);
      var size = clamp(st.size, 0.3, 8);
      // BOTH COUNTS COME FROM ONE WHOLE MULTIPLIER, which is what holds them in the rung's own
      // ratio. The module takes the first count from the geometry and the second by rounding
      // `n1 · r2/r1`, and at the rungs whose first number is above one that rounding lands off the
      // ratio: 3:4 comes out as 14:19 and 2:3 as 13:20, and a mesh in 19:14 does not close on
      // itself — a tooth stops meeting a gap after one turn. Counting in whole rungs holds the ratio
      // exactly and returns the module's own 57:114 at the module's own handles, so nothing about
      // its default frame moves.
      var span = rr[0] + rr[1];
      var k = Math.max(1, Math.round(TAU * size * 2 / (span * pitch)));
      while (rr[0] * k < 3 || rr[1] * k < 3) k++;
      var n1 = rr[0] * k, n2 = rr[1] * k;
      var R1 = n1 * pitch / TAU, R2 = n2 * pitch / TAU;
      var amp = pitch * (TOOTH_MIN + (TOOTH_MAX - TOOTH_MIN) * clamp(st.tooth, 0, 1));

      // How far apart the teeth's own moments stand, in the mask's own units. The mask reads about
      // twice the distance from the line where the rims meet, so a spread of one moves a tooth's own
      // moment by a quarter of a frame height — one tooth handing over while its neighbour has not.
      var spread = clamp(st.order, 0, 1) * 1.2;

      // A TOOTH STANDS NO TALLER THAN THE WHEEL IT STANDS ON. Away from the teeth the mask's field
      // runs from −2·R2 to +2·R1, so a door can only be a whole work while the teeth and the spread
      // together stay inside that depth. At the module's own size the depth is nine half-heights and
      // nothing comes near it; at a small pair with a far-apart ratio the two together can ask for
      // more than the field holds, and then no placement of the pair makes either door whole. Both
      // are scaled back together, which keeps their proportion and keeps both doors exact.
      var room = 2 * Math.min(R1, R2) * 0.85 - DOOR_SLACK;
      var want = 2 * amp + 0.5 * spread;
      if (want > room) {
        var back = room > 0 ? room / want : 0;
        amp *= back;
        spread *= back;
      }

      // WHERE THE PAIR STANDS ACROSS THE FRAME. The centre travels in the frame's own coordinates,
      // the same ones the radial measure reads: x across from the left edge, y down from the top.
      var ox = (clamp(st.centreX, 0, 1) - 0.5) * 2 * aspect;
      var oy = (0.5 - clamp(st.centreY, 0, 1)) * 2;

      var reach = reachFor(aspect, ox, oy, R1, R2, amp, spread);
      var xc = reach - 2 * reach * d;

      // THE WHEELS TURN, and they turn from two things at once. THE TRAVEL rolls them: the pair moves
      // across the frame and the rims roll on each other without slipping, one tooth of turn for
      // every tooth of travel, which is why the teeth never come unmeshed. THE CLOCK drives them on
      // top of that, windowed to nothing at both doors, so the first work stands still, the drive
      // spins up, and the second is brought to standing exactly as it lands.
      var win = Math.sin(Math.PI * d);
      var rate = 2.6 * clamp(st.turn, 0, 1) * win;
      var ph = (reach - xc) * (TAU / pitch) + (st.reduced ? 0 : st.t) * rate;

      return {
        n1: n1, n2: n2, R1: R1, R2: R2, amp: amp, ph: ph, spread: spread,
        flank: clamp(st.flank, 0.05, 1),
        cA: [xc - R1 + ox, oy], cB: [xc + R2 + ox, oy],
        off: clamp(st.travel, 0, 1) * AMP * 4 * d * (1 - d),
        guard: clamp(st.shade, 0, 1) * smoothstep(0, 0.09, d) * smoothstep(1, 0.91, d),
        // read on the diagnostic surface, bound to no uniform: what the handles came to
        pitch: pitch, reach: reach, xc: xc, rate: rate, dial: d, size: size,
        ratioN: rr[0] * 1000 + rr[1],
      };
    }

    var manifest = {
      id: "gears", api: 1, arity: 2,
      roles: ["disassembly", "mystery", "assembly"],
      levels: ["SURFACE", "CELL"],
      params: { bandPeriod: [0.02, 1], ratio: [0, 1], size: [0.3, 8] },
      // EVERY handle a score can drive (§4.4b). The module ran its wheels on its own accumulating
      // clock and held its judges, its die and its flank as constants; all of them are published
      // here, so no handle keeps a clock or a roll of its own and a seeded run repeats to the pixel.
      //
      // THE THREE THE PORT PUBLISHES THAT THE MODULE HELD AS CONSTANTS, and why each is a handle:
      //   · `size` — THE PAIR'S OWN SIZE in frame half-heights, the module's R_BASE of 4.5. The
      //     module's own note names both ends of it: "Below about three the rims curve hard enough
      //     inside the frame to read as two circles overlapping; above about eight they are straight
      //     and the pair stops reading as wheels at all" (gears.js:211-215). That is the axis the
      //     measured pair travels along, so it is published rather than pinned.
      //   · `bandPeriod` — THE TOOTH PITCH, said as the period of the tooth line as a fraction of the
      //     frame's height. The module carried the same number as a whole count of teeth across the
      //     height, stepped 3 to 12; said as a period it is the unit the pair's own measurement uses,
      //     and the count no longer has to be whole, which is what puts the pair's measured period
      //     inside reach.
      //   · `centreX`/`centreY` — WHERE THE PAIR STANDS, in the frame's own coordinates. The module
      //     pins the pair to the middle of the frame's height and carries it across the frame on the
      //     dial alone. The field is built from the distance to each centre, so carrying both centres
      //     together moves the whole construction and changes no mathematics.
      //
      // `dial` is OPEN: a score that names no track for it leaves the instrument deriving the
      // travelled number from `mix` through the measured response curve, exactly as the module does.
      // Nothing falls back, so nothing is recorded as a fallback.
      handles: {
        mix: { min: 0, max: 1, def: 0 },
        clock: { min: 0, max: 14, def: 0 },
        dial: { min: 0, max: 1, def: 0, open: true },
        size: { min: 0.3, max: 8, def: 4.5 },
        centreX: { min: 0, max: 1, def: 0.5 },
        centreY: { min: 0, max: 1, def: 0.5 },
        bandPeriod: { min: 0.02, max: 1, def: 1 / 6 },
        ratio: { min: 0, max: 1, def: 0.5 },
        tooth: { min: 0, max: 1, def: 0.4 },
        order: { min: 0, max: 1, def: 0.4 },
        turn: { min: 0, max: 1, def: 0.55 },
        flank: { min: 0.05, max: 1, def: 0.35 },
        seed: { min: 0, max: 8, def: 0 },
        shade: { min: 0, max: 1, def: 1 },
        travel: { min: 0, max: 1, def: 1 },
      },
      neutrals: { a: 0, b: 1 },
      doors: { in: { handle: "mix", value: 0, work: "a" },
               out: { handle: "mix", value: 1, work: "b" } },
      // Both doors frame alike, so one record covers them: the constant centre crop the tangential
      // sweep is paid for with (ZOOM above, 1.13).
      framings: { "0": { coverCrop: ZOOM }, "1": { coverCrop: ZOOM } },
      drivers: ["progress", "cueProgress", "time", "velocity", "capability", "noise", "static",
                "curve", "spline", "map", "add", "multiply", "mix", "clamp", "hold", "segment",
                "ramp", "slew", "oscillate", "node"],
      // The construction moves no point of view: it decides which wheel owns each point of the frame
      // and slides the two works along their own rims inside it. Both are what it does to its own
      // surface, so the witness camera stays the stage's (§6).
      camera: { needs: "none", authority: "stage" },
      gl: { preserveDrawingBuffer: false },
      neutralPose: { dial: 0, size: 4.5, centreX: 0.5, centreY: 0.5, bandPeriod: 1 / 6, ratio: 0.5,
                     tooth: 0.4, order: 0.4, turn: 0.55, flank: 0.35, shade: 1, travel: 1,
                     cssWidth: 1000, cssHeight: 1000, t: 0, reduced: false },
      passes: [{
        program: "gears", vert: VERT, frag: FRAG, position: "aPos",
        uniforms: [
          { name: "uA", type: "sampler2D", source: "textureA" },
          { name: "uB", type: "sampler2D", source: "textureB" },
          { name: "uFitA", type: "vec4", source: "fitA" },
          { name: "uFitB", type: "vec4", source: "fitB" },
          { name: "uRes", type: "vec2", source: "resolution" },
          { name: "uCA", type: "vec2", source: "frame:cA" },
          { name: "uCB", type: "vec2", source: "frame:cB" },
          { name: "uR1", type: "float", source: "frame:R1" },
          { name: "uR2", type: "float", source: "frame:R2" },
          { name: "uN1", type: "float", source: "frame:n1" },
          { name: "uN2", type: "float", source: "frame:n2" },
          { name: "uAmp", type: "float", source: "frame:amp" },
          { name: "uPh", type: "float", source: "frame:ph" },
          { name: "uFlank", type: "float", source: "frame:flank" },
          { name: "uSpread", type: "float", source: "frame:spread" },
          { name: "uOff", type: "float", source: "frame:off" },
          { name: "uGuard", type: "float", source: "frame:guard" },
          { name: "uSeed", type: "float", source: "handle:seed" },
        ],
      }],
      // The instrument allocates nothing of its own: it spends the two source-texture slots the host
      // already holds and the one programme the host builds from this manifest.
      resources: { lean: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                           passes: 1, bytesEstimate: 0, variant: "lean" },
                   standard: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                               passes: 1, bytesEstimate: 0, variant: "standard" },
                   rich: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                           passes: 1, bytesEstimate: 0, variant: "rich" } },
      capabilities: ["webgl2"],
      decline: ["one work only", "a source that never decoded"],
      provenance: { labPath: "lab/effects/gears.js", commit: "e0f1b91" },
      readiness: "production-ready",
    };

    var live = false;
    return {
      name: "gears",
      manifest: manifest,
      values: values,
      fit: fit,
      feel: feelOf,
      prepare: function (o) {
        if (!o.sources) return { take: false, why: "the meshing instrument needs both works" };
        if (!o.cue) return { take: false, why: "no cue names it" };
        return { take: true };
      },
      start: function () { live = true; },
      // The pose the shader draws. Every number in it comes from a handle a score can drive.
      //
      // THE REDRAW THE PRESERVED BUFFER STOOD IN FOR. The lab module drew on a parameter change, on
      // a resize and on its own frame loop, and under reduced motion it drew once and stopped —
      // whatever stayed on screen after that was the preserved buffer's doing. Here the host's
      // buffer keeps nothing between frames, so this draws on every frame it is handed, reduced or
      // not. Reduced motion stops the wheels' drive inside `values` and stops nothing else.
      frame: function (st) {
        if (!live) return;
        var h = st.handles;
        var dial = typeof h.dial === "number" ? h.dial : feelOf(clamp(h.mix, 0, 1));
        st.draw({
          dial: dial,
          size: h.size, centreX: h.centreX, centreY: h.centreY, bandPeriod: h.bandPeriod,
          ratio: h.ratio, tooth: h.tooth, order: h.order, turn: h.turn, flank: h.flank,
          shade: h.shade, travel: h.travel,
          cssWidth: st.viewport.w, cssHeight: st.viewport.h, t: h.clock, reduced: st.reduced,
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

  // ---- what this pack declares --------------------------------------------------------------
  // The host reads this record and registers each instrument under the name its own manifest
  // carries. An instrument whose manifest asks for something the host cannot supply is refused
  // here with its reason, and the pack is refused whole: a stack missing a voice is a picture
  // nobody wrote.
  join({
    version: PACK_VERSION,
    instruments: [weaveInstrument(), matterInstrument(), gearsInstrument()],
  });
})();
