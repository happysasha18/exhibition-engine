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
  // UNJUSTIFIED — the longest a transaction may run. Fourteen seconds is the contract's own §2.5
  // bound, written there rather than here, and no measurement of any pair stands behind it.
  var DURATION_MIN = 0, DURATION_MAX = 14000;
  // UNJUSTIFIED — how long the host waits for every instrument of a score to answer `prepare`. Four
  // hundred milliseconds was chosen when this seam was built and nobody has measured it since.
  var PREPARE_MIN = 0, PREPARE_MAX = 400;
  // UNJUSTIFIED — how far past its own duration a transaction may run before the watchdog ends it.
  // Two seconds was chosen beside the budget above and stands on nothing measured.
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
  var foldHeld = null;       // the superseding command, held for as long as the crossing it
                             // supersedes takes to fold up — {cmd, hooks}; see `offerNow`
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
  // UNJUSTIFIED — the rungs the render scale steps through. Five of them, at these five widths,
  // were chosen in lab/gl-carrier.js and carried here unchanged; nobody measured which five.
  var STEPS = [1.0, 0.85, 0.72, 0.60, 0.50];
  // CAPABILITY — a fact about the machine: past two device pixels to the point, a full-screen pass
  // spends memory and fill it never sees back on any display this walk runs on.
  var DPR_CAP = 2;
  // CAPABILITY — arithmetic on the release envelope's own target. One frame at the thirty a second
  // it asks for is 33 ms, which is the bar above which the ladder steps down.
  var P95_DROP = 33;
  // UNJUSTIFIED — the bar below which the ladder climbs back. It was chosen under the drop bar so
  // the two do not chatter against each other, and nothing measured where it should stand.
  var P95_RAISE = 22;
  // UNJUSTIFIED — how many frame gaps a step down and a step up are each read over, and how many
  // the recorder keeps. All three were chosen in lab/gl-carrier.js and nothing measured them.
  var WIN_DROP = 45, WIN_RAISE = 120, KEEP = 240;

  var stage = null;          // {canvas, gl, vao, quad, texA, texB, sceneTex, programs}
  var stageGen = 0;          // bumped by every canvas reveal, read by `stageHideAfterPresent`
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
    // The sharpest copy, which is what every instrument written before the chain existed reads and
    // what its own conformance rows are measured against. An instrument that DECLARES it reads the
    // chain gets the filter that walks it, for the length of its own draw and no longer — see
    // `drawPose` below and §8's `gl.readsChain`.
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
    canvas.style.cssText = "position:fixed;left:0;top:0;width:100%;height:100%;display:block;" +
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
    stage = { canvas: canvas, gl: gl, vao: null, quad: null,
              texA: null, texB: null, sceneTex: null, sceneW: 0, sceneH: 0, programs: {} };
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
    if (!stage) return;
    if (on) stageGen++;
    stage.canvas.style.visibility = on ? "visible" : "hidden";
    if (!on) {
      stage.canvas.style.transform = "";
      stage.canvas.style.left = "0"; stage.canvas.style.top = "0";
      stage.canvas.style.width = "100%"; stage.canvas.style.height = "100%";
    }
  }

  // THE DOOR FRAME NEEDS ITS OWN BROWSER FRAME BEFORE THE CURTAIN DROPS. `cadenceLand` draws the
  // cadence's last frame — the one that stands ON the door — synchronously inside `finish`, and
  // hiding the canvas in that SAME task (as the old code did, right there) means a browser never
  // composites that draw at all: a browser only paints what a task leaves standing at its end, so
  // the door frame is skipped outright and whatever the previous, still-flying rAF tick had drawn
  // is the last thing a visitor actually sees. Waiting one more `requestAnimationFrame` lets that
  // draw be presented before the hide. The generation check guards the one real race this opens:
  // "the held command takes the stage the instant the fold lets go of it" (`finish`, below) can
  // start a NEW pass on this same shared canvas, synchronously, before this callback fires — and
  // that new pass's own reveal must not be undone by a hide meant for the pass it replaced.
  function stageHideAfterPresent(caps) {
    var gen = stageGen;
    requestAnimationFrame(function () {
      if (stageGen !== gen) return;
      stageShow(false);
      camApply(null, caps);
    });
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
      stage.sceneW = stage.sceneH = 0;
      forgetApplied();
    }
  }

  // A READING IS DEFINED ON THE GRID IT WAS TAKEN ON, and the grid moves under a pass: the
  // resolution ladder steps down when frames go long, a window resize or an orientation change
  // arrives mid-flight. The instant the drawing buffer changes, every reading already published
  // stops describing anything that is on screen. A voice whose window has since closed will never
  // report again, so its old reading would otherwise ride to the landing and be published as this
  // passage's applied state on a buffer it was never taken on. It is dropped here instead: a voice
  // that has not reported on the grid now standing carries NOTHING, which is exactly the shape a
  // voice that never reported at all already has. Added 2026-08-17 with the staleness repair.
  function forgetApplied() {
    if (!cur || !cur.voices) return;
    for (var i = 0; i < cur.voices.length; i++) cur.voices[i].applied = null;
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
  function programFor(pass, inst) {
    var P = stage.programs;
    var key = pass.program;
    if (P[key]) return P[key];
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
    P[key] = { prog: p, U: U };
    return P[key];
  }

  // ---- what the host can supply, and the refusal of anything else (§7) ---------------------------
  // `sceneTexture` is the carrier left by the voice immediately below this one. Existing
  // instruments need not name it; instruments that do can treat the preceding construction as
  // matter instead of starting again from either original file. `sceneAvailable` is zero for the
  // ground voice and one thereafter. This is a host capability, never a per-instrument surface.
  var SUPPLY = { textureA: 1, textureB: 1, sceneTexture: 1, sceneAvailable: 1,
                 fitA: 1, fitB: 1, resolution: 1, seconds: 1 };
  // CAPABILITY — a fact about the format: the four uniform types this host knows how to bind. The
  // ones are set membership and not quantities.
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
  // The pose as the uniforms are bound from it: every handle the manifest declares, standing at the
  // value the pose names or, where it names none, at the handle's own declared rest. The pose itself
  // is never touched — an instrument's own `values` reads what it was handed.
  function withRests(pose, inst) {
    var hs = inst && inst.manifest && inst.manifest.handles;
    if (!hs) return pose;
    var out = null, k;
    for (k in hs) {
      if (!Object.prototype.hasOwnProperty.call(hs, k)) continue;
      if (pose[k] !== undefined || hs[k].def === undefined) continue;
      if (!out) {
        out = {};
        for (var j in pose) {
          if (Object.prototype.hasOwnProperty.call(pose, j)) out[j] = pose[j];
        }
      }
      out[k] = hs[k].def;
    }
    return out || pose;
  }

  function bindUniform(gl, loc, u, box) {
    var v;
    if (u.source === "textureA") v = 0;
    else if (u.source === "textureB") v = 1;
    else if (u.source === "sceneTexture") v = 2;
    else if (u.source === "sceneAvailable") v = box.sceneAvailable ? 1 : 0;
    else if (u.source === "fitA") v = box.fitA;
    else if (u.source === "fitB") v = box.fitB;
    else if (u.source === "resolution") v = box.resolution || [W, H];
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
  function ensureSceneTexture() {
    if (!stage) return null;
    var gl = stage.gl;
    if (!stage.sceneTex) stage.sceneTex = makeTex(gl);
    if (stage.sceneW !== W || stage.sceneH !== H) {
      gl.bindTexture(gl.TEXTURE_2D, stage.sceneTex);
      gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, W, H, 0, gl.RGBA, gl.UNSIGNED_BYTE, null);
      stage.sceneW = W; stage.sceneH = H;
    }
    return stage.sceneTex;
  }

  // Snapshot the composed canvas without preserving its drawing buffer and without allocating a
  // second canvas or context. One reusable texture is the whole carrier. A later voice can name it
  // in its manifest; source-over voices that predate the carrier keep composing into the same
  // framebuffer exactly as before.
  function carryScene() {
    var tx = ensureSceneTexture();
    if (!tx) return;
    var gl = stage.gl;
    gl.activeTexture(gl.TEXTURE2);
    gl.bindTexture(gl.TEXTURE_2D, tx);
    gl.copyTexSubImage2D(gl.TEXTURE_2D, 0, 0, 0, 0, 0, W, H);
  }

  function drawPose(inst, pose, src, over, plane) {
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
    var px = plane || { x: 0, y: 0, w: W, h: H, door: 0 };
    var pw = Math.max(1, Math.round(px.w)), ph = Math.max(1, Math.round(px.h));
    gl.viewport(Math.round(px.x), Math.round(px.y), pw, ph);
    gl.enable(gl.SCISSOR_TEST);
    gl.scissor(Math.round(px.x), Math.round(px.y), pw, ph);
    // The work itself is the carrier. At either door it is sampled whole; the instrument's own
    // travel headroom grows in continuously once the plane has left the wall.
    var ownA = inst.fit(src.aw, src.ah, pw, ph), ownB = inst.fit(src.bw, src.bh, pw, ph);
    var q = Math.max(0, Math.min(1, 1 - (Number(px.door) || 0)));
    function seated(f) {
      return [1 + (((f && f[0]) || 1) - 1) * q,
              1 + (((f && f[1]) || 1) - 1) * q,
              ((f && f[2]) || 0) * q, ((f && f[3]) || 0) * q];
    }
    var box = {
      frame: inst.values(pose),
      // A POSE THAT NAMES NO VALUE FOR A DECLARED HANDLE STANDS AT THAT HANDLE'S OWN REST, which is
      // what `def` in a manifest means and what a caller handing a partial pose has always meant to
      // say. Until the entry-door contract landed nothing noticed: every handle a shader read was
      // one every caller filled in. The contract adds `presence` to ten manifests at a rest of ONE —
      // draw exactly as you always did — and a caller that predates it names no value for it, so the
      // uniform went unset. An unset uniform is ZERO in GL, which for this handle means «not in the
      // frame at all», and an instrument drawn from such a pose went blank. Read off the manifest
      // here rather than defended against in ten instruments, because the manifest is where the rest
      // is declared and this is the one place a pose becomes uniforms.
      handles: withRests(pose, inst),
      seconds: pose.t,
      fitA: seated(ownA), fitB: seated(ownB),
      resolution: [pw, ph], sceneAvailable: !!over,
    };
    // WHICH READING OF THE PICTURE THIS INSTRUMENT GETS. The two source textures carry a chain of
    // smaller copies, uploaded with them, so an instrument can read the picture COARSELY — which is
    // how anything belonging to distance is drawn: softness behind a near edge, haze that grows
    // with depth, colour parting at a far edge. Without the chain a coarser reading silently
    // returns the sharpest copy and the frame comes out flat.
    //
    // BUT THE FILTER IS THE INSTRUMENT'S OWN CHOICE, and that is not tidiness. Walking the chain
    // also changes what an instrument reading the picture at no named level gets under minification,
    // and every instrument here is measured frame against frame with a lab module that has no chain
    // at all. Setting the filter for everyone moved two of those readings past their threshold —
    // measured, both suites green before and one row red after. So an instrument declares
    // `gl.readsChain` and gets the walking filter for the length of its own draw; every other
    // instrument reads exactly the copy it always read. The wrap stays clamped throughout: the
    // instruments here carry their own clamp against the travel pushing a sample off the picture,
    // and a repeating wrap would turn that backstop into a wrapped edge.
    var chain = !!(inst.manifest.gl && inst.manifest.gl.readsChain);
    var minf = chain ? gl.LINEAR_MIPMAP_LINEAR : gl.LINEAR;
    inst.manifest.passes.forEach(function (pass) {
      var p = programFor(pass, inst);
      gl.useProgram(p.prog);
      gl.bindVertexArray(stage.vao);
      gl.activeTexture(gl.TEXTURE0);
      gl.bindTexture(gl.TEXTURE_2D, stage.texA);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, minf);
      gl.activeTexture(gl.TEXTURE1);
      gl.bindTexture(gl.TEXTURE_2D, stage.texB);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, minf);
      if (over && stage.sceneTex) {
        gl.activeTexture(gl.TEXTURE2);
        gl.bindTexture(gl.TEXTURE_2D, stage.sceneTex);
      }
      pass.uniforms.forEach(function (u) {
        var loc = p.U[u.name];
        if (loc !== null && loc !== undefined) bindUniform(gl, loc, u, box);
      });
      gl.drawArrays(gl.TRIANGLES, 0, 3);
      census.passesLastFrame++;
    });
    gl.disable(gl.SCISSOR_TEST);
    gl.viewport(0, 0, W, H);
  }

  function instrumentReadsScene(inst) {
    var passes = inst && inst.manifest && inst.manifest.passes || [];
    for (var i = 0; i < passes.length; i++) {
      var us = passes[i].uniforms || [];
      for (var j = 0; j < us.length; j++) if (us[j].source === "sceneTexture") return true;
    }
    return false;
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
    gl.generateMipmap(gl.TEXTURE_2D);
    gl.bindTexture(gl.TEXTURE_2D, stage.texB);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGB, gl.RGB, gl.UNSIGNED_BYTE, src.b);
    gl.generateMipmap(gl.TEXTURE_2D);
    census.uploads++;
    // sized from real dimensions, three bytes a point at RGB/UNSIGNED_BYTE — the size of a thing,
    // which an object count misses entirely (§7). The chain of smaller copies is counted with them:
    // each level is a quarter of the one above it, so the whole chain weighs a third more than the
    // picture alone, and the census says so rather than reporting the level a reader can see.
    census.bytes = Math.round((src.aw * src.ah + src.bw * src.bh) * 3 * 4 / 3);
  }

  // ---- context loss and restoration (§7) ---------------------------------------------------------
  function onContextLost(e) {
    if (e && e.preventDefault) e.preventDefault();
    logEvt("context-lost", cur ? cur.cmd.gen : null, null);
    if (stage) {
      stage.programs = {}; stage.texA = stage.texB = stage.sceneTex = stage.vao = stage.quad = null;
      stage.sceneW = stage.sceneH = 0;
    }
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
  // CAPABILITY — arithmetic. One turn in radians.
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
  // The number a composed float is carrying, or null where this is not one. A node record always
  // names an `op`, a `source` or another `node`; a boxed float names none of the three and answers
  // to `valueOf` while it is still an object in this realm, and carries its number on `v` once it
  // has been through JSON.
  function boxedNumber(o) {
    if (o.op !== undefined || o.source !== undefined || o.node !== undefined) return null;
    if (typeof o.valueOf === "function") {
      var n = o.valueOf();
      if (typeof n === "number" && isFinite(n)) return n;
    }
    return (typeof o.v === "number" && isFinite(o.v)) ? o.v : null;
  }

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
    // A COMPOSED FLOAT ARRIVES BOXED, AND THIS IS THE READER THAT NEVER LEARNED IT.
    // `pass-composer.js` wraps every composed number in its own `Flt` — an object whose `valueOf`
    // returns the number — and the camera reader already unwraps it (`camRead`, with its own note
    // saying the box exists). A node operand is the other place a composed number arrives, and it
    // was never taught: serialised onto a score the prototype does not survive, so what reaches
    // here is a plain `{ v: 0 }` with no `op`, no `source` and no `node`. It fell through to
    // `evalOp`, which answered «the operator «undefined» is declared and drawn by no evaluator
    // yet», the node failed, and the HANDLE FELL BACK TO ITS MANIFEST DEFAULT — silently, for the
    // whole passage, with the score's own number never reaching the picture.
    //
    // It is not a small thing. The composed `mix` template is `mix({v:0}, {v:1}, curve(...))`, so
    // the crossing's own dial fell back to its default on every composed cue that used it — and a
    // dial resting at its entry-door value all the way through tells an instrument it stands at its
    // entry door on every frame. That is what recovered a passage on the phone bench: unfold read
    // `mix` at nought while its own `field` opened the world, and its door proof refused a door it
    // was never actually standing at. The host said so the whole time on its own surface
    // («handle-fallback: mix: the operator «undefined»») and nothing was reading it.
    //
    // Unwrapped HERE and once, the way `camRead` already does it, rather than asking every operator
    // to know the box exists.
    var boxed = boxedNumber(spec);
    if (boxed !== null) return okv(boxed);
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
      case "pointer": {
        // The product owns listeners and gesture arbitration. The renderer reads one normalised
        // snapshot from the command, never the DOM. A node may name x/y, delta, energy or active;
        // the default is energy, the useful scalar accompaniment for a score with one spare voice.
        var p = ctx.pointer;
        if (!p) return nov("the source «pointer» has no normalised host signal on this command");
        var ch = spec.channel || "energy";
        if (ch === "x" || ch === "y" || ch === "dx" || ch === "dy" || ch === "energy") {
          return okv(Number(p[ch]) || 0);
        }
        if (ch === "active") return okv(p.active ? 1 : 0);
        return nov("the source «pointer» names the unknown channel «" + ch + "»");
      }
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
  // CAPABILITY — a fact about the score's own grammar: which two camera places a track names only
  // when it uses them. The ones are set membership and not quantities.
  var CAM_OPTIONAL = { orbit: 1, tilt: 1 };
  // The field of view a turn is seen through where a score names none. Without a projection an orbit
  // is an affine squash rather than a turn, so the host carries its own lens: 0.9 rad is 51.6
  // degrees across the frame's height, which is the ordinary lens a room is photographed with.
  // UNJUSTIFIED — the lens a turn is seen through where a score names none. This file chose 0.9
  // radians because it is the angle a room is ordinarily photographed at; no photograph of this
  // collection was measured for it, and none was consulted.
  var CAM_TURN_FOV = 0.9;
  // The pose rests on the arriving work within this much. The check READS THE POSE rather than the
  // picture, so the number is a computation tolerance and not a matter of taste: a spline evaluated
  // at its own last point returns that point, and only floating point stands between.
  // CAPABILITY — arithmetic. A spline evaluated at its own last point returns that point, so what
  // this bar leaves room for is floating point and nothing else.
  var CAM_REST_TOL = 1e-6;
  // A handoff between two authorities is continuous within this much, measured on the pose across
  // the handoff frame. Normalised pan and radians share one bar.
  // UNJUSTIFIED — how far two camera authorities may stand apart across the instant one hands to
  // the other. This file chose a thousandth; nobody measured how far apart a person can see them
  // stand, and the number is a thousand times the arithmetic bar above it rather than a reading.
  var CAM_HANDOFF_TOL = 1e-3;

  // `pass-composer.js` boxes every composed float in its own `Flt` wrapper (a plain object whose
  // `valueOf` returns the number, so ordinary arithmetic and `Number(...)` already see through it —
  // the same coercion `evalOp`'s "static" case leans on at `Number(spec.value)`). `typeof` does not
  // see through it, though, and this is the one camera reader every axis funnels through, so it
  // unwraps a boxed value here, once, rather than asking every caller to know the box exists.
  function camRead(p, key) {
    var v = key === "panX" ? (p.pan ? p.pan.x : undefined)
          : key === "panY" ? (p.pan ? p.pan.y : undefined)
          : p[key];
    return (v && typeof v === "object" && typeof v.valueOf === "function") ? Number(v) : v;
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
  //
  // UNWRAPPED HERE, LIKE EVERY OTHER WINDOW READER IN THIS FILE (`cueLiveAt`, `windowsMeet`,
  // `metAcross`, the door-progress read in `playFrame`). The composer always writes a cue's window
  // as a pair of `Flt`-tagged numbers (`pass-composer.js:4184`'s `[flt(...), flt(...)]`), whose
  // `valueOf` (`pass-composer.js:66`) makes them read correctly through arithmetic and comparison —
  // which is why the callers that only ever compare or subtract a window edge never needed this —
  // but a bare property access such as `.toFixed()` does not go through `valueOf` at all. The one
  // caller here (`camPoseAt`'s handoff read, `+at.toFixed(4)`) does exactly that, so a real handoff
  // on a real composed score — box-fold's own-camera window closing at the pass's own duration,
  // the fleet's only `cameraAuthority:"own"` cue — threw `TypeError: at.toFixed is not a function`
  // (found 2026-09-01, V2-CONVERGENCE-PLAN's cause G) the instant the running clock read a hair past
  // that edge, which a landing cadence's own rest-check loop (cause F, already traced) routinely
  // does. The throw fired inside `runFrame`, was caught as `frame-threw`, and re-entered `finish`'s
  // own cause-F loop without ever drawing a cadence frame — "no cadence frame was caught."
  function camEdge(score, ownerName, entering) {
    var id = ownerName && ownerName.indexOf("cue:") === 0 ? ownerName.slice(4) : null;
    var cues = (score && score.cues) || [];
    for (var i = 0; i < cues.length; i++) {
      if (cues[i].id === id) {
        var w = cues[i].window || [0, 0];
        return Number(entering ? w[0] : w[1]);
      }
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
  // `over` is the plane's own overscan — how many times the frame the carrier has been grown to so
  // that this very pose still reaches every edge (see `planeReach`). It changes what a PERCENTAGE
  // means and nothing else: a CSS percentage translation resolves against the element's own border
  // box, so a pan written as a plain percentage would travel further the moment the carrier grew,
  // and the pose would stop meaning what it says. Divided by the overscan, the pan moves the picture
  // by the same share of the FRAME it always moved it by, whatever size the carrier under it is. A
  // carrier at its ordinary size passes `over` of 1 and the transform is written exactly as before.
  function camApply(pose, caps, over) {
    if (!stage) return;
    if (!pose) { stage.canvas.style.transform = ""; return; }
    var span = (typeof over === "number" && over > 0) ? over : 1;
    var s = Math.exp(caps.logScale ? pose.logScale : 0);
    var deg = 180 / Math.PI;
    // Pitch and yaw need the same lens orbit and tilt already fall back to: without a perspective
    // projection a rotateX/rotateY is a near-invisible cosine squash rather than a real 3D tilt (a
    // 6° yaw is a ~0.5% squash), and no camera track template ever names `fov` explicitly.
    var turn = (caps.orbit && pose.orbit) || (caps.tilt && pose.tilt)
            || (caps.pitch && pose.pitch) || (caps.yaw && pose.yaw);
    var fov = (caps.fov && typeof pose.fov === "number" && pose.fov > 0) ? pose.fov
            : (turn ? CAM_TURN_FOV : 0);
    var t = "";
    if (fov) t += "perspective(" + (0.5 * Math.max(cssH, 1) / Math.tan(fov / 2)).toFixed(3) + "px) ";
    // THE PAN IS THE HINGE OF THE CHAIN, and which side of it an axis stands on is the whole
    // difference between the two kinds of turn. A list is applied right to left, so an axis written
    // to the RIGHT of the pan acts BEFORE it and one written to the LEFT acts after. The camera's
    // own three — pitch, yaw and roll — stand to the left: the subject is carried to its place
    // first and the camera then turns where it stands, so the scene swings across the frame. Orbit
    // and tilt stand to the right: the scene turns about the frame's own centre and the pan then
    // carries the turned subject to its place, so the point of view travels around the work while
    // the work holds its framing. Written on one side, as it was until now, a yaw is an orbit under
    // another name and the orbit axis says nothing the yaw did not already say.
    if (caps.pitch && pose.pitch) t += "rotateX(" + (pose.pitch * deg).toFixed(4) + "deg) ";
    if (caps.yaw && pose.yaw) t += "rotateY(" + (pose.yaw * deg).toFixed(4) + "deg) ";
    if (caps.roll && pose.roll) t += "rotate(" + (pose.roll * deg).toFixed(4) + "deg) ";
    t += "translate(" + (caps.panX ? pose.panX * 100 / span : 0).toFixed(4) + "%,"
       + (caps.panY ? pose.panY * 100 / span : 0).toFixed(4) + "%) ";
    if (caps.orbit && pose.orbit) t += "rotateY(" + (pose.orbit * deg).toFixed(4) + "deg) ";
    if (caps.tilt && pose.tilt) t += "rotateX(" + (pose.tilt * deg).toFixed(4) + "deg) ";
    t += "scale(" + s.toFixed(6) + ")";
    stage.canvas.style.transformOrigin = "50% 50%";
    stage.canvas.style.transform = t;
  }

  // ================================================================================================
  // THE PLANE'S REACH — a pose that would bare an edge is drawn on a carrier large enough to cover it
  // ================================================================================================
  // HIS WORD, 2026-08-25: it is beautiful when the camera stands at an angle, but that does not
  // always cover the screen. It does not, and nothing checked it. The coverage law already in this
  // file answers a different question — whether a voice drawing over another lets what is beneath it
  // show through where it draws nothing. This is the other case, and it is geometric: the drawn plane
  // itself, carried by a pose that pans or dollies out or turns, stops short of the frame's own
  // edges, and whatever lies under the canvas shows in the gap.
  //
  // THE CARRIER IS GROWN, THE POSE IS NEVER REFUSED. The charter's laws degrade a crossing and never
  // refuse one, and its second shelf asks for the camera's excursion — so the repair is on the
  // carrier's own size and not on the pose. The plane is enlarged about the frame's centre until the
  // very pose that would have bared an edge lands inside it. The enlargement is UNIFORM, so the
  // carrier keeps the frame's aspect and therefore the drawing buffer's, and the instrument's cover
  // fit is seated exactly as it was — the picture is simply drawn larger and the frame crops it a
  // little tighter. What it costs is resolution, in the ratio of the enlargement, which is the same
  // currency the render ladder already spends and is spent here only on the poses that need it.
  //
  // WHY IT IS COMPUTED RATHER THAN TABULATED. The reach is a property of THE POSE, and the pose is
  // composed at run time from the two photographs in front of it. There is no pose list to look it
  // up in, and a single number covering every pose would over-grow every ordinary one.
  //
  // The chain below is the very chain `camApply` writes, as a matrix. Written twice it could drift,
  // so `camApply` is the reader of record for the string and this is the reader of record for the
  // geometry; the conformance rows hold the two against the browser's own rendering of the string.
  function m4mul(a, b) {
    var o = new Array(16), i, j, k, s;
    for (i = 0; i < 4; i++) {
      for (j = 0; j < 4; j++) {
        s = 0;
        for (k = 0; k < 4; k++) s += a[i * 4 + k] * b[k * 4 + j];
        o[i * 4 + j] = s;
      }
    }
    return o;
  }
  function m4id() { return [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]; }
  function m4rotX(r) {
    var c = Math.cos(r), s = Math.sin(r);
    return [1, 0, 0, 0, 0, c, -s, 0, 0, s, c, 0, 0, 0, 0, 1];
  }
  function m4rotY(r) {
    var c = Math.cos(r), s = Math.sin(r);
    return [c, 0, s, 0, 0, 1, 0, 0, -s, 0, c, 0, 0, 0, 0, 1];
  }
  function m4rotZ(r) {
    var c = Math.cos(r), s = Math.sin(r);
    return [c, -s, 0, 0, s, c, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1];
  }
  function m4trans(x, y) { return [1, 0, 0, x, 0, 1, 0, y, 0, 0, 1, 0, 0, 0, 0, 1]; }
  function m4scale(s) { return [s, 0, 0, 0, 0, s, 0, 0, 0, 0, s, 0, 0, 0, 0, 1]; }
  // CSS `perspective(P)`: the one entry that makes the map projective rather than affine.
  function m4persp(p) {
    var m = m4id();
    if (p > 0) m[14] = -1 / p;
    return m;
  }

  // The matrix of one pose on a carrier of the given CSS size. `panBox` is the box a percentage
  // translation resolves against — the carrier's own UNENLARGED size, which is what keeps a pan
  // meaning the same share of the frame however far the carrier has been grown.
  function camMatrix(pose, caps, panBox) {
    var s = Math.exp(caps.logScale ? pose.logScale : 0);
    var turn = (caps.orbit && pose.orbit) || (caps.tilt && pose.tilt)
            || (caps.pitch && pose.pitch) || (caps.yaw && pose.yaw);
    var fov = (caps.fov && typeof pose.fov === "number" && pose.fov > 0) ? pose.fov
            : (turn ? CAM_TURN_FOV : 0);
    var m = fov ? m4persp(0.5 * Math.max(cssH, 1) / Math.tan(fov / 2)) : m4id();
    if (caps.pitch && pose.pitch) m = m4mul(m, m4rotX(pose.pitch));
    if (caps.yaw && pose.yaw) m = m4mul(m, m4rotY(pose.yaw));
    if (caps.roll && pose.roll) m = m4mul(m, m4rotZ(pose.roll));
    m = m4mul(m, m4trans(caps.panX ? pose.panX * panBox.w : 0,
                         caps.panY ? pose.panY * panBox.h : 0));
    if (caps.orbit && pose.orbit) m = m4mul(m, m4rotY(pose.orbit));
    if (caps.tilt && pose.tilt) m = m4mul(m, m4rotX(pose.tilt));
    return m4mul(m, m4scale(s));
  }

  // Where the carrier's four corners land, in frame coordinates measured from the frame's centre.
  // A corner behind the vanishing plane (w at or below zero) is reported as null: the quad has
  // turned inside out there, and no enlargement of a plane seen edge-on ever covers anything.
  function camQuad(pose, caps, halfW, halfH, panBox) {
    var m = camMatrix(pose, caps, panBox), out = [], i;
    var corners = [[-halfW, -halfH], [halfW, -halfH], [halfW, halfH], [-halfW, halfH]];
    for (i = 0; i < 4; i++) {
      var x = corners[i][0], y = corners[i][1];
      var w = m[12] * x + m[13] * y + m[15];
      if (!(w > 1e-6)) return null;
      out.push([(m[0] * x + m[1] * y + m[3]) / w, (m[4] * x + m[5] * y + m[7]) / w]);
    }
    return out;
  }

  // Is every corner of the frame inside the quad? The quad is walked as a loop and a point is inside
  // when it lies on the same side of all four edges. The frame's own four corners are the only points
  // that need asking about: both shapes are convex, so a convex quad containing the four corners of a
  // rectangle contains the whole rectangle.
  function quadCovers(q, halfW, halfH) {
    if (!q) return false;
    var pts = [[-halfW, -halfH], [halfW, -halfH], [halfW, halfH], [-halfW, halfH]];
    var sign = 0, i, j, k;
    for (i = 0; i < 4; i++) {
      var a = q[i], b = q[(i + 1) % 4];
      var ex = b[0] - a[0], ey = b[1] - a[1];
      for (j = 0; j < 4; j++) {
        var cross = ex * (pts[j][1] - a[1]) - ey * (pts[j][0] - a[0]);
        k = cross > 1e-9 ? 1 : (cross < -1e-9 ? -1 : 0);
        if (k === 0) continue;
        if (sign === 0) sign = k;
        else if (k !== sign) return false;
      }
    }
    return true;
  }

  // HOW WIDE THE CARRIER MAY GROW, AND THE NUMBER IS NOT CHOSEN. Growing the carrier spends
  // resolution and nothing else: the drawing buffer is sized to the frame, so a carrier of k frames
  // spreads those same points over k frames' worth of screen and the picture stands at one part in k
  // of the resolution it would otherwise have had. The engine has already declared how much of that
  // it is willing to spend — the render ladder's own last rung, `STEPS[STEPS.length - 1]`, is the
  // resolution it will draw a passage at on a device that needs it. So the carrier may grow until
  // the picture stands at exactly that same floor and no further: one over the ladder's last rung.
  // The overscan therefore spends the same currency, out of the same purse, down to the same floor
  // the file already set for itself.
  function reachCeiling() { return 1 / STEPS[STEPS.length - 1]; }

  // HOW FAR THE CARRIER HAS TO REACH FOR THIS POSE, as a multiple of the frame, and HOW MUCH OF THE
  // POSE THE CARRIER CAN THEN CARRY.
  //
  // One and whole is the ordinary answer: a pose at its neutral needs no enlargement and pays
  // nothing, and most of a flight is spent near it. Where a pose does need room, the least room that
  // answers it is found — and where the ceiling above cannot answer it even at its widest, the POSE
  // IS HELD CLOSER IN rather than the frame being left bare. Held, never refused: the excursion
  // still plays, on the same axes, in the same direction, through the same arc — it simply travels
  // as far as the frame can be kept whole and no further. That is the charter's own degrade, and it
  // is what shelf 2's excursion asks for on a device that cannot carry all of it.
  //
  // BOTH ANSWERS ARE FOUND BY HALVING, NOT BY STEPPING. A carrier quantised to rungs would step
  // between one frame and the next, and a step in the carrier is a step in the picture — the very
  // seam the crossing charter's own seam check reds on. Halving converges to a width finer than a
  // point of the screen, so what the eye sees moves as smoothly as the pose that drives it.
  // CAPABILITY — how finely the carrier's own width is settled, and it is a fact about the screen
  // rather than about any pair. The search runs on an interval no wider than the ceiling itself, a
  // little over one frame, and each halving cuts that in two: twenty-four of them settle the width
  // to about one part in seventeen million of a frame, which is thousands of times finer than the
  // point the width is finally rounded onto. Fewer would leave a carrier that steps between two
  // frames, and a step in the carrier is a step in the picture; more would settle a difference no
  // screen can carry. No picture, no walk and no session has anything to say about it.
  var REACH_HALVINGS = 24;
  function coversAt(pose, caps, panBox, k) {
    return quadCovers(camQuad(pose, caps, cssW * k / 2, cssH * k / 2, panBox), cssW / 2, cssH / 2);
  }
  function poseHeld(pose, t) {
    if (t >= 1) return pose;
    var out = {}, i;
    for (i = 0; i < CAM_KEYS.length; i++) {
      var k = CAM_KEYS[i];
      out[k] = (k === "fov") ? pose[k]
             : (typeof pose[k] === "number" ? pose[k] * t : pose[k]);
    }
    return out;
  }
  function camFit(pose, caps, panBox) {
    var top = reachCeiling(), i, lo, hi, mid;
    if (!pose || coversAt(pose, caps, panBox, 1)) {
      return { over: 1, hold: 1, pose: pose };
    }
    if (coversAt(pose, caps, panBox, top)) {
      // The least carrier that answers this pose, between the frame itself and the ceiling.
      lo = 1; hi = top;
      for (i = 0; i < REACH_HALVINGS; i++) {
        mid = (lo + hi) / 2;
        if (coversAt(pose, caps, panBox, mid)) hi = mid; else lo = mid;
      }
      return { over: hi, hold: 1, pose: pose };
    }
    // The ceiling cannot answer it: hold the pose in until the widest carrier can.
    lo = 0; hi = 1;
    for (i = 0; i < REACH_HALVINGS; i++) {
      mid = (lo + hi) / 2;
      if (coversAt(poseHeld(pose, mid), caps, panBox, top)) lo = mid; else hi = mid;
    }
    return { over: top, hold: lo, pose: poseHeld(pose, lo) };
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
  function containCss(iw, ih) {
    var a = Math.max(1, Number(iw)) / Math.max(1, Number(ih));
    var w = cssW, h = w / a;
    if (h > cssH) { h = cssH; w = h * a; }
    return { x: (cssW - w) / 2, y: (cssH - h) / 2, w: w, h: h };
  }

  function hangPoseOf(geom, inst, iw, ih) {
    if (!geom || !geom.w || !geom.h || cssW <= 0 || cssH <= 0) return null;
    // The camera seats the WHOLE source plane, independent of whichever instrument happens to sing
    // first. Deriving this from an instrument's cover crop made the work's centre leave the wall
    // while its edges stayed behind. Both rectangles here contain the same whole photograph.
    var full = containCss(iw, ih);
    var k = geom.w / full.w;
    if (!isFinite(k) || k <= 0) return null;
    return {
      panX: (geom.x + geom.w / 2 - cssW / 2) / cssW,
      panY: (geom.y + geom.h / 2 - cssH / 2) / cssH,
      logScale: Math.log(k), pitch: 0, yaw: 0, roll: 0, fov: null,
      // What the two readings of one scale disagree by. Both roads keep the work's aspect, so this
      // stands at zero; it is written down rather than asserted, because a layout that began to crop
      // would show up here as a number instead of as a soft edge nobody can name.
      aspectOff: +Math.abs(geom.h / full.h - k).toFixed(9),
    };
  }

  // THE FLIGHT'S TWO ENDS ARE THE TWO HANGS. A passage leaves the departing work exactly where it
  // hangs, rises to the whole frame for the crossing itself, and comes back down onto the arriving
  // work's own box. The rise and the fall are seconds a score may name; with none named they take a
  // share of the pass at either end, and the whole middle stands at the neutral pose.
  // UNJUSTIFIED — the share of a passage the rise and the fall each take where the score names no
  // seconds for them. This file chose 0.18 and nothing measured it.
  var HANG_SHARE = 0.18;
  function hangEdges(rec) {
    var cam = (rec.cmd && rec.cmd.score && rec.cmd.score.camera) || {}, h = cam.hang || {};
    var dur = rec.duration / 1000, half = dur / 2;
    var rise = Number(h.rise), fall = Number(h.fall);
    if (!isFinite(rise) || rise < 0) rise = dur * HANG_SHARE;
    if (!isFinite(fall) || fall < 0) fall = dur * HANG_SHARE;
    return { rise: Math.min(rise, half), fall: Math.min(fall, half), dur: dur };
  }

  function doorEase(u) { return CURVES.smooth(u <= 0 ? 0 : u >= 1 ? 1 : u); }

  // One geometric plane carries the picture for the entire passage; it is never replaced by a DOM
  // clone. THE PLANE IS THE CAMERA'S HANG ANCHOR MADE PHYSICAL. `anchorPose` above travels the
  // departing hang → the neutral → the arriving hang, and `camPoseAt` deliberately leaves that
  // anchor out of the transform it applies (`art`) because this box carries it instead. So the
  // plane's two ends are the two measured DOM rectangles and its middle is the NEUTRAL — the frame
  // itself, one drawing-buffer point to one frame point. Nothing else is a legal middle: the
  // instrument seats the work into the buffer on its own (see `seated` in `drawPose`, which cancels
  // that seating only as `door` reaches 1), so a box that is not the frame would seat the same work
  // a second time in CSS and hand the visitor a cover fit of a cover fit.
  //
  // A DOOR IS A DOOR ONLY WHERE A RECTANGLE WAS MEASURED. `hangGeometry` answers null for a work
  // the layout never hung — a host driven from a bench, a walk whose adapter found no image, a
  // passage that opens on nothing. There is then no wall to leave and no wall to land on: the plane
  // stands at the frame for the whole pass and `door` stays zero, so the instrument seats the work
  // exactly as it did before any plane existed. Reporting a door there while substituting some
  // other rectangle for the missing hang is what made the door rows read a work seated twice.
  // Coordinates are drawing-buffer coordinates because gl.viewport's origin is below.
  // THE CARRIER REACHES AS FAR AS THE POSE ON IT NEEDS, and only where the passage claims the whole
  // frame. `art` is the score's own camera track — the very pose `camApply` puts on this canvas, the
  // hang anchor excluded because this box carries that instead. Where `door` stands above zero the
  // passage is on its way out of one wall or onto another and the walk around it is MEANT to be
  // seen: the carrier is the work's own rectangle there and enlarging it would paint over the room.
  // Where `door` is zero the passage owns the frame outright, and owning it means reaching every
  // pixel of it.
  function planeAt(rec, seconds, art) {
    // The neutral: the whole frame, which is what the camera's own neutral pose means.
    var full = { x: 0, y: 0, w: cssW, h: cssH };
    var e = rec.hangEdge || hangEdges(rec), door = 0, box = full, radius = 0;
    function lerpBox(a, b, q) {
      return { x: a.x + (b.x - a.x) * q, y: a.y + (b.y - a.y) * q,
               w: a.w + (b.w - a.w) * q, h: a.h + (b.h - a.h) * q };
    }
    if (rec.hangA && e.rise > 0 && seconds <= e.rise) {
      var qo = doorEase(seconds / e.rise);
      box = lerpBox(rec.hangA, full, qo); door = 1 - qo;
      radius = (Number(rec.hangA.radius) || 0) * (1 - qo);
    } else if (rec.hangB && e.fall > 0 && seconds >= e.dur - e.fall) {
      var qi = doorEase((seconds - (e.dur - e.fall)) / e.fall);
      box = lerpBox(full, rec.hangB, qi); door = qi;
      radius = (Number(rec.hangB.radius) || 0) * qi;
    }
    var fit = (door === 0 && art) ? camFit(art, rec.caps, box) : { over: 1, hold: 1, pose: art };
    if (fit.over !== 1) {
      box = { x: box.x - box.w * (fit.over - 1) / 2, y: box.y - box.h * (fit.over - 1) / 2,
              w: box.w * fit.over, h: box.h * fit.over };
    }
    return { x: 0, y: 0, w: W, h: H, door: door, over: fit.over, hold: fit.hold, art: fit.pose,
             cssX: box.x, cssY: box.y, cssW: box.w, cssH: box.h, cssRadius: radius };
  }

  function planeApply(plane) {
    if (!stage || !plane) return;
    var c = stage.canvas;
    c.style.left = plane.cssX.toFixed(3) + "px";
    c.style.top = plane.cssY.toFixed(3) + "px";
    c.style.width = plane.cssW.toFixed(3) + "px";
    c.style.height = plane.cssH.toFixed(3) + "px";
    c.style.borderRadius = Math.max(0, Number(plane.cssRadius) || 0).toFixed(3) + "px";
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
    // AN OWN CUE HOLDS THE SAME SLOT THE SCORE'S TRACK HOLDS, and it is the slot ON TOP of the
    // anchor, never instead of it. What an instrument reports through `reportPose` is a CSS
    // transform on the carrier — the very thing `camApply` writes and `art` below carries — and the
    // carrier is already standing on the work's own hang box, because `planeApply` puts it there
    // physically. So the residual is the own pose and the pose AS APPLIED is anchor + residual +
    // carry, composed exactly as the stage road composes its track.
    //
    // REPLACING THE STAGE POSE OUTRIGHT IS WHAT MADE AN OWN CUE FAIL TO REST (2026-09-01,
    // V2-CONVERGENCE-PLAN's cause F). `rec.lastPose` is what `finish` and `settle` judge against the
    // arriving work's own hang pose; with the anchor replaced rather than composed, an own cue's
    // reading was its bare residual — near zero at a door — while the bar was the full hang pose off
    // the frame's centre. The gate therefore fired at every real door, on the fleet's one
    // `cameraAuthority:"own"` instrument and on no other, and its remedy laid the hang on a canvas
    // the plane had already hung. Composed here, an own cue at rest reads what a stage cue at rest
    // reads: the anchor, and nothing on top of it.
    //
    // A CUE THAT STOPS REPORTING STILL HANDS AUTHORITY BACK AT ITS LAST POSE — `rec.ownPose` is
    // sticky (`reportPose` only ever writes it), so the fallback below is reached only by a cue that
    // has not reported at all, and there the residual the stage was holding an instant ago is the
    // continuous one to hold. That is the same fallback `art` already used.
    var ownArt = rec.ownPose || track;
    var pose = stagePose;
    if (owner !== "stage") pose = camCompose(anchor, ownArt, rec.carry, carryWeight(rec, tSec));
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
        // compared on the same footing rather than one of them reading a bare track. BOTH SIDES
        // CARRY THE ANCHOR, or the reading is the anchor rather than the discontinuity: until
        // 2026-09-01 the stage side was composed here and the own side was the instrument's bare
        // residual, so at a window edge standing at a real hang the row read the whole hang pose as
        // a jump. Box-fold's own window closes at the pass's own last second, where the anchor IS
        // the arriving hang — which is why the fleet's one own-camera instrument was the only one
        // whose handoff row moved. The residual is what the two authorities can actually disagree
        // about, and composing both onto one anchor is what leaves only that in the number.
        var anchorAt = anchorPose(rec, at), carryAt = carryWeight(rec, at);
        var trackAt = camStagePose(score, camStageClock(score, at), durationSec, null);
        var there = camCompose(anchorAt, trackAt, rec.carry, carryAt);
        var here = camCompose(anchorAt, rec.ownPose || trackAt, rec.carry, carryAt);
        var off = camOff(there, here);
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
    // `art` excludes the hang anchor. The source plane itself now travels through the exact measured
    // DOM rectangles; applying the anchor as a CSS transform as well would move it twice. The
    // score's witness-camera accompaniment remains continuous on top of that physical carrier.
    return { owner: owner, pose: pose, stage: stagePose,
             art: owner === "stage" ? track : ownArt };
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

  // A COPY OF THE COMMAND WITH A REPLACED SCORE. Neither the funnel's last-resort cast nor the
  // stack-shed below is allowed to mutate the command a caller still holds a reference to (the walk,
  // the diagnostic surface, a superseding declare all read the same object) — so a rescue always
  // works on a fresh object carrying the same `gen`, `from`, `to` and every other field untouched,
  // with only `score` replaced.
  function mergeScore(cmd, scorePatch) {
    var s = (cmd && cmd.score) || {}, ns = {}, nc = {}, k;
    for (k in s) if (Object.prototype.hasOwnProperty.call(s, k)) ns[k] = s[k];
    for (k in scorePatch) if (Object.prototype.hasOwnProperty.call(scorePatch, k)) ns[k] = scorePatch[k];
    for (k in cmd) if (Object.prototype.hasOwnProperty.call(cmd, k)) nc[k] = cmd[k];
    nc.score = ns;
    return nc;
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
  // UNJUSTIFIED — the most of a passage that may carry no cue at all. The crossing charter's
  // seventeenth shelf sets the third, and the charter says of it in as many words that the tier
  // numbers beside it were written by an agent in `ae2b5da` on 2026-08-08 at 15:59 and that nobody
  // measured them. It is carried here rather than chosen here, and it stands on nothing.
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
  // THE LOWEST VOICE MAY NOT STAND ABSENT AT ITS OWN DOOR. The entry-door contract gives an
  // instrument standing over another a state in which it draws nothing — the reserved `presence`
  // handle at zero — so a voice can join a running picture without replacing it. The lowest voice of
  // a score has no such licence: it is drawn onto the cleared buffer, nothing stands beneath it, and
  // a door at which it draws nothing is a door at which the visitor sees the page. Only the host can
  // say which cue is lowest, so the law is stated here rather than inside any instrument. It is
  // checked for a score of ONE cue as well as for a stack: a lone voice is its own lowest, and the
  // coverage law's own exemption for a one-cue score does not extend to this.
  var PRESENCE_HANDLE = "presence";
  function presenceWhyNo(cues) {
    if (!cues || !cues.length) return null;
    var rows = stackOrder(cues), low = rows[0] && rows[0].cue;
    var doors = (low && low.doors) || {}, side;
    for (side in doors) {
      if (!Object.prototype.hasOwnProperty.call(doors, side)) continue;
      var d = doors[side];
      if (d && d.handle === PRESENCE_HANDLE && Number(d.value) === 0) {
        return "cue «" + low.id + "» stands lowest in the stack and names its " + side
             + " door at no presence at all — nothing stands beneath the lowest voice, so a door it "
             + "draws nothing at is a door the visitor sees the page through";
      }
    }
    return null;
  }

  function scoreWhyNo(cmd) {
    var s = cmd && cmd.score;
    if (!s) return null;
    var cues = s.cues || [], i, j;
    var low = presenceWhyNo(cues);
    if (low) return low;
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
    // THE TIER BUDGET IS RECKONED AND RECORDED, AND IT REFUSES NOTHING (2026-08-18, his word of
    // 09:51). Shelf 17's budget is a law about how a passage is COMPOSED, and the composer answers
    // to it: it counts letters and miracles as it builds, gives up moves it cannot spend, and
    // DECLARES the tier its voices actually realised. A second reckoning here could only disagree
    // with the first, and its disagreement cost the visitor the whole crossing — a well-formed
    // score, every instrument ready, refused for a count. The reckoning stands on the diagnostic
    // surface where a person can read it; what a frame cannot recover from is what this function
    // still refuses, and a voice count is not that.
    return null;
  }

  // A SCORE'S REFUSAL IS A PROPERTY OF THE STACK, NOT OF ANY ONE VOICE (2026-08-24). All five
  // reasons `scoreWhyNo` names — a cycle inside a cue, two cues racing for the camera, two cues
  // naming one instrument across a shared instant, and the two placements of the coverage law — are
  // read off the STACK the score declares, and every one of them can be answered by playing a
  // smaller stack instead of playing none at all. This walks the same ladder `grantVariant` already
  // walks for a device that cannot carry the full stack: stand the topmost voice down and ask
  // `scoreWhyNo` again, repeating until it answers null or nothing is left to shed. A refusal that
  // survives down to one cue is a defect INSIDE that cue's own node table (its own graph cycles on
  // itself), which is not a stack property at all and is left for the funnel's last-resort cast.
  function scoreShed(cmd) {
    var s = cmd && cmd.score, cues = s && s.cues;
    if (!cues || cues.length < 2) return null;
    cues = cues.slice();
    while (cues.length > 1) {
      var order = stackOrder(cues);
      var topmost = order[order.length - 1].cue;
      cues = cues.filter(function (c) { return c !== topmost; });
      var trial = mergeScore(cmd, { cues: cues });
      if (!scoreWhyNo(trial)) return trial;
    }
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
  // score has always meant. AN UNKNOWN INSTRUMENT SHEDS ITS OWN VOICE RATHER THAN REFUSING THE WHOLE
  // SCORE (2026-08-24): the registry not carrying one name is a property of that one cue, exactly
  // like a device that cannot carry a voice's cost, and the stack plays short a voice instead of not
  // at all. Only when EVERY cue's instrument is unknown — nothing left to shed down to — does this
  // give the command up, which is the funnel's own cue to cast the last resort.
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
      if (!instruments[id]) { logEvt("no-instrument", cmd.gen, String(id)); continue; }
      out.push({ cue: rows[i].cue, inst: instruments[id], said: {}, driverState: {},
                 lastHandles: null, applied: null,
                 live: false, stack: rows[i].stack, line: rows[i].line });
    }
    if (!out.length) return null;
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
  //
  // THE RUNG COMES FROM THE DEVICE; A NAMED SETTING OUTRANKS IT (charter shelf 19). The nineteenth
  // shelf puts the order this way round: the device is read first and the plan is DEGRADED to what
  // it can carry, never refused for not being able to carry more. This function used to read the
  // `qualityTier` setting and nothing else, so the rung a visitor got was whatever a session, a site
  // record or the register's own default happened to say, and the machine in front of the person was
  // never asked.
  //
  // THE READING IS THE ONE ALREADY BEING TAKEN, not a second one. `stepIx` is where the render-scale
  // ladder stands — walked down by `decideScale` on a p95 of the last 45 frame gaps against 33 ms,
  // and back up on 120 gaps under 22 ms — so it is exactly «how many rungs this device's own frame
  // times have already cost it». The tier walks down one rung for each rung the scale ladder has
  // spent, and stops at the tier ladder's own floor. Nothing here can walk a tier UP: a fast device
  // gets what was asked for and no more, because a machine being quick is not a request for a
  // richer plan.
  //
  // WHAT «NAMED» MEANS, exactly. The bundle's own settings ladder resolves each name on the session,
  // the score, the site record and the register's default, in that order, and says on the frozen
  // command which rung won (`source`). Any rung but `default` is a word somebody said, and a word
  // outranks the measurement. `default` is nobody having said anything, and it yields.
  function variantOf(cmd) {
    var t = cmd && cmd.params && cmd.params.qualityTier;
    var name = t ? t.base : "standard";
    if (name !== "rich" && name !== "lean") name = "standard";
    if (t && t.source && t.source !== "default") return name;
    var ix = VARIANTS.indexOf(name);
    if (ix < 0) ix = VARIANTS.indexOf("standard");
    return VARIANTS[Math.max(0, ix - stepIx)];
  }

  // THE LADDER'S MIDDLE STEP: the accompaniment at 30 while the miracle keeps 60 (charter shelf 19).
  // The shelf names three things a weak device is given in order — a lighter plan, then accompaniment
  // voices at half rate while the miracle holds full rate, then resolution easing — and this file
  // already carries ONE reading those three hang off: the render-scale ladder's rungs. So the order
  // is read off the rungs rather than off three separately chosen numbers:
  //
  //   rung 0 (scale 1.00)  nothing is given up.
  //   rung 1 (scale 0.85)  the plan walks down a tier — `variantOf` above, first thing given up.
  //   rung 2 (scale 0.72)  the accompaniment halves — this, second thing given up; by this rung the
  //                        tier ladder has already reached its own floor and has nothing left.
  //   rungs 3-4            resolution alone keeps easing, which is what `decideScale` already does.
  //
  // A PINNED SCALE IS A BENCH, NOT A DEVICE: a row that holds the ladder still is photographing one
  // instant, and halving a voice under it would move the picture between two shots of one pose.
  function halvesAccompaniment() {
    return !fixedScale && stepIx >= 2;
  }

  // THE JOY FLOOR (charter shelf 19), and every number in it is one already being read. Below the
  // floor the device plays the floor grammar instead of a degraded miracle — and without one, the
  // scale ladder simply walks on to its last rung and keeps drawing a miracle nobody can see move.
  //
  // The floor is where the ladders RUN OUT, which is a reading and not a number: the render ladder
  // standing on its own last rung (`STEPS[STEPS.length - 1]`, nothing further down to step to) while
  // the device's frame times are STILL over the same threshold that made every step before it
  // (`P95_DROP`, on the same window `decideScale` reads). At that point every rung the file has has
  // been spent and the frames are still long — there is nothing left to degrade, so what plays is the
  // grammar rather than a thinner miracle. `fixedScale` is a bench holding the ladder still, and a
  // held ladder has spent no rungs.
  function joyFloorWhy() {
    if (fixedScale || stepIx < STEPS.length - 1) return null;
    var hot = p95Over(WIN_DROP);
    if (hot === null || hot <= P95_DROP) return null;
    return "the render ladder stands on its last rung (" + STEPS[stepIx] + ") and this device's own "
         + "frame gaps still run over " + P95_DROP + " ms: every rung is spent, so the floor grammar "
         + "plays rather than a degraded miracle";
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
    // THE PLAN IS LIGHTENED BEFORE IT IS GIVEN UP, which is his own recorded ladder rather than a
    // loosening of it: a weak device first gets a LIGHTER PLAN WITH FEWER VOICES, and only under
    // that does the plain grammar play. This answered with nothing the moment a stack overran the
    // leanest budget, and the visitor took the walk's plain glide with every instrument in the
    // collection ready to draw. So the topmost voice stands down and the ladder is walked again;
    // a single voice that still overruns is where §7's own floor stands and the plain grammar
    // plays, which is the one case this returns nothing for.
    if (voices.length > 1) {
      var lighter = stackOrder(voices).slice(0, -1).map(function (r) { return r; });
      var kept = [];
      for (var k = 0; k < voices.length; k++) {
        for (var n2 = 0; n2 < lighter.length; n2++) {
          if (lighter[n2].cue === voices[k].cue) { kept.push(voices[k]); break; }
        }
      }
      if (kept.length && kept.length < voices.length) {
        var again = grantVariant(kept, want);
        if (again.variant) {
          again.lightened = (again.lightened || 0) + (voices.length - kept.length);
          again.voices = kept;
          return again;
        }
      }
    }
    var last = tried[tried.length - 1], floor = VARIANTS[0];
    return { variant: null, sum: peakDeclared(voices, floor), budget: BUDGET[floor], tried: tried,
             lowered: false,
             why: "the stack asks for " + last.asked + " " + last.over + " at «" + floor
                + "», which grants " + last.grants + ", and lightening the plan does not reach it "
                + "either — §7's own floor, below which the plain grammar plays" };
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
    // A WALK STILL GOING GETS ITS DOOR BEFORE THE CURTAIN DROPS, WHICHEVER ROAD ARRIVED HERE. The
    // road below reads "a landing cadence already flown" and then applies the arriving pose in CSS —
    // which is right for a cadence that HAS flown and wrong for one still in the air, because it
    // hands the DOM the frame at whatever value the envelopes had reached. `cadenceLand` draws the
    // one frame that stands ON the door and writes the landing down; the caller's own `landState`
    // then carries on below, so a watchdog still reads back as a watchdog and a lost context as a
    // lost context. `cadenceEnd` is deliberately not called: it would dock this record a second
    // time under the cadence's own name.
    if (rec.cadence && !rec.cadence.ended) {
      cadenceLand(rec, why || landState);
      // The door frame is a real frame, so an instrument may refuse its own door from inside it and
      // land the transaction there and then (`st.fail`). Nothing is left for this call to do.
      if (rec.docked) return;
    }
    // EVERY EXIT OWES THE SAME ARRIVING CAMERA DOOR.  A natural settle already starts a cadence
    // when it notices this gap, but watchdog, deadline, context-loss and fail roads reach this
    // one shared door directly.  They used to log an off-rest camera and hand the DOM over anyway.
    // Give a drawable transaction the same short landing cadence before marking it docked; if a
    // renderer is already gone, apply the exact arriving pose before the one-frame handoff.  Thus
    // no exit can reveal B while the carrier still stands at an in-between camera pose.
    var neededRest = rec.hangPoseB || CAM_NEUTRAL;
    var restOff = camOff(rec.lastPose || CAM_NEUTRAL, neededRest);
    // THE LANDING IS FLOWN AGAIN UNTIL IT RESTS, and that repetition is a convergence rather than a
    // loop: `cadenceEnd` calls this function, each flight leaves the camera nearer the arriving
    // door than the one before it, and the reading below is re-taken on a pose that has actually
    // moved. It terminates because the reading improves. What made it NOT terminate was cause F's
    // own reading defect (2026-09-01): an own-camera cue's `lastPose` was its bare residual while
    // the bar was the full hang pose, so no amount of flying could ever close a distance the
    // measurement was not measuring — the seam suite read that as "no cadence frame was caught",
    // and box-fold's real crossings as never docking. Repaired at the source, in `camPoseAt`.
    // Capping the attempts here instead was tried on 2026-09-01 and reverted: it lands a stage cue
    // short of its own door, which is the thing this road exists to prevent.
    if (restOff > CAM_REST_TOL) {
      if (rec.inst && rec.inst.manifest && (!rec.cadence || rec.cadence.ended)) {
        rec.cadence = null;
        cadenceStart(rec, "finish-rest", false, landState);
        return;
      }
      // THIS ROAD IS REACHED ONLY WHERE NO FRAME CAN BE DRAWN — a renderer already gone, or a
      // landing cadence already flown. The plane is then standing wherever the last drawn frame
      // left it, which is not the arriving box, and the instrument's own seating has not been
      // cancelled either, so the arriving hang genuinely has to be laid on in CSS here: it is the
      // only carrier left. It is NOT the double-application cause F named — that was the rest
      // READING, repaired in `camPoseAt` above, which used to send box-fold down this road at every
      // real door while its plane already stood on the box. Left exactly as it was.
      camApply(neededRest, rec.caps);
      rec.lastPose = neededRest;
      rec.camera = neededRest;
    }
    rec.docked = true;
    clearTimeout(rec.watchdogT);
    clearTimeout(rec.deadlineT);
    if (rec.raf) { cancelAnimationFrame(rec.raf); rec.raf = 0; }
    // THE CAMERA RESTS ON THE ARRIVING WORK'S OWN BOX. What the last pose is measured against is the
    // HANG pose of the arriving work — the pose that lays the immersive frame exactly onto the box
    // the work hangs in. The neutral pose is the special case of that, where the box is the whole
    // frame, so a transaction with no hang geometry reads exactly as it always did. The row reads
    // the POSE rather than the picture, and stays honest when the picture changes.
    var restAt = neededRest;
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
                // THE GRID THIS RUN ENDED ON, frozen with everything else the run left behind. The
                // census below is the LIVE canvas and stays that way — that is its job — but a
                // reader asking what one passage applied has to name the passage's own grid, not
                // whatever the canvas has become since. Without this the record could carry the
                // readings of one run beside the buffer of a later one.
                drawnOn: { buffer: W + "x" + H, dpr: dpr },
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
    stageHideAfterPresent(rec.caps);
    try { rec.hooks.dock(rec.cmd); } catch (e) {}
    try { rec.hooks.mark("host-" + landState, rec.cmd, why || null); } catch (e) {}
    // EVERY instrument of the stack releases what it was granted, in draw order.
    instrumentsOf(rec.voices || []).forEach(function (x) {
      try { if (x.dispose) x.dispose(); } catch (e) {}
    });
    cur = null;
    // THE HELD COMMAND TAKES THE STAGE THE INSTANT THE FOLD LETS GO OF IT. This stands in `finish`
    // rather than at the end of the cadence because `finish` is the single dock every exit from
    // `running` passes through: a fold that lands on its own envelope, one the deadline force-ends,
    // an instrument that settles mid-fold, a watchdog, a lost context — all of them arrive here, so
    // a held command can be stranded by none of them.
    //
    // `offer` already answered `true` for this command, so this file owns its landing outright: a
    // road that cannot take it hands it to the glide here rather than returning a `false` nobody is
    // left to read.
    if (foldHeld) {
      var held = foldHeld;
      foldHeld = null;
      if (!offerNow(held.cmd, held.hooks)) {
        try { held.hooks.mark("host-declined", held.cmd, "no instrument could be cast"); } catch (e) {}
        try { held.hooks.glide(held.cmd); } catch (e) {}
      }
    }
  }

  // Both settle and fail are token-checked against the CURRENT transaction's own generation (§2.3),
  // and both are idempotent (§2.4): a call that misses either check changes nothing and is recorded
  // as stale rather than silently dropped.
  function settle(token) {
    if (!cur || cur.docked || token !== cur.cmd.gen || cur.state !== "running") {
      logEvt("stale-settle", token, null);
      return;
    }
    // A CADENCE ALREADY LANDING THIS TRANSACTION OWNS THE LANDING, and an instrument settling
    // inside it is answering a question that has already been answered. The cadence's own last
    // frame stands at the door — which for an arriving door is the pass's own end — so an
    // instrument that settles when it sees its end reports one from inside the call that is landing
    // the pass. Acted on, it docks the transaction half way through `cadenceEnd`, and everything a
    // landing sets running (a held command a fold is holding, above all) starts underneath it.
    // ONCE A CADENCE HAS BEGUN IT OWNS THE LANDING, ended or not. `cadenceEnd` marks itself ended
    // before it draws its own last frame — it has to, or a frame scheduled inside that call would
    // start a second walk — and that last frame stands at the DOOR'S own progress, which for an
    // arriving door is the pass's own end. So an instrument that settles when it sees its end
    // reports one from inside the very call that is landing the pass, at the one instant `ended` is
    // already true. Guarding on `!ended` let exactly that through: the pass docked half way through
    // `cadenceEnd`, and the held command a fold was holding started underneath it.
    if (cur.cadence) {
      logEvt("stale-settle", token, "a cadence is already landing this transaction");
      return;
    }
    // A3 (P1.1): RESOLVE RATHER THAN BLOCK. §6 asks for the camera to rest on the arriving work's
    // own hang pose before the handoff, never after it — and until now `finish` only MEASURED that
    // and logged "camera-not-rested" when it missed, with no branch between the reading and the
    // unconditional handoff a line below it. A natural settle can still miss the exact hang pose by
    // more than the tolerance below — most concretely on a passage the settle reaches through an
    // earlier interruption's own cadence with no usable coverage door, which used to freeze the
    // camera's own clock wherever the interruption caught it (fixed above, in `cadenceStart`) — so
    // the same measurement that already exists here is turned into the actual gate: not resting no
    // longer means "log it and hand the DOM over anyway", it means the camera keeps being driven
    // home through the SAME envelope an interruption already resolves through (`cadenceStart`), and
    // the handoff (inside `finish`, via `cadenceEnd`) waits for that resolution. The one comparison
    // this reads — `camOff(...) <= CAM_REST_TOL` — is the exact one `finish` already made and the
    // test suite already reads back (`tests/test_pass_hang.py`'s REST_TOL, the same 1e-6): no
    // second threshold is invented for this gate.
    var restAt = cur.hangPoseB || CAM_NEUTRAL;
    var atRest = camOff(cur.lastPose || CAM_NEUTRAL, restAt) <= CAM_REST_TOL;
    if (!atRest && cur.inst && cur.inst.manifest) {
      cadenceStart(cur, "settle-rest", false, "docked");
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

  // THE FUNNEL'S LAST DOOR (2026-08-24). Both entries into `offerNow` and its refused-score branch
  // already cast the last resort before a command ever reaches here — this is the one road that did
  // not: every voice's own `prepare` declined, threw, or rejected (`resolveVoices` gave up with
  // `kept.length === 0`), or even the `lean` tier could not fit what the stack — already shed to one
  // voice, where `grantVariant` gets that far — still asks for. Neither is a property of the SCORE
  // the way `scoreWhyNo`'s reasons are; both are properties of what actually ran just now, which is
  // exactly what the last resort exists to answer for.
  //
  // ONE ATTEMPT ONLY (`__lastResortTried`, set by `mergeLastResort` above). A command that has
  // already been through a rescue reaches this function again only if the RESCUED command itself
  // declined — and the built-in instrument's own `prepare` never declines, so that can only be the
  // rare real-instrument rescue failing on its own account. Trying a second cast on the same command
  // would ask the same question of the same DOM images and, most likely, cast the same instrument
  // again — a loop this guard closes rather than one that runs and happens not to recur.
  function declineCurrent(rec, why) {
    if (cur !== rec) return;
    cur = null;
    if (!rec.cmd.__lastResortTried) {
      var cast = lastResortCast(rec.cmd);
      if (cast) {
        var rescued = mergeLastResort(rec.cmd, cast);
        logEvt("declined", rec.cmd.gen, why + " — casting the last resort");
        if (offerNow(rescued, rec.hooks)) return;
      }
    }
    logEvt("declined", rec.cmd.gen, why);
    // ON THE LIVE ROUTE, NO DIAGNOSTICS KEY NEEDED (2026-08-24): `performance.mark` costs nothing and
    // is written unconditionally, the same road `passMark`/`finish`'s own "host-docked" mark already
    // stands on — so a crossing that fell through reads back to its own reason on the timeline by
    // anyone, without turning diagnostics on first.
    try { rec.hooks.mark("host-declined", rec.cmd, why); } catch (e) {}
    try { rec.hooks.glide(rec.cmd); } catch (e) {}
  }

  // A TRANSACTION THAT IS LANDING HAS NOT STOPPED, AND THE WATCHDOG'S QUESTION IS WHETHER IT STOPPED.
  // The watchdog is armed once, at the pass's own duration plus the settle slack, and it used to fire
  // straight into `fail` whatever the transaction was doing. An interruption that arrives near the end
  // of a slow pass therefore raced it: the cadence began, the watchdog fired a few hundred
  // milliseconds later, and `fail` → `finish` docked the visit UNDERNEATH a walk that was still going
  // — the cadence's own deadline cleared, `landedInMs` left null, `ended` left false, and the curtain
  // dropped on a half-walked picture. That is a cut of exactly the kind the seam rows exist to catch,
  // and it read as one: `tests/test_pass_seam.py`'s liquid cadence row measured the abandoned walk
  // against the DOM it was handed to at 240 of 255 over 95 per cent of the frame.
  //
  // `settle` already refuses to act inside a cadence, in those words — "ONCE A CADENCE HAS BEGUN IT
  // OWNS THE LANDING, ended or not" — and this is the same law on the other road. The watchdog waits
  // instead, and what it waits for is not a new number: `cadenceStart` set a real-time `setTimeout`
  // for the cadence's own budget, which `budgetOf` clamps and which runs off the wall clock rather
  // than off the frame loop, so the cadence lands within that budget whatever the frame rate is doing.
  // Re-arming for the SAME budget puts the watchdog strictly behind that deadline — by then the
  // landing has docked the record and this returns at its first line — and leaves the liveness
  // guarantee intact for the case the deadline somehow did not answer.
  function watchdogFire(rec) {
    if (cur !== rec || rec.docked) return;
    var c = rec.cadence;
    if (c && !c.ended) {
      logEvt("watchdog-waits", rec.cmd.gen,
             "a cadence is landing this transaction on door «" + (c.door || "none")
             + "»; the watchdog re-arms behind the cadence's own " + c.budget + " ms budget");
      rec.watchdogT = setTimeout(function () { watchdogFire(rec); }, c.budget);
      return;
    }
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
      pointer: rec.cmd && rec.cmd.interaction && rec.cmd.interaction.pointer,
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
  // the other thing — on an interruption every handle TRAVELS through its own envelope, inside the
  // score's own budget, to the door the visit is landing on, and the transition then lands. The host
  // force-ends at the deadline, so a slow envelope can no more strand the visitor than a silent
  // instrument can.
  // UNJUSTIFIED — the longest a cadence may take to walk to its door. The nineteenth shelf asks
  // for about seven hundred milliseconds and this file chose two seconds as the outer clamp; no
  // measurement of a person watching one stands behind either figure.
  var CADENCE_MIN = 0, CADENCE_MAX = 2000;

  function budgetOf(cmd) {
    var s = cmd && cmd.score, i = s && s.interruption;
    return clampNum(i && i.withinMs !== undefined ? i.withinMs : 0, CADENCE_MIN, CADENCE_MAX);
  }

  // THE SCORE'S OWN WORD ABOUT WHERE A CADENCE RESOLVES, read forward. `interruption.resolve` has
  // carried «nearest-door» on every composed score since the composer shipped and no line of this
  // file ever read it; what the host actually did was walk to the nearer door, and that is what put
  // the picture on one work while the visit docked on the other. The field is read now, and a value
  // asking for a door other than the one the visit lands on is RECORDED rather than obeyed — a
  // score cannot name a resolution that contradicts its own `failLand`, because the two would be
  // two answers to one question again.
  function resolveOf(rec) {
    var s = rec.cmd && rec.cmd.score, i = s && s.interruption;
    var named = i && i.resolve ? String(i.resolve) : null;
    if (named && named !== "arriving-door" && !rec.said.resolve) {
      rec.said.resolve = true;
      logEvt("interruption-resolve", rec.cmd.gen,
             "the score asks for «" + named + "»; the cadence resolves to the door the visit is "
             + "landing on, which is where the dock and §6's rest both already stand");
    }
    return "arriving-door";
  }

  // THE DOOR THE TRANSACTION IS LANDING ON. The cue names its two doors by ONE handle and its two
  // values; the cadence walks to the one whose picture is the work this visit is arriving at. The
  // whole transition picks one door — every handle then travels to the value IT takes at that door,
  // so the picture that lands is a whole work and never a mongrel of two.
  //
  // WHAT STOOD HERE BEFORE was the NEAREST door: whichever of the two values the live handle
  // happened to stand closer to. That gave one question two answers. Interrupted early, the cadence
  // walked back to the DEPARTING work while `finish` docked the visit on the ARRIVING one — the
  // canvas rested on A and the DOM revealed B, in one frame, which is his own 2026-08-25 complaint
  // («картинка бабах и перевернулась прямо перед конечной») and which the seam rows measured at 241
  // of 255 over 99.87 per cent of the frame. A cadence landing on the wrong picture is a cut by any
  // other name, whatever its envelopes did on the way.
  //
  // WHY THE DOCK IS THE ONE THAT WAS RIGHT, read off the mechanism and not off which was cheaper:
  //   · `finish` measures the last pose against `rec.hangPoseB` — the ARRIVING work's own box — and
  //     writes «camera-not-rested» when it misses. §6's rest law already named the arrival, and it
  //     was firing on exactly the landings this repair is about.
  //   · `dock(cmd)` lands the visit on `cmd.to`, and the walk's own resting record is corrected to
  //     that same work at the same instant.
  //   · a further step counts from the running transaction's destination (15-motion.js), so the walk
  //     already considers itself on its way to the arriving work while the passage plays.
  //   · the score itself says so twice — `failLand: "arrive"` and `camera.rests: "b"`.
  // Four readings name the arrival and one named whichever was closer; the one is the one that moved.
  //
  // AND IT IS WHAT THE NINETEENTH SHELF ASKS FOR IN ITS OWN WORDS: on interruption the crossing
  // COMPRESSES TO ITS CADENCE. A crossing interrupted at a tenth of its length compresses the
  // remaining nine tenths into the cadence's own budget, through the same envelopes. Retreating to
  // where it began is not a compression of a crossing; it is the abandonment of one.
  function landingDoorOf(rec, live) {
    var v = rec.primary, cue = v.cue || {}, doors = cue.doors || {};
    var din = doors["in"], dout = doors.out;
    if (!din || !dout || din.handle !== dout.handle) return null;
    var k = din.handle, at = Number(live[k]);
    if (!isFinite(at)) return null;
    // THE DOOR MAY NAME A HANDLE THE MANIFEST NEVER PUBLISHED. Nothing refuses such a score: the
    // host's own `scoreWhyNo` reads no door against any manifest, and the gate that does stands
    // outside this engine and never sees a score this composer wrote (`SPEC.md`, `INV-109`). This
    // read `manifest.handles[k].min` straight, so the blank door cost a TypeError inside the
    // interruption cadence — the one moment the visitor is already leaving — instead of the plain
    // landing the cadence has for a cue that names no usable door. `doorHandles` beside it has
    // guarded the same read since it was written; this is the same guard and the same answer,
    // said out loud on the diagnostic surface so the score can be found and mended.
    if (!(v.inst.manifest.handles || {})[k]) {
      logEvt("cadence-door-unpublished", rec.cmd && rec.cmd.gen,
             "cue «" + (cue.id || "?") + "» names its doors on handle «" + k + "», which «"
             + (v.inst.name || "?") + "» does not publish — there is "
             + "no door to land on, so the handles hold where they stand");
      return null;
    }
    // The arriving door is the cue's own far end — the state the pass would have ended in had
    // nothing interrupted it, which is the state the visit is docking on.
    var which = "out";
    var seconds = (cue.window || [0, rec.duration / 1000])[1];
    var progress = 1;
    // Every handle at the door: its own track read at the door's own instant, with the door handle
    // itself pinned to exactly the value the door names.
    var want = handlesOf(rec, v, progress, seconds, 0);
    var at_door = {};
    Object.keys(want).forEach(function (h) { at_door[h] = want[h]; });
    at_door[k] = clampNum(doors[which].value, v.inst.manifest.handles[k].min,
                          v.inst.manifest.handles[k].max);
    return { which: which, handle: k, value: Number(doors[which].value), handles: at_door,
             progress: progress, seconds: seconds,
             // How far the walk actually is — the reading the old choice was made on, kept because
             // it says what the compression cost, and dropped as an authority over where to land.
             walk: +Math.abs(at - Number(dout.value)).toFixed(9) };
  }

  // Each handle travels on its OWN envelope. A cue may name one per handle in `cadence` — any of the
  // four named curves — and a handle the cue says nothing about walks on `smooth`, which leaves and
  // arrives at rest.
  function envelopeFor(cue, handle) {
    var named = cue && cue.cadence ? cue.cadence[handle] : null;
    return CURVES[named] || CURVES.smooth;
  }

  function cadenceStart(rec, reason, immediate, landState) {
    var live = rec.lastHandles
             || handlesOf(rec, rec.primary, rec.lastProgress || 0, rec.lastSeconds || 0, 0);
    resolveOf(rec);
    var door = landingDoorOf(rec, live);
    var budget = immediate ? 0 : budgetOf(rec.cmd);
    rec.cadence = {
      reason: reason, budget: budget, forced: !!immediate, landState: landState || "cancelled",
      door: door ? door.which : null, doorHandle: door ? door.handle : null,
      // A3 FOLLOW-UP (found under load, `tests/test_pass_hang.py`'s own row A3 flaking in the full
      // parallel suite): this field — NOT `toSeconds` below — is what `cadenceEnd` draws its own
      // FINAL frame at. `cadenceEnd` runs on two roads: the cadence reaching its own envelope's end
      // (`runFrame`, where `rec.lastSeconds` has already been advanced to `toSeconds` by that same
      // call) and the deadline timer firing first (a real-time `setTimeout`, independent of the
      // frame loop) — and under a slow or sparse frame rate the deadline can fire before any frame
      // ever reaches the envelope's own end, landing `cadenceEnd` on whatever `rec.lastSeconds` the
      // LAST natural frame left behind, short of the target. Leaving this field `undefined` for the
      // no-door case fell back to exactly that stale value (`cadenceEnd`'s own
      // `c.seconds === undefined ? rec.lastSeconds : c.seconds`) regardless of which road landed it,
      // so the camera's own last frame could be drawn short of the true end on the deadline road
      // even though `toSeconds` below already marches the FRAME LOOP there correctly — a race
      // between which road gets there first, not a fix. Stating it explicitly, the same way
      // `toSeconds` is, closes both roads on the one number.
      seconds: door ? door.seconds : (rec.duration > 0 ? rec.duration / 1000 : undefined),
      from: live, to: door ? door.handles : live,
      // THE PASSAGE'S OWN CLOCK TRAVELS WITH THE HANDLES. A cadence used to walk the instrument's
      // handles to their door while the SECOND fed to the frame loop went on running off the wall
      // clock — so the carrier and the camera, which read that second and not the handles, stayed
      // wherever the interruption caught them and were then put on the landing in `cadenceEnd`'s one
      // last frame. The handles arrived through their envelopes and the plane arrived in a step: a
      // crossing cut short at a tenth of its length snapped from the whole frame down to the
      // arriving work's own rectangle between two frames, which is a cut whatever the handles did.
      // The nineteenth shelf asks for EVERY voice to resolve through the same envelopes, and the
      // carrier and the flight are voices. So the second travels too, from where the interruption
      // caught the passage to the door's own second, and the remaining span of the crossing is
      // COMPRESSED into the cadence's budget — which is the shelf's own word for what this is.
      //
      // THE CAMERA'S OWN TARGET NEVER FREEZES, EVEN WITHOUT A DOOR (A3, P1.1). `door` answers for
      // the CUE's own handles — a coverage door on a shared handle, which not every cue names — but
      // the camera's target is `rec.hangPoseB`, read straight off the DOM and owed independently of
      // whatever the cue's own doors say (§6: "the seam: exact A hang → one continuous passage →
      // exact B hang", failLand:"arrive"). `anchorPose`'s spline already clamps at the passage's own
      // full duration, so marching the clock there — rather than freezing it at wherever an
      // interruption caught the passage — is what lets the camera actually rest on arrival even on a
      // cue with no usable coverage door; the cue's own handles are unaffected, because a cadence
      // frame always pins them to `c.to` directly (`playFrame`'s `hold`) rather than reading them off
      // this clock.
      fromSeconds: rec.lastSeconds || 0,
      toSeconds: door ? door.seconds : (rec.duration > 0 ? rec.duration / 1000 : (rec.lastSeconds || 0)),
      fromProgress: rec.lastProgress || 0, toProgress: 1,
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
    // The passage's own second and its own progress, carried on `smooth` — the curve a handle the
    // cue says nothing about already walks on, and the second is exactly such a thing: no cue names
    // it, and every voice that reads it (the carrier, the flight, a window's own opening) must
    // arrive with the handles rather than after them.
    var e = CURVES.smooth(u);
    return { handles: out, u: u,
             seconds: c.fromSeconds + (c.toSeconds - c.fromSeconds) * e,
             progress: c.fromProgress + (c.toProgress - c.fromProgress) * e };
  }

  // THE LANDING ITSELF, WITHOUT THE DOCK THAT NORMALLY FOLLOWS IT. `cadenceEnd` below is this plus
  // the dock, and it is the road a cadence takes when it reaches its own end. This half stands on its
  // own because `finish` needs it too: an exit road that force-lands a transaction while a cadence is
  // STILL WALKING owes that cadence its door before the curtain drops, and it owes it under its OWN
  // land state rather than the cadence's — so it cannot call `cadenceEnd`, which would dock the
  // transaction a second time under a different name. Split out rather than written twice, so the
  // door frame, the `atDoor` reading and the cleared deadline can never drift apart between the two
  // callers.
  function cadenceLand(rec, why) {
    var c = rec.cadence;
    c.ended = true;
    c.landedInMs = Math.round(performance.now() - c.t0);
    // ONE LAST FRAME, ON THE DOOR ITSELF, so the picture the curtain drops on is the door and not
    // wherever the envelope had reached when the deadline arrived. This is what makes the host's
    // force-end at the deadline a landing rather than a cut.
    if (rec.inst && rec.inst.manifest && !rec.docked) {
      try { playFrame(rec, c.seconds === undefined ? (rec.lastSeconds || 0) : c.seconds,
                      c.toProgress === undefined ? (rec.lastProgress || 0) : c.toProgress,
                      0, c.to); }
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
  }

  function cadenceEnd(rec, why) {
    if (!rec.cadence || rec.cadence.ended) return;
    var c = rec.cadence;
    cadenceLand(rec, why);
    // `finish` acts on whatever stands in `cur`. Every other caller in this file checks first that
    // the record it means is still the one there; this one does too, so a landing that happened
    // inside the frame above can never be followed by a second landing of somebody else's pass.
    // `c.landState` is "cancelled" for every caller that always named it (an interruption, a
    // supersede) and "docked" for the one that does not (A3's settle-rest resolve, below) — so a
    // natural landing that only needed its camera driven the rest of the way home still reads back
    // as the natural landing it was, rather than an interruption that never happened.
    if (cur === rec && !rec.docked) finish(c.landState, c.reason);
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
    var gl = stage && stage.gl;
    if (gl) {
      gl.disable(gl.SCISSOR_TEST);
      gl.viewport(0, 0, W, H);
      gl.disable(gl.BLEND);
      gl.clearColor(0, 0, 0, 0);
      gl.clear(gl.COLOR_BUFFER_BIT);
    }
    var plane = planeAt(rec, seconds, cam.art);
    planeApply(plane);
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
    // THE ACCOMPANIMENT AT HALF RATE, THE MIRACLE AT FULL (charter shelf 19's middle step). Every
    // voice still DRAWS on every frame — the buffer is cleared and rebuilt each time, so a voice that
    // skipped its draw would blink out rather than play slower — and what halves is the rate its own
    // motion is re-read at: on the odd frames an accompaniment voice is handed the very handles it
    // was handed on the frame before, so its motion advances 30 times a second while the miracle's
    // advances 60. `rec.primary` is the miracle — the score's own line-0 voice — and it is never
    // slowed. A voice on its first frame has no previous handles to hold and reads its own.
    var halve = halvesAccompaniment();
    var odd = (rec.frames & 1) === 1;
    // THE HANDLES A HELD FRAME IS DRAWN WITH ARE KNOWN BEFORE IT IS DRAWN, so they are written down
    // before it is drawn. This stood at the foot of the loop, after every voice had been walked, and
    // an instrument that FAILS from inside its own frame never reached it: `st.fail` lands the
    // transaction there and then, and `finish` freezes what the run left behind — so the record
    // carried the PREVIOUS frame's handles beside a reading the instrument had just published from
    // THIS one, and the two could not be read as one frame. A door proof refusing at the cadence's
    // own landing frame is exactly that case, and it is not a rare one: it is what a door proof is
    // for. `hold` is the cadence's own handle set, settled before the loop begins and untouched by
    // it, so nothing is lost by saying so first.
    if (hold) rec.lastHandles = hold;
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
      var slowed = halve && odd && v !== rec.primary && v.paceHandles;
      var handles = (hold && v === rec.primary) ? hold
                  : (hold ? doorHandles(rec, v, (rec.cadence && rec.cadence.door) || "out")
                          : (slowed ? v.paceHandles
                                    : handlesOf(rec, v, progress, seconds, dt)));
      // WRITTEN DOWN BEFORE THE INSTRUMENT IS ASKED, for the same reason the frame's own handles
      // are: an instrument that refuses its door does so from inside `frame`, and `st.fail` lands
      // the transaction from there — so a voice's row would otherwise be frozen carrying the
      // handles of the frame BEFORE the one whose reading it is published beside, and the two could
      // not be read as one frame.
      if (hold) v.lastHandles = handles;
      v.inst.frame(frameState(rec, v, seconds, progress, handles, cam, hold, drew, plane));
      if (v.drawnThisFrame) { drew++; v.drawnThisFrame = false; }
      if (!hold) v.paceHandles = handles;
    }
    rec.liveCues = live;
    rec.drewLastFrame = drew;
    // THE POSE AS THE CARRIER COULD CARRY IT. `plane.art` is the score's own track where the frame
    // is covered outright, and the same track held closer in where covering it would have asked for
    // more carrier than the resolution floor allows. The pose the record reports is what was ASKED;
    // `plane.hold` beside it is how much of it the frame could take.
    camApply(plane.art || cam.art, rec.caps, plane.over);
    rec.camHold = plane.hold;
    rec.camOver = plane.over;
  }

  // ---- §8's `seams` block: THE FLEET'S TWO SHARED SEAM SHAPES ------------------------------------
  // Three instruments — kaleidoscope, planet, tunnel — each cut the frame at a boundary a picture
  // cannot help but have (a fold's own edge, a wrap's own join) and each rounded it by hand, in its
  // own file, with its own typed number: kaleidoscope's crease retouch, planet's cross-dissolve where
  // a curled strip's two ends meet, tunnel's cross-fade where one depth-ring hands over to the next.
  // All three are one of exactly two shapes, and an instrument now DECLARES which one it needs
  // (`manifest.seams`) instead of carrying the arithmetic itself.
  //
  //   A HAIRLINE RETOUCH rounds a crease that is already continuous — the fold does not jump, only
  //   its own derivative does — so its width is CAPABILITY: a fact about the SAMPLING GRID and not
  //   about the picture, exactly like how many bytes a float takes or how long a frame is. Below one
  //   point of the drawing buffer it falls inside a single sample and does nothing; past three it
  //   stops rounding a crease and starts smearing it into a visible band. 1.5 buffer points is the
  //   middle of that span AT ONE POINT OF BUFFER PER CSS PIXEL — kaleidoscope's own number, argued
  //   in its file before this block existed. It used to travel from there into this host unchanged,
  //   digit for digit, which answered no question this host had not already been asked: a buffer
  //   point is not a fixed physical width, because the drawing buffer this host binds is the CSS
  //   frame times the device's own pixel ratio times the render ladder's live rung
  //   (`bindCanvas`/`changeStep` above bind `W = cssW * dpr * s`), and both of those move under a
  //   score without either photograph changing at all. 1.5 read as CSS-pixel-equivalent points and
  //   carried onto the actual buffer through `seamScaleOf()` — the ratio the host already measures
  //   between the buffer it just bound and the CSS frame it was asked for — answers the same
  //   question kaleidoscope's own file argued (below one sample does nothing, past three it smears)
  //   on the buffer this frame is actually drawn on, rather than on the buffer kaleidoscope's file
  //   happened to carry the argument against. It does not shrink as its element repeats more often,
  //   because a hairline spends none of the element's own room.
  //
  //   A HANDOVER ZONE glues two ends of a wrap together over a real, visible span — a cross-dissolve,
  //   not an antialiasing retouch — so its width IS a share of the room the wrap itself has: one part
  //   in eight of what a single repeat gets AT THAT SAME ONE-POINT-PER-CSS-PIXEL BUFFER, halved again
  //   for every further repeat sharing the same turn, and never allowed under a hundredth or over a
  //   fifth — the same floor-and-ceiling reasoning the hairline stands on, read in the handover's own
  //   unit. The eighth is a share of a repeat's own span in BUFFER points, so at a buffer standing
  //   denser than one point per CSS pixel a repeat holds more of them and the same physical blend
  //   costs a smaller share of it; `seamScaleOf()` carries the fraction the same way it carries the
  //   hairline, so the fleet reads one measurement rather than two.
  //
  // `seamScaleOf()` IS THE ONE MEASUREMENT BOTH NUMBERS BELOW READ. `W / cssW` is buffer points per
  // CSS pixel on the frame actually bound this instant: 1 on a dpr-1 screen at the render ladder's
  // top rung, 2 on a dpr-2 screen at that same rung, and less again the moment the ladder has dropped
  // a rung under perf pressure (`changeStep` above). Nothing here is typed against any one screen or
  // photograph; it is read off the same `W`/`cssW` the buffer was just bound with, so a retina screen
  // and a throttled rung both move the number the way the case argues they should, rather than both
  // handing every pair the one literal a single earlier file happened to be measured against.
  function seamScaleOf() {
    var scale = W / Math.max(cssW, 1);
    return scale > 0 ? scale : 1;
  }
  // CAPABILITY: the middle of the one-to-three-buffer-point span the HAIRLINE RETOUCH paragraph
  // above argues, read at one buffer point per CSS pixel — a fact about the sampling grid at that
  // baseline density, exactly as kaleidoscope's own file argued it, and no more about either
  // picture than it ever was. `seamHairlineOf` carries it onto the buffer actually bound.
  var SEAM_HAIRLINE_CSS_POINTS = 1.5;
  // CAPABILITY: one part in eight of a repeat's own span at that same one-point-per-CSS-pixel
  // baseline — the HANDOVER ZONE paragraph's own floor-and-ceiling sampling argument, read in the
  // handover's own unit rather than the hairline's. `seamHandoverOf` carries it the same way.
  var SEAM_HANDOVER_CSS_SHARE = 0.125;
  function seamHairlineOf() {
    var pts = SEAM_HAIRLINE_CSS_POINTS * seamScaleOf();
    return pts < 1 ? 1 : (pts > 3 ? 3 : pts);
  }
  function seamHandoverOf(count) {
    var share = (SEAM_HANDOVER_CSS_SHARE / seamScaleOf()) / Math.max(Number(count) || 1, 1);
    return share < 0.01 ? 0.01 : (share > 0.2 ? 0.2 : share);
  }
  // THE DECLARATION READ, for one instrument, on the handles this frame actually stands at. `of`
  // names the handle counting how many times this seam's own element repeats round its full turn;
  // an instrument whose seam is not spent per-repeat (planet's wrap, tunnel's ring) names none, and
  // the share is read as a single turn's own share. Returns null where the manifest names no seam at
  // all, so an instrument that predates this block asks the host for nothing and gets nothing back.
  function seamsOf(inst, handles) {
    var decl = inst && inst.manifest && inst.manifest.seams;
    if (!decl || !decl.length) return null;
    var out = {};
    decl.forEach(function (s) {
      var count = s.of && handles && handles[s.of] !== undefined ? handles[s.of] : 1;
      out[s.kind] = s.unit === "points of the drawing buffer" ? seamHairlineOf()
                                                               : seamHandoverOf(count);
    });
    return out;
  }

  // The record one voice receives. Held apart from the loop above so the closure over `v` and `drew`
  // is made once per voice per frame rather than captured by accident from a shared variable.
  function frameState(rec, v, seconds, progress, handles, cam, hold, drew, plane) {
    return {
      token: rec.cmd.gen, t: seconds, progress: progress,
      handles: handles,
      // WHERE THIS VOICE STANDS IN THE STACK, which is the one thing an instrument cannot know about
      // itself and which decides WHICH DOOR LAW it owes (see the entry-door contract,
      // docs/design/ENTRY-DOOR.md). The lowest voice of a score is drawn onto the cleared buffer
      // with blending disabled and must be the departing work whole at its entry door and the
      // arriving work whole at its exit — that is the law every door proof in the fleet was written
      // against. A voice standing OVER another owes the opposite: at its doors it must be ABSENT at
      // every point, so that what stands beneath it is what the door shows, whole and untouched.
      // `rec.voices` is held in draw order, ascending stack, so its first entry is the lowest.
      standsOver: !!(rec.voices && rec.voices.length && v !== rec.voices[0]),
      // The frame, and the grid it is drawn on. `w`/`h` are CSS pixels; `bufferW`/`bufferH` are the
      // drawing buffer this host binds as the `resolution` source, which is the CSS frame times the
      // device ratio times the live resolution step. An instrument whose own law depends on where a
      // sample lands — the meshing one reads its doors there — has to read the buffer, because the
      // step moves under it while a pass plays and no serialised plan can know it. Added 2026-08-16.
      viewport: { w: cssW, h: cssH, dpr: dpr, bufferW: W, bufferH: H },
      // BOTH WORKS' SEATING ON THIS BUFFER, which only the host can answer. The instrument's own
      // `fit` cover-fits a work into the frame and pulls in by its own framing headroom, and the
      // draw binds the result as the `fitA`/`fitB` uniforms — so a shader that folds a work, and one
      // that drifts it, read the seating BACK out of it (`SZ`, `outOf`) while their scripts could
      // not reach it at all. Both therefore bounded their geometry by the worst a cover fit can hand
      // and could only over-hold. Asked for here, on the same buffer, through the same function the
      // draw calls, so the script and the shader work from ONE seating rather than two guesses at
      // it. Added 2026-08-17 on the doors lane's request.
      fitA: instFit(v.inst, rec.src.aw, rec.src.ah),
      fitB: instFit(v.inst, rec.src.bw, rec.src.bh),
      // THE SEAM WIDTHS §8's `seams` block asks for, read once here off the handles this frame
      // stands at, so kaleidoscope's crease, planet's wrap and tunnel's ring-join draw one shared
      // shape apiece instead of the number each used to carry on its own. Null where the manifest
      // declares no seam, which is every instrument that predates this block.
      seams: seamsOf(v.inst, handles),
      reduced: !!rec.cmd.reduced,
      camera: cam.pose,
      // a pinned run is a bench run: it holds its pose instead of walking to the end door, so a
      // conformance row can photograph one instant twice and compare it to itself
      pinned: pinProgress !== null || !!hold,
      draw: function (pose) {
        v.drawnThisFrame = true;
        drawPose(v.inst, pose, rec.src, drew > 0, plane);
        if (rec.needsScene) carryScene();
      },
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

  // ================================================================================================
  // THE LAST RESORT (2026-08-24, the charter's own word: for any pair of pictures a way to play the
  // crossing must be found — nothing prepared in advance, nothing that could have existed before the
  // two pictures were known). SHIPS INSIDE THIS FILE, registered unconditionally, the moment the
  // site's record has settled either way (§7's boundary comment above still holds: no SITE instrument
  // NAME is written here — this one belongs to the host's own machinery, the same shelf the
  // diagnostics-only test instrument stands on, except this one is registered for real use). Its job
  // is narrow: give `offerNow` something playable when the score names an instrument the registry
  // does not carry, or names no instrument at all, so a cold visit whose baked instrument list has
  // not landed yet — or never lands — still crosses.
  function fitCoverSpan(iw, ih, pw, ph) {
    iw = Math.max(1, Number(iw) || 1); ih = Math.max(1, Number(ih) || 1);
    pw = Math.max(1, Number(pw) || 1); ph = Math.max(1, Number(ph) || 1);
    var boxAsp = pw / ph, imgAsp = iw / ih;
    return imgAsp > boxAsp ? [imgAsp / boxAsp, 1, 0, 0] : [1, boxAsp / imgAsp, 0, 0];
  }
  var LAST_RESORT_NAME = "@host/last-resort";
  function makeLastResortInstrument() {
    var VERT = "attribute vec2 aPos;\nvarying vec2 vUV;\n"
             + "void main(){ vUV = aPos * 0.5 + 0.5; gl_Position = vec4(aPos, 0.0, 1.0); }\n";
    // A REAL WIPE, NOT A CROSSFADE (charter shelf 18 forbids a "no bridge derives" fallback road): a
    // moving boundary between two sharp images, never a blend of both. The handle's own span carries
    // padding past 0…1 (see MANIFEST below) so the frame reads as purely A at the door and purely B
    // at the far door, with no partial mix visible at either rest.
    //
    // IS THIS RESCUE'S BOUNDARY A WIPE SHELF 18 STILL CONVICTS? THE THREE-PART TEST, ANSWERED ON ALL
    // THREE COUNTS (2026-08-26, replacing an earlier draft that failed all three by comparing
    // `uReveal` against `vUV.x` — a frame coordinate that reads neither photograph and could have
    // been written before either work was known):
    //   1. THE BOUNDARY IS A LEVEL SET OF WHAT THE TWO PHOTOGRAPHS THEMSELVES CARRY. `field` below
    //      is built from `lumA` and `lumB`, the luminance of the very texels each fragment already
    //      read off `uTexA`/`uTexB` — never from `vUV`, and never from anything that could exist
    //      before this pair's own pixels were sampled.
    //   2. THE TWO IMAGES INTERACT AT EVERY FRAGMENT, NOT ACROSS A LINE. Both textures are read and
    //      folded into `field` before any mix weight exists, so no pixel's fate is decided by one
    //      picture alone or by neither.
    //   3. IT READS AS A DISSOLVE LED BY THE PICTURES, NEVER AN EDGE TRAVELLING THE FRAME. The same
    //      `uReveal` run against two different pairs yields two different boundary shapes, because
    //      the shape IS the pair's own measured field (shelf 21: nothing here could have been baked
    //      in before the two photographs arrived).
    var FRAG = "precision mediump float;\nvarying vec2 vUV;\n"
             + "uniform sampler2D uTexA;\nuniform sampler2D uTexB;\n"
             + "uniform vec4 uFitA;\nuniform vec4 uFitB;\nuniform float uReveal;\n"
             + "vec2 coverUV(vec2 uv, vec4 fit) {\n"
             + "  vec2 c = uv - 0.5;\n"
             + "  c.x /= max(fit.x, 0.0001);\n"
             + "  c.y /= max(fit.y, 0.0001);\n"
             + "  return c + 0.5;\n"
             + "}\n"
             + "void main() {\n"
             + "  vec2 uvA = clamp(coverUV(vUV, uFitA), 0.0, 1.0);\n"
             + "  vec2 uvB = clamp(coverUV(vUV, uFitB), 0.0, 1.0);\n"
             + "  vec3 a = texture2D(uTexA, uvA).rgb;\n"
             + "  vec3 b = texture2D(uTexB, uvB).rgb;\n"
             + "  float lumA = dot(a, vec3(0.2126, 0.7152, 0.0722));\n"
             + "  float lumB = dot(b, vec3(0.2126, 0.7152, 0.0722));\n"
             + "  float field = 0.5 * (lumA + (1.0 - lumB));\n"
             + "  float w = smoothstep(uReveal - 0.08, uReveal + 0.08, field);\n"
             + "  gl_FragColor = vec4(mix(b, a, w), 1.0);\n"
             + "}\n";
    var MANIFEST = {
      neutralPose: { reveal: -0.15, t: 0 },
      handles: { reveal: { min: -0.15, max: 1.15, def: -0.15 } },
      coverage: { writes: false },
      resources: {
        lean:     { textures: 2, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1, passes: 1, bytesEstimate: 4194304 },
        standard: { textures: 2, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1, passes: 1, bytesEstimate: 4194304 },
        rich:     { textures: 2, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1, passes: 1, bytesEstimate: 4194304 },
      },
      passes: [{
        program: "host-last-resort-wipe",
        position: "aPos",
        vert: VERT, frag: FRAG,
        uniforms: [
          { name: "uTexA", type: "sampler2D", source: "textureA" },
          { name: "uTexB", type: "sampler2D", source: "textureB" },
          { name: "uFitA", type: "vec4", source: "fitA" },
          { name: "uFitB", type: "vec4", source: "fitB" },
          { name: "uReveal", type: "float", source: "handle:reveal" },
        ],
      }],
    };
    var settledTok = null;
    return {
      name: LAST_RESORT_NAME,
      manifest: MANIFEST,
      fit: fitCoverSpan,
      values: function () { return {}; },
      prepare: function () { settledTok = null; return { take: true }; },
      start: function (token) { settledTok = token; },
      frame: function (state) {
        var pose = {}, h = state.handles || {}, k;
        for (k in h) if (Object.prototype.hasOwnProperty.call(h, k)) pose[k] = h[k];
        pose.t = state.t;
        state.draw(pose);
        if (state.progress >= 1 && settledTok !== null) {
          var t = settledTok; settledTok = null; state.settle(t);
        }
      },
      resize: function () {},
      cancel: function () {},
      dispose: function () {},
      contextLost: function () {},
      contextRestored: function () {},
    };
  }

  // WHICH INSTRUMENT THE LAST RESORT CASTS. A real, already-registered drawing instrument (never the
  // diagnostics probe, never this built-in) is preferred ONLY where it is PROVABLY playable alone —
  // its own declared `lean` cost fits under the leanest budget by itself, the same arithmetic
  // `grantVariant` judges every score by — so a warm visit casts with the site's own instrument
  // where doing so cannot itself reopen a resources-decline the funnel exists to close. Anything
  // else, including a cold visit with nothing loaded yet, falls back to the built-in above, whose
  // declared cost is set to clear that same floor by construction.
  function lastResortCastInstrument() {
    var keys = Object.keys(instruments), i, cand, d;
    for (i = 0; i < keys.length; i++) {
      cand = instruments[keys[i]];
      if (!cand || !cand.manifest || cand.probe || cand.name === LAST_RESORT_NAME) continue;
      d = (cand.manifest.resources || {}).lean;
      if (d && !overBudget(d, BUDGET.lean)) return cand;
    }
    return instruments[LAST_RESORT_NAME] || null;
  }

  // A PLAYABLE SCORE BUILT FROM WHAT THE HOST ALREADY HOLDS, NOTHING LOOKED UP. One cue, one
  // instrument, no track the score had to author in advance: every handle the instrument declares is
  // driven across its own [min, max] span by `progress`, through the evaluator already in this file,
  // so the motion comes from whichever instrument's own manifest is on the registry right now —
  // nothing baked, nothing pair-specific. A one-cue score is exempt from the coverage law and cannot
  // be refused by the tier budget (`coverageWhyNo`, `grantVariant`'s floor), so nothing downstream of
  // this can decline it again except a genuinely absent WebGL2 context or a picture truly missing
  // from the DOM.
  // THE FLEET'S JUDGES' CHANNEL, BY NAME. `mask` is how every instrument in the registry (droste,
  // strata-light, waterline, parquet, studio, gates, liquid, unfold, grid-colour, livemirror,
  // kaleidoscope and the rest) names the channel a door-refusal is read against — pass-inst-gates.js
  // calls it "the fleet's judges' channel, published by thirteen instruments". It rests at its own
  // declared `def` (0 on every instrument that carries it) at both doors; sweeping it end to end is
  // exactly Bug 1's door-refusal class, so the rescue leaves it alone the same way it already leaves
  // an `open` handle alone.
  // CAPABILITY — a fact about the fleet's own declared names: which handle the rescue leaves where
  // its instrument rests it. The one is set membership and not a quantity.
  var LAST_RESORT_REST_HANDLES = { mask: 1 };

  // A COARSE READING OF THE TWO ACTUAL PICTURES, taken fresh at the instant of the cast — never
  // prepared ahead of the visit, per shelf 21 of the crossing charter ("could this value have
  // existed before the two pictures in front of it were known? If yes, it is banned"). A rescue is
  // a poorer instrument, not one blind to which two pictures it was cast for. `im` may still be
  // mid-load this late in a decline — every read here is defensive and answers `null` rather than
  // throwing, so a stalled image degrades the bias, never the rescue's own reliability.
  function lastResortImageStat(im) {
    try {
      if (!im || !im.naturalWidth || !im.naturalHeight) return null;
      var n = 8, c = document.createElement("canvas");
      c.width = n; c.height = n;
      var ctx = c.getContext("2d");
      if (!ctx) return null;
      ctx.drawImage(im, 0, 0, n, n);
      var d = ctx.getImageData(0, 0, n, n).data, sumR = 0, sumG = 0, sumB = 0, sumL = 0, count = n * n, i;
      for (i = 0; i < d.length; i += 4) {
        sumR += d[i]; sumG += d[i + 1]; sumB += d[i + 2];
        sumL += 0.2126 * d[i] + 0.7152 * d[i + 1] + 0.0722 * d[i + 2];
      }
      return { lum: sumL / count / 255, r: sumR / count / 255, g: sumG / count / 255, b: sumB / count / 255 };
    } catch (e) {
      return null;
    }
  }
  // Which way and how far the rescue sweeps, from the two actual pictures. `dir < 0` reverses a
  // handle's own [min,max] to [max,min] — the arriving picture reads darker/cooler than the
  // departing one, so the rescue travels the other way — and `mag` (0..1) scales how much of the
  // handle's own span the sweep uses, so two measurably similar pictures get a gentler rescue than
  // two very different ones (still moving — never collapsed to a standstill — at `mag === 0`).
  function lastResortBias(a, b) {
    var sa = lastResortImageStat(a), sb = lastResortImageStat(b);
    if (sa && sb) {
      var dl = sb.lum - sa.lum;
      var chroma = (Math.abs(sb.r - sa.r) + Math.abs(sb.g - sa.g) + Math.abs(sb.b - sa.b)) / 3;
      var diff = Math.max(Math.abs(dl), chroma);
      return { dir: dl >= 0 ? 1 : -1, mag: Math.min(1, diff * 3) };
    }
    // The pixel sample needs a decoded image; where neither picture has one yet, its own natural
    // aspect ratio is the cheapest always-available signal already on the DOM.
    var aa = a && a.naturalWidth ? a.naturalWidth / Math.max(1, a.naturalHeight) : null;
    var ab = b && b.naturalWidth ? b.naturalWidth / Math.max(1, b.naturalHeight) : null;
    if (aa !== null && ab !== null) {
      var da = ab - aa;
      return { dir: da >= 0 ? 1 : -1, mag: Math.min(1, Math.abs(da)) };
    }
    return { dir: 1, mag: 0 };
  }
  function lastResortCast(cmd) {
    var a = workImg(cmd && cmd.from && cmd.from.id), b = workImg(cmd && cmd.to && cmd.to.id);
    if (!a || !b) return null;
    var inst = lastResortCastInstrument();
    if (!inst) return null;
    var bias = lastResortBias(a, b);   // computed fresh for this cast, never cached or precomputed
    var tracks = {}, handles = inst.manifest.handles || {}, k;
    for (k in handles) {
      if (!Object.prototype.hasOwnProperty.call(handles, k)) continue;
      var h = handles[k];
      if (h.open || LAST_RESORT_REST_HANDLES[k]) continue;
      var lo = h.min === undefined ? 0 : Number(h.min), hi = h.max === undefined ? 1 : Number(h.max);
      var mid = (lo + hi) / 2, span = (hi - lo) * (0.4 + 0.6 * bias.mag);
      var loEff = mid - span / 2, hiEff = mid + span / 2;
      tracks[k] = { op: "map", "in": { source: "progress" }, from: [0, 1],
                    to: bias.dir >= 0 ? [loEff, hiEff] : [hiEff, loEff] };
    }
    return { cues: [{ id: "last-resort", instrument: { id: inst.name }, tracks: tracks }] };
  }

  // ONE COMMAND, ONE LAST-RESORT ATTEMPT. `__lastResortTried` is set the instant a cast is merged
  // in, on the merged copy `mergeScore` returns — never on the command it was built from — so the
  // mark travels with the rescued command and with no other. `mergeScore` itself stays plain (it
  // also builds `scoreShed`'s trial stacks, which are not a last-resort cast); every place that
  // merges a last-resort cast — the funnel's two give-up exits in `offerNow`, its refused-score
  // branch when `scoreShed` cannot answer, and `declineCurrent`'s own rescue below — goes through
  // here instead, so no route can hand a command a second cast to try.
  function mergeLastResort(cmd, cast) {
    var nc = mergeScore(cmd, cast);
    nc.__lastResortTried = true;
    return nc;
  }

  function runFrame(rec, now) {
    if (cur !== rec || rec.docked) return;
    rec.raf = requestAnimationFrame(function (t) { runFrame(rec, t); });
    rec.frames++;              // this transaction's own frame count, which the half-rate accompaniment
                               // reads the parity of — never the wall clock, so a pinned bench clock
                               // and a live one pace the voices the same way
    noteFrame(now);
    var dt = rec.lastNow ? (now - rec.lastNow) / 1000 : 0;
    rec.lastNow = now;
    var seconds = pinClock !== null ? pinClock : (now - rec.t0) / 1000;
    var progress = pinProgress !== null ? pinProgress
      : (rec.duration > 0 ? Math.min(1, (now - rec.t0) / rec.duration) : 1);
    try {
      if (rec.cadence && !rec.cadence.ended) {
        // THE CADENCE OWNS THE CLOCK while it plays. The second and the progress are its own
        // compressed ones, and everything downstream — the carrier's box, the camera's anchor, the
        // placement of the walk under cover — reads them, so the whole picture arrives together.
        var walk = cadenceHandles(rec, now);
        rec.lastSeconds = walk.seconds;
        rec.lastProgress = walk.progress;
        // THE WALK IS PLACED UNDER COVER ON THE CADENCE'S CLOCK TOO. Interrupted before the
        // passage reached its own middle, the placement never happened at all and the pass landed
        // on a PREDICTED arriving box rather than a measured one. The compressed clock crosses that
        // threshold on its way to the door, so the destination is measured before it is landed on.
        placeUnderCover(rec, walk.seconds);
        playFrame(rec, walk.seconds, walk.progress, dt, walk.handles);
        if (walk.u >= 1) cadenceEnd(rec, "on its own envelope");
        return;
      }
      // A RACE `cancel` CANNOT WIN BY ITSELF (found under load, `tests/test_pass_seam.py`'s own
      // liquid real-pair cadence row reading `cadence: null` — not late, not cut short, never
      // started). `st.settle` (every `pass-inst-*.js`'s own `if (st.progress >= 1 && !st.pinned)
      // st.settle(st.token)`) fires from INSIDE this same frame the moment `progress` first reads
      // 1, and it is reachable from here whether or not this transaction has drawn a single LIVE
      // frame before it. `progress` is read off the wall clock (`now - rec.t0`) rather than off
      // frames drawn, on purpose (A5's own reasoning: a late frame catches up rather than replaying
      // in slow motion) — but a `requestAnimationFrame` callback can itself arrive arbitrarily late
      // (a backgrounded tab, this file's own render thread starved by whatever else the process is
      // doing), and when the FIRST live frame back from such a gap already reads `progress: 1`, the
      // transaction reaches its own door in one step with no frame ever having stood between the
      // two — which is exactly the jump this whole cadence machinery exists to smooth over for an
      // interruption, and `cancel` has no way to win a race against a `requestAnimationFrame`
      // callback that the browser was already about to run: once both are queued, which one the
      // browser runs first is not this file's to decide.
      //
      // So the door is walked here instead of asked for: a transaction that reaches `progress: 1`
      // having never drawn a frame strictly between its own two doors is landed through the SAME
      // cadence an explicit interruption gets (`landState: "docked"`, the one `settle`'s own
      // off-rest branch already uses for a natural landing that still owes its camera a flight) —
      // not a new number: `midflightSeen` is a fact this record already has the frames to answer,
      // never a magnitude compared against one. A pinned bench clock (`pinProgress`) is untouched:
      // pinning stands for a test naming the exact instant it wants photographed, not for a
      // passage that was actually away.
      if (pinProgress === null && progress >= 1 && !rec.midflightSeen && rec.duration > 0
          && rec.inst && rec.inst.manifest) {
        cadenceStart(rec, "reached its door with no frame ever drawn between them", false, "docked");
        return;
      }
      if (progress > 0 && progress < 1) rec.midflightSeen = true;
      rec.lastSeconds = seconds;
      rec.lastProgress = progress;
      placeUnderCover(rec, seconds);
      playFrame(rec, seconds, progress, dt, null);
    } catch (e) {
      logEvt("frame-threw", rec.cmd.gen, String((e && e.message) || e));
      fail(rec.cmd.gen, "frame threw");
    }
  }

  // offer(cmd, hooks) — the ONE bridge the bundle calls. Returns true the moment the host has taken
  // responsibility for landing this command, whether by eventually taking over or by calling the
  // glide hook itself on decline; it never means a renderer is now drawing.
  // THE COMMAND WAITS FOR ITS OWN INSTRUMENTS, HOWEVER LONG THAT TAKES. Every instrument a score
  // names is fetched at the address the site's record gives its name, and a command whose
  // instruments are all in hand goes on at once, by the road below, unchanged. A command still
  // waiting on a file waits until `whenNamedLoaded` calls back, which it always does — on real
  // success or on any definitive failure (bad status, digest mismatch, refused registration,
  // network error all flow through the same landing). Nothing is on the screen yet either way — the
  // curtain goes up after prepare — so there is no still frame to protect against; there is only the
  // glide that runs on genuine failure, which the callback below still triggers exactly as before.
  //
  // ONE CONNECTION `whenNamedLoaded` CANNOT RING BACK FROM: dead air — a request that neither lands
  // nor fails, ever, because the network never answers at all (fetch has no floor of its own for
  // this). DEAD_AIR_MS below is not a second load budget brought back under another name: every
  // number that second-guessed a normal load is gone, on purpose, and this is not one of them. It
  // sits in "this connection is broken" territory, not "this connection is slow" territory, and it
  // exists only so a visit stuck behind a dead socket eventually reads as broken instead of pulsing
  // forever. It is not offered through host.configure — nothing legitimate ever needs to move it.
  // UNJUSTIFIED — how long a request may neither land nor fail before the visit reads it as a
  // broken connection. This file chose twenty-five seconds; nothing measured it, and the sentence
  // above says only what the number is FOR, which is not the same as what it should be.
  var DEAD_AIR_MS = 25000;
  var offeredGen = 0;
  var awaiting = null;      // the command held while its files cross the network, and its own gen
  function offer(cmd, hooks) {
    // NO COMMAND IS NOTHING TO OFFER. Every road past this point — the synchronous take below, the
    // awaited-instruments branch, and everything offerNow does once it has taken the transaction —
    // reads cmd.gen unguarded, because a real declare() always hands back a real command; only a
    // caller mistake (or a declare() that itself declined) could pass null through. Refused here,
    // the same way an unrecognised instrument or an empty voice stack is refused inside offerNow,
    // rather than reaching one of those unguarded reads and taking the whole session down with it.
    if (!cmd) return false;
    offeredGen = cmd.gen;
    var waiting = warmFor(cmd);
    if (!waiting) return offerNow(cmd, hooks);
    // A HELD COMMAND IS NOT AN IDLE HOST, and the diagnostic surface says so: `state` reads
    // «awaiting» for as long as the files are in the air. A surface that read «idle» here would
    // tell a reader the transaction had finished when it had not begun.
    awaiting = { gen: cmd.gen, names: waiting };
    logEvt("instruments-awaited", cmd.gen, waiting + " of the score's instruments");
    var rung = false;
    function release() { if (awaiting && awaiting.gen === cmd.gen) awaiting = null; }
    var deadAir = setTimeout(function () {
      if (rung) return;
      rung = true;
      release();
      // Not a decline, not a refusal — the request itself never came back, which is its own reason
      // and reads differently on the surface from every other road through this file.
      logEvt("instruments-dead-air", cmd.gen, "no answer after " + DEAD_AIR_MS
             + "ms — the load request itself never resolved");
      if (cmd.gen !== offeredGen) return;
      var why = "dead air: no answer after " + DEAD_AIR_MS + "ms";
      if (!cmd.__lastResortTried) {
        var cast = lastResortCast(cmd);
        if (cast) {
          var rescued = mergeLastResort(cmd, cast);
          logEvt("declined", cmd.gen, why + " — casting the last resort");
          if (offerNow(rescued, hooks)) return;
        }
      }
      try { hooks.mark("host-declined", cmd, why); } catch (e) {}
      try { hooks.glide(cmd); } catch (e) {}
    }, DEAD_AIR_MS);
    whenNamedLoaded(cmd, function () {
      if (rung) return;
      rung = true;
      clearTimeout(deadAir);
      release();
      // A newer declare has superseded this one, and the newer command owns its own landing. Running
      // a glide for the command that was superseded would move the walk twice.
      if (cmd.gen !== offeredGen) { logEvt("offer-superseded", cmd.gen, null); return; }
      if (!offerNow(cmd, hooks)) {
        try { hooks.mark("host-declined", cmd, "no instrument could be cast, even the last resort"); } catch (e) {}
        try { hooks.glide(cmd); } catch (e) {}
      }
    });
    return true;
  }

  function offerNow(cmd, hooks) {
    // ---- A SWIPE FOLDS THE RUNNING CROSSING UP; IT NEVER CUTS IT (§2.5 / charter shelf 19) -------
    // The nineteenth shelf makes every plan exhale-able from any point, and names a swipe as the
    // first interruption it means: the crossing COMPRESSES TO ITS CADENCE, every voice resolving to
    // neutral through the same envelopes, inside the score's own bound. Every other surface already
    // reached that road — a zoom, a quiz, the door, the Back arrow all call `cancel(reason)` with no
    // `immediate` and the cadence walks. A supersede was the one road that did not: it collapsed the
    // budget to nothing and put every handle ON its door in one frame.
    //
    // THE REASON THE SHORTCUT EXISTED IS ANSWERED HERE RATHER THAN IGNORED. It was that the next
    // command is already on its way and the product's declare is synchronous, so there was nowhere
    // to put it while the cadence played. There is now: the host holds it. `offer` has already
    // returned `true` to the walk, which is the word this file has always given for «I have taken
    // responsibility for landing this command» — so the walk goes no further, nothing else declares,
    // and the command waits exactly as long as the fold takes and no longer.
    //
    // AND THE FOLD COSTS THE ARRIVING CROSSING NO TIME IT WOULD OTHERWISE HAVE SPENT. The one part
    // of a takeover that touches nothing shared is the decode of the two photographs, and it is
    // started here, on the held command, at the instant the fold begins — so the pictures cross the
    // decode while the picture on screen resolves. Everything past that point — prepare, the texture
    // upload, the programme build — writes into instruments and a stage that the folding crossing is
    // still drawing with, which is why it waits for the fold and not the other way round.
    //
    // A SECOND SWIPE INSIDE THE FOLD REPLACES THE HELD COMMAND rather than starting a second fold:
    // the newer declare owns its own landing, the same law `offer-superseded` already reads by, and
    // one crossing folding up is one cadence however many gestures arrive while it plays.
    if (foldHeld) {
      logEvt("fold-superseded", foldHeld.cmd.gen, "held command replaced by gen " + cmd.gen);
      foldHeld = { cmd: cmd, hooks: hooks };
      return true;
    }
    // The fold road is taken only where there is something to walk and time to walk it in: a running
    // transaction, an instrument that draws (one without a manifest has no handle and no door), no
    // cadence already playing, and a score naming a budget. A score naming none clamps to zero at
    // `budgetOf`, and a zero budget IS the one-frame placement — so a pair whose score asks for no
    // cadence keeps exactly the landing it had.
    if (cur && !cur.docked && !cur.cadence && cur.state === "running"
        && cur.inst && cur.inst.manifest && budgetOf(cur.cmd) > 0) {
      foldHeld = { cmd: cmd, hooks: hooks };
      // the arriving pair's two photographs decode WHILE the fold plays; the rejection is swallowed
      // because this is a warm-up and never the arm — `armSources` is called again for real when the
      // held command is taken, and a picture that cannot decode is refused there, on its own road.
      try { armSources(cmd).then(null, function () {}); } catch (e) {}
      cancel("superseded");
      // A CUE NAMING NO PAIR OF DOORS HAS NOTHING TO WALK TO, and holding the visitor on a still
      // picture for the length of the budget would be the stall the fold exists to avoid. The
      // cadence has already said so on its own record, so this reads its answer rather than asking
      // the question a second time.
      if (foldHeld && cur && cur.cadence && !cur.cadence.door) {
        cadenceEnd(cur, "the cue names no door to walk to");
      }
      return true;
    }
    var inst = pick(cmd);
    if (!inst) {
      // THE FIRST OF THE FUNNEL'S TWO GIVE-UP EXITS: the cue's own instrument names nothing the
      // registry carries. Cast the last resort on the two pictures the DOM already holds before
      // this reaches the plain glide.
      var castA = lastResortCast(cmd);
      if (!castA) return false;
      cmd = mergeLastResort(cmd, castA);
      inst = pick(cmd);
      if (!inst) return false;   // the last resort itself failed manifest validation — a real bug
    }
    // THE GRAPH IS WALKED BEFORE THE COMMAND IS TAKEN. A cycle, two cues claiming the camera at one
    // instant, two cues naming one instrument across a shared window, or either half of the coverage
    // law is refused here — but the refusal is a property of the STACK (`scoreShed`), so a smaller
    // stack is tried before the crossing is given up, and the last resort stands behind that.
    var no = scoreWhyNo(cmd);
    if (no) {
      var shed = scoreShed(cmd);
      if (shed) {
        logEvt("score-shed", cmd.gen, no + " — shed to " + shed.score.cues.length + " voice(s)");
        cmd = shed;
      } else {
        var castB = lastResortCast(cmd);
        if (castB) {
          logEvt("score-shed", cmd.gen, no + " — cast the last resort instead");
          cmd = mergeLastResort(cmd, castB);
        } else {
          logEvt("score-refused", cmd.gen, no);
          try { hooks.mark("host-declined", cmd, "score refused: " + no); } catch (e) {}
          try { hooks.glide(cmd); } catch (e) {}
          return true;
        }
      }
    }
    // THE JOY FLOOR, ON THE SAME ROAD §7'S RESOURCE FLOOR ALREADY TAKES. Below it the device plays
    // the floor grammar rather than a degraded miracle — and the floor grammar this file has is the
    // last resort: one programme, one pass, the two photographs the DOM already holds, cast fresh on
    // this pair at this instant. So the crossing is DEGRADED to the cheapest thing that is still a
    // crossing, and no branch here ends in none: a command that has already been rescued once is let
    // through untouched, and where the two pictures cannot even be read the ordinary funnel below
    // answers exactly as it always did.
    var floorWhy = cmd.__lastResortTried ? null : joyFloorWhy();
    if (floorWhy) {
      var castJ = lastResortCast(cmd);
      if (castJ) {
        logEvt("joy-floor", cmd.gen, floorWhy);
        cmd = mergeLastResort(cmd, castJ);
        inst = pick(cmd) || inst;
      }
    }
    if (cur) cancel("superseded", true);   // defensive: declare's own supersede already ended the
                                     // bundle's OWN bookkeeping; this keeps the host's record in step
    var duration = durationOf(cmd);
    var budget = clampNum(prepareBudgetMs, PREPARE_MIN, PREPARE_MAX);
    var slack = clampNum(settleSlackMs, SLACK_MIN, SLACK_MAX);
    var cue = cueOf(cmd);
    var voices = voicesFor(cmd);
    if (!voices) {
      // THE SECOND GIVE-UP EXIT: every voice the score names is unknown to the registry. The same
      // rescue, on the same two pictures.
      var castC = lastResortCast(cmd);
      if (!castC) return false;
      cmd = mergeLastResort(cmd, castC);
      cue = cueOf(cmd);
      voices = voicesFor(cmd);
      if (!voices) return false;
    }
    var primary = voices[0];
    for (var vi = 0; vi < voices.length; vi++) if (voices[vi].line === 0) primary = voices[vi];
    // §7's grant across the whole stack: the summed declaration at the pass's worst instant against
    // the chosen variant's budget, granted, lowered a rung, or declined.
    var asked = variantOf(cmd);
    var got = grantVariant(voices, asked);
    var variant = got.variant || asked;
    // THE LIGHTENED PLAN IS WHAT PLAYS, where the ladder had to shed a voice to fit the device.
    // His own recorded ladder puts a lighter plan with fewer voices above the plain grammar, so the
    // voices the grant kept are the ones the rest of this record is built from.
    if (got.voices && got.voices.length && got.voices.length < voices.length) {
      voices = got.voices;
      if (primary && voices.indexOf(primary) < 0) primary = voices[0];
      cue = primary && primary.cue ? primary.cue : cue;
      inst = primary && primary.inst ? primary.inst : inst;
      logEvt("plan-lightened", cmd.gen, got.lightened + " voice(s) stood down so the device can "
                                        + "carry the rest");
    }
    var rec = { cmd: cmd, hooks: hooks, inst: inst, cue: cue, variant: variant, state: "offered",
                voices: voices, primary: primary, grant: got, liveCues: [], drewLastFrame: 0,
                needsScene: voices.length > 1
                  && voices.some(function (vv) { return instrumentReadsScene(vv.inst); }),
                docked: false, watchdogT: null, duration: duration, raf: 0, t0: 0, src: null,
                frames: 0,
                said: {}, driverState: {}, lastHandles: null, lastNow: 0,
                lastSeconds: 0, lastProgress: 0,
                caps: camCaps(variant), camOwner: null, camera: null, lastPose: null, ownPose: null,
                handoffs: [], cadence: null, deadlineT: null, rest: null,
                // the two boxes, the pose each asks for, the flight's own edges, and the carry a
                // reframe leaves behind — all null until prepare has read them
                hangA: null, hangB: null, hangPoseA: null, hangPoseB: null, hangEdge: null,
                lastAnchor: null, carry: null, carryFrom: 0, placed: false,
                // whether any LIVE frame has ever been drawn strictly between the two doors
                // (0 < progress < 1) — see `runFrame`'s own note over the check that reads it
                midflightSeen: false };
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
    var budgetTimer = null;
    // A5 (P1.1): the instrument's own prepare budget is armed once the pictures are actually ready
    // to hand it, never before — see the note over `armSources(cmd).then(...)` below for why.
    function armPrepareTimer() {
      budgetTimer = setTimeout(function () {
        if (answered || cur !== rec) return;
        answered = true;
        logEvt("prepare-timeout", cmd.gen, "over " + budget + "ms");
        declineCurrent(rec, "prepare timeout");
      }, budget);
    }

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
            x.manifest.passes.forEach(function (pass) { programFor(pass, x); });
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
        // A first frame may refuse the transaction itself (for example when the entry-door proof
        // sees a camera pose that cannot keep A whole). `fail` has already handed the DOM back and
        // hidden this canvas; never make that released canvas visible again underneath the landing.
        if (cur !== rec || rec.docked) return;
        stageShow(true);
        runFrame(rec, performance.now());
      }
      rec.watchdogT = setTimeout(function () { watchdogFire(rec); }, duration + slack);
    }

    // EVERY INSTRUMENT THE SCORE NAMES IS PREPARED, each on its own cue and its own grant. A voice
    // whose instrument declines, throws, or rejects at prepare is SHED rather than refusing the
    // whole command (2026-08-24) — the same lightening `grantVariant` already runs for a slow
    // device now runs for an instrument that simply would not take its cue. Only losing every voice
    // this way still gives the command up.
    function ask() {
      try {
        var answers = voices.map(function (v) {
          try {
            return v.inst.prepare({ cmd: cmd, token: cmd.gen, duration: duration, budgetMs: budget,
                                    score: cmd.score || null, cue: v.cue, variant: variant,
                                    sources: rec.src,
                                    grant: cueDeclares(v.cue, v.inst, variant) });
          } catch (e) {
            return { take: false, why: "threw: " + String((e && e.message) || e) };
          }
        });
        var thenable = answers.some(function (r) { return r && typeof r.then === "function"; });
        if (thenable) {
          Promise.all(answers.map(function (r) {
            return Promise.resolve(r).then(function (a) { return a; }, function (e) {
              return { take: false, why: "prepare rejected: " + String((e && e.message) || e) };
            });
          })).then(function (all) { onAnswer(resolveVoices(all)); });
        } else {
          onAnswer(resolveVoices(answers));
        }
      } catch (e) {
        if (!answered) { answered = true; clearTimeout(budgetTimer); declineCurrent(rec, "prepare threw"); }
      }
    }
    function resolveVoices(all) {
      var kept = [], shedWhy = [], i;
      for (i = 0; i < all.length; i++) {
        var r = all[i];
        if (r && r.take === true) kept.push(voices[i]);
        else shedWhy.push(voices[i].inst.name + ": " + ((r && r.why) || "declined"));
      }
      if (!kept.length) return { take: false, why: shedWhy.join("; ") || "declined" };
      if (kept.length < voices.length) {
        logEvt("voice-shed", cmd.gen, shedWhy.join("; "));
        voices = kept;
        if (primary && voices.indexOf(primary) < 0) primary = voices[0];
        cue = primary && primary.cue ? primary.cue : cue;
        inst = primary && primary.inst ? primary.inst : inst;
        rec.voices = voices; rec.primary = primary; rec.cue = cue; rec.inst = inst;
      }
      return { take: true };
    }

    // The host owns every FrameSource and decodes both works during prepare, so an instrument that
    // takes a command receives sources already decoded (§4.1/§10.1).
    //
    // A5 (P1.1): THE PICTURES ARE WAITED FOR ON THEIR OWN CLOCK, never the instrument's compute
    // budget. `prepareBudgetMs` (120ms by default) used to start the instant this record was made
    // and govern BOTH halves of getting a crossing on screen — the instrument's own `prepare()`
    // (local, compute-bound) AND `armSources`'s image decode (network-bound: `decodeOf` waits on
    // `img.decode()`, which itself waits on the fetch) — so a newly-in-view photograph that simply
    // had not finished downloading yet timed out exactly as a slow instrument would, and
    // `declineCurrent` fell the crossing to the plain glide. The glide is a DOM-level crossfade of
    // the two `<img>` elements themselves, so falling to it exposes whatever those elements are
    // doing on their own — including the per-work loading plate `06-ground-load-doorwarm.js` arms
    // on exactly this condition (a newly-in-view image still in flight), which is how a network
    // wait for one photograph turned into visible "loading" chrome mid-route (the invariant this
    // наряд's A5 is named for: no loading UI inside a live route).
    //
    // The fix holds instead of dropping: the wait for the pictures is bounded by the SAME outer
    // arithmetic the transaction's own watchdog already answers to once running (`duration + slack`,
    // both already-clamped values — no new numeric constant), so a genuinely stalled fetch still
    // gives the crossing up rather than holding the door open forever, while an ordinary network
    // wait — the common case this bug actually fired on — no longer races the instrument's own much
    // shorter compute budget at all. The instrument's `prepareBudgetMs` starts only once the
    // pictures are actually in hand, exactly as before for every score whose pictures were already
    // warm (prewarm/preload already make that the common case, so this changes nothing there).
    if (inst.manifest) {
      var sourcesTimer = setTimeout(function () {
        if (answered || cur !== rec) return;
        answered = true;
        logEvt("sources-timeout", cmd.gen,
               "the pictures had not finished decoding within " + (duration + slack) + "ms");
        declineCurrent(rec, "sources timeout");
      }, duration + slack);
      armSources(cmd).then(function (src) {
        clearTimeout(sourcesTimer);
        if (answered || cur !== rec) return;
        rec.src = src;
        armPrepareTimer();
        ask();
      }, function (e) {
        clearTimeout(sourcesTimer);
        if (answered || cur !== rec) return;
        answered = true;
        declineCurrent(rec, String((e && e.message) || e));
      });
    } else {
      armPrepareTimer();
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
  // `immediate` collapses the envelope to nothing: every handle is put ON its door in one step
  // instead of walking there, and the record says so (`forced`).
  //
  // A SUPERSEDE NO LONGER TAKES THAT ROAD. It used to, because §2.5 wants the cadence played before
  // the next command declares and the product's declare is synchronous — there was nowhere to put
  // the arriving command while the fold played. `offerNow` now holds it (see the fold-up note there)
  // and the walked cadence is what a swipe gets. What is left for `immediate` is the case where the
  // fold has nowhere to go: a defensive supersede reaching a transaction that is ALREADY folding,
  // which ends that fold on its door rather than letting two cadences overlap on one canvas.
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
      // The superseding command waiting for the crossing it superseded to fold up, by its own
      // generation — null whenever nothing is held, which is every instant outside a fold.
      held: foldHeld ? foldHeld.cmd.gen : null,
      duration: cur ? cur.duration : null,
      variant: cur ? cur.variant : null,
      prepareBudgetMs: prepareBudgetMs, settleSlackMs: settleSlackMs,
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
      // THE GRID THE STACK ABOVE WAS DRAWN ON. Live while a pass runs; after the landing it is the
      // grid that run ended on, frozen with the rest of what it left behind. A reading on the stack
      // and this pair are one passage's facts and must be read together — the census further down
      // is the live canvas and answers a different question.
      drawnOn: cur ? { buffer: W + "x" + H, dpr: dpr }
                   : (lastRun ? lastRun.drawnOn : null),
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
      // CHARTER SHELF 19's LADDER, as the device stands on it right now: which rung of the render
      // ladder its own frame times have walked it to, the scale that rung draws at, the rate each
      // kind of voice is re-read at, and the joy floor's own reason where the rungs have run out
      // (null everywhere above it). A picture that looks thin reads back to the rung that made it.
      pace: { rung: stepIx, rungs: STEPS.length, scale: STEPS[stepIx],
              miracle: 60, accompaniment: halvesAccompaniment() ? 30 : 60,
              floor: joyFloorWhy() },
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
      // WHAT THE CARRIER HAD TO DO TO KEEP THE FRAME WHOLE at the last frame drawn: how many frames
      // wide it stood, how much of the pose it could carry at that width, and the widest it is ever
      // allowed to stand. A picture that looks tighter than the plan asked for reads back to these.
      carrier: { over: cur ? (cur.camOver || 1) : null, hold: cur ? (cur.camHold || 1) : null,
                 ceiling: +reachCeiling().toFixed(6) },
      frames: { count: s.length, p95: +quantile(s, 0.95).toFixed(2), p50: +quantile(s, 0.5).toFixed(2) },
    };
  }

  var host = {
    name: "pass-host",
    offer: offer, resize: resize, cancel: cancel,
    contextLost: contextLost, contextRestored: contextRestored,
    settle: settle, fail: fail, register: register, configure: configure, report: report,
    prewarmInstruments: prewarmInstruments,
    // THE NAMES THIS HOST CAN ACTUALLY CAST, off the site's own record — the P2/P3 skew's real fix
    // (2026-08-24, named as a follow-up: the composer's own castable set should read from this
    // instead of its separately baked copy; wiring the composer to consume it is outside this file
    // and outside this pass). Until that lands, a name the composer picks that this list does not
    // carry sheds to `voicesFor`/the funnel exactly like any other unknown instrument.
    castable: function () { return record ? Object.keys(record) : []; },
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

  // WHAT A RECORD MUST SATISFY BEFORE ANY OF IT IS HELD. Every entry is judged, and ONE BAD ENTRY IS
  // SET ASIDE RATHER THAN CARRIED WHOLE (2026-08-24): a record of many instruments where one entry
  // is malformed used to refuse every address it held, leaving a visit unable to load ANY of them
  // over a single typo in one. The malformed entry alone stands unreachable — a cue naming it finds
  // no address, exactly as if the record never carried it, and `voicesFor`/the funnel already treat
  // that as a voice to shed or a last resort to cast rather than a reason to glide outright. Only a
  // record with NOTHING readable left in it still refuses whole.
  function recordWhyNo(settings) {
    var block = settings && settings.pass;
    var rows = block && block.instruments;
    if (!rows || typeof rows !== "object") return "carries no instrument record";
    var names = Object.keys(rows), out = {}, skipped = [], i, e;
    if (!names.length) return "carries an instrument record with nothing in it";
    for (i = 0; i < names.length; i++) {
      e = rows[names[i]];
      if (!e || typeof e !== "object" || typeof e.src !== "string" || !e.src
          || typeof e.version !== "string" || !e.version
          || !/^[0-9a-f]{64}$/.test(String(e.digest))) {
        skipped.push(names[i]);
        continue;
      }
      out[names[i]] = { src: e.src, version: e.version, digest: String(e.digest) };
    }
    if (!Object.keys(out).length) return "carries an instrument record with nothing readable in it";
    record = out;
    if (skipped.length) {
      logEvt("record-entry-skipped", null,
             skipped.join(", ") + ": carries no address, version and digest");
    }
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

  // A REFUSAL THAT NAMES A FACT ABOUT THE FILE ITSELF STANDS FOR THE VISIT: its bytes weigh to the
  // wrong digest, or it declares the wrong version or the wrong name — no retry changes any of
  // those, the record and the file simply disagree. Every other refusal names the WIRE instead — a
  // bad status, a dropped connection, bytes that would not run as a script — and the very same file
  // may answer cleanly a moment later, so it is retried with backoff rather than poisoned for the
  // visit (2026-08-24).
  function instLoadPermanent(why) {
    if (!why) return false;
    return /^its bytes weigh to /.test(why)
        || /^declares version /.test(why)
        || /^declares the instrument /.test(why)
        || /^declares no named instrument/.test(why)
        || /^its instrument /.test(why)
        || /^handed over nothing an instrument could be read from/.test(why);
  }
  // UNJUSTIFIED — how many times an instrument file is asked for again, and how long the first
  // wait is. Both were chosen here and nothing measured either.
  var INST_RETRY_MAX = 3, INST_RETRY_BASE_MS = 1500;
  function instRetryEligible(f) {
    return !!f && f.state === "refused" && !f.permanent && f.attempts < INST_RETRY_MAX
        && Date.now() >= f.retryAt;
  }

  // ONE INSTRUMENT, FETCHED BY THE ADDRESS THE RECORD GIVES ITS NAME. The bytes are weighed before
  // they run, and the bytes that were weighed are the bytes that run: one fetch, one digest over
  // what arrived, and the very same buffer evaluated.
  //
  // Every road ends by calling `done` exactly once with the reason, or with null when the instrument
  // is on the registry. A file that fails to arrive, fails its version, fails its digest, fails its
  // name or fails registration leaves the host without that instrument for THIS call, and a command
  // naming it finds none: `pick`/`voicesFor` shed the voice or the funnel casts the last resort. A
  // wire-level failure is retried with backoff (`instLoadPermanent`, above) up to INST_RETRY_MAX
  // times before it is treated the same as a permanent one; a genuine fact about the file, or a name
  // the record never carried at all, is never retried.
  function instLoad(name, done) {
    done = done || function () {};
    if (instruments[name]) return done(null);
    var f = files[name];
    if (f) {
      if (f.state === "asked") { f.waiting.push(done); return; }
      if (!instRetryEligible(f)) return done(f.why);
      files[name] = null;   // fall through and ask again, fresh
    }
    var road = noRoad();
    if (road) {
      files[name] = { state: "refused", src: null, version: null, waiting: [], why: road,
                      permanent: true, attempts: 1, retryAt: Infinity };
      logEvt("instrument-refused", null, name + ": " + road);
      return done(road);
    }
    var want = record && record[name];
    if (!want) {
      files[name] = { state: "refused", src: null, version: null, waiting: [],
                      why: "the site's record names no instrument by that name",
                      permanent: true, attempts: 1, retryAt: Infinity };
      logEvt("instrument-refused", null, name + ": " + files[name].why);
      return done(files[name].why);
    }
    var priorAttempts = (f && f.attempts) || 0;
    var rec = { state: "asked", why: null, src: want.src, version: want.version, waiting: [done],
                permanent: false, attempts: priorAttempts + 1, retryAt: 0 };
    files[name] = rec;
    function land(why) {
      var permanent = why ? instLoadPermanent(why) : false;
      rec.state = why ? "refused" : "loaded";
      rec.why = why || null;
      rec.permanent = permanent;
      var retrying = !!why && !permanent && rec.attempts < INST_RETRY_MAX;
      rec.retryAt = retrying ? Date.now() + INST_RETRY_BASE_MS * Math.pow(2, rec.attempts - 1) : Infinity;
      logEvt(why ? "instrument-refused" : "instrument-loaded", null,
             name + " (" + want.src + ")" + (why ? ": " + why + (retrying ? " — retrying" : "")
                                                  : " v" + want.version));
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

  // PREWARM (2026-08-21): asked for by NO command, only by a caller that believes a real command is
  // coming — the bundle's own head-start layer, never a stored table of what usually plays. The same
  // dedup `warmFor` already leans on (`instLoad` refuses to ask twice, and a name once refused stays
  // refused for the visit) is what makes an over-eager guess free: a name this prewarm asked for that
  // the real command never ends up naming just sits on the registry unused, and a name it guessed
  // right about is the wait `offer` would otherwise have spent, already gone.
  function prewarmInstruments(names) {
    var i, n;
    for (i = 0; i < (names || []).length; i++) {
      n = String(names[i] || "");
      if (n && !instruments[n] && (!files[n] || instRetryEligible(files[n]))) instLoad(n);
    }
  }

  // WHAT A COMMAND NAMES AND THIS HOST DOES NOT HOLD IS ASKED FOR HERE, and the count of what is
  // still in the air is handed back so the caller knows whether to wait. A name already asked for is
  // not asked for twice; a name refused for a fact about the file stays refused for the visit, but a
  // wire-level refusal is retried once its backoff has elapsed (`instRetryEligible`) rather than
  // treated as settled forever.
  function warmFor(cmd) {
    var names = namedBy(cmd), waiting = 0, i, id;
    for (i = 0; i < names.length; i++) {
      id = names[i];
      if (instruments[id]) continue;
      if (!files[id] || instRetryEligible(files[id])) instLoad(id);
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
  // REGISTERED FOR REAL USE, NOT ONLY FOR DIAGNOSTICS, AND UNCONDITIONALLY: the one thing that must
  // stand before any score has ever been read, so a cold visit's very first crossing — the
  // instruments registry still empty either way the record settled — has something to cast.
  register(makeLastResortInstrument());
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
        inst.manifest.passes.forEach(function (pass) { programFor(pass, inst); });
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
      // THE CARRIER'S OWN REACH FOR ONE POSE, and whether the frame is covered at a given reach —
      // the very functions the frame loop calls, handed over so a conformance row reads the host's
      // own geometry rather than a copy of it made in the row. `covers` answers for a carrier of
      // `over` times the frame, so a row can ask the question the repair exists to answer both
      // before and after it: does THIS pose on THAT carrier reach every pixel of the frame.
      reach: function (pose, variant) {
        return camFit(pose, camCaps(variant || "standard"), { w: cssW, h: cssH }).over;
      },
      fit: function (pose, variant) {
        var f = camFit(pose, camCaps(variant || "standard"), { w: cssW, h: cssH });
        return { over: f.over, hold: f.hold, pose: f.pose, ceiling: reachCeiling() };
      },
      covers: function (pose, variant, over) {
        var k = (typeof over === "number" && over > 0) ? over : 1;
        return quadCovers(camQuad(pose, camCaps(variant || "standard"),
                                  cssW * k / 2, cssH * k / 2, { w: cssW, h: cssH }),
                          cssW / 2, cssH / 2);
      },
      // Where the four corners of that carrier land, in frame coordinates from the frame's centre —
      // what a row holds against the browser's own rendering of the transform string.
      quad: function (pose, variant, over) {
        var k = (typeof over === "number" && over > 0) ? over : 1;
        return camQuad(pose, camCaps(variant || "standard"),
                       cssW * k / 2, cssH * k / 2, { w: cssW, h: cssH });
      },
      frame: function () { return { w: cssW, h: cssH, buffer: [W, H] }; },
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
