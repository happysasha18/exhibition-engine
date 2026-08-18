/*!pass-inst-parquet.js*/
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
// OWNERSHIP. This instrument was carried over from lab/effects/parquet.js. The artistic instruments
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
  // THE MIRROR-FLOOR INSTRUMENT (§8) — lab/effects/parquet.js carried across
  // ================================================================================================
  // WHAT THE VISITOR SEES. The photograph stands whole and frontal, filling the frame. It tips away
  // into a floor tiled with itself: every tile flipped against the one beside it, so the seams close
  // and the pattern runs on without an edge, receding toward a horizon beyond the top of the frame.
  // Then the floor hands the room over. Beginning where it runs off toward the horizon and coming
  // forward to the row standing under the eye, each tile's top sheet turns up on the tile's own far
  // edge the way a blind rolls up, and the second photograph — already laid under the first, tile
  // for tile, in the same mirrored pattern — stands open under it. Each lifting sheet throws its
  // shadow forward onto the work it has just uncovered. The floor lays back flat, and the second
  // photograph stands whole. Flat, world, flat: one layer the whole way, no seam anywhere and no
  // fade anywhere.
  //
  // WHY IT STANDS HERE. His word of 2026-08-18 08:52, after walking the live route — the transitions
  // are all alike, the arsenal is full and only a corner of it plays — and his word of 08:58, carry
  // the WHOLE arsenal across and recompose the walk. The charter's vocabulary carries this module by
  // name with his own standing verdict on it: «как все плавно работает и перспектива изменяется»
  // (09:42), level SURFACE+CELL, role both. The composer's own `MISSING_INSTRUMENT` names the gap
  // this fills — «an instrument that cuts on tiles, for tile_crossfade» — and that entry has stood
  // unanswered since the map was written.
  //
  // ------------------------------------------------------------------------------------------------
  // HOW THIS DIFFERS FROM THE PARQUET THE UNFOLD ALREADY CARRIES
  // ------------------------------------------------------------------------------------------------
  // pass-inst-unfold.js grew a parquet register of its own on 2026-08-17, and the two are genuinely
  // different acts rather than one act played twice. Four differences, each of them structural:
  //
  //   · WHAT IS DRAWN. The unfold's parquet is a BACKDROP: it draws only where no panel of its sheet
  //     stands, past the sheet's own rectangle, and inside the sheet it never draws at all. This
  //     instrument's floor IS the frame, at every point, from one door to the other; there is
  //     nothing else in the picture.
  //   · HOW MANY WORKS THE PARQUET ITSELF CARRIES. The unfold's continuation repeats ONE work — the
  //     sheet's own — and the crossing happens elsewhere, on the closed sheet, as a dissolve between
  //     two flat pictures. Here the parquet carries BOTH: the arriving work is laid under the
  //     departing one tile for tile from the first frame, and the crossing IS the floor handing the
  //     room over, tile by tile, by the geometry of each sheet turning up on its hinge. Nothing
  //     fades and no two pictures are ever mixed except across the last sliver of one sheet's swing.
  //   · WHAT IT CUTS ON. The unfold cuts on `panel` — the four hinged quarters of its sheet. This
  //     cuts on `tile`, which is the kind the composer's own map has never had an instrument for.
  //   · WHAT A SCORE HAS TO DO TO GET IT. The unfold's world is a second handle, `field`, which a
  //     score must drive and which the unfold REFUSES at a door. Here the whole arc rides the dial:
  //     the floor rises out of the flat photograph, hands the room over and lays back down on `mix`
  //     alone, and both doors are exact by construction at every value of every other handle.
  //
  // ------------------------------------------------------------------------------------------------
  // WHAT CAME OVER, AND WHAT STAYED BEHIND
  // ------------------------------------------------------------------------------------------------
  // WHAT CAME OVER, digit for digit: the mirror counted from the middle tile, so the tile the dry
  // door stands on carries the photograph the way it was taken; the floor's own deepest lean and the
  // eye's own distance over it; the crop a tile shows at the wet end; the three shares the arrival
  // is spent in and the die that scatters them; how far a sheet swings and where in its swing it
  // starts to go; the slant this floor's light stands at and how dark the contact shadow goes at a
  // sheet's foot; the floor's own falling-off light and its vignette; and the module's own measured
  // response curves, both of them — the logarithmic curve on the floor's lean and the arc on the
  // arrival, with the fitted numbers the module carries.
  //
  // WHAT STAYED BEHIND: the module's own stage and its hundred-and-twenty-one elements, its frame
  // loop, its resize timer, its pointer — the lifting of tiles under a hand, the sheen that follows
  // it, the press — and its slow camera drift and breath. All of those are the module's own life on
  // a page it owns. A scored passage is composed at visit time from the two works' records and the
  // walk's live state, and a picture that answered a pointer would not be the same picture on two
  // screens; the module says as much itself, where it puts the hand off the floor entirely the
  // moment a score takes the pose.
  //
  // THE PORT'S OWN ONE REPAIR, and the reason it is the port's. The module draws each tile SQUARE
  // and paints the photograph into it with `background-size: <bg> <bg>` — two equal lengths, which
  // stretches the picture to a square. On a frame that is not square its dry door is therefore not
  // the work as the file carries it but the work squashed, and the door law of this engine is
  // absolute. So the tile here takes THE FRAME'S OWN SHAPE: at the dry door one tile is the frame
  // exactly and carries the source cover-fitted, which is the door. It is the same class of repair
  // the unfold module made for itself on 2026-08-13, and the measurement is in this port's report.
  //
  // ------------------------------------------------------------------------------------------------
  // THE COVERAGE: THIS INSTRUMENT FILLS THE FRAME
  // ------------------------------------------------------------------------------------------------
  // §7's coverage law of 12:40 asks every instrument to say where its own matter is absent. It is
  // absent nowhere, and the reason is a proof rather than a claim. The floor has no edges — past its
  // own tile the mirror simply carries on, one triangle wave per axis, which is the same law the
  // pattern is built by — so the only place a point of the frame can fail to land on it is BEYOND
  // THE HORIZON. The horizon of a plane tipped by θ and seen from a distance D stands at D·cot θ
  // above the frame's own middle, in half-frame units; the frame's top edge is at 1. This floor's
  // deepest lean is 30 degrees, the module's own, and the eye's distance is the module's own rule
  // rather than a number — 3 half-frames on a frame no taller than it is wide, coming in as the
  // frame narrows — with a guard under it that holds the eye no closer than tan 30 times the room
  // the horizon is given. So the horizon stands at least a quarter of a frame clear of the top edge
  // whatever shape the frame is: on a 390 x 844 phone it stands at 2.40 against a top edge at 1, and
  // on a square frame at 5.196. There is no sky in this picture and there cannot be. The alpha is
  // the constant 1, said as a decision; the door's own reading walks the buffer's sample points and
  // refuses a door where any of them stands off the floor.
  function parquetInstrument() {
    var VERT = [
      "attribute vec2 aPos;",
      "varying vec2 vUv;",
      "void main(){ vUv = vec2(aPos.x * 0.5 + 0.5, 0.5 - aPos.y * 0.5); gl_Position = vec4(aPos, 0.0, 1.0); }",
    ].join("\n");

    // ----------------------------------------------------------------------------------------------
    // THE SHADER — the module's own DOM read backwards
    // ----------------------------------------------------------------------------------------------
    // The module builds one plane, N by N tiles, each tile a stack of four surfaces: the arriving
    // work underneath, the shadow the lifting sheet throws on it, the sheet itself carrying the
    // departing work, and the floor's own shading over both. Every one of those is a pure function
    // of where a point of the frame falls on the plane, so the whole stack is read here per pixel
    // and nothing is built.
    var FRAG = [
      "precision highp float;",
      "varying vec2 vUv;",
      "uniform sampler2D uA;",             // the work the room belongs to
      "uniform sampler2D uB;",             // the work it is being handed to
      "uniform vec4 uFitA;",
      "uniform vec4 uFitB;",
      "uniform vec2 uRes;",
      // THE FLOOR'S POSE: how far the floor stands open, the sine and cosine of its lean, and the
      // eye's own distance over it in half-frames. The first is nothing at either door, and with it
      // nothing the other three describe a plane that is not tipped at all.
      "uniform vec4 uPose;",
      // THE LATTICE: the zoom that carries one tile to the whole frame, the tile's own two sides in
      // plane units, and the angle the lattice is cut at.
      "uniform vec4 uLat;",
      // THE ARRIVAL: how far the front has come, the die the tiles' own moments are scattered by,
      // the crop a tile shows of the picture, and the weight of this floor's own light.
      "uniform vec4 uArr;",
      // The judges' channel: the tile map as colour.
      "uniform float uMask;",
      // ---- the module's own numbers, carried digit for digit ------------------------------------
      // THE THREE SHARES THE ARRIVAL IS SPENT IN, and they add to exactly one, which is what makes
      // both doors exact: at nothing no tile has started, because every start is at or above zero;
      // at one every tile has finished, because the latest start is SPREAD + SCATTER and it has
      // SWING left to run (parquet.js:222-224).
      "const float SPREAD = 0.56;",
      "const float SWING = 0.30;",
      "const float SCATTER = 0.14;",
      // HOW FAR A SHEET SWINGS — a little past standing, so it passes edge-on and goes over rather
      // than stopping upright in the frame — and where in its own swing it starts to go, by which
      // point the uncovering is already done by the hinge and what leaves is a foreshortened sliver
      // (parquet.js:227-231).
      "const float TIP = 96.0;",
      "const float GONE = 0.72;",
      // THE PERSPECTIVE ONE SHEET TURNS UNDER, in tile heights (parquet.js:360, `tile * 4.4`). It is
      // what carries a turning sheet's near edge toward the eye and draws it LONGER than the plain
      // cosine: at 45 degrees the edge stands at 0.843 of the tile, not 0.707.
      "const float PP = 4.4;",
      // THE FLOOR'S OWN DEEPEST LEAN, as its cosine and its sine. The seat below is read at THIS
      // lean and never at the lean standing this frame, so the order the floor turns over in is
      // settled once and does not walk as the floor rises. The module settles it once too, at build,
      // and for the same reason (parquet.js:386-399).
      "const float WCO = 0.8660254;",
      "const float WSI = 0.5;",
      // THE LIGHT OVER THIS FLOOR stands about 61 degrees above it, from beyond the horizon, so a
      // standing sheet throws its shadow forward onto the work it has just uncovered. This is that
      // slant, and how dark the shadow goes at the sheet's own foot (parquet.js:232-240).
      "const float SLANT = 0.55;",
      "const float CAST = 0.68;",
      // The floor's own shading at rest and how much of it the distance adds (parquet.js:110, :644).
      "const float BASE_SHADE = 0.17;",
      "const float DEPTH_SHADE = 0.32;",
      // The three colours the module paints with: the shadow a sheet throws, the floor's own shade,
      // and the vignette's black (parquet.js:24, :35, :39).
      "const vec3 CASTC = vec3(0.0118, 0.0235, 0.0353);",
      "const vec3 SHADEC = vec3(0.0157, 0.0275, 0.0392);",
      // THE DIE IN THE FRAME. weave's own hash, written for plain numbers, so the two modules roll
      // the same way (parquet.js:70-73, and lab/effects/weave.js:58).
      "float hash21(float x, float y){",
      "  float s = sin(x * 41.317 + y * 289.107) * 43758.5453;",
      "  return s - floor(s);",
      "}",
      // A work carries its source cover-fitted over the whole tile, so a tile standing at the frame
      // IS the file cover-fitted, which is the door.
      "vec2 into(vec2 p, vec4 f){",
      "  return clamp((p - 0.5) * f.xy + 0.5 + f.zw, 0.0008, 0.9992);",
      "}",
      // WHERE ONE POINT OF THE FRAME FALLS ON THE FLOOR. The plane is tipped by θ about the frame's
      // own horizontal axis and seen from a distance D, so a plane point (u, v) — v running AWAY
      // from the eye, toward the horizon — stands on the frame at (u, v·cosθ) / (1 + v·sinθ/D). This
      // is that read backwards, and it is exact rather than a search: one divide answers it.
      // `w` is the projection's own divisor, which is 1 in the frame's own plane and grows without
      // bound toward the horizon, so it is what says how far away a tile ended up.
      "bool onFloor(vec2 s, float co, float si, float D, out vec2 q, out float w){",
      "  float den = co - s.y * si / D;",
      "  q = vec2(0.0); w = 1.0;",
      "  if (den <= 1e-5) return false;",           // beyond the horizon: not on the floor at all
      "  float v = s.y / den;",
      "  w = 1.0 + v * si / D;",
      "  q = vec2(s.x * w, v);",
      "  return true;",
      "}",
      "void main(){",
      "  float aspect = uRes.x / max(uRes.y, 1.0);",
      // the screen point in frame units: x across, y UP, so the top edge is +1 and the floor runs
      // off toward it
      "  vec2 sp = vec2((vUv.x - 0.5) * 2.0 * aspect, 1.0 - vUv.y * 2.0);",
      "  float open = uPose.x, co = uPose.y, si = uPose.z, D = uPose.w;",
      "  vec2 q; float w;",
      "  bool on = onFloor(sp, co, si, D, q, w);",
      // THE ZOOM. At the dry door the floor is scaled up until ONE tile fills the frame, which is
      // how the module's own dry door stands (parquet.js:358, `doorS`); as the floor opens the zoom
      // walks back to 1 and the lattice's own count stands across the frame. Dividing the plane
      // coordinate by it is the same thing as scaling the floor, so a tile keeps its own index the
      // whole way and the front never re-tiles under itself.
      "  vec2 P = uLat.yz;",
      "  vec2 g = q / max(uLat.x, 1e-4);",
      // the lattice's own turn, taken about the floor's own centre so it pivots where the work does
      "  float ct = cos(uLat.w), st = sin(uLat.w);",
      "  vec2 r = vec2(g.x * ct + g.y * st, -g.x * st + g.y * ct);",
      // WHICH TILE, AND WHERE INSIDE IT. The lattice is counted FROM THE MIDDLE TILE — the half
      // period below is the whole of that — so the tile the dry door stands on is the identity tile
      // and carries the photograph the way it was taken (parquet.js:440-447).
      "  vec2 t = (r + P * 0.5) / P;",
      "  vec2 idx = floor(t);",
      "  vec2 loc = t - idx;",
      // THE MIRROR: every second column flipped across, every second row flipped down. This is one
      // triangle wave per axis and nothing else — the same fold the unfold's own continuation uses,
      // read here as the parity of the tile's index, which is the same number.
      "  vec2 par = mod(idx, 2.0);",
      "  vec2 mir = mix(loc, 1.0 - loc, par);",
      // WHEN THIS TILE'S OWN SHEET STARTS TO GO. Its place in the frame first — 0 where the floor
      // runs off toward the horizon, 1 under the eye — and its own moment out of the die on top of
      // that, so the front is a ragged band and not a ruled line (parquet.js:481-488).
      //
      // THE SEAT IS READ AT THE FLOOR'S OWN DEEPEST LEAN, not at the lean standing this frame, so
      // the order the floor turns over in is settled once and does not walk as the floor rises. The
      // module settles it once too, at build, and for the same reason.
      "  float cv = idx.y * P.y;",
      "  float sy = cv * WCO / (1.0 + cv * WSI / D);",
      "  float seat = clamp((1.0 - sy) * 0.5, 0.0, 1.0);",
      "  float start = seat * SPREAD + hash21(idx.x + uArr.y + 19.7, idx.y + uArr.y - 7.3) * SCATTER;",
      "  float a = clamp((uArr.x - start) / SWING, 0.0, 1.0);",
      // HOW FAR THIS TILE'S SHEET HAS TURNED, and where its own near edge has landed. NOT the plain
      // cosine: the sheet turns under a perspective of its own, which carries its near edge toward
      // the eye and draws it longer, and a shadow drawn at the cosine would begin underneath the
      // sheet and never be seen (parquet.js:576-584).
      "  float th = TIP * a * 0.0174532925;",
      "  float sth = sin(th), cth = cos(th);",
      "  float foot = clamp(cth * PP / max(PP - sth, 1e-4), 0.0, 1.0);",
      // where this point stands along the tile, measured FROM THE HINGE, which is the tile's own far
      // edge — the one toward the horizon
      "  float f = 1.0 - loc.y;",
      // WHAT THE SHEET SHOWS AT THIS POINT. The same projection inverted: a point standing `f` of
      // the tile from the hinge on the screen carries the sheet's own content at `gg` from the
      // hinge, and at a swing of nothing the two are the same number, which is the door.
      "  float gg = f * PP / max(cth * PP + f * sth, 1e-4);",
      "  vec2 locS = vec2(loc.x, 1.0 - gg);",
      "  vec2 mirS = mix(locS, 1.0 - locS, par);",
      // THE CROP a tile shows of the picture: the whole of it at the dry door, the central 0.80 of
      // it at the floor's deepest — one number for the floor, so the crop travels with the lean and
      // the two cannot disagree (parquet.js:105, :603).
      "  float crop = uArr.z;",
      // A TILE'S OWN SECOND COORDINATE RUNS UP THE FLOOR AND AN IMAGE'S ROWS RUN DOWN IT, so it is
      // turned over here — once, at the one place a picture is read — or the whole floor stands on
      // its head. The mirror above is counted in the tile's own coordinate and is untouched by it.
      "  vec2 tex = vec2(mir.x, 1.0 - mir.y);",
      "  vec2 texS = vec2(mirS.x, 1.0 - mirS.y);",
      "  vec3 under = texture2D(uB, into((tex - 0.5) * crop + 0.5, uFitB)).rgb;",
      "  vec3 sheet = texture2D(uA, into((texS - 0.5) * crop + 0.5, uFitA)).rgb;",
      // WHY THIS IS NOT A CROSSFADE. What uncovers the arriving work is the GEOMETRY of the sheet
      // turning up on its hinge — at half its swing the sheet has already given up a third of its
      // tile — and the frame is covered at every moment by one work or the other. The sheet's own
      // weight only goes out in the last stretch of its swing, where it is edge-on and worth a
      // sliver of the tile (parquet.js:212-216, :577).
      "  float o = a < GONE ? 1.0 : (1.0 - a) / (1.0 - GONE);",
      "  float onSheet = step(f, foot) * step(0.0, f);",
      "  vec3 col = mix(under, sheet, onSheet * o);",
      // THE SHADOW THE LIFTING SHEET THROWS. It begins where the sheet's own edge lands and reaches
      // as far as this floor's light is slanted, and it lies on the work the sheet has just
      // uncovered. The three stops are the module's own gradient (parquet.js:24).
      "  float reach = SLANT * sth;",
      "  float ct2 = clamp((f - foot) / max(reach, 1e-4), 0.0, 1.0);",
      "  float grad = ct2 < 0.44 ? mix(0.66, 0.38, ct2 / 0.44) : mix(0.38, 0.0, (ct2 - 0.44) / 0.56);",
      "  float castA = CAST * sth * o * grad * step(foot, f) * step(f - foot, reach);",
      "  col = mix(col, CASTC, clamp(castA, 0.0, 1.0));",
      // THE FLOOR'S OWN LIGHT FALLING OFF WITH DISTANCE, read off the projection's own divisor at
      // the tile's own place, so the far side of the floor goes darker a tile at a time the way the
      // module shades it (parquet.js:641-644). It is weighted by how far the floor stands open, so
      // at the dry door nothing is shaded at all.
      "  float wc = 1.0 + cv * si / D;",
      "  float dep = clamp((wc - 1.0) * 2.0, -0.75, 1.0);",
      "  float sh = uArr.w * open * (BASE_SHADE + DEPTH_SHADE * dep);",
      "  col = mix(col, SHADEC, clamp(sh, 0.0, 1.0));",
      // THE VIGNETTE the module lays over its whole stage, which is what makes the floor read as a
      // room rather than as a pattern (parquet.js:38-39). It rides the same opening, so the dry door
      // carries none of it.
      "  vec2 vg = vec2((vUv.x - 0.5) / 0.78, (vUv.y - 0.46) / 0.80);",
      "  float vr = length(vg);",
      "  float va = vr < 0.40 ? 0.0",
      "           : (vr < 0.72 ? mix(0.0, 0.18, (vr - 0.40) / 0.32)",
      "                        : mix(0.18, 0.62, clamp((vr - 0.72) / 0.28, 0.0, 1.0)));",
      "  col *= 1.0 - va * open;",
      // THE TILE MAP, the judges' own frame: which work stands at this point of the frame, whether
      // it stands under a sheet or open, and where in its own tile. It is BLACK exactly where no
      // tile stands — which the crop above makes impossible — so a row reads off the picture whether
      // the floor kept its promise, and it carries no coverage of its own because what it is for is
      // to be read as colour.
      "  float code = on ? (onSheet > 0.5 ? 0.5 : 1.0) : 0.0;",
      "  vec2 lc = onSheet > 0.5 ? texS : tex;",
      "  vec3 judge = vec3(code, clamp(lc.x, 0.0, 1.0), clamp(lc.y, 0.0, 1.0));",
      "  col = mix(col, judge, uMask);",
      // THE COVERAGE: the alpha is the constant 1, and it is a decision rather than a default. The
      // floor has no edges and its horizon stands five frames above the frame's own top edge, so
      // this instrument has no absence to publish and stands as the ground a stack is laid on.
      "  gl_FragColor = vec4(col, 1.0);",
      "}",
    ].join("\n");

    var DEG = Math.PI / 180;

    function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }

    // ---- THE MODULE'S OWN NUMBERS, carried digit for digit ----------------------------------------

    /* HOW FAR THE FLOOR LEANS when it stands whole open, in degrees. The module's own two terms: a
       permanent touch of floor recession and the whole of the lean its camera reaches, which
       together are the grazing pitch the crown was judged at (parquet.js:107-108, :121, and the
       charter's shelf 8 — «keep all three pitches, В7 grazing best»). */
    var BASE_X = 11, LEAN = 19;
    var PITCH_MAX = BASE_X + LEAN;                 // 30 degrees

    /* HOW FAR BACK THE EYE STANDS OVER THE FLOOR, in half-frames — and this one is a RULE and not a
       number, because the module's own is. It writes `max(720, min(W, H) * 1.5)` in pixels
       (parquet.js:359), which read in half-frames is 3 on a frame no taller than it is wide and
       3 · aspect on a taller one: the eye comes IN as the frame narrows, which is what keeps a phone
       frame a room rather than a wallpaper. That rule is carried; the module's own floor of 720
       pixels is not, because a pixel count means one thing on a mount the module sizes itself and
       another on a drawing buffer the host scales by the device ratio, so it would be a number read
       off the wrong thing.

       AND THE PORT'S OWN GUARD IN ITS PLACE. The coverage below is a proof, and the proof needs the
       horizon to stand clear of the frame's own top edge: the horizon of a plane tipped by θ stands
       at D·cot θ above the frame's middle, and the top edge stands at 1. So the eye is held no
       closer than tan θ times the room the horizon is given, which puts the horizon a quarter of a
       frame clear at the deepest lean this instrument reaches whatever shape the frame is. On a
       390 x 844 phone the rule answers 1.386 and the guard 0.722, so the rule stands and the horizon
       is 2.40 half-frames above a top edge at 1. */
    var EYE_D_LONG = 3.0;
    var HORIZON_ROOM = 1.25;

    /* WHAT A TILE SHOWS OF THE PICTURE at the floor's deepest: the central 80 per cent of it
       (parquet.js:105). At the dry door the crop opens to the whole picture, so the door is the file
       and nothing else. */
    var CROP = 0.80;

    /* HOW MANY TILES STAND ACROSS THE FLOOR, at the module's own three bounds (parquet.js:81, and
       the charter's own taste-approved vista preset «parquet 5/12», which is this count at 5). */
    var TILES_MIN = 3, TILES_MAX = 11, TILES_DEF = 5;

    /* HOW FAR THE FLOOR TURNS ACROSS THE WHOLE PASSAGE, in degrees, where a score names nothing.
       The module spins its floor on a clock — the vista preset's `turn` of 12 is 0.9 degrees a
       second (parquet.js:287) — and this engine hands an instrument no clock it may keep. So the
       module's own approved rate is carried at this engine's own pass duration of 6.5 seconds, which
       is 5.85 degrees over the whole dial. It is the one handle here that names no measurement, and
       it is written down as that in this port's report rather than passed off as read. */
    var SPIN_DEF = 5.85;
    var SPIN_MAX = 30;

    /* THE RESPONSE CURVE OF THE FLOOR'S OWN LEAN (DARKROOM-DRAFT D2, the equal-felt-change law;
       parquet.js:293-320). MEASURED by the module and carried whole, family and fitted number both.
       The floor is nearly still while the eye stands over it and bolts as the eye pitches toward
       grazing, which is the perspective itself: the picture a plane throws grows as 1/cos of the
       pitch, so the change per degree is a RATIO and not a difference — which is why the family is
       logarithmic. v = (e^(ku) - 1)/(e^k - 1), with k = -2.9 the one fitted number, k negative
       because the raw travel is slow at the start. The module measured a band of 5.62 raw and 1.98
       with the curve in force. Both ends are exact — feel(0) is 0 and feel(1) is 1 — so no door
       moves. */
    var FEEL_K = -2.9;
    function feel(u) {
      return (Math.exp(FEEL_K * clamp(u, 0, 1)) - 1) / (Math.exp(FEEL_K) - 1);
    }

    /* THE RESPONSE CURVE OF THE ARRIVAL (DARKROOM-DRAFT D2 again; parquet.js:243-267). MEASURED
       FIRST and then fitted, and the measurement decided the family: this handle does not take the
       lean's curve just because it stands in the same module. The front's road is a TRAPEZIUM —
       nothing is in flight at either end, the population of turning sheets grows over the first
       stretch, holds level through the middle and drains over the last — and a curve that levels a
       trapezium has to be INFINITELY steep at both ends, which no exponential and no power of the
       handle can be. The arc can: arccos(1 - 2u)/pi is the inverse of the raised cosine and its
       slope runs to infinity at 0 and at 1. W = 1.24 is the one fitted number, the share the arc is
       mixed with the straight handle at; the module measured a band of 37.9 raw and 2.34 with the
       curve in force, against the arsenal's ceiling of 2.5. W above one leans past the pure arc and
       stays rising all the way, so the handle never turns back. */
    var ARRIVE_W = 1.24;
    function arriveFeel(u) {
      var c = 1 - 2 * clamp(u, 0, 1);
      if (c < -1) c = -1; else if (c > 1) c = 1;
      return (1 - ARRIVE_W) * clamp(u, 0, 1) + ARRIVE_W * Math.acos(c) / Math.PI;
    }

    // The three shares the arrival is spent in, carried here as well as in the shader because the
    // door's own reading walks them (parquet.js:222-224).
    var SPREAD = 0.56, SWING = 0.30, SCATTER = 0.14;

    // The die, weave's own hash written for plain numbers, carried so the reading rolls exactly what
    // the shader rolls (parquet.js:70-73).
    function hash21(x, y) {
      var s = Math.sin(x * 41.317 + y * 289.107) * 43758.5453;
      return s - Math.floor(s);
    }

    // Cover-fit a work into the frame, and nothing beyond it. At either door one tile stands at the
    // frame exactly and carries the source cover-fitted, so this port asks the host for no crop and
    // `framings` publishes 1 at both ends.
    function fit(iw, ih, w, h) {
      var fa = w / Math.max(h, 1);
      var ia = iw / Math.max(ih, 1);
      if (ia > fa) return [fa / ia, 1, 0, 0];
      return [1, ia / fa, 0, 0];
    }

    /* THE ONE ENVELOPE THE WHOLE PASSAGE RIDES, AND THE PORT'S OWN ONE NUMBER.
       lab/PARQUET-WORLD-BRIEF.md's own rule is that the eye's axes ride ONE envelope so they cannot
       argue with each other, and the module's own shape is the charter's — flat, world, flat, one
       layer the whole way. Here that shape is spent on the dial: the floor rises out of the flat
       photograph over the first RISE of it, stands at its deepest while the room changes hands, and
       lays back down over the last RISE.

       RISE IS A QUARTER, and the reason is the manifest's own three roles rather than taste: this
       instrument declares `disassembly`, `mystery`, `assembly`, and a quarter, a half and a quarter
       is what those three ask for. The number is the port's and nothing measured it; it is on the
       revisit list in this port's report.

       WHY THE TWO CURVES ARE APPLIED TO PLAIN RAMPS AND NOT TO THE SHAPE. Each of the module's two
       measured curves converts a HAND POSITION into the raw value that feels that far along, so it
       levels the felt change only when it is handed a ramp that runs at a constant rate. Laying one
       over a shape already curved would curve it twice, and the measurement would stop meaning
       anything. So the floor's own curve is applied to the rise's own ramp, the arrival's to the
       middle's own ramp, and the shape is the three plain stretches those ramps stand in. Both ends
       of both curves are exact, which is what makes both doors exact.

       AND THE FLOOR STANDS STILL WHILE THE ROOM CHANGES HANDS, which is the module's own reading:
       the front crosses a floor, and a floor that were still rising under it would put two events
       on one stretch of the hand. The floor's own slow turn goes on through the middle, so no
       stretch of the passage stands with nothing moving in it. */
    var RISE = 0.25;
    function openAt(u) {
      u = clamp(u, 0, 1);
      return feel(clamp((u <= 0.5 ? u : 1 - u) / RISE, 0, 1));
    }
    function arriveAt(u) {
      return arriveFeel(clamp((clamp(u, 0, 1) - RISE) / (1 - 2 * RISE), 0, 1));
    }

    // THE NUMBERS OF ONE FRAME. Every one of them is a pure function of the pose, and every number
    // in the pose comes from a handle a score drives, so a seeded run repeats to the pixel.
    function posed(st) {
      var dial = clamp(st.mix, 0, 1);
      // how deep the room goes at the middle of the passage. It cannot move a door — the envelope is
      // nothing at both ends whatever it is multiplied by — so a score may hold the floor flatter
      // without the doors ever noticing.
      var depth = clamp(typeof st.depth === "number" ? st.depth : 1, 0, 1);
      var open = openAt(dial) * depth;
      var pitch = PITCH_MAX * open * DEG;
      // the lattice's count, held to the module's own three bounds and to odd counts, so the middle
      // tile is a tile and not a seam (parquet.js:340-343)
      var n = Math.round(typeof st.tiles === "number" ? st.tiles : TILES_DEF);
      if (n % 2 === 0) n += 1;
      n = clamp(n, TILES_MIN, TILES_MAX);
      // THE ZOOM. One tile at the frame's own size at the dry door, the whole lattice at the wet
      // end. It is the module's own `doorS` read as a ratio rather than as a pixel count.
      var zoom = n + (1 - n) * open;
      var aspect = Math.max(st.cssWidth, 1) / Math.max(st.cssHeight, 1);
      var grid = gridOf(st);
      if (grid.given) aspect = grid.w / Math.max(grid.h, 1);
      // THE TILE'S OWN TWO SIDES, in plane units. It takes THE FRAME'S OWN SHAPE — the port's one
      // repair — so that at the dry door one tile is the frame exactly and the door is the file.
      var px = 2 * aspect / n, py = 2 / n;
      // THE EYE'S OWN DISTANCE, from the frame's own shape and from the guard the coverage proof
      // needs. Both are stated where the two constants above are declared.
      var eye = Math.max(EYE_D_LONG * Math.min(aspect, 1),
                         Math.tan(PITCH_MAX * DEG) * HORIZON_ROOM);
      // the lattice's own turn, and the floor's own slow turn across the passage on top of it. Both
      // ride the opening, so at either door the lattice stands square and neither can move a door.
      var lat = ((typeof st.lattice === "number" ? st.lattice : 0)
                 + (typeof st.spin === "number" ? st.spin : SPIN_DEF) * dial) * open * DEG;
      var arrive = arriveAt(dial);
      return {
        pose: [open, Math.cos(pitch), Math.sin(pitch), eye],
        lat: [zoom, px, py, lat],
        arr: [arrive, typeof st.seed === "number" ? st.seed : 0,
              1 / (1 + (1 / CROP - 1) * open),
              clamp(typeof st.shade === "number" ? st.shade : 1, 0, 1)],
        // read on the diagnostic surface, bound to no uniform: what the hand came to
        open: open, pitchDeg: PITCH_MAX * open, tiles: n, zoom: zoom, arrive: arrive,
        aspect: aspect, eye: eye, horizon: eye / Math.max(Math.tan(pitch), 1e-9),
        grid: grid, mask: clamp(st.mask, 0, 1),
      };
    }

    // ---- THE DOOR THE INSTRUMENT READS FOR ITSELF --------------------------------------------------
    // His 18:00 architecture decision, carried in the U27 brief: the instrument reads its doors at
    // runtime on the actual buffer, and the report it hands back is the runtime truth; what the
    // manifest declares is only the claim. The meshing instrument answered that first
    // (pass-inst-gears.js), the unfold reads its own panel map and the box its own two faces; this
    // is the same law read in this instrument's own unit, which is THE FLOOR — where it stands over
    // the frame, and how far the tile standing at the frame stands from its own landing.
    //
    // WHAT A DOOR ASKS OF THIS INSTRUMENT. At either door one work stands whole, at the plain cover
    // fit the `framings` block publishes. Four things carry that, and this reads all four ON THE
    // BUFFER rather than declaring them:
    //   · THE FLOOR COVERS THE FRAME. The floor has no edges and its horizon stands five frames
    //     above the frame's top, so no point of the frame is ever off it. That is a claim about a
    //     GRID — whether a bare point falls between samples or on one — and it is walked at the
    //     buffer's own sample points instead of being asserted.
    //   · THE FLOOR LIES FLAT AND THE TILE STANDING AT IT IS THE FRAME. At a door the envelope is
    //     nothing, so the lean is nothing, the lattice is square and the zoom carries the middle
    //     tile to the frame's own four corners. How far those corners stand from the frame's own —
    //     the greatest travel of any of the four, in points of the grid — is one number that catches
    //     a floor left tipped, a lattice left turned and a zoom that did not come home.
    //   · THE ROOM HAS FINISHED CHANGING HANDS. At the entry door no sheet has begun to turn and at
    //     the exit door every one has finished. That is the three shares adding to exactly one, and
    //     it is read rather than trusted: the reading walks the tiles the frame can hold and takes
    //     the worst of them.
    //   · THE JUDGES' CHANNEL IS SHUT. `mask` draws the tile map itself as colour, which is what it
    //     is for; left open at a door the frame is a false-colour map of the floor and not the
    //     photograph at all.
    //
    // AND THERE IS NOTHING HERE TO HOLD. The meshing instrument holds a leaking size whole and the
    // unfold holds a pair of panels flat, because in both a grid can show a fault a guard read in
    // the grid's own units can close. This floor has no such fault: the envelope is a sine at its
    // own zero at both ends, so the landing is exact by construction rather than by a tolerance, and
    // anything this reading finds is a real fault no widening closes. `held` is therefore always
    // nothing, and it says so rather than carrying a guard that could never fire.
    var DOOR_SLIP = 0.5;   // points of the grid: half a point, inside which a sample cannot move
    // How much of the tile map may stand in the frame at a door and it still BE the photograph: half
    // a level of 255, under anything the frame itself can carry. The charter's own door bar is 6 of
    // 255 over the canvas rect, and half a level is an eighth of that at one point.
    var DOOR_SHOW = 0.5 / 255;

    // The grid the door is read on, and which of the two it is. `drawn` says which one the sentence
    // below names, since a reader told «a 780 x 1688 frame» would look for a device that has none.
    function gridOf(st) {
      var bw = Math.round(st.bufWidth), bh = Math.round(st.bufHeight);
      if (bw >= 1 && bh >= 1) return { w: bw, h: bh, drawn: true, given: true };
      var cw = Math.round(st.cssWidth), ch = Math.round(st.cssHeight);
      if (cw >= 1 && ch >= 1) return { w: cw, h: ch, drawn: false, given: true };
      return { w: 0, h: 0, drawn: false, given: false };
    }

    // FRAG's own `onFloor`, carried here line for line so the reading walks the very plane the
    // shader draws.
    function onFloor(sx, sy, co, si, D) {
      var den = co - sy * si / D;
      if (den <= 1e-5) return null;
      var v = sy / den;
      var w = 1 + v * si / D;
      return { u: sx * w, v: v, w: w };
    }

    // Where one point of the floor lands back on the frame — the same projection forwards, so the
    // reading of the standing tile's corners is the shader's own arithmetic and not a second
    // description of it.
    function toScreen(u, v, co, si, D) {
      var w = 1 + v * si / D;
      return [u / w, v * co / w];
    }

    // THE FLOOR, READ ON THE BUFFER THE SHADER WILL SAMPLE ON. The walk takes the buffer's own
    // sample points: its four corners, where the horizon is nearest; the midpoints of its four
    // edges; and the nine points around its centre, where the middle tile's own seams cross. Every
    // one of them must land on the floor.
    function floorReadOf(v, W, H) {
      var aspect = W / Math.max(H, 1);
      var co = v.pose[1], si = v.pose[2], D = v.pose[3];
      var walked = 0, bare = 0, spare = 1e9, worstA = 0, bestA = 1, i, j;
      function walk(px, py) {
        var sx = (px / W) * 2 * aspect - aspect, sy = 1 - (py / H) * 2;
        var hit = onFloor(sx, sy, co, si, D);
        walked++;
        if (!hit) { bare++; return; }
        // how much frame this point had TO SPARE before the horizon reached it, in the same units
        // the horizon is measured in
        var head = (co * D / Math.max(si, 1e-9)) - sy;
        if (head < spare) spare = head;
        // how far this point's own tile has turned, so a door says what the room was doing rather
        // than only what the floor was
        var g = [hit.u / Math.max(v.lat[0], 1e-4), hit.v / Math.max(v.lat[0], 1e-4)];
        var ct = Math.cos(v.lat[3]), stt = Math.sin(v.lat[3]);
        var rx = g[0] * ct + g[1] * stt, ry = -g[0] * stt + g[1] * ct;
        var ix = Math.floor((rx + v.lat[1] * 0.5) / v.lat[1]);
        var iy = Math.floor((ry + v.lat[2] * 0.5) / v.lat[2]);
        var cv = iy * v.lat[2];
        var syT = cv * co / (1 + cv * si / D);
        var seat = clamp((1 - syT) * 0.5, 0, 1);
        var start = seat * SPREAD + hash21(ix + v.arr[1] + 19.7, iy + v.arr[1] - 7.3) * SCATTER;
        var a = clamp((v.arr[0] - start) / SWING, 0, 1);
        if (a > worstA) worstA = a;
        if (a < bestA) bestA = a;
      }
      for (i = 0; i < 2; i++) {
        for (j = 0; j < 2; j++) { walk(i ? W - 0.5 : 0.5, j ? H - 0.5 : 0.5); }
      }
      walk(0.5, H * 0.5); walk(W - 0.5, H * 0.5); walk(W * 0.5, 0.5); walk(W * 0.5, H - 0.5);
      for (i = -1; i <= 1; i++) {
        for (j = -1; j <= 1; j++) { walk(W * 0.5 + i, H * 0.5 + j); }
      }
      // HOW FAR THE STANDING TILE STANDS FROM ITS OWN LANDING, in points of this grid. At a door the
      // middle tile's four corners are the frame's own four corners; one frame unit is half the
      // grid's height in points, which is the reading the shader's own screen space is written in.
      var half = [v.lat[0] * v.lat[1] * 0.5, v.lat[0] * v.lat[2] * 0.5];
      var ct2 = Math.cos(v.lat[3]), st2 = Math.sin(v.lat[3]);
      var offPx = 0;
      var qs = [[-1, -1], [1, -1], [1, 1], [-1, 1]];
      for (i = 0; i < 4; i++) {
        var cx = qs[i][0] * half[0], cy = qs[i][1] * half[1];
        // the lattice's turn, taken back off, so the corner is where the shader puts it
        var wx = cx * ct2 - cy * st2, wy = cx * st2 + cy * ct2;
        var scr = toScreen(wx, wy, co, si, D);
        var dx = scr[0] - qs[i][0] * aspect, dy = scr[1] - qs[i][1];
        offPx = Math.max(offPx, Math.sqrt(dx * dx + dy * dy) * H / 2);
      }
      return { walked: walked, bare: bare, spare: spare === 1e9 ? 0 : spare, offPx: offPx,
               worstA: worstA, bestA: bestA, tiles: v.tiles, open: v.open, pitchDeg: v.pitchDeg,
               mask: v.mask };
    }

    // THE DOOR, MEASURED. Null everywhere but at a door, since away from the doors a floor standing
    // open is the picture rather than a fault. The door is named by the manifest's own `doors` block:
    // `mix` at 0 is the entry door, where the frame is the departing work whole, and `mix` at 1 the
    // exit door, where it is the arriving one.
    function doorReadOf(v, st) {
      var want = st.mix === 0 ? 1 : (st.mix === 1 ? 0 : -1);
      if (want < 0) return null;
      var g = v.grid;
      if (!g.given) return null;
      var read = floorReadOf(v, g.w, g.h);
      read.grid = g;
      read.want = want;
      return read;
    }

    // THE REFUSAL, worded the way the host's own manifest refusals read: what is wrong, in this
    // instrument's own measured numbers, on the grid it was measured on. The floor is named as the
    // cause where the floor is the cause, and the bare points it opens are its symptom.
    function doorWhyNoOf(read) {
      if (!read) return null;
      var g = read.grid, door = read.want ? "the entry" : "the exit";
      var work = read.want ? "departing" : "arriving";
      var where = " of a " + g.w + " x " + g.h + (g.drawn ? " buffer" : " frame");
      if (read.bare) {
        return door + " door leaks: the floor stands " + read.open.toFixed(6) + " open and tipped "
             + read.pitchDeg.toFixed(2) + " degrees, so " + read.bare + " of the " + read.walked
             + " points this reading walked" + where + " stand past its own horizon with no floor "
             + "under them, where " + door + " door's own law asks for the " + work
             + " work at every point";
      }
      if (read.offPx >= DOOR_SLIP) {
        return door + " door leaks: the floor stands " + read.open.toFixed(6) + " open, so the tile "
             + "standing at the frame stands " + read.offPx.toFixed(2) + " points" + where
             + " away from its own landing and the frame is a floor running away rather than the "
             + work + " work standing whole, where " + door + " door's own law asks for that work "
             + "square at every point";
      }
      if (read.want && read.worstA > 0) {
        return door + " door leaks: a sheet of the floor has already turned " + read.worstA.toFixed(4)
             + " of its own swing, so the " + work + " work is uncovered on part of the frame, where "
             + door + " door's own law asks for the " + work + " work at every point";
      }
      if (!read.want && read.bestA < 1) {
        return door + " door leaks: a sheet of the floor still stands at " + read.bestA.toFixed(4)
             + " of its own swing, so the departing work is still covering part of the frame, where "
             + door + " door's own law asks for the " + work + " work at every point";
      }
      if (read.mask >= DOOR_SHOW) {
        return door + " door leaks: the judges' own channel stands at " + read.mask.toFixed(6)
             + ", so the frame draws the tile map — " + read.tiles + " tiles across a "
             + g.w + " x " + g.h + (g.drawn ? " buffer" : " frame")
             + " — instead of the " + work + " work, where " + door
             + " door's own law asks for the " + work + " work at every point";
      }
      return null;
    }

    // THE NUMBERS OF ONE FRAME, WITH ITS DOOR READ ON THE BUFFER BEING DRAWN. Away from a door this
    // is `posed` and nothing more: the reading is taken nowhere else. At a door it walks its own
    // floor over the buffer and publishes what it read — how many points it walked, how many stood
    // off the floor, how much frame the tightest of them had to spare before the horizon, how far
    // the standing tile stands from its own landing, and how far the room has changed hands.
    function values(st) {
      var v = posed(st);
      var read = doorReadOf(v, st);
      v.doorGrid = read ? read.grid : null;
      v.floorMap = read ? { walked: read.walked, bare: read.bare, spare: read.spare,
                            offPx: read.offPx, worstA: read.worstA, bestA: read.bestA,
                            open: read.open, pitchDeg: read.pitchDeg, tiles: read.tiles } : null;
      v.doorHeld = null;
      v.doorWhyNo = doorWhyNoOf(read);
      return v;
    }

    var manifest = {
      id: "parquet", api: 1, arity: 2,
      // The floor comes up out of the flat photograph, the room changes hands tile by tile while it
      // stands open, and it lays back down with the second work standing whole.
      roles: ["disassembly", "mystery", "assembly"],
      // WHERE THIS STANDS ON THE CHARTER'S SHELF. The vocabulary table of lab/CROSSING-BRIEF.md
      // carries this module by name with its level already read — SURFACE+CELL — and that row is
      // carried here rather than re-decided:
      //   · SURFACE — the whole frame is one plane carrying one field, the mirrored lattice, and
      //     what changes as the passage runs is that field's own attitude and period.
      //   · CELL — the tiles. The floor is a partition of the frame into cells that hand their own
      //     content over one at a time, which is exactly the `tile` element the composer's
      //     `KIND_OF_MEASURE` reads out of a `grid` pivot.
      // WORLD IS NOT CLAIMED, and that is a decision worth the judge's eye rather than an oversight.
      // The module's own header reaches for shelf 8's language — a picture becoming a world the
      // viewer is inside — but the plane's attitude here is the SURFACE's own lean and no camera of
      // this instrument's own moves through a space: the eye stands still, the floor tips. That is
      // the same reading pass-inst-unfold.js makes of its own parquet, and it is what the charter's
      // own table records. Claiming the world would spend the crossing's one miracle and put this
      // instrument out of reach of every step whose role has none to spend, which would be a large
      // consequence to draw from a word the table does not use.
      levels: ["SURFACE", "CELL"],
      params: { tiles: [TILES_MIN, TILES_MAX], depth: [0, 1], lattice: [0, 180], spin: [0, SPIN_MAX] },
      // WHAT THIS INSTRUMENT SHOWS BESIDES A CROSSING (his 19:13 word, the second register). A work
      // laid out as a mirrored floor of itself is the work's own cutting device carried on: the
      // lattice repeats at the step the work was cut at and turns at the angle it was cut at, and
      // the mirror is the rule that closes the seams. What the visitor watches is how the work was
      // made, and nothing is explained to anybody.
      register: "process",
      // EVERY handle a score can drive (§4.4b). `mix` is the dial and it carries the whole passage;
      // the four below it are the module's own declared geometry; `shade` and `seed` are the module's
      // own two judge channels, resting where it rests them; `mask` is the judges' channel.
      //
      // NO `clock` HANDLE, AND THAT IS A DECISION. The module counts a second of its own up and
      // spends it on a slow camera drift, a fifteen-second breath and the floor's own turn. The
      // first two are the module's life on a page it owns and they stayed there; the third rides the
      // dial instead, so this picture moves with the hand and with nothing else, and a seeded score
      // draws one picture on every screen.
      //
      // NO HANDLE HERE KEEPS A ROLL OF ITS OWN. The module rolls its own die where a score names no
      // seed (`Math.random()` in its own `seedFrom`); here that case answers with nothing instead,
      // because an instrument that rolls its own die makes a seeded score draw two different
      // pictures.
      handles: {
        mix: { min: 0, max: 1, def: 0 },
        tiles: { min: TILES_MIN, max: TILES_MAX, def: TILES_DEF, kind: "enum", step: 2,
                 unit: "how many tiles stand across the floor",
                 reads: "the work's own frame side over structure.grid.periodPx — the count of the "
                      + "work's own measured lattice across it, which is what makes the floor the "
                      + "work's own device repeated and not a pattern laid over it; the same count "
                      + "off structure.ownDevice.stepPx where the work carries no grid period. THE "
                      + "GRID IS NAMED FIRST AND THE DEVICE SECOND, which is the other way round "
                      + "from the unfold's parquet, and the reason is measured on this collection: "
                      + "the grid period spreads the 121 works over all five counts (6 at three, 79 "
                      + "at five, 17 at seven, 6 at nine, 13 at eleven) while the device step "
                      + "saturates at the range's own top on 100 of them, so a floor laid from the "
                      + "device would be the same floor for five works in six",
                 applied: { oddOnly: true,
                            why: "the middle tile is what the dry door stands on, so the count has "
                               + "to leave one, which is the module's own oddClamp" } },
        depth: { min: 0, max: 1, def: 1,
                 unit: "how far the floor tips at the middle of the passage",
                 applied: { degreesAtWhole: PITCH_MAX, restsAt: "both doors",
                            why: "the envelope is nothing at both ends whatever this multiplies it "
                               + "by, so this handle can flatten the room without a door noticing" },
                 reads: "nothing in this tree bears on it: how deep a room a passage wants is the "
                      + "score's own reading of the step it stands at, and it rests at the module's "
                      + "own deepest" },
        lattice: { min: 0, max: 180, def: 0, unit: "degrees",
                   reads: "structure.grid.angleDeg — the direction the work's own lattice varies "
                        + "along, which is the angle the step was cut at, and which stands off "
                        + "square on 91 of this collection's 121 works; "
                        + "structure.ownDevice.angleDeg where the work carries no grid angle, "
                        + "which is nothing on 117 of the 121 and is named second for that reason" },
        spin: { min: 0, max: SPIN_MAX, def: SPIN_DEF, unit: "degrees across the whole passage",
                reads: "nothing in this tree bears on it. The module turns its floor on a clock at "
                     + "the taste-approved vista preset's own rate, and this engine hands an "
                     + "instrument no clock, so the rate is carried at this engine's own pass "
                     + "duration and rides the dial. It is the one handle here that names no "
                     + "measurement, and the port's report says so rather than leaving a reader to "
                     + "find it from a missing row" },
        shade: { min: 0, max: 1, def: 1,
                 unit: "the weight of this floor's own light and of the shadow a sheet throws",
                 applied: { atRest: 0.17, addedByDistance: 0.32, restsAt: "both doors" } },
        seed: { min: 0, max: 8, def: 0, unit: "the ordered pair's own die",
                reads: "the score's own seed, which scatters the tiles' own moments over 0.14 of "
                     + "the dial so the front turns the floor over in a ragged band rather than "
                     + "along a ruled line; the same number turns the same floor over tile for tile" },
        // THE MEASUREMENT THIS HANDLE IS READ AGAINST AT A DOOR. `readAtADoor` says what is read
        // (this instrument's own floor, walked at the buffer's own sample points), on which grid
        // (the drawing buffer the host binds, with the CSS frame where it hands none), what the
        // reading is counted in, and that there is no hold — this floor's landing is exact by
        // construction rather than by a tolerance, so a door this reading finds a fault at is
        // refused outright.
        mask: { min: 0, max: 1, def: 0,
                applied: { readAtADoor: { points: DOOR_SLIP, readOn: "the drawing buffer",
                                          reads: "landing",
                                          measures: "this instrument's own floor over the frame, "
                                                  + "walked at the buffer's own sample points, the "
                                                  + "standing tile's travel from its landing, and "
                                                  + "how far the room has changed hands",
                                          held: null } } },
      },
      neutrals: { a: 0, b: 1 },
      doors: { in: { handle: "mix", value: 0, work: "a" },
               out: { handle: "mix", value: 1, work: "b" } },
      // BOTH DOORS FRAME ALIKE, AND BOTH ARE THE PLAIN COVER FIT. At a door the zoom carries the
      // middle tile to the frame's own four corners and the crop opens to the whole picture, so what
      // stands there is the source cover-fitted and nothing else. This is the port's own repair —
      // the module draws its tile square and stretches the picture into it — and it is what makes
      // the door law keepable on a frame that is not square.
      framings: { "0": { coverCrop: 1 }, "1": { coverCrop: 1 } },
      drivers: ["progress", "cueProgress", "time", "velocity", "capability", "noise", "static",
                "curve", "spline", "map", "add", "multiply", "mix", "clamp", "hold", "segment",
                "ramp", "slew", "oscillate", "node"],
      camera: { needs: "none", authority: "stage" },
      gl: { preserveDrawingBuffer: false },
      // WHAT THIS INSTRUMENT WRITES WHERE ITS OWN MATTER IS ABSENT (§7's coverage law, and the
      // per-instrument specification in docs/design/COVERAGE.md). It is absent nowhere. Under the
      // placement rule (§8 as amended 14:05, and `coverageWhyNo`) that makes it lawful as the LOWEST
      // cue of a stack and as a whole one-cue score.
      coverage: { writes: false,
                  how: "the floor has no edges — past its own tile the mirror carries on, one "
                     + "triangle wave per axis — so the only place a point of the frame can miss it "
                     + "is beyond the horizon. The horizon of a plane tipped by this floor's own "
                     + "deepest lean of 30 degrees stands at the eye's distance times cot 30 above "
                     + "the frame's middle, and the eye is held no closer than tan 30 times the "
                     + "room the horizon is given, so it stands a quarter of a frame clear of a top "
                     + "edge at 1 whatever shape the frame is. The alpha is the constant 1; at a "
                     + "door the floor's own reading walks the buffer's sample points and refuses a "
                     + "door where any of them stands off the floor" },
      // The neutral pose is the ENTRY DOOR — `mix` at 0, the value the `doors` block above names —
      // so the frame keys the host reads off it at registration include the door's own record.
      neutralPose: { mix: 0, tiles: TILES_DEF, depth: 1, lattice: 0, spin: SPIN_DEF,
                     shade: 1, seed: 0, mask: 0,
                     reduced: false, cssWidth: 1000, cssHeight: 1000 },
      passes: [{
        program: "parquet", vert: VERT, frag: FRAG, position: "aPos",
        uniforms: [
          { name: "uA", type: "sampler2D", source: "textureA" },
          { name: "uB", type: "sampler2D", source: "textureB" },
          { name: "uFitA", type: "vec4", source: "fitA" },
          { name: "uFitB", type: "vec4", source: "fitB" },
          { name: "uRes", type: "vec2", source: "resolution" },
          { name: "uPose", type: "vec4", source: "frame:pose" },
          { name: "uLat", type: "vec4", source: "frame:lat" },
          { name: "uArr", type: "vec4", source: "frame:arr" },
          { name: "uMask", type: "float", source: "handle:mask" },
        ],
      }],
      // The instrument allocates nothing of its own: it spends the two source-texture slots the host
      // already holds and the one programme the host builds from this manifest. The module's own
      // stage, its style sheet, its hundred-and-twenty-one tiles with four surfaces each, its
      // animations and its own frame loop are what this port does without.
      resources: { lean: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                           passes: 1, bytesEstimate: 0, variant: "lean" },
                   standard: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0,
                               programs: 1, passes: 1, bytesEstimate: 0, variant: "standard" },
                   rich: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                           passes: 1, bytesEstimate: 0, variant: "rich" } },
      capabilities: ["webgl2"],
      decline: ["one work only", "a source that never decoded"],
      provenance: { labPath: "lab/effects/parquet.js", commit: "4106bd8",
                    sha256: "78249004542a5a3859a625323f0868edf5397c5ecd1695b8c4254fbd280827da" },
      readiness: "production-ready",
    };

    var live = false;
    return {
      name: "parquet",
      manifest: manifest,
      values: values,
      fit: fit,
      feel: feel,
      prepare: function (o) {
        if (!o.sources) return { take: false, why: "the mirror-floor instrument needs both works" };
        if (!o.cue) return { take: false, why: "no cue names it" };
        return { take: true };
      },
      start: function () { live = true; },
      // The pose the shader draws. The module's stage, its frame loop, its pointer and its own slow
      // drift are gone, so every number here comes from a handle a score drives or from the frame
      // the host is about to bind.
      //
      // A DOOR THIS INSTRUMENT CANNOT KEEP WHOLE IS REFUSED RATHER THAN DRAWN. The door law is the
      // instrument's own claim, so the instrument is what answers for it: at either door it walks
      // its own floor over the buffer the host is about to bind and, where a point of that grid
      // stands off the floor, where the standing tile stands off its own landing further than a
      // sample can move, where a sheet has not finished turning, or where the judges' channel is
      // left open, it hands the host the reason with the measured numbers in it instead of drawing a
      // door that is not the photograph. The host recovers the transaction on that reason and the
      // walk's own glide carries the visitor, which is the product's own behaviour with no renderer.
      frame: function (st) {
        if (!live) return;
        var h = st.handles;
        var pose = {
          mix: h.mix, tiles: h.tiles, depth: h.depth, lattice: h.lattice, spin: h.spin,
          shade: h.shade, seed: h.seed, mask: h.mask, reduced: st.reduced,
          cssWidth: st.viewport.w, cssHeight: st.viewport.h,
          // THE GRID THE SHADER WILL SAMPLE ON, carried into the pose so the geometry is built for
          // the frame the host is about to bind as `uRes` and the door is read on it rather than on
          // the CSS frame around it. The host settles it from the device ratio and its own
          // resolution step, so it moves while a pass plays and each door is read on the grid
          // standing at that door's own instant.
          bufWidth: st.viewport.bufferW, bufHeight: st.viewport.bufferH,
        };
        // AT A DOOR THE INSTRUMENT SAYS WHAT IT APPLIED, and says it before it refuses. The reading
        // is taken on the buffer this frame is drawn on, so it is the run-time truth his 18:00
        // decision asks for. `request` is the travel a landing asks of the standing tile — none —
        // and `applied` is the travel this grid actually shows.
        if (h.mix === 0 || h.mix === 1) {
          var v = values(pose);
          if (st.reportApplied) {
            st.reportApplied({
              door: h.mix === 0 ? "in" : "out",
              buffer: [pose.bufWidth, pose.bufHeight],
              reads: "landing", request: 0,
              applied: v.floorMap ? v.floorMap.offPx : null,
              moved: v.floorMap ? v.floorMap.offPx : null,
              unit: "points of the drawing buffer",
              // What the floor itself was doing over the frame at this door: how far it stood open,
              // how many of the walked points stood off it, and how far the room had changed hands.
              open: v.floorMap ? v.floorMap.open : null,
              bare: v.floorMap ? v.floorMap.bare : null,
              spare: v.floorMap ? v.floorMap.spare : null,
              turned: v.floorMap ? [v.floorMap.bestA, v.floorMap.worstA] : null,
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
    instrument: parquetInstrument(),
  });
})();
