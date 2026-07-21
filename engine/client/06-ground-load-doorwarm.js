  // ---- EX-LADDER (INV-63): one home for the tier ladder -----------------------
  // The law is owed by EVERY work a visitor is shown, on every surface, so the ladder is
  // written once here and each surface hands only its own box description (`sizes`). The
  // tiers themselves are the work's baked `srcset` (640/960/1280, written by the display-cap
  // bake); no cap ⇒ no srcset key ⇒ the surface stays byte-identical to a ladder-less one.
  const LADDER_FALLBACK = { walk: "88vw", lane: "64vw", print: "(max-width:640px) 110px, 150px" };
  function ladderSizes(surface) {                      // the baked string, else the CSS box it mirrors
    return (data[surface + "_sizes"] || LADDER_FALLBACK[surface] || "100vw");
  }
  function ladderAttr(w, sizes) {                      // for a surface that writes its img as HTML
    return (w && w.srcset) ? ` srcset="${w.srcset}" sizes="${sizes}"` : "";
  }
  function ladderOn(img, w, sizes) {                   // for a surface that builds an Image object
    if (img && w && w.srcset) { img.sizes = sizes; img.srcset = w.srcset; }
    return img;
  }

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
    // --tone: the wall label's DIMMED accent — the same live tone at low brightness, lightly
    // tinting the plaque's letters work→work (EX-STORY-LINE, his call ×0.66)
    document.documentElement.style.setProperty(
      "--tone", `rgb(${a.map((v) => Math.round(v * 0.66)).join(",")})`);
  }
  const groundRest = () => {
    document.body.style.setProperty("--ground", "12,11,10");
    document.documentElement.style.removeProperty("--accent");    // back to resting bone
    document.documentElement.style.removeProperty("--accent-2");
    document.documentElement.style.removeProperty("--tone");       // the plaque rests plain, no tint
  };

  // ---- EX-LOAD-2 / EX-LOAD-3 (INV-72 / INV-73): the in-flight ladder + the one-ahead preload ----
  // Supersedes the lone-hairline FACE of the loading breath (EX-LOAD/INV-37): a frame in view whose
  // pixels are late wears the work's OWN dominant tone (a plate), and on a genuinely long wait a
  // thin wordless bar joins on the plate; the photograph fades in OVER the plate when it lands. The
  // breath's promises are re-carried whole — no frame in view stays empty, wholly wordless (INV-1),
  // retires on load-or-error, ONE reused overlay for the single in-view frame, the door/crossing
  // cover their own frames. Every wait a beat ×tempo (INV-33). The `#ex-breath` node below stays
  // for EX-ARRIVE's locked breath-entry row; the plate ladder is the shipped loader now.
  const breath = document.createElement("div");         // vestigial — kept for the EX-ARRIVE lock
  breath.id = "ex-breath";
  breath.hidden = true;
  document.body.appendChild(breath);

  // the knobs (config.exhibition, INV-28) — each a beat ×tempo (INV-33); the ordering
  // load_plate_grace < load_bar_wait is LAW (prover F7): an inverted/equal pair is CLAMPED at boot
  // (the bar wait raised past the grace) so no tuning can ask for a bar before its plate.
  const secs = (x, d) => { const n = parseFloat(x); return Number.isFinite(n) && n >= 0 ? n : d; };
  const PLATE_GRACE = secs(EX.load_plate_grace, 0.35);  // black → plate; the fast/slow reveal split
  let   BAR_WAIT    = secs(EX.load_bar_wait, 1.5);       // plate → plate+bar (a genuinely long wait)
  if (!(PLATE_GRACE < BAR_WAIT)) BAR_WAIT = PLATE_GRACE + 0.6;   // F7 clamp: a bar never before its plate
  const REVEAL_SLOW = secs(EX.load_reveal, 2.0);         // the reveal token — the graceful settle (plate stood)
  const REVEAL_FAST = secs(EX.load_reveal_fast, 0.6);    // the soft token — the crisp settle (beat the plate)
  const PRELOAD_AHEAD = clampInt(EX.preload_ahead, 1, 0, 1);     // EX-LOAD-3: one ahead, the bounded reach

  // ONE reused overlay: the plate (the work's raw tone) carrying its crawling bar, moved into the
  // in-view frame while its pixels are late (only the in-view frame ever ladders, so one suffices).
  const plate = document.createElement("div");
  plate.id = "ex-plate"; plate.hidden = true;
  plate.innerHTML = '<i class="ex-bar" aria-hidden="true"></i>';
  // hide ANY plate (the walk's single reused one, or a door window's own) — shared by both call sites
  function plateHideEl(el) {
    el.hidden = true; el.classList.remove("show", "bar");
    if (el.parentNode) el.parentNode.removeChild(el);
  }
  function plateHide() { plateHideEl(plate); }
  let armTimers = [];
  let armedImg = null;                                  // the one in-flight image the ladder waits on
  function armClear() { armTimers.forEach(clearTimeout); armTimers.length = 0; }
  // retire the whole ladder + preload — the door/ceremony cover every walk frame (EX-LOAD boundary)
  function ladderOff() { armClear(); armedImg = null; plateHide(); preloadCancel(); }
  // the reveal: the photo fades in over the plate at the chosen settle (fast when it beat the plate,
  // the reveal token when the plate stood). Rides the one clock (×TEMPO — reduced motion collapses it).
  function reveal(img, durSec) {
    img.style.transition = "none";
    img.style.opacity = "0";
    void img.offsetWidth;
    img.style.transition = "opacity " + (durSec * TEMPO).toFixed(3) + "s var(--ease)";
    img.style.opacity = "";                             // .seen → opacity 1, fades over durSec
    img.dataset.ladder = "done";
  }
  // the in-flight CORE, shared by the walk's one reused plate AND the door's per-window plates —
  // ONE implementation of the grace/bar/reveal timings + classes (never a second copy of the knobs).
  // The caller has already read the settled state; this arms a GENUINELY in-flight image only. Black
  // held → plate (grace) → plate+bar (long wait) → reveal on load. `alive()` says whether this wait is
  // still the live one (the walk swaps the in-view frame; a door window is rebuilt on relayout/re-deal);
  // `timers` is the caller's own list (mutated in place); `mark` gates the walk's single-frame ex: marks
  // (the door stays off the walk's counter — no door marks). On load: fade over the plate at the settle
  // (fast when it beat the plate, the reveal token when the plate stood), then retire the plate.
  function ladderFlight(img, w, host, plateEl, timers, alive, mark) {
    host.insertBefore(plateEl, host.firstChild);        // behind the photo, same cell
    plateEl.style.aspectRatio = (w.w && w.h) ? (w.w + " / " + w.h) : "";
    plateEl.style.background = "rgb(" + w.dom.join(",") + ")";   // the work's RAW baked tone (not liveAccent)
    plateEl.hidden = false;
    void plateEl.offsetWidth;                           // a fresh fade from opacity 0
    img.style.transition = "none";
    img.style.opacity = "0";                            // hold the photo behind the plate until it lands
    let plateShown = false;
    timers.push(setTimeout(() => {                      // the grace beat → the plate fades in (soft token)
      if (!alive() || img.complete) return;
      plateShown = true;
      plateEl.classList.add("show");
      if (mark) tlog("plate");
    }, Math.round(PLATE_GRACE * 1000 * TEMPO)));
    timers.push(setTimeout(() => {                      // the long wait → the wordless bar joins the plate
      if (!alive() || img.complete) return;             // (past here a silent stall crawls indefinitely —
      plateEl.classList.add("show", "bar");             //  the ladder owns no timeout, the browser's fetch does)
      if (mark) tlog("bar");
    }, Math.round(BAR_WAIT * 1000 * TEMPO)));
    const done = () => {                                // load OR error, whichever speaks first
      if (!alive()) return;
      timers.forEach(clearTimeout); timers.length = 0;
      if (img.naturalWidth > 0) {                       // pixels home: fade over the plate then retire it
        const dur = plateShown ? REVEAL_SLOW : REVEAL_FAST;
        reveal(img, dur);
        timers.push(setTimeout(() => { if (alive()) plateHideEl(plateEl); },
                               Math.round(dur * 1000 * TEMPO) + 60));
      } else {                                          // a dead image never traps (INV-37): retire whole,
        img.dataset.ladder = "done"; plateHideEl(plateEl);  //   caption + counter hold, no plate as the picture
      }
    };
    img.addEventListener("load", done, { once: true });
    img.addEventListener("error", done, { once: true });
  }

  // arm the ladder on a frame taking view. The arm READS THE SETTLED STATE FIRST (prover F1):
  // a warm image (complete, real pixels) reveals at once down the fast path — no plate, no clock;
  // an already-errored one retires at once, caption + counter holding; only a genuinely in-flight
  // image arms the grace/bar clocks and the load/error listeners — never a wait on a spent event.
  // Arms ONCE per frame-taking-view (prover F6): a post-reveal tier swap (INV-63) never re-plates.
  function arm(img, w, frame) {
    if (!img || !w || !frame) return;
    if (img.dataset.ladder === "done") return;          // already resolved — never re-plate (F6)
    if (img === armedImg && !plate.hidden) return;      // already laddering THIS frame — don't restart
                                                        //   the clocks (resize/re-observe)
    if (img.complete) {                                 // the settled read (F1), synchronous
      plateHide();                                      // clear a plate lingering from a prior frame
      if (img.naturalWidth > 0) reveal(img, REVEAL_FAST);   // warm ⇒ reveal at once, no plate/clock
      else img.dataset.ladder = "done";                     // pre-errored ⇒ retire; the caption holds
      return;
    }
    // genuinely in flight: black held → plate (grace) → plate+bar (long wait) → reveal on load
    armClear();
    armedImg = img;
    plateHide();
    ladderFlight(img, w, frame, plate, armTimers, () => img === armedImg, true);
  }

  // EX-LOAD-3: the next work quietly preloads — the walk arrives warm. While a work rests in view,
  // fetch the NEXT work in the current DIRECTION OF TRAVEL at the device tier (the same srcset/sizes
  // the walk uses, INV-63) — exactly preload_ahead (1) ahead, never the arc (INV-25/30). Best-effort
  // and silent (a dead preload costs nothing); cancelled on a turn or a #w- jump (prover F5), then
  // re-aimed to the new direction of travel.
  let travelDir = 1;                                    // +1 forward · -1 back — set by every step
  let preImg = null, preId = null;
  function preloadCancel() {
    if (preImg) { preImg.src = ""; preImg = null; }     // abandon the in-flight fetch cleanly (F5)
    preId = null;
    try { window.__@@NS@@Preload = null; } catch (e) {}     // the test read-side, like @@NS_UPPER@@Timings/__@@NS@@Seen
  }
  function preloadAhead(curN) {                         // curN = the 1-based frame in view
    if (!PRELOAD_AHEAD) { preloadCancel(); return; }
    if (dataSaver()) { preloadCancel(); return; }       // the Save-Data class law binds the one-ahead (EX-LOAD-3)
    const idx = (curN - 1) + travelDir;                 // one ahead along the feet
    if (idx < 0 || idx >= order.length) { preloadCancel(); return; }
    const id = String(order[idx]);
    if (id === preId) return;                           // already warming this exact next work
    preloadCancel();                                    // a turn/jump abandons the old one cleanly (F5)
    const w = byId[id]; if (!w) return;
    preId = id;
    const im = new Image();
    ladderOn(im, w, ladderSizes("walk"));
    im.src = w.img;                                     // the browser picks the device tier
    preImg = im;
    try { window.__@@NS@@Preload = { id: id, dir: travelDir }; } catch (e) {}
  }

  // ---- EX-DOOR-WARM (INV-25): the door warms its candidates — a pick opens warm ----
  // After the threshold's five windows decode AND the door rests, quietly warm ONE room-tier picture
  // per candidate (≤5) at LOW priority — the EXACT URL the room's first hang will request (the walk's
  // own full-frame `srcset`/`sizes`, INV-63), so the room's <img> finds the file already in cache.
  // Never before the door's own windows (fired only after they decode), never under Save-Data (the
  // class law's one home, dataSaver). Also the crossing's own pick-time warm (EX-DOOR-2e): the same
  // one picture for the picked work, so a fast picker who beats the rest still opens warm.
  const DOOR_WARM_SETTLE = 1000;                        // ms the threshold rests before warming (a network settle, unscaled)
  let warmGen = 0;                                      // a re-deal / relayout rebuild / pick cancels a pending warm
  let warmSettleT = null;
  const warmed = new Set();
  function warmRoomPicture(w) {
    if (!w || dataSaver()) return;                      // the Save-Data class law, consulted here too (EX-LOAD-3)
    if (warmed.has(w.id)) return;                       // one picture per candidate, once
    warmed.add(w.id);
    const im = new Image();
    try { im.fetchPriority = "low"; } catch (e) {}      // never contends with the door's five windows
    ladderOn(im, w, ladderSizes("walk"));               // the room's own tier
    im.src = w.img;                                     // the browser resolves the exact room-hang URL (INV-63)
  }
  function warmCandidates(gen) {
    if (gen !== warmGen || !atDoor || entered || busy || dataSaver()) return;
    const spread = (doorFace && doorFace.spread) ? doorFace.spread.slice(0, curLay.n) : [];
    spread.forEach((e) => warmRoomPicture(byId[e.id]));
  }
  // Track the threshold's decode: which layer each window belongs to is read ONCE at build — the
  // STATIC layer is the windows whose pixels are already present (a cache hit, no fetch, the seam the
  // door's own ladder reads via img.complete, EX-DOOR-2c); the DYNAMIC layer is the windows that must
  // fetch. Their decode promises close the load ladder's last two rungs, lay door_ready (arm 1), and
  // — after the rest — fire the candidate warm.
  function doorWatch(facade) {
    const imgs = [...facade.querySelectorAll(".exd-window img")];
    if (!imgs.length) return;
    const gen = ++warmGen;                              // this watch supersedes any pending warm
    clearTimeout(warmSettleT); warmSettleT = null;
    const decodeP = (img) => {
      if (img.complete && img.naturalWidth > 0) return Promise.resolve();
      if (img.decode) return img.decode().catch(() => {});
      return new Promise((res) => {
        img.addEventListener("load", res, { once: true });
        img.addEventListener("error", res, { once: true });
      });
    };
    const staticImgs = imgs.filter((i) => i.complete && i.naturalWidth > 0);
    Promise.all(staticImgs.map(decodeP)).then(() => { if (gen === warmGen) markStage("static"); });
    Promise.all(imgs.map(decodeP)).then(() => {
      if (gen !== warmGen) return;                      // a rebuild superseded this watch
      markStage("static");                              // dynamic implies the static rung was passed (monotonic)
      markStage("dynamic");
      layDoorReady();                                   // arm 1: the door's five windows decoded
      warmSettleT = setTimeout(() => warmCandidates(gen), DOOR_WARM_SETTLE);
    });
  }

