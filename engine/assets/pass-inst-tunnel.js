/*!pass-inst-tunnel.js*/
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
// OWNERSHIP. This instrument was carried over from lab/effects/tunnel.js. The artistic instruments
// and their manifests belong to tlvphotos, which builds these files from its own sources; the
// engine's copies are what ships until that handover lands.
(function () {
  var join = window.__@@NS@@PassInstrument;
  if (typeof join !== "function") return;

  // THIS FILE'S OWN VERSION, and the one home of that fact. The build reads this literal out of the
  // source and writes it into the site's record beside the digest, so the version a file declares
  // and the version a host was told to load cannot drift apart without the build noticing.
  var INSTRUMENT_VERSION = "1.0.0";

  // ================================================================================================
  // THE CORRIDOR INSTRUMENT (§8) — lab/effects/tunnel.js carried across
  // ================================================================================================
  // WHAT THE VISITOR SEES. The photograph stops being a flat picture and becomes a corridor the eye
  // falls down. A piece of the work is wrapped around a vanishing point and repeats away from the
  // viewer ring after ring, each ring turning the picture over so the joins carry no jump; the far
  // end sinks into a cold dark with a breath of light in the hole, the near ring stays bright, and
  // the whole corridor leans and wanders slowly as it falls. Then, out of the hole at the far end,
  // the ARRIVING work opens as a ring and comes toward the viewer, growing until it has washed past
  // the eye and the corridor is built of the second work alone. The corridor then closes back into a
  // flat picture, and what stands in the frame is the arriving work whole.
  //
  // WHERE IT STANDS ON THE CHARTER'S SHELF. lab/CROSSING-BRIEF.md's vocabulary table carries his own
  // standing verdict on this module: «tunnel | коридор | переход (mystery middle) | SURFACE |
  // approved; псевдо-тоннель В24 cut — the real corridor with interaction stays». Two things follow
  // and both are obeyed here. Its ROLE is the mystery middle of a crossing, which is what the three
  // acts below are. Its LEVEL is SURFACE — the levels law of shelf 17 keeps WORLD for the camera and
  // gives SURFACE to «floor, cylinder, ribbon», and a corridor is a cylinder. So this instrument
  // does NOT claim the world level and does not spend a crossing's one miracle: it is a passage a
  // quiet link may play as readily as a culmination.
  //
  // AND THE COMPOSER HAS BEEN ASKING FOR IT. engine/assets/pass-composer.js already names a corridor
  // as one of its three polar worlds (`POLAR_WORLD = { planet: "sphere", tunnel: "corridor",
  // twirl: "log-spiral" }`), and its own `middle-world` intent template reads «the flat picture
  // becomes a {worldName} the viewer stands inside». The corridor was the one world in that list
  // with no instrument behind it.
  //
  // ------------------------------------------------------------------------------------------------
  // THE THREE ACTS, AND WHY THE DOORS ARE EXACT
  // ------------------------------------------------------------------------------------------------
  // The dial `mix` walks one passage through three acts, with a dead band at either end where the
  // hand is already spent:
  //
  //   · THE CORRIDOR OPENS on the departing work. The module's own crossing dial walks the SAMPLE
  //     COORDINATE — never a colour crossfade — between the plain cover-fit point every straight
  //     photograph uses and the corridor wall the log-polar map worked out. One fetch answers every
  //     dial value, so the frame is one picture in sharp focus at every mark of the handle rather
  //     than two renderings of it laid over each other. That law and its wording are the lab
  //     module's own (tunnel.js:38-46) and this port carries it unchanged.
  //   · THE ARRIVING WORK COMES UP THE CORRIDOR. It stands beyond a STATION in the corridor's own
  //     depth axis, and the station travels toward the eye. On the frame that station is a RING —
  //     the level set of the depth axis is a circle about the vanishing point, leaned exactly as the
  //     corridor leans — so the second work opens out of the hole and grows until it has passed the
  //     eye. This is the one act the module never had, because the module carries one photograph and
  //     a crossing carries an ordered pair.
  //   · THE CORRIDOR CLOSES on the arriving work, by the same dial running back to nothing.
  //
  // THE DOORS ARE EXACT BY ARITHMETIC AND NOT BY A TOLERANCE. Inside the dead bands the dial is
  // exactly nothing, so `mix(flat, wall, dial)` is the plain cover-fit point and the lod spent on the
  // wall is nothing too; and the flood's own two gates are exactly 0 and exactly 1 there, so every
  // point of the frame reads one work. At `mix` 0 the frame is the departing work cover-fitted and
  // NOTHING ELSE — no crop, which is why `framings` publishes a cover crop of 1 at both doors, where
  // the folding instrument had to publish 1.90.
  //
  // ------------------------------------------------------------------------------------------------
  // IS THE RING A WIPE? THE THREE-PART TEST, ANSWERED ON ALL THREE COUNTS
  // ------------------------------------------------------------------------------------------------
  // lab/CROSSING-BRIEF.md's ban list convicts THE WIPE only where ALL THREE of its counts convict:
  // «(a) the boundary is imposed from outside the works' structure, AND (b) the two images never
  // interact, AND (c) the gesture reads as a quotation from television's vocabulary». A boundary
  // that travels across a frame has to answer that test out loud, so:
  //
  //   (a) THE BOUNDARY IS THE CORRIDOR'S OWN RING, and the corridor is built out of the departing
  //       work's own measurements: its centre is the pair's own measured radial centre, its ring
  //       spacing is the work's own measured ring repeat and its angular repeats are the work's own
  //       measured turn. Nothing about the boundary's shape or its place is chosen here — it is the
  //       level set of a depth axis whose every parameter is a reading of the photographs.
  //   (b) THE TWO IMAGES INTERACT ALONG THE WHOLE PASSAGE. They are the near and the far halves of
  //       ONE corridor: one geometry, one crop, one continuous depth axis, one lean, one fall. Each
  //       is drawn through the other's rings, they meet at a ring that carries a contact shade the
  //       way the corridor's own ring joins do, and the eye travels through the boundary rather than
  //       watching it slide past.
  //   (c) IT READS AS FALLING DOWN A CORRIDOR. What arrives is a place further down the corridor,
  //       reached by travelling, which is the opposite gesture from a shape swept across a screen.
  //
  // So the test acquits on all three counts, each by construction rather than by argument, and the
  // ban does not reach this instrument. The charter's own tail is the reason the question is asked
  // and answered here rather than left for a reader: «the difference is whose structure draws the
  // boundary».
  //
  // ------------------------------------------------------------------------------------------------
  // WHAT CAME OVER, AND WHAT STAYED BEHIND
  // ------------------------------------------------------------------------------------------------
  // WHAT CAME OVER, digit for digit, and the suite reads both files for each: the log-polar map and
  // its depth axis, the mirrored wrap across the picture, the ring-edge cross-fade, the lean, the
  // spiral shear and its slow breath, the drift the fall wanders on, the depth the fall starts at,
  // the crossing dial and the coordinate walk it drives, the contrast and the fog and the cold tint
  // and the hole at the far end and the breath of light in it and the vignette, and the three
  // expressions the module measures a pixel's own footprint with.
  //
  // WHAT STAYED BEHIND: the module's own canvas and context, its frame loop, its resize observer,
  // its texture uploads, its pointer — the hand that steered the fall and dived on a press — and
  // with the pointer the dive's own smear and field-of-view nudge, which the module computes from
  // the dive multiplier and which rest at nothing whenever nobody is pressing. The module's own
  // scored road (`poseAt`) already rests them there, and a scored corridor has no hand, so they are
  // carried as the module's own resting values and no uniform spends a slot on them.
  //
  // AND THE PER-PHOTOGRAPH CROP TABLE STAYED BEHIND, because it is exactly what his 19:13 word
  // forbids. The module carries `CROPS = [[0.26, 0.02, 0.48, 0.48], [0.22, 0.10, 0.56, 0.56]]`, two
  // rectangles typed by hand for two named photographs. Here the crop's PLACE is the pair's own
  // measured radial centre and its SIZE is the largest square that stands inside the picture about
  // that centre, held between the module's own two measured sides. See `cropOf`.
  //
  // ------------------------------------------------------------------------------------------------
  // THE ONE THING THAT COULD NOT CROSS: THE MIP CHAIN
  // ------------------------------------------------------------------------------------------------
  // The module uploads its own texture and calls `generateMipmap`, then picks the mip level by hand
  // — `fract()` breaks the automatic derivatives, so it measures the pixel's own footprint along the
  // depth axis and along the two angular ones and reads the picture at that level. The host uploads
  // both works with `LINEAR` filtering and NO mip chain (pass-layer.js's own `makeTex`), and §1.2's
  // fence leaves every texture to the host, so an instrument cannot build one.
  //
  // The measurement crosses; only the thing it was spent on changes. The three footprint expressions
  // are carried over word for word, divided by the crop's own texel counts so they read in the crop's
  // own units, and spent on FIVE TAPS spread over that footprint instead of on a mip level. The
  // pattern is a rotated cross, which is what an anisotropic footprint asks for: the corridor's
  // footprint is long along the depth axis and short across it near the eye, and the other way about
  // near the hole. `FOOT_MAX` caps the spread at a third of the crop, past which the far end is
  // already inside the hole the module blacks out. This is the port's own arithmetic and the file
  // says so; the suite levels it against the module by serving both roads at one tap and one level.
  function tunnelInstrument() {
    var VERT = [
      "attribute vec2 aPos;",
      "varying vec2 vUv;",
      // vUv runs 0 at the frame's top, the way an image's rows run, so the flat door's cover fit is
      // the plain seating the host hands and needs no flip of its own. The module flipped twice —
      // once because it uploaded its texture upside down and once to read it back — and the two
      // flips cancel into this one line.
      "void main(){ vUv = vec2(aPos.x * 0.5 + 0.5, 0.5 - aPos.y * 0.5); gl_Position = vec4(aPos, 0.0, 1.0); }",
    ].join("\n");

    var FRAG = [
      "precision highp float;",
      "precision highp sampler2D;",
      "varying vec2 vUv;",
      "uniform sampler2D uA;",     // the work the corridor is built of at the entry door
      "uniform sampler2D uB;",     // the work it is built of at the exit door
      "uniform vec4 uFitA;",       // both works' seating on this buffer, the host's own answer
      "uniform vec4 uFitB;",
      "uniform vec2 uRes;",
      // THE EYE: the frame's own ratio, the vanishing point the corridor falls toward, and the
      // field-of-view nudge, which rests at the module's own undriven 1.
      "uniform vec4 uCam;",
      // THE CORRIDOR'S SHAPE: the unit vector it leans toward, how hard it leans, and the log of the
      // ring size ratio — the module's own uLeanDir, uLean and uLogB.
      "uniform vec4 uLean;",
      // WHAT THE FALL HAS COME TO: the depth travelled, the spiral shear in radians per ring, the
      // angular repeats, and the crossing dial — 0 the flat photograph, 1 the corridor as the module
      // has always shipped it.
      "uniform vec4 uRing;",
      // THE STATION THE ARRIVING WORK STANDS BEYOND, in the corridor's own depth, and the gate on
      // the contact shade at the ring where the two works meet — nothing at either door.
      "uniform vec2 uWipe;",
      // The piece of each work the corridor's wall carries: xy the corner, zw the size.
      "uniform vec4 uCrop;",
      // The judges' channel: which work stands at this point of the corridor, and where in its crop.
      "uniform float uMask;",
      "",
      "const float TAU = 6.28318530718;",
      // THE FIVE TAPS' OWN CAP, in the crop's own units. Past a third of the crop the footprint is
      // reading the far end of the corridor, which the module's own hole has already blacked out.
      "const float FOOT_MAX = 0.3333;",
      // THE HOLE AT THE FAR END (tunnel.js:128), and the one place the wipe reads it. The depth axis
      // runs away without bound at the vanishing point, so the station could never stand beyond ALL
      // of it and the entry door could never be exact. Reading the wipe's own depth at the hole's own
      // radius closes that: inside the hole the corridor is blacked out and there is no picture to
      // hand over, so every point of it shares the hole's own place in the corridor and the depth the
      // station is compared against is bounded. That is what makes both doors exact by arithmetic
      // rather than by a fade.
      "const float HOLE = 0.115;",
      // THE CONTACT SHADE AT THE RING WHERE THE TWO WORKS MEET: how deep it goes at the ring itself
      // and how far it reaches into the corridor, in POINTS of the drawing buffer — the same reading
      // the folding instrument's own contact shadow is written in, so it is the same physical edge
      // whatever the fall is doing to the geometry. Both are gated to nothing at either door.
      "const float RING_SHADE = 0.30;",
      "const float RING_REACH = 7.0;",
      "",
      // seamless wrap across the picture: an even number of mirrored copies (tunnel.js:51)
      "float mirrorU(float x){ float m = fract(x * 0.5); return abs(m * 2.0 - 1.0); }",
      // a work cover-fitted into the frame, held off its own edge — the seating the host hands
      "vec2 into(vec2 p, vec4 f){",
      "  return clamp((p - 0.5) * f.xy + 0.5 + f.zw, 0.0008, 0.9992);",
      "}",
      "vec3 tex(vec2 c, float which){",
      "  return which < 0.5 ? texture2D(uA, c).rgb : texture2D(uB, c).rgb;",
      "}",
      // ONE POINT ON THE CORRIDOR WALL, and the crossing dial carried down to the fetch itself
      // (tunnel.js:56-58). `flat` is the plain cover-fit point this work's straight photograph uses;
      // the crop's own rectangle is the corridor wall; the dial walks the SAMPLE COORDINATE between
      // them, so one fetch answers every dial value and the frame is one picture in sharp focus at
      // every mark of the handle.
      "vec3 pick(vec2 t, float which, vec2 flat0){",
      "  return tex(mix(flat0, uCrop.xy + t * uCrop.zw, uRing.w), which);",
      "}",
      // THE PIXEL'S OWN FOOTPRINT, SPENT ON TAPS. A rotated cross over the footprint the module
      // measured: the corridor's footprint is long one way and short the other, and which way about
      // turns over between the eye and the hole, so the pattern has to be anisotropic. The taps
      // shrink to nothing with the dial, so the flat door is one fetch of one point.
      "vec3 pickF(vec2 t, vec2 foot, float which, vec2 flat0){",
      "  vec2 f = foot * uRing.w;",
      // A FOOTPRINT NARROWER THAN THE FILTER ALREADY IN THE TEXTURE NEEDS NO TAPS. Under a
      // thousandth of the crop's own side the four extra points land inside the bilinear filter the
      // host's own sampler already runs, so they would average one colour with itself at four times
      // the cost. Near the eye — which is most of the frame most of the time, and the whole frame at
      // both doors — this is one fetch of one point.
      "  if (max(f.x, f.y) < 0.001) return pick(t, which, flat0);",
      "  vec3 s = pick(t, which, flat0);",
      "  s += pick(t + vec2( f.x * 0.5,  f.y * 0.25), which, flat0);",
      "  s += pick(t - vec2( f.x * 0.5,  f.y * 0.25), which, flat0);",
      "  s += pick(t + vec2( f.x * 0.25, -f.y * 0.5), which, flat0);",
      "  s += pick(t - vec2( f.x * 0.25, -f.y * 0.5), which, flat0);",
      "  return s * 0.2;",
      "}",
      // The picture runs down the depth axis and turns around at each ring edge, so the joins carry
      // no jump; a short cross-fade with the neighbouring ring softens the turn itself
      // (tunnel.js:60-71).
      "vec3 wall(float zz, float um, vec2 foot, float which, vec2 flat0){",
      "  float f = fract(zz * 0.5);",
      "  float v = abs(f * 2.0 - 1.0);",
      "  vec3 a = pickF(vec2(um, v), foot, which, flat0);",
      "  float edge = smoothstep(0.90, 1.0, abs(v * 2.0 - 1.0));",
      "  if (edge > 0.001) {",
      "    float f2 = fract(zz * 0.5 + 0.5);",
      "    vec3 b = pickF(vec2(um, abs(f2 * 2.0 - 1.0)), foot, which, flat0);",
      "    a = mix(a, b, edge * 0.5);",
      "  }",
      "  return a;",
      "}",
      "",
      "void main(){",
      "  vec2 uv = vUv;",
      "  vec2 flatA = into(uv, uFitA);",
      "  vec2 flatB = into(uv, uFitB);",
      "  float asp = uCam.x;",
      "  vec2 p = (uv - uCam.yz) * 2.0 * vec2(asp, 1.0) * uCam.w;",
      "",
      "  float r = max(length(p), 1e-4);",
      "  vec2 dirp = p / r;",
      // leaning the corridor: rings ride nearer on one side, further on the other (tunnel.js:86-87)
      "  float leanF = max(1.0 + uLean.z * dot(dirp, uLean.xy), 0.22);",
      "  float rl = max(r * leanF, 1e-4);",
      "",
      "  float ang = atan(p.y, p.x);",
      "  float depth = log(rl) / uLean.w;",      // grows outward, one unit per ring
      "  float zz = uRing.x - depth;",
      "",
      "  float a2 = ang + uRing.y * depth;",     // spiral shear -> vortex
      "  float um = mirrorU(a2 / TAU * uRing.z);",
      "",
      // THE FOOTPRINT, in the crop's own units. These are the module's own three expressions
      // (tunnel.js:97-101) with the crop's texel counts divided back out, which is what makes them
      // independent of how big a file the visitor was served.
      "  float pxU = uRes.y * 0.5;",
      "  float fv  = 1.0 / (uLean.w * rl * pxU);",
      "  float fuT = uRing.z / (TAU * rl * pxU);",
      "  float fuR = abs(uRing.y) * uRing.z / (TAU * uLean.w * rl * pxU);",
      "  vec2 foot = vec2(min(max(fuT, fuR), FOOT_MAX), min(fv, FOOT_MAX));",
      "",
      // WHICH WORK STANDS AT THIS POINT OF THE CORRIDOR. The arriving work stands beyond the station
      // in the corridor's own depth; the boundary is antialiased over exactly one point of the
      // drawing buffer, read through the same depth axis the corridor is built on. The depth the
      // station is compared against is the one read at the hole's own radius or further out, which is
      // what bounds it and makes both doors exact.
      "  float rlw = max(rl, HOLE);",
      "  float zw = uRing.x - log(rlw) / uLean.w;",
      // THE BOUNDARY'S OWN FOOTPRINT IS READ WHERE ITS DEPTH IS READ, at the clamped radius and not
      // at the raw one. It is one point of the buffer measured in the wipe's own depth, so it is the
      // derivative of the very expression above; taking it at a radius running to nothing at the
      // vanishing point made the footprint run to infinity there, and a boundary antialiased over an
      // infinite band is a boundary that never lands — which is exactly how the exit door leaked one
      // point of arriving work at the far end of the corridor.
      "  float footZ = max(leanF / (uLean.w * rlw * pxU), 1e-6);",
      "  float ringPx = (zw - uWipe.x) / footZ;",
      "  float w = clamp(ringPx, 0.0, 1.0);",
      "",
      "  vec3 col;",
      "  if (w <= 0.0) {",
      "    col = wall(zz, um, foot, 0.0, flatA);",
      "  } else if (w >= 1.0) {",
      "    col = wall(zz, um, foot, 1.0, flatB);",
      "  } else {",
      "    col = mix(wall(zz, um, foot, 0.0, flatA), wall(zz, um, foot, 1.0, flatB), w);",
      "  }",
      "",
      // THE CONTACT SHADE AT THE MEETING RING, read in points of the drawing buffer and out at both
      // doors. It is what makes the two works meet at an edge of the corridor rather than at a line
      // drawn over it, and it is the same device the folding instrument uses at its crease.
      "  col *= 1.0 - RING_SHADE * uWipe.y * exp(-abs(ringPx) / RING_REACH);",
      "",
      // The finish below belongs to the corridor alone — none of it stands at either door — so every
      // term is gated to its own identity by the same dial the coordinate travelled on
      // (tunnel.js:113-134, carried digit for digit).
      "  float d = uRing.w;",
      "  float lum0 = dot(col, vec3(0.299, 0.587, 0.114));",
      "  col = clamp(mix(vec3(lum0), col, mix(1.0, 1.06, d)) * mix(1.0, 1.04, d) - 0.055 * d,",
      "              0.0, 1.0);",
      "  col = clamp((col - 0.46) * mix(1.0, 1.42, d) + mix(0.46, 0.40, d), 0.0, 1.0);",
      "",
      "  float fog = pow(smoothstep(0.004, 0.66, rl), 0.95);",
      "  float lum = dot(col, vec3(0.299, 0.587, 0.114));",
      "  col = mix(col, mix(vec3(lum) * vec3(0.62, 0.76, 0.98), col, 0.45 + 0.55 * fog), d);",
      "  col = mix(col, mix(vec3(0.016, 0.022, 0.036), col, fog), d);",
      "  col *= mix(1.0, 0.80 + 0.38 * smoothstep(0.05, 1.05, rl), d);",
      "  col *= mix(1.0, smoothstep(0.0, 0.115, rl), d);",
      "  col += d * vec3(0.20, 0.26, 0.34) * 0.22 * exp(-rl * 55.0);",
      "  vec2 q = (uv - 0.5) * 2.0;",
      "  col *= 1.0 - d * 0.20 * dot(q, q) * 0.5;",
      "  col = clamp(col, 0.0, 1.0);",
      "",
      // THE JUDGES' FRAME: which work stands at this point of the corridor, and where in that work's
      // own picture the point reads. It carries no coverage of its own because what it is for is to
      // be read as colour.
      "  vec2 loc = mix(flatA, uCrop.xy + vec2(um, abs(fract(zz * 0.5) * 2.0 - 1.0)) * uCrop.zw,",
      "                 uRing.w);",
      "  vec3 judge = vec3(w, clamp(loc.x, 0.0, 1.0), clamp(loc.y, 0.0, 1.0));",
      "  col = mix(col, judge, uMask);",
      // THE COVERAGE: the alpha is the constant 1, and it is a decision rather than a default. A
      // log-polar map answers every point of the plane, so this instrument has no absence to publish
      // and stands as the ground a stack is laid on.
      "  gl_FragColor = vec4(col, 1.0);",
      "}",
    ].join("\n");

    function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
    function smoothstep(a, b, x) {
      var t = (x - a) / (b - a);
      t = t < 0 ? 0 : t > 1 ? 1 : t;
      return t * t * (3 - 2 * t);
    }

    /* THE MODULE'S OWN NUMBERS, carried digit for digit (tunnel.js:166-168, :324, :360-366, :292).
       The three declared params are the fall's speed, the spiral shear and the angular repeats, each
       on its own published range with the module's own shipped value at the middle of nothing — they
       are what the module ships and what the vista preset «tunnel 26/16/10» of the charter's own
       taste-approved list stands at. FAR_REACH and RIBS_REACH are the two reaches the module states
       for the handles a score already drives it by; Z0 is the depth the fall starts at. */
    var SPEED_TOP = 1.15, SPEED_DEF = 0.26;
    var TWIST_TOP = 1.5, TWIST_DEF = 0.16;
    var REPS_DEF = 10, REPS_MIN = 4, REPS_MAX = 18;
    var FAR_REACH = 0.5, RIBS_REACH = 2.0;
    var Z0 = 0.35;

    /* THE DEAD BANDS AT EITHER END OF THE HAND. Over the first and last five hundredths of the dial
       the corridor stands exactly flat: the hand is spent there and the standing work is the picture
       its source carries, to the point. This is the folding instrument's own number and the same
       law — what makes a door a door and not a checkpoint. */
    var FEEL_D0 = 0.05;

    /* THE THREE ACTS, as shares of what is left of the dial after the dead bands. A third opens the
       corridor, a third carries the arriving work up it, a third closes it — which is shelf 17's own
       three-part reading of a crossing (disassembly, mystery, assembly) said in one number. The
       corridor stands whole for the whole middle act, so the arriving work never travels while the
       geometry is still moving and the two motions are never read at once. */
    var ACT = 1 / 3;

    /* THE CROP'S OWN TWO SIDES, and whose numbers they are (tunnel.js:143). The module carries two
       rectangles typed for two named photographs; his 19:13 word, lifted to the class at 19:21,
       makes a typed rectangle a finding rather than a constant. What is kept from the module is the
       SPAN its two crops stand in — 0.48 and 0.56 of the picture's side — and what replaces the
       table is the derivation in `cropOf`: the place is the pair's own measured radial centre and
       the side is the largest square that stands inside the picture about that centre, held inside
       the module's own span. */
    var CROP_MIN = 0.48, CROP_MAX = 0.56;

    /* THE DRIFT, a pure function of the second (tunnel.js:369-376). This is the wander of the fall
       when nobody is touching it, and under a handed second it is the whole of the fall's own
       motion: the module's scored road (`poseAt`) lands it straight, with no easing, because the
       ease is the HAND's channel and a scored corridor has no hand. */
    function driftAt(t) {
      return {
        tx: 0.5 + 0.115 * Math.sin(t * 0.19) + 0.045 * Math.sin(t * 0.077),
        ty: 0.5 + 0.100 * Math.cos(t * 0.15) + 0.038 * Math.cos(t * 0.058),
        lx: 0.20 * Math.sin(t * 0.13),
        ly: 0.20 * Math.cos(t * 0.11),
      };
    }

    /* THE SCORE'S DIE, read the way the folding instrument reads its own so one seeded score draws
       one picture. Here it is spent on the drift's own phase: two corridors falling on one second
       wander differently, which is what keeps a route from playing one corridor twice. A handle that
       is not a number answers with nothing rather than with a roll of the instrument's own, because
       an instrument that rolls its own die makes a seeded run draw two different pictures (§4.4b). */
    function seedFrom(v) {
      var n = +v;
      if (!(n === n) || n === Infinity || n === -Infinity) return 0;
      var s = Math.sin(n) * 43758.5453;
      return (s - Math.floor(s)) * 8;
    }

    // The angular repeats are an EVEN count, because the wrap across the picture is a mirrored pair
    // (tunnel.js:362-366): an odd count would put a seam where the mirror closes.
    function repsEven(n) {
      var k = Math.round(Number(n) || REPS_DEF);
      k = Math.round(k / 2) * 2;
      return clamp(k, REPS_MIN, REPS_MAX);
    }

    // ---- the grid one frame is drawn on ------------------------------------------------------------
    // The buffer the host is about to bind as `resolution`, with the CSS frame where it hands none
    // and a square where it hands neither. The corridor's whole geometry reads it: the frame's ratio
    // stands in every point of the map, and the footprint that decides the taps is read in the
    // buffer's own points. `drawn` says which of the two the reading below names.
    function gridOf(st) {
      var bw = Math.round(st.bufWidth), bh = Math.round(st.bufHeight);
      if (bw >= 1 && bh >= 1) return { w: bw, h: bh, drawn: true, given: true };
      var cw = Math.round(st.cssWidth), ch = Math.round(st.cssHeight);
      if (cw >= 1 && ch >= 1) return { w: cw, h: ch, drawn: false, given: true };
      return { w: 1, h: 1, drawn: false, given: false };
    }

    // Cover-fit a work into the frame, and nothing beyond it. The corridor asks for no crop of its
    // own: the log-polar map answers every point of the plane, so the frame needs no headroom and a
    // door stands the source cover-fitted and nothing else.
    function fit(iw, ih, w, h) {
      var fa = w / Math.max(h, 1);
      var ia = iw / Math.max(ih, 1);
      if (ia > fa) return [fa / ia, 1, 0, 0];
      return [1, ia / fa, 0, 0];
    }

    /* THE CROP, DERIVED FROM THE WORK'S OWN CENTRE. The piece of a photograph the corridor's wall
       carries is a square standing about the pair's own measured radial centre — the same reading
       the vanishing point itself is placed by, which is what makes the corridor fall toward the
       thing the photograph is already about. Its side is the largest square that stands inside the
       picture about that centre, held between the module's own two measured sides so the wall
       carries about as much picture as the module measured it should.

       A centre at the picture's middle therefore takes the module's own larger crop, and a centre
       near an edge takes its smaller one, and no rectangle is typed anywhere. */
    function cropOf(cx, cy) {
      var room = 2 * Math.min(Math.min(cx, 1 - cx), Math.min(cy, 1 - cy));
      var side = clamp(room, CROP_MIN, CROP_MAX);
      return [clamp(cx - side / 2, 0, 1 - side), clamp(cy - side / 2, 0, 1 - side), side, side];
    }

    // ---- the numbers of one frame ------------------------------------------------------------------
    // Everything the shader gets beyond the seating of the two works is a pure function of the pose,
    // and every number in the pose comes from a handle a score can drive. The one thing that moves
    // with time is the fall itself, which is the module's own `poseAt(t)`: a corridor that did not
    // fall would not be a corridor, so unlike the folding instrument this one publishes a `clock`
    // and the picture reads it.
    function posed(st) {
      var dial = clamp(st.mix, 0, 1);
      var grid = gridOf(st);
      var aspect = grid.w / Math.max(grid.h, 1);
      var t = Number(st.clock);
      if (!(t === t)) t = 0;
      var seed = seedFrom(st.seed);

      // THE THREE ACTS. `x` is the dial with the dead bands spent; `corridor` opens over the first
      // act, stands through the middle and closes over the last, and `flood` runs only while the
      // corridor stands whole.
      var x = clamp((dial - FEEL_D0) / (1 - 2 * FEEL_D0), 0, 1);
      var corridor = Math.min(smoothstep(0, ACT, x), smoothstep(1, 1 - ACT, x));
      var flood = clamp((x - ACT) / (1 - 2 * ACT), 0, 1);

      // THE FALL, the module's own scored road (tunnel.js:386-390) with the die spent on the drift's
      // own phase. Nothing eases: a handed second lands straight.
      var g = driftAt(t + seed);
      var speed = clamp(typeof st.depth === "number" ? st.depth : SPEED_DEF, 0, 1) * SPEED_TOP;
      var far = clamp(typeof st.centreX === "number" ? st.centreX : 0.5, 0, 1);
      var farY = clamp(typeof st.centreY === "number" ? st.centreY : 0.5, 0, 1);
      var cx = g.tx + (far - 0.5) * 2 * FAR_REACH;
      var cy = g.ty + (farY - 0.5) * 2 * FAR_REACH;
      var leanX = g.lx, leanY = g.ly;
      var z = Z0 + t * speed;

      // THE CORRIDOR'S OWN SHAPE, off the two handles that read the works' structure. `ribs` moves
      // the ring spacing in RATIOS, because the rings stand at even ratios of depth; `spokes` is the
      // angular repeat count, and the module's own uLogB is TAU over it.
      var ribs = clamp(typeof st.ribs === "number" ? st.ribs : 0.5, 0, 1);
      var reps = repsEven(typeof st.spokes === "number" ? st.spokes : REPS_DEF);
      var logB = (2 * Math.PI) / reps * Math.pow(RIBS_REACH, 1 - 2 * ribs);

      // THE SPIRAL SHEAR AND ITS SLOW BREATH (tunnel.js:433-434), carried whole.
      var twistH = clamp(typeof st.twist === "number" ? st.twist : TWIST_DEF, 0, 1) * TWIST_TOP;
      var breath = 0.78 + 0.22 * Math.sin((t + seed) * 0.147);
      var twist = twistH * breath + 0.07 * Math.sin((t + seed) * 0.093);

      var lean = Math.sqrt(leanX * leanX + leanY * leanY);
      var ldx = lean > 1e-5 ? leanX / lean : 1, ldy = lean > 1e-5 ? leanY / lean : 0;
      var leanAmt = Math.min(lean, 0.62);

      // WHERE THE STATION STANDS, in the corridor's own depth. It is placed against the frame's own
      // two extremes rather than at a number: at the flood's start it stands beyond the deepest point
      // of the frame, so no point reads the arriving work; at its end it stands nearer than the
      // frame's nearest point, so every point does. Both ends are then made exact by the two gates,
      // which is what carries the doors.
      var station = stationOf(z, logB, aspect, cx, cy, leanAmt, ldx, ldy, flood);
      // THE CROP IS PLACED BY THE MEASUREMENT AND NOT BY THE WANDER. The handle carries the pair's
      // own measured radial centre; the screen's vanishing point is that place plus the module's own
      // slow drift. The wall's rectangle is a piece of the PICTURE, so it stands where the
      // measurement says and holds still while the corridor wanders about it.
      var crop = cropOf(far, farY);

      return {
        cam: [aspect, cx, cy, 1],
        lean: [ldx, ldy, leanAmt, logB],
        ring: [z, twist, reps, corridor],
        // THE CONTACT SHADE BELONGS TO THE MEETING RING AND TO NOTHING ELSE, so it is out wherever
        // there is no meeting: at both doors, where the corridor is flat, and through the opening and
        // the closing acts, where one work holds the whole corridor and the station stands off the
        // frame.
        wipe: [station.at, corridor * smoothstep(0, 0.02, flood) * smoothstep(1, 0.98, flood)],
        crop: crop,
        // read on the diagnostic surface, bound to no uniform
        hand: dial, within: x, corridor: corridor, flood: flood,
        act: x < ACT ? "the corridor opens" : (x > 1 - ACT ? "the corridor closes"
                                                           : "the arriving work comes up it"),
        seconds: t, seed: seed, depthTravelled: z, speed: speed,
        reps: reps, logB: logB, ribs: ribs, twist: twist, breath: breath,
        centre: [cx, cy], leanAmount: leanAmt,
        stationFar: station.far, stationNear: station.near,
        mask: clamp(typeof st.mask === "number" ? st.mask : 0, 0, 1),
        coverCrop: 1,
        grid: grid,
        // BOTH WORKS' SEATING ON THIS GRID. The host answers it and its answer is the authority,
        // because the host is what binds the two uniforms; where the pose carries the two works'
        // own sizes instead, the seating is this instrument's OWN `fit` of them onto the same grid,
        // which is the very function the host calls to answer. A pose carrying neither leaves the
        // door reading unable to say what a cover fit even is, and it takes no reading at all.
        fitA: st.fitA || (st.aw && st.ah ? fit(st.aw, st.ah, grid.w, grid.h) : null),
        fitB: st.fitB || (st.bw && st.bh ? fit(st.bw, st.bh, grid.w, grid.h) : null),
      };
    }

    /* THE TWO ENDS THE STATION TRAVELS BETWEEN, read off the frame itself and not typed. A point of
       the frame stands at depth log(rl)/logB, so the frame's own deepest point is its farthest corner
       and its nearest is wherever the leaned radius is smallest — the vanishing point, where the
       radius runs to nothing and the depth runs away. The near end is therefore taken at the hole
       the module itself blacks out (rl = 0.115, tunnel.js:128): inside it there is no picture to
       hand over, and the two gates carry the last of the travel exactly. */
    var HOLE = 0.115;

    /* AND A LITTLE ROOM BEYOND EITHER END, so the doors are exact without a fade to make them so.
       The station's travel overshoots the frame's own two extremes by this much of the depth axis at
       both ends, which is about eight points of a phone's buffer at the hole and a hundred at the
       frame's corner — comfortably wider than the one point the boundary is antialiased over, and
       narrow enough that the arriving work is on its way within the first hundredths of its own act.
       Without it the two works would stand at half strength over the frame's far corner at the end
       of the travel, which is the colour crossfade this whole design exists to avoid. */
    var MARGIN = 0.25;

    function stationOf(z, logB, aspect, cx, cy, lean, ldx, ldy, flood) {
      var i, j, rlMax = 1e-4;
      for (i = 0; i < 2; i++) {
        for (j = 0; j < 2; j++) {
          var px = (i - cx) * 2 * aspect, py = (j - cy) * 2;
          var r = Math.max(Math.sqrt(px * px + py * py), 1e-4);
          var leanF = Math.max(1 + lean * ((px / r) * ldx + (py / r) * ldy), 0.22);
          rlMax = Math.max(rlMax, r * leanF);
        }
      }
      // beyond the frame's deepest point nothing reads the arriving work; nearer than the hole
      // everything does
      var far = z - Math.log(HOLE) / logB + MARGIN;
      var near = z - Math.log(Math.max(rlMax, HOLE)) / logB - MARGIN;
      return { at: far + (near - far) * flood, far: far, near: near };
    }

    // ---- THE DOOR THE INSTRUMENT READS FOR ITSELF --------------------------------------------------
    // His 18:00 architecture decision: the instrument reads its doors at runtime on the actual buffer,
    // and the report it hands back is the runtime truth; what the manifest declares is only the claim.
    //
    // WHAT A DOOR ASKS OF A CORRIDOR, and all three are read ON THE BUFFER rather than declared:
    //   · THE CORRIDOR IS FLAT. The dial walks the sample coordinate, so a dial left open means every
    //     point of the frame is reading somewhere other than where the plain cover fit says. That is
    //     a claim about WHERE A SAMPLE LANDS, so it is walked at the buffer's own sample points and
    //     the answer is published as the greatest distance any of them stands from its own cover-fit
    //     point, IN POINTS OF THE BUFFER — the same unit the picture is seen in.
    //   · ONE WORK STANDS, NOT TWO. The flood's gates make the entry door all departing work and the
    //     exit door all arriving work; a point reading the other work at a door is the door showing
    //     the wrong photograph, and the walk counts them.
    //   · THE JUDGES' CHANNEL IS SHUT. `mask` draws the corridor's own map as colour, which is what
    //     it is for; left open at a door the frame is a false-colour map and not the photograph.
    //
    // AND THERE IS NOTHING HERE TO HOLD. A corridor's flat door is exact by construction rather than
    // by a tolerance — the dead band spends the hand and the dial is exactly nothing inside it — so
    // anything this reading finds is a real fault that no widening closes, and the refusal stands
    // alone. `held` is therefore always nothing, and it says so rather than carrying a guard that
    // could never fire.
    var DOOR_SLIP = 0.5;         // points of the buffer: half a point, inside which a sample cannot move
    var DOOR_SHOW = 0.5 / 255;   // half a level of 255, an eighth of the charter's own 6-of-255 bar

    // The coordinate the shader will actually sample at one point of the frame, and the plain
    // cover-fit coordinate the door's own law asks for. Written from the shader's own lines so the
    // reading walks the very map the picture is drawn by.
    function readAt(v, px, py, W, H) {
      var uv = [px / W, py / H];
      var fit = v.wipeSide ? v.fitB : v.fitA;
      var flat = [clamp((uv[0] - 0.5) * fit[0] + 0.5 + fit[2], 0.0008, 0.9992),
                  clamp((uv[1] - 0.5) * fit[1] + 0.5 + fit[3], 0.0008, 0.9992)];
      var p = [(uv[0] - v.cam[1]) * 2 * v.cam[0] * v.cam[3],
               (uv[1] - v.cam[2]) * 2 * v.cam[3]];
      var r = Math.max(Math.sqrt(p[0] * p[0] + p[1] * p[1]), 1e-4);
      var leanF = Math.max(1 + v.lean[2] * ((p[0] / r) * v.lean[0] + (p[1] / r) * v.lean[1]), 0.22);
      var rl = Math.max(r * leanF, 1e-4);
      var depth = Math.log(rl) / v.lean[3];
      var zz = v.ring[0] - depth;
      var ang = Math.atan2(p[1], p[0]);
      var a2 = ang + v.ring[1] * depth;
      var m = a2 / (2 * Math.PI) * v.ring[2] * 0.5;
      var um = Math.abs((m - Math.floor(m)) * 2 - 1);
      var f = zz * 0.5;
      var vv = Math.abs((f - Math.floor(f)) * 2 - 1);
      var wallAt = [v.crop[0] + um * v.crop[2], v.crop[1] + vv * v.crop[3]];
      var drawn = [flat[0] + (wallAt[0] - flat[0]) * v.ring[3],
                   flat[1] + (wallAt[1] - flat[1]) * v.ring[3]];
      // the sample's own travel, said in points of the buffer: a step of the source's own coordinate
      // covers one frame width divided by the seating, so the seating is what turns the one into the
      // other
      var offX = (drawn[0] - flat[0]) / Math.max(fit[0], 1e-6) * W;
      var offY = (drawn[1] - flat[1]) / Math.max(fit[1], 1e-6) * H;
      // which work this point reads, by the shader's own line — the depth and its footprint both
      // read at the clamped radius, which is what makes the reading the shader's own
      var rlw = Math.max(rl, HOLE);
      var footZ = Math.max(leanF / (v.lean[3] * rlw * (H * 0.5)), 1e-6);
      var zw = v.ring[0] - Math.log(rlw) / v.lean[3];
      var w = clamp((zw - v.wipe[0]) / footZ, 0, 1);
      return { off: Math.sqrt(offX * offX + offY * offY), w: w };
    }

    // THE CORRIDOR, READ ON THE BUFFER THE SHADER WILL SAMPLE ON. The walk takes the buffer's own
    // sample points: its four corners, where the corridor is nearest the eye; the midpoints of its
    // four edges; the nine points around the buffer's own centre; and the nine points around THE
    // CORRIDOR'S OWN VANISHING POINT, which is a different place — the fall wanders, so the far end
    // of the corridor stands wherever the second has carried it. Those last nine are the ones that
    // matter: the hole at the far end is where the arriving work opens, so a fault in which work a
    // door reads shows there first and nowhere else on the frame.
    function doorReadOf(v, st) {
      var want = st.mix === 0 ? 0 : (st.mix === 1 ? 1 : -1);
      if (want < 0) return null;
      var g = v.grid;
      if (!g.given) return null;
      if (!v.fitA || !v.fitB) return null;
      v.wipeSide = want;
      var W = g.w, H = g.h, i, j, walked = 0, offPx = 0, wrong = 0;
      function walk(px, py) {
        var got = readAt(v, px, py, W, H);
        walked++;
        if (got.off > offPx) offPx = got.off;
        if (Math.abs(got.w - want) > 0.5) wrong++;
      }
      for (i = 0; i < 2; i++) {
        for (j = 0; j < 2; j++) { walk(i ? W - 0.5 : 0.5, j ? H - 0.5 : 0.5); }
      }
      walk(0.5, H * 0.5); walk(W - 0.5, H * 0.5); walk(W * 0.5, 0.5); walk(W * 0.5, H - 0.5);
      for (i = -1; i <= 1; i++) {
        for (j = -1; j <= 1; j++) { walk(W * 0.5 + i, H * 0.5 + j); }
      }
      var vx = clamp(v.cam[1], 0, 1) * W, vy = clamp(v.cam[2], 0, 1) * H;
      for (i = -1; i <= 1; i++) {
        for (j = -1; j <= 1; j++) { walk(vx + i, vy + j); }
      }
      return { walked: walked, offPx: offPx, wrong: wrong, dial: v.ring[3], mask: v.mask,
               grid: g, want: want, hole: [vx, vy] };
    }

    // THE REFUSAL, worded the way the host's own manifest refusals read: what is wrong, in this
    // instrument's own measured numbers, on the grid it was measured on.
    function doorWhyNoOf(read) {
      if (!read) return null;
      var g = read.grid, door = read.want ? "the exit" : "the entry";
      var work = read.want ? "arriving" : "departing";
      var other = read.want ? "departing" : "arriving";
      var where = " of a " + g.w + " x " + g.h + (g.drawn ? " buffer" : " frame");
      if (read.offPx >= DOOR_SLIP) {
        return door + " door leaks: the corridor stands " + read.dial.toFixed(6) + " open, so the "
             + "frame reads the " + work + " work " + read.offPx.toFixed(2) + " points" + where
             + " away from its own cover fit — a corridor wall and not the picture standing flat — "
             + "where " + door + " door's own law asks for that work at every point";
      }
      if (read.wrong) {
        return door + " door leaks: " + read.wrong + " of the " + read.walked + " points this "
             + "reading walked" + where + " read the " + other + " work, where " + door
             + " door's own law asks for the " + work + " work at every point";
      }
      if (read.mask >= DOOR_SHOW) {
        return door + " door leaks: the judges' own channel stands at " + read.mask.toFixed(6)
             + ", so the frame draws the corridor's own map over a " + g.w + " x " + g.h
             + (g.drawn ? " buffer" : " frame") + " instead of the " + work + " work, where " + door
             + " door's own law asks for the " + work + " work at every point";
      }
      return null;
    }

    // THE NUMBERS OF ONE FRAME, WITH ITS DOOR READ ON THE BUFFER BEING DRAWN. Away from a door this
    // is `posed` and nothing more: the reading is taken nowhere else.
    function values(st) {
      var v = posed(st);
      var read = doorReadOf(v, st);
      v.doorGrid = read ? read.grid : null;
      v.doorMap = read ? { walked: read.walked, offPx: read.offPx, wrong: read.wrong,
                           dial: read.dial } : null;
      v.doorHeld = null;
      v.doorWhyNo = doorWhyNoOf(read);
      return v;
    }

    // ONE TRAVELLING NUMBER, read on the diagnostic surface: how far the passage has come. The
    // corridor's opening, the arriving work's travel up it and its closing are the shape of it.
    function feelOf(u) {
      return clamp((clamp(u, 0, 1) - FEEL_D0) / (1 - 2 * FEEL_D0), 0, 1);
    }

    var manifest = {
      id: "tunnel", api: 1, arity: 2,
      // The photograph comes apart into a corridor, the arriving work comes up it out of the hole,
      // and the corridor closes on that work standing whole.
      roles: ["disassembly", "mystery", "assembly"],
      // WHERE THIS STANDS ON THE CHARTER'S SHELF, and the reading is carried rather than derived:
      // lab/CROSSING-BRIEF.md's vocabulary table records his own standing verdict on this module with
      // its level in the same row — SURFACE.
      //   · SURFACE — the flat frame becomes a cylinder the eye falls down. Shelf 17's levels law
      //     keeps WORLD for the camera and gives SURFACE «floor, cylinder, ribbon», so a corridor is
      //     a surface and this instrument spends no crossing's miracle.
      //   · CELL — the rings. The corridor is partitioned along its depth axis into rings, each
      //     carrying the picture turned over from its neighbour, and the ring is where the two works
      //     meet. That is the cell the composer's `KIND_OF_MEASURE` reads out of a `radial` pivot.
      // CELL CONTENT is not claimed: nothing inside a ring changes while it stands. TEXTURE and
      // LIGHT-COLOUR are not claimed either: the fog, the cold tint and the hole are the module's own
      // depth cue on one surface rather than a voice over a field.
      levels: ["SURFACE", "CELL"],
      params: { depth: [0, 1], ribs: [0, 1], spokes: [REPS_MIN, REPS_MAX], twist: [0, 1] },
      // EVERY handle a score can drive (§4.4b). `mix` is the dial and `clock` the second the host
      // hands down — a corridor that did not fall would not be a corridor, so unlike the folding
      // instrument this one reads a clock and the picture moves with it. The rest are the module's
      // own declared params and the two handles it already publishes for a score, each naming the
      // measurement of the photograph it derives from.
      handles: {
        // `mix` is the crossing's own dial and `clock` the module's own time; neither drives a
        // structural level of the picture.
        mix: { min: 0, max: 1, def: 0, level: null },
        clock: { min: 0, max: 14, def: 0, unit: "the second the fall is read at",
                 applied: { depthPerSecondAtWhole: SPEED_TOP, startsAt: Z0 }, level: null },
        // Where the corridor's own vanishing point stands is where its axis stands — a WORLD
        // reading — but this instrument deliberately does not claim WORLD (the header's own WHERE
        // IT STANDS ON THE CHARTER'S SHELF), so WORLD is not in its `levels` array. This falls back
        // to SURFACE, the nearest declared level: a placement of the whole frame's own vanishing
        // point rather than a repeating unit.
        centreX: { min: 0, max: 1, def: 0.5,
                   unit: "where the corridor's far point stands across the frame",
                   reads: "the midpoint of the two works' own measured radial centres, "
                        + "structure.radial.centre — the place each photograph's own structure "
                        + "turns about, so the corridor falls toward what the picture is already "
                        + "about",
                   applied: { reach: FAR_REACH,
                              restsAt: "the module's own wandering vanishing point at that second" },
                   level: "SURFACE" },
        centreY: { min: 0, max: 1, def: 0.5,
                   unit: "where the corridor's far point stands up the frame",
                   reads: "the midpoint of the two works' own measured radial centres, "
                        + "structure.radial.centre, read on the other axis",
                   applied: { reach: FAR_REACH,
                              restsAt: "the module's own wandering vanishing point at that second" },
                   level: "SURFACE" },
        // How fast the eye travels down the corridor is a WORLD reading (how near the eye stands to
        // it, moving), which this instrument does not claim; it falls back to SURFACE, the nearest
        // declared level, as the whole frame's own drift down the passage.
        depth: { min: 0, max: 1, def: SPEED_DEF,
                 unit: "how fast the fall travels down the corridor",
                 reads: "the departing work's own corridor reading, structure.polar.tunnel — a "
                      + "photograph whose depth already reads as a corridor is fallen down further "
                      + "in the same passage than one that barely does",
                 applied: { depthPerSecondAtWhole: SPEED_TOP, moduleShipsAt: SPEED_DEF },
                 level: "SURFACE" },
        // The rings' own spacing: CELL.
        ribs: { min: 0, max: 1, def: 0.5, unit: "how far apart the corridor's rings stand",
                reads: "the departing work's own measured ring repeat — structure.ownDevice.count "
                     + "where that work was cut as rings, and the work's own ring set's measured "
                     + "grain otherwise. The rings stand at even RATIOS of depth, so this handle "
                     + "moves the spacing in ratios too",
                applied: { reach: RIBS_REACH, restsAt: "the module's own spacing, TAU over the "
                                                     + "angular repeats" },
                level: "CELL" },
        // The angular repeat count: CELL.
        spokes: { min: REPS_MIN, max: REPS_MAX, def: REPS_DEF, kind: "enum", step: 2,
                  unit: "how many mirrored copies of the picture stand around the corridor",
                  reads: "the departing work's own measured turn, structure.rotational.n — how many "
                       + "times that photograph's structure comes round about its own centre, which "
                       + "is what an angular repeat is. Where the turn reads under its own floor the "
                       + "corridor takes that work's own ring count instead "
                       + "(structure.ownDevice.count where it was cut as rings), rounded to the "
                       + "nearest even count, because the wrap across the picture is a mirrored pair "
                       + "and an odd count would put a seam where the mirror closes",
                  level: "CELL" },
        // The rings' own phase shift: CELL.
        twist: { min: 0, max: 1, def: TWIST_DEF, unit: "the corridor's spiral shear",
                 reads: "the departing work's own measured twirl, structure.polar.twirl — the "
                      + "reading that says how far that photograph's structure already spirals about "
                      + "its centre, which is exactly what a shear per ring is",
                 applied: { radiansPerRingAtWhole: TWIST_TOP, moduleShipsAt: TWIST_DEF,
                            breathes: "0.78 to 1.00 of itself, on the module's own slow breath" },
                 level: "CELL" },
        seed: { min: 0, max: 8, def: 0, unit: "the ordered pair's own die",
                reads: "the score's own seed, spent on the phase of the drift the fall wanders on, "
                     + "so two corridors falling on one second wander differently and a route never "
                     + "plays one corridor twice",
                level: null },
        // THE MEASUREMENT THIS HANDLE IS READ AGAINST AT A DOOR. `readAtADoor` says what is read
        // (this instrument's own sample coordinate, walked at the buffer's own sample points), on
        // which grid, what the reading is counted in, and that there is no hold. It is the judges'
        // own channel and drives no structural level.
        mask: { min: 0, max: 1, def: 0,
                applied: { readAtADoor: { points: DOOR_SLIP, readOn: "the drawing buffer",
                                          reads: "flatness",
                                          measures: "how far this instrument's own sample coordinate "
                                                  + "stands from the door work's plain cover fit, "
                                                  + "walked at the buffer's own sample points, and "
                                                  + "how many of them read the other work",
                                          held: null } },
                level: null },
      },
      neutrals: { a: 0, b: 1 },
      doors: { in: { handle: "mix", value: 0, work: "a" },
               out: { handle: "mix", value: 1, work: "b" } },
      // BOTH DOORS FRAME ALIKE AND NEITHER IS CROPPED. A log-polar map answers every point of the
      // plane, so this instrument asks the frame for no headroom at all: at a door the picture is the
      // source cover-fitted and nothing else, which is the whole of the price this coverage is paid
      // with.
      framings: { "0": { coverCrop: 1 }, "1": { coverCrop: 1 } },
      drivers: ["progress", "cueProgress", "time", "velocity", "capability", "noise", "static",
                "curve", "spline", "map", "add", "multiply", "mix", "clamp", "hold", "segment",
                "ramp", "slew", "oscillate", "node"],
      camera: { needs: "none", authority: "stage" },
      // NO `gl.readsChain`, AND IT IS MEASURED RATHER THAN AN OVERSIGHT. The flag `beauty` added
      // on 2026-08-18 hands an instrument the walking minification filter for the length of its
      // own draw, and four instruments of this collection ask for it. This one must not: it
      // already spends the module's own footprint measurement on FIVE TAPS on a rotated cross,
      // which is its answer to the same minification, and a chained copy underneath those taps
      // is the same job done twice. Measured at the merge: with the flag declared the two roads
      // part at o3 (8.38 of 255 against a bar of 6) where they agree at 1.79 without it. The
      // module picks a level by hand where this port takes the taps, and the taps are what
      // crossed.
      gl: { preserveDrawingBuffer: false },
      // WHAT THIS INSTRUMENT WRITES WHERE ITS OWN MATTER IS ABSENT (§7's coverage law, and the
      // per-instrument specification in docs/design/COVERAGE.md). It is absent nowhere: a log-polar
      // map is defined at every point of the frame, so the alpha is the constant 1, said as a
      // decision. Under the placement rule this instrument is lawful as the lowest cue of a stack
      // and as a whole one-cue score.
      coverage: { writes: false,
                  how: "the corridor is a log-polar map of the whole plane, so every point of the "
                     + "frame stands on some ring of it at every place of the fall and the alpha is "
                     + "the constant 1; at a door the instrument walks the buffer's own sample "
                     + "points and refuses a door where any of them reads somewhere other than the "
                     + "door work's own cover fit" },
      // The neutral pose is the ENTRY DOOR — `mix` at 0, the value the `doors` block above names.
      neutralPose: { mix: 0, clock: 0, centreX: 0.5, centreY: 0.5, depth: SPEED_DEF, ribs: 0.5,
                     spokes: REPS_DEF, twist: TWIST_DEF, seed: 0, mask: 0,
                     reduced: false, cssWidth: 1000, cssHeight: 1000 },
      passes: [{
        program: "tunnel", vert: VERT, frag: FRAG, position: "aPos",
        uniforms: [
          { name: "uA", type: "sampler2D", source: "textureA" },
          { name: "uB", type: "sampler2D", source: "textureB" },
          { name: "uFitA", type: "vec4", source: "fitA" },
          { name: "uFitB", type: "vec4", source: "fitB" },
          { name: "uRes", type: "vec2", source: "resolution" },
          { name: "uCam", type: "vec4", source: "frame:cam" },
          { name: "uLean", type: "vec4", source: "frame:lean" },
          { name: "uRing", type: "vec4", source: "frame:ring" },
          { name: "uWipe", type: "vec2", source: "frame:wipe" },
          { name: "uCrop", type: "vec4", source: "frame:crop" },
          { name: "uMask", type: "float", source: "handle:mask" },
        ],
      }],
      // The instrument allocates nothing of its own: it spends the two source-texture slots the host
      // already holds and the one programme the host builds from this manifest. The module's own
      // canvas, its context, its two textures and its own frame loop are what this port does without.
      resources: { lean: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                           passes: 1, bytesEstimate: 0, variant: "lean" },
                   standard: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0,
                               programs: 1, passes: 1, bytesEstimate: 0, variant: "standard" },
                   rich: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                           passes: 1, bytesEstimate: 0, variant: "rich" } },
      capabilities: ["webgl2"],
      decline: ["one work only", "a source that never decoded"],
      provenance: { labPath: "lab/effects/tunnel.js", commit: "fc885a3",
                    sha256: "b10a51b402ae0ddb276297d1773e698d26d3268aec6e1db19ff7e27b224e7e3b" },
      readiness: "production-ready",
    };

    var live = false;
    return {
      name: "tunnel",
      manifest: manifest,
      values: values,
      fit: fit,
      feel: feelOf,
      prepare: function (o) {
        if (!o.sources) return { take: false, why: "the corridor instrument needs both works" };
        if (!o.cue) return { take: false, why: "no cue names it" };
        return { take: true };
      },
      start: function () { live = true; },
      // The pose the shader draws. The module's canvas, its frame loop and its pointer are gone, so
      // every number here comes from a handle a score drives or from the frame the host is about to
      // bind.
      //
      // A DOOR THIS INSTRUMENT CANNOT KEEP WHOLE IS REFUSED RATHER THAN DRAWN. At either door it
      // walks its own sample coordinate over the buffer the host is about to bind and, where a point
      // of that grid reads further from the door work's own cover fit than a sample can move, where
      // a point reads the other work, or where the judges' channel is left open, it hands the host
      // the reason with the measured numbers in it instead of drawing a door that is not the
      // photograph. The host recovers the transaction on that reason and the walk's own glide carries
      // the visitor, which is the product's own behaviour with no renderer.
      frame: function (st) {
        if (!live) return;
        var h = st.handles;
        var pose = {
          mix: h.mix, clock: h.clock, centreX: h.centreX, centreY: h.centreY, depth: h.depth,
          ribs: h.ribs, spokes: h.spokes, twist: h.twist, seed: h.seed, mask: h.mask,
          reduced: st.reduced,
          cssWidth: st.viewport.w, cssHeight: st.viewport.h,
          // THE GRID THE SHADER WILL SAMPLE ON, carried into the pose so the footprint the taps are
          // spread over is measured on the frame the host is about to bind as `uRes` and the door is
          // read on it rather than on the CSS frame around it.
          bufWidth: st.viewport.bufferW, bufHeight: st.viewport.bufferH,
          // BOTH WORKS' SEATING ON THAT BUFFER, which only the host can answer. The door reading
          // needs it: what a door asks is that the sample coordinate be the plain cover fit, and the
          // cover fit is the host's own number.
          fitA: st.fitA, fitB: st.fitB,
        };
        // AT A DOOR THE INSTRUMENT SAYS WHAT IT APPLIED, and says it before it refuses. The reading
        // is taken on the buffer this frame is drawn on, so it is the run-time truth his 18:00
        // decision asks for. `request` is the travel a flat door asks of the sample coordinate —
        // none — and `applied` is the travel this grid actually shows.
        if (h.mix === 0 || h.mix === 1) {
          var v = values(pose);
          if (st.reportApplied) {
            st.reportApplied({
              door: h.mix === 0 ? "in" : "out",
              buffer: [pose.bufWidth, pose.bufHeight],
              reads: "flatness", request: 0,
              applied: v.doorMap ? v.doorMap.offPx : null,
              moved: v.doorMap ? v.doorMap.offPx : null,
              unit: "points of the drawing buffer",
              // What the corridor itself was doing at this door: how far the dial stood open and how
              // many of the walked points read the other work.
              dial: v.doorMap ? v.doorMap.dial : null,
              wrong: v.doorMap ? v.doorMap.wrong : null,
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
    instrument: tunnelInstrument(),
  });
})();
