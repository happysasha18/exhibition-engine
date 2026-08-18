/*!pass-inst-droste.js*/
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
// OWNERSHIP. This instrument was carried over from lab/effects/droste.js. The artistic instruments
// and their manifests belong to tlvphotos, which builds these files from its own sources; the
// engine's copies are what ships until that handover lands.
(function () {
  var join = window.__@@NS@@PassInstrument;
  if (typeof join !== "function") return;

  // THIS FILE'S OWN VERSION, and the one home of that fact. The build reads this literal out of the
  // source and writes it into the site's record beside the digest, so the version a file declares
  // and the version a host was told to load cannot drift apart without the build noticing.
  var INSTRUMENT_VERSION = "1.0.0";

  // ================================================================================================
  // THE DROSTE INSTRUMENT (§8) — lab/effects/droste.js carried across
  // ================================================================================================
  // WHAT THE VISITOR SEES. The photograph opens into a smaller copy of itself, and that copy opens
  // into a smaller one again, without end. The copies do not sit square inside each other: the whole
  // picture is sheared as it goes down, so straight lines running out of the middle wind into a
  // spiral and the eye falls along it toward a dark throat. Then a ring appears at the frame's own
  // edge and travels inward: outside the ring the copies belong to the arriving work, inside it to
  // the departing one, so the picture the visitor came in on shrinks ring by ring into the throat
  // and vanishes at a point while the other photograph closes in around it. When the ring has passed
  // the middle the spiral unwinds again, and what stands flat in the frame is the arriving work.
  //
  // WHAT IT CUTS ON. RINGS. The copies are annuli about the work's own measured radial centre, the
  // handover happens on one of them, and the seam it happens across is as wide as the module's own
  // seam between two copies. This is the collection's `radial` measure, whose element kind is
  // `ring`, and this instrument fills the frame at every point, so it can stand as the GROUND a
  // stack is laid on — which the meshing instrument, the only other one that cuts on rings, cannot,
  // because it writes coverage.
  //
  // WHAT A PAIR MUST READ FOR THIS TO BE WORTH PLAYING. A spiral has a throat, and a throat has to
  // stand somewhere the photograph itself puts it. So this instrument asks that one of the two works
  // reads RADIAL over the collection's own tight floor: a picture built around a centre — concentric
  // rings, or spokes running out of one point — strongly enough that the centre is the work's own
  // device rather than an accident of framing. Rings become the copies; spokes become the spiral,
  // because the shear turns a straight spoke into one. A photograph with no centre gives the dive
  // nowhere to fall, and the crossing is better played on another instrument. The condition is
  // declared on the manifest under `asks`, in the instrument's own words, and it is answered when a
  // pair is handed over rather than swept for in advance (his word of 2026-08-18 09:01).
  //
  // WHERE IT STANDS ON THE CHARTER'S SHELF. SURFACE, and that is his own standing verdict:
  // lab/CROSSING-BRIEF.md's vocabulary table carries «droste · внутрь себя · переход + vista ·
  // SURFACE · approved; conformal-with-rotation is its named deep end». The named deep end is the
  // shear this port carries whole. Shelf 8 lists the log-spiral among the projection worlds, and a
  // world-level claim would spend the crossing's one miracle; the table is the dated verdict and the
  // table says SURFACE, so SURFACE is what the manifest declares and the tension is written down in
  // the lane's report rather than settled here.
  //
  // ------------------------------------------------------------------------------------------------
  // HOW ONE PHOTOGRAPH BECAME TWO
  // ------------------------------------------------------------------------------------------------
  // The module dives into ONE picture: its `picture` param picks the first or the second and the
  // other is never drawn. A cue of this engine carries an ordered pair and owes a door at each end,
  // so the port had to find where a second work enters a spiral without a crossfade over the frame,
  // which the charter bans as an arrival.
  //
  // IT ENTERS ON A RING, AND THE RING IS THE ONE THE MODULE ALREADY DRAWS ITS SEAM ON. At every
  // point of the frame the module reads the photograph twice — this copy and the next one in — and
  // dissolves the two across a band a fifth of a copy wide, which is what keeps the repeat from ever
  // showing. This port reads the SAME two points, of ONE work, and chooses WHICH work by the point's
  // own distance from the throat: outside the handover ring the arriving work, inside it the
  // departing one, dissolved across a band of exactly that same fifth of a copy. So the two works
  // meet on an annulus about the work's own measured centre, at a seam the module's own arithmetic
  // draws, and the frame is one picture in sharp focus at every point of the ride.
  //
  // THE RING TRAVELS ONE WAY AND COMPLETES. It comes in from beyond the frame's farthest corner and
  // leaves past the throat, so nothing retraces (the charter's ban on rotational gestures that
  // retrace) and both doors are exact by construction rather than by tolerance: at `mix` 0 the ring
  // stands outside every point of the frame and the whole frame is the departing work; at `mix` 1 it
  // has passed inside every point and the whole frame is the arriving one.
  //
  // AND IT TRAVELS WHILE THE SPIRAL STANDS OPEN. The wind — how far the photograph has wound into
  // the spiral — is nothing at both doors, whole across the middle third, and the ring's own travel
  // is confined to exactly that middle, so the works exchange INSIDE the spiral and never on the
  // flat. Three acts: the photograph winds in, the works exchange in the wound middle, the arriving
  // work unwinds onto the flat. The charter's own law is that the zero is a door and never a
  // checkpoint — an effect enters through its zero and leaves through it — and the two zeros here
  // carry different photographs, so nothing is played backwards.
  //
  // ------------------------------------------------------------------------------------------------
  // WHAT CAME OVER, AND WHAT STAYED BEHIND
  // ------------------------------------------------------------------------------------------------
  // WHAT CAME OVER, digit for digit, and the suite reads both files for each: the log-polar map and
  // its shear, the period 40 the copies are cut from, the exact derivatives that keep the sampler
  // sane across the wrap, the two-copy read and its dissolve band, the dark rim on the seam, the
  // well at the throat, the two sinks at the corners and past the frame, the finish (the gamma, the
  // bite and the lift of colour), the centre's own wander on three unaligned periods, the breathing
  // bend, the two response curves on the turn and the speed, the closed form the module answers a
  // handed second with, and the reach a named centre has.
  //
  // WHAT STAYED BEHIND: the module's own canvas and context, its frame loop, its resize observer,
  // its texture uploads and mip chain, its pointer listeners and the hand's own easing (the engine
  // parks the pointer and a scored spiral never has one settling), and its `picture` param, which a
  // pair replaces.
  //
  // THE PORT'S OWN THREE NUMBERS are the middle third the wind holds across, the share of a copy the
  // handover seam takes, and the floor under the throat — and each is stated where it stands. The
  // seam's share is the module's own dissolve width read back as a number; the floor is one point of
  // the drawing buffer, which is where a picture stops having anything to say.
  //
  // ------------------------------------------------------------------------------------------------
  // THE COVERAGE: THIS INSTRUMENT FILLS THE FRAME
  // ------------------------------------------------------------------------------------------------
  // §7's coverage law asks every instrument to say where its own matter is absent. Here it is absent
  // nowhere: the map is defined at every point of the frame and every point is written, so the alpha
  // is the constant 1 and `writes: false` is a decision rather than a default. Under the placement
  // rule (§8 as amended 14:05, and `coverageWhyNo`) that makes it lawful as the LOWEST cue of a
  // stack and as a whole one-cue score — which is the placement the ring cut wanted and had no
  // instrument for.
  function drosteInstrument() {
    var VERT = [
      "attribute vec2 aPos;",
      "void main(){ gl_Position = vec4(aPos, 0.0, 1.0); }",
    ].join("\n");

    // ----------------------------------------------------------------------------------------------
    // THE SHADER, AND THE FIVE THINGS THAT ARE NOT THE MODULE'S OWN LINES
    // ----------------------------------------------------------------------------------------------
    //   · IT IS WRITTEN IN THE LANGUAGE EVERY OTHER INSTRUMENT HERE IS WRITTEN IN, and the host
    //     stamps the version onto it (`toES3` in pass-layer.js). The module carries its own
    //     `#version 300 es` header, and a source that already has one is handed through untouched,
    //     so keeping it would have compiled too — but the fleet's own rows read these files as one
    //     fleet, in one dialect, and an instrument that speaks a second one makes every such row
    //     answer for a difference that means nothing. `textureGrad` needs the second version of the
    //     language and survives the stamping unchanged, so nothing of the map is given up for it.
    //   · THE TWO WORKS. Each of the module's two reads is taken from both sources and chosen
    //     between by the handover ring. Four fetches where the module took two; not one line of the
    //     map changed.
    //   · THE PICTURE ARRIVES ENCODED. The module uploads its own texture as `SRGB8_ALPHA8`, so its
    //     sampler hands the shader linear light. The host uploads plain `RGB` — one texture serving
    //     every instrument — so this shader undoes the file's own transfer itself, with the exact
    //     inverse of the transfer the module's own flat door encodes with. At the doors the two
    //     cancel to the file's own bytes.
    //   · THE ROWS RUN THE OTHER WAY. The module uploads with `UNPACK_FLIP_Y_WEBGL`; the host does
    //     not, so the row coordinate is turned over at the fetch, and the gradient's row with it.
    //   · THE THROAT HAS A FLOOR, and it is one point of the drawing buffer. It is used for ONE
    //     question only — which work this point carries — because below one point there is no
    //     picture to choose for, and without it the exit door would keep a disc of the departing
    //     work at the very middle where the radius runs to nothing. The geometry itself reads the
    //     unfloored radius, exactly as the module does.
    var FRAG = [
      "precision highp float;",
      "uniform sampler2D uA;",             // the work the visitor is leaving
      "uniform sampler2D uB;",             // the work arriving
      "uniform vec4 uFitA;",               // its cover fit into the frame, and its own door
      "uniform vec4 uFitB;",
      "uniform vec2 uRes;",                // the drawing buffer, in points
      "uniform vec2 uCentre;",             // the spiral's throat, 0..1 across the frame, y up
      // THE DIVE: how far along the endless fall this frame stands, the turn that came with it, the
      // radians of turn per e-fold of radius, and one repeat in log-radius.
      "uniform vec4 uDive;",               // x phase, y spin, z twist, w P
      // THE FORM: the scale between neighbouring copies, how dark the throat goes, the wind (0 the
      // flat photograph, 1 the spiral as the module ships it) and the weight of the darkening.
      "uniform vec4 uForm;",               // x S, y well, z wind, w shade
      // THE HANDOVER: where the ring stands in log-radius, and how wide its seam is.
      "uniform vec2 uRing;",               // x front, y band
      // The judges' channel: which work each point carries, as colour.
      "uniform float uMask;",

      // The file's own transfer, undone. The module got this from its sRGB texture; here it is
      // written out, and it is the exact inverse of the encode the flat door finishes with.
      "vec3 toLin(vec3 c){",
      "  return mix(c / 12.92, pow((c + 0.055) / 1.055, vec3(2.4)), step(vec3(0.04045), c));",
      "}",
      // One read of one work, with the rows turned over for a texture the host uploaded unflipped.
      "vec3 grab(sampler2D t, vec2 uv, vec2 gx, vec2 gy){",
      "  return toLin(textureGrad(t, vec2(uv.x, 1.0 - uv.y),",
      "                           vec2(gx.x, -gx.y), vec2(gy.x, -gy.y)).rgb);",
      "}",

      "void main(){",
      "  vec2 uv = gl_FragCoord.xy / uRes;",
      "  float aspect = uRes.x / uRes.y;",
      "  vec2 p = (uv - uCentre) * vec2(aspect, 1.0);",
      "  float r2 = max(dot(p, p), 1e-14);",
      "  float r  = sqrt(r2);",
      "  float l  = log(r);",
      "  float ang = atan(p.y, p.x);",
      "  float P = uDive.w;",

      // where along the endless dive this pixel sits
      "  float L = l + uDive.x;",
      "  float f = L / P;",
      "  f = f - floor(f);",
      "  float m = exp(f * P);",            // radius inside one copy, in [1, S]

      // the shear: the read angle drifts with depth, so spokes become spirals
      "  float aa = ang + uDive.z * l + uDive.y;",
      "  vec2 dir  = vec2(cos(aa), sin(aa));",
      "  vec2 dirT = vec2(-dir.y, dir.x);",
      "  float s = 0.5 / uForm.x;",
      "  vec2 q = (s * m) * dir;",

      // exact derivatives of the read position, so the sampler picks a sane footprint even across
      // the ring where the pattern wraps
      "  vec2 dl   = p / r2;",
      "  vec2 dang = vec2(-p.y, p.x) / r2;",
      "  vec2 daa  = dang + uDive.z * dl;",
      "  float g = 1.0 / uRes.y;",
      "  vec2 ddx = (s * m) * (dir * dl.x + dirT * daa.x) * g;",
      "  vec2 ddy = (s * m) * (dir * dl.y + dirT * daa.y) * g;",

      // THE WIND. It picks WHICH POINT of the photograph a pixel reads, never which of two
      // already-drawn colours to show: the flat point is the plain cover fit every straight
      // photograph uses, the wound point is the one the log-polar map above worked out, and the wind
      // walks the SAMPLE COORDINATE between them. One fetch per copy per work answers every value of
      // it, so the frame is one picture in sharp focus at every mark of the ride, never two
      // renderings laid over each other. The spiral's geometry is never pushed toward zero to reach
      // the flat door, and the flat point is read off the frame's own middle, so no wandering centre
      // touches the door.
      "  vec2 vp = (uv - 0.5) * vec2(aspect, 1.0);",
      "  vec2 flatA = vec2(0.5) + vp * uFitA.xy;",
      "  vec2 flatB = vec2(0.5) + vp * uFitB.xy;",
      "  vec2 gxA = vec2(uFitA.x / uRes.y, 0.0), gyA = vec2(0.0, uFitA.y / uRes.y);",
      "  vec2 gxB = vec2(uFitB.x / uRes.y, 0.0), gyB = vec2(0.0, uFitB.y / uRes.y);",
      "  float d = uForm.z;",

      // WHICH WORK THIS POINT CARRIES. The ring is a place in log-radius, so it is an annulus about
      // the work's own centre; its seam is as wide as the module's own dissolve between two copies.
      // Outside it the arriving work, inside it the departing one. The radius this reads is the
      // module's own guarded one, so the frame's exact middle — where the radius runs to nothing —
      // is answered by the same guard that keeps the map's own division honest.
      "  float hw = 0.5 * uRing.y;",
      "  float share = smoothstep(uRing.x - hw, uRing.x + hw, l);",

      // this copy and the next one in, each read from the work this point carries, and the two
      // cross-faded across the repeat exactly as the module fades them
      "  vec2 sa = vec2(0.5) + q;",
      "  vec2 sb = vec2(0.5) + q / uForm.x;",
      "  vec3 a = mix(grab(uA, mix(flatA, sa, d), mix(gxA, ddx, d), mix(gyA, ddy, d)),",
      "               grab(uB, mix(flatB, sa, d), mix(gxB, ddx, d), mix(gyB, ddy, d)), share);",
      "  vec3 b = mix(grab(uA, mix(flatA, sb, d), mix(gxA, ddx / uForm.x, d),",
      "                    mix(gyA, ddy / uForm.x, d)),",
      "               grab(uB, mix(flatB, sb, d), mix(gxB, ddx / uForm.x, d),",
      "                    mix(gyB, ddy / uForm.x, d)), share);",
      // most of each copy is read straight; only a narrow ring dissolves into the next one, which is
      // what keeps the repeat from ever showing
      "  float w = smoothstep(0.40, 0.60, f);",
      "  vec3 col = mix(a, b, w);",

      // THE FINISH BELONGS TO THE SPIRAL ALONE — none of it stands at either door — so every term is
      // gated to its own identity by the same wind the coordinate travelled on, and weighted by the
      // one handle that carries the darkening.
      "  float dS = d * uForm.w;",
      // a dark line where one copy gives way to the next. It reads as the edge of the picture inside
      // the picture, and the hand-over happens inside it.
      "  float e = (f - 0.5) / 0.12;",
      "  float rim = 1.0 - 0.55 * exp(-e * e);",
      "  col *= mix(1.0, rim, dS);",
      // the throat darkens, so the middle reads as distance and not as mush
      "  float well = mix(uForm.y, 1.0, smoothstep(0.0, 0.22, r));",
      "  col *= mix(1.0, well, dS);",
      // the copy at the very edge is the largest one, so it is also the softest
      "  col *= 1.0 - dS * 0.55 * smoothstep(0.34, 0.96, length(vp));",
      // and where the centre stands out at an edge, the far side is blown up several times over.
      // Sink it rather than show the mush.
      "  col *= 1.0 - dS * 0.50 * smoothstep(0.75, 1.70, r);",

      // The picture is in linear light here. The module has always put it back with a plain 2.2
      // gamma, which is close to the file's own transfer but not it. At a door the frame owes the
      // file its own bytes, so the door encodes with the exact inverse transfer and the module's own
      // gamma travels in on the wind. One fetch, two encodings of it.
      "  vec3 lin = max(col, vec3(0.0));",
      "  vec3 exact = mix(lin * 12.92, 1.055 * pow(lin, vec3(1.0 / 2.4)) - 0.055,",
      "                   step(vec3(0.0031308), lin));",
      "  vec3 srgb = mix(exact, pow(lin, vec3(1.0 / 2.2)), d);",
      // put back the bite that the dissolve takes away
      "  srgb = (srgb - 0.5) * mix(1.0, 1.14, d) + 0.5;",
      "  float lum = dot(srgb, vec3(0.2126, 0.7152, 0.0722));",
      "  srgb = mix(vec3(lum), srgb, mix(1.0, 1.20, d));",

      // THE COPY MAP, the judges' own frame: which work this point carries, where in the copy it
      // stands, and how far the picture has wound in. A row reads the handover ring's own place off
      // the picture with it, and a door is refused when it is left open.
      "  vec3 judge = vec3(share, f, d);",
      "  srgb = mix(srgb, judge, uMask);",
      // THE COVERAGE: the alpha is the constant 1, and it is a decision. The map is defined at every
      // point of the frame, so this instrument has no absence to publish and stands as the ground a
      // stack is laid on.
      "  col = clamp(srgb, 0.0, 1.0);",
      "  gl_FragColor = vec4(col, 1.0);",
      "}",
    ].join("\n");

    function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
    function num(v, def) { var n = +v; return n === n ? n : def; }
    function smoothstep(a, b, x) {
      var t = (x - a) / (b - a);
      t = t < 0 ? 0 : t > 1 ? 1 : t;
      return t * t * (3 - 2 * t);
    }
    var TAU = Math.PI * 2;

    /* THE COPIES ARE CUT FROM A FALL OF FORTY (droste.js:291-294). One repeat is the log of the
       fortieth root taken `copies` times, so the whole dive from the frame's edge to the throat is
       one fall of forty whatever the count, and the count only says how many copies stand inside it.
       The module's own number, carried. */
    var DIVE_SPAN = 40;

    /* HOW WIDE THE HANDOVER'S OWN SEAM IS, as a share of one copy. The module dissolves its two
       reads over `smoothstep(0.40, 0.60, f)` — a fifth of a copy (droste.js:89) — and that is the
       one seam width this picture already carries, so the handover takes the same and no second
       width is invented. */
    var SEAM_SHARE = 0.20;

    /* HOW MUCH OF THE PASSAGE THE WIND HOLDS OPEN, at each end. The photograph winds in over the
       first third, the spiral stands whole across the middle third — which is where the two works
       exchange — and it unwinds over the last. THE PORT'S OWN NUMBER: the module has no passage and
       no doors, so nothing measured it. What decides it is that the handover must happen with the
       spiral open (a ring travelling across a flat photograph would be a boundary imposed from
       outside the work, which the charter convicts), and that the two ramps are equal because
       nothing distinguishes them. */
    var WIND_HOLD = 0.35;

    /* THE SINGULAR POINT AT THE THROAT, as the module itself bounds it: it guards the squared
       radius at a hundred-trillionth (droste.js:41), so no point of any frame it draws stands
       nearer the throat than a ten-millionth of the frame's own height. That is where the ring's
       travel ends, and it is the module's number rather than one this port chose — which is what
       makes the exit door whole at the frame's exact middle, where the radius runs to nothing. */
    var GUARD = 1e-7;

    /* THE CENTRE'S OWN REACH (droste.js:256). A named centre is an OFFSET on the module's own
       wander and not a place in the frame, because the wander is what the spiral does on its own and
       a handle at its middle must not stop it. The reach is the hand's own, read off the pointer
       line it replaces. */
    var CENTRE_REACH = 0.5;

    /* THE MODULE'S OWN RESTING VALUES for the three handles a score places from a measurement
       (droste.js:137-141, and the vista preset his 08-08 11:39 word approved: droste 32/45/copies
       4). The module states them out of 100; a handle of this engine runs 0 to 1. */
    var TURN_DEF = 0.32, SPEED_DEF = 0.45, COPIES_DEF = 4;

    /* HOW DARK THE THROAT GOES (droste.js:342). The module's own uniform, pinned there and lifted
       here onto the one handle that carries the darkening, which rests at the module's own weight. */
    var WELL = 0.05;

    // ---- the grid one frame is drawn on ------------------------------------------------------------
    // The buffer the host is about to bind as `resolution`, with the CSS frame where it hands none
    // and a square where it hands neither. Every geometric reading below is in the frame's own
    // height, which is the unit the shader's own `p` is in, so the grid is what the throat's floor
    // and the ring's own reach are read from. `drawn` says which of the two the reading names, since
    // a reader told «a 390 x 844 frame» would look for a device that has none.
    function gridOf(st) {
      var bw = Math.round(st.bufWidth), bh = Math.round(st.bufHeight);
      if (bw >= 1 && bh >= 1) return { w: bw, h: bh, drawn: true, given: true };
      var cw = Math.round(st.cssWidth), ch = Math.round(st.cssHeight);
      if (cw >= 1 && ch >= 1) return { w: cw, h: ch, drawn: false, given: true };
      return { w: 1, h: 1, drawn: false, given: false };
    }

    // HOW FAR THE FARTHEST CORNER OF THE FRAME STANDS FROM THE THROAT, in the frame's own height.
    // The ring starts beyond it, so at the entry door no point of the frame is outside the ring. It
    // is read off the throat the frame is actually drawn with — the wander included — rather than
    // off a bound, so the reach is this frame's own and no margin has to be guessed.
    function reachOf(cx, cy, aspect) {
      var far = 0, i, j, dx, dy;
      for (i = 0; i < 2; i++) {
        for (j = 0; j < 2; j++) {
          dx = (i - cx) * aspect;
          dy = j - cy;
          far = Math.max(far, Math.sqrt(dx * dx + dy * dy));
        }
      }
      return far;
    }

    // ---- the numbers of one frame ------------------------------------------------------------------
    // Everything the shader gets beyond the seating of the two works is a pure function of the pose,
    // and every number in the pose comes from a handle a score can drive. The module counted its own
    // second up in its own frame loop and answered a handed one in closed form (droste.js:386-406);
    // that closed form is what stands here, so the second the host hands down names the very place
    // the module's own clock would have reached.
    function posed(st) {
      var dial = clamp(num(st.mix, 0), 0, 1);
      var grid = gridOf(st);
      var aspect = grid.w / Math.max(grid.h, 1);
      var t = num(st.clock, 0);
      var copies = Math.round(clamp(num(st.size, COPIES_DEF), 2, 6));
      var P = Math.log(Math.pow(DIVE_SPAN, 1 / copies));
      var S = Math.exp(P);

      // the module's own breathing bend and its two response curves
      var bend = 1.0 + 0.62 * Math.sin(t * 0.14);
      var twistA = Math.pow(clamp(num(st.turn, TURN_DEF), 0, 1), 1.15) * 1.75;
      var speed = Math.pow(clamp(num(st.speed, SPEED_DEF), 0, 1), 1.35) * 0.95;
      var twist = twistA * bend;
      // the dive and the turn, integrated in closed form: the bend the turn rides is
      // 1 + 0.62 sin(0.14 t), so the turn is speed * A * (t + (0.62/0.14)(1 - cos(0.14 t)))
      var phase = speed * t;
      var spin = twistA * speed * (t + (0.62 / 0.14) * (1 - Math.cos(t * 0.14)));
      phase -= P * Math.floor(phase / P);
      spin -= TAU * Math.floor(spin / TAU);

      // the throat: the module's own wander on three unaligned periods, offset by the two handles
      // that read the work's own measured radial centre
      var cx = 0.5 + 0.16 * Math.sin(t * 0.107) + 0.05 * Math.sin(t * 0.31)
             + (clamp(num(st.centreX, 0.5), 0, 1) - 0.5) * 2 * CENTRE_REACH;
      var cy = 0.5 + 0.12 * Math.cos(t * 0.083)
             + (clamp(num(st.centreY, 0.5), 0, 1) - 0.5) * 2 * CENTRE_REACH;

      // THE WIND, AND THE HANDOVER'S OWN TRAVEL INSIDE IT. One dial carries both, so they cannot
      // disagree: the wind is nothing at both doors and whole across the middle, and the ring's
      // travel is confined to exactly the stretch the wind holds open.
      var wind = smoothstep(0, WIND_HOLD, dial) * smoothstep(1, 1 - WIND_HOLD, dial);
      var hand = clamp((dial - WIND_HOLD) / Math.max(1 - 2 * WIND_HOLD, 1e-9), 0, 1);

      // THE RING. It travels from beyond the frame's farthest corner to under the throat's own
      // singular point, so at `mix` 0 every point of the frame stands inside it and at `mix` 1
      // every point stands outside it. Both ends are read off THIS frame — its corners and its
      // throat — so neither is a margin anybody chose.
      //
      // A WHOLE SEAM BAND BEYOND EITHER END, not half of one. Half a band puts the ring's own edge
      // exactly on the farthest corner at the entry door — whole by arithmetic, with nothing at all
      // to spare — and a door with no room to spare cannot be told from one that has just lost it.
      //
      // AND IT TRAVELS IN THE RADIUS, NOT IN THE LOGARITHM OF IT. The picture is written in log
      // radius, so walking the ring there is the arithmetically obvious thing and it is wrong on
      // the frame: the frame's area sits almost entirely at the rim, so a ring walking evenly in
      // the logarithm has handed over four fifths of the frame in the first fifth of its travel and
      // spends the rest of the passage inside a disc a hand's breadth across. Walking evenly in the
      // radius makes the departing work shrink toward the throat at ONE speed, in the frame's own
      // unit, which is what the eye is actually reading.
      var band = SEAM_SHARE * P;
      var hw = 0.5 * band;
      var reach = reachOf(cx, cy, aspect);
      var rHi = reach * Math.exp(band);
      var rLo = GUARD * Math.exp(-band);
      var rRing = rHi + (rLo - rHi) * hand;
      var front = Math.log(rRing);

      return {
        centre: [cx, cy],
        dive: [phase, spin, twist, P],
        form: [S, WELL, wind, clamp(num(st.shade, 1), 0, 1)],
        ring: [front, band],
        // read on the diagnostic surface, bound to no uniform
        hand: dial, wind: wind, handover: hand, copies: copies, period: P, scale: S,
        phase: phase, spin: spin, twist: twist, bend: bend, speed: speed,
        throat: [cx, cy], reach: reach, radius: rRing, band: band, front: front,
        mask: clamp(num(st.mask, 0), 0, 1),
        aspect: aspect, grid: grid,
      };
    }

    // ONE TRAVELLING NUMBER, read on the diagnostic surface: how much of the handover the frame has
    // done. It is nothing until the spiral is open and whole before it closes, which is the shape of
    // this instrument's own response.
    function feelOf(u) {
      return clamp((clamp(u, 0, 1) - WIND_HOLD) / Math.max(1 - 2 * WIND_HOLD, 1e-9), 0, 1);
    }

    // COVER-FIT A WORK INTO THE FRAME, IN THE FRAME'S OWN HEIGHT, which is the module's own
    // `flatTexel` and not the plain uv-space cover fit the other instruments of this engine carry
    // (droste.js:330-335). The difference is the space it is read in: this shader measures the frame
    // in its own height — the same `vp` the spiral is written in — so the frame's ratio is already
    // in the coordinate the fit multiplies, and a fit that carried the ratio a second time would
    // squeeze the picture by it twice. The picture's short side fills the frame's short side, so a
    // door draws the file and nothing else, and `framings` publishes a crop of 1.
    function fit(iw, ih, w, h) {
      var fw = w / Math.max(h, 1);                 // the frame, in its own height
      var ta = iw / Math.max(ih, 1);               // the picture, same unit
      var Sw = Math.max(fw, ta);                   // the picture, cover-fitted
      return [1 / Sw, ta / Sw, 0, 0];
    }

    // ---- THE DOOR THE INSTRUMENT READS FOR ITSELF --------------------------------------------------
    // His 18:00 architecture decision: the instrument reads its doors at runtime on the actual
    // buffer, and the report it hands back is the runtime truth; what the manifest declares is only
    // the claim. Read here in this instrument's own unit, which is the SHARE — how much of the
    // arriving work stands at a point of the frame.
    //
    // WHAT A DOOR ASKS OF A SPIRAL. Three things, and this reads all three ON THE BUFFER:
    //   · ONE WORK STANDS AT EVERY POINT. At the entry door the share is nothing at every point of
    //     the frame and at the exit door it is whole; anything between is two photographs in one
    //     frame, which is the picture and not the door. The walk takes the buffer's own sample
    //     points and publishes, beside the worst share it found, how much room the ring had to
    //     spare — in copies, which is the unit the ring's own travel is measured in — so a ring
    //     whose reach is trimmed shows the margin closing long before a share moves.
    //   · THE PHOTOGRAPH STANDS FLAT. The wind is nothing at both doors by construction; it is read
    //     rather than declared, because a later change to the window would otherwise reach the
    //     doors unnoticed.
    //   · THE JUDGES' CHANNEL IS SHUT. `mask` draws the copy map itself as colour, which is what it
    //     is for; left open at a door the frame is a false-colour map and not the photograph.
    //
    // AND THERE IS NOTHING HERE TO HOLD. Both ends of the ring's travel are computed from the frame
    // the shader is about to draw on, so a fault this reading finds is a real one that no widening
    // closes, and the refusal stands alone. `held` is therefore always nothing, and it says so
    // rather than carrying a guard that could never fire.
    //
    // How much of the other work may stand in the frame at a door and it still BE the photograph:
    // half a level of 255, an eighth of the charter's own door bar of 6 of 255 taken at one point.
    var DOOR_SHOW = 0.5 / 255;

    // THE FRAME, WALKED AT THE BUFFER'S OWN SAMPLE POINTS: its four corners, where the ring has the
    // least room at the entry door; the midpoints of its four edges; the nine points around its
    // middle and the middle itself, where the ring has the least room at the exit door.
    function ringReadOf(v, W, H) {
      var aspect = W / Math.max(H, 1);
      var cx = v.centre[0], cy = v.centre[1];
      var hw = 0.5 * v.band;
      var worst = 0, spare = 1e9, walked = 0, i, j;
      var want = v.want;
      function walk(px, py) {
        var dx = (px / W - cx) * aspect, dy = (1 - py / H) - cy;
        // the module's own guard on the squared radius, so the walk reads the very number the
        // shader reads at the frame's exact middle
        var r = Math.sqrt(Math.max(dx * dx + dy * dy, 1e-14));
        var lPick = Math.log(r);
        var share = smoothstep(v.front - hw, v.front + hw, lPick);
        worst = Math.max(worst, Math.abs(share - want));
        // how much room the ring had to spare at this point, in copies of the dive
        spare = Math.min(spare, (want ? (lPick - v.front - hw) : (v.front - hw - lPick)) / v.period);
        walked++;
      }
      for (i = 0; i < 2; i++) {
        for (j = 0; j < 2; j++) { walk(i ? W - 0.5 : 0.5, j ? H - 0.5 : 0.5); }
      }
      walk(0.5, H * 0.5); walk(W - 0.5, H * 0.5); walk(W * 0.5, 0.5); walk(W * 0.5, H - 0.5);
      for (i = -1; i <= 1; i++) {
        for (j = -1; j <= 1; j++) { walk(W * 0.5 + i, H * 0.5 + j); }
      }
      walk(W * cx, H * (1 - cy));
      return { walked: walked, worst: worst, spareCopies: spare, want: want,
               wind: v.wind, mask: v.mask, front: v.front, period: v.period };
    }

    // THE DOOR, MEASURED. Null everywhere but at a door, since away from the doors two works in one
    // frame is the picture rather than a fault. The door is named by the manifest's own `doors`
    // block: `mix` at 0 is the entry door, where the frame is the departing work whole, and `mix` at
    // 1 the exit door, where it is the arriving one.
    function doorReadOf(v, st) {
      var want = st.mix === 0 ? 0 : (st.mix === 1 ? 1 : -1);
      if (want < 0) return null;
      var g = v.grid;
      if (!g.given) return null;
      v.want = want;
      var read = ringReadOf(v, g.w, g.h);
      read.grid = g;
      return read;
    }

    // THE REFUSAL, worded the way the host's own manifest refusals read: what is wrong, in this
    // instrument's own measured numbers, on the grid it was measured on.
    function doorWhyNoOf(read) {
      if (!read) return null;
      var g = read.grid, door = read.want ? "the exit" : "the entry";
      var work = read.want ? "arriving" : "departing";
      var other = read.want ? "departing" : "arriving";
      var where = " of a " + g.w + " x " + g.h + (g.drawn ? " buffer" : " frame");
      if (read.worst >= DOOR_SHOW) {
        return door + " door leaks: the " + other + " work stands at " + read.worst.toFixed(6)
             + " of the frame's own colour at the worst of the " + read.walked
             + " points this reading walked" + where + ", so the frame is two photographs at once, "
             + "where " + door + " door's own law asks for the " + work + " work at every point";
      }
      if (read.wind >= DOOR_SHOW) {
        return door + " door leaks: the picture stands " + read.wind.toFixed(6)
             + " wound into the spiral" + where + ", so the frame is a spiral and not the " + work
             + " work standing flat, where " + door + " door's own law asks for that work at every "
             + "point";
      }
      if (read.mask >= DOOR_SHOW) {
        return door + " door leaks: the judges' own channel stands at " + read.mask.toFixed(6)
             + ", so the frame draws the copy map — which work each point carries, over a "
             + g.w + " x " + g.h + (g.drawn ? " buffer" : " frame")
             + " — instead of the " + work + " work, where " + door + " door's own law asks for the "
             + work + " work at every point";
      }
      return null;
    }

    // THE NUMBERS OF ONE FRAME, WITH ITS DOOR READ ON THE BUFFER BEING DRAWN. Away from a door this
    // is `posed` and nothing more: the reading is taken nowhere else.
    function values(st) {
      var v = posed(st);
      var read = doorReadOf(v, st);
      v.doorGrid = read ? read.grid : null;
      v.ringMap = read ? { walked: read.walked, worst: read.worst, spareCopies: read.spareCopies,
                           want: read.want } : null;
      v.doorHeld = null;
      v.doorWhyNo = doorWhyNoOf(read);
      return v;
    }

    var manifest = {
      id: "droste", api: 1, arity: 2,
      // The photograph comes apart into copies of itself, the works exchange on a ring in the wound
      // middle, and the arriving work unwinds whole.
      roles: ["disassembly", "mystery", "assembly"],
      // WHERE THIS STANDS ON THE CHARTER'S SHELF: SURFACE, his own standing verdict in the
      // vocabulary table of lab/CROSSING-BRIEF.md. The whole frame becomes one wound surface; no
      // cell of it lives a life of its own, the copies being the same surface at other scales. CELL
      // is not claimed for that reason, and WORLD is not claimed because the table does not.
      levels: ["SURFACE"],
      // WHAT IT CUTS ON. Rings: the copies are annuli about the work's own measured radial centre
      // and the handover happens on one of them. The collection's `radial` measure cuts on this
      // kind.
      cuts: ["ring"],
      // WHAT A PAIR MUST READ FOR THIS CROSSING TO BE WORTH PLAYING HERE, in the instrument's own
      // words, so the choice can be made when a pair is handed over rather than swept for.
      asks: {
        measure: "radial",
        floor: "radial_tight",
        of: "either work of the pair",
        says: "a spiral has a throat, and the throat has to stand where the photograph itself puts "
            + "it. One of the two works must read radial over the collection's own tight floor — a "
            + "picture built around a centre, concentric rings or spokes running out of one point, "
            + "strongly enough that the centre is the work's own device and not an accident of "
            + "framing. Rings become the copies; spokes become the spiral, because the shear turns "
            + "a straight spoke into one. A photograph with no centre gives the dive nowhere to "
            + "fall",
      },
      params: { size: [2, 6], turn: [0, 1], speed: [0, 1], centreX: [0, 1], centreY: [0, 1] },
      // EVERY handle a score can drive (§4.4b). `mix` is the dial — the module's own `spiral` and
      // its own dive, under one envelope. `clock` is the second the host hands down, which the
      // module answers in closed form. The five below them are the module's declared params a pair
      // can stand, each naming the measurement it reads; `shade` is the darkening the module keeps
      // to itself, resting where it rests it; `mask` is the judges' channel.
      //
      // NO `seed` HANDLE, AND THAT IS A DECISION. Nothing in this picture is rolled: the wander, the
      // bend, the dive and the turn are all closed forms of the handed second, so a seeded run
      // repeats to the point and a die would be a handle a score could walk without moving anything.
      //
      // THE MODULE'S `picture` PARAM IS PUBLISHED BY NEITHER NAME. A cue carries an ordered pair and
      // owes a door at each end, so which work stands where is the passage's own question and not a
      // handle: the ring answers it.
      handles: {
        mix: { min: 0, max: 1, def: 0 },
        clock: { min: 0, max: 14, def: 0, unit: "seconds",
                 reads: "the second the host hands down; the dive, the turn, the centre's wander "
                      + "and the breathing bend are closed forms of it" },
        size: { min: 2, max: 6, def: COPIES_DEF, kind: "enum", step: 1,
                unit: "how many copies stand inside one fall of forty",
                reads: "the work's own measured ring count, the collection's `radial` reading — the "
                     + "same measurement the meshing instrument takes its ring count from. A work "
                     + "of few rings dives in few large copies and one of many in many small ones",
                applied: { fallOfForty: DIVE_SPAN, onePeriodIs: "log(40) over the count" } },
        turn: { min: 0, max: 1, def: TURN_DEF,
                unit: "how far the copies wind into a spiral, in radians of turn per e-fold",
                reads: "the work's own measured radial score, so a work whose rings are its own "
                     + "device winds hard into the spiral and one that barely reads radial barely "
                     + "winds at all",
                applied: { radiansPerEFoldAtWhole: 1.75, curve: "u^1.15, the module's own" } },
        speed: { min: 0, max: 1, def: SPEED_DEF, unit: "how fast the dive falls",
                 reads: "the copy count against the instrument's own default count, so one copy "
                      + "passes the eye in the same time whatever the pair",
                 applied: { periodsPerSecondAtWhole: 0.95, curve: "u^1.35, the module's own" } },
        centreX: { min: 0, max: 1, def: 0.5,
                   unit: "where the spiral's throat stands across the frame, as an offset on the "
                       + "module's own wander",
                   reads: "the work's own measured radial centre, the collection's `radial.centreX`",
                   applied: { reach: CENTRE_REACH, restsOn: "the module's own wander" } },
        centreY: { min: 0, max: 1, def: 0.5,
                   unit: "where the throat stands up the frame, as an offset on that same wander",
                   reads: "the work's own measured radial centre, the collection's `radial.centreY`. "
                        + "The module publishes only the across-frame half of this pair; the other "
                        + "half is the port's, in the module's own idiom, because a measured centre "
                        + "has two coordinates and a handle for one of them would read half of it",
                   applied: { reach: CENTRE_REACH, restsOn: "the module's own wander" } },
        shade: { min: 0, max: 1, def: 1,
                 unit: "the weight of the darkening the spiral carries",
                 applied: { wellAtTheThroat: WELL, rimOnTheSeam: 0.55, cornerSink: 0.55,
                            farSink: 0.50, restsAt: "both doors" } },
        // THE MEASUREMENT THIS HANDLE IS READ AGAINST AT A DOOR. `readAtADoor` says what is read
        // (this instrument's own share of the arriving work, walked at the buffer's own sample
        // points), on which grid, what the reading is counted in, and that there is no hold — the
        // ring's two ends are computed from the frame the shader draws on, so a door this reading
        // finds a fault at is refused outright.
        mask: { min: 0, max: 1, def: 0,
                applied: { readAtADoor: { points: DOOR_SHOW, readOn: "the drawing buffer",
                                          reads: "handover",
                                          measures: "the arriving work's own share at the buffer's "
                                                  + "own sample points, the wind, and this channel",
                                          held: null } } },
      },
      neutrals: { a: 0, b: 1 },
      doors: { in: { handle: "mix", value: 0, work: "a" },
               out: { handle: "mix", value: 1, work: "b" } },
      // BOTH DOORS FRAME ALIKE, AND NEITHER IS CROPPED. The spiral is a map of the frame onto
      // itself and asks for no room beyond it, so a door is the source cover-fitted and nothing
      // else.
      framings: { "0": { coverCrop: 1 }, "1": { coverCrop: 1 } },
      drivers: ["progress", "cueProgress", "time", "velocity", "capability", "noise", "static",
                "curve", "spline", "map", "add", "multiply", "mix", "clamp", "hold", "segment",
                "ramp", "slew", "oscillate", "node"],
      camera: { needs: "none", authority: "stage" },
      // THE PICTURE'S OWN CHAIN OF SMALLER COPIES, asked for by §8's `gl.readsChain`. The dive
      // minifies hard near the throat — a deep copy is a few pixels across — and the host binds one
      // plain texture per work with no chain, so those copies alias where a chain would have
      // smoothed them. The well darkens that region to a twentieth, which is why the port read as
      // acceptable rather than broken; with the chain uploaded the deep copies resolve instead.
      // `textureGrad` in the map above is already handed the exact derivatives to walk it with.
      gl: { preserveDrawingBuffer: false, readsChain: true },
      // WHAT THIS INSTRUMENT WRITES WHERE ITS OWN MATTER IS ABSENT (§7's coverage law, and the
      // per-instrument specification in docs/design/COVERAGE.md). It is absent nowhere.
      coverage: { writes: false,
                  how: "the log-polar map is defined at every point of the frame and every point is "
                     + "written, so the alpha is the constant 1; at a door the instrument walks the "
                     + "buffer's own sample points and refuses a door where any of them carries a "
                     + "share of the other work" },
      // The neutral pose is the ENTRY DOOR — `mix` at 0, the value the `doors` block names — so the
      // frame keys the host reads off it at registration include the door's own record.
      neutralPose: { mix: 0, clock: 0, size: COPIES_DEF, turn: TURN_DEF, speed: SPEED_DEF,
                     centreX: 0.5, centreY: 0.5, shade: 1, mask: 0,
                     reduced: false, cssWidth: 1000, cssHeight: 1000 },
      passes: [{
        program: "droste", vert: VERT, frag: FRAG, position: "aPos",
        uniforms: [
          { name: "uA", type: "sampler2D", source: "textureA" },
          { name: "uB", type: "sampler2D", source: "textureB" },
          { name: "uFitA", type: "vec4", source: "fitA" },
          { name: "uFitB", type: "vec4", source: "fitB" },
          { name: "uRes", type: "vec2", source: "resolution" },
          { name: "uCentre", type: "vec2", source: "frame:centre" },
          { name: "uDive", type: "vec4", source: "frame:dive" },
          { name: "uForm", type: "vec4", source: "frame:form" },
          { name: "uRing", type: "vec2", source: "frame:ring" },
          { name: "uMask", type: "float", source: "handle:mask" },
        ],
      }],
      // The instrument allocates nothing of its own: it spends the two source-texture slots the host
      // already holds and the one programme the host builds from this manifest. The module's own
      // canvas, its context, its two textures with their mip chains and its own frame loop are what
      // this port does without.
      resources: { lean: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                           passes: 1, bytesEstimate: 0, variant: "lean" },
                   standard: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0,
                               programs: 1, passes: 1, bytesEstimate: 0, variant: "standard" },
                   rich: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                           passes: 1, bytesEstimate: 0, variant: "rich" } },
      capabilities: ["webgl2"],
      decline: ["one work only", "a source that never decoded"],
      provenance: { labPath: "lab/effects/droste.js", commit: "fc885a3",
                    sha256: "445cdf4afa7495905fe5a4c7443d9e775943d376d72982cc941815ca9a22ee4b" },
      readiness: "production-ready",
    };

    var live = false;
    return {
      name: "droste",
      manifest: manifest,
      values: values,
      fit: fit,
      feel: feelOf,
      prepare: function (o) {
        if (!o.sources) return { take: false, why: "the droste instrument needs both works" };
        if (!o.cue) return { take: false, why: "no cue names it" };
        return { take: true };
      },
      start: function () { live = true; },
      // The pose the shader draws. The module's canvas, its frame loop and its pointer are gone, so
      // every number here comes from a handle a score drives or from the frame the host is about to
      // bind.
      //
      // A DOOR THIS INSTRUMENT CANNOT KEEP WHOLE IS REFUSED RATHER THAN DRAWN. At either door it
      // walks its own share of the arriving work over the buffer the host is about to bind and,
      // where any sample point carries the other work, where the picture is still wound, or where
      // the judges' channel is left open, it hands the host the reason with the measured numbers in
      // it instead of drawing a door that is not the photograph. The host recovers the transaction
      // on that reason and the walk's own glide carries the visitor.
      frame: function (st) {
        if (!live) return;
        var h = st.handles;
        var pose = {
          mix: h.mix, clock: h.clock, size: h.size, turn: h.turn, speed: h.speed,
          centreX: h.centreX, centreY: h.centreY, shade: h.shade, mask: h.mask,
          reduced: st.reduced,
          cssWidth: st.viewport.w, cssHeight: st.viewport.h,
          // THE GRID THE SHADER WILL SAMPLE ON, carried into the pose so the ring's own two ends and
          // the throat's floor are built for the frame the host is about to bind as `uRes` and the
          // door is read on it rather than on the CSS frame around it.
          bufWidth: st.viewport.bufferW, bufHeight: st.viewport.bufferH,
        };
        // AT A DOOR THE INSTRUMENT SAYS WHAT IT APPLIED, and says it before it refuses. `request` is
        // the share a door asks for — nothing at the entry, whole at the exit — and `applied` is the
        // worst share this grid actually shows, so `moved` is the two read against each other.
        if (h.mix === 0 || h.mix === 1) {
          var v = values(pose);
          if (st.reportApplied) {
            st.reportApplied({
              door: h.mix === 0 ? "in" : "out",
              buffer: [pose.bufWidth, pose.bufHeight],
              reads: "handover",
              request: v.ringMap ? v.ringMap.want : null,
              applied: v.ringMap ? (v.ringMap.want ? 1 - v.ringMap.worst : v.ringMap.worst) : null,
              moved: v.ringMap ? v.ringMap.worst : null,
              unit: "the arriving work's own share of the frame",
              // What the ring was doing over the frame at this door: how many points were walked,
              // and how much room in copies of the dive the tightest of them had to spare.
              walked: v.ringMap ? v.ringMap.walked : null,
              spareCopies: v.ringMap ? v.ringMap.spareCopies : null,
              wind: v.wind,
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
    instrument: drosteInstrument(),
  });
})();
