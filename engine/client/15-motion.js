  // ---- EX-GLIDE (INV-39): one input → one centered frame (the paginated walk) ----------
  // The decided motion model (supersedes the old free-inertia settle): every input — an arrow
  // key, a wheel notch, a touch swipe, done HOWEVER — makes exactly ONE ideal transition to the
  // adjacent frame in that direction. It ALWAYS starts smooth and ALWAYS lands smooth, CENTERED
  // on the target; it never rests between frames and never drifts afterwards. The old free-scroll
  // + stillness detector — "stops somewhere, then slowly floats another ~1.5s" — is RETIRED; that
  // lingering float was the felt defect. PHASE 1 (here): force is IGNORED — one fixed curve for
  // every input, always exactly one frame. PHASE 2 (a later tuning, NOT built now): force will
  // seed the SAME transition (see the `velocity` hook in glideToFrame) — a stronger input runs
  // faster through the start, lands just as gently, a violent flick advancing at most one extra.
  //
  // Split by input: TOUCH docks with native momentum under CSS scroll-snap (mandatory +
  // scroll-snap-stop:always — it never fights iOS momentum, so the jerk-fix holds by construction);
  // DESKTOP (wheel + keys) is owned by the JS animator below, which replaces native free-scroll so
  // no lingering drift can exist. Both resolve to the same one-frame-centered landing.
  const TOUCHY = matchMedia("(hover: none)").matches;
  let glideRaf = null;
  let gliding = false;
  let glideGoal = null;                                // where the running transition is headed
  let glideTargetEl = null;                            // the destination SECTION of the running glide (INV-86)
  function glideCancel() {
    if (glideRaf) { cancelAnimationFrame(glideRaf); glideRaf = null; }
    gliding = false;
    if (faceStands()) guardHold = scrollY;             // a glide ended under a face — hold where it landed (EX-CHROME)
  }
  // the one fixed transition: a sine in-out over one tempo-scaled clock. Monotonic 0→1 with both
  // ends soft — it provably cannot overshoot, so it ALWAYS lands centered on the frame, no bounce.
  const GLIDE_MS = clampInt(EX.glide_ms, 520, 120, 2000);  // a CALM gesture's one-frame dock (config knob, INV-28)
  // INV-84: force scales the single glide's SPEED, never the count. A sharp gesture eases the glide
  // down toward this floor; a calm one rides the full GLIDE_MS. Both land the SAME one frame, only the
  // duration differs. Named knobs Alexander can tune (a config override, else the [default]s here).
  const GLIDE_MS_SHARP = clampInt(EX.glide_ms_sharp, 260, 100, 2000);  // a SHARP gesture's shorter glide
  const VEL_CALM = clampInt(EX.glide_vel_calm, 40, 0, 4000);    // |deltaY| peak at/below → the full calm glide
  const VEL_SHARP = clampInt(EX.glide_vel_sharp, 480, 1, 8000); // |deltaY| peak at/above → the sharp floor
  // map a gesture's force (wheel peak |deltaY|, touch swipe magnitude) to the glide DURATION within the
  // clamped [GLIDE_MS_SHARP, GLIDE_MS] range — sharper → shorter (faster), still exactly one frame (INV-84).
  function glideDur(velocity) {
    const v = +velocity || 0;
    const f = Math.max(0, Math.min(1, (v - VEL_CALM) / (VEL_SHARP - VEL_CALM)));
    const base = GLIDE_MS - f * (GLIDE_MS - GLIDE_MS_SHARP);
    // the clock still scales the base (EX-MOTION / INV-33); reduced motion collapses it near-instant
    // (EX-MOTION-R). Capped ×1.5 so a slow tempo never makes the dock crawl.
    return base * Math.min(1.5, TEMPO / 1.35);
  }
  function glideToFrame(to, velocity) {
    glideCancel();
    const from = scrollY;
    const d = to - from;
    if (Math.abs(d) < 2) { glideGoal = null; return; } // already centered — nothing to move
    glideGoal = to;
    // INV-84: the gesture's velocity sets this single glide's duration (calm ~520ms → sharp ~260ms);
    // a re-time mid-flight (a rising wheel peak) restarts from the current position to the same goal,
    // so the position stays continuous and monotonic while only the speed changes — never a second frame.
    const dur = glideDur(velocity);
    const ease = (t) => 0.5 - 0.5 * Math.cos(Math.PI * t);
    const t0 = performance.now();
    gliding = true;
    const step = (now) => {
      if (atDoor || busy || sideOpen) { glideCancel(); glideGoal = null; return; }
      const p = Math.min(1, (now - t0) / dur);
      scrollTo(0, from + d * ease(p));                 // the animator OWNS the position
      if (p < 1) glideRaf = requestAnimationFrame(step);
      else { glideCancel(); glideGoal = null; }        // landed centered — no tail, no drift
    };
    glideRaf = requestAnimationFrame(step);
  }
  // The stops are MEASURED off the real sections, never k×innerHeight arithmetic: on a phone
  // the browser chrome makes the live innerHeight smaller than the frames' 100vh, so a computed
  // stop lands off centre and drifts FURTHER off with every step (his bug 2026-07-09). A
  // section's stop puts ITS centre on the live viewport's centre, so a landing is exactly
  // centered whatever the chrome did since the last one — each step self-corrects, never drifts.
  function frameCenter(el) {
    const r = el.getBoundingClientRect();
    const max = document.documentElement.scrollHeight - innerHeight;
    return Math.max(0, Math.min(max,
      Math.round(scrollY + r.top + (r.height - innerHeight) / 2)));
  }
  function frameStops() {
    const els = stage.querySelectorAll(".exh-frame, .exh-fin");
    return Array.prototype.map.call(els, frameCenter);
  }
  function nearestStop(stops, at) {
    let i = 0;
    for (let j = 1; j < stops.length; j++)
      if (Math.abs(stops[j] - at) < Math.abs(stops[i] - at)) i = j;
    return i;
  }
  // one step = advance exactly ONE frame from where the walk is — or from where a running
  // transition is headed, so a second input CHAINS to the next frame, never re-rounds backward.
  function stepFrame(dir, velocity) {
    travelDir = dir < 0 ? -1 : 1;                        // the feet declare a direction (EX-LOAD-3)
    const els = stage.querySelectorAll(".exh-frame, .exh-fin");
    const stops = Array.prototype.map.call(els, frameCenter);
    if (!stops.length) return;
    const base = gliding && glideGoal != null ? glideGoal : scrollY;
    const cur = nearestStop(stops, base);
    const k = Math.min(stops.length - 1, Math.max(0, cur + dir));
    if (k === cur) noteStuckStep(); else stuckBurst = [];   // EX-FRICTION: a clamped no-move step vs a real advance
    glideTargetEl = els[k];                              // the destination SECTION — a mid-glide rotation docks HERE (INV-86)
    glideToFrame(stops[k], velocity);
  }
  // the viewport metric moves under a RESTING walk (phone chrome collapses, a window resize) —
  // quietly re-dock the frame the eye is on to the new centre; mid-glide the landing already
  // rides fresh measurements, and the door/overlays own their own resize.
  // INV-86: the walk survives a device rotation. A portrait↔landscape turn (caught as its OWN
  // orientationchange beat, and via resize for a bare window change) recomputes the frame stops
  // against the NEW viewport so the docked frame stays centred under the eye. A turn arriving while a
  // glide is IN FLIGHT first cancels that glide to a dock at its TARGET frame (never a stale old-
  // viewport stop), then recomputes — so the far side of the turn holds one-gesture-one-frame. With the
  // zoom standing the walk beneath is re-docked too (invisibly, under the layer) so its exit lands true.
  let turnT = null, turnTargetEl = null;
  function onViewportTurn() {
    if (gliding && glideTargetEl && document.body.contains(glideTargetEl)) {
      turnTargetEl = glideTargetEl;                    // remember the destination across coalesced turn events
      glideCancel(); glideGoal = null;                 // stop writing OLD-viewport positions at once
    }
    clearTimeout(turnT);
    turnT = setTimeout(() => {                          // after the reflow — measure the fresh viewport
      if (document.documentElement.classList.contains("ex-walk")) {
        const stops = frameStops();
        if (stops.length) {
          let y;
          if (turnTargetEl && document.body.contains(turnTargetEl)) { y = frameCenter(turnTargetEl); restingEl = turnTargetEl; }
          else if (restingEl && document.body.contains(restingEl)) y = frameCenter(restingEl);
          else y = stops[nearestStop(stops, scrollY)];
          scrollTo(0, y);
          guardHold = y;                               // if the zoom (a face) stands, hold the recomputed place beneath (EX-CHROME)
        }
        schedulePlaceCaption();                        // EX-CAPTION (INV-97): re-seat the caption for the new viewport, on the same turn beat (INV-86)
      }
      turnTargetEl = null;
    }, 120);
  }
  addEventListener("resize", () => { if (walkOwnsInput() || gliding || zoomOpen) onViewportTurn(); });
  addEventListener("orientationchange", onViewportTurn);   // a rotation is its OWN beat (INV-86), not merely a resize
  // iOS reports stale innerWidth/innerHeight for ~200-400ms after a rotation, past the 120ms settle
  // above; the visualViewport "resize" fires as the viewport ACTUALLY settles, so re-measuring on it
  // catches the true post-turn dimensions (the between-pictures gutter would otherwise stay skewed).
  if (window.visualViewport) visualViewport.addEventListener("resize", () => { if (walkOwnsInput() || gliding || zoomOpen) onViewportTurn(); });
  function walkOwnsInput() {                            // the door/ceremony/faces keep native —
    return document.documentElement.classList.contains("ex-walk")   // a standing face owns the
      && !atDoor && !busy && !sideOpen && !quizOpen && !giftOpen;   // input (EX-COMPOSE)
  }

  // EX-CHROME (INV-70): one page shape for the browser. The root overflow cut is retired as a lock;
  // instead EVERY standing face — the re-opened door, the side room, the question card, the gift
  // card — locks the walk by resting input + a snap-back guard, while the walk's own tall document
  // stays in place beneath. The STANDING DOOR is a face like the others for locking (its own
  // controls stay live). `busy` is the whole door/side ceremony (its own lock, EX-DOOR-2e).
  const FACE_SEL = "#ex-door, #ex-side, #ex-quiz-card, #ex-gift-card, #ex-sound";  // face roots + chrome
  let guardHold = 0;                                    // the place the walk holds while a face stands
  function faceStands() { return atDoor || busy || sideOpen || quizOpen || giftOpen || zoomOpen; }
  // mirror the stand onto the root: `ex-face` sleeps the scrollbar (gutter-stable, no reflow) and
  // arms the input rest + guard. On a RISE (no face → a face) freeze the walk's place to hold.
  function faceSync() {
    const stands = faceStands();
    const had = document.documentElement.classList.contains("ex-face");
    document.documentElement.classList.toggle("ex-face", stands);
    if (stands && !had) guardHold = scrollY;           // a face rose — remember the place beneath
  }
  // the snap-back guard is the ONLY lock now. While a face stands and the house's own animator is
  // not running, any scroll the house did NOT write (a dragged scrollbar, a slipped native gesture)
  // is corrected to the held place in the same beat — a correction, no designed motion (INV-33).
  // The house's own writes (the ceremony, Back restore, the leave re-centre) re-freeze guardHold, so
  // the guard answers only scroll the house did not write itself.
  // A standing finger is NOT input rest (EX-CHROME): while a pointer/touch is DOWN the guard HOLDS.
  // An active touch drags the page a few px (the phone's rubber-band); a correction written mid-touch
  // only makes the finger drag again next frame — a per-frame fight the visitor sees as the whole
  // screen trembling (his 2026-07-10 phone find). The guard corrects only at rest, one settle on lift.
  let heldTouches = 0;
  const heldPointers = new Set();
  function pointerHeld() { return heldTouches > 0 || heldPointers.size > 0; }
  function settleGuard() {                              // one correction when the last finger lifts
    if (!faceStands() || gliding || pointerHeld()) return;
    if (Math.abs(scrollY - guardHold) > 1) scrollTo(0, guardHold);
  }
  // EX-CHROME: the moving-finger gesture, tracked so the face can EAT a drag at the source. The
  // start point and a per-gesture verdict (fDecided: null undecided · true a truly scrollable part
  // of the face keeps native · false the walk never gets the drag) are set on a 1-touch touchstart
  // and cleared on lift. The verdict is picked once, on the first ~4px, and held to the lift.
  let fX = null, fY = null, fDecided = null;
  addEventListener("touchstart", (e) => {
    heldTouches = e.touches.length;
    fDecided = null;                                    // a new gesture — fresh verdict
    if (e.touches.length === 1) { fX = e.touches[0].clientX; fY = e.touches[0].clientY; }
    else { fX = fY = null; }
  }, { passive: true, capture: true });
  ["touchend", "touchcancel"].forEach((k) => addEventListener(k, (e) => {
    heldTouches = e.touches.length; if (!e.touches.length) fX = fY = null;
    if (!pointerHeld()) settleGuard();
  }, { passive: true, capture: true }));
  addEventListener("pointerdown", (e) => { heldPointers.add(e.pointerId); },
                   { passive: true, capture: true });
  ["pointerup", "pointercancel"].forEach((k) => addEventListener(k, (e) => {
    heldPointers.delete(e.pointerId); if (!pointerHeld()) settleGuard();
  }, { passive: true, capture: true }));
  addEventListener("scroll", () => {
    if (!faceStands() || gliding) return;
    if (pointerHeld()) return;                          // a finger rests on the glass — hold, settle on lift
    if (Math.abs(scrollY - guardHold) > 1) scrollTo(0, guardHold);
  }, { passive: true });

  // EX-COMPOSE: the last face leaves into a fresh-measured room — an INSTANT re-centre of the
  // section that stood beneath, discharged under the leaving face's own fade. A correction with
  // no designed motion, so it can never race a glide for scrollY.
  function recentreUnder() {
    if (sideOpen || quizOpen || giftOpen || atDoor || busy) return;  // a face still stands
    if (!document.documentElement.classList.contains("ex-walk")) return;
    const stops = frameStops();
    if (!stops.length) return;
    scrollTo(0, restingEl ? frameCenter(restingEl) : stops[nearestStop(stops, scrollY)]);
  }
  // DESKTOP wheel: one gesture → one frame. A mouse notch is a single event; a trackpad swipe is
  // a burst of them — both coalesce to ONE step (force ignored, phase 1). preventDefault kills
  // native free-scroll entirely, so there is no momentum left to "float" after the stop.
  let wheelIdle = null;
  let wheelPeak = 0;                                   // the live gesture's PEAK |deltaY| — the force→speed input
  let wheelMode = null;                                // "walk" (plain wheel) | "zoom" (ctrl+wheel) — latched per burst
  // INV-84 re-arm, SETTINGS-INDEPENDENT (his 2026-07-16 word): macOS scales every wheel |deltaY| by
  // the user's own trackpad-speed setting, so ANY absolute |deltaY| threshold is wrong per-user by
  // construction. The verdict below reads only TIME and RATIOS — both invariant under any speed
  // setting. No browser exposes the macOS momentum phase to JS, so the SHAPE of the stream is the
  // only signal. The physical key: a momentum tail carries the finger's decaying kinetic energy, so
  // it only ever FALLS — it cannot sustain a climb on its own. A NEW gesture is the one thing that
  // makes the stream CLIMB again after the peak. But a single CONTINUOUS drag that eases then pushes
  // again also climbs, without a finger lift — so a climb alone is not enough. The separating fact:
  // a new gesture follows a momentum END; a within-drag re-accel does not. So inside a non-fresh burst
  // a new step fires only when ALL hold: the momentum DIED (fell to ≤ CREST_RATIO × peak — a real
  // death, so an ease to a quarter of the peak never qualifies), it has climbed for RISE_RUN
  // consecutive events on the finger's OWN dense cadence (gap ≤ RISE_GAP_MS — a sparse far-tail ripple
  // rides wide gaps and is excluded), that climb clears the decayed envelope by REARM_RATIO, and
  // STEP_MIN_MS passed since the last step. This replaced the earlier bare time-gap re-arm, which read
  // a momentum tail's own GROWING gaps as fresh gestures (one swipe → four steps, WHL9) and swallowed
  // a fast second swipe under a 250ms floor (WHL10). Known narrow residual (a "too few", his feel-tune,
  // fundamentally in tension with never double-stepping a drag): a GENTLE-and-slow second swipe whose
  // onset rides wide gaps AND whose hole is under the 150ms idle window can be missed — a dense reswipe,
  // or any reswipe past the idle window, always lands. Every constant is a provisional STRUCTURE —
  // Alexander tunes the values by FEEL on the live site; none is an absolute |deltaY| magnitude.
  const WHEEL_IDLE_MS = 150;   // gesture end: this much event silence → the next event opens a FRESH burst (the kept idle window)
  const STEP_MIN_MS = 120;     // a small refractory floor between steps — a fast double-swipe still lands two (a human-rhythm constant, not a device one)
  const REARM_RATIO = 1.6;     // a new-gesture onset clears the decayed envelope by at least this ratio (a ratio — speed-setting-proof)
  const CREST_RATIO = 0.18;    // re-arm eligible only once the stream fell to ≤ this × the peak — the momentum has DIED, not merely eased: a drag that slows to a quarter of its peak and pushes again is ONE contact, not a new gesture, so it never re-arms (the audit's within-drag re-accel)
  const ENV_HALF_MS = 80;      // the envelope's half-life: how fast the remembered level follows the tail down
  const RISE_RUN = 2;          // a re-arm needs this many CONSECUTIVE climbing events — momentum falls, only input climbs
  const RISE_GAP_MS = 35;      // the re-arm's climb rides the finger's own DENSE cadence (~12ms); a far tail spaces its events 50-130ms apart, so a sparse tail ripple can never be a re-swipe onset
  // The per-event verdict, PURE and DOM-free — test_wheel.py extracts this block (the constants
  // above + this function) and replays recorded envelopes in node: no browser, no timers, no sleeps.
  // Keep it self-contained. `st` carries: env (the decaying envelope following the tail), peak (the
  // burst's high-water mark, for the crest test), crested (fell into the tail), rises (consecutive
  // climbing events), prev (the previous |deltaY|), stepT (when the last step fired), lastT (the
  // previous event), fresh (this event opened a new burst). Returns the step: -1 | 0 | +1.
  function wheelWalkStep(s, st) {
    const mag = Math.abs(s.dy);
    const gap = st.lastT == null ? Infinity : s.t - st.lastT;
    st.fresh = gap >= WHEEL_IDLE_MS;                   // the idle boundary read off timestamps — the setTimeout twin in the listener resets state on true idle
    let step = 0;
    if (st.fresh) {
      step = s.dy > 0 ? 1 : -1;                        // a fresh burst always steps once
      st.env = mag; st.peak = mag; st.crested = false; st.stepT = s.t; st.prev = mag; st.rises = 0;
    } else {
      const env = st.env * Math.pow(0.5, gap / ENV_HALF_MS);       // the envelope, decayed toward the tail at NOW
      if (mag > st.peak) st.peak = mag;
      if (!st.crested && st.peak > 0 && mag <= st.peak * CREST_RATIO) st.crested = true;
      st.rises = (mag > st.prev) ? st.rises + 1 : 0;               // consecutive climbing events — momentum never climbs
      // a re-swipe onset is a DENSE climb (the finger's own cadence) that clears the decayed tail; a sparse
      // far-tail ripple climbs across wide gaps where the envelope has itself decayed to the live value, so
      // the ratio alone degenerates there — the tight-gap gate is what tells the two apart (INV-84).
      const onset = st.crested && st.rises >= RISE_RUN && gap <= RISE_GAP_MS && mag >= env * REARM_RATIO;
      if (mag > 0 && s.t - st.stepT >= STEP_MIN_MS && onset) {
        step = s.dy > 0 ? 1 : -1;                      // a deliberate SECOND swipe — re-armed
        st.env = mag; st.peak = mag; st.crested = false; st.stepT = s.t; st.rises = 0;
      } else {
        st.env = Math.max(env, mag);                   // ride the stream: attack to the live value, else follow the tail down
      }
      st.prev = mag;
    }
    st.lastT = s.t;
    return step;
  }
  const wheelS = { env: 0, peak: 0, crested: false, stepT: 0, lastT: null, fresh: true, prev: 0, rises: 0 };
  if (!TOUCHY) {
    addEventListener("wheel", (e) => {
      // The burst boundary and the MEANING are both fixed at the first event: a mouse notch is one
      // event, a trackpad swipe a decaying burst — the idle timer resets the state only once all
      // motion stops, so the NEXT gesture is genuinely fresh (the pure verdict reads the same 150ms
      // off e.timeStamp, so the two agree). The meaning is latched here and held for the whole
      // coalesced burst, so a ctrl gained or lost mid-burst never flips it (EX-PROTECT/INV-85).
      clearTimeout(wheelIdle);
      wheelIdle = setTimeout(() => { wheelPeak = 0; wheelMode = null; wheelS.lastT = null; }, WHEEL_IDLE_MS);
      const step = wheelWalkStep({ t: e.timeStamp, dy: e.deltaY }, wheelS);
      if (wheelS.fresh) { wheelMode = e.ctrlKey ? "zoom" : "walk"; wheelPeak = 0; }
      // INV-85 / EX-PROTECT: the browser's own ctrl-wheel (viewport) zoom is refused on EVERY ctrl+wheel.
      // The old blunt guard was `if (e.ctrlKey) { e.preventDefault(); return; }` — a flat refusal. INV-85
      // KEEPS that preventDefault (in the "zoom" branch just below) but now HANDS the same ctrl+wheel to
      // our own inspect layer instead of dropping it: the browser still never viewport-zooms, and the
      // gesture drives the app zoom. A plain wheel stays the walk — the split is clean.
      if (wheelMode === "zoom") { e.preventDefault(); pinchWheel(e); return; }
      if (faceStands()) {                              // EX-CHROME: rest the walk's input behind a face
        if (e.target && e.target.closest && e.target.closest(FACE_SEL)) return;  // the face's own scroll / chrome stays native
        e.preventDefault(); return;                    // the overflow cut is gone — the rest holds the walk
      }
      if (!walkOwnsInput()) return;
      if (e.target && e.target.closest
          && e.target.closest("#ex-side, #ex-quiz-card, #ex-gift-card")) return;  // overlay scrolls
      e.preventDefault();                              // the walk is paginated, not free
      const mag = Math.abs(e.deltaY);
      // INV-84: one continuous burst = EXACTLY one frame. The verdict is the pure wheelWalkStep
      // above — a fresh burst steps once; inside a burst only a real stream hole or a relative
      // re-acceleration out of the crested tail (never sooner than the human double-swipe floor)
      // re-arms. A non-stepping event still feeds the ONE glide's SPEED: a rising peak re-times
      // the running glide to the same goal (force→speed, unchanged).
      if (step) { wheelPeak = mag; stepFrame(step, mag); return; }
      if (mag > wheelPeak) {
        wheelPeak = mag;
        if (gliding && glideGoal != null) glideToFrame(glideGoal, wheelPeak);
      } else wheelPeak = Math.max(mag, wheelPeak * 0.95);
    }, { passive: false });
  }
  // DESKTOP keys ARE the walk's step: space/↓/PageDown forward, ↑/PageUp (and shift+space) back —
  // the SAME one transition; a held key = one frame per press; a press mid-transition chains to
  // the next frame; every other key is left to its own owner.
  const PAGE_KEYS = { "ArrowDown": 1, "ArrowRight": 1, "PageDown": 1, " ": 1,
                      "ArrowUp": -1, "ArrowLeft": -1, "PageUp": -1 };  // all four arrows page (his note)
  addEventListener("keydown", (e) => {
    if (!PAGE_KEYS[e.key]) return;
    if (!walkOwnsInput()) return;                      // the walk's faces keep their own keys
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    const t = e.target;
    if (t && (t.tagName === "INPUT" || t.tagName === "TEXTAREA" || t.isContentEditable)) return;
    let dir = PAGE_KEYS[e.key];
    if (e.key === " " && e.shiftKey) dir = -1;         // shift+space pages back, as everywhere
    e.preventDefault();                                // the native jump never fights the glide
    if (e.repeat) return;                              // a held key = one frame per press
    stepFrame(dir);
  }, { passive: false });

  // EX-CHROME: while a face stands, rest the browser's own scroll keys behind it (the walk's step
  // handler above already sits a face out). Home/End join the arrows / space / page keys. A face's
  // OWN keys (Esc, typing in a field) are untouched — only scroll keys, and never inside a field.
  const REST_KEYS = { " ": 1, "ArrowDown": 1, "ArrowUp": 1, "ArrowLeft": 1, "ArrowRight": 1,
                      "PageDown": 1, "PageUp": 1, "Home": 1, "End": 1 };
  addEventListener("keydown", (e) => {
    if (!faceStands() || !REST_KEYS[e.key]) return;
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    const t = e.target;
    if (t && t.closest && t.closest(FACE_SEL)) return;         // the face's own scroll / field keeps native
    if (t && (t.tagName === "INPUT" || t.tagName === "TEXTAREA" || t.isContentEditable)) return;
    e.preventDefault();                                        // no native scroll behind the veil
  }, { passive: false });

  // TOUCH: one swipe → one frame (his phone bug 2026-07-09 — CSS scroll-snap-stop:always did not
  // hold, so a momentum swipe flew through several works). The walk takes the touch the same way
  // the wheel takes a desktop gesture: native scroll is blocked while the walk owns the input, and
  // ONE swipe docks exactly ONE frame through glideToFrame. The animator writes the position only
  // AFTER the finger lifts, so there is no live iOS momentum to fight (the old jerk is impossible
  // here). Overlays (side room, quiz/gift card) and the door keep native scroll — see the guards.
  if (TOUCHY) {
    let tY = null, tLast = 0, tMoved = false;
    const SWIPE_MIN = 24;                              // net px that counts as a swipe (a tap/hold does nothing)
    const NATIVE_TOUCH = "#ex-side, #ex-quiz-card, #ex-gift-card, #ex-sound, .ex-share";
    addEventListener("touchstart", (e) => {
      if (!walkOwnsInput() || e.touches.length !== 1
          || (e.target && e.target.closest && e.target.closest(NATIVE_TOUCH))) {
        tY = null; return;                             // door / overlays / chrome controls / multi-touch keep native touch
      }
      tY = tLast = e.touches[0].clientY;
      tMoved = false;
    }, { passive: true });
    // EX-CHROME: does some part of the face under the finger truly take this drag's axis?
    function faceConsumes(target, horiz) {
      for (let el = target; el && el !== document.documentElement; el = el.parentElement) {
        if (el.matches && el.matches("input, textarea, select, [contenteditable]")) return true;
        if (el instanceof Element) {
          const cs = getComputedStyle(el);
          if (horiz ? (el.scrollWidth  > el.clientWidth  + 1 && /(auto|scroll)/.test(cs.overflowX))
                    : (el.scrollHeight > el.clientHeight + 1 && /(auto|scroll)/.test(cs.overflowY))) return true;
          if (el.matches && el.matches(FACE_SEL)) break;   // reached the face root — nothing consumed
        }
      }
      return false;
    }
    addEventListener("touchmove", (e) => {
      if (faceStands()) {                              // EX-CHROME: the face EATS the drag at the source
        if (e.touches.length === 1 && fX != null) {
          if (fDecided == null) {
            const dx = e.touches[0].clientX - fX, dy = e.touches[0].clientY - fY;
            const adx = Math.abs(dx), ady = Math.abs(dy);
            const inFace = !!(e.target && e.target.closest && e.target.closest(FACE_SEL));
            // An overflow-x lane under the finger (EX-SERIES): DEFER the axis verdict past the noisy
            // first pixels and decide by the DOMINANT travel — a rightward drag from a slightly-vertical
            // start still scrolls the lane, where the 4px latch used to hand it to the walk and the lane
            // never moved (his phone find 2026-07-15). Every other face keeps the first-4px verdict.
            const laneUnder = inFace && faceConsumes(e.target, true);
            if (laneUnder) {
              // INV-96: while still ambiguous over the lane, WATCH ONLY — no preventDefault. On
              // phone WebKit eating even the ambiguous-window events poisoned the native scroll
              // hand-off for the WHOLE gesture (a slow-starting swipe went dead — the every-other-
              // swipe report 2026-07-16), because that hand-off is decided from the gesture's very
              // first events. The walk itself is already inert here (walkOwnsInput() is false while
              // sideOpen), so there is nothing of the walk's own to protect by consuming early.
              if (adx < 12 && ady < 12) { return; }   // still ambiguous — hold, don't latch, don't eat
              fDecided = adx >= ady;                                       // horizontal → native, the lane runs
            } else if (adx + ady >= 4) {                                   // the first ~4px pick the axis
              fDecided = inFace && faceConsumes(e.target, adx > ady);
            } else { e.preventDefault(); return; }                        // undecided yet — eat, the walk never gets a first pixel
          }
          if (fDecided) return;                        // a truly scrollable part — native, the lane lives
          e.preventDefault(); return;
        }
        if (e.target && e.target.closest && e.target.closest(FACE_SEL)) return;  // multi-touch: today's treatment
        e.preventDefault(); return;                    // the overflow cut is gone — the rest holds the walk
      }
      if (tY == null) {
        // a pinch or a 2-finger touch dropped back to ONE finger mid-walk: re-take the gesture so
        // the tail cannot free-scroll the paginated walk (the fly-through the animator exists to
        // kill). Only when the walk truly owns the input and the finger is not on chrome/an overlay.
        if (e.touches.length === 1 && walkOwnsInput()
            && !(e.target && e.target.closest && e.target.closest(NATIVE_TOUCH))) {
          tY = tLast = e.touches[0].clientY; tMoved = false;
        } else return;
      }
      tLast = e.touches[0].clientY;
      if (Math.abs(tLast - tY) > 6) tMoved = true;
      e.preventDefault();                              // the walk is paginated — no native scroll, no fly-through
    }, { passive: false });
    addEventListener("touchcancel", () => { tY = null; });   // a system-cancelled touch leaves no stale drag
    addEventListener("touchend", () => {
      if (tY == null) return;
      const net = tY - tLast;                          // finger travels UP (net>0) = advance forward
      tY = null;
      if (!tMoved || Math.abs(net) < SWIPE_MIN) return;
      stepFrame(net > 0 ? 1 : -1);                     // exactly one framed transition, force ignored (phase 1)
    }, { passive: true });
  }

