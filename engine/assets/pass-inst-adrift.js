/*!pass-inst-adrift.js*/
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
  // THE ADRIFT INSTRUMENT (§8) — lab/effects/adrift.js carried across
  // ================================================================================================
  // WHAT THE VISITOR SEES. A dense thing stands in an empty field. It leaves alone across that
  // emptiness — travelling, turning, shrinking, coming apart grain by grain — while the field stays.
  // The field itself then changes hands along a front the two works' own measurements aim, with a
  // band of interlocking fingers round it. The second work's thing arrives out of the far side and
  // settles into its own measured place. The two things never touch: the first is wholly gone by
  // 0.47 of the travel and the second begins at 0.53, so for six hundredths of the hand the frame
  // holds an emptiness that belongs to neither work.
  //
  // WHY IT STANDS HERE. It publishes CELL CONTENT, the level no landed instrument occupies, and it
  // cuts on named regions, which is what 570 declined pairs ask for. Its own motif fires on none of
  // those 570 pairs, so it plays on the elements a plan hands it through the handles below rather
  // than on a motif reading of its own. That qualification is the analysis's own and is recorded
  // here rather than smoothed over.
  //
  // What came over: the shader, the field, the two silhouettes with their measured thresholds, the
  // contact shadow, the seating of a work in the frame (coverFit), the measured response curves,
  // and the numbers of one frame (values). What stayed behind: its own canvas, its own WebGL 1
  // context, its own frame loop, its resize observer and its own accumulated clock (§1.2's fence).
  //
  // ------------------------------------------------------------------------------------------------
  // THE FOUR TEXTURES, AND WHY TWO CARRY IT
  // ------------------------------------------------------------------------------------------------
  // The lab module binds four: `uA`, `uB` — the two works — and `uGA`, `uGB`, each work's GROUND
  // PLATE. A plate is the file with the thing's own region filled in by a push-pull pyramid inpaint
  // and the work's measured film grain laid back over the fill (adrift.js:474-602). Outside the
  // filled region a plate is the file byte for byte. The plate's one job is the hole: a thing that
  // travels leaves the place it stood, and in a module that is alone on the screen that place has to
  // be filled with something.
  //
  // THE PLATES ARE NOT DERIVABLE HERE, and the reading says so plainly. The fill is a pyramid of
  // halvings carried by a known-or-unknown weight with eight relaxation sweeps at every level. A
  // fragment shader sees one point and its own sampler, so it can reach neither the weight nor the
  // levels; the mip chain of the source carries the thing's own colour into every level and answers
  // a different question. Building a plate needs a second canvas and a read of the pixels, which
  // §1.2 puts outside this file.
  //
  // WHAT ANSWERS IT IS THE COVERAGE LAW OF 12:40, which landed after that obstacle was written down.
  // An instrument writes opaque where its own matter stands and clear where its matter is absent,
  // and the space between its elements belongs to whatever plays underneath. The vacated place is
  // exactly where this instrument has no matter: the content has left it, and no picture of this
  // instrument's own stands there. So the port publishes it as its absence rather than inventing a
  // fill for it, and the cue beneath draws it. The plates answered a module standing alone; a voice
  // in a stack has a truer answer to the same question.
  //
  // WHAT THIS COSTS, said out loud. Where the score gives this instrument nothing beneath it, the
  // vacated place falls to the work's own measured ground colour — one flat colour where the plate
  // carried a gradient and a grain. That is the placement rule COVERAGE.md §3.3 already states for
  // `matter`: an instrument that publishes an absence is scored over something.
  //
  // ------------------------------------------------------------------------------------------------
  // WHAT MOVED INTO THE SHADER, AND WHY
  // ------------------------------------------------------------------------------------------------
  // The module reads the frame's aspect from a uniform of its own; it is the ratio of the two
  // numbers bound as `resolution`, so it is computed from those, as the three landed instruments
  // already do. Beyond that one line, the measured place of each thing arrives in the units the
  // measurement was written in — a share of the FILE — and the seating of a file in the frame is the
  // host's own `fitA`/`fitB`. So `outOf`, the inverse of the `into` the shader already carries, maps
  // each measured place through the seating the host actually applied, and everything that follows
  // from those two places — the object line, the handover front's axis, how far its ladder runs over
  // the frame, and the four numbers that are normalized by that run — stands where the fit and the
  // buffer size are known. The arithmetic is the module's own, character for character; the place it
  // stands in moved from the module's JS to the shader because that is where the host's two numbers
  // are.
  //
  // THE PRESERVED DRAWING BUFFER. The module asks its own context for one (adrift.js:661) and §7
  // refuses it. The flag stood in for a redraw: the module draws on demand — from onParam, from
  // resize — and between two such draws the browser hands back the frame that was already there.
  // The host draws every frame of a running transaction and redraws on every resize, so the frame
  // the compositor shows is one this instrument drew for it.
  function adriftInstrument() {
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
      // each work's own ground colour, read outside its measured box
      "uniform vec4 uVoidA;",
      "uniform vec4 uVoidB;",
      // where each thing stands at its own door, as a share of the FILE
      "uniform vec2 uHomeA;",
      "uniform vec2 uHomeB;",
      // how far each has travelled down the object line, frame heights
      "uniform vec2 uTrav;",
      // scale, cos turn, sin turn
      "uniform vec4 uPoseA;",
      "uniform vec4 uPoseB;",
      // the density each silhouette is cut at, now
      "uniform vec2 uThr;",
      // and at its own door, which is where the measured place stands
      "uniform vec2 uThr0;",
      // how much of each thing is still in the frame at all
      "uniform vec2 uLive;",
      // the ground's coarse grain and the fine one that shatters the front
      "uniform vec2 uGrain;",
      // where the grain has drifted to, in cells
      "uniform vec2 uDrift;",
      // one cell, the fingers' depth, the front's travel, the pair's lean
      "uniform vec4 uField;",
      // the counter-motion of the two grounds
      "uniform float uDrag;",
      // the contact shadow's gate: exactly zero at both doors
      "uniform float uGuard;",
      "uniform float uSeed;",
      // the judges' handle: the two silhouettes as colour
      "uniform float uMask;",
      // A fifth of the threshold is the die's, so a thing comes apart in an order that is mostly its
      // own density and partly the score's number (adrift.js:339).
      "const float JITTER = 0.20;",
      // Six parts the plain ladder against four parts the grain, read as the front's own displacement
      // at the scale of one cell (adrift.js:335, :845).
      "const float LADDER = 0.6;",
      // How far the contact shadow reaches, in screen points: a thing lying on the emptiness rather
      // than floating a storey above it (adrift.js:331).
      "const float SHADOW_PX = 4.5;",
      "float h11(vec2 i){ return fract(sin(dot(i, vec2(41.317, 289.107)) + uSeed) * 43758.5453); }",
      // value noise with its own exact gradient: the grain of the ground, and the way it drags
      "vec3 vnoise(vec2 p){",
      "  vec2 i = floor(p), f = fract(p);",
      "  float a = h11(i), b = h11(i + vec2(1.0, 0.0));",
      "  float c = h11(i + vec2(0.0, 1.0)), d = h11(i + vec2(1.0, 1.0));",
      "  vec2 u = f * f * (3.0 - 2.0 * f);",
      "  vec2 du = 6.0 * f * (1.0 - f);",
      "  float k = a - b - c + d;",
      "  float v = a + (b - a) * u.x + (c - a) * u.y + k * u.x * u.y;",
      "  return vec3(v, ((b - a) + k * u.y) * du.x, ((c - a) + k * u.x) * du.y);",
      "}",
      "vec2 into(vec2 p, vec4 f){",
      "  return clamp((p - 0.5) * f.xy + 0.5 + f.zw, 0.0008, 0.9992);",
      "}",
      // the seating read backwards: a place measured on the file, put where the host seated it
      "vec2 outOf(vec2 q, vec4 f){ return (q - 0.5 - f.zw) / f.xy + 0.5; }",
      "vec3 texA(vec2 p){ return texture2D(uA, into(p, uFitA)).rgb; }",
      "vec3 texB(vec2 p){ return texture2D(uB, into(p, uFitB)).rgb; }",
      "void main(){",
      "  vec2 uv = vUv;",
      "  float aspect = uRes.x / max(uRes.y, 1.0);",
      "  vec2 p = vec2(uv.x * aspect, uv.y);",
      "  float h = 1.0 / max(uRes.y, 1.0);",

      // ---- the two measured places, and the line between them ------------------------------------
      "  vec2 hA = outOf(uHomeA, uFitA);",
      "  vec2 hB = outOf(uHomeB, uFitB);",
      "  vec2 vv = vec2((hB.x - hA.x) * aspect, hB.y - hA.y);",
      "  float vl = length(vv);",
      "  vv = vl < 1e-3 ? vec2(1.0, 0.0) : vv / vl;",
      "  vec2 ln = vec2(vv.x / max(aspect, 0.05), vv.y);",
      "  vec2 cenA = hA - ln * uTrav.x;",
      "  vec2 cenB = hB - ln * uTrav.y;",
      // THE FRONT LEANS TOWARD HORIZONTAL BY THE WORKS' OWN HORIZONS: a pair with no waterline in it
      // crosses along the object line alone, a pair that carries one crosses along its own.
      "  vec2 axis = vec2(vv.x * (1.0 - uField.w), vv.y * (1.0 - uField.w) + uField.w);",
      "  axis /= max(length(axis), 1e-4);",
      // how far the projection runs over the frame, so the ladder spans exactly 0 to 1
      "  vec2 ee = vec2(aspect * axis.x, axis.y);",
      "  float lo = min(min(0.0, ee.x), min(ee.y, ee.x + ee.y));",
      "  float sp = max(max(max(0.0, ee.x), max(ee.y, ee.x + ee.y)) - lo, 1e-4);",
      "  float grainW = 2.0 * ((1.0 - LADDER) / LADDER) * uField.x / sp;",
      "  float fine = 2.0 * uField.y / sp;",
      "  float band = (1.2 * uField.y + 0.03) / sp;",
      "  float margin = 0.03 + 0.5 * (grainW + fine);",
      "  float tau = -margin + (1.0 + 2.0 * margin) * uField.z;",

      // ---- THE FIELD. Six parts the plain ladder across the frame along the front the two works'
      //      own measurements aim, four parts a seeded grain. The ladder is read from the far end,
      //      so each work's emptiness gives way starting at its own end of the line.
      "  vec3 n1 = vnoise(p * uGrain.x + uDrift);",
      "  vec3 n2 = vnoise(p * uGrain.y - uDrift * 1.7);",
      "  float ladder = 1.0 - (dot(p, axis) - lo) / sp;",
      "  float F0 = ladder + grainW * (n1.x - 0.5);",
      "  vec2 gF0 = -axis / sp + grainW * n1.yz * uGrain.x;",
      // ---- THE INTERLOCKING BAND. Near the front, and only there, a finer grain enters the field,
      //      so the boundary between the two emptinesses is a band of fingers of one ground inside
      //      the other. It is widest at the middle of the hand, which is the emptiest instant.
      "  float ec = F0 - tau;",
      "  float near = exp(-(ec * ec) / max(band * band, 1e-6));",
      "  vec2 gNear = near * (-2.0 * ec / max(band * band, 1e-6)) * gF0;",
      "  float F = F0 + fine * near * (n2.x - 0.5);",
      "  vec2 gF = gF0 + fine * (near * n2.yz * uGrain.y + (n2.x - 0.5) * gNear);",
      "  float grad = max(length(gF), 1e-5);",
      // 1 is the first work's ground, 0 the second's, and the boundary is one point wide, always
      "  float covV = clamp(0.5 + (F - tau) / (grad * h), 0.0, 1.0);",
      // ---- THE DRAG. The two grounds are pushed against each other along the front's own normal and
      //      nowhere else: away from the band there is nothing to push and the emptiness stands.
      "  vec2 flow = gF0 / max(length(gF0), 1e-5);",
      "  vec2 drag = vec2(flow.x / max(aspect, 0.05), flow.y) * (uDrag * near);",

      // ---- THE EMPTINESS ITSELF. The lab module reads its two ground plates here. This instrument
      //      reads the two works, and publishes the vacated place below as its own absence.
      "  vec2 qHA = uv + drag;",
      "  vec2 qHB = uv - drag;",
      "  vec3 baseA = texA(qHA);",
      "  vec3 baseB = texB(qHB);",
      "  vec3 col = mix(baseB, baseA, covV);",

      // ---- THE FIRST WORK'S THING, leaving. The frame point is mapped back into its home frame —
      //      un-turned, un-scaled, un-travelled — so what crosses the emptiness is a piece of the
      //      work rather than a stencil.
      "  vec2 relA = vec2((uv.x - cenA.x) * aspect, uv.y - cenA.y);",
      "  relA = vec2(uPoseA.y * relA.x + uPoseA.z * relA.y, -uPoseA.z * relA.x + uPoseA.y * relA.y);",
      "  relA /= max(uPoseA.x, 1e-3);",
      "  vec2 qA = hA + vec2(relA.x / max(aspect, 0.05), relA.y) + drag;",
      "  float fpA = h / max(uPoseA.x, 1e-3);",
      // the silhouette is the picture's own distance from its own ground colour, cut at the threshold
      // the measured share names; the order it dissolves in is that density jittered by the field's
      // own seeded grain
      "  float thrA = uThr.x * (1.0 + JITTER * (n1.x - 0.5));",
      "  vec3 pixA = texA(qA);",
      "  float dA = length(pixA - uVoidA.rgb) - thrA;",
      "  float axA = length(texA(qA + vec2(fpA, 0.0)) - uVoidA.rgb) - length(texA(qA - vec2(fpA, 0.0)) - uVoidA.rgb);",
      "  float ayA = length(texA(qA + vec2(0.0, fpA)) - uVoidA.rgb) - length(texA(qA - vec2(0.0, fpA)) - uVoidA.rgb);",
      "  float gA = max(length(vec2(axA, ayA)) / (2.0 * fpA), 1e-4);",
      "  float covA = clamp(0.5 + dA / (gA * fpA), 0.0, 1.0);",

      // ---- THE SECOND WORK'S THING, arriving into the same emptiness and settling into its place.
      "  vec2 relB = vec2((uv.x - cenB.x) * aspect, uv.y - cenB.y);",
      "  relB = vec2(uPoseB.y * relB.x + uPoseB.z * relB.y, -uPoseB.z * relB.x + uPoseB.y * relB.y);",
      "  relB /= max(uPoseB.x, 1e-3);",
      "  vec2 qB = hB + vec2(relB.x / max(aspect, 0.05), relB.y) - drag;",
      "  float fpB = h / max(uPoseB.x, 1e-3);",
      "  float thrB = uThr.y * (1.0 + JITTER * (n2.x - 0.5));",
      "  vec3 pixB = texB(qB);",
      "  float dB = length(pixB - uVoidB.rgb) - thrB;",
      "  float axB = length(texB(qB + vec2(fpB, 0.0)) - uVoidB.rgb) - length(texB(qB - vec2(fpB, 0.0)) - uVoidB.rgb);",
      "  float ayB = length(texB(qB + vec2(0.0, fpB)) - uVoidB.rgb) - length(texB(qB - vec2(0.0, fpB)) - uVoidB.rgb);",
      "  float gB = max(length(vec2(axB, ayB)) / (2.0 * fpB), 1e-4);",
      "  float covB = clamp(0.5 + dB / (gB * fpB), 0.0, 1.0);",

      // ---- THE MEASURED PLACE, READ IN THE FRAME THIS INSTRUMENT DREW. The same silhouette, at the
      //      same construction, standing where the measurement put it and cut at the threshold its
      //      own door carries. It says where each work's own content stands in the emptiness above,
      //      and the difference between it and the travelling silhouette is the place the thing has
      //      left — the region this instrument carries nothing in.
      "  float hthrA = uThr0.x * (1.0 + JITTER * (n1.x - 0.5));",
      "  float hdA = length(baseA - uVoidA.rgb) - hthrA;",
      "  float hxA = length(texA(qHA + vec2(h, 0.0)) - uVoidA.rgb) - length(texA(qHA - vec2(h, 0.0)) - uVoidA.rgb);",
      "  float hyA = length(texA(qHA + vec2(0.0, h)) - uVoidA.rgb) - length(texA(qHA - vec2(0.0, h)) - uVoidA.rgb);",
      "  float hgA = max(length(vec2(hxA, hyA)) / (2.0 * h), 1e-4);",
      "  float holeA = clamp(clamp(0.5 + hdA / (hgA * h), 0.0, 1.0) - covA, 0.0, 1.0);",
      "  float hthrB = uThr0.y * (1.0 + JITTER * (n2.x - 0.5));",
      "  float hdB = length(baseB - uVoidB.rgb) - hthrB;",
      "  float hxB = length(texB(qHB + vec2(h, 0.0)) - uVoidB.rgb) - length(texB(qHB - vec2(h, 0.0)) - uVoidB.rgb);",
      "  float hyB = length(texB(qHB + vec2(0.0, h)) - uVoidB.rgb) - length(texB(qHB - vec2(0.0, h)) - uVoidB.rgb);",
      "  float hgB = max(length(vec2(hxB, hyB)) / (2.0 * h), 1e-4);",
      "  float holeB = clamp(clamp(0.5 + hdB / (hgB * h), 0.0, 1.0) - covB, 0.0, 1.0);",
      "  float hole = mix(holeB, holeA, covV);",

      // ---- THE CONTACT SHADOW. A thing lies on the emptiness, so the emptiness darkens at its edge
      //      and the darkening decays outward. It is read as the silhouette itself, stepped back
      //      along the light three times with a falling weight, because the distance a linearised
      //      coverage reports is the picture's own gradient. The gate is exactly zero at both doors,
      //      and each half of it is zero while its own thing is not in the frame at all.
      "  vec2 shDir = SHADOW_PX * ln;",
      "  float shA = uLive.x * (1.0 - covA) * (",
      "      0.55 * step(thrA, length(texA(qA + shDir * fpA) - uVoidA.rgb))",
      "    + 0.30 * step(thrA, length(texA(qA + shDir * fpA * 2.2) - uVoidA.rgb))",
      "    + 0.15 * step(thrA, length(texA(qA + shDir * fpA * 3.8) - uVoidA.rgb)));",
      "  float shB = uLive.y * (1.0 - covB) * (",
      "      0.55 * step(thrB, length(texB(qB + shDir * fpB) - uVoidB.rgb))",
      "    + 0.30 * step(thrB, length(texB(qB + shDir * fpB * 2.2) - uVoidB.rgb))",
      "    + 0.15 * step(thrB, length(texB(qB + shDir * fpB * 3.8) - uVoidB.rgb)));",
      "  col *= 1.0 - 0.34 * uGuard * max(shA, shB);",
      "  col = mix(col, pixA, covA);",
      "  col = mix(col, pixB, covB);",
      // the judges' own frame: the two silhouettes as colour, so a check reads on the picture whether
      // the two things ever stand on one point. It carries no coverage of its own, because what it is
      // for is to be read as colour.
      "  col = mix(col, vec3(covA, covB, 0.0), uMask);",
      // THE COVERAGE, PREMULTIPLIED, which is the form the host blends: it lays a cue down with
      // `ONE, ONE_MINUS_SRC_ALPHA`, so the colour a fragment hands over is the colour it contributes
      // and the alpha is how much of the frame beneath it hides. Where this instrument carries
      // nothing it contributes nothing and hides nothing, and the cue underneath stands. Played with
      // nothing underneath, the cleared buffer stands there instead, which is the same sentence read
      // against an empty stack.
      "  float a = mix(1.0 - hole, 1.0, uMask);",
      "  gl_FragColor = vec4(col * a, a);",
      "}",
    ].join("\n");

    function smoothstep(a, b, x) {
      var t = (x - a) / (b - a);
      t = t < 0 ? 0 : t > 1 ? 1 : t;
      return t * t * (3 - 2 * t);
    }
    function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }

    // WHAT THE HAND'S OWN TRAVEL IS MADE OF (adrift.js:312-313). The first thing is wholly gone by
    // 0.47 and the second begins at 0.53, so six hundredths of the hand hold an emptiness that
    // belongs to neither work, and «the two things never touch» is a fact of construction. The field
    // changes hands across the middle five and a half tenths: under 0.14 the emptiness is entirely
    // the first work's and the thing leaves across a ground that stays.
    var DEPART = 0.47, ARRIVE = 0.53;
    var FRONT_FROM = 0.14, FRONT_TO = 0.86;
    // HOW FAR A THING MAY TRAVEL, as a multiple of the pair's own smaller void share: a frame nine
    // tenths empty has nine tenths of a frame to cross (adrift.js:320).
    var FLIGHT_OF_VOID = 1.15;
    var TURN_MAX = 0.42;         // radians a thing turns across its whole leaving or arriving
    var SHRINK_MAX = 0.72;       // how far down the shrink handle may take its size
    // How far the two grounds are dragged past each other at the front, in frame heights, and the
    // crop that pays for it. ZOOM is derived from DRAG and is no free number.
    var DRAG = 0.06, ZOOM = 1 + 2 * DRAG + 0.05;
    // How coarse the ground's own grain may be, in cells across the frame's height. Under about five
    // the field stops being a material; over about thirty-three a cell is finer than the film grain
    // of these photographs and the front's fingers stop reading as fingers (adrift.js:345).
    var GRAIN_MIN = 5, GRAIN_MAX = 33, GRAIN_FINE = 3.4;
    // The threshold is walked past the density nothing in the work reaches, so the last grain leaves
    // and the mask is exactly empty. It is walked past by a whole shut rather than by a hair: a
    // coverage read as 0.5 + d/(g·fp) is linearised at the point, and where the density gradient is
    // steep a threshold a hundredth above the maximum still reads a fifth of a point of coverage
    // (adrift.js:788).
    var SHUT = 0.86, SHUT_PAST = 0.9;
    // The strongest waterline any work carrying this motif reaches, which is what the pair's lean is
    // measured against (adrift.js:728).
    var SEAM_FULL = 0.13;

    // THE RESPONSE CURVES, MEASURED AND CARRIED DIGIT FOR DIGIT (adrift.js:358-379). How far the
    // picture moves per unit of the raw parameter was measured with the curves taken out, that rate
    // integrated, and each table is the inverse of the integral at twenty-one evenly spaced shares
    // with straight lines between them. Flight, horizon and shrink carry no table, and that is an
    // assertion rather than an empty cell: the raw parameter is already even, measured at 1.1, 1.5
    // and 1.4 of raw band against the arsenal's ceiling of 2.5. The grain's table is fitted on the
    // geometric ladder, where equal movements of the hand are equal ratios of cell size.
    var FEEL_D0 = 0.05;
    var FEEL_MIX = [0, 0.0812, 0.1349, 0.181, 0.2261, 0.2721, 0.3227, 0.379, 0.4387, 0.4927, 0.544,
                    0.5984, 0.6482, 0.6913, 0.7325, 0.7726, 0.8142, 0.8559, 0.8978, 0.9424, 1];
    var FEEL_GRAIN = [0, 0.0285, 0.0586, 0.0905, 0.1228, 0.1554, 0.1892, 0.2233, 0.256, 0.2877,
                      0.3182, 0.348, 0.3787, 0.4113, 0.4471, 0.4866, 0.5352, 0.5966, 0.6721, 0.7903, 1];
    function table(q, d0, u) {
      var x = clamp(d0 > 0 ? (clamp(u, 0, 1) - d0) / (1 - 2 * d0) : clamp(u, 0, 1), 0, 1);
      var s = x * (q.length - 1), i = Math.min(q.length - 2, Math.floor(s));
      return q[i] + (q[i + 1] - q[i]) * (s - i);
    }
    function feelOf(u) { return table(FEEL_MIX, FEEL_D0, u); }

    // cover-fit a work into the frame, then pull in by the drag's own headroom. The host hands the
    // source's own dimensions, so the instrument never touches an image object.
    function fit(iw, ih, w, h) {
      var fa = w / Math.max(h, 1);
      var ia = iw / Math.max(ih, 1);
      var sx, sy;
      if (ia > fa) { sx = fa / ia; sy = 1; } else { sx = 1; sy = ia / fa; }
      return [sx / ZOOM, sy / ZOOM, 0, 0];
    }

    // The numbers of one frame (adrift.js:748-878). Everything the shader gets beyond the seating of
    // the two works and the two measured places is a pure function of the pose.
    //
    // ONE EASE AND NOT TWO: `smoothstep` is already flat at both ends, and easing it a second time
    // leaves the first sixth of a departure moving nothing at all. LEAVING AND ARRIVING ARE NOT
    // MIRROR IMAGES, and the readability law settled it: a thing leaving should cross the emptiness
    // as a thing and come apart at the end of its crossing, so its threshold lags the travel by the
    // square; a thing arriving should be there in traces from the moment it enters and firm up as it
    // comes, so its threshold runs ahead of its travel by the fourth power. Both read a straight ramp
    // of the hand rather than the eased travel, because an ease is flat where it starts and an
    // arrival read off it stood three quarters dissolved a fifth of the way in.
    //
    // The ground's grain is a parameter here rather than read straight off the pose, because the
    // hold in `values` below asks this same function for the same pose at a neighbouring cell
    // count. Nothing else about it moved.
    function posed(st, grainA) {
      var d = feelOf(clamp(st.mix, 0, 1));
      var flight = clamp(st.flight, 0, 1);
      var horizon = clamp(st.horizon, 0, 1);
      var shrink = clamp(st.shrink, 0, 1);
      var eA = smoothstep(0, DEPART, d), eB = smoothstep(ARRIVE, 1, d);
      // THE COUNTER-MOTION, IN ONE NUMBER because it is one thing in two registers: the two grounds
      // dragged past each other across the front, and the two things travelling in opposite senses.
      // The `travel` handle scales both together through this one place.
      var push = clamp(st.travel, 0, 1);
      var reach = FLIGHT_OF_VOID * Math.min(st.voidShareA, st.voidShareB) * flight * push;
      var departLin = clamp(d / DEPART, 0, 1), arriveLin = clamp((d - ARRIVE) / (1 - ARRIVE), 0, 1);
      var mA = departLin * departLin, mB = Math.pow(1 - arriveLin, 4);
      var thrA = st.thrA + (st.maxA - st.thrA) * Math.min(mA / SHUT, 1)
               + SHUT_PAST * smoothstep(SHUT - 0.02, 1, mA);
      var thrB = st.thrB + (st.maxB - st.thrB) * Math.min(mB / SHUT, 1)
               + SHUT_PAST * smoothstep(SHUT - 0.02, 1, mB);
      // THE GRAIN LADDER IS GEOMETRIC: a grain count is a scale, and what the eye reads is the size
      // of a cell. Stepped arithmetically the first tenth of the handle changes the cell size by a
      // third and the last tenth by a fortieth, and no curve fitted on a frame-distance measure buys
      // that back (adrift.js:823-831).
      var cell = 1 / grainA;
      // THE FINGERS: how far into each emptiness the other one reaches at the front, in cells of the
      // ground's own grain — a clean waterline at one end, a band four cells deep at the other.
      var fingers = (0.15 + 3.9 * horizon) * cell;
      // THE FRONT TRAVELS EVENLY and enters the frame exactly at FRONT_FROM. Eased in and out it
      // spent the first fifth of its range off the edge of the picture, and the response curve is
      // the place unevenness belongs.
      var front = clamp((d - FRONT_FROM) / (FRONT_TO - FRONT_FROM), 0, 1);
      var drift = (st.reduced ? 0 : st.t) * 0.09;
      // the shadow's gate and the drag's: both exactly zero at both doors
      var guard = smoothstep(0, 0.07, d) * smoothstep(1, 0.93, d);
      return {
        homeA: [st.homeAx, st.homeAy], homeB: [st.homeBx, st.homeBy],
        voidColA: [st.voidAr, st.voidAg, st.voidAb, 1], voidColB: [st.voidBr, st.voidBg, st.voidBb, 1],
        trav: [reach * eA, reach * (1 - eB)],
        poseA: [1 - SHRINK_MAX * shrink * eA, Math.cos(TURN_MAX * eA), Math.sin(TURN_MAX * eA), 0],
        poseB: [1 - SHRINK_MAX * shrink * (1 - eB), Math.cos(-TURN_MAX * (1 - eB)),
                Math.sin(-TURN_MAX * (1 - eB)), 0],
        thr: [thrA, thrB],
        thr0: [st.thrA, st.thrB],
        // HOW MUCH OF EACH THING IS STILL IN THE FRAME AT ALL, read off its own threshold against the
        // density its own work reaches: 1 at its door, 0 once the threshold has been walked past the
        // top. A shadow of a thing that is nowhere is a defect rather than a shadow.
        live: [clamp((st.maxA - thrA) / Math.max(st.maxA - st.thrA, 1e-6), 0, 1),
               clamp((st.maxB - thrB) / Math.max(st.maxB - st.thrB, 1e-6), 0, 1)],
        grain: [grainA, grainA * GRAIN_FINE],
        drift: [drift, drift * 0.6],
        field: [cell, fingers, front, clamp(0.5 * (st.seamA + st.seamB) / SEAM_FULL, 0, 1)],
        drag: push * DRAG * guard,
        guard: clamp(st.shade, 0, 1) * guard,
        // read on the diagnostic surface, bound to no uniform: what the hand came to
        dial: d, eA: eA, eB: eB, reach: reach,
      };
    }

    // ---- THE DOOR THE INSTRUMENT READS FOR ITSELF ------------------------------------------------
    // His 18:00 architecture decision, carried in the U27 brief: the instrument reads its doors at
    // runtime on the actual buffer, and the report it hands back is the runtime truth; what the
    // manifest declares is only the claim. The meshing instrument answered that first
    // (pass-inst-gears.js, THE DOOR THE INSTRUMENT READS FOR ITSELF); this is the same law read in
    // this instrument's own units, which are the CELLS of the ground's grain and the SILHOUETTE each
    // work's own content is cut at.
    //
    // WHAT A DOOR ASKS OF THIS INSTRUMENT, and which half of it the buffer decides.
    //   · THE SILHOUETTE PAIR is exact at either door by construction, and the reading publishes it
    //     rather than fearing it. At the entry door the departing thing has not moved (`trav` 0,
    //     scale 1, turn 0) and its threshold stands at the very number its measured place was solved
    //     at (`thr` equals `thr0`), so `covA` and the home reading of it are the SAME expression at
    //     the SAME arguments and `holeA` is exactly 0 on any grid. The exit door says the same of
    //     the arriving thing. So what is published is the pose the silhouette settled on.
    //   · THE HANDOVER FRONT is what the buffer decides. `covV` must be exactly 1 at the entry door
    //     and exactly 0 at the exit, because the alpha the frame hands over is
    //     `1 − mix(holeB, holeA, covV)`: at the entry door `holeB` is the arriving work's whole
    //     silhouette (its threshold has been walked past the top, so `covB` is nothing while the
    //     home reading is not), and the moment `covV` falls short of 1 that silhouette is punched
    //     straight through the door as transparency. `covV` is
    //         clamp(0.5 + (F − tau) / (grad · h)),   h = 1 / uRes.y
    //     so the front crosses over inside a band HALF THE FIELD'S OWN SLOPE PER BUFFER POINT wide,
    //     and the door is whole exactly while that band clears the front's own margin.
    //
    // THE MARGIN IS THE SHADER'S OWN 0.03, and it is exact rather than estimated. `margin` in FRAG
    // is `0.03 + 0.5·(grainW + fine)` and `tau` is `−margin` at the entry door, while `F` is the
    // ladder (0 at its least) displaced by at most `0.5·grainW` and `0.5·fine`. The two halves
    // cancel term for term, so `F − tau` is at least 0.03 at either door whatever the grain and the
    // fingers do — which is why 0.03 and not a number of this reading's own invention.
    var FRONT_MARGIN = 0.03;
    // Six parts the plain ladder against four parts the grain — FRAG's own `LADDER` const, carried
    // here so the front's own widths can be recomputed in script.
    var LADDER_JS = 0.6;
    // The value noise's own steepest slope, per cell. Its partials are `((b−a) + k·u.y) · 6f(1−f)`
    // and its mirror; the bracket is linear in u and lands on b−a at one end and d−c at the other,
    // so it never leaves [−1, 1], and 6f(1−f) tops out at 1.5.
    var NOISE_SLOPE = 1.5 * Math.SQRT2;
    var DOOR_HOLD = 2;   // how far the hold reaches, in whole cells of the ground's grain

    // The grid the door is read on, and which of the two it is. `drawn` says which one the sentence
    // below names, since a reader told «a 390 x 160 frame» would look for a device that has none.
    function doorGridOf(st) {
      var bw = Math.round(st.bufWidth), bh = Math.round(st.bufHeight);
      if (bw >= 1 && bh >= 1) return { w: bw, h: bh, drawn: true };
      return { w: Math.round(st.cssWidth), h: Math.round(st.cssHeight), drawn: false };
    }

    // THE FRONT'S OWN CROSSOVER, READ ON THE BUFFER. Every width here has its counterpart in FRAG:
    // `grainW`, `fine`, `band` and the two gradient terms, all of them divided by `sp` — how far the
    // front's projection runs over the frame.
    //
    // WHY `sp` IS TAKEN AT ITS SMALLEST. `sp` is `aspect·|axis.x| + |axis.y|`, and the axis is built
    // from the two works' own measured places seated through the fit the host applied — which the
    // host hands this instrument nothing of (`frameState` carries the viewport and no seating). The
    // span is smallest at a pure axis, `min(aspect, 1)`, and every width above rises as the span
    // falls, so reading at that smallest span is the worst case over every axis the seating can
    // produce. It can only ever OVER-hold, and the hold costs the picture nothing at a door.
    //
    // WHY THE SWEEP. The fine grain only enters the field near the front (`near`), and `near` and
    // the distance from the threshold are two readings of one number: fix the distance and both the
    // slope and the least `F − tau` follow. So the reading walks the distance outward from the
    // closest a door allows — `0.03 + fine/2`, which is exactly where the ladder stands at its own
    // end — and keeps the place where the crossover stands worst against the margin left there.
    function frontReadOf(v, aspect, H) {
      var cell = v.field[0], fingers = v.field[1];
      var grainA = v.grain[0], grainB = v.grain[1];
      var sp = Math.max(Math.min(aspect, 1), 1e-4);
      var grainW = 2 * ((1 - LADDER_JS) / LADDER_JS) * cell / sp;
      var fine = 2 * fingers / sp;
      var band = (1.2 * fingers + 0.03) / sp;
      var g0 = 1 / sp + grainW * grainA * NOISE_SLOPE;
      var h = 1 / H;
      var ecMin = FRONT_MARGIN + 0.5 * fine;
      var worst = { ratio: 0, slope: g0, cross: 0.5 * g0 * h, margin: ecMin };
      for (var i = 0; i <= 32; i++) {
        var ec = ecMin + (5 * band) * (i / 32);
        var near = Math.exp(-(ec * ec) / Math.max(band * band, 1e-12));
        var m = ec - 0.5 * fine * near;
        var g = g0 * (1 + fine * near * 2 * ec / Math.max(band * band, 1e-12))
              + fine * near * NOISE_SLOPE * grainB;
        var cross = 0.5 * g * h;
        var ratio = cross / Math.max(m, 1e-9);
        if (ratio > worst.ratio) { worst = { ratio: ratio, slope: g, cross: cross, margin: m }; }
      }
      worst.cells = grainA;
      worst.fingers = fingers * grainA;   // the fingers' depth in cells of the ground's own grain
      worst.cellPx = H / Math.max(grainA, 1e-6);
      return worst;
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
      var front = frontReadOf(v, W / Math.max(H, 1), H);
      return { grid: g, want: want, front: front,
               // THE SILHOUETTE'S OWN APPLIED STATE at this door: how far the thing that owns the
               // door has travelled, the scale and the turn it stands at, and the distance between
               // the threshold it is cut at now and the one its measured place was solved at. All
               // four are exactly the door's own numbers, and this is the reading that says so.
               silhouette: { travelled: want ? v.trav[0] : v.trav[1],
                             scale: want ? v.poseA[0] : v.poseB[0],
                             turn: want ? v.poseA[2] : v.poseB[2],
                             offThreshold: Math.abs((want ? v.thr[0] : v.thr[1])
                                                  - (want ? v.thr0[0] : v.thr0[1])),
                             drag: v.drag } };
    }

    // THE REFUSAL, worded the way the host's own manifest refusals read: what is wrong, in this
    // instrument's own measured numbers, on the grid it was measured on.
    function doorWhyNoOf(read) {
      if (!read || read.front.ratio <= 1) return null;
      var g = read.grid, f = read.front;
      return (read.want ? "the entry" : "the exit") + " door leaks: at a ground grain of "
           + f.cells.toFixed(2) + " cells across the frame's height — " + f.cellPx.toFixed(2)
           + " points of a " + g.w + " x " + g.h + (g.drawn ? " buffer" : " frame")
           + " to a cell — with fingers " + f.fingers.toFixed(2)
           + " cells deep, the field's own steepest slope is " + f.slope.toFixed(2)
           + ", so the handover front crosses over inside " + f.cross.toFixed(4)
           + " of the field against the " + f.margin.toFixed(4)
           + " its own margin leaves at a door, and the " + (read.want ? "arriving" : "departing")
           + " work's own silhouette is punched through this door as transparency, where "
           + (read.want ? "the entry" : "the exit") + " door's own law asks for one whole work, "
           + "opaque at every point";
    }

    // THE NUMBERS OF ONE FRAME, WITH ITS DOOR HELD WHOLE ON THE BUFFER BEING DRAWN. Away from a door
    // this is `posed` and nothing more: the reading is taken nowhere else and no grain moves. At a
    // door whose front crosses over inside the frame on the buffer being drawn, the instrument steps
    // to a COARSER whole cell count — the only direction that closes it, since every width of the
    // front is a multiple of the cell and the margin it stands against is not — and answers with the
    // first pose whose door is whole. What the score asked for and what was applied are both on the
    // record: `grain` carries the grain drawn, `grainRequest` the one handed in, `grainCells` how
    // many whole cells apart they stand, and `doorHeld` the leak the request would have drawn.
    //
    // HOW FAR «NEAR» REACHES, and why it is two cells. The ground's own unit is the cell, so that is
    // the unit the distance is counted in. Two cells of a grain that runs from five to thirty-three
    // is a step of the ground nobody watching a door can see, because at a door the frame is one
    // whole work and no cell of the ground is on screen; beyond two cells the pose the score asked
    // for is genuinely a different ground and the refusal is the honest answer. A guard that never
    // refuses proves nothing.
    function values(st) {
      var grainA = GRAIN_MIN * Math.pow(GRAIN_MAX / GRAIN_MIN, table(FEEL_GRAIN, 0, st.grain));
      var v = posed(st, grainA);
      v.grainRequest = grainA;
      v.grainCells = 0;
      v.doorHeld = null;
      var read = doorReadOf(v, st);
      var no = doorWhyNoOf(read);
      v.doorGrid = read ? read.grid : null;
      v.doorSilhouette = read ? read.silhouette : null;
      v.doorCross = read ? read.front.cross : null;
      v.cellPx = read ? read.front.cellPx : null;
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
        w.doorSilhouette = wRead.silhouette;
        w.doorCross = wRead.front.cross;
        w.cellPx = wRead.front.cellPx;
        return w;
      }
      v.doorWhyNo = no + ", and no whole cell stands within " + DOOR_HOLD
                  + " cells of the grain handed in";
      return v;
    }

    var manifest = {
      id: "adrift", api: 1, arity: 2,
      // The departing thing comes apart, the middle holds an emptiness belonging to neither work,
      // and the arriving thing gathers and settles.
      roles: ["disassembly", "mystery", "assembly"],
      // READ OFF THE MODULE'S OWN CONSTRUCTION, and said to be derived. The vocabulary table carries
      // no `adrift` row and `module-contract.json` no `adrift` entry, so no level is published for it
      // anywhere and these two are read here:
      //   · CELL CONTENT — the two things themselves. Each is cut from its work by the density
      //     threshold its own measured share solves for, carried with its own picture, travelled,
      //     turned, shrunk and dissolved as one object. That is the content of a named region moving
      //     as a whole, which is the level `providers.json` places `region` at, and no landed
      //     instrument occupies it.
      //   · SURFACE — the field of emptiness. One field runs over the whole frame and its value at a
      //     point decides whose ground that point is.
      // TEXTURE is not claimed. The grain here shapes the front's own boundary and its fingers; the
      // picture's own material is the works' film grain, which this instrument does not touch.
      levels: ["SURFACE", "CELL CONTENT"],
      params: { flight: [0, 1], horizon: [0, 1], grain: [0, 1], shrink: [0, 1] },
      // EVERY handle a score can drive (§4.4b). `mix` is the dial and `clock` is the second the host
      // hands down; the four below them are the module's declared params; `seed` is its die; `shade`,
      // `travel` and `mask` are the judges' channels, resting where the module rests them.
      //
      // NO HANDLE HERE KEEPS A CLOCK OF ITS OWN. The one place the module reads time is the drift of
      // the grain, `t * 0.09` (adrift.js:854), where `t` was its own accumulated frame time. It reads
      // the `clock` handle instead, so a seeded score repeats to the pixel.
      //
      // THE FOURTEEN THAT CARRY THE PAIR'S OWN MEASUREMENTS. The module reads four numbers per work
      // out of `lab/data/motifs.json` and solves three more off the file itself at build. This file
      // may not read a file, so every one of them arrives as a handle a score row drives — which is
      // also what «plays on the elements a plan hands it» means in practice:
      //   · `homeAx`/`homeAy` — the centre of `figure_bbox`, as a share of the FILE. The shader seats
      //     it through the fit the host applied.
      //   · `voidA` — the work's own ground colour, the mean outside its measured box, in three
      //     channels.
      //   · `thrA` — the density its silhouette is cut at: the threshold at which the mask's area is
      //     exactly the measured `figure_share`. It is solved rather than chosen.
      //   · `maxA` — the density nothing in the work reaches, so a threshold walked up to there
      //     empties the silhouette exactly and no fade is needed to make a thing go.
      //   · `voidShareA` — `void_share`, how much of the frame is empty ground, which is how far a
      //     thing may travel before it stands on architecture instead of on emptiness.
      //   · `seamA` — `seam_horizon`, how strongly the work carries a waterline of its own, which is
      //     how far the handover front leans off the object line.
      // THEIR DEFAULTS ARE THE MODULE'S OWN NAIVE READING (adrift.js:608) — the centre of the frame
      // and a fixed share, which is the reading the motif exists to replace and which the module
      // records as `blind`. The ground colour, the threshold and the maximum have no naive value in
      // the module because it reads them off the file; they rest at neutral numbers here, and a pair
      // whose row carries no measurement gets a picture standing on those.
      handles: {
        mix: { min: 0, max: 1, def: 0 },
        clock: { min: 0, max: 14, def: 0 },
        flight: { min: 0, max: 1, def: 0.55 },
        horizon: { min: 0, max: 1, def: 0.55 },
        // THE MEASUREMENT THIS HANDLE IS READ AGAINST AT A DOOR, published beside its range the way
        // the meshing instrument publishes its own. `heldWholeAtADoor` says what is read (the
        // handover front's own crossover, held against the margin the front leaves at a door), on
        // which grid (the drawing buffer the host binds, with the CSS frame where it hands none),
        // how far the hold reaches (two whole cells of the ground's grain) and where the request the
        // score handed in stays on the record.
        grain: { min: 0, max: 1, def: 0.66,
                 applied: { heldWholeAtADoor: { cells: DOOR_HOLD, readOn: "the drawing buffer",
                                                reads: "grainRequest",
                                                measures: "the handover front's own crossover "
                                                        + "against the margin it leaves at a "
                                                        + "door" } } },
        shrink: { min: 0, max: 1, def: 0.5 },
        seed: { min: 0, max: 8, def: 0 },
        shade: { min: 0, max: 1, def: 1 },
        travel: { min: 0, max: 1, def: 1 },
        mask: { min: 0, max: 1, def: 0 },
        homeAx: { min: 0, max: 1, def: 0.5 },
        homeAy: { min: 0, max: 1, def: 0.5 },
        homeBx: { min: 0, max: 1, def: 0.5 },
        homeBy: { min: 0, max: 1, def: 0.5 },
        voidAr: { min: 0, max: 1, def: 0.5 },
        voidAg: { min: 0, max: 1, def: 0.5 },
        voidAb: { min: 0, max: 1, def: 0.5 },
        voidBr: { min: 0, max: 1, def: 0.5 },
        voidBg: { min: 0, max: 1, def: 0.5 },
        voidBb: { min: 0, max: 1, def: 0.5 },
        thrA: { min: 0, max: 1.7321, def: 0.35 },
        thrB: { min: 0, max: 1.7321, def: 0.35 },
        maxA: { min: 0, max: 1.7321, def: 0.9 },
        maxB: { min: 0, max: 1.7321, def: 0.9 },
        voidShareA: { min: 0, max: 1, def: 0.75 },
        voidShareB: { min: 0, max: 1, def: 0.75 },
        seamA: { min: 0, max: 1, def: 0.05 },
        seamB: { min: 0, max: 1, def: 0.05 },
      },
      neutrals: { a: 0, b: 1 },
      doors: { in: { handle: "mix", value: 0, work: "a" },
               out: { handle: "mix", value: 1, work: "b" } },
      // Both doors frame alike: the crop the drag's headroom is paid for with is a constant, and the
      // drag itself is zero at both ends.
      framings: { "0": { coverCrop: ZOOM }, "1": { coverCrop: ZOOM } },
      drivers: ["progress", "cueProgress", "time", "velocity", "capability", "noise", "static",
                "curve", "spline", "map", "add", "multiply", "mix", "clamp", "hold", "segment",
                "ramp", "slew", "oscillate", "node"],
      camera: { needs: "none", authority: "stage" },
      gl: { preserveDrawingBuffer: false },
      // WHAT THIS INSTRUMENT WRITES WHERE ITS OWN MATTER IS ABSENT (§7's coverage law, and the
      // per-instrument specification in docs/design/COVERAGE.md). Its absence is the place a thing
      // has left: the work's own content stood there at the door, it stands there no longer, and
      // this instrument carries no picture of its own for it. The quantity is the shader's own
      // silhouette coverage read twice — once where the thing stands now and once where the
      // measurement put it — and the alpha is 1 minus the difference. At both doors the two readings
      // are the same expression at the same arguments, so the difference is exactly zero and each
      // door is one whole work, opaque at every point.
      coverage: {
        writes: true,
        how: "1.0 - clamp(covHome - cov), the measured place each work's own content has left, "
             + "taken on the side of the handover front that owns the point",
      },
      // The neutral pose is the ENTRY DOOR — `mix` at 0, the value the `doors` block above names —
      // so the frame keys the host reads off it at registration include the door's own record.
      neutralPose: { mix: 0, flight: 0.55, horizon: 0.55, grain: 0.66, shrink: 0.5, seed: 0,
                     cssWidth: 1000, cssHeight: 1000,
                     shade: 1, travel: 1, mask: 0,
                     homeAx: 0.5, homeAy: 0.5, homeBx: 0.5, homeBy: 0.5,
                     voidAr: 0.5, voidAg: 0.5, voidAb: 0.5, voidBr: 0.5, voidBg: 0.5, voidBb: 0.5,
                     thrA: 0.35, thrB: 0.35, maxA: 0.9, maxB: 0.9, voidShareA: 0.75, voidShareB: 0.75,
                     seamA: 0.05, seamB: 0.05, t: 0, reduced: false },
      passes: [{
        program: "adrift", vert: VERT, frag: FRAG, position: "aPos",
        uniforms: [
          { name: "uA", type: "sampler2D", source: "textureA" },
          { name: "uB", type: "sampler2D", source: "textureB" },
          { name: "uFitA", type: "vec4", source: "fitA" },
          { name: "uFitB", type: "vec4", source: "fitB" },
          { name: "uRes", type: "vec2", source: "resolution" },
          { name: "uVoidA", type: "vec4", source: "frame:voidColA" },
          { name: "uVoidB", type: "vec4", source: "frame:voidColB" },
          { name: "uHomeA", type: "vec2", source: "frame:homeA" },
          { name: "uHomeB", type: "vec2", source: "frame:homeB" },
          { name: "uTrav", type: "vec2", source: "frame:trav" },
          { name: "uPoseA", type: "vec4", source: "frame:poseA" },
          { name: "uPoseB", type: "vec4", source: "frame:poseB" },
          { name: "uThr", type: "vec2", source: "frame:thr" },
          { name: "uThr0", type: "vec2", source: "frame:thr0" },
          { name: "uLive", type: "vec2", source: "frame:live" },
          { name: "uGrain", type: "vec2", source: "frame:grain" },
          { name: "uDrift", type: "vec2", source: "frame:drift" },
          { name: "uField", type: "vec4", source: "frame:field" },
          { name: "uDrag", type: "float", source: "frame:drag" },
          { name: "uGuard", type: "float", source: "frame:guard" },
          { name: "uSeed", type: "float", source: "handle:seed" },
          { name: "uMask", type: "float", source: "handle:mask" },
        ],
      }],
      // The instrument allocates nothing of its own: it spends the two source-texture slots the host
      // already holds and the one programme the host builds from this manifest. The lab module's two
      // ground plates are the two textures this port does not ask for.
      resources: { lean: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                           passes: 1, bytesEstimate: 0, variant: "lean" },
                   standard: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                               passes: 1, bytesEstimate: 0, variant: "standard" },
                   rich: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                           passes: 1, bytesEstimate: 0, variant: "rich" } },
      capabilities: ["webgl2"],
      decline: ["one work only", "a source that never decoded"],
      // The lab module stands untracked in the tlvphotos worktree on the day of this port, so there
      // is no commit to name and none is invented. The digest of the file the port was read from
      // stands in its place, and a row re-weighs the file against it.
      provenance: { labPath: "lab/effects/adrift.js", commit: null,
                    sha256: "3d72fbdfee393ccf20813c2655d8b14316c35bdb5bd3d20ee89da85aec35020e" },
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
      suits: { reads: ["measures.named_objects"],
               how: "it cuts on the things IN the picture, so it suits a pair both of whose works "
                  + "carry named objects; the weaker of the two readings is the fit, and it is "
                  + "nothing where one work names nothing" },
      readiness: "production-ready",
    };

    var live = false;
    return {
      name: "adrift",
      manifest: manifest,
      values: values,
      fit: fit,
      feel: feelOf,
      prepare: function (o) {
        if (!o.sources) return { take: false, why: "the adrift instrument needs both works" };
        if (!o.cue) return { take: false, why: "no cue names it" };
        return { take: true };
      },
      start: function () { live = true; },
      // The pose the shader draws. Every number in it comes from a handle a score can drive, and the
      // grain's drift reads the second the host hands down, so a seeded run repeats to the pixel.
      // The redraw the preserved buffer stood in for is the host's own frame loop: this draws on
      // every frame it is handed, and reduced motion stops the grain's drift alone.
      //
      // A DOOR THIS INSTRUMENT CANNOT KEEP WHOLE IS REFUSED RATHER THAN DRAWN. The door law is the
      // instrument's own claim (the manifest's coverage line above), so the instrument is what
      // answers for it: at either door it reads its own handover front on the buffer the host is
      // about to bind and, where the front crosses over inside the frame there and no whole cell
      // within reach closes it, hands the host the reason with the measured crossing in it instead
      // of punching the other work's silhouette through the door as transparency. The host recovers
      // the transaction on that reason and the walk's own glide carries the visitor, which is the
      // product's own behaviour with no renderer.
      frame: function (st) {
        if (!live) return;
        var h = st.handles;
        var pose = {
          mix: h.mix, flight: h.flight, horizon: h.horizon, grain: h.grain, shrink: h.shrink,
          seed: h.seed, shade: h.shade, travel: h.travel, mask: h.mask,
          homeAx: h.homeAx, homeAy: h.homeAy, homeBx: h.homeBx, homeBy: h.homeBy,
          voidAr: h.voidAr, voidAg: h.voidAg, voidAb: h.voidAb,
          voidBr: h.voidBr, voidBg: h.voidBg, voidBb: h.voidBb,
          thrA: h.thrA, thrB: h.thrB, maxA: h.maxA, maxB: h.maxB,
          voidShareA: h.voidShareA, voidShareB: h.voidShareB, seamA: h.seamA, seamB: h.seamB,
          t: h.clock, reduced: st.reduced,
          cssWidth: st.viewport.w, cssHeight: st.viewport.h,
          // THE GRID THE SHADER WILL SAMPLE ON, carried into the pose so the door is read on the
          // buffer the host is about to bind as `uRes` rather than on the CSS frame around it. The
          // host settles it from the device ratio and its own resolution step, so it moves while a
          // pass plays and each door is read on the grid standing at that door's own instant.
          bufWidth: st.viewport.bufferW, bufHeight: st.viewport.bufferH,
        };
        // AT A DOOR THE INSTRUMENT SAYS WHAT IT APPLIED, and says it before it refuses. The reading
        // is taken on the buffer this frame is drawn on, so it is the run-time truth his 18:00
        // decision asks for rather than the grain the score asked for. `applied` is the request less
        // the whole cells the hold walked back, which is the grain the frame was actually posed on.
        if (h.mix === 0 || h.mix === 1) {
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
    instrument: adriftInstrument(),
  });
})();
