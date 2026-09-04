/*!darkroom.js*/
// THE DARKROOM BENCH — one exported function, given one work's own record and the chain of
// instrument operations already applied to it in this session, answers which of the fleet's
// instrument ids the bench offers next, in the order it offers them.
//
// THIS IS NEW. No prior spec names a "darkroom bench" anywhere in this tree (grepped SPEC.md,
// TEST_MATRIX.md and docs/design/ before writing a line here) — the four rules below are this
// file's own construction against the record, D4's "grain appears only after structure exists"
// and Requirement 30 criterion 16's "Grain shall be seasoning and never the picture's base", both
// handed down with this file's own brief. Nothing here re-describes what an instrument reads: the
// fleet's own `manifest.suits.reads` — already the fact each instrument's own file states under
// "HOW WELL THIS INSTRUMENT SUITS A PAIR" — is read at call time, so a manifest that changes what
// it reads changes what this bench offers with no second table here to fall out of step. (This is
// a different, static, per-instrument declaration from pass-composer.js's own `INSTRUMENT_SUITS`,
// which is a set of hand-written fit functions over a PAIR of records for the crossing; this bench
// reads only the manifest's own field-path list, against the one record in front of it.)
function darkroomBenchOffers(record, chain, manifests) {
  record = record || {};
  manifests = manifests || {};
  chain = (chain || []).map(function (step) {
    if (typeof step === "string") return step;
    return (step && (step.instrument || step.id)) || null;
  }).filter(Boolean);

  function get(obj, path) {
    var parts = path.split(".");
    var v = obj;
    for (var i = 0; i < parts.length; i++) {
      if (v === null || v === undefined) return undefined;
      v = v[parts[i]];
    }
    return v;
  }

  // A resolved reading, read generically rather than per-field: a plain number is this record's
  // own measurement already on a reading's own scale (clamped, since a few fields in this schema —
  // frameSide, stepPx, periodPx — carry raw pixels rather than a 0..1 reading, and a bench asking
  // "how strong" only needs "at least as strong as the scale tops out at" from those); a non-empty
  // string or truthy value is a reading of 1 (the record named something, which a number could
  // not have said); anything absent is 0.
  function readingOf(v) {
    if (typeof v === "number" && isFinite(v)) return Math.max(0, Math.min(1, v));
    if (typeof v === "boolean") return v ? 1 : 0;
    if (typeof v === "string") return v ? 1 : 0;
    return 0;
  }

  // THE ONLY PLACE THIS FILE READS "WHAT AN INSTRUMENT READS": `manifest.suits.reads`, the array
  // of record field paths an instrument's own file already declares for ranking purposes (as
  // opposed to a handle's own per-parameter `reads:` prose, which drives one slider's default and
  // answers a narrower question than "does this instrument suit this photograph at all").
  function declaredReads(m) {
    var reads = m && m.suits && m.suits.reads;
    if (!Array.isArray(reads)) return [];
    return reads.filter(function (p) { return typeof p === "string" && p.indexOf(".") > 0; });
  }

  // WHICH PATTERN THE RECORD ALREADY CARRIES, READ CATEGORICALLY, NOT BY A MAGNITUDE FLOOR. The
  // record's own analyser always assigns structure.ownDevice.kind one of a fixed small set of
  // family names (rings/tiles/stripes over this collection's 121 records); there is no written
  // number anywhere in this tree for how confident a reading has to be before it counts as "a
  // pattern the work already carries" (this project's own history at pass-composer.js:1784-1834
  // removed exactly that kind of invented "typed floor"), so the kind itself, and the one field
  // family it names, is the fact read here — never a score compared against a chosen cutoff.
  var ownDevice = get(record, "structure.ownDevice") || {};
  var deviceKind = String(ownDevice.kind || "");
  var PATTERN_ROOTS = deviceKind ? ["structure.ownDevice"] : [];
  if (deviceKind === "tiles") PATTERN_ROOTS.push("structure.grid");
  if (deviceKind === "stripes") PATTERN_ROOTS.push("structure.banding");

  // A ROOT COUNTS AS ALREADY ADDRESSED once some earlier step in the chain is itself an instrument
  // whose own declared reads name that same root — the device it would have stacked a further
  // pattern onto has already been engaged by that step, so a later instrument reading the same
  // root no longer stacks on a pattern still standing untouched.
  function rootAddressedByChain(root) {
    return chain.some(function (id) {
      var m = manifests[id];
      return m && declaredReads(m).some(function (p) {
        return p === root || p.indexOf(root + ".") === 0;
      });
    });
  }

  function wouldStackPattern(m) {
    return declaredReads(m).some(function (p) {
      return PATTERN_ROOTS.some(function (root) {
        return (p === root || p.indexOf(root + ".") === 0)
             && !rootAddressedByChain(root);
      });
    });
  }

  // GRAIN IS SEASONING, NEVER THE BASE (D4; Requirement 30 criterion 16): an instrument declaring
  // its own `grain` handle is withheld until the chain already carries a step — any step, since
  // every instrument in this fleet cuts on some structural shape of its own (every manifest
  // declares a non-empty `cuts`), so the first applied step is already the structure grain seasons.
  function isGrainBearing(m) { return !!(m && m.handles && m.handles.grain); }
  var structuralStepDone = chain.length > 0;

  var ids = Object.keys(manifests).sort();
  var offered = ids.filter(function (id) {
    var m = manifests[id];
    if (isGrainBearing(m) && !structuralStepDone) return false;
    if (wouldStackPattern(m)) return false;
    return true;
  });

  // ORDER: by what the record's own measurements afford this instrument, read off its own
  // declared reads — the mean reading across the paths it names, strongest first. An instrument
  // that names no reads of its own (this fleet's seven ports with no `suits` block at all) affords
  // nothing to rank by and sits at the back of the order this pass gives it.
  function affordance(id) {
    var reads = declaredReads(manifests[id]);
    if (!reads.length) return 0;
    var sum = 0;
    reads.forEach(function (p) { sum += readingOf(get(record, p)); });
    return sum / reads.length;
  }
  offered.sort(function (a, b) {
    var d = affordance(b) - affordance(a);
    if (d !== 0) return d;
    return a < b ? -1 : (a > b ? 1 : 0);
  });

  // THE FOLD LEADS ON A STRONG REFLECTION. `livemirror` is the fleet's own fold — the reflection
  // the frame closes onto its own crease — the same identity lab/CROSSING-HISTORY.md's vocabulary
  // table already carries for it (`livemirror | зеркальный сгиб`, cited in this instrument's own
  // pass-inst-livemirror.js header); this is that one fact about the fleet's shape, not a second
  // list of what livemirror reads. "Strong" is read as the record's own boolean verdict rather than
  // a magnitude cutoff chosen here: symmetry.reflection.leftOntoRight.inRecipe is the reflection
  // analyser's own decision that this axis belongs to the work's symmetry recipe at all (already
  // read as a boolean elsewhere in this tree, tests/test_pass_p13.py:137), so no floor is invented
  // on top of the continuous .reading field.
  var FOLD_INSTRUMENT = "livemirror";
  var foldReflection = get(record, "symmetry.reflection.leftOntoRight") || {};
  if (foldReflection.inRecipe) {
    var at = offered.indexOf(FOLD_INSTRUMENT);
    if (at > 0) {
      offered.splice(at, 1);
      offered.unshift(FOLD_INSTRUMENT);
    }
  }

  return offered;
}

