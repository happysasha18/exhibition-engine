/*!pass-hand.js*/
// The hand overlay's own file — EX-HAND (Requirement 38 criterion 9), the touch affordance over the
// walk's own standing work. Fetched separately, the same shape as pass-layer.js (PASS-API's classic-
// script join): the client asks for this file once the walk lands, installs its receiver global
// first, and this script hands the join one plain object of named functions once it runs.
//
// THE REACH IS DECIDED BY THE CLIENT, NOT HERE (engine/client/01a-pass.js): its window-capture
// pointerdown listener tests `e.target.closest(".exh-frame img.work")` and calls `attach` for
// nothing else, so the threshold window, the quiz chip, the share control, the sound tray and the
// series room never reach this file at all — and it detaches on its own while the closer look
// (EX-ZOOM) covers the same picture, re-attaching the moment that layer clears. This file holds only
// the attachment itself: which work, if any, the hand currently stands on.
//
// U3 ADDS THE VOICE AND THE SIX VERBS (Requirement 37 case "the band"; Requirement 38 case "the six
// verbs" and case "the chart law"). This file runs outside 01a-pass.js's own closure — it cannot
// call that file's `passHandleSpan` directly — so it reads the same fact that function reads (a
// handle's declared `min`/`max`) off the instrument's OWN served file, `pass-inst-unfold.js`, which
// ships beside this one in every bake. Nobody types the span in here; it is read off the manifest
// text at runtime, the same two fields (`min`, `max`) `passHandleSpan` itself reads
// (engine/client/01a-pass.js:1358-1368).
//
// THERE IS NO SURFACE THAT RENDERS A STANDING WORK YET (the drawing layer only ever plays a
// crossing) — this file plays no pixel. What it computes is reported on `report()`, the one surface
// a test (or a future renderer) reads.
//
// The six verbs answer mouse and touch alike from one set of listeners, gated by the same reach
// `.exh-frame img.work` names, added and released passively (capture, no `preventDefault`) so the
// walk's own wheel/touch pagers keep sole ownership of navigation (tests/test_pass.py:83-88's law,
// held here by construction rather than by copying that file's own block).
(function () {
  var join = window.__@@NS@@PassHand;
  if (typeof join !== "function") return;

  var attached = null;   // the standing work's own id, or null — U1's own bookkeeping, unchanged

  function attach(el, workRecord) {
    attached = (workRecord && workRecord.id != null) ? workRecord.id : null;
  }
  function detach() {
    attached = null;
  }

  // ---- the manifest span, read off the instrument's own file, never typed in --------------------
  var INSTRUMENT_FILE = "pass-inst-unfold.js";
  var manifestPromise = null;
  var manifest = null;   // { tilt: {lo,hi,span}|null, mix: {lo,hi,span}|null } once loaded
  function readHandle(text, name) {
    var re = new RegExp("\\b" + name + "\\s*:\\s*\\{\\s*min\\s*:\\s*([0-9.]+)\\s*,\\s*max\\s*:\\s*([0-9.]+)");
    var m = re.exec(text);
    if (!m) return null;
    var lo = +m[1], hi = +m[2];
    return { lo: lo, hi: hi, span: hi - lo };
  }
  function loadManifest() {
    if (manifestPromise) return manifestPromise;
    manifestPromise = fetch(INSTRUMENT_FILE).then(function (r) { return r.text(); })
      .then(function (text) {
        manifest = { tilt: readHandle(text, "tilt"), mix: readHandle(text, "mix") };
      })
      .catch(function () { manifest = { tilt: null, mix: null }; });
    return manifestPromise;
  }
  // passHandleSpan("unfold", handle) — the same two fields 01a-pass.js:1358-1368 reads, read here
  // off the instrument's own served text because this file runs outside that closure.
  function passHandleSpan(instrument, handle) {
    if (instrument !== "unfold" || !manifest) return null;
    return manifest[handle] || null;
  }
  loadManifest();   // asked for the moment this file runs, so a first drag never races the fetch

  // ---- the reach: one hit-test, the same one the host applies before it ever calls attach() -----
  var TARGET_SEL = ".exh-frame img.work";
  function pick(e) { return e.target && e.target.closest ? e.target.closest(TARGET_SEL) : null; }
  function now() { return performance.now(); }
  function clamp(v, lo, hi) { return Math.max(lo, Math.min(hi, v)); }

  // ---- the whisper voice (Requirement 37 case "the band") — tilt's own resting breath -----------
  var breath = { t0: 0, gain: 1 };
  function resetPhase() { breath.t0 = now(); }     // arrive uses this
  function setGain(g) { breath.gain = clamp(+g || 0, 0, 1); }  // hold uses this
  var PERIOD_MS = 8000;   // Requirement 37 c1's own floor — "a period of at least 8 s"
  function breathPhase(t) {
    // rubato on the period: a slow wobble on the period itself, its depth the same 1/32 fraction
    // the amplitude already carries and its own timescale twice the base period — no fresh number
    // invented for the wobble.
    var wobble = 1 + (1 / 32) * Math.sin(((t - breath.t0) / (PERIOD_MS * 2)) * 2 * Math.PI);
    var period = PERIOD_MS * wobble;
    return ((t - breath.t0) / period) % 1;
  }
  function breathAmplitude() {
    var span = manifest && manifest.tilt ? manifest.tilt.span : 0;
    return span / 32;   // Requirement 37 c1 — "a thirty-second of a letter's full crossing travel"
  }
  function breathValue(t) {
    return breathAmplitude() * Math.sin(breathPhase(t) * 2 * Math.PI) * breath.gain;
  }

  // ---- the six verbs' own state ------------------------------------------------------------------
  var overWork = false;      // an unpressed mouse hover currently stands on the work
  var currentEl = null;
  var kind = null;           // e.pointerType of the live interaction, mouse or touch
  var pointerId = null;      // the one engaged pointer, or null
  var downRect = null;       // the element's own rect, read once at press, held for the gesture
  var downX = 0, downY = 0;  // the press point, normalised -1..1 within the element
  var lastMoveAt = 0;
  var lastVerb = null;
  var attend = { x: 0, y: 0, target: null, _t: 0 };
  var lean = { value: 0, engaged: false, direction: null };
  var hold = { active: false, stretch: 0, lastX: 0, lastY: 0 };
  var RING_MS = 700;               // criterion 11's own exhale bound
  var RING_FREQ = 2 / 0.700;       // criterion 9's two hinge tremors inside that bound
  var ring = { kind: null, startedAt: 0 };  // kind: "strike" | "release" | null
  var rafId = null;

  function fireVerb(name) { lastVerb = name; }
  function handOn() { return overWork || pointerId !== null; }

  function normPos(e, rect) {
    var nx = rect.width ? ((e.clientX - rect.left) / rect.width) * 2 - 1 : 0;
    var ny = rect.height ? ((e.clientY - rect.top) / rect.height) * 2 - 1 : 0;
    return { x: clamp(nx, -1, 1), y: clamp(ny, -1, 1) };
  }

  function doArrive() {
    resetPhase();
    fireVerb("arrive");
  }

  function ensureLoop() {
    if (rafId !== null) return;
    var step = function () {
      tick();
      if (handOn() || ring.kind !== null || Math.abs(lean.value) > 1e-4) {
        rafId = requestAnimationFrame(step);
      } else {
        rafId = null;
      }
    };
    rafId = requestAnimationFrame(step);
  }

  function tick() {
    loadManifest();   // idempotent — the one fetch this file ever makes
    var t = now();
    if (!attend._t) attend._t = t;
    var dt = Math.max(0, (t - attend._t) / 1000);
    attend._t = t;
    var pressed = pointerId !== null;
    // the capture/release constants, read off lab/effects/livemirror.js:360 rather than invented:
    // fast while the hand holds the point, slow once it lets go.
    var gTau = pressed ? 0.09 : 0.8;
    var k = dt > 0 ? 1 - Math.exp(-dt / gTau) : 0;
    if (attend.target) {
      attend.x += (attend.target.x - attend.x) * k;
      attend.y += (attend.target.y - attend.y) * k;
    }
    if (pressed && !hold.active && (t - lastMoveAt) >= 400) {   // Req 38 c1 hold — "about 400 ms still"
      hold.active = true;
      fireVerb("hold");
    }
    setGain(hold.active ? 0.25 : 1);   // hold dims to a residual quarter
    if (hold.active) {
      hold.stretch += Math.hypot(attend.x - hold.lastX, attend.y - hold.lastY);
      hold.lastX = attend.x; hold.lastY = attend.y;
    }
    if (!lean.engaged && lean.value !== 0) {
      // the spring return, through the matter's own ring — Requirement 37 c2's own "release of
      // about 1.2 s"
      var kl = dt > 0 ? 1 - Math.exp(-dt / 1.2) : 0;
      lean.value += (0 - lean.value) * kl;
      if (Math.abs(lean.value) < 1e-4) lean.value = 0;
    }
    if (ring.kind && (t - ring.startedAt) > RING_MS * 2) ring.kind = null;
  }

  function leanCap() {
    var span = manifest && manifest.mix ? manifest.mix.span : 0;
    return span / 8;   // Requirement 38 c1 lean — "a gain of at most an eighth of the full travel"
  }

  addEventListener("pointerover", function (e) {
    var el = pick(e);
    if (!el) return;
    currentEl = el; overWork = true; kind = e.pointerType;
    doArrive();
    ensureLoop();
  }, { capture: true, passive: true });

  addEventListener("pointerout", function (e) {
    if (pointerId !== null) return;         // an engaged pointer owns the state until it lifts
    var el = pick(e);
    if (!el || el !== currentEl) return;
    overWork = false;
  }, { capture: true, passive: true });

  addEventListener("pointerdown", function (e) {
    var el = pick(e);
    if (!el || pointerId !== null) return;  // one engaged pointer at a time — the reach is a single tap
    currentEl = el; pointerId = e.pointerId; kind = e.pointerType;
    downRect = el.getBoundingClientRect();
    var p = normPos(e, downRect);
    downX = p.x; downY = p.y; lastMoveAt = now();
    attend.target = p;
    hold.active = false; hold.stretch = 0; hold.lastX = attend.x; hold.lastY = attend.y;
    lean.engaged = true; lean.value = 0; lean.direction = null;
    if (!overWork) doArrive();              // touch's own first contact, with no prior hover
    overWork = true;
    ensureLoop();
  }, { capture: true, passive: true });

  addEventListener("pointermove", function (e) {
    var pressed = pointerId !== null;
    if (pressed && e.pointerId !== pointerId) return;
    var el = pressed ? currentEl : pick(e);
    if (!el) return;
    var rect = pressed ? downRect : el.getBoundingClientRect();
    var p = normPos(e, rect);
    attend.target = p;
    lastMoveAt = now();
    if (pressed) {
      var dx = p.x - downX;
      var travelPx = Math.abs(dx) * (rect.width / 2);
      if (travelPx >= 12) {   // the same tap/drag line 01a-pass.js:3206 already draws
        lean.value = clamp(dx * leanCap(), -leanCap(), leanCap());
        lean.direction = dx >= 0 ? "toward-source" : "into-construction";
        fireVerb("lean");
      } else {
        fireVerb("attend");
      }
      if (Math.abs(p.x - downX) > 0.02 || Math.abs(p.y - downY) > 0.02) hold.active = false;
    } else if (overWork) {
      fireVerb("attend");
    }
  }, { capture: true, passive: true });

  function endPress(e) {
    if (pointerId === null || e.pointerId !== pointerId) return;
    var wasHold = hold.active;
    var travelPx = Math.hypot((attend.target.x - downX) * (downRect.width / 2),
                               (attend.target.y - downY) * (downRect.height / 2));
    pointerId = null; lean.engaged = false; hold.active = false;
    if (!wasHold && travelPx < 12) {
      ring.kind = "strike"; ring.startedAt = now();
      fireVerb("strike");
    } else {
      ring.kind = "release"; ring.startedAt = now();
      fireVerb("release");
    }
    ensureLoop();
  }
  addEventListener("pointerup", endPress, { capture: true, passive: true });
  addEventListener("pointercancel", endPress, { capture: true, passive: true });

  // ---- the chart law (Requirement 38 case "the chart law") ---------------------------------------
  // The hand's own two-parameter field maps onto exactly two of unfold's parameters: its horizontal
  // reading onto `mix` (lean — toward the source photograph or deeper into the construction) and its
  // vertical reading onto `tilt` (attend's own free point, inside the same whisper band the breath
  // already keeps). `HAND_HANDLES` is the one list this file ever writes through; a third entry here
  // is the defect S-38's row exists to catch.
  function handHandles() {
    var tiltAmp = breathAmplitude();
    return { mix: lean.value, tilt: attend.y * tiltAmp };
  }

  // ---- the hand as clock (Requirement 40 criteria 1, 9, 10 — unit U5) ----------------------------
  // A SECOND, SEPARATE ROAD FROM THE CHART LAW ABOVE, never wired to it and never called from any
  // listener in this file: `lean`'s R/8 ceiling (Requirement 38 c1) is the shipped walk's own drag
  // and stands exactly as U3 left it. This is a pure, stateless response curve — hand position in,
  // progress out — that a caller (a conformance row today; the darkroom's own drive tomorrow) uses
  // to drive `unfold`'s progress pin (`pass-layer.js` `configure({progressPin})`) across its FULL
  // declared range. Nothing here reaches into `pass-layer.js` or any `pass-inst-*.js`; the curve is
  // read off and written into those files only by whatever calls `clockCurve`.
  //
  // THE CURVE IS THIS FILE'S OWN, drawn from criterion 10's own general law — "perception is
  // logarithmic in many dimensions" — never from `unfold`'s own internal fold response, which this
  // file never reads: there is no such reading anywhere in this file, on purpose, since the room's
  // own profile (criterion 9's own gap) has nothing proven yet to borrow from the crossing's side.
  var CLOCK_K = 15;   // the log's own compression — a plain constant of this curve, not a measurement
  function clockCurve(u) {
    u = clamp(+u || 0, 0, 1);
    return Math.log(1 + CLOCK_K * u) / Math.log(1 + CLOCK_K);
  }
  // Criterion 9's own five facts, published once and read back whole: unipolar (the clock never
  // runs backward), logarithmic (the curve above), the declared 0..1 range progress itself already
  // carries, and a neutral that is also where the hand leaves it at rest — the "in" door `unfold`'s
  // own manifest already names for `mix`.
  var CLOCK_PROFILE = { polarity: "unipolar", curve: "logarithmic",
                         range: { min: 0, max: 1 }, neutral: 0, resting: 0 };
  function clockProfile() { return CLOCK_PROFILE; }

  function report() {
    loadManifest();
    var t = now();
    var handles = handHandles();
    var ringElapsed = ring.kind ? (t - ring.startedAt) : null;
    return {
      attached: attached,
      verb: lastVerb,
      kind: kind,
      tilt: {
        span: manifest ? manifest.tilt : null,
        breathAmplitude: breathAmplitude(),
        breathValue: breathValue(t),
        phase: breathPhase(t),
        gain: breath.gain,
        running: handOn(),
      },
      hold: { active: hold.active, stretch: hold.stretch },
      lean: { value: lean.value, cap: leanCap(), direction: lean.direction, engaged: lean.engaged },
      attend: { x: attend.x, y: attend.y, target: attend.target },
      release: ring.kind === "release" ? {
        ring: ringElapsed <= RING_MS,
        resolved: ringElapsed > RING_MS,
        afterglow: ringElapsed <= RING_MS * 2,
      } : null,
      strike: ring.kind === "strike" ? { ring: ringElapsed <= RING_MS } : null,
      chart: {
        unfold: { x: { handle: "mix", value: handles.mix }, y: { handle: "tilt", value: handles.tilt } },
        moves: Object.keys(handles),
      },
    };
  }

  join({ attach: attach, detach: detach, report: report, resetPhase: resetPhase, setGain: setGain,
         handleSpan: passHandleSpan, ringFreq: RING_FREQ,
         clockCurve: clockCurve, clockProfile: clockProfile });
})();
