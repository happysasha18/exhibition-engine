  // ---- the walk TRACKS its place (INV-32c — the law outlived the ↗, its first carrier):
  // the io callback above writes the per-tab marker per frame in view; any return within
  // the tab (reload, the work page's plain link, Back) restores it
  function restorePlace() {
    let m = null;
    try { m = JSON.parse(sessionStorage.getItem(PLACE_KEY) || "null"); } catch (e) {}
    try { sessionStorage.removeItem(PLACE_KEY); } catch (e) {}   // one-shot
    if (!m || m.v !== VER) return;                     // stale/foreign marker → the top, never an error
    const f = stage.querySelector('.exh-frame[data-id="' + m.id + '"]');
    if (f) scrollTo(0, frameCenter(f));               // centered in the LIVE viewport (EX-GLIDE)
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
    pulse("share_arrive", hid, shareTokenExtra());       // join back to the share that minted `s` (EX-SHARE / INV-1)
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
    // a #w- landing abandons any in-flight preload and re-aims a fresh one-ahead from the landing
    // frame, forward by default until a step declares a direction (EX-LOAD-3 / prover F5)
    travelDir = 1; preloadCancel();
    const f = stage.querySelector('.exh-frame[data-id="' + hid + '"]');
    if (f) scrollTo(0, frameCenter(f));               // instant, centered in the LIVE viewport
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
  // the face the tab last stood on survives a reload in history.state (INV-54): a reload HOLDS it —
  // the door stays the door, the walk stays the walk; only a PICK ever commits a walk behind the door.
  // A door is "held" on reload ONLY when it was reached by EXITING a walk (`returned`) — a cold door,
  // and a cold door with a returning/injected walk, keep the normal paths (greeting / the walk).
  const prior = (history.state && history.state.@@NS@@) || null;
  const returnedDoor = !!(prior && prior.face === "door" && prior.returned);
  entered = restore();
  document.body.classList.add("ex-live");              // hide the static index, wake the live face
  const handed = consumeHash();
  if (handed) {
    arriveByHash(handed);                              // the shared work itself is the welcome
  } else if (returnedDoor && doorAvailable) {
    // EX-DOOR-RELOAD (INV-54): the visitor walked, EXITED back to the door, then reloaded — HOLD the
    // door, never drop into the walk saved behind it. The held door refreshes gently: ≥60% kept, ≤40%
    // new. The `returned` mark rides on so repeated reloads keep holding the door.
    // EX-DOOR-4 (F1 folded 11:50): an unconsumed circle wins ONCE — deal fresh; every reload with no
    // circle pending obeys the reload law, and the fresh hand's own later reloads keep ≥60% too.
    const pend = circlePending();
    const sp = pend ? dealHand(pend) : refreshHand();
    renderDoor(sp, false);                             // the exit already spent the greeting
    replaceFace({ face: "door", spread: sp.map((e) => e.id), returned: true });
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

