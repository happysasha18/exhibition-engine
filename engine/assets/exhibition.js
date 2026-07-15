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
  const KEY = "ex.exhibition";                       // the walk (INV-26)
  const PLACE_KEY = "ex.place";                      // the per-tab place marker (INV-32c)
  const TEMPO_KEY = "ex-tempo";                      // the motion override (EX-MOTION-R)
  const SPENT_KEY = "ex.spent";                      // the hash hand-over, consumed once (EX-SHARE-IN)
  const VISITOR_KEY = "ex.visitor";                  // the coat-check token (EX-MEMORY)
  const HAND_KEY = "ex.hand";                        // the last dealt threshold hand (EX-DOOR-3)
  const SEENC_KEY = "ex.seenc";                      // the seen-list's local copy (EX-DOOR-3)
  const DOORDEALT_KEY = "ex.doordealt";              // works the diverse door has dealt this round (EX-DOOR-3/INV-75)
  const LANG_KEY = "ex.lang";                        // the guest's chosen tongue (EX-LANG)
  const SND_KEY = "ex.sound";                         // the ambient player's on/off + volume (EX-SOUND)
  const BEEN_KEY = "ex.been";                         // EX-RETURN: this browser has walked the exhibition before
  const MORE_EXIT_EN = "there is more still hanging — come again";   // the exit farewell (English fallback)
  const MORE_RETURN_EN = "back again — a new way in";               // the returning-arrival line (English fallback)

  // ---- EX-TIMING (INV-38): the museum keeps time — for its builder only -------
  // Marks are free and invisible (INV-1: no DOM text; INV-18: no beacon, nothing
  // leaves the tab). ?timings narrates the beats to the console as they land;
  // EXTimings() hands the walk's clock over as data for export.
  const WANT_T = new URLSearchParams(location.search).has("timings");
  function tlog(beat) {
    try { performance.mark("ex:" + beat); } catch (e) {}
    if (WANT_T) {
      try { console.log("ex:" + beat, (performance.now() / 1000).toFixed(3) + "s"); } catch (e) {}
    }
  }
  window.EXTimings = () => performance.getEntriesByType("mark")
    .filter((m) => m.name.indexOf("ex:") === 0)
    .map((m) => ({ beat: m.name.slice(3), at: +(m.startTime / 1000).toFixed(3) }));
  tlog("boot");

  // ---- EX-PULSE (INV-41): the walk counts its beats for the archive's owner ----
  // Rides the ONE sanctioned wire (the baked GA tag); no tag ⇒ total silence; an event
  // carries at most the plain name + the work's public id — never a vector (INV-1).

  // EX-QUIZ-FLOW (INV-69): the session-scoped running-max stage for the quiz funnel.
  // Restored from sessionStorage at boot so a reload never lowers what was reached.
  const QUIZ_STAGE_KEY = "ex.quizstage";
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
      // a closed BAKED-ladder word rides a beat that owns one (gift_kind, lang) — never free text (INV-1)
      if (extra) for (const k in extra) params[k] = extra[k];
      // EX-STORY-AB: when a told story walks beside the guest its variant rides the EXISTING
      // unfold/exit beats as a dimension — no sixth beat is added (INV-41 stands)
      if (storyVariant && (beat === "walk_unfold" || beat === "walk_exit")) {
        params.story_variant = storyVariant;
      }
      // EX-QUIZ-AB (INV-62): the arm rides the SAME two beats as a dimension — only when the flag
      // is on; control/flag-off never carry the key (the payload stays byte-for-byte today's)
      if (quizArm && (beat === "walk_unfold" || beat === "walk_exit")) {
        params.quiz_arm = quizArm;
      }
      // EX-QUIZ-FLOW (INV-69): the quiz stage rides the SAME two beats as a dimension — only when
      // the arm is on and a stage has been reached; never a sixth beat (INV-41 stands)
      if (quizStage && (beat === "walk_unfold" || beat === "walk_exit")) {
        params.quiz_stage = quizStage;
      }
      window.gtag("event", beat, params);
    } catch (e) {}
  }

  // ---- EX-RESET (INV-35): the ?reset address — the museum forgets THIS browser --
  // One wipe, named keys only, BEFORE anything restores; the param strips itself via
  // replaceState — no history step laid (INV-32 fenced) and the pre-strip URL leaves
  // history with it; a storage refusal never blocks the arrival; a sibling window's
  // later save re-creates state by INV-26's last-writer rule.
  if (new URLSearchParams(location.search).has("reset")) {
    try { localStorage.removeItem(KEY); } catch (e) {}
    try { localStorage.removeItem(TEMPO_KEY); } catch (e) {}
    try { sessionStorage.removeItem(PLACE_KEY); } catch (e) {}
    try { sessionStorage.removeItem(SPENT_KEY); } catch (e) {}  // the hash re-seeds a FIRST arrival
    try { localStorage.removeItem(VISITOR_KEY); } catch (e) {}   // forgetting is whole (EX-MEMORY)
    try { localStorage.removeItem(HAND_KEY); } catch (e) {}
    try { localStorage.removeItem(SEENC_KEY); } catch (e) {}
    try { localStorage.removeItem(DOORDEALT_KEY); } catch (e) {}  // the door forgets its shown-round memory (EX-RESET/INV-75)
    try { localStorage.removeItem(LANG_KEY); } catch (e) {}     // the browser's tongue returns
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
  const clampInt = (x, dflt, lo, hi) => {
    const n = parseInt(x, 10);
    return Number.isFinite(n) ? Math.max(lo, Math.min(hi, n)) : dflt;
  };
  const SPREAD = clampInt(EX.spread_size, 10, 3, 12);   // the hang shows ~10, never the catalogue
  const UNFOLD = clampInt(EX.unfold_step, 5, 1, 12);
  const MAXU = clampInt(EX.max_unfolds, 2, 0, 5);       // «ещё 5» retires after this (INV-30)
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

  // ---- honest Back (INV-32): the walk and the browser speak the same history --
  // Steps are laid per FACE (door | walk), never per frame; a door step CARRIES the
  // spread it showed; the ↗ place marker is per-tab (sessionStorage), one-shot.
  try { history.scrollRestoration = "manual"; } catch (e) {}
  const pushFace = (st) => { try { history.pushState({ ex: st }, ""); } catch (e) {} };
  const replaceFace = (st) => { try { history.replaceState({ ex: st }, ""); } catch (e) {} };

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
  try { window.EXStory = { order: storyOrder, hourGap: hourGap }; window.CONFIG = cfg; } catch (e) {}

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
  const QUIZ_SHOWN_KEY = "ex.quizshown";    // per-browser timestamp of the last quiz show
  const QUIZ_TAB_KEY = "ex.quiztab";        // a stable per-tab id when the coat-check is off
  const QUIZ_LS = (id) => "ex.quiz." + id; // per-work answered-memory key (not the coat-check)
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
    } catch (e) {}
    try {                                    // else a stable per-tab id — survives a reload within the walk
      let t = sessionStorage.getItem(QUIZ_TAB_KEY);
      if (!t) { t = Math.random().toString(36).slice(2) + Date.now().toString(36); sessionStorage.setItem(QUIZ_TAB_KEY, t); }
      return t;
    } catch (e) {}
    return "anon";
  })();
  // the A/B arm — decided ONCE per walk off the same token with a DIFFERENT salt; null when the
  // flag is off so nothing stamps the GA beats (the payload stays byte-for-byte today's — INV-60)
  const quizArm = QUIZ_ON ? ((quizHash(QUIZ_TOKEN + ":quizarm") / 4294967296) < 0.5 ? "on" : "control") : null;
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
    // EX-QUIZ-FLOW (INV-69): the chip rendering is the "shown" stage — only under flag+on-arm,
    // which is exactly the quizShows condition; control/flag-off never reach this branch (quizArm guard)
    if (quizArm === "on") quizStageUp("shown");
  }
  // a work surfaces its chip only when the flag is on, the arm is on, and this is the chosen work
  const quizShows = (w) => QUIZ_ON && quizArm === "on" && !!(w && w.quiz) && w.id === quizChosenId;
  // `_hash` is exported for the JS↔Python parity test (test_parity.py): the A/B arm and the
  // per-work pick are drawn from this exact function, so the Python util must mirror it byte-for-byte.
  try { window.EXQuiz = { chosen: () => quizChosenId, arm: () => quizArm, token: QUIZ_TOKEN, _hash: quizHash }; } catch (e) {}
  const STORYLINES = Object.create(null);
  let storyVariant = null;          // the mode the served story reported — rides the GA beats (EX-STORY-AB)
  const toldPortions = new Set();   // portion keys whose plot has actually come back (told ONLY on a served plot)
  const askingPortions = new Set(); // portion keys with a request in flight (never double-ask the same portion)
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
    }
    // the unfold budget DERIVES from shown, never trusted (INV-30 holds on restore)
    shown = clampInt(st.shown, SPREAD, SPREAD, Math.min(order.length, CAP));
    return true;
  }
  const spentUnfolds = () => Math.max(0, Math.floor((shown - SPREAD) / UNFOLD));

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
  // hide ANY plate (the walk's single reused one, or a door window's own) — shared by both call sites
  function plateHideEl(el) {
    el.hidden = true; el.classList.remove("show", "bar");
    if (el.parentNode) el.parentNode.removeChild(el);
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
      if (mark) tlog("plate");
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
    try { window.__exPreload = null; } catch (e) {}     // the test read-side, like EXTimings/__exSeen
  }
  function preloadAhead(curN) {                         // curN = the 1-based frame in view
    if (!PRELOAD_AHEAD) { preloadCancel(); return; }
    const idx = (curN - 1) + travelDir;                 // one ahead along the feet
    if (idx < 0 || idx >= order.length) { preloadCancel(); return; }
    const id = String(order[idx]);
    if (id === preId) return;                           // already warming this exact next work
    preloadCancel();                                    // a turn/jump abandons the old one cleanly (F5)
    const w = byId[id]; if (!w) return;
    preId = id;
    const im = new Image();
    if (w.srcset) { im.sizes = data.walk_sizes || "88vw"; im.srcset = w.srcset; }
    im.src = w.img;                                     // the browser picks the device tier
    preImg = im;
    try { window.__exPreload = { id: id, dir: travelDir }; } catch (e) {}
  }

  // ---- THE DOOR (door.html's face — the norm) --------------------------------
  const door = document.createElement("div");
  door.id = "ex-door";
  door.hidden = true;                                  // born hidden — a restored walk must never
                                                       // wake under a dark cover (2026-07-06 bug)
  door.innerHTML =
    '<div class="exd-wm"></div>' +                    // brand from config.site_name (INV-28)
    '<div class="exd-greet" id="exd-greet" hidden></div>' +
    '<div class="exd-ask">что ближе сейчас?</div>' +
    '<div class="exd-more" id="exd-more" hidden></div>' +   // EX-RETURN: "there is more" — a farewell at the exit, a welcome-back on a return
    '<div class="exd-facade" id="exd-facade"></div>';  // no silent entry — the pick IS the
  door.querySelector(".exd-wm").textContent = cfg.site_name || "";
  document.body.appendChild(door);                     // entry (EX-DOOR-2a, his design word)
  const veil = document.createElement("div");          // the ceremony's black (EX-DOOR-2e)
  veil.id = "ex-veil";
  veil.hidden = true;
  document.body.appendChild(veil);

  let atDoor = false;
  let entered = false;                                 // a walk exists behind the door
  let doorFace = null;                                 // the spread the standing door renders
  let curLay = { n: 0, col: null };

  // cold=true only on the COLD-arrival face: a museum greets on arrival, not on every
  // pass through the lobby (EX-GREET) — the re-opened door keeps the localized ask only
  function renderDoor(spread, cold) {    // the spread is CARRIED by the caller (INV-32a)
    ceremonyCancel();                                  // a door render wins over any crossing
    ladderOff();                                       // the door covers every frame (EX-LOAD-2/-3)
    atDoor = true;
    faceSync();                                        // the door is a face — arm the rest + guard (EX-CHROME)
    tlog("door");
    document.body.classList.add("ex-door");
    door.classList.remove("leaving");
    door.hidden = false;
    doorFace = { spread: spread || doorSet() };
    curLay = { n: 0, col: null };
    const L = greetLang();
    door.setAttribute("dir", L && L.t.dir === "rtl" ? "rtl" : "ltr");
    if (L) door.setAttribute("lang", L.code);
    else door.removeAttribute("lang");
    door.querySelector(".exd-ask").textContent = L ? L.t.ask : "что ближе сейчас?";
    const g = door.querySelector("#exd-greet");
    const line = (cold && GPLACE !== "off" && L) ? greetLine(L.t) : "";
    g.textContent = line;
    g.hidden = !line;                    // ambient: Back to a cold step re-greets at the CURRENT hour
    // EX-RETURN (INV-78): the door says there is more. A door reached by leaving a walk (cold=false) is
    // proof this browser has walked, so we remember it and show the exit farewell; a later COLD arrival
    // from a browser that has walked before is welcomed back. Both true today — the collection outlasts
    // one visit and the door deals a fresh set each open. Localized, English falls back; the return line
    // stands in for the daypart greeting so the door never crowds.
    const more = door.querySelector("#exd-more");
    let moreLine = "";
    let been = null;
    try { been = localStorage.getItem(BEEN_KEY); } catch (e) {}
    if (!cold) {
      try { localStorage.setItem(BEEN_KEY, "1"); } catch (e) {}
      moreLine = (L && L.t.more_exit) || MORE_EXIT_EN;
    } else if (been) {
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
      // the halo speaks liveAccent, never the raw dominant — a near-black dominant is
      // invisible on the dark ground (card 01's note, EX-DOOR-2c)
      const a = liveAccent(w.dom);
      b.style.setProperty("--glow", `rgb(${a.join(",")})`);
      if (animate) {
        b.style.animationDelay = ((0.55 + i * 0.2) * TEMPO).toFixed(2) + "s";
      } else {                                         // relayout: already on screen, no re-fade
        b.style.animation = "none"; b.style.opacity = "1";
      }
      b.innerHTML = `<img src="${w.img}" alt="${alt}">`;
      doorArm(b.querySelector("img"), w, b);             // DL1/DL2: this window rides the walk's ladder
      // EX-QUIZ (INV-64/66): the quiz chip NEVER appears on the door (button-only screen) —
      // only over a work in view on the plaque (quizShows checked in the IO observer below).
      b.addEventListener("click", () => doorPick(w));
      facade.appendChild(b);
    });
  }
  let rsz;
  addEventListener("resize", () => { clearTimeout(rsz); rsz = setTimeout(doorRender, 150); });

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
    door.classList.remove("wm-out");
    document.body.classList.remove("ex-crossing", "ex-cross-cap");
    busy = false;
    faceSync();                                        // the ceremony released (EX-CHROME)
  }

  // the beats below are ONE THIRD of the card's old clock (EX-DOOR-2e re-ruled, his word
  // 2026-07-06 evening) — only the WAITS shortened; the reveal fade keeps its full span
  function doorPick(w) {
    if (busy) return;
    busy = true;
    faceSync();                                        // the ceremony holds the lock (EX-CHROME)
    tlog("pick");
    pulse("door_pick", w.id);
    const g = ++cerGen;
    const ok = () => g === cerGen;
    pick = w.id;
    order = assembleOrder(pick);
    shown = SPREAD;                                    // a fresh arc = a fresh budget (INV-30/31)
    storyReset();                                      // …and a fresh story — no portion leaks across picks (EX-STORY)
    veil.hidden = false;
    veil.style.transitionDuration = (0.33 * TEMPO) + "s";
    door.classList.add("leaving");                     // the wordmark drifts to the center
    requestAnimationFrame(() => veil.classList.add("on"));
    cerAfter(0.92, () => { if (!ok()) return;          // the name lets go
      door.classList.add("wm-out");
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
    cerAfter(1.78, () => { if (!ok()) return;          // …then the first work, separately
      tlog("reveal");
      const first = stage.querySelector(".exh-frame img.work");
      if (first) first.style.transitionDuration = (1.5 * TEMPO) + "s";
      document.body.classList.remove("ex-crossing");
      document.body.classList.add("ex-cross-cap");     // the caption still waits its beat
    });
    cerAfter(1.93, () => { if (!ok()) return;          // the caption, last (+.15)
      tlog("caption");
      document.body.classList.remove("ex-cross-cap");
      const first = stage.querySelector(".exh-frame img.work");
      if (first) first.style.transitionDuration = "";
      veil.hidden = true;
      busy = false;
      faceSync();                                      // the walk is bare — the lock lifts (EX-CHROME)
      // the crossing warms its own picked work, so the room opens without a plate; but a
      // cache-evicted or slow-landing first image falls through to THIS ladder now the lock has
      // lifted (EX-DOOR-2e → EX-LOAD-2). And the feet warm forward from the threshold (EX-LOAD-3).
      travelDir = 1;
      const f0 = stage.querySelector(".exh-frame");
      const im0 = f0 && f0.querySelector("img.work");
      if (im0 && !im0.complete) arm(im0, byId[f0.dataset.id], f0);
      preloadCancel();
      preloadAhead(1);
    });
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
    tlog("exit");
    pulse("walk_exit");
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
    const wasWalk = !atDoor;                            // the face we are LEAVING (before any render)
    const wasSide = sideOpen;                           // the side room may be the face we leave (EX-SERIES)
    ceremonyCancel();                                  // navigation wins mid-ceremony (EX-DOOR-2e)
    const st = ev.state && ev.state.ex;
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
      if (wasWalk) pulse("walk_exit");
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
      scrollTo(0, walkY);                              // the closing screen the visitor left (INV-32b)
      tellStory();                                     // a return is a natural beat — any owed portion re-asks (EX-STORY)
    }
  });

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

  const io = new IntersectionObserver((es) => es.forEach((x) => {
    if (!x.isIntersecting) return;
    if (!sideOpen && !quizOpen && !giftOpen
        && performance.now() - lastResizeAt > 250) {
      restingEl = x.target;                            // the eye's section, fin included — organic
    }                                                  // moves only, never a reflow's stale pixels
    // the closing screen is not a work: the plaque must not strand the last work's title + told
    // story over the finale. Fade the caption out like a frame leaving — never a jump, never stale.
    if (x.target.id === "exh-fin") {                   // the closing screen clears the walk chrome
      cap.classList.remove("show"); shareBtn.classList.remove("show"); focusedId = null; return;
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
    if (window.__exSeen) window.__exSeen(w.id);      // the coat-check report (EX-MEMORY)
    // the walk tracks its place per frame in view (INV-32c re-carried after the ↗ retired)
    try { sessionStorage.setItem(PLACE_KEY, JSON.stringify({ v: VER, id: w.id })); } catch (e) {}
    // a late callback must never re-live the tone ON the door (EX-ACCENT rests at the seams)
    if (!atDoor) ground(w.dom);
    counter.querySelector(".now").textContent = String(+x.target.dataset.n).padStart(2, "0");
    counter.classList.add("show");
    // the floating link follows the eye: it always shares the work IN VIEW (EX-SHARE-BTN)
    shareBtn.dataset.share = w.id;
    shareBtn.setAttribute("aria-label", shareStrings().label);
    shareBtn.classList.add("show");
    // his words and the archive's facts only — never machine prose, never a readout (INV-1);
    // a REAL series (3+) grows its quiet pill — «серия · N», never the machine's theme (EX-SERIES)
    const serIdx = (typeof w.ser === "number" && SERIES[w.ser]) ? w.ser : null;
    const serWord = ((greetLang() || { t: {} }).t.series) || "серия";
    // the wall label's three voices: the NAME, the told LINE (empty until the narrator speaks —
    // EX-STORY-LINE fills it from STORYLINES), the FACTS with a red dot when the work is sold
    cap.innerHTML =
      `<div class="title ${w.title ? "" : "untitled"}">${w.title || "untitled"}</div>` +
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
    fillTold();                                        // the narrator's line for this work, if spoken
  }), { threshold: 0.55 });

  // ---- the told line settles onto the plaque (EX-STORY-LINE) ------------------
  // fillTold paints the focused work's line into the wall label's told-slot (as textContent — the
  // model's words never become markup); it breathes in on the tempo even when it lands late.
  function fillTold() {
    const toldEl = cap.querySelector(".told");
    if (!toldEl) return;
    const line = focusedId != null ? STORYLINES[String(focusedId)] : "";
    if (!line) { toldEl.textContent = ""; return; }    // silent → :empty hides it, no ghost gap
    if (toldEl.textContent === line) return;
    toldEl.textContent = line;
    toldEl.style.animation = "none"; void toldEl.offsetWidth; toldEl.style.animation = "";  // EX-ARRIVE
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
  function storyPortions(n) {                          // [[lo,hi], …] over order indices, the unfold's own beats
    const parts = [];
    const first = Math.min(SPREAD, n);
    if (first > 0) parts.push([0, first]);
    for (let s = first; s < n; ) { const e = Math.min(n, s + UNFOLD); parts.push([s, e]); s = e; }
    return parts;
  }
  function askPortion(loI, hiI) {
    const ids = order.slice(loI, hiI).map(String);
    if (!ids.length) return;
    const key = ids.join(",");                         // this portion's own ordered slice — its cache key
    if (toldPortions.has(key) || askingPortions.has(key)) return;   // already told, or in flight
    askingPortions.add(key);
    const lang = (viewerLang() || "en").toLowerCase();
    fetch("/api/story", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ids: ids, variant: STORY_VARIANT, lang: lang }),
    }).then((r) => (r && r.ok ? r.json() : null)).then((data) => {
      askingPortions.delete(key);
      if (!data || !Array.isArray(data.lines)) return; // refused/failed → key NOT stamped → stays owed
      toldPortions.add(key);                           // told only once the plot has actually come back
      storyVariant = data.story_variant || STORY_VARIANT;   // the mode now rides the GA beats
      for (const l of data.lines) {
        if (l && l.id != null && typeof l.line === "string") STORYLINES[String(l.id)] = l.line;
      }
      fillTold();                                      // settle the line under the work in view
    }).catch(() => { askingPortions.delete(key); });   // a dead worker changes nothing — the portion stays owed
  }
  // tellStory re-asks every portion up to `shown` that is not yet told: the newly opened one on an
  // «ещё 5», plus any earlier portion still owed from a refusal (re-asked at this natural beat). A
  // told portion returns free from cache; an owed one waits for the next beat. Called at each beat —
  // the hang builds, an unfold grows the set, a return re-shows the walk.
  function tellStory() {
    if (!STORY_ON) return;
    for (const [lo, hi] of storyPortions(shown)) askPortion(lo, hi);
  }
  // A fresh door pick is a fresh arc, so it is a fresh story — the previous walk's told/owed portions
  // and its lines never leak into the new one (EX-STORY / INV-30/31).
  function storyReset() {
    toldPortions.clear();
    askingPortions.clear();
    for (const k in STORYLINES) delete STORYLINES[k];
    storyVariant = null;
  }

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
    if (!hold) toastTimer = setTimeout(toastOff, Math.round(3000 * TEMPO));
  }
  toastEl.addEventListener("click", toastOff);
  addEventListener("keydown", (ev) => { if (ev.key === "Escape") toastOff(); });

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
    // from Direct/bot noise — the utm rides before the hash (GA reads the query, the room reads #w-<id>)
    const link = ROOT_URL + "/?utm_source=share&utm_medium=referral#w-" + id;
    const S = shareStrings();
    const write = (navigator.clipboard && navigator.clipboard.writeText)
      ? navigator.clipboard.writeText(link)
      : Promise.reject(new Error("no clipboard"));
    pulse("share_copy", id);
    write.then(() => toast(S.copied))
         .catch(() => toast(link, true));              // never a silent failure (EX-SHARE-BTN)
  });

  // ---- EX-PROTECT (INV-49): a grabbed work meets a GIFT, not the browser's raw save ----
  // A right-click / long-press (contextmenu) or a drag on a work is intercepted and answered by
  // the SAME toast the share line rides — a quiet localized «enjoy» + the site host, arriving on
  // the house breath (EX-ARRIVE). It is a gracious line, never a scold or an error.
  // (CSS `user-select:none` / `touch-action:pan-x pan-y` / `-webkit-touch-callout:none` on
  // img.work handle the soft layer; these listeners handle contextmenu + drag + pinch-zoom.)
  function enjoyLine() {
    const T = (greetLang() || { t: {} }).t;
    const host = ROOT_URL.replace(/^https?:\/\//, "");   // «example.com», appended in code
    const enjoy = T.enjoy || "enjoy";                     // locale string; English built-in fallback
    return enjoy + " · " + host;                          // never blank (EX-PROTECT empty/error facet)
  }
  // EX-PROTECT-RES (INV-56): the download filename base — a slug of the site's own name from config
  // (INV-28), never a hardcoded brand. A grabbed file is «<site>-<original>.jpg».
  const DL_BASE = ((cfg.site_name || "gallery").toLowerCase().replace(/[^a-z0-9]+/g, "-")
                   .replace(/^-+|-+$/g, "")) || "gallery";
  // ---- EX-PROTECT-GIFT: the picture is OFFERED, never dumped ----
  // The gift CEREMONY (his word 2026-07-08): a right-click on a work is answered by a gentle card
  // «like it? · a gift :)» and the picture is handed over only on a yes — never a blunt auto-download.
  // A won quiz ends in the SAME ceremony at better resolution. Rides the house breath (EX-ARRIVE);
  // Esc / click-outside close it.
  const giftCard = document.createElement("div");
  giftCard.id = "ex-gift-card";
  giftCard.setAttribute("role", "dialog");
  giftCard.setAttribute("aria-modal", "true");
  giftCard.hidden = true;
  giftCard.innerHTML =
    '<div class="gift-inner">' +
      '<img class="gift-thumb" alt="">' +
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
    return name || (DL_BASE + "-" + ((src.split("/").pop() || "photo").split("?")[0]));
  }
  function rawDownload(src, name) {
    try {
      const a = document.createElement("a");
      a.href = src; a.download = giftName(src, name);
      document.body.appendChild(a); a.click(); a.remove();
    } catch (e) { /* the walk loses nothing if a browser refuses the save */ }
  }
  // EX-PROTECT-RES (INV-56): the SHOWN image is CLEAN; the site-host mark is stamped ONLY on a TAKEN
  // copy, HERE, client-side via canvas. The quiz prize already wears its own baked mark (preMarked)
  // and goes out raw. A browser that refuses the canvas still gets the clean file (never blocked).
  function giftDownload(src, name, preMarked, workId) {
    // a gift file actually leaves for the visitor's device — the beat rides BESIDE the download, its
    // kind from the closed pair: the quiz prize goes out preMarked, a right-click grab is signed here
    pulse("gift_download", workId, { gift_kind: preMarked ? "quiz_prize" : "grab" });
    if (preMarked) { rawDownload(src, name); return; }
    const host = ROOT_URL.replace(/^https?:\/\//, "").replace(/\/$/, "");
    const im = new Image();
    im.onload = () => {
      try {
        const cv = document.createElement("canvas");
        cv.width = im.naturalWidth || im.width; cv.height = im.naturalHeight || im.height;
        const ctx = cv.getContext("2d");
        ctx.drawImage(im, 0, 0);
        const fs = Math.max(13, Math.round(cv.width * 0.022)), pad = Math.round(fs * 0.9);
        ctx.font = "600 " + fs + "px -apple-system,'Segoe UI',sans-serif";
        ctx.textAlign = "right"; ctx.textBaseline = "alphabetic";
        ctx.fillStyle = "rgba(0,0,0,.34)"; ctx.fillText(host, cv.width - pad + 1, cv.height - pad + 1);
        ctx.fillStyle = "rgba(235,231,222,.66)"; ctx.fillText(host, cv.width - pad, cv.height - pad);
        cv.toBlob((blob) => {
          if (!blob) { rawDownload(src, name); return; }
          const url = URL.createObjectURL(blob);
          const a = document.createElement("a");
          a.href = url; a.download = giftName(src, name);
          document.body.appendChild(a); a.click(); a.remove();
          setTimeout(() => URL.revokeObjectURL(url), 5000);
        }, "image/jpeg", 0.92);
      } catch (e) { rawDownload(src, name); }
    };
    im.onerror = () => rawDownload(src, name);
    im.src = src;
  }
  // onYes (optional): called when the visitor says yes, BEFORE closeGift — used by the quiz-win path
  // to stamp the "gift" stage (EX-QUIZ-FLOW / INV-69) WITHOUT touching the shared ceremony behaviour.
  function openGift(src, name, preMarked, onYes, workId) {
    const T = (greetLang() || { t: {} }).t;
    giftCard.querySelector(".gift-thumb").src = src;
    giftCard.querySelector(".gift-ask").textContent = T.gift_ask || "like it?";
    const yes = giftCard.querySelector(".gift-yes");
    yes.textContent = T.gift_yes || "a gift :)";
    giftCard.querySelector(".gift-no").textContent = T.gift_no || "not now";
    giftCard.querySelector(".gift-line").textContent = enjoyLine();   // «enjoy · example.com»
    giftCard.querySelector(".gift-buy").textContent = T.gift_buy || "";
    yes.onclick = () => { giftDownload(src, name, preMarked, workId); if (onYes) onYes(); closeGift(); };
    giftCard.hidden = false; giftOpen = true;
    faceSync();                                        // the gift card is a face — arm the rest + guard (EX-CHROME)
    requestAnimationFrame(() => giftCard.classList.add("show"));       // EX-ARRIVE breath
  }
  function closeGift() {
    if (!giftOpen) return;
    giftCard.classList.remove("show");
    setTimeout(() => { giftCard.hidden = true; }, Math.round(350 * TEMPO));
    giftOpen = false;
    faceSync();                                        // the gift card left (EX-CHROME)
    recentreUnder();                                   // the last face leaves (EX-COMPOSE)
  }
  giftCard.querySelector(".gift-no").addEventListener("click", closeGift);
  giftCard.addEventListener("click", (ev) => { if (!ev.target.closest(".gift-inner")) closeGift(); });
  addEventListener("keydown", (ev) => { if (ev.key === "Escape" && giftOpen) closeGift(); });

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
  zoom.hidden = true;
  // The zoom holds the minimum on screen (INV-77): only the picture and a single CLOSE in the free
  // TOP-LEFT corner. The ambient player retracts while the zoom stands (body.ex-zoom, like every covering
  // face), and the zoom carries no share of its own — a visitor shares a work from the walk itself.
  zoom.innerHTML = '<button type="button" class="exz-btn exz-close" aria-label="закрыть">&times;</button>'
                 + '<div class="exz-stage"><img class="exz-img" alt=""></div>';
  document.body.appendChild(zoom);
  let zoomOpen = false, zScale = 1, zPinch = 0, zStartS = 1;
  // The way OUT mirrors the way IN (INV-82): the picture flies UP from its place into the layer on open
  // and back DOWN to that place on close. The FLIP rides a WRAPPER (.exz-stage) so the pinch keeps the
  // .exz-img's own transform (INV-81 — the live two-touch distance stays the sole scale authority); the
  // stage carries the entry/exit position+scale, the img carries the pinch. zSrcEl is the tapped picture,
  // re-measured on close so a rotation under the zoom lands the shrink on its fresh place (INV-82).
  let zSrcEl = null, zLastEl = null, zDismiss = 0;      // zLastEl survives close so a Forward step reopens (INV-83)
  const DISMISS_T = 0.82;      // release below this raw pinch-in ratio at 1× dismisses the layer (INV-82)
  // once zoomed past 1×, a one-finger drag PANS the enlarged picture. zTx/zTy are the pan offset in
  // screen px; zPan* hold the gesture's start. The offset is bounded to the picture's visible overflow
  // so the image can never be dragged past its own edge.
  let zTx = 0, zTy = 0, zPanning = false, zPanX = 0, zPanY = 0, zPanTx = 0, zPanTy = 0;
  // INV-85 desktop pinch (ctrl+wheel / Safari gesture*): accumulate into the SAME 1×–4× scale the touch
  // pinch drives. zDesk holds the below-1× dismiss accumulator (starts at 1, a continued pinch-IN eases
  // it down; at/below DISMISS_T it commits). zDismissing latches from the moment history.back() is asked
  // until closeZoom runs, so a rapid open→dismiss race can never pop the walk's own history step twice.
  let zDesk = 1, zDismissing = false;
  const zImg = zoom.querySelector(".exz-img");
  const zStage = zoom.querySelector(".exz-stage");
  const zReduce = matchMedia("(prefers-reduced-motion: reduce)");
  const zDist = (t) => Math.hypot(t[0].clientX - t[1].clientX, t[0].clientY - t[1].clientY);
  // Fly the stage between the source picture's place and its resting place. `back=false` opens
  // (source → rest), `back=true` closes (rest → source). The wall image is already cached, so the
  // layer's img lays out within one frame and its box is real to measure against. Reduced motion
  // swaps instantly. The pinch's own transform on .exz-img is never touched here (INV-81).
  function zFlip(rect, back, done) {
    if (!rect || zReduce.matches) {
      zStage.style.transition = "none"; zStage.style.transform = "";
      if (done) (back ? setTimeout(done, 0) : requestAnimationFrame(done));
      return;
    }
    const box = zImg.getBoundingClientRect();
    if (!box.width || !box.height) { zStage.style.transition = "none"; zStage.style.transform = ""; if (done) done(); return; }
    const s = rect.width / box.width;
    const dx = (rect.left + rect.width / 2) - (box.left + box.width / 2);
    const dy = (rect.top + rect.height / 2) - (box.top + box.height / 2);
    const atSource = "translate(" + dx.toFixed(1) + "px," + dy.toFixed(1) + "px) scale(" + s.toFixed(3) + ")";
    if (back) {                                     // resting → source: animate out, teardown after
      zStage.style.transition = "";
      requestAnimationFrame(() => { zStage.style.transform = atSource; });
      setTimeout(() => { if (done) done(); }, Math.round(300 * TEMPO));
    } else {                                        // source → resting: pin at source, then release to fly in
      zStage.style.transition = "none";
      zStage.style.transform = atSource;
      requestAnimationFrame(() => { zStage.style.transition = ""; zStage.style.transform = ""; if (done) done(); });
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
    zSrcEl = el; zLastEl = el;                          // the tapped picture — the FLIP's place, re-measured on close
    const rect = el.getBoundingClientRect();
    zImg.src = src; zImg.alt = el.alt || "";
    zScale = 1; zTx = 0; zTy = 0; zPanning = false; zDismiss = 0; zDesk = 1; zDismissing = false; zApply();
    zStage.style.transition = "none"; zStage.style.transform = "";
    zoom.hidden = false; zoomOpen = true;
    document.body.classList.add("ex-zoom");            // the player retracts too — the minimum on screen (INV-77)
    faceSync();                                        // the zoom is a face — freeze the page beneath (EX-CHROME)
    if (!(opts && opts.lay === false)) pushFace({ face: "zoom" });   // one honest road out (INV-83), above any standing face
    requestAnimationFrame(() => { zoom.classList.add("show"); zFlip(rect, false); });   // backdrop fades, picture flies in (INV-82)
  }
  // The single teardown, reached only through popstate (history.back): the ×, backdrop, Esc, and the
  // dismissing pinch all go through history.back so Back and they share one road (INV-83).
  function closeZoom() {
    if (!zoomOpen) return;
    zoomOpen = false; zDismissing = false; zDesk = 1;
    zScale = 1; zTx = 0; zTy = 0; zPanning = false; zDismiss = 0; zApply();   // the exit scales from 1×
    const rect = (zSrcEl && document.body.contains(zSrcEl)) ? zSrcEl.getBoundingClientRect() : null;  // fresh place (rotation, INV-82)
    zoom.classList.remove("show");                     // backdrop fades; the player returns to its rail at once
    document.body.classList.remove("ex-zoom");
    zFlip(rect, true, () => {                           // picture flies back DOWN to its place, then teardown
      zoom.hidden = true; zImg.removeAttribute("src");
      zStage.style.transition = "none"; zStage.style.transform = "";
      zSrcEl = null;
    });
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
      const raw = zStartS * (zDist(e.touches) / zPinch);
      if (raw < 1 && zScale <= 1.001 && zStartS <= 1.03) {   // at 1×, pinching further IN previews the dismiss (INV-82)
        zDismiss = raw;
        const shrink = 1 - (1 - Math.max(0.5, raw)) * 0.45;  // resistance — the picture eases toward its place
        zStage.style.transition = "none";
        zStage.style.transform = "scale(" + shrink.toFixed(3) + ")";
      } else {
        if (zDismiss) { zDismiss = 0; zStage.style.transition = "none"; zStage.style.transform = ""; }
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
    if (e.touches.length < 2) zPinch = 0;
    if (e.touches.length === 0) zPanning = false;
    if (zDismiss) {                                    // released mid dismiss-pinch (INV-82)
      if (zDismiss < DISMISS_T && e.touches.length === 0) { history.back(); return; }   // commit → close through history (INV-83)
      zDismiss = 0; zStage.style.transition = ""; zStage.style.transform = "";           // cancel → ease back to 1×
    }
    if (zScale <= 1.03) { zScale = 1; zTx = 0; zTy = 0; zApply(); }   // a near-1 release settles flat + centred
  }, { passive: true });
  // Every way out is the same road (INV-83): the ×, a backdrop tap, and Esc all step history BACK, and
  // the popstate handler runs the one closeZoom — so the browser's own Back button closes the zoom too.
  const zoomBack = () => { if (zoomOpen) history.back(); };
  zoom.querySelector(".exz-close").addEventListener("click", zoomBack);
  zoom.addEventListener("click", (e) => { if (e.target === zoom) zoomBack(); });   // tap the backdrop
  addEventListener("keydown", (e) => { if (e.key === "Escape" && zoomOpen) zoomBack(); });
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
  // resolved picture, a pinch-IN past the ~0.82× dismiss threshold DISMISSES through the one history step.
  const ZOOM_WHEEL_STEP = 0.0025;                        // scale change per |deltaY| unit of a ctrl+wheel / pinch
  function pinchWheel(e) {
    const dScale = -e.deltaY * ZOOM_WHEEL_STEP;          // OUT (deltaY<0) → +, IN (deltaY>0) → −
    if (!zoomOpen) {
      if (dScale <= 0) return;                           // a pinch-IN with nothing open opens nothing (INV-81 mirror)
      const t = zoomTargetAt(e.clientX, e.clientY);
      if (!t) return;                                    // no picture resolves → nothing opens (browser zoom stays refused)
      openZoom(t);                                       // lays the one history step (INV-83) — the dismiss road
      if (!zoomOpen) return;
      zDesk = 1; zScale = Math.min(4, 1 + dScale); zApply();
      return;
    }
    const ns = zScale + dScale;
    if (ns < 1) {                                        // at/into 1× a continued pinch-IN previews the dismiss (INV-82)
      zScale = 1; zTx = 0; zTy = 0; zApply();
      zDesk = (zDesk < 1 ? zDesk : 1) + (ns - 1);
      if (zDesk <= DISMISS_T && !zDismissing) { zDismissing = true; zDesk = 1; history.back(); }  // commit through the one road (INV-83)
      return;
    }
    zDesk = 1;
    zScale = Math.min(4, ns); zClampPan(); zApply();
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

  function onGrab(ev) {                                    // ONE delegated listener per kind, O(1)
    const img = ev.target.closest && ev.target.closest(".exh-frame img.work");
    if (!img) return;                                      // only the hung work; chrome is left alone
    ev.preventDefault();                                   // the raw save / drag ghost never fires
    // DESKTOP right-click → the gift ceremony; TOUCH (or a drag) → just the gracious line, no download
    if (ev.type === "contextmenu" && !matchMedia("(pointer: coarse)").matches) {
      const fr = img.closest(".exh-frame");            // the grabbed work — gift_kind=grab (EX-PULSE)
      openGift(img.currentSrc || img.getAttribute("src") || img.src, undefined, undefined, undefined,
               fr && fr.dataset.id);                   // OFFER, never dump
    } else {
      toast(enjoyLine());                                   // rides the breath, leaves by itself
    }
  }
  stage.addEventListener("contextmenu", onGrab);
  stage.addEventListener("dragstart", onGrab);
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
    const target = gStart * (ev.scale || 1);
    if (target < 1) {                                    // pinch-IN past 1× → preview / commit the dismiss (INV-82)
      zScale = 1; zTx = 0; zTy = 0; zApply();
      zDesk = target;
      if (zDesk <= DISMISS_T && !zDismissing) { zDismissing = true; zDesk = 1; history.back(); }
      return;
    }
    zDesk = 1; zScale = Math.min(4, target); zClampPan(); zApply();
  }
  function onGestureEnd(ev) {
    ev.preventDefault();
    if (!TOUCHY && zoomOpen && zScale <= 1.03) { zScale = 1; zTx = 0; zTy = 0; zApply(); }  // near-1 release settles flat
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
    return T.quiz_ask || "question?";
  }
  function quizChipHTML(id) {
    // a soft, slow one-time glint runs across the chip as it appears (EX-QUIZ-GLINT) — the
    // .ex-quiz-glint span is a pure-CSS sweep, born with the chip, plays once
    return `<button type="button" class="ex-quiz-chip" data-quiz="${id}">${quizLabel()}` +
      `<span class="ex-quiz-glint" aria-hidden="true"></span></button>`;
  }
  const PRIZE_DL = DL_BASE + "-wallpaper.jpg";           // the prize download name (site-slug, INV-28)

  const quizCard = document.createElement("div");
  quizCard.id = "ex-quiz-card";
  quizCard.setAttribute("role", "dialog");
  quizCard.setAttribute("aria-modal", "true");
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
      if (stored.prize) { openGift("/" + stored.prize, PRIZE_DL, true, undefined, id); return; }
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
    requestAnimationFrame(() => { quizCard.classList.add("show"); });
  }

  function quizCardClose() {
    if (!quizOpen) return;
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
      out.textContent = T.quiz_wrong || "not this time";
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
                   () => { quizStageUp("gift"); }, id);   // gift_kind=quiz_prize, the work (EX-PULSE)
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

  function frameHTML(id, n) {
    const w = byId[id];
    // EX-LADDER (INV-63): the responsive ladder rides the baked per-work `srcset` (640/960/1280,
    // written by the display-cap bake); the base `src` stays the untouched fallback. No cap ⇒ no
    // srcset key ⇒ the img is byte-identical to a ladder-less walk.
    const ladder = w.srcset ? ` srcset="${w.srcset}" sizes="${data.walk_sizes || "88vw"}"` : "";
    return (
      `<section class="exh-frame" data-id="${w.id}" data-n="${n}">` +
        `<img class="work" loading="lazy" src="${w.img}"${ladder} alt="">` +
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
    const moreLabel = (FT.more || "ещё {n}").replace("{n}", String(UNFOLD));
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
    const k = Math.min(stops.length - 1, Math.max(0, nearestStop(stops, base) + dir));
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
      }
      turnTargetEl = null;
    }, 120);
  }
  addEventListener("resize", () => { if (walkOwnsInput() || gliding || zoomOpen) onViewportTurn(); });
  addEventListener("orientationchange", onViewportTurn);   // a rotation is its OWN beat (INV-86), not merely a resize
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
  let wheelLock = false;
  let wheelIdle = null;
  let wheelPeak = 0;                                   // the live gesture's PEAK |deltaY| — the force→speed input
  let wheelMode = null;                                // "walk" (plain wheel) | "zoom" (ctrl+wheel) — latched per burst
  let wheelQuiet = false;                              // the burst has decayed to its floor after a real peak — a re-swipe gap
  // INV-84 re-arm (thread the two bugs): one CONTINUOUS swipe advances ONE frame — its own ramp-in and
  // its monotonically-decaying tail never re-step. A DELIBERATE second swipe (a genuine re-acceleration)
  // must still step. The tell is a real quiet gap: after a swipe has actually peaked (wheelPeak past
  // RESWIPE_PEAK), the stream decays to a low floor (RESWIPE_FLOOR) — THEN a rise back above RESWIPE_RISE
  // is a new gesture. A single swipe's ramp-in can't trip it (wheelPeak isn't past its own peak yet, and
  // quiet is only armed on the FALLING side); its decaying tail can't (it never rises). Both thresholds
  // sit in the dead band between one swipe's tail (falls to ~2–6, never climbs) and a real re-swipe's
  // rise (climbs back past ~20) — see test_glide rows 10 (one frame) & 11 (two frames).
  const RESWIPE_PEAK = 20;                             // a burst must have crested this to count as a real swipe worth re-arming after
  const RESWIPE_FLOOR = 12;                            // |deltaY| at/below (after that crest) → the stream has gone quiet
  const RESWIPE_RISE = 20;                             // a rise back to/above this out of the quiet → a deliberate NEW swipe
  if (!TOUCHY) {
    addEventListener("wheel", (e) => {
      // The burst boundary and the MEANING are both fixed at the first event: a mouse notch is one
      // event, a trackpad swipe a decaying burst — an idle timer clears the lock only once all motion
      // stops, so the NEXT gesture is genuinely fresh. The meaning is latched here and held for the
      // whole coalesced burst, so a ctrl gained or lost mid-burst never flips it (EX-PROTECT/INV-85).
      const fresh = !wheelLock;
      clearTimeout(wheelIdle);
      wheelIdle = setTimeout(() => { wheelLock = false; wheelPeak = 0; wheelMode = null; }, 150);
      if (fresh) { wheelLock = true; wheelMode = e.ctrlKey ? "zoom" : "walk"; wheelPeak = 0; wheelQuiet = false; }
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
      // INV-84: one continuous burst = EXACTLY one frame. Its rising ramp-in and its decaying tail only
      // feed the single glide's SPEED (the sharper the burst, the shorter its one glide) — they never
      // re-step. A DELIBERATE second swipe DOES step: it shows up as a re-acceleration OUT of a genuine
      // quiet gap (the first swipe's tail died to a low floor, then a fresh rise). The old code re-armed
      // on any rise > peak×1.3 and flew through the gallery on one gentle swipe's ramp-in; this arms
      // `wheelQuiet` only on the FALLING side of a real crest, so a ramp-in can never trip it.
      if (!fresh) {
        if (wheelPeak >= RESWIPE_PEAK && mag <= RESWIPE_FLOOR) wheelQuiet = true;  // the burst has gone quiet
        if (wheelQuiet && mag >= RESWIPE_RISE) {          // ...then re-accelerates → a genuinely new swipe, re-armed
          wheelQuiet = false; wheelPeak = mag;
          stepFrame(e.deltaY > 0 ? 1 : -1, mag);
          return;
        }
        if (mag > wheelPeak) {
          wheelPeak = mag;
          if (gliding && glideGoal != null) glideToFrame(glideGoal, wheelPeak);
        } else wheelPeak = Math.max(mag, wheelPeak * 0.95);
        return;
      }
      wheelPeak = mag; wheelQuiet = false;
      stepFrame(e.deltaY > 0 ? 1 : -1, mag);
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
            if (Math.abs(dx) + Math.abs(dy) >= 4)      // the first ~4px pick the axis — verdict held to lift
              fDecided = !!(e.target && e.target.closest && e.target.closest(FACE_SEL))
                         && faceConsumes(e.target, Math.abs(dx) > Math.abs(dy));
            else { e.preventDefault(); return; }       // undecided yet — eat, the walk never gets a first pixel
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

  function renderHang() {
    tlog("hang");
    recomputeQuizChoice();                               // EX-QUIZ-ONCE (INV-66): pick ONE eligible work
    document.documentElement.classList.add("ex-walk");   // the walk's face (geometry in CSS)
    stage.innerHTML = "";
    appendFrames(order.slice(0, shown), 1);
    scrollTo(0, 0);
    if (faceStands()) guardHold = 0;                     // the walk builds under the ceremony's veil — hold its top (EX-CHROME)
    tellStory();                                         // the voice, if the story is on (set-guarded)
  }

  // ---- EX-SERIES (INV-46): the side room — theme and variations, a look ASIDE --------
  // A FACE over the walk: opening lays ONE history step; the page locks beneath (the
  // threshold's own law); chip, Esc and Back all land the guest on the exact frame left.
  const side = document.createElement("div");
  side.id = "ex-side";
  side.hidden = true;
  side.innerHTML = '<button type="button" class="exs-back"></button>' +
                   '<div class="exs-stage" id="exs-stage"></div>';
  document.body.appendChild(side);
  let sideOpen = false;
  function openSide(idx, laystep) {
    const S = SERIES[idx];
    if (!S || sideOpen || busy) return;
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
  function dressSide(S, idx, laystep) {
    const st = side.querySelector("#exs-stage");
    st.className = "exs-stage " + S.variant;           // the series' own character picks the face
    st.innerHTML = "";
    S.members.forEach((id, i) => {
      const w = byId[id];
      if (!w) return;
      if (S.variant === "lane") {
        const im = new Image();
        im.src = w.img;
        st.appendChild(im);
        return;
      }
      const p = document.createElement("div");         // the polaroid table
      p.className = "exs-print";
      p.style.left = (8 + (i % 5) * 17 + (i * 7) % 5) + "%";
      p.style.top = (12 + Math.floor(i / 5) * 26 + (i * 11) % 7) + "%";
      p.style.setProperty("--rot", ((((i * 37) % 13) - 6)) + "deg");
      p.innerHTML = '<img src="' + w.img + '" alt="">';
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
    const T = (greetLang() || { t: {} }).t;
    side.querySelector(".exs-back").textContent = T.room_back || "← комната";
    side.hidden = false;
    document.body.classList.add("ex-side");            // the lock law, reused (EX-DOOR-2f)
    if (laystep !== false) pushFace({ face: "series", ser: idx });
    pulse("series_open", focusedId);                   // the work whose series opened (EX-PULSE registry)
  }
  function closeSide(soft) {
    if (!sideOpen) return;
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
          const y = restingEl ? frameCenter(restingEl) : stops[nearestStop(stops, scrollY)];
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
    if (ev.key === "Escape" && sideOpen) history.back();
  });
  // EX-COMPOSE: a print lifted to the light re-centres to the live viewport — a centre measured
  // before a rotation never survives it (the delta rides ON TOP of the standing --cx/--cy).
  let sdrsz = null;
  addEventListener("resize", () => {
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
  });

  // ---- the walk TRACKS its place (INV-32c — the law outlived the ↗, its first carrier):
  // the io callback above writes the per-tab marker per frame in view; any return within
  // the tab (reload, the work page's plain link, Back) restores it
  function restorePlace() {
    let m = null;
    try { m = JSON.parse(sessionStorage.getItem(PLACE_KEY) || "null"); } catch (e) {}
    try { sessionStorage.removeItem(PLACE_KEY); } catch (e) {}   // one-shot
    if (!m || m.v !== VER) return;                     // stale/foreign marker → the top, never an error
    const f = stage.querySelector('.exh-frame[data-id="' + m.id + '"]');
    if (f) scrollTo(0, frameCenter(f));               // centered in the LIVE viewport (EX-GLIDE)
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
    pulse("share_arrive", hid);
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
    if (f) scrollTo(0, frameCenter(f));               // instant, centered in the LIVE viewport
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
  const prior = (history.state && history.state.ex) || null;
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

  // ---- EX-I18N (INV-42): the museum speaks ANY language — after first paint ----
  // A locale outside the baked seven meets the fallback INSTANTLY; the site then quietly asks
  // its own worker for that locale's set (once per language-version, ever), keeps a browser
  // copy, and the standing surfaces re-speak without a jump. A dead worker changes nothing.
  function respeak() {
    const L = greetLang();
    if (!L) return;
    const T = L.t;
    if (atDoor) {
      door.setAttribute("dir", T.dir === "rtl" ? "rtl" : "ltr");
      door.setAttribute("lang", L.code);
      door.querySelector(".exd-ask").textContent = T.ask || "что ближе сейчас?";
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
    const fin = document.getElementById("exh-fin");
    if (fin) {
      fin.setAttribute("lang", L.code);
      fin.setAttribute("dir", T.dir === "rtl" ? "rtl" : "ltr");
      const u = fin.querySelector("#ex-unfold");
      const b = fin.querySelector("#ex-return");
      const q = fin.querySelector(".q");
      if (q) q.textContent = u ? (T.q_more || q.textContent) : (T.q_spent || q.textContent);
      if (u) u.textContent = (T.more || "ещё {n}").replace("{n}", String(UNFOLD)) + " ↓";
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
    window.__exSeen = (id) => {
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
  function requestSet(code) {                          // cached-or-fetch, the ONE road (EX-LANG)
    if (!I18N_ON) return;
    const CK = "ex.i18n." + VER + "." + code;
    let cached = null;
    try { cached = JSON.parse(localStorage.getItem(CK) || "null"); } catch (e) {}
    if (cached) { applySet(code, cached); return; }
    fetch("/api/i18n?lang=" + code + "&v=" + encodeURIComponent(VER))
      .then((r) => (r.ok ? r.json() : null))
      .then((set) => {
        if (!set) return;
        try { localStorage.setItem(CK, JSON.stringify(set)); } catch (e) {}
        applySet(code, set);
      })
      .catch(() => {});                                // a dead worker changes nothing
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

    const browserCode = (navigator.language || "").toLowerCase().slice(0, 2);
    const codes = Object.keys(GREET.langs).slice();
    if (I18N_ON && /^[a-z]{2,3}$/.test(browserCode)
        && !GREET.langs[(GREET.aliases || {})[browserCode] || browserCode]
        && codes.indexOf(browserCode) < 0) {
      codes.push(browserCode);                         // the guest's own outsider tongue
    }
    const markOf = () => {
      const c = viewerLang();
      return ((GREET.aliases || {})[c] || c).toUpperCase().slice(0, 2) || "EN";
    };
    const redraw = () => {
      cur.textContent = markOf();
      list.querySelectorAll(".exl-item").forEach((b) =>
        b.classList.toggle("cur", b.dataset.lang === viewerLang()));
    };
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
        // reports `other`, never a raw locale string on the wire — the ladder stays closed (INV-1)
        pulse("lang_pick", null, { lang: baked ? known : "other" });
        if (baked) respeak();                          // a baked tongue answers at once
        else requestSet(c);                            // an outsider rides the one layer
        redraw();
      });
      list.appendChild(b);
    });
    cur.addEventListener("click", (ev) => {
      ev.stopPropagation();
      list.hidden ? listOpen() : listClose();
    });
    door.addEventListener("click", () => { listClose(); });
    redraw();
  }

  // ---- EX-SOUND (INV-48): the ambient loop walks beside the guest ----------------------------
  // OFF by default — a fresh visit is silent and the audio is fetched ONLY on the first turn-on
  // (the perf fence), never on cold load. Gapless via Web Audio: decode into a looping
  // AudioBufferSourceNode. Fade in ~1.2s ×tempo, out ~0.8s and on leaving / unload (pagehide,
  // best-effort). Volume default 0.3 with a ≥44px touch-friendly slider. The on/off + volume
  // persist in ex.sound (versioned); a return ON ARMS on the first gesture (autoplay is blocked
  // without one) rather than fetching on cold load. A missing/failed file fails SILENT (INV-1).
  // Two beats ride the EXISTING EX-PULSE wire: sound_on / sound_off (no new analytics plumbing).
  // EX-SOUND-PAUSE (INV-52): off is a PAUSE that holds the moment, on RESUMES from it.
  // Config keys (config.json → exhibition): sound_url (audio file, empty = player hidden),
  // sound_credit.artist / sound_credit.title / sound_credit.url (the credit tray text + link).
  (function sound() {
    const SND_URL = (EX.sound_url || "").trim();
    if (!SND_URL) return;                                // no audio configured — player stays hidden
    const CREDIT = EX.sound_credit || {};
    const FADE_IN = 1.2, FADE_OUT = 0.8, DEFAULT_VOL = 0.3;

    const box = document.createElement("div");
    box.id = "ex-sound";
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
          ' aria-label="volume">' +
      '</div>' +
      '<button class="exsnd-btn" type="button" aria-pressed="false"' +
        ' aria-label="sound"><span class="exsnd-eq"><i></i><i></i><i></i></span></button>';
    document.body.appendChild(box);
    requestAnimationFrame(() => box.classList.add("show"));   // EX-ARRIVE: arrives on the breath

    const btn = box.querySelector(".exsnd-btn");
    const vol = box.querySelector(".exsnd-vol");

    let ctx = null, buffer = null, source = null, gain = null;
    let target = DEFAULT_VOL, desired = false, playing = false, armed = false;
    let ready = false, loading = false, fetched = false;
    // EX-SOUND-PAUSE (INV-52): off is a PAUSE that holds the moment, on RESUMES from it — never a
    // restart. `pausedOffset` is seconds into the track; `startedAt`/`startedFrom` clock the running
    // source so a stop can compute where it reached (a looping buffer has no readable playhead).
    let pausedOffset = 0, startedAt = 0, startedFrom = 0;

    // the remembered choice (versioned like the walk)
    let pref = null;
    try { pref = JSON.parse(localStorage.getItem(SND_KEY) || "null"); } catch (e) {}
    if (!pref || pref.v !== VER) pref = null;
    if (pref && Number.isFinite(+pref.vol)) target = Math.min(1, Math.max(0, +pref.vol));
    vol.value = String(target);

    function persist() {
      try {
        localStorage.setItem(SND_KEY, JSON.stringify({ v: VER, on: desired, vol: target }));
      } catch (e) {}
    }

    async function prepare() {
      if (ready || loading) return ready;
      loading = true;
      try {
        ctx = ctx || new (window.AudioContext || window.webkitAudioContext)();
        gain = ctx.createGain(); gain.gain.value = 0; gain.connect(ctx.destination);
        fetched = true;
        const bytes = await fetch(SND_URL).then((r) => {
          if (!r.ok) throw new Error("no audio"); return r.arrayBuffer();
        });
        buffer = await ctx.decodeAudioData(bytes);
        ready = true;
      } catch (e) { ready = false; }
      loading = false;
      return ready;
    }

    function arm() {
      if (armed || playing) return;
      armed = true;
      ["pointerdown", "touchstart", "scroll", "keydown"].forEach((e) =>
        addEventListener(e, onGesture, { once: true, passive: true, capture: true }));
    }
    function disarm() {
      if (!armed) return;
      armed = false;
      ["pointerdown", "touchstart", "scroll", "keydown"].forEach((e) =>
        removeEventListener(e, onGesture, { capture: true }));
    }
    function onGesture() { disarm(); if (desired) start(); }

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
      const ok = await prepare();
      if (!desired) return;
      if (!ok) { box.classList.remove("playing"); return; }
      if (ctx.state === "suspended") { try { await ctx.resume(); } catch (e) {} }
      if (!desired) return;
      if (ctx.state === "suspended") { arm(); return; }
      if (source) return;
      source = ctx.createBufferSource();
      source.buffer = buffer; source.loop = true;
      source.connect(gain);
      startedFrom = pausedOffset % buffer.duration;    // RESUME where the pause held — not the top
      source.start(0, startedFrom);
      startedAt = ctx.currentTime;
      const now = ctx.currentTime;
      gain.gain.cancelScheduledValues(now);
      gain.gain.setValueAtTime(Math.max(0.0001, gain.gain.value), now);
      gain.gain.linearRampToValueAtTime(target, now + FADE_IN * TEMPO);
      playing = true; armed = false;
      box.classList.add("playing");
    }

    function stop() {
      disarm();
      if (source && ctx) {
        const now = ctx.currentTime, s = source;
        if (buffer) pausedOffset = (startedFrom + (now - startedAt)) % buffer.duration;
        gain.gain.cancelScheduledValues(now);
        gain.gain.setValueAtTime(gain.gain.value, now);
        gain.gain.linearRampToValueAtTime(0, now + FADE_OUT * TEMPO);
        setTimeout(() => { try { s.stop(); } catch (e) {} },
          Math.round(FADE_OUT * TEMPO * 1000) + 80);
        source = null;
      }
      playing = false;
      box.classList.remove("playing");
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
    addEventListener("pagehide", () => { if (playing) stop(); });

    // a return visit with the pref ON: ARM on the first gesture — never a cold-load fetch
    if (pref && pref.on) { desired = true; btn.setAttribute("aria-pressed", "true"); arm(); }

    // the player's own reachable surface, for the suite
    try {
      window.EXSound = { state: () => ({ desired, playing, armed, ready, fetched, loading,
                                         pausedOffset }),
                         url: SND_URL };
    } catch (e) {}
  })();
})();
