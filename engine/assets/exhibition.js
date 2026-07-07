/* exhibition.js — the adaptive exhibition (EX): the DOOR → the GALLERY (the Room's museum hang).
   Norm for look & feel: gallery/door.html + gallery/room.html — Alexander's approved prototypes
   (2026-07-06: "прототип — норма"). The laws: a cold arrival meets the door — his photographs and
   the quiet ask «что ближе сейчас» (EX-DOOR); the pick seeds the hang — one work per viewport,
   caption in the margin, breathing ground (EX-HANG); the walk ENDS (INV-30) and always loops back
   to the threshold (INV-31). Every knob reads from config.json → exhibition (INV-28).
   Kinship math runs in the browser on baked vectors ($0, no server). No axis name, score or
   confidence ever renders (INV-1) — the caption zone speaks only his titles and the archive's facts. */
(async function () {
  "use strict";
  const stage = document.getElementById("ex-stage");
  if (!stage) return;                                 // no live root → JS-off face stays

  // ---- the visitor's own trace, its three homes (one place for the names) -----
  const KEY = "tlv.exhibition";                       // the walk (INV-26)
  const PLACE_KEY = "tlv.place";                      // the per-tab place marker (INV-32c)
  const TEMPO_KEY = "tlv-tempo";                      // the motion override (EX-MOTION-R)
  const SPENT_KEY = "tlv.spent";                      // the hash hand-over, consumed once (EX-SHARE-IN)
  const VISITOR_KEY = "tlv.visitor";                  // the coat-check token (EX-MEMORY)
  const HAND_KEY = "tlv.hand";                        // the last dealt threshold hand (EX-DOOR-3)
  const SEENC_KEY = "tlv.seenc";                      // the seen-list's local copy (EX-DOOR-3)
  const LANG_KEY = "tlv.lang";                        // the guest's chosen tongue (EX-LANG)

  // ---- EX-TIMING (INV-38): the museum keeps time — for its builder only -------
  // Marks are free and invisible (INV-1: no DOM text; INV-18: no beacon, nothing
  // leaves the tab). ?timings narrates the beats to the console as they land;
  // TLVTimings() hands the walk's clock over as data for export.
  const WANT_T = new URLSearchParams(location.search).has("timings");
  function tlog(beat) {
    try { performance.mark("tlv:" + beat); } catch (e) {}
    if (WANT_T) {
      try { console.log("tlv:" + beat, (performance.now() / 1000).toFixed(3) + "s"); } catch (e) {}
    }
  }
  window.TLVTimings = () => performance.getEntriesByType("mark")
    .filter((m) => m.name.indexOf("tlv:") === 0)
    .map((m) => ({ beat: m.name.slice(4), at: +(m.startTime / 1000).toFixed(3) }));
  tlog("boot");

  // ---- EX-PULSE (INV-41): the walk counts its beats for the archive's owner ----
  // Rides the ONE sanctioned wire (the baked GA tag); no tag ⇒ total silence; an event
  // carries at most the plain name + the work's public id — never a vector (INV-1).
  function pulse(beat, workId) {
    try {
      if (typeof window.gtag !== "function") return;
      window.gtag("event", beat, workId ? { work: String(workId) } : {});
    } catch (e) {}
  }

  // ---- EX-RESET (INV-35): the ?reset address — the museum forgets THIS browser --
  // One wipe, named keys only, BEFORE anything restores; the param strips itself via
  // replaceState — no history step laid (INV-32 fenced) and the pre-strip URL leaves
  // history with it; a storage refusal never blocks the arrival; a sibling window's
  // later save re-creates state by INV-26's last-writer rule.
  if (new URLSearchParams(location.search).has("reset")) {
    try { localStorage.removeItem(KEY); } catch (e) {}
    try { localStorage.removeItem(TEMPO_KEY); } catch (e) {}
    try { sessionStorage.removeItem(PLACE_KEY); } catch (e) {}
    try { sessionStorage.removeItem(SPENT_KEY); } catch (e) {}  // the hash re-seeds a FIRST arrival
    try { localStorage.removeItem(VISITOR_KEY); } catch (e) {}   // forgetting is whole (EX-MEMORY)
    try { localStorage.removeItem(HAND_KEY); } catch (e) {}
    try { localStorage.removeItem(SEENC_KEY); } catch (e) {}
    try { localStorage.removeItem(LANG_KEY); } catch (e) {}     // the browser's tongue returns
    const q = new URLSearchParams(location.search);
    q.delete("reset");
    const rest = q.toString();
    try {
      history.replaceState(history.state, "",
        location.pathname + (rest ? "?" + rest : "") + location.hash);
    } catch (e) {}
  }

  let cfg, data;
  try {
    [cfg, data] = await Promise.all([
      fetch("config.json").then((r) => r.json()),
      fetch("exhibition_data.json").then((r) => r.json()),
    ]);
  } catch (e) {
    document.documentElement.classList.remove("js");  // static face returns NOW (CS-8/INV-25)
    return;
  }
  tlog("data");

  // ---- feel knobs, all from config (INV-28) ---------------------------------
  const EX = cfg.exhibition || {};
  const clampInt = (x, dflt, lo, hi) => {
    const n = parseInt(x, 10);
    return Number.isFinite(n) ? Math.max(lo, Math.min(hi, n)) : dflt;
  };
  const SPREAD = clampInt(EX.spread_size, 10, 3, 12);   // the hang shows ~10, never the catalogue
  const UNFOLD = clampInt(EX.unfold_step, 5, 1, 12);
  const MAXU = clampInt(EX.max_unfolds, 2, 0, 5);       // «ещё 5» retires after this (INV-30)
  const DOOR_SIZE = clampInt(EX.door_size, 5, 3, 5);    // works at the threshold (EX-DOOR)
  // EX-MOTION: ONE clock for CSS and JS — config tempo, a visitor/test override in
  // localStorage['tlv-tempo'] clamped to [0.05, 3]; stillness (reduced motion) wins over both
  const REDUCED = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const TEMPO = (() => {
    if (REDUCED) return 0.05;
    let o = NaN;
    try { o = parseFloat(localStorage.getItem(TEMPO_KEY)); } catch (e) {}
    const t = Number.isFinite(o) ? o : Number(EX.tempo) || 1.35;
    return Math.min(3, Math.max(0.05, t));
  })();
  if (!REDUCED) document.documentElement.style.setProperty("--tempo", String(TEMPO));
  const COLD = EX.cold_spread || "diverse";
  const ARC = EX.arc_shape || "widening";
  const AXES = EX.kinship_axes || "all";
  const CAP = SPREAD + MAXU * UNFOLD;
  const GPLACE = ["ask", "top", "off"].indexOf(EX.greeting) >= 0 ? EX.greeting : "ask";
  // the room permalink's canonical root (EX-SHARE-BTN): the copied line is the SITE's,
  // clean of whatever params/host the sharer's own address carries
  const ROOT_URL = String(cfg.site_url || location.origin).replace(/\/+$/, "");

  // ---- the greeting (EX-GREET): the visitor's own words, at their own hour ---
  // Language = the browser's own setting; hour = the device clock. Strings are the BAKED
  // cache riding exhibition_data.json (EX-GREET-BAKE) — no cache, no greeting, the door
  // stands on its built-in lines (it never blocks entry).
  const GREET = data.greet || null;
  // ONE reader of the guest's tongue (EX-LANG, prover L1): the chosen override outranks the
  // browser everywhere a language is read — the greeting, the strings, the any-locale fetch.
  let langOverride = null;
  try {
    const lo = localStorage.getItem(LANG_KEY);
    if (lo && /^[a-z]{2,3}$/.test(lo)) langOverride = lo;
  } catch (e) {}
  function viewerLang() {
    return (langOverride || navigator.language || "").toLowerCase().slice(0, 2);
  }
  function greetLang() {
    if (!GREET || !GREET.langs) return null;
    let code = viewerLang();
    code = (GREET.aliases || {})[code] || code;
    if (!GREET.langs[code]) code = GREET.fallback || "en";
    const t = GREET.langs[code];
    return t ? { code, t } : null;
  }
  function greetLine(t) {
    const h = new Date().getHours();
    const part = h < 6 ? "night" : h < 12 ? "morning" : h < 18 ? "day" : "evening";
    const pool = (t.greet || {})[part] || [];
    if (!pool.length) return "";
    const day = new Date().toISOString().slice(0, 10);   // date-seeded like the door rotation
    let s = 0;
    for (const c of day) s = (s * 31 + c.charCodeAt(0)) >>> 0;
    return pool[s % pool.length];
  }

  // ---- honest Back (INV-32): the walk and the browser speak the same history --
  // Steps are laid per FACE (door | walk), never per frame; a door step CARRIES the
  // spread it showed; the ↗ place marker is per-tab (sessionStorage), one-shot.
  try { history.scrollRestoration = "manual"; } catch (e) {}
  const pushFace = (st) => { try { history.pushState({ tlv: st }, ""); } catch (e) {} };
  const replaceFace = (st) => { try { history.replaceState({ tlv: st }, ""); } catch (e) {} };

  // ---- baked data -----------------------------------------------------------
  const SERIES = data.series || [];                    // real series only (3+), variant each
  const VER = String(data.version || "1");
  const works = data.works;                 // [{id,img,slug,w,h,dom,title,sec,place}]
  const byId = Object.fromEntries(works.map((w) => [w.id, w]));
  const V = data.v;
  const DIM = V[works[0].id].length;
  const sel = Array.isArray(AXES) ? AXES.filter((i) => i >= 0 && i < DIM)
                                  : [...Array(DIM).keys()];
  const vec = (id) => sel.map((i) => V[id][i]);
  const dist = (a, b) => {
    let s = 0;
    for (let i = 0; i < a.length; i++) { const d = a[i] - b[i]; s += d * d; }
    return Math.sqrt(s);
  };

  // the door pool — baked provenance ∩ living works; thinner than door_size ⇒ NO door:
  // silent entry onto the default hang (the door never blocks entry, EX-DOOR)
  const doorPool = ((data.door || {}).pool || []).filter((e) => e && byId[e.id]);
  const doorAvailable = doorPool.length >= DOOR_SIZE;

  // ---- orderings ------------------------------------------------------------
  function coldOrder() {                    // maximally diverse (farthest-point)
    const ids = works.map((w) => w.id);
    if (COLD === "first") return ids.slice();
    const cx = vec(ids[0]).map((_, i) => ids.reduce((s, id) => s + vec(id)[i], 0) / ids.length);
    const order = [ids.reduce((b, id) => (dist(vec(id), cx) > dist(vec(b), cx) ? id : b))];
    const used = new Set(order);
    while (order.length < ids.length) {
      let best = null, bd = -1;
      for (const id of ids) {
        if (used.has(id)) continue;
        const md = Math.min(...order.map((c) => dist(vec(id), vec(c))));
        if (md > bd) { bd = md; best = id; }
      }
      order.push(best); used.add(best);
    }
    return order;
  }

  function arcOrder(pickId) {               // near neighbours drawn in, widening steps hold contrast
    const sorted = works.filter((w) => w.id !== pickId)
      .sort((a, b) => dist(vec(a.id), vec(pickId)) - dist(vec(b.id), vec(pickId)));
    const order = [pickId];
    const used = new Set(order);
    if (ARC === "nearest") {
      sorted.forEach((w) => { order.push(w.id); used.add(w.id); });
      return order;
    }
    let step = 1, i = 0;
    while (i < sorted.length) {
      const id = sorted[i].id;
      if (!used.has(id)) { order.push(id); used.add(id); }
      i += step; step = Math.max(1, Math.round(step * 1.6));
    }
    for (const w of sorted) if (!used.has(w.id)) { order.push(w.id); used.add(w.id); }
    return order;
  }

  // EX-DOOR-3 (INV-44): the hand LIVES — rotation + novelty + the hour, under HIS LAW
  // (a new hand repeats at most a THIRD of the previous one). The pool stays curated
  // (EX-DOOR-2d); his file order is the tie-break voice; a pool of exactly door_size
  // stands the law down (the hand IS the pool).
  function dealHand() {
    const n = Math.min(DOOR_SIZE, doorPool.length);
    if (doorPool.length <= n) return doorPool.slice(0, n);
    let prev = [];
    try {
      const h = JSON.parse(localStorage.getItem(HAND_KEY) || "null");
      if (h && h.v === VER && Array.isArray(h.ids)) prev = h.ids;
    } catch (e) {}
    let seen = new Set();
    try {
      const c = JSON.parse(localStorage.getItem(SEENC_KEY) || "null");
      if (c && Array.isArray(c.ids)) seen = new Set(c.ids.map(String));
    } catch (e) {}
    const hour = new Date().getHours();
    const part = hour < 6 ? "night" : hour < 12 ? "morning" : hour < 18 ? "day" : "evening";
    const tone = (e) => {
      const l = Number(e.luma), w = Number(e.warmth);
      if (!Number.isFinite(l) || !Number.isFinite(w)) return 0;
      if (part === "night") return 1 - l;              // the darker faces
      if (part === "evening") return w;                // the warmer
      return l;                                        // morning + day lean bright
    };
    const scored = doorPool.map((e, i) => ({
      e,
      s: (seen.has(String(e.id)) ? 0 : 2)              // novelty first (his pick)
         + tone(e) * 0.9                               // the hour leans
         - i * 0.01                                    // his order breaks ties
         + Math.random() * 0.25,                       // the rotation's own breath
    }));
    scored.sort((a, b) => b.s - a.s);
    const maxRepeat = Math.floor(n / 3);               // HIS LAW: ≤ a third repeats
    const hand = [];
    let repeats = 0;
    for (const c of scored) {
      const isPrev = prev.indexOf(c.e.id) >= 0;
      if (isPrev && repeats >= maxRepeat) continue;
      hand.push(c.e);
      if (isPrev) repeats += 1;
      if (hand.length === n) break;
    }
    for (const c of scored) {                          // the law can never starve the hand
      if (hand.length === n) break;
      if (hand.indexOf(c.e) < 0) hand.push(c.e);
    }
    try { localStorage.setItem(HAND_KEY, JSON.stringify({ v: VER, ids: hand.map((e) => e.id) })); } catch (e) {}
    return hand;
  }
  function standingHand() {                            // the session keeps its set (INV-31/2d)
    try {
      const h = JSON.parse(localStorage.getItem(HAND_KEY) || "null");
      if (h && h.v === VER && Array.isArray(h.ids)) {
        const by = Object.fromEntries(doorPool.map((e) => [e.id, e]));
        const sp = h.ids.map((id) => by[id]).filter(Boolean);
        if (sp.length >= Math.min(DOOR_SIZE, doorPool.length)) return sp;
      }
    } catch (e) {}
    return null;
  }
  function doorSet() { return standingHand() || dealHand(); }

  // one line, always (EX-DOOR-2b — card 01's algorithm IS the norm): a row when landscape
  // (W/H > 1.02), a column when portrait; windows shrink first, the count drops second
  // (row 5→4→3 while each keeps ≥118px; column 3→2 below 104px); never a second line
  function doorLayout() {
    const W = innerWidth, H = innerHeight, col = W / H <= 1.02;
    let gap, n, size;
    if (!col) {
      gap = Math.max(16, Math.min(44, W * 0.03));
      const cap = Math.min(190, H * 0.42);
      n = Math.min(DOOR_SIZE, doorPool.length);
      for (; n > 3; n--) {
        size = Math.min(cap, (W * 0.88 - (n - 1) * gap) / n);
        if (size >= 118) break;
      }
      size = Math.min(cap, (W * 0.88 - (n - 1) * gap) / n);
    } else {
      gap = Math.max(14, Math.min(30, H * 0.025));
      const cap = Math.min(190, W * 0.62);
      n = Math.min(3, doorPool.length);
      size = Math.min(cap, (H * 0.52 - (n - 1) * gap) / n);
      if (size < 104 && n > 2) { n = 2; size = Math.min(cap, (H * 0.52 - gap) / 2); }
    }
    return { n, col, gap, size: Math.max(76, size) };
  }

  // ---- state + persistence (INV-26) -----------------------------------------
  let pick = null;
  let order = coldOrder();
  let shown = SPREAD;

  function save() {
    try { localStorage.setItem(KEY, JSON.stringify({ v: VER, pick, shown })); } catch (e) {}
  }
  function restore() {
    let st;
    try { st = JSON.parse(localStorage.getItem(KEY) || "null"); } catch (e) { st = null; }
    if (!st || st.v !== VER) return false;            // old-version state → clean start (the door)
    if (st.pick != null) {
      if (!byId[st.pick]) return false;               // pick gone from the gallery → clean start
      pick = st.pick; order = arcOrder(pick);
    }
    // the unfold budget DERIVES from shown, never trusted (INV-30 holds on restore)
    shown = clampInt(st.shown, SPREAD, SPREAD, Math.min(order.length, CAP));
    return true;
  }
  const spentUnfolds = () => Math.max(0, Math.floor((shown - SPREAD) / UNFOLD));

  // ---- the breathing ground (room.html's tone math) --------------------------
  // EX-ACCENT rides the same pair: the focused work's tone raised to readable light
  // (Y≈170, 20% bone; near-black → bone whole) lives while the ground does, rests with it
  const BONE = [179, 162, 132];                        // #b3a284 — the resting accent
  function liveAccent(dom) {
    const [r, g, b] = dom;
    const y = 0.2126 * r + 0.7152 * g + 0.0722 * b;
    if (y < 24) return BONE;
    const k = Math.min(170 / y, 6);
    return [r, g, b].map((v, i) => Math.round(Math.min(255, v * k) * 0.8 + BONE[i] * 0.2));
  }
  function ground(dom) {
    if (!dom) return;
    const [r, g, b] = dom;
    const y = 0.2126 * r + 0.7152 * g + 0.0722 * b;
    const tone = (c) => 0.7 * (c * 0.2) + 0.3 * (y * 0.2);
    const mix = (c) => Math.round(12 + (tone(c) - 12) * 0.7);
    document.body.style.setProperty("--ground", `${mix(r)},${mix(g)},${mix(b)}`);
    const a = liveAccent(dom);
    document.documentElement.style.setProperty("--accent", `rgb(${a.join(",")})`);
    document.documentElement.style.setProperty(
      "--accent-2", `rgb(${a.map((v) => Math.round(v * 0.86)).join(",")})`);
  }
  const groundRest = () => {
    document.body.style.setProperty("--ground", "12,11,10");
    document.documentElement.style.removeProperty("--accent");    // back to resting bone
    document.documentElement.style.removeProperty("--accent-2");
  };

  // ---- EX-LOAD (INV-37): the loading breath — no frame in view stays empty ----
  // One wordless hairline (INV-1), armed by the frame currently in view whenever its
  // pixels have not arrived; a grace beat keeps a healthy network from ever seeing it;
  // load OR error retires it — a dead image never traps the breath.
  const breath = document.createElement("div");
  breath.id = "ex-breath";
  breath.hidden = true;
  document.body.appendChild(breath);
  let breathTimer = null;
  let waited = null;                                   // the one image the breath waits for
  function breathOff() {
    clearTimeout(breathTimer); breathTimer = null;
    breath.hidden = true;
  }
  function breathe(img) {                              // the frame in view changed
    breathOff();
    waited = img;
    if (!img || img.complete) return;                  // pixels home (or already failed)
    let shownBreath = false;
    breathTimer = setTimeout(() => {                   // the grace beat (~.35s ×tempo)
      if (img !== waited || img.complete) return;
      shownBreath = true;
      breath.hidden = false;
      tlog("breath");
    }, Math.round(350 * TEMPO));
    const done = () => {                               // load OR error, whichever speaks first
      if (img !== waited) return;
      breathOff();
      if (!shownBreath) return;                        // landed inside the grace — nothing to undo
      tlog("img");
      if (img.naturalWidth) {                          // late pixels enter by the room's own fade,
        img.style.transition = "none";                 // never a hard pop
        img.style.opacity = "0";
        void img.offsetWidth;
        img.style.transition = "";
        img.style.opacity = "";
      }
    };
    img.addEventListener("load", done, { once: true });
    img.addEventListener("error", done, { once: true });
  }

  // ---- THE DOOR (door.html's face — the norm) --------------------------------
  const door = document.createElement("div");
  door.id = "ex-door";
  door.hidden = true;                                  // born hidden — a restored walk must never
                                                       // wake under a dark cover (2026-07-06 bug)
  door.innerHTML =
    '<div class="exd-wm">TLV PHOTOS</div>' +   // the brand is PLURAL, never translated (5j)
    '<div class="exd-greet" id="exd-greet" hidden></div>' +
    '<div class="exd-ask">что ближе сейчас</div>' +
    '<div class="exd-facade" id="exd-facade"></div>';  // no silent entry — the pick IS the
  document.body.appendChild(door);                     // entry (EX-DOOR-2a, his design word)
  const veil = document.createElement("div");          // the ceremony's black (EX-DOOR-2e)
  veil.id = "ex-veil";
  veil.hidden = true;
  document.body.appendChild(veil);

  let atDoor = false;
  let entered = false;                                 // a walk exists behind the door
  let doorFace = null;                                 // the spread the standing door renders
  let curLay = { n: 0, col: null };

  // cold=true only on the COLD-arrival face: a museum greets on arrival, not on every
  // pass through the lobby (EX-GREET) — the re-opened door keeps the localized ask only
  function renderDoor(spread, cold) {    // the spread is CARRIED by the caller (INV-32a)
    ceremonyCancel();                                  // a door render wins over any crossing
    breathOff();                                       // the door covers every frame (EX-LOAD)
    atDoor = true;
    tlog("door");
    document.body.classList.add("ex-door");
    door.classList.remove("leaving");
    door.hidden = false;
    doorFace = { spread: spread || doorSet() };
    curLay = { n: 0, col: null };
    const L = greetLang();
    door.setAttribute("dir", L && L.t.dir === "rtl" ? "rtl" : "ltr");
    if (L) door.setAttribute("lang", L.code);
    else door.removeAttribute("lang");
    door.querySelector(".exd-ask").textContent = L ? L.t.ask : "что ближе сейчас";
    const g = door.querySelector("#exd-greet");
    const line = (cold && GPLACE !== "off" && L) ? greetLine(L.t) : "";
    g.textContent = line;
    g.hidden = !line;                    // ambient: Back to a cold step re-greets at the CURRENT hour
    door.classList.toggle("greet-top", GPLACE === "top");
    doorRender();
    if (cold) hintArm(); else hintOff(); // the re-opened door never hints (EX-DOOR-2g)
  }

  // layout-aware render — re-runs on resize; rebuilds only when count/orientation change
  function doorRender() {
    if (!atDoor || !doorFace) return;
    const c = doorLayout();
    const facade = door.querySelector("#exd-facade");
    facade.classList.toggle("col", c.col);
    facade.style.setProperty("--exd-gap", c.gap.toFixed(1) + "px");
    facade.style.setProperty("--exd-wsize", c.size.toFixed(1) + "px");
    if (c.n === curLay.n && c.col === curLay.col) return;
    curLay = c;
    facade.innerHTML = "";
    doorFace.spread.slice(0, c.n).forEach((e, i) => {
      const w = byId[e.id];
      const alt = (e.alt || "").replace(/"/g, "&quot;");
      const b = document.createElement("button");
      b.type = "button"; b.className = "exd-window";
      b.dataset.id = w.id;
      b.setAttribute("aria-label", e.alt || w.title || "");
      // the halo speaks liveAccent, never the raw dominant — a near-black dominant is
      // invisible on the dark ground (card 01's note, EX-DOOR-2c)
      const a = liveAccent(w.dom);
      b.style.setProperty("--glow", `rgb(${a.join(",")})`);
      b.style.animationDelay = ((0.55 + i * 0.2) * TEMPO).toFixed(2) + "s";
      b.innerHTML = `<img src="${w.img}" alt="${alt}">`;
      b.addEventListener("click", () => doorPick(w));
      facade.appendChild(b);
    });
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
    door.classList.remove("wm-out");
    document.body.classList.remove("ex-crossing", "ex-cross-cap");
    busy = false;
  }

  // the beats below are ONE THIRD of the card's old clock (EX-DOOR-2e re-ruled, his word
  // 2026-07-06 evening) — only the WAITS shortened; the reveal fade keeps its full span
  function doorPick(w) {
    if (busy) return;
    busy = true;
    tlog("pick");
    pulse("door_pick", w.id);
    const g = ++cerGen;
    const ok = () => g === cerGen;
    pick = w.id;
    order = arcOrder(pick);
    shown = SPREAD;                                    // a fresh arc = a fresh budget (INV-30/31)
    veil.hidden = false;
    veil.style.transitionDuration = (0.33 * TEMPO) + "s";
    door.classList.add("leaving");                     // the wordmark drifts to the center
    requestAnimationFrame(() => veil.classList.add("on"));
    cerAfter(0.92, () => { if (!ok()) return;          // the name lets go
      door.classList.add("wm-out");
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
    cerAfter(1.78, () => { if (!ok()) return;          // …then the first work, separately
      tlog("reveal");
      const first = stage.querySelector(".exh-frame img.work");
      if (first) first.style.transitionDuration = (1.5 * TEMPO) + "s";
      document.body.classList.remove("ex-crossing");
      document.body.classList.add("ex-cross-cap");     // the caption still waits its beat
    });
    cerAfter(1.93, () => { if (!ok()) return;          // the caption, last (+.15)
      tlog("caption");
      document.body.classList.remove("ex-cross-cap");
      const first = stage.querySelector(".exh-frame img.work");
      if (first) first.style.transitionDuration = "";
      veil.hidden = true;
      busy = false;
    });
  }

  function closeDoor() {
    hintOff();
    atDoor = false;
    entered = true;
    door.hidden = true;
    document.body.classList.remove("ex-door");
  }

  let walkY = 0;                                       // the walk's place while a door covers it
  function doorReturn() {                              // the gallery's quiet exit (INV-31)
    if (busy || !doorAvailable) return;
    tlog("exit");
    pulse("walk_exit");
    walkY = scrollY;                                   // Back must return HERE (INV-32b)
    groundRest();
    const sp = doorSet();                              // the SAME curated set — a fresh quiz
    renderDoor(sp, false);                             // is a fresh PICK (EX-DOOR-2d)
    pushFace({ face: "door", spread: sp.map((e) => e.id) });  // the step carries its spread
    scrollTo(0, 0);
  }

  addEventListener("popstate", (ev) => {               // Back/Forward walk the faces (INV-32)
    ceremonyCancel();                                  // navigation wins mid-ceremony (EX-DOOR-2e)
    const st = ev.state && ev.state.tlv;
    closeSide();                                       // a step away closes the side room (EX-SERIES)
    if (st && st.face === "series" && typeof st.ser === "number") {
      openSide(st.ser, false);                         // Forward re-opens without a new step
      return;
    }
    if (st && st.face === "door") {
      // the door AS IT STOOD: rebuild the carried spread from the pool (never a fresh roll)
      const byPool = Object.fromEntries(doorPool.map((e) => [e.id, e]));
      const sp = (st.spread || []).map((id) => byPool[id]).filter(Boolean);
      groundRest();
      renderDoor(sp.length ? sp : undefined, st.cold === true);
      scrollTo(0, 0);
      return;
    }
    // a walk step renders the walk AS IT NOW IS (INV-32d) — a dead arc never resurrects
    if (atDoor) {
      closeDoor();
      if (pick && byId[pick]) ground(byId[pick].dom);
      scrollTo(0, walkY);                              // the closing screen the visitor left (INV-32b)
    }
  });

  // ---- THE GALLERY (room.html's museum hang — the norm) ----------------------
  const counter = document.createElement("div");
  counter.className = "exh-counter"; counter.id = "exh-counter";
  counter.innerHTML = '<span class="now">01</span> / <span class="tot">–</span>';
  const cap = document.createElement("div");
  cap.className = "exh-capzone"; cap.id = "exh-cap";
  document.body.appendChild(counter);
  document.body.appendChild(cap);

  const io = new IntersectionObserver((es) => es.forEach((x) => {
    if (!x.isIntersecting) return;
    x.target.classList.add("seen");
    const w = byId[x.target.dataset.id];
    if (!w) return;
    breathe(x.target.querySelector("img.work"));       // late pixels meet the breath (EX-LOAD)
    if (window.__tlvSeen) window.__tlvSeen(w.id);      // the coat-check report (EX-MEMORY)
    // the walk tracks its place per frame in view (INV-32c re-carried after the ↗ retired)
    try { sessionStorage.setItem(PLACE_KEY, JSON.stringify({ v: VER, id: w.id })); } catch (e) {}
    // a late callback must never re-live the tone ON the door (EX-ACCENT rests at the seams)
    if (!atDoor) ground(w.dom);
    counter.querySelector(".now").textContent = String(+x.target.dataset.n).padStart(2, "0");
    counter.classList.add("show");
    // his words and the archive's facts only — never machine prose, never a readout (INV-1);
    // a REAL series (3+) grows its quiet pill — «серия · N», never the machine's theme (EX-SERIES)
    const serIdx = (typeof w.ser === "number" && SERIES[w.ser]) ? w.ser : null;
    const serWord = ((greetLang() || { t: {} }).t.series) || "серия";
    cap.innerHTML =
      `<div class="title ${w.title ? "" : "untitled"}">${w.title || "untitled"}</div>` +
      `<div class="meta">${w.sec || ""}${w.place ? " · " + w.place : ""}</div>` +
      (serIdx == null ? "" :
        `<button type="button" class="ex-series" data-ser="${serIdx}">` +
        `${serWord} · ${SERIES[serIdx].members.length}</button>`);
    cap.classList.add("show");
  }), { threshold: 0.55 });

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
    toastEl.hidden = true;
    toastEl.classList.remove("hold");
  }
  function toast(text, hold) {
    clearTimeout(toastTimer); toastTimer = null;
    toastEl.textContent = text;
    toastEl.classList.toggle("hold", !!hold);
    toastEl.hidden = false;
    if (!hold) toastTimer = setTimeout(toastOff, Math.round(3000 * TEMPO));
  }
  toastEl.addEventListener("click", toastOff);
  addEventListener("keydown", (ev) => { if (ev.key === "Escape") toastOff(); });

  stage.addEventListener("click", (ev) => {            // ONE delegated listener, O(1) per frame
    const b = ev.target.closest && ev.target.closest(".ex-share");
    if (!b) return;
    const link = ROOT_URL + "/#w-" + b.dataset.share;
    const S = shareStrings();
    const write = (navigator.clipboard && navigator.clipboard.writeText)
      ? navigator.clipboard.writeText(link)
      : Promise.reject(new Error("no clipboard"));
    pulse("share_copy", b.dataset.share);
    write.then(() => toast(S.copied))
         .catch(() => toast(link, true));              // never a silent failure (EX-SHARE-BTN)
  });

  function frameHTML(id, n) {
    const w = byId[id];
    const S = shareStrings();
    return (
      `<section class="exh-frame" data-id="${w.id}" data-n="${n}">` +
        `<img class="work" loading="lazy" src="${w.img}" alt="">` +
        `<button type="button" class="ex-share" data-share="${w.id}"` +
        ` aria-label="${S.label}">${SHARE_GLYPH}</button>` +
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
    const moreLabel = (FT.more || "ещё {n}").replace("{n}", String(UNFOLD));
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
    fin.querySelector("#ex-unfold")?.addEventListener("click", () => {
      if (spentUnfolds() >= MAXU || shown >= order.length) return;   // the unfolding ENDS (INV-30)
      tlog("unfold");
      pulse("walk_unfold");
      const s = shown;
      shown = Math.min(order.length, shown + UNFOLD, CAP);
      appendFrames(order.slice(s, shown), s + 1);
      save();
    });
    fin.querySelector("#ex-return")?.addEventListener("click", doorReturn);
    counter.querySelector(".tot").textContent = String(shown).padStart(2, "0");
  }

  // ---- EX-GLIDE (INV-39): the amortized scroll — the walk settles like breath ----
  // Card 02's law: while the hand moves, nothing yanks; a beat of stillness glides the room
  // to the nearest frame; ANY new input cancels mid-flight — the museum never wrestles.
  let glideRaf = null;
  let gliding = false;                                 // the glide's own motion never re-arms
  let glideGoal = null;                                // where the running glide is headed
  let progAt = 0;                                      // …not even its tail event after a cancel
  function glideCancel() {
    if (glideRaf) { cancelAnimationFrame(glideRaf); glideRaf = null; }
    gliding = false;
  }
  function glideTo(to) {
    glideCancel();
    glideGoal = to;
    const from = scrollY;
    const d = to - from;
    if (Math.abs(d) < 2) return;                       // a sub-2px correction is noise
    // v3 (his 09:31 word: «красивую кривую, асимметричный гистерезис»): length grows with
    // distance, capped; scaled by tempo/default, capped ×1.25 — and a settle that must move
    // AGAINST the hand's last direction (a back-correction) takes a third longer: the room
    // never tugs back briskly (the hysteresis half)
    const dur = Math.min(2400, 950 + Math.abs(d) * 0.75)
      * Math.min(1.25, TEMPO / 1.35)
      * (travel && Math.sign(d) !== travel ? 1.3 : 1);
    const t0 = performance.now();
    // v4 «въезжает вальяжно» (his 09:43 word — the spring's darty middle was the miss): a
    // STATELY roll-in — sine in-out, the calmest of the classic curves (lowest peak speed,
    // soft at both ends), over a long clock; the docking itself stays visibly slow
    const ease = (t) => 0.5 - 0.5 * Math.cos(Math.PI * t);
    gliding = true;
    const step = (now) => {
      const p = Math.min(1, (now - t0) / dur);
      progAt = now;
      scrollTo(0, from + d * ease(p));
      if (p < 1) glideRaf = requestAnimationFrame(step);
      else glideCancel();
    };
    glideRaf = requestAnimationFrame(step);
  }
  // desktop keys PAGE by frame (his word 2026-07-07 morning: «пробел или кнопки вниз/вверх
  // должны плавно допрокручивать на следующую картинку») — the paging keys answer with the
  // same soft glide; every OTHER key stays the hand that wins and cancels
  const PAGE_KEYS = { "ArrowDown": 1, "PageDown": 1, " ": 1, "ArrowUp": -1, "PageUp": -1 };
  ["wheel", "touchstart"].forEach((e) =>               // the hand always wins — and takes
    addEventListener(e, () => { glideCancel(); glideGoal = null; },  // the goal with it
      { passive: true }));
  addEventListener("keydown", (e) => {                 // a non-paging key cancels like a hand
    if (!PAGE_KEYS[e.key]) glideCancel();
  }, { passive: true });
  addEventListener("keydown", (e) => {
    if (!PAGE_KEYS[e.key]) return;
    if (atDoor || busy || sideOpen) return;            // the walk's faces keep their own keys
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    const t = e.target;
    if (t && (t.tagName === "INPUT" || t.tagName === "TEXTAREA" || t.isContentEditable)) return;
    let dir = PAGE_KEYS[e.key];
    if (e.key === " " && e.shiftKey) dir = -1;         // shift+space pages back, as everywhere
    e.preventDefault();                                // the native jump never fights the glide
    if (e.repeat) return;                              // a held key = one frame per press
    const vh = innerHeight;
    const max = document.documentElement.scrollHeight - vh;
    const base = gliding && glideGoal != null ? glideGoal : scrollY;
    const k = Math.round(base / vh) + dir;             // chained presses ride the running goal
    glideTo(Math.min(max, Math.max(0, k * vh)));
  }, { passive: false });
  // on a touch device the settle CONTINUES the hand's direction — a flick that entered the
  // next frame never gets pulled back (his phone report); a pointer keeps plain-nearest
  const TOUCHY = matchMedia("(hover: none)").matches;
  let lastY = 0;
  let travel = 0;                                      // the hand's last direction: +down / -up
  // the idleness detector samples POSITION PER FRAME, never trusts event timing: momentum
  // (iOS, mac trackpads) delivers scroll events in bursts with long gaps — a timer fires in a
  // gap and the glide FIGHTS the still-moving native scroll (his iPhone jerk, 2026-07-07).
  // Only ~0.28s of true WALL-TIME stillness opens the glide — Still no tempo scaling (a detector).
  let watchRaf = null;
  function watchCancel() {
    if (watchRaf) { cancelAnimationFrame(watchRaf); watchRaf = null; }
  }
  function watchSettle() {
    if (watchRaf) return;                              // one watcher at a time
    let last = scrollY;
    let movedAt = performance.now();
    const tick = (now) => {
      watchRaf = null;
      if (gliding || atDoor || busy) return;           // the glide/door/ceremony own motion now
      const y = scrollY;
      if (Math.abs(y - last) >= 0.6) movedAt = now;    // stillness is WALL TIME, frames only
      last = y;                                        // sample it (60 vs 120Hz must not matter)
      if (now - movedAt < 280) { watchRaf = requestAnimationFrame(tick); return; }
      const vh = innerHeight;                          // TRUE stillness — settle (EX-GLIDE)
      const max = document.documentElement.scrollHeight - vh;
      const raw = y / vh;
      let k = Math.round(raw);
      if (TOUCHY && travel) {
        const frac = raw - Math.floor(raw);
        if (travel > 0) k = frac >= 0.12 ? Math.ceil(raw) : Math.floor(raw);
        else k = frac <= 0.88 ? Math.floor(raw) : Math.ceil(raw);
      }
      glideTo(Math.min(max, Math.max(0, k * vh)));
    };
    watchRaf = requestAnimationFrame(tick);
  }
  addEventListener("scroll", () => {
    if (gliding || performance.now() - progAt < 80) { lastY = scrollY; return; }
    travel = scrollY > lastY ? 1 : (scrollY < lastY ? -1 : travel);
    lastY = scrollY;
    watchSettle();
  }, { passive: true });

  function renderHang() {
    tlog("hang");
    document.documentElement.classList.add("ex-walk");   // the walk's face (geometry in CSS)
    stage.innerHTML = "";
    appendFrames(order.slice(0, shown), 1);
    scrollTo(0, 0);
  }

  // ---- EX-SERIES (INV-46): the side room — theme and variations, a look ASIDE --------
  // A FACE over the walk: opening lays ONE history step; the page locks beneath (the
  // threshold's own law); chip, Esc and Back all land the guest on the exact frame left.
  const side = document.createElement("div");
  side.id = "ex-side";
  side.hidden = true;
  side.innerHTML = '<button type="button" class="exs-back"></button>' +
                   '<div class="exs-stage" id="exs-stage"></div>';
  document.body.appendChild(side);
  let sideOpen = false;
  function openSide(idx, laystep) {
    const S = SERIES[idx];
    if (!S || sideOpen) return;
    sideOpen = true;
    const st = side.querySelector("#exs-stage");
    st.className = "exs-stage " + S.variant;           // the series' own character picks the face
    st.innerHTML = "";
    S.members.forEach((id, i) => {
      const w = byId[id];
      if (!w) return;
      if (S.variant === "lane") {
        const im = new Image();
        im.src = w.img;
        st.appendChild(im);
        return;
      }
      const p = document.createElement("div");         // the polaroid table
      p.className = "exs-print";
      p.style.left = (8 + (i % 5) * 17 + (i * 7) % 5) + "%";
      p.style.top = (12 + Math.floor(i / 5) * 26 + (i * 11) % 7) + "%";
      p.style.setProperty("--rot", ((((i * 37) % 13) - 6)) + "deg");
      p.innerHTML = '<img src="' + w.img + '" alt="">';
      p.addEventListener("click", () => {
        const was = p.classList.contains("lift");
        st.querySelectorAll(".exs-print").forEach((x) => x.classList.remove("lift"));
        if (!was) {
          const r = p.getBoundingClientRect();
          p.style.setProperty("--cx", (innerWidth / 2 - (r.left + r.width / 2)) + "px");
          p.style.setProperty("--cy", (innerHeight / 2 - (r.top + r.height / 2)) + "px");
          p.classList.add("lift");
        }
      });
      st.appendChild(p);
    });
    const T = (greetLang() || { t: {} }).t;
    side.querySelector(".exs-back").textContent = T.room_back || "← комната";
    side.hidden = false;
    document.body.classList.add("ex-side");            // the lock law, reused (EX-DOOR-2f)
    if (laystep !== false) pushFace({ face: "series", ser: idx });
    pulse("series_open");
  }
  function closeSide() {
    if (!sideOpen) return;
    sideOpen = false;
    side.hidden = true;
    document.body.classList.remove("ex-side");
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

  // ---- the walk TRACKS its place (INV-32c — the law outlived the ↗, its first carrier):
  // the io callback above writes the per-tab marker per frame in view; any return within
  // the tab (reload, the work page's plain link, Back) restores it
  function restorePlace() {
    let m = null;
    try { m = JSON.parse(sessionStorage.getItem(PLACE_KEY) || "null"); } catch (e) {}
    try { sessionStorage.removeItem(PLACE_KEY); } catch (e) {}   // one-shot
    if (!m || m.v !== VER) return;                     // stale/foreign marker → the top, never an error
    const f = stage.querySelector('.exh-frame[data-id="' + m.id + '"]');
    if (f) f.scrollIntoView({ behavior: "instant" });
  }

  // ---- the permalink arrival (EX-SHARE-IN): the hash is a doorway, not a leash ----
  // #w-<id> = a handed-over pick: among the SHOWN frames → instant jump, the arc unchanged;
  // otherwise → acts as a pick (fresh-top, the door passed, no greeting). Consumed once per
  // hand-over (per-tab spent marker); it stays in the address and lays no step of its own.
  function consumeHash() {
    const m = location.hash.match(/^#w-([\w-]+)$/);
    const hid = m && m[1];
    if (!hid || !byId[hid]) return null;               // unknown id changes nothing (c)
    let spent = null;
    try { spent = sessionStorage.getItem(SPENT_KEY); } catch (e) {}
    return spent === "w-" + hid ? null : hid;          // INV-32c wins once the hash is spent
  }
  function arriveByHash(hid) {
    tlog("handover");
    pulse("share_arrive", hid);
    const shownIds = entered ? order.slice(0, shown) : [];
    if (!(entered && shownIds.indexOf(hid) >= 0)) {    // (b) acts as a pick — fresh-top,
      pick = hid;                                      // the same law a door pick lives by
      order = arcOrder(pick);
      shown = SPREAD;                                  // the budget stays derived+capped (INV-30)
      entered = true;
      if (atDoor) closeDoor();
      ground(byId[hid].dom);
      renderHang();
      save();
    } else {                                           // (a) already hangs — the walk continues,
      if (atDoor) closeDoor();                         // «выставка не рвётся»
      ground(byId[hid].dom);
      if (!stage.querySelector(".exh-frame")) renderHang();
    }
    replaceFace({ face: "walk" });                     // no step of its own (INV-32e)
    try { sessionStorage.setItem(SPENT_KEY, "w-" + hid); } catch (e) {}
    const f = stage.querySelector('.exh-frame[data-id="' + hid + '"]');
    if (f) f.scrollIntoView({ behavior: "instant" });  // no smooth-scroll tear
    // the consuming jump writes the place marker so the room's memory agrees with the eye
    try { sessionStorage.setItem(PLACE_KEY, JSON.stringify({ v: VER, id: hid })); } catch (e) {}
  }
  addEventListener("hashchange", () => {               // a pasted room link IS an arrival too
    const hid = consumeHash();
    if (!hid) return;
    ceremonyCancel();
    arriveByHash(hid);
  });

  // ---- boot -----------------------------------------------------------------
  entered = restore();
  document.body.classList.add("ex-live");              // hide the static index, wake the live face
  const handed = consumeHash();
  if (handed) {
    arriveByHash(handed);                              // the shared work itself is the welcome
  } else if (entered) {
    if (pick) ground(byId[pick] && byId[pick].dom);
    renderHang();                                      // a return visit continues its walk — no door
    replaceFace({ face: "walk" });                     // the standing entry is a walk step (INV-32)
    restorePlace();                                    // the ↗ round-trip keeps the place (INV-32c)
  } else if (doorAvailable) {
    const sp = dealHand();                             // a cold ARRIVAL deals a fresh hand (EX-DOOR-3)
    renderDoor(sp, true);                              // a cold visitor meets the threshold — greeted
    replaceFace({ face: "door", spread: sp.map((e) => e.id), cold: true });
  } else {
    entered = true;                                    // no/thin pool → the diverse hang directly,
    renderHang();                                      // never a block (EX-DOOR-2a: the skip's old
    save();                                            // mechanism, internal only now)
    replaceFace({ face: "walk" });
  }

  // ---- EX-I18N (INV-42): the museum speaks ANY language — after first paint ----
  // A locale outside the baked seven meets the fallback INSTANTLY; the site then quietly asks
  // its own worker for that locale's set (once per language-version, ever), keeps a browser
  // copy, and the standing surfaces re-speak without a jump. A dead worker changes nothing.
  function respeak() {
    const L = greetLang();
    if (!L) return;
    const T = L.t;
    if (atDoor) {
      door.setAttribute("dir", T.dir === "rtl" ? "rtl" : "ltr");
      door.setAttribute("lang", L.code);
      door.querySelector(".exd-ask").textContent = T.ask || "что ближе сейчас";
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
    const fin = document.getElementById("exh-fin");
    if (fin) {
      fin.setAttribute("lang", L.code);
      fin.setAttribute("dir", T.dir === "rtl" ? "rtl" : "ltr");
      const u = fin.querySelector("#ex-unfold");
      const b = fin.querySelector("#ex-return");
      const q = fin.querySelector(".q");
      if (q) q.textContent = u ? (T.q_more || q.textContent) : (T.q_spent || q.textContent);
      if (u) u.textContent = (T.more || "ещё {n}").replace("{n}", String(UNFOLD)) + " ↓";
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
    window.__tlvSeen = (id) => {
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
    const CK = "tlv.i18n." + VER + "." + code;
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
    const browserCode = (navigator.language || "").toLowerCase().slice(0, 2);
    const codes = Object.keys(GREET.langs).slice();
    if (I18N_ON && /^[a-z]{2,3}$/.test(browserCode)
        && !GREET.langs[(GREET.aliases || {})[browserCode] || browserCode]
        && codes.indexOf(browserCode) < 0) {
      codes.push(browserCode);                         // the guest's own outsider tongue
    }
    const markOf = () => {
      const c = viewerLang();
      return ((GREET.aliases || {})[c] || c).toUpperCase().slice(0, 2) || "EN";
    };
    const redraw = () => {
      cur.textContent = markOf();
      list.querySelectorAll(".exl-item").forEach((b) =>
        b.classList.toggle("cur", b.dataset.lang === viewerLang()));
    };
    codes.forEach((c) => {
      const b = document.createElement("button");
      b.type = "button"; b.className = "exl-item";
      b.dataset.lang = c;
      b.textContent = c.toUpperCase();
      b.addEventListener("click", (ev) => {
        ev.stopPropagation();
        langOverride = c;
        try { localStorage.setItem(LANG_KEY, c); } catch (e) {}
        list.hidden = true;
        const known = (GREET.aliases || {})[c] || c;
        if (GREET.langs[known]) respeak();             // a baked tongue answers at once
        else requestSet(c);                            // an outsider rides the one layer
        redraw();
      });
      list.appendChild(b);
    });
    cur.addEventListener("click", (ev) => {
      ev.stopPropagation();
      list.hidden = !list.hidden;
    });
    door.addEventListener("click", () => { list.hidden = true; });
    redraw();
  }
})();
