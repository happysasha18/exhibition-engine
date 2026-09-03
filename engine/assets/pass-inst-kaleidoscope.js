/*!pass-inst-kaleidoscope.js*/
// One instrument, travelling as its own file (PASS-API-V1 §7/§8, his word of 2026-08-14 08:39: the
// engine knows no effect name and loads version-pinned opaque effect files).
//
// WHAT THIS FILE IS. One instrument and the mathematics it draws by: a name, a manifest declaring
// what it cuts on, its passes, its uniforms with the source each is bound from, its handles and its
// doors, and the pure functions that answer the numbers of one frame. The manifest's declared names
// are the whole interface — the host binds by them and refuses at registration anything it cannot
// supply.
//
// WHAT THIS FILE MAY NOT DO. It reads no wall clock, holds no listener, creates no WebGL context,
// loads no picture and touches no DOM (§1.2's fence). The host owns the canvas, the context, the
// frame loop, the clock, the camera and the transaction; the instrument owns the picture.
//
// OWNERSHIP. This instrument was carried over from lab/effects/kaleidoscope.js. The artistic
// instruments and their manifests belong to tlvphotos, which builds these files from its own
// sources; the engine's copies are what ships until that handover lands. The contract this file
// answers to is §7 and §8 of docs/design/PASS-API-V1.md, and the record that names it is the site's
// own `pass` block.
(function () {
  var join = window.__@@NS@@PassInstrument;
  if (typeof join !== "function") return;

  // THIS FILE'S OWN VERSION, and the one home of that fact. The build reads this literal out of the
  // source and writes it into the site's record beside the digest, so the version a file declares
  // and the version a host was told to load cannot drift apart without the build noticing.
  var INSTRUMENT_VERSION = "1.0.0";

  // ================================================================================================
  // THE KALEIDOSCOPE INSTRUMENT (§8) — lab/effects/kaleidoscope.js carried across
  // ================================================================================================
  //
  // WHAT THE VISITOR SEES. The departing photograph stands whole. Then one slice of it lifts out of
  // the frame and is repeated round a centre — the centre the work itself turns about — mirrored at
  // every edge so the picture becomes a rosette, and the slice tiles outward into rings that mirror
  // at every turn. The rosette deepens to the middle of the passage; under its deepest fold, where
  // the eye can no longer hold what it is looking at, the photograph in the wedges becomes the OTHER
  // work; and the rosette then closes back down onto that second photograph standing whole. It is
  // one continuous fold and unfold of a single picture, never a dissolve between two.
  //
  // WHY IT STANDS HERE. The composer's own census (S1-D-report, «2 · An opaque instrument on ring
  // and band cuts»): a `ring` cut has no instrument that fills the frame, so a pair whose ground is
  // the radial measure has no ground to stand a stack on and loses its second move. The meshing
  // instrument cuts on rings and writes coverage, which makes it a travelling voice and never the
  // ground. This one cuts on rings and fills the frame at every point, which is the hole. It is also
  // the instrument the composer's own `kaleidoscope` road is named for: that road qualifies a pair
  // on its radial reading and then has to be carried by whatever cuts on rings.
  //
  // ------------------------------------------------------------------------------------------------
  // HIS THREE STANDING WORDS ON THIS EFFECT, AND WHAT EACH COST
  // ------------------------------------------------------------------------------------------------
  // lab/CROSSING-HISTORY.md's vocabulary table carries his verdict on every effect. This one reads:
  // «approved; wedge seams need retouch (В9); rings>2 washes to milk», at level SURFACE. Three
  // words, and each is answered here by a number rather than by an intention.
  //
  //   1. APPROVED — so the mathematics is carried digit for digit and nothing is redesigned. Every
  //      constant the picture stands on is the module's own and the suite reads both files for each.
  //   2. THE WEDGE SEAMS NEED RETOUCH. The module's own header claims no seam can appear at a wedge
  //      edge, and it is right about CONTINUITY: the triangle wave in angle is continuous across
  //      every edge. What it is not is SMOOTH — the fold's derivative flips sign at the edge, so the
  //      photograph's own texture reverses direction along a hard line and the eye reads a crease.
  //      That is the seam he saw, and no filtering closes it because it is the fold itself. The
  //      retouch is `softAbs` below: the corner of the triangle wave is rounded over a width read in
  //      POINTS OF THE DRAWING BUFFER, so the crease is softened over the same handful of points at
  //      every radius, on every frame the host can hand, and the picture pays nothing anywhere else.
  //   3. RINGS OVER 2 WASH TO MILK. The module publishes its radial repeat up to 5. This instrument
  //      publishes it up to 2, and the number is his rather than a taste of this port's.
  //
  // ------------------------------------------------------------------------------------------------
  // WHAT CAME OVER, AND WHAT STAYED BEHIND
  // ------------------------------------------------------------------------------------------------
  // WHAT CAME OVER, digit for digit: the wedge fold and its twist, the radial repeat and its soft
  // floor at the centre, the radius that holds one whole repeat, the sample point's own wander and
  // the sample width's own breath, the closed-form turn, the finish — the gamma, the
  // desaturate-and-boost mix and the vignette — with each of its terms gated to its own identity by
  // the fold, and the whole of the crossing dial's construction: the fold walks the SAMPLE
  // COORDINATE and never the final colour, so the frame is one picture in sharp focus at every value
  // of it rather than two renderings of one laid over each other.
  //
  // WHAT STAYED BEHIND: the module's own canvas and context, its frame loop, its resize observer, its
  // texture uploads, its pointer branch and its press-to-swap, its still-frame binding under reduced
  // motion, and its `source` parameter — a cue of this engine carries an ordered PAIR and the passage
  // itself is what moves between the two works, so which photograph stands is the dial's business.
  //
  // THE PORT'S OWN THREE NUMBERS, each named as the port's where it appears: the shape of the
  // crossing (`FOLD_WINDOW`), the width of the exchange (`SWAP_UNDER`, from which `SWAP_HALF` is
  // derived rather than chosen), and the crease's softening (`SOFT_POINTS`).
  //
  // ------------------------------------------------------------------------------------------------
  // THE TWO THINGS THIS HOST BINDS DIFFERENTLY FROM THE MODULE, AND WHAT EACH COST
  // ------------------------------------------------------------------------------------------------
  //   · THE WRAP. The module binds its own textures MIRRORED_REPEAT, and the wedge leans on it: the
  //     sample point wanders well outside the picture and the hardware mirrors it back in. This host
  //     binds CLAMP_TO_EDGE (pass-layer.js's own `makeTex`), under which the same sample point smears
  //     the picture's outermost row of texels across the whole outer ring. So the mirror is done HERE,
  //     in the shader, by the arithmetic the wrap mode performs — `mirrorInto` — and the wrap is never
  //     asked for a point outside the picture at all. This is the port's own repair and it carries a
  //     row that reddens when it is reverted.
  //   · THE MIP CHAIN, and it is half closed since the port was written. The module builds one and
  //     asks for anisotropy, and its whole gradient estimate exists to pick a mip level that does
  //     not jump at a fold line. The host built no chain at all when this file landed, so
  //     `textureGrad` would have had nothing to choose between and the estimate was inert
  //     arithmetic; it is therefore not carried, and the fact is written down rather than lost. The
  //     host now BUILDS the chain and hands it to any instrument declaring `gl.readsChain`, which
  //     this manifest does, so the aliasing in the outer rings at a deep sample width is answered by
  //     the walking filter. Choosing the level explicitly is still the module's own arithmetic and
  //     still not carried; that remains a request to the host's own sampler rather than something an
  //     instrument can close from inside §1.2's fence.
  //
  // ------------------------------------------------------------------------------------------------
  // THE COVERAGE: THIS INSTRUMENT FILLS THE FRAME, AND TAKES NO BITE OUT OF THE WORK
  // ------------------------------------------------------------------------------------------------
  // §7's coverage law asks every instrument to say where its own matter is absent. Here it is absent
  // nowhere, and it costs the picture nothing to be so. Every point of the frame reads one point of
  // one photograph: at the doors the plain cover fit, in between a folded coordinate that the mirror
  // holds inside the picture whatever it does. So the alpha is the constant 1 and BOTH DOORS PUBLISH
  // A COVER CROP OF 1 — the frame is the whole picture cover-fitted and nothing is trimmed to buy the
  // coverage, which is what separates this ground from the folding instrument's (its crop of 1.90
  // costs a landed face 47 per cent of its own side). Under the placement rule (§8 as amended 14:05)
  // that makes this instrument lawful as the LOWEST cue of a stack and as a whole one-cue score.
  function kaleidoscopeInstrument() {
    var VERT = [
      "attribute vec2 aPos;",
      "varying vec2 vUv;",
      "void main(){ vUv = vec2(aPos.x * 0.5 + 0.5, 0.5 - aPos.y * 0.5); gl_Position = vec4(aPos, 0.0, 1.0); }",
    ].join("\n");

    // ----------------------------------------------------------------------------------------------
    // THE SHADER
    // ----------------------------------------------------------------------------------------------
    // The module works in a frame coordinate measured UP the frame and uploads its textures flipped;
    // this host uploads them as they are and hands the shader a coordinate measured DOWN. So `q`
    // below is the module's own coordinate, rebuilt from this host's, every line between is the
    // module's own line, and the flip happens once at the fetch. Flipping and mirroring commute, so
    // which side of `mirrorInto` the flip stands on cannot change a pixel.
    //
    // THE TWO WORKS ARE READ AT TWO COORDINATES, where the module read one. The module's two
    // photographs are one file's size, so one aspect correction served both; a pair of this
    // collection is any two works, so each is cover-fitted by its own seating and its wedge is
    // corrected by its own file's shape. That is the same law read on two works instead of one.
    var FRAG = [
      "precision highp float;",
      "varying vec2 vUv;",
      "uniform sampler2D uA;",              // the work the passage leaves
      "uniform sampler2D uB;",              // the work it arrives at
      "uniform vec4 uFitA;",
      "uniform vec4 uFitB;",
      "uniform vec2 uRes;",
      // HOW DEEP THE FOLD STANDS, how far the two works have exchanged, how many wedges the fold
      // makes and how far the wedge leans as it goes out. The first two are the crossing itself: the
      // first is nothing at both doors and whole in the middle, the second is nothing at one door and
      // whole at the other and moves only under the deepest fold.
      "uniform vec4 uFold;",
      // THE RADIAL REPEAT, the sample width, the turn, and the finish's own weight. The last is the
      // fold's depth times the finish handle, so every term of the finish stands at its own identity
      // at a door however the handle is placed.
      "uniform vec4 uRing;",
      // THE CREASE'S SOFTENING (his В9 word): in angle at unit radius, and in the radial repeat. Both
      // are read in points of the drawing buffer by the script and arrive here already in the units
      // the fold is folded in.
      "uniform vec2 uSoft;",
      // WHERE THE WEDGE READS THE PAIR — the centre the work itself turns about, with the module's
      // own wander already added, measured up the picture.
      "uniform vec4 uCentre;",
      // EACH FILE'S OWN ASPECT CORRECTION, which is what keeps the sampled disc round in the
      // photograph's own pixels rather than round on a screen of some shape the work never saw.
      "uniform vec4 uTexel;",
      // The judges' channel: how far each point's sample has travelled from its flat place, as colour.
      "uniform float uMask;",
      "const float TAU = 6.28318530718;",
      // the radius that holds one whole radial repeat (kaleidoscope.js:35)
      "const float R0  = 1.25;",
      // THE WRAP, DONE IN ARITHMETIC. This is exactly MIRRORED_REPEAT: a triangle wave of period two
      // that is 0 at 0, 1 at 1 and mirrors on both sides for ever. The module got it from the sampler;
      // this host binds CLAMP_TO_EDGE, so without this line the outer rings would be the picture's own
      // edge row smeared across them.
      "vec2 mirrorInto(vec2 uv){ return 1.0 - abs(mod(uv, 2.0) - 1.0); }",
      // The plain cover fit — the module's own flat door (kaleidoscope.js:76), written in this host's
      // own seating carrier. The two are the same arithmetic: the host's `fit` returns the very
      // half-extents the module's `flatFit` computes.
      "vec2 flatAt(vec2 q, vec4 f){ return (q - 0.5) * f.xy + 0.5 + f.zw; }",
      // THE RETOUCHED CREASE. |x| EXACTLY outside a band of e about the fold, and inside it the
      // parabola that meets |x| at both ends with the same slope, so the fold's own derivative does
      // not jump and the photograph's texture turns instead of creasing. At e of nothing this is |x|
      // to the last bit, which is the module's own line.
      //
      // WHY A PARABOLA AND NOT THE ROUNDED HYPOTENUSE. `sqrt(x*x + e*e) - e` is the shorter way to
      // write a rounded corner and it is the wrong one here: away from the crease it tends to
      // |x| - e, so it does not soften a crease, it TURNS THE WHOLE WEDGE by e. Measured on the two
      // roads at a fold of 0.84, that mistake stood the port 12.17 of 255 from the module against a
      // bar of 6; the parabola below is 1.5 points of the buffer wide and nothing outside it.
      "float softAbs(float x, float e){",
      "  float a = abs(x);",
      "  return a >= e ? a : (x * x + e * e) / (2.0 * max(e, 1e-9));",
      "}",
      "vec2 wedgeAt(vec2 p, float r, vec2 texel){",
      "  float seg = TAU / uFold.z;",
      // the softening in angle, at THIS radius: a fixed number of buffer points subtends less angle
      // the further out it stands, and it is never allowed past a quarter of a wedge, so the fold
      // stays a fold at the very centre where an angle means almost nothing.
      "  float ea = min(uSoft.x / max(r, 1e-4), 0.25 * seg);",
      "  vec2 d = r < 1e-6 ? vec2(1.0, 0.0) : p / r;",
      "  float a = atan(d.y, d.x) + uRing.z;",
      /* the fold: one wedge, every second copy mirrored (kaleidoscope.js:43-48) */
      "  a = mod(a, seg);",
      "  a = softAbs(a - 0.5 * seg, ea);",
      "  a += uFold.w * r;",                 // same on both sides of an edge -> still seamless
      /* the radial repeat: the wedge tiles outward into rings, mirrored at every turn */
      "  float t  = r / R0 * uRing.x;",
      "  float f  = softAbs(mod(t + 1.0, 2.0) - 1.0, uSoft.y);",
      "  float rr = f * R0;",
      "  rr = sqrt(rr * rr + 0.0016);",      // soft floor: the centre never collapses to a point
      "  return uCentre.xy + vec2(cos(a), sin(a)) * rr * uRing.y * texel;",
      "}",
      "void main(){",
      "  float m = min(uRes.x, uRes.y);",
      // the module's own frame coordinate, measured up the frame, rebuilt from this host's
      "  vec2 q = vec2(vUv.x, 1.0 - vUv.y);",
      "  vec2 p = (q - 0.5) * uRes / m;",
      "  float r = length(p);",
      // THE CROSSING DIAL. `uFold.x` picks WHICH POINT of each photograph a pixel reads, never which
      // of two already-rendered colours to show. The flat place is the plain cover fit every straight
      // photograph uses; the wedge place is the wandering, repeated point above; the fold walks the
      // SAMPLE COORDINATE between them, so one texture fetch answers every value of it and the frame
      // is always one picture in sharp focus, never two renderings of it laid over each other — the
      // ghost a colour crossfade leaves at the middle of the ride (kaleidoscope.js:59-65).
      "  vec2 fa = flatAt(q, uFitA);",
      "  vec2 fb = flatAt(q, uFitB);",
      "  vec2 ua = mix(fa, wedgeAt(p, r, uTexel.xy), uFold.x);",
      "  vec2 ub = mix(fb, wedgeAt(p, r, uTexel.zw), uFold.x);",
      "  vec2 sa = mirrorInto(vec2(ua.x, 1.0 - ua.y));",
      "  vec2 sb = mirrorInto(vec2(ub.x, 1.0 - ub.y));",
      // THE EXCHANGE, and it is one line because it stands under the deepest fold and nowhere else.
      "  vec3 col = mix(texture2D(uA, sa).rgb, texture2D(uB, sb).rgb, uFold.y);",
      // The finish belongs to the fold alone — none of it stands at a door — so each term is gated to
      // its own identity by the fold's own depth: gamma at the first power, the desaturate-and-boost
      // mix at its own colour, the vignette at 1.0 (kaleidoscope.js:96-102).
      "  float g = uRing.w;",
      "  col = pow(col, vec3(mix(1.0, 1.24, g)));",
      "  col = mix(vec3(dot(col, vec3(0.299, 0.587, 0.114))), col, mix(1.0, 1.12, g));",
      "  float rn = r / (0.5 * length(uRes) / m);",      // 1.0 at the corner, any shape of frame
      "  col *= mix(1.0, mix(1.0, 0.34, smoothstep(0.40, 1.0, rn)), g);",
      // THE JUDGES' OWN FRAME: how far this point's sample has travelled from its flat place, in red,
      // with the place itself in the other two channels. It is BLACK exactly where a point still reads
      // the photograph where the photograph stands, so a row reads off the picture whether a door is
      // the flat photograph, and it carries no coverage of its own because what it is for is to be
      // read as colour.
      "  vec2 flatDown = vec2(fa.x, 1.0 - fa.y);",
      "  vec3 judge = vec3(clamp(length(sa - flatDown) * 8.0, 0.0, 1.0), sa.x, sa.y);",
      "  col = mix(col, judge, uMask);",
      // THE COVERAGE: the alpha is the constant 1, and it is a decision rather than a default. Every
      // point of the frame reads one point of one photograph at every value of the dial, so this
      // instrument has no absence to publish and stands as the ground a stack is laid on.
      "  gl_FragColor = vec4(col, 1.0);",
      "}",
    ].join("\n");

    function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
    function num(v, d) { var n = Number(v); return n === n && n !== Infinity && n !== -Infinity ? n : d; }
    function smoothstep(a, b, x) {
      var t = (x - a) / (b - a);
      t = t < 0 ? 0 : t > 1 ? 1 : t;
      return t * t * (3 - 2 * t);
    }

    /* ---- THE MODULE'S OWN NUMBERS, carried digit for digit ---------------------------------- */

    /* THE WEDGE COUNT, THE LEAN AND THE RADIAL REPEAT at rest. These three are the vista preset his
       taste approved on 2026-08-08 11:39 and the charter records — «kaleidoscope 8/.55/repeats 1» —
       and they are the module's own declared defaults besides (kaleidoscope.js:135-137). */
    var WEDGES_MIN = 3, WEDGES_MAX = 24, WEDGES_DEF = 8;
    var TWIST_MIN = -1.2, TWIST_MAX = 1.2, TWIST_DEF = 0.55;

    /* THE RADIAL REPEAT, AND WHERE ITS CEILING COMES FROM. The module publishes 1 to 5. His standing
       verdict in the charter's vocabulary table is «rings>2 washes to milk», so the ceiling here is 2
       and it is HIS number: past it the mirrored rings average the photograph away and the frame goes
       pale. Nothing else about the repeat is changed — at 1 this instrument computes the module's own
       line, and the suite reads both files for the arithmetic. */
    var RINGS_MIN = 1, RINGS_MAX = 2, RINGS_DEF = 1;

    /* HOW MUCH OF THE PICTURE ONE WEDGE READS, across it. The module's own sample width breathes
       about 0.30 by a quarter either way on its own clock (`driftZoom`, kaleidoscope.js:429-431);
       0.30 is that breath's own middle and the two ends are the module's own floor and ceiling under
       the hand it no longer has. */
    var REACH_MIN = 0.12, REACH_MAX = 0.5, REACH_DEF = 0.30;

    /* THE MODULE'S OWN WANDER AND BREATH (kaleidoscope.js:423-431). Nothing here is a parameter: it
       is what the thing does when nobody touches it, and it reaches the picture through the second
       the host hands down. */
    function driftX(t) {
      return 0.170 * Math.sin(t * 0.0617) + 0.080 * Math.sin(t * 0.1631 + 1.7);
    }
    function driftY(t) {
      return 0.145 * Math.sin(t * 0.0472) + 0.062 * Math.sin(t * 0.1187 + 2.4);
    }
    function breathOf(t) { return 1.0 + 0.26 * Math.sin(t * 0.0431 + 1.1); }

    /* THE TURN, in closed form (kaleidoscope.js:432-439): the exact integral of
       0.030 + 0.014*sin(t*0.0271), zeroed at t = 0. Written closed-form rather than accumulated frame
       by frame, so a driven second reads the same turn whichever wall-clock moment actually drew it. */
    var ROT_RATE = 0.030, ROT_AMP = 0.014, ROT_W = 0.0271;
    function rotOf(t) {
      return ROT_RATE * t + (ROT_AMP / ROT_W) * (1.0 - Math.cos(ROT_W * t));
    }

    // HOW LONG A SECOND A SCORE MAY HAND IN. §2.5's transaction bound, in seconds — the same
    // ceiling pass-composer.js reads off its own tier table into TRANSACTION_MS and
    // pass-layer.js reads off its own tier table into DURATION_MAX (S-70, 2026-09-03).
    //
    // UNJUSTIFIED — a third typed copy of that same 14, not derived from either. OWNED, ONE HOME
    // NOT AVAILABLE HERE (plan row S-82, 2026-09-03): this file is a version-pinned,
    // independently-loaded instrument (PASS-API-V1 §1.2 — "the host owns... the clock... and the
    // transaction; the instrument owns the picture"), so it carries no import of the composer's
    // or the layer's module scope and cannot read either derivation. A shared home would need the
    // host to publish this bound through the manifest contract itself, which is the wire change
    // named in docs/evidence/2026-09-03-s69-s72-constants.md and not done here. If §2.5 ever
    // moves, this file is the one place besides the two derivations that must be told by hand.
    var CLOCK_MAX = 14;

    /* ---- THE PORT'S OWN THREE NUMBERS -------------------------------------------------------- */

    /* 1 · THE SHAPE OF THE CROSSING, and it is the port's because the module has no crossing at all.
       lab/data/module-contract.json records this module's dial as ONE-SIDED, resting at the fold with
       the flat photograph as its only door: the module opens the fold and stays there. A passage of
       this engine has TWO doors and a photograph standing whole at each, so the fold has to open and
       close again inside one hand. One sine over the whole passage is what does it: nothing at both
       ends of the hand, whole in the middle, and — because it is a sine at its own zero — a landing
       that is exact by construction rather than by a tolerance.

       IT IS ALSO THE CHARTER'S MYSTERY MIDDLE, read straight (shelf 5): the debt peaks mid-crossing,
       in a stretch where what is emerging cannot yet be told. Here that stretch is where the rosette
       stands deepest, and it is the same stretch the two works exchange in.

       WRITTEN AS ONE SINE OVER THE HALF-HAND, MIRRORED, and that spelling is the whole reason the
       door law below can say «nothing exactly» rather than «nothing nearly». `sin(PI * u)` at u of 1
       is 1.2246e-16 and not 0, because PI is not pi; `sin(PI * min(u, 1 - u))` is the same function
       of u at every point and its argument at both ends is the literal 0, whose sine is the literal
       0. The peak is exact for the same reason: at the middle the argument is PI/2 to the bit. */
    function foldWindow(u) {
      var x = clamp(u, 0, 1);
      return Math.sin(Math.PI * Math.min(x, 1 - x));
    }

    /* 2 · WHERE THE TWO PHOTOGRAPHS EXCHANGE, and the width is DERIVED rather than chosen. Charter
       shelf 5's second corollary — the CONJUROR — puts the content swap at the plan's motion peak,
       where the eye is led away. The motion peak of this instrument is the fold's own peak, so the
       exchange runs exactly across the stretch where the fold stands over nine tenths of its whole
       and nowhere else. `SWAP_UNDER` is that share; the half-width below follows from it and from the
       window above by arithmetic, and moving one moves the other.

       WHY A CROSSFADE IS LAWFUL HERE where the fold's own dial refuses one. The module's dial walks a
       sample COORDINATE precisely so one picture is never laid over another; that law is about ONE
       photograph seen twice, which is the ghost. Two different photographs exchanging is the
       crossing itself, and it happens under the deepest fold, where neither is legible as a
       photograph and the eye is holding a rosette. */
    var SWAP_UNDER = 0.9;
    var SWAP_HALF = 0.5 - Math.asin(SWAP_UNDER) / Math.PI;
    function swapAt(u) { return smoothstep(0.5 - SWAP_HALF, 0.5 + SWAP_HALF, clamp(u, 0, 1)); }

    /* 3 · THE CREASE'S SOFTENING, in points of the drawing buffer — his В9 word, «wedge seams need
       retouch», answered as a measurement. The fold is continuous across a wedge edge and the module
       says so rightly; what it is not is smooth, and the sign flip in the fold's own derivative turns
       the photograph's texture along a hard line the eye reads as a crease. Rounding the corner of
       the triangle wave over a width read in POINTS closes it at every radius and on every frame the
       host can hand, and it costs the picture nothing anywhere else: past the softening `softAbs` is
       the absolute value to the last bit.

       THIS NUMBER NOW TRAVELS ON THE HOST'S OWN SEAM (§8's `seams` block, pass-layer.js). It used to
       stand here as a private number with a note that it wanted revisiting; the argument for it —
       below one point of the drawing buffer the retouch falls inside a single sample and does
       nothing, past three it stops rounding a crease and starts being a smear the eye reads as blur
       along a line, and one and a half points is the middle of that span — did not belong to this
       fold alone, because planet's own wrap-seam and tunnel's own ring-join were rounding an edge by
       the same reasoning in two more files. The manifest below DECLARES both of this instrument's
       seams (the wedge's own crease and the radial repeat's own crease) as `unit: "points of the
       drawing buffer"`, the host answers with the one number the argument above settles on, and
       `SOFT_POINTS` here is only the value this file falls back to where no host has answered yet —
       at manifest registration, before any frame has been asked for. */
    var SOFT_POINTS = 1.5;

    // ---- the grid one frame is drawn on ------------------------------------------------------------
    // The buffer the host is about to bind as `resolution`, with the CSS frame where it hands none
    // and a square where it hands neither. The crease's softening is read on it and the door's own
    // reading is counted in its points. `drawn` says which of the two the reading below names, since
    // a reader told «a 780 x 1688 frame» would look for a device that has none.
    function gridOf(st) {
      var bw = Math.round(num(st.bufWidth, 0)), bh = Math.round(num(st.bufHeight, 0));
      if (bw >= 1 && bh >= 1) return { w: bw, h: bh, drawn: true, given: true };
      var cw = Math.round(num(st.cssWidth, 0)), ch = Math.round(num(st.cssHeight, 0));
      if (cw >= 1 && ch >= 1) return { w: cw, h: ch, drawn: false, given: true };
      return { w: 1, h: 1, drawn: false, given: false };
    }

    // Cover-fit a work into the frame, and nothing beyond it. Both doors of this instrument are the
    // plain cover fit — the module's own flat door is exactly that (kaleidoscope.js:376-388) — so the
    // port asks the host for no crop and `framings` publishes 1 at both ends.
    function fit(iw, ih, w, h) {
      var fa = w / Math.max(h, 1);
      var ia = iw / Math.max(ih, 1);
      if (ia > fa) return [fa / ia, 1, 0, 0];
      return [1, ia / fa, 0, 0];
    }

    // EACH FILE'S OWN ASPECT CORRECTION, recovered from its seating. The module reads it off the file
    // it loaded (`shortSide / iw, shortSide / ih`, kaleidoscope.js:230-232); an instrument loads no
    // file, so it is recovered from the cover fit the host binds, which carries exactly the same
    // fact: a cover fit is [fa/ia, 1] or [1, ia/fa], so the picture's own aspect is
    // `fa * fit.y / fit.x` in both branches and the correction follows from it. Where no seating has
    // arrived yet the frame's own shape stands in, which is what a square file would have asked for.
    function texelOf(f, fa) {
      var sx = num(f && f[0], 1), sy = num(f && f[1], 1);
      if (!(sx > 0)) sx = 1;
      if (!(sy > 0)) sy = 1;
      var ia = fa * sy / sx;
      if (!(ia > 0)) ia = 1;
      return ia > 1 ? [1 / ia, 1] : [1, ia];
    }

    // ---- the numbers of one frame ------------------------------------------------------------------
    // Everything the shader gets beyond the seating of the two works is a pure function of the pose;
    // every number in the pose comes from a handle a score can drive. The one thing that moves with
    // time is the module's own wander, and it reads the `clock` handle rather than a clock of its
    // own, so a seeded run repeats to the pixel and a driven walk repeats whichever wall-clock moment
    // drew it.
    function posed(st) {
      var dial = clamp(num(st.mix, 0), 0, 1);
      var fold = foldWindow(dial);
      var wet = swapAt(dial);
      var t = clamp(num(st.clock, 0), 0, CLOCK_MAX);
      var grid = gridOf(st);
      var m = Math.min(grid.w, grid.h);
      var aspect = grid.w / Math.max(grid.h, 1);
      var wedges = Math.round(clamp(num(st.wedges, WEDGES_DEF), WEDGES_MIN, WEDGES_MAX));
      var twist = clamp(num(st.twist, TWIST_DEF), TWIST_MIN, TWIST_MAX);
      var rings = clamp(num(st.rings, RINGS_DEF), RINGS_MIN, RINGS_MAX);
      var reach = clamp(num(st.reach, REACH_DEF), REACH_MIN, REACH_MAX);
      // THE SAMPLE POINT: the pair's own measured radial centre, with the module's own wander riding
      // on it. The module anchored its wander on two numbers chosen by eye for its own two
      // photographs (`homeX`, `homeY`, kaleidoscope.js:420-421); here the anchor is a measurement of
      // the works, which is the class law of his 19:21 word, and the wander around it is the
      // module's own. The handle is measured DOWN the picture, the way every place in a work record
      // is; the fold reads UP, so it is turned over once, here.
      var cx = clamp(num(st.centreX, 0.5), 0, 1) + driftX(t);
      var cy = (1 - clamp(num(st.centreY, 0.5), 0, 1)) + driftY(t);
      var zoom = reach * breathOf(t);
      var rot = rotOf(t);
      var finish = clamp(num(st.shade, 1), 0, 1) * fold;
      var texA = texelOf(st.fitA, aspect), texB = texelOf(st.fitB, aspect);
      // THE CREASE'S SOFTENING, carried into the units each fold is folded in. Both widths arrive in
      // POINTS OF THE DRAWING BUFFER off the host's own `seams` reading (§8, pass-layer.js) — the
      // manifest names both as hairline retouches, so the host answers with the same number for both
      // and `SOFT_POINTS` stands in only where no host has answered yet. In ANGLE that width is read
      // at unit radius and the shader divides by the radius so the width on the frame is the same
      // everywhere. In the RADIAL repeat one buffer point is `rings / (R0 * m)` of the repeat's own
      // coordinate, which is the chain rule of `t = r / R0 * rings` and nothing more.
      var softWedgePts = num(st.seam && st.seam.wedge, SOFT_POINTS);
      var softRingPts = num(st.seam && st.seam.ring, SOFT_POINTS);
      var soft = [softWedgePts / Math.max(m, 1), softRingPts * rings / (1.25 * Math.max(m, 1))];
      return {
        fold: [fold, wet, wedges, twist],
        ring: [rings, zoom, rot, finish],
        soft: soft,
        centre: [cx, cy, 0, 0],
        texel: [texA[0], texA[1], texB[0], texB[1]],
        // read on the diagnostic surface, bound to no uniform: what the hand came to, and every
        // number the works themselves own
        hand: dial, depth: fold, exchanged: wet, wedges: wedges, twist: twist,
        rings: rings, reach: reach, zoom: zoom, turn: rot, second: t,
        centreX: cx, centreYUp: cy, finish: finish,
        softPoints: softWedgePts, softRingPoints: softRingPts, swapHalf: SWAP_HALF,
        ringsCeiling: RINGS_MAX,
        mask: clamp(num(st.mask, 0), 0, 1),
        fitA: [num(st.fitA && st.fitA[0], 1), num(st.fitA && st.fitA[1], 1)],
        fitB: [num(st.fitB && st.fitB[0], 1), num(st.fitB && st.fitB[1], 1)],
        grid: grid,
      };
    }

    // ---- THE DOOR THE INSTRUMENT READS FOR ITSELF --------------------------------------------------
    // His 18:00 architecture decision: the instrument reads its doors at runtime on the actual buffer,
    // and the report it hands back is the runtime truth; what the manifest declares is only the claim.
    // The meshing instrument answered that first, the unfold reads its own panel map the same way and
    // the folding one walks its two faces; this is the same law read in this instrument's own unit,
    // which is THE SAMPLE POINT — where each point of the frame reads the photograph.
    //
    // WHAT A DOOR ASKS OF A KALEIDOSCOPE. At either door the frame is one work, cover-fitted, pixel
    // for pixel what the file carries. Three things carry that, and this reads all three ON THE
    // BUFFER rather than declaring them:
    //   · EVERY POINT READS ITS FLAT PLACE. The fold is a sine at its own zero at both ends of the
    //     hand, so the sample coordinate is the plain cover fit. How far the furthest walked point's
    //     sample stands from that place — in POINTS OF THE GRID, since it is a claim about samples —
    //     is one number that catches a fold that did not close, a wander that leaked through it and a
    //     turn that reached the coordinate.
    //   · NO POINT READS OUTSIDE THE PICTURE. The mirror holds the wedge inside the work; at a door
    //     nothing should ever ask it to. A point whose flat place has run off the picture is a
    //     seating fault, and the count of them is published beside the travel.
    //   · THE FRAME IS ONE WORK AND NOT TWO. The exchange stands under the deepest fold and is
    //     nothing at one door and whole at the other; if it ever reached a door the frame would be a
    //     blend of two photographs, which is the one thing this instrument's whole construction
    //     exists to avoid. What share of the wrong work stands in the frame is read and published.
    //   · THE JUDGES' CHANNEL IS SHUT. `mask` draws the sample's own travel as colour, which is what
    //     it is for; left open at a door the frame is a false-colour map and not the photograph.
    //
    // AND THERE IS NOTHING HERE TO HOLD. The meshing instrument holds a leaking size whole and the
    // unfold holds a pair of panels flat, because in both a grid can show a fault a guard read in the
    // grid's own units can close. A kaleidoscope has no such fault: the fold is `sin(pi * 0)`, which
    // is nothing exactly and not nearly, so anything this reading finds is a real fault that no
    // widening closes and the refusal stands alone. `held` is therefore always nothing, and it says
    // so rather than carrying a guard that could never fire.
    var DOOR_SLIP = 0.5;          // points of the grid: half a point, inside which a sample cannot move
    // How much of the other work, and how much of the judges' channel, may stand in the frame at a
    // door and it still BE the photograph: half a level of 255, under anything the frame can carry.
    // The charter's own door bar is 6 of 255 over the canvas rect, and half a level is an eighth of
    // that at one point.
    // CAPABILITY — a fact about the frame's own eight bits rather than about pictures: half of
    // one level of 255 is under the smallest difference the buffer can carry, so a door reading
    // at this bar is reading something the frame could not have shown. Settled once for the nine
    // files that carry it (S-71, 2026-09-03).
    var DOOR_SHOW = 0.5 / 255;

    // THE SAMPLE POINT, WALKED ON THE BUFFER THE SHADER WILL SAMPLE ON. The walk takes the buffer's
    // own sample points: its four corners, where the fold's wander reaches furthest; the midpoints of
    // its four edges; and the nine points around its centre, where the wedge's own crease crosses. At
    // each of them the frame's own coordinate is rebuilt exactly as the shader rebuilds it and both
    // places — the flat one and the folded one — are answered by the same functions the shader runs.
    function sampleReadOf(v, W, H, which) {
      var m = Math.min(W, H), aspect = W / Math.max(H, 1);
      var f = which ? v.fitB : v.fitA;
      var texel = which ? [v.texel[2], v.texel[3]] : [v.texel[0], v.texel[1]];
      var walked = 0, bare = 0, offPx = 0, i, j;
      function walk(px, py) {
        var q = [px / W, 1 - py / H];
        var p = [(q[0] - 0.5) * W / m, (q[1] - 0.5) * H / m];
        var r = Math.sqrt(p[0] * p[0] + p[1] * p[1]);
        var flat = [(q[0] - 0.5) * f[0] + 0.5, (q[1] - 0.5) * f[1] + 0.5];
        var w = wedgePlace(v, p, r, texel);
        var uv = [flat[0] + (w[0] - flat[0]) * v.fold[0],
                  flat[1] + (w[1] - flat[1]) * v.fold[0]];
        walked += 1;
        if (uv[0] < 0 || uv[0] > 1 || uv[1] < 0 || uv[1] > 1) bare += 1;
        // one unit of the picture's own coordinate spans W / f.x points across and H / f.y up, which
        // is the flat map read backwards
        var dx = (uv[0] - flat[0]) * W / Math.max(f[0], 1e-6);
        var dy = (uv[1] - flat[1]) * H / Math.max(f[1], 1e-6);
        offPx = Math.max(offPx, Math.sqrt(dx * dx + dy * dy));
      }
      for (i = 0; i < 2; i++) {
        for (j = 0; j < 2; j++) { walk(i ? W - 0.5 : 0.5, j ? H - 0.5 : 0.5); }
      }
      walk(0.5, H * 0.5); walk(W - 0.5, H * 0.5); walk(W * 0.5, 0.5); walk(W * 0.5, H - 0.5);
      for (i = -1; i <= 1; i++) {
        for (j = -1; j <= 1; j++) { walk(W * 0.5 + i, H * 0.5 + j); }
      }
      // the share of the WRONG work standing in the frame at this door
      var other = which ? (1 - v.fold[1]) : v.fold[1];
      return { walked: walked, bare: bare, offPx: offPx, other: other, mask: v.mask,
               fold: v.fold[0], aspect: aspect };
    }

    // FRAG's own `softAbs`, in script, so the reading below rounds the crease exactly where the
    // shader rounds it.
    function softAbsOf(x, e) {
      var a = Math.abs(x);
      return a >= e ? a : (x * x + e * e) / (2 * Math.max(e, 1e-9));
    }

    // The wedge's own place, in script — FRAG's `wedgeAt` line for line, so the reading walks the very
    // coordinate the shader draws with and not a second description of it.
    function wedgePlace(v, p, r, texel) {
      var seg = 2 * Math.PI / Math.max(v.fold[2], 1);
      var ea = Math.min(v.soft[0] / Math.max(r, 1e-4), 0.25 * seg);
      var dx = r < 1e-6 ? 1 : p[0] / r, dy = r < 1e-6 ? 0 : p[1] / r;
      var a = Math.atan2(dy, dx) + v.ring[2];
      a = a - seg * Math.floor(a / seg);
      a = softAbsOf(a - 0.5 * seg, ea);
      a += v.fold[3] * r;
      var t = r / 1.25 * v.ring[0];
      var u = (t + 1) - 2 * Math.floor((t + 1) / 2) - 1;
      var f = softAbsOf(u, v.soft[1]);
      var rr = f * 1.25;
      rr = Math.sqrt(rr * rr + 0.0016);
      return [v.centre[0] + Math.cos(a) * rr * v.ring[1] * texel[0],
              v.centre[1] + Math.sin(a) * rr * v.ring[1] * texel[1]];
    }

    // THE DOOR, MEASURED. Null everywhere but at a door, since away from the doors a folding
    // photograph is the picture rather than a fault. The door is named by the manifest's own `doors`
    // block: `mix` at 0 is the entry door, where the frame is the departing work whole, and `mix` at
    // 1 the exit door, where it is the arriving one.
    function doorReadOf(v, st) {
      var which = st.mix === 0 ? 0 : (st.mix === 1 ? 1 : -1);
      if (which < 0) return null;
      var g = v.grid;
      if (!g.given) return null;
      var read = sampleReadOf(v, g.w, g.h, which);
      read.grid = g;
      read.which = which;
      return read;
    }

    // THE REFUSAL, worded the way the host's own manifest refusals read: what is wrong, in this
    // instrument's own measured numbers, on the grid it was measured on.
    // PHASE 7, ITEM 5 — RE-ANCHOR CHECKED, NO CHANGE NEEDED, AND THE REASON IS SAID EXACTLY. `f` in
    // `sampleReadOf` (line 514, `v.fitA`/`v.fitB`) is `st.fitA`/`st.fitB` read straight through
    // (line 463) — the host's own seating, with nowhere in this file that recomputes a crop of its
    // own for it to disagree with. That rules out hero's OWN class of bug (a second crop, multiplied
    // in only inside `fit()`, that never cancelled through `seated` — so hero's old proof was
    // checking a number the door's own truth had already left behind).
    //
    // WHAT `offPx` ACTUALLY GUARDS, SAID PLAINLY RATHER THAN OVERSTATED. At a real door `v.fold[0]`
    // is exactly 0 (`sin(pi * 0)`), and `uv = flat + (w − flat) · fold[0]` collapses to `flat`
    // identically WHATEVER `f` holds — planting a wrong `fitA` into a throwaway copy and reading
    // `values()` at `mix: 0` confirms `offPx` stays exactly 0 regardless. So this row is not, and
    // structurally cannot be, a check that the SEATING itself is right — it is a check that the FOLD
    // itself reaches exactly nothing at a door, which is the fault class this instrument actually
    // has room to carry. There is no seating fault a re-anchor could catch here because there is no
    // place in this file `f` could go wrong.
    function doorWhyNoOf(read) {
      if (!read) return null;
      var g = read.grid, door = read.which ? "the exit" : "the entry";
      var work = read.which ? "arriving" : "departing";
      var other = read.which ? "departing" : "arriving";
      var where = " of a " + g.w + " x " + g.h + (g.drawn ? " buffer" : " frame");
      if (read.offPx >= DOOR_SLIP) {
        return door + " door leaks: the fold stands " + read.offPx.toFixed(2) + " points" + where
             + " open, so the frame reads the " + work + " work folded into wedges rather than "
             + "standing flat, where " + door + " door's own law asks for that work at every point";
      }
      if (read.bare) {
        return door + " door leaks: " + read.bare + " of the " + read.walked + " points this "
             + "reading walked" + where + " read outside the " + work + " work altogether, so the "
             + "frame carries the picture's own edge smeared across it, where " + door + " door's "
             + "own law asks for the " + work + " work cover-fitted at every point";
      }
      if (read.other >= DOOR_SHOW) {
        return door + " door leaks: the " + other + " work stands at "
             + read.other.toFixed(6) + " of the frame, so the frame is a blend of two photographs "
             + "and not one, where " + door + " door's own law asks for the " + work
             + " work alone at every point";
      }
      if (read.mask >= DOOR_SHOW) {
        return door + " door leaks: the judges' own channel stands at " + read.mask.toFixed(6)
             + ", so the frame draws the sample's own travel over a " + g.w + " x " + g.h
             + (g.drawn ? " buffer" : " frame") + " instead of the " + work + " work, where " + door
             + " door's own law asks for the " + work + " work at every point";
      }
      return null;
    }

    // THE NUMBERS OF ONE FRAME, WITH ITS DOOR READ ON THE BUFFER BEING DRAWN. Away from a door this
    // is `posed` and nothing more: the reading is taken nowhere else. At a door it walks its own
    // sample point over the buffer and publishes what it read — how many points it walked, how many
    // read outside the work, how far the furthest sample stands from its flat place, and how much of
    // the other work stands in the frame.
    function values(st) {
      var v = posed(st);
      var read = doorReadOf(v, st);
      v.doorGrid = read ? read.grid : null;
      v.sampleMap = read ? { walked: read.walked, bare: read.bare, offPx: read.offPx,
                             other: read.other, fold: read.fold } : null;
      v.doorHeld = null;
      v.doorWhyNo = doorWhyNoOf(read);
      return v;
    }

    // ONE TRAVELLING NUMBER, read on the diagnostic surface: how far the passage has come. THE
    // RESPONSE IS THE IDENTITY, and that is the module's own measured result rather than a default —
    // walking its raw dial in steps of 0.02 and reading the mean channel distance between
    // neighbouring frames gives a spread of 1.33 across the whole travel, because the fold's wedges
    // are a lattice at even angular steps and equal steps of the dial already carry equal change
    // (kaleidoscope.js:353-358). What this instrument adds on top of that dial is the sine window
    // above, whose own band is measured in the suite and published on the `mix` handle.
    function feelOf(u) { return clamp(u, 0, 1); }

    var manifest = {
      id: "kaleidoscope", api: 1, arity: 2,
      // The picture opens into a rosette, the two works exchange under its deepest fold, and the
      // rosette closes onto the arriving photograph.
      roles: ["disassembly", "mystery", "assembly"],
      // WHAT THIS INSTRUMENT CUTS ON, declared by the instrument itself. A RING: the wedge tiles
      // outward into mirrored rings about the work's own measured centre, and the ring is the
      // element the composer's `radial` measure cuts on (`KIND_OF_MEASURE.radial`). The composer's
      // own census names the ring cut as the one with no frame-filling instrument at all — the
      // meshing instrument cuts on rings and writes coverage, so it can only ever be the travelling
      // voice — and this one fills the frame, which is what a ground has to do.
      //
      // NOT `wedge`, though the fold plainly makes wedges. The composer's wedge kind is the pivot of
      // a SHARED ROTATIONAL ORDER, drawn from a work's own measured wedge set, and 3 of the
      // collection's 121 works carry one; the wedges this instrument makes are the fold's own
      // symmetry rather than an element set a pair could be cast from. Claiming the kind would let a
      // pivot be held on elements this instrument never reads.
      cuts: ["ring"],
      // WHERE THIS INSTRUMENT HAS A SEAM (§8's `seams` block), declared so the host can round both
      // rather than this file carrying two copies of one argument. The WEDGE seam is the fold's own
      // angular crease — the corner the triangle wave turns at every wedge edge; the RING seam is
      // the same crease read in the radial repeat, where the tiling mirrors. Both are HAIRLINE
      // retouches: the fold is already continuous across either edge, so what is rounded is the sign
      // flip in its own derivative, a fact about the sampling grid rather than about either work, and
      // `of` names no handle because a hairline does not shrink as its element repeats more often.
      seams: [{ kind: "wedge", of: null, unit: "points of the drawing buffer" },
              { kind: "ring", of: null, unit: "points of the drawing buffer" }],
      // WHAT A PAIR MUST READ FOR THE CROSSING TO BE WORTH PLAYING HERE, said in the instrument's own
      // terms and left for the composer to test against the collection's own floors — the numbers
      // belong to the collection and no instrument may keep a copy of them.
      //
      // In plain words: BOTH photographs have to read as radial at all, so the fold is opening a
      // structure both of them carry rather than one imposed on a work that has none; and the work
      // the passage ARRIVES at has to read radial strongly, on RINGS rather than on spokes, because
      // the rosette is what that work's own rings open into and a work of spokes turns instead. A
      // pair of two facades with no centre between them gets nothing from this instrument and should
      // be carried by something else.
      // WHAT THIS INSTRUMENT READS OF A PAIR, and it is a reading rather than a condition.
      //
      // An `asks` block stood here and named two FLOORS and a direction: both works over the
      // collection's cut-line floor, and the ARRIVING work over the tight floor with its own subtype
      // on rings. Three things were wrong with it and all three are his own words. A measurement
      // ranks the genres of a crossing and sets the parameters inside the winning one; it never
      // decides whether a pair qualifies (2026-08-18 09:51 and 09:53), so a floor here could only
      // take a crossing away from a visitor. The collection's floors were struck from the composer
      // the same morning, so both were names for numbers no longer in the tree. And a reading of a
      // PAIR carries no direction, so a condition on the arriving work alone would have cast an edge
      // one way and refused it the other.
      //
      // Every one of the three readings survives, as the ranking it always was. The composer holds
      // the arithmetic in `INSTRUMENT_SUITS`, which is the one place holding both records; this
      // block is the fact the instrument owns — what it reads, and what a whole fit and a fit of
      // nothing mean for it.
      suits: { reads: ["structure.radial.score", "structure.radial.subType"],
               how: "the wedge tiles outward into mirrored rings about the work's own centre, so it "
                  + "suits a pair BOTH of whose works read radial — the weaker of the two readings "
                  + "is the fit, because a fold opening a structure only one work carries is laid "
                  + "on rather than found — and it suits it more where the pair's own subtype is "
                  + "rings, since rings are what open into a rosette and spokes turn instead" },
      // WHERE THIS STANDS ON THE CHARTER'S SHELF. Two records answer, and they answer differently, so
      // both are carried and the reading is said to be derived from the pair of them.
      //   · SURFACE — lab/CROSSING-HISTORY.md's vocabulary table, which is his own standing verdict:
      //     the whole frame's coordinate is remapped at once and what happens happens to the picture
      //     as a surface.
      //   · CELL — lab/data/module-contract.json's own row for this module: the wedge is a cell, and
      //     during the fold the frame is partitioned into wedges and rings that mirror at every edge.
      // NO WORLD IS CLAIMED, and that is a decision with a consequence. This instrument carries no
      // camera and opens no space the eye travels into: it folds a surface. Charter shelf 8's folded
      // space, which shelf 6 says consumes the crossing's one miracle, is what the composer's own
      // `worldOf` opens ON TOP of a passage, and it stays the composer's to spend. So a step whose
      // role has no miracle to spend — a quiet link, an entrance, a return — can still be carried by
      // this instrument, which is what keeps the ring cut answered at every role rather than at two.
      levels: ["SURFACE", "CELL"],
      params: { wedges: [WEDGES_MIN, WEDGES_MAX], twist: [TWIST_MIN, TWIST_MAX],
                rings: [RINGS_MIN, RINGS_MAX], reach: [REACH_MIN, REACH_MAX] },
      // EVERY handle a score can drive (§4.4b). `mix` is the dial — the module's own `fold` key under
      // the name every instrument in this engine gives it, carrying the crossing's whole shape.
      // `clock` is the second the host hands down, which is the module's own wander and breath.
      // `centreX`/`centreY` are where the fold reads the pair. Four are the module's declared
      // parameters a pair can stand. `shade` is the finish's own weight, resting where the module
      // rests it, and `mask` is the judges' channel.
      //
      // NO `seed` HANDLE, AND THAT IS A DECISION. Nothing in this picture is rolled: the module holds
      // no die and this instrument adds none, so a handle a score could walk without moving the
      // picture would be noise in the score (§4.4b). A seeded run repeats to the pixel because there
      // is nothing to seed.
      //
      // NO `turn` HANDLE EITHER, and the module's own reasoning is why. The module opened one, and
      // wrote in the same breath that its travel is exactly ONE SYMMETRY STEP of the fold, so its two
      // doors are the same frame pixel for pixel (kaleidoscope.js:259-287). The turn a passage needs
      // is already in the picture — the closed-form `rotOf` rides the `clock` handle — and a second
      // handle whose two ends coincide would be a handle naming no measurement of any work. The turn
      // that reaches this instrument reaches it as the second.
      handles: {
        // NO LEVEL FOR `mix`, `clock`, `shade` OR `mask`: the crossing's own dial, the module's own
        // time, and the fleet's own judge channels — none of them drive a structural level.
        mix: { min: 0, max: 1, def: 0,
               unit: "the passage's own travel, door to door",
               reads: "the pass's own progress; it opens the fold to whole at the middle of the "
                    + "passage and closes it onto the arriving work",
               applied: { window: "one sine over the whole hand", swapHalfWidth: SWAP_HALF,
                          swapStandsUnder: SWAP_UNDER },
               level: null },
        clock: { min: 0, max: CLOCK_MAX, def: 0,
                 unit: "the second the host hands down",
                 reads: "the transaction's own seconds; the module's own wander, breath and turn "
                      + "are pure functions of it, so a driven walk repeats to the pixel",
                 level: null },
        // THE MEASUREMENTS THE FOLD'S CENTRE READS. His 19:13 word lifted to the class at 19:21: a
        // geometric parameter names the measurement of the photograph it derives from. The module
        // anchored its wander on two numbers chosen by eye for its own two photographs; the anchor
        // here is the pair's own measured radial centre, which is the very place the works turn
        // about, and the module's wander rides on it unchanged.
        // THE CENTRE IS DECLARED IN THE HOUSE THE FILL ACTUALLY READS IT FROM. A record carries the
        // point a work turns about twice — as `motifs.radialCentre` and as `structure.radial.centre`
        // — and `measuredParts()`'s own `radialCx`/`radialCy` read the motif FIRST, falling back to
        // the radial reading only where a work carries no motif. Every work of this collection
        // carries the motif, so naming the fallback made the sentence unprovable: a run that varies
        // `structure.radial.centre` sees this handle stand still and cannot tell a wrong wiring from
        // a second name for one number. Both houses are named now, in the order the code reads them,
        // which is the rule tests/test_pass_reads.py's own header states for every such twin.
        centreX: { min: 0, max: 1, def: 0.5,
                   unit: "across the picture, from its left edge",
                   reads: "motifs.radialCentre, and structure.radial.centre where a work carries no "
                        + "motif — the midpoint of the two works' own measured radial centres, "
                        + "which is the point the fold is built around",
                   applied: { wanderRidesOn: "the module's own driftX" },
                   level: "SURFACE" },
        centreY: { min: 0, max: 1, def: 0.5,
                   unit: "down the picture, from its top edge, the way every place in a work "
                       + "record is measured",
                   reads: "motifs.radialCentre, and structure.radial.centre where a work carries no "
                        + "motif — the midpoint of the two works' own measured radial centres, read "
                        + "on the other axis",
                   applied: { wanderRidesOn: "the module's own driftY",
                              turnedOverOnce: "the fold reads up the picture" },
                   level: "SURFACE" },
        wedges: { min: WEDGES_MIN, max: WEDGES_MAX, def: WEDGES_DEF, kind: "enum", step: 1,
                  unit: "how many wedges the fold makes round the centre",
                  reads: "the work's own measured rotational order — its `wedge` element set, the "
                       + "count the collection records where a work carries a rotational symmetry "
                       + "at all (rotational order 2 is the measurement floor). WHERE A WORK "
                       + "CARRIES NONE the fold stands at 8, which is the vista preset his taste "
                       + "approved on 2026-08-08 11:39 and the module's own default besides; that "
                       + "case is a gap in the record rather than a number this file invented, and "
                       + "it is said here rather than left for a reader to discover",
                  applied: { withoutARotationalOrder: WEDGES_DEF },
                  level: "CELL" },
        twist: { min: TWIST_MIN, max: TWIST_MAX, def: TWIST_DEF,
                 unit: "how far the wedge leans as it goes out",
                 reads: "structure.polar.twirl — how strongly the work's own making reads as a "
                      + "twirl. A work that was turned about its centre gets a fold that turns "
                      + "with it; one that was not gets a straight rosette. Its rest of 0.55 is "
                      + "the vista preset his taste approved on 2026-08-08 11:39",
                 level: "CELL" },
        rings: { min: RINGS_MIN, max: RINGS_MAX, def: RINGS_DEF,
                 unit: "how many times the wedge tiles outward before it mirrors",
                 reads: "structure.ownDevice.count where the work's own device is rings — the "
                      + "measured number of radial repeats the work itself carries, read onto this "
                      + "handle's own span",
                 applied: { ceiling: RINGS_MAX,
                            whoseNumber: "his standing verdict in the charter's vocabulary table, "
                                       + "«rings>2 washes to milk»; the module publishes up to 5" },
                 level: "CELL" },
        reach: { min: REACH_MIN, max: REACH_MAX, def: REACH_DEF,
                 unit: "how much of the picture one wedge reads, across it",
                 reads: "structure.ownDevice.stepPx over the work's own frame side where the "
                      + "work's own device is rings — how coarse the work's own radial repeat is, "
                      + "which is what one wedge should take in",
                 applied: { breathesBy: 0.26, whose: "the module's own driftZoom, on the clock" },
                 level: "CELL" },
        shade: { min: 0, max: 1, def: 1,
                 unit: "the finish's own weight",
                 reads: "a judge channel the module rests at 1",
                 applied: { gamma: 1.24, boost: 1.12, vignette: 0.34,
                            restsAt: "both doors, whatever this handle is placed at" },
                 level: null },
        // THE MEASUREMENT THIS HANDLE IS READ AGAINST AT A DOOR. `readAtADoor` says what is read
        // (this instrument's own sample point, walked at the buffer's own sample points), on which
        // grid (the drawing buffer the host binds, with the CSS frame where it hands none), what the
        // reading is counted in, and that there is no hold — the fold at a door is a sine at its own
        // zero, so a door this reading finds a fault at is refused outright.
        mask: { min: 0, max: 1, def: 0,
                unit: "the judges' channel: the sample's own travel, as colour",
                reads: "a judge channel the module rests shut",
                applied: { readAtADoor: { points: DOOR_SLIP, readOn: "the drawing buffer",
                                          reads: "the sample point",
                                          measures: "how far each walked point's sample stands from "
                                                  + "its flat place, how many read outside the work "
                                                  + "at all, and how much of the other work stands "
                                                  + "in the frame",
                                          held: null } },
                level: null },
      },
      neutrals: { a: 0, b: 1 },
      doors: { in: { handle: "mix", value: 0, work: "a" },
               out: { handle: "mix", value: 1, work: "b" } },
      // BOTH DOORS FRAME ALIKE, AND NEITHER TAKES A BITE OUT OF THE WORK. The fold reads the picture
      // through the mirror rather than past its edge, so nothing has to be held in reserve and the
      // door is the plain cover fit — which is what lab/data/module-contract.json's own framing row
      // for this module already publishes: «the flat end is the plain cover-fit of the same texture,
      // so both doors frame the picture alike».
      framings: { "0": { coverCrop: 1 }, "1": { coverCrop: 1 } },
      drivers: ["progress", "cueProgress", "time", "velocity", "capability", "noise", "static",
                "curve", "spline", "map", "add", "multiply", "mix", "clamp", "hold", "segment",
                "ramp", "slew", "oscillate", "node"],
      camera: { needs: "none", authority: "stage" },
      // THE PICTURE'S OWN CHAIN OF SMALLER COPIES, asked for by §8's `gl.readsChain`. Every
      // instrument that magnifies and minifies one frame at once pays for a missing chain and a
      // kaleidoscope pays most: at a deep sample width the outer rings alias visibly. It is also
      // what his verdict «rings past two washes to milk» was read on — the lab module minifies
      // through a chain and the mips average the picture pale, while with no chain the frame
      // ALIASES instead and does not wash at all (its spread stands at 33.41 of 255 at five
      // repeats against 33.44 at two). His ceiling of two stands on his word either way; the
      // flag is what makes the mechanism his word describes exist in this engine.
      gl: { preserveDrawingBuffer: false, readsChain: true },
      // WHAT THIS INSTRUMENT WRITES WHERE ITS OWN MATTER IS ABSENT (§7's coverage law, and the
      // per-instrument specification in docs/design/COVERAGE.md). It is absent nowhere, and unlike
      // every other ground in this collection it costs the picture nothing to be so.
      coverage: { writes: false,
                  how: "every point of the frame reads one point of one photograph at every value "
                     + "of the dial — at the doors the plain cover fit, in between a folded "
                     + "coordinate the mirror holds inside the picture — so the alpha is the "
                     + "constant 1 and both doors publish a cover crop of 1; at a door the "
                     + "instrument walks its own sample point over the buffer and refuses a door "
                     + "where any of them has left its flat place, read outside the work, or where "
                     + "the other work still stands in the frame" },
      // The neutral pose is the ENTRY DOOR — `mix` at 0, the value the `doors` block above names — so
      // the frame keys the host reads off it at registration include the door's own record.
      neutralPose: { mix: 0, clock: 0, centreX: 0.5, centreY: 0.5, wedges: WEDGES_DEF,
                     twist: TWIST_DEF, rings: RINGS_DEF, reach: REACH_DEF, shade: 1, mask: 0,
                     reduced: false, cssWidth: 1000, cssHeight: 1000,
                     fitA: [1, 1, 0, 0], fitB: [1, 1, 0, 0] },
      passes: [{
        program: "kaleidoscope", vert: VERT, frag: FRAG, position: "aPos",
        uniforms: [
          { name: "uA", type: "sampler2D", source: "textureA" },
          { name: "uB", type: "sampler2D", source: "textureB" },
          { name: "uFitA", type: "vec4", source: "fitA" },
          { name: "uFitB", type: "vec4", source: "fitB" },
          { name: "uRes", type: "vec2", source: "resolution" },
          { name: "uFold", type: "vec4", source: "frame:fold" },
          { name: "uRing", type: "vec4", source: "frame:ring" },
          { name: "uSoft", type: "vec2", source: "frame:soft" },
          { name: "uCentre", type: "vec4", source: "frame:centre" },
          { name: "uTexel", type: "vec4", source: "frame:texel" },
          { name: "uMask", type: "float", source: "handle:mask" },
        ],
      }],
      // The instrument allocates nothing of its own: it spends the two source-texture slots the host
      // already holds and the one programme the host builds from this manifest. The module's own
      // canvas, its context, its two textures with their mip chains and its own frame loop are what
      // this port does without.
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
                   programs: 1, passes: 1, bytesEstimate: 2666783, variant: "lean" },
                   standard: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0,
                               programs: 1, passes: 1, bytesEstimate: 10666783,
                               variant: "standard" },
                   rich: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                           passes: 1, bytesEstimate: 42666783, variant: "rich" } },
      capabilities: ["webgl2"],
      decline: ["one work only", "a source that never decoded"],
      provenance: { labPath: "lab/effects/kaleidoscope.js", commit: "4c7dfe4",
                    sha256: "719088dc474c56fbb0b0a016be5e3312ad9d4d81fe633962b1b3872a3377c285" },
      readiness: "production-ready",
    };

    var live = false;
    return {
      name: "kaleidoscope",
      manifest: manifest,
      values: values,
      fit: fit,
      feel: feelOf,
      // WHAT THIS INSTRUMENT'S `feel` PROMISES (Phase 7, item 3b): identity-because-no-travel.
      // `feelOf` at kaleidoscope.js:644 is the raw dial, clamped and nothing else — a written "no"
      // rather than a silence, and the generic law asks nothing of a curve that was never claimed.
      feelClass: "identity",
      prepare: function (o) {
        if (!o.sources) return { take: false, why: "the kaleidoscope needs both works: the fold "
                                                 + "carries one photograph into the other" };
        if (!o.cue) return { take: false, why: "no cue names it" };
        return { take: true };
      },
      start: function () { live = true; },
      // The pose the shader draws. The module's canvas, its frame loop, its pointer and its own
      // texture uploads are gone, so every number here comes from a handle a score drives or from the
      // frame the host is about to bind.
      //
      // A DOOR THIS INSTRUMENT CANNOT KEEP WHOLE IS REFUSED RATHER THAN DRAWN. The door law is the
      // instrument's own claim, so the instrument is what answers for it: at either door it walks its
      // own sample point over the buffer the host is about to bind and, where a point of that grid
      // has left its flat place further than a sample can move, has read outside the work, where the
      // other work still stands in the frame, or where the judges' channel is left open, it hands the
      // host the reason with the measured numbers in it instead of drawing a door that is not the
      // photograph. The host recovers the transaction on that reason and the walk's own glide carries
      // the visitor, which is the product's own behaviour with no renderer.
      frame: function (st) {
        if (!live) return;
        var h = st.handles;
        var pose = {
          mix: h.mix, clock: h.clock, centreX: h.centreX, centreY: h.centreY,
          wedges: h.wedges, twist: h.twist, rings: h.rings, reach: h.reach,
          shade: h.shade, mask: h.mask, reduced: st.reduced,
          cssWidth: st.viewport.w, cssHeight: st.viewport.h,
          // THE GRID THE SHADER WILL SAMPLE ON, carried into the pose so the crease's own softening
          // is read in the points of the frame the host is about to bind as `uRes` and the door is
          // read on it rather than on the CSS frame around it. The host settles it from the device
          // ratio and its own resolution step, so it moves while a pass plays and each door is read
          // on the grid standing at that door's own instant.
          bufWidth: st.viewport.bufferW, bufHeight: st.viewport.bufferH,
          // BOTH WORKS' SEATING ON THIS BUFFER, which only the host can answer. Each work's own
          // aspect correction is recovered from it, so the script and the shader work from ONE
          // seating rather than two guesses at it.
          fitA: st.fitA, fitB: st.fitB,
          // THE CREASE'S SOFTENING, off the host's own `seams` reading (§8's `seams` block). Only
          // the host knows what every instrument declaring a hairline retouch is holding its own
          // crease to, so it answers once and this file carries the number rather than choosing it.
          seam: st.seams,
        };
        // AT A DOOR THE INSTRUMENT SAYS WHAT IT APPLIED, and says it before it refuses. The reading
        // is taken on the buffer this frame is drawn on, so it is the run-time truth his 18:00
        // decision asks for. `request` is the travel a door asks of the sample point — none — and
        // `applied` is the travel this grid actually shows, so `moved` is the two read against each
        // other in the grid's own points.
        if (h.mix === 0 || h.mix === 1) {
          var v = values(pose);
          if (st.reportApplied) {
            st.reportApplied({
              door: h.mix === 0 ? "in" : "out",
              buffer: [pose.bufWidth, pose.bufHeight],
              reads: "the sample point", request: 0,
              applied: v.sampleMap ? v.sampleMap.offPx : null,
              moved: v.sampleMap ? v.sampleMap.offPx : null,
              unit: "points of the drawing buffer",
              // What the fold itself was doing at this door: how deep it stood, how many walked
              // points read outside the work, and how much of the other work stood in the frame.
              fold: v.sampleMap ? v.sampleMap.fold : null,
              bare: v.sampleMap ? v.sampleMap.bare : null,
              other: v.sampleMap ? v.sampleMap.other : null,
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
    instrument: kaleidoscopeInstrument(),
  });
})();
