/*!pass-inst-strata-light.js*/
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
  // THE PARTING-BY-LIGHT INSTRUMENT (§8) — lab/effects/strata-light.js carried across
  // ================================================================================================
  // WHAT THE VISITOR SEES. The departing photograph splits along its own light: everything at or
  // above a level of its own tone is the BRIGHT stratum and everything below it the DARK one. The
  // bright half slides straight up and out of the top of the frame while the dark half slides
  // straight down and out of the bottom, and the arriving photograph's two halves come in the
  // opposite way at the same instant — its bright half down out of the top, its dark half up out of
  // the bottom — until they close on each other and the second work stands whole. Nothing is ever
  // faded: what leaves the eye leaves the frame, and where neither work's matter has reached yet
  // this instrument carries nothing and whatever plays beneath it is seen.
  //
  // ONE MODULE, TWO LAYERS, ONE PASS. The lab module holds ONE work (`needs: 1`) and its dial runs
  // from the work standing whole to an EMPTY frame. The engine's instruments run over an ordered
  // PAIR with an exact door at each end, and an empty frame is no door. The module's own header
  // names the road out: «The same dial run backwards, 1 → 0, slides the strata together into the
  // whole work — which is how a layer ARRIVES without a fade». So this instrument is the module read
  // TWICE in one pass: the departing work's own dial runs 0 → 1 as `mix` does, the arriving work's
  // runs 1 → 0, and both are put through the module's own response curve. At `mix` 0 the departing
  // work stands whole and the arriving work is wholly outside the frame; at `mix` 1 the opposite.
  // Both doors are exact by construction on any grid, and the paragraph THE DOOR THE INSTRUMENT
  // READS FOR ITSELF below says exactly why.
  //
  // ------------------------------------------------------------------------------------------------
  // WHAT CAME OVER
  // ------------------------------------------------------------------------------------------------
  //   · THE CUT. A work parts at a level of its own luminance, read on a grid of `cells` over the
  //     FILE — the module's own `lumGrid`/`MASK_CELLS`, so the mask is the work's and not the crop's
  //     and its edges step at the cell rather than at the pixel.
  //   · THE TWO SENSES. Bright leaves upward, dark leaves downward (strata-light.js:240).
  //   · THE RESPONSE CURVE, digit for digit: the two-piece exponential hinged at the measured median
  //     of the felt change, FEEL_C 0.37, FEEL_K1 −0.2, FEEL_K2 2.2 (strata-light.js:335-355).
  //   · BOTH ACCOMPANYING VOICES, digit for digit: `a·sin(2π(u/p + phase))·4u(1−u)`, the colour
  //     voice breathing a piece's saturation against its own grey twin and the light voice writing
  //     the standing matter lighter and darker, each held to nothing at both doors by the window
  //     (strata-light.js:283-312).
  //   · NO FADE ANYWHERE. A point either carries a work's matter or it does not; the alpha this
  //     shader writes is 1 or 0 and never anything between.
  //
  // ------------------------------------------------------------------------------------------------
  // WHAT DID NOT COME OVER, NAMED RATHER THAN SMOOTHED OVER
  // ------------------------------------------------------------------------------------------------
  // THE CONNECTED AREAS. The module cuts each stratum into the CONNECTED AREAS of its mask and
  // travels each area as a rigid piece by exactly the distance that clears the frame for that piece
  // — a flood fill over the mask grid, a bounding box per area and one draw per area per frame
  // (strata-light.js:85-106, 214-244). A fragment shader is handed one output point and has to
  // answer it by looking BACK along a travel, so it can only invert a displacement it can name from
  // the point alone. A per-area distance cannot be named from the point: it is a property of the
  // whole area the point belongs to, and finding that area means labelling connected components,
  // which needs repeated passes over a framebuffer and a reduction per label that a fragment shader
  // has no way to take. Solving it once on the first frame is the other road and it is closed for a
  // second reason as well: it means reading the picture's pixels, and §1.2 leaves no canvas, no
  // context and no image in this file to read them with.
  //
  // WHAT STANDS INSTEAD, and what it costs. Each STRATUM travels as ONE rigid body over exactly ONE
  // FRAME HEIGHT — the distance that clears the frame for every piece of it at once, since a bright
  // piece's own bottom edge and a dark piece's own top edge both lie inside the frame. So rigidity
  // survives whole (a stratum only translates; nothing is stretched, sheared or scaled), the two
  // senses survive, nothing fades, and both doors stay exact. What is lost is that the picture no
  // longer comes apart into MANY pieces each moving at its own rate: it parts into TWO, and a bright
  // area near the top of the frame — which in the module clears the frame early and stands still
  // thereafter — here keeps moving with the rest of its stratum until it is out. `MAX_AREAS = 64`,
  // the module's own draw budget, therefore has no counterpart here at all.
  //
  // THE CELL IS READ AT ITS CENTRE. The module reads a cell as the MEAN of the file's pixels inside
  // it — a smoothed draw of the picture down to the mask grid (strata-light.js:59-72). This file
  // reads the cell at its own centre point instead, one fetch, because averaging the cell in the
  // shader means either walking its pixels (sixteen fetches a point where the module takes one) or
  // walking the picture's chain of smaller copies, whose level is chosen from the derivative of the
  // coordinate — and the coordinate here is a step function, constant inside a cell and jumping at
  // its edge, so the chain would be read at the wrong level on exactly the points at a cell's
  // boundary. What it costs is that a cell whose centre is untypical of it falls on the other side
  // of the level from where the module puts it; the suite measures that share on the two
  // photographs it runs on and prints the number rather than assuming it.
  //
  // THE MEASUREMENT ITSELF. `measure(image)` publishes the median of the work's own luminance at
  // build time (strata-light.js:110-113), and the module handed no `level` measures its own picture.
  // This file may not read a picture, so the level arrives as a handle per work — `levelA`, `levelB`
  // — exactly as the drifting instrument's own measured thresholds do. Where a score names none, the
  // handle rests at the module's OWN answer for a picture it cannot read, `{ level: 0.5 }`
  // (strata-light.js:111).
  function strataLightInstrument() {
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
      // each work's own dial: the departing work's runs 0 to 1 with the hand, the arriving work's
      // runs 1 to 0, both through the module's own response curve
      "uniform vec2 uDial;",
      // the level each work parts at, on its own luminance
      "uniform vec2 uLevel;",
      // the mask grid each work is read on, cells across its own long side
      "uniform vec2 uCells;",
      // how much palette each work's drawn matter holds now — the colour voice
      "uniform vec2 uSat;",
      // and how much lighter or darker the light voice writes it, signed
      "uniform vec2 uLight;",
      // the judges' handle: the two works' own coverage as colour
      "uniform float uMask;",
      "uniform float uPresence;",  // the entry-door contract's reserved dry
      "vec2 into(vec2 p, vec4 f){",
      "  return clamp((p - 0.5) * f.xy + 0.5 + f.zw, 0.0008, 0.9992);",
      "}",
      // the module's own luminance, the same three weights it reads its grid with
      "float lumaOf(vec3 c){ return dot(c, vec3(0.2126, 0.7152, 0.0722)); }",
      // THE MASK GRID OF ONE FILE — `cells` on its long side and the short side in proportion,
      // exactly the module's own `lumGrid`. The file's own aspect is recovered from the seating the
      // host applied: a cover fit carries the frame's aspect times the ratio of its two scales.
      "vec2 gridOf(float cells, vec4 f, float aspect){",
      "  float ia = aspect * f.y / max(f.x, 1e-4);",
      "  float other = max(1.0, floor((ia >= 1.0 ? cells / ia : cells * ia) + 0.5));",
      "  return ia >= 1.0 ? vec2(cells, other) : vec2(other, cells);",
      "}",
      // the cell a point falls in, read at its own centre
      "vec2 cellOf(vec2 t, vec2 g){ return (floor(t * g) + 0.5) / g; }",
      // ONE WORK'S OWN MATTER AT THIS POINT. Its bright stratum has travelled `u` frame heights UP
      // and its dark stratum `u` DOWN, each as one rigid body, so the matter standing here came from
      // `u` BELOW this point if it is bright and `u` ABOVE it if it is dark. A source point outside
      // the frame is a stratum that has travelled wholly out, and there is nothing of it here.
      //
      // WHERE BOTH STRATA HAVE CARRIED MATTER TO ONE POINT the bright one stands over the dark one.
      // The module settles this by draw order alone — its pieces are drawn largest first, so the
      // last piece drawn wins and neither stratum owns the rule — so the port had to choose, and it
      // chose the stratum travelling toward the top. At the doors the two strata tile the picture
      // and never meet, so the choice is invisible at either end of the hand.
      "vec4 matterOf(sampler2D tex, vec4 f, vec2 g, float lev, float u, float sat, float lit, vec2 uv){",
      "  vec4 got = vec4(0.0);",
      "  vec2 sd = vec2(uv.x, uv.y - u);",
      "  if (sd.y >= 0.0 && sd.y <= 1.0) {",
      "    vec2 t = into(sd, f);",
      "    if (lumaOf(texture2D(tex, cellOf(t, g)).rgb) < lev) got = vec4(texture2D(tex, t).rgb, 1.0);",
      "  }",
      "  vec2 sb = vec2(uv.x, uv.y + u);",
      "  if (sb.y >= 0.0 && sb.y <= 1.0) {",
      "    vec2 t = into(sb, f);",
      "    if (lumaOf(texture2D(tex, cellOf(t, g)).rgb) >= lev) got = vec4(texture2D(tex, t).rgb, 1.0);",
      "  }",
      "  if (got.a <= 0.0) return got;",
      // THE COLOUR VOICE — the piece's own grey twin blended into it at its own moved position, so
      // the saturation breathes and the piece's own alpha never moves (strata-light.js:246-252).
      "  got.rgb = mix(vec3(lumaOf(got.rgb)), got.rgb, sat);",
      // THE LIGHT VOICE — written over what is drawn and ONLY where something is drawn, so this is a
      // move of light and nothing else and an empty frame stays empty (strata-light.js:300-312).
      "  got.rgb = mix(got.rgb, vec3(step(0.0, lit)), abs(lit));",
      "  return got;",
      "}",
      "void main(){",
      "  vec2 uv = vUv;",
      "  float aspect = uRes.x / max(uRes.y, 1.0);",
      "  vec4 a = matterOf(uA, uFitA, gridOf(uCells.x, uFitA, aspect),",
      "                    uLevel.x, uDial.x, uSat.x, uLight.x, uv);",
      "  vec4 b = matterOf(uB, uFitB, gridOf(uCells.y, uFitB, aspect),",
      "                    uLevel.y, uDial.y, uSat.y, uLight.y, uv);",
      // THE ARRIVING WORK'S MATTER STANDS OVER THE DEPARTING WORK'S. Read the other way round an
      // arriving stratum would slide UNDER what is still standing and only appear as the departing
      // work cleared it, which is an arrival by uncovering — the fade this module exists to avoid,
      // read backwards. This way both motions are on screen the whole way.
      "  vec3 col = mix(a.rgb, b.rgb, b.a);",
      // THE COVERAGE LAW (§7). This instrument's own matter is the two works' strata, wherever they
      // have carried them; where neither has, it carries nothing, contributes nothing and hides
      // nothing, and the cue beneath is seen. At either door one work's two strata tile the frame
      // exactly — every point is at or above that work's level or below it, one or the other, and
      // neither has moved — so the alpha is 1 at every point and the door is one whole work.
      "  float cov = max(a.a, b.a);",
      // the judges' own frame: the two works' coverage as colour, so a check reads on the picture
      // which work claims a point and whether either alpha ever stands between 0 and 1
      "  col = mix(col, vec3(a.a, b.a, 0.0), uMask);",
      "  gl_FragColor = vec4(col, mix(cov, 1.0, uMask) * uPresence);",
      "}",
    ].join("\n");

    function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }

    // THE MASK GRID THE MODULE MEASURES ON, its own construction number: a connected area is at
    // least one cell, so the grid sets what counts as a piece rather than a speck, and 128 cells on
    // the long side is the scale at which a cell is under one percent of the frame
    // (strata-light.js:36-40). It is published as a handle here rather than pinned, because it is a
    // reading of the work — how fine the material of a photograph is — and the composer measures
    // exactly that. Its two ends are this port's own and are named in its report: below eight cells
    // a stratum is two or three blocks and the parting stops being the work's own, and past five
    // hundred a cell is finer than a point of the buffer on the frames this engine draws.
    var MASK_CELLS = 128, CELLS_MIN = 8, CELLS_MAX = 512;

    // HOW FAR A STRATUM TRAVELS, in frame heights. It is not a free number and it is not a taste: a
    // bright piece's own bottom edge and a dark piece's own top edge both lie inside the frame, so
    // one frame height is exactly the distance that carries every piece of a stratum wholly out, and
    // it is what makes the far door exact.
    var TRAVEL = 1.0;

    // THE MODULE'S OWN CEILING ON THE LIGHT VOICE (strata-light.js:305): the writing never passes
    // nine tenths, so the matter under it is never wholly lost to white or to black.
    var LIGHT_CEILING = 0.9;

    // THE RESPONSE CURVE (DARKROOM-DRAFT D2, his word of 2026-08-08 17:57), carried digit for digit
    // out of the module (strata-light.js:335-355). Equal movements of the hand produce equal felt
    // change. The raw travel runs downhill — 169 channels in the first tenth against 25 in the last
    // — because the bright stratum and the dark one leave together and the frame empties, so the
    // same step of the hand moves less and less as there is less left in the frame to move. The
    // family is a two-piece exponential hinged at the MEASURED median of the felt change: c = 0.37
    // is that median, and on each side of it the curve is the plain logarithm the other modules
    // carry with its two ends fixed by its own side. The port re-derives nothing.
    var FEEL_C = 0.37, FEEL_K1 = -0.2, FEEL_K2 = 2.2;
    function feelLog(x, k) {
      return Math.abs(k) < 1e-6 ? x : (Math.exp(k * x) - 1) / (Math.exp(k) - 1);
    }
    function feelOf(u) {
      return u <= 0.5 ? FEEL_C * feelLog(2 * u, FEEL_K1)
                      : FEEL_C + (1 - FEEL_C) * feelLog(2 * u - 1, FEEL_K2);
    }

    // A VOICE AT THIS DIAL, carried digit for digit (strata-light.js:283-291). One breath of a named
    // period and a named phase, held to nothing at BOTH doors by the window 4u(1 − u). The period is
    // read in the dial's own units, so a voice is the same voice whatever second the score walks the
    // handle over, and the phase is the head start the score gives it. A voice the score names no
    // period or no amplitude for is silent.
    //
    // THE WINDOW IS WHAT KEEPS THE DOORS THE DOORS, and this instrument's own door reading below is
    // held against exactly that: at either end of the hand the window is exactly zero, so a door is
    // exactly the picture the file carries and exactly the empty frame the arriving layer waits
    // behind, whatever numbers a score gives the two voices.
    function voiceAt(period, phase, amp, u) {
      var a = +amp, p = +period;
      if (!(a > 0) || !(p > 0)) return 0;
      return a * Math.sin(2 * Math.PI * (u / p + (+phase || 0))) * 4 * u * (1 - u);
    }

    // How much palette a work's matter holds at this dial: full, but for the colour voice's own
    // breath — there is no drain here to lead or follow, so the voice is the whole of the motion,
    // and clamped at 1 it is one-sided (strata-light.js:294-298).
    function satAt(v) { return clamp(1 + v, 0, 1); }

    // Cover-fit a work into the frame, with NO crop of its own. Nothing here is dragged outside the
    // picture — a stratum only translates, and a point that translates off the picture is a stratum
    // that has left rather than a sample to fetch — so the module's own framing is the plain cover
    // fit and `coverCrop` is 1 (lab/data/module-contract.json, this module's `dial.framing`).
    function fit(iw, ih, w, h) {
      var fa = w / Math.max(h, 1);
      var ia = iw / Math.max(ih, 1);
      var sx, sy;
      if (ia > fa) { sx = fa / ia; sy = 1; } else { sx = 1; sy = ia / fa; }
      return [sx, sy, 0, 0];
    }

    // ---- THE DOOR THE INSTRUMENT READS FOR ITSELF ------------------------------------------------
    // His 18:00 architecture decision, carried in the U27 brief: the instrument reads its doors at
    // runtime on the actual buffer, and the report it hands back is the runtime truth; what the
    // manifest declares is only the claim.
    //
    // WHAT A DOOR ASKS OF THIS INSTRUMENT, AND WHY THE GRID DECIDES NOTHING HERE. The meshing and
    // the material instruments read a MASK that crosses over inside a band whose width is set by the
    // buffer, so for them the grid is what decides a door. This instrument's mask crosses over
    // nowhere: a point is at or above a work's level or it is below it, and the strata are
    // translated by whole frame heights rather than blended. At the entry door the departing work's
    // dial is exactly 0, so both its strata stand where the file put them, every point of the frame
    // belongs to exactly one of them and the alpha is exactly 1 — on any buffer, at any cell count,
    // at any level. The arriving work's dial is exactly 1 there, so its bright stratum's source
    // stands a whole frame height below every point of the frame and its dark stratum's a whole
    // frame height above, and neither has anything to draw. The exit door says the same the other
    // way round. Neither reading has a width in it, so neither can be closed or opened by a grid.
    //
    // WHAT CAN STILL BREAK A DOOR, and it is the one thing this reading is for. The two accompanying
    // voices are written over the matter that stands, so a door is the file itself only while both
    // of the standing work's voices are exactly nothing there. They are — the window 4u(1 − u) is
    // exactly zero at both ends of the dial and the response curve lands exactly on 0 and on 1 — and
    // that is the claim this instrument makes to the composer. So this is what it reads, in its own
    // numbers, on the buffer it is about to draw: the two voices of the work whose door it is. A
    // reading that is not zero is a door carrying a breath of light or of colour that the file does
    // not, and the instrument refuses it with the reading in the refusal rather than drawing it.
    //
    // It refuses on no pose this file as written can produce, and that is said plainly rather than
    // hidden: it is a claim proved, not a range guarded. The suite's red-on-bug row takes the window
    // out of the voice and makes exactly this refusal fire.
    function doorGridOf(st) {
      var bw = Math.round(st.bufWidth), bh = Math.round(st.bufHeight);
      if (bw >= 1 && bh >= 1) return { w: bw, h: bh, drawn: true };
      return { w: Math.round(st.cssWidth), h: Math.round(st.cssHeight), drawn: false };
    }

    function doorReadOf(v, st) {
      var door = st.mix === 0 ? "in" : (st.mix === 1 ? "out" : null);
      if (door === null) return null;
      var g = doorGridOf(st);
      if (!(g.w >= 1) || !(g.h >= 1)) return null;
      // which of the two works this door stands the whole picture of: the departing one at the
      // entry door, the arriving one at the exit
      var i = door === "in" ? 0 : 1;
      return { grid: g, door: door, standing: i,
               dial: [v.dial[0], v.dial[1]],
               level: [v.level[0], v.level[1]],
               cells: [v.cells[0], v.cells[1]],
               colourVoice: [v.colourVoice[0], v.colourVoice[1]],
               lightVoice: [v.lightVoice[0], v.lightVoice[1]] };
    }

    // THE REFUSAL, worded the way the host's own manifest refusals read: what is wrong, in this
    // instrument's own measured numbers, on the grid it was measured on.
    function doorWhyNoOf(read) {
      if (!read) return null;
      var i = read.standing;
      var c = Math.abs(read.colourVoice[i]), l = Math.abs(read.lightVoice[i]);
      if (!(c > 0) && !(l > 0)) return null;
      var g = read.grid;
      return (read.door === "in" ? "the entry" : "the exit") + " door leaks: the "
           + (read.door === "in" ? "departing" : "arriving") + " work stands at a dial of "
           + read.dial[i] + " on a " + g.w + " x " + g.h + (g.drawn ? " buffer" : " frame")
           + ", where its own window holds both accompanying voices to nothing — and its colour "
           + "voice reads " + c.toFixed(6) + " and its light voice " + l.toFixed(6)
           + ", so the frame carries a breath of "
           + (c > 0 && l > 0 ? "colour and of light" : (c > 0 ? "colour" : "light"))
           + " the file itself does not, where this door's own law asks for the work exactly as the "
           + "file carries it";
    }

    // THE NUMBERS OF ONE FRAME. Everything the shader gets beyond the seating of the two works is a
    // pure function of the pose. The departing work's dial is the hand through the module's own
    // response curve and the arriving work's is the hand read backwards through the same curve, so
    // one pass carries the module twice and neither reading is a second curve.
    //
    // NOTHING HERE READS THE SECOND THE HOST HANDS DOWN, and that is the module's own law rather
    // than an omission: every position in it is a pure function of the dial, so a seam lands
    // wherever the dial says it does, at any second (strata-light.js:364-367). The `clock` handle is
    // published because the module accepts one and a score owns the clock everywhere; a run of this
    // instrument repeats to the pixel because there is nothing in it for a clock to move.
    function values(st) {
      var hand = clamp(st.mix, 0, 1);
      var dA = feelOf(hand), dB = feelOf(1 - hand);
      var cvA = voiceAt(st.colourPeriodA, st.colourPhaseA, st.colourAmpA, dA);
      var cvB = voiceAt(st.colourPeriodB, st.colourPhaseB, st.colourAmpB, dB);
      var lvA = voiceAt(st.lightPeriodA, st.lightPhaseA, st.lightAmpA, dA);
      var lvB = voiceAt(st.lightPeriodB, st.lightPhaseB, st.lightAmpB, dB);
      var v = {
        dial: [dA * TRAVEL, dB * TRAVEL],
        level: [clamp(+st.levelA, 0, 1), clamp(+st.levelB, 0, 1)],
        cells: [Math.max(CELLS_MIN, Math.min(CELLS_MAX, Math.round(+st.cellsA || MASK_CELLS))),
                Math.max(CELLS_MIN, Math.min(CELLS_MAX, Math.round(+st.cellsB || MASK_CELLS)))],
        sat: [satAt(cvA), satAt(cvB)],
        light: [clamp(lvA, -LIGHT_CEILING, LIGHT_CEILING),
                clamp(lvB, -LIGHT_CEILING, LIGHT_CEILING)],
        // read on the diagnostic surface, bound to no uniform: the two voices on their own, which is
        // the only part of the picture a judge can weigh against the voice the score declared — the
        // same two fields the module's own `reading()` publishes
        colourVoice: [cvA, cvB], lightVoice: [lvA, lvB], hand: hand,
      };
      var read = doorReadOf(v, st);
      v.doorGrid = read ? read.grid : null;
      v.doorStanding = read ? read.standing : null;
      v.doorWhyNo = doorWhyNoOf(read);
      return v;
    }

    var manifest = {
      id: "strata-light", api: 1, arity: 2,
      // The departing work comes apart into its two strata, the middle holds a frame neither work
      // has closed, and the arriving work's strata gather into it.
      roles: ["disassembly", "mystery", "assembly"],
      // CELL IS READ OFF THE MODULE'S OWN PUBLISHED ROW: `lab/data/module-contract.json` gives this
      // module `level: "CELL"`, and until the colour-and-light lane that was the whole of it — the
      // two accompanying voices carried no reading and so never actually moved anything, and a level
      // nothing moves on is not a level the instrument occupies.
      //
      // LIGHT-COLOUR IS ADDED because that stopped being true. Shelf 11: "Colour is an accompaniment
      // voice and counts in the budget." Shelf 17's levels law: "one active voice per structural
      // level ... LIGHT-COLOUR its own slot." Once the colour and light voices are driven off the
      // two works' own colour readings (pass-composer.js, the "strata-light" branch of `fillPlan`)
      // they act on LIGHT-COLOUR exactly the way grid-colour's own palette-and-light voices do
      // (pass-inst-grid-colour.js:806-816, which already carries this second level for the same
      // reason) — so a cue this instrument owns must be allowed to own LIGHT-COLOUR too, or the
      // composer's own level-ownership resolution (`ownTheLevels`) would never see that a second cue
      // could be singing there and two voices could land on one level silently, which is exactly what
      // the levels law forbids. `lab/data/module-contract.json` still carries only CELL — that file
      // is the module's own render-time contract and nothing in this lane touches it — so this is a
      // point where the engine's declared level set now says more than the lab's upstream row, and
      // the gap is named here rather than hidden.
      levels: ["CELL", "LIGHT-COLOUR"],
      // WHAT THIS INSTRUMENT CUTS ON. A stratum is a TONAL ZONE of the work — everything at or above
      // a level of its own light, and everything below it — which is the band kind. It is the very
      // decomposition the composer's own tonal-and-spectral pivot cuts on, and that pivot reads on
      // any two photographs by construction.
      cuts: ["band"],
      // WHERE THIS INSTRUMENT HAS A SEAM (§8's `seams` block, pass-layer.js). None is declared, and
      // the file's own construction argues it rather than an oversight leaving it out: "NO FADE
      // ANYWHERE. A point either carries a work's matter or it does not; the alpha this shader writes
      // is 1 or 0 and never anything between." The shader reads the tonal cut with a plain `<`/`>=`
      // against `uLevel` (`matterOf` above) and nothing softens the two sides of it into each other —
      // there is no smoothstep at the level, no crossfade where bright gives way to dark, because the
      // module this instrument carries is built to leave the frame rather than to dissolve across it.
      // What the boundary does cost is named already, in its own terms rather than as a seam: it steps
      // at the mask's own cell rather than at the pixel ("a cell whose centre is untypical of it falls
      // on the other side of the level from where the module puts it"), which is the cell grid's own
      // coarseness and not a line this manifest has softening for.
      seams: [],
      // The module declares NO slider-facing params at all (`params: []`,
      // lab/effects/strata-light.js:415): no page grows a control for it and every one of its
      // handles is a hidden one a score drives. That empty list is carried rather than filled in.
      params: {},
      // EVERY handle a score can drive (§4.4b). `mix` is the dial and `clock` is the second the host
      // hands down; the rest are the module's own hidden handles, published PER WORK because this
      // instrument plays the module twice and the lab's own assembler gives each layer its own
      // numbers (lab/step4-assembler.js, the accompanying voices).
      //
      //   · `levelA`/`levelB` — THE LEVEL EACH WORK PARTS AT, on its own luminance. The module
      //     publishes it through `measure(image)` at build time and measures its own picture where a
      //     score names none; this file may not read a picture, so it arrives as a handle instead.
      //     IT NO LONGER RESTS AT NOTHING. The composer's `fillPlan` ("strata-light" branch,
      //     HANDLE_SOURCE below carries both rows as "measured") drives it off the two works' own
      //     `luminance.level` — lab/analyze/recipes.py:551-613 colour_stats()'s python port of this
      //     module's own `measure(image)` — A the departing work's, B the arriving work's, exactly
      //     the number the module would have solved for itself where a score names none.
      //   · `cellsA`/`cellsB` — THE MASK GRID each work is read on, cells across its own long side.
      //     The module holds one number for both (`MASK_CELLS = 128`); a pair is two photographs
      //     with two materials, so it is published per work and rests at the module's own number.
      //   · the six voice fields, twice — `colourPeriod/Phase/Amp` and `lightPeriod/Phase/Amp` for
      //     each work. THEY NO LONGER REST AT NOTHING. The composer's `fillPlan` (its
      //     "strata-light" branch, HANDLE_SOURCE below carries the same twelve rows as "measured")
      //     drives all twelve off the two works' own colour readings, porting the derivation
      //     lab/step4-assembler.js:1966-2010 already worked out: A takes the departing work's own
      //     colour.sat and colour.contrast, B the arriving work's, each turned into a period through
      //     BEAT_DIAL and `spread` (step4-assembler.js:60-66, :1613-1636, ported into
      //     pass-composer.js as `voiceSpread`/`voicesAligned`), a phase a quarter turn from its
      //     neighbours (`i / 4`), and an amplitude VOICE_SHARE of the work's own measure
      //     (step4-assembler.js:91 — VOICE_SHARE is itself the assembler's own admitted number of
      //     taste, carried across as that admission rather than re-derived as a measurement).
      //     WHAT STAYS IN THE LAB: the assembler's own audibility loop that follows this first pass —
      //     `voiceMove`, `VOICE_TARGET` — renders a layer off-screen and measures how far it actually
      //     moved real pixels, muting a voice a work cannot sing loud enough to clear the visible
      //     threshold. The composer derives a crossing at the instant a visit casts it and cannot
      //     render a probe frame to measure against, so every voice here plays at its first-pass
      //     amplitude, unmuted, and that refinement is not ported.
      //     ALL TWELVE ARE DRIVEN ONLY WHERE THIS CUE OWNS LIGHT-COLOUR (shelf 17's levels law, the
      //     manifest's own `levels` entry above): a cue that merely accompanies another cue on that
      //     level leaves every one of the twelve unset and each rests at the manifest's own 0, which
      //     is the module's silence and not a second mechanism.
      //   · `mask` — the judges' channel, resting where the module has no such thing at all: at 0
      //     the picture, at 1 the two works' own coverage as colour.
      //
      // THREE FLEET HANDLES ARE ABSENT, and each absence is a fact about this module rather than an
      // oversight:
      //   · `seed` — nothing in this module is rolled. Its cut is the work's own luminance and its
      //     motion is a translation; there is no die to publish and inventing one would publish a
      //     handle that reaches nothing.
      //   · `shade` — the judge channel for a contact shadow. This module casts none: a stratum
      //     translates over the frame and nothing here lies on anything.
      //   · `travel` — how far the matter is carried. Here that distance is exactly one frame
      //     height, which is what makes the far door exact; a handle scaling it below one would
      //     leave the departing work standing in the frame at `mix` 1 and break the door this
      //     instrument's own coverage line claims.
      // LEVEL, PER SHELF 17 (docs/design/PASS-API-V1.md:716). `mix` is the crossing's own dial and
      // `clock` is the module's own time — neither is a structural level. `mask` is the judges'
      // channel, the same reason as every other instrument's own `mask`.
      handles: {
        mix: { min: 0, max: 1, def: 0, level: null },
        clock: { min: 0, max: 14, def: 0, level: null },
        levelA: { min: 0, max: 1, def: 0.5, level: "CELL" },
        levelB: { min: 0, max: 1, def: 0.5, level: "CELL" },
        cellsA: { min: CELLS_MIN, max: CELLS_MAX, def: MASK_CELLS,
                  applied: { roundedToWholeCells: true },
                  level: "CELL" },
        cellsB: { min: CELLS_MIN, max: CELLS_MAX, def: MASK_CELLS,
                  applied: { roundedToWholeCells: true },
                  level: "CELL" },
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
      // of its own, `sc = Math.max(W/iw, H/ih)` (lab/effects/strata-light.js build, and this
      // module's own `dial.framing` row in lab/data/module-contract.json).
      framings: { "0": { coverCrop: 1.0 }, "1": { coverCrop: 1.0 } },
      drivers: ["progress", "cueProgress", "time", "velocity", "capability", "noise", "static",
                "curve", "spline", "map", "add", "multiply", "mix", "clamp", "hold", "segment",
                "ramp", "slew", "oscillate", "node"],
      // The construction moves no point of view: it decides which stratum of which work owns each
      // point of the frame and translates the two works' strata inside it, so the witness camera
      // stays the stage's (§6).
      camera: { needs: "none", authority: "stage" },
      gl: { preserveDrawingBuffer: false },
      // WHAT THIS INSTRUMENT WRITES WHERE ITS OWN MATTER IS ABSENT (§7's coverage law, and the
      // per-instrument specification in docs/design/COVERAGE.md). Its absence is the place both
      // works' strata have left: the departing work's matter has travelled out of it and the
      // arriving work's has not yet reached it, and this instrument carries no picture of its own
      // for it — which is exactly the module's own door 1, «a layer invisible by geometry, never by
      // transparency». At both doors the standing work's two strata tile the frame, so the alpha is
      // 1 at every point and each door is one whole work, opaque throughout.
      coverage: {
        writes: true,
        how: "max of the two works' own coverage, each 1 where a stratum of that work has carried "
             + "matter to this point and 0 where neither of its strata has",
      },
      // The neutral pose is the ENTRY DOOR — `mix` at 0, the value the `doors` block above names —
      // so the frame keys the host reads off it at registration include the door's own record.
      neutralPose: { mix: 0, clock: 0, levelA: 0.5, levelB: 0.5,
                     cellsA: MASK_CELLS, cellsB: MASK_CELLS,
                     colourPeriodA: 0, colourPhaseA: 0, colourAmpA: 0,
                     lightPeriodA: 0, lightPhaseA: 0, lightAmpA: 0,
                     colourPeriodB: 0, colourPhaseB: 0, colourAmpB: 0,
                     lightPeriodB: 0, lightPhaseB: 0, lightAmpB: 0,
                     mask: 0, presence: 1, reduced: false, cssWidth: 1000, cssHeight: 1000 },
      passes: [{
        program: "strata-light", vert: VERT, frag: FRAG, position: "aPos",
        uniforms: [
          { name: "uPresence", type: "float", source: "handle:presence" },
          { name: "uA", type: "sampler2D", source: "textureA" },
          { name: "uB", type: "sampler2D", source: "textureB" },
          { name: "uFitA", type: "vec4", source: "fitA" },
          { name: "uFitB", type: "vec4", source: "fitB" },
          { name: "uRes", type: "vec2", source: "resolution" },
          { name: "uDial", type: "vec2", source: "frame:dial" },
          { name: "uLevel", type: "vec2", source: "frame:level" },
          { name: "uCells", type: "vec2", source: "frame:cells" },
          { name: "uSat", type: "vec2", source: "frame:sat" },
          { name: "uLight", type: "vec2", source: "frame:light" },
          { name: "uMask", type: "float", source: "handle:mask" },
        ],
      }],
      // The instrument allocates nothing of its own: it spends the two source-texture slots the host
      // already holds and the one programme the host builds from this manifest. The module's own
      // canvases — the standing picture, its grey twin and two per travelling piece — are the
      // textures this port does not ask for: the twin is the luminance of the very fragment already
      // fetched, and the pieces are the inverse map itself.
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
                   programs: 1, passes: 1, bytesEstimate: 2000088, variant: "lean" },
                   standard: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0,
                               programs: 1, passes: 1, bytesEstimate: 8000088,
                               variant: "standard" },
                   rich: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                           passes: 1, bytesEstimate: 32000088, variant: "rich" } },
      capabilities: ["webgl2"],
      decline: ["one work only", "a source that never decoded"],
      provenance: { labPath: "lab/effects/strata-light.js", commit: "468f491",
                    sha256: "c12288a97465d59452db742daffc663e7e84ef9b2d14dadb0869b6789d7a1a19" },
      // HOW WELL THIS INSTRUMENT SUITS A PAIR (2026-08-18, his word of 09:51 and its sharpening at
      // 09:53). An instrument no longer answers WHETHER it takes a pair — it answers how well it
      // suits one, so a poor fit is still playable and still explains itself. The arithmetic runs in
      // the composer, which is the one place holding both records; what stands here is the
      // instrument's own statement of WHAT IT READS, which is the fact this file owns. A fit of
      // nothing is never a refusal — it ranks last and plays where nothing ranks higher.
      suits: { reads: ["luminance.level"],
               how: "each work parts at a level of its own light, so what would suit it best is a "
                  + "pair standing far apart in TONE. `luminance.level` (the judge seat's standing "
                  + "correction of 2026-08-18/19) is that genuine reading, the median of each "
                  + "work's own luminance, and this fit now ranks a pair by the distance between "
                  + "their two levels — the very decomposition the composer's own tonal-and-"
                  + "spectral pivot cuts on" },
      readiness: "production-ready",
    };

    var live = false;
    return {
      name: "strata-light",
      manifest: manifest,
      values: values,
      fit: fit,
      feel: feelOf,
      voice: voiceAt,
      prepare: function (o) {
        if (!o.sources) return { take: false, why: "the parting-by-light instrument needs both works" };
        if (!o.cue) return { take: false, why: "no cue names it" };
        return { take: true };
      },
      start: function () { live = true; },
      // The pose the shader draws. Every number in it comes from a handle a score can drive, and
      // nothing in it reads a clock, so a run of one score repeats to the pixel.
      //
      // THE REDRAW THE PRESERVED BUFFER STOOD IN FOR. The module draws on demand — from onParam,
      // from resize — and between two such draws the browser hands back the frame that was already
      // there. The host draws every frame of a running transaction and redraws on every resize, so
      // the frame the compositor shows is one this instrument drew for it.
      //
      // A DOOR THIS INSTRUMENT CANNOT KEEP WHOLE IS REFUSED RATHER THAN DRAWN. The door law is the
      // instrument's own claim (the manifest's coverage line above), so the instrument is what
      // answers for it: at either door it reads its own two voices on the buffer the host is about
      // to bind and, where the standing work's voices are not exactly nothing there, hands the host
      // the reason with the readings in it instead of drawing a door that carries a breath the file
      // does not. The host recovers the transaction on that reason and the walk's own glide carries
      // the visitor, which is the product's own behaviour with no renderer.
      frame: function (st) {
        if (!live) return;
        var h = st.handles;
        var pose = {
          mix: h.mix, mask: h.mask,
          levelA: h.levelA, levelB: h.levelB, cellsA: h.cellsA, cellsB: h.cellsB,
          colourPeriodA: h.colourPeriodA, colourPhaseA: h.colourPhaseA, colourAmpA: h.colourAmpA,
          lightPeriodA: h.lightPeriodA, lightPhaseA: h.lightPhaseA, lightAmpA: h.lightAmpA,
          colourPeriodB: h.colourPeriodB, colourPhaseB: h.colourPhaseB, colourAmpB: h.colourAmpB,
          lightPeriodB: h.lightPeriodB, lightPhaseB: h.lightPhaseB, lightAmpB: h.lightAmpB,
          presence: h.presence,
          t: h.clock, reduced: st.reduced,
          cssWidth: st.viewport.w, cssHeight: st.viewport.h,
          // THE GRID THE SHADER WILL SAMPLE ON, carried into the pose so the door is read on the
          // buffer the host is about to bind as `uRes` rather than on the CSS frame around it.
          bufWidth: st.viewport.bufferW, bufHeight: st.viewport.bufferH,
        };
        // AT A DOOR THE INSTRUMENT SAYS WHAT IT APPLIED, and says it before it refuses. Nothing is
        // ever walked back here — no grid decides this instrument's doors — so the request and the
        // applied state are one and the same, and what the record carries is the state itself: the
        // two dials, the two levels, the two cell counts and the two voices of the work whose door
        // it is.
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
              reads: "the standing work's own two voices",
              request: [v.colourVoice[i], v.lightVoice[i]],
              applied: [v.colourVoice[i], v.lightVoice[i]],
              moved: 0, unit: "of the voice's own amplitude",
              standing: [v.dial[i], v.level[i], v.cells[i]],
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
    instrument: strataLightInstrument(),
  });
})();
