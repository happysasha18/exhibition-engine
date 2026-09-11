  // ---- EX-STANDING (S-112): the standing work is drawn breathing on the walk ---------------------
  // SPEC.md Requirement 37, standing life at rest. The whisper voice (`engine/assets/pass-hand.js`,
  // S-37) computes a breath and the conductor (`08a-conductor.js`, S-39) says whose it is; until
  // this file both stopped at a report, and a visitor walking the gallery met neither. This file is
  // the surface: the work the conductor seated is drawn breathing, inside the box the hang measured
  // (`hangGeometry`, S-91), and every other work stands exactly as still as it stood before.
  //
  // THE THREE PIECES, EACH READ AND NONE REBUILT.
  //   · the voice — `passHand.unit()`: the breath's own curve between -1 and 1, with the hold's gain
  //     and the seat's gain already in it. A work the conductor gave no seat reads 0 here, and 0 is
  //     what this file writes, which is a work standing still.
  //   · the seat — `conductorVoiced()`: the one work carrying the voice this instant, by the very
  //     rule the voice reads its own gain by. One name, one home, so the work that is voiced and the
  //     work that is drawn cannot be two different works.
  //   · the frame — `hangGeometry(id)`: the box the walk hung that work in, read the way a crossing
  //     reads it.
  //
  // WHERE EVERY NUMBER COMES FROM, AND WHY NONE IS TYPED HERE BUT THE CRITERIA'S OWN FRACTIONS.
  // Requirement 37 states the band as fractions of a letter's full crossing travel — criterion 1's
  // thirty-second for the breath, criterion 3's sixth for the hard cap — and then states the SAME
  // ceiling a second time in the units a drawn frame actually has: criterion 4, "at rest, any frame
  // shall differ from the canonical work by under 1 % of frame width in any pixel's displacement".
  // Criterion 3's sixth and criterion 4's one percent are the same ceiling read from two sides, so
  // on the shipped frame the letter's full travel is six percent of the frame's own width, and
  // criterion 1's thirty-second of that travel is the amplitude below. Nothing is measured, nothing
  // is tuned, and the peak displacement this file ever draws is a fifth of what criterion 4 allows.
  //
  // WHAT IS DRAWN, AND WHY IT IS STILL THE WORK. A uniform scale about the work's own centre: the
  // swell. A photograph scaled by a fraction of a percent is that photograph, so criterion 4's
  // screenshot law holds in kind as well as in magnitude, and the amplitude above is the
  // displacement of the pixel furthest from the centre — the corner — which is the quantity the
  // criterion names. The letter is written with the standalone `scale` property rather than
  // `transform`, so the computed `transform` the hang reads (`hangGeometry`) stays untouched.
  //
  // AND THE SWELL RIDES ONE-SIDED, OUT OF THE HANG AND BACK INTO IT — never through it. This is the
  // same argument `pass-hand.js` already makes for the rubato on the period: a swing centred on the
  // resting point spends half its life on the wrong side of the very thing that point names, and
  // here that point is the box the walk hung the work in. A work that spent half its breath SMALLER
  // than its hang would make its own box disagree with the hang by up to the amplitude, and the box
  // is a shared fact — the site's own frame row (S-91) reads it to ask whether a crossing painted
  // outside the work, and it went red by exactly this amplitude while the breath swung both ways.
  // Riding outward only, the picture is never smaller than the box anyone else reads, and the whole
  // travel is still the amplitude above. The one-sided reading is the voice's own curve mapped onto
  // its positive half — no second curve, and the phase, the period and the two gains are all the
  // voice's.
  //
  // NOTHING BRANCHES ON THE DEVICE. One CSS property on one element, at any ceiling S-110 reads;
  // this file takes no reading of its own and holds no fallback of its own.
  const STAND_STILL = 0.01;   // criterion 4 — "under 1 % of frame width in any pixel's displacement"
  const STAND_CAP = 6;        // criterion 3 — the hard cap is a sixth of the travel
  const STAND_BREATH = 32;    // criterion 1 — the breath is a thirty-second of the travel
  // The travel in the frame's own width, and the breath's share of it: 6 % and 6/32 of a percent.
  const STAND_AMPLITUDE = STAND_STILL * STAND_CAP / STAND_BREATH;

  let standId = null;      // the work being drawn, or null
  let standEl = null;      // its own picture, the one element this file ever writes
  let standAmp = 0;        // the peak displacement in CSS pixels, off that work's own box
  let standReach = 0;      // the distance from the box's centre to its furthest corner
  let standAt = "";        // the viewport the box above was measured on
  let standRaf = null;

  function standViewport() { return innerWidth + "x" + innerHeight; }

  // The work stops being written the instant it stops being the one the conductor voiced, so a work
  // left behind by a scroll is left standing rather than frozen mid-breath at somebody else's phase.
  function standClear() {
    if (standEl) { standEl.style.scale = ""; }
    standId = null; standEl = null; standAmp = 0; standReach = 0; standAt = "";
  }

  // The box, taken once per work and again when the viewport changes shape. It is read while the
  // picture carries no scale of its own — a fresh work has none, and `standClear` above takes the
  // old one off first — so the reading is of the hang and never of this file's own last frame.
  //
  // A WORK WHOSE PIXELS HAVE NOT ARRIVED HANGS IN A BOX OF NOTHING, and nothing is taken from it:
  // the reading is refused and tried again on the next frame, so the work is taken the moment it
  // has a box, and the same road answers a work whose box grows when its picture lands. The
  // assignment happens only once the box is real, so no half-taken work is ever left cached.
  function standTake(id) {
    const frame = condFrameOf(id);
    const el = (frame && frame.querySelector) ? frame.querySelector("img.work") : null;
    standClear();
    if (!el) return false;
    const g = hangGeometry(id);
    const reach = g ? Math.hypot(g.w, g.h) / 2 : 0;
    if (!reach) return false;
    standId = id; standEl = el;
    standAmp = g.w * STAND_AMPLITUDE;
    standReach = reach;
    standAt = standViewport();
    return true;
  }

  function standUnit() {
    if (!passHand || typeof passHand.unit !== "function") return 0;
    try { const u = +passHand.unit(); return isFinite(u) ? u : 0; } catch (e) { return 0; }
  }

  // Answers whether a breath was actually written, which is what the loop below runs on.
  // ---- THE STANDING WORK ANSWERS THE HAND ON ITS OWN LETTER (2026-09-11, his word: «в стоячем
  // положении можно больше эффектов из имеющихся задействовать», held together with his word of
  // 2026-09-06 above: motion belongs under the hand). Nothing moves while nobody touches. The
  // moment the hand stands on a work — a hover, a finger — the composer is asked for that work's
  // crossing WITH ITSELF (one pivot cue on the instrument its own structure cuts on), and the
  // drawing layer holds that crossing as a «stand» (pass-layer.js: no watchdog, the frame clipped
  // to the work's own box, cut at once by any real crossing), its clock pinned every frame to what
  // the hand says, in lab/STANDING-LIFE-DRAFT.md shelf 20's own band: under a resting hand the
  // voice's breath (`passHand.unit`, period eight seconds) through the first thirty-second of the
  // pass — criterion 1's R/32, R the letter's full crossing travel; under an engaged drag the
  // hand's own lean, read off the hand's report against the cap the hand already holds it to,
  // criterion 1 of Requirement 38's R/8, on top of the breath. So the work moves exactly as its
  // own crossing would begin, and no further than an eighth of it, and it rests again when the
  // hand leaves. Every number is the requirement's or the composer's; nothing scales with the
  // collection — one request, for the one work under the hand, when the hand arrives.
  const STAND_SHARE = 1 / STAND_BREATH;     // R/32 — the breath's share of the letter's travel
  const STAND_LEAN = 1 / 8;                  // R/8  — the lean's cap, Requirement 38 criterion 1
  let standCmd = null;                       // {id, gen, duration} of the running stand
  let standN = 0;                            // stands are numbered below zero: never a crossing's gen

  function standLayerReport() {
    try { return passLayer && typeof passLayer.report === "function" ? passLayer.report() : null; } catch (e) { return null; }
  }
  function standHand() {
    try { return passHand && typeof passHand.report === "function" ? passHand.report() : null; } catch (e) { return null; }
  }
  function standEnd(why) {
    if (!standCmd) return;
    standCmd = null;
    try { passLayer.configure({ clockPin: null, progressPin: null }); } catch (e) {}
    try { passLayer.cancel("stand: " + why, true); } catch (e) {}
  }
  function standOffer(id) {
    const frame = condFrameOf(id);
    if (!frame || !passComposer || !passLayer) return false;
    let req = null, made = null;
    try { req = passRequestFor(frame, frame); } catch (e) { req = null; }
    if (!req) return false;
    try { made = passComposer.passageFor(req); } catch (e) { made = null; }
    const score = made && !made.declined ? made.score : null;
    if (!score) return false;
    const gen = -(++standN);
    const cmd = Object.freeze({
      gen: gen, from: { id: String(id), n: 1 }, to: { id: String(id), n: 1 },
      dir: 1, span: 0, kind: "stand", cause: "stand", velocity: 0,
      reduced: !!REDUCED, saveData: !!dataSaver(),
      rtl: (document.documentElement.getAttribute("dir") === "rtl"),
      dpr: window.devicePixelRatio || 1,
      viewport: Object.freeze({ w: innerWidth, h: innerHeight }),
      params: passSnapshot(score), score: score,
      signal: Object.freeze({ get aborted() { return !standCmd || standCmd.gen !== gen; } }),
    });
    let took = false;
    try {
      passLayer.configure({ clockPin: 0, progressPin: 0 });
      took = passLayer.offer(cmd, {
        dock: function () {}, glide: function () { if (standCmd && standCmd.gen === gen) standCmd = null; },
        curtain: function () {}, mark: passMark, hangGeometry: hangGeometry, handoff: function () {},
      }) === true;
    } catch (e) { took = false; }
    if (!took) { try { passLayer.configure({ clockPin: null, progressPin: null }); } catch (e) {} return false; }
    standCmd = { id: String(id), gen: gen, duration: +score.duration || 0 };
    return true;
  }
  function standDraw() {
    standClear();                                   // the CSS swell stays off (his word of 2026-09-06)
    const rep = standLayerReport(), hand = standHand();
    if (!rep) { standCmd = null; return false; }
    if (rep.active) { standCmd = null; return false; }          // a crossing owns the frame; a stand was cut with it
    // THE HAND IS ON THE WORK: attached by the walk AND a hover standing on the picture or an
    // engaged pointer (`over`/`pressed`, pass-hand.js's own report). The walk also attaches the hand
    // at every dock with nobody touching, so attachment alone is not a hand.
    const present = !!(hand && hand.attached != null && (hand.over || hand.pressed));
    const id = present && conductorVoiced() != null ? String(hand.attached) : null;
    const standGen = rep.stand ? rep.stand.gen : null;          // the stand the layer holds, by its own row
    if (standCmd && standGen !== standCmd.gen) standCmd = null;  // ended elsewhere
    if (id == null) {
      if (standCmd) standEnd("the hand left");
      else if (rep.standing) {                                   // a stand of this file's the record lost track of
        try { passLayer.configure({ clockPin: null, progressPin: null }); passLayer.cancel("stand: the hand left", true); } catch (e) {}
      }
      return false;
    }
    if (standCmd && standCmd.id !== id) standEnd("the hand moved to another work");
    if (!standCmd) {
      if (rep.standing || rep.state === "awaiting") return true;   // its own stand still leaving, or an offer warming
      return standOffer(id);
    }
    const breath = STAND_SHARE * (1 + standUnit()) / 2;         // out of the rest and back, never through it
    const lean = hand.lean && hand.lean.cap > 0 ? STAND_LEAN * Math.min(1, Math.abs(+hand.lean.value || 0) / hand.lean.cap) : 0;
    const at = Math.min(1, breath + lean);
    try { passLayer.configure({ clockPin: at * standCmd.duration / 1000, progressPin: at }); } catch (e) {}
    return true;
  }
  // The hand arriving on a work is the fourth thing that makes a work drawable (the three below
  // are the hang, a work in view and a dock): the walk attaches the hand on these same events
  // (01a-pass.js), so the loop is woken here on the same reach, passively, and goes back to sleep
  // the moment the hand leaves and `standDraw` returns false.
  ["pointerover", "pointerdown"].forEach((name) => {
    addEventListener(name, (e) => {
      if (e.target && e.target.closest && e.target.closest(".exh-frame img.work")) standWake();
    }, { capture: true, passive: true });
  });

  // ONE LOOP, AND ONLY WHILE A WORK IS ACTUALLY BEING DRAWN. It is requestAnimationFrame all the way
  // down, so a hidden tab is not drawing and this file is asleep with it, and it holds no timer and
  // no scroll listener. A breathing work is a frame written per frame; that write is what the row
  // exists for, and there is one of it.
  //
  // IT STOPS THE INSTANT THERE IS NOTHING TO DRAW, and this is not thrift for its own sake — it is
  // Requirement 39's own battery argument, and the first shape of this file got it wrong. That shape
  // re-armed unconditionally while the walk had ever hung a frame, so it went on running with the
  // visitor standing at the door, and with a crossing covering the room, and — worst — over frames
  // the walk had already taken out of the document, where every frame re-read a hang that was no
  // longer there. Across a session that walks door to walk and back many times it left the page
  // rendering continuously and forcing a layout per frame for nothing, and the walk's own in-view
  // marks began to land late enough that the door's circle row (tests/test_door.py's EX-DOOR-4, "the
  // marks count the moment they are made") went red — a row this row never touched.
  //
  // THREE THINGS WAKE IT, and each is a moment when a work becomes drawable: the walk hanging frames
  // (`14-walk-render.js`), a work coming into view (the conductor's own observer, `08a-conductor.js`)
  // and a crossing landing (`dock`, 01a-pass.js). Nothing else has to, because nothing else can make
  // a work drawable that was not drawable before.
  function standTick() {
    standRaf = null;
    if (!condFrames.length) return;
    let drew = false;
    try { drew = standDraw(); } catch (e) { standClear(); drew = false; }
    if (drew) standWake();
  }
  function standWake() {
    tiltArm();
    if (standRaf !== null || typeof requestAnimationFrame !== "function") return;
    standRaf = requestAnimationFrame(standTick);
  }

  // ---- EX-TILT: the standing work slides with the tilt of the phone (his word 2026-09-10 18:42) ---
  // A picture at rest on a phone that nobody is touching answers the phone's own tilt: tipped left,
  // it slides a little left; tipped forward, a little down; and it does so on a mass, so it creeps
  // after the hand and settles rather than snapping. This is not the ambient breath the owner
  // retired on 2026-09-06 — nothing moves unless the visitor moves the phone.
  //
  // WHAT IT WRITES. The standalone `translate` property on the one picture the conductor seated —
  // the same element `standDraw` above wrote its `scale` on, for the same reason: the computed
  // `transform` the hang reads (`hangGeometry`) and the hand layer's own `transform` (pass-hand.js
  // `paint`) both stay untouched, so the three never overwrite each other. The touch overlay
  // (pass-touch.js) carries the picture's `translate` the way it already carries its `transform`.
  //
  // THE HAND WINS. While a finger is on the work the slide eases home and stays there: under the
  // hand the picture answers the hand (pass-hand.js), and two movements at once is a picture that
  // answers neither.
  //
  // THE ASK. Safari on iOS hands out the tilt only after the visitor says yes, and only asks inside
  // a tap. So on such a phone the ask rides the first tap on a work of the walk — the dialog is the
  // browser's own — and is made once per page; a no is remembered for the session, never nagged.
  // Elsewhere the events either flow without an ask (Android) or never come (a desk), and nothing
  // is asked or armed on a fine pointer at all.
  const TILT_REACH = 0.04;   // at full tilt the picture has slid 4 % of its own width
  const TILT_FULL = 18;      // the tilt, in degrees off where the phone was, that counts as full
  const TILT_K = 10;         // the spring's stiffness ...
  const TILT_D = 5.5;        // ... and its damping: the slide creeps and settles in about a second
  let tiltArmed = false, tiltOn = false, tiltZero = null, tiltListening = false;
  const tiltTarget = { x: 0, y: 0 }, tiltPos = { x: 0, y: 0 }, tiltVel = { x: 0, y: 0 };
  let tiltEl = null, tiltRaf = null, tiltAt = 0, tiltHand = false;

  function tiltCoarse() {
    try { return matchMedia("(pointer: coarse)").matches; } catch (e) { return false; }
  }
  function tiltRead(e) {
    if (e.gamma == null || e.beta == null) return;
    if (!tiltZero) tiltZero = { b: e.beta, g: e.gamma };
    let x = (e.gamma - tiltZero.g) / TILT_FULL, y = (e.beta - tiltZero.b) / TILT_FULL;
    // a phone turned on its side reads its axes turned with it
    let angle = 0;
    try { angle = (screen.orientation && screen.orientation.angle) || 0; } catch (err) { angle = 0; }
    if (angle === 90) { const t = x; x = -y; y = t; }
    else if (angle === 270 || angle === -90) { const t = x; x = y; y = -t; }
    tiltTarget.x = Math.max(-1, Math.min(1, x));
    tiltTarget.y = Math.max(-1, Math.min(1, y));
    tiltOn = true;
    tiltWake();
  }
  function tiltListen() {
    if (tiltListening) return;
    tiltListening = true;
    addEventListener("deviceorientation", tiltRead);
  }
  function tiltAsk(e) {
    const img = e.target && e.target.closest ? e.target.closest(".exh-frame img.work") : null;
    if (!img) return;
    removeEventListener("pointerup", tiltAsk, true);
    try {
      if (sessionStorage.getItem("ex-tilt") === "no") return;
      DeviceOrientationEvent.requestPermission().then((r) => {
        if (r === "granted") tiltListen();
        else try { sessionStorage.setItem("ex-tilt", "no"); } catch (err) {}
      }).catch(() => {});
    } catch (err) {}
  }
  function tiltArm() {
    if (tiltArmed) return;
    tiltArmed = true;
    if (!tiltCoarse() || typeof DeviceOrientationEvent === "undefined") return;
    // the hand: the slide goes home while a finger is on a work, and comes back when it lifts
    addEventListener("pointerdown", (e) => {
      if (e.target && e.target.closest && e.target.closest(".exh-frame img.work")) { tiltHand = true; tiltWake(); }
    }, true);
    const lift = () => { if (tiltHand) { tiltHand = false; tiltWake(); } };
    addEventListener("pointerup", lift, true);
    addEventListener("pointercancel", lift, true);
    if (typeof DeviceOrientationEvent.requestPermission === "function") addEventListener("pointerup", tiltAsk, true);
    else tiltListen();
  }
  function tiltClear() {
    if (tiltEl) { try { tiltEl.style.translate = ""; } catch (e) {} }
    tiltEl = null; tiltPos.x = tiltPos.y = tiltVel.x = tiltVel.y = 0;
  }
  function tiltTick() {
    tiltRaf = null;
    const t = performance.now();
    const dt = Math.min(0.05, tiltAt ? (t - tiltAt) / 1000 : 0);
    tiltAt = t;
    let id = null;
    try { id = conductorVoiced(); } catch (e) { id = null; }
    const frame = id != null ? condFrameOf(id) : null;
    const el = (frame && frame.querySelector) ? frame.querySelector("img.work") : null;
    if (el !== tiltEl) { tiltClear(); tiltEl = el; }
    if (!tiltEl || !document.body.contains(tiltEl)) { tiltClear(); tiltAt = 0; return; }
    const home = tiltHand || !tiltOn;
    const tx = home ? 0 : tiltTarget.x, ty = home ? 0 : tiltTarget.y;
    // a mass on a spring, towards where the tilt points
    tiltVel.x += ((tx - tiltPos.x) * TILT_K - tiltVel.x * TILT_D) * dt;
    tiltVel.y += ((ty - tiltPos.y) * TILT_K - tiltVel.y * TILT_D) * dt;
    tiltPos.x += tiltVel.x * dt;
    tiltPos.y += tiltVel.y * dt;
    const w = tiltEl.getBoundingClientRect().width;
    const reach = w * TILT_REACH;
    tiltEl.style.translate = (tiltPos.x * reach).toFixed(2) + "px " + (tiltPos.y * reach).toFixed(2) + "px";
    const moving = Math.abs(tx - tiltPos.x) > 0.002 || Math.abs(ty - tiltPos.y) > 0.002
                || Math.abs(tiltVel.x) > 0.002 || Math.abs(tiltVel.y) > 0.002;
    if (moving) tiltWake();
    else { tiltAt = 0; if (home) tiltClear(); }
  }
  function tiltWake() {
    if (tiltRaf !== null || typeof requestAnimationFrame !== "function") return;
    tiltRaf = requestAnimationFrame(tiltTick);
  }
  function tiltReport() {
    return { armed: tiltArmed, listening: tiltListening, coarse: tiltCoarse(), on: tiltOn, hand: tiltHand, drawing: tiltEl ? (condIdOf(tiltEl.closest(".exh-frame")) || null) : null,
             target: { x: tiltTarget.x, y: tiltTarget.y }, at: { x: tiltPos.x, y: tiltPos.y },
             translate: tiltEl ? (tiltEl.style.translate || null) : null,
             law: { reachOfWidth: TILT_REACH, fullDegrees: TILT_FULL, k: TILT_K, d: TILT_D } };
  }

  // The report, on the diagnostic surface beside the conductor's (01a-pass.js): which work is being
  // drawn, on what box, how far its breath is granted to travel, and the three fractions that
  // granted it. The scale actually standing on the picture is read off the element rather than
  // recomputed, so a row reads what a visitor is looking at.
  function standingReport() {
    return {
      version: 1,
      drawing: standId,
      unit: standUnit(),
      scale: standEl ? (standEl.style.scale || null) : null,
      swell: standEl ? (1 + standUnit()) / 2 : 0,
      frame: standId ? { amplitudePx: standAmp, reachPx: standReach, at: standAt } : null,
      law: { stillOfFrameWidth: STAND_STILL, capOfTravel: STAND_CAP, breathOfTravel: STAND_BREATH,
             amplitudeOfFrameWidth: STAND_AMPLITUDE },
      running: standRaf !== null,
      tilt: tiltReport(),
    };
  }
