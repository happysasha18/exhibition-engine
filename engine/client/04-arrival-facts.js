  // ---- EX-PULSE/INV-79: the arrival's own facts — measured ONCE per load ------
  // Placed AFTER quizArm/storyVariant are initialized: pulse() reads those dimension vars, so an
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

