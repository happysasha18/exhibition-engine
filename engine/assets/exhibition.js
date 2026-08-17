/*!00-prelude.js*/
/* exhibition.js — the adaptive exhibition (EX): the DOOR → the GALLERY (the Room's museum hang).
   Norm for look & feel: gallery/door.html + gallery/room.html — the approved look-and-feel prototypes.
   The laws: a cold arrival meets the door — a small pool of works and
   the quiet ask "what feels closest now" (EX-DOOR); the pick seeds the hang — one work per viewport,
   caption in the margin, breathing ground (EX-HANG); the walk ENDS (INV-30) and always loops back
   to the threshold (INV-31). Every knob reads from config.json → exhibition (INV-28).
   Kinship math runs in the browser on baked vectors ($0, no server). No axis name, score or
   confidence ever renders (INV-1) — the caption zone speaks only his titles and the archive's facts. */
(async function () {
  "use strict";
  const stage = document.getElementById("ex-stage");
  if (!stage) return;                                 // no live root → JS-off face stays

  // ---- N7-A11Y (INV-102 / CS-5 / OS-A2): ONE accessible-description reader, ONE baked source ----
  // build.py bakes each walk record's `desc` — the SAME string its /w page + the static-index alt
  // carry. Every img site (walk frame, closer look, series polaroid + lane, gift prize) applies THIS
  // reader, so no surface invents its own alt. `byId` initializes in 02-kinship-orderings.js; this
  // reader runs only at runtime img sites (all after boot), so the forward reference resolves.
  function workDesc(id) {
    try { const w = byId[id] || byId[String(id)]; return w && w.desc ? String(w.desc) : ""; }
    catch (e) { return ""; }
  }
  function escAttr(s) {                                // for a description carried in an HTML attribute
    return String(s == null ? "" : s).replace(/[<>&"]/g,
      (c) => ({ "<": "&lt;", ">": "&gt;", "&": "&amp;", '"': "&quot;" }[c]));
  }

  // ---- EX-BUSY: ONE waiting mark for every CONTROL that waits (INV-48) -------------------------
  // A single reusable ring that fills along a control's contour while an action of that control is
  // in flight — the sound button buffering its stream, a language chip fetching an outsider tongue,
  // the gift's yes preparing a slow file. It reads as the SAME "working" gesture wherever a control
  // waits, so no surface invents its own spinner. The picture surfaces (walk frame, series room,
  // closer look) wait behind their OWN kind of mark — the plate ladder / the skeleton shimmer — this
  // is only for the small chrome controls. The host is made positioning-context by CSS (.ex-busy-ring
  // is absolutely placed just outside the control's edge); the ring is aria-hidden — the control keeps
  // its own label, and a11y busy state rides aria-busy where a caller sets it.
  function exBusyRing(host, on) {
    if (!host) return;
    let r = host.querySelector(":scope > .ex-busy-ring");
    if (on) {
      if (!r) {
        r = document.createElement("span");
        r.className = "ex-busy-ring";
        r.setAttribute("aria-hidden", "true");
        r.innerHTML = '<svg viewBox="0 0 40 40" fill="none"><circle cx="20" cy="20" r="17"></circle></svg>';
        host.appendChild(r);
      }
      requestAnimationFrame(() => r.classList.add("on"));
    } else if (r) {
      r.classList.remove("on");
    }
  }

  // ---- N7-A11Y (INV-102 / B1): ONE focus trap, four modal callers ----------------------------
  // The gift ceremony (11), the closer look (12), the quiz card (13), and the series room (16) each
  // open through openTrap and close through closeTrap and never re-implement it (architecture N7-A11Y,
  // "one trap, four callers"). openTrap moves focus INTO the layer and holds Tab inside it — a focus
  // loop, so the covered walk is never reached; closeTrap releases and, when the open recorded an
  // opener, returns focus to it. The origin rule the spec sets lives in WHAT each caller passes as the
  // opener: the keyboard route passes the focused work (restore to it on close); a pointer / touch open
  // passes nothing, so the zoom leaves NO forced focus and its exact-restore invariant (INV-74/INV-83)
  // is untouched. A stack carries a rare nesting (a closer look opened from a lane image over the series
  // room) so the inner close restores to the lane image, the outer to the series' opener.
  const FOCUSABLE_SEL =
    'a[href],button:not([disabled]),input:not([disabled]),select:not([disabled]),' +
    'textarea:not([disabled]),[tabindex]:not([tabindex="-1"])';
  const _trapStack = [];
  // Last-input modality (EX-CHROME focus policy). A KEYBOARD open of a modal lights its first
  // control (a visible focus mark the keyboard visitor needs); a POINTER / TOUCH open anchors the
  // trap on the layer itself and lights nothing — so a finger never leaves a modal's close / first
  // button wearing a focus ring (his 2026-07-23: the zoom × and the gift «yes» rose on a tan focus
  // fill + the browser's blue ring after a tap). This ENFORCES for every caller the intent the trap
  // comment already stated (a pointer open forces no focus): the opener alone did not carry it,
  // since the quiz and the series room capture activeElement as opener under any modality.
  let _kbModality = false;
  addEventListener("keydown", () => { _kbModality = true; }, { capture: true, passive: true });
  ["pointerdown", "mousedown", "touchstart"].forEach((e) =>
    addEventListener(e, () => { _kbModality = false; }, { capture: true, passive: true }));
  // EX-CHROME touch-press (his 2026-07-23). 1.11.1 gated every control's engaged FILL to hover:hover
  // so a finger tap leaves no sticky tint — correct, but it left a tap with NO feedback at all. This
  // gives a coarse pointer the response a mouse gets from hover: a press lights the control's OWN
  // engaged affordance for the DURATION of the touch. One delegated pair toggles `.ex-press` on the
  // pressed CONTROL (pointerdown → on, lift / cancel → off); the styling is hover:none-gated in CSS,
  // so a mouse (hover:hover, its own hover fill) is untouched. The player already answered a tap by
  // turning `.playing`; this brings every other button up to the same felt response. PRESS_SEL is the
  // WHOLE control class — every chrome button that wears a hover/focus fill owes a touch-press twin
  // (his 2026-07-23 find: the series pill and the room's back button were left out, felt dead on a
  // finger). A press that drifts into a swipe clears on the browser's pointercancel.
  // The closing screen's controls are matched by their PLACE in its row, never by name: a control
  // added to that row later joins the class by standing there (2026-07-27, the about link). Naming
  // `.more` and `.back` one by one is what left the series pill and the room's back button dead
  // under a finger, with the consistency test sharing the code's own blind spot.
  const PRESS_SEL = ".ex-share,#ex-zoom .exz-btn,.exsnd-btn,.quiz-opt,.exl-cur,.exl-item," +
    ".exd-window,#ex-gift-card .gift-yes,#ex-gift-card .gift-no," +
    ".ex-series,.exs-back,.ex-quiz-chip,.exh-fin .row > *";
  let _pressEl = null;
  function _pressClear() { if (_pressEl) { _pressEl.classList.remove("ex-press"); _pressEl = null; } }
  addEventListener("pointerdown", (e) => {
    _pressClear();
    const c = (e.target && e.target.closest) ? e.target.closest(PRESS_SEL) : null;
    if (c) { c.classList.add("ex-press"); _pressEl = c; }
  }, { capture: true, passive: true });
  ["pointerup", "pointercancel"].forEach((e) =>
    addEventListener(e, _pressClear, { capture: true, passive: true }));
  function _focusablesIn(layer) {
    return Array.prototype.filter.call(
      layer.querySelectorAll(FOCUSABLE_SEL),
      (el) => !el.hidden && el.tabIndex !== -1 && (el.offsetWidth > 0 || el.offsetHeight > 0));
  }
  function openTrap(layer, opener) {                   // opener: the element to restore to, or falsy for none
    if (!layer) return;
    const rec = {
      layer: layer,
      opener: (opener && opener.focus && document.body.contains(opener)) ? opener : null,
      keydown: null,
    };
    const first = _focusablesIn(layer)[0] || layer;
    // keyboard origin → focus the first control (its focus-visible mark is wanted). Pointer / touch
    // origin → anchor the trap on the LAYER (a programmatic, non-focus-visible target): Tab still
    // enters the layer and lands the first control keyboard-lit, but the open itself lights nothing.
    if (_kbModality) {
      if (first === layer && layer.tabIndex < 0) layer.setAttribute("tabindex", "-1");
      requestAnimationFrame(() => { try { first.focus({ preventScroll: true }); } catch (e) {} });
    } else {
      if (layer.tabIndex < 0) layer.setAttribute("tabindex", "-1");
      requestAnimationFrame(() => { try { layer.focus({ preventScroll: true }); } catch (e) {} });
    }
    rec.keydown = (e) => {                             // hold Tab inside — a loop at both ends
      if (e.key !== "Tab") return;
      const items = _focusablesIn(layer);
      if (!items.length) { e.preventDefault(); return; }
      const idx = items.indexOf(document.activeElement);
      if (e.shiftKey) {
        if (idx <= 0) { e.preventDefault(); items[items.length - 1].focus({ preventScroll: true }); }
      } else if (idx === -1 || idx === items.length - 1) {
        e.preventDefault(); items[0].focus({ preventScroll: true });
      }
    };
    layer.addEventListener("keydown", rec.keydown);
    _trapStack.push(rec);
  }
  function closeTrap(layer) {
    let i = -1;
    for (let k = _trapStack.length - 1; k >= 0; k--) { if (_trapStack[k].layer === layer) { i = k; break; } }
    if (i === -1) return;
    const rec = _trapStack[i];
    if (rec.keydown) layer.removeEventListener("keydown", rec.keydown);
    _trapStack.splice(i, 1);
    if (rec.opener && document.body.contains(rec.opener)) {
      requestAnimationFrame(() => { try { rec.opener.focus({ preventScroll: true }); } catch (e) {} });
    } else if (rec.opener) {
      // the opener has LEFT the page while the layer stood (the room re-dressed, the walk rebuilt
      // beneath). Doing nothing drops a keyboard visitor to the document body, with no way back into
      // the page but a full Tab walk — so focus the surface still standing UNDER the layer: the
      // standing face's own container, else the walk stage.
      const back = _standingSurface();
      if (back) {
        if (back.tabIndex < 0) back.setAttribute("tabindex", "-1");   // the conventional programmatic-only stop
        requestAnimationFrame(() => { try { back.focus({ preventScroll: true }); } catch (e) {} });
      }
    }
  }
  // which surface stands beneath a closing layer. The face flags (atDoor / sideOpen) and their
  // containers are declared later in the bundle; this only ever runs at close time, long after boot,
  // so the references resolve — the try guards the one impossible case.
  function _standingSurface() {
    try {
      if (sideOpen) {
        const s = document.getElementById("ex-side");
        if (s && !s.hidden) return s;
      }
      if (atDoor) {
        const d = document.getElementById("ex-door");
        if (d && !d.hidden) return d;
      }
    } catch (e) {}
    return stage;
  }

  // ---- the visitor's own trace, its three homes (one place for the names) -----
  const KEY = "@@NS@@.exhibition";                       // the walk (INV-26)
  const PLACE_KEY = "@@NS@@.place";                      // the per-tab place marker (INV-32c)
  const TEMPO_KEY = "@@NS@@-tempo";                      // the motion override (EX-MOTION-R)
  const SPENT_KEY = "@@NS@@.spent";                      // the hash hand-over, consumed once (EX-SHARE-IN)
  const ORIGIN_KEY = "@@NS@@.origin";                    // the channel this visit first arrived under, folded (EX-SHARE-ORIGIN)
  const VISITOR_KEY = "@@NS@@.visitor";                  // the coat-check token (EX-MEMORY)
  const HAND_KEY = "@@NS@@.hand";                        // the last dealt threshold hand (EX-DOOR-3)
  const SEENC_KEY = "@@NS@@.seenc";                      // the seen-list's local copy (EX-DOOR-3)
  const DOORDEALT_KEY = "@@NS@@.doordealt";              // works the diverse door has dealt this round (EX-DOOR-3/INV-75)
  const LANG_KEY = "@@NS@@.lang";                        // the guest's chosen tongue (EX-LANG)
  const SND_KEY = "@@NS@@.sound";                         // the ambient player's on/off + volume (EX-SOUND)
  const BEEN_KEY = "@@NS@@.been";                         // EX-RETURN: this browser has walked the exhibition before
  const LAST_KEY = "@@NS@@.last";                        // EX-PULSE/INV-79: this browser's last-visit timestamp (return_gap); EX-RETURN reuses it for the welcome-back window
  const EXITS_KEY = "@@NS@@.exits";                      // EX-RETURN/INV-78: count of real walk→door exits (the farewell waits for the 2nd)
  const SOLO_KEY = "@@NS@@.solo";                        // EX-STORY-FILL/INV-107: this clock hour's one-work asks (stands through a door pick)
  const MORE_EXIT_EN = "there is more still hanging — come again";   // the exit farewell (English fallback)
  const MORE_RETURN_EN = "back again — a new way in";               // the returning-arrival line (English fallback)
  // EX-RETURN/INV-78 window bounds — tunable, both ends bound in TIME so the door never over-speaks:
  const FAREWELL_MIN_EXITS = 2;                       // the farewell is silent on the 1st exit, speaks from the 2nd onward
  const RETURN_MIN_MS = 6 * 60 * 60 * 1000;          // welcome-back lower bound: a return sooner than 6h is a reload, stays silent
  const RETURN_MAX_MS = 14 * 24 * 60 * 60 * 1000;    // welcome-back upper bound: a return later than 14d is met as new, no welcome-back

  // ---- EX-TIMING (INV-38): the museum keeps time — for its builder only -------
  // Marks are free and invisible (INV-1: no DOM text; INV-18: no beacon, nothing
  // leaves the tab). ?timings narrates the beats to the console as they land;
  // @@NS_UPPER@@Timings() hands the walk's clock over as data for export.
  const WANT_T = new URLSearchParams(location.search).has("timings");
  function tlog(beat) {
    try { performance.mark("@@NS@@:" + beat); } catch (e) {}
    if (WANT_T) {
      try { console.log("@@NS@@:" + beat, (performance.now() / 1000).toFixed(3) + "s"); } catch (e) {}
    }
  }
  window.@@NS_UPPER@@Timings = () => performance.getEntriesByType("mark")
    .filter((m) => m.name.indexOf("@@NS@@:") === 0)
    .map((m) => ({ beat: m.name.slice(@@NS_MARK_LEN@@), at: +(m.startTime / 1000).toFixed(3) }));
  tlog("boot");

  // ---- EX-PULSE (INV-41): the walk counts its beats for the archive's owner ----
  // Rides the ONE sanctioned wire (the baked GA tag); no tag ⇒ total silence; an event
  // carries at most the plain name + the work's public id — never a vector (INV-1).

  // EX-QUIZ-FLOW (INV-69): the session-scoped running-max stage for the quiz funnel.
  // Restored from sessionStorage at boot so a reload never lowers what was reached.
  const QUIZ_STAGE_KEY = "@@NS@@.quizstage";
  let quizStage = null;
  try {
    const _qs = sessionStorage.getItem(QUIZ_STAGE_KEY);
    if (_qs) quizStage = _qs;
  } catch (e) {}
  const QUIZ_STAGE_RANK = { shown: 1, opened: 2, won: 3, lost: 3, gift: 4 };
  function quizStageUp(name) {
    // Raise only — never lower; "gift" accepted only when current stage is "won" (INV-69).
    if (name === "gift" && quizStage !== "won") return;
    const next = QUIZ_STAGE_RANK[name];
    if (!next) return;
    const cur = QUIZ_STAGE_RANK[quizStage] || 0;
    if (next <= cur) return;
    quizStage = name;
    try { sessionStorage.setItem(QUIZ_STAGE_KEY, name); } catch (e) {}
  }

  function pulse(beat, workId, extra) {
    try {
      if (typeof window.gtag !== "function") return;
      const params = workId ? { work: String(workId) } : {};
      // EX-PICSTAT (INV-41): the work's public id also rides as the registered `pic` dimension on
      // EVERY work-carrying beat, kept apart from the event-target `work` (INV-6) so GA can cross-tab
      // any beat per work. One stamp here covers all nine work-carrying beats — no per-site copy.
      if (workId) params.pic = String(workId);
      // a closed BAKED-ladder word rides a beat that owns one (gift_kind, lang) — never free text (INV-1)
      if (extra) for (const k in extra) params[k] = extra[k];
      // EX-AB (INV-91): every dealt arm rides EVERY registry beat as a dimension, keyed by the
      // experiment's name; flag off / no arm dealt ⇒ no key (INV-60 stands) — no beat lays variant-blind
      for (const abK in abArms) params[abK] = abArms[abK];
      // EX-STORY-AB: the declared story variant rides every beat too — the frame's stamp (INV-41 stands)
      if (storyVariant) params.story_variant = storyVariant;
      // EX-QUIZ-FLOW (INV-69): the quiz stage is a funnel step rather than an arm — it keeps the
      // SAME two walk beats as a dimension; never a sixth beat (INV-41 stands)
      if (quizStage && (beat === "walk_unfold" || beat === "walk_exit")) {
        params.quiz_stage = quizStage;
      }
      window.gtag("event", beat, params);
    } catch (e) {}
  }

  // EX-PULSE measurement extension (INV-79): coarse CLOSED-LADDER buckets — a raw number never rides
  // the wire (INV-1), only a fixed word, so the honest picture stays closed-vocabulary.
  function lagBucket(ms) {
    return ms < 300 ? "instant" : ms < 1000 ? "quick" : ms < 3000 ? "slow" : "late";
  }
  function gapBucket(ms) {
    const H = 36e5, D = 24 * H;
    return ms < H ? "hour" : ms < D ? "day" : ms < 7 * D ? "week" : ms < 30 * D ? "month" : "far";
  }

  // ---- EX-TIME-READ (INV-41): the arrival's load, read as ONE coarse beat -------
  // `door_ready` lays ONCE per arrival, at the EARLIEST of the door's five windows decoding, a pick
  // crossing into a room, or the guest leaving before either (the leaving arm best-effort at
  // page-hide). It carries a `load_stage` — the FURTHEST reached rung of the closed ladder
  // paint · script · door · static · dynamic — plus a per-stage `lag_<stage>` reusing story_told's
  // round-trip ladder (lagBucket). No raw number ever rides the wire (INV-1) — the marks are the
  // tab's own clock (performance.now, ms since navigation start), read only as a bucket word.
  const LOAD_LADDER = ["paint", "script", "door", "static", "dynamic"];
  const stageAt = {};                                  // stage -> ms since navigation start
  function markStage(stage) {
    if (stageAt[stage] == null) stageAt[stage] = performance.now();
  }
  markStage("script");                                 // the client is running — the script has arrived
  requestAnimationFrame(() => {                        // the first rAF lands just past first paint
    if (stageAt.paint != null) return;
    let t = null;
    try {
      const ps = performance.getEntriesByType("paint");
      const fp = ps.find((e) => e.name === "first-contentful-paint") ||
                 ps.find((e) => e.name === "first-paint");
      if (fp) t = fp.startTime;
    } catch (e) {}
    stageAt.paint = (t != null ? t : performance.now());
  });

  // ---- EX-ERROR (INV-41): a fault reports itself as its own coarse beat --------
  // A script error or an unhandled promise rejection lays ONE `error` beat carrying only a closed
  // `kind` (script · promise) and the furthest load `phase` reached — never the message, the stack,
  // or the url (INV-1), so a fault is a visible canary while no raw string ever rides the wire. Its
  // own moment, entered through the registry beside door_ready and inspect (the same INV-41 pattern).
  // Capped at ERROR_CAP per page so a looping fault cannot flood the tag (a closed number, off wire).
  const ERROR_CAP = 3;
  let errorsSent = 0;
  function loadPhase() {
    for (let i = LOAD_LADDER.length - 1; i >= 0; i--) {
      if (stageAt[LOAD_LADDER[i]] != null) return LOAD_LADDER[i];
    }
    return "boot";
  }
  function reportError(kind) {
    if (errorsSent >= ERROR_CAP) return;
    errorsSent++;
    try { pulse("error", null, { kind: kind, phase: loadPhase() }); } catch (e) {}
  }
  try {
    // default (bubbling) listener — an uncaught script exception only; a resource load error does
    // not bubble to window, so image fallbacks (im.onerror) stay the picture layer's own affair.
    window.addEventListener("error", () => reportError("script"));
    window.addEventListener("unhandledrejection", () => reportError("promise"));
  } catch (e) {}

  // ---- EX-FRICTION (INV-41 / INV-99): frustration reports itself as its own coarse beat -------
  // A visitor who taps a dead spot again and again, or swipes while the walk is already at its end
  // (going nowhere), is stuck — a signal invisible in the analytics until now. ONE `friction` beat
  // carries only a closed `friction_kind` (tap · swipe) and a coarse `where` (door · walk · zoom) —
  // never a coordinate, a delta, or a count (INV-1). Capped per page like the error beat so a
  // genuinely-stuck guest lays a bounded count, never a flood. All thresholds are [default], his tune.
  const FRICTION_CAP = 3;
  const FRICTION_TAPS = 4;        // taps in one spot that read as frustration
  const FRICTION_TAP_MS = 1200;   // the burst window
  const FRICTION_TAP_PX = 44;     // a fingertip — the burst stays in one place
  const FRICTION_SWIPES = 4;      // stuck (no-move) steps in a row that read as frustration
  const FRICTION_SWIPE_MS = 2000; // the stuck-swipe window
  let frictionSent = 0;
  function frictionWhere() {
    if (zoomOpen) return "zoom";
    if (atDoor) return "door";
    return "walk";
  }
  function reportFriction(kind) {
    if (frictionSent >= FRICTION_CAP) return;
    frictionSent++;
    try { pulse("friction", null, { friction_kind: kind, where: frictionWhere() }); } catch (e) {}
  }
  // rage-tap: repeated taps on a NON-interactive surface, landing in one spot in quick succession —
  // the guest taps and nothing answers. A press on a button / link / window is intent, never counted
  // (and it breaks any running burst), so the closing screen's «ещё 5» and the door windows never
  // read as friction.
  let tapBurst = [];               // {t, x, y} within the live window, anchored on the first
  try {
    addEventListener("pointerdown", (e) => {
      if (e.target && e.target.closest
          && e.target.closest("button, a, [role=button], input, select, textarea, label")) {
        tapBurst = []; return;
      }
      const now = performance.now(), x = e.clientX, y = e.clientY;
      tapBurst = tapBurst.filter((p) => now - p.t <= FRICTION_TAP_MS);
      if (tapBurst.length) {
        const a = tapBurst[0];
        if (Math.abs(x - a.x) > FRICTION_TAP_PX || Math.abs(y - a.y) > FRICTION_TAP_PX) tapBurst = [];
      }
      tapBurst.push({ t: now, x: x, y: y });
      if (tapBurst.length >= FRICTION_TAPS) { reportFriction("tap"); tapBurst = []; }
    }, { passive: true });
  } catch (e) {}
  // rage-swipe: fed from stepFrame — a step that clamps at an end and moves NOWHERE. A real browse
  // that advances a frame clears the burst, so only going-nowhere thrashing ever lays the beat.
  let stuckBurst = [];
  function noteStuckStep() {
    const now = performance.now();
    stuckBurst = stuckBurst.filter((t) => now - t <= FRICTION_SWIPE_MS);
    stuckBurst.push(now);
    if (stuckBurst.length >= FRICTION_SWIPES) { reportFriction("swipe"); stuckBurst = []; }
  }

  // EX-LOAD-3 (INV-73): the Save-Data class law's ONE home — a single predicate every client-side
  // picture prefetch consults (the walk's one-ahead, the door's candidate warm, the crossing's
  // pick-time warm). A browser asking to save data warms NOTHING; the pictures then load on the
  // step itself through the in-view ladder (EX-LOAD-2).
  function dataSaver() {
    try { return !!(navigator.connection && navigator.connection.saveData); }
    catch (e) { return false; }
  }

  let doorReadyLaid = false;                            // door_ready lays ONCE per arrival (INV-41)
  function furthestStage() {
    let f = "paint";
    for (const s of LOAD_LADDER) if (stageAt[s] != null) f = s;
    return f;
  }
  function layDoorReady() {
    if (doorReadyLaid) return;
    doorReadyLaid = true;
    if (stageAt.paint == null) stageAt.paint = performance.now();
    const reached = furthestStage();
    const extra = { load_stage: reached };
    for (const s of LOAD_LADDER) {                      // a lag word for each stage the arrival reached
      if (stageAt[s] != null) extra["lag_" + s] = lagBucket(stageAt[s]);
      if (s === reached) break;
    }
    pulse("door_ready", null, extra);                  // pulse stamps the experiment arm like every beat
  }
  // the leaving arm: the guest departs before the door decodes or a pick — best-effort at page-hide
  // (a beacon may be lost for the fastest bounces; the read's own caption owns that honesty).
  addEventListener("visibilitychange", () => { if (document.hidden) layDoorReady(); });
  addEventListener("pagehide", layDoorReady);

/*!01-knobs-lang-history.js*/
  // ---- EX-RESET (INV-35): the ?reset address — the museum forgets THIS browser --
  // One wipe, named keys only, BEFORE anything restores; the param strips itself via
  // replaceState — no history step laid (INV-32 fenced) and the pre-strip URL leaves
  // history with it; a storage refusal never blocks the arrival; a sibling window's
  // later save re-creates state by INV-26's last-writer rule.
  if (new URLSearchParams(location.search).has("reset")) {
    // EX-PASS §10.3 names "reset" among the surfaces that stand in front of the walk, but this road
    // runs at BOOT — before 01a-pass.js's own `let passNav` has left the temporal dead zone — so
    // calling interrupt() here would throw on every ?reset visit rather than no-op quietly. Nothing
    // can be mid-transaction this early regardless (no declare has run yet), so there is nothing for
    // interrupt to do; the surfaces that stand in front of an ALREADY-WALKING visitor (zoom, quiz,
    // gift, door, series, popstate) are the ones actually wired.
    try { localStorage.removeItem(KEY); } catch (e) {}
    try { localStorage.removeItem(TEMPO_KEY); } catch (e) {}
    try { sessionStorage.removeItem(PLACE_KEY); } catch (e) {}
    try { sessionStorage.removeItem("@@NS@@-pass"); } catch (e) {}   // the session's seam overrides go too (EX-PASS — forgetting is whole)
    try { sessionStorage.removeItem(SPENT_KEY); } catch (e) {}  // the hash re-seeds a FIRST arrival
    try { sessionStorage.removeItem(ORIGIN_KEY); } catch (e) {}  // the remembered channel forgets too (EX-SHARE-ORIGIN)
    try { localStorage.removeItem(VISITOR_KEY); } catch (e) {}   // forgetting is whole (EX-MEMORY)
    try { localStorage.removeItem(HAND_KEY); } catch (e) {}
    try { localStorage.removeItem(SEENC_KEY); } catch (e) {}
    try { localStorage.removeItem(DOORDEALT_KEY); } catch (e) {}  // the door forgets its shown-round memory (EX-RESET/INV-75)
    try { localStorage.removeItem(LANG_KEY); } catch (e) {}     // the browser's tongue returns
    try { localStorage.removeItem(LAST_KEY); } catch (e) {}     // the return-gap clock resets (EX-PULSE/INV-79 — forgetting is whole)
    try { localStorage.removeItem(EXITS_KEY); } catch (e) {}    // the exit counter resets (EX-RETURN/INV-78 — the farewell starts over)
    try { localStorage.removeItem(SOLO_KEY); } catch (e) {}     // the hour's one-work asks reset (EX-STORY-FILL/INV-107 — forgetting is whole)
    try { localStorage.removeItem(SND_KEY); } catch (e) {}      // the museum forgets the sound choice (EX-SOUND)
    try { sessionStorage.removeItem(QUIZ_STAGE_KEY); } catch (e) {}   // EX-QUIZ-FLOW (INV-69): the stage wipes with the walk
    const q = new URLSearchParams(location.search);
    q.delete("reset");
    const rest = q.toString();
    try {
      history.replaceState(history.state, "",
        location.pathname + (rest ? "?" + rest : "") + location.hash);
    } catch (e) {}
  }

  let cfg, data;
  try {
    [cfg, data] = await Promise.all([
      fetch("config.json").then((r) => r.json()),
      fetch("exhibition_data.json").then((r) => r.json()),
    ]);
  } catch (e) {
    document.documentElement.classList.remove("js");  // static face returns NOW (CS-8/INV-25)
    return;
  }
  tlog("data");

  // ---- feel knobs, all from config (INV-28) ---------------------------------
  const EX = cfg.exhibition || {};
  // EX-I18N built-ins (INV-42): every one of these fires ONLY when the baked greet cache itself is
  // entirely absent (a malformed/flag-off build) — the source tongue is ENGLISH, never a locale
  // literal (SPEC "No Russian ever ships to a non-Russian walk").
  const ASK_EN = "what feels closer now?";
  const ENJOY_EN = "enjoy — it's yours to keep";
  const SERIES_EN = "series";
  const ROOM_BACK_EN = "← room";
  const MORE_EN = "{n} more";
  const UNTITLED_EN = "untitled";
  const A11Y_CLOSE_EN = "close";
  const A11Y_VOLUME_EN = "volume";
  const A11Y_SOUND_EN = "sound";
  // N7-A11Y (INV-102): accessible names for the four modal layers + the walk frame's roledescription;
  // each localizes through EX-I18N (T.a11y_*), the fallback ENGLISH (source tongue), never a locale literal
  const A11Y_ZOOM_EN = "closer look";
  const A11Y_ROOM_EN = "series";
  const A11Y_GIFT_EN = "a gift";
  const A11Y_QUIZ_EN = "a question";
  const A11Y_PHOTO_EN = "photograph";
  const SOUND_GREET_EN = "music";           // EX-SOUND-GREET (INV-101): first-visit greeting, source tongue (a plain invitation, no question mark)
  const clampInt = (x, dflt, lo, hi) => {
    const n = parseInt(x, 10);
    return Number.isFinite(n) ? Math.max(lo, Math.min(hi, n)) : dflt;
  };
  const SPREAD = clampInt(EX.spread_size, 10, 3, 12);   // the hang shows ~10, never the catalogue
  const UNFOLD = clampInt(EX.unfold_step, 5, 1, 12);
  const MAXU = clampInt(EX.max_unfolds, 2, 0, 5);       // «ещё 5» retires after this (INV-30)
  // EX-STORY-LEAD: how many works of the FIRST spread the opening plot covers. The rest of that
  // spread is told by a second plot, asked as the visitor comes near it. Most visits rest inside the
  // first few works, so the opening ask buys what a visit actually reads and the deeper walk pays
  // for its own reading as it happens (his 2026-07-28 word, read against the walk's own record).
  const STORY_LEAD = clampInt(EX.story_lead, 3, 1, 12);
  const DOOR_SIZE = clampInt(EX.door_size, 5, 3, 5);    // works at the threshold (EX-DOOR)
  // EX-DOOR-3 (door_diversity): when the bake ships the block, the door deals a FRESH, evenly-spread,
  // place-guaranteed set every open (variety over the session-held hand — his word 2026-07-12). Absent
  // ⇒ the curated hand stands exactly as before (the byte-identical fallback, INV-19).
  const DIVERSE = !!(EX.door_diversity);
  const clamp01 = (x) => Math.max(0, Math.min(1, x));
  const PLACE_MIN = clamp01((EX.door_diversity && Number(EX.door_diversity.place_min_fraction)) || 0.6);
  // INV-75: each open shows at least this fraction of works NOT dealt since the last round reset
  const FRESH_MIN = clamp01((EX.door_diversity && Number(EX.door_diversity.fresh_min)) || 0.6);
  // EX-MOTION: ONE clock for CSS and JS — config tempo, a visitor/test override in
  // localStorage['ex-tempo'] clamped to [0.05, 3]; stillness (reduced motion) wins over both
  const REDUCED = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const TEMPO = (() => {
    if (REDUCED) return 0.05;
    let o = NaN;
    try { o = parseFloat(localStorage.getItem(TEMPO_KEY)); } catch (e) {}
    const t = Number.isFinite(o) ? o : Number(EX.tempo) || 1.35;
    return Math.min(3, Math.max(0.05, t));
  })();
  if (!REDUCED) document.documentElement.style.setProperty("--tempo", String(TEMPO));
  // EX-CAPTION (INV-98): the narrow-screen type-step is an owner knob — engine default one step, 0
  // disables. The CSS below 400px reads --cap-narrow-step; set it here so the instance needs nothing.
  document.documentElement.style.setProperty(
    "--cap-narrow-step", String(clampInt(EX.caption_narrow_step, 1, 0, 2)));
  const COLD = EX.cold_spread || "diverse";
  const ARC = EX.arc_shape || "widening";
  const AXES = EX.kinship_axes || "all";
  const CAP = SPREAD + MAXU * UNFOLD;
  const GPLACE = ["ask", "top", "off"].indexOf(EX.greeting) >= 0 ? EX.greeting : "ask";
  // the room permalink's canonical root (EX-SHARE-BTN): the copied line is the SITE's,
  // clean of whatever params/host the sharer's own address carries
  const ROOT_URL = String(cfg.site_url || location.origin).replace(/\/+$/, "");

  // ---- the greeting (EX-GREET): the visitor's own words, at their own hour ---
  // Language = the browser's own setting; hour = the device clock. Strings are the BAKED
  // cache riding exhibition_data.json (EX-GREET-BAKE) — no cache, no greeting, the door
  // stands on its built-in lines (it never blocks entry).
  const GREET = data.greet || null;
  // ONE reader of the guest's tongue (EX-LANG, prover L1): the chosen override outranks the
  // browser everywhere a language is read — the greeting, the strings, the any-locale fetch.
  let langOverride = null;
  try {
    const lo = localStorage.getItem(LANG_KEY);
    if (lo && /^[a-z]{2,3}$/.test(lo)) langOverride = lo;
  } catch (e) {}
  function viewerLang() {
    return (langOverride || navigator.language || "").toLowerCase().slice(0, 2);
  }
  function greetLang() {
    if (!GREET || !GREET.langs) return null;
    let code = viewerLang();
    code = (GREET.aliases || {})[code] || code;
    if (!GREET.langs[code]) code = GREET.fallback || "en";
    const t = GREET.langs[code];
    return t ? { code, t } : null;
  }
  function greetLine(t) {
    const h = new Date().getHours();
    const part = h < 6 ? "night" : h < 12 ? "morning" : h < 18 ? "day" : "evening";
    const pool = (t.greet || {})[part] || [];
    if (!pool.length) return "";
    const day = new Date().toISOString().slice(0, 10);   // date-seeded like the door rotation
    let s = 0;
    for (const c of day) s = (s * 31 + c.charCodeAt(0)) >>> 0;
    return pool[s % pool.length];
  }

  // ---- EX-RTL (INV-80): the WHOLE layout mirrors for a right-to-left tongue ----
  // The viewer's direction is the active locale's own `dir` — the baked greet set carries it (`he`
  // is `rtl`); an outsider RTL locale learns its dir when the any-locale layer answers, and respeak()
  // re-applies it then. Set on the DOCUMENT ROOT so the entire tree inherits it: the pinned chrome is
  // written in logical properties (inset-inline-*, text-align:start/end) that flip on this one flag,
  // so an RTL guest meets a mirrored interface and an LTR guest is byte-for-byte unchanged
  // (dir="ltr" is the document default — setting it explicitly changes no layout). Re-run on a manual
  // language pick and on an any-locale arrival (both reach respeak).
  function applyDocDir() {
    const L = greetLang();
    const de = document.documentElement;
    de.setAttribute("dir", L && L.t && L.t.dir === "rtl" ? "rtl" : "ltr");
    if (L && L.code) de.setAttribute("lang", L.code);
  }
  applyDocDir();

  // ---- honest Back (INV-32): the walk and the browser speak the same history --
  // Steps are laid per FACE (door | walk), never per frame; a door step CARRIES the
  // spread it showed; the ↗ place marker is per-tab (sessionStorage), one-shot.
  try { history.scrollRestoration = "manual"; } catch (e) {}
  const pushFace = (st) => { try { history.pushState({ @@NS@@: st }, ""); } catch (e) {} };
  const replaceFace = (st) => { try { history.replaceState({ @@NS@@: st }, ""); } catch (e) {} };

/*!01a-pass.js*/
  // ---- EX-PASS: the transition seam — live settings, one command, one landing owner -------------
  // The seam a visual transition layer plugs into. It draws NOTHING. With no layer registered the
  // walk's own glide (15-motion.js) runs exactly as it always did, so on the served walk this
  // fragment changes no pixel until a layer registers itself through passLayerSet.
  //
  // Every value below is a LIVE SETTING: a validated name with a range, a safe default, a source
  // ladder, an observable applied value and a recorded fallback. None is a compile-time constant.
  // Changing a registered value needs no rebuild. A rebuild belongs to a change of CAPABILITY —
  // a new name in the register, a new instrument, a new driver kind, a new shader branch — never
  // to a change of a registered value.
  //
  // Placed right after the knobs fragment because the in-view watcher (08) builds its observer at
  // EVALUATION time and reads landProgress from here; everything else is called from handlers,
  // long after the whole client has evaluated.
  //
  // The standard source ladder, first match wins: the session's own override, then the pair's
  // score, then the site's live config, then the built-in default. A descriptor may name its own
  // order; qualityTier and diagnostics do, because a per-pair score has no business setting them.
  const PASS_KEY = "@@NS@@-pass";
  const PASS_ORDER = ["session", "score", "site", "default"];
  const PASS_INSTRUMENTS = ["weave"];
  const PASS_DRIVERS = ["static", "phase", "velocity", "pointer", "capability"];
  const PASS_DRIVERS_BUILT = ["static"];
  const PASS_CURVES = ["linear", "smooth", "ease-in", "ease-out", "spline"];
  // A limit is part of the CAPABILITY, so raising one is a rebuild, never a setting.
  // `text` is the fence on a NAME — a setting name, a cause, an instrument name — and it keeps its
  // full force there. `intent` is a separate fence on the one field §4.4 calls prose: a score's
  // opening line, authored at build time, which the lab's own generator writes at about 250
  // characters. Reading one limit for both would have refused a real score for being a sentence.
  //
  // `bytes` IS AN OBSERVED BASELINE WITH ITS EVIDENCE, NOT A CHOSEN ROUND NUMBER. It stood at
  // 8192 B while the only score a pair could carry was the one a site wrote by hand. Since the
  // passage composer ships, a crossing's score is a serialised composed passage, and those were
  // measured: the delivery pack of 2026-08-15 (`plans/v2-b27cc41a8bf15346/`, built by the site's own
  // lab/build-delivery-v1.py) carries 7708 filled scores whose median weighs 7029 B and whose
  // LONGEST weighs 10 851 B, read as JSON.stringify writes them — the very measure passScoreCheck
  // applies below. At 8192 B, 1783 of those 7708 were refused before any instrument saw them, which
  // is 23.1 percent of everything the composer had to say. The baseline is therefore set at
  // 12 288 B: the shipped pack's longest score passes with 1 437 B to spare, and a score half again
  // as long as anything the composer has ever written still does not.
  // It is a CAPABILITY and not a setting — raising it is this rebuild — and the bake publishes it
  // into the settings record under `pass.capabilities`, so the composer measures a filled score
  // against the number the client actually applies instead of against a copy of it.
  // 2026-08-17 — `intent` MOVED FROM 400 TO 600 (U27 stage 0), and the move is a defect this unit
  // found rather than a budget it wanted. The composer writes the passage's intent as a sentence a
  // person reads — what holds, what travels, from which reading to which, and what the camera does
  // — and over the whole collection 1 004 of the 6 304 composed crossings write one longer than 400
  // characters, the longest at 507. Every one of them was refused WHOLE by this checker, with
  // «intent is no short text», so no composed crossing of that thousand could ever have played on
  // any road — the prebaked pack's included. 600 is the measured 507 plus about a fifth. The cap
  // itself stays: an intent is a sentence, not a place to put a payload.
  const PASS_LIMITS = { camera: 64, phases: 3, instruments: 8, curve: 128, text: 200,
                        intent: 600, bytes: 12288 };
  const PASS_SCORE_FIELDS = ["schema", "intent", "seed", "pair", "params"];
  // PASS-API §4.4a: two schema versions live at once. Version 2 carries the cue list a host plays;
  // version 1 keeps working, because such an address can already sit in a visitor's session store.
  const PASS_SCORE_FIELDS2 = ["schema", "intent", "pair", "seed", "duration", "direction",
                              "interruption", "failLand", "camera", "cues", "quality", "provenance",
                              "chromeReveal"];

  // The register. `def` is the safe default; `kind` decides the check.
  // landProgress — where in a frame's travel the walk calls the arriving work current. 0.55 is
  // today's value, carried over so the seam changes no behaviour; it is a setting like any other.
  // landCommit — who commits the arriving work: the in-view watcher, or the transition's end.
  // flightMs — the transition's own duration; 0 hands the duration back to the walk's glide.
  const PASS_REG = {
    landProgress: { kind: "number", min: 0, max: 1, def: 0.55 },
    landCommit: { kind: "enum", of: ["observe", "transitionEnd"], def: "observe" },
    flightMs: { kind: "number", min: 0, max: 4000, def: 0 },
    phaseWindows: { kind: "ratio3", def: [0.25, 0.5, 0.25] },
    cameraTrack: { kind: "points", max: PASS_LIMITS.camera, def: [] },
    // instrumentNames — the instruments a transition may name, as a list of names off the
    // allow-list. THE NAME IS THE REGISTER'S OWN and it is not the record's. The bake writes the
    // instrument ADDRESS record — one entry per instrument, each with its file, version and digest
    // — into the settings block under `pass.instruments` (engine/build.py), and this register once
    // carried a setting of that same name. The register's site rung reads the settings block by the
    // name, so every resolve handed a record to a check that wants a list, and «setting
    // `instruments`: wants a list» went onto the refusal ring about four times per step — the ring
    // holds 64 rows, so within ten steps it had pushed every real refusal off (U10 §5 had to read
    // the layer's own refusal one step into the visit for exactly that reason). The record's name
    // is the landed contract of PASS-API §4.4d and the site's own delivery check reads it, so the
    // record keeps it and the register's setting takes a name of its own.
    instrumentNames: { kind: "names", of: PASS_INSTRUMENTS, max: PASS_LIMITS.instruments, def: [] },
    qualityTier: { kind: "enum", of: ["rich", "standard", "lean"], def: "standard",
                   order: ["session", "site", "default"] },
    visualLayer: { kind: "enum", of: ["off", "pass"], def: "off" },
    diagnostics: { kind: "enum", of: ["off", "on"], def: "off",
                   order: ["session", "site", "default"] },
    // familySeed — the seed the visit's own family roll runs on (§4.4f). Zero, the default, means
    // this visit rolls a seed of its own, which is the public bar: a crossing's bounded handles
    // land where no other visit's landed and every public run exists once. Any other number PINS
    // the visit, and a run at a pinned seed reproduces its predecessor to the pixel — the judging
    // mode. It resolves on the session, site and default rungs alone: a per-pair score has no
    // business setting the mode a whole visit is judged in, exactly as it has none for the tier or
    // the diagnostics switch.
    familySeed: { kind: "number", min: 0, max: 4294967295, def: 0,
                  order: ["session", "site", "default"] },
  };

  const passEvents = [];
  const passRefusals = [];
  const passApplied = {};
  function passNote(list, row) { list.push(row); if (list.length > 64) list.shift(); }

  // ?pass=landProgress:0.531,diagnostics:on writes the session store once, the way ?reset writes its
  // wipe once, then the address strips itself so the walk's own address stays clean.
  function passSession() {
    try {
      const o = JSON.parse(sessionStorage.getItem(PASS_KEY) || "{}");
      return (o && typeof o === "object") ? o : {};
    } catch (e) { return {}; }
  }
  (function () {
    const q = new URLSearchParams(location.search);
    const raw = q.get("pass");
    if (!raw) return;
    const put = passSession();
    raw.split(",").forEach((pair) => {
      const i = pair.indexOf(":");
      if (i <= 0) return;
      const k = pair.slice(0, i).trim(), v = pair.slice(i + 1).trim();
      if (!PASS_REG[k]) { passNote(passRefusals, { what: "setting", name: k, why: "unknown name" }); return; }
      put[k] = /^-?\d*\.?\d+$/.test(v) ? parseFloat(v) : v;
    });
    try { sessionStorage.setItem(PASS_KEY, JSON.stringify(put)); } catch (e) {}
    q.delete("pass");
    const rest = q.toString();
    try {
      history.replaceState(history.state, "",
        location.pathname + (rest ? "?" + rest : "") + location.hash);
    } catch (e) {}
  })();

  // One value, checked. Returns {ok, value, why}. A refused value never reaches the walk; the
  // caller falls back and the report says so, so a bad setting is visible instead of silent.
  function passCheck(d, v) {
    if (v === undefined || v === null) return { ok: false, why: "absent" };
    const k = d.kind;
    if (k === "number") {
      const n = typeof v === "number" ? v : parseFloat(v);
      if (!Number.isFinite(n)) return { ok: false, why: "no number" };
      if (n < d.min || n > d.max) return { ok: false, why: "outside " + d.min + "…" + d.max };
      return { ok: true, value: n };
    }
    if (k === "enum") {
      const s = String(v);
      return d.of.indexOf(s) < 0 ? { ok: false, why: "outside the named set" } : { ok: true, value: s };
    }
    if (k === "ratio3") {
      if (!Array.isArray(v) || v.length !== PASS_LIMITS.phases) return { ok: false, why: "wants three shares" };
      const a = v.map(Number);
      if (a.some((x) => !Number.isFinite(x) || x < 0 || x > 1)) return { ok: false, why: "a share outside 0…1" };
      if (Math.abs(a[0] + a[1] + a[2] - 1) > 0.001) return { ok: false, why: "the shares miss 1" };
      return { ok: true, value: Object.freeze(a) };
    }
    if (k === "points") {
      if (!Array.isArray(v)) return { ok: false, why: "wants a list" };
      if (v.length > d.max) return { ok: false, why: "over " + d.max };
      const pts = [];
      for (let i = 0; i < v.length; i++) {
        const p = v[i];
        if (!p || typeof p !== "object" || Array.isArray(p)) return { ok: false, why: "no record" };
        if (Object.keys(p).some((f) => ["at", "x", "y", "scale"].indexOf(f) < 0)) {
          return { ok: false, why: "unknown field" };
        }
        const at = Number(p.at);
        if (!Number.isFinite(at) || at < 0 || at > 1) return { ok: false, why: "outside 0…1" };
        pts.push(Object.freeze({ at: at, x: Number(p.x) || 0, y: Number(p.y) || 0,
                                 scale: Number.isFinite(Number(p.scale)) ? Number(p.scale) : 1 }));
      }
      return { ok: true, value: Object.freeze(pts) };
    }
    if (k === "names") {
      if (!Array.isArray(v)) return { ok: false, why: "wants a list" };
      if (v.length > d.max) return { ok: false, why: "over " + d.max };
      const out = [];
      for (let i = 0; i < v.length; i++) {
        const s = String(v[i]);
        if (s.length > PASS_LIMITS.text) return { ok: false, why: "name too long" };
        if (d.of.indexOf(s) < 0) return { ok: false, why: "no allow-list" };
        out.push(s);
      }
      return { ok: true, value: Object.freeze(out) };
    }
    return { ok: false, why: "no check" };
  }

  // The driver graph. A setting's value may be a plain value (a static driver, written short) or a
  // record naming how the frame's value is found: base + phase-curve + velocity-response +
  // pointer-response. Only the static kind is BUILT here; the rest are part of the declared schema,
  // validate like any other, and fall back to their base with the fallback recorded. Nonlinear shape
  // rides named curves and spline points from the score — the format accepts no expression and no
  // executable field.
  function passDriver(d, v) {
    if (v === null || v === undefined || typeof v !== "object" || Array.isArray(v) || !v.driver) {
      const plain = passCheck(d, v);
      return plain.ok
        ? { ok: true, node: { driver: "static", base: plain.value, curve: null, points: null, supported: true } }
        : { ok: false, why: plain.why };
    }
    if (Object.keys(v).some((f) => ["driver", "base", "curve", "points"].indexOf(f) < 0)) {
      return { ok: false, why: "driver names an unknown field" };
    }
    const kind = String(v.driver);
    if (PASS_DRIVERS.indexOf(kind) < 0) return { ok: false, why: "driver on no allow-list" };
    const base = passCheck(d, v.base);
    if (!base.ok) return { ok: false, why: "driver base " + base.why };
    let curve = null, points = null;
    if (v.curve !== undefined) {
      curve = String(v.curve);
      if (PASS_CURVES.indexOf(curve) < 0) return { ok: false, why: "curve on no allow-list" };
    }
    if (v.points !== undefined) {
      if (!Array.isArray(v.points)) return { ok: false, why: "points want a list" };
      if (v.points.length > PASS_LIMITS.curve) return { ok: false, why: "over " + PASS_LIMITS.curve };
      const pts = v.points.map(Number);
      if (pts.some((x) => !Number.isFinite(x))) return { ok: false, why: "a point is no number" };
      points = Object.freeze(pts);
    }
    const built = PASS_DRIVERS_BUILT.indexOf(kind) >= 0;
    if (!built) passNote(passRefusals, { what: "driver", name: kind, why: "declared, drawn by no renderer yet — the base stands" });
    return { ok: true, node: { driver: built ? kind : "static", asked: kind, base: base.value,
                               curve: curve, points: points, supported: built } };
  }

  function passRawFrom(src, key, score) {
    if (src === "session") return passSession()[key];
    if (src === "score") return (score && score.params) ? score.params[key] : undefined;
    if (src === "site") return (((EX && EX.pass) || (cfg && cfg.pass) || {}))[key];
    if (src === "default") return PASS_REG[key].def;
    return undefined;
  }
  // Resolve one name against the ladder, recording what was asked, who won, what got applied.
  function passResolve(key, score) {
    const d = PASS_REG[key];
    const order = d.order || PASS_ORDER;
    let asked, from = null, why = null, node = null;
    for (let i = 0; i < order.length; i++) {
      const src = order[i];
      const raw = passRawFrom(src, key, score);
      if (raw === undefined || raw === null) continue;
      const got = passDriver(d, raw);
      if (got.ok) { asked = raw; from = src; node = got.node; break; }
      if (why === null) { asked = raw; why = got.why; }
      passNote(passRefusals, { what: "setting", name: key, source: src, why: got.why });
    }
    if (from === null) { node = passDriver(d, d.def).node; from = "default"; }
    passApplied[key] = Object.freeze({
      name: key, asked: asked === undefined ? null : asked, source: from, applied: node.base,
      driver: node.asked || node.driver, supported: node.supported,
      fallback: why !== null || from === "default", why: why });
    return Object.freeze(node);
  }
  // The one convenience read for code that wants a value now (the watcher's threshold, the layer
  // switch). Anything inside a running transition reads the frozen snapshot instead.
  function passGet(key, score) { return passResolve(key, score).base; }

  // The score: a versioned record with an allow-list of fields. An unknown field refuses the WHOLE
  // score, so a typo lands as a refusal in the report instead of half-applying.
  function passScoreCheck(raw) {
    if (!raw || typeof raw !== "object" || Array.isArray(raw)) return { ok: false, why: "no record" };
    let bytes = 0;
    try { bytes = JSON.stringify(raw).length; } catch (e) { return { ok: false, why: "does not write out" }; }
    // The refusal names the size it MEASURED beside the fence it applied. A score refused for its
    // weight is refused for a number, and a reason that gives only the fence leaves the one thing
    // its author has to act on unsaid.
    if (bytes > PASS_LIMITS.bytes) {
      return { ok: false, why: "weighs " + bytes + " bytes, over the " + PASS_LIMITS.bytes
                             + " a score may weigh" };
    }
    const v = raw.schema;
    if (v !== 1 && v !== 2) return { ok: false, why: "names no schema 1 or 2" };
    const stray = Object.keys(raw).filter(
      (k) => (v === 2 ? PASS_SCORE_FIELDS2 : PASS_SCORE_FIELDS).indexOf(k) < 0);
    if (stray.length) return { ok: false, why: "unknown field «" + stray[0] + "»" };
    if (raw.intent !== undefined && (typeof raw.intent !== "string" || raw.intent.length > PASS_LIMITS.intent)) {
      return { ok: false, why: "intent is no short text" };
    }
    if (raw.seed !== undefined && !Number.isFinite(Number(raw.seed))) return { ok: false, why: "seed is no number" };
    const p = raw.params;
    if (p !== undefined) {
      if (!p || typeof p !== "object" || Array.isArray(p)) return { ok: false, why: "params is no record" };
      const bad = Object.keys(p).filter((k) => !PASS_REG[k]);
      if (bad.length) return { ok: false, why: "params names «" + bad[0] + "», in no register" };
      const shut = Object.keys(p).filter((k) => (PASS_REG[k].order || PASS_ORDER).indexOf("score") < 0);
      if (shut.length) return { ok: false, why: "«" + shut[0] + "» is closed to a score" };
    }
    return { ok: true, score: raw, read: v };
  }

  // A SCORE PER PAIR CANNOT COVER A DEALT WALK. The walk deals its works afresh each visit and
  // orders them by its own arc, so a pair scored ahead of time essentially never comes up; and a
  // collection of 121 works holds about fourteen thousand ordered pairs, which one whole score each
  // would make ~50 MB of settings file. So a site may carry, beside `pass.scores`:
  //   pass.scoreTemplates[<instrument>]  one score with its per-pair numbers left empty and its
  //                                      slots named — cue, roles, levels, window, doors, camera,
  //                                      quality, interruption and driver graph, all of it the same
  //                                      whatever two works are in hand;
  //   pass.scoreTables[<instrument>]     one row per ordered pair, carrying ONLY that pair's
  //                                      measured numbers.
  // Filling a template's named slots from a row is a data operation: nothing is measured in the
  // browser, so the law that measuring and casting happen at build time keeps its full force. A pair
  // with no row hands back nothing and the walk's own glide runs, exactly as a pair with no score of
  // its own always has; a row the template cannot take is refused WHOLE and says why, the same way a
  // score naming an unknown field is.
  // `readiness` is the one row field that fills no slot: it is the pair's own measured readiness,
  // and the row is refused outright when it stands under the table's floor — the same floor the
  // build-time walk applies, carried in the table so the refusal needs no measurement here. The
  // score is built on a COPY of the template, so a row refused halfway leaves nothing behind.
  // ---- family breath (§4.4f) ---------------------------------------------------------------------
  // A ROW MAY SAY WHAT MAY BREATHE. Filling a row's measured numbers exactly means a pair flipped
  // twice inside one visit plays one score byte for byte — the defect the site's own U9 measurement
  // read on four flips of one pair. The charter asks for the same family each time with small shifts
  // pass by pass, so a row may carry a family-bounds record naming, per SLOT it already fills, the
  // closed span the fill may roll that slot inside, and whether the score's own seed re-rolls.
  //
  // THE ROLL LIVES HERE, AND BOTH ROADS CALL IT. The inline road below fills from a template and a
  // table; the pack's reader fills from a shape's template and a shard's row in its own file. One
  // roll serves both — the reader is handed this function in its environment record — so the two
  // roads cannot drift into two ideas of what a family is. This function knows nothing about slot
  // paths or slot names: it is given the spans keyed however that road keys its slots and hands back
  // the rolled values under the same keys, and each road writes them through its own fill.
  //
  // THE SEED IS THE VISIT, THE PASS INDEX AND THE PAIR. The pass index is the generation `declare`
  // has already minted for the crossing being declared, so a pair flipped twice in one visit rolls
  // twice; the visit's seed keeps the whole visit apart from every other visit; and the pair's key
  // keeps two crossings declared at the same index from sharing a roll. Nothing here reads a clock:
  // a wall-time roll would make a pinned run irreproducible, which is the very thing §4.4b's
  // determinism row exists to hold.
  const passFamilies = [];
  let passVisit = 0, passVisitPinned = false;
  function passVisitSeed() {
    if (!passVisit) {
      // Read ONCE, at the first crossing that breathes, and held for the visit: a seed that
      // re-resolved per crossing would let a mid-visit change split one visit into two families.
      const pin = passGet("familySeed") >>> 0;
      passVisit = pin || ((Math.random() * 4294967296) >>> 0) || 1;
      passVisitPinned = !!pin;
    }
    return passVisit;
  }
  function passMix(a, b) {
    let h = Math.imul((a >>> 0) ^ 0x9e3779b9, 0x85ebca6b) >>> 0;
    h = Math.imul(h ^ (b >>> 0), 0xc2b2ae35) >>> 0;
    return (h ^ (h >>> 15)) >>> 0;
  }
  function passText(s) {
    let h = 2166136261 >>> 0;
    s = String(s);
    for (let i = 0; i < s.length; i++) h = Math.imul(h ^ s.charCodeAt(i), 16777619) >>> 0;
    return h >>> 0;
  }
  // The rolled values for one crossing, or a reason. A record that does not check out hands back a
  // reason and the caller refuses the WHOLE row — half a rolled score is the one outcome no road
  // here produces. A rolled value is checked against its own span before it is handed back: the
  // roll cannot produce one outside, so a value that lands there says the roll itself is broken, and
  // that is a refusal rather than a picture nobody can read back to a number.
  function passBreath(key, fam) {
    if (!fam || typeof fam !== "object" || Array.isArray(fam)) return { why: "its family bounds are no record" };
    const odd = Object.keys(fam).filter((f) => ["spans", "seed"].indexOf(f) < 0);
    if (odd.length) return { why: "its family bounds name «" + odd[0] + "», in no allow-list" };
    if (fam.seed !== undefined && typeof fam.seed !== "boolean") return { why: "its family seed is no yes-or-no" };
    const spans = fam.spans === undefined ? {} : fam.spans;
    if (!spans || typeof spans !== "object" || Array.isArray(spans)) return { why: "its family spans are no record" };
    const at = passGen, visit = passVisitSeed();
    const pass = passMix(passMix(visit, at), passText(key));
    const names = Object.keys(spans), v = {};
    for (let i = 0; i < names.length; i++) {
      const s = spans[names[i]];
      if (!Array.isArray(s) || s.length !== 2 || !Number.isFinite(+s[0]) || !Number.isFinite(+s[1])
          || +s[0] > +s[1]) {
        return { why: "the span for «" + names[i] + "» is no low-to-high pair of numbers" };
      }
      const lo = +s[0], hi = +s[1];
      const got = lo + (passMix(pass, passText(names[i])) / 4294967296) * (hi - lo);
      if (!(got >= lo && got <= hi)) {
        return { why: "the rolled «" + names[i] + "» " + got + " stands outside its span "
                      + lo + "…" + hi };
      }
      v[names[i]] = got;
    }
    const seed = fam.seed ? passMix(pass, 0x5eed5) / 4294967296 : null;
    passNote(passFamilies, { pair: key, at: at, visit: visit, pinned: passVisitPinned, seed: pass,
                             scoreSeed: seed, spans: spans, applied: v });
    return { v: v, seed: seed, at: at, visit: visit, seedOfPass: pass };
  }

  // ---- the composed road (§4.4d, U27 stage 0) ---------------------------------------------------
  // WHERE A SCORE COMES FROM. It is DERIVED, here, at the instant the walk casts the pair, from the
  // two works' own records. His word of 2026-08-17 19:21: the collection grows to thousands of works
  // and nothing on the product path may scale with the number of pairs. A table of pairs is
  // quadratic in the collection — 121 works are already 10 558 ordered pairs — while a record per
  // work is linear, and the whole living collection's records weigh 33 000 B gzipped where the pair
  // rows they replace weighed 1 862 611 B.
  //
  // WHAT LEFT WITH THE TABLE. Three roads used to answer for a pair's score, and all three are gone:
  // `pass.scores` keyed by ordered pair, the delivery pack read through pass-reader.js, and
  // `pass.scoreTables` filled into `pass.scoreTemplates`. So are the reader file, the shard warming
  // that fetched a work's outgoing crossings at every landing, and the site steps that staged and
  // copied the packs. A pair no longer has a score to find; it has one to derive.
  //
  // THE COMPOSER TRAVELS AS ITS OWN FILE, the way the picture layer and the instruments do. It is
  // fetched once, at the walk's first landing on a visit whose settings record actually carries the
  // records it reads and whose layer is on, and a visit that never reaches that state never asks for
  // it. Nothing ever waits on it: a crossing declared before it has arrived answers nothing and
  // falls through to the walk's own glide, exactly as a pair with no score always has. What stays
  // HERE is the door — where the composer is asked for, the request the walk builds for it, and the
  // one synchronous question a declare puts to it.
  const PASS_COMPOSER_SRC = "pass-composer.js";
  let passComposer = null, passComposerAsked = false, passComposerState = "absent";
  let passComposerSaid = null;
  const passPassages = [];
  function passWorkRecords() { return (((EX && EX.pass) || (cfg && cfg.pass) || {})).works; }
  function passComposerConsts() { return (((EX && EX.pass) || (cfg && cfg.pass) || {})).composer; }
  // The composer hands over a factory rather than a finished composer, so the bundle stays the one
  // owner of the settings block: the composer is handed the collection's own constants and reaches
  // nothing else in this file.
  function passComposerSet(part) {
    passComposer = null;
    const mk = part && part.make;
    if (typeof mk !== "function") {
      passComposerState = "refused";
      passNote(passRefusals, { what: "composer", name: PASS_COMPOSER_SRC,
                               why: "handed over no composer" });
      return;
    }
    try { passComposer = mk(passComposerConsts()) || null; } catch (e) { passComposer = null; }
    passComposerState = passComposer ? "read" : "refused";
    if (!passComposer) {
      passNote(passRefusals, { what: "composer", name: PASS_COMPOSER_SRC,
                               why: "the collection's constants made no composer" });
    }
  }
  function passComposerOpen() {
    if (passComposerAsked) return;
    const works = passWorkRecords(), consts = passComposerConsts();
    if (!works || typeof works !== "object" || !Object.keys(works).length) return;
    if (!consts || typeof consts !== "object" || !Object.keys(consts).length) return;
    if (passGet("visualLayer") !== "pass") return;
    // THE STAND-DOWN LAW BINDS THIS FETCH AS A CLASS (EX-LOAD-3 / INV-73), the same way it bound the
    // pack's. `passOpen` below reads the same two questions and stands the drawing machinery down,
    // so a visit under either request plays no crossing at all — fetching the file that decides one
    // would be a fetch for a crossing that can never run.
    const no = REDUCED ? "reduced motion" : dataSaver() ? "save data" : null;
    if (no) {
      passComposerAsked = true;
      passNote(passRefusals, { what: "composer", name: PASS_COMPOSER_SRC, why: no });
      return;
    }
    passComposerAsked = true;
    passComposerState = "asked";
    try {
      window.__@@NS@@PassComposer = passComposerSet;
      const s = document.createElement("script");
      s.src = PASS_COMPOSER_SRC;
      s.async = true;
      s.onerror = () => {
        passComposerState = "absent";
        passNote(passRefusals, { what: "composer", name: PASS_COMPOSER_SRC, why: "load failed" });
      };
      document.head.appendChild(s);
    } catch (e) {
      passComposerState = "absent";
      passNote(passRefusals, { what: "composer", name: PASS_COMPOSER_SRC, why: "no door" });
    }
  }

  // THE DIE THE WALK ROLLS, once per crossing. Charter shelf 16: a pinned seed reproduces a run
  // exactly, which is the judging mode, and the public walk rolls a fresh one each time, which is
  // the viewer mode. Both fall out of `passVisitSeed` above with no second idea of what a seed is —
  // the visit's own seed (pinned by `familySeed` or rolled once), the pass index the declare has
  // already minted, and the edge's own key. Nothing here reads a clock.
  //
  // The span is the composer's own and is READ from it: the choice core fences its seed at 0…8 and
  // the meshing instrument's manifest publishes the same span for its `seed` handle. A copy of it
  // here would be a copy that goes stale.
  function passSeedFor(key) {
    const span = (passComposer && passComposer.seedSpan) || [0, 8];
    const lo = +span[0], hi = +span[1];
    const roll = passMix(passMix(passVisitSeed(), passGen), passText(key)) / 4294967296;
    return lo + roll * (hi - lo);
  }

  // THE PASSAGE REQUEST the walk builds for one edge (§4.7, U27 stage 0). The edge is named in ONE
  // order whichever way the visitor walks it — the two ids sorted — and `direction` says which way
  // this passage runs, so A to B and B to A are two distinct passages of one edge and the site's own
  // edge record has a stable key to hang on (§4.8, stage 1 lane C).
  //
  // `routeRole` and `sessionMemory` are left unsaid here on purpose. The walk of stage 0 authors no
  // dramaturgy and keeps no edge memory, and the composer's own defaults — a middle, and nothing
  // played on this edge yet — are what reproduces today's score exactly. Stage 1 and stage 2 fill
  // them at this one place.
  function passRequestFor(fromEl, toEl) {
    const from = fromEl && fromEl.dataset ? fromEl.dataset.id : null;
    const to = toEl && toEl.dataset ? toEl.dataset.id : null;
    if (!from || !to) return null;
    const works = passWorkRecords() || {};
    const forward = String(from) <= String(to);
    const a = works[forward ? from : to], b = works[forward ? to : from];
    if (!a || !b) return null;
    return {
      workRecordA: a,
      workRecordB: b,
      direction: forward ? "a-to-b" : "b-to-a",
      seed: passSeedFor(String(forward ? from : to) + "__" + String(forward ? to : from)),
      // The pose the camera rests in as the passage starts: the departing work's real box in the
      // hang at this instant, measured off the DOM by the walk's own `hangGeometry`.
      cameraState: hangGeometry(from),
      // The buffer as it stands on this device at this moment. The instrument reads the one it is
      // actually drawing on, which is the truth either way (his architecture decision of 18:00);
      // this is what the walk can see from outside it.
      buffer: { width: innerWidth, height: innerHeight, dpr: window.devicePixelRatio || 1,
                orientation: innerWidth >= innerHeight ? "landscape" : "portrait",
                quality: passGet("qualityTier") },
    };
  }

  // The pair's own passage, derived. This road never waits and never fetches: a composer that has
  // not arrived answers nothing, the reason goes on the diagnostic surface, and the crossing falls
  // through to the walk's own glide exactly as a pair with no score always has. A named refusal from
  // the composer takes the same road, which is what a refusal has always meant here.
  function passComposeFor(fromEl, toEl) {
    if (!passComposer) {
      // ONCE PER STATE, never once per crossing. The refusal ring holds 64 rows and a row written
      // at every step pushes every real refusal off it inside ten steps — the defect U10 §5 read on
      // the register's own settings row. A composer that has not arrived is one fact about the
      // visit, so it is said once and said again only when that fact changes.
      if (passComposerSaid !== passComposerState) {
        passComposerSaid = passComposerState;
        passNote(passRefusals, { what: "composer", name: PASS_COMPOSER_SRC,
                                 why: "asked for a crossing before it arrived: "
                                      + passComposerState });
      }
      return null;
    }
    const request = passRequestFor(fromEl, toEl);
    if (!request) {
      passNote(passRefusals, { what: "composer", name: "request",
                               why: "one of the two works carries no record on this walk" });
      return null;
    }
    let passage = null;
    try { passage = passComposer.passageFor(request); } catch (e) { passage = null; }
    if (!passage) {
      passNote(passRefusals, { what: "composer", name: "passage", why: "the entry threw" });
      return null;
    }
    // ONE RECORD CARRIES THE WHOLE PASSAGE: what was asked, what came back, and — written on later,
    // when the host reports — what the instrument applied on the buffer it drew on or the refusal it
    // named. `applied` is the runtime truth and it cannot be known before the frame is drawn.
    passNote(passPassages, passage);
    if (passage.declined) {
      passNote(passRefusals, { what: "passage", name: passage.key, why: passage.declined });
      return null;
    }
    return passage.score;
  }

  // WHAT THE INSTRUMENT APPLIED, written back onto the passage that asked for it. The host publishes
  // each live cue's own handles on its report, and an instrument that holds a door for itself
  // publishes what it moved and why there — the meshing one names `sizeRequest`, the size it drew,
  // how many rungs apart they stand, the leak it was holding against, and the refusal where no whole
  // size stood within reach. That reading is the runtime truth (his architecture decision of
  // 2026-08-17 18:00), and it belongs on the passage record beside the request that asked for it.
  // `key` is optional: without one the passage this walk derived last is the one that just played,
  // which is what the landing asks about.
  function passApply(key) {
    let row = null;
    for (let i = passPassages.length - 1; i >= 0; i--) {
      if (key === undefined || passPassages[i].key === key) { row = passPassages[i]; break; }
    }
    if (!row || row.declined) return null;
    let rep = null;
    try { rep = passLayer && passLayer.report ? passLayer.report() : null; } catch (e) {}
    if (!rep) return null;
    row.applied = {
      instrument: rep.instrument,
      buffer: rep.census ? rep.census.buffer : null,
      dpr: rep.census ? rep.census.dpr : null,
      // `handles` is what the HOST resolved and asked each cue for. `applied` is what the INSTRUMENT
      // published about its own door on the buffer it drew on, through the frame state's
      // `reportApplied` — the request it was handed, the value it drew, how far apart the two stand,
      // the leak it was holding against, and the refusal where no whole value stood within reach.
      // The two travel side by side because the edge is read against both: the plan's intention and
      // the run-time truth.
      cues: (rep.stack || []).map((v) => ({ id: v.id, instrument: v.instrument,
                                            handles: v.handles || null,
                                            applied: v.applied || null })),
    };
    return row.applied;
  }

  // Every setting resolves ONCE, at nav-start, and the result is frozen onto the command. A live
  // change lands on the NEXT transition; the geometry and the camera of a transition already in
  // flight stay as they were. A setting whose descriptor names a way to apply live may travel inside
  // the flight; none does yet, so a running transition is fully frozen.
  function passSnapshot(score) {
    const out = {};
    Object.keys(PASS_REG).forEach((k) => { out[k] = passResolve(k, score); });
    return Object.freeze(out);
  }

  let passGen = 0;
  let passNav = null;
  let passPending = null;
  let passLastEl = null, passLastGen = -1;
  function passWhere(el) {
    if (!el) return null;
    // PASS-API §1.1: the door is a destination like any other. It carries no dataset.id of its own
    // (it is not a work), so it is named by its element id instead — the one case passWhere resolves
    // by anything other than dataset.
    if (el.id === "ex-door") return Object.freeze({ id: "door", n: null });
    return Object.freeze({ id: (el.dataset && el.dataset.id) || null,
                           n: (el.dataset && el.dataset.n) ? +el.dataset.n : null });
  }
  // The marks carry their own prefix, so the walk's existing timings keep their exact shape and the
  // suite's mark counts stay honest; the seam's own suite filters this prefix.
  function passMark(name, cmd, extra) {
    const row = { at: Math.round(performance.now()), name: name,
                  gen: cmd ? cmd.gen : 0, kind: cmd ? cmd.kind : null, cause: cmd ? cmd.cause : null,
                  from: cmd && cmd.from ? cmd.from.id : null, to: cmd && cmd.to ? cmd.to.id : null,
                  why: extra || null };
    passNote(passEvents, row);
    try { performance.mark("@@NS@@-pass:" + name, { detail: row }); }
    catch (e) { try { performance.mark("@@NS@@-pass:" + name); } catch (e2) {} }
  }
  // A held-back landing always lands, never strands.
  function passFlush() {
    const p = passPending; passPending = null;
    if (p) { passLastEl = p.el; passLastGen = passGen; p.commit(p.el, "flush"); }
  }
  function passEnd(name, why) {
    if (!passNav) return;
    const cmd = passNav; passNav = null;
    passFlush();
    passMark(name, cmd, why);
  }
  // The one place a transition is declared. Every road that moves the visitor from one work to
  // another comes through here — the stepping input AND every programmatic jump — so the state
  // contract is the same for all of them, whatever the picture does.
  function passStart(a) {
    passEnd("nav-abort", "superseded");
    passGen += 1;
    const g = passGen;
    let score = null;
    const raw = a.score || passComposeFor(a.fromEl, a.toEl);
    if (raw) {
      const seen = passScoreCheck(raw);
      if (seen.ok) {
        score = seen.score;
        // The checker says which version it read (§4.4a). A version-1 score is read forward: its
        // five fields keep feeding the settings ladder exactly as they always did, and it names no
        // cue — so no instrument takes the command and the walk's glide plays, which is what a
        // version-1 score has always meant. The reading is recorded rather than assumed.
        if (seen.read === 1) {
          passNote(passRefusals, { what: "score", name: "schema 1",
                                   why: "read forward: params feed the ladder, no cue to play" });
        }
      } else passNote(passRefusals, { what: "score", name: raw.intent || "unnamed", why: seen.why });
    }
    const cmd = Object.freeze({
      gen: g,
      from: passWhere(a.fromEl), to: passWhere(a.toEl),
      dir: (+a.dir < 0) ? -1 : 1,
      span: Math.abs(+a.span || 0),
      kind: a.kind === "jump" ? "jump" : "step",
      cause: String(a.cause || "step").slice(0, PASS_LIMITS.text),
      velocity: +a.velocity || 0,
      reduced: !!REDUCED,
      saveData: !!dataSaver(),
      rtl: (document.documentElement.getAttribute("dir") === "rtl"),
      dpr: window.devicePixelRatio || 1,
      viewport: Object.freeze({ w: innerWidth, h: innerHeight }),
      params: passSnapshot(score),
      // The score travels frozen ON the command, so the host reads the cue, the duration and the
      // fail policy of THIS transaction and never a live value that moved under it mid-flight.
      score: score,
      signal: Object.freeze({ get aborted() { return g !== passGen; } }),
    });
    passNav = cmd;
    passMark("nav-start", cmd);
    return cmd;
  }
  function passLandNow() { passEnd("nav-land", null); }
  function passAbortNow(why) { passEnd("nav-abort", why || "cancelled"); }

  // ---- ProductNavigationAdapter (PASS-API §1.1) -------------------------------------------------
  // declare(a) is the ONE door every road between two works now knocks on — the stepping road and
  // every programmatic jump alike. It adds the two locks §1.1 names on top of passStart's freeze:
  //   - a command whose destination is absent is refused outright (never reaches passStart, never
  //     mints a generation) — the class of defect a null-destination jump could leave behind (a
  //     landing keyed on the destination has nothing to read).
  //   - two declares inside one animation frame make the second a refusal with its reason; a declare
  //     arriving while another is merely RUNNING still supersedes it (passStart's own job, unchanged)
  //     — only the same-frame race is new law.
  let passFrameLock = false;
  function passFrameUnlock() { passFrameLock = false; }
  function declare(a) {
    if (!a || !a.toEl) {
      passNote(passRefusals, { what: "declare", name: (a && a.cause) || "unnamed", why: "no destination" });
      return null;
    }
    if (passFrameLock) {
      passNote(passRefusals, { what: "declare", name: a.cause || "unnamed", why: "second declare in one frame" });
      return null;
    }
    passFrameLock = true;
    try { requestAnimationFrame(passFrameUnlock); } catch (e) { passFrameLock = false; }
    return passStart(a);
  }
  // A programmatic move — a restored place, a pasted link, a closed room, a rotation, a fresh hang,
  // the Back arrow. It takes the SAME command and the same landing owner, so the state contract
  // covers every road between two works; the picture layer declines it by kind, so the eye still
  // sees an instant land. A jump with no destination is refused by declare and lands nothing.
  function passJump(toEl, cause, fromEl) {
    const cmd = declare({ fromEl: fromEl || null, toEl: toEl || null, dir: 1, span: 0,
                          kind: "jump", cause: cause, velocity: 0 });
    if (cmd) passLandNow();
    return cmd;
  }

  // dock(cmd) — PASS-API §1.1/§2.4: makes the arriving work current, exactly once, keyed on the
  // command's OWN frozen generation together with its destination (never the live global passGen,
  // which is exactly the key the seam got wrong — §10.2). Called by the host on settle/fail/cancel;
  // reads cmd.to and takes no element, so a caller cannot dock a work the command never named.
  const passDockKeys = Object.create(null);
  function passResolveEl(to) {
    if (!to) return null;
    if (to.id === "door" || to.id === null) return { id: "exh-fin" };  // the door's own landing clears
    return stage.querySelector('.exh-frame[data-id="' + String(to.id).replace(/"/g, "") + '"]');
  }
  function dock(cmd) {
    if (!cmd || !cmd.to) return;
    const key = cmd.gen + ":" + (cmd.to.id === null ? "" : cmd.to.id);
    if (passDockKeys[key]) {
      passNote(passRefusals, { what: "dock", name: key, why: "already docked" });
      return;
    }
    passDockKeys[key] = true;
    // THE RUNTIME TRUTH, READ AT THE LANDING. The instrument has finished drawing and the host's
    // report still carries what the last transaction left behind, so this is the one instant the
    // applied state can be written back onto the passage that asked for it. It reads and decides
    // nothing: a passage that was refused or never derived leaves the row untouched.
    if (cmd.score) passApply();
    const el = passResolveEl(cmd.to);
    // THE WALK'S REST RECORD FOLLOWS THE DOCK (INV-86). `restingEl` — the section under the eye,
    // the one a turn re-docks to — is written by the in-view watcher's organic intersection alone
    // (08). A crossing moves the eye without one: the walk's own scroll stands still for the whole
    // flight, and a device change arriving mid-flight brings some other section across the
    // threshold inside the watcher's own 250 ms reflow guard, so the report that would have named
    // the arriving work is the one report the guard swallows. The record then keeps naming the
    // DEPARTING work and the next turn honours it — the visitor is thrown back one work. The
    // landing is where the arriving work is known for certain, so the landing corrects the record.
    // A door landing carries no section of its own (passResolveEl hands back a plain marker), and
    // that is what the dataset check keeps out.
    if (el && el.dataset && document.body.contains(el)) restingEl = el;
    if (el) passLandGate(el, "dock", landOn, cmd.gen);
    passMark("dock", cmd, cmd.to.id === "door" ? "door" : null);
    // The chrome comes back HERE and nowhere else, so it can only ever follow the arrival. The
    // curtain has already dropped and the canvas has already been released (the host calls
    // handoff(cmd) before dock — §2.2 settle/fail), so this is the first instant the walk owns its
    // own pixels again. Focus travels with the chrome rather than standing apart from it: the
    // accessibility handoff is one of the chrome's named parts, and two owners would move focus
    // twice.
    chromeReveal(cmd);
  }

  // ---- hangGeometry (PASS-API §1.1) --------------------------------------------------------------
  // THE WORK'S REAL BOX in the exhibition layout at this instant, measured off the DOM. The walk
  // seats a work by CSS — max-height 82dvh, max-width 88vw, the work's own aspect kept, a 2px radius
  // — so only the element itself knows where it stands, and the number changes with every resize,
  // turn and re-hang. The renderer lays its own frame onto this box at both ends of a passage, which
  // is what makes the two handoffs exact instead of approximately right.
  //
  // The element measured is the PICTURE, never the section around it: the section is a full-viewport
  // grid cell and says nothing about where the work hangs inside it.
  function hangGeometry(workId) {
    const el = passResolveEl({ id: workId });
    const im = (el && el.querySelector) ? el.querySelector("img.work") : null;
    if (!im || !im.getBoundingClientRect) return null;
    const r = im.getBoundingClientRect();
    if (!r.width || !r.height) return null;
    // The walk shows a work WHOLE, so its crop is 1 and its fit contains rather than covers. Both
    // are READ rather than assumed, because a layout that ever crops must say so here instead of
    // letting the renderer seat a whole work into a cropped box. The radius and any transform the
    // layout applies travel with them for the same reason.
    const cs = getComputedStyle(im);
    return Object.freeze({
      workId: workId, x: r.left, y: r.top, w: r.width, h: r.height,
      fit: cs.objectFit || "fill", crop: 1,
      radius: parseFloat(cs.borderTopLeftRadius) || 0,
      transform: cs.transform === "none" ? null : cs.transform,
      dpr: window.devicePixelRatio || 1,
      orientation: innerWidth >= innerHeight ? "landscape" : "portrait",
    });
  }

  // handoff(cmd) — the DOM's work is shown and the renderer's canvas released inside ONE frame.
  // The work's own reveal carries an opacity transition on the walk's road (it fades in as the
  // visitor scrolls to it); a passage has already drawn that work, so the transition is switched off
  // for this one reveal and the picture is simply there. Nothing fades, and no frame draws neither
  // picture: the DOM is revealed FIRST and the canvas dropped after, inside the same task.
  // THE WALK IS PLACED AT THE ARRIVING WORK. A takeover returns before the walk's own glide ever
  // runs (15-motion.js: an offer that is taken returns), so nothing else moves the walk, and the
  // work a passage arrived at would be revealed a viewport away from the eye. The placement is
  // instant — the passage was the animation, and a second one here would be the walk travelling
  // twice — and it is called once under cover, mid-passage, while the renderer's canvas stands at
  // the whole frame and nothing of the walk is in sight.
  //
  // `place` asks for that placement alone. Called without it the whole handoff runs: the work's own
  // reveal carries an opacity transition on the walk's road, and a passage has already drawn that
  // work, so the transition is switched off for this one reveal and the picture is simply there.
  // Nothing fades, and no frame draws neither picture — the DOM is revealed FIRST and the canvas
  // dropped after, inside the same task.
  function handoff(cmd, place) {
    if (!cmd || !cmd.to) return;
    const el = passResolveEl(cmd.to);
    const im = (el && el.querySelector) ? el.querySelector("img.work") : null;
    if (im) scrollTo(0, frameCenter(el));
    if (place) { passMark("place", cmd, null); return; }
    if (im) { im.style.transition = "none"; im.style.opacity = "1"; }
    if (el && el.classList) el.classList.add("seen");
    curtain(false);
    passMark("handoff", cmd, null);
  }

  // ---- chromeReveal (PASS-API §1.1) --------------------------------------------------------------
  // The walk's own chrome comes back after the arrival and the handoff, ONCE per command, with its
  // parts named: the title and plaque, the counter, share, the sound control, the series and control
  // affordances, and the focus and accessibility handoff. The timing is data a score may name; with
  // no score naming it the default below plays, so a site that writes no timing still gets the whole
  // choreography.
  //
  // SOUND IS SHOWN, NEVER TOUCHED. The control is put back on screen; whether it is playing, at what
  // volume, and what the visitor asked for are the sound player's own state and cross a passage
  // untouched.
  // The six parts and the millisecond each waits by default. One record names them, so the parts a
  // score may time and the parts the choreography plays can never drift apart.
  //
  // THE REVEAL IS ONCE BECAUSE THE LANDING IS ONCE. dock is its only caller, and dock already keeps
  // the one ledger that says whether this command has landed — keyed on the command's own
  // generation together with its destination (§2.4/§10.2). A second ledger here would be a second
  // home for one fact, and the two could disagree; the conformance rows measure the reveal count
  // across every exit rather than trusting either.
  const PASS_CHROME_MS = { plaque: 0, counter: 0, share: 90, sound: 90, series: 140, focus: 0 };
  function chromeReveal(cmd) {
    if (!cmd || !cmd.to) return;
    const el = passResolveEl(cmd.to);
    const named = (cmd.score && cmd.score.chromeReveal) || {};
    // Four of the six are one element each, put back by the very class the walk already shows them
    // with. `series` stands up the series and control affordances, which live INSIDE the plaque the
    // landing wrote — one body class carries them together. `focus` is the accessibility handoff.
    const one = { plaque: cap, counter: counter, share: shareBtn,
                  sound: document.getElementById("ex-sound") };
    Object.keys(PASS_CHROME_MS).forEach((name) => {
      const asked = Number(named[name]);
      const ok = Number.isFinite(asked) && asked >= 0 && asked <= 2000;
      if (named[name] !== undefined && !ok) {
        passNote(passRefusals, { what: "chrome", name: name, why: "outside 0…2000 ms" });
      }
      const go = () => {
        try {
          if (one[name]) one[name].classList.add("show");
          else if (name === "series") document.body.classList.add("ex-pass-chrome");
          else if (el && el.focus && !stage.contains(document.activeElement)) el.focus({ preventScroll: true });
        } catch (e) {}
        passMark("chrome-" + name, cmd, null);
      };
      const ms = ok ? asked : PASS_CHROME_MS[name];
      if (ms > 0) setTimeout(go, ms); else go();
    });
    passMark("chrome", cmd, null);
  }

  // glide(cmd) — the walk's own scroll animation, the standing fallback; called by the host when no
  // renderer takes the command (a decline, a timed-out prepare, or no renderer registered at all).
  function glide(cmd) {
    if (!cmd) return;
    const el = passResolveEl(cmd.to);
    if (el && el.getBoundingClientRect) glideToFrame(frameCenter(el), cmd.velocity || 0, "pass");
    else passLandNow();
  }

  // interrupt(reason) — PASS-API §1.1/§10.3: ends the transaction in flight from a product surface
  // that stands in front of the walk. Reaches the host too (a takeover the per-frame glide checker
  // never sees, because during a takeover that loop does not run) and then ends the bundle's own
  // bookkeeping the way passAbortNow always has.
  // The host is told FIRST, and unconditionally. The bundle's own bookkeeping can already have
  // landed while a renderer still holds the frame — a takeover whose command has flushed its
  // nav-land is exactly that state — and returning early on `passNav` left the renderer drawing
  // over a walk the product believed it had finished with. §10.3's whole claim is that a surface
  // standing in front of the walk reaches the renderer; it cannot depend on the bundle's own record.
  function interrupt(reason) {
    if (passLayer && typeof passLayer.cancel === "function") {
      try { passLayer.cancel(reason); } catch (e) {}
    }
    if (passNav) passAbortNow(reason);
  }

  // reframe(viewport) — the resize/orientation road tells a RUNNING transaction its frame changed
  // size, so it resizes in place instead of being superseded (§10.3's third repair).
  function reframe(viewport) {
    if (passLayer && typeof passLayer.resize === "function") {
      try { passLayer.resize(viewport); } catch (e) {}
    }
  }
  function passRunning() {
    try { return !!(passLayer && passLayer.report && passLayer.report().active); }
    catch (e) { return false; }
  }

  // curtain(on) — the host only. Covers the walk with the renderer's canvas and hides the covered
  // walk from the accessibility tree; the caption's own size/change watchers suspend with it. Focus
  // returns to the arriving work at the landing (dock already restores the plaque/counter/share).
  function curtain(on) {
    document.body.classList.toggle("ex-pass-curtain", !!on);
    if (on) { stage.setAttribute("aria-hidden", "true"); stage.inert = true; }
    else { stage.removeAttribute("aria-hidden"); stage.inert = false; }
    try {
      if (capRO) {
        if (on) capRO.disconnect();
        else { const im = capInViewImg(); if (im) capRO.observe(im); }
      }
    } catch (e) {}
    try {
      if (capMO) {
        if (on) capMO.disconnect();
        else capMO.observe(cap, { childList: true, subtree: true, characterData: true });
      }
    } catch (e) {}
  }

  // The one owner of «this work is now current». The in-view watcher (08) and the end of a
  // transition both arrive here. A work that is ALREADY the last one landed, inside the same
  // generation, is a repeat — that is the watcher re-reporting what is still on screen after a
  // rebuilt threshold, and it commits nothing twice. A visitor who walks back to a work does land
  // it again: the work between them moved the last-landed mark.
  // `gen` lets a caller pin the generation the check reads against instead of the LIVE passGen — the
  // host's own dock(cmd) passes cmd.gen, its command's own frozen generation, so a callback arriving
  // after a newer command has already declared still keys against the generation it actually belongs
  // to (PASS-API §10.2: keyed on generation AND destination, never a global that has moved on).
  function passLandGate(el, reason, commit, gen) {
    if (!el) return;
    // THE WALK LANDED. The composer is asked for HERE and nowhere else (§4.4d: warming happens at
    // the landing and nothing ever waits on the wire), because a crossing is declared the instant
    // the visitor moves and the passage is derived inside that same call — a fetch begun there could
    // never arrive in time. It is asked for once per visit; every landing after the first returns at
    // the first line. Nothing per work is fetched: one file decides every crossing of the walk.
    passComposerOpen();
    const g = gen === undefined ? passGen : gen;
    if (el === passLastEl && g === passLastGen) return;
    if (reason === "observe" && passNav && passNav.to
        && passNav.to.id === ((el.dataset && el.dataset.id) || null)
        && passGet("landCommit") === "transitionEnd") {
      passPending = { el: el, commit: commit };
      return;
    }
    passLastEl = el; passLastGen = g;
    commit(el, reason);
  }

  // A drawing layer registers itself here. With none registered — the state of this branch — every
  // command falls through to the walk's own glide, which is the fallback the seam keeps reversible:
  // turning the layer off is a setting, never a rebuild.
  let passLayer = null, passState = "absent";
  // PASS-API §12: the renderer's own file registers the HOST here — a registry taking one
  // instrument, exposing offer/resize/cancel/report. The seam's old {name, run} shape is gone with
  // the single run(cmd, done) entry point it belonged to (§0, "Where it stands").
  function passLayerSet(layer) {
    passLayer = (layer && typeof layer.offer === "function") ? layer : null;
    passState = passLayer ? "registered" : "absent";
  }
  function passVisualTakes(cmd) {
    if (!passLayer) return false;
    if (cmd.kind === "jump") return false;
    if (cmd.reduced || cmd.saveData) return false;
    return cmd.params.visualLayer.base === "pass";
  }
  // A layer that throws is dropped for the rest of the visit and the walk's glide takes at once. The
  // host owns the offer/prepare/decline decision entirely (§2.1); a `true` return means the host has
  // taken responsibility for landing this command — by taking over, or by calling the glide hook
  // itself when it declines — never that a renderer is now drawing.
  function passOffer(cmd) {
    try {
      return passLayer.offer(cmd, { dock: dock, glide: glide, curtain: curtain, mark: passMark,
                                    hangGeometry: hangGeometry, handoff: handoff }) === true;
    }
    catch (e) {
      passNote(passRefusals, { what: "layer", name: "offer", why: "threw" });
      passLayerSet(null);
      return false;
    }
  }

  // The drawing layer ships as its OWN file, fetched the first time a walk wants it: this bundle
  // carries the door and none of the picture. One request per visit, one capability probe, and
  // every refusal on the diagnostic surface. The walk keeps gliding throughout — the layer joins a
  // later transition when it arrives, and a visit where it never arrives is the walk as it is today.
  const PASS_SRC = "pass-layer.js";
  let passAsked = false, passAble = null;
  function passCan() {
    if (passAble === null) {
      try {
        const g = document.createElement("canvas").getContext("webgl2");
        passAble = !!g;
        const lose = g && g.getExtension("WEBGL_lose_context");
        if (lose) lose.loseContext();
      } catch (e) { passAble = false; }
    }
    return passAble;
  }
  function passOpen() {
    if (passAsked || passLayer) return;
    if (passGet("visualLayer") !== "pass") return;
    const no = REDUCED ? "reduced motion" : dataSaver() ? "save data" : passCan() ? null : "no webgl2";
    if (no) { passNote(passRefusals, { what: "layer", name: PASS_SRC, why: no }); passAsked = true; return; }
    passAsked = true;
    passState = "asked";
    try {
      window.__@@NS@@PassLayer = passLayerSet;
      const s = document.createElement("script");
      s.src = PASS_SRC;
      s.async = true;
      s.onerror = () => { passState = "absent"; passNote(passRefusals, { what: "layer", name: PASS_SRC, why: "load failed" }); };
      document.head.appendChild(s);
    } catch (e) { passState = "absent"; passNote(passRefusals, { what: "layer", name: PASS_SRC, why: "no door" }); }
  }

  // The diagnostic surface: technical rows only — the register, the lifecycle, the refusals, the
  // command in flight, and what the device reports. The told story, the quiz answers, the gift, the
  // visitor's own marks, the remembered place and anything the counting wire carries stay out by
  // construction: this function reads its own four lists and nothing else.
  function passPlain(params) {
    const out = {};
    Object.keys(params).forEach((k) => { out[k] = params[k].base; });
    return out;
  }
  function passReport() {
    return {
      version: 1,
      // resolved FRESH on every read: the register's rows report where each name stands NOW, so a
      // value changed mid-session is visible at once. What a running transition froze is a separate
      // row of its own, below, and the two never pretend to be the same reading.
      settings: Object.keys(PASS_REG).map((k) => { passResolve(k, null); return passApplied[k]; }),
      events: passEvents.slice(),
      refusals: passRefusals.slice(),
      nav: passNav ? { gen: passNav.gen, kind: passNav.kind, cause: passNav.cause,
                       to: passNav.to ? passNav.to.id : null, params: passPlain(passNav.params) } : null,
      device: { reduced: !!REDUCED, saveData: !!dataSaver(), dpr: window.devicePixelRatio || 1,
                webgl2: passAble, viewport: { w: innerWidth, h: innerHeight } },
      limits: PASS_LIMITS,
      drivers: { declared: PASS_DRIVERS.slice(), built: PASS_DRIVERS_BUILT.slice() },
      layer: passState,
      // The passage composer, on the same surface: where its file stands, how many work records the
      // settings record carries for it to read, and one row per passage this visit has derived —
      // the key, the request that was made, the shape that came back or the refusal that was named,
      // and what the instrument applied on the buffer it drew on. A picture that looks wrong reads
      // back to the request that made it without reading anything else.
      composer: { src: PASS_COMPOSER_SRC, state: passComposerState,
                  version: passComposer ? passComposer.version : null,
                  works: Object.keys(passWorkRecords() || {}).length,
                  passages: passPassages.map((row) => ({
                    key: row.key, request: row.request, shape: row.shape || null,
                    bytes: row.bytes === undefined ? null : row.bytes,
                    overTheFence: row.overTheFence === undefined ? null : row.overTheFence,
                    declined: row.declined || null, applied: row.applied || null })) },
      // The family roll, on the same surface (§4.4f): the visit's own seed and whether it was
      // pinned, and one row per rolled crossing carrying the pair, the pass index, the seed that
      // pass ran on, the spans it read and the value it applied to each bounded slot. A picture
      // that looks wrong reads back to the number that made it without reading anything else.
      family: { visit: passVisit || null, pinned: passVisitPinned, rolls: passFamilies.slice() },
    };
  }
  // `score` is the checker itself, handed over so a score can be judged without being played — the
  // surface stays read-only about the walk and decides nothing on its own. `adapter` and `layer` are
  // a TESTING seam, gated the same way: they let a conformance row construct a real command and drive
  // the host directly, on real elements, without needing to simulate every input road by hand.
  if (passGet("diagnostics") === "on") {
    try {
      window.__@@NS@@Pass = {
        report: passReport, score: passScoreCheck, version: 1,
        // `passage` is the ONE entry a passage comes through, handed over so a conformance row can
        // put a request to it directly and read the score or the named refusal that comes back,
        // without driving a whole walk to reach it. `request` builds the request the walk itself
        // would build for two real elements, so a row can prove the two agree.
        passage: function (req) { return passComposer ? passComposer.passageFor(req) : null; },
        request: passRequestFor, applied: passApply, seed: passSeedFor,
        adapter: { declare: declare, dock: dock, glide: glide, interrupt: interrupt,
                   reframe: reframe, curtain: curtain, mark: passMark,
                   hangGeometry: hangGeometry, handoff: handoff, chromeReveal: chromeReveal },
        layer: function () { return passLayer; },
      };
    } catch (e) {}
  }
/*!02-kinship-orderings.js*/
  // ---- baked data -----------------------------------------------------------
  const SERIES = data.series || [];                    // real series only (3+), variant each
  const VER = String(data.version || "1");
  const works = data.works;                 // [{id,img,slug,w,h,dom,title,sec,place}]
  const byId = Object.fromEntries(works.map((w) => [w.id, w]));
  const V = data.v;
  const DIM = V[works[0].id].length;
  const sel = Array.isArray(AXES) ? AXES.filter((i) => i >= 0 && i < DIM)
                                  : [...Array(DIM).keys()];
  const vec = (id) => sel.map((i) => V[id][i]);
  const dist = (a, b) => {
    let s = 0;
    for (let i = 0; i < a.length; i++) { const d = a[i] - b[i]; s += d * d; }
    return Math.sqrt(s);
  };

  // the door pool — baked provenance ∩ living works; thinner than door_size ⇒ NO door:
  // silent entry onto the default hang (the door never blocks entry, EX-DOOR)
  const doorPool = ((data.door || {}).pool || []).filter((e) => e && byId[e.id]);
  const doorAvailable = doorPool.length >= DOOR_SIZE;

  // ---- orderings ------------------------------------------------------------
  function coldOrder() {                    // maximally diverse (farthest-point)
    const ids = works.map((w) => w.id);
    if (COLD === "first") return ids.slice();
    const cx = vec(ids[0]).map((_, i) => ids.reduce((s, id) => s + vec(id)[i], 0) / ids.length);
    const order = [ids.reduce((b, id) => (dist(vec(id), cx) > dist(vec(b), cx) ? id : b))];
    const used = new Set(order);
    while (order.length < ids.length) {
      let best = null, bd = -1;
      for (const id of ids) {
        if (used.has(id)) continue;
        const md = Math.min(...order.map((c) => dist(vec(id), vec(c))));
        if (md > bd) { bd = md; best = id; }
      }
      order.push(best); used.add(best);
    }
    return order;
  }

  function arcOrder(pickId) {               // near neighbours drawn in, widening steps hold contrast
    const sorted = works.filter((w) => w.id !== pickId)
      .sort((a, b) => dist(vec(a.id), vec(pickId)) - dist(vec(b.id), vec(pickId)));
    const order = [pickId];
    const used = new Set(order);
    if (ARC === "nearest") {
      sorted.forEach((w) => { order.push(w.id); used.add(w.id); });
      return order;
    }
    let step = 1, i = 0;
    while (i < sorted.length) {
      const id = sorted[i].id;
      if (!used.has(id)) { order.push(id); used.add(id); }
      i += step; step = Math.max(1, Math.round(step * 1.6));
    }
    for (const w of sorted) if (!used.has(w.id)) { order.push(w.id); used.add(w.id); }
    return order;
  }

/*!03-quiz-seed-ab-story.js*/
  // ---- the told story's ORDER (EX-STORY-ORDER, INV-47) ----------------------
  // The light leans the order, and only leans it. Beside kinship (the arc's own metric) the story
  // adds ONE soft term — the hour-discontinuity over the authored time-of-day mark SETS — weighted
  // by story.light_weight (0 = pure kinship, high = a strict light march). Computed DETERMINISTICALLY
  // in code: the model writes lines, never the sequence (prover ST7), so the same pick yields the
  // same order and a stable cache key. It runs ONLY when the story is on; with the voice off the arc
  // stands exactly as today (the byte-identical guard, ST1). A two-hour work is a hinge; a `free`
  // work is a zero-cost wildcard — the arc drops it wherever it needs a breath or the turn.
  const SPINE = { day: 0, zenith: 0, sunset: 1, night: 2 };  // the light's own axis, dusk between
  function hourGap(todA, todB) {
    if (!todA || !todB || todA.indexOf("free") >= 0 || todB.indexOf("free") >= 0) return 0;
    let best = Infinity;
    for (const a of todA) { if (!(a in SPINE)) continue;
      for (const b of todB) { if (b in SPINE) best = Math.min(best, Math.abs(SPINE[a] - SPINE[b])); } }
    return best === Infinity ? 0 : best;
  }
  const todOf = (id) => (byId[id] && byId[id].tod) || ["free"];
  const STORY = (EX && EX.story) || {};
  function storyOrder(ids, opts) {
    opts = opts || {};
    const w = Number.isFinite(+opts.lightWeight) ? +opts.lightWeight : (STORY.light_weight || 0);
    const pool = ids.slice();
    const pick = opts.pick != null && pool.indexOf(opts.pick) >= 0 ? opts.pick : pool[0];
    const order = [pick];
    const used = new Set([pick]);
    while (order.length < pool.length) {
      const prev = order[order.length - 1];
      let best = null, bc = Infinity;
      for (const id of pool) {                 // greedy: kinship + w × the light seam, ties by pool order
        if (used.has(id)) continue;
        const c = dist(vec(prev), vec(id)) + w * hourGap(todOf(prev), todOf(id));
        if (c < bc) { bc = c; best = id; }
      }
      order.push(best); used.add(best);
    }
    return order;
  }
  // the story layer's own reachable surface (the walk calls storyOrder when ai_story is on; the
  // suite calls it directly). No axis name or vector ever crosses it — only ids and hour marks.
  try { window.@@NS_UPPER@@Story = { order: storyOrder, hourGap: hourGap }; window.CONFIG = cfg; } catch (e) {}

  // ---- the told story's VOICE (EX-STORY-LINE / EX-STORY-EDGE, INV-47) --------------------------
  // On when ai_story ships true. The hang leans by light (assembleOrder), and the ordered pick-set
  // is sent to /api/story; each returned line settles into its work's plaque told-slot (STORYLINES).
  // Any failure — flag off, worker down, malformed — is SILENCE: no line, the walk whole (CS-8).
  const STORY_ON = cfg.ai_story === true;
  const STORY_VARIANT = STORY.variant || "B";
  const LIGHT_W = Number.isFinite(+STORY.light_weight) ? +STORY.light_weight : 0.6;

  // ---- EX-QUIZ (INV-60/64/65/66): the per-work question chip + 4-option card -----------------
  // On when the quiz flag ships true AND the work carries public quiz data (baked into `w.quiz`).
  // PLACEMENT is a config knob (INV-28): an instance tunes where the «question?» chip advertises.
  // ONE question per show is chosen deterministically from the eligible set (INV-66); a cooldown
  // suppresses the chip for QUIZ_COOLDOWN_H hours after one show (no nagging repeats).
  const QUIZ_ON = cfg.quiz === true;
  const QUIZ_CFG = (EX && EX.quiz) || {};
  const QUIZ_PLACE = Array.isArray(QUIZ_CFG.placement) ? QUIZ_CFG.placement : ["plaque"];
  const QUIZ_COOLDOWN_H = Number.isFinite(+EX.quiz_cooldown_hours) ? +EX.quiz_cooldown_hours : 6;
  const QUIZ_SHOWN_KEY = "@@NS@@.quizshown";    // per-browser timestamp of the last quiz show
  const QUIZ_TAB_KEY = "@@NS@@.quiztab";        // a stable per-tab id when the coat-check is off
  const QUIZ_LS = (id) => "@@NS@@.quiz." + id; // per-work answered-memory key (not the coat-check)
  function quizHash(str) {
    let s = 0;
    for (const c of String(str)) s = (s * 31 + c.charCodeAt(0)) >>> 0;
    s = Math.imul(s ^ (s >>> 16), 0x45d9f3b) >>> 0;
    s = Math.imul(s ^ (s >>> 16), 0x45d9f3b) >>> 0;
    return (s ^ (s >>> 16)) >>> 0;
  }
  const QUIZ_TOKEN = (function () {
    try {                                    // the coat-check token when the museum remembers (EX-MEMORY)
      const v = localStorage.getItem(VISITOR_KEY);
      if (v && /^[a-z0-9]{8,40}$/.test(v)) return v;
      if (cfg.visitor_memory === true) {     // EX-AB (INV-90): the seed read MINTS the token when none
        let r = "";                          // exists yet, so visit 1 already deals off the token visit 2
        try {                                // holds (the mint mirrors EX-MEMORY's own, which then reuses it)
          const b = new Uint8Array(12);
          crypto.getRandomValues(b);
          r = Array.from(b, (x) => (x % 36).toString(36)).join("");
        } catch (e2) { r = Math.random().toString(36).slice(2, 14); }
        const t = r + Date.now().toString(36);
        localStorage.setItem(VISITOR_KEY, t);
        return t;
      }
    } catch (e) {}
    try {                                    // else a stable per-tab id — survives a reload within the walk
      let t = sessionStorage.getItem(QUIZ_TAB_KEY);
      if (!t) { t = Math.random().toString(36).slice(2) + Date.now().toString(36); sessionStorage.setItem(QUIZ_TAB_KEY, t); }
      return t;
    } catch (e) {}
    return "anon";
  })();
  // EX-AB (INV-90): the variant frame — at boot, ahead of any beat, deal each registered experiment
  // one arm off the visitor's seed by the pinned quizHash formula; equal split over the arms in order.
  // A degenerate entry (under two arms) stays undealt — the bake refuses those before they serve.
  const abArms = {};
  try {
    const ABREG = cfg.experiments || {};
    for (const abName in ABREG) {
      const abEntry = ABREG[abName] || {};
      const abList = Array.isArray(abEntry.arms) ? abEntry.arms : null;
      if (!abList || abList.length < 2) continue;
      const abU = quizHash(QUIZ_TOKEN + ":" + (abEntry.salt || abName)) / 4294967296;
      abArms[abName] = abList[Math.floor(abU * abList.length)];
    }
  } catch (e) {}
  // EX-QUIZ-ONCE (INV-66): ONE quiz chip per walk show, chosen deterministically from the eligible
  // set. eligible = works in the current order that carry a quiz AND are not yet answered.
  // The cooldown: a localStorage timestamp silences the chip for QUIZ_COOLDOWN_H hours after a show.
  let quizChosenId = null;
  function quizAnswered(id) {
    // widened answered-memory: old {prize:...} reads as answered; {answered:true,...} is new.
    try {
      const v = JSON.parse(localStorage.getItem(QUIZ_LS(id)) || "null");
      return !!(v && typeof v === "object" && (v.answered === true || v.prize));
    } catch (e) { return false; }
  }
  function quizCooldownActive() {
    try {
      const ts = Number(localStorage.getItem(QUIZ_SHOWN_KEY));
      return Number.isFinite(ts) && ts > 0 && (Date.now() - ts) < QUIZ_COOLDOWN_H * 3600000;
    } catch (e) { return false; }
  }
  function recomputeQuizChoice() {
    // eligible: works in the current ordered walk that carry a quiz AND are not already answered
    const seen = Object.create(null);
    const eligible = [];
    for (let i = 0; i < order.length; i++) {
      const id = order[i];
      if (seen[id]) continue; seen[id] = true;
      if (byId[id] && byId[id].quiz && !quizAnswered(id)) eligible.push(id);
    }
    if (!QUIZ_ON || quizCooldownActive() || eligible.length === 0) {
      quizChosenId = null;
      return;
    }
    quizChosenId = eligible[quizHash(QUIZ_TOKEN + ":once") % eligible.length];
    // stamp happens when the card is OPENED (quizCardOpen), not on pick: the pick is a
    // session-stable internal choice; the cooldown represents a card actually shown to the visitor.
    // EX-QUIZ-FLOW (INV-69): the chip rendering is the "shown" stage — every visitor with the flag
    // on and an eligible pick reaches this branch (the quiz_arm split retired 2026-07-28)
    quizStageUp("shown");
  }
  // a work surfaces its chip only when the flag is on and this is the chosen work
  const quizShows = (w) => QUIZ_ON && !!(w && w.quiz) && w.id === quizChosenId;
  // `_hash` is exported for the JS↔Python parity test (test_parity.py): the per-work pick and any
  // registry arm are drawn from this exact function, so the Python util must mirror it byte-for-byte.
  // `arms` exposes the whole dealt-arms map (EX-AB/INV-91) rather than one experiment's own arm, so
  // a test can read whichever live experiment's arm rides the beats without a per-experiment export.
  try { window.@@NS_UPPER@@Quiz = { chosen: () => quizChosenId, token: QUIZ_TOKEN, _hash: quizHash, arms: () => abArms }; } catch (e) {}
  const STORYLINES = Object.create(null);
  let storyVariant = null;          // the mode the served story reported — rides the GA beats (EX-STORY-AB)
  const toldPortions = new Set();   // portion keys whose plot has actually come back (told ONLY on a served plot)
  const askingPortions = new Set(); // portion keys with a request in flight (never double-ask the same portion)

/*!04-arrival-facts.js*/
  // ---- EX-PULSE/INV-79: the arrival's own facts — measured ONCE per load ------
  // Placed AFTER abArms/storyVariant are initialized: pulse() reads those dimension vars, so an
  // earlier call would hit their temporal dead zone and silently self-catch (the wire stays honest).
  // VIEWER LANGUAGE is the tongue the guest actually views in (a chosen override, else the browser),
  // whether or not they ever touch the door's tongue list — it tells RTL scope and which baked locales
  // earn their place; a raw locale never rides the wire, only a baked code (outsider ⇒ other), the same
  // closed ladder lang_pick uses (INV-1). RETURN GAP is how long since this browser last walked, a
  // COARSE bucket (never a raw timestamp) that sets a welcome-back window's bounds — laid only when a
  // prior visit is remembered. The last-visit clock lives in @@NS@@.last (forgotten whole on ?reset).
  // EX-RETURN/INV-78: the real gap since the last visit, captured HERE (at load, before @@NS@@.last is
  // overwritten below) and stashed for renderDoor — the welcome-back window reads THIS, never a fresh
  // now-minus-now of ~0. null when no prior visit is remembered (a first-ever arrival, or after ?reset).
  let returnGapMs = null;
  (function () {
    const vc = viewerLang();
    const vknown = (GREET && GREET.aliases && GREET.aliases[vc]) || vc;
    const vbaked = !!(GREET && GREET.langs && GREET.langs[vknown]);
    pulse("viewer_lang", null, { lang: vbaked ? vknown : "other" });
    let last = null;
    try { last = localStorage.getItem(LAST_KEY); } catch (e) {}
    const now = Date.now();
    if (last) {
      const gap = now - parseInt(last, 10);
      if (Number.isFinite(gap) && gap >= 0) {
        returnGapMs = gap;                             // reused by EX-RETURN's welcome-back window (one clock, INV-79)
        pulse("return_gap", null, { gap: gapBucket(gap) });
      }
    }
    try { localStorage.setItem(LAST_KEY, String(now)); } catch (e) {}
  })();

  // the hang's order: the kinship arc, leaned by light ONLY when the story is on (EX-STORY-ORDER,
  // ST1 — off is byte-for-byte today's arc). A greedy failure falls back to the plain arc.
  function assembleOrder(pickId) {
    const base = arcOrder(pickId);
    if (!STORY_ON || base.length < 2) return base;
    try {
      const leaned = storyOrder(base, { pick: pickId, lightWeight: LIGHT_W });
      return (leaned && leaned.length === base.length) ? leaned : base;
    } catch (e) { return base; }
  }

/*!05-door-deal-circle-walkstate.js*/
  // EX-DOOR-4 (INV-71): the walk's own in-session seen marks — every hung frame that has stood
  // in view THIS session, added the MOMENT the mark is made (pending flush included, since this
  // set is written synchronously in the intersection callback). It feeds the circle check and the
  // next deal's novelty voice even where the museum's memory (visitor_memory / ex.seenc) is off.
  const walkSeen = new Set();

  // EX-DOOR-3 (door_diversity): a FRESH, evenly-spread, place-guaranteed set every open. The pool
  // spans the whole living gallery (baked with five axes + a `place` flag). We min-max normalize the
  // five axes, SEED near the set's centre among the works UNSEEN this round (a random pick among the
  // closest few — the variety knob per open), then greedily add the work FARTHEST from the picked set
  // while keeping both quotas reachable: at least PLACE_MIN place works and at least FRESH_MIN works
  // unseen this round (INV-75 — else the farthest-point spread keeps surfacing the same extreme poles).
  // The unseen memory is per-round: when it can no longer honour either fraction the round resets and
  // the whole gallery is walked again. The ORDER varies too — a random axis and direction each open,
  // since there is no single right order over these axes.
  const DPARAMS = ["luma", "warmth", "colorful", "edge", "sym"];
  function dealDiverse(want) {
    const pool = doorPool;
    const n = Math.max(1, Math.min(want || DOOR_SIZE, pool.length));
    if (pool.length <= n) return pool.slice(0, n);
    const mins = {}, maxs = {};
    DPARAMS.forEach((p) => {
      let lo = Infinity, hi = -Infinity;
      pool.forEach((e) => { const v = Number(e[p]);
        if (Number.isFinite(v)) { if (v < lo) lo = v; if (v > hi) hi = v; } });
      mins[p] = lo; maxs[p] = hi;
    });
    const V = pool.map((e) => DPARAMS.map((p) => {
      const span = maxs[p] - mins[p];
      return span > 0 ? (Number(e[p]) - mins[p]) / span : 0;
    }));
    const d2 = (a, b) => { let s = 0; for (let i = 0; i < a.length; i++) { const t = a[i] - b[i]; s += t * t; } return s; };
    const minTo = (i, set) => { let m = Infinity; for (const j of set) { if (j === i) continue; const dd = d2(V[i], V[j]); if (dd < m) m = dd; } return m; };
    const isPlace = (i) => !!pool[i].place;
    // INV-75 — novelty across visits: the round memory of works this door has already dealt. Each open
    // must show ≥ FRESH_MIN works NOT in this memory (else the farthest-point spread, which always
    // gravitates to the same extreme poles, would show a returning phone visitor the same faces). When
    // the unseen pool can no longer honour the fresh OR the place fraction the round is SPENT — the
    // memory clears and a fresh round walks the whole gallery again (the just-dealt set re-seeds it).
    let shown = new Set();
    try {
      const s = JSON.parse(localStorage.getItem(DOORDEALT_KEY) || "null");
      if (s && s.v === VER && Array.isArray(s.ids)) s.ids.forEach((id) => shown.add(String(id)));
    } catch (e) {}
    const needPlace = Math.min(n, Math.ceil(PLACE_MIN * n));
    const needFresh = Math.min(n, Math.ceil(FRESH_MIN * n));
    // both fractions together want more than n works (0.6n + 0.6n > n), so some shown windows must be
    // BOTH unseen AND place — this many at least (the joint overlap the deal must honour):
    const overlapNeed = Math.max(0, needFresh + needPlace - n);
    let isFresh = (i) => !shown.has(String(pool[i].id));
    const tally = (pred) => { let c = 0; for (let i = 0; i < pool.length; i++) if (pred(i)) c++; return c; };
    // the round is spent when the unseen pool can't supply the fresh floor OR the fresh∧place overlap
    // both quotas jointly demand → clear it and walk the whole gallery again
    if (tally(isFresh) < needFresh || tally((i) => isFresh(i) && isPlace(i)) < overlapNeed) {
      shown = new Set();                                  // the round is spent → a new round over the whole pool
      isFresh = () => true;                               // every work is fresh again
    }
    // both quotas hold together because we only ADD a work when the remaining slots can still be filled
    // to meet the fresh AND place counts (a small feasibility test), and among the still-feasible works
    // we take the FARTHEST (spread), with stale works discounted so fresh is preferred while the pool is deep.
    const feasibleAfter = (cand, picked, fc, pc) => {
      const nfc = fc + (isFresh(cand) ? 1 : 0), npc = pc + (isPlace(cand) ? 1 : 0);
      const nSlots = n - picked.length - 1;              // slots left AFTER adding cand
      const rf = Math.max(0, needFresh - nfc), rp = Math.max(0, needPlace - npc);
      if (rf > nSlots || rp > nSlots) return false;
      let af = 0, ap = 0, afp = 0;                        // fresh / place / both, among unpicked ≠ cand
      for (let k = 0; k < pool.length; k++) {
        if (k === cand || picked.indexOf(k) >= 0) continue;
        const f = isFresh(k), p = isPlace(k);
        if (f) af++;
        if (p) ap++;
        if (f && p) afp++;
      }
      return af >= rf && ap >= rp && afp >= Math.max(0, rf + rp - nSlots);
    };
    // seed near the centre among FRESH works — a novel yet still-typical start each open
    const mean = DPARAMS.map((_, k) => V.reduce((s, v) => s + v[k], 0) / V.length);
    const freshIdx = pool.map((_, i) => i).filter(isFresh);
    const seedFrom = (freshIdx.length ? freshIdx : pool.map((_, i) => i))
      .sort((a, b) => d2(V[a], mean) - d2(V[b], mean));
    const seedK = Math.min(seedFrom.length, Math.max(3, Math.ceil(pool.length * 0.15)));
    const picked = [seedFrom[Math.floor(Math.random() * seedK)]];
    let fc = isFresh(picked[0]) ? 1 : 0, pc = isPlace(picked[0]) ? 1 : 0;
    while (picked.length < n) {                           // greedy farthest-point, quota-feasible + fresh-first
      let best = -1, bd = -Infinity, bestAny = -1, bdAny = -Infinity;
      for (let i = 0; i < pool.length; i++) {
        if (picked.indexOf(i) >= 0) continue;
        let md = minTo(i, picked);
        if (!isFresh(i)) md *= 0.15;                      // discount stale → fresh preferred while pool is deep
        if (md > bdAny) { bdAny = md; bestAny = i; }
        if (md > bd && feasibleAfter(i, picked, fc, pc)) { bd = md; best = i; }
      }
      const add = best >= 0 ? best : bestAny;             // feasibility keeps a candidate; fallback is a safety net
      picked.push(add);
      if (isFresh(add)) fc++;
      if (isPlace(add)) pc++;
    }
    const axis = Math.floor(Math.random() * DPARAMS.length);   // varying order: a random axis + direction
    const dir = Math.random() < 0.5 ? 1 : -1;
    picked.sort((a, b) => dir * (V[a][axis] - V[b][axis]));
    const hand = picked.map((i) => pool[i]);
    try {                                                 // remember what this open dealt (this round's memory)
      hand.forEach((e) => shown.add(String(e.id)));
      localStorage.setItem(DOORDEALT_KEY, JSON.stringify({ v: VER, ids: Array.from(shown).slice(-500) }));
    } catch (e) {}
    return hand;
  }

  // EX-DOOR-3 (INV-44): the hand LIVES — rotation + novelty + the hour, under HIS LAW
  // (a new hand repeats at most a THIRD of the previous one). The pool stays curated
  // (EX-DOOR-2d); his file order is the tie-break voice; a pool of exactly door_size
  // stands the law down (the hand IS the pool). `circleStamp` (EX-DOOR-4) records the circle
  // (pick + shown) this deal answered, so one circle earns exactly one deal.
  function dealHand(circleStamp) {
    if (DIVERSE) return dealDiverse(doorLayout().n);     // door_diversity: a fresh spread set every open
    const n = Math.min(DOOR_SIZE, doorPool.length);
    if (doorPool.length <= n) return doorPool.slice(0, n);
    let prev = [];
    try {
      const h = JSON.parse(localStorage.getItem(HAND_KEY) || "null");
      if (h && h.v === VER && Array.isArray(h.ids)) prev = h.ids;
    } catch (e) {}
    const seen = new Set(walkSeen);                    // the just-walked works count as met (EX-DOOR-4)
    try {
      const c = JSON.parse(localStorage.getItem(SEENC_KEY) || "null");
      if (c && Array.isArray(c.ids)) c.ids.forEach((id) => seen.add(String(id)));
    } catch (e) {}
    const hour = new Date().getHours();
    const part = hour < 6 ? "night" : hour < 12 ? "morning" : hour < 18 ? "day" : "evening";
    const tone = (e) => {
      const l = Number(e.luma), w = Number(e.warmth);
      if (!Number.isFinite(l) || !Number.isFinite(w)) return 0;
      if (part === "night") return 1 - l;              // the darker faces
      if (part === "evening") return w;                // the warmer
      return l;                                        // morning + day lean bright
    };
    const scored = doorPool.map((e, i) => ({
      e,
      s: (seen.has(String(e.id)) ? 0 : 2)              // novelty first (his pick)
         + tone(e) * 0.9                               // the hour leans
         - i * 0.01                                    // his order breaks ties
         + Math.random() * 0.25,                       // the rotation's own breath
    }));
    scored.sort((a, b) => b.s - a.s);
    const maxRepeat = Math.floor(n / 3);               // HIS LAW: ≤ a third repeats
    const hand = [];
    let repeats = 0;
    for (const c of scored) {
      const isPrev = prev.indexOf(c.e.id) >= 0;
      if (isPrev && repeats >= maxRepeat) continue;
      hand.push(c.e);
      if (isPrev) repeats += 1;
      if (hand.length === n) break;
    }
    for (const c of scored) {                          // the law can never starve the hand
      if (hand.length === n) break;
      if (hand.indexOf(c.e) < 0) hand.push(c.e);
    }
    const rec = { v: VER, ids: hand.map((e) => e.id) };
    if (circleStamp) rec.circle = circleStamp;         // remember the circle this deal answered
    try { localStorage.setItem(HAND_KEY, JSON.stringify(rec)); } catch (e) {}
    return hand;
  }
  function standingHand() {                            // the session keeps its set (INV-31/2d)
    if (DIVERSE) return null;                            // door_diversity overrides INV-31 for the door —
    // every open re-deals a fresh spread set (his word 2026-07-12); the walk behind still persists
    try {
      const h = JSON.parse(localStorage.getItem(HAND_KEY) || "null");
      if (h && h.v === VER && Array.isArray(h.ids)) {
        const by = Object.fromEntries(doorPool.map((e) => [e.id, e]));
        const sp = h.ids.map((id) => by[id]).filter(Boolean);
        if (sp.length >= Math.min(DOOR_SIZE, doorPool.length)) return sp;
      }
    } catch (e) {}
    return null;
  }
  function doorSet() { return standingHand() || dealHand(); }
  function shuffle(a) {                                 // Fisher–Yates, in place
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1)); const t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }
  function refreshHand() {
    if (DIVERSE) return dealDiverse(doorLayout().n);     // door_diversity: a reload deals fresh too (his word 2026-07-12)
    // EX-DOOR-RELOAD (INV-54): the gentle cousin of the cold deal — a RELOAD keeps the door face and
    // swaps in ≤40% NEW works, so the threshold feels alive on reload yet cannot be reloaded into a
    // tour of the whole library (dealHand's ≥⅔-new is only a COLD arrival or the exit's fresh quiz).
    const standing = standingHand();
    if (!standing) return dealHand();                  // no stored hand → a normal deal
    const n = standing.length;
    const swapN = Math.floor(n * 0.4);                 // ≤40% turns over; the rest is held
    if (swapN < 1 || doorPool.length <= n) return standing;   // too small / no room → hold it whole
    const idx = shuffle(standing.map((_, i) => i)).slice(0, swapN);
    const drop = new Set(idx);
    const kept = standing.filter((_, i) => !drop.has(i));
    const held = new Set(standing.map((e) => e.id));    // never re-add a work already in the hand
    const fresh = shuffle(doorPool.filter((e) => !held.has(e.id)));
    const hand = shuffle(kept.concat(fresh.slice(0, swapN)));
    const rec = { v: VER, ids: hand.map((e) => e.id) };
    const cc = consumedCircle();                        // a reload keeps the consumed-circle memory
    if (cc) rec.circle = cc;                            // (EX-DOOR-4: one circle, one deal survives reloads)
    try { localStorage.setItem(HAND_KEY, JSON.stringify(rec)); } catch (e) {}
    return hand;
  }

  // ---- EX-DOOR-4 (INV-71): the full circle retires the hand -------------------
  // A walk is "circled" when every work of its current hang — order.slice(0, shown), the spread
  // plus every unfold taken — has stood in view (walkSeen, the in-session marks, joined with the
  // persisted seen copy so a reload still knows; F3: counted the moment marks are made). The NEXT
  // door render over a circled, not-yet-answered walk deals a fresh EX-DOOR-3 hand — the exit
  // control, the browser's own Back, and a returned-door reload behave alike (F1/F2 folded 11:50);
  // on this one point the history's "as it stood" (INV-32a) yields, the fresh hand standing as THE
  // standing hand from that moment on. One circle, one deal: the fresh hand remembers the circle
  // (pick + shown) it answered, so walking door↔walk over the same circle never re-rolls. A hand
  // with no circle field (an older client) reads as "no circle consumed" (F4).
  function consumedCircle() {
    try {
      const h = JSON.parse(localStorage.getItem(HAND_KEY) || "null");
      if (h && h.v === VER && h.circle && h.circle.pick != null) return h.circle;
    } catch (e) {}
    return null;
  }
  function walkCircled() {
    if (pick == null) return false;
    const need = order.slice(0, shown).map(String);
    if (!need.length) return false;
    const seen = new Set(walkSeen);
    try {
      const c = JSON.parse(localStorage.getItem(SEENC_KEY) || "null");
      if (c && Array.isArray(c.ids)) c.ids.forEach((id) => seen.add(String(id)));
    } catch (e) {}
    return need.every((id) => seen.has(id));
  }
  function circlePending() {              // a circle not yet answered by the standing hand
    if (!walkCircled()) return null;
    const cur = { pick: pick, shown: shown };
    const cc = consumedCircle();
    if (cc && String(cc.pick) === String(cur.pick) && cc.shown === cur.shown) return null;
    return cur;
  }
  // the hand for a door render, honouring the carve-out: a pending circle deals fresh ONCE, else
  // `fallback` (the standing set — EX-DOOR-2d — or the reload refresh) holds.
  function doorHand(fallback) {
    const pend = circlePending();
    return pend ? dealHand(pend) : fallback();
  }

  // one line, always (EX-DOOR-2b — card 01's algorithm IS the norm): a row when landscape
  // (W/H > 1.02), a column when portrait; windows shrink first, the count drops second
  // (row 5→4→3 while each keeps ≥118px; column 3→2 below 104px); never a second line
  // how many windows FIT a viewport of the given W×H (the count only, no sizing)
  function doorFit(W, H) {
    const col = W / H <= 1.02;
    if (!col) {
      const gap = Math.max(16, Math.min(44, W * 0.03));
      const cap = Math.min(190, H * 0.42);
      let n = Math.min(DOOR_SIZE, doorPool.length);
      for (; n > 3; n--) { if (Math.min(cap, (W * 0.88 - (n - 1) * gap) / n) >= 118) break; }
      return n;
    }
    const gap = Math.max(14, Math.min(30, H * 0.025));
    const cap = Math.min(190, W * 0.62);
    let n = Math.min(3, doorPool.length);
    if (Math.min(cap, (H * 0.52 - (n - 1) * gap) / n) < 104 && n > 2) n = 2;
    return n;
  }
  // the door's window count HOLDS across a rotation: it is the running MINIMUM that has fit this
  // load, so turning the phone never ADDS windows (his word 2026-07-12: «не добавлять при повороте,
  // смотрим минимальное и придерживаемся»). A wide screen that never rotates keeps its full count.
  let doorNMin = Infinity;
  function doorLayout() {
    const W = innerWidth, H = innerHeight, col = W / H <= 1.02;
    doorNMin = Math.min(doorNMin, doorFit(W, H));
    const n = Math.max(2, doorNMin);
    let gap, size;
    if (!col) {
      gap = Math.max(16, Math.min(44, W * 0.03));
      size = Math.min(Math.min(190, H * 0.42), (W * 0.88 - (n - 1) * gap) / n);
    } else {
      gap = Math.max(14, Math.min(30, H * 0.025));
      size = Math.min(Math.min(190, W * 0.62), (H * 0.52 - (n - 1) * gap) / n);
    }
    return { n, col, gap, size: Math.max(76, size) };
  }

  // ---- state + persistence (INV-26) -----------------------------------------
  let pick = null;
  let order = coldOrder();
  let shown = SPREAD;

  function save() {
    try { localStorage.setItem(KEY, JSON.stringify({ v: VER, pick, shown })); } catch (e) {}
  }
  function restore() {
    let st;
    try { st = JSON.parse(localStorage.getItem(KEY) || "null"); } catch (e) { st = null; }
    if (!st || st.v !== VER) return false;            // old-version state → clean start (the door)
    if (st.pick != null) {
      if (!byId[st.pick]) return false;               // pick gone from the gallery → clean start
      pick = st.pick; order = assembleOrder(pick);
      recomputeQuizChoice();   // INV-66: re-establish after the restored order is known
    }
    // the unfold budget DERIVES from shown, never trusted (INV-30 holds on restore)
    shown = clampInt(st.shown, SPREAD, SPREAD, Math.min(order.length, CAP));
    return true;
  }
  const spentUnfolds = () => Math.max(0, Math.floor((shown - SPREAD) / UNFOLD));

/*!06-ground-load-doorwarm.js*/
  // ---- EX-LADDER (INV-63): one home for the tier ladder -----------------------
  // The law is owed by EVERY work a visitor is shown, on every surface, so the ladder is
  // written once here and each surface hands only its own box description (`sizes`). The
  // tiers themselves are the work's baked `srcset` (640/960/1280, written by the display-cap
  // bake); no cap ⇒ no srcset key ⇒ the surface stays byte-identical to a ladder-less one.
  const LADDER_FALLBACK = { walk: "88vw", lane: "64vw", print: "(max-width:640px) 110px, 150px" };
  function ladderSizes(surface) {                      // the baked string, else the CSS box it mirrors
    return (data[surface + "_sizes"] || LADDER_FALLBACK[surface] || "100vw");
  }
  function ladderAttr(w, sizes) {                      // for a surface that writes its img as HTML
    return (w && w.srcset) ? ` srcset="${w.srcset}" sizes="${sizes}"` : "";
  }
  function ladderOn(img, w, sizes) {                   // for a surface that builds an Image object
    if (img && w && w.srcset) { img.sizes = sizes; img.srcset = w.srcset; }
    return img;
  }

  // ---- the breathing ground (room.html's tone math) --------------------------
  // EX-ACCENT rides the same pair: the focused work's tone raised to readable light
  // (Y≈170, 20% bone; near-black → bone whole) lives while the ground does, rests with it
  const BONE = [179, 162, 132];                        // #b3a284 — the resting accent
  function liveAccent(dom) {
    const [r, g, b] = dom;
    const y = 0.2126 * r + 0.7152 * g + 0.0722 * b;
    if (y < 24) return BONE;
    const k = Math.min(170 / y, 6);
    return [r, g, b].map((v, i) => Math.round(Math.min(255, v * k) * 0.8 + BONE[i] * 0.2));
  }
  function ground(dom) {
    if (!dom) return;
    const [r, g, b] = dom;
    const y = 0.2126 * r + 0.7152 * g + 0.0722 * b;
    const tone = (c) => 0.7 * (c * 0.2) + 0.3 * (y * 0.2);
    const mix = (c) => Math.round(12 + (tone(c) - 12) * 0.7);
    document.body.style.setProperty("--ground", `${mix(r)},${mix(g)},${mix(b)}`);
    const a = liveAccent(dom);
    document.documentElement.style.setProperty("--accent", `rgb(${a.join(",")})`);
    document.documentElement.style.setProperty(
      "--accent-2", `rgb(${a.map((v) => Math.round(v * 0.86)).join(",")})`);
    // --tone: the wall label's DIMMED accent — the same live tone at low brightness, lightly
    // tinting the plaque's letters work→work (EX-STORY-LINE, his call ×0.66)
    document.documentElement.style.setProperty(
      "--tone", `rgb(${a.map((v) => Math.round(v * 0.66)).join(",")})`);
  }
  const groundRest = () => {
    document.body.style.setProperty("--ground", "12,11,10");
    document.documentElement.style.removeProperty("--accent");    // back to resting bone
    document.documentElement.style.removeProperty("--accent-2");
    document.documentElement.style.removeProperty("--tone");       // the plaque rests plain, no tint
  };

  // ---- EX-LOAD-2 / EX-LOAD-3 (INV-72 / INV-73): the in-flight ladder + the one-ahead preload ----
  // Supersedes the lone-hairline FACE of the loading breath (EX-LOAD/INV-37): a frame in view whose
  // pixels are late wears the work's OWN dominant tone (a plate), and on a genuinely long wait a
  // thin wordless bar joins on the plate; the photograph fades in OVER the plate when it lands. The
  // breath's promises are re-carried whole — no frame in view stays empty, wholly wordless (INV-1),
  // retires on load-or-error, ONE reused overlay for the single in-view frame, the door/crossing
  // cover their own frames. Every wait a beat ×tempo (INV-33). The `#ex-breath` node below stays
  // for EX-ARRIVE's locked breath-entry row; the plate ladder is the shipped loader now.
  const breath = document.createElement("div");         // vestigial — kept for the EX-ARRIVE lock
  breath.id = "ex-breath";
  breath.hidden = true;
  document.body.appendChild(breath);

  // the knobs (config.exhibition, INV-28) — each a beat ×tempo (INV-33); the ordering
  // load_plate_grace < load_bar_wait is LAW (prover F7): an inverted/equal pair is CLAMPED at boot
  // (the bar wait raised past the grace) so no tuning can ask for a bar before its plate.
  const secs = (x, d) => { const n = parseFloat(x); return Number.isFinite(n) && n >= 0 ? n : d; };
  const PLATE_GRACE = secs(EX.load_plate_grace, 0.35);  // black → plate; the fast/slow reveal split
  let   BAR_WAIT    = secs(EX.load_bar_wait, 1.5);       // plate → plate+bar (a genuinely long wait)
  if (!(PLATE_GRACE < BAR_WAIT)) BAR_WAIT = PLATE_GRACE + 0.6;   // F7 clamp: a bar never before its plate
  const REVEAL_SLOW = secs(EX.load_reveal, 2.0);         // the reveal token — the graceful settle (plate stood)
  const REVEAL_FAST = secs(EX.load_reveal_fast, 0.6);    // the soft token — the crisp settle (beat the plate)
  const PRELOAD_AHEAD = clampInt(EX.preload_ahead, 1, 0, 1);     // EX-LOAD-3: one ahead, the bounded reach

  // ONE reused overlay: the plate (the work's raw tone) carrying its crawling bar, moved into the
  // in-view frame while its pixels are late (only the in-view frame ever ladders, so one suffices).
  const plate = document.createElement("div");
  plate.id = "ex-plate"; plate.hidden = true;
  plate.innerHTML = '<i class="ex-bar" aria-hidden="true"></i>';
  // the walk's loading frame: while the walk's ONE reused plate stands, the chrome (share, ambient
  // player, plaque) retracts and the counter alone stands with a quiet "loading" mark — the CSS
  // ex-loading-frame sibling of the door's ex-crossing/ex-cross-cap (his 2026-07-22 note). The door's
  // own per-window plates carry their crossing separately, so this rides ONLY the walk plate (`plate`).
  function loadFrame(on) {
    document.body.classList.toggle("ex-loading-frame", on);
    var c = document.getElementById("exh-counter");
    if (c) c.classList.toggle("loading", on);
  }
  // hide ANY plate (the walk's single reused one, or a door window's own) — shared by both call sites
  function plateHideEl(el) {
    el.hidden = true; el.classList.remove("show", "bar");
    if (el.parentNode) el.parentNode.removeChild(el);
    if (el === plate) loadFrame(false);                 // the walk plate is gone → chrome returns
  }
  function plateHide() { plateHideEl(plate); }
  let armTimers = [];
  let armedImg = null;                                  // the one in-flight image the ladder waits on
  function armClear() { armTimers.forEach(clearTimeout); armTimers.length = 0; }
  // retire the whole ladder + preload — the door/ceremony cover every walk frame (EX-LOAD boundary)
  function ladderOff() { armClear(); armedImg = null; plateHide(); preloadCancel(); }
  // the reveal: the photo fades in over the plate at the chosen settle (fast when it beat the plate,
  // the reveal token when the plate stood). Rides the one clock (×TEMPO — reduced motion collapses it).
  function reveal(img, durSec) {
    img.style.transition = "none";
    img.style.opacity = "0";
    void img.offsetWidth;
    img.style.transition = "opacity " + (durSec * TEMPO).toFixed(3) + "s var(--ease)";
    img.style.opacity = "";                             // .seen → opacity 1, fades over durSec
    img.dataset.ladder = "done";
  }
  // the in-flight CORE, shared by the walk's one reused plate AND the door's per-window plates —
  // ONE implementation of the grace/bar/reveal timings + classes (never a second copy of the knobs).
  // The caller has already read the settled state; this arms a GENUINELY in-flight image only. Black
  // held → plate (grace) → plate+bar (long wait) → reveal on load. `alive()` says whether this wait is
  // still the live one (the walk swaps the in-view frame; a door window is rebuilt on relayout/re-deal);
  // `timers` is the caller's own list (mutated in place); `mark` gates the walk's single-frame ex: marks
  // (the door stays off the walk's counter — no door marks). On load: fade over the plate at the settle
  // (fast when it beat the plate, the reveal token when the plate stood), then retire the plate.
  function ladderFlight(img, w, host, plateEl, timers, alive, mark) {
    host.insertBefore(plateEl, host.firstChild);        // behind the photo, same cell
    plateEl.style.aspectRatio = (w.w && w.h) ? (w.w + " / " + w.h) : "";
    // the work's shape as a NUMBER too: a surface whose plate has no box of its own (the walk's
    // centered frame, the room's lane) reads --ar to turn its own caps into this picture's box —
    // aspect-ratio alone has nothing to be an aspect OF when both sides resolve to auto. Set for
    // every plate, one place; a plate that already has a box (a door window's inset:0) ignores it.
    if (w.w && w.h) plateEl.style.setProperty("--ar", w.w / w.h);
    plateEl.style.background = "rgb(" + w.dom.join(",") + ")";   // the work's RAW baked tone (not liveAccent)
    plateEl.hidden = false;
    void plateEl.offsetWidth;                           // a fresh fade from opacity 0
    img.style.transition = "none";
    img.style.opacity = "0";                            // hold the photo behind the plate until it lands
    let plateShown = false;
    timers.push(setTimeout(() => {                      // the grace beat → the plate fades in (soft token)
      if (!alive() || img.complete) return;
      plateShown = true;
      plateEl.classList.add("show");
      if (mark) { loadFrame(true); tlog("plate"); }     // the walk plate stands → chrome retracts (EX-LOAD-FRAME)
    }, Math.round(PLATE_GRACE * 1000 * TEMPO)));
    timers.push(setTimeout(() => {                      // the long wait → the wordless bar joins the plate
      if (!alive() || img.complete) return;             // (past here a silent stall crawls indefinitely —
      plateEl.classList.add("show", "bar");             //  the ladder owns no timeout, the browser's fetch does)
      if (mark) tlog("bar");
    }, Math.round(BAR_WAIT * 1000 * TEMPO)));
    const done = () => {                                // load OR error, whichever speaks first
      if (!alive()) return;
      timers.forEach(clearTimeout); timers.length = 0;
      if (img.naturalWidth > 0) {                       // pixels home: fade over the plate then retire it
        const dur = plateShown ? REVEAL_SLOW : REVEAL_FAST;
        reveal(img, dur);
        timers.push(setTimeout(() => { if (alive()) plateHideEl(plateEl); },
                               Math.round(dur * 1000 * TEMPO) + 60));
      } else {                                          // a dead image never traps (INV-37): retire whole,
        img.dataset.ladder = "done"; plateHideEl(plateEl);  //   caption + counter hold, no plate as the picture
      }
    };
    img.addEventListener("load", done, { once: true });
    img.addEventListener("error", done, { once: true });
  }

  // arm the ladder on a frame taking view. The arm READS THE SETTLED STATE FIRST (prover F1):
  // a warm image (complete, real pixels) reveals at once down the fast path — no plate, no clock;
  // an already-errored one retires at once, caption + counter holding; only a genuinely in-flight
  // image arms the grace/bar clocks and the load/error listeners — never a wait on a spent event.
  // Arms ONCE per frame-taking-view (prover F6): a post-reveal tier swap (INV-63) never re-plates.
  function arm(img, w, frame) {
    if (!img || !w || !frame) return;
    if (img.dataset.ladder === "done") return;          // already resolved — never re-plate (F6)
    if (img === armedImg && !plate.hidden) return;      // already laddering THIS frame — don't restart
                                                        //   the clocks (resize/re-observe)
    if (img.complete) {                                 // the settled read (F1), synchronous
      plateHide();                                      // clear a plate lingering from a prior frame
      if (img.naturalWidth > 0) reveal(img, REVEAL_FAST);   // warm ⇒ reveal at once, no plate/clock
      else img.dataset.ladder = "done";                     // pre-errored ⇒ retire; the caption holds
      return;
    }
    // genuinely in flight: black held → plate (grace) → plate+bar (long wait) → reveal on load
    armClear();
    armedImg = img;
    plateHide();
    ladderFlight(img, w, frame, plate, armTimers, () => img === armedImg, true);
  }

  // EX-LOAD-3: the next work quietly preloads — the walk arrives warm. While a work rests in view,
  // fetch the NEXT work in the current DIRECTION OF TRAVEL at the device tier (the same srcset/sizes
  // the walk uses, INV-63) — exactly preload_ahead (1) ahead, never the arc (INV-25/30). Best-effort
  // and silent (a dead preload costs nothing); cancelled on a turn or a #w- jump (prover F5), then
  // re-aimed to the new direction of travel.
  let travelDir = 1;                                    // +1 forward · -1 back — set by every step
  let preImg = null, preId = null;
  function preloadCancel() {
    if (preImg) { preImg.src = ""; preImg = null; }     // abandon the in-flight fetch cleanly (F5)
    preId = null;
    try { window.__@@NS@@Preload = null; } catch (e) {}     // the test read-side, like @@NS_UPPER@@Timings/__@@NS@@Seen
  }
  function preloadAhead(curN) {                         // curN = the 1-based frame in view
    if (!PRELOAD_AHEAD) { preloadCancel(); return; }
    if (dataSaver()) { preloadCancel(); return; }       // the Save-Data class law binds the one-ahead (EX-LOAD-3)
    const idx = (curN - 1) + travelDir;                 // one ahead along the feet
    if (idx < 0 || idx >= order.length) { preloadCancel(); return; }
    const id = String(order[idx]);
    if (id === preId) return;                           // already warming this exact next work
    preloadCancel();                                    // a turn/jump abandons the old one cleanly (F5)
    const w = byId[id]; if (!w) return;
    preId = id;
    const im = new Image();
    ladderOn(im, w, ladderSizes("walk"));
    im.src = w.img;                                     // the browser picks the device tier
    preImg = im;
    try { window.__@@NS@@Preload = { id: id, dir: travelDir }; } catch (e) {}
  }

  // ---- EX-DOOR-WARM (INV-25): the door warms its candidates — a pick opens warm ----
  // After the threshold's five windows decode AND the door rests, quietly warm ONE room-tier picture
  // per candidate (≤5) at LOW priority — the EXACT URL the room's first hang will request (the walk's
  // own full-frame `srcset`/`sizes`, INV-63), so the room's <img> finds the file already in cache.
  // Never before the door's own windows (fired only after they decode), never under Save-Data (the
  // class law's one home, dataSaver). Also the crossing's own pick-time warm (EX-DOOR-2e): the same
  // one picture for the picked work, so a fast picker who beats the rest still opens warm.
  const DOOR_WARM_SETTLE = 1000;                        // ms the threshold rests before warming (a network settle, unscaled)
  let warmGen = 0;                                      // a re-deal / relayout rebuild / pick cancels a pending warm
  let warmSettleT = null;
  const warmed = new Set();
  function warmRoomPicture(w) {
    if (!w || dataSaver()) return;                      // the Save-Data class law, consulted here too (EX-LOAD-3)
    if (warmed.has(w.id)) return;                       // one picture per candidate, once
    warmed.add(w.id);
    const im = new Image();
    try { im.fetchPriority = "low"; } catch (e) {}      // never contends with the door's five windows
    ladderOn(im, w, ladderSizes("walk"));               // the room's own tier
    im.src = w.img;                                     // the browser resolves the exact room-hang URL (INV-63)
  }
  function warmCandidates(gen) {
    if (gen !== warmGen || !atDoor || entered || busy || dataSaver()) return;
    const spread = (doorFace && doorFace.spread) ? doorFace.spread.slice(0, curLay.n) : [];
    spread.forEach((e) => warmRoomPicture(byId[e.id]));
  }
  // Track the threshold's decode: which layer each window belongs to is read ONCE at build — the
  // STATIC layer is the windows whose pixels are already present (a cache hit, no fetch, the seam the
  // door's own ladder reads via img.complete, EX-DOOR-2c); the DYNAMIC layer is the windows that must
  // fetch. Their decode promises close the load ladder's last two rungs, lay door_ready (arm 1), and
  // — after the rest — fire the candidate warm.
  function doorWatch(facade) {
    const imgs = [...facade.querySelectorAll(".exd-window img")];
    if (!imgs.length) return;
    const gen = ++warmGen;                              // this watch supersedes any pending warm
    clearTimeout(warmSettleT); warmSettleT = null;
    const decodeP = (img) => {
      if (img.complete && img.naturalWidth > 0) return Promise.resolve();
      if (img.decode) return img.decode().catch(() => {});
      return new Promise((res) => {
        img.addEventListener("load", res, { once: true });
        img.addEventListener("error", res, { once: true });
      });
    };
    const staticImgs = imgs.filter((i) => i.complete && i.naturalWidth > 0);
    Promise.all(staticImgs.map(decodeP)).then(() => { if (gen === warmGen) markStage("static"); });
    Promise.all(imgs.map(decodeP)).then(() => {
      if (gen !== warmGen) return;                      // a rebuild superseded this watch
      markStage("static");                              // dynamic implies the static rung was passed (monotonic)
      markStage("dynamic");
      layDoorReady();                                   // arm 1: the door's five windows decoded
      warmSettleT = setTimeout(() => warmCandidates(gen), DOOR_WARM_SETTLE);
    });
  }

/*!07-door-face-ceremony.js*/
  // ---- THE DOOR (door.html's face — the norm) --------------------------------
  const door = document.createElement("div");
  door.id = "ex-door";
  door.hidden = true;                                  // born hidden — a restored walk must never
                                                       // wake under a dark cover (2026-07-06 bug)
  door.innerHTML =
    '<div class="exd-wm"></div>' +                    // brand from config.site_name (INV-28)
    '<div class="exd-greet" id="exd-greet" hidden></div>' +
    '<div class="exd-ask">' + ASK_EN + '</div>' +   // real markup overwritten by renderDoor() before paint
    '<div class="exd-more" id="exd-more" hidden></div>' +   // EX-RETURN: "there is more" — a farewell at the exit, a welcome-back on a return
    '<div class="exd-facade" id="exd-facade"></div>';  // no silent entry — the pick IS the
  door.querySelector(".exd-wm").textContent = cfg.site_name || "";
  document.body.appendChild(door);                     // entry (EX-DOOR-2a, his design word)
  const veil = document.createElement("div");          // the ceremony's black (EX-DOOR-2e)
  veil.id = "ex-veil";
  veil.hidden = true;
  document.body.appendChild(veil);

  let atDoor = false;
  // EX-GREET-LIVE (INV-55): the door greeting tracks the LIVE daypart — an open door left from the
  // evening into the morning re-greets itself, no reload needed (his word). A reload already re-greets
  // (renderDoor recomputes at the current hour); this catches the tab that just STAYS open or is
  // returned to. Registered once below; harmless when the door isn't showing.
  let shownPart = null;
  function dayPart() {
    const h = new Date().getHours();
    return h < 6 ? "night" : h < 12 ? "morning" : h < 18 ? "day" : "evening";
  }
  function regreet() {
    if (!atDoor) return;
    const p = dayPart();
    if (p === shownPart) return;                        // same part → leave the chosen line be
    shownPart = p;
    const L = greetLang(), g = door.querySelector("#exd-greet");
    if (L && g && !g.hidden) g.textContent = greetLine(L.t);   // a fresh line for the new hour
  }
  // EX-RETURN/INV-94: a tab idle past the return window's lower bound wakes AT THE DOOR, not wherever
  // it stood — the ordinary arrival then reads the same last-visit clock through INV-78's own machinery.
  // lastAwake stamps every moment this tab stood visible; a wake's gap against it decides reload vs.
  // an ordinary re-greet. Runs BEFORE the daypart re-greet below; a fresh load re-initializes the
  // stamp, so a reload never loops back into itself.
  let lastAwake = Date.now();
  function wakeGate() {
    const gap = Date.now() - lastAwake;
    if (gap < RETURN_MIN_MS) { lastAwake = Date.now(); regreet(); return; }
    if (navigator.onLine === false) return;   // offline: the gap stays STANDING, untouched — the
    // spec's own word ("tries again at the next wake"): erasing it here would silently forgive the
    // idle time, so the very next online wake must still see the full, real gap and fire at once.
    try {
      // the reset's own non-goal: the walk's POSITION never rides across it (a plain reload alone
      // would resume it — INV-54 holds the face across an ordinary refresh on purpose). Two holes a
      // fresh audit found in that plain reload: (1) a first-session walker who never exited carries
      // no BEEN_KEY, so a cold door after the reset could show no welcome-back line for them — stamp
      // it here, the same flag an ordinary exit already sets; (2) history.state.returned rides an
      // ordinary reload too (INV-54's own law), so a tab asleep on a HELD door woke right back into
      // the silent held-door branch — history.replaceState(null,"") clears it, forcing a true cold
      // arrival. The visitor's own separate memory (EX-MEMORY: seen list, language, sound) is
      // untouched by any of this.
      if (localStorage.getItem(KEY)) localStorage.setItem(BEEN_KEY, "1");
      localStorage.removeItem(KEY);
      sessionStorage.removeItem(PLACE_KEY);
      history.replaceState(null, "");
    } catch (e) {}
    location.reload();
  }
  function onVisibility() {
    if (document.hidden) { lastAwake = Date.now(); return; }   // stamp the moment the tab hides
    wakeGate();
  }
  document.addEventListener("visibilitychange", onVisibility);   // returned to the tab (fired on document)
  addEventListener("pageshow", (e) => { if (e.persisted) wakeGate(); });   // the bfcache return
  addEventListener("focus", regreet);                   // some browsers wake a tab with focus, not visibility
  // the minute backstop is itself a WAKE DETECTOR, not just a stamp: after a real system sleep (or a
  // lid-close that fires no visibilitychange at all) an overdue tick runs the full gate, so the reset
  // still fires on its own; wakeGate's own below-bound path already stamps + regreets, so an ordinary
  // visible tab ticking along sees no change at all.
  setInterval(() => { if (!document.hidden) wakeGate(); }, 60000);
  let entered = false;                                 // a walk exists behind the door
  let doorFace = null;                                 // the spread the standing door renders
  let curLay = { n: 0, col: null };

  // EX-RETURN/INV-78: count a real walk→door leave (the exit control AND a history Back from the walk,
  // the same two moments that pulse walk_exit) so the farewell can wait for the second exit. A door
  // reload or a Back that only restores a door never passes here, so it never inflates the count.
  function noteExit() {
    let n = 0;
    try { n = parseInt(localStorage.getItem(EXITS_KEY), 10) || 0; } catch (e) {}
    try { localStorage.setItem(EXITS_KEY, String(n + 1)); } catch (e) {}
  }

  // cold=true only on the COLD-arrival face: a museum greets on arrival, not on every
  // pass through the lobby (EX-GREET) — the re-opened door keeps the localized ask only
  function renderDoor(spread, cold) {    // the spread is CARRIED by the caller (INV-32a)
    ceremonyCancel();                                  // a door render wins over any crossing
    ladderOff();                                       // the door covers every frame (EX-LOAD-2/-3)
    atDoor = true;
    faceSync();                                        // the door is a face — arm the rest + guard (EX-CHROME)
    tlog("door");
    markStage("door");                                 // EX-TIME-READ: the door drawn — the ladder's 3rd rung
    document.body.classList.add("ex-door");
    door.classList.remove("leaving");
    door.hidden = false;
    doorFace = { spread: spread || doorSet() };
    curLay = { n: 0, col: null };
    const L = greetLang();
    door.setAttribute("dir", L && L.t.dir === "rtl" ? "rtl" : "ltr");
    if (L) door.setAttribute("lang", L.code);
    else door.removeAttribute("lang");
    door.querySelector(".exd-ask").textContent = L ? L.t.ask : ASK_EN;
    const g = door.querySelector("#exd-greet");
    const line = (cold && GPLACE !== "off" && L) ? greetLine(L.t) : "";
    g.textContent = line;
    g.hidden = !line;                    // ambient: Back to a cold step re-greets at the CURRENT hour
    shownPart = line ? dayPart() : null; // the daypart on show — the live re-greet compares against it
    // EX-RETURN (INV-78): the door says there is more, but BOUNDED IN TIME so it never over-speaks.
    // A door REACHED BY LEAVING a walk (cold=false) is proof this browser has walked, so we remember it;
    // the FAREWELL then stays silent on the first exit and speaks only from the second exit onward
    // (noteExit counts the real walk→door leaves). A later COLD arrival from a browser that has walked
    // before is WELCOMED BACK, but only after a real gap and within a window: a return sooner than
    // RETURN_MIN_MS is a quick reload (silent), a return later than RETURN_MAX_MS is met as new (silent),
    // and the gap read is returnGapMs — the last-visit clock captured at load (one clock, INV-79 reused).
    // Localized, English falls back; the line rides below the ask, the daypart greeting kept (EX-GREET).
    const more = door.querySelector("#exd-more");
    let moreLine = "";
    let been = null;
    try { been = localStorage.getItem(BEEN_KEY); } catch (e) {}
    if (!cold) {
      try { localStorage.setItem(BEEN_KEY, "1"); } catch (e) {}
      let exits = 0;
      try { exits = parseInt(localStorage.getItem(EXITS_KEY), 10) || 0; } catch (e) {}
      if (exits >= FAREWELL_MIN_EXITS) moreLine = (L && L.t.more_exit) || MORE_EXIT_EN;   // silent on the 1st exit
    } else if (been && returnGapMs != null && returnGapMs >= RETURN_MIN_MS && returnGapMs <= RETURN_MAX_MS) {
      moreLine = (L && L.t.more_return) || MORE_RETURN_EN;   // a quiet extra line below the ask; the daypart greeting stays (EX-GREET)
    }
    more.textContent = moreLine;
    more.hidden = !moreLine;
    door.classList.toggle("greet-top", GPLACE === "top");
    doorRender(true);                                  // a fresh open breathes its windows in
    if (cold) hintArm(); else hintOff(); // the re-opened door never hints (EX-DOOR-2g)
  }

  // EX-DOOR-2c / DL1-DL2: the door's OWN ladder arm — one per window (five may fly at once), reusing
  // the walk's knobs, reveal, classes and in-flight core (never a second copy). Each window owns its
  // own `.exd-plate` behind its photo. Reads the SETTLED STATE FIRST the way the walk's arm does (the
  // crux / prover seam 5): a window whose image is already cached reveals at once with NO plate, so a
  // relayout re-render or a fresh full-circle deal re-flashes no plate — only a still-in-flight window
  // plates. No ex: marks — the door stays off the walk's loading counter.
  function doorArm(img, w, win) {
    if (!img || !w || !win) return;
    if (img.complete) { img.dataset.ladder = "done"; return; }   // cached ⇒ shows at once, no plate
    const p = document.createElement("div");                     // a plate PER window (not the walk's single one)
    p.className = "exd-plate";
    p.innerHTML = '<i class="ex-bar" aria-hidden="true"></i>';
    ladderFlight(img, w, win, p, [], () => win.isConnected, false);
  }

  // layout-aware render — re-runs on resize; rebuilds only when count/orientation change.
  // `animate` is true only on a fresh open; a resize relayout (aspect change) rebuilds WITHOUT the
  // entry fade — the windows are already on screen, so re-running exd-rise reads as a wrong fade-in.
  function doorRender(animate) {
    if (!atDoor || !doorFace) return;
    const c = doorLayout();
    const facade = door.querySelector("#exd-facade");
    facade.classList.toggle("col", c.col);
    facade.style.setProperty("--exd-gap", c.gap.toFixed(1) + "px");
    facade.style.setProperty("--exd-wsize", c.size.toFixed(1) + "px");
    // A RELAYOUT (a resize / a phone rotation, `animate` false) with the SAME window count flows the
    // new arrangement through CSS — the direction flips, the sizes transition — WITHOUT tearing the
    // windows down. Rebuilding here emptied the facade for a frame, and a fast rotation made that
    // empty (black) facade visible (a phone find 2026-07-12). The count holds across rotation
    // (doorLayout's running minimum), so this is the common path; only a genuine count change or a
    // fresh open (animate) rebuilds the DOM.
    if (c.n === curLay.n && !animate) { curLay = c; return; }
    curLay = c;
    facade.innerHTML = "";
    doorFace.spread.slice(0, c.n).forEach((e, i) => {
      const w = byId[e.id];
      const alt = (e.alt || "").replace(/"/g, "&quot;");
      const b = document.createElement("button");
      b.type = "button"; b.className = "exd-window";
      b.dataset.id = w.id;
      b.setAttribute("aria-label", e.alt || w.title || "");
      // N7-A11Y (INV-102, B2/B3): a window announces `z` ONLY. It answers `g` with the gracious line
      // rather than the ceremony (it carries no hung-work identity, INV-49/F1), so announcing `g`
      // here would promise a gift the door never gives.
      b.setAttribute("aria-keyshortcuts", "z");
      // the halo speaks liveAccent, never the raw dominant — a near-black dominant is
      // invisible on the dark ground (card 01's note, EX-DOOR-2c)
      const a = liveAccent(w.dom);
      b.style.setProperty("--glow", `rgb(${a.join(",")})`);
      if (animate) {
        b.style.animationDelay = ((0.55 + i * 0.2) * TEMPO).toFixed(2) + "s";
      } else {                                         // relayout: already on screen, no re-fade
        b.style.animation = "none"; b.style.opacity = "1";
      }
      // EX-LADDER (INV-63): a window's box is the layout's own size (--exd-wsize), so it hands
      // that exact width and a phone pulls the small tier instead of the full display file.
      b.innerHTML = `<img src="${w.img}"${ladderAttr(w, c.size.toFixed(0) + "px")} alt="${alt}">`;
      doorArm(b.querySelector("img"), w, b);             // DL1/DL2: the window's own plate + halo
      // EX-QUIZ (INV-64/66): the quiz chip NEVER appears on the door (button-only screen) —
      // only over a work in view on the plaque (quizShows checked in the IO observer below).
      b.addEventListener("click", () => doorPick(w, b));   // the window itself rides along (EX-STORY-BEAT: its picture is the beat's star)
      facade.appendChild(b);
    });
    doorWatch(facade);   // EX-TIME-READ + EX-DOOR-WARM: watch the windows decode → door_ready + the candidate warm
  }
  let rsz;
  function doorReflow() { clearTimeout(rsz); rsz = setTimeout(doorRender, 150); }
  addEventListener("resize", doorReflow);
  // a rotation is its OWN beat on iOS (INV-86); its settled dimensions arrive on the visualViewport
  // "resize", so the door facade re-lays-out true after a phone turn rather than on stale metrics.
  addEventListener("orientationchange", doorReflow);
  if (window.visualViewport) visualViewport.addEventListener("resize", doorReflow);

  // ---- the idle hint (EX-DOOR-2g): a cold untouched door breathes its first halo ----
  // Behavior, never a word; ANY interaction retires it; the re-opened door never hints.
  let hintT = null;
  let hintPulseT = null;
  function hintOff() {
    clearTimeout(hintT); hintT = null;
    clearTimeout(hintPulseT); hintPulseT = null;
    const w = door.querySelector(".exd-window.hint");
    if (w) w.classList.remove("hint");
  }
  function hintPulse() {
    if (!atDoor || REDUCED) return;
    const w = door.querySelector(".exd-window");
    if (!w) return;
    w.classList.remove("hint");
    void w.offsetWidth;                                // restart the one-cycle breath
    w.classList.add("hint");
    hintPulseT = setTimeout(hintPulse, Math.round(7000 * TEMPO));
  }
  function hintArm() {
    hintOff();
    if (REDUCED) return;                               // stillness wins (EX-MOTION-R)
    hintT = setTimeout(hintPulse, Math.round(3000 * TEMPO));
  }
  ["pointerover", "touchstart", "keydown", "mousedown"].forEach((e) =>
    door.addEventListener(e, hintOff, { passive: true }));

  // ---- ceremony B «через чёрное» (EX-DOOR-2e; cards 01 + 05 are the norm) ----
  // from the general to the particular: the veil takes the door → the wordmark alone drifts
  // to the black's center and lets go → the room's TONE rises first → the first work reveals
  // separately → the caption last. Every beat ×tempo; ONE history step; any navigation cancels.
  let busy = false;                                    // the lock spans the WHOLE ceremony
  let cerGen = 0;
  const cerTimers = [];
  function cerAfter(s, fn) { cerTimers.push(setTimeout(fn, Math.round(s * 1000 * TEMPO))); }
  function ceremonyCancel() {                          // the arriving face wins, no stranded veil
    cerGen += 1;
    while (cerTimers.length) clearTimeout(cerTimers.pop());
    veil.hidden = true; veil.classList.remove("on");
    beatKill();                                        // …and no stranded centred picture (EX-STORY-BEAT)
    door.classList.remove("wm-out");
    document.body.classList.remove("ex-crossing", "ex-cross-cap");
    busy = false;
    faceSync();                                        // the ceremony released (EX-CHROME)
  }

  // ---- EX-STORY-BEAT (INV-89): the crossing is the voice's head start ----
  // The picked picture flies from its window to the black's centre and BREATHES there while the
  // story's first portion travels — the photograph is the star of the loading beat, never a blank
  // veil. The clone rides above the veil, flies and pulses on the house tempo, and at the landing
  // hands off into the first work's own reveal — one continuous motion, no second reveal. Torn
  // down by ceremonyCancel like every ceremony prop; reduced motion never builds it.
  const BEAT_HOLD = 2.5;      // s×tempo the crossing may stretch past its plain reveal while the
                              // first portion is still in flight ([default], his tune)
  const BEAT_GRACE = 0.45;    // s×tempo after the wordmark beat that a near-instant open is given to
                              // settle BOTH sides before any pulse builds — a fast open skips it
                              // outright (no third copy of the picture); [default], his tune (INV-89)
  let beatEl = null, beatRect = null, beatSrc = "";
  function beatKill() {
    if (beatEl) { try { beatEl.remove(); } catch (e) {} beatEl = null; }
  }
  function beatFly() {
    if (REDUCED || beatEl || !beatRect || !beatRect.width || !beatSrc) return;
    const r = beatRect;
    const el = document.createElement("div");
    el.className = "exd-beat";
    el.style.left = r.left + "px"; el.style.top = r.top + "px";
    el.style.width = r.width + "px"; el.style.height = r.height + "px";
    const im = document.createElement("img");
    im.src = beatSrc; im.alt = "";
    el.appendChild(im);
    document.body.appendChild(el);
    const k = Math.min(innerWidth * 0.38 / r.width, innerHeight * 0.38 / r.height);
    const dx = innerWidth / 2 - (r.left + r.width / 2);
    const dy = innerHeight / 2 - (r.top + r.height / 2);
    requestAnimationFrame(() => {
      el.style.transform = "translate(" + dx.toFixed(1) + "px," + dy.toFixed(1) + "px) scale(" + k.toFixed(4) + ")";
      el.classList.add("breathe");                     // the slow pulse rides the inner img (CSS)
    });
    beatEl = el;
  }
  function beatLand() {                                // hand off into the first work's own reveal
    if (!beatEl) return;
    const el = beatEl; beatEl = null;
    el.classList.remove("breathe");
    const img = stage.querySelector(".exh-frame img.work");
    const r = img && img.getBoundingClientRect();
    if (r && r.width && beatRect && beatRect.width) {
      const dx = (r.left + r.width / 2) - (beatRect.left + beatRect.width / 2);
      const dy = (r.top + r.height / 2) - (beatRect.top + beatRect.height / 2);
      el.style.transform = "translate(" + dx.toFixed(1) + "px," + dy.toFixed(1) + "px) scale(" + (r.width / beatRect.width).toFixed(4) + ")";
    }
    el.style.opacity = "0";                            // …and yields as the work breathes in
    setTimeout(() => { try { el.remove(); } catch (e) {} }, Math.round(900 * TEMPO) + 60);
  }

  // the beats below are ONE THIRD of the card's old clock (EX-DOOR-2e re-ruled, his word
  // 2026-07-06 evening) — only the WAITS shortened; the reveal fade keeps its full span
  function doorPick(w, win) {
    if (busy) return;
    interrupt("door");                                  // EX-PASS §10.3: the door ceremony stands in
                                                         // front of the walk — end any transaction first
    busy = true;
    faceSync();                                        // the ceremony holds the lock (EX-CHROME)
    tlog("pick");
    pulse("door_pick", w.id);
    // EX-TIME-READ: the pick-crossing is a door_ready lay arm (this arrival's load reached the pick,
    // however far the door got) — laid ONCE, distinct from door_pick (they mark different things).
    warmGen += 1; clearTimeout(warmSettleT);           // a pick cancels any pending candidate warm
    layDoorReady();
    // EX-DOOR-2e: the crossing's own pick-time warm — the picked work's room-tier picture, so a fast
    // picker who beat the candidate warm still opens onto a warm first frame (Save-Data-gated).
    warmRoomPicture(w);
    const g = ++cerGen;
    const ok = () => g === cerGen;
    pick = w.id;
    order = assembleOrder(pick);
    recomputeQuizChoice();   // INV-66: the new arc = the new eligible set for the one quiz chip
    shown = SPREAD;                                    // a fresh arc = a fresh budget (INV-30/31)
    storyReset();                                      // …and a fresh story — no portion leaks across picks (EX-STORY)
    // EX-STORY-BEAT (INV-89): the pick itself asks the picked arc's first portion — the model's
    // head start is the whole crossing, and ONLY the picked arc is ever asked (an unpicked window
    // costs nothing). The reveal below waits on this settle or the hold cap, never longer.
    // EX-STORY-BEAT (INV-89): a UNIFIED cold-test — the beat holds while EITHER side still travels,
    // and is done only when BOTH settle. The story side (voice on) and the picture side (the picked
    // work's own room-tier decode) each carry their own flag; voice off ⇒ the story side is already
    // done, so the picture's decode alone carries the test.
    let storyDone = true, picDone = true, beatWake = null;
    const beatDone = () => storyDone && picDone;
    const beatWakeMaybe = () => { if (beatWake && beatDone()) beatWake(); };
    if (STORY_ON) {
      const parts = storyPortions(Math.min(shown, order.length));
      if (parts.length) {
        storyDone = false;
        askPortion(parts[0][0], parts[0][1], () => { storyDone = true; beatWakeMaybe(); });
      }
    }
    // The picture side (INV-89 + INV-25): the picked work's room-tier decode. A warm room whose frame
    // has already decoded settles this side at once (opens plateless). Awaited only OFF Save-Data /
    // reduced motion — the class law forbids an early room-tier fetch under Save-Data (EX-LOAD-3), so
    // there the picture side never blocks and never fetches early.
    if (!REDUCED && !dataSaver()) {
      const rim = new Image();
      if (w.srcset) { rim.sizes = data.walk_sizes || "88vw"; rim.srcset = w.srcset; }
      rim.src = w.img;
      picDone = false;
      const wake = () => { if (!ok()) return; picDone = true; beatWakeMaybe(); };
      if (rim.decode) rim.decode().then(wake, wake);
      else if (rim.complete) wake();
      else { rim.onload = wake; rim.onerror = wake; }
    }
    beatKill();
    const bimg = win && win.querySelector ? win.querySelector("img") : null;
    beatRect = bimg ? bimg.getBoundingClientRect() : null;
    beatSrc = bimg ? (bimg.currentSrc || bimg.src || "") : "";
    veil.hidden = false;
    veil.style.transitionDuration = (0.33 * TEMPO) + "s";
    door.classList.add("leaving");                     // the wordmark drifts to the center
    requestAnimationFrame(() => veil.classList.add("on"));
    cerAfter(0.92, () => { if (!ok()) return;          // the name lets go
      door.classList.add("wm-out");
      // INV-89: a near-instant open is given a grace to settle BOTH sides before any pulse builds —
      // if still travelling AFTER the grace, the picked picture takes the black's centre; if both
      // settle within it, no pulse ever (the fast open goes straight to the reveal, no third copy).
      if (!beatDone()) cerAfter(BEAT_GRACE, () => { if (!ok()) return; if (!beatDone()) beatFly(); });
    });
    cerAfter(1.18, () => { if (!ok()) return;          // faces swap under the black
      document.body.classList.add("ex-crossing");      // works + details held back
      closeDoor(); door.classList.remove("wm-out");
      ground(w.dom);
      renderHang(); save();
      pushFace({ face: "walk" });                      // ONE step, laid as the walk arrives (INV-32a)
      veil.style.transitionDuration = (0.53 * TEMPO) + "s";
      veil.classList.remove("on");                     // …the tone rises first
    });
    let landed = false;
    const land = () => { if (!ok() || landed) return;  // …then the first work, separately
      landed = true;
      beatLand();                                      // the centred picture hands off into the reveal
      tlog("reveal");
      const first = stage.querySelector(".exh-frame img.work");
      if (first) first.style.transitionDuration = (1.5 * TEMPO) + "s";
      document.body.classList.remove("ex-crossing");
      document.body.classList.add("ex-cross-cap");     // the caption still waits its beat
      cerAfter(0.15, capBeat);                         // the caption keeps its own +.15 offset
    };
    cerAfter(1.78, () => { if (!ok()) return;
      // EX-STORY-BEAT: reveal at once when the portion has settled (served OR failed — a dead
      // voice never holds the guest) or under reduced motion; else the pulse holds until the
      // settle or the hold cap, whichever lands first (fails open, INV-89)
      if (beatDone() || REDUCED) { land(); return; }
      beatWake = land;
      cerAfter(BEAT_HOLD, land);
    });
    const capBeat = () => { if (!ok()) return;         // the caption, last (+.15)
      tlog("caption");
      document.body.classList.remove("ex-cross-cap");
      const first = stage.querySelector(".exh-frame img.work");
      if (first) first.style.transitionDuration = "";
      veil.hidden = true;
      busy = false;
      faceSync();                                      // the walk is bare — the lock lifts (EX-CHROME)
      // INV-32c: the hand-over writes the place itself, so the walk's memory agrees with the eye
      // from its first breath — the same write the #w- hand-over makes at its own jump. The
      // watcher holds its report for the length of a stand, and the whole ceremony is one; the
      // picked work is where the visitor stands the moment the walk is bare, before they have
      // moved a frame.
      try { sessionStorage.setItem(PLACE_KEY, JSON.stringify({ v: VER, id: pick })); } catch (e) {}
      // the crossing warms its own picked work, so the room opens without a plate; but a
      // cache-evicted or slow-landing first image falls through to THIS ladder now the lock has
      // lifted (EX-DOOR-2e → EX-LOAD-2). And the feet warm forward from the threshold (EX-LOAD-3).
      travelDir = 1;
      const f0 = stage.querySelector(".exh-frame");
      const im0 = f0 && f0.querySelector("img.work");
      if (im0 && !im0.complete) arm(im0, byId[f0.dataset.id], f0);
      preloadCancel();
      preloadAhead(1);
    };
  }

  function closeDoor() {
    hintOff();
    atDoor = false;
    entered = true;
    door.hidden = true;
    document.body.classList.remove("ex-door");
    faceSync();                                        // the door left (EX-CHROME)
  }

  let walkY = 0;                                       // the walk's place while a door covers it
  function doorReturn() {                              // the gallery's quiet exit (INV-31)
    if (busy || !doorAvailable) return;
    interrupt("door");                                  // EX-PASS §10.3: leaving to the door also
                                                         // stands in front of the walk
    tlog("exit");
    pulse("walk_exit");
    noteExit();                                        // EX-RETURN/INV-78: this real leave counts toward the 2nd-exit farewell
    // the paginated walk always rests ON a frame (EX-GLIDE, INV-39) — remember its MEASURED
    // centered stop so Back restores a whole work centered, never a stray sub-frame offset
    // (INV-32b); measured, because on a phone innerHeight ≠ the frames' 100vh.
    { const stops = frameStops();
      walkY = stops.length ? stops[nearestStop(stops, scrollY)] : 0; }
    groundRest();
    const sp = doorHand(doorSet);                      // the SAME curated set (EX-DOOR-2d), unless a
    renderDoor(sp, false);                             // full circle earns a fresh deal (EX-DOOR-4)
    // `returned:true` marks a door reached BY EXITING a walk (vs a cold arrival) — a reload of THIS
    // door holds it (INV-54), while a cold door + an injected/returning walk still opens the walk
    pushFace({ face: "door", spread: sp.map((e) => e.id), returned: true });
    scrollTo(0, 0);
    guardHold = 0;                                      // the door rests at its top — the guard holds it here (EX-CHROME)
  }

  addEventListener("popstate", (ev) => {               // Back/Forward walk the faces (INV-32)
    interrupt("popstate");                              // EX-PASS §10.3: the address road stands in
                                                         // front of the walk too — end any transaction
                                                         // in flight before a face renders over it
    const wasWalk = !atDoor;                            // the face we are LEAVING (before any render)
    const wasSide = sideOpen;                           // the side room may be the face we leave (EX-SERIES)
    ceremonyCancel();                                  // navigation wins mid-ceremony (EX-DOOR-2e)
    const st = ev.state && ev.state.@@NS@@;
    // The zoom is the topmost face (INV-83): a Back that leaves it closes ONLY the zoom and stops here,
    // so the room or door beneath keeps its step and no walk_exit or series beat fires. A Forward back
    // INTO a zoom step re-opens it over whatever now stands, laying no new step.
    if (zoomOpen && !(st && st.face === "zoom")) { closeZoom(); return; }
    if (!zoomOpen && st && st.face === "zoom") {
      if (zLastEl && document.body.contains(zLastEl)) openZoom(zLastEl, { lay: false });
      return;
    }
    const toSeries = st && st.face === "series" && typeof st.ser === "number";
    // room → walk: the exit MIRRORS the soft entry (EX-SERIES) — the veil crossing reveals the walk
    // on its exact frame. Only when the walk stands behind; a step to the door or a forward re-open
    // of another series paints its own visuals, so those close the room instantly (below).
    if (wasSide && !toSeries && !(st && st.face === "door")) {
      closeSide(true);
      return;
    }
    closeSide();                                       // instant teardown; the next face paints its own visuals
    if (toSeries) {
      openSide(st.ser, false);                         // Forward re-opens without a new step
      return;
    }
    if (st && st.face === "door") {
      // EX-PULSE registry: a browser-Back (or Forward) leave from the WALK to the door counts ONCE,
      // exactly like the exit control — the funnel undercounted history leaves. The exit control uses
      // pushState (never popstate), so control and history never double-count.
      if (wasWalk) {
        pulse("walk_exit"); noteExit();                  // EX-RETURN/INV-78: a Back-leave counts like the exit control
        // INV-32b: and it remembers the walk's place the same way the exit control does. The spec
        // holds the two leaves alike — the exit control, the browser's own Back landing on the door
        // and a returned-door reload all count as the same door render — so the walk this step
        // returns to must stand where the visitor left it. Measured here, before the door's own
        // scrollTo(0, 0) below rests it at the top and the reading is gone; the same MEASURED
        // centered stop doorReturn takes, so Back restores a whole work rather than a sub-frame offset.
        const stops = frameStops();
        walkY = stops.length ? stops[nearestStop(stops, scrollY)] : 0;
      }
      groundRest();
      // EX-DOOR-4 (F2 folded 11:50): a Back landing on the door over a circled, unanswered walk
      // deals FRESH — the history step's "as it stood" (INV-32a) yields on this one point, and the
      // fresh hand becomes THE standing hand (the step is replaced to carry it).
      const pend = circlePending();
      if (pend) {
        const sp = dealHand(pend);
        renderDoor(sp, st.cold === true);
        replaceFace({ face: "door", spread: sp.map((e) => e.id),
                      returned: st.returned === true, cold: st.cold === true });
        scrollTo(0, 0);
        guardHold = 0;
        return;
      }
      // the door AS IT STOOD: rebuild the carried spread from the pool (never a fresh roll)
      const byPool = Object.fromEntries(doorPool.map((e) => [e.id, e]));
      const sp = (st.spread || []).map((id) => byPool[id]).filter(Boolean);
      renderDoor(sp.length ? sp : undefined, st.cold === true);
      scrollTo(0, 0);
      guardHold = 0;                                    // the returned door rests at its top (EX-CHROME)
      return;
    }
    // a walk step renders the walk AS IT NOW IS (INV-32d) — a dead arc never resurrects
    if (atDoor) {
      closeDoor();
      if (pick && byId[pick]) ground(byId[pick].dom);
      // EX-PASS §1.1: declare refuses an absent destination, so the section this Back is about
      // to rest on (the same measured stop doorReturn remembered as walkY) is named here — the
      // same nearest-stop reading the rotation road already uses, not a null left for the watcher.
      const stops = frameStops();
      const sections = stage.querySelectorAll(".exh-frame, .exh-fin");
      passJump(stops.length ? sections[nearestStop(stops, walkY)] : null, "popstate");
      scrollTo(0, walkY);                              // the closing screen the visitor left (INV-32b)
      tellStory();                                     // a return is a natural beat — any owed portion re-asks (EX-STORY)
    }
  });

/*!08-plaque-caption-io.js*/
  // ---- THE GALLERY (room.html's museum hang — the norm) ----------------------
  const counter = document.createElement("div");
  counter.className = "exh-counter"; counter.id = "exh-counter";
  counter.innerHTML = '<span class="now">01</span> / <span class="tot">–</span>';
  const cap = document.createElement("div");
  cap.className = "exh-capzone"; cap.id = "exh-cap";
  document.body.appendChild(counter);
  document.body.appendChild(cap);
  let focusedId = null;                                 // the work the caption currently speaks for
  let restingEl = null;                                 // the SECTION under the eye (frame or fin) —
                                                        // every re-dock re-measures THIS, never a
                                                        // nearest-by-stale-pixels guess (EX-COMPOSE)
  let lastResizeAt = 0;                                 // the mark FREEZES while a face stands and
  addEventListener("resize", () => { lastResizeAt = performance.now(); });   // through a reflow —
                                                        // a rotation must not drift the eye's mark

  // N7-A11Y (INV-102, EX-HANG): ONE composer of what a screen reader hears on the walk, so the ear and
  // the eye can never drift — the wall label's three voices, then that work's told line if it has one.
  // Its callers are the walk step below and the tongue layer (18), which speaks the label again when a
  // newly picked tongue lands while the guest is already walking.
  function announceLabel(w) {
    if (!w) return;
    const T = (greetLang() || { t: {} }).t;
    announceCaption([(w.title || T.untitled || UNTITLED_EN), (w.sec || ""), (w.place || "")]
      .filter((s) => s && String(s).trim()).join(" · "));
    fillTold();                                         // the line, where the narrator has spoken
  }

  // EX-PASS: ONE owner of «this work is now current». Everything the arriving work switches — the
  // seen mark, the circle's count, the ladder, the remembered place, the tone, the counter, the
  // share link, the plaque, the ear's label, the narrator's next ask — lives in this one function.
  // The in-view watcher below calls it, and so does the end of a transition when the landCommit
  // setting says so; passLandGate lets exactly one of them through per work per generation.
  function landOn(target, reason) {
    // the watcher's own shape, kept whole so the body below reads exactly as it did in the callback
    const x = { target: target };
    // the closing screen is not a work: the plaque must not strand the last work's title + told
    // story over the finale. Fade the caption out like a frame leaving — never a jump, never stale.
    if (x.target.id === "exh-fin") {                   // the closing screen clears the walk chrome
      cap.classList.remove("show"); shareBtn.classList.remove("show"); focusedId = null;
      clearLabelRegion();                              // N7-A11Y (INV-102): the ear loses the label too
      return;
    }
    x.target.classList.add("seen");
    const w = byId[x.target.dataset.id];
    if (!w) return;
    walkSeen.add(String(w.id));                        // the circle counts a mark the MOMENT it is
                                                        // made — no wait for the debounced flush (EX-DOOR-4)
    // the in-flight ladder + the one-ahead preload (EX-LOAD-2/-3) — armed from THIS in-view watcher.
    // The door and the crossing keep their own image handling (they warm the picked work); only the
    // WALK's in-view frame ladders, and only once the ceremony's lock has lifted.
    if (!busy && !atDoor) {
      arm(x.target.querySelector("img.work"), w, x.target);
      preloadAhead(+x.target.dataset.n);
    }
    if (window.__@@NS@@Seen) window.__@@NS@@Seen(w.id);      // the coat-check report (EX-MEMORY)
    // the walk tracks its place per frame in view (INV-32c re-carried after the ↗ retired) — and
    // ONLY while the walk is the surface the visitor stands on. A face over the walk rests at its
    // own top (the door writes scrollTo(0,0) as it renders), so the covered document's first frames
    // cross this watcher's threshold under a scroll the HOUSE wrote, and an unguarded write replaced
    // the place the visitor left with the walk's first work — gone before any return could restore
    // it. The marker HOLDS for the length of the stand, the same freeze faceSync already keeps for
    // the walk's own scroll beneath a standing face (`guardHold`, EX-CHROME/INV-70).
    if (!faceStands()) {
      try { sessionStorage.setItem(PLACE_KEY, JSON.stringify({ v: VER, id: w.id })); } catch (e) {}
    }
    // a late callback must never re-live the tone ON the door (EX-ACCENT rests at the seams)
    if (!atDoor) ground(w.dom);
    counter.querySelector(".now").textContent = String(+x.target.dataset.n).padStart(2, "0");
    counter.classList.add("show");
    // the floating link follows the eye: it always shares the work IN VIEW (EX-SHARE-BTN)
    shareBtn.dataset.share = w.id;
    shareBtn.setAttribute("aria-label", shareStrings().label);
    shareBtn.classList.add("show");
    // his words and the archive's facts only — never machine prose, never a readout (INV-1);
    // a REAL series (3+) grows its quiet pill — «series · N», localized, never the machine's theme (EX-SERIES)
    const serIdx = (typeof w.ser === "number" && SERIES[w.ser]) ? w.ser : null;
    const CT = (greetLang() || { t: {} }).t;
    const serWord = CT.series || SERIES_EN;
    const untitledWord = CT.untitled || UNTITLED_EN;    // every line localizes through EX-I18N; the
                                                        // fallback is ENGLISH (source tongue), never Russian
    // the wall label's three voices: the NAME, the told LINE (empty until the narrator speaks —
    // EX-STORY-LINE fills it from STORYLINES), the FACTS with a red dot when the work is sold
    cap.innerHTML =
      `<div class="title ${w.title ? "" : "untitled"}">${w.title || untitledWord}</div>` +
      `<div class="told"></div>` +
      `<div class="meta"><span class="dot"${w.sold ? "" : " hidden"}></span>` +
      `<span class="t">${w.sec || ""}${w.place ? " · " + w.place : ""}</span></div>` +
      (serIdx == null ? "" :
        `<button type="button" class="ex-series" data-ser="${serIdx}">` +
        `${serWord} · ${SERIES[serIdx].members.length}</button>`) +
      // EX-QUIZ (INV-64/66): a subtle plaque chip — only when this is the ONE chosen work for this
      // show and the arm is "on" and "plaque" is a configured placement (quizShows covers all checks)
      (QUIZ_PLACE.indexOf("plaque") >= 0 && quizShows(w) ? quizChipHTML(w.id) : "");
    cap.classList.add("show");
    focusedId = w.id;
    announceLabel(w);                                  // N7-A11Y (INV-102): the ear gets this label too
    // …which also fills the visible told seat for this work, if the narrator has spoken (EX-STORY)
    storyPreAsk();                                     // near the fork, the NEXT portion asks ahead (INV-89)
    capSettle(x.target.querySelector("img.work"));     // EX-CAPTION (INV-97): seat the caption in the free zone at the frame's settle
  }

  // The watcher itself carries no product state any more: it names the eye's section and hands the
  // arriving work to its one owner. Its threshold is the live landProgress setting, taken EXACTLY —
  // a rounded threshold would make the setting lie about the moment it names. A changed value
  // rebuilds the watcher at the next transition start (EX-PASS), never inside a running one.
  let io = null, ioAt = null;
  function ioSaw(es) {
    es.forEach((x) => {
      if (!x.isIntersecting) return;
      // WHILE A RENDERER HOLDS THE COMMAND, THE COMMAND OWNS WHERE THE WALK IS. The walk's own
      // scroll stands still under the curtain for the whole flight, so a device change arriving
      // mid-flight leaves that standing offset naming a different section in the new viewport, and
      // this watcher then reports a work the visitor is neither on nor going to — which warms its
      // picture ladder and its one-ahead (U10 §4a measured 19 fresh requests on one turn, 18 of
      // them pictures, for a work eight frames away). The report for the command's OWN destination
      // is the arrival and passes exactly as it always did; every other section, for the length of
      // the flight, is the stale offset speaking and is left alone.
      if (passRunning() && passNav && passNav.to
          && passNav.to.id !== ((x.target.dataset && x.target.dataset.id) || null)) return;
      if (!sideOpen && !quizOpen && !giftOpen
          && performance.now() - lastResizeAt > 250) {
        restingEl = x.target;                          // the eye's section, fin included — organic
      }                                                // moves only, never a reflow's stale pixels
      // PASS-API §3: the gate binds the TAKEOVER road, where two landings could actually happen —
      // never the plain walk. With visualLayer off the watcher runs exactly as it does on the
      // shipped engine (fe52eac): every intersecting report re-runs landOn whole, ungated, so a
      // repeat report after a rebuilt threshold or a language switch still refills the caption.
      if (passGet("visualLayer") === "pass") passLandGate(x.target, "observe", landOn);
      else landOn(x.target, "observe");
    });
  }
  function ioBuild() {
    const t = passGet("landProgress");
    const held = [];
    if (io) {
      stage.querySelectorAll(".exh-frame.observed").forEach((f) => held.push(f));
      const fin = document.getElementById("exh-fin");
      if (fin) held.push(fin);
      io.disconnect();
    }
    io = new IntersectionObserver(ioSaw, { threshold: t });
    ioAt = t;
    held.forEach((f) => io.observe(f));                 // a re-watch re-reports what is already in view;
  }                                                    // the gate's per-generation claim absorbs that
  function passObserverSync() { if (passGet("landProgress") !== ioAt) ioBuild(); }
  ioBuild();

  // ---- EX-CAPTION (INV-97/98): the caption keeps to its own space -------------------------------
  // The centred picture is never moved or scaled here (INV-27); the caption block alone measures the
  // real free space it leaves and seats there — the bottom band when the space below the picture holds
  // the block, else a side band on the logical-start edge (below the counter, its reserved neighbour),
  // never over the picture and never under the share rail's reserved column on the end edge. A soft
  // scrim backs the text ONLY where no honest gutter remains. The measure runs at the frame's settle
  // and on a rotation (INV-86) — read from a ResizeObserver on the in-view picture, whose box changes
  // exactly at those beats (load, rotation rescale) and never on a within-frame scroll — so the seat is
  // one layout read per settle, not a continuous reflow. Logical properties carry the RTL mirror.
  const capRO = ("ResizeObserver" in window) ? new ResizeObserver(schedulePlaceCaption) : null;
  let capRaf = 0;
  function schedulePlaceCaption() {
    if (capRaf) return;
    capRaf = requestAnimationFrame(() => { capRaf = 0; placeCaption(); });
  }
  // Re-seat whenever the block's OWN content changes height, not only when the picture's box does: a
  // told-story fills after the first seat (an async story portion resolving, EX-STORY), growing the block
  // AFTER placeCaption already measured a shorter one — on a wide window the grown block would then lie over
  // the picture (the ultra-wide INV-97 hole). This watches the caption's text, not its box, so placeCaption
  // (which sets styles, never text) never re-triggers it — no loop. The rAF coalesces bursts to one seat.
  // CONSTRAINT: nothing with per-tick LIVE text (a countdown, a live "sold" ticker) belongs inside #exh-cap,
  // or this watch would fire every tick and re-seat continuously; keep any live chrome in its own body element.
  const capMO = ("MutationObserver" in window)
    ? new MutationObserver(schedulePlaceCaption) : null;
  if (capMO) capMO.observe(cap, { childList: true, subtree: true, characterData: true });
  function capSettle(img) {
    if (capRO && img) capRO.observe(img);              // observing an element already watched is a no-op
    schedulePlaceCaption();
  }
  function capInViewImg() {                            // the frame nearest the viewport centre (as the probe reads)
    const vh = innerHeight, cy = vh / 2; let best = null, bd = 1e9;
    stage.querySelectorAll("section.exh-frame").forEach((f) => {
      const r = f.getBoundingClientRect();
      if (r.bottom < 0 || r.top > vh) return;
      const d = Math.abs((r.top + r.bottom) / 2 - cy);
      if (d < bd) { bd = d; best = f; }
    });
    return best ? best.querySelector("img.work") : null;
  }
  function placeCaption() {
    if (!cap.classList.contains("show") || faceStands()) return;   // the walk's own frame only (EX-CHROME)
    const img = capInViewImg();
    if (!img) return;
    const W = innerWidth, H = innerHeight;
    const rtl = document.documentElement.getAttribute("dir") === "rtl";
    const pic = img.getBoundingClientRect();
    const cr = counter.getBoundingClientRect();
    const sr = shareBtn.getBoundingClientRect();
    const GAP = 10;                                    // the honest breath between the block and its neighbours
    const CAP_SIDE_FLOOR = 140;                        // INV-97 legibility floor: a free column is an honest
                                                       // gutter only at a readable width — below it (the audit
                                                       // key: a 42px ribbon wrapped a title one letter per line
                                                       // and ran ~2100px past the screen) it is no gutter at all
    const startInset = rtl ? (W - cr.right) : cr.left;                 // the counter holds the start edge
    const endReserve = (rtl ? sr.right : (W - sr.left)) + GAP;         // the share rail's reserved column, end edge
    const startGap   = rtl ? (W - pic.right) : pic.left;              // free width from the start edge to the picture
    // measure the block's natural height in the CSS bottom-band default, then choose the seat
    cap.style.insetInlineStart = ""; cap.style.insetInlineEnd = "";
    cap.style.inlineSize = ""; cap.style.maxInlineSize = ""; cap.style.overflowWrap = "";
    cap.style.top = ""; cap.style.bottom = "";
    cap.style.maxBlockSize = ""; cap.style.overflow = "";        // clear any prior containment clamp
    const bottomInset = W <= 640 ? 14 : 30;
    const topBB = H - bottomInset - cap.offsetHeight;
    if (topBB >= pic.bottom - 1) {                     // the bottom band sits clear below the picture
      cap.style.insetInlineEnd = endReserve + "px";    // still hold the share rail's column clear
      if (W > 640) cap.style.maxInlineSize = "none";
      cap.classList.remove("cap-scrim");
      // Verify the PLACED block actually clears the picture, never trusting the pre-measure alone: the
      // block's final layout can grow past the bottom margin (a told-story that fills after the seat, an
      // ultra-wide rewrap where the wide bottom band reads shorter at measure than it renders). If the
      // seated top still crosses the picture, undo the bottom-band inset and fall through to the side band
      // — a wide window leaves a wide honest side column the block belongs in (INV-97, the felt ultra-wide bug).
      if (cap.getBoundingClientRect().top >= pic.bottom - 1) return;   // truly clear below the picture
      cap.style.insetInlineEnd = ""; cap.style.maxInlineSize = "";     // let the side band / scrim take it
    }
    const sideCol = startGap - startInset;             // the free column from the counter's inset to the picture
    const sideW = sideCol - GAP;                        // the band's own width, a breath shy of the picture
    const SHORT = H <= 640;                             // a short (landscape-phone) window — no vertical room for a bottom band
    // The side band is the seat on a SHORT (landscape) window, where the picture fills the height and leaves
    // no honest bottom margin, so the free zone is the column beside it. On a TALL window (a desktop, a
    // portrait phone) the caption keeps the bottom-left band for EVERY work — the museum label's own home,
    // one stable seat — and the scrim below backs the text only where a tall or square picture's bottom
    // reaches it. (His 2026-07-22 find: on a square-dominant portfolio the aspect-driven side seat put the
    // label top-left for most works and made it jump top↔bottom between works and with the window height;
    // the bottom band is the stable seat, chosen on his word. INV-97 desktop rule.)
    if (SHORT && sideCol >= CAP_SIDE_FLOOR) {          // an honest side column beside the picture, short window
      const topPx = cr.bottom + GAP;                    // below the counter's line (block axis, unmirrored)
      cap.style.top = topPx + "px";
      cap.style.bottom = "auto";
      cap.style.insetInlineStart = startInset + "px";
      cap.style.inlineSize = sideW + "px";
      cap.style.maxInlineSize = "none";
      cap.style.overflowWrap = "anywhere";             // a narrow worst-case band breaks long words rather than spilling onto the work
      cap.classList.remove("cap-scrim");
      // INV-97 containment: the seated block always ends within the viewport. A band taller than the room
      // below the counter is clamped to that room — it stays an honest side band and never runs off-screen;
      // the scrim below is only for a sub-floor column, not for an honest one.
      if (cap.getBoundingClientRect().bottom > H - bottomInset + 1) {
        cap.style.maxBlockSize = Math.max(0, H - bottomInset - topPx) + "px";
        cap.style.overflow = "hidden";
      }
      return;
    }
    if (!SHORT) {
      // A TALL window keeps the bottom-left band (the CSS default seat cleared above). A short caption
      // sits clear in the bottom-left column beside a tall/square picture and needs no backing; a long
      // one reaches the work, and only THEN does the scrim back it. The measure is the placed block's own
      // rect against the picture's — the scrim paints only on an actual crossing (INV-97 keeps it rare).
      cap.classList.remove("cap-scrim");
      const cb = cap.getBoundingClientRect();
      if (cb.left < pic.right && cb.right > pic.left && cb.top < pic.bottom && cb.bottom > pic.top)
        cap.classList.add("cap-scrim");
      return;
    }
    cap.classList.add("cap-scrim");                    // a short window with no honest side column — the last resort backs the text (INV-97)
  }

/*!09-story-voice.js*/
  // ---- the told line settles onto the plaque (EX-STORY-LINE / EX-STORY-WAIT) ----
  // A focused work's told-slot wears one of three states while the plot travels (EX-STORY-WAIT):
  //   pending — its portion is in flight and the line has not landed: a quiet wait mark holds the
  //             seat (never a finished line), so the guest who arrives ahead of the voice sees the
  //             narrator is about to speak rather than an empty, silent slot (pictures already
  //             carry their own loading plate — EX-LOAD-2 — the line matches that grace);
  //   arrived — the line is here: it settles as textContent (the model's words never become markup)
  //             and breathes in on the tempo, a single house fade even when it lands late (EX-ARRIVE);
  //   failed/owed/off — no request in flight and no line: silent exactly as before, :empty hides the
  //             slot with no ghost gap, and the picture stays whole (a refused portion loses nothing).
  // portionPending answers whether the focused work sits in a portion whose request is still in flight.
  let storyGen = 0;                                    // bumped on every fresh arc so a pending retry from a previous walk stands down
  // A portion whose request FAILED but still has a retry queued: it is no longer in flight (its
  // askingPortions key was dropped) yet the narrator is still about to speak, so the wait mark must
  // HOLD across the retry gap and clear to silence only when the LAST retry is spent. Without this the
  // dots froze forever on a focused work after a portion gave up (his 2026-07-23: «перезагрузил и всё
  // равно нет сторителлинга» — a failed portion left the wait mark painted, never repainting to
  // silence, because owed() dropped the in-flight key but nothing re-ran fillTold).
  const retryingPortions = new Set();
  // EX-STORY-FILL (INV-107): a work whose portion's plot came back carrying no line for it waits in
  // the OWED set and travels by its OWN ask — a request naming that work by id and marked as a
  // one-work ask, so the edge keys and locks it under its own shape. A work leaves the set when a
  // line is seated for it or when the walk is replaced. A work in the set with an ask in flight or a
  // re-ask queued wears the wait mark; a work in the set with neither shows silence.
  const owedWorks = new Set();
  const askingWorks = new Set();                       // its own ask is in flight
  const retryingWorks = new Set();                     // its own ask failed and a re-ask is queued
  const triedWorks = new Set();                        // its own ladder came to rest — it waits for a
                                                       // fresh arc, so a work the edge can never answer
                                                       // for spends one ask rather than the hour's five
  const SOLO_PER_HOUR = 5;                             // a browser's own asks per CLOCK hour — the unit
                                                       // the edge's per-address ceiling counts in
  function markOwed() {
    try { window.__@@NS@@Owed = Array.from(owedWorks); } catch (e) {}   // test read-side
  }
  function portionPending(id) {
    if (id == null) return false;
    const w = String(id);
    if (askingWorks.has(w) || retryingWorks.has(w)) return true;   // its OWN ask is travelling
    const s = "," + String(id) + ",";
    for (const key of askingPortions) {                // in flight now
      if (("," + key + ",").indexOf(s) !== -1) return true;
    }
    for (const key of retryingPortions) {              // failed, but a retry is still queued to land it
      if (("," + key + ",").indexOf(s) !== -1) return true;
    }
    return false;
  }
  function fillTold() {
    const toldEl = cap.querySelector(".told");
    if (!toldEl) return;
    const id = focusedId != null ? String(focusedId) : null;
    const line = id != null ? STORYLINES[id] : "";
    if (line) {                                        // arrived — the narrator's line, faded in
      // N7-A11Y (INV-102, EX-HANG): the ONE road every told line takes to the ear, whichever way it
      // came — a portion's coordinated reveal or a one-work ask's own landing. It reads the work IN
      // VIEW, so a line landing for a work the guest has left is announced nowhere, and the step's own
      // slot keeps a second arrival over the same seat silent.
      announceLine(line);
      if (toldEl.textContent === line && !toldEl.querySelector(".told-wait")) return;
      toldEl.textContent = line;                       // replaces any wait mark held in the seat
      toldEl.style.animation = "none"; void toldEl.offsetWidth; toldEl.style.animation = "";  // EX-ARRIVE
      return;
    }
    if (id != null && portionPending(id)) {            // pending — the quiet wait mark holds the seat
      if (toldEl.querySelector(".told-wait")) return;  // already marked — never restart its breath
      toldEl.innerHTML = '<span class="told-wait" aria-hidden="true"></span>';
      return;
    }
    toldEl.textContent = "";                           // silent → :empty hides it, no ghost gap
  }
  // revealPortion draws a whole resolved portion's lines in ONE coordinated reveal (a single
  // eye-draw, never a per-line trickle): every one of the portion's told lines is already written
  // into STORYLINES together by the caller, so as the eye lands on any of its works the line is
  // there — the work in view fades from its wait mark to its line on the one house breath.
  function revealPortion() {
    try { window.__@@NS@@Reveals = (window.__@@NS@@Reveals || 0) + 1; } catch (e) {}  // test read-side
    fillTold();                                        // settle the line under the work in view
  }

  // The story's unit is the PORTION just opened (EX-STORY — a plot per opened portion). The walk's
  // works fall into portions by the very boundaries the unfolding lays: the cold first spread, then
  // each «ещё 5». Every portion asks /api/story for ITS OWN ordered ids alone — never the grown
  // 0..shown set — so each plot lands under its own edge cache key and a line already read is never
  // re-requested and never shifts. A portion counts as told only once its plot has come back: its
  // key is stamped on success alone, so a refused or failed portion stays owed and is re-asked at the
  // next natural beat — the next unfold or a return to the walk. The edge's own wait carries any
  // Retry-After: a re-ask that lands inside the window is refused server-side (429/dead-flag, before
  // any model call) and the portion simply stays owed, so the client re-asks freely and holds no
  // backoff clock of its own. Every failure path is silence (CS-8, INV-19).
  // EX-STORY-LEAD: the first spread carries TWO portions — a short opening plot over the first
  // STORY_LEAD works, then one plot over the rest of that spread. The opening one is asked the moment
  // the walk stands; the remainder waits until the visitor comes within a work of it (storyPreAsk),
  // so a visit that rests in the first few works never buys the whole spread's telling. Each portion
  // still lands under its own edge cache key, and a shorter opening slice repeats across visitors
  // more often, so it is served from that cache more often as well.
  function storyPortions(n) {                          // [[lo,hi], …] over order indices, the unfold's own beats
    const parts = [];
    const first = Math.min(SPREAD, n);
    if (first > 0) {
      const lead = Math.min(STORY_LEAD, first);
      parts.push([0, lead]);
      if (lead < first) parts.push([lead, first]);
    }
    for (let s = first; s < n; ) { const e = Math.min(n, s + UNFOLD); parts.push([s, e]); s = e; }
    return parts;
  }
  // A portion inside the FIRST spread past the opening one waits for the visitor to come near it;
  // every other portion is asked at its own beat, exactly as before (an unfold opens its own slice).
  function portionReached(lo) {
    if (lo <= 0 || lo >= SPREAD) return true;
    if (focusedId == null) return false;
    const idx = order.indexOf(focusedId);
    return idx >= 0 && idx >= lo - 1;
  }
  // An owed portion (a refused, failed, or dead-worker outcome) re-asks ITSELF a bounded number of
  // times before it falls back to waiting for the next natural beat (an unfold, a return). Without it
  // a transient hiccup on the FIRST portion left the opening plaques silent until the visitor unfolded
  // — «иногда открываю и нет рассказика» (his find 2026-07-22). Every path stays silence (CS-8,
  // INV-19): a retry shows nothing either, it only gives the plot a few more chances to land. The
  // re-ask waits SECONDS, so a server Retry-After window has passed by then; a fresh arc bumps storyGen
  // (storyReset) so a pending retry from a previous walk never lands its slice in the new one.
  const STORY_RETRY_MS = [2500, 6000];
  function askPortion(loI, hiI, settle, attempt) {
    attempt = attempt || 0;
    const gen = storyGen;
    const done = () => { if (settle) { const f = settle; settle = null; f(); } };   // once, any outcome
    const ids = order.slice(loI, hiI).map(String);
    if (!ids.length) { done(); return; }
    const key = ids.join(",");                         // this portion's own ordered slice — its cache key
    if (toldPortions.has(key) || askingPortions.has(key)) { done(); return; }   // already told, or in flight
    const owed = () => {                               // the plot did not land — re-ask shortly, then wait for a beat
      done();
      if (attempt >= STORY_RETRY_MS.length || !STORY_ON) {
        retryingPortions.delete(key);                  // no retry left — the portion truly gives up…
        fillTold();                                    // …so the focused work's wait mark clears to silence (CS-8, INV-19), never a frozen dot
        return;
      }
      retryingPortions.add(key);                       // a retry is queued — the wait mark HOLDS across the gap (portionPending stays true)
      setTimeout(() => {
        retryingPortions.delete(key);
        if (gen !== storyGen) return;                  // a fresh arc opened — this slice belongs to the old walk
        if (toldPortions.has(key) || askingPortions.has(key)) return;   // already served / re-asked elsewhere
        askPortion(loI, hiI, null, attempt + 1);
      }, STORY_RETRY_MS[attempt]);
    };
    askingPortions.add(key);
    const lang = (viewerLang() || "en").toLowerCase();
    const t0 = performance.now();                      // EX-PULSE/INV-79: the round-trip clock (bucketed, never raw)
    fetch("/api/story", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ids: ids, variant: STORY_VARIANT, lang: lang }),
    }).then((r) => (r && r.ok ? r.json() : null)).then((data) => {
      // A fresh door pick opened a new arc while this plot travelled: it belongs to the walk that is
      // gone, so it is dropped WHOLE — its lines, its told stamp and its reveal (EX-STORY reset).
      // The check stands AHEAD of every set change: picking the same door twice reproduces this very
      // portion key, and dropping it would tear down the NEW walk's own in-flight mark.
      if (gen !== storyGen) { done(); return; }
      askingPortions.delete(key);
      if (!data || !Array.isArray(data.lines)) { owed(); return; } // refused/failed → key NOT stamped → re-asks, then stays owed
      toldPortions.add(key);                           // told only once the plot has actually come back
      // EX-PULSE/INV-79: the portion's round-trip lands — its lag rides a coarse bucket, and the RACE
      // word marks whether the guest already stood at a work in THIS portion whose line had not yet
      // arrived (they saw the empty slot) — measured BEFORE the lines fill in, so `late` is honest.
      const fid = focusedId != null ? String(focusedId) : null;
      const raced = !!(fid && ids.indexOf(fid) !== -1 && !STORYLINES[fid]);
      pulse("story_told", null, { lag: lagBucket(performance.now() - t0), race: raced ? "late" : "ahead" });
      storyVariant = data.story_variant || STORY_VARIANT;   // the mode now rides the GA beats
      for (const l of data.lines) {                    // the whole portion's lines land TOGETHER…
        if (l && l.id != null && typeof l.line === "string") STORYLINES[String(l.id)] = l.line;
      }
      // EX-STORY-FILL (INV-107): read the plot against the ids this request asked for — a work the
      // plot passed over joins the owed set and is asked for on its own. The asks REGISTER here,
      // before the coordinated reveal, so a wordless seat moves from one wait mark to the next with
      // no blank between them.
      for (const id of ids) {
        const w = String(id);
        if (STORYLINES[w]) owedWorks.delete(w); else owedWorks.add(w);
      }
      markOwed();
      sweepOwed();
      revealPortion();                                 // …then ONE coordinated reveal (EX-STORY-WAIT)
      done();
    }).catch(() => {                                   // a dead worker → re-ask shortly, then the portion stays owed
      if (gen !== storyGen) { done(); return; }        // the arc it belonged to is gone
      askingPortions.delete(key);
      owed();
    });
  }
  // ---- EX-STORY-FILL (INV-107): the one-work ask ----------------------------------------------
  // A browser spends at most SOLO_PER_HOUR own asks per CLOCK hour — the unit the edge's per-address
  // ceiling counts in. The count stands through a door pick, so a second walk inherits what the first
  // spent: at the shipped knobs two walks of 9 rungs plus five asks of 3 rungs reach 33 against the
  // per-address ceiling of 40 (EX-EDGE-GUARD). A knob raised past that makes this sentence read false.
  function soloTake() {
    const hour = Math.floor(Date.now() / 3600000);
    let rec = null;
    try { rec = JSON.parse(localStorage.getItem(SOLO_KEY) || "null"); } catch (e) {}
    if (!rec || rec.h !== hour) rec = { h: hour, n: 0 };   // a new clock hour brings a fresh count
    if (rec.n >= SOLO_PER_HOUR) return false;
    rec.n++;
    try { localStorage.setItem(SOLO_KEY, JSON.stringify(rec)); } catch (e) {}
    return true;
  }
  // The ask names the work by ID — never an order slice, which would land on whatever work sits at
  // that position after a fresh pick. It rides the portion ladder's own bounds (the ask and two
  // re-asks); the hour's count is taken once per ASK, at the sweep, so a ladder costs one slot.
  function askWork(id, attempt) {
    attempt = attempt || 0;
    const gen = storyGen;
    const w = String(id);
    if (askingWorks.has(w) || STORYLINES[w]) return;
    askingWorks.add(w);
    const lang = (viewerLang() || "en").toLowerCase();  // the live tongue, read as the ask goes out
    fetch("/api/story", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ids: [w], variant: STORY_VARIANT, lang: lang, one: true }),
    }).then((r) => (r && r.ok ? r.json() : null)).then((data) => {
      if (gen !== storyGen) return;                    // the arc it was born from is gone — and the
      askingWorks.delete(w);                           // NEW walk's own mark for this work must stand
      const found = (data && Array.isArray(data.lines))
        ? data.lines.find((l) => l && String(l.id) === w && typeof l.line === "string" && l.line)
        : null;
      if (!found) { soloOwed(w, gen, attempt); return; }
      STORYLINES[w] = found.line;                      // the line settles on the house breath (EX-ARRIVE)
      owedWorks.delete(w);
      markOwed();
      fillTold();                                      // …and reaches the ear by the walk step's own law
    }).catch(() => {
      if (gen !== storyGen) return;
      askingWorks.delete(w);
      soloOwed(w, gen, attempt);
    });
  }
  function soloOwed(w, gen, attempt) {                 // this ask's own bounded ladder
    if (attempt >= STORY_RETRY_MS.length || !STORY_ON) {
      retryingWorks.delete(w);                         // the ladder is spent — the work stays owed…
      triedWorks.add(w);                               // …and rests: a further beat asks it no more,
      fillTold();                                      // so one unanswerable work never eats the hour's
      return;                                          // whole count. Its seat clears to silence (INV-8).
    }
    retryingWorks.add(w);                              // a re-ask is queued — the wait mark HOLDS
    setTimeout(() => {
      if (gen !== storyGen) return;                    // ahead of the set change, as everywhere here
      retryingWorks.delete(w);
      if (STORYLINES[w]) return;
      askWork(w, attempt + 1);
    }, STORY_RETRY_MS[attempt]);
  }
  // The owed set is swept at the walk's own beats — the hang building, an unfold, a return to the
  // walk, and the focus beat that already asks the next portion ahead. The sweep stands AHEAD of that
  // beat's own conditions, so it runs when the unfolds are spent and the guest walks on, which is
  // where a work standing late in the last portion is reached. The works are taken in the WALK's own
  // order, so the ones the guest meets first are asked first; a work the hour's count cannot reach
  // stays owed and shows silence, and the next hour's count can reach it while he is still walking.
  function sweepOwed() {
    if (!STORY_ON || !owedWorks.size) return;
    for (const id of order) {
      const w = String(id);
      if (!owedWorks.has(w) || STORYLINES[w]) continue;
      if (askingWorks.has(w) || retryingWorks.has(w) || triedWorks.has(w)) continue;
      if (!soloTake()) return;                         // the hour is spent — the rest stay owed
      askWork(w, 0);
    }
  }
  // tellStory re-asks every portion up to `shown` that is not yet told: the newly opened one on an
  // «ещё 5», plus any earlier portion still owed from a refusal (re-asked at this natural beat). A
  // told portion returns free from cache; an owed one waits for the next beat. Called at each beat —
  // the hang builds, an unfold grows the set, a return re-shows the walk.
  function tellStory() {
    if (!STORY_ON) return;
    sweepOwed();                                       // the owed works ride this beat too (EX-STORY-FILL)
    for (const [lo, hi] of storyPortions(shown)) { if (portionReached(lo)) askPortion(lo, hi); }
  }
  // EX-STORY-BEAT (INV-89): the voice stays ahead at the fork — as the focus comes within two
  // works of the spread's end, the NEXT portion (the very slice an «ещё 5» would open) is asked
  // ahead, gated on that proximity so intent pays for it. The portion keys dedupe, so the unfold's
  // own tellStory finds the plot in flight or served, never double-charged; when no next portion
  // exists (the arc spent, the unfolding retired) nothing is asked.
  function storyPreAsk() {
    if (!STORY_ON) return;
    sweepOwed();                                       // ahead of this beat's OWN conditions, so an owed
                                                       // work is reached once the unfolds are spent
    // EX-STORY-LEAD: the rest of the first spread is asked here, as the focus comes within a work of
    // it. Only a portion INSIDE the first spread rides this beat: a portion an unfold opened keeps
    // the cadence it always had — its own unfold, a return to the walk, or its bounded self-retry —
    // so a refused slice is never re-asked once per scroll. The portion keys dedupe, so a slice
    // already told or in flight costs nothing to name again.
    for (const [lo, hi] of storyPortions(shown)) {
      if (lo > 0 && lo < SPREAD && portionReached(lo)) askPortion(lo, hi);
    }
    if (focusedId == null) return;
    if (spentUnfolds() >= MAXU || shown >= order.length || shown >= CAP) return;   // no next portion
    const idx = order.indexOf(focusedId);
    if (idx < 0 || idx < shown - 2) return;            // not yet near the fork
    askPortion(shown, Math.min(order.length, shown + UNFOLD, CAP));
  }
  // A fresh door pick is a fresh arc, so it is a fresh story — the previous walk's told/owed portions
  // and its lines never leak into the new one (EX-STORY / INV-30/31).
  function storyReset() {
    storyGen++;                                        // a fresh arc — any owed-portion retry from the old walk stands down
    toldPortions.clear();
    askingPortions.clear();
    retryingPortions.clear();                          // …including a portion still queued for retry (its wait mark clears with the arc)
    owedWorks.clear();                                 // every outstanding own ask stands down with the
    askingWorks.clear();                               // arc it belonged to (EX-STORY-FILL/INV-107); the
    retryingWorks.clear();                             // HOUR's count is not touched — it stands through a pick
    triedWorks.clear();
    markOwed();
    for (const k in STORYLINES) delete STORYLINES[k];
    storyVariant = null;
  }

/*!10-share-toast.js*/
  // ---- EX-SHARE: the quiet per-frame affordance — it copies, never navigates ----
  // (the ↗ corner link out to /w/ RETIRED with it, 2026-07-06 evening; /w/ pages stay
  // the machines' surface, reachable from the static index — CS-6)
  const SHARE_GLYPH =
    '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor"' +
    ' stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
    '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/>' +
    '<path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>';
  const shareStrings = () => {
    const L = greetLang();
    const T = L ? L.t : {};
    return {                                           // RU built-ins stand under a missing cache
      label: T.share_label || "скопировать ссылку",
      copied: T.share_copied || "ссылка скопирована",
    };
  };

  // the toast — one quiet line; the success face leaves by itself, the refusal face
  // CARRIES the link and stays until dismissed (a tap, Esc) — it must be hand-copyable
  const toastEl = document.createElement("div");
  toastEl.id = "ex-toast";
  toastEl.hidden = true;
  toastEl.setAttribute("role", "status");              // announced politely, never interrupts
  toastEl.setAttribute("aria-live", "polite");
  document.body.appendChild(toastEl);
  let toastTimer = null;
  function toastOff() {
    clearTimeout(toastTimer); toastTimer = null;
    toastEl.classList.remove("show", "hold");             // EX-ARRIVE: drop the show class first
    toastEl.hidden = true;
  }
  function toast(text, hold) {
    clearTimeout(toastTimer); toastTimer = null;
    toastEl.classList.remove("show");                     // EX-ARRIVE: reset so rAF re-fires the fade
    toastEl.textContent = text;
    toastEl.classList.toggle("hold", !!hold);
    toastEl.hidden = false;
    requestAnimationFrame(() => { toastEl.classList.add("show"); }); // EX-ARRIVE: breath in
    if (!hold) toastTimer = setTimeout(toastOff, Math.round(1600 * TEMPO)); // long enough to READ the two-word line, then gone — never a lingering banner (his 2026-07-23)
  }
  toastEl.addEventListener("click", toastOff);
  addEventListener("keydown", (ev) => { if (ev.key === "Escape") toastOff(); });

  // ---- N7-A11Y (INV-102 / F5): two polite live regions beside the toast — one creator, disciplined
  // writers. The caption-and-line region carries what the VISIBLE wall label carries for the work in
  // view: the caption (REPLACE on each walk step, from the caption plaque 08) and that one work's told
  // line appended under it (from the story's seat-filling path 09, wherever the line arrived from — a
  // portion's reveal or a one-work ask), at most once per step. The result region takes the quiz
  // verdict (13) and the gift result (11) on a REPLACE discipline. A told line and a result therefore
  // land in DIFFERENT nodes and never overwrite each other. Both are visually hidden (screen-reader
  // present) via inline style, so no CSS dependency is added.
  function srLive(id) {
    const el = document.createElement("div");
    el.id = id;
    el.className = "ex-sr-live";
    el.setAttribute("role", "status");
    el.setAttribute("aria-live", "polite");
    el.style.cssText = "position:absolute;width:1px;height:1px;margin:-1px;padding:0;border:0;" +
      "overflow:hidden;clip:rect(0 0 0 0);clip-path:inset(50%);white-space:nowrap;";
    document.body.appendChild(el);
    return el;
  }
  const liveCap = srLive("ex-live-cap");               // caption (replace) + this work's told line (once)
  const liveResult = srLive("ex-live-result");         // quiz verdict + gift result (replace), a SEPARATE node
  // The step's line slot: a caption opens it, the line closes it. It starts CLOSED, so a line can never
  // stand in the region with no label above it (the door, the closing screen).
  let capLineSaid = true;
  function announceCaption(text) {                     // a walk step REPLACES — the prior label goes whole
    if (text == null) return;
    const d = document.createElement("div");
    d.className = "ex-sr-cap"; d.textContent = String(text);
    liveCap.replaceChildren(d);
    capLineSaid = false;                               // …and opens this step's one line slot
  }
  function clearLabelRegion() {                        // the closing screen: the label goes, the region with it
    liveCap.replaceChildren();
    capLineSaid = true;
  }
  function announceLine(text) {                        // the work IN VIEW's told line, once per step
    if (!text || capLineSaid) return;
    const d = document.createElement("div");
    d.className = "ex-sr-told"; d.textContent = String(text);
    liveCap.appendChild(d);
    capLineSaid = true;
  }
  function announceResult(text) {                       // the SEPARATE result region, REPLACE discipline
    if (text == null) return;
    const d = document.createElement("div");
    d.className = "ex-sr-result"; d.textContent = String(text);
    liveResult.replaceChildren(d);
  }

  // ---- EX-SHARE join (INV-1): a copied link carries a FRESH random per-share token `s` so GA
  // can join THIS specific share to the specific open it produces (the virality loop / k-factor).
  // The token is minted per click, is a bounded closed-alphabet word, and carries NO visitor
  // identity — a random draw, never the coat-check token — so the loop closes without linking
  // people (INV-1: no free text, no identity on the wire).
  function mintShareToken() {
    try {
      const b = new Uint8Array(6);
      crypto.getRandomValues(b);
      return Array.from(b, (x) => (x % 36).toString(36)).join("");
    } catch (e) { return Math.random().toString(36).slice(2, 8); }
  }
  function shareTokenExtra() {                          // read `s` off THIS arrival's query, closed-shape
    try {
      const m = (location.search || "").match(/[?&]s=([a-z0-9]{1,16})(?:&|$)/);
      if (m) return { s: m[1] };                        // validated shape ⇒ safe to ride (INV-1)
    } catch (e) {}
    return undefined;                                   // no token ⇒ the payload is byte-for-byte today's
  }

  // ---- EX-SHARE-ORIGIN (INV-1): the channel a visit first arrived under, folded to a closed shape ----
  // A value riding a stranger's own link (a folded `o` already on the address, else `utm_content`, else
  // `utm_source` — the first one found wins) is never free text on the wire: lowercased, cut to the
  // closed alphabet of letters, digits, hyphen and underscore, capped at 32 characters. An empty
  // result rides nothing.
  function foldOrigin(raw) {
    return String(raw || "").toLowerCase().replace(/[^a-z0-9_-]+/g, "").slice(0, 32);
  }
  function readOriginParam() {
    try {
      const q = new URLSearchParams(location.search);
      return foldOrigin(q.get("o") || q.get("utm_content") || q.get("utm_source") || "");
    } catch (e) { return ""; }
  }
  // the FIRST channel this visit arrived under survives every forward: a folded origin already
  // stored for this visit wins outright — only an EMPTY store takes THIS load's own reading — so a
  // visitor who opens a forwarded copy keeps the channel their own first arrival met, never the
  // copy's bare marks. Per-visit (sessionStorage), wiped with its siblings on ?reset (EX-RESET).
  let shareOrigin = null;
  try { shareOrigin = sessionStorage.getItem(ORIGIN_KEY) || null; } catch (e) {}
  if (!shareOrigin) {
    const o = readOriginParam();
    if (o) {
      shareOrigin = o;
      try { sessionStorage.setItem(ORIGIN_KEY, o); } catch (e) {}
    }
  }
  function shareArriveExtra() {                          // the join token AND the remembered channel, only when present
    const extra = shareTokenExtra() || {};
    if (shareOrigin) extra.origin = shareOrigin;
    return Object.keys(extra).length ? extra : undefined;
  }

  // ONE share control FLOATS over the walk (2026-07-09: the player and the link are chrome
  // ABOVE the room — they never ride a frame, so nothing drifts with a scroll). It acts on the
  // work IN VIEW (dataset.share follows the frame observer) and lives by the caption's law:
  // shows with a work, leaves on the closing screen, the door hides all walk chrome.
  const shareBtn = document.createElement("button");
  shareBtn.type = "button";
  shareBtn.className = "ex-share";
  shareBtn.id = "ex-share";
  shareBtn.innerHTML = SHARE_GLYPH;
  document.body.appendChild(shareBtn);
  shareBtn.addEventListener("click", () => {
    const id = shareBtn.dataset.share;
    if (!id) return;
    // The copied line carries UTM attribution (EX-SHARE-BTN) so a shared arrival separates
    // from Direct/bot noise — the utm rides before the hash (GA reads the query, the room reads #w-<id>).
    // A fresh per-share token `s` rides too (EX-SHARE join / INV-1), stamped on this copy so the
    // matching arrival joins back to it.
    const s = mintShareToken();
    // a stored origin (this visit's own remembered channel, EX-SHARE-ORIGIN) rides onward beside the
    // house source mark and the join token; with nothing stored the link keeps exactly today's shape.
    const link = ROOT_URL + "/?utm_source=share&utm_medium=referral&s=" + s +
      (shareOrigin ? "&o=" + shareOrigin : "") + "#w-" + id;
    const S = shareStrings();
    const write = (navigator.clipboard && navigator.clipboard.writeText)
      ? navigator.clipboard.writeText(link)
      : Promise.reject(new Error("no clipboard"));
    pulse("share_copy", id, shareOrigin ? { s: s, origin: shareOrigin } : { s: s });
    write.then(() => toast(S.copied))
         .catch(() => toast(link, true));              // never a silent failure (EX-SHARE-BTN)
  });

/*!11-protect-gift.js*/
  // ---- EX-PROTECT (INV-49): a grabbed work meets a GIFT, not the browser's raw save ----
  // A right-click / long-press (contextmenu) or a drag on a work is intercepted and answered by
  // the SAME toast the share line rides — a quiet localized «enjoy» + the site host, arriving on
  // the house breath (EX-ARRIVE). It is a gracious line, never a scold or an error.
  // (CSS `user-select:none` / `touch-action:pan-x pan-y` / `-webkit-touch-callout:none` on
  // img.work handle the soft layer; these listeners handle contextmenu + drag + pinch-zoom.)
  function enjoyLine() {
    const T = (greetLang() || { t: {} }).t;
    const host = ROOT_URL.replace(/^https?:\/\//, "");   // «example.com», appended in code
    const enjoy = T.enjoy || ENJOY_EN;                    // every line localizes through EX-I18N; the
                                                          // fallback is ENGLISH (source tongue), never Russian
    return enjoy + " · " + host;                          // never blank (EX-PROTECT empty/error facet)
  }
  // EX-PROTECT-RES (INV-56): the download filename base — the site's OWN HOST from config (INV-28),
  // never a hardcoded brand. A grabbed file is «<host>-<original>.jpg», so the picture carries the
  // gallery's domain wherever it lands (the same host the watermark stamps). The host's leading label
  // is taken (tlvphotos.com → tlvphotos), a plain slug, with a never-blank fallback.
  const DL_BASE = ((ROOT_URL.replace(/^https?:\/\//, "").split("/")[0].split(":")[0].split(".")[0])
                   .toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "")) || "gallery";
  // EX-PROTECT-RES (INV-56): the file an ORDINARY grab hands over is capped on its LONG EDGE, on every
  // screen. The walk's <img> resolves the responsive ladder to 640 / 960 / 1280 px by viewport x pixel
  // density, so on a retina screen a right-click used to carry away a 1280 px file — LARGER than the
  // quiz prize, which is the pre-marked ~1000 px bake. The prize is the reward for playing, so it must
  // be the better file: the ceremony grab is drawn DOWN to this cap before it is stamped and encoded.
  // The shown image is untouched — this governs only the copy that leaves the machine. An image already
  // inside the cap is drawn at its own size (the cap never enlarges), and the quiz prize never travels
  // this road at all (it goes out as the fetched pre-marked bytes).
  const GRAB_MAX_PX = 800;        // [default] the long edge of a grabbed file (his word 2026-07-28)
  // ---- EX-PROTECT-GIFT: the picture is OFFERED, never dumped ----
  // The gift CEREMONY (his word 2026-07-08): a right-click on a work is answered by a gentle card
  // «like it? · a gift :)» and the picture is handed over only on a yes — never a blunt auto-download.
  // A won quiz ends in the SAME ceremony at better resolution. Rides the house breath (EX-ARRIVE);
  // Esc / click-outside close it.
  const giftCard = document.createElement("div");
  giftCard.id = "ex-gift-card";
  giftCard.setAttribute("role", "dialog");
  giftCard.setAttribute("aria-modal", "true");
  // N7-A11Y (INV-102, C4/C5): the ceremony names itself to a screen reader (localized, EN fallback)
  giftCard.setAttribute("aria-label", ((greetLang() || { t: {} }).t.a11y_gift) || A11Y_GIFT_EN);
  giftCard.hidden = true;
  giftCard.innerHTML =
    '<div class="gift-inner">' +
      '<div class="gift-ask"></div>' +
      '<div class="gift-act">' +
        '<button type="button" class="gift-yes"></button>' +
        '<button type="button" class="gift-no"></button>' +
      '</div>' +
      '<div class="gift-line"></div>' +
      '<div class="gift-buy"></div>' +
    '</div>';
  document.body.appendChild(giftCard);
  let giftOpen = false;
  function giftName(src, name) {
    // The handed file is always a JPEG — a raw source is `.jpg`, and a stamped grab is re-encoded
    // image/jpeg through the canvas. So the download name carries `.jpg` regardless of the source's
    // own extension, and the label always matches the bytes (a config `name` override owns its own).
    if (name) return name;
    const base = ((src.split("/").pop() || "photo").split("?")[0]).replace(/\.[a-z0-9]+$/i, "");
    return DL_BASE + "-" + base + ".jpg";
  }
  // EX-PROTECT-RES (INV-56): the file reaches the visitor's device by the road that device expects.
  // A phone `<a download>` does NOT reach the Photos library — iOS Safari drops the bytes into Files
  // or nowhere, which is why a saved grab «went somewhere unclear» (his find 2026-07-22). The one web
  // road into Photos is the native share sheet's «Save Image», so a coarse-pointer device is handed
  // the file through navigator.share; the desktop keeps the direct anchor save. A dismissed sheet
  // saves nothing and drops no second copy to Files — the visitor closed it (INV-1 silence).
  function anchorSave(blobOrUrl, name) {
    const isBlob = (typeof Blob !== "undefined") && (blobOrUrl instanceof Blob);
    const url = isBlob ? URL.createObjectURL(blobOrUrl) : blobOrUrl;
    const a = document.createElement("a");
    a.href = url; a.download = name;
    document.body.appendChild(a); a.click(); a.remove();
    if (isBlob) setTimeout(() => URL.revokeObjectURL(url), 5000);
  }
  function saveBlob(blob, name) {
    try {
      const file = new File([blob], name, { type: (blob && blob.type) || "image/jpeg" });
      if (matchMedia("(pointer: coarse)").matches
          && navigator.canShare && navigator.canShare({ files: [file] })) {
        navigator.share({ files: [file] }).catch((err) => {   // the sheet's «Save Image» → Photos
          // a closed sheet is the visitor's choice — save nothing (INV-1 silence). Any OTHER refusal
          // (e.g. an activation lost on a very fast yes) falls to the anchor so a file still leaves.
          if (err && err.name === "AbortError") return;
          anchorSave(blob, name);
        });
        return;
      }
    } catch (e) { /* an engine without file-share falls through to the anchor */ }
    anchorSave(blob, name);
  }
  // The last-resort road, reached ONLY when the canvas itself refused (a decode failure, a tainted
  // canvas, a toBlob that returned nothing). It hands over the source bytes as they are, so it carries
  // neither the host mark nor the GRAB_MAX_PX cap — the same canvas that would resize is the one that
  // just failed, so no other road is left. A browser that cannot stamp still gets its picture rather
  // than an error (INV-56's never-blocked clause); the marked, capped file is what every working
  // browser receives.
  function rawDownload(src, name) {
    try { anchorSave(src, giftName(src, name)); } catch (e) { /* the walk loses nothing if a browser refuses the save */ }
  }
  // EX-PROTECT-RES (INV-56): the SHOWN image is CLEAN; the site-host mark is stamped ONLY on a TAKEN
  // copy, HERE, client-side via canvas. The quiz prize already wears its own baked mark (preMarked)
  // and goes out raw. A browser that refuses the canvas still gets the clean file (never blocked).
  function stampToBlob(src, cb) {                             // cb(blob) or cb(null) on any failure
    const host = ROOT_URL.replace(/^https?:\/\//, "").replace(/\/$/, "");
    const im = new Image();
    im.onload = () => {
      try {
        const nw = im.naturalWidth || im.width, nh = im.naturalHeight || im.height;
        // GRAB_MAX_PX caps the long edge; Math.min(1, ...) keeps a smaller image at its own size, so a
        // grab never enlarges what it was given (a 640 px tier stays 640, it does not stretch to 800).
        const k = Math.min(1, GRAB_MAX_PX / Math.max(nw, nh, 1));
        const cv = document.createElement("canvas");
        cv.width = Math.max(1, Math.round(nw * k)); cv.height = Math.max(1, Math.round(nh * k));
        const cx = cv.getContext("2d");
        cx.drawImage(im, 0, 0, cv.width, cv.height);
        // the burnt host mark is sized off the CANVAS width, so it keeps its proportion at any cap
        const fs = Math.max(13, Math.round(cv.width * 0.022)), pad = Math.round(fs * 0.9);
        cx.font = "600 " + fs + "px -apple-system,'Segoe UI',sans-serif";
        cx.textAlign = "right"; cx.textBaseline = "alphabetic";
        cx.fillStyle = "rgba(0,0,0,.34)"; cx.fillText(host, cv.width - pad + 1, cv.height - pad + 1);
        cx.fillStyle = "rgba(235,231,222,.66)"; cx.fillText(host, cv.width - pad, cv.height - pad);
        cv.toBlob((blob) => cb(blob || null), "image/jpeg", 0.92);
      } catch (e) { cb(null); }
    };
    im.onerror = () => cb(null);
    im.src = src;
  }
  // The share sheet MUST be opened inside the user gesture, but the stamp (image load + canvas +
  // toBlob) is async and would spend the yes-tap's activation before navigator.share runs. So the
  // file is rendered AHEAD — the moment the ceremony opens (renderGiftBlob), while the visitor reads
  // «did you like it?» — and the yes-tap shares the READY blob synchronously. An unrendered blob (a
  // very fast yes, or a failed stamp) falls to an on-the-spot render; the phone share may then be
  // refused after the async step, so saveBlob drops to the anchor and the file still leaves.
  let giftBlob = null, giftBlobFor = null;
  function renderGiftBlob(src, preMarked) {
    giftBlob = null; giftBlobFor = src;
    if (preMarked) {
      fetch(src).then((r) => (r && r.ok ? r.blob() : null)).then((blob) => {
        if (giftBlobFor === src) giftBlob = blob;
      }).catch(() => {});
    } else {
      stampToBlob(src, (blob) => { if (giftBlobFor === src) giftBlob = blob; });
    }
  }
  function giftDownload(src, name, preMarked, workId, onDone) {
    // a gift file actually leaves for the visitor's device — the beat rides BESIDE the download, its
    // kind from the closed pair: the quiz prize goes out preMarked, a right-click grab is signed here.
    // onDone (optional) fires once the file has left by ANY terminal road (the ready blob, the fetched
    // blob, the raw fallback, or a failed stamp): the slow path shows the EX-BUSY ring until then.
    pulse("gift_download", workId, { gift_kind: preMarked ? "quiz_prize" : "grab" });
    const fname = giftName(src, name);
    const done = () => { if (onDone) { try { onDone(); } catch (e) {} } };
    if (giftBlob && giftBlobFor === src) { saveBlob(giftBlob, fname); done(); return; }   // the pre-rendered file → synchronous share keeps the iOS activation
    if (preMarked) {
      fetch(src).then((r) => (r && r.ok ? r.blob() : null)).then((blob) => {
        if (blob) saveBlob(blob, fname); else rawDownload(src, name); done();
      }).catch(() => { rawDownload(src, name); done(); });
    } else {
      stampToBlob(src, (blob) => { if (blob) saveBlob(blob, fname); else rawDownload(src, name); done(); });
    }
  }
  // onYes (optional): called when the visitor says yes, BEFORE closeGift — used by the quiz-win path
  // to stamp the "gift" stage (EX-QUIZ-FLOW / INV-69) WITHOUT touching the shared ceremony behaviour.
  // N7-A11Y (INV-102, B1) — the restore is ORIGIN-CONDITIONED, uniform with the closer look (12): the
  // CALLER passes the opener only when the open is focus-origin (a keyboard grab passes the focused work,
  // a quiz-win passes the chip); a pointer / touch open passes nothing, so the ceremony forces NO focus and
  // the walk beneath is left as it was. openTrap treats a falsy opener as "restore none" (D4, 2026-07-21).
  function openGift(src, name, preMarked, onYes, workId, opener) {
    interrupt("gift");   // EX-PASS §10.3: the gift ceremony stands in front of the walk
    const T = (greetLang() || { t: {} }).t;
    // EX-PROTECT-RES (INV-56): the GRAB ceremony carries NO picture of its own. On a right-click the
    // work is already in view behind the card, so a thumb of the CLEAN source would only add a SECOND,
    // unguarded copy a right-click could save past the watermark — the leak this surface exists to
    // close. The QUIZ PRIZE is the one exception: it is a wallpaper the visitor won that is NOT
    // otherwise on screen, and it already wears a BAKED mark (`preMarked`), so revealing it in the card
    // leaks nothing. So the thumb is injected ONLY on the preMarked prize path; the grab card stays
    // imageless, its clean `src` a local handed to giftDownload only, stamped on its way out.
    const inner = giftCard.querySelector(".gift-inner");
    let thumb = giftCard.querySelector(".gift-thumb");
    if (preMarked) {
      if (!thumb) {
        thumb = document.createElement("img");
        thumb.className = "gift-thumb"; thumb.alt = "";
        inner.insertBefore(thumb, inner.firstChild);
      }
      thumb.src = src;                                   // the marked prize — the reveal, never a clean grab
      thumb.alt = workDesc(workId) || (((greetLang() || { t: {} }).t.a11y_gift) || A11Y_GIFT_EN);   // N7-A11Y (C8): the won wallpaper speaks
    } else if (thumb) {
      thumb.remove();                                    // a reused card returning to the grab path drops any prize image
    }
    giftCard.classList.toggle("prize", !!preMarked);     // the won wallpaper wants a dark stage; the grab wash lets the work show through (option C)
    renderGiftBlob(src, preMarked);                      // stamp the file AHEAD so a yes-tap can share it synchronously (iOS) — EX-PROTECT-RES
    // every line localizes through EX-I18N; the fallback is ENGLISH (source tongue), never Russian
    giftCard.querySelector(".gift-ask").textContent = T.gift_ask || "did you like it?";
    const yes = giftCard.querySelector(".gift-yes");
    yes.textContent = T.gift_yes || "it's yours :)";
    giftCard.querySelector(".gift-no").textContent = T.gift_no || "not now";
    giftCard.querySelector(".gift-line").textContent = enjoyLine();   // localized «enjoy · <host>»
    announceResult(enjoyLine());                        // N7-A11Y (INV-102 / F5): the gift result rides the SEPARATE result region
    // EX-PROTECT's own non-goal: the shop is a later movement. Until a print can actually be bought
    // the line stays HIDDEN — an empty content key hides it, and the agreed copy for the day it opens
    // is «buy a larger print» (his word 2026-07-22). No fallback literal, so an empty key shows nothing.
    const buyEl = giftCard.querySelector(".gift-buy");
    const buyText = (T.gift_buy || "").trim();
    buyEl.textContent = buyText;
    buyEl.hidden = !buyText;
    yes.onclick = () => {
      if (onYes) onYes();
      // the file is normally pre-rendered while the visitor read «did you like it?», so the yes shares
      // it synchronously and the ceremony closes at once (the iOS activation is kept). A very fast yes
      // or a failed pre-render leaves the file still to prepare: the yes then wears the EX-BUSY ring
      // (INV-48) and the ceremony holds until the file has left, so a slow grab is never a silent close.
      if (giftBlob && giftBlobFor === src) { giftDownload(src, name, preMarked, workId); closeGift(); return; }
      exBusyRing(yes, true); yes.setAttribute("aria-busy", "true"); yes.disabled = true;
      giftDownload(src, name, preMarked, workId, () => {
        exBusyRing(yes, false); yes.removeAttribute("aria-busy"); yes.disabled = false;
        closeGift();
      });
    };
    giftCard.dataset.work = workId != null ? String(workId) : "";   // the buy line's beat reads it
    giftCard.hidden = false; giftOpen = true;
    faceSync();                                        // the gift card is a face — arm the rest + guard (EX-CHROME)
    openTrap(giftCard, opener);                        // N7-A11Y (B1): focus into the ceremony, hold Tab inside, restore to the opener on close
    requestAnimationFrame(() => giftCard.classList.add("show"));       // EX-ARRIVE breath
  }
  function closeGift() {
    if (!giftOpen) return;
    closeTrap(giftCard);                               // N7-A11Y (B1): release the trap, restore focus to the opener
    giftCard.classList.remove("show");
    setTimeout(() => { giftCard.hidden = true; }, Math.round(350 * TEMPO));
    giftOpen = false;
    faceSync();                                        // the gift card left (EX-CHROME)
    recentreUnder();                                   // the last face leaves (EX-COMPOSE)
  }
  giftCard.querySelector(".gift-no").addEventListener("click", closeGift);
  // EX-PULSE buy_click: the pre-conversion reach — the buy line pressed means a print is wanted.
  // Today the line only measures (a shop destination is its own later movement), so the demand is
  // counted from day one; the beat carries the work like every commerce-adjacent beat.
  giftCard.querySelector(".gift-buy").addEventListener("click", () => {
    if (giftOpen) pulse("buy_click", giftCard.dataset.work || null);
  });
  giftCard.addEventListener("click", (ev) => { if (!ev.target.closest(".gift-inner")) closeGift(); });
  addEventListener("keydown", (ev) => { if (ev.key === "Escape" && giftOpen) closeGift(); });

/*!12-zoom-inspect-grab.js*/
  // ---- EX-ZOOM: pinch to inspect a picture (his word 2026-07-12: «люди хотят зумить картинки») ----
  // A two-finger pinch on ANY exhibition picture — a work on the walk, a door window, a polaroid —
  // opens that picture in its own zoom layer: the image scales under the pinch, a × returns, and the
  // page beneath stays EXACTLY as it was (a face, EX-CHROME — the walk is frozen, never scrolled).
  // The browser's own pinch stays refused document-wide (EX-PROTECT / INV-49), so the walk never
  // desyncs; the zoom is OUR controlled scale in its own overlay. Touch only — a desktop trackpad
  // pinch is a Ctrl-wheel, already refused (EX-PROTECT), and never opens the layer.
  const zoom = document.createElement("div");
  zoom.id = "ex-zoom";
  zoom.setAttribute("role", "dialog");
  zoom.setAttribute("aria-modal", "true");
  zoom.setAttribute("aria-label", ((greetLang() || { t: {} }).t.a11y_zoom) || A11Y_ZOOM_EN);   // N7-A11Y (C4/C5)
  zoom.hidden = true;
  // The zoom holds the minimum on screen (INV-77): only the picture and a single CLOSE in the free
  // TOP-LEFT corner. The ambient player retracts while the zoom stands (body.ex-zoom, like every covering
  // face), and the zoom carries no share of its own — a visitor shares a work from the walk itself.
  // The close aria-label localizes through EX-I18N like every other chrome string; the fallback is
  // ENGLISH (source tongue), never a hardcoded locale literal.
  const ZT = (greetLang() || { t: {} }).t;
  zoom.innerHTML = '<button type="button" class="exz-btn exz-close" aria-label="'
                 + (ZT.a11y_close || A11Y_CLOSE_EN) + '">&times;</button>'
                 + '<div class="exz-stage"><img class="exz-img" alt=""></div>';
  document.body.appendChild(zoom);
  let zoomOpen = false, zScale = 1, zPinch = 0, zStartS = 1;
  // The way OUT mirrors the way IN (INV-82): the picture flies UP from its place into the layer on open
  // and back DOWN to that place on close. The FLIP rides a WRAPPER (.exz-stage) so the pinch keeps the
  // .exz-img's own transform (INV-81 — the live two-touch distance stays the sole scale authority); the
  // stage carries the entry/exit position+scale, the img carries the pinch. zSrcEl is the tapped picture,
  // re-measured on close so a rotation under the zoom lands the shrink on its fresh place (INV-82).
  let zSrcEl = null, zLastEl = null, zDismiss = 0;      // zLastEl survives close so a Forward step reopens (INV-83)
  // INV-93 (2026-07-16, one margin for every pinch): the in-pinch mirrors the out-pinch — DISMISS_T
  // sits just under the picture's own resting size, so a release just below resting closes the layer
  // whatever gesture it belongs to, and a release at/above resting leaves the picture open at its size.
  const DISMISS_T = 0.92;                                 // (his 2026-07-23) 0.98 closed on a 2% squeeze — a pinch-OUT that began with a hair of inward drift tripped the dismiss; his word: firmer, an 8% squeeze, so the zoom holds and only a deliberate pinch-in closes it
  // once zoomed past 1×, a one-finger drag PANS the enlarged picture. zTx/zTy are the pan offset in
  // screen px; zPan* hold the gesture's start. The offset is bounded to the picture's visible overflow
  // so the image can never be dragged past its own edge.
  let zTx = 0, zTy = 0, zPanning = false, zPanX = 0, zPanY = 0, zPanTx = 0, zPanTy = 0;
  // INV-85 desktop pinch (ctrl+wheel / Safari gesture*): accumulate into the SAME 1×–4× scale the touch
  // pinch drives. zDesk holds the below-1× dismiss accumulator (starts at 1, a continued pinch-IN eases
  // it down; at/below DISMISS_T it commits). zDismissing latches from the moment history.back() is asked
  // until closeZoom runs, so a rapid open→dismiss race can never pop the walk's own history step twice.
  let zDesk = 1, zDismissing = false, zWheelIdle = 0;
  let zBelow = false;          // the desktop gesture stands below 1× (the crossing re-based already)
  const zImg = zoom.querySelector(".exz-img");
  const zStage = zoom.querySelector(".exz-stage");
  // The dismiss preview composes on the LIVE stage transform, latched on the preview's first frame —
  // so a preview arriving over a flight still in motion shrinks from what the eye sees, and the close
  // can read the same live matrix (INV-87 rule 4 extended: no one-frame return to full). One preview
  // for every pointer kind (INV-82/85: touch resistance = desktop resistance).
  let zPrevBase = null;
  function zPreview(ratio) {
    if (zPrevBase === null) {
      const live = getComputedStyle(zStage).transform;
      zPrevBase = (live && live !== "none") ? live + " " : "";
    }
    const shrink = 1 - (1 - Math.max(0.5, ratio)) * 0.45;   // resistance — eases toward its place
    zStage.style.transition = "none";
    zStage.style.transform = zPrevBase + "scale(" + shrink.toFixed(3) + ")";
  }
  function zPreviewEnd(ease) {                   // leave the preview: the stage returns to its rest
    if (zPrevBase === null) return;
    zPrevBase = null;
    zStage.style.transition = ease ? "" : "none";
    zStage.style.transform = "";
  }
  const zReduce = matchMedia("(prefers-reduced-motion: reduce)");
  const zDist = (t) => Math.hypot(t[0].clientX - t[1].clientX, t[0].clientY - t[1].clientY);
  // ---- EX-PICSTAT (INV-41): a SETTLED zoom lays one `inspect` per episode ------------------------
  // The closer look enters the registry as its own beat by the door-leak precedent [EX-TIME-READ]: a
  // release that leaves the picture open at/above its resting size (INV-93) lays one `inspect`,
  // debounced to the pinch coming to REST; a flick that dismisses below rest, or never opens, lays
  // nothing (the old frame-spam silence narrows to the un-settled flick, INV-1). ONE per zoom episode
  // — re-entering the zoom later is a new episode (the flag resets in openZoom), repeated releases
  // within one open zoom lay once. It carries the work (`pic`) and its `context` from the closed
  // ladder door·walk·room, read off the source surface the zoom opened from (the seam the zoom knows).
  let inspectTimer = 0, inspectLaid = false;
  function inspectContext(el) {
    if (!el || !el.closest) return null;
    const win = el.closest(".exd-window");
    if (win) return { context: "door", pic: win.dataset.id };     // a window on the front door
    const print = el.closest(".exs-print");
    if (print) return { context: "room", pic: print.dataset.id }; // a polaroid in the side room
    const side = el.closest("#ex-side");
    if (side) return { context: "room", pic: el.dataset.id };     // a lane image in the side room
    const frame = el.closest(".exh-frame");
    if (frame) return { context: "walk", pic: frame.dataset.id };  // a hung work on the walk
    return null;
  }
  function clearInspect() { if (inspectTimer) { clearTimeout(inspectTimer); inspectTimer = 0; } }
  function armInspect() {                                          // (re-)arm the settle debounce
    clearInspect();
    if (!zoomOpen || zDismissing || inspectLaid) return;
    inspectTimer = setTimeout(() => {
      inspectTimer = 0;
      if (!zoomOpen || zDismissing || inspectLaid) return;
      if (zScale < DISMISS_T) return;                             // must rest at/above resting size (INV-93)
      const meta = inspectContext(zSrcEl);
      if (!meta || !meta.context || !meta.pic) return;
      inspectLaid = true;                                         // once per episode
      pulse("inspect", meta.pic, { context: meta.context });      // pic + context; the arm rides via pulse (INV-91)
    }, 320);
  }
  // ---- EX-ZOOM the inspect flight (INV-82 rework, design 2026-07-15) — one motion class over the
  // five trigger types: entry IS the exit's mirror by construction. The stage owns the flight (always
  // animated, both ways on the SAME clock); the img owns only the pinch surplus; the crop is a clip
  // morph; the pin is measured transform-free. Every duration is read from CSS — no literal lives in
  // this JS (EX-MOTION owns the clock).
  function zDur(el) {                                    // ms of a computed transition-duration (first value)
    const d = (getComputedStyle(el).transitionDuration || "0s").split(",")[0].trim();
    return d.slice(-2) === "ms" ? parseFloat(d) : parseFloat(d) * 1000;
  }
  const zFlightDur = () => zDur(zStage);                 // the stage flight's own clock (--d-cross)
  const zFadeDur = () => zDur(zoom);                     // the backdrop crossfade clock (reduced / source-gone)
  let zTeardown = null;                                  // a pending exit teardown — a reopen cancels it (rule 7)
  function zCancelTeardown() {
    if (!zTeardown) return;
    clearTimeout(zTeardown.timer);
    if (zTeardown.onEnd) zStage.removeEventListener("transitionend", zTeardown.onEnd);
    zTeardown = null;
  }
  // the exit teardown fires on the flight's OWN transitionend (the true end of the motion) with a
  // computed-duration fallback, so an occluded/headless compositor that never paints the transition
  // still tears down — whichever lands first runs once (rule 7).
  function zArmTeardown(done) {
    zCancelTeardown();
    if (!done) return;
    const fire = () => { if (!zTeardown) return; zCancelTeardown(); done(); };
    const onEnd = (ev) => { if (ev.target === zStage && ev.propertyName === "transform") fire(); };
    zStage.addEventListener("transitionend", onEnd);
    zTeardown = { onEnd: onEnd, timer: setTimeout(fire, Math.round(zFlightDur() * 1.5) + 1) };
  }
  function zArmFade(done) {                              // reduced-motion / source-gone teardown, on the fade clock
    zCancelTeardown();
    if (!done) return;
    zTeardown = { onEnd: null, timer: setTimeout(() => { zCancelTeardown(); done(); }, Math.round(zFadeDur()) + 1) };
  }
  // the layer img's REST box, TRANSFORM-FREE (offset* ignore transforms) so a live pinch already on
  // .exz-img can never poison the pin (rule 3). The stage centres the img in the viewport. Not yet laid
  // out (a cold slot): derive from the natural fit into the CSS max-box (94vw/88vh) — the flight NEVER
  // degrades to an instant swap (rule 6).
  function zRestBox() {
    let w = zImg.offsetWidth, h = zImg.offsetHeight;
    if (!w || !h) {
      const nw = zImg.naturalWidth || 1, nh = zImg.naturalHeight || 1;
      const s = Math.min(innerWidth * 0.94 / nw, innerHeight * 0.88 / nh);
      w = nw * s; h = nh * s;
    }
    return { w: w, h: h, cx: innerWidth / 2, cy: innerHeight / 2 };
  }
  // frame-0 of the flight for a source picture: its cover-crop mapped onto the layer (rule 2). A square
  // window / polaroid shows a CENTRE cover-crop while the layer shows the whole contain image, so the
  // layer starts CLIPPED to that crop and the clip morphs open; a contain source (a hung work, a lane
  // image) crops nothing (visW=visH=1). One uniform scale + a centred translate carries the position,
  // so no aspect ever jumps between the source and the layer.
  function zCropFrame(rect, box, rot) {
    const dx = (rect.left + rect.width / 2) - box.cx;
    const dy = (rect.top + rect.height / 2) - box.cy;
    let visW = 1, visH = 1;
    const fit = zSrcEl ? getComputedStyle(zSrcEl).objectFit : "";
    if (fit === "cover" && rect.height > 0 && box.h > 0) {
      const boxA = rect.width / rect.height, imgA = box.w / box.h;
      if (boxA > imgA) visH = imgA / boxA; else visW = boxA / imgA;   // cover crops the longer relative side
    }
    const s = (rect.width / visW) / box.w;                            // the full image at the source's per-pixel scale
    const ix = ((1 - visW) / 2 * 100).toFixed(2), iy = ((1 - visH) / 2 * 100).toFixed(2);
    const r = rot ? " rotate(" + (rot * 180 / Math.PI).toFixed(2) + "deg)" : "";
    return { transform: "translate(" + dx.toFixed(1) + "px," + dy.toFixed(1) + "px)" + r + " scale(" + s.toFixed(4) + ")",
             clip: "inset(" + iy + "% " + ix + "% " + iy + "% " + ix + "%)",
             rot: rot || 0 };
  }
  // A resting polaroid TILTS (.exs-print rotate(--rot)), and getBoundingClientRect alone returns the
  // rotated print's inflated axis-aligned box — a translate+scale pin would un-tilt it in a snap at
  // frame-0 and land ~10% large. The pin carries the source's own rotation and its TRUE visual rect
  // (offset size × the print's own scale, centred on the box centre), so the tilt rides the flight
  // (INV-87): upright as it arrives, back into the tilt on the way home.
  function zSrcFrame(rect) {
    const pr = zSrcEl && zSrcEl.closest && zSrcEl.closest(".exs-print");
    const tr = pr ? getComputedStyle(pr).transform : "";
    const m = tr && tr !== "none" ? /matrix\(([^)]+)\)/.exec(tr) : null;
    if (!m) return { rect: rect, rot: 0 };
    const v = m[1].split(",").map(parseFloat);
    const rot = Math.atan2(v[1], v[0]);
    if (!rot) return { rect: rect, rot: 0 };
    const sc = Math.hypot(v[0], v[1]);                     // the print's own scale rides the same matrix
    const w = zSrcEl.offsetWidth * sc, h = zSrcEl.offsetHeight * sc;
    const cx = rect.left + rect.width / 2, cy = rect.top + rect.height / 2;
    return { rect: { left: cx - w / 2, top: cy - h / 2, width: w, height: h }, rot: rot };
  }
  // The single flight carrier. `back=false` opens (frame-0 crop → full contain), `back=true` closes
  // (full → the source's crop) — the SAME stage transform + img clip both directions on the SAME clock
  // (rule 8). Reduced motion / a vanished source: a short opacity crossfade in place, no flight
  // (rules 9 + 10). The pinch's own transform on .exz-img is never written here (INV-81).
  function zFlip(rect, back, done) {
    const box = zRestBox();
    if (!rect || zReduce.matches || !box.w || !box.h) {
      zStage.style.transition = "none";
      if (!back) { zStage.style.transform = ""; zImg.style.transition = "none"; zImg.style.clipPath = "inset(0)"; }
      if (done) { if (back) zArmFade(done); else requestAnimationFrame(done); }
      return;
    }
    const sf = zSrcFrame(rect);                     // the source's true visual rect + its own tilt (INV-87)
    const c = zCropFrame(sf.rect, box, sf.rot);
    if (back) {                                     // full → source crop: animate out, tear down on transitionend
      zStage.style.transition = ""; zImg.style.transition = "";
      requestAnimationFrame(() => { zStage.style.transform = c.transform; zImg.style.clipPath = c.clip; });
      zArmTeardown(done);
    } else {                                        // pin at the source crop, then release to fly in + morph open
      zStage.style.transition = "none"; zImg.style.transition = "none";
      zStage.style.transform = c.transform; zImg.style.clipPath = c.clip;
      void zStage.offsetWidth;                      // commit the pin before the release — a bare rAF pair
                                                    // can coalesce on WebKit and skip the entry flight
      requestAnimationFrame(() => {
        zStage.style.transition = ""; zImg.style.transition = "";
        // a rotated pin releases to the SAME function list (translate rotate scale) so the tilt
        // interpolates cleanly to upright; an unrotated pin keeps the plain rest form
        zStage.style.transform = c.rot ? "translate(0px,0px) rotate(0deg) scale(1)" : "";
        zImg.style.clipPath = "inset(0)";
        if (done) done();
      });
    }
  }
  function zClampPan() {                                 // keep the offset within the picture's overflow
    const ox = Math.max(0, (zImg.offsetWidth * zScale - innerWidth) / 2);
    const oy = Math.max(0, (zImg.offsetHeight * zScale - innerHeight) / 2);
    zTx = Math.max(-ox, Math.min(ox, zTx));
    zTy = Math.max(-oy, Math.min(oy, zTy));
  }
  function zApply() {
    zImg.style.transform = "translate(" + zTx.toFixed(1) + "px," + zTy.toFixed(1) + "px) scale(" + zScale.toFixed(3) + ")";
  }
  function openZoom(el, opts) {
    if (zoomOpen || !el) return;
    const src = el.currentSrc || el.getAttribute("src") || el.src;
    if (!src) return;
    interrupt("zoom");   // EX-PASS §10.3: the closer look stands in front of the walk
    inspectLaid = false; clearInspect();               // EX-PICSTAT: a fresh open is a new inspect episode
    zCancelTeardown();                                 // a reopen mid-teardown lands clean (rule 7)
    zSrcEl = el; zLastEl = el;                          // the tapped picture — the FLIP's place, re-measured on close
    const rect = el.getBoundingClientRect();           // its VISUAL rect (its own transform, e.g. a lifted print — rule 9)
    // N7-A11Y (INV-102, C7): the inspected image speaks the source picture's own description (the walk
    // frame / door window / polaroid all carry alt = the work's desc); the layer names itself by it too.
    zImg.src = src; zImg.alt = el.alt || "";
    zoom.setAttribute("aria-label", zImg.alt || (((greetLang() || { t: {} }).t.a11y_zoom) || A11Y_ZOOM_EN));
    zScale = 1; zTx = 0; zTy = 0; zPanning = false; zDismiss = 0; zDesk = 1; zBelow = false; zDismissing = false; zApply();
    zPrevBase = null;                                  // no preview rides into a fresh open
    if (zWheelIdle) { clearTimeout(zWheelIdle); zWheelIdle = 0; }
    zoom.classList.remove("desk");                     // a fresh open is finger-driven until a wheel/gesture says otherwise
    zStage.style.transition = "none"; zStage.style.transform = ""; zImg.style.clipPath = "inset(0)";
    zImg.style.willChange = "transform"; zStage.style.willChange = "transform";   // transient — cleared at teardown (never left on: compositor stall)
    zoom.hidden = false; zoomOpen = true;
    document.body.classList.add("ex-zoom");            // the player retracts too — the minimum on screen (INV-77)
    faceSync();                                        // the zoom is a face — freeze the page beneath (EX-CHROME)
    // N7-A11Y (INV-102, B1): the closer look takes keyboard focus; the origin rule is ORIGIN-CONDITIONED
    // — only a KEYBOARD open passes an opener (opts.opener, the focused work), so a pinch / ctrl-wheel /
    // trackpad open forces NO focus and the exact-restore invariant (INV-74/INV-83) is left untouched.
    openTrap(zoom, opts && opts.opener);
    if (!(opts && opts.lay === false)) pushFace({ face: "zoom" });   // one honest road out (INV-83), above any standing face
    requestAnimationFrame(() => {
      zoom.classList.add("show");                      // backdrop fades in
      const fly = () => { if (zoomOpen) { zImg.classList.remove("ex-skel"); zFlip(rect, false); } };  // picture flies in + the crop morphs open (INV-82)
      if (zImg.complete && zImg.naturalWidth) fly();                  // cached (the usual path) — fly at once
      else {                                                          // a cold slot: the shimmer holds the stage while it decodes (EX-SKEL/INV-48), never an instant swap (rule 6)
        zImg.classList.add("ex-skel");
        if (zImg.decode) zImg.decode().then(fly, fly);
        else fly();
      }
    });
  }
  // The single teardown, reached only through popstate (history.back): the ×, backdrop, Esc, and the
  // dismissing pinch all go through history.back so Back and they share one road (INV-83).
  function closeZoom() {
    if (!zoomOpen) return;
    clearInspect();                                    // EX-PICSTAT: a closing zoom lays no inspect
    zoomOpen = false; zDismissing = false; zDesk = 1; zBelow = false;
    const rect = (zSrcEl && document.body.contains(zSrcEl)) ? zSrcEl.getBoundingClientRect() : null;  // fresh VISUAL place (rotation/lift, INV-82 + rule 9)
    // Fold the current visual scale+pan into the flight's START, composed ONTO the live stage
    // transform — whatever the eye already sees (a dismiss preview's shrink, a flight still in
    // motion) — then reset the img: the exit is ONE composed motion home, never a snap to 1× and
    // never a one-frame return to full before the fly (rule 4). Both transforms originate at the
    // viewport centre (the img is flex-centred), so the composition is exact.
    const live = getComputedStyle(zStage).transform;
    // the img may still be EASING toward its model under the desk ease (.desk, --d-pinch) when a
    // fast pinch-shut commits — fold what the eye SEES (the computed matrix), never the model's
    // target, or the img snaps to 1× the instant .desk drops (read BEFORE the class is removed)
    const imLive = getComputedStyle(zImg).transform;
    const fold = (imLive && imLive !== "none")
      ? imLive
      : "translate(" + zTx.toFixed(1) + "px," + zTy.toFixed(1) + "px) scale(" + zScale.toFixed(4) + ")";
    zoom.classList.remove("desk");                     // the img resets instantly (no eased double-motion)
    zPrevBase = null;                                  // the preview is riding the fold now
    if (zWheelIdle) { clearTimeout(zWheelIdle); zWheelIdle = 0; }
    zStage.style.transition = "none";
    zStage.style.transform = (live && live !== "none" ? live + " " : "") + fold;
    zScale = 1; zTx = 0; zTy = 0; zPanning = false; zDismiss = 0; zApply();   // the img → identity, in place
    void zStage.offsetWidth;                           // commit the fold before the flight starts (no jump)
    zoom.classList.remove("show");                     // backdrop fades; the player returns to its rail at once
    document.body.classList.remove("ex-zoom");
    zFlip(rect, true, () => {                           // picture flies back DOWN to its place, then teardown
      zoom.hidden = true; zImg.removeAttribute("src");
      zStage.style.transition = "none"; zStage.style.transform = ""; zImg.style.clipPath = "";
      zImg.style.willChange = ""; zStage.style.willChange = "";     // release the transient compositor hint
      zSrcEl = null;
    });
    closeTrap(zoom);                                   // N7-A11Y (B1): release the trap; restore focus only if a keyboard open recorded an opener (after the composed-exit fold, so the flight's structure stands as INV-87 pins it)
    faceSync();                                        // the page beneath returns untouched (EX-COMPOSE)
  }
  // a pinch over the OPEN zoom scales the picture; our JS owns it, so the browser never viewport-zooms.
  // The handlers listen at the DOCUMENT, gated on zoomOpen (INV-81): touch events keep targeting the
  // element where the gesture STARTED — for the pinch that just opened the layer that is the picture
  // beneath, never #ex-zoom itself — and they bubble to the document, so one set of handlers serves
  // both the opening gesture (the direct scale, no arming tap) and any later gesture on the layer.
  addEventListener("touchstart", (e) => {
    if (!zoomOpen) return;
    if (e.touches.length === 2) {                       // two fingers → pinch-scale (pan yields)
      zPinch = zDist(e.touches); zStartS = zScale; zPanning = false;
      clearInspect();                                   // a resumed pinch is not at rest (EX-PICSTAT)
    } else if (e.touches.length === 1 && zScale > 1
               && e.target.closest && e.target.closest(".exz-img")) {
      zPanning = true;                                  // one finger on the enlarged picture → pan
      zPanX = e.touches[0].clientX; zPanY = e.touches[0].clientY;
      zPanTx = zTx; zPanTy = zTy;
    }
  }, { passive: true });
  addEventListener("touchmove", (e) => {
    if (!zoomOpen) return;
    if (e.touches.length === 2 && zPinch) {
      e.preventDefault();                              // our scale, never the browser's
      let raw = zStartS * (zDist(e.touches) / zPinch);
      if (raw < 1 && zScale <= 1.001) {   // at/into 1×, a continued pinch-IN previews the dismiss — one continuous gesture crosses from zoom-out into dismiss (rule 5)
        if (zStartS !== 1) {              // a pinch that began zoomed RE-BASES at the 1× crossing (INV-82):
          zPinch = zDist(e.touches);      // the dismiss ratio reads from HERE, so the squeeze is the same
          zStartS = 1;                    // whatever the prior zoom and a fast crossing frame never commits
          raw = 1;
        }
        zDismiss = raw;
        zPreview(raw);
      } else {
        // the recovery EASES back (never a snap): the latched base may be a mid-flight matrix —
        // an instant reset here was the one-frame jump the composed close exists to kill (INV-87)
        if (zDismiss) { zDismiss = 0; zPreviewEnd(true); }
        zScale = Math.max(1, Math.min(4, raw));
        zClampPan();                                   // a smaller scale shrinks the pannable overflow
        zApply();
      }
    } else if (e.touches.length === 1 && zPanning) {
      e.preventDefault();                              // drag the enlarged picture, bounded to its edges
      zTx = zPanTx + (e.touches[0].clientX - zPanX);
      zTy = zPanTy + (e.touches[0].clientY - zPanY);
      zClampPan();
      zApply();
    }
  }, { passive: false });
  addEventListener("touchend", (e) => {
    if (!zoomOpen) return;
    const pinchBroke = zPinch && e.touches.length < 2;   // the two-finger pinch just broke (first finger up)
    if (e.touches.length < 2) zPinch = 0;
    if (e.touches.length === 0) zPanning = false;
    if (zDismiss) {                                    // in the dismiss preview (INV-82)
      // The verdict LATCHES the moment the pinch breaks — a STAGGERED two-finger release still commits,
      // where the old code cancelled on the first touchend before the last finger lifted (rules 1 + 5).
      if (pinchBroke) {
        if (zDismiss < DISMISS_T && !zDismissing) { zDismissing = true; history.back(); return; }   // commit → close through history (INV-83)
        zDismiss = 0; zPreviewEnd(true);                                                   // above threshold → ease back to 1×
      }
      return;
    }
    if (zScale <= 1.03 && e.touches.length === 0) { zScale = 1; zTx = 0; zTy = 0; zApply(); }   // a near-1 release settles flat + centred
    // EX-PICSTAT: a release that leaves the picture open at/above resting arms the settle debounce
    if (zoomOpen && !zDismissing && e.touches.length === 0) armInspect();
  }, { passive: true });
  // A gesture the system TAKES AWAY (an incoming call, a notification pulled over the page, a palm the
  // browser rejects) fires touchcancel and never touchend, so pinch, pan and dismiss state would stand
  // mid-gesture under the open layer and the next touch would resume a gesture the visitor never made.
  // It ends the gesture like a lift that commits nothing: the dismiss preview eases back, pinch and pan
  // clear, the picture keeps the size the visitor reached, and the settle re-arms (INV-82).
  addEventListener("touchcancel", () => {
    if (!zoomOpen) return;
    zPinch = 0;
    zPanning = false;
    if (zDismiss) { zDismiss = 0; zPreviewEnd(true); }
    if (!zDismissing) armInspect();
  }, { passive: true });
  // Every way out is the same road (INV-83): the ×, a backdrop tap, and Esc all step history BACK, and
  // the popstate handler runs the one closeZoom — so the browser's own Back button closes the zoom too.
  const zoomBack = () => { if (zoomOpen) history.back(); };
  zoom.querySelector(".exz-close").addEventListener("click", zoomBack);
  zoom.addEventListener("click", (e) => { if (e.target === zoom) zoomBack(); });   // tap the backdrop
  addEventListener("keydown", (e) => { if (e.key === "Escape" && zoomOpen) zoomBack(); });

  // ---- N7-A11Y (INV-102, B2/B3): the keyboard opens the closer look and the grab from a FOCUSED work ----
  // A work HANGS in four places — a walk photograph (.exh-frame), a door window (.exd-window), a
  // polaroid on the table (.exs-print) and a lane picture in the series room (a direct <img> child of
  // #exs-stage; a polaroid's own inner <img> is NOT one, it belongs to its print). One selector set
  // names all four, and every road below — the keyboard, the right-click, the long press — resolves
  // through it, so no surface carries a private list of what counts as a picture.
  const HANG_SEL = ".exh-frame, .exd-window, .exs-print, #exs-stage > img";
  function hangPlace(el) {                              // the hanging place under an element, or null
    return (el && el.closest) ? el.closest(HANG_SEL) : null;
  }
  function hangPic(place) {                             // the picture a hanging place shows
    if (!place) return null;
    return place.tagName === "IMG" ? place : place.querySelector("img");
  }
  // The gift ceremony is offered against a work the visitor has CHOSEN and walked to. A door window
  // shows the facade's spread before that choice exists, so it carries no hung-work identity to
  // ceremony over and always answers with the gracious line instead (INV-49, F1) — the one exception,
  // stated here once rather than re-derived at each road.
  function hangGiftId(place) {
    if (!place || (place.classList && place.classList.contains("exd-window"))) return "";
    return (place.dataset && place.dataset.id) || "";
  }
  // With a hanging place holding focus, `z` looks closer (openZoom, recording the PLACE as the opener so
  // close restores focus to it — B1), and `y` hands over the gift through the SAME imageless clean-source
  // openGift path onGrab routes a right-click through, so no new grab road is built (INV-49) — not `g`,
  // which both NVDA and JAWS already consume as browse-mode next-graphic before the page ever sees it.
  // Enter keeps its walk-only meaning: on a polaroid it lifts (16's own handler) and on a door window it
  // enters.
  addEventListener("keydown", (e) => {
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    // A standing LAYER's own keys own the input. atDoor and sideOpen are deliberately NOT here: the
    // door and the series room are not layers over a work, they HANG works, and a face passes `z` and
    // `g` to the work its visitor has focused (INV-67, input ownership).
    if (zoomOpen || quizOpen || giftOpen || busy) return;
    const place = hangPlace(e.target);
    if (!place) return;                                // a key only opens from a focused hanging place
    const img = hangPic(place);
    if (!img) return;
    if (e.key === "z" || e.key === "Z") {              // look closer, wherever the work hangs
      e.preventDefault();
      openZoom(img, { opener: place });
    } else if (e.key === "y" || e.key === "Y") {       // take the gift — the keyboard grab (not `g`: the
                                                        // screen readers' own next-graphic key, never reaches the page)
      e.preventDefault();
      const gid = hangGiftId(place);
      if (gid) {
        openGift(img.currentSrc || img.getAttribute("src") || img.src, undefined, undefined, undefined,
                 gid, place);                           // OFFER, never dump — reuse the clean-source path; keyboard origin → restore to the place (INV-49, D4)
      } else {
        toast(enjoyLine());                             // a door window keeps the gracious line (F1)
      }
    } else if (e.key === "Enter" && place.classList.contains("exh-frame")) {
      e.preventDefault();                              // the walk's own Enter, unchanged
      openZoom(img, { opener: place });
    }
  }, { passive: false });
  // INV-81 — the trigger reaches every picture, the small ones included: a polaroid never fits two
  // fingertips, so the match reads the element under EACH touch point (the event's own target first —
  // one deterministic pick when two pictures sit under the two fingers), and the WHOLE print
  // (.exs-print, paper frame included) is the polaroid's hit area, resolving to the photograph inside.
  const ZOOM_SEL = ".exh-frame img.work, .exd-window img, #ex-side img, .exs-print";
  function zoomPick(e) {
    let hit = e.target && e.target.closest && e.target.closest(ZOOM_SEL);
    for (let i = 0; !hit && i < e.touches.length; i++) {
      const el = document.elementFromPoint(e.touches[i].clientX, e.touches[i].clientY);
      hit = el && el.closest && el.closest(ZOOM_SEL);
    }
    if (!hit) return null;
    return hit.tagName === "IMG" ? hit : hit.querySelector("img");
  }
  addEventListener("touchstart", (e) => {
    if (e.touches.length !== 2 || zoomOpen) return;   // one zoom at a time; opens over ANY face
    const t = zoomPick(e);
    if (!t) return;
    openZoom(t);                                       // pass the picture itself — its rect is the FLIP's place (INV-82)
    // seed the pinch so the SAME gesture keeps scaling the just-opened layer — its later touchmoves
    // bubble to the document handlers above; no second pinch, no arming tap (INV-81)
    if (zoomOpen) { zPinch = zDist(e.touches); zStartS = 1; zPanning = false; }
  }, { passive: true });

  // INV-85 target resolution (derived from EX-HANG): a trackpad pinch does not move the cursor, so the
  // picture UNDER the pointer wins (the same ZOOM_SEL selector set); with the pointer over no picture the
  // single work then in the viewport is the target (one work per viewport, EX-HANG); else nothing opens.
  function zoomTargetAt(x, y) {
    const el = document.elementFromPoint(x, y);
    let hit = el && el.closest && el.closest(ZOOM_SEL);
    if (hit) return hit.tagName === "IMG" ? hit : hit.querySelector("img");
    if (restingEl && restingEl.querySelector) {          // no picture under the pointer → the viewport's one work
      const img = restingEl.querySelector("img.work");
      if (img) return img;
    }
    return null;
  }
  // INV-85: a ctrl+wheel `deltaY` accumulates into the very 1×–4× scale the touch pinch drives —
  // deltaY<0 (pinch OUT) grows it, deltaY>0 (pinch IN) shrinks it; a rising scale OPENS #ex-zoom on the
  // resolved picture, a pinch-IN past the mirror margin (DISMISS_T) DISMISSES through the one history step.
  const ZOOM_WHEEL_STEP = 0.0025;                        // scale change per |deltaY| unit of a ctrl+wheel / pinch
  function pinchWheel(e) {
    const dScale = -e.deltaY * ZOOM_WHEEL_STEP;          // OUT (deltaY<0) → +, IN (deltaY>0) → −
    zoom.classList.add("desk");                          // the wheel surplus eases on the img (rule 8) — finger pinch stays instant
    if (!zoomOpen) {
      if (dScale <= 0) return;                           // a pinch-IN with nothing open opens nothing (INV-81 mirror)
      const t = zoomTargetAt(e.clientX, e.clientY);
      if (!t) return;                                    // no picture resolves → nothing opens (browser zoom stays refused)
      openZoom(t);                                       // lays the one history step (INV-83) — the dismiss road
      if (!zoomOpen) return;
      zDesk = 1; zScale = Math.min(4, 1 + dScale); zApply();
      armInspect();                                      // EX-PICSTAT: the wheel-pinch settles too
      return;
    }
    const ns = zScale + dScale;
    if (ns < 1) {                                        // at/into 1× a continued pinch-IN previews the dismiss (INV-82)
      zScale = 1; zTx = 0; zTy = 0; zApply();
      // the crossing EVENT re-bases at 1× — its below-1 residue never commits by itself, the same
      // law the touch path holds (INV-82); travel below 1× counts only from the crossing on
      zDesk = zBelow ? zDesk + (ns - 1) : 1;
      zBelow = true;
      if (zWheelIdle) { clearTimeout(zWheelIdle); zWheelIdle = 0; }
      if (zDesk <= DISMISS_T && !zDismissing) { zDismissing = true; zDesk = 1; history.back(); return; }  // commit through the one road (INV-83)
      zPreview(zDesk);                                   // the desktop pinch-shut previews with the touch resistance (INV-82/85)
      // Blink's ctrl-wheel stream carries no end event — a short idle eases an uncommitted preview back
      zWheelIdle = setTimeout(() => {
        zWheelIdle = 0;
        if (zoomOpen && !zDismissing) { zDesk = 1; zBelow = false; zPreviewEnd(true); }
      }, 140);
      return;
    }
    zDesk = 1; zBelow = false;
    zPreviewEnd(true);                                   // recovered above 1× — the preview eases off
    zScale = Math.min(4, ns); zClampPan(); zApply();
    armInspect();                                        // EX-PICSTAT: the wheel-pinch coming to rest
  }
  // INV-76 desktop pan: once enlarged past 1×, a mouse drag inside the layer pans the picture — the
  // direct equivalent of the one-finger touch pan, under the same edge-bounded clamp (zClampPan).
  zStage.addEventListener("mousedown", (e) => {
    if (!zoomOpen || zScale <= 1) return;
    e.preventDefault();
    zPanning = true; zPanX = e.clientX; zPanY = e.clientY; zPanTx = zTx; zPanTy = zTy;
  });
  addEventListener("mousemove", (e) => {
    if (!zoomOpen || !zPanning) return;
    zTx = zPanTx + (e.clientX - zPanX); zTy = zPanTy + (e.clientY - zPanY);
    zClampPan(); zApply();
  });
  addEventListener("mouseup", () => { if (zPanning) zPanning = false; });

  // EX-PROTECT (INV-49; 2026-07-13 uniformity fix): the grab guard now matches on the door window's
  // picture too (.exd-window img), not only a hung work — the door face was the one surface a guest
  // could still freely save, on FIRST entry, before the gift ceremony's identity even exists (his find:
  // the room refuses a grab, the door facade did not). A door window carries no HUNG WORK identity
  // (no .exh-frame, no frame id) to offer the desktop gift ceremony against, so its refusal never
  // invents one — it always answers with the SAME gracious toast the room gives a drag/touch grab,
  // never a new behaviour or new copy.
  let lpTouchFired = false;                               // A1: a just-fired touch long-press swallows a follow-up contextmenu (Android)
  // the PICTURE at each of the four hanging places — the grab's own hit set. It stays a picture-level
  // list (never the whole place) so a grab on a frame's breathing margin or on room chrome is still
  // left alone; the place it hangs in is resolved from the picture through hangPlace.
  const GRAB_SEL = ".exh-frame img.work, .exd-window img, .exs-print img, #exs-stage > img";
  function onGrab(ev) {                                    // ONE delegated listener per kind, O(1)
    const img = ev.target.closest && ev.target.closest(GRAB_SEL);
    if (!img) return;                                      // only a picture that hangs somewhere; chrome is left alone
    ev.preventDefault();                                   // the raw browser save menu / drag ghost never fires
    if (lpTouchFired) { lpTouchFired = false; return; }    // the touch long-press already answered this grab (A1) — a contextmenu that trails it is swallowed
    const gid = hangGiftId(hangPlace(img));                // "" for a door window (INV-49 uniformity)
    // EX-PULSE/INV-79: the guest REACHES to take a hung work — the earlier moment gift_download cannot
    // see (that lays only when a file leaves), a demand signal. The grab KIND is a closed ladder:
    // `drag` · `menu` (desktop right-click → the gift ceremony) · `touch` (a coarse-pointer press).
    const grab = ev.type === "dragstart" ? "drag"
      : matchMedia("(pointer: coarse)").matches ? "touch" : "menu";
    pulse("copy_attempt", gid || null, { grab: grab });
    // DESKTOP right-click on a work that carries an identity → the gift ceremony; a door window (no
    // `gid`), TOUCH, or a drag → just the gracious line, no download (his word 2026-07-08: on the phone
    // the picture is earned through the quiz, not grabbed; a door window has no hung-work identity to
    // ceremony over either)
    if (gid && ev.type === "contextmenu" && !matchMedia("(pointer: coarse)").matches) {
      openGift(img.currentSrc || img.getAttribute("src") || img.src, undefined, undefined, undefined,
               gid);                                    // OFFER, never dump — gift_kind=grab (EX-PULSE)
    } else {
      toast(enjoyLine());
    }
  }
  stage.addEventListener("contextmenu", onGrab);
  stage.addEventListener("dragstart", onGrab);
  door.addEventListener("contextmenu", onGrab);           // the door's own facade (INV-49 uniformity) —
  door.addEventListener("dragstart", onGrab);             //   #ex-door lives OUTSIDE #ex-stage (EX-DOOR-2a)
  // EX-PROTECT (INV-49): the enlarged view is a face that shows a picture — the largest one — so it
  // refuses a raw save like every other. #ex-zoom lives on document.body (outside #ex-stage), so it
  // binds its own guard: a desktop right-click / drag on the magnified copy meets the SAME gracious
  // line the hung work gives, never the browser's save menu. The iOS long-press sheet is handled by
  // the CSS `-webkit-touch-callout:none` on .exz-img (the touch road), and the long-press ceremony
  // detector already stands down while a zoom is open (pointerdown returns on zoomOpen).
  zoom.addEventListener("contextmenu", (ev) => { ev.preventDefault(); toast(enjoyLine()); });
  zoom.addEventListener("dragstart", (ev) => { ev.preventDefault(); });
  // the series room binds the SAME onGrab where it is built (16-renderhang-series.js) — #ex-side is
  // appended to document.body, outside both #ex-stage and #ex-door, so its works were reachable by no
  // grab road at all until it did.
  // ---- EX-PROTECT (A1, INV-49): a touch LONG-PRESS on a hung work opens the SAME gift ceremony --------
  // iOS fires no reliable `contextmenu`, so the finger's grab rides a real press-and-hold detector here,
  // beside onGrab and the pinch it must coexist with. It ARMS on `pointerdown`, FIRES after a hold of
  // ~500ms `[default]` with no drift past a small px threshold `[default]`, and reuses the imageless
  // clean-source openGift path onGrab routes a right-click through — never a new grab road, never a clean
  // copy in the card (INV-49). It CANCELS on a lift, on a drift past the threshold (so the walk swipe in
  // 15-motion wins), and on a second finger (so the inspect pinch wins). A door window (no hung-work
  // identity) keeps the gracious toast, never the ceremony (F1). The ~500ms / px values are Alexander's
  // device-feel tune, like the 1.7.5 swipe constants — a touch input threshold, never tempo-scaled.
  const LP_MS = 320;                                      // [default] the hold that arms the grab (his 2026-07-23: 500→400→320, a touch wanted the gift a further ~20% sooner)
  const LP_PX = 10;                                       // [default] the drift that cancels it (a swipe)
  let lpTimer = 0, lpX = 0, lpY = 0, lpImg = null, lpPtrs = 0;
  function lpCancel() { if (lpTimer) { clearTimeout(lpTimer); lpTimer = 0; } lpImg = null; }
  addEventListener("pointerdown", (e) => {
    if (e.pointerType === "mouse") return;                // the pointer's own grab road is the right-click (onGrab)
    lpPtrs++;
    if (lpPtrs > 1) { lpCancel(); return; }               // a second finger → the inspect pinch owns the touch
    // a covering LAYER stands — its own gestures own the input. sideOpen is deliberately absent: the
    // series room HANGS works (a polaroid, a lane picture) and a press must reach them (INV-67). The
    // GRAB_SEL match below is the gate instead — a press on the bare table or on the room's own chrome
    // resolves to no picture and still does nothing.
    if (zoomOpen || giftOpen || quizOpen) return;
    const img = e.target && e.target.closest && e.target.closest(GRAB_SEL);
    if (!img) return;                                     // only a picture that hangs somewhere
    lpImg = img; lpX = e.clientX; lpY = e.clientY;
    lpTimer = setTimeout(() => {
      lpTimer = 0;
      if (!lpImg || lpPtrs !== 1 || zoomOpen || giftOpen || quizOpen) return;
      const gid = hangGiftId(hangPlace(lpImg));           // "" for a door window (INV-49 uniformity)
      pulse("copy_attempt", gid || null, { grab: "touch" });   // the demand beat, the touch kind (EX-PULSE)
      lpTouchFired = true;                                // swallow any follow-up contextmenu (Android) in onGrab
      setTimeout(() => { lpTouchFired = false; }, 700);   // the trailing contextmenu, if any, lands right after; then clear the swallow window
      if (gid) {
        openGift(lpImg.currentSrc || lpImg.getAttribute("src") || lpImg.src, undefined, undefined,
                 undefined, gid);                         // OFFER — the imageless clean-source path; touch origin → no forced focus (INV-49, D4)
      } else {
        toast(enjoyLine());                               // a door window keeps the gracious line (F1)
      }
      lpImg = null;
    }, LP_MS);
  }, { passive: true });
  addEventListener("pointermove", (e) => {
    if (!lpTimer) return;
    if (Math.hypot(e.clientX - lpX, e.clientY - lpY) > LP_PX) lpCancel();   // a drift → a swipe, cancel the arm
  }, { passive: true });
  function lpUp(e) {
    if (e.pointerType === "mouse") return;
    if (lpPtrs > 0) lpPtrs--;
    lpCancel();                                           // a lift cancels a still-pending arm (a tap, never a grab)
  }
  addEventListener("pointerup", lpUp, { passive: true });
  addEventListener("pointercancel", lpUp, { passive: true });
  // EX-PROTECT + EX-CHROME: the immersive walk refuses browser zoom across the WHOLE surface, not
  // only over a work. A browser zoom scales the visual viewport out from under the JS scroll animator
  // and the fixed chrome — the measured centering drifts and the fixed controls float, so the walk
  // desyncs (his phone field-find). Pinch: Safari fires gesture events; Blink zooms via a two-finger
  // drag — both refused document-wide here. Double-tap zoom: blocked by `touch-action:manipulation`
  // (CSS) since iOS IGNORES the viewport's user-scalable=no. On Blink the viewport meta also pins
  // scale to 1. Silent — a pinch is exploratory, not a save, so no gift line, only no zoom.
  // INV-85: Safari fires gesturestart/gesturechange/gestureend for a trackpad pinch (Blink does not —
  // its equivalent is the ctrl+wheel above). We preventDefault ALWAYS so the browser never viewport-
  // zooms (EX-PROTECT), and on a NON-touch device drive the SAME inspect layer from `ev.scale`: the
  // gesture's live scale (× the scale at gesturestart) accumulates into the 1×–4× clamp, and a pinch-IN
  // past the dismiss threshold closes through the one history step. (Headless Blink dispatches no
  // gesture* events, so this path is verified only on a real Mac — named in the test's real-device set.)
  let gStart = 1;
  function onGestureStart(ev) {
    ev.preventDefault();
    if (TOUCHY) return;                                  // touch Safari uses the touch pinch path above
    gStart = zoomOpen ? zScale : 1;
    if (!zoomOpen) {
      const x = ev.clientX || innerWidth / 2, y = ev.clientY || innerHeight / 2;
      const t = zoomTargetAt(x, y);
      if (t) { openZoom(t); gStart = 1; zDesk = 1; }
    }
  }
  function onGestureChange(ev) {
    ev.preventDefault();
    if (TOUCHY || !zoomOpen) return;
    zoom.classList.add("desk");                          // Safari trackpad surplus eases on the img (rule 8)
    let target = gStart * (ev.scale || 1);
    if (target < 1) {                                    // pinch-IN past 1× → preview / commit the dismiss (INV-82)
      zScale = 1; zTx = 0; zTy = 0; zApply();
      if (!zBelow) {                                     // first frame below 1× re-bases at the crossing
        gStart = 1 / (ev.scale || 1);                    // — a fast crossing frame reads 1, never commits
        target = 1;                                      // by itself (INV-82, the touch path's own law)
        zBelow = true;
      }
      zDesk = target;
      if (zDesk <= DISMISS_T && !zDismissing) { zDismissing = true; zDesk = 1; history.back(); return; }
      zPreview(zDesk);                                   // Safari's trackpad pinch-shut previews too (INV-82/85)
      return;
    }
    zDesk = 1; zBelow = false; zPreviewEnd(true); zScale = Math.min(4, target); zClampPan(); zApply();
  }
  function onGestureEnd(ev) {
    ev.preventDefault();
    if (TOUCHY || !zoomOpen) return;
    if (zDesk < 1 && !zDismissing) { zDesk = 1; zBelow = false; zPreviewEnd(true); }   // an uncommitted release eases back (gestureend)
    if (zScale <= 1.03) { zScale = 1; zTx = 0; zTy = 0; zApply(); }    // near-1 release settles flat
    if (zoomOpen && !zDismissing) armInspect();          // EX-PICSTAT: the trackpad pinch coming to rest
  }
  document.addEventListener("gesturestart", onGestureStart, { passive: false });
  document.addEventListener("gesturechange", onGestureChange, { passive: false });
  document.addEventListener("gestureend", onGestureEnd, { passive: false });
  // EX-PROTECT belt: the SAME three gesture events also carry a flat preventDefault-only guard, so on
  // ANY device — touch Safari included, where the INV-85 handlers early-return on TOUCHY — the browser's
  // own viewport pinch-zoom is refused document-wide. The INV-85 handlers layer the app-zoom on top; this
  // pair keeps the raw browser gesture from ever scaling the viewport (the walk desyncs if it does).
  function onPinch(ev) { ev.preventDefault(); }
  ["gesturestart", "gesturechange", "gestureend"].forEach((g) =>
    document.addEventListener(g, onPinch, { passive: false }));
  document.addEventListener("touchmove", (e) => {
    if (e.touches.length > 1) e.preventDefault();          // a two-finger drag = a Blink pinch
  }, { passive: false });

/*!13-quiz-card.js*/
  // ---- EX-QUIZ (INV-60/64/65/66): the 4-option chip + card + edge round-trip ----------------
  // A subtle chip advertises a work's question (placement is a config knob, INV-28). Tapping it
  // opens a modal card: the public prompt, a 2×2 grid of option buttons, and the response zone.
  // ONE tap LOCKS — the tapped option is POSTed to /api/quiz; the edge compares it to the ONE
  // PRIVATE correct option (INV-64), never a served byte. A hit shows quiz_win → gift ceremony.
  // A miss shows quiz_wrong → card fades out (~1.5s). The card TINTS to the work's live tone and
  // RTL-mirrors with the active locale. ONE question per walk-show is chosen deterministically
  // from the eligible set (INV-66); a cooldown suppresses the chip for QUIZ_COOLDOWN_H hours.
  // Every chrome string localizes through EX-I18N with ENGLISH source-tongue fallbacks.
  function quizLabel() {
    const T = (greetLang() || { t: {} }).t;
    // EX-QUIZ-COPY (INV-100): ONE sentence, the owner's own (2026-07-28) — it names the question
    // the chip asks and the gift a right answer gives. The quiz_chip_copy split (place/place_prize)
    // RETIRED with it on the same word: the traffic cannot settle a two-arm test, so the wording is
    // adopted rather than dealt (SPEC.md carries the dated tombstone). The words ride the ordinary
    // localized set (`quiz_ask`, EX-I18N) with the English source tongue standing as the fallback.
    return T.quiz_ask || "where was this shot? · win a wallpaper";
  }
  function quizChipHTML(id) {
    // a soft, slow one-time glint runs across the chip as it appears (EX-QUIZ-GLINT) — the
    // .ex-quiz-glint span is a pure-CSS sweep, born with the chip, plays once
    return `<button type="button" class="ex-quiz-chip" data-quiz="${id}">${quizLabel()}` +
      `<span class="ex-quiz-glint" aria-hidden="true"></span></button>`;
  }
  const PRIZE_DL = EX.quiz_prize_name || (DL_BASE + "-wallpaper.jpg");  // prize download name: config override → site-slug default (INV-28)

  const quizCard = document.createElement("div");
  quizCard.id = "ex-quiz-card";
  quizCard.setAttribute("role", "dialog");
  quizCard.setAttribute("aria-modal", "true");
  quizCard.setAttribute("aria-label", ((greetLang() || { t: {} }).t.a11y_quiz) || A11Y_QUIZ_EN);   // N7-A11Y (C4/C5)
  quizCard.hidden = true;
  // EX-QUIZ-PICK (INV-64): 4 option buttons replace the free-text form.
  quizCard.innerHTML =
    '<div class="quiz-inner">' +
      '<div class="quiz-prompt"></div>' +
      '<div class="quiz-opts"></div>' +
      '<div class="quiz-out"></div>' +
    '</div>';
  document.body.appendChild(quizCard);

  let quizOpen = false;
  let quizWorkId = null;
  let quizOpener = null;       // the chip the card opened from — passed to the prize gift so its restore
                              // reaches the chip (the gift's origin-conditioned restore, D4)
  let quizCloseT = null;      // the wrong-answer auto-close timer (a miss lingers ~1s, then closes)
  let quizWaitT = null;       // the in-flight grace timer → the quiet «one more moment» reassurance

  // EX-QUIZ-REPLY (INV-65): the async reply slot names three states. PENDING is the dimmed-lock the
  // moment a tap fires; if the round-trip is still owed past a house grace, the SAME quiet reassurance
  // the edge failure shows lands in the reply slot (the reused quiz_submit key, English fallback). The
  // grace rides the one clock like every other wait (×TEMPO) and follows the config-knob pattern.
  const QUIZ_WAIT_GRACE = secs(EX.quiz_wait_grace, 0.6);

  function quizCardOpen(id) {
    const w = byId[id];
    if (!w || !w.quiz) return;
    interrupt("quiz");   // EX-PASS §10.3: the question card stands in front of the walk
    const opener = document.activeElement;             // N7-A11Y (INV-102, B1): the card returns focus to its opener (the chip)
    quizOpener = opener;                               // remembered so the prize gift restores to the chip too (D4)
    quizWorkId = id;

    // RESET ON REOPEN: every open starts clean — cleared feedback, fresh buttons, no lingering state.
    clearTimeout(quizCloseT); quizCloseT = null;
    clearTimeout(quizWaitT); quizWaitT = null;
    quizCard.classList.remove("gone", "quiz-inflight");
    // RTL mirror (INV-65): the card leans to the active locale's direction, like the door + finale do.
    try { const L = (greetLang() || { t: {} }).t; quizCard.setAttribute("dir", L.dir === "rtl" ? "rtl" : "ltr"); } catch (e) {}
    const out = quizCard.querySelector(".quiz-out");
    out.className = "quiz-out"; out.textContent = "";

    // VISUAL TINT: the card's accent is THIS work's own live tone — tints to the picture, never fixed.
    try {
      const a = liveAccent(w.dom);
      quizCard.style.setProperty("--accent", `rgb(${a.join(",")})`);
      quizCard.style.setProperty("--accent-2", `rgb(${a.map((v) => Math.round(v * 0.86)).join(",")})`);
    } catch (e) {}

    // answered-memory: widened shape — {answered,right,prize} is new; old {prize:...} also reads answered.
    let stored = null;
    try { stored = JSON.parse(localStorage.getItem(QUIZ_LS(id)) || "null"); } catch (e) {}
    if (stored && typeof stored === "object" && (stored.answered === true || stored.prize)) {
      // already answered — straight to the gift ceremony when there is a prize
      if (stored.prize) { openGift("/" + stored.prize, PRIZE_DL, true, undefined, id, opener); return; }
      return;  // answered wrong previously — nothing more to show
    }

    // build the four option buttons from the public options (the tapped value is sent to the edge)
    quizCard.querySelector(".quiz-prompt").textContent = w.quiz.prompt || "";
    const optsEl = quizCard.querySelector(".quiz-opts");
    optsEl.innerHTML = "";
    const options = Array.isArray(w.quiz.options) ? w.quiz.options : [];
    options.forEach((city) => {
      const b = document.createElement("button");
      b.type = "button"; b.className = "quiz-opt";
      b.dataset.val = city;
      b.setAttribute("aria-label", city);
      b.innerHTML = "<bdi>" + city.replace(/[<>&"]/g, (c) => ({"<":"&lt;",">":"&gt;","&":"&amp;",'"':"&quot;"})[c]) + "</bdi>";
      b.addEventListener("click", () => { answer(city); });
      optsEl.appendChild(b);
    });

    // stamp the cooldown: this is "a show that asked" — suppress the chip for QUIZ_COOLDOWN_H hours
    try { localStorage.setItem(QUIZ_SHOWN_KEY, String(Date.now())); } catch (e) {}
    // EX-QUIZ-FLOW (INV-69): the card opening advances the stage to "opened"
    quizStageUp("opened");
    quizCard.hidden = false;
    quizOpen = true;
    faceSync();                                        // the card is a face — arm the rest + guard (EX-CHROME)
    openTrap(quizCard, opener);                        // N7-A11Y (B1): focus into the card, hold Tab inside, restore to the opener
    requestAnimationFrame(() => { quizCard.classList.add("show"); });
  }

  function quizCardClose() {
    if (!quizOpen) return;
    closeTrap(quizCard);                               // N7-A11Y (B1): release the trap, restore focus to the opener
    clearTimeout(quizCloseT); quizCloseT = null;
    clearTimeout(quizWaitT); quizWaitT = null;      // a mid-flight close cancels the pending reassurance
    quizCard.classList.remove("show", "quiz-inflight");
    setTimeout(() => { quizCard.hidden = true; }, Math.round(350 * TEMPO));
    quizOpen = false;
    quizWorkId = null;
    faceSync();                                        // the card left (EX-CHROME)
    recentreUnder();                                   // the last face leaves (EX-COMPOSE);
  }                                                    // a win hand-off re-checks at the gift's own close

  // EX-QUIZ-REPLY (INV-65): one tap decides — the city button fires answer(city).
  // After a tap all buttons are disabled and the unchosen dim. Win: quiz_win line → gift ceremony.
  // Miss: quiz_wrong line → card fades out on var(--d-*). A server verdict (win/miss) LOCKS the work;
  // a reach failure that never got a verdict re-opens the choice (reachFailed) and burns nothing.
  function answer(city) {
    const id = quizWorkId;
    if (!id) return;
    const w = byId[id];
    if (!w || !w.quiz) return;

    // the question is being answered — the chip's job is done. Drop the «question?» chip from the
    // plaque now and clear this show's choice so it never reappears; the answered-memory written
    // below keeps it gone in future walks too (EX-QUIZ-ONCE: once answered, the chip goes).
    quizChosenId = null;
    document.querySelectorAll(".ex-quiz-chip").forEach((el) => el.remove());

    // LOCK all buttons immediately — one tap, no re-pick
    const opts = Array.from(quizCard.querySelectorAll(".quiz-opt"));
    opts.forEach((b) => {
      b.disabled = true;
      if (b.dataset.val !== city) b.classList.add("dim");
    });

    const out = quizCard.querySelector(".quiz-out");
    out.className = "quiz-out"; out.textContent = "";

    // PENDING (EX-QUIZ-REPLY): the dimmed-lock is the named in-flight state from this instant; past a
    // house grace a still-owed round-trip shows the quiet «one more moment» reassurance the spec names
    // for a slow or failing edge (the reused quiz_submit key, English fallback here — never a scold).
    quizCard.classList.add("quiz-inflight");
    clearTimeout(quizWaitT);
    quizWaitT = setTimeout(() => {
      quizWaitT = null;
      const T = (greetLang() || { t: {} }).t;
      out.className = "quiz-out quiz-wait";
      out.textContent = T.quiz_submit || "one more moment";
      requestAnimationFrame(() => out.classList.add("show"));
    }, Math.round(QUIZ_WAIT_GRACE * 1000 * TEMPO));
    function settled() { clearTimeout(quizWaitT); quizWaitT = null; quizCard.classList.remove("quiz-inflight"); }

    function missAndFade() {
      settled();
      // mark the tapped button as wrong
      opts.forEach((b) => { if (b.dataset.val === city) b.classList.add("wrong"); });
      const T = (greetLang() || { t: {} }).t;
      out.className = "quiz-out quiz-miss";
      out.textContent = T.quiz_wrong || "thanks for guessing. another question waits for you further on.";
      announceResult(out.textContent);                 // N7-A11Y (INV-102 / F5): the verdict rides the SEPARATE result region
      requestAnimationFrame(() => out.classList.add("show"));
      // remember the miss so the work is excluded from eligible in future walks (INV-65 / INV-66)
      try { localStorage.setItem(QUIZ_LS(id), JSON.stringify({ answered: true, right: false })); } catch (e) {}
      // EX-QUIZ-FLOW (INV-69): the tap was judged — advance the stage to "lost"
      quizStageUp("lost");
      // fade the card out after the visitor reads the line, then call quizCardClose
      clearTimeout(quizCloseT);
      quizCloseT = setTimeout(() => {
        quizCard.classList.add("gone");   // CSS: opacity:0 + translateY(6px) on var(--d-*)
        quizCloseT = setTimeout(() => { quizCard.classList.remove("gone"); quizCardClose(); },
          Math.round(650 * TEMPO));
      }, Math.round(1500 * TEMPO));
    }

    // EX-QUIZ-REPLY (INV-65/INV-138): an edge that never returned a verdict — a non-ok status
    // (429/503/down) or a network drop — holds the same calm pending face and RE-OPENS the choice.
    // A connectivity blip never reads as a wrong answer and never burns the question: no answered-memory
    // is written and no stage advances, so the work still asks on a later walk. Only a verdict the
    // server actually returned (win or genuine miss) locks the work.
    function reachFailed() {
      settled();
      const T = (greetLang() || { t: {} }).t;
      out.className = "quiz-out quiz-wait";
      out.textContent = T.quiz_submit || "one more moment";
      requestAnimationFrame(() => out.classList.add("show"));
      opts.forEach((b) => { b.disabled = false; b.classList.remove("dim", "wrong"); });
    }

    fetch("/api/quiz", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id: String(id), answer: city }),
    }).then((r) => { if (!r || !r.ok) throw new Error("unreachable"); return r.json(); }).then((data) => {
      if (data && data.ok) {
        settled();                                     // ARRIVED: the pending reassurance is replaced
        // WIN: mark correct, show quiz_win line, close quiz, open the gift ceremony
        opts.forEach((b) => { if (b.dataset.val === city) b.classList.add("correct"); });
        const T = (greetLang() || { t: {} }).t;
        out.className = "quiz-out quiz-win";
        out.textContent = T.quiz_win || "you have the eye.";
        announceResult(out.textContent);               // N7-A11Y (INV-102 / F5): the verdict rides the SEPARATE result region
        requestAnimationFrame(() => out.classList.add("show"));
        // remember the win so this work never re-asks (INV-65 / INV-66 answered-memory)
        try { localStorage.setItem(QUIZ_LS(id), JSON.stringify({ answered: true, right: true, prize: data.prize })); } catch (e) {}
        // EX-QUIZ-FLOW (INV-69): the tap was judged correct — advance the stage to "won"
        quizStageUp("won");
        clearTimeout(quizCloseT);
        quizCloseT = setTimeout(() => {
          quizCardClose();
          // EX-QUIZ-FLOW (INV-69): pass onYes so the gift stage stamps ONLY on the quiz prize's yes
          openGift("/" + data.prize, PRIZE_DL, true,
                   () => { quizStageUp("gift"); }, id, quizOpener);   // gift_kind=quiz_prize, the work (EX-PULSE); restore to the chip (D4)
        }, Math.round(700 * TEMPO));
      } else {
        missAndFade();
      }
    }).catch(() => { reachFailed(); });  // a non-ok edge or a network drop never reached a verdict — a calm face, no scold, no burned question
  }

  // the chip tap opens the card (delegated on cap)
  cap.addEventListener("click", (ev) => {
    const b = ev.target.closest && ev.target.closest(".ex-quiz-chip");
    if (!b) return;
    const id = b.dataset.quiz;
    if (quizOpen && quizWorkId === id) return;            // already open for this work — do nothing
    if (quizOpen) quizCardClose();                        // close any open card first (one at a time)
    setTimeout(() => quizCardOpen(id), quizOpen ? Math.round(350 * TEMPO) : 0);
  });
  addEventListener("keydown", (ev) => { if (ev.key === "Escape" && quizOpen) quizCardClose(); });
  quizCard.addEventListener("click", (ev) => {
    if (!ev.target.closest(".quiz-inner")) quizCardClose();
  });

/*!14-walk-render.js*/
  function frameHTML(id, n) {
    const w = byId[id];
    // EX-LADDER (INV-63): the ladder itself lives in one place (ladderAttr); the walk hands its
    // own box — CSS max-width:88vw. The base `src` stays the untouched fallback.
    const ladder = ladderAttr(w, ladderSizes("walk"));
    // N7-A11Y (INV-102, C1/C3): the frame img speaks the work's own description (never alt=""), and the
    // frame names itself a photograph within the walk (role + roledescription + the same accessible name).
    const desc = escAttr(workDesc(w.id));
    const photoWord = escAttr(((greetLang() || { t: {} }).t.a11y_photo) || A11Y_PHOTO_EN);
    return (
      `<section class="exh-frame" data-id="${w.id}" data-n="${n}" tabindex="0"` +
        ` role="group" aria-roledescription="${photoWord}" aria-label="${desc}"` +
        // N7-A11Y (INV-102, B2/B3): the frame ANNOUNCES the two keys it answers — `z` looks closer, `y` opens the gift
        ` aria-keyshortcuts="z y">` +
        `<img class="work" loading="lazy" src="${w.img}"${ladder} alt="${desc}">` +
      "</section>"
    );
  }

  function appendFrames(slice, startN) {
    document.getElementById("exh-fin")?.remove();
    const html = slice.map((id, i) => frameHTML(id, startN + i)).join("");
    stage.insertAdjacentHTML("beforeend", html);
    stage.querySelectorAll(".exh-frame:not(.observed)").forEach((f) => {
      f.classList.add("observed"); io.observe(f);
    });
    // the walk's closing screen: onward while the budget lasts, the door ALWAYS (INV-29/30/31).
    // Its copy speaks the visitor's language like the door does (his word 2026-07-06: the exit
    // is «выход», localized — never «к двери»); built-ins only carry a missing cache.
    const spent = spentUnfolds() >= MAXU || shown >= order.length;
    const FL = greetLang();
    const FT = FL ? FL.t : {};
    const moreLabel = (FT.more || MORE_EN).replace("{n}", String(UNFOLD));
    // EX-ABOUT (INV-103): the closing screen is the one place the exhibition already offers a
    // choice of where to go, so the door to the about page stands here — in the VISITOR's own
    // tongue when that tongue has a page, else at the fallback page every bundle bakes first.
    // The baked signature below carries no about link, so this screen shows exactly one door.
    const AB = data.about;
    const aboutWord = ((FT.about || "") + "").trim();
    const aboutHref = !AB ? "" :
      (FL && AB.langs.indexOf(FL.code) >= 0 && FL.code !== AB.fallback)
        ? "/about/" + FL.code : "/about";
    const fin = document.createElement("section");
    fin.className = "exh-fin"; fin.id = "exh-fin";
    if (FL) {
      fin.setAttribute("lang", FL.code);
      fin.setAttribute("dir", FT.dir === "rtl" ? "rtl" : "ltr");
    }
    fin.innerHTML =
      `<div class="q">${spent ? (FT.q_spent || "дальше — новый выбор") : (FT.q_more || "идти дальше?")}</div>` +
      '<div class="row">' +
      (spent ? "" : `<button type="button" class="more" id="ex-unfold">${moreLabel} ↓</button>`) +
      (aboutHref && aboutWord ? `<a class="about" id="ex-about" href="${aboutHref}">${aboutWord}</a>` : "") +
      (doorAvailable ? `<button type="button" class="back" id="ex-return">${FT.exit || "выход"}</button>` : "") +
      "</div>" +
      // the archive signs its rooms (EX-COPY) — one baked line; missing field renders nothing
      (data.copyright ? `<div class="exh-sign">${data.copyright}</div>` : "");
    stage.appendChild(fin);
    io.observe(fin);                                    // watch the finale too, so the caption clears on it
    requestAnimationFrame(() => { fin.classList.add("show"); }); // EX-ARRIVE: breath in from opacity:0
    fin.querySelector("#ex-unfold")?.addEventListener("click", () => {
      if (spentUnfolds() >= MAXU || shown >= order.length) return;   // the unfolding ENDS (INV-30)
      tlog("unfold");
      pulse("walk_unfold");
      const s = shown;
      shown = Math.min(order.length, shown + UNFOLD, CAP);
      appendFrames(order.slice(s, shown), s + 1);
      save();
      tellStory();                                     // the voice extends over the grown set (ST2)
    });
    fin.querySelector("#ex-return")?.addEventListener("click", doorReturn);
    counter.querySelector(".tot").textContent = String(shown).padStart(2, "0");
  }

/*!15-motion.js*/
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
  // Split by CAPABILITY, not by a single either/or flag. The finger pager and the wheel/key pager
  // are installed by what the device CAN do, independently — a hybrid that both has a touchscreen
  // AND hovers (a Surface, a touch Windows laptop) gets BOTH, so the walk paginates the same way on
  // every platform. The old `hover:none` flag conflated "touch" with "no hover", so a touch-with-
  // hover device fell into the wheel/key branch alone and its finger swipe free-scrolled the walk
  // with no snap (the fly-through EX-GLIDE exists to kill, reintroduced for that device class).
  // HAS_TOUCH: any coarse pointer or a real touch count → install the finger pager (it blocks native
  // scroll and docks one frame per swipe). HAS_WHEEL: a fine pointer or hover → install the wheel/key
  // pager; a pure-touch device (neither) skips it (no wheel fires there anyway). Keys are always on.
  const HAS_TOUCH = (navigator.maxTouchPoints || 0) > 0 || matchMedia("(any-pointer: coarse)").matches;
  const HAS_WHEEL = matchMedia("(any-pointer: fine)").matches || matchMedia("(hover: hover)").matches || !HAS_TOUCH;
  // TOUCHY is still read by the closer-look module (12) to sit out the desktop-Safari pinch handlers on a
  // touch device — kept here as its long-standing home so that shared reference resolves. It carries the
  // ORIGINAL hover:none meaning unchanged; the pager split above is what moved to the capability model.
  const TOUCHY = matchMedia("(hover: none)").matches;
  // the walk's own reachable surface, for the suite: which pagers this device installed. A hybrid
  // (touch AND hover) MUST read both true — the parity the suite pins (INV-39).
  try {
    window.@@NS_UPPER@@Motion = { hasTouch: HAS_TOUCH, hasWheel: HAS_WHEEL, touchPager: false, wheelPager: false };
  } catch (e) {}
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
  // The transition curve: a cubic with s(0)=0, s(1)=1, s'(0)=m, s'(1)=0, entered at speed m (the
  // entering speed over this glide's own distance/duration). m=0 is exactly smoothstep, so a glide
  // from a resting walk is unchanged; a glide REPLACING one in flight enters at the speed that one
  // had, so the walk never stops dead mid-frame. m is clamped to the band where the cubic stays
  // monotonic and cannot overshoot the frame (INV-39). Why, in full: SPEC EX-GLIDE + INV-84.
  const GLIDE_M_MAX = 2;
  const GLIDE_MIN_MS = 16;                             // shorter than one frame — just land
  function glideCurve(m) {
    const s = Math.max(0, Math.min(GLIDE_M_MAX, +m || 0));
    return {
      m: s,
      at: (t) => (((s - 2) * t + (3 - 2 * s)) * t + s) * t,   // s(t)
      dat: (t) => (3 * (s - 2) * t + 2 * (3 - 2 * s)) * t + s, // s'(t)
    };
  }
  // The pure half of a glide — DOM-free and clock-free, so the suite replays recorded trackpad
  // envelopes through it in node (test_glide_speed), as it does the step verdict. `dist` px still
  // to travel · `want` the duration this force asks for a WHOLE frame · `span` the frame travel the
  // running glide set out on (0 starts one) · `carry` its speed px/ms (0 = rest) · `leftMs` what is
  // left of its deadline (Infinity = none). A re-time may only bring the landing nearer.
  function glidePlan(a) {
    const span = a.span || Math.abs(a.dist) || 1;
    let dur = a.want * Math.min(1, Math.abs(a.dist) / span);
    if (dur > a.leftMs) dur = a.leftMs;
    if (!(dur > GLIDE_MIN_MS)) return { dur: 0, m: 0, span: span };
    const m = (a.carry * a.dist > 0)
      ? Math.max(0, Math.min(GLIDE_M_MAX, a.carry * dur / a.dist)) : 0;
    return { dur: dur, m: m, span: span };
  }
  let glideDist = 0, glideDurMs = 0, glideT0 = 0, glideCurveNow = null, glideEndAt = 0, glideSpan = 0;
  function glideSpeedNow(now) {                        // px per ms, signed, of the glide in flight
    if (!gliding || !glideCurveNow || !(glideDurMs > 0)) return 0;
    const p = Math.max(0, Math.min(1, (now - glideT0) / glideDurMs));
    return glideDist * glideCurveNow.dat(p) / glideDurMs;
  }
  // mode: "" fresh from a resting walk · "chain" a second gesture re-targeting to the next frame ·
  // "retime" the same goal at a new speed. Chain and re-time both carry the running speed.
  function glideToFrame(to, velocity, mode) {
    const now = performance.now();
    const carry = (mode === "chain" || mode === "retime") && gliding ? glideSpeedNow(now) : 0;
    const deadline = (mode === "retime" && gliding) ? glideEndAt : Infinity;
    const spanRef = (mode === "retime" && gliding) ? glideSpan : 0;
    glideCancel();
    const from = scrollY;
    const d = to - from;
    if (Math.abs(d) < 2) { glideGoal = null; return; } // already centered — nothing to move
    glideGoal = to;
    // INV-84: the gesture's velocity sets this single glide's duration (calm ~520ms → sharp ~260ms).
    // A re-time asks that duration for the whole frame, then takes the share still left to travel.
    const plan = glidePlan({ dist: d, want: glideDur(velocity), span: spanRef,
                             carry: carry, leftMs: deadline - now });
    const dur = plan.dur;
    if (!dur) { scrollTo(0, to); glideGoal = null; return; }          // inside one frame — just land
    const cv = glideCurve(plan.m);
    const t0 = now;
    glideDist = d; glideDurMs = dur; glideT0 = t0; glideCurveNow = cv; glideEndAt = t0 + dur;
    glideSpan = plan.span;
    gliding = true;
    const step = (nw) => {
      // EVERY standing face stops the flight, by the one predicate the rest of this fragment uses.
      // The three-flag list this replaced left a glide writing scrollY under an open closer-look or
      // question card, where the snap-back guard is already holding the place — the two then fought
      // for the position frame by frame.
      if (faceStands()) { glideCancel(); glideGoal = null; passAbortNow("a face stands"); return; }
      const p = Math.min(1, (nw - t0) / dur);
      scrollTo(0, from + d * cv.at(p));                // the animator OWNS the position
      if (p < 1) glideRaf = requestAnimationFrame(step);
      else { glideCancel(); glideGoal = null; passLandNow(); }  // landed centered — no tail, no drift
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
    // WHERE THE STEP COUNTS FROM. The walk's own glide names its goal, and a step taken while it
    // flies chains from that goal — that road is unchanged. A RENDERER holding the command is the
    // second road to the same law (EX-GLIDE, SPEC.md:1329-1331): a new input mid-transition chains
    // to the next frame and never re-rounds backward. While the renderer holds it the walk's own
    // scroll has not moved — the passage is the motion, and the placement comes at the handoff — so
    // `scrollY` still names the DEPARTING frame and a second gesture re-rounds onto it and
    // re-declares the very step already in flight (U10 §3, four rows red: the visitor's second
    // swipe bought a shortened crossing and no progress). The running transaction's own destination
    // is where the walk is headed, so that is what this step counts from.
    let base = scrollY;
    if (gliding && glideGoal != null) base = glideGoal;
    else if (passRunning() && passNav && passNav.kind === "step" && passNav.to) {
      const held = passNav.to.id
        ? stage.querySelector('.exh-frame[data-id="' + String(passNav.to.id).replace(/"/g, "") + '"]')
        : document.getElementById("exh-fin");
      if (held && document.body.contains(held)) base = frameCenter(held);
    }
    const cur = nearestStop(stops, base);
    const k = Math.min(stops.length - 1, Math.max(0, cur + dir));
    if (k === cur) noteStuckStep(); else stuckBurst = [];   // EX-FRICTION: a clamped no-move step vs a real advance
    glideTargetEl = els[k];                              // the destination SECTION — a mid-glide rotation docks HERE (INV-86)
    // EX-PASS: the transition is DECLARED here. This is the one place holding both works, the
    // direction and the force, and it is the place that calls the landing — so a picture layer can
    // be handed a whole command and hand control back on the arriving work. A clamped no-move step
    // declares nothing: there is no work to arrive at.
    const cmd = (k === cur) ? null : declare({
      fromEl: els[cur], toEl: els[k], dir: dir,
      span: Math.abs(stops[k] - stops[cur]),
      kind: "step", cause: "step", velocity: velocity,
    });
    if (cmd) { passObserverSync(); passOpen(); }        // a changed landProgress takes effect between
    if (cmd && passVisualTakes(cmd) && passOffer(cmd)) return;   // transitions; the layer's file is asked for once
    glideToFrame(stops[k], velocity, "chain");         // a second gesture keeps the speed it had
    if (cmd && !gliding) passLandNow();                // already centred — the command lands within the frame
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
    // EX-PASS §10.3: a turn arriving while a renderer has TAKEN the command resizes the running
    // transaction in place — the host's own instrument keeps its progress — rather than superseding
    // it the way a fresh declare would. The free-glide path below is unaffected and unchanged.
    if (passRunning()) { reframe({ w: innerWidth, h: innerHeight }); return; }
    if (gliding && glideTargetEl && document.body.contains(glideTargetEl)) {
      turnTargetEl = glideTargetEl;                    // remember the destination across coalesced turn events
      glideCancel(); glideGoal = null;                 // stop writing OLD-viewport positions at once
    }
    clearTimeout(turnT);
    turnT = setTimeout(() => {                          // after the reflow — measure the fresh viewport
      if (document.documentElement.classList.contains("ex-walk")) {
        const stops = frameStops();
        if (stops.length) {
          let y, docked = null;
          if (turnTargetEl && document.body.contains(turnTargetEl)) { docked = turnTargetEl; y = frameCenter(docked); restingEl = docked; }
          else if (restingEl && document.body.contains(restingEl)) { docked = restingEl; y = frameCenter(docked); }
          else { const i = nearestStop(stops, scrollY); y = stops[i]; docked = stage.querySelectorAll(".exh-frame, .exh-fin")[i] || null; }
          passJump(docked, "rotate");                  // EX-PASS: a turn lands on a work, so it carries a command too
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
    const i = nearestStop(stops, scrollY);
    const under = restingEl || stage.querySelectorAll(".exh-frame, .exh-fin")[i] || null;
    passJump(under, "recentre");                       // EX-PASS: the re-centre under a leaving face lands on a work
    scrollTo(0, restingEl ? frameCenter(restingEl) : stops[i]);
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
  if (HAS_WHEEL) {
    try { window.@@NS_UPPER@@Motion.wheelPager = true; } catch (e) {}
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
        if (gliding && glideGoal != null) glideToFrame(glideGoal, wheelPeak, "retime");
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
  if (HAS_TOUCH) {
    try { window.@@NS_UPPER@@Motion.touchPager = true; } catch (e) {}
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

/*!16-renderhang-series.js*/
  function renderHang() {
    tlog("hang");
    recomputeQuizChoice();                               // EX-QUIZ-ONCE (INV-66): pick ONE eligible work
    document.documentElement.classList.add("ex-walk");   // the walk's face (geometry in CSS)
    stage.innerHTML = "";
    appendFrames(order.slice(0, shown), 1);
    passJump(stage.querySelector(".exh-frame"), "hang");  // EX-PASS: a fresh hang stands at its first work
    scrollTo(0, 0);
    if (faceStands()) guardHold = 0;                     // the walk builds under the ceremony's veil — hold its top (EX-CHROME)
    tellStory();                                         // the voice, if the story is on (set-guarded)
  }

  // ---- EX-SERIES (INV-46): the side room — theme and variations, a look ASIDE --------
  // A FACE over the walk: opening lays ONE history step; the page locks beneath (the
  // threshold's own law); chip, Esc and Back all land the guest on the exact frame left.
  const side = document.createElement("div");
  side.id = "ex-side";
  side.setAttribute("role", "dialog");                                                          // N7-A11Y (B-role): the room is a modal layer, one kind with the other three
  side.setAttribute("aria-modal", "true");
  side.setAttribute("aria-label", ((greetLang() || { t: {} }).t.a11y_room) || A11Y_ROOM_EN);   // N7-A11Y (C4/C5)
  side.hidden = true;
  side.innerHTML = '<button type="button" class="exs-back"></button>' +
                   '<div class="exs-stage" id="exs-stage"></div>';
  document.body.appendChild(side);
  // EX-PROTECT (INV-49): the room's own works refuse a grab through the SAME delegated onGrab the walk
  // and the door use. #ex-side is appended to document.body — outside both #ex-stage and #ex-door — so
  // until this binding a polaroid and a lane picture were reachable by no grab road at all. The binding
  // lives here, at the element's construction site, because 12 runs before this file exists.
  side.addEventListener("contextmenu", onGrab);
  side.addEventListener("dragstart", onGrab);
  let sideOpen = false;
  let sideOpener = null;            // N7-A11Y (INV-102, B1): the element that opened the room — focus returns here on close
  let laneTouchOff = null;          // the CURRENT dress's own lane touchstart handler (INV-88) —
                                     // removed at the top of every dressSide so it never piles up
                                     // across reopens of the reused #exs-stage
  function openSide(idx, laystep) {
    const S = SERIES[idx];
    if (!S || sideOpen || busy) return;
    interrupt("series");   // EX-PASS §10.3: the series room stands in front of the walk
    sideOpener = document.activeElement;               // N7-A11Y (B1): remember the opener (the series chip) before the crossing
    sideOpen = true;
    faceSync();                                        // the room is a face — arm the rest + guard (EX-CHROME)
    // the room opens THROUGH THE SAME BLACK the door crosses (his 09:53 word: «такой же
    // транзишен как с двери в комнату») — a shortened breath of the entry ceremony; the
    // ceremony's own cancel law carries it (any arriving face wins, no stranded veil)
    busy = true;
    faceSync();                                        // the crossing holds the lock (EX-CHROME)
    const g = ++cerGen;
    const ok = () => g === cerGen;
    veil.hidden = false;
    veil.style.transitionDuration = (0.33 * TEMPO) + "s";
    requestAnimationFrame(() => veil.classList.add("on"));
    cerAfter(0.4, () => { if (!ok()) return;           // the room dresses under the black
      dressSide(S, idx, laystep);
      veil.style.transitionDuration = (0.53 * TEMPO) + "s";
      veil.classList.remove("on");                     // …and is revealed in one breath
    });
    cerAfter(0.95, () => { if (!ok()) return;
      veil.hidden = true;
      busy = false;
      faceSync();                                      // the room stands revealed; sideOpen keeps the lock (EX-CHROME)
    });
  }
  // EX-LOAD-2 (INV-72): the room's pictures ride the walk's and the door's own in-flight ladder —
  // the SAME core, knobs, classes and timings, never a second copy of them. A plate PER picture
  // (a whole room may be in flight at once), and no ex: marks: the room stays off the walk's loading
  // counter, exactly as the door does. The caller hands the host the plate is laid in and, in the
  // lane, the grid column the picture stands in; a picture already in hand shows at once, no plate.
  function seriesArm(img, w, host, col) {
    if (!img || !w || !host) return;
    if (img.complete) { img.dataset.ladder = "done"; return; }   // cached ⇒ shows at once, no plate
    const p = document.createElement("div");
    p.className = "exs-plate";
    p.innerHTML = '<i class="ex-bar" aria-hidden="true"></i>';
    if (w.w && w.h) p.style.setProperty("--ar", w.w / w.h);      // the lane's caps read the work's shape
    if (col) { p.style.gridColumn = col; p.style.gridRow = "1"; }  // the picture's own cell
    ladderFlight(img, w, host, p, [], () => img.isConnected, false);
    // the core lays every plate at the host's head; in the LANE the host is the whole row, so the
    // plate is moved to its own picture's side — the two then read as one pair, and the lane's rest
    // can pass from the plate to the photograph the moment it lands (the CSS pair rule)
    if (col) host.insertBefore(p, img);
  }
  function dressSide(S, idx, laystep) {
    const st = side.querySelector("#exs-stage");
    st.className = "exs-stage " + S.variant;           // the series' own character picks the face
    st.innerHTML = "";
    if (laneTouchOff) {               // the PRIOR dress's own listener, if any, dies here — #exs-stage
      st.removeEventListener("touchstart", laneTouchOff);   // is reused, innerHTML="" does not remove
      laneTouchOff = null;                                  // a listener bound to the container itself
    }
    const dressGen = cerGen;          // THIS dress's own generation (INV-88) — a rebuilt/closed
    const decodes = [];               // room before the pictures decode is never touched again
    let laneTaken = false;            // the visitor already took the lane in hand — the decode
                                       // re-affirm below must never yank it back out from under them
    let laneCol = 0;                  // the lane is ONE grid row; each picture takes the next column
    S.members.forEach((id, i) => {
      const w = byId[id];
      if (!w) return;
      if (S.variant === "lane") {
        const col = String(++laneCol);                   // the picture's own column — its plate shares it
        const im = new Image();
        ladderOn(im, w, ladderSizes("lane"));            // EX-LADDER (INV-63): the lane's box is CSS max-width:64vw
        im.src = w.img;
        im.alt = workDesc(w.id);                         // N7-A11Y (INV-102, C6): the lane photograph speaks
        im.dataset.id = w.id;                            // EX-PICSTAT: the room look reads its pic
        im.tabIndex = 0;                                 // N7-A11Y (INV-102, B4): the lane photograph is keyboard-reachable (the lane scrolls by arrow key — the side-level handler below)
        im.setAttribute("aria-keyshortcuts", "z y");     // N7-A11Y (INV-102, B2/B3): it ANNOUNCES the two keys it answers — the closer look and the gift
        im.style.gridColumn = col;
        im.style.gridRow = "1";
        st.appendChild(im);
        seriesArm(im, w, st, col);                       // EX-LOAD-2 (INV-72): the work's own tone holds the place, the photograph fades in over it
        if (im.decode) decodes.push(im.decode().catch(() => {}));   // N7-A11Y (INV-102, D3): feature-guard like the three siblings (06/07/12) — no bare decode where it is unsupported
        return;
      }
      const p = document.createElement("div");         // the polaroid table
      p.className = "exs-print";
      p.dataset.id = w.id;                             // EX-PICSTAT: the room look reads its pic
      p.style.left = (8 + (i % 5) * 17 + (i * 7) % 5) + "%";
      p.style.top = (12 + Math.floor(i / 5) * 26 + (i * 11) % 7) + "%";
      p.style.setProperty("--rot", ((((i * 37) % 13) - 6)) + "deg");
      // EX-LADDER (INV-63): a polaroid's box is a small clamp (84–150px, 72–110px on a phone),
      // so it hands that box and the browser pulls the smallest tier instead of the display file.
      p.innerHTML = '<img src="' + w.img + '"' + ladderAttr(w, ladderSizes("print")) + ' alt="">';
      const pim = p.querySelector("img");                // N7-A11Y (INV-102, C6): the polaroid speaks
      if (pim) {
        pim.alt = workDesc(w.id);
        seriesArm(pim, w, p);                            // EX-LOAD-2 (INV-72): the plate covers the photograph's slot; the cream paper stays paper
      }
      // N7-A11Y (INV-102, B4): the polaroid is a keyboard button — focusable, named, opened by Enter/Space
      p.tabIndex = 0;
      p.setAttribute("role", "button");
      p.setAttribute("aria-keyshortcuts", "z y");        // N7-A11Y (INV-102, B2/B3): the closer look and the gift, announced
      p.setAttribute("aria-label", workDesc(w.id) || ((greetLang() || { t: {} }).t.a11y_photo) || A11Y_PHOTO_EN);
      p.addEventListener("keydown", (ev) => {
        if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); p.click(); }   // open (lift) on the keyboard's own keys
      });
      p.addEventListener("click", () => {
        const was = p.classList.contains("lift");
        st.querySelectorAll(".exs-print").forEach((x) => x.classList.remove("lift"));
        if (!was) {
          const r = p.getBoundingClientRect();
          p.style.setProperty("--cx", (innerWidth / 2 - (r.left + r.width / 2)) + "px");
          p.style.setProperty("--cy", (innerHeight / 2 - (r.top + r.height / 2)) + "px");
          p.classList.add("lift");
          pulse("series_lift", w.id);                  // every LIFT counts; setting it down does not (EX-PULSE)
        }
      });
      st.appendChild(p);
    });
    if (S.variant === "lane") {       // a real touch on the lane spends the re-affirm below (INV-88):
      laneTouchOff = () => { laneTaken = true; };            // the visitor already has it in hand,
      st.addEventListener("touchstart", laneTouchOff, { passive: true, once: true });   // never yank it
    }
    const T = (greetLang() || { t: {} }).t;
    side.querySelector(".exs-back").textContent = T.room_back || ROOM_BACK_EN;
    side.hidden = false;
    openTrap(side, sideOpener);                         // N7-A11Y (B1): the room takes focus, holds Tab inside, returns focus to the opener on close
    // the room opens on the series' FIRST member — a fresh look from the top, never resuming where a
    // prior visit left the lane. #exs-stage is a reused element and the browser's scroll-anchoring
    // keeps its leftover scrollLeft across a content rebuild, so clear it explicitly on open (INV-88).
    st.scrollLeft = 0;
    // the rest survives the pictures' own late arrival (INV-88): CSS refuses the browser's scroll
    // compensation (overflow-anchor:none), and once every lane picture has actually decoded (taken
    // its real size) the rest is re-affirmed — guarded by this dress's own generation AND by whether
    // the visitor has already taken the lane in hand (a touch mid-decode spends laneTaken), so a
    // rebuilt/closed room, or one the visitor is already mid-swipe on, is never touched.
    if (decodes.length) {
      Promise.all(decodes).then(() => {
        if (dressGen === cerGen && sideOpen && !laneTaken) st.scrollLeft = 0;
      });
    }
    document.body.classList.add("ex-side");            // the lock law, reused (EX-DOOR-2f)
    if (laystep !== false) pushFace({ face: "series", ser: idx });
    pulse("series_open", focusedId);                   // the work whose series opened (EX-PULSE registry)
  }
  function closeSide(soft) {
    if (!sideOpen) return;
    closeTrap(side);                                   // N7-A11Y (B1): release the trap, restore focus to the opener
    sideOpen = false;
    if (!soft) {                                       // instant teardown — the next face paints its
      faceSync();                                      // own visuals (a door render, a forward re-open);
      side.hidden = true;                              // the caller ran ceremonyCancel already
      document.body.classList.remove("ex-side");
      recentreUnder();                                 // a rotation under the room is honoured (EX-COMPOSE)
      return;
    }
    // SOFT: the way OUT mirrors the way IN (EX-SERIES / INV-46) — the same veil crossing openSide
    // plays, reversed. His phone find 2026-07-12: the entry was a soft black crossing while the exit
    // snapped back in one instant. Now the veil covers, the walk returns beneath the black on its
    // exact frame, one fade reveals it — the exit carries the entry's own breath.
    busy = true;                                       // the lock spans the whole close crossing (EX-CHROME)
    faceSync();
    const g = ++cerGen;                                // a second navigation mid-close wins (ceremonyCancel)
    const ok = () => g === cerGen;
    veil.hidden = false;
    veil.style.transitionDuration = (0.33 * TEMPO) + "s";
    requestAnimationFrame(() => veil.classList.add("on"));   // the black covers first
    cerAfter(0.4, () => { if (!ok()) return;                 // under the black: the room leaves, the walk returns
      side.hidden = true;
      document.body.classList.remove("ex-side");
      // land on the EXACT frame left (INV-32b / EX-COMPOSE). recentreUnder() no-ops while a face
      // stands (busy is held for the whole crossing, as on the way in), so under the black we drive
      // the scroll directly and re-freeze the guard at the landing — the guard would otherwise hold
      // the pre-close position and undo the re-centre.
      if (document.documentElement.classList.contains("ex-walk")) {
        const stops = frameStops();
        if (stops.length) {
          const i = nearestStop(stops, scrollY);
          const y = restingEl ? frameCenter(restingEl) : stops[i];
          passJump(restingEl || stage.querySelectorAll(".exh-frame, .exh-fin")[i] || null, "series");
          scrollTo(0, y);
          guardHold = y;                                     // the guard holds the re-centred frame (EX-CHROME)
        }
      }
      veil.style.transitionDuration = (0.53 * TEMPO) + "s";
      veil.classList.remove("on");                           // …and the walk is revealed in one breath
    });
    cerAfter(0.95, () => { if (!ok()) return;
      veil.hidden = true;
      busy = false;
      faceSync();
    });
  }
  cap.addEventListener("click", (ev) => {
    const b = ev.target.closest && ev.target.closest(".ex-series");
    if (!b) return;
    openSide(+b.dataset.ser);
  });
  side.querySelector(".exs-back").addEventListener("click", () => history.back());
  addEventListener("keydown", (ev) => {                // Esc = the same honest road as Back
    if (ev.key !== "Escape" || !sideOpen) return;
    // a layer standing ABOVE the room owns the key — its own Escape is already taking the step back.
    // The room hangs works a visitor can open a closer look or a gift ceremony from (INV-67), so
    // without this the one key would step history twice and tear down both layers at once.
    if (zoomOpen || giftOpen || quizOpen) return;
    history.back();
  });
  // N7-A11Y (INV-102, B4): the lane scrolls by keyboard as well as by tap and by click. One listener on
  // the room (never piling up across reused dresses); it acts only while a LANE stage stands.
  side.addEventListener("keydown", (ev) => {
    if (!sideOpen || (ev.key !== "ArrowRight" && ev.key !== "ArrowLeft")) return;
    const st = side.querySelector("#exs-stage");
    if (!st || !st.classList.contains("lane")) return;
    ev.preventDefault();
    st.scrollLeft += (ev.key === "ArrowRight" ? 1 : -1) * Math.max(120, Math.round(st.clientWidth * 0.6));
  });
  // EX-COMPOSE: a print lifted to the light re-centres to the live viewport — a centre measured
  // before a rotation never survives it (the delta rides ON TOP of the standing --cx/--cy).
  let sdrsz = null;
  function sideReCentre() {
    if (!sideOpen) return;
    clearTimeout(sdrsz);
    sdrsz = setTimeout(() => {
      const p = side.querySelector(".exs-print.lift");
      if (!p) return;
      const r = p.getBoundingClientRect();
      const cx = parseFloat(p.style.getPropertyValue("--cx")) || 0;
      const cy = parseFloat(p.style.getPropertyValue("--cy")) || 0;
      p.style.setProperty("--cx", (cx + (innerWidth / 2 - (r.left + r.width / 2))) + "px");
      p.style.setProperty("--cy", (cy + (innerHeight / 2 - (r.top + r.height / 2))) + "px");
    }, 150);
  }
  addEventListener("resize", sideReCentre);
  // a rotation is its OWN beat on iOS (INV-86), and its settled dimensions arrive on the visualViewport
  // "resize" — without these the lifted print stays off-centre after a phone turn.
  addEventListener("orientationchange", sideReCentre);
  if (window.visualViewport) visualViewport.addEventListener("resize", sideReCentre);

/*!17-place-hash-boot.js*/
  // ---- the walk TRACKS its place (INV-32c — the law outlived the ↗, its first carrier):
  // the io callback above writes the per-tab marker per frame in view; any return within
  // the tab (reload, the work page's plain link, Back) restores it
  function restorePlace() {
    let m = null;
    try { m = JSON.parse(sessionStorage.getItem(PLACE_KEY) || "null"); } catch (e) {}
    try { sessionStorage.removeItem(PLACE_KEY); } catch (e) {}   // one-shot
    if (!m || m.v !== VER) return;                     // stale/foreign marker → the top, never an error
    const f = stage.querySelector('.exh-frame[data-id="' + m.id + '"]');
    if (f) { passJump(f, "restore"); scrollTo(0, frameCenter(f)); }   // centered in the LIVE viewport (EX-GLIDE)
  }

  // ---- the permalink arrival (EX-SHARE-IN): the hash is a doorway, not a leash ----
  // #w-<id> = a handed-over pick: among the SHOWN frames → instant jump, the arc unchanged;
  // otherwise → acts as a pick (fresh-top, the door passed, no greeting). Consumed once per
  // hand-over (per-tab spent marker); it stays in the address and lays no step of its own.
  function consumeHash() {
    const m = location.hash.match(/^#w-([\w-]+)$/);
    const hid = m && m[1];
    if (!hid || !byId[hid]) return null;               // unknown id changes nothing (c)
    let spent = null;
    try { spent = sessionStorage.getItem(SPENT_KEY); } catch (e) {}
    return spent === "w-" + hid ? null : hid;          // INV-32c wins once the hash is spent
  }
  function arriveByHash(hid) {
    tlog("handover");
    pulse("share_arrive", hid, shareArriveExtra());      // join back to the share that minted `s`, plus the remembered channel (EX-SHARE / EX-SHARE-ORIGIN / INV-1)
    const shownIds = entered ? order.slice(0, shown) : [];
    if (!(entered && shownIds.indexOf(hid) >= 0)) {    // (b) acts as a pick — fresh-top,
      pick = hid;                                      // the same law a door pick lives by
      order = arcOrder(pick);
      shown = SPREAD;                                  // the budget stays derived+capped (INV-30)
      entered = true;
      if (atDoor) closeDoor();
      ground(byId[hid].dom);
      renderHang();
      save();
    } else {                                           // (a) already hangs — the walk continues,
      if (atDoor) closeDoor();                         // «выставка не рвётся»
      ground(byId[hid].dom);
      if (!stage.querySelector(".exh-frame")) renderHang();
    }
    replaceFace({ face: "walk" });                     // no step of its own (INV-32e)
    try { sessionStorage.setItem(SPENT_KEY, "w-" + hid); } catch (e) {}
    // a #w- landing abandons any in-flight preload and re-aims a fresh one-ahead from the landing
    // frame, forward by default until a step declares a direction (EX-LOAD-3 / prover F5)
    travelDir = 1; preloadCancel();
    const f = stage.querySelector('.exh-frame[data-id="' + hid + '"]');
    if (f) { passJump(f, "hash"); scrollTo(0, frameCenter(f)); }      // instant, centered in the LIVE viewport
    // the consuming jump writes the place marker so the room's memory agrees with the eye
    try { sessionStorage.setItem(PLACE_KEY, JSON.stringify({ v: VER, id: hid })); } catch (e) {}
  }
  addEventListener("hashchange", () => {               // a pasted room link IS an arrival too
    const hid = consumeHash();
    if (!hid) return;
    ceremonyCancel();
    arriveByHash(hid);
  });

  // ---- boot -----------------------------------------------------------------
  // the face the tab last stood on survives a reload in history.state (INV-54): a reload HOLDS it —
  // the door stays the door, the walk stays the walk; only a PICK ever commits a walk behind the door.
  // A door is "held" on reload ONLY when it was reached by EXITING a walk (`returned`) — a cold door,
  // and a cold door with a returning/injected walk, keep the normal paths (greeting / the walk).
  const prior = (history.state && history.state.@@NS@@) || null;
  const returnedDoor = !!(prior && prior.face === "door" && prior.returned);
  entered = restore();
  document.body.classList.add("ex-live");              // hide the static index, wake the live face
  const handed = consumeHash();
  if (handed) {
    arriveByHash(handed);                              // the shared work itself is the welcome
  } else if (returnedDoor && doorAvailable) {
    // EX-DOOR-RELOAD (INV-54): the visitor walked, EXITED back to the door, then reloaded — HOLD the
    // door, never drop into the walk saved behind it. The held door refreshes gently: ≥60% kept, ≤40%
    // new. The `returned` mark rides on so repeated reloads keep holding the door.
    // EX-DOOR-4 (F1 folded 11:50): an unconsumed circle wins ONCE — deal fresh; every reload with no
    // circle pending obeys the reload law, and the fresh hand's own later reloads keep ≥60% too.
    const pend = circlePending();
    const sp = pend ? dealHand(pend) : refreshHand();
    renderDoor(sp, false);                             // the exit already spent the greeting
    replaceFace({ face: "door", spread: sp.map((e) => e.id), returned: true });
  } else if (entered) {
    if (pick) ground(byId[pick] && byId[pick].dom);
    renderHang();                                      // a return visit continues its walk — no door
    replaceFace({ face: "walk" });                     // the standing entry is a walk step (INV-32)
    restorePlace();                                    // the ↗ round-trip keeps the place (INV-32c)
  } else if (doorAvailable) {
    const sp = dealHand();                             // a cold ARRIVAL deals a fresh hand (EX-DOOR-3)
    renderDoor(sp, true);                              // a cold visitor meets the threshold — greeted
    replaceFace({ face: "door", spread: sp.map((e) => e.id), cold: true });
  } else {
    entered = true;                                    // no/thin pool → the diverse hang directly,
    renderHang();                                      // never a block (EX-DOOR-2a: the skip's old
    save();                                            // mechanism, internal only now)
    replaceFace({ face: "walk" });
  }

/*!18-i18n-memory-lang.js*/
  // ---- EX-I18N (INV-42): the museum speaks ANY language — after first paint ----
  // A locale outside the baked seven meets the fallback INSTANTLY; the site then quietly asks
  // its own worker for that locale's set (once per language-version, ever), keeps a browser
  // copy, and the standing surfaces re-speak without a jump. A dead worker changes nothing.
  function respeak() {
    applyDocDir();                                    // EX-RTL: a manual pick / any-locale arrival re-mirrors the whole tree
    const L = greetLang();
    if (!L) return;
    const T = L.t;
    // the zoom close + the sound chrome carry aria-labels, not visible text, but they still ride the
    // ONE string layer (EX-I18N) — the controls live on every face (walk, door, side room), so they
    // relabel regardless of atDoor
    const zClose = zoom.querySelector(".exz-close");
    if (zClose) zClose.setAttribute("aria-label", T.a11y_close || A11Y_CLOSE_EN);
    const sndVol = document.querySelector("#ex-sound .exsnd-vol");
    const sndBtn = document.querySelector("#ex-sound .exsnd-btn");
    if (sndVol) sndVol.setAttribute("aria-label", T.a11y_volume || A11Y_VOLUME_EN);
    if (sndBtn) sndBtn.setAttribute("aria-label", T.a11y_sound || A11Y_SOUND_EN);
    if (atDoor) {
      door.setAttribute("dir", T.dir === "rtl" ? "rtl" : "ltr");
      door.setAttribute("lang", L.code);
      door.querySelector(".exd-ask").textContent = T.ask || ASK_EN;
      const g = door.querySelector("#exd-greet");
      if (g && !g.hidden) g.textContent = greetLine(T) || g.textContent;
      return;
    }
    const f = Array.prototype.find.call(
      stage.querySelectorAll(".exh-frame"),
      (x) => { const r = x.getBoundingClientRect();
               return r.top < innerHeight * 0.5 && r.bottom > innerHeight * 0.5; });
    const w = f && byId[f.dataset.id];
    const tEl = cap.querySelector(".title");
    if (w && tEl && w.title) { tEl.textContent = w.title; tEl.classList.remove("untitled"); }
    else if (tEl && tEl.classList.contains("untitled")) { tEl.textContent = T.untitled || UNTITLED_EN; }
    // N7-A11Y (INV-102, EX-HANG): the label just changed tongue under the guest's eye, so the ear is
    // told it again — otherwise the region would stand in a tongue the label has left, and a guest
    // using a screen reader would get no sign at all that the switch landed.
    if (w && cap.classList.contains("show")) announceLabel(w);
    const fin = document.getElementById("exh-fin");
    if (fin) {
      fin.setAttribute("lang", L.code);
      fin.setAttribute("dir", T.dir === "rtl" ? "rtl" : "ltr");
      const u = fin.querySelector("#ex-unfold");
      const b = fin.querySelector("#ex-return");
      const q = fin.querySelector(".q");
      if (q) q.textContent = u ? (T.q_more || q.textContent) : (T.q_spent || q.textContent);
      if (u) u.textContent = (T.more || MORE_EN).replace("{n}", String(UNFOLD)) + " ↓";
      if (b) b.textContent = T.exit || b.textContent;
    }
  }
  // ---- EX-MEMORY (INV-43): the coat-check token — the museum remembers a guest ----
  // A random token (no name, no mail — a cloakroom number); the frames the visitor actually
  // met report in ONE debounced call, fire-and-forget; a failed report is dropped silently.
  if (cfg.visitor_memory === true) {
    let tok = null;
    try { tok = localStorage.getItem(VISITOR_KEY); } catch (e) {}
    if (!tok || !/^[a-z0-9]{16,40}$/.test(tok)) {
      let r = "";
      try {
        const b = new Uint8Array(12);
        crypto.getRandomValues(b);
        r = Array.from(b, (x) => (x % 36).toString(36)).join("");
      } catch (e) { r = Math.random().toString(36).slice(2, 14); }
      tok = r + Date.now().toString(36);
      try { localStorage.setItem(VISITOR_KEY, tok); } catch (e) {}
    }
    const pending = new Set();
    let seenT = null;
    const flush = () => {
      clearTimeout(seenT); seenT = null;
      if (!pending.size) return;
      const add = Array.from(pending); pending.clear();
      try {                                            // the seen-list's local copy grows too —
        const c = JSON.parse(localStorage.getItem(SEENC_KEY) || "null") || { v: VER, ids: [] };
        const st = new Set((c.ids || []).map(String));
        add.forEach((a) => st.add(String(a)));
        localStorage.setItem(SEENC_KEY, JSON.stringify({ v: VER, ids: Array.from(st).slice(-500) }));
      } catch (e) {}                                   // — the NEXT deal's novelty voice (EX-DOOR-3)
      try {
        fetch("/api/visitor", {
          method: "PUT", keepalive: true,
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ t: tok, add: add }),
        }).catch(() => {});
      } catch (e) {}
    };
    window.__@@NS@@Seen = (id) => {
      pending.add(String(id));
      clearTimeout(seenT);
      seenT = setTimeout(flush, 3000);                 // one debounced report per walk stretch
    };
    addEventListener("pagehide", flush);
  }

  const I18N_ON = cfg.ai_i18n === true && GREET && GREET.langs;
  function applySet(code, set) {
    if (!set || !set.ask || !set.dir) return;          // strict shape or nothing (prover I1)
    GREET.langs[code] = set;                           // greetLang() now finds the guest
    if (set.titles) {
      for (const id in set.titles) {
        if (byId[id] && (byId[id].title || "").trim()) byId[id].title = set.titles[id];
      }
    }
    respeak();
  }
  // EX-BUSY (INV-48): a pick of an outsider (non-baked) tongue rides a worker fetch, so the chip wears
  // the waiting ring until the translated strings land (or the fetch fails) — the language pick is no
  // longer a silent hang in the prior tongue. A baked tongue answers from memory and never shows it.
  function langBusy(on) {
    const c = document.querySelector(".exl-cur");
    if (!c) return;
    exBusyRing(c, on);
    if (on) c.setAttribute("aria-busy", "true"); else c.removeAttribute("aria-busy");
  }
  function requestSet(code) {                          // cached-or-fetch, the ONE road (EX-LANG)
    if (!I18N_ON) return;
    const CK = "@@NS@@.i18n." + VER + "." + code;
    let cached = null;
    try { cached = JSON.parse(localStorage.getItem(CK) || "null"); } catch (e) {}
    if (cached) { applySet(code, cached); langBusy(false); return; }
    fetch("/api/i18n?lang=" + code + "&v=" + encodeURIComponent(VER))
      .then((r) => (r.ok ? r.json() : null))
      .then((set) => {
        if (!set) { langBusy(false); return; }
        try { localStorage.setItem(CK, JSON.stringify(set)); } catch (e) {}
        applySet(code, set);
        langBusy(false);                                // the tongue landed — the ring clears
      })
      .catch(() => { langBusy(false); });               // a dead worker changes nothing but the ring clears
  }
  if (I18N_ON) {
    const code = viewerLang();
    const known = (GREET.aliases || {})[code] || code;
    if (/^[a-z]{2,3}$/.test(code) && !GREET.langs[known]) {
      setTimeout(() => requestSet(code), 400);         // deferred — never the arrival's fetch
    }
  }

  // ---- EX-LANG (INV-45): the corner mark — the guest chooses the museum's tongue ----
  if (GREET && GREET.langs) {
    const box = document.createElement("div");
    box.className = "exd-lang";
    box.id = "exd-lang";
    const cur = document.createElement("button");
    cur.type = "button"; cur.className = "exl-cur";
    const list = document.createElement("div");
    list.className = "exl-list"; list.hidden = true;
    box.appendChild(cur); box.appendChild(list);
    door.appendChild(box);                             // the threshold's corner chrome, both faces
    // EX-ARRIVE: the mark is born at opacity:0; the next frame adds .show to breathe it in
    requestAnimationFrame(() => { box.classList.add("show"); });

    // EX-ARRIVE: the dropdown opens and closes by breath (d-soft) so it never pops
    let listCloseTimer = null;
    function listOpen() {
      clearTimeout(listCloseTimer); listCloseTimer = null;
      list.hidden = false;
      requestAnimationFrame(() => { list.classList.add("show"); });
    }
    function listClose() {
      clearTimeout(listCloseTimer); listCloseTimer = null;
      list.classList.remove("show");
      listCloseTimer = setTimeout(() => { list.hidden = true; }, Math.round(600 * TEMPO));
    }

    // EX-LANG-GEO (INV-45/INV-1): the corner offers FEW, geo-relevant tongues — English always and
    // first, then the languages of the visitor's ARRIVING COUNTRY (Cloudflare geo), then the guest's
    // own browser locale — deduped, capped. Not all baked langs. An offered tongue need NOT be baked:
    // ai_i18n's edge-translate layer speaks an outsider on pick (respeak vs requestSet, unchanged).
    const browserCode = (navigator.language || "").toLowerCase().slice(0, 2);
    const LG = cfg.lang_geo || {};                      // the owner's map (may be absent → [en, browser])
    const CMAP = LG.country_langs || {};                // uppercase ISO country → ordered lang codes
    const LANG_CAP = (LG.cap | 0) > 0 ? (LG.cap | 0) : 4;   // total chips; default 4 when absent/invalid

    // The pure narrowing law (testable in isolation): given a country, the country→langs map, the
    // browser locale, and the cap → ordered, deduped codes with English FIRST, then geo langs, then
    // the browser locale; overflow drops from the END (English is never dropped). The map is never
    // trusted to carry "en" — the client always adds it first. The country is only ever an input here.
    /* __EX_LANG_GEO_NARROW__ */
    function narrowLangCodes(country, countryLangs, browserCode, cap) {
      const out = [];
      const seen = {};
      const add = (c) => {
        c = (c || "").toLowerCase();
        if (!/^[a-z]{2,3}$/.test(c) || seen[c]) return;
        seen[c] = true; out.push(c);
      };
      add("en");                                       // English always present, and always first
      const geo = (countryLangs && country && countryLangs[country]) || [];
      for (const c of geo) add(c);                      // the arriving country's tongues, in its order
      add(browserCode);                                // the guest's own tongue, last
      const n = (cap | 0) > 0 ? (cap | 0) : 4;          // default 4 when absent/invalid
      return out.slice(0, n);                           // the cap drops overflow from the END
    }
    /* __/EX_LANG_GEO_NARROW__ */

    const markOf = () => {
      const c = viewerLang();
      return ((GREET.aliases || {})[c] || c).toUpperCase().slice(0, 2) || "EN";
    };
    const redraw = () => {
      cur.textContent = markOf();
      list.querySelectorAll(".exl-item").forEach((b) =>
        b.classList.toggle("cur", b.dataset.lang === viewerLang()));
    };
    // ONE chip-append road — the initial build and the post-geo refresh both run it, so per-chip
    // behavior can never drift between them. The list is cleared first: no stale chip, no double listener.
    const renderCodes = (codes) => {
      list.textContent = "";
      codes.forEach((c) => {
        const b = document.createElement("button");
        b.type = "button"; b.className = "exl-item";
        b.dataset.lang = c;
        b.textContent = c.toUpperCase();
        b.addEventListener("click", (ev) => {
          ev.stopPropagation();
          langOverride = c;
          try { localStorage.setItem(LANG_KEY, c); } catch (e) {}
          listClose();
          const known = (GREET.aliases || {})[c] || c;
          const baked = !!GREET.langs[known];
          // EX-PULSE registry: the chosen tongue is a CODE from the baked list; an outsider tongue
          // reports `other`, never a raw locale string on the wire — the ladder stays closed (INV-1).
          // The ARRIVING COUNTRY never enters a pulse: it only picked which chips exist.
          pulse("lang_pick", null, { lang: baked ? known : "other" });
          if (baked) respeak();                        // a baked tongue answers at once
          else { langBusy(true); requestSet(c); }      // an outsider rides the one layer — the chip waits (EX-BUSY)
          redraw();
        });
        list.appendChild(b);
      });
      redraw();
    };

    // First paint: English + the browser locale only (geo has not answered yet).
    renderCodes(narrowLangCodes("", CMAP, browserCode, LANG_CAP));

    // Then, once and quietly, ask the edge for the arriving country and re-narrow. Best-effort:
    // a failed, blocked, or unknown-country geo NEVER touches the box — it stays [en, browser].
    // The country is used ONLY to pick chips here; it is never stored, never sent to GA, never on a beat.
    try {
      fetch("/api/geo")
        .then((r) => (r.ok ? r.json() : null))
        .then((g) => {
          const cc = g && typeof g.c === "string" ? g.c.toUpperCase() : "";
          if (!cc || !CMAP[cc]) return;                // no country, or one we hold no langs for ⇒ stand pat
          renderCodes(narrowLangCodes(cc, CMAP, browserCode, LANG_CAP));
        })
        .catch(() => {});                              // a dead / blocked geo changes nothing
    } catch (e) {}

    cur.addEventListener("click", (ev) => {
      ev.stopPropagation();
      list.hidden ? listOpen() : listClose();
    });
    door.addEventListener("click", () => { listClose(); });
    // N7-A11Y (INV-102, B5): the list closes under every modality — on the keyboard's own Escape (from
    // anywhere while the list stands), and when focus leaves the corner entirely (a Tab / a click away),
    // beside the existing document-click. Escape is document-level so it closes regardless of where focus
    // sits; the focus-out close reads a real focus leaving the box.
    addEventListener("keydown", (ev) => {
      if (ev.key === "Escape" && !list.hidden) { listClose(); try { cur.focus(); } catch (e) {} }
    });
    box.addEventListener("focusout", (ev) => {
      if (!list.hidden && !box.contains(ev.relatedTarget)) listClose();   // focus left the corner → close
    });
    redraw();
  }

/*!98-sound.js*/
  // ---- EX-SOUND (INV-48): the ambient loop walks beside the guest ----------------------------
  // OFF by default — a fresh visit is silent and the audio loads ONLY on the first turn-on
  // (the perf fence), never on cold load. STREAMS from a <audio> element (preload none, native
  // loop): it plays as the first fragments arrive, so the press is answered at once rather than
  // after the whole file downloads and decodes. The native loop carries a faint seam at the wrap —
  // the accepted cost of the instant start. The fade rides a MediaElementSource → gain node so the
  // ramp works on every device (iOS included, where the element's own volume cannot be scripted):
  // in ~0.7s ×tempo, out ~0.8s and on leaving / unload (pagehide, best-effort). Volume default 0.3
  // with a ≥44px touch-friendly slider. The on/off + volume persist in ex.sound (versioned); a
  // return ON ARMS on the first gesture (autoplay is blocked without one) rather than loading on
  // cold arrival. A missing/failed file fails SILENT (INV-1). Two beats ride the EXISTING EX-PULSE
  // wire: sound_on / sound_off (no new analytics plumbing).
  // EX-SOUND-PAUSE (INV-52): off is a PAUSE that holds the moment on the element's own currentTime,
  // on RESUMES from it — a fresh page load builds a new element and starts from the top.
  // Config keys (config.json → exhibition): sound_url (audio file, empty = player hidden),
  // sound_credit.artist / sound_credit.title / sound_credit.url (the credit tray text + link).
  (function sound() {
    const SND_URL = (EX.sound_url || "").trim();
    if (!SND_URL) return;                                // no audio configured — player stays hidden
    const CREDIT = EX.sound_credit || {};
    const FADE_IN = 0.7, FADE_OUT = 0.8, DEFAULT_VOL = 0.3;

    const box = document.createElement("div");
    box.id = "ex-sound";
    // aria-labels localize through EX-I18N like every other chrome string; the fallback is ENGLISH
    // (source tongue), never a hardcoded locale literal
    const SNDT = (greetLang() || { t: {} }).t;
    // the tray sits to the LEFT of the button (slides out on hover / while playing / focus-within);
    // the credit uses config-driven artist/title/url — never hardcoded content (INV-1)
    const artistHtml = CREDIT.artist ? `<span class="t"><b>${CREDIT.artist}</b></span>` : "";
    const titleHtml = CREDIT.title ? `<span class="t">«${CREDIT.title}»</span>` : "";
    const linkHtml = CREDIT.url
      ? `<a href="${CREDIT.url}" target="_blank" rel="noopener">${CREDIT.url.replace(/^https?:\/\//, "")}</a>`
      : "";
    box.innerHTML =
      '<div class="exsnd-tray">' +
        '<span class="exsnd-cred">' + artistHtml + titleHtml + linkHtml + '</span>' +
        '<input class="exsnd-vol" type="range" min="0" max="1" step="0.01" value="0.3"' +
          ' aria-label="' + (SNDT.a11y_volume || A11Y_VOLUME_EN) + '">' +
      '</div>' +
      '<button class="exsnd-btn" type="button" aria-pressed="false"' +
        ' aria-label="' + (SNDT.a11y_sound || A11Y_SOUND_EN) +
        '"><span class="ex-busy-ring" aria-hidden="true"><svg viewBox="0 0 40 40" fill="none">' +
          '<circle cx="20" cy="20" r="17"></circle></svg></span>' +
        '<span class="exsnd-note"><svg viewBox="0 0 16 16" fill="none" aria-hidden="true">' +
          '<path d="M6.3 4.1 L12.9 3" stroke="currentColor" stroke-width="2.1" stroke-linecap="round"/>' +
          '<path d="M6.3 4.1 V12 M12.9 3 V11" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>' +
          '<circle cx="4.2" cy="12" r="2.35" fill="currentColor"/><circle cx="10.8" cy="11" r="2.35" fill="currentColor"/>' +
        '</svg></span><span class="exsnd-eq"><i></i><i></i><i></i></span></button>';
    document.body.appendChild(box);
    requestAnimationFrame(() => box.classList.add("show"));   // EX-ARRIVE: arrives on the breath

    const btn = box.querySelector(".exsnd-btn");
    const vol = box.querySelector(".exsnd-vol");

    // The player STREAMS: a single <audio> element (preload none, native loop) plays as soon as the
    // first fragments arrive and fetches the rest on the fly, so the press is answered at once — no
    // download-then-decode wait. The element routes through a MediaElementAudioSourceNode → gain so
    // the fade ramps on every device, iOS included, where the element's own volume cannot be scripted.
    let ctx = null, srcNode = null, gain = null;
    let aud = null, wired = false, pauseTimer = 0;
    let target = DEFAULT_VOL, desired = false, playing = false, armed = false;
    let ready = false, loading = false;
    // EX-SOUND-PAUSE (INV-52): off is a PAUSE, on RESUMES — never a within-session restart. The
    // element OWNS the playhead (aud.currentTime), so a pause holds the moment natively and a resume
    // continues from it; no manual offset bookkeeping. A fresh page load builds a new element at 0.

    // the remembered choice (versioned like the walk)
    let pref = null;
    try { pref = JSON.parse(localStorage.getItem(SND_KEY) || "null"); } catch (e) {}
    if (!pref || pref.v !== VER) pref = null;
    if (pref && Number.isFinite(+pref.vol)) target = Math.min(1, Math.max(0, +pref.vol));
    vol.value = String(target);

    function persist() {
      try {
        localStorage.setItem(SND_KEY, JSON.stringify({ v: VER, on: desired, vol: target, greeted: greeted }));
      } catch (e) {}
    }

    // EX-SOUND-GREET (INV-101): on the FIRST visit only, a localized word greets beside the note,
    // holds, then settles away — leaving the bare note. It fires the first frame the player is truly
    // VISIBLE (the control retracts under the door, so a greeting on cold load would breathe out of
    // sight; this waits for the walk), robust to every entry — the door, a shared work, a resumed walk.
    // The once-ness is consumed only when the word actually shows and persists in ex.sound (`greeted`),
    // so a return meets only the quiet note. Reduced motion / Save-Data stand the choreography down (the
    // note rests, unmarked, so a later ordinary visit may still greet once). The word is a greeting,
    // The word rides a small pill that is a SECOND HIT AREA for the control beside it: a press on the
    // word turns the sound on (the owner's word of 2026-07-28 — "a button carrying the word music").
    // It stays aria-hidden with no tab stop, since the control it presses stands next to it and every
    // road — finger, pointer, key — already reaches that one button; the press is forwarded to it.
    // A one-time glint sweeps the pill as it arrives, the same sweep the quiz chip wears.
    // NEVER BOTH AT ONCE (his same word): the word waits for a moment when no quiz chip stands on the
    // walk, and a chip arriving while the word shows withdraws the word at once and RELEASES the
    // first-arrival mark, so a later quiet moment still greets a first-time visitor properly.
    let greeted = !!(pref && pref.greeted);
    const chipStands = () => !!document.querySelector(".ex-quiz-chip");
    function greetOnce() {
      if (greeted || REDUCED || dataSaver()) return;
      greeted = true;
      persist();                                          // consume the first arrival on show
      const g = document.createElement("button");
      g.type = "button";
      g.className = "exsnd-greet";
      g.setAttribute("aria-hidden", "true");              // the control beside it owns every road in
      g.tabIndex = -1;                                    // one control on the tab road, never two
      g.textContent = SNDT.sound_greet || SOUND_GREET_EN;
      const gl = document.createElement("span");
      gl.className = "exsnd-glint";
      gl.setAttribute("aria-hidden", "true");
      g.appendChild(gl);
      g.addEventListener("click", () => { try { btn.click(); } catch (e) {} });
      box.appendChild(g);
      requestAnimationFrame(() => g.classList.add("greet"));
      g.addEventListener("animationend", (ev) => {
        if (ev.target !== g) return;                      // the glint's own end never removes the word
        try { g.remove(); } catch (e) {}
      });
      // the never-both watch: a chip that arrives mid-word takes the moment, the word leaves and the
      // first arrival is handed back (the mark is released, so the greeting is still owed)
      let watch = 0;
      (function watchChip() {
        if (!g.isConnected) return;
        if (chipStands()) {
          g.classList.add("yield");
          greeted = false; persist();
          setTimeout(() => { try { g.remove(); } catch (e) {} }, 400);
          return;
        }
        if (++watch > 400) return;
        requestAnimationFrame(watchChip);
      })();
    }
    if (!greeted && !REDUCED && !dataSaver()) {
      let tries = 0;
      (function waitVisible() {
        if (greeted) return;
        const shown = parseFloat(getComputedStyle(box).opacity || "0") > 0.5
                      && !document.body.classList.contains("ex-door")
                      && !chipStands();                   // never offered beside the quiz chip
        if (shown) { greetOnce(); return; }
        if (++tries > 600) return;                        // ~10s cap — the visitor never left the door
        requestAnimationFrame(waitVisible);
      })();
    }

    function prepare() {
      if (ready || loading) return ready;
      loading = true;
      try {
        aud = document.createElement("audio");
        aud.src = SND_URL;
        aud.loop = true;                                 // native loop — a faint seam at the wrap
        aud.preload = "none";                            // stream on play, never a cold-load fetch
        // NO crossOrigin: the audio is same-origin, and a MediaElementSource over a CORS request the
        // static host does not answer (Cloudflare Pages sends no ACAO on static assets) would taint
        // the node and output SILENCE — same-origin needs no CORS and must not opt into it
        // a failed file fails SILENT (INV-1): stop the graph so no equalizer shows, and leave the
        // button's own aria-pressed as the visitor's CHOICE (the equalizer bars, not the button,
        // signal actual playback) — desired and aria-pressed stay coherent, no false sound_off beat
        aud.addEventListener("error", () => { stop(); });
        ctx = ctx || new (window.AudioContext || window.webkitAudioContext)();
        gain = ctx.createGain(); gain.gain.value = 0; gain.connect(ctx.destination);
        // one MediaElementSource per element, created once; the element's output now routes ONLY
        // through the graph, so the gain MUST reach the destination (wired just above)
        srcNode = ctx.createMediaElementSource(aud);
        srcNode.connect(gain);
        wired = true;
        ready = true;
      } catch (e) { ready = false; }
      loading = false;
      return ready;
    }

    // "scroll" is deliberately NOT in the arm set: a scroll grants no user-activation, so it would
    // burn the one-shot arm on a play() that WebKit is guaranteed to refuse. Only true activation
    // gestures (a press or a key) can start audio.
    function arm() {
      if (armed || playing) return;
      armed = true;
      ["pointerdown", "touchstart", "keydown"].forEach((e) =>
        addEventListener(e, onGesture, { once: true, passive: true, capture: true }));
    }
    function disarm() {
      if (!armed) return;
      armed = false;
      ["pointerdown", "touchstart", "keydown"].forEach((e) =>
        removeEventListener(e, onGesture, { capture: true }));
    }
    function onGesture(e) {
      disarm();
      // a gesture ON the player itself is the button's own click to own (the toggle). Starting here
      // too would race start() against the same tap's click → setDesired() toggle-off — the "second
      // press does nothing / turns off" shape. Let the click be the single owner of an on-player tap.
      if (e && e.target && box.contains(e.target)) return;
      if (desired) start();
    }

    function setDesired(on) {
      if (on === desired) return;
      desired = on;
      btn.setAttribute("aria-pressed", on ? "true" : "false");
      pulse(on ? "sound_on" : "sound_off");
      persist();
      if (on) start(); else stop();
    }

    async function start() {
      if (playing) return;
      const ok = prepare();
      if (!desired) return;
      if (!ok) { box.classList.remove("playing"); return; }
      if (pauseTimer) { clearTimeout(pauseTimer); pauseTimer = 0; }   // cancel a pending pause
      // EX-SOUND-LOADING (INV-48): the press is taken the instant it lands — the note breathes
      // softly (CSS .loading) while the stream buffers, so a slow first fetch reads as "loading",
      // never as "nothing happened". It clears the moment sound begins, the file fails, or a still-
      // blocked press falls back to arming.
      box.classList.add("loading");
      // ONE press is ONE user-activation, and the element's play() needs it. play() is called
      // synchronously inside the gesture and its success is NEVER discarded. The context resume is
      // kicked alongside, but the code never blocks forever on it: on WebKit ctx.resume() can hang
      // unsettled, and iOS parks a fresh context in a non-running state ("suspended"/"interrupted"),
      // so the AUDIBLE ramp is DEFERRED to the moment the context actually reaches "running"
      // (fadeInWhenRunning), with every later gesture nudging resume until it does. The element
      // resumes from its own playhead (EX-SOUND-PAUSE/INV-52).
      const resuming = (ctx.state !== "running") ? ctx.resume() : null;
      let played = false;
      try { await aud.play(); played = true; }
      catch (e) {
        // WebKit refused the FIRST play() because the context was not yet running at the call. Give
        // the resume a BOUNDED moment — race it against a short timeout so a never-settling resume
        // (a known WebKit state) cannot hang the press — then RETRY play() ONCE on the same activation
        // chain. A genuine block (no activation at all) still fails and arms below.
        if (resuming) { try { await Promise.race([resuming, new Promise((r) => setTimeout(r, 250))]); } catch (e2) {} }
        try { await aud.play(); played = true; } catch (e2) { played = false; }
      }
      if (!desired) { box.classList.remove("loading"); try { aud.pause(); } catch (e) {} return; }
      if (!played) { box.classList.remove("loading"); arm(); return; }   // no activation at all → wait for the next gesture
      // a successful play() is KEPT even while the context is still suspended: audible output rides
      // the graph, so the fade waits for the context to run (fadeInWhenRunning). The first press is
      // therefore never thrown away — no second tap is ever required to make sound.
      box.classList.remove("loading");
      playing = true; armed = false;
      box.classList.add("playing");
      fadeInWhenRunning();
    }

    // The audible fade rides the gain node, which sounds only once the context is "running". On WebKit
    // a fresh context stays suspended past the first gesture, so the ramp is scheduled the instant the
    // context reaches "running" — the same gesture when resume lands in time, a moment later otherwise,
    // a later gesture at worst — and every real gesture nudges resume until it does. This is why a
    // successful first press never needs a second tap: the play is kept, the fade merely waits.
    function rampIn() {
      if (!ctx || !gain) return;
      const now = ctx.currentTime;
      gain.gain.cancelScheduledValues(now);
      gain.gain.setValueAtTime(Math.max(0.0001, gain.gain.value), now);
      gain.gain.linearRampToValueAtTime(target, now + FADE_IN * TEMPO);
    }
    let fadeArmed = false;
    function fadeInWhenRunning() {
      if (!ctx) return;
      if (ctx.state === "running") { rampIn(); return; }
      if (fadeArmed) return;
      fadeArmed = true;
      const nudge = () => { if (ctx.state !== "running") { try { ctx.resume(); } catch (e) {} } };
      const onchange = () => {
        if (ctx.state !== "running") return;
        fadeArmed = false;
        ctx.removeEventListener("statechange", onchange);
        ["pointerdown", "keydown"].forEach((e) => removeEventListener(e, nudge, { capture: true }));
        if (playing && desired) rampIn();
      };
      ctx.addEventListener("statechange", onchange);
      // persistent (NOT once): every later real gesture re-tries resume until the context runs
      ["pointerdown", "keydown"].forEach((e) => addEventListener(e, nudge, { passive: true, capture: true }));
    }

    function stop() {
      disarm();
      if (wired && ctx && gain) {
        const now = ctx.currentTime;
        gain.gain.cancelScheduledValues(now);
        gain.gain.setValueAtTime(gain.gain.value, now);
        gain.gain.linearRampToValueAtTime(0, now + FADE_OUT * TEMPO);
        // pause AFTER the fade so the ramp is heard; the element holds currentTime for a resume.
        // re-read `desired` at fire time — a fast off→on toggle must not pause the re-enabled player.
        if (pauseTimer) clearTimeout(pauseTimer);
        pauseTimer = setTimeout(() => {
          pauseTimer = 0;
          if (!desired && aud) { try { aud.pause(); } catch (e) {} }
        }, Math.round(FADE_OUT * TEMPO * 1000) + 80);
      }
      playing = false;
      box.classList.remove("playing");
      box.classList.remove("loading");   // a file error / off during buffer clears the loading note
    }

    btn.addEventListener("click", () => { setDesired(!desired); });
    vol.addEventListener("input", () => {
      target = Math.min(1, Math.max(0, parseFloat(vol.value) || 0));
      if (playing && ctx) {
        const now = ctx.currentTime;
        gain.gain.cancelScheduledValues(now);
        gain.gain.setValueAtTime(gain.gain.value, now);
        gain.gain.linearRampToValueAtTime(target, now + 0.15);
      }
      persist();
    });
    addEventListener("pagehide", () => {
      if (playing) stop();
      if (aud) { try { aud.pause(); } catch (e) {} }   // best-effort immediate silence on leave
    });

    // a return visit with the pref ON: ARM on the first gesture — never a cold-load fetch
    if (pref && pref.on) { desired = true; btn.setAttribute("aria-pressed", "true"); arm(); }

    // the player's own reachable surface, for the suite
    try {
      window.@@NS_UPPER@@Sound = { state: () => ({ desired, playing, armed, ready, loading,
                                         currentTime: aud ? aud.currentTime : 0 }),
                         url: SND_URL };
    } catch (e) {}
  })();
/*!99-close.js*/
})();
