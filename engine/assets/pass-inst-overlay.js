/*!pass-inst-overlay.js*/
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
  // THE OVERLAY INSTRUMENT (§8) — lab/effects/overlay.js carried across
  // ================================================================================================
  // WHAT THE VISITOR SEES. Two of the works lie one over the other and turn slowly against each
  // other, each on its own period and the opposite way, and where they cross a third picture stands
  // that is neither of them. A slow field tips different places of the frame toward different works,
  // so both stay findable somewhere. At either end of the dominance travel one work stands alone,
  // exactly as its file carries it, with none of this instrument's own hand on it.
  //
  // WHY IT STANDS HERE. It is the only instrument on the LIGHT-COLOUR level. The charter's levels
  // law allows one voice per level, and the five instruments the settings record publishes hold
  // WORLD, SURFACE, CELL, CELL CONTENT and TEXTURE between them — a plan wanting a colour voice has
  // had none to reach for. It is also the multi-exposure of the charter's shelf 10 and his own В22,
  // «a double-exposure moment mixed into a transport middle», and the vocabulary table carries his
  // standing verdict on it: approved, «переход + vista», level LIGHT-COLOUR.
  //
  // WHAT CAME OVER: the six blend rules and the tone table that conditions each one going in and
  // holds it to a readable exposure coming out, the two layers' turns, scale breaths and drifts, the
  // one envelope every axis of the frame hangs on, the two-stage dial with the second work's colour
  // ahead of its forms, the mix field, the interfered arrival, the presence region with its own
  // spread and its own edge, the highlight shoulder, the corner shading, the dither and the three
  // measured response curves. WHAT STAYED BEHIND: its own canvas and WebGL context, its own textures
  // and their mipmap chains, its own rAF clock, its pointer listeners, its resize observer, and the
  // hunt it walked its own dominance by when nobody held it (§1.2's fence, and §4.4b for the hunt —
  // a handle that walks itself makes a seeded score draw two different pictures).
  //
  // ------------------------------------------------------------------------------------------------
  // THE THREE THINGS THE PORT HAD TO DECIDE, AND WHAT DECIDED THEM
  // ------------------------------------------------------------------------------------------------
  // 1. WHERE THE WORKS SIT IN THE FRAME. The module's own line reads the FRAME and not the
  //    photograph: a frame at least as wide as it is tall is filled edge to edge, and a taller one
  //    pulls back to `lo + 0.62 * (hi - lo)` so a square work is not cropped down to a strip. That
  //    line exists because the module has no host to ask for a seating; this engine has one, and
  //    lab/data/module-contract.json records the cost of the module's own answer in its own words —
  //    «a door standing in such a frame draws the file smaller than a cover-fit». So the seating is
  //    asked of the host: `fit` below cover-fits each work into the module's own unit square by that
  //    work's own two sides, and the square covers the frame's longer side. On a square frame with
  //    square works the two roads are the same arithmetic, digit for digit; on every other frame the
  //    port's doors are the plain cover fit and the module's are not, which is why `framings`
  //    publishes a crop of 1 at both doors and can.
  // 2. WHAT HAPPENS PAST THE EDGE OF A WORK. The module binds its own textures with MIRRORED_REPEAT;
  //    the host binds its two source slots CLAMP_TO_EDGE (pass-layer.js:110-113), which would smear
  //    an edge texel across everything the turn and the scale breath carry past the frame. The
  //    mirror is therefore written in the shader, one triangle wave per axis, taken in the module's
  //    own unit square — the same law the unfold's parquet is continued by.
  // 3. THE FLATTEST LEVEL OF THE ARRIVING WORK. The module reads the last step of its own mipmap
  //    chain, which is that work's colour with every form averaged out of it. The host builds no
  //    mipmap chain, so the port reads the work at a lattice of forty-nine places instead. It is
  //    the same quantity read at fewer points, and how far the two stand apart is measured and
  //    published rather than assumed — see NUMBERS TO REVISIT in the report.
  //
  // ------------------------------------------------------------------------------------------------
  // THE COVERAGE: THIS INSTRUMENT CAN LEAVE THE FRAME CARRYING NOTHING
  // ------------------------------------------------------------------------------------------------
  // §7's coverage law of 12:40 asks every instrument to say where its own matter is absent. Here it
  // is absent wherever `presence` stands below whole: a place is inside the exposure's region or
  // outside it, and outside it this instrument writes nothing at all, so whatever stands under it
  // shows through untouched. The declaration is `writes: true`, which under the placement rule
  // (§8 as amended 14:05, and `coverageWhyNo`) makes it lawful over another cue and as a whole
  // one-cue score, and unlawful as the lowest cue of a stack. That is the point of it: it is the
  // one LIGHT-COLOUR roof the engine has, and his В22 asks for exactly a roof.
  function overlayInstrument() {
    var VERT = [
      "attribute vec2 aPos;",
      // THE FRAME'S OWN COORDINATES, Y UP, which is the coordinate the module's own `gl_FragCoord`
      // gave it. Every field and every drift below is written in it, sign for sign; the one place
      // the picture is read the other way up is the texture fetch, and `pane` turns it there.
      "varying vec2 vUv;",
      "void main(){ vUv = aPos * 0.5 + 0.5; gl_Position = vec4(aPos, 0.0, 1.0); }",
    ].join("\n");

    var FRAG = [
      "precision highp float;",
      "varying vec2 vUv;",
      "uniform sampler2D uA;",
      "uniform sampler2D uB;",
      // When this exposure stands over another voice, the host supplies the actual frame that
      // voice has already made.  This is the carrier of a crossing: the second voice develops
      // the first voice's transformed matter, rather than both voices restarting from A/B and
      // merely accumulating source-over blur.  It is unavailable to a ground voice, where this
      // instrument remains its original two-work exposure.
      "uniform sampler2D uScene;",
      "uniform float uSceneAvailable;",
      // the seating of each work: how much of its own file the module's unit square carries
      "uniform vec4 uFitA;",
      "uniform vec4 uFitB;",
      "uniform vec2 uRes;",
      "uniform float uTime;",
      // the dial: dominance, the exposure's first stage, its second stage, and the one envelope
      "uniform vec4 uDial;",
      // the lean, how much of the frame the exposure stands on, which blend rule, the judges' handle
      "uniform vec4 uForm;",
      // each layer's own turn, scale and drift, already carried by the envelope
      "uniform vec4 uLayerA;",
      "uniform vec4 uLayerB;",
      // each field's own gain and the cosine and sine of the angle its lattice was cut at
      "uniform vec4 uMixField;",
      "uniform vec4 uRegionField;",
      "uniform vec4 uPre;",
      "uniform vec4 uPost;",
      // §8's `seams` block: how wide the mirrored fold's own retouch stands, in points of the
      // drawing buffer, off the host's own shared hairline reading.
      "uniform float uSeam;",

      // THE SOFTNESS OF THE REGION'S EDGE, in the units of the module's own presence field. It is a
      // fixed width and does not grow with presence: the region ARRIVES by growing, never by turning
      // up somewhere, and this number only keeps its boundary off the pixel grid's stairs.
      "const float EDGE = 0.045;",
      // PRESENCE IS A SHARE OF THE FRAME, and it is one because the field's own depths are spread
      // evenly across the region's travel: the three waves below pile up in the middle of their
      // range, and SPREAD pulls that pile flat, so the share standing at presence p is p itself.
      "const float SPREAD = 0.46;",

      "mat2 rot(float a){ float c = cos(a), s = sin(a); return mat2(c, -s, s, c); }",

      // THE CORNER OF A TRIANGLE WAVE, ROUNDED — the fleet's own `softAbs`, character for character
      // the one the folding instrument argues and draws with (`pass-inst-kaleidoscope.js`, THE
      // CREASE'S SOFTENING). Past `e` it is the absolute value to the last bit, so it costs the
      // picture nothing anywhere but at the corner itself.
      "float softAbs(float x, float e){",
      "  float a = abs(x);",
      "  return a >= e ? a : (x * x + e * e) / (2.0 * max(e, 1e-9));",
      "}",

      // PAST THE EDGE OF A WORK THE PICTURE MIRRORS. The module's own textures carry
      // MIRRORED_REPEAT; the host's two slots are clamped, so the law is written here — one triangle
      // wave per axis, in the module's own unit square, which is the same continuation the unfold's
      // parquet runs on.
      //
      // AND THE FOLD IS A SEAM (§8's `seams` block, pass-layer.js). Where a layer's own turn, scale
      // or drift carries a lookup past a work's own edge the sampling turns around, and the turn is
      // a sign flip in the lookup's own derivative — the same corner the folding instrument
      // retouches at every wedge edge. `e` rounds it over a width read in points of the drawing
      // buffer and carried into this coordinate's own units by the caller.
      "vec2 mir(vec2 q, vec2 e){",
      "  vec2 t = mod(q, 2.0);",
      "  return vec2(1.0 - softAbs(t.x - 1.0, e.x), 1.0 - softAbs(t.y - 1.0, e.y));",
      "}",

      // ONE WORK, READ AT ONE PLACE OF THE MODULE'S OWN SQUARE. The square is turned the right way
      // up for a host that uploads with no flip, and then the work is seated inside it by its own
      // two sides, which is the cover fit `fit` below computes and the host binds here.
      "vec3 pane(sampler2D tex, vec2 uv, vec4 fit, vec2 e){",
      "  vec2 q = mir(uv, e);",
      "  q.y = 1.0 - q.y;",
      "  q = (q - 0.5) * fit.xy + 0.5;",
      "  return texture2D(tex, q).rgb;",
      "}",

      // THE ARRIVING WORK AT ITS FLATTEST — its colour with every form averaged out of it. The
      // module reads the last step of its own mipmap chain, which is the exact mean of the file;
      // the host builds no mipmap chain, so this reads the same quantity at a lattice of forty-nine
      // places, each row shifted by the golden fraction so the lattice cannot fall into step with a
      // work that carries a lattice of its own. Measured against the exact mean over the
      // collection's twenty-six photographs: 5.02 of 255 mean, 3.46 median, 14.36 worst — against
      // 9.50 mean and 40.76 worst at a lattice of twenty-five. The taps are asked for only where
      // the dial has not finished, so a frame at whole exposure pays nothing for them.
      "vec3 flatOf(sampler2D tex, vec4 fit){",
      "  vec3 acc = vec3(0.0);",
      "  for (int j = 0; j < 7; j++) {",
      "    float v = (float(j) + 0.5) / 7.0;",
      "    for (int i = 0; i < 7; i++) {",
      "      float u = fract((float(i) + 0.5) / 7.0 + float(j) * 0.6180339887);",
      // The lattice stands inside the unit square by construction, so no lookup here can reach the
      // fold and the retouch has nothing to round: it is asked for at a width of nothing, which
      // leaves `softAbs` the plain absolute value.
      "      acc += pane(tex, vec2(u, v), fit, vec2(0.0));",
      "    }",
      "  }",
      "  return acc / 49.0;",
      "}",

      // SIX RULES, AND THE SIXTH WAS ADDED 13.08 FOR A MEASURED REASON. A crossing's middle wants
      // two things at once: to stand FAR from both works — so the eye cannot name which of them it
      // is looking at — and to keep the COLOURS the two works themselves carry, so it reads as a
      // meeting of two pictures rather than as a colour inversion. Of the first five, only
      // `difference` and `exclusion` stand far, and both get there by inverting colour. `light
      // difference` is the one rule that separates the two questions: the LIGHT of the frame is the
      // difference of the two works' light — a structure belonging to neither — while the COLOUR is
      // the two works' own colour, averaged, so nothing outside their palettes can appear.
      "vec3 blendPair(vec3 a, vec3 b){",
      "  float k = uForm.z;",
      "  if (k < 0.5) return 1.0 - (1.0 - a) * (1.0 - b);",          // screen
      "  if (k < 1.5) return abs(a - b);",                            // difference
      "  if (k < 2.5) return a + b - 2.0 * a * b;",                   // exclusion
      "  if (k < 3.5) return a * b;",                                 // multiply
      "  if (k < 4.5) return mix(2.0 * a * b, 1.0 - 2.0 * (1.0 - a) * (1.0 - b), step(vec3(0.5), b));",
      "  float la = dot(a, vec3(0.2126, 0.7152, 0.0722));",
      "  float lb = dot(b, vec3(0.2126, 0.7152, 0.0722));",
      "  return clamp(vec3(abs(la - lb)) + 0.5 * ((a - la) + (b - lb)), 0.0, 1.0);",
      "}",

      // A FIELD IS READ IN THE WORK'S OWN LATTICE. The module wrote its two fields on periods and
      // directions of its own; his 19:13 word lifted to the class at 19:21 asks every geometric
      // parameter to name the measurement of the photograph it reads, so each field is turned into
      // the lattice its work was cut along and scaled by the step it was cut at. At a gain of 1 and
      // an angle of nothing this is the module's own field, arithmetic for arithmetic.
      "vec2 laid(vec2 p, vec4 fld){",
      "  vec2 r = vec2(p.x * fld.y + p.y * fld.z, -p.x * fld.z + p.y * fld.y);",
      "  return r * fld.x;",
      "}",

      "void main(){",
      // THE SQUARE COVERS THE FRAME'S LONGER SIDE, and each work is seated inside the square by its
      // own two sides. The module's own line read the frame instead and pulled back on a tall one;
      // the seating the host already computes is the reading of the photograph that line was
      // standing in for, so it is asked for here. See THE THREE THINGS THE PORT HAD TO DECIDE.
      "  float m = max(uRes.x, uRes.y);",
      "  vec2 p = (vUv - 0.5) * uRes / m;",
      "  float t = uTime;",
      "  float dom = uDial.x, wet = uDial.y, sw = uDial.z, cw = uDial.w;",

      // bottom layer — slow, one way; its own travel comes alive with the envelope and rests
      // wherever the envelope rests, where the frame holds the photograph the file carries
      "  vec2 uvA = rot(uLayerA.x) * (p / uLayerA.y) + 0.5 + uLayerA.zw;",
      // top layer — faster, the other way, and the counter-turn turns it further
      "  vec2 uvB = rot(uLayerB.x) * (p / uLayerB.y) + 0.5 + uLayerB.zw;",

      // THE FOLD'S OWN RETOUCH, in each layer's own coordinate (§8's `seams` block). Each layer's
      // map is `rot(turn) · p / scale`, a rotation and a scale, so one point of the drawing buffer
      // is `1 / (scale · m)` of the layer's coordinate on either axis — `p` is the frame divided by
      // `m` and one buffer point of the frame is `1 / uRes`, and the two `uRes` cancel. It rides
      // `cw` — the envelope this file already hangs the travel, the highlight shoulder, the corner
      // shading and the dither on — because the fold can only bite where a layer's own turn, scale
      // and drift have carried a lookup off the work, and `cw` is exactly nothing at both ends of
      // the dominance travel and at the dry door. So at a door these are the plain mirror to the
      // last bit and the door's own law reads the cover fit it always read.
      "  vec2 eA = vec2(uSeam / (max(uLayerA.y, 1e-4) * m)) * cw;",
      "  vec2 eB = vec2(uSeam / (max(uLayerB.y, 1e-4) * m)) * cw;",
      "  vec3 a = pane(uA, uvA, uFitA, eA);",
      // The copied scene is a framebuffer reading, already seated and oriented in the stage's
      // coordinates.  It replaces the departing source only while a lower voice exists; at a
      // door the upper overlay's own coverage is absent, and a one-voice overlay never asks for
      // this branch.  Thus the carrier changes the middle event without weakening either exact
      // picture door.
      "  if (uSceneAvailable > 0.5) a = texture2D(uScene, vUv).rgb;",
      // THE SECOND WORK'S PALETTE ARRIVES BEFORE ITS FORMS (charter shelf 11, colour as herald): the
      // first stage of the dial carries that work read at its flattest, which is its colour with no
      // shape left in it, and the second stage grows its own picture into that colour. The flat
      // reading is asked for only where the dial has not finished, so a frame at whole exposure —
      // which is where both doors stand — pays nothing for it.
      "  vec3 b = pane(uB, uvB, uFitB, eB);",
      "  if (sw < 1.0) b = mix(flatOf(uB, uFitB), b, sw);",

      // the mix is not one number over the whole frame: a slow field tips different regions toward
      // different layers, so both pictures stay findable somewhere
      "  vec2 pm = laid(p, uMixField);",
      "  float f = sin(pm.x * 3.7 + t * 0.113) * cos(pm.y * 3.1 - t * 0.087)",
      "          + 0.60 * sin((pm.x + pm.y) * 5.3 - t * 0.061)",
      "          + 0.45 * cos((pm.x - pm.y) * 4.1 + t * 0.133);",
      "  f /= 2.05;",
      // WHERE THE FRAME STANDS BETWEEN THE TWO WORKS — dominance, region by region. Dominance
      // carries it and the field only leans it either way; the lean rides the envelope, so it is
      // widest where the two works stand level and closes to nothing at both ends of the travel.
      // Named on a score, the interfered arrival makes the lean keep growing to the wet end instead
      // of closing at it, so the places where the interference stands highest hand the frame to the
      // second work first. Both doors stay exact all the same.
      "  float w = clamp(dom + uForm.x * f, 0.0, 1.0) * wet;",

      // Each layer is conditioned on the way in — exclusion in particular goes chalky unless the top
      // layer is pushed away from mid grey first — and the composite is then held to a readable
      // exposure on the way out.
      "  vec3 ca = clamp((a - 0.5) * uPre.z + 0.5, 0.0, 1.0) * uPre.x;",
      "  vec3 cb = clamp((b - 0.5) * uPre.w + 0.5, 0.0, 1.0) * uPre.y;",
      "  vec3 bl = blendPair(ca, cb);",
      "  bl *= uPost.x;",
      "  bl = (bl - uPost.w) * uPost.y + uPost.w;",
      "  float L = dot(bl, vec3(0.2126, 0.7152, 0.0722));",
      "  bl = max(mix(vec3(L), bl, uPost.z), 0.0);",

      // w = 0 is the bottom picture alone, 0.5 the composite, 1 the top picture alone
      "  float wa = smoothstep(0.0, 1.0, clamp(w * 2.0, 0.0, 1.0));",
      "  float wb = smoothstep(0.0, 1.0, clamp(w * 2.0 - 1.0, 0.0, 1.0));",
      "  vec3 col = mix(mix(a, bl, wa), b, wb);",

      // ONE ENVELOPE ON EVERY AXIS OF THIS FRAME (charter, the grammar of liveliness, law 5). The
      // shoulder, the corner shading and the dither are the composite's own finish, so they arrive
      // with it on the one envelope: where no composite stands — the dry door, or either end of the
      // dominance travel — the frame carries the photograph untouched, which is what lets a scored
      // exposure LEAVE into the work it was resolving into.
      "  float k = 0.80;",
      "  vec3 over = max(col - k, 0.0);",
      "  col = mix(col, min(col, vec3(k)) + (1.0 - k) * (over / (over + (1.0 - k))), cw);",
      "  float r = length(p);",
      "  col *= 1.0 - 0.20 * cw * smoothstep(0.25, 0.64, r);",
      "  float n = fract(sin(dot(gl_FragCoord.xy, vec2(12.9898, 78.233))) * 43758.5453);",
      "  col += cw * (n - 0.5) / 255.0;",

      // WHERE THE EXPOSURE STANDS. A second slow field, on periods of its own that share nothing
      // with the mix field's, says how deep each place of the frame lies; presence says how far the
      // region has come. A place is inside the region or outside it — nothing here is drawn at half
      // strength — and the region GROWS as presence rises, which is how everything else in this
      // project arrives: by taking more of the frame, never by turning up faintly.
      "  vec2 pr = laid(p, uRegionField);",
      "  float fp = sin(pr.x * 7.3 - t * 0.041) * cos(pr.y * 8.9 + t * 0.057)",
      "           + 0.55 * sin((pr.y - pr.x) * 11.7 + t * 0.029);",
      "  fp /= 1.55;",
      "  float deep = 0.5 + 0.5 * tanh(clamp(fp, -1.0, 1.0) / SPREAD);",
      "  float reach = uForm.y * (1.0 + 2.0 * EDGE) - EDGE;",
      "  float stands = smoothstep(deep - EDGE, deep + EDGE, reach);",

      // THE JUDGES' CHANNEL, the map this instrument is read by: where the exposure stands, where the
      // frame stands between the two works, and how far the envelope is open. It is drawn as colour,
      // which is what it is for, and a door left with it open is refused below.
      "  col = mix(col, vec3(stands, w, cw), uForm.w);",
      // THE COVERAGE, published as the alpha the host blends by. At presence whole every point comes
      // out at 1 and the frame is the picture; below it the region's outside carries nothing at all
      // and whatever stands under this layer shows through untouched.
      "  gl_FragColor = vec4(col, stands);",
      "}",
    ].join("\n");

    var DEG = Math.PI / 180;

    // A handle a score left undriven reaches here as nothing at all, and a number that is not a
    // number would travel through the whole pose and be bound as one. Every read below goes through
    // `num`, which answers the handle's own rest where no number arrived.
    function num(v, def) { v = +v; return v === v ? v : def; }
    function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
    function unit(v) { return clamp(num(v, 0), 0, 1); }
    function smooth(x) { x = unit(x); return x * x * (3 - 2 * x); }

    // ---- THE MODULE'S OWN CONSTANTS, carried digit for digit -------------------------------------
    // Per blend rule: how hard each layer is driven going in, and how the result is pulled back to a
    // readable exposure coming out (overlay.js:40-52). Tuned by looking at the shots. Both source
    // pictures are bright, so screen and hard light have to be held back; multiply comes out too
    // dark and difference too vivid, so both are corrected. Light difference comes out dark — two
    // works of similar light stand close together — and thin in colour, because averaging two
    // chromas halves both.
    var BLENDS = ["screen", "difference", "exclusion", "multiply", "hard light", "light difference"];
    var TONE = [
      { pre: [0.56, 0.42, 1.06, 1.10], post: [1.00, 1.40, 1.10, 0.45] },   // screen
      { pre: [1.00, 1.00, 1.00, 1.00], post: [1.14, 1.08, 0.88, 0.42] },   // difference
      { pre: [1.00, 1.00, 1.12, 1.75], post: [1.00, 1.22, 1.12, 0.48] },   // exclusion
      { pre: [1.00, 1.00, 1.00, 1.00], post: [1.90, 1.16, 1.00, 0.42] },   // multiply
      { pre: [0.88, 0.80, 1.00, 1.00], post: [1.00, 1.14, 1.00, 0.50] },   // hard light
      { pre: [1.00, 1.00, 1.00, 1.00], post: [1.55, 1.10, 1.70, 0.34] },   // light difference
    ];
    // FRAG's own two consts, carried here so the door can be read in script (overlay.js:68, :229).
    var EDGE = 0.045, SPREAD = 0.46;
    // THE TWO FIELDS' OWN BASE WAVENUMBERS (overlay.js:161, :219). A field's gain below is the work's
    // own step read against these, so a work cut at exactly the module's own step gives a gain of 1
    // and the module's own field comes back arithmetic for arithmetic.
    var MIX_BASE = 3.7, REGION_BASE = 7.3;
    var MIX_PERIOD_DEF = 1 / MIX_BASE, REGION_PERIOD_DEF = 1 / REGION_BASE;
    var PERIOD_MIN = 0.02, PERIOD_MAX = 1;
    var SCALE_MIN = 0.65, SCALE_MAX = 1.7;

    // HOW WIDE THE MIRRORED FOLD'S OWN RETOUCH STANDS WHERE NO HOST HAS ANSWERED — at registration,
    // before any frame has been asked for. NOTHING, because nothing is what this file drew the fold
    // at before §8's `seams` block reached it: the wrap was the bare triangle wave and its corner
    // was left where the sampling grid found it. A fallback of one point would be a different
    // picture from the one this file used to draw, and a fallback nobody asked for is exactly the
    // number §8 exists to take away. Every drawn frame reads the host's own answer instead.
    var SEAM_POINTS = 0;
    function seamOf(st) {
      var s = st && st.seam && st.seam.tile;
      return typeof s === "number" && isFinite(s) && s > 0 ? s : SEAM_POINTS;
    }

    /* THE RESPONSE CURVES OF THIS MODULE'S THREE HANDLES (DARKROOM-DRAFT D2, his word 08-08 17:57),
       carried digit for digit from overlay.js:300-352: equal movements of the hand produce equal felt
       change. Every number was measured by walking the raw handle in steps of 0.02 and reading the
       mean channel distance between neighbouring frames.

       EXPOSURE. The travel is two stages by this module's own design (charter shelf 11, colour ahead
       of forms). Measured, the two stages are not equal and cannot be made equal: the colour stage
       moves the frame by 191 channels and the forms stage by 18, a ten to one the curve must not
       touch, because the handle's middle is where the score reads colour full and forms not yet
       begun. Inside each stage the travel is a hump, which the curve does flatten. FAMILY: an S-curve
       on each stage, hinged at the middle — v = u^s/(u^s + (1-u)^s), which fixes 0, 1/2 and 1 by
       construction. s = 0.65 is the one fitted number. Spread falls from 3.45 to 1.62 on the colour
       stage and from 3.06 to 1.06 on the forms stage.

       DOMINANCE is TWO-SIDED: a whole work at either end, the double exposure across the middle.
       Measured 78 channels a tenth at the ends against 12 in the middle, a spread of 6.8. FAMILY: a
       logarithm on each half mirrored about the middle, which keeps the two works symmetric, k = 1.65.
       The band falls from 6.34 to 1.84.

       PRESENCE is the SHARE OF THE FRAME the exposure stands on. Measured 4.9 channels in the first
       tenth and 4.4 in the last against 12 in the second, a spread of 2.8: the first and last slivers
       of the travel are the region's own soft edge arriving and closing. FAMILY: the same plain S,
       s = 0.91, with a dead band of 0.02 at either end where the frame does not move at all. The band
       falls from 2.77 to 1.51. */
    var FEEL_S = 0.65, FEEL_MIX_K = 1.65, FEEL_PRES_S = 0.91, FEEL_PRES_D = 0.02;
    var CURVE_BANDS = { exposure: [3.45, 1.62], mix: [6.34, 1.84], presence: [2.77, 1.51] };
    var CURVE_MEASURED_ON = "the drawn frame's own mean channel distance between neighbouring "
                          + "frames, read by walking the raw handle in steps of 0.02 "
                          + "(lab/effects/overlay.js:300-331)";
    function feelS(u, s) {
      if (u <= 0) return 0;
      if (u >= 1) return 1;
      var a = Math.pow(u, s), b = Math.pow(1 - u, s);
      return a / (a + b);
    }
    function feelExposure(u) {
      u = unit(u);
      return u <= 0.5 ? 0.5 * feelS(2 * u, FEEL_S) : 0.5 + 0.5 * feelS(2 * u - 1, FEEL_S);
    }
    function feelMix(u) {
      u = unit(u);
      var half = function (x) {
        return (Math.exp(FEEL_MIX_K * x) - 1) / (Math.exp(FEEL_MIX_K) - 1);
      };
      return u <= 0.5 ? 0.5 * half(2 * u) : 1 - 0.5 * half(2 - 2 * u);
    }
    function feelPresence(u) {
      return FEEL_PRES_D + (1 - 2 * FEEL_PRES_D) * feelS(unit(u), FEEL_PRES_S);
    }

    // COVER-FIT ONE WORK INTO THE MODULE'S OWN UNIT SQUARE, by that work's own two sides and nothing
    // else. The square then covers the frame's longer side (FRAG's `m`), so the two together are the
    // plain cover fit of the work into the frame at every frame shape, which is why `framings`
    // publishes a crop of 1 at both doors. The module asked for no seating and stretched a work that
    // was not square; this is the reading of the photograph that stood in for.
    function fit(iw, ih, w, h) {
      var ia = iw / Math.max(ih, 1);
      if (!(ia > 0)) return [1, 1, 0, 0];
      return [Math.min(1, 1 / ia), Math.min(1, ia), 0, 0];
    }

    // ---- THE DOOR THE INSTRUMENT READS FOR ITSELF ------------------------------------------------
    // His 18:00 architecture decision, carried in the U27 brief: the instrument reads its doors at
    // runtime on the actual buffer, and the report it hands back is the runtime truth; what the
    // manifest declares is only the claim. This is that law read in this instrument's own unit,
    // which is the SHARE OF THE FRAME the exposure stands on.
    //
    // WHAT A DOOR ASKS OF THIS INSTRUMENT. At either door the frame is one work standing whole, at
    // the plain cover fit the `framings` block publishes. Three things carry that, and all three are
    // read on the buffer rather than declared:
    //   · THE EXPOSURE REACHES ALL THE WAY. At dominance 0 the frame is the departing work whatever
    //     the exposure stands at, because the envelope is shut there; at dominance 1 it is the
    //     arriving work only where the exposure is whole, and short of that the frame is a composite.
    //   · THE EXPOSURE STANDS ON THE WHOLE FRAME. Below whole presence, part of the frame carries
    //     nothing at all, and a door with a hole in it is not the work standing whole. The reading is
    //     taken at the field's own DEEPEST possible place rather than at a walk of sample points, so
    //     it can only ever over-hold and never miss a bare one.
    //   · THE JUDGES' CHANNEL IS SHUT. `mask` draws the exposure's own map as colour, which is what
    //     it is for; left open at a door the frame is a false-colour map and not the photograph.
    //
    // THE ONE HOLD, AND WHY IT IS LAWFUL. The presence curve carries a dead band of two hundredths at
    // either end — the module's own measured stretch «where the frame does not move at all» — so a
    // score asking for whole presence is handed 0.98 and the field's deepest place comes out at 0.972
    // of full instead of 1. At a door, where the applied presence stands inside that dead band of
    // whole, it is held at exactly whole and what was held is published. Nothing a person can see
    // moves, because the band is by measurement the stretch that moves nothing; the door becomes
    // exact. Away from a door nothing is held and the curve stands as the module wrote it.
    var DOOR_SHOW = 0.5 / 255;   // half a level of 255: what the judges' channel may stand at
    var DOOR_HOLD = FEEL_PRES_D; // how far the hold reaches, in the presence curve's own dead band

    // The grid the door is read on, and which of the two it is. `drawn` says which one the sentence
    // below names, since a reader told «a 780 x 1688 frame» would look for a device that has none.
    function doorGridOf(st) {
      var bw = Math.round(st.bufWidth), bh = Math.round(st.bufHeight);
      if (bw >= 1 && bh >= 1) return { w: bw, h: bh, drawn: true, given: true };
      var cw = Math.round(st.cssWidth), ch = Math.round(st.cssHeight);
      return { w: cw, h: ch, drawn: false, given: cw >= 1 && ch >= 1 };
    }

    // HOW MUCH OF THE FRAME THE EXPOSURE STANDS ON AT ITS THINNEST POINT. The presence field is three
    // waves whose sum is bounded by 1 and reaches it, so the deepest place the field can put anywhere
    // in the frame is known in closed form; reading there is stronger than walking a grid, because a
    // walk can step over the very point a grid would show. `share` is the module's own measured law —
    // the share standing at presence p is p itself, within three parts in a hundred, whatever second
    // of the clock it is (overlay.js:224-228).
    function standsOf(presence) {
      var deep = 0.5 + 0.5 * Math.tanh(1 / SPREAD);
      var reach = presence * (1 + 2 * EDGE) - EDGE;
      return { deepest: deep, reach: reach,
               worst: smooth((reach - (deep - EDGE)) / (2 * EDGE)), share: unit(presence) };
    }

    // The numbers of one frame. Everything the shader gets beyond the seating of the two works is a
    // pure function of the pose; every number in the pose comes from a handle a score can drive, and
    // every motion reads the second the host hands down, so a seeded run repeats to the pixel.
    function posed(st, presence) {
      // THE DIAL, IN TWO STAGES, AND THE COLOUR LEADS (overlay.js:127-128). The first stage carries
      // the arriving work's colour and is full by the middle; the second brings its shapes in over
      // the rest. Both rise the whole way, so the dial never returns.
      // THE TWO CURVES THE MANIFEST SAYS ARE APPLIED, APPLIED HERE. Both are the module's own,
      // digit for digit, and both fix their own ends by construction — feelMix answers 0 at 0 and 1
      // at 1, feelExposure answers 1 at whole — so neither door moves and what the curve buys is
      // equal felt change per equal step of the hand in between.
      var exposure = feelExposure(unit(num(st.exposure, 1)));
      var dom = feelMix(unit(num(st.mix, 0)));
      var wet = smooth(clamp(exposure * 2, 0, 1));
      var sw = smooth(clamp(exposure * 2 - 1, 0, 1));
      // ONE ENVELOPE ON EVERY AXIS OF THIS FRAME. A composite is in the frame only where two things
      // hold at once: the dial has reached for it, AND the two works are anywhere near level. `cw` is
      // that one number, and the travel, the highlight shoulder, the corner shading and the dither
      // all hang on it — so at either end of the dominance travel, as at the dry door, the frame is
      // one work exactly as its file carries it (overlay.js:138-139).
      var level = 4 * dom * (1 - dom);
      var cw = wet * level;
      // Under reduced motion nothing turns, breathes or drifts and the two fields stand still; the
      // frame is the composite the two works make at rest. The pose the shader is handed carries the
      // parked second too, so the fields the shader draws and the layers this script poses cannot
      // stand at two different instants.
      var t = st.reduced ? 0 : num(st.t, 0);
      var turnOff = num(st.turn, 0) * DEG;
      var scale = clamp(num(st.scale, 1), SCALE_MIN, SCALE_MAX);
      var blend = Math.round(clamp(num(st.blend, 0), 0, BLENDS.length - 1));
      var tone = TONE[blend];
      var arrive = num(st.arrival, 0) >= 0.5 ? 1 : 0;
      // THE INTERFERED ARRIVAL (charter shelf 7: «the third picture of a multi-exposure resolves into
      // B»). Named on a score, the lean rides an envelope that keeps growing to the wet end rather
      // than closing at it. Both doors stay exact all the same — at dominance 0 the lean is nothing
      // and at dominance 1 the clamp puts every region at the second work.
      var lean = arrive ? 0.55 * dom : 0.26 * level;
      var pres = unit(presence);
      var read = standsOf(pres);
      // A FIELD IS TURNED INTO ITS WORK'S OWN LATTICE AND SCALED BY THE STEP IT WAS CUT AT. A gain of
      // 1 and an angle of nothing is the module's own field.
      function fld(period, turnDeg, base) {
        var g = (1 / clamp(num(period, 1 / base), PERIOD_MIN, PERIOD_MAX)) / base;
        var a = num(turnDeg, 0) * DEG;
        return [g, Math.cos(a), Math.sin(a), 0];
      }
      return {
        dial: [dom, wet, sw, cw],
        form: [lean, pres, blend, unit(st.mask)],
        // THE FOLD'S OWN RETOUCH (§8's `seams` block), in points of the drawing buffer, carried into
        // the shader so the width the picture is drawn at is the host's own answer and not a number
        // this file chose.
        seam: seamOf(st),
        // bottom layer — slow, one way (overlay.js:143-146)
        layerA: [0.0135 * t * cw,
                 1 + (0.02 + 0.085 * Math.sin(t * 0.0721)) * cw,
                 0.016 * Math.sin(t * 0.0533) * cw,
                 0.014 * Math.cos(t * 0.0411) * cw],
        // top layer — faster, the other way, and the counter-turn turns it further (:149-152)
        layerB: [(-0.0262 * t + turnOff) * cw,
                 (1 + 0.11 * Math.sin(t * 0.0487 + 1.7) * cw) * scale,
                 0.021 * Math.cos(t * 0.0367) * cw,
                 0.019 * Math.sin(t * 0.0295) * cw],
        mixField: fld(st.mixPeriod, st.mixTurn, MIX_BASE),
        regionField: fld(st.regionPeriod, st.regionTurn, REGION_BASE),
        pre: tone.pre, post: tone.post,
        // read on the diagnostic surface, bound to no uniform: what the hand came to
        exposureApplied: exposure, dominance: dom, envelope: cw, blendRule: BLENDS[blend],
        arrive: arrive, topScale: scale, turnDeg: turnOff / DEG,
        presenceApplied: pres, standsWorst: read.worst, deepest: read.deepest,
        reach: read.reach, share: read.share, mask: unit(st.mask),
      };
    }

    // THE REFUSAL, worded the way the host's own manifest refusals read: what is wrong, in this
    // instrument's own measured numbers, on the grid it was measured on.
    function doorWhyNoOf(v, st, grid) {
      var want = st.mix === 0 ? 1 : (st.mix === 1 ? 0 : -1);
      if (want < 0) return null;
      var door = want ? "the entry" : "the exit";
      var work = want ? "departing" : "arriving";
      var where = grid.given
        ? (" of a " + grid.w + " x " + grid.h + (grid.drawn ? " buffer" : " frame")) : "";
      // THE EXPOSURE IS READ FIRST, BECAUSE IT IS THE CAUSE. Short of whole at the exit door the
      // frame is a composite of the two works, and a refusal naming the region would be naming a
      // symptom. At the entry door the envelope is shut whatever the exposure stands at, so this
      // never fires there.
      if (!want && v.exposureApplied < 1) {
        return door + " door leaks: the exposure stands at " + v.exposureApplied.toFixed(6)
             + " of its reach, so the frame is the two works composited by «" + v.blendRule
             + "» and not the " + work + " work, where " + door + " door's own law asks for the "
             + work + " work at every point";
      }
      // THE JUDGES' CHANNEL IS READ BEFORE THE REGION, AND NOT AFTER IT. The region's own reading is
      // the one fault the hold below can close, and a refusal that named it while the channel stood
      // open would send a reader to the region for a fault that is in the channel.
      if (v.mask >= DOOR_SHOW) {
        return door + " door leaks: the judges' own channel stands at " + v.mask.toFixed(6)
             + ", so the frame draws the exposure's own map — where it stands, where the frame "
             + "stands between the two works, and how far the envelope is open" + where
             + " — instead of the " + work + " work, where " + door + " door's own law asks for the "
             + work + " work at every point";
      }
      if (v.standsWorst < 1 - DOOR_SHOW) {
        return door + " door leaks: the exposure stands on " + (v.share * 100).toFixed(1)
             + " per cent of the frame and its thinnest place carries " + v.standsWorst.toFixed(6)
             + " of a whole point" + where + ", so the rest carries nothing at all and whatever "
             + "stands under this layer shows through, where " + door + " door's own law asks for "
             + "the " + work + " work at every point";
      }
      return null;
    }

    // THE NUMBERS OF ONE FRAME, WITH ITS DOOR READ ON THE BUFFER BEING DRAWN. Away from a door this
    // is `posed` and nothing more: the reading is taken nowhere else and no guard moves. At a door it
    // reads its own presence field at that field's deepest possible place and publishes what it read
    // — the share of the frame the exposure stands on, the thinnest point of it, and the field's own
    // deepest place. Where the applied presence stands inside the curve's own dead band of whole, it
    // is held whole with the travel it gave up on the record; beyond that, and for an exposure short
    // of its reach or a judges' channel left open, the refusal stands.
    function values(st) {
      var request = feelPresence(unit(num(st.presence, 1)));
      var v = posed(st, request);
      v.presenceRequest = request;
      v.presenceHeld = null;
      v.doorHeld = null;
      var grid = doorGridOf(st);
      v.doorGrid = (st.mix === 0 || st.mix === 1) ? grid : null;
      var no = doorWhyNoOf(v, st, grid);
      if (!no) { v.doorWhyNo = null; return v; }
      // The hold answers ONE thing: a presence standing inside the curve's own dead band of whole.
      // An exposure short of its reach is a different fault and nothing here can close it — the whole
      // frame is a composite, not a hole in one — so it is refused outright and never held.
      if (request >= 1 - DOOR_HOLD && request < 1) {
        var w = posed(st, 1);
        var wNo = doorWhyNoOf(w, st, grid);
        if (!wNo) {
          w.presenceRequest = request;
          w.presenceHeld = 1 - request;
          w.doorHeld = no;
          w.doorWhyNo = null;
          w.doorGrid = grid;
          return w;
        }
      }
      v.doorWhyNo = no;
      return v;
    }

    var manifest = {
      id: "overlay", api: 1, arity: 2,
      // The first work stands alone, the two lie over each other and turn against each other with a
      // third picture standing where they cross, and the second work is left standing alone.
      roles: ["disassembly", "mystery", "assembly"],
      // WHERE THIS STANDS ON THE CHARTER'S SHELF, and the reading is carried rather than re-decided.
      // lab/data/module-contract.json records this module's level as LIGHT-COLOUR, and the
      // vocabulary table of lab/CROSSING-BRIEF.md carries the same word beside his standing verdict.
      // Nothing here cuts the frame into cells that move, nothing claims a world and nothing touches
      // the grain: what this instrument owns is the light and the colour of the frame, and it is the
      // only instrument the settings record publishes that owns them.
      levels: ["LIGHT-COLOUR"],
      // WHAT THIS INSTRUMENT CUTS ON, ADDED 2026-08-31 (cause A, item 5 — the reconciliation).
      // This file never declared the key; the composer's own `INSTRUMENTS.cuts` carried «band»,
      // «field». `band` stands: this instrument's own fit function (`INSTRUMENT_SUITS.overlay`)
      // reads the two works' colour worlds standing apart, the same reading `PIVOT_SHAPES
      // ["shared-palette-region"]`'s own `colour_world` cut is built on. `field` does not survive
      // the same check — see `pass-composer.js`'s own note on `field` at `KIND_OF_MEASURE`/
      // `KIND_OF_AXIS` above `castForKindsRanked` (cause A, item 3): no measure this file or the
      // composer publishes maps to it, so a kind named here could never be asked for by any ground
      // or travelling candidate, whatever this instrument's own comments elsewhere call the whole-
      // frame construction its `mix` dial walks. Naming a kind nothing can ever ask for is not a
      // preference the die can rank low, the same shape cause A closed everywhere else in this
      // file's own vocabulary; carrying it here would only restate the defect one file over.
      cuts: ["band"],
      // WHERE THIS INSTRUMENT HAS A SEAM (§8's `seams` block, pass-layer.js). One, and it is not a
      // cut of the frame into elements — the `levels` note above says rightly that nothing here cuts
      // the frame into cells, and a seam is a different question: not what elements the frame is
      // divided into, but what boundary a picture drawn this way cannot help but have.
      //   · TILE — the mirrored fold in `mir`/`pane` above. Each layer turns, breathes and drifts
      //     under the envelope, and where that carries a lookup past a work's own edge the picture
      //     mirrors: the module binds its own textures MIRRORED_REPEAT and this host binds every
      //     source clamped, so the wrap is written into the shader as `1 − |mod(q, 2) − 1|`, one
      //     triangle wave per axis. Its derivative flips sign at every fold, which is the same corner
      //     the folding instrument closes at a wedge edge and the floor instrument at a tile's edge —
      //     and this file's own comment already names the construction by the fleet's word for it,
      //     "the same continuation the unfold's parquet runs on". A HAIRLINE and not a handover: the
      //     fold is continuous in value across the edge and only its derivative kinks, so what is
      //     rounded is a fact about the sampling grid rather than about either work. `of` names no
      //     handle, for the reason the host's own block gives — a hairline spends none of an element's
      //     own room, so it does not shrink as an element repeats more often.
      //
      // THE REGION'S OWN EDGE IS NOT A SECOND SEAM, and that is a decision rather than an omission.
      // `EDGE` above is a deliberate, visible softness in the units of the module's own presence
      // field, chosen so the region reads as arriving by growing; it is drawn at that width whatever
      // grid the frame stands on, and it would be a lie to publish it as a boundary the sampling
      // asks for. The region is one field's own level set and nothing repeats round a turn, so
      // neither of the two shapes §8 publishes fits it.
      seams: [{ kind: "tile", of: null, unit: "points of the drawing buffer" }],
      // The module's own declared params, in its own ranges (overlay.js:282-293). Its `pair` handle
      // does not come over: it chose two of the three pictures the module's own test page hands it,
      // and a cue of this engine carries exactly two works, so there is nothing left to choose.
      params: { mix: [0, 1], presence: [0, 1], scale: [SCALE_MIN, SCALE_MAX],
                blend: [0, BLENDS.length - 1], arrival: [0, 1] },
      // WHAT THIS INSTRUMENT SHOWS BESIDES A CROSSING. It is the charter's shelf 10 — two works read
      // as wave fields whose interference is the third picture — so what a person watches is the two
      // works beating against each other, which is a spectacular atypical event rather than a
      // revealing of how either was made.
      register: "spectacle",
      // EVERY handle a score can drive (§4.4b). `mix` is the dial the doors stand on and `clock` is
      // the second the host hands down; `exposure` and `presence` are the module's own two other
      // handles; the four field handles carry the two works' own lattices; `mask` is the judges'
      // channel, resting where the module has no such thing at all.
      //
      // NO HANDLE HERE KEEPS A CLOCK, A POINTER OR A HUNT OF ITS OWN. The module walked its own
      // dominance by a pair of incommensurate sines whenever nobody held its dial, and read the
      // pointer across its mount for dominance and for the top layer's turn (overlay.js:536-545);
      // both are gone. The one place time reaches the picture is the two layers' breath and the two
      // fields' drift, and both read the `clock` handle, so a seeded score repeats to the pixel.
      // LEVEL, PER SHELF 17 (docs/design/PASS-API-V1.md:716). This instrument declares one level,
      // LIGHT-COLOUR, and its own comment above already disclaims the rest: nothing here cuts the
      // frame into cells, claims a world or touches the grain, so the turn, the scale and the two
      // fields' periods are not a lattice of their own — they are how this one light-and-colour
      // effect is built, and every one of them is read at LIGHT-COLOUR rather than at a level this
      // instrument does not occupy. `mix` is the crossing's own dial and `clock` is the module's own
      // time, so neither is a structural level; `mask` is the judges' channel.
      handles: {
        mix: { min: 0, max: 1, def: 0,
               unit: "which of the two works the frame belongs to",
               curve: { family: "a logarithm on each half, mirrored about the middle, k = 1.65",
                        band: CURVE_BANDS.mix, applied: true, measuredOn: CURVE_MEASURED_ON },
               level: null },
        clock: { min: 0, max: 14, def: 0, level: null },
        exposure: { min: 0, max: 1, def: 1,
                    unit: "how far the composite reaches",
                    curve: { family: "an S-curve on each of the dial's two stages, s = 0.65",
                             band: CURVE_BANDS.exposure, applied: true,
                             measuredOn: CURVE_MEASURED_ON },
                    applied: { colourFullAt: 0.5, formsBeginAt: 0.5,
                               doorsExactAt: "whole, which is where this handle rests" },
                    level: "LIGHT-COLOUR" },
        // THE MEASUREMENT THIS HANDLE IS READ AGAINST AT A DOOR. `readAtADoor` says what is read
        // (this instrument's own presence field at that field's deepest possible place), on which
        // grid (the drawing buffer the host binds, with the CSS frame where it hands none), how far
        // the hold reaches (the curve's own dead band of two hundredths) and where the request the
        // score handed in stays on the record.
        presence: { min: 0, max: 1, def: 1,
                    unit: "the share of the frame the exposure stands on",
                    curve: { family: "an S-curve with a dead band of 0.02 at either end, s = 0.91",
                             band: CURVE_BANDS.presence, applied: true,
                             measuredOn: CURVE_MEASURED_ON },
                    applied: { shareStandingAtWhole: 1, edgeOfTheRegion: EDGE, spread: SPREAD,
                               readAtADoor: { band: DOOR_HOLD, readOn: "the drawing buffer",
                                              reads: "presenceRequest",
                                              measures: "this instrument's own presence field at "
                                                      + "that field's deepest possible place" } },
                    level: "LIGHT-COLOUR" },
        blend: { min: 0, max: BLENDS.length - 1, def: 0, kind: "enum", step: 1,
                 unit: "which rule the two works meet under",
                 names: { "0": BLENDS[0], "1": BLENDS[1], "2": BLENDS[2],
                          "3": BLENDS[3], "4": BLENDS[4], "5": BLENDS[5] },
                 reads: "nothing of either photograph: the six rules are his own approved list and "
                      + "the choice between them is a score's, not a measurement's. «light "
                      + "difference» is the one that stands far from both works without inverting "
                      + "colour, and the vista preset of 08-08 11:39 names «screen», which is why "
                      + "screen rests here",
                 level: "LIGHT-COLOUR" },
        scale: { min: SCALE_MIN, max: SCALE_MAX, def: 1,
                 unit: "how large the arriving work stands against the departing one",
                 reads: "the ratio of the two works' own cutting steps — "
                      + "structure.ownDevice.stepPx of the arriving work over the departing one's, "
                      + "with structure.grid.periodPx where no device was derived. Charter shelf 10 "
                      + "is why: the third picture is the two works' interference, and near-matched "
                      + "rhythms are what yield the slow large beats, so the handle that sets how "
                      + "near they stand has to be the two rhythms themselves",
                 level: "LIGHT-COLOUR" },
        turn: { min: 0, max: 180, def: 0, unit: "degrees",
                reads: "the angle between the two works' own lattices — "
                     + "structure.ownDevice.angleDeg of the arriving work less the departing one's, "
                     + "with structure.grid.angleDeg where no device was derived. It is the second "
                     + "half of shelf 10's reading: two lattices at a small angle beat into a "
                     + "moiré, two at a large one do not",
                level: "LIGHT-COLOUR" },
        arrival: { min: 0, max: 1, def: 0, kind: "enum", step: 1,
                   names: { "0": "the whole frame at once", "1": "interfered" },
                   unit: "which named arrival the score put on this exposure",
                   reads: "nothing of either photograph: charter shelf 7 names the interfered "
                        + "arrival and a score names it, so this is a plan's word and not a "
                        + "measurement",
                   level: "LIGHT-COLOUR" },
        mixPeriod: { min: PERIOD_MIN, max: PERIOD_MAX, def: MIX_PERIOD_DEF,
                     unit: "a fraction of the departing work's own frame side",
                     reads: "structure.ownDevice.stepPx over the departing work's own frame side — "
                          + "the step that work was actually cut at, so the field that decides "
                          + "which places of the frame lean to which work leans along the work's "
                          + "own structure; structure.grid.periodPx over the same side where no "
                          + "device was derived",
                     level: "LIGHT-COLOUR" },
        mixTurn: { min: 0, max: 180, def: 0, unit: "degrees",
                   reads: "structure.ownDevice.angleDeg of the departing work, the angle that same "
                        + "step was cut at; structure.grid.angleDeg where no device was derived",
                   level: "LIGHT-COLOUR" },
        regionPeriod: { min: PERIOD_MIN, max: PERIOD_MAX, def: REGION_PERIOD_DEF,
                        unit: "a fraction of the arriving work's own frame side",
                        reads: "structure.ownDevice.stepPx over the ARRIVING work's own frame side "
                             + "— the exposure's region grows along the structure of the work it is "
                             + "resolving into, which is what makes the arrival that work's own; "
                             + "structure.grid.periodPx over the same side where no device was "
                             + "derived",
                        level: "LIGHT-COLOUR" },
        regionTurn: { min: 0, max: 180, def: 0, unit: "degrees",
                      reads: "structure.ownDevice.angleDeg of the arriving work; "
                           + "structure.grid.angleDeg where no device was derived",
                      level: "LIGHT-COLOUR" },
        mask: { min: 0, max: 1, def: 0,
                applied: { readAtADoor: { band: DOOR_SHOW, readOn: "the drawing buffer",
                                          reads: "mask",
                                          measures: "this instrument's own map — where the exposure "
                                                  + "stands, where the frame stands between the two "
                                                  + "works, and how far the envelope is open",
                                          held: null } },
                level: null },
      },
      neutrals: { a: 0, b: 1 },
      doors: { in: { handle: "mix", value: 0, work: "a" },
               out: { handle: "mix", value: 1, work: "b" } },
      // BOTH DOORS FRAME ALIKE, AND BOTH ARE THE PLAIN COVER FIT. Each work is seated into the
      // module's own unit square by its own two sides and the square covers the frame's longer side,
      // so a door is the file cover-fitted with no crop of its own at any frame shape. The module's
      // own line pulled back on a frame taller than wide and drew the file smaller than a cover fit
      // there (lab/data/module-contract.json, this module's `framing` row, in its own words); the
      // port asks the host for the seating instead, which is what makes one record true of every
      // frame rather than of square and wide ones only.
      framings: { "0": { coverCrop: 1 }, "1": { coverCrop: 1 } },
      drivers: ["progress", "cueProgress", "time", "velocity", "capability", "noise", "static",
                "curve", "spline", "map", "add", "multiply", "mix", "clamp", "hold", "segment",
                "ramp", "slew", "oscillate", "node"],
      camera: { needs: "none", authority: "stage" },
      // THE PICTURE'S OWN CHAIN OF SMALLER COPIES, asked for by §8's `gl.readsChain`. The
      // module reads the LAST step of its own chain for the arriving work's flattest level,
      // which is the exact mean of the file; the host builds no chain, so `flatOf` walks a
      // lattice of forty-nine places instead and stands 5.02 of 255 from that mean on average
      // and 14.36 at worst. With the chain uploaded the module's own read is available again.
      gl: { preserveDrawingBuffer: false, readsChain: true },
      // WHAT THIS INSTRUMENT WRITES WHERE ITS OWN MATTER IS ABSENT (§7's coverage law, and the
      // per-instrument specification in docs/design/COVERAGE.md). It is absent wherever `presence`
      // stands below whole: a place is inside the exposure's region or outside it, and outside it
      // nothing at all is written, so whatever stands under this layer shows through untouched. The
      // alpha is the region's own membership and nothing else — never a fade, and never a weight the
      // instrument imposes on the cue beneath it. Under the placement rule this instrument is lawful
      // over another cue and as a whole one-cue score, and unlawful as the lowest cue of a stack.
      coverage: { writes: true,
                  how: "the presence field says how deep each place of the frame lies and presence "
                     + "says how far the region has come; a place inside the region carries the "
                     + "exposure whole and a place outside it carries nothing at all, with the "
                     + "region's own edge of 0.045 of the field the only place between the two. The "
                     + "share standing at presence p is p itself, within three parts in a hundred, "
                     + "whatever second of the clock it is — the field's own depths are pulled flat "
                     + "so that the handle means the share it names. At whole presence every point "
                     + "comes out at 1 and the frame is filled" },
      // The neutral pose is the ENTRY DOOR — `mix` at 0, the value the `doors` block above names —
      // so the frame keys the host reads off it at registration include the door's own record.
      neutralPose: { mix: 0, exposure: 1, presence: 1, blend: 0, scale: 1, turn: 0, arrival: 0,
                     mixPeriod: MIX_PERIOD_DEF, mixTurn: 0,
                     regionPeriod: REGION_PERIOD_DEF, regionTurn: 0, mask: 0,
                     t: 0, reduced: false, cssWidth: 1000, cssHeight: 1000 },
      passes: [{
        program: "overlay", vert: VERT, frag: FRAG, position: "aPos",
        uniforms: [
          { name: "uA", type: "sampler2D", source: "textureA" },
          { name: "uB", type: "sampler2D", source: "textureB" },
          { name: "uScene", type: "sampler2D", source: "sceneTexture" },
          { name: "uSceneAvailable", type: "float", source: "sceneAvailable" },
          { name: "uFitA", type: "vec4", source: "fitA" },
          { name: "uFitB", type: "vec4", source: "fitB" },
          { name: "uRes", type: "vec2", source: "resolution" },
          { name: "uTime", type: "float", source: "seconds" },
          { name: "uDial", type: "vec4", source: "frame:dial" },
          { name: "uForm", type: "vec4", source: "frame:form" },
          { name: "uLayerA", type: "vec4", source: "frame:layerA" },
          { name: "uLayerB", type: "vec4", source: "frame:layerB" },
          { name: "uMixField", type: "vec4", source: "frame:mixField" },
          { name: "uRegionField", type: "vec4", source: "frame:regionField" },
          { name: "uPre", type: "vec4", source: "frame:pre" },
          { name: "uPost", type: "vec4", source: "frame:post" },
          { name: "uSeam", type: "float", source: "frame:seam" },
        ],
      }],
      // The instrument allocates nothing of its own: it spends the two source-texture slots the host
      // already holds and the one programme the host builds from this manifest. The module's own
      // canvas, its context, its two textures with their mipmap chains and its own frame loop are
      // what this port does without.
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
                   programs: 1, passes: 1, bytesEstimate: 2666839, variant: "lean" },
                   standard: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0,
                               programs: 1, passes: 1, bytesEstimate: 10666839,
                               variant: "standard" },
                   rich: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                           passes: 1, bytesEstimate: 42666839, variant: "rich" } },
      capabilities: ["webgl2"],
      decline: ["one work only", "a source that never decoded"],
      provenance: { labPath: "lab/effects/overlay.js", commit: "a24594c",
                    sha256: "0751cc89f5636111c03d12faaca273f80701e545a835b526bb43ac3bd6bcf71c" },
      readiness: "production-ready",
    };

    var live = false;
    return {
      name: "overlay",
      manifest: manifest,
      values: values,
      fit: fit,
      feel: feelMix,
      feelExposure: feelExposure,
      feelPresence: feelPresence,
      prepare: function (o) {
        if (!o.sources) return { take: false, why: "the overlay instrument needs both works" };
        if (!o.cue) return { take: false, why: "no cue names it" };
        return { take: true };
      },
      start: function () { live = true; },
      // The pose the shader draws. The module's canvas, its frame loop, its pointer and its own hunt
      // are gone, so every number here comes from a handle a score drives or from the frame the host
      // is about to bind.
      //
      // A DOOR THIS INSTRUMENT CANNOT KEEP WHOLE IS REFUSED RATHER THAN DRAWN. The door law is the
      // instrument's own claim (the manifest's coverage line above), so the instrument is what
      // answers for it: at either door it reads its own presence field at that field's deepest place
      // on the buffer the host is about to bind and, where the exposure stands short of its reach,
      // where the region leaves part of the frame carrying nothing, or where the judges' channel is
      // left open, it hands the host the reason with the measured numbers in it instead of drawing a
      // door that is not the photograph. The host recovers the transaction on that reason and the
      // walk's own glide carries the visitor, which is the product's own behaviour with no renderer.
      //
      // A ROOF CUE NEVER MEETS THIS. A layer laid over another cue with the region standing on part
      // of the frame is what `presence` is for, and a score that wants that keeps the layer's own
      // dial away from its doors — which is the module's own instruction in its own words: «a score
      // that wants the exposure to arrive walks this down and up itself».
      frame: function (st) {
        if (!live) return;
        var h = st.handles;
        var pose = {
          mix: h.mix, exposure: h.exposure, presence: h.presence, blend: h.blend, scale: h.scale,
          turn: h.turn, arrival: h.arrival, mask: h.mask,
          mixPeriod: h.mixPeriod, mixTurn: h.mixTurn,
          regionPeriod: h.regionPeriod, regionTurn: h.regionTurn,
          // THE SECOND, AND ONLY FROM A HANDLE (§4.4b). The module counted its own frame time up;
          // here the score hands the second down, so a seeded run repeats to the pixel. Under
          // reduced motion it is parked at nothing before it leaves this line, so the fields the
          // shader draws — which read this same number as `seconds` — stand exactly where this
          // script's own layers stand.
          t: st.reduced ? 0 : h.clock, reduced: st.reduced,
          cssWidth: st.viewport.w, cssHeight: st.viewport.h,
          // THE GRID THE SHADER WILL SAMPLE ON, carried into the pose so the door is read on the
          // buffer the host is about to bind as `uRes` rather than on the CSS frame around it. The
          // host settles it from the device ratio and its own resolution step, so it moves while a
          // pass plays and each door is read on the grid standing at that door's own instant.
          bufWidth: st.viewport.bufferW, bufHeight: st.viewport.bufferH,
          // THE FOLD'S OWN RETOUCH, off the host's own `seams` reading (§8's `seams` block). Only
          // the host knows what every instrument declaring a hairline is holding its own edge to, so
          // it answers once and this file carries the number rather than choosing it.
          seam: st.seams,
        };
        // AT A DOOR THE INSTRUMENT SAYS WHAT IT APPLIED, and says it before it refuses. The reading
        // is taken on the buffer this frame is drawn on, so it is the run-time truth his 18:00
        // decision asks for rather than the curve the module carries. `moved` is how far the applied
        // presence had to be walked to whole for this door to be the photograph.
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
              reads: "presence", request: v.presenceRequest, applied: v.presenceApplied,
              moved: v.presenceHeld, unit: "share of the frame",
              // What the exposure itself was doing at this door: how far the dial had reached and
              // how much of a whole point the region's thinnest place carried, so a door held whole
              // says so about the exposure as well as about the region.
              exposure: v.exposureApplied, standsWorst: v.standsWorst,
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
    instrument: overlayInstrument(),
  });
})();
