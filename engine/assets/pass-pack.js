/*!pass-pack.js*/
// The effect pack — the instruments themselves, shipped as one file the host loads by address,
// version and digest (PASS-API-V1 §7/§8, his word of 2026-08-14 08:39: the engine knows no effect
// name and loads a version-pinned opaque pack).
//
// WHAT THIS FILE IS. A list of instruments and the mathematics each one draws by. Every instrument
// here is a plain record: a name, a manifest declaring its passes, its uniforms with the source
// each is bound from, its handles and its doors, and the pure functions that answer the numbers of
// one frame. The manifest's declared names are the whole interface — the host binds by them and
// refuses at registration anything it cannot supply.
//
// WHAT THIS FILE MAY NOT DO. It reads no wall clock, holds no listener, creates no WebGL context,
// loads no picture and touches no DOM (§1.2's fence). The host owns the canvas, the context, the
// frame loop, the clock, the camera and the transaction; the pack owns the picture.
//
// HOW IT REACHES THE HOST. The host fetches this file, weighs its bytes against the digest the
// build stamped, evaluates the bytes it weighed, and reads the record handed to the join function
// below. A version or a digest that fails to match is refused with its reason and the walk's own
// glide runs instead, which is what a visit with no pack has always looked like.
//
// OWNERSHIP. The three instruments standing here today were carried over from lab/effects/. The
// artistic pack and its manifests belong to tlvphotos, which builds this file from its own
// instrument sources; the engine's copy is the pack that ships until that handover lands. See the
// handover note in docs/design/ for the file's shape and its build inputs.
(function () {
  var join = window.__@@NS@@PassPack;
  if (typeof join !== "function") return;

  // THE PACK'S OWN VERSION, and the one home of that fact. The build reads this literal out of the
  // source and stamps it into the host beside the digest, so the number a pack declares and the
  // number a host was told to load cannot drift apart without the build noticing.
  var PACK_VERSION = "1.0.0";

  var TAU = Math.PI * 2;

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
    function values(st) {
      var d = feelOf(clamp(st.mix, 0, 1));
      var flight = clamp(st.flight, 0, 1);
      var horizon = clamp(st.horizon, 0, 1);
      var grain = table(FEEL_GRAIN, 0, st.grain);
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
      var grainA = GRAIN_MIN * Math.pow(GRAIN_MAX / GRAIN_MIN, grain);
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
        grain: { min: 0, max: 1, def: 0.66 },
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
      neutralPose: { mix: 0, flight: 0.55, horizon: 0.55, grain: 0.66, shrink: 0.5, seed: 0,
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
      frame: function (st) {
        if (!live) return;
        var h = st.handles;
        st.draw({
          mix: h.mix, flight: h.flight, horizon: h.horizon, grain: h.grain, shrink: h.shrink,
          seed: h.seed, shade: h.shade, travel: h.travel, mask: h.mask,
          homeAx: h.homeAx, homeAy: h.homeAy, homeBx: h.homeBx, homeBy: h.homeBy,
          voidAr: h.voidAr, voidAg: h.voidAg, voidAb: h.voidAb,
          voidBr: h.voidBr, voidBg: h.voidBg, voidBb: h.voidBb,
          thrA: h.thrA, thrB: h.thrB, maxA: h.maxA, maxB: h.maxB,
          voidShareA: h.voidShareA, voidShareB: h.voidShareB, seamA: h.seamA, seamB: h.seamB,
          t: h.clock, reduced: st.reduced,
        });
        if (st.progress >= 1 && !st.pinned) st.settle(st.token);
      },
      resize: function () {},
      cancel: function () {},
      dispose: function () { live = false; },
      contextLost: function () { live = false; },
      contextRestored: function () {},
    };
  }

  // ================================================================================================
  // THE WOVEN INSTRUMENT (§8) — lab/effects/weave.js carried across
  // ================================================================================================
  // What came over: the shader, the seating of a work in the frame (coverFit), the response curve
  // (feelOf), the turn of the weave (rotForTime) and the numbers of one frame (frameValuesOf). Not
  // one number changed; this is the same mathematics, standing on the host's frame.
  //
  // What stayed behind: its own canvas, its own WebGL 1 context, its own frame loop, its pointer and
  // resize listeners, its 2D fallback and its own clock. The instrument here reads no wall clock,
  // holds no listener, creates no context and loads no picture (§1.2's fence).
  function weaveInstrument() {
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
      "uniform float uT;",
      "uniform float uNv;",
      "uniform float uDuty;",
      "uniform float uAmp;",
      "uniform float uRot;",
      "uniform float uSpeed;",
      "uniform float uSeed;",
      "const float TAU = 6.28318530718;",
      "vec2 into(vec2 p, vec4 f){",
      "  return clamp((p - 0.5) * f.xy + 0.5 + f.zw, 0.0008, 0.9992);",
      "}",
      "vec3 texA(vec2 p){ return texture2D(uA, into(p, uFitA)).rgb; }",
      "vec3 texB(vec2 p){ return texture2D(uB, into(p, uFitB)).rgb; }",
      "float sqI(float t, float d){ return floor(t) * d + min(fract(t), d); }",
      "float sqcov(float x, float d, float w){",
      "  w = max(w, 1e-5);",
      "  if (d >= 1.0) return 1.0;",
      "  if (d <= 0.0) return 0.0;",
      "  return clamp((sqI(x + w, d) - sqI(x - w, d)) / (2.0 * w), 0.0, 1.0);",
      "}",
      "float hash21(vec2 p){ return fract(sin(dot(p, vec2(41.317, 289.107))) * 43758.5453); }",
      "float warpV(float x, float k, float ph){ return x + 0.42 * sin(k * TAU * x + ph) / (k * TAU); }",
      "float warpD(float x, float k, float ph){ return 1.0 + 0.42 * cos(k * TAU * x + ph); }",
      "void main(){",
      "  vec2 uv = vUv;",
      "  float aspect = uRes.x / max(uRes.y, 1.0);",
      "  float av = clamp(2.0 - 2.0 * uRot, 0.0, 1.0);",
      "  float ah = clamp(2.0 * uRot, 0.0, 1.0);",
      "  float basket = min(av, ah);",
      "  float nV = max(5.0, uNv * (1.0 - 0.25 * basket));",
      "  float nH = max(3.0, nV / max(aspect, 0.05));",
      "  float phV = uT * 0.31;",
      "  float phH = uT * 0.24 + 1.7;",
      "  float alive = smoothstep(0.0, 0.10, uDuty) * smoothstep(1.0, 0.90, uDuty);",
      "  float aV1 = TAU * (uv.y * 1.7 - uT * 0.090);",
      "  float aV2 = TAU * (uv.y * 3.1 + uT * 0.062 + 1.3);",
      "  float edgeV = alive * (0.34 * sin(aV1) + 0.17 * sin(aV2));",
      "  float dEdgeV = alive * TAU * (0.34 * 1.7 * cos(aV1) + 0.17 * 3.1 * cos(aV2));",
      "  float aH1 = TAU * (uv.x * 1.6 + uT * 0.081);",
      "  float aH2 = TAU * (uv.x * 2.9 - uT * 0.055 + 0.7);",
      "  float edgeH = alive * (0.34 * sin(aH1) + 0.17 * sin(aH2));",
      "  float dEdgeH = alive * TAU * (0.34 * 1.6 * cos(aH1) + 0.17 * 2.9 * cos(aH2));",
      "  float cV = warpV(uv.x, 2.0, phV) * nV + edgeV;",
      "  float cH = warpV(uv.y, 3.0, phH) * nH + edgeH;",
      "  float iv = floor(cV), fv = fract(cV);",
      "  float ih = floor(cH), fh = fract(cH);",
      "  float wV = 0.5 * (nV * warpD(uv.x, 2.0, phV) / uRes.x + abs(dEdgeV) / uRes.y);",
      "  float wH = 0.5 * (nH * warpD(uv.y, 3.0, phH) / uRes.y + abs(dEdgeH) / uRes.x);",
      "  float ph = uT * uSpeed * 0.17;",
      "  float offV = uAmp * sin(TAU * (ph + (iv + 0.5) / nV * 1.5 + 0.35 * hash21(vec2(iv, uSeed))));",
      "  float offH = uAmp * sin(TAU * (ph * 0.86 + (ih + 0.5) / nH * 1.5 + 0.31 + 0.35 * hash21(vec2(uSeed, ih))));",
      "  float push = 2.0 * basket * uDuty * (1.0 - uDuty);",
      "  float dutyV = clamp(uDuty + push, 0.0, 1.0);",
      "  float dutyH = clamp(uDuty - push, 0.0, 1.0);",
      "  float guardV = smoothstep(0.0, 0.12, dutyV) * smoothstep(1.0, 0.88, dutyV);",
      "  float guardH = smoothstep(0.0, 0.12, dutyH) * smoothstep(1.0, 0.88, dutyH);",
      "  float covV = sqcov(cV, dutyV, wV);",
      "  vec3 colV = mix(texB(uv + vec2(0.0, -offV)), texA(uv + vec2(0.0, offV)), covV);",
      "  float swV = max(4.0 * wV, min(0.12, 0.35 * min(dutyV, 1.0 - dutyV)));",
      "  float parV = step(0.5, mod(iv, 2.0));",
      "  float onBv = exp(-max(fv - dutyV, 0.0) / swV) * (1.0 - covV);",
      "  float onAv = exp(-max(dutyV - fv, 0.0) / swV) * covV;",
      "  colV *= 1.0 - 0.34 * guardV * mix(onBv, onAv, parV);",
      "  float covH = sqcov(cH, dutyH, wH);",
      "  vec3 colH = mix(texB(uv + vec2(-offH, 0.0)), texA(uv + vec2(offH, 0.0)), covH);",
      "  float swH = max(4.0 * wH, min(0.12, 0.35 * min(dutyH, 1.0 - dutyH)));",
      "  float parH = step(0.5, mod(ih, 2.0));",
      "  float onBh = exp(-max(fh - dutyH, 0.0) / swH) * (1.0 - covH);",
      "  float onAh = exp(-max(dutyH - fh, 0.0) / swH) * covH;",
      "  colH *= 1.0 - 0.34 * guardH * mix(onBh, onAh, parH);",
      "  float bv = floor(iv * 0.5), bh = floor(ih * 0.5);",
      "  float pV = av / max(av + ah, 1e-4);",
      "  float parity = step(mod(bv + bh, 2.0), 0.5);",
      "  float chooseB = clamp(parity + (2.0 * uDuty - 1.0), 0.0, 1.0);",
      "  float choose = mix(pV, chooseB, basket);",
      "  float ord = mix(0.5 * ((bv * 2.0 + 1.0) / nV + (bh * 2.0 + 1.0) / nH),",
      "                  hash21(vec2(bv, bh) + uSeed), 0.4);",
      "  float showV = step(ord * 0.996 + 0.002, choose);",
      "  vec3 col = mix(colH, colV, showV);",
      "  float fbv = fract(cV * 0.5), fbh = fract(cH * 0.5);",
      "  float grooveV = 1.0 - smoothstep(0.0, 0.05, min(fv, 1.0 - fv));",
      "  float grooveH = 1.0 - smoothstep(0.0, 0.05, min(fh, 1.0 - fh));",
      "  float diveV = 1.0 - smoothstep(0.0, 0.16, min(fbh, 1.0 - fbh));",
      "  float diveH = 1.0 - smoothstep(0.0, 0.16, min(fbv, 1.0 - fbv));",
      "  float shade = mix(0.55 * diveH + 0.30 * grooveH, 0.55 * diveV + 0.30 * grooveV, showV);",
      "  float shadeGate = smoothstep(0.0, 0.22, uDuty) * smoothstep(1.0, 0.78, uDuty);",
      "  col *= 1.0 - basket * shadeGate * min(shade, 0.62);",
      "  gl_FragColor = vec4(col, 1.0);",
      "}",
    ].join("\n");

    function smoothstep(a, b, x) {
      var t = (x - a) / (b - a);
      t = t < 0 ? 0 : t > 1 ? 1 : t;
      return t * t * (3 - 2 * t);
    }
    function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }

    // How far a ribbon may slide along its own axis, as a fraction of the frame. Every sample the
    // shader takes is the frame coordinate pushed by at most TRAVEL, so the cover-fit is pulled in by
    // TRAVEL at each end: ZOOM is derived from TRAVEL and is not a free number.
    var AMP = 0.10, PRESS = 1.30, TRAVEL = AMP * PRESS, ZOOM = 1 + 2 * TRAVEL + 0.03;

    // cover-fit a work into the frame, then pull in by the travel headroom. The host hands the
    // source's own dimensions, so the instrument never touches an image object.
    function fit(iw, ih, w, h) {
      var fa = w / Math.max(h, 1);
      var ia = iw / Math.max(ih, 1);
      var sx, sy;
      if (ia > fa) { sx = fa / ia; sy = 1; } else { sx = 1; sy = ia / fa; }
      return [sx / ZOOM, sy / ZOOM, 0, 0];
    }

    var AXES = ["up and down", "side to side", "both"];
    function axisNameOf(axis) {
      if (typeof axis === "number") return AXES[clamp(Math.round(axis), 0, 2)];
      return AXES.indexOf(axis) >= 0 ? axis : "both";
    }
    function rotForTime(time, axis) {
      var a = axisNameOf(axis);
      if (a === "up and down") return 0;
      if (a === "side to side") return 1;
      var p = (time / 27) % 1;
      if (p < 0) p += 1;
      return 0.5 * smoothstep(0.06, 0.16, p) + 0.5 * smoothstep(0.28, 0.38, p)
        - 0.5 * smoothstep(0.56, 0.66, p) - 0.5 * smoothstep(0.78, 0.88, p);
    }

    // THE RESPONSE CURVE (darkroom draft D2): equal movements of the hand produce equal felt change.
    // A two-piece exponential hinged at the median of the felt change of one half, mirrored about the
    // middle because a whole work stands at either end. The dead bands at either end are what make
    // both doors exact: at mix 0 the duty is a whole 1 and at mix 1 a whole 0.
    var FEEL_D0 = 0.06, FEEL_C = 0.43, FEEL_K1 = -1.6, FEEL_K2 = 1.8;
    function feelLog(x, k) {
      return Math.abs(k) < 1e-6 ? x : (Math.exp(k * x) - 1) / (Math.exp(k) - 1);
    }
    function feelKnee(u) {
      return u <= 0.5 ? FEEL_C * feelLog(2 * u, FEEL_K1)
                      : FEEL_C + (1 - FEEL_C) * feelLog(2 * u - 1, FEEL_K2);
    }
    function feelOf(u) {
      var f = u <= 0.5 ? 0.5 * feelKnee(2 * u) : 1 - 0.5 * feelKnee(2 - 2 * u);
      return FEEL_D0 + (1 - 2 * FEEL_D0) * f;
    }

    // The numbers of one frame: everything the shader gets beyond the seating of the two works is a
    // pure function of the pose. The host calls this; so does the lab's own carrier, from the same
    // source — which is why the two roads can be compared frame against frame.
    function values(st) {
      var ab = Math.abs(st.bal);
      var shaped = (st.bal < 0 ? -1 : 1) * smoothstep(0.08, 0.88, ab);
      var duty = 0.5 + 0.5 * shaped;
      var weave = 1 - smoothstep(0.14, 0.86, ab);
      return {
        duty: duty,
        amp: Math.min(AMP * weave * st.press, TRAVEL),
        nV: clamp(st.strips * st.nMul * clamp(st.cssWidth / 1000, 0.5, 1), 6, 64),
        rot: st.reduced ? 0 : rotForTime(st.t, st.axis),
      };
    }

    var manifest = {
      id: "weave", api: 1, arity: 2,
      roles: ["disassembly", "mystery", "assembly"],
      levels: ["SURFACE", "CELL"],
      params: { strips: [8, 64], axis: [0, 2], speed: [0.1, 2.5] },
      // EVERY handle a score can drive (§4.4b). `mix` is the dial; `clock` is the second the host
      // hands down; the other four were the module's own params and its own die, and they are
      // published here so no handle keeps a clock or a roll of its own.
      //
      // THE THREE THAT ANSWERED TO NO TRACK, brought across 2026-08-14. The module ran these on its
      // own eased clock, so under a scored run they kept moving on wall time and one seed gave a
      // different picture (§4.4b names exactly this defect):
      //   · `nMul` — THE STRIP-COUNT BREATH. The module drifts it as 1 + 0.35·sin(t·0.021·TAU + 1.1)
      //     when nobody drives, and the hand reaches 0.62 … 1.65 across the frame (weave.js:452,
      //     :443). Those two ends are the module's own, so they are the range here.
      //   · `press` — THE PRESS RESPONSE. It eases toward PRESS = 1.30 held down and back to 1 let
      //     go (weave.js:236, :466). Resting at 1 is what the module itself does under a parked
      //     pointer, so 1 is the default and 1.30 the far end.
      //   · `bal` — THE BALANCE ITSELF, which the module drifts as 0.97·sin(t·0.030·TAU)³ when no
      //     dial holds it (weave.js:450–451). It is OPEN: a score that names no track for it leaves
      //     the instrument deriving the balance from `mix` through the response curve, exactly as
      //     the module lets its own dial win over the drift (weave.js:459). Nothing falls back, so
      //     nothing is recorded as a fallback.
      handles: {
        mix: { min: 0, max: 1, def: 0 },
        clock: { min: 0, max: 14, def: 0 },
        strips: { min: 8, max: 64, def: 28 },
        axis: { min: 0, max: 2, def: 2 },
        speed: { min: 0.1, max: 2.5, def: 1 },
        seed: { min: 0, max: 8, def: 0 },
        nMul: { min: 0.62, max: 1.65, def: 1 },
        press: { min: 1, max: PRESS, def: 1 },
        bal: { min: -1, max: 1, def: 1, open: true },
      },
      neutrals: { a: 0, b: 1 },
      doors: { in: { handle: "mix", value: 0, work: "a" },
               out: { handle: "mix", value: 1, work: "b" } },
      // Both doors frame alike, so one record covers them: the constant centre crop the strips'
      // travel pays for (ZOOM above; module-contract.json publishes the same 1.29).
      framings: { "0": { coverCrop: ZOOM }, "1": { coverCrop: ZOOM } },
      drivers: ["progress", "cueProgress", "time", "velocity", "capability", "noise", "static",
                "curve", "spline", "map", "add", "multiply", "mix", "clamp", "hold", "segment",
                "ramp", "slew", "oscillate", "node"],
      camera: { needs: "none", authority: "stage" },
      gl: { preserveDrawingBuffer: false },
      neutralPose: { bal: 1, nMul: 1, press: 1, strips: 28, axis: 2, cssWidth: 1000, t: 0, reduced: false },
      passes: [{
        program: "weave", vert: VERT, frag: FRAG, position: "aPos",
        uniforms: [
          { name: "uA", type: "sampler2D", source: "textureA" },
          { name: "uB", type: "sampler2D", source: "textureB" },
          { name: "uFitA", type: "vec4", source: "fitA" },
          { name: "uFitB", type: "vec4", source: "fitB" },
          { name: "uRes", type: "vec2", source: "resolution" },
          { name: "uT", type: "float", source: "seconds" },
          { name: "uNv", type: "float", source: "frame:nV" },
          { name: "uDuty", type: "float", source: "frame:duty" },
          { name: "uAmp", type: "float", source: "frame:amp" },
          { name: "uRot", type: "float", source: "frame:rot" },
          { name: "uSpeed", type: "float", source: "handle:speed" },
          { name: "uSeed", type: "float", source: "handle:seed" },
        ],
      }],
      // The instrument allocates NOTHING of its own: it spends the two source-texture slots the host
      // already holds and the one programme the host builds from this manifest.
      resources: { lean: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                           passes: 1, bytesEstimate: 0, variant: "lean" },
                   standard: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                               passes: 1, bytesEstimate: 0, variant: "standard" },
                   rich: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                           passes: 1, bytesEstimate: 0, variant: "rich" } },
      capabilities: ["webgl2"],
      decline: ["one work only", "a source that never decoded"],
      provenance: { labPath: "lab/effects/weave.js", commit: "547a100" },
      readiness: "production-ready",
    };

    var live = false;
    return {
      name: "weave",
      manifest: manifest,
      values: values,
      fit: fit,
      feel: feelOf,
      prepare: function (o) {
        if (!o.sources) return { take: false, why: "the woven instrument needs both works" };
        if (!o.cue) return { take: false, why: "no cue names it" };
        return { take: true };
      },
      start: function () { live = true; },
      // The pose the shader draws. Every number in it now comes from a handle a score can drive, so
      // a seeded run repeats to the pixel with every voice scored. `bal` is the one open handle: a
      // score that drives it directly carries the module's own drift, and a score that says nothing
      // about it leaves the balance derived from the dial through the response curve, which is how
      // the module itself resolves the same pair.
      //
      // The remaining voices ride these handles rather than constants: the two width breaths at
      // their own unaligned rates (0.31 and 0.24 + 1.7 rad) and the 27 s turn with its unequal holds
      // of 3.2 s and 4.9 s read `clock`; the strips' travel reads `clock` and `speed` together
      // (speed × 0.17, the horizontal at 0.86 of it + 0.31 turn); the over/under order reads `seed`.
      // Their rates stay inside the shader and inside rotForTime, where their author put them.
      frame: function (st) {
        if (!live) return;
        var h = st.handles;
        var bal = typeof h.bal === "number" ? h.bal : 1 - 2 * feelOf(clamp(h.mix, 0, 1));
        st.draw({
          bal: bal,
          nMul: h.nMul, press: h.press,
          strips: h.strips, axis: h.axis, speed: h.speed, seed: h.seed,
          cssWidth: st.viewport.w, t: h.clock, reduced: st.reduced,
        });
        if (st.progress >= 1 && !st.pinned) st.settle(st.token);
      },
      resize: function () {},
      cancel: function () {},
      dispose: function () { live = false; },
      contextLost: function () { live = false; },
      contextRestored: function () {},
    };
  }

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
      "  gl_FragColor = vec4(col, 1.0);",
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

    // The numbers of one frame: everything the shader gets beyond the seating of the two works is a
    // pure function of the pose (matter.js:309-329). The threshold travels a tenth past either end
    // of the field and no further — past the field's own range every point stands on one side and
    // the work is whole, which is what makes both doors exact.
    function values(st) {
      var d = feelOf(clamp(st.mix, 0, 1));
      var grainA = GRAIN_MIN + (GRAIN_MAX - GRAIN_MIN) * clamp(st.grain, 0, 1);
      var reach = 0.5 + 0.10;
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
        grain: { min: 0, max: 1, def: 0.45 },
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
      neutralPose: { mix: 0, loosen: 0.6, drift: 0.45, gather: 0.3, grain: 0.45,
                     seed: 0, shade: 1, travel: 1, t: 0, reduced: false },
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
      frame: function (st) {
        if (!live) return;
        var h = st.handles;
        st.draw({
          mix: h.mix, loosen: h.loosen, drift: h.drift, gather: h.gather, grain: h.grain,
          shade: h.shade, travel: h.travel, seed: h.seed, t: h.clock, reduced: st.reduced,
        });
        if (st.progress >= 1 && !st.pinned) st.settle(st.token);
      },
      resize: function () {},
      cancel: function () {},
      dispose: function () { live = false; },
      contextLost: function () { live = false; },
      contextRestored: function () {},
    };
  }

  // ================================================================================================
  // THE MESHING INSTRUMENT (§8) — lab/effects/gears.js carried across
  // ================================================================================================
  // TWO WHEELS, MESHING. Their centres stand off the frame on either side, so what the eye sees is
  // the line where the two rims meet — a row of interlocking teeth running down the picture — and the
  // crossing is that line rolling across the frame, one work riding each wheel.
  //
  // What came over: the shader, the seating of a work in the frame (coverFit), the response curve
  // (the measured inverse FEEL_Q), the ladder of small whole ratios, and the numbers of one frame
  // (values). What stayed behind: its own canvas, its own WebGL 1 context, its own frame loop, its
  // resize listener and its own clock. The instrument here reads no wall clock, holds no listener,
  // creates no context and loads no picture (§1.2's fence).
  //
  // THE FOUR THINGS THE MODULE'S CARD ASKED A PORT TO PROVE (docs/immersive/effects/gears.md §11),
  // and where each stands here.
  //   1. The uniform set is bound BY DECLARED NAME from the manifest below — nineteen names, of
  //      which only six are shared with the woven instrument. The host reads the manifest; no list
  //      of names is written into the host.
  //   2. `preserveDrawingBuffer` is off. The lab module asked for it at gears.js:276 and drew only
  //      on a parameter change, on a resize and on its own frame loop, so the preserved buffer was
  //      standing in for the frames it did not draw. THE REDRAW IT STOOD IN FOR IS CARRIED: this
  //      instrument draws on EVERY frame the host hands it, including a reduced-motion run, where
  //      the module rendered once and stopped. Reduced motion stops the wheels' drive and never the
  //      drawing.
  //   3. The `ratio` handle steps through the module's own ladder of small whole pairs and is never
  //      interpolated. A tooth count is a whole number by the time it reaches the shader, so a tooth
  //      of one wheel always meets a gap of the other and the mesh closes on itself.
  //   4. The shader carries no version header of its own, so the host's translator stamps exactly
  //      one. A row counts them.
  //
  // ONE LINE OF THE SHADER IS NOT THE MODULE'S. The lab module hands the frame's aspect in as its
  // own uniform, computed from the drawing buffer it owns. The host owns the buffer here and already
  // binds its size as `uRes`, so the aspect is derived from `uRes` inside the shader. The mathematics
  // then reads the buffer the host actually drew into, whatever the resolution ladder has done to it.
  // Every other line of the shader is the module's own, character for character.
  function gearsInstrument() {
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
      "uniform vec2 uCA;",            // the first wheel's centre, frame half-heights
      "uniform vec2 uCB;",            // the second wheel's
      "uniform float uR1;",           // their pitch radii
      "uniform float uR2;",
      "uniform float uN1;",           // and their tooth counts, which stand in the same ratio
      "uniform float uN2;",
      "uniform float uAmp;",          // how far a tooth stands out of the pitch circle
      "uniform float uPh;",           // where the teeth stand along the rims: the wheels' own turn
      "uniform float uFlank;",        // how upright a tooth's flank is
      "uniform float uSpread;",       // how far apart the teeth's own moments are set
      "uniform float uSeed;",
      "uniform float uOff;",          // counter-motion, tangential, frame heights
      "uniform float uGuard;",
      "const float PI = 3.14159265359;",
      "const float TAU = 6.28318530718;",

      "float hash11(float n){ return fract(sin(n * 127.1) * 43758.5453); }",

      // A TOOTH, not a wave. A cosine gives a boundary that curves the whole way and reads as a
      // blob; a tooth stands out to its full height, holds there across its own top, and drops on
      // a flank. uFlank is how much of a tooth is flank — the clamp does the holding.
      "float tooth(float x){ return clamp(sin(x) / uFlank, -1.0, 1.0); }",
      "float toothD(float x){ return abs(sin(x)) < uFlank ? cos(x) / uFlank : 0.0; }",

      "vec2 into(vec2 p, vec4 f){",
      "  return clamp((p - 0.5) * f.xy + 0.5 + f.zw, 0.0008, 0.9992);",
      "}",

      "void main(){",
      "  vec2 uv = vUv;",
      // the aspect of the buffer the host drew into, read from the size the host binds
      "  float uAspect = uRes.x / max(uRes.y, 1.0);",
      // the frame in half-heights: x across, y up
      "  vec2 p = vec2((uv.x - 0.5) * 2.0 * uAspect, (0.5 - uv.y) * 2.0);",
      "  float h = 2.0 / max(uRes.y, 1.0);",

      // EACH WHEEL, AS A RIM. The point stands somewhere out from each centre; the rim it is being
      // held against is the pitch circle with the teeth standing on it, and how far INSIDE that rim
      // the point lies is what decides whose the point is.
      "  vec2 dA = p - uCA;   float rA = max(length(dA), 1e-5);",
      "  vec2 dB = p - uCB;   float rB = max(length(dB), 1e-5);",
      "  vec2 uAv = dA / rA;  vec2 nA = vec2(-uAv.y, uAv.x);",
      "  vec2 uBv = dB / rB;",
      // the angle round each wheel, both counted from the ray that runs to the point where the two
      // rims meet — so ONE arc length, one pitch, and the two sets of teeth cannot drift apart
      "  float thA = atan(dA.y, dA.x);",
      "  float thB = atan(dB.y, -dB.x);",
      "  float wA = uN1 * thA + uPh;",
      "  float wB = uN2 * thB + uPh;",
      // the second wheel's teeth are the first's turned inside out: where one stands, the other is
      // a gap, which is what meshing is
      "  float RA = uR1 + uAmp * tooth(wA);",
      "  float RB = uR2 - uAmp * tooth(wB);",

      // WHICH WEDGE OF WHICH WHEEL, and when that tooth hands over: six parts a ladder down the
      // line where the two rims meet, four parts the score's die.
      "  float ti = floor(wA / TAU);",
      "  float ladder = clamp(0.5 + 0.5 * p.y, 0.0, 1.0);",
      "  float ord = mix(ladder, hash11(ti + uSeed), 0.4);",

      "  float M = (RA - rA) - (RB - rB) + uSpread * (ord - 0.5);",
      // the field's own gradient, exactly: the rims' own turning plus the two radial directions
      "  vec2 gB = vec2(dB.y, -dB.x) / (rB * rB);",
      "  vec2 gM = uAmp * toothD(wA) * uN1 * nA / rA",
      "          + uAmp * toothD(wB) * uN2 * gB",
      "          - uAv + uBv;",
      "  float grad = max(length(gM), 1e-5);",
      "  float d = M / (grad * h);",
      "  float cov = clamp(0.5 + d, 0.0, 1.0);",

      // the two works sweep along their own rims, against each other at the mesh — the flanks of
      // two meshing teeth slide past one another, and this is that slide
      "  vec2 tA = vec2(nA.x / max(uAspect, 0.05), -nA.y);",
      "  vec2 tB = vec2(-uBv.y / max(uAspect, 0.05), uBv.x);",
      "  vec3 colA = texture2D(uA, into(uv + tA * uOff, uFitA)).rgb;",
      "  vec3 colB = texture2D(uB, into(uv - tB * uOff * (uN1 / max(uN2, 1.0)), uFitB)).rgb;",
      "  vec3 col = mix(colB, colA, cov);",

      "  col *= 1.0 - 0.32 * uGuard * (1.0 - cov) * exp(-max(-d, 0.0) / 7.0);",
      "  gl_FragColor = vec4(col, 1.0);",
      "}",
    ].join("\n");

    function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
    function smoothstep(a, b, x) {
      var t = (x - a) / (b - a);
      t = t < 0 ? 0 : t > 1 ? 1 : t;
      return t * t * (3 - 2 * t);
    }

    // THE SMALL WHOLE RATIOS the handle walks. A gear pair is only a gear pair when the two counts
    // stand in a ratio of small whole numbers — that is what makes the mesh close on itself — so the
    // handle does not slide through the reals: it steps through this ladder. The `ratio` handle is a
    // place on the ladder and is rounded to a rung before any count is taken from it.
    var RATIOS = [[1, 1], [3, 4], [2, 3], [1, 2], [2, 5], [1, 3], [1, 4]];

    // THE TANGENTIAL SWEEP, in frame heights, and the crop that pays for it. The sweep is bounded
    // and the wheels' own turning is unbounded — the teeth go round for as long as the clock runs,
    // while the pictures only lean into the sweep — so the crop stays small.
    var AMP = 0.05;
    var ZOOM = 1 + 2 * AMP + 0.03;

    // How tall a tooth stands against its own pitch. A real gear tooth stands about a third of its
    // pitch out of the pitch circle on each side; below about a tenth the mesh reads as a wavy line
    // and above about a half the teeth are longer than they are wide and read as a comb.
    var TOOTH_MIN = 0.12, TOOTH_MAX = 0.40;

    // THE MEASURED RESPONSE CURVE, carried over digit for digit (gears.js:329-337). How far the
    // picture moves per unit of the raw travel was measured with the curve taken out of the module,
    // that rate integrated, and this is the inverse of the integral at twenty-one evenly spaced
    // shares, with straight lines between them. Half the whole change stands at 0.28 of the travel,
    // which is why no two-piece logarithm fits it.
    var FEEL_D0 = 0.05;
    var FEEL_Q = [0, 0.0272, 0.0544, 0.0815, 0.1084, 0.1348, 0.1608, 0.1869, 0.214, 0.244,
                  0.2807, 0.3286, 0.3865, 0.4545, 0.545, 0.6185, 0.6926, 0.7607, 0.8211,
                  0.8897, 1];
    function feelOf(u) {
      var x = clamp((u - FEEL_D0) / (1 - 2 * FEEL_D0), 0, 1);
      var s = x * (FEEL_Q.length - 1), i = Math.min(FEEL_Q.length - 2, Math.floor(s));
      return FEEL_Q[i] + (FEEL_Q[i + 1] - FEEL_Q[i]) * (s - i);
    }

    // cover-fit a work into the frame, then pull in by the travel headroom. The host hands the
    // source's own dimensions, so the instrument never touches an image object.
    function fit(iw, ih, w, h) {
      var fa = w / Math.max(h, 1);
      var ia = iw / Math.max(ih, 1);
      var sx, sy;
      if (ia > fa) { sx = fa / ia; sy = 1; } else { sx = 1; sy = ia / fa; }
      return [sx / ZOOM, sy / ZOOM, 0, 0];
    }

    function ratioAt(v) { return RATIOS[Math.round(clamp(v, 0, 1) * (RATIOS.length - 1))]; }

    // ---- WHERE THE RIMS MEET AT A DOOR, SOLVED RATHER THAN APPROXIMATED ---------------------------
    // At a door one whole work stands, which asks that the mask cover the whole frame: at door 0
    // every point of the frame lies inside the first wheel's rim, at door 1 every point lies inside
    // the second's. The module holds that by standing the meeting line beyond the frame's own edge
    // by `2·amp + spread/4 + 0.08`, which is the right margin for ONE wheel size — the module's own
    // R_BASE of 4.5, where the two rims are nearly straight across the frame and the field grows as
    // twice the distance from the meeting line.
    //
    // The port lets the wheel size travel, because that is what carries the pair's own reading from
    // angular to ring. At a small size the rims are no longer straight: the field is a function of
    // the ANGLE about the pair, it reaches its full depth only far from the pair, and the module's
    // margin leaves teeth of the far work standing in the frame's corners. So the condition itself
    // is solved instead of approximated.
    //
    // The condition, written out. Away from the teeth the mask's field is
    //     G(p) = R1 − R2 + |p − cB| − |p − cA|,
    // and the teeth and the spread move it by at most `2·amp + spread/2`. G is monotone over the
    // frame, so its extremes stand at the frame's four corners. Door 0 asks that the smallest G over
    // those corners stand above that much, door 1 that the largest stand below it. G improves as the
    // pair is carried further out, so a bisection on the reach finds the smallest reach that answers
    // both doors. The walk is a fixed count of steps and reads no clock, so a seeded run repeats.
    var DOOR_SLACK = 0.02;   // half-heights; the mask crosses over within about half a point of the
                             // boundary, and this stands well clear of that on any frame the host runs
    function gAt(px, py, cA, cB, R1, R2) {
      var ax = px - cA[0], ay = py - cA[1], bx = px - cB[0], by = py - cB[1];
      return R1 - R2 + Math.sqrt(bx * bx + by * by) - Math.sqrt(ax * ax + ay * ay);
    }
    // The smallest and largest G over the frame's four corners, with the pair standing at `xc`.
    function gEdge(xc, ox, oy, R1, R2, aspect) {
      var cA = [xc - R1 + ox, oy], cB = [xc + R2 + ox, oy];
      var lo = Infinity, hi = -Infinity, i, j, g;
      for (i = -1; i <= 1; i += 2) {
        for (j = -1; j <= 1; j += 2) {
          g = gAt(i * aspect, j, cA, cB, R1, R2);
          if (g < lo) lo = g;
          if (g > hi) hi = g;
        }
      }
      return { lo: lo, hi: hi };
    }
    function doorsHold(reach, ox, oy, R1, R2, aspect, need) {
      return gEdge(reach, ox, oy, R1, R2, aspect).lo > need
          && gEdge(-reach, ox, oy, R1, R2, aspect).hi < -need;
    }
    function reachFor(aspect, ox, oy, R1, R2, amp, spread) {
      var need = 2 * amp + 0.5 * spread + DOOR_SLACK;
      // the module's own margin first, widened by however far the centre has been carried across
      var base = aspect + 2 * amp + spread * 0.25 + 0.08 + Math.abs(ox);
      if (doorsHold(base, ox, oy, R1, R2, aspect, need)) return base;
      var lo = base, hi = base, i;
      for (i = 0; i < 48 && !doorsHold(hi, ox, oy, R1, R2, aspect, need); i++) {
        lo = hi;
        hi = hi * 2 + 1;
      }
      for (i = 0; i < 48; i++) {
        var mid = 0.5 * (lo + hi);
        if (doorsHold(mid, ox, oy, R1, R2, aspect, need)) hi = mid; else lo = mid;
      }
      return hi;
    }

    // THE NUMBERS OF ONE FRAME. Everything the shader gets beyond the seating of the two works is a
    // pure function of the pose. This is the module's own `values()` with three of its constants
    // published as handles: the pair's own size (the module's R_BASE), the tooth pitch (the module's
    // `teeth`, said as the band period it makes) and the pair's centre (the module pins it to the
    // middle of the frame's height).
    function values(st) {
      var aspect = Math.max(st.cssWidth, 1) / Math.max(st.cssHeight, 1);
      var d = clamp(st.dial, 0, 1);
      var rr = ratioAt(st.ratio);

      // THE PAIR. The two works' repeat counts stand as the ratio of the two WHEELS — equal tooth
      // pitch, counts and radii in one and the same small whole ratio, so the mesh closes on itself
      // and a tooth of one always meets a gap of the other. The pitch is the band period the score
      // holds, said in frame half-heights; the counts follow from it and from the pair's size,
      // rounded to whole teeth so the closing is exact.
      var pitch = clamp(2 * st.bandPeriod, 0.04, 2.0);
      var size = clamp(st.size, 0.3, 8);
      // BOTH COUNTS COME FROM ONE WHOLE MULTIPLIER, which is what holds them in the rung's own
      // ratio. The module takes the first count from the geometry and the second by rounding
      // `n1 · r2/r1`, and at the rungs whose first number is above one that rounding lands off the
      // ratio: 3:4 comes out as 14:19 and 2:3 as 13:20, and a mesh in 19:14 does not close on
      // itself — a tooth stops meeting a gap after one turn. Counting in whole rungs holds the ratio
      // exactly and returns the module's own 57:114 at the module's own handles, so nothing about
      // its default frame moves.
      var span = rr[0] + rr[1];
      var k = Math.max(1, Math.round(TAU * size * 2 / (span * pitch)));
      while (rr[0] * k < 3 || rr[1] * k < 3) k++;
      var n1 = rr[0] * k, n2 = rr[1] * k;
      var R1 = n1 * pitch / TAU, R2 = n2 * pitch / TAU;
      var amp = pitch * (TOOTH_MIN + (TOOTH_MAX - TOOTH_MIN) * clamp(st.tooth, 0, 1));

      // How far apart the teeth's own moments stand, in the mask's own units. The mask reads about
      // twice the distance from the line where the rims meet, so a spread of one moves a tooth's own
      // moment by a quarter of a frame height — one tooth handing over while its neighbour has not.
      var spread = clamp(st.order, 0, 1) * 1.2;

      // A TOOTH STANDS NO TALLER THAN THE WHEEL IT STANDS ON. Away from the teeth the mask's field
      // runs from −2·R2 to +2·R1, so a door can only be a whole work while the teeth and the spread
      // together stay inside that depth. At the module's own size the depth is nine half-heights and
      // nothing comes near it; at a small pair with a far-apart ratio the two together can ask for
      // more than the field holds, and then no placement of the pair makes either door whole. Both
      // are scaled back together, which keeps their proportion and keeps both doors exact.
      var room = 2 * Math.min(R1, R2) * 0.85 - DOOR_SLACK;
      var want = 2 * amp + 0.5 * spread;
      if (want > room) {
        var back = room > 0 ? room / want : 0;
        amp *= back;
        spread *= back;
      }

      // WHERE THE PAIR STANDS ACROSS THE FRAME. The centre travels in the frame's own coordinates,
      // the same ones the radial measure reads: x across from the left edge, y down from the top.
      var ox = (clamp(st.centreX, 0, 1) - 0.5) * 2 * aspect;
      var oy = (0.5 - clamp(st.centreY, 0, 1)) * 2;

      var reach = reachFor(aspect, ox, oy, R1, R2, amp, spread);
      var xc = reach - 2 * reach * d;

      // THE WHEELS TURN, and they turn from two things at once. THE TRAVEL rolls them: the pair moves
      // across the frame and the rims roll on each other without slipping, one tooth of turn for
      // every tooth of travel, which is why the teeth never come unmeshed. THE CLOCK drives them on
      // top of that, windowed to nothing at both doors, so the first work stands still, the drive
      // spins up, and the second is brought to standing exactly as it lands.
      var win = Math.sin(Math.PI * d);
      var rate = 2.6 * clamp(st.turn, 0, 1) * win;
      var ph = (reach - xc) * (TAU / pitch) + (st.reduced ? 0 : st.t) * rate;

      return {
        n1: n1, n2: n2, R1: R1, R2: R2, amp: amp, ph: ph, spread: spread,
        flank: clamp(st.flank, 0.05, 1),
        cA: [xc - R1 + ox, oy], cB: [xc + R2 + ox, oy],
        off: clamp(st.travel, 0, 1) * AMP * 4 * d * (1 - d),
        guard: clamp(st.shade, 0, 1) * smoothstep(0, 0.09, d) * smoothstep(1, 0.91, d),
        // read on the diagnostic surface, bound to no uniform: what the handles came to
        pitch: pitch, reach: reach, xc: xc, rate: rate, dial: d, size: size,
        ratioN: rr[0] * 1000 + rr[1],
      };
    }

    var manifest = {
      id: "gears", api: 1, arity: 2,
      roles: ["disassembly", "mystery", "assembly"],
      levels: ["SURFACE", "CELL"],
      params: { bandPeriod: [0.02, 1], ratio: [0, 1], size: [0.3, 8] },
      // EVERY handle a score can drive (§4.4b). The module ran its wheels on its own accumulating
      // clock and held its judges, its die and its flank as constants; all of them are published
      // here, so no handle keeps a clock or a roll of its own and a seeded run repeats to the pixel.
      //
      // THE THREE THE PORT PUBLISHES THAT THE MODULE HELD AS CONSTANTS, and why each is a handle:
      //   · `size` — THE PAIR'S OWN SIZE in frame half-heights, the module's R_BASE of 4.5. The
      //     module's own note names both ends of it: "Below about three the rims curve hard enough
      //     inside the frame to read as two circles overlapping; above about eight they are straight
      //     and the pair stops reading as wheels at all" (gears.js:211-215). That is the axis the
      //     measured pair travels along, so it is published rather than pinned.
      //   · `bandPeriod` — THE TOOTH PITCH, said as the period of the tooth line as a fraction of the
      //     frame's height. The module carried the same number as a whole count of teeth across the
      //     height, stepped 3 to 12; said as a period it is the unit the pair's own measurement uses,
      //     and the count no longer has to be whole, which is what puts the pair's measured period
      //     inside reach.
      //   · `centreX`/`centreY` — WHERE THE PAIR STANDS, in the frame's own coordinates. The module
      //     pins the pair to the middle of the frame's height and carries it across the frame on the
      //     dial alone. The field is built from the distance to each centre, so carrying both centres
      //     together moves the whole construction and changes no mathematics.
      //
      // `dial` is OPEN: a score that names no track for it leaves the instrument deriving the
      // travelled number from `mix` through the measured response curve, exactly as the module does.
      // Nothing falls back, so nothing is recorded as a fallback.
      handles: {
        mix: { min: 0, max: 1, def: 0 },
        clock: { min: 0, max: 14, def: 0 },
        dial: { min: 0, max: 1, def: 0, open: true },
        size: { min: 0.3, max: 8, def: 4.5 },
        centreX: { min: 0, max: 1, def: 0.5 },
        centreY: { min: 0, max: 1, def: 0.5 },
        bandPeriod: { min: 0.02, max: 1, def: 1 / 6 },
        ratio: { min: 0, max: 1, def: 0.5 },
        tooth: { min: 0, max: 1, def: 0.4 },
        order: { min: 0, max: 1, def: 0.4 },
        turn: { min: 0, max: 1, def: 0.55 },
        flank: { min: 0.05, max: 1, def: 0.35 },
        seed: { min: 0, max: 8, def: 0 },
        shade: { min: 0, max: 1, def: 1 },
        travel: { min: 0, max: 1, def: 1 },
      },
      neutrals: { a: 0, b: 1 },
      doors: { in: { handle: "mix", value: 0, work: "a" },
               out: { handle: "mix", value: 1, work: "b" } },
      // Both doors frame alike, so one record covers them: the constant centre crop the tangential
      // sweep is paid for with (ZOOM above, 1.13).
      framings: { "0": { coverCrop: ZOOM }, "1": { coverCrop: ZOOM } },
      drivers: ["progress", "cueProgress", "time", "velocity", "capability", "noise", "static",
                "curve", "spline", "map", "add", "multiply", "mix", "clamp", "hold", "segment",
                "ramp", "slew", "oscillate", "node"],
      // The construction moves no point of view: it decides which wheel owns each point of the frame
      // and slides the two works along their own rims inside it. Both are what it does to its own
      // surface, so the witness camera stays the stage's (§6).
      camera: { needs: "none", authority: "stage" },
      gl: { preserveDrawingBuffer: false },
      neutralPose: { dial: 0, size: 4.5, centreX: 0.5, centreY: 0.5, bandPeriod: 1 / 6, ratio: 0.5,
                     tooth: 0.4, order: 0.4, turn: 0.55, flank: 0.35, shade: 1, travel: 1,
                     cssWidth: 1000, cssHeight: 1000, t: 0, reduced: false },
      passes: [{
        program: "gears", vert: VERT, frag: FRAG, position: "aPos",
        uniforms: [
          { name: "uA", type: "sampler2D", source: "textureA" },
          { name: "uB", type: "sampler2D", source: "textureB" },
          { name: "uFitA", type: "vec4", source: "fitA" },
          { name: "uFitB", type: "vec4", source: "fitB" },
          { name: "uRes", type: "vec2", source: "resolution" },
          { name: "uCA", type: "vec2", source: "frame:cA" },
          { name: "uCB", type: "vec2", source: "frame:cB" },
          { name: "uR1", type: "float", source: "frame:R1" },
          { name: "uR2", type: "float", source: "frame:R2" },
          { name: "uN1", type: "float", source: "frame:n1" },
          { name: "uN2", type: "float", source: "frame:n2" },
          { name: "uAmp", type: "float", source: "frame:amp" },
          { name: "uPh", type: "float", source: "frame:ph" },
          { name: "uFlank", type: "float", source: "frame:flank" },
          { name: "uSpread", type: "float", source: "frame:spread" },
          { name: "uOff", type: "float", source: "frame:off" },
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
      provenance: { labPath: "lab/effects/gears.js", commit: "e0f1b91" },
      readiness: "production-ready",
    };

    var live = false;
    return {
      name: "gears",
      manifest: manifest,
      values: values,
      fit: fit,
      feel: feelOf,
      prepare: function (o) {
        if (!o.sources) return { take: false, why: "the meshing instrument needs both works" };
        if (!o.cue) return { take: false, why: "no cue names it" };
        return { take: true };
      },
      start: function () { live = true; },
      // The pose the shader draws. Every number in it comes from a handle a score can drive.
      //
      // THE REDRAW THE PRESERVED BUFFER STOOD IN FOR. The lab module drew on a parameter change, on
      // a resize and on its own frame loop, and under reduced motion it drew once and stopped —
      // whatever stayed on screen after that was the preserved buffer's doing. Here the host's
      // buffer keeps nothing between frames, so this draws on every frame it is handed, reduced or
      // not. Reduced motion stops the wheels' drive inside `values` and stops nothing else.
      frame: function (st) {
        if (!live) return;
        var h = st.handles;
        var dial = typeof h.dial === "number" ? h.dial : feelOf(clamp(h.mix, 0, 1));
        st.draw({
          dial: dial,
          size: h.size, centreX: h.centreX, centreY: h.centreY, bandPeriod: h.bandPeriod,
          ratio: h.ratio, tooth: h.tooth, order: h.order, turn: h.turn, flank: h.flank,
          shade: h.shade, travel: h.travel,
          cssWidth: st.viewport.w, cssHeight: st.viewport.h, t: h.clock, reduced: st.reduced,
        });
        if (st.progress >= 1 && !st.pinned) st.settle(st.token);
      },
      resize: function () {},
      cancel: function () {},
      dispose: function () { live = false; },
      contextLost: function () { live = false; },
      contextRestored: function () {},
    };
  }

  // ---- what this pack declares --------------------------------------------------------------
  // The host reads this record and registers each instrument under the name its own manifest
  // carries. An instrument whose manifest asks for something the host cannot supply is refused
  // here with its reason, and the pack is refused whole: a stack missing a voice is a picture
  // nobody wrote.
  join({
    version: PACK_VERSION,
    instruments: [weaveInstrument(), matterInstrument(), gearsInstrument(), adriftInstrument()],
  });
})();
