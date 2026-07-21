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
      if (wasWalk) { pulse("walk_exit"); noteExit(); }   // EX-RETURN/INV-78: a Back-leave counts like the exit control
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

