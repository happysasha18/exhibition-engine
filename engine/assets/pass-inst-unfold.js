/*!pass-inst-unfold.js*/
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
  // THE UNFOLD INSTRUMENT (§8) — lab/effects/unfold.js carried across
  // ================================================================================================
  // WHAT THE VISITOR SEES. One work stands whole and fills the frame. It folds shut along its own
  // mirrored panels until what is left standing, filling the frame again, is the single photograph
  // it was cut from. That standing photograph is where the two works meet: across eight hundredths
  // of the hand the frame holds one flat picture and the first work's quarter gives way to the
  // second's. Then the second work opens out along the same seams and stands whole.
  //
  // WHY IT STANDS HERE. The composer's own census counts 1 296 declined pairs whose pivot asks for
  // an instrument that cuts on PANELS — for `region_dissolve` and `object_reveal` — which is the
  // largest single road to variety the collection is waiting on
  // (lab/data/sceneplans/index.json, declinesByReason, read 2026-08-17). A further 866 travelling
  // axes are dropped for the same want. This instrument cuts the frame into its own panels and is
  // what those plans name.
  //
  // WHAT CAME OVER: the growth law that keeps the frame filled at every point of the travel, the
  // room the lean needs and the room the corner needs, the viewing distance, the panel turn, the
  // point at which a turned panel is counted gone, the mirror swap and the degrees it takes, the
  // stagger between the two pairs, the shades, the creases, the backing, the lean, and the measured
  // response curve at its twenty-one marks. WHAT STAYED BEHIND: its own DOM stage, its panel
  // elements, its gradients, its pointer listeners, its own rAF clock and its own breath (§1.2's
  // fence, and §4.4b for the breath — a handle that keeps a clock of its own makes a seeded score
  // draw two different pictures).
  //
  // ------------------------------------------------------------------------------------------------
  // THE ONE THING THAT HAD NO WEBGL SHAPE, AND THE SHAPE IT WAS GIVEN
  // ------------------------------------------------------------------------------------------------
  // Every instrument landed before this one came from a lab module that already held a WebGL context
  // and a fragment shader, so the port carried a shader across. This module holds none: it draws with
  // CSS 3D — a stage with a perspective, a sheet, four hinged panels, two faces on each of three of
  // them, four gradient shades and three gradient creases — and the browser's own compositor is what
  // projects them. On that reading it was unregistrable, since §7 supplies a manifest with passes and
  // uniforms and nothing else, and a manifest with no pass is refused by name (`manifestWhyNo`:
  // "declares no pass").
  //
  // THE SHAPE. A CSS 3D transform chain is affine in the panel's own two coordinates and the
  // perspective divides once, so the map from a point of a panel to a point of the frame is a
  // HOMOGRAPHY — and a homography is invertible. The shader therefore reads the chain BACKWARDS: for
  // one point of the frame it solves, for each panel, the two-by-two system that says where on that
  // panel the point falls, keeps the panels the point actually lands on, and takes the one nearest
  // the eye. The arithmetic of the chain is the module's own, term for term; only its direction is
  // reversed. So the instrument declares one pass, thirteen uniforms bound by name, and needs no
  // second slot, no framebuffer and no extra texture.
  //
  // WHERE THE SHEET'S OWN SIZE IS KNOWN. The module cover-fits the file over the mount and cuts the
  // sheet into quarters, so the sheet is exactly the seating the host already computes and hands down
  // as `fitA`/`fitB`. The shader recovers the sheet's width and height from that seating and the
  // frame's own two numbers, and every measurement written in the module's units — one point, two
  // points, the mount's width and height — is written here in the same units against `resolution`.
  // That is why the growth law, the corner's own foreshortening and the viewing distance stand in the
  // shader: they read the frame's size, and the pose values below cannot.
  //
  // ------------------------------------------------------------------------------------------------
  // A ONE-WORK MODULE PLAYED AS A CROSSING
  // ------------------------------------------------------------------------------------------------
  // lab/data/module-contract.json records `unfold` as `needsTwoWorks: false`, and the module takes one
  // picture. A cue of this engine carries two works and two doors (§8: `neutrals`, `doors`), so the
  // port had to say where the second work enters. It enters at the one instant the module's own
  // construction offers: the far door, where the sheet stands closed and the frame holds a single flat
  // quarter of the file at exactly the framing the whole work stood at. Both works reach that instant
  // as one flat full-frame picture, so the exchange between them is a dissolve of two flat pictures
  // and nothing is folded while it happens.
  //
  // The hand therefore runs: the first work folds shut over the first forty-six hundredths, the two
  // works exchange across the eight hundredths in the middle, and the second work opens out over the
  // last forty-six. The module's own response curve is applied to each half of the hand, so equal
  // movements of the hand are equal felt change on both sides of the exchange, which is the whole
  // point of the curve. HOLD is the port's own number and the only one that is; every other constant
  // below is the module's.
  //
  // ------------------------------------------------------------------------------------------------
  // THE COVERAGE: THIS INSTRUMENT FILLS THE FRAME
  // ------------------------------------------------------------------------------------------------
  // §7's coverage law of 12:40 asks every instrument to say where its own matter is absent. Here it is
  // absent nowhere, and that is the module's own repair of 2026-08-13: the sheet is the file COVER-
  // fitted, and the growth law grows it by exactly what each turning panel gives up, so the standing
  // picture covers the frame at every point of the travel and nothing ever fades. The declaration is
  // `writes: false`, which under the placement rule (§8 as amended 14:05, and `coverageWhyNo`) makes
  // it lawful as the LOWEST cue of a stack and as a whole one-cue score. The composer's census counts
  // 1 320 plans declined for having no such ground, so the same port answers that want too.
  function unfoldInstrument() {
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
      // the cosine and sine of each pair's own turn: the standing hinge, then the lying one
      "uniform vec4 uTurn;",
      // how much of a panel still reaches past its hinge, and how far into its turn each pair is
      "uniform vec4 uReach;",
      // the lean's gate, the viewing distance, the four-panel flag, and the backing's weight
      "uniform vec4 uForm;",
      // the sheet's three lean angles in radians, and how far the mirror has come on
      "uniform vec4 uLean;",
      // the four shades: the standing panel, the turning one, and the two below them
      "uniform vec4 uShade;",
      // the three creases, and how far the exchange between the two works has come
      "uniform vec4 uCrease;",
      // the judges' handle: the panel map as colour
      "uniform float uMask;",
      // THE ROOM THE LEAN NEEDS, and the room the CORNER needs on top of it (unfold.js:42, :47). Both
      // are the module's own numbers and both are nothing at either door, because nothing leans and
      // nothing turns there.
      "const float EDGE = 1.16;",
      "const float PULL = 1.8;",
      // The sheet's own lean, applied to one vector: rotateZ, then rotateY, then rotateX, which is
      // the order a CSS transform list composes in (unfold.js:383).
      "vec3 stood(vec3 v){",
      "  float cx = cos(uLean.x), sx = sin(uLean.x);",
      "  float cy = cos(uLean.y), sy = sin(uLean.y);",
      "  float cz = cos(uLean.z), sz = sin(uLean.z);",
      "  vec3 p = vec3(v.x * cz - v.y * sz, v.x * sz + v.y * cz, v.z);",
      "  p = vec3(p.x * cy + p.z * sy, p.y, -p.x * sy + p.z * cy);",
      "  return vec3(p.x, p.y * cx - p.z * sx, p.y * sx + p.z * cx);",
      "}",
      // WHERE ONE POINT OF THE FRAME FALLS ON ONE PANEL. The panel's plane is `a + bu·u + bv·v`, the
      // perspective divides by `1 - z/d`, and the pair (u, v) is therefore the solution of a two-by-two
      // system rather than the result of a search. `z` comes back with it, which is what decides which
      // panel the eye sees where two of them cover one point.
      "bool lands(vec2 s, vec3 a, vec3 bu, vec3 bv, float d, vec2 lim, out vec2 uv, out float z){",
      "  vec2 c1 = vec2(bu.x + s.x * bu.z / d, bu.y + s.y * bu.z / d);",
      "  vec2 c2 = vec2(bv.x + s.x * bv.z / d, bv.y + s.y * bv.z / d);",
      "  float k = 1.0 - a.z / d;",
      "  vec2 r = vec2(s.x * k - a.x, s.y * k - a.y);",
      "  float det = c1.x * c2.y - c2.x * c1.y;",
      "  float safe = abs(det) < 1e-9 ? 1e-9 : det;",
      "  uv = vec2(r.x * c2.y - c2.x * r.y, c1.x * r.y - r.x * c1.y) / safe;",
      "  z = a.z + bu.z * uv.x + bv.z * uv.y;",
      "  return abs(det) > 1e-9 && uv.x >= 0.0 && uv.y >= 0.0 && uv.x <= lim.x && uv.y <= lim.y;",
      "}",
      // A face reads the file at the sheet's own coordinates, because the sheet IS the file: the
      // module sets the background to the whole file at the sheet's size (unfold.js:151).
      "vec3 pane(sampler2D tex, vec2 q, vec2 sz){ return texture2D(tex, clamp(q / sz, 0.0, 1.0)).rgb; }",
      // ONE WORK'S SHEET, WHOLE. Everything below is the module's own render() read backwards.
      "vec3 sheet(sampler2D tex, vec4 fit, out vec3 judge){",
      "  float aspect = uRes.x / max(uRes.y, 1.0);",
      "  float pt = 1.0 / max(uRes.y, 1.0);",
      // the sheet, cover-fitted over the frame: the seating the host applied, read backwards
      "  vec2 SZ = vec2(aspect / max(fit.x, 1e-4), 1.0 / max(fit.y, 1e-4));",
      "  float four = step(0.5, uForm.z);",
      "  float CW = SZ.x * 0.5;",
      "  float CH = four > 0.5 ? SZ.y * 0.5 : SZ.y;",
      "  float cY = uTurn.x, sY = uTurn.y, cX = uTurn.z, sX = uTurn.w;",
      "  float rY = uReach.x, rX = uReach.y;",
      "  float reachR = CW * rY, reachB = CH * rX;",
      "  float persp = uForm.y;",
      // A TURNED PANEL IS COUNTED FOR WHAT IT COVERS ON THE SCREEN (unfold.js:340-347): the corner
      // carried away by both turns at once is drawn smaller, and counting the plain cosine there opened
      // a triangle of bare frame.
      "  float deep = 2.0 * persp;",
      "  float corner = deep / (deep + sY + (CH / CW) * sX);",
      "  float extX = (CW - reachR) * 0.5 + reachR * corner;",
      "  float extY = (CH - reachB) * 0.5 + reachB * corner;",
      // THE GROWTH LAW (unfold.js:323-330): what a panel gives up by turning, the sheet takes back by
      // growing, so no margin can open at any point of the travel.
      "  float room = 1.0 + (EDGE - 1.0) * uForm.x + PULL * (1.0 - corner) * rY * rX;",
      "  float sc = room * max(max(aspect / (2.0 * extX), 1.0 / (2.0 * extY)), 1.0);",
      "  float d = persp * SZ.x * sc;",
      "  vec2 slide = vec2((CW - reachR) * 0.5, four > 0.5 ? (CH - reachB) * 0.5 : 0.0);",
      "  vec2 s = vec2(vUv.x * aspect - aspect * 0.5, vUv.y - 0.5);",
      // the three bases a panel's own two coordinates run along, once the sheet's lean is applied
      "  vec3 e0 = stood(vec3(sc, 0.0, 0.0));",
      "  vec3 e1 = stood(vec3(0.0, sc, 0.0));",
      "  vec3 eY = stood(vec3(cY * sc, 0.0, -sY));",
      "  vec3 eX = stood(vec3(0.0, cX * sc, -sX));",
      "  vec3 eXY = stood(vec3(-sX * sY * sc, cX * sc, -sX * cY));",
      "  vec2 mid = SZ * 0.5;",
      "  vec3 oTL = stood(vec3((slide - mid) * sc, 0.0));",
      "  vec3 oTR = stood(vec3((slide + vec2(CW, 0.0) - mid) * sc, 0.0));",
      "  vec3 oBL = stood(vec3((slide + vec2(0.0, CH) - mid) * sc, 0.0));",
      "  vec3 oBR = stood(vec3((slide + vec2(CW, CH) - mid) * sc, 0.0));",
      "  vec2 uTL, uTR, uBL, uBR, uSh;",
      "  float zTL, zTR, zBL, zBR, zSh;",
      // A face runs one point past its hinge, so the panels meet with no hairline (unfold.js:172-175).
      "  float ey = four > 0.5 ? pt : 0.0;",
      "  bool hTL = lands(s, oTL, e0, e1, d, vec2(CW + pt, CH + ey), uTL, zTL);",
      "  bool hTR = lands(s, oTR, eY, e1, d, vec2(CW, CH + ey), uTR, zTR);",
      "  bool hBL = lands(s, oBL, e0, eX, d, vec2(CW + pt, CH), uBL, zBL);",
      "  bool hBR = lands(s, oBR, eY, eXY, d, vec2(CW, CH), uBR, zBR);",
      "  bool hSh = lands(s, oTL, e0, e1, d, SZ, uSh, zSh);",
      "  hBL = hBL && four > 0.5;",
      "  hBR = hBR && four > 0.5;",
      // THE PANEL'S OWN QUARTER, AND THE MIRROR OVER IT. Flat, a panel is its own quarter of the work;
      // MIRROR degrees into its turn it is the mirror of the quarter the sheet closes onto
      // (unfold.js:398-401). The standing panel IS that quarter, so it carries one face and never swaps.
      "  vec3 cTL = pane(tex, uTL, SZ);",
      "  vec3 cTR = mix(pane(tex, vec2(CW + uTR.x, uTR.y), SZ),",
      "                 pane(tex, vec2(CW - uTR.x, uTR.y), SZ), uLean.w);",
      "  vec3 cBL = mix(pane(tex, vec2(uBL.x, CH + uBL.y), SZ),",
      "                 pane(tex, vec2(uBL.x, CH - uBL.y), SZ), uLean.w);",
      "  vec3 cBR = mix(pane(tex, vec2(CW + uBR.x, CH + uBR.y), SZ),",
      "                 pane(tex, vec2(CW - uBR.x, CH - uBR.y), SZ), uLean.w);",
      // THE SHADES a panel catches as it swings away from the light. Each runs across its own panel
      // from the module's own opening weight to full black (unfold.js:186-192).
      "  cTL *= 1.0 - uShade.x * (0.28 + 0.72 * clamp(uTL.x / CW, 0.0, 1.0)) * step(uTL.x, CW) * step(uTL.y, CH);",
      "  cTR *= 1.0 - uShade.y * (0.28 + 0.72 * clamp(uTR.x / CW, 0.0, 1.0)) * step(uTR.y, CH);",
      "  cBL *= 1.0 - uShade.z * (0.30 + 0.70 * clamp(uBL.y / CH, 0.0, 1.0)) * step(uBL.x, CW);",
      "  cBR *= 1.0 - uShade.w * (0.30 + 0.70 * clamp(uBR.y / CH, 0.0, 1.0));",
      // THE CREASES light up as they open and go out with the panel whose turn opens them. Each is two
      // points wide and brightest down its middle (unfold.js:193-200).
      "  float band = 2.0 * pt;",
      "  float tHL = (uTL.y - (CH - pt)) / band;",
      "  cTL = mix(cTL, vec3(1.0), clamp(uCrease.x * 0.85 * max(0.0, 1.0 - abs(2.0 * tHL - 1.0))",
      "                                 * step(uTL.x, CW), 0.0, 1.0));",
      "  float tHR = (uTR.y - (CH - pt)) / band;",
      "  cTR = mix(cTR, vec3(1.0), clamp(uCrease.y * 0.85 * max(0.0, 1.0 - abs(2.0 * tHR - 1.0)), 0.0, 1.0));",
      // WHICH PANEL THE EYE SEES. The three turning panels are sorted by their own depth; the sheet's
      // backing stands at the sheet's own plane, in front of everything that has turned away; and the
      // standing panel is laid down after the backing, which is the order the module builds them in.
      "  vec3 col = vec3(0.0);",
      "  float z = 0.0, code = 0.0;",
      "  vec2 loc = vec2(0.0);",
      "  bool got = false;",
      "  if (hTR) { col = cTR; z = zTR; code = 0.50; loc = uTR / vec2(CW, CH); got = true; }",
      "  if (hBL && (!got || zBL > z)) { col = cBL; z = zBL; code = 0.75; loc = uBL / vec2(CW, CH); got = true; }",
      "  if (hBR && (!got || zBR > z)) { col = cBR; z = zBR; code = 1.00; loc = uBR / vec2(CW, CH); got = true; }",
      "  if (hSh) {",
      "    vec3 back = pane(tex, uSh, SZ);",
      "    if (!got) { col = back; z = zSh; }",
      "    else if (zSh > z + 1e-6) { col = mix(col, back, uForm.w); }",
      "  }",
      "  if (hTL) { col = cTL; code = 0.25; loc = uTL / vec2(CW, CH); got = true; }",
      // The standing crease lies on the sheet itself and is drawn last of all (unfold.js:231).
      "  if (hSh) {",
      "    float tV = (uSh.x - (CW - pt)) / band;",
      "    col = mix(col, vec3(1.0), clamp(uCrease.z * 0.85 * max(0.0, 1.0 - abs(2.0 * tV - 1.0))",
      "                                   * step(uSh.y, CH), 0.0, 1.0));",
      "  }",
      // THE PANEL MAP, the judges' own frame: which panel stands at this point of the frame and where
      // in it. It is black exactly where no panel stands, so a row reads off the picture whether the
      // growth law kept its promise, and it carries no coverage of its own because what it is for is
      // to be read as colour.
      "  judge = vec3(code, clamp(loc.x, 0.0, 1.0), clamp(loc.y, 0.0, 1.0));",
      "  return col;",
      "}",
      "void main(){",
      "  vec3 jA, jB, judge, col;",
      // THE EXCHANGE. Outside the hold one work's sheet is drawn and the other is never sampled; inside
      // it both stand closed, flat and full-frame, and the frame is the two quarters dissolving.
      "  if (uCrease.w <= 0.0) { col = sheet(uA, uFitA, judge); }",
      "  else if (uCrease.w >= 1.0) { col = sheet(uB, uFitB, judge); }",
      "  else {",
      "    vec3 ca = sheet(uA, uFitA, jA);",
      "    vec3 cb = sheet(uB, uFitB, jB);",
      "    col = mix(ca, cb, uCrease.w);",
      "    judge = mix(jA, jB, uCrease.w);",
      "  }",
      "  col = mix(col, judge, uMask);",
      // THE COVERAGE: the alpha is the constant 1, and it is a decision rather than a default. The
      // growth law fills the frame with picture at every point of the travel, so this instrument has no
      // absence to publish and stands as the ground a stack is laid on.
      "  gl_FragColor = vec4(col, 1.0);",
      "}",
    ].join("\n");

    var DEG = Math.PI / 180;

    function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
    function smooth(x) { x = clamp(x, 0, 1); return x * x * (3 - 2 * x); }
    function mix(a, b, t) { return a + (b - a) * t; }
    function smoothstep(a, b, x) { return smooth((x - a) / (b - a)); }

    // THE MODULE'S OWN CONSTANTS, carried digit for digit (unfold.js:28-78).
    var MAXA = 84;             // degrees a panel swings before it stands edge-on
    var HOME = 80;             // where a turned panel is counted gone by the growth law
    var MIRROR = 14;           // degrees of its own turn a panel takes to take on its mirror
    var PERSP_FLAT = 4.4, PERSP_DEEP = 2.6;   // the two ends of the viewing distance
    var HOME_C = Math.cos(HOME * DEG);
    function reachOf(c) { return Math.max(0, (c - HOME_C) / (1 - HOME_C)); }

    // THE PORT'S OWN ONE NUMBER. How much of the hand the closed sheet stands for, and therefore where
    // the two works exchange. It is centred on the middle of the hand, so the two halves are equal and
    // the module's own curve runs once over each. The exchange has to sit entirely inside the rest at
    // fold 1, because that is the only instant at which both works stand as one flat full-frame picture
    // and a dissolve between them shows no fold at all. Eight hundredths is that rest, wide enough to
    // read as a held photograph at the pass durations this engine runs — half a second at 6.5 s — and
    // narrow enough that the fold itself keeps the rest of the hand.
    var HOLD = 0.08;
    var SHUT_IN = 0.5 - HOLD / 2, SHUT_OUT = 0.5 + HOLD / 2;

    /* THE RESPONSE CURVE, MEASURED AND CARRIED DIGIT FOR DIGIT (unfold.js:257-277). Equal movements of
       the hand produce equal felt change, and the curve is not guessed: the raw fold was walked in fine
       steps, the picture's travel read in each step, those distances added up along the travel, and the
       curve is the inverse of that running total. It is the module's curve and not one work's — it was
       read on two works whose shapes pull opposite ways and inverted against the hand's own steps a
       second time. Raw band before the curve: 5.19. */
    var FEEL_KNOTS = [
      0, 0.1199, 0.2105, 0.2709, 0.3176, 0.3567, 0.3913, 0.4231, 0.4528, 0.481, 0.5086,
      0.5369, 0.5673, 0.6133, 0.6607, 0.7065, 0.7519, 0.7969, 0.8415, 0.8885, 1
    ];
    function feelOf(u) {
      u = clamp(u, 0, 1);
      var n = FEEL_KNOTS.length - 1, x = u * n, i = Math.min(n - 1, Math.floor(x));
      return mix(FEEL_KNOTS[i], FEEL_KNOTS[i + 1], x - i);
    }

    // Cover-fit a work into the frame, and nothing beyond it. The module's own sheet is the plain cover
    // fit at both doors, so the port asks the host for no crop: `framings` publishes 1 at both ends.
    function fit(iw, ih, w, h) {
      var fa = w / Math.max(h, 1);
      var ia = iw / Math.max(ih, 1);
      if (ia > fa) return [fa / ia, 1, 0, 0];
      return [1, ia / fa, 0, 0];
    }

    // The numbers of one frame. Everything the shader gets beyond the seating of the two works is a
    // pure function of the pose; every number in the pose comes from a handle a score can drive, and
    // the lean reads the second the host hands down, so a seeded run repeats to the pixel.
    // A hair of an angle leaves two panels almost in one plane, which renders with a stray sliver
    // along the crease. The module holds them exactly flat below half a degree (unfold.js, and the
    // line in `posed` below), and that half degree is the module's own number, unchanged everywhere
    // but at a door — where the reading further down asks what it is worth in POINTS OF THE BUFFER
    // and holds a pair flat that stands under two of them.
    var FLAT_DEG = 0.5;
    // THE ROOM THE LEAN NEEDS and the room the CORNER needs on top of it — FRAG's own `EDGE` and
    // `PULL` consts (unfold.js:42, :47), carried here so the growth law can be recomputed in script.
    // Both are nothing at either door, because nothing leans and nothing turns there.
    var EDGE_JS = 1.16, PULL_JS = 1.8;

    // The numbers of one frame, at a given flat guard. The guard is a parameter here rather than the
    // constant it was, because the hold in `values` below asks this same function for the same pose
    // at the guard a door's own grid asks for. At the module's own half degree it answers, number
    // for number, exactly what it answered before.
    function posed(st, flatDeg) {
      var dial = clamp(st.mix, 0, 1);
      var four = st.panels >= 0.5;
      var lag = clamp(st.stagger, 0, 0.6);
      // THE HAND'S TWO HALVES. The first work folds shut, the two works exchange on the closed sheet,
      // the second work opens out. The module's own curve runs over each half.
      var fold = dial <= 0.5
        ? feelOf(clamp(dial / SHUT_IN, 0, 1))
        : feelOf(1 - clamp((dial - SHUT_OUT) / (1 - SHUT_OUT), 0, 1));
      var cross = smoothstep(SHUT_IN, SHUT_OUT, dial);
      // WHEN EACH PAIR OF PANELS GOES (unfold.js:303-315). Both pairs stand flat at fold 0 and fully
      // turned at fold 1 whatever the stagger is, so the handle cannot move either door.
      var fR = four ? smooth(fold / (1 - lag)) : smooth(fold);
      var fB = four ? smooth((fold - lag) / (1 - lag)) : 0;
      // A hair of an angle leaves two panels almost in one plane, which renders with a stray sliver
      // along the crease; hold them exactly flat instead.
      var aY = fR * MAXA, aX = fB * MAXA;
      if (aY < flatDeg) aY = 0;
      if (aX < flatDeg) aX = 0;
      var cY = Math.cos(aY * DEG), cX = Math.cos(aX * DEG);
      var rY = reachOf(cY), rX = four ? reachOf(cX) : 0;
      // THE LEAN RESTS AT BOTH DOORS (unfold.js:365-370): every term of it is carried by this gate,
      // which stands at nothing at either end of the fold, at any tilt and at any second of the clock.
      var gate = clamp(4 * fold * (1 - fold), 0, 1);
      var tl = clamp(st.tilt, 0, 1);
      // Under reduced motion the sway is parked, so the lean stands where it starts and nothing drifts.
      var ty = st.reduced ? 0 : st.t;
      var sh = clamp(st.shade, 0, 1);
      var open = Math.max(fR, fB);
      return {
        turn: [cY, Math.sin(aY * DEG), cX, Math.sin(aX * DEG)],
        reach: [rY, rX, fR, fB],
        form: [gate, mix(PERSP_FLAT, PERSP_DEEP, clamp(st.depth, 0, 1)), four ? 1 : 0,
               1 - smooth((open - 0.004) / 0.05)],
        // NO POINTER UNDER A SCORE (unfold.js:372-376): the module answers the hand outside it and
        // nothing else, so a scored frame is the same frame on any screen.
        lean: [gate * (tl * -4 + Math.sin(ty * 0.31) * 1.6) * DEG,
               gate * tl * Math.sin(ty * 0.23 + 1.1) * 7 * DEG,
               gate * Math.sin(ty * 0.17 + 2.2) * 1.3 * tl * DEG,
               smooth(Math.max(aY, aX) / MIRROR)],
        // A shade is cast BY the panel that is turning, so it goes out with the panel that casts it: at
        // the closed sheet the standing quarter carries none and the far door is the photograph bare.
        shade: [sh * 0.10 * fR * rY, sh * 0.97 * Math.pow(1 - cY, 0.8),
                sh * 0.93 * Math.pow(1 - cX, 0.8), sh * 0.97 * Math.pow(1 - cY * cX, 0.8)],
        crease: [0.5 * Math.sin(aX * DEG) * rX, 0.5 * Math.sin(aX * DEG) * cY * rX,
                 0.5 * Math.sin(aY * DEG) * rY, cross],
        // read on the diagnostic surface, bound to no uniform: what the hand came to
        fold: fold, cross: cross, aY: aY, aX: aX, four: four ? 1 : 0, flatDeg: flatDeg,
        mask: clamp(st.mask, 0, 1),
      };
    }

    // ---- THE DOOR THE INSTRUMENT READS FOR ITSELF ------------------------------------------------
    // His 18:00 architecture decision, carried in the U27 brief: the instrument reads its doors at
    // runtime on the actual buffer, and the report it hands back is the runtime truth; what the
    // manifest declares is only the claim. The meshing instrument answered that first
    // (pass-inst-gears.js, THE DOOR THE INSTRUMENT READS FOR ITSELF); this is the same law read in
    // this instrument's own unit, which is the PANEL — and the map of them over the frame.
    //
    // WHAT A DOOR ASKS OF THIS INSTRUMENT. At either door the frame is one work standing whole, at
    // the plain cover fit the `framings` block publishes. Three things carry that, and this reads
    // all three ON THE BUFFER rather than declaring them:
    //   · THE PANEL MAP COVERS THE FRAME. The growth law grows the sheet by exactly what each
    //     turning panel gives up, so no point of the frame is ever left with no panel standing on
    //     it. That is a claim about a GRID — whether a bare point falls between samples or on one —
    //     and it is now walked at the buffer's own sample points instead of being asserted.
    //   · THE SHEET LIES FLAT. Every panel's turn is nothing at a door, so the map is the sheet
    //     itself and the frame is the file. A pair standing a hair out of plane opens a sliver along
    //     its crease, and how wide that sliver is depends entirely on the buffer: the module's own
    //     guard holds a pair flat below half a degree, which is nothing on a small frame and three
    //     points of a tall one.
    //   · THE JUDGES' CHANNEL IS SHUT. `mask` draws the panel map itself as colour, which is what it
    //     is for; left open at a door the frame is a false-colour map of the panels and not the
    //     photograph at all.
    //
    // WHAT THIS READING FINDS, SAID PLAINLY. On every buffer the host can hand and every pose these
    // handles admit, the first two come out whole: at a door `fold` is exactly 0, every panel lies
    // in the sheet's own plane, the growth law's scale comes out exactly 1 and the map claims every
    // point walked. That is not a reason to leave the claim unread — it is the runtime truth this
    // lane was asked for, and it is published as the applied state below, where a suite reads it and
    // a later change to the fold, the stagger or the growth law reddens against it. The one door
    // this instrument's own handles can spoil is the third, and it is refused.
    //
    // WHERE THE SHEET'S OWN SIZE COMES FROM. The shader recovers it from the seating the host
    // applied (`SZ` in FRAG reads `fitA`/`fitB`), and the host hands this instrument no seating
    // (`frameState` carries the viewport and nothing of the fit). The sheet is the file COVER-fitted,
    // so it is never smaller than the frame: `SZ` is at its smallest `(aspect, 1)`, which is exactly
    // the case in which the panel map has the least frame to spare. The reading takes that smallest
    // sheet, so it can only ever over-hold, never miss a bare point.
    var DOOR_SLIP = 0.5;   // points of the grid: half a point, inside which a sample cannot move
    var DOOR_HOLD = 2;     // how far the hold reaches, in points of the grid
    // How much of the panel map may stand in the frame at a door and it still BE the photograph:
    // half a level of 255, under anything the frame itself can carry. The charter's own door bar is
    // 6 of 255 over the canvas rect, and half a level is an eighth of that at one point.
    var DOOR_SHOW = 0.5 / 255;

    // The grid the door is read on, and which of the two it is. `drawn` says which one the sentence
    // below names, since a reader told «a 780 x 1688 frame» would look for a device that has none.
    function doorGridOf(st) {
      var bw = Math.round(st.bufWidth), bh = Math.round(st.bufHeight);
      if (bw >= 1 && bh >= 1) return { w: bw, h: bh, drawn: true };
      return { w: Math.round(st.cssWidth), h: Math.round(st.cssHeight), drawn: false };
    }

    // The sheet's own lean, applied to one vector — FRAG's `stood`, carried across line for line.
    function stood(x, y, z, L) {
      var cx = Math.cos(L[0]), sx = Math.sin(L[0]);
      var cy = Math.cos(L[1]), sy = Math.sin(L[1]);
      var cz = Math.cos(L[2]), sz = Math.sin(L[2]);
      var px = x * cz - y * sz, py = x * sz + y * cz, pz = z;
      var qx = px * cy + pz * sy, qy = py, qz = -px * sy + pz * cy;
      return [qx, qy * cx - qz * sx, qy * sx + qz * cx];
    }

    // Where one point of the frame falls on one panel — FRAG's `lands`, carried across line for
    // line, with the pair (u, v) and the depth it comes back with.
    function lands(sx, sy, a, bu, bv, d, limx, limy) {
      var c1x = bu[0] + sx * bu[2] / d, c1y = bu[1] + sy * bu[2] / d;
      var c2x = bv[0] + sx * bv[2] / d, c2y = bv[1] + sy * bv[2] / d;
      var k = 1 - a[2] / d;
      var rx = sx * k - a[0], ry = sy * k - a[1];
      var det = c1x * c2y - c2x * c1y;
      var safe = Math.abs(det) < 1e-9 ? 1e-9 : det;
      var ux = (rx * c2y - c2x * ry) / safe, uy = (c1x * ry - rx * c1y) / safe;
      return { hit: Math.abs(det) > 1e-9 && ux >= 0 && uy >= 0 && ux <= limx && uy <= limy,
               u: ux, v: uy, z: a[2] + bu[2] * ux + bv[2] * uy };
    }

    // THE PANEL MAP, READ ON THE BUFFER THE SHADER WILL SAMPLE ON. The sheet is built exactly as
    // FRAG builds it and the map is walked at the buffer's own sample points: its four corners,
    // where the growth law has the least to spare; the midpoints of its four edges; and the nine
    // points around its centre, where the panels' own seams cross at a door. Every one of them must
    // be claimed by a panel or by the sheet's own backing.
    function mapReadOf(v, W, H) {
      var aspect = W / Math.max(H, 1), pt = 1 / H;
      var SZ = [aspect, 1];                 // the tightest sheet a cover fit can hand
      var four = v.four > 0.5;
      var CW = SZ[0] * 0.5, CH = four ? SZ[1] * 0.5 : SZ[1];
      var cY = v.turn[0], sY = v.turn[1], cX = v.turn[2], sX = v.turn[3];
      var rY = v.reach[0], rX = v.reach[1];
      var reachR = CW * rY, reachB = CH * rX;
      var persp = v.form[1];
      var deep = 2 * persp;
      var corner = deep / (deep + sY + (CH / CW) * sX);
      var extX = (CW - reachR) * 0.5 + reachR * corner;
      var extY = (CH - reachB) * 0.5 + reachB * corner;
      var room = 1 + (EDGE_JS - 1) * v.form[0] + PULL_JS * (1 - corner) * rY * rX;
      var sc = room * Math.max(Math.max(aspect / (2 * extX), 1 / (2 * extY)), 1);
      var d = persp * SZ[0] * sc;
      var slide = [(CW - reachR) * 0.5, four ? (CH - reachB) * 0.5 : 0];
      var L = v.lean;
      var e0 = stood(sc, 0, 0, L), e1 = stood(0, sc, 0, L);
      var eY = stood(cY * sc, 0, -sY, L), eX = stood(0, cX * sc, -sX, L);
      var eXY = stood(-sX * sY * sc, cX * sc, -sX * cY, L);
      var mid = [SZ[0] * 0.5, SZ[1] * 0.5];
      function origin(dx, dy) {
        return stood((slide[0] + dx - mid[0]) * sc, (slide[1] + dy - mid[1]) * sc, 0, L);
      }
      var oTL = origin(0, 0), oTR = origin(CW, 0), oBL = origin(0, CH), oBR = origin(CW, CH);
      var ey = four ? pt : 0;
      var reads = [], bare = 0, i, j;
      function walk(px, py) {
        var sx = (px / W) * aspect - aspect * 0.5, sy = py / H - 0.5;
        var got = false, code = 0;
        var hTL = lands(sx, sy, oTL, e0, e1, d, CW + pt, CH + ey);
        var hTR = lands(sx, sy, oTR, eY, e1, d, CW, CH + ey);
        var hBL = lands(sx, sy, oBL, e0, eX, d, CW + pt, CH);
        var hBR = lands(sx, sy, oBR, eY, eXY, d, CW, CH);
        var hSh = lands(sx, sy, oTL, e0, e1, d, SZ[0], SZ[1]);
        if (hTR.hit) { got = true; code = 0.50; }
        if (hBL.hit && four) { got = true; code = 0.75; }
        if (hBR.hit && four) { got = true; code = 1.00; }
        if (hSh.hit) got = true;
        if (hTL.hit) { got = true; code = 0.25; }
        if (!got) bare++;
        reads.push(code);
      }
      for (i = 0; i < 2; i++) {
        for (j = 0; j < 2; j++) { walk(i ? W - 0.5 : 0.5, j ? H - 0.5 : 0.5); }
      }
      walk(0.5, H * 0.5); walk(W - 0.5, H * 0.5); walk(W * 0.5, 0.5); walk(W * 0.5, H - 0.5);
      for (i = -1; i <= 1; i++) {
        for (j = -1; j <= 1; j++) { walk(W * 0.5 + i, H * 0.5 + j); }
      }
      // HOW FAR EITHER PAIR STANDS OUT OF THE SHEET'S OWN PLANE, in points of this grid: the far edge
      // of a turned panel, carried by its own sine, read against the buffer's own height.
      return { walked: reads.length, bare: bare, codes: reads, sheet: [SZ[0] * sc, SZ[1] * sc],
               scale: sc, panels: four ? 4 : 2, seamPx: pt * H,
               turnPx: Math.max(sY * CW * H, sX * CH * H) };
    }

    // THE DOOR, MEASURED. Null everywhere but at a door, since away from the doors a folding sheet
    // is the picture rather than a fault. The door is named by the manifest's own `doors` block:
    // `mix` at 0 is the entry door, where the frame is the departing work whole, and `mix` at 1 the
    // exit door, where it is the arriving one.
    function doorReadOf(v, st) {
      var want = st.mix === 0 ? 1 : (st.mix === 1 ? 0 : -1);
      if (want < 0) return null;
      var g = doorGridOf(st), W = g.w, H = g.h;
      if (!(W >= 1) || !(H >= 1)) return null;
      var map = mapReadOf(v, W, H);
      map.grid = g;
      map.want = want;
      map.mask = v.mask;
      return map;
    }

    // THE REFUSAL, worded the way the host's own manifest refusals read: what is wrong, in this
    // instrument's own measured numbers, on the grid it was measured on.
    function doorWhyNoOf(read) {
      if (!read) return null;
      var g = read.grid, door = read.want ? "the entry" : "the exit";
      var work = read.want ? "departing" : "arriving";
      var where = " of a " + g.w + " x " + g.h + (g.drawn ? " buffer" : " frame");
      if (read.bare) {
        return door + " door leaks: the panel map leaves " + read.bare + " of the " + read.walked
             + " points this reading walked" + where + " with no panel standing on them, where "
             + door + " door's own law asks for the " + work + " work at every point";
      }
      if (read.turnPx >= DOOR_SLIP) {
        return door + " door leaks: a pair of panels stands " + read.turnPx.toFixed(2)
             + " points" + where + " out of the sheet's own plane, so a sliver of the frame is "
             + "drawn along its crease, where " + door + " door's own law asks for the flat sheet "
             + "and the " + work + " work at every point";
      }
      if (read.mask >= DOOR_SHOW) {
        return door + " door leaks: the judges' own channel stands at " + read.mask.toFixed(6)
             + ", so the frame draws the panel map — " + read.panels + " panels over a "
             + g.w + " x " + g.h + (g.drawn ? " buffer" : " frame")
             + " — instead of the " + work + " work, where " + door
             + " door's own law asks for the " + work + " work at every point";
      }
      return null;
    }

    // THE NUMBERS OF ONE FRAME, WITH ITS DOOR READ ON THE BUFFER BEING DRAWN. Away from a door this
    // is `posed` and nothing more: the reading is taken nowhere else and no guard moves. At a door
    // it walks its own panel map on the buffer and publishes what it read — how many points it
    // walked, how many stood bare, the panel count, the sheet's own drawn size, the growth law's
    // scale, the seam in points of the grid and how far either pair stands out of plane. Where a
    // pair stands out of plane by less than the hold's own reach, the module's own flat guard is
    // re-asked in the grid's own units and the pair is held whole flat, with the travel it gave up
    // on the record; beyond that, and for a judges' channel left open, the refusal stands.
    //
    // WHY THE HOLD IS IN POINTS AND NOT IN DEGREES. Half a degree is the module's own number and it
    // is a number about a SCREEN: on a short frame it is a fraction of a point and on a tall one it
    // is three of them. At a door the sheet must be flat, so what the guard has to answer is «can
    // this grid show the turn», which is a question in points. Two points is the reach, for the same
    // reason the meshing instrument holds two rungs: it closes what a real grid can open, and it
    // leaves the refusal standing rather than making a guard that never fires.
    function values(st) {
      var v = posed(st, FLAT_DEG);
      v.flatDegRequest = FLAT_DEG;
      v.turnHeld = null;
      v.doorHeld = null;
      var read = doorReadOf(v, st);
      var no = doorWhyNoOf(read);
      v.doorGrid = read ? read.grid : null;
      v.panelMap = read ? { walked: read.walked, bare: read.bare, panels: read.panels,
                            sheet: read.sheet, scale: read.scale, seamPx: read.seamPx,
                            turnPx: read.turnPx } : null;
      if (!no) { v.doorWhyNo = null; return v; }
      if (read.bare === 0 && read.turnPx >= DOOR_SLIP && read.turnPx < DOOR_HOLD) {
        // the angle whose far edge travels one point of this grid, which is the guard this grid
        // asks for in place of the module's own half degree
        var w = posed(st, Math.max(FLAT_DEG, Math.max(v.aY, v.aX) + 1e-9));
        var wRead = doorReadOf(w, st);
        if (!doorWhyNoOf(wRead)) {
          w.flatDegRequest = FLAT_DEG;
          w.turnHeld = read.turnPx;
          w.doorHeld = no;
          w.doorWhyNo = null;
          w.doorGrid = wRead.grid;
          w.panelMap = { walked: wRead.walked, bare: wRead.bare, panels: wRead.panels,
                         sheet: wRead.sheet, scale: wRead.scale, seamPx: wRead.seamPx,
                         turnPx: wRead.turnPx };
          return w;
        }
      }
      v.doorWhyNo = no;
      return v;
    }

    var manifest = {
      id: "unfold", api: 1, arity: 2,
      // The sheet comes apart into its own panels, the closed photograph stands while the two works
      // exchange on it, and the second work gathers itself out of the same seams.
      roles: ["disassembly", "mystery", "assembly"],
      // WHERE THIS STANDS ON THE CHARTER'S SHELF, and the reading is said to be derived.
      //   · CELL — the panels themselves. lab/data/module-contract.json records this module's level as
      //     CELL, and that row is carried here rather than re-decided: the motion is a partition of the
      //     frame into cells that turn.
      //   · CELL CONTENT — what a cell CARRIES. Each panel shows its own quarter of the work while it
      //     lies flat and the mirror of the closing quarter once it has turned, and at the far door the
      //     whole frame is one quarter standing alone. That is the content of a named region changing
      //     inside the region, which is the level the composer's own census records as held by no
      //     landed instrument.
      // SURFACE is not claimed. What covers the frame here is the works' own pictures, cut and carried;
      // no field of this instrument's own runs over it. Claiming it would also put this voice on the one
      // level all three landed instruments already hold, where the levels law allows a single owner.
      levels: ["CELL", "CELL CONTENT"],
      params: { tilt: [0, 1], shade: [0, 1], depth: [0, 1], stagger: [0, 0.6], panels: [0, 1] },
      // EVERY handle a score can drive (§4.4b). `mix` is the dial and `clock` is the second the host
      // hands down; the five below them are the module's declared params; `mask` is the judges' channel,
      // resting where the module has no such thing at all.
      //
      // NO HANDLE HERE KEEPS A CLOCK OR A POINTER OF ITS OWN. The module runs a fifteen-second breath
      // and reads the pointer across its mount (unfold.js:424-462); both are gone. The one place time
      // reaches the picture is the sway that carries the lean, and that reads the `clock` handle, so a
      // seeded score repeats to the pixel. The module's own `pace` was never a published handle and is
      // not one here, for the reason the module gives: a handle a score can walk without moving the
      // picture is noise in the score.
      //
      // `panels` IS THE MODULE'S `mode`, WITH ITS TWO NAMES. The module rebuilds its DOM when the mode
      // changes; nothing is rebuilt here, so the handle is a plain number a score can hold or step, and
      // the frame answers it at once.
      handles: {
        mix: { min: 0, max: 1, def: 0 },
        clock: { min: 0, max: 14, def: 0 },
        tilt: { min: 0, max: 1, def: 0.5 },
        shade: { min: 0, max: 1, def: 1 },
        depth: { min: 0, max: 1, def: 0.5 },
        stagger: { min: 0, max: 0.6, def: 0.34 },
        panels: { min: 0, max: 1, def: 1, kind: "enum", step: 1,
                  names: { "0": "two", "1": "four" } },
        // THE MEASUREMENT THIS HANDLE IS READ AGAINST AT A DOOR, published beside its range the way
        // the meshing instrument publishes its own. `readAtADoor` says what is read (this
        // instrument's own panel map, walked at the buffer's own sample points), on which grid (the
        // drawing buffer the host binds, with the CSS frame where it hands none), how far the hold
        // reaches (two points of that grid, for a pair standing out of the sheet's plane) and where
        // the guard the module's own constant asks for stays on the record.
        mask: { min: 0, max: 1, def: 0,
                applied: { readAtADoor: { points: DOOR_HOLD, readOn: "the drawing buffer",
                                          reads: "flatDegRequest",
                                          measures: "this instrument's own panel map, walked at "
                                                  + "the buffer's own sample points" } } },
      },
      neutrals: { a: 0, b: 1 },
      doors: { in: { handle: "mix", value: 0, work: "a" },
               out: { handle: "mix", value: 1, work: "b" } },
      // Both doors frame alike, and both are the PLAIN COVER FIT: the module's repair of 2026-08-13
      // made the sheet the file cover-fitted and put the room the lean needs on the gate, which stands
      // at nothing at either end. So neither door is cropped and neither is upscaled.
      framings: { "0": { coverCrop: 1 }, "1": { coverCrop: 1 } },
      drivers: ["progress", "cueProgress", "time", "velocity", "capability", "noise", "static",
                "curve", "spline", "map", "add", "multiply", "mix", "clamp", "hold", "segment",
                "ramp", "slew", "oscillate", "node"],
      camera: { needs: "none", authority: "stage" },
      gl: { preserveDrawingBuffer: false },
      // WHAT THIS INSTRUMENT WRITES WHERE ITS OWN MATTER IS ABSENT (§7's coverage law, and the
      // per-instrument specification in docs/design/COVERAGE.md). It is absent nowhere. The growth law
      // grows the sheet by exactly what each turning panel gives up, so the standing picture covers the
      // frame at every point of the travel and no transparency is ever drawn. The alpha is the constant
      // 1, said as a decision. Under the placement rule this instrument is lawful as the lowest cue of
      // a stack and as a whole one-cue score, which is the ground 1 320 declined plans are waiting on.
      coverage: { writes: false,
                  how: "the growth law grows the sheet by exactly what each turning panel gives up, so "
                     + "the standing picture covers the frame at every point of the travel and the "
                     + "alpha is the constant 1" },
      // The neutral pose is the ENTRY DOOR — `mix` at 0, the value the `doors` block above names —
      // so the frame keys the host reads off it at registration include the door's own record.
      neutralPose: { mix: 0, tilt: 0.5, shade: 1, depth: 0.5, stagger: 0.34, panels: 1, mask: 0,
                     t: 0, reduced: false, cssWidth: 1000, cssHeight: 1000 },
      passes: [{
        program: "unfold", vert: VERT, frag: FRAG, position: "aPos",
        uniforms: [
          { name: "uA", type: "sampler2D", source: "textureA" },
          { name: "uB", type: "sampler2D", source: "textureB" },
          { name: "uFitA", type: "vec4", source: "fitA" },
          { name: "uFitB", type: "vec4", source: "fitB" },
          { name: "uRes", type: "vec2", source: "resolution" },
          { name: "uTurn", type: "vec4", source: "frame:turn" },
          { name: "uReach", type: "vec4", source: "frame:reach" },
          { name: "uForm", type: "vec4", source: "frame:form" },
          { name: "uLean", type: "vec4", source: "frame:lean" },
          { name: "uShade", type: "vec4", source: "frame:shade" },
          { name: "uCrease", type: "vec4", source: "frame:crease" },
          { name: "uMask", type: "float", source: "handle:mask" },
        ],
      }],
      // The instrument allocates nothing of its own: it spends the two source-texture slots the host
      // already holds and the one programme the host builds from this manifest. The module's own DOM
      // stage — a perspective container, a sheet, four panels, seven faces, four gradients and three
      // creases — is what this port does without.
      resources: { lean: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                           passes: 1, bytesEstimate: 0, variant: "lean" },
                   standard: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                               passes: 1, bytesEstimate: 0, variant: "standard" },
                   rich: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                           passes: 1, bytesEstimate: 0, variant: "rich" } },
      capabilities: ["webgl2"],
      decline: ["one work only", "a source that never decoded"],
      provenance: { labPath: "lab/effects/unfold.js", commit: "4c7dfe4",
                    sha256: "28688b86686a12b57c9fbc4dd9775350d77f9906681b1f4aff57e20dd6f71408" },
      readiness: "production-ready",
    };

    var live = false;
    return {
      name: "unfold",
      manifest: manifest,
      values: values,
      fit: fit,
      feel: feelOf,
      prepare: function (o) {
        if (!o.sources) return { take: false, why: "the unfold instrument needs both works" };
        if (!o.cue) return { take: false, why: "no cue names it" };
        return { take: true };
      },
      start: function () { live = true; },
      // The pose the shader draws. The module's breath and its pointer are gone, so every number here
      // comes from a handle a score drives, and the lean's sway reads the second the host hands down.
      //
      // A DOOR THIS INSTRUMENT CANNOT KEEP WHOLE IS REFUSED RATHER THAN DRAWN. The door law is the
      // instrument's own claim (the manifest's coverage line above), so the instrument is what
      // answers for it: at either door it walks its own panel map on the buffer the host is about to
      // bind and, where a point of that grid stands bare, where a pair stands out of the sheet's
      // plane further than the hold reaches, or where the judges' channel is left open, it hands the
      // host the reason with the measured map in it instead of drawing a door that is not the
      // photograph. The host recovers the transaction on that reason and the walk's own glide
      // carries the visitor, which is the product's own behaviour with no renderer.
      frame: function (st) {
        if (!live) return;
        var h = st.handles;
        var pose = {
          mix: h.mix, tilt: h.tilt, shade: h.shade, depth: h.depth, stagger: h.stagger,
          panels: h.panels, mask: h.mask, t: h.clock, reduced: st.reduced,
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
    instrument: unfoldInstrument(),
  });
})();