// RESIST — Requirement 41 criterion 7: "The room shall measure output busyness live and stiffen
// the gesture near the cliff, so the hand feels the edge of taste as elastic resistance; clamps
// and warnings shall never appear." `busyness` is read through engine/assets/darkroom-measure.js's
// own `busyness(frame)` (darkroom-measure.js:84-91, a fraction in [0, 1]) — this file measures
// nothing a second way; the number handed to `resist` is that call's own return value.
//
// A clamp returns a boundary; this returns a shrinking fraction of the travel the hand offered
// instead — `travel / (1 + b)`. At `b = 0` the divisor is 1 and the hand meets no resistance at
// all; as `b` climbs toward its own top of 1 the divisor climbs toward 2 and no further, so the
// returned travel is always a strictly positive multiple of `travel` — never zero, never past the
// travel the hand itself offered, and (one positive number times `travel`) never the same for two
// different travels at one busyness reading either.
function resist(travel, busyness) {
  var b = typeof busyness === "number" && isFinite(busyness) ? Math.max(0, Math.min(1, busyness)) : 0;
  return travel / (1 + b);
}

// THE EXPONENTIAL EASE — Requirement 34 criterion 4's form, `k = 1 - exp(-dt/tau)`, is why a live
// input never snaps to its target (Requirement 40 criterion 11: "every change shall pass through
// envelopes, so nothing ever snaps"). `tau` is the caller's own time constant — criterion 4 names
// 0.09s under the hand and 0.5s free — carried as a parameter here rather than chosen inside this
// function, since which one applies is a fact about the gesture's state, not about the ease.
function darkroomEase(current, target, dt, tau) {
  var k = 1 - Math.exp(-dt / tau);
  return current + (target - current) * k;
}

