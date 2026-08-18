/*!pass-inst-hero.js*/
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
  // THE FOLD-WINDOW-PLANET INSTRUMENT (§8) — lab/effects/hero.js carried across
  // ================================================================================================
  // WHAT THE VISITOR SEES. The departing photograph stands whole. It folds about a vertical axis and
  // meets its own mirror; a second fold crosses the first; two more folds and a mirror across a ring
  // open the frame into a rose window of wedges and courses. At the deepest place the wedges unwind
  // while the picture pours into a polar reading — the angle becomes a column of the photograph and
  // the distance becomes a row, so the frame is a small planet standing in its own sky. The arriving
  // photograph comes in there, on a soft ring that sweeps outward so no point of the frame ever shows
  // two photographs at once, and the whole road is then walked back: the planet unwinds into the
  // window, the window closes fold by fold, and the arriving photograph stands whole.
  //
  // EVERYTHING BETWEEN THE TWO DOORS IS ONE WARP FIELD in polar coordinates about one centre, so
  // every in-between position is a real transformation of a photograph and never a dissolve between
  // two pictures. That is the module's own first sentence and it is the reason this instrument is
  // lawful under the charter's parameter-travel law.
  //
  // WHERE IT STANDS IN THE CHARTER. lab/CROSSING-BRIEF.md's vocabulary table records it as
  // «hero · fold-window-planet · ready story · multi · scroll-driven; unused in crossings yet». It is
  // the only entry in that table whose role is a whole STORY rather than a переход or an оживление,
  // and this port is what makes the story a crossing: the same table gives `planet` and
  // `kaleidoscope` — the two devices this module's middle is built out of — the SURFACE level, and
  // `livemirror`, the mirror fold it opens with, the CELL level. Those two are what this instrument
  // declares, and the reading is derived rather than carried: the module postdates
  // lab/data/module-contract.json and has no row there.
  //
  // WHAT A CROSSING USES IT FOR, SAID PLAINLY. It is a whole passage in one voice. The folds take the
  // departing work apart about its own measured radial centre — that is the disassembly; the rose
  // window and the planet are a place where neither work is legible — that is the mystery; and the
  // same road walked backwards puts the arriving work together — that is the assembly. One cue
  // covers the three roles a crossing is built out of, so a route may cast it where the pair reads
  // radial and get a whole crossing out of a single instrument, which is what the charter's «ready
  // story» means. It fills the frame at every point, so it is also the GROUND a ring-cut passage
  // stands on — the want lane D's report named as the one instrument the collection still lacked.
  //
  // ------------------------------------------------------------------------------------------------
  // THE ARC, AND WHOSE SHAPE IT IS
  // ------------------------------------------------------------------------------------------------
  // The module's story runs one way: a page scrolls and the planet leaves at the bottom of it. A
  // crossing has two doors and the arriving work has to STAND at the second one, so the story here is
  // walked out and back — out through the folds into the window and the planet, and back out of them
  // into the arriving work.
  //
  // THE THERE-AND-BACK IS THE MODULE'S OWN WALK AND NOT THIS PORT'S INVENTION. Where nothing drives
  // its scroll the module walks exactly this: a triangle out and back, eased by `tri*tri*(3-2*tri)`
  // (hero.js's own `targetScroll`). This instrument takes that walk as its dial's own shape, hands it
  // to the module's own measured response curve `feel`, and multiplies by the story's own far end.
  // Both ends of the triangle and its turning point are places where the picture rests, which is why
  // a landing is exact and why the deepest place holds instead of bouncing.
  //
  // HOW FAR OUT THE ARC GOES IS THE PAIR'S OWN READING. `planet` carries `structure.polar.planet`,
  // the collection's own measurement of how strongly a work reads as a planet, and it places the far
  // end of the arc between the rose window standing widest — s = 0.54, where the module's fourth fold
  // is at its peak and the unwinding has barely begun — and the small planet at s = 0.80, which the
  // module names as the last place in its story where a picture still STANDS. A pair that reads
  // nothing polar turns back at the window; a pair that reads it goes all the way to the planet.
  //
  // ------------------------------------------------------------------------------------------------
  // WHAT CAME OVER, AND WHAT STAYED BEHIND
  // ------------------------------------------------------------------------------------------------
  // WHAT CAME OVER, digit for digit: the four successive angular mirrors about 0, PI/2, PI/4 and
  // PI/8 with their own ramps and their own unwinding; `foldTo`, where the reflected copy is always
  // the exact reflection and what grows with the amount is the circle the mirror has reached out to,
  // with its travelling crease light; the mirror across a ring that turns the wedges into a window
  // with courses; the polar reading and the 1.45 power its rows are read on; the soft ring `wipe`
  // that carries a picture change outward so no point shows two photographs at once; the sky past the
  // planet's rim with its own thinning, its rim light and its centre light; the spin, the twirl and
  // the crop's own pull-back; the frame's own narrow-and-open sampling; the vignette, the soft clip
  // and the dither. Every one of them is carried at the module's own numbers and the suite reads both
  // files for each.
  //
  // WHAT STAYED BEHIND: the module's own canvas and context, its frame loop, its resize observer, its
  // texture uploads and its pointer listeners (§1.2's fence); the page's own furniture — the quiet
  // area under the title, the title's own ellipse and the ramp that carries the planet down out of
  // the frame as the page scrolls on, none of which exists inside a crossing; and the module's third
  // photograph, because a cue carries an ordered PAIR (§8's `arity: 2`) and two works are what a pair
  // can stand. With two works there is ONE picture change instead of three, and it is the module's
  // own third one — the change that happens while the planet forms, which is the one place on this
  // road where neither work is legible.
  //
  // AND TWO THINGS THE HOST OWNS THAT THE MODULE OWNED. The module uploads its own textures with
  // mirrored wrapping and a full mipmap chain, and its sampler reads every point TWICE — once sharp
  // for brightness and once blurred for colour, which is its answer to the coloured speckle a
  // web-compressed photograph carries in its chroma. The host owns every texture in this engine and
  // uploads them clamped at their own edges with no mipmap chain at all (pass-layer.js's own
  // `makeTex`), so on the host's texture an explicit level-of-detail selects the base level whatever
  // it asks for and the second, coarser tap returns the very same texel as the first: both the
  // anti-aliasing and the chroma trick are INERT here rather than removed. Carrying dead arithmetic
  // in a shipping instrument would be worse than saying so, so neither is carried — and both are
  // written down as findings, because what the module bought with them (a planet that does not
  // alias, and a sky without coloured speckle) is a real thing this port does without until the host
  // uploads its sources with a mipmap chain.
  //
  // ------------------------------------------------------------------------------------------------
  // THE COVERAGE: THIS INSTRUMENT FILLS THE FRAME
  // ------------------------------------------------------------------------------------------------
  // §7's coverage law of 12:40 asks every instrument to say where its own matter is absent. It is
  // absent nowhere, and the reason is the construction rather than a claim: the warp field is a map
  // from every point of the frame to a point of a source, the map is total — a fold, a ring mirror
  // and a polar reading are each defined at every point — and the host's sources are clamped at their
  // own edges, so every point of the frame carries a photograph. Where the planet stands, the frame
  // past its rim carries the sky the module draws there, which is a COLOUR and not an absence. The
  // alpha is therefore the constant 1, said as a decision, and under the placement rule (§8 as
  // amended 14:05, and `coverageWhyNo`) that makes this instrument lawful as the LOWEST cue of a
  // stack and as a whole one-cue score.
  function heroInstrument() {
    var VERT = [
      "attribute vec2 aPos;",
      "varying vec2 vUv;",
      "void main(){ vUv = vec2(aPos.x * 0.5 + 0.5, 0.5 - aPos.y * 0.5); gl_Position = vec4(aPos, 0.0, 1.0); }",
    ].join("\n");

    // ----------------------------------------------------------------------------------------------
    // THE SHADER, AND THE THREE THINGS THE HOST'S CARRIERS CHANGED ABOUT IT
    // ----------------------------------------------------------------------------------------------
    // The module's own fragment shader is GLSL ES 3.00 and reads a vertex id; it declares three
    // sources, three aspects, three pixel widths, three pixel heights and two three-wide content
    // offsets. The host binds four uniform types and no more — `sampler2D`, `float`, `vec2`, `vec4`
    // (pass-layer.js's own `UTYPE`) — draws a quad from an attribute it binds by the manifest's own
    // name, and stamps the version header itself. Three things follow, and none of them touches a
    // line of the mathematics:
    //
    //   · THE SOURCE'S OWN SHAPE ARRIVES AS THE HOST'S COVER FIT. The module scales its sampling by
    //     `min(1, aspect/frameAspect) * crop`, which is the cover fit written out by hand from an
    //     aspect it uploads for itself. The host already hands every instrument that same fit as
    //     `fitA`/`fitB`, and the two are equal term for term: for a source wider than the frame the
    //     fit is (frame/source, 1) and the module's factor is `crop`; for a narrower one the fit is
    //     (1, source/frame) and the module's factor is `crop * source/frame`. So the three aspect
    //     uniforms are gone and the sampling reads the host's own supply instead.
    //   · THE ROWS RUN THE OTHER WAY. The module uploads its textures flipped, so its own v = 0 is a
    //     picture's bottom row; the host uploads them unflipped (`UNPACK_FLIP_Y_WEBGL, false`). Every
    //     v this shader computes is therefore turned over once, at the one place it is built.
    //   · THE LOOSE FLOATS TRAVEL FOUR TO A CARRIER. Eleven single numbers of the pose ride three
    //     `vec4`s — the warp, the sky and the world — in the order the comments below name. No number
    //     is combined with another; the carriers are boxes.
    var FRAG = [
      "precision highp float;",
      "varying vec2 vUv;",
      "uniform sampler2D uA;",            // the work the frame is leaving
      "uniform sampler2D uB;",            // the work it is arriving at
      "uniform vec4 uFitA;",
      "uniform vec4 uFitB;",
      "uniform vec2 uRes;",
      // WHERE THE FOLDS TURN, in frame units with y up and the frame's own middle at nothing. This is
      // the pair's own measured radial centre standing where that point of the picture stands in the
      // frame, and it is nothing at both doors.
      "uniform vec2 uCen;",
      // AND WHERE THAT CENTRE SITS INSIDE THE PICTURE, in the host's own uv with rows running down.
      "uniform vec2 uSam;",
      // THE FOUR ANGULAR MIRRORS' OWN AMOUNTS: about 0, PI/2, PI/4 and PI/8, each arriving and
      // leaving on its own ramp, so a half-engaged fold is a picture caught halfway into its mirror.
      "uniform vec4 uFold;",
      // THE WARP: how much of the picture the frame spans, the ring mirror's own strength, the radius
      // it stands at, and how far the reading has poured from flat into polar.
      "uniform vec4 uWarp;",
      // THE SKY: the planet's own radius in frame-height units, the turn the story carries, the
      // twirl that gathers about the centre, and how hard the world ends at its rim.
      "uniform vec4 uSky;",
      // THE WORLD: how far the picture is pushed away, the light the story asks for, how far the
      // frame has left its own door, and how far the picture change has swept.
      "uniform vec4 uWorld;",
      // The judges' channel: the warp field itself, as colour.
      "uniform float uMask;",
      "const float PI  = 3.14159265359;",
      "const float TAU = 6.28318530718;",
      // WHAT THE BOX THE SKY IS PAINTED IN (hero.js:159): the ground past the rim of the world.
      "const vec3 SKY = vec3(0.045, 0.048, 0.058);",
      // A SOFT RING SWEEPING OUTWARD (hero.js:71-75): nothing everywhere at m = 0, everything
      // everywhere at m = 1, and in between one travelling edge, so no point of the frame ever shows
      // two photographs at once.
      "float wipe(float m, float x){",
      "  float f = mix(-0.09, 1.27, m);",
      "  return smoothstep(f + 0.09, f - 0.09, x);",
      "}",
      // ONE MIRROR (hero.js:77-91). The reflected copy is always the exact reflection, never a
      // squeezed one: what grows with the amount is the circle out to which the mirror has reached.
      // A half-made fold is the picture near the crease and its own reflection inside it, and the
      // crease carries a little light while it travels.
      "float foldTo(float A, float axis, float amt, float sgn, float r, float w, inout float edge){",
      "  if (amt <= 0.002) return A;",
      "  float t    = (A - axis) * sgn;",
      "  float side = step(0.0, -t);",
      "  float front = amt * 1.45;",
      "  float k = side * (1.0 - smoothstep(front - w, front + w, r));",
      "  float g = amt * (1.0 - amt) * 4.0;",
      "  float b = (r - front) / (w * 2.4);",
      "  edge += side * g * exp(-b * b);",
      "  return mix(A, 2.0 * axis - A, k);",
      "}",
      // WHERE ONE POINT OF THE FRAME FALLS ON ONE SOURCE, read either flat or polar and travelling
      // between the two readings of the very same point (hero.js:93-114). Flat: the direction and the
      // distance, cover-fitted by the host's own fit and cropped by the story's own crop. Polar: the
      // angle read as a COLUMN of the source and the distance as a ROW of it. The rows are turned
      // over once here, because the host uploads its sources unflipped.
      "vec2 uvOf(vec4 f, float af, float A, float rr, vec2 dd){",
      "  vec2 uvA = vec2(uSam.x + (dd.x / af) * f.x * uWarp.x,",
      "                  uSam.y - dd.y * f.y * uWarp.x);",
      "  float vr = rr / max(uSky.x, 1e-5);",
      "  vec2 uvB = vec2(A / TAU + 0.5, 1.0 - pow(min(vr, 1.0), 1.45));",
      "  return clamp(mix(uvA, uvB, uWarp.w), 0.0008, 0.9992);",
      "}",
      "void main(){",
      "  float af = uRes.x / max(uRes.y, 1.0);",
      "  vec2  n  = vUv;",
      "  vec2  q  = vec2((vUv.x - 0.5) * af, 0.5 - vUv.y);",
      "  vec2  d  = (q - uCen) * uWorld.x;",
      "  float r  = length(d);",
      "  float a  = atan(d.x, d.y) + uSky.y + uSky.z * exp(-r * 2.4);",
      "  a = mod(a + PI, TAU) - PI;",
      // FOUR SUCCESSIVE MIRRORS: 1 -> 2 -> 4 -> 8 -> 16 wedges, each one arriving on its own. The
      // seam is held at a few points wide whatever the radius (hero.js:125-134).
      "  float pxu = uRes.y / max(uWorld.x, 1e-6);",
      "  float fw  = 5.0 / pxu;",
      "  float edge = 0.0;",
      "  float A = a;",
      "  A = foldTo(A, 0.0,        uFold.x,  1.0, r, fw, edge);",
      "  A = foldTo(A, 0.5   * PI, uFold.y, -1.0, r, fw, edge);",
      "  A = foldTo(A, 0.25  * PI, uFold.z, -1.0, r, fw, edge);",
      "  A = foldTo(A, 0.125 * PI, uFold.w, -1.0, r, fw, edge);",
      // A MIRROR ACROSS A RING turns the wedges into a window with courses (hero.js:136-142).
      "  float rw = 7.0 / pxu;",
      "  float rt = uWarp.z - r;",
      "  float rk = step(0.001, uWarp.y) * step(0.0, -rt) *",
      "             (1.0 - smoothstep(uWarp.y * 0.34 - rw, uWarp.y * 0.34 + rw, -rt));",
      "  float rr = max(mix(r, 2.0 * uWarp.z - r, rk), 0.0);",
      "  vec2  dd = vec2(sin(A), cos(A)) * rr;",
      // THE PICTURE CHANGE, on the module's own outward ring (hero.js:144-148). One change, because a
      // cue carries one ordered pair.
      "  float x = clamp(rr / 0.85, 0.0, 1.15);",
      "  float w = wipe(uWorld.w, x);",
      "  vec2 uva = uvOf(uFitA, af, A, rr, dd);",
      "  vec2 uvb = uvOf(uFitB, af, A, rr, dd);",
      "  vec3 col = mix(texture2D(uA, uva).rgb, texture2D(uB, uvb).rgb, w);",
      // PAST THE RIM OF THE WORLD the sky keeps going, and thins (hero.js:155-163).
      "  float v      = rr / max(uSky.x, 1e-5);",
      "  float beyond = max(v - 1.0, 0.0);",
      "  float atmo   = exp(-beyond * mix(3.2, 7.5, uSky.w));",
      "  col = mix(SKY, col, mix(1.0, atmo, uWarp.w));",
      "  col += uWarp.w * 0.09 * exp(-abs(v - 1.0) * 15.0) * vec3(0.62, 0.68, 0.80);",
      "  col += uWarp.w * 0.16 * exp(-length(q - uCen) * 1.3) * vec3(0.34, 0.40, 0.52);",
      "  col += clamp(edge, 0.0, 2.0) * 0.085 * vec3(1.00, 0.97, 0.92);",
      "  col = clamp(col, 0.0, 1.0);",
      // EVERY COLOUR THIS INSTRUMENT LAYS OVER THE PHOTOGRAPH RIDES THE DOOR GATE — the soft clip,
      // the vignette and the dither. That is one rule and it is the reason a door is exactly the work
      // its source carries: at a door the gate is nothing and the frame is the photograph and nothing
      // else. Everywhere the gate stands whole they are the module's own, at its own numbers
      // (hero.js:166, :178-183).
      "  float lean = uWorld.z;",
      "  col = mix(col, col * col * (3.0 - 2.0 * col), 0.16 * lean);",
      "  vec2  fp = vec2((n.x - 0.5) * af, n.y - 0.5);",
      "  float vg = length(fp * vec2(0.86, 1.0));",
      "  col *= 1.0 - 0.34 * lean * smoothstep(0.30, 0.95, vg);",
      "  col *= uWorld.y;",
      "  float dth = (fract(sin(dot(gl_FragCoord.xy, vec2(12.9898, 78.233))) * 43758.5453) - 0.5) / 255.0;",
      "  col += dth * lean;",
      // THE JUDGES' OWN FRAME: the warp field itself. Red is how far out of the frame's own middle
      // this point reads, green and blue are the point of the departing source it lands on, so a row
      // reads the field off the picture instead of trusting a number. It carries no coverage of its
      // own because what it is for is to be read as colour.
      "  vec3 judge = vec3(clamp(rr, 0.0, 1.0), uva.x, uva.y);",
      "  col = mix(col, judge, uMask);",
      // THE COVERAGE: the alpha is the constant 1, and it is a decision rather than a default. The
      // warp field maps every point of the frame onto a point of a source and the sources are clamped
      // at their own edges, so this instrument has no absence to publish and stands as the ground a
      // stack is laid on.
      "  gl_FragColor = vec4(col, 1.0);",
      "}",
    ].join("\n");

    function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
    function clamp01(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }
    // hero.js:200 — the module's own smoothstep, spelled the module's way.
    function ss(a, b, x) { var t = clamp01((x - a) / (b - a)); return t * t * (3 - 2 * t); }
    function mix(a, b, t) { return a + (b - a) * t; }
    // hero.js:202-206 — a bump that is nothing outside its own window.
    function bump(x, a, b) {
      var t = (x - a) / (b - a);
      if (t <= 0 || t >= 1) return 0;
      return Math.pow(Math.sin(Math.PI * t), 1.4);
    }

    /* THE STORY'S TWO PLACES, and both are the module's own read off its own ramps (hero.js:421-431).
       WINDOW is where the rose window stands widest: the fourth mirror's ramp `ss(0.38, 0.54, s)` is
       full there and the unwinding `ss(0.50, 0.64, s)` has taken only a sixth of it back. SPAN is the
       small planet, and the module names it in its own words as «the last place in the story where a
       picture still STANDS» — past it the page's own scroll carries the planet down out of the frame,
       and that ramp does not exist inside a crossing. The pair's own polar reading places the far end
       of the arc between the two. */
    var STORY_WINDOW = 0.54;
    var STORY_SPAN = 0.80;

    /* THE MODULE'S OWN MEASURED RESPONSE CURVE (hero.js:338-362, DARKROOM-DRAFT D2, his word of
       08-08 17:57): equal movements of the hand produce equal felt change. A two-piece exponential
       hinged at the MEDIAN of the felt change — c = 0.61 is that median, measured by walking the raw
       dial in steps of 0.02 and reading the mean channel distance between neighbouring frames — with
       k1 = 0.4 below the knee and k2 = 1.4 above, and a dead band of 0.02 at the near end where the
       frame does not move at all. Carried digit for digit and applied where the module applies it, so
       that one number handed to this instrument and to the module puts both at one pose. */
    var FEEL_D0 = 0.02, FEEL_C = 0.61, FEEL_K1 = 0.4, FEEL_K2 = 1.4;
    function feelLog(x, k) {
      return Math.abs(k) < 1e-6 ? x : (Math.exp(k * x) - 1) / (Math.exp(k) - 1);
    }
    function feel(u) {
      var f = u <= 0.5 ? FEEL_C * feelLog(2 * u, FEEL_K1)
                       : FEEL_C + (1 - FEEL_C) * feelLog(2 * u - 1, FEEL_K2);
      return FEEL_D0 + (1 - FEEL_D0) * f;
    }

    /* THE DEAD BAND AT EITHER END OF THE HAND, and it is the module's own number read onto this
       instrument's dial. Over the first and last two hundredths of the hand the frame stands exactly
       at its door. It is not the whole of what makes a landing exact — the story's own ramps do most
       of it, and the frame is the photograph untouched for the first seven-odd hundredths of the hand
       because `lean` does not leave nothing until s passes 0.03 — but it is what makes the two ends
       of the dial flat rather than merely slow. */
    var DIAL_D0 = 0.02;

    /* WHERE THE ARRIVING WORK COMES IN, as a share of the outward leg. The module changes its third
       picture over s in [0.62, 0.80] while the planet forms (hero.js:471), and that is the one place
       on this road where neither work is legible. Said here as a fraction of the story rather than as
       an absolute place, because the far end of the arc is the pair's own reading and the change has
       to arrive whatever that reading is: at `planet` = 1 the two are the same window. */
    var CHANGE_FROM = 0.62 / STORY_SPAN;
    var CHANGE_TO = 1.0;

    /* HOW MUCH OF THE PICTURE THE FRAME SPANS AT A DOOR, and how far the frame pulls back once the
       folds have taken the picture over (hero.js:447). The sources are square and the frame opens on
       almost the whole photograph. A door is therefore the source cover-fitted and centre-cropped by
       the reciprocal of the first of these, which is what the `framings` block publishes. */
    var CROP_0 = 0.94, CROP_PULL = 0.34;

    /* WHERE THE RING MIRROR STANDS when a work carries no ring device of its own (hero.js:488), in
       frame-height units, and how far it breathes about that place. Where the work does carry one the
       mirror moves onto the work's own nearest ring — see the `course` handle. */
    var RING_REST = 0.34, RING_BREATH = 0.02;

    /* THE FLOOR THAT STOOD HERE IS GONE (2026-08-18, at the merge). `FOLD_FLOOR = 0.5` decided
       whether the window opened to the work's own count or to the module's own four folds, and its
       whole justification was that it was the composer's own DEVICE_LEGIBLE. That number has since
       been struck out of `pass-composer.js` under his word of 09:53 — a measurement ranks and never
       admits — so the floor's one source no longer stands, and a number nobody measured whose reason
       has been withdrawn is exactly what his 08:47 word strikes.

       What replaces it is the confidence itself, carrying the count. `foldsOf` below travels the
       window between the module's own four folds and the pair's own measured order in proportion to
       how confidently that order reads. Both ends the floor had are kept exactly: a confidence of
       nothing lands on the module's own four folds, a whole one on the work's own count. What goes
       is the cliff between them, where a work reading 0.49 and one reading 0.51 were cut at
       different orders on a reading that differs by a fiftieth. */

    /* THE MODULE'S OWN BREATH, at its own rates (hero.js:410-411, :447, :451-452, :488): the wander
       that carries the fold's centre about the frame, the crop's own sway, the sample point's two
       sways and the ring's. Every one of them is a pure function of the second the host hands down,
       so a scored run repeats to the point, and every one of them rides `lean` so a door is exact. */
    var WANDER_X = 0.16, WANDER_Y = 0.12;

    // ---- the grid one frame is drawn on ------------------------------------------------------------
    // The buffer the host is about to bind as `resolution`, with the CSS frame where it hands none and
    // a square where it hands neither. The frame's own ratio decides the planet's radius, the sample
    // point's own narrow-frame reading and where the measured centre stands, so the reading names
    // which of the two it read.
    function gridOf(st) {
      var bw = Math.round(st.bufWidth), bh = Math.round(st.bufHeight);
      if (bw >= 1 && bh >= 1) return { w: bw, h: bh, drawn: true, given: true };
      var cw = Math.round(st.cssWidth), ch = Math.round(st.cssHeight);
      if (cw >= 1 && ch >= 1) return { w: cw, h: ch, drawn: false, given: true };
      return { w: 1, h: 1, drawn: false, given: false };
    }

    // Cover-fit a work into the frame, and nothing beyond it: the same fit the host binds as
    // `fitA`/`fitB`, spelled here because the pose's own geometry reads it too.
    function fit(iw, ih, w, h) {
      var fa = w / Math.max(h, 1);
      var ia = iw / Math.max(ih, 1);
      if (ia > fa) return [fa / ia, 1, 0, 0];
      return [1, ia / fa, 0, 0];
    }

    // ---- HOW MANY WEDGES THE WINDOW OPENS TO, AND WHOSE NUMBER THAT IS ------------------------------
    // The rose window is four successive mirrors and its depth is a COUNT: two wedges, four, eight,
    // sixteen. That is a number the works themselves carry — `structure.rotational.n`, the order of a
    // work's own turn — and his 19:13 word lifted to the class at 19:21 asks every geometric parameter
    // to read one. So the window opens to the departing pair's own measured order, snapped onto the
    // module's own ladder, and the mirrors past that order do not play at all.
    //
    // BELOW THE FLOOR THE MODULE'S OWN FOUR FOLDS STAND, and the reading says so. A work whose turn
    // reads at less than a confidence has no order for a window to be cut at, and putting one there
    // would be passing a made-up number off as the work's own — the same shape the box's crease
    // answers with, and for the same reason.
    function foldsOf(st) {
      var score = typeof st.foldsScore === "number" ? clamp01(st.foldsScore) : 0;
      var asked = typeof st.folds === "number" ? st.folds : 4;
      var lvl = Math.round(4 + (clamp(asked, 1, 4) - 4) * score);
      return { level: lvl, wedges: Math.pow(2, lvl), score: score, measured: score > 0,
               from: score > 0
                 ? "the pair's own measured order of turn, carried " + score.toFixed(2)
                   + " of the way from the module's own four folds by the confidence it reads at"
                 : "the module's own four folds — the pair's turn carries no confidence at all" };
    }

    // ---- WHERE THE RING MIRROR STANDS, AND WHOSE NUMBER THAT IS -------------------------------------
    // The mirror across a ring is what turns the wedges into a window with COURSES, and a course is a
    // ring. Where a work was cut as rings its own step is measured — `structure.ownDevice.stepPx` over
    // its own frame side — and the mirror then stands on one of the work's own rings: the one nearest
    // the module's own resting radius, so the course the window is built on is the work's course and
    // not a radius this file typed. Where no ring step was measured the handle rests at nothing, the
    // module's own radius stands, and the reading says which of the two it is.
    function courseOf(st) {
      var step = typeof st.course === "number" ? clamp(st.course, 0, 0.5) : 0;
      if (step > 1e-4) {
        var k = Math.max(1, Math.round(RING_REST / step));
        return { at: k * step, step: step, ring: k, measured: true,
                 from: "the work's own measured ring step" };
      }
      return { at: RING_REST, step: 0, ring: 0, measured: false,
               from: "the module's own resting radius — no ring step was measured" };
    }

    // ---- the numbers of one frame ------------------------------------------------------------------
    // Everything the shader gets beyond the seating of the two works is a pure function of the pose,
    // and every number in the pose comes from a handle a score can drive. The one clock this
    // instrument reads is the second the host hands down through `clock`, exactly as the module reads
    // a handed second: nothing here counts a clock of its own, so a scored frame is a pure function of
    // the dial and the second and repeats to the point.
    function posed(st) {
      var u = clamp01(st.mix);
      var t = typeof st.clock === "number" && isFinite(st.clock) ? st.clock : 0;
      var grid = gridOf(st);
      var af = grid.w / Math.max(grid.h, 1);

      // THE ARC. The dial's own dead bands come off first, then the module's own there-and-back walk,
      // then the module's own measured response curve, then the far end the pair's polar reading
      // places. `dialOut` is the same walk taken as though the arc never turned back, and it is what
      // the picture change rides, so the change arrives whatever the far end is.
      var x = clamp01((u - DIAL_D0) / (1 - 2 * DIAL_D0));
      var tri = x <= 0.5 ? x * 2 : (1 - x) * 2;
      var dial = tri * tri * (3 - 2 * tri);
      var out = Math.min(x * 2, 1);
      var dialOut = out * out * (3 - 2 * out);
      var far = mix(STORY_WINDOW, STORY_SPAN, clamp01(typeof st.planet === "number" ? st.planet : 1));
      var s = far * feel(dial);
      var m = ss(CHANGE_FROM, CHANGE_TO, feel(dialOut));

      // THE FOUR MIRRORS, arriving and unwinding on the module's own ramps (hero.js:421-426), with
      // every mirror past the pair's own measured order left out of the window entirely.
      var fold = foldsOf(st);
      var f1 = ss(0.05, 0.26, s);
      var f2 = ss(0.24, 0.42, s);
      var f3 = ss(0.30, 0.47, s);
      var f4 = ss(0.38, 0.54, s) * 0.88;
      var o3 = ss(0.50, 0.64, s), o2 = ss(0.55, 0.70, s), o1 = ss(0.60, 0.80, s);
      f4 *= (1 - o3); f3 *= (1 - o3); f2 *= (1 - o2); f1 *= (1 - o1);
      if (fold.level < 4) f4 = 0;
      if (fold.level < 3) f3 = 0;
      if (fold.level < 2) f2 = 0;

      var planet = ss(0.54, 0.80, s);
      var ring = ss(0.34, 0.50, s) * 0.55 * (1 - ss(0.50, 0.66, s));
      var disc = ss(0.70, 0.96, s);
      // THE DOOR GATE. The module's own «the towers stand straight until the first fold» — a tilted
      // building reads as a mistake — and this port asks one more thing of it: every wander, every
      // breath and every colour this instrument lays over the photograph rides it, so at a door the
      // frame is the work its source carries and nothing has been done to it.
      var lean = ss(0.03, 0.22, s);

      // THE TURN THE STORY CARRIES (hero.js:438-444). Under a handed second the accumulation is that
      // second times the rate the story's own position asks for — the same integral the module's free
      // walk builds up, in closed form, so a scored frame repeats to the point.
      var turn = clamp01(typeof st.turn === "number" ? st.turn : 1);
      var px = 0.5 + WANDER_X * Math.sin(t * 0.21);
      var py = 0.5 + WANDER_Y * Math.sin(t * 0.157 + 1.3);
      var spinPh = t * (0.018 * f1 + 0.055 * planet);
      var spin = (spinPh + (px - 0.5) * 0.30 * lean + 0.25 * ss(0.30, 0.80, s)) * turn;
      var twirl = 1.5 * bump(s, 0.46, 0.78) * turn;

      // THE FRAME'S OWN READING OF THE PICTURE (hero.js:447-452). The crop opens on almost the whole
      // photograph and pulls back once the folds have taken it over; a narrow frame keeps the full
      // height of a square source and takes a column out of it, and the sample point comes to the
      // middle as the story opens.
      var crop = (CROP_0 + CROP_PULL * ss(0.02, 0.52, s)) * (1 + 0.010 * Math.sin(t * 0.19) * lean);
      var narrow = 1 - clamp01((af - 0.60) / 0.75);
      var open = ss(0.02, 0.50, s);
      var base = mix(mix(0.54, 0.50, narrow), 0.50, open);
      var samx = 0.50 + 0.010 * Math.sin(t * 0.11) * lean;
      var samy = 0.50 + (base - 0.50) * lean + 0.008 * Math.cos(t * 0.083) * lean;

      // WHERE THE FOLDS TURN, AND WHOSE PLACE IT IS. The module let a visitor's pointer steer the
      // centre; a crossing has no visitor's hand on it, and the place the folds belong is the point of
      // the picture the collection already measures — `structure.radial.centre`, which arrives as
      // `centreX`/`centreY`. That point is carried into the frame through the door's own framing, so
      // the folds turn about the very place of the photograph the measurement names, standing where
      // that place stands in the frame. The module's own «off to one side» constant is what it wrote
      // for want of such a measurement and it is not carried; its wander is, at its own rates.
      // THE SEATING IS THE HOST'S OWN ANSWER, not a second guess at it. Since 2026-08-17 the host
      // hands both works' seating on the very buffer it is about to bind (`fitA`/`fitB` on the frame
      // state, computed by the same function the draw calls), so the script and the shader work from
      // ONE seating. Where none arrives — a bench posing this instrument by hand — the plain cover
      // fit of the sizes the pose carries stands instead.
      var fA = st.fitA || fit(st.aw || 1, st.ah || 1, grid.w, grid.h);
      var fB = st.fitB || fit(st.bw || 1, st.bh || 1, grid.w, grid.h);
      var cx = clamp01(typeof st.centreX === "number" ? st.centreX : 0.5);
      var cy = clamp01(typeof st.centreY === "number" ? st.centreY : 0.5);
      var cxF = clamp((cx - 0.5) * af / Math.max(fA[0] * CROP_0, 1e-6), -af / 2, af / 2);
      var cyF = clamp((0.5 - cy) / Math.max(fA[1] * CROP_0, 1e-6), -0.5, 0.5);
      var cenx = (cxF + (px - 0.5) * 0.20) * lean;
      var ceny = (cyF + (0.5 - py) * 0.15) * lean;

      // THE PLANET, and how far the world stands back from the eye (hero.js:472-476). A scored layer
      // has the WHOLE frame — there is no scrolled-away strip inside a crossing — so the pull-back is
      // read against the frame entire, which is the module's own repair of the bead in an empty dark.
      var Rp = 0.36 * Math.min(1, Math.max(0.55, af));
      var scale = 1 + (Math.min(8, Math.max(1, Rp / RING_REST)) - 1) * ss(0.46, 0.86, s);
      var dim = 1 + 0.85 * ss(0.48, 0.86, s);
      var course = courseOf(st);

      return {
        cen: [cenx, ceny],
        sam: [samx, 1 - samy],
        fold: [f1, f2, f3, f4],
        warp: [crop, ring, course.at + RING_BREATH * Math.sin(t * 0.23) * lean, planet],
        sky: [Rp, spin, twirl, disc],
        world: [scale, dim, lean, m],
        mask: clamp01(typeof st.mask === "number" ? st.mask : 0),
        // read on the diagnostic surface, bound to no uniform: where the hand came to, what the story
        // is doing there, and the two numbers the works themselves own
        hand: u, story: s, storyFar: far, dial: dial, change: m, lean: lean,
        wedges: fold.wedges, foldLevel: fold.level, foldScore: fold.score,
        foldMeasured: fold.measured, foldFrom: fold.from,
        courseAt: course.at, courseStep: course.step, courseRing: course.ring,
        courseMeasured: course.measured, courseFrom: course.from,
        centreAt: [cx, cy], centreInFrame: [cxF, cyF],
        crop: crop, planetRadius: Rp, spin: spin, twirl: twirl, scale: scale,
        fitA: fA, fitB: fB, grid: grid, aspect: af,
      };
    }

    // ---- THE DOOR THE INSTRUMENT READS FOR ITSELF --------------------------------------------------
    // His 18:00 architecture decision, carried in the U27 brief: the instrument reads its doors at
    // runtime on the actual buffer, and the report it hands back is the runtime truth; what the
    // manifest declares is only the claim. The meshing instrument answered that first, the unfold
    // instrument reads its own panel map and the box its own two faces; this is the same law read in
    // this instrument's own unit, which is THE WARP FIELD.
    //
    // WHAT A DOOR ASKS OF A WARP FIELD. At either door the field is the identity: no fold has reached
    // any radius, no ring is mirrored, nothing has poured into polar, the frame's own middle is where
    // the folds turn, the sample point is the picture's own middle and the crop rests at its own
    // number. Then and only then is the frame the source cover-fitted and centre-cropped by the crop
    // the `framings` block publishes. This reading does not declare that — it walks the buffer the
    // host is about to bind, maps each of its sample points through the pose the shader is about to be
    // handed, maps the same point through the DOOR's own framing, and reports the greatest distance
    // between the two in points of that buffer.
    //
    // THE DOOR'S OWN FRAMING IS WRITTEN FROM FIRST PRINCIPLES and not taken from the pose above, on
    // purpose: a reference computed by the same arithmetic it is checking would agree with a broken
    // landing as readily as with a whole one.
    //
    // AND THE COLOUR IS READ TOO, in one number. Every colour this instrument lays over a photograph —
    // the soft clip, the vignette, the dither — rides `lean`, so `lean` at a door is the whole of that
    // question, and a door where it stands above nothing is a door where the frame is the work with
    // something done to it.
    //
    // THERE IS NOTHING HERE TO HOLD. The landing is exact by construction rather than by a tolerance:
    // the dial's dead band spends the hand, every ramp of the story is a smoothstep at its own zero
    // and every wander is multiplied by a gate that is exactly nothing there. So anything this reading
    // finds is a real fault that no widening closes, and the refusal stands alone; `held` is always
    // nothing and it says so rather than carrying a guard that could never fire.
    var DOOR_SLIP = 0.5;    // points of the grid: half a point, inside which a sample cannot move
    // How much of the judges' channel may stand in the frame at a door and it still BE the photograph:
    // half a level of 255, an eighth of the charter's own door bar of 6 of 255 at one point.
    var DOOR_SHOW = 0.5 / 255;

    // WHERE ONE POINT OF THE FRAME FALLS ON THE DEPARTING SOURCE, under the pose the shader is about
    // to be handed. FRAG's own `uvOf`, carried here so the reading walks the very field the shader
    // draws rather than a description of it.
    function uvAt(v, f, qx, qy) {
      var dx = (qx - v.cen[0]) * v.world[0], dy = (qy - v.cen[1]) * v.world[0];
      var r = Math.sqrt(dx * dx + dy * dy);
      var a = Math.atan2(dx, dy) + v.sky[1] + v.sky[2] * Math.exp(-r * 2.4);
      a = ((a + Math.PI) % (2 * Math.PI) + 2 * Math.PI) % (2 * Math.PI) - Math.PI;
      var A = a, i, axis = [0, 0.5 * Math.PI, 0.25 * Math.PI, 0.125 * Math.PI];
      var sgn = [1, -1, -1, -1];
      var fw = 5.0 / (v.grid.h / Math.max(v.world[0], 1e-6));
      for (i = 0; i < 4; i++) {
        var amt = v.fold[i];
        if (amt <= 0.002) continue;
        var tt = (A - axis[i]) * sgn[i];
        var side = tt <= 0 ? 1 : 0;
        var front = amt * 1.45;
        var k = side * (1 - ss(front - fw, front + fw, r));
        A = A + (2 * axis[i] - 2 * A) * k;
      }
      var rt = v.warp[2] - r;
      var rw = 7.0 / (v.grid.h / Math.max(v.world[0], 1e-6));
      var rk = (v.warp[1] > 0.001 && rt <= 0)
        ? (1 - ss(v.warp[1] * 0.34 - rw, v.warp[1] * 0.34 + rw, -rt)) : 0;
      var rr = Math.max(r + (2 * v.warp[2] - 2 * r) * rk, 0);
      var ddx = Math.sin(A) * rr, ddy = Math.cos(A) * rr;
      var uax = v.sam[0] + (ddx / v.aspect) * f[0] * v.warp[0];
      var uay = v.sam[1] - ddy * f[1] * v.warp[0];
      var vr = rr / Math.max(v.sky[0], 1e-5);
      var ubx = A / (2 * Math.PI) + 0.5, uby = 1 - Math.pow(Math.min(vr, 1), 1.45);
      return [clamp(mix(uax, ubx, v.warp[3]), 0.0008, 0.9992),
              clamp(mix(uay, uby, v.warp[3]), 0.0008, 0.9992)];
    }

    // THE FIELD, READ ON THE BUFFER THE SHADER WILL SAMPLE ON. The walk takes the buffer's own sample
    // points: its four corners, where a fold reaches last and the crop has the least to spare; the
    // midpoints of its four edges; and the nine points around its centre, where every mirror's crease
    // and the planet's own middle stand.
    function fieldReadOf(v, W, H) {
      var af = W / Math.max(H, 1);
      var f = v.fitA, worst = 0, walked = 0, i, j;
      function walk(pxi, pyi) {
        var qx = (pxi / W - 0.5) * af, qy = 0.5 - pyi / H;
        var got = uvAt(v, f, qx, qy);
        // the door's own framing, written from first principles: the plain cover fit about the
        // picture's own middle, cropped by the crop the `framings` block publishes
        var wx = 0.5 + (qx / af) * f[0] * CROP_0;
        var wy = 0.5 - qy * f[1] * CROP_0;
        // the departure, carried back into the frame's own units so it can be counted in points
        var ex = (got[0] - wx) / Math.max(f[0] * CROP_0, 1e-6) * af;
        var ey = (got[1] - wy) / Math.max(f[1] * CROP_0, 1e-6);
        worst = Math.max(worst, Math.sqrt(ex * ex + ey * ey) * H / 2);
        walked++;
      }
      for (i = 0; i < 2; i++) {
        for (j = 0; j < 2; j++) { walk(i ? W - 0.5 : 0.5, j ? H - 0.5 : 0.5); }
      }
      walk(0.5, H * 0.5); walk(W - 0.5, H * 0.5); walk(W * 0.5, 0.5); walk(W * 0.5, H - 0.5);
      for (i = -1; i <= 1; i++) {
        for (j = -1; j <= 1; j++) { walk(W * 0.5 + i, H * 0.5 + j); }
      }
      return { walked: walked, offPx: worst, lean: v.world[2], mask: v.mask };
    }

    // THE DOOR, MEASURED. Null everywhere but at a door, since away from the doors a folding frame is
    // the picture rather than a fault. The door is named by the manifest's own `doors` block: `mix` at
    // 0 is the entry door, where the frame is the departing work whole, and `mix` at 1 the exit door,
    // where it is the arriving one.
    function doorReadOf(v, st) {
      var want = st.mix === 0 ? 1 : (st.mix === 1 ? 0 : -1);
      if (want < 0) return null;
      var g = v.grid;
      if (!g.given) return null;
      var read = fieldReadOf(v, g.w, g.h);
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
      if (read.offPx >= DOOR_SLIP) {
        return door + " door leaks: the warp field carries a point of the frame "
             + read.offPx.toFixed(2) + " points" + where + " away from where the door's own framing "
             + "puts it, so the frame is the " + work + " work folded, mirrored or poured into its "
             + "own polar reading, where " + door + " door's own law asks for that work standing "
             + "whole at every point";
      }
      if (read.lean > 0) {
        return door + " door leaks: the frame stands " + read.lean.toFixed(6) + " out of its own "
             + "door, so the soft clip, the vignette and the dither are laid over the " + work
             + " work, where " + door + " door's own law asks for that work and nothing done to it";
      }
      if (read.mask >= DOOR_SHOW) {
        return door + " door leaks: the judges' own channel stands at " + read.mask.toFixed(6)
             + ", so the frame draws the warp field over a " + g.w + " x " + g.h
             + (g.drawn ? " buffer" : " frame") + " instead of the " + work + " work, where " + door
             + " door's own law asks for the " + work + " work at every point";
      }
      return null;
    }

    // THE NUMBERS OF ONE FRAME, WITH ITS DOOR READ ON THE BUFFER BEING DRAWN. Away from a door this is
    // `posed` and nothing more: the reading is taken nowhere else. At a door it walks its own field
    // over the buffer and publishes what it read.
    function values(st) {
      var v = posed(st);
      var read = doorReadOf(v, st);
      v.doorGrid = read ? read.grid : null;
      v.fieldMap = read ? { walked: read.walked, offPx: read.offPx, lean: read.lean } : null;
      v.doorHeld = null;
      v.doorWhyNo = doorWhyNoOf(read);
      return v;
    }

    // ONE TRAVELLING NUMBER, read on the diagnostic surface: how far out along the story the frame
    // stands, where 1 is the far end of the arc. The entry, the deepest place and the exit are the
    // shape of its response.
    function feelOf(u) {
      var x = clamp01((clamp01(u) - DIAL_D0) / (1 - 2 * DIAL_D0));
      var tri = x <= 0.5 ? x * 2 : (1 - x) * 2;
      return feel(tri * tri * (3 - 2 * tri));
    }

    var manifest = {
      id: "hero", api: 1, arity: 2,
      // The departing work comes apart into its own mirrors, the window and the planet are a place
      // where neither work is legible, and the arriving work is put back together on the same road.
      roles: ["disassembly", "mystery", "assembly"],
      // WHERE THIS STANDS ON THE CHARTER'S SHELF, and the reading is said to be derived. The module
      // carries no row in lab/data/module-contract.json — it postdates that table — so its level is
      // read off the two devices its own middle is built out of, both of which the charter's
      // vocabulary table does carry.
      //   · SURFACE — the whole frame is one warp field. The rose window is `kaleidoscope`, which
      //     that table gives SURFACE; the polar reading is `planet`, which it gives SURFACE too.
      //   · CELL — the wedges. Between the mirrors and the unwinding the frame is partitioned into
      //     the window's own wedges and courses, each carrying its own reflection of a work.
      // WORLD IS NOT CLAIMED, and that is a decision. This instrument carries no camera and no
      // projection — `camera: { needs: "none" }` — and the charter's own table puts the planet at
      // SURFACE rather than at a folded space. Claiming WORLD would spend a crossing's one miracle
      // and bar this instrument from every quiet link, entrance and return on a route, which is where
      // a ground instrument is most wanted. TEXTURE and LIGHT-COLOUR are not claimed either: the
      // light this instrument adds is the planet's own sky and rim, which belong to the reading
      // rather than to a field laid over one.
      levels: ["SURFACE", "CELL"],
      params: { folds: [1, 4], planet: [0, 1], turn: [0, 1], course: [0, 0.5] },
      // EVERY handle a score can drive (§4.4b). `mix` is the dial and `clock` the second the host
      // hands down; the pair's own measured radial centre places the folds; its measured order of
      // turn cuts the window; its polar reading places the far end of the arc; its radial score
      // carries the turn; its ring step places the courses; and `mask` is the judges' channel.
      //
      // NO `seed` HANDLE, AND THAT IS A DECISION. Nothing in this picture is rolled: the module holds
      // no die, and every number of every frame is a function of the dial and the second. A handle a
      // score can walk without moving the picture is noise in the score, so none is published, and a
      // seeded run repeats to the point for the same reason.
      handles: {
        mix: { min: 0, max: 1, def: 0 },
        clock: { min: 0, max: 3600, def: 0, unit: "seconds",
                 applied: { carries: "the wander of the fold's centre, the crop's own sway, the "
                                   + "sample point's two sways, the ring's breath and the turn the "
                                   + "story accumulates",
                            restsAt: "every door, where each of them is multiplied by nothing" } },
        centreX: { min: 0, max: 1, def: 0.5,
                   unit: "where along the picture's own width the folds turn",
                   reads: "structure.radial.centre — the place lab/step1 measures a work's own radial "
                        + "reading about, taken as the midpoint of the two works' own centres, which "
                        + "is the same measurement the meshing instrument's own centre reads. The "
                        + "module let a visitor's pointer steer this place; a crossing has no hand on "
                        + "it and the work's own measured centre is where the folds belong" },
        centreY: { min: 0, max: 1, def: 0.5,
                   unit: "where down the picture's own height the folds turn",
                   reads: "structure.radial.centre, the same measurement read on the other axis" },
        folds: { min: 1, max: 4, def: 4, kind: "enum", step: 1,
                 names: { "1": "two wedges", "2": "four wedges", "3": "eight wedges",
                          "4": "sixteen wedges" },
                 unit: "how many of the four mirrors the window opens",
                 reads: "structure.rotational.n, the order of the pair's own measured turn, read onto "
                      + "the module's own ladder of two, four, eight and sixteen wedges, so the "
                      + "window is cut at the count the works themselves carry",
                 applied: { atNoConfidence: "the module's own four folds" } },
        foldsScore: { min: 0, max: 1, def: 0,
                      unit: "how confidently that order of turn reads",
                      reads: "structure.rotational.score, which CARRIES the count: the window "
                           + "travels between the module's own four folds and the pair's own order "
                           + "in proportion to how confidently that order reads, so a reading of "
                           + "nothing lands on the module's own folds and a whole one on the work's",
                      applied: { atNothing: "the module's own four folds",
                                 atWhole: "the pair's own measured order of turn" } },
        planet: { min: 0, max: 1, def: 1,
                  unit: "how far out along the story the arc travels",
                  reads: "structure.polar.planet, the collection's own measurement of how strongly a "
                       + "work reads as a planet. It places the far end of the arc between the rose "
                       + "window standing widest and the small planet, so a pair that reads nothing "
                       + "polar turns back at the window and one that reads it goes all the way",
                  applied: { atNothing: STORY_WINDOW, atWhole: STORY_SPAN } },
        turn: { min: 0, max: 1, def: 1,
                unit: "how far the window turns as it opens",
                reads: "each work's own measured radial score, so a work whose rings are its own "
                     + "device drives the turn and one that barely reads radial barely turns — the "
                     + "same measurement and the same reasoning the meshing instrument's own turn "
                     + "reads",
                applied: { restsAt: "every door" } },
        course: { min: 0, max: 0.5, def: 0,
                  unit: "the work's own ring step, as a fraction of its frame side",
                  reads: "structure.ownDevice.stepPx over the work's own frame side, where that "
                       + "device is rings — the step the work was actually cut at. The ring mirror "
                       + "then stands on the work's own ring nearest the module's resting radius, so "
                       + "the course the window is built on is the work's course",
                  applied: { restsAt: RING_REST, breath: RING_BREATH } },
        // THE MEASUREMENT THIS HANDLE IS READ AGAINST AT A DOOR. `readAtADoor` says what is read
        // (this instrument's own warp field, walked at the buffer's own sample points), on which grid
        // (the drawing buffer the host binds, with the CSS frame where it hands none), what the
        // reading is counted in, and that there is no hold.
        mask: { min: 0, max: 1, def: 0,
                applied: { readAtADoor: { points: DOOR_SLIP, readOn: "the drawing buffer",
                                          reads: "landing",
                                          measures: "this instrument's own warp field, walked at the "
                                                  + "buffer's own sample points against the door's "
                                                  + "own framing, and the gate every colour it lays "
                                                  + "over a photograph rides",
                                          held: null } } },
      },
      neutrals: { a: 0, b: 1 },
      doors: { in: { handle: "mix", value: 0, work: "a" },
               out: { handle: "mix", value: 1, work: "b" } },
      // BOTH DOORS FRAME ALIKE. The module opens on almost the whole photograph and pulls back only
      // once the folds have taken it over, so a door is the source cover-fitted and centre-cropped by
      // the reciprocal of the crop it rests at. That is the module's own number and it is published
      // here rather than left for the frame to reveal.
      framings: { "0": { coverCrop: 1 / CROP_0 }, "1": { coverCrop: 1 / CROP_0 } },
      drivers: ["progress", "cueProgress", "time", "velocity", "capability", "noise", "static",
                "curve", "spline", "map", "add", "multiply", "mix", "clamp", "hold", "segment",
                "ramp", "slew", "oscillate", "node"],
      camera: { needs: "none", authority: "stage" },
      // THE PICTURE'S OWN CHAIN OF SMALLER COPIES, asked for by §8's `gl.readsChain`. The module
      // uploads its own with a full chain and reads every point twice, once sharp for brightness
      // and once blurred for colour; the host built no chain, so both reads were inert here and
      // the port carries neither rather than shipping dead arithmetic. What it lost is real: the
      // planet aliases at its rim. The flag asks the host for the chain, which is what closes it.
      gl: { preserveDrawingBuffer: false, readsChain: true },
      // WHAT THIS INSTRUMENT WRITES WHERE ITS OWN MATTER IS ABSENT (§7's coverage law, and the
      // per-instrument specification in docs/design/COVERAGE.md). It is absent nowhere.
      coverage: { writes: false,
                  how: "the warp field is a total map from every point of the frame onto a point of "
                     + "a source — a fold, a mirror across a ring and a polar reading are each "
                     + "defined at every point — and the host's sources are clamped at their own "
                     + "edges, so every point of the frame carries a photograph and the alpha is the "
                     + "constant 1; where the planet stands, the frame past its rim carries the sky "
                     + "this instrument draws there, which is a colour and not an absence" },
      // The neutral pose is the ENTRY DOOR — `mix` at 0, the value the `doors` block above names — so
      // the frame keys the host reads off it at registration include the door's own record.
      neutralPose: { mix: 0, clock: 0, centreX: 0.5, centreY: 0.5, folds: 4, foldsScore: 0,
                     planet: 1, turn: 1, course: 0, mask: 0,
                     reduced: false, cssWidth: 1000, cssHeight: 1000 },
      passes: [{
        program: "hero", vert: VERT, frag: FRAG, position: "aPos",
        uniforms: [
          { name: "uA", type: "sampler2D", source: "textureA" },
          { name: "uB", type: "sampler2D", source: "textureB" },
          { name: "uFitA", type: "vec4", source: "fitA" },
          { name: "uFitB", type: "vec4", source: "fitB" },
          { name: "uRes", type: "vec2", source: "resolution" },
          { name: "uCen", type: "vec2", source: "frame:cen" },
          { name: "uSam", type: "vec2", source: "frame:sam" },
          { name: "uFold", type: "vec4", source: "frame:fold" },
          { name: "uWarp", type: "vec4", source: "frame:warp" },
          { name: "uSky", type: "vec4", source: "frame:sky" },
          { name: "uWorld", type: "vec4", source: "frame:world" },
          { name: "uMask", type: "float", source: "handle:mask" },
        ],
      }],
      // The instrument allocates nothing of its own: it spends the two source-texture slots the host
      // already holds and the one programme the host builds from this manifest. The module's own
      // canvas, its context, its three textures with their mipmap chains and its own frame loop are
      // what this port does without.
      resources: { lean: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                           passes: 1, bytesEstimate: 0, variant: "lean" },
                   standard: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0,
                               programs: 1, passes: 1, bytesEstimate: 0, variant: "standard" },
                   rich: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                           passes: 1, bytesEstimate: 0, variant: "rich" } },
      capabilities: ["webgl2"],
      decline: ["one work only", "a source that never decoded"],
      provenance: { labPath: "lab/effects/hero.js", commit: "2afa485",
                    sha256: "ef455f09b98f6758753703eb3da1cf752e2b7898488cb19aad2fad6aa1eb43b1" },
      readiness: "production-ready",
    };

    var live = false;
    return {
      name: "hero",
      manifest: manifest,
      values: values,
      fit: fit,
      feel: feelOf,
      prepare: function (o) {
        if (!o.sources) return { take: false, why: "the fold-window-planet instrument needs both works" };
        if (!o.cue) return { take: false, why: "no cue names it" };
        return { take: true };
      },
      start: function () { live = true; },
      // The pose the shader draws. The module's canvas, its frame loop, its pointer and its own third
      // photograph are gone, so every number here comes from a handle a score drives or from the frame
      // the host is about to bind.
      //
      // A DOOR THIS INSTRUMENT CANNOT KEEP WHOLE IS REFUSED RATHER THAN DRAWN. At either door it walks
      // its own warp field over the buffer the host is about to bind and, where a point of that grid
      // stands further from the door's own framing than a sample can move, where the gate every added
      // colour rides is open, or where the judges' channel is left open, it hands the host the reason
      // with the measured numbers in it instead of drawing a door that is not the photograph.
      frame: function (st) {
        if (!live) return;
        var h = st.handles;
        var pose = {
          mix: h.mix, clock: h.clock, centreX: h.centreX, centreY: h.centreY,
          folds: h.folds, foldsScore: h.foldsScore, planet: h.planet, turn: h.turn,
          course: h.course, mask: h.mask, reduced: st.reduced,
          cssWidth: st.viewport.w, cssHeight: st.viewport.h,
          // THE GRID THE SHADER WILL SAMPLE ON, carried into the pose so the geometry is built for the
          // frame the host is about to bind as `uRes` and the door is read on it rather than on the
          // CSS frame around it.
          bufWidth: st.viewport.bufferW, bufHeight: st.viewport.bufferH,
          // BOTH WORKS' SEATING ON THAT BUFFER, which only the host can answer and which it hands
          // down on the frame state. The measured centre is carried into the frame through it, so
          // the folds turn about the place of the photograph the measurement names rather than about
          // a place a cover fit was guessed at.
          fitA: st.fitA, fitB: st.fitB,
        };
        // AT A DOOR THE INSTRUMENT SAYS WHAT IT APPLIED, and says it before it refuses. `request` is
        // the travel a landing asks of the field — none — and `applied` is the travel this grid
        // actually shows, so `moved` is the two read against each other in the grid's own points.
        if (h.mix === 0 || h.mix === 1) {
          var v = values(pose);
          if (st.reportApplied) {
            st.reportApplied({
              door: h.mix === 0 ? "in" : "out",
              buffer: [pose.bufWidth, pose.bufHeight],
              reads: "landing", request: 0,
              applied: v.fieldMap ? v.fieldMap.offPx : null,
              moved: v.fieldMap ? v.fieldMap.offPx : null,
              unit: "points of the drawing buffer",
              // and the gate every colour this instrument adds rides, so a door held whole says so
              // about the light as well as about the geometry
              lean: v.fieldMap ? v.fieldMap.lean : null,
              walked: v.fieldMap ? v.fieldMap.walked : null,
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
    instrument: heroInstrument(),
  });
})();
