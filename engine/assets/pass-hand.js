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
// verbs" and case "the chart law"). S-37 then gave the voice the rest of Requirement 37: it runs at
// rest with no hand on the work, it rides the letter a standing work can actually move, its rubato
// holds the eight-second floor at every instant, and it publishes the period and the hard cap so a
// row reads those laws off the voice. This file runs outside 01a-pass.js's own closure — it cannot
// call that file's `passHandleSpan` directly — so the client hands that very function over at join
// (`host` below), and a handle's declared `min`/`max` is read through it, out of the settings record
// the walk already holds. Nobody types the span in here and this file fetches nothing of its own.
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

  // ---- the manifest span, read through the host's own reader, never fetched and never typed in ---
  // A handle's declared `min`/`max` lives in the collection's SETTINGS RECORD, under
  // `pass.composer.manifests`, which this bundle's own `passHandleSpan` reads
  // (engine/client/01a-pass.js:1358-1368) out of a file the walk already holds. The client hands
  // that reader over at join (`host` below, called from `passHandSet`), so this file asks for
  // nothing of its own.
  //
  // WHY IT IS NOT READ OFF THE INSTRUMENT'S OWN FILE. The first shape fetched `pass-inst-unfold.js`
  // and read the two fields out of its text. That put an INSTRUMENT file on the wire for every
  // drawing visit, including one whose score names no instrument at all, and the walk's own law is
  // that a visit pays for the instruments its own passage names — measured 2026-09-04 at the merge
  // into main, where tests/test_pass_pack.py's "a drawing visit fetches the host, then only the
  // instruments its own score names" went red naming that very file. The settings record carries
  // the same two numbers and is already on the visit's bill.
  var hostSpan = null;
  function host(api) {
    hostSpan = (api && typeof api.handleSpan === "function") ? api.handleSpan : null;
  }
  // passHandleSpan("unfold", handle) — asked of the host each time rather than cached, so a settings
  // record that lands after this file does is never missed, and a handle the record does not carry
  // reads as absent rather than as a span of zero pretending to be measured.
  function passHandleSpan(instrument, handle) {
    if (instrument !== "unfold" || !hostSpan) return null;
    var h = null;
    try { h = hostSpan(instrument, handle); } catch (e) { h = null; }
    if (!h || !isFinite(+h.lo) || !isFinite(+h.hi)) return null;
    return { lo: +h.lo, hi: +h.hi, span: +h.hi - +h.lo };
  }
  function handSpan(handle) {
    var s = passHandleSpan("unfold", handle);
    return s ? s.span : 0;
  }
  // ---- the reach: one hit-test, the same one the host applies before it ever calls attach() -----
  var TARGET_SEL = ".exh-frame img.work";
  function pick(e) { return e.target && e.target.closest ? e.target.closest(TARGET_SEL) : null; }
  function now() { return performance.now(); }
  function clamp(v, lo, hi) { return Math.max(lo, Math.min(hi, v)); }

  // ---- the whisper voice (Requirement 37, standing life at rest) ---------------------------------
  //
  // IT RUNS AT REST, WITH NO HAND ANYWHERE (Requirement 37's own title, "standing life at rest",
  // and criterion 13, "micro-motion shall survive every state"). The phase is a pure function of
  // wall time and of the last arrival, so it needs no loop of its own to keep going and it is
  // running before the first pointer event ever lands. `resetPhase` greets a hand, `setGain` dims
  // the voice under a held press, and neither of them starts it.
  var breath = { t0: 0, gain: 1 };
  function resetPhase() { breath.t0 = now(); }     // arrive uses this
  function setGain(g) { breath.gain = clamp(+g || 0, 0, 1); }  // hold uses this
  var PERIOD_MS = 8000;   // Requirement 37 c1's own floor — "a period of at least 8 s"
  var RUBATO = 1 / 32;    // the depth of the wobble: the same thirty-second the amplitude carries
  // The rubato rides ONE-SIDED, out of the floor and back into it. A wobble centred on the base
  // period puts the period below the base for half of its own cycle, and the base IS the floor
  // criterion 1 names — so a two-sided wobble spends half its life under the law. This one wanders
  // between eight seconds and a thirty-second more, and the floor holds at every instant.
  function periodAt(t) {
    var wobble = 1 + RUBATO * (1 - Math.cos(((t - breath.t0) / (PERIOD_MS * 2)) * 2 * Math.PI)) / 2;
    return PERIOD_MS * wobble;
  }
  function breathPhase(t) { return ((t - breath.t0) / periodAt(t)) % 1; }
  // WHICH LETTER THE VOICE RIDES, AND WHY IT IS THE MAKING AXIS.
  //
  // U3 gave the voice `tilt`, the hinge, on Requirement 39 criterion 1's reading that hinged panels
  // breathe by a micro-hinge. On a work STANDING AT ITS DOOR that letter is frozen: walked to both
  // ends at the door, tilt, shade, depth, stagger, the panel count, the clock, the parquet's three
  // and the field each move exactly 0.000 of 255 (measured 2026-09-05 on the pass bench, printed by
  // tests/test_pass_whisper.py's own run). It is the instrument's own repair of 2026-08-13 that put
  // it there — the sheet stands square at its door at any tilt and at any second — and a voice on a
  // letter the door freezes is a work that does not breathe.
  //
  // So the standing voice rides `mix`, the making axis: Requirement 37 criterion 6, "the final
  // letter of the recipe shall be one candidate for the breath", and Requirement 39 criterion 19,
  // the making-axis verb at micro-gain. It is also what gives criterion 3's cap something to bite
  // on: the lean rides the same letter, so the eighth and the thirty-second add on one travel and
  // land under the sixth, exactly as criteria 1, 2 and 3 read together.
  function breathAmplitude() {
    var span = handSpan("mix");
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
    var span = handSpan("mix");
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
  // keeps). This list is the one thing this file ever writes through; a third entry here is the
  // defect S-38's row exists to catch.
  //
  // THE BREATH RIDES UNDER THE HAND'S OWN READING ON THE SAME LETTER (Requirement 37 criterion 13,
  // "micro-motion shall survive every state, the held press included"). At rest the hand's reading
  // is zero and what the frame carries is the breath alone, which is Requirement 37's own title;
  // under a held press the breath is at a quarter of itself, because `breathValue` already carries
  // the gain hold sets. Before this the voice was computed and reported and reached no handle at
  // all, so a standing work stood still — S-37's own defect.
  //
  // AND THE HARD CAP (criterion 3): "combined instantaneous displacement shall be hard-capped at a
  // sixth of that travel". The three fractions nest — the lean's eighth plus the breath's
  // thirty-second is five thirty-seconds of the travel, under the sixth — so the cap stands over
  // what this file plays today with room to spare, and it holds the letter a third voice would add.
  function handHandles(t) {
    var amp = breathAmplitude();
    var capTilt = handSpan("tilt") / 6;
    var capMix = handSpan("mix") / 6;
    return { mix: clamp(lean.value + breathValue(t), -capMix, capMix),
             tilt: clamp(attend.y * amp, -capTilt, capTilt) };
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
  // DERIVED — the log's own compression, drawn so equal hand steps read equal real screen change.
  // The derivation stands in tests/test_pass_hand_profile.py row 2, which measures this curve
  // against a straight-line drive on real captured frames: a search across K=1..25 found 4 the
  // clearest, most robust margin over the straight line, and 15 — the prior, un-measured constant —
  // loses to the straight line under that same bench.
  var CLOCK_K = 4;
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

  // ONE INSTANT PER REPORT. Every time-read below comes off the same `t`, so the breath's own value
  // and the letter it is written onto agree exactly rather than by a few microseconds.
  function report() {
    var t = now();
    var handles = handHandles(t);
    var ringElapsed = ring.kind ? (t - ring.startedAt) : null;
    return {
      attached: attached,
      verb: lastVerb,
      kind: kind,
      // THE VOICE. Its own block, named for the letter it rides. The five keys U3 published under
      // `tilt` keep their names here: they were always the voice's own.
      breath: {
        handle: "mix",
        span: passHandleSpan("unfold", "mix"),
        breathAmplitude: breathAmplitude(),
        breathValue: breathValue(t),
        phase: breathPhase(t),
        gain: breath.gain,
        // The voice is a pure function of wall time: it is running before the first pointer event
        // and it goes on running after the last one (Requirement 37, standing life at rest).
        running: true,
        // The period, published as the three numbers criterion 1 names, so a row reads the law off
        // the voice itself: the base, the floor the rubato never crosses, and the ceiling it
        // reaches. `periodMs` is the period this very instant is being measured on.
        period: { baseMs: PERIOD_MS, minMs: PERIOD_MS, maxMs: PERIOD_MS * (1 + RUBATO),
                  rubato: RUBATO, periodMs: periodAt(t) },
        // Criterion 3's hard cap on the letter this voice rides, in the units that letter carries.
        cap: handSpan("mix") / 6,
      },
      // The hinge, which the hand's own free point rides (Requirement 38 criterion 4's chart law).
      tilt: { span: passHandleSpan("unfold", "tilt"), cap: handSpan("tilt") / 6 },
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
         host: host, handleSpan: passHandleSpan, ringFreq: RING_FREQ,
         clockCurve: clockCurve, clockProfile: clockProfile });
})();
