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
  // mirrored panels until the panels swing back out again — the same turn, not a flat rest — and it
  // is across that swing, at its own deepest point, that the first work's panels give way to the
  // second's: across eight hundredths of the hand the panels leave their own closed sheet and return
  // to it, and the exchange happens at the swing's own turned middle rather than at either of its
  // shut ends. Then the second work opens out along the same seams and stands whole.
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
  // port had to say where the second work enters. It enters near the one instant the module's own
  // construction offers: the far door, where the sheet stands closed and the frame holds a single flat
  // quarter of the file at exactly the framing the whole work stood at. Both works pass through that
  // shut instant — first the departing work closing over it, then the arriving work opening back out
  // of it — but the hand does not change which work the panels read AT it: it changes hands at the
  // swing's own deepest turn, between the two shut edges, where a real panel stands on screen rather
  // than the closed sheet (S-03, the fresh chair audit of 2026-08-27).
  //
  // WHAT A FLAT PICTURE CANNOT ANSWER WITH A SECOND FOLD. By the instant the sheet stands shut, every
  // panel has already turned past HOME and the growth law has already given it up — folding a closed
  // panel FURTHER moves nothing the eye can read. So the one motion left to a panel that has nowhere
  // further to retreat is the one it already owns: swing back OUT of its own turn, away from flat, and
  // in again. The first work's panels take that swing to leave, the second work's panels take the same
  // swing, mirrored, to arrive — and the hand changes which file the panels read at the swing's own
  // DEEPEST turn, not at either of its shut ends, so the two works change hands while panels genuinely
  // stand turned on screen rather than while the sheet is shut (S-03, the fresh chair audit of
  // 2026-08-27: a swing that came back to flat at the handover answered «no blend of two textures» and
  // still cut, at that one instant, between two full-frame photographs — the geometric hand-over the
  // наряд asked for stood nowhere on screen when it was needed most).
  //
  // The hand therefore runs: the first work folds shut over the first forty-six hundredths, the first
  // work's own panels swing out from flat across the hold's own first half, the hand changes which work
  // the panels read at the hold's own middle — where the swing stands at its own deepest turn — the
  // second work's own panels swing back in to flat across the hold's own second half, and the second
  // work opens out over the last forty-six. The module's own response curve is applied to each of the
  // two long halves, so equal movements of the hand are equal felt change on both sides of the
  // exchange, which is the whole point of the curve. HOLD and FLUTTER_DIP are the port's own numbers
  // and the only two that are; every other constant below is the module's.
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
      // THE WORLD THE SHEET OPENS INTO: how far it has opened, the plane's own attitude to the eye
      // in radians, the parquet's own period as a share of the sheet, and the turn of its lattice.
      // Every one of the four is nothing at nothing, which is what makes the door exact.
      "uniform vec4 uField;",
      // THE ROOM THE LEAN NEEDS, and the room the CORNER needs on top of it (unfold.js:42, :47). Both
      // are the module's own numbers and both are nothing at either door, because nothing leans and
      // nothing turns there.
      "const float EDGE = 1.16;",
      "const float PULL = 1.8;",
      // HOW FAR THE WORLD'S OWN LIGHT REACHES INTO THE PARQUET at the horizon itself. It is the
      // port's own number and it belongs to the world rather than to the module, which has no
      // world. It squares with distance, so the near tiles are the photograph whole and only the
      // far ones give way to the light.
      "const float HAZE = 0.78;",
      // HOW CLOSE THE EYE COMES TO THE PLANE as the world opens, as a share of the viewing distance
      // the module stands at. It is what puts the HORIZON inside the frame, and without it the
      // parquet is a flat mirrored pattern with a hint of foreshortening — a wallpaper and not a
      // floor. The vanishing line of a plane tipped by θ lands at d / tan θ above the frame's own
      // middle, so at the module's own distance and seventy degrees it stands a fifth of a frame
      // ABOVE the glass and is never seen; at this share it lands in the frame's upper quarter,
      // where a floor's horizon belongs. Going to the floor is the eye's own first axis in
      // lab/PARQUET-WORLD-BRIEF.md, and here it rides the world's one envelope with the rest.
      "const float NEAR = 0.42;",
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
      // WHERE ONE POINT OF THE FRAME FALLS ON THE PLANE THE SHEET LIES IN, with no edge to the
      // plane at all. It is `lands` with its two limits taken off — the same two-by-two system,
      // the same divide — because past the sheet's own rectangle the plane goes on. The one test
      // that replaces the limits is the HORIZON: a point solves to a place behind the eye's own
      // vanishing distance as readily as to one in front of it, and only the ones in front are on
      // the floor. That test is what draws the horizon line, and nothing else in this file does.
      "bool ground(vec2 s, vec3 a, vec3 bu, vec3 bv, float dd, out vec2 uv, out float z){",
      "  vec2 c1 = vec2(bu.x + s.x * bu.z / dd, bu.y + s.y * bu.z / dd);",
      "  vec2 c2 = vec2(bv.x + s.x * bv.z / dd, bv.y + s.y * bv.z / dd);",
      "  float k = 1.0 - a.z / dd;",
      "  vec2 r = vec2(s.x * k - a.x, s.y * k - a.y);",
      "  float det = c1.x * c2.y - c2.x * c1.y;",
      "  if (abs(det) < 1e-9) { uv = vec2(0.0); z = 0.0; return false; }",
      "  uv = vec2(r.x * c2.y - c2.x * r.y, c1.x * r.y - r.x * c1.y) / det;",
      "  z = a.z + bu.z * uv.x + bv.z * uv.y;",
      "  return dd - z > 1e-4;",
      "}",
      // THE PARQUET'S OWN FOLD. Past its own edge the sheet does not stop and it does not repeat:
      // it MIRRORS, which is the same law the four panels already obey inside the frame — each
      // panel is the mirror of the quarter the sheet closes onto. So the continuation is that law
      // carried on without end, and a viewer watching it sees the rule the work was cut by rather
      // than being told it. One triangle wave per axis is the whole of it.
      "vec2 folded(vec2 q, vec2 period){",
      "  vec2 t = mod(q / period, 2.0);",
      "  return period * (1.0 - abs(t - 1.0));",
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
      // THE GROWTH LAW, AND THE ONE THING THAT RELEASES IT. `grow` is what the sheet has to be
      // scaled by so that no point of the frame is ever left bare — the module's own repair of
      // 2026-08-13. It is exactly 1 at either door and above 1 through the fold. As the world opens
      // the sheet stops having to cover the frame, because the plane it lies in covers it instead,
      // so `grow` is walked back to 1 by `uField.x`. At nothing this is `room * grow`, character for
      // character what stood here before, and at either door it is `room` and `grow` both at 1.
      "  float grow = max(max(aspect / (2.0 * extX), 1.0 / (2.0 * extY)), 1.0);",
      "  float sc = room * mix(grow, 1.0, uField.x);",
      "  float d = persp * SZ.x * sc * mix(1.0, NEAR, uField.x);",
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
      // ---- THE WORLD THE SHEET OPENS INTO ------------------------------------------------------
      // HIS 19:13 WORD, THE SECOND REGISTER. A crossing may be a spectacular atypical event, or it
      // may let the viewer glimpse HOW the works were made — never a lesson, simply a
      // transformation that reveals the making. His own instance is this one: an unfold that
      // becomes an infinite parquet while the camera shows the plane at an angle.
      //
      // WHAT IS DRAWN HERE. The sheet lies in a plane. Where a PANEL stands it is the picture and
      // nothing below is asked for. Everywhere else the same plane goes on — folded at the
      // parquet's own period, mirrored the way the four panels are mirrored, receding to the eye's
      // own horizon — and past the horizon the world's light stands, which is the work's own tone.
      // So the frame is filled at every point and the alpha stays the constant 1 this instrument
      // has always published.
      //
      // THE SHEET'S OWN BACKING GIVES WAY TO THE PARQUET RATHER THAN STANDING AGAINST IT. Inside
      // the sheet's own rectangle the backing draws the whole file at the sheet's size, which is
      // the parquet at a period of one whole sheet and nothing else; at any other period the two
      // are different pictures and one of them has to win. The parquet wins, WEIGHTED BY THE WORLD,
      // so at a world of nothing the backing is untouched and every step of the way is continuous.
      //
      // HOW IT ENTERS AND LEAVES. Through its own zero and nowhere else. At `uField.x` of nothing
      // the plane's attitude is nothing, the growth law binds, the sheet covers the frame at every
      // point and this branch draws on no point at all. As the world opens, the plane tips, the
      // growth law is walked back, and the parquet grows into exactly the room the tipping opened
      // — it is never laid over anything and it never appears.
      //
      // WHAT IT READS FROM THE WORK. The period is the work's own cutting step and the turn is the
      // angle that step was cut at, both named at the handles below. So the parquet the viewer
      // watches run off to the horizon is the work's own device, continued.
      "  if (uField.x > 0.0 && !got) {",
      // The world's light: the work's own tone, read at four places rather than one so a single
      // texel cannot decide the colour of a whole sky.
      "    vec3 tone = 0.25 * (pane(tex, SZ * 0.3, SZ) + pane(tex, SZ * vec2(0.7, 0.3), SZ)",
      "                      + pane(tex, SZ * vec2(0.3, 0.7), SZ) + pane(tex, SZ * 0.7, SZ));",
      "    vec3 wcol = tone; float wcode = 0.0625;",
      "    vec2 wloc = vec2(0.0);",
      "    vec2 gq; float gz;",
      "    if (ground(s, oTL, e0, e1, d, gq, gz)) {",
      // the parquet's own turn, taken about the sheet's own centre so the lattice pivots where the
      // work does and not at the frame's corner
      "      vec2 c0 = gq - SZ * 0.5;",
      "      float ct = cos(uField.w), stt = sin(uField.w);",
      "      vec2 rq = vec2(c0.x * ct + c0.y * stt, -c0.x * stt + c0.y * ct) + SZ * 0.5;",
      "      vec2 P = SZ * max(uField.z, 0.05);",
      "      vec2 fq = folded(rq, P);",
      "      wcol = pane(tex, fq, SZ);",
      // DEPTH, THE ONE THING THAT MAKES A PLANE READ AS A PLANE. What is far takes the world's own
      // light; without it the parquet is a flat pattern however the plane is tipped.
      //
      // AND IT IS READ OFF THE PROJECTION'S OWN DIVISOR, not off `z`. Away from the eye is NEGATIVE
      // z in this chain — a panel turning away carries `-sin` into its own basis, which is where
      // that sign was set — so a fade written on `z / d` puts the haze on the NEAREST tiles and
      // leaves the far ones bare, which is the reading turned inside out. The divisor `1 - z/d` is
      // 1 in the sheet's own plane and grows without bound toward the vanishing point, so
      // `1 - 1/k` is 0 at the sheet and 1 at the horizon whichever way the plane is tipped.
      "      float k = 1.0 - gz / d;",
      "      float far = clamp(1.0 - 1.0 / max(k, 1.0), 0.0, 1.0);",
      "      wcol = mix(wcol, tone, HAZE * far * far);",
      "      wcode = 0.125;",
      "      wloc = clamp(fq / vec2(CW, CH), 0.0, 1.0);",
      "    }",
      // Outside the sheet nothing else drew, so the world is the picture whole. Inside it the
      // backing drew, and the world takes it over by exactly how far the world stands open.
      "    float w = hSh ? uField.x : 1.0;",
      "    col = mix(col, wcol, w);",
      "    code = mix(code, wcode, w);",
      "    loc = mix(loc, wloc, w);",
      "  }",
      // THE PANEL MAP, the judges' own frame: which panel stands at this point of the frame and where
      // in it. It is black exactly where no panel stands, so a row reads off the picture whether the
      // growth law kept its promise, and it carries no coverage of its own because what it is for is
      // to be read as colour.
      "  judge = vec3(code, clamp(loc.x, 0.0, 1.0), clamp(loc.y, 0.0, 1.0));",
      "  return col;",
      "}",
      "void main(){",
      "  vec3 judge, col;",
      // THE EXCHANGE (S-03). One work's sheet is drawn and the other is never sampled, at every point
      // of the hand alike: the first work's own panels carry the fold up to and through their own
      // leaving swing, the hand changes which file the panels read at the hold's own middle — where
      // `uCrease.w` (the very handle that used to weigh a blend) crosses its own half, AND where
      // `posed`'s own swing stands at its deepest turn rather than at flat, so a real panel is what
      // changes hands — and the second work's own panels carry the fold on from their own arriving
      // swing. No two pictures are ever combined: the frame is always the one sheet the fold is
      // standing on.
      "  if (uCrease.w >= 0.5) { col = sheet(uB, uFitB, judge); }",
      "  else { col = sheet(uA, uFitA, judge); }",
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

    // THE PORT'S OWN FIRST NUMBER. How much of the hand carries the exchange, and therefore where it
    // sits. It is centred on the middle of the hand, so the two halves are equal and the module's own
    // curve runs once over each of the two long closing/opening stretches either side of it. Both works
    // reach fold 1 — the one instant each stands as one flat full-frame picture — at the hold's own
    // middle, which is where the hand switches which file the panels read. Eight hundredths is that
    // span, wide enough to carry one full swing out and back on each side at the pass durations this
    // engine runs — half a second at 6.5 s — and narrow enough that the fold itself keeps the rest of
    // the hand.
    var HOLD = 0.08;
    var SHUT_IN = 0.5 - HOLD / 2, SHUT_OUT = 0.5 + HOLD / 2;
    // THE PORT'S OWN SECOND NUMBER (S-03, replacing first the flat cross-dissolve this exchange used
    // to play, and then — the fresh chair audit of 2026-08-27 — the flat CUT that replaced it: a swing
    // built to come back to fold 1 exactly where the hand changed which work the panels read answered
    // «no blend of two textures» to the letter and still handed the eye a straight cut between two
    // full-frame photographs, since both works stood flat there alike). By SHUT_IN the sheet already
    // stands shut and every panel has already turned past HOME, so folding a closed panel FURTHER moves
    // nothing the eye can read — the one motion left to it is the one it already owns: swing back out
    // of its own turn and in again. The swing spans the WHOLE hold as one hump — shut at each of the
    // hold's own outer edges, at its own deepest turn exactly where the hand changes which work the
    // panels read — using the very aY/aX/reach machinery every other fold on this frame already stands
    // on, so nothing new is drawn, only the fold this swing asks for. FLUTTER_DIP is how far that swing
    // gives the fold back: low enough that it reads as the panels' own turn and not a second unfold,
    // high enough that the angle actually clears HOME, so the turn is
    // seen rather than merely computed. One half back is that clearance with room held either side of
    // it — HOME sits 0.9524 of the way from 0 to MAXA, and 0.5 stops well short of it.
    var FLUTTER_DIP = 0.5;

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
    // THE HOLD'S OWN EDGE SPEED (S-03, stitched smooth 2026-08-27). `feelOf`'s own last measured
    // step, read at its own last knot and carried through the very division by SHUT_IN that `posed`
    // below reaches it by, is the rate fold is ALREADY moving at the instant the hold's swing takes
    // over — and, since SHUT_IN and `1 - SHUT_OUT` are the same number, the rate the second work's
    // own closing piece is moving at where the swing hands back to it. Built once here so the swing
    // can be built to leave and return at exactly this rate instead of at nothing.
    var FEEL_EDGE_SLOPE = (FEEL_KNOTS[FEEL_KNOTS.length - 1] - FEEL_KNOTS[FEEL_KNOTS.length - 2])
                          * (FEEL_KNOTS.length - 1) / SHUT_IN;

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
    // ---- THE RESPONSE CURVES, MEASURED ON THIS INSTRUMENT'S OWN FRAME ----------------------------
    // The charter's law: equal movement of the hand, equal felt change. Until 2026-08-17 this
    // instrument carried one measured curve and spent it on one handle — the crossing's own
    // progress — so equal steps of every OTHER handle were not equal felt change, and the composer
    // that drives five of them said so in its own report. These are the curves for the rest.
    //
    // HOW THEY WERE MEASURED, AND THE ONE THING THAT HAD TO BE GOT RIGHT. At forty-one places along
    // the raw handle the frame is drawn twice, four thousandths of the handle's own range apart,
    // and the distance between those two frames is the picture's RATE of change there. The rate is
    // then integrated along the handle and the running total inverted against the hand's own
    // twenty-one equal marks. Reading the distance between consecutive COARSE steps instead — the
    // obvious method — saturates: past a step of a few tens of 255 two frames of one photograph
    // differ by about as much however far apart they stand, and every band it measures comes out
    // near 1 whatever the truth is. The small probe is what keeps the reading a rate. All five were
    // read at a fold of 0.30 on a 390 x 844 buffer, and the largest probe any of them answered was
    // 13.7 of 255, well inside the linear reach.
    //
    // WHAT THE BAND IS. The widest felt change of one hand step against the narrowest. A band of 1
    // is the law kept exactly; the module's own raw fold measured 5.19 before its curve.
    //
    // WHICH HANDLES CARRY A CURVE, AND WHICH CANNOT. A curve belongs on a handle whose value is a
    // POSITION on a scale — the hand asks «how far along», and the instrument owes it equal change
    // per equal step. A handle whose value is a QUANTITY in its own unit — a period, an angle, a
    // count — carries none, because a curve on it would corrupt the very measurement it carries:
    // a composer that has measured the work's cutting step and asks for it must get it.
    //
    // WHICH ARE APPLIED HERE, AND WHICH ARE PUBLISHED FOR WHOEVER PLACES THE REQUEST. `field` is a
    // pure position — the score drives it with the passage's own travel and nothing else — so its
    // curve is applied here, where the module applies its own. The other four carry a unit of their
    // own as well as a position, and a composer places their requests from a measurement, so their
    // curves are PUBLISHED on the manifest beside their ranges and the placing stays with whoever
    // owns the request. Nothing is applied twice and nothing is applied silently.
    var CURVE_MEASURED_ON = "the drawn frame's own rate of change, read at forty-one places along "
                          + "the raw handle across a probe of four thousandths of its range, at a "
                          + "fold of 0.30 on a 390 x 844 buffer";
    var CURVES = {
      // band 4.017 before, 1.079 after — the world opens slowly at first and quickly at the end,
      // which is exactly what the eye saw before this was measured: at half a hand the frame had
      // barely left the closed sheet.
      field: [0, 0.0991, 0.1885, 0.2696, 0.3445, 0.4147, 0.4814, 0.5408, 0.5909, 0.6343, 0.6736, 0.7097,
                0.744, 0.7781, 0.8134, 0.848, 0.8812, 0.9135, 0.9442, 0.9731, 1],
      // band 1.174 before, 1.014 after
      tilt: [0, 0.0537, 0.1072, 0.1604, 0.2135, 0.2661, 0.3181, 0.3695, 0.4203, 0.4706, 0.5208, 0.5706,
               0.62, 0.6688, 0.7173, 0.7654, 0.8133, 0.8606, 0.9073, 0.9536, 1],
      // band 1.383 before, 1.115 after
      shade: [0, 0.0499, 0.0981, 0.1495, 0.1995, 0.2497, 0.2989, 0.3498, 0.3997, 0.4497, 0.4999, 0.5499,
                0.5999, 0.6498, 0.7001, 0.7499, 0.8003, 0.8501, 0.9002, 0.9502, 1],
      // band 2.546 before, 1.025 after
      depth: [0, 0.0771, 0.15, 0.2187, 0.2841, 0.346, 0.4048, 0.4605, 0.5137, 0.5646, 0.6132, 0.6596,
                0.7041, 0.7465, 0.7872, 0.8264, 0.8638, 0.8999, 0.9346, 0.9679, 1],
      // band 12.728 before, 1.124 after — by far the widest of the five, and the one a hand
      // feels most: at the low end of the lag the two pairs turn almost together and the frame
      // barely answers, and at the high end one pair is alone in the frame and every step tells.
      stagger: [0, 0.0406, 0.0799, 0.1177, 0.1541, 0.1894, 0.2239, 0.2577, 0.2911, 0.3239, 0.3565, 0.3891,
                  0.4221, 0.4558, 0.4939, 0.5472, 0.604, 0.6643, 0.7305, 0.8124, 1],
    };
    var CURVE_BANDS = { field: [4.017, 1.079], tilt: [1.174, 1.014], shade: [1.383, 1.115],
                        depth: [2.546, 1.025], stagger: [12.728, 1.124] };
    // One curve read at one place of the hand — the same piecewise walk `feelOf` above takes over
    // the module's own twenty-one marks, so the two are one method and not two.
    function curveAt(knots, u) {
      u = clamp(u, 0, 1);
      var n = knots.length - 1, x = u * n, i = Math.min(n - 1, Math.floor(x));
      return mix(knots[i], knots[i + 1], x - i);
    }

    // ---- THE WORLD THE SHEET OPENS INTO, IN SCRIPT ----------------------------------------------
    // HOW FAR THE PLANE TIPS when the world stands whole open. Below about forty degrees a parquet
    // reads as a flat pattern and the whole point of it is lost; past about eighty the far tiles
    // compress under one point of the buffer and the continuation turns to aliasing. Seventy is
    // inside the window and near its far end, which is where a floor reads as a floor. It is the
    // port's own number.
    var PITCH_MAX = 70;
    // The parquet's own period where a score turns the world up and says nothing about the period:
    // half the sheet each way, which is the unfold's own quarter — the sheet's four panels
    // continuing past its edge as themselves.
    var TILE_DEF = 0.5, TILE_MIN = 0.05, TILE_MAX = 1;

    // THE ROOM THE LEAN NEEDS and the room the CORNER needs on top of it — FRAG's own `EDGE` and
    // `PULL` consts (unfold.js:42, :47), carried here so the growth law can be recomputed in script.
    // Both are nothing at either door, because nothing leans and nothing turns there.
    var EDGE_JS = 1.16, PULL_JS = 1.8;
    // FRAG's own `NEAR`, carried so the door's own reading walks the eye the shader draws from.
    var NEAR_JS = 0.42;

    // The numbers of one frame, at a given flat guard. The guard is a parameter here rather than the
    // constant it was, because the hold in `values` below asks this same function for the same pose
    // at the guard a door's own grid asks for. At the module's own half degree it answers, number
    // for number, exactly what it answered before.
    function posed(st, flatDeg) {
      var dial = clamp(st.mix, 0, 1);
      var four = st.panels >= 0.5;
      var lag = clamp(st.stagger, 0, 0.6);
      // THE HAND'S FOUR STRETCHES. The first work folds shut, its own panels swing out and back to
      // leave, the hand changes hands at the hold's own middle, the second work's panels swing out and
      // back to arrive, and the second work opens out. The module's own curve runs over each of the two
      // long stretches; the two swings carry the fold themselves and ask no curve, since a curve is
      // read against a POSITION on the whole travel and a swing is a there-and-back on one spot of it.
      var fold;
      if (dial <= SHUT_IN) {
        fold = feelOf(clamp(dial / SHUT_IN, 0, 1));
      } else if (dial < SHUT_OUT) {
        // THE HOLD'S OWN SWING (S-03, stitched smooth 2026-08-27; moved off the flat instant
        // 2026-08-27 by the fresh chair audit): one smooth hump spanning the WHOLE hold, in place of
        // the two half-sine pieces that used to meet at its own middle — and PEAKING at that middle
        // rather than returning to flat there. The two half-sine pieces agreed with the flat curve
        // either side of them, and with each other at the middle, in VALUE — every join stood at fold
        // 1 — but not in the RATE fold was moving at: a sine half-cycle starts and ends at its own
        // steepest, so the swing arrived at each of its three stitches at a dead run while the curve
        // either side of it was moving at a comparative walk (measured 2026-08-26: about 4.85 a unit
        // of dial against about 39.3 a unit at HOLD = 0.08). That defect was fixed by riding a single
        // hump over the whole hold, but the hump built that day was shaped to return to fold 1 — no
        // panel standing, both works flat alike — at its own middle, which is the one instant the hand
        // changes which work the panels read: the fold's own SPEED no longer jolted, but the picture
        // at the handover was a straight cut between two full-frame photographs, which is the fault
        // the fresh chair audit of 2026-08-27 found. Naming the hump's PEAK at the middle instead — a
        // real, turned panel exactly where the hand changes hands — is the one change below.
        //
        // `y` is the dial's own place in the hold, centred and scaled so the hold's middle is 0 and
        // its two edges are ±0.5. `hHold` is the smooth part that carries fold across the hold at
        // all: it is exactly 1 at both edges, at either edge its slope is exactly `FEEL_EDGE_SLOPE`
        // (in the same dial units the curve on both sides is already moving at there) — so the join
        // carries the flat curve's own rate of travel across it rather than stopping it dead — and it
        // is exactly 1 at the middle too, where it contributes no swing of its own. `dip` is `cos`
        // squared of the hold's own turn: it is exactly nothing, AND exactly flat, at the hold's own
        // two edges (a squared cosine touches zero tangent-first there, not corner-first, which a bare
        // `Math.abs(cos(...))` does not, so the join with the outer curve is smooth in rate as well as
        // in value), and it climbs to its own peak of 1 exactly at the hold's own middle, where its own
        // slope is again exactly nothing — a turning point, not a kink, so the texture switch below
        // reads a panel standing at its most-turned angle rather than at a corner in the curve. Riding
        // it on `hHold` swings the fold away from flat across the whole hold and lands it at that
        // lowest angle exactly where the hand changes which work the panels read.
        var y = (dial - 0.5) / HOLD;
        var hHold = 1 + FEEL_EDGE_SLOPE * HOLD * y * y * (1 - 4 * y * y);
        var dip = Math.cos(Math.PI * y);
        fold = hHold - FLUTTER_DIP * dip * dip;
      } else {
        fold = feelOf(1 - clamp((dial - SHUT_OUT) / (1 - SHUT_OUT), 0, 1));
      }
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
      // THE WORLD, ON ONE ENVELOPE. lab/PARQUET-WORLD-BRIEF.md settles this: the eye's three axes
      // ride one envelope so they cannot argue with each other. Here that envelope is one handle —
      // it tips the plane, it walks the growth law back, and it is what the parquet grows in on.
      // At nothing every one of the three is nothing and the frame is the module's own, arithmetic
      // for arithmetic.
      // THE HAND ASKS «HOW FAR ALONG», AND THE CURVE ANSWERS WITH THE RAW WORLD THAT FEELS THAT
      // FAR. Both ends are exact — the curve's first knot is 0 and its last is 1 — so neither door
      // moves and every row that reads a door reads what it read before.
      var world = typeof st.field === "number" ? curveAt(CURVES.field, clamp(st.field, 0, 1)) : 0;
      // THE PLANE'S ATTITUDE RIDES THE SHEET'S OWN LEAN and is not a second rotation. `stood`
      // composes rotateZ, then rotateY, then rotateX, and the pitch is a turn about that same last
      // axis — so adding it to the lean's own X angle IS the composition, at no cost in the shader
      // and with the door's own panel-map reading picking it up for free.
      // AND THE CAMERA'S OWN TILT IS TAKEN OFF IT, so the two never turn the same plane twice. The
      // host's flight tilts the whole scene about the frame's own centre; where it already carries
      // part of the angle the world asks for, the instrument supplies only the remainder, and where
      // the flight carries the whole of it the instrument's own pitch is nothing and the plane's
      // attitude is the camera's alone — one voice on the world level, which is the levels law.
      // Read defensively: a host that hands no camera tilt leaves the angle wholly the plane's.
      var camTilt = typeof st.cameraTilt === "number" ? Math.max(0, st.cameraTilt) : 0;
      var pitch = Math.max(0, world * PITCH_MAX * DEG - camTilt);
      var tl = clamp(st.tilt, 0, 1);
      // Under reduced motion the sway is parked, so the lean stands where it starts and nothing drifts.
      var ty = st.reduced ? 0 : st.t;
      // THE SHADES ARE READ DOWN AS THE WORLD OPENS. The module's own weights — 0.97 and 0.93 at
      // full turn — describe a sheet standing alone against a dark ground, where a face turned away
      // goes to black. In a world with a floor and a light of its own, a turned face is SHADED and
      // never black; left at full it reads as a hole cut in the parquet. So the weight is walked
      // back with the world and stands at the module's own number wherever the world is shut.
      var sh = clamp(st.shade, 0, 1) * (1 - 0.55 * world);
      var open = Math.max(fR, fB);
      return {
        turn: [cY, Math.sin(aY * DEG), cX, Math.sin(aX * DEG)],
        reach: [rY, rX, fR, fB],
        form: [gate, mix(PERSP_FLAT, PERSP_DEEP, clamp(st.depth, 0, 1)), four ? 1 : 0,
               1 - smooth((open - 0.004) / 0.05)],
        // NO POINTER UNDER A SCORE (unfold.js:372-376): the module answers the hand outside it and
        // nothing else, so a scored frame is the same frame on any screen.
        lean: [gate * (tl * -4 + Math.sin(ty * 0.31) * 1.6) * DEG + pitch,
               gate * tl * Math.sin(ty * 0.23 + 1.1) * 7 * DEG,
               gate * Math.sin(ty * 0.17 + 2.2) * 1.3 * tl * DEG,
               smooth(Math.max(aY, aX) / MIRROR)],
        // A shade is cast BY the panel that is turning, so it goes out with the panel that casts it: at
        // the closed sheet the standing quarter carries none and the far door is the photograph bare.
        shade: [sh * 0.10 * fR * rY, sh * 0.97 * Math.pow(1 - cY, 0.8),
                sh * 0.93 * Math.pow(1 - cX, 0.8), sh * 0.97 * Math.pow(1 - cY * cX, 0.8)],
        crease: [0.5 * Math.sin(aX * DEG) * rX, 0.5 * Math.sin(aX * DEG) * cY * rX,
                 0.5 * Math.sin(aY * DEG) * rY, cross],
        // THE WORLD: how far it has opened, the plane's own attitude in radians, the parquet's
        // period as a share of the sheet, and the turn of its lattice in radians. The shader reads
        // the first, the third and the fourth; the second travels here so what the plane was tipped
        // by stands on the record beside what was drawn by it.
        // `pitch` is the instrument's OWN remainder; the plane's whole attitude is that plus the
        // camera's tilt, which is published beside it so a reader never has to add two records.
        cameraTilt: camTilt, planeTilt: pitch + camTilt,
        field: [world, pitch,
                typeof st.parquetPeriod === "number"
                  ? clamp(st.parquetPeriod, TILE_MIN, TILE_MAX) : TILE_DEF,
                (typeof st.parquetTurn === "number" ? st.parquetTurn : 0) * DEG],
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
    function mapReadOf(v, W, H, fit) {
      var aspect = W / Math.max(H, 1), pt = 1 / H;
      // THE SHEET THE SHADER WILL ACTUALLY BUILD. FRAG recovers it from the seating the host
      // applied (`SZ` reads `fitA`/`fitB`), and since 2026-08-17 the host hands that seating down
      // on the frame state, so this reading walks the sheet the frame is drawn with instead of the
      // smallest one a cover fit could hand. Where no seating arrives the tightest sheet stands, as
      // it did before: it is the case with the least frame to spare, so the reading can only ever
      // over-hold and never miss a bare point.
      var SZ = (fit && fit.length >= 2 && fit[0] > 0 && fit[1] > 0)
        ? [aspect / fit[0], 1 / fit[1]] : [aspect, 1];
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
      // FRAG's own `grow` and its release by the world, carried here so the reading walks the very
      // sheet the shader draws. At a world of nothing this is the plain growth law.
      var world = v.field ? v.field[0] : 0, pitch = v.field ? v.field[1] : 0;
      var grow = Math.max(Math.max(aspect / (2 * extX), 1 / (2 * extY)), 1);
      var sc = room * (grow + (1 - grow) * world);
      var d = persp * SZ[0] * sc * (1 + (NEAR_JS - 1) * world);
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
      return { walked: reads.length, bare: bare, codes: reads, seated: !!(fit && fit.length >= 2),
               sheet: [SZ[0] * sc, SZ[1] * sc],
               scale: sc, panels: four ? 4 : 2, seamPx: pt * H,
               turnPx: Math.max(sY * CW * H, sX * CH * H),
               // HOW FAR THE PLANE ITSELF STANDS OUT OF THE EYE'S OWN SQUARE, in points of this
               // grid: the sheet's own far edge carried by the pitch, read against the buffer's
               // height. At a door it is exactly 0, and anything a grid can show is a floor going
               // away rather than the photograph.
               world: world, worldPx: Math.abs(Math.sin(pitch)) * 0.5 * sc * H };
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
      // The seating of the work THIS door stands: A at the entry door and B at the exit, which is
      // exactly the pair the manifest's own `doors` block names.
      var map = mapReadOf(v, W, H, want ? st.fitA : st.fitB);
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
      // THE WORLD IS READ FIRST, BECAUSE IT IS THE CAUSE. A tipped plane opens bare points in the
      // panel map as a matter of course — that is what the parquet is there to take over — so a
      // refusal that named the bare points would be naming the symptom and leaving the reader to
      // find the reason. Where the world stands open at a door, the world is what is wrong.
      if (read.worldPx >= DOOR_SLIP) {
        return door + " door leaks: the world stands " + read.world.toFixed(6) + " open and the "
             + "plane the sheet lies in is tipped " + read.worldPx.toFixed(2) + " points" + where
             + " out of the eye's own square, so the frame is a floor running away and not the "
             + work + " work standing whole, where " + door + " door's own law asks for the "
             + work + " work at every point";
      }
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
                            turnPx: read.turnPx, world: read.world,
                            worldPx: read.worldPx } : null;
      if (!no) { v.doorWhyNo = null; return v; }
      // The hold answers ONE thing: a pair of panels standing a hair out of the sheet's plane on a
      // grid tall enough to show it. A world left open is a different fault and nothing here can
      // close it — the whole frame is a floor, not a sliver along a crease — so it is refused
      // outright and never held.
      if (read.worldPx < DOOR_SLIP
          && read.bare === 0 && read.turnPx >= DOOR_SLIP && read.turnPx < DOOR_HOLD) {
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
                         turnPx: wRead.turnPx, world: wRead.world, worldPx: wRead.worldPx };
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
      // SURFACE is not claimed. What covers the frame here is the works' own pictures, cut and carried;
      // no field of this instrument's own runs over it. Claiming it would also put this voice on the one
      // level all three landed instruments already hold, where the levels law allows a single owner.
      //   · CELL CONTENT — what a cell CARRIES. Each panel shows its own quarter of the work while
      //     it lies flat and the mirror of the quarter the sheet closes onto once it has turned, so
      //     the content of a named region changes inside the region while nothing about the region
      //     itself moves. It is read on the shader rather than asserted: the three turning panels
      //     each sample through `mix(pane(tex, CW + u), pane(tex, CW - u), uLean.w)` a few screens
      //     up, which is one panel's own point travelling from its quarter to that quarter's mirror
      //     as the sheet turns. The frame at the far door is one quarter standing alone.
      //
      // THIS DECLARATION WAS REMOVED ON 2026-08-25 AND IS RESTORED, because the argument for
      // removing it does not survive the mechanism, and the argument is worth writing down so it is
      // not made again. It ran: no handle published below asks for CELL CONTENT — `panels`,
      // `stagger`, `tilt`, `depth`, `field` and the parquet pair all shape the partition, which is
      // CELL — so a level this instrument occupies but never moves is a claim it cannot keep; and an
      // owner holds a level to the exclusion of every other cue, so claiming it would silence
      // whichever voice actually drove it.
      //
      // THE FIRST HALF IS TRUE AND IS NOT A REASON. No dial of this instrument moves what a panel
      // carries; the geometry of the turn does. But `levels` says what a voice ACTS on, and the
      // levels law exists because two voices acting on one level at one instant collide on screen.
      // A voice that acts without a dial collides exactly as hard as one that acts with a dial, so a
      // level dropped for want of a handle is a collision the law can no longer see.
      //
      // THE SECOND HALF IS NOT TRUE OF THE COMPOSER. Ownership does not go to whoever claims a
      // level; `preferredOn` (pass-composer.js) filters the group to the cues that DRIVE a handle on
      // that level and falls back to the whole group only when not one of them does. So a cue
      // declaring a level it cannot drive is passed over the moment any rival can drive it, and is
      // marked as accompanying that rival. Claiming CELL CONTENT here takes it from nobody. Where no
      // cue in the group can drive it, this one may hold it — and holding a level nobody can move
      // excludes nobody who could have moved it.
      //
      // ONE THING THIS FIELD IS BEING ASKED TO DO TWICE, left standing and written down rather than
      // repaired here, because it belongs to the levels sweep and not to this instrument. `levels`
      // says what a voice ACTS on, and the levels law reads it for collisions. The sweep also reads
      // it as the allowed set a handle's own `level:` may name — so three handles below say CELL
      // while their own sentences say WORLD: `tilt` is the sheet's lean in space, `depth` is how
      // near the eye stands to it, and the parquet's continuation is the world the sheet opens
      // into. Each falls back to CELL for no reason but that WORLD is absent from this array. Those
      // three now publish a level their own words deny, which is the same shape of defect as a level
      // dropped for want of a handle: a declaration that stays true in form while what it means has
      // moved. Either the two readings want two fields, or a handle's level wants to be free of the
      // instrument's own array.
      levels: ["CELL", "CELL CONTENT"],
      // WHERE THIS INSTRUMENT HAS A SEAM (§8's `seams` block, pass-layer.js). The sheet cuts the
      // frame into its own panels, and a panel meets its neighbour at their shared hinge. The shader
      // grows each face one point past its own hinge before it is tested — `pt = 1.0 / uRes.y` and
      // the corner it is spent at, `vec2(CW + pt, CH + ey)` and its three siblings a few lines below
      // it — with the comment standing over that very line: "A face runs one point past its hinge,
      // so the panels meet with no hairline" (unfold.js:172-175). This is a HAIRLINE case and not a
      // HANDOVER ZONE: a panel's own quarter and the mirror of the quarter it turns into already
      // meet at the same texture coordinate at the hinge by the fold's own geometry — "the mirror
      // over it" a few lines further down, `MIRROR degrees into its turn it is the mirror of the
      // quarter the sheet closes onto" — so the growth by one point buys nothing against a colour
      // mismatch and everything against the gap a sampling grid could otherwise open exactly on the
      // hinge line. `of` names no handle: the growth is pinned at one point of the buffer regardless
      // of how the sheet is posed, and no handle below counts a repeating element the width could
      // scale with — the sheet always folds into the same four panels.
      seams: [{ kind: "panel", of: null, unit: "points of the drawing buffer" }],
      params: { tilt: [0, 1], shade: [0, 1], depth: [0, 1], stagger: [0, 0.6], panels: [0, 1] },
      // WHAT THIS INSTRUMENT SHOWS BESIDES A CROSSING (his 19:13 word, the second register). The
      // sheet opening past its own edges into a parquet that continues without end, on a plane the
      // eye sees at an angle, is a transformation that reveals HOW the work was made: the period
      // the parquet repeats at is the work's own cutting step and the turn is the angle that step
      // was cut at, so what runs off to the horizon is the work's own device carried on.
      register: "process",
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
        // `mix` is the crossing's own dial and `clock` the module's own time; neither drives a
        // structural level of the picture.
        mix: { min: 0, max: 1, def: 0, level: null },
        clock: { min: 0, max: 14, def: 0, level: null },
        // The sheet's own lean is an axis of the whole sheet standing in space — a WORLD reading —
        // but WORLD is not in this instrument's own `levels` array, so this falls back to CELL, the
        // nearest declared level and the one that already carries the sheet's own global geometry.
        tilt: { min: 0, max: 1, def: 0.5,
                 curve: { knots: CURVES.tilt, band: CURVE_BANDS.tilt, applied: false,
                          measuredOn: CURVE_MEASURED_ON },
                 level: "CELL",
               },
        // The fleet's own shade judge channel; it drives no structural level.
        shade: { min: 0, max: 1, def: 1,
                 curve: { knots: CURVES.shade, band: CURVE_BANDS.shade, applied: false,
                          measuredOn: CURVE_MEASURED_ON },
                 level: null,
               },
        // The viewing distance is how near the eye stands to the sheet — a WORLD reading — but
        // WORLD is not in this instrument's own `levels` array, so this falls back to CELL, the
        // same nearest declared level `tilt` above falls back to.
        depth: { min: 0, max: 1, def: 0.5,
                 curve: { knots: CURVES.depth, band: CURVE_BANDS.depth, applied: false,
                          measuredOn: CURVE_MEASURED_ON },
                 level: "CELL",
               },
        // A phase offset between the two panel pairs' own turning: CELL.
        stagger: { min: 0, max: 0.6, def: 0.34,
                 curve: { knots: CURVES.stagger, band: CURVE_BANDS.stagger, applied: false,
                          measuredOn: CURVE_MEASURED_ON },
                 level: "CELL",
               },
        panels: { min: 0, max: 1, def: 1, kind: "enum", step: 1,
                  names: { "0": "two", "1": "four" }, level: "CELL" },
        // THE MEASUREMENT THIS HANDLE IS READ AGAINST AT A DOOR, published beside its range the way
        // the meshing instrument publishes its own. `readAtADoor` says what is read (this
        // instrument's own panel map, walked at the buffer's own sample points), on which grid (the
        // drawing buffer the host binds, with the CSS frame where it hands none), how far the hold
        // reaches (two points of that grid, for a pair standing out of the sheet's plane) and where
        // the guard the module's own constant asks for stays on the record.
        // THE THREE THAT OPEN THE WORLD, all resting at the closed sheet. `field` is the whole
        // switch and the other two cost nothing while it is shut: at nothing the plane's attitude
        // is nothing, the growth law binds, the sheet covers the frame at every point and the
        // parquet draws on no point at all — the module's own frame, arithmetic for arithmetic.
        // The world the sheet opens into is a WORLD reading by its own name, but WORLD is not in
        // this instrument's own `levels` array. The parquet is the sheet's own four panels
        // continuing past their edge as themselves — the same lattice extended without end — so
        // this falls back to CELL, the nearest declared level.
        field: { min: 0, max: 1, def: 0,
                 unit: "how far the world stands open, on the curve's own scale",
                 curve: { knots: CURVES.field, band: CURVE_BANDS.field, applied: true,
                          measuredOn: CURVE_MEASURED_ON },
                 reads: "the passage's own travel; the score walks it and it carries the plane's "
                      + "attitude, the growth law's release and the parquet's arrival on one "
                      + "envelope, which is lab/PARQUET-WORLD-BRIEF.md's own rule that the eye's "
                      + "axes ride one envelope and cannot argue",
                 applied: { pitchDegreesAtWhole: PITCH_MAX, shutAt: 0 },
                 level: "CELL" },
        // The parquet's own repeating period: CELL.
        parquetPeriod: { min: TILE_MIN, max: TILE_MAX, def: TILE_DEF,
                         unit: "a fraction of the work's own side",
                         reads: "structure.ownDevice.stepPx over the work's own frame side — the "
                              + "step the work was actually cut at, which is what makes the "
                              + "continuation the work's own device and not a pattern laid over "
                              + "it; structure.grid.periodPx over the same side where no device "
                              + "was derived",
                         level: "CELL" },
        // The lattice's own turn: CELL.
        parquetTurn: { min: 0, max: 180, def: 0, unit: "degrees",
                       reads: "structure.ownDevice.angleDeg, the angle that same step was cut at; "
                            + "structure.grid.angleDeg, the direction the work's own lattice "
                            + "varies along, where no device was derived",
                       level: "CELL" },
        // The judges' own panel-map channel: it drives no structural level.
        mask: { min: 0, max: 1, def: 0,
                applied: { readAtADoor: { points: DOOR_HOLD, readOn: "the drawing buffer",
                                          reads: "flatDegRequest",
                                          measures: "this instrument's own panel map, walked at "
                                                  + "the buffer's own sample points" } },
                level: null },
      },
      neutrals: { a: 0, b: 1 },
      doors: { in: { handle: "mix", value: 0, work: "a" },
               out: { handle: "mix", value: 1, work: "b" } },
      // Both doors frame alike, and both are the PLAIN COVER FIT: the module's repair of 2026-08-13
      // made the sheet the file cover-fitted and put the room the lean needs on the gate, which stands
      // at nothing at either end. So neither door is cropped and neither is upscaled.
      framings: { "0": { coverCrop: 1 }, "1": { coverCrop: 1 } },
      surface: { type: "hinged-panel-sheet", anchor: "measured-hang",
                 tessellation: { panels: "panels", field: "field" }, cameraAuthority: "stage",
                 entry: { mix: 0, work: "a", pose: "flat" },
                 exit: { mix: 1, work: "b", pose: "flat" } },
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
                     + "alpha is the constant 1; where the world opens the growth law is walked back "
                     + "and the plane the sheet lies in takes over — the parquet up to the eye's own "
                     + "horizon and the world's light past it — so the frame stays filled by the "
                     + "same law read one step further out" },
      // The neutral pose is the ENTRY DOOR — `mix` at 0, the value the `doors` block above names —
      // so the frame keys the host reads off it at registration include the door's own record.
      neutralPose: { mix: 0, tilt: 0.5, shade: 1, depth: 0.5, stagger: 0.34, panels: 1, mask: 0,
                     field: 0, parquetPeriod: TILE_DEF, parquetTurn: 0, cameraTilt: 0,
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
          { name: "uField", type: "vec4", source: "frame:field" },
        ],
      }],
      // The instrument allocates nothing of its own: it spends the two source-texture slots the host
      // already holds and the one programme the host builds from this manifest. The module's own DOM
      // stage — a perspective container, a sheet, four panels, seven faces, four gradients and three
      // creases — is what this port does without.
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
                   programs: 1, passes: 1, bytesEstimate: 2000156, variant: "lean" },
                   standard: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0,
                               programs: 1, passes: 1, bytesEstimate: 8000156,
                               variant: "standard" },
                   rich: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                           passes: 1, bytesEstimate: 32000156, variant: "rich" } },
      capabilities: ["webgl2"],
      decline: ["one work only", "a source that never decoded"],
      provenance: { labPath: "lab/effects/unfold.js", commit: "4c7dfe4",
                    sha256: "28688b86686a12b57c9fbc4dd9775350d77f9906681b1f4aff57e20dd6f71408" },
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
      suits: { reads: ["structure.ownDevice.confidence", "structure.ownDevice.stepPx"],
               how: "it reveals how a work was made, so the fit is how legibly the making READS — "
                  + "the clearer of the two works' device confidences, which is what a confidence "
                  + "is for; it is nothing where neither work carries a measured step to open on" },
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
          // The world, straight to the pose. A score that names none of the three leaves the sheet
          // closed on itself, which is the module's own frame.
          field: h.field, parquetPeriod: h.parquetPeriod, parquetTurn: h.parquetTurn,
          // THE CAMERA'S OWN TILT AND BOTH WORKS' SEATING, as the host hands them down since
          // 2026-08-17. The tilt is taken off the plane's attitude so the two do not double; the
          // seating lets the door's own reading walk the sheet the shader will actually build,
          // rather than the smallest one a cover fit could hand. Both are read defensively, so a
          // host that carries neither draws exactly what it drew before.
          cameraTilt: st.camera && typeof st.camera.tilt === "number" ? st.camera.tilt : 0,
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
        // decision asks for rather than the flat guard the module carries. `moved` is how far the
        // guard had to open past the module's own half degree for this grid to show the sheet flat.
        if (h.mix === 0 || h.mix === 1) {
          var v = values(pose);
          if (st.reportApplied) {
            st.reportApplied({
              door: h.mix === 0 ? "in" : "out",
              buffer: [pose.bufWidth, pose.bufHeight],
              reads: "flatDeg", request: v.flatDegRequest, applied: v.flatDeg,
              moved: v.flatDeg - v.flatDegRequest, unit: "degrees",
              // What the plane itself was doing at this door, in the grid's own points, so a door
              // held whole says so about the world as well as about the panels.
              world: v.panelMap ? v.panelMap.world : null,
              worldPx: v.panelMap ? v.panelMap.worldPx : null,
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
    instrument: unfoldInstrument(),
  });
})();
