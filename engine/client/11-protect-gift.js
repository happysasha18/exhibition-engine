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
    // The handed file is always a JPEG — a raw source is `.jpg`, and a stamped grab is re-encoded
    // image/jpeg through the canvas. So the download name carries `.jpg` regardless of the source's
    // own extension, and the label always matches the bytes (a config `name` override owns its own).
    if (name) return name;
    const base = ((src.split("/").pop() || "photo").split("?")[0]).replace(/\.[a-z0-9]+$/i, "");
    return DL_BASE + "-" + base + ".jpg";
  }
  // EX-PROTECT-RES (INV-56): the file reaches the visitor's device by the road that device expects.
  // A phone `<a download>` does NOT reach the Photos library — iOS Safari drops the bytes into Files
  // or nowhere, which is why a saved grab «went somewhere unclear» (his find 2026-07-22). The one web
  // road into Photos is the native share sheet's «Save Image», so a coarse-pointer device is handed
  // the file through navigator.share; the desktop keeps the direct anchor save. A dismissed sheet
  // saves nothing and drops no second copy to Files — the visitor closed it (INV-1 silence).
  function anchorSave(blobOrUrl, name) {
    const isBlob = (typeof Blob !== "undefined") && (blobOrUrl instanceof Blob);
    const url = isBlob ? URL.createObjectURL(blobOrUrl) : blobOrUrl;
    const a = document.createElement("a");
    a.href = url; a.download = name;
    document.body.appendChild(a); a.click(); a.remove();
    if (isBlob) setTimeout(() => URL.revokeObjectURL(url), 5000);
  }
  function saveBlob(blob, name) {
    try {
      const file = new File([blob], name, { type: (blob && blob.type) || "image/jpeg" });
      if (matchMedia("(pointer: coarse)").matches
          && navigator.canShare && navigator.canShare({ files: [file] })) {
        navigator.share({ files: [file] }).catch((err) => {   // the sheet's «Save Image» → Photos
          // a closed sheet is the visitor's choice — save nothing (INV-1 silence). Any OTHER refusal
          // (e.g. an activation lost on a very fast yes) falls to the anchor so a file still leaves.
          if (err && err.name === "AbortError") return;
          anchorSave(blob, name);
        });
        return;
      }
    } catch (e) { /* an engine without file-share falls through to the anchor */ }
    anchorSave(blob, name);
  }
  function rawDownload(src, name) {
    try { anchorSave(src, giftName(src, name)); } catch (e) { /* the walk loses nothing if a browser refuses the save */ }
  }
  // EX-PROTECT-RES (INV-56): the SHOWN image is CLEAN; the site-host mark is stamped ONLY on a TAKEN
  // copy, HERE, client-side via canvas. The quiz prize already wears its own baked mark (preMarked)
  // and goes out raw. A browser that refuses the canvas still gets the clean file (never blocked).
  function stampToBlob(src, cb) {                             // cb(blob) or cb(null) on any failure
    const host = ROOT_URL.replace(/^https?:\/\//, "").replace(/\/$/, "");
    const im = new Image();
    im.onload = () => {
      try {
        const cv = document.createElement("canvas");
        cv.width = im.naturalWidth || im.width; cv.height = im.naturalHeight || im.height;
        const cx = cv.getContext("2d");
        cx.drawImage(im, 0, 0);
        const fs = Math.max(13, Math.round(cv.width * 0.022)), pad = Math.round(fs * 0.9);
        cx.font = "600 " + fs + "px -apple-system,'Segoe UI',sans-serif";
        cx.textAlign = "right"; cx.textBaseline = "alphabetic";
        cx.fillStyle = "rgba(0,0,0,.34)"; cx.fillText(host, cv.width - pad + 1, cv.height - pad + 1);
        cx.fillStyle = "rgba(235,231,222,.66)"; cx.fillText(host, cv.width - pad, cv.height - pad);
        cv.toBlob((blob) => cb(blob || null), "image/jpeg", 0.92);
      } catch (e) { cb(null); }
    };
    im.onerror = () => cb(null);
    im.src = src;
  }
  // The share sheet MUST be opened inside the user gesture, but the stamp (image load + canvas +
  // toBlob) is async and would spend the yes-tap's activation before navigator.share runs. So the
  // file is rendered AHEAD — the moment the ceremony opens (renderGiftBlob), while the visitor reads
  // «did you like it?» — and the yes-tap shares the READY blob synchronously. An unrendered blob (a
  // very fast yes, or a failed stamp) falls to an on-the-spot render; the phone share may then be
  // refused after the async step, so saveBlob drops to the anchor and the file still leaves.
  let giftBlob = null, giftBlobFor = null;
  function renderGiftBlob(src, preMarked) {
    giftBlob = null; giftBlobFor = src;
    if (preMarked) {
      fetch(src).then((r) => (r && r.ok ? r.blob() : null)).then((blob) => {
        if (giftBlobFor === src) giftBlob = blob;
      }).catch(() => {});
    } else {
      stampToBlob(src, (blob) => { if (giftBlobFor === src) giftBlob = blob; });
    }
  }
  function giftDownload(src, name, preMarked, workId) {
    // a gift file actually leaves for the visitor's device — the beat rides BESIDE the download, its
    // kind from the closed pair: the quiz prize goes out preMarked, a right-click grab is signed here
    pulse("gift_download", workId, { gift_kind: preMarked ? "quiz_prize" : "grab" });
    const fname = giftName(src, name);
    if (giftBlob && giftBlobFor === src) { saveBlob(giftBlob, fname); return; }   // the pre-rendered file → synchronous share keeps the iOS activation
    if (preMarked) {
      fetch(src).then((r) => (r && r.ok ? r.blob() : null)).then((blob) => {
        if (blob) saveBlob(blob, fname); else rawDownload(src, name);
      }).catch(() => rawDownload(src, name));
    } else {
      stampToBlob(src, (blob) => { if (blob) saveBlob(blob, fname); else rawDownload(src, name); });
    }
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
    giftCard.classList.toggle("prize", !!preMarked);     // the won wallpaper wants a dark stage; the grab wash lets the work show through (option C)
    renderGiftBlob(src, preMarked);                      // stamp the file AHEAD so a yes-tap can share it synchronously (iOS) — EX-PROTECT-RES
    // every line localizes through EX-I18N; the fallback is ENGLISH (source tongue), never Russian
    giftCard.querySelector(".gift-ask").textContent = T.gift_ask || "did you like it?";
    const yes = giftCard.querySelector(".gift-yes");
    yes.textContent = T.gift_yes || "it's yours :)";
    giftCard.querySelector(".gift-no").textContent = T.gift_no || "not now";
    giftCard.querySelector(".gift-line").textContent = enjoyLine();   // localized «enjoy · <host>»
    announceResult(enjoyLine());                        // N7-A11Y (INV-102 / F5): the gift result rides the SEPARATE result region
    // EX-PROTECT's own non-goal: the shop is a later movement. Until a print can actually be bought
    // the line stays HIDDEN — an empty content key hides it, and the agreed copy for the day it opens
    // is «buy a larger print» (his word 2026-07-22). No fallback literal, so an empty key shows nothing.
    const buyEl = giftCard.querySelector(".gift-buy");
    const buyText = (T.gift_buy || "").trim();
    buyEl.textContent = buyText;
    buyEl.hidden = !buyText;
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

