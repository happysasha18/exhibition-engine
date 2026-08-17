/*!pass-inst-matter.js*/
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

  // ================================================================================================
  // THE MATTER INSTRUMENT (§8) — lab/effects/matter.js carried across
  // ================================================================================================
  // What the visitor sees: the departing work loosens into a material — grain dragged along a seeded
  // field — and the arriving work condenses out of that same material. A band of loosened matter
  // travels across the frame with one work whole ahead of it and the other whole behind. It stands
  // beside the woven instrument because it carries disassembly and assembly, which the woven one
  // does not.
  //
  // What came over: the shader, the seating of a work in the frame (fit), the response curve (feel),
  // the field constants and the numbers of one frame (values). Not one number changed.
  //
  // What stayed behind: its own canvas, its own WebGL 1 context, its own frame loop, its resize
  // listener and its own accumulated clock. The instrument here reads no wall clock, holds no
  // listener, creates no context and loads no picture (§1.2's fence).
  //
  // THREE THINGS THE PORT HAD TO ANSWER, named in the module's own card
  // (docs/immersive/effects/matter.md §11):
  //   · THE UNIFORM SET. The lab carrier's draw call names one instrument's six uniforms literally,
  //     and nine of this module's fourteen have no place in that list. The host binds by the name
  //     each uniform declares in the manifest below, so the set is the instrument's own.
  //   · THE PRESERVED DRAWING BUFFER. The module asks its own context for one (matter.js:250), and
  //     §7 refuses a manifest that asks for it. What the flag stood in for is a redraw: the module
  //     draws on demand — from onParam, from resize — and between two such draws the browser has to
  //     hand back the frame that was already there. The host draws every frame of a running
  //     transaction and redraws on every resize, so the frame the compositor shows is one this
  //     instrument drew for it. The row «no empty frame at any sampled instant» measures that,
  //     across a resize as well as across the pass.
  //   · THE VERSION HEADER. This module's shader carries none, so the host's translator stamps the
  //     one it needs and no second one arrives.
  //
  // ASPECT. The module reads the frame's aspect from a uniform of its own that the host does not
  // supply. It is the ratio of the two numbers the host already binds as `resolution`, so it is
  // computed from those inside the shader and every use of it reads the same number as before.
  function matterInstrument() {
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
      "uniform float uGrainA;",      // the coarse grain of the material, cells per frame height
      "uniform float uGrainB;",      // and the fine grain over it
      "uniform vec2 uDrift;",        // where the material has drifted to, in cells
      "uniform float uLadder;",      // how much of the field is the plain ladder across the frame
      "uniform float uTau;",
      "uniform float uLoosen;",      // how far the picture is dragged, frame heights
      "uniform float uGather;",      // how wide the loosened band is, in field units
      "uniform float uSeed;",
      "uniform float uGuard;",
      "float h11(vec2 i){ return fract(sin(dot(i, vec2(41.317, 289.107)) + uSeed) * 43758.5453); }",
      // value noise with its own exact gradient: the material's grain, and the direction it drags
      "vec3 vnoise(vec2 p){",
      "  vec2 i = floor(p), f = fract(p);",
      "  float a = h11(i), b = h11(i + vec2(1.0, 0.0));",
      "  float c = h11(i + vec2(0.0, 1.0)), d = h11(i + vec2(1.0, 1.0));",
      "  vec2 u = f * f * (3.0 - 2.0 * f);",
      "  vec2 du = 6.0 * f * (1.0 - f);",
      "  float k = a - b - c + d;",
      "  float v = a + (b - a) * u.x + (c - a) * u.y + k * u.x * u.y;",
      "  float vx = ((b - a) + k * u.y) * du.x;",
      "  float vy = ((c - a) + k * u.x) * du.y;",
      "  return vec3(v, vx, vy);",
      "}",
      "vec2 into(vec2 p, vec4 f){",
      "  return clamp((p - 0.5) * f.xy + 0.5 + f.zw, 0.0008, 0.9992);",
      "}",
      "void main(){",
      "  vec2 uv = vUv;",
      "  float aspect = uRes.x / max(uRes.y, 1.0);",
      "  vec2 p = vec2(uv.x * aspect, uv.y);",
      "  float h = 1.0 / max(uRes.y, 1.0);",
      // THE FIELD: two grains of matter over a plain ladder across the frame. The ladder gives the
      // crossing its direction, the grain gives it its material.
      "  vec3 n1 = vnoise(p * uGrainA + uDrift);",
      "  vec3 n2 = vnoise(p * uGrainB - uDrift * 1.7);",
      "  float ladder = uv.x;",
      "  float F = uLadder * ladder + (1.0 - uLadder) * (0.62 * n1.x + 0.38 * n2.x);",
      "  vec2 gF = vec2(uLadder / max(aspect, 0.05), 0.0)",
      "          + (1.0 - uLadder) * (0.62 * n1.yz * uGrainA + 0.38 * n2.yz * uGrainB);",
      "  float grad = max(length(gF), 1e-5);",
      "  float d = (F - uTau) / (grad * h);",
      "  float cov = clamp(0.5 + d, 0.0, 1.0);",
      // THE LOOSENING. Strongest at the front — where the field stands nearest the threshold — and
      // gone on both sides of it, so a band of loose matter travels and the rest of the frame is the
      // picture standing still. The drag runs along the field's own gradient, and across it the two
      // works are dragged against each other.
      "  float near = exp(-((F - uTau) * (F - uTau)) / max(uGather * uGather, 1e-6));",
      "  vec2 flow = gF / grad;",
      "  vec2 across = vec2(-flow.y, flow.x);",
      "  vec2 pull = (flow * (0.6 + 0.4 * n1.x) + across * 0.8) * uLoosen * near;",
      "  vec2 pullA = vec2(pull.x / max(aspect, 0.05), pull.y);",
      "  vec2 pullB = vec2((flow.x * (0.6 + 0.4 * n2.x) - across.x * 0.8) / max(aspect, 0.05),",
      "                    flow.y * (0.6 + 0.4 * n2.x) - across.y * 0.8) * uLoosen * near;",
      "  vec3 colA = texture2D(uA, into(uv + pullA, uFitA)).rgb;",
      "  vec3 colB = texture2D(uB, into(uv + pullB, uFitB)).rgb;",
      "  vec3 col = mix(colB, colA, cov);",
      "  col *= 1.0 - 0.32 * uGuard * cov * exp(-max(d, 0.0) / 7.0);",
      // THE COVERAGE LAW (§7). `cov` is 1 where the point still stands on work A's side of the
      // travelling threshold and 0 where the front has passed it, so `1.0 - cov` is the territory
      // the ARRIVING work has taken — this instrument's own matter. Work B then grows out of the
      // frame beneath it rather than being pasted over it, which is what lets an arrival be carried.
      //
      // ONE THING IS LOST HERE AND IS RECORDED RATHER THAN HIDDEN: the contact shadow on the line
      // above rides `cov`, so it stands on the side this alpha clears and is discarded wherever a
      // cue plays beneath. The meshing instrument's shadow rides `(1.0 - cov)` and survives. Casting
      // a shadow onto what plays underneath would need a multiply blend, which would let one cue
      // darken another — an imposed weight by another road, which the charter bans as a class.
      "  gl_FragColor = vec4(col, 1.0 - cov);",
      "}",
    ].join("\n");

    function smoothstep(a, b, x) {
      var t = (x - a) / (b - a);
      t = t < 0 ? 0 : t > 1 ? 1 : t;
      return t * t * (3 - 2 * t);
    }
    function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }

    // HOW COARSE THE MATERIAL IS, in cells across the frame's height, at either end of the `grain`
    // handle (matter.js:191). The fine grain rides at three times the coarse one, which is what
    // gives the front its crumb.
    var GRAIN_MIN = 4, GRAIN_MAX = 34, GRAIN_FINE = 3.0;
    // How far the picture is dragged at the fullest loosening, in frame heights, and the crop that
    // pays for it (matter.js:195-196). ZOOM is derived from AMP and is no free number.
    var AMP = 0.07, ZOOM = 1 + 2 * AMP + 0.03;
    // Six parts plain ladder against four parts grain (matter.js:205). At four parts ladder the
    // field has no direction, the loosened band is the whole frame, and the picture reads as marble.
    var LADDER = 0.6;

    // cover-fit a work into the frame, then pull in by the drag's own headroom. The host hands the
    // source's own dimensions, so the instrument never touches an image object.
    function fit(iw, ih, w, h) {
      var fa = w / Math.max(h, 1);
      var ia = iw / Math.max(ih, 1);
      var sx, sy;
      if (ia > fa) { sx = fa / ia; sy = 1; } else { sx = 1; sy = ia / fa; }
      return [sx / ZOOM, sy / ZOOM, 0, 0];
    }

    // THE RESPONSE CURVE, MEASURED (matter.js:267-307, the module's re-fit of 2026-08-13): equal
    // movements of the hand, equal felt change. The rate of change of the picture per unit of the
    // raw threshold was measured with the curve taken out, that rate integrated, and this is the
    // inverse of the integral at twenty-one evenly spaced shares with straight lines between them.
    // The two-piece logarithm the module carried before it cannot hold this handle: the field's own
    // values crowd the middle and thin to nothing at both ends, so the curve stands nearly vertical
    // at both ends and nearly flat across the middle. Carried here digit for digit; the port
    // re-derives nothing.
    var FEEL_D0 = 0.05;
    var FEEL_Q = [0, 0.1994, 0.2488, 0.2852, 0.3168, 0.3454, 0.372, 0.3972, 0.4215, 0.4454,
                  0.469, 0.4925, 0.5162, 0.5405, 0.5657, 0.5923, 0.621, 0.653, 0.6902,
                  0.7388, 1];
    function feelOf(u) {
      var x = clamp((u - FEEL_D0) / (1 - 2 * FEEL_D0), 0, 1);
      var s = x * (FEEL_Q.length - 1), i = Math.min(FEEL_Q.length - 2, Math.floor(s));
      return FEEL_Q[i] + (FEEL_Q[i + 1] - FEEL_Q[i]) * (s - i);
    }

    // HOW FAR PAST THE FIELD'S OWN RANGE THE THRESHOLD TRAVELS (matter.js:312, `reach = 0.5 + 0.10`).
    // The field runs from 0 to 1 — a plain ladder over the frame at six parts and two grains at four,
    // each of them between 0 and 1 — so a threshold a tenth below 0 leaves every point of the frame
    // on work A's side and a tenth above 1 leaves every point on work B's. That tenth is the MARGIN
    // either door stands on, and it is the number the reading below is held against.
    var MARGIN = 0.10;

    // The numbers of one frame: everything the shader gets beyond the seating of the two works is a
    // pure function of the pose (matter.js:309-329). The threshold travels a tenth past either end
    // of the field and no further — past the field's own range every point stands on one side and
    // the work is whole, which is what makes both doors exact.
    //
    // The grain is a parameter here rather than read straight off the pose, because the hold in
    // `values` below asks this same function for the same pose at a neighbouring cell count. Nothing
    // else about it moved.
    function posed(st, grainA) {
      var d = feelOf(clamp(st.mix, 0, 1));
      var reach = 0.5 + MARGIN;
      var drift = (st.reduced ? 0 : st.t) * 0.11 * clamp(st.drift, 0, 1);
      return {
        dial: d, grainA: grainA, grainB: grainA * GRAIN_FINE, ladder: LADDER,
        gather: 0.04 + 0.26 * clamp(st.gather, 0, 1),
        tau: 0.5 - reach + 2 * reach * d,
        drift: [drift, drift * 0.6],
        loosen: st.travel * AMP * clamp(st.loosen, 0, 1) * 4 * d * (1 - d),
        guard: st.shade * smoothstep(0, 0.09, d) * smoothstep(1, 0.91, d),
      };
    }

    // ---- THE DOOR THE INSTRUMENT READS FOR ITSELF ------------------------------------------------
    // His 18:00 architecture decision, carried in the U27 brief: the instrument reads its doors at
    // runtime on the actual buffer, and the report it hands back is the runtime truth; what the
    // manifest declares is only the claim. The meshing instrument answered that first
    // (pass-inst-gears.js, THE DOOR THE INSTRUMENT READS FOR ITSELF); this is the same law read in
    // the material's own units, which are its CELLS.
    //
    // WHAT A DOOR ASKS OF THIS INSTRUMENT, and where the buffer enters it. At either door the mask
    // must be whole — `cov` exactly 1 at the entry door and exactly 0 at the exit — and `cov` is
    //     clamp(0.5 + (F − tau) / (grad · h)),   h = 1 / uRes.y
    // so the mask crosses over inside a band of the field HALF THE FIELD'S OWN SLOPE PER BUFFER
    // POINT wide. Away from a door that band is the front the visitor watches travel. At a door it
    // must fall entirely outside the frame, and it does exactly while
    //     0.5 · grad · h  ≤  MARGIN,     i.e.   grad ≤ 2 · MARGIN · bufH.
    // The threshold's tenth is fixed; the slope is set by the GRAIN, which is cells across the
    // frame's height; and the buffer's own height is what turns those cells into points. So a grain
    // that is whole on a tall buffer is a leak on a short one — the same class the meshing
    // instrument found at its own singular point, in this instrument's own numbers.
    //
    // THE SLOPE IS READ AS THE FIELD'S OWN CEILING, and that is said rather than hidden. The field
    // is `LADDER · uv.x + (1 − LADDER) · (0.62 · n1 + 0.38 · n2)`, so its steepest possible slope is
    // the ladder's own plus each grain's cell count times the value noise's own steepest slope. That
    // noise is `a + (b−a)u.x + (c−a)u.y + k·u.x·u.y` on smoothstep coordinates, whose partials are
    // `((b−a) + k·u.y) · 6f(1−f)` and its mirror: the bracket never leaves [−1, 1] because it is
    // linear in u and lands on b−a at one end and d−c at the other, and 6f(1−f) tops out at 1.5. So
    // one cell's slope never passes 1.5·√2, and the ceiling below is exact as a ceiling.
    //
    // WHY A CEILING RATHER THAN THE MASK ITSELF. The meshing instrument reads its own mask because
    // its leak stands at ONE point it can name — the wheel's centre — so a three-point neighbourhood
    // answers it. This field's steepest cell can stand anywhere on the frame, and reading it exactly
    // would mean walking the whole buffer twice over at a door instant. The ceiling costs two
    // multiplications, it can only ever OVER-hold — a door it calls whole is whole beyond argument —
    // and the hold it triggers costs the picture nothing at a door, where the frame is one whole
    // work whatever the grain is. What it buys is stated in the refusal itself, in the field's own
    // units, so a reader can see exactly how far past the margin the slope stood.
    var NOISE_SLOPE = 1.5 * Math.SQRT2;
    var DOOR_HOLD = 2;   // how far the hold reaches, in whole cells of the coarse grain

    // The grid the door is read on, and which of the two it is. `drawn` says which one the sentence
    // below names, since a reader told «a 390 x 200 frame» would look for a device that has none.
    function doorGridOf(st) {
      var bw = Math.round(st.bufWidth), bh = Math.round(st.bufHeight);
      if (bw >= 1 && bh >= 1) return { w: bw, h: bh, drawn: true };
      return { w: Math.round(st.cssWidth), h: Math.round(st.cssHeight), drawn: false };
    }

    // The field's own steepest slope anywhere on the frame, in field units per frame height. Every
    // term has its counterpart in `gF` in FRAG above.
    function slopeOf(v, aspect) {
      return v.ladder / Math.max(aspect, 0.05)
           + (1 - v.ladder) * (0.62 * v.grainA + 0.38 * v.grainB) * NOISE_SLOPE;
    }

    // THE DOOR, MEASURED. Null everywhere but at a door, since away from the doors a travelling
    // front is the picture rather than a fault. The door is named by the manifest's own `doors`
    // block: `mix` at 0 is the entry door, where the frame is the departing work whole, and `mix` at
    // 1 the exit door, where it is the arriving one.
    function doorReadOf(v, st) {
      var want = st.mix === 0 ? 1 : (st.mix === 1 ? 0 : -1);
      if (want < 0) return null;
      var g = doorGridOf(st), W = g.w, H = g.h;
      if (!(W >= 1) || !(H >= 1)) return null;
      var slope = slopeOf(v, W / Math.max(H, 1));
      return { grid: g, want: want, slope: slope,
               // half the mask's own crossover, in the field's own units, on THIS buffer
               cross: 0.5 * slope / H,
               cells: v.grainA, cellPx: H / Math.max(v.grainA, 1e-6) };
    }

    // THE REFUSAL, worded the way the host's own manifest refusals read: what is wrong, in this
    // instrument's own measured numbers, on the grid it was measured on.
    function doorWhyNoOf(read) {
      if (!read || read.cross <= MARGIN) return null;
      var g = read.grid;
      return (read.want ? "the entry" : "the exit") + " door leaks: at a grain of "
           + read.cells.toFixed(2) + " cells across the frame's height — "
           + read.cellPx.toFixed(2) + " points of a " + g.w + " x " + g.h
           + (g.drawn ? " buffer" : " frame") + " to a cell — the field's own steepest slope is "
           + read.slope.toFixed(2) + ", so this instrument's own mask crosses over inside "
           + read.cross.toFixed(4) + " of the field, past the " + MARGIN
           + " the threshold stands beyond the field's own range, and the "
           + (read.want ? "arriving" : "departing")
           + " work takes the points of the frame nearest that crossing, where "
           + (read.want ? "the entry" : "the exit") + " door's own law asks for the "
           + (read.want ? "departing" : "arriving") + " work at every point";
    }

    // THE NUMBERS OF ONE FRAME, WITH ITS DOOR HELD WHOLE ON THE BUFFER BEING DRAWN. Away from a door
    // this is `posed` and nothing more: the reading is taken nowhere else and no grain moves. At a
    // door whose grain crosses the mask over inside the frame on the buffer being drawn, the
    // instrument steps to a COARSER whole cell count — the only direction that closes it, since the
    // slope rises with the cell count — and answers with the first pose whose door is whole. What
    // the score asked for and what was applied are both on the record: `grainA` is the grain drawn,
    // `grainRequest` is the one handed in, `grainCells` says how many whole cells apart they stand,
    // and `doorHeld` carries the leak the request would have drawn, in its own words.
    //
    // HOW FAR «NEAR» REACHES, and why it is two cells. The material's own unit is the cell, so that
    // is the unit the distance is counted in. Two cells of a grain that runs from four to
    // thirty-four is a step of the material nobody watching a door can see, because at a door the
    // frame is one whole work and no grain of it is on screen; beyond two cells the pose the score
    // asked for is genuinely a different material and the refusal is the honest answer. A guard
    // that never refuses proves nothing.
    function values(st) {
      var grainA = GRAIN_MIN + (GRAIN_MAX - GRAIN_MIN) * clamp(st.grain, 0, 1);
      var v = posed(st, grainA);
      v.grainRequest = grainA;
      v.grainCells = 0;
      v.doorHeld = null;
      var read = doorReadOf(v, st);
      var no = doorWhyNoOf(read);
      v.doorGrid = read ? read.grid : null;
      v.cellPx = read ? read.cellPx : null;
      v.doorCross = read ? read.cross : null;
      if (!no) { v.doorWhyNo = null; return v; }
      var rung = Math.floor(grainA);
      for (var step = 0; step <= DOOR_HOLD; step++) {
        var tryA = rung - step;
        if (tryA < GRAIN_MIN || tryA >= grainA) continue;
        var w = posed(st, tryA);
        var wRead = doorReadOf(w, st);
        if (doorWhyNoOf(wRead)) continue;
        w.grainRequest = grainA;
        w.grainCells = grainA - tryA;
        w.doorHeld = no;
        w.doorWhyNo = null;
        w.doorGrid = wRead.grid;
        w.cellPx = wRead.cellPx;
        w.doorCross = wRead.cross;
        return w;
      }
      v.doorWhyNo = no + ", and no whole cell stands within " + DOOR_HOLD
                  + " cells of the grain handed in";
      return v;
    }

    var manifest = {
      id: "matter", api: 1, arity: 2,
      // The module's own header ties it to the release envelope's disassembly–mystery–reassembly
      // class: the first work comes apart into the material and the second gathers out of it.
      roles: ["disassembly", "mystery", "assembly"],
      // READ OFF THE MODULE'S OWN CONSTRUCTION. The vocabulary table publishes no level for this
      // module (lab/CROSSING-BRIEF.md carries no `matter` row), so these two are derived and said to
      // be derived: one field runs over the whole frame at SURFACE, and its grain is the TEXTURE.
      levels: ["SURFACE", "TEXTURE"],
      params: { loosen: [0, 1], drift: [0, 1], gather: [0, 1], grain: [0, 1] },
      // EVERY handle a score can drive (§4.4b). `mix` is the dial and `clock` is the second the host
      // hands down; the four below them are the module's declared params; `seed` is its die; and
      // `shade` and `travel` are the two judge channels the module keeps for measuring a law on the
      // picture — the frame with the contact shadow against the frame without it, and the same for
      // the drag. They rest at 1, which is what the module does with them.
      //
      // NO HANDLE HERE KEEPS A CLOCK OF ITS OWN. The one place the module reads time is the drift of
      // the field, `t * 0.11 * drift` (matter.js:321), where `t` was its own accumulated frame time.
      // It reads the `clock` handle instead, so a seeded score repeats to the pixel.
      handles: {
        mix: { min: 0, max: 1, def: 0 },
        clock: { min: 0, max: 14, def: 0 },
        loosen: { min: 0, max: 1, def: 0.6 },
        drift: { min: 0, max: 1, def: 0.45 },
        gather: { min: 0, max: 1, def: 0.3 },
        // THE MEASUREMENT THIS HANDLE IS READ AGAINST AT A DOOR, published beside its range the way
        // the meshing instrument publishes its own. `heldWholeAtADoor` says what is read (the
        // field's own steepest slope, held against the tenth the threshold stands past the field's
        // own range), on which grid (the drawing buffer the host binds, with the CSS frame where it
        // hands none), how far the hold reaches (two whole cells of the coarse grain) and where the
        // request the score handed in stays on the record.
        grain: { min: 0, max: 1, def: 0.45,
                 applied: { heldWholeAtADoor: { cells: DOOR_HOLD, readOn: "the drawing buffer",
                                                reads: "grainRequest",
                                                measures: "the field's own steepest slope against "
                                                        + "the tenth the threshold stands past the "
                                                        + "field's own range" } } },
        seed: { min: 0, max: 8, def: 0 },
        shade: { min: 0, max: 1, def: 1 },
        travel: { min: 0, max: 1, def: 1 },
      },
      // The dial's two ends. At 0 the threshold stands a tenth below the field's whole range, so
      // every point covers on A; at 1 it stands a tenth above it and every point covers on B. The
      // drag and the contact shadow are both nothing there, so each door is one work and nothing
      // else. Neither is published in module-contract.json, which carries no `matter` entry — both
      // are read off the module's own geometry and the conformance rows measure them.
      neutrals: { a: 0, b: 1 },
      doors: { in: { handle: "mix", value: 0, work: "a" },
               out: { handle: "mix", value: 1, work: "b" } },
      // Both doors frame alike: the crop the drag's headroom is paid for with is a constant, while
      // the drag itself dies at both ends.
      framings: { "0": { coverCrop: ZOOM }, "1": { coverCrop: ZOOM } },
      drivers: ["progress", "cueProgress", "time", "velocity", "capability", "noise", "static",
                "curve", "spline", "map", "add", "multiply", "mix", "clamp", "hold", "segment",
                "ramp", "slew", "oscillate", "node"],
      camera: { needs: "none", authority: "stage" },
      gl: { preserveDrawingBuffer: false },
      // THE COVERAGE LAW (§7). The mask the shader already builds from the travelling threshold is
      // published as the alpha: `1.0 - cov`, the share of the arriving work. The threshold travels a
      // tenth past either end of the field, so at the entry door every point stands on A's side and
      // the alpha is 0 at every point, and at the exit door every point stands on B's side and the
      // alpha is 1 at every point. That is what keeps door B this instrument's own whole work.
      coverage: { writes: true,
                  how: "1.0 - cov, the share of the arriving work at the travelling threshold" },
      // The neutral pose is the ENTRY DOOR — `mix` at 0, the value the `doors` block above names —
      // so the frame keys the host reads off it at registration include the door's own record.
      neutralPose: { mix: 0, loosen: 0.6, drift: 0.45, gather: 0.3, grain: 0.45,
                     seed: 0, shade: 1, travel: 1, t: 0, reduced: false,
                     cssWidth: 1000, cssHeight: 1000 },
      passes: [{
        program: "matter", vert: VERT, frag: FRAG, position: "aPos",
        uniforms: [
          { name: "uA", type: "sampler2D", source: "textureA" },
          { name: "uB", type: "sampler2D", source: "textureB" },
          { name: "uFitA", type: "vec4", source: "fitA" },
          { name: "uFitB", type: "vec4", source: "fitB" },
          { name: "uRes", type: "vec2", source: "resolution" },
          { name: "uGrainA", type: "float", source: "frame:grainA" },
          { name: "uGrainB", type: "float", source: "frame:grainB" },
          { name: "uDrift", type: "vec2", source: "frame:drift" },
          { name: "uLadder", type: "float", source: "frame:ladder" },
          { name: "uTau", type: "float", source: "frame:tau" },
          { name: "uLoosen", type: "float", source: "frame:loosen" },
          { name: "uGather", type: "float", source: "frame:gather" },
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
      provenance: { labPath: "lab/effects/matter.js", commit: "e0f1b91" },
      readiness: "production-ready",
    };

    var live = false;
    return {
      name: "matter",
      manifest: manifest,
      values: values,
      fit: fit,
      feel: feelOf,
      prepare: function (o) {
        if (!o.sources) return { take: false, why: "the matter instrument needs both works" };
        if (!o.cue) return { take: false, why: "no cue names it" };
        return { take: true };
      },
      start: function () { live = true; },
      // The pose the shader draws. Every number in it comes from a handle a score can drive, and the
      // field's drift reads the second the host hands down, so a seeded run repeats to the pixel.
      //
      // A DOOR THIS INSTRUMENT CANNOT KEEP WHOLE IS REFUSED RATHER THAN DRAWN. The door law is the
      // instrument's own claim (the manifest's coverage line above), so the instrument is what
      // answers for it: at either door it reads its own field on the buffer the host is about to
      // bind and, where the grain crosses the mask over inside the frame there and no whole cell
      // within reach closes it, hands the host the reason with the measured slope in it instead of
      // drawing a door that is two works at once. The host recovers the transaction on that reason
      // and the walk's own glide carries the visitor, which is the product's own behaviour with no
      // renderer.
      frame: function (st) {
        if (!live) return;
        var h = st.handles;
        var pose = {
          mix: h.mix, loosen: h.loosen, drift: h.drift, gather: h.gather, grain: h.grain,
          shade: h.shade, travel: h.travel, seed: h.seed, t: h.clock, reduced: st.reduced,
          cssWidth: st.viewport.w, cssHeight: st.viewport.h,
          // THE GRID THE SHADER WILL SAMPLE ON, carried into the pose so the door is read on the
          // buffer the host is about to bind as `uRes` rather than on the CSS frame around it. The
          // host settles it from the device ratio and its own resolution step, so it moves while a
          // pass plays and each door is read on the grid standing at that door's own instant.
          bufWidth: st.viewport.bufferW, bufHeight: st.viewport.bufferH,
        };
        if (h.mix === 0 || h.mix === 1) {
          var no = values(pose).doorWhyNo;
          if (no) { st.fail(st.token, no); return; }
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
    instrument: matterInstrument(),
  });
})();
