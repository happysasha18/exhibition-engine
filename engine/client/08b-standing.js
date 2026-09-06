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
  function standDraw() {
    // OWNER'S WORD, 2026-09-06: a work that moves while nobody is touching it is excess, and the
    // motion belongs under the hand instead (`pass-hand.js`'s own `paint()`, which this stand-down
    // never touches — the breath it rides, `breathUnit`, is unchanged). Standing off unconditionally
    // — `standClear()` takes whatever `scale` a picture still carries back off it, and returning
    // `false` is `standTick` below's own signal to stop re-arming, so the loop goes back to sleep
    // for good rather than drawing nothing forever. The rest of this function is kept rather than
    // deleted — a later "bring the ambient breath back" has a real body to re-enable, not a rewrite
    // from nothing — but nothing below this line runs any more.
    standClear();
    return false;
    const id = conductorVoiced();
    if (id == null) { standClear(); return false; }
    if (id !== standId || standViewport() !== standAt || !document.body.contains(standEl)) {
      if (!standTake(id)) return false;
    }
    const swell = (1 + standUnit()) / 2;      // the voice's own curve, ridden out of the hang alone
    standEl.style.scale = String(1 + swell * standAmp / standReach);
    return true;
  }

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
    if (standRaf !== null || typeof requestAnimationFrame !== "function") return;
    standRaf = requestAnimationFrame(standTick);
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
    };
  }
