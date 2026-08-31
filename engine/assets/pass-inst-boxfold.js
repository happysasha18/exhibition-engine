/*!pass-inst-boxfold.js*/
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
  // THE BOX-FOLD INSTRUMENT (§8) — lab/effects/box.js carried across
  // ================================================================================================
  // WHY IT IS NAMED «boxfold» AND NOT «box». The host's own boundary row forbids the built host from
  // naming any instrument at all, and it reads that by searching the built bytes for every shipping
  // instrument's name. `box` is three letters of ordinary English and the host uses it for a local
  // of its own — the record of uniform sources it binds a pass from (`drawPose` in pass-layer.js) —
  // so an instrument called `box` makes that row red on a word that has nothing to do with it, and
  // a row that cannot tell a real leak from an accident guards nothing. `boxfold` is the composer's
  // own name for the road this instrument answers, and it appears nowhere in the host.
  //
  // WHAT THE VISITOR SEES. The frame is one face of a box. The box turns a quarter with true
  // perspective while the camera rides up through the turn and slides sideways, and the face that
  // was standing gives way to the face coming round. The two faces meet at a finger joint with a
  // contact shadow along it, they interlock like the corner of a made box, and each of them carries
  // its own picture travelling the other way while the turn is happening. The turn's rate is nothing
  // at each landing and most in the middle, so the arriving face comes to rest rather than being
  // spun to a stop, and it lands exactly: at either door the frame is the work its source carries.
  //
  // WHY IT STANDS HERE. The composer's box-fold road qualifies on the measurements for 4 670 ordered
  // pairs and plays for none of them, because `INSTRUMENT_OF_KIND.panel` in pass-composer.js names
  // no instrument at all and the plan is declined for want of one (its own `MISSING_INSTRUMENT`
  // entry: «an instrument that cuts on panels, for region_dissolve and object_reveal»). This
  // instrument is what that line will name.
  //
  // ------------------------------------------------------------------------------------------------
  // THE FIVE-CONDITION PARDON, AND WHICH OF THE FIVE THIS FILE ANSWERS
  // ------------------------------------------------------------------------------------------------
  // The charter convicts the screen-as-cube-face turn by name and pardons the box in the same
  // sentence, under five conditions (lab/CROSSING-BRIEF.md, the keeper list's own amendment of
  // 12.08 23:43 and 23:49). Each is answered by a measurement rather than by argument, and each has
  // an owner. The instrument answers three of them whole, one with the composer, and one with the
  // host.
  //
  //   1. THE FOLD STANDS ON THE DEPARTING WORK'S OWN MEASURED REGION LINE — the instrument's, with
  //      the composer. The instrument slides the whole camera through the turn by exactly what
  //      carries the crease onto that line, and rests that slide at every landing. WHERE the line
  //      stands is a measurement of the work, and no instrument may take it: reading it means
  //      drawing the picture into a scratch surface and counting, which §1.2's fence forbids here.
  //      So the place arrives as a handle — `seam`, with `seamScore` as its gate — and the handle
  //      publishes the measurement it reads: `structure.regions` from lab/cut-lines.py, whose
  //      `line.<axis>.at` is the place and whose `line.<axis>.explains` is the gate — that second
  //      reading, and not the record's own `regions.score`, is what the floor was calibrated
  //      against. Below the floor the crease stays where the
  //      box's own edge puts it and the reading says so out loud, rather than passing a made-up
  //      number off as the work's own.
  //   2. THE FACES CARRY LIVE PICTURES RE-READ EVERY DRAWN FRAME — the host's. The module re-read a
  //      live source into its texture on every frame it drew, so whatever another module was drawing
  //      on a face was playing on that face. Here the two faces are the host's own two source
  //      textures, uploaded by the host and bound afresh for every pass it issues; this instrument
  //      caches no face, holds no texture of its own and samples what is bound at the instant it
  //      draws. The half of that condition the module's own header calls THE CLASS — a face being a
  //      surface ANOTHER module is drawing on this second — waits on a host that binds more than two
  //      sources, which §7's uniform-source set does not yet carry.
  //   3. A CONTACT SHADOW READS ON EVERY EDGE — the instrument's, whole. The shadow decays
  //      exponentially from the crease's own line into whichever face lies farther from the eye, it
  //      is read in points of the drawing buffer so it is the same physical edge whatever the turn
  //      is doing to the geometry, and it is gated to nothing at every landing, where one face
  //      stands whole and there is no edge for it to lie on.
  //   4. THE CAMERA TRAVELS WITH TRUE PERSPECTIVE — the instrument's, whole. Each face's map from
  //      its own square to the frame is a homography, and the shader reads that map BACKWARDS for
  //      every point of the frame: a real projection inverted per pixel, not an affine fake. The
  //      camera's own height through the turn and its slide onto the work's region line ride the
  //      same window, and both are nothing at a landing. The instrument asks the HOST's camera for
  //      nothing (`camera: { needs: "none" }`), because the perspective it needs is inside its own
  //      pass.
  //   5. IT LANDS EXACTLY — the instrument's, whole, and it is the door law below. At either door
  //      the turn is a whole quarter, the camera is level, the slide is nothing, the joint has no
  //      bite and the shadow is out, so the frame is the source cover-fitted and centre-cropped by
  //      the box's own crop and nothing else. The instrument does not declare that: it reads it on
  //      the drawing buffer the host is about to bind, publishes what it read, and refuses a door it
  //      cannot keep whole.
  //
  // ------------------------------------------------------------------------------------------------
  // WHAT CAME OVER, AND WHAT STAYED BEHIND
  // ------------------------------------------------------------------------------------------------
  // WHAT CAME OVER: the crop that keeps the frame covered at every angle, the camera's own distance
  // range and its dip, the turn's rate inside a quarter and the dead bands at either end, the
  // counter-motion each face's picture travels by, the finger joint with its count and its half-
  // seeded order, the contact shadow with its depth and its reach, the gate that puts the shadow out
  // at a landing, the floor a work's region split must clear before it counts as a seam, and the
  // background the box stands against. Every one of them is carried digit for digit and the suite
  // reads both files for each.
  //
  // THE PORT'S OWN ONE NUMBER is the room the crease's travel needs in the crop, and the reason it is
  // the port's is that the module measured its crop for the turn alone and moved the crease onto the
  // work's own line afterwards without reading the crop again. It is the only number below the module
  // did not measure, and it is measured here on the same sweep.
  //
  // WHAT STAYED BEHIND: the module's own canvas and context, its frame loop, its resize observer,
  // its texture uploads, its `preserveDrawingBuffer` request (§7 refuses a manifest that asks for
  // it), and its own measurement of the seam off the picture — that one is a measurement of the
  // work, and it arrives as a handle for the reason condition 1 gives above.
  //
  // AND THE BOX SHOWS TWO FACES, NOT FOUR. The module's `faces` param runs to four, and a face is a
  // work: a cue of this engine carries an ordered PAIR (§8's `arity: 2`, and the `doors` block's own
  // `work: "a"` and `work: "b"`), so two is what a pair can stand. A journey of an odd number of
  // quarters would land the visitor back on the departing work, which the exit door forbids by name.
  // The handle is therefore not published and the number is pinned, said here rather than left for a
  // reader to discover from a missing row.
  //
  // ------------------------------------------------------------------------------------------------
  // THE COVERAGE: THIS INSTRUMENT FILLS THE FRAME
  // ------------------------------------------------------------------------------------------------
  // §7's coverage law of 12:40 asks every instrument to say where its own matter is absent. Here it
  // is absent nowhere, and the reason is two measured numbers rather than a claim. A box turning
  // about its own centre does not cover a rectangular frame at every angle — mid-quarter the two
  // visible faces retreat from the frame's corners — and a camera sliding to put the crease on the
  // work's own region line pulls the box off the frame on top of that. So the box is built LARGER
  // than the frame by the room the turn needs plus the room the crease's travel needs, and the frame
  // is a window cut out of the middle of a bigger box. The first room is the module's own measured
  // number; the second is this port's, and it exists because the module measured its crop for the
  // turn alone and never read it again after the crease was moved onto the work's line. The
  // declaration is `writes: false`, which under the placement rule (§8 as amended 14:05, and
  // `coverageWhyNo`) makes it lawful as the LOWEST cue of a stack and as a whole one-cue score —
  // and it is that placement which makes the leak worth closing, because a bare point at the bottom
  // of a stack shows the cleared buffer.
  function boxInstrument() {
    var VERT = [
      "attribute vec2 aPos;",
      "varying vec2 vUv;",
      "void main(){ vUv = vec2(aPos.x * 0.5 + 0.5, 0.5 - aPos.y * 0.5); gl_Position = vec4(aPos, 0.0, 1.0); }",
    ].join("\n");

    // ----------------------------------------------------------------------------------------------
    // THE SHADER, AND THE ONE THING THE HOST'S CARRIERS CHANGED ABOUT IT
    // ----------------------------------------------------------------------------------------------
    // The module handed its shader two three-by-three matrices and two arrays of four lines. The host
    // binds four uniform types and no more — `sampler2D`, `float`, `vec2`, `vec4` (pass-layer.js's
    // own `UTYPE`) — so neither a matrix nor an array of lines can travel. Two things follow, and
    // neither touches a line of the mathematics:
    //
    //   · EACH INVERSE MAP TRAVELS AS ITS THREE ROWS, one row to a carrier. A three-by-three holds
    //     nine numbers and the widest carrier holds four, so the fourth place of each carrier is
    //     unused. The rows are the same rows the module built and multiplied by, in the same order.
    //   · EACH FACE'S SCREEN SHAPE TRAVELS AS ITS FOUR CORNERS, two corners to a carrier, and the
    //     four straight edges are built from them HERE. A projection takes a straight edge to a
    //     straight edge, so a face's screen shape is an exact quadrilateral and its four corners are
    //     the whole of it; the module's own `edgesOf` is carried across line for line and simply runs
    //     in the shader instead of in the script. Eight numbers travel where twelve did, and the two
    //     descriptions of one quadrilateral can no longer disagree with each other.
    var FRAG = [
      "precision highp float;",
      "varying vec2 vUv;",
      "uniform sampler2D uA;",             // the face the eye is leaving
      "uniform sampler2D uB;",             // the face it is arriving at
      "uniform vec4 uFitA;",
      "uniform vec4 uFitB;",
      "uniform vec2 uRes;",
      // The two inverse maps, screen (frame units, the camera's own travel taken out) -> the face's
      // own square, a row of three to a carrier.
      "uniform vec4 uInvA0;",
      "uniform vec4 uInvA1;",
      "uniform vec4 uInvA2;",
      "uniform vec4 uInvB0;",
      "uniform vec4 uInvB1;",
      "uniform vec4 uInvB2;",
      // The two screen quads, corner 0 and corner 1 in the first carrier, corners 2 and 3 in the
      // second, in the order the module walks them: (-1,-1), (1,-1), (1,1), (-1,1) of the face's own
      // square. The shared edge between the two faces is face A's own corner 0 to corner 3.
      "uniform vec4 uQuadA0;",
      "uniform vec4 uQuadA1;",
      "uniform vec4 uQuadB0;",
      "uniform vec4 uQuadB1;",
      // THE CAMERA: the frame's own aspect, how far the eye has ridden up through this quarter, and
      // the slide that carries the crease onto the departing work's own region line. The last three
      // are all nothing at a landing.
      "uniform vec4 uCam;",
      // WHAT THE TURN IS DOING TO THE TWO FACES: whether the second face has any width at all, how
      // far each face's picture has travelled along its own axis, which face lies nearer the eye at
      // the crease, and the contact shadow's own gate.
      "uniform vec4 uTurn;",
      // THE FINGER JOINT: how deep it bites, in frame units, and how many fingers stand along the
      // crease.
      "uniform vec2 uJoint;",
      // The score's die, which decides four parts in ten of the joint's order.
      "uniform float uSeed;",
      // The judges' channel: the face map as colour.
      "uniform float uMask;",
      // WHAT THE BOX STANDS AGAINST where neither face reaches. The crop below is measured so that
      // this is drawn on no point of the frame at any angle of the turn; it is here because a
      // picture that quietly drew nothing would be worse than one that draws something a reading can
      // see, and the door's own reading counts exactly the points that would take it (box.js:207).
      "const vec3 DARK = vec3(0.031, 0.031, 0.039);",
      // THE CONTACT SHADOW'S OWN TWO NUMBERS (box.js:205): how deep it goes at the crease itself,
      // and how far it reaches into the face, in points of the drawing buffer. Reading the reach in
      // POINTS rather than in frame units is what makes it the same physical edge whatever the turn
      // is doing to the geometry.
      "const float SHADE = 0.34;",
      "const float REACH = 9.0;",
      // HOW MUCH OF THE JOINT'S ORDER THE SCORE'S DIE OWNS (box.js:185): six parts a plain ladder
      // along the crease, four parts the die. A whole ladder reads as a comb and a whole die reads as
      // noise; this is the module's own measured mixture, and because it is the SCORE's die and not
      // a roll of the instrument's own, a seeded run draws one picture.
      "const float DIE = 0.4;",
      "float hash11(float n){ return fract(sin(n * 127.1) * 43758.5453); }",
      // A face carries its source cover-fit over the WHOLE face, and the face is larger than the
      // frame by the crop the turn needs, so the frame sees the middle of the picture and the travel
      // never runs off it (box.js:149-154).
      "vec2 into(vec2 p, vec4 f){",
      "  return clamp((p - 0.5) * f.xy + 0.5 + f.zw, 0.0008, 0.9992);",
      "}",
      // WHERE ONE POINT OF THE FRAME FALLS ON ONE FACE. The map is projective and it is read
      // backwards: three dot products and one divide, which is the module's own `uInvA * vec3(pp,
      // 1.0)` with the matrix arriving as its three rows. The guard on the divide is the port's own
      // and costs no pixel: it fires only on the face's own horizon line, where the module divided by
      // nothing at all.
      "vec2 onFace(vec4 r0, vec4 r1, vec4 r2, vec2 p){",
      "  vec3 t = vec3(p, 1.0);",
      "  float w = dot(r2.xyz, t);",
      "  return vec2(dot(r0.xyz, t), dot(r1.xyz, t)) / (abs(w) < 1e-9 ? 1e-9 : w);",
      "}",
      // ONE EDGE OF A SCREEN QUAD, as a line with the quad's own inside positive — box.js's
      // `edgesOf` for a single edge, the normal turned to face the quad's centre.
      "float side(vec2 p, vec2 q, vec2 mid, vec2 x){",
      "  vec2 n = vec2(-(q.y - p.y), q.x - p.x);",
      "  float len = length(n);",
      "  n /= (len < 1e-9 ? 1e-9 : len);",
      "  float d = -dot(n, p);",
      "  return ((dot(n, mid) + d) < 0.0 ? -1.0 : 1.0) * (dot(n, x) + d);",
      "}",
      "vec2 midOf(vec4 q0, vec4 q1){ return 0.25 * (q0.xy + q0.zw + q1.xy + q1.zw); }",
      // HOW FAR INSIDE ITS OWN FACE A POINT OF THE FRAME LIES, in frame units — the least of its four
      // signed edge distances, negative outside (box.js:156-160).
      "float inside(vec4 q0, vec4 q1, vec2 x){",
      "  vec2 m = midOf(q0, q1);",
      "  return min(min(side(q0.xy, q0.zw, m, x), side(q0.zw, q1.xy, m, x)),",
      "             min(side(q1.xy, q1.zw, m, x), side(q1.zw, q0.xy, m, x)));",
      "}",
      "void main(){",
      // the screen point in frame units, x across, y up, and the same point with the camera's own
      // height and slide taken out, which is the space the two maps are written in
      "  vec2 sp = vec2((vUv.x - 0.5) * 2.0 * uCam.x, (0.5 - vUv.y) * 2.0);",
      "  vec2 pp = vec2(sp.x - uCam.z, sp.y - uCam.y - uCam.w);",
      "  float px = 2.0 / max(uRes.y, 1.0);",     // one point of the drawing buffer, in frame units
      "  vec2 stA = onFace(uInvA0, uInvA1, uInvA2, pp);",
      "  vec2 stB = onFace(uInvB0, uInvB1, uInvB2, pp);",
      // st.y runs UP the frame and an image's rows run DOWN it, so the row coordinate is turned over
      // here, or the face stands on its head
      "  vec2 uvA = vec2(stA.x * 0.5 + 0.5, 0.5 - stA.y * 0.5);",
      "  vec2 uvB = vec2(stB.x * 0.5 + 0.5, 0.5 - stB.y * 0.5);",
      "  float dA = inside(uQuadA0, uQuadA1, sp);",
      "  float dB = mix(inside(uQuadB0, uQuadB1, sp), -1e9, uTurn.x);",
      // THE FINGER JOINT. The crease is displaced back and forth along its own length, finger by
      // finger, and which face a finger belongs to is six parts a ladder along the crease and four
      // parts the score's die. The displacement is nothing at a landing, so a whole face stays whole
      // (box.js:180-186).
      "  float along = clamp(stA.y * 0.5 + 0.5, 0.0, 1.0);",
      "  float fi = floor(along * uJoint.y);",
      "  float ord = mix(fi / max(uJoint.y - 1.0, 1.0), hash11(fi + uSeed), DIE);",
      "  float bite = uJoint.x * (ord - 0.5) * 2.0;",
      // COVERAGE OVER THE PIXEL'S OWN FOOTPRINT, NEVER TRANSPARENCY. The crease is where the two
      // distances meet, and the answer is the share of THIS point that falls on the leaving face. No
      // fade anywhere; the alpha below is written 1 (box.js:188-192).
      "  float m = (dA - dB) * 0.5 + bite;",
      "  float cov = clamp(0.5 + m / px, 0.0, 1.0);",
      "  float onBox = clamp(0.5 + max(dA, dB) / px, 0.0, 1.0);",
      // COUNTER-MOTION along each face's own first axis, in opposite senses; both are nothing at a
      // landing, so a landed face is the picture its source carries.
      "  vec3 colA = texture2D(uA, into(uvA + vec2(uTurn.y, 0.0), uFitA)).rgb;",
      "  vec3 colB = texture2D(uB, into(uvB - vec2(uTurn.y, 0.0), uFitB)).rgb;",
      "  vec3 col = mix(colB, colA, cov);",
      // THE CONTACT SHADOW at the crease, on whichever face lies farther from the eye. The crease is
      // face A's own corner 0 to corner 3 — the same edge of the same solid the two faces share —
      // and the distance is read from that line in points, so the shade is the same physical edge
      // whatever the turn is doing to the geometry (box.js:199-205).
      "  float dc = side(uQuadA0.xy, uQuadA1.zw, midOf(uQuadA0, uQuadA1), sp) / px;",
      "  float far = uTurn.z > 0.0 ? max(-dc, 0.0) : max(dc, 0.0);",
      "  float lit = uTurn.z > 0.0 ? (1.0 - cov) : cov;",
      "  col *= 1.0 - SHADE * uTurn.w * lit * exp(-far / REACH);",
      "  col = mix(DARK, col, onBox);",
      // THE FACE MAP, the judges' own frame: which face stands at this point of the frame and where
      // in it. It is BLACK exactly where neither face stands, so a row reads off the picture whether
      // the crop kept its promise, and it carries no coverage of its own because what it is for is to
      // be read as colour.
      "  vec2 loc = mix(uvB, uvA, step(0.5, cov));",
      "  vec3 judge = vec3(onBox * mix(1.0, 0.5, cov), clamp(loc.x, 0.0, 1.0), clamp(loc.y, 0.0, 1.0));",
      "  col = mix(col, judge, uMask);",
      // THE COVERAGE: the alpha is the constant 1, and it is a decision rather than a default. The
      // crop is measured so the two faces cover the frame at every angle of the turn, so this
      // instrument has no absence to publish and stands as the ground a stack is laid on.
      "  gl_FragColor = vec4(col, 1.0);",
      "}",
    ].join("\n");

    function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
    function smoothstep(a, b, x) {
      var t = (x - a) / (b - a);
      t = t < 0 ? 0 : t > 1 ? 1 : t;
      return t * t * (3 - 2 * t);
    }

    /* THE ROOM THE TURN NEEDS, and why it is not a free number (box.js:259-271). A box turning about
       its own centre does not cover a rectangular frame at every angle: mid-quarter the two visible
       faces retreat from the frame's corners, worst around ten to twenty degrees into the turn, where
       the far edge of the arriving face reaches only 0.74 of the frame's half-width at the deepest
       perspective this instrument allows. The box is therefore built larger than the frame by exactly
       the reciprocal of that worst case, with a margin for the camera's dip. MEASURED, not guessed: a
       sweep of both axes, three perspectives, both dips and twenty-one places on the turn shows a
       crop of 1.34 leaking a background wedge of 2.1 per cent of the frame at eighteen degrees into
       the turn, and 1.48 leaking nothing at all anywhere. */
    var BOX_CROP = 1.48;

    /* AND THE ROOM THE CREASE'S OWN TRAVEL NEEDS ON TOP OF IT. This is the port's own number, and the
       reason it exists is a gap in the module's own record: the crop above was measured for the TURN
       ALONE, and the crease was moved onto the departing work's own region line afterwards
       (box.js:300-328, the repair of 13.08) without the crop being read again. Carrying the camera's
       slide over a box built for no slide opens the frame's own corners: at the far end of the
       measurement's window the module leaves up to 0.60 of a frame half-extent of its corners bare
       mid-turn, and it is a leak this engine cannot carry, because an instrument declaring it writes
       no coverage stands at the bottom of a stack, where a bare point shows the cleared buffer and
       not a dark corner.

       WHAT THE NUMBER IS, AND HOW IT WAS READ. The crease's travel is bounded by the MEASUREMENT'S
       own window: lab/cut-lines.py and the module's own `seamOf` search the middle half of the work
       for the line, so a region line stands between a quarter and three quarters of the way across
       and the camera's slide never exceeds half a frame half-extent. The room was then read the same
       way the module read its own: both axes, five perspectives, three dips, five frame ratios from
       a tall phone to a wide desk, a hundred places on the turn and the crease at either end of that
       window. A room of 0.40 still leaves 0.014 of a frame half-extent of the corner bare at the
       deepest camera and the biggest dip; 0.42 leaves nothing bare anywhere on the sweep. The whole
       crop is the two rooms together, and it is what the doors' framing publishes: a landed face
       stands the source cover-fit and centre-cropped by it. */
    var SEAM_REACH = 0.25;
    var SEAM_ROOM = 0.42;
    var CROP = BOX_CROP + SEAM_ROOM;

    /* THE CAMERA (box.js:273-278). Its distance is read in box half-widths and runs from a shallow
       eight — where the turn is nearly a fold — to a deep three, where the near corner is two thirds
       again the size of the far one. Below three the faces stop covering the frame at the crop above,
       so the range is the crop's own consequence and not a taste. The dip is how far the eye rides up
       and down through the turn; 0.12 of the frame's half-height is what the crop's margin pays
       for. */
    var CAM_FAR = 8.0, CAM_NEAR = 3.0, DIP_MAX = 0.12;

    /* THE TURN'S OWN RATE inside a quarter: v = f^p / (f^p + (1-f)^p) with p below (box.js:280-284).
       The rate is NOTHING at each landing and about a third again the mean in the middle, so the eye
       rests at every place it arrives at and the move never reads as a constant-speed spin — which is
       the stock transition's own signature, and the exemption the felt-change law grants this module
       by the name `landing-paced`. */
    var EASE_P = 1.9;

    /* HOW FAR A FACE'S PICTURE TRAVELS inside one quarter, in the face's own uv, and how deep the
       finger joint bites, in frame units (box.js:286-290). The travel is bounded by the crop's own
       headroom, so 0.05 of uv is well inside what the face carries. */
    var AMP = 0.05;
    var FING_MAX = 0.09;

    /* HOW MANY FINGERS STAND ALONG THE CREASE, and whose number it is (box.js:291-298). This is one
       of the two numbers of the box's geometry the WORKS themselves own: a score derives it from the
       departing work's own measured repeat across the crease — the same measurement grid-colour takes
       as countFrom, the collection's own in lab/data/step3-grid-derivation.json — so the SHAPE of the
       boundary is drawn by the work and not by the box. Below three it reads as one chunk taken out
       of the edge; above about fourteen it reads as a comb and stops being a joint. Seven is what the
       instrument stands at until a score names the work's own. */
    var FING_N = 7;

    /* HOW FAR A WORK MUST FALL INTO TWO REGIONS before its best line counts as a seam at all
       (box.js:300-328): the split must explain a fifth of how the work's own columns differ from one
       another. Measured on the six photographs the lab pages carry, that separates them into the ones
       with a line and the ones without — glassgrid splits at 0.62 explaining 0.89, pink-grid at 0.29
       explaining 0.48, cluster at 0.34 explaining 0.28, while towers, a single repeating facade,
       explains 0.03 and has no seam at all. Below the floor the crease stays where the box's own edge
       puts it and the reading says so out loud, rather than passing a made-up number off as the
       work's own. */
    var SEAM_FLOOR = 0.20;

    /* THE DEAD BANDS AT EITHER END OF THE HAND (box.js:481). Over the first and last five hundredths
       of the hand the box stands exactly landed: the hand is spent there and the standing face is the
       picture its source carries, to the point. Everything that moves through a quarter — the turn,
       the camera's dip, the crease's slide, the counter-motion and the joint's bite — is nothing
       inside these bands, which is what makes a door a door and not a checkpoint. */
    var FEEL_D0 = 0.05;

    /* THE FACES THE JOURNEY RUNS OVER. Two, and the reason is the header's: a cue carries an ordered
       pair, so two works are what stand on the faces, and an odd journey would land the visitor back
       on the departing work. The number is pinned rather than published as a handle. */
    var FACES = 2;

    // Face i's outward normal and first axis at rest, in the plane the turn happens in (box.js:499):
    // (n, u): (z, x) -> (-x, z) -> (-z, -x) -> (x, -z); the second face is the one that comes to the
    // front as the turn advances.
    var NRM = [[0, 1], [-1, 0], [0, -1], [1, 0]];
    var AXU = [[1, 0], [0, 1], [-1, 0], [0, -1]];
    // the face's own square, walked in the order the shader reads its two carriers in
    var CORNERS = [[-1, -1], [1, -1], [1, 1], [-1, 1]];

    // The score's die, read the way the module reads it, so one seeded score draws one picture
    // (box.js:245-250). A handle that is not a number is the one case the module answered with a
    // roll of its own; here it answers with nothing instead, because an instrument that rolls its
    // own die makes a seeded run draw two different pictures (§4.4b).
    function seedFrom(v) {
      var n = +v;
      if (!(n === n) || n === Infinity || n === -Infinity) return 0;
      var s = Math.sin(n) * 43758.5453;
      return (s - Math.floor(s)) * 8;
    }

    function ease(f) {
      var a = Math.pow(clamp(f, 0, 1), EASE_P), b = Math.pow(1 - clamp(f, 0, 1), EASE_P);
      return a / Math.max(a + b, 1e-9);
    }

    // WHERE THE HAND HAS BROUGHT THE TURN (box.js:486-493): which quarter, and how far into it, with
    // the dead bands taken off first and the quarter's own rate applied after.
    function journey(u) {
      var x = clamp((u - FEEL_D0) / (1 - 2 * FEEL_D0), 0, 1);
      var n = FACES - 1;
      var g = x * n;
      var j = Math.min(n - 1, Math.floor(g));
      var f = clamp(g - j, 0, 1);
      return { j: j, f: ease(f), raw: f, n: n };
    }

    // ONE TRAVELLING NUMBER, read on the diagnostic surface: how much of the whole journey the turn
    // has completed. The entry, the middle and the ending are the shape of its response.
    function feelOf(u) {
      var jj = journey(u);
      return (jj.j + jj.f) / Math.max(jj.n, 1);
    }

    // Cover-fit a work into the frame, and nothing beyond it. A face's own two sides always stand in
    // the frame's own ratio — the crop scales both by the same number and the axis swaps which of the
    // two is which — so the seating a face asks for IS the plain cover fit into the frame, and the
    // crop the doors publish is what the frame then sees of it.
    function fit(iw, ih, w, h) {
      var fa = w / Math.max(h, 1);
      var ia = iw / Math.max(ih, 1);
      if (ia > fa) return [fa / ia, 1, 0, 0];
      return [1, ia / fa, 0, 0];
    }

    // The plain three-by-three inverse the module carries (box.js:385-394), returning the nine
    // numbers as three rows of three, or nothing where the map cannot be inverted.
    function inv3(m) {
      var a = m[0], b = m[1], c = m[2], d = m[3], e = m[4], f = m[5], g = m[6], h = m[7], i = m[8];
      var A = e * i - f * h, B = -(d * i - f * g), C = d * h - e * g;
      var det = a * A + b * B + c * C;
      if (!det) return null;
      var s = 1 / det;
      return [A * s, (c * h - b * i) * s, (b * f - c * e) * s,
              B * s, (a * i - c * g) * s, (c * d - a * f) * s,
              C * s, (b * g - a * h) * s, (a * e - b * d) * s];
    }

    // ---- WHERE THE CREASE STANDS, AND WHOSE NUMBER THAT IS -----------------------------------------
    // The charter convicts «the screen-as-cube-face turn» and pardons in the same sentence «the WORK
    // folding into a solid along its own seams… the difference is whose structure draws the
    // boundary». That is one test with one subject — the boundary — and it has two halves, its shape
    // and its place. The fingers' COUNT is the shape and it comes from the work; this is the PLACE,
    // and it comes from the work too.
    //
    // The place is where the work falls into its two regions: the line along the turn's own direction
    // that best splits the work's columns (or its rows, when the crease lies flat) into two groups.
    // That is the question lab/cut-lines.py asks as `regions`, and the answer travels here as two
    // handles — `seam`, the line, and `seamScore`, how much of the difference between the work's own
    // columns that line explains. The module measured both for itself off the picture; an instrument
    // may not, because measuring means drawing the work into a surface of its own and counting, and
    // §1.2's fence leaves every surface to the host. So the measurement is named at the handle and
    // handed in by the score, which is where every other measured number in this engine already comes
    // from.
    //
    // BELOW THE FLOOR THE CREASE GOES BACK TO THE BOX'S OWN EDGE, and the reading says so. A work
    // that does not fall into two regions has no line to put a fold on, and inventing one would be
    // the convicted gesture with a number painted on it.
    function seamPlaceOf(st) {
      var score = typeof st.seamScore === "number" ? clamp(st.seamScore, 0, 1) : 0;
      if (score >= SEAM_FLOOR) {
        // The place is held inside the window the measurement itself searches — the middle half of
        // the work — because that is where a region line can be found and because the box is built
        // with room for exactly that travel and no more.
        return { at: clamp(typeof st.seam === "number" ? st.seam : 0.5,
                           0.5 - SEAM_REACH, 0.5 + SEAM_REACH),
                 score: score, measured: true, from: "the departing work's own region line" };
      }
      return { at: 0.5, score: score, measured: false,
               from: "the box's own edge — the work's region split stands under the floor" };
    }

    // ---- the grid one frame is drawn on ------------------------------------------------------------
    // The buffer the host is about to bind as `resolution`, with the CSS frame where it hands none
    // and a square where it hands neither. The instrument's whole geometry reads it: the box's own
    // half-sides are the frame's own two half-extents grown by the crop, so the frame's ratio is in
    // every corner the shader is handed. `drawn` says which of the two the reading below names, since
    // a reader told «a 780 x 1688 frame» would look for a device that has none.
    function gridOf(st) {
      var bw = Math.round(st.bufWidth), bh = Math.round(st.bufHeight);
      if (bw >= 1 && bh >= 1) return { w: bw, h: bh, drawn: true, given: true };
      var cw = Math.round(st.cssWidth), ch = Math.round(st.cssHeight);
      if (cw >= 1 && ch >= 1) return { w: cw, h: ch, drawn: false, given: true };
      return { w: 1, h: 1, drawn: false, given: false };
    }

    // ---- the numbers of one frame ------------------------------------------------------------------
    // Everything the shader gets beyond the seating of the two works is a pure function of the pose;
    // every number in the pose comes from a handle a score can drive. NOTHING HERE READS A CLOCK, and
    // no handle carries one: the module's own `t` was counted up by its frame loop and reached no
    // uniform, so the picture this instrument draws depends on the hand and on nothing else in time.
    // A handle a score can walk without moving the picture is noise in the score (§4.4b), so no
    // `clock` handle is published, and a seeded run repeats to the point for the same reason.
    //
    function posed(st) {
      var dial = clamp(st.mix, 0, 1);
      // WHICH WAY THE BOX TURNS, and therefore which way the crease lies. At 0 the faces travel
      // across the frame and the crease stands upright; at 1 they travel up the frame and the crease
      // lies flat. The `seam` handle is read along the same direction, which is why the two are one
      // decision and not two.
      var flat = clamp(typeof st.axis === "number" ? st.axis : 0, 0, 1) >= 0.5;
      var grid = gridOf(st);
      var aspect = grid.w / Math.max(grid.h, 1);
      var jj = journey(dial);
      // the box: half-side across the turn's plane, half-extent along its axis. Both are the frame's
      // own half-extents grown by the crop, which is what makes the frame a window in the middle of a
      // bigger box.
      var m = flat ? CROP : CROP * aspect;
      var side = flat ? CROP * aspect : CROP;
      var D = m * (CAM_FAR + (CAM_NEAR - CAM_FAR) * clamp(st.depth, 0, 1));
      var theta = (jj.j + jj.f) * Math.PI / 2;
      var co = Math.cos(theta), si = Math.sin(theta);
      // THE WINDOW EVERYTHING THAT MOVES RIDES. One sine over one quarter, nothing at both ends of
      // it: the camera's dip, the crease's slide, the counter-motion and the joint's bite all carry
      // it, which is the single reason every landing is exact.
      var win = Math.sin(Math.PI * jj.f);
      var dip = DIP_MAX * clamp(st.dip, 0, 1) * win;
      var seam = seamPlaceOf(st);
      // the crease travels up the frame when the box turns the faces up it and across when it turns
      // them across, so the slide follows the crease
      var w = (seam.at - 0.5) * 2 * win;
      var slide = flat ? [0, -w] : [w * aspect, 0];
      var c = D - m;

      function face(i) {
        var n = NRM[i % 4], au = AXU[i % 4];
        // a point of the face, before the turn: m·n + s·m·u along the plane, t·side along the axis
        function pt(s, tt) {
          var px = m * n[0] + s * m * au[0];        // across the turn's plane
          var pz = m * n[1] + s * m * au[1];        // into depth
          var X = px * co + pz * si;
          var Z = -px * si + pz * co;
          return flat ? { x: tt * side, y: X, z: Z } : { x: X, y: tt * side, z: Z };
        }
        var o = pt(0, 0), es = pt(1, 0), et = pt(0, 1);
        var Xs = es.x - o.x, Xt = et.x - o.x;
        var Ys = es.y - o.y, Yt = et.y - o.y;
        var Zs = es.z - o.z, Zt = et.z - o.z;
        // the map (s, t, 1) -> (screen·w, w), with the camera's height taken out of the screen
        var Hm = [c * Xs, c * Xt, c * o.x,
                  c * Ys, c * Yt, c * (o.y - dip),
                  -Zs, -Zt, D - o.z];
        // is the face turned toward the eye at all
        var nx = n[0] * co + n[1] * si, nz = -n[0] * si + n[1] * co;
        var nw = flat ? { x: 0, y: nx, z: nz } : { x: nx, y: 0, z: nz };
        var view = { x: -o.x, y: -o.y, z: D - o.z };
        var facing = nw.x * view.x + nw.y * view.y + nw.z * view.z;
        var cs = CORNERS.map(function (q) {
          var p = pt(q[0], q[1]);
          var k = c / Math.max(D - p.z, 1e-6);
          return [p.x * k + slide[0], (p.y - dip) * k + dip + slide[1]];
        });
        return { H: Hm, corners: cs, facing: facing, depth: D - o.z };
      }

      var A = face(jj.j), B = face(jj.j + 1);
      var invA = inv3(A.H), invB = inv3(B.H);
      // A face whose map cannot be inverted stands nowhere the eye can read it; its own screen quad
      // is what decides coverage, so the map is filled with the one that reads every point as the
      // face's own centre and the quad keeps it off the frame.
      if (!invA) invA = [0, 0, 0, 0, 0, 0, 0, 0, 1];
      var only = (!invB || B.facing <= 0 || Math.abs(jj.f) < 1e-6) ? 1 : 0;
      if (!invB) invB = invA;
      var off = AMP * win * clamp(typeof st.travel === "number" ? st.travel : 1, 0, 1);
      var fing = FING_MAX * clamp(st.lead, 0, 1) * win;
      var fingN = Math.round(clamp(typeof st.fingers === "number" ? st.fingers : FING_N, 3, 14));
      // THE CONTACT SHADOW'S GATE, out at every landing (box.js:695). It is walked up over the first
      // nine hundredths of the quarter and down over the last nine, so a face standing whole carries
      // no shade at all.
      var guard = clamp(typeof st.shade === "number" ? st.shade : 1, 0, 1)
                * smoothstep(0, 0.09, jj.f) * smoothstep(1, 0.91, jj.f);
      return {
        // the two inverse maps, a row of three to a carrier
        invA0: [invA[0], invA[1], invA[2], 0], invA1: [invA[3], invA[4], invA[5], 0],
        invA2: [invA[6], invA[7], invA[8], 0],
        invB0: [invB[0], invB[1], invB[2], 0], invB1: [invB[3], invB[4], invB[5], 0],
        invB2: [invB[6], invB[7], invB[8], 0],
        // the two screen quads, two corners to a carrier
        quadA0: [A.corners[0][0], A.corners[0][1], A.corners[1][0], A.corners[1][1]],
        quadA1: [A.corners[2][0], A.corners[2][1], A.corners[3][0], A.corners[3][1]],
        quadB0: [B.corners[0][0], B.corners[0][1], B.corners[1][0], B.corners[1][1]],
        quadB1: [B.corners[2][0], B.corners[2][1], B.corners[3][0], B.corners[3][1]],
        cam: [aspect, dip, slide[0], slide[1]],
        turn: [only, off, A.depth <= B.depth ? 1 : 0, guard],
        joint: [fing, fingN],
        seed: seedFrom(st.seed),
        // read on the diagnostic surface, bound to no uniform: what the hand came to, and the two
        // numbers the works themselves own
        hand: dial, quarter: jj.j, within: jj.f, raw: jj.raw,
        turnDeg: theta * 180 / Math.PI, window: win,
        camera: D / m, crop: CROP, turnRoom: BOX_CROP, seamRoom: SEAM_ROOM, faces: FACES,
        axis: flat ? "the crease lies flat" : "the crease stands upright",
        seamAt: seam.at, seamScore: seam.score, seamMeasured: seam.measured, seamFrom: seam.from,
        fingers: fingN, mask: clamp(typeof st.mask === "number" ? st.mask : 0, 0, 1),
        // the standing face at this door, and where its four corners stand when the box is landed
        stand: jj.f >= 0.5 ? jj.j + 1 : jj.j,
        landedCorners: landedCornersOf(m, side, flat),
        grid: grid,
      };
    }

    // WHERE THE STANDING FACE'S FOUR CORNERS STAND WHEN THE BOX IS LANDED, in frame units, derived
    // from the box's own two half-extents and nothing else. At a landing the standing face lies
    // square-on at the box's own near distance, where the projection's scale is exactly one, so its
    // corners are the box's half-extents themselves. This is written from first principles rather
    // than taken from the geometry above ON PURPOSE: it is what the door's reading measures the drawn
    // frame AGAINST, and a reference computed by the same arithmetic it is checking would agree with
    // a broken landing as readily as with a whole one.
    function landedCornersOf(m, side, flat) {
      return CORNERS.map(function (q) {
        return flat ? [q[1] * side, q[0] * m] : [q[0] * m, q[1] * side];
      });
    }

    // ---- THE DOOR THE INSTRUMENT READS FOR ITSELF --------------------------------------------------
    // His 18:00 architecture decision, carried in the U27 brief: the instrument reads its doors at
    // runtime on the actual buffer, and the report it hands back is the runtime truth; what the
    // manifest declares is only the claim. The meshing instrument answered that first
    // (pass-inst-gears.js) and the unfold instrument reads its own panel map the same way; this is
    // the same law read in this instrument's own unit, which is the BOX — its two faces over the
    // frame, and where the standing one stands.
    //
    // WHAT A DOOR ASKS OF A BOX. At either door one face stands square-on, filling the frame, at the
    // source cover-fit centre-cropped by the box's own crop, which is what the `framings` block
    // publishes. Three things carry that, and this reads all three ON THE BUFFER rather than
    // declaring them:
    //   · THE BOX COVERS THE FRAME. The crop is measured so that no point of the frame is ever left
    //     with no face standing on it. That is a claim about a GRID — whether a bare point falls
    //     between samples or on one — and it is walked at the buffer's own sample points instead of
    //     being asserted. What the walk publishes beside the count is how much frame the tightest of
    //     those points had TO SPARE, in points of the grid, so a crop trimmed toward its floor shows
    //     the margin closing long before anything goes bare.
    //   · THE STANDING FACE IS ON ITS LANDING. The turn is a whole quarter at a door, the camera is
    //     level and the crease's slide is nothing, so the standing face's four screen corners are the
    //     box's own half-extents. How far they stand from there — the greatest travel of any of the
    //     four, in points of the grid — is one number that catches a residual turn, a camera left off
    //     level, and a slide that did not rest, and it is a number about a SCREEN, so it is read in
    //     the screen's own points.
    //   · THE JUDGES' CHANNEL IS SHUT. `mask` draws the face map itself as colour, which is what it
    //     is for; left open at a door the frame is a false-colour map of the two faces and not the
    //     photograph at all.
    //
    // WHAT THIS READING FINDS, SAID PLAINLY. On every buffer the host can hand and every pose these
    // handles admit, the first two come out whole: at a door the hand is inside its own dead band, so
    // the turn is exactly a whole quarter and the window every travelling number rides is exactly
    // nothing. That is not a reason to leave the claim unread — it is the runtime truth this lane was
    // asked for, and it is published as the applied state below, where a suite reads it and a later
    // change to the dead bands, the window, the crop or the camera reddens against it. The one door
    // this instrument's own handles can spoil is the third, and it is refused.
    //
    // AND THERE IS NOTHING HERE TO HOLD. The meshing instrument holds a leaking size whole and the
    // unfold instrument holds a pair of panels flat, because in both a grid can show a fault that a
    // guard read in the grid's own units can close. A box has no such fault: the landing is exact by
    // construction rather than by a tolerance — the dead band spends the hand and the window is a
    // sine at its own zero — so anything this reading finds is a real fault that no widening closes,
    // and the refusal stands alone. `held` is therefore always nothing, and it says so rather than
    // carrying a guard that could never fire.
    var DOOR_SLIP = 0.5;   // points of the grid: half a point, inside which a sample cannot move
    // How much of the face map may stand in the frame at a door and it still BE the photograph: half
    // a level of 255, under anything the frame itself can carry. The charter's own door bar is 6 of
    // 255 over the canvas rect, and half a level is an eighth of that at one point.
    var DOOR_SHOW = 0.5 / 255;

    // The four straight edges of a screen quad and the least signed distance to them — FRAG's own
    // `side` and `inside`, carried here so the reading walks the very shape the shader draws.
    function sideOf(p, q, mid, x) {
      var nx = -(q[1] - p[1]), ny = q[0] - p[0];
      var len = Math.sqrt(nx * nx + ny * ny);
      var s = len < 1e-9 ? 1e-9 : len;
      nx /= s; ny /= s;
      var d = -(nx * p[0] + ny * p[1]);
      var turn = (nx * mid[0] + ny * mid[1] + d) < 0 ? -1 : 1;
      return turn * (nx * x[0] + ny * x[1] + d);
    }
    function insideOf(cs, x) {
      var mid = [0, 0], i;
      for (i = 0; i < 4; i++) { mid[0] += cs[i][0] / 4; mid[1] += cs[i][1] / 4; }
      var least = 1e9;
      for (i = 0; i < 4; i++) {
        least = Math.min(least, sideOf(cs[i], cs[(i + 1) % 4], mid, x));
      }
      return least;
    }
    function quadOf(v, which) {
      var q0 = which ? v.quadB0 : v.quadA0, q1 = which ? v.quadB1 : v.quadA1;
      return [[q0[0], q0[1]], [q0[2], q0[3]], [q1[0], q1[1]], [q1[2], q1[3]]];
    }

    // THE BOX, READ ON THE BUFFER THE SHADER WILL SAMPLE ON. The two screen quads are the ones the
    // shader is about to be handed, and the walk takes the buffer's own sample points: its four
    // corners, where the crop has the least to spare; the midpoints of its four edges; and the nine
    // points around its centre, where the crease crosses the frame mid-turn. Every one of them must
    // be claimed by one of the two faces.
    function boxReadOf(v, W, H) {
      var aspect = W / Math.max(H, 1);
      var qA = quadOf(v, 0), qB = quadOf(v, 1);
      var only = v.turn[0] >= 0.5;
      var reads = [], bare = 0, spare = 1e9, i, j;
      function walk(px, py) {
        var x = [(px / W) * 2 * aspect - aspect, 1 - (py / H) * 2];
        var dA = insideOf(qA, x);
        var dB = only ? -1e9 : insideOf(qB, x);
        var on = Math.max(dA, dB);
        if (on < 0) bare++;
        if (on < spare) spare = on;
        reads.push(on);
      }
      for (i = 0; i < 2; i++) {
        for (j = 0; j < 2; j++) { walk(i ? W - 0.5 : 0.5, j ? H - 0.5 : 0.5); }
      }
      walk(0.5, H * 0.5); walk(W - 0.5, H * 0.5); walk(W * 0.5, 0.5); walk(W * 0.5, H - 0.5);
      for (i = -1; i <= 1; i++) {
        for (j = -1; j <= 1; j++) { walk(W * 0.5 + i, H * 0.5 + j); }
      }
      // HOW FAR THE STANDING FACE STANDS FROM ITS OWN LANDING, in points of this grid. One frame unit
      // is half the grid's height in points, which is the same reading the shader's own `px` is
      // written in.
      var stand = v.stand === v.quarter ? qA : qB;
      var offPx = 0;
      for (i = 0; i < 4; i++) {
        var dx = stand[i][0] - v.landedCorners[i][0];
        var dy = stand[i][1] - v.landedCorners[i][1];
        offPx = Math.max(offPx, Math.sqrt(dx * dx + dy * dy) * H / 2);
      }
      return { walked: reads.length, bare: bare, sparePx: spare * H / 2, offPx: offPx,
               faces: v.faces, crop: v.crop, mask: v.mask, only: only ? 1 : 0 };
    }

    // THE DOOR, MEASURED. Null everywhere but at a door, since away from the doors a turning box is
    // the picture rather than a fault. The door is named by the manifest's own `doors` block: `mix`
    // at 0 is the entry door, where the frame is the departing work whole, and `mix` at 1 the exit
    // door, where it is the arriving one.
    function doorReadOf(v, st) {
      var want = st.mix === 0 ? 1 : (st.mix === 1 ? 0 : -1);
      if (want < 0) return null;
      var g = v.grid;
      if (!g.given) return null;
      var read = boxReadOf(v, g.w, g.h);
      read.grid = g;
      read.want = want;
      return read;
    }

    // THE REFUSAL, worded the way the host's own manifest refusals read: what is wrong, in this
    // instrument's own measured numbers, on the grid it was measured on.
    function doorWhyNoOf(read) {
      if (!read) return null;
      var g = read.grid, door = read.want ? "the entry" : "the exit";
      var work = read.want ? "departing" : "arriving";
      var where = " of a " + g.w + " x " + g.h + (g.drawn ? " buffer" : " frame");
      if (read.bare) {
        return door + " door leaks: the box leaves " + read.bare + " of the " + read.walked
             + " points this reading walked" + where + " with no face standing on them, where "
             + door + " door's own law asks for the " + work + " work at every point";
      }
      if (read.offPx >= DOOR_SLIP) {
        return door + " door leaks: the standing face stands " + read.offPx.toFixed(2) + " points"
             + where + " away from its own landing, so the frame is the " + work + " work seen off "
             + "its landing — turned, or under a camera that has not come back to rest — where "
             + door + " door's own law asks for that work standing square at every point";
      }
      if (read.mask >= DOOR_SHOW) {
        return door + " door leaks: the judges' own channel stands at " + read.mask.toFixed(6)
             + ", so the frame draws the face map — " + read.faces + " faces over a "
             + g.w + " x " + g.h + (g.drawn ? " buffer" : " frame")
             + " — instead of the " + work + " work, where " + door
             + " door's own law asks for the " + work + " work at every point";
      }
      return null;
    }

    // THE NUMBERS OF ONE FRAME, WITH ITS DOOR READ ON THE BUFFER BEING DRAWN. Away from a door this
    // is `posed` and nothing more: the reading is taken nowhere else. At a door it walks its own two
    // faces over the buffer and publishes what it read — how many points it walked, how many stood
    // bare, how much frame the tightest of them had to spare, and how far the standing face stands
    // from its own landing, all in points of the grid the shader will sample on.
    function values(st) {
      var v = posed(st);
      var read = doorReadOf(v, st);
      v.doorGrid = read ? read.grid : null;
      v.boxMap = read ? { walked: read.walked, bare: read.bare, sparePx: read.sparePx,
                          offPx: read.offPx, only: read.only, faces: read.faces,
                          crop: read.crop } : null;
      v.doorHeld = null;
      v.doorWhyNo = doorWhyNoOf(read);
      return v;
    }

    // THE SURFACE'S OWN CAMERA POSE. The box already reads the eye's lateral travel from the
    // measured crease and its own perspective construction; `posed` publishes that travel as the
    // two `cam` slide coordinates. They are zero at both doors because they ride the same sine
    // window as the dip and the turn, so this is a surface pose the host can own without moving
    // either exact hang. The carrier itself continues to travel through the measured DOM hang boxes;
    // this pose is only the motion riding on that physical carrier, never a second seating.
    function surfaceCameraPose(v) {
      return { panX: Number(v.cam[2]) || 0, panY: Number(v.cam[3]) || 0,
               logScale: 0, pitch: 0, yaw: 0, roll: 0, orbit: 0, tilt: 0, fov: null };
    }

    var manifest = {
      id: "boxfold", api: 1, arity: 2,
      // The frame comes apart into the two faces of one solid, the turn carries the eye from the one
      // to the other, and the arriving face lands whole.
      roles: ["disassembly", "mystery", "assembly"],
      // WHERE THIS STANDS ON THE CHARTER'S SHELF, and the reading is said to be derived. The module
      // carries no row in lab/data/module-contract.json — it postdates that table — so its level is
      // read off its own construction rather than carried from a record.
      //   · WORLD — the flat frame becomes one face of a solid standing in a space, seen through a
      //     real projection, with the eye riding up through the turn and sliding along it. What the
      //     visitor watches is a journey between places rather than something happening to a picture,
      //     which is the level the charter's shelf 17 keeps for a folded space.
      //   · CELL — the two faces. During the turn the frame is partitioned into two cells that meet
      //     at a finger joint, which is the panel the composer's `KIND_OF_MEASURE` reads out of a
      //     `regions` pivot.
      // CELL CONTENT is not claimed. Each face carries its own work and nothing inside a face changes
      // while it stands. TEXTURE and LIGHT-COLOUR are not claimed either: the contact shadow is the
      // one thing this instrument writes over a picture, and it lies along a cell's own edge rather
      // than over a field.
      levels: ["WORLD", "CELL"],
      // WHAT THIS INSTRUMENT CUTS ON, ADDED 2026-08-31 (cause A, item 5 — the reconciliation).
      // This file never declared the key: the composer's own `INSTRUMENTS.cuts` carried «panel»
      // for this instrument, read off nowhere in this file, and the manifest is the one home a
      // fact this small should ever have. `panel` is what the seam just below already says the
      // crease is — the box's own finger joint splits the frame into the two faces the fold hinges
      // between — so the declaration restates what this file already proves rather than adding a
      // fact.
      cuts: ["panel"],
      // WHERE THIS INSTRUMENT HAS A SEAM (§8's `seams` block). The crease between the two faces is a
      // PANEL edge — the box's own finger joint, where face A's coverage `dA` and face B's coverage
      // `dB` meet and the shader turns their difference into `cov` over exactly one point of the
      // drawing buffer, `px` (FRAG's own `float m = (dA - dB) * 0.5 + bite; float cov = clamp(0.5 +
      // m / px, 0.0, 1.0);`, with `px = 2.0 / max(uRes.y, 1.0)`). That is a HAIRLINE retouch and not
      // a cross-fade: the boundary itself is exact by construction — the finger joint's own bite is
      // a real geometric displacement of the crease, six parts a ladder and four the score's die
      // (box.js:180-186) — and what `px` rounds off is only the sign flip in the coverage's own
      // derivative at the crease, a fact about the sampling grid rather than a deliberate dissolve
      // between the two faces. `of` names no handle: the width stands at one point of the buffer
      // whatever `fingers` says, so it does not shrink as the joint's own count grows.
      seams: [{ kind: "panel", of: null, unit: "points of the drawing buffer" }],
      params: { axis: [0, 1], depth: [0, 1], dip: [0, 1], lead: [0, 1], fingers: [3, 14] },
      // EVERY handle a score can drive (§4.4b). `mix` is the dial — the module's own hidden `turn`
      // key, under the name every instrument in this engine gives it. The five below it are the
      // module's declared params that a pair can stand; `seam` and `seamScore` carry the crease's own
      // place; `shade` and `travel` are the module's two judge channels, resting where it rests them;
      // `seed` is the score's die and `mask` is the judges' channel.
      //
      // NO `clock` HANDLE, AND THAT IS A DECISION. The module counted a second of its own up in its
      // frame loop and no uniform ever read it: nothing in this picture moves with time, only with
      // the hand. A handle a score can walk without moving the picture is noise in the score, so none
      // is published, and the time that would have reached this instrument reaches it as nothing at
      // all.
      //
      // NO HANDLE HERE KEEPS A CLOCK OR A ROLL OF ITS OWN. The module rolled its own die where a
      // score named no seed (`Math.random()` in its own `seedFrom`); here that case answers with
      // nothing instead, because an instrument that rolls its own die makes a seeded score draw two
      // different pictures.
      handles: {
        // NO LEVEL FOR `mix`, `seed`, `shade`, `travel` OR `mask`: the crossing's own dial, the
        // score's die, and the fleet's own judge channels — none of them drive a structural level.
        mix: { min: 0, max: 1, def: 0, level: null },
        axis: { min: 0, max: 1, def: 0, kind: "enum", step: 1,
                names: { "0": "the crease stands upright", "1": "the crease lies flat" },
                unit: "which way the box turns",
                reads: "the banding axis lab/data/cut-lines.json recorded for the pivot — the "
                     + "direction the two works' own structure runs, so the crease crosses it",
                level: "WORLD" },
        depth: { min: 0, max: 1, def: 0.9, unit: "how deep the perspective is",
                 applied: { boxHalfWidthsAtNothing: CAM_FAR, boxHalfWidthsAtWhole: CAM_NEAR },
                 level: "WORLD" },
        dip: { min: 0, max: 1, def: 0.5, unit: "how far the eye rides up through a quarter",
               applied: { framesOfHalfHeightAtWhole: DIP_MAX, restsAt: "every landing" },
               level: "WORLD" },
        lead: { min: 0, max: 1, def: 0.5, unit: "how deep the finger joint bites",
                applied: { frameUnitsAtWhole: FING_MAX, restsAt: "every landing" },
                level: "CELL" },
        fingers: { min: 3, max: 14, def: FING_N, kind: "enum", step: 1,
                   unit: "how many fingers stand along the crease",
                   reads: "structure.grid.countFrom over the departing work's own frame side — the "
                        + "measured repeat that work carries ACROSS the crease, the collection's own "
                        + "in lab/data/step3-grid-derivation.json, which is the same number "
                        + "grid-colour derives its count from. It is the SHAPE of the boundary, and "
                        + "the work owns it",
                   level: "CELL" },
        // THE MEASUREMENT THE CREASE READS, published beside the handle's range the way the meshing
        // instrument publishes its own. This is the half of the charter's boundary test that asks
        // whose structure draws the boundary, and the answer has to be a measurement of the work or
        // it is no answer at all.
        seam: { min: 0.5 - SEAM_REACH, max: 0.5 + SEAM_REACH, def: 0.5,
                unit: "where along the turn's own direction the work falls into two regions",
                reads: "structure.regions from lab/cut-lines.py — the place along the turn's own "
                     + "direction that best splits the departing work's columns into two groups, "
                     + "read across the crease. The measure wins on 66 of the collection's 121 "
                     + "works, and it is the line the fold is placed on. The range is the "
                     + "measurement's own search window — cut-lines.py looks for the line in the "
                     + "middle half of the work — and the box is built with room for exactly that "
                     + "travel and no more",
                applied: { restsAt: "every landing", belowTheFloor: "the box's own edge",
                           roomInTheCrop: SEAM_ROOM },
                level: "CELL" },
        seamScore: { min: 0, max: 1, def: 0,
                     unit: "how much of the difference between the work's own columns that line "
                         + "explains",
                     // THIS SENTENCE NAMED THE WRONG FIELD until 2026-08-26. It read
                     // `structure.regions.score`, which the record does carry — but that is a
                     // different quantity from the one the `unit` two lines above describes and the
                     // one `SEAM_FLOOR` was set against. The floor's own calibration lists four
                     // works explaining 0.89, 0.48, 0.28 and 0.03, and those are the per-axis
                     // `explains` readings; the same record's `score` stands elsewhere entirely (on
                     // the fixture's own first work, `score` is 0.7401 while the line explains
                     // 0.1402 across and 0.6054 down). So the gate was published against a number
                     // it was never calibrated on. The floor has not moved and no behaviour changes
                     // here: what is corrected is the name the handle publishes for what it reads.
                     reads: "structure.regions.line.<axis>.explains from the same file — the axis "
                          + "being the one the crease runs along — which is the gate: a work whose "
                          + "line explains less of the difference between its own columns than the "
                          + "floor has no region line to fold along, and the crease goes back to "
                          + "the box's own edge with the reading saying so",
                     applied: { floor: SEAM_FLOOR },
                     level: "CELL" },
        shade: { min: 0, max: 1, def: 1, unit: "the contact shadow's own weight",
                 applied: { depthAtTheCrease: 0.34, pointsOfReach: 9, restsAt: "every landing" },
                 level: null },
        travel: { min: 0, max: 1, def: 1, unit: "the counter-motion each face's picture travels by",
                  applied: { uvAtWhole: AMP, restsAt: "every landing" },
                  level: null },
        seed: { min: 0, max: 8, def: 0, unit: "the ordered pair's own die",
                reads: "the score's own seed, which decides four parts in ten of the order the "
                     + "joint's fingers stand in; the other six are a plain ladder along the crease",
                level: null },
        // THE MEASUREMENT THIS HANDLE IS READ AGAINST AT A DOOR. `readAtADoor` says what is read
        // (this instrument's own two faces, walked at the buffer's own sample points), on which grid
        // (the drawing buffer the host binds, with the CSS frame where it hands none), what the
        // reading is counted in, and that there is no hold — a box's landing is exact by construction
        // rather than by a tolerance, so a door this reading finds a fault at is refused outright.
        mask: { min: 0, max: 1, def: 0,
                applied: { readAtADoor: { points: DOOR_SLIP, readOn: "the drawing buffer",
                                          reads: "landing",
                                          measures: "this instrument's own two faces over the frame, "
                                                  + "walked at the buffer's own sample points, and "
                                                  + "the standing face's own travel from its landing",
                                          held: null } },
                level: null },
      },
      neutrals: { a: 0, b: 1 },
      doors: { in: { handle: "mix", value: 0, work: "a" },
               out: { handle: "mix", value: 1, work: "b" } },
      // BOTH DOORS FRAME ALIKE, AND BOTH ARE CROPPED BY THE BOX'S OWN CROP. A face carries its source
      // cover-fit over the whole face and the face is larger than the frame by the crop, so a landed
      // face is the source cover-fitted and centre-cropped by that number. It is the price the
      // coverage law is paid with, and it is published here rather than left for the frame to reveal.
      framings: { "0": { coverCrop: CROP }, "1": { coverCrop: CROP } },
      drivers: ["progress", "cueProgress", "time", "velocity", "capability", "noise", "static",
                "curve", "spline", "map", "add", "multiply", "mix", "clamp", "hold", "segment",
                "ramp", "slew", "oscillate", "node"],
      // The explicit surface contract P3 starts with. The two faces are one typed carrier, its
      // anchor is the host's measured hang, and its local camera is the box's own crease travel.
      // Entry and exit name the two exact door states the box already reads on its drawing buffer.
      surface: { type: "two-face-fold", anchor: "measured-hang", tessellation: { faces: FACES },
                 cameraAuthority: "own", entry: { mix: 0, work: "a", pose: "flat" },
                 exit: { mix: 1, work: "b", pose: "flat" } },
      camera: { needs: "none", authority: "own" },
      gl: { preserveDrawingBuffer: false },
      // WHAT THIS INSTRUMENT WRITES WHERE ITS OWN MATTER IS ABSENT (§7's coverage law, and the
      // per-instrument specification in docs/design/COVERAGE.md). It is absent nowhere. The crop is
      // measured so the two faces cover the frame at every angle of the turn, so the alpha is the
      // constant 1, said as a decision. Under the placement rule this instrument is lawful as the
      // lowest cue of a stack and as a whole one-cue score.
      coverage: { writes: false,
                  how: "the box is built larger than the frame by the room the turn needs — the "
                     + "reciprocal of the worst angle, with a margin for the camera's dip — plus the "
                     + "room the crease's own travel onto the work's region line needs, so the two "
                     + "visible faces cover the frame at every point of the turn and the alpha is "
                     + "the constant 1; at a door the box's own reading walks the buffer's sample "
                     + "points and refuses a door where any of them stands with no face on it" },
      // The neutral pose is the ENTRY DOOR — `mix` at 0, the value the `doors` block above names — so
      // the frame keys the host reads off it at registration include the door's own record.
      neutralPose: { mix: 0, axis: 0, depth: 0.9, dip: 0.5, lead: 0.5, fingers: FING_N,
                     seam: 0.5, seamScore: 0, shade: 1, travel: 1, seed: 0, mask: 0,
                     reduced: false, cssWidth: 1000, cssHeight: 1000 },
      passes: [{
        program: "boxfold", vert: VERT, frag: FRAG, position: "aPos",
        uniforms: [
          { name: "uA", type: "sampler2D", source: "textureA" },
          { name: "uB", type: "sampler2D", source: "textureB" },
          { name: "uFitA", type: "vec4", source: "fitA" },
          { name: "uFitB", type: "vec4", source: "fitB" },
          { name: "uRes", type: "vec2", source: "resolution" },
          { name: "uInvA0", type: "vec4", source: "frame:invA0" },
          { name: "uInvA1", type: "vec4", source: "frame:invA1" },
          { name: "uInvA2", type: "vec4", source: "frame:invA2" },
          { name: "uInvB0", type: "vec4", source: "frame:invB0" },
          { name: "uInvB1", type: "vec4", source: "frame:invB1" },
          { name: "uInvB2", type: "vec4", source: "frame:invB2" },
          { name: "uQuadA0", type: "vec4", source: "frame:quadA0" },
          { name: "uQuadA1", type: "vec4", source: "frame:quadA1" },
          { name: "uQuadB0", type: "vec4", source: "frame:quadB0" },
          { name: "uQuadB1", type: "vec4", source: "frame:quadB1" },
          { name: "uCam", type: "vec4", source: "frame:cam" },
          { name: "uTurn", type: "vec4", source: "frame:turn" },
          { name: "uJoint", type: "vec2", source: "frame:joint" },
          { name: "uSeed", type: "float", source: "frame:seed" },
          { name: "uMask", type: "float", source: "handle:mask" },
        ],
      }],
      // The instrument allocates nothing of its own: it spends the two source-texture slots the host
      // already holds and the one programme the host builds from this manifest. The module's own
      // canvas, its context, its two textures and its own frame loop are what this port does without.
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
                   programs: 1, passes: 1, bytesEstimate: 2000248, variant: "lean" },
                   standard: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0,
                               programs: 1, passes: 1, bytesEstimate: 8000248,
                               variant: "standard" },
                   rich: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                           passes: 1, bytesEstimate: 32000248, variant: "rich" } },
      capabilities: ["webgl2"],
      decline: ["one work only", "a source that never decoded"],
      provenance: { labPath: "lab/effects/box.js", commit: "11e2db4",
                    sha256: "8d57315003f0bbc1e5c430b15db9504bd62c167c1a6c875defc2d57df6b8f8c4" },
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
      suits: { reads: ["structure.regions.score", "the panel element sets"],
               how: "the crease is placed on a work's own measured region line, so the fit is the "
                  + "region reading of the better-divided work; it is nothing where neither work "
                  + "falls into panels a solid could be built from, since a solid with one face is "
                  + "no solid" },
      readiness: "production-ready",
    };

    var live = false;
    return {
      name: "boxfold",
      manifest: manifest,
      values: values,
      fit: fit,
      feel: feelOf,
      prepare: function (o) {
        if (!o.sources) return { take: false, why: "the box instrument needs both works" };
        if (!o.cue) return { take: false, why: "no cue names it" };
        return { take: true };
      },
      start: function () { live = true; },
      // The pose the shader draws. The module's canvas, its frame loop and its own measurement of the
      // seam are gone, so every number here comes from a handle a score drives or from the frame the
      // host is about to bind.
      //
      // A DOOR THIS INSTRUMENT CANNOT KEEP WHOLE IS REFUSED RATHER THAN DRAWN. The door law is the
      // instrument's own claim, so the instrument is what answers for it: at either door it walks its
      // own two faces over the buffer the host is about to bind and, where a point of that grid
      // stands with no face on it, where the standing face stands off its own landing further than a
      // sample can move, or where the judges' channel is left open, it hands the host the reason with
      // the measured numbers in it instead of drawing a door that is not the photograph. The host
      // recovers the transaction on that reason and the walk's own glide carries the visitor, which
      // is the product's own behaviour with no renderer.
      frame: function (st) {
        if (!live) return;
        var h = st.handles;
        var pose = {
          mix: h.mix, axis: h.axis, depth: h.depth, dip: h.dip, lead: h.lead, fingers: h.fingers,
          seam: h.seam, seamScore: h.seamScore, shade: h.shade, travel: h.travel,
          seed: h.seed, mask: h.mask, reduced: st.reduced,
          cssWidth: st.viewport.w, cssHeight: st.viewport.h,
          // THE GRID THE SHADER WILL SAMPLE ON, carried into the pose so the geometry is built for
          // the frame the host is about to bind as `uRes` and the door is read on it rather than on
          // the CSS frame around it. The host settles it from the device ratio and its own resolution
          // step, so it moves while a pass plays and each door is read on the grid standing at that
          // door's own instant.
          bufWidth: st.viewport.bufferW, bufHeight: st.viewport.bufferH,
        };
        // The host's authority handoff reads exactly this pose. It is a pure reading of the same
        // box state the shader receives, so the host camera and the folded surface cannot drift
        // onto two independently invented paths.
        var surface = posed(pose);
        if (st.reportPose) st.reportPose(surfaceCameraPose(surface));
        // AT A DOOR THE INSTRUMENT SAYS WHAT IT APPLIED, and says it before it refuses. The reading is
        // taken on the buffer this frame is drawn on, so it is the run-time truth his 18:00 decision
        // asks for. `request` is the travel a landing asks of the standing face — none — and
        // `applied` is the travel this grid actually shows, so `moved` is the two read against each
        // other in the grid's own points.
        if (h.mix === 0 || h.mix === 1) {
          var v = values(pose);
          if (st.reportApplied) {
            st.reportApplied({
              door: h.mix === 0 ? "in" : "out",
              buffer: [pose.bufWidth, pose.bufHeight],
              reads: "landing", request: 0,
              applied: v.boxMap ? v.boxMap.offPx : null,
              moved: v.boxMap ? v.boxMap.offPx : null,
              unit: "points of the drawing buffer",
              // What the box itself was doing over the frame at this door: how many of the walked
              // points stood with no face on them, and how much frame the tightest of them had to
              // spare, so a door held whole says so about the crop as well as about the landing.
              bare: v.boxMap ? v.boxMap.bare : null,
              sparePx: v.boxMap ? v.boxMap.sparePx : null,
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
    instrument: boxInstrument(),
  });
})();
