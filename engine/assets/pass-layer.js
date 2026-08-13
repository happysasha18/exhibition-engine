/*!pass-layer.js*/
// The drawing layer's own file — PassHost (PASS-API-V1 §1.2/§2/§12), the renderer's own half of the
// transition. Fetched separately so the walk's bundle stays under its byte fence; the client asks
// for this file once, only when the visualLayer setting asks for it, the device reports WebGL2, and
// the visit runs neither reduced motion nor Save-Data.
//
// This build draws NOTHING and owns no GPU object. It is the state machine
// idle → offered → armed → running → docked/recovered/cancelled → disposed, the watchdog, the
// idempotence guard, and a registry taking exactly one instrument. With no instrument registered —
// the state of every real visit today, since no production instrument has landed — every offer
// declines at once and the walk's own glide runs, exactly as the old stub's unconditional decline
// did. A TEST INSTRUMENT registers itself here, reachable only when diagnostics are on (§9's
// conformance rows are built against it — see tests/test_pass_api.py).
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

  var instrument = null;     // the ONE registered instrument (a registry taking one, §12)
  var cur = null;            // the current transaction record, or null between transactions
  var prepareBudgetMs = 120; // within PREPARE_MIN…PREPARE_MAX; overridable for testing (host.configure)
  var settleSlackMs = 300;   // within SLACK_MIN…SLACK_MAX

  function register(inst) { instrument = inst || null; }

  function durationOf(cmd) {
    var p = cmd && cmd.params && cmd.params.flightMs;
    return clampNum(p ? p.base : 0, DURATION_MIN, DURATION_MAX);
  }

  // Every exit from `running` ends in exactly one dock (§2.4/row 25/row 1) — `finish` is the single
  // place that can make that true, since it is the only place that ever sets `docked`.
  function finish(landState, why) {
    var rec = cur;
    if (!rec || rec.docked) return;
    rec.docked = true;
    clearTimeout(rec.watchdogT);
    logEvt(landState, rec.cmd.gen, why || null);
    try { rec.hooks.curtain(false); } catch (e) {}
    try { rec.hooks.dock(rec.cmd); } catch (e) {}
    try { rec.hooks.mark("host-" + landState, rec.cmd, why || null); } catch (e) {}
    try { if (instrument && instrument.dispose) instrument.dispose(); } catch (e) {}
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

  // offer(cmd, hooks) — the ONE bridge the bundle calls. Returns true the moment the host has taken
  // responsibility for landing this command, whether by eventually taking over or by calling the
  // glide hook itself on decline; it never means a renderer is now drawing.
  function offer(cmd, hooks) {
    if (!instrument) return false;
    if (cur) cancel("superseded");   // defensive: declare's own supersede already ended the bundle's
                                     // OWN bookkeeping; this keeps the host's own record in step too
    var duration = durationOf(cmd);
    var budget = clampNum(prepareBudgetMs, PREPARE_MIN, PREPARE_MAX);
    var slack = clampNum(settleSlackMs, SLACK_MIN, SLACK_MAX);
    var rec = { cmd: cmd, hooks: hooks, state: "offered", docked: false, watchdogT: null, duration: duration };
    cur = rec;
    logEvt("offer", cmd.gen, null);
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
      try { hooks.curtain(true); } catch (e) {}
      rec.state = "running";
      logEvt("running", cmd.gen, null);
      try { instrument.start(cmd.gen); }
      catch (e) { logEvt("start-threw", cmd.gen, String((e && e.message) || e)); fail(cmd.gen, "start threw"); return; }
      rec.watchdogT = setTimeout(function () { watchdogFire(rec); }, duration + slack);
    }
    try {
      var res = instrument.prepare({ cmd: cmd, token: cmd.gen, duration: duration, budgetMs: budget });
      if (res && typeof res.then === "function") {
        res.then(onAnswer, function () { onAnswer({ take: false, why: "prepare rejected" }); });
      } else {
        onAnswer(res);
      }
    } catch (e) {
      if (!answered) { answered = true; clearTimeout(budgetTimer); declineCurrent(rec, "prepare threw"); }
    }
    return true;
  }

  // cancel(reason) — an interruption (§2.2/§10.3). Before takeover it is a plain decline; armed or
  // running, §11's hard stop resolves at once (the graded interruption cadence is declared and
  // unbuilt) and lands through the SAME single dock every other exit uses.
  function cancel(reason) {
    if (!cur || cur.docked) return;
    if (cur.state === "offered") { declineCurrent(cur, reason || "cancelled"); return; }
    try { if (instrument && instrument.cancel) instrument.cancel(reason); } catch (e) {}
    finish("cancelled", reason || "cancelled");
  }

  function resize(viewport) {
    if (cur && cur.state === "running" && instrument && instrument.resize) {
      try { instrument.resize(viewport); } catch (e) {}
    }
  }
  function contextLost() {
    if (instrument && instrument.contextLost) { try { instrument.contextLost(); } catch (e) {} }
    if (cur && !cur.docked) fail(cur.cmd.gen, "context lost");
  }
  function contextRestored(resources) {
    if (instrument && instrument.contextRestored) {
      try { instrument.contextRestored(resources); } catch (e) { fail(cur ? cur.cmd.gen : null, "no rebuild"); }
    }
  }
  function configure(opts) {
    if (!opts) return;
    if (opts.prepareBudgetMs !== undefined) prepareBudgetMs = clampNum(opts.prepareBudgetMs, PREPARE_MIN, PREPARE_MAX);
    if (opts.settleSlackMs !== undefined) settleSlackMs = clampNum(opts.settleSlackMs, SLACK_MIN, SLACK_MAX);
  }
  function report() {
    return {
      state: cur ? cur.state : "idle",
      active: !!cur,
      gen: cur ? cur.cmd.gen : null,
      duration: cur ? cur.duration : null,
      prepareBudgetMs: prepareBudgetMs, settleSlackMs: settleSlackMs,
      events: log.slice(),
      instrument: instrument ? instrument.name : null,
    };
  }

  var host = {
    name: "pass-host",
    offer: offer, resize: resize, cancel: cancel,
    contextLost: contextLost, contextRestored: contextRestored,
    settle: settle, fail: fail, register: register, configure: configure, report: report,
  };

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
  }

  join(host);
})();
