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

  // ---- the visitor's own trace, its three homes (one place for the names) -----
  const KEY = "@@NS@@.exhibition";                       // the walk (INV-26)
  const PLACE_KEY = "@@NS@@.place";                      // the per-tab place marker (INV-32c)
  const TEMPO_KEY = "@@NS@@-tempo";                      // the motion override (EX-MOTION-R)
  const SPENT_KEY = "@@NS@@.spent";                      // the hash hand-over, consumed once (EX-SHARE-IN)
  const VISITOR_KEY = "@@NS@@.visitor";                  // the coat-check token (EX-MEMORY)
  const HAND_KEY = "@@NS@@.hand";                        // the last dealt threshold hand (EX-DOOR-3)
  const SEENC_KEY = "@@NS@@.seenc";                      // the seen-list's local copy (EX-DOOR-3)
  const DOORDEALT_KEY = "@@NS@@.doordealt";              // works the diverse door has dealt this round (EX-DOOR-3/INV-75)
  const LANG_KEY = "@@NS@@.lang";                        // the guest's chosen tongue (EX-LANG)
  const SND_KEY = "@@NS@@.sound";                         // the ambient player's on/off + volume (EX-SOUND)
  const BEEN_KEY = "@@NS@@.been";                         // EX-RETURN: this browser has walked the exhibition before
  const LAST_KEY = "@@NS@@.last";                        // EX-PULSE/INV-79: this browser's last-visit timestamp (return_gap); EX-RETURN reuses it for the welcome-back window
  const EXITS_KEY = "@@NS@@.exits";                      // EX-RETURN/INV-78: count of real walk→door exits (the farewell waits for the 2nd)
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

