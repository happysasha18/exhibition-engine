/*!pass-hand-gestures.js*/
// The darkroom's own gesture recognisers — Requirement 40's "The gestures" and "The tuning chart and
// the mouse dialect". A second host-side layer, the same shape as pass-hand.js (PASS-API's classic-
// script join): fetched separately, it installs its receiver global first and this script hands the
// join one plain object of named functions once it runs. It never writes pass-hand.js and carries no
// attachment reach test of its own — that reach is a room concern, wired wherever the room attaches
// an instrument to the visitor's own contact.
//
// THREE RECOGNISERS, ONE PER INSTRUMENT NAMED IN THIS UNIT'S BRIEF, each driving the two parameters
// Requirement 40 criterion 4 names for it:
//   fold        on livemirror — a one-contact drag places the crease; released, it snaps to the
//               nearest structural line the served record carries (criterion 5's magnet), or holds
//               exactly where the finger let go where no line exists — never a caught radius, never
//               a number this file invented past what the record measures.
//   twirl       on kaleidoscope — a circling one-contact drag: the angle travelled between two
//               samples sets `twist`, the sample's own radius about the frame's centre sets `reach`,
//               each read against the instrument's own declared span so the mapping travels with the
//               instrument rather than a copy of its numbers.
//   pinch       on droste — a two-contact spread steps `size`, an enum handle whose module (criterion
//               4's own "never an interpolation") stands at whole counts alone.
// Criterion 8's desktop translation rides the same three functions rather than a fourth: Shift+wheel
// is the pinch's own notch, a Shift-held single-pointer drag is pinch's synthetic second contact
// (the anchor stands still, the drag is the second finger's own travel), and a plain drag is the
// crease — kept out of pinch's own reach by the instrument test on `state.instrument` below, so a
// livemirror attachment never reads a modifier at all and a droste one only ever reads a plain touch
// spread or a modified one.
//
// EVERY CHANGE GOES THROUGH ONE FUNCTION, `applyChange` — criterion 11's envelope law. A continuous
// handle (centreX, centreY, twist, reach) moves at most a fixed share of its own declared span per
// call, so a target far from where a handle stands is reached over several calls and never in one;
// `settleTo` is the release-time loop that keeps calling it until the exact target is standing (the
// crease's own "lands exactly on it"). An enum handle (size) moves by its own declared step alone —
// never a fraction of one — which is criterion 4's "never an interpolation" applied through the same
// door rather than a second one.
//
// NO CLOCK ANYWHERE IN THIS FILE. Angular speed and spread are both read as a difference between two
// samples, never as a rate over wall time — the space this file works over is decided the moment
// each event fires, not the CPU's own pace delivering it, so a driven run repeats to the sample.
(function () {
  var join = window.__@@NS@@PassHandGestures;
  if (typeof join !== "function") return;

  function clamp(v, lo, hi) { return Math.max(lo, Math.min(hi, v)); }

  // ---- the three instruments' own declared handles, read once here (Requirement 38's chart law: an
  // instrument owns its mapping's target span; the numbers below are the same MIN/MAX the manifests
  // in pass-inst-livemirror.js, pass-inst-kaleidoscope.js and pass-inst-droste.js already publish) --
  var SPANS = {
    livemirror: { centreX: { lo: 0, hi: 1 }, centreY: { lo: 0, hi: 1 } },
    kaleidoscope: { twist: { lo: -1.2, hi: 1.2 }, reach: { lo: 0.12, hi: 0.5 } },
    droste: { size: { lo: 2, hi: 6, enumStep: 1 } },
  };
  var DEFAULTS = {
    livemirror: { centreX: 0.5, centreY: 0.5 },
    kaleidoscope: { twist: 0.55, reach: 0.30 },
    droste: { size: 4 },
  };

  var ENV_STEP_FRACTION = 0.35;      // ponytail: a designed slew rate, tune by feel once a room drives it for real
  var PINCH_STEP_RATIO = 1.25;       // a spread (or its drag-synthesised stand-in) growing/shrinking by this ratio is one step
  var PINCH_DRAG_STEP_PX = 40;       // the Shift-drag's own per-step travel, standing in for a real second contact's own spread

  function freshState() {
    return {
      el: null, instrument: null, record: null,
      handles: {}, spans: {}, changes: [],
      drag: null, twirl: null, pinchTouch: null, pinchDrag: null,
    };
  }
  var st = freshState();

  // THE ONE DOOR EVERY HANDLE CHANGES THROUGH (criterion 11). Continuous handles move a bounded
  // fraction of their own span per call; an enum handle moves by its own declared step. Either way
  // the change is logged, so `report()` can show that nothing here ever snapped to a value unread.
  function applyChange(handle, targetRaw) {
    var span = st.spans[handle];
    if (!span) return st.handles[handle];
    var target = clamp(targetRaw, span.lo, span.hi);
    var before = st.handles[handle];
    var after;
    if (span.enumStep) {
      after = target > before ? Math.min(target, before + span.enumStep)
            : target < before ? Math.max(target, before - span.enumStep)
            : before;
    } else {
      var maxStep = (span.hi - span.lo) * ENV_STEP_FRACTION;
      var delta = clamp(target - before, -maxStep, maxStep);
      after = before + delta;
    }
    if (after !== before) {
      st.handles[handle] = after;
      st.changes.push({ handle: handle, from: before, to: after, target: target, via: "envelope" });
    }
    return after;
  }
  // The release-time settle: calls the same door until the exact value stands, bounded so a stray
  // target (never expected past a handle's own span, already clamped by applyChange) cannot loop
  // forever.
  function settleTo(handle, targetRaw) {
    var span = st.spans[handle];
    if (!span) return;
    var target = clamp(targetRaw, span.lo, span.hi);
    var guard = 0;
    while (Math.abs(st.handles[handle] - target) > 1e-9 && guard < 200) {
      applyChange(handle, target);
      guard++;
    }
  }

  // ---- the crease's own magnet (Requirement 40 criterion 5) ------------------------------------
  // Every candidate line the served record carries, named with the axis it stands on: the region
  // line lab/build-workrecords-v1.py:92-112 writes at `structure.regions.line.{x,y}.{at,explains}`,
  // and beside it the second source `symmetry.reflection.leftOntoRight.axisX` /
  // `.topOntoBottom.axisY` (build-workrecords-v1.py:242-245) — a work's own mirror axis, carrying no
  // `explains` of its own, so a tie against a region line never wins on a share it does not measure.
  function creaseCandidates(record) {
    var out = [];
    var st4 = record && record.structure;
    var line = st4 && st4.regions && st4.regions.line;
    if (line && line.x && Number.isFinite(+line.x.at)) {
      out.push({ axis: "x", value: +line.x.at,
                 explains: Number.isFinite(+line.x.explains) ? +line.x.explains : -Infinity });
    }
    if (line && line.y && Number.isFinite(+line.y.at)) {
      out.push({ axis: "y", value: +line.y.at,
                 explains: Number.isFinite(+line.y.explains) ? +line.y.explains : -Infinity });
    }
    var refl = record && record.symmetry && record.symmetry.reflection;
    var lr = refl && refl.leftOntoRight;
    if (lr && Number.isFinite(+lr.axisX)) out.push({ axis: "x", value: +lr.axisX, explains: -Infinity });
    var tb = refl && refl.topOntoBottom;
    if (tb && Number.isFinite(+tb.axisY)) out.push({ axis: "y", value: +tb.axisY, explains: -Infinity });
    return out;
  }
  // Nearest-candidate-wins, tie broken by the higher `explains` — never a distance, never a caught
  // radius: every candidate stands, and the one nearest the finger's own release point takes it.
  function nearestCandidate(cands, p) {
    var best = null;
    cands.forEach(function (c) {
      var d = Math.abs((c.axis === "x" ? p.x : p.y) - c.value);
      if (!best || d < best.d - 1e-9
          || (Math.abs(d - best.d) <= 1e-9 && c.explains > best.explains)) {
        best = { axis: c.axis, value: c.value, explains: c.explains, d: d };
      }
    });
    return best;
  }
  function normPoint(clientX, clientY) {
    var r = st.el.getBoundingClientRect();
    return { x: clamp((clientX - r.left) / (r.width || 1), 0, 1),
             y: clamp((clientY - r.top) / (r.height || 1), 0, 1) };
  }
  function foldTrack(e) {
    var p = normPoint(e.clientX, e.clientY);
    st.drag.last = p;
    applyChange("centreX", p.x);
    applyChange("centreY", p.y);
  }
  function foldDown(e) { st.drag = { last: null }; foldTrack(e); }
  function foldMove(e) { if (st.drag) foldTrack(e); }
  function foldUp(e) {
    if (!st.drag) return;
    var p = st.drag.last || normPoint(e.clientX, e.clientY);
    var winner = nearestCandidate(creaseCandidates(st.record), p);
    var targetX = (winner && winner.axis === "x") ? winner.value : p.x;
    var targetY = (winner && winner.axis === "y") ? winner.value : p.y;
    settleTo("centreX", targetX);
    settleTo("centreY", targetY);
    st.drag = null;
  }

  // ---- the twirl (Requirement 40 criterion 4) ----------------------------------------------------
  // Angle and radius are both read about the frame's own centre — the drag places nothing, it only
  // circles — so what a sample sets is the difference from the one before it: how far the angle
  // turned (twist, span-mapped) and how far out the sample stands (reach, span-mapped).
  function angleDelta(a, b) {
    var d = a - b;
    while (d > Math.PI) d -= 2 * Math.PI;
    while (d < -Math.PI) d += 2 * Math.PI;
    return d;
  }
  function twirlDown(e) {
    var r = st.el.getBoundingClientRect();
    var cx = r.left + r.width / 2, cy = r.top + r.height / 2;
    st.twirl = { cx: cx, cy: cy, half: Math.max(1, Math.min(r.width, r.height) / 2),
                 prevAngle: Math.atan2(e.clientY - cy, e.clientX - cx) };
  }
  function twirlMove(e) {
    if (!st.twirl) return;
    var t = st.twirl;
    var dx = e.clientX - t.cx, dy = e.clientY - t.cy;
    var angle = Math.atan2(dy, dx);
    var speedNorm = clamp(Math.abs(angleDelta(angle, t.prevAngle)) / (Math.PI / 2), 0, 1);
    t.prevAngle = angle;
    var radiusNorm = clamp(Math.hypot(dx, dy) / t.half, 0, 1);
    var spanT = st.spans.twist, spanR = st.spans.reach;
    applyChange("twist", spanT.lo + speedNorm * (spanT.hi - spanT.lo));
    applyChange("reach", spanR.lo + radiusNorm * (spanR.hi - spanR.lo));
  }
  function twirlUp() { st.twirl = null; }

  // ---- the pinch (Requirement 40 criterion 4, and criterion 8's own two-finger dialect) -----------
  function touchDist(touches) {
    var a = touches[0], b = touches[1];
    return Math.hypot(a.clientX - b.clientX, a.clientY - b.clientY);
  }
  function pinchStep(dir) {
    applyChange("size", clamp(st.handles.size + dir, st.spans.size.lo, st.spans.size.hi));
  }
  function pinchTouchStart(e) {
    if (e.touches.length === 2) st.pinchTouch = { dist: touchDist(e.touches) };
  }
  function pinchTouchMove(e) {
    if (!st.pinchTouch || e.touches.length !== 2) return;
    var d = touchDist(e.touches);
    var ratio = d / (st.pinchTouch.dist || 1);
    if (ratio >= PINCH_STEP_RATIO) { pinchStep(1); st.pinchTouch.dist = d; }
    else if (ratio <= 1 / PINCH_STEP_RATIO) { pinchStep(-1); st.pinchTouch.dist = d; }
  }
  function pinchTouchEnd(e) { if (e.touches.length < 2) st.pinchTouch = null; }
  // Shift+wheel — criterion 8's own named pinch dialect. One notch, one step, sign of deltaY.
  function pinchWheel(e) {
    if (!e.shiftKey || e.ctrlKey) return;
    pinchStep(e.deltaY > 0 ? -1 : 1);
  }
  // Shift-held single-pointer drag — "the second finger": the press point is the anchor a real
  // second contact would stand at, and the drag's own travel away from it is that contact's spread.
  function pinchDragDown(e) { st.pinchDrag = { ax: e.clientX, ay: e.clientY, steps: 0 }; }
  function pinchDragMove(e) {
    if (!st.pinchDrag) return;
    if (!e.shiftKey) { st.pinchDrag = null; return; }
    var d = Math.hypot(e.clientX - st.pinchDrag.ax, e.clientY - st.pinchDrag.ay);
    var wantSteps = Math.trunc(d / PINCH_DRAG_STEP_PX);
    while (wantSteps > st.pinchDrag.steps) { pinchStep(1); st.pinchDrag.steps++; }
    while (wantSteps < st.pinchDrag.steps) { pinchStep(-1); st.pinchDrag.steps--; }
  }
  function pinchDragUp() { st.pinchDrag = null; }

  // ---- the reach: routed by instrument and, for the one-contact gestures, by the Shift key --------
  function onPointerDown(e) {
    if (!st.el) return;
    if (st.instrument === "livemirror" && !e.shiftKey) foldDown(e);
    else if (st.instrument === "kaleidoscope" && !e.shiftKey) twirlDown(e);
    else if (st.instrument === "droste" && e.shiftKey) pinchDragDown(e);
  }
  function onPointerMove(e) {
    if (st.drag) foldMove(e);
    else if (st.twirl) twirlMove(e);
    else if (st.pinchDrag) pinchDragMove(e);
    // a hover carries none of these states — this reach carries no operation for it (criterion 6)
  }
  function onPointerUp(e) {
    if (st.drag) foldUp(e);
    else if (st.twirl) twirlUp();
    else if (st.pinchDrag) pinchDragUp();
  }
  function onTouchStart(e) { if (st.instrument === "droste") pinchTouchStart(e); }
  function onTouchMove(e) { if (st.instrument === "droste") pinchTouchMove(e); }
  function onTouchEnd(e) { if (st.instrument === "droste") pinchTouchEnd(e); }
  function onWheel(e) { if (st.instrument === "droste") pinchWheel(e); }

  function detach() {
    if (st.el) {
      st.el.removeEventListener("pointerdown", onPointerDown);
      st.el.removeEventListener("touchstart", onTouchStart);
      st.el.removeEventListener("touchmove", onTouchMove);
      st.el.removeEventListener("touchend", onTouchEnd);
      st.el.removeEventListener("touchcancel", onTouchEnd);
      st.el.removeEventListener("wheel", onWheel);
    }
    window.removeEventListener("pointermove", onPointerMove);
    window.removeEventListener("pointerup", onPointerUp);
    window.removeEventListener("pointercancel", onPointerUp);
    st = freshState();
  }
  // `instrument` names which of the three recognisers this element answers to; `record` is the work
  // record the room already holds for it (or null — a work with none plays the crease's own no-line
  // reading, row 2's "the finger's own place"). NEVER calls .focus() on anything (criterion 6): the
  // attach itself moves no focus and neither does any handler above.
  function attach(el, instrument, record) {
    detach();
    if (!el || !DEFAULTS[instrument]) return;
    st.el = el;
    st.instrument = instrument;
    st.record = record || null;
    st.handles = Object.assign({}, DEFAULTS[instrument]);
    st.spans = SPANS[instrument];
    st.changes = [];
    el.addEventListener("pointerdown", onPointerDown);
    el.addEventListener("touchstart", onTouchStart, { passive: true });
    el.addEventListener("touchmove", onTouchMove, { passive: true });
    el.addEventListener("touchend", onTouchEnd, { passive: true });
    el.addEventListener("touchcancel", onTouchEnd, { passive: true });
    el.addEventListener("wheel", onWheel, { passive: true });
    window.addEventListener("pointermove", onPointerMove);
    window.addEventListener("pointerup", onPointerUp);
    window.addEventListener("pointercancel", onPointerUp);
  }
  function report() {
    return { instrument: st.instrument, handles: Object.assign({}, st.handles),
             changes: st.changes.map(function (c) { return Object.assign({}, c); }) };
  }

  join({ attach: attach, detach: detach, report: report });
})();
