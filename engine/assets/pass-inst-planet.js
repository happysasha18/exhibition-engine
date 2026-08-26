/*!pass-inst-planet.js*/
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
// OWNERSHIP. This instrument was carried over from lab/effects/planet.js. The artistic instruments
// and their manifests belong to tlvphotos, which builds these files from its own sources; the
// engine's copies are what ships until that handover lands. The contract this file answers to is §7
// and §8 of docs/design/PASS-API-V1.md, and the record that names it is the site's own `pass` block.
(function () {
  var join = window.__@@NS@@PassInstrument;
  if (typeof join !== "function") return;

  // THIS FILE'S OWN VERSION, and the one home of that fact. The build reads this literal out of the
  // source and writes it into the site's record beside the digest, so the version a file declares
  // and the version a host was told to load cannot drift apart without the build noticing.
  var INSTRUMENT_VERSION = "1.0.0";

  // ================================================================================================
  // THE PLANET INSTRUMENT (§8) — lab/effects/planet.js carried across
  // ================================================================================================
  // WHAT THE VISITOR SEES. The departing photograph curls. Its two ends come round to meet each
  // other and close into a small round world: the foot of the frame goes to the centre, so whatever
  // stands up in the picture stands up out of the little world, and the picture's own sky becomes
  // the ring around it — the same sky, smeared and dimmed, lying over the rest of the stage, so the
  // world stands in its own light rather than in a black box. Then the arriving photograph rises
  // out of the world's own centre, where the picture's rows collapse to a point, and floods outward
  // ring by ring until it owns the whole world and the departing one survives only as the light
  // around it. Then the world uncurls, and the arriving photograph stands flat in the frame.
  //
  // THAT SHAPE IS THE CHARTER'S OWN, NOT AN INVENTION. lab/CROSSING-BRIEF.md shelf 8 — ontology
  // shift and projection worlds — names the sphere among its worlds and writes the passage down in
  // four words: «flat → world → flat», with «B enters through the singular locus». The singular
  // locus of this world is its centre, and that is where the arriving work enters. The shelf also
  // says a folded space is at most one per crossing and IS the miracle, which is what the levels
  // block below declares and pays for.
  //
  // ------------------------------------------------------------------------------------------------
  // WHAT CAME OVER, AND WHAT STAYED BEHIND
  // ------------------------------------------------------------------------------------------------
  // WHAT CAME OVER: the whole curl geometry (the strip bent round a circle, its angular sweep, its
  // outer radius and its radial thickness, the framing that pulls back as the ring closes), the
  // cross-dissolve where the two ends meet, the fold past either end, the sky wash with its own
  // reach read off the frame's farthest corner, the radial curve of light, the shading, the
  // horizon's own response curve, the turn's reach, the breath, the dial's own response curve, and
  // the flat door as a blend of the SAMPLE COORDINATE rather than of the finished colour. Every
  // number is carried digit for digit and the suite reads both files for each.
  //
  // WHAT STAYED BEHIND: the module's own canvas and context, its frame loop, its resize observer,
  // its texture uploads, its mipmap chain and its anisotropic filtering (see THE HOST BINDS NO
  // MIPMAPS below), its pointer handling, and its `photo` parameter — a cue of this engine carries
  // an ordered PAIR, so which photographs stand is the host's and not a slider's.
  //
  // WHAT IS NEW, AND IT IS THE WHOLE REASON THIS IS AN INSTRUMENT AND NOT A MODULE. The module
  // curls ONE photograph. A crossing carries two, and the second one arrives here through the
  // world's own centre: THE CUT IS A ROW OF THE PHOTOGRAPH. Below the row the arriving work stands,
  // above it the departing one, and the row travels from under the frame's foot to over its sky. In
  // the flat frame that row is a straight horizontal line; in the world it is a RING, because the
  // world is built by wrapping the picture's rows round a circle. One law, two readings, and the
  // instrument declares the ring as its cut because the ring is what the passage is played on.
  //
  // NO DISSOLVE ANYWHERE, and that is a rule rather than a taste. The charter bans the dead
  // dissolve between two works, and lab/data/module-contract.json's own note on this module says it
  // again from the other side: blending two finished colours makes the middle of a travel the
  // average of its ends, which is a ghost. So the two works meet at a HARD boundary, and what
  // softens it is one pixel's own footprint — the share of this point of the buffer that falls on
  // the arriving side, computed from the module's own analytic derivative of the row coordinate.
  // Coverage over the pixel's footprint, never transparency.
  //
  // ------------------------------------------------------------------------------------------------
  // THE HOST BINDS NO MIPMAPS, AND WHAT THAT COSTS
  // ------------------------------------------------------------------------------------------------
  // The module uploads its own two textures with a mipmap chain and up to four-times anisotropic
  // filtering (planet.js:262-282). The host's two source textures carry neither: they are made with
  // a LINEAR minification filter and no chain at all (pass-layer.js:106-118, :434-445). So under
  // this host `textureGrad` buys no blur where the picture compresses toward the pole, and
  // `textureLod` clamps to level 0, which makes the sky wash read sharp where the module's reads
  // smeared. Both lines belong to the host — a `generateMipmap` on each upload and a minification
  // filter to match — and neither is this instrument's to write. The shader keeps the module's own
  // two calls exactly as the module wrote them, so the day the host hands a chain this picture
  // gains the module's own filtering with no edit here. The suite measures what the missing chain
  // costs and the report carries the number.
  //
  // ------------------------------------------------------------------------------------------------
  // THE COVERAGE: THIS INSTRUMENT FILLS THE FRAME
  // ------------------------------------------------------------------------------------------------
  // §7's coverage law of 12:40 asks every instrument to say where its own matter is absent. Here it
  // is absent nowhere, and the reason is the module's own construction rather than a claim: outside
  // the world's rim the frame is not empty, it carries the departing work's own sky smeared wide
  // and dimmed, and the reach of that wash is READ OFF THE FRAME — the farthest corner of whatever
  // stage the host hands stands at the same place on the wash's own curve (planet.js:323-337). The
  // alpha is the constant 1 at every point of every pose. Under the placement rule (§8 as amended
  // 14:05, and `coverageWhyNo`) that makes this instrument lawful as the LOWEST cue of a stack and
  // as a whole one-cue score.
  function planetInstrument() {
    // The host's own fullscreen triangle, and a vertex shader that does nothing to it.
    //
    // WHY NEITHER SHADER CARRIES A VERSION HEADER, THOUGH THE MODULE'S DOES. The module writes GLSL
    // ES 3.00 and stamps its own header; every instrument of this engine hands the host a
    // first-version source and lets the host's own translator stamp one (pass-layer.js `toES3`,
    // which is mechanical and touches no line of mathematics). Both roads end at the same compiled
    // shader, and the second is the one every other instrument takes — the host's own coverage law
    // is read by finding each shader's output line, and a shader writing to an output of its own
    // naming is a shader that law cannot read. So the header and the name of the output are the
    // host's, and everything between them is the module's. The two filtered fetches this module
    // depends on — `textureGrad` and `textureLod` — are second-version functions and they survive
    // the translation untouched, because what the host compiles is the second version either way.
    var VERT = [
      "attribute vec2 aPos;",
      "void main(){ gl_Position = vec4(aPos, 0.0, 1.0); }",
    ].join("\n");

    // ----------------------------------------------------------------------------------------------
    // THE SHADER. Every line the module wrote is here, in the module's own order, with three
    // changes and no fourth:
    //
    //   · TWO WORKS WHERE THE MODULE HAD ONE. `uTex` becomes `uA` and `uB`, each read at the same
    //     curled coordinate, and `uCut` decides which of the two stands at this point of the frame.
    //   · THE ROW COORDINATE IS TURNED OVER ONCE. The module uploads its texture flipped
    //     (planet.js:266) and the host uploads unflipped (pass-layer.js:157), so `uv()` turns the
    //     row over here and nowhere else.
    //   · THE CARRIERS. The host binds four uniform types and no more — sampler2D, float, vec2,
    //     vec4 (pass-layer.js's own `UTYPE`) — so the module's fourteen scalars travel packed four
    //     to a carrier. Not one number changes; `uBg` becomes the constant DARK, because it never
    //     was a parameter.
    // ----------------------------------------------------------------------------------------------
    var FRAG = [
      "precision highp float;",
      "uniform sampler2D uA;",             // the work the visitor is leaving
      "uniform sampler2D uB;",             // the work arriving
      "uniform vec2  uRes;",
      // THE WORLD'S OWN GEOMETRY: the angular sweep of the strip, the radius of its outer (sky)
      // edge, its radial thickness, and the shape-space y of the bounding box's centre.
      "uniform vec4  uGeom;",              // Phi, R, D, Ycb
      // THE STAGE: pixels per shape unit, the spin added to the column coordinate, the horizon's
      // own gamma, and whether the world is turned inside out into a corridor.
      "uniform vec4  uCam;",               // S, spin, gamma, flip
      // THE WEDGE still open between the two ends: how wide it is in picture widths, the narrowest
      // cross-dissolve so a shut ring has no cut either, how solidly the picture carries across it,
      // and how far the sky wash reaches past the rim in shape units.
      "uniform vec4  uWedge;",             // gapW, seam, far, atm
      "uniform vec2  uCrop;",              // the rows of the photograph used: x at the centre, y at the rim
      "uniform float uWorld;",             // the crossing dial: 0 the flat photograph, 1 the world
      // THE FLAT DOOR'S OWN SCALE, in picture units per device pixel, one number per axis and one
      // pair per work. Handed in already cover-fitted to the frame the host gave this pass, so the
      // shader carries no frame-shape reasoning of its own and the door holds at any shape.
      "uniform vec4  uFlatPP;",            // A.x, A.y, B.x, B.y
      // THE CUT — the row of the photograph the two works change over at, the footprint that row
      // travels inside one point of the buffer, and the row the sky wash is read at.
      "uniform vec4  uCut;",               // tau, footprint, skyRow, unused
      "uniform float uShade;",             // the world's own finish, a judge channel resting at 1
      "uniform float uMask;",              // the judges' channel: the cut map as colour
      // WHAT THE WORLD STANDS AGAINST at the very outside of the wash. The module's own three
      // numbers (planet.js:558); it was never a parameter, so it travels as a constant.
      "const vec3 DARK = vec3(0.031, 0.031, 0.036);",
      "",
      // THE ROW COORDINATE, TURNED OVER ONCE. The module's own line is
      // `vec2(s, mix(uCrop.x, uCrop.y, v))` over a texture it uploaded flipped; the host uploads
      // unflipped, so the row is turned over here and the picture stands the right way up.
      "vec2 uv(float s, float v){ return vec2(s, 1.0 - mix(uCrop.x, uCrop.y, v)); }",
      // past either end the picture folds back on itself instead of freezing its last column:
      // the fold is continuous, so nothing streaks and no line runs out of the join
      "float fold(float x){ x = mod(abs(x), 2.0); return x > 1.0 ? 2.0 - x : x; }",
      "",
      "void main(){",
      "  float uPhi = uGeom.x, uR = uGeom.y, uD = uGeom.z, uYcb = uGeom.w;",
      "  float uS = uCam.x, uSpin = uCam.y, uGamma = uCam.z, uFlip = uCam.w;",
      "  float uGapW = uWedge.x, uSeam = uWedge.y, uFar = uWedge.z, uAtm = uWedge.w;",
      "  vec2 P = gl_FragCoord.xy - 0.5 * uRes;",
      "  vec2 d = vec2(P.x / uS, P.y / uS + uYcb);",
      "  float r = max(length(d), 1e-6);",
      "  float a = atan(d.x, d.y) + uSpin;",                        // spin turns the world itself
      "  a -= 6.28318531 * floor((a + 3.14159265) / 6.28318531);",  // back into (-PI, PI]
      "  float sw = a / uPhi + 0.5;",
      "  float tr = (uR - r) / uD;",             // 0 at the sky edge, 1 at the ground edge
      "",
      "  float t  = clamp(tr, 0.0, 1.0);",
      "  float tg = pow(max(t, 1e-4), uGamma);",
      "  float v  = mix(1.0 - tg, tg, uFlip);",  // picture row: 0 = foot of the frame, 1 = sky
      "",
      // The two ends. q walks the circle from the right end (q = 0) round the open wedge to
      // the left end (q = uGapW); inside the picture it runs negative or past the wedge. Both
      // ends are sampled for every pixel and cross-dissolved, which leaves no cut anywhere: a
      // shut ring blends over uSeam, an open one over the wedge.
      "  float g = uGapW;",
      "  float e = max(0.0, 0.5 * (uSeam - g));",
      "  float q = (sw >= 0.5) ? (sw - 1.0) : (sw + g);",
      "  float u = clamp((q + e) / (g + 2.0 * e), 0.0, 1.0);",
      "  float uu = u * u * (3.0 - 2.0 * u);",
      "  float sA = fold(1.0 + q);",              // reading forward off the right end
      "  float sB = fold(q - g);",                // reading back off the left end
      "  float lin = max(0.0, min(q, g - q));",   // how deep into the open wedge this pixel is
      "",
      // THE CROSSING DIAL. uWorld picks WHICH POINT of the photograph a pixel reads, never which of
      // two already-rendered colours to show: uvFlat is the plain, independent cover-fit point every
      // straight photograph uses, uv(sA/sB, v) is the curled point the world geometry above already
      // computed, and uWorld walks the SAMPLE COORDINATE between them — so the frame is always one
      // picture in sharp focus, never two renderings of it laid over each other. The curl geometry
      // itself is never pushed toward zero to reach the flat door; the coordinate mix alone carries
      // the walk to flat.
      "  vec2 uvFlatA = clamp(vec2(0.5 + P.x * uFlatPP.x, 0.5 - P.y * uFlatPP.y), 0.0, 1.0);",
      "  vec2 uvFlatB = clamp(vec2(0.5 + P.x * uFlatPP.z, 0.5 - P.y * uFlatPP.w), 0.0, 1.0);",
      "",
      // analytic derivatives: automatic ones break across the atan seam. The flat door reads a
      // plain, constant screen-to-picture scale (no seam at all), and its own gradient travels
      // on the same uWorld the coordinate above is mixed on.
      "  float blur = 1.0 + 14.0 * smoothstep(0.0, 0.12, lin);",
      "  float k  = blur / (uPhi * uS * r * r);",
      "  vec2  gs = vec2(k * d.y, -k * d.x);",
      "  float gv = uGamma * pow(max(t, 2e-3), uGamma - 1.0) * abs(uCrop.y - uCrop.x) / (uD * uS);",
      "  vec2  gvv = gv * d / r;",
      "  vec2  gxA = mix(vec2(uFlatPP.x, 0.0), vec2(gs.x, gvv.x), uWorld);",
      "  vec2  gyA = mix(vec2(0.0, uFlatPP.y), vec2(gs.y, gvv.y), uWorld);",
      "  vec2  gxB = mix(vec2(uFlatPP.z, 0.0), vec2(gs.x, gvv.x), uWorld);",
      "  vec2  gyB = mix(vec2(0.0, uFlatPP.w), vec2(gs.y, gvv.y), uWorld);",
      "  vec2  cur0 = uv(sA, v), cur1 = uv(sB, v);",
      "  vec3 colA = mix(textureGrad(uA, mix(uvFlatA, cur0, uWorld), gxA, gyA).rgb,",
      "                  textureGrad(uA, mix(uvFlatA, cur1, uWorld), gxA, gyA).rgb, uu);",
      "  vec3 colB = mix(textureGrad(uB, mix(uvFlatB, cur0, uWorld), gxB, gyB).rgb,",
      "                  textureGrad(uB, mix(uvFlatB, cur1, uWorld), gxB, gyB).rgb, uu);",
      "",
      // THE CUT, AND IT IS ONE ROW OF THE PHOTOGRAPH. Below the row the arriving work stands, above
      // it the departing one. The row is mixed on the very uWorld the sample coordinate is mixed
      // on: in the world it is the picture's own row, which is a RING because the world is the
      // picture's rows wrapped round a circle, and at the flat door it is the frame's own height,
      // which at a cover fit is a row of the picture the visitor can see — one law, two readings.
      // What softens it is one point of the buffer's own footprint and nothing else — the module's
      // own analytic derivative of the row coordinate where the world stands, the buffer's own
      // point where it does not. Coverage over a pixel's footprint, never transparency.
      "  float rowW = mix(uCrop.x, uCrop.y, v);",
      "  float rowFlat = clamp(0.5 + P.y / max(uRes.y, 1.0), 0.0, 1.0);",
      "  float row = mix(rowFlat, rowW, uWorld);",
      "  float foot = max(mix(uCut.y, gv, uWorld), 1e-6);",
      "  float cov = clamp(0.5 + (uCut.x - row) / foot, 0.0, 1.0);",
      "  vec3 pic = mix(colA, colB, cov);",
      "",
      // the sky of these same photographs, smeared wide, is what lies outside the world.
      // both ends are fetched here too: blending the column instead would draw a line
      "  float outward = clamp((r - uR) / uAtm, 0.0, 1.0);",
      "  float lod = mix(3.0, 7.0, outward);",
      "  float vSky = mix(0.93, 0.07, uFlip);",
      "  vec3 skyA = mix(textureLod(uA, uv(sA, vSky), lod).rgb,",
      "                  textureLod(uA, uv(sB, vSky), lod).rgb, uu);",
      "  vec3 skyB = mix(textureLod(uB, uv(sA, vSky), lod).rgb,",
      "                  textureLod(uB, uv(sB, vSky), lod).rgb, uu);",
      // the wash belongs to whichever work owns the row it is read at, so the departing work's own
      // light is the last of it to go
      "  float covSky = clamp(0.5 + (uCut.x - uCut.z) / foot, 0.0, 1.0);",
      "  vec3 sky = mix(skyA, skyB, covSky);",
      "",
      // one radial curve of light: brightest a third of the way out, falling to the rim and
      // on into the wash, so the edge of the world never burns to a white ring
      "  float rn = min(r / uR, 1.0);",
      // this whole finish belongs to the world alone — none of it stands at the flat door — so
      // shade, lit and the coverage below are each gated to their own identity by uWorld, and the
      // judges may take the finish out on uShade without touching the geometry
      "  float fin = uWorld * uShade;",
      "  float shade = mix(1.0, mix(1.10, 0.74, smoothstep(0.18, 1.0, rn)), fin);",
      // one light, fixed to the stage rather than to the world, so the round thing reads round
      "  float lit = mix(1.0, 1.0 + 0.13 * dot(d / r * min(r / uR, 1.15), vec2(-0.6, 0.8)), fin);",
      // turned inside out it is the foot of the frame that lies along the rim, and its bright
      // haze would flare in the wash, so the wash is held back there
      "  float dimOut = 0.74 * mix(1.0, 0.72, uFlip) * exp(-3.2 * outward);",
      "  float inward = clamp((uR - r) / (0.9 * uR), 0.0, 1.0);",
      "  float dimIn  = 0.74 - 0.42 * smoothstep(0.0, 1.0, inward);",
      "  float dimB   = (r >= uR) ? dimOut : dimIn;",
      // only the far outside settles to the page; inside the open roll the sky stays,
      // dim, so a half-curled picture is not sitting on a black hole
      "  vec3 back = mix(sky * dimB, DARK, smoothstep(0.5, 1.0, outward));",
      "",
      // where the picture itself shows: not past the rim, not in the open middle of the roll,
      // and only as far round the wedge as the curl has earned
      "  float rim  = 1.0 - smoothstep(0.0, 0.022, outward);",
      "  float hole = smoothstep(0.0, 1.5 / (uD * uS), 1.0 - tr);",
      // the wider the wedge, the longer the ends have to dissolve into the sky behind them
      "  float bell = smoothstep(0.0, clamp(0.35 * g, 0.05, 0.16), lin);",
      "  float aStrip = mix(1.0, uFar, bell);",
      // coverage: at uWorld 0 the picture fills the whole frame (covered 1, back never shows);
      // at uWorld 1 this is the world's own rim/hole/wedge coverage, exactly as always shipped
      "  float covered = mix(1.0, rim * hole * aStrip, uWorld);",
      "  pic *= mix(1.0, mix(1.0, 0.88, bell * smoothstep(0.015, 0.10, g)), uWorld);",
      "",
      // the very centre is where the sampling collapses: let it sit back a little
      "  pic *= mix(1.0, mix(0.90, 1.0, smoothstep(0.0, 0.025, r / uR)), fin);",
      "",
      "  vec3 col = mix(back, pic * shade, covered) * lit;",
      // these skies are pale and flat; a touch of curve gives the world some body — gone at the
      // flat door along with the rest of the finish
      "  col = pow(max(col, 0.0), vec3(mix(1.0, 1.12, fin)));",
      // THE CUT MAP, the judges' own frame, and it answers the three questions a row asks of this
      // instrument. RED: which work stands at this point — the departing one at half, the arriving
      // one at full. GREEN: whether the picture itself stands here or the sky wash does. BLUE: how
      // much of the page's own colour stands here, which is the one reading that could ever say
      // this instrument's matter is absent — it is what the coverage declaration is measured by
      // rather than argued from.
      "  vec3 judge = vec3(mix(0.5, 1.0, cov), covered,",
      "                    (1.0 - covered) * smoothstep(0.5, 1.0, outward));",
      "  col = mix(col, judge, uMask);",
      // THE COVERAGE: the alpha is the constant 1, and it is a decision rather than a default. The
      // frame is filled at every point by the world and its own sky, so this instrument has no
      // absence to publish and stands as the ground a stack is laid on.
      //
      // AND THE FRAME'S FINAL COLOUR IS CALLED `col` BECAUSE THIS LINE IS READ. The host's own
      // coverage law is checked by finding each instrument's output line and reading the alpha it
      // writes (tests/test_pass_coverage.py, tests/test_pass_stack.py), and the whole fleet writes
      // it as `vec4(col, 1.0)`. So the module's own two names are turned about here — its `col`,
      // the picture before its finish, is `pic`, and its `res`, the finished frame, is `col` — and
      // nothing else about either is touched.
      "  gl_FragColor = vec4(col, 1.0);",
      "}",
    ].join("\n");

    function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
    function clamp01(v) { return clamp(v, 0, 1); }
    function smoothstep(a, b, x) {
      var t = clamp((x - a) / (b - a), 0, 1);
      return t * t * (3 - 2 * t);
    }
    function num(v, d) { var n = +v; return n === n ? n : d; }

    var TAU = 2 * Math.PI;

    /* THE NARROWEST CROSS-DISSOLVE where the two ends of the curled strip meet, so a shut ring has
       no cut down it either. planet.js:554 carried this digit for digit as 0.14 when this port was
       first written, and that is still the fallback below where no host has answered yet.

       IT NOW TRAVELS ON THE HOST'S OWN SEAM (§8's `seams` block, pass-layer.js), and moving it there
       changed the number. The 0.14 was the module's own typed literal, fixed regardless of how the
       strip is bent or how big the buffer is; the host answers instead with a HANDOVER ZONE's own
       share — one part in eight of the one wrap this strip makes, which is 0.125 — the same shape
       tunnel's own ring-join now rounds its edge with, so a wrap glued to itself in one file and a
       ring handed to the next in another read one argument instead of two typed numbers that happen
       to be close. The difference between 0.14 and 0.125 is inside the crossing's own seam
       threshold, which is what the two-roads row below still measures against the module untouched.
    */
    var SEAM = 0.14;

    /* HOW FAR THE SKY WASH REACHES, AT ANY FRAME SHAPE (planet.js:323-337). The wash is what keeps
       the world standing in its own light instead of in a black box, and its reach is READ OFF THE
       FRAME ITSELF: the farthest corner of the stage stands at the same place on the wash's own
       curve whatever shape the stage is. The constant is derived rather than chosen — on the
       module's own 4:3 stage with the ring shut the corner sits at 1.792 R, which is 0.792 R past
       the rim against the old cap of 1.25 R, and 0.792/1.25 = 0.634 — so feeding it back on a 4:3
       frame returns exactly the module's own number. */
    var ATM_REACH = 0.634;

    /* THE TURN'S OWN REACH and THE HORIZON'S, both read off the pointer lines they replace
       (planet.js:320-321): the hand reached (pointer.x - 0.5) * 2.2 across, so half of 2.2 either
       way, and look.gamma * (1.5 - pointer.y) up and down, so half a gamma either way. */
    var TURN_REACH = 1.1;
    var HORIZON_REACH = 0.5;

    /* THE RESPONSE CURVE OF THE DIAL (DARKROOM-DRAFT D2, his word 08-08 17:57, planet.js:383-399):
       equal movements of the hand produce equal felt change across the whole travel. Measured by
       walking the raw dial in steps of 0.02 and reading the mean channel distance between
       neighbouring frames — the flat photograph curls into a world fast at the start and slowly at
       the end, 76.1 channels in the first tenth against 24.9 in the last, a spread of 3.1. The
       family is logarithmic because curling is felt in RATIOS of the sphere's radius; a and b are
       fixed by the two doors and k = 1.45 is the one fitted number. */
    var FEEL_K = 1.45;

    /* THE HORIZON'S OWN CURVE (planet.js:340-366): a two-piece logarithm hinged AT THE MIDDLE,
       because the middle of that handle is a DOOR — it is where the module stands on its own, and a
       curve that moved it would move the module's own picture. */
    var FEEL_H_C = 0.5, FEEL_H_K1 = 0.85, FEEL_H_K2 = 0.65;

    /* THE MODULE'S OWN THREE PHOTOGRAPHS AND WHAT IT DID WITH THEM (planet.js:28-37). This table is
       the closest thing this module has to a measurement of a work, and it is what the crop and the
       horizon are derived from below rather than being typed as constants:

         tower       fills the frame already   crop to 0.98 of the rows, gamma 0.76
         dark tower  a low dark crown          crop to 0.72,             gamma 0.50
         two towers  two small spikes          crop to 0.62,             gamma 0.36

       and the module's own sentence for why: «the building fills two thirds of the first frame and
       a fifth of the last, so the last two are taken with less sky above them and bent harder, or
       the towers come out as specks in a cloud». So the reading the table stands on is HOW MUCH OF
       THE FRAME THE FIGURE HOLDS, which every work of this collection carries as a measurement of
       its own. The two named shares are the two ends. */
    var FIG_LO = 0.20, FIG_HI = 0.667;
    var CROP_LO = 0.62, CROP_HI = 0.98;
    var GAMMA_LO = 0.36, GAMMA_HI = 0.76;
    var CROP_FOOT = 0.0;      // every row of the module's own table starts at the foot of the frame

    /* ---- THE PORT'S OWN NUMBERS, and there are three ---------------------------------------------

       WHERE THE ARRIVING WORK RISES. The world opens and shuts on one sine over the pass, and the
       arriving work comes out of the centre through the MIDDLE HALF of it — so the first quarter is
       the departing work curling into a world, the middle half is the handover, and the last
       quarter is the world uncurling into the arriving work. The two numbers are not chosen here:
       they are the walk's own three phases, whose default in the client's register is
       [0.25, 0.5, 0.25] (engine/client/01a-pass.js, `phaseWindows`), and the charter's own reading
       of a passage — whole works stand only at the start and the end, the middle lives in
       fragments. */
    var POLE_FROM = 0.25, POLE_TO = 0.75;

    /* HOW FAR PAST EITHER END OF THE PICTURE'S ROWS THE CUT TRAVELS. A cut standing exactly on the
       last row would leave that row half blended at a door, which is a half-lit line across the top
       or the bottom of the photograph. So the row runs from a little under the foot to a little
       over the sky, and this is that little: two hundredths of the picture's height, which is
       sixteen points of a 844-point frame and comfortably more than the widest footprint one point
       of the buffer ever spans. */
    var CUT_ROOM = 0.02;

    /* THE FLOOR THAT STOOD HERE IS GONE (2026-08-18, at the merge). `WORLD_FLOOR = 0.20` was how
       strongly a work had to read as one of the two worlds this instrument draws before the
       crossing was «worth playing on it», and its own comment said where it came from: the
       collection's radial floor, borrowed because the polar readings carry no published floor of
       their own. The collection's ten floors were struck from the composer the same morning under
       his word of 09:51 — a quartile of some collection says how a reading stands among other
       photographs when what is asked is how these two stand to each other — so the borrowed number
       has nothing left to be borrowed from, and a number nobody measured goes with it (08:47).

       Nothing about the reading is lost. Every clause the ask made is a ranking in the composer's
       own `INSTRUMENT_SUITS.planet`, which is where both work records are in hand: the world
       reading itself, times the share of that reading which is NOT the log-spiral's, halved where
       no horizon was measured. A pair with no world ranks the curl below its rivals and still
       crosses. */

    function feel(u) {
      return (Math.exp(FEEL_K * u) - 1) / (Math.exp(FEEL_K) - 1);
    }
    function feelLog(x, k) {
      return Math.abs(k) < 1e-6 ? x : (Math.exp(k * x) - 1) / (Math.exp(k) - 1);
    }
    function feelHorizon(u) {
      return u <= 0.5 ? FEEL_H_C * feelLog(2 * u, FEEL_H_K1)
                      : FEEL_H_C + (1 - FEEL_H_C) * feelLog(2 * u - 1, FEEL_H_K2);
    }

    // ---- WHAT THE FIGURE'S OWN SHARE OF THE FRAME DECIDES -------------------------------------------
    // The module's table read straight: a work whose figure fills the frame keeps nearly all its
    // rows and is bent gently; one whose figure is a spike in a wide sky is taken with the sky cut
    // away and bent harder, or it comes out as a speck in a cloud. Both lines are the same two
    // points of the module's own table, and the table's THIRD row is the check: it stands at a crop
    // of 0.72 and a gamma of 0.50, which these two lines place at a figure share of 0.329 and 0.363
    // — one photograph, two independent readings, agreeing to 0.034.
    function cropTopOf(figShare) {
      var f = clamp(num(figShare, FIG_HI), FIG_LO, FIG_HI);
      return CROP_LO + (CROP_HI - CROP_LO) * (f - FIG_LO) / (FIG_HI - FIG_LO);
    }
    function gammaOf(figShare) {
      var f = clamp(num(figShare, FIG_HI), FIG_LO, FIG_HI);
      return GAMMA_LO + (GAMMA_HI - GAMMA_LO) * (f - FIG_LO) / (FIG_HI - FIG_LO);
    }

    // ---- the grid one frame is drawn on ------------------------------------------------------------
    // The buffer the host is about to bind as `resolution`, with the CSS frame where it hands none
    // and a square where it hands neither. `drawn` says which of the two the reading below names,
    // since a reader told «a 780 x 1688 frame» would look for a device that has none.
    function gridOf(st) {
      var bw = Math.round(num(st.bufWidth, 0)), bh = Math.round(num(st.bufHeight, 0));
      if (bw >= 1 && bh >= 1) return { w: bw, h: bh, drawn: true, given: true };
      var cw = Math.round(num(st.cssWidth, 0)), ch = Math.round(num(st.cssHeight, 0));
      if (cw >= 1 && ch >= 1) return { w: cw, h: ch, drawn: false, given: true };
      return { w: 1, h: 1, drawn: false, given: false };
    }

    // Cover-fit a work into the frame, and nothing beyond it. The doors of this instrument stand
    // the photograph cover-fitted and cropped by nothing at all, which is what
    // lab/data/module-contract.json publishes for both of them (`framing.coverCrop` 1.0), so the
    // seating a work asks for IS the plain cover fit and the `framings` block says so.
    function fit(iw, ih, w, h) {
      var fa = w / Math.max(h, 1);
      var ia = iw / Math.max(ih, 1);
      if (ia > fa) return [fa / ia, 1, 0, 0];
      return [1, ia / fa, 0, 0];
    }

    // A WORK'S OWN SHAPE, READ BACK OUT OF THE SEATING THE HOST HANDED. The host asks this file's
    // own `fit` for each work's cover fit on this buffer and publishes both on the frame state
    // (pass-layer.js:2031). The curl geometry needs the picture's own proportions — the module took
    // them straight off the image it uploaded — and this is where they come from here: the same two
    // numbers, read back through the fit that produced them, so the shape the geometry is built on
    // and the seating the shader samples through cannot disagree.
    // A bench hands the two files' own sizes instead, and where it does they are read straight:
    // one road into this number rather than two, whichever the caller has.
    function aspectOf(f, frameAspect, iw, ih) {
      var w = num(iw, 0), h = num(ih, 0);
      if (w > 0 && h > 0) return h / w;
      if (!f || f.length < 2) return 1;
      var sx = num(f[0], 1), sy = num(f[1], 1);
      var ia = sx < 1 ? frameAspect / Math.max(sx, 1e-6) : Math.max(sy, 1e-6) * frameAspect;
      // the module's own `aspect` is height over width
      return 1 / Math.max(ia, 1e-6);
    }

    // ---- THE PASSAGE'S OWN SHAPE ------------------------------------------------------------------
    // One dial carries the whole crossing, and both doors are exact by construction rather than by a
    // tolerance: the world opens and shuts on a sine that is exactly nothing at each end of the
    // pass, and the cut stands past the picture's own rows at both.
    function windowOf(dial) { return Math.sin(Math.PI * clamp01(dial)); }
    function worldOf(dial) { return feel(windowOf(dial)); }
    function cutRowOf(dial) {
      var s = smoothstep(POLE_FROM, POLE_TO, clamp01(dial));
      return -CUT_ROOM + (1 + 2 * CUT_ROOM) * s;
    }

    // ONE TRAVELLING NUMBER, read on the diagnostic surface: how far the passage has come. The
    // entry, the handover and the arrival are the shape of its response.
    function feelOf(dial) { return clamp01(dial); }

    // ---- the numbers of one frame ------------------------------------------------------------------
    // Everything the shader gets is a pure function of the pose; every number in the pose comes from
    // a handle a score can drive. NOTHING HERE READS A CLOCK: the module counted its own second up
    // in its own frame loop and the score's own second arrives on the `clock` handle instead, so a
    // driven walk repeats to the pixel.
    function posed(st) {
      var dial = clamp01(num(st.mix, 0));
      var grid = gridOf(st);
      var frameAspect = grid.w / Math.max(grid.h, 1);
      var iaA = aspectOf(st.fitA, frameAspect, st.aw, st.ah);
      var iaB = aspectOf(st.fitB, frameAspect, st.bw, st.bh);
      var W = grid.w, H = grid.h;

      var world = worldOf(dial);
      var tau = cutRowOf(dial);

      // THE BREATH, on the score's own second (planet.js:462-464). The module counted this on its
      // own frame loop; here the handle carries it, so two runs of one score draw one picture. The
      // world stays shut; the breath only lets the join open by a few degrees.
      var clock = num(st.clock, 0);
      var breath = st.reduced ? 0
        : 0.055 * (0.62 * Math.sin(clock * 0.115) + 0.38 * Math.sin(clock * 0.079));

      // HOW FAR THE STRIP IS BENT. The slider is eased: the first half is the bend, the second half
      // closes the ring (planet.js:466).
      var curlBase = clamp01(num(st.curl, 0.82));
      var c = clamp(1 - Math.pow(1 - clamp01(curlBase + breath), 2.4), 0.006, 1);

      // WHICH OF THE TWO WORLDS. At the floor and below the picture closes into a sphere; over it,
      // the same geometry turned inside out is a corridor, which is what the module's own `flip`
      // draws. The handle carries the departing work's own corridor reading, so the choice is the
      // work's rather than a taste.
      var flip = num(st.depth, 0) >= 0.5 ? 1 : 0;

      // THE FIGURE'S OWN SHARE OF THE FRAME decides how many rows are used and how hard the horizon
      // is pulled in — the module's own table, read as the line it is.
      var figure = clamp01(num(st.gather, FIG_HI));
      var cropTop = cropTopOf(figure);
      var gammaBase = gammaOf(figure);

      // THE HORIZON, moved about the work's own place by the handle, on the module's own two-piece
      // curve; and the turn, which is linear by measurement because equal angles of turn move the
      // same picture past the same eye.
      var horizon = feelHorizon(clamp01(num(st.dip, 0.5)));
      var gamma = gammaBase * (1 + (horizon - 0.5) * 2 * HORIZON_REACH);
      var spin = (clamp01(num(st.turn, 0.5)) - 0.5) * 2 * TURN_REACH;

      // THE WORLD'S SHAPE FOLLOWS THE WORK THAT OWNS IT: it is built on the departing work's own
      // proportions while that work holds the world and on the arriving work's once it has taken
      // it, travelling with the very row the two change over at.
      var ia = iaA + (iaB - iaA) * clamp01(tau);
      var asp = ia * (cropTop - CROP_FOOT);      // the strip is what is used
      var p = TAU * asp;
      var Phi = TAU * c;
      var R = 1 / Phi;
      // the hole in the middle of the roll shuts well before the ends meet: no dark dot left
      var D = R * Math.min(1, (1 - Math.pow(1 - c, p)) * (1 + 0.35 * c));
      var r0 = R - D;
      // Frame the strip itself while it is still a bowed band; as the ring closes, pull back
      // smoothly until the whole round world is in view.
      var cmin = Math.cos(Phi / 2);
      var ymax = R;
      var ymin = cmin >= 0 ? Math.max(r0 * cmin, r0) : R * cmin;
      var k = smoothstep(0.45, 0.78, c);
      var ycb = (1 - k) * (ymax + ymin) / 2;
      var hw = (Phi >= Math.PI) ? R : R * Math.sin(Phi / 2);
      var hh = (1 - k) * (ymax - ymin) / 2 + k * R;
      // the disc is given nearly the whole short side; the sky wash takes the rest,
      // so nothing is clipped and nothing is left over as black
      var S = Math.min(W / (2 * hw), H / (2 * hh)) * 0.93;

      // spin is counted in turns of the picture, so it feels the same at any curl. The world also
      // turns slowly on its own, at the module's own rate of 0.052 turns a second, and here that
      // rate rides the score's second rather than a clock of the instrument's own — so a driven
      // walk repeats to the pixel and the world is still alive while it stands.
      var totalSpin = ((clock * 0.052 + spin) / TAU) * Phi;
      var gapW = 1 / c - 1;                          // wedge left open, in picture widths
      var far = smoothstep(0.62, 0.99, c);           // and how solidly it is carried across
      // the farthest point of THIS frame from the world's own centre, in shape units, and the wash
      // stretched to put it at ATM_REACH on its curve. The old pair of numbers stays as the floor,
      // so a half-rolled strip — whose sky edge can stand outside the frame entirely — keeps the
      // reach it always had.
      var farX = W / (2 * S), farY = H / (2 * S) + Math.abs(ycb);
      var rFar = Math.sqrt(farX * farX + farY * farY);
      var atm = Math.max(Math.min(1.25 * R, 0.55 * Math.max(W, H) / S), (rFar - R) / ATM_REACH);

      // THE FLAT DOOR AT ANY FRAME SHAPE. The door owes the work itself, cover-fitted, in whatever
      // frame the host hands: kCover is the width the WHOLE file would be drawn at, taken as the
      // LARGER of what each axis demands, so the file covers the frame on both axes and the frame's
      // own shape decides which axis is cropped. The clamp in the shader is a guard, not a fit.
      var kA = Math.max(W, H / Math.max(iaA, 1e-6));
      var kB = Math.max(W, H / Math.max(iaB, 1e-6));
      var flatPP = [1 / kA, 1 / (kA * iaA), 1 / kB, 1 / (kB * iaB)];

      // THE CUT'S OWN FOOTPRINT AT THE FLAT DOOR — how much of the frame's own height one point of
      // the buffer spans, which is what makes the boundary a hard edge softened by exactly one
      // point and never a fade. Where the world stands, the shader mixes this toward the module's
      // own analytic derivative of the row coordinate at that very pixel, so the softening is one
      // point of the buffer wherever the cut happens to fall.
      var footFlat = 1 / Math.max(H, 1);
      var skyRow = CROP_FOOT + (cropTop - CROP_FOOT) * (flip ? 0.07 : 0.93);
      // THE WRAP'S OWN SEAM, off the host's own `seams` reading; SEAM is only where this file falls
      // back before any host has answered.
      var seam = num(st.seam && st.seam.ring, SEAM);

      return {
        geom: [Phi, R, D, ycb],
        cam: [S, totalSpin, gamma, flip],
        wedge: [gapW, seam, far, atm],
        crop: [CROP_FOOT, cropTop],
        world: world,
        flatPP: flatPP,
        cut: [tau, footFlat, skyRow, 0],
        // read on the diagnostic surface, bound to no uniform
        hand: dial, window: windowOf(dial), curl: c, breath: breath,
        cutRow: tau, cutFoot: footFlat, skyRow: skyRow,
        turnDeg: (spin / TAU) * 360, gamma: gamma, gammaBase: gammaBase,
        figure: figure, cropTop: cropTop, shape: flip ? "a corridor" : "a sphere",
        aspects: [iaA, iaB, ia],
        shade: clamp01(num(st.shade, 1)), mask: clamp01(num(st.mask, 0)),
        grid: grid,
      };
    }

    // ---- THE DOOR THE INSTRUMENT READS FOR ITSELF --------------------------------------------------
    // His 18:00 architecture decision, carried in the U27 brief: the instrument reads its doors at
    // runtime on the actual buffer, and the report it hands back is the runtime truth; what the
    // manifest declares is only the claim. The meshing instrument answered that first, the unfold
    // reads its own panel map and the box walks its own two faces; this is the same law read in
    // this instrument's own unit, which is THE ROW — where the cut stands over the buffer's own
    // sample points, and whether the world is shut.
    //
    // WHAT A DOOR ASKS OF A WORLD. At either door the world is flat and one whole work stands in
    // the frame, cover-fitted and cropped by nothing, which is what the `framings` block publishes.
    // Three things carry that and this reads all three ON THE BUFFER rather than declaring them:
    //
    //   · THE WORLD IS SHUT. The dial's own window is a sine at its zero, so the sample coordinate
    //     is the plain cover-fit point at every pixel. A world standing even slightly open is a
    //     curled photograph and not a photograph.
    //   · ONE WORK STANDS, AND IT IS THE RIGHT ONE. The cut is walked at the buffer's own sample
    //     points — its four corners, the midpoints of its four edges, and the nine points around
    //     its centre — and every one of them must fall on the work the door names. What the walk
    //     publishes beside the count is how much row the nearest of those points had TO SPARE, so a
    //     cut trimmed toward its own ends shows the margin closing long before anything crosses.
    //   · THE JUDGES' CHANNEL IS SHUT. `mask` draws the cut map itself as colour, which is what it
    //     is for; left open at a door the frame is a false-colour map and not the photograph.
    //
    // AND THERE IS NOTHING HERE TO HOLD. The meshing instrument holds a leaking size whole and the
    // unfold holds a pair of panels flat, because in both a grid can show a fault a guard read in
    // the grid's own units can close. This one cannot: both doors are exact by construction — the
    // window is a sine at its own zero and the cut stands a fiftieth of the picture past its last
    // row — so anything this reading finds is a real fault that no widening closes, and the refusal
    // stands alone. `held` is therefore always nothing, and it says so rather than carrying a guard
    // that could never fire.
    var DOOR_OPEN = 0.5 / 255;    // how much world may stand at a door: half a level of 255
    var DOOR_SHOW = 0.5 / 255;    // and how much of the judges' channel, by the same reading

    // THE CUT, READ ON THE BUFFER THE SHADER WILL SAMPLE ON. The walk takes the buffer's own sample
    // points and asks each of them the very question the shader asks: which side of the row does
    // this point fall on. At a door the world is flat, so the row a point reads is the flat one —
    // the cover fit's own — and this reads it that way rather than assuming it.
    function cutReadOf(v, W, H) {
      var wrong = 0, spare = 1e9, walked = 0, i, j;
      var Phi = v.geom[0], R = v.geom[1], D = v.geom[2], ycb = v.geom[3];
      // the spin turns the world under the eye and never moves a row, so the second carrier is not
      // read here at all
      var S = v.cam[0], gamma = v.cam[2], flip = v.cam[3];
      var tau = v.cut[0], footFlat = v.cut[1];
      var want = tau > 0.5 ? 1 : 0;       // which work the cut says stands over the whole frame
      // ONE POINT OF THE BUFFER, ANSWERED THE SHADER'S OWN WAY. Every line here is the shader's,
      // read in the same order on the same numbers, so what this walks is the frame that is about
      // to be drawn rather than a second description of it.
      function walk(px, py) {
        var Px = px - 0.5 * W, Py = (H - py) - 0.5 * H;
        var dx = Px / S, dy = Py / S + ycb;
        var r = Math.max(Math.sqrt(dx * dx + dy * dy), 1e-6);
        var tr = (R - r) / D;
        var t = clamp(tr, 0, 1);
        var tg = Math.pow(Math.max(t, 1e-4), gamma);
        var vRow = flip ? tg : 1 - tg;
        var rowW = v.crop[0] + (v.crop[1] - v.crop[0]) * vRow;
        var rowFlat = clamp(0.5 + Py / Math.max(H, 1), 0, 1);
        var row = rowFlat + (rowW - rowFlat) * v.world;
        var gv = gamma * Math.pow(Math.max(t, 2e-3), gamma - 1)
               * Math.abs(v.crop[1] - v.crop[0]) / (D * S);
        var foot = Math.max(footFlat + (gv - footFlat) * v.world, 1e-6);
        var cov = clamp(0.5 + (tau - row) / foot, 0, 1);
        walked++;
        if ((want ? 1 - cov : cov) > 0.5 / 255) wrong++;
        spare = Math.min(spare, Math.abs(tau - row));
      }
      for (i = 0; i < 2; i++) {
        for (j = 0; j < 2; j++) { walk(i ? W - 0.5 : 0.5, j ? H - 0.5 : 0.5); }
      }
      walk(0.5, H * 0.5); walk(W - 0.5, H * 0.5); walk(W * 0.5, 0.5); walk(W * 0.5, H - 0.5);
      for (i = -1; i <= 1; i++) {
        for (j = -1; j <= 1; j++) { walk(W * 0.5 + i, H * 0.5 + j); }
      }
      return { walked: walked, wrong: wrong, spareRows: spare, want: want, cut0: tau,
               world: v.world, mask: v.mask };
    }

    // THE DOOR, MEASURED. Null everywhere but at a door, since away from the doors a curling world
    // is the picture rather than a fault. The door is named by the manifest's own `doors` block:
    // `mix` at 0 is the entry door, where the frame is the departing work whole, and `mix` at 1 the
    // exit door, where it is the arriving one.
    function doorReadOf(v, st) {
      var at = st.mix === 0 ? 0 : (st.mix === 1 ? 1 : -1);
      if (at < 0) return null;
      var g = v.grid;
      if (!g.given) return null;
      var read = cutReadOf(v, g.w, g.h);
      read.grid = g;
      read.door = at;
      return read;
    }

    // THE REFUSAL, worded the way the host's own manifest refusals read: what is wrong, in this
    // instrument's own measured numbers, on the grid it was measured on.
    function doorWhyNoOf(read) {
      if (!read) return null;
      var g = read.grid, door = read.door ? "the exit" : "the entry";
      var work = read.door ? "arriving" : "departing";
      var where = " of a " + g.w + " x " + g.h + (g.drawn ? " buffer" : " frame");
      if (read.world >= DOOR_OPEN) {
        return door + " door leaks: the world stands " + read.world.toFixed(6)
             + " open, so the frame is a photograph curled toward a world and not the " + work
             + " work standing flat, where " + door + " door's own law asks for the " + work
             + " work at every point";
      }
      if (read.wrong) {
        return door + " door leaks: the wrong work stands on " + read.wrong + " of the "
             + read.walked + " points this reading walked" + where + ", because the cut stands at "
             + "row " + read.cut0.toFixed(4) + " of the photograph instead of past its own ends, "
             + "where " + door + " door's own law asks for the " + work + " work at every point";
      }
      if (read.mask >= DOOR_SHOW) {
        return door + " door leaks: the judges' own channel stands at " + read.mask.toFixed(6)
             + ", so the frame draws the cut map — which work owns each point of a "
             + g.w + " x " + g.h + (g.drawn ? " buffer" : " frame")
             + " — instead of the " + work + " work, where " + door + " door's own law asks for "
             + "the " + work + " work at every point";
      }
      return null;
    }

    // THE NUMBERS OF ONE FRAME, WITH ITS DOOR READ ON THE BUFFER BEING DRAWN. Away from a door this
    // is `posed` and nothing more: the reading is taken nowhere else. At a door it walks the cut
    // over the buffer and publishes what it read — how many points it walked, how many stood on the
    // wrong work, how much row the nearest of them had to spare, and how far the world stood open.
    function values(st) {
      var v = posed(st);
      var read = doorReadOf(v, st);
      v.doorGrid = read ? read.grid : null;
      v.cutMap = read ? { walked: read.walked, wrong: read.wrong, spareRows: read.spareRows,
                          world: read.world, want: read.want } : null;
      v.doorHeld = null;
      v.doorWhyNo = doorWhyNoOf(read);
      return v;
    }

    // ---- WHAT A PAIR MUST READ FOR THIS CROSSING TO BE WORTH PLAYING -------------------------------
    // His word of 2026-08-18 09:01: an instrument does not go looking through a collection, it
    // answers for the pair in front of it. This is that answer, as a pure function of the two work
    // records, and it is published on the instrument so the composer can ask it at the instant a
    // visitor steps.
    //
    // WHAT IT READS OF A WORK, AND WHY EACH READING IS THERE. This answered a QUESTION until
    // 2026-08-18 — three clauses, each of which could decline a pair — and every one of the three
    // is kept, as the reading it always was. The arithmetic that ranks them lives in the composer's
    // `INSTRUMENT_SUITS`, the one place holding both records; what stands here is the reading of
    // one work, which is the fact this instrument owns.
    //   · HOW MUCH OF A WORLD THIS INSTRUMENT CAN DRAW THE WORK ALREADY IS. The record measures four
    //     polar readings per work; this instrument draws two of them — the sphere and the corridor
    //     — and the log-spiral is another instrument's world. So the stronger of `polar.planet` and
    //     `polar.tunnel` is the reading, and the log-spiral's share of the same family is taken off
    //     it rather than tested against it: a work reading equally as both is half a world here.
    //   · WHETHER THE WORK CARRIES A MEASURED HORIZON. The curl only becomes a WORLD where the
    //     picture divides into ground and sky: the foot of the frame goes to the centre and the sky
    //     becomes the ring around it and the light the whole stage stands in. A picture with no such
    //     division curls into a disc of pattern, which is a different and lesser thing — so it ranks
    //     lower, and it is not turned away.
    //   · READ OF THE PAIR AND NOT OF ONE END OF IT. A ground is the pair's, and the family read off
    //     it has to be the same one whichever way the visitor walks, so both works are read and the
    //     stronger reading carries the crossing.
    function polarOf(w) {
      var s = (w && w.structure) || {};
      var p = s.polar || {};
      var sphere = num(p.planet, 0), corridor = num(p.tunnel, 0), spiral = num(p.twirl, 0);
      var best = Math.max(sphere, corridor);
      var y = s.horizon ? s.horizon.y : null;
      return { sphere: sphere, corridor: corridor, spiral: spiral, best: best,
               shape: corridor > sphere ? "a corridor" : "a sphere",
               horizon: (y === null || y === undefined) ? null : num(y, null) };
    }
    // HOW MUCH OF A LITTLE WORLD ONE WORK IS, between nothing and whole. Three readings, none of
    // them a bar: the world reading, the share of it that is not the log-spiral's, and whether a
    // horizon was measured. A work answering nothing to all three reads 0, which is playable — it
    // simply ranks last.
    function worldOfOne(w) {
      var p = polarOf(w);
      var whole = p.best + p.spiral;
      var mine = whole > 0 ? p.best / whole : 0;
      var hasHorizon = !(p.horizon === null || !(p.horizon > 0) || !(p.horizon < 1));
      var fit = p.best * mine * (hasHorizon ? 1 : 0.5);
      return [fit, "reads " + p.shape + " at " + p.best.toFixed(4) + ", a log-spiral at "
              + p.spiral.toFixed(4) + ", and "
              + (hasHorizon ? "carries a measured horizon at " + p.horizon.toFixed(4)
                            : "carries no measured horizon, so it has no ground and sky to become "
                              + "a world and its own ring of light")];
    }
    // WHAT THE PAIR READS, with no direction on it and no pair turned away. The stronger of the two
    // works carries the crossing, because one world is what it curls into.
    function suitsPair(a, b) {
      var ra = worldOfOne(a), rb = worldOfOne(b);
      var best = ra[0] >= rb[0] ? ra : rb;
      return [best[0], "the better-suited work of the pair " + best[1]];
    }

    var manifest = {
      id: "planet", api: 1, arity: 2,
      // The photograph comes apart from the frame it hangs in and becomes a place; the arriving work
      // rises out of that place's own centre; and it lands flat.
      roles: ["disassembly", "mystery", "assembly"],
      // WHERE THIS STANDS ON THE CHARTER'S SHELF, and the two readings that decide it.
      //   · WORLD — the flat frame becomes a round place standing in its own light, seen from
      //     outside it, and the arriving work enters through that place's singular point.
      //     lab/data/module-contract.json's own row for this module reads `"level": "WORLD"`, and
      //     the charter's shelf 8 names the sphere among its projection worlds and says a folded
      //     space is at most one per crossing and IS the miracle. This declaration is what pays for
      //     that: an instrument publishing WORLD spends the crossing's one miracle, which puts it
      //     on the steps that have one to spend.
      //   · SURFACE — the curl is a deformation of the picture's own surface, and the cut the two
      //     works change over at is a ring OF that surface. This is the level his own standing
      //     verdict gives the module in the charter's vocabulary table («planet · SURFACE»), and it
      //     is kept because it is the level the CUT lives on.
      // The two readings disagreed and both are recorded: the vocabulary's SURFACE is the older and
      // coarser of the two, the contract table's WORLD is the module's own row, and the shelf that
      // names the sphere settles it. CELL, CELL CONTENT, TEXTURE and LIGHT-COLOUR are not claimed.
      levels: ["WORLD", "SURFACE"],
      // WHERE THIS INSTRUMENT HAS A SEAM (§8's `seams` block). The strip this curl bends is one
      // photograph wrapped into a RING, and its two ends meet at a join the module itself never
      // closes to nothing — «a shut ring has no cut down it either» — so the join is glued by a
      // HANDOVER ZONE, a real cross-dissolve rather than an antialiasing retouch. `of` names no
      // handle: the strip wraps exactly once, so the zone is a single wrap's own share and not a
      // share divided among several.
      seams: [{ kind: "ring", of: null, unit: "a share of one repeat's own span" }],
      params: { curl: [0, 1], depth: [0, 1], dip: [0, 1], turn: [0, 1], gather: [0, 1] },
      // EVERY handle a score can drive (§4.4b). `mix` is the dial — the module's own hidden `world`
      // key, under the name every instrument in this engine gives it, carrying the whole passage:
      // the world opens, the arriving work rises out of its centre, the world shuts.
      //
      // NO SEED, AND THAT IS A DECISION. Nothing in this picture is rolled: the module carries no
      // die of its own and this port adds none, so a handle for one would be a handle a score could
      // walk without moving the picture, which is noise in the score (§4.4b).
      handles: {
        // `mix` is the crossing's own dial and `clock` the module's own time; neither drives a
        // structural level of the picture.
        mix: { min: 0, max: 1, def: 0, level: null },
        clock: { min: 0, max: 14, def: 0, unit: "the second the passage stands at",
                 applied: { breathAtWhole: 0.055,
                            restsAt: "no instant; the breath is a sum of two slow sines and the "
                                   + "world stays shut through all of it" },
                 level: null },
        // How far it bends: WORLD.
        curl: { min: 0, max: 1, def: 0.82,
                unit: "how far the strip is bent when the world stands open",
                reads: "structure.polar.planet, the departing work's own reading as a little world "
                     + "— a picture that already turns about a centre is closed the whole way, and "
                     + "one that barely does is left as a bowed band. The rest at 0.82 is his own "
                     + "taste-approved state of 2026-08-08 11:39 («planet curl 82»), which is where "
                     + "the handle stands until a score names the work's own",
                applied: { easedBy: 2.4, floor: 0.006 },
                level: "WORLD" },
        // Which geometry the space itself takes — a sphere or a corridor: WORLD.
        depth: { min: 0, max: 1, def: 0,
                 unit: "which of the two worlds: a sphere, or the same one turned inside out",
                 reads: "structure.polar.tunnel, the departing work's own corridor reading. Over "
                      + "half the picture is turned inside out and the visitor stands inside a "
                      + "corridor instead of outside a sphere; under it the world is a sphere",
                 applied: { turnsInsideOutAbove: 0.5 },
                 level: "WORLD" },
        // Where the horizon's axis stands: WORLD.
        dip: { min: 0, max: 1, def: 0.5,
               unit: "where the horizon stands: how much of the sky is pulled in toward the centre",
               reads: "structure.horizon.y, the departing work's own measured horizon. The middle "
                    + "of the handle is the picture's own place — the module's own door — and the "
                    + "reach is half a gamma either way, which is the reach the hand had",
               applied: { reach: HORIZON_REACH, curve: "a two-piece logarithm hinged at the middle, "
                                                     + "because the middle is a door" },
               level: "WORLD" },
        // Turns the world about its own axis: WORLD.
        turn: { min: 0, max: 1, def: 0.5, unit: "how far the world is turned",
                reads: "structure.radial.score, the work's own measured radial reading — a work "
                     + "whose rings are its own device turns the world and one that barely reads "
                     + "radial barely turns it",
                applied: { reach: TURN_REACH, restsAt: "the middle, where the world stands square",
                           curve: "linear by measurement: equal angles of turn move the same "
                                + "picture past the same eye" },
                level: "WORLD" },
        // How much of the frame the figure holds — a gather of the whole picture, taken as one:
        // SURFACE.
        gather: { min: 0, max: 1, def: FIG_HI,
                  unit: "how much of the frame the work's own figure holds",
                  reads: "the share of the frame the work's own measured dominant object holds. It "
                       + "is the reading the module's own table of three photographs stands on: a "
                       + "figure filling the frame keeps nearly all its rows and is bent gently, "
                       + "and a spike in a wide sky is taken with the sky cut away and bent harder, "
                       + "or it comes out as a speck in a cloud",
                  applied: { cropAt: [CROP_LO, CROP_HI], gammaAt: [GAMMA_LO, GAMMA_HI],
                             readAt: [FIG_LO, FIG_HI] },
                  level: "SURFACE" },
        // The fleet's own shade judge channel; it drives no structural level.
        shade: { min: 0, max: 1, def: 1, unit: "the world's own finish",
                 applied: { restsAt: "1, where the finish is the module's own",
                            covers: "the radial curve of light, the stage's own lamp, the sitting "
                                  + "back of the collapsing centre and the closing gamma" },
                 level: null },
        // THE MEASUREMENT THIS HANDLE IS READ AGAINST AT A DOOR. `readAtADoor` says what is read
        // (this instrument's own cut, walked at the buffer's own sample points), on which grid (the
        // drawing buffer the host binds, with the CSS frame where it hands none), what the reading
        // is counted in, and that there is no hold — both doors are exact by construction rather
        // than by a tolerance, so a door this reading finds a fault at is refused outright. It is
        // the judges' own channel and drives no structural level.
        mask: { min: 0, max: 1, def: 0,
                applied: { readAtADoor: { rows: CUT_ROOM, readOn: "the drawing buffer",
                                          reads: "the cut",
                                          measures: "which work stands at the buffer's own sample "
                                                  + "points, and how far the world stands open",
                                          held: null } },
                level: null },
      },
      neutrals: { a: 0, b: 1 },
      doors: { in: { handle: "mix", value: 0, work: "a" },
               out: { handle: "mix", value: 1, work: "b" } },
      // BOTH DOORS FRAME ALIKE AND NEITHER CROPS. A door of this instrument stands the work
      // cover-fitted into the frame and nothing else, which is exactly what
      // lab/data/module-contract.json publishes for this module's own two doors: «the flat end is
      // the plain cover-fit of the same texture unit, so both doors frame the picture alike».
      framings: { "0": { coverCrop: 1.0 }, "1": { coverCrop: 1.0 } },
      drivers: ["progress", "cueProgress", "time", "velocity", "capability", "noise", "static",
                "curve", "spline", "map", "add", "multiply", "mix", "clamp", "hold", "segment",
                "ramp", "slew", "oscillate", "node"],
      camera: { needs: "none", authority: "stage" },
      // THE PICTURE'S OWN CHAIN OF SMALLER COPIES, asked for by §8's `gl.readsChain`. The
      // module against itself with its chain taken off reads 0.36 and 0.41 of 255, worst
      // channel 44 and 82: the host binds one plain texture per work with no chain, so
      // `textureLod` clamps to level 0 here and the sky wash reads sharper than the module's.
      // The flag asks the host for the chain and the shader keeps the module's own two
      // fetches exactly as they stand.
      gl: { preserveDrawingBuffer: false, readsChain: true },
      // WHAT THIS INSTRUMENT WRITES WHERE ITS OWN MATTER IS ABSENT (§7's coverage law, and the
      // per-instrument specification in docs/design/COVERAGE.md). It is absent nowhere.
      coverage: { writes: false,
                  how: "outside the world's own rim the frame is not empty: it carries the sky of "
                     + "the work that owns the world, smeared wide and dimmed, and the reach of "
                     + "that wash is read off the frame itself so the farthest corner of any stage "
                     + "stands at the same place on its curve. The alpha is the constant 1 at every "
                     + "point of every pose, and at a door the world is shut and the frame is the "
                     + "photograph cover-fitted" },
      // WHAT A PAIR MUST READ, published beside the handles so a reader finds it where the rest of
      // the contract is. The function itself is on the instrument, so the answer is the
      // instrument's own rather than a copy of it kept somewhere else.
      suits: { reads: ["structure.polar.planet", "structure.polar.tunnel", "structure.polar.twirl",
                       "structure.horizon.y"],
               how: "it suits a pair the better one of whose works already is a little world — a "
                  + "sphere or a corridor rather than a log-spiral, which is another instrument's "
                  + "world, and one carrying a measured horizon, since a real division into ground "
                  + "and sky is what the curl turns into a world with its own ring of light. A work "
                  + "with none of that reads nothing here, which still plays and simply ranks last" },
      // The neutral pose is the ENTRY DOOR — `mix` at 0, the value the `doors` block above names —
      // so the frame keys the host reads off it at registration include the door's own record.
      neutralPose: { mix: 0, clock: 0, curl: 0.82, depth: 0, dip: 0.5, turn: 0.5, gather: FIG_HI,
                     shade: 1, mask: 0, reduced: false, cssWidth: 1000, cssHeight: 1000,
                     fitA: [1, 1, 0, 0], fitB: [1, 1, 0, 0] },
      passes: [{
        program: "planet", vert: VERT, frag: FRAG, position: "aPos",
        uniforms: [
          { name: "uA", type: "sampler2D", source: "textureA" },
          { name: "uB", type: "sampler2D", source: "textureB" },
          { name: "uRes", type: "vec2", source: "resolution" },
          { name: "uGeom", type: "vec4", source: "frame:geom" },
          { name: "uCam", type: "vec4", source: "frame:cam" },
          { name: "uWedge", type: "vec4", source: "frame:wedge" },
          { name: "uCrop", type: "vec2", source: "frame:crop" },
          { name: "uWorld", type: "float", source: "frame:world" },
          { name: "uFlatPP", type: "vec4", source: "frame:flatPP" },
          { name: "uCut", type: "vec4", source: "frame:cut" },
          { name: "uShade", type: "float", source: "handle:shade" },
          { name: "uMask", type: "float", source: "handle:mask" },
        ],
      }],
      // The instrument allocates nothing of its own: it spends the two source-texture slots the host
      // already holds and the one programme the host builds from this manifest. The module's own
      // canvas, its context, its two textures, its mipmap chains and its own frame loop are what
      // this port does without.
      resources: { lean: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                           passes: 1, bytesEstimate: 0, variant: "lean" },
                   standard: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0,
                               programs: 1, passes: 1, bytesEstimate: 0, variant: "standard" },
                   rich: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                           passes: 1, bytesEstimate: 0, variant: "rich" } },
      capabilities: ["webgl2"],
      // THE TWO DECLINES LEFT BOTH SAY THERE IS NO PAIR. A third stood here — "a pair where
      // neither work reads as a world worth curling" — and it went with the floor it named,
      // 2026-08-18: a reading is never grounds for refusing a visitor a crossing (his 09:51).
      decline: ["one work only", "a source that never decoded"],
      provenance: { labPath: "lab/effects/planet.js", commit: "4952bfe",
                    sha256: "0782a8bc4b7cb35e11cc35966f33695a601789eb1aee8f3a2ea19e205384eb3e" },
      readiness: "production-ready",
    };

    var live = false;
    return {
      name: "planet",
      manifest: manifest,
      values: values,
      fit: fit,
      feel: feelOf,
      // WHAT A PAIR READS, as a function rather than as a sentence. A composer holding two work
      // records asks this and gets back a fit between nothing and whole with the reason in the
      // works' own numbers — never a yes or a no. A fit of nothing is playable and ranks last.
      suits: suitsPair,
      prepare: function (o) {
        if (!o.sources) return { take: false, why: "the planet instrument needs both works" };
        if (!o.cue) return { take: false, why: "no cue names it" };
        return { take: true };
      },
      start: function () { live = true; },
      // The pose the shader draws. The module's canvas, its frame loop, its pointer and its own
      // second are gone, so every number here comes from a handle a score drives or from the frame
      // the host is about to bind.
      //
      // A DOOR THIS INSTRUMENT CANNOT KEEP WHOLE IS REFUSED RATHER THAN DRAWN. At either door it
      // walks its own cut over the buffer the host is about to bind and, where the world stands
      // open, where a point of that grid falls on the wrong work, or where the judges' channel is
      // left open, it hands the host the reason with the measured numbers in it instead of drawing
      // a door that is not the photograph. The host recovers the transaction on that reason and the
      // walk's own glide carries the visitor, which is the product's own behaviour with no renderer.
      frame: function (st) {
        if (!live) return;
        var h = st.handles;
        var pose = {
          mix: h.mix, clock: h.clock, curl: h.curl, depth: h.depth, dip: h.dip, turn: h.turn,
          gather: h.gather, shade: h.shade, mask: h.mask, reduced: st.reduced,
          cssWidth: st.viewport.w, cssHeight: st.viewport.h,
          // THE GRID THE SHADER WILL SAMPLE ON, carried into the pose so the geometry is built for
          // the frame the host is about to bind as `uRes` and the door is read on it rather than on
          // the CSS frame around it. The host settles it from the device ratio and its own
          // resolution step, so it moves while a pass plays and each door is read on the grid
          // standing at that door's own instant.
          bufWidth: st.viewport.bufferW, bufHeight: st.viewport.bufferH,
          // BOTH WORKS' SEATING ON THAT SAME BUFFER, which only the host can answer. The curl's own
          // geometry is built on the picture's proportions, and this is where they come from: the
          // seating the host asked this file's own `fit` for and will bind to the shader.
          fitA: st.fitA, fitB: st.fitB,
          // THE WRAP'S OWN SEAM, off the host's own `seams` reading (§8's `seams` block). Only the
          // host knows what every instrument declaring a handover zone is holding its own wrap to.
          seam: st.seams,
        };
        // AT A DOOR THE INSTRUMENT SAYS WHAT IT APPLIED, and says it before it refuses. The reading
        // is taken on the buffer this frame is drawn on, so it is the run-time truth his 18:00
        // decision asks for. `request` is what a landing asks of the world — that it be shut — and
        // `applied` is how far open this grid actually shows it, so `moved` is the two read against
        // each other on the dial's own scale.
        if (h.mix === 0 || h.mix === 1) {
          var v = values(pose);
          if (st.reportApplied) {
            st.reportApplied({
              door: h.mix === 0 ? "in" : "out",
              buffer: [pose.bufWidth, pose.bufHeight],
              reads: "the world shut and one whole work standing",
              request: 0, applied: v.world, moved: v.world,
              unit: "the dial's own units, 0 the flat photograph and 1 the world",
              // What the cut was doing over the frame at this door: how many of the walked points
              // stood on the wrong work, and how much row the nearest of them had to spare, so a
              // door held whole says so about the cut as well as about the world.
              wrong: v.cutMap ? v.cutMap.wrong : null,
              walked: v.cutMap ? v.cutMap.walked : null,
              spareRows: v.cutMap ? v.cutMap.spareRows : null,
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
    instrument: planetInstrument(),
  });
})();
