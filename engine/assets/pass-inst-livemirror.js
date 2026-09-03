/*!pass-inst-livemirror.js*/
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
  // THE LIVE-MIRROR INSTRUMENT (§8) — lab/effects/livemirror.js carried across
  // ================================================================================================
  // WHAT THE VISITOR SEES. One work stands whole and fills the frame. A fold line appears across it,
  // standing on a line the work itself carries, and everything past that line stops being the
  // photograph and becomes the mirror of what lies before it — the picture closing on itself the way
  // a sheet of paper closes on a crease. The frame goes on folding until it is a field of mirrored
  // panels with a thin bright seam down each crease; there the two works exchange; then the second
  // work opens back out of its own mirror and stands whole.
  //
  // HIS STANDING VERDICT ON THIS EFFECT, and the one condition it carries.
  // lab/CROSSING-HISTORY.md's vocabulary table, the row `livemirror | зеркальный сгиб | both | CELL`:
  // «approved; fold lines must land on the work's own structural lines». That sentence is the whole
  // brief for this port, and it is why the module's own wandering line is not what a score gets. The
  // module drifts its line across the mount on two incommensurate sines because it lives on a page
  // with a pointer and nothing else to read; an instrument in this engine is handed the pair's own
  // measured structural line — `structure.regions.line.{x,y}.at`, the same reading boxfold's own
  // crease reads, in place of the radial-centre midpoint this port first stood the fold at, corrected
  // Phase 9's own sweep (2026-09-01) — and stands the fold there. The wander survives as `drift`,
  // resting at nothing, so the module's own life is reachable and is never the default.
  //
  // WHY IT STANDS HERE. It cuts on PANELS — the fold lines partition the frame into two or four
  // mirrored panels — which is the kind the composer's own census counts 1 296 declined pairs
  // waiting on, and it FILLS THE FRAME, which is the ground 1 320 further plans are declined for
  // want of. Two instruments already cut on panels and both are the wrong act for most of the
  // collection: the box fold spends the crossing's one miracle (it declares the WORLD level) so no
  // quiet link and no return may reach it, and the unfold sets out to reveal a work's own making so
  // it stands down where that making does not read. This one claims no world, spends no miracle and
  // asks only for a line — which is what a step with nothing to spend can actually cast.
  //
  // ------------------------------------------------------------------------------------------------
  // A ONE-WORK MODULE PLAYED AS A CROSSING
  // ------------------------------------------------------------------------------------------------
  // The module takes ONE picture (`needs: 1` in its own declaration) and its dial runs from the flat
  // photograph to the fold. A cue of this engine carries two works and two doors (§8: `neutrals`,
  // `doors`), so the port had to say where the second work enters — and this module's construction
  // puts that instant at the OPPOSITE end from the unfold's. The unfold's works exchange on a flat
  // photograph, because that is where its sheet stands closed; here the flat photograph is the DOOR,
  // and the closed state is the DEEP FOLD, where the frame is a field of mirrored panels and neither
  // work is legible as itself. That is where the two exchange: the charter's mystery in the middle,
  // and the one instant of this instrument's travel at which a dissolve shows no photograph coming
  // apart.
  //
  // The hand therefore runs: the first work folds into its mirror over the first forty-six
  // hundredths, the two works exchange across the eight hundredths in the middle while the frame is
  // wholly mirrored, and the second work opens back out over the last forty-six. HOLD is the port's
  // own number and the only one of the travel's that is.
  //
  // ------------------------------------------------------------------------------------------------
  // THE ONE THING THAT HAD NO SHAPE IN THIS HOST, AND THE SHAPE IT WAS GIVEN
  // ------------------------------------------------------------------------------------------------
  // Past the border of the photograph the module's own comment says the texture KEEPS MIRRORING and
  // never stretches, and it gets that for nothing: it uploads its own texture and sets
  // `TEXTURE_WRAP_S`/`TEXTURE_WRAP_T` to `MIRRORED_REPEAT` (livemirror.js:190-191). The host of this
  // engine uploads both works itself and binds them CLAMP_TO_EDGE (pass-layer.js:110-111), and an
  // instrument may not touch a texture parameter — it never sees the context. Bound as the host
  // binds them, every sample past the border returns the border texel and the continuation SMEARS,
  // which is the one thing the module's own comment forbids.
  //
  // THE SHAPE. MIRRORED_REPEAT is a triangle wave on the sample coordinate and nothing else, so the
  // wrap is written into the shader: `1 - |mod(q, 2) - 1|` per axis, which is the sampler's own rule
  // stated as arithmetic. It is the same move the unfold made for its parquet, one axis at a time.
  // The residual against the module's hardware wrap is a sub-texel filtering difference at the
  // mirror line alone, and the suite measures it rather than assuming it.
  //
  // ------------------------------------------------------------------------------------------------
  // THE COVERAGE: THIS INSTRUMENT FILLS THE FRAME
  // ------------------------------------------------------------------------------------------------
  // §7's coverage law of 12:40 asks every instrument to say where its own matter is absent. It is
  // absent nowhere, and that is the mirror's own construction rather than a crop bought for it: the
  // work is COVER-fitted over the frame, so at the flat door every point of the frame is the
  // photograph; and once the fold runs, every point of the frame reads SOME point of the work,
  // because a reflection is a map onto the work and the wrap above carries whatever falls past its
  // border back into it. There is no angle, no line and no breath at which a point of the frame has
  // nothing to read. The declaration is `writes: false`, which under the placement rule (§8 as
  // amended 14:05, and `coverageWhyNo`) makes it lawful as the LOWEST cue of a stack and as a whole
  // one-cue score.
  function livemirrorInstrument() {
    var VERT = [
      "attribute vec2 aPos;",
      "varying vec2 vUv;",
      "void main(){ vUv = vec2(aPos.x * 0.5 + 0.5, 0.5 - aPos.y * 0.5); gl_Position = vec4(aPos, 0.0, 1.0); }",
    ].join("\n");

    // The module's own fragment shader, carried across term for term. It is written in ESSL 1.00
    // here, as every instrument of this engine is, where the module wrote ESSL 3.00 — `texture` is
    // `texture2D`, `fragColor` is `gl_FragColor` and the mode is a float rather than an int, because
    // the host builds one programme per manifest and every other pass it builds is ESSL 1.00. No
    // number moves.
    var FRAG = [
      "precision highp float;",
      "varying vec2 vUv;",
      "uniform sampler2D uA;",
      "uniform sampler2D uB;",
      // the seating of each work over the frame — the plain cover fit, which is the module's own
      // `cov` (livemirror.js:54-55) computed by the host instead of in the shader
      "uniform vec4 uFitA;",
      "uniform vec4 uFitB;",
      "uniform vec2 uRes;",
      // where the fold point stands across the frame, how far the photograph has become a fold, and
      // how far the two works have exchanged
      "uniform vec4 uFold;",
      // which fold, the seam's own brightness, the weight the further mirrored copies fall into the
      // dark by, and the breathing zoom
      "uniform vec4 uForm;",
      // the judges' handle: the fold map as colour
      "uniform float uMask;",
      // HOW FAR APART THE MIRRORED COPIES' OWN EXCHANGES STAND (charter shelf 7's PROPAGATED
      // arrival, наряд S-06: «в зеркальных копиях дальняя меняется первой» — of the mirrored
      // copies, the far one changes first). At nothing the whole frame exchanges at once, which is
      // what every other arrival asks for and what this instrument always did.
      "uniform float uProp;",
      // THE SAMPLER'S OWN MIRRORED WRAP, written as the triangle wave it is. The host binds both
      // works CLAMP_TO_EDGE and an instrument never sees the context, so the module's own
      // MIRRORED_REPEAT (livemirror.js:190-191) is carried here instead of asked for.
      "vec2 mirrored(vec2 q){ return 1.0 - abs(mod(q, 2.0) - 1.0); }",
      // ONE WORK, READ THROUGH THE FOLD. Everything below is the module's own fragment shader read
      // in the same order it wrote it.
      "vec3 folded(sampler2D tex, vec4 fit, out vec3 judge, out float near){",
      "  vec2 uv = vUv;",
      "  float ma = uRes.x / max(uRes.y, 1.0);",
      "  vec2 asp = vec2(ma, 1.0);",
      "  vec2 at = uFold.xy;",
      "  float dial = uFold.z;",
      "  float mode = uForm.x;",
      // fold: everything past the line is replaced by the reflection of what is before it
      "  vec2 p = (uv - at) * asp;",
      "  vec2 q = p;",
      "  float d;",
      "  float side = 0.0;",
      // HOW MANY MIRROR STEPS THIS POINT STANDS FROM THE PICTURE ITSELF — nothing where the point
      // is the photograph, one where it is its reflection, and two in the corner the both-folds
      // form reflects twice. It is the same `step(0.0, …)` test the panel above is named by, read
      // for its COUNT rather than for its name, and it is what makes «the further copy» a number.
      "  float steps = 0.0, maxSteps = 1.0;",
      "  if (mode < 0.5)      { d = abs(p.x); q.x = -d; side = step(0.0, p.x); steps = side; }",
      "  else if (mode < 1.5) { d = abs(p.y); q.y = -d; side = step(0.0, p.y); steps = side; }",
      "  else if (mode < 2.5) { d = min(abs(p.x), abs(p.y)); q = -abs(p);",
      "                         side = step(0.0, p.x) + 2.0 * step(0.0, p.y);",
      "                         steps = step(0.0, p.x) + step(0.0, p.y); maxSteps = 2.0; }",
      "  else {",
      "    vec2 n = vec2(0.7071067812, -0.7071067812);",
      "    float h = dot(p, n);",
      "    d = abs(h);",
      // the far side alone is reflected: below the line `h + abs(h)` is nothing and the point
      // stands where it was
      "    q = p - (h + abs(h)) * n;",
      "    side = step(0.0, h);",
      "    steps = side;",
      "  }",
      // THE CROSSING DIAL, and the module's own note on it, which is the reason this instrument
      // stays in focus at every mark of the hand: the dial picks WHICH POINT of the photograph a
      // pixel reads, never which of two already-rendered colours to show. `uv` is the pixel's own
      // place, the reflected point above is where the fold sends it, and the dial walks the SAMPLE
      // COORDINATE between them. One fetch answers every mark, so the frame is one picture in sharp
      // focus throughout and never two renderings laid over each other.
      "  vec2 uv2 = mix(uv, q / asp + at, dial);",
      // cover the frame with the work: crop, never stretch. `fit` is the host's own seating, which
      // is the module's `cov` by the same arithmetic.
      "  vec2 st = (uv2 - 0.5) * fit.xy / mix(1.0, uForm.w, dial) + 0.5;",
      // past the border of the work the picture keeps mirroring and never stretches; each further
      // copy is pushed down into the dark so the first fold stays the subject
      "  float over = max(max(-st.x, st.x - 1.0), max(-st.y, st.y - 1.0));",
      "  float out2 = smoothstep(0.0, 0.60, max(over, 0.0));",
      "  float depth = 1.0 - uForm.z * out2;",
      // HOW NEAR THIS POINT STANDS TO THE PICTURE ITSELF, as a share: 1 where the point IS the
      // photograph and nothing in the furthest copy of it the frame carries. Two readings make it
      // and both are already in this shader — the count of mirror steps above, which is how many
      // times the fold has reflected this point, and `out2`, the module's own reading of how far
      // past the work's own border the sample fell, which is what makes one further copy darker
      // than the last. Nothing new is measured for the exchange; the copies the module already
      // writes deeper into the dark are exactly the copies it calls further away.
      "  near = 1.0 - clamp((steps + out2) / max(maxSteps, 1.0), 0.0, 1.0);",
      "  vec2 mst = clamp(mirrored(st), 0.0, 1.0);",
      // the finish below belongs to the fold alone — none of it stands at the flat door — so every
      // term is gated to its own identity by the same dial the coordinate travelled on
      "  vec3 col = texture2D(tex, mst).rgb * mix(1.0, depth, dial);",
      "  float sm = uForm.y * dial;",
      // the seam itself: a thin bright core with a soft lift around it, plus two dark hairlines
      // flanking it wherever the photograph is pale, so the line reads on white walls as well as on
      // shadow and never blows out into a white smear
      "  float cw = 0.0016;",
      "  float core = exp(-(d * d) / (cw * cw));",
      "  float ring = max(exp(-(d * d) / (0.0052 * 0.0052)) - core, 0.0);",
      "  float halo = exp(-(d * d) / (0.038 * 0.038));",
      "  float lum = clamp(dot(col, vec3(0.299, 0.587, 0.114)), 0.0, 1.0);",
      "  float gain = mix(1.0, 0.45, lum);",
      "  col *= 1.0 - sm * ring * 0.55 * smoothstep(0.35, 0.75, lum);",
      "  col *= 1.0 + sm * halo * 0.16 * gain;",
      "  col += sm * (core * 0.60 + halo * 0.10) * gain * vec3(1.0, 0.965, 0.90);",
      "  float r = length((uv - 0.5) * asp) / (0.5 * length(asp));",
      "  col *= 1.0 - dial * 0.16 * pow(clamp(r, 0.0, 1.0), 2.4);",
      // THE FOLD MAP, the judges' own frame: which mirrored panel this point of the frame stands in,
      // and where in the work it reads. It is the same channel the panels instrument publishes and
      // it is what makes the coverage claim readable rather than asserted — a point with nothing to
      // read would carry no place at all.
      "  judge = vec3((side + 1.0) * 0.25, mst);",
      "  return col;",
      "}",
      "void main(){",
      "  vec3 jA, jB, judge, col;",
      "  float nA, nB, nJ;",
      "  float cross = uFold.w;",
      // THE EXCHANGE. Outside the hold one work is drawn and the other is never sampled; inside it
      // the frame is wholly mirrored on both roads and the two mirrored fields exchange.
      //
      // AND THE COPIES NEED NOT EXCHANGE TOGETHER. Under the charter's PROPAGATED arrival the
      // change runs THROUGH the mirrored copies, the far one first: a point's own exchange opens at
      // `near · spread` of the crossing and runs over what is left of it, so a point standing in a
      // further copy — small `near` — has already exchanged while the first copy still carries the
      // departing work. At a spread of nothing every point's own exchange opens at nothing and the
      // frame exchanges as one, which is the picture this instrument always drew.
      //
      // NEITHER DOOR MOVES UNDER ANY SPREAD, and it is arithmetic rather than a reading: the offset
      // stands in [0, spread], so at `cross` 0 every point's own share is nothing and at `cross` 1
      // every point's own share is `(1 − offset) / (1 − spread) >= 1`. The two branches above the
      // exchange are therefore still the two doors, untouched.
      "  float spread = clamp(uProp, 0.0, 0.9);",
      "  if (cross <= 0.0) { col = folded(uA, uFitA, judge, nJ); }",
      "  else if (cross >= 1.0) { col = folded(uB, uFitB, judge, nJ); }",
      "  else {",
      "    vec3 ca = folded(uA, uFitA, jA, nA);",
      "    vec3 cb = folded(uB, uFitB, jB, nB);",
      // THE COPY IS READ ON BOTH FIELDS AT ONCE. Each work is seated by its own cover fit, so the
      // two answer «which copy is this» a hair apart wherever the two files differ in shape; the
      // mean of them is one number for the one point being drawn, and a point where they disagree
      // is a point at a copy's own border, where the exchange is between two neighbouring copies
      // either way.
      "    float near = 0.5 * (nA + nB);",
      "    float t = clamp((cross - near * spread) / max(1.0 - spread, 1e-4), 0.0, 1.0);",
      "    col = mix(ca, cb, t);",
      "    judge = mix(jA, jB, t);",
      "  }",
      "  col = mix(col, judge, uMask);",
      // The module's own dither, carried: a half-level of ordered noise so a wide soft gradient in a
      // mirrored panel does not band. It is a half of one level of 255 and it stands at both doors,
      // where the door bar is 6 of 255.
      "  float n = fract(sin(dot(gl_FragCoord.xy, vec2(12.9898, 78.233))) * 43758.5453);",
      // THE COVERAGE: the alpha is the constant 1, and it is a decision rather than a default. A
      // reflection is a map onto the work and the wrap carries whatever falls past its border back
      // into it, so no point of the frame is ever without a point of the work to read.
      "  gl_FragColor = vec4(col + (n - 0.5) / 255.0, 1.0);",
      "}",
    ].join("\n");

    function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
    function clamp01(v) { return clamp(v, 0, 1); }
    function smooth(x) { x = clamp01(x); return x * x * (3 - 2 * x); }
    function smoothstep(a, b, x) { return smooth((x - a) / (b - a)); }
    function num(v, d) { var n = +v; return n === n ? n : d; }

    // ---- THE MODULE'S OWN CONSTANTS, carried digit for digit ------------------------------------
    // THE MIRROR'S OWN LIFE (livemirror.js:318-320, :365-366, :401). Two incommensurate sines on
    // each axis carry the line, and a third carries the breathing zoom. Under a handed second the
    // module's `poseAt` is a pure function of that second — no easing, no grip, no pointer — which
    // is exactly what an instrument of this engine may keep, so the whole of it comes across. What
    // is left behind is the pointer that steers it, the easing that settles it and the module's own
    // rAF clock (§1.2's fence, and §4.4b for the clock — a handle that keeps a clock of its own
    // makes a seeded score draw two different pictures).
    var LINE_X = [0.30, 0.21, 0.4, 0.09, 0.37, 1.7];
    var LINE_Y = [0.26, 0.163, 2.1, 0.10, 0.29, 0.6];
    var BREATH = [0.012, 0.26];
    // How far the mirrored copies past the work's own border fall into the dark, and the module's
    // own resting brightness of the seam (livemirror.js:61, :326). Both are the rest the handles
    // below are published against, so a score that names neither draws the module's own frame.
    var DEPTH_REST = 0.62;
    var GLINT_REST = 0.62;
    // THE ROOM THE FOLD NEEDS AT THE FRAME'S OWN EDGE, and it is the module's own number, named as
    // its own in the module's own words: «with less than a tenth of the frame beyond it the fold has
    // almost nothing left to mirror and the travel goes slack before it goes dead»
    // (livemirror.js:226-229). A score handed a work whose measured line falls nearer an edge than
    // this gets the line held at a tenth, with the hold on the record rather than silent.
    var LINE_EDGE = 0.10;

    // ---- THE PORT'S OWN ONE NUMBER OF THE TRAVEL -------------------------------------------------
    // How much of the hand the wholly mirrored frame stands for, and therefore where the two works
    // exchange. It is centred on the middle of the hand, so the two halves are equal and the
    // module's own dial runs once over each. The exchange has to sit entirely inside the deep fold,
    // because that is the only stretch of this instrument's travel at which neither work is legible
    // as itself and a dissolve therefore shows no photograph coming apart. Eight hundredths is that
    // stretch — half a second at the 6.5 s this engine runs a middle at — and it is the same width
    // the panels instrument settled on for the opposite instant of its own hand, so the two ports
    // hold one number rather than two.
    var HOLD = 0.08;
    var SHUT_IN = 0.5 - HOLD / 2, SHUT_OUT = 0.5 + HOLD / 2;

    /* THE RESPONSE CURVE (SPEC.md Requirement 40, criterion 10, his word 08-08 17:57) IS THE IDENTITY HERE, and that is
       a measured result carried across rather than an omission (livemirror.js:288-294). Walking the
       raw dial in steps of 0.02 and reading the mean channel distance between neighbouring frames —
       the same measurement every door of this engine uses — gives 29.9 channels at the slowest step
       against 42.9 at the fastest, a band of 1.43. The reason is the construction: the dial walks
       the sampling point between a pixel's own place and its reflection, the distance travelled is
       linear in the dial and the picture is equally sharp at both ends, so equal steps already carry
       equal change and the curve is v = u.
       IT IS WRITTEN AS A FUNCTION RATHER THAN LEFT OUT because the hand this port runs is not the
       module's dial: it is two halves with an exchange between them, and the row that measures the
       band measures it on THIS hand. A later reading that finds a band on the port's own travel has
       one place to put its knots. */
    function feelOf(u) { return clamp01(u); }

    // Cover-fit a work into the frame, and nothing beyond it. The module cover-fits its file over
    // its mount and crops nothing (livemirror.js:54-56), so the port asks the host for no crop:
    // `framings` publishes 1 at both doors.
    function fit(iw, ih, w, h) {
      var fa = w / Math.max(h, 1);
      var ia = iw / Math.max(ih, 1);
      if (ia > fa) return [fa / ia, 1, 0, 0];
      return [1, ia / fa, 0, 0];
    }

    // Where the mirror's own line stands at one second, about a named place. At `drift` 0 the line
    // stands exactly where it was named — which is his own condition on this effect, the fold
    // landing on the work's own structural line — and at 1 the two sines are the module's own,
    // amplitude for amplitude and phase for phase. With the place at the middle of the frame and the
    // drift whole, this IS the module's own line at that second.
    function lineAt(place, wander, t, w) {
      return place + wander * (w[0] * Math.sin(t * w[1] + w[2]) + w[3] * Math.sin(t * w[4] + w[5]));
    }

    // The numbers of one frame. Everything the shader gets beyond the seating of the two works is a
    // pure function of the pose; every number in the pose comes from a handle a score can drive, and
    // the mirror's own life reads the second the host hands down, so a seeded run repeats to the
    // pixel.
    function posed(st) {
      var hand = clamp01(num(st.mix, 0));
      // THE HAND'S TWO HALVES. The first work folds into its mirror, the two exchange on the wholly
      // mirrored frame, the second opens back out. The module's own dial runs over each half, so
      // both doors stand at a dial of exactly 0 whatever the hold is.
      var dial = hand <= 0.5
        ? feelOf(clamp01(hand / SHUT_IN))
        : feelOf(1 - clamp01((hand - SHUT_OUT) / (1 - SHUT_OUT)));
      var cross = smoothstep(SHUT_IN, SHUT_OUT, hand);
      var mode = Math.round(clamp(num(st.axis, 2), 0, 3));
      var wander = clamp01(num(st.drift, 0));
      // Under reduced motion the mirror's own life is parked, so nothing drifts and nothing breathes
      // — the same rule the panels instrument applies to its sway.
      var t = st.reduced ? 0 : num(st.clock, 0);
      // WHERE THE FOLD IS ASKED FOR, AND WHERE IT CAN ACTUALLY STAND. Past a tenth of the frame the
      // fold has almost nothing left to mirror, so a place nearer an edge than that is held at the
      // edge's own room and the hold travels on the record beside what was asked for.
      var wantX = clamp01(num(st.centreX, 0.5)), wantY = clamp01(num(st.centreY, 0.5));
      var atX = clamp(wantX, LINE_EDGE, 1 - LINE_EDGE);
      var atY = clamp(wantY, LINE_EDGE, 1 - LINE_EDGE);
      var fx = lineAt(atX, wander, t, LINE_X);
      var fy = lineAt(atY, wander, t, LINE_Y);
      var zoom = 1 + wander * BREATH[0] * Math.sin(t * BREATH[1]);
      return {
        fold: [fx, fy, dial, cross],
        form: [mode, clamp01(num(st.glint, GLINT_REST)), clamp01(num(st.shade, DEPTH_REST)), zoom],
        // read on the diagnostic surface, bound to no uniform: what the hand came to, what the line
        // was asked for and what it was given
        dial: dial, cross: cross, mode: mode, wander: wander, zoom: zoom,
        lineWant: [wantX, wantY], line: [atX, atY],
        lineHeld: (atX !== wantX || atY !== wantY)
          ? [wantX - atX, wantY - atY] : null,
        mask: clamp01(num(st.mask, 0)),
      };
    }

    // ---- THE DOOR THE INSTRUMENT READS FOR ITSELF ------------------------------------------------
    // His 18:00 architecture decision, carried in the U27 brief: the instrument reads its doors at
    // runtime on the actual buffer, and the report it hands back is the runtime truth; what the
    // manifest declares is only the claim. The meshing instrument answered that first, the panels
    // and the box followed; this is the same law read in THIS instrument's own unit, which is the
    // SAMPLE'S OWN TRAVEL — how far the fold moves the point of the work a pixel reads, away from
    // the pixel's own place.
    //
    // WHAT A DOOR ASKS OF THIS INSTRUMENT. At either door the frame is one work standing whole, at
    // the plain cover fit the `framings` block publishes. Four things carry that, and this reads all
    // four ON THE BUFFER rather than declaring them:
    //   · THE FOLD MOVES NOTHING. At a door the dial is nothing and every sample reads its own
    //     place. How far a sample may move before a grid can show it is a question in POINTS of that
    //     grid and not in units of the hand, so it is asked in points.
    //   · NO MIRRORED COPY STANDS IN THE FRAME. The work is cover-fitted, so at the door every
    //     sample falls inside the work's own rectangle; a sample past it is a second copy of the
    //     work standing in the frame, which is not the work standing whole.
    //   · THE TWO WORKS ARE NOT BLENDED. The exchange is nothing at the entry door and whole at the
    //     exit; anything between them is a frame that is neither work.
    //   · THE JUDGES' CHANNEL IS SHUT. `mask` draws the fold map itself as colour, which is what it
    //     is for; left open at a door the frame is a false-colour map of the panels and not the
    //     photograph at all.
    //
    // WHAT THIS READING FINDS, SAID PLAINLY. On every buffer the host can hand and every pose these
    // handles admit, all four come out whole: the hand's own two halves put the dial at exactly 0 at
    // either end, every sample reads its own place, the cover fit leaves no sample outside the work
    // and the exchange stands at its own end. That is not a reason to leave the claim unread — it is
    // the runtime truth this lane was asked for, and it is published as the applied state below,
    // where a suite reads it and a later change to the hand, the hold or the coverage reddens
    // against it.
    var DOOR_SLIP = 0.5;   // points of the grid: half a point, inside which a sample cannot move
    var DOOR_HOLD = 2;     // how far the hold reaches, in points of the grid
    // How much of the fold map may stand in the frame at a door and it still BE the photograph: half
    // a level of 255, under anything the frame itself can carry. The charter's own door bar is 6 of
    // 255 over the canvas rect, and half a level is an eighth of that at one point.
    // CAPABILITY — a fact about the frame's own eight bits rather than about pictures: half of
    // one level of 255 is under the smallest difference the buffer can carry, so a door reading
    // at this bar is reading something the frame could not have shown. Settled once for the nine
    // files that carry it (S-71, 2026-09-03).
    var DOOR_SHOW = 0.5 / 255;

    // The grid the door is read on, and which of the two it is. `drawn` says which one the sentence
    // below names, since a reader told «a 780 x 1688 frame» would look for a device that has none.
    function doorGridOf(st) {
      var bw = Math.round(st.bufWidth), bh = Math.round(st.bufHeight);
      if (bw >= 1 && bh >= 1) return { w: bw, h: bh, drawn: true };
      return { w: Math.round(st.cssWidth), h: Math.round(st.cssHeight), drawn: false };
    }

    // The fold, applied to one point of the frame — FRAG's own branch, carried across line for line,
    // so the reading walks the very map the shader draws.
    function foldPoint(ux, uy, at, mode, ma) {
      var px = (ux - at[0]) * ma, py = uy - at[1];
      var qx = px, qy = py;
      if (mode < 0.5) { qx = -Math.abs(px); }
      else if (mode < 1.5) { qy = -Math.abs(py); }
      else if (mode < 2.5) { qx = -Math.abs(px); qy = -Math.abs(py); }
      else {
        var nx = 0.7071067812, ny = -0.7071067812;
        var h = px * nx + py * ny;
        qx = px - (h + Math.abs(h)) * nx;
        qy = py - (h + Math.abs(h)) * ny;
      }
      return [qx / ma + at[0], qy + at[1]];
    }

    // THE FOLD MAP, READ ON THE BUFFER THE SHADER WILL SAMPLE ON. The map is walked at the buffer's
    // own sample points: its four corners, where a fold near an edge has the least frame to spare;
    // the midpoints of its four edges; the nine points around its centre, where the two creases
    // cross; and the nine points around the fold point itself, which is where the seam stands and
    // where a fold that has moved shows first.
    function mapReadOf(v, W, H, fitv) {
      var ma = W / Math.max(H, 1);
      var at = [v.fold[0], v.fold[1]], dial = v.fold[2], mode = v.form[0], zoom = v.form[3];
      var cov = (fitv && fitv.length >= 2 && fitv[0] > 0 && fitv[1] > 0)
        ? [fitv[0], fitv[1]] : [1, 1];
      var z = 1 + (zoom - 1) * dial;
      var walked = 0, movedPx = 0, outside = 0, worstOver = 0;
      function walk(px, py) {
        var ux = px / W, uy = py / H;
        var f = foldPoint(ux, uy, at, mode, ma);
        var vx = ux + (f[0] - ux) * dial, vy = uy + (f[1] - uy) * dial;
        // how far the fold moved this sample, in points of this grid, read on each axis in that
        // axis's own points because a grid is not square
        var m = Math.max(Math.abs(vx - ux) * W, Math.abs(vy - uy) * H);
        if (m > movedPx) movedPx = m;
        var sx = (vx - 0.5) * cov[0] / z + 0.5, sy = (vy - 0.5) * cov[1] / z + 0.5;
        var over = Math.max(Math.max(-sx, sx - 1), Math.max(-sy, sy - 1));
        if (over > 0) outside++;
        if (over > worstOver) worstOver = over;
        walked++;
      }
      var i, j;
      for (i = 0; i < 2; i++) {
        for (j = 0; j < 2; j++) { walk(i ? W - 0.5 : 0.5, j ? H - 0.5 : 0.5); }
      }
      walk(0.5, H * 0.5); walk(W - 0.5, H * 0.5); walk(W * 0.5, 0.5); walk(W * 0.5, H - 0.5);
      for (i = -1; i <= 1; i++) {
        for (j = -1; j <= 1; j++) { walk(W * 0.5 + i, H * 0.5 + j); }
      }
      for (i = -1; i <= 1; i++) {
        for (j = -1; j <= 1; j++) {
          walk(clamp(at[0] * W + i, 0.5, W - 0.5), clamp(at[1] * H + j, 0.5, H - 0.5));
        }
      }
      return { walked: walked, movedPx: movedPx, outside: outside,
               overPx: worstOver * 0.5 * H, dial: dial, cross: v.fold[3],
               line: [at[0], at[1]], mode: mode, seated: !!(fitv && fitv.length >= 2) };
    }

    // THE DOOR, MEASURED. Null everywhere but at a door, since away from the doors a folding picture
    // is the picture rather than a fault. The door is named by the manifest's own `doors` block:
    // `mix` at 0 is the entry door, where the frame is the departing work whole, and `mix` at 1 the
    // exit door, where it is the arriving one.
    function doorReadOf(v, st) {
      var want = st.mix === 0 ? 1 : (st.mix === 1 ? 0 : -1);
      if (want < 0) return null;
      var g = doorGridOf(st), W = g.w, H = g.h;
      if (!(W >= 1) || !(H >= 1)) return null;
      // The seating of the work THIS door stands: A at the entry door and B at the exit, which is
      // exactly the pair the manifest's own `doors` block names.
      var read = mapReadOf(v, W, H, want ? st.fitA : st.fitB);
      read.grid = g;
      read.want = want;
      read.mask = v.mask;
      return read;
    }

    // THE REFUSAL, worded the way the host's own manifest refusals read: what is wrong, in this
    // instrument's own measured numbers, on the grid it was measured on.
    // PHASE 7, ITEM 5 — RE-ANCHOR CHECKED, NO CHANGE NEEDED, AND THE SENSITIVITY IS VERIFIED RATHER
    // THAN ASSUMED. `mapReadOf`'s `fitv` (line 501, `st.fitA`/`st.fitB`) is the host's own seating,
    // read straight through with no crop of this file's own standing between them — ruling out
    // hero's own class of bug, a second crop multiplied in only inside `fit()` that never cancelled
    // through `seated`. Unlike the fold-collapse instruments (`kaleidoscope`, `tunnel` — where the
    // door reading's own comparison cancels to zero at a door regardless of the framing, because
    // both sides of it are built from the SAME framing), this one is not merely dial-gated to
    // nothing: `sx`/`sy` (line 466) divide the sample by `cov`/`z` on their own, independent of
    // `dial`, so a wrong `fitv` genuinely moves the bound the `outside` count is read against.
    // Planting an oversized `fitA` ([2, 2, 0, 0] against the real [1, 1, 0, 0]) into a throwaway
    // copy and reading `values()` at `mix: 0` reds `doorWhyNo` — "8 of the 26 points this reading
    // walked... read past the departing work's own border" — confirming this row would catch a real
    // seating fault, not only a fold that failed to close.
    function doorWhyNoOf(read) {
      if (!read) return null;
      var g = read.grid, door = read.want ? "the entry" : "the exit";
      var work = read.want ? "departing" : "arriving";
      var other = read.want ? "arriving" : "departing";
      var where = " of a " + g.w + " x " + g.h + (g.drawn ? " buffer" : " frame");
      // THE EXCHANGE IS READ FIRST, BECAUSE IT IS THE WIDEST FAULT. A frame carrying both works is
      // neither of them at any point at all, where every fault below leaves most of the frame right.
      var here = read.want ? read.cross : 1 - read.cross;
      if (here > 0) {
        return door + " door leaks: the two works stand exchanged " + here.toFixed(6)
             + " of the way, so every point of the frame carries part of the " + other + " work "
             + "as well, where " + door + " door's own law asks for the " + work
             + " work at every point";
      }
      if (read.movedPx >= DOOR_SLIP) {
        return door + " door leaks: the fold moves a sample " + read.movedPx.toFixed(2) + " points"
             + where + " off its own place, so the frame is the " + work + " work folded onto its "
             + "own mirror and not standing whole, where " + door + " door's own law asks for the "
             + work + " work at every point";
      }
      if (read.outside) {
        return door + " door leaks: " + read.outside + " of the " + read.walked + " points this "
             + "reading walked" + where + " read past the " + work + " work's own border, the "
             + "worst by " + read.overPx.toFixed(2) + " points, so a second mirrored copy of it "
             + "stands in the frame where " + door + " door's own law asks for the one work whole";
      }
      if (read.mask >= DOOR_SHOW) {
        return door + " door leaks: the judges' own channel stands at " + read.mask.toFixed(6)
             + ", so the frame draws the fold map — the mirrored panels of a " + g.w + " x " + g.h
             + (g.drawn ? " buffer" : " frame") + " — instead of the " + work + " work, where "
             + door + " door's own law asks for the " + work + " work at every point";
      }
      return null;
    }

    // THE NUMBERS OF ONE FRAME, WITH ITS DOOR READ ON THE BUFFER BEING DRAWN. Away from a door this
    // is `posed` and nothing more: the reading is taken nowhere else and no guard moves. At a door
    // it walks its own fold map on the buffer and publishes what it read — how many points it
    // walked, how far the furthest of them was moved by the fold, how many read past the work's own
    // border and by how much. Where a sample stands moved by less than the hold's own reach, the
    // dial is held at exactly nothing and the travel it gave up stays on the record; beyond that,
    // and for an exchange left standing or a judges' channel left open, the refusal stands.
    //
    // WHY THE HOLD IS IN POINTS AND NOT IN THE HAND'S OWN UNITS. A hand of 1e-9 is nothing on a
    // short frame and a whole point on a tall one, so what a door has to answer is «can this grid
    // show the fold», which is a question in points. Two points is the reach, for the same reason
    // the meshing instrument holds two rungs and the panels instrument two points: it closes what a
    // real grid can open, and it leaves the refusal standing rather than making a guard that never
    // fires.
    function values(st) {
      var v = posed(st);
      v.dialRequest = v.dial;
      v.doorHeld = null;
      var read = doorReadOf(v, st);
      var no = doorWhyNoOf(read);
      v.doorGrid = read ? read.grid : null;
      v.foldMap = read ? { walked: read.walked, movedPx: read.movedPx, outside: read.outside,
                           overPx: read.overPx, line: read.line, mode: read.mode,
                           cross: read.cross, seated: read.seated } : null;
      if (!no) { v.doorWhyNo = null; return v; }
      // The hold answers ONE thing: a dial standing a hair off nothing on a grid tall enough to show
      // it. An exchange left standing and a judges' channel left open are different faults and
      // nothing here can close them — the whole frame is wrong rather than a sample of it — so they
      // are refused outright and never held.
      if (read.cross === (read.want ? 0 : 1) && read.mask < DOOR_SHOW
          && read.movedPx >= DOOR_SLIP && read.movedPx < DOOR_HOLD) {
        var w = posed(st);
        w.fold[2] = 0;
        var wRead = doorReadOf(w, st);
        if (!doorWhyNoOf(wRead)) {
          w.dialRequest = v.dial;
          w.dial = 0;
          w.doorHeld = no;
          w.doorWhyNo = null;
          w.doorGrid = wRead.grid;
          w.foldMap = { walked: wRead.walked, movedPx: wRead.movedPx, outside: wRead.outside,
                        overPx: wRead.overPx, line: wRead.line, mode: wRead.mode,
                        cross: wRead.cross, seated: wRead.seated };
          return w;
        }
      }
      v.doorWhyNo = no;
      return v;
    }

    var manifest = {
      id: "livemirror", api: 1, arity: 2,
      // The work folds onto its own mirror, the two works exchange while the frame is wholly
      // mirrored and neither is legible as itself, and the second opens back out of the mirror.
      roles: ["disassembly", "mystery", "assembly"],
      // WHERE THIS STANDS ON THE CHARTER'S SHELF, and the reading is CARRIED rather than re-decided:
      // lab/CROSSING-HISTORY.md's vocabulary table records this module's level as CELL, and that row
      // is his own standing verdict. The fold lines partition the frame into mirrored panels and the
      // motion is what happens to those panels.
      //
      // WORLD IS NOT CLAIMED, and that is the difference between this instrument and the box. No
      // space is folded and no eye travels: the frame is a picture reflected in its own line, which
      // is an event on the CELL level and nowhere above it. That is what makes this instrument
      // reachable at a step whose role has no miracle to spend — which is every quiet link and every
      // return of a walk, where the box may not stand at all.
      //
      // CELL CONTENT is not claimed either. A panel carries the work read at a reflected point, and
      // the reflection is the partition rather than a second thing happening inside a panel.
      levels: ["CELL"],
      // WHAT THIS INSTRUMENT CUTS ON, ADDED 2026-08-31 (cause A, item 5 — the reconciliation).
      // This file never declared the key; the composer's own `INSTRUMENTS.cuts` carried «panel»
      // with no line here to answer for it. The seam note just below says it directly: the fold
      // is a reflection that makes «the two panels the fold makes», the same construction hero's
      // and kaleidoscope's own folds stand on.
      cuts: ["panel"],
      // WHERE THIS INSTRUMENT HAS A SEAM (§8's `seams` block) — and here it has none to declare. The
      // fold is a reflection about the crease, `q = p - (h + abs(h)) * n` in FRAG's own `folded`, and
      // at the crease itself `h` is nothing, so `q` equals `p` and the sampled point on either side of
      // the line is the very same point of the picture: the two panels the fold makes meet with no
      // gap to hide and no hard line for a hairline retouch to round off, the same construction
      // hero's and kaleidoscope's own folds stand on. What this file's own comments call "the seam" —
      // "a thin bright core with a soft lift around it, plus two dark hairlines flanking it" — is not
      // a retouch of that boundary at all: it is glint, a deliberate light the shader lays along an
      // already-seamless crease so a fold reads as a fold, gated by the `glint` handle and drawn only
      // while the dial is off nothing. Unlike the wedge and ring folds hero and kaleidoscope hold an
      // antialiasing width at, this one carries no smoothstep at the coordinate map itself — a
      // straight-line fold has no grazing radius for such a width to guard — so there is no width
      // here for `seams` to publish.
      seams: [],
      params: { axis: [0, 3], centreX: [0, 1], centreY: [0, 1], drift: [0, 1], glint: [0, 1],
                shade: [0, 1], propagate: [0, 0.9] },
      // WHAT THIS INSTRUMENT SHOWS BESIDES A CROSSING (his 19:13 word, the two registers). A picture
      // closing onto its own reflection along a line the picture itself carries is a spectacular
      // atypical event: nothing about the making is explained and nothing is a lesson — the work
      // simply does something no photograph does.
      register: "spectacle",
      // EVERY handle a score can drive (§4.4b). `mix` is the dial and `clock` is the second the host
      // hands down; `axis` and the two centres place the fold; `drift` is the mirror's own life;
      // `glint` and `shade` are the module's own two resting channels; `mask` is the judges'.
      //
      // NO HANDLE HERE KEEPS A CLOCK OR A POINTER OF ITS OWN. The module runs its own rAF loop,
      // reads the pointer across its mount, eases the line toward it with two time constants and
      // brightens the seam while a hand is moving it (livemirror.js:349-387). All of it is gone: the
      // module's own `poseAt` — its pose under a HANDED second, with the grip let go and the easing
      // bypassed — is exactly the pure function an instrument of this engine may keep, and it is
      // what came across. The one place time reaches the picture is `drift`, and that reads the
      // `clock` handle, so a seeded score repeats to the pixel.
      // LEVEL, PER SHELF 17 (docs/design/PASS-API-V1.md:716). This instrument declares one level,
      // CELL — the fold partitions the frame into mirrored panels and every handle below either
      // places that partition or is levelless in the fleet's own idiom. `mix` is the crossing's own
      // dial, `clock` is the module's own time, and `shade` is the fleet's own judge-idiom name
      // (held levelless here as everywhere it appears, though this instrument's own prose calls it a
      // "resting channel" rather than a judges' channel); `mask` is the judges' channel proper.
      // `glint` — the fold line's own brightness — is honestly a LIGHT-COLOUR reading, which this
      // instrument does not declare, so it is held at CELL under the HARD CONSTRAINT above, as the
      // seam's own finish on the CELL boundary it lights; named here and in this port's report.
      handles: {
        mix: { min: 0, max: 1, def: 0, level: null },
        clock: { min: 0, max: 14, def: 0, level: null },
        // WHICH FOLD. The module's own `mode`, with its four names. The module rebuilds nothing when
        // the mode changes and neither does this, so the handle is a plain number a score can hold
        // or step and the frame answers it at once. It rests at BOTH, which is his own taste-
        // approved vista state for this effect (TASTE.md, the vista presets of 08-08
        // 11:39: «livemirror both/stairwell/drift on»).
        axis: { min: 0, max: 3, def: 2, kind: "enum", step: 1,
                names: { "0": "the fold stands upright", "1": "the fold lies flat",
                         "2": "both folds at once", "3": "the fold runs diagonally" },
                unit: "which way the picture folds onto itself",
                reads: "the banding axis lab/data/cut-lines.json recorded for the pivot — the "
                     + "direction the two works' own structure runs, so the fold line lies ALONG "
                     + "that structure rather than across it, which is what his standing verdict on "
                     + "this effect asks for: the fold lines land on the work's own lines",
                level: "CELL" },
        // WHERE THE FOLD STANDS. His standing verdict on this effect in one pair of handles. The
        // module's line is placed by a pointer and wanders on its own when nobody holds it; here it
        // is placed by the pair's own measured structural line on the axis the fold actually stands
        // on — `structure.regions.line.{x,y}.at`, the same reading boxfold's own crease reads — and
        // falls back to the pair's own measured radial centre where neither work carries one.
        centreX: { min: 0, max: 1, def: 0.5,
                   unit: "where across the frame the upright fold stands",
                   reads: "structure.regions.line.x.at — the midpoint of the two works' own "
                        + "measured structural line on this axis, the place their own picture "
                        + "falls into two regions, so a vertical fold lands on the line a mirror "
                        + "fold has to land on for the reflection to read as the work's own and "
                        + "not as a line drawn over it. Falls back to the midpoint of the two "
                        + "works' measured radial centres, structure.radial.centre, where neither "
                        + "work carries a readable line on this axis",
                   applied: { roomAtTheEdge: LINE_EDGE },
                   level: "CELL" },
        centreY: { min: 0, max: 1, def: 0.5,
                   unit: "where down the frame the flat fold stands",
                   reads: "structure.regions.line.y.at, read the same way as centreX on the other "
                        + "axis, with the same radial-centre fallback where neither work carries a "
                        + "readable line",
                   applied: { roomAtTheEdge: LINE_EDGE },
                   level: "CELL" },
        // THE MIRROR'S OWN LIFE, ON ONE ENVELOPE (charter shelf 5: properties that belong to one
        // gesture hang on one scalar, so they cannot disagree). One handle carries how far the fold
        // line wanders about the place it was given AND how deep the picture breathes, because both
        // are the same thing — the mirror living rather than standing — and a score that turned one
        // up and the other down would be asking the mirror to be alive and still at once.
        //
        // IT RESTS AT NOTHING, and that is his verdict applied rather than a taste of this port's:
        // a wandering fold line does not land on the work's own structural line. At 1 the two sines
        // on each axis and the breath are the module's own, amplitude for amplitude and phase for
        // phase, so the module's own frame is a value of this handle rather than a state that was
        // lost.
        drift: { min: 0, max: 1, def: 0,
                 unit: "how far the mirror lives about the place it was given",
                 reads: "the fractional part of the two works' measured spectral periods in ratio, "
                      + "charter shelf 13's incommensurate-period instrument — which is what this "
                      + "wander already is: two incommensurate sines on each axis and a third on "
                      + "the breath",
                 applied: { lineX: LINE_X, lineY: LINE_Y, breath: BREATH,
                            restsAt: "the place the two centres name" },
                 level: "CELL" },
        // HOW FAR APART THE MIRRORED COPIES' OWN EXCHANGES STAND — the charter's PROPAGATED
        // arrival (shelf 7), where it reaches this instrument's pixels. This is the one instrument
        // of the fleet that makes MIRRORED COPIES of a work, so it is the one that can say what
        // that arrival says: the change runs through the copies with the further one changing
        // first. At nothing every copy exchanges at the same instant, which is the picture this
        // instrument drew before the handle existed and the picture every other arrival asks for.
        propagate: { min: 0, max: 0.9, def: 0,
                     unit: "how far apart the mirrored copies' own exchanges stand, as a share of "
                         + "the crossing",
                     reads: "structure.rotational.score of the ARRIVING work — how strongly that "
                          + "work already reads as its own copies repeated about a centre, which is "
                          + "the very reading the composer ranks the charter's PROPAGATED arrival "
                          + "on. A work that plainly IS its own copies propagates the change "
                          + "through them over most of the crossing; one that barely reads as "
                          + "copies exchanges nearly at once",
                     applied: { furtherCopiesFirst: true,
                                copyReadOffTheSameSmoothstepAs: "shade",
                                restsAt: "both doors, where no copy has anything to exchange" },
                     level: "CELL" },
        // THE MODULE'S OWN TWO RESTING CHANNELS, published at the rests the module holds them at.
        glint: { min: 0, max: 1, def: GLINT_REST,
                 unit: "the fold line's own brightness",
                 applied: { moduleRest: GLINT_REST, heldByAHand: 1,
                            restsAt: "both doors, where the dial gates it to nothing" },
                 level: "CELL" },
        shade: { min: 0, max: 1, def: DEPTH_REST,
                 unit: "how deep each further mirrored copy falls into the dark",
                 applied: { moduleRest: DEPTH_REST, reach: 0.60,
                            restsAt: "both doors, where no copy stands in the frame" },
                 level: null },
        // THE MEASUREMENT THIS HANDLE IS READ AGAINST AT A DOOR, published beside its range the way
        // the meshing instrument publishes its own. `readAtADoor` says what is read (this
        // instrument's own fold map, walked at the buffer's own sample points), on which grid (the
        // drawing buffer the host binds, with the CSS frame where it hands none), how far the hold
        // reaches (two points of that grid, for a dial standing a hair off nothing) and what the
        // reading is counted in.
        mask: { min: 0, max: 1, def: 0,
                applied: { readAtADoor: { points: DOOR_HOLD, readOn: "the drawing buffer",
                                          reads: "the sample's own travel",
                                          measures: "this instrument's own fold map, walked at the "
                                                  + "buffer's own sample points, and how far the "
                                                  + "fold moves each of them off its own place" } },
                level: null },
      },
      neutrals: { a: 0, b: 1 },
      doors: { in: { handle: "mix", value: 0, work: "a" },
               out: { handle: "mix", value: 1, work: "b" } },
      // Both doors frame alike, and both are the PLAIN COVER FIT: the module cover-fits its file
      // over its mount and the breathing zoom is gated by the dial, which stands at nothing at
      // either end. So neither door is cropped and neither is upscaled.
      framings: { "0": { coverCrop: 1 }, "1": { coverCrop: 1 } },
      drivers: ["progress", "cueProgress", "time", "velocity", "capability", "noise", "static",
                "curve", "spline", "map", "add", "multiply", "mix", "clamp", "hold", "segment",
                "ramp", "slew", "oscillate", "node"],
      camera: { needs: "none", authority: "stage" },
      gl: { preserveDrawingBuffer: false },
      // WHAT THIS INSTRUMENT WRITES WHERE ITS OWN MATTER IS ABSENT (§7's coverage law, and the
      // per-instrument specification in docs/design/COVERAGE.md). It is absent nowhere, and unlike
      // the two instruments that cut on panels before it, nothing had to be bought for that: a
      // reflection is a map ONTO the work rather than a rearrangement of pieces of it, so every
      // point of the frame has a point of the work to read at every mark of the hand. The alpha is
      // the constant 1, said as a decision. Under the placement rule this instrument is lawful as
      // the lowest cue of a stack and as a whole one-cue score.
      coverage: { writes: false,
                  how: "the work is cover-fitted over the frame and the fold is a reflection, which "
                     + "maps every point of the frame onto a point of the work; whatever the fold "
                     + "sends past the work's own border is carried back into it by the mirrored "
                     + "wrap the shader writes, so no point of the frame is ever without a point of "
                     + "the work to read and the alpha is the constant 1" },
      // The neutral pose is the ENTRY DOOR — `mix` at 0, the value the `doors` block above names —
      // so the frame keys the host reads off it at registration include the door's own record.
      neutralPose: { mix: 0, axis: 2, centreX: 0.5, centreY: 0.5, drift: 0, propagate: 0,
                     glint: GLINT_REST, shade: DEPTH_REST, mask: 0, clock: 0,
                     reduced: false, cssWidth: 1000, cssHeight: 1000 },
      passes: [{
        program: "livemirror", vert: VERT, frag: FRAG, position: "aPos",
        uniforms: [
          { name: "uA", type: "sampler2D", source: "textureA" },
          { name: "uB", type: "sampler2D", source: "textureB" },
          { name: "uFitA", type: "vec4", source: "fitA" },
          { name: "uFitB", type: "vec4", source: "fitB" },
          { name: "uRes", type: "vec2", source: "resolution" },
          { name: "uFold", type: "vec4", source: "frame:fold" },
          { name: "uForm", type: "vec4", source: "frame:form" },
          { name: "uMask", type: "float", source: "handle:mask" },
          { name: "uProp", type: "float", source: "handle:propagate" },
        ],
      }],
      // The instrument allocates nothing of its own: it spends the two source-texture slots the host
      // already holds and the one programme the host builds from this manifest. The module's own
      // canvas, its context, its two textures with their mirrored wrap, its resize observer and its
      // own frame loop are what this port does without.
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
                   programs: 1, passes: 1, bytesEstimate: 2000076, variant: "lean" },
                   standard: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0,
                               programs: 1, passes: 1, bytesEstimate: 8000076,
                               variant: "standard" },
                   rich: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                           passes: 1, bytesEstimate: 32000076, variant: "rich" } },
      capabilities: ["webgl2"],
      decline: ["one work only", "a source that never decoded"],
      provenance: { labPath: "lab/effects/livemirror.js", commit: "fc885a3",
                    sha256: "0ba04829a423da60a519f983492141bfb11d243fe54f4d78d17bf2657875b655" },
      readiness: "production-ready",
    };

    var live = false;
    return {
      name: "livemirror",
      manifest: manifest,
      values: values,
      fit: fit,
      feel: feelOf,
      // WHAT THIS INSTRUMENT'S `feel` PROMISES (Phase 7, item 3b): identity-because-no-travel.
      // `feelOf` at livemirror.js:323 is the raw dial, clamped and nothing else — a written "no"
      // rather than a silence, and the generic law asks nothing of a curve that was never claimed.
      feelClass: "identity",
      prepare: function (o) {
        if (!o.sources) return { take: false, why: "the live-mirror instrument needs both works" };
        if (!o.cue) return { take: false, why: "no cue names it" };
        return { take: true };
      },
      start: function () { live = true; },
      // The pose the shader draws. The module's canvas, its frame loop, its pointer and its easing
      // are gone, so every number here comes from a handle a score drives, and the mirror's own life
      // reads the second the host hands down.
      //
      // A DOOR THIS INSTRUMENT CANNOT KEEP WHOLE IS REFUSED RATHER THAN DRAWN. The door law is the
      // instrument's own claim (the manifest's coverage line above), so the instrument is what
      // answers for it: at either door it walks its own fold map on the buffer the host is about to
      // bind and, where the fold moves a sample further than the hold reaches, where a sample reads
      // past the work's own border, where the two works stand exchanged or where the judges'
      // channel is left open, it hands the host the reason with the measured map in it instead of
      // drawing a door that is not the photograph. The host recovers the transaction on that reason
      // and the walk's own glide carries the visitor, which is the product's own behaviour with no
      // renderer.
      frame: function (st) {
        if (!live) return;
        var h = st.handles;
        var pose = {
          mix: h.mix, axis: h.axis, centreX: h.centreX, centreY: h.centreY, drift: h.drift,
          glint: h.glint, shade: h.shade, mask: h.mask, clock: h.clock, reduced: st.reduced,
          // BOTH WORKS' SEATING, as the host hands it down since 2026-08-17, so the door's own
          // reading walks the very cover fit the shader will sample through rather than assuming
          // one. Read defensively: a host that carries none leaves the reading at the plain square,
          // which is the seating with the least frame to spare and can only ever over-hold.
          fitA: st.fitA, fitB: st.fitB,
          cssWidth: st.viewport.w, cssHeight: st.viewport.h,
          // THE GRID THE SHADER WILL SAMPLE ON, carried into the pose so the door is read on the
          // buffer the host is about to bind as `uRes` rather than on the CSS frame around it. The
          // host settles it from the device ratio and its own resolution step, so it moves while a
          // pass plays and each door is read on the grid standing at that door's own instant.
          bufWidth: st.viewport.bufferW, bufHeight: st.viewport.bufferH,
        };
        // AT A DOOR THE INSTRUMENT SAYS WHAT IT APPLIED, and says it before it refuses. The reading
        // is taken on the buffer this frame is drawn on, so it is the run-time truth his 18:00
        // decision asks for. `request` is the dial the hand came to and `applied` is the dial this
        // grid was actually drawn with, so `moved` is the travel the hold took away.
        if (h.mix === 0 || h.mix === 1) {
          var v = values(pose);
          if (st.reportApplied) {
            st.reportApplied({
              door: h.mix === 0 ? "in" : "out",
              buffer: [pose.bufWidth, pose.bufHeight],
              reads: "the sample's own travel", request: v.dialRequest, applied: v.dial,
              moved: v.dial - v.dialRequest, unit: "the dial's own units",
              // What the fold itself was doing over the frame at this door, in the grid's own
              // points, and where the line was asked to stand against where it could.
              movedPx: v.foldMap ? v.foldMap.movedPx : null,
              outside: v.foldMap ? v.foldMap.outside : null,
              line: v.line, lineWant: v.lineWant, lineHeld: v.lineHeld,
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
    instrument: livemirrorInstrument(),
  });
})();
