/* exhibition.js — the adaptive exhibition (EX).
   The JS-on face of `/`: re-renders the crawlable static index into a live, personal walk.
   A COLD arrival meets the DOOR first (EX-DOOR): door_size of his photos asking wordlessly
   "which is closer?" — the tap IS the resonance seed; a quiet skip leads to the default hang.
   The gallery keeps a quiet EXIT back to the threshold (INV-31 — no one-way faces), and the
   unfolding ENDS (INV-30 — value over volume, budget derived, never trusted from storage).
   Every knob of the feel is read from config.json → exhibition (INV-28) — no magic constants here.
   Kinship math runs entirely in the browser on baked vectors ($0, no server — the AI-OFF experience).
   It renders NO axis name, score, or confidence (INV-1): figures carry only the work id + image. */
(async function () {
  "use strict";
  const stage = document.getElementById("ex-stage");
  const moreWrap = document.getElementById("ex-more-wrap");
  const moreBtn = document.getElementById("ex-more");
  const head = document.getElementById("ex-hint");
  if (!stage) return;                                 // no live root → JS-off face stays

  let cfg, data;
  try {
    [cfg, data] = await Promise.all([
      fetch("config.json").then((r) => r.json()),
      fetch("exhibition_data.json").then((r) => r.json()),
    ]);
  } catch (e) {
    // any fetch failure → restore the static face NOW (don't wait out the head-script timer) (CS-8)
    document.documentElement.classList.remove("js");
    return;
  }

  // ---- feel knobs, all from config (INV-28) ---------------------------------
  const EX = cfg.exhibition || {};
  const clampInt = (x, dflt, lo, hi) => {
    const n = parseInt(x, 10);
    return Number.isFinite(n) ? Math.max(lo, Math.min(hi, n)) : dflt;
  };
  const SPREAD = clampInt(EX.spread_size, 10, 3, 12);   // a wall of ~10, never the whole catalogue
  const UNFOLD = clampInt(EX.unfold_step, 5, 1, 12);
  const ROW = clampInt(EX.row_size, 4, 2, 6);           // works per row on a wide screen
  const MAXU = clampInt(EX.max_unfolds, 2, 0, 5);       // unfold steps before "more" retires (INV-30)
  const DOOR_SIZE = clampInt(EX.door_size, 5, 3, 5);    // works at the threshold (EX-DOOR)
  const TMS = Number(EX.transition_ms) || 620;
  const COLD = EX.cold_spread || "diverse";
  const ARC = EX.arc_shape || "widening";
  const AXES = EX.kinship_axes || "all";
  const CAP = SPREAD + MAXU * UNFOLD;                   // one arc never shows more (INV-30)
  document.documentElement.style.setProperty("--ex-tms", TMS + "ms");
  document.documentElement.style.setProperty("--ex-row", ROW);    // wall rhythm on laptop (INV-27)

  // ---- baked data -----------------------------------------------------------
  const VER = String(data.version || "1");
  const works = data.works;                           // [{id,img,slug,w,h,dom:[r,g,b]}]
  const byId = Object.fromEntries(works.map((w) => [w.id, w]));
  const V = data.v;                                   // {id:[floats]} — neutral coords, no axis names
  const DIM = V[works[0].id].length;
  const sel = Array.isArray(AXES) ? AXES.filter((i) => i >= 0 && i < DIM)
                                  : [...Array(DIM).keys()];
  const vec = (id) => sel.map((i) => V[id][i]);
  const dist = (a, b) => {
    let s = 0;
    for (let i = 0; i < a.length; i++) { const d = a[i] - b[i]; s += d * d; }
    return Math.sqrt(s);
  };

  // the door pool — baked provenance ids intersected with the living works; a pool thinner than
  // door_size (or absent, or broken) means NO door: silent entry onto the default hang (EX-DOOR
  // never blocks entry)
  const doorPool = ((data.door || {}).pool || [])
    .filter((e) => e && byId[e.id]);
  const doorAvailable = doorPool.length >= DOOR_SIZE;

  // ---- orderings ------------------------------------------------------------
  // cold spread → maximally diverse full ordering (farthest-point sampling)
  function coldOrder() {
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

  // arc from a pick → full ordering, near neighbours drawn in with widening steps so contrast is
  // held (never all-nearest); the remainder appended by distance. "open more" reveals more of THIS
  // order, so already-seen works keep their positions (INV-29).
  function arcOrder(pickId) {
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
    for (const w of sorted) if (!used.has(w.id)) { order.push(w.id); used.add(w.id); }  // fill skipped
    return order;
  }

  // the door's spread — date-seeded deterministic rotation (clean A/B readouts), turned one notch
  // each time the door re-opens within a visit (the exit's "fresh quiz", INV-31)
  let doorTurns = 0;
  function doorSpread() {
    const day = new Date().toISOString().slice(0, 10);
    let h = 0;
    for (const c of day) h = (h * 31 + c.charCodeAt(0)) >>> 0;
    const off = (h + doorTurns) % doorPool.length;
    const out = [];
    for (let i = 0; i < DOOR_SIZE; i++) out.push(doorPool[(off + i) % doorPool.length]);
    return out;
  }

  // ---- state + persistence (INV-26) -----------------------------------------
  const KEY = "tlv.exhibition";
  let pick = null;        // id of the resonant work, or null for the default hang
  let order = coldOrder();
  let shown = SPREAD;
  let atDoor = false;     // the threshold face is showing (EX-DOOR)
  let entered = false;    // the visitor has a walk behind the door (exit-skip returns to it untouched)

  function save() {
    try { localStorage.setItem(KEY, JSON.stringify({ v: VER, pick, shown })); } catch (e) {}
  }
  function restore() {
    let st;
    try { st = JSON.parse(localStorage.getItem(KEY) || "null"); } catch (e) { st = null; }
    if (!st || st.v !== VER) return false;            // old-version state → ignore, clean start
    if (st.pick != null) {
      if (!byId[st.pick]) return false;               // pick no longer exists → drop → clean cold
      pick = st.pick; order = arcOrder(pick);
    }
    // the unfold budget is DERIVED from what a stored walk had seen, never trusted: a tampered or
    // pre-cap value can never grant unlimited "more" (INV-30 holds on restore)
    shown = clampInt(st.shown, SPREAD, SPREAD, Math.min(order.length, CAP));
    return true;
  }
  const spentUnfolds = () => Math.max(0, Math.floor((shown - SPREAD) / UNFOLD));

  // ---- rendering (FLIP reflow — reassemble, never blink or reload) -----------
  function ground(id) {
    const w = byId[id];
    if (!w || !w.dom) return;
    document.documentElement.style.setProperty("--ex-gx", (32 + (w.dom[0] / 255) * 36) + "%");
    document.documentElement.style.setProperty("--ex-gy", (30 + (w.dom[2] / 255) * 30) + "%");
  }

  function figureHTML(id) {
    const w = byId[id];
    return (
      '<figure class="ex-work" data-id="' + w.id + '">' +
        '<img src="' + w.img + '" alt="" loading="lazy" ' +
          "onerror=\"this.closest('figure').style.display='none'\">" +
        '<a class="ex-open" href="' + w.slug + '" aria-label="Open this work">↗</a>' +
      "</figure>"
    );
  }

  // a door work: keyboard-reachable, alt text from his title/caption, NO ↗ affordance —
  // at the threshold there are only the works and the skip (EX-DOOR)
  function doorFigureHTML(e) {
    const w = byId[e.id];
    const alt = (e.alt || "").replace(/"/g, "&quot;");
    return (
      '<figure class="ex-work ex-door-work" data-id="' + w.id + '" tabindex="0" role="button"' +
        ' aria-label="' + alt + '">' +
        '<img src="' + w.img + '" alt="' + alt + '" loading="eager" ' +
          "onerror=\"this.closest('figure').style.display='none'\">" +
      "</figure>"
    );
  }

  function render() {
    if (atDoor) { renderDoor(); return; }
    document.body.classList.remove("ex-door");
    document.documentElement.style.setProperty("--ex-row", ROW);
    const list = order.slice(0, shown);
    const first = {};
    stage.querySelectorAll("figure").forEach((f) => (first[f.dataset.id] = f.getBoundingClientRect()));
    stage.innerHTML = list.map(figureHTML).join("");
    stage.querySelectorAll("figure").forEach((f) => {
      const id = f.dataset.id;
      // focus reads at a glance: the picked work stays lit, the others recede gently (EX-WALK)
      if (id === pick) f.classList.add("picked");
      else if (pick) f.classList.add("dim");
      const fr = first[id];
      if (fr) {                                        // FLIP: play from old box to new
        const nr = f.getBoundingClientRect();
        const dx = fr.left - nr.left, dy = fr.top - nr.top;
        if (dx || dy) {
          f.style.transition = "none";
          f.style.transform = "translate(" + dx + "px," + dy + "px)";
          requestAnimationFrame(() => { f.style.transition = ""; f.style.transform = ""; });
        }
      } else {                                         // new arrival → fade in
        f.style.opacity = 0;
        requestAnimationFrame(() => { f.style.opacity = ""; });
      }
      f.addEventListener("click", (e) => {
        if (e.target.closest(".ex-open")) return;      // the open link navigates; never resonance
        choose(id);
      });
    });
    // "open more" retires when the arc is spent OR the budget is (INV-30); never a dead control
    if (moreBtn) moreBtn.hidden = shown >= order.length || spentUnfolds() >= MAXU;
    if (exitBtn) exitBtn.hidden = false;
    if (skipBtn) skipBtn.hidden = true;
    if (head) head.textContent = pick
      ? "the walk is tuned to your eye — tap another, or open more"
      : "tap the one that pulls you — the exhibition assembles under you";
  }

  // the threshold: door_size works, wordless, the quiet skip — nothing else (EX-DOOR)
  function renderDoor() {
    document.body.classList.add("ex-door");
    document.documentElement.style.setProperty("--ex-row", DOOR_SIZE);
    const spread = doorSpread();
    stage.innerHTML = spread.map(doorFigureHTML).join("");
    stage.querySelectorAll("figure").forEach((f) => {
      f.style.opacity = 0;
      requestAnimationFrame(() => { f.style.opacity = ""; });
      const act = () => chooseFromDoor(f.dataset.id);
      f.addEventListener("click", act);
      f.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); act(); }
      });
    });
    if (moreBtn) moreBtn.hidden = true;
    if (exitBtn) exitBtn.hidden = true;
    if (skipBtn) skipBtn.hidden = false;
    if (head) head.textContent = "";                   // the door asks wordlessly
  }

  // ---- interaction ----------------------------------------------------------
  let busy = false;                                    // ignore taps mid-reassembly (EX-WALK)
  function lock() { busy = true; setTimeout(() => (busy = false), TMS); }

  function choose(id) {
    if (busy) return;
    lock();
    pick = id;
    order = arcOrder(id);
    shown = SPREAD;                                    // a fresh arc = a fresh unfold budget (INV-30)
    ground(id);
    render();
    save();
  }

  // a door tap IS the resonance seed — same semantics, same in-flight lock (EX-DOOR)
  function chooseFromDoor(id) {
    if (busy) return;
    atDoor = false;
    entered = true;
    choose(id);
  }

  // the quiet skip → the default hang; from a re-entered door it returns to the walk UNTOUCHED
  function doorSkip() {
    if (busy) return;
    atDoor = false;
    if (entered) { render(); return; }                 // stored walk survives the visit (INV-31)
    entered = true;
    render();
    save();                                            // a silent entry is still an entry (no re-ask)
  }

  // the gallery's quiet exit → the threshold again, a fresh quiz (INV-31 — no one-way faces)
  function doorExit() {
    if (busy || !doorAvailable) return;
    doorTurns += 1;                                    // the rotation turns to a new set
    atDoor = true;
    renderDoor();
  }

  function openMore() {
    if (busy || shown >= order.length || spentUnfolds() >= MAXU) return;   // the unfolding ENDS (INV-30)
    lock();
    shown = Math.min(order.length, shown + UNFOLD, CAP);
    render();
    save();
  }

  if (moreBtn) moreBtn.addEventListener("click", openMore);
  // (the "all works" full-catalogue reveal was REMOVED same day it was added — Alexander, evening
  // review 2026-07-05: the wall shows ~10 and unfolds by steps, never the whole dump. The static
  // index stays crawler-only. See SPEC EX-ALL tombstone.)

  // the door's two quiet controls live in the live face only — created here, never baked into the
  // crawler-visible HTML (EX-DOOR lives only in the live face; INV-25(a) untouched)
  let skipBtn = null, exitBtn = null;
  if (moreWrap) {
    skipBtn = document.createElement("button");
    skipBtn.type = "button"; skipBtn.id = "ex-skip"; skipBtn.className = "ex-skip";
    skipBtn.textContent = "just enter →";
    skipBtn.hidden = true;
    skipBtn.addEventListener("click", doorSkip);
    exitBtn = document.createElement("button");
    exitBtn.type = "button"; exitBtn.id = "ex-exit"; exitBtn.className = "ex-exit";
    exitBtn.textContent = "⟲ the door";
    exitBtn.hidden = true;
    exitBtn.addEventListener("click", doorExit);
    if (!doorAvailable) exitBtn.style.display = "none"; // no pool → no threshold to return to
    moreWrap.appendChild(skipBtn);
    moreWrap.appendChild(exitBtn);
  }

  // ---- boot -----------------------------------------------------------------
  // a return visit continues its walk (the door never re-asks on its own, INV-26/EX-DOOR);
  // a first visit meets the door; a missing/thin pool degrades to silent entry (default hang)
  entered = restore();
  atDoor = !entered && doorAvailable;
  if (pick) ground(pick);
  document.body.classList.add("ex-live");              // hide the static index, reveal the live face
  render();                                            // cold render does NOT lock — instantly tappable
})();
