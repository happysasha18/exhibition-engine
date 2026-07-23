  // ---- EX-ZOOM: pinch to inspect a picture (his word 2026-07-12: «люди хотят зумить картинки») ----
  // A two-finger pinch on ANY exhibition picture — a work on the walk, a door window, a polaroid —
  // opens that picture in its own zoom layer: the image scales under the pinch, a × returns, and the
  // page beneath stays EXACTLY as it was (a face, EX-CHROME — the walk is frozen, never scrolled).
  // The browser's own pinch stays refused document-wide (EX-PROTECT / INV-49), so the walk never
  // desyncs; the zoom is OUR controlled scale in its own overlay. Touch only — a desktop trackpad
  // pinch is a Ctrl-wheel, already refused (EX-PROTECT), and never opens the layer.
  const zoom = document.createElement("div");
  zoom.id = "ex-zoom";
  zoom.setAttribute("role", "dialog");
  zoom.setAttribute("aria-modal", "true");
  zoom.setAttribute("aria-label", ((greetLang() || { t: {} }).t.a11y_zoom) || A11Y_ZOOM_EN);   // N7-A11Y (C4/C5)
  zoom.hidden = true;
  // The zoom holds the minimum on screen (INV-77): only the picture and a single CLOSE in the free
  // TOP-LEFT corner. The ambient player retracts while the zoom stands (body.ex-zoom, like every covering
  // face), and the zoom carries no share of its own — a visitor shares a work from the walk itself.
  // The close aria-label localizes through EX-I18N like every other chrome string; the fallback is
  // ENGLISH (source tongue), never a hardcoded locale literal.
  const ZT = (greetLang() || { t: {} }).t;
  zoom.innerHTML = '<button type="button" class="exz-btn exz-close" aria-label="'
                 + (ZT.a11y_close || A11Y_CLOSE_EN) + '">&times;</button>'
                 + '<div class="exz-stage"><img class="exz-img" alt=""></div>';
  document.body.appendChild(zoom);
  let zoomOpen = false, zScale = 1, zPinch = 0, zStartS = 1;
  // The way OUT mirrors the way IN (INV-82): the picture flies UP from its place into the layer on open
  // and back DOWN to that place on close. The FLIP rides a WRAPPER (.exz-stage) so the pinch keeps the
  // .exz-img's own transform (INV-81 — the live two-touch distance stays the sole scale authority); the
  // stage carries the entry/exit position+scale, the img carries the pinch. zSrcEl is the tapped picture,
  // re-measured on close so a rotation under the zoom lands the shrink on its fresh place (INV-82).
  let zSrcEl = null, zLastEl = null, zDismiss = 0;      // zLastEl survives close so a Forward step reopens (INV-83)
  // INV-93 (2026-07-16, one margin for every pinch): the in-pinch mirrors the out-pinch — DISMISS_T
  // sits just under the picture's own resting size, so a release just below resting closes the layer
  // whatever gesture it belongs to, and a release at/above resting leaves the picture open at its size.
  const DISMISS_T = 0.92;                                 // (his 2026-07-23) 0.98 closed on a 2% squeeze — a pinch-OUT that began with a hair of inward drift tripped the dismiss; his word: firmer, an 8% squeeze, so the zoom holds and only a deliberate pinch-in closes it
  // once zoomed past 1×, a one-finger drag PANS the enlarged picture. zTx/zTy are the pan offset in
  // screen px; zPan* hold the gesture's start. The offset is bounded to the picture's visible overflow
  // so the image can never be dragged past its own edge.
  let zTx = 0, zTy = 0, zPanning = false, zPanX = 0, zPanY = 0, zPanTx = 0, zPanTy = 0;
  // INV-85 desktop pinch (ctrl+wheel / Safari gesture*): accumulate into the SAME 1×–4× scale the touch
  // pinch drives. zDesk holds the below-1× dismiss accumulator (starts at 1, a continued pinch-IN eases
  // it down; at/below DISMISS_T it commits). zDismissing latches from the moment history.back() is asked
  // until closeZoom runs, so a rapid open→dismiss race can never pop the walk's own history step twice.
  let zDesk = 1, zDismissing = false, zWheelIdle = 0;
  let zBelow = false;          // the desktop gesture stands below 1× (the crossing re-based already)
  const zImg = zoom.querySelector(".exz-img");
  const zStage = zoom.querySelector(".exz-stage");
  // The dismiss preview composes on the LIVE stage transform, latched on the preview's first frame —
  // so a preview arriving over a flight still in motion shrinks from what the eye sees, and the close
  // can read the same live matrix (INV-87 rule 4 extended: no one-frame return to full). One preview
  // for every pointer kind (INV-82/85: touch resistance = desktop resistance).
  let zPrevBase = null;
  function zPreview(ratio) {
    if (zPrevBase === null) {
      const live = getComputedStyle(zStage).transform;
      zPrevBase = (live && live !== "none") ? live + " " : "";
    }
    const shrink = 1 - (1 - Math.max(0.5, ratio)) * 0.45;   // resistance — eases toward its place
    zStage.style.transition = "none";
    zStage.style.transform = zPrevBase + "scale(" + shrink.toFixed(3) + ")";
  }
  function zPreviewEnd(ease) {                   // leave the preview: the stage returns to its rest
    if (zPrevBase === null) return;
    zPrevBase = null;
    zStage.style.transition = ease ? "" : "none";
    zStage.style.transform = "";
  }
  const zReduce = matchMedia("(prefers-reduced-motion: reduce)");
  const zDist = (t) => Math.hypot(t[0].clientX - t[1].clientX, t[0].clientY - t[1].clientY);
  // ---- EX-PICSTAT (INV-41): a SETTLED zoom lays one `inspect` per episode ------------------------
  // The closer look enters the registry as its own beat by the door-leak precedent [EX-TIME-READ]: a
  // release that leaves the picture open at/above its resting size (INV-93) lays one `inspect`,
  // debounced to the pinch coming to REST; a flick that dismisses below rest, or never opens, lays
  // nothing (the old frame-spam silence narrows to the un-settled flick, INV-1). ONE per zoom episode
  // — re-entering the zoom later is a new episode (the flag resets in openZoom), repeated releases
  // within one open zoom lay once. It carries the work (`pic`) and its `context` from the closed
  // ladder door·walk·room, read off the source surface the zoom opened from (the seam the zoom knows).
  let inspectTimer = 0, inspectLaid = false;
  function inspectContext(el) {
    if (!el || !el.closest) return null;
    const win = el.closest(".exd-window");
    if (win) return { context: "door", pic: win.dataset.id };     // a window on the front door
    const print = el.closest(".exs-print");
    if (print) return { context: "room", pic: print.dataset.id }; // a polaroid in the side room
    const side = el.closest("#ex-side");
    if (side) return { context: "room", pic: el.dataset.id };     // a lane image in the side room
    const frame = el.closest(".exh-frame");
    if (frame) return { context: "walk", pic: frame.dataset.id };  // a hung work on the walk
    return null;
  }
  function clearInspect() { if (inspectTimer) { clearTimeout(inspectTimer); inspectTimer = 0; } }
  function armInspect() {                                          // (re-)arm the settle debounce
    clearInspect();
    if (!zoomOpen || zDismissing || inspectLaid) return;
    inspectTimer = setTimeout(() => {
      inspectTimer = 0;
      if (!zoomOpen || zDismissing || inspectLaid) return;
      if (zScale < DISMISS_T) return;                             // must rest at/above resting size (INV-93)
      const meta = inspectContext(zSrcEl);
      if (!meta || !meta.context || !meta.pic) return;
      inspectLaid = true;                                         // once per episode
      pulse("inspect", meta.pic, { context: meta.context });      // pic + context; the arm rides via pulse (INV-91)
    }, 320);
  }
  // ---- EX-ZOOM the inspect flight (INV-82 rework, design 2026-07-15) — one motion class over the
  // five trigger types: entry IS the exit's mirror by construction. The stage owns the flight (always
  // animated, both ways on the SAME clock); the img owns only the pinch surplus; the crop is a clip
  // morph; the pin is measured transform-free. Every duration is read from CSS — no literal lives in
  // this JS (EX-MOTION owns the clock).
  function zDur(el) {                                    // ms of a computed transition-duration (first value)
    const d = (getComputedStyle(el).transitionDuration || "0s").split(",")[0].trim();
    return d.slice(-2) === "ms" ? parseFloat(d) : parseFloat(d) * 1000;
  }
  const zFlightDur = () => zDur(zStage);                 // the stage flight's own clock (--d-cross)
  const zFadeDur = () => zDur(zoom);                     // the backdrop crossfade clock (reduced / source-gone)
  let zTeardown = null;                                  // a pending exit teardown — a reopen cancels it (rule 7)
  function zCancelTeardown() {
    if (!zTeardown) return;
    clearTimeout(zTeardown.timer);
    if (zTeardown.onEnd) zStage.removeEventListener("transitionend", zTeardown.onEnd);
    zTeardown = null;
  }
  // the exit teardown fires on the flight's OWN transitionend (the true end of the motion) with a
  // computed-duration fallback, so an occluded/headless compositor that never paints the transition
  // still tears down — whichever lands first runs once (rule 7).
  function zArmTeardown(done) {
    zCancelTeardown();
    if (!done) return;
    const fire = () => { if (!zTeardown) return; zCancelTeardown(); done(); };
    const onEnd = (ev) => { if (ev.target === zStage && ev.propertyName === "transform") fire(); };
    zStage.addEventListener("transitionend", onEnd);
    zTeardown = { onEnd: onEnd, timer: setTimeout(fire, Math.round(zFlightDur() * 1.5) + 1) };
  }
  function zArmFade(done) {                              // reduced-motion / source-gone teardown, on the fade clock
    zCancelTeardown();
    if (!done) return;
    zTeardown = { onEnd: null, timer: setTimeout(() => { zCancelTeardown(); done(); }, Math.round(zFadeDur()) + 1) };
  }
  // the layer img's REST box, TRANSFORM-FREE (offset* ignore transforms) so a live pinch already on
  // .exz-img can never poison the pin (rule 3). The stage centres the img in the viewport. Not yet laid
  // out (a cold slot): derive from the natural fit into the CSS max-box (94vw/88vh) — the flight NEVER
  // degrades to an instant swap (rule 6).
  function zRestBox() {
    let w = zImg.offsetWidth, h = zImg.offsetHeight;
    if (!w || !h) {
      const nw = zImg.naturalWidth || 1, nh = zImg.naturalHeight || 1;
      const s = Math.min(innerWidth * 0.94 / nw, innerHeight * 0.88 / nh);
      w = nw * s; h = nh * s;
    }
    return { w: w, h: h, cx: innerWidth / 2, cy: innerHeight / 2 };
  }
  // frame-0 of the flight for a source picture: its cover-crop mapped onto the layer (rule 2). A square
  // window / polaroid shows a CENTRE cover-crop while the layer shows the whole contain image, so the
  // layer starts CLIPPED to that crop and the clip morphs open; a contain source (a hung work, a lane
  // image) crops nothing (visW=visH=1). One uniform scale + a centred translate carries the position,
  // so no aspect ever jumps between the source and the layer.
  function zCropFrame(rect, box, rot) {
    const dx = (rect.left + rect.width / 2) - box.cx;
    const dy = (rect.top + rect.height / 2) - box.cy;
    let visW = 1, visH = 1;
    const fit = zSrcEl ? getComputedStyle(zSrcEl).objectFit : "";
    if (fit === "cover" && rect.height > 0 && box.h > 0) {
      const boxA = rect.width / rect.height, imgA = box.w / box.h;
      if (boxA > imgA) visH = imgA / boxA; else visW = boxA / imgA;   // cover crops the longer relative side
    }
    const s = (rect.width / visW) / box.w;                            // the full image at the source's per-pixel scale
    const ix = ((1 - visW) / 2 * 100).toFixed(2), iy = ((1 - visH) / 2 * 100).toFixed(2);
    const r = rot ? " rotate(" + (rot * 180 / Math.PI).toFixed(2) + "deg)" : "";
    return { transform: "translate(" + dx.toFixed(1) + "px," + dy.toFixed(1) + "px)" + r + " scale(" + s.toFixed(4) + ")",
             clip: "inset(" + iy + "% " + ix + "% " + iy + "% " + ix + "%)",
             rot: rot || 0 };
  }
  // A resting polaroid TILTS (.exs-print rotate(--rot)), and getBoundingClientRect alone returns the
  // rotated print's inflated axis-aligned box — a translate+scale pin would un-tilt it in a snap at
  // frame-0 and land ~10% large. The pin carries the source's own rotation and its TRUE visual rect
  // (offset size × the print's own scale, centred on the box centre), so the tilt rides the flight
  // (INV-87): upright as it arrives, back into the tilt on the way home.
  function zSrcFrame(rect) {
    const pr = zSrcEl && zSrcEl.closest && zSrcEl.closest(".exs-print");
    const tr = pr ? getComputedStyle(pr).transform : "";
    const m = tr && tr !== "none" ? /matrix\(([^)]+)\)/.exec(tr) : null;
    if (!m) return { rect: rect, rot: 0 };
    const v = m[1].split(",").map(parseFloat);
    const rot = Math.atan2(v[1], v[0]);
    if (!rot) return { rect: rect, rot: 0 };
    const sc = Math.hypot(v[0], v[1]);                     // the print's own scale rides the same matrix
    const w = zSrcEl.offsetWidth * sc, h = zSrcEl.offsetHeight * sc;
    const cx = rect.left + rect.width / 2, cy = rect.top + rect.height / 2;
    return { rect: { left: cx - w / 2, top: cy - h / 2, width: w, height: h }, rot: rot };
  }
  // The single flight carrier. `back=false` opens (frame-0 crop → full contain), `back=true` closes
  // (full → the source's crop) — the SAME stage transform + img clip both directions on the SAME clock
  // (rule 8). Reduced motion / a vanished source: a short opacity crossfade in place, no flight
  // (rules 9 + 10). The pinch's own transform on .exz-img is never written here (INV-81).
  function zFlip(rect, back, done) {
    const box = zRestBox();
    if (!rect || zReduce.matches || !box.w || !box.h) {
      zStage.style.transition = "none";
      if (!back) { zStage.style.transform = ""; zImg.style.transition = "none"; zImg.style.clipPath = "inset(0)"; }
      if (done) { if (back) zArmFade(done); else requestAnimationFrame(done); }
      return;
    }
    const sf = zSrcFrame(rect);                     // the source's true visual rect + its own tilt (INV-87)
    const c = zCropFrame(sf.rect, box, sf.rot);
    if (back) {                                     // full → source crop: animate out, tear down on transitionend
      zStage.style.transition = ""; zImg.style.transition = "";
      requestAnimationFrame(() => { zStage.style.transform = c.transform; zImg.style.clipPath = c.clip; });
      zArmTeardown(done);
    } else {                                        // pin at the source crop, then release to fly in + morph open
      zStage.style.transition = "none"; zImg.style.transition = "none";
      zStage.style.transform = c.transform; zImg.style.clipPath = c.clip;
      void zStage.offsetWidth;                      // commit the pin before the release — a bare rAF pair
                                                    // can coalesce on WebKit and skip the entry flight
      requestAnimationFrame(() => {
        zStage.style.transition = ""; zImg.style.transition = "";
        // a rotated pin releases to the SAME function list (translate rotate scale) so the tilt
        // interpolates cleanly to upright; an unrotated pin keeps the plain rest form
        zStage.style.transform = c.rot ? "translate(0px,0px) rotate(0deg) scale(1)" : "";
        zImg.style.clipPath = "inset(0)";
        if (done) done();
      });
    }
  }
  function zClampPan() {                                 // keep the offset within the picture's overflow
    const ox = Math.max(0, (zImg.offsetWidth * zScale - innerWidth) / 2);
    const oy = Math.max(0, (zImg.offsetHeight * zScale - innerHeight) / 2);
    zTx = Math.max(-ox, Math.min(ox, zTx));
    zTy = Math.max(-oy, Math.min(oy, zTy));
  }
  function zApply() {
    zImg.style.transform = "translate(" + zTx.toFixed(1) + "px," + zTy.toFixed(1) + "px) scale(" + zScale.toFixed(3) + ")";
  }
  function openZoom(el, opts) {
    if (zoomOpen || !el) return;
    const src = el.currentSrc || el.getAttribute("src") || el.src;
    if (!src) return;
    inspectLaid = false; clearInspect();               // EX-PICSTAT: a fresh open is a new inspect episode
    zCancelTeardown();                                 // a reopen mid-teardown lands clean (rule 7)
    zSrcEl = el; zLastEl = el;                          // the tapped picture — the FLIP's place, re-measured on close
    const rect = el.getBoundingClientRect();           // its VISUAL rect (its own transform, e.g. a lifted print — rule 9)
    // N7-A11Y (INV-102, C7): the inspected image speaks the source picture's own description (the walk
    // frame / door window / polaroid all carry alt = the work's desc); the layer names itself by it too.
    zImg.src = src; zImg.alt = el.alt || "";
    zoom.setAttribute("aria-label", zImg.alt || (((greetLang() || { t: {} }).t.a11y_zoom) || A11Y_ZOOM_EN));
    zScale = 1; zTx = 0; zTy = 0; zPanning = false; zDismiss = 0; zDesk = 1; zBelow = false; zDismissing = false; zApply();
    zPrevBase = null;                                  // no preview rides into a fresh open
    if (zWheelIdle) { clearTimeout(zWheelIdle); zWheelIdle = 0; }
    zoom.classList.remove("desk");                     // a fresh open is finger-driven until a wheel/gesture says otherwise
    zStage.style.transition = "none"; zStage.style.transform = ""; zImg.style.clipPath = "inset(0)";
    zImg.style.willChange = "transform"; zStage.style.willChange = "transform";   // transient — cleared at teardown (never left on: compositor stall)
    zoom.hidden = false; zoomOpen = true;
    document.body.classList.add("ex-zoom");            // the player retracts too — the minimum on screen (INV-77)
    faceSync();                                        // the zoom is a face — freeze the page beneath (EX-CHROME)
    // N7-A11Y (INV-102, B1): the closer look takes keyboard focus; the origin rule is ORIGIN-CONDITIONED
    // — only a KEYBOARD open passes an opener (opts.opener, the focused work), so a pinch / ctrl-wheel /
    // trackpad open forces NO focus and the exact-restore invariant (INV-74/INV-83) is left untouched.
    openTrap(zoom, opts && opts.opener);
    if (!(opts && opts.lay === false)) pushFace({ face: "zoom" });   // one honest road out (INV-83), above any standing face
    requestAnimationFrame(() => {
      zoom.classList.add("show");                      // backdrop fades in
      const fly = () => { if (zoomOpen) { zImg.classList.remove("ex-skel"); zFlip(rect, false); } };  // picture flies in + the crop morphs open (INV-82)
      if (zImg.complete && zImg.naturalWidth) fly();                  // cached (the usual path) — fly at once
      else {                                                          // a cold slot: the shimmer holds the stage while it decodes (EX-SKEL/INV-48), never an instant swap (rule 6)
        zImg.classList.add("ex-skel");
        if (zImg.decode) zImg.decode().then(fly, fly);
        else fly();
      }
    });
  }
  // The single teardown, reached only through popstate (history.back): the ×, backdrop, Esc, and the
  // dismissing pinch all go through history.back so Back and they share one road (INV-83).
  function closeZoom() {
    if (!zoomOpen) return;
    clearInspect();                                    // EX-PICSTAT: a closing zoom lays no inspect
    zoomOpen = false; zDismissing = false; zDesk = 1; zBelow = false;
    const rect = (zSrcEl && document.body.contains(zSrcEl)) ? zSrcEl.getBoundingClientRect() : null;  // fresh VISUAL place (rotation/lift, INV-82 + rule 9)
    // Fold the current visual scale+pan into the flight's START, composed ONTO the live stage
    // transform — whatever the eye already sees (a dismiss preview's shrink, a flight still in
    // motion) — then reset the img: the exit is ONE composed motion home, never a snap to 1× and
    // never a one-frame return to full before the fly (rule 4). Both transforms originate at the
    // viewport centre (the img is flex-centred), so the composition is exact.
    const live = getComputedStyle(zStage).transform;
    // the img may still be EASING toward its model under the desk ease (.desk, --d-pinch) when a
    // fast pinch-shut commits — fold what the eye SEES (the computed matrix), never the model's
    // target, or the img snaps to 1× the instant .desk drops (read BEFORE the class is removed)
    const imLive = getComputedStyle(zImg).transform;
    const fold = (imLive && imLive !== "none")
      ? imLive
      : "translate(" + zTx.toFixed(1) + "px," + zTy.toFixed(1) + "px) scale(" + zScale.toFixed(4) + ")";
    zoom.classList.remove("desk");                     // the img resets instantly (no eased double-motion)
    zPrevBase = null;                                  // the preview is riding the fold now
    if (zWheelIdle) { clearTimeout(zWheelIdle); zWheelIdle = 0; }
    zStage.style.transition = "none";
    zStage.style.transform = (live && live !== "none" ? live + " " : "") + fold;
    zScale = 1; zTx = 0; zTy = 0; zPanning = false; zDismiss = 0; zApply();   // the img → identity, in place
    void zStage.offsetWidth;                           // commit the fold before the flight starts (no jump)
    zoom.classList.remove("show");                     // backdrop fades; the player returns to its rail at once
    document.body.classList.remove("ex-zoom");
    zFlip(rect, true, () => {                           // picture flies back DOWN to its place, then teardown
      zoom.hidden = true; zImg.removeAttribute("src");
      zStage.style.transition = "none"; zStage.style.transform = ""; zImg.style.clipPath = "";
      zImg.style.willChange = ""; zStage.style.willChange = "";     // release the transient compositor hint
      zSrcEl = null;
    });
    closeTrap(zoom);                                   // N7-A11Y (B1): release the trap; restore focus only if a keyboard open recorded an opener (after the composed-exit fold, so the flight's structure stands as INV-87 pins it)
    faceSync();                                        // the page beneath returns untouched (EX-COMPOSE)
  }
  // a pinch over the OPEN zoom scales the picture; our JS owns it, so the browser never viewport-zooms.
  // The handlers listen at the DOCUMENT, gated on zoomOpen (INV-81): touch events keep targeting the
  // element where the gesture STARTED — for the pinch that just opened the layer that is the picture
  // beneath, never #ex-zoom itself — and they bubble to the document, so one set of handlers serves
  // both the opening gesture (the direct scale, no arming tap) and any later gesture on the layer.
  addEventListener("touchstart", (e) => {
    if (!zoomOpen) return;
    if (e.touches.length === 2) {                       // two fingers → pinch-scale (pan yields)
      zPinch = zDist(e.touches); zStartS = zScale; zPanning = false;
      clearInspect();                                   // a resumed pinch is not at rest (EX-PICSTAT)
    } else if (e.touches.length === 1 && zScale > 1
               && e.target.closest && e.target.closest(".exz-img")) {
      zPanning = true;                                  // one finger on the enlarged picture → pan
      zPanX = e.touches[0].clientX; zPanY = e.touches[0].clientY;
      zPanTx = zTx; zPanTy = zTy;
    }
  }, { passive: true });
  addEventListener("touchmove", (e) => {
    if (!zoomOpen) return;
    if (e.touches.length === 2 && zPinch) {
      e.preventDefault();                              // our scale, never the browser's
      let raw = zStartS * (zDist(e.touches) / zPinch);
      if (raw < 1 && zScale <= 1.001) {   // at/into 1×, a continued pinch-IN previews the dismiss — one continuous gesture crosses from zoom-out into dismiss (rule 5)
        if (zStartS !== 1) {              // a pinch that began zoomed RE-BASES at the 1× crossing (INV-82):
          zPinch = zDist(e.touches);      // the dismiss ratio reads from HERE, so the squeeze is the same
          zStartS = 1;                    // whatever the prior zoom and a fast crossing frame never commits
          raw = 1;
        }
        zDismiss = raw;
        zPreview(raw);
      } else {
        // the recovery EASES back (never a snap): the latched base may be a mid-flight matrix —
        // an instant reset here was the one-frame jump the composed close exists to kill (INV-87)
        if (zDismiss) { zDismiss = 0; zPreviewEnd(true); }
        zScale = Math.max(1, Math.min(4, raw));
        zClampPan();                                   // a smaller scale shrinks the pannable overflow
        zApply();
      }
    } else if (e.touches.length === 1 && zPanning) {
      e.preventDefault();                              // drag the enlarged picture, bounded to its edges
      zTx = zPanTx + (e.touches[0].clientX - zPanX);
      zTy = zPanTy + (e.touches[0].clientY - zPanY);
      zClampPan();
      zApply();
    }
  }, { passive: false });
  addEventListener("touchend", (e) => {
    if (!zoomOpen) return;
    const pinchBroke = zPinch && e.touches.length < 2;   // the two-finger pinch just broke (first finger up)
    if (e.touches.length < 2) zPinch = 0;
    if (e.touches.length === 0) zPanning = false;
    if (zDismiss) {                                    // in the dismiss preview (INV-82)
      // The verdict LATCHES the moment the pinch breaks — a STAGGERED two-finger release still commits,
      // where the old code cancelled on the first touchend before the last finger lifted (rules 1 + 5).
      if (pinchBroke) {
        if (zDismiss < DISMISS_T && !zDismissing) { zDismissing = true; history.back(); return; }   // commit → close through history (INV-83)
        zDismiss = 0; zPreviewEnd(true);                                                   // above threshold → ease back to 1×
      }
      return;
    }
    if (zScale <= 1.03 && e.touches.length === 0) { zScale = 1; zTx = 0; zTy = 0; zApply(); }   // a near-1 release settles flat + centred
    // EX-PICSTAT: a release that leaves the picture open at/above resting arms the settle debounce
    if (zoomOpen && !zDismissing && e.touches.length === 0) armInspect();
  }, { passive: true });
  // A gesture the system TAKES AWAY (an incoming call, a notification pulled over the page, a palm the
  // browser rejects) fires touchcancel and never touchend, so pinch, pan and dismiss state would stand
  // mid-gesture under the open layer and the next touch would resume a gesture the visitor never made.
  // It ends the gesture like a lift that commits nothing: the dismiss preview eases back, pinch and pan
  // clear, the picture keeps the size the visitor reached, and the settle re-arms (INV-82).
  addEventListener("touchcancel", () => {
    if (!zoomOpen) return;
    zPinch = 0;
    zPanning = false;
    if (zDismiss) { zDismiss = 0; zPreviewEnd(true); }
    if (!zDismissing) armInspect();
  }, { passive: true });
  // Every way out is the same road (INV-83): the ×, a backdrop tap, and Esc all step history BACK, and
  // the popstate handler runs the one closeZoom — so the browser's own Back button closes the zoom too.
  const zoomBack = () => { if (zoomOpen) history.back(); };
  zoom.querySelector(".exz-close").addEventListener("click", zoomBack);
  zoom.addEventListener("click", (e) => { if (e.target === zoom) zoomBack(); });   // tap the backdrop
  addEventListener("keydown", (e) => { if (e.key === "Escape" && zoomOpen) zoomBack(); });

  // ---- N7-A11Y (INV-102, B2/B3): the keyboard opens the closer look and the grab from a FOCUSED work ----
  // A work HANGS in four places — a walk photograph (.exh-frame), a door window (.exd-window), a
  // polaroid on the table (.exs-print) and a lane picture in the series room (a direct <img> child of
  // #exs-stage; a polaroid's own inner <img> is NOT one, it belongs to its print). One selector set
  // names all four, and every road below — the keyboard, the right-click, the long press — resolves
  // through it, so no surface carries a private list of what counts as a picture.
  const HANG_SEL = ".exh-frame, .exd-window, .exs-print, #exs-stage > img";
  function hangPlace(el) {                              // the hanging place under an element, or null
    return (el && el.closest) ? el.closest(HANG_SEL) : null;
  }
  function hangPic(place) {                             // the picture a hanging place shows
    if (!place) return null;
    return place.tagName === "IMG" ? place : place.querySelector("img");
  }
  // The gift ceremony is offered against a work the visitor has CHOSEN and walked to. A door window
  // shows the facade's spread before that choice exists, so it carries no hung-work identity to
  // ceremony over and always answers with the gracious line instead (INV-49, F1) — the one exception,
  // stated here once rather than re-derived at each road.
  function hangGiftId(place) {
    if (!place || (place.classList && place.classList.contains("exd-window"))) return "";
    return (place.dataset && place.dataset.id) || "";
  }
  // With a hanging place holding focus, `z` looks closer (openZoom, recording the PLACE as the opener so
  // close restores focus to it — B1), and `y` hands over the gift through the SAME imageless clean-source
  // openGift path onGrab routes a right-click through, so no new grab road is built (INV-49) — not `g`,
  // which both NVDA and JAWS already consume as browse-mode next-graphic before the page ever sees it.
  // Enter keeps its walk-only meaning: on a polaroid it lifts (16's own handler) and on a door window it
  // enters.
  addEventListener("keydown", (e) => {
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    // A standing LAYER's own keys own the input. atDoor and sideOpen are deliberately NOT here: the
    // door and the series room are not layers over a work, they HANG works, and a face passes `z` and
    // `g` to the work its visitor has focused (INV-67, input ownership).
    if (zoomOpen || quizOpen || giftOpen || busy) return;
    const place = hangPlace(e.target);
    if (!place) return;                                // a key only opens from a focused hanging place
    const img = hangPic(place);
    if (!img) return;
    if (e.key === "z" || e.key === "Z") {              // look closer, wherever the work hangs
      e.preventDefault();
      openZoom(img, { opener: place });
    } else if (e.key === "y" || e.key === "Y") {       // take the gift — the keyboard grab (not `g`: the
                                                        // screen readers' own next-graphic key, never reaches the page)
      e.preventDefault();
      const gid = hangGiftId(place);
      if (gid) {
        openGift(img.currentSrc || img.getAttribute("src") || img.src, undefined, undefined, undefined,
                 gid, place);                           // OFFER, never dump — reuse the clean-source path; keyboard origin → restore to the place (INV-49, D4)
      } else {
        toast(enjoyLine());                             // a door window keeps the gracious line (F1)
      }
    } else if (e.key === "Enter" && place.classList.contains("exh-frame")) {
      e.preventDefault();                              // the walk's own Enter, unchanged
      openZoom(img, { opener: place });
    }
  }, { passive: false });
  // INV-81 — the trigger reaches every picture, the small ones included: a polaroid never fits two
  // fingertips, so the match reads the element under EACH touch point (the event's own target first —
  // one deterministic pick when two pictures sit under the two fingers), and the WHOLE print
  // (.exs-print, paper frame included) is the polaroid's hit area, resolving to the photograph inside.
  const ZOOM_SEL = ".exh-frame img.work, .exd-window img, #ex-side img, .exs-print";
  function zoomPick(e) {
    let hit = e.target && e.target.closest && e.target.closest(ZOOM_SEL);
    for (let i = 0; !hit && i < e.touches.length; i++) {
      const el = document.elementFromPoint(e.touches[i].clientX, e.touches[i].clientY);
      hit = el && el.closest && el.closest(ZOOM_SEL);
    }
    if (!hit) return null;
    return hit.tagName === "IMG" ? hit : hit.querySelector("img");
  }
  addEventListener("touchstart", (e) => {
    if (e.touches.length !== 2 || zoomOpen) return;   // one zoom at a time; opens over ANY face
    const t = zoomPick(e);
    if (!t) return;
    openZoom(t);                                       // pass the picture itself — its rect is the FLIP's place (INV-82)
    // seed the pinch so the SAME gesture keeps scaling the just-opened layer — its later touchmoves
    // bubble to the document handlers above; no second pinch, no arming tap (INV-81)
    if (zoomOpen) { zPinch = zDist(e.touches); zStartS = 1; zPanning = false; }
  }, { passive: true });

  // INV-85 target resolution (derived from EX-HANG): a trackpad pinch does not move the cursor, so the
  // picture UNDER the pointer wins (the same ZOOM_SEL selector set); with the pointer over no picture the
  // single work then in the viewport is the target (one work per viewport, EX-HANG); else nothing opens.
  function zoomTargetAt(x, y) {
    const el = document.elementFromPoint(x, y);
    let hit = el && el.closest && el.closest(ZOOM_SEL);
    if (hit) return hit.tagName === "IMG" ? hit : hit.querySelector("img");
    if (restingEl && restingEl.querySelector) {          // no picture under the pointer → the viewport's one work
      const img = restingEl.querySelector("img.work");
      if (img) return img;
    }
    return null;
  }
  // INV-85: a ctrl+wheel `deltaY` accumulates into the very 1×–4× scale the touch pinch drives —
  // deltaY<0 (pinch OUT) grows it, deltaY>0 (pinch IN) shrinks it; a rising scale OPENS #ex-zoom on the
  // resolved picture, a pinch-IN past the mirror margin (DISMISS_T) DISMISSES through the one history step.
  const ZOOM_WHEEL_STEP = 0.0025;                        // scale change per |deltaY| unit of a ctrl+wheel / pinch
  function pinchWheel(e) {
    const dScale = -e.deltaY * ZOOM_WHEEL_STEP;          // OUT (deltaY<0) → +, IN (deltaY>0) → −
    zoom.classList.add("desk");                          // the wheel surplus eases on the img (rule 8) — finger pinch stays instant
    if (!zoomOpen) {
      if (dScale <= 0) return;                           // a pinch-IN with nothing open opens nothing (INV-81 mirror)
      const t = zoomTargetAt(e.clientX, e.clientY);
      if (!t) return;                                    // no picture resolves → nothing opens (browser zoom stays refused)
      openZoom(t);                                       // lays the one history step (INV-83) — the dismiss road
      if (!zoomOpen) return;
      zDesk = 1; zScale = Math.min(4, 1 + dScale); zApply();
      armInspect();                                      // EX-PICSTAT: the wheel-pinch settles too
      return;
    }
    const ns = zScale + dScale;
    if (ns < 1) {                                        // at/into 1× a continued pinch-IN previews the dismiss (INV-82)
      zScale = 1; zTx = 0; zTy = 0; zApply();
      // the crossing EVENT re-bases at 1× — its below-1 residue never commits by itself, the same
      // law the touch path holds (INV-82); travel below 1× counts only from the crossing on
      zDesk = zBelow ? zDesk + (ns - 1) : 1;
      zBelow = true;
      if (zWheelIdle) { clearTimeout(zWheelIdle); zWheelIdle = 0; }
      if (zDesk <= DISMISS_T && !zDismissing) { zDismissing = true; zDesk = 1; history.back(); return; }  // commit through the one road (INV-83)
      zPreview(zDesk);                                   // the desktop pinch-shut previews with the touch resistance (INV-82/85)
      // Blink's ctrl-wheel stream carries no end event — a short idle eases an uncommitted preview back
      zWheelIdle = setTimeout(() => {
        zWheelIdle = 0;
        if (zoomOpen && !zDismissing) { zDesk = 1; zBelow = false; zPreviewEnd(true); }
      }, 140);
      return;
    }
    zDesk = 1; zBelow = false;
    zPreviewEnd(true);                                   // recovered above 1× — the preview eases off
    zScale = Math.min(4, ns); zClampPan(); zApply();
    armInspect();                                        // EX-PICSTAT: the wheel-pinch coming to rest
  }
  // INV-76 desktop pan: once enlarged past 1×, a mouse drag inside the layer pans the picture — the
  // direct equivalent of the one-finger touch pan, under the same edge-bounded clamp (zClampPan).
  zStage.addEventListener("mousedown", (e) => {
    if (!zoomOpen || zScale <= 1) return;
    e.preventDefault();
    zPanning = true; zPanX = e.clientX; zPanY = e.clientY; zPanTx = zTx; zPanTy = zTy;
  });
  addEventListener("mousemove", (e) => {
    if (!zoomOpen || !zPanning) return;
    zTx = zPanTx + (e.clientX - zPanX); zTy = zPanTy + (e.clientY - zPanY);
    zClampPan(); zApply();
  });
  addEventListener("mouseup", () => { if (zPanning) zPanning = false; });

  // EX-PROTECT (INV-49; 2026-07-13 uniformity fix): the grab guard now matches on the door window's
  // picture too (.exd-window img), not only a hung work — the door face was the one surface a guest
  // could still freely save, on FIRST entry, before the gift ceremony's identity even exists (his find:
  // the room refuses a grab, the door facade did not). A door window carries no HUNG WORK identity
  // (no .exh-frame, no frame id) to offer the desktop gift ceremony against, so its refusal never
  // invents one — it always answers with the SAME gracious toast the room gives a drag/touch grab,
  // never a new behaviour or new copy.
  let lpTouchFired = false;                               // A1: a just-fired touch long-press swallows a follow-up contextmenu (Android)
  // the PICTURE at each of the four hanging places — the grab's own hit set. It stays a picture-level
  // list (never the whole place) so a grab on a frame's breathing margin or on room chrome is still
  // left alone; the place it hangs in is resolved from the picture through hangPlace.
  const GRAB_SEL = ".exh-frame img.work, .exd-window img, .exs-print img, #exs-stage > img";
  function onGrab(ev) {                                    // ONE delegated listener per kind, O(1)
    const img = ev.target.closest && ev.target.closest(GRAB_SEL);
    if (!img) return;                                      // only a picture that hangs somewhere; chrome is left alone
    ev.preventDefault();                                   // the raw browser save menu / drag ghost never fires
    if (lpTouchFired) { lpTouchFired = false; return; }    // the touch long-press already answered this grab (A1) — a contextmenu that trails it is swallowed
    const gid = hangGiftId(hangPlace(img));                // "" for a door window (INV-49 uniformity)
    // EX-PULSE/INV-79: the guest REACHES to take a hung work — the earlier moment gift_download cannot
    // see (that lays only when a file leaves), a demand signal. The grab KIND is a closed ladder:
    // `drag` · `menu` (desktop right-click → the gift ceremony) · `touch` (a coarse-pointer press).
    const grab = ev.type === "dragstart" ? "drag"
      : matchMedia("(pointer: coarse)").matches ? "touch" : "menu";
    pulse("copy_attempt", gid || null, { grab: grab });
    // DESKTOP right-click on a work that carries an identity → the gift ceremony; a door window (no
    // `gid`), TOUCH, or a drag → just the gracious line, no download (his word 2026-07-08: on the phone
    // the picture is earned through the quiz, not grabbed; a door window has no hung-work identity to
    // ceremony over either)
    if (gid && ev.type === "contextmenu" && !matchMedia("(pointer: coarse)").matches) {
      openGift(img.currentSrc || img.getAttribute("src") || img.src, undefined, undefined, undefined,
               gid);                                    // OFFER, never dump — gift_kind=grab (EX-PULSE)
    } else {
      toast(enjoyLine());
    }
  }
  stage.addEventListener("contextmenu", onGrab);
  stage.addEventListener("dragstart", onGrab);
  door.addEventListener("contextmenu", onGrab);           // the door's own facade (INV-49 uniformity) —
  door.addEventListener("dragstart", onGrab);             //   #ex-door lives OUTSIDE #ex-stage (EX-DOOR-2a)
  // EX-PROTECT (INV-49): the enlarged view is a face that shows a picture — the largest one — so it
  // refuses a raw save like every other. #ex-zoom lives on document.body (outside #ex-stage), so it
  // binds its own guard: a desktop right-click / drag on the magnified copy meets the SAME gracious
  // line the hung work gives, never the browser's save menu. The iOS long-press sheet is handled by
  // the CSS `-webkit-touch-callout:none` on .exz-img (the touch road), and the long-press ceremony
  // detector already stands down while a zoom is open (pointerdown returns on zoomOpen).
  zoom.addEventListener("contextmenu", (ev) => { ev.preventDefault(); toast(enjoyLine()); });
  zoom.addEventListener("dragstart", (ev) => { ev.preventDefault(); });
  // the series room binds the SAME onGrab where it is built (16-renderhang-series.js) — #ex-side is
  // appended to document.body, outside both #ex-stage and #ex-door, so its works were reachable by no
  // grab road at all until it did.
  // ---- EX-PROTECT (A1, INV-49): a touch LONG-PRESS on a hung work opens the SAME gift ceremony --------
  // iOS fires no reliable `contextmenu`, so the finger's grab rides a real press-and-hold detector here,
  // beside onGrab and the pinch it must coexist with. It ARMS on `pointerdown`, FIRES after a hold of
  // ~500ms `[default]` with no drift past a small px threshold `[default]`, and reuses the imageless
  // clean-source openGift path onGrab routes a right-click through — never a new grab road, never a clean
  // copy in the card (INV-49). It CANCELS on a lift, on a drift past the threshold (so the walk swipe in
  // 15-motion wins), and on a second finger (so the inspect pinch wins). A door window (no hung-work
  // identity) keeps the gracious toast, never the ceremony (F1). The ~500ms / px values are Alexander's
  // device-feel tune, like the 1.7.5 swipe constants — a touch input threshold, never tempo-scaled.
  const LP_MS = 320;                                      // [default] the hold that arms the grab (his 2026-07-23: 500→400→320, a touch wanted the gift a further ~20% sooner)
  const LP_PX = 10;                                       // [default] the drift that cancels it (a swipe)
  let lpTimer = 0, lpX = 0, lpY = 0, lpImg = null, lpPtrs = 0;
  function lpCancel() { if (lpTimer) { clearTimeout(lpTimer); lpTimer = 0; } lpImg = null; }
  addEventListener("pointerdown", (e) => {
    if (e.pointerType === "mouse") return;                // the pointer's own grab road is the right-click (onGrab)
    lpPtrs++;
    if (lpPtrs > 1) { lpCancel(); return; }               // a second finger → the inspect pinch owns the touch
    // a covering LAYER stands — its own gestures own the input. sideOpen is deliberately absent: the
    // series room HANGS works (a polaroid, a lane picture) and a press must reach them (INV-67). The
    // GRAB_SEL match below is the gate instead — a press on the bare table or on the room's own chrome
    // resolves to no picture and still does nothing.
    if (zoomOpen || giftOpen || quizOpen) return;
    const img = e.target && e.target.closest && e.target.closest(GRAB_SEL);
    if (!img) return;                                     // only a picture that hangs somewhere
    lpImg = img; lpX = e.clientX; lpY = e.clientY;
    lpTimer = setTimeout(() => {
      lpTimer = 0;
      if (!lpImg || lpPtrs !== 1 || zoomOpen || giftOpen || quizOpen) return;
      const gid = hangGiftId(hangPlace(lpImg));           // "" for a door window (INV-49 uniformity)
      pulse("copy_attempt", gid || null, { grab: "touch" });   // the demand beat, the touch kind (EX-PULSE)
      lpTouchFired = true;                                // swallow any follow-up contextmenu (Android) in onGrab
      setTimeout(() => { lpTouchFired = false; }, 700);   // the trailing contextmenu, if any, lands right after; then clear the swallow window
      if (gid) {
        openGift(lpImg.currentSrc || lpImg.getAttribute("src") || lpImg.src, undefined, undefined,
                 undefined, gid);                         // OFFER — the imageless clean-source path; touch origin → no forced focus (INV-49, D4)
      } else {
        toast(enjoyLine());                               // a door window keeps the gracious line (F1)
      }
      lpImg = null;
    }, LP_MS);
  }, { passive: true });
  addEventListener("pointermove", (e) => {
    if (!lpTimer) return;
    if (Math.hypot(e.clientX - lpX, e.clientY - lpY) > LP_PX) lpCancel();   // a drift → a swipe, cancel the arm
  }, { passive: true });
  function lpUp(e) {
    if (e.pointerType === "mouse") return;
    if (lpPtrs > 0) lpPtrs--;
    lpCancel();                                           // a lift cancels a still-pending arm (a tap, never a grab)
  }
  addEventListener("pointerup", lpUp, { passive: true });
  addEventListener("pointercancel", lpUp, { passive: true });
  // EX-PROTECT + EX-CHROME: the immersive walk refuses browser zoom across the WHOLE surface, not
  // only over a work. A browser zoom scales the visual viewport out from under the JS scroll animator
  // and the fixed chrome — the measured centering drifts and the fixed controls float, so the walk
  // desyncs (his phone field-find). Pinch: Safari fires gesture events; Blink zooms via a two-finger
  // drag — both refused document-wide here. Double-tap zoom: blocked by `touch-action:manipulation`
  // (CSS) since iOS IGNORES the viewport's user-scalable=no. On Blink the viewport meta also pins
  // scale to 1. Silent — a pinch is exploratory, not a save, so no gift line, only no zoom.
  // INV-85: Safari fires gesturestart/gesturechange/gestureend for a trackpad pinch (Blink does not —
  // its equivalent is the ctrl+wheel above). We preventDefault ALWAYS so the browser never viewport-
  // zooms (EX-PROTECT), and on a NON-touch device drive the SAME inspect layer from `ev.scale`: the
  // gesture's live scale (× the scale at gesturestart) accumulates into the 1×–4× clamp, and a pinch-IN
  // past the dismiss threshold closes through the one history step. (Headless Blink dispatches no
  // gesture* events, so this path is verified only on a real Mac — named in the test's real-device set.)
  let gStart = 1;
  function onGestureStart(ev) {
    ev.preventDefault();
    if (TOUCHY) return;                                  // touch Safari uses the touch pinch path above
    gStart = zoomOpen ? zScale : 1;
    if (!zoomOpen) {
      const x = ev.clientX || innerWidth / 2, y = ev.clientY || innerHeight / 2;
      const t = zoomTargetAt(x, y);
      if (t) { openZoom(t); gStart = 1; zDesk = 1; }
    }
  }
  function onGestureChange(ev) {
    ev.preventDefault();
    if (TOUCHY || !zoomOpen) return;
    zoom.classList.add("desk");                          // Safari trackpad surplus eases on the img (rule 8)
    let target = gStart * (ev.scale || 1);
    if (target < 1) {                                    // pinch-IN past 1× → preview / commit the dismiss (INV-82)
      zScale = 1; zTx = 0; zTy = 0; zApply();
      if (!zBelow) {                                     // first frame below 1× re-bases at the crossing
        gStart = 1 / (ev.scale || 1);                    // — a fast crossing frame reads 1, never commits
        target = 1;                                      // by itself (INV-82, the touch path's own law)
        zBelow = true;
      }
      zDesk = target;
      if (zDesk <= DISMISS_T && !zDismissing) { zDismissing = true; zDesk = 1; history.back(); return; }
      zPreview(zDesk);                                   // Safari's trackpad pinch-shut previews too (INV-82/85)
      return;
    }
    zDesk = 1; zBelow = false; zPreviewEnd(true); zScale = Math.min(4, target); zClampPan(); zApply();
  }
  function onGestureEnd(ev) {
    ev.preventDefault();
    if (TOUCHY || !zoomOpen) return;
    if (zDesk < 1 && !zDismissing) { zDesk = 1; zBelow = false; zPreviewEnd(true); }   // an uncommitted release eases back (gestureend)
    if (zScale <= 1.03) { zScale = 1; zTx = 0; zTy = 0; zApply(); }    // near-1 release settles flat
    if (zoomOpen && !zDismissing) armInspect();          // EX-PICSTAT: the trackpad pinch coming to rest
  }
  document.addEventListener("gesturestart", onGestureStart, { passive: false });
  document.addEventListener("gesturechange", onGestureChange, { passive: false });
  document.addEventListener("gestureend", onGestureEnd, { passive: false });
  // EX-PROTECT belt: the SAME three gesture events also carry a flat preventDefault-only guard, so on
  // ANY device — touch Safari included, where the INV-85 handlers early-return on TOUCHY — the browser's
  // own viewport pinch-zoom is refused document-wide. The INV-85 handlers layer the app-zoom on top; this
  // pair keeps the raw browser gesture from ever scaling the viewport (the walk desyncs if it does).
  function onPinch(ev) { ev.preventDefault(); }
  ["gesturestart", "gesturechange", "gestureend"].forEach((g) =>
    document.addEventListener(g, onPinch, { passive: false }));
  document.addEventListener("touchmove", (e) => {
    if (e.touches.length > 1) e.preventDefault();          // a two-finger drag = a Blink pinch
  }, { passive: false });

