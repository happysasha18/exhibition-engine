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
    try { localStorage.removeItem(LAST_KEY); } catch (e) {}     // the return-gap clock resets (EX-PULSE/INV-79 — forgetting is whole)
    try { localStorage.removeItem(EXITS_KEY); } catch (e) {}    // the exit counter resets (EX-RETURN/INV-78 — the farewell starts over)
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