// ENGAGE — shelf 17's one-owner-per-level law (pass-composer.js:3994's `ownTheLevels`), felt as a
// hand's own action rather than the crossing's plan. `ownTheLevels` arbitrates who owns a level
// once, over a whole scored passage, already built; this is the same arbitration at the moment a
// person reaches for a new instrument in a live darkroom session, where the answer is not "who
// owns it" but "what happens to the instrument that is about to lose it" — and Requirement 40
// criterion 11 answers that: it never snaps, it eases (`darkroomEase`, above — no second ease is
// written here).
//
// STATE IS THE CALLER'S OWN RECORD OF WHAT IS ENGAGED, carried in and back out rather than kept
// here: a plain `{ instrumentId: { handle: value, ... }, ... }` map, the smallest shape that
// answers "what is engaged, and at what handle values" — everything `engage` needs to know what to
// walk back, and nothing it would otherwise have to keep of its own between calls.
//
// A LEVEL IS READ THE ONE PLACE THIS FLEET DECLARES IT: a handle's own `level` field on its own
// manifest (e.g. pass-inst-livemirror.js:687-728), never a second table kept here — the same field
// `ownTheLevels`'s own `levelOf` reads (pass-composer.js:4245-4248). `level: null` claims no level
// and answers to no exchange, exactly as `levelOf` already treats it.
//
// dt/tau are Requirement 34 criterion 4's own pair for a change nobody's hand is driving live —
// "0.5s free" — since this walk-back runs while the hand has moved on to the newly engaged
// instrument, not while it holds the one being walked back. Kept local to the function, like every
// other constant this file's own extracted-function tests read (darkroom.js is extracted by
// balanced braces per function; a module-level var here would be invisible to that extraction).
function engage(instrumentId, state, manifests) {
  var ENGAGE_DT = 1 / 60;
  var ENGAGE_TAU = 0.5;
  state = state || {};
  manifests = manifests || {};
  var manifest = manifests[instrumentId] || {};
  var handles = manifest.handles || {};

  function levelOf(m, handle) {
    var spec = m && m.handles && m.handles[handle];
    return (spec && spec.level) || null;
  }

  // A HANDLE CLAIMS A LEVEL ONLY WHEN IT DECLARES ONE — `level: null` (or no `level` at all) is not
  // itself a level two handles can share; it is the fleet's own idiom for "answers to no ownership
  // at all" (pass-composer.js:4245-4248's `levelOf`). One place decides that, so nothing downstream
  // re-decides it a second way.
  function isRealLevel(lv) { return !!lv; }

  // THE LEVELS THIS INSTRUMENT DECLARES AT ALL — the union of every one of its own handles' `level`,
  // read off its manifest, `level: null` entries dropped as claiming nothing.
  var incomingLevels = [];
  Object.keys(handles).forEach(function (h) {
    var lv = handles[h] && handles[h].level;
    if (isRealLevel(lv) && incomingLevels.indexOf(lv) < 0) incomingLevels.push(lv);
  });

  // A copy, never the caller's own object — `engage` hands back the next state rather than mutating
  // the one it was given.
  var next = {};
  Object.keys(state).forEach(function (iid) {
    next[iid] = {};
    Object.keys(state[iid] || {}).forEach(function (h) { next[iid][h] = state[iid][h]; });
  });

  // WALK BACK EVERY ALREADY-ENGAGED HANDLE STANDING ON A LEVEL THE NEWLY ENGAGED INSTRUMENT ALSO
  // DECLARES — one ease step per call, so a session driving `engage` every frame the collision
  // stands feels the handle travel down to its own manifest's `def` rather than land there at once.
  if (incomingLevels.length) {
    Object.keys(next).forEach(function (iid) {
      if (iid === instrumentId) return;
      var otherManifest = manifests[iid] || {};
      Object.keys(next[iid]).forEach(function (h) {
        var lv = levelOf(otherManifest, h);
        if (!isRealLevel(lv) || incomingLevels.indexOf(lv) < 0) return;
        var spec = otherManifest.handles[h];
        var def = spec && typeof spec.def === "number" ? spec.def : next[iid][h];
        next[iid][h] = darkroomEase(next[iid][h], def, ENGAGE_DT, ENGAGE_TAU);
      });
    });
  }

  // A FIRST ENGAGEMENT STARTS AT REST — every handle this instrument declares, at its own
  // manifest's `def`, the same rest every neutral pose in this fleet already means. Re-engaging an
  // instrument already in state leaves its own current values exactly where they stood.
  if (!next[instrumentId]) {
    next[instrumentId] = {};
    Object.keys(handles).forEach(function (h) {
      var d = handles[h] && handles[h].def;
      next[instrumentId][h] = typeof d === "number" ? d : 0;
    });
  }

  return next;
}
