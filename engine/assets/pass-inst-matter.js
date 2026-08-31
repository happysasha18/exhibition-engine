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
      // §8's `seams` block: how wide the travelling front's own crossover stands, in points of the
      // drawing buffer, off the host's own shared hairline reading.
      "uniform float uSeam;",
      "uniform float uPresence;",  // the entry-door contract's reserved dry
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
      // THE FRONT'S OWN RETOUCH, off the host's own `seams` reading (§8's `seams` block,
      // pass-layer.js). `d` is the signed distance to the front counted in POINTS OF THE DRAWING
      // BUFFER — the division by `grad * h` is what puts it in that unit — so the crossover this
      // line writes is `uSeam` buffer points wide and nothing else. It stood at a bare `0.5 + d`,
      // which is the same statement with the width typed in as 1, and that 1 was this file's own
      // number for the very question kaleidoscope's crease, planet's wrap and tunnel's ring-join
      // each answered privately before the host took the argument over. The manifest below declares
      // this front as an `isoline` HAIRLINE and the host answers with the one width every hairline
      // in the fleet is held to, read on the buffer this frame is actually drawn on.
      "  float cov = clamp(0.5 + d / max(uSeam, 1e-4), 0.0, 1.0);",
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
      "  gl_FragColor = vec4(col, (1.0 - cov) * uPresence);",
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
    // inverse of the integral at twenty-one evenly spaced shares (how the curve is read BETWEEN two
    // of those shares is the block below, and it is the port's own answer, not the module's).
    // The two-piece logarithm the module carried before it cannot hold this handle: the field's own
    // values crowd the middle and thin to nothing at both ends, so the curve stands nearly vertical
    // at both ends and nearly flat across the middle. Carried here digit for digit; the port
    // re-derives nothing.
    var FEEL_D0 = 0.05;
    var FEEL_Q = [0, 0.1994, 0.2488, 0.2852, 0.3168, 0.3454, 0.372, 0.3972, 0.4215, 0.4454,
                  0.469, 0.4925, 0.5162, 0.5405, 0.5657, 0.5923, 0.621, 0.653, 0.6902,
                  0.7388, 1];

    // HOW THOSE TWENTY-ONE SHARES ARE READ BETWEEN THEIR OWN POINTS (S-20, 2026-08-28). Not one of
    // the numbers above moves here. What changed is the line drawn BETWEEN two of them.
    //
    // WHAT WAS WRONG WITH STRAIGHT LINES. The curve's own VALUE was right at every knot and its
    // SPEED was a staircase: constant inside each share, and stepping at each of the nineteen joins
    // between them. On this table the worst of those joins is the last, where the threshold's travel
    // went from 1.080 of the dial a unit to 5.804 in one instant — five and a third times faster,
    // with nothing at all between the two speeds — and the first join steps the other way just as
    // hard, from 4.431 down to 1.098, four-fold in one instant.
    // The same step stood at the dead band's own edge: the dial is held perfectly still across the
    // first FEEL_D0 of the hand and then left at 4.43 of the dial a unit at once. Neither step is in
    // the measurement. What was integrated to build this table is a smooth reading of how far a
    // photograph travels, and a polyline through its samples invents corners the reading never had —
    // and this instrument spends the whole of that speed on ONE thing the eye is watching, the front
    // that carries the arriving work across the frame (`tau` below travels 1.2 of the field on it).
    //
    // THE SHAPE IS THE HOST'S OWN, and it is the same repair one layer down. `pass-layer.js`'s
    // `splineSlopes`/`splineAt` — Fritsch–Carlson, carried over unchanged — is what his word of
    // 2026-08-11 put on every score track after he judged speed steps at segment joints; a response
    // curve read as twenty separate lines is that same defect inside one handle. One curve through
    // all twenty-one points passes through every knot exactly, cannot overshoot or turn back (so the
    // curve stays monotone and both doors stand exactly where they stood), and rests at both its own
    // ends — so it leaves the dead band at rest instead of at a run, for the reason the host's own
    // note gives for its zero end tangents: the value is HELD either side, and a track rests where it
    // is held.
    var FEEL_M = (function (q) {
      var n = q.length, h = 1 / (n - 1), d = [], m = [], i, a, b, s;
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
      return m;
    }(FEEL_Q));
    function feelOf(u) {
      var x = clamp((u - FEEL_D0) / (1 - 2 * FEEL_D0), 0, 1);
      var n = FEEL_Q.length, h = 1 / (n - 1);
      var i = Math.min(n - 2, Math.floor(x * (n - 1)));
      var s = (x - i * h) / h, s2 = s * s, s3 = s2 * s;
      return (2 * s3 - 3 * s2 + 1) * FEEL_Q[i] + (s3 - 2 * s2 + s) * h * FEEL_M[i]
           + (3 * s2 - 2 * s3) * FEEL_Q[i + 1] + (s3 - s2) * h * FEEL_M[i + 1];
    }

    // HOW FAR PAST THE FIELD'S OWN RANGE THE THRESHOLD TRAVELS (matter.js:312, `reach = 0.5 + 0.10`).
    // The field runs from 0 to 1 — a plain ladder over the frame at six parts and two grains at four,
    // each of them between 0 and 1 — so a threshold a tenth below 0 leaves every point of the frame
    // on work A's side and a tenth above 1 leaves every point on work B's. That tenth is the MARGIN
    // either door stands on, and it is the number the reading below is held against.
    var MARGIN = 0.10;

    // HOW WIDE THE FRONT'S OWN CROSSOVER STANDS WHERE NO HOST HAS ANSWERED — at registration, before
    // any frame has been asked for. One point of the drawing buffer is the width this file drew the
    // front at before §8's `seams` block existed (`cov = clamp(0.5 + d)` in FRAG, where `d` is
    // already counted in buffer points), so the fallback is that number and nothing invented. Every
    // drawn frame reads the host's own answer instead.
    var SEAM_POINTS = 1.0;
    function seamOf(st) {
      var s = st && st.seam && st.seam.isoline;
      return typeof s === "number" && isFinite(s) && s > 0 ? s : SEAM_POINTS;
    }

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
        // THE FRONT'S OWN RETOUCH (§8's `seams` block), carried into the shader and read back by the
        // door reading below, so the width the picture is drawn at and the width the door is held
        // against cannot be two different numbers.
        seam: seamOf(st),
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
               // half the mask's own crossover, in the field's own units, on THIS buffer — and at
               // the width §8's `seams` block holds this front to, which is the same number the
               // shader draws it at. A wider retouch is a wider crossover and a door that has to
               // stand further past the field's own range to stay whole, so the two move together
               // rather than the reading being held against a width the picture no longer uses.
               cross: 0.5 * v.seam * slope / H,
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
      // WHAT THIS INSTRUMENT CUTS ON, ADDED 2026-08-31 (cause A, item 5 — the reconciliation).
      // This file never declared the key; the composer's own `INSTRUMENTS.cuts` carried «band»,
      // «scale» with no line here to answer for it. Both check out independently: the header just
      // below names the travelling threshold itself «a band of loosened matter», and this
      // instrument's own fit function (`INSTRUMENT_SUITS.matter`) reads the pair's tonal and
      // spectral bridge — exactly `PIVOT_SHAPES["tonal-and-spectral"]`'s own two element kinds,
      // `band` and `scale`.
      cuts: ["band", "scale"],
      // WHERE THIS INSTRUMENT HAS A SEAM (§8's `seams` block, pass-layer.js). It cuts the frame in
      // one place and the file's own header names it: "a band of loosened matter travels across the
      // frame with one work whole ahead of it and the other whole behind" (above, THE MATTER
      // INSTRUMENT). The edge of that band is the travelling threshold `cov` in FRAG — the level set
      // of the field `F` where it stands at `uTau`, one work on either side of it — so the shape cut
      // here is a LEVEL SET OF A CONTINUOUS FIELD and `isoline` is the fleet's own word for it,
      // already carried by the veiling instrument, whose own declaration names this instrument by
      // name as running the same construction (`pass-inst-veil.js`, WHERE THIS INSTRUMENT HAS A
      // SEAM). It is a HAIRLINE retouch and not a handover zone: `d` in FRAG is the distance to that
      // level set counted in points of the drawing buffer, so what the crossover exists for is to
      // keep the boundary off the sampling grid's own stairs rather than to blend two unrelated
      // things across a visible band — the field either side of it is one continuous surface. `of`
      // names no handle for the reason the host's own block gives: a hairline spends none of an
      // element's own room, so it does not shrink as the material's cells multiply, and this
      // instrument's `grain` handle drives the cell count without touching the width of this edge.
      //
      // THE GRAIN IS NOT A SECOND SEAM, and that is a decision rather than an omission. `vnoise` is
      // value noise on smoothstep coordinates — continuous in value AND in its first derivative
      // across every cell boundary, which is what its own exact gradient in FRAG returns — so a
      // cell's edge is no boundary the picture can help but have. Only the threshold is.
      seams: [{ kind: "isoline", of: null, unit: "points of the drawing buffer" }],
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
      // LEVEL, PER SHELF 17 (docs/design/PASS-API-V1.md:716). The field — its direction, its drag
      // and the band it loosens — runs over the whole frame at SURFACE; the grain it drags is the
      // TEXTURE, per the manifest's own `levels` reasoning above. `mix` is the crossing's own dial
      // and `clock` is the module's own time, neither a structural level; `seed` is the score's die;
      // `shade` and `travel` are the two judge channels named in this file's own handles comment.
      handles: {
        mix: { min: 0, max: 1, def: 0, level: null },
        clock: { min: 0, max: 14, def: 0, level: null },
        loosen: { min: 0, max: 1, def: 0.6, level: "SURFACE" },
        drift: { min: 0, max: 1, def: 0.45, level: "SURFACE" },
        gather: { min: 0, max: 1, def: 0.3, level: "SURFACE" },
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
                                                        + "field's own range" } },
                 level: "TEXTURE" },
        seed: { min: 0, max: 8, def: 0, level: null },
        shade: { min: 0, max: 1, def: 1, level: null },
        travel: { min: 0, max: 1, def: 1, level: null },
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
                     seed: 0, shade: 1, travel: 1, presence: 1, t: 0, reduced: false,
                     cssWidth: 1000, cssHeight: 1000 },
      passes: [{
        program: "matter", vert: VERT, frag: FRAG, position: "aPos",
        uniforms: [
          { name: "uPresence", type: "float", source: "handle:presence" },
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
          { name: "uSeam", type: "float", source: "frame:seam" },
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
                   programs: 1, passes: 1, bytesEstimate: 2000084, variant: "lean" },
                   standard: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0,
                               programs: 1, passes: 1, bytesEstimate: 8000084,
                               variant: "standard" },
                   rich: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                           passes: 1, bytesEstimate: 32000084, variant: "rich" } },
      capabilities: ["webgl2"],
      decline: ["one work only", "a source that never decoded"],
      provenance: { labPath: "lab/effects/matter.js", commit: "e0f1b91" },
      // HOW WELL THIS INSTRUMENT SUITS A PAIR (2026-08-18, his word of 09:51 and its sharpening at
      // 09:53). An instrument no longer answers WHETHER it takes a pair — it answers how well it
      // suits one, so a poor fit is still playable and still explains itself. The arithmetic runs in
      // the composer, which is the one place holding both records; what stands here is the
      // instrument's own statement of WHAT IT READS, which is the fact this file owns.
      //
      // THE SHAPE, for the ports in flight: `suits.reads` names the measurements, by their path in
      // a work record, and `suits.how` says in one sentence what a whole fit and a fit of nothing
      // mean for this instrument. A fit of nothing is never a refusal — it ranks last and plays
      // where nothing ranks higher.
      suits: { reads: ["luminance.level", "texture.detailPx"],
               how: "it hands one tonal world and one detail scale over to another — substance "
                  + "reads through light, so `luminance.level` (the judge seat's standing "
                  + "correction of 2026-08-18/19, the median of each work's own luminance) is the "
                  + "genuine tone, where `palette.colourfulness` stood here before — so it suits a "
                  + "pair whose grounds and detail scales stand close enough for the handover to "
                  + "read as one substance changing rather than two pictures swapped; both readings "
                  + "are of the pair by construction, which is why it suits every pair somewhat and "
                  + "no pair absolutely" },
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
          shade: h.shade, travel: h.travel, seed: h.seed, presence: h.presence,
          t: h.clock, reduced: st.reduced,
          cssWidth: st.viewport.w, cssHeight: st.viewport.h,
          // THE GRID THE SHADER WILL SAMPLE ON, carried into the pose so the door is read on the
          // buffer the host is about to bind as `uRes` rather than on the CSS frame around it. The
          // host settles it from the device ratio and its own resolution step, so it moves while a
          // pass plays and each door is read on the grid standing at that door's own instant.
          bufWidth: st.viewport.bufferW, bufHeight: st.viewport.bufferH,
          // THE FRONT'S OWN RETOUCH, off the host's own `seams` reading (§8's `seams` block). Only
          // the host knows what every instrument declaring a hairline is holding its own edge to, so
          // it answers once and this file carries the number rather than choosing it.
          seam: st.seams,
        };
        // AT A DOOR THE INSTRUMENT SAYS WHAT IT APPLIED, and says it before it refuses. The reading
        // is taken on the buffer this frame is drawn on, so it is the run-time truth his 18:00
        // decision asks for rather than the grain the score asked for. `applied` is the request less
        // the whole cells the hold walked back, which is the grain the frame was actually posed on.
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
              reads: "grain", request: v.grainRequest,
              applied: v.grainRequest - v.grainCells,
              moved: v.grainCells, unit: "cells",
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
    instrument: matterInstrument(),
  });
})();
