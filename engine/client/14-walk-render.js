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
    const moreLabel = (FT.more || MORE_EN).replace("{n}", String(UNFOLD));
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

