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
//   3. The registry and the instrument loader (§7). Every instrument lives in a file of its own,
//      and a visit fetches only the ones its own score names. The names come out of the score's
//      cues; the addresses, versions and digests come out of the site's own settings record, which
//      this host reads at boot. A file loads once its bytes weigh to the digest the record gives its
//      name and it declares the version the record gives it, and its instrument lands on the
//      registry under the name its own manifest carries. NO INSTRUMENT NAME IS WRITTEN IN THIS FILE,
//      and a conformance row greps the built host for every name that ships today and reds on any of
//      them. A TEST INSTRUMENT registers itself here, reachable only when diagnostics are on (§9's
//      lifecycle rows are built against it); it draws nothing and belongs to the host's own
//      machinery rather than to the picture.
//
// A command carrying no score reaches no production instrument at all: the score names the cue, the
// cue names the instrument. With no score the walk's own glide runs, which is the standing fallback.
(function () {
  var join = window.__@@NS@@PassLayer;
  if (typeof join !== "function") return;

  // ---- the three ranges of contract §2.5 — a legal value must read differently from a hang -------
  var DURATION_MIN = 0, DURATION_MAX = 14000;
  var PREPARE_MIN = 0, PREPARE_MAX = 400;
  // HOW LONG A COMMAND WAITS FOR THE INSTRUMENT FILES ITS OWN SCORE NAMES, and why it is its own
  // number rather than the prepare budget's. The prepare budget bounds an instrument that is
  // already in hand; this bounds a file crossing the network, which is a different thing and fails
  // for different reasons. It is short on purpose: the walk's own glide is what runs when the wait
  // runs out, and a visitor whose network is slow should meet that glide a quarter of a second late
  // rather than watch a still frame while a file arrives.
  var LOAD_MIN = 0, LOAD_MAX = 4000;
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
  var loadBudgetMs = 250;    // within LOAD_MIN…LOAD_MAX; overridable for testing (host.configure)
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
  //
  // `over` says this cue is being laid down onto a frame another cue has already drawn into. The
  // stack is DEPTH ORDER and nothing else: the charter's own law hands out no opacity handle and
  // lets no plan fade a layer, so the host imposes no weight of its own on any cue. What it does is
  // read the alpha the INSTRUMENT'S OWN shader writes, so an instrument that writes coverage —
  // matter here, nothing there — lets the frame beneath show through where it carries nothing.
  //
  // THE BLEND IS STRAIGHT SOURCE-OVER, AND PREMULTIPLIED IS REFUSED. One and the same fragment
  // shader serves two jobs. Laid over another cue it must contribute only its own matter. Laid down
  // FIRST — as the bottom cue of a stack, or as the whole of a one-cue score — it must write the
  // picture it has always written, and there the `else` branch below disables blending and the
  // fourth component is never read. A shader emitting premultiplied `rgb * a` would then write BLACK
  // wherever its alpha stands below 1, and a one-cue `matter` score would go black across its field.
  // Under SRC_ALPHA/ONE_MINUS_SRC_ALPHA the colour channel of every instrument is untouched, so a
  // one-cue score is byte-identical by construction rather than by measurement luck (row 54).
  //
  // No separate alpha equation is needed: the context is created with `alpha: false`, so the
  // destination alpha never reaches the page and no factor here reads it.
  //
  // Blending is switched off again for the bottom cue of every frame, so a one-cue score meets a
  // context in exactly the state the stage was built in. That is why the LOWEST cue of a stack must
  // be an instrument that fills the frame — its gaps would show the cleared buffer, there being
  // nothing drawn beneath it — which `coverageWhyNo` refuses at validation.
  function drawPose(inst, pose, src, over) {
    if (!stage) return;
    stageResize();
    var gl0 = stage.gl;
    if (over) {
      gl0.enable(gl0.BLEND);
      gl0.blendFunc(gl0.SRC_ALPHA, gl0.ONE_MINUS_SRC_ALPHA);
    } else {
      gl0.disable(gl0.BLEND);
      census.passesLastFrame = 0;
    }
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
  // Pan is normalised — a fraction of the frame. Pitch, yaw, roll, orbit, tilt and the field of view
  // are RADIANS.
  //
  // EVERY AXIS TRAVELS IN THE COORDINATE ITS OWN LAW IS STRAIGHT IN. The charter's shelf 2 states
  // the general form — a nonlinear camera is a straight line in another coordinate system, lawful in
  // its own space and miraculous on screen — and names two cases: a uniform zoom is a walk in
  // log-space, a polar orbit is a straight line in angle. So the record carries the LOGARITHM of the
  // dolly and the ANGLE of the orbit, and each is interpolated as it stands: an interpolation of
  // `logScale` is a geometric interpolation of scale, and the applied factor is exp of it, which is
  // the natural logarithm and no other base. Equal movement of the handle is then equal felt change
  // of approach, which is the measured-response law.
  //
  // WHAT THE COURSE IS, AND WHY IT IS NOT A STRAIGHT LINE IN TIME. Each axis is carried by the
  // monotone spline of §5 — his word of 2026-08-11, given after judging speed steps at segment
  // joints, made that the whole-track course. The charter's «straight line» fixes WHICH COORDINATE
  // is carried, never whether the carrying eases: an orbit splined in angle never leaves the circle
  // it travels, and it departs and arrives at rest instead of starting and stopping in one frame.
  //
  // ORBIT AND TILT TURN THE POINT OF VIEW ABOUT THE SUBJECT; PITCH, YAW AND ROLL TURN THE CAMERA
  // WHERE IT STANDS. They are different moves and the transform chain says which is which: orbit and
  // tilt act BEFORE the pan, so they turn the scene about the frame's own centre and the pan then
  // carries the turned subject to its place — the point of view travels around the work while the
  // work holds its framing. Pitch, yaw and roll act after, so the scene swings across the frame.
  // Both hangs are flat and square-on, so orbit and tilt stand at zero at either end of a flight and
  // the landing rests exactly as it did.
  var CAM_KEYS = ["panX", "panY", "logScale", "pitch", "yaw", "roll", "orbit", "tilt", "fov"];
  var CAM_NEUTRAL = { panX: 0, panY: 0, logScale: 0, pitch: 0, yaw: 0, roll: 0, orbit: 0, tilt: 0,
                      fov: null };
  // The two axes a score names only when it uses them. Every other place is part of every flight, so
  // a track that never names one has lost something and the host says so; a track that names no
  // orbit is simply a flight that does not orbit, and a sentence about it would be noise on every
  // passage the collection plays.
  var CAM_OPTIONAL = { orbit: 1, tilt: 1 };
  // The field of view a turn is seen through where a score names none. Without a projection an orbit
  // is an affine squash rather than a turn, so the host carries its own lens: 0.9 rad is 51.6
  // degrees across the frame's height, which is the ordinary lens a room is photographed with.
  var CAM_TURN_FOV = 0.9;
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
  //
  // EACH AXIS IS CARRIED THROUGH THE POINTS THAT NAME IT, AND THROUGH NO OTHERS. That is what gives
  // every axis its own arc on one unbroken flight: the dolly may rise and fall at the two edges
  // while the orbit sweeps once across the whole middle and the tilt holds a plane at an angle over
  // a window of its own, each on its own points at its own seconds. Until 2026-08-17 a place was
  // carried only where EVERY point named a number for it, so one axis could not be given its own
  // timing without giving every other axis a point at the same second — and a flight of several arcs
  // could not be written down at all. A track that names every place at every point reads exactly as
  // it did, which is what every composed score does.
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
      var own = [];
      for (var i = 0; i < pts.length; i++) {
        if (typeof camRead(pts[i].p, k) === "number") own.push(pts[i]);
      }
      if (!own.length) {
        if (say && !CAM_OPTIONAL[k]) {
          say("camera:" + k, "no point names a number for «" + k + "»; it stands at its neutral");
        }
        pose[k] = CAM_NEUTRAL[k];
        return;
      }
      pose[k] = splineAt(own, tSec, function (q) { return camRead(q.p, k); });
    });
    return pose;
  }

  // WHICH PLACES THIS DEVICE CAN CARRY. Pan, dolly and roll are a plain affine of the frame and every
  // device the host runs on carries them. Pitch, yaw and the field of view need the perspective road,
  // and §7's degrade ladder lightens the score FIRST — so the `lean` variant drops those three and
  // records the fallback. Which axes lean drops is a taste call and is named as a question.
  // Orbit and tilt travel with pitch and yaw: a turn about the subject is seen through a projection,
  // and without one it is an affine squash rather than a turn.
  function camCaps(variant) {
    var deep = variant !== "lean";
    return { panX: true, panY: true, logScale: true, roll: true, pitch: deep, yaw: deep, fov: deep,
             orbit: deep, tilt: deep };
  }

  // The pose, applied. One transform on the host's own canvas, above every pixel the instrument drew.
  //
  // THE ORDER OF THE CHAIN IS THE STATEMENT ABOUT WHAT MOVES. A transform list is applied right to
  // left, so what stands nearest the scale acts on the picture first: the picture is scaled, then
  // tilted and orbited about the canvas's own centre, then turned by the camera's own pitch, yaw and
  // roll, and only then panned into its place in the frame. Orbit and tilt therefore turn the SCENE
  // about the point the pan is holding — the point of view travels around the subject and the
  // subject keeps its framing — while pitch, yaw and roll turn the camera where it stands and let
  // the scene swing across the frame.
  function camApply(pose, caps) {
    if (!stage) return;
    if (!pose) { stage.canvas.style.transform = ""; return; }
    var s = Math.exp(caps.logScale ? pose.logScale : 0);
    var deg = 180 / Math.PI;
    var turn = (caps.orbit && pose.orbit) || (caps.tilt && pose.tilt);
    var fov = (caps.fov && typeof pose.fov === "number" && pose.fov > 0) ? pose.fov
            : (turn ? CAM_TURN_FOV : 0);
    var t = "";
    if (fov) t += "perspective(" + (0.5 * Math.max(cssH, 1) / Math.tan(fov / 2)).toFixed(3) + "px) ";
    t += "translate(" + (caps.panX ? pose.panX * 100 : 0).toFixed(4) + "%,"
       + (caps.panY ? pose.panY * 100 : 0).toFixed(4) + "%) ";
    if (caps.pitch && pose.pitch) t += "rotateX(" + (pose.pitch * deg).toFixed(4) + "deg) ";
    if (caps.yaw && pose.yaw) t += "rotateY(" + (pose.yaw * deg).toFixed(4) + "deg) ";
    if (caps.roll && pose.roll) t += "rotate(" + (pose.roll * deg).toFixed(4) + "deg) ";
    if (caps.orbit && pose.orbit) t += "rotateY(" + (pose.orbit * deg).toFixed(4) + "deg) ";
    if (caps.tilt && pose.tilt) t += "rotateX(" + (pose.tilt * deg).toFixed(4) + "deg) ";
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
  // ONE READING OF THE SEATING, asked of the instrument on the buffer it is drawing on. The draw
  // binds exactly this as its `fitA`/`fitB` uniforms and the frame state hands exactly this to the
  // instrument's own script, so the shader's seating and the script's seating are one number.
  function instFit(inst, iw, ih) {
    try { return inst.fit(iw, ih, W, H) || null; } catch (e) { return null; }
  }
  function hangPoseOf(geom, inst, iw, ih) {
    if (!geom || !geom.w || !geom.h || cssW <= 0 || cssH <= 0) return null;
    var f = instFit(inst, iw, ih);
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

  // A CAMERA-LED PASSAGE: the flight itself is the transition. A score declares it with
  // `camera.lead`, and it says that the world voice of the levels law is spent on the camera — the
  // travel of the point of view through the scene is what carries the visitor from one work to the
  // other, and the instruments underneath hold a quiet register on their own levels.
  function camLed(score) {
    return !!(score && score.camera && score.camera.lead);
  }

  // The anchor at one second: one monotone spline per place through four points — the departing
  // hang, the whole frame, the whole frame again, the arriving hang. The two middle points hold the
  // same value, so the spline's own slopes there are zero and the crossing plays at the whole frame
  // without drifting through it.
  //
  // A LED FLIGHT HAS NO HELD MIDDLE. Where the camera accompanies, the passage rises to the whole
  // frame, plays the crossing there and descends: the flight stands still through the middle while
  // the instruments work. Where the camera LEADS, standing still would be the passage stopping, so
  // the anchor is three points instead of four — the departing hang, the whole frame at the halfway
  // second, the arriving hang — and the pose travels the entire duration without ever resting. The
  // two ends are the same two hangs either way, so the landing rests exactly as it did.
  function anchorPose(rec, tSec) {
    var A = rec.hangPoseA, B = rec.hangPoseB;
    if (!A && !B) return null;
    var e = rec.hangEdge || hangEdges(rec), N = CAM_NEUTRAL;
    var led = camLed(rec.cmd && rec.cmd.score);
    var at = led ? [0, e.dur / 2, e.dur] : [0, e.rise, e.dur - e.fall, e.dur];
    var poses = led ? [A || N, N, B || N] : [A || N, N, N, B || N];
    var out = {};
    CAM_KEYS.forEach(function (k) {
      if (k === "fov") { out[k] = null; return; }
      var pts = [], i;
      for (i = 0; i < at.length; i++) {
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

  // A score names one cue or several. The FIRST LINE is the primary one: it is the cue whose doors
  // the interruption cadence walks to and whose instrument seats the two hang boxes, so a one-cue
  // score reads exactly as it always did and a stack adds voices around that same spine.
  function cueOf(cmd) {
    var s = cmd && cmd.score;
    if (!s || !s.cues || !s.cues.length) return null;
    return s.cues[0];
  }
  function cuesOf(cmd) {
    var s = cmd && cmd.score;
    return (s && s.cues && s.cues.length) ? s.cues : [];
  }

  // ---- the stack (§4.4's `stack`) -----------------------------------------------------------------
  // THE SCORE'S OWN ORDER IS THE STACK UNLESS THE SCORE SAYS OTHERWISE. Where no cue names a
  // `stack`, the first line stands topmost, so the first cue takes the highest number and the last
  // takes the lowest. Higher stands nearer the eye. The returned list is DRAW ORDER — ascending, so
  // the cue nearest the eye is laid down last and covers what it draws over.
  //
  // The tie is broken by the same sentence: where two cues name one number, the earlier line is the
  // nearer of the two, so it is drawn later.
  function stackOrder(cues) {
    var n = cues.length;
    var rows = cues.map(function (c, i) {
      var s = (c.stack === undefined || c.stack === null) ? (n - i) : Number(c.stack);
      if (!isFinite(s)) s = n - i;
      return { cue: c, stack: s, line: i };
    });
    rows.sort(function (p, q) { return (p.stack - q.stack) || (q.line - p.line); });
    return rows;
  }

  // WHETHER A CUE IS PLAYING AT THIS SECOND. A cue naming no window plays the whole pass, which is
  // what a one-cue score written before windows existed means. Both edges are inside the window, so
  // a cue whose window closes exactly at the pass's own last second still draws the door it lands.
  function cueLiveAt(cue, seconds) {
    var w = cue && cue.window;
    if (Object.prototype.toString.call(w) !== "[object Array]" || w.length < 2) return true;
    return seconds >= Number(w[0]) && seconds <= Number(w[1]);
  }
  // ---- the three properties of a WHOLE score that no single frame can see -------------------------
  // Two cues share an instant when their windows touch: both edges are inside a window, so a cue
  // closing at the very second another opens is live at that one second and the two are judged
  // together. A cue naming no window plays the whole pass and therefore meets every other cue.
  function windowsMeet(a, b) {
    var wa = a && a.window, wb = b && b.window;
    var arr = "[object Array]";
    if (Object.prototype.toString.call(wa) !== arr) return true;
    if (Object.prototype.toString.call(wb) !== arr) return true;
    return Number(wa[0]) <= Number(wb[1]) && Number(wb[0]) <= Number(wa[1]);
  }
  function metAcross(a, b) {
    var wa = a.window || [0, 0], wb = b.window || [0, 0];
    return Math.max(Number(wa[0]), Number(wb[0])) + "…" + Math.min(Number(wa[1]), Number(wb[1]));
  }

  // THE LEVELS LAW (§4.4, the charter's shelf 17) IS ENFORCED AT BUILD TIME, AND NO LONGER HERE.
  // One voice to a structural level: two cues whose level lists intersect in windows that meet are
  // a red, unless one declares itself the accompaniment of the other on that level. The law keeps
  // its full force; only its home changed, on 2026-08-14.
  //
  // WHY IT MOVED. The declaration the law reads is the cue's own `levelOwnership` record, and
  // §4.4's cue allow-list is closed and does not carry that field — a score is refused whole on any
  // unknown field. A run-time checker here therefore stood on a field no legal score may carry, and
  // a real allow-list checker would refuse every composed score before this code was ever reached.
  // The levels law is a law about how a passage is COMPOSED, and it is decidable the moment the
  // plan is authored, from the plan alone. Nothing about a live frame informs it.
  //
  // WHERE IT IS ENFORCED NOW. tlvphotos-sceneplan, lab/sceneplan-build-check.py — the per-level
  // reading that gathers each level's holders, requires every declared level to be owned or
  // accompanied, and refuses two owners of one level. That gate runs over the authored plans at
  // build time, and a plan that breaks the law never becomes a score the host could be handed.

  // THE TIER BUDGET (§4.4, the charter's shelf 17). The reckoning is a plain record so a row can
  // read every number it is judged on rather than only the verdict.
  //
  // The three bands, in seconds, and what each carries:
  //   quiet        2…4    exactly one letter, at most one accompaniment, no miracle
  //   middle       5…8    at most two letters, at most two accompaniments, at most one miracle
  //   culmination  9…14   two or three letters, at most three accompaniments, exactly one miracle
  //
  // A duration falling in NO band names no tier, and the budget then stands aside with that reason
  // recorded. §2.5 makes `duration: 0` a legal instant transition and the bands leave gaps between
  // them, so a score outside every band is a score the tier rules say nothing about.
  var TIERS = [
    { name: "quiet", lo: 2, hi: 4, lettersLo: 1, lettersHi: 1, accompaniments: 1,
      miraclesLo: 0, miraclesHi: 0 },
    { name: "middle", lo: 5, hi: 8, lettersLo: 0, lettersHi: 2, accompaniments: 2,
      miraclesLo: 0, miraclesHi: 1 },
    { name: "culmination", lo: 9, hi: 14, lettersLo: 2, lettersHi: 3, accompaniments: 3,
      miraclesLo: 1, miraclesHi: 1 },
  ];
  var HELD_MAX = 1 / 3;

  // The seconds of the pass some cue's window covers, with the overlaps merged so a second under
  // three cues counts once. What is left over is HELD TIME: the passage standing with no voice
  // playing, which is the reading of the charter's «held time (vistas + crests)» the host can
  // actually measure from a score.
  function coveredSeconds(cues, durSec) {
    var spans = [], i;
    for (i = 0; i < cues.length; i++) {
      var w = cues[i].window;
      var lo = 0, hi = durSec;
      if (Object.prototype.toString.call(w) === "[object Array]" && w.length >= 2) {
        lo = Math.max(0, Number(w[0]));
        hi = Math.min(durSec, Number(w[1]));
      }
      if (hi > lo) spans.push([lo, hi]);
    }
    spans.sort(function (p, q) { return p[0] - q[0]; });
    var total = 0, at = -1;
    for (i = 0; i < spans.length; i++) {
      var s = Math.max(spans[i][0], at < 0 ? spans[i][0] : at);
      if (spans[i][1] > s) { total += spans[i][1] - s; at = spans[i][1]; }
      else if (at < spans[i][1]) at = spans[i][1];
    }
    return total;
  }

  function budgetOfScore(score) {
    var cues = (score && score.cues) || [];
    var durSec = clampNum(score && score.duration, DURATION_MIN, DURATION_MAX) / 1000;
    var letters = 0, accompaniments = 0, miracles = 0;
    cues.forEach(function (c) {
      if (c.voice === "letter") letters++;
      else if (c.voice === "accompaniment") accompaniments++;
      else if (c.voice === "miracle") miracles++;
    });
    // THE CAMERA COUNTS AS ONE ACCOMPANIMENT wherever the score names a camera track (§4.4, amended
    // 2026-08-14 10:31). The camera is carried in the score's own `camera` record rather than as a
    // cue, so a count reading the cues alone never saw it and every scored flight was one short.
    // The charter's shelf 17 opens its list of accompaniment voices with the camera and closes with
    // «EVERYTHING counts; no never-counted class exists».
    var track = score && score.camera && score.camera.track;
    var camera = Object.prototype.toString.call(track) === "[object Array]" && track.length > 0;
    if (camera) accompaniments++;
    var covered = coveredSeconds(cues, durSec);
    var held = durSec > 0 ? (durSec - covered) / durSec : 0;
    var tier = null;
    for (var i = 0; i < TIERS.length; i++) {
      if (durSec >= TIERS[i].lo && durSec <= TIERS[i].hi) { tier = TIERS[i]; break; }
    }
    var rec = { tier: tier ? tier.name : null, seconds: +durSec.toFixed(4),
                letters: letters, accompaniments: accompaniments, miracles: miracles,
                camera: camera, cameraCounted: camera ? 1 : 0,
                coveredSeconds: +covered.toFixed(4), held: +held.toFixed(6), heldMax: HELD_MAX,
                why: null };
    if (held >= HELD_MAX) {
      rec.why = "held time stands at " + (held * 100).toFixed(1) + " percent of the pass, and a "
              + "third is the ceiling — " + (durSec - covered).toFixed(3) + " s of " + durSec
              + " s carry no cue at all";
      return rec;
    }
    if (!tier) {
      rec.whyNoTier = "a duration of " + durSec + " s falls in no tier band (2…4, 5…8, 9…14), so "
                    + "the tier rules say nothing about this score";
      return rec;
    }
    if (letters < tier.lettersLo || letters > tier.lettersHi) {
      rec.why = "a " + tier.name + " carries " + (tier.lettersLo === tier.lettersHi
                ? tier.lettersLo + " letter" : tier.lettersLo + " to " + tier.lettersHi + " letters")
              + " and this score carries " + letters;
    } else if (accompaniments > tier.accompaniments) {
      rec.why = "a " + tier.name + " carries at most " + tier.accompaniments + " accompaniments and "
              + "this score carries " + accompaniments
              + (camera ? ", the camera among them" : "");
    } else if (miracles < tier.miraclesLo || miracles > tier.miraclesHi) {
      rec.why = "a " + tier.name + " carries " + (tier.miraclesLo === tier.miraclesHi
                ? "exactly " + tier.miraclesLo : "at most " + tier.miraclesHi) + " miracle"
              + (tier.miraclesHi === 1 ? "" : "s") + " and this score carries " + miracles;
    }
    return rec;
  }

  // THE SCORE, JUDGED ONCE, BEFORE ANYTHING IS TAKEN (§5/§6/§4.4). Returns the reason it is refused,
  // or null. Everything checked here is a property of the WHOLE score that no single frame can see:
  // a driver graph that reaches itself, two cues both claiming the camera at one instant, two cues
  // standing on one structural level at one instant, one instrument asked to carry two cues at once,
  // and the tier budget.
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
    // A LED FLIGHT SPENDS THE WORLD VOICE, AND NOTHING MAY SPEND IT TWICE. The charter's shelf 17
    // opens its list of voices with the camera and its levels law allows one active voice per
    // structural level, the world being the camera's own. So a score that declares `camera.lead`
    // and then gives a cue the world level is asking for two voices on one level, which the law
    // calls noise, and it is refused before the command is taken. The levels law is otherwise a
    // build-time reading (see the note above the tier budget); this one case is decidable here
    // because the declaration and the claim both stand in the score the host was handed.
    if (camLed(s)) {
      for (i = 0; i < cues.length; i++) {
        if ((cues[i].levels || []).indexOf("WORLD") >= 0) {
          return "the camera leads this passage and cue «" + cues[i].id + "» claims the world level "
               + "beside it — one voice to a level";
        }
      }
    }
    // ONE INSTRUMENT CARRIES ONE CUE AT A TIME. An instrument is one object on the host's registry
    // with one set of its own state, so two cues naming it across windows that meet would have it
    // playing two parts at once through a single `live` flag and a single pose.
    for (i = 0; i < cues.length; i++) {
      for (j = i + 1; j < cues.length; j++) {
        var ia = cues[i].instrument && cues[i].instrument.id;
        var ib = cues[j].instrument && cues[j].instrument.id;
        if (ia && ia === ib && windowsMeet(cues[i], cues[j])) {
          return "cues «" + cues[i].id + "» and «" + cues[j].id + "» both name the instrument «"
               + ia + "» across " + metAcross(cues[i], cues[j])
               + " s — one instrument carries one cue at a time";
        }
      }
    }
    var cov = coverageWhyNo(cues);
    if (cov) return cov;
    // The levels law is checked over the authored plan at build time and not here; see the note
    // above budgetOfScore for where it lives and why it moved.
    var bud = budgetOfScore(s);
    if (bud.why) return "the tier budget: " + bud.why;
    return null;
  }

  // THE COVERAGE PLACEMENT RULE (§7's coverage law, §8's `coverage` block).
  //
  // A stack is drawn ASCENDING, so the lowest cue is laid down first onto the cleared buffer and the
  // cue nearest the eye is laid down last. Two placements follow, and they are mirror images:
  //
  //   · THE LOWEST CUE MUST FILL THE FRAME. Nothing is drawn beneath it, blending is disabled for
  //     it, and its alpha is never read — so where its matter is absent the cleared buffer shows.
  //     That cue's instrument must declare `coverage.writes === false`.
  //   · EVERY CUE ABOVE THE LOWEST MUST WRITE COVERAGE. A frame-filling cue anywhere above the floor
  //     is drawn over voices that are then never seen, which is exactly the defect measured on
  //     2026-08-14: three instruments in one frame, every one of them opaque, and the band family
  //     the whole passage stands on visible at no instant.
  //
  // A ONE-CUE SCORE IS EXEMPT FROM BOTH. It never enables blending, so its alpha is never read and
  // the law costs it nothing — which is what row 54 measures.
  //
  // An instrument the registry does not carry is left to `voicesFor`, which refuses the whole score
  // on its own terms; this check stays silent about it rather than reporting a second reason.
  function coverageWhyNo(cues) {
    if (!cues || cues.length < 2) return null;
    var rows = stackOrder(cues), i, inst, m, id;
    for (i = 0; i < rows.length; i++) {
      id = rows[i].cue.instrument && rows[i].cue.instrument.id;
      inst = instruments[id];
      m = inst && inst.manifest;
      if (!m) continue;
      var fills = !(m.coverage && m.coverage.writes === true);
      if (i === 0 && !fills) {
        return "cue «" + rows[i].cue.id + "» stands lowest in the stack and its instrument «" + id
             + "» writes coverage — the lowest cue is drawn onto the cleared buffer with no blending,"
             + " so it must fill the frame";
      }
      if (i > 0 && fills) {
        return "cue «" + rows[i].cue.id + "» stands over another cue and its instrument «" + id
             + "» fills the frame whole — everything beneath it would be drawn and never seen";
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

  // THE VOICES OF THE STACK, in draw order, each carrying the instrument its own cue names. A
  // command with no score at all reaches only the diagnostics probe, which is what a command with no
  // score has always meant. ONE unknown instrument refuses the whole score: a stack missing a voice
  // is not the passage the score names, and playing it short would be a picture nobody wrote.
  function voicesFor(cmd) {
    var cues = cuesOf(cmd);
    if (!cues.length) {
      if (!probe) return null;
      return [{ cue: null, inst: probe, said: {}, driverState: {}, lastHandles: null,
                applied: null, live: true, stack: 0, line: 0 }];
    }
    var rows = stackOrder(cues), out = [];
    for (var i = 0; i < rows.length; i++) {
      var id = rows[i].cue.instrument && rows[i].cue.instrument.id;
      if (!instruments[id]) { logEvt("no-instrument", cmd.gen, String(id)); return null; }
      out.push({ cue: rows[i].cue, inst: instruments[id], said: {}, driverState: {},
                 lastHandles: null, applied: null,
                 live: false, stack: rows[i].stack, line: rows[i].line });
    }
    return out;
  }
  // The instruments of a stack, each named once, in draw order — what `prepare`, the programme
  // build and `dispose` walk, so an instrument carrying two cues is asked once.
  function instrumentsOf(voices) {
    var seen = [], out = [];
    voices.forEach(function (v) {
      if (seen.indexOf(v.inst) >= 0) return;
      seen.push(v.inst);
      out.push(v.inst);
    });
    return out;
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

  // ---- resources across a stack (§7) --------------------------------------------------------------
  var RES_KEYS = ["textures", "textureSlots", "framebuffers", "pingPong", "programs", "passes",
                  "bytesEstimate"];
  // THE BUDGET PER QUALITY VARIANT. §7 has the host compare a declaration against the budget for the
  // chosen variant and then grant it, grant a lower variant, or decline. The budget itself had no
  // home in the code until a stack made the sum worth comparing against anything.
  //
  // THESE THREE ROWS ARE PROVISIONAL BASELINES AWAITING A REAL DEVICE, and they are labelled so
  // here beside the per-tier durations and the render scale, which stand in the same state. They
  // carry no measurement behind them yet. They are set so one instrument fits every variant, a
  // stack of three fits `standard` and `rich`, and `lean` stops at two — which is §7's own floor,
  // «below which the plain fallback plays instead of a thin miracle».
  //
  // WHAT A NUMBER HERE IS, AND WHAT IT IS NOT (his word of 2026-08-14 08:39). A size limit is an
  // observed performance baseline with evidence behind it. It is a reading of what a device can
  // carry, and a change to one of these rows is answerable by a measurement rather than by taste.
  // None of these numbers is an artistic law: no row here says what a passage should look like, and
  // no plan is shaped by one.
  //
  // AUTOMATIC TIER SELECTION STAYS DISABLED until real-device evidence supports it. The variant is
  // read from the qualityTier SETTING (variantOf, just above) and from nothing else — the host
  // measures no device and picks no tier on a visitor's behalf. What the host does do is lower a
  // variant that will not fit and record the reason, which is arithmetic against the rows below and
  // needs no reading of the device at all.
  //
  // What is built here is the road that reads these numbers, and moving a row moves no line of it.
  var VARIANTS = ["lean", "standard", "rich"];
  var BUDGET = {
    lean: { textures: 2, textureSlots: 4, framebuffers: 1, pingPong: 0, programs: 2, passes: 2,
            bytesEstimate: 8388608 },
    standard: { textures: 4, textureSlots: 8, framebuffers: 2, pingPong: 1, programs: 4, passes: 4,
                bytesEstimate: 33554432 },
    rich: { textures: 8, textureSlots: 16, framebuffers: 4, pingPong: 2, programs: 8, passes: 8,
            bytesEstimate: 100663296 },
  };

  // What ONE cue declares at a variant. A cue may carry its own per-variant map, or one flat record
  // naming the variant it stands for; carrying neither, the instrument's manifest answers for it.
  function cueDeclares(cue, inst, variant) {
    var r = cue && cue.resources;
    if (r) {
      if (r[variant]) return r[variant];
      if (typeof r.variant === "string") return r;
    }
    return (inst && inst.manifest && (inst.manifest.resources || {})[variant]) || null;
  }

  // THE PEAK OF THE STACK, which is the thing a budget has to be compared against. With several
  // instruments live at once the grants add up, so the sum is taken across the cues live at one
  // instant. The live set changes only where a window opens, so summing at every opening second
  // finds the true worst instant without sampling the pass. Each resource takes its own ceiling.
  function peakDeclared(voices, variant) {
    var edges = [0], i, k, n;
    for (i = 0; i < voices.length; i++) {
      var w = voices[i].cue && voices[i].cue.window;
      if (Object.prototype.toString.call(w) === "[object Array]") edges.push(Number(w[0]));
    }
    var peak = { textures: 0, textureSlots: 0, framebuffers: 0, pingPong: 0, programs: 0,
                 passes: 0, bytesEstimate: 0 };
    var most = 0, at = 0, ids = [];
    for (k = 0; k < edges.length; k++) {
      var sum = { textures: 0, textureSlots: 0, framebuffers: 0, pingPong: 0, programs: 0,
                  passes: 0, bytesEstimate: 0 }, here = [];
      for (i = 0; i < voices.length; i++) {
        if (!cueLiveAt(voices[i].cue, edges[k])) continue;
        var d = cueDeclares(voices[i].cue, voices[i].inst, variant) || {};
        for (n = 0; n < RES_KEYS.length; n++) sum[RES_KEYS[n]] += Number(d[RES_KEYS[n]]) || 0;
        here.push(voices[i].cue && voices[i].cue.id);
      }
      for (n = 0; n < RES_KEYS.length; n++) {
        if (sum[RES_KEYS[n]] > peak[RES_KEYS[n]]) peak[RES_KEYS[n]] = sum[RES_KEYS[n]];
      }
      if (here.length > most) { most = here.length; at = edges[k]; ids = here; }
    }
    peak.at = at;
    peak.cues = ids;
    return peak;
  }

  function overBudget(sum, budget) {
    for (var i = 0; i < RES_KEYS.length; i++) {
      if ((sum[RES_KEYS[i]] || 0) > (budget[RES_KEYS[i]] || 0)) return RES_KEYS[i];
    }
    return null;
  }

  // §7's grant, made a road: compare the summed declaration against the chosen variant's budget and
  // grant it, grant a LOWER variant, or decline. The ladder walks down only — a device asking for
  // `lean` is never handed `rich` because the sum happened to fit up there.
  function grantVariant(voices, want) {
    var ix = VARIANTS.indexOf(want);
    if (ix < 0) ix = VARIANTS.indexOf("standard");
    var tried = [];
    for (var i = ix; i >= 0; i--) {
      var name = VARIANTS[i], sum = peakDeclared(voices, name);
      var over = overBudget(sum, BUDGET[name]);
      tried.push({ variant: name, over: over, asked: over ? sum[over] : null,
                   grants: over ? BUDGET[name][over] : null });
      if (!over) {
        return { variant: name, sum: sum, budget: BUDGET[name], tried: tried, why: null,
                 lowered: name !== want };
      }
    }
    var last = tried[tried.length - 1], floor = VARIANTS[0];
    return { variant: null, sum: peakDeclared(voices, floor), budget: BUDGET[floor], tried: tried,
             lowered: false,
             why: "the stack asks for " + last.asked + " " + last.over + " at «" + floor
                + "», which grants " + last.grants };
  }

  // The census against the declaration (§7). The cues declared textures, framebuffers and a byte
  // estimate; the host counts what was actually created FOR THEM and shows both, so a declaration
  // that understates its counts or its bytes reads as the lie it is. With a stack the declaration
  // being judged is the SUM at the pass's worst instant.
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
                // Whether the flight itself was the transition, so a walk and a row can read what
                // kind of passage played rather than infer it from the shape of the pose.
                cameraLed: camLed(rec.cmd.score),
                cadence: rec.cadence || null, handles: rec.lastHandles || null,
                hang: hangRow(rec),
                stack: (rec.voices || []).map(function (v) {
                  return { id: v.cue ? v.cue.id : null, instrument: v.inst.name, stack: v.stack,
                           line: v.line, live: !!v.live,
                           window: v.cue ? (v.cue.window || null) : null,
                           levels: v.cue ? (v.cue.levels || null) : null,
                           handles: v.lastHandles || null,
                           // THE READING SURVIVES THE LANDING. A walk asks what happened once the
                           // pass has landed and the host is idle again, so the last thing each
                           // instrument published has to be readable after its voice is gone.
                           applied: v.applied || null };
                }),
                live: rec.liveCues || [], drew: rec.drewLastFrame || 0,
                budget: budgetOfScore(rec.cmd.score), grant: rec.grant || null };
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
    // EVERY instrument of the stack releases what it was granted, in draw order.
    instrumentsOf(rec.voices || []).forEach(function (x) {
      try { if (x.dispose) x.dispose(); } catch (e) {}
    });
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
  // Each voice of the stack carries its OWN node table, its own cue progress and its own remembering
  // driver state, so one cue's `slew` can never be read by another and two cues naming one node name
  // stay apart.
  function driverCtx(rec, v, progress, seconds, dt) {
    var cue = v.cue || {}, w = cue.window || [0, rec.duration / 1000];
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
      state: v.driverState,
    };
  }
  function handlesOf(rec, v, progress, seconds, dt) {
    var m = v.inst.manifest, cue = v.cue, out = {};
    var ctx = driverCtx(rec, v, progress, seconds, dt);
    Object.keys(m.handles).forEach(function (k) {
      var h = m.handles[k], got = null;
      if (cue && cue.tracks && cue.tracks[k]) got = evalNode(cue.tracks[k], ctx, 0);
      if (!got || !got.ok) {
        if (h.open && !(cue && cue.tracks && cue.tracks[k])) { out[k] = undefined; return; }
        if (!v.said[k]) {
          v.said[k] = true;
          logEvt("handle-fallback", rec.cmd.gen, k + ": " + ((got && got.why) || "the score drives it with no track"));
        }
        out[k] = h.def;
      } else {
        out[k] = clampNum(got.v, h.min, h.max);
      }
    });
    v.lastHandles = out;
    if (v === rec.primary) rec.lastHandles = out;
    return out;
  }

  // WHERE A CUE HOLDS WHILE IT IS NOT PLAYING. A cue outside its window draws nothing and holds
  // every handle at the value ITS OWN DOOR gives — the entry door before the window opens, the exit
  // door after it closes. Each is that cue's own tracks read at the door's own instant, with the
  // door handle pinned to exactly the number the door names, which is the same reckoning the
  // interruption cadence walks to. The record is built once per pass and per door, since neither
  // the tracks nor the doors move.
  function doorHandles(rec, v, which) {
    var key = "door:" + which;
    if (v[key]) return v[key];
    var cue = v.cue || {}, doors = cue.doors || {}, d = doors[which];
    var w = cue.window || [0, rec.duration / 1000];
    var seconds = which === "in" ? Number(w[0]) : Number(w[1]);
    var progress = rec.duration > 0 ? Math.max(0, Math.min(1, seconds * 1000 / rec.duration))
                                    : (which === "in" ? 0 : 1);
    var at = handlesOf(rec, v, progress, seconds, 0);
    var out = {};
    Object.keys(at).forEach(function (h) { out[h] = at[h]; });
    if (d && d.handle && v.inst.manifest.handles[d.handle]) {
      out[d.handle] = clampNum(d.value, v.inst.manifest.handles[d.handle].min,
                               v.inst.manifest.handles[d.handle].max);
    }
    v[key] = out;
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
    var v = rec.primary, cue = v.cue || {}, doors = cue.doors || {};
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
    var want = handlesOf(rec, v, progress, seconds, 0);
    var at_door = {};
    Object.keys(want).forEach(function (h) { at_door[h] = want[h]; });
    at_door[k] = clampNum(doors[which].value, v.inst.manifest.handles[k].min,
                          v.inst.manifest.handles[k].max);
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
    var live = rec.lastHandles
             || handlesOf(rec, rec.primary, rec.lastProgress || 0, rec.lastSeconds || 0, 0);
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
    instrumentsOf(rec.voices || []).forEach(function (x) {
      try { if (x.cancel) x.cancel(reason); } catch (e) {}
    });
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
  // ONE FRAME OF THE WHOLE STACK. The camera is read once for the instant, because §6 keeps one
  // authority per instant however many voices are playing, and it is applied once to the canvas
  // above everything drawn into it.
  //
  // The voices are walked in DRAW ORDER — ascending stack, so the cue nearest the eye is laid down
  // last. Every live cue draws into THE ONE CANVAS and THE ONE CONTEXT; nothing here makes a second
  // of either, which is §7's law and holds at any number of cues. A cue outside its window draws
  // nothing and holds its handles at its own door.
  //
  // `drew` counts what has already been laid down this frame, so the first cue clears the frame's
  // pass count and every later one composites over what stands there.
  function playFrame(rec, seconds, progress, dt, hold) {
    var cam = camPoseAt(rec, seconds);
    rec.camera = cam;
    // A CUE'S WINDOW IS WRITTEN IN THE PASS'S OWN SECONDS, and the pass's own seconds run from zero
    // to its duration. A second outside that span is judged AT THE NEAREST END OF IT, because that
    // is where the transaction actually stands: a frame landing at 3.01 s of a 3 s pass is the pass
    // at its last instant, and the cue holding the last door is the cue that must draw it. Without
    // this, the frames past the final second fall outside every window, nothing draws, and a pass
    // whose instrument settles on its own last frame never settles at all.
    //
    // It is also what keeps a pinned bench clock honest. The pins stop the frame loop reading the
    // wall clock so one instant can be photographed twice; a bench that pins the clock past the
    // pass's end is still photographing the pass's last instant, and the picture it draws reads the
    // pinned second exactly as it always did — only the question of WHICH cues are playing is asked
    // at the pass's own end.
    var span = rec.duration > 0 ? rec.duration / 1000 : 0;
    var judge = span > 0 ? Math.max(0, Math.min(seconds, span)) : 0;
    var drew = 0, live = [];
    for (var i = 0; i < rec.voices.length; i++) {
      var v = rec.voices[i];
      var on = cueLiveAt(v.cue, judge);
      v.live = on;
      if (!on) {
        // Held at its own door: the entry door before its window opens, the exit door after it
        // closes. Nothing is drawn, and the handles a reader sees are the door's own numbers.
        v.lastHandles = doorHandles(rec, v, judge < Number((v.cue.window || [0, 0])[0])
                                            ? "in" : "out");
        continue;
      }
      live.push(v.cue && v.cue.id);
      var handles = (hold && v === rec.primary) ? hold
                  : (hold ? doorHandles(rec, v, (rec.cadence && rec.cadence.door) || "out")
                          : handlesOf(rec, v, progress, seconds, dt));
      v.inst.frame(frameState(rec, v, seconds, progress, handles, cam, hold, drew));
      if (v.drawnThisFrame) { drew++; v.drawnThisFrame = false; }
      if (hold) v.lastHandles = handles;
    }
    rec.liveCues = live;
    rec.drewLastFrame = drew;
    camApply(cam.pose, rec.caps);
    if (hold) rec.lastHandles = hold;
  }

  // The record one voice receives. Held apart from the loop above so the closure over `v` and `drew`
  // is made once per voice per frame rather than captured by accident from a shared variable.
  function frameState(rec, v, seconds, progress, handles, cam, hold, drew) {
    return {
      token: rec.cmd.gen, t: seconds, progress: progress,
      handles: handles,
      // The frame, and the grid it is drawn on. `w`/`h` are CSS pixels; `bufferW`/`bufferH` are the
      // drawing buffer this host binds as the `resolution` source, which is the CSS frame times the
      // device ratio times the live resolution step. An instrument whose own law depends on where a
      // sample lands — the meshing one reads its doors there — has to read the buffer, because the
      // step moves under it while a pass plays and no serialised plan can know it. Added 2026-08-16.
      viewport: { w: cssW, h: cssH, dpr: dpr, bufferW: W, bufferH: H },
      // BOTH WORKS' SEATING ON THIS BUFFER, which only the host can answer. The instrument's own
      // `fit` cover-fits a work into the frame and pulls in by its own framing headroom, and the
      // draw binds the result as the `fitA`/`fitB` uniforms — so the shaders of the unfold and the
      // adrift read the seating BACK out of it (`SZ`, `outOf`) while their scripts could not reach
      // it at all. Both therefore bounded their geometry by the worst seating a cover fit can hand
      // and could only over-hold. Asked for here, on the same buffer, through the same function the
      // draw calls, so the script and the shader work from ONE seating rather than two guesses at
      // it. Added 2026-08-17 on the doors lane's request.
      fitA: instFit(v.inst, rec.src.aw, rec.src.ah),
      fitB: instFit(v.inst, rec.src.bw, rec.src.bh),
      reduced: !!rec.cmd.reduced,
      camera: cam.pose,
      // a pinned run is a bench run: it holds its pose instead of walking to the end door, so a
      // conformance row can photograph one instant twice and compare it to itself
      pinned: pinProgress !== null || !!hold,
      draw: function (pose) { v.drawnThisFrame = true; drawPose(v.inst, pose, rec.src, drew > 0); },
      // A cue that carries the camera by its own device reports its pose here, once a frame. The
      // host applies it and holds its own flight still across that window.
      reportPose: function (p) { if (p) rec.ownPose = p; },
      // WHAT THE INSTRUMENT ITSELF APPLIED, said in the instrument's own numbers. His architecture
      // decision of 2026-08-17 18:00 makes the instrument's run-time reading on the actual buffer
      // the truth of a passage; the composer emits only the request. This is the channel that
      // reading travels back on, and it stands beside `reportPose` because it is the same kind of
      // thing: a fact only the instrument knows, published once at the instant it is known.
      //
      // THE HOST STORES IT AND READS NOTHING IN IT. Whatever record arrives is kept as it came and
      // published on this voice's row of the diagnostic surface; no field is required, none is
      // renamed, and no number is judged here. Every instrument in the tree agrees on one plain
      // shape — `door`, `buffer`, `reads`, `request`, `applied`, `moved`, `unit`, `held`, `whyNo` —
      // but that agreement is the instruments' own, kept in their files, and this host would carry
      // any other shape unchanged.
      //
      // A REFUSAL KEEPS ITS OWN ROAD. `st.fail(st.token, why)` is still how an instrument refuses,
      // and nothing here changes it. What this carries is what WAS applied, including the applied
      // state on the way to a refusal — an instrument reports first and refuses after, so the walk
      // can read the door that could not be held rather than only the sentence about it.
      reportApplied: function (a) { if (a && typeof a === "object") v.applied = a; },
      settle: settle, fail: fail,
    };
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
  // THE COMMAND WAITS FOR ITS OWN INSTRUMENTS, AND FOR NO LONGER THAN THE PREPARE BUDGET. Every
  // instrument a score names is fetched at the address the site's record gives its name, and a
  // command whose instruments are all in hand goes on at once, by the road below, unchanged. A
  // command still waiting on a file waits inside the same budget every other pre-takeover failure
  // is bounded by: the files land and the pass runs, or the budget runs out and the walk's own
  // glide lands the transition. Nothing is on the screen yet either way — the curtain goes up after
  // prepare — so a wait costs the visitor a delayed glide at worst, never a stalled picture.
  var offeredGen = 0;
  var awaiting = null;      // the command held while its files cross the network, and its own gen
  function offer(cmd, hooks) {
    offeredGen = cmd && cmd.gen;
    var waiting = warmFor(cmd);
    if (!waiting) return offerNow(cmd, hooks);
    var budget = clampNum(loadBudgetMs, LOAD_MIN, LOAD_MAX);
    var answered = false;
    // A HELD COMMAND IS NOT AN IDLE HOST, and the diagnostic surface says so: `state` reads
    // «awaiting» for as long as the files are in the air. A surface that read «idle» here would
    // tell a reader the transaction had finished when it had not begun.
    awaiting = { gen: cmd.gen, names: waiting };
    logEvt("instruments-awaited", cmd.gen, waiting + " of the score's instruments");
    function release() { if (awaiting && awaiting.gen === cmd.gen) awaiting = null; }
    var timer = setTimeout(function () {
      if (answered) return;
      answered = true;
      release();
      logEvt("instruments-timeout", cmd.gen, "over " + budget + "ms");
      try { hooks.glide(cmd); } catch (e) {}
    }, budget);
    whenNamedLoaded(cmd, function () {
      if (answered) return;
      answered = true;
      clearTimeout(timer);
      release();
      // A newer declare has superseded this one, and the newer command owns its own landing. Running
      // a glide for the command that was superseded would move the walk twice.
      if (cmd.gen !== offeredGen) { logEvt("offer-superseded", cmd.gen, null); return; }
      if (!offerNow(cmd, hooks)) { try { hooks.glide(cmd); } catch (e) {} }
    });
    return true;
  }

  function offerNow(cmd, hooks) {
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
    var voices = voicesFor(cmd);
    if (!voices) return false;
    var primary = voices[0];
    for (var vi = 0; vi < voices.length; vi++) if (voices[vi].line === 0) primary = voices[vi];
    // §7's grant across the whole stack: the summed declaration at the pass's worst instant against
    // the chosen variant's budget, granted, lowered a rung, or declined.
    var asked = variantOf(cmd);
    var got = grantVariant(voices, asked);
    var variant = got.variant || asked;
    var rec = { cmd: cmd, hooks: hooks, inst: inst, cue: cue, variant: variant, state: "offered",
                voices: voices, primary: primary, grant: got, liveCues: [], drewLastFrame: 0,
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
    logEvt("offer", cmd.gen, instrumentsOf(voices).map(function (x) { return x.name; }).join(" + ")
                             + " at " + variant + (got.lowered ? " (lowered from " + asked + ")" : ""));
    if (!got.variant) {
      // §7's floor: the stack asks for more than even the leanest variant grants, so the plain
      // fallback plays instead of a thin miracle.
      logEvt("resources-declined", cmd.gen, got.why);
      declineCurrent(rec, "resources: " + got.why);
      return true;
    }
    if (got.lowered) logEvt("variant-lowered", cmd.gen, asked + " → " + variant + ": " + got.tried[0].over);
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
          // EVERY instrument the score names gets its programmes built before takeover, so no cue
          // pays for a shader build on the frame its window opens.
          instrumentsOf(voices).forEach(function (x) {
            x.manifest.passes.forEach(function (pass) { programFor(pass); });
          });
        } catch (e) {
          logEvt("stage-threw", cmd.gen, String((e && e.message) || e));
          declineCurrent(rec, "stage threw");
          return;
        }
        // The declaration the census is judged against is the SUM at the pass's worst instant, so a
        // stack is measured against what the stack actually asked for.
        declared = got.sum;
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
      // Every instrument of the stack is started, in draw order. §2.2's promise — the first frame
      // after start is a complete picture of A at its door — is the WHOLE stack's promise, and the
      // frame drawn just below is what keeps it.
      try { instrumentsOf(voices).forEach(function (x) { x.start(cmd.gen); }); }
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

    // EVERY INSTRUMENT THE SCORE NAMES IS PREPARED, each on its own cue and its own grant. One
    // decline refuses the whole command with that instrument's reason: the score names a passage of
    // several voices, and a passage short of a voice is not the one the score wrote.
    function ask() {
      try {
        var answers = voices.map(function (v) {
          return v.inst.prepare({ cmd: cmd, token: cmd.gen, duration: duration, budgetMs: budget,
                                  score: cmd.score || null, cue: v.cue, variant: variant,
                                  sources: rec.src,
                                  grant: cueDeclares(v.cue, v.inst, variant) });
        });
        var thenable = answers.some(function (r) { return r && typeof r.then === "function"; });
        if (thenable) {
          Promise.all(answers.map(function (r) { return Promise.resolve(r); }))
            .then(function (all) { onAnswer(firstNo(all)); },
                  function () { onAnswer({ take: false, why: "prepare rejected" }); });
        } else {
          onAnswer(firstNo(answers));
        }
      } catch (e) {
        if (!answered) { answered = true; clearTimeout(budgetTimer); declineCurrent(rec, "prepare threw"); }
      }
    }
    function firstNo(all) {
      for (var i = 0; i < all.length; i++) {
        var r = all[i];
        if (!r || r.take !== true) {
          return { take: false, why: voices[i].inst.name + ": " + ((r && r.why) || "declined") };
        }
      }
      return { take: true };
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
      instrumentsOf(cur.voices || []).forEach(function (x) {
        try { if (x.cancel) x.cancel(reason); } catch (e) {}
      });
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
      instrumentsOf(cur.voices || []).forEach(function (x) {
        if (x.resize) { try { x.resize(viewport); } catch (e) {} }
      });
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
    if (opts.loadBudgetMs !== undefined) loadBudgetMs = clampNum(opts.loadBudgetMs, LOAD_MIN, LOAD_MAX);
    if (opts.settleSlackMs !== undefined) settleSlackMs = clampNum(opts.settleSlackMs, SLACK_MIN, SLACK_MAX);
    if (opts.clockPin !== undefined) pinClock = opts.clockPin === null ? null : Number(opts.clockPin);
    if (opts.progressPin !== undefined) pinProgress = opts.progressPin === null ? null : Number(opts.progressPin);
    if (opts.fixedScale !== undefined) fixedScale = !!opts.fixedScale;
  }
  function report() {
    var s = times.slice().sort(function (a, b) { return a - b; });
    return {
      state: cur ? cur.state : (awaiting ? "awaiting" : "idle"),
      active: !!cur,
      gen: cur ? cur.cmd.gen : null,
      duration: cur ? cur.duration : null,
      variant: cur ? cur.variant : null,
      prepareBudgetMs: prepareBudgetMs, settleSlackMs: settleSlackMs, loadBudgetMs: loadBudgetMs,
      events: log.slice(),
      instrument: cur ? cur.inst.name : null,
      registered: Object.keys(instruments),
      // THE SITE'S RECORD, on the diagnostic surface: where it was read from, whether it was read
      // or refused, the reason in the host's own words when it was refused, and the names it
      // carries. A refusal is readable here without reading the event log for it.
      record: { src: RECORD_SRC, state: recordState, why: recordWhy,
                names: record ? Object.keys(record) : [] },
      // EVERY INSTRUMENT FILE THIS VISIT HAS ASKED FOR, and nothing it has not: the address and
      // version it was told, where the load stands, and the reason when it was refused. A visit
      // that names one instrument shows one row here, which is the whole point of the shape.
      files: Object.keys(files).map(function (n) {
        return { name: n, src: files[n].src, version: files[n].version,
                 state: files[n].state, why: files[n].why };
      }),
      // THE STACK, as the host actually walks it: draw order, ascending, the cue nearest the eye
      // last. `live` is what the last frame drew, `drew` how many cues that frame laid down, and
      // `handles` each cue's own numbers — a cue outside its window shows the door it is holding at.
      // `applied` is the INSTRUMENT'S own reading of its door on the buffer it drew on, exactly as
      // the instrument published it through `reportApplied`; `handles` beside it is what the HOST
      // resolved and asked for. The two stand side by side on purpose: the plan's intention and the
      // run-time truth, readable against each other on one row.
      stack: cur ? cur.voices.map(function (v) {
        return { id: v.cue ? v.cue.id : null, instrument: v.inst.name, stack: v.stack,
                 line: v.line, live: !!v.live,
                 window: v.cue ? (v.cue.window || null) : null,
                 levels: v.cue ? (v.cue.levels || null) : null,
                 handles: v.lastHandles || null,
                 applied: v.applied || null };
      }) : (lastRun ? lastRun.stack : null),
      live: cur ? cur.liveCues : (lastRun ? lastRun.live : null),
      drew: cur ? cur.drewLastFrame : (lastRun ? lastRun.drew : null),
      // §4.4's tier reckoning, every number it is judged on rather than only its verdict
      budget: cur ? budgetOfScore(cur.cmd.score) : (lastRun ? lastRun.budget : null),
      // §7's grant across the stack: what was asked, what the ladder landed on, and the sum the
      // census below is judged against
      grant: cur ? cur.grant : (lastRun ? lastRun.grant : null),
      budgets: BUDGET,
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
  // THE INSTRUMENT FILES (§7) — each instrument arrives as its own file, and a visit fetches only
  // the ones its own score names
  // ================================================================================================
  // His word of 2026-08-14 08:39: the engine knows no effect name and loads version-pinned opaque
  // effect files, and tlvphotos owns them and their manifests. So this file holds the host alone.
  // No instrument name is written anywhere in it — a conformance row greps the built host for every
  // name that ships today and reds on any of them, which is what makes the boundary checkable
  // rather than merely intended.
  //
  // WHERE THE NAMES COME FROM, AND WHERE THE ADDRESSES DO. Nothing is stamped into this file at
  // bake. A score's cue names its instrument, and that is where every name this host ever handles
  // comes from. The addresses come from the SITE'S OWN SETTINGS RECORD — the same record that
  // already carries the score tables and the score templates — where each instrument has an entry
  // under its own name carrying three things:
  //   · the address its file is served at,
  //   · the version that file must declare,
  //   · the digest its bytes must weigh to.
  // The host reads that record once, at boot, and holds it as data. A name the record does not
  // carry is refused with that reason, `pick` then answers null, `offer` returns false, and the
  // walk's own glide lands the transition.
  //
  // WHY ONE FILE EACH. One file holding every instrument makes a visit pay for the whole farm to
  // see one crossing, and it makes one byte fence answer for a number nobody can act on. One file
  // per instrument makes the fence the honest unit — one instrument, one number — and makes a visit
  // pay for the instruments its own passage uses.
  var RECORD_SRC = "config.json";
  var record = null;           // name → { src, version, digest }, once the record has been read
  var recordState = "asked";   // asked → read | refused
  var recordWhy = null;        // the reason, when refused
  var files = {};              // name → { state, why, src, version, waiting }

  function recordRefuse(why) {
    recordState = "refused";
    recordWhy = why;
    record = {};
    logEvt("record-refused", null, RECORD_SRC + ": " + why);
  }

  function hexOf(buf) {
    var b = new Uint8Array(buf), s = "", i;
    for (i = 0; i < b.length; i++) s += (b[i] < 16 ? "0" : "") + b[i].toString(16);
    return s;
  }

  // WHAT A RECORD MUST SATISFY BEFORE ANY OF IT IS HELD. Every entry is judged, and one bad entry
  // refuses the record whole: a record half-held would leave the host fetching some addresses and
  // silently missing others, and a visitor would meet a stack with a voice absent from it.
  function recordWhyNo(settings) {
    var block = settings && settings.pass;
    var rows = block && block.instruments;
    if (!rows || typeof rows !== "object") return "carries no instrument record";
    var names = Object.keys(rows), out = {}, i, e;
    if (!names.length) return "carries an instrument record with nothing in it";
    for (i = 0; i < names.length; i++) {
      e = rows[names[i]];
      if (!e || typeof e !== "object" || typeof e.src !== "string" || !e.src
          || typeof e.version !== "string" || !e.version
          || !/^[0-9a-f]{64}$/.test(String(e.digest))) {
        return "its entry «" + names[i] + "» carries no address, version and digest";
      }
      out[names[i]] = { src: e.src, version: e.version, digest: String(e.digest) };
    }
    record = out;
    return null;
  }

  // WHETHER THIS PAGE CAN LOAD AN INSTRUMENT AT ALL, asked once and answered in plain words. Three
  // things are needed and each is named: a fetch to bring a file, a script road to run the bytes
  // that arrived, and a digest engine to weigh them before they run. Running unweighed bytes
  // because the scales are missing would make the digest a courtesy, and it is a condition of
  // loading. A page missing any of the three is told so at boot rather than at the first score, and
  // the host joins the walk with that reason on its diagnostic surface.
  function noRoad() {
    if (typeof fetch !== "function") return "this page cannot fetch a file";
    if (typeof document === "undefined" || typeof URL === "undefined"
        || typeof URL.createObjectURL !== "function") {
      return "this page cannot run a file it has fetched";
    }
    var sub = window.crypto && window.crypto.subtle;
    if (!sub || typeof sub.digest !== "function") {
      return "this page offers no digest engine, so a file's bytes cannot be weighed";
    }
    return null;
  }

  function recordLoad(done) {
    var ran = false;
    function finishOnce() { if (!ran) { ran = true; done(); } }
    var road = noRoad();
    if (road) {
      recordRefuse(road + ", so no instrument can be loaded");
      return finishOnce();
    }
    fetch(RECORD_SRC, { credentials: "omit" }).then(function (r) {
      if (!r.ok) throw new Error("the server answered " + r.status);
      return r.json();
    }).then(function (settings) {
      var no = recordWhyNo(settings);
      if (no) throw new Error(no);
      recordState = "read";
      logEvt("record-read", null, RECORD_SRC + ": " + Object.keys(record).length + " instruments");
      finishOnce();
    })["catch"](function (e) {
      recordRefuse(e && e.message ? e.message : String(e));
      finishOnce();
    });
  }

  // ONE FILE RUNS AT A TIME, and the fetches run together. Two files evaluating at once would share
  // the one join point below, and each would be handed whatever the other declared. So the network
  // half is parallel and the evaluation half is a queue of one.
  var evalBusy = false, evalQ = [];
  function evalPump() {
    if (evalBusy || !evalQ.length) return;
    evalBusy = true;
    var job = evalQ.shift();
    // THE WEIGHED BUFFER RUNS, AND NOTHING ELSE DOES. The blob is built from the very buffer that
    // was digested, so what executes is the bytes that passed the check — a second fetch of the same
    // address would leave a gap between weighing and running. It travels as a script element rather
    // than through eval or a Function body: §5's law is that a score is data and no string a command
    // carries is ever executed, and this host's own file is held to it too (a conformance row greps
    // the built host for both and reds on either).
    var url = URL.createObjectURL(new Blob([job.bytes], { type: "text/javascript" }));
    var s = document.createElement("script");
    var joined = null;
    window["__@@NS@@PassInstrument"] = function (p) { joined = p; };
    function clear() {
      URL.revokeObjectURL(url);
      if (s.parentNode) s.parentNode.removeChild(s);
      try { delete window["__@@NS@@PassInstrument"]; }
      catch (e2) { window["__@@NS@@PassInstrument"] = null; }
      evalBusy = false;
      setTimeout(evalPump, 0);
    }
    // A file whose own code throws still fires onload, and it reaches the same landing one line
    // down: it declared nothing, and the host has no instrument. onerror is the road for bytes the
    // page would not run as a script at all.
    s.onload = function () { clear(); job.ok(joined); };
    s.onerror = function () { clear(); job.no(new Error("its bytes would not run as a script")); };
    s.src = url;
    document.head.appendChild(s);
  }

  // WHAT A FILE MUST SATISFY BEFORE ITS INSTRUMENT IS REGISTERED. The version is checked first, then
  // the name, then the manifest. The name check is what keeps an address and the instrument at it
  // from drifting apart: this host asked one address for one name, and a file answering with another
  // instrument is refused rather than registered under a name nobody asked for.
  function fileWhyNo(joined, name, want) {
    if (!joined || typeof joined !== "object") {
      return "handed over nothing an instrument could be read from";
    }
    if (String(joined.version) !== String(want.version)) {
      return "declares version «" + joined.version + "», and this host was told to load «"
           + want.version + "»";
    }
    var inst = joined.instrument;
    if (!inst || !inst.name) return "declares no named instrument";
    if (String(inst.name) !== String(name)) {
      return "declares the instrument «" + inst.name + "», and this host asked that address for «"
           + name + "»";
    }
    var why = manifestWhyNo(inst);
    return why ? "its instrument " + why : null;
  }

  // ONE INSTRUMENT, FETCHED BY THE ADDRESS THE RECORD GIVES ITS NAME. The bytes are weighed before
  // they run, and the bytes that were weighed are the bytes that run: one fetch, one digest over
  // what arrived, and the very same buffer evaluated.
  //
  // Every road ends by calling `done` exactly once with the reason, or with null when the instrument
  // is on the registry. A file that fails to arrive, fails its version, fails its digest, fails its
  // name or fails registration leaves the host without that instrument, and a command naming it
  // finds none: `pick` answers null, `offer` returns false, and the walk's own glide lands the
  // transition. That is the product's own behaviour, which is what a visit with no renderer file at
  // all has always looked like (§2's refusal roads).
  function instLoad(name, done) {
    done = done || function () {};
    if (instruments[name]) return done(null);
    var f = files[name];
    if (f) {
      if (f.state === "asked") { f.waiting.push(done); return; }
      return done(f.why);
    }
    var road = noRoad();
    if (road) {
      files[name] = { state: "refused", src: null, version: null, waiting: [], why: road };
      logEvt("instrument-refused", null, name + ": " + road);
      return done(road);
    }
    var want = record && record[name];
    if (!want) {
      files[name] = { state: "refused", src: null, version: null, waiting: [],
                      why: "the site's record names no instrument by that name" };
      logEvt("instrument-refused", null, name + ": " + files[name].why);
      return done(files[name].why);
    }
    var rec = { state: "asked", why: null, src: want.src, version: want.version, waiting: [done] };
    files[name] = rec;
    function land(why) {
      rec.state = why ? "refused" : "loaded";
      rec.why = why || null;
      logEvt(why ? "instrument-refused" : "instrument-loaded", null,
             name + " (" + want.src + ")" + (why ? ": " + why : " v" + want.version));
      var q = rec.waiting, i;
      rec.waiting = [];
      for (i = 0; i < q.length; i++) q[i](why);
    }
    var sub = window.crypto.subtle;
    var bytes = null;
    fetch(want.src, { credentials: "omit" }).then(function (r) {
      if (!r.ok) throw new Error("the server answered " + r.status);
      return r.arrayBuffer();
    }).then(function (buf) {
      bytes = buf;
      return sub.digest("SHA-256", buf);
    }).then(function (d) {
      var got = hexOf(d);
      if (got !== want.digest) {
        throw new Error("its bytes weigh to " + got.slice(0, 16) + "…, and this host was told "
                      + want.digest.slice(0, 16) + "…");
      }
      return new Promise(function (resolve, reject) {
        evalQ.push({ bytes: bytes, ok: resolve, no: reject });
        evalPump();
      });
    }).then(function (joined) {
      var no = fileWhyNo(joined, name, want);
      if (no) throw new Error(no);
      if (!register(joined.instrument)) throw new Error("its instrument was refused at registration");
      land(null);
    })["catch"](function (e) {
      land(e && e.message ? e.message : String(e));
    });
  }

  // THE NAMES ONE COMMAND CARRIES, each named once. A score naming one instrument on three cues
  // asks for one file.
  function namedBy(cmd) {
    var cues = cuesOf(cmd), out = [], i, id;
    for (i = 0; i < cues.length; i++) {
      id = cues[i] && cues[i].instrument && cues[i].instrument.id;
      if (id && out.indexOf(String(id)) < 0) out.push(String(id));
    }
    return out;
  }

  // WHAT A COMMAND NAMES AND THIS HOST DOES NOT HOLD IS ASKED FOR HERE, and the count of what is
  // still in the air is handed back so the caller knows whether to wait. A name already asked for
  // is not asked for twice, and a name already refused stays refused for the rest of the visit: a
  // file that would not load once is not going to load on the next step, and a walk that retried it
  // every transition would spend the visit fetching the same refusal.
  function warmFor(cmd) {
    var names = namedBy(cmd), waiting = 0, i, id;
    for (i = 0; i < names.length; i++) {
      id = names[i];
      if (instruments[id]) continue;
      if (!files[id]) instLoad(id);
      if (files[id] && files[id].state === "asked") waiting++;
    }
    return waiting;
  }

  // Ring back once every instrument this command names has landed — on the registry, or refused
  // with its reason. Every road through instLoad ends in its callback, so this always rings.
  function whenNamedLoaded(cmd, done) {
    var names = namedBy(cmd), left = names.length, i;
    if (!left) return done();
    function one() { if (!--left) done(); }
    for (i = 0; i < names.length; i++) instLoad(names[i], one);
  }

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

  // THE HOST REACHES THE WALK ONCE THE SITE'S RECORD IS SETTLED — read, or refused with its reason.
  // Joining earlier would leave a window in which the walk can see a host that cannot yet say
  // whether it knows an address for the instrument a score names, and a transition falling inside
  // that window would decline for a reason that stops being true a moment later. No instrument file
  // is fetched here: what a score names is asked for when a score arrives. The walk glides
  // throughout, which is what it does for the whole time this file itself is being fetched.
  recordLoad(function () {
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
      // The hand a conformance row warms an instrument with. A bench draws one pose rather than one
      // command, so no offer passes by to ask for the file the instrument travels in; this asks for
      // it by the same road an offer would, and answers each name with its reason or with null.
      load: function (names, done) {
        var whys = {}, left = names.length;
        if (!left) return done ? done(whys) : undefined;
        names.forEach(function (n) {
          instLoad(String(n), function (why) {
            whys[n] = why || null;
            if (!--left && done) done(whys);
          });
        });
      },
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
      coverageWhyNo: function (cues) { return coverageWhyNo(cues || []); },
      // What each registered instrument declares about its own coverage (§8), so a row reads the
      // declaration the host actually judges a placement on.
      coverageOf: function (id) {
        var inst = instruments[id];
        return inst && inst.manifest ? (inst.manifest.coverage || null) : null;
      },
      // ---- the stack, the levels law, the tier budget and the grant, read as data ---------------
      // The same functions a running transaction calls, with the transaction spared, so a row states
      // a score and reads the number the host actually judges it on.
      stackOrder: function (cues) {
        return stackOrder(cues || []).map(function (r) {
          return { id: r.cue.id, stack: r.stack, line: r.line };
        });
      },
      liveAt: function (cues, seconds) {
        return (cues || []).filter(function (c) { return cueLiveAt(c, seconds); })
                           .map(function (c) { return c.id; });
      },
      budget: function (score) { return budgetOfScore(score); },
      grant: function (score, variant) {
        var vs = voicesFor({ score: score, gen: 0 });
        if (!vs) return null;
        return grantVariant(vs, variant || "standard");
      },
      declares: function (cue, instrumentId, variant) {
        return cueDeclares(cue, instruments[instrumentId], variant || "standard");
      },
      budgets: function () { return BUDGET; },
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
          // The instrument the score's own first cue names, read the way a running transaction
          // reads it. The host writes no instrument name of its own anywhere in this file.
          inst: instruments[(((scoreRec.cues || [])[0] || {}).instrument || {}).id],
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
      // THE FLIGHT BETWEEN THE TWO HANGS, read at stated seconds on stated boxes. The reseat above
      // answers what a moved destination does; this answers what the undisturbed flight IS — where
      // its two ends stand against the two hang poses, whether the middle is held or travelling, and
      // what each axis is doing at each instant. The real anchorPose and the real camStagePose run,
      // composed the way a frame composes them, so a row reads the pose a visitor would be shown.
      hangFlight: function (scoreRec, durationMs, geomA, geomB, times) {
        var rec = {
          cmd: { score: scoreRec, gen: 0, from: { id: "a" }, to: { id: "b" } },
          duration: durationMs, said: {}, placed: false,
          src: { aw: 1000, ah: 1000, bw: 1000, bh: 1000 },
          inst: instruments[(((scoreRec.cues || [])[0] || {}).instrument || {}).id],
          hooks: { hangGeometry: function (id) { return id === "a" ? geomA : geomB; } },
          carry: null, carryFrom: 0, lastSeconds: 0,
        };
        rec.hangEdge = hangEdges(rec);
        readHang(rec);
        var durSec = durationMs / 1000;
        return {
          poseA: rec.hangPoseA, poseB: rec.hangPoseB, edge: rec.hangEdge,
          led: camLed(scoreRec),
          at: times.map(function (t) {
            return camCompose(anchorPose(rec, t),
                              camStagePose(scoreRec, camStageClock(scoreRec, t), durSec, null),
                              null, 0);
          }),
        };
      },
      // THE RECORD ONE VOICE IS HANDED, built by the very function a running frame builds it with,
      // so a row reads what an instrument actually receives rather than a copy of it made here.
      frameState: function (id, src, seconds) {
        var inst = instruments[id];
        if (!inst) return null;
        return frameState({ cmd: { gen: 0 }, src: src, said: {} }, { inst: inst },
                          seconds || 0, 0, {}, { pose: CAM_NEUTRAL }, null, 0);
      },
      camNeutral: function () { return CAM_NEUTRAL; },
      camOff: function (a, b) { return camOff(a, b); },
      camKeys: function () { return CAM_KEYS.slice(); },
      camApplied: function (pose, caps) {
        // The transform string the host would set, without a stage to set it on: the one place the
        // pose becomes pixels, so a row can read WHAT an orbit or a tilt actually does.
        var held = stage;
        stage = { canvas: { style: {} } };
        camApply(pose, caps || camCaps("standard"));
        var t = stage.canvas.style.transform;
        stage = held;
        return t;
      },
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
  });
})();
