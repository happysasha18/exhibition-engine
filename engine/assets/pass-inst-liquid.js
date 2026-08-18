/*!pass-inst-liquid.js*/
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
  // THE LIQUID INSTRUMENT (§8) — lab/effects/liquid.js carried across
  // ================================================================================================
  // WHAT THE VISITOR SEES. The photograph is the top of a body of water. A slow swell travels over
  // it — three broad waves on their own headings, each a little wider than the frame — and the
  // picture rides their slope: a straight line in the architecture bows as a crest passes and comes
  // back behind it. The arriving work SURFACES ON THE CRESTS: where the water stands high enough it
  // is already the second photograph, and as the swell rises the second work floods down the flanks
  // into the troughs until the whole surface is the arriving work and the water settles flat.
  //
  // WHERE IT STANDS ON THE CHARTER'S SHELF. `lab/CROSSING-BRIEF.md`'s vocabulary table carries a
  // `liquid` row, and it is one of the two rows in that table that name no crossing:
  //
  //     | liquid | жидкая поверхность | оживление + garnish | TEXTURE | unused yet; his liquid
  //     | wish exists as a module |
  //
  // Two things follow, and both are decisions rather than readings.
  //
  //   · THE LEVEL IS HIS. TEXTURE is what the table says and TEXTURE is what this manifest declares
  //     — the water bends the picture's own material, and the colour splits at the bend. SURFACE
  //     stands beside it and is DERIVED rather than carried: one field runs over the whole frame and
  //     its value at a point decides which of the two works stands there, which is the level
  //     `pass-inst-adrift.js` places exactly that act at.
  //   · THE ROLE IS WIDENED, AND THAT IS SAID OUT LOUD. His row calls this оживление and garnish —
  //     one work enlivened, or a second voice laid over another crossing. This engine has no garnish
  //     slot: a cue carries an ordered PAIR and the three slots a plan casts (pivot, travel,
  //     arrival) all hand one work over to another. The nearest thing to his own word is the pivot
  //     cue VOICED AS ACCOMPANIMENT, whose roles the composer writes as `["surface", "breath"]` —
  //     the ground held and breathing, which is оживление in this engine's own vocabulary. So the
  //     instrument is built to cross, and it is at its quietest exactly where his row puts it. What
  //     is NOT claimed is that the table's verdict was read as a licence: it says «unused yet», and
  //     the port is what makes it usable.
  //
  // ------------------------------------------------------------------------------------------------
  // WHAT CAME OVER, AND — the larger half — WHAT DID NOT
  // ------------------------------------------------------------------------------------------------
  // The module is two passes. A SIMULATION at a low resolution ping-pongs a field between two
  // textures: a drag vector the pointer pushes into the surface and a height wave spreading from
  // where the pointer pressed. A DRAW pass then offsets the picture's lookup by that field and by a
  // swell of its own.
  //
  // THE WHOLE SIMULATION STAYS BEHIND, and the module's own header is the authority for it:
  //
  //     «that field is filled only by a hand pressing the surface, the engine parks the hand inside
  //      a crossing, so under a score the field is flat at every mark of such a handle and both its
  //      doors would draw one frame»
  //
  // (liquid.js:369-375, the module's own reason for not publishing its simulation constants). A
  // crossing carries no hand, so the field is flat at every instant of every pass this instrument
  // will ever play; carrying the two framebuffers, the two half-float targets, the twelve-step
  // integration and the byte-packing fallback across would be carrying a machine that draws nothing.
  // With them go the module's three declared params — `strength`, `heal` and `refraction` shape the
  // pointer's wake, its settling and the colour split, and only the last of the three survives a
  // flat field. So this instrument allocates NO texture, NO framebuffer and no ping-pong, and it
  // spends one programme over the two source-texture slots the host already holds.
  //
  // WHAT CAME OVER, digit for digit: the three waves' headings, their rates, their long counts and
  // their amplitudes; the swell's own displacement of the picture; the soft ceiling that lets the
  // surface bend and never tear; the taper at the frame's edge; the breathing zoom; the colour split
  // held to a hair; the specular the swell catches; the light the height carries; the reach of the
  // module's own `wave` and `spread` handles and the fitted response curve on the second of them;
  // and the module's own MIRRORED_REPEAT wrap, which is written out in the shader because the host
  // binds its sources CLAMP_TO_EDGE.
  //
  // ------------------------------------------------------------------------------------------------
  // THE PORT'S OWN ONE ADDITION: THE HANDOVER
  // ------------------------------------------------------------------------------------------------
  // The module carries ONE work. A cue of this engine carries an ordered pair, so the port has to
  // say how the second photograph arrives, and the honest question is which of the module's own
  // numbers already answers it. It is `hs` — the swell's HEIGHT at a point, `dot(sin(ph), sa)`,
  // which the module already computes and already reads for the light the travel carries
  // (liquid.js:129, :162). The handover is a level in that height: above the line the arriving work
  // stands, below it the departing one, and the line walks with the dial from above every crest to
  // below every trough.
  //
  // NOTHING ELSE WAS INVENTED, and three things follow that are worth stating.
  //   · THE BOUNDARY IS THE WATER'S OWN. The two works are read through the SAME displacement, so
  //     this is one sheet of water carrying two pictures rather than two pictures with two waters.
  //   · THE COVERAGE IS ANALYTIC. The height's own gradient is `swell` — the very vector the module
  //     already computes for the displacement — so the share of a point that falls on either work is
  //     read from a number that was already there, and the boundary is anti-aliased without a second
  //     sample.
  //   · BOTH DOORS ARE EXACT BY CONSTRUCTION. The line travels a margin past the height's own
  //     ceiling at either end, so every point of the frame stands on one work; and the module's own
  //     crossing dial is nothing there, so the frame is the plain cover fit with no bend, no colour
  //     split, no specular and no breathing zoom. That is the module's own published door
  //     (liquid.js:140-145) with a whole work standing in it.
  //
  // ------------------------------------------------------------------------------------------------
  // THE COVERAGE: THIS INSTRUMENT FILLS THE FRAME
  // ------------------------------------------------------------------------------------------------
  // §7's coverage law of 12:40 asks every instrument to say where its own matter is absent. Here it
  // is absent nowhere: every point of the frame carries one of the two photographs, both branches of
  // the mix are picture, and the alpha is the constant 1. The declaration is `writes: false`, which
  // under the placement rule (§8 as amended 14:05) makes it lawful as the LOWEST cue of a stack and
  // as a whole one-cue score — which is the placement a ground takes, and a ground is what this
  // instrument is cast as.
  function liquidInstrument() {
    var VERT = [
      "attribute vec2 aPos;",
      "varying vec2 vUv;",
      "void main(){ vUv = vec2(aPos.x * 0.5 + 0.5, 0.5 - aPos.y * 0.5); gl_Position = vec4(aPos, 0.0, 1.0); }",
    ].join("\n");

    // ----------------------------------------------------------------------------------------------
    // THE SHADER — liquid.js's own DRAW_FS with the field taken out and the second work put in
    // ----------------------------------------------------------------------------------------------
    // The module's draw pass reads the simulation field in three places: `dg`, the four-tap average
    // of the drag; `grad`, the slope of the height the pointer pressed in; and `f.b`, that height
    // itself. All three are exactly zero under a score for the reason the header gives, so all three
    // are gone and every term they multiplied goes with them. What is left is the module's swell,
    // line for line.
    //
    // TWO CARRIERS HOLD EVERYTHING THAT MOVES, because the host binds four uniform types and a
    // shorter list is a shorter fence: `uWave` is the crossing dial, the swell's own amplitude, the
    // crest spacing and the phase; `uDial` is the handover line, the colour split, and the two judge
    // channels.
    var FRAG = [
      "precision highp float;",
      "varying vec2 vUv;",
      "uniform sampler2D uA;",          // the work the visitor is leaving
      "uniform sampler2D uB;",          // the work arriving on the crests
      "uniform vec4 uFitA;",
      "uniform vec4 uFitB;",
      "uniform vec2 uRes;",
      // wet: 0 the still photograph, 1 the water exactly as the module ships it (liquid.js:140-145).
      // life: how far the picture bends, the module's own `uLife`, handed in already scaled by wet.
      // spread: how far apart the crests stand, the module's own `uSpread`.
      // advect: how far the swell has been carried, in radians, the module's own `uAdvect`.
      "uniform vec4 uWave;",
      // front: the level in the swell's height the handover stands at.
      // refr: the colour split, handed in already scaled by wet.
      // travel and shade: the two judge channels, the bend and the water's own light.
      "uniform vec4 uDial;",
      "uniform float uTime;",
      "uniform float uMask;",
      // THE THREE WAVES (liquid.js:121-131), carried digit for digit. Each heading is a vector in
      // the frame's own unit square, each rate is radians a second, and each long count is the slow
      // rise and fall of that wave's own amplitude — so crests arrive in groups and no two moments
      // in a visit look alike.
      "const vec3 SA = vec3(0.55, 0.42, 0.30);",
      "const vec3 KX = vec3( 1.4,  4.3, -3.1);",
      "const vec3 KY = vec3( 5.2, -2.4,  3.0);",
      "const vec3 RATE = vec3(1.70, 1.35, 2.25);",
      "const vec3 SLOW = vec3(0.23, 0.31, 0.17);",
      "const vec3 SLOWPH = vec3(0.0, 2.1, 4.3);",
      // The soft ceiling the surface bends inside, and the hair the colour is allowed to split by
      // (liquid.js:135, :150). Both are the module's own.
      "const float BEND_MAX = 0.070;",
      "const float SPLIT_MAX = 0.0032;",
      // THE MODULE'S OWN WRAP, WRITTEN OUT. liquid.js binds its picture MIRRORED_REPEAT
      // (liquid.js:273-274); this host binds every source CLAMP_TO_EDGE, so the fold is done here
      // and the two roads read the same texel wherever the swell carries a lookup off the frame.
      "vec2 mirror(vec2 x){ vec2 m = mod(x, 2.0); return 1.0 - abs(1.0 - m); }",
      // Where one point of the frame falls on one work: the host's own seating, pulled in by the
      // breathing zoom exactly as liquid.js:94-97 pulls it in.
      "vec2 into(vec2 p, vec4 f, float zoom){",
      "  return mirror((p - 0.5) * f.xy / max(zoom, 1e-4) + 0.5 + f.zw);",
      "}",
      // GLSL ES 1.00 carries no `tanh`; the module's own two soft ceilings are written out here and
      // answer the same numbers.
      "float tanh1(float x){ float e = exp(2.0 * clamp(x, -12.0, 12.0)); return (e - 1.0) / (e + 1.0); }",
      "void main(){",
      // The module measures the frame from the BOTTOM (gl_FragCoord over uRes) and this host hands
      // rows down the picture, so the swell is computed in the module's own square and the
      // displacement's second component is turned over when it is spent on a lookup.
      "  vec2 q = vec2(vUv.x, 1.0 - vUv.y);",
      "  float t = uTime;",
      "  float spread = uWave.z;",
      // THE SWELL (liquid.js:113-131). Three broad waves cross the frame on their own headings and
      // speeds; `spread` crowds the crests or lets them out, and it multiplies the three headings,
      // so a shorter wave of the same height carries a steeper slope and the picture bends harder —
      // that is the water, not a defect. `advect` carries the whole swell forward by a phase the
      // score names, the same fraction of each wave's own length.
      "  vec3 ph = vec3(dot(vec2(KX.x, KY.x) * spread, q) - t * RATE.x,",
      "                 dot(vec2(KX.y, KY.y) * spread, q) - t * RATE.y,",
      "                 dot(vec2(KX.z, KY.z) * spread, q) - t * RATE.z) - uWave.w;",
      "  vec3 sa = SA * (0.78 + 0.22 * sin(vec3(t * SLOW.x + SLOWPH.x,",
      "                                         t * SLOW.y + SLOWPH.y,",
      "                                         t * SLOW.z + SLOWPH.z)));",
      "  vec3 cs = cos(ph) * sa;",
      "  float hs = dot(sin(ph), sa);",
      // The swell's own gradient, which is the vector the picture rides. ONE VECTOR ANSWERS TWO
      // QUESTIONS: it is the module's own displacement, and it is the exact slope of the height the
      // handover reads, so the boundary below is anti-aliased off a number that was already here.
      "  vec2 swell = vec2(dot(cs, KX * spread), dot(cs, KY * spread));",
      "  vec2 disp = swell * uWave.y * uDial.z;",
      // a soft ceiling: the surface bends, it never tears (liquid.js:133-135)
      "  float dl = length(disp);",
      "  disp *= (BEND_MAX * tanh1(dl / BEND_MAX)) / max(dl, 1e-6);",
      "  vec2 e = min(q, 1.0 - q);",
      "  float taper = smoothstep(0.0, 0.05, min(e.x, e.y));",
      "  disp *= taper;",
      "  float breath = 1.0 + 0.0075 * sin(t * 0.26) + 0.0040 * sin(t * 0.11 + 1.3);",
      // THE CROSSING DIAL (liquid.js:140-146). At wet 0 the frame is the still photograph — a plain
      // cover-fit sample, no bend, no breathing zoom — because `life` and `refr` are handed in
      // already scaled by it and the zoom is gated here for the same reason.
      "  float zoom = mix(1.0, 1.055 * breath, uWave.x);",
      // red and blue land a hair apart — held to a hair, so a deep bend keeps its colour
      "  vec2 cd = disp * (0.20 * uDial.y);",
      "  float cl = length(cd);",
      "  cd *= (SPLIT_MAX * tanh1(cl / SPLIT_MAX)) / max(cl, 1e-6);",
      // the module's square has y running up and the picture's rows run down it
      "  vec2 sp = vec2(disp.x, -disp.y);",
      "  vec2 sc = vec2(cd.x, -cd.y);",
      "  vec3 colA, colB;",
      "  colA.r = texture2D(uA, into(vUv + sp + sc, uFitA, zoom)).r;",
      "  colA.g = texture2D(uA, into(vUv + sp, uFitA, zoom)).g;",
      "  colA.b = texture2D(uA, into(vUv + sp - sc, uFitA, zoom)).b;",
      "  colB.r = texture2D(uB, into(vUv + sp + sc, uFitB, zoom)).r;",
      "  colB.g = texture2D(uB, into(vUv + sp, uFitB, zoom)).g;",
      "  colB.b = texture2D(uB, into(vUv + sp - sc, uFitB, zoom)).b;",
      // THE HANDOVER, AND ITS OWN FOOTPRINT. `cov` is the share of THIS point that still stands on
      // the departing work: 1 where the water is lower than the line, 0 where it is higher. The
      // crossover is one point of the drawing buffer wide, read through the height's own gradient,
      // so the boundary carries no fade of its own and no step either.
      "  vec2 g = vec2(swell.x / max(uRes.x, 1.0), swell.y / max(uRes.y, 1.0));",
      "  float band = max(length(g), 1e-6);",
      "  float cov = clamp(0.5 + (uDial.x - hs) / band, 0.0, 1.0);",
      "  vec3 col = mix(colB, colA, cov);",
      // the bend catches a little light, the way a swell does (liquid.js:155-159)
      "  vec2 slope = swell * uWave.y * uDial.z * 0.8 * 11.0 * taper;",
      "  vec3 n = normalize(vec3(-slope, 1.0));",
      "  float spec = pow(max(dot(n, normalize(vec3(0.30, 0.52, 0.80))), 0.0), 26.0);",
      "  col += spec * (0.04 + 0.12 * uDial.y) * uWave.x * uDial.w;",
      // the swell carries its own light with it, so the travel reads even on a flat patch
      "  col *= 1.0 + clamp(hs * uWave.y * 7.0, -0.05, 0.05) * taper * uDial.w;",
      // THE JUDGES' OWN FRAME: which work stands at this point, how high the water is under it, and
      // how far the taper has let the bend in. It is read as colour and carries no coverage of its
      // own, because what it is for is to be measured rather than looked at.
      "  vec3 judge = vec3(cov, hs * 0.3937 + 0.5, taper);",
      "  col = mix(col, judge, uMask);",
      // THE COVERAGE: the alpha is the constant 1, and it is a decision rather than a default. Both
      // branches of the mix are photograph, so this instrument has no absence to publish and stands
      // as the ground a stack is laid on.
      "  gl_FragColor = vec4(col, 1.0);",
      "}",
    ].join("\n");

    function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }

    /* THE THREE WAVES, in the script's own copy of the shader's constants, because the door reading
       below walks the very height the shader draws and a second description of one swell could
       disagree with the first. Every number is liquid.js:121-131. */
    var SA = [0.55, 0.42, 0.30];
    var KX = [1.4, 4.3, -3.1];
    var KY = [5.2, -2.4, 3.0];
    var RATE = [1.70, 1.35, 2.25];
    var SLOW = [0.23, 0.31, 0.17];
    var SLOWPH = [0.0, 2.1, 4.3];

    /* HOW HIGH THE WATER CAN EVER STAND, and it is a ceiling rather than a measurement. Each wave's
       amplitude is its own base times `0.78 + 0.22·sin(...)`, which never passes 1, and the height
       is the sum of the three sines against those amplitudes — so |hs| never passes the sum of the
       three bases. This is exact, and it is what the handover's line has to travel past for a door
       to be one whole work. */
    var FIELD_TOP = SA[0] + SA[1] + SA[2];        // 1.27

    /* THE STEEPEST THE HEIGHT CAN EVER RUN, in field units per frame side, at a crest spacing of
       one. Same construction: each wave contributes its own amplitude times the length of its own
       heading, and the cosines cannot all stand at one together for longer than they do. It is a
       ceiling and it can only ever OVER-hold, which is the property the door reading wants. */
    var SLOPE_TOP = (function () {
      var s = 0, i;
      for (i = 0; i < 3; i++) s += SA[i] * Math.sqrt(KX[i] * KX[i] + KY[i] * KY[i]);
      return s;                                   // 6.3243
    })();

    /* HOW FAR PAST THE HEIGHT'S OWN CEILING THE HANDOVER'S LINE TRAVELS. A line a margin above every
       crest leaves every point of the frame on the departing work and a line a margin below every
       trough leaves every point on the arriving one; that margin is what either door stands on, and
       it is the number the reading below is held against. A tenth of the field, which is the same
       share `pass-inst-matter.js` gives its own travelling threshold — one law, one number, read in
       two instruments' own units. */
    var MARGIN = 0.10;

    /* THE DEAD BANDS AT EITHER END OF THE HAND, the number every instrument of this engine uses. Over
       the first and last five hundredths of the dial the water is flat and the line stands past the
       ceiling: the hand is spent there and the standing work is the picture its source carries, to
       the point. That is what makes a door a door and not a checkpoint. */
    var FEEL_D0 = 0.05;

    /* THE WATER'S OWN LIFE (liquid.js:335). The module derives it from its `strength` control —
       `0.0042 + 0.0037·s` — and that control does not come over, because everything else it touches
       is the pointer's wake. So it is pinned at the module's own declared default of 55, and the
       whole of its range is inside the `swell` handle's own reach: the module's note at :376-381
       says the life runs 0.0042 to 0.0079 across that control, a factor of 1.9, which is why the
       handle's reach is a factor of two either way. */
    var LIFE_DOOR = 0.0042 + 0.0037 * 0.55;       // 0.006235
    /* AND WHAT IT IS UNDER LESS MOTION (liquid.js:539). The module holds the swell at a sixth of its
       own life there, and holds its clock at a settled phase (liquid.js:648). */
    var LIFE_REDUCED = 0.0012;
    var REDUCED_T = 6.2;

    /* THE TWO REACHES, the module's own (liquid.js:382 and the note above it). `swell` at its middle
       gives back the module's own swell exactly and reaches a factor of two either way, which is the
       module's own range restated; `spread` takes the same factor of two, because the three waves
       the module ships already stand at headings 3.0 to 5.6 long — a factor of 1.9 between the
       widest and the narrowest. */
    var WAVE_REACH = 2.0, SPREAD_REACH = 2.0;

    /* THE RESPONSE CURVE OF `crest` (liquid.js:391-410, DARKROOM-DRAFT D2, his word 08-08 17:57),
       carried digit for digit. A two-piece logarithm hinged AT THE HANDLE'S OWN NEUTRAL, which is
       the module's own spacing — so the door lands to the pixel wherever it stands. The hinge sits
       where the CHANGE divides rather than at the middle of the hand's travel: crowding the crests
       moves the picture far more than letting them out, 36 channels a tenth at the crowded end
       against 14 at the open one, and a band of 2.58 falls to 1.31. THE HINGE IS WHY THIS HANDLE'S
       DEFAULT IS 0.702 AND NOT A HALF: `feelCrest(0.702)` is exactly 0.5, which is the spacing the
       module ships. */
    var FEEL_C_U0 = 0.702, FEEL_C_K1 = 0.59, FEEL_C_K2 = 0.91;
    function feelLog(x, k) {
      return Math.abs(k) < 1e-6 ? x : (Math.exp(k * x) - 1) / (Math.exp(k) - 1);
    }
    function feelCrest(u) {
      return u <= FEEL_C_U0
        ? 0.5 * feelLog(u / FEEL_C_U0, FEEL_C_K1)
        : 0.5 + 0.5 * feelLog((u - FEEL_C_U0) / (1 - FEEL_C_U0), FEEL_C_K2);
    }

    /* THE SPAN THE SCORE'S DIE ARRIVES ON, and what this instrument spends it on: the phase the
       swell stands at when the crossing opens. The module publishes that as its own third handle and
       records that THE TRAVEL IS ONE WHOLE WAVE, so the two ends of it stand the same picture
       (liquid.js:364-368). A whole wave over the die's own span is therefore the honest mapping, and
       a die of nothing is the module's own rest. It is also the one thing that keeps two passes over
       one edge from opening on the same crest, which is charter shelf 13's rubato read on this
       instrument's own time axis. */
    var SEED_SPAN = 8;

    // Cover-fit a work into the frame and nothing beyond it. The breathing zoom is applied inside
    // the shader, where it is gated by the crossing dial, so the seating a work asks for IS the
    // plain cover fit and BOTH DOORS FRAME AT A CROP OF EXACTLY ONE.
    function fit(iw, ih, w, h) {
      var fa = w / Math.max(h, 1);
      var ia = iw / Math.max(ih, 1);
      if (ia > fa) return [fa / ia, 1, 0, 0];
      return [1, ia / fa, 0, 0];
    }

    // WHERE THE HAND HAS BROUGHT THE CROSSING, with the dead bands taken off. One travelling number,
    // read on the diagnostic surface: how much of the passage has happened.
    function feelOf(u) {
      return clamp((clamp(u, 0, 1) - FEEL_D0) / (1 - 2 * FEEL_D0), 0, 1);
    }

    // The grid one frame is drawn on: the buffer the host is about to bind as `resolution`, with the
    // CSS frame where it hands none. `drawn` says which of the two the reading below names, since a
    // reader told «a 390 x 844 frame» would look for a device that has none.
    function gridOf(st) {
      var bw = Math.round(st.bufWidth), bh = Math.round(st.bufHeight);
      if (bw >= 1 && bh >= 1) return { w: bw, h: bh, drawn: true, given: true };
      var cw = Math.round(st.cssWidth), ch = Math.round(st.cssHeight);
      if (cw >= 1 && ch >= 1) return { w: cw, h: ch, drawn: false, given: true };
      return { w: 1, h: 1, drawn: false, given: false };
    }

    // ---- the numbers of one frame ------------------------------------------------------------------
    // Everything the shader gets beyond the seating of the two works is a pure function of the pose,
    // and every number in the pose comes from a handle a score drives. The one place the module read
    // time — its own accumulated frame clock — reads the `clock` handle here instead, so a seeded
    // score repeats to the pixel.
    //
    // The crest spacing is a parameter rather than read straight off the pose, because the hold in
    // `values` below asks this same function for the same pose at a wider spacing. Nothing else about
    // it moved.
    function posed(st, crest) {
      var d = feelOf(st.mix);
      // THE WATER RISES AND SETTLES ON ONE ENVELOPE. Nothing at both doors, whole in the middle: one
      // sine over the whole crossing, which is what makes both landings exact and what makes the
      // swell a thing that happens rather than a thing that is switched on.
      var wet = Math.sin(Math.PI * d);
      var spread = Math.pow(SPREAD_REACH, 1 - 2 * feelCrest(clamp(crest, 0, 1)));
      var life = (st.reduced ? LIFE_REDUCED : LIFE_DOOR)
               * wet * WAVE_REACH * clamp(st.swell, 0, 1);
      var advect = (clamp(st.seed, 0, SEED_SPAN) / SEED_SPAN) * 2 * Math.PI;
      // THE HANDOVER'S OWN LINE, walking from a margin above every crest to a margin below every
      // trough. It is monotone in the hand and it is the only thing that decides which work a point
      // stands on, so a person watching sees the arriving work surface on the crests and flood down
      // the flanks, and never sees it fade in.
      var front = (FIELD_TOP + MARGIN) * (1 - 2 * d);
      var refr = clamp(st.refract, 0, 1) * wet;
      var travel = clamp(st.travel, 0, 1);
      var shade = clamp(st.shade, 0, 1);
      var t = st.reduced ? REDUCED_T : (Number(st.t) || 0);
      return {
        // the two carriers the shader reads, and the second the swell travels on
        wave: [wet, life, spread, advect],
        dial: [front, refr, travel, shade],
        t: t,
        // the same numbers by name, for the reading below and for the diagnostic surface
        dialAt: d, wet: wet, spread: spread, life: life, advect: advect, front: front,
        refr: refr, travel: travel, shade: shade,
        mask: clamp(typeof st.mask === "number" ? st.mask : 0, 0, 1),
        crest: clamp(crest, 0, 1), crestFelt: feelCrest(clamp(crest, 0, 1)),
        fieldTop: FIELD_TOP, margin: MARGIN, coverCrop: 1,
        grid: gridOf(st),
      };
    }

    // ---- THE DOOR THE INSTRUMENT READS FOR ITSELF --------------------------------------------------
    // His 18:00 architecture decision, carried in the U27 brief: the instrument reads its doors at
    // runtime on the actual buffer, and the report it hands back is the runtime truth; what the
    // manifest declares is only the claim. The meshing instrument answered that first
    // (pass-inst-gears.js), the folding one walks its two faces over the frame, and this is the same
    // law read in THIS instrument's own unit, which is the WATER — its height over the frame, and
    // which work that height puts at a point.
    //
    // WHAT A DOOR ASKS OF A BODY OF WATER. Two things, and both are read on the buffer rather than
    // declared:
    //   · THE WATER IS FLAT. The crossing dial is spent inside its dead band, so the bend, the colour
    //     split, the specular, the water's own light and the breathing zoom are all exactly nothing
    //     and the frame is the source cover-fitted and nothing else. That is exact by construction —
    //     `wet` is a sine at its own zero — and it is published as the applied state rather than
    //     asserted, so a later change to the dead bands or the envelope reddens against it.
    //   · EVERY POINT STANDS ON ONE WORK. The handover's line travels a margin past the height's own
    //     ceiling, so no point of the frame should carry any share of the other photograph. That is a
    //     claim about a GRID — the crossover is one point of the buffer wide, and how wide one point
    //     is in the field's own units depends on the buffer the host binds — so it is WALKED at the
    //     buffer's own sample points instead of being asserted: the same height the shader computes,
    //     the same gradient, the same coverage, at the corners where the swell can stand highest
    //     against a small frame, at the edge midpoints and at the nine points around the centre.
    //
    // WHAT THIS READING FINDS, SAID PLAINLY. On every buffer a phone or a desk can hand, the crossover
    // is a small fraction of the margin and both doors come out whole. The reading is still taken,
    // because a door held by a number nobody read is a claim rather than a landing: it publishes how
    // much field the tightest point had TO SPARE, so a crest spacing driven toward its crowded end,
    // or a resolution ladder stepping down under a slow frame, shows the margin closing long before
    // anything crosses.
    //
    // AND THERE IS SOMETHING HERE TO HOLD. Unlike the box's landing, this fault has a direction that
    // closes it: the crossover is proportional to the crest SPACING — crowded crests carry a steeper
    // height and a wider crossover — so a door the score's spacing cannot keep whole is answered by
    // letting the crests out until it is, and the request stays on the record beside what was
    // applied. Past the hold's own reach the pose the score asked for is genuinely a different water
    // and the door is refused with the measured numbers in it.
    var DOOR_HOLD = 0.25;      // how far the hold may walk the crest handle, in the handle's own units
    var DOOR_STEP = 0.05;      // and in what steps
    var DOOR_GRID = 10;        // how many steps the reading walks across each side of the buffer

    // The height of the water at one point of the frame, and its own gradient — the shader's own
    // `hs` and `swell`, written once more here so the reading walks the very surface the shader
    // draws rather than a description of it.
    function heightAt(v, qx, qy) {
      var i, hs = 0, gx = 0, gy = 0, ph, sa;
      for (i = 0; i < 3; i++) {
        ph = (KX[i] * v.spread) * qx + (KY[i] * v.spread) * qy - v.t * RATE[i] - v.advect;
        sa = SA[i] * (0.78 + 0.22 * Math.sin(v.t * SLOW[i] + SLOWPH[i]));
        hs += Math.sin(ph) * sa;
        gx += Math.cos(ph) * sa * KX[i] * v.spread;
        gy += Math.cos(ph) * sa * KY[i] * v.spread;
      }
      return { hs: hs, gx: gx, gy: gy };
    }

    // THE WATER, WALKED ON THE BUFFER THE SHADER WILL SAMPLE ON. `want` is 1 at the entry door, where
    // every point owes its coverage to the departing work, and 0 at the exit. What comes back is how
    // many points were walked, how many carried any share of the wrong work, how much field the
    // tightest of them had to spare, and how wide the crossover stood there.
    function waterReadOf(v, W, H, want) {
      var walked = 0, i, j, wrong = 0, spare = 1e9, widest = 0;
      function walk(px, py) {
        var qx = px / W, qy = 1 - py / H;
        var r = heightAt(v, qx, qy);
        var band = Math.max(Math.sqrt((r.gx / W) * (r.gx / W) + (r.gy / H) * (r.gy / H)), 1e-6);
        var cov = clamp(0.5 + (v.front - r.hs) / band, 0, 1);
        var room = want ? (v.front - r.hs) : (r.hs - v.front);
        if (want ? cov < 1 : cov > 0) wrong++;
        if (room < spare) spare = room;
        if (band > widest) widest = band;
        walked++;
      }
      // A GRID AND NOT A HANDFUL OF POINTS, and the reason is this instrument's own shape. The box
      // reads its two faces at the corners because a face is a quadrilateral and its worst point is
      // one of four; a swell has no corners — its crest can stand anywhere on the frame, and a
      // reading that walked nine points would call a door whole because it happened to look between
      // two crests. The grid is odd, so it lands on the frame's own centre, and it takes the four
      // corners exactly, where the swell's own taper does not reach.
      for (i = 0; i <= DOOR_GRID; i++) {
        for (j = 0; j <= DOOR_GRID; j++) {
          walk(clamp((i / DOOR_GRID) * W, 0.5, W - 0.5),
               clamp((j / DOOR_GRID) * H, 0.5, H - 0.5));
        }
      }
      // THE CEILING BESIDE THE WALK. The walk reads seventeen points and the water's crest can stand
      // between two of them, so the ceiling — the steepest the height can ever run on this buffer at
      // this spacing — is read as well and the refusal below stands on whichever of the two is worse.
      // It costs two multiplications and it can only ever OVER-hold.
      var ceil = 0.5 * SLOPE_TOP * v.spread / Math.max(Math.min(W, H), 1);
      return { walked: walked, wrong: wrong, spareField: spare, widestBand: widest,
               ceilingBand: ceil, spread: v.spread, crest: v.crest, want: want };
    }

    function doorReadOf(v, st) {
      var want = st.mix === 0 ? 1 : (st.mix === 1 ? 0 : -1);
      if (want < 0) return null;
      var g = v.grid;
      if (!g.given) return null;
      var read = waterReadOf(v, g.w, g.h, want);
      read.grid = g;
      return read;
    }

    // THE REFUSAL, worded the way the host's own manifest refusals read: what is wrong, in this
    // instrument's own measured numbers, on the grid it was measured on.
    function doorWhyNoOf(read) {
      if (!read) return null;
      var g = read.grid, door = read.want ? "the entry" : "the exit";
      var work = read.want ? "departing" : "arriving";
      var other = read.want ? "arriving" : "departing";
      var where = " of a " + g.w + " x " + g.h + (g.drawn ? " buffer" : " frame");
      if (read.wrong) {
        return door + " door leaks: the water puts the " + other + " work on " + read.wrong
             + " of the " + read.walked + " points this reading walked" + where
             + ", where " + door + " door's own law asks for the " + work + " work at every point";
      }
      if (read.ceilingBand >= MARGIN) {
        return door + " door leaks: at a crest spacing of " + read.spread.toFixed(3)
             + " the water's own steepest slope crosses this instrument's handover over inside "
             + read.ceilingBand.toFixed(4) + " of the field" + where + ", past the " + MARGIN
             + " the handover's line stands beyond the water's own ceiling of "
             + FIELD_TOP.toFixed(2) + ", so the " + other
             + " work takes the points of the frame nearest a crest, where " + door
             + " door's own law asks for the " + work + " work at every point";
      }
      return null;
    }

    // THE NUMBERS OF ONE FRAME, WITH ITS DOOR READ ON THE BUFFER BEING DRAWN. Away from a door this
    // is `posed` and nothing more: the reading is taken nowhere else and no spacing moves. At a door
    // whose crest spacing crowds the crossover past the margin on the buffer being drawn, the
    // instrument lets the crests OUT — the only direction that closes it, since the crossover rises
    // with the crowding — and answers with the first pose whose door is whole. What the score asked
    // for and what was applied are both on the record.
    function values(st) {
      var asked = clamp(typeof st.crest === "number" ? st.crest : FEEL_C_U0, 0, 1);
      var v = posed(st, asked);
      v.crestRequest = asked;
      v.crestMoved = 0;
      v.doorHeld = null;
      var read = doorReadOf(v, st);
      var no = doorWhyNoOf(read);
      v.doorGrid = read ? read.grid : null;
      v.water = read ? { walked: read.walked, wrong: read.wrong, spareField: read.spareField,
                         widestBand: read.widestBand, ceilingBand: read.ceilingBand } : null;
      if (!no) { v.doorWhyNo = null; return v; }
      // Letting the crests out means walking the handle UP past its own hinge, since `feelCrest`
      // rises with the handle and the spacing falls as `2^(1-2·feelCrest)`.
      for (var step = DOOR_STEP; step <= DOOR_HOLD + 1e-9; step += DOOR_STEP) {
        var tryC = asked + step;
        if (tryC > 1) break;
        var w = posed(st, tryC);
        var wRead = doorReadOf(w, st);
        if (doorWhyNoOf(wRead)) continue;
        w.crestRequest = asked;
        w.crestMoved = tryC - asked;
        w.doorHeld = no;
        w.doorWhyNo = null;
        w.doorGrid = wRead.grid;
        w.water = { walked: wRead.walked, wrong: wRead.wrong, spareField: wRead.spareField,
                    widestBand: wRead.widestBand, ceilingBand: wRead.ceilingBand };
        return w;
      }
      v.doorWhyNo = no + ", and letting the crests out by the " + DOOR_HOLD
                  + " of this handle's own travel the hold reaches does not close it";
      return v;
    }

    var manifest = {
      id: "liquid", api: 1, arity: 2,
      // The departing work loosens onto the swell, the middle is water carrying two photographs at
      // once, and the arriving work settles flat.
      roles: ["disassembly", "mystery", "assembly"],
      // THE CHARTER'S OWN ROW GIVES THE FIRST; THE SECOND IS DERIVED AND SAID TO BE DERIVED.
      //   · TEXTURE — `lab/CROSSING-BRIEF.md`'s vocabulary table publishes exactly this level for
      //     this module. The water bends the picture's own material and splits its colour at the
      //     bend; nothing here cuts the frame into parts.
      //   · SURFACE — one field runs over the whole frame and its value at a point decides which of
      //     the two works stands there, which is the level `pass-inst-adrift.js` places that same act
      //     at. WORLD is not claimed: the eye never leaves the glass, and this instrument asks the
      //     host's camera for nothing.
      levels: ["SURFACE", "TEXTURE"],
      params: { swell: [0, 1], crest: [0, 1], refract: [0, 1] },
      // EVERY handle a score can drive (§4.4b). `mix` is the dial — the module's own `wet` under the
      // name every instrument in this engine gives it — and `clock` is the second the host hands
      // down, which is the one place the module read time. The three below them are the module's own
      // two published handles and the one declared param that survives a flat field. `seed` is the
      // score's die, `shade` and `travel` are the two judge channels, and `mask` is the judges' own
      // frame.
      //
      // THREE OF THE MODULE'S DECLARED HANDLES DO NOT TRAVEL, and the reason is one sentence in the
      // module's own header: the engine parks the hand inside a crossing, so `strength` and `heal` —
      // which shape the pointer's wake and its settling — would be handles a score could walk without
      // moving the picture, which is noise in the score (§4.4b). The module's third published handle,
      // its `advect`, DOES travel, but not as a handle of its own: what it names is a phase, and no
      // measurement of a photograph is a phase. It is spent on the score's die instead, where it
      // keeps two passes over one edge from opening on the same crest.
      handles: {
        mix: { min: 0, max: 1, def: 0 },
        clock: { min: 0, max: 14, def: 0 },
        swell: { min: 0, max: 1, def: 0.5,
                 unit: "how far the picture bends as a crest passes",
                 reads: "texture.scoreFromCutLines, how much of the work reads as grain rather than "
                      + "as line — his 19:13 word says a wave plays where the work carries one, so "
                      + "a work that IS texture takes the deep swell and a work of straight "
                      + "architecture takes the shallow one",
                 applied: { atMiddle: LIFE_DOOR, reach: WAVE_REACH,
                            restsAt: "both doors, where the crossing dial is nothing" } },
        crest: { min: 0, max: 1, def: FEEL_C_U0,
                 unit: "how far apart the crests of the swell stand",
                 // READ AS A POSITION AND NOT AS AN EQUALITY, and the reason is a measurement. The
                 // module's three waves stand 1.17, 1.28 and 1.46 frame sides long, so its crests
                 // are WIDER than the frame — the module's own «each is a little wider than the
                 // frame». A work's strongest spectral band is an order finer than that (170.7
                 // points over a 1440-point side, on 78 of the 121 works), so a handle that made
                 // the crests equal to it would crowd them elevenfold, far past this handle's own
                 // reach of two. What the handle takes is therefore where the work's own period
                 // stands INSIDE the collection's own spread of that measurement, mapped onto this
                 // handle's own published range: a work whose repeat is finer than the collection's
                 // middle crowds the crests, one coarser lets them out.
                 reads: "texture.spectralPeriodPx over the work's own frame side, read as a "
                      + "position on this handle's own range against the collection's own spread "
                      + "of that period. The same measurement the woven instrument's `wavePeriod` "
                      + "reads, so one number serves both",
                 applied: { hinge: FEEL_C_U0, reach: SPREAD_REACH,
                            curve: "a two-piece logarithm hinged at the module's own spacing, "
                                 + "liquid.js:391-410, band 2.58 to 1.31",
                            heldWholeAtADoor: { travel: DOOR_HOLD, readOn: "the drawing buffer",
                                                reads: "crestRequest",
                                                measures: "the water's own crossover against the "
                                                        + "tenth the handover's line stands beyond "
                                                        + "the height's own ceiling" } } },
        refract: { min: 0, max: 1, def: 0.45,
                   unit: "how far red and blue land apart at the bend",
                   // ALSO A POSITION. The module holds the split to a hair of 0.0032 of the frame
                   // and the collection's own finest detail runs about 2 points of a 1440-point
                   // side, which is 0.0014 — the same order, but the two are not one number and
                   // saying they were would be a scale nobody measured. What the handle takes is
                   // where the work's own detail stands inside the collection's spread: a work of
                   // fine detail splits least, because the split is what smears it first.
                   reads: "texture.detailPx over the work's own frame side, read as a position on "
                        + "this handle's own range against the collection's own spread of that "
                        + "detail — the split is what would smear the work's finest detail first",
                   applied: { hairAtWhole: 0.0032,
                              restsAt: "both doors, where the crossing dial is nothing" } },
        seed: { min: 0, max: SEED_SPAN, def: 0,
                unit: "the phase the swell stands at when the crossing opens",
                reads: "the score's own die. The travel is ONE WHOLE WAVE (liquid.js:364-368), so "
                     + "the two ends of the span stand the same picture and a die of nothing is the "
                     + "module's own rest" },
        shade: { min: 0, max: 1, def: 1,
                 unit: "the water's own light — the specular the bend catches and the light the "
                     + "height carries",
                 applied: { restsAt: "both doors" } },
        travel: { min: 0, max: 1, def: 1, unit: "the bend the picture rides",
                  applied: { restsAt: "both doors" } },
        // THE MEASUREMENT THIS HANDLE IS READ AGAINST AT A DOOR. `readAtADoor` says what is read
        // (the water's own height walked at the buffer's own sample points, with its ceiling beside
        // it), on which grid, what the reading is counted in, and how far the hold reaches.
        mask: { min: 0, max: 1, def: 0,
                applied: { readAtADoor: { field: MARGIN, readOn: "the drawing buffer",
                                          reads: "handover",
                                          measures: "the water's own height at the buffer's own "
                                                  + "sample points, and the widest its crossover "
                                                  + "stands there",
                                          held: DOOR_HOLD } } },
      },
      neutrals: { a: 0, b: 1 },
      doors: { in: { handle: "mix", value: 0, work: "a" },
               out: { handle: "mix", value: 1, work: "b" } },
      // BOTH DOORS FRAME AT A CROP OF EXACTLY ONE, and that is this instrument's own small luxury.
      // The module's breathing zoom of 1.055 is gated by the crossing dial, so at either door the
      // frame is the source cover-fitted and nothing else — no headroom bought from the picture,
      // because the swell's own displacement is tapered to nothing at the frame's edge and never
      // needs any.
      framings: { "0": { coverCrop: 1 }, "1": { coverCrop: 1 } },
      drivers: ["progress", "cueProgress", "time", "velocity", "capability", "noise", "static",
                "curve", "spline", "map", "add", "multiply", "mix", "clamp", "hold", "segment",
                "ramp", "slew", "oscillate", "node"],
      camera: { needs: "none", authority: "stage" },
      gl: { preserveDrawingBuffer: false },
      // WHAT THIS INSTRUMENT WRITES WHERE ITS OWN MATTER IS ABSENT (§7's coverage law, and the
      // per-instrument specification in docs/design/COVERAGE.md). It is absent nowhere: both branches
      // of the handover are photograph and the alpha is the constant 1. Under the placement rule this
      // instrument is lawful as the lowest cue of a stack and as a whole one-cue score.
      coverage: { writes: false,
                  how: "the handover mixes the two works at every point of the frame — one sheet of "
                     + "water carrying two pictures, both branches picture — so the alpha is the "
                     + "constant 1; at a door the water's own reading walks the buffer's sample "
                     + "points and refuses a door where any of them carries the other work" },
      // The neutral pose is the ENTRY DOOR — `mix` at 0, the value the `doors` block above names.
      neutralPose: { mix: 0, clock: 0, swell: 0.5, crest: FEEL_C_U0, refract: 0.45, seed: 0,
                     shade: 1, travel: 1, mask: 0, reduced: false,
                     cssWidth: 1000, cssHeight: 1000 },
      passes: [{
        program: "liquid", vert: VERT, frag: FRAG, position: "aPos",
        uniforms: [
          { name: "uA", type: "sampler2D", source: "textureA" },
          { name: "uB", type: "sampler2D", source: "textureB" },
          { name: "uFitA", type: "vec4", source: "fitA" },
          { name: "uFitB", type: "vec4", source: "fitB" },
          { name: "uRes", type: "vec2", source: "resolution" },
          { name: "uWave", type: "vec4", source: "frame:wave" },
          { name: "uDial", type: "vec4", source: "frame:dial" },
          { name: "uTime", type: "float", source: "frame:t" },
          { name: "uMask", type: "float", source: "handle:mask" },
        ],
      }],
      // The instrument allocates nothing of its own: it spends the two source-texture slots the host
      // already holds and the one programme the host builds from this manifest. The module's own
      // canvas, its context, its two field textures, its two framebuffers, its ping-pong and its own
      // frame loop are what this port does without.
      resources: { lean: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                           passes: 1, bytesEstimate: 0, variant: "lean" },
                   standard: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0,
                               programs: 1, passes: 1, bytesEstimate: 0, variant: "standard" },
                   rich: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                           passes: 1, bytesEstimate: 0, variant: "rich" } },
      capabilities: ["webgl2"],
      decline: ["one work only", "a source that never decoded"],
      provenance: { labPath: "lab/effects/liquid.js" },
      readiness: "production-ready",
    };

    var live = false;
    return {
      name: "liquid",
      manifest: manifest,
      values: values,
      fit: fit,
      feel: feelOf,
      prepare: function (o) {
        if (!o.sources) return { take: false, why: "the liquid instrument needs both works" };
        if (!o.cue) return { take: false, why: "no cue names it" };
        return { take: true };
      },
      start: function () { live = true; },
      // The pose the shader draws. The module's canvas, its frame loop, its pointer and its whole
      // simulation are gone, so every number here comes from a handle a score drives or from the
      // frame the host is about to bind.
      //
      // A DOOR THIS INSTRUMENT CANNOT KEEP WHOLE IS REFUSED RATHER THAN DRAWN. At either door it
      // walks its own water over the buffer the host is about to bind and, where a point of that
      // grid carries any share of the other photograph and letting the crests out does not close it,
      // it hands the host the reason with the measured numbers in it. The host recovers the
      // transaction on that reason and the walk's own glide carries the visitor, which is the
      // product's own behaviour with no renderer.
      frame: function (st) {
        if (!live) return;
        var h = st.handles;
        var pose = {
          mix: h.mix, swell: h.swell, crest: h.crest, refract: h.refract,
          seed: h.seed, shade: h.shade, travel: h.travel, mask: h.mask,
          t: h.clock, reduced: st.reduced,
          cssWidth: st.viewport.w, cssHeight: st.viewport.h,
          // THE GRID THE SHADER WILL SAMPLE ON, carried into the pose so the door is read on the
          // buffer the host is about to bind as `uRes` rather than on the CSS frame around it. The
          // host settles it from the device ratio and its own resolution step, so it moves while a
          // pass plays and each door is read on the grid standing at that door's own instant.
          bufWidth: st.viewport.bufferW, bufHeight: st.viewport.bufferH,
        };
        // AT A DOOR THE INSTRUMENT SAYS WHAT IT APPLIED, and says it before it refuses. `request` is
        // the crest spacing the score asked for and `applied` the one this grid could keep a whole
        // door at, so `moved` is the two read against each other in the handle's own units.
        if (h.mix === 0 || h.mix === 1) {
          var v = values(pose);
          if (st.reportApplied) {
            st.reportApplied({
              door: h.mix === 0 ? "in" : "out",
              buffer: [pose.bufWidth, pose.bufHeight],
              reads: "handover",
              request: v.crestRequest,
              applied: v.crestRequest + v.crestMoved,
              moved: v.crestMoved,
              unit: "the crest handle's own units",
              // What the water itself was doing over the frame at this door: how many of the walked
              // points carried the other work, how much field the tightest of them had to spare, and
              // how wide the crossover stood, so a door held whole says so about the water as well
              // as about the landing.
              wrong: v.water ? v.water.wrong : null,
              spareField: v.water ? v.water.spareField : null,
              band: v.water ? v.water.widestBand : null,
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
    instrument: liquidInstrument(),
  });
})();
