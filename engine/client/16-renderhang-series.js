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
  side.setAttribute("role", "dialog");                                                          // N7-A11Y (B-role): the room is a modal layer, one kind with the other three
  side.setAttribute("aria-modal", "true");
  side.setAttribute("aria-label", ((greetLang() || { t: {} }).t.a11y_room) || A11Y_ROOM_EN);   // N7-A11Y (C4/C5)
  side.hidden = true;
  side.innerHTML = '<button type="button" class="exs-back"></button>' +
                   '<div class="exs-stage" id="exs-stage"></div>';
  document.body.appendChild(side);
  let sideOpen = false;
  let sideOpener = null;            // N7-A11Y (INV-102, B1): the element that opened the room — focus returns here on close
  let laneTouchOff = null;          // the CURRENT dress's own lane touchstart handler (INV-88) —
                                     // removed at the top of every dressSide so it never piles up
                                     // across reopens of the reused #exs-stage
  function openSide(idx, laystep) {
    const S = SERIES[idx];
    if (!S || sideOpen || busy) return;
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
    S.members.forEach((id, i) => {
      const w = byId[id];
      if (!w) return;
      if (S.variant === "lane") {
        const im = new Image();
        im.src = w.img;
        im.alt = workDesc(w.id);                         // N7-A11Y (INV-102, C6): the lane photograph speaks
        im.dataset.id = w.id;                            // EX-PICSTAT: the room look reads its pic
        im.tabIndex = 0;                                 // N7-A11Y (INV-102, B4): the lane photograph is keyboard-reachable (the lane scrolls by arrow key — the side-level handler below)
        st.appendChild(im);
        if (im.decode) decodes.push(im.decode().catch(() => {}));   // N7-A11Y (INV-102, D3): feature-guard like the three siblings (06/07/12) — no bare decode where it is unsupported
        return;
      }
      const p = document.createElement("div");         // the polaroid table
      p.className = "exs-print";
      p.dataset.id = w.id;                             // EX-PICSTAT: the room look reads its pic
      p.style.left = (8 + (i % 5) * 17 + (i * 7) % 5) + "%";
      p.style.top = (12 + Math.floor(i / 5) * 26 + (i * 11) % 7) + "%";
      p.style.setProperty("--rot", ((((i * 37) % 13) - 6)) + "deg");
      p.innerHTML = '<img src="' + w.img + '" alt="">';
      const pim = p.querySelector("img");                // N7-A11Y (INV-102, C6): the polaroid speaks
      if (pim) pim.alt = workDesc(w.id);
      // N7-A11Y (INV-102, B4): the polaroid is a keyboard button — focusable, named, opened by Enter/Space
      p.tabIndex = 0;
      p.setAttribute("role", "button");
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

