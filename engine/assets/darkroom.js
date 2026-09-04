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
