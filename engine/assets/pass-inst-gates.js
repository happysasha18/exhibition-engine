/*!pass-inst-gates.js*/
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

  var TAU = Math.PI * 2;

  // ================================================================================================
  // THE GATE INSTRUMENT (§8) — lab/effects/gates.js carried across
  // ================================================================================================
  // WHAT THE VISITOR SEES. Two masses of the departing work stand facing each other across a slot of
  // emptiness. The slot parts. What stands behind it is already the arriving work — alive from the
  // first crack of the opening and never faded in — squeezed toward the slot it comes through and
  // opening out to its own frame as the gate opens, while the two masses travel out of the frame.
  // Where the slot stands upright the gates open sideways; where it lies across they part up and
  // down. While the opening is still narrower than the slot's own emptiness the two leaves part
  // along a straight edge; once the opening reaches the masses the jamb breaks into teeth and the
  // matter tears unevenly, so a work with a wide gate parts quietly for a long while and one with a
  // narrow gate starts tearing at once.
  //
  // THE LEVEL, READ OFF THE MODULE'S OWN HEADER AND SAID TO BE DERIVED. Neither
  // `lab/data/module-contract.json` nor `module-contract-new.json` carries a `gates` row — the ten
  // and eleven modules they hold are other modules — so no level is published for this one anywhere
  // and the two below are read out of the module's own text, at the lines named:
  //   · CELL — the motion is two whole pieces of the frame moving as pieces. «two masses facing each
  //     other across a slot of emptiness» (gates.js:2) and «THE LEAVES. Each is a rigid half of the
  //     departing work sliding out of the frame» (gates.js:176-177). The frame changes hands OUTWARD
  //     from the slot (gates.js:72-73), which is a cut of the frame into panels and their travel.
  //   · CELL CONTENT — the content INSIDE each piece moves in its own right, on both sides of the
  //     cut. «`uSwing` turns the flat slide into a door turning on that hinge — a plain
  //     one-dimensional projective warp» (gates.js:178-180), and the arriving work «stands squeezed
  //     toward the slot it comes through and opens out to its own frame» (gates.js:192-194).
  // SURFACE is NOT claimed. One carrier field decides which work a point shows (gates.js:68-70), but
  // nothing here runs a motion over the whole picture plane: away from the two edges the field is
  // saturated and the picture is one work or the other, undisturbed.
  //
  // What came over: the shader character for character, the seating of a work in the frame
  // (coverFit), the measured response curve with its dead bands, the module's own constants, and the
  // numbers of one frame (frameValues). What stayed behind: its own canvas, its own WebGL 1 context,
  // its own frame loop, its resize observer, its own accumulated clock, and the whole build-time
  // measuring instrument described below.
  //
  // ------------------------------------------------------------------------------------------------
  // THE SLOT'S PLACE AND WIDTH, AND WHY THEY ARRIVE AS HANDLES
  // ------------------------------------------------------------------------------------------------
  // The lab module measures the source it was actually given. `gateOf` (gates.js:398-409) opens the
  // departing photograph, draws it into a canvas of its own at 512 on the longest side, reads the
  // pixels back, builds the collection's own busy field out of them — CIELAB lightness, a Sobel
  // gradient over 3.0 lightness units per pixel, box-filtered over a sixteenth of the read — and
  // walks a band across each axis to find where the emptiness between two masses stands and how wide
  // it is. §1.2 puts every one of those steps outside this file: an instrument here may not create a
  // canvas, may not touch the DOM and may not read a picture's pixels.
  //
  // SO THE READING ARRIVES AS HANDLES A SCORE DRIVES, which is the road the drifting instrument
  // already took for exactly this problem (pass-inst-adrift.js, «THE FOURTEEN THAT CARRY THE PAIR'S
  // OWN MEASUREMENTS»: fourteen numbers the module solved off the two files at build, published as
  // handles resting at the module's own naive reading). Three handles carry it here — `slotAxis`,
  // `slotPlace` and `slotHalf` — and they rest at the module's own `none` reading (gates.js:399-400):
  // upright, the middle of the frame, and half the motif's own band of 0.16. That is the reading the
  // module itself falls back to when a source carries no gate, and it is the band step1-motifs.py
  // pins for the whole collection, so a pair whose record says nothing about a gate gets exactly the
  // picture the module gives such a pair.
  //
  // THE MODULE'S OWN DOOR FOR THIS IS THE ONE BEING USED. gates.js:488-503 already takes `slot`,
  // `slotAxis` and `slotHalf` from the score «which is how the engine hands in a row it already
  // has», and measures only where none is handed. This port is that branch and only that branch.
  //
  // AND THE FLOOR STAYED BEHIND WITH THE INSTRUMENT. `GATE_FLOOR` (gates.js:273) is the collection's
  // quarter rule, and it belongs to the measuring walk that decides whether a source has a gate at
  // all. That walk is not here, so its floor is not here either: no reading of a pair can make this
  // instrument refuse a crossing, and `suits` below ranks and never admits.
  //
  // ------------------------------------------------------------------------------------------------
  // WHAT THE SEATING DOES TO THE SLOT
  // ------------------------------------------------------------------------------------------------
  // The slot's place and width are places in the FILE, and the file is cover-fitted into the frame
  // and pulled in by ZOOM before it reaches the frame. The module carries both through that same fit
  // (gates.js:514-521) rather than assuming they survive it. Here the fit is the HOST'S: since
  // 2026-08-17 the frame state hands both works' seating on the very buffer the host is about to bind
  // (`fitA`/`fitB`, computed by the same function the draw calls), so the script and the shader work
  // from ONE seating rather than two guesses at one. Where none arrives — a bench posing this
  // instrument by hand — the plain cover fit of the sizes the pose carries stands instead, which is
  // the road `pass-inst-hero.js` already takes.
  //
  // THE PRESERVED DRAWING BUFFER. The module asks its own context for one (gates.js:469) and §7
  // refuses it. The flag stood in for a redraw: the module draws on demand — from onParam, from
  // resize — and under reduced motion it drew once and stopped. The host draws every frame of a
  // running transaction and redraws on every resize, so the frame the compositor shows is one this
  // instrument drew for it. Reduced motion stops the arriving work's drift inside `values` and stops
  // nothing else.
  function gatesInstrument() {
    var VERT = [
      "attribute vec2 aPos;",
      "varying vec2 vUv;",
      "void main(){ vUv = vec2(aPos.x * 0.5 + 0.5, 0.5 - aPos.y * 0.5); gl_Position = vec4(aPos, 0.0, 1.0); }",
    ].join("\n");

    // THE MODULE'S OWN SHADER, CHARACTER FOR CHARACTER BUT FOR TWO ADDED LINES. Not one line of the
    // module's own moved — not even the one line every other port in this farm had to rewrite. The
    // lab modules compute the frame's aspect from the drawing buffer they own and an instrument has
    // to derive it from the size the host binds; this shader never reads an aspect at all, because it
    // works in the frame's own uv from end to end, and the module hands its own buffer's size in as
    // `uRes` which is exactly what the host binds under the name `resolution`.
    //
    // THE TWO LINES THAT ARE ADDED, named the way the beat instrument names its own:
    //   1. `uniform float uMask;` — the fleet's judges' channel, published by thirteen instruments
    //      before this one.
    //   2. `col = mix(col, vec3(covL, covR, 0.0), uMask);` — the one line that reads it. It paints
    //      THIS INSTRUMENT'S OWN CUT in place of the picture: red where the leaf that opens toward
    //      the low end of the gate's axis stands, green where the other one stands, and black over
    //      the opening the arriving work comes through. So a law about the cut — that the two leaves
    //      never overlap, that the opening is exactly what they have given up — can be measured ON
    //      THE PICTURE rather than taken on this file's word. It rests at 0, where
    //      `mix(col, ·, 0.0)` is `col` exactly, so a score that never names the channel draws the
    //      module's own frame to the bit.
    var FRAG = [
      "precision highp float;",
      "varying vec2 vUv;",
      "uniform sampler2D uA;",
      "uniform sampler2D uB;",
      "uniform vec4 uFitA;",        // xy = scale into image uv, zw = pan
      "uniform vec4 uFitB;",
      "uniform vec2 uRes;",         // device pixels
      "uniform float uVert;",       // 1 the slot stands upright, 0 it lies across
      "uniform float uSlot;",       // where the slot stands along the gate's axis, frame units
      "uniform vec2 uOpen;",        // how far each leaf has parted from the slot, frame units
      "uniform float uBite;",       // how deep the teeth bite, as a share of a leaf's own opening
      "uniform float uTeeth;",      // how many teeth stand along the slot
      "uniform float uSeed;",
      "uniform float uSwing;",      // the leaves' projective turn, 0 = a flat slide
      "uniform float uPress;",      // the second work's squeeze into the slot
      "uniform float uDrift;",      // its slow travel along the slot, on the handed second
      "uniform float uGuard;",      // the contact shadow's gate: nothing at either door
      "uniform float uMask;",       // the judges' channel: this instrument's own cut as colour

      // Every sample is a frame coordinate pushed by at most the squeeze and the drift, and the
      // cover-fit was pulled in by exactly that much (ZOOM in the script below), so a push always
      // lands on picture. The clamp is the backstop; half a texel of inset keeps the linear filter
      // off the border (weave.js:39-41).
      "vec2 into(vec2 p, vec4 f){",
      "  return clamp((p - 0.5) * f.xy + 0.5 + f.zw, 0.0008, 0.9992);",
      "}",
      "vec3 texA(vec2 p){ return texture2D(uA, into(p, uFitA)).rgb; }",
      "vec3 texB(vec2 p){ return texture2D(uB, into(p, uFitB)).rgb; }",

      "float hash11(float n){ return fract(sin(n * 127.1) * 43758.5453); }",

      // the frame point rebuilt out of the gate's own two coordinates: `a` runs ACROSS the gate,
      // `b` runs ALONG the slot
      "vec2 uvOf(float a, float b){ return mix(vec2(b, a), vec2(a, b), uVert); }",

      // WHICH TOOTH THIS POINT STANDS ON, and how much wider that tooth stands open than its
      // neighbours: six parts the tooth's own place along the slot, four parts the score's die.
      "float toothOpen(float b){",
      "  float tn = max(uTeeth, 1.0);",
      "  float j = floor(b * tn);",
      "  float rung = (j + 0.5) / tn;",
      "  float ord = mix(rung, hash11(j + uSeed), 0.4);",
      "  return 1.0 + uBite * (2.0 * ord - 1.0);",
      "}",

      "void main(){",
      "  vec2 uv = vUv;",
      "  float a = mix(uv.y, uv.x, uVert);",
      "  float b = mix(uv.x, uv.y, uVert);",
      "  float resA = mix(uRes.y, uRes.x, uVert);",
      "  float resB = mix(uRes.x, uRes.y, uVert);",
      "  float hA = 1.0 / max(resA, 1.0);",
      "  float hB = 1.0 / max(resB, 1.0);",

      // COVERAGE OVER THE PIXEL'S OWN FOOTPRINT. Across the gate the edge is a straight line and the
      // signed distance in pixels is exact; along the slot a tooth's step is filtered by three taps
      // over the pixel's own height, so a step never lands as a hard stair.
      "  float covL = 0.0, covR = 0.0;",
      "  float eL = uSlot, eR = uSlot;",
      "  for (int k = -1; k <= 1; k++) {",
      "    float bb = b + float(k) * hB * 0.5;",
      "    float m = toothOpen(bb);",
      "    float l = uSlot - uOpen.x * m;",
      "    float r = uSlot + uOpen.y * m;",
      "    covL += clamp(0.5 + (l - a) / hA, 0.0, 1.0);",
      "    covR += clamp(0.5 + (a - r) / hA, 0.0, 1.0);",
      "    if (k == 0) { eL = l; eR = r; }",
      "  }",
      "  covL /= 3.0; covR /= 3.0;",
      "  float cov = clamp(covL + covR, 0.0, 1.0);",

      // THE LEAVES. Each is a rigid half of the departing work sliding out of the frame: the left
      // leaf's own free edge always shows the material standing at the slot, and its hinge stands at
      // the frame's edge. `uSwing` turns the flat slide into a door turning on that hinge — a plain
      // one-dimensional projective warp, identity at zero, both ends of the leaf pinned — so the
      // leaf keeps covering exactly what it covered and no hole can open behind it.
      "  float oL = uSlot - eL, oR = eR - uSlot;",
      "  float k1 = uSwing;",
      "  float xiL = clamp(a / max(eL, 1e-5), 0.0, 1.0);",
      "  xiL = xiL * (1.0 + k1) / (1.0 + k1 * xiL);",
      "  float matL = oL + xiL * (uSlot - oL);",
      "  float xiR = clamp((1.0 - a) / max(1.0 - eR, 1e-5), 0.0, 1.0);",
      "  xiR = xiR * (1.0 + k1) / (1.0 + k1 * xiR);",
      "  float matR = (1.0 - oR) + xiR * (uSlot - 1.0 + oR);",
      "  vec3 leaf = covL >= covR ? texA(uvOf(matL, b)) : texA(uvOf(matR, b));",

      // THE SECOND WORK, standing behind the gate from the first crack of it. Its content travels
      // INWARD while the leaves travel outward: it stands squeezed toward the slot it comes through
      // and opens out to its own frame exactly at the door. The drift carries it slowly along the
      // slot on the handed second, and is nothing at both doors.
      "  float aB = uSlot + (a - uSlot) * (1.0 + uPress);",
      "  vec3 colB = texB(uvOf(aB, b + uDrift));",

      "  vec3 col = mix(colB, leaf, cov);",

      // THE CONTACT SHADOW: the leaf lies on top, and the opening takes a shadow from its edge,
      // decaying into the opening. Read in pixels, so it is the same physical edge at any size.
      "  float d = max(eL - a, a - eR) / hA;",
      "  float into2 = max(-d, 0.0);",
      "  col *= 1.0 - 0.34 * uGuard * (1.0 - cov) * exp(-into2 / 14.0);",

      // THE JUDGES' CHANNEL, the fleet's own and the second of the two lines this port adds: the cut
      // itself in place of the picture, so a law about the two leaves is measured on the frame rather
      // than taken on this file's word. Red is the leaf opening toward the low end of the gate's
      // axis, green the other, black the opening between them. It writes no blue, which is what tells
      // a judge the frame it is reading is the cut map and not the photographs.
      "  col = mix(col, vec3(covL, covR, 0.0), uMask);",

      // THE COVERAGE LAW (§7). This instrument's own matter is the WHOLE FRAME: `cov` decides which
      // of the two works a point shows, and both branches are picture. No point of the frame is left
      // unclaimed, so the alpha is the constant 1 and the manifest's `coverage.writes` is false —
      // which is the module's own first law, «COVERAGE, NEVER TRANSPARENCY … No alpha is ever
      // written but 1» (gates.js:48-55).
      "  gl_FragColor = vec4(col, 1.0);",
      "}",
    ].join("\n");

    function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
    function smoothstep(a, b, x) {
      var t = (x - a) / (b - a);
      t = t < 0 ? 0 : t > 1 ? 1 : t;
      return t * t * (3 - 2 * t);
    }

    // HOW FAR THE SECOND WORK IS SQUEEZED INTO THE SLOT, in frame units, and the crop that pays for
    // it. Every sample is a frame coordinate pushed by at most PRESS_MAX across the gate and
    // DRIFT_MAX along the slot, so the cover-fit is pulled in by that much at each end and ZOOM
    // follows from them rather than being a number of its own (gates.js:417-419).
    var PRESS_MAX = 0.12;
    var DRIFT_MAX = 0.03;
    var ZOOM = 1 + 2 * PRESS_MAX + 0.03;

    // THE MOTIF'S OWN BAND, and the bounds a slot's width is held inside — the three numbers of the
    // measuring walk that the module's own naive reading still stands on (gates.js:268, :278). The
    // band is the collection's central 0.42 to 0.58, said as a width; the bounds are the module's.
    var MOTIF_BAND = 0.16;
    var SLOT_MIN = 0.02, SLOT_MAX = 0.30;
    // and where a slot may stand along its axis, both as the module clamps a score's own number
    // (gates.js:496) and as it clamps the place once seated in the frame (gates.js:518)
    var SLOT_AT_MIN = 0.02, SLOT_AT_MAX = 0.98;
    var SEATED_MIN = 0.06, SEATED_MAX = 0.94;

    // ================================================================================================
    // THE PINNED NUMBERS, SWEPT — his 15:13 word on static parameters, and his 19:13 and 19:21 words
    // making the derivation the law: a number a work record could have set is a parameter and belongs
    // on a handle; a number no measurement can reach stays pinned and is NAMED rather than left to
    // look like a decision nobody made. This is that sweep, written down so it is not redone.
    //
    // WHAT WAS CONVERTED: nothing, and the reason is that this port's central decision converted it
    // all already. Exactly three numbers of this instrument are things a record could honestly
    // speak about — WHERE the departing work's slot stands, HOW WIDE it is, and WHICH AXIS it runs
    // on — and all three are published handles (`slotPlace`, `slotHalf`, `slotAxis`), resting at the
    // module's own naive reading. There is no fourth, and the rest of this note says why for each.
    //
    // WHAT IS A RANGE RATHER THAN A PINNED NUMBER, so it is not on the list at all:
    //   · `MOTIF_BAND` reaches the picture at ONE place — `slotHalf`'s published default. A default
    //     is what stands where nothing was measured, which is its whole job; a record cannot set it
    //     because the case it answers is the record saying nothing.
    //   · `SLOT_AT_MIN`/`SLOT_AT_MAX` are the declared min and max of `slotPlace`, and `SLOT_MIN`/
    //     `SLOT_MAX` the declared min and max of `slotHalf`. A published range is what a record sets
    //     a value INSIDE of.
    //
    // WHAT IS PINNED, WHAT IT DOES, AND WHY NO MEASUREMENT REACHES IT:
    //   · SEATED_MIN / SEATED_MAX (0.06, 0.94) — a SECOND clamp, on the slot's place AFTER the host's
    //     fit has carried it from the file into the frame. It is the one pinned number here most able
    //     to move a picture the record asked for: the fit magnifies distance from the middle, so a
    //     slot standing well off centre in the file can seat outside the frame, and this is what keeps
    //     a leaf from having no width at all. No reading says how near an edge a slot may stand.
    //   · SLOT_MAX (0.30) — the same shape, on the WIDTH after the fit. A wide slot seated at a tight
    //     fit is capped here, and the teeth then begin to bite earlier than the work's own gate says.
    //     CONSIDERED AND REJECTED: driving it from the departing work's `voidShare`. Void share is how
    //     much of the WHOLE FRAME is open ground; a slot width is the extent of ONE BAND of it, and
    //     the module's own header is explicit that the two readings come apart — the collection's gate
    //     measure divided by the denser flank «and 24 works that carry no gate at all did exactly
    //     that» (gates.js:32-39), which is the confusion the `facing` term was added to fix. Using
    //     void share here would re-make it.
    //   · SLOT_MIN (0.02) as that same second clamp CANNOT BIND, and is carried anyway. The seating
    //     scale is a cover fit divided by ZOOM, so it is always below 1 and the fit can only WIDEN a
    //     seated slot; the handle's own floor is already 0.02. It is kept because it is the module's
    //     own line (gates.js:519) and diverging from the module to delete a line that decides nothing
    //     buys nothing — but it decides nothing, and that is said here rather than left to be found.
    //   · PRESS_MAX (0.12) and DRIFT_MAX (0.03) — the full scale of the squeeze and of the drift, in
    //     frame units, and what ZOOM is derived from, so neither can move without moving the crop both
    //     doors are framed by. `press` is the published handle over the first. No reading in a work
    //     record is a displacement in frame units.
    //   · The 0.02 in `reach` — how far past the frame's edge a leaf must travel to clear it. The exit
    //     door's exactness rests on it being above zero (see the door reading below). No measurement.
    //   · `smoothstep(1, 0.85, d)` on the bite, and 1.8 on the swing — where the teeth close as the
    //     dial ends, and the swing handle's full scale in warp units. Both are shapes in DIAL space,
    //     which is the passage's own axis and not either photograph's.
    //   · The 9 in the drift's `sin(TAU · t / 9)` — the only temporal number in this file, the drift's
    //     period in seconds. The whole `measuredParts` vocabulary is spatial — pixels, shares, counts,
    //     angles — and carries no period in seconds for anything to read.
    //   · In the shader, carried character for character: 0.34 the contact shadow's depth (the `shade`
    //     handle is published over it), 14.0 its reach in points, and the 0.4 of «six parts the
    //     tooth's own place along the slot, four parts the score's die». That last is the fleet's own
    //     shared law carried from weave (gates.js:71-76) rather than a per-pair number, and it lives
    //     in the shader, so publishing it would both add a uniform and end the character-for-character
    //     carry that this port's own row proves.
    // ================================================================================================

    // THE RESPONSE CURVE, MEASURED AND NOT NAMED, carried over digit for digit (gates.js:543-546).
    // How far the picture moves per unit of the raw handle was measured with the curve taken out of
    // the module, that rate integrated, and this is the inverse of the integral at twenty-one evenly
    // spaced shares (how it is read BETWEEN two of them is the block below, and it is the port's
    // own answer, not the module's). The DEAD BANDS of 0.055 at either end are what
    // hold a whole picture whole: the dial stands at exactly 0 across the first band and at exactly 1
    // across the last, so a door is a door to the pixel.
    var FEEL_D0 = 0.055;
    var FEEL_Q = [0, 0.0261, 0.0525, 0.0792, 0.1064, 0.1341, 0.1631, 0.1947, 0.2286, 0.2648,
                  0.3029, 0.3408, 0.3813, 0.425, 0.4732, 0.5261, 0.5854, 0.6535, 0.7377, 0.8523,
                  1];

    // HOW THOSE TWENTY-ONE SHARES ARE READ BETWEEN THEIR OWN POINTS (S-20, 2026-08-28). Not one of
    // the numbers above moves here. What changed is the line drawn BETWEEN two of them.
    //
    // WHAT WAS WRONG WITH STRAIGHT LINES. The curve's own VALUE was right at every knot and its
    // SPEED was a staircase: constant inside each share, and stepping at each of the nineteen joins
    // between them. On this table the worst of those joins is the second to last, where the dial
    // went from 1.892 of its own travel a unit of the hand to 2.575 in one instant — a third again
    // as fast, with nothing between the two speeds. The same step stood at the dead band's own edge:
    // the dial is held perfectly still across the first FEEL_D0 of the hand and then left at 0.587 a
    // unit at once. Neither step is in the measurement. What was integrated to build this table is a
    // smooth reading of how far the picture travels, and a polyline through its samples invents
    // corners the reading never had.
    //
    // THE SHAPE IS THE HOST'S OWN, and it is the same repair one layer down. `pass-layer.js`'s
    // `splineSlopes`/`splineAt` — Fritsch–Carlson, carried over unchanged — is what his word of
    // 2026-08-11 put on every score track after he judged speed steps at segment joints; a response
    // curve read as twenty separate lines is that same defect inside one handle. One curve through
    // all twenty-one points passes through every knot exactly, cannot overshoot or turn back (so the
    // curve stays monotone and both doors stand exactly where they stood), and rests at both its own
    // ends — so it leaves the dead band at rest instead of at a run, for the reason the host's own
    // note gives for its zero end tangents: the value is HELD either side, and a track rests where it
    // is held.
    var FEEL_M = (function (q) {
      var n = q.length, h = 1 / (n - 1), d = [], m = [], i, a, b, s;
      for (i = 0; i < n - 1; i++) d.push((q[i + 1] - q[i]) / h);
      for (i = 0; i < n; i++) m.push(i === 0 || i === n - 1 ? 0 : (d[i - 1] + d[i]) / 2);
      for (i = 0; i < n - 1; i++) {
        if (d[i] === 0) { m[i] = 0; m[i + 1] = 0; continue; }
        a = m[i] / d[i]; b = m[i + 1] / d[i];
        if (a < 0) { a = 0; m[i] = 0; }
        if (b < 0) { b = 0; m[i + 1] = 0; }
        s = a * a + b * b;
        if (s > 9) { s = 3 / Math.sqrt(s); m[i] = s * a * d[i]; m[i + 1] = s * b * d[i]; }
      }
      return m;
    }(FEEL_Q));
    function feelOf(u) {
      var x = clamp((u - FEEL_D0) / (1 - 2 * FEEL_D0), 0, 1);
      var n = FEEL_Q.length, h = 1 / (n - 1);
      var i = Math.min(n - 2, Math.floor(x * (n - 1)));
      var s = (x - i * h) / h, s2 = s * s, s3 = s2 * s;
      return (2 * s3 - 3 * s2 + 1) * FEEL_Q[i] + (s3 - 2 * s2 + s) * h * FEEL_M[i]
           + (3 * s2 - 2 * s3) * FEEL_Q[i + 1] + (s3 - s2) * h * FEEL_M[i + 1];
    }

    // cover-fit a work into the frame, then pull in by the squeeze's own headroom. The host hands the
    // source's own dimensions, so the instrument never touches an image object.
    function fit(iw, ih, w, h) {
      var fa = w / Math.max(h, 1);
      var ia = iw / Math.max(ih, 1);
      var sx, sy;
      if (ia > fa) { sx = fa / ia; sy = 1; } else { sx = 1; sy = ia / fa; }
      return [sx / ZOOM, sy / ZOOM, 0, 0];
    }

    // WHERE THE SLOT STANDS IN THE FRAME (gates.js:514-521). The slot is a place in the FILE; the
    // file is cover-fitted and pulled in by ZOOM before it reaches the frame, so the place and the
    // width are carried through that same fit rather than assumed to survive it. `k` is the seating's
    // own scale along the gate's axis — the x scale where the slot stands upright, the y scale where
    // it lies across — which is exactly the module's `g.vertical ? fit[0] : fit[1]`.
    function seatOf(st, vert) {
      var f = st.fitA || fit(st.aw || 1, st.ah || 1,
                             st.cssWidth || 1, st.cssHeight || 1);
      var k = vert ? f[0] : f[1];
      var place = clamp(typeof st.slotPlace === "number" ? st.slotPlace : 0.5,
                        SLOT_AT_MIN, SLOT_AT_MAX);
      var half = clamp(typeof st.slotHalf === "number" ? st.slotHalf : MOTIF_BAND / 2,
                       SLOT_MIN, SLOT_MAX);
      return {
        inFile: place, halfInFile: half, seating: k,
        place: clamp((place - 0.5) / Math.max(k, 1e-4) + 0.5, SEATED_MIN, SEATED_MAX),
        half: clamp(half / Math.max(k, 1e-4), SLOT_MIN, SLOT_MAX),
      };
    }

    // THE NUMBERS OF ONE FRAME (gates.js:554-580). Everything the shader gets beyond the seating of
    // the two works is a pure function of the pose. The module's `judge.travel` and `judge.shade` are
    // the `travel` and `shade` handles here, resting where the module rests them; its `judge.slot` is
    // not a channel at all here, because putting the gate back in the middle of the frame is what the
    // three slot handles already do when they stand at their own defaults.
    function posed(st) {
      var d = typeof st.dial === "number" ? clamp(st.dial, 0, 1)
                                          : feelOf(clamp(Number(st.mix) || 0, 0, 1));
      var vert = (typeof st.slotAxis === "number" ? st.slotAxis : 1) >= 0.5;
      var f = seatOf(st, vert);
      // HOW FAR EACH LEAF HAS TO GO TO CLEAR THE FRAME, from the slot's own place. Both leaves reach
      // it at the far door exactly, whatever the lead does to their rates.
      var reach = Math.max(f.place, 1 - f.place) + 0.02;
      var lead = clamp(st.lead, 0, 1);
      var openL = reach * Math.pow(d, 0.5 + lead);
      var openR = reach * Math.pow(d, 1.5 - lead);
      var open = 0.5 * (openL + openR);
      // THE TEETH BITE ONLY ONCE THE OPENING HAS PASSED THE SLOT'S OWN EMPTINESS: while the two
      // leaves are still parting inside the work's own hole, the jamb is one straight edge. They
      // close again at the far door so both leaves clear the frame exactly.
      var bite = clamp(st.jamb, 0, 0.9)
               * clamp((open - f.half) / Math.max(f.half, 1e-4), 0, 1)
               * smoothstep(1, 0.85, d);
      return {
        vert: vert ? 1 : 0,
        slot: f.place,
        open: [openL, openR],
        bite: bite,
        teeth: Math.max(1, Math.round(clamp(st.teeth, 1, 24))),
        swing: clamp(st.swing, 0, 1) * 1.8 * d,
        press: clamp(st.travel, 0, 1) * clamp(st.press, 0, 1) * PRESS_MAX * (1 - d),
        drift: st.reduced ? 0 : DRIFT_MAX * Math.sin(TAU * (st.t || 0) / 9) * 4 * d * (1 - d),
        guard: clamp(st.shade, 0, 1) * smoothstep(0, 0.09, d) * smoothstep(1, 0.91, d),
        // read on the diagnostic surface, bound to no uniform: what the handles came to
        dial: d, half: f.half, reach: reach,
        slotInFile: f.inFile, halfInFile: f.halfInFile, seating: f.seating,
      };
    }

    // ---- THE DOOR THE INSTRUMENT READS FOR ITSELF ------------------------------------------------
    // His 18:00 architecture decision of 2026-08-17, carried in the U27 brief: the instrument reads
    // its doors at runtime on the actual buffer, and the report it hands back is the runtime truth;
    // what the manifest declares is only the claim. The meshing instrument answered that first
    // (pass-inst-gears.js) and the drifting one after it; this is the same law read in this
    // instrument's own units, which are the two LEAF EDGES and the buffer's own samples across them.
    //
    // WHAT A DOOR ASKS, AND WHY BOTH DOORS HOLD ON ANY BUFFER BY CONSTRUCTION. The shader's `cov` is
    // 1 for the points the departing work's leaves own and 0 for the points the arriving work owns.
    //   · AT THE ENTRY DOOR the dial stands at exactly 0 (the dead band above), so `pow(d, ·)` is 0,
    //     both openings are 0 and both edges stand exactly at the slot. Then `covL` is
    //     clamp(0.5 + (slot − a)/hA) and `covR` is clamp(0.5 + (a − slot)/hA) — one number and its
    //     own negation about a half — so their sum is 1 at every sample of every grid, and the frame
    //     is the departing work whole.
    //   · AT THE EXIT DOOR the dial stands at exactly 1, `bite` is zero because `smoothstep(1, 0.85, d)`
    //     is zero there, so every tooth stands at 1 and both leaves have opened by the full `reach`.
    //     The left edge stands at slot − reach ≤ −0.02 and the right at slot + reach ≥ 1.02. The
    //     FIRST sample centre of the buffer is at hA/2, so covL there is clamp(0.5 + (eL − hA/2)/hA)
    //     = clamp(eL/hA), which is 0 for any eL below zero on ANY buffer, however coarse; the last
    //     sample says the same of covR. So the frame is the arriving work whole.
    // Both readings are algebra rather than tolerance, which is what «by construction rather than by
    // tolerance» asks for.
    //
    // WHAT THE READING IS FOR, THEN. It is not a search for a leak this construction can produce —
    // it cannot produce one. It is the instrument answering for its own claim on the buffer it is
    // actually drawing on: break either of the two facts above and the reading says so in its own
    // measured numbers, which is exactly what the suite's red-on-bug rows put to it. There is no HOLD
    // beside it and none is invented: the slot is the departing work's own, and there is no
    // neighbouring slot this instrument could honestly move to.
    //
    // HOW FAR EITHER SIDE OF AN EDGE IS READ. The crossover band is exactly one sample wide — the
    // signed distance is divided by hA, so `cov` moves by one over one sample — and this reads three
    // samples either side, which carries that band three times over. The frame's own first and last
    // samples are read besides, so a leaf standing WHOLE in the frame is caught where the window
    // round its edge would not reach it. The three is this file's own and is named as such.
    var DOOR_READ = 3;

    // The grid the door is read on, and which of the two it is. `drawn` says which one the sentence
    // below names, since a reader told «a 780 x 1688 frame» would look for a device that has none.
    function doorGridOf(st) {
      var bw = Math.round(st.bufWidth), bh = Math.round(st.bufHeight);
      if (bw >= 1 && bh >= 1) return { w: bw, h: bh, drawn: true };
      return { w: Math.round(st.cssWidth), h: Math.round(st.cssHeight), drawn: false };
    }

    // THE LEAST AND THE MOST A TOOTH STANDS OPEN, exactly. `toothOpen` in FRAG runs over a WHOLE
    // COUNT of teeth, so the extremes are a walk over that count rather than a bound over the reals:
    // six parts the tooth's own place along the slot, four parts the score's die, both carried here
    // line for line.
    function toothSpan(v, seed) {
      var tn = Math.max(v.teeth, 1), lo = Infinity, hi = -Infinity, j, s, hash, rung, ord, m;
      for (j = 0; j < tn; j++) {
        rung = (j + 0.5) / tn;
        s = Math.sin((j + seed) * 127.1) * 43758.5453;
        hash = s - Math.floor(s);
        ord = rung + (hash - rung) * 0.4;
        m = 1 + v.bite * (2 * ord - 1);
        if (m < lo) lo = m;
        if (m > hi) hi = m;
      }
      return [lo, hi];
    }

    // The shader's own `cov` at one sample across the gate, with one tooth's opening. Every line has
    // its counterpart in FRAG above and nothing is simplified.
    function covAt(v, a, m, hA) {
      var l = v.slot - v.open[0] * m;
      var r = v.slot + v.open[1] * m;
      return clamp(clamp(0.5 + (l - a) / hA, 0, 1) + clamp(0.5 + (a - r) / hA, 0, 1), 0, 1);
    }

    // THE DOOR, MEASURED ON THE BUFFER. Null everywhere but at a door, since away from the doors a
    // gate standing part open is the picture rather than a fault. `want` is what the door's own law
    // asks `cov` to be at every point: 1 at the entry door, where the frame is the departing work
    // whole, and 0 at the exit door, where it is the arriving one.
    //
    // THE UNIT THE DEPARTURE IS SAID IN IS THE FRAME'S OWN. `col` is mix(colB, leaf, cov), so a
    // departure of `off` in the mask draws at most `off` of the distance between the two works on
    // that point — at most `off · 255` whole channel steps of an eight-bit frame. The reading
    // therefore counts WHOLE STEPS, which is a ceiling of what the frame can show and never an
    // estimate of it: below one whole step no pixel of the buffer can differ, and no threshold of
    // this file's own choosing stands anywhere in it.
    function doorReadOf(v, st) {
      var want = v.dial === 0 ? 1 : (v.dial === 1 ? 0 : -1);
      if (want < 0) return null;
      var g = doorGridOf(st);
      var resA = v.vert ? g.w : g.h;
      if (!(resA >= 1)) return null;
      var hA = 1 / resA;
      var span = toothSpan(v, Number(st.seed) || 0);
      var worst = 0, at = -1, mAt = 1, i, k, mi, m, edge, ie, i0, i1, a, off;
      var reads = [];
      for (k = 0; k < 2; k++) {
        for (mi = 0; mi < 2; mi++) {
          m = span[mi];
          edge = k ? v.slot + v.open[1] * m : v.slot - v.open[0] * m;
          ie = edge * resA - 0.5;
          i0 = Math.max(0, Math.ceil(ie - DOOR_READ));
          i1 = Math.min(resA - 1, Math.floor(ie + DOOR_READ));
          for (i = i0; i <= i1; i++) reads.push([i, m]);
        }
      }
      // the frame's own two ends, so a leaf standing whole inside the frame is caught even where the
      // window round its edge does not reach it
      reads.push([0, span[0]], [resA - 1, span[0]], [0, span[1]], [resA - 1, span[1]]);
      for (i = 0; i < reads.length; i++) {
        a = (reads[i][0] + 0.5) / resA;
        off = Math.abs(covAt(v, a, reads[i][1], hA) - want);
        if (off > worst) { worst = off; at = reads[i][0]; mAt = reads[i][1]; }
      }
      return { grid: g, want: want, resA: resA, worst: worst, at: at, tooth: mAt,
               steps: Math.round(255 * worst), samples: reads.length };
    }

    // THE REFUSAL, worded the way the host's own manifest refusals read: what is wrong, in this
    // instrument's own measured numbers, on the grid it was measured on.
    function doorWhyNoOf(read) {
      if (!read || read.steps < 1) return null;
      var g = read.grid;
      return (read.want ? "the entry" : "the exit") + " door leaks: at sample " + read.at
           + " of the " + read.resA + " this instrument's own mask is sampled at across the gate's "
           + "axis on a " + g.w + " x " + g.h + (g.drawn ? " buffer" : " frame")
           + ", that mask draws a coverage of "
           + (read.want ? 1 - read.worst : read.worst).toFixed(6)
           + " for the " + (read.want ? "arriving" : "departing") + " work there — "
           + read.steps + " whole channel step" + (read.steps === 1 ? "" : "s")
           + " of 255 — where " + (read.want ? "the entry" : "the exit")
           + " door's own law asks for the " + (read.want ? "departing" : "arriving")
           + " work at every point";
    }

    // THE NUMBERS OF ONE FRAME, WITH ITS DOOR READ ON THE BUFFER BEING DRAWN. Away from a door this
    // is `posed` and nothing more: the reading is taken nowhere else. At a door it is taken and
    // published, and the record carries what the score asked for beside what the seating applied —
    // `slotInFile` is the place the score handed in, as a share of the file, and `slot` is where that
    // place landed in the frame once the host's own cover fit had carried it there.
    function values(st) {
      var v = posed(st);
      var read = doorReadOf(v, st);
      v.doorGrid = read ? read.grid : null;
      v.doorWorst = read ? read.worst : null;
      v.doorSteps = read ? read.steps : null;
      v.doorSamples = read ? read.samples : null;
      v.doorWhyNo = doorWhyNoOf(read);
      return v;
    }

    var manifest = {
      id: "gates", api: 1, arity: 2,
      // The departing work's two masses come apart and travel out of the frame; the opening between
      // them is the mystery; the arriving work stands behind it from the first crack and opens out to
      // its own frame as they leave.
      roles: ["disassembly", "mystery", "assembly"],
      // READ OFF THE MODULE'S OWN HEADER AND SAID TO BE DERIVED — the two levels, with the lines they
      // were read from, stand in this file's opening comment. Neither module-contract file carries a
      // `gates` row, so no level is published for it anywhere else.
      levels: ["CELL", "CELL CONTENT"],
      // WHAT THIS INSTRUMENT CUTS ON. Two masses facing each other across a slot: the frame falls
      // into panels along the work's own region line and the crossing is those panels parting. The
      // composer's own `KIND_OF_MEASURE` maps the `regions` measure to `panel`, which is the kind
      // this cut is named in.
      cuts: ["panel"],
      // WHERE THIS INSTRUMENT HAS A SEAM (§8's `seams` block, pass-layer.js). The panel cut is the two
      // leaves parting from the slot, and the shader's own comment above names the edge exactly:
      // "COVERAGE OVER THE PIXEL'S OWN FOOTPRINT. Across the gate the edge is a straight line and the
      // signed distance in pixels is exact" — `covL`/`covR` are `clamp(0.5 + (l - a) / hA, 0.0, 1.0)`
      // and its mirror, `hA = 1.0 / resA`. THE DOOR THE INSTRUMENT READS FOR ITSELF says the width of
      // it plainly: "the crossover band is exactly one sample wide — the signed distance is divided
      // by hA, so `cov` moves by one over one sample" (HOW FAR EITHER SIDE OF AN EDGE IS READ, above).
      // That is a hairline retouch on an edge that is otherwise exact by construction, not a
      // deliberate handover — along the slot a tooth's own step is filtered by three taps for the
      // same reason, so a jittered tooth edge never lands as a hard stair. `of` names no handle
      // because the one-sample width is set by `hA` alone and does not shrink as the tooth count
      // moves.
      seams: [{ kind: "line", of: null, unit: "points of the drawing buffer" }],
      params: { jamb: [0, 0.9], teeth: [1, 24], swing: [0, 1], press: [0, 1], lead: [0, 1] },
      // EVERY handle a score can drive (§4.4b). The five above are the module's own declared params
      // (gates.js:435-441); `mix` is its one travelling number and `clock` the second the host hands
      // down; `seed` is its die; `shade` and `travel` are two of its three judge channels, resting
      // where the module rests them.
      //
      // NO HANDLE HERE KEEPS A CLOCK OR A ROLL OF ITS OWN. The one place the module reads time is the
      // arriving work's drift along the slot (gates.js:577), where `t` was its own accumulated frame
      // time; it reads the `clock` handle instead, so a seeded score repeats to the pixel. The die
      // the module rolls once at creation when a score names none (gates.js:249-254) is the `seed`
      // handle here, and nothing rolls unasked.
      //
      // THE THREE THAT CARRY THE DEPARTING WORK'S OWN GATE. The module measures the source it was
      // handed at build (`gateOf`, gates.js:398-409) and this file may not read a picture, so the
      // reading arrives as handles — the road pass-inst-adrift.js already took for its own fourteen
      // build-time numbers. THEIR DEFAULTS ARE THE MODULE'S OWN NAIVE READING (gates.js:399-400): the
      // slot upright, in the middle of the frame, at half the motif's own band. That is the reading
      // the module itself uses for a source with no gate, so a pair whose record says nothing about a
      // gate gets exactly the picture the module gives such a pair — and never an invented number
      // passed off as the work's own.
      //   · `slotAxis` — 1 the slot stands upright and the gates open sideways, 0 it lies across and
      //     they part up and down. The module reads both axes and takes the better one.
      //   · `slotPlace` — where the slot stands along that axis, AS A SHARE OF THE FILE. `values`
      //     seats it through the fit the host applied, exactly as the module seats its own.
      //   · `slotHalf` — half the slot's own width, on the same share of the file. It decides how
      //     long the two leaves part along a straight edge before the jamb breaks into teeth.
      //
      // THE COLUMN A RECORD PUBLISHES FOR THESE THREE, since lab/step1-motifs.py's rewrite of
      // 2026-08-19 that ported `slotOn`/`gateOf` (gates.js:376-409) into the collection's own
      // measure and deleted the fixed 0.42-to-0.58 band this note used to name. A work record now
      // carries all three beside `motifs.gateGap`:
      //     motifs.gateAxis    — which axis the slot stands on   (lab: motifs.gate_axis)
      //     motifs.gatePlace   — where it stands along that axis, as a share of the FILE's own side
      //                                                          (lab: motifs.gate_place)
      //     motifs.gateHalf    — half its own width, on that same share
      //                                                          (lab: motifs.gate_half)
      // and `measuredParts()` in pass-composer.js carries them through as `gateAxis`, `gatePlace`
      // and `gateHalf`, which the fill's own "gates" branch there drives `slotAxis`, `slotPlace`
      // and `slotHalf` from — the vocabulary this file's own handles speak.
      //
      // THE TWO THAT TAKE A NUMBER OTHER THAN THE ONE THEY ARE HANDED, published beside their ranges
      // by the same rule the meshing instrument's ladder is published by.
      //   · `teeth` — A WHOLE COUNT. `toothOpen` divides the slot into that many teeth, so the count
      //     is rounded to a whole before any tooth is cut and never interpolated.
      //   · `jamb` — HELD SHUT UNTIL THE OPENING PASSES THE SLOT'S OWN EMPTINESS, and closed again at
      //     the far door. Both are the module's own gate on the bite (gates.js:567-569): the teeth
      //     cannot bite while the leaves are still parting inside the work's own hole, and they close
      //     at the end so both leaves clear the frame exactly, which is what makes the exit door one
      //     whole work.
      //
      // `dial` is OPEN: a score that names no track for it leaves the instrument deriving the
      // travelled number from `mix` through the measured response curve, exactly as the module does.
      // It is also where the module's third judge channel went — `rawfeel` (gates.js:730), the walk
      // with the curve taken out, is a score driving `dial` straight.
      handles: {
        // LEVEL, PER CHARTER SHELF 17 (docs/design/PASS-API-V1.md:716). `mix` is the crossing's own
        // dial, `clock` the module's own time, `seed` the score's die, and `shade`/`travel`/`mask`
        // are the fleet's judge channels — all six are the passage's own idiom rather than a
        // structural level, and level: null across the whole fleet.
        mix: { min: 0, max: 1, def: 0, level: null },
        clock: { min: 0, max: 14, def: 0, level: null },
        // `dial` is already `open: true` — the instrument reads its own door here and the composer
        // drives it at no level.
        dial: { min: 0, max: 1, def: 0, open: true, level: null },
        jamb: { min: 0, max: 0.9, def: 0.55,
                applied: { shutBelowTheSlotsOwnWidth: true, shutAtTheFarDoor: true },
                level: "CELL" },
        teeth: { min: 1, max: 24, def: 9, kind: "count", applied: { roundedToWholeTeeth: true },
                 level: "CELL" },
        swing: { min: 0, max: 1, def: 0.35, level: "CELL CONTENT" },
        press: { min: 0, max: 1, def: 0.65, level: "CELL CONTENT" },
        lead: { min: 0, max: 1, def: 0.5, level: "CELL" },
        slotAxis: { min: 0, max: 1, def: 1, level: "CELL" },
        slotPlace: { min: SLOT_AT_MIN, max: SLOT_AT_MAX, def: 0.5,
                     applied: { seatedThroughTheHostsOwnFit: true, reads: "slotInFile",
                                clampedInFrame: [SEATED_MIN, SEATED_MAX] },
                     level: "CELL" },
        slotHalf: { min: SLOT_MIN, max: SLOT_MAX, def: MOTIF_BAND / 2,
                    applied: { seatedThroughTheHostsOwnFit: true, reads: "halfInFile",
                               clampedInFrame: [SLOT_MIN, SLOT_MAX] },
                    level: "CELL" },
        seed: { min: 0, max: 8, def: 0, level: null },
        shade: { min: 0, max: 1, def: 1, level: null },
        travel: { min: 0, max: 1, def: 1, level: null },
        // THE FLEET'S JUDGES' CHANNEL, and the one handle here the lab module has no counterpart
        // for. It is not an artistic handle and it is not invented for this instrument: thirteen
        // instruments published it before this one, always for the same job — the frame with the
        // instrument's OWN CUT painted in place of the picture, so a law about the cut is measured on
        // the frame. This one paints the two leaves and the opening between them, and it rests at 0,
        // where the line that reads it is the identity.
        mask: { min: 0, max: 1, def: 0,
                applied: { shows: "the two leaves as red and green and the opening as black, "
                                + "written with no blue at all" },
                level: null },
      },
      neutrals: { a: 0, b: 1 },
      doors: { in: { handle: "mix", value: 0, work: "a" },
               out: { handle: "mix", value: 1, work: "b" } },
      // Both doors frame alike, so one record covers them: the constant centre crop the squeeze and
      // the drift are paid for with (ZOOM above, 1.27).
      framings: { "0": { coverCrop: ZOOM }, "1": { coverCrop: ZOOM } },
      drivers: ["progress", "cueProgress", "time", "velocity", "capability", "noise", "static",
                "curve", "spline", "map", "add", "multiply", "mix", "clamp", "hold", "segment",
                "ramp", "slew", "oscillate", "node"],
      // The construction moves no point of view: it decides which work owns each point of the frame,
      // slides the departing work's two masses out of it and squeezes the arriving one through the
      // opening. All of that is what it does to its own surface, so the witness camera stays the
      // stage's (§6).
      camera: { needs: "none", authority: "stage" },
      gl: { preserveDrawingBuffer: false },
      // THE COVERAGE LAW (§7). This instrument fills the frame: `cov` partitions every point between
      // the departing work's leaves and the arriving work behind them, both branches are picture, and
      // no point is left unclaimed — the module's own first law, «COVERAGE, NEVER TRANSPARENCY … No
      // alpha is ever written but 1» (gates.js:48-55). So the alpha is the constant 1 and a cue of
      // this instrument may stand at the bottom of a stack.
      coverage: { writes: false,
                  how: "the gate partitions the frame between the departing work's two leaves and "
                     + "the arriving work standing behind them, so no point of the frame is left "
                     + "unclaimed and the alpha is the constant 1" },
      // The neutral pose is the ENTRY DOOR — `mix` at 0, the value the `doors` block above names —
      // so the frame keys the host reads off it at registration include the door's own record.
      neutralPose: { mix: 0, jamb: 0.55, teeth: 9, swing: 0.35, press: 0.65, lead: 0.5,
                     slotAxis: 1, slotPlace: 0.5, slotHalf: MOTIF_BAND / 2,
                     seed: 0, shade: 1, travel: 1, mask: 0,
                     cssWidth: 1000, cssHeight: 1000, t: 0, reduced: false },
      passes: [{
        program: "gates", vert: VERT, frag: FRAG, position: "aPos",
        uniforms: [
          { name: "uA", type: "sampler2D", source: "textureA" },
          { name: "uB", type: "sampler2D", source: "textureB" },
          { name: "uFitA", type: "vec4", source: "fitA" },
          { name: "uFitB", type: "vec4", source: "fitB" },
          { name: "uRes", type: "vec2", source: "resolution" },
          { name: "uVert", type: "float", source: "frame:vert" },
          { name: "uSlot", type: "float", source: "frame:slot" },
          { name: "uOpen", type: "vec2", source: "frame:open" },
          { name: "uBite", type: "float", source: "frame:bite" },
          { name: "uTeeth", type: "float", source: "frame:teeth" },
          { name: "uSwing", type: "float", source: "frame:swing" },
          { name: "uPress", type: "float", source: "frame:press" },
          { name: "uDrift", type: "float", source: "frame:drift" },
          { name: "uGuard", type: "float", source: "frame:guard" },
          { name: "uSeed", type: "float", source: "handle:seed" },
          { name: "uMask", type: "float", source: "handle:mask" },
        ],
      }],
      // The instrument allocates nothing of its own: it spends the two source-texture slots the host
      // already holds and the one programme the host builds from this manifest.
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
      // The lab module stands untracked in the tlvphotos worktree on the day of this port, so there
      // is no commit to name and none is invented. The digest of the file the port was read from
      // stands in its place, and a row re-weighs the file against it.
      provenance: { labPath: "lab/effects/gates.js", commit: null,
                    sha256: "f2e581532509445d6a452b1b4d65cf51b1d0e9238310d5b50fcb89c0da8bafd7" },
      // HOW WELL THIS INSTRUMENT SUITS A PAIR (2026-08-18, his word of 09:51 and its sharpening at
      // 09:53). An instrument no longer answers WHETHER it takes a pair — it answers how well it
      // suits one, so a poor fit is still playable and still explains itself. The arithmetic runs in
      // the composer, which is the one place holding both records; what stands here is the
      // instrument's own statement of WHAT IT READS, which is the fact this file owns.
      //
      // THE MOTIF IS ALREADY THE COMPOSER'S. It carries `MOTIF_GATE = "ворота"` and its `LOCUS_KINDS`
      // name a `gate`, so a work record's `motifs.measured` list and its `motifs.gateGap` are the two
      // readings this instrument is placed by, and neither has to be invented for it.
      //
      // THE DEPARTING WORK'S OWN SLOT IS WHAT PARTS, so the reading is of that work rather than of
      // both: the arriving work comes THROUGH the opening and gives the gate nothing. A fit of
      // nothing is never a refusal — it ranks last, plays where nothing ranks higher, and the slot
      // then stands in the middle of the frame at the motif's own band width, which is the module's
      // own reading for a work with no gate.
      suits: { reads: ["motifs.measured", "motifs.gateGap"],
               how: "the departing work's own slot is what parts, so it suits a pair whose departing "
                  + "work carries ворота plainly — the fit is that work's own measured gate gap, and "
                  + "it is nothing where the work carries no gate at all, which still plays with the "
                  + "slot standing in the middle of the frame at the motif's own band width" },
      readiness: "production-ready",
    };

    var live = false;
    return {
      name: "gates",
      manifest: manifest,
      values: values,
      fit: fit,
      feel: feelOf,
      prepare: function (o) {
        if (!o.sources) return { take: false, why: "the gate instrument needs both works" };
        if (!o.cue) return { take: false, why: "no cue names it" };
        return { take: true };
      },
      start: function () { live = true; },
      // The pose the shader draws. Every number in it comes from a handle a score can drive, and the
      // arriving work's drift reads the second the host hands down, so a seeded run repeats to the
      // pixel. The redraw the preserved buffer stood in for is the host's own frame loop: this draws
      // on every frame it is handed, and reduced motion stops the drift alone.
      //
      // A DOOR THIS INSTRUMENT CANNOT KEEP WHOLE IS REFUSED RATHER THAN DRAWN. The door law is the
      // instrument's own claim (the manifest's coverage line above), so the instrument is what
      // answers for it: at either door it reads its own mask on the buffer the host is about to bind
      // and, where the mask draws a whole channel step of the wrong work, hands the host the reason
      // with the measured coverage in it instead of drawing a door that is two works at once. The
      // host recovers the transaction on that reason and the walk's own glide carries the visitor,
      // which is the product's own behaviour with no renderer.
      frame: function (st) {
        if (!live) return;
        var h = st.handles;
        var dial = typeof h.dial === "number" ? h.dial : feelOf(clamp(h.mix, 0, 1));
        var pose = {
          dial: dial,
          jamb: h.jamb, teeth: h.teeth, swing: h.swing, press: h.press, lead: h.lead,
          slotAxis: h.slotAxis, slotPlace: h.slotPlace, slotHalf: h.slotHalf,
          seed: h.seed, shade: h.shade, travel: h.travel, mask: h.mask,
          cssWidth: st.viewport.w, cssHeight: st.viewport.h, t: h.clock, reduced: st.reduced,
          // THE GRID THE SHADER WILL SAMPLE ON, carried into the pose so the door is read on the
          // buffer the host is about to bind as `uRes` rather than on the CSS frame around it. The
          // host settles it from the device ratio and its own resolution step, so it moves while a
          // pass plays and each door is read on the grid standing at that door's own instant.
          bufWidth: st.viewport.bufferW, bufHeight: st.viewport.bufferH,
          // BOTH WORKS' SEATING ON THAT BUFFER, which only the host can answer and which it hands
          // down on the frame state. The slot's measured place is carried into the frame through it,
          // so the gate opens where the measurement says the work's own gate stands rather than where
          // a cover fit was guessed at.
          fitA: st.fitA, fitB: st.fitB,
        };
        // AT A DOOR THE INSTRUMENT SAYS WHAT IT APPLIED, and says it before it refuses. `request` is
        // the slot the score handed in, as a share of the FILE; `applied` is where that slot landed
        // in the frame once the host's own cover fit had carried it there; `moved` is the two read
        // against each other, in frame widths along the gate's own axis.
        if (dial === 0 || dial === 1) {
          var v = values(pose);
          if (st.reportApplied) {
            st.reportApplied({
              door: dial === 0 ? "in" : "out",
              buffer: [pose.bufWidth, pose.bufHeight],
              reads: "slot", request: v.slotInFile, applied: v.slot,
              moved: v.slot - v.slotInFile, unit: "frame widths",
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
    instrument: gatesInstrument(),
  });
})();
