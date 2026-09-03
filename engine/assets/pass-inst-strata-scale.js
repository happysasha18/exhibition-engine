/*!pass-inst-strata-scale.js*/
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
// OWNERSHIP. This instrument was carried over from lab/effects/strata-scale.js. The owner's word of
// 2026-08-18 23:21: every instrument the lab holds but the shards belongs in the arsenal. The
// artistic instruments and their manifests belong to tlvphotos, which builds these files from its
// own sources; the engine's copies are what ships until that handover lands. The contract this file
// answers to is §7 and §8 of docs/design/PASS-API-V1.md, and the record that names it is the site's
// own `pass` block.
(function () {
  var join = window.__@@NS@@PassInstrument;
  if (typeof join !== "function") return;

  // THIS FILE'S OWN VERSION, and the one home of that fact. The build reads this literal out of the
  // source and writes it into the site's record beside the digest, so the version a file declares
  // and the version a host was told to load cannot drift apart without the build noticing.
  var INSTRUMENT_VERSION = "1.0.0";

  // ================================================================================================
  // THE PARTING-BY-SCALE INSTRUMENT (§8) — lab/effects/strata-scale.js carried across
  // ================================================================================================
  // WHAT THE VISITOR SEES. The departing photograph parts into two strata that read at two different
  // scales of the SAME picture: the MASSES, the work read down to the scale at which only its large
  // shapes survive, and the DETAIL, the sharp picture standing over them. On the way out the detail
  // lifts off first and the masses follow, each stratum leaving SIDEWAYS toward the side of its own
  // measured centre of gravity; the arriving work's two strata come in the opposite way at the same
  // instant, its masses growing first with its detail growing into it, until the two close on each
  // other and the second work stands whole. Nothing is ever faded: what leaves the eye leaves the
  // frame, and where neither work's matter has reached yet this instrument carries nothing and
  // whatever plays beneath it is seen.
  //
  // ONE MODULE, TWO LAYERS, ONE PASS. The lab module holds ONE work (`needs: 1`) and its dial runs
  // from the work standing whole to an EMPTY frame — the module's own header names the road out
  // exactly as strata-light's does: "the same dial run backwards, 1 → 0, slides the strata together
  // into the whole work — which is how a layer ARRIVES without a fade" (strata-scale.js:7-9). So this
  // instrument is the module read TWICE in one pass, the same construction pass-inst-strata-light.js
  // already proved for its own sibling: the departing work's own dial runs 0 → 1 as `mix` does, the
  // arriving work's runs 1 → 0, and both are put through the module's own response curve. At `mix` 0
  // the departing work stands whole and the arriving work is wholly outside the frame; at `mix` 1 the
  // opposite. Both doors are exact by construction, and the paragraph THE DOOR THE INSTRUMENT READS
  // FOR ITSELF below says exactly why.
  //
  // ------------------------------------------------------------------------------------------------
  // WHAT CAME OVER
  // ------------------------------------------------------------------------------------------------
  //   · THE CUT. A work parts at the MEDIAN of its own relief field — the picture read at MASK_CELLS
  //     = 128 cells against the same picture read at MASS_CELLS = 16 cells and drawn back up, the
  //     absolute difference between the two (strata-scale.js:42, :47, :87-101, :138-141). Ported to
  //     python as `edge`, the number this port's own centres below are cut at
  //     (lab/analyze/recipes.py's `strata_scale_measure()`).
  //   · THE TWO STRATA'S OWN CENTRES OF GRAVITY (strata-scale.js:279-287): the mass cells' own mean
  //     position and the detail cells' own, along the frame's long axis, each deciding which side a
  //     piece of that stratum leaves toward — "the side is the stratum's own" (strata-scale.js:11-12).
  //     Ported to python beside `edge`, in the same call, for the reason THE CENTRE OF GRAVITY below
  //     names.
  //   · THE HANDOVER (strata-scale.js:49-51, :450-506): the dial's own first share carries the detail
  //     off, the rest carries the masses, DETAIL_SHARE = 0.4 the module's own hard number and
  //     HANDOVER_REACH = 0.25 the module's own named departure from it, both carried digit for digit,
  //     including the module's own response curve for the handle that walks between them
  //     (strata-scale.js:468-495, FEEL_H_U0/K1/K2).
  //   · THE RESPONSE CURVE, digit for digit: the two-piece exponential hinged at the measured median
  //     of the felt change, FEEL_C 0.47, FEEL_K1 1.2, FEEL_K2 2.6 (strata-scale.js:421-441).
  //   · BOTH ACCOMPANYING VOICES, digit for digit: `a·sin(2π(u/p + phase))·4u(1−u)`, the colour voice
  //     breathing a piece's saturation against its own grey twin and the light voice writing the
  //     standing matter lighter and darker, each held to nothing at both doors by the window
  //     (strata-scale.js:355-384).
  //   · NO FADE ANYWHERE. A point either carries a work's matter or it does not; the alpha this
  //     shader writes is 1 or 0 and never anything between.
  //
  // ------------------------------------------------------------------------------------------------
  // THE CENTRE OF GRAVITY IS A PER-WORK READING, NOT A CROSSING — and this is the one place an
  // earlier pass over this file stopped, wrongly, calling the whole port unreachable for it
  // ------------------------------------------------------------------------------------------------
  // `edge` is a reduction over ONE photograph's own relief field and so is each stratum's own centre
  // of gravity — a mean position taken over that same one photograph's own cells, nothing about a
  // second work anywhere in the arithmetic. A shader handed one frame at the instant of a visit
  // cannot run either reduction; a python build measuring one file, once, ahead of any visit, can —
  // exactly the road strata-light's own `luminance.level` already opened for this family
  // (lab/analyze/recipes.py, `luma_level`/`colour_stats`, threaded through build-elements-v1.py and
  // build-workrecords-v1.py into `luminance.level`). His law of 2026-08-18 15:13 forbids a crossing
  // computed ahead of the visit or the same number standing for every pair; a per-work fact obeys
  // both, because it is measured once per PHOTOGRAPH and travels inside that work's own record, and
  // two different works hand two different numbers to two different pairs. `edge`,
  // `massCentreX` and `detailCentreX` are carried into `texture.reliefEdge`/`reliefCentreMassX`/
  // `reliefCentreDetailX` by lab/build-elements-v1.py and lab/build-workrecords-v1.py, the same two
  // files that already carry `luminance.level`, and `pass-composer.js`'s own "strata-scale" branch of
  // `fillPlan` drives this instrument's `massCentreXA`/`massCentreXB`/`detailCentreXA`/
  // `detailCentreXB` handles from them, one work at a time.
  //
  // ------------------------------------------------------------------------------------------------
  // WHAT DID NOT COME OVER, NAMED RATHER THAN SMOOTHED OVER
  // ------------------------------------------------------------------------------------------------
  // THE CONNECTED AREAS AND THEIR OWN PER-PIECE DIRECTION. The module cuts the relief mask into its
  // CONNECTED AREAS (strata-scale.js:111-134) and, for EVERY area regardless of which class it
  // belongs to, cuts BOTH a sharp piece and a masses piece of that same shape (strata-scale.js:257-
  // 306) — so the detail layer and the masses layer each, on their own, tile the WHOLE frame, and a
  // piece's own direction is decided by whether ITS OWN midpoint stands to one side or the other of
  // its stratum's own centre of gravity (strata-scale.js:298-302). A fragment shader is handed one
  // output point and answers it by looking BACK along a displacement it can name from the point
  // alone; a per-area direction is a property of the whole area a point happens to fall in, and
  // finding that area means labelling connected components over a framebuffer, which needs repeated
  // passes and a reduction per label this file has no way to take — the identical wall
  // pass-inst-strata-light.js already met and named for its own per-area travel distance.
  //
  // WHAT STANDS INSTEAD, and what it costs. Since the detail layer (and, separately, the masses
  // layer) tiles the WHOLE frame regardless of the relief mask's own areas, the port drops the mask's
  // own irregular tessellation and asks, per POINT rather than per AREA, which side of the stratum's
  // own measured centre that point's own position falls on: everything to one side travels toward
  // that edge, everything to the other travels toward the other. This is the same simplification
  // family strata-light's own port already stands on — MANY puzzle pieces, each clearing the frame at
  // its own pace, collapsed to a SMALL NUMBER of rigid bodies clearing it together — read here at the
  // finer grain a continuous split affords rather than at strata-light's two whole strata. What is
  // lost: a piece that in the module stands near the centre and travels only a little now travels the
  // same full course as one that starts at the frame's own edge, and a piece whose OWN midpoint
  // happens to sit on the far side of the centre from most of its neighbours (a puzzle piece is not a
  // point) now travels with the point-wise reading rather than its own whole shape's. `MAX_AREAS = 48`
  // and the module's own connected-components walk therefore have no counterpart here at all — this
  // port never needs to label an area to begin with.
  //
  // BECAUSE OF THAT SAME COLLAPSE, THE RELIEF MASK ITSELF NEVER HAS TO BE READ AT RUNTIME. The
  // module's own per-cell relief classification (strata-scale.js:257-260) exists only to build the
  // connected areas and to weigh the two centres of gravity (strata-scale.js:281-287) — nothing in
  // `cut()` uses a cell's own class to decide which RENDERING (sharp or masses) shows at a point, since
  // every area gets both cuts regardless of its own class. Once the per-area tessellation is dropped,
  // the mask has nothing left to decide in this port, and `edge` itself never reaches the shader —
  // only the two centres it was used to weigh do. This is a genuine simplification and not a corner
  // cut: strata-light's own port DOES read a mask at runtime because its classification decides which
  // stratum a point belongs to at all; this module's classification never did that.
  //
  // THE MASSES ARE READ AT A CELL'S OWN CENTRE, BILINEARLY BLENDED. The module builds its masses
  // rendering by drawing the file down to MASS_CELLS on the long side and back up with the canvas's
  // own smoothing (strata-scale.js:204-211) — a true box mean at the coarse scale, smoothly
  // interpolated on the way back up. A fragment shader cannot average a cell in one fetch, so this
  // port reads each of the four grid points nearest a texture coordinate at ITS OWN centre — a single
  // fetch standing in for the box mean at that cell, exactly the cost strata-light's own port already
  // names for reading a mask cell at its centre (that port's own "THE CELL IS READ AT ITS CENTRE") —
  // and blends the four bilinearly, which is the smoothed upsample the module performs. What this
  // costs: a mass cell whose centre is untypical of the whole cell (a hard edge crossing it) reads a
  // little sharper than the module's true box mean would.
  function strataScaleInstrument() {
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
      // how far each work's own DETAIL layer has travelled, in frame widths, sideways from its own
      // measured centre — the module's own dial split by the handover (strata-scale.js:393-395)
      "uniform vec2 uDetailU;",
      // how far each work's own MASSES layer has travelled, the same way
      "uniform vec2 uMassU;",
      // each work's own measured centre of gravity of its DETAIL cells, a fraction of the frame's
      // own width — texture.reliefCentreDetailX
      "uniform vec2 uDetailCentre;",
      // each work's own measured centre of gravity of its MASS cells, the same way —
      // texture.reliefCentreMassX
      "uniform vec2 uMassCentre;",
      // how much palette each work's drawn matter holds now — the colour voice
      "uniform vec2 uSat;",
      // and how much lighter or darker the light voice writes it, signed
      "uniform vec2 uLight;",
      // the judges' handle: the two works' own coverage as colour
      "uniform float uMask;",
      "uniform float uPresence;",  // the entry-door contract's reserved dry
      // THE MASS GRID'S OWN CELL COUNT, pinned rather than published — this port's own choice, unlike
      // strata-light's own `cellsA`/`cellsB` handle, and named as a choice: see this file's own
      // comment beside the JS `MASS_CELLS` constant below for why.
      "const float MASS_CELLS = 16.0;",
      "vec2 into(vec2 p, vec4 f){",
      "  return clamp((p - 0.5) * f.xy + 0.5 + f.zw, 0.0008, 0.9992);",
      "}",
      // the module's own luminance, the same three weights strata-light's own port reads
      "float lumaOf(vec3 c){ return dot(c, vec3(0.2126, 0.7152, 0.0722)); }",
      // THE MASS GRID OF ONE FILE — MASS_CELLS on its long side and the short side in proportion,
      // exactly the module's own `gridSize(img, MASS_CELLS)` (strata-scale.js:67-71) and the same
      // construction strata-light's own port already reads its own mask grid with (that port's own
      // `gridOf`). The file's own aspect is recovered from the seating the host applied, the way
      // every other instrument in this arsenal reads it: a cover fit carries the frame's aspect times
      // the ratio of its two scales.
      "vec2 gridOf(float cells, vec4 f, float aspect){",
      "  float ia = aspect * f.y / max(f.x, 1e-4);",
      "  float other = max(1.0, floor((ia >= 1.0 ? cells / ia : cells * ia) + 0.5));",
      "  return ia >= 1.0 ? vec2(cells, other) : vec2(other, cells);",
      "}",
      // THE MASSES SCALE, bilinearly read off a virtual grid over the file at MASS_CELLS on its own
      // long side — see the header's own "THE MASSES ARE READ AT A CELL'S OWN CENTRE" for why this is
      // a fetch of four rather than the module's own true box mean, and what that costs.
      "vec3 massesAt(sampler2D tex, vec4 f, vec2 mg, vec2 t){",
      "  vec2 gp = t * mg - 0.5;",
      "  vec2 gi = floor(gp);",
      "  vec2 gf = clamp(gp - gi, 0.0, 1.0);",
      "  vec3 c00 = texture2D(tex, into((gi + vec2(0.5, 0.5)) / mg, f)).rgb;",
      "  vec3 c10 = texture2D(tex, into((gi + vec2(1.5, 0.5)) / mg, f)).rgb;",
      "  vec3 c01 = texture2D(tex, into((gi + vec2(0.5, 1.5)) / mg, f)).rgb;",
      "  vec3 c11 = texture2D(tex, into((gi + vec2(1.5, 1.5)) / mg, f)).rgb;",
      "  return mix(mix(c00, c10, gf.x), mix(c01, c11, gf.x), gf.y);",
      "}",
      // ONE STRATUM'S OWN MATTER AT THIS POINT. `centre` is that stratum's own measured centre of
      // gravity — a fraction of the frame's own width — and content that started to the LEFT of it
      // has travelled `u` frame widths further LEFT, while content that started AT OR RIGHT of it has
      // travelled `u` further RIGHT (strata-scale.js:296-302, this port's own uniform-travel reading
      // of it, the header's own "WHAT STANDS INSTEAD"). Read backwards from a destination point `uv`,
      // exactly one of the two candidate sources can be valid: `sl = uv.x + u` is the source of
      // content that moved LEFT to land here, valid where `sl` itself was left-half (`sl <= centre`);
      // `sr = uv.x - u` is the source of content that moved RIGHT, valid where `sr` was right-half
      // (`sr >= centre`). For `u > 0` the two conditions can never both hold — there is a gap of width
      // `2u` centred on `centre` where NEITHER candidate is valid, which is the stratum's own matter
      // having cleared that band of the frame; the OTHER stratum, or the arriving work, or nothing at
      // all shows there instead. At `u = 0` the two candidates agree (`sl = sr = uv.x`) and the
      // stratum tiles the frame whole, matching the module's own dial-at-rest branch.
      "float stratumAt(vec4 f, vec2 uv, float centre, float u, out vec2 t){",
      "  float sl = uv.x + u;",
      "  if (sl <= centre) { t = into(vec2(sl, uv.y), f); return 1.0; }",
      "  float sr = uv.x - u;",
      "  if (sr >= centre) { t = into(vec2(sr, uv.y), f); return 1.0; }",
      "  return 0.0;",
      "}",
      // ONE WORK'S OWN MATTER AT THIS POINT — its masses stratum and its detail stratum, each read by
      // `stratumAt` off its own centre and its own travel, DETAIL STANDING OVER MASSES wherever both
      // still cover the point: "on the way out the detail is taken off first" (strata-scale.js:6), so
      // the sharp layer is what still hides the blurred one until it, too, has cleared — the module's
      // own draw order, masses before detail in every frame it writes (strata-scale.js:398-417).
      "vec4 workMatterAt(sampler2D tex, vec4 f, vec2 mg, vec2 uv, float massCentre, float detailCentre,",
      "                   float uMass, float uDetail, float sat, float lit){",
      "  vec2 td;",
      "  if (stratumAt(f, uv, detailCentre, uDetail, td) > 0.5) {",
      "    vec4 got = vec4(texture2D(tex, td).rgb, 1.0);",
      "    got.rgb = mix(vec3(lumaOf(got.rgb)), got.rgb, sat);",
      "    got.rgb = mix(got.rgb, vec3(step(0.0, lit)), abs(lit));",
      "    return got;",
      "  }",
      "  vec2 tm;",
      "  if (stratumAt(f, uv, massCentre, uMass, tm) > 0.5) {",
      "    vec4 got = vec4(massesAt(tex, f, mg, tm), 1.0);",
      "    got.rgb = mix(vec3(lumaOf(got.rgb)), got.rgb, sat);",
      "    got.rgb = mix(got.rgb, vec3(step(0.0, lit)), abs(lit));",
      "    return got;",
      "  }",
      "  return vec4(0.0);",
      "}",
      "void main(){",
      "  vec2 uv = vUv;",
      "  float aspect = uRes.x / max(uRes.y, 1.0);",
      "  vec2 mgA = gridOf(MASS_CELLS, uFitA, aspect);",
      "  vec2 mgB = gridOf(MASS_CELLS, uFitB, aspect);",
      "  vec4 a = workMatterAt(uA, uFitA, mgA, uv, uMassCentre.x, uDetailCentre.x,",
      "                        uMassU.x, uDetailU.x, uSat.x, uLight.x);",
      "  vec4 b = workMatterAt(uB, uFitB, mgB, uv, uMassCentre.y, uDetailCentre.y,",
      "                        uMassU.y, uDetailU.y, uSat.y, uLight.y);",
      // THE ARRIVING WORK'S MATTER STANDS OVER THE DEPARTING WORK'S, exactly as strata-light's own
      // port reads it: read the other way round an arriving stratum would slide UNDER what is still
      // standing and only appear as the departing work cleared it, which is an arrival by uncovering
      // — the fade this module exists to avoid, read backwards.
      "  vec3 col = mix(a.rgb, b.rgb, b.a);",
      // THE COVERAGE LAW (§7). This instrument's own matter is the two works' own two strata apiece,
      // wherever either has carried matter to a point; where none has, it carries nothing,
      // contributes nothing and hides nothing, and the cue beneath is seen. At either door one work's
      // own two strata tile the frame exactly (both `u` are exactly 0 there, see the door proof
      // below), so the alpha is 1 at every point and the door is one whole work.
      "  float cov = max(a.a, b.a);",
      // the judges' own frame: the two works' coverage as colour
      "  col = mix(col, vec3(a.a, b.a, 0.0), uMask);",
      "  gl_FragColor = vec4(col, mix(cov, 1.0, uMask) * uPresence);",
      "}",
    ].join("\n");
    // THE MASS GRID'S OWN CELL COUNT — pinned as the shader's own `const float MASS_CELLS = 16.0`
    // above rather than read off a uniform: this port's own choice, unlike strata-light's own
    // `cellsA`/`cellsB` handle, which publishes ITS grid because that port's own choice was to make
    // it one. `MASK_CELLS = 128` never reaches this shader at all: see the header's own "BECAUSE OF
    // THAT SAME COLLAPSE, THE RELIEF MASK ITSELF NEVER HAS TO BE READ AT RUNTIME" for why.
    var MASS_CELLS = 16;   // lab/effects/strata-scale.js:47 (MASS_CELLS)

    function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
    function clamp01(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }

    // TRAVEL — how far a stratum's own point-wise split moves, in frame widths. Not a free number and
    // not a taste: one full frame WIDTH is exactly the distance that carries a point on either side of
    // its stratum's own centre wholly out of the frame regardless of where in [0, 1] that centre
    // stands (a point starting at the frame's far edge from its own centre clears in less; TRAVEL = 1
    // is what makes the far door exact for every centre, including one standing at either edge of the
    // frame) — the same role strata-light's own `TRAVEL = 1.0` plays for its top-and-bottom departure,
    // read here sideways.
    var TRAVEL = 1.0;

    // THE MODULE'S OWN CEILING ON THE LIGHT VOICE (strata-scale.js:377, the same line strata-light's
    // own module carries): the writing never passes nine tenths, so the matter under it is never
    // wholly lost to white or to black.
    var LIGHT_CEILING = 0.9;

    // THE RESPONSE CURVE (SPEC.md Requirement 40, criterion 10, his word of 2026-08-08 17:57), carried digit for digit
    // out of the module (strata-scale.js:421-441). Equal movements of the hand produce equal felt
    // change; the family is a two-piece exponential hinged at the MEASURED median of the felt change,
    // c = 0.47, with the plain logarithm on each side fixed by its own ends, k1 = 1.2 below the knee
    // and k2 = 2.6 above. The port re-derives nothing.
    // DERIVED — the module's own measured response curve, carried digit for digit, and the block
    // above names the module, the lines and the measurement it came off (S-71, 2026-09-03).
    var FEEL_C = 0.47, FEEL_K1 = 1.2, FEEL_K2 = 2.6;
    function feelLog(x, k) {
      return Math.abs(k) < 1e-6 ? x : (Math.exp(k * x) - 1) / (Math.exp(k) - 1);
    }
    function feelOf(u) {
      return u <= 0.5 ? FEEL_C * feelLog(2 * u, FEEL_K1)
                      : FEEL_C + (1 - FEEL_C) * feelLog(2 * u - 1, FEEL_K2);
    }

    // THE HANDOVER (strata-scale.js:450-506): «ONE MOTION THIS MODULE KEPT TO ITSELF, now a handle a
    // score can drive» (his word of 2026-08-12 23:09, carried verbatim in the module's own comment).
    // DETAIL_SHARE = 0.4 is the module's own hard number, the share of the dial's own travel the
    // detail takes before the masses start to go; HANDOVER_REACH = 0.25 is the module's own named
    // departure from it, «my own number, named as mine» (strata-scale.js:458-459). The response curve
    // that walks the handle, FEEL_H_U0/K1/K2, is carried digit for digit (strata-scale.js:490).
    //
    // THIS PORT'S OWN NEUTRAL. `handoverPin = null` in the module (no score names a value) rests
    // `detailShare()` at DETAIL_SHARE exactly; `handoverPin = 0.5` gives the identical number, since
    // `DETAIL_SHARE + (0.5 - 0.5) * 2 * HANDOVER_REACH = DETAIL_SHARE`. The module's own response
    // curve reaches exactly 0.5 at its own hinge, `feelHandover(FEEL_H_U0) = 0.5 * feelLog(1, K1) =
    // 0.5` in exact arithmetic — so a handle resting at FEEL_H_U0 reproduces the module's own rest
    // exactly, and that is where this manifest's `handover` handle defaults.
    var DETAIL_SHARE = 0.4;      // strata-scale.js:51
    var HANDOVER_REACH = 0.25;   // strata-scale.js:465, "my own number, named as mine"
    var FEEL_H_U0 = 0.744, FEEL_H_K1 = -0.40, FEEL_H_K2 = -0.86;   // strata-scale.js:490
    function feelHandoverOf(u) {
      return u <= FEEL_H_U0 ? 0.5 * feelLog(u / FEEL_H_U0, FEEL_H_K1)
                            : 0.5 + 0.5 * feelLog((u - FEEL_H_U0) / (1 - FEEL_H_U0), FEEL_H_K2);
    }
    function detailShareOf(handover) {
      var pin = feelHandoverOf(clamp01(typeof handover === "number" ? handover : FEEL_H_U0));
      return DETAIL_SHARE + (pin - 0.5) * 2 * HANDOVER_REACH;
    }

    // A VOICE AT THIS DIAL, carried digit for digit (strata-scale.js:360-369, the same line
    // strata-light's own port already reads). One breath of a named period and a named phase, held to
    // nothing at BOTH doors by the window 4u(1 − u).
    function voiceAt(period, phase, amp, u) {
      var a = +amp, p = +period;
      if (!(a > 0) || !(p > 0)) return 0;
      return a * Math.sin(2 * Math.PI * (u / p + (+phase || 0))) * 4 * u * (1 - u);
    }

    // How much palette a work's matter holds at this dial: full, but for the colour voice's own
    // breath — clamped at 1, therefore one-sided (strata-scale.js:366-370).
    function satAt(v) { return clamp(1 + v, 0, 1); }

    // Cover-fit a work into the frame, with NO crop of its own — the module's own `sc =
    // Math.max(W/iw, H/ih)` (strata-scale.js build()).
    function fit(iw, ih, w, h) {
      var fa = w / Math.max(h, 1);
      var ia = iw / Math.max(ih, 1);
      var sx, sy;
      if (ia > fa) { sx = fa / ia; sy = 1; } else { sx = 1; sy = ia / fa; }
      return [sx, sy, 0, 0];
    }

    // ---- THE DOOR THIS INSTRUMENT READS FOR ITSELF ------------------------------------------------
    // His 18:00 architecture decision, carried in the U27 brief: the instrument reads its own doors
    // at run time and the report it hands back is the run-time truth. This instrument's own doors
    // hold by ALGEBRA rather than by a grid, exactly the way pass-inst-studio.js's own do: `feelOf(0)
    // = 0` and `feelOf(1) = 1` in exact arithmetic (the two-piece exponential's own ends), so at `mix`
    // 0 the departing work's own `uDetail`/`uMass` are both exactly `clamp(0 / share, 0, 1) = 0` and
    // `clamp((0 - share) / (1 - share), 0, 1) = 0` (the numerator is negative, the clamp floors it),
    // and the arriving work's own are both exactly `clamp(1 / share, 0, 1) = 1` and `clamp((1 -
    // share) / (1 - share), 0, 1) = 1` — whatever `share` the handover names, since `0 < share < 1`
    // always. `stratumAt` above reads `u = 0` as the whole stratum tiling the frame and `u = 1` as it
    // wholly cleared, on ANY centre, so neither reading has a width a grid could close or open. What
    // CAN still break a door is the two accompanying voices, written over whatever stands — exactly
    // the one thing strata-light's own door reading is held against — so this is what is read, in its
    // own numbers, on the buffer about to be drawn: the standing work's own two voices.
    function doorReadOf(v, st) {
      var door = st.mix === 0 ? "in" : (st.mix === 1 ? "out" : null);
      if (door === null) return null;
      var i = door === "in" ? 0 : 1;
      return { door: door, standing: i, detailU: v.detailU[i], massU: v.massU[i],
               colourVoice: v.colourVoice[i], lightVoice: v.lightVoice[i] };
    }

    function doorWhyNoOf(read) {
      if (!read) return null;
      var i = read.standing;
      var geom = Math.abs(read.detailU) + Math.abs(read.massU);
      var c = Math.abs(read.colourVoice), l = Math.abs(read.lightVoice);
      if (!(geom > 0) && !(c > 0) && !(l > 0)) return null;
      // Unreachable on any pose this file as written can produce — `feelOf` returns exactly 0 or 1
      // at the dial's own two ends and nowhere else the door reading is taken — and it is said here
      // rather than removed, the same way studio's own door note is: a claim proved, not a range
      // guarded.
      return (read.door === "in" ? "the entry" : "the exit") + " door leaks: the "
           + (read.door === "in" ? "departing" : "arriving") + " work's own detail travel reads "
           + read.detailU + " and its masses travel " + read.massU + " where its own construction "
           + "asks for both exactly " + (i === 0 ? "0" : "1") + ", and its colour voice reads "
           + c.toFixed(6) + " and its light voice " + l.toFixed(6) + " where its own window holds "
           + "both to nothing there";
    }

    // THE NUMBERS OF ONE FRAME. Everything the shader gets beyond the seating of the two works is a
    // pure function of the pose. The departing work's dial is the hand through the module's own
    // response curve and the arriving work's is the hand read backwards through the same curve, so
    // one pass carries the module twice and neither reading is a second curve.
    //
    // NOTHING HERE READS THE SECOND THE HOST HANDS DOWN, and that is the module's own law rather than
    // an omission: every position in it is a pure function of the dial (strata-scale.js:508-510). The
    // `clock` handle is published because the module accepts one and a score owns the clock
    // everywhere; a run of this instrument repeats to the pixel because there is nothing in it for a
    // clock to move.
    function values(st) {
      var hand = clamp01(typeof st.mix === "number" ? st.mix : 0);
      var dA = feelOf(hand), dB = feelOf(1 - hand);
      var share = detailShareOf(st.handover);
      var v = {
        dial: [dA, dB],
        detailU: [clamp01(dA / share) * TRAVEL, clamp01(dB / share) * TRAVEL],
        massU: [clamp01((dA - share) / (1 - share)) * TRAVEL,
                clamp01((dB - share) / (1 - share)) * TRAVEL],
        detailCentre: [clamp01(+st.detailCentreXA), clamp01(+st.detailCentreXB)],
        massCentre: [clamp01(+st.massCentreXA), clamp01(+st.massCentreXB)],
        share: share,
      };
      var cvA = voiceAt(st.colourPeriodA, st.colourPhaseA, st.colourAmpA, dA);
      var cvB = voiceAt(st.colourPeriodB, st.colourPhaseB, st.colourAmpB, dB);
      var lvA = voiceAt(st.lightPeriodA, st.lightPhaseA, st.lightAmpA, dA);
      var lvB = voiceAt(st.lightPeriodB, st.lightPhaseB, st.lightAmpB, dB);
      v.sat = [satAt(cvA), satAt(cvB)];
      v.light = [clamp(lvA, -LIGHT_CEILING, LIGHT_CEILING), clamp(lvB, -LIGHT_CEILING, LIGHT_CEILING)];
      // read on the diagnostic surface, bound to no uniform: the two voices on their own, which is
      // the only part of the picture a judge can weigh against the voice the score declared — the
      // same two fields strata-light's own `values()` publishes
      v.colourVoice = [cvA, cvB]; v.lightVoice = [lvA, lvB]; v.hand = hand;
      var read = doorReadOf(v, st);
      v.doorStanding = read ? read.standing : null;
      v.doorWhyNo = doorWhyNoOf(read);
      return v;
    }

    var manifest = {
      id: "strata-scale", api: 1, arity: 2,
      // The departing work's detail lifts off first and its masses follow, the middle holds a frame
      // neither work has closed, and the arriving work's masses gather first with its detail growing
      // into them.
      roles: ["disassembly", "mystery", "assembly"],
      // THE MODULE'S OWN PUBLISHED LEVEL, lab/data/module-contract.json's own `strata-scale.level` row
      // — "CELL+TEXTURE" — read here whole: CELL because the departure still cuts the frame into
      // pieces that travel as rigid bodies (this port's own point-wise collapse of that same cut, the
      // header's own "WHAT DID NOT COME OVER"), and TEXTURE because the two strata are not a spatial
      // partition of ONE rendering the way strata-light's bright and dark are — they are two SEPARATE
      // renderings of the SAME work at two different scales of its own material, shown one over the
      // other. LIGHT-COLOUR joins the two the same way it joined strata-light's own row (that port's
      // own note beside its `levels` field): the module carries no reading of its own for either voice
      // and this composer now drives both, so a cue that owns that level has to be able to say so.
      levels: ["CELL", "TEXTURE", "LIGHT-COLOUR"],
      // WHAT THIS INSTRUMENT CUTS ON. `pass-composer.js`'s own PIVOT_SHAPES names the pivot this
      // instrument completes: "THE TONAL ZONES AND THE DETAIL SCALES... the arriving work's blurred
      // mass growing first with its detail growing into it" (that pivot's own words) cuts on both
      // `band` and `scale`, elementKinds `["band", "scale"]` — a decomposition worded for exactly
      // this module before this module had a port to answer it. `band` because the cut is a threshold
      // over a measured field into two classes, the same construction strata-light's own `cuts:
      // ["band"]` names; `scale` because what the threshold is taken OVER is the picture's own detail
      // scale, the same word beat.js's own cut list gives its rhythm difference
      // ("texture to scale in its KIND_OF_MEASURE", that file's own comment).
      cuts: ["band", "scale"],
      // WHERE THIS INSTRUMENT HAS A SEAM (§8's `seams` block, pass-layer.js). None is declared, for
      // the same reason strata-light's own sibling gives none: "NO FADE ANYWHERE. A point either
      // carries a work's matter or it does not; the alpha this shader writes is 1 or 0 and never
      // anything between." `stratumAt` above reads the split as a plain `<=`/`>=` against each
      // stratum's own measured centre — a point is on one side or the other, with nothing written to
      // blend the two together where they meet. The one place two candidate sources could both fail is
      // "a gap of width `2u` centred on `centre` where NEITHER candidate is valid", and the file is
      // explicit that this gap is "the stratum's own matter having cleared that band of the frame" —
      // this cut's own coverage absence, which the other stratum, the other work or nothing at all
      // shows through, not a line this cut still needs softening at.
      seams: [],
      // The module declares NO slider-facing params at all (`params: []`, lab/effects/strata-
      // scale.js:559), the same empty list strata-light's own module carries: no page grows a control
      // for any of this and every handle below is a hidden one a score drives.
      params: {},
      // EVERY handle a score can drive (§4.4b). `mix` is the dial and `clock` is the second the host
      // hands down; `handover` is the module's own single shared handle (strata-scale.js:450-506, see
      // "THE HANDOVER" above) — ONE number for the whole pair, since the module's own detail/masses
      // split is a property of the departure itself and not of either work; the rest are published
      // PER WORK because this instrument plays the module twice.
      //
      //   · `massCentreXA`/`massCentreXB`/`detailCentreXA`/`detailCentreXB` — EACH STRATUM'S OWN
      //     MEASURED CENTRE OF GRAVITY, a fraction of the frame's own width. The module solves these
      //     inside `cut()` at build time and never publishes them (strata-scale.js:279-287); this file
      //     may not read a picture, so they arrive as handles instead, driven by `pass-composer.js`'s
      //     own "strata-scale" branch of `fillPlan` off `texture.reliefCentreMassX`/
      //     `reliefCentreDetailX` — lab/analyze/recipes.py's own port of the same lines, threaded
      //     through build-elements-v1.py and build-workrecords-v1.py exactly as `luminance.level`
      //     already is for strata-light. A is the departing work's own pair, B the arriving work's.
      //   · the six voice fields, twice — `colourPeriod/Phase/Amp` and `lightPeriod/Phase/Amp` for
      //     each work, driven the same way strata-light's own twelve are (`pass-composer.js`'s
      //     "strata-scale" branch, ported from lab/step4-assembler.js:1966-2010) — ALL TWELVE DRIVEN
      //     ONLY WHERE THIS CUE OWNS LIGHT-COLOUR (shelf 17's levels law), and resting at the
      //     manifest's own 0 otherwise, the module's own silence and not a second mechanism.
      //   · `mask` — the judges' channel, resting where the module has no such thing at all: at 0 the
      //     picture, at 1 the two works' own coverage as colour.
      //
      // TWO FLEET HANDLES ARE ABSENT, and each absence is a fact about this module rather than an
      // oversight:
      //   · `seed` — nothing in this module is rolled. Its cut is the work's own measured relief field
      //     and its motion is a translation; there is no die to publish and inventing one would
      //     publish a handle that reaches nothing.
      //   · `shade` — the judge channel for a contact shadow. This module casts none: a stratum
      //     translates over the frame and nothing here lies on anything.
      handles: {
        // `mix` is the crossing's own dial and `clock` the module's own time; neither drives a
        // structural level of the picture.
        mix: { min: 0, max: 1, def: 0, level: null },
        clock: { min: 0, max: 14, def: 0, level: null },
        // Splits the dial's own travel between the two strata, named for and weighted toward the
        // fine-detail (texture-scale) stratum's own share.
        handover: { min: 0, max: 1, def: FEEL_H_U0,
                    reads: "nothing of either photograph: the module's own single shared handle "
                         + "(strata-scale.js:450-506), resting at the value that reproduces its own "
                         + "rest of DETAIL_SHARE exactly (see this file's own THE HANDOVER note)",
                    level: "TEXTURE" },
        // The mass stratum is the coarse, large-shape reading of the work — a whole-picture drift
        // rather than a grain, which reads as SURFACE. SURFACE is not in this instrument's own
        // `levels` array, so this falls back to CELL, the nearest declared level and the one that
        // already carries this stratum's own travel geometry.
        massCentreXA: { min: 0, max: 1, def: 0.5,
                        reads: "the departing work's own texture.reliefCentreMassX — the mass "
                             + "stratum's own measured centre of gravity, lab/analyze/recipes.py's "
                             + "port of lab/effects/strata-scale.js:279-287",
                        level: "CELL" },
        massCentreXB: { min: 0, max: 1, def: 0.5, reads: "the same of the arriving work",
                        level: "CELL" },
        // The detail stratum is the fine, full-resolution reading of the work, so this is a
        // texture-scale placement.
        detailCentreXA: { min: 0, max: 1, def: 0.5,
                          reads: "the departing work's own texture.reliefCentreDetailX — the detail "
                               + "stratum's own measured centre of gravity, the same port",
                          level: "TEXTURE" },
        detailCentreXB: { min: 0, max: 1, def: 0.5, reads: "the same of the arriving work",
                          level: "TEXTURE" },
        colourPeriodA: { min: 0, max: 4, def: 0, level: "LIGHT-COLOUR" },
        colourPhaseA: { min: 0, max: 1, def: 0, level: "LIGHT-COLOUR" },
        colourAmpA: { min: 0, max: 1, def: 0, level: "LIGHT-COLOUR" },
        lightPeriodA: { min: 0, max: 4, def: 0, level: "LIGHT-COLOUR" },
        lightPhaseA: { min: 0, max: 1, def: 0, level: "LIGHT-COLOUR" },
        lightAmpA: { min: 0, max: 1, def: 0, level: "LIGHT-COLOUR" },
        colourPeriodB: { min: 0, max: 4, def: 0, level: "LIGHT-COLOUR" },
        colourPhaseB: { min: 0, max: 1, def: 0, level: "LIGHT-COLOUR" },
        colourAmpB: { min: 0, max: 1, def: 0, level: "LIGHT-COLOUR" },
        lightPeriodB: { min: 0, max: 4, def: 0, level: "LIGHT-COLOUR" },
        lightPhaseB: { min: 0, max: 1, def: 0, level: "LIGHT-COLOUR" },
        lightAmpB: { min: 0, max: 1, def: 0, level: "LIGHT-COLOUR" },
        // The judges' own coverage channel: it drives no structural level.
        mask: { min: 0, max: 1, def: 0, level: null },
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
      neutrals: { a: 0, b: 1 },
      doors: { in: { handle: "mix", value: 0, work: "a" },
               out: { handle: "mix", value: 1, work: "b" } },
      // BOTH DOORS FRAME ALIKE, and the number is the module's own: the plain cover fit with no crop
      // of its own (strata-scale.js build(), `sc = Math.max(W/iw, H/ih)`).
      framings: { "0": { coverCrop: 1.0 }, "1": { coverCrop: 1.0 } },
      drivers: ["progress", "cueProgress", "time", "velocity", "capability", "noise", "static",
                "curve", "spline", "map", "add", "multiply", "mix", "clamp", "hold", "segment",
                "ramp", "slew", "oscillate", "node"],
      // The construction moves no point of view: it decides which stratum of which work owns each
      // point of the frame and translates it sideways inside the frame, so the witness camera stays
      // the stage's (§6).
      camera: { needs: "none", authority: "stage" },
      gl: { preserveDrawingBuffer: false },
      // WHAT THIS INSTRUMENT WRITES WHERE ITS OWN MATTER IS ABSENT (§7's coverage law). Its absence
      // is the band both a work's own strata have left — the departing work's matter has travelled
      // out of it and the arriving work's has not yet reached it — and this instrument carries no
      // picture of its own for it. At both doors the standing work's own two strata tile the frame,
      // so the alpha is 1 at every point and each door is one whole work, opaque throughout.
      coverage: {
        writes: true,
        how: "max of the two works' own coverage, each 1 where a stratum (masses or detail) of that "
             + "work has carried matter to this point and 0 where neither of its two strata has",
      },
      // The neutral pose is the ENTRY DOOR — `mix` at 0.
      neutralPose: { mix: 0, clock: 0, handover: FEEL_H_U0,
                     massCentreXA: 0.5, massCentreXB: 0.5, detailCentreXA: 0.5, detailCentreXB: 0.5,
                     colourPeriodA: 0, colourPhaseA: 0, colourAmpA: 0,
                     lightPeriodA: 0, lightPhaseA: 0, lightAmpA: 0,
                     colourPeriodB: 0, colourPhaseB: 0, colourAmpB: 0,
                     lightPeriodB: 0, lightPhaseB: 0, lightAmpB: 0,
                     mask: 0, presence: 1, reduced: false, cssWidth: 1000, cssHeight: 1000 },
      passes: [{
        program: "strata-scale", vert: VERT, frag: FRAG, position: "aPos",
        uniforms: [
          { name: "uPresence", type: "float", source: "handle:presence" },
          { name: "uA", type: "sampler2D", source: "textureA" },
          { name: "uB", type: "sampler2D", source: "textureB" },
          { name: "uFitA", type: "vec4", source: "fitA" },
          { name: "uFitB", type: "vec4", source: "fitB" },
          { name: "uRes", type: "vec2", source: "resolution" },
          { name: "uDetailU", type: "vec2", source: "frame:detailU" },
          { name: "uMassU", type: "vec2", source: "frame:massU" },
          { name: "uDetailCentre", type: "vec2", source: "frame:detailCentre" },
          { name: "uMassCentre", type: "vec2", source: "frame:massCentre" },
          { name: "uSat", type: "vec2", source: "frame:sat" },
          { name: "uLight", type: "vec2", source: "frame:light" },
          { name: "uMask", type: "float", source: "handle:mask" },
        ],
      }],
      // The instrument allocates nothing of its own: it spends the two source-texture slots the host
      // already holds and the one programme the host builds from this manifest. The module's own
      // canvases — the standing picture, the masses picture, two grey twins and two per travelling
      // piece — are the textures this port does not ask for: the masses reading is a bilinear blend
      // of the very texture already bound, and the twins are the luminance of the same fetch.
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
                   programs: 1, passes: 1, bytesEstimate: 2000096, variant: "lean" },
                   standard: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0,
                               programs: 1, passes: 1, bytesEstimate: 8000096,
                               variant: "standard" },
                   rich: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                           passes: 1, bytesEstimate: 32000096, variant: "rich" } },
      capabilities: ["webgl2"],
      decline: ["one work only", "a source that never decoded"],
      provenance: { labPath: "lab/effects/strata-scale.js", commit: "fc885a3",
                    sha256: "786e746ab79cd541e4339bb0d4b9f30f5435d6d37cdb76cfff09dbbf6a9bf53a" },
      // HOW WELL THIS INSTRUMENT SUITS A PAIR (2026-08-18, his word of 09:51 and its sharpening at
      // 09:53). Ranking only, never a floor: any two photographs get a crossing on this instrument,
      // since every photograph carries both a masses scale and a detail scale of its own. What ranks
      // it is `texture.reliefEdge` — the same field driving nothing of the geometry directly (see the
      // header's own "THE CENTRE OF GRAVITY IS A PER-WORK READING") but published for exactly this,
      // the module's own `measure(image)`, "a score may carry the number so a разбор can name where
      // it came from" (strata-scale.js:16-18) — read here as the distance between the two works' own
      // measured relief threshold: two works that lose very different shares of their own luminance
      // to the mass scale read as two different textures parting, and two that lose nearly the same
      // share still cross, at the module's own opening pose.
      suits: { reads: ["texture.reliefEdge"],
               how: "each work parts at the median of its own relief field, so what would suit it "
                  + "best is a pair standing far apart in how much of their own luminance the mass "
                  + "scale loses — `texture.reliefEdge`, lab/analyze/recipes.py's port of "
                  + "lab/effects/strata-scale.js:138-141 — and this fit ranks a pair by the distance "
                  + "between their own two relief-edge readings" },
      readiness: "production-ready",
    };

    var live = false;
    return {
      name: "strata-scale",
      manifest: manifest,
      values: values,
      fit: fit,
      feel: feelOf,
      // WHAT THIS INSTRUMENT'S `feel` PROMISES (Phase 7, item 3b): monotone, door to door — the
      // claim, not yet the fact. `feelOf` hinges its two pieces at FEEL_C = 0.47, off the middle,
      // so the two slopes at the join are not forced equal the way a point-symmetric mirror forces
      // them, and the roll call below reads a real speed step there. Declared here so the roll call
      // reaches it and reports what it finds; repairing the hinge is core logic and outside this
      // phase's write-set (curve declaration only for the fleet's remaining instruments).
      feelClass: "monotone",
      voice: voiceAt,
      prepare: function (o) {
        if (!o.sources) return { take: false, why: "the parting-by-scale instrument needs both works" };
        if (!o.cue) return { take: false, why: "no cue names it" };
        return { take: true };
      },
      start: function () { live = true; },
      // The pose the shader draws. Every number in it comes from a handle a score can drive, and
      // nothing in it reads a clock, so a run of one score repeats to the pixel.
      //
      // A DOOR THIS INSTRUMENT CANNOT KEEP WHOLE IS REFUSED RATHER THAN DRAWN. The door law is the
      // instrument's own claim (the manifest's coverage line above), so the instrument is what
      // answers for it: at either door it reads its own two voices and its own geometry on the pose
      // about to be drawn and, where the standing work's own reading is not exactly what the door
      // asks for, hands the host the reason with the readings in it instead of drawing a door that
      // carries a breath the file does not.
      frame: function (st) {
        if (!live) return;
        var h = st.handles;
        var pose = {
          mix: h.mix, mask: h.mask, handover: h.handover,
          massCentreXA: h.massCentreXA, massCentreXB: h.massCentreXB,
          detailCentreXA: h.detailCentreXA, detailCentreXB: h.detailCentreXB,
          colourPeriodA: h.colourPeriodA, colourPhaseA: h.colourPhaseA, colourAmpA: h.colourAmpA,
          lightPeriodA: h.lightPeriodA, lightPhaseA: h.lightPhaseA, lightAmpA: h.lightAmpA,
          colourPeriodB: h.colourPeriodB, colourPhaseB: h.colourPhaseB, colourAmpB: h.colourAmpB,
          lightPeriodB: h.lightPeriodB, lightPhaseB: h.lightPhaseB, lightAmpB: h.lightAmpB,
          presence: h.presence,
          t: h.clock, reduced: st.reduced,
          cssWidth: st.viewport.w, cssHeight: st.viewport.h,
          bufWidth: st.viewport.bufferW, bufHeight: st.viewport.bufferH,
        };
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
          var i = h.mix === 0 ? 0 : 1;
          if (st.reportApplied) {
            st.reportApplied({
              door: h.mix === 0 ? "in" : "out",
              buffer: [pose.bufWidth, pose.bufHeight],
              reads: "the standing work's own detail/masses travel and its own two voices",
              request: [v.detailU[i], v.massU[i], v.colourVoice[i], v.lightVoice[i]],
              applied: [v.detailU[i], v.massU[i], v.colourVoice[i], v.lightVoice[i]],
              moved: 0, unit: "of a frame width, and of the voice's own amplitude",
              standing: [v.dial[i], v.share],
              held: null, whyNo: v.doorWhyNo,
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
    instrument: strataScaleInstrument(),
  });
})();
