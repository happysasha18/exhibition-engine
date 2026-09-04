/*!pass-inst-veil.js*/
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
// OWNERSHIP, AND WHERE THIS ONE CAME FROM. `lab/effects/` holds no fog module. The charter's shelf
// 14 asks for one — «fog/veil layers, hiding and revealing; depth read as thickness» — so the
// mathematics below is authored here rather than ported, and that is said out loud: `provenance
// .labPath` is null, no response curve is carried, and every constant that is not derived names the
// sentence it stands on.
//
// THE INSTRUMENT IS FINISHED AND THE WIRE IS NOT. An instrument plays only where the composer holds
// a suitability reading, a register row per handle and a fill branch for it. None of the three
// exists yet, so until the fill branch lands every handle below would stand at its manifest rest for
// every pair alike. The three blocks ready to apply are in `docs/design/ELEMENTS-WIRING.md`.
(function () {
  var join = window.__@@NS@@PassInstrument;
  if (typeof join !== "function") return;

  // THIS FILE'S OWN VERSION, and the one home of that fact. The build reads this literal out of the
  // source and writes it into the site's record beside the digest, so the version a file declares
  // and the version a host was told to load cannot drift apart without the build noticing.
  var INSTRUMENT_VERSION = "1.0.0";

  // ================================================================================================
  // THE VEIL INSTRUMENT (§8) — charter shelf 14, the elements
  // ================================================================================================
  // WHAT THE VISITOR SEES. Four sheets of veil hang between the eye and the two photographs, each at
  // its own depth, each with its own bodies — thick banks and thin places — and each drifting on its
  // own wind, the nearest fastest and the deepest almost still. The departing photograph stands at
  // the front, in front of every sheet, and is seen exactly as its file carries it. Over the passage
  // the two works TRADE DEPTHS: the departing one walks back through the sheets one at a time while
  // the arriving one walks forward, and each is seen through whatever veil has come to stand in
  // front of it. Where the veil is thin the deeper work shows through and reads soft; where it banks
  // thick the nearer work holds the frame. The arriving work therefore arrives by COMING FORWARD —
  // it appears first in the thin places, as its own soft mass, and sharpens as it passes each sheet.
  //
  // DEPTH IS READ AS THICKNESS, AND THICKNESS IS READ AS COARSENESS. A photograph seen through veil
  // is not a photograph mixed with grey; it is a photograph whose own light has been scattered on
  // the way to the eye, which is to say a photograph read at a coarser scale of its own. So the one
  // thing the thickness in front of a work does here is choose HOW COARSELY that work is read, off
  // the chain of smaller copies the host uploads with every source. The veil writes no colour of its
  // own anywhere in this file, and there is nothing in it that could whiten a frame.
  //
  // ------------------------------------------------------------------------------------------------
  // THE FOUR THINGS THE CONSTRUCTION HAS TO ANSWER
  // ------------------------------------------------------------------------------------------------
  //   · WHAT A SHEET IS. A field over the frame with a floor under it: `FLOOR + (1 − FLOOR) · noise`,
  //     so a sheet is thinner in some places and thicker in others and is NOWHERE ABSENT. That floor
  //     is what makes both doors exact, and the paragraph on the doors below says exactly how.
  //   · HOW MUCH VEIL STANDS IN FRONT OF A WORK. The sheets between the eye and that work, added up.
  //     A sheet is not a plane but a SLAB of its own thickness in depth, so a work moving back
  //     through it takes it on gradually — `smoothstep` across the slab — rather than the whole
  //     sheet switching on at one instant across the whole frame, which would read as a flash.
  //   · WHICH WORK STANDS AT A POINT. The one with LESS veil in front of it at that point. Nothing
  //     else decides it, and the two works are never mixed: the crossover between them is one point
  //     of the drawing buffer, read off the analytic gradient of the two thicknesses' own difference.
  //   · HOW DEEP A WORK LOOKS. Its own thickness, spent as the level of the chain it is read at. A
  //     work with nothing in front of it is read at the sharpest copy, which is its file.
  //
  // WHY THE DOORS ARE EXACT, IN ONE PARAGRAPH. At the entry door the departing work stands at a
  // depth in front of every slab, so nothing at all stands in front of it and its thickness is
  // exactly nothing at every point of the frame: it is read at the sharpest copy and it is the file.
  // The arriving work stands at a depth behind every slab, so all four sheets stand in front of it
  // and its thickness is at least four times the floor — which is strictly greater than nothing at
  // every point, because a sheet is nowhere absent. So the departing work has less veil in front of
  // it EVERYWHERE and takes every point of the frame. The exit door is the same sentence with the
  // two works exchanged. Neither reading has a width in it and neither can be closed or opened by a
  // grid, which is why the door reading below is a claim proved rather than a range guarded.
  //
  // ------------------------------------------------------------------------------------------------
  // THE BANS, AND THE ONE THIS INSTRUMENT CAME NEAREST TO
  // ------------------------------------------------------------------------------------------------
  // NO ALPHA CROSSFADE AS THE ARRIVAL, and this is the ban a fog stands closest to — a veil that
  // thickens over one picture and thins over another IS a crossfade wearing weather. Three things
  // keep this one clear of it, and each is checkable rather than asserted.
  //   · THE TWO WORKS ARE NEVER WEIGHED AGAINST EACH OTHER. At a point one of them stands, whole,
  //     and the other is not drawn there at all. The only place a mix runs is the one-buffer-point
  //     crossover between them, which is anti-aliasing and is the same construction the material and
  //     the water instruments both close their boundaries with.
  //   · WHAT TRAVELS IS A DEPTH AND NOT A WEIGHT. The dial moves the two works through the stack;
  //     it touches no opacity, and this file publishes no opacity to touch.
  //   · THE BOUNDARY HAS A SHAPE OF ITS OWN AND IT MOVES. It is the isoline where the two
  //     thicknesses meet — the shape of the sheets standing between the two works — so what a
  //     viewer watches is a bank of veil parting, drifting on its own wind, and never a rectangle
  //     getting lighter.
  //
  // NO PATTERN LAID OVER A WORK THAT CARRIES ITS OWN. The sheets are never drawn. They are read to
  // decide which work stands where and how coarsely it is read, and neither of those puts a mark on
  // the picture; the bodies a viewer sees are the two photographs' own material at two scales.
  // NO ROTATIONAL GESTURE THAT RETRACES ITS OWN PATH. Nothing turns; the sheets drift in one
  // direction, the works travel in depth in one direction, and neither comes back.
  // NOTHING THAT READS AS A STOCK EFFECT. The stock fog is a wash of grey or white over the frame at
  // a rising opacity. There is no colour here to wash with — the veil's whole effect is the level of
  // the chain each work is read at — so the frame can never lose its picture to a haze.
  function veilInstrument() {
    var VERT = [
      "attribute vec2 aPos;",
      "varying vec2 vUv;",
      "void main(){ vUv = vec2(aPos.x * 0.5 + 0.5, 0.5 - aPos.y * 0.5); gl_Position = vec4(aPos, 0.0, 1.0); }",
    ].join("\n");

    // ----------------------------------------------------------------------------------------------
    // THE SHADER
    // ----------------------------------------------------------------------------------------------
    // FOUR SHEETS AND NOT A NUMBER A SCORE PICKS. Three sheets leave no veil standing between the
    // two works over the middle of the passage, where the crossing actually happens; past four the
    // slabs crowd inside the depth a work travels and each is thinner than the step between two
    // levels of the chain, so a fifth sheet changes nothing a viewer can see and costs a fifth
    // gradient every point. The count is therefore fixed here, said out loud, and the SPREAD of the
    // four in depth is what a score drives.
    var FRAG = [
      "precision highp float;",
      "varying vec2 vUv;",
      "uniform sampler2D uA;",          // the work the visitor is leaving, walking back
      "uniform sampler2D uB;",          // the work arriving, walking forward
      "uniform vec4 uFitA;",
      "uniform vec4 uFitB;",
      "uniform vec2 uRes;",
      // zA, zB: the two works' own depths. slab: half the depth one sheet occupies.
      // weight: how much thickness one sheet carries at its thickest.
      "uniform vec4 uDepth;",
      // the four sheets' own depths, nearest first
      "uniform vec4 uStack;",
      // bodies: how many bodies of veil stand across the frame, on the nearest sheet.
      // ax, ay: which way the wind carries them. run: how far it has carried them.
      "uniform vec4 uAir;",
      "uniform float uMask;",
      "uniform float uSeamPts;",     // §8's `seams` block: the isoline's hairline, in points of the drawing buffer
      // HOW THIN A SHEET IS WHERE IT IS THINNEST. Not nothing, and that is the whole of why the
      // doors are exact: a sheet with a hole in it would let the far work through at the door.
      "const float FLOOR = 0.22;",
      // HOW MUCH COARSER EACH SHEET STANDS THAN THE ONE IN FRONT OF IT, and how much slower it
      // drifts. Both are the same fact seen twice — a body further away subtends less and moves
      // less — which is the one depth cue this construction spends beyond the thickness itself.
      "const float COARSER = 1.65;",
      // THE DEEPEST THE CHAIN IS EVER READ AT. Five levels is a copy 32 times smaller each way, at
      // which a photograph is its own masses and nothing else; past that every picture is one
      // colour and the veil would start writing a wash after all.
      "const float DEEPEST = 5.0;",
      "float h11(vec2 i){ return fract(sin(dot(i, vec2(41.317, 289.107)) + uAir.w) * 43758.5453); }",
      // value noise with its own exact gradient — the same construction the material instrument
      // carries. The gradient is what closes the boundary below inside one point of the buffer
      // without a second sample.
      "vec3 vnoise(vec2 p){",
      "  vec2 i = floor(p), f = fract(p);",
      "  float a = h11(i), b = h11(i + vec2(1.0, 0.0));",
      "  float c = h11(i + vec2(0.0, 1.0)), d = h11(i + vec2(1.0, 1.0));",
      "  vec2 u = f * f * (3.0 - 2.0 * f);",
      "  vec2 du = 6.0 * f * (1.0 - f);",
      "  float k = a - b - c + d;",
      "  return vec3(a + (b - a) * u.x + (c - a) * u.y + k * u.x * u.y,",
      "              ((b - a) + k * u.y) * du.x,",
      "              ((c - a) + k * u.x) * du.y);",
      "}",
      "vec2 into(vec2 p, vec4 f){",
      "  return clamp((p - 0.5) * f.xy + 0.5 + f.zw, 0.0008, 0.9992);",
      "}",
      "void main(){",
      "  vec2 uv = vUv;",
      "  float aspect = uRes.x / max(uRes.y, 1.0);",
      "  vec2 p = vec2(uv.x * aspect, uv.y);",
      "  vec2 wind = vec2(uAir.y, uAir.z);",
      "  float slab = max(uDepth.z, 1e-4);",
      // THE FOUR SHEETS, WALKED ONCE. For each: how much of it stands in front of the departing
      // work, how much in front of the arriving one, its own body at this point, and the gradient
      // of that body. The two thicknesses and the gradient of their difference all come out of the
      // one walk.
      "  float tA = 0.0, tB = 0.0;",
      "  vec2 gd = vec2(0.0);",
      "  for (int l = 0; l < 4; l++) {",
      "    float zl = l == 0 ? uStack.x : (l == 1 ? uStack.y : (l == 2 ? uStack.z : uStack.w));",
      "    float cells = uAir.x / pow(COARSER, float(l));",
      "    float speed = 1.0 / (1.0 + zl);",
      "    vec3 nv = vnoise(p * cells + wind * uAir.w * speed);",
      "    float body = FLOOR + (1.0 - FLOOR) * nv.x;",
      "    vec2 gb = (1.0 - FLOOR) * nv.yz * cells;",
      // A SLAB AND NOT A PLANE: how much of this sheet a work at depth z has already passed behind.
      "    float sA = smoothstep(zl - slab, zl + slab, uDepth.x);",
      "    float sB = smoothstep(zl - slab, zl + slab, uDepth.y);",
      "    tA += sA * uDepth.w * body;",
      "    tB += sB * uDepth.w * body;",
      "    gd += (sB - sA) * uDepth.w * gb;",
      "  }",
      // WHICH WORK STANDS HERE: the one with less veil in front of it. The crossover is one point of
      // the drawing buffer wide, read off the gradient the walk above already computed, so the
      // boundary carries no fade of its own and no step either.
      "  vec2 gp = vec2(gd.x / max(uRes.x, 1.0) * aspect, gd.y / max(uRes.y, 1.0));",
      "  float band = max(length(gp), 1e-6);",
      "  float cov = clamp(0.5 + (tB - tA) / (band * uSeamPts), 0.0, 1.0);",
      // HOW DEEP EACH WORK LOOKS. Its own thickness spends the level of the chain it is read at, so
      // a work with nothing in front of it is read at the sharpest copy — its file, to the point.
      "  vec3 colA = texture2D(uA, into(uv, uFitA), DEEPEST * clamp(tA, 0.0, 1.0)).rgb;",
      "  vec3 colB = texture2D(uB, into(uv, uFitB), DEEPEST * clamp(tB, 0.0, 1.0)).rgb;",
      "  vec3 col = mix(colB, colA, cov);",
      // THE JUDGES' OWN FRAME: which work stands at this point, and the two thicknesses that decided
      // it. It is read as colour and carries no coverage of its own, because what it is for is to be
      // measured rather than looked at.
      "  vec3 judge = vec3(cov, clamp(tA, 0.0, 1.0), clamp(tB, 0.0, 1.0));",
      "  col = mix(col, judge, uMask);",
      // THE COVERAGE LAW (§7). The alpha is the constant 1, and it is a decision rather than a
      // default: every point of the frame carries one of the two photographs, both branches of the
      // choice are picture, and this instrument has no absence to publish. Under the placement rule
      // (§8 as amended 14:05) `writes: false` makes it lawful as the LOWEST cue of a stack and as a
      // whole one-cue score, which is the placement a ground takes.
      "  gl_FragColor = vec4(col, 1.0);",
      "}",
    ].join("\n");

    function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }

    /* HOW THIN A SHEET IS WHERE IT IS THINNEST, in the script's own copy of the shader's constant,
       because the door reading below stands on exactly this number and a second description of one
       veil could disagree with the first. A sheet is nowhere absent, and that is the whole of why
       both doors are exact: the far work always has four floors of veil in front of it and the near
       work has none. */
    var FLOOR = 0.22;

    /* HOW FAR APART IN DEPTH THE FOUR SHEETS STAND, at either end of the `depth` handle. At the near
       end the four crowd into a fifth of the travel and the crossing happens as one bank parting; at
       the far end they spread over nine tenths of it and each is passed on its own. Both ends are
       this file's own decision and are named in its report. */
    var GAP_MIN = 0.06, GAP_MAX = 0.30;

    /* HALF THE DEPTH ONE SHEET OCCUPIES. It is derived from the gap rather than typed: a sheet's own
       slab is four tenths of the distance to its neighbour, so the four never run into one another
       at any spread a score can name and a work always passes them one at a time. */
    var SLAB_SHARE = 0.40;

    /* HOW MUCH THICKNESS ONE SHEET CARRIES AT ITS THICKEST, at either end of the `thickness` handle.
       THE FLOOR UNDER IT IS THE POINT: a `thickness` of nothing is still a real veil, so the doors
       stay exact for every value of every handle rather than for every value but one. A quarter is a
       veil the deeper work reads plainly through; a whole one buries it in its own masses. */
    var WEIGHT_MIN = 0.25, WEIGHT_MAX = 1.00;

    /* HOW MANY BODIES OF VEIL STAND ACROSS THE FRAME on the nearest sheet, at either end of the
       `bodies` handle. Two is one bank filling half the frame; forty is a body six points wide on a
       390-point frame, at which the veil stops being weather and starts being grain. */
    var BODIES_MIN = 2, BODIES_MAX = 40;

    /* HOW FAR THE WIND CARRIES THE NEAREST SHEET IN ONE SECOND, in frame widths. The deeper sheets
       take a share of it — `1 / (1 + depth)` — which is the same parallax the shader spends on their
       cell counts, one fact seen twice. */
    var WIND_RATE = 0.045;

    // THE DEAD BANDS AT EITHER END OF THE HAND. Over the first and last five hundredths of the
    // dial the two works stand at the two ends of their travel and neither has begun to move, so
    // the standing work is the picture its source carries, to the point.
    //
    // UNJUSTIFIED — a local copy of the one home, pass-inst-boxfold.js:458 (plan row S-82,
    // 2026-09-03); a pass-inst-*.js file is independently loaded and version-pinned (PASS-API-V1
    // §1.2) with no shared runtime to read that file's value from, so this literal is kept in
    // sync by hand rather than by construction.
    var FEEL_D0 = 0.05;

    /* NO RESPONSE CURVE IS CARRIED, and that is a fact rather than an omission: there is no lab
       module here whose felt change was measured, and fitting a curve to a picture nobody has
       watched would be a number nobody read reaching the picture. What the hand gets is the dead
       bands and nothing else. What a viewer actually feels is the SLAB — a work crosses a sheet
       over the slab's own depth, so the passage already has four events in it rather than one
       even ramp, and those four are geometry rather than taste. */
    function feelOf(u) {
      return clamp((clamp(u, 0, 1) - FEEL_D0) / (1 - 2 * FEEL_D0), 0, 1);
    }

    /* THE SPAN THE SCORE'S DIE ARRIVES ON, and what this instrument spends it on: WHERE THE BANKS OF
       VEIL STAND. The die is the offset in the sheets' own hash, so two passes over one edge meet
       two different weathers while every other number of the frame stays where the score put it —
       charter shelf 13's rubato read on this instrument's own axis. It moves neither door: whatever
       the banks look like, a sheet is nowhere absent and that is all a door reads. */
    var SEED_SPAN = 8;

    /* THE FOUR SHEETS' OWN DEPTHS, and the two ends the works travel between. The stack is centred
       on the middle of the travel and spread by the gap, so the deepest sheet stands at
       `0.5 + 1.5·gap` and the nearest at `0.5 − 1.5·gap`. The works travel a slab and a margin past
       both, which is what puts a work in front of every sheet at one door and behind every sheet at
       the other — derived from the stack rather than typed against it. */
    function stackOf(gap) {
      return [0.5 - 1.5 * gap, 0.5 - 0.5 * gap, 0.5 + 0.5 * gap, 0.5 + 1.5 * gap];
    }
    var DEPTH_MARGIN = 0.05;
    function reachOf(gap) {
      return 1.5 * gap + SLAB_SHARE * gap + DEPTH_MARGIN;
    }

    // Cover-fit a work into the frame and nothing beyond it. Nothing here is displaced at all — the
    // veil moves no point of either picture, it only chooses which picture stands at a point and how
    // coarsely it is read — so BOTH DOORS FRAME AT A CROP OF EXACTLY ONE.
    function fit(iw, ih, w, h) {
      var fa = w / Math.max(h, 1);
      var ia = iw / Math.max(ih, 1);
      if (ia > fa) return [fa / ia, 1, 0, 0];
      return [1, ia / fa, 0, 0];
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
    // and every number in the pose comes from a handle a score drives. The one place a second is read
    // is the wind's own run, which reads the `clock` handle rather than a wall clock, so a seeded
    // score repeats to the pixel.
    function values(st) {
      var d = feelOf(st.mix);
      var gap = GAP_MIN + (GAP_MAX - GAP_MIN) * clamp(st.depth, 0, 1);
      var stack = stackOf(gap);
      var reach = reachOf(gap);
      // THE TWO WORKS TRADE DEPTHS ON ONE STRAIGHT LINE. The departing work walks from a reach in
      // front of the nearest sheet to a reach behind the deepest one; the arriving work walks the
      // same line backwards. They cross exactly at the middle of the stack, which is the instant the
      // frame is most evenly shared — and both ends are past every slab, which is what makes both
      // doors exact.
      var zA = (0.5 - reach) + d * 2 * reach;
      var zB = (0.5 + reach) - d * 2 * reach;
      var weight = WEIGHT_MIN + (WEIGHT_MAX - WEIGHT_MIN) * clamp(st.thickness, 0, 1);
      var bodies = BODIES_MIN + (BODIES_MAX - BODIES_MIN) * clamp(st.bodies, 0, 1);
      var ang = (Number(st.airAngle) || 0) * Math.PI / 180;
      var run = (st.reduced ? 0 : (Number(st.t) || 0)) * WIND_RATE;
      var phase = (clamp(st.seed, 0, SEED_SPAN) / SEED_SPAN) * 2 * Math.PI;
      var v = {
        depth: [zA, zB, SLAB_SHARE * gap, weight],
        stack: stack,
        air: [bodies, Math.cos(ang), Math.sin(ang), run],
        // the same numbers by name, for the reading below and for the diagnostic surface
        dialAt: d, zA: zA, zB: zB, gap: gap, slab: SLAB_SHARE * gap, reach: reach,
        weight: weight, bodies: bodies, angle: (Number(st.airAngle) || 0), run: run, phase: phase,
        floor: FLOOR, coverCrop: 1,
        mask: clamp(typeof st.mask === "number" ? st.mask : 0, 0, 1),
        grid: gridOf(st),
        // THE ISOLINE'S OWN HAIRLINE (§8's `seams` block, pass-layer.js), off the host's own
        // `seams` reading. Only the host knows what every instrument declaring a hairline retouch
        // is holding its own crease to, so it answers once and this file carries the number rather
        // than choosing it; `1.0` is only the value this file falls back to where no host has
        // answered yet — the same one point of the drawing buffer the crossover always read before
        // this seam was connected.
        seamPts: (st.seam && typeof st.seam.isoline === "number") ? st.seam.isoline : 1.0,
      };
      var read = doorReadOf(v, st);
      v.doorGrid = read ? read.grid : null;
      v.doorStanding = read ? read.standing : null;
      v.veil = read ? { inFront: read.inFront, behind: read.behind, clear: read.clear } : null;
      v.doorWhyNo = doorWhyNoOf(read);
      return v;
    }

    // ---- THE DOOR THE INSTRUMENT READS FOR ITSELF --------------------------------------------------
    // His 18:00 architecture decision, carried in the U27 brief: the instrument reads its doors at
    // runtime on the actual buffer, and the report it hands back is the runtime truth; what the
    // manifest declares is only the claim.
    //
    // WHY THE GRID DECIDES NOTHING HERE, AND WHAT IS READ INSTEAD. The material and the water
    // instruments read a mask that crosses over inside a band whose width the buffer sets, so for
    // them the grid is what decides a door. This instrument's choice crosses over nowhere that
    // matters at a door: at the entry door the departing work has NOTHING in front of it — every
    // sheet's own share is exactly zero, because its depth stands a full slab and a margin in front
    // of the nearest sheet — while the arriving work has all four sheets in front of it, each at
    // least its own floor. So the difference the choice reads is at least four floors on every point
    // of every buffer, and the departing work is read at the sharpest copy of its file. Neither
    // reading has a width in it.
    //
    // SO WHAT THIS READS IS THE TWO NUMBERS THE CLAIM RESTS ON, on the buffer it is about to draw:
    // how much veil stands in front of the work whose door it is (which must be exactly nothing) and
    // how much stands in front of the other (which must be strictly more than nothing at every point
    // of the frame, and is bounded below by four floors rather than sampled). A reading that is not
    // those two is a door carrying a veil the file does not, and the instrument refuses it with the
    // reading in the refusal rather than drawing it.
    //
    // It refuses on no pose this file as written can produce, and that is said plainly rather than
    // hidden: it is a claim proved, not a range guarded. The suite's red-on-bug rows take the floor
    // out from under a sheet and shorten the works' own travel, and each makes exactly this refusal
    // fire.
    function shareOf(zl, slab, z) {
      var lo = zl - slab, hi = zl + slab;
      var t = clamp((z - lo) / Math.max(hi - lo, 1e-6), 0, 1);
      return t * t * (3 - 2 * t);
    }
    function inFrontOf(v, z) {
      var i, s = 0;
      for (i = 0; i < 4; i++) s += shareOf(v.stack[i], v.slab, z);
      return s;
    }

    function doorReadOf(v, st) {
      var door = st.mix === 0 ? "in" : (st.mix === 1 ? "out" : null);
      if (door === null) return null;
      var g = v.grid;
      if (!g.given) return null;
      var standing = door === "in" ? 0 : 1;
      var zStand = standing === 0 ? v.zA : v.zB;
      var zFar = standing === 0 ? v.zB : v.zA;
      // The sheets in front of each, counted in whole sheets: nothing in front of the standing work,
      // all four in front of the other. The thickness itself is that count times the weight times a
      // body, and a body is never under the floor — so the far work's own thickness is at least
      // `sheets · weight · floor`, which is the number `clear` publishes.
      var front = inFrontOf(v, zStand);
      var behind = inFrontOf(v, zFar);
      return { grid: g, door: door, standing: standing,
               inFront: front, behind: behind,
               clear: behind * v.weight * v.floor,
               zA: v.zA, zB: v.zB, stack: v.stack, slab: v.slab };
    }

    // THE REFUSAL, worded the way the host's own manifest refusals read: what is wrong, in this
    // instrument's own measured numbers, on the grid it was measured on.
    function doorWhyNoOf(read) {
      if (!read) return null;
      var g = read.grid, where = " of a " + g.w + " x " + g.h + (g.drawn ? " buffer" : " frame");
      var who = read.door === "in" ? "departing" : "arriving";
      var other = read.door === "in" ? "arriving" : "departing";
      if (read.inFront > 0) {
        return (read.door === "in" ? "the entry" : "the exit") + " door leaks: the " + who
             + " work stands at a depth of "
             + (read.standing === 0 ? read.zA : read.zB).toFixed(4) + " with "
             + read.inFront.toFixed(6) + " of a sheet's veil in front of it" + where
             + ", so it is read off a coarser copy than its own file, where this door's own law asks "
             + "for the work exactly as the file carries it";
      }
      if (!(read.clear > 0)) {
        return (read.door === "in" ? "the entry" : "the exit") + " door leaks: the " + other
             + " work has " + read.behind.toFixed(4) + " sheets in front of it and a thinnest "
             + "thickness of " + read.clear.toFixed(6) + where + ", so somewhere on the frame it "
             + "stands as clear as the " + who + " work and takes points this door's own law gives "
             + "the " + who + " work at every point";
      }
      return null;
    }

    var manifest = {
      id: "veil", api: 1, arity: 2,
      // The departing work walks back into the veil and comes apart into its own masses, the middle
      // is a frame where neither work is wholly legible, and the arriving work gathers as it comes
      // forward.
      roles: ["disassembly", "mystery", "assembly"],
      // READ OFF THIS INSTRUMENT'S OWN CONSTRUCTION, and said to be read rather than published:
      // there is no lab module for a veil, so no vocabulary table carries a row for it.
      //   · SURFACE — one field runs over the whole frame, the difference between the two works'
      //     own thicknesses, and its value at a point decides which of them stands there. That is
      //     the level `pass-inst-adrift.js` and `pass-inst-liquid.js` both place that act at.
      //   · TEXTURE — what the veil actually does to a photograph is read it at a coarser scale of
      //     its own material. Nothing here is cut into parts and nothing is moved; the whole of the
      //     depth reads on the picture's own grain.
      // LIGHT-COLOUR IS NOT CLAIMED, and the reason is a fact about this file rather than a
      // preference: it writes no colour anywhere. A fog that whitened a frame would be moving light
      // and would owe that level; this one spends its thickness entirely on which copy of the chain
      // a work is read from, so there is no voice here for shelf 17 to count.
      levels: ["SURFACE", "TEXTURE"],
      // WHAT THIS INSTRUMENT CUTS ON. It parts each work by HOW COARSELY IT IS READ — the scale of
      // its own detail — which is the kind `KIND_OF_MEASURE` gives the recorded `texture` measure,
      // and the very half of the tonal-and-spectral pivot that cuts on a scale: the arriving work's
      // blurred mass growing first with its detail growing into it. The declaration lives here, in
      // the instrument's own file, because the site's settings build prefers a manifest's own `cuts`
      // to any table it keeps and names an instrument that declares none as UNPLACED.
      cuts: ["scale"],
      // WHERE THIS INSTRUMENT HAS A SEAM (§8's `seams` block). The crossover between the two works —
      // "the isoline where the two thicknesses meet" (above, "THE BOUNDARY HAS A SHAPE OF ITS OWN AND
      // IT MOVES") — is read as `cov = clamp(0.5 + (tB - tA) / band, 0.0, 1.0)` with `band` the
      // gradient of that difference measured in the buffer's own resolution (`gd / uRes`), which the
      // file's own words already close as "the crossover between them is one point of the drawing
      // buffer, read off the analytic gradient of the two thicknesses' own difference... anti-
      // aliasing and... the same construction the material and the water instruments both close
      // their boundaries with" (above, "THE BANS"). A HAIRLINE retouch, not a wedge, a ring or a
      // tile — the shape crossed here is a level set of a continuous field, so `isoline` is this
      // file's own word for it rather than a forced fit to one of the fleet's usual four. `of` names
      // no handle: the crossover's width is the buffer's own sampling footprint and does not depend
      // on any count this instrument publishes.
      seams: [{ kind: "isoline", of: null, unit: "points of the drawing buffer" }],
      params: { thickness: [0, 1], bodies: [0, 1], depth: [0, 1], airAngle: [0, 180] },
      // EVERY handle a score can drive (§4.4b). `mix` is the dial and `clock` is the second the host
      // hands down — the one place a second reaches this instrument at all, the wind's own run.
      // `seed` is the score's die and `mask` is the judges' frame.
      //
      // EVERY HANDLE THAT SHAPES THE PICTURE NAMES THE MEASUREMENT OF A PHOTOGRAPH IT READS, which
      // is his 19:13 word lifted to the class at 19:21. What stands here is the sentence; the
      // arithmetic that turns a reading into a value runs in the composer.
      //
      // TWO FLEET HANDLES ARE ABSENT, and each absence is a fact about this instrument:
      //   · `shade` — the judge channel for a light this instrument moves. It moves none: the veil
      //     writes no colour and casts no shadow, and publishing the handle would publish one that
      //     reaches nothing.
      //   · `travel` — how far the matter is carried. Nothing here is carried at all; the two works
      //     stay exactly where their seating puts them and only their DEPTH moves.
      // EVERY HANDLE DECLARES THE STRUCTURAL LEVEL IT DRIVES, from shelf 17's own six — WORLD,
      // SURFACE, CELL, CELL CONTENT, TEXTURE, LIGHT-COLOUR — and the composer writes a handle only
      // where its cue owns that level. A cue that does not own it rests there at the value below
      // and goes on playing the levels it does own.
      //
      // `level: null` IS FOR A HANDLE THAT DRIVES NO STRUCTURAL LEVEL, and the fleet has five such
      // handles by idiom: `mix` is the crossing's own dial, which is the passage itself and answers
      // to no ownership; `clock` is the second the host hands down; `seed` is the score's die; and
      // `shade`, `travel` and `mask` are the judge channels the module rests at. None of them draws
      // a pattern, so none of them can stack one on another.
      handles: {
        mix: { min: 0, max: 1, def: 0 , level: null },
        clock: { min: 0, max: 14, def: 0 , level: null },
        thickness: { min: 0, max: 1, def: 0.5,
                     unit: "how much veil one sheet carries at its thickest",
                     reads: "texture.scoreFromCutLines — how much of a work reads as grain rather "
                          + "than as line. A work that IS texture makes a thick air, because what "
                          + "the veil does to a picture is read it at a coarser scale of its own "
                          + "material and a work of straight architecture has little there to "
                          + "lose. It TRAVELS from the departing work's reading to the arriving "
                          + "one's, so the air itself changes over the crossing",
                     applied: { weightAt: [WEIGHT_MIN, WEIGHT_MAX],
                                floorUnderIt: "a sheet is nowhere absent, so both doors are exact "
                                            + "at every value of this handle including nothing" } , level: "TEXTURE" },
        bodies: { min: 0, max: 1, def: 0.4,
                  unit: "how many bodies of veil stand across the frame on the nearest sheet",
                  reads: "structure.grid.periodPx over the work's own frame side — the count of the "
                       + "work's own measured lattice across it — and structure.ownDevice.stepPx "
                       + "where no grid period was derived, read as a position on this handle's own "
                       + "range. The weather banks at the scale the work's own structure already "
                       + "stands at",
                  applied: { bodiesAt: [BODIES_MIN, BODIES_MAX] } , level: "TEXTURE" },
        depth: { min: 0, max: 1, def: 0.5,
                 unit: "how far apart in depth the four sheets stand",
                 reads: "structure.polar.tunnel — how strongly a work already reads as a corridor. "
                      + "A picture that already carries depth gets a deep stack and passes the "
                      + "sheets one at a time; one that reads flat gets them crowded into a single "
                      + "bank that parts once",
                 applied: { gapAt: [GAP_MIN, GAP_MAX],
                            slabIsDerived: SLAB_SHARE,
                            reachIsDerived: "1.5·gap + slab + " + DEPTH_MARGIN } , level: "SURFACE" },
        airAngle: { min: 0, max: 180, def: 90,
                    unit: "which way the wind carries the sheets",
                    reads: "structure.grid.angleDeg — the direction the work's own lattice runs — "
                         + "and structure.ownDevice.angleDeg where the device recovered one. The "
                         + "air moves along the work's own grain rather than across a direction "
                         + "nobody measured. It is the same recorded angle the parquet's own "
                         + "`lattice` handle reads, so one measurement serves both" , level: "SURFACE" },
        seed: { min: 0, max: SEED_SPAN, def: 0,
                unit: "where the banks of veil stand",
                reads: "the score's own die. It is the offset in the sheets' own hash, so two "
                     + "passes over one edge meet two different weathers and neither door moves" , level: null },
        mask: { min: 0, max: 1, def: 0,
                applied: { readAtADoor: { readOn: "the drawing buffer", reads: "the two thicknesses",
                                          measures: "how much veil stands in front of each work at "
                                                  + "the door, which is exactly nothing for the "
                                                  + "standing work and at least four floors for "
                                                  + "the other" } } , level: null },
      },
      neutrals: { a: 0, b: 1 },
      doors: { in: { handle: "mix", value: 0, work: "a" },
               out: { handle: "mix", value: 1, work: "b" } },
      // BOTH DOORS FRAME AT A CROP OF EXACTLY ONE. Nothing is displaced, so no headroom is bought
      // from either photograph and a landed door is the source cover-fitted and nothing else.
      framings: { "0": { coverCrop: 1 }, "1": { coverCrop: 1 } },
      drivers: ["progress", "cueProgress", "time", "velocity", "capability", "noise", "static",
                "curve", "spline", "map", "add", "multiply", "mix", "clamp", "hold", "segment",
                "ramp", "slew", "oscillate", "node"],
      // The construction moves no point of view. The two works change DEPTH, which is a fact about
      // what stands in front of them and not about where the eye is; the witness camera stays the
      // stage's (§6).
      camera: { needs: "none", authority: "stage" },
      // THE PICTURE'S OWN CHAIN OF SMALLER COPIES, asked for by §8's `gl.readsChain`. It is not an
      // optimisation here, it is the mechanism: the level a work is read at IS its depth in the
      // veil. Without the chain a coarser reading silently returns the sharpest copy and the frame
      // comes out flat, which is exactly the defect the host's own note on this flag names.
      gl: { preserveDrawingBuffer: false, readsChain: true },
      // WHAT THIS INSTRUMENT WRITES WHERE ITS OWN MATTER IS ABSENT (§7's coverage law, and the
      // per-instrument specification in docs/design/COVERAGE.md). It is absent nowhere: every point
      // of the frame carries one of the two photographs and the alpha is the constant 1. Under the
      // placement rule this instrument is lawful as the lowest cue of a stack and as a whole one-cue
      // score, which is the placement a ground takes.
      coverage: { writes: false,
                  how: "the work with less veil in front of it takes the point, so both branches "
                     + "of the choice are photograph and the alpha is the constant 1; at a door "
                     + "the standing work has nothing in front of it and the other has all four "
                     + "sheets, so the door is one whole work by construction" },
      // The neutral pose is the ENTRY DOOR — `mix` at 0, the value the `doors` block above names.
      neutralPose: { mix: 0, clock: 0, thickness: 0.5, bodies: 0.4, depth: 0.5, airAngle: 90,
                     seed: 0, mask: 0, reduced: false, cssWidth: 1000, cssHeight: 1000 },
      passes: [{
        program: "veil", vert: VERT, frag: FRAG, position: "aPos",
        uniforms: [
          { name: "uA", type: "sampler2D", source: "textureA" },
          { name: "uB", type: "sampler2D", source: "textureB" },
          { name: "uFitA", type: "vec4", source: "fitA" },
          { name: "uFitB", type: "vec4", source: "fitB" },
          { name: "uRes", type: "vec2", source: "resolution" },
          { name: "uDepth", type: "vec4", source: "frame:depth" },
          { name: "uStack", type: "vec4", source: "frame:stack" },
          { name: "uAir", type: "vec4", source: "frame:air" },
          { name: "uMask", type: "float", source: "handle:mask" },
          { name: "uSeamPts", type: "float", source: "frame:seamPts" },
        ],
      }],
      // The instrument allocates nothing of its own: it spends the two source-texture slots the host
      // already holds and the one programme the host builds from this manifest. The four sheets are
      // four evaluations of one noise function, not four textures, and there is no state between
      // frames — every number is a pure function of the dial, which is what lets a seeded score
      // repeat to the pixel and a scrub run backwards.
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
                   programs: 1, passes: 1, bytesEstimate: 2666759, variant: "lean" },
                   standard: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0,
                               programs: 1, passes: 1, bytesEstimate: 10666759,
                               variant: "standard" },
                   rich: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                           passes: 1, bytesEstimate: 42666759, variant: "rich" } },
      capabilities: ["webgl2"],
      decline: ["one work only", "a source that never decoded"],
      // AUTHORED HERE RATHER THAN PORTED. There is no lab module for a veil, so there is no path and
      // no commit to name, and saying so is the honest entry.
      provenance: { labPath: null,
                    authored: "engine/assets/pass-inst-veil.js, against charter shelf 14's «fog/veil "
                            + "layers, hiding and revealing; depth read as thickness»" },
      // HOW WELL THIS INSTRUMENT SUITS A PAIR (2026-08-18, his word of 09:51 and its sharpening at
      // 09:53). An instrument answers how well it suits a pair, never whether it takes one; the
      // arithmetic runs in the composer, and what stands here is the instrument's own statement of
      // WHAT IT READS. A fit of nothing is never a refusal — it ranks last and plays where nothing
      // ranks higher.
      // THE GRAIN READING IS DECLARED IN THE HOUSE THE FIT ACTUALLY READS IT FROM. Every record
      // carries this one number twice — raw as `texture.scoreFromCutLines` and digested as
      // `measures.texture` — and the composer's own `veil` fit reads the digest. Naming the raw
      // twin made the sentence unprovable rather than false, which is the worse of the two: a run
      // that varies the raw house sees the fit stand still and cannot tell a wrong wiring from a
      // second name. The rule the fleet now follows is in tests/test_pass_reads.py's own header —
      // a declaration names the house the code reads, and the twin is named only as the twin.
      //
      // AND THE CORRIDOR CAME OFF. `structure.polar.tunnel` stood third here until PLAN.md S-86
      // and the fit read no polar field whatever. It is a real reading of this instrument — the
      // `depth` handle declares it and answers to it — but it never ranked a pair, and the `how`
      // sentence below never claimed it did.
      suits: { reads: ["measures.texture", "texture.detailPx"],
               how: "a veil is only worth watching where a work has something to lose to it: the "
                  + "two works' own grain readings say how much material the coarsening can take "
                  + "away, and how far apart their detail scales stand says whether coming forward "
                  + "through the sheets is a change the eye can follow. Every photograph reads at "
                  + "some grain, so this instrument suits every pair somewhat and no pair "
                  + "absolutely" },
      readiness: "production-ready",
    };

    var live = false;
    return {
      name: "veil",
      manifest: manifest,
      values: values,
      fit: fit,
      feel: feelOf,
      // WHAT THIS INSTRUMENT'S `feel` PROMISES (Phase 7, item 3b): monotone, door to door — the
      // claim, not yet the fact. `feelOf` holds flat under FEEL_D0 and past 1 - FEEL_D0 and leaves
      // each dead band at the ramp's own nonzero speed at once, the same edge S-20 already closed
      // for `matter`/`beat`/`gears`/`gates`/`adrift`/`waterline`/`tilt`. Declared here so the roll
      // call reaches it and reports what it finds; repairing the edge is core logic and outside
      // this phase's write-set (curve declaration only for the fleet's remaining instruments).
      feelClass: "monotone",
      inFront: inFrontOf,
      prepare: function (o) {
        if (!o.sources) return { take: false, why: "the veil instrument needs both works" };
        if (!o.cue) return { take: false, why: "no cue names it" };
        return { take: true };
      },
      start: function () { live = true; },
      // The pose the shader draws. Every number in it comes from a handle a score can drive, and the
      // wind's own run reads the second the host hands down, so a seeded run repeats to the pixel.
      //
      // A DOOR THIS INSTRUMENT CANNOT KEEP WHOLE IS REFUSED RATHER THAN DRAWN. At either door it
      // reads the two thicknesses on the buffer the host is about to bind and, where the standing
      // work has any veil in front of it or the other work has none, hands the host the reason with
      // the readings in it instead of drawing a door that carries a weather the file does not. The
      // host recovers the transaction on that reason and the walk's own glide carries the visitor,
      // which is the product's own behaviour with no renderer.
      frame: function (st) {
        if (!live) return;
        var h = st.handles;
        var pose = {
          mix: h.mix, thickness: h.thickness, bodies: h.bodies, depth: h.depth,
          airAngle: h.airAngle, seed: h.seed, mask: h.mask,
          t: h.clock, reduced: st.reduced,
          cssWidth: st.viewport.w, cssHeight: st.viewport.h,
          // THE GRID THE SHADER WILL SAMPLE ON, carried into the pose so the door is read on the
          // buffer the host is about to bind as `uRes` rather than on the CSS frame around it.
          bufWidth: st.viewport.bufferW, bufHeight: st.viewport.bufferH,
          // THE ISOLINE'S OWN HAIRLINE, off the host's own `seams` reading (§8's `seams` block).
          // Only the host knows what every instrument declaring a hairline retouch is holding its
          // own crease to, so it answers once and this file carries the number rather than
          // choosing it.
          seam: st.seams,
        };
        // AT A DOOR THE INSTRUMENT SAYS WHAT IT APPLIED, and says it before it refuses. Nothing is
        // ever walked back here — no grid decides this instrument's doors — so the request and the
        // applied state are one and the same, and what the record carries is the state itself: the
        // two depths and the two thicknesses that decide the door.
        if (h.mix === 0 || h.mix === 1) {
          var v = values(pose);
          if (st.reportApplied) {
            st.reportApplied({
              door: h.mix === 0 ? "in" : "out",
              buffer: [pose.bufWidth, pose.bufHeight],
              reads: "the two thicknesses",
              request: v.veil ? [v.veil.inFront, v.veil.behind] : null,
              applied: v.veil ? [v.veil.inFront, v.veil.behind] : null,
              moved: 0, unit: "sheets of veil",
              standing: [v.zA, v.zB],
              thinnest: v.veil ? v.veil.clear : null,
              held: null, whyNo: v.doorWhyNo,
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
    instrument: veilInstrument(),
  });
})();
