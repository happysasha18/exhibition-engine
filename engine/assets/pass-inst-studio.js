/*!pass-inst-studio.js*/
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
// OWNERSHIP. This instrument was carried over from lab/effects/studio.js. The artistic instruments
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
  // THE DARKROOM INSTRUMENT (§8) — lab/effects/studio.js carried across, the owner's word of
  // 2026-08-18 23:21 that every instrument but the shards belongs in the arsenal
  // ================================================================================================
  // WHAT THE MODULE IS. Eight operations in a fixed order — zoom, twirl, planet, mirror,
  // kaleidoscope, endless zoom, tile, colour — each one switchable and each with its own numbers,
  // all applied to one photograph inside a single fragment shader that reads backwards: the shader
  // walks the visible chain in reverse from the pixel on screen until it lands on a point of the
  // photograph (studio.js:1-18, its own header). The module's own `uBench` is already worded as a
  // crossing dial in its own comment — "THE CROSSING DIAL. uBench picks WHICH POINT of the
  // photograph a pixel reads... so one fetch answers every mark of the handle" (studio.js:172-179) —
  // but the crossing it names is between ONE photograph as it was taken and the SAME photograph run
  // through the chain, never between two different works. That is the whole of the gap this port has
  // to close, and closing it is this port's own addition, said plainly below.
  //
  // WHERE IT STANDS IN THE CHARTER. `lab/CROSSING-BRIEF.md`'s vocabulary table carries a bare row —
  // `| studio | — | — | — | unused |` (CROSSING-BRIEF.md:493) — naming no role, no level and no
  // verdict, unlike `shatter`'s row two lines below it, which carries a DATED WORD, "OUT by his 10:28
  // word; returns only on his call" (CROSSING-BRIEF.md:492). `studio`'s row carries no date and
  // stands nowhere in the document's own PARKED section (CROSSING-BRIEF.md:517-531, which lists
  // shatter's own vocabulary by name at 524 and says nothing of studio). "Unused" is a STATUS, not an
  // order: the same word sits beside `liquid` ("unused yet") and `hero` ("unused in crossings yet"),
  // both of which this arsenal has since ported. The owner's word of 2026-08-18 23:21 — every
  // instrument but the shards belongs in the arsenal — finds no dated word here to collide with, and
  // this port is what turns "unused" into "usable", the same turn liquid's and hero's own ports made
  // of their own "unused" rows.
  //
  // ------------------------------------------------------------------------------------------------
  // THE PORT'S OWN ADDITION: THE THERE-AND-BACK, AND WHY IT IS NOT AN INVENTION
  // ------------------------------------------------------------------------------------------------
  // A cue of this engine carries an ORDERED PAIR and owes a door at each end (§8's `arity: 2`), and
  // at each door the law every instrument in this arsenal already answers to is that the frame is
  // the standing work's own file, cover-fitted, and nothing has been done to it. The module's own
  // `bench` runs the other way: at bench 1 the frame is not a second plain photograph but the FIRST
  // one run through the whole chain — the very thing a visitor is curating. Retrofitting a second
  // photograph in at bench 1 without touching the chain's own strength would leave the exit door
  // showing the arriving work WARPED, which is a door no instrument in this arsenal is allowed to
  // draw.
  //
  // `pass-inst-hero.js` met exactly this wall with lab/effects/hero.js, whose own module tells a
  // one-way story (a page scrolls and the planet leaves at the bottom of it) with no second door of
  // its own. Its port's own words: "the story here is walked out and back — out through the folds
  // into the window and the planet, and back out of them into the arriving work... THE THERE-AND-BACK
  // IS THE MODULE'S OWN WALK AND NOT THIS PORT'S INVENTION" (pass-inst-hero.js, "THE ARC, AND WHOSE
  // SHAPE IT IS"). Hero's own module already walked a triangle out and back where nothing drove it
  // (`targetScroll`); studio's own module has no such walk on file, because its bench is a visitor's
  // own hand and not a free-running life. So this port's triangle is not carried DIGIT FOR DIGIT the
  // way hero's is — it is the SAME CONSTRUCTION hero's own port already proved lawful for exactly
  // this class of module (a one-way chain with no second door), read onto a module that has no walk
  // of its own to borrow the shape from. Said here rather than left to be found: this is the one
  // place this port adds a mechanism the lab file does not carry, and it is bounded to the one
  // question every one-way module forced into a two-door arity must answer the same way.
  //
  // THE CONSTRUCTION ITSELF. `mix` runs the passage door to door. Read as a triangle — up from 0 to 1
  // across the first half, back down to 0 across the second — and then through the module's own
  // measured response curve `feel` (studio.js:839-845, carried digit for digit, see below), the
  // result is the CHAIN'S OWN STRENGTH at this instant: the module's `uBench` in every particular
  // except that it now stands at EXACTLY ZERO at BOTH ends of the hand rather than only at the near
  // one. Zero is exact by construction and not by a dead band this file invents: `feel(0) = 0`
  // because `feelHalf(0) = (e^0 - 1)/(e^K - 1) = 0` in exact arithmetic, and a triangle built from
  // `min(u, 1-u)*2` reaches exactly 0 at u=0 and at u=1 for the same reason a straight line does. So
  // at either door the shader's own `mix(p, chain(p), dial)` reads `dial = 0` and returns `p`
  // UNCHANGED, whatever the chain would otherwise compute — the module's own line, untouched — which
  // is what makes a door a door without a single invented constant.
  //
  // WHICH WORK STANDS AT WHICH HALF. The chain is a pure function of a POINT; it holds no memory of
  // which photograph it is bent around. So the departing work stands through the whole outward leg
  // (mix 0 to 0.5, warping up to the chain's own full strength) and the arriving work stands through
  // the whole return leg (mix 0.5 to 1, unwarping back down from that same full strength to nothing)
  // — a single hard swap at the passage's own centre, exactly where the chain stands at its own
  // deepest reach and the frame is furthest from reading as either photograph plainly. No blend is
  // drawn AT the swap: hero's own planet has a rim to sweep a soft ring across (its own "no point of
  // the frame ever shows two photographs at once", hero.js:71-75); studio's chain has no such rim in
  // general — a kaleidoscope of eight wedges is a rosette everywhere at once — so a spatial wipe here
  // would be two ghosts laid over one another rather than a boundary, and this port draws the plain
  // swap instead of inventing one. WHERE THE SWAP STANDS is this port's own second choice and it is
  // named as one: the passage's own centre of symmetry, u = 0.5, the one point the there-and-back
  // construction fixes without a further number to name.
  //
  // ------------------------------------------------------------------------------------------------
  // WHAT CAME OVER, DIGIT FOR DIGIT
  // ------------------------------------------------------------------------------------------------
  // The eight operations' own mathematics — `stCrop`, `stTwirl`, `stPolar`, `stMirror`, `stKal`,
  // `stEndless`, `stTile` and `chain`'s own order (studio.js:59-145) — every uniform they read kept
  // its own name, and `grade` (studio.js:156-165), the colour operation's own hue turn, desaturation
  // and contrast. The measured response curve, `FEEL_K = 3.55` and `feelHalf`/`feel` (studio.js:839-
  // 845). The twirl radius `0.62` (studio.js: `gl.uniform1f(U.uTwirlR, 0.62)`). The endless zoom's
  // three ring sizes, `RING_RATIO = [4.4, 2.9, 1.95]` (studio.js:319), its own phase constant
  // `Math.log(0.58)` and its own drift rate of `0.10` a second (studio.js:909, :959). The
  // kaleidoscope's own drift rate of `0.035` a second and the planet's own spin drift of `0.055` a
  // second (studio.js:907-908). The three colour looks' own pinned saturation and contrast pairs —
  // muted 0.45/0.92, rich 1.38/1.14, inverted 1.0/1.0 with the invert flag standing (studio.js:965-
  // 970). The module's own opening pose — mirror on, mode left-right, fold line at -0.06; planet on,
  // spread 0.62; zoom on, 1.15 — is this port's own neutral pose (studio.js:1023-1027, "open on
  // something worth looking at"), and the module's own declared defaults where the opening pose is
  // silent: twirl amount 1.4, ring twist 0.35 at ring size "some" (index 1), kaleidoscope 8 wedges,
  // tile 2, colour look "rich" (studio.js:408-417).
  //
  // WHAT STAYED BEHIND. Its own canvas, its own WebGL2 context, its own frame loop, its resize
  // observer, its pointer listener and the whole panel it draws over the canvas — the thumbnail
  // strip, the eight sliders, the "surprise me" die and the save-to-PNG road (§1.2's fence, and the
  // same fence every port in this farm answers to). Its own twelve-photograph library
  // (studio.js:301-314) does not travel either: a cue of this engine carries the ordered pair the
  // route already gave it, and studio's own pictures were never that pair's own — see "sources.py")
  // — a module that read from image content this instrument never touches, so nothing about the
  // library crosses. WHAT ELSE DID NOT COME OVER, AND WHY: the module's own two-tap
  // `textureGrad`/`dFdx`/`dFdy` anti-aliasing and its GLSL ES 3.00 `#version 300 es` shader
  // (studio.js:20-38, :182-196). `pass-inst-hero.js` already found this exact wall and left the same
  // finding rather than carrying dead arithmetic: "the host owns every texture in this engine and
  // uploads them clamped at their own edges with no mipmap chain at all... an explicit level-of-
  // detail selects the base level whatever it asks for... both the anti-aliasing and the chroma trick
  // are INERT here" (pass-inst-hero.js). This port answers the same way studio's OWN wedges and
  // rosettes already ask an ordinary GLSL ES 1.00 sampler to answer for every other instrument in
  // this arsenal: a plain `texture2D` call, and the aliasing a hard kaleidoscope seam or a tight tile
  // can show on a small buffer is named here as a real thing this port does without, exactly as hero
  // names it, until the host uploads its sources with a mipmap chain.
  //
  // ------------------------------------------------------------------------------------------------
  // THE COVERAGE: THIS INSTRUMENT FILLS THE FRAME
  // ------------------------------------------------------------------------------------------------
  // §7's coverage law asks every instrument to say where its own matter is absent. It is absent
  // nowhere: the wrap the chain reads is a mirrored, period-two fold of the frame's own square
  // (`uvOf` below, carried from `toTex`, studio.js:150-154) so every point of the frame lands on a
  // point of whichever source is standing, and both sources are sampled clamped at their own edges.
  // The alpha is therefore the constant 1, and under the placement rule this instrument is lawful as
  // the lowest cue of a stack and as a whole one-cue score.
  function studioInstrument() {
    var VERT = [
      "attribute vec2 aPos;",
      "varying vec2 vUv;",
      "void main(){ vUv = vec2(aPos.x * 0.5 + 0.5, 0.5 - aPos.y * 0.5); gl_Position = vec4(aPos, 0.0, 1.0); }",
    ].join("\n");

    // THE SHADER. The eight operations and `grade` are studio.js's own lines, character for
    // character but for their uniform declarations (GLSL ES 1.00 here, `#version 300 es` there) and
    // the two additions named in the header above: `main` reads TWO sources through the SAME warped
    // coordinate instead of one, chosen by `uChange`, and the coordinate walk it drives is `uDial`,
    // this port's own there-and-back reading of `mix`, in the module's own `uBench`'s place.
    var FRAG = [
      "precision highp float;",
      "varying vec2 vUv;",
      "uniform sampler2D uA;",           // the work the visitor is leaving
      "uniform sampler2D uB;",           // the work the visitor is reaching
      "uniform vec4 uFitA;",
      "uniform vec4 uFitB;",
      "uniform vec2 uRes;",
      "uniform float uCropOn;   uniform float uZoom;   uniform vec2  uOff;",
      "uniform float uTwirlOn;  uniform float uTwirl;  uniform float uTwirlR;",
      "uniform float uPolarOn;  uniform float uSpread; uniform float uFlip; uniform float uSpin;",
      "uniform float uMirrorOn; uniform float uMirrorMode; uniform vec2 uFoldLine;",
      "uniform float uKalOn;    uniform float uKalN;   uniform float uKalRot;",
      "uniform float uDrOn;     uniform float uDrL;    uniform float uDrTwist; uniform float uDrPhase;",
      "uniform float uTileOn;   uniform float uTileN;",
      "uniform float uColOn;    uniform float uHue;    uniform float uSat; uniform float uCon; uniform float uInv;",
      // THIS PORT'S OWN TWO, in the module's `uBench`'s place: `uDial` is the chain's own strength at
      // this instant (studio's `uBench` read at the there-and-back triangle instead of at `mix`
      // straight), zero at both doors by construction; `uChange` says which source the chain is bent
      // around, 0 the departing work through the outward leg, 1 the arriving work through the return.
      "uniform float uDial;",
      "uniform float uChange;",
      "uniform float uMask;",            // the fleet's judges' channel: this instrument's own reading, as colour
      "const float PI  = 3.14159265359;",
      "const float TAU = 6.28318530718;",
      "float gSeam;",
      // ---- the eight operations, studio.js's own lines ------------------------------------------
      "vec2 stTile(vec2 p){",
      "  float s = 1.0 / max(uTileN, 1.0);",
      "  vec2 q = p / s + 0.5;",
      "  vec2 c = floor(q);",
      "  vec2 f = fract(q);",
      "  f = mix(f, 1.0 - f, mod(c, 2.0));",
      "  return (f - 0.5) * s;",
      "}",
      "vec2 stEndless(vec2 p, float layer){",
      "  float r = max(length(p), 1e-6);",
      "  float a = atan(p.y, p.x);",
      "  float lr = log(r);",
      "  float x  = (lr - uDrPhase) / uDrL;",
      "  float k  = floor(x);",
      "  gSeam = smoothstep(0.82, 1.0, x - k);",
      "  k += layer;",
      "  lr -= k * uDrL;",
      "  a  -= k * uDrTwist;",
      "  return exp(lr) * vec2(cos(a), sin(a));",
      "}",
      "vec2 stKal(vec2 p){",
      "  float r = length(p);",
      "  float w = TAU / max(uKalN, 2.0);",
      "  float a = atan(p.y, p.x) - uKalRot;",
      "  a = mod(a, w);",
      "  a = abs(a - w * 0.5);",
      "  a += uKalRot;",
      "  return r * vec2(cos(a), sin(a));",
      "}",
      "vec2 stMirror(vec2 p){",
      "  float mx = uMirrorMode > 1.5 && uMirrorMode < 2.5 ? 0.0 : 1.0;",
      "  float my = uMirrorMode < 1.5 ? 0.0 : 1.0;",
      "  p.x = mix(p.x, uFoldLine.x - abs(p.x - uFoldLine.x), mx);",
      "  p.y = mix(p.y, uFoldLine.y - abs(p.y - uFoldLine.y), my);",
      "  return p;",
      "}",
      "vec2 stPolar(vec2 p){",
      "  float r = length(p);",
      "  float a = atan(p.y, p.x) + uSpin;",
      "  float wrap = 2.0 * (uCropOn > 0.5 ? max(uZoom, 0.02) : 1.0);",
      "  float u = a / TAU * wrap;",
      "  float v = r / max(uSpread, 0.05);",
      "  v = mix(v, 1.0 - v, uFlip);",
      "  return vec2(u, v - 0.5);",
      "}",
      "vec2 stTwirl(vec2 p){",
      "  float r = length(p);",
      "  float k = 1.0 - smoothstep(0.0, uTwirlR, r);",
      "  float a = uTwirl * k * k;",
      "  float s = sin(a), c = cos(a);",
      "  return vec2(c * p.x - s * p.y, s * p.x + c * p.y);",
      "}",
      "vec2 stCrop(vec2 p){",
      "  return p / max(uZoom, 0.02) + uOff;",
      "}",
      "vec2 chain(vec2 p, float layer){",
      "  if (uTileOn   > 0.5) p = stTile(p);",
      "  if (uDrOn     > 0.5) p = stEndless(p, layer);",
      "  if (uKalOn    > 0.5) p = stKal(p);",
      "  if (uMirrorOn > 0.5) p = stMirror(p);",
      "  if (uPolarOn  > 0.5) p = stPolar(p);",
      "  if (uTwirlOn  > 0.5) p = stTwirl(p);",
      "  if (uCropOn   > 0.5) p = stCrop(p);",
      "  return p;",
      "}",
      "vec3 grade(vec3 c){",
      "  vec3 k = vec3(0.57735026919);",
      "  float cs = cos(uHue), sn = sin(uHue);",
      "  c = c * cs + cross(k, c) * sn + k * dot(k, c) * (1.0 - cs);",
      "  float l = dot(c, vec3(0.2126, 0.7152, 0.0722));",
      "  c = mix(vec3(l), c, uSat);",
      "  c = (c - 0.5) * uCon + 0.5;",
      "  c = mix(c, 1.0 - c, uInv);",
      "  return c;",
      "}",
      // THIS PORT'S OWN: the mirrored, period-two square fold, carried from `toTex` (studio.js:150-
      // 154). studio's OWN `s` there converts a FRAME-NORMALISED delta straight into a texture delta
      // using the PHOTOGRAPH'S aspect alone (`uTexAsp`), because studio's own `p` already carries the
      // FRAME's aspect correction (`unit` below) — so `s` only has the texture's own share left to
      // supply. The host's `fitA`/`fitB` are a DIFFERENT factor: built for a plain [0,1] uv with no
      // frame-normalisation in it yet, they carry both the frame's aspect and the texture's in one
      // number (pass-inst-hero.js, "THE SOURCE'S OWN SHAPE ARRIVES AS THE HOST'S COVER FIT" — true of
      // `p` itself in hero, which is never frame-normalised before the fit meets it). Feeding this
      // file's own frame-normalised `p` straight to `fitA`/`fitB` would therefore apply the frame's
      // own aspect TWICE. `uvOf` divides the frame's own `unit` back out first, so what reaches the
      // fit is the same plain uv-centred delta every other instrument's `into()` reads.
      //
      // THE SECOND TURN, AND WHY IT STANDS HERE AND NOT ON `p` ITSELF. `p`'s own Y climbs upward —
      // studio.js's own gl_FragCoord convention, kept for the CHAIN, so a twirl turns the way the
      // module turns it and a mirror's fold line sits on the side the module's own `fy` names. A
      // texture's own v runs the other way — v = 0 is a picture's TOP row — so the sample alone
      // turns the sign of the vertical share back before it reaches the fit, and the chain's own
      // geometry never sees that turn at all.
      "vec2 uvOf(vec2 p, vec2 unit, vec4 f){",
      "  vec2 q = 0.5 - abs(mod(p + 0.5, 2.0) - 1.0);",
      "  vec2 qs = vec2(q.x, -q.y);",
      "  return clamp(vec2(0.5) + (qs / unit) * f.xy + f.zw, 0.0008, 0.9992);",
      "}",
      "void main(){",
      // studio's own unit square: the frame's longer axis spans exactly [-0.5, 0.5], the shorter one
      // less (studio.js's `main`, `fit`/`unit`/`p`), read off `vUv` with the row order turned over
      // once because the host uploads its sources unflipped where the module's own canvas convention
      // ran bottom-up (liquid.js's own `vec2 q = vec2(vUv.x, 1.0 - vUv.y);` is the same turn).
      "  float af = uRes.x / max(uRes.y, 1.0);",
      "  float fit = max(af, 1.0);",
      "  vec2 unit = vec2(af, 1.0) / fit;",
      "  vec2 qv = vec2(vUv.x, 1.0 - vUv.y);",
      "  vec2 p = (qv - 0.5) * unit;",
      "  vec2 t0 = mix(p, chain(p, 0.0), uDial);",
      "  float seam = gSeam;",
      "  vec3 col;",
      "  if (uChange > 0.5) { col = texture2D(uB, uvOf(t0, unit, uFitB)).rgb; }",
      "  else { col = texture2D(uA, uvOf(t0, unit, uFitA)).rgb; }",
      "  if (uDrOn > 0.5 && seam > 0.001) {",
      "    vec2 t1 = mix(p, chain(p, 1.0), uDial);",
      "    vec3 alt;",
      "    if (uChange > 0.5) { alt = texture2D(uB, uvOf(t1, unit, uFitB)).rgb; }",
      "    else { alt = texture2D(uA, uvOf(t1, unit, uFitA)).rgb; }",
      "    col = mix(col, alt, seam * uDial);",
      "  }",
      "  if (uColOn > 0.5) { col = mix(col, grade(col), uDial); }",
      // THE JUDGES' OWN FRAME: which work stands (red), the chain's own strength (green), the
      // endless zoom's own seam (blue) — so a row can read the there-and-back construction and the
      // picture change off the picture rather than off this file's word.
      "  vec3 judge = vec3(uChange, clamp(uDial, 0.0, 1.0), seam);",
      "  col = mix(col, judge, uMask);",
      "  gl_FragColor = vec4(clamp(col, 0.0, 1.0), 1.0);",
      "}",
    ].join("\n");

    function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
    function clamp01(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }

    // ---- PINNED NUMBERS, EVERY ONE CITED TO studio.js -------------------------------------------
    var TWIRL_R = 0.62;                        // studio.js: gl.uniform1f(U.uTwirlR, 0.62)
    var RING_RATIO = [4.4, 2.9, 1.95];         // studio.js:319
    var RING_PHASE_BASE = Math.log(0.58);      // studio.js:959, Math.log(0.58)
    var KAL_DRIFT_RATE = 0.035;                // studio.js:908, drift.rot += dt * 0.035
    var POLAR_SPIN_RATE = 0.055;               // studio.js:874/907, drift.spin ... t * 0.055
    var RING_PHASE_RATE = 0.10;                // studio.js:876/909, drift.phase ... t * 0.10
    // THE THREE COLOUR LOOKS' OWN PINNED PAIRS (studio.js:965-970): muted, rich, inverted.
    var LOOK_SAT = [0.45, 1.38, 1.0];
    var LOOK_CON = [0.92, 1.14, 1.0];

    // THE RESPONSE CURVE (studio.js:839-845), carried digit for digit — the one number this port
    // reads at a NEW argument (the there-and-back triangle, "THE PORT'S OWN ADDITION" above) rather
    // than at `mix` straight, and not one digit of the curve itself moved for that.
    var FEEL_K = 3.55;
    function feelHalf(u) { return (Math.exp(FEEL_K * u) - 1) / (Math.exp(FEEL_K) - 1); }
    function feelOf(u) {
      return u <= 0.5 ? 0.5 * feelHalf(2 * u) : 1 - 0.5 * feelHalf(2 - 2 * u);
    }

    // Cover-fit a work into the frame, nothing beyond it: the module's own `uTexAsp` fit, restated
    // as the host's own fit function so `uvOf` above and this file's own reading of a door agree.
    function fit(iw, ih, w, h) {
      var fa = w / Math.max(h, 1);
      var ia = iw / Math.max(ih, 1);
      if (ia > fa) return [fa / ia, 1, 0, 0];
      return [1, ia / fa, 0, 0];
    }

    function gridOf(st) {
      var bw = Math.round(st.bufWidth), bh = Math.round(st.bufHeight);
      if (bw >= 1 && bh >= 1) return { w: bw, h: bh, drawn: true, given: true };
      var cw = Math.round(st.cssWidth), ch = Math.round(st.cssHeight);
      if (cw >= 1 && ch >= 1) return { w: cw, h: ch, drawn: false, given: true };
      return { w: 1, h: 1, drawn: false, given: false };
    }

    // ---- THE NUMBERS OF ONE FRAME ------------------------------------------------------------------
    // Everything the shader gets beyond the seating of the two works is a pure function of the pose,
    // and every number in it comes from a handle a score drives or from the second the host hands
    // down through `clock` — the one place the module read a live clock of its own (its accumulated
    // `life`, studio.js:812) and the one place this port reads `clock` instead, exactly as every
    // other instrument in this arsenal answers §1.2's fence on a module with a breath of its own.
    function posed(st) {
      var u = clamp01(typeof st.mix === "number" ? st.mix : 0);
      // THE THERE-AND-BACK TRIANGLE, and the chain's own strength at this instant — see "THE PORT'S
      // OWN ADDITION" above for why this is not a number invented on top of studio.js, only a
      // construction pass-inst-hero.js already proved for exactly this class of module.
      var x = u <= 0.5 ? u * 2 : (1 - u) * 2;
      var dial = feelOf(x);
      var change = u >= 0.5 ? 1 : 0;
      var t = st.reduced ? 0 : (typeof st.clock === "number" ? st.clock : 0);

      var cropOn = (typeof st.cropOn === "number" ? st.cropOn : 1) > 0.5;
      var zoom = clamp(typeof st.zoom === "number" ? st.zoom : 1.15, 0.30, 3.20);
      var ox = clamp(typeof st.panX === "number" ? st.panX : 0, -0.30, 0.30);
      var oy = clamp(typeof st.panY === "number" ? st.panY : 0, -0.30, 0.30);

      var twirlOn = (typeof st.twirlOn === "number" ? st.twirlOn : 0) > 0.5;
      var twirl = clamp(typeof st.twirlAmt === "number" ? st.twirlAmt : 1.4, -4, 4);

      var polarOn = (typeof st.polarOn === "number" ? st.polarOn : 1) > 0.5;
      var spread = clamp(typeof st.polarSpread === "number" ? st.polarSpread : 0.62, 0.30, 0.95);
      var flip = (typeof st.polarFlip === "number" ? st.polarFlip : 0) > 0.5;
      // THE PLANET'S OWN SPIN DRIFT (studio.js:874, :907): the breath the module carries whenever no
      // pointer drives it. A crossing has no pointer, so it always runs on the handed second.
      var spin = polarOn ? t * POLAR_SPIN_RATE : 0;

      var mirrorOn = (typeof st.mirrorOn === "number" ? st.mirrorOn : 1) > 0.5;
      var mode = clamp(Math.round(typeof st.mirrorMode === "number" ? st.mirrorMode : 0), 0, 2);
      var fx = clamp(typeof st.foldX === "number" ? st.foldX : -0.06, -0.50, 0.50);
      var fy = clamp(typeof st.foldY === "number" ? st.foldY : 0, -0.50, 0.50);

      var kalOn = (typeof st.kalOn === "number" ? st.kalOn : 0) > 0.5;
      var kalN = clamp(Math.round(typeof st.kalN === "number" ? st.kalN : 8), 3, 16);
      // THE KALEIDOSCOPE'S OWN DRIFT (studio.js:875, :908): the same breath, on this instrument's
      // own turning handle.
      var kalRotBase = typeof st.kalRot === "number" ? st.kalRot : 0;
      var kalRot = kalOn ? kalRotBase + t * KAL_DRIFT_RATE : kalRotBase;

      var ringOn = (typeof st.ringOn === "number" ? st.ringOn : 0) > 0.5;
      var ringSize = clamp(Math.round(typeof st.ringSize === "number" ? st.ringSize : 1), 0, 2);
      var ringTwist = clamp(typeof st.ringTwist === "number" ? st.ringTwist : 0.35, -1.20, 1.20);
      var logRatio = Math.log(RING_RATIO[ringSize]);
      var drTwist = ringTwist * (Math.PI * 2) / 4;
      // THE ENDLESS ZOOM'S OWN DRIFT (studio.js:876, :909): a phase that always runs while the ring
      // is on, never gated by a pointer in the module either.
      var phaseFrac = ringOn ? t * RING_PHASE_RATE : 0;
      phaseFrac = phaseFrac - Math.floor(phaseFrac);
      var drPhase = RING_PHASE_BASE - logRatio - phaseFrac * logRatio;

      var tileOn = (typeof st.tileOn === "number" ? st.tileOn : 0) > 0.5;
      var tileN = clamp(Math.round(typeof st.tileN === "number" ? st.tileN : 2), 2, 6);

      var colOn = (typeof st.colOn === "number" ? st.colOn : 0) > 0.5;
      var hue = clamp(typeof st.hue === "number" ? st.hue : 0, -Math.PI, Math.PI);
      var look = clamp(Math.round(typeof st.colLook === "number" ? st.colLook : 1), 0, 2);

      return {
        dial: dial, change: change, x: x, u: u,
        cropOn: cropOn ? 1 : 0, zoom: zoom, off: [ox, oy],
        twirlOn: twirlOn ? 1 : 0, twirl: twirl, twirlR: TWIRL_R,
        polarOn: polarOn ? 1 : 0, spread: spread, flip: flip ? 1 : 0, spin: spin,
        mirrorOn: mirrorOn ? 1 : 0, mode: mode, foldLine: [fx, fy],
        kalOn: kalOn ? 1 : 0, kalN: kalN, kalRot: kalRot,
        ringOn: ringOn ? 1 : 0, drL: logRatio, drTwist: drTwist, drPhase: drPhase,
        tileOn: tileOn ? 1 : 0, tileN: tileN,
        colOn: colOn ? 1 : 0, hue: hue,
        sat: LOOK_SAT[look], con: LOOK_CON[look], inv: look === 2 ? 1 : 0,
        mask: clamp01(typeof st.mask === "number" ? st.mask : 0),
        grid: gridOf(st),
      };
    }

    // ---- THE DOOR THIS INSTRUMENT READS FOR ITSELF -------------------------------------------------
    // His 18:00 architecture decision, carried in the U27 brief: the instrument reads its own doors
    // at run time and the report it hands back is the run-time truth. This instrument's own doors
    // hold by ALGEBRA rather than by a grid: `dial` is exactly 0 at `mix` 0 and at `mix` 1 because
    // `feel(0) = 0` in exact arithmetic and the there-and-back triangle reaches exactly 0 at both
    // ends, and `mix(p, chain(p), 0)` returns `p` exactly whatever `chain(p)` computes. No buffer, no
    // cell count and no sample grid can open that multiplication back up, so the reading below has no
    // width to walk — it is the one number, checked, rather than a search across a grid.
    function doorReadOf(v, st) {
      var want = st.mix === 0 ? "in" : (st.mix === 1 ? "out" : null);
      if (want === null) return null;
      return { door: want, dial: v.dial, grid: v.grid };
    }

    function doorWhyNoOf(read) {
      if (!read) return null;
      if (read.dial === 0) return null;
      // Unreachable on any pose this file as written can produce — `feelOf` returns exactly 0 at the
      // triangle's own two ends and nowhere else the door reading is taken — and it is said here
      // rather than removed, the same way strata-light's own door note is: a claim proved, not a
      // range guarded.
      return "the " + (read.door === "in" ? "entry" : "exit") + " door leaks: the chain's own "
           + "strength reads " + read.dial + " where its own construction asks for exactly 0";
    }

    function values(st) {
      var v = posed(st);
      var read = doorReadOf(v, st);
      v.doorGrid = read ? read.grid : null;
      v.doorWhyNo = doorWhyNoOf(read);
      return v;
    }

    var manifest = {
      id: "studio", api: 1, arity: 2,
      // The departing work bends up through the chain across the outward leg, the passage's own
      // centre is where neither work is legible — the chain stands at its own deepest reach — and
      // the arriving work unwinds back down through the same chain across the return leg.
      roles: ["disassembly", "mystery", "assembly"],
      // THE TWO LEVELS THIS INSTRUMENT ACTS ON, and the levels law's own defect named so it is not
      // repeated: shelf 17 asks every instrument to declare every structural level it acts on, not
      // fewer, and strata-light's own port names the exact miss this one avoids — claiming CELL alone
      // while its own colour-and-light voices act on LIGHT-COLOUR too. This instrument declares two
      // for the parallel reason.
      //   · TEXTURE — the eight operations bend the picture's OWN MATERIAL: a twirl turns it about a
      //     centre, a kaleidoscope folds it into wedges, an endless zoom nests it inside itself, a
      //     tile repeats it, a mirror folds it onto itself. None of them cuts the frame into named
      //     pieces or regions; all of them warp the coordinate a point of material is read from,
      //     which is liquid's own level for the same reason ("the water bends the picture's own
      //     material", pass-inst-liquid.js) and studio's own chain does the same act by a coordinate
      //     walk instead of a displacement field.
      //   · LIGHT-COLOUR — the colour operation turns the picture's hue, drains or lifts its
      //     saturation and stretches its contrast (`grade`, studio.js:156-165), the same act
      //     grid-colour's and strata-light's own colour voices are placed at (pass-inst-grid-
      //     colour.js, pass-inst-strata-light.js).
      // SURFACE is NOT claimed. A SURFACE-level instrument decides, POINT BY POINT, which of the two
      // works stands there (adrift, liquid's own second level, gates' whole construction); this
      // instrument's picture change is a single hard swap for the WHOLE FRAME at once (see the header
      // above), never a field that varies across it, so no point of the frame is ever in question
      // about which work it belongs to independent of any other point.
      levels: ["TEXTURE", "LIGHT-COLOUR"],
      // WHAT THIS INSTRUMENT CUTS ON. WEDGE, because the kaleidoscope folds the frame into angular
      // wedges about a turning centre; RING, because the endless zoom nests the picture inside rings
      // of itself at a measured spacing; TILE, because the tile operation repeats the picture across
      // the plane, mirrored at every seam — three of the module's own eight operations, each cutting
      // the frame a different way, and the composer's own `KIND_OF_MEASURE` already carries all
      // three in its vocabulary (droste and kaleidoscope both cut on `ring`, parquet on `tile`).
      cuts: ["ring", "wedge", "tile"],
      // THE MODULE'S OWN SLIDER-FACING NUMBERS (studio.js:549-594), published beside their ranges —
      // the artistic eight a visitor's own hand would reach for first. The mode words, the on/off
      // switches and the two handles this port drives off a measurement (`panX`/`panY`, `foldX`/
      // `foldY` share that pair) are not params for the same reason gates' three slot handles are
      // not: a page that grew a slider for them would fight a score that already drives them.
      params: { zoom: [0.30, 3.20], twirlAmt: [-4, 4], polarSpread: [0.30, 0.95],
                foldX: [-0.50, 0.50], foldY: [-0.50, 0.50], kalN: [3, 16],
                ringTwist: [-1.20, 1.20], tileN: [2, 6], hue: [-3.14159, 3.14159] },
      // EVERY handle a score can drive (§4.4b). `mix` is the dial and `clock` is the second the host
      // hands down — the one place the module read a clock of its own, its `life` (studio.js:812),
      // for the three operations' own breath (kaleidoscope, planet, endless zoom). The twenty-four
      // below are the eight operations' own switches and numbers, at the module's own defaults or its
      // own "open on something worth looking at" pose (studio.js:1023-1027). `mask` is the fleet's
      // own judges' channel, resting where the module has no such thing at all.
      //
      // SIX ARE DRIVEN OFF A MEASUREMENT, and the composer's own "studio" branch in `fillPlan`
      // carries the reading:
      //   · `kalN` — the pair's own measured rotational order, `structure.rotational.n`, the same
      //     reading the kaleidoscope instrument's own `wedges` handle already reads.
      //   · `tileN` — the pair's own measured lattice count, `structure.grid.periodPx` said as a
      //     count across the frame side, the same reading parquet's own `tiles` handle reads.
      //   · `polarSpread` — how strongly the pair reads as a little world, `structure.polar.planet`,
      //     the same reading hero's own `planet` handle reads, placed on this handle's own span.
      //   · `twirlAmt` — how strongly the pair's own making already winds, `structure.polar.twirl`,
      //     the same reading kaleidoscope's own `twist` handle reads.
      //   · `panX`/`panY` and `foldX`/`foldY` — the midpoint of the two works' own measured radial
      //     centres, the same construction hero's and livemirror's and kaleidoscope's own centre
      //     handles already read (`centreOfThePair` in pass-composer.js).
      // THE REST REST AT THE MODULE'S OWN NUMBERS, AND EACH SAYS SO HONESTLY RATHER THAN HIDING IT
      // (his law of 2026-08-18 15:13): no reading in a work record says whether a visitor's own hand
      // would have switched an operation on, how far a zoom or a fold or a tile count or a hue turn
      // should stand, or how a ring should size itself — these are the module's own eight-way choice
      // of instrument the way `jamb`/`teeth`/`swing` are gates' own choice of departure, and they
      // rest at the numbers named in "WHAT CAME OVER" above, the same for every pair until a
      // measurement answers them.
      handles: {
        // NO LEVEL FOR `mix` OR `clock`: mix is the crossing's own dial, the passage itself, and
        // clock is the module's own time — neither drives a structural level.
        mix: { min: 0, max: 1, def: 0, level: null },
        clock: { min: 0, max: 14, def: 0, level: null },
        cropOn: { min: 0, max: 1, def: 1, level: "TEXTURE" },
        zoom: { min: 0.30, max: 3.20, def: 1.15, level: "TEXTURE" },
        panX: { min: -0.30, max: 0.30, def: 0,
                reads: "the midpoint of the two works' own measured radial centres, "
                     + "structure.radial.centre — the same construction hero's centreX reads",
                level: "TEXTURE" },
        panY: { min: -0.30, max: 0.30, def: 0,
                reads: "the midpoint of the two works' own measured radial centres, "
                     + "structure.radial.centre — the same construction hero's centreY reads",
                level: "TEXTURE" },
        twirlOn: { min: 0, max: 1, def: 0, level: "TEXTURE" },
        twirlAmt: { min: -4, max: 4, def: 1.4,
                    reads: "structure.polar.twirl, how strongly the pair's own making already winds — "
                         + "the same reading kaleidoscope's own twist handle reads",
                    level: "TEXTURE" },
        polarOn: { min: 0, max: 1, def: 1, level: "TEXTURE" },
        polarSpread: { min: 0.30, max: 0.95, def: 0.62,
                       reads: "structure.polar.planet, how strongly the pair reads as a little world — "
                            + "the same reading hero's own planet handle reads",
                       level: "TEXTURE" },
        polarFlip: { min: 0, max: 1, def: 0, level: "TEXTURE" },
        mirrorOn: { min: 0, max: 1, def: 1, level: "TEXTURE" },
        mirrorMode: { min: 0, max: 2, def: 0, kind: "count", applied: { roundedToAWholeMode: true },
                      level: "TEXTURE" },
        foldX: { min: -0.50, max: 0.50, def: -0.06,
                 reads: "the midpoint of the two works' own measured radial centres, "
                      + "structure.radial.centre — the same construction livemirror's own fold reads",
                 level: "TEXTURE" },
        foldY: { min: -0.50, max: 0.50, def: 0,
                 reads: "the midpoint of the two works' own measured radial centres, "
                      + "structure.radial.centre — the same construction livemirror's own fold reads",
                 level: "TEXTURE" },
        kalOn: { min: 0, max: 1, def: 0, level: "TEXTURE" },
        kalN: { min: 3, max: 16, def: 8, kind: "count", applied: { roundedToAWholeCount: true },
                reads: "structure.rotational.n, the pair's own measured rotational order — the same "
                     + "reading kaleidoscope's own wedges handle reads",
                level: "TEXTURE" },
        kalRot: { min: -6.5, max: 6.5, def: 0, level: "TEXTURE" },
        ringOn: { min: 0, max: 1, def: 0, level: "TEXTURE" },
        ringTwist: { min: -1.20, max: 1.20, def: 0.35, level: "TEXTURE" },
        ringSize: { min: 0, max: 2, def: 1, kind: "count", applied: { roundedToAWholeSize: true },
                    level: "TEXTURE" },
        tileOn: { min: 0, max: 1, def: 0, level: "TEXTURE" },
        tileN: { min: 2, max: 6, def: 2, kind: "count", applied: { roundedToAWholeCount: true },
                 reads: "structure.grid.periodPx said as a count across the work's own frame side — "
                      + "the same reading parquet's own tiles handle reads",
                 level: "TEXTURE" },
        colOn: { min: 0, max: 1, def: 0, level: "LIGHT-COLOUR" },
        hue: { min: -3.14159, max: 3.14159, def: 0, unit: "radians", level: "LIGHT-COLOUR" },
        colLook: { min: 0, max: 2, def: 1, kind: "count", applied: { roundedToAWholeLook: true },
                   level: "LIGHT-COLOUR" },
        // THE FLEET'S JUDGES' CHANNEL: at 0 the picture, at 1 which work stands (red), the chain's
        // own strength (green) and the endless zoom's own seam (blue) — the one handle here the lab
        // module has no counterpart for. NO LEVEL: a judge channel, not a structural act.
        mask: { min: 0, max: 1, def: 0,
                applied: { shows: "which work stands as red, the chain's own strength as green and "
                                + "the endless zoom's own seam as blue" },
                level: null },
      },
      neutrals: { a: 0, b: 1 },
      doors: { in: { handle: "mix", value: 0, work: "a" },
               out: { handle: "mix", value: 1, work: "b" } },
      // BOTH DOORS FRAME AT A CROP OF EXACTLY ONE: the chain's own strength is zero at both ends of
      // the hand by construction (see the header), so no headroom is ever bought from either picture.
      framings: { "0": { coverCrop: 1 }, "1": { coverCrop: 1 } },
      drivers: ["progress", "cueProgress", "time", "velocity", "capability", "noise", "static",
                "curve", "spline", "map", "add", "multiply", "mix", "clamp", "hold", "segment",
                "ramp", "slew", "oscillate", "node"],
      // The construction moves no point of view: it decides which work the chain is bent around and
      // walks the sample coordinate for the whole frame at once, so the witness camera stays the
      // stage's (§6).
      camera: { needs: "none", authority: "stage" },
      gl: { preserveDrawingBuffer: false },
      // THE COVERAGE LAW (§7). Every point of the frame lands on a point of whichever source is
      // standing — the mirrored, period-two fold repeats the picture over the whole plane and the
      // host's own sources are clamped at their own edges — so the alpha is the constant 1, a
      // decision rather than a default, and this instrument may stand at the bottom of a stack.
      coverage: { writes: false,
                  how: "the mirrored, period-two fold of the frame's own square lands every point on "
                     + "a point of whichever source the chain is bent around, so no point of the "
                     + "frame is ever left unclaimed and the alpha is the constant 1" },
      neutralPose: { mix: 0, clock: 0, cropOn: 1, zoom: 1.15, panX: 0, panY: 0,
                     twirlOn: 0, twirlAmt: 1.4, polarOn: 1, polarSpread: 0.62, polarFlip: 0,
                     mirrorOn: 1, mirrorMode: 0, foldX: -0.06, foldY: 0,
                     kalOn: 0, kalN: 8, kalRot: 0,
                     ringOn: 0, ringTwist: 0.35, ringSize: 1,
                     tileOn: 0, tileN: 2, colOn: 0, hue: 0, colLook: 1, mask: 0,
                     reduced: false, cssWidth: 1000, cssHeight: 1000 },
      passes: [{
        program: "studio", vert: VERT, frag: FRAG, position: "aPos",
        uniforms: [
          { name: "uA", type: "sampler2D", source: "textureA" },
          { name: "uB", type: "sampler2D", source: "textureB" },
          { name: "uFitA", type: "vec4", source: "fitA" },
          { name: "uFitB", type: "vec4", source: "fitB" },
          { name: "uRes", type: "vec2", source: "resolution" },
          { name: "uCropOn", type: "float", source: "frame:cropOn" },
          { name: "uZoom", type: "float", source: "frame:zoom" },
          { name: "uOff", type: "vec2", source: "frame:off" },
          { name: "uTwirlOn", type: "float", source: "frame:twirlOn" },
          { name: "uTwirl", type: "float", source: "frame:twirl" },
          { name: "uTwirlR", type: "float", source: "frame:twirlR" },
          { name: "uPolarOn", type: "float", source: "frame:polarOn" },
          { name: "uSpread", type: "float", source: "frame:spread" },
          { name: "uFlip", type: "float", source: "frame:flip" },
          { name: "uSpin", type: "float", source: "frame:spin" },
          { name: "uMirrorOn", type: "float", source: "frame:mirrorOn" },
          { name: "uMirrorMode", type: "float", source: "frame:mode" },
          { name: "uFoldLine", type: "vec2", source: "frame:foldLine" },
          { name: "uKalOn", type: "float", source: "frame:kalOn" },
          { name: "uKalN", type: "float", source: "frame:kalN" },
          { name: "uKalRot", type: "float", source: "frame:kalRot" },
          { name: "uDrOn", type: "float", source: "frame:ringOn" },
          { name: "uDrL", type: "float", source: "frame:drL" },
          { name: "uDrTwist", type: "float", source: "frame:drTwist" },
          { name: "uDrPhase", type: "float", source: "frame:drPhase" },
          { name: "uTileOn", type: "float", source: "frame:tileOn" },
          { name: "uTileN", type: "float", source: "frame:tileN" },
          { name: "uColOn", type: "float", source: "frame:colOn" },
          { name: "uHue", type: "float", source: "frame:hue" },
          { name: "uSat", type: "float", source: "frame:sat" },
          { name: "uCon", type: "float", source: "frame:con" },
          { name: "uInv", type: "float", source: "frame:inv" },
          { name: "uDial", type: "float", source: "frame:dial" },
          { name: "uChange", type: "float", source: "frame:change" },
          { name: "uMask", type: "float", source: "handle:mask" },
        ],
      }],
      resources: { lean: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                           passes: 1, bytesEstimate: 0, variant: "lean" },
                   standard: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                               passes: 1, bytesEstimate: 0, variant: "standard" },
                   rich: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                           passes: 1, bytesEstimate: 0, variant: "rich" } },
      capabilities: ["webgl2"],
      decline: ["one work only", "a source that never decoded"],
      provenance: { labPath: "lab/effects/studio.js", commit: "2afa485",
                    sha256: "50428c1904aa9be72e35cb29eddbf1dc99ccea62eb6d82a51d2389bfe62de73d" },
      // HOW WELL THIS INSTRUMENT SUITS A PAIR (2026-08-18, his word of 09:51 and its sharpening at
      // 09:53). Ranking only, never a floor: any two photographs get a crossing on this instrument.
      // The chain's own operations read best on a pair whose own structure already carries the
      // vocabulary the operations turn on — a rotational order for the kaleidoscope, a device of
      // rings for the endless zoom, a lattice for the tile — so the reading ranks a pair by how much
      // of that vocabulary the two works carry, and a pair carrying none of it still plays at the
      // module's own opening pose.
      suits: { reads: ["structure.rotational", "structure.polar", "structure.grid",
                       "structure.radial"],
               how: "the operations read best on a pair whose own structure already carries a "
                  + "rotational order, a little-world reading, a measured lattice or a radial centre "
                  + "— the vocabulary the kaleidoscope, the planet, the tile and the fold turn on — so "
                  + "the fit ranks how much of that vocabulary the two works carry between them, and a "
                  + "pair carrying none of it still plays at the module's own opening pose" },
      readiness: "production-ready",
    };

    var live = false;
    return {
      name: "studio",
      manifest: manifest,
      values: values,
      fit: fit,
      feel: feelOf,
      prepare: function (o) {
        if (!o.sources) return { take: false, why: "the darkroom instrument needs both works" };
        if (!o.cue) return { take: false, why: "no cue names it" };
        return { take: true };
      },
      start: function () { live = true; },
      frame: function (st) {
        if (!live) return;
        var h = st.handles;
        var pose = {
          mix: h.mix, clock: h.clock,
          cropOn: h.cropOn, zoom: h.zoom, panX: h.panX, panY: h.panY,
          twirlOn: h.twirlOn, twirlAmt: h.twirlAmt,
          polarOn: h.polarOn, polarSpread: h.polarSpread, polarFlip: h.polarFlip,
          mirrorOn: h.mirrorOn, mirrorMode: h.mirrorMode, foldX: h.foldX, foldY: h.foldY,
          kalOn: h.kalOn, kalN: h.kalN, kalRot: h.kalRot,
          ringOn: h.ringOn, ringTwist: h.ringTwist, ringSize: h.ringSize,
          tileOn: h.tileOn, tileN: h.tileN,
          colOn: h.colOn, hue: h.hue, colLook: h.colLook, mask: h.mask,
          reduced: st.reduced, cssWidth: st.viewport.w, cssHeight: st.viewport.h,
          bufWidth: st.viewport.bufferW, bufHeight: st.viewport.bufferH,
        };
        if (h.mix === 0 || h.mix === 1) {
          var v = values(pose);
          if (st.reportApplied) {
            st.reportApplied({
              door: h.mix === 0 ? "in" : "out",
              buffer: [pose.bufWidth, pose.bufHeight],
              reads: "the chain's own strength",
              request: v.dial, applied: v.dial, moved: 0, unit: "of the there-and-back triangle",
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
    instrument: studioInstrument(),
  });
})();
