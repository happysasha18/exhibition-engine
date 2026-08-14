/*!pass-layer.js*/
// The drawing layer's own file — PassHost (PASS-API-V1 §1.2/§2/§7/§12), the renderer's own half of
// the transition. Fetched separately so the walk's bundle stays under its byte fence; the client asks
// for this file once, only when the visualLayer setting asks for it, the device reports WebGL2, and
// the visit runs neither reduced motion nor Save-Data.
//
// Root: his word 2026-08-13 23:03 — carry the woven instrument across first, with a real pair score
// feeding a real instrument.
//
// THREE PARTS LIVE HERE.
//   1. The transaction: idle → offered → armed → running → docked/recovered/cancelled → disposed,
//      the watchdog, the idempotence guard and the token check (§2). Unchanged from the build of
//      2026-08-13 except where the frame half needed a hand.
//   2. The frame half (§1.2/§7): one canvas above the walk, one WebGL2 context with the drawing
//      buffer unpreserved, one vertex buffer, the two source textures of the pair, a programme cache
//      keyed by branch name, the frame loop, the clock handed down as transaction seconds, resize,
//      the resolution ladder, the resource census and context loss/restoration. This is the lab's
//      shared carrier (lab/gl-carrier.js) carried onto the host under the contract's ownership rules,
//      with one difference that matters: the carrier names one instrument's six uniforms literally,
//      and the host binds BY DECLARED NAME from each instrument's manifest instead.
//   3. The instruments: a registry keyed by id. The woven instrument (§8) ships here as an isolated
//      module — its mathematics and its shader carried across from lab/effects/weave.js, its own
//      canvas, context, frame loop and pointer code left behind. A TEST INSTRUMENT registers itself
//      too, reachable only when diagnostics are on (§9's lifecycle rows are built against it).
//
// A command carrying no score reaches no production instrument at all: the score names the cue, the
// cue names the instrument. With no score the walk's own glide runs, which is the standing fallback.
(function () {
  var join = window.__@@NS@@PassLayer;
  if (typeof join !== "function") return;

  // ---- the three ranges of contract §2.5 — a legal value must read differently from a hang -------
  var DURATION_MIN = 0, DURATION_MAX = 14000;
  var PREPARE_MIN = 0, PREPARE_MAX = 400;
  var SLACK_MIN = 0, SLACK_MAX = 2000;
  function clampNum(n, lo, hi) {
    n = Number(n);
    if (!isFinite(n)) n = lo;
    return Math.max(lo, Math.min(hi, n));
  }

  // ---- the renderer half of the diagnostic surface (§9): state, token, lifecycle, refusals, timing
  var log = [];
  function logEvt(name, gen, why) {
    var row = { at: Math.round(performance.now()), name: name, gen: gen, why: why == null ? null : why };
    log.push(row);
    if (log.length > 128) log.shift();
    return row;
  }

  var instruments = {};      // the registry, keyed by instrument id (§7: the render graph is built
                             // from manifests, so one host carries many instruments)
  var probe = null;          // the diagnostics-only test instrument, when one is registered
  var cur = null;            // the current transaction record, or null between transactions
  var lastRun = null;        // what the last transaction left behind for the diagnostic surface:
                             // the camera's rest, its handoffs and the cadence it landed through
  var prepareBudgetMs = 120; // within PREPARE_MIN…PREPARE_MAX; overridable for testing (host.configure)
  var settleSlackMs = 300;   // within SLACK_MIN…SLACK_MAX
  // The two pins are a TESTING seam, set only through host.configure: with a pinned clock and a
  // pinned progress the frame loop stops reading the wall clock, so a seeded run can be compared
  // frame against frame (§9 row 10). A live visit never sets either.
  var pinClock = null, pinProgress = null, fixedScale = false;

  // ================================================================================================
  // THE FRAME STAGE — the host's own hardware, owned by nobody else (§1.2, §7)
  // ================================================================================================
  // The numbers below are the shared carrier's own, carried across unchanged from lab/gl-carrier.js:
  // the release envelope asks for steady 30 frames a second, p95 within 33 ms, so the ladder drops a
  // step above 33 ms and climbs back below 22 ms; a device pixel ratio past two costs memory a
  // full-screen pass never sees back.
  var STEPS = [1.0, 0.85, 0.72, 0.60, 0.50];
  var DPR_CAP = 2, P95_DROP = 33, P95_RAISE = 22, WIN_DROP = 45, WIN_RAISE = 120, KEEP = 240;

  var stage = null;          // {canvas, gl, vao, quad, texA, texB, programs}
  var stepIx = 0, W = 1, H = 1, cssW = 1, cssH = 1, dpr = 1;
  var times = [], changes = 0, sinceChange = 0, lastAt = 0;
  // The census (§7). `stage` counts what the host holds for everyone; `grant` counts what was created
  // for the instrument holding the frame, and that is the half the manifest's declaration is judged
  // against. Bytes are sized from real dimensions, never from an object count.
  var census = { canvases: 0, contexts: 0, textures: 0, buffers: 0, framebuffers: 0,
                 programs: 0, bytes: 0, passesLastFrame: 0, uploads: 0, restores: 0 };
  var grant = { textures: 0, programs: 0, framebuffers: 0, bytes: 0 };
  var declared = null;       // what the running instrument's manifest promised, per variant

  function quantile(sorted, q) {
    if (!sorted.length) return 0;
    var i = (sorted.length - 1) * q;
    var lo = Math.floor(i), hi = Math.ceil(i);
    return lo === hi ? sorted[lo] : sorted[lo] + (sorted[hi] - sorted[lo]) * (i - lo);
  }

  function makeTex(gl) {
    var tx = gl.createTexture();
    census.textures++;
    gl.bindTexture(gl.TEXTURE_2D, tx);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
    return tx;
  }

  // One canvas above the walk, one context, the drawing buffer unpreserved. The canvas is the
  // curtain's own pixels: the product's curtain(on) hides the walk beneath it and this shows it.
  function stageMake() {
    if (stage) return stage;
    var canvas = document.createElement("canvas");
    canvas.setAttribute("aria-hidden", "true");
    canvas.style.cssText = "position:fixed;inset:0;width:100%;height:100%;display:block;" +
      "z-index:2147483000;background:#08080a;pointer-events:none;visibility:hidden;";
    document.body.appendChild(canvas);
    census.canvases++;
    var gl = canvas.getContext("webgl2", {
      antialias: false, alpha: false, depth: false, stencil: false,
      preserveDrawingBuffer: false, powerPreference: "high-performance",
    });
    if (!gl) {
      if (canvas.parentNode) canvas.parentNode.removeChild(canvas);
      census.canvases--;
      return null;
    }
    census.contexts++;
    canvas.addEventListener("webglcontextlost", onContextLost, false);
    canvas.addEventListener("webglcontextrestored", onContextRestored, false);
    stage = { canvas: canvas, gl: gl, vao: null, quad: null, texA: null, texB: null, programs: {} };
    stageBuild();
    return stage;
  }

  // Everything the context itself owns. Split out from stageMake because a restored context has to
  // rebuild exactly this and nothing else (§7's context-loss law).
  function stageBuild() {
    var gl = stage.gl;
    stage.vao = gl.createVertexArray();
    gl.bindVertexArray(stage.vao);
    stage.quad = gl.createBuffer();
    census.buffers++;
    gl.bindBuffer(gl.ARRAY_BUFFER, stage.quad);
    // one triangle covers the frame: a third fewer edge points across the diagonal than two
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
    gl.enableVertexAttribArray(0);
    gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 0, 0);
    gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, false);
    stage.texA = makeTex(gl);
    stage.texB = makeTex(gl);
    stage.programs = {};
    gl.disable(gl.DEPTH_TEST);
    gl.disable(gl.BLEND);
    W = H = 1;
    stageResize();
  }

  function stageShow(on) {
    if (stage) stage.canvas.style.visibility = on ? "visible" : "hidden";
  }

  function stageResize() {
    if (!stage) return;
    cssW = Math.max(1, Math.round(window.innerWidth || 1));
    cssH = Math.max(1, Math.round(window.innerHeight || 1));
    dpr = Math.min(window.devicePixelRatio || 1, DPR_CAP);
    var s = STEPS[stepIx];
    var w = Math.max(1, Math.round(cssW * dpr * s));
    var h = Math.max(1, Math.round(cssH * dpr * s));
    if (w !== W || h !== H) {
      W = w; H = h;
      stage.canvas.width = W;
      stage.canvas.height = H;
      stage.gl.viewport(0, 0, W, H);
    }
  }

  // The measurement belongs to its own resolution: changing the step forgets the frame times, which
  // were taken on a different number of points and say nothing about the new one.
  function changeStep(to) {
    stepIx = to;
    times = [];
    sinceChange = 0;
    changes++;
    stageResize();
  }
  function p95Over(n) {
    if (times.length < n) return null;
    var tail = times.slice(times.length - n).sort(function (a, b) { return a - b; });
    return quantile(tail, 0.95);
  }
  function decideScale() {
    if (fixedScale) return;
    var hot = p95Over(WIN_DROP);
    if (hot !== null && hot > P95_DROP && stepIx < STEPS.length - 1 && sinceChange >= WIN_DROP) {
      changeStep(stepIx + 1); return;
    }
    var cool = p95Over(WIN_RAISE);
    if (cool !== null && cool < P95_RAISE && stepIx > 0 && sinceChange >= WIN_RAISE) {
      changeStep(stepIx - 1);
    }
  }
  function noteFrame(now) {
    if (lastAt) {
      var dt = now - lastAt;
      times.push(dt);
      if (times.length > KEEP) times.shift();
      sinceChange++;
      decideScale();
    }
    lastAt = now;
  }

  // ---- shader version handling (§7) --------------------------------------------------------------
  // The lab modules were written for WebGL 1, where a shader declares varying and writes to
  // gl_FragColor; the host's one context is the second version, so the translation is mechanical and
  // touches no line of mathematics. A module that already ships GLSL ES 3.00 carries its own header,
  // and a second one is a build-time red — so the header is stamped only where none is present, and
  // a source that already has one is handed through untouched.
  function toES3(src, isVert) {
    if (/^\s*#version\b/.test(src)) return src;
    var out = src
      .replace(/\battribute\b/g, "in")
      .replace(/\bvarying\b/g, isVert ? "out" : "in")
      .replace(/\btexture2D\b/g, "texture");
    if (!isVert) {
      out = out.replace(/\bgl_FragColor\b/g, "oColour");
      out = out.replace(/(precision[^\n]*\n)/, "$1out vec4 oColour;\n");
      if (out.indexOf("out vec4 oColour;") < 0) out = "out vec4 oColour;\n" + out;
    }
    return "#version 300 es\n" + out;
  }

  function compile(gl, type, src, what) {
    var s = gl.createShader(type);
    gl.shaderSource(s, src);
    gl.compileShader(s);
    if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) {
      var info = gl.getShaderInfoLog(s);
      gl.deleteShader(s);
      throw new Error(what + ": " + info);
    }
    return s;
  }

  // Programmes live by branch name and outlive every transaction: a second pass over the same branch
  // takes the built programme, so a walk never pays for a shader build twice.
  function programFor(pass) {
    var P = stage.programs;
    if (P[pass.program]) return P[pass.program];
    var gl = stage.gl;
    var vs = compile(gl, gl.VERTEX_SHADER, toES3(pass.vert, true), pass.program + " vertex");
    var fs = compile(gl, gl.FRAGMENT_SHADER, toES3(pass.frag, false), pass.program + " fragment");
    var p = gl.createProgram();
    census.programs++;
    grant.programs++;
    gl.attachShader(p, vs);
    gl.attachShader(p, fs);
    gl.bindAttribLocation(p, 0, pass.position || "aPos");
    gl.linkProgram(p);
    gl.deleteShader(vs);
    gl.deleteShader(fs);
    if (!gl.getProgramParameter(p, gl.LINK_STATUS)) {
      throw new Error(pass.program + " link: " + gl.getProgramInfoLog(p));
    }
    // THE UNIFORM CONTRACT IS NAME-DRIVEN (§7). Every location is looked up by the name the manifest
    // declares — never by position and never from a list written into the host.
    var U = {};
    pass.uniforms.forEach(function (u) { U[u.name] = gl.getUniformLocation(p, u.name); });
    P[pass.program] = { prog: p, U: U };
    return P[pass.program];
  }

  // ---- what the host can supply, and the refusal of anything else (§7) ---------------------------
  var SUPPLY = { textureA: 1, textureB: 1, fitA: 1, fitB: 1, resolution: 1, seconds: 1 };
  var UTYPE = { sampler2D: 1, float: 1, vec2: 1, vec4: 1 };
  function supplySeen(source, provides) {
    if (SUPPLY[source]) return true;
    if (source.indexOf("frame:") === 0) return provides.frame.indexOf(source.slice(6)) >= 0;
    if (source.indexOf("handle:") === 0) return provides.handles.indexOf(source.slice(7)) >= 0;
    return false;
  }

  // A manifest is judged ONCE, at registration (§7: binding by position or by a hardcoded list is
  // refused at registration). Returns the reason it was refused, or null.
  function manifestWhyNo(inst) {
    var m = inst.manifest;
    if (!m) return null;                       // an instrument that draws nothing declares nothing
    if (m.gl && m.gl.preserveDrawingBuffer === true) {
      return "asks for the drawing buffer to be preserved";
    }
    if (!m.passes || !m.passes.length) return "declares no pass";
    var provides = { handles: Object.keys(m.handles || {}), frame: [] };
    try { provides.frame = Object.keys(inst.values(m.neutralPose) || {}); }
    catch (e) { return "its own frame values do not answer a neutral pose"; }
    for (var i = 0; i < m.passes.length; i++) {
      var pass = m.passes[i];
      if (!pass.uniforms || !pass.uniforms.length) return "pass «" + pass.program + "» names no uniform";
      for (var j = 0; j < pass.uniforms.length; j++) {
        var u = pass.uniforms[j];
        if (!u.name) return "a uniform of «" + pass.program + "» has no name";
        if (!UTYPE[u.type]) return "uniform «" + u.name + "» names the unknown type «" + u.type + "»";
        if (!supplySeen(String(u.source), provides)) {
          return "uniform «" + u.name + "» asks for «" + u.source + "», which the host cannot supply";
        }
      }
    }
    return null;
  }

  // ---- one frame ---------------------------------------------------------------------------------
  function bindUniform(gl, loc, u, box) {
    var v;
    if (u.source === "textureA") v = 0;
    else if (u.source === "textureB") v = 1;
    else if (u.source === "fitA") v = box.fitA;
    else if (u.source === "fitB") v = box.fitB;
    else if (u.source === "resolution") v = [W, H];
    else if (u.source === "seconds") v = box.seconds;
    else if (u.source.indexOf("frame:") === 0) v = box.frame[u.source.slice(6)];
    else v = box.handles[u.source.slice(7)];
    if (u.type === "sampler2D") gl.uniform1i(loc, v);
    else if (u.type === "float") gl.uniform1f(loc, Number(v) || 0);
    else if (u.type === "vec2") gl.uniform2f(loc, v[0], v[1]);
    else gl.uniform4f(loc, v[0], v[1], v[2], v[3]);
  }

  // The one draw. The instrument hands its pose; the host asks the instrument's own pure functions
  // for the numbers of the frame and the seating of each work, then binds every declared uniform by
  // its declared name and issues the declared passes.
  function drawPose(inst, pose, src) {
    if (!stage) return;
    stageResize();
    census.passesLastFrame = 0;
    var gl = stage.gl;
    var box = {
      frame: inst.values(pose),
      handles: pose,
      seconds: pose.t,
      fitA: inst.fit(src.aw, src.ah, W, H),
      fitB: inst.fit(src.bw, src.bh, W, H),
    };
    inst.manifest.passes.forEach(function (pass) {
      var p = programFor(pass);
      gl.useProgram(p.prog);
      gl.bindVertexArray(stage.vao);
      gl.activeTexture(gl.TEXTURE0);
      gl.bindTexture(gl.TEXTURE_2D, stage.texA);
      gl.activeTexture(gl.TEXTURE1);
      gl.bindTexture(gl.TEXTURE_2D, stage.texB);
      pass.uniforms.forEach(function (u) {
        var loc = p.U[u.name];
        if (loc !== null && loc !== undefined) bindUniform(gl, loc, u, box);
      });
      gl.drawArrays(gl.TRIANGLES, 0, 3);
      census.passesLastFrame++;
    });
  }

  // ---- the sources: the host arms and decodes both works before takeover (§4.1/§10.1) ------------
  function workImg(id) {
    if (!id) return null;
    var f = document.querySelector('.exh-frame[data-id="' + String(id).replace(/"/g, "") + '"]');
    return f ? f.querySelector("img") : null;
  }
  function decodeOf(im) {
    if (im.loading === "lazy") im.loading = "eager";
    if (im.complete && im.naturalWidth) return Promise.resolve(im);
    if (!im.decode) return Promise.reject(new Error("no decode"));
    return im.decode().then(function () { return im; });
  }
  function armSources(cmd) {
    var a = workImg(cmd.from && cmd.from.id), b = workImg(cmd.to && cmd.to.id);
    if (!a || !b) return Promise.reject(new Error("no picture for " + (a ? "the arriving" : "the departing") + " work"));
    return Promise.all([decodeOf(a), decodeOf(b)]).then(function () {
      return { a: a, b: b, aw: a.naturalWidth, ah: a.naturalHeight,
               bw: b.naturalWidth, bh: b.naturalHeight };
    });
  }
  // The two source textures are the stage's own and survive every change of pair: a new pair is an
  // upload into the same two objects, never two more.
  function uploadPair(src) {
    var gl = stage.gl;
    gl.bindTexture(gl.TEXTURE_2D, stage.texA);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGB, gl.RGB, gl.UNSIGNED_BYTE, src.a);
    gl.bindTexture(gl.TEXTURE_2D, stage.texB);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGB, gl.RGB, gl.UNSIGNED_BYTE, src.b);
    census.uploads++;
    // sized from real dimensions, three bytes a point at RGB/UNSIGNED_BYTE — the size of a thing,
    // which an object count misses entirely (§7)
    census.bytes = (src.aw * src.ah + src.bw * src.bh) * 3;
  }

  // ---- context loss and restoration (§7) ---------------------------------------------------------
  function onContextLost(e) {
    if (e && e.preventDefault) e.preventDefault();
    logEvt("context-lost", cur ? cur.cmd.gen : null, null);
    if (stage) { stage.programs = {}; stage.texA = stage.texB = stage.vao = stage.quad = null; }
    stageShow(false);
    Object.keys(instruments).forEach(function (k) {
      try { if (instruments[k].contextLost) instruments[k].contextLost(); } catch (err) {}
    });
    if (cur && !cur.docked) fail(cur.cmd.gen, "context lost");
  }
  function onContextRestored() {
    logEvt("context-restored", cur ? cur.cmd.gen : null, null);
    census.restores++;
    try { stageBuild(); }
    catch (e) { logEvt("no-rebuild", null, String((e && e.message) || e)); return; }
    Object.keys(instruments).forEach(function (k) {
      var inst = instruments[k];
      if (!inst.contextRestored) return;
      try { inst.contextRestored({ stage: true }); }
      catch (e2) { if (cur) fail(cur.cmd.gen, "no rebuild"); }
    });
  }

  // ================================================================================================
  // DRIVER AST v1 (§5) — A GRAPH OF DATA, EVALUATED
  // ================================================================================================
  // Every node is a plain record and every operator is a named branch of one switch. There is no
  // eval, no new Function and no string that is executed anywhere on this road — a conformance row
  // greps the BUILT file for both and reds on either.
  //
  // TWO RULES THE REVIEWS FOUND NECESSARY.
  //   · NAMED NODES WITH REFERENCES. A cue declares `nodes` by name; anywhere a node is expected a
  //     record `{node:"name"}` stands in its place. One node therefore feeds several channels, which
  //     is exactly what the grammar's fifth law needs — the balance that drives duty, travel
  //     amplitude and the geometric cap at once is ONE node with three readers, not three copies
  //     that can drift apart.
  //   · CYCLES REFUSED AT VALIDATION, WITH THE CYCLE NAMED. A graph is walked once before a command
  //     is taken; a node that reaches itself is refused and the path is written out, so the score's
  //     author reads which three names close the ring rather than watching a frame hang.
  var TAU = Math.PI * 2;

  // The four named curves are the lab engine's own (lab/crossing-engine.js SHAPES), carried across
  // unchanged so one score reads the same on both roads. Not one number here is new.
  var CURVES = {
    linear: function (u) { return u; },
    smooth: function (u) { return u * u * (3 - 2 * u); },
    "in": function (u) { return u * u; },
    out: function (u) { return 1 - (1 - u) * (1 - u); },
  };
  // `oscillate`'s three shapes. The argument is an ANGLE IN RADIANS, so a rate reads in cycles a
  // second and a phase reads in radians — which is how every voice in the lab's own instruments is
  // written (weave.js: `sin(t * 0.021 * TAU + 1.1)`), and a score can therefore carry those numbers
  // across digit for digit instead of through a conversion nobody can check by eye.
  var SHAPES = {
    sin: function (a) { return Math.sin(a); },
    tri: function (a) { var p = a / TAU + 0.25; return 1 - 4 * Math.abs(p - Math.floor(p) - 0.5); },
    "cubed-sin": function (a) { var s = Math.sin(a); return s * s * s; },
  };

  // The one hash the woven instrument's shader already rolls its over/under order from
  // (weave.js hash21, constants 41.317 / 289.107 / 43758.5453). `noise(seed, stream)` uses the same
  // three numbers, so a seeded score and a seeded shader agree about what chance means.
  function noiseOf(seed, stream) {
    var s = Math.sin(Number(seed) * 41.317 + Number(stream) * 289.107) * 43758.5453;
    return s - Math.floor(s);
  }

  // THE MONOTONE SPLINE, Fritsch–Carlson — lab/crossing-engine.js `flowSlopes`/`flowAt` carried over
  // whole. One curve through all of a track's points, so a track changes SPEED as smoothly as it
  // changes value: one tangent per point shared by the segments either side of it, no overshoot and
  // no return, and both end tangents zero so the track rests where it is held. His word 2026-08-11
  // after judging speed steps at segment joints; the same shape belongs here.
  function splineSlopes(pts, get) {
    var n = pts.length, d = [], m = [], i, h, a, b, s;
    for (i = 0; i < n - 1; i++) {
      h = pts[i + 1].at - pts[i].at;
      d.push(h > 0 ? (get(pts[i + 1]) - get(pts[i])) / h : 0);
    }
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
  }
  function splineAt(pts, x, get) {
    var n = pts.length, m, i, a, b, h, u, u2, u3;
    if (!n) return 0;
    if (n === 1 || x <= pts[0].at) return get(pts[0]);
    if (x >= pts[n - 1].at) return get(pts[n - 1]);
    m = splineSlopes(pts, get);
    for (i = 1; i < n - 1; i++) if (x <= pts[i].at) break;
    a = pts[i - 1]; b = pts[i];
    h = b.at - a.at;
    if (h <= 0) return get(b);
    u = (x - a.at) / h; u2 = u * u; u3 = u2 * u;
    return (2 * u3 - 3 * u2 + 1) * get(a) + (u3 - 2 * u2 + u) * h * m[i - 1] +
           (3 * u2 - 2 * u3) * get(b) + (u3 - u2) * h * m[i];
  }
  function pointValue(p) { return p.value; }

  // `hold` and `segment` read the same list of points the same way — held before the first point,
  // held after the last — and differ only in what happens between two of them: `hold` stands still
  // until the next point arrives, `segment` walks there on the named curve of the point it ends at.
  function stepAt(pts, x, curved) {
    var i, a, b, span;
    if (!pts || !pts.length) return 0;
    if (x <= pts[0].at) return pts[0].value;
    for (i = 1; i < pts.length; i++) {
      a = pts[i - 1]; b = pts[i];
      if (x <= b.at) {
        if (!curved) return a.value;
        span = b.at - a.at;
        if (span <= 0) return b.value;
        return a.value + (b.value - a.value) * (CURVES[b.shape] || CURVES.linear)((x - a.at) / span);
      }
    }
    return pts[pts.length - 1].value;
  }

  // The only slots that ever hold another node. `from`, `to`, `points`, `rate`, `phase`, `min` and
  // `max` are plain numbers or plain lists of points and are never walked as graph edges.
  var KID_KEYS = ["in", "a", "b", "t"];
  function eachChild(n, fn) {
    if (!n || typeof n !== "object") return;
    for (var i = 0; i < KID_KEYS.length; i++) {
      var v = n[KID_KEYS[i]];
      if (v === null || v === undefined || typeof v !== "object") continue;
      if (Object.prototype.toString.call(v) === "[object Array]") {
        for (var j = 0; j < v.length; j++) if (v[j] && typeof v[j] === "object") fn(v[j]);
      } else fn(v);
    }
  }

  // THE CYCLE, NAMED. A depth-first walk of every declared node; the moment a name is met that is
  // already on the walk's own stack, the ring is written out from that name back round to itself.
  function cycleIn(nodes) {
    var state = {}, path = [], found = null;
    function inline(spec) {
      if (found || !spec || typeof spec !== "object") return;
      if (spec.node) { named(spec.node); return; }
      eachChild(spec, inline);
    }
    function named(name) {
      if (found) return;
      if (state[name] === 1) {
        found = path.slice(path.indexOf(name)).concat([name]).join(" → ");
        return;
      }
      if (state[name] === 2) return;
      state[name] = 1;
      path.push(name);
      inline(nodes[name]);
      path.pop();
      state[name] = 2;
    }
    Object.keys(nodes || {}).forEach(named);
    return found;
  }

  function okv(v) { return { ok: true, v: v }; }
  function nov(why) { return { ok: false, why: why }; }

  // ONE EVALUATION. `ctx` carries the sources of §5 and the cue's own node table; `spec` is any node
  // record, a `{node:"name"}` reference, or a bare number. A node that cannot answer returns its
  // reason rather than a number, and the caller records the fallback with that reason — silence
  // about an unbuilt field is what makes an unbuilt field dangerous.
  function evalNode(spec, ctx, depth) {
    if (spec === null || spec === undefined) return nov("names no node");
    if (typeof spec === "number") return okv(spec);
    if (typeof spec !== "object") return nov("is not a node record");
    depth = depth || 0;
    if (depth > 64) return nov("the graph is deeper than 64 nodes");
    if (spec.node) {
      var ref = (ctx.nodes || {})[spec.node];
      if (!ref) return nov("names the node «" + spec.node + "», which the cue never declares");
      return evalNode(ref, ctx, depth + 1);
    }
    if (spec.source !== undefined) return evalSource(spec, ctx);
    return evalOp(spec, ctx, depth);
  }

  function evalSource(spec, ctx) {
    switch (spec.source) {
      case "progress": return okv(ctx.progress);
      case "cueProgress": return okv(ctx.cueProgress);
      case "time": return okv(ctx.seconds);
      case "velocity": return okv(ctx.velocity);
      case "capability": return okv(ctx.capability);
      case "noise": return okv(noiseOf(spec.seed, spec.stream));
      // DECLARED AND FALLING BACK TO ITS BASE (§5/§11). One normalised host signal arrives on a
      // later branch; instruments attach no listeners of their own, so until it does there is
      // nothing honest to answer with, and the fallback is recorded with this reason.
      case "pointer":
        return nov("the source «pointer» is declared and one normalised host signal arrives later");
      default:
        return nov("names the source «" + spec.source + "», which the host does not carry");
    }
  }

  function evalList(list, ctx, depth) {
    var out = [];
    if (Object.prototype.toString.call(list) !== "[object Array]") return { ok: false, why: "«in» is not a list" };
    for (var i = 0; i < list.length; i++) {
      var r = evalNode(list[i], ctx, depth + 1);
      if (!r.ok) return r;
      out.push(r.v);
    }
    return { ok: true, list: out };
  }

  function evalOp(spec, ctx, depth) {
    var op = spec.op, i, r, x, c, pts;
    switch (op) {
      case "static":
        return okv(Number(spec.value));

      case "curve":
        c = CURVES[spec.name];
        if (!c) return nov("names the curve «" + spec.name + "» — the host draws linear, smooth, in, out");
        r = evalNode(spec["in"], ctx, depth + 1);
        if (!r.ok) return r;
        x = r.v < 0 ? 0 : r.v > 1 ? 1 : r.v;
        return okv(c(x));

      // The monotone spline: the whole track's own course, the shape his word of 2026-08-11 named
      // after judging speed steps at segment joints.
      case "spline":
        pts = spec.points;
        if (Object.prototype.toString.call(pts) !== "[object Array]" || !pts.length) {
          return nov("a spline is a list of points over its own input");
        }
        r = evalNode(spec["in"] === undefined ? { source: "progress" } : spec["in"], ctx, depth + 1);
        if (!r.ok) return r;
        return okv(splineAt(pts, r.v, pointValue));

      case "hold":
      case "segment":
        pts = spec.points;
        if (Object.prototype.toString.call(pts) !== "[object Array]" || !pts.length) {
          return nov("«" + op + "» is a list of points over its own input");
        }
        r = evalNode(spec["in"] === undefined ? { source: "progress" } : spec["in"], ctx, depth + 1);
        if (!r.ok) return r;
        return okv(stepAt(pts, r.v, op === "segment"));

      case "map":
        r = evalNode(spec["in"], ctx, depth + 1);
        if (!r.ok) return r;
        var f = spec.from || [0, 1], t = spec.to || [0, 1];
        var span = Number(f[1]) - Number(f[0]);
        if (!span) return nov("«map» reads from an empty range");
        return okv(Number(t[0]) + (Number(t[1]) - Number(t[0])) * ((r.v - Number(f[0])) / span));

      case "add":
      case "multiply":
        r = evalList(spec["in"], ctx, depth);
        if (!r.ok) return r;
        x = op === "add" ? 0 : 1;
        for (i = 0; i < r.list.length; i++) x = op === "add" ? x + r.list[i] : x * r.list[i];
        return okv(x);

      case "mix":
        var ra = evalNode(spec.a, ctx, depth + 1); if (!ra.ok) return ra;
        var rb = evalNode(spec.b, ctx, depth + 1); if (!rb.ok) return rb;
        var rt = evalNode(spec.t, ctx, depth + 1); if (!rt.ok) return rt;
        return okv(ra.v + (rb.v - ra.v) * rt.v);

      case "clamp":
        r = evalNode(spec["in"], ctx, depth + 1);
        if (!r.ok) return r;
        var lo = spec.min === undefined ? -Infinity : Number(spec.min);
        var hi = spec.max === undefined ? Infinity : Number(spec.max);
        return okv(r.v < lo ? lo : r.v > hi ? hi : r.v);

      // `ramp`/`slew` is the ONE node that remembers: it carries its own value forward and is
      // allowed to move it by at most `rate` a second. It therefore keeps state per transaction,
      // keyed by the node's place in the score, and a run with a pinned clock holds it perfectly
      // still — which is what keeps the seeded-repeat row honest.
      case "ramp":
      case "slew":
        r = evalNode(spec["in"], ctx, depth + 1);
        if (!r.ok) return r;
        var key = spec.__id || (spec.__id = "slew" + (++slewIds));
        var had = ctx.state[key];
        if (had === undefined) { ctx.state[key] = r.v; return okv(r.v); }
        var step = Math.abs(Number(spec.rate) || 0) * ctx.dt;
        var d = r.v - had;
        if (d > step) d = step; else if (d < -step) d = -step;
        ctx.state[key] = had + d;
        return okv(ctx.state[key]);

      // Almost every instrument's breath is a periodic function of unbounded time, and every named
      // curve above is a bounded monotone shape — which is why the review of 2026-08-13 added this.
      case "oscillate":
        var sh = SHAPES[spec.shape === undefined ? "sin" : spec.shape];
        if (!sh) return nov("names the shape «" + spec.shape + "» — the host plays sin, tri, cubed-sin");
        r = evalNode(spec["in"] === undefined ? { source: "time" } : spec["in"], ctx, depth + 1);
        if (!r.ok) return r;
        return okv(sh(TAU * (Number(spec.rate) || 0) * r.v + (Number(spec.phase) || 0)));

      default:
        return nov("the operator «" + op + "» is declared and drawn by no evaluator yet");
    }
  }
  var slewIds = 0;

  // ================================================================================================
  // THE CAMERA (§6) — one continuous voice with its own arc, resting exactly on B
  // ================================================================================================
  // The pose is ONE RECORD, applied ONCE, BY THE HOST, above whatever the instrument does to its own
  // surface inside the frame. The two never mix: the instrument draws its picture into the host's
  // canvas, and the host then carries that whole canvas through the pose. An instrument that moved
  // the point of view by its own construction would be doubling as a camera, which §6 forbids.
  //
  // Pan is normalised — a fraction of the frame. Pitch, yaw, roll and the field of view are RADIANS.
  // Dolly travels in LOG SPACE and is interpolated there: `logScale` IS the logarithm, so a plain
  // interpolation of it is a geometric interpolation of scale, and the applied factor is exp of it.
  // The existing lab engine interpolates raw scale on both of its paths, which the charter's own law
  // contradicts; the lock states log space and a row proves it.
  var CAM_KEYS = ["panX", "panY", "logScale", "pitch", "yaw", "roll", "fov"];
  var CAM_NEUTRAL = { panX: 0, panY: 0, logScale: 0, pitch: 0, yaw: 0, roll: 0, fov: null };
  // The pose rests on the arriving work within this much. The check READS THE POSE rather than the
  // picture, so the number is a computation tolerance and not a matter of taste: a spline evaluated
  // at its own last point returns that point, and only floating point stands between.
  var CAM_REST_TOL = 1e-6;
  // A handoff between two authorities is continuous within this much, measured on the pose across
  // the handoff frame. Normalised pan and radians share one bar.
  var CAM_HANDOFF_TOL = 1e-3;

  function camRead(p, key) {
    if (key === "panX") return p.pan ? p.pan.x : undefined;
    if (key === "panY") return p.pan ? p.pan.y : undefined;
    return p[key];
  }
  // A track point stands at a second, or at one of the two doors the pass runs between: "a" is the
  // departing work at zero and "b" is the arriving work at the pass's own last second.
  function camWhen(p, durationSec) {
    if (p.at === "a") return 0;
    if (p.at === "b") return durationSec;
    var n = Number(p.at);
    return isFinite(n) ? n : 0;
  }

  // WHO HOLDS THE CAMERA AT THIS INSTANT. The score names the owner per window: a cue carrying the
  // camera by its own device declares `cameraAuthority:"own"`, and across that window the stage's
  // flight holds still. Exactly one owner is returned at every instant — two cues claiming one
  // instant is refused before the command is taken (scoreWhyNo below), so the runtime never has to
  // guess between them.
  function camOwnerAt(score, tSec) {
    var cues = (score && score.cues) || [];
    for (var i = 0; i < cues.length; i++) {
      var c = cues[i], w = c.window || [0, 0];
      if (c.cameraAuthority === "own" && tSec >= w[0] && tSec <= w[1]) return "cue:" + c.id;
    }
    return "stage";
  }
  // THE STAGE'S FLIGHT HOLDS STILL ACROSS AN OWNED WINDOW. Held means its own clock stops, not that
  // its pose freezes and then jumps: resuming at the second the visitor has actually reached would
  // put a step into the flight, and a camera cut is the wipe under another name.
  // The second an owned window opens or closes — the instant a handoff is judged at.
  function camEdge(score, ownerName, entering) {
    var id = ownerName && ownerName.indexOf("cue:") === 0 ? ownerName.slice(4) : null;
    var cues = (score && score.cues) || [];
    for (var i = 0; i < cues.length; i++) {
      if (cues[i].id === id) { var w = cues[i].window || [0, 0]; return entering ? w[0] : w[1]; }
    }
    return null;
  }
  function camStageClock(score, tSec) {
    var cues = (score && score.cues) || [], spent = 0;
    for (var i = 0; i < cues.length; i++) {
      var c = cues[i], w = c.window || [0, 0];
      if (c.cameraAuthority !== "own" || tSec <= w[0]) continue;
      spent += Math.min(tSec, w[1]) - w[0];
    }
    return tSec - spent;
  }

  // The stage's own pose at a second: one monotone spline per place, held before the first point and
  // after the last. A place no point names a number for stands at its neutral, and the fallback is
  // recorded with its reason — `fov` has no identity value, so a track that never names one leaves
  // the field of view unapplied rather than inventing an angle.
  function camStagePose(score, tSec, durationSec, say) {
    var cam = (score && score.camera) || null;
    var track = cam && cam.track;
    var pose = { panX: 0, panY: 0, logScale: 0, pitch: 0, yaw: 0, roll: 0, fov: null };
    if (Object.prototype.toString.call(track) !== "[object Array]" || !track.length) {
      if (say) say("camera", "the score names no camera track; the stage rests at the neutral pose");
      return pose;
    }
    var pts = track.map(function (p) { return { at: camWhen(p, durationSec), p: p }; });
    pts.sort(function (a, b) { return a.at - b.at; });
    CAM_KEYS.forEach(function (k) {
      var all = true;
      for (var i = 0; i < pts.length; i++) {
        if (typeof camRead(pts[i].p, k) !== "number") { all = false; break; }
      }
      if (!all) {
        if (say) say("camera:" + k, "no point names a number for «" + k + "»; it stands at its neutral");
        pose[k] = CAM_NEUTRAL[k];
        return;
      }
      pose[k] = splineAt(pts, tSec, function (q) { return camRead(q.p, k); });
    });
    return pose;
  }

  // WHICH PLACES THIS DEVICE CAN CARRY. Pan, dolly and roll are a plain affine of the frame and every
  // device the host runs on carries them. Pitch, yaw and the field of view need the perspective road,
  // and §7's degrade ladder lightens the score FIRST — so the `lean` variant drops those three and
  // records the fallback. Which axes lean drops is a taste call and is named as a question.
  function camCaps(variant) {
    var deep = variant !== "lean";
    return { panX: true, panY: true, logScale: true, roll: true, pitch: deep, yaw: deep, fov: deep };
  }

  // The pose, applied. One transform on the host's own canvas, above every pixel the instrument drew.
  function camApply(pose, caps) {
    if (!stage) return;
    if (!pose) { stage.canvas.style.transform = ""; return; }
    var s = Math.exp(caps.logScale ? pose.logScale : 0);
    var deg = 180 / Math.PI;
    var t = "";
    if (caps.fov && typeof pose.fov === "number" && pose.fov > 0) {
      t += "perspective(" + (0.5 * Math.max(cssH, 1) / Math.tan(pose.fov / 2)).toFixed(3) + "px) ";
    }
    t += "translate(" + (caps.panX ? pose.panX * 100 : 0).toFixed(4) + "%,"
       + (caps.panY ? pose.panY * 100 : 0).toFixed(4) + "%) ";
    if (caps.pitch && pose.pitch) t += "rotateX(" + (pose.pitch * deg).toFixed(4) + "deg) ";
    if (caps.yaw && pose.yaw) t += "rotateY(" + (pose.yaw * deg).toFixed(4) + "deg) ";
    if (caps.roll && pose.roll) t += "rotate(" + (pose.roll * deg).toFixed(4) + "deg) ";
    t += "scale(" + s.toFixed(6) + ")";
    stage.canvas.style.transformOrigin = "50% 50%";
    stage.canvas.style.transform = t;
  }

  function camOff(a, b) {
    var worst = 0;
    CAM_KEYS.forEach(function (k) {
      var x = typeof a[k] === "number" ? a[k] : 0, y = typeof b[k] === "number" ? b[k] : 0;
      var d = Math.abs(x - y);
      if (d > worst) worst = d;
    });
    return worst;
  }

  // ================================================================================================
  // THE TWO GEOMETRIES PER DOOR (§6) — the whole frame, and the box the work hangs in
  // ================================================================================================
  // The immersive geometry is the fullscreen scene, which is the neutral pose. The HANG geometry is
  // the work's real box in the exhibition layout at that instant, measured off the DOM by the
  // product and handed down through the offer's own hooks — the renderer holds no reference to the
  // adapter, only the one function it was given.
  //
  // THE POSE THAT LAYS ONE ONTO THE OTHER IS A PLAIN PAN AND A DOLLY, and that is a fact about the
  // two roads rather than a convenience. The walk seats a work inside its box without cropping it,
  // so the box carries the work's own aspect; the instrument cover-fits the work into the frame and
  // then pulls in by its own framing headroom, so the work's WHOLE extent inside the frame carries
  // that same aspect. Two rectangles of one shape are carried onto each other by one scale, and the
  // pose record of §6 needs no new place to say it.
  //
  // The extent is read from the instrument's OWN fit rather than recomputed here. `fit` answers the
  // share of the source the frame shows, so the whole work spans 1/share frames. Asking the
  // instrument keeps the two seatings identical by construction, framing headroom and all.
  function hangPoseOf(geom, inst, iw, ih) {
    if (!geom || !geom.w || !geom.h || cssW <= 0 || cssH <= 0) return null;
    var f;
    try { f = inst.fit(iw, ih, W, H); } catch (e) { return null; }
    if (!f) return null;
    var shareX = Math.abs(f[0]), shareY = Math.abs(f[1]);
    if (!shareX || !shareY) return null;
    var ew = cssW / shareX, eh = cssH / shareY;     // the work's whole extent, in frame points
    var k = geom.w / ew;
    if (!isFinite(k) || k <= 0) return null;
    return {
      panX: (geom.x + geom.w / 2 - cssW / 2) / cssW,
      panY: (geom.y + geom.h / 2 - cssH / 2) / cssH,
      logScale: Math.log(k), pitch: 0, yaw: 0, roll: 0, fov: null,
      // What the two readings of one scale disagree by. Both roads keep the work's aspect, so this
      // stands at zero; it is written down rather than asserted, because a layout that began to crop
      // would show up here as a number instead of as a soft edge nobody can name.
      aspectOff: +Math.abs(geom.h / eh - k).toFixed(9),
    };
  }

  // THE FLIGHT'S TWO ENDS ARE THE TWO HANGS. A passage leaves the departing work exactly where it
  // hangs, rises to the whole frame for the crossing itself, and comes back down onto the arriving
  // work's own box. The rise and the fall are seconds a score may name; with none named they take a
  // share of the pass at either end, and the whole middle stands at the neutral pose.
  var HANG_SHARE = 0.18;
  function hangEdges(rec) {
    var cam = (rec.cmd && rec.cmd.score && rec.cmd.score.camera) || {}, h = cam.hang || {};
    var dur = rec.duration / 1000, half = dur / 2;
    var rise = Number(h.rise), fall = Number(h.fall);
    if (!isFinite(rise) || rise < 0) rise = dur * HANG_SHARE;
    if (!isFinite(fall) || fall < 0) fall = dur * HANG_SHARE;
    return { rise: Math.min(rise, half), fall: Math.min(fall, half), dur: dur };
  }

  // The anchor at one second: one monotone spline per place through four points — the departing
  // hang, the whole frame, the whole frame again, the arriving hang. The two middle points hold the
  // same value, so the spline's own slopes there are zero and the crossing plays at the whole frame
  // without drifting through it.
  function anchorPose(rec, tSec) {
    var A = rec.hangPoseA, B = rec.hangPoseB;
    if (!A && !B) return null;
    var e = rec.hangEdge || hangEdges(rec), N = CAM_NEUTRAL;
    var at = [0, e.rise, e.dur - e.fall, e.dur];
    var poses = [A || N, N, N, B || N];
    var out = {};
    CAM_KEYS.forEach(function (k) {
      if (k === "fov") { out[k] = null; return; }
      var pts = [], i;
      for (i = 0; i < 4; i++) {
        pts.push({ at: at[i], value: typeof poses[i][k] === "number" ? poses[i][k] : 0 });
      }
      out[k] = splineAt(pts, tSec, pointValue);
    });
    return out;
  }

  // A REFRAME IS CARRIED, NEVER CUT. When the frame changes size or turns, the destination box moves
  // and the anchor moves with it. The distance between the pose the old geometry read at that
  // instant and the pose the new one reads is held as a carry and spent down across the rest of the
  // flight: the picture goes on from where it actually was, and it still arrives on the exact box,
  // because at the end the carry is zero and the rest reads the hang pose to the last decimal.
  function carryWeight(rec, tSec) {
    if (!rec.carry) return 0;
    var e = rec.hangEdge, span = e ? e.dur - rec.carryFrom : 0;
    if (!(span > 0)) return 0;
    var u = (tSec - rec.carryFrom) / span;
    return u <= 0 ? 1 : u >= 1 ? 0 : 1 - CURVES.smooth(u);
  }

  // Where the pose actually stands: the anchor the host holds, plus what the score's own track says
  // on top of it, plus whatever a reframe is still spending down. A transaction with no hang
  // geometry and no carry hands the track back untouched, which is what every bench row reads.
  function camCompose(anchor, track, carry, weight) {
    if (!anchor && !carry) return track;
    var out = {};
    CAM_KEYS.forEach(function (k) {
      if (k === "fov") { out[k] = typeof track[k] === "number" ? track[k] : null; return; }
      var t = typeof track[k] === "number" ? track[k] : 0;
      var a = (anchor && typeof anchor[k] === "number") ? anchor[k] : 0;
      var c = (carry && typeof carry[k] === "number") ? carry[k] : 0;
      out[k] = a + t + c * weight;
    });
    return out;
  }

  // Both boxes, read now. The product measures; the host only asks and seats.
  function readHang(rec) {
    var ask = rec.hooks && rec.hooks.hangGeometry;
    if (typeof ask !== "function" || !rec.src || !rec.inst) return;
    var aId = rec.cmd.from && rec.cmd.from.id, bId = rec.cmd.to && rec.cmd.to.id;
    try { rec.hangA = aId ? ask(aId) : null; } catch (e) { rec.hangA = null; }
    try { rec.hangB = bId ? ask(bId) : null; } catch (e) { rec.hangB = null; }
    rec.hangPoseA = hangPoseOf(rec.hangA, rec.inst, rec.src.aw, rec.src.ah);
    rec.hangPoseB = hangPoseOf(rec.hangB, rec.inst, rec.src.bw, rec.src.bh);
    if (!rec.hangPoseB && !rec.said.hang) {
      rec.said.hang = true;
      logEvt("hang-fallback", rec.cmd.gen,
             "the arriving work reports no box; the pass rests at the whole frame");
    }
  }

  // THE WALK IS RE-HUNG UNDER COVER. Until the walk moves, the arriving work's box sits a viewport
  // away from where that work actually hangs, because a takeover returns before the walk's own glide
  // ever runs. The one moment the walk can be placed without the eye seeing it move is the middle of
  // the passage, where the anchor stands at the whole frame and the canvas covers everything. The
  // product does the placing; the host then asks for the arriving box again and gets a measured
  // truth instead of a predicted one, and the descent lands on that.
  function placeUnderCover(rec, seconds) {
    if (rec.placed || !rec.hangEdge || typeof rec.hooks.handoff !== "function") return;
    var e = rec.hangEdge;
    if (seconds < (e.rise + (e.dur - e.fall)) / 2) return;
    rec.placed = true;
    try { rec.hooks.handoff(rec.cmd, true); } catch (err) { return; }
    rec.lastSeconds = seconds;
    reseatHang(rec);
  }

  // Re-read both boxes and hold the difference, so a resize or a turn mid-passage moves the
  // destination without putting a step into the flight.
  function reseatHang(rec) {
    if (!rec || !rec.src) return;
    var before = anchorPose(rec, rec.lastSeconds);
    var held = rec.carry, w = carryWeight(rec, rec.lastSeconds);
    rec.hangEdge = hangEdges(rec);
    readHang(rec);
    var after = anchorPose(rec, rec.lastSeconds);
    if (!before || !after) return;
    rec.carry = {};
    CAM_KEYS.forEach(function (k) {
      if (k === "fov") return;
      var b = typeof before[k] === "number" ? before[k] : 0;
      var a = typeof after[k] === "number" ? after[k] : 0;
      rec.carry[k] = b - a + ((held && typeof held[k] === "number") ? held[k] * w : 0);
    });
    rec.carryFrom = rec.lastSeconds;
    logEvt("reframe-hang", rec.cmd.gen, "the destination box moved; the pose is carried across it");
  }

  // The camera of ONE INSTANT, whoever holds it. A cue that owns the camera reports its pose each
  // frame; the host applies THAT and holds its own flight still. A cue that owns the camera and then
  // stops reporting hands authority back at the pose it last reported — authority never lapses into
  // nobody's hands.
  function camPoseAt(rec, tSec) {
    var score = rec.cmd.score || {}, durationSec = rec.duration / 1000;
    var owner = camOwnerAt(score, tSec);
    var track = camStagePose(score, camStageClock(score, tSec), durationSec, function (what, why) {
      if (rec.said["cam:" + what]) return;
      rec.said["cam:" + what] = true;
      logEvt("camera-fallback", rec.cmd.gen, what + ": " + why);
    });
    // The score's own track rides ON the anchor the host holds between the two hangs, so a score
    // that rests at its neutral leaves both ends exact and a score that flies still departs from
    // the departing work's own box and arrives on the arriving one's.
    var anchor = anchorPose(rec, tSec);
    rec.lastAnchor = anchor;
    var stagePose = camCompose(anchor, track, rec.carry, carryWeight(rec, tSec));
    var pose = stagePose;
    if (owner !== "stage") pose = rec.ownPose || rec.lastPose || stagePose;
    // THE HANDOFF ITSELF, MEASURED. §6: at a handoff instant the two poses must agree within a
    // stated tolerance. What is compared is therefore the pose the OUTGOING authority reads at this
    // instant against the pose the INCOMING one reads at the same instant — never this frame against
    // the frame before it, which would count one frame of ordinary flight as a discontinuity. The
    // host writes the distance it actually saw onto the diagnostic surface, so the row reads a
    // number rather than a claim. The very first frame has no authority behind it and is no handoff.
    if (owner !== rec.camOwner) {
      if (rec.camOwner !== null) {
        // Measured AT THE WINDOW'S OWN EDGE, never at whichever frame happened to land past it —
        // otherwise a slower frame rate would read as a bigger discontinuity, and the tolerance
        // would be measuring the device instead of the score.
        var edge = camEdge(score, owner === "stage" ? rec.camOwner : owner, owner !== "stage");
        var at = edge === null ? tSec : edge;
        // Measured on the pose as APPLIED, anchor and carry included, so the two authorities are
        // compared on the same footing rather than one of them reading a bare track.
        var there = camCompose(anchorPose(rec, at),
                               camStagePose(score, camStageClock(score, at), durationSec, null),
                               rec.carry, carryWeight(rec, at));
        var off = camOff(there, rec.ownPose || there);
        rec.handoffs.push({ at: +at.toFixed(4), from: rec.camOwner, to: owner,
                            off: +off.toFixed(9), within: off <= CAM_HANDOFF_TOL });
        if (off > CAM_HANDOFF_TOL) {
          logEvt("camera-handoff-jump", rec.cmd.gen,
                 rec.camOwner + " → " + owner + " moves the pose by " + off.toFixed(6));
        }
      }
      rec.camOwner = owner;
    }
    rec.lastPose = pose;
    return { owner: owner, pose: pose, stage: stagePose };
  }

  // ================================================================================================
  // THE TRANSACTION (§2)
  // ================================================================================================
  function register(inst) {
    if (!inst) return false;
    var why = manifestWhyNo(inst);
    if (why) {
      logEvt("manifest-refused", null, (inst.name || "unnamed") + ": " + why);
      return false;
    }
    instruments[inst.name] = inst;
    if (inst.probe) probe = inst;
    return true;
  }

  // This slice plays ONE cue, the woven instrument's own single gesture; a stack of cues sharing a
  // window is the next unit, and §4.4's levels law is what will judge it.
  function cueOf(cmd) {
    var s = cmd && cmd.score;
    if (!s || !s.cues || !s.cues.length) return null;
    return s.cues[0];
  }
  // THE SCORE, JUDGED ONCE, BEFORE ANYTHING IS TAKEN (§5/§6). Returns the reason it is refused, or
  // null. Two things are checked here because both are properties of the WHOLE score and neither can
  // be seen from inside a single frame: a driver graph that reaches itself, and two cues both
  // claiming the camera at one instant.
  function scoreWhyNo(cmd) {
    var s = cmd && cmd.score;
    if (!s) return null;
    var cues = s.cues || [], i, j;
    for (i = 0; i < cues.length; i++) {
      var ring = cycleIn(cues[i].nodes || {});
      if (ring) return "cue «" + cues[i].id + "» draws a cycle: " + ring;
    }
    var own = [];
    for (i = 0; i < cues.length; i++) if (cues[i].cameraAuthority === "own") own.push(cues[i]);
    for (i = 0; i < own.length; i++) {
      for (j = i + 1; j < own.length; j++) {
        var a = own[i].window || [0, 0], b = own[j].window || [0, 0];
        if (a[0] <= b[1] && b[0] <= a[1]) {
          return "cues «" + own[i].id + "» and «" + own[j].id + "» both carry the camera across "
               + Math.max(a[0], b[0]) + "…" + Math.min(a[1], b[1]) + " s — one authority at a time";
        }
      }
    }
    return null;
  }

  function pick(cmd) {
    var cue = cueOf(cmd);
    if (!cue) return probe;              // no score: only the diagnostics probe can take a command
    var id = cue.instrument && cue.instrument.id;
    if (instruments[id]) return instruments[id];
    logEvt("no-instrument", cmd.gen, String(id));
    return null;
  }
  function durationOf(cmd) {
    var s = cmd && cmd.score;
    if (s && s.duration !== undefined) return clampNum(s.duration, DURATION_MIN, DURATION_MAX);
    var p = cmd && cmd.params && cmd.params.flightMs;
    return clampNum(p ? p.base : 0, DURATION_MIN, DURATION_MAX);
  }
  // §7's quality tier finally gains a consumer: the host reads it at prepare, picks the variant and
  // records the decision with its reason.
  function variantOf(cmd) {
    var t = cmd && cmd.params && cmd.params.qualityTier;
    var name = t ? t.base : "standard";
    return name === "rich" || name === "lean" ? name : "standard";
  }

  // The census against the declaration (§7). The instrument declared textures, framebuffers and a
  // byte estimate; the host counts what was actually created FOR IT and shows both, so a declaration
  // that understates its counts or its bytes reads as the lie it is.
  function grantRow() {
    var d = declared || {};
    return {
      declared: d, granted: { textures: grant.textures, programs: grant.programs,
                              framebuffers: grant.framebuffers, bytes: grant.bytes },
      over: (grant.textures > (d.textures || 0) || grant.programs > (d.programs || 0)
             || grant.framebuffers > (d.framebuffers || 0) || grant.bytes > (d.bytesEstimate || 0)),
    };
  }

  // The two boxes and the flight between them, as the diagnostic surface reads them: what was
  // measured at either end, the pose each box asks for, the seconds the rise and the fall take, and
  // whatever a reframe is still spending down.
  function hangRow(rec) {
    if (!rec) return null;
    return { a: rec.hangA || null, b: rec.hangB || null,
             poseA: rec.hangPoseA || null, poseB: rec.hangPoseB || null,
             edge: rec.hangEdge || null, carry: rec.carry || null,
             carryFrom: rec.carryFrom === undefined ? null : rec.carryFrom };
  }

  // Every exit from `running` ends in exactly one dock (§2.4/row 25/row 1) — `finish` is the single
  // place that can make that true, since it is the only place that ever sets `docked`.
  function finish(landState, why) {
    var rec = cur;
    if (!rec || rec.docked) return;
    rec.docked = true;
    clearTimeout(rec.watchdogT);
    clearTimeout(rec.deadlineT);
    if (rec.raf) { cancelAnimationFrame(rec.raf); rec.raf = 0; }
    // THE CAMERA RESTS ON THE ARRIVING WORK'S OWN BOX. What the last pose is measured against is the
    // HANG pose of the arriving work — the pose that lays the immersive frame exactly onto the box
    // the work hangs in. The neutral pose is the special case of that, where the box is the whole
    // frame, so a transaction with no hang geometry reads exactly as it always did. The row reads
    // the POSE rather than the picture, and stays honest when the picture changes.
    var restAt = rec.hangPoseB || CAM_NEUTRAL;
    rec.rest = { off: +camOff(rec.lastPose || CAM_NEUTRAL, restAt).toFixed(9),
                 tol: CAM_REST_TOL, owner: rec.camOwner,
                 on: rec.hangPoseB ? "hang" : "neutral", hang: rec.hangB || null };
    rec.rest.rested = rec.rest.off <= CAM_REST_TOL;
    if (!rec.rest.rested) {
      logEvt("camera-not-rested", rec.cmd.gen,
             "the last pose stands " + rec.rest.off.toFixed(6) + " from the " + rec.rest.on + " pose");
    }
    lastRun = { camera: rec.camera || null, rest: rec.rest, handoffs: rec.handoffs,
                cadence: rec.cadence || null, handles: rec.lastHandles || null,
                hang: hangRow(rec) };
    logEvt(landState, rec.cmd.gen, why || null);
    // THE HANDOFF, INSIDE ONE FRAME. The DOM's work is revealed and the canvas released in that
    // order, inside one task, so no frame draws neither picture. The canvas at rest already carries
    // the very pixels the DOM carries, so there is nothing to fade between and nothing is faded.
    // The transform is cleared only once the canvas is gone: clearing it while the canvas still
    // stood would snap it back to the whole frame for one frame, which is the flash itself.
    try {
      if (rec.hooks.handoff) rec.hooks.handoff(rec.cmd);
      else rec.hooks.curtain(false);
    } catch (e) {}
    stageShow(false);
    camApply(null, rec.caps);
    try { rec.hooks.dock(rec.cmd); } catch (e) {}
    try { rec.hooks.mark("host-" + landState, rec.cmd, why || null); } catch (e) {}
    try { if (rec.inst && rec.inst.dispose) rec.inst.dispose(); } catch (e) {}
    cur = null;
  }

  // Both settle and fail are token-checked against the CURRENT transaction's own generation (§2.3),
  // and both are idempotent (§2.4): a call that misses either check changes nothing and is recorded
  // as stale rather than silently dropped.
  function settle(token) {
    if (!cur || cur.docked || token !== cur.cmd.gen || cur.state !== "running") {
      logEvt("stale-settle", token, null);
      return;
    }
    finish("docked", null);
  }
  function fail(token, why) {
    if (!cur || cur.docked || token !== cur.cmd.gen) {
      logEvt("stale-fail", token, why || null);
      return;
    }
    finish("recovered", why || "fail");
  }

  function declineCurrent(rec, why) {
    if (cur !== rec) return;
    logEvt("declined", rec.cmd.gen, why);
    cur = null;
    try { rec.hooks.glide(rec.cmd); } catch (e) {}
  }

  function watchdogFire(rec) {
    if (cur !== rec || rec.docked) return;
    logEvt("watchdog", rec.cmd.gen, "no settle");
    fail(rec.cmd.gen, "no settle");
  }

  // ---- the handles a score drives (§4.4b / §5) ----------------------------------------------------
  // Every handle the instrument publishes is read through the driver graph above. A handle the score
  // leaves untracked falls back to the manifest's own default and the fallback is recorded with its
  // reason — which is the treatment every unbuilt driver kind gets, and is what keeps §4.4b's
  // determinism row honest: a handle that kept its own clock would make that row red and the row
  // would name the handle.
  //
  // A handle marked `open` in the manifest is one the instrument can answer for itself (the woven
  // instrument derives its balance from `mix` when no score drives `bal` directly). It is left
  // UNDEFINED rather than defaulted when the score names no track, and no fallback is recorded,
  // because nothing fell back.
  function driverCtx(rec, progress, seconds, dt) {
    var cue = rec.cue || {}, w = cue.window || [0, rec.duration / 1000];
    var span = (w[1] - w[0]) || 1;
    return {
      nodes: cue.nodes || {},
      progress: progress,
      cueProgress: Math.max(0, Math.min(1, (seconds - w[0]) / span)),
      seconds: seconds,
      velocity: Number(rec.cmd.velocity) || 0,
      // The capability, as one number a curve can read: the three named tiers in their own order.
      capability: rec.variant === "rich" ? 1 : rec.variant === "lean" ? 0 : 0.5,
      dt: dt || 0,
      state: rec.driverState,
    };
  }
  function handlesOf(rec, progress, seconds, dt) {
    var m = rec.inst.manifest, cue = rec.cue, out = {};
    var ctx = driverCtx(rec, progress, seconds, dt);
    Object.keys(m.handles).forEach(function (k) {
      var h = m.handles[k], got = null;
      if (cue && cue.tracks && cue.tracks[k]) got = evalNode(cue.tracks[k], ctx, 0);
      if (!got || !got.ok) {
        if (h.open && !(cue && cue.tracks && cue.tracks[k])) { out[k] = undefined; return; }
        if (!rec.said[k]) {
          rec.said[k] = true;
          logEvt("handle-fallback", rec.cmd.gen, k + ": " + ((got && got.why) || "the score drives it with no track"));
        }
        out[k] = h.def;
      } else {
        out[k] = clampNum(got.v, h.min, h.max);
      }
    });
    rec.lastHandles = out;
    return out;
  }

  // ---- the interruption cadence (§2.5 / §11) ------------------------------------------------------
  // WHAT STOOD HERE BEFORE was a hard stop: a cancel resolved the transaction inside one call and the
  // picture jumped to whatever the curtain dropped on. §2.5 and the charter's nineteenth shelf ask for
  // the other thing — on an interruption every handle TRAVELS to its nearest door through its own
  // envelope, inside the score's own budget, and the transition then lands. The host force-ends at the
  // deadline, so a slow envelope can no more strand the visitor than a silent instrument can.
  var CADENCE_MIN = 0, CADENCE_MAX = 2000;

  function budgetOf(cmd) {
    var s = cmd && cmd.score, i = s && s.interruption;
    return clampNum(i && i.withinMs !== undefined ? i.withinMs : 0, CADENCE_MIN, CADENCE_MAX);
  }

  // WHICH DOOR THE VISITOR IS NEAREST. The cue names its two doors by ONE handle and its two values;
  // whichever value the live handle stands nearer is the door the cadence walks to. The whole
  // transition picks one door — every handle then travels to the value IT takes at that door, so the
  // picture that lands is a whole work and never a mongrel of two.
  function nearestDoorOf(rec, live) {
    var cue = rec.cue || {}, doors = cue.doors || {};
    var din = doors["in"], dout = doors.out;
    if (!din || !dout || din.handle !== dout.handle) return null;
    var k = din.handle, at = Number(live[k]);
    if (!isFinite(at)) return null;
    var toIn = Math.abs(at - Number(din.value)), toOut = Math.abs(at - Number(dout.value));
    var which = toIn <= toOut ? "in" : "out";
    var seconds = (cue.window || [0, rec.duration / 1000])[which === "in" ? 0 : 1];
    var progress = which === "in" ? 0 : 1;
    // Every handle at the door: its own track read at the door's own instant, with the door handle
    // itself pinned to exactly the value the door names.
    var want = handlesOf(rec, progress, seconds, 0);
    var at_door = {};
    Object.keys(want).forEach(function (h) { at_door[h] = want[h]; });
    at_door[k] = clampNum(doors[which].value, rec.inst.manifest.handles[k].min,
                          rec.inst.manifest.handles[k].max);
    return { which: which, handle: k, value: Number(doors[which].value), handles: at_door,
             progress: progress, seconds: seconds };
  }

  // Each handle travels on its OWN envelope. A cue may name one per handle in `cadence` — any of the
  // four named curves — and a handle the cue says nothing about walks on `smooth`, which leaves and
  // arrives at rest.
  function envelopeFor(cue, handle) {
    var named = cue && cue.cadence ? cue.cadence[handle] : null;
    return CURVES[named] || CURVES.smooth;
  }

  function cadenceStart(rec, reason, immediate) {
    var live = rec.lastHandles || handlesOf(rec, rec.lastProgress || 0, rec.lastSeconds || 0, 0);
    var door = nearestDoorOf(rec, live);
    var budget = immediate ? 0 : budgetOf(rec.cmd);
    rec.cadence = {
      reason: reason, budget: budget, forced: !!immediate,
      door: door ? door.which : null, doorHandle: door ? door.handle : null,
      seconds: door ? door.seconds : undefined,
      from: live, to: door ? door.handles : live,
      t0: performance.now(), landedInMs: null, ended: false, atDoor: null,
    };
    if (!door) {
      logEvt("cadence-no-door", rec.cmd.gen,
             "the cue names no pair of doors on one handle; the handles hold where they stand");
    }
    logEvt("cadence", rec.cmd.gen,
           reason + " → door «" + (door ? door.which : "none") + "» within " + budget + " ms");
    try { if (rec.inst && rec.inst.cancel) rec.inst.cancel(reason); } catch (e) {}
    if (budget <= 0) { cadenceEnd(rec, "at once"); return; }
    rec.deadlineT = setTimeout(function () { cadenceEnd(rec, "deadline"); }, budget);
  }

  // Where every handle stands part-way through the cadence.
  function cadenceHandles(rec, now) {
    var c = rec.cadence, cue = rec.cue;
    var u = c.budget > 0 ? Math.max(0, Math.min(1, (now - c.t0) / c.budget)) : 1;
    var out = {};
    Object.keys(c.to).forEach(function (k) {
      var a = c.from[k], b = c.to[k];
      if (typeof a !== "number" || typeof b !== "number") { out[k] = b; return; }
      out[k] = a + (b - a) * envelopeFor(cue, k)(u);
    });
    return { handles: out, u: u };
  }

  function cadenceEnd(rec, why) {
    if (!rec.cadence || rec.cadence.ended) return;
    var c = rec.cadence;
    c.ended = true;
    c.landedInMs = Math.round(performance.now() - c.t0);
    // ONE LAST FRAME, ON THE DOOR ITSELF, so the picture the curtain drops on is the door and not
    // wherever the envelope had reached when the deadline arrived. This is what makes the host's
    // force-end at the deadline a landing rather than a cut.
    if (rec.inst && rec.inst.manifest && !rec.docked) {
      try { playFrame(rec, c.seconds === undefined ? (rec.lastSeconds || 0) : c.seconds,
                      rec.lastProgress || 0, 0, c.to); }
      catch (e) { logEvt("cadence-frame-threw", rec.cmd.gen, String((e && e.message) || e)); }
    }
    // EVERY HANDLE AT A DOOR, written down as a number rather than asserted. The last frame put each
    // handle on its envelope's own end; this is the distance that actually remained.
    c.atDoor = {};
    Object.keys(c.to).forEach(function (k) {
      var want = c.to[k], is = (rec.lastHandles || {})[k];
      c.atDoor[k] = { want: want, is: is,
                      off: (typeof want === "number" && typeof is === "number")
                        ? +Math.abs(want - is).toFixed(9) : null };
    });
    clearTimeout(rec.deadlineT);
    logEvt("cadence-end", rec.cmd.gen, why + " in " + c.landedInMs + " ms");
    finish("cancelled", c.reason);
  }

  // ---- the frame loop ----------------------------------------------------------------------------
  // One frame of the instrument, with the camera's pose applied by the host above whatever the
  // instrument drew. `hold` is the cadence's own handle set when a cadence is playing; a cadence
  // frame is `pinned`, so the instrument walks to the door on the host's envelope instead of
  // settling of its own accord half-way through it.
  function playFrame(rec, seconds, progress, dt, hold) {
    var cam = camPoseAt(rec, seconds);
    rec.camera = cam;
    rec.inst.frame({
      token: rec.cmd.gen, t: seconds, progress: progress,
      handles: hold || handlesOf(rec, progress, seconds, dt),
      viewport: { w: cssW, h: cssH, dpr: dpr },
      reduced: !!rec.cmd.reduced,
      camera: cam.pose,
      // a pinned run is a bench run: it holds its pose instead of walking to the end door, so a
      // conformance row can photograph one instant twice and compare it to itself
      pinned: pinProgress !== null || !!hold,
      draw: function (pose) { drawPose(rec.inst, pose, rec.src); },
      // A cue that carries the camera by its own device reports its pose here, once a frame. The
      // host applies it and holds its own flight still across that window.
      reportPose: function (p) { if (p) rec.ownPose = p; },
      settle: settle, fail: fail,
    });
    camApply(cam.pose, rec.caps);
    if (hold) rec.lastHandles = hold;
  }

  function runFrame(rec, now) {
    if (cur !== rec || rec.docked) return;
    rec.raf = requestAnimationFrame(function (t) { runFrame(rec, t); });
    noteFrame(now);
    var dt = rec.lastNow ? (now - rec.lastNow) / 1000 : 0;
    rec.lastNow = now;
    var seconds = pinClock !== null ? pinClock : (now - rec.t0) / 1000;
    var progress = pinProgress !== null ? pinProgress
      : (rec.duration > 0 ? Math.min(1, (now - rec.t0) / rec.duration) : 1);
    rec.lastSeconds = seconds;
    rec.lastProgress = progress;
    placeUnderCover(rec, seconds);
    try {
      if (rec.cadence && !rec.cadence.ended) {
        var walk = cadenceHandles(rec, now);
        playFrame(rec, seconds, progress, dt, walk.handles);
        if (walk.u >= 1) cadenceEnd(rec, "on its own envelope");
        return;
      }
      playFrame(rec, seconds, progress, dt, null);
    } catch (e) {
      logEvt("frame-threw", rec.cmd.gen, String((e && e.message) || e));
      fail(rec.cmd.gen, "frame threw");
    }
  }

  // offer(cmd, hooks) — the ONE bridge the bundle calls. Returns true the moment the host has taken
  // responsibility for landing this command, whether by eventually taking over or by calling the
  // glide hook itself on decline; it never means a renderer is now drawing.
  function offer(cmd, hooks) {
    var inst = pick(cmd);
    if (!inst) return false;
    // THE GRAPH IS WALKED BEFORE THE COMMAND IS TAKEN. A cycle, or two cues claiming the camera at
    // one instant, is refused here with its own reason rather than met half-way through a frame.
    var no = scoreWhyNo(cmd);
    if (no) {
      logEvt("score-refused", cmd.gen, no);
      try { hooks.glide(cmd); } catch (e) {}
      return true;
    }
    if (cur) cancel("superseded", true);   // defensive: declare's own supersede already ended the
                                     // bundle's OWN bookkeeping; this keeps the host's record in step
    var duration = durationOf(cmd);
    var budget = clampNum(prepareBudgetMs, PREPARE_MIN, PREPARE_MAX);
    var slack = clampNum(settleSlackMs, SLACK_MIN, SLACK_MAX);
    var cue = cueOf(cmd);
    var variant = variantOf(cmd);
    var rec = { cmd: cmd, hooks: hooks, inst: inst, cue: cue, variant: variant, state: "offered",
                docked: false, watchdogT: null, duration: duration, raf: 0, t0: 0, src: null,
                said: {}, driverState: {}, lastHandles: null, lastNow: 0,
                lastSeconds: 0, lastProgress: 0,
                caps: camCaps(variant), camOwner: null, camera: null, lastPose: null, ownPose: null,
                handoffs: [], cadence: null, deadlineT: null, rest: null,
                // the two boxes, the pose each asks for, the flight's own edges, and the carry a
                // reframe leaves behind — all null until prepare has read them
                hangA: null, hangB: null, hangPoseA: null, hangPoseB: null, hangEdge: null,
                lastAnchor: null, carry: null, carryFrom: 0, placed: false };
    cur = rec;
    logEvt("offer", cmd.gen, inst.name + " at " + variant);
    var answered = false;
    var budgetTimer = setTimeout(function () {
      if (answered || cur !== rec) return;
      answered = true;
      logEvt("prepare-timeout", cmd.gen, "over " + budget + "ms");
      declineCurrent(rec, "prepare timeout");
    }, budget);

    function onAnswer(res) {
      if (answered || cur !== rec) return;
      answered = true;
      clearTimeout(budgetTimer);
      if (!res || res.take !== true) { declineCurrent(rec, (res && res.why) || "declined"); return; }
      rec.state = "armed";
      logEvt("armed", cmd.gen, null);
      // Everything that can still fail happens BEFORE the curtain: `armed` sits before takeover, and
      // a decline there costs the visitor nothing (§2.1).
      if (inst.manifest) {
        try {
          if (!stageMake()) { declineCurrent(rec, "no webgl2"); return; }
          uploadPair(rec.src);
          inst.manifest.passes.forEach(function (pass) { programFor(pass); });
        } catch (e) {
          logEvt("stage-threw", cmd.gen, String((e && e.message) || e));
          declineCurrent(rec, "stage threw");
          return;
        }
        declared = (inst.manifest.resources || {})[variant] || null;
        // BOTH BOXES ARE READ BEFORE TAKEOVER (§1.1). The host asks the product for the hang
        // geometry of A and of B here, while `armed` still sits before the curtain, so the very
        // first frame it draws can stand on A's own box rather than on the whole frame.
        rec.hangEdge = hangEdges(rec);
        readHang(rec);
      }
      // The curtain goes up BEFORE start, and stays there. `start` can end the whole transaction
      // inside its own call — an instrument that fails at once does exactly that — and a curtain
      // raised afterwards would be raised over a transaction that had already landed and lowered it.
      try { hooks.curtain(true); } catch (e) {}
      rec.state = "running";
      rec.t0 = performance.now();
      logEvt("running", cmd.gen, null);
      try { inst.start(cmd.gen); }
      catch (e) { logEvt("start-threw", cmd.gen, String((e && e.message) || e)); fail(cmd.gen, "start threw"); return; }
      if (inst.manifest && cur === rec && !rec.docked) {
        lastAt = 0;
        // THE FIRST FRAME IS DRAWN BEFORE THE CANVAS IS SHOWN. §2.2 asks that the first frame after
        // start be a complete picture of A at its door, and this sharpens it to A at its HANG box:
        // showing an unpainted canvas would put one frame of its own clear colour between the walk
        // and the passage, which is the blank frame the conformance row measures. Painted first, the
        // canvas appears already carrying A, seated exactly where the DOM hangs it.
        try { playFrame(rec, 0, 0, 0, null); }
        catch (e) {
          logEvt("frame-threw", cmd.gen, String((e && e.message) || e));
          fail(cmd.gen, "frame threw");
          return;
        }
        stageShow(true);
        runFrame(rec, performance.now());
      }
      rec.watchdogT = setTimeout(function () { watchdogFire(rec); }, duration + slack);
    }

    function ask() {
      try {
        var res = inst.prepare({ cmd: cmd, token: cmd.gen, duration: duration, budgetMs: budget,
                                 score: cmd.score || null, cue: cue, variant: variant,
                                 sources: rec.src, grant: declaredFor(inst, variant) });
        if (res && typeof res.then === "function") {
          res.then(onAnswer, function () { onAnswer({ take: false, why: "prepare rejected" }); });
        } else {
          onAnswer(res);
        }
      } catch (e) {
        if (!answered) { answered = true; clearTimeout(budgetTimer); declineCurrent(rec, "prepare threw"); }
      }
    }

    // The host owns every FrameSource and decodes both works during prepare, so an instrument that
    // takes a command receives sources already decoded (§4.1/§10.1).
    if (inst.manifest) {
      armSources(cmd).then(function (src) {
        if (answered || cur !== rec) return;
        rec.src = src;
        ask();
      }, function (e) {
        if (answered || cur !== rec) return;
        answered = true;
        clearTimeout(budgetTimer);
        declineCurrent(rec, String((e && e.message) || e));
      });
    } else {
      ask();
    }
    return true;
  }
  function declaredFor(inst, variant) {
    return inst.manifest ? ((inst.manifest.resources || {})[variant] || null) : null;
  }

  // cancel(reason) — an interruption (§2.2/§10.3/§2.5). Before takeover it is a plain decline, and
  // that costs the visitor nothing. Running, the CADENCE plays: every handle travels to its nearest
  // door through its own envelope inside the score's own budget, and the transition then lands
  // through the SAME single dock every other exit uses.
  //
  // `immediate` collapses the envelope to nothing. It is the supersede's own road: §2.5 wants the
  // cadence played before the next command declares, but the product's declare is synchronous and
  // this branch leaves the product side untouched, so a superseded transition puts every handle ON
  // its door in one step instead of walking there. Every handle still lands at a door; only the
  // walking is skipped, and the record says so (`forced`). Playing the full cadence ahead of a
  // supersede needs the bundle's declare to become deferrable, which is named as a question.
  function cancel(reason, immediate) {
    if (!cur || cur.docked) return;
    if (cur.state === "offered") { declineCurrent(cur, reason || "cancelled"); return; }
    if (cur.cadence) { if (immediate) cadenceEnd(cur, "superseded mid-cadence"); return; }
    if (!cur.inst || !cur.inst.manifest) {
      // an instrument that draws nothing has no handle to walk and no door to walk to
      try { if (cur.inst && cur.inst.cancel) cur.inst.cancel(reason); } catch (e) {}
      finish("cancelled", reason || "cancelled");
      return;
    }
    cadenceStart(cur, reason || "cancelled", !!immediate);
  }

  // A resize or an orientation change reaches here through the product's own reframe road (§10.3).
  // The frame is resized, the destination box is re-read, and the pose is carried across the change
  // instead of stepping — the transaction goes on rather than being replaced.
  function resize(viewport) {
    stageResize();
    if (cur && cur.state === "running") {
      reseatHang(cur);
      if (cur.inst && cur.inst.resize) { try { cur.inst.resize(viewport); } catch (e) {} }
    }
  }
  function contextLost() {
    Object.keys(instruments).forEach(function (k) {
      if (instruments[k].contextLost) { try { instruments[k].contextLost(); } catch (e) {} }
    });
    if (cur && !cur.docked) fail(cur.cmd.gen, "context lost");
  }
  function contextRestored(resources) {
    Object.keys(instruments).forEach(function (k) {
      var inst = instruments[k];
      if (!inst.contextRestored) return;
      try { inst.contextRestored(resources); } catch (e) { fail(cur ? cur.cmd.gen : null, "no rebuild"); }
    });
  }
  function configure(opts) {
    if (!opts) return;
    if (opts.prepareBudgetMs !== undefined) prepareBudgetMs = clampNum(opts.prepareBudgetMs, PREPARE_MIN, PREPARE_MAX);
    if (opts.settleSlackMs !== undefined) settleSlackMs = clampNum(opts.settleSlackMs, SLACK_MIN, SLACK_MAX);
    if (opts.clockPin !== undefined) pinClock = opts.clockPin === null ? null : Number(opts.clockPin);
    if (opts.progressPin !== undefined) pinProgress = opts.progressPin === null ? null : Number(opts.progressPin);
    if (opts.fixedScale !== undefined) fixedScale = !!opts.fixedScale;
  }
  function report() {
    var s = times.slice().sort(function (a, b) { return a - b; });
    return {
      state: cur ? cur.state : "idle",
      active: !!cur,
      gen: cur ? cur.cmd.gen : null,
      duration: cur ? cur.duration : null,
      variant: cur ? cur.variant : null,
      prepareBudgetMs: prepareBudgetMs, settleSlackMs: settleSlackMs,
      events: log.slice(),
      instrument: cur ? cur.inst.name : null,
      registered: Object.keys(instruments),
      // §7's census, both halves side by side on the one surface
      census: { canvases: census.canvases, contexts: census.contexts, textures: census.textures,
                buffers: census.buffers, framebuffers: census.framebuffers,
                programs: census.programs, programsCached: stage ? Object.keys(stage.programs).length : 0,
                bytes: census.bytes, passesLastFrame: census.passesLastFrame,
                uploads: census.uploads, restores: census.restores,
                preserveDrawingBuffer: stage ? stage.gl.getContextAttributes().preserveDrawingBuffer : null,
                buffer: W + "x" + H, scale: STEPS[stepIx], changes: changes, dpr: dpr },
      resources: grantRow(),
      // §9's inspector: the drivers with their evaluated values, the camera with its authority and
      // its pose, the handoffs it measured, and the cadence an interruption landed through. What the
      // last transaction left behind stays readable after it has gone, so a row can read a landing.
      handles: cur ? cur.lastHandles : (lastRun ? lastRun.handles : null),
      camera: cur ? cur.camera : (lastRun ? lastRun.camera : null),
      camCaps: cur ? cur.caps : null,
      rest: cur ? cur.rest : (lastRun ? lastRun.rest : null),
      // the two geometries of §6 as they were actually measured, so a row reads the boxes the pass
      // departed from and arrived on rather than the ones it was meant to
      hang: cur ? hangRow(cur) : (lastRun ? lastRun.hang : null),
      handoffs: cur ? cur.handoffs : (lastRun ? lastRun.handoffs : []),
      cadence: cur ? cur.cadence : (lastRun ? lastRun.cadence : null),
      camTolerances: { rest: CAM_REST_TOL, handoff: CAM_HANDOFF_TOL },
      frames: { count: s.length, p95: +quantile(s, 0.95).toFixed(2), p50: +quantile(s, 0.5).toFixed(2) },
    };
  }

  var host = {
    name: "pass-host",
    offer: offer, resize: resize, cancel: cancel,
    contextLost: contextLost, contextRestored: contextRestored,
    settle: settle, fail: fail, register: register, configure: configure, report: report,
  };

  // ================================================================================================
  // THE WOVEN INSTRUMENT (§8) — lab/effects/weave.js carried across
  // ================================================================================================
  // What came over: the shader, the seating of a work in the frame (coverFit), the response curve
  // (feelOf), the turn of the weave (rotForTime) and the numbers of one frame (frameValuesOf). Not
  // one number changed; this is the same mathematics, standing on the host's frame.
  //
  // What stayed behind: its own canvas, its own WebGL 1 context, its own frame loop, its pointer and
  // resize listeners, its 2D fallback and its own clock. The instrument here reads no wall clock,
  // holds no listener, creates no context and loads no picture (§1.2's fence).
  function weaveInstrument() {
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
      "uniform float uT;",
      "uniform float uNv;",
      "uniform float uDuty;",
      "uniform float uAmp;",
      "uniform float uRot;",
      "uniform float uSpeed;",
      "uniform float uSeed;",
      "const float TAU = 6.28318530718;",
      "vec2 into(vec2 p, vec4 f){",
      "  return clamp((p - 0.5) * f.xy + 0.5 + f.zw, 0.0008, 0.9992);",
      "}",
      "vec3 texA(vec2 p){ return texture2D(uA, into(p, uFitA)).rgb; }",
      "vec3 texB(vec2 p){ return texture2D(uB, into(p, uFitB)).rgb; }",
      "float sqI(float t, float d){ return floor(t) * d + min(fract(t), d); }",
      "float sqcov(float x, float d, float w){",
      "  w = max(w, 1e-5);",
      "  if (d >= 1.0) return 1.0;",
      "  if (d <= 0.0) return 0.0;",
      "  return clamp((sqI(x + w, d) - sqI(x - w, d)) / (2.0 * w), 0.0, 1.0);",
      "}",
      "float hash21(vec2 p){ return fract(sin(dot(p, vec2(41.317, 289.107))) * 43758.5453); }",
      "float warpV(float x, float k, float ph){ return x + 0.42 * sin(k * TAU * x + ph) / (k * TAU); }",
      "float warpD(float x, float k, float ph){ return 1.0 + 0.42 * cos(k * TAU * x + ph); }",
      "void main(){",
      "  vec2 uv = vUv;",
      "  float aspect = uRes.x / max(uRes.y, 1.0);",
      "  float av = clamp(2.0 - 2.0 * uRot, 0.0, 1.0);",
      "  float ah = clamp(2.0 * uRot, 0.0, 1.0);",
      "  float basket = min(av, ah);",
      "  float nV = max(5.0, uNv * (1.0 - 0.25 * basket));",
      "  float nH = max(3.0, nV / max(aspect, 0.05));",
      "  float phV = uT * 0.31;",
      "  float phH = uT * 0.24 + 1.7;",
      "  float alive = smoothstep(0.0, 0.10, uDuty) * smoothstep(1.0, 0.90, uDuty);",
      "  float aV1 = TAU * (uv.y * 1.7 - uT * 0.090);",
      "  float aV2 = TAU * (uv.y * 3.1 + uT * 0.062 + 1.3);",
      "  float edgeV = alive * (0.34 * sin(aV1) + 0.17 * sin(aV2));",
      "  float dEdgeV = alive * TAU * (0.34 * 1.7 * cos(aV1) + 0.17 * 3.1 * cos(aV2));",
      "  float aH1 = TAU * (uv.x * 1.6 + uT * 0.081);",
      "  float aH2 = TAU * (uv.x * 2.9 - uT * 0.055 + 0.7);",
      "  float edgeH = alive * (0.34 * sin(aH1) + 0.17 * sin(aH2));",
      "  float dEdgeH = alive * TAU * (0.34 * 1.6 * cos(aH1) + 0.17 * 2.9 * cos(aH2));",
      "  float cV = warpV(uv.x, 2.0, phV) * nV + edgeV;",
      "  float cH = warpV(uv.y, 3.0, phH) * nH + edgeH;",
      "  float iv = floor(cV), fv = fract(cV);",
      "  float ih = floor(cH), fh = fract(cH);",
      "  float wV = 0.5 * (nV * warpD(uv.x, 2.0, phV) / uRes.x + abs(dEdgeV) / uRes.y);",
      "  float wH = 0.5 * (nH * warpD(uv.y, 3.0, phH) / uRes.y + abs(dEdgeH) / uRes.x);",
      "  float ph = uT * uSpeed * 0.17;",
      "  float offV = uAmp * sin(TAU * (ph + (iv + 0.5) / nV * 1.5 + 0.35 * hash21(vec2(iv, uSeed))));",
      "  float offH = uAmp * sin(TAU * (ph * 0.86 + (ih + 0.5) / nH * 1.5 + 0.31 + 0.35 * hash21(vec2(uSeed, ih))));",
      "  float push = 2.0 * basket * uDuty * (1.0 - uDuty);",
      "  float dutyV = clamp(uDuty + push, 0.0, 1.0);",
      "  float dutyH = clamp(uDuty - push, 0.0, 1.0);",
      "  float guardV = smoothstep(0.0, 0.12, dutyV) * smoothstep(1.0, 0.88, dutyV);",
      "  float guardH = smoothstep(0.0, 0.12, dutyH) * smoothstep(1.0, 0.88, dutyH);",
      "  float covV = sqcov(cV, dutyV, wV);",
      "  vec3 colV = mix(texB(uv + vec2(0.0, -offV)), texA(uv + vec2(0.0, offV)), covV);",
      "  float swV = max(4.0 * wV, min(0.12, 0.35 * min(dutyV, 1.0 - dutyV)));",
      "  float parV = step(0.5, mod(iv, 2.0));",
      "  float onBv = exp(-max(fv - dutyV, 0.0) / swV) * (1.0 - covV);",
      "  float onAv = exp(-max(dutyV - fv, 0.0) / swV) * covV;",
      "  colV *= 1.0 - 0.34 * guardV * mix(onBv, onAv, parV);",
      "  float covH = sqcov(cH, dutyH, wH);",
      "  vec3 colH = mix(texB(uv + vec2(-offH, 0.0)), texA(uv + vec2(offH, 0.0)), covH);",
      "  float swH = max(4.0 * wH, min(0.12, 0.35 * min(dutyH, 1.0 - dutyH)));",
      "  float parH = step(0.5, mod(ih, 2.0));",
      "  float onBh = exp(-max(fh - dutyH, 0.0) / swH) * (1.0 - covH);",
      "  float onAh = exp(-max(dutyH - fh, 0.0) / swH) * covH;",
      "  colH *= 1.0 - 0.34 * guardH * mix(onBh, onAh, parH);",
      "  float bv = floor(iv * 0.5), bh = floor(ih * 0.5);",
      "  float pV = av / max(av + ah, 1e-4);",
      "  float parity = step(mod(bv + bh, 2.0), 0.5);",
      "  float chooseB = clamp(parity + (2.0 * uDuty - 1.0), 0.0, 1.0);",
      "  float choose = mix(pV, chooseB, basket);",
      "  float ord = mix(0.5 * ((bv * 2.0 + 1.0) / nV + (bh * 2.0 + 1.0) / nH),",
      "                  hash21(vec2(bv, bh) + uSeed), 0.4);",
      "  float showV = step(ord * 0.996 + 0.002, choose);",
      "  vec3 col = mix(colH, colV, showV);",
      "  float fbv = fract(cV * 0.5), fbh = fract(cH * 0.5);",
      "  float grooveV = 1.0 - smoothstep(0.0, 0.05, min(fv, 1.0 - fv));",
      "  float grooveH = 1.0 - smoothstep(0.0, 0.05, min(fh, 1.0 - fh));",
      "  float diveV = 1.0 - smoothstep(0.0, 0.16, min(fbh, 1.0 - fbh));",
      "  float diveH = 1.0 - smoothstep(0.0, 0.16, min(fbv, 1.0 - fbv));",
      "  float shade = mix(0.55 * diveH + 0.30 * grooveH, 0.55 * diveV + 0.30 * grooveV, showV);",
      "  float shadeGate = smoothstep(0.0, 0.22, uDuty) * smoothstep(1.0, 0.78, uDuty);",
      "  col *= 1.0 - basket * shadeGate * min(shade, 0.62);",
      "  gl_FragColor = vec4(col, 1.0);",
      "}",
    ].join("\n");

    function smoothstep(a, b, x) {
      var t = (x - a) / (b - a);
      t = t < 0 ? 0 : t > 1 ? 1 : t;
      return t * t * (3 - 2 * t);
    }
    function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }

    // How far a ribbon may slide along its own axis, as a fraction of the frame. Every sample the
    // shader takes is the frame coordinate pushed by at most TRAVEL, so the cover-fit is pulled in by
    // TRAVEL at each end: ZOOM is derived from TRAVEL and is not a free number.
    var AMP = 0.10, PRESS = 1.30, TRAVEL = AMP * PRESS, ZOOM = 1 + 2 * TRAVEL + 0.03;

    // cover-fit a work into the frame, then pull in by the travel headroom. The host hands the
    // source's own dimensions, so the instrument never touches an image object.
    function fit(iw, ih, w, h) {
      var fa = w / Math.max(h, 1);
      var ia = iw / Math.max(ih, 1);
      var sx, sy;
      if (ia > fa) { sx = fa / ia; sy = 1; } else { sx = 1; sy = ia / fa; }
      return [sx / ZOOM, sy / ZOOM, 0, 0];
    }

    var AXES = ["up and down", "side to side", "both"];
    function axisNameOf(axis) {
      if (typeof axis === "number") return AXES[clamp(Math.round(axis), 0, 2)];
      return AXES.indexOf(axis) >= 0 ? axis : "both";
    }
    function rotForTime(time, axis) {
      var a = axisNameOf(axis);
      if (a === "up and down") return 0;
      if (a === "side to side") return 1;
      var p = (time / 27) % 1;
      if (p < 0) p += 1;
      return 0.5 * smoothstep(0.06, 0.16, p) + 0.5 * smoothstep(0.28, 0.38, p)
        - 0.5 * smoothstep(0.56, 0.66, p) - 0.5 * smoothstep(0.78, 0.88, p);
    }

    // THE RESPONSE CURVE (darkroom draft D2): equal movements of the hand produce equal felt change.
    // A two-piece exponential hinged at the median of the felt change of one half, mirrored about the
    // middle because a whole work stands at either end. The dead bands at either end are what make
    // both doors exact: at mix 0 the duty is a whole 1 and at mix 1 a whole 0.
    var FEEL_D0 = 0.06, FEEL_C = 0.43, FEEL_K1 = -1.6, FEEL_K2 = 1.8;
    function feelLog(x, k) {
      return Math.abs(k) < 1e-6 ? x : (Math.exp(k * x) - 1) / (Math.exp(k) - 1);
    }
    function feelKnee(u) {
      return u <= 0.5 ? FEEL_C * feelLog(2 * u, FEEL_K1)
                      : FEEL_C + (1 - FEEL_C) * feelLog(2 * u - 1, FEEL_K2);
    }
    function feelOf(u) {
      var f = u <= 0.5 ? 0.5 * feelKnee(2 * u) : 1 - 0.5 * feelKnee(2 - 2 * u);
      return FEEL_D0 + (1 - 2 * FEEL_D0) * f;
    }

    // The numbers of one frame: everything the shader gets beyond the seating of the two works is a
    // pure function of the pose. The host calls this; so does the lab's own carrier, from the same
    // source — which is why the two roads can be compared frame against frame.
    function values(st) {
      var ab = Math.abs(st.bal);
      var shaped = (st.bal < 0 ? -1 : 1) * smoothstep(0.08, 0.88, ab);
      var duty = 0.5 + 0.5 * shaped;
      var weave = 1 - smoothstep(0.14, 0.86, ab);
      return {
        duty: duty,
        amp: Math.min(AMP * weave * st.press, TRAVEL),
        nV: clamp(st.strips * st.nMul * clamp(st.cssWidth / 1000, 0.5, 1), 6, 64),
        rot: st.reduced ? 0 : rotForTime(st.t, st.axis),
      };
    }

    var manifest = {
      id: "weave", api: 1, arity: 2,
      roles: ["disassembly", "mystery", "assembly"],
      levels: ["SURFACE", "CELL"],
      params: { strips: [8, 64], axis: [0, 2], speed: [0.1, 2.5] },
      // EVERY handle a score can drive (§4.4b). `mix` is the dial; `clock` is the second the host
      // hands down; the other four were the module's own params and its own die, and they are
      // published here so no handle keeps a clock or a roll of its own.
      //
      // THE THREE THAT ANSWERED TO NO TRACK, brought across 2026-08-14. The module ran these on its
      // own eased clock, so under a scored run they kept moving on wall time and one seed gave a
      // different picture (§4.4b names exactly this defect):
      //   · `nMul` — THE STRIP-COUNT BREATH. The module drifts it as 1 + 0.35·sin(t·0.021·TAU + 1.1)
      //     when nobody drives, and the hand reaches 0.62 … 1.65 across the frame (weave.js:452,
      //     :443). Those two ends are the module's own, so they are the range here.
      //   · `press` — THE PRESS RESPONSE. It eases toward PRESS = 1.30 held down and back to 1 let
      //     go (weave.js:236, :466). Resting at 1 is what the module itself does under a parked
      //     pointer, so 1 is the default and 1.30 the far end.
      //   · `bal` — THE BALANCE ITSELF, which the module drifts as 0.97·sin(t·0.030·TAU)³ when no
      //     dial holds it (weave.js:450–451). It is OPEN: a score that names no track for it leaves
      //     the instrument deriving the balance from `mix` through the response curve, exactly as
      //     the module lets its own dial win over the drift (weave.js:459). Nothing falls back, so
      //     nothing is recorded as a fallback.
      handles: {
        mix: { min: 0, max: 1, def: 0 },
        clock: { min: 0, max: 14, def: 0 },
        strips: { min: 8, max: 64, def: 28 },
        axis: { min: 0, max: 2, def: 2 },
        speed: { min: 0.1, max: 2.5, def: 1 },
        seed: { min: 0, max: 8, def: 0 },
        nMul: { min: 0.62, max: 1.65, def: 1 },
        press: { min: 1, max: PRESS, def: 1 },
        bal: { min: -1, max: 1, def: 1, open: true },
      },
      neutrals: { a: 0, b: 1 },
      doors: { in: { handle: "mix", value: 0, work: "a" },
               out: { handle: "mix", value: 1, work: "b" } },
      // Both doors frame alike, so one record covers them: the constant centre crop the strips'
      // travel pays for (ZOOM above; module-contract.json publishes the same 1.29).
      framings: { "0": { coverCrop: ZOOM }, "1": { coverCrop: ZOOM } },
      drivers: ["progress", "cueProgress", "time", "velocity", "capability", "noise", "static",
                "curve", "spline", "map", "add", "multiply", "mix", "clamp", "hold", "segment",
                "ramp", "slew", "oscillate", "node"],
      camera: { needs: "none", authority: "stage" },
      gl: { preserveDrawingBuffer: false },
      neutralPose: { bal: 1, nMul: 1, press: 1, strips: 28, axis: 2, cssWidth: 1000, t: 0, reduced: false },
      passes: [{
        program: "weave", vert: VERT, frag: FRAG, position: "aPos",
        uniforms: [
          { name: "uA", type: "sampler2D", source: "textureA" },
          { name: "uB", type: "sampler2D", source: "textureB" },
          { name: "uFitA", type: "vec4", source: "fitA" },
          { name: "uFitB", type: "vec4", source: "fitB" },
          { name: "uRes", type: "vec2", source: "resolution" },
          { name: "uT", type: "float", source: "seconds" },
          { name: "uNv", type: "float", source: "frame:nV" },
          { name: "uDuty", type: "float", source: "frame:duty" },
          { name: "uAmp", type: "float", source: "frame:amp" },
          { name: "uRot", type: "float", source: "frame:rot" },
          { name: "uSpeed", type: "float", source: "handle:speed" },
          { name: "uSeed", type: "float", source: "handle:seed" },
        ],
      }],
      // The instrument allocates NOTHING of its own: it spends the two source-texture slots the host
      // already holds and the one programme the host builds from this manifest.
      resources: { lean: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                           passes: 1, bytesEstimate: 0, variant: "lean" },
                   standard: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                               passes: 1, bytesEstimate: 0, variant: "standard" },
                   rich: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                           passes: 1, bytesEstimate: 0, variant: "rich" } },
      capabilities: ["webgl2"],
      decline: ["one work only", "a source that never decoded"],
      provenance: { labPath: "lab/effects/weave.js", commit: "547a100" },
      readiness: "production-ready",
    };

    var live = false;
    return {
      name: "weave",
      manifest: manifest,
      values: values,
      fit: fit,
      feel: feelOf,
      prepare: function (o) {
        if (!o.sources) return { take: false, why: "the woven instrument needs both works" };
        if (!o.cue) return { take: false, why: "no cue names it" };
        return { take: true };
      },
      start: function () { live = true; },
      // The pose the shader draws. Every number in it now comes from a handle a score can drive, so
      // a seeded run repeats to the pixel with every voice scored. `bal` is the one open handle: a
      // score that drives it directly carries the module's own drift, and a score that says nothing
      // about it leaves the balance derived from the dial through the response curve, which is how
      // the module itself resolves the same pair.
      //
      // The remaining voices ride these handles rather than constants: the two width breaths at
      // their own unaligned rates (0.31 and 0.24 + 1.7 rad) and the 27 s turn with its unequal holds
      // of 3.2 s and 4.9 s read `clock`; the strips' travel reads `clock` and `speed` together
      // (speed × 0.17, the horizontal at 0.86 of it + 0.31 turn); the over/under order reads `seed`.
      // Their rates stay inside the shader and inside rotForTime, where their author put them.
      frame: function (st) {
        if (!live) return;
        var h = st.handles;
        var bal = typeof h.bal === "number" ? h.bal : 1 - 2 * feelOf(clamp(h.mix, 0, 1));
        st.draw({
          bal: bal,
          nMul: h.nMul, press: h.press,
          strips: h.strips, axis: h.axis, speed: h.speed, seed: h.seed,
          cssWidth: st.viewport.w, t: h.clock, reduced: st.reduced,
        });
        if (st.progress >= 1 && !st.pinned) st.settle(st.token);
      },
      resize: function () {},
      cancel: function () {},
      dispose: function () { live = false; },
      contextLost: function () { live = false; },
      contextRestored: function () {},
    };
  }

  register(weaveInstrument());

  // ================================================================================================
  // THE MATTER INSTRUMENT (§8) — lab/effects/matter.js carried across
  // ================================================================================================
  // What the visitor sees: the departing work loosens into a material — grain dragged along a seeded
  // field — and the arriving work condenses out of that same material. A band of loosened matter
  // travels across the frame with one work whole ahead of it and the other whole behind. It stands
  // beside the woven instrument because it carries disassembly and assembly, which the woven one
  // does not.
  //
  // What came over: the shader, the seating of a work in the frame (fit), the response curve (feel),
  // the field constants and the numbers of one frame (values). Not one number changed.
  //
  // What stayed behind: its own canvas, its own WebGL 1 context, its own frame loop, its resize
  // listener and its own accumulated clock. The instrument here reads no wall clock, holds no
  // listener, creates no context and loads no picture (§1.2's fence).
  //
  // THREE THINGS THE PORT HAD TO ANSWER, named in the module's own card
  // (docs/immersive/effects/matter.md §11):
  //   · THE UNIFORM SET. The lab carrier's draw call names one instrument's six uniforms literally,
  //     and nine of this module's fourteen have no place in that list. The host binds by the name
  //     each uniform declares in the manifest below, so the set is the instrument's own.
  //   · THE PRESERVED DRAWING BUFFER. The module asks its own context for one (matter.js:250), and
  //     §7 refuses a manifest that asks for it. What the flag stood in for is a redraw: the module
  //     draws on demand — from onParam, from resize — and between two such draws the browser has to
  //     hand back the frame that was already there. The host draws every frame of a running
  //     transaction and redraws on every resize, so the frame the compositor shows is one this
  //     instrument drew for it. The row «no empty frame at any sampled instant» measures that,
  //     across a resize as well as across the pass.
  //   · THE VERSION HEADER. This module's shader carries none, so the host's translator stamps the
  //     one it needs and no second one arrives.
  //
  // ASPECT. The module reads the frame's aspect from a uniform of its own that the host does not
  // supply. It is the ratio of the two numbers the host already binds as `resolution`, so it is
  // computed from those inside the shader and every use of it reads the same number as before.
  function matterInstrument() {
  // THE MESHING INSTRUMENT (§8) — lab/effects/gears.js carried across
  // ================================================================================================
  // TWO WHEELS, MESHING. Their centres stand off the frame on either side, so what the eye sees is
  // the line where the two rims meet — a row of interlocking teeth running down the picture — and the
  // crossing is that line rolling across the frame, one work riding each wheel.
  //
  // What came over: the shader, the seating of a work in the frame (coverFit), the response curve
  // (the measured inverse FEEL_Q), the ladder of small whole ratios, and the numbers of one frame
  // (values). What stayed behind: its own canvas, its own WebGL 1 context, its own frame loop, its
  // resize listener and its own clock. The instrument here reads no wall clock, holds no listener,
  // creates no context and loads no picture (§1.2's fence).
  //
  // THE FOUR THINGS THE MODULE'S CARD ASKED A PORT TO PROVE (docs/immersive/effects/gears.md §11),
  // and where each stands here.
  //   1. The uniform set is bound BY DECLARED NAME from the manifest below — nineteen names, of
  //      which only six are shared with the woven instrument. The host reads the manifest; no list
  //      of names is written into the host.
  //   2. `preserveDrawingBuffer` is off. The lab module asked for it at gears.js:276 and drew only
  //      on a parameter change, on a resize and on its own frame loop, so the preserved buffer was
  //      standing in for the frames it did not draw. THE REDRAW IT STOOD IN FOR IS CARRIED: this
  //      instrument draws on EVERY frame the host hands it, including a reduced-motion run, where
  //      the module rendered once and stopped. Reduced motion stops the wheels' drive and never the
  //      drawing.
  //   3. The `ratio` handle steps through the module's own ladder of small whole pairs and is never
  //      interpolated. A tooth count is a whole number by the time it reaches the shader, so a tooth
  //      of one wheel always meets a gap of the other and the mesh closes on itself.
  //   4. The shader carries no version header of its own, so the host's translator stamps exactly
  //      one. A row counts them.
  //
  // ONE LINE OF THE SHADER IS NOT THE MODULE'S. The lab module hands the frame's aspect in as its
  // own uniform, computed from the drawing buffer it owns. The host owns the buffer here and already
  // binds its size as `uRes`, so the aspect is derived from `uRes` inside the shader. The mathematics
  // then reads the buffer the host actually drew into, whatever the resolution ladder has done to it.
  // Every other line of the shader is the module's own, character for character.
  function gearsInstrument() {
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
      "uniform float uGrainA;",      // the coarse grain of the material, cells per frame height
      "uniform float uGrainB;",      // and the fine grain over it
      "uniform vec2 uDrift;",        // where the material has drifted to, in cells
      "uniform float uLadder;",      // how much of the field is the plain ladder across the frame
      "uniform float uTau;",
      "uniform float uLoosen;",      // how far the picture is dragged, frame heights
      "uniform float uGather;",      // how wide the loosened band is, in field units
      "uniform float uSeed;",
      "uniform float uGuard;",
      "float h11(vec2 i){ return fract(sin(dot(i, vec2(41.317, 289.107)) + uSeed) * 43758.5453); }",
      // value noise with its own exact gradient: the material's grain, and the direction it drags
      "vec3 vnoise(vec2 p){",
      "  vec2 i = floor(p), f = fract(p);",
      "  float a = h11(i), b = h11(i + vec2(1.0, 0.0));",
      "  float c = h11(i + vec2(0.0, 1.0)), d = h11(i + vec2(1.0, 1.0));",
      "  vec2 u = f * f * (3.0 - 2.0 * f);",
      "  vec2 du = 6.0 * f * (1.0 - f);",
      "  float k = a - b - c + d;",
      "  float v = a + (b - a) * u.x + (c - a) * u.y + k * u.x * u.y;",
      "  float vx = ((b - a) + k * u.y) * du.x;",
      "  float vy = ((c - a) + k * u.x) * du.y;",
      "  return vec3(v, vx, vy);",
      "}",
      "vec2 into(vec2 p, vec4 f){",
      "  return clamp((p - 0.5) * f.xy + 0.5 + f.zw, 0.0008, 0.9992);",
      "}",
      "void main(){",
      "  vec2 uv = vUv;",
      "  float aspect = uRes.x / max(uRes.y, 1.0);",
      "  vec2 p = vec2(uv.x * aspect, uv.y);",
      "  float h = 1.0 / max(uRes.y, 1.0);",
      // THE FIELD: two grains of matter over a plain ladder across the frame. The ladder gives the
      // crossing its direction, the grain gives it its material.
      "  vec3 n1 = vnoise(p * uGrainA + uDrift);",
      "  vec3 n2 = vnoise(p * uGrainB - uDrift * 1.7);",
      "  float ladder = uv.x;",
      "  float F = uLadder * ladder + (1.0 - uLadder) * (0.62 * n1.x + 0.38 * n2.x);",
      "  vec2 gF = vec2(uLadder / max(aspect, 0.05), 0.0)",
      "          + (1.0 - uLadder) * (0.62 * n1.yz * uGrainA + 0.38 * n2.yz * uGrainB);",
      "  float grad = max(length(gF), 1e-5);",
      "  float d = (F - uTau) / (grad * h);",
      "  float cov = clamp(0.5 + d, 0.0, 1.0);",
      // THE LOOSENING. Strongest at the front — where the field stands nearest the threshold — and
      // gone on both sides of it, so a band of loose matter travels and the rest of the frame is the
      // picture standing still. The drag runs along the field's own gradient, and across it the two
      // works are dragged against each other.
      "  float near = exp(-((F - uTau) * (F - uTau)) / max(uGather * uGather, 1e-6));",
      "  vec2 flow = gF / grad;",
      "  vec2 across = vec2(-flow.y, flow.x);",
      "  vec2 pull = (flow * (0.6 + 0.4 * n1.x) + across * 0.8) * uLoosen * near;",
      "  vec2 pullA = vec2(pull.x / max(aspect, 0.05), pull.y);",
      "  vec2 pullB = vec2((flow.x * (0.6 + 0.4 * n2.x) - across.x * 0.8) / max(aspect, 0.05),",
      "                    flow.y * (0.6 + 0.4 * n2.x) - across.y * 0.8) * uLoosen * near;",
      "  vec3 colA = texture2D(uA, into(uv + pullA, uFitA)).rgb;",
      "  vec3 colB = texture2D(uB, into(uv + pullB, uFitB)).rgb;",
      "  vec3 col = mix(colB, colA, cov);",
      "  col *= 1.0 - 0.32 * uGuard * cov * exp(-max(d, 0.0) / 7.0);",
      "uniform vec2 uCA;",            // the first wheel's centre, frame half-heights
      "uniform vec2 uCB;",            // the second wheel's
      "uniform float uR1;",           // their pitch radii
      "uniform float uR2;",
      "uniform float uN1;",           // and their tooth counts, which stand in the same ratio
      "uniform float uN2;",
      "uniform float uAmp;",          // how far a tooth stands out of the pitch circle
      "uniform float uPh;",           // where the teeth stand along the rims: the wheels' own turn
      "uniform float uFlank;",        // how upright a tooth's flank is
      "uniform float uSpread;",       // how far apart the teeth's own moments are set
      "uniform float uSeed;",
      "uniform float uOff;",          // counter-motion, tangential, frame heights
      "uniform float uGuard;",
      "const float PI = 3.14159265359;",
      "const float TAU = 6.28318530718;",

      "float hash11(float n){ return fract(sin(n * 127.1) * 43758.5453); }",

      // A TOOTH, not a wave. A cosine gives a boundary that curves the whole way and reads as a
      // blob; a tooth stands out to its full height, holds there across its own top, and drops on
      // a flank. uFlank is how much of a tooth is flank — the clamp does the holding.
      "float tooth(float x){ return clamp(sin(x) / uFlank, -1.0, 1.0); }",
      "float toothD(float x){ return abs(sin(x)) < uFlank ? cos(x) / uFlank : 0.0; }",

      "vec2 into(vec2 p, vec4 f){",
      "  return clamp((p - 0.5) * f.xy + 0.5 + f.zw, 0.0008, 0.9992);",
      "}",

      "void main(){",
      "  vec2 uv = vUv;",
      // the aspect of the buffer the host drew into, read from the size the host binds
      "  float uAspect = uRes.x / max(uRes.y, 1.0);",
      // the frame in half-heights: x across, y up
      "  vec2 p = vec2((uv.x - 0.5) * 2.0 * uAspect, (0.5 - uv.y) * 2.0);",
      "  float h = 2.0 / max(uRes.y, 1.0);",

      // EACH WHEEL, AS A RIM. The point stands somewhere out from each centre; the rim it is being
      // held against is the pitch circle with the teeth standing on it, and how far INSIDE that rim
      // the point lies is what decides whose the point is.
      "  vec2 dA = p - uCA;   float rA = max(length(dA), 1e-5);",
      "  vec2 dB = p - uCB;   float rB = max(length(dB), 1e-5);",
      "  vec2 uAv = dA / rA;  vec2 nA = vec2(-uAv.y, uAv.x);",
      "  vec2 uBv = dB / rB;",
      // the angle round each wheel, both counted from the ray that runs to the point where the two
      // rims meet — so ONE arc length, one pitch, and the two sets of teeth cannot drift apart
      "  float thA = atan(dA.y, dA.x);",
      "  float thB = atan(dB.y, -dB.x);",
      "  float wA = uN1 * thA + uPh;",
      "  float wB = uN2 * thB + uPh;",
      // the second wheel's teeth are the first's turned inside out: where one stands, the other is
      // a gap, which is what meshing is
      "  float RA = uR1 + uAmp * tooth(wA);",
      "  float RB = uR2 - uAmp * tooth(wB);",

      // WHICH WEDGE OF WHICH WHEEL, and when that tooth hands over: six parts a ladder down the
      // line where the two rims meet, four parts the score's die.
      "  float ti = floor(wA / TAU);",
      "  float ladder = clamp(0.5 + 0.5 * p.y, 0.0, 1.0);",
      "  float ord = mix(ladder, hash11(ti + uSeed), 0.4);",

      "  float M = (RA - rA) - (RB - rB) + uSpread * (ord - 0.5);",
      // the field's own gradient, exactly: the rims' own turning plus the two radial directions
      "  vec2 gB = vec2(dB.y, -dB.x) / (rB * rB);",
      "  vec2 gM = uAmp * toothD(wA) * uN1 * nA / rA",
      "          + uAmp * toothD(wB) * uN2 * gB",
      "          - uAv + uBv;",
      "  float grad = max(length(gM), 1e-5);",
      "  float d = M / (grad * h);",
      "  float cov = clamp(0.5 + d, 0.0, 1.0);",

      // the two works sweep along their own rims, against each other at the mesh — the flanks of
      // two meshing teeth slide past one another, and this is that slide
      "  vec2 tA = vec2(nA.x / max(uAspect, 0.05), -nA.y);",
      "  vec2 tB = vec2(-uBv.y / max(uAspect, 0.05), uBv.x);",
      "  vec3 colA = texture2D(uA, into(uv + tA * uOff, uFitA)).rgb;",
      "  vec3 colB = texture2D(uB, into(uv - tB * uOff * (uN1 / max(uN2, 1.0)), uFitB)).rgb;",
      "  vec3 col = mix(colB, colA, cov);",

      "  col *= 1.0 - 0.32 * uGuard * (1.0 - cov) * exp(-max(-d, 0.0) / 7.0);",
      "  gl_FragColor = vec4(col, 1.0);",
      "}",
    ].join("\n");

    function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
    function smoothstep(a, b, x) {
      var t = (x - a) / (b - a);
      t = t < 0 ? 0 : t > 1 ? 1 : t;
      return t * t * (3 - 2 * t);
    }
    function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }

    // HOW COARSE THE MATERIAL IS, in cells across the frame's height, at either end of the `grain`
    // handle (matter.js:191). The fine grain rides at three times the coarse one, which is what
    // gives the front its crumb.
    var GRAIN_MIN = 4, GRAIN_MAX = 34, GRAIN_FINE = 3.0;
    // How far the picture is dragged at the fullest loosening, in frame heights, and the crop that
    // pays for it (matter.js:195-196). ZOOM is derived from AMP and is no free number.
    var AMP = 0.07, ZOOM = 1 + 2 * AMP + 0.03;
    // Six parts plain ladder against four parts grain (matter.js:205). At four parts ladder the
    // field has no direction, the loosened band is the whole frame, and the picture reads as marble.
    var LADDER = 0.6;

    // cover-fit a work into the frame, then pull in by the drag's own headroom. The host hands the

    // THE SMALL WHOLE RATIOS the handle walks. A gear pair is only a gear pair when the two counts
    // stand in a ratio of small whole numbers — that is what makes the mesh close on itself — so the
    // handle does not slide through the reals: it steps through this ladder. The `ratio` handle is a
    // place on the ladder and is rounded to a rung before any count is taken from it.
    var RATIOS = [[1, 1], [3, 4], [2, 3], [1, 2], [2, 5], [1, 3], [1, 4]];

    // THE TANGENTIAL SWEEP, in frame heights, and the crop that pays for it. The sweep is bounded
    // and the wheels' own turning is unbounded — the teeth go round for as long as the clock runs,
    // while the pictures only lean into the sweep — so the crop stays small.
    var AMP = 0.05;
    var ZOOM = 1 + 2 * AMP + 0.03;

    // How tall a tooth stands against its own pitch. A real gear tooth stands about a third of its
    // pitch out of the pitch circle on each side; below about a tenth the mesh reads as a wavy line
    // and above about a half the teeth are longer than they are wide and read as a comb.
    var TOOTH_MIN = 0.12, TOOTH_MAX = 0.40;

    // THE MEASURED RESPONSE CURVE, carried over digit for digit (gears.js:329-337). How far the
    // picture moves per unit of the raw travel was measured with the curve taken out of the module,
    // that rate integrated, and this is the inverse of the integral at twenty-one evenly spaced
    // shares, with straight lines between them. Half the whole change stands at 0.28 of the travel,
    // which is why no two-piece logarithm fits it.
    var FEEL_D0 = 0.05;
    var FEEL_Q = [0, 0.0272, 0.0544, 0.0815, 0.1084, 0.1348, 0.1608, 0.1869, 0.214, 0.244,
                  0.2807, 0.3286, 0.3865, 0.4545, 0.545, 0.6185, 0.6926, 0.7607, 0.8211,
                  0.8897, 1];
    function feelOf(u) {
      var x = clamp((u - FEEL_D0) / (1 - 2 * FEEL_D0), 0, 1);
      var s = x * (FEEL_Q.length - 1), i = Math.min(FEEL_Q.length - 2, Math.floor(s));
      return FEEL_Q[i] + (FEEL_Q[i + 1] - FEEL_Q[i]) * (s - i);
    }

    // cover-fit a work into the frame, then pull in by the travel headroom. The host hands the
    // source's own dimensions, so the instrument never touches an image object.
    function fit(iw, ih, w, h) {
      var fa = w / Math.max(h, 1);
      var ia = iw / Math.max(ih, 1);
      var sx, sy;
      if (ia > fa) { sx = fa / ia; sy = 1; } else { sx = 1; sy = ia / fa; }
      return [sx / ZOOM, sy / ZOOM, 0, 0];
    }

    // THE RESPONSE CURVE, MEASURED (matter.js:267-307, the module's re-fit of 2026-08-13): equal
    // movements of the hand, equal felt change. The rate of change of the picture per unit of the
    // raw threshold was measured with the curve taken out, that rate integrated, and this is the
    // inverse of the integral at twenty-one evenly spaced shares with straight lines between them.
    // The two-piece logarithm the module carried before it cannot hold this handle: the field's own
    // values crowd the middle and thin to nothing at both ends, so the curve stands nearly vertical
    // at both ends and nearly flat across the middle. Carried here digit for digit; the port
    // re-derives nothing.
    var FEEL_D0 = 0.05;
    var FEEL_Q = [0, 0.1994, 0.2488, 0.2852, 0.3168, 0.3454, 0.372, 0.3972, 0.4215, 0.4454,
                  0.469, 0.4925, 0.5162, 0.5405, 0.5657, 0.5923, 0.621, 0.653, 0.6902,
                  0.7388, 1];
    function feelOf(u) {
      var x = clamp((u - FEEL_D0) / (1 - 2 * FEEL_D0), 0, 1);
      var s = x * (FEEL_Q.length - 1), i = Math.min(FEEL_Q.length - 2, Math.floor(s));
      return FEEL_Q[i] + (FEEL_Q[i + 1] - FEEL_Q[i]) * (s - i);
    }

    // The numbers of one frame: everything the shader gets beyond the seating of the two works is a
    // pure function of the pose (matter.js:309-329). The threshold travels a tenth past either end
    // of the field and no further — past the field's own range every point stands on one side and
    // the work is whole, which is what makes both doors exact.
    function values(st) {
      var d = feelOf(clamp(st.mix, 0, 1));
      var grainA = GRAIN_MIN + (GRAIN_MAX - GRAIN_MIN) * clamp(st.grain, 0, 1);
      var reach = 0.5 + 0.10;
      var drift = (st.reduced ? 0 : st.t) * 0.11 * clamp(st.drift, 0, 1);
      return {
        dial: d, grainA: grainA, grainB: grainA * GRAIN_FINE, ladder: LADDER,
        gather: 0.04 + 0.26 * clamp(st.gather, 0, 1),
        tau: 0.5 - reach + 2 * reach * d,
        drift: [drift, drift * 0.6],
        loosen: st.travel * AMP * clamp(st.loosen, 0, 1) * 4 * d * (1 - d),
        guard: st.shade * smoothstep(0, 0.09, d) * smoothstep(1, 0.91, d),
    function ratioAt(v) { return RATIOS[Math.round(clamp(v, 0, 1) * (RATIOS.length - 1))]; }

    // ---- WHERE THE RIMS MEET AT A DOOR, SOLVED RATHER THAN APPROXIMATED ---------------------------
    // At a door one whole work stands, which asks that the mask cover the whole frame: at door 0
    // every point of the frame lies inside the first wheel's rim, at door 1 every point lies inside
    // the second's. The module holds that by standing the meeting line beyond the frame's own edge
    // by `2·amp + spread/4 + 0.08`, which is the right margin for ONE wheel size — the module's own
    // R_BASE of 4.5, where the two rims are nearly straight across the frame and the field grows as
    // twice the distance from the meeting line.
    //
    // The port lets the wheel size travel, because that is what carries the pair's own reading from
    // angular to ring. At a small size the rims are no longer straight: the field is a function of
    // the ANGLE about the pair, it reaches its full depth only far from the pair, and the module's
    // margin leaves teeth of the far work standing in the frame's corners. So the condition itself
    // is solved instead of approximated.
    //
    // The condition, written out. Away from the teeth the mask's field is
    //     G(p) = R1 − R2 + |p − cB| − |p − cA|,
    // and the teeth and the spread move it by at most `2·amp + spread/2`. G is monotone over the
    // frame, so its extremes stand at the frame's four corners. Door 0 asks that the smallest G over
    // those corners stand above that much, door 1 that the largest stand below it. G improves as the
    // pair is carried further out, so a bisection on the reach finds the smallest reach that answers
    // both doors. The walk is a fixed count of steps and reads no clock, so a seeded run repeats.
    var DOOR_SLACK = 0.02;   // half-heights; the mask crosses over within about half a point of the
                             // boundary, and this stands well clear of that on any frame the host runs
    function gAt(px, py, cA, cB, R1, R2) {
      var ax = px - cA[0], ay = py - cA[1], bx = px - cB[0], by = py - cB[1];
      return R1 - R2 + Math.sqrt(bx * bx + by * by) - Math.sqrt(ax * ax + ay * ay);
    }
    // The smallest and largest G over the frame's four corners, with the pair standing at `xc`.
    function gEdge(xc, ox, oy, R1, R2, aspect) {
      var cA = [xc - R1 + ox, oy], cB = [xc + R2 + ox, oy];
      var lo = Infinity, hi = -Infinity, i, j, g;
      for (i = -1; i <= 1; i += 2) {
        for (j = -1; j <= 1; j += 2) {
          g = gAt(i * aspect, j, cA, cB, R1, R2);
          if (g < lo) lo = g;
          if (g > hi) hi = g;
        }
      }
      return { lo: lo, hi: hi };
    }
    function doorsHold(reach, ox, oy, R1, R2, aspect, need) {
      return gEdge(reach, ox, oy, R1, R2, aspect).lo > need
          && gEdge(-reach, ox, oy, R1, R2, aspect).hi < -need;
    }
    function reachFor(aspect, ox, oy, R1, R2, amp, spread) {
      var need = 2 * amp + 0.5 * spread + DOOR_SLACK;
      // the module's own margin first, widened by however far the centre has been carried across
      var base = aspect + 2 * amp + spread * 0.25 + 0.08 + Math.abs(ox);
      if (doorsHold(base, ox, oy, R1, R2, aspect, need)) return base;
      var lo = base, hi = base, i;
      for (i = 0; i < 48 && !doorsHold(hi, ox, oy, R1, R2, aspect, need); i++) {
        lo = hi;
        hi = hi * 2 + 1;
      }
      for (i = 0; i < 48; i++) {
        var mid = 0.5 * (lo + hi);
        if (doorsHold(mid, ox, oy, R1, R2, aspect, need)) hi = mid; else lo = mid;
      }
      return hi;
    }

    // THE NUMBERS OF ONE FRAME. Everything the shader gets beyond the seating of the two works is a
    // pure function of the pose. This is the module's own `values()` with three of its constants
    // published as handles: the pair's own size (the module's R_BASE), the tooth pitch (the module's
    // `teeth`, said as the band period it makes) and the pair's centre (the module pins it to the
    // middle of the frame's height).
    function values(st) {
      var aspect = Math.max(st.cssWidth, 1) / Math.max(st.cssHeight, 1);
      var d = clamp(st.dial, 0, 1);
      var rr = ratioAt(st.ratio);

      // THE PAIR. The two works' repeat counts stand as the ratio of the two WHEELS — equal tooth
      // pitch, counts and radii in one and the same small whole ratio, so the mesh closes on itself
      // and a tooth of one always meets a gap of the other. The pitch is the band period the score
      // holds, said in frame half-heights; the counts follow from it and from the pair's size,
      // rounded to whole teeth so the closing is exact.
      var pitch = clamp(2 * st.bandPeriod, 0.04, 2.0);
      var size = clamp(st.size, 0.3, 8);
      // BOTH COUNTS COME FROM ONE WHOLE MULTIPLIER, which is what holds them in the rung's own
      // ratio. The module takes the first count from the geometry and the second by rounding
      // `n1 · r2/r1`, and at the rungs whose first number is above one that rounding lands off the
      // ratio: 3:4 comes out as 14:19 and 2:3 as 13:20, and a mesh in 19:14 does not close on
      // itself — a tooth stops meeting a gap after one turn. Counting in whole rungs holds the ratio
      // exactly and returns the module's own 57:114 at the module's own handles, so nothing about
      // its default frame moves.
      var span = rr[0] + rr[1];
      var k = Math.max(1, Math.round(TAU * size * 2 / (span * pitch)));
      while (rr[0] * k < 3 || rr[1] * k < 3) k++;
      var n1 = rr[0] * k, n2 = rr[1] * k;
      var R1 = n1 * pitch / TAU, R2 = n2 * pitch / TAU;
      var amp = pitch * (TOOTH_MIN + (TOOTH_MAX - TOOTH_MIN) * clamp(st.tooth, 0, 1));

      // How far apart the teeth's own moments stand, in the mask's own units. The mask reads about
      // twice the distance from the line where the rims meet, so a spread of one moves a tooth's own
      // moment by a quarter of a frame height — one tooth handing over while its neighbour has not.
      var spread = clamp(st.order, 0, 1) * 1.2;

      // A TOOTH STANDS NO TALLER THAN THE WHEEL IT STANDS ON. Away from the teeth the mask's field
      // runs from −2·R2 to +2·R1, so a door can only be a whole work while the teeth and the spread
      // together stay inside that depth. At the module's own size the depth is nine half-heights and
      // nothing comes near it; at a small pair with a far-apart ratio the two together can ask for
      // more than the field holds, and then no placement of the pair makes either door whole. Both
      // are scaled back together, which keeps their proportion and keeps both doors exact.
      var room = 2 * Math.min(R1, R2) * 0.85 - DOOR_SLACK;
      var want = 2 * amp + 0.5 * spread;
      if (want > room) {
        var back = room > 0 ? room / want : 0;
        amp *= back;
        spread *= back;
      }

      // WHERE THE PAIR STANDS ACROSS THE FRAME. The centre travels in the frame's own coordinates,
      // the same ones the radial measure reads: x across from the left edge, y down from the top.
      var ox = (clamp(st.centreX, 0, 1) - 0.5) * 2 * aspect;
      var oy = (0.5 - clamp(st.centreY, 0, 1)) * 2;

      var reach = reachFor(aspect, ox, oy, R1, R2, amp, spread);
      var xc = reach - 2 * reach * d;

      // THE WHEELS TURN, and they turn from two things at once. THE TRAVEL rolls them: the pair moves
      // across the frame and the rims roll on each other without slipping, one tooth of turn for
      // every tooth of travel, which is why the teeth never come unmeshed. THE CLOCK drives them on
      // top of that, windowed to nothing at both doors, so the first work stands still, the drive
      // spins up, and the second is brought to standing exactly as it lands.
      var win = Math.sin(Math.PI * d);
      var rate = 2.6 * clamp(st.turn, 0, 1) * win;
      var ph = (reach - xc) * (TAU / pitch) + (st.reduced ? 0 : st.t) * rate;

      return {
        n1: n1, n2: n2, R1: R1, R2: R2, amp: amp, ph: ph, spread: spread,
        flank: clamp(st.flank, 0.05, 1),
        cA: [xc - R1 + ox, oy], cB: [xc + R2 + ox, oy],
        off: clamp(st.travel, 0, 1) * AMP * 4 * d * (1 - d),
        guard: clamp(st.shade, 0, 1) * smoothstep(0, 0.09, d) * smoothstep(1, 0.91, d),
        // read on the diagnostic surface, bound to no uniform: what the handles came to
        pitch: pitch, reach: reach, xc: xc, rate: rate, dial: d, size: size,
        ratioN: rr[0] * 1000 + rr[1],
      };
    }

    var manifest = {
      id: "matter", api: 1, arity: 2,
      // The module's own header ties it to the release envelope's disassembly–mystery–reassembly
      // class: the first work comes apart into the material and the second gathers out of it.
      roles: ["disassembly", "mystery", "assembly"],
      // READ OFF THE MODULE'S OWN CONSTRUCTION. The vocabulary table publishes no level for this
      // module (lab/CROSSING-BRIEF.md carries no `matter` row), so these two are derived and said to
      // be derived: one field runs over the whole frame at SURFACE, and its grain is the TEXTURE.
      levels: ["SURFACE", "TEXTURE"],
      params: { loosen: [0, 1], drift: [0, 1], gather: [0, 1], grain: [0, 1] },
      // EVERY handle a score can drive (§4.4b). `mix` is the dial and `clock` is the second the host
      // hands down; the four below them are the module's declared params; `seed` is its die; and
      // `shade` and `travel` are the two judge channels the module keeps for measuring a law on the
      // picture — the frame with the contact shadow against the frame without it, and the same for
      // the drag. They rest at 1, which is what the module does with them.
      //
      // NO HANDLE HERE KEEPS A CLOCK OF ITS OWN. The one place the module reads time is the drift of
      // the field, `t * 0.11 * drift` (matter.js:321), where `t` was its own accumulated frame time.
      // It reads the `clock` handle instead, so a seeded score repeats to the pixel.
      handles: {
        mix: { min: 0, max: 1, def: 0 },
        clock: { min: 0, max: 14, def: 0 },
        loosen: { min: 0, max: 1, def: 0.6 },
        drift: { min: 0, max: 1, def: 0.45 },
        gather: { min: 0, max: 1, def: 0.3 },
        grain: { min: 0, max: 1, def: 0.45 },
      id: "gears", api: 1, arity: 2,
      roles: ["disassembly", "mystery", "assembly"],
      levels: ["SURFACE", "CELL"],
      params: { bandPeriod: [0.02, 1], ratio: [0, 1], size: [0.3, 8] },
      // EVERY handle a score can drive (§4.4b). The module ran its wheels on its own accumulating
      // clock and held its judges, its die and its flank as constants; all of them are published
      // here, so no handle keeps a clock or a roll of its own and a seeded run repeats to the pixel.
      //
      // THE THREE THE PORT PUBLISHES THAT THE MODULE HELD AS CONSTANTS, and why each is a handle:
      //   · `size` — THE PAIR'S OWN SIZE in frame half-heights, the module's R_BASE of 4.5. The
      //     module's own note names both ends of it: "Below about three the rims curve hard enough
      //     inside the frame to read as two circles overlapping; above about eight they are straight
      //     and the pair stops reading as wheels at all" (gears.js:211-215). That is the axis the
      //     measured pair travels along, so it is published rather than pinned.
      //   · `bandPeriod` — THE TOOTH PITCH, said as the period of the tooth line as a fraction of the
      //     frame's height. The module carried the same number as a whole count of teeth across the
      //     height, stepped 3 to 12; said as a period it is the unit the pair's own measurement uses,
      //     and the count no longer has to be whole, which is what puts the pair's measured period
      //     inside reach.
      //   · `centreX`/`centreY` — WHERE THE PAIR STANDS, in the frame's own coordinates. The module
      //     pins the pair to the middle of the frame's height and carries it across the frame on the
      //     dial alone. The field is built from the distance to each centre, so carrying both centres
      //     together moves the whole construction and changes no mathematics.
      //
      // `dial` is OPEN: a score that names no track for it leaves the instrument deriving the
      // travelled number from `mix` through the measured response curve, exactly as the module does.
      // Nothing falls back, so nothing is recorded as a fallback.
      handles: {
        mix: { min: 0, max: 1, def: 0 },
        clock: { min: 0, max: 14, def: 0 },
        dial: { min: 0, max: 1, def: 0, open: true },
        size: { min: 0.3, max: 8, def: 4.5 },
        centreX: { min: 0, max: 1, def: 0.5 },
        centreY: { min: 0, max: 1, def: 0.5 },
        bandPeriod: { min: 0.02, max: 1, def: 1 / 6 },
        ratio: { min: 0, max: 1, def: 0.5 },
        tooth: { min: 0, max: 1, def: 0.4 },
        order: { min: 0, max: 1, def: 0.4 },
        turn: { min: 0, max: 1, def: 0.55 },
        flank: { min: 0.05, max: 1, def: 0.35 },
        seed: { min: 0, max: 8, def: 0 },
        shade: { min: 0, max: 1, def: 1 },
        travel: { min: 0, max: 1, def: 1 },
      },
      // The dial's two ends. At 0 the threshold stands a tenth below the field's whole range, so
      // every point covers on A; at 1 it stands a tenth above it and every point covers on B. The
      // drag and the contact shadow are both nothing there, so each door is one work and nothing
      // else. Neither is published in module-contract.json, which carries no `matter` entry — both
      // are read off the module's own geometry and the conformance rows measure them.
      neutrals: { a: 0, b: 1 },
      doors: { in: { handle: "mix", value: 0, work: "a" },
               out: { handle: "mix", value: 1, work: "b" } },
      // Both doors frame alike: the crop the drag's headroom is paid for with is a constant, while
      // the drag itself dies at both ends.
      neutrals: { a: 0, b: 1 },
      doors: { in: { handle: "mix", value: 0, work: "a" },
               out: { handle: "mix", value: 1, work: "b" } },
      // Both doors frame alike, so one record covers them: the constant centre crop the tangential
      // sweep is paid for with (ZOOM above, 1.13).
      framings: { "0": { coverCrop: ZOOM }, "1": { coverCrop: ZOOM } },
      drivers: ["progress", "cueProgress", "time", "velocity", "capability", "noise", "static",
                "curve", "spline", "map", "add", "multiply", "mix", "clamp", "hold", "segment",
                "ramp", "slew", "oscillate", "node"],
      camera: { needs: "none", authority: "stage" },
      gl: { preserveDrawingBuffer: false },
      neutralPose: { mix: 0, loosen: 0.6, drift: 0.45, gather: 0.3, grain: 0.45,
                     seed: 0, shade: 1, travel: 1, t: 0, reduced: false },
      passes: [{
        program: "matter", vert: VERT, frag: FRAG, position: "aPos",
      // The construction moves no point of view: it decides which wheel owns each point of the frame
      // and slides the two works along their own rims inside it. Both are what it does to its own
      // surface, so the witness camera stays the stage's (§6).
      camera: { needs: "none", authority: "stage" },
      gl: { preserveDrawingBuffer: false },
      neutralPose: { dial: 0, size: 4.5, centreX: 0.5, centreY: 0.5, bandPeriod: 1 / 6, ratio: 0.5,
                     tooth: 0.4, order: 0.4, turn: 0.55, flank: 0.35, shade: 1, travel: 1,
                     cssWidth: 1000, cssHeight: 1000, t: 0, reduced: false },
      passes: [{
        program: "gears", vert: VERT, frag: FRAG, position: "aPos",
        uniforms: [
          { name: "uA", type: "sampler2D", source: "textureA" },
          { name: "uB", type: "sampler2D", source: "textureB" },
          { name: "uFitA", type: "vec4", source: "fitA" },
          { name: "uFitB", type: "vec4", source: "fitB" },
          { name: "uRes", type: "vec2", source: "resolution" },
          { name: "uGrainA", type: "float", source: "frame:grainA" },
          { name: "uGrainB", type: "float", source: "frame:grainB" },
          { name: "uDrift", type: "vec2", source: "frame:drift" },
          { name: "uLadder", type: "float", source: "frame:ladder" },
          { name: "uTau", type: "float", source: "frame:tau" },
          { name: "uLoosen", type: "float", source: "frame:loosen" },
          { name: "uGather", type: "float", source: "frame:gather" },
          { name: "uCA", type: "vec2", source: "frame:cA" },
          { name: "uCB", type: "vec2", source: "frame:cB" },
          { name: "uR1", type: "float", source: "frame:R1" },
          { name: "uR2", type: "float", source: "frame:R2" },
          { name: "uN1", type: "float", source: "frame:n1" },
          { name: "uN2", type: "float", source: "frame:n2" },
          { name: "uAmp", type: "float", source: "frame:amp" },
          { name: "uPh", type: "float", source: "frame:ph" },
          { name: "uFlank", type: "float", source: "frame:flank" },
          { name: "uSpread", type: "float", source: "frame:spread" },
          { name: "uOff", type: "float", source: "frame:off" },
          { name: "uGuard", type: "float", source: "frame:guard" },
          { name: "uSeed", type: "float", source: "handle:seed" },
        ],
      }],
      // The instrument allocates nothing of its own: it spends the two source-texture slots the host
      // already holds and the one programme the host builds from this manifest.
      resources: { lean: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                           passes: 1, bytesEstimate: 0, variant: "lean" },
                   standard: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                               passes: 1, bytesEstimate: 0, variant: "standard" },
                   rich: { textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1,
                           passes: 1, bytesEstimate: 0, variant: "rich" } },
      capabilities: ["webgl2"],
      decline: ["one work only", "a source that never decoded"],
      provenance: { labPath: "lab/effects/matter.js", commit: "e0f1b91" },
      provenance: { labPath: "lab/effects/gears.js", commit: "e0f1b91" },
      readiness: "production-ready",
    };

    var live = false;
    return {
      name: "matter",
      name: "gears",
      manifest: manifest,
      values: values,
      fit: fit,
      feel: feelOf,
      prepare: function (o) {
        if (!o.sources) return { take: false, why: "the matter instrument needs both works" };
        if (!o.sources) return { take: false, why: "the meshing instrument needs both works" };
        if (!o.cue) return { take: false, why: "no cue names it" };
        return { take: true };
      },
      start: function () { live = true; },
      // The pose the shader draws. Every number in it comes from a handle a score can drive, and the
      // field's drift reads the second the host hands down, so a seeded run repeats to the pixel.
      frame: function (st) {
        if (!live) return;
        var h = st.handles;
        st.draw({
          mix: h.mix, loosen: h.loosen, drift: h.drift, gather: h.gather, grain: h.grain,
          shade: h.shade, travel: h.travel, seed: h.seed, t: h.clock, reduced: st.reduced,
      // The pose the shader draws. Every number in it comes from a handle a score can drive.
      //
      // THE REDRAW THE PRESERVED BUFFER STOOD IN FOR. The lab module drew on a parameter change, on
      // a resize and on its own frame loop, and under reduced motion it drew once and stopped —
      // whatever stayed on screen after that was the preserved buffer's doing. Here the host's
      // buffer keeps nothing between frames, so this draws on every frame it is handed, reduced or
      // not. Reduced motion stops the wheels' drive inside `values` and stops nothing else.
      frame: function (st) {
        if (!live) return;
        var h = st.handles;
        var dial = typeof h.dial === "number" ? h.dial : feelOf(clamp(h.mix, 0, 1));
        st.draw({
          dial: dial,
          size: h.size, centreX: h.centreX, centreY: h.centreY, bandPeriod: h.bandPeriod,
          ratio: h.ratio, tooth: h.tooth, order: h.order, turn: h.turn, flank: h.flank,
          shade: h.shade, travel: h.travel,
          cssWidth: st.viewport.w, cssHeight: st.viewport.h, t: h.clock, reduced: st.reduced,
        });
        if (st.progress >= 1 && !st.pinned) st.settle(st.token);
      },
      resize: function () {},
      cancel: function () {},
      dispose: function () { live = false; },
      contextLost: function () { live = false; },
      contextRestored: function () {},
    };
  }

  register(matterInstrument());
  register(gearsInstrument());

  // ---- the test instrument (§9/brief): reachable only when diagnostics are on -------------------
  // Ships INSIDE this file rather than as a separate registration point because it must be able to
  // call the host's own settle/fail with the exact tokens a real instrument would carry, including
  // the wrong ones — that is the only way the token/generation rows (2, 26) become a real run instead
  // of a claim. It draws nothing, owns nothing, and is never registered unless diagnostics are on.
  function makeTestInstrument() {
    var counts = { prepare: 0, start: 0, frame: 0, resize: 0, cancel: 0, dispose: 0,
                   contextLost: 0, contextRestored: 0 };
    var mode = "decline";   // decline | take | throw-prepare | throw-start | never | late | double |
                            // stale | fail — set with host.test.mode(name)
    var lastToken = null;
    var lateMs = 30;
    var inst = {
      name: "test",
      probe: true,
      prepare: function (offer) {
        counts.prepare++;
        lastToken = offer.token;
        if (mode === "throw-prepare") throw new Error("test: throw-prepare");
        if (mode === "decline") return { take: false, why: "test: decline" };
        return { take: true };
      },
      start: function () {
        counts.start++;
        if (mode === "throw-start") throw new Error("test: throw-start");
        if (mode === "never") return;                              // no callback, ever — the watchdog's job
        if (mode === "late") { setTimeout(function () { host.settle(lastToken); }, lateMs); return; }
        if (mode === "double") { host.settle(lastToken); host.settle(lastToken); return; }
        if (mode === "stale") { host.settle(lastToken - 1); return; }   // a foreign/old token
        if (mode === "fail") { host.fail(lastToken, "test: fail"); return; }
        host.settle(lastToken);
      },
      frame: function () { counts.frame++; },
      resize: function () { counts.resize++; },
      cancel: function () { counts.cancel++; },
      dispose: function () { counts.dispose++; },
      contextLost: function () { counts.contextLost++; },
      contextRestored: function () { counts.contextRestored++; },
    };
    return {
      inst: inst,
      counts: counts,
      mode: function (m) { if (m !== undefined) mode = String(m); return mode; },
      lateMs: function (ms) { if (ms !== undefined) lateMs = +ms; return lateMs; },
      lastToken: function () { return lastToken; },
      reset: function () {
        mode = "decline"; lastToken = null;
        Object.keys(counts).forEach(function (k) { counts[k] = 0; });
      },
    };
  }

  var diag = window.__@@NS@@Pass;
  if (diag) {
    var test = makeTestInstrument();
    register(test.inst);
    diag.host = host;
    diag.test = test;
    // The bench: the diagnostics-only hand a conformance row draws one frame with. It is the exact
    // road a running transaction takes — the same drawPose, the same programme cache, the same two
    // source textures — with the pose handed in instead of derived from a score, so the host's frame
    // and the lab module's frame can be compared on ONE pose rather than on two guesses at one.
    diag.bench = {
      make: function () { return !!stageMake(); },
      pair: function (a, b) {
        if (!stageMake()) return false;
        uploadPair({ a: a, b: b, aw: a.naturalWidth, ah: a.naturalHeight,
                     bw: b.naturalWidth, bh: b.naturalHeight });
        return true;
      },
      draw: function (id, pose) {
        var inst = instruments[id];
        if (!inst || !stage) return false;
        inst.manifest.passes.forEach(function (pass) { programFor(pass); });
        drawPose(inst, pose, { aw: pose.aw, ah: pose.ah, bw: pose.bw, bh: pose.bh });
        return true;
      },
      show: stageShow,
      manifest: function (id) { return instruments[id] ? instruments[id].manifest : null; },
      // The numbers of one frame, read without drawing it: the same pure function the draw calls.
      values: function (id, pose) { return instruments[id] ? instruments[id].values(pose) : null; },
      register: function (inst) { return register(inst); },
      es3: function (src, isVert) { return toES3(src, !!isVert); },
      // ---- the driver graph and the camera, read as data ----------------------------------------
      // A row states inputs and reads the value the evaluator answers with. Nothing is stubbed: this
      // is the same evalNode a running frame calls, and the same camera evaluation a running frame
      // applies — only the transaction around them is spared.
      driver: function (spec, nodes, ctx) {
        ctx = ctx || {};
        return evalNode(spec, {
          nodes: nodes || {},
          progress: ctx.progress || 0, cueProgress: ctx.cueProgress || 0,
          seconds: ctx.seconds || 0, velocity: ctx.velocity || 0,
          capability: ctx.capability === undefined ? 0.5 : ctx.capability,
          dt: ctx.dt || 0, state: ctx.state || {},
        }, 0);
      },
      cycle: function (nodes) { return cycleIn(nodes || {}); },
      scoreWhyNo: function (score) { return scoreWhyNo({ score: score, gen: 0 }); },
      camera: function (score, tSec, ownPose) {
        var rec = { cmd: { score: score, gen: 0 }, duration: (score.duration || 0),
                    said: {}, handoffs: [], camOwner: null, lastPose: null, ownPose: ownPose || null };
        var got = camPoseAt(rec, tSec);
        return { owner: got.owner, pose: got.pose, stage: got.stage, handoffs: rec.handoffs };
      },
      // ONE RECORD walked across several instants, so a handoff is measured inside one flight the
      // way a running transaction measures it, rather than across records that each start afresh.
      cameraWalk: function (score, times, ownPose) {
        var rec = { cmd: { score: score, gen: 0 }, duration: (score.duration || 0),
                    said: {}, handoffs: [], camOwner: null, lastPose: null, ownPose: ownPose || null };
        var poses = times.map(function (t) {
          var got = camPoseAt(rec, t);
          return { at: t, owner: got.owner, pose: got.pose, stage: got.stage };
        });
        return { poses: poses, handoffs: rec.handoffs };
      },
      // ---- the two geometries, read as data ------------------------------------------------------
      // THE RESEAT ITSELF, on stated boxes. A live flight cannot isolate this: on a walk that hangs
      // its works centred and small, the destination's pose barely moves when the frame changes, so
      // the step a cut reframe would leave is a fraction of what the flight is travelling anyway and
      // hides inside it. Here the two boxes are stated, and they may differ as much as a row likes.
      // The REAL reseatHang runs — the very function a resize reaches — so a reframe that stopped
      // carrying the pose across would show up as the picture moving at the instant the destination
      // did, which is the whole claim.
      hangReseat: function (scoreRec, durationMs, geomA, geomB, geomB2, tSec) {
        var turned = false;
        var rec = {
          cmd: { score: scoreRec, gen: 0, from: { id: "a" }, to: { id: "b" } },
          duration: durationMs, said: {}, placed: false,
          src: { aw: 1000, ah: 1000, bw: 1000, bh: 1000 },
          inst: instruments.weave,
          hooks: { hangGeometry: function (id) {
            if (id === "a") return geomA;
            return turned ? geomB2 : geomB;
          } },
          carry: null, carryFrom: 0, lastSeconds: tSec,
        };
        rec.hangEdge = hangEdges(rec);
        readHang(rec);
        function applied(t) {
          return camCompose(anchorPose(rec, t), CAM_NEUTRAL, rec.carry, carryWeight(rec, t));
        }
        var before = applied(tSec);
        turned = true;                 // the frame changed: the arriving work hangs elsewhere now
        reseatHang(rec);
        return { before: before, after: applied(tSec), end: applied(durationMs / 1000),
                 wants: rec.hangPoseB, carry: rec.carry };
      },
      camNeutral: function () { return CAM_NEUTRAL; },
      camCaps: function (variant) { return camCaps(variant); },
      camTolerances: function () { return { rest: CAM_REST_TOL, handoff: CAM_HANDOFF_TOL }; },
      ladder: function (ms, frames) {
        var t = 1e6;
        for (var i = 0; i < frames; i++) { t += ms; noteFrame(t); }
        return { scale: STEPS[stepIx], changes: changes };
      },
    };
  }

  join(host);
})();
