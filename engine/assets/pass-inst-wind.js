/*!pass-inst-wind.js*/
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
// OWNERSHIP, AND WHERE THIS ONE CAME FROM. `lab/effects/` holds no wind module. The charter's shelf
// 14 asks for one — «wind bending rows» — so the mathematics below is authored here rather than
// ported, and that is said out loud: `provenance.labPath` is null, no response curve is carried, and
// every constant that is not derived names the sentence it stands on.
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
  // THE WIND INSTRUMENT (§8) — charter shelf 14, the elements
  // ================================================================================================
  // WHAT THE VISITOR SEES. The photograph is cut into rows along its own banding axis, and one gust
  // crosses them. Where the gust stands, the rows bow: each is pushed sideways out of its own line
  // and carried a little along the wind as well, so a straight edge running across the picture goes
  // slack as the gust reaches it and comes taut again behind it. The gust does not arrive on every
  // row at once — it comes in at the angle the work's own lattice runs, so it reaches the near rows
  // first and the far rows last, and what travels across the frame is a leaning front rather than a
  // line. THE CHANGE OF HANDS RIDES THAT FRONT: everything the gust has passed is the arriving
  // photograph, everything ahead of it is the departing one, and because the front is bent by the
  // same air that bends the rows, the boundary between the two works is a bowed, staggered thing
  // that no editor's wipe could draw.
  //
  // ONE GUST TO A CROSSING. It enters before the first row and leaves past the last, once, in one
  // direction, and it never comes back — which is the whole answer to the ban on a gesture that
  // retraces its own path. What a row does is return to its own line after the gust has gone, and
  // that is a row standing still rather than a figure travelling back over itself: nothing on the
  // frame ever walks a path twice.
  //
  // ------------------------------------------------------------------------------------------------
  // THE FOUR THINGS THE CONSTRUCTION HAS TO ANSWER
  // ------------------------------------------------------------------------------------------------
  //   · WHERE THE GUST IS. One number of the dial, travelling from before the leading edge of the
  //     frame to past its trailing edge plus the whole of the rows' own lag. So at the entry door no
  //     point of any row has been reached and at the exit door every point of every row has, which
  //     is what makes both doors exact for every lag a score can name.
  //   · HOW A ROW BENDS. The gust carries a body of its own length, and a row is pushed by that
  //     body: hardest at the front, nothing well ahead of it and nothing well behind. The push is
  //     mostly ACROSS the row — that is the bow — with a third of it ALONG the row, which is what
  //     bends the boundary as well as the picture.
  //   · WHY THE ROWS READ AS ROWS. Each row takes its own share of the push, drawn from its own
  //     hash, so neighbouring rows lean by different amounts and shear against one another. That
  //     shear is the row structure a viewer sees. It is a displacement of the picture and never a
  //     mark: nothing is drawn between two rows, and the two rows' matter meets edge to edge.
  //   · WHY A DOOR IS THE FILE. The bend rides one envelope over the whole passage — nothing at
  //     both doors, whole in the middle — so at either door the displacement is exactly zero at
  //     every point and the frame is the source cover-fitted and nothing else.
  //
  // ------------------------------------------------------------------------------------------------
  // THE BANS, AND THE ONE THIS INSTRUMENT CAME NEAREST TO
  // ------------------------------------------------------------------------------------------------
  // NOTHING THAT READS AS A STOCK EFFECT FROM A CHEAP VIDEO EDITOR, and this is the ban the
  // construction stood closest to. The stock effect is the RIPPLE: one sine displacing the whole
  // frame, running forever, on nobody's structure. Four things separate this from it, and each is a
  // property of the construction rather than a promise.
  //   · IT IS NOT ONE FIELD OVER THE WHOLE FRAME. The picture is cut into rows and each row takes
  //     its own share of the push, so what moves is a set of ribbons and never a rubber sheet.
  //   · IT DOES NOT REPEAT. There is one gust, it crosses once, and its position is a function of
  //     the dial and not of a clock. A pass has one event in it, at the place the front happens to
  //     be when the visitor is watching.
  //   · IT STANDS ON THE WORK'S OWN STRUCTURE. Which way the rows run is the recorded banding axis;
  //     how many there are is the pair's own measured band count; how long the gust's body is and
  //     how far it leans are the work's own repeat and its own lattice angle. Take those away and
  //     there is no picture here to draw.
  //   · IT CARRIES THE CROSSING. The displacement is not decoration over a dissolve — the change of
  //     hands rides the gust's own front, so the wind IS the handover.
  //
  // NO DRAWN SEAM LINE BETWEEN ROWS. Nothing is drawn at a row's boundary; two rows differ by a
  // displacement and their matter meets edge to edge, which is a shear and not a stroke.
  // NO ALPHA CROSSFADE AS THE ARRIVAL. The two works are never weighed against each other. The
  // boundary is one point of the drawing buffer wide, read off the gust's own direction.
  // NO PATTERN LAID OVER A WORK THAT CARRIES ITS OWN. There is no pattern at all: the only field
  // written over a photograph is a displacement, and its geometry is the work's own banding.
  function windInstrument() {
    var VERT = [
      "attribute vec2 aPos;",
      "varying vec2 vUv;",
      "void main(){ vUv = vec2(aPos.x * 0.5 + 0.5, 0.5 - aPos.y * 0.5); gl_Position = vec4(aPos, 0.0, 1.0); }",
    ].join("\n");

    // ----------------------------------------------------------------------------------------------
    // THE SHADER
    // ----------------------------------------------------------------------------------------------
    // THE FRAME IS READ IN THE ROWS' OWN COORDINATES. `along` runs the length of a row and `across`
    // runs from one row to the next, both taken about the frame's own centre so a turn of the axis
    // turns the rows and moves nothing else. Everything below is written in those two, and the one
    // place a lookup happens turns them back.
    //
    // THREE CARRIERS HOLD EVERYTHING THAT MOVES, because the host binds four uniform types and a
    // shorter list is a shorter fence.
    var FRAG = [
      "precision highp float;",
      "varying vec2 vUv;",
      "uniform sampler2D uA;",          // the work ahead of the gust
      "uniform sampler2D uB;",          // the work the gust has already passed
      "uniform vec4 uFitA;",
      "uniform vec4 uFitB;",
      "uniform vec2 uRes;",
      // dx, dy: which way a row runs. rows: how many rows the picture is cut into.
      // lag: how much of the gust's own travel the far rows stand behind the near ones.
      "uniform vec4 uRow;",
      // front: where the gust stands, in the rows' own along-coordinate, before any lag.
      // body: how long the gust's body is, along a row.
      // amp: how far the air may push a row now, already through the passage's own envelope.
      // phase: the die's own offset into the row hash.
      "uniform vec4 uGust;",
      // shade: the judge channel for the light a leaning row catches.
      // travel: the judge channel for the bend itself.
      // flutter: the fine tremor the clock carries, already through the same envelope.
      "uniform vec4 uJudge;",
      "uniform float uMask;",
      // HOW FAR THE AIR MAY PUSH A ROW AT THE FULLEST GUST, in frame widths, and how much of that
      // push runs ALONG the row rather than across it. The first is under a twelfth of the frame —
      // a row leans, it never leaves its own place — and the second is a third, which is what bends
      // the boundary as well as the picture without turning the bow into a slide.
      "const float REACH = 0.080;",
      "const float DOWNWIND = 0.35;",
      // HOW MUCH OF ITS OWN SHARE OF THE PUSH A ROW KEEPS. Every row takes at least two thirds, so
      // no row stands still while its neighbour bows, and the third that varies is what makes them
      // shear against one another.
      "const float KEEP = 0.66;",
      // HOW MUCH LIGHT A ROW LEANING AWAY LOSES. A fifth, so a bow reads as a bow and the picture is
      // never lost to the modelling.
      "const float LIGHT = 0.20;",
      "float h11(float i){ return fract(sin(i * 78.233 + uGust.w) * 43758.5453); }",
      "vec2 into(vec2 p, vec4 f){",
      "  return clamp((p - 0.5) * f.xy + 0.5 + f.zw, 0.0008, 0.9992);",
      "}",
      "void main(){",
      "  vec2 uv = vUv;",
      "  vec2 dir = vec2(uRow.x, uRow.y);",
      "  vec2 nrm = vec2(-dir.y, dir.x);",
      "  vec2 c = uv - 0.5;",
      "  float along = dot(c, dir) + 0.5;",
      "  float across = dot(c, nrm) + 0.5;",
      "  float rows = max(uRow.z, 1.0);",
      // WHICH ROW THIS POINT BELONGS TO, and how far behind the near rows it stands. The lag is
      // ORDERLY and not rolled: the air comes in at an angle, so it reaches the rows in their own
      // order, and the die below moves only how hard each row leans.
      "  float rj = floor(clamp(across, 0.0, 0.9999) * rows);",
      "  float lag = uRow.w * (rj / max(rows - 1.0, 1.0));",
      "  float front = uGust.x - lag;",
      // THE GUST'S OWN BODY. Hardest at the front, nothing well ahead of it and nothing well behind,
      // so what crosses the picture is a body of air and not a wall.
      "  float e = (along - front) / max(uGust.y, 1e-3);",
      "  float body = exp(-e * e);",
      // HOW HARD THIS ROW LEANS. Its own share of the push, with the clock's fine tremor over it —
      // and the tremor is already through the passage's own envelope, so it cannot reach a door.
      "  float share = KEEP + (1.0 - KEEP) * h11(rj);",
      "  float push = uGust.z * body * share * uJudge.z;",
      "  vec2 ee = min(uv, 1.0 - uv);",
      "  float taper = smoothstep(0.0, 0.05, min(ee.x, ee.y));",
      "  push *= taper;",
      // WHERE THIS POINT'S MATTER CAME FROM: back along the push. Mostly across the row, which is
      // the bow; a third of it along the row, which is what carries the boundary with the air.
      "  vec2 disp = nrm * push + dir * (DOWNWIND * push);",
      "  vec2 src = uv - disp;",
      // THE CHANGE OF HANDS RIDES THE FRONT, read at the SOURCE point rather than at the output one,
      // so the boundary is bent by the very air that bends the picture. It is one point of the
      // drawing buffer wide, measured along the gust's own direction, so it carries no fade of its
      // own and no step either.
      "  float alongS = dot(src - 0.5, dir) + 0.5;",
      "  float band = max(length(vec2(dir.x / max(uRes.x, 1.0), dir.y / max(uRes.y, 1.0))), 1e-6);",
      "  float cov = clamp(0.5 + (front - alongS) / band, 0.0, 1.0);",
      "  vec3 colA = texture2D(uA, into(src, uFitA)).rgb;",
      "  vec3 colB = texture2D(uB, into(src, uFitB)).rgb;",
      "  vec3 col = mix(colA, colB, cov);",
      // THE LIGHT A LEANING ROW CATCHES. A row pushed one way takes the light and one pushed the
      // other loses it, written over the row's body and nowhere near its boundary — which is why
      // there is no drawn line between two rows here. It rides the same push, so it is exactly
      // nothing at both doors.
      "  col *= 1.0 + LIGHT * (push / max(REACH, 1e-6)) * uJudge.x;",
      // THE JUDGES' OWN FRAME: which work stands at this point, how hard this row is leaning, and
      // where the gust's own body stands. It is read as colour and carries no coverage of its own,
      // because what it is for is to be measured rather than looked at.
      "  vec3 judge = vec3(cov, clamp(push / max(REACH, 1e-6) * 0.5 + 0.5, 0.0, 1.0), body);",
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

    /* HOW MANY ROWS THE PICTURE IS CUT INTO, at either end of the `rows` handle. Three is a picture
       in three bands, which is the fewest that can shear against one another at all; sixty is a row
       under fourteen points of a 844-point frame, at which a row is thinner than the bow it takes
       and the shear stops reading as rows. */
    var ROWS_MIN = 3, ROWS_MAX = 60;

    /* HOW LONG THE GUST'S BODY IS ALONG A ROW, at either end of the `gust` handle, in frame widths.
       At the short end the front is a hard edge of air and the crossing reads as a wipe the wind
       carries; at the long end the whole frame is inside one gust at once and the picture bows as a
       single field. Both ends are this file's own decision and are named in its report. */
    var BODY_MIN = 0.06, BODY_MAX = 0.70;

    /* HOW MUCH OF THE GUST'S OWN TRAVEL THE FAR ROWS STAND BEHIND THE NEAR ONES, at either end of
       the `lag` handle. At nothing the front is square to the rows and reaches them all together;
       at a whole one the last row is reached only as the first is cleared, which is air coming in
       at forty-five degrees across the frame. */
    var LAG_MAX = 1.0;

    /* HOW FAR THE FRONT TRAVELS BEYOND EITHER EDGE OF THE FRAME. A tenth, the same share the
       material and the water instruments both give their own travelling thresholds — one law, one
       number, read in three instruments' own units. It is what leaves the gust wholly outside the
       frame at the entry door and wholly past it at the exit. */
    var MARGIN = 0.10;

    /* HOW FAR A ROW MAY BE PUSHED AT THE FULLEST GUST, in the script's own copy of the shader's
       constant, because the door reading below stands on exactly this number and a second
       description of one wind could disagree with the first. */
    var REACH = 0.080;

    // THE DEAD BANDS AT EITHER END OF THE HAND. Over the first and last five hundredths of the
    // dial the gust stands wholly outside the frame and the envelope holds the bend at nothing,
    // so the standing work is the picture its source carries, to the point.
    //
    // UNJUSTIFIED — a local copy of the one home, pass-inst-boxfold.js:458 (plan row S-82,
    // 2026-09-03); a pass-inst-*.js file is independently loaded and version-pinned (PASS-API-V1
    // §1.2) with no shared runtime to read that file's value from, so this literal is kept in
    // sync by hand rather than by construction.
    var FEEL_D0 = 0.05;

    /* NO RESPONSE CURVE IS CARRIED, and that is a fact rather than an omission: there is no lab
       module here whose felt change was measured, and fitting a curve to a picture nobody has
       watched would be a number nobody read reaching the picture. What the hand gets is the dead
       bands and nothing else. What a viewer actually feels is the gust's own body passing, which is
       geometry rather than taste. */
    function feelOf(u) {
      return clamp((clamp(u, 0, 1) - FEEL_D0) / (1 - 2 * FEEL_D0), 0, 1);
    }

    /* THE SPAN THE SCORE'S DIE ARRIVES ON, and what this instrument spends it on: HOW HARD EACH ROW
       LEANS. The die is a phase into the row hash, so two passes over one edge see the same gust
       take the rows differently while every other number of the frame stays where the score put it —
       charter shelf 13's rubato read on this instrument's own axis. It moves neither door: every
       row's share is between two thirds and one, and both doors hold the push at exactly nothing
       whatever the share is. */
    var SEED_SPAN = 8;

    // Cover-fit a work into the frame and nothing beyond it. The bend is tapered to nothing at the
    // frame's own edge, so no sample is ever fetched from outside the picture and no headroom has to
    // be bought from it — BOTH DOORS FRAME AT A CROP OF EXACTLY ONE.
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
    // and every number in the pose comes from a handle a score drives. The one place a second is
    // read is the fine tremor, which reads the `clock` handle rather than a wall clock, so a seeded
    // score repeats to the pixel.
    //
    // The gust's own length is a parameter rather than read straight off the pose, because the hold
    // in `values` below asks this same function for the same pose at a shorter gust. Nothing else
    // about it moved.
    function posed(st, gust) {
      var d = feelOf(st.mix);
      var rows = Math.max(ROWS_MIN, Math.min(ROWS_MAX, Math.round(Number(st.rows) || ROWS_MIN)));
      var ang = clamp(Number(st.axis) || 0, 0, 1) * Math.PI;   // the axis handle in half turns
      var lag = clamp(st.lag, 0, 1) * LAG_MAX;
      var body = BODY_MIN + (BODY_MAX - BODY_MIN) * clamp(gust, 0, 1);
      // HOW FAR THE FRAME REACHES ALONG THE ROWS, DERIVED FROM THE AXIS AND NOT ASSUMED. With the
      // rows square to the frame the along-coordinate runs from 0 to 1; turn them and the frame's
      // own corners run further — the furthest corner stands at `(|cos| + |sin|) / 2` from the
      // middle, which is a seventh over a half at forty-five degrees. Reading it rather than
      // assuming a half is what keeps both doors exact at every axis a score can name; assuming one
      // would have left a corner of the frame on the wrong side of the front at the shortest gust.
      var half = (Math.abs(Math.cos(ang)) + Math.abs(Math.sin(ang))) / 2;
      // THE GUST'S OWN TRAVEL. It starts a margin and two body-lengths before the frame's furthest
      // leading corner — so even the head of its body is outside the frame — and finishes the same
      // distance past the furthest trailing corner PLUS the whole of the rows' own lag, so the last
      // row is cleared too. Both ends are derived from the axis, the body and the lag rather than
      // typed against them.
      var start = 0.5 - half - MARGIN - 2 * body;
      var end = 0.5 + half + MARGIN + 2 * body + lag;
      var front = start + d * (end - start);
      // THE ONE ENVELOPE THE BEND RIDES. Nothing at both doors, whole in the middle, so both
      // landings are exact and the bend is a thing that happens rather than a thing switched on.
      //
      // IT IS BUILT OUT OF THE DIAL ITSELF AND NOT OUT OF A SINE, and that is a repair rather than a
      // preference: `sin(π·d)` at d = 1 is the machine's own rounding of π rather than nothing —
      // 1.22e-16 of a frame width — so a door that asks for still air would be refused by its own
      // instrument on a pose that is correct. `4·d·(1 − d)` lands on exactly nothing at both ends
      // in floating point, which is the same window the parting-by-light instrument holds its two
      // accompanying voices with, and it is the one this file's own door reading stands on.
      var env = 4 * d * (1 - d);
      var travel = clamp(st.travel, 0, 1);
      var amp = REACH * clamp(st.bend, 0, 1) * env * travel;
      var flutterAt = st.reduced ? 0 : (Number(st.t) || 0);
      var flutter = 1 + 0.22 * env * Math.sin(flutterAt * 5.7);
      var phase = (clamp(st.seed, 0, SEED_SPAN) / SEED_SPAN) * 2 * Math.PI;
      var v = {
        row: [Math.cos(ang), Math.sin(ang), rows, lag],
        gust: [front, body, amp, phase],
        judge: [clamp(st.shade, 0, 1), travel, flutter, 0],
        // the same numbers by name, for the reading below and for the diagnostic surface
        dialAt: d, rows: rows, angle: ang, lag: lag, body: body, front: front,
        start: start, end: end, env: env, amp: amp, flutter: flutter, phase: phase,
        shade: clamp(st.shade, 0, 1), travel: travel, reach: REACH, margin: MARGIN, coverCrop: 1,
        mask: clamp(typeof st.mask === "number" ? st.mask : 0, 0, 1),
        gustAsked: clamp(gust, 0, 1),
        grid: gridOf(st),
      };
      return v;
    }

    // ---- THE DOOR THE INSTRUMENT READS FOR ITSELF --------------------------------------------------
    // His 18:00 architecture decision, carried in the U27 brief: the instrument reads its doors at
    // runtime on the actual buffer, and the report it hands back is the runtime truth; what the
    // manifest declares is only the claim.
    //
    // WHAT A DOOR ASKS OF A WIND. Two things, and both are walked on the buffer rather than
    // declared:
    //   · THE AIR IS STILL. The envelope is exactly nothing at both ends of the dial, so the push is
    //     exactly nothing at every point and the frame is the source cover-fitted and nothing else.
    //   · THE GUST IS WHOLLY OUTSIDE THE FRAME. The front travels a margin and two body-lengths past
    //     either edge, and past the rows' own lag at the far end, so no point of any row stands on
    //     the wrong side of it. That is a claim about a GRID — the boundary is one point of the
    //     buffer wide, and how wide one point is along the gust's own direction depends on the
    //     buffer the host binds — so it is WALKED at the buffer's own sample points instead of being
    //     asserted: the four corners, where a turned axis carries the along-coordinate furthest, and
    //     an even walk of the rows between them.
    //
    // WHAT THE READING FINDS, SAID PLAINLY. On every buffer a phone or a desk can hand, the front
    // stands two whole body-lengths clear and both doors come out whole. The reading is still taken,
    // because a door held by a number nobody read is a claim rather than a landing: it publishes how
    // many crossover bands the tightest point had TO SPARE, so a gust driven toward its longest
    // body, or a lag driven to its far end, shows the margin closing long before anything crosses.
    //
    // AND THERE IS SOMETHING HERE TO HOLD. The fault has a direction that closes it: the travel is
    // derived FROM the body, so a shorter gust stands further clear at both ends — a door a score's
    // gust length cannot keep whole is answered by shortening the gust until it is, and the request
    // stays on the record beside what was applied.
    var DOOR_HOLD = 0.25;     // how far the hold may walk the gust handle, in the handle's own units
    var DOOR_STEP = 0.05;     // and in what steps
    var DOOR_GRID = 24;       // how many steps the reading walks across the frame

    function windReadOf(v, W, H, want) {
      var walked = 0, wrong = 0, spare = 1e9, push = 0, i, j, ux, uy;
      var dx = Math.cos(v.angle), dy = Math.sin(v.angle);
      var band = Math.max(Math.sqrt((dx / W) * (dx / W) + (dy / H) * (dy / H)), 1e-6);
      function walk(px, py) {
        ux = px / W; uy = py / H;
        var along = (ux - 0.5) * dx + (uy - 0.5) * dy + 0.5;
        var across = -(ux - 0.5) * dy + (uy - 0.5) * dx + 0.5;
        var rj = Math.floor(clamp(across, 0, 0.9999) * v.rows);
        var front = v.front - v.lag * (rj / Math.max(v.rows - 1, 1));
        // `cov` is 1 where the arriving work stands. At the entry door every point owes its picture
        // to the departing work, so `cov` must be 0 at every point; at the exit door it must be 1.
        var cov = clamp(0.5 + (front - along) / band, 0, 1);
        var room = want ? (along - front) / band : (front - along) / band;
        if (want ? cov > 0 : cov < 1) wrong++;
        if (room < spare) spare = room;
        walked++;
      }
      for (i = 0; i <= DOOR_GRID; i++) {
        for (j = 0; j <= DOOR_GRID; j++) {
          walk(clamp((i / DOOR_GRID) * W, 0.5, W - 0.5),
               clamp((j / DOOR_GRID) * H, 0.5, H - 0.5));
        }
      }
      push = Math.abs(v.amp);
      return { walked: walked, wrong: wrong, spareBands: spare, push: push, want: want,
               body: v.body, gust: v.gustAsked, lag: v.lag, band: band };
    }

    function doorReadOf(v, st) {
      var want = st.mix === 0 ? 0 : (st.mix === 1 ? 1 : -1);
      if (want < 0) return null;
      var g = v.grid;
      if (!g.given) return null;
      var read = windReadOf(v, g.w, g.h, want === 0 ? 1 : 0);
      read.entry = want === 0;
      read.grid = g;
      return read;
    }

    // THE REFUSAL, worded the way the host's own manifest refusals read: what is wrong, in this
    // instrument's own measured numbers, on the grid it was measured on.
    function doorWhyNoOf(read) {
      if (!read) return null;
      var g = read.grid, where = " of a " + g.w + " x " + g.h + (g.drawn ? " buffer" : " frame");
      var door = read.entry ? "the entry" : "the exit";
      var work = read.entry ? "departing" : "arriving";
      var other = read.entry ? "arriving" : "departing";
      if (read.push > 0) {
        return door + " door leaks: the air is not still — the push stands at " + read.push.toFixed(6)
             + " of a frame width" + where + ", where this door's own law asks for the " + work
             + " work exactly as the file carries it";
      }
      if (read.wrong) {
        return door + " door leaks: the gust puts the " + other + " work on " + read.wrong
             + " of the " + read.walked + " points this reading walked" + where
             + " — at a body of " + read.body.toFixed(3) + " and a lag of " + read.lag.toFixed(3)
             + " the front has not travelled clear of the frame — where " + door
             + " door's own law asks for the " + work + " work at every point";
      }
      return null;
    }

    // THE NUMBERS OF ONE FRAME, WITH ITS DOOR READ ON THE BUFFER BEING DRAWN. Away from a door this
    // is `posed` and nothing more: the reading is taken nowhere else and no gust length moves. At a
    // door whose gust has not travelled clear of the frame on the buffer being drawn, the instrument
    // SHORTENS the gust — the only direction that closes it, since the travel is derived from the
    // body — and answers with the first pose whose door is whole. What the score asked for and what
    // was applied are both on the record.
    function values(st) {
      var asked = clamp(typeof st.gust === "number" ? st.gust : 0.45, 0, 1);
      var v = posed(st, asked);
      v.gustRequest = asked;
      v.gustMoved = 0;
      v.doorHeld = null;
      var read = doorReadOf(v, st);
      var no = doorWhyNoOf(read);
      v.doorGrid = read ? read.grid : null;
      v.air = read ? { walked: read.walked, wrong: read.wrong, spareBands: read.spareBands,
                       push: read.push } : null;
      if (!no) { v.doorWhyNo = null; return v; }
      for (var step = DOOR_STEP; step <= DOOR_HOLD + 1e-9; step += DOOR_STEP) {
        var tryG = asked - step;
        if (tryG < 0) break;
        var w = posed(st, tryG);
        var wRead = doorReadOf(w, st);
        if (doorWhyNoOf(wRead)) continue;
        w.gustRequest = asked;
        w.gustMoved = asked - tryG;
        w.doorHeld = no;
        w.doorWhyNo = null;
        w.doorGrid = wRead.grid;
        w.air = { walked: wRead.walked, wrong: wRead.wrong, spareBands: wRead.spareBands,
                  push: wRead.push };
        return w;
      }
      v.doorWhyNo = no + ", and shortening the gust by the " + DOOR_HOLD
                  + " of this handle's own travel the hold reaches does not close it";
      return v;
    }

    var manifest = {
      id: "wind", api: 1, arity: 2,
      // The departing work goes slack as the gust reaches it, the middle is a frame of rows leaning
      // between two pictures, and the arriving work comes taut behind the front.
      roles: ["disassembly", "mystery", "assembly"],
      // READ OFF THIS INSTRUMENT'S OWN CONSTRUCTION, and said to be read rather than published:
      // there is no lab module for a wind, so no vocabulary table carries a row for it.
      //   · CELL — the frame is cut into rows and each row takes its own share of the push and
      //     shears against its neighbours, which is a named part of the frame moving as a whole.
      //   · SURFACE — one front runs over the whole frame and its position decides which of the two
      //     works stands at a point, which is the level `pass-inst-adrift.js` and
      //     `pass-inst-liquid.js` both place that act at.
      // TEXTURE IS NOT CLAIMED: the air moves the picture's rows and never touches the material
      // inside them, which is untouched in both works.
      levels: ["SURFACE", "CELL"],
      // WHAT THIS INSTRUMENT CUTS ON. A row is a band of the frame taken along the work's own
      // recorded banding axis, which is the STRIP kind — the same family the woven instrument's
      // ribbons are cut from, and the kind `KIND_OF_MEASURE` gives the recorded `banding` measure.
      // The declaration lives here, in the instrument's own file, because the site's settings build
      // prefers a manifest's own `cuts` to any table it keeps and names an instrument that declares
      // none as UNPLACED — landed and uncastable.
      cuts: ["strip"],
      // WHERE THIS INSTRUMENT HAS A SEAM (§8's `seams` block). The change of hands rides the gust's
      // own front, read at the source point: `cov = clamp(0.5 + (front - alongS) / band, 0.0, 1.0)`
      // with `band` the gust's own direction measured in the buffer's resolution — the shader's own
      // words above it: "It is one point of the drawing buffer wide, measured along the gust's own
      // direction, so it carries no fade of its own and no step either." A HAIRLINE retouch: the
      // boundary is bowed and staggered by the same air that bends the rows, but its WIDTH is the
      // buffer's own sampling footprint rather than a band the shader grew on purpose. `of` names no
      // handle: the crossover stays one buffer point wide whatever `rows` the picture is cut into or
      // however hard the gust leans the front through `lag`.
      seams: [{ kind: "line", of: null, unit: "points of the drawing buffer" }],
      params: { rows: [ROWS_MIN, ROWS_MAX], bend: [0, 1], gust: [0, 1], lag: [0, 1], axis: [0, 1] },
      // EVERY handle a score can drive (§4.4b). `mix` is the dial and `clock` is the second the host
      // hands down — the one place a second reaches this instrument at all, the fine tremor over the
      // gust. `seed` is the score's die, `shade` and `travel` are the two judge channels, and `mask`
      // is the judges' frame.
      //
      // EVERY HANDLE THAT SHAPES THE PICTURE NAMES THE MEASUREMENT OF A PHOTOGRAPH IT READS, which
      // is his 19:13 word lifted to the class at 19:21. What stands here is the sentence; the
      // arithmetic that turns a reading into a value runs in the composer.
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
        rows: { min: ROWS_MIN, max: ROWS_MAX, def: 14,
                unit: "how many rows the picture is cut into",
                reads: "the pivot's own band family, its measured count along the cut — the same "
                     + "reading the woven instrument's `strips` names, under this instrument's own "
                     + "name because a row of this instrument is a row and not a ribbon: it is not "
                     + "woven with anything, it is bent",
                applied: { roundedToWholeRows: true } , level: "CELL" },
        axis: { min: 0, max: 1, def: 0,
                unit: "which way the rows run, in half turns",
                reads: "the banding axis cut-lines.json recorded — the same recorded axis the woven "
                     + "instrument's ribbons run along and the folding one's crease crosses. Here "
                     + "it is the direction the rows lie in, so the air bends the work's own bands "
                     + "rather than a direction nobody measured" , level: "CELL" },
        bend: { min: 0, max: 1, def: 0.5,
                unit: "how far the air bends a row",
                reads: "structure.banding.score — how plainly a work bands. A work that bands "
                     + "plainly has rows the air can catch; one that reads as a single field is "
                     + "barely moved, which is the picture saying what it is rather than a floor "
                     + "turning it away. It TRAVELS from the departing work's reading to the "
                     + "arriving one's, so the air is stronger at the end that has more to bend",
                applied: { reachAtWhole: REACH,
                           restsAt: "both doors, where the envelope is exactly nothing" } , level: "CELL" },
        gust: { min: 0, max: 1, def: 0.45,
                unit: "how long the gust's own body is along a row",
                reads: "structure.grid.periodPx of the work over its own frame side — the repeat "
                     + "the work carries along the row — and structure.ownDevice.stepPx where no "
                     + "grid period was derived, read as a position on this handle's own range. "
                     + "The body of air is as long as the thing it is blowing over",
                applied: { bodyAt: [BODY_MIN, BODY_MAX],
                           heldWholeAtADoor: { travel: DOOR_HOLD, readOn: "the drawing buffer",
                                               reads: "gustRequest",
                                               measures: "the gust's own front against the frame's "
                                                       + "own edges, at the buffer's own sample "
                                                       + "points" } } , level: "CELL" },
        lag: { min: 0, max: 1, def: 0.4,
               unit: "how much of the gust's travel the far rows stand behind the near ones",
               reads: "structure.grid.angleDeg — the direction the work's own lattice runs — and "
                    + "structure.ownDevice.angleDeg where the device recovered one, read against "
                    + "the row axis above: the lag is the tangent of the angle between the two, so "
                    + "the air comes in across the work's own grain rather than square to a "
                    + "direction nobody measured" , level: "SURFACE" },
        seed: { min: 0, max: SEED_SPAN, def: 0,
                unit: "how hard each row leans",
                reads: "the score's own die. It is a phase into the row hash, so two passes over "
                     + "one edge see the same gust take the rows differently and neither door "
                     + "moves" , level: null },
        shade: { min: 0, max: 1, def: 1,
                 unit: "the light a leaning row catches",
                 applied: { restsAt: "both doors, where the push is exactly nothing" } , level: null },
        travel: { min: 0, max: 1, def: 1, unit: "the bend the picture rides",
                  applied: { restsAt: "both doors" } , level: null },
        mask: { min: 0, max: 1, def: 0,
                applied: { readAtADoor: { readOn: "the drawing buffer", reads: "the gust",
                                          measures: "the push over the frame and the front's own "
                                                  + "distance past either edge, at the buffer's "
                                                  + "own sample points",
                                          held: DOOR_HOLD } } , level: null },
      },
      neutrals: { a: 0, b: 1 },
      doors: { in: { handle: "mix", value: 0, work: "a" },
               out: { handle: "mix", value: 1, work: "b" } },
      // BOTH DOORS FRAME AT A CROP OF EXACTLY ONE, and that is this instrument's own small luxury:
      // the bend is tapered to nothing at the frame's edge, so it never needs headroom bought from
      // the picture and a landed door is the source cover-fitted and nothing else.
      framings: { "0": { coverCrop: 1 }, "1": { coverCrop: 1 } },
      drivers: ["progress", "cueProgress", "time", "velocity", "capability", "noise", "static",
                "curve", "spline", "map", "add", "multiply", "mix", "clamp", "hold", "segment",
                "ramp", "slew", "oscillate", "node"],
      // The construction moves no point of view: it bends the rows inside the frame and decides
      // which work owns each point, so the witness camera stays the stage's (§6).
      camera: { needs: "none", authority: "stage" },
      gl: { preserveDrawingBuffer: false },
      // WHAT THIS INSTRUMENT WRITES WHERE ITS OWN MATTER IS ABSENT (§7's coverage law, and the
      // per-instrument specification in docs/design/COVERAGE.md). It is absent nowhere: every point
      // of the frame carries one of the two photographs and the alpha is the constant 1. Under the
      // placement rule this instrument is lawful as the lowest cue of a stack and as a whole one-cue
      // score, which is the placement a ground takes.
      coverage: { writes: false,
                  how: "the gust's own front decides which work stands at every point of the frame "
                     + "— both branches of the choice are photograph — so the alpha is the constant "
                     + "1; at a door the front stands wholly outside the frame and the door is one "
                     + "whole work" },
      // The neutral pose is the ENTRY DOOR — `mix` at 0, the value the `doors` block above names.
      neutralPose: { mix: 0, clock: 0, rows: 14, axis: 0, bend: 0.5, gust: 0.45, lag: 0.4,
                     seed: 0, shade: 1, travel: 1, mask: 0, reduced: false,
                     cssWidth: 1000, cssHeight: 1000 },
      passes: [{
        program: "wind", vert: VERT, frag: FRAG, position: "aPos",
        uniforms: [
          { name: "uA", type: "sampler2D", source: "textureA" },
          { name: "uB", type: "sampler2D", source: "textureB" },
          { name: "uFitA", type: "vec4", source: "fitA" },
          { name: "uFitB", type: "vec4", source: "fitB" },
          { name: "uRes", type: "vec2", source: "resolution" },
          { name: "uRow", type: "vec4", source: "frame:row" },
          { name: "uGust", type: "vec4", source: "frame:gust" },
          { name: "uJudge", type: "vec4", source: "frame:judge" },
          { name: "uMask", type: "float", source: "handle:mask" },
        ],
      }],
      // The instrument allocates nothing of its own: it spends the two source-texture slots the host
      // already holds and the one programme the host builds from this manifest. There is no state
      // between frames — the gust's position is a pure function of the dial, which is what lets a
      // seeded score repeat to the pixel and a scrub run backwards.
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
                   programs: 1, passes: 1, bytesEstimate: 2000092, variant: "lean" },
                   standard: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0,
                               programs: 1, passes: 1, bytesEstimate: 8000092,
                               variant: "standard" },
                   rich: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                           passes: 1, bytesEstimate: 32000092, variant: "rich" } },
      capabilities: ["webgl2"],
      decline: ["one work only", "a source that never decoded"],
      // AUTHORED HERE RATHER THAN PORTED. There is no lab module for a wind, so there is no path and
      // no commit to name, and saying so is the honest entry.
      provenance: { labPath: null,
                    authored: "engine/assets/pass-inst-wind.js, against charter shelf 14's «wind "
                            + "bending rows»" },
      // HOW WELL THIS INSTRUMENT SUITS A PAIR (2026-08-18, his word of 09:51 and its sharpening at
      // 09:53). An instrument answers how well it suits a pair, never whether it takes one; the
      // arithmetic runs in the composer, and what stands here is the instrument's own statement of
      // WHAT IT READS. A fit of nothing is never a refusal — it ranks last and plays where nothing
      // ranks higher.
      suits: { reads: ["structure.banding.score", "structure.grid.angleDeg"],
               how: "the air catches what bands: the two works' own banding readings say how much "
                  + "row structure there is for a gust to take, and how far apart their lattice "
                  + "angles stand says whether the front comes in ACROSS the picture's own grain, "
                  + "which is what makes a gust read as air rather than as a wipe" },
      readiness: "production-ready",
    };

    var live = false;
    return {
      name: "wind",
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
      prepare: function (o) {
        if (!o.sources) return { take: false, why: "the wind instrument needs both works" };
        if (!o.cue) return { take: false, why: "no cue names it" };
        return { take: true };
      },
      start: function () { live = true; },
      // The pose the shader draws. Every number in it comes from a handle a score can drive, and the
      // fine tremor reads the second the host hands down, so a seeded run repeats to the pixel.
      //
      // A DOOR THIS INSTRUMENT CANNOT KEEP WHOLE IS REFUSED RATHER THAN DRAWN. At either door it
      // walks its own front over the buffer the host is about to bind and, where a point of that
      // walk carries the wrong work and shortening the gust does not close it, hands the host the
      // reason with the measured numbers in it. The host recovers the transaction on that reason and
      // the walk's own glide carries the visitor, which is the product's own behaviour with no
      // renderer.
      frame: function (st) {
        if (!live) return;
        var h = st.handles;
        var pose = {
          mix: h.mix, rows: h.rows, axis: h.axis, bend: h.bend, gust: h.gust, lag: h.lag,
          seed: h.seed, shade: h.shade, travel: h.travel, mask: h.mask,
          t: h.clock, reduced: st.reduced,
          cssWidth: st.viewport.w, cssHeight: st.viewport.h,
          // THE GRID THE SHADER WILL SAMPLE ON, carried into the pose so the door is read on the
          // buffer the host is about to bind as `uRes` rather than on the CSS frame around it.
          bufWidth: st.viewport.bufferW, bufHeight: st.viewport.bufferH,
        };
        // AT A DOOR THE INSTRUMENT SAYS WHAT IT APPLIED, and says it before it refuses. `request` is
        // the gust length the score asked for and `applied` the one this grid could keep a whole
        // door at, so `moved` is the two read against each other in the handle's own units.
        if (h.mix === 0 || h.mix === 1) {
          var v = values(pose);
          if (st.reportApplied) {
            st.reportApplied({
              door: h.mix === 0 ? "in" : "out",
              buffer: [pose.bufWidth, pose.bufHeight],
              reads: "the gust",
              request: v.gustRequest,
              applied: v.gustRequest - v.gustMoved,
              moved: v.gustMoved,
              unit: "the gust handle's own units",
              // What the air itself was doing over the frame at this door: how many of the walked
              // points carried the wrong work, how many crossover bands the tightest of them had to
              // spare, and how hard the rows were being pushed.
              wrong: v.air ? v.air.wrong : null,
              spareBands: v.air ? v.air.spareBands : null,
              push: v.air ? v.air.push : null,
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
    instrument: windInstrument(),
  });
})();
