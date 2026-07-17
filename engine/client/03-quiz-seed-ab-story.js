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
  // the quiz arm is the frame's first rider (salt "quizarm", arms on/control — INV-62's split,
  // unchanged); null when the flag is off so nothing stamps the GA beats (INV-60)
  const quizArm = QUIZ_ON ? (abArms.quiz_arm || null) : null;
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
  try { window.@@NS_UPPER@@Quiz = { chosen: () => quizChosenId, arm: () => quizArm, token: QUIZ_TOKEN, _hash: quizHash }; } catch (e) {}
  const STORYLINES = Object.create(null);
  let storyVariant = null;          // the mode the served story reported — rides the GA beats (EX-STORY-AB)
  const toldPortions = new Set();   // portion keys whose plot has actually come back (told ONLY on a served plot)
  const askingPortions = new Set(); // portion keys with a request in flight (never double-ask the same portion)

