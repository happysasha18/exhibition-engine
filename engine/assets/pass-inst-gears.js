/*!pass-inst-gears.js*/
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

  var TAU = Math.PI * 2;

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
      // THE COVERAGE LAW (§7). `cov` is 1 for the points wheel A owns and 0 for the points wheel B
      // owns, so `1.0 - cov` is the territory of the ARRIVING wheel — this instrument's own matter.
      // The line where the two rims meet, which is what the eye actually sees here, is the boundary
      // of that territory. At the entry door the alpha is 0 at every point, so the instant the cue's
      // window opens the frame does not change; at the exit door it is 1 at every point, so the door
      // is this instrument's own whole work.
      //
      // THE COLOUR CHANNEL IS UNTOUCHED, which is what makes a one-cue score byte-identical: laid
      // down first the host disables blending and reads no alpha, so `col` reaches the frame exactly
      // as it always did. The blend is STRAIGHT source-over, never premultiplied — see the host.
      "  gl_FragColor = vec4(col, 1.0 - cov);",
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
      //
      // THE THREE HANDLES THAT TAKE A NUMBER OTHER THAN THE ONE THEY ARE HANDED, published here
      // beside their ranges by the same rule the woven instrument's band count is published by.
      //   · `ratio` — A PLACE ON A LADDER OF SEVEN RUNGS, never a number between them. ratioAt
      //     rounds it to a rung before any tooth count is taken, because a mesh closes on itself
      //     only at a ratio of small whole numbers. The seven pairs are RATIOS above, published here
      //     by reference so the ladder has one home, and `step` is the distance between two rungs.
      //   · `size` — ROUNDED TO WHOLE TEETH. Both counts come from one whole multiplier k, and the
      //     pair's drawn radii follow from the counts, so the size the frame draws is the nearest
      //     one that leaves the rung's ratio exact and each wheel at three teeth or more.
      //   · `tooth` and `order` — SCALED BACK TOGETHER. A tooth stands no taller than the wheel it
      //     stands on: while 2·amp + spread/2 asks for more than the field's own depth of
      //     2·min(R1,R2)·0.85 − 0.02, both are multiplied by one factor, which keeps their
      //     proportion and keeps both doors whole. At the module's own size nothing comes near it;
      //     at a small pair with a far-apart rung it binds.
      handles: {
        mix: { min: 0, max: 1, def: 0 },
        clock: { min: 0, max: 14, def: 0 },
        dial: { min: 0, max: 1, def: 0, open: true },
        size: { min: 0.3, max: 8, def: 4.5, applied: { roundedToWholeTeeth: true, leastTeeth: 3 } },
        centreX: { min: 0, max: 1, def: 0.5 },
        centreY: { min: 0, max: 1, def: 0.5 },
        bandPeriod: { min: 0.02, max: 1, def: 1 / 6 },
        ratio: { min: 0, max: 1, def: 0.5, kind: "enum", step: 1 / (RATIOS.length - 1),
                 rungs: RATIOS },
        tooth: { min: 0, max: 1, def: 0.4, applied: { scaledBackWith: "order" } },
        order: { min: 0, max: 1, def: 0.4, applied: { scaledBackWith: "tooth" } },
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
      // THE COVERAGE LAW (§7). The mask the shader already builds to decide which wheel owns each
      // point is published as the alpha: `1.0 - cov`, the share of the frame inside the arriving
      // wheel's rim. Both doors stay whole because `reachFor` solves the placement so that at either
      // door every corner of the frame lies inside ONE rim — so the alpha is 0 at every point at the
      // entry door and 1 at every point at the exit door, never a mixture.
      coverage: { writes: true,
                  how: "1.0 - cov, the share of the frame inside the arriving wheel's rim" },
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

  // ---- what this file declares --------------------------------------------------------------
  // The host registers this instrument under the name its own manifest carries, and refuses it when
  // that name disagrees with the name whose address this file was fetched from, when its version
  // disagrees, or when its manifest asks for something the host cannot supply.
  join({
    version: INSTRUMENT_VERSION,
    instrument: gearsInstrument(),
  });
})();
