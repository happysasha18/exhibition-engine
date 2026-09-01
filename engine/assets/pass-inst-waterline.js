/*!pass-inst-waterline.js*/
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
  // THE WATERLINE INSTRUMENT (§8) — lab/effects/waterline.js carried across
  // ================================================================================================
  // WHAT A PERSON SEES. The frame becomes a landscape. A horizon is drawn across it — sky above,
  // water below — and the water carries the sky folded about that line, copy under copy where it is
  // deeper than the sky is tall. The departing work stands above the line and keeps its own body
  // below it, combed by the swell and sunk in the depth's shade. The ARRIVING work comes in as its
  // own reflection, from the deepest water upward, so the water is showing a picture the frame does
  // not hold yet; the sky changes hands afterwards. The line itself travels down (or up) the frame,
  // and the instant it passes the middle of the frame is the instant the two works change places.
  //
  // WHERE THE LINE COMES FROM, and it is the whole point of this instrument. It is no number of its
  // own: it is the DEPARTING WORK'S OWN MEASURED SEAM — `seam_y` out of the project's own motif
  // measure — carried into the frame through the cover-fit the host applied, and it travels to the
  // ARRIVING work's own seam (lab/effects/waterline.js:1-18, and its `seamInFrame` at :419-426).
  //
  // THE PROBLEM THAT MADE THIS PORT DIFFERENT, and the road already opened for it. The lab module is
  // handed both seams at creation and reads the cover-fit off a canvas it owns. This file may read no
  // file and owns no canvas, so — exactly as the drifting instrument's manifest says of its own
  // fourteen measured numbers (pass-inst-adrift.js, «THE FOURTEEN THAT CARRY THE PAIR'S OWN
  // MEASUREMENTS») — both seams arrive as HANDLES a score row drives: `seamA` and `seamB`. The
  // seating they are carried through is the host's own: `frame()` receives `st.fitA`/`st.fitB`, the
  // very seating the draw binds as the `uFitA`/`uFitB` uniforms, so the script and the shader work
  // from ONE seating rather than two guesses at it.
  //
  // What came over: the shader, the seating of a work in the frame (coverFit → fit), the six
  // measured response curves, the line's travel and its hinge, and the numbers of one frame
  // (frameValues → values). Not one number changed.
  //
  // What stayed behind: its own canvas, its own WebGL 1 context, its own frame loop, its resize
  // listener, its own accumulated clock and its `photo` handle — which cannot cross, because the host
  // owns which two works stand in the pair and the instrument is handed two textures rather than a
  // list to pick from.
  //
  // THREE THINGS THE PORT HAD TO ANSWER.
  //   · THE ASPECT. The module hands the frame's aspect in as a uniform of its own, computed from
  //     the drawing buffer it owns. The host owns the buffer here and already binds its size as
  //     `uRes`, so the aspect is derived from `uRes` inside the shader and every use of it reads the
  //     same number as before. Every other line of the shader is the module's own, character for
  //     character.
  //   · THE PRESERVED DRAWING BUFFER. The module asks its own context for one (waterline.js:407) and
  //     §7 refuses a manifest that asks for it. What the flag stood in for is a redraw: the module
  //     draws on a parameter change, on a resize and on its own frame loop, and under reduced motion
  //     it draws once and stops. Here the host's buffer keeps nothing between frames, so this draws
  //     on EVERY frame it is handed, reduced or not. Reduced motion stops the swell's own travel
  //     inside `values` and stops nothing else.
  //   · THE VERSION HEADER. This module's shader carries none, so the host's translator stamps the
  //     one it needs and no second one arrives.
  function waterlineInstrument() {
    /* --- the numbers this module chose for itself -------------------------------------------
       CARRIED, NOT CHOSEN. Every one of these is the lab module's own taste fork, and the row in
       lab/data/fix-waterline.json names each of them again with what it buys (its `taste` block).
       Nothing here was picked by this port; the suite reads each of them out of both files. */
    var AMP = 0.055;        // counter-motion, frame heights at its widest
    var RIP = 0.020;        // how far the swell combs the reflection sideways, frame heights
    var SWAY = 0.005;       // how far the waterline itself wavers
    // Every sample is the frame coordinate pushed by at most AMP + RIP, so the cover-fit is
    // pulled in by exactly that much at each end. ZOOM is derived and is not a free number.
    var ZOOM = 1 + 2 * (AMP + RIP) + 0.03;
    var DIE_W = 0.40;       // how much of the handover's order belongs to the score's die
    var CELLS_X = 19.0;     // the tide line's own patches across the frame...
    var CELLS_Q = 8.0;      // ...and down the ladder
    var SHADE_FRONT = 0.30; // the contact shadow at the arriving work's edge
    var SHADE_REACH = 6.0;  // and how many pixels it decays over
    var SHADE_LINE = 0.26;  // the contact shadow under the waterline
    var LINE_REACH = 10.0;
    var DARK_DEEP = 0.16;   // how much darker the water gets toward the near edge
    var DARK_BASE = 0.05;
    var HAZE = 0.12;        // and how much colour it loses there
    var LINE_LIFT = 0.15;   // how far the `line` handle may carry the waterline off its own place
    var LINE_HOLD = 0.22;   // the line stands at the departing work's seam over this much of the
                            // dial, and rests on the arriving work's over as much at the far end;
                            // the travel takes the rest, half of it each side of the middle
    var OPEN_IN = 0.12;     // how much of the handle the water takes to rise into the frame,
                            // and it is SMALLER than LINE_HOLD on purpose: there is a stretch of
                            // the dial where the water stands fully open AND the line stands
                            // exactly on the departing work's own seam, which is the only place
                            // a check can measure the derivation on the picture
    var GUARD_IN = 0.10;    // and the shadows to come up
    var DEP_LO = 0.75, DEP_HI = 2.25;   // the mirror's scale: crowded folds to one long fold

    // HOW FAR THE TIDE'S OWN PATCH SIZE TRAVELS, in octaves either side of the module's own count.
    // The two counts above are what the die is rolled on and the module took both itself; the
    // `tideCells` handle carries them together, so the 19-to-8 proportion the module chose and the
    // 2.7 the fine roll rides at are held at every setting and the handle's own middle lands on
    // exactly 19.0 and 8.0. One octave either way is the register's own unit for a reading no file
    // in this tree calibrates — the same unit `acrossTheSpan` positions the material instrument's
    // grain by — so the span is the module's number and the register's unit and no third choice.
    var CELL_SPAN = 1.0;

    // HOW FAR APART THE PATCHES' OWN MOMENTS ARE SET at the far end of the `order` handle, and how
    // far past the field's own range the travelling threshold reaches (waterline.js:463-467). Both
    // are the module's, said here as named constants because the door reading below is held against
    // the second of them and a number read in two places has to have one home.
    var SPREAD_MAX = 1.10;
    var MARGIN = 0.05;
    // WHERE THE WATERLINE STANDS WITH THE WATER DRAINED OUT — below the bottom edge of the frame, so
    // a door is the work the file carries and not a work with a horizon drawn across it. It is the
    // shader's own first argument to `mix(1.04, uLine, uOpen)` below, named here for the same
    // reason: the door reading is arithmetic on it.
    var BASE_OUT = 1.04;

    var VERT = [
      "attribute vec2 aPos;",
      "varying vec2 vUv;",
      // uv.y runs downward so it matches both the image rows and the pointer
      "void main(){ vUv = vec2(aPos.x * 0.5 + 0.5, 0.5 - aPos.y * 0.5); gl_Position = vec4(aPos, 0.0, 1.0); }",
    ].join("\n");

    var FRAG = [
      "precision highp float;",
      "varying vec2 vUv;",
      "uniform sampler2D uA;",
      "uniform sampler2D uB;",
      "uniform vec4 uFitA;",       // xy = scale into image uv, zw = pan
      "uniform vec4 uFitB;",
      "uniform vec2 uRes;",        // device pixels
      "uniform float uLine;",      // the waterline's place, frame units
      "uniform float uOpen;",      // how far the water has risen into the frame
      "uniform float uTau;",       // the one travelling threshold
      "uniform float uLead;",      // how far the water runs ahead of the sky
      "uniform float uSpread;",    // how far apart the patches' own moments are set
      "uniform float uDep;",       // the mirror's scale
      "uniform float uSway;",      // the surface's own waver
      "uniform float uComb;",      // and how hard it combs what lies under it
      // THE ONE LINE OF THE SHADER THE PORT ADDED, and it is said rather than buried. The module
      // substitutes its two cell counts into the source as literals; here they arrive as a uniform,
      // because a cell across the frame's height is exactly what the works' own records measure and
      // a count nobody can set is a static parameter. The two lines that read it are the two that
      // spelled the literals, and nothing else about the die moved.
      "uniform vec2 uCells;",      // the tide line's own patches, across the frame and down the ladder
      "uniform float uTime;",      // seconds
      "uniform float uOff;",       // counter-motion, frame heights
      "uniform float uGuardE;",    // the arrival edge's shadow gate: nothing at either door
      "uniform float uGuardL;",    // and the waterline's own
      "uniform float uSeed;",
      "const float TAU = 6.28318530718;",

      // The sample is pushed by at most uOff + the swell's comb, and the cover-fit was pulled in
      // by exactly that much (ZOOM in the script below), so the push always lands on picture. The
      // clamp is the backstop; half a texel of inset keeps the linear filter off the border.
      "vec2 into(vec2 p, vec4 f){",
      "  return clamp((p - 0.5) * f.xy + 0.5 + f.zw, 0.0008, 0.9992);",
      "}",
      "vec3 texA(vec2 p){ return texture2D(uA, into(p, uFitA)).rgb; }",
      "vec3 texB(vec2 p){ return texture2D(uB, into(p, uFitB)).rgb; }",

      "float hash21(vec2 p){ return fract(sin(dot(p, vec2(41.317, 289.107))) * 43758.5453); }",

      // THE DEEPER MIRROR COPIES. A still water plane under a distant sky reflects it one to one:
      // the geometry is an exact fold about the horizon, not a squash. Where the water is deeper
      // than the sky is tall — which is most of this crossing, since one of the two seams always
      // sits well off the centre — the fold runs out of sky and BOUNCES: copy after copy, each one
      // deeper and dimmer. A triangle wave is that stack of copies exactly, and its slope is ±1
      // everywhere, so no copy is ever a smear and nothing aliases.
      "float foldTo(float s, float m){",
      "  float w = 2.0 * m;",
      "  float p = s - w * floor(s / w);",
      "  return p <= m ? p : w - p;",
      "}",

      "void main(){",
      "  vec2 uv = vUv;",
      // the aspect of the buffer the host drew into, read from the size the host binds
      "  float uAspect = uRes.x / max(uRes.y, 1.0);",
      // p.x is measured in frame HEIGHTS, so a wavelength means the same thing whichever way it
      // is measured and one pixel is the same length on both axes
      "  float px = uv.x * uAspect;",
      "  float h = 1.0 / max(uRes.y, 1.0);",

      // --- the surface, and its own movement -------------------------------------------------
      "  float w1 = sin(TAU * (px * 2.10 + uTime * 0.083));",
      "  float w2 = sin(TAU * (px * 3.70 - uTime * 0.061 + 0.37));",
      "  float sway = uSway * uOpen * (0.62 * w1 + 0.38 * w2);",
      "  float dsway = uSway * uOpen * TAU * (0.62 * 2.10 * cos(TAU * (px * 2.10 + uTime * 0.083))",
      "                                      - 0.38 * 3.70 * cos(TAU * (px * 3.70 - uTime * 0.061 + 0.37)));",
      // THE WATER RISES INTO THE FRAME. With the handle at a door the waterline stands below the
      // bottom edge, so there is no water at all and the frame is the work the file carries; as the
      // handle opens, the line climbs to the place the departing work's own seam names.
      "  float base = mix(1.04, uLine, uOpen);",
      "  float L = base + SWAY_C * sway;",
      "  float dL = SWAY_C * dsway;",                    // per frame-height along x

      "  float d = uv.y - L;",                           // > 0 is water, < 0 is sky
      "  float D = max(1.0 - L, 1e-3);",
      "  float S = max(L, 1e-3);",
      "  float water = step(0.0, d);",

      // --- ONE LADDER FROM THE DEEPEST WATER TO THE TOP OF THE SKY ---------------------------
      // q is when a point hands over: 0 goes first. The water spans [0, sp] and the sky
      // [0.5·lead, 1], so with the lead open the deep water is already the arriving work while
      // the whole sky is still the departing one — the mirror ahead of what it mirrors. With the
      // lead shut the two spans coincide and the halves hand over in step.
      "  float sp = 1.0 - 0.5 * uLead;",
      "  float aw = clamp(1.0 - d / D, 0.0, 1.0);",      // 0 at the deepest, 1 at the line
      "  float as = clamp(-d / S, 0.0, 1.0);",           // 0 at the line, 1 at the top
      "  float q = mix(0.5 * uLead + sp * as, sp * aw, water);",
      "  float dqdy = mix(-sp / S, -sp / D, water);",

      // ORDER: part a ladder, part the score's die. The ladder is q itself — a place in the
      // frame, which holds still while the line travels under it — and the die scatters the
      // patches' own moments, so the tide line comes in ragged and not as a ruled edge. The
      // patches are WARPED before they are counted: on a straight grid the die reads as a
      // staircase of rectangles, which is a grid and not a shore.
      "  float wx = px + 0.06 * sin(TAU * (q * 2.30 + 0.70));",
      "  float wq = q + 0.05 * sin(TAU * (px * 1.70 + 0.20));",
      // TWO SCALES, because one is a comb. A single cell size gives the tide one wavelength and
      // the eye reads a repeating sawtooth; a coarse roll with a finer one inside it reads as a
      // shore. The two are one die: both hashes take the same seed.
      "  float r1 = hash21(vec2(floor(wx * uCells.x), floor(wq * uCells.y)) + uSeed);",
      "  float r2 = hash21(vec2(floor(wx * uCells.x * 2.7), floor(wq * uCells.y * 2.7)) + uSeed + 11.3);",
      "  float ord = mix(q, 0.62 * r1 + 0.38 * r2, DIE_W_C);",
      "  float qe = q + uSpread * (ord - 0.5);",

      // COVERAGE OVER THE PIXEL'S OWN FOOTPRINT, from the field's own gradient — the boundary is
      // a side, not a blend, and it is one pixel wide wherever it runs. dq/dx is there because
      // the waterline wavers, which tilts the field near the surface.
      "  vec2 g = (1.0 + uSpread * (1.0 - DIE_W_C)) * vec2(-dqdy * dL, dqdy);",
      "  float grad = max(length(g), 1e-5);",
      "  float sd = (uTau - qe) / (grad * h);",          // signed pixels; positive has handed over
      "  float cov = clamp(0.5 + sd, 0.0, 1.0);",

      /* --- where each of the two works reads its picture --------------------------------------
         THE DEPARTING WORK KEEPS ITS OWN BODY. The motif is not that the lower half OUGHT to be a
         reflection — it is that in these works it ALREADY reads as one: lightness and busy-ness
         flip across the seam, which is what lab/step1-motifs.py measures. Rebuilding the lower
         half as a mirror of the upper would throw the work's own mass away — measured, it did:
         the hangar under work A's seam vanished by a third of the handle. So the departing work
         stands as it stands, and the module MEANS the fold rather than making it: below the line
         its own picture is combed by the swell, sinks in the depth's shadow and takes the
         waterline's own contact shadow.

         THE ARRIVING WORK COMES IN AS ITS REFLECTION, and that is the whole arrival mode: what
         the water carries of the second work is its sky folded about the line, so the water is
         showing something the frame does not hold yet. The fold runs at slope ±1 and bounces off
         the top of the sky, so where the water is deeper than the sky is tall the copies stack —
         the deeper mirror copies, and they are the ones that hand over first. */
      "  float dd = max(d, 0.0);",
      "  float ys = foldTo(L - dd / max(uDep, 0.05), S);",
      "  float near = clamp(dd / D, 0.0, 1.0);",
      // ONE SURFACE COMBS BOTH: the same swell displaces whatever lies under the water, so the two
      // works are held by one carrier and not by two.
      "  float ra = RIP_C * uComb * uOpen * (0.35 + 0.65 * near);",
      "  float rx = ra * sin(TAU * (px * 4.30 + uTime * 0.17)) / max(uAspect, 0.05);",
      "  float ry = ra * 0.45 * sin(TAU * (px * 2.90 - uTime * 0.12 + 0.90));",
      "  vec2 posA = uv + water * vec2(rx, ry);",
      "  vec2 posB = mix(uv, vec2(uv.x + rx, ys + ry), water);",

      // COUNTER-MOTION: the departing work settles down the frame, the arriving one rises. Below
      // the line the fold turns the arriving work's movement around, which is what a mirror does
      // to a movement.
      "  vec3 colA = texA(posA - vec2(0.0, uOff));",
      "  vec3 colB = texB(posB + vec2(0.0, uOff));",
      "  vec3 col = mix(colA, colB, cov);",

      // --- the water's own body --------------------------------------------------------------
      "  float body = water * uOpen;",
      "  col *= 1.0 - body * (DARK_BASE_C + DARK_DEEP_C * near);",
      "  col = mix(col, vec3(dot(col, vec3(0.299, 0.587, 0.114))), body * HAZE_C * near);",

      // --- TWO CONTACT SHADOWS, both exactly nothing at either door --------------------------
      // The arriving work lies on top of the departing one, so the departing side takes a shadow
      // from that edge, decaying into it.
      "  float into2 = max(-sd, 0.0);",
      "  col *= 1.0 - SHADE_FRONT_C * uGuardE * (1.0 - cov) * exp(-into2 / SHADE_REACH_C);",
      // And whatever stands above the waterline lies on top of the water, so the water takes a
      // shadow from the line downward.
      "  col *= 1.0 - SHADE_LINE_C * uGuardL * body * exp(-(dd * uRes.y) / LINE_REACH_C);",

      // THE COVERAGE LAW (§7). EVERY POINT OF THE FRAME IS THIS INSTRUMENT'S OWN PICTURE — above
      // the line one work's sky, below it one work's body under the other's folded reflection —
      // so there is no place where its matter is absent and the alpha is the constant 1. The
      // manifest's `coverage` block below says so, which is what makes this instrument lawful as
      // the lowest cue of a stack and never lawful laid over another.
      "  gl_FragColor = vec4(col, 1.0);",
      "}",
    ].join("\n")
      .replace(/SWAY_C/g, SWAY.toFixed(4))
      .replace(/RIP_C/g, RIP.toFixed(4))
      .replace(/DIE_W_C/g, DIE_W.toFixed(3))
      .replace(/SHADE_FRONT_C/g, SHADE_FRONT.toFixed(3))
      .replace(/SHADE_REACH_C/g, SHADE_REACH.toFixed(1))
      .replace(/SHADE_LINE_C/g, SHADE_LINE.toFixed(3))
      .replace(/LINE_REACH_C/g, LINE_REACH.toFixed(1))
      .replace(/DARK_BASE_C/g, DARK_BASE.toFixed(3))
      .replace(/DARK_DEEP_C/g, DARK_DEEP.toFixed(3))
      .replace(/HAZE_C/g, HAZE.toFixed(3));

    function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
    function smoothstep(a, b, x) {
      var t = (x - a) / (b - a);
      t = t < 0 ? 0 : t > 1 ? 1 : t;
      return t * t * (3 - 2 * t);
    }

    /* --- RESPONSE CURVES, MEASURED AND NOT NAMED (waterline.js:302-327) ------------------------
       One method for the dial and for every handle, the arsenal's own: how far the picture moves
       per unit of the RAW handle is measured with the curves taken out of the module — the judges'
       channel `raw` does exactly that — the rate is integrated, and the curve is the INVERSE of the
       integral, so the hand's own value is the share of the whole change. Each array below holds
       that inverse at twenty-one evenly spaced shares (how a table is read BETWEEN two of them is
       the block further down, and it is the port's own answer, not the module's).
       `lab/waterline-check.py --fit` wrote them; nothing here was typed by taste and the port
       re-derives nothing.

       DEAD BANDS of 0.055 at both ends of the dial: the hand is SPENT there, the dial stands at
       exactly its door across the band, and a whole work is whole to the pixel. */
    var DIAL_D0 = 0.055;
    var CURVES = {
      dial: [0, 0.063, 0.1182, 0.1817, 0.2459, 0.301, 0.356, 0.4088, 0.4694, 0.544, 0.5867, 0.6232,
             0.6576, 0.6936, 0.7323, 0.7762, 0.8268, 0.8733, 0.9087, 0.9489, 1],
      line: [0, 0.0593, 0.1201, 0.182, 0.2441, 0.3054, 0.3637, 0.4187, 0.4711, 0.5215, 0.57,
             0.6163, 0.6613, 0.7056, 0.7496, 0.7925, 0.8342, 0.8753, 0.9164, 0.9577, 1],
      depth: [0, 0.0399, 0.0793, 0.1178, 0.1557, 0.1935, 0.2318, 0.2709, 0.3111, 0.3526, 0.3957,
              0.4406, 0.4876, 0.5373, 0.59, 0.646, 0.7054, 0.7694, 0.8391, 0.9157, 1],
      swell: [0, 0.0498, 0.0994, 0.1489, 0.1983, 0.248, 0.2977, 0.3477, 0.3974, 0.4473, 0.4972,
              0.5473, 0.5974, 0.6477, 0.698, 0.7483, 0.7985, 0.8488, 0.8991, 0.9496, 1],
      lead: [0, 0.0791, 0.1554, 0.2281, 0.2976, 0.3649, 0.4288, 0.4866, 0.541, 0.5935, 0.6422,
             0.6876, 0.7296, 0.769, 0.8052, 0.839, 0.8704, 0.9006, 0.9296, 0.9599, 1],
      order: [0, 0.0311, 0.0664, 0.1034, 0.14, 0.1769, 0.2173, 0.2618, 0.3101, 0.3597, 0.4113,
              0.4627, 0.5162, 0.5697, 0.6218, 0.6719, 0.7253, 0.7814, 0.8442, 0.9206, 1]
    };

    // HOW A TABLE IS READ BETWEEN TWO OF ITS OWN POINTS (S-20, 2026-08-28). Not one number in the six
    // tables above moves here. What changed is the line drawn BETWEEN two of them.
    //
    // WHAT WAS WRONG WITH STRAIGHT LINES. Each curve's own VALUE was right at every knot and its
    // SPEED was a staircase: constant inside each share, and stepping at each of the nineteen joins
    // between them. The dial's own table steps hardest, from 1.676 of the dial a unit of the hand
    // down to 0.960 in one instant at its ninth join; the same step stands at the dead band's own
    // edge, where the dial is held perfectly still across the first DIAL_D0 of the hand and then
    // leaves at 1.416 a unit at once. Neither step is in the measurement: what
    // `lab/waterline-check.py --fit` integrated to write these tables is a smooth reading of how far
    // the picture travels, and a polyline through its samples invents corners the reading never had.
    //
    // THE SHAPE IS THE HOST'S OWN, and it is the same repair one layer down. `pass-layer.js`'s
    // `splineSlopes`/`splineAt` — Fritsch–Carlson, carried over unchanged — is what his word of
    // 2026-08-11 put on every score track after he judged speed steps at segment joints; a response
    // curve read as twenty separate lines is that same defect inside one handle. One curve through
    // all twenty-one points passes through every knot exactly, cannot overshoot or turn back (so each
    // curve stays monotone and both doors stand exactly where they stood), and rests at both its own
    // ends — so it leaves a dead band at rest instead of at a run, for the reason the host's own note
    // gives for its zero end tangents: the value is HELD either side, and a track rests where it is
    // held. The tangents are built once per table, the first time that table is read.
    var KNOT_TANGENTS = [];
    function tangentsOf(q) {
      var t, n, h, d, m, i, a, b, s;
      for (t = 0; t < KNOT_TANGENTS.length; t++) {
        if (KNOT_TANGENTS[t][0] === q) return KNOT_TANGENTS[t][1];
      }
      n = q.length; h = 1 / (n - 1); d = []; m = [];
      for (i = 0; i < n - 1; i++) d.push((q[i + 1] - q[i]) / h);
      for (i = 0; i < n; i++) m.push(i === 0 || i === n - 1 ? 0 : (d[i - 1] + d[i]) / 2);
      for (i = 0; i < n - 1; i++) {
        if (d[i] === 0) { m[i] = 0; m[i + 1] = 0; continue; }
        a = m[i] / d[i]; b = m[i + 1] / d[i];
        if (a < 0) { a = 0; m[i] = 0; }
        if (b < 0) { b = 0; m[i + 1] = 0; }
        s = a * a + b * b;
        if (s > 9) { s = 3 / Math.sqrt(s); m[i] = s * a * d[i]; m[i + 1] = s * b * d[i]; }
      }
      KNOT_TANGENTS.push([q, m]);
      return m;
    }
    function knots(q, u) {
      var x = clamp(u, 0, 1), n = q.length, h = 1 / (n - 1), m = tangentsOf(q);
      var i = Math.min(n - 2, Math.floor(x * (n - 1)));
      var s = (x - i * h) / h, s2 = s * s, s3 = s2 * s;
      return (2 * s3 - 3 * s2 + 1) * q[i] + (s3 - 2 * s2 + s) * h * m[i]
           + (3 * s2 - 2 * s3) * q[i + 1] + (s3 - s2) * h * m[i + 1];
    }
    // THE JUDGES' CHANNEL `raw` TAKES EVERY CURVE OUT, exactly as the module's own `curve`/`feel`
    // do. It is published as a handle rather than kept for a bench, because the curves above were
    // fitted from the rate measured through it and a rate nobody can re-measure is a number nobody
    // can check.
    function curveOf(name, u, raw) {
      return raw ? clamp(u, 0, 1) : knots(CURVES[name], u);
    }
    function feelOf(u, raw) {
      if (raw) return clamp(u, 0, 1);
      return knots(CURVES.dial, clamp((clamp(u, 0, 1) - DIAL_D0) / (1 - 2 * DIAL_D0), 0, 1));
    }

    // cover-fit a work into the frame, then pull in by the counter-motion's and the swell's own
    // headroom. The host hands the source's own dimensions, so the instrument never touches an
    // image object.
    function fit(iw, ih, w, h) {
      var fa = w / Math.max(h, 1);
      var ia = iw / Math.max(ih, 1);
      var sx, sy;
      if (ia > fa) { sx = fa / ia; sy = 1; } else { sx = 1; sy = ia / fa; }
      return [sx / ZOOM, sy / ZOOM, 0, 0];
    }

    /* WHERE A WORK'S OWN SEAM LANDS IN THE FRAME (waterline.js:419-426). `seam_y` is a place in the
       FILE; the frame shows the file cover-fitted and then pulled in by ZOOM, so the seam moves.
       This is that same map read backwards, and it is why the line's place is a derivation and
       never a number: change the crop and the line follows the picture.

       THE SEATING IS THE HOST'S OWN. `fy` is the y of the very `fit` the draw binds as `uFitA` /
       `uFitB`, handed to `frame()` on the buffer being drawn. The module read it off a canvas it
       owned; nothing else about the arithmetic moved. */
    function seamInFrame(seam, fy) {
      return clamp(0.5 + (clamp(seam, 0, 1) - 0.5) / Math.max(fy, 1e-4), 0.06, 0.94);
    }

    /* THE LINE'S TRAVEL, AND WHY THE CENTRE IS THE INSTANT OF THE EXCHANGE (waterline.js:428-454).
       The line stands at the departing work's own seam over the first LINE_HOLD of the dial,
       travels over the next stretch, and rests on the arriving work's seam over as much at the far
       end. The travel is bent — two pieces hinged at the dial's own middle — so that the share of
       the way it has come at the middle is exactly the share at which the line sits on 0.5.
       Whatever the two seams are, the line crosses the frame's centre at the mark where half the
       frame has changed hands. */
    /* The handle's lift is read AGAINST ITS OWN DEFAULT and not against the middle of its range:
       the response curve is fitted from the picture and need not send 0.5 back to 0.5, and a curve
       that did not would quietly carry the line off the seam it is derived from at the very setting
       the row calls its default. Written this way the lift is exactly nothing at the default
       whatever the curve turns out to be. */
    function liftOf(st) {
      var here = curveOf("line", clamp(st.line, 0, 1), st.raw);
      var rest = curveOf("line", 0.5, st.raw);
      return (here - rest) * 2 * LINE_LIFT;
    }

    function lineAt(d, st) {
      var la = seamInFrame(st.seamA, st.fitAy);
      var lb = seamInFrame(st.seamB, st.fitBy);
      var mid = 0.5;
      var span = lb - la;
      // THE HINGE. The share of the way come at the dial's own middle is exactly the share at which
      // the line sits on 0.5, so whatever the two seams are, the line crosses the frame's centre at
      // the mark where half the frame has changed hands.
      var wMid = Math.abs(span) < 1e-4 ? 0.5 : clamp((mid - la) / span, 0.02, 0.98);
      var ramp = 0.5 - LINE_HOLD;
      var s;
      if (d <= 0.5) s = wMid * smoothstep(0, 1, (d - LINE_HOLD) / ramp);
      else s = wMid + (1 - wMid) * smoothstep(0, 1, (d - 0.5) / ramp);
      return { L: clamp(la + span * s + liftOf(st), 0.10, 0.90), la: la, lb: lb, w: s };
    }

    // ---- THE DOOR THIS INSTRUMENT READS FOR ITSELF -----------------------------------------------
    // His 18:00 architecture decision, carried in the U27 brief: the instrument reads its doors at
    // runtime on the actual buffer, and the report it hands back is the runtime truth; what the
    // manifest declares is only the claim. The meshing instrument answered that in its own mask and
    // the material one in its own cells; this is the same law read in THIS instrument's own units,
    // which are the ladder's.
    //
    // WHAT A DOOR ASKS, WRITTEN OUT. At either door `uOpen` is 0, so the waterline stands at
    // BASE_OUT — below the bottom edge — every point of the frame is sky, the swell's waver is
    // nothing and `dL` with it. The field is then
    //     q  = 0.5·lead + sp·as,        sp = 1 − 0.5·lead,   as = (BASE_OUT − uv.y) / BASE_OUT
    //     qe = q·(1 + spread·(1 − DIE_W)) + spread·(0.4·R − 0.5),    R = the die, in [0, 1)
    // and `cov` is `clamp(0.5 + (tau − qe)/(grad·h))` with `grad = (1 + spread·(1−DIE_W))·sp/BASE_OUT`
    // and `h = 1/bufH`. So the mask crosses over inside a band of the field HALF THE FIELD'S OWN
    // SLOPE PER BUFFER POINT wide, and a door is whole exactly while that band falls outside the
    // range the field actually takes.
    //
    // THE TWO MARGINS, EXACTLY. `q` reaches 1 at the top of the frame — sp·1 + 0.5·lead is exactly 1
    // whatever the lead is — so at the exit door the margin comes out at exactly MARGIN, the
    // module's own +0.05 in `reach`, whatever the handles are. At the entry door it is that plus
    // `qMin·(1 + spread·(1−DIE_W))`, which is never less. So MARGIN is the number that makes the
    // dead bands dead, and the reading below is held against it.
    //
    // NOTHING HERE REFUSES, AND THAT IS SAID RATHER THAN LEFT AS AN OMISSION. Put the worst handles
    // in — spread at its widest and the lead shut — and the crossover is 0.5·1.66/BASE_OUT/bufH,
    // which stands under MARGIN on every buffer at least sixteen points tall. The host's buffer is
    // the CSS frame times the device ratio times its own resolution step and no browser hands a
    // frame that short, so there is no case to refuse and no hold to walk: this instrument's doors
    // are whole by construction on every buffer it can be drawn on. What is published is the
    // READING — the margin, the crossover and the grid both were taken on — so a person can check
    // that claim on the frame in front of them rather than take it on trust.
    function doorGridOf(st) {
      var bw = Math.round(st.bufWidth), bh = Math.round(st.bufHeight);
      if (bw >= 1 && bh >= 1) return { w: bw, h: bh, drawn: true };
      return { w: Math.round(st.cssWidth), h: Math.round(st.cssHeight), drawn: false };
    }

    function doorReadOf(v, st) {
      var want = st.mix === 0 ? 1 : (st.mix === 1 ? 0 : -1);
      if (want < 0) return null;
      var g = doorGridOf(st);
      if (!(g.w >= 1) || !(g.h >= 1)) return null;
      var sp = 1 - 0.5 * v.lead;
      var steep = 1 + v.spread * (1 - DIE_W);
      // the smallest the ladder reads anywhere on the frame, at its own bottom row
      var qMin = 0.5 * v.lead + sp * ((BASE_OUT - 1) / BASE_OUT);
      var margin = want ? qMin * steep + MARGIN : MARGIN;
      var slope = steep * sp / BASE_OUT;
      return { grid: g, want: want, slope: slope, margin: margin,
               // half the mask's own crossover, in the field's own units, on THIS buffer
               cross: 0.5 * slope / g.h };
    }

    // THE REFUSAL, worded the way the host's own manifest refusals read: what is wrong, in this
    // instrument's own measured numbers, on the grid it was measured on (Phase 7, item 5 — this
    // instrument carried the measurement above, `doorReadOf`, and a bare boolean, `doorWhole`, but no
    // `doorWhyNo` string: every other instrument in the fleet turns its own door reading into a
    // refusal a bench or a suite can read, and this file never did. The comment above `doorGridOf`
    // already proves the case never fires on any buffer a browser hands out — this function is that
    // proof made into code, so a future change that DOES let the crossover past its own margin reds
    // here rather than passing silently for want of anywhere to say so).
    function doorWhyNoOf(read) {
      if (!read || read.cross <= read.margin) return null;
      var g = read.grid, door = read.want ? "the entry" : "the exit";
      var work = read.want ? "departing" : "arriving";
      return door + " door leaks: on a " + g.w + " x " + g.h + (g.drawn ? " buffer" : " frame")
           + " the field's own steepest slope is " + read.slope.toFixed(4) + ", so the tide's own "
           + "mask crosses over inside " + read.cross.toFixed(4) + " of the field against the "
           + read.margin.toFixed(4) + " its own margin leaves at a door, and the waterline is drawn "
           + "across the " + work + " work's own frame, where " + door + " door's own law asks for "
           + "that work whole, no line drawn across it";
    }

    // THE NUMBERS OF ONE FRAME (waterline.js:456-484). Everything the shader gets beyond the seating
    // of the two works is a pure function of the pose, and the door reading rides beside them.
    function values(st) {
      var raw = clamp(Number(st.raw) || 0, 0, 1);
      var d = feelOf(Number(st.mix) || 0, raw);
      var pose = { seamA: st.seamA, seamB: st.seamB, fitAy: st.fitAy, fitBy: st.fitBy,
                   line: st.line, raw: raw };
      var ln = lineAt(d, pose);
      // 1.10 and not the 0.62 this handle first carried: measured with the curves out of the way, a
      // spread of 0.62 moved the picture by two channels across the handle's whole range — a handle
      // whose doors a check cannot tell apart is not a handle.
      var spread = curveOf("order", clamp(st.order, 0, 1), raw) * SPREAD_MAX;
      // The threshold's own reach: past the field's range by half the spread and MARGIN more, so at
      // a door EVERY patch stands whole on the same side.
      var reach = 0.5 * spread + MARGIN;
      var swell = curveOf("swell", clamp(st.swell, 0, 1), raw);
      // The water rises into the frame and drains out of it again, so a door is the work the file
      // carries and not a work with a horizon drawn across it.
      var open = smoothstep(0, OPEN_IN, d) * smoothstep(1, 1 - OPEN_IN, d);
      // and the two shadows' gate, widest in the middle and nothing at either door
      var guard = clamp(st.shade, 0, 1)
                * smoothstep(0, GUARD_IN, d) * smoothstep(1, 1 - GUARD_IN, d);
      // THE TIDE'S OWN PATCH SIZE, both counts carried together so the module's own proportion
      // stands at every setting. The handle's middle is exactly 1, so the frame the module draws is
      // the frame this draws at the middle, to the digit.
      var cell = Math.pow(2, (2 * clamp(st.tideCells, 0, 1) - 1) * CELL_SPAN);
      var v = {
        dial: d,
        line: ln.L, lineA: ln.la, lineB: ln.lb, way: ln.w,
        tau: -reach + (1 + 2 * reach) * d,
        lead: curveOf("lead", clamp(st.lead, 0, 1), raw),
        spread: spread,
        dep: DEP_LO + (DEP_HI - DEP_LO) * curveOf("depth", clamp(st.depth, 0, 1), raw),
        swell: swell,
        comb: swell * clamp(st.comb, 0, 1),
        open: open,
        cells: [CELLS_X * cell, CELLS_Q * cell],
        // THE COUNTER-MOTION, widest in the middle and nothing at either door. AMP is how far it
        // reaches at its widest and stays pinned, because the cover crop is derived from it; what
        // travels is the SHARE of that reach the pair asks for, which is the `settle` handle. The
        // judges' `travel` channel stands beside it and rests at 1, the way the fleet holds it.
        off: AMP * 4 * d * (1 - d) * clamp(st.travel, 0, 1) * clamp(st.settle, 0, 1),
        guardE: guard * clamp(st.shadeEdge, 0, 1),
        guardL: guard * clamp(st.shadeLine, 0, 1),
        // THE MODULE'S OWN CLOCK, WHICH IS THE HOST'S. Every motion of the water is a pure function
        // of the second handed in, so a seeded score repeats to the pixel. Reduced motion stands the
        // second still and stops nothing else.
        time: st.reduced ? 0 : (Number(st.t) || 0)
      };
      var read = doorReadOf(v, st);
      v.doorGrid = read ? read.grid : null;
      v.doorMargin = read ? read.margin : null;
      v.doorCross = read ? read.cross : null;
      v.doorWhole = read ? read.cross <= read.margin : null;
      v.doorWhyNo = doorWhyNoOf(read);
      return v;
    }

    var manifest = {
      id: "waterline", api: 1, arity: 2,
      // The module's own header ties it to the release envelope's disassembly–mystery–reassembly
      // class: one work sinks under a rising horizon while the other rises out of its own
      // reflection, and the middle is a frame holding both at once.
      roles: ["disassembly", "mystery", "assembly"],
      // READ OFF THE MODULE'S OWN CONSTRUCTION, and said to be derived. Neither module-contract file
      // carries a `waterline` row, so the two levels below come from the header of
      // lab/effects/waterline.js:
      //   · WORLD — «the fold stops being a fold and becomes a waterline — sky above, its mirrored
      //     mass below, and the work becomes a landscape» (:5-7), and «The waterline is a real
      //     horizon, so the crossing travels through it» (:13-14). What changes is the world the
      //     frame stands in, not a cut inside it.
      //   · SURFACE — one water surface runs across the frame and everything under it is read
      //     through that one carrier: «ONE SURFACE COMBS BOTH: the same swell displaces whatever
      //     lies under the water, so the two works are held by one carrier and not by two» (:196-197).
      // The staged row in lab/data/fix-waterline.json reads «WORLD+SURFACE», which is the same two.
      levels: ["WORLD", "SURFACE"],
      // WHAT THIS INSTRUMENT CUTS ON. The waterline parts the frame into two BANDS — the sky and the
      // water — and the crossing travels through the line between them: what the eye follows is that
      // one horizontal boundary sweeping the frame while each band changes hands on its own
      // schedule. No other element kind is cut here: no tile, no wedge, no ring, no region.
      cuts: ["band"],
      // WHERE THIS INSTRUMENT HAS A SEAM (§8's `seams` block). The boundary between the two bands is
      // `cov = clamp(0.5 + sd, 0.0, 1.0)` with `sd = (uTau - qe) / (grad * h)`, `h = 1 / bufH` — the
      // shader's own words above it say exactly what this is: "COVERAGE OVER THE PIXEL'S OWN
      // FOOTPRINT, from the field's own gradient — the boundary is a side, not a blend, and it is one
      // pixel wide wherever it runs." A HAIRLINE retouch and not a deliberate cross-fade: the tide's
      // own raggedness (`uSpread`, the die) moves WHERE the line runs, never how WIDE the crossover
      // is, so `of` names no handle — the width is fixed at one buffer point regardless of how ragged
      // the shore reads or how many patches the die scatters.
      seams: [{ kind: "line", of: null, unit: "points of the drawing buffer" }],
      params: { line: [0, 1], depth: [0, 1], swell: [0, 1], lead: [0, 1], order: [0, 1],
                settle: [0, 1], tideCells: [0, 1] },
      // THE TWO THE PORT PUBLISHES THAT THE MODULE HELD AS CONSTANTS, and why each is a handle. His
      // 15:13 word of 2026-08-18 bans a static transition, and his 19:13 word lifted to the class at
      // 19:21 makes the derivation the law: a geometric or temporal number the works' own records
      // could set is a parameter, not a constant. Both below stand at exactly the module's own
      // number at their own default, so the frame the module draws is the frame this draws.
      //   · `settle` — THE SHARE OF THE COUNTER-MOTION the pair asks for. The module carries the
      //     counter-motion at AMP alone (waterline.js:481), and the only handle over it is the
      //     judges' `travel`, which rests at 1 — so before this the departing work settled and the
      //     arriving one rose by one and the same distance for every pair in the world. AMP itself
      //     stays pinned and is named below, because the cover crop is DERIVED from it and a crop
      //     that moved with the pose could not be published once in `framings`.
      //   · `tideCells` — THE TIDE'S OWN PATCH SIZE, the module's CELLS_X and CELLS_Q carried
      //     together in octaves about its own 19 and 8. A cell across the frame's height is exactly
      //     what a work's own spectral period measures, so this is the one number here whose unit
      //     matches a record's without anything standing between them.
      //
      // WHAT STAYS PINNED, AND WHY EACH DOES — so the sweep is on the record rather than only its
      // findings. AMP 0.055 and RIP 0.020 are the two the crop is derived from; RIP and SWAY 0.005
      // already reach the picture through a MEASURED handle, since the shader scales both by `uSway`
      // and `uComb`, which are the `swell` handle. DIE_W 0.40 is how much of the handover is the die
      // rather than the ladder, and the die's own spread is already the `order` handle. SHADE_FRONT
      // 0.30, SHADE_LINE 0.26 and their reaches of 6 and 10 points, and DARK_BASE 0.05, DARK_DEEP
      // 0.16 and HAZE 0.12, are how deep a contact shadow bites and how the water darkens with
      // depth: nothing in a work's record measures a lighting fact, and reading them off the tonal
      // ladder would be an invented mapping rather than a derivation. LINE_LIFT 0.15 bounds a handle
      // that reads nothing by design. LINE_HOLD 0.22, OPEN_IN 0.12 and GUARD_IN 0.10 are shares of
      // the DIAL — the passage's own schedule, which is the transaction's and no photograph's, the
      // same tag the register already gives a floor's turn and an arrival's choice. DEP_LO/DEP_HI,
      // SPREAD_MAX and CELL_SPAN are the published spans of handles that ARE measured. MARGIN 0.05
      // and BASE_OUT 1.04 are the door's own construction. The swell's wave numbers are the water's
      // own carrier rather than the picture's, and the module's whole claim is that ONE surface
      // combs both works — driving its wavelength from a photograph would say the water is made of
      // that photograph, which the module does not claim and this port will not add.
      // EVERY handle a score can drive (§4.4b). `mix` is the dial and `clock` is the second the host
      // hands down; the five below them are the module's declared params; `seed` is its die; and
      // `shade`, `shadeEdge`, `shadeLine`, `travel`, `comb` and `raw` are the six channels the module
      // keeps for measuring a law on the picture, resting where the module rests them.
      //
      // NO HANDLE HERE KEEPS A CLOCK OF ITS OWN. The module ran its water on its own accumulating
      // frame time (waterline.js:562-569); every wave train here reads the `clock` handle through
      // `values`, so a seeded score repeats to the pixel.
      //
      // TWO SHADOW CHANNELS AND NOT ONE, carried over with the module's own reason: this module has
      // two edges where one thing lies on top of another — the arriving work's own front, and the
      // waterline with the standing world above it — and one handle over both cannot prove either.
      // A spoiling that took the front's shadow out left the law green on the waterline's alone,
      // measured 2026-08-13 (waterline.js:638-642).
      //
      // THE TWO THAT CARRY THE PAIR'S OWN MEASUREMENTS. `seamA` and `seamB` are the two works' OWN
      // measured mirror lines — `seam_y`, a place down the FILE — which the module is handed at
      // creation and reads out of the project's own motif measure. This file may read no file, so
      // each arrives as a handle a score row drives, and `seamInFrame` above carries it into the
      // frame through the seating the host applied.
      //
      // THEIR DEFAULT IS THE MODULE'S OWN FALLBACK. Handed no measured seam the module stands the
      // line at the centre of the frame and says so in the judges' notes (waterline.js:375-381);
      // 0.5 is that centre. A pair carrying no measured seam therefore still plays, with the line
      // standing where the frame's own middle is — which is why nothing here refuses such a pair.
      //
      // NOTE ON THE NAME, since the drifting instrument publishes handles called `seamA`/`seamB`
      // too: those carry `seam_horizon`, how STRONGLY a work reads a waterline, and these carry
      // `seam_y`, WHERE that line sits. Two different numbers of one measure, in two instruments'
      // own namespaces.
      handles: {
        // `mix` is the crossing's own dial and `clock` the module's own time; neither drives a
        // structural level of the picture.
        // THE KNOTS ON THE MANIFEST (Phase 7, item 3a): the same twenty-one points `feelOf` reads,
        // published where a bench can find them without reading the source, so the roll call needs
        // no hand-typed map of which file's own table answers which handle.
        mix: { min: 0, max: 1, def: 0, level: null,
               curve: { knots: CURVES.dial, band: DIAL_D0, applied: true } },
        clock: { min: 0, max: 14, def: 0, level: null },
        // The waterline is the world's own horizon: where its axis stands.
        line: { min: 0, max: 1, def: 0.5,
                // WHAT THIS HANDLE IS READ AGAINST, published beside its range the way the meshing
                // and the material instruments publish their own: the lift is taken against the
                // handle's OWN default rather than against the middle of its range, so at the
                // default the waterline stands exactly on the seam it is derived from whatever the
                // measured curve turns out to be.
                applied: { liftAgainst: "its own default", reach: LINE_LIFT,
                           measures: "the departing work's own measured seam, carried into the "
                                   + "frame through the seating the host applied" },
                level: "WORLD" },
        // How near the eye stands to the water's own reflection: the mirror's fold density is a
        // reading of the world's own depth.
        depth: { min: 0, max: 1, def: 0.3, level: "WORLD" },
        // The one surface that combs both works (this file's own note above the `handles` map).
        swell: { min: 0, max: 1, def: 0.45, level: "SURFACE" },
        // Which band of the world — sky or water — hands over first.
        lead: { min: 0, max: 1, def: 0.62, level: "WORLD" },
        // The shoreline's own raggedness, a property of the one water surface rather than of
        // either photograph.
        order: { min: 0, max: 1, def: 0.2, level: "SURFACE" },
        // The two the port publishes; the block above this `handles` map says why each is one.
        // `settle` rests at 1, which is the whole of the counter-motion the module carries, and
        // `tideCells` at its own middle, which is exactly the module's 19 and 8.
        //
        // `settle` is the counter-motion's own share — a drift of the picture taken as one, which
        // is SURFACE. `tideCells` is honestly a CELL reading — the tide's own patch count — but
        // CELL is not in this instrument's own `levels` array, so it falls back to SURFACE, the
        // nearest declared level and the one that already carries the water's own shore texture.
        settle: { min: 0, max: 1, def: 1, level: "SURFACE" },
        tideCells: { min: 0, max: 1, def: 0.5,
                     applied: { octavesEitherSide: CELL_SPAN, aboutCells: [CELLS_X, CELLS_Q],
                                measures: "a cell across the frame's height, which is the unit a "
                                        + "work's own measured spectral period is read in" },
                     level: "SURFACE" },
        seed: { min: 0, max: 8, def: 0, level: null },
        // `shade`, `shadeEdge` and `shadeLine` are the fleet's shade judge channel, split into its
        // two gates so a check can measure each contact shadow independently (the block above this
        // `handles` map, "TWO SHADOW CHANNELS AND NOT ONE"); `travel` is the fleet's own travel
        // judge channel. None of the four drives a structural level.
        shade: { min: 0, max: 1, def: 1, level: null },
        shadeEdge: { min: 0, max: 1, def: 1, level: null },
        shadeLine: { min: 0, max: 1, def: 1, level: null },
        travel: { min: 0, max: 1, def: 1, level: null },
        // How hard the one surface's own swell combs what lies under it.
        comb: { min: 0, max: 1, def: 1, level: "SURFACE" },
        // Takes every response curve out for measurement; it drives no structural level of its own.
        raw: { min: 0, max: 1, def: 0, level: null },
        // The measured input the world's own horizon line is built from.
        seamA: { min: 0, max: 1, def: 0.5, level: "WORLD" },
        seamB: { min: 0, max: 1, def: 0.5, level: "WORLD" },
      },
      // The dial's two ends. At 0 the water stands below the bottom edge of the frame, the threshold
      // stands MARGIN below everything the field reads, both contact shadows and the counter-motion
      // are exactly nothing, and the frame is the departing work the file carries. At 1 the same,
      // the other way about. Neither is published in either module-contract file, which carries no
      // `waterline` entry — both are read off the module's own geometry and the rows measure them.
      neutrals: { a: 0, b: 1 },
      doors: { in: { handle: "mix", value: 0, work: "a" },
               out: { handle: "mix", value: 1, work: "b" } },
      // Both doors frame alike: the crop the counter-motion's and the swell's headroom are paid for
      // with is a constant, while both travels die at either end.
      framings: { "0": { coverCrop: ZOOM }, "1": { coverCrop: ZOOM } },
      surface: { type: "shoreline-reflection-field", anchor: "measured-hang",
                 tessellation: { bands: 2, tideCells: "tideCells" }, cameraAuthority: "stage",
                 entry: { mix: 0, work: "a", pose: "flat" },
                 exit: { mix: 1, work: "b", pose: "flat" } },
      drivers: ["progress", "cueProgress", "time", "velocity", "capability", "noise", "static",
                "curve", "spline", "map", "add", "multiply", "mix", "clamp", "hold", "segment",
                "ramp", "slew", "oscillate", "node"],
      // The construction moves no point of view: it draws a horizon on its own surface and folds one
      // work about it. That is what it does to its own surface, so the witness camera stays the
      // stage's (§6).
      camera: { needs: "none", authority: "stage" },
      gl: { preserveDrawingBuffer: false },
      // THE COVERAGE LAW (§7). Every point of the frame is written with picture — one work's sky
      // above the line, one work's own body under the other's folded reflection below it — so this
      // instrument has no place where its own matter is absent and the alpha is the constant 1.
      // Both doors are one whole work by the same construction: the travelling threshold stands
      // MARGIN outside everything the field reads at either end, so no patch of the far work stands
      // anywhere.
      coverage: { writes: false,
                  how: "the frame is parted into two bands and both are picture at every point, so "
                     + "the alpha is the constant 1; at a door the instrument reads its own field's "
                     + "crossover against the margin the threshold stands beyond that field, on the "
                     + "buffer being drawn, and publishes both" },
      // The neutral pose is the ENTRY DOOR — `mix` at 0, the value the `doors` block above names —
      // so the frame keys the host reads off it at registration include the door's own record. The
      // two seatings rest at a square work in a square frame, which is what `fit` returns for one.
      neutralPose: { mix: 0, line: 0.5, depth: 0.3, swell: 0.45, lead: 0.62, order: 0.2,
                     settle: 1, tideCells: 0.5,
                     seed: 0, shade: 1, shadeEdge: 1, shadeLine: 1, travel: 1, comb: 1, raw: 0,
                     seamA: 0.5, seamB: 0.5, t: 0, reduced: false,
                     cssWidth: 1000, cssHeight: 1000, fitAy: 1 / ZOOM, fitBy: 1 / ZOOM },
      passes: [{
        program: "waterline", vert: VERT, frag: FRAG, position: "aPos",
        uniforms: [
          { name: "uA", type: "sampler2D", source: "textureA" },
          { name: "uB", type: "sampler2D", source: "textureB" },
          { name: "uFitA", type: "vec4", source: "fitA" },
          { name: "uFitB", type: "vec4", source: "fitB" },
          { name: "uRes", type: "vec2", source: "resolution" },
          { name: "uLine", type: "float", source: "frame:line" },
          { name: "uOpen", type: "float", source: "frame:open" },
          { name: "uTau", type: "float", source: "frame:tau" },
          { name: "uLead", type: "float", source: "frame:lead" },
          { name: "uSpread", type: "float", source: "frame:spread" },
          { name: "uDep", type: "float", source: "frame:dep" },
          { name: "uSway", type: "float", source: "frame:swell" },
          { name: "uComb", type: "float", source: "frame:comb" },
          { name: "uCells", type: "vec2", source: "frame:cells" },
          { name: "uTime", type: "float", source: "frame:time" },
          { name: "uOff", type: "float", source: "frame:off" },
          { name: "uGuardE", type: "float", source: "frame:guardE" },
          { name: "uGuardL", type: "float", source: "frame:guardL" },
          { name: "uSeed", type: "float", source: "handle:seed" },
        ],
      }],
      // The instrument allocates nothing of its own: it spends the two source-texture slots the host
      // already holds and the one programme the host builds from this manifest.
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
                   programs: 1, passes: 1, bytesEstimate: 2000100, variant: "lean" },
                   standard: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0,
                               programs: 1, passes: 1, bytesEstimate: 8000100,
                               variant: "standard" },
                   rich: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                           passes: 1, bytesEstimate: 32000100, variant: "rich" } },
      capabilities: ["webgl2"],
      decline: ["one work only", "a source that never decoded"],
      provenance: { labPath: "lab/effects/waterline.js", commit: "60ef8f3",
                    sha256: "90750f44b66d33e34a7c449394a7739e3a38c85528d2726d57f75edd016ea38d" },
      // HOW WELL THIS INSTRUMENT SUITS A PAIR (2026-08-18, his word of 09:51 and its sharpening at
      // 09:53). An instrument no longer answers WHETHER it takes a pair — it answers how well it
      // suits one, so a poor fit is still playable and still explains itself. The arithmetic runs in
      // the composer, which is the one place holding both records; what stands here is the
      // instrument's own statement of WHAT IT READS, which is the fact this file owns.
      //
      // RANKING ONLY, AND NEVER A FLOOR. A pair whose works carry no measured waterline at all still
      // plays: the line then stands where the frame's own middle is — the module's own fallback —
      // and the crossing runs there. That is a fit of nothing, which ranks last and plays where
      // nothing ranks higher; it is never a refusal.
      suits: { reads: ["motifs.measured", "structure.horizon.y"],
               how: "it parts the frame at a line each work measured for itself and travels the "
                  + "crossing through that line, so it suits a pair whose works plainly carry their "
                  + "own waterline — the weaker of the two readings is the fit, because the line has "
                  + "to leave one measured seam and land on another — and a pair carrying no seam "
                  + "at all is a fit of nothing rather than a refusal: the line stands where the "
                  + "frame's own middle is and the crossing plays there",
      },
      readiness: "production-ready",
    };

    var live = false;
    return {
      name: "waterline",
      manifest: manifest,
      values: values,
      fit: fit,
      feel: function (u) { return feelOf(u, 0); },
      // WHAT THIS INSTRUMENT'S `feel` PROMISES (Phase 7, item 3b): monotone, door to door.
      feelClass: "monotone",
      prepare: function (o) {
        if (!o.sources) return { take: false, why: "the waterline instrument needs both works" };
        if (!o.cue) return { take: false, why: "no cue names it" };
        return { take: true };
      },
      start: function () { live = true; },
      // The pose the shader draws. Every number in it comes from a handle a score can drive, and
      // every motion of the water reads the second the host hands down, so a seeded run repeats to
      // the pixel.
      //
      // THE REDRAW THE PRESERVED BUFFER STOOD IN FOR. The lab module drew on a parameter change, on
      // a resize and on its own frame loop, and under reduced motion it drew once and stopped —
      // whatever stayed on screen after that was the preserved buffer's doing. Here the host's
      // buffer keeps nothing between frames, so this draws on every frame it is handed, reduced or
      // not.
      frame: function (st) {
        if (!live) return;
        var h = st.handles;
        var pose = {
          mix: h.mix, line: h.line, depth: h.depth, swell: h.swell, lead: h.lead, order: h.order,
          settle: h.settle, tideCells: h.tideCells,
          shade: h.shade, shadeEdge: h.shadeEdge, shadeLine: h.shadeLine,
          travel: h.travel, comb: h.comb, raw: h.raw,
          seamA: h.seamA, seamB: h.seamB, seed: h.seed,
          t: h.clock, reduced: st.reduced,
          cssWidth: st.viewport.w, cssHeight: st.viewport.h,
          // THE GRID THE SHADER WILL SAMPLE ON, carried into the pose so the door is read on the
          // buffer the host is about to bind as `uRes` rather than on the CSS frame around it.
          bufWidth: st.viewport.bufferW, bufHeight: st.viewport.bufferH,
          // BOTH WORKS' SEATING ON THAT BUFFER, which only the host can answer, taken through the
          // same `fit` the draw calls. The waterline's whole derivation stands on it.
          fitAy: st.fitA ? st.fitA[1] : 1 / ZOOM,
          fitBy: st.fitB ? st.fitB[1] : 1 / ZOOM,
        };
        // AT A DOOR THE INSTRUMENT SAYS WHAT IT READ. The reading is taken on the buffer this frame
        // is drawn on, so it is the run-time truth his 18:00 decision asks for. Nothing is held back
        // and nothing is refused — see the door reading's own note above for why there is no case to
        // refuse — so `applied` is the line the frame was posed on and `whyNo` is always null.
        if (h.mix === 0 || h.mix === 1) {
          var v = values(pose);
          if (st.reportApplied) {
            st.reportApplied({
              door: h.mix === 0 ? "in" : "out",
              buffer: [pose.bufWidth, pose.bufHeight],
              reads: "the field's own crossover against the margin the threshold stands beyond it",
              request: v.doorMargin, applied: v.doorCross,
              moved: 0, unit: "the field's own units",
              held: null, whyNo: null,
            });
          }
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
    instrument: waterlineInstrument(),
  });
})();
