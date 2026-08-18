/*!pass-inst-tilt.js*/
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
// OWNERSHIP. This instrument was carried over from lab/effects/tilt.js. The artistic instruments and
// their manifests belong to tlvphotos, which builds these files from its own sources; the engine's
// copies are what ships until that handover lands. The contract this file answers to is §7 and §8 of
// docs/design/PASS-API-V1.md, and the record that names it is the site's own `pass` block.
(function () {
  var join = window.__@@NS@@PassInstrument;
  if (typeof join !== "function") return;

  // THIS FILE'S OWN VERSION, and the one home of that fact. The build reads this literal out of the
  // source and writes it into the site's record beside the digest, so the version a file declares
  // and the version a host was told to load cannot drift apart without the build noticing.
  var INSTRUMENT_VERSION = "1.0.0";

  // ================================================================================================
  // THE LEANING INSTRUMENT (§8) — lab/effects/tilt.js carried across
  // ================================================================================================
  // WHAT THE VISITOR SEES. The whole frame lies down into depth: its rows crowd together toward the
  // far edge and open out toward the eye, and the camera pushes in by exactly what the lean costs so
  // the frame stays full. The second work stands on that same plane, beyond the first, and the line
  // where they meet travels from the far edge forward to the eye. Because the plane is projective
  // that line creeps where the rows are dense and runs where they open out — the arrival's own
  // unevenness is the projection's, which is the charter's mystery with no fade. The frame comes back
  // upright as the second work lands.
  //
  // WHAT CAME OVER: the shader, the plane and its camera (`planeOf`), the smallest push-in that keeps
  // the frame covered (`zoomFor`), the inverse of the plane's own map (`inv3`), the seating of a work
  // in the frame (`fit`), the response curve (`feelOf`) and the numbers of one frame (`values`).
  // Not one of the module's numbers changed.
  //
  // WHAT STAYED BEHIND: its own canvas, its own WebGL 1 context, its own frame loop, its resize
  // listener and its own accumulated clock (§1.2's fence).
  //
  // ---- THE CARRIER HALF DID NOT CROSS, AND IT IS NAMED RATHER THAN DROPPED --------------------
  // The lab module is a CARRIER (lab/CROSSING-HISTORY.md:240-242). A face of it may be a SOURCE that
  // is not a photograph at all but a canvas another module is drawing on, re-read on every frame this
  // one draws, so the picture that leans can be any effect in the arsenal running its own handle on
  // its own clock (tilt.js:7-11, and its `upload` re-reading a live source every frame).
  //
  // THIS ENGINE HANDS AN INSTRUMENT TWO DECODED WORKS AND NOTHING ELSE. The host arms and decodes the
  // two photographs off the walk's own markup and binds them as `textureA` and `textureB`; there is
  // no second instrument's canvas anywhere in the supply an instrument may name (§7's `SUPPLY`), and
  // an instrument that named one would be refused at registration. So the carrier half cannot cross
  // as it stands, and nothing here stands in for it.
  //
  // WHAT DID CROSS IS THE MODULE'S OWN OTHER ROAD, which the module itself supports and its own header
  // names: «Handed no source, it carries the plain photographs of ctx.images, which is the same module
  // with nothing playing on it». Every number, every line of geometry and both doors are that road's,
  // unchanged. What is lost is the leaning of a MOVING picture, and the loss is exact: it is the
  // difference between two live canvases and two still photographs on the same plane.
  //
  // ---- THREE THINGS THE PORT HAD TO ANSWER ------------------------------------------------------
  //   · THE INVERSE ARRIVES AS THREE ROWS. The module binds its plane's inverse as one `mat3`
  //     uniform. §7's type vocabulary is sampler2D, float, vec2 and vec4, so a matrix cannot be
  //     bound as one name. The three ROWS travel as three vec4s and the shader rebuilds the very
  //     same `mat3` out of them before a single line of the module's own body runs — so `uInv *
  //     vec3(sp, 1.0)` and the two elements the footprint reads are character for character the
  //     module's, and no line of mathematics was re-derived to fit the transport.
  //   · THE PRESERVED DRAWING BUFFER. The module asks its own context for one (tilt.js:242) and §7
  //     refuses a manifest that asks for it. What the flag stood in for is a REDRAW: the module drew
  //     on a parameter change, on a resize and on its own frame loop, and under reduced motion it
  //     drew once and stopped. The host draws every frame of a running transaction and redraws on
  //     every resize, so the frame the compositor shows is one this instrument drew for it.
  //   · THE VERSION HEADER. This module's shader carries none, so the host's translator stamps the
  //     one it needs and no second one arrives.
  //
  // ASPECT. The module reads the frame's aspect from the drawing buffer it owns. The host owns the
  // buffer here and already binds its size as `uRes`, so the shader derives the aspect from `uRes`
  // and `values` below reads the same two numbers off the pose — one aspect, in both places, which is
  // what makes a door exact rather than nearly exact.
  function tiltInstrument() {
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
      // THE THREE ROWS OF THE PLANE'S OWN INVERSE — screen (frame units, zoom removed) to the
      // plane's own square. The module binds one mat3; §7 knows no matrix type, so the rows travel
      // and the matrix is rebuilt below out of exactly the numbers the module uploaded.
      "uniform vec4 uInv0;",
      "uniform vec4 uInv1;",
      "uniform vec4 uInv2;",
      "uniform float uZoom;",
      "uniform float uFront;",       // where the front stands, in the plane's own row coordinate
      "uniform float uSpread;",      // how far apart the columns' own moments are set
      "uniform float uCols;",        // how many columns carry their own moment
      "uniform float uSeed;",
      "uniform float uOff;",         // counter-motion, in the plane's own uv
      "uniform float uGuard;",
      "uniform float uMask;",        // the judges' channel: draw this instrument's own coverage

      "float hash11(float n){ return fract(sin(n * 127.1) * 43758.5453); }",

      "vec2 into(vec2 p, vec4 f){",
      "  return clamp((p - 0.5) * f.xy + 0.5 + f.zw, 0.0008, 0.9992);",
      "}",

      "void main(){",
      // the aspect of the buffer the host drew into, read from the size the host binds
      "  float uAspect = uRes.x / max(uRes.y, 1.0);",
      // THE MODULE'S OWN MATRIX, REBUILT. GLSL's mat3 constructor takes its nine floats column by
      // column, and the module uploaded exactly these nine in exactly this order, so the matrix
      // below is the matrix the module bound — including which element each of `uInv[1]` and
      // `uInv[2]` names, which the footprint two lines down depends on.
      "  mat3 uInv = mat3(uInv0.x, uInv1.x, uInv2.x,",
      "                   uInv0.y, uInv1.y, uInv2.y,",
      "                   uInv0.z, uInv1.z, uInv2.z);",
      "  vec2 sp = vec2((vUv.x - 0.5) * 2.0 * uAspect, (0.5 - vUv.y) * 2.0) / uZoom;",
      "  float px = 2.0 / max(uRes.y, 1.0) / uZoom;",

      "  vec3 q = uInv * vec3(sp, 1.0);",
      "  vec2 st = q.xy / q.z;",
      // st.y runs UP the frame, the way the geometry is built, and an image's rows run DOWN it,
      // so the row coordinate is turned over here — otherwise the source stands on its head
      "  vec2 uv = vec2(st.x * 0.5 + 0.5, 0.5 - st.y * 0.5);",

      // THE PIXEL'S OWN FOOTPRINT IN THE PLANE'S ROWS, from the projection's own Jacobian. Where
      // the rows are dense — at the far edge — one pixel covers many rows, and the front's edge is
      // filtered by exactly that much.
      "  float dtdy = (uInv[1].y * q.z - q.y * uInv[2].y) / max(q.z * q.z, 1e-9);",
      "  float foot = max(abs(dtdy) * px * 0.5, 1e-6);",

      // THE FRONT, ragged column by column: six parts a ladder across the plane, four parts the die.
      "  float ci = floor(clamp(uv.x, 0.0, 0.9999) * uCols);",
      "  float ord = mix(ci / max(uCols - 1.0, 1.0), hash11(ci + uSeed), 0.4);",
      "  float front = uFront + uSpread * (ord - 0.5);",

      // COVERAGE: the near side of the front is the first work, the far side the second. st.y runs
      // +1 at the far edge and −1 at the near edge.
      "  float d = (front - st.y) / (2.0 * foot);",
      "  float cov = clamp(0.5 + d, 0.0, 1.0);",

      "  vec3 colA = texture2D(uA, into(uv + vec2(0.0, uOff), uFitA)).rgb;",
      "  vec3 colB = texture2D(uB, into(uv - vec2(0.0, uOff), uFitB)).rgb;",
      "  vec3 col = mix(colB, colA, cov);",

      // the near work lies over the far one: the shadow decays from the front INTO the far work
      "  col *= 1.0 - 0.34 * uGuard * (1.0 - cov) * exp(-max(-d, 0.0) / 6.0);",
      // THE JUDGES' CHANNEL, resting at nothing, where it costs the picture exactly nothing: the
      // frame drawn is the coverage this instrument publishes as its alpha, so a law about the
      // coverage can be read OFF THE PICTURE rather than taken on the instrument's word.
      "  col = mix(col, vec3(1.0 - cov), uMask);",
      // THE COVERAGE LAW (§7). `cov` is 1 at the points the near work owns and 0 at the points the
      // far one owns, so `1.0 - cov` is the territory of the work RIDING IN over the far edge —
      // this instrument's own matter. At the entry door the front stands beyond the far edge of the
      // plane, so the alpha is 0 at every point and the instant the cue's window opens the frame
      // does not change; at the exit door it has travelled past the near edge, so the alpha is 1 at
      // every point and the door is this instrument's own whole work.
      //
      // THE CONTACT SHADOW SURVIVES A STACK. It rides `(1.0 - cov)` — the side this alpha keeps —
      // the way the meshing instrument's does, so a cue playing beneath is not darkened by it and no
      // multiply blend is wanted anywhere.
      //
      // THE COLOUR CHANNEL IS UNTOUCHED at the judges' rest, which is what makes a one-cue score
      // byte-identical: laid down first the host disables blending and reads no alpha, so `col`
      // reaches the frame exactly as the lab module drew it.
      "  gl_FragColor = vec4(col, 1.0 - cov);",
      "}",
    ].join("\n");

    function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
    function num(v, d) { var n = Number(v); return n === n ? n : d; }
    function smoothstep(a, b, x) {
      var t = (x - a) / (b - a);
      t = t < 0 ? 0 : t > 1 ? 1 : t;
      return t * t * (3 - 2 * t);
    }

    /* THE LEAN AT ITS FULLEST, in degrees, and the camera's range (tilt.js:169). Past about
       thirty-five degrees the far rows of these photographs — dense window grids — stop resolving
       into anything and the picture reads as a smear, which is the same reason the woven instrument
       holds its strip count down. The camera's distance is read in frame half-heights: far is nearly
       a shear, near is a strong one-over-depth. Both ends are published on the `squeeze` handle. */
    var TILT_MAX = 35, CAM_FAR = 9.0, CAM_NEAR = 2.6;

    /* THE STANDING CROP (tilt.js:174-175). The camera pays for the lean itself, so the only headroom
       wanted here is for the counter-motion — the frame coordinate is pushed by at most AMP, and the
       crop is that push at both ends and a hair. It is the 1.12 lab/data/module-contract-new.json
       records for this module's framing. */
    var AMP = 0.05;
    var CROP = 1 + 2 * AMP + 0.02;

    /* HOW MANY COLUMNS CARRY THEIR OWN MOMENT ALONG THE FRONT. The module pins this at nine
       (tilt.js:176); here it is a handle, because how many columns a front breaks into is a reading
       of the pair rather than a constant of the instrument — see the `columns` handle below, which
       names the measurement it is driven from. Nine is its default, so a score that names no track
       for it draws the module's own frame. */
    var COLS = 9;
    var COLS_MIN = 1, COLS_MAX = 24;

    /* HOW FAR THE FRONT TRAVELS PAST THE PLANE'S OWN FAR AND NEAR EDGES (tilt.js:389, the module's
       own `reach = 1 + spread * 0.5 + 0.03`). The plane's row coordinate runs from −1 at the near
       edge to +1 at the far one, and the raggedness moves a column's own front by at most half the
       spread, so a front standing `MARGIN` beyond ±1 with the spread already added leaves every
       column's front clear of the plane. THE SPREAD CANCELS EXACTLY: the earliest column's front at
       the entry door stands at `reach − spread/2 = 1 + MARGIN`, whatever the raggedness is. That is
       why MARGIN is the one number the door reading below is held against. */
    var MARGIN = 0.03;

    /* HOW FAR THE CAMERA MAY PUSH IN (tilt.js:403). The push-in is computed rather than chosen; this
       is only the stop the module puts on a degenerate plane, carried over unchanged. */
    var ZOOM_CAP = 4;

    // cover-fit a work into the frame, then pull in by the counter-motion's headroom. The host hands
    // the source's own dimensions, so the instrument never touches an image object.
    function fit(iw, ih, w, h) {
      var fa = w / Math.max(h, 1);
      var ia = iw / Math.max(ih, 1);
      var sx, sy;
      if (ia > fa) { sx = fa / ia; sy = 1; } else { sx = 1; sy = ia / fa; }
      return [sx / CROP, sy / CROP, 0, 0];
    }

    /* THE RESPONSE CURVE, carried digit for digit (tilt.js:262-273). Dead bands of 0.05 at both
       ends — lab/data/module-contract-new.json's own `dial.deadBand` for this module — and between
       them a two-piece exponential hinged at 0.4 of one half, k1 = −0.9 below the knee and k2 = 1.5
       above it, mirrored about the middle because a whole work stands at either end. The port
       re-derives nothing. */
    var FEEL_D0 = 0.05, FEEL_C = 0.4, FEEL_K1 = -0.9, FEEL_K2 = 1.5;
    function feelLog(x, k) {
      return Math.abs(k) < 1e-6 ? x : (Math.exp(k * x) - 1) / (Math.exp(k) - 1);
    }
    function feelKnee(u) {
      return u <= 0.5 ? FEEL_C * feelLog(2 * u, FEEL_K1)
                      : FEEL_C + (1 - FEEL_C) * feelLog(2 * u - 1, FEEL_K2);
    }
    function feelOf(u) {
      var x = clamp((u - FEEL_D0) / (1 - 2 * FEEL_D0), 0, 1);
      return x <= 0.5 ? 0.5 * feelKnee(2 * x) : 1 - 0.5 * feelKnee(2 - 2 * x);
    }

    // The inverse of a three by three, the module's own (tilt.js:178-187).
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

    // ---- THE PLANE, ITS LEAN, AND THE CAMERA THAT PAYS FOR IT (tilt.js:276-306) -------------------
    // The lean is nothing at either door and most in the middle: the frame leaves upright and comes
    // back upright, which is the whole shape of this carrier.
    function planeOf(st, aspect) {
      var d = feelOf(clamp(num(st.mix, 0), 0, 1));
      var phi = TILT_MAX * Math.PI / 180 * clamp(num(st.tilt, 0), 0, 1) * Math.sin(Math.PI * d);
      var D = CAM_FAR + (CAM_NEAR - CAM_FAR) * clamp(num(st.squeeze, 0), 0, 1);
      // the axis the plane turns about: high in the frame is a far horizon, low is a near one
      var y0 = (1 - 2 * clamp(num(st.horizon, 0), 0, 1));
      var mx = aspect, my = 1;
      var co = Math.cos(phi), si = Math.sin(phi);

      function pt(s, tt) {
        var y = tt * my;
        return { x: s * mx, y: y0 + (y - y0) * co, z: -(y - y0) * si };
      }
      var o = pt(0, 0), es = pt(1, 0), et = pt(0, 1);
      var Xs = es.x - o.x, Xt = et.x - o.x;
      var Ys = es.y - o.y, Yt = et.y - o.y;
      var Zs = es.z - o.z, Zt = et.z - o.z;
      var c = D;                                   // the plane at z = 0 draws at scale 1
      var Hm = [c * Xs, c * Xt, c * o.x,
                c * Ys, c * Yt, c * o.y,
                -Zs, -Zt, D - o.z];
      var corners = [[-1, -1], [1, -1], [1, 1], [-1, 1]].map(function (qq) {
        var p = pt(qq[0], qq[1]);
        var k = c / Math.max(D - p.z, 1e-6);
        return [p.x * k, p.y * k];
      });
      return { H: Hm, corners: corners, phi: phi, D: D, dial: d, aspect: aspect };
    }

    /* WHAT THE LEAN COSTS THE FRAME, and the camera paying it (tilt.js:313-331). A leaning plane's
       far edge draws smaller, so the frame is no longer covered; the answer is the smallest push-in
       that puts every corner of the frame back inside the projected plane. Read off the plane's own
       four edges, so it is exactly the cost and not a guess — and at a door, where nothing leans, it
       is exactly 1, which is what makes the doors the source cover-fit and nothing else. */
    function zoomFor(corners, aspect) {
      var cx = 0, cy = 0, i, j, z = 1;
      for (i = 0; i < 4; i++) { cx += corners[i][0] / 4; cy += corners[i][1] / 4; }
      var frame = [[-aspect, -1], [aspect, -1], [aspect, 1], [-aspect, 1]];
      for (i = 0; i < 4; i++) {
        var p = corners[i], q = corners[(i + 1) % 4];
        var nx = -(q[1] - p[1]), ny = q[0] - p[0];
        var len = Math.sqrt(nx * nx + ny * ny) || 1;
        nx /= len; ny /= len;
        var d = -(nx * p[0] + ny * p[1]);
        if (nx * cx + ny * cy + d < 0) { nx = -nx; ny = -ny; d = -d; }
        if (d <= 1e-6) return 1e3;
        for (j = 0; j < 4; j++) {
          var need = -(nx * frame[j][0] + ny * frame[j][1]) / d;
          if (need > z) z = need;
        }
      }
      return z;
    }

    // ---- THE GRID A DOOR IS READ ON --------------------------------------------------------------
    // His architecture decision of 2026-08-17 18:00, carried in the U27 brief: the instrument reads
    // its doors at runtime on the buffer it actually draws on, and the report it hands back is the
    // runtime truth; what the manifest declares is only the claim. `drawn` says which of the two grids
    // the refusal names, since a reader told «a 390 x 30 frame» would look for a device that has none.
    function doorGridOf(st) {
      var bw = Math.round(num(st.bufWidth, 0)), bh = Math.round(num(st.bufHeight, 0));
      if (bw >= 1 && bh >= 1) return { w: bw, h: bh, drawn: true };
      return { w: Math.round(num(st.cssWidth, 0)), h: Math.round(num(st.cssHeight, 0)),
               drawn: false };
    }

    // ---- THE TWO DOORS THIS INSTRUMENT READS FOR ITSELF ------------------------------------------
    //
    // WHAT A DOOR ASKS. At the entry door every point of the frame must show the near work whole and
    // at the exit door the far one whole — `cov` exactly 1 and exactly 0, with no point in between.
    // Two things can put a point in between, and the instrument reads both.
    //
    // ONE · THE FRONT'S OWN MARGIN AGAINST THE PIXEL'S FOOTPRINT. `cov` crosses over inside a band of
    // the plane's rows `foot` wide either side of the front, and `foot` is the projection's own
    // Jacobian times half a buffer point. At a door the plane is flat, so that Jacobian is exactly 1
    // and the footprint is exactly one over the buffer's HEIGHT. The earliest column's front stands
    // `MARGIN` past the plane's own far edge whatever the raggedness is. So the door is whole exactly
    // while
    //     foot  ≤  MARGIN,     i.e.   the buffer stands at least 1/MARGIN points tall.
    // The reading is taken at the frame's own far edge rather than at the outermost sample centre, so
    // it can only ever over-hold by half a point — a door it calls whole is whole beyond argument.
    //
    // THERE IS NO HOLD FOR IT, and that is a fact rather than an omission. The meshing instrument can
    // step its mesh to a neighbouring rung and the material instrument its grain to a neighbouring
    // cell, because in both the leak is set by a handle. Here both sides of the inequality are fixed:
    // MARGIN is the module's own constant inside `reach`, and the footprint is the buffer's own row.
    // No handle this instrument publishes moves either, so a door this reading finds a fault at is
    // refused outright.
    //
    // TWO · THE JUDGES' CHANNEL. `mask` draws this instrument's own coverage as the picture, which is
    // exactly what a door may not be: at a door the coverage is one flat value over the whole frame,
    // so a door drawn with the channel open is a flat field and not a whole work. It rests at nothing,
    // where it costs the picture nothing at all, and the reading is exact rather than held against a
    // number somebody chose — anything above nothing is a door that is not the work.
    function doorReadOf(v, st) {
      var mix = num(st.mix, -1);
      var want = mix === 0 ? 1 : (mix === 1 ? 0 : -1);
      if (want < 0) return null;
      var g = doorGridOf(st);
      if (!(g.w >= 1) || !(g.h >= 1)) return null;
      // the shader's own `foot` at the frame's own far edge, with every term's counterpart in FRAG
      // above: at a door the plane is flat, the push-in is 1 and the Jacobian is 1, so this is the
      // buffer's own half-row doubled — read rather than assumed.
      var inv = v.invRows;
      var spy = want ? 1 : -1;
      var qy = inv[1][0] * 0 + inv[1][1] * spy + inv[1][2];
      var qz = inv[2][0] * 0 + inv[2][1] * spy + inv[2][2];
      var dtdy = (inv[1][1] * qz - qy * inv[1][2]) / Math.max(qz * qz, 1e-9);
      var px = 2 / Math.max(g.h, 1) / Math.max(v.zoom, 1e-9);
      return { grid: g, want: want, foot: Math.max(Math.abs(dtdy) * px * 0.5, 1e-6),
               mask: v.mask };
    }

    // THE REFUSAL, worded the way the host's own manifest refusals read: what is wrong, in this
    // instrument's own measured numbers, on the grid it was measured on.
    function doorWhyNoOf(read) {
      if (!read) return null;
      var g = read.grid, door = read.want ? "the entry" : "the exit";
      if (read.mask > 0) {
        return door + " door leaks: the judges' own channel stands at " + read.mask.toFixed(6)
             + ", so the frame drawn on the " + g.w + " x " + g.h + (g.drawn ? " buffer" : " frame")
             + " is this instrument's own coverage rather than a photograph, and at a door that "
             + "coverage is one flat value over every point of it, where " + door
             + " door's own law asks for the " + (read.want ? "departing" : "arriving")
             + " work whole";
      }
      if (read.foot > MARGIN) {
        return door + " door leaks: on a " + g.w + " x " + g.h
             + (g.drawn ? " buffer" : " frame") + " one point of the frame covers "
             + read.foot.toFixed(4) + " of the plane's own rows, past the " + MARGIN
             + " the front stands beyond the plane's own edge, so this instrument's own mask crosses "
             + "over inside the frame and the " + (read.want ? "arriving" : "departing")
             + " work takes the rows nearest that edge, where " + door
             + " door's own law asks for the " + (read.want ? "departing" : "arriving")
             + " work at every point";
      }
      return null;
    }

    // THE NUMBERS OF ONE FRAME. Everything the shader gets beyond the seating of the two works is a
    // pure function of the pose — the module's own `values()` and `plane()` with the frame's aspect
    // read off the pose instead of off a canvas this file does not own.
    function values(st) {
      var g = doorGridOf(st);
      var aspect = Math.max(g.w, 1) / Math.max(g.h, 1);
      var pl = planeOf(st, aspect);
      var d = pl.dial;
      var inv = inv3(pl.H);
      // A PLANE WITH NO INVERSE DRAWS THE DOOR'S OWN MAP. The module returns from its draw without
      // drawing anything; an instrument that returned no frame values would be refused at
      // registration, so the flat plane's own map stands in its place. It is unreachable at the
      // lean this instrument holds — the determinant only vanishes at a quarter turn and the lean
      // stops at TILT_MAX — and it is written down rather than left to chance.
      if (!inv) inv = [1 / Math.max(pl.D * aspect, 1e-9), 0, 0,
                       0, 1 / Math.max(pl.D, 1e-9), 0,
                       0, 0, 1 / Math.max(pl.D, 1e-9)];
      // the front's raggedness, in the plane's own rows: eight tenths of the handle reaches a
      // sixth of the plane, which is a front the eye reads as broken rather than as a line
      var spread = clamp(num(st.lead, 0), 0, 1) * 0.8;
      // the front travels from beyond the far edge to beyond the near one, so both doors stand a
      // whole work whatever the columns' own moments are
      var reach = 1 + spread * 0.5 + MARGIN;
      // A COUNT OF COLUMNS IS A WHOLE NUMBER by the time it reaches the shader: the shader cuts the
      // plane at `floor(uv.x * uCols)` and spaces the ladder over `uCols - 1`, so a fractional count
      // would leave a sliver column at one edge standing on its own moment.
      var colsWanted = clamp(num(st.columns, COLS), COLS_MIN, COLS_MAX);
      var cols = Math.max(COLS_MIN, Math.round(colsWanted));
      var v = {
        // the three rows of the plane's own inverse, padded to the vec4 the host binds
        inv0: [inv[0], inv[1], inv[2], 0],
        inv1: [inv[3], inv[4], inv[5], 0],
        inv2: [inv[6], inv[7], inv[8], 0],
        zoom: Math.min(zoomFor(pl.corners, pl.aspect), ZOOM_CAP),
        front: reach - 2 * reach * d,
        spread: spread,
        cols: cols,
        off: clamp(num(st.travel, 1), 0, 1) * AMP * 4 * d * (1 - d),
        guard: clamp(num(st.shade, 1), 0, 1) * smoothstep(0, 0.09, d) * smoothstep(1, 0.91, d),
        // read on the diagnostic surface, bound to no uniform: what the handles came to
        dial: d, lean: pl.phi * 180 / Math.PI, camera: pl.D, aspect: aspect, crop: CROP,
        reach: reach, mask: clamp(num(st.mask, 0), 0, 1),
        colsRequest: colsWanted, colsRounded: cols - colsWanted,
        invRows: [[inv[0], inv[1], inv[2]], [inv[3], inv[4], inv[5]], [inv[6], inv[7], inv[8]]],
      };
      var read = doorReadOf(v, st);
      v.doorGrid = read ? read.grid : null;
      v.doorFoot = read ? read.foot : null;
      v.doorWhyNo = doorWhyNoOf(read);
      return v;
    }

    var manifest = {
      id: "tilt", api: 1, arity: 2,
      // The frame comes apart from its own flatness, the middle is a plane going away into depth with
      // a front riding forward over it, and the arriving work stands upright and whole.
      roles: ["disassembly", "mystery", "assembly"],
      // THE LEVEL IS CARRIED, NOT DERIVED. lab/data/module-contract-new.json's own `tilt` row reads
      // «level: WORLD», and its `family` says why: the frame is one projective plane and the boundary
      // is a row of that plane travelling toward the eye — a geometry rather than a field.
      //
      // WHAT DECLARING IT COSTS, said out loud because it is a real consequence. An instrument that
      // declares WORLD spends the crossing's ONE MIRACLE (the composer's own `spendsTheMiracle`,
      // which reads this very line rather than any list of names): folding the space a work lives in
      // is a world act, it consumes the slot, and it never stacks. So a tier whose budget carries no
      // miracle — a quiet link, and every role the composer gives no miracle to — cannot be carried
      // by this instrument at all, and a culmination that spends its miracle here spends it nowhere
      // else. That is the right price for this module: what the visitor watches is the space the
      // photographs live in lying down, not something happening on their surface.
      levels: ["WORLD"],
      // WHAT THIS INSTRUMENT CUTS ON, from §8's own vocabulary.
      //   · `strip` — the handover front travels ROW BY ROW across the tilted plane. Which work a
      //     point shows is decided by that point's own row coordinate against the travelling front,
      //     which is a strip cut and nothing else; the composer's `KIND_OF_MEASURE` reads the same
      //     kind out of a `banding` pivot.
      //   · `field` — the plane itself. It is one surface carrying both works at once, and the
      //     crossing is a change of how much of that one surface each of them owns, so the whole
      //     frame is the element. It is the kind the double-exposure instrument declares, and this
      //     is the second published instrument to cut on it.
      cuts: ["strip", "field"],
      params: { tilt: [0, 1], horizon: [0, 1], squeeze: [0, 1], lead: [0, 1] },
      // EVERY handle a score can drive (§4.4b). `mix` is the dial — the key the module's own contract
      // row names. The four below it are the module's declared params; `columns` is the one constant
      // the port publishes; `seed` is the score's die; `shade` and `travel` are the module's own two
      // judge channels, resting where it rests them, and `mask` is the third in the fleet's idiom.
      //
      // NO `clock` HANDLE, AND THAT IS A DECISION WITH THE MODULE'S OWN RECORD BEHIND IT. The module
      // accumulates a second in its frame loop and takes one through `onParam('clock', …)`, and no
      // uniform of its shader ever reads it: `values()` is a pure function of the hand. Its contract
      // row says the same in one word — `clockMoves: false`, and its `breath.none` reads «no motion
      // of the module's own — the lean, the front and the travel are pure functions of the dial».
      // What DID move on that clock is the life of a live source, which is the carrier half this port
      // could not take (see the header). A handle a score can walk without moving the picture is
      // noise in the score, so none is published and the time that would have reached this instrument
      // reaches it as nothing at all.
      //
      // NO HANDLE HERE KEEPS A CLOCK OR A ROLL OF ITS OWN. The module rolls its own die where a score
      // names no seed (`Math.random()` inside its `seedFrom`); here that case answers with the
      // handle's own rest instead, because an instrument that rolls its own die makes a seeded score
      // draw two different pictures.
      handles: {
        mix: { min: 0, max: 1, def: 0 },
        // THE LEAN. Its two ends are the module's own words: nothing at all is the carrier switched
        // off and the crossing walking a flat picture; whole is TILT_MAX at mid-passage, the most
        // these photographs' window grids survive before the far rows stop resolving.
        tilt: { min: 0, max: 1, def: 0.72,
                unit: "how far the frame lies down into depth",
                applied: { degreesAtMidPassageWhenWhole: TILT_MAX, restsAt: "both doors" },
                reads: "structure.polar.tunnel — how strongly a work already reads as a corridor, "
                     + "the weaker of the pair's two readings, since a lean built on a depth only "
                     + "one work carries is laid on rather than found" },
        // THE LINE THE PLANE TURNS ABOUT. Nothing is a line at the top of the frame — almost all of
        // it goes away into depth; whole is a line at the bottom and the frame leans toward the eye.
        horizon: { min: 0, max: 1, def: 0.35,
                   unit: "where the plane's own axis stands down the frame",
                   reads: "structure.horizon.y — the work's own measured horizon, which is the line "
                        + "the plane should turn about; a work that carries none leaves this at the "
                        + "module's own rest" },
        // HOW HARD THE ROWS CROWD. Nothing stands the camera CAM_FAR half-heights off, where the
        // lean is nearly a shear; whole brings it to CAM_NEAR, where the far rows crowd by one over
        // the depth and the near ones open right out.
        squeeze: { min: 0, max: 1, def: 0.55,
                   unit: "how near the camera stands, in frame half-heights",
                   applied: { halfHeightsAtNothing: CAM_FAR, halfHeightsAtWhole: CAM_NEAR },
                   reads: "texture.spectralPeriodPx over structure.frameSide — the pair's own repeat "
                        + "said as cells across the frame's height, which is what decides how far "
                        + "the far rows may crowd before they stop resolving into anything" },
        // HOW BROKEN THE FRONT IS. Nothing is one straight row travelling forward; whole spreads the
        // columns' own moments over four fifths of the plane.
        lead: { min: 0, max: 1, def: 0.4,
                unit: "how far apart the columns' own moments stand, in the plane's own rows",
                // NO MEASUREMENT NAMES THIS ONE, and it is said rather than filled with the nearest
                // number to hand. How ragged a handover should read is a matter of the crossing's own
                // taste; nothing in a work record measures it, and inventing a reading for it would
                // be a number nobody measured.
                reads: null },
        // THE ONE CONSTANT THE PORT PUBLISHES. The module pins nine columns (tilt.js:176). How many
        // columns a front breaks into is a reading of the pair — it is the count of vertical divisions
        // the works themselves carry — so it travels as a handle rather than as a constant, and it is
        // rounded to a whole count before the shader sees it.
        columns: { min: COLS_MIN, max: COLS_MAX, def: COLS, kind: "enum", step: 1,
                   unit: "how many columns carry their own moment along the front",
                   applied: { roundedToWholeColumns: true, reads: "colsRequest" },
                   reads: "the strip element sets — the count of the bands a work's own structure "
                        + "was measured to fall into across the frame, which is what the front's "
                        + "columns should stand on" },
        seed: { min: 0, max: 8, def: 0 },
        shade: { min: 0, max: 1, def: 1,
                 unit: "the weight of the contact shadow the near work throws over the far one",
                 applied: { atTheFront: 0.34, decaysOverRows: 6, restsAt: "both doors" } },
        travel: { min: 0, max: 1, def: 1,
                  unit: "the weight of the counter-motion inside the plane",
                  applied: { frameUnitsAtMidPassage: AMP, restsAt: "both doors" } },
        // THE JUDGES' THIRD CHANNEL, and the measurement its door is read against. It rests at
        // nothing, where the picture is the module's own; opened it draws this instrument's own
        // coverage, so a law about the coverage is read off the picture. `readAtADoor` says what is
        // read, on which grid, and that there is no hold — at a door the coverage is one flat value
        // over the whole frame, so a door drawn with this channel open is refused outright.
        mask: { min: 0, max: 1, def: 0,
                applied: { readAtADoor: { readOn: "the drawing buffer", reads: "mask",
                                          measures: "this channel itself, and the footprint of one "
                                                  + "buffer point in the plane's own rows against "
                                                  + "the margin the front stands beyond the plane's "
                                                  + "own edge",
                                          held: null } } },
      },
      neutrals: { a: 0, b: 1 },
      doors: { in: { handle: "mix", value: 0, work: "a" },
               out: { handle: "mix", value: 1, work: "b" } },
      // BOTH DOORS FRAME ALIKE. The lean is NOT paid for by a standing crop — the camera pushes in by
      // exactly what the lean costs and that push-in is 1 at both doors — so the only crop either
      // door carries is the counter-motion's own headroom, which is the 1.12 the module's contract
      // row records for it.
      framings: { "0": { coverCrop: CROP }, "1": { coverCrop: CROP } },
      drivers: ["progress", "cueProgress", "time", "velocity", "capability", "noise", "static",
                "curve", "spline", "map", "add", "multiply", "mix", "clamp", "hold", "segment",
                "ramp", "slew", "oscillate", "node"],
      // THE PERSPECTIVE IS INSIDE THIS INSTRUMENT'S OWN SURFACE. The plane leans and the camera
      // pushes in, but both happen in the projection this file builds and neither asks the stage for
      // a point of view, so the witness camera stays the stage's (§6).
      camera: { needs: "none", authority: "stage" },
      gl: { preserveDrawingBuffer: false },
      // THE COVERAGE LAW (§7). The mask the shader already builds to decide which work owns each
      // point is published as the alpha: `1.0 - cov`, the share of the frame the work riding in over
      // the far edge has taken. Both doors stay whole because the front travels MARGIN past the
      // plane's own far and near edges with the raggedness already inside its reach — so the alpha is
      // 0 at every point at the entry door and 1 at every point at the exit door, never a mixture.
      coverage: { writes: true,
                  how: "1.0 - cov, the share of the plane the work riding in over the far edge has "
                     + "taken from the front's travel" },
      // The neutral pose is the ENTRY DOOR — `mix` at 0, the value the `doors` block above names — so
      // the frame keys the host reads off it at registration include the door's own record.
      neutralPose: { mix: 0, tilt: 0.72, horizon: 0.35, squeeze: 0.55, lead: 0.4, columns: COLS,
                     seed: 0, shade: 1, travel: 1, mask: 0, reduced: false,
                     cssWidth: 1000, cssHeight: 1000 },
      passes: [{
        program: "tilt", vert: VERT, frag: FRAG, position: "aPos",
        uniforms: [
          { name: "uA", type: "sampler2D", source: "textureA" },
          { name: "uB", type: "sampler2D", source: "textureB" },
          { name: "uFitA", type: "vec4", source: "fitA" },
          { name: "uFitB", type: "vec4", source: "fitB" },
          { name: "uRes", type: "vec2", source: "resolution" },
          { name: "uInv0", type: "vec4", source: "frame:inv0" },
          { name: "uInv1", type: "vec4", source: "frame:inv1" },
          { name: "uInv2", type: "vec4", source: "frame:inv2" },
          { name: "uZoom", type: "float", source: "frame:zoom" },
          { name: "uFront", type: "float", source: "frame:front" },
          { name: "uSpread", type: "float", source: "frame:spread" },
          { name: "uCols", type: "float", source: "frame:cols" },
          { name: "uOff", type: "float", source: "frame:off" },
          { name: "uGuard", type: "float", source: "frame:guard" },
          { name: "uSeed", type: "float", source: "handle:seed" },
          { name: "uMask", type: "float", source: "handle:mask" },
        ],
      }],
      // The instrument allocates nothing of its own: it spends the two source-texture slots the host
      // already holds and the one programme the host builds from this manifest.
      resources: { lean: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                           passes: 1, bytesEstimate: 0, variant: "lean" },
                   standard: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0,
                               programs: 1, passes: 1, bytesEstimate: 0, variant: "standard" },
                   rich: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                           passes: 1, bytesEstimate: 0, variant: "rich" } },
      capabilities: ["webgl2"],
      decline: ["one work only", "a source that never decoded"],
      provenance: { labPath: "lab/effects/tilt.js", commit: "80bc046" },
      // HOW WELL THIS INSTRUMENT SUITS A PAIR (2026-08-18, his word of 09:51 and its sharpening at
      // 09:53). An instrument no longer answers WHETHER it takes a pair — it answers how well it
      // suits one, so a poor fit is still playable and still explains itself. The arithmetic runs in
      // the composer, which is the one place holding both records; what stands here is the
      // instrument's own statement of WHAT IT READS, which is the fact this file owns.
      //
      // RANKING ONLY. There is no floor here, no minimum and no condition a pair can fail: a fit of
      // nothing ranks last and plays where nothing ranks higher, which is his word of 09:51 — any two
      // photographs in the world get a crossing, and a measurement only ranks which genre suits.
      suits: { reads: ["structure.polar.tunnel", "structure.horizon.y"],
               how: "the whole frame is laid down as one plane going away into depth, so what it "
                  + "suits is a pair with depth to be revealed: the weaker of the two corridor "
                  + "readings is the fit, raised where both works stand a measured horizon of their "
                  + "own for the plane to turn about, because a lean built on a depth only one work "
                  + "carries is laid on rather than found; a pair that reads no depth at all still "
                  + "crosses on it, as a flat ground lying down and coming upright again",
      },
      readiness: "production-ready",
    };

    var live = false;
    return {
      name: "tilt",
      manifest: manifest,
      values: values,
      fit: fit,
      feel: feelOf,
      prepare: function (o) {
        if (!o.sources) return { take: false, why: "the leaning instrument needs both works" };
        if (!o.cue) return { take: false, why: "no cue names it" };
        return { take: true };
      },
      start: function () { live = true; },
      // The pose the shader draws. Every number in it comes from a handle a score can drive.
      //
      // THE REDRAW THE PRESERVED BUFFER STOOD IN FOR. The lab module drew on a parameter change, on a
      // resize and on its own frame loop, and under reduced motion it drew once and stopped —
      // whatever stayed on screen after that was the preserved buffer's doing. Here the host's buffer
      // keeps nothing between frames, so this draws on every frame it is handed, reduced or not.
      // Nothing in this instrument moves with time, so reduced motion changes no number of it.
      //
      // A DOOR THIS INSTRUMENT CANNOT KEEP WHOLE IS REFUSED RATHER THAN DRAWN. The door law is the
      // instrument's own claim (the manifest's coverage line above), so the instrument is what
      // answers for it: at either door it reads its own footprint and its own judges' channel on the
      // buffer the host is about to bind and, on a fault, hands the host the reason with the measured
      // number in it instead of drawing a door that is two works at once — or none. The host recovers
      // the transaction on that reason and the walk's own glide carries the visitor, which is the
      // product's own behaviour with no renderer.
      frame: function (st) {
        if (!live) return;
        var h = st.handles;
        var pose = {
          mix: h.mix, tilt: h.tilt, horizon: h.horizon, squeeze: h.squeeze, lead: h.lead,
          columns: h.columns, seed: h.seed, shade: h.shade, travel: h.travel, mask: h.mask,
          reduced: st.reduced,
          cssWidth: st.viewport.w, cssHeight: st.viewport.h,
          // THE GRID THE SHADER WILL SAMPLE ON, carried into the pose so the door is read on the
          // buffer the host is about to bind as `uRes` rather than on the CSS frame around it. The
          // host settles it from the device ratio and its own resolution step, so it moves while a
          // pass plays and each door is read on the grid standing at that door's own instant.
          bufWidth: st.viewport.bufferW, bufHeight: st.viewport.bufferH,
        };
        // AT A DOOR THE INSTRUMENT SAYS WHAT IT APPLIED, and says it before it refuses. The reading
        // is taken on the buffer this frame is drawn on, so it is the run-time truth his 18:00
        // decision asks for rather than the count the score asked for.
        if (h.mix === 0 || h.mix === 1) {
          var v = values(pose);
          if (st.reportApplied) {
            st.reportApplied({
              door: h.mix === 0 ? "in" : "out",
              buffer: [pose.bufWidth, pose.bufHeight],
              reads: "columns", request: v.colsRequest, applied: v.cols,
              moved: v.colsRounded, unit: "columns",
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
    instrument: tiltInstrument(),
  });
})();
