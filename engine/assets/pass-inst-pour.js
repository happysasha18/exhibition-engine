/*!pass-inst-pour.js*/
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
// OWNERSHIP, AND WHERE THIS ONE CAME FROM. Every other instrument in this directory was carried
// over from a lab module. This one was not: `lab/effects/` holds no pour, and the charter's shelf 14
// asks for one — «granular pour (particles with an angle of repose; B condenses from the pour)».
// So the mathematics below is authored here rather than ported, and that is said out loud in three
// places: `provenance.labPath` is null, no response curve is carried (there is no module
// measurement behind one), and every constant that is not derived names the sentence it stands on.
//
// THE INSTRUMENT IS FINISHED AND THE WIRE IS NOT. An instrument plays only where the composer holds
// three things for it — a suitability reading, a register row per handle, and a fill branch. None of
// the three exists yet. Until the fill branch lands, every handle below would stand at its manifest
// rest for every pair alike, which is the sameness his 08:52 word names; the three blocks ready to
// apply are in `docs/design/ELEMENTS-WIRING.md` in this tree.
(function () {
  var join = window.__@@NS@@PassInstrument;
  if (typeof join !== "function") return;

  // THIS FILE'S OWN VERSION, and the one home of that fact. The build reads this literal out of the
  // source and writes it into the site's record beside the digest, so the version a file declares
  // and the version a host was told to load cannot drift apart without the build noticing.
  var INSTRUMENT_VERSION = "1.0.0";

  // ================================================================================================
  // THE POUR INSTRUMENT (§8) — charter shelf 14, the elements
  // ================================================================================================
  // WHAT THE VISITOR SEES. The departing photograph loses its grip a column at a time. A column
  // lets go, and everything in it falls straight down and out of the bottom of the frame, its top
  // edge breaking into grain as it goes. What it leaves behind is not an empty frame: the matter
  // that has fallen HEAPS, and the heap is the ARRIVING photograph. The heap grows from the floor
  // of the frame, one pile to a column, and the piles run together along their own angle of repose
  // — the steepest slope loose material will stand at — so the arriving work rises as a landscape
  // of slopes rather than as a rectangle. When every column has poured, the heap has buried the
  // frame and the arriving work stands whole.
  //
  // «B CONDENSES FROM THE POUR» IS THE HEAP, AND THAT IS THE WHOLE OF IT. The falling matter is the
  // departing work; the moment it lands it is the arriving one. There is no instant at which a
  // point carries a mixture of the two: a point is heap, or it is falling matter, or it is the gap
  // between them, and the gap is this instrument's own absence rather than a fade.
  //
  // ------------------------------------------------------------------------------------------------
  // THE FIVE THINGS THE CONSTRUCTION HAS TO ANSWER, AND HOW EACH IS ANSWERED
  // ------------------------------------------------------------------------------------------------
  //   · WHEN A COLUMN LETS GO. Each column's own release stands at `hash(column) · stagger` of the
  //     dial, so at a stagger of nothing every column pours at once and at a wide stagger they pour
  //     one after another over most of the passage. A column's own travel is then the rest of the
  //     dial, `(d − release) / (1 − stagger)`, which is nothing at the entry door for every column
  //     and whole at the exit door for every column. Both doors are therefore exact for every
  //     stagger a score can name, and no reading is needed to know it.
  //   · HOW FAR IT FALLS. Exactly the heap's own ceiling, which is over one frame height, so at the
  //     exit door every point's source stands above the picture and the departing work has left the
  //     frame rather than faded out of it. The fall accelerates — the distance is the square of the
  //     column's own travel — which is the one piece of physics this file spends, and it is a shape
  //     rather than a number: it is nothing at nothing and whole at whole, so it moves neither door.
  //   · WHERE THE HEAP'S SURFACE STANDS. A column that has poured a share of itself has piled that
  //     share, so a pile's height is the heap's ceiling times its own column's travel. A pile alone
  //     would be a rectangle; the ANGLE OF REPOSE is what makes it a heap, and it enters as the one
  //     rule loose material obeys: the surface at a point is the highest any pile can reach there
  //     without standing steeper than the repose slope, `max over piles of (height − distance ·
  //     slope)`. That is a cone from every pile and the surface is their upper envelope.
  //   · WHY THE EXIT DOOR IS EXACT. At the exit every pile stands at the ceiling, so the surface at
  //     a point is the ceiling less the distance to the nearest pile's own centre times the slope.
  //     The nearest centre is never further than half a column, so the ceiling is DERIVED rather
  //     than typed: `1 + (slope / 2·columns) + margin` puts the surface over the whole frame at
  //     every point, at every column count and at every repose angle a score can name.
  //   · WHY IT READS AS GRAIN AND NOT AS BLOCKS. Two boundaries carry the material's own noise —
  //     the falling matter's top edge and the heap's own surface — and each carries it at the
  //     grain's own cell count, so both break up at the scale of the material rather than at the
  //     scale of the column. Both noises are held to nothing at both doors, one by the column's own
  //     travel and one by a window that closes at each end, so neither can reach a door.
  //
  // ------------------------------------------------------------------------------------------------
  // THE BANS, AND THE ONE THIS INSTRUMENT CAME NEAREST TO
  // ------------------------------------------------------------------------------------------------
  // NO DRAWN SEAM LINE BETWEEN PARTICLES, and this is the ban the construction stood closest to.
  // A heap wants a contact line: the eye reads a pile by the dark crease where it meets what it is
  // heaped against, and the cheapest way to draw one is a stroke along the surface. There is none
  // here. The heap's light is a BODY shading and not an edge: the surface's own lean — which side
  // of a pile's cone a point stands on, and how steep that cone is — writes the whole flank lighter
  // or darker, so the light is strongest in the middle of a slope and exactly nothing where the
  // heap is flat. Nothing is drawn AT the boundary at all; the boundary is where one work stops and
  // the other starts, one point of the drawing buffer wide, read off the surface's own height.
  //
  // NO ALPHA CROSSFADE AS THE ARRIVAL. The arriving work is never mixed with the departing one. A
  // point is inside the heap or it is not, and the crossover is one point of the buffer.
  // NO PATTERN LAID OVER A WORK THAT CARRIES ITS OWN. The only field this instrument writes over a
  // photograph is the grain that breaks its own falling edge, and its cell count is read off the
  // work's own measured repeat, so the material a work comes apart into is the material it is made
  // of.
  // NO ROTATIONAL GESTURE THAT RETRACES ITS OWN PATH. Nothing here turns; everything falls, once,
  // in one direction.
  // NOTHING THAT READS AS A STOCK EFFECT. A dissolve into particles is the stock one, and it is a
  // dissolve because the particles go nowhere: they thin out where they stand. Here the matter has
  // somewhere to go, it obeys one law on the way, and what it builds when it lands is the second
  // photograph.
  function pourInstrument() {
    var VERT = [
      "attribute vec2 aPos;",
      "varying vec2 vUv;",
      "void main(){ vUv = vec2(aPos.x * 0.5 + 0.5, 0.5 - aPos.y * 0.5); gl_Position = vec4(aPos, 0.0, 1.0); }",
    ].join("\n");

    // ----------------------------------------------------------------------------------------------
    // THE SHADER
    // ----------------------------------------------------------------------------------------------
    // The frame is measured from the BOTTOM here — `q.y` runs up from the floor the heap grows off —
    // because every sentence above is about height, and a picture whose rows run down would have to
    // turn each of them over twice. The one place the lookup happens turns it back.
    //
    // THREE CARRIERS HOLD EVERYTHING THAT MOVES, because the host binds four uniform types and a
    // shorter list is a shorter fence.
    var FRAG = [
      "precision highp float;",
      "varying vec2 vUv;",
      "uniform sampler2D uA;",          // the work that pours
      "uniform sampler2D uB;",          // the work the heap is made of
      "uniform vec4 uFitA;",
      "uniform vec4 uFitB;",
      "uniform vec2 uRes;",
      // dial: the hand with its dead bands taken off.
      // columns: how many columns the picture pours in, a whole number.
      // stagger: how much of the dial the columns' own releases are spread over.
      // phase: the die's own offset into the column hash.
      "uniform vec4 uPour;",
      // slope: the repose slope, the tangent of the angle loose material stands at.
      // ceiling: how high a pile stands when its column has wholly poured — DERIVED, see `topOf`.
      // grain: the material's own cell count across the frame.
      // drift: how far the grain has been carried, so a pour is not frozen between frames.
      "uniform vec4 uHeap;",
      // shade: the judge channel for the heap's own light.
      // window: 4d(1−d), exactly nothing at both doors, which is what holds the grain and the light
      // off the two landings.
      "uniform vec2 uLight;",
      "uniform float uMask;",
      "uniform float uPresence;",  // the entry-door contract's reserved dry
      // HOW FAR THE FALLING MATTER SCATTERS SIDEWAYS INSIDE ITS OWN COLUMN, in column widths, and
      // how far the grain breaks its own top edge, in frame heights. Both are shapes of the
      // material rather than free numbers: the first is under one column, so matter never crosses
      // into a neighbour's stream; the second is under a twentieth of the frame, so the edge reads
      // as crumb and never as a second cut.
      "const float SCATTER = 0.80;",
      "const float CRUMB = 0.055;",
      // How much of a flank the heap's own light may write, and how much of a pile the grain may
      // move. Neither passes a third, so the material is never lost to the light or to the noise.
      "const float LIGHT = 0.30;",
      "const float ROUGH = 0.32;",
      "float h11(float i){ return fract(sin(i * 127.1 + uPour.w) * 43758.5453); }",
      // The material's own grain: plain value noise on smoothstep coordinates, one number a point.
      // No gradient is taken of it — the two places it is spent are boundaries whose own crossover
      // is read off the height, not off the noise.
      "float vnoise(vec2 p){",
      "  vec2 i = floor(p), f = fract(p);",
      "  float a = h11(i.x + i.y * 57.0), b = h11(i.x + 1.0 + i.y * 57.0);",
      "  float c = h11(i.x + (i.y + 1.0) * 57.0), d = h11(i.x + 1.0 + (i.y + 1.0) * 57.0);",
      "  vec2 u = f * f * (3.0 - 2.0 * f);",
      "  return a + (b - a) * u.x + (c - a) * u.y + (a - b - c + d) * u.x * u.y;",
      "}",
      "vec2 into(vec2 p, vec4 f){",
      "  return clamp((p - 0.5) * f.xy + 0.5 + f.zw, 0.0008, 0.9992);",
      "}",
      // HOW FAR ONE COLUMN HAS POURED. Nothing at the entry door for every column, whole at the exit
      // door for every column, and monotone in the hand in between — which is the whole of why this
      // instrument needs no reading to know its own doors are exact.
      "float pouredOf(float i){",
      "  float rest = max(1.0 - uPour.z, 1e-4);",
      "  return clamp((uPour.x - h11(i) * uPour.z) / rest, 0.0, 1.0);",
      "}",
      "void main(){",
      "  vec2 uv = vUv;",
      "  vec2 q = vec2(uv.x, 1.0 - uv.y);",
      "  float n = max(uPour.y, 1.0);",
      "  float slope = uHeap.x;",
      "  float top = uHeap.y;",
      "  float win = uLight.y;",
      "  float ci = floor(q.x * n);",
      // THE HEAP'S OWN SURFACE — the upper envelope of the piles' cones. The sweep is the point's
      // own column and eight to each side of it, and the truncation is stated rather than hidden:
      // a pile nine columns away can only win here where it stands over its nearer neighbours by
      // more than eight column widths of slope, which mid-passage understates the surface by a hair
      // nobody watching can name. IT CANNOT REACH A DOOR: the point's own column is always in the
      // sweep, and at the exit door that one cone alone puts the surface over the whole frame.
      "  float H = 0.0, lean = 0.0;",
      "  for (int k = -8; k <= 8; k++) {",
      "    float j = ci + float(k);",
      "    if (j < 0.0 || j > n - 1.0) continue;",
      "    float cx = (j + 0.5) / n;",
      "    float v = top * pouredOf(j) - abs(q.x - cx) * slope;",
      "    if (v > H) { H = v; lean = q.x < cx ? -1.0 : 1.0; }",
      "  }",
      "  H = max(H, 0.0);",
      // THE MATERIAL'S OWN ROUGHNESS ON THAT SURFACE, and it is written as a SHARE of the height
      // rather than added to it: a heap of nothing stays a heap of nothing whatever the noise says,
      // which is one of the two independent reasons the entry door cannot carry it. The other is
      // the window, which is exactly zero at both ends of the hand.
      "  float g = vnoise(vec2(q.x, q.y + uHeap.w) * uHeap.z);",
      "  float Hd = H * (1.0 + ROUGH * (g - 0.5) * win);",
      // WHICH WORK STANDS AT THIS POINT, ON THE HEAP'S SIDE. One point of the drawing buffer wide,
      // read off the surface's own height, so the boundary carries no fade of its own and no step.
      "  float covHeap = clamp(0.5 + (Hd - q.y) * uRes.y, 0.0, 1.0);",
      // THE FALLING MATTER. Its column's own travel says how far it has dropped, the square of that
      // travel says the fall accelerates, and the grain breaks its top edge and scatters it a
      // fraction of a column sideways — both scaled by the same travel, so both are exactly nothing
      // at the entry door.
      "  float u = pouredOf(ci);",
      "  float s = u * u * top;",
      "  float gA = vnoise(vec2(q.x + 3.7, q.y * 1.7 - uHeap.w * 0.6) * uHeap.z) - 0.5;",
      "  float srcY = q.y + s + CRUMB * gA * u;",
      "  float sx = SCATTER * gA * u / n;",
      "  float covFall = clamp(0.5 + (1.0 - srcY) * uRes.y, 0.0, 1.0);",
      "  vec3 colA = texture2D(uA, into(vec2(q.x + sx, 1.0 - srcY), uFitA)).rgb;",
      "  vec3 colB = texture2D(uB, into(uv, uFitB)).rgb;",
      // THE HEAP'S OWN LIGHT. A flank leaning one way takes the light and the other loses it, and
      // the strength of it is the flank's own steepness — so a shallow heap is barely modelled and
      // a steep one reads as a slope. It is written over the heap's body and NOWHERE NEAR its
      // boundary, which is the whole reason there is no drawn crease here.
      "  float face = lean * slope / sqrt(1.0 + slope * slope);",
      "  colB *= 1.0 + LIGHT * face * uLight.x * win;",
      "  vec3 col = mix(colA, colB, covHeap);",
      // THE JUDGES' OWN FRAME: which work stands at this point, whether the departing work still
      // has matter over it, and how high the heap has come. It is read as colour and carries no
      // coverage of its own, because what it is for is to be measured rather than looked at.
      "  vec3 judge = vec3(covHeap, covFall, clamp(Hd, 0.0, 1.0));",
      "  col = mix(col, judge, uMask);",
      // THE COVERAGE LAW (§7). This instrument's own matter is the heap and the matter still in the
      // air. Where a column has drained past a point and the heap has not yet reached it, this
      // instrument carries nothing, hides nothing, and the cue beneath is seen. At the entry door
      // no column has moved, so the falling branch covers every point; at the exit door the heap
      // stands over the whole frame. Each door is therefore one whole work, opaque throughout.
      "  gl_FragColor = vec4(col, mix(max(covHeap, covFall), 1.0, uMask) * uPresence);",
      "}",
    ].join("\n");

    function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }

    /* HOW STEEP LOOSE MATERIAL STANDS. The two ends of the `repose` handle in the slope's own units,
       which is the tangent of the angle: 0.36 is about twenty degrees and 3.00 is about seventy-
       two. Real materials sit between them — dry sand near thirty-four degrees, wet sand far
       steeper — and the pair of ends is this file's own decision, named as one: what it buys is that
       a work of coarse material heaps in low mounds and a work of fine material heaps in cones. */
    var SLOPE_MIN = 0.36, SLOPE_MAX = 3.00;

    /* HOW COARSE THE MATERIAL IS, in cells across the frame, at either end of the `grain` handle.
       Four cells is a material whose crumb is a quarter of the frame — a rubble — and 220 is one
       whose crumb is under a point of the buffer on the frames this engine draws, which is where a
       finer grain stops being visible at all. Both ends are named in this file's own report. */
    var GRAIN_MIN = 4, GRAIN_MAX = 220;

    /* HOW MANY COLUMNS THE PICTURE POURS IN. Below four the picture falls as slabs and the pour
       stops being a pour; past sixty-four a column is under six points of a 390-point frame, so the
       stream is thinner than the grain inside it and the two readings fight. */
    var COLS_MIN = 4, COLS_MAX = 64;

    /* HOW FAR PAST ONE WHOLE FRAME HEIGHT THE HEAP'S OWN CEILING STANDS. The ceiling itself is
       derived — see `topOf` — and this is the margin it is derived WITH: a tenth of the frame, the
       same share the material and the water instruments both give their own travelling thresholds.
       One law, one number, read in three instruments' own units. */
    var MARGIN = 0.10;

    /* THE DEAD BANDS AT EITHER END OF THE HAND, the number every instrument of this engine uses.
       Over the first and last five hundredths of the dial nothing has poured and nothing has
       heaped: the hand is spent there and the standing work is the picture its source carries, to
       the point. That is what makes a door a door and not a checkpoint. */
    var FEEL_D0 = 0.05;

    /* NO RESPONSE CURVE IS CARRIED, and that is a fact about this instrument rather than an
       omission. Every other instrument here carries one because a lab module measured the felt
       change of its own hand and fitted a curve to it; there is no pour module and so no such
       measurement, and fitting a curve to a picture nobody has watched would be a number nobody
       read reaching the picture, which is exactly the class his 19:21 word strikes. What the hand
       gets instead is the dead bands and nothing else, and the shape a viewer actually feels is the
       fall's own acceleration, which is physics and not taste. */
    function feelOf(u) {
      return clamp((clamp(u, 0, 1) - FEEL_D0) / (1 - 2 * FEEL_D0), 0, 1);
    }

    /* THE SPAN THE SCORE'S DIE ARRIVES ON, and what this instrument spends it on: WHICH COLUMN
       LETS GO FIRST. The die is a phase into the column hash, so two passes over one edge pour in
       two different orders while every other number of the frame stays where the score put it —
       which is charter shelf 13's rubato read on this instrument's own axis. It moves neither door:
       whatever the order, at the entry door no column has released and at the exit door every
       column has. */
    var SEED_SPAN = 8;

    /* HOW HIGH A PILE STANDS WHEN ITS COLUMN HAS WHOLLY POURED, DERIVED AND NOT TYPED. At the exit
       door every pile stands at this height, so the surface at a point is this height less the
       distance to the nearest pile's own centre times the repose slope. The nearest centre is never
       further than half a column, `0.5 / columns`, so a ceiling of `1 + slope/(2·columns) + margin`
       leaves the surface over every point of a frame one high — at every column count and at every
       repose angle a score can name. This is the sentence the exit door stands on and it is exact
       as an inequality rather than as a tolerance. */
    function topOf(slope, cols) {
      return 1 + slope / (2 * Math.max(cols, 1)) + MARGIN;
    }

    // Cover-fit a work into the frame and nothing beyond it. Nothing here is dragged in from outside
    // the picture — matter that falls off the bottom is matter that has left, not a sample to fetch,
    // and the sideways scatter is under one column and clamped — so BOTH DOORS FRAME AT A CROP OF
    // EXACTLY ONE and no headroom is bought from either photograph.
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
    // and every number in the pose comes from a handle a score drives. The only place a second is
    // read is the grain's own drift, which reads the `clock` handle rather than a wall clock, so a
    // seeded score repeats to the pixel.
    //
    // The repose is a parameter rather than read straight off the pose, because the hold in `values`
    // below asks this same function for the same pose at a steeper angle. Nothing else about it
    // moved.
    function posed(st, repose) {
      var d = feelOf(st.mix);
      var cols = Math.max(COLS_MIN, Math.min(COLS_MAX, Math.round(Number(st.columns) || COLS_MIN)));
      var slope = SLOPE_MIN + (SLOPE_MAX - SLOPE_MIN) * clamp(repose, 0, 1);
      var stagger = clamp(st.stagger, 0, 0.9);
      var grain = GRAIN_MIN + (GRAIN_MAX - GRAIN_MIN) * clamp(st.grain, 0, 1);
      var drift = (st.reduced ? 0 : (Number(st.t) || 0)) * 0.07;
      var phase = (clamp(st.seed, 0, SEED_SPAN) / SEED_SPAN) * 2 * Math.PI;
      // THE ONE WINDOW BOTH THE GRAIN AND THE LIGHT RIDE. Exactly nothing at both ends of the hand
      // and whole across the middle, so a door is the file itself whatever numbers a score gives
      // the material — the same construction the parting-by-light instrument holds its two
      // accompanying voices with.
      var win = 4 * d * (1 - d);
      return {
        pour: [d, cols, stagger, phase],
        heap: [slope, topOf(slope, cols), grain, drift],
        light: [clamp(st.shade, 0, 1), win],
        // the same numbers by name, for the reading below and for the diagnostic surface
        dialAt: d, cols: cols, slope: slope, repose: clamp(repose, 0, 1), stagger: stagger,
        grain: grain, drift: drift, phase: phase, window: win, ceiling: topOf(slope, cols),
        shade: clamp(st.shade, 0, 1), margin: MARGIN, coverCrop: 1,
        mask: clamp(typeof st.mask === "number" ? st.mask : 0, 0, 1),
        grid: gridOf(st),
      };
    }

    // ---- THE DOOR THE INSTRUMENT READS FOR ITSELF --------------------------------------------------
    // His 18:00 architecture decision, carried in the U27 brief: the instrument reads its doors at
    // runtime on the actual buffer, and the report it hands back is the runtime truth; what the
    // manifest declares is only the claim. This is that law read in THIS instrument's own unit,
    // which is the HEAP — its surface over the frame, and whether the falling matter still stands
    // over a point.
    //
    // WHAT A DOOR ASKS OF A POUR, and where the buffer enters it. Both boundaries this instrument
    // draws are read against the buffer's own row height: the heap's surface crosses over inside
    // one point of the buffer, and so does the falling matter's top edge. So a door is whole
    // exactly while the surface stands a half-point CLEAR of the frame's own top row at the exit,
    // and the falling matter's source stands a half-point clear of the picture's own top at the
    // entry. Both are claims about a GRID, so both are WALKED at the buffer's own sample points
    // rather than asserted.
    //
    // WHAT THE READING FINDS, SAID PLAINLY. It refuses on no pose this file as written can produce:
    // the ceiling is derived from the very inequality the exit door needs, and the entry door has
    // nothing moving at all. The reading is still taken, because a door held by a number nobody
    // read is a claim rather than a landing — it publishes how much frame the tightest point had TO
    // SPARE, so a change to the ceiling, to the sweep or to the dead bands shows the margin closing
    // long before anything crosses. The suite's red-on-bug rows type the ceiling flat and take the
    // reading out in turn, and each makes exactly this refusal fire.
    //
    // AND THERE IS SOMETHING HERE TO HOLD. The fault has a direction that closes it: the surface
    // rises with the repose slope — the ceiling gains `slope / 2·columns` while the point's own cone
    // loses at most the same — so a door a score's repose cannot keep whole is answered by standing
    // the heap STEEPER until it is, and the request stays on the record beside what was applied.
    var DOOR_HOLD = 0.25;      // how far the hold may walk the repose handle, in the handle's own units
    var DOOR_STEP = 0.05;      // and in what steps
    var DOOR_GRID = 32;        // how many steps the reading walks across the frame

    // ONE COLUMN'S OWN TRAVEL, written once more in the script so the reading walks the very pour
    // the shader draws rather than a description of it. The hash is the shader's own.
    function hash11(i, phase) {
      var x = Math.sin(i * 127.1 + phase) * 43758.5453;
      return x - Math.floor(x);
    }
    function pouredOf(v, i) {
      return clamp((v.dialAt - hash11(i, v.phase) * v.stagger) / Math.max(1 - v.stagger, 1e-4), 0, 1);
    }
    // THE HEAP'S SURFACE AT ONE POINT ACROSS THE FRAME — the shader's own envelope, with the same
    // sweep, so the reading and the picture cannot disagree.
    function heapAt(v, qx) {
      var ci = Math.floor(qx * v.cols), H = 0, k, j, cx, h;
      for (k = -8; k <= 8; k++) {
        j = ci + k;
        if (j < 0 || j > v.cols - 1) continue;
        cx = (j + 0.5) / v.cols;
        h = v.ceiling * pouredOf(v, j) - Math.abs(qx - cx) * v.slope;
        if (h > H) H = h;
      }
      return H;
    }

    // THE DOOR, WALKED ON THE BUFFER THE SHADER WILL SAMPLE ON. `want` is 1 at the entry door, where
    // every point owes its picture to the falling branch and the heap must be nowhere, and 0 at the
    // exit, where the heap must be over every point. What comes back is how many points were
    // walked, how many carried any share of the wrong work, and how much frame the tightest of them
    // had to spare, in points of the buffer.
    function pourReadOf(v, W, H, want) {
      var walked = 0, wrong = 0, spare = 1e9, poured = 0, i, qx, surf, room, cov, u;
      for (i = 0; i <= DOOR_GRID; i++) {
        qx = clamp(i / DOOR_GRID, 0.5 / W, 1 - 0.5 / W);
        surf = heapAt(v, qx);
        u = pouredOf(v, Math.floor(qx * v.cols));
        if (u > poured) poured = u;
        if (want) {
          // THE ENTRY DOOR asks two things at once and both are walked. The heap must stand below
          // the frame's own bottom sample row, so no point carries the arriving work; and no column
          // may have poured at all, so the departing work stands exactly where its file puts it.
          room = (0.5 / H - surf) * H;
          cov = clamp(0.5 + (surf - 0.5 / H) * H, 0, 1);
          if (cov > 0 || u > 0) wrong++;
        } else {
          // THE EXIT DOOR asks one: the surface must stand over the frame's own topmost sample row,
          // so every point carries the arriving work. The departing work's own travel is whole
          // wherever that holds, since a column that has wholly poured has its source above the
          // picture by the same ceiling.
          room = (surf - (1 - 0.5 / H)) * H;
          cov = clamp(0.5 + (surf - (1 - 0.5 / H)) * H, 0, 1);
          if (cov < 1) wrong++;
        }
        if (room < spare) spare = room;
        walked++;
      }
      return { walked: walked, wrong: wrong, spareRows: spare, poured: poured, want: want,
               repose: v.repose, ceiling: v.ceiling, cols: v.cols, slope: v.slope };
    }

    function doorReadOf(v, st) {
      var want = st.mix === 0 ? 1 : (st.mix === 1 ? 0 : -1);
      if (want < 0) return null;
      var g = v.grid;
      if (!g.given) return null;
      var read = pourReadOf(v, g.w, g.h, want);
      read.grid = g;
      return read;
    }

    // THE REFUSAL, worded the way the host's own manifest refusals read: what is wrong, in this
    // instrument's own measured numbers, on the grid it was measured on.
    function doorWhyNoOf(read) {
      if (!read || !read.wrong) return null;
      var g = read.grid, where = " of a " + g.w + " x " + g.h + (g.drawn ? " buffer" : " frame");
      if (read.want) {
        return "the entry door leaks: the heap already stands over " + read.wrong + " of the "
             + read.walked + " points this reading walked" + where
             + ", or a column has already poured — the widest of them by "
             + read.poured.toFixed(4) + " of its own travel — where the entry door's own law asks "
             + "for the departing work at every point";
      }
      return "the exit door leaks: at a repose of " + read.repose.toFixed(3) + " over "
           + read.cols + " columns the heap's own ceiling of " + read.ceiling.toFixed(3)
           + " leaves its surface short of the frame's top row on " + read.wrong + " of the "
           + read.walked + " points this reading walked" + where + " — the tightest of them by "
           + Math.abs(read.spareRows).toFixed(3) + " of a row — so the departing work's own gap "
           + "takes the points of the frame furthest from a pile, where the exit door's own law "
           + "asks for the arriving work at every point";
    }

    // THE NUMBERS OF ONE FRAME, WITH ITS DOOR READ ON THE BUFFER BEING DRAWN. Away from a door this
    // is `posed` and nothing more: the reading is taken nowhere else and no angle moves. At a door
    // whose repose leaves the heap short on the buffer being drawn, the instrument stands the heap
    // STEEPER — the only direction that closes it — and answers with the first pose whose door is
    // whole. What the score asked for and what was applied are both on the record.
    function values(st) {
      var asked = clamp(typeof st.repose === "number" ? st.repose : 0.45, 0, 1);
      var v = posed(st, asked);
      v.reposeRequest = asked;
      v.reposeMoved = 0;
      v.doorHeld = null;
      var read = doorReadOf(v, st);
      var no = doorWhyNoOf(read);
      v.doorGrid = read ? read.grid : null;
      v.pileRead = read ? { walked: read.walked, wrong: read.wrong, spareRows: read.spareRows,
                       poured: read.poured } : null;
      if (!no) { v.doorWhyNo = null; return v; }
      for (var step = DOOR_STEP; step <= DOOR_HOLD + 1e-9; step += DOOR_STEP) {
        var tryR = asked + step;
        if (tryR > 1) break;
        var w = posed(st, tryR);
        var wRead = doorReadOf(w, st);
        if (doorWhyNoOf(wRead)) continue;
        w.reposeRequest = asked;
        w.reposeMoved = tryR - asked;
        w.doorHeld = no;
        w.doorWhyNo = null;
        w.doorGrid = wRead.grid;
        w.pileRead = { walked: wRead.walked, wrong: wRead.wrong, spareRows: wRead.spareRows,
                   poured: wRead.poured };
        return w;
      }
      v.doorWhyNo = no + ", and standing the heap steeper by the " + DOOR_HOLD
                  + " of this handle's own travel the hold reaches does not close it";
      return v;
    }

    var manifest = {
      id: "pour", api: 1, arity: 2,
      // The departing work comes apart into a material, the middle is a frame carrying matter in the
      // air with a gap behind it, and the arriving work gathers out of what has landed.
      roles: ["disassembly", "mystery", "assembly"],
      // READ OFF THIS INSTRUMENT'S OWN CONSTRUCTION, and said to be read rather than published:
      // there is no lab module for a pour, so no vocabulary table carries a row for it.
      //   · SURFACE — one field runs over the whole frame, the heap's own height, and its value at a
      //     point decides which of the two works stands there. That is the level `pass-inst-adrift.js`
      //     and `pass-inst-liquid.js` both place exactly that act at.
      //   · CELL — the frame is cut into columns and each column lets go on its own release and
      //     falls at its own rate, which is a named part of the frame moving as a whole.
      // TEXTURE IS NOT CLAIMED, and the reason is the same one the drifting instrument gives: the
      // grain here shapes the BOUNDARY of the matter — where the falling edge breaks and how rough
      // the heap's surface stands — and never the picture's own material, which is untouched inside
      // both works.
      levels: ["SURFACE", "CELL"],
      // WHAT THIS INSTRUMENT CUTS ON. A column is a band of the frame taken along one axis, which is
      // the STRIP kind — the same family the woven instrument's ribbons and the beat's own bands
      // are cut from, and the kind `KIND_OF_MEASURE` gives the recorded `banding` measure. The
      // declaration lives here, in the instrument's own file, because the site's settings build
      // prefers a manifest's own `cuts` to any table it keeps and names an instrument that declares
      // none as UNPLACED — landed and uncastable.
      cuts: ["strip"],
      // WHERE THIS INSTRUMENT HAS A SEAM (§8's `seams` block, pass-layer.js). None is declared,
      // because the file's own bans section already argues the strip cut's boundary out of existence
      // rather than softening it: "NO DRAWN SEAM LINE BETWEEN PARTICLES... A heap wants a contact
      // line: the eye reads a pile by the dark crease where it meets what it is heaped against... There
      // is none here." Two neighbouring columns never meet at a drawn edge because the heap's own
      // surface is the UPPER ENVELOPE of every pile's cone, `H = max over piles of (height − distance ·
      // slope)` — a max of continuous cones is itself continuous, so where one column's pile gives way
      // to its neighbour's the surface already agrees on the height at every point between them and
      // there is no gap or step for a smoothstep to close. The one width the shader does carry, the
      // heap's own top edge against the gap above it (`covHeap`, one point of `uRes.y` wide), softens a
      // boundary between a WORK and the frame's own absence — the coverage law, not this cut — and the
      // file names it as "one point of the drawing buffer wide, read off the surface's own height", a
      // hairline it already draws rather than a seam this cut still owes.
      seams: [],
      params: { columns: [COLS_MIN, COLS_MAX], repose: [0, 1], stagger: [0, 0.9], grain: [0, 1] },
      // EVERY handle a score can drive (§4.4b). `mix` is the dial and `clock` is the second the host
      // hands down — the one place a second reaches this instrument at all, the grain's own drift.
      // `seed` is the score's die, `shade` is the judge channel for the heap's own light, and `mask`
      // is the judges' frame.
      //
      // EVERY HANDLE THAT SHAPES THE PICTURE NAMES THE MEASUREMENT OF A PHOTOGRAPH IT READS, which
      // is his 19:13 word lifted to the class at 19:21. What stands here is the sentence; the
      // arithmetic that turns a reading into a value runs in the composer, which is the one place
      // holding both records.
      //
      // `travel` IS ABSENT, and the absence is a fact about this instrument rather than an
      // oversight — the same reason the parting-by-light instrument gives for its own. How far the
      // matter is carried is exactly the heap's own ceiling, which is what makes the exit door
      // exact; a handle scaling it below that would leave the departing work standing in the frame
      // at `mix` 1 and break the door this instrument's own coverage line claims.
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
        columns: { min: COLS_MIN, max: COLS_MAX, def: 16,
                   unit: "how many columns the picture pours in",
                   reads: "structure.grid.periodPx over the work's own frame side — the count of "
                        + "the work's own measured lattice across it — and structure.ownDevice."
                        + "stepPx where no grid period was derived. The picture lets go along the "
                        + "repeat it was made on, so the streams stand where the work's own "
                        + "structure already stands",
                   applied: { roundedToWholeColumns: true } , level: "CELL" },
        repose: { min: 0, max: 1, def: 0.45,
                  unit: "the angle loose material stands at, as its own slope",
                  reads: "texture.detailPx of the ARRIVING work over its own frame side, read as a "
                       + "position on this handle's own range: the heap is made of the arriving "
                       + "work, and a fine material heaps at a steeper angle than a coarse one",
                  applied: { slopeAt: [SLOPE_MIN, SLOPE_MAX],
                             heldWholeAtADoor: { travel: DOOR_HOLD, readOn: "the drawing buffer",
                                                 reads: "reposeRequest",
                                                 measures: "the heap's own surface against the "
                                                         + "frame's topmost sample row" } } , level: "SURFACE" },
        stagger: { min: 0, max: 0.9, def: 0.5,
                   unit: "how much of the dial the columns' own releases are spread over",
                   reads: "structure.regions.score of the DEPARTING work — how much of the "
                        + "difference between its own columns its region line explains. A work that "
                        + "falls plainly into regions lets go region by region; one that reads as "
                        + "a single mass lets go all at once" , level: "CELL" },
        grain: { min: 0, max: 1, def: 0.4,
                 unit: "how coarse the material is",
                 reads: "texture.spectralPeriodPx of the DEPARTING work over its own frame side, "
                      + "read as a position on this handle's own range — the work's own strongest "
                      + "repeat, said as cells across the frame, which is the same unit the "
                      + "material instrument's coarse grain is published in",
                 applied: { cellsAt: [GRAIN_MIN, GRAIN_MAX] } , level: "SURFACE" },
        seed: { min: 0, max: SEED_SPAN, def: 0,
                unit: "which column lets go first",
                reads: "the score's own die. It is a phase into the column hash, so two passes over "
                     + "one edge pour in two different orders and neither door moves" , level: null },
        shade: { min: 0, max: 1, def: 1,
                 unit: "the heap's own light — how strongly a flank leaning toward the light is "
                     + "written lighter and one leaning away darker",
                 applied: { restsAt: "both doors, where the window is exactly nothing" } , level: null },
        mask: { min: 0, max: 1, def: 0,
                applied: { readAtADoor: { readOn: "the drawing buffer", reads: "the heap",
                                          measures: "the heap's own surface and the falling "
                                                  + "matter's own top edge at the buffer's own "
                                                  + "sample points",
                                          held: DOOR_HOLD } } , level: null },
        // THE RESERVED DRY OF THE ENTRY-DOOR CONTRACT (docs/design/ENTRY-DOOR.md). One name across
        // the whole fleet, declared the same way in every manifest, so the host and the composer
        // learn it once instead of nine times. It says WHETHER THIS VOICE IS IN THE FRAME AT ALL:
        // at zero the instrument draws nothing anywhere and what stands beneath it shows whole; at
        // one it draws exactly as it always did, which is where it rests, so a plan that says
        // nothing about it gets the picture this instrument has always drawn.
        //
        // IT IS NOT THE BANNED OPACITY HANDLE RETURNING, and the difference is the whole point. An
        // opacity handle fades one whole layer against another — the crossfade the charter's own
        // ladder removed the tempting tool for. This says whether a voice is present, and it is
        // ZERO AT BOTH DOORS of a voice standing over another: the voice joins a running picture
        // without replacing it and stands down the same way. Nothing is ever faded against anything.
        presence: { min: 0, max: 1, def: 1, level: null,
                    unit: "whether this voice is in the frame at all" },
      },
      neutrals: { a: 0, b: 1 },
      doors: { in: { handle: "mix", value: 0, work: "a" },
               out: { handle: "mix", value: 1, work: "b" } },
      // BOTH DOORS FRAME AT A CROP OF EXACTLY ONE. Nothing is dragged in from outside either
      // picture: the fall is a translation and the sideways scatter is under one column and clamped,
      // so no headroom is bought from either photograph and a landed door is the source cover-fitted
      // and nothing else.
      framings: { "0": { coverCrop: 1 }, "1": { coverCrop: 1 } },
      drivers: ["progress", "cueProgress", "time", "velocity", "capability", "noise", "static",
                "curve", "spline", "map", "add", "multiply", "mix", "clamp", "hold", "segment",
                "ramp", "slew", "oscillate", "node"],
      // The construction moves no point of view: it decides which work owns each point of the frame
      // and translates the departing work's columns inside it, so the witness camera stays the
      // stage's (§6).
      camera: { needs: "none", authority: "stage" },
      gl: { preserveDrawingBuffer: false },
      // WHAT THIS INSTRUMENT WRITES WHERE ITS OWN MATTER IS ABSENT (§7's coverage law, and the
      // per-instrument specification in docs/design/COVERAGE.md). Its absence is the gap the pour
      // opens: a point a column has drained past and the heap has not yet reached carries neither
      // work, and this instrument carries no picture of its own for it. At both doors that gap is
      // empty — nothing has moved at the entry, everything has landed at the exit — so the alpha is
      // 1 at every point and each door is one whole work, opaque throughout.
      coverage: {
        writes: true,
        how: "the greater of the heap's own coverage and the falling matter's — 1 where the heap "
             + "has reached this point or the departing work still stands over it, 0 in the gap "
             + "between the two",
      },
      // The neutral pose is the ENTRY DOOR — `mix` at 0, the value the `doors` block above names —
      // so the frame keys the host reads off it at registration include the door's own record.
      neutralPose: { mix: 0, clock: 0, columns: 16, repose: 0.45, stagger: 0.5, grain: 0.4,
                     seed: 0, shade: 1, mask: 0, presence: 1, reduced: false,
                     cssWidth: 1000, cssHeight: 1000 },
      passes: [{
        program: "pour", vert: VERT, frag: FRAG, position: "aPos",
        uniforms: [
          { name: "uPresence", type: "float", source: "handle:presence" },
          { name: "uA", type: "sampler2D", source: "textureA" },
          { name: "uB", type: "sampler2D", source: "textureB" },
          { name: "uFitA", type: "vec4", source: "fitA" },
          { name: "uFitB", type: "vec4", source: "fitB" },
          { name: "uRes", type: "vec2", source: "resolution" },
          { name: "uPour", type: "vec4", source: "frame:pour" },
          { name: "uHeap", type: "vec4", source: "frame:heap" },
          { name: "uLight", type: "vec2", source: "frame:light" },
          { name: "uMask", type: "float", source: "handle:mask" },
        ],
      }],
      // The instrument allocates nothing of its own: it spends the two source-texture slots the host
      // already holds and the one programme the host builds from this manifest. There is no
      // simulation here and no state between frames — a pile's height is a pure function of the
      // dial, which is what lets a seeded score repeat to the pixel and a scrub run backwards.
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
                   programs: 1, passes: 1, bytesEstimate: 2000088, variant: "lean" },
                   standard: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0,
                               programs: 1, passes: 1, bytesEstimate: 8000088,
                               variant: "standard" },
                   rich: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                           passes: 1, bytesEstimate: 32000088, variant: "rich" } },
      capabilities: ["webgl2"],
      decline: ["one work only", "a source that never decoded"],
      // AUTHORED HERE RATHER THAN PORTED. There is no lab module for a pour, so there is no path and
      // no commit to name, and saying so is the honest entry.
      provenance: { labPath: null,
                    authored: "engine/assets/pass-inst-pour.js, against charter shelf 14's «granular "
                            + "pour (particles with an angle of repose; B condenses from the pour)»" },
      // HOW WELL THIS INSTRUMENT SUITS A PAIR (2026-08-18, his word of 09:51 and its sharpening at
      // 09:53). An instrument no longer answers WHETHER it takes a pair — it answers how well it
      // suits one, so a poor fit is still playable and still explains itself. The arithmetic runs in
      // the composer, which is the one place holding both records; what stands here is the
      // instrument's own statement of WHAT IT READS, which is the fact this file owns. A fit of
      // nothing is never a refusal — it ranks last and plays where nothing ranks higher.
      suits: { reads: ["structure.regions.score", "texture.spectralPeriodPx", "texture.detailPx"],
               how: "a pour needs a picture that will let go in pieces and a material to heap: the "
                  + "departing work's own region line says how plainly it comes apart into streams, "
                  + "and the two works' detail scales say whether the material that falls is the "
                  + "material that heaps. Both readings stand on any two photographs, which is why "
                  + "this instrument suits every pair somewhat and no pair absolutely" },
      readiness: "production-ready",
    };

    var live = false;
    return {
      name: "pour",
      manifest: manifest,
      values: values,
      fit: fit,
      feel: feelOf,
      heapAt: heapAt,
      prepare: function (o) {
        if (!o.sources) return { take: false, why: "the pour instrument needs both works" };
        if (!o.cue) return { take: false, why: "no cue names it" };
        return { take: true };
      },
      start: function () { live = true; },
      // The pose the shader draws. Every number in it comes from a handle a score can drive, and the
      // grain's own drift reads the second the host hands down, so a seeded run repeats to the pixel.
      //
      // A DOOR THIS INSTRUMENT CANNOT KEEP WHOLE IS REFUSED RATHER THAN DRAWN. At either door it
      // walks its own heap over the buffer the host is about to bind and, where a point of that walk
      // carries the wrong work and standing the heap steeper does not close it, hands the host the
      // reason with the measured numbers in it. The host recovers the transaction on that reason and
      // the walk's own glide carries the visitor, which is the product's own behaviour with no
      // renderer.
      frame: function (st) {
        if (!live) return;
        var h = st.handles;
        var pose = {
          mix: h.mix, columns: h.columns, repose: h.repose, stagger: h.stagger, grain: h.grain,
          seed: h.seed, shade: h.shade, mask: h.mask,
          presence: h.presence,
          t: h.clock, reduced: st.reduced,
          cssWidth: st.viewport.w, cssHeight: st.viewport.h,
          // THE GRID THE SHADER WILL SAMPLE ON, carried into the pose so the door is read on the
          // buffer the host is about to bind as `uRes` rather than on the CSS frame around it. The
          // host settles it from the device ratio and its own resolution step, so it moves while a
          // pass plays and each door is read on the grid standing at that door's own instant.
          bufWidth: st.viewport.bufferW, bufHeight: st.viewport.bufferH,
        };
        // AT A DOOR THE INSTRUMENT SAYS WHAT IT APPLIED, and says it before it refuses. `request` is
        // the repose the score asked for and `applied` the one this grid could keep a whole door at,
        // so `moved` is the two read against each other in the handle's own units.
        // WHICH DOOR LAW THIS VOICE OWES, and it is not this instrument's to choose — the host
        // publishes where the voice stands and the contract is docs/design/ENTRY-DOOR.md. Standing
        // LOWEST, it owes the departing work whole at its entry door and the arriving work whole at
        // its exit, which is what the proof below measures. Standing OVER another voice at no
        // presence at all it owes the opposite, and already keeps it: its alpha is zero at every
        // point, so what the door shows is whatever stands beneath, whole and untouched. There is no
        // reading to take of a frame this instrument never drew into, and the whole-work proof would
        // refuse it for doing exactly what its own law asks.
        var absent = st.standsOver && !(h.presence > 0);
        if ((h.mix === 0 || h.mix === 1) && !absent) {
          var v = values(pose);
          if (st.reportApplied) {
            st.reportApplied({
              door: h.mix === 0 ? "in" : "out",
              buffer: [pose.bufWidth, pose.bufHeight],
              reads: "the heap",
              request: v.reposeRequest,
              applied: v.reposeRequest + v.reposeMoved,
              moved: v.reposeMoved,
              unit: "the repose handle's own units",
              // What the heap itself was doing over the frame at this door: how many of the walked
              // points carried the wrong work, and how much frame the tightest of them had to spare
              // in rows of the buffer.
              wrong: v.pileRead ? v.pileRead.wrong : null,
              spareRows: v.pileRead ? v.pileRead.spareRows : null,
              ceiling: v.ceiling,
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
    instrument: pourInstrument(),
  });
})();
