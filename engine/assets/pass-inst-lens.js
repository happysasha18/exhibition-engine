/*!pass-inst-lens.js*/
// One instrument, travelling as its own file (PASS-API-V1 §7/§8, his word of 2026-08-14 08:39: the
// engine knows no effect name and loads version-pinned opaque effect files).
//
// WHAT THIS FILE IS. One instrument and the mathematics it draws by: a name, a manifest declaring
// its passes, its uniforms with the source each is bound from, its handles and its doors, and the
// pure functions that answer the numbers of one frame.
//
// WHAT THIS FILE MAY NOT DO. It reads no wall clock, holds no listener, creates no WebGL context,
// loads no picture and touches no DOM (§1.2's fence). The host owns the canvas, the context, the
// frame loop, the clock, the camera and the transaction; the instrument owns the picture.
//
// OWNERSHIP. This instrument was carried over from lab/effects/lens.js. The artistic instruments
// and their manifests belong to tlvphotos, which builds these files from its own sources; the
// engine's copies are what ships until that handover lands.
(function () {
  var join = window.__@@NS@@PassInstrument;
  if (typeof join !== "function") return;

  // THIS FILE'S OWN VERSION, and the one home of that fact.
  var INSTRUMENT_VERSION = "1.0.0";

  // ================================================================================================
  // THE GLASS INSTRUMENT (§8) — lab/effects/lens.js carried across
  // ================================================================================================
  // WHAT THE VISITOR SEES. The departing work stands whole. A round glass opens out of nothing over
  // the place the work's own structure turns about, and everything the glass covers is folded: into
  // mirrored wedges, or wound about the glass's own middle and unwound exactly at its rim, or simply
  // brought nearer. The glass grows until the whole frame is inside it and the picture is nothing but
  // fold; under that fold the departing work gives way to the arriving one; then the glass closes
  // back to nothing and the arriving work stands whole. The rim carries the module's own glass — a
  // touch of lift inside it, a tight inner shade, one light hairline just inside the rim and one dark
  // one just outside — so it reads as a lens over a picture and not as a hole cut in one.
  //
  // ------------------------------------------------------------------------------------------------
  // HIS OWN STANDING VERDICT ON THIS EFFECT, AND WHAT IT COSTS THE PORT
  // ------------------------------------------------------------------------------------------------
  // lab/CROSSING-HISTORY.md's vocabulary table records `lens` as «блуждающая линза · оживление
  // (gallery) · CELL · mouse-mapping feature PARKED (his 09:42 «отдельная фича»)». Two things follow
  // and both are answered here rather than argued away:
  //
  //   · IT IS RECORDED AS AN ОЖИВЛЕНИЕ AND NOT AS A ПЕРЕХОД. The module's own dial is the lens's
  //     REACH, and a reach is not a passage: walked from nothing to whole it opens a glass over a
  //     standing wall and leaves the wall standing. So the module's dial cannot be this instrument's
  //     `mix`, and what carries the crossing is stated below as THE ONE ENVELOPE — the reach opens,
  //     holds while the two works change hands under the glass, and closes. Everything the module
  //     measured about its own reach — the curve, the exponent, the dead band — is carried into that
  //     envelope digit for digit; the envelope's shape is the port's own and it is named as such.
  //   · THE POINTER IS PARKED BY HIS WORD. The module's lens follows the hand, and where no hand is
  //     there it walks two sines of its own with literal rates. Both stayed in the lab: the glass
  //     here rests where the two works' own measured radial centres meet, which is a measurement of
  //     the pair, and it does not rove at all. The parked feature is not smuggled in under another
  //     name.
  //
  // ------------------------------------------------------------------------------------------------
  // THE ONE ENVELOPE, AND WHY THE PASSAGE HAS THIS SHAPE
  // ------------------------------------------------------------------------------------------------
  // The charter's fifth law of the model — one envelope couples the axes, so properties belonging to
  // one gesture cannot disagree — is what this instrument is built on. ONE number, the reach, carries
  // the whole passage:
  //
  //   · Over the first and last `FEEL_D0` of the hand the reach is exactly nothing. There is no
  //     glass anywhere in the frame, the fold is the identity map, the two works have not begun to
  //     change hands and the glass's own lift, shade and hairlines are gated out with the reach. So
  //     the frame at either door is the source cover-fitted into it and nothing else — no crop, no
  //     rim, no residue. THE DOOR IS EXACT BY CONSTRUCTION and not by a tolerance.
  //   · Over the first third the reach opens on the module's own measured response curve until the
  //     glass covers the whole frame; it holds covered through the middle third; it closes over the
  //     last third. That arc — reached over the first third, held through the middle, flat at both
  //     doors — is the one the camera lane landed and recorded on 2026-08-17, and it is taken from
  //     there rather than invented here.
  //   · THE TWO WORKS CHANGE HANDS ONLY WHILE THE GLASS COVERS THE FRAME, which is exactly the
  //     middle third. That is the charter's conjuror read straight: the content swap sits where the
  //     eye is led away. It is also the whole reason the reach has a plateau at all — a share of the
  //     arriving work standing on a point of the frame OUTSIDE the glass would be a plain dissolve
  //     between two photographs, which is the cheap-editor gesture his 08-08 10:28 word vetoes by
  //     name. The instrument does not declare that it never happens: `values` walks the buffer's own
  //     sample points at every pose and publishes how many of them stand outside the glass while the
  //     handover is running, and a suite row reddens when the plateau is taken out.
  //
  // ------------------------------------------------------------------------------------------------
  // THE WALL THAT STAYED BEHIND, AND WHAT STANDS IN ITS PLACE
  // ------------------------------------------------------------------------------------------------
  // The module draws a drifting grid of fourteen finished works into a 2D texture array, with a
  // seeded layer table that pushes copies of one work apart, a pitch, a gap and a vertical drift.
  // None of it could travel: a cue of this engine carries an ordered PAIR (§8's `arity: 2`), the host
  // binds two source textures and no more, and the module's own reason for the wall is that the fold
  // must reach past one tile «so the fold always gathers several works and never collapses into a
  // single dark picture» (lens.js:75-76).
  //
  // WHAT STANDS IN ITS PLACE IS THE WORK CONTINUED PAST ITS OWN EDGE BY MIRRORING — one triangle wave
  // per axis, which is the same law `pass-inst-unfold.js` already continues its sheet by and the same
  // law the mirror family of this collection is cut by. Inside the frame the plane IS the work,
  // point for point, so the doors need nothing done to them; past the frame the fold goes on
  // gathering picture without end and never meets a gap, a bar or a background. The wall's gap, its
  // pitch, its layer table, its seed and its drift stayed in the lab with the gallery page they were
  // for, and this instrument therefore rolls no die and publishes no seed.
  //
  // ------------------------------------------------------------------------------------------------
  // WHAT CAME OVER
  // ------------------------------------------------------------------------------------------------
  // The three glasses and every number in them — the kaleidoscope's gather, its reach past the rim
  // and its turn, the swirl's twist, its pull and the exact unwinding at the rim, the magnification
  // and the squeezed band that makes it read as glass; the glass itself — the lift inside, the inner
  // shade with its depth and its reach in points, the two hairlines with their offsets and their
  // weights, and the two colours they are drawn in; and the reach's own response curve, its exponent
  // and its dead band. Every one of them is carried digit for digit and the suite reads both files
  // for each.
  //
  // THE FOUR TEMPORAL LITERALS DID NOT COME OVER, and that is a decision. The module breathes: the
  // kaleidoscope spins at 0.075 and swells at 0.31, the swirl's twist breathes at 0.45. Not one of
  // those rates reads anything off a photograph, which his 19:13 word lifted to the class at 19:21
  // forbids, and all three exist to keep a STANDING gallery wall alive rather than to carry a
  // passage. So no `clock` handle is published, the spin stands at nothing and the two breaths stand
  // at their own middles — 2.30 and 0.78, which is what the module draws at the middle of its own
  // breath. Nothing in this picture moves with time; it moves with the hand.
  //
  // ------------------------------------------------------------------------------------------------
  // WHAT IT CUTS ON, AND WHAT A PAIR MUST READ FOR IT TO BE WORTH CASTING
  // ------------------------------------------------------------------------------------------------
  // A LENS IS RADIAL THROUGH AND THROUGH — a disc about a middle, an angular fold, a wind about that
  // middle, a magnification centred on it — so the element kind it cuts on is the RING, and the
  // wedge where a pair carries one. The composer already reaches that kind through the `radial`
  // measure, whose cut it names `rings_or_spokes` and `radial_unfold`; a kaleidoscope IS a radial
  // unfold. The meshing instrument has stood alone on that kind, which by the composer's own rule
  // means it plays every ring ground there is; a second instrument on the kind is a CHOICE the pair's
  // own readings decide, which is what his 18:56 word asks for one level below the roads.
  //
  // WHAT A PAIR MUST READ: the stronger of the two works reads radial at or over the collection's
  // own TIGHT floor. Under it the centre this glass rests on would not be the work's own point but a
  // made-up one, and every geometric parameter here is placed about that centre. The composer's
  // `INSTRUMENT_ASKS` is where that condition is stated in the composer's own terms, beside the two
  // panel instruments' own; it is stated here so the two readings cannot drift apart.
  //
  // ------------------------------------------------------------------------------------------------
  // THE COVERAGE: THIS INSTRUMENT FILLS THE FRAME
  // ------------------------------------------------------------------------------------------------
  // §7's coverage law asks every instrument to say where its own matter is absent. Here it is absent
  // nowhere, and the reason is the mirrored plane: every point of the frame samples the plane at some
  // point, the plane is the work continued without end, and the alpha is the constant 1. The
  // declaration is `writes: false`, which under the placement rule makes it lawful as the LOWEST cue
  // of a stack and as a whole one-cue score.
  function lensInstrument() {
    var VERT = [
      "attribute vec2 aPos;",
      "varying vec2 vUv;",
      "void main(){ vUv = vec2(aPos.x * 0.5 + 0.5, 0.5 - aPos.y * 0.5); gl_Position = vec4(aPos, 0.0, 1.0); }",
    ].join("\n");

    // ----------------------------------------------------------------------------------------------
    // THE SHADER
    // ----------------------------------------------------------------------------------------------
    // The module's own fragment shader, with the wall's sampler2DArray, its layer table, its pitch,
    // its gap and its drift taken out and the mirrored plane put in their place. The three glasses
    // and the rim are line for line the module's.
    var FRAG = [
      "precision highp float;",
      "varying vec2 vUv;",
      "uniform sampler2D uA;",            // the work the eye is leaving
      "uniform sampler2D uB;",            // the work it is arriving at
      "uniform vec4 uFitA;",
      "uniform vec4 uFitB;",
      "uniform vec2 uRes;",
      // THE GLASS'S PLACE AND ITS REACH: where its middle stands in points of the drawing buffer
      // (x across, y UP the frame, which is the sense the module's own `atan` is written in), how
      // far it reaches in the same points, and how many points of the buffer stand on one point of
      // the css frame — the module's own `uPx`, which is what makes the rim the same physical width
      // whatever the device.
      "uniform vec4 uLens;",
      // WHICH GLASS AND HOW DEEP: the rule (0 kaleidoscope, 1 swirl, 2 magnify), how many mirrored
      // wedges the kaleidoscope folds the disc into, how hard the swirl winds, and the reciprocal of
      // the magnification.
      "uniform vec4 uGlass;",
      // WHAT THE PASSAGE IS DOING: how far the two works have changed hands, and the weight the
      // glass itself is drawn at — the module's own `uDial`, which is nothing at both doors.
      "uniform vec2 uHand;",
      // The judges' channel: the glass map as colour.
      "uniform float uMask;",
      "",
      "const float TAU = 6.28318530718;",
      // THE KALEIDOSCOPE'S OWN THREE NUMBERS (lens.js:77-79). The fold reaches 2.30 times its own
      // radius into the plane so it always gathers more than one frame of picture; it reaches a
      // further fifth of the glass's own radius so the middle of the disc carries pattern instead of
      // the single point the fold collapses to; and it stands turned by 0.35 of a radian.
      "const float GATHER = 2.30;",
      "const float EDGE = 0.20;",
      "const float TURN0 = 0.35;",
      // THE SWIRL'S OWN THREE (lens.js:83-85): how far it winds at the middle in radians, the middle
      // of the module's own breath on that number, and how far it pulls the picture in toward the
      // middle. All three are nothing exactly at the rim, which is what lets the glass's edge cross
      // a picture without a seam.
      "const float TWIST_MAX = 3.6;",
      "const float BREATH = 0.78;",
      "const float PULL = 0.22;",
      // WHERE THE MAGNIFIER'S SQUEEZED BAND BEGINS (lens.js:89): the core is flat and the last
      // quarter of the radius is squeezed back to nothing at the rim, which is what makes it read as
      // glass rather than as a zoom.
      "const float RIM0 = 0.76;",
      // THE GLASS ITSELF (lens.js:136-146): the lift inside the rim, the inner shade's depth and its
      // reach in points of the buffer, the two hairlines' offsets and their common softness, and the
      // two colours they are drawn in.
      "const float LIFT = 1.045;",
      "const float SHADE_D = 0.30;",
      "const float SHADE_R = 7.0;",
      "const float HAIR = 1.7;",
      "const float HAIR_IN = 0.9;",
      "const float HAIR_OUT = 1.7;",
      "const vec3 LIT = vec3(0.96, 0.95, 0.92);",
      "const vec3 DARK = vec3(0.03, 0.03, 0.04);",
      "",
      // THE PLANE THE GLASS LOOKS AT. Past the frame's own edge the work does not stop and it does
      // not repeat: it MIRRORS, one triangle wave per axis — the law pass-inst-unfold.js continues
      // its sheet by, and the law the mirror family of this collection is cut by. Inside the frame
      // the wave is the identity, so the plane IS the work there, point for point.
      "float mirror1(float x){ float t = mod(x, 2.0); return 1.0 - abs(t - 1.0); }",
      // How a point of the plane reads its source: the cover fit the host applied, held off the
      // file's own edge (lens.js's own coverDraw, in the seating the host now owns).
      "vec2 into(vec2 p, vec4 f){ return clamp((p - 0.5) * f.xy + 0.5 + f.zw, 0.0008, 0.9992); }",
      "vec3 plane(vec2 q){",
      "  vec2 u = vec2(q.x / max(uRes.x, 1.0), 1.0 - q.y / max(uRes.y, 1.0));",
      "  vec2 m = vec2(mirror1(u.x), mirror1(u.y));",
      "  vec3 a = texture2D(uA, into(m, uFitA)).rgb;",
      "  vec3 b = texture2D(uB, into(m, uFitB)).rgb;",
      "  return mix(a, b, clamp(uHand.x, 0.0, 1.0));",
      "}",
      "",
      // A POINT OF THE FRAME, TAKEN TO THE POINT OF THE PLANE THE GLASS SHOWS THERE (lens.js:66-90).
      "vec2 glass(vec2 c, vec2 d, float r, float t, float R){",
      "  int rule = int(uGlass.x + 0.5);",
      "  if (rule == 0) {",
      // kaleidoscope: fold the disc into mirrored wedges of the plane
      "    float seg = TAU / max(uGlass.y, 1.0);",
      "    float a = atan(d.y, d.x);",
      "    a = abs(mod(a, seg) - seg * 0.5);",
      "    float rr = r * GATHER + EDGE * R;",
      "    return c + vec2(cos(a + TURN0), sin(a + TURN0)) * rr;",
      "  } else if (rule == 1) {",
      // swirl: wind hard at the middle, unwound exactly at the rim
      "    float k = 1.0 - t;",
      "    float amt = TWIST_MAX * clamp(uGlass.z, 0.0, 1.0) * k * k * BREATH;",
      "    float a = atan(d.y, d.x) + amt;",
      "    float rr = r * (1.0 - PULL * k * k);",
      "    return c + vec2(cos(a), sin(a)) * rr;",
      "  }",
      // magnify: a flat core, squeezed back to nothing in a band at the rim
      "  float k = mix(uGlass.w, 1.0, smoothstep(RIM0, 1.0, t));",
      "  return c + d * k;",
      "}",
      "",
      "void main(){",
      // the point of the frame in points of the drawing buffer, x across and y UP
      "  vec2 p = vec2(vUv.x * uRes.x, (1.0 - vUv.y) * uRes.y);",
      "  vec2 c = uLens.xy;",
      "  float R = uLens.z;",
      "  float px = max(uLens.w, 1.0);",
      "  vec2 d = p - c;",
      "  float r = length(d);",
      // Away from any glass at all `t` is put past the rim, so nothing below can read as inside it.
      "  float t = R > 0.0 ? r / R : 2.0;",
      "  vec2 q = p;",
      "  float inGlass = 0.0;",
      "  if (R > 0.0 && t < 1.0) { q = glass(c, d, r, t, R); inGlass = 1.0; }",
      "  vec3 col = plane(q);",
      "",
      // THE GLASS, gated by the same number the reach rides (lens.js:136-146). At either door the
      // weight is nothing, so a rim of no radius cannot leave one lit speck standing at the glass's
      // own middle.
      "  float w = clamp(uHand.y, 0.0, 1.0);",
      "  float ins = w * (1.0 - smoothstep(R - px, R + px, r));",
      "  col *= mix(1.0, LIFT, ins);",
      "  float sh = (1.0 - smoothstep(0.0, SHADE_R * px, R - r)) * ins;",
      "  col *= 1.0 - SHADE_D * sh;",
      // the bezel: a light hairline just inside the rim and a dark one just outside, so the rim stays
      // legible over a bright picture and over a dark one
      "  float lit  = w * (1.0 - smoothstep(0.0, HAIR * px, abs(r - (R - HAIR_IN * px))));",
      "  float dark = w * (1.0 - smoothstep(0.0, HAIR * px, abs(r - (R + HAIR_OUT * px))));",
      "  col = mix(col, LIT, lit * 0.80);",
      "  col = mix(col, DARK, dark * 0.60);",
      "",
      // THE GLASS MAP, the judges' own frame: whether this point stands inside the glass, how far the
      // two works have changed hands, and where in the glass the point lies. It carries no coverage
      // of its own because what it is for is to be read as colour.
      "  vec3 judge = vec3(inGlass, clamp(uHand.x, 0.0, 1.0), clamp(t, 0.0, 1.0));",
      "  col = mix(col, judge, uMask);",
      // THE COVERAGE: the alpha is the constant 1, and it is a decision rather than a default. The
      // plane is the work continued without end, so this instrument has no absence to publish.
      "  gl_FragColor = vec4(col, 1.0);",
      "}",
    ].join("\n");

    function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
    function num(v, dflt) {
      var n = Number(v);
      return (n === n && n !== Infinity && n !== -Infinity) ? n : dflt;
    }
    function smoothstep(a, b, x) {
      var t = (x - a) / (b - a);
      t = t < 0 ? 0 : t > 1 ? 1 : t;
      return t * t * (3 - 2 * t);
    }

    /* THE REACH'S OWN RESPONSE CURVE, carried whole from the module (lens.js:371-390, the darkroom
       draft's D2 on his word of 08-08 17:57). Equal movements of the hand produce equal felt change,
       and the module fitted that on its own frame: a lens covers AREA, the frame it takes goes as
       the square of its radius, so the raw reach's first seventh does nothing the eye can find and
       its last third does everything. The family is a power curve — Stevens' law in its plainest
       form, v = u^g — and g = 0.42 is the module's one fitted number, near the 1/2 the area argument
       predicts. The module's own judged run reads the band this leaves at 1.33 against the 1.34 it
       was fitted at (lab/data/effects-dials-check.txt, «блуждающая линза»).

       AND THE DEAD BAND, WHICH IS THE SAME NUMBER DOING THE JOB IT WAS MEASURED FOR. The module
       measured that below 0.14 of the raw travel the lens has no footprint at all — under 0.06
       channels a step — and started its curve there so the hand never spends travel on nothing.
       Here that band is spent at the DOORS instead, where a door needs exactly nothing rather than
       nearly nothing, and the curve runs over what is left. So the module's two numbers cross over
       unchanged and each is doing what it was measured to do. */
    // DERIVED — the module's own measured response curve, carried digit for digit, and the block
    // above names the module, the lines and the measurement it came off (S-71, 2026-09-03).
    var FEEL_D0 = 0.14, FEEL_G = 0.42;

    /* THE ARC THE REACH RIDES, and it is the port's own — the module has no passage to shape.
       Reached over the first third, held through the middle, flat at both doors: the arc the camera
       lane measured and landed on 2026-08-17 for the plane's attitude, taken from there rather than
       chosen here. The plateau is not decoration: it is the stretch the two works are allowed to
       change hands over, and outside it they may not. */
    var HOLD_IN = 1 / 3, HOLD_OUT = 2 / 3;

    /* HOW FAR PAST THE FRAME'S FARTHEST CORNER THE RIM HAS TO STAND at the plateau, in points of the
       drawing buffer, and it is derived rather than chosen: the glass's inner shade reaches SHADE_R
       points inside the rim (lens.js:139) and its dark hairline stands HAIR_OUT points outside it and
       fades over HAIR more (lens.js:144). Seven points is the larger of the two, so a rim standing
       seven points past the farthest corner keeps every part of the glass off the frame while the
       frame is inside the glass — otherwise a hairline would sit across the frame's own corners
       through the whole middle third, which is the one place this instrument shows no rim at all. */
    var RIM_ROOM = 7.0;

    /* THE MODULE'S OWN THREE GLASSES, and the numbers each of them rests at (lens.js:277). The rule
       rests at the kaleidoscope, which is the module's own default; the wedge count rests at the six
       the module folds into; the twist rests whole; and the magnification rests at the module's own
       two. */
    var RULES = ["kaleidoscope", "swirl", "magnify"];
    var WEDGES_N = 6, WEDGES_LO = 3, WEDGES_HI = 12;
    var TWIST_REST = 1;
    var POWER_REST = 2, POWER_LO = 1, POWER_HI = 4;

    // ---- the grid one frame is drawn on ------------------------------------------------------------
    // The buffer the host is about to bind as `resolution`, with the CSS frame where it hands none
    // and a square where it hands neither. `drawn` says which of the two the reading below names.
    function gridOf(st) {
      var bw = Math.round(num(st.bufWidth, 0)), bh = Math.round(num(st.bufHeight, 0));
      var cw = Math.round(num(st.cssWidth, 0)), ch = Math.round(num(st.cssHeight, 0));
      if (bw >= 1 && bh >= 1) {
        return { w: bw, h: bh, drawn: true, given: true,
                 px: (ch >= 1) ? Math.max(1, bh / ch) : 1 };
      }
      if (cw >= 1 && ch >= 1) return { w: cw, h: ch, drawn: false, given: true, px: 1 };
      return { w: 1, h: 1, drawn: false, given: false, px: 1 };
    }

    // ---- the numbers of one frame ------------------------------------------------------------------
    // Everything the shader gets beyond the seating of the two works is a pure function of the pose,
    // and every number in the pose comes from a handle a score can drive. NOTHING HERE READS A CLOCK.

    // HOW FAR THE GLASS HAS OPENED, on the module's own curve inside the port's own arc. Exactly
    // nothing inside the two dead bands, exactly whole across the middle third.
    function reachOf(mix) {
      if (mix <= FEEL_D0 || mix >= 1 - FEEL_D0) return 0;
      if (mix >= HOLD_IN && mix <= HOLD_OUT) return 1;
      var u = mix < HOLD_IN ? (mix - FEEL_D0) / (HOLD_IN - FEEL_D0)
                            : ((1 - FEEL_D0) - mix) / ((1 - FEEL_D0) - HOLD_OUT);
      return Math.pow(clamp(u, 0, 1), FEEL_G);
    }

    // HOW FAR THE TWO WORKS HAVE CHANGED HANDS. Exactly nothing up to the plateau and exactly whole
    // from its far end, so the handover lives inside the stretch the glass covers the frame over and
    // nowhere else.
    function handoverOf(mix) {
      return smoothstep(HOLD_IN, HOLD_OUT, clamp(mix, 0, 1));
    }

    // THE RADIUS THAT PUTS THE WHOLE FRAME INSIDE THE GLASS, from wherever the glass stands: the
    // farthest of the frame's four corners, plus the room the rim's own drawing needs.
    function coverOf(cx, cy, W, H, px) {
      var most = 0, i, j, dx, dy;
      for (i = 0; i < 2; i++) {
        for (j = 0; j < 2; j++) {
          dx = (i ? W : 0) - cx;
          dy = (j ? H : 0) - cy;
          most = Math.max(most, Math.sqrt(dx * dx + dy * dy));
        }
      }
      return most + RIM_ROOM * px;
    }

    function ruleOf(st) {
      var r = Math.round(clamp(num(st.fold, 0), 0, RULES.length - 1));
      return r;
    }

    function posed(st) {
      var dial = clamp(num(st.mix, 0), 0, 1);
      var grid = gridOf(st);
      var W = grid.w, H = grid.h, px = grid.px;
      // WHERE THE GLASS RESTS. The record's own centres are read from the top of the frame; the
      // shader's own y runs up it, which is the sense the module's `atan` is written in, so the
      // second of the two is turned over here and in one place only.
      var cx = clamp(num(st.centreX, 0.5), 0, 1) * W;
      var cy = (1 - clamp(num(st.centreY, 0.5), 0, 1)) * H;
      var open = reachOf(dial);
      var cover = coverOf(cx, cy, W, H, px);
      var R = open * cover;
      var hand = handoverOf(dial);
      var weight = clamp(num(st.shade, 1), 0, 1) * open;
      var rule = ruleOf(st);
      var wedges = Math.round(clamp(num(st.wedges, WEDGES_N), WEDGES_LO, WEDGES_HI));
      var twist = clamp(num(st.twist, TWIST_REST), 0, 1);
      var power = clamp(num(st.power, POWER_REST), POWER_LO, POWER_HI);
      return {
        lens: [cx, cy, R, px],
        glass: [rule, wedges, twist, 1 / power],
        hand: [hand, weight],
        // read on the diagnostic surface, bound to no uniform
        dial: dial, open: open, reach: R, cover: cover, handover: hand, weight: weight,
        rule: RULES[rule], wedges: wedges, twist: twist, power: power,
        centre: [cx, cy], holdIn: HOLD_IN, holdOut: HOLD_OUT, band: FEEL_D0, rimRoom: RIM_ROOM,
        mask: clamp(num(st.mask, 0), 0, 1),
        grid: grid,
      };
    }

    // ---- THE READING THE INSTRUMENT TAKES ON THE BUFFER IT DRAWS ON --------------------------------
    // His 18:00 architecture decision: the instrument reads its doors at runtime on the actual
    // buffer, and the report it hands back is the runtime truth; what the manifest declares is only
    // the claim. This instrument's unit is THE GLASS — where its rim stands over the frame — and it
    // is read twice, because this instrument makes two claims about it rather than one:
    //
    //   · AT A DOOR there is no glass anywhere. Every sample point of the buffer must stand outside
    //     the rim, the two works must have finished changing hands (or not begun), and the judges'
    //     channel must be shut. What the walk publishes beside the count is how much room the
    //     tightest of those points had, in points of the grid.
    //   · WHILE THE TWO WORKS CHANGE HANDS the glass must cover the frame. Every sample point must
    //     stand INSIDE the rim, or a share of the arriving work stands on a point of the plain
    //     departing work and the frame is a dissolve between two photographs. This is read at every
    //     pose, not only at a door, because the fault it catches is a fault in the middle.
    //
    // The walk takes the buffer's own sample points: its four corners, where the glass has the least
    // room to spare; the midpoints of its four edges; and the nine points around its middle, where
    // the glass first opens.
    function walkPoints(W, H) {
      var pts = [], i, j;
      for (i = 0; i < 2; i++) {
        for (j = 0; j < 2; j++) { pts.push([i ? W - 0.5 : 0.5, j ? H - 0.5 : 0.5]); }
      }
      pts.push([0.5, H * 0.5]); pts.push([W - 0.5, H * 0.5]);
      pts.push([W * 0.5, 0.5]); pts.push([W * 0.5, H - 0.5]);
      for (i = -1; i <= 1; i++) {
        for (j = -1; j <= 1; j++) { pts.push([W * 0.5 + i, H * 0.5 + j]); }
      }
      return pts;
    }

    // THE GLASS, READ ON THE BUFFER THE SHADER WILL SAMPLE ON. `inside` counts the sample points the
    // glass stands over; `spare` is how far the tightest point stands from the rim, in points of the
    // grid, positive when it is outside the glass and negative when it is inside.
    function glassReadOf(v, W, H) {
      var pts = walkPoints(W, H), cx = v.lens[0], cy = v.lens[1], R = v.lens[2];
      var inside = 0, nearest = 1e9, farthest = -1e9, i, dx, dy, r, gap;
      for (i = 0; i < pts.length; i++) {
        // the walk is in the shader's own space: x across the buffer, y UP it
        dx = pts[i][0] - cx;
        dy = (H - pts[i][1]) - cy;
        r = Math.sqrt(dx * dx + dy * dy);
        gap = r - R;
        if (R > 0 && gap < 0) inside += 1;
        if (gap < nearest) nearest = gap;
        if (gap > farthest) farthest = gap;
      }
      return { walked: pts.length, inside: inside, nearestPx: nearest, farthestPx: farthest,
               outside: pts.length - inside };
    }

    // WHAT THE INSTRUMENT CLAIMS ABOUT THE HANDOVER, MEASURED. Null wherever the two works are not
    // changing hands, since a frame that is wholly one work or wholly the other has no claim to keep.
    function handReadOf(v, read) {
      if (!(v.handover > 0) || !(v.handover < 1)) return null;
      return { walked: read.walked, bare: read.outside, sparePx: -read.farthestPx,
               handover: v.handover };
    }

    function handWhyNoOf(v, hr, g) {
      if (!hr || !hr.bare) return null;
      return "the two works are " + (v.handover * 100).toFixed(1) + " per cent of the way through "
           + "changing hands and the glass stands over only part of the frame: " + hr.bare + " of "
           + hr.walked + " points of a " + g.w + " x " + g.h + (g.drawn ? " buffer" : " frame")
           + " carry a share of both photographs with no fold over them, which is a plain dissolve "
           + "between two pictures and not a glass";
    }

    // THE DOOR, MEASURED. Null everywhere but at a door, since away from the doors an open glass is
    // the picture rather than a fault.
    var DOOR_SLIP = 0.5;         // points of the grid: half a point, inside which a sample cannot move
    // How much of the judges' channel may stand in the frame at a door and it still BE the
    // photograph: half a level of 255, an eighth of the charter's own 6-of-255 door bar at one point.
    // CAPABILITY — a fact about the frame's own eight bits rather than about pictures: half of
    // one level of 255 is under the smallest difference the buffer can carry, so a door reading
    // at this bar is reading something the frame could not have shown. Settled once for the nine
    // files that carry it (S-71, 2026-09-03).
    var DOOR_SHOW = 0.5 / 255;

    function doorReadOf(v, st) {
      var want = st.mix === 0 ? 0 : (st.mix === 1 ? 1 : -1);
      if (want < 0) return null;
      var g = v.grid;
      if (!g.given) return null;
      var read = glassReadOf(v, g.w, g.h);
      read.grid = g;
      read.want = want;
      read.reach = v.reach;
      read.handover = v.handover;
      read.mask = v.mask;
      return read;
    }

    // THE REFUSAL, worded the way the host's own manifest refusals read: what is wrong, in this
    // instrument's own measured numbers, on the grid it was measured on.
    function doorWhyNoOf(read) {
      if (!read) return null;
      var g = read.grid, door = read.want ? "the exit" : "the entry";
      var work = read.want ? "arriving" : "departing";
      var other = read.want ? "departing" : "arriving";
      var where = " of a " + g.w + " x " + g.h + (g.drawn ? " buffer" : " frame");
      if (read.reach > DOOR_SLIP || read.inside) {
        return door + " door leaks: the glass still reaches " + read.reach.toFixed(2) + " points"
             + where + " and stands over " + read.inside + " of the " + read.walked + " points this "
             + "reading walked, so the frame is the " + work + " work folded rather than standing, "
             + "where " + door + " door's own law asks for that work whole at every point";
      }
      var slip = read.want ? (1 - read.handover) : read.handover;
      if (slip > DOOR_SHOW) {
        return door + " door leaks: the two works stand " + (slip * 100).toFixed(2) + " per cent of "
             + "the way toward the " + other + " one, so the frame is a blend of both photographs "
             + "where " + door + " door's own law asks for the " + work + " work at every point";
      }
      if (read.mask >= DOOR_SHOW) {
        return door + " door leaks: the judges' own channel stands at " + read.mask.toFixed(6)
             + ", so the frame draws the glass map over a " + g.w + " x " + g.h
             + (g.drawn ? " buffer" : " frame") + " instead of the " + work + " work, where " + door
             + " door's own law asks for the " + work + " work at every point";
      }
      return null;
    }

    // THE NUMBERS OF ONE FRAME, WITH THE GLASS READ ON THE BUFFER BEING DRAWN.
    function values(st) {
      var v = posed(st);
      var g = v.grid;
      var read = g.given ? glassReadOf(v, g.w, g.h) : null;
      var door = doorReadOf(v, st);
      v.glassMap = read ? { walked: read.walked, inside: read.inside, outside: read.outside,
                            nearestPx: read.nearestPx, farthestPx: read.farthestPx } : null;
      var hr = read ? handReadOf(v, read) : null;
      v.handMap = hr;
      v.handWhyNo = hr ? handWhyNoOf(v, hr, g) : null;
      v.doorGrid = door ? door.grid : null;
      v.doorHeld = null;
      v.doorWhyNo = doorWhyNoOf(door);
      return v;
    }

    // Cover-fit a work into the frame, and nothing beyond it. This instrument asks the host for no
    // crop at either door: the plane IS the work inside the frame, so what a door shows is the plain
    // cover fit and the `framings` block publishes 1.
    function fit(iw, ih, w, h) {
      var fa = w / Math.max(h, 1);
      var ia = iw / Math.max(ih, 1);
      if (ia > fa) return [fa / ia, 1, 0, 0];
      return [1, ia / fa, 0, 0];
    }

    // ONE TRAVELLING NUMBER, read on the diagnostic surface: how far the glass has opened.
    function feelOf(u) { return reachOf(clamp(num(u, 0), 0, 1)); }

    var manifest = {
      id: "lens", api: 1, arity: 2,
      // The glass opens over the departing work and folds it, the fold is the whole frame while the
      // two works change hands under it, and the arriving work is left standing whole.
      roles: ["disassembly", "mystery", "assembly"],
      // WHERE THIS STANDS ON THE CHARTER'S SHELF. lab/CROSSING-HISTORY.md's vocabulary table records
      // this module at CELL and this port keeps that reading rather than growing it:
      //   · SURFACE — the fold is one map over one surface, and the plane it reads is the work
      //     continued past its own edge. Nothing here stands in a space with a camera in it.
      //   · CELL — under the kaleidoscope the disc is partitioned into mirrored wedges, which are
      //     cells the eye reads as cells.
      // WORLD IS NOT CLAIMED, deliberately. Claiming it would spend the crossing's one miracle
      // (shelf 6, and the composer reads exactly this field to decide it), and nothing here folds
      // the space a work lives in: the glass is a map over a picture, not a solid the eye walks
      // round. So a quiet link and a return can reach this instrument, which is where a route's
      // breadth is won or lost.
      levels: ["SURFACE", "CELL"],
      // THE ELEMENT KINDS THIS INSTRUMENT CUTS ON, declared here so the wire's own table is read off
      // the manifest rather than kept as a second copy of it. A lens is radial: a disc about a
      // middle, an angular fold, a wind about that middle. The condition a pair must meet is above.
      cuts: ["ring", "wedge"],
      // WHERE THIS INSTRUMENT HAS A SEAM (§8's `seams` block, pass-layer.js). Two edges, because the
      // two cuts above are drawn by two different mechanisms and neither is the module's own crossfade.
      // THE WEDGE is the kaleidoscope's own fold, `a = abs(mod(a, seg) - seg * 0.5)` in the shader
      // above: mod's own wrap and the abs either side of it cancel exactly, so the value is continuous
      // across every wedge boundary — the same triangle-wave law `mirror1` continues the frame's own
      // edge by. There is nothing here for a HANDOVER ZONE to cross-fade, so a wedge edge that shows
      // at all is a sampling artifact and its unit is the buffer's own points, not a share of a repeat.
      // THE RING is the glass's own rim, and the module does not leave it bare: "the rim carries the
      // module's own glass — a touch of lift inside it, a tight inner shade, one light hairline just
      // inside the rim and one dark one just outside" (this file's own opening), gated in the shader by
      // `smoothstep(R - px, R + px, r)` for the lift and by `HAIR * px` for the two hairlines — bands a
      // few points of the buffer wide and not a share of the glass's own radius, so this edge's unit is
      // the same as the wedge's. Neither width answers to a handle: the bezel stands at the same few
      // points whatever `wedges` names, and the wedge fold's own continuity does not depend on the
      // count either.
      seams: [
        { kind: "wedge", of: null, unit: "points of the drawing buffer" },
        { kind: "ring", of: null, unit: "points of the drawing buffer" },
      ],
      params: { fold: [0, 2], wedges: [WEDGES_LO, WEDGES_HI], twist: [0, 1],
                power: [POWER_LO, POWER_HI] },
      // EVERY handle a score can drive (§4.4b). `mix` is the dial, under the name every instrument
      // in this engine gives it. `fold`, `wedges`, `twist` and `power` are the module's own three
      // glasses and the depth of each; `centreX` and `centreY` carry the place the glass rests at;
      // `shade` is the module's own judge channel for the rim, resting where it rests it; `mask` is
      // the judges' channel.
      //
      // NO `clock` HANDLE, AND NO `seed`. The module's four temporal literals stayed in the lab with
      // the standing gallery wall they kept alive, so nothing in this picture moves with time; and
      // the module's one die rolled the wall's layer table, which did not travel, so there is
      // nothing here for a die to decide. A handle a score can walk without moving the picture is
      // noise in the score, so neither is published, and a seeded run repeats to the point because
      // the picture is a pure function of the hand.
      //
      // NO `size` HANDLE EITHER, AND THAT IS THE DOOR LAW RATHER THAN A CHOICE. The module's own
      // `size` sets how much of the frame the lens takes. Here the reach is not free: it must be
      // exactly nothing at either door and it must cover the frame while the two works change hands,
      // so it is derived from the frame's own corners and the place the glass rests at. It is
      // published as a reading, never as a handle a score could put a wrong number in.
      handles: {
        // NO LEVEL: `mix` is the crossing's own dial and does not itself drive a structural level.
        mix: { min: 0, max: 1, def: 0, level: null },
        // `fold` chooses which single map is applied over the whole disc — the kaleidoscope's,
        // the swirl's or the magnifier's — rather than the wedge count itself, so it is the map over
        // the surface rather than the cell it can produce under one of its three rules.
        fold: { min: 0, max: 2, def: 0, kind: "enum", step: 1,
                names: { "0": "kaleidoscope", "1": "swirl", "2": "magnify" },
                unit: "which glass the pair is seen through",
                reads: "the two works' own measured polar and rotational readings — "
                     + "structure.rotational.n and .score for the mirrored wedges, "
                     + "structure.polar.twirl for the wound glass, whichever of the two reads "
                     + "loudest, and the plain magnification only where neither reading stands at "
                     + "all, which is a fact about the pair and not a bar it failed to clear",
                level: "SURFACE" },
        wedges: { min: WEDGES_LO, max: WEDGES_HI, def: WEDGES_N, kind: "enum", step: 1,
                  unit: "how many mirrored wedges the disc folds into",
                  reads: "structure.rotational.n, the work's own measured rotational order, so the "
                       + "fold repeats as often as the work itself does. The module's own six is "
                       + "what it stands at until a score names the work's",
                  applied: { restsAt: "every door", moduleOwn: WEDGES_N },
                  level: "CELL" },
        twist: { min: 0, max: 1, def: TWIST_REST,
                 unit: "how hard the glass winds the picture at its middle",
                 reads: "structure.polar.twirl, the work's own measured twirl — a work that turns "
                      + "about its own middle is wound and one that does not is barely touched",
                 applied: { radiansAtWhole: 3.6, restsAt: "the rim, exactly, at every reach" },
                 level: "SURFACE" },
        power: { min: POWER_LO, max: POWER_HI, def: POWER_REST,
                 unit: "how much nearer the glass brings the picture",
                 reads: "the ratio of the two works' own measured device steps — "
                      + "structure.ownDevice.stepPx — so the glass brings a piece of the departing "
                      + "work to the size of the arriving work's own piece. The module's own two is "
                      + "what it stands at until a score names the pair's",
                 level: "SURFACE" },
        centreX: { min: 0, max: 1, def: 0.5, unit: "where across the frame the glass rests",
                   reads: "the midpoint of the two measured radial centres, structure.radial.centre "
                        + "— the point the two works' own structure turns about",
                   level: "SURFACE" },
        centreY: { min: 0, max: 1, def: 0.5, unit: "where down the frame the glass rests",
                   reads: "the midpoint of the two measured radial centres, structure.radial.centre "
                        + "— the point the two works' own structure turns about",
                   level: "SURFACE" },
        shade: { min: 0, max: 1, def: 1, unit: "the glass's own weight — its lift, its inner shade "
                                            + "and its two hairlines",
                 applied: { liftInside: 1.045, shadeDepth: 0.30, shadePointsOfReach: 7,
                            restsAt: "every door" },
                 level: null },
        // THE MEASUREMENT THIS HANDLE IS READ AGAINST AT A DOOR. `readAtADoor` says what is read
        // (this instrument's own glass, walked at the buffer's own sample points), on which grid,
        // what the reading is counted in, and that there is no hold — the reach is exactly nothing
        // inside the hand's own dead band, so a door this reading finds a fault at is refused.
        mask: { min: 0, max: 1, def: 0,
                applied: { readAtADoor: { points: DOOR_SLIP, readOn: "the drawing buffer",
                                          reads: "no glass",
                                          measures: "this instrument's own glass over the frame, "
                                                  + "walked at the buffer's own sample points, and "
                                                  + "how far the two works have changed hands",
                                          held: null } },
                level: null },
      },
      neutrals: { a: 0, b: 1 },
      doors: { in: { handle: "mix", value: 0, work: "a" },
               out: { handle: "mix", value: 1, work: "b" } },
      // BOTH DOORS FRAME ALIKE, AND NEITHER IS CROPPED. Inside the frame the plane is the work
      // itself, so a door stands the source cover-fitted into the frame and nothing is taken off it.
      framings: { "0": { coverCrop: 1 }, "1": { coverCrop: 1 } },
      drivers: ["progress", "cueProgress", "time", "velocity", "capability", "noise", "static",
                "curve", "spline", "map", "add", "multiply", "mix", "clamp", "hold", "segment",
                "ramp", "slew", "oscillate", "node"],
      camera: { needs: "none", authority: "stage" },
      gl: { preserveDrawingBuffer: false },
      // WHAT THIS INSTRUMENT WRITES WHERE ITS OWN MATTER IS ABSENT (§7's coverage law). It is absent
      // nowhere: the plane is the work continued past its own edge by mirroring, so every point of
      // the frame samples picture and the alpha is the constant 1.
      coverage: { writes: false,
                  how: "past the frame's own edge the work does not stop and does not repeat — it "
                     + "mirrors, one triangle wave per axis — so every point the glass sends a "
                     + "sample to lands on picture and the alpha is the constant 1; at a door the "
                     + "glass's own reading walks the buffer's sample points and refuses a door "
                     + "where any of them stands inside the rim" },
      // The neutral pose is the ENTRY DOOR — `mix` at 0, the value the `doors` block names.
      neutralPose: { mix: 0, fold: 0, wedges: WEDGES_N, twist: TWIST_REST, power: POWER_REST,
                     centreX: 0.5, centreY: 0.5, shade: 1, mask: 0,
                     reduced: false, cssWidth: 1000, cssHeight: 1000 },
      passes: [{
        program: "lens", vert: VERT, frag: FRAG, position: "aPos",
        uniforms: [
          { name: "uA", type: "sampler2D", source: "textureA" },
          { name: "uB", type: "sampler2D", source: "textureB" },
          { name: "uFitA", type: "vec4", source: "fitA" },
          { name: "uFitB", type: "vec4", source: "fitB" },
          { name: "uRes", type: "vec2", source: "resolution" },
          { name: "uLens", type: "vec4", source: "frame:lens" },
          { name: "uGlass", type: "vec4", source: "frame:glass" },
          { name: "uHand", type: "vec2", source: "frame:hand" },
          { name: "uMask", type: "float", source: "handle:mask" },
        ],
      }],
      // The instrument allocates nothing of its own: it spends the two source-texture slots the host
      // already holds and the one programme the host builds from this manifest. The module's own
      // canvas, its context, its 2D texture array of fourteen works, its scratch canvas and its own
      // frame loop are what this port does without.
      // `bytesEstimate` is DERIVED. Two texture reads at this manifest's own reference frame
      // (`cssWidth`/`cssHeight` above, 1000×1000 CSS px), sized per variant off two facts
      // already read elsewhere on this road: the render ladder's own floor scale (pass-layer.js
      // `STEPS`, 0.50) for `lean`, the native frame for `standard`, and the device pixel ratio
      // ceiling (`DPR_CAP`, 2) for `rich` — at four bytes a pixel (RGBA8, a fact of the format),
      // doubled for the two
      // texture slots this instrument reads. The rest is CAPABILITY: 0 own textures,
      // 0 own framebuffers, 1 programme, 1 pass — a single-pass compositor that
      // spends only the two source slots the host already holds.
      resources: { lean: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0,
                   programs: 1, passes: 1, bytesEstimate: 2000084, variant: "lean" },
                   standard: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0,
                               programs: 1, passes: 1, bytesEstimate: 8000084,
                               variant: "standard" },
                   rich: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                           passes: 1, bytesEstimate: 32000084, variant: "rich" } },
      capabilities: ["webgl2"],
      decline: ["one work only", "a source that never decoded"],
      provenance: { labPath: "lab/effects/lens.js", commit: "2afa485",
                    sha256: "f52846e21115b8e43d2462eaa64fe8916e5eeea70ffe7ecda10dfe92c307774f" },
      readiness: "production-ready",
    };

    var live = false;
    return {
      name: "lens",
      manifest: manifest,
      values: values,
      fit: fit,
      feel: feelOf,
      // WHAT THIS INSTRUMENT'S `feel` PROMISES (Phase 7, item 3b): excursion, deliberately.
      // `reachOf` (lens.js above) is exactly nothing across the two dead bands at either end of the
      // hand and whole across the middle third — a plateau, not a door-to-door ramp — so it neither
      // starts at 0 nor ends at 1 by way of a straight monotone climb, and turns back is not even
      // the right word: it is flat, then rises, then flat again. The monotone law is not asked of
      // it. The generic law reads it for continuity alone.
      feelClass: "excursion",
      prepare: function (o) {
        if (!o.sources) return { take: false, why: "the glass instrument needs both works" };
        if (!o.cue) return { take: false, why: "no cue names it" };
        return { take: true };
      },
      start: function () { live = true; },
      // The pose the shader draws.
      //
      // A DOOR THIS INSTRUMENT CANNOT KEEP WHOLE IS REFUSED RATHER THAN DRAWN, and so is a frame
      // where the two works change hands outside the glass. The door law and the handover law are
      // both this instrument's own claims, so the instrument is what answers for them: it walks its
      // own glass over the buffer the host is about to bind and hands the host the reason, with the
      // measured numbers in it, instead of drawing a door that is not the photograph or a dissolve
      // that is not a fold. The host recovers the transaction on that reason and the walk's own
      // glide carries the visitor.
      frame: function (st) {
        if (!live) return;
        var h = st.handles;
        var pose = {
          mix: h.mix, fold: h.fold, wedges: h.wedges, twist: h.twist, power: h.power,
          centreX: h.centreX, centreY: h.centreY, shade: h.shade, mask: h.mask,
          reduced: st.reduced,
          cssWidth: st.viewport.w, cssHeight: st.viewport.h,
          // THE GRID THE SHADER WILL SAMPLE ON, carried into the pose so the glass is built for the
          // frame the host is about to bind as `uRes` and read on it rather than on the CSS frame
          // around it.
          bufWidth: st.viewport.bufferW, bufHeight: st.viewport.bufferH,
        };
        var v = values(pose);
        if (h.mix === 0 || h.mix === 1) {
          if (st.reportApplied) {
            st.reportApplied({
              door: h.mix === 0 ? "in" : "out",
              buffer: [pose.bufWidth, pose.bufHeight],
              reads: "no glass", request: 0,
              applied: v.reach,
              moved: v.reach,
              unit: "points of the drawing buffer",
              // What the glass was doing over the frame at this door: how many of the walked points
              // it stood over, and how much room the tightest of them had.
              inside: v.glassMap ? v.glassMap.inside : null,
              sparePx: v.glassMap ? v.glassMap.nearestPx : null,
              held: v.doorHeld, whyNo: v.doorWhyNo,
            });
          }
          if (v.doorWhyNo) { st.fail(st.token, v.doorWhyNo); return; }
        } else if (v.handWhyNo) {
          st.fail(st.token, v.handWhyNo);
          return;
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
    instrument: lensInstrument(),
  });
})();
