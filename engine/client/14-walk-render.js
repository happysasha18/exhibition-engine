  function frameHTML(id, n) {
    const w = byId[id];
    // EX-LADDER (INV-63): the ladder itself lives in one place (ladderAttr); the walk hands its
    // own box — CSS max-width:88vw. The base `src` stays the untouched fallback.
    const ladder = ladderAttr(w, ladderSizes("walk"));
    // N7-A11Y (INV-102, C1/C3): the frame img speaks the work's own description (never alt=""), and the
    // frame names itself a photograph within the walk (role + roledescription + the same accessible name).
    const desc = escAttr(workDesc(w.id));
    const photoWord = escAttr(((greetLang() || { t: {} }).t.a11y_photo) || A11Y_PHOTO_EN);
    return (
      `<section class="exh-frame" data-id="${w.id}" data-n="${n}" tabindex="0"` +
        ` role="group" aria-roledescription="${photoWord}" aria-label="${desc}"` +
        // N7-A11Y (INV-102, B2/B3): the frame ANNOUNCES the two keys it answers — `z` looks closer, `y` opens the gift
        ` aria-keyshortcuts="z y">` +
        `<img class="work" loading="lazy" src="${w.img}"${ladder} alt="${desc}">` +
      "</section>"
    );
  }

  function appendFrames(slice, startN) {
    // The first selection is known here, before its first photograph is even drawn.  Start BOTH
    // pieces of the crossing vocabulary now: the record wave and the collection-wide composer.
    // Opening the composer only after the first landing made the first gesture of every visit a
    // guaranteed plain glide, however fast the network and however rich the pair.  The composer
    // needs its fixed constants, not a record already in the map; the two records arrive in parallel
    // while the visitor is choosing whether to move on.
    passComposerOpen();
    passRecordsAskFor(slice);
    passOpen();
    document.getElementById("exh-fin")?.remove();
    const html = slice.map((id, i) => frameHTML(id, startN + i)).join("");
    stage.insertAdjacentHTML("beforeend", html);
    stage.querySelectorAll(".exh-frame:not(.observed)").forEach((f) => {
      f.classList.add("observed"); io.observe(f); condWatch(f);   // EX-CONDUCTOR (S-39) watches too
    });
    // the walk's closing screen: onward while the budget lasts, the door ALWAYS (INV-29/30/31).
    // Its copy speaks the visitor's language like the door does (his word 2026-07-06: the exit
    // is «выход», localized — never «к двери»); built-ins only carry a missing cache.
    const spent = spentUnfolds() >= MAXU || shown >= order.length;
    const FL = greetLang();
    const FT = FL ? FL.t : {};
    const moreLabel = (FT.more || MORE_EN).replace("{n}", String(UNFOLD));
    // EX-ABOUT (INV-103): the closing screen is the one place the exhibition already offers a
    // choice of where to go, so the door to the about page stands here — in the VISITOR's own
    // tongue when that tongue has a page, else at the fallback page every bundle bakes first.
    // The baked signature below carries no about link, so this screen shows exactly one door.
    const AB = data.about;
    const aboutWord = ((FT.about || "") + "").trim();
    const aboutHref = !AB ? "" :
      (FL && AB.langs.indexOf(FL.code) >= 0 && FL.code !== AB.fallback)
        ? "/about/" + FL.code : "/about";
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
      (aboutHref && aboutWord ? `<a class="about" id="ex-about" href="${aboutHref}">${aboutWord}</a>` : "") +
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
