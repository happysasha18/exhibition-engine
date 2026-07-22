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
    if (window.__@@NS@@Seen) window.__@@NS@@Seen(w.id);      // the coat-check report (EX-MEMORY)
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
    // N7-A11Y (INV-102): announce this work's caption to the polite region — a walk step REPLACES it,
    // so a screen reader hears the current work rather than a pile-up (the story portions append below).
    announceCaption([(w.title || untitledWord), (w.sec || ""), (w.place || "")]
      .filter((s) => s && String(s).trim()).join(" · "));
    fillTold();                                        // the narrator's line for this work, if spoken
    storyPreAsk();                                     // near the fork, the NEXT portion asks ahead (INV-89)
    capSettle(x.target.querySelector("img.work"));     // EX-CAPTION (INV-97): seat the caption in the free zone at the frame's settle
  }), { threshold: 0.55 });

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

