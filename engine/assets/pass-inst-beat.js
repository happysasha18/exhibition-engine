/*!pass-inst-beat.js*/
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
// OWNERSHIP. This instrument was carried over from lab/effects/beat.js. The artistic instruments and
// their manifests belong to tlvphotos, which builds these files from its own sources; the engine's
// copies are what ships until that handover lands. The contract this file answers to is §7 and §8 of
// docs/design/PASS-API-V1.md, and the record that names it is the site's own `pass` block.
(function () {
  var join = window.__@@NS@@PassInstrument;
  if (typeof join !== "function") return;

  // THIS FILE'S OWN VERSION, and the one home of that fact. The build reads this literal out of the
  // source and writes it into the site's record beside the digest, so the version a file declares
  // and the version a host was told to load cannot drift apart without the build noticing.
  var INSTRUMENT_VERSION = "1.0.0";

  // ================================================================================================
  // THE INTERFERING INSTRUMENT (§8) — lab/effects/beat.js carried across
  // ================================================================================================
  // WHAT THE VISITOR SEES. Both photographs are read as wave fields — two fine gratings, one lying
  // flat across the frame and one standing nine degrees off it. The two periods travel toward each
  // other and pass, and where two nearly equal periods add they make a beat: large slow lobes
  // standing out of the two fast gratings. The crossing is a threshold walked across that field, so
  // the frame hands over one whole lobe at a time — broad soft shapes, born of the two rhythms
  // rather than of any pattern this instrument chose, sliding across the picture from one side to
  // the other. At the near door the first photograph stands whole and still; at the far door the
  // second does, and the two periods have exchanged places on the way.
  //
  // WHY A BEAT AND NOT A BLEND, in the module's own words (beat.js:7-12). Two gratings of nearly the
  // same period add to one product: cos A + cos B = 2·cos((A−B)/2)·cos((A+B)/2) — a fast carrier
  // inside a slow envelope. The envelope is not drawn anywhere: it is what the two periods DO to
  // each other, and it is the only structure in this module large enough to read as a shape.
  //
  // WHAT CAME OVER. The shader, character for character but for the three lines named below; the
  // seating of a work in the frame (`coverFit`, here `fit`); the measured response curve (FEEL_Q and
  // its dead bands of 0.055); the second grating's tilt, the counter-motion's amplitude and
  // the crop that pays for it, the two ends of the period range, and the numbers of one frame
  // (`frameValues`, here `posed`). Not one of those numbers changed.
  //
  // ONE OF THEM STOPPED BEING A CONSTANT AND BECAME A HANDLE: the tilt, `beatTilt` below, which
  // rests at the module's own nine degrees and is read from the angle the two works' own lattices
  // actually stand apart where a score fills it. His word of 2026-08-17 19:13, lifted to the class
  // at 19:21 — every geometric parameter derives from the work's own measured structure — and the
  // third picture here IS the two works' gratings interfering, so the angle they interfere at is
  // the pair's own fact rather than a number chosen before either photograph was looked at.
  //
  // WHAT STAYED BEHIND. Its own canvas, its own WebGL 1 context, its own frame loop, its resize
  // listener, its accumulated clock and its `seedFrom` fold. The clock is the `clock` handle the host
  // hands down and the die is the `seed` handle, already folded, exactly as the meshing and the
  // material instruments take theirs.
  //
  // THE THREE LINES OF THE SHADER THAT ARE NOT THE MODULE'S, each named with its reason.
  //   1. `uniform float uAspect;` is gone and the aspect is derived inside the shader from `uRes`,
  //      which the host already binds. The module computed it from the drawing buffer it owned; the
  //      host owns the buffer here, so the mathematics reads the buffer actually drawn into whatever
  //      the resolution ladder has done to it. The meshing and the material instruments did the same.
  //   2. `uniform float uMask;` and the one line that reads it are added. It is the fleet's judges'
  //      channel — the frame with this instrument's own coverage painted in place of the picture, so
  //      a law about the mask can be measured ON THE PICTURE rather than taken on the module's word.
  //      It rests at 0, where `mix(col, vec3(cov), 0.0)` is `col` exactly.
  //   3. `gl_FragColor = vec4(col, 1.0);` becomes `vec4(col, 1.0 - cov);` — THE COVERAGE LAW (§7).
  //      `cov` is 1 where the point still stands on the departing work's side of the travelling
  //      threshold, so `1.0 - cov` is the territory the ARRIVING work has taken, which is this
  //      instrument's own matter. The module had no stack to lie under and wrote a flat 1.
  function beatInstrument() {
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
      "uniform vec4 uFitA;",        // xy = scale into image uv, zw = pan
      "uniform vec4 uFitB;",
      "uniform vec2 uRes;",         // the drawing buffer the host binds
      "uniform vec2 uKA;",          // wave vector of the first field, cycles per frame height
      "uniform vec2 uKB;",
      "uniform vec2 uPhase;",       // the two fields' phases, in cycles
      "uniform float uTau;",        // the travelling threshold
      "uniform float uContrast;",   // 0 the raw sum owns the cut, 1 the slow envelope owns it
      "uniform float uSpread;",     // how far apart the lobes' own moments are set
      "uniform float uDPhase;",     // the two fields' phases differenced, in cycles
      "uniform float uSeed;",
      "uniform float uOff;",        // counter-motion, frame heights
      "uniform float uGuard;",      // the contact shadow's gate: nothing at either door
      "uniform float uMask;",       // the judges' channel: the coverage in place of the picture
      "const float PI = 3.14159265359;",

      // The sample is pushed by at most uOff, and the cover-fit was pulled in by exactly that
      // much (ZOOM in the script below), so the push always lands on picture. The clamp is the
      // backstop and half a texel of inset keeps the linear filter off the border.
      "vec2 into(vec2 p, vec4 f){",
      "  return clamp((p - 0.5) * f.xy + 0.5 + f.zw, 0.0008, 0.9992);",
      "}",
      "vec3 texA(vec2 p){ return texture2D(uA, into(p, uFitA)).rgb; }",
      "vec3 texB(vec2 p){ return texture2D(uB, into(p, uFitB)).rgb; }",

      "float hash11(float n){ return fract(sin(n * 127.1) * 43758.5453); }",

      "void main(){",
      "  vec2 uv = vUv;",
      // the aspect of the buffer the host drew into, read from the size the host binds
      "  float uAspect = uRes.x / max(uRes.y, 1.0);",
      // p is measured in frame HEIGHTS on both axes, so a period means the same thing whichever
      // way the grating lies and one pixel is the same length whichever way it is measured.
      "  vec2 p = vec2(uv.x * uAspect, uv.y);",
      "  float h = 1.0 / max(uRes.y, 1.0);",

      "  float eA = dot(uKA, p) + uPhase.x;",      // the two fields, in cycles
      "  float eB = dot(uKB, p) + uPhase.y;",
      "  float sA = sin(2.0 * PI * eA), cA = cos(2.0 * PI * eA);",
      "  float sB = sin(2.0 * PI * eB), cB = cos(2.0 * PI * eB);",
      // the sum of the two fields, and the slow envelope the two of them make between them
      "  float S = 0.5 * (cA + cB);",
      "  float E = cos(PI * (eA - eB));",
      "  vec2 gS = -PI * (uKA * sA + uKB * sB);",
      "  vec2 gE = -PI * (uKA - uKB) * sin(PI * (eA - eB));",
      // the beat's contrast: how much of the cut belongs to the slow envelope and how much to the
      // fast carrier the two gratings still carry inside it
      "  float M = mix(S, E, uContrast);",
      "  vec2 gM = mix(gS, gE, uContrast);",

      // WHICH LOBE THIS POINT BELONGS TO, and when that lobe hands over: six parts a ladder across
      // the frame, four parts the score's die. The offsets are held to nothing at both doors by
      // the same number that opens the threshold's travel, so a door stays a whole picture.
      //
      // THE LADDER IS THE LOBE'S OWN PLACE IN THE FRAME, not its number (the module's repair of
      // 13.08). The lobe NUMBER is counted along kA − kB, and that direction turns through the
      // crossing, so a ladder built on the number means a different thing at every mark. Reading the
      // lobe's CENTRE and taking where that centre stands across the frame gives a rung that holds
      // still while the field turns under it.
      "  vec2 kd = uKA - uKB;",
      "  float e = eA - eB;",
      "  float lobe = floor(e * 0.5);",
      "  float ec = (lobe + 0.5) * 2.0;",                 // the lobe's own centre line, in cycles
      // where that centre line stands ACROSS THE FRAME, read on this point's own row: the whole of
      // one lobe along one row therefore shares one rung. kd.x is −sin(9°)/periodB and never near
      // zero, so the row is always defined.
      "  float lx = (ec - uDPhase - kd.y * p.y) / kd.x;",
      "  float ladder = clamp(lx / max(uAspect, 0.05), 0.0, 1.0);",
      "  float ord = mix(ladder, hash11(lobe + uSeed), 0.4);",
      "  float tau = uTau + uSpread * (ord - 0.5);",

      // COVERAGE OVER THE PIXEL'S OWN FOOTPRINT: how much of this pixel stands above the
      // threshold, from the field's own gradient. Where the field is flat the answer is a plain
      // side, not a blend: the clamp takes it to 0 or 1.
      "  float grad = max(length(gM), 1e-5);",
      "  float d = (M - tau) / (grad * h);",
      "  float cov = clamp(0.5 + d, 0.0, 1.0);",

      // COUNTER-MOTION: the first work's content travels along its own grating, the second's
      // against its own — the two fields drift into each other.
      "  vec2 dA = uKA / max(length(uKA), 1e-5);",
      "  vec2 dB = uKB / max(length(uKB), 1e-5);",
      "  vec3 colA = texA(uv + vec2(dA.x / max(uAspect, 0.05), dA.y) * uOff);",
      "  vec3 colB = texB(uv - vec2(dB.x / max(uAspect, 0.05), dB.y) * uOff);",
      "  vec3 col = mix(colB, colA, cov);",

      // THE CONTACT SHADOW. The first work lies on top; the second one takes a shadow from that
      // edge, decaying exponentially into it. The reach is read in pixels so a boundary is the same
      // physical edge whatever the period is.
      "  float into2 = max(-d, 0.0);",                       // pixels below the boundary
      "  col *= 1.0 - 0.32 * uGuard * (1.0 - cov) * exp(-into2 / 7.0);",

      // THE JUDGES' CHANNEL. At rest this line is the identity; opened, the frame carries this
      // instrument's own coverage in place of the picture, so a law about the mask is measured on
      // the frame rather than taken on the instrument's word.
      "  col = mix(col, vec3(cov), uMask);",

      // THE COVERAGE LAW (§7). `cov` is 1 for the points the departing work owns and 0 for the
      // points the arriving one owns, so `1.0 - cov` is the ARRIVING work's territory — this
      // instrument's own matter. At the entry door the alpha is 0 at every point, so the instant the
      // cue's window opens the frame does not change; at the exit door it is 1 at every point, so
      // the door is this instrument's own whole work.
      //
      // THE CONTACT SHADOW SURVIVES A STACK, and that is worth saying beside the material
      // instrument, whose shadow does not. The shadow above rides `(1.0 - cov)` — it lies on the
      // arriving work's side, which is exactly the territory this alpha keeps — so a cue played over
      // another still carries its own contact edge.
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
    function num(v, d) { var n = Number(v); return n === n ? n : d; }
    function len2(x, y) { return Math.sqrt(x * x + y * y); }

    // THE SECOND GRATING'S ANGLE against the first, in degrees (beat.js:224-230), which the module
    // pins and this port PUBLISHES AS A HANDLE. The module's own words for why it may never be
    // zero: with two collinear gratings of equal period the envelope goes flat over the whole frame
    // and the picture would flip whole at mid-handle, which is the one thing a crossing may never
    // do. At nine degrees the difference of the two wave vectors never falls below 2·sin(4.5°) =
    // 0.157 of a wave vector, so mid-handle the frame still holds a few large, slow, finite lobes.
    //
    // WHY IT BECOMES A HANDLE, AND THAT THE LAB MODULE HAS NONE IS NOT A REASON TO HOLD BACK. His
    // word of 2026-08-17 19:13, lifted to the class at 19:21: every geometric parameter derives from
    // the work's own measured structure. A pinned nine degrees is a relationship between two
    // photographs' gratings decided before either photograph was looked at. THE ANGLE THE TWO WORKS'
    // OWN LATTICES ACTUALLY STAND APART is that same relationship, measured — and the third picture
    // here IS the two works' gratings interfering, so the angle they interfere at should be theirs.
    // `beatTilt` is the name, because the composer's register already spends `tilt` on another
    // instrument and two measurements under one name is the collision the register exists to stop.
    //
    // THE DEFAULT IS THE MODULE'S OWN NINE, so a score that names no track for it draws exactly the
    // frame the module drew, to the pixel.
    var BEAT_TILT = 9;
    // THE TWO ENDS OF THE ANGLE. The ceiling is 90° because a lattice angle is a LINE direction,
    // defined only up to half a turn, so two grating families never stand more than a right angle
    // apart — a fill reading the two records folds `|angleA − angleB| mod 180` back under 90 and
    // lands inside this span by construction. The floor of 1° is mine and is named as mine in the
    // report: below it the two wave vectors differ by under 2·sin(0.5°) = 0.017 of a wave vector, so
    // at mid-handle the frame holds well under one lobe and the picture flips whole; it is also what
    // keeps `kd.x` — the shader's own divisor when it reads which rung a lobe stands on — away from
    // zero, at −sin(1°)/P_MAX = 0.053 or steeper.
    var TILT_MIN = 1, TILT_MAX = 90;

    // HOW FAR THE CONTENT TRAVELS, in frame heights, and the crop that pays for it (beat.js:232-236).
    // Every sample is the frame coordinate pushed by at most AMP, so the cover-fit is pulled in by
    // AMP at each end; ZOOM follows from AMP and is not a free number.
    var AMP = 0.055;
    var ZOOM = 1 + 2 * AMP + 0.03;

    // THE PERIODS THE HANDLES' DOORS STAND AT, in frame heights (beat.js:238-243). The floor is set
    // by the eye and not by the arithmetic: below about a fortieth of the frame a grating of these
    // photographs stops reading as a cut and starts reading as hatching. The ceiling is a third of
    // the frame: coarser than that and there are not enough periods left in the frame to beat at all.
    var P_MIN = 0.025, P_MAX = 0.33;

    // HOW FAR PAST THE FIELD'S OWN RANGE AND THE LOBES' OWN SPREAD THE THRESHOLD TRAVELS
    // (beat.js:391, `reach = 1 + spread * 0.5 + 0.04`). The field runs from −1 to +1 and the lobes'
    // moments are spread by at most half the spread either way, so a threshold a MARGIN below −1
    // leaves every point of the frame on the departing work's side and a MARGIN above +1 leaves
    // every point on the arriving one's. That hair is the margin either door stands on, and it is
    // the number the reading below is held against. Named here because it is read in two places.
    var MARGIN = 0.04;

    // cover-fit a work into the frame, then pull in by the counter-motion's headroom. The host hands
    // the source's own dimensions, so the instrument never touches an image object.
    function fit(iw, ih, w, h) {
      var fa = w / Math.max(h, 1);
      var ia = iw / Math.max(ih, 1);
      var sx, sy;
      if (ia > fa) { sx = fa / ia; sy = 1; } else { sx = 1; sy = ia / fa; }
      return [sx / ZOOM, sy / ZOOM, 0, 0];
    }

    /* THE RESPONSE CURVE, MEASURED AND NOT NAMED (beat.js:307-342, the module's re-fit of
       2026-08-13), carried digit for digit; the port re-derives nothing. How far the picture moves
       per unit of the RAW handle was measured with the curve taken out of the module — forty steps
       of 0.025, the mean channel difference between neighbouring frames — that rate was integrated,
       and the curve is the INVERSE of the integral, so the hand's own value is the share of the
       whole change. FEEL_Q is that inverse at twenty-one evenly spaced shares, straight lines
       between them.

       THE DEAD BANDS of 0.055 at both ends are what the contract publishes for this module: the hand
       is SPENT there — the dial stands at exactly 0 across the first band and at exactly 1 across the
       last — so a whole picture is whole to the pixel and a judge can measure it as nothing moving.

       WHAT THE RATE LOOKS LIKE HERE, measured on the lab pair: about 17.5 channels a step at the
       near end, 25 across the first half, a NOTCH of 9.9 exactly where the two periods pass, and 8.0
       at the far end. The notch is the module's own physics: where the periods cross there is about
       one lobe across the whole frame, so a step of the handle moves one broad boundary instead of a
       dozen. The curve races the hand through the notch. The rate was measured on the lab's own pair
       at the module's default handles, so another pair shifts the curve a little and the honest
       re-fit is another run of the same measurement. */
    var FEEL_D0 = 0.055;
    var FEEL_Q = [0, 0.0556, 0.1101, 0.1589, 0.2019, 0.2412, 0.2794, 0.3185, 0.3596, 0.403,
                  0.4501, 0.5068, 0.5589, 0.6043, 0.6496, 0.6908, 0.7323, 0.7759, 0.8249,
                  0.8933, 1];
    function feelOf(u) {
      var x = clamp((u - FEEL_D0) / (1 - 2 * FEEL_D0), 0, 1);
      var s = x * (FEEL_Q.length - 1), i = Math.min(FEEL_Q.length - 2, Math.floor(s));
      return FEEL_Q[i] + (FEEL_Q[i + 1] - FEEL_Q[i]) * (s - i);
    }

    function periodOf(v) { return P_MIN + (P_MAX - P_MIN) * clamp(v, 0, 1); }

    // WHERE THE TWO PERIODS STAND AT THIS DIAL (beat.js:365-368). They travel toward each other and
    // PASS: at the first door the first work's grating is fine and the second's coarse, at
    // mid-handle they are one period apart in name and only the fixed tilt keeps them apart in fact,
    // and at the far door each stands where the other started.
    function periodsAt(d, pa, pb) { return [pa + (pb - pa) * d, pb + (pa - pb) * d]; }

    // THE TWO WAVE VECTORS AT THIS DIAL, and how many lobes stand across the frame (beat.js:372-382).
    // The first grating lies flat; the second stands aslant by the tilt, which is what keeps the
    // difference of the two vectors finite where the two periods cross. The module read its own
    // pinned BEAT_TILT here; this reads the angle handed in, which rests at that same nine degrees.
    function wavesAt(pp, aspect, tiltDeg) {
      var a = tiltDeg * Math.PI / 180;
      var kAx = 0, kAy = 1 / pp[0];
      var kBx = Math.sin(a) / pp[1], kBy = Math.cos(a) / pp[1];
      var dx = kAx - kBx, dy = kAy - kBy;
      var reach = len2(dx, dy);
      return { kA: [kAx, kAy], kB: [kBx, kBy],
               n: Math.max(1, reach * Math.sqrt(aspect * aspect + 1) * 0.5) };
    }

    // The grid a door is read on, and which of the two it is. `drawn` says which one the sentence
    // below names, since a reader told «a 390 x 220 frame» would look for a device that has none.
    function doorGridOf(st) {
      var bw = Math.round(num(st.bufWidth, 0)), bh = Math.round(num(st.bufHeight, 0));
      if (bw >= 1 && bh >= 1) return { w: bw, h: bh, drawn: true };
      return { w: Math.round(num(st.cssWidth, 0)), h: Math.round(num(st.cssHeight, 0)),
               drawn: false };
    }

    // THE NUMBERS OF ONE FRAME (beat.js:384-415). Everything the shader gets beyond the seating of
    // the two works is a pure function of the pose. The two door periods are parameters here rather
    // than read straight off the pose, because the hold in `values` below asks this same function
    // for the same pose at a neighbouring pair. Nothing else about it moved.
    function posed(st, pa, pb, aspect) {
      var d = feelOf(clamp(num(st.mix, 0), 0, 1));
      var pp = periodsAt(d, pa, pb);
      // THE ANGLE THE TWO GRATINGS INTERFERE AT, the pair's own where a score names it and the
      // module's pinned nine where none does.
      var tilt = clamp(num(st.beatTilt, BEAT_TILT), TILT_MIN, TILT_MAX);
      var w = wavesAt(pp, aspect, tilt);
      var spread = clamp(num(st.lead, 0), 0, 1) * 0.9;
      // The threshold's own reach: past the field's range by half the lobes' spread and a hair
      // more, so at a door EVERY lobe stands whole on the same side. This is the number that makes
      // the dead bands dead.
      var reach = 1 + spread * 0.5 + MARGIN;
      var tau = -reach + 2 * reach * d;
      // The counter-motion is at its widest in the middle and nothing at either door, so a door is
      // the picture the file carries and not the picture pushed a hair off its place.
      var travel = AMP * 4 * d * (1 - d);
      /* THE PHASE IS READ ON THE DIFFERENCE OF THE TWO FIELDS, not on both of them at once
         (beat.js:396-403): it pushes the first field forward and the second back by the same amount,
         exactly as the drift does. Pushed both the same way, the beat's envelope — which is a
         function of the DIFFERENCE — would not move at all and the handle's two doors would stand on
         one picture; measured, that arrangement moved the frame by half a channel. A quarter of a
         cycle each way is half a cycle of the difference, which walks the envelope from a lobe to
         the gap between two lobes and no further. */
      var ph = clamp(num(st.phase, 0), 0, 1) * 0.25;
      // The two fields drift INTO each other on the handed clock: the first forward along its own
      // direction, the second backward along its own. The module accumulated its own frame time
      // here; this reads the `clock` handle, so a seeded score repeats to the pixel.
      var drift = (st.reduced ? 0 : num(st.t, 0)) * 0.035;
      var phases = [ph + drift, -ph - drift];
      return {
        dial: d, tau: tau, spread: spread,
        kA: w.kA, kB: w.kB, lobes: w.n,
        // read on the diagnostic surface and bound to no uniform: the angle the two gratings
        // actually interfered at, so a plan can be read back against the pair it was filled from
        tilt: tilt,
        periodA: pp[0], periodB: pp[1],
        phase: phases,
        dphase: phases[0] - phases[1],
        contrast: clamp(num(st.contrast, 0), 0, 1),
        off: travel * clamp(num(st.travel, 1), 0, 1),
        // the shadow's gate: nothing at either door, where one work stands whole
        guard: clamp(num(st.shade, 1), 0, 1) * smoothstep(0, 0.09, d) * smoothstep(1, 0.91, d),
      };
    }

    // ---- THE DOOR THE INSTRUMENT READS FOR ITSELF ------------------------------------------------
    // His 18:00 architecture decision of 2026-08-17, carried in the U27 brief: the instrument reads
    // its doors at runtime on the actual buffer, and the report it hands back is the runtime truth;
    // what the manifest declares is only the claim. The meshing instrument answered that first and
    // the material one in its own units; this is the same law read in THIS instrument's units, which
    // are its GRATINGS — the count of the finer field's periods across the frame's height.
    //
    // WHAT A DOOR ASKS OF THIS INSTRUMENT, written out. The mask is
    //     cov = clamp(0.5 + (M − τ) / (grad · h)),   grad = |∇M|,   h = 1 / uRes.y,
    // so at the entry door `cov` is 1 at every point exactly while, everywhere on the frame,
    //     (M − τ) ≥ 0.5 · |∇M| · h.
    // At that door τ never rises above −(1 + MARGIN), because the threshold stands at −reach and the
    // lobes' own spread moves it by at most half the spread; so it is enough that
    //     (1 + M) + MARGIN ≥ 0.5 · |∇M| · h        at every point of the frame.
    // The exit door is the same statement with (1 − M) in place of (1 + M), by the same arithmetic
    // read from the other end, so ONE condition answers both doors.
    //
    // THE CONDITION, SOLVED RATHER THAN SAMPLED. Write the two fields as α = 2π·eA, β = 2π·eB and
    // φ = π·(eA − eB), and let u = |cos(α/2)|, v = |cos(β/2)|, w = |cos(φ/2)|. Then
    //     1 + S = u² + v²,        1 + E = 2w²,
    //     |∇S| ≤ 2π·(Ka·u + Kb·v),   |∇E| ≤ 2π·Kd·w,
    // where Ka, Kb are the two wave vectors' lengths and Kd is the length of their difference. With
    // the contrast c mixing the two, the condition becomes
    //     (1−c)(u² + v²) + 2c·w² + MARGIN ≥ π·h·[(1−c)(Ka·u + Kb·v) + c·Kd·w],
    // and minimising the three terms independently — which can only ever OVER-hold, since u, v and w
    // are not free of one another — leaves one number to compare against the margin:
    //     (π·h)² · [ (1−c)(Ka² + Kb²)/4 + c·Kd²/8 ]  ≤  MARGIN.
    // That left side is `doorReach` below: how far this instrument's own mask reaches past the
    // field's own extreme, in the field's own units, on the buffer being drawn. It costs a handful
    // of multiplications, it is exact in form rather than sampled, and the door it calls whole is
    // whole beyond argument.
    //
    // WHY THE BUFFER ENTERS AT ALL. `h` is one buffer row, so the mask crosses over inside a band of
    // the field HALF THE FIELD'S OWN SLOPE PER BUFFER ROW wide. The slope is set by the PERIODS, and
    // the buffer's height is what turns a period into rows. So periods whole on a tall buffer are a
    // leak on a short one — the same class the meshing instrument found at its singular point, in
    // this instrument's own numbers.
    function doorReachOf(v, h) {
      var Ka = len2(v.kA[0], v.kA[1]), Kb = len2(v.kB[0], v.kB[1]);
      var Kd = len2(v.kA[0] - v.kB[0], v.kA[1] - v.kB[1]);
      var c = v.contrast, ph = Math.PI * h;
      return ph * ph * ((1 - c) * (Ka * Ka + Kb * Kb) / 4 + c * Kd * Kd / 8);
    }

    // THE DOOR, MEASURED. Null everywhere but at a door, since away from the doors a travelling beat
    // is the picture rather than a fault. The door is named by the manifest's own `doors` block:
    // `mix` at 0 is the entry door, where the frame is the departing work whole, and `mix` at 1 the
    // exit door, where it is the arriving one.
    function doorReadOf(v, st) {
      var want = st.mix === 0 ? 1 : (st.mix === 1 ? 0 : -1);
      if (want < 0) return null;
      var g = doorGridOf(st);
      if (!(g.w >= 1) || !(g.h >= 1)) return null;
      var h = 1 / g.h;
      return { grid: g, want: want, reach: doorReachOf(v, h),
               // the two fields as the eye would count them: gratings across the frame's height
               gratingsA: 1 / v.periodA, gratingsB: 1 / v.periodB };
    }

    // THE REFUSAL, worded the way the host's own manifest refusals read: what is wrong, in this
    // instrument's own measured numbers, on the grid it was measured on.
    function doorWhyNoOf(read) {
      if (!read || read.reach <= MARGIN) return null;
      var g = read.grid;
      return (read.want ? "the entry" : "the exit") + " door leaks: at periods of "
           + read.gratingsA.toFixed(2) + " and " + read.gratingsB.toFixed(2)
           + " gratings across the frame's height on a " + g.w + " x " + g.h
           + (g.drawn ? " buffer" : " frame") + ", this instrument's own mask reaches "
           + read.reach.toFixed(4) + " of the field past the field's own extreme, past the "
           + MARGIN + " the threshold stands beyond that extreme and the lobes' own spread, and the "
           + (read.want ? "arriving" : "departing")
           + " work takes the points of the frame nearest that crossing, where "
           + (read.want ? "the entry" : "the exit") + " door's own law asks for the "
           + (read.want ? "departing" : "arriving") + " work at every point";
    }

    // HOW FAR «NEAR» REACHES, and why it is two gratings. This instrument's own unit is the grating
    // — one period of the finer of the two fields across the frame's height — so that is the unit
    // the distance is counted in. Two gratings of a field that stands anywhere from three to forty
    // across the height is a step of the pattern nobody watching a door can see, because at a door
    // the frame is one whole work and no grating of it is on screen; beyond two gratings the pose the
    // score asked for is genuinely a different rhythm and the refusal is the honest answer. A guard
    // that never refuses proves nothing.
    var DOOR_HOLD = 2;

    // THE NUMBERS OF ONE FRAME, WITH ITS DOOR HELD WHOLE ON THE BUFFER BEING DRAWN. Away from a door
    // this is `posed` and nothing more: the reading is taken nowhere else and no period moves. At a
    // door whose periods cross the mask over inside the frame on the buffer being drawn, the
    // instrument steps to a COARSER whole grating — the only direction that closes it, since the
    // field's slope rises as the periods fall — and answers with the first pose whose door is whole.
    //
    // BOTH PERIODS ARE SCALED BY ONE FACTOR, and that is the whole of the hold. The beat is made of
    // the RATIO of the two periods; scaling both together scales the whole construction and leaves
    // that ratio exact, so the lobes keep their shape and only their size moves. Scaling one alone
    // would change the beat itself, which is the one thing a hold may not do.
    //
    // What the score asked for and what was applied are both on the record: `periodA`/`periodB` are
    // the periods drawn, `periodRequestA`/`periodRequestB` the ones handed in, `periodGratings` says
    // how many whole gratings apart they stand, and `doorHeld` carries the leak the request would
    // have drawn, in its own words.
    function values(st) {
      var g = doorGridOf(st);
      var aspect = (g.w >= 1 && g.h >= 1) ? g.w / g.h : 1;
      var pa = periodOf(num(st.periodA, 0)), pb = periodOf(num(st.periodB, 0));
      var v = posed(st, pa, pb, aspect);
      v.periodRequestA = v.periodA;
      v.periodRequestB = v.periodB;
      v.periodGratings = 0;
      v.doorHeld = null;
      var read = doorReadOf(v, st);
      var no = doorWhyNoOf(read);
      v.doorGrid = read ? read.grid : null;
      v.doorReach = read ? read.reach : null;
      if (!no) { v.doorWhyNo = null; return v; }
      // the finer of the two fields, counted in whole gratings across the frame's height
      var fine = Math.min(v.periodA, v.periodB);
      var rung = Math.floor(1 / fine);
      for (var step = 0; step <= DOOR_HOLD; step++) {
        var nTry = rung - step;
        if (nTry < 1) continue;
        var scale = (1 / nTry) / fine;
        if (!(scale > 1)) continue;                 // only coarser closes it
        var w = posed(st, pa * scale, pb * scale, aspect);
        var wRead = doorReadOf(w, st);
        if (doorWhyNoOf(wRead)) continue;
        w.periodRequestA = v.periodA;
        w.periodRequestB = v.periodB;
        w.periodGratings = 1 / fine - nTry;
        w.doorHeld = no;
        w.doorWhyNo = null;
        w.doorGrid = wRead.grid;
        w.doorReach = wRead.reach;
        return w;
      }
      v.doorWhyNo = no + ", and no whole grating stands within " + DOOR_HOLD
                  + " gratings of the periods handed in";
      return v;
    }

    var manifest = {
      id: "beat", api: 1, arity: 2,
      // The departing work loses lobe after lobe, the middle is a field belonging to neither, and
      // the arriving work gathers lobe by lobe out of the same field.
      roles: ["disassembly", "mystery", "assembly"],
      // WHERE THIS STANDS ON THE CHARTER'S SHELF: SURFACE, which is what the module's own contract
      // row publishes for it (lab/data/module-contract-new.json, `beat`.level). One field runs over
      // the whole frame and its value at a point decides whose that point is; no cell of the frame
      // lives a life of its own. TEXTURE is not claimed — the gratings shape the boundary between
      // the two works and never touch either work's own material.
      levels: ["SURFACE"],
      // WHAT IT CUTS ON. STRIPS, because a grating is a band family and the lobes hand over along
      // the two gratings' own direction; and SCALES, because which lobes there are at all is settled
      // by the two works' own measured periods — the beat is the difference between two rhythms, and
      // a rhythm is a scale. Both kinds stand in the composer's own vocabulary: `banding` maps to
      // `strip` and `texture` to `scale` in its `KIND_OF_MEASURE`.
      cuts: ["strip", "scale"],
      params: { periodA: [0, 1], periodB: [0, 1], phase: [0, 1], contrast: [0, 1], lead: [0, 1],
                beatTilt: [TILT_MIN, TILT_MAX] },
      // EVERY handle a score can drive (§4.4b). `mix` is the dial — the module's one travelling
      // number, hidden from its declared params so no page grows a slider the score would fight
      // with. `clock` is the second the host hands down. The five below them are the module's own
      // declared params at the module's own defaults. `seed` is its die, `shade` and `travel` the two
      // judge channels it keeps for measuring a law on the picture — the frame with the contact
      // shadow against the frame without it, and the same for the counter-motion — and `mask` is the
      // fleet's own judges' channel, which the module has none of.
      //
      // NO HANDLE HERE KEEPS A CLOCK OR A ROLL OF ITS OWN. The module read time in one place, the
      // drift of the two fields at `t * 0.035` (beat.js:407), where `t` was its own accumulated frame
      // time; that reads the `clock` handle here. The die was folded at creation by `seedFrom`; the
      // `seed` handle arrives already folded, exactly as the meshing and the material instruments
      // take theirs. So a seeded score repeats to the pixel.
      //
      // ONE HANDLE OF THE MODULE DOES NOT CROSS, and it is named rather than dropped: `photo`, which
      // chose which of the mount's pictures stood as the second work. A cue carries an ORDERED pair
      // and owes a door at each end, so which work stands where is the passage's own question and
      // never a handle. The spiral instrument's port names the same absence for the same reason.
      //
      // WHAT STAYS PINNED, AND WHY EACH ONE DOES. The module's every other geometric and temporal
      // number was swept for a reading of the two works that could honestly set it, and one of them
      // had one — the tilt, now `beatTilt`. These did not, and a handle nothing can fill is a
      // handle a score walks without knowing what it is walking:
      //   · `AMP` = 0.055, how far the content drifts along its own grating. A distance, and no
      //     reading of a photograph says how far its own content should travel. The `travel`
      //     channel already scales it end to end, so a score that wants it moved can move it.
      //   · `ZOOM` = 1 + 2·AMP + 0.03, and it is not free: it is the crop AMP obliges, derived.
      //   · `P_MIN`/`P_MAX` = 0.025 / 0.33 — not a value but the SPAN the two period handles are
      //     read onto, which is where the pair's own measured rhythms land. The module sets both by
      //     the eye: finer than a fortieth of the frame a grating reads as hatching rather than as
      //     a cut, coarser than a third there are not enough periods left in the frame to beat.
      //   · `MARGIN` = 0.04 and the smoothstep gates at 0.09 / 0.91 — the door's own construction.
      //     Moving either would make a door a mixture, which is the one thing it may never be.
      //   · `FEEL_D0` = 0.055 and the twenty-one knots of `FEEL_Q` — a MEASUREMENT already, of this
      //     module on the lab's own pair. The honest way to move it is another run of that same
      //     measurement on another pair, never a score row.
      //   · 0.9 and 0.25 — the spans the `lead` and `phase` handles are read onto, both derived:
      //     0.9 is what carries the lobes' moments across the threshold's own range, and a quarter
      //     of a cycle each way is half a cycle of the DIFFERENCE, which walks the envelope from a
      //     lobe to the gap between two and no further.
      //   · 0.035, how fast the two fields drift into each other per second, and 0.32 / 7.0, the
      //     contact shadow's weight and its reach in pixels. All three are rates and weights of the
      //     instrument's own hand, and nothing measured of a photograph sets them; `clock` and
      //     `shade` scale them where a score wants them moved.
      handles: {
        mix: { min: 0, max: 1, def: 0 },
        clock: { min: 0, max: 14, def: 0 },
        // THE TWO PERIODS, AND THE SPAN THAT SAYS WHAT THEY MEAN. A range of 0…1 is a place, not a
        // length, and a fill holding the two works' own measured periods — `spectralPeriodPx` over
        // `frameSide`, which is already a share of a frame — has nothing to map that share onto
        // without the span. So the span travels with the handle: `frameHeights` is `[P_MIN, P_MAX]`
        // BY REFERENCE, the way the meshing instrument publishes its ladder of ratios, so the two
        // ends have one home and a composer and this file cannot come to hold different numbers for
        // them. `periodOf` above is the whole of the mapping: P_MIN + (P_MAX − P_MIN) · handle.
        //
        // WHICH WORK EACH READS is the module's own construction and not a choice here: the two
        // periods TRAVEL toward each other and pass, so the first field starts at the departing
        // work's own rhythm and ends at the arriving work's, and the second does the reverse
        // (`periodsAt`). Filling them from the two works therefore makes the crossing the two
        // rhythms passing through one another, which is what the beat is.
        periodA: { min: 0, max: 1, def: 0.14,
                   unit: "a position on the span below, in frame heights",
                   frameHeights: [P_MIN, P_MAX],
                   reads: { of: "the departing work",
                            paths: ["texture.spectralPeriodPx", "frameSide"],
                            how: "the work's own measured period said as a share of its own frame "
                               + "side, placed on this handle's own span in frame heights" } },
        periodB: { min: 0, max: 1, def: 0.42,
                   unit: "a position on the span below, in frame heights",
                   frameHeights: [P_MIN, P_MAX],
                   reads: { of: "the arriving work",
                            paths: ["texture.spectralPeriodPx", "frameSide"],
                            how: "the work's own measured period said as a share of its own frame "
                               + "side, placed on this handle's own span in frame heights" } },
        phase: { min: 0, max: 1, def: 0 },
        // THE MEASUREMENT THE PERIODS ARE READ AGAINST AT A DOOR, published beside the range of the
        // handle that sets the field's steepness. `heldWholeAtADoor` says what is read (how far this
        // instrument's own mask reaches past the field's extreme, held against the margin the
        // threshold stands beyond it), on which grid (the drawing buffer the host binds, with the
        // CSS frame where it hands none), how far the hold reaches (two whole gratings of the finer
        // field) and where the request the score handed in stays on the record.
        contrast: { min: 0, max: 1, def: 0.82,
                    applied: { heldWholeAtADoor: { gratings: DOOR_HOLD,
                                                   readOn: "the drawing buffer",
                                                   reads: "periodRequestA",
                                                   measures: "how far this instrument's own mask "
                                                           + "reaches past the field's own extreme, "
                                                           + "against the margin the threshold "
                                                           + "stands beyond that extreme" } } },
        lead: { min: 0, max: 1, def: 0.6 },
        // THE ONE HANDLE THIS PORT PUBLISHES THAT THE MODULE HELD AS A CONSTANT, and the
        // measurement it names, published beside its range the way the meshing instrument publishes
        // its own. `reads` says which reading of a WORK RECORD sets it and how the two are put
        // together: the angle between the two works' own lattices, which is `structure.ownDevice.
        // angleDeg` where a step was recovered and `structure.grid.angleDeg` where none was — the
        // same order of preference the composer's own `latticeAngleDeg` already reads them in. Two
        // line directions, so the difference folds back under a right angle and lands inside this
        // handle's span by construction. `def` is the module's pinned nine, so a score naming no
        // track for it draws the module's own frame to the pixel.
        beatTilt: { min: TILT_MIN, max: TILT_MAX, def: BEAT_TILT, unit: "degrees",
                    reads: { of: "both works", paths: ["structure.ownDevice.angleDeg",
                                                       "structure.grid.angleDeg"],
                             how: "the angle between the two works' own measured lattices — "
                                + "|angleA - angleB| taken modulo half a turn and folded back "
                                + "under a right angle, since a lattice angle is a line direction "
                                + "and two grating families never stand further apart than that" } },
        seed: { min: 0, max: 8, def: 0 },
        shade: { min: 0, max: 1, def: 1 },
        travel: { min: 0, max: 1, def: 1 },
        mask: { min: 0, max: 1, def: 0 },
      },
      // The dial's two ends, as the module's contract row words them. At 0 the threshold stands a
      // margin below the field's whole range, so every point of the frame is the first work standing
      // whole and still — the picture the file carries, cover-fit and centre-cropped by the headroom
      // the counter-motion needs. At 1 it stands a margin above, so every point is the second work,
      // framed the same way; the two periods have exchanged places on the way. The counter-motion
      // and the contact shadow are both nothing at either end.
      neutrals: { a: 0, b: 1 },
      doors: { in: { handle: "mix", value: 0, work: "a" },
               out: { handle: "mix", value: 1, work: "b" } },
      // Both doors frame alike: the crop the counter-motion's headroom is paid for with is a
      // constant, while the motion itself dies at both ends. 1.14, which is the module's own ZOOM and
      // the number its contract row publishes.
      framings: { "0": { coverCrop: ZOOM }, "1": { coverCrop: ZOOM } },
      drivers: ["progress", "cueProgress", "time", "velocity", "capability", "noise", "static",
                "curve", "spline", "map", "add", "multiply", "mix", "clamp", "hold", "segment",
                "ramp", "slew", "oscillate", "node"],
      // The construction moves no point of view: it decides which work owns each point of the frame
      // and drifts the two works along their own gratings inside it. Both are what it does to its own
      // surface, so the witness camera stays the stage's (§6).
      camera: { needs: "none", authority: "stage" },
      gl: { preserveDrawingBuffer: false },
      // THE COVERAGE LAW (§7). The mask the shader already builds from the travelling threshold is
      // published as the alpha: `1.0 - cov`, the share of the arriving work. The threshold travels a
      // margin past either end of the field, so at the entry door every point stands on the departing
      // work's side and the alpha is 0 at every point, and at the exit door every point stands on the
      // arriving one's and the alpha is 1 at every point.
      coverage: { writes: true,
                  how: "1.0 - cov, the share of the arriving work at the travelling threshold" },
      // The neutral pose is the ENTRY DOOR — `mix` at 0, the value the `doors` block above names —
      // so the frame keys the host reads off it at registration include the door's own record.
      neutralPose: { mix: 0, periodA: 0.14, periodB: 0.42, phase: 0, contrast: 0.82, lead: 0.6,
                     beatTilt: BEAT_TILT, seed: 0, shade: 1, travel: 1, mask: 0, t: 0,
                     reduced: false, cssWidth: 1000, cssHeight: 1000 },
      passes: [{
        program: "beat", vert: VERT, frag: FRAG, position: "aPos",
        uniforms: [
          { name: "uA", type: "sampler2D", source: "textureA" },
          { name: "uB", type: "sampler2D", source: "textureB" },
          { name: "uFitA", type: "vec4", source: "fitA" },
          { name: "uFitB", type: "vec4", source: "fitB" },
          { name: "uRes", type: "vec2", source: "resolution" },
          { name: "uKA", type: "vec2", source: "frame:kA" },
          { name: "uKB", type: "vec2", source: "frame:kB" },
          { name: "uPhase", type: "vec2", source: "frame:phase" },
          { name: "uTau", type: "float", source: "frame:tau" },
          { name: "uContrast", type: "float", source: "frame:contrast" },
          { name: "uSpread", type: "float", source: "frame:spread" },
          { name: "uDPhase", type: "float", source: "frame:dphase" },
          { name: "uOff", type: "float", source: "frame:off" },
          { name: "uGuard", type: "float", source: "frame:guard" },
          { name: "uSeed", type: "float", source: "handle:seed" },
          { name: "uMask", type: "float", source: "handle:mask" },
        ],
      }],
      // The instrument allocates nothing of its own: it spends the two source-texture slots the host
      // already holds and the one programme the host builds from this manifest.
      resources: { lean: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                           passes: 1, bytesEstimate: 0, variant: "lean" },
                   standard: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0,
                               programs: 1, passes: 1, bytesEstimate: 0, variant: "standard" },
                   rich: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                           passes: 1, bytesEstimate: 0, variant: "rich" } },
      capabilities: ["webgl2"],
      decline: ["one work only", "a source that never decoded"],
      provenance: { labPath: "lab/effects/beat.js", commit: "e0f1b91" },
      // HOW WELL THIS INSTRUMENT SUITS A PAIR (2026-08-18, his word of 09:51 and its sharpening at
      // 09:53). An instrument no longer answers WHETHER it takes a pair — it answers how well it
      // suits one, so a poor fit is still playable and still explains itself. The arithmetic runs in
      // the composer, which is the one place holding both records; what stands here is the
      // instrument's own statement of WHAT IT READS, which is the fact this file owns.
      //
      // RANKING ONLY, AND NEVER A FLOOR. Charter shelf 10 says it in his own struck-and-restated
      // words: near-matched rhythms rank this shelf high for a pair and NEVER ADMIT IT. Any two
      // photographs get a crossing on this instrument; the reading only says how much the third
      // picture will be the two works' own interference rather than a pattern laid over them.
      suits: { reads: ["texture.spectralPeriodPx", "frameSide"],
               how: "the third picture here is the two works' interference, so it suits a pair whose "
                  + "own measured rhythms stand near one another — two nearly equal periods make the "
                  + "large slow lobes this instrument hands the frame over in, while two far-apart "
                  + "periods leave lobes no coarser than the gratings themselves; a whole fit is two "
                  + "works whose spectral periods, read as counts across their own frames, coincide, "
                  + "and a fit of nothing is a pair standing at opposite ends of the range, which "
                  + "still plays and reads as a fine fast handover" },
      readiness: "production-ready",
    };

    var live = false;
    return {
      name: "beat",
      manifest: manifest,
      values: values,
      fit: fit,
      feel: feelOf,
      prepare: function (o) {
        if (!o.sources) return { take: false, why: "the interfering instrument needs both works" };
        if (!o.cue) return { take: false, why: "no cue names it" };
        return { take: true };
      },
      start: function () { live = true; },
      // The pose the shader draws. Every number in it comes from a handle a score can drive, and the
      // two fields' drift reads the second the host hands down, so a seeded run repeats to the pixel.
      //
      // A DOOR THIS INSTRUMENT CANNOT KEEP WHOLE IS REFUSED RATHER THAN DRAWN. The door law is the
      // instrument's own claim (the manifest's coverage line above), so the instrument is what
      // answers for it: at either door it reads its own field on the buffer the host is about to
      // bind and, where the periods cross the mask over inside the frame there and no whole grating
      // within reach closes it, hands the host the reason with the measured reach in it instead of
      // drawing a door that is two works at once. The host recovers the transaction on that reason
      // and the walk's own glide carries the visitor, which is the product's own behaviour with no
      // renderer.
      frame: function (st) {
        if (!live) return;
        var h = st.handles;
        var pose = {
          mix: h.mix, periodA: h.periodA, periodB: h.periodB, phase: h.phase,
          contrast: h.contrast, lead: h.lead, beatTilt: h.beatTilt,
          shade: h.shade, travel: h.travel, seed: h.seed, mask: h.mask,
          t: h.clock, reduced: st.reduced,
          cssWidth: st.viewport.w, cssHeight: st.viewport.h,
          // THE GRID THE SHADER WILL SAMPLE ON, carried into the pose so the door is read on the
          // buffer the host is about to bind as `uRes` rather than on the CSS frame around it. The
          // host settles it from the device ratio and its own resolution step, so it moves while a
          // pass plays and each door is read on the grid standing at that door's own instant.
          bufWidth: st.viewport.bufferW, bufHeight: st.viewport.bufferH,
        };
        // AT A DOOR THE INSTRUMENT SAYS WHAT IT APPLIED, and says it before it refuses. The reading
        // is taken on the buffer this frame is drawn on, so it is the run-time truth his 18:00
        // decision asks for rather than the periods the score asked for.
        if (h.mix === 0 || h.mix === 1) {
          var v = values(pose);
          if (st.reportApplied) {
            st.reportApplied({
              door: h.mix === 0 ? "in" : "out",
              buffer: [pose.bufWidth, pose.bufHeight],
              reads: "period",
              request: [v.periodRequestA, v.periodRequestB],
              applied: [v.periodA, v.periodB],
              moved: v.periodGratings, unit: "gratings",
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
    instrument: beatInstrument(),
  });
})();
