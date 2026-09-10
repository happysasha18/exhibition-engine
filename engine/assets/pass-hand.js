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
// S-39 PUTS THE VOICE UNDER A CONDUCTOR (Requirement 39 case "the conductor"). The gallery seats
// one work as the soloist and stills the rest, and this voice reads its own gain off that seat
// (`seatGain` below) instead of always sounding: a work the conductor has not seated writes a
// breath of zero, and while a crossing runs no work breathes at all.
//
// S-38 GIVES THE READING A SINK (`paint` below). Until it, the six verbs were computed, reported,
// and reached no pixel at all: the drawing layer plays a crossing alone, nothing on the walk read
// `report()`, and a visitor pressing a work on the served page met no answer — measured 2026-09-05
// on a staged bake of tlvphotos.com, where a tap fired `verb: "strike"` on this file's own report
// while the pressed picture's computed transform stayed `none`. The reading is now written back
// onto the picture through the SAME space it was read in: `normPos` normalises a contact to -1..1
// over the element's half-extents, so a chart value carried as a fraction of its letter's declared
// travel comes back out over those very half-extents. No number is introduced to do it — the two
// caps, the ring's bound and the ring's frequency are the ones the verbs already carry, and the
// declared spans are the manifest's, read through the host as everything else here is. `report()`
// stays the surface a test reads; it now reports a reading that reaches the frame.
//
// S-112 GIVES THE VOICE A SURFACE ON THE WALK. Beside the hand's own writing back onto the pressed
// picture, this file publishes the breath for a second reader: `engine/client/08b-standing.js` draws
// the work the conductor seated, inside the box the hang measured. The narrow door for that renderer
// is `unit()` below — the curve at its own two gains, in no letter's units — beside `voice()`, which
// is the conductor's. The two sinks share one clock: `paint()` writes the hand's reading onto the
// element under the hand, and `unit()` hands the standing renderer the same breath the voice runs on.
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
    // THE ROOT OF S-38's OWN DEFECT, STILL STANDING FOR EVERY CALLER OF THIS DOOR (measured
    // 2026-09-06): three roads call `attach` — a press, a hover (both 01a-pass.js), and the
    // zoom-close re-attach a few lines below THAT file's own MutationObserver — and until now none
    // of them repainted anything here. `attached` is bookkeeping only; `paint()` reads `currentEl`,
    // set solely by this file's OWN pointerover/pointerdown listeners below, which never re-fire on
    // a re-attach with no fresh pointer event. Proven on a real run: press a work, pinch it open,
    // Escape it closed with the mouse held still — `report().attached` names the work correctly and
    // `img.style.transform` stays "" (S-38's own defect: computed, reported, painted nowhere).
    // Fixed once here, where every caller already converges, rather than patched on each of the
    // three callers separately.
    //
    // `overWork` IS ASKED OF THE BROWSER, NOT ASSUMED (found 2026-09-06 reviewing this very fix): a
    // press and a hover call this door FROM the native event that makes it true — the pointer really
    // is on `el` this instant. The zoom-close re-attach a few lines below calls it from
    // `passHandLastEl`, a name remembered from BEFORE the closer look ever opened; nothing says the
    // pointer is still there once it closes; a mouse is free to leave while the closer look covers
    // the page and never fire a real `pointerout` for a picture it already stopped hit-testing.
    // Setting `overWork` unconditionally would paint a work the pointer had already left, and no
    // event was left behind to ever correct it — `:hover` is the one live, zero-cost answer this
    // file can ask instead of assuming. A touch press does not read `:hover` reliably; it does not
    // need to, since `handOn()` below is already `overWork || pointerId !== null`, and a genuine
    // press keeps `pointerId` set through this file's OWN `pointerdown` handler regardless of what
    // this line decides.
    if (!el) return;
    currentEl = el;
    try { overWork = el.matches(":hover"); } catch (e) { overWork = true; }
    ensureLoop();
  }
  function detach() {
    attached = null;
    // S-38: the host detaches while the closer look covers this very picture. The reading may still
    // be standing on it, so the picture is handed back before the hand lets go of it — otherwise a
    // work would sit off its rest under a layer that owns the whole viewport.
    unpaint();
    currentEl = null; overWork = false;
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
  var hostSeat = null;
  var hostMatter = null;
  var hostInstrument = null;
  function host(api) {
    hostSpan = (api && typeof api.handleSpan === "function") ? api.handleSpan : null;
    hostSeat = (api && typeof api.seatRegister === "function") ? api.seatRegister : null;
    hostMatter = (api && typeof api.matterInHand === "function") ? api.matterInHand : null;
    hostInstrument = (api && typeof api.matterInstrument === "function") ? api.matterInstrument : null;
  }
  // THE INSTRUMENT ACTUALLY STANDING THERE, read fresh off the host rather than assumed: whatever
  // last drew (or is drawing now), by its own name. Before any crossing has ever played the host
  // knows nothing yet, and "unfold" is what this file has always asked for in that silence, so that
  // one case keeps reading exactly as it did before this fallback existed.
  function currentInstrument() {
    var got = null;
    try { got = hostInstrument ? hostInstrument() : null; } catch (e) { got = null; }
    return (typeof got === "string" && got) ? got : "unfold";
  }
  // passHandleSpan(instrument, handle) — asked of the host each time rather than cached, so a
  // settings record that lands after this file does is never missed, and a handle the record does
  // not carry reads as absent rather than as a span of zero pretending to be measured.
  function passHandleSpan(instrument, handle) {
    if (!hostSpan) return null;
    var h = null;
    try { h = hostSpan(instrument, handle); } catch (e) { h = null; }
    if (!h || !isFinite(+h.lo) || !isFinite(+h.hi)) return null;
    return { lo: +h.lo, hi: +h.hi, span: +h.hi - +h.lo };
  }
  function handSpan(handle) {
    var s = passHandleSpan(currentInstrument(), handle);
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
  // running before the first pointer event ever lands. Arrival does not re-clock it: a picture may
  // be attached again when an overlay clears or a pointer crosses its surface, and restarting the
  // eight-second curve there reads as a visible jerk rather than a living response. `setGain` dims
  // the voice under a held press, and neither starts or re-clocks it.
  var breath = { t0: 0, gain: 1 };
  function setGain(g) { breath.gain = clamp(+g || 0, 0, 1); }  // hold uses this
  // The residual quarter-breath, Requirement 38 criterion 1's own hold verb — "self-life dims to a
  // residual quarter-breath". Named once here and read twice: by `hold` below, and by the seat, for
  // whom it is Requirement 39 criterion 15's "cheapest register". Every gain the voice plays is
  // this file's, so the conductor names registers and carries no number of its own.
  // DERIVED — a quarter is the word Requirement 38 criterion 1 uses for what hold leaves running,
  // and this is that word written as a fraction; nothing measured it and nothing tuned it.
  var RESIDUAL = 0.25;
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
  // THE SEAT, WHICH DECIDES WHETHER THIS VOICE SOUNDS AT ALL (Requirement 39 case "the conductor").
  // The gallery conductor (`engine/client/08a-conductor.js`) seats one work as the soloist at full
  // whisper, at most two neighbours at the cheapest register, and everything else at a register with
  // no voice — a work in view standing as a still, a work outside the viewport paused. It hands this
  // file the register through `host` above, and the register becomes the gain here, because every
  // gain the voice plays is this file's own. A host that hands over no seat — an older bundle, or a
  // bench driving this file alone — reads as the soloist's, which is exactly what this voice played
  // before the conductor existed.
  function seatGain() {
    if (!hostSeat) return 1;
    var register = null;
    try { register = hostSeat(); } catch (e) { register = null; }
    if (register === "neighbour") return RESIDUAL;
    if (register === "still" || register === "paused") return 0;
    return 1;
  }
  // THE CURVE ITSELF, at its own two gains and in no letter's units: the sine of the phase, dimmed
  // by the hold and by the seat. One home for the shape of the breath, read twice — by the value
  // below, which puts it on the letter it rides, and by the standing renderer
  // (engine/client/08b-standing.js), which puts it on the work the conductor seated. A renderer
  // reading `breathValue` instead would have to divide by an amplitude that is nil wherever the
  // settings record declares no span for the letter, so it would go silent for a reason that has
  // nothing to do with whether the work is breathing.
  function breathUnit(t) {
    return Math.sin(breathPhase(t) * 2 * Math.PI) * breath.gain * seatGain();
  }
  function breathValue(t) {
    return breathAmplitude() * breathUnit(t);
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
  // ---- the ring, which is the matter's own (Requirement 37 criteria 9 to 11) ---------------------
  //
  // "Every matter shall own one impulse response", and criterion 11 makes the impulse-response table
  // "the one home of the curve". That table exists now — `engine/assets/matter-response.json`, plan
  // row S-40 — with one row per family carrying the shape its criterion words and the number of
  // cycles its criterion counts. So the count is READ from the family in hand rather than typed
  // here, and a family that rings differently rings differently: hinged panels ring two tremors,
  // yarn one slow shiver, the corridor's shudder counts none at all.
  //
  // The bound stays where it already was. Criterion 11's 700 ms exhale is `RING_MS` above, and the
  // table's own `ring` column says so in as many words — "a family's ring frequency is its own
  // cycles over that bound, so the count lives here and the bound stays where it already was". A
  // frequency is the one over the other, and neither number is written twice.
  //
  // WHICH FAMILY IS IN HAND. The host answers (`matterInHand`, 01a-pass.js), off the drawing layer's
  // own report of the instrument the crossing in flight cast — the one place the engine says out
  // loud what matter is being drawn. THREE ROADS ANSWER NOTHING, and all three fall back to the same
  // row: a walk at rest, where no instrument is drawing and a standing work names no family; an
  // instrument the table names in no row, of which `unfold` — the letter this file's own voice rides
  // — is one; and a bake that serves no table at all.
  //
  // THE FALLBACK IS THE HINGED PANELS' ROW, and it is the honest one rather than a neutral invented
  // for the occasion: the count that stood in this file before the table existed was that family's
  // own two tremors, so a work whose family is not determined rings exactly as every work rang
  // before this hand-off, and nothing that already shipped moves. It is named here by matter rather
  // than by number, so the day the table gives hinged panels a different count, the fallback follows
  // it too. A table that carries no such row leaves the frequency unread, and a reader is told so.
  var RING_FALLBACK = "hinged panels";
  function matterRow(name) {
    if (!hostMatter) return null;
    try { return hostMatter(name) || null; } catch (e) { return null; }
  }
  function ringRow() {
    var row = matterRow();
    if (row && row.ring) return { matter: row.matter, ring: row.ring, determined: true };
    var back = matterRow(RING_FALLBACK);
    return { matter: RING_FALLBACK, ring: back && back.ring ? back.ring : null, determined: false };
  }
  // The frequency criterion 9 asks for: the family's own cycles inside criterion 11's own bound. A
  // family whose criterion counts no cycles (the corridor's receding shudder) has no frequency to
  // publish, and this answers null rather than standing a number in for a count nobody made.
  function ringFreq() {
    var row = ringRow();
    var cycles = row.ring && Number(row.ring.cycles);
    return (row.ring && row.ring.cycles != null && isFinite(cycles))
      ? cycles / (RING_MS / 1000) : null;
  }
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
    // Arrival is an interaction verb, not the beginning of a new ambient loop.  Keeping the one
    // wall-clock phase is what makes a re-attach and a finger arriving mid-cycle feel continuous.
    fireVerb("arrive");
  }

  function ensureLoop() {
    if (rafId !== null) return;
    var step = function () {
      tick();
      paint();
      // The free point eases home once the hand leaves (`pointerout` below), so the loop has to
      // outlive the hand by that ease — otherwise it stops on a work still held off its rest and
      // `paint`'s own clear becomes a snap the visitor sees.
      if (handOn() || ring.kind !== null || Math.abs(lean.value) > 1e-4
          || Math.abs(attend.x) > 1e-3 || Math.abs(attend.y) > 1e-3) {
        rafId = requestAnimationFrame(step);
      } else {
        rafId = null;
        unpaint();
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
    setGain(hold.active ? RESIDUAL : 1);   // hold dims to a residual quarter
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
    // The free point goes home the way the lean already does — over the release time constant
    // `tick` reads for an unpressed hand — so a work the hand leaves settles rather than snapping
    // back the instant the loop lets go of it. Touch reaches this too: a lifted touch pointer fires
    // `pointerout` right behind its own `pointerup`.
    attend.target = { x: 0, y: 0 };
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
  //
  // THE RING RIDES THE HINGE (criterion 9's "two hinge tremors", criterion 11's 700 ms exhale
  // bound). Both are already named above, the bound as `RING_MS` and the rate as `ringFreq()`, which
  // S-112 turned from a typed constant into the matter table's own row; the tremor's own size is the
  // breath's, because every amplitude this file plays is the breath's thirty-second, and it decays
  // linearly to nothing exactly at the bound rather than trailing past it. Nothing new is measured
  // or chosen here. Before S-38 the ring was a pair of booleans on `report()` and reached nothing,
  // so a tap on a work — strike, the one verb with no travel of its own — was felt as no answer.
  function ringValue(t) {
    if (!ring.kind) return 0;
    var e = (t - ring.startedAt) / RING_MS;
    if (e < 0 || e > 1) return 0;
    // The frequency is the matter table's own, through `ringFreq()` above — the family's cycles
    // inside criterion 11's bound. A family whose criterion counts no cycles publishes no frequency,
    // and a tremor at an unnamed rate would be a number this file invented, so it plays none.
    var freq = ringFreq();
    if (freq == null || !isFinite(freq)) return 0;
    return breathAmplitude() * (1 - e) * Math.sin(2 * Math.PI * freq * (t - ring.startedAt) / 1000);
  }
  function handHandles(t) {
    var amp = breathAmplitude();
    var capTilt = handSpan("tilt") / 6;
    var capMix = handSpan("mix") / 6;
    // 2026-09-06, measured live at 1440x900 (CDP input, img.work.style.transform): a plain hover
    // painted only 0.012 of the frame's width, next to a press-and-drag's 0.054 — because mix's
    // own driver, `lean`, answers a press alone, and a hover's mix carried nothing but the breath.
    // Attend's free point already rides `tilt` on its y (below); the same point's x now rides
    // `mix` too, at the SAME amp the breath already plays there, gated to zero while `lean` is
    // engaged so a press keeps summing exactly `lean.value + breathValue` as it always has. A
    // hover now reads ~0.027, about half the press reach, through this file's own attend/lean verbs.
    // His word 2026-09-10 20:45: the mouse should change the work a little, the way a touch does
    // on a phone. A hover rode the breath's own thirty-second, which painted 0.014 of the frame's
    // width at the far edge — under what the hand can feel (row 19's floor of 0.02). It now rides
    // half the lean's own eighth on both axes: a hover reaches half of what a press reaches, on
    // the same two letters the press moves, and the press keeps summing exactly as it did.
    var hoverAmp = lean.engaged ? 0 : leanCap() / 2;
    var hoverTilt = handSpan("tilt") / 16;
    var hoverMix = attend.x * hoverAmp;
    return { mix: clamp(lean.value + hoverMix + breathValue(t), -capMix, capMix),
             tilt: clamp(attend.y * hoverTilt + ringValue(t), -capTilt, capTilt) };
  }

  // ---- the sink: the reading, written onto the picture the hand stands on ------------------------
  // The hinge carries the free point's thirty-second and the ring's thirty-second, a sixteenth of
  // the travel together, so criterion 3's sixth still stands over both with room, exactly as it
  // does over the lean's eighth plus the breath's thirty-second on the making axis.
  //
  // A visitor who asked for less motion gets none of it: the reading goes on being computed and
  // reported, and only the write is skipped, so a row reads the same verbs either way.
  var reduce;
  function still() {
    if (reduce === undefined) {
      try { reduce = matchMedia("(prefers-reduced-motion: reduce)"); } catch (e) { reduce = null; }
    }
    return !!(reduce && reduce.matches);
  }
  var painted = null;
  function paint() {
    var el = currentEl;
    if (!el) return;
    if (still()) { unpaint(); return; }
    var t = now();
    var h = handHandles(t);
    var sMix = passHandleSpan(currentInstrument(), "mix"), sTilt = passHandleSpan(currentInstrument(), "tilt");
    // Read fresh rather than off `downRect`: that rect belongs to a press, and a hover arrives with
    // no press at all. Only the two extents are read, and a translate moves neither of them, so the
    // write below can never feed its own reading.
    var r = el.getBoundingClientRect();
    // The element's own half-extents are the units the contact was read in, so the reading returns
    // in them. A letter the settings record does not carry reads as absent and writes nothing on
    // its axis, the same refusal `passHandleSpan` already makes everywhere else in this file.
    var x = (sMix && sMix.span) ? (h.mix / sMix.span) * (r.width / 2) : 0;
    var y = (sTilt && sTilt.span) ? (h.tilt / sTilt.span) * (r.height / 2) : 0;
    painted = el;
    el.style.transform = "translate3d(" + x.toFixed(2) + "px," + y.toFixed(2) + "px,0)";
  }
  // The picture is handed back exactly as the walk laid it out — the walk writes no inline
  // transform on a work of its own (the door ceremony and the closer look each own their own
  // elements), so clearing the property is the whole of putting it back.
  function unpaint() {
    if (!painted) return;
    try { painted.style.transform = ""; } catch (e) {}
    painted = null;
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
        span: passHandleSpan(currentInstrument(), "mix"),
        breathAmplitude: breathAmplitude(),
        breathValue: breathValue(t),
        // The same reading in no units at all, between -1 and 1, both gains already in it — what a
        // renderer writes onto whatever travel it owns (S-112).
        unit: breathUnit(t),
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
        // The seat the conductor gave this voice, and the gain that register comes to. A voice with
        // no seat writes a breath of zero, which is Requirement 39 criteria 15 to 17 reaching the
        // frame rather than standing as a name on a report.
        seat: { register: hostSeat ? (function () {
                  try { return hostSeat(); } catch (e) { return null; } })() : null,
                gain: seatGain() },
      },
      // The hinge, which the hand's own free point rides (Requirement 38 criterion 4's chart law).
      tilt: { span: passHandleSpan(currentInstrument(), "tilt"), cap: handSpan("tilt") / 6 },
      hold: { active: hold.active, stretch: hold.stretch },
      lean: { value: lean.value, cap: leanCap(), direction: lean.direction, engaged: lean.engaged },
      attend: { x: attend.x, y: attend.y, target: attend.target },
      release: ring.kind === "release" ? {
        ring: ringElapsed <= RING_MS,
        resolved: ringElapsed > RING_MS,
        afterglow: ringElapsed <= RING_MS * 2,
      } : null,
      strike: ring.kind === "strike" ? { ring: ringElapsed <= RING_MS } : null,
      // THE MATTER THE RING BELONGS TO, and whether it was determined at all: the family's own row
      // out of the matter table, the cycles its criterion counts, the bound they finish inside, and
      // the frequency that is the one over the other. `determined` false is the fallback road, and
      // `matter` then names the row it fell back to.
      matter: (function () {
        var row = ringRow();
        return { matter: row.matter, determined: row.determined,
                 shape: row.ring ? row.ring.shape : null,
                 cycles: row.ring ? row.ring.cycles : null,
                 boundMs: RING_MS, freq: ringFreq() };
      })(),
      chart: {
        unfold: { x: { handle: "mix", value: handles.mix }, y: { handle: "tilt", value: handles.tilt } },
        moves: Object.keys(handles),
      },
    };
  }

  // THE VOICE'S NARROW DOOR, for the conductor alone. `report()` computes the breath, and the
  // breath asks the conductor for its gain, so a conductor reading `report()` would close a ring.
  // What it actually needs is the work this hand stands on and where the breath is in its own
  // cycle — the phase, the period this instant, and the floor criterion 1 names — and not one of
  // those depends on a gain.
  function voice() {
    var t = now();
    return { attached: attached, phase: breathPhase(t), periodMs: periodAt(t), floorMs: PERIOD_MS };
  }

  // The renderer's own door, beside the conductor's. One number per frame, no object built: the
  // breath's curve at its own two gains, which is everything a renderer needs from this file.
  function unit() { return breathUnit(now()); }

  join({ attach: attach, detach: detach, report: report, setGain: setGain,
         host: host, handleSpan: passHandleSpan, ringFreq: ringFreq, ringRow: ringRow,
         residual: RESIDUAL,
         voice: voice, unit: unit, clockCurve: clockCurve, clockProfile: clockProfile });
})();
