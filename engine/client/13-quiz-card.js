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
    // EX-QUIZ-COPY (INV-100): the chip's words ride the quiz_chip_copy arm — the reward-named arm
    // speaks the gift, the plain arm names only the act; either drops the bare «question?». The
    // arm is dealt in 03 (abArms); an absent registry falls to the plain copy. English source-
    // tongue fallbacks stand when a locale lacks the key (EX-I18N).
    const arm = (abArms && abArms.quiz_chip_copy) || null;
    if (arm === "place_prize") return T.quiz_ask_prize || "guess the place · win a wallpaper";
    return T.quiz_ask_place || "guess the place";
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

