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
  function portionPending(id) {
    if (id == null) return false;
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
  function storyPortions(n) {                          // [[lo,hi], …] over order indices, the unfold's own beats
    const parts = [];
    const first = Math.min(SPREAD, n);
    if (first > 0) parts.push([0, first]);
    for (let s = first; s < n; ) { const e = Math.min(n, s + UNFOLD); parts.push([s, e]); s = e; }
    return parts;
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
      // N7-A11Y (INV-102 / F5): the arriving portion APPENDS to the caption-and-story region — earlier
      // portions stand, the caption above them stands, until the next walk step replaces the region.
      const portionText = data.lines
        .map((l) => (l && typeof l.line === "string") ? l.line : "").filter(Boolean).join(" ");
      if (portionText) announceStory(portionText);
      revealPortion();                                 // …then ONE coordinated reveal (EX-STORY-WAIT)
      done();
    }).catch(() => { askingPortions.delete(key); owed(); });   // a dead worker → re-ask shortly, then the portion stays owed
  }
  // tellStory re-asks every portion up to `shown` that is not yet told: the newly opened one on an
  // «ещё 5», plus any earlier portion still owed from a refusal (re-asked at this natural beat). A
  // told portion returns free from cache; an owed one waits for the next beat. Called at each beat —
  // the hang builds, an unfold grows the set, a return re-shows the walk.
  function tellStory() {
    if (!STORY_ON) return;
    for (const [lo, hi] of storyPortions(shown)) askPortion(lo, hi);
  }
  // EX-STORY-BEAT (INV-89): the voice stays ahead at the fork — as the focus comes within two
  // works of the spread's end, the NEXT portion (the very slice an «ещё 5» would open) is asked
  // ahead, gated on that proximity so intent pays for it. The portion keys dedupe, so the unfold's
  // own tellStory finds the plot in flight or served, never double-charged; when no next portion
  // exists (the arc spent, the unfolding retired) nothing is asked.
  function storyPreAsk() {
    if (!STORY_ON || focusedId == null) return;
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
    for (const k in STORYLINES) delete STORYLINES[k];
    storyVariant = null;
  }

