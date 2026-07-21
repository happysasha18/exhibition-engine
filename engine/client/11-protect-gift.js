  // ---- EX-PROTECT (INV-49): a grabbed work meets a GIFT, not the browser's raw save ----
  // A right-click / long-press (contextmenu) or a drag on a work is intercepted and answered by
  // the SAME toast the share line rides — a quiet localized «enjoy» + the site host, arriving on
  // the house breath (EX-ARRIVE). It is a gracious line, never a scold or an error.
  // (CSS `user-select:none` / `touch-action:pan-x pan-y` / `-webkit-touch-callout:none` on
  // img.work handle the soft layer; these listeners handle contextmenu + drag + pinch-zoom.)
  function enjoyLine() {
    const T = (greetLang() || { t: {} }).t;
    const host = ROOT_URL.replace(/^https?:\/\//, "");   // «example.com», appended in code
    const enjoy = T.enjoy || ENJOY_EN;                    // every line localizes through EX-I18N; the
                                                          // fallback is ENGLISH (source tongue), never Russian
    return enjoy + " · " + host;                          // never blank (EX-PROTECT empty/error facet)
  }
  // EX-PROTECT-RES (INV-56): the download filename base — the site's OWN HOST from config (INV-28),
  // never a hardcoded brand. A grabbed file is «<host>-<original>.jpg», so the picture carries the
  // gallery's domain wherever it lands (the same host the watermark stamps). The host's leading label
  // is taken (tlvphotos.com → tlvphotos), a plain slug, with a never-blank fallback.
  const DL_BASE = ((ROOT_URL.replace(/^https?:\/\//, "").split("/")[0].split(":")[0].split(".")[0])
                   .toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "")) || "gallery";
  // ---- EX-PROTECT-GIFT: the picture is OFFERED, never dumped ----
  // The gift CEREMONY (his word 2026-07-08): a right-click on a work is answered by a gentle card
  // «like it? · a gift :)» and the picture is handed over only on a yes — never a blunt auto-download.
  // A won quiz ends in the SAME ceremony at better resolution. Rides the house breath (EX-ARRIVE);
  // Esc / click-outside close it.
  const giftCard = document.createElement("div");
  giftCard.id = "ex-gift-card";
  giftCard.setAttribute("role", "dialog");
  giftCard.setAttribute("aria-modal", "true");
  // N7-A11Y (INV-102, C4/C5): the ceremony names itself to a screen reader (localized, EN fallback)
  giftCard.setAttribute("aria-label", ((greetLang() || { t: {} }).t.a11y_gift) || A11Y_GIFT_EN);
  giftCard.hidden = true;
  giftCard.innerHTML =
    '<div class="gift-inner">' +
      '<div class="gift-ask"></div>' +
      '<div class="gift-act">' +
        '<button type="button" class="gift-yes"></button>' +
        '<button type="button" class="gift-no"></button>' +
      '</div>' +
      '<div class="gift-line"></div>' +
      '<div class="gift-buy"></div>' +
    '</div>';
  document.body.appendChild(giftCard);
  let giftOpen = false;
  function giftName(src, name) {
    return name || (DL_BASE + "-" + ((src.split("/").pop() || "photo").split("?")[0]));
  }
  function rawDownload(src, name) {
    try {
      const a = document.createElement("a");
      a.href = src; a.download = giftName(src, name);
      document.body.appendChild(a); a.click(); a.remove();
    } catch (e) { /* the walk loses nothing if a browser refuses the save */ }
  }
  // EX-PROTECT-RES (INV-56): the SHOWN image is CLEAN; the site-host mark is stamped ONLY on a TAKEN
  // copy, HERE, client-side via canvas. The quiz prize already wears its own baked mark (preMarked)
  // and goes out raw. A browser that refuses the canvas still gets the clean file (never blocked).
  function giftDownload(src, name, preMarked, workId) {
    // a gift file actually leaves for the visitor's device — the beat rides BESIDE the download, its
    // kind from the closed pair: the quiz prize goes out preMarked, a right-click grab is signed here
    pulse("gift_download", workId, { gift_kind: preMarked ? "quiz_prize" : "grab" });
    if (preMarked) { rawDownload(src, name); return; }
    const host = ROOT_URL.replace(/^https?:\/\//, "").replace(/\/$/, "");
    const im = new Image();
    im.onload = () => {
      try {
        const cv = document.createElement("canvas");
        cv.width = im.naturalWidth || im.width; cv.height = im.naturalHeight || im.height;
        const ctx = cv.getContext("2d");
        ctx.drawImage(im, 0, 0);
        const fs = Math.max(13, Math.round(cv.width * 0.022)), pad = Math.round(fs * 0.9);
        ctx.font = "600 " + fs + "px -apple-system,'Segoe UI',sans-serif";
        ctx.textAlign = "right"; ctx.textBaseline = "alphabetic";
        ctx.fillStyle = "rgba(0,0,0,.34)"; ctx.fillText(host, cv.width - pad + 1, cv.height - pad + 1);
        ctx.fillStyle = "rgba(235,231,222,.66)"; ctx.fillText(host, cv.width - pad, cv.height - pad);
        cv.toBlob((blob) => {
          if (!blob) { rawDownload(src, name); return; }
          const url = URL.createObjectURL(blob);
          const a = document.createElement("a");
          a.href = url; a.download = giftName(src, name);
          document.body.appendChild(a); a.click(); a.remove();
          setTimeout(() => URL.revokeObjectURL(url), 5000);
        }, "image/jpeg", 0.92);
      } catch (e) { rawDownload(src, name); }
    };
    im.onerror = () => rawDownload(src, name);
    im.src = src;
  }
  // onYes (optional): called when the visitor says yes, BEFORE closeGift — used by the quiz-win path
  // to stamp the "gift" stage (EX-QUIZ-FLOW / INV-69) WITHOUT touching the shared ceremony behaviour.
  // N7-A11Y (INV-102, B1) — the restore is ORIGIN-CONDITIONED, uniform with the closer look (12): the
  // CALLER passes the opener only when the open is focus-origin (a keyboard grab passes the focused work,
  // a quiz-win passes the chip); a pointer / touch open passes nothing, so the ceremony forces NO focus and
  // the walk beneath is left as it was. openTrap treats a falsy opener as "restore none" (D4, 2026-07-21).
  function openGift(src, name, preMarked, onYes, workId, opener) {
    const T = (greetLang() || { t: {} }).t;
    // EX-PROTECT-RES (INV-56): the GRAB ceremony carries NO picture of its own. On a right-click the
    // work is already in view behind the card, so a thumb of the CLEAN source would only add a SECOND,
    // unguarded copy a right-click could save past the watermark — the leak this surface exists to
    // close. The QUIZ PRIZE is the one exception: it is a wallpaper the visitor won that is NOT
    // otherwise on screen, and it already wears a BAKED mark (`preMarked`), so revealing it in the card
    // leaks nothing. So the thumb is injected ONLY on the preMarked prize path; the grab card stays
    // imageless, its clean `src` a local handed to giftDownload only, stamped on its way out.
    const inner = giftCard.querySelector(".gift-inner");
    let thumb = giftCard.querySelector(".gift-thumb");
    if (preMarked) {
      if (!thumb) {
        thumb = document.createElement("img");
        thumb.className = "gift-thumb"; thumb.alt = "";
        inner.insertBefore(thumb, inner.firstChild);
      }
      thumb.src = src;                                   // the marked prize — the reveal, never a clean grab
      thumb.alt = workDesc(workId) || (((greetLang() || { t: {} }).t.a11y_gift) || A11Y_GIFT_EN);   // N7-A11Y (C8): the won wallpaper speaks
    } else if (thumb) {
      thumb.remove();                                    // a reused card returning to the grab path drops any prize image
    }
    // every line localizes through EX-I18N; the fallback is ENGLISH (source tongue), never Russian
    giftCard.querySelector(".gift-ask").textContent = T.gift_ask || "did you like it?";
    const yes = giftCard.querySelector(".gift-yes");
    yes.textContent = T.gift_yes || "it's yours :)";
    giftCard.querySelector(".gift-no").textContent = T.gift_no || "not now";
    giftCard.querySelector(".gift-line").textContent = enjoyLine();   // localized «enjoy · <host>»
    announceResult(enjoyLine());                        // N7-A11Y (INV-102 / F5): the gift result rides the SEPARATE result region
    giftCard.querySelector(".gift-buy").textContent = T.gift_buy || "for a larger print — buy";
    yes.onclick = () => { giftDownload(src, name, preMarked, workId); if (onYes) onYes(); closeGift(); };
    giftCard.dataset.work = workId != null ? String(workId) : "";   // the buy line's beat reads it
    giftCard.hidden = false; giftOpen = true;
    faceSync();                                        // the gift card is a face — arm the rest + guard (EX-CHROME)
    openTrap(giftCard, opener);                        // N7-A11Y (B1): focus into the ceremony, hold Tab inside, restore to the opener on close
    requestAnimationFrame(() => giftCard.classList.add("show"));       // EX-ARRIVE breath
  }
  function closeGift() {
    if (!giftOpen) return;
    closeTrap(giftCard);                               // N7-A11Y (B1): release the trap, restore focus to the opener
    giftCard.classList.remove("show");
    setTimeout(() => { giftCard.hidden = true; }, Math.round(350 * TEMPO));
    giftOpen = false;
    faceSync();                                        // the gift card left (EX-CHROME)
    recentreUnder();                                   // the last face leaves (EX-COMPOSE)
  }
  giftCard.querySelector(".gift-no").addEventListener("click", closeGift);
  // EX-PULSE buy_click: the pre-conversion reach — the buy line pressed means a print is wanted.
  // Today the line only measures (a shop destination is its own later movement), so the demand is
  // counted from day one; the beat carries the work like every commerce-adjacent beat.
  giftCard.querySelector(".gift-buy").addEventListener("click", () => {
    if (giftOpen) pulse("buy_click", giftCard.dataset.work || null);
  });
  giftCard.addEventListener("click", (ev) => { if (!ev.target.closest(".gift-inner")) closeGift(); });
  addEventListener("keydown", (ev) => { if (ev.key === "Escape" && giftOpen) closeGift(); });

