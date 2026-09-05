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
// THE PREDICATE FOR "DOES THIS INSTRUMENT SPEND THE ROOM'S MIRACLE SLOT" — the same derivation
// pass-composer.js's own `isWorldFold` reads (pass-composer.js:1729-1735): a manifest carrying a
// real `surface` and naming WORLD among its own `levels`. Read fresh off the manifests handed in
// here, every call, so a manifest that changes its own surface/levels declaration changes this
// answer with no second, hand-typed list of instrument ids anywhere in this file.
function isSlotSpendingInstrument(instrumentId, manifests) {
  var m = (manifests || {})[instrumentId];
  return !!(m && m.surface && (m.levels || []).indexOf("WORLD") >= 0);
}

// THE ROOM'S ONE MIRACLE SLOT — one per making, spent either by opening the room's own recursion
// (the pinch past the frame, modelled here only as a state the caller sets — not built in this
// unit) or by engaging an instrument `isSlotSpendingInstrument` answers true for. State is the
// caller's own record, carried in and back out, the same idiom `engage`'s own `state` already
// uses: `{ spent: bool, spentBy: "recursion" | <instrumentId> | null }`.
function darkroomSlotState() {
  return { spent: false, spentBy: null };
}

// Engaging an instrument spends the slot once, attributed to that instrument — a slot already
// spent, or an instrument that does not fold space, leaves the slot exactly as it stood.
function darkroomSlotAfterEngage(slot, instrumentId, manifests) {
  slot = slot || darkroomSlotState();
  if (slot.spent) return slot;
  if (!isSlotSpendingInstrument(instrumentId, manifests)) return slot;
  return { spent: true, spentBy: instrumentId };
}

// Unwinding an instrument (unengaging it, or walking its handle back to its own declared neutral)
// returns the slot only when that instrument is the one holding it spent — unwinding any other
// instrument, or one that never spent the slot, leaves it exactly as it stood.
function darkroomSlotAfterUnwind(slot, instrumentId) {
  slot = slot || darkroomSlotState();
  if (slot.spentBy === instrumentId) return darkroomSlotState();
  return slot;
}

// Opening the recursion spends the slot, attributed to "recursion" rather than an instrument id
// (no manifest declares it — it is the room's own state); closing it returns the slot only when
// the recursion is the one holding it spent.
function darkroomSlotAfterRecursion(slot, open) {
  slot = slot || darkroomSlotState();
  if (open) {
    if (slot.spent) return slot;
    return { spent: true, spentBy: "recursion" };
  }
  if (slot.spentBy === "recursion") return darkroomSlotState();
  return slot;
}

