  // EX-DOOR-4 (INV-71): the walk's own in-session seen marks — every hung frame that has stood
  // in view THIS session, added the MOMENT the mark is made (pending flush included, since this
  // set is written synchronously in the intersection callback). It feeds the circle check and the
  // next deal's novelty voice even where the museum's memory (visitor_memory / ex.seenc) is off.
  const walkSeen = new Set();

  // EX-DOOR-3 (door_diversity): a FRESH, evenly-spread, place-guaranteed set every open. The pool
  // spans the whole living gallery (baked with five axes + a `place` flag). We min-max normalize the
  // five axes, SEED near the set's centre among the works UNSEEN this round (a random pick among the
  // closest few — the variety knob per open), then greedily add the work FARTHEST from the picked set
  // while keeping both quotas reachable: at least PLACE_MIN place works and at least FRESH_MIN works
  // unseen this round (INV-75 — else the farthest-point spread keeps surfacing the same extreme poles).
  // The unseen memory is per-round: when it can no longer honour either fraction the round resets and
  // the whole gallery is walked again. The ORDER varies too — a random axis and direction each open,
  // since there is no single right order over these axes.
  const DPARAMS = ["luma", "warmth", "colorful", "edge", "sym"];
  function dealDiverse(want) {
    const pool = doorPool;
    const n = Math.max(1, Math.min(want || DOOR_SIZE, pool.length));
    if (pool.length <= n) return pool.slice(0, n);
    const mins = {}, maxs = {};
    DPARAMS.forEach((p) => {
      let lo = Infinity, hi = -Infinity;
      pool.forEach((e) => { const v = Number(e[p]);
        if (Number.isFinite(v)) { if (v < lo) lo = v; if (v > hi) hi = v; } });
      mins[p] = lo; maxs[p] = hi;
    });
    const V = pool.map((e) => DPARAMS.map((p) => {
      const span = maxs[p] - mins[p];
      return span > 0 ? (Number(e[p]) - mins[p]) / span : 0;
    }));
    const d2 = (a, b) => { let s = 0; for (let i = 0; i < a.length; i++) { const t = a[i] - b[i]; s += t * t; } return s; };
    const minTo = (i, set) => { let m = Infinity; for (const j of set) { if (j === i) continue; const dd = d2(V[i], V[j]); if (dd < m) m = dd; } return m; };
    const isPlace = (i) => !!pool[i].place;
    // INV-75 — novelty across visits: the round memory of works this door has already dealt. Each open
    // must show ≥ FRESH_MIN works NOT in this memory (else the farthest-point spread, which always
    // gravitates to the same extreme poles, would show a returning phone visitor the same faces). When
    // the unseen pool can no longer honour the fresh OR the place fraction the round is SPENT — the
    // memory clears and a fresh round walks the whole gallery again (the just-dealt set re-seeds it).
    let shown = new Set();
    try {
      const s = JSON.parse(localStorage.getItem(DOORDEALT_KEY) || "null");
      if (s && s.v === VER && Array.isArray(s.ids)) s.ids.forEach((id) => shown.add(String(id)));
    } catch (e) {}
    const needPlace = Math.min(n, Math.ceil(PLACE_MIN * n));
    const needFresh = Math.min(n, Math.ceil(FRESH_MIN * n));
    // both fractions together want more than n works (0.6n + 0.6n > n), so some shown windows must be
    // BOTH unseen AND place — this many at least (the joint overlap the deal must honour):
    const overlapNeed = Math.max(0, needFresh + needPlace - n);
    let isFresh = (i) => !shown.has(String(pool[i].id));
    const tally = (pred) => { let c = 0; for (let i = 0; i < pool.length; i++) if (pred(i)) c++; return c; };
    // the round is spent when the unseen pool can't supply the fresh floor OR the fresh∧place overlap
    // both quotas jointly demand → clear it and walk the whole gallery again
    if (tally(isFresh) < needFresh || tally((i) => isFresh(i) && isPlace(i)) < overlapNeed) {
      shown = new Set();                                  // the round is spent → a new round over the whole pool
      isFresh = () => true;                               // every work is fresh again
    }
    // both quotas hold together because we only ADD a work when the remaining slots can still be filled
    // to meet the fresh AND place counts (a small feasibility test), and among the still-feasible works
    // we take the FARTHEST (spread), with stale works discounted so fresh is preferred while the pool is deep.
    const feasibleAfter = (cand, picked, fc, pc) => {
      const nfc = fc + (isFresh(cand) ? 1 : 0), npc = pc + (isPlace(cand) ? 1 : 0);
      const nSlots = n - picked.length - 1;              // slots left AFTER adding cand
      const rf = Math.max(0, needFresh - nfc), rp = Math.max(0, needPlace - npc);
      if (rf > nSlots || rp > nSlots) return false;
      let af = 0, ap = 0, afp = 0;                        // fresh / place / both, among unpicked ≠ cand
      for (let k = 0; k < pool.length; k++) {
        if (k === cand || picked.indexOf(k) >= 0) continue;
        const f = isFresh(k), p = isPlace(k);
        if (f) af++;
        if (p) ap++;
        if (f && p) afp++;
      }
      return af >= rf && ap >= rp && afp >= Math.max(0, rf + rp - nSlots);
    };
    // seed near the centre among FRESH works — a novel yet still-typical start each open
    const mean = DPARAMS.map((_, k) => V.reduce((s, v) => s + v[k], 0) / V.length);
    const freshIdx = pool.map((_, i) => i).filter(isFresh);
    const seedFrom = (freshIdx.length ? freshIdx : pool.map((_, i) => i))
      .sort((a, b) => d2(V[a], mean) - d2(V[b], mean));
    const seedK = Math.min(seedFrom.length, Math.max(3, Math.ceil(pool.length * 0.15)));
    const picked = [seedFrom[Math.floor(Math.random() * seedK)]];
    let fc = isFresh(picked[0]) ? 1 : 0, pc = isPlace(picked[0]) ? 1 : 0;
    while (picked.length < n) {                           // greedy farthest-point, quota-feasible + fresh-first
      let best = -1, bd = -Infinity, bestAny = -1, bdAny = -Infinity;
      for (let i = 0; i < pool.length; i++) {
        if (picked.indexOf(i) >= 0) continue;
        let md = minTo(i, picked);
        if (!isFresh(i)) md *= 0.15;                      // discount stale → fresh preferred while pool is deep
        if (md > bdAny) { bdAny = md; bestAny = i; }
        if (md > bd && feasibleAfter(i, picked, fc, pc)) { bd = md; best = i; }
      }
      const add = best >= 0 ? best : bestAny;             // feasibility keeps a candidate; fallback is a safety net
      picked.push(add);
      if (isFresh(add)) fc++;
      if (isPlace(add)) pc++;
    }
    const axis = Math.floor(Math.random() * DPARAMS.length);   // varying order: a random axis + direction
    const dir = Math.random() < 0.5 ? 1 : -1;
    picked.sort((a, b) => dir * (V[a][axis] - V[b][axis]));
    const hand = picked.map((i) => pool[i]);
    try {                                                 // remember what this open dealt (this round's memory)
      hand.forEach((e) => shown.add(String(e.id)));
      localStorage.setItem(DOORDEALT_KEY, JSON.stringify({ v: VER, ids: Array.from(shown).slice(-500) }));
    } catch (e) {}
    return hand;
  }

  // EX-DOOR-3 (INV-44): the hand LIVES — rotation + novelty + the hour, under HIS LAW
  // (a new hand repeats at most a THIRD of the previous one). The pool stays curated
  // (EX-DOOR-2d); his file order is the tie-break voice; a pool of exactly door_size
  // stands the law down (the hand IS the pool). `circleStamp` (EX-DOOR-4) records the circle
  // (pick + shown) this deal answered, so one circle earns exactly one deal.
  function dealHand(circleStamp) {
    if (DIVERSE) return dealDiverse(doorLayout().n);     // door_diversity: a fresh spread set every open
    const n = Math.min(DOOR_SIZE, doorPool.length);
    if (doorPool.length <= n) return doorPool.slice(0, n);
    let prev = [];
    try {
      const h = JSON.parse(localStorage.getItem(HAND_KEY) || "null");
      if (h && h.v === VER && Array.isArray(h.ids)) prev = h.ids;
    } catch (e) {}
    const seen = new Set(walkSeen);                    // the just-walked works count as met (EX-DOOR-4)
    try {
      const c = JSON.parse(localStorage.getItem(SEENC_KEY) || "null");
      if (c && Array.isArray(c.ids)) c.ids.forEach((id) => seen.add(String(id)));
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
    const rec = { v: VER, ids: hand.map((e) => e.id) };
    if (circleStamp) rec.circle = circleStamp;         // remember the circle this deal answered
    try { localStorage.setItem(HAND_KEY, JSON.stringify(rec)); } catch (e) {}
    return hand;
  }
  function standingHand() {                            // the session keeps its set (INV-31/2d)
    if (DIVERSE) return null;                            // door_diversity overrides INV-31 for the door —
    // every open re-deals a fresh spread set (his word 2026-07-12); the walk behind still persists
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
  function shuffle(a) {                                 // Fisher–Yates, in place
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1)); const t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }
  function refreshHand() {
    if (DIVERSE) return dealDiverse(doorLayout().n);     // door_diversity: a reload deals fresh too (his word 2026-07-12)
    // EX-DOOR-RELOAD (INV-54): the gentle cousin of the cold deal — a RELOAD keeps the door face and
    // swaps in ≤40% NEW works, so the threshold feels alive on reload yet cannot be reloaded into a
    // tour of the whole library (dealHand's ≥⅔-new is only a COLD arrival or the exit's fresh quiz).
    const standing = standingHand();
    if (!standing) return dealHand();                  // no stored hand → a normal deal
    const n = standing.length;
    const swapN = Math.floor(n * 0.4);                 // ≤40% turns over; the rest is held
    if (swapN < 1 || doorPool.length <= n) return standing;   // too small / no room → hold it whole
    const idx = shuffle(standing.map((_, i) => i)).slice(0, swapN);
    const drop = new Set(idx);
    const kept = standing.filter((_, i) => !drop.has(i));
    const held = new Set(standing.map((e) => e.id));    // never re-add a work already in the hand
    const fresh = shuffle(doorPool.filter((e) => !held.has(e.id)));
    const hand = shuffle(kept.concat(fresh.slice(0, swapN)));
    const rec = { v: VER, ids: hand.map((e) => e.id) };
    const cc = consumedCircle();                        // a reload keeps the consumed-circle memory
    if (cc) rec.circle = cc;                            // (EX-DOOR-4: one circle, one deal survives reloads)
    try { localStorage.setItem(HAND_KEY, JSON.stringify(rec)); } catch (e) {}
    return hand;
  }

  // ---- EX-DOOR-4 (INV-71): the full circle retires the hand -------------------
  // A walk is "circled" when every work of its current hang — order.slice(0, shown), the spread
  // plus every unfold taken — has stood in view (walkSeen, the in-session marks, joined with the
  // persisted seen copy so a reload still knows; F3: counted the moment marks are made). The NEXT
  // door render over a circled, not-yet-answered walk deals a fresh EX-DOOR-3 hand — the exit
  // control, the browser's own Back, and a returned-door reload behave alike (F1/F2 folded 11:50);
  // on this one point the history's "as it stood" (INV-32a) yields, the fresh hand standing as THE
  // standing hand from that moment on. One circle, one deal: the fresh hand remembers the circle
  // (pick + shown) it answered, so walking door↔walk over the same circle never re-rolls. A hand
  // with no circle field (an older client) reads as "no circle consumed" (F4).
  function consumedCircle() {
    try {
      const h = JSON.parse(localStorage.getItem(HAND_KEY) || "null");
      if (h && h.v === VER && h.circle && h.circle.pick != null) return h.circle;
    } catch (e) {}
    return null;
  }
  function walkCircled() {
    if (pick == null) return false;
    const need = order.slice(0, shown).map(String);
    if (!need.length) return false;
    const seen = new Set(walkSeen);
    try {
      const c = JSON.parse(localStorage.getItem(SEENC_KEY) || "null");
      if (c && Array.isArray(c.ids)) c.ids.forEach((id) => seen.add(String(id)));
    } catch (e) {}
    return need.every((id) => seen.has(id));
  }
  function circlePending() {              // a circle not yet answered by the standing hand
    if (!walkCircled()) return null;
    const cur = { pick: pick, shown: shown };
    const cc = consumedCircle();
    if (cc && String(cc.pick) === String(cur.pick) && cc.shown === cur.shown) return null;
    return cur;
  }
  // the hand for a door render, honouring the carve-out: a pending circle deals fresh ONCE, else
  // `fallback` (the standing set — EX-DOOR-2d — or the reload refresh) holds.
  function doorHand(fallback) {
    const pend = circlePending();
    return pend ? dealHand(pend) : fallback();
  }

  // one line, always (EX-DOOR-2b — card 01's algorithm IS the norm): a row when landscape
  // (W/H > 1.02), a column when portrait; windows shrink first, the count drops second
  // (row 5→4→3 while each keeps ≥118px; column 3→2 below 104px); never a second line
  // how many windows FIT a viewport of the given W×H (the count only, no sizing)
  function doorFit(W, H) {
    const col = W / H <= 1.02;
    if (!col) {
      const gap = Math.max(16, Math.min(44, W * 0.03));
      const cap = Math.min(190, H * 0.42);
      let n = Math.min(DOOR_SIZE, doorPool.length);
      for (; n > 3; n--) { if (Math.min(cap, (W * 0.88 - (n - 1) * gap) / n) >= 118) break; }
      return n;
    }
    const gap = Math.max(14, Math.min(30, H * 0.025));
    const cap = Math.min(190, W * 0.62);
    let n = Math.min(3, doorPool.length);
    if (Math.min(cap, (H * 0.52 - (n - 1) * gap) / n) < 104 && n > 2) n = 2;
    return n;
  }
  // the door's window count HOLDS across a rotation: it is the running MINIMUM that has fit this
  // load, so turning the phone never ADDS windows (his word 2026-07-12: «не добавлять при повороте,
  // смотрим минимальное и придерживаемся»). A wide screen that never rotates keeps its full count.
  let doorNMin = Infinity;
  function doorLayout() {
    const W = innerWidth, H = innerHeight, col = W / H <= 1.02;
    doorNMin = Math.min(doorNMin, doorFit(W, H));
    const n = Math.max(2, doorNMin);
    let gap, size;
    if (!col) {
      gap = Math.max(16, Math.min(44, W * 0.03));
      size = Math.min(Math.min(190, H * 0.42), (W * 0.88 - (n - 1) * gap) / n);
    } else {
      gap = Math.max(14, Math.min(30, H * 0.025));
      size = Math.min(Math.min(190, W * 0.62), (H * 0.52 - (n - 1) * gap) / n);
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
      pick = st.pick; order = assembleOrder(pick);
      recomputeQuizChoice();   // INV-66: re-establish after the restored order is known
    }
    // the unfold budget DERIVES from shown, never trusted (INV-30 holds on restore)
    shown = clampInt(st.shown, SPREAD, SPREAD, Math.min(order.length, CAP));
    return true;
  }
  const spentUnfolds = () => Math.max(0, Math.floor((shown - SPREAD) / UNFOLD));

