  // ---- EX-SHARE: the quiet per-frame affordance — it copies, never navigates ----
  // (the ↗ corner link out to /w/ RETIRED with it, 2026-07-06 evening; /w/ pages stay
  // the machines' surface, reachable from the static index — CS-6)
  const SHARE_GLYPH =
    '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor"' +
    ' stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
    '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/>' +
    '<path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>';
  const shareStrings = () => {
    const L = greetLang();
    const T = L ? L.t : {};
    return {                                           // RU built-ins stand under a missing cache
      label: T.share_label || "скопировать ссылку",
      copied: T.share_copied || "ссылка скопирована",
    };
  };

  // the toast — one quiet line; the success face leaves by itself, the refusal face
  // CARRIES the link and stays until dismissed (a tap, Esc) — it must be hand-copyable
  const toastEl = document.createElement("div");
  toastEl.id = "ex-toast";
  toastEl.hidden = true;
  toastEl.setAttribute("role", "status");              // announced politely, never interrupts
  toastEl.setAttribute("aria-live", "polite");
  document.body.appendChild(toastEl);
  let toastTimer = null;
  function toastOff() {
    clearTimeout(toastTimer); toastTimer = null;
    toastEl.classList.remove("show", "hold");             // EX-ARRIVE: drop the show class first
    toastEl.hidden = true;
  }
  function toast(text, hold) {
    clearTimeout(toastTimer); toastTimer = null;
    toastEl.classList.remove("show");                     // EX-ARRIVE: reset so rAF re-fires the fade
    toastEl.textContent = text;
    toastEl.classList.toggle("hold", !!hold);
    toastEl.hidden = false;
    requestAnimationFrame(() => { toastEl.classList.add("show"); }); // EX-ARRIVE: breath in
    if (!hold) toastTimer = setTimeout(toastOff, Math.round(3000 * TEMPO));
  }
  toastEl.addEventListener("click", toastOff);
  addEventListener("keydown", (ev) => { if (ev.key === "Escape") toastOff(); });

  // ---- EX-SHARE join (INV-1): a copied link carries a FRESH random per-share token `s` so GA
  // can join THIS specific share to the specific open it produces (the virality loop / k-factor).
  // The token is minted per click, is a bounded closed-alphabet word, and carries NO visitor
  // identity — a random draw, never the coat-check token — so the loop closes without linking
  // people (INV-1: no free text, no identity on the wire).
  function mintShareToken() {
    try {
      const b = new Uint8Array(6);
      crypto.getRandomValues(b);
      return Array.from(b, (x) => (x % 36).toString(36)).join("");
    } catch (e) { return Math.random().toString(36).slice(2, 8); }
  }
  function shareTokenExtra() {                          // read `s` off THIS arrival's query, closed-shape
    try {
      const m = (location.search || "").match(/[?&]s=([a-z0-9]{1,16})(?:&|$)/);
      if (m) return { s: m[1] };                        // validated shape ⇒ safe to ride (INV-1)
    } catch (e) {}
    return undefined;                                   // no token ⇒ the payload is byte-for-byte today's
  }

  // ONE share control FLOATS over the walk (2026-07-09: the player and the link are chrome
  // ABOVE the room — they never ride a frame, so nothing drifts with a scroll). It acts on the
  // work IN VIEW (dataset.share follows the frame observer) and lives by the caption's law:
  // shows with a work, leaves on the closing screen, the door hides all walk chrome.
  const shareBtn = document.createElement("button");
  shareBtn.type = "button";
  shareBtn.className = "ex-share";
  shareBtn.id = "ex-share";
  shareBtn.innerHTML = SHARE_GLYPH;
  document.body.appendChild(shareBtn);
  shareBtn.addEventListener("click", () => {
    const id = shareBtn.dataset.share;
    if (!id) return;
    // The copied line carries UTM attribution (EX-SHARE-BTN) so a shared arrival separates
    // from Direct/bot noise — the utm rides before the hash (GA reads the query, the room reads #w-<id>).
    // A fresh per-share token `s` rides too (EX-SHARE join / INV-1), stamped on this copy so the
    // matching arrival joins back to it.
    const s = mintShareToken();
    const link = ROOT_URL + "/?utm_source=share&utm_medium=referral&s=" + s + "#w-" + id;
    const S = shareStrings();
    const write = (navigator.clipboard && navigator.clipboard.writeText)
      ? navigator.clipboard.writeText(link)
      : Promise.reject(new Error("no clipboard"));
    pulse("share_copy", id, { s: s });
    write.then(() => toast(S.copied))
         .catch(() => toast(link, true));              // never a silent failure (EX-SHARE-BTN)
  });

