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
    if (!hold) toastTimer = setTimeout(toastOff, Math.round(1600 * TEMPO)); // long enough to READ the two-word line, then gone — never a lingering banner (his 2026-07-23)
  }
  toastEl.addEventListener("click", toastOff);
  addEventListener("keydown", (ev) => { if (ev.key === "Escape") toastOff(); });

  // ---- N7-A11Y (INV-102 / F5): two polite live regions beside the toast — one creator, disciplined
  // writers. The caption-and-line region carries what the VISIBLE wall label carries for the work in
  // view: the caption (REPLACE on each walk step, from the caption plaque 08) and that one work's told
  // line appended under it (from the story's seat-filling path 09, wherever the line arrived from — a
  // portion's reveal or a one-work ask), at most once per step. The result region takes the quiz
  // verdict (13) and the gift result (11) on a REPLACE discipline. A told line and a result therefore
  // land in DIFFERENT nodes and never overwrite each other. Both are visually hidden (screen-reader
  // present) via inline style, so no CSS dependency is added.
  function srLive(id) {
    const el = document.createElement("div");
    el.id = id;
    el.className = "ex-sr-live";
    el.setAttribute("role", "status");
    el.setAttribute("aria-live", "polite");
    el.style.cssText = "position:absolute;width:1px;height:1px;margin:-1px;padding:0;border:0;" +
      "overflow:hidden;clip:rect(0 0 0 0);clip-path:inset(50%);white-space:nowrap;";
    document.body.appendChild(el);
    return el;
  }
  const liveCap = srLive("ex-live-cap");               // caption (replace) + this work's told line (once)
  const liveResult = srLive("ex-live-result");         // quiz verdict + gift result (replace), a SEPARATE node
  // The step's line slot: a caption opens it, the line closes it. It starts CLOSED, so a line can never
  // stand in the region with no label above it (the door, the closing screen).
  let capLineSaid = true;
  function announceCaption(text) {                     // a walk step REPLACES — the prior label goes whole
    if (text == null) return;
    const d = document.createElement("div");
    d.className = "ex-sr-cap"; d.textContent = String(text);
    liveCap.replaceChildren(d);
    capLineSaid = false;                               // …and opens this step's one line slot
  }
  function clearLabelRegion() {                        // the closing screen: the label goes, the region with it
    liveCap.replaceChildren();
    capLineSaid = true;
  }
  function announceLine(text) {                        // the work IN VIEW's told line, once per step
    if (!text || capLineSaid) return;
    const d = document.createElement("div");
    d.className = "ex-sr-told"; d.textContent = String(text);
    liveCap.appendChild(d);
    capLineSaid = true;
  }
  function announceResult(text) {                       // the SEPARATE result region, REPLACE discipline
    if (text == null) return;
    const d = document.createElement("div");
    d.className = "ex-sr-result"; d.textContent = String(text);
    liveResult.replaceChildren(d);
  }

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

  // ---- EX-SHARE-ORIGIN (INV-1): the channel a visit first arrived under, folded to a closed shape ----
  // A value riding a stranger's own link (a folded `o` already on the address, else `utm_content`, else
  // `utm_source` — the first one found wins) is never free text on the wire: lowercased, cut to the
  // closed alphabet of letters, digits, hyphen and underscore, capped at 32 characters. An empty
  // result rides nothing.
  function foldOrigin(raw) {
    return String(raw || "").toLowerCase().replace(/[^a-z0-9_-]+/g, "").slice(0, 32);
  }
  function readOriginParam() {
    try {
      const q = new URLSearchParams(location.search);
      return foldOrigin(q.get("o") || q.get("utm_content") || q.get("utm_source") || "");
    } catch (e) { return ""; }
  }
  // the FIRST channel this visit arrived under survives every forward: a folded origin already
  // stored for this visit wins outright — only an EMPTY store takes THIS load's own reading — so a
  // visitor who opens a forwarded copy keeps the channel their own first arrival met, never the
  // copy's bare marks. Per-visit (sessionStorage), wiped with its siblings on ?reset (EX-RESET).
  let shareOrigin = null;
  try { shareOrigin = sessionStorage.getItem(ORIGIN_KEY) || null; } catch (e) {}
  if (!shareOrigin) {
    const o = readOriginParam();
    if (o) {
      shareOrigin = o;
      try { sessionStorage.setItem(ORIGIN_KEY, o); } catch (e) {}
    }
  }
  function shareArriveExtra() {                          // the join token AND the remembered channel, only when present
    const extra = shareTokenExtra() || {};
    if (shareOrigin) extra.origin = shareOrigin;
    return Object.keys(extra).length ? extra : undefined;
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
    // a stored origin (this visit's own remembered channel, EX-SHARE-ORIGIN) rides onward beside the
    // house source mark and the join token; with nothing stored the link keeps exactly today's shape.
    const link = ROOT_URL + "/?utm_source=share&utm_medium=referral&s=" + s +
      (shareOrigin ? "&o=" + shareOrigin : "") + "#w-" + id;
    const S = shareStrings();
    const write = (navigator.clipboard && navigator.clipboard.writeText)
      ? navigator.clipboard.writeText(link)
      : Promise.reject(new Error("no clipboard"));
    pulse("share_copy", id, shareOrigin ? { s: s, origin: shareOrigin } : { s: s });
    write.then(() => toast(S.copied))
         .catch(() => toast(link, true));              // never a silent failure (EX-SHARE-BTN)
  });