function darkroomBenchOffers(record, chain, manifests, slot) {
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

  // THE MIRACLE SLOT, IF SPENT, WITHHOLDS EVERY OTHER SLOT-SPENDING INSTRUMENT — absence, never a
  // refusal: a visitor meets no rule as a blocking error, the instrument is simply missing from
  // this list. The instrument already holding the slot spent stays offered (re-engaging it, or
  // reaching its own handles, is not a second spend).
  var slotSpent = !!(slot && slot.spent);
  var slotSpentBy = slot && slot.spentBy;

  var ids = Object.keys(manifests).sort();
  var offered = ids.filter(function (id) {
    var m = manifests[id];
    if (isGrainBearing(m) && !structuralStepDone) return false;
    if (wouldStackPattern(m)) return false;
    if (slotSpent && id !== slotSpentBy && isSlotSpendingInstrument(id, manifests)) return false;
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

// ================================================================================================
// S-47 — THE RESULT'S LIFE. The link is the work: a making is written as one word, the word is read
// back, and the film of that making is compiled through the crossing skeleton — the same
// `passageFor` every edge of the walk comes through — with the seam check and the no-cut lint run
// on every film before it is handed back.
//
// SPEC.md Requirement 41, criteria 13 (the word), 15 (compiled through the skeleton, never replayed
// step by step), 16 (both checks on every compiled movie), 18 (the card), 35 and 36 (a word whose
// referents moved). The word's own shape is donated by lab/make-your-own.js:38, :421, :472 — the
// photograph by NAME, the chain in order with each step's numbers, and the recursion depth, with a
// step resting at its quiet value writing nothing and a depth of 1 leaving no mark.
//
// NOTHING HERE IS KEYED BY A PAIR. The film is composed at the moment the link is opened, out of
// the two records in front of it, exactly as Requirement 12 binds every other crossing.
// ================================================================================================

// FOUR DECIMALS, AND THE PLACE THAT NUMBER IS READ FROM: every value a work record carries is
// already written at four (lab/analyze/recipes.py rounds each of its own readings with `round(x, 4)`),
// so a word written at the same precision can never say more about a handle than the collection
// says about a photograph.
function darkroomRound4(v) {
  var n = Number(v);
  if (n !== n || !isFinite(n)) return 0;
  return Math.round(n * 10000) / 10000;
}

function darkroomClamp(v, lo, hi) {
  if (typeof lo === "number" && v < lo) return lo;
  if (typeof hi === "number" && v > hi) return hi;
  return v;
}

// THE WORD. `making` is `{photo, chain: [{instrument, handles}], depth}`; `manifests` is the fleet's
// own registration map, the one place a handle's range and its quiet value are declared.
function darkroomWord(making, manifests) {
  making = making || {};
  manifests = manifests || {};
  var photo = making.photo === undefined || making.photo === null ? "" : String(making.photo);
  var steps = [];
  (making.chain || []).forEach(function (step) {
    var id = step && (step.instrument || step.id);
    if (!id) return;
    var declared = (manifests[id] || {}).handles || {};
    var handles = (step && step.handles) || {};
    var parts = [String(id)];
    Object.keys(handles).sort().forEach(function (h) {
      var v = darkroomRound4(handles[h]);
      var spec = declared[h];
      // A STEP RESTING AT ITS QUIET VALUE WRITES NONE, so a word stays as short as the making was
      // (lab/make-your-own.js:435-438, the same rule and the same reason).
      if (spec && typeof spec.def === "number" && v === darkroomRound4(spec.def)) return;
      parts.push(h + "=" + v);
    });
    steps.push(parts.join(","));
  });
  var word = photo + "/" + steps.join(";");
  var depth = Math.round(Number(making.depth) || 1);
  if (depth > 1) word += "/x" + depth;
  return word;
}

// THE WORD READ BACK. A step naming an instrument the registry no longer carries keeps its place in
// the order and names no handle of its own — Requirement 41 criterion 36's «held at its declared
// neutral», so the surviving steps still read in their own order.
function darkroomReadWord(text, manifests) {
  if (typeof text !== "string" || !text) return null;
  manifests = manifests || {};
  var parts = text.split("/");
  var photo = parts[0];
  if (!photo) return null;
  var chain = [];
  (parts[1] ? parts[1].split(";") : []).forEach(function (token) {
    if (!token) return;
    var fields = token.split(",");
    var id = fields.shift();
    if (!id) return;
    var manifest = manifests[id];
    var declared = (manifest || {}).handles || {};
    var handles = {};
    if (manifest) {
      Object.keys(declared).forEach(function (h) {
        var d = declared[h] && declared[h].def;
        handles[h] = typeof d === "number" ? d : 0;
      });
      fields.forEach(function (field) {
        var at = field.indexOf("=");
        if (at < 0) return;
        var h = field.slice(0, at);
        var v = Number(field.slice(at + 1));
        if (v !== v || !isFinite(v) || !declared[h]) return;
        handles[h] = darkroomClamp(v, declared[h].min, declared[h].max);
      });
    }
    chain.push({ instrument: id, handles: handles, held: !manifest });
  });
  var depth = 1;
  if (parts[2] && parts[2].charAt(0) === "x") {
    var d = parseInt(parts[2].slice(1), 10);
    if (d >= 1) depth = d;
  }
  return { photo: photo, chain: chain, depth: depth };
}

// THE MADE WORK'S OWN RECORD. Requirement 41 criterion 19 — the analysers run on the result, so the
// visitor's work carries the same measurements as the collection's own. The room measures the lit
// print live through darkroom-measure.js's `bestAxis`, and the two readings that measurement answers
// are the two the record already names: `symmetry.reflection.leftOntoRight` and `topOntoBottom`
// (lab/build-workrecords-v1.py:242-245, filled from recipes.py's own `best_axis`). Every other
// reading is carried across untouched — the making did not measure it, so this file does not claim
// it. The id is the word itself, which is what the made work is called.
function darkroomMadeRecord(record, word, measured) {
  var made = {};
  Object.keys(record || {}).forEach(function (k) { made[k] = record[k]; });
  made.id = String(word);
  measured = measured || {};
  var sym = record && record.symmetry;
  if (!sym || !sym.reflection) return made;
  var reflection = {};
  Object.keys(sym.reflection).forEach(function (k) { reflection[k] = sym.reflection[k]; });
  function write(name, axisKey, read) {
    if (!read || typeof read.position !== "number" || typeof read.score !== "number") return;
    var was = reflection[name] || {};
    var now = {};
    Object.keys(was).forEach(function (k) { now[k] = was[k]; });
    now[axisKey] = darkroomRound4(read.position);
    now.reading = darkroomRound4(read.score);
    reflection[name] = now;
  }
  write("leftOntoRight", "axisX", measured.leftOntoRight);
  write("topOntoBottom", "axisY", measured.topOntoBottom);
  var symmetry = {};
  Object.keys(sym).forEach(function (k) { symmetry[k] = sym[k]; });
  symmetry.reflection = reflection;
  made.symmetry = symmetry;
  return made;
}

// A NUMBER IS UNWRAPPED THE ONE WAY THE COMPOSER'S OWN READERS UNWRAP IT — the score carries
// Python's floats as `{v: n}` (pass-composer.js's `Flt`), and every reader of a composed plan in
// this tree does exactly this (tests/test_pass_step_sequencer.py's own `unwrap`).
function darkroomNum(v) {
  if (v && typeof v === "object" && "v" in v) return Number(v.v);
  return Number(v);
}

// THE GROUND OF A FILM — the one cue that spans it whole. The composer builds the pivot's window at
// `[0, duration]` before it reads an argument, so the ground never sequences, and it is the voice a
// film's own travel rides.
function darkroomFilmGround(plan) {
  var cues = (plan && plan.cues) || [];
  var duration = darkroomNum(plan && plan.duration) / 1000;
  for (var i = 0; i < cues.length; i++) {
    var w = cues[i].window || [];
    if (darkroomNum(w[0]) <= 0 && Math.abs(darkroomNum(w[1]) - duration) < 0.001) return cues[i];
  }
  return null;
}

// THE TWO CHECKS EVERY COMPILED MOVIE IS RUN THROUGH — Requirement 41 criterion 16. Both read the
// compiled plan and nothing else: no clock, no browser, no frame.
//
// THE SEAM. A handoff is a change of authority (tests/test_pass_seam.py's own words), and on a plan
// the authority change is the cue's own door: the handle it enters on and the handle it leaves on.
// A cue with no door on a side hands the frame over with nothing standing at the handover, which is
// the seam vanishing. The film's own two ends are the same fact at the outside: the camera rests on
// the departing work at the head and the arriving one at the foot (Requirement 14 criterion 3).
//
// THE NO CUT. Shelf 18 (SPEC.md Requirement 30 criterion 9) — «playing whole operations one after
// another, each from start to finish, is banned». Three counts, each a splice the ban names:
// the ground must span the film whole (a ground that opens late or closes early leaves the film
// with a head or a tail nothing holds); no voice may be laid end to end after another, which is the
// same predicate tests/test_pass_step_sequencer.py reads off `cues[i].window`; and the camera's own
// knots must run forward inside the film's own span, because a knot out of order is a camera cut,
// and Requirement 14 criterion 2 makes a camera cut one instance of the same ban.
function darkroomFilmChecks(plan) {
  var cues = (plan && plan.cues) || [];
  var track = ((plan && plan.camera) || {}).track || [];
  var duration = darkroomNum(plan && plan.duration) / 1000;
  var seam = [];
  var cut = [];

  cues.forEach(function (c) {
    ["in", "out"].forEach(function (side) {
      var door = c && c.doors && c.doors[side];
      var value = door ? darkroomNum(door.value) : NaN;
      if (!door || typeof door.handle !== "string" || !door.handle || value !== value) {
        seam.push("the voice «" + ((c && c.id) || "?") + "» has no " + side + " door");
      }
    });
  });
  if (!track.length) seam.push("the film carries no camera track");
  else {
    if (track[0].at !== "a") seam.push("the camera does not rest on the departing work");
    if (track[track.length - 1].at !== "b") seam.push("the camera does not rest on the arriving work");
  }

  var ground = darkroomFilmGround(plan);
  if (!ground) cut.push("no voice spans the film whole, so its head or its tail is held by nothing");

  var spans = cues.filter(function (c) { return c !== ground; })
    .map(function (c) {
      return { id: c.id, open: darkroomNum((c.window || [])[0]), close: darkroomNum((c.window || [])[1]) };
    })
    .sort(function (p, q) { return p.open - q.open; });
  for (var i = 1; i < spans.length; i++) {
    if (!(spans[i].open < spans[i - 1].close)) {
      cut.push("the voice «" + spans[i].id + "» opens only after «" + spans[i - 1].id
               + "» has already closed");
    }
  }

  var last = null;
  track.forEach(function (knot, at) {
    var t = knot.at === "a" ? 0 : (knot.at === "b" ? duration : darkroomNum(knot.at));
    if (t !== t) { cut.push("camera knot " + at + " stands at no time"); return; }
    if (t < 0 || t > duration + 0.001) cut.push("camera knot " + at + " stands outside the film");
    if (last !== null && t < last) cut.push("camera knot " + at + " stands before the knot ahead of it");
    last = t;
  });

  return { seam: { ok: seam.length === 0, faults: seam },
           cut: { ok: cut.length === 0, faults: cut } };
}

// THE FILM ITSELF. One call into the crossing skeleton — `composer.passageFor`, the same entry every
// edge of the walk comes through — from the photograph as it stands to the work as it was made, and
// the two checks run on what comes back before it is handed on.
//
// THE ROLE IS `middle` AND IT IS READ, NOT CHOSEN: Requirement 41 criterion 11 says the room runs at
// middle tier, and `ROLE_BUDGETS` (pass-composer.js:4942-4948) is the one place a role's tier is
// declared — `middle` is the role whose budget names that tier.
//
// THE DIE IS THE WORD'S OWN. The link is the work, so the same link must play the same film; the
// seed is therefore a plain reading of the word's own characters, and the composer wraps a seed
// outside its published span into it by itself.
function darkroomFilmSeed(word) {
  var h = 0;
  for (var i = 0; i < word.length; i++) h = ((h * 31) + word.charCodeAt(i)) % 2147483647;
  return h;
}

function darkroomFilm(making, records, room, composer) {
  room = room || {};
  var manifests = room.manifests || {};
  var word = darkroomWord(making, manifests);
  var from = (records || {})[String(making && making.photo)];
  // Requirement 41 criterion 35 — a link naming a photograph the collection no longer holds is not
  // an error and is never resolved to a different photograph. It is refused here, wordlessly, and
  // the room answers it in its own grammar.
  if (!from) return { word: word, refused: "the collection holds no such photograph" };
  if (!composer || typeof composer.passageFor !== "function") {
    return { word: word, refused: "no composer" };
  }
  var made = darkroomMadeRecord(from, word, room.measured);
  var envelope = composer.passageFor({
    workRecordA: from,
    workRecordB: made,
    routeRole: "middle",
    direction: "a-to-b",
    seed: darkroomFilmSeed(word),
    deviceCeiling: room.deviceCeiling || null
  });
  var plan = envelope && envelope.plan;
  if (!plan) return { word: word, refused: "the skeleton composed no passage" };
  return { word: word, plan: plan, made: made, checks: darkroomFilmChecks(plan) };
}

// THE FILM'S OWN FRAME AT ONE INSTANT, read off the compiled plan and nothing else. The making's
// travel rides the ground's own door — the handle it enters on and the value it leaves on — and the
// eye stands where the camera's own track puts it, its knots read the way the host reads them
// (pass-layer.js:1298, the applied factor is exp of `logScale`; pan is a share of the frame).
function darkroomFilmFrame(plan, seconds) {
  var duration = darkroomNum(plan && plan.duration) / 1000;
  var t = darkroomClamp(Number(seconds) || 0, 0, duration);
  var ground = darkroomFilmGround(plan);
  var travel = duration > 0 ? t / duration : 1;
  if (ground && ground.doors && ground.doors.in && ground.doors.out) {
    var from = darkroomNum(ground.doors.in.value);
    var to = darkroomNum(ground.doors.out.value);
    if (from === from && to === to) travel = from + (to - from) * (duration > 0 ? t / duration : 1);
  }
  var track = ((plan && plan.camera) || {}).track || [];
  function timeOf(k) { return k.at === "a" ? 0 : (k.at === "b" ? duration : darkroomNum(k.at)); }
  function poseOf(k) {
    return { x: darkroomNum((k.pan || {}).x) || 0, y: darkroomNum((k.pan || {}).y) || 0,
             logScale: darkroomNum(k.logScale) || 0, roll: darkroomNum(k.roll) || 0 };
  }
  var pose = { x: 0, y: 0, logScale: 0, roll: 0 };
  for (var i = 0; i < track.length; i++) {
    var t1 = timeOf(track[i]);
    if (t <= t1 || i === track.length - 1) {
      if (i === 0) { pose = poseOf(track[0]); break; }
      var t0 = timeOf(track[i - 1]);
      var f = t1 > t0 ? darkroomClamp((t - t0) / (t1 - t0), 0, 1) : 1;
      var a = poseOf(track[i - 1]), b = poseOf(track[i]);
      pose = { x: a.x + (b.x - a.x) * f, y: a.y + (b.y - a.y) * f,
               logScale: a.logScale + (b.logScale - a.logScale) * f,
               roll: a.roll + (b.roll - a.roll) * f };
      break;
    }
  }
  return { travel: travel, panX: pose.x, panY: pose.y, roll: pose.roll,
           scale: Math.exp(pose.logScale) };
}

// THE CONTACT STRIP — Requirement 41 criterion 18, «the print plus a thin contact strip of its
// making». A contact strip is what a photographer lays a sheet of exposures out as, and the
// exposures of a making are its own steps: one frame per step, each carrying the chain as it stood
// when that step landed. The strip therefore reads the chain and names no instant of its own, so a
// making of n steps hands back exactly n frames whatever the film's own length turned out to be.
// The first frame is the picture after the first step, never the bare print — the bare print is the
// card's own large frame and would be shown twice.
function darkroomStripStates(making) {
  var stood = {};
  var out = [];
  ((making || {}).chain || []).forEach(function (step) {
    var id = step && (step.instrument || step.id);
    if (!id) return;
    var handles = (step && step.handles) || {};
    var next = {};
    Object.keys(stood).forEach(function (iid) {
      next[iid] = {};
      Object.keys(stood[iid]).forEach(function (h) { next[iid][h] = stood[iid][h]; });
    });
    next[id] = next[id] || {};
    Object.keys(handles).forEach(function (h) { next[id][h] = Number(handles[h]); });
    stood = next;
    out.push(next);
  });
  return out;
}
