  // ---- EX-I18N (INV-42): the museum speaks ANY language — after first paint ----
  // A locale outside the baked seven meets the fallback INSTANTLY; the site then quietly asks
  // its own worker for that locale's set (once per language-version, ever), keeps a browser
  // copy, and the standing surfaces re-speak without a jump. A dead worker changes nothing.
  function respeak() {
    applyDocDir();                                    // EX-RTL: a manual pick / any-locale arrival re-mirrors the whole tree
    const L = greetLang();
    if (!L) return;
    const T = L.t;
    // the zoom close + the sound chrome carry aria-labels, not visible text, but they still ride the
    // ONE string layer (EX-I18N) — the controls live on every face (walk, door, side room), so they
    // relabel regardless of atDoor
    const zClose = zoom.querySelector(".exz-close");
    if (zClose) zClose.setAttribute("aria-label", T.a11y_close || A11Y_CLOSE_EN);
    const sndVol = document.querySelector("#ex-sound .exsnd-vol");
    const sndBtn = document.querySelector("#ex-sound .exsnd-btn");
    if (sndVol) sndVol.setAttribute("aria-label", T.a11y_volume || A11Y_VOLUME_EN);
    if (sndBtn) sndBtn.setAttribute("aria-label", T.a11y_sound || A11Y_SOUND_EN);
    if (atDoor) {
      door.setAttribute("dir", T.dir === "rtl" ? "rtl" : "ltr");
      door.setAttribute("lang", L.code);
      door.querySelector(".exd-ask").textContent = T.ask || ASK_EN;
      const g = door.querySelector("#exd-greet");
      if (g && !g.hidden) g.textContent = greetLine(T) || g.textContent;
      return;
    }
    const f = Array.prototype.find.call(
      stage.querySelectorAll(".exh-frame"),
      (x) => { const r = x.getBoundingClientRect();
               return r.top < innerHeight * 0.5 && r.bottom > innerHeight * 0.5; });
    const w = f && byId[f.dataset.id];
    const tEl = cap.querySelector(".title");
    if (w && tEl && w.title) { tEl.textContent = w.title; tEl.classList.remove("untitled"); }
    else if (tEl && tEl.classList.contains("untitled")) { tEl.textContent = T.untitled || UNTITLED_EN; }
    const fin = document.getElementById("exh-fin");
    if (fin) {
      fin.setAttribute("lang", L.code);
      fin.setAttribute("dir", T.dir === "rtl" ? "rtl" : "ltr");
      const u = fin.querySelector("#ex-unfold");
      const b = fin.querySelector("#ex-return");
      const q = fin.querySelector(".q");
      if (q) q.textContent = u ? (T.q_more || q.textContent) : (T.q_spent || q.textContent);
      if (u) u.textContent = (T.more || MORE_EN).replace("{n}", String(UNFOLD)) + " ↓";
      if (b) b.textContent = T.exit || b.textContent;
    }
  }
  // ---- EX-MEMORY (INV-43): the coat-check token — the museum remembers a guest ----
  // A random token (no name, no mail — a cloakroom number); the frames the visitor actually
  // met report in ONE debounced call, fire-and-forget; a failed report is dropped silently.
  if (cfg.visitor_memory === true) {
    let tok = null;
    try { tok = localStorage.getItem(VISITOR_KEY); } catch (e) {}
    if (!tok || !/^[a-z0-9]{16,40}$/.test(tok)) {
      let r = "";
      try {
        const b = new Uint8Array(12);
        crypto.getRandomValues(b);
        r = Array.from(b, (x) => (x % 36).toString(36)).join("");
      } catch (e) { r = Math.random().toString(36).slice(2, 14); }
      tok = r + Date.now().toString(36);
      try { localStorage.setItem(VISITOR_KEY, tok); } catch (e) {}
    }
    const pending = new Set();
    let seenT = null;
    const flush = () => {
      clearTimeout(seenT); seenT = null;
      if (!pending.size) return;
      const add = Array.from(pending); pending.clear();
      try {                                            // the seen-list's local copy grows too —
        const c = JSON.parse(localStorage.getItem(SEENC_KEY) || "null") || { v: VER, ids: [] };
        const st = new Set((c.ids || []).map(String));
        add.forEach((a) => st.add(String(a)));
        localStorage.setItem(SEENC_KEY, JSON.stringify({ v: VER, ids: Array.from(st).slice(-500) }));
      } catch (e) {}                                   // — the NEXT deal's novelty voice (EX-DOOR-3)
      try {
        fetch("/api/visitor", {
          method: "PUT", keepalive: true,
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ t: tok, add: add }),
        }).catch(() => {});
      } catch (e) {}
    };
    window.__@@NS@@Seen = (id) => {
      pending.add(String(id));
      clearTimeout(seenT);
      seenT = setTimeout(flush, 3000);                 // one debounced report per walk stretch
    };
    addEventListener("pagehide", flush);
  }

  const I18N_ON = cfg.ai_i18n === true && GREET && GREET.langs;
  function applySet(code, set) {
    if (!set || !set.ask || !set.dir) return;          // strict shape or nothing (prover I1)
    GREET.langs[code] = set;                           // greetLang() now finds the guest
    if (set.titles) {
      for (const id in set.titles) {
        if (byId[id] && (byId[id].title || "").trim()) byId[id].title = set.titles[id];
      }
    }
    respeak();
  }
  function requestSet(code) {                          // cached-or-fetch, the ONE road (EX-LANG)
    if (!I18N_ON) return;
    const CK = "@@NS@@.i18n." + VER + "." + code;
    let cached = null;
    try { cached = JSON.parse(localStorage.getItem(CK) || "null"); } catch (e) {}
    if (cached) { applySet(code, cached); return; }
    fetch("/api/i18n?lang=" + code + "&v=" + encodeURIComponent(VER))
      .then((r) => (r.ok ? r.json() : null))
      .then((set) => {
        if (!set) return;
        try { localStorage.setItem(CK, JSON.stringify(set)); } catch (e) {}
        applySet(code, set);
      })
      .catch(() => {});                                // a dead worker changes nothing
  }
  if (I18N_ON) {
    const code = viewerLang();
    const known = (GREET.aliases || {})[code] || code;
    if (/^[a-z]{2,3}$/.test(code) && !GREET.langs[known]) {
      setTimeout(() => requestSet(code), 400);         // deferred — never the arrival's fetch
    }
  }

  // ---- EX-LANG (INV-45): the corner mark — the guest chooses the museum's tongue ----
  if (GREET && GREET.langs) {
    const box = document.createElement("div");
    box.className = "exd-lang";
    box.id = "exd-lang";
    const cur = document.createElement("button");
    cur.type = "button"; cur.className = "exl-cur";
    const list = document.createElement("div");
    list.className = "exl-list"; list.hidden = true;
    box.appendChild(cur); box.appendChild(list);
    door.appendChild(box);                             // the threshold's corner chrome, both faces
    // EX-ARRIVE: the mark is born at opacity:0; the next frame adds .show to breathe it in
    requestAnimationFrame(() => { box.classList.add("show"); });

    // EX-ARRIVE: the dropdown opens and closes by breath (d-soft) so it never pops
    let listCloseTimer = null;
    function listOpen() {
      clearTimeout(listCloseTimer); listCloseTimer = null;
      list.hidden = false;
      requestAnimationFrame(() => { list.classList.add("show"); });
    }
    function listClose() {
      clearTimeout(listCloseTimer); listCloseTimer = null;
      list.classList.remove("show");
      listCloseTimer = setTimeout(() => { list.hidden = true; }, Math.round(600 * TEMPO));
    }

    // EX-LANG-GEO (INV-45/INV-1): the corner offers FEW, geo-relevant tongues — English always and
    // first, then the languages of the visitor's ARRIVING COUNTRY (Cloudflare geo), then the guest's
    // own browser locale — deduped, capped. Not all baked langs. An offered tongue need NOT be baked:
    // ai_i18n's edge-translate layer speaks an outsider on pick (respeak vs requestSet, unchanged).
    const browserCode = (navigator.language || "").toLowerCase().slice(0, 2);
    const LG = cfg.lang_geo || {};                      // the owner's map (may be absent → [en, browser])
    const CMAP = LG.country_langs || {};                // uppercase ISO country → ordered lang codes
    const LANG_CAP = (LG.cap | 0) > 0 ? (LG.cap | 0) : 4;   // total chips; default 4 when absent/invalid

    // The pure narrowing law (testable in isolation): given a country, the country→langs map, the
    // browser locale, and the cap → ordered, deduped codes with English FIRST, then geo langs, then
    // the browser locale; overflow drops from the END (English is never dropped). The map is never
    // trusted to carry "en" — the client always adds it first. The country is only ever an input here.
    /* __EX_LANG_GEO_NARROW__ */
    function narrowLangCodes(country, countryLangs, browserCode, cap) {
      const out = [];
      const seen = {};
      const add = (c) => {
        c = (c || "").toLowerCase();
        if (!/^[a-z]{2,3}$/.test(c) || seen[c]) return;
        seen[c] = true; out.push(c);
      };
      add("en");                                       // English always present, and always first
      const geo = (countryLangs && country && countryLangs[country]) || [];
      for (const c of geo) add(c);                      // the arriving country's tongues, in its order
      add(browserCode);                                // the guest's own tongue, last
      const n = (cap | 0) > 0 ? (cap | 0) : 4;          // default 4 when absent/invalid
      return out.slice(0, n);                           // the cap drops overflow from the END
    }
    /* __/EX_LANG_GEO_NARROW__ */

    const markOf = () => {
      const c = viewerLang();
      return ((GREET.aliases || {})[c] || c).toUpperCase().slice(0, 2) || "EN";
    };
    const redraw = () => {
      cur.textContent = markOf();
      list.querySelectorAll(".exl-item").forEach((b) =>
        b.classList.toggle("cur", b.dataset.lang === viewerLang()));
    };
    // ONE chip-append road — the initial build and the post-geo refresh both run it, so per-chip
    // behavior can never drift between them. The list is cleared first: no stale chip, no double listener.
    const renderCodes = (codes) => {
      list.textContent = "";
      codes.forEach((c) => {
        const b = document.createElement("button");
        b.type = "button"; b.className = "exl-item";
        b.dataset.lang = c;
        b.textContent = c.toUpperCase();
        b.addEventListener("click", (ev) => {
          ev.stopPropagation();
          langOverride = c;
          try { localStorage.setItem(LANG_KEY, c); } catch (e) {}
          listClose();
          const known = (GREET.aliases || {})[c] || c;
          const baked = !!GREET.langs[known];
          // EX-PULSE registry: the chosen tongue is a CODE from the baked list; an outsider tongue
          // reports `other`, never a raw locale string on the wire — the ladder stays closed (INV-1).
          // The ARRIVING COUNTRY never enters a pulse: it only picked which chips exist.
          pulse("lang_pick", null, { lang: baked ? known : "other" });
          if (baked) respeak();                        // a baked tongue answers at once
          else requestSet(c);                          // an outsider rides the one layer
          redraw();
        });
        list.appendChild(b);
      });
      redraw();
    };

    // First paint: English + the browser locale only (geo has not answered yet).
    renderCodes(narrowLangCodes("", CMAP, browserCode, LANG_CAP));

    // Then, once and quietly, ask the edge for the arriving country and re-narrow. Best-effort:
    // a failed, blocked, or unknown-country geo NEVER touches the box — it stays [en, browser].
    // The country is used ONLY to pick chips here; it is never stored, never sent to GA, never on a beat.
    try {
      fetch("/api/geo")
        .then((r) => (r.ok ? r.json() : null))
        .then((g) => {
          const cc = g && typeof g.c === "string" ? g.c.toUpperCase() : "";
          if (!cc || !CMAP[cc]) return;                // no country, or one we hold no langs for ⇒ stand pat
          renderCodes(narrowLangCodes(cc, CMAP, browserCode, LANG_CAP));
        })
        .catch(() => {});                              // a dead / blocked geo changes nothing
    } catch (e) {}

    cur.addEventListener("click", (ev) => {
      ev.stopPropagation();
      list.hidden ? listOpen() : listClose();
    });
    door.addEventListener("click", () => { listClose(); });
    // N7-A11Y (INV-102, B5): the list closes under every modality — on the keyboard's own Escape (from
    // anywhere while the list stands), and when focus leaves the corner entirely (a Tab / a click away),
    // beside the existing document-click. Escape is document-level so it closes regardless of where focus
    // sits; the focus-out close reads a real focus leaving the box.
    addEventListener("keydown", (ev) => {
      if (ev.key === "Escape" && !list.hidden) { listClose(); try { cur.focus(); } catch (e) {} }
    });
    box.addEventListener("focusout", (ev) => {
      if (!list.hidden && !box.contains(ev.relatedTarget)) listClose();   // focus left the corner → close
    });
    redraw();
  }

