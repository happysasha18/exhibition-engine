/*!pass-composer.js*/
// The passage composer's choice core, in the browser — PASS-API-V1 §4.7 composed at show time.
//
// ROOT. His law of 2026-08-14 16:14 and his word of 2026-08-17 17:06: a pair's crossing is
// decided when the pair is shown, and the product carries no table of pairs. The site's
// lab/build-sceneplan-v1.py already holds the whole decision — the pivot, the travelling axis,
// the actors, the arrival, the voices, the levels, the camera and the two doors — and it holds it
// in stdlib arithmetic over records that describe ONE work each. This file is that decision,
// carried across a line: two per-work records and a seed in, the §4.4 score out.
//
// THE BYTE-PARITY CLAIM AGAINST lab/sceneplan-to-score.py WAS RETIRED 2026-08-19: that reference
// belongs to the table-based build the architecture decision of 2026-08-14 16:14 and his word of
// 2026-08-17 17:06 (above) replaced, and no live gate ever enforced the match.
//
// WHAT IT MEASURES: nothing. Every number that describes a WORK was measured once, per work, and
// written down. It opens no image and asks no network. The pair step is arithmetic over the two
// records, which is why it can run at the instant a walk casts the pair.
//
// THE ONE LIVE READ (charter shelf 16's day's-weather-bias step, added 2026-08-24): `weatherNow`,
// below, reads the real clock at the instant a ground is rolled — the day and the hour, and nothing
// else about the machine it runs on. Nothing it reads is stored, cached across a call, or seeded
// from anything prepared ahead of the visit (shelf 21); it is a session-time input exactly as the
// seed and the visit's own memory are, not a measurement of the collection.
//
// WHAT IT IS HANDED. `make(consts)` takes the facts that belong to the collection rather than to
// one work: the three instrument manifests as their own files publish them, the cut-line floors,
// the discriminating thresholds the shared measure is read against, the client's score fence and
// the provenance sentence the record carries. Nothing about an instrument is written down here —
// the manifest is the instrument's own home for it, and a copy of a number that lives somewhere
// else is a copy that goes stale.
//
// WHY THE NUMBERS ARE PRINTED BY HAND. The score travels as JSON and the equality this file is
// held to is BYTE equality against Python's own `json.dumps(score, ensure_ascii=False, indent=1,
// sort_keys=True)`. Two languages print numbers differently in exactly three places — an integral
// float, a negative zero, and the fourth decimal of a rounded value — so this file carries
// Python's own rules for all three: `flt` marks a value Python holds as a float, `r4` rounds the
// way Python's own `round` does, half to even on the exact binary value, and `writeJson` writes
// the object the way Python writes it.
//
// WHERE IT STANDS ON THE PRODUCT PATH (U27 stage 0, the seam). It travels as its own fetched file
// the way pass-layer.js and the instruments do, opened once per visit at the walk's first landing,
// and `passageFor` at the foot of this file is the ONE entry every edge of the walk comes through.
// The prebaked per-pair score pack it replaces is gone from the walk, with the reader that fetched
// it and the site steps that staged it.
//
// WHAT IT DOES NOT DO. It measures nothing, and it holds no door: the meshing instrument reads its
// own doors at run time on the buffer it is drawing on, and this file emits the artistic request
// (his architecture decision of 2026-08-17 18:00).
(function () {
  var join = window.__@@NS@@PassComposer;
  if (typeof join !== "function") return;

  // THIS FILE'S OWN VERSION, and the one home of that fact. It travels onto the diagnostic
  // surface with every score this file composes, so a score and the core that chose it can be
  // read together.
  var COMPOSER_VERSION = "1";

  // ---------------------------------------------------------------------------------------
  // Python's own numbers: a float that knows it is one, its printing, and its rounding.
  // ---------------------------------------------------------------------------------------

  // A value Python holds as a float. JavaScript has one number type and Python has two, and the
  // difference shows in one character: Python writes 1.0 where JavaScript writes 1. So a value the
  // Python composer holds as a float is marked here, and everything else is an integer.
  function Flt(v) { this.v = v; }
  Flt.prototype.valueOf = function () { return this.v; };
  function flt(v) { return new Flt(v); }
  function isFlt(v) { return v instanceof Flt; }
  function num(v) { return isFlt(v) ? v.v : v; }

  // A number as Python prints it: an integer where the value is whole and the composition holds
  // it as one, a float otherwise, with the negative zero Python keeps and JavaScript drops.
  function floatText(x) {
    if (x !== x) return "NaN";
    if (x === Infinity) return "Infinity";
    if (x === -Infinity) return "-Infinity";
    var s = String(x);
    if (Object.is(x, -0)) return "-0.0";
    // JavaScript writes an exponent from 1e-7 down and Python from 1e-5 down; a rounded number of
    // this composition never stands there, and where one does it is written Python's way.
    if (s.indexOf("e") >= 0) {
      var at = s.indexOf("e"), mant = s.slice(0, at), exp = s.slice(at + 1);
      var sign = exp.charAt(0) === "-" ? "-" : "+";
      var digits = exp.replace(/^[+-]/, "");
      if (digits.length < 2) digits = "0" + digits;
      if (mant.indexOf(".") < 0) mant += ".0";
      return mant + "e" + sign + digits;
    }
    if (s.indexOf(".") < 0) return s + ".0";
    return s;
  }

  function pyText(v) {
    if (isFlt(v)) return floatText(v.v);
    if (typeof v === "number") return Number.isInteger(v) ? String(v) : floatText(v);
    if (Array.isArray(v)) {
      var parts = [], i;
      for (i = 0; i < v.length; i++) parts.push(pyText(v[i]));
      return "[" + parts.join(", ") + "]";
    }
    if (v === null || v === undefined) return "None";
    return String(v);
  }

  // Python's own `round(x, 4)`: half to even, decided on the double's exact value rather than on
  // the shortest decimal that stands for it. `toFixed` gives that exact value far enough out for
  // a tie to be visible, since a tie at four places is a dyadic number with five decimals.
  function roundHalfEven(x, places) {
    if (!isFinite(x)) return x;
    var neg = x < 0 || Object.is(x, -0);
    var s = Math.abs(x).toFixed(Math.min(20, places + 16));
    var dot = s.indexOf("."), digits = s.replace(".", "");
    var cut = dot + places;                       // digits kept, before the deciding one
    var head = digits.slice(0, cut), tail = digits.slice(cut);
    var keep = head === "" ? 0 : parseInt(head, 10);
    var first = tail.charAt(0);
    var rest = tail.slice(1).replace(/0+$/, "");
    var up = false;
    if (first > "5") up = true;
    else if (first === "5") up = rest.length > 0 ? true : (keep % 2 === 1);
    if (up) keep += 1;
    var out = keep / Math.pow(10, places);
    // The division above is one rounding step, and reading the decimal back is what Python does.
    out = parseFloat((keep / Math.pow(10, places)).toFixed(places));
    return neg ? -out : out;
  }

  function r4(x) { return roundHalfEven(Number(num(x)) + 0.0, 4); }

  // Python's `round(x)` to a whole number, half to even.
  function roundToInt(x) {
    var f = Math.floor(x), d = x - f;
    if (d > 0.5) return f + 1;
    if (d < 0.5) return f;
    return f % 2 === 0 ? f : f + 1;
  }

  // ---------------------------------------------------------------------------------------
  // Python's own JSON: sorted keys, one space of indent, unicode written as itself.
  // ---------------------------------------------------------------------------------------

  // CAPABILITY — JSON's own escape table. The format says which code points must be written which
  // way, and nothing here is a choice: a different table would write invalid JSON.
  var ESCAPES = { 8: "\\b", 9: "\\t", 10: "\\n", 12: "\\f", 13: "\\r", 34: "\\\"", 92: "\\\\" };

  function jsonString(s) {
    var out = "\"", i, c, code;
    for (i = 0; i < s.length; i++) {
      c = s.charAt(i);
      code = s.charCodeAt(i);
      if (ESCAPES[code] !== undefined) out += ESCAPES[code];
      else if (code < 0x20) out += "\\u" + ("000" + code.toString(16)).slice(-4);
      else out += c;
    }
    return out + "\"";
  }

  function jsonNumber(v) {
    if (isFlt(v)) return floatText(v.v);
    if (Number.isInteger(v)) return String(v);
    // A bare non-integral number reaching the writer is a value the port forgot to mark, and a
    // silent guess about how Python holds it would be exactly the drift this file is proving
    // absent. It is named instead.
    throw new Error("pass-composer: an unmarked non-integral number reached the writer: " + v);
  }

  function writeJson(value, indent) {
    var pad = new Array(indent + 1).join(" ");
    var padIn = new Array(indent + 2).join(" ");
    var i, keys, parts;
    if (value === null || value === undefined) return "null";
    if (value === true) return "true";
    if (value === false) return "false";
    if (isFlt(value) || typeof value === "number") return jsonNumber(value);
    if (typeof value === "string") return jsonString(value);
    if (Array.isArray(value)) {
      if (!value.length) return "[]";
      parts = [];
      for (i = 0; i < value.length; i++) parts.push(padIn + writeJson(value[i], indent + 1));
      return "[\n" + parts.join(",\n") + "\n" + pad + "]";
    }
    keys = Object.keys(value).sort();
    if (!keys.length) return "{}";
    parts = [];
    for (i = 0; i < keys.length; i++) {
      parts.push(padIn + jsonString(keys[i]) + ": " + writeJson(value[keys[i]], indent + 1));
    }
    return "{\n" + parts.join(",\n") + "\n" + pad + "}";
  }

  // The weight `passScoreCheck` measures: the same object with no space in it at all.
  function writeJsonTight(value) {
    var i, keys, parts;
    if (value === null || value === undefined) return "null";
    if (value === true) return "true";
    if (value === false) return "false";
    if (isFlt(value) || typeof value === "number") return jsonNumber(value);
    if (typeof value === "string") return jsonString(value);
    if (Array.isArray(value)) {
      parts = [];
      for (i = 0; i < value.length; i++) parts.push(writeJsonTight(value[i]));
      return "[" + parts.join(",") + "]";
    }
    keys = Object.keys(value);
    parts = [];
    for (i = 0; i < keys.length; i++) {
      parts.push(jsonString(keys[i]) + ":" + writeJsonTight(value[keys[i]]));
    }
    return "{" + parts.join(",") + "}";
  }

  function copy(value) {
    var i, out, keys;
    if (value === null || value === undefined) return value;
    if (isFlt(value)) return flt(value.v);
    if (typeof value !== "object") return value;
    if (Array.isArray(value)) {
      out = [];
      for (i = 0; i < value.length; i++) out.push(copy(value[i]));
      return out;
    }
    out = {};
    keys = Object.keys(value);
    for (i = 0; i < keys.length; i++) out[keys[i]] = copy(value[keys[i]]);
    return out;
  }

  // ---------------------------------------------------------------------------------------
  // The composer's own vocabulary, carried from lab/build-sceneplan-v1.py word for word.
  // ---------------------------------------------------------------------------------------

  // CAPABILITY — the score's own wire format version (§4.4a). Two schemas live at once and this
  // names which one this module writes; the number belongs to the format, not to any pair.
  var SCHEMA = 1;
  var CUE_IDS = ["pivot", "travel", "arrival"];
  var TRAVEL_AXES = ["banding", "dominant_object", "grid", "radial", "regions", "texture"];
  var LOCUS_KINDS = ["none", "pole", "horizon-seam", "gate"];
  // `PINNED_LEVELS` STOOD HERE AND IS RETIRED. It named the levels a cue could stand on without
  // owning them, because on those levels this composer actually held a non-owner's handles at the
  // instrument's own rest instead of merely saying it did. It held one entry, LIGHT-COLOUR, and one
  // gate behind it. Every level has that gate now: each handle declares in its own instrument's
  // manifest which structural level it drives, and `buildTemplate` takes the handles of an unowned
  // level off the cue's track list, so a non-owner rests there and plays on where it owns. A list of
  // the gated levels is now a list of all six, and `castForKinds` reads no such list.
  //
  // The six are shelf 17's own and there is no seventh: WORLD, SURFACE, CELL, CELL CONTENT,
  // TEXTURE, LIGHT-COLOUR (docs/design/PASS-API-V1.md:716).
  var LEVELS = ["WORLD", "SURFACE", "CELL", "CELL CONTENT", "TEXTURE", "LIGHT-COLOUR"];
  var WORLDS = ["sphere", "corridor", "log-spiral"];
  var POLAR_WORLD = { planet: "sphere", tunnel: "corridor", twirl: "log-spiral" };
  var SUBTYPES = ["angular", "ring", "none"];
  var REGISTERS = ["none", "discovery", "provocation", "apparition"];
  var PIVOT_KINDS = ["shared-measure", "shared-rotational-order", "shared-palette-region",
                     "tonal-and-spectral"];
  var MEASURES = ["banding", "grid", "regions", "dominant_object", "texture", "radial",
                  "named_objects"];
  // `SHARED_MEASURES` stood beside `MEASURES` here until 2026-08-24 — the same seven names in
  // another order, read by nothing in this file or in any file of either tree. A second list of one
  // fact is a list that can go stale against the first, and this one already had: nothing would have
  // said so.
  var CUT_OF_MEASURE = {
    regions: ["regions", "region_dissolve"],
    named_objects: ["named_boxes", "object_by_object"],
    texture: ["grain", "grain_wipe"],
    banding: ["bands", "band_slide"],
    radial: ["rings_or_spokes", "radial_unfold"],
    dominant_object: ["figure_ground", "object_reveal"],
    grid: ["tiles", "tile_crossfade"]
  };
  var KIND_OF_MEASURE = {
    regions: "panel", named_objects: "region", texture: "scale", banding: "strip",
    radial: "ring", dominant_object: "panel", grid: "tile"
  };
  // The three pivots that are not a shared measure carry their cut, transform and element kinds on
  // the pivot's own shape rather than on the pair. `elementKinds` is the whole list, and every
  // pivot carries one — a table of exceptions stood beside these three rows naming the kinds ONE of
  // them cut on, and because `compose` read the single `elementKind` and not the table, half of
  // that pivot's own cut was unreachable by any instrument: nothing refused, nothing errored, and a
  // whole way of crossing simply never got walked while every suite stayed green. There is no
  // exception table now; the shape says what it cuts and the casting asks the shape.
  var PIVOT_SHAPES = {
    "shared-rotational-order": { cut: "wedges", transform: "gear_mesh", elementKind: "wedge",
                                 elementKinds: ["wedge"] },
    "shared-palette-region": { cut: "colour_world", transform: "palette_handover",
                               elementKind: "band", elementKinds: ["band"] },
    // THE TONAL ZONES AND THE DETAIL SCALES. Two decompositions that apply to any two photographs by
    // construction — the highlights leaving before the shadows, and the arriving work's blurred mass
    // growing first with its detail growing into it — so this pivot reads on every pair and cuts on
    // both a band and a scale.
    //
    // IT IS NOT A BRIDGE AND IT IS NOT A FALLBACK, on his word of 2026-08-18 10:15: «я не просил
    // запасную дорогу, логика построена так что дорога всегда сработает». It was reached only after
    // every other ground had turned a pair away, and a candidate reachable only after every rival
    // has refused is selected by those refusals and not by its own fit — a fact about the control
    // flow, true whatever pool it stands in. They were not choosing it, they were pushed. It is now a
    // candidate like the rest, ranked on its own reading of the pair, reached by the same code path
    // as every other, and it wins where it suits the pair better than the others do.
    "tonal-and-spectral": { cut: "tonal_zones_and_detail_scales",
                            transform: "zone_handover_and_scale_growth",
                            elementKind: "band", elementKinds: ["band", "scale"] }
  };
  // WHICH INSTRUMENTS CUT ON WHICH ELEMENT KIND — read off the collection's own record, never
  // written down here. Every instrument the settings record publishes names the cuts it plays in
  // its own entry, so the map from a kind to the instruments that can cut it is derived in `make`
  // below and a landing instrument joins the candidates by arriving.
  //
  // WHAT THIS REPLACES, AND WHY IT WAS A DEFECT. A table here named ONE instrument per kind. The
  // folding instrument landed on the panel kind and the unfold, which had cut on panels all along,
  // was silently retired — it travelled to every visitor and could never be chosen. That contradicts
  // three of his words at once: the arsenal stays full so the options in hand are always plentiful
  // (18:56); process is a register of its own, and the unfold is the only instrument that shows a
  // person how a work was made (19:13); and a full route displays the vocabulary's breadth, with one
  // lovely move standing alone recorded as a failure (19:13). A rule under which a landing
  // instrument retires an existing one would have done it again at the next arrival, so the rule is
  // what is repaired rather than the one pair of instruments it happened to catch.
  //
  // WHERE SEVERAL CUT ON ONE KIND the choice is made the way the genres are chosen: every published
  // instrument says how well it suits THIS pair, on its own terms, and the die runs over those
  // readings. The two panel instruments are genuinely different acts and their readings say so —
  // folding into a solid is an impossible event that claims the world, while opening into a parquet
  // reveals the making and claims no world at all.
  //
  // NO KIND IS EVER WITHOUT AN INSTRUMENT. A table stood here naming, for four element kinds, the
  // instrument this collection has not got, and the composer answered a pair whose ground cut on one
  // of them with «pivot needs an instrument that cuts on tiles» — no crossing at all. His word of
  // 2026-08-18 09:51 strikes that whole idea out: any two photographs in the world get a crossing,
  // and a measurement only ranks which genre suits and shapes it once chosen. So a kind no
  // instrument cuts is not a refusal; the instruments that DO cut it rank first, and where there are
  // none the best-suited instrument in the collection plays the pair on its own cut and the plan
  // says which cut it wanted and which it got.
  var KIND_OF_AXIS = { banding: "strip", radial: "ring", regions: "panel", grid: "tile",
                       texture: "scale", dominant_object: "panel" };
  var TIERS = [
    // A `duration` stood on each of these three rows — 3000, 6500 and 11000 — and the composition
    // read one of them straight off, so every plan that realised a tier ran the same number of
    // milliseconds whatever pair it was made of. Shelf 17 gives each tier a BAND of seconds, not a
    // number — 2 to 4 at a quiet one, 5 to 8 at a middle, 9 to 14 at a culmination — and the band is
    // what stands here now; the pair's own reading places the length inside it (`compose`).
    { tier: "quiet", letters: [1, 1], accompaniments: [0, 1], miracles: [0, 0],
      band: [2000, 4000] },
    { tier: "middle", letters: [0, 2], accompaniments: [0, 2], miracles: [0, 1],
      band: [5000, 8000] },
    { tier: "culmination", letters: [2, 3], accompaniments: [0, 3], miracles: [1, 1],
      band: [9000, 14000] }
  ];
  // DERIVED — the three tiers in their own order, so a role can be asked whether a realised tier
  // reaches it. It reads `TIERS` above rather than restating it, so a row added, removed or
  // reordered there carries this with it and no second copy of shelf 17's ladder can go stale.
  var TIER_RANK = (function () {
    var out = {}, i;
    for (i = 0; i < TIERS.length; i++) out[TIERS[i].tier] = i;
    return out;
  }());
  // DERIVED — the transaction's own ceiling, which is the top of shelf 17's longest band: a
  // culmination runs nine to fourteen seconds and the transaction ends where the longest crossing
  // does. It stood here as a typed 14000, a third copy of one number that also lives in `TIERS`
  // above and in `pass-layer.js`'s own §2.5 range, and three copies of one fact drift. Read from the
  // table, so a change to the charter's own bands carries the ceiling with it. `pass-layer.js`'s
  // `DURATION_MAX` is the third copy and stays a literal on purpose: it is on the other side of the
  // line and the layer must enforce §2.5 whatever the composer thinks.
  var TRANSACTION_MS = (function () {
    var top = 0, i;
    for (i = 0; i < TIERS.length; i++) if (TIERS[i].band[1] > top) top = TIERS[i].band[1];
    return top;
  }());
  // How far the camera may come in or pull back on the score's own track, as a natural logarithm:
  // 0.5 bounds the approach at 1.65 times, and it bounds a magnification of the RENDERED canvas,
  // because the host applies the dolly as one transform over the buffer the instrument drew on.
  // Since 2026-08-17 it is a LIMIT the demand is compressed toward rather than a wall it is cut at;
  // `cameraFlight` below carries that and the measurement behind it.
  //
  // THE NUMBER IS UNMEASURED AND IT IS ON HIS LIST FOR GATE 1 (U27 stage 1, the camera lane,
  // 2026-08-17 22:2x). It was written when this field held a base-2 logarithm, so it bounded the
  // approach at 1.41 times and now bounds it at 1.65. No number here can be the honest bound, and
  // the argument for that is a construction one: what the door framings ASK for is the logarithm of
  // a ratio of two framings, which runs the whole real line and is bounded above by nothing at all,
  // so no cap on it can be read off anything the composer holds. What the FRAME can carry is
  // bounded, and by something else entirely: the buffer's own oversampling, min(dpr, 2) times the
  // resolution step, which is 1.00 times on any dpr-1 frame and falls to 1.00 on a dpr-2 phone at
  // the governor's floor. The bound is therefore a property of the device the composer cannot see
  // (his architecture decision of 18:00). The defect the composer lane found belongs to the CLIPPING
  // rather than to this value: a clamp is constant on the whole half-line above its bound, so it
  // destroys the ordering there for every input whatever, and the approach carries no reading of any
  // pair on any of them. The report names the repair; nothing is guessed here in the meantime.
  //
  // UNJUSTIFIED. Everything above argues the SHAPE — that a bound belongs to the device rather than
  // to any pair, and that a limit is the right form for it — and none of it derives this value. The
  // half was chosen by this seat. What it has to satisfy is only that it be positive, so the limit
  // holds and the map stays monotone; every positive value satisfies that equally, and the number
  // that would be right is a property of the buffer the composer cannot see.
  var DOLLY_CAP = 0.5;
  // WHAT LEFT THIS BLOCK ON 2026-08-18, and it is one sweep rather than eight repairs. His word of
  // 09:57: a number this project computed and gave a name to, with no requirement of his behind it,
  // goes as well — «убирай тоже как класс». Eight named numbers stood here and every one of them
  // was this seat's own invention wearing the clothes of a measurement:
  //
  //   LEAD_SHARE 0.1          how far a flight had to travel before it could carry a passage. The
  //                           plan itself already says it: a passage with no travelling and no
  //                           arriving cue has nothing BUT the camera to be the transition, and
  //                           that reading needs no number at all.
  //   SIZE_FLOOR 0.7          the size the meshing picture stopped reading at. That is a fact about
  //                           the meshing instrument, and the instrument publishes it — its `size`
  //                           handle's own minimum, read from the manifest at the moment it is
  //                           needed rather than copied here.
  //   CULMINATION_DISTANCE .5 how far two axes had to stand apart for a crossing to be a
  //                           culmination. The step's ROLE says whether it is one; the distance only
  //                           guessed, and the guess overrode the walk.
  //   LOCUS_NEAR 0.1          how close a figure had to stand to a locus. The figure carries its own
  //                           measured box, so the question is whether the locus falls inside it.
  //   VOID_SHARE_FLOOR 0.6    the open ground an apparition asked for.
  //   LADDER_DISTANCE 0.5     the tonal gap a provocation asked for. Both are now what they always
  //   READY_FLOOR 0.12        should have been: readings that RANK the registers against each other.
  //                           the readiness a pair had to clear before it counted at all — a floor
  //                           whose only act was to write a real reading down to zero.
  //   DOOR_HOLD 0.08          the share of a passage held at its doors. It reached no field of any
  //                           score, so it decided nothing and was carried on the plan for nobody.
  //
  // The ten typed floors and the seven discriminating thresholds the collection's record carried
  // went with them, and `make` below says why.
  var MOTIF_SEAM = "горизонт-шов";
  var MOTIF_GATE = "ворота";

  // A ROW RECORDS WHAT A HANDLE READS, so one reading is one row and two readings are two rows.
  //
  // The plain keys below are shared readings: every instrument that drives that handle reads that
  // measurement, and one row serves them all. That is the `twist` case — the glass winds by it, the
  // kaleidoscope leans its fold by it and the corridor shears its spiral by it, three acts of one
  // reading, and renaming any of them would put a second name on one measurement.
  //
  // A key of the shape `instrument.handle` is the OTHER case, and it is a real one: two instruments
  // publish one name for two different measurements. Before 2026-08-18 this table was keyed by
  // handle name alone, so the second instrument to publish a name inherited the first one's reading
  // — the gates port found its own `lead` about to be driven by the folding instrument's finger
  // count, which is a wrong parameter reaching the picture while every row looks answered, and that
  // is worse than a handle standing at its rest. `sourceOf` reads the scoped row first and falls
  // back to the shared one, so a name that means one thing everywhere still costs one row.
  //
  // NOTHING IS RENAMED TO FIT THIS TABLE. A module's own handle name is the module's, and bending
  // it to a table's shape is the invention his 08:47 word strikes; the table takes the instrument's
  // name instead.
  // THE FIRST WORD OF A ROW SAYS WHERE THE NUMBER COMES FROM, and the node writer dispatches on it
  // rather than on the handle's name. There are six words and each has exactly one road:
  //
  //   · `measured`    — read off the two works' own records. The composition owes a value; a handle
  //                     of this kind that reaches the writer with none is a broken promise, and the
  //                     writer says so rather than freezing it at the manifest default in silence.
  //   · `progress`    — the passage's own travel, door to door. It rides `cueProgress`.
  //   · `host-clock`  — the second the host hands down.
  //   · `plan`        — a value of neither photograph that the PLAN names: shelf 7's interfered
  //                     arrival, and which of his six approved meeting rules two works meet under.
  //                     The composition owes a value here too, for the same reason.
  //   · `unmeasured`  — nothing in a work record carries it. Resting at the instrument's own default
  //                     is the honest answer and the plan says so in its own sentence.
  //   · `module-rest` — a judge channel the module rests at. Resting is what it is for.
  //
  // `transaction` STOOD WHERE FOUR OF THESE NOW DO, and one word covering four sources is what let
  // the defect live: the writer could not dispatch on it, so it dispatched on the handle's NAME
  // instead — `mix` and `clock` by name, and every other transaction handle fell through to the
  // static branch and held still at its default for the whole passage. A row promising the
  // passage's own travel and a node that never moves is the sharpest form of it, and it reached
  // `parquet.spin`, `unfold.field`, `overlay.blend` and the interfered `arrival` of two
  // instruments. The word is split so that what a row promises and what the writer does are the
  // same fact read once.
  var HANDLE_SOURCE = {
    mix: ["progress", "the pass's own progress, door to door"],
    clock: ["host-clock", "the second the host hands down"],
    seed: ["measured", "the ordered pair's own seed"],
    strips: ["measured", "the pivot's band family, its measured count along the cut"],
    // WIDENED 2026-08-17 for the box: for the woven instrument `axis` is which way the ribbons run,
    // for the folding one it is which way the solid turns — the crease upright or lying flat. Both
    // derive from the one recorded banding axis, so the crease crosses the works' own structure
    // rather than being laid across it, and one row serves both because one measurement does.
    // WIDENED AGAIN 2026-08-18 for the mirror: one measurement, three senses. For the woven
    // instrument it is which way the ribbons run, for the folding one which way the solid turns so
    // its crease CROSSES that structure, and for the mirroring one which way the picture folds onto
    // itself — where the fold lies ALONG the structure rather than across it. Three acts, one
    // recorded axis, so one row and not three names.
    axis: ["measured", "the banding axis cut-lines.json recorded — which way the ribbons run, "
                       + "which way the solid turns so its crease crosses that, and which way the "
                       + "picture folds onto itself so the fold line lies along it"],
    size: ["measured", "the two works' measured ring counts"],
    ratio: ["measured", "the two works' measured ring counts, on seven steps"],
    bandPeriod: ["measured", "the pivot's own period as a fraction of frame height"],
    centreX: ["measured", "the midpoint of the two measured radial centres"],
    centreY: ["measured", "the midpoint of the two measured radial centres"],
    shade: ["module-rest", "a judge channel the module rests at 1"],
    travel: ["module-rest", "a judge channel the module rests at 1"],
    glint: ["module-rest", "a judge channel the mirror rests at its own 0.62, the brightness of "
                           + "the fold line"],
    curl: ["measured", "each work's own reading as a little world, structure.polar.planet — a "
                       + "picture that already turns about a centre closes the whole way and one "
                       + "that barely does is left a bowed band"],
    // THE INTERFERING INSTRUMENT'S NINE, and the four lattice rows are charter shelf 10's own
    // reading: the third picture is the two works' interference, so what sets how near the two
    // rhythms stand has to be the two rhythms themselves. Each row takes the sentence the handle
    // publishes on the instrument, which is the fact the instrument owns.
    // THE MIRROR FLOOR'S OWN THREE, and its `depth` is the row widened above. `mix`, `seed`,
    // `shade` and `mask` already carried rows of the shapes the other instruments use.
    tiles: ["measured", "the work's own frame side over structure.grid.periodPx, the count of its "
                        + "own measured lattice across it; the same off structure.ownDevice.stepPx "
                        + "where no grid period was derived. The grid is named FIRST here and the "
                        + "device second, the other way round from the unfold's parquet, and the "
                        + "reason is measured: the grid period spreads the collection over all five "
                        + "counts while the device step saturates at the range's own top on five "
                        + "works in six, so a floor laid from the device would be one floor"],
    lattice: ["measured", "structure.grid.angleDeg, the direction the work's own lattice varies "
                          + "along; structure.ownDevice.angleDeg where no grid angle was derived"],
    // THE FLOOR'S OWN SLOW TURN, which reads no photograph and says so. It is not «unmeasured» —
    // there is nothing to measure. The module turns its floor on a clock at the vista preset's own
    // taste-approved rate of 2026-08-08, and this engine hands an instrument no clock, so the rate
    // is carried at the engine's own pass duration and rides the dial. That is the passage's own
    // travel, the same tag the plane and the parquet's envelope already stand under.
    spin: ["progress", "the passage's own travel: the module's own floor turn at the vista "
                          + "preset's approved rate, carried at this engine's pass duration "
                          + "because an instrument is handed no clock"],
    // THE READY STORY'S OWN FOUR. Its other five — mix, clock, centreX, centreY, turn, mask — were
    // already named, and `turn` reads the radial score here for the same reason the mesh's does.
    folds: ["measured", "the order of the pair's own measured turn, structure.rotational.n, read "
                        + "onto the module's ladder of two, four, eight and sixteen wedges"],
    foldsScore: ["measured", "structure.rotational.score, the confidence that order reads at, which "
                             + "carries the window between the module's own four folds and the "
                             + "pair's own count"],
    planet: ["measured", "structure.polar.planet, how strongly the pair's works read as a planet, "
                         + "which places the far end of the arc"],
    course: ["measured", "structure.ownDevice.stepPx over the work's own frame side where that "
                         + "device is rings — the step the work was cut at"],
    // THE WATER'S OWN THREE. Every other handle it publishes — mix, clock, seed, shade, travel,
    // mask — was already named.
    swell: ["measured", "texture.scoreFromCutLines, how much of the work reads as grain rather "
                        + "than as line"],
    crest: ["measured", "texture.spectralPeriodPx over the work's own frame side, read as a "
                        + "position on the handle's own range"],
    refract: ["measured", "texture.detailPx over the work's own frame side, read as a position on "
                          + "the handle's own range"],
    exposure: ["measured", "how far the composite reaches, positioned by the two works' own colour "
                           + "distance: two palettes standing apart make a third colour world "
                           + "worth reaching for, two standing close make one work slightly "
                           + "veiled"],
    // THE COMPOSITE'S OWN REGION SHARE, SCOPED TO THE INSTRUMENT THAT MEANS IT. This row is
    // `overlay`'s and nobody else's: on that instrument `presence` is the share of the frame the
    // exposure stands on, a LIGHT-COLOUR reading of the pair. Since the entry-door contract landed
    // (2026-08-25) the bare name means something else across the rest of the fleet — the reserved
    // dry, below — so this row is scoped exactly as `axis` and `weave.depth` were scoped before it:
    // one name, two senses, and `sourceOf` reads the scoped row first.
    "overlay.presence": ["measured", "the share of the frame the composite stands on, read off the "
                                     + "same colour distance the exposure is placed by"],
    // THE ENTRY DOOR'S RESERVED DRY, and it takes a word of its own rather than borrowing one.
    //
    // WHY NOT `progress`. That word promises the passage's own travel across a handle's published
    // span, and the writer keeps that promise literally: it maps `smooth(cueProgress)` from the
    // handle's floor to its ceiling, a monotone rise. The dry owes the opposite shape — nothing at
    // the cue's own two doors and whole across its middle — so a `progress` row would promise one
    // journey and the writer would have to dispatch on the handle's NAME to write another. That is
    // exactly the defect the paragraph above this register records: `transaction` covered four
    // sources at once, the writer could not dispatch on it, so it dispatched on names instead. The
    // word is what the writer reads; a different shape earns a different word.
    //
    // WHY IT IS NOT `plan` EITHER. `plan` names a choice a score is free to make — the blend rule,
    // the interfered arrival. This is not free: the contract fixes it. An upper voice's dry is
    // nothing at both of its doors and whole between, and the lowest voice's is whole throughout,
    // and which of the two a cue owes is decided by where it stands in its own stack and by nothing
    // else. It is a law being stated, not a taste being exercised.
    presence: ["entry-door", "the entry-door contract's reserved dry: nothing at the cue's own two "
                             + "doors, whole across its middle, so a voice joins a running picture "
                             + "without replacing it and stands down the same way. The lowest voice "
                             + "of a stack owes the opposite and stands whole throughout, because "
                             + "nothing stands beneath it"],
    // TWO HANDLES THAT READ NOTHING OF EITHER PHOTOGRAPH AND SAY SO. They are not «uncalibrated»
    // and they are not unmeasured: there is no measurement to take, because the choice is his and a
    // score's. They stand under the same tag as the passage's own travel envelope — what the
    // transaction itself supplies — and the class law holds, because a handle naming a score's word
    // is a handle naming what it reads.
    blend: ["plan", "nothing of either photograph: the six rules the two works meet under are his "
                    + "own approved list of 2026-08-08 11:39 and the choice between them is a "
                    + "score's word"],
    arrival: ["plan", "nothing of either photograph: charter shelf 7 names the five arrivals — the "
                      + "interfered one the overlay and the grid-and-colour cut carry, the "
                      + "crystallized one the pour's own column order carries — and a score names "
                      + "which of them this crossing makes, so this is a plan's word"],
    scale: ["measured", "the ratio of the two works' own cutting steps — structure.ownDevice.stepPx "
                        + "of the arriving work over the departing one's, with "
                        + "structure.grid.periodPx where no device was derived"],
    mixPeriod: ["measured", "structure.ownDevice.stepPx over the departing work's own frame side, "
                            + "so the field deciding which places lean to which work leans along "
                            + "that work's own structure; structure.grid.periodPx where no device "
                            + "was derived"],
    mixTurn: ["measured", "structure.ownDevice.angleDeg of the departing work, the angle that same "
                          + "step was cut at; structure.grid.angleDeg where no device was derived"],
    regionPeriod: ["measured", "structure.ownDevice.stepPx over the ARRIVING work's own frame side, "
                               + "so the exposure's region grows along the structure of the work it "
                               + "is resolving into; structure.grid.periodPx where none"],
    regionTurn: ["measured", "structure.ownDevice.angleDeg of the arriving work; "
                             + "structure.grid.angleDeg where no device was derived"],
    // THE GEOMETRY-FROM-THE-WORK SWEEP, 2026-08-17 (U27 stage 1, lane A). His 19:13 word lifted to
    // the class at 19:21: every geometric and temporal parameter derives from the work's own
    // measured structure and names the measurement it reads. Nine handles that stood here as
    // «uncalibrated» or «unmeasured» now name theirs; the two that still do not say why, and the
    // two above are the module's own resting channels rather than parameters of the work.
    grain: ["measured", "the two works' own measured spectral periods, said in cells across the "
                        + "frame's height, positioned about the handle's default by their ratio"],
    order: ["measured", "the golden-angle stagger of the work's own measured ring count, charter "
                        + "shelf 13's stagger instrument on the radial time axis"],
    gather: ["measured", "the share of the frame each work's own measured dominant object holds"],
    loosen: ["measured", "the share of the frame each work's own measured open ground holds"],
    nMul: ["measured", "the ratio of the two works' measured strip counts, so the fabric's count "
                       + "travels from the departing family to the arriving one"],
    // WIDENED 2026-08-18 for the spiral: one row serves both because one construction does. For the
    // woven instrument the count is of strips and for the spiralling one of copies, and in both the
    // reading is the same — the count this pair asks for against the count the instrument rests at,
    // so one unit of the pattern passes the eye in the same time whatever the pair.
    speed: ["measured", "the pattern's own count — strips for the fabric, copies for the spiral — "
                        + "against the instrument's own default count, so one unit of the pattern "
                        + "crosses its own width in the same time whatever the pair"],
    // THE MIRROR'S OWN LIFE IS NOT DRIVEN, AND THAT IS A RECORDED VERDICT RATHER THAN A GAP. The
    // reading this row named is real and the record carries it, but `fillPlan`'s own note beside the
    // live-mirror branch states the decision plainly: the handle rests at nothing because a
    // wandering fold line does not land on the work's own structural line, and a reading may not
    // overrule that verdict on the effect. A row saying `measured` beside a decision not to drive it
    // is the register contradicting the code, and the register is what was wrong: the handle rests
    // on purpose, so the row says so and the plan carries the sentence.
    drift: ["unmeasured", "the fractional part of the two works' measured spectral periods in ratio "
                          + "is the reading, and it is deliberately not driven: a wandering fold "
                          + "line does not land on the work's own structural line"],
    tooth: ["measured", "how much finer each work's measured ring repeat is than the cut it was "
                        + "given, which is the relief a tooth stands in"],
    // WIDENED 2026-08-18 for the spiral, on the same one measurement: for the meshing instrument the
    // radial score drives how hard the mesh turns, for the spiralling one how hard the picture winds
    // into its throat per e-fold. A work whose rings are its own device turns and winds hard; one
    // that barely reads radial barely does either.
    turn: ["measured", "each work's own measured radial score, so a work whose rings are its own "
                       + "device drives the turn — the mesh's rotation and the spiral's wind — and "
                       + "one that barely reads radial barely turns and barely winds"],
    press: ["unmeasured", "the hand's own pressure, which no build-time file measures"],
    // THE FOLDING INSTRUMENT'S OWN SEVEN, checked against the class law here rather than carried
    // over as they were handed. His 19:13 word lifted to the class at 19:21: a handle that cannot
    // name a measurement is a FINDING, not a constant. Three that arrived as «unmeasured» name one
    // after all — `depth` reads how strongly the departing work already reads as a corridor,
    // `dip` reads that work's own measured horizon, and `lead` is the finger count read from one
    // published range onto another and turned over, so a joint of many fingers bites shallow and
    // one of few bites deep and the joint's own travel holds. One names a different measurement
    // than the row it was handed in: `fingers` was written against `structure.grid.countFrom`,
    // which is stripped before a work record reaches the engine, and the period that count is
    // derived from is not — so the same number is derived here from the number that travels. And
    // one is a real gap, stated rather than filled: see `seam`.
    //
    // A NOTE TRAVELS IN EVERY SCORE, SO IT IS A SENTENCE AND NOT AN ESSAY. Each of these strings is
    // written into every node the handle drives, and the first draft of this block put 823 of the
    // collection's scores over the client's own byte fence — where a score is refused WHOLE, which
    // is the same lesson the intent cap taught one section down. The reasoning lives in this
    // comment, where it costs a reader nothing and the wire nothing at all.
    // WIDENED 2026-08-18 for the mirror floor: one measurement, two senses. For the folding
    // instrument it is how far the perspective runs, for the floor how deep a room the passage
    // stands in — and how much a work reads as a corridor answers both. The port declared this
    // «unmeasured»; it is not, and the reading was already here.
    depth: ["measured", "each work's own corridor reading, structure.polar.tunnel — how far the "
                        + "perspective runs, and how deep a room the floor stands in"],
    dip: ["measured", "the departing work's own measured horizon, structure.horizon.y"],
    lead: ["measured", "the finger count, read off its own range onto this one and turned over"],
    fingers: ["measured", "the departing work's repeat across the crease: its frame side over "
                          + "structure.grid.periodPx"],
    // THE GAP THAT WAS REAL AND IS NOW CLOSED (2026-08-26). Where along the turn the departing work
    // falls into two regions is measured in lab/cut-lines.py, and until tonight it was STRIPPED
    // before the engine saw it: a record carried `structure.regions.count` and `.score` and no
    // position at all, so this file could hand no line, `seam` stood at the instrument's own edge
    // and `seamScore` was handed under the instrument's floor to say so out loud. The record now
    // carries `structure.regions.line.{x,y}.at` and `.explains` — a Python mirror of
    // `lab/effects/box.js`'s own `seamOf`, verified against that file's published readings — so the
    // first of the charter's five box conditions is met rather than honestly unmet, and both rows
    // below name a measurement because a record now holds one.
    //
    // WHICH AXIS EACH READS is the crease's own direction and is settled in the fill branch, not
    // here: `box.js` has `vertical = P.axis >= 0.5` and calls `seamOf(src, !vertical)`, and the
    // engine's `flat` is that same `vertical`, so a crease at or above a half reads the record's
    // `y` and one below it reads the `x`.
    seam: ["measured", "structure.regions.line.<axis>.at — where along the crease's own direction "
                       + "the departing work falls into two regions, as a share of its own frame. "
                       + "The handle's published span is the measurement's own search window, the "
                       + "middle half of the work, so the reading is placed on it in the unit it is "
                       + "already in"],
    // AND THIS ROW NAMES `.explains` AND NOT `regions.score`, which is the substantive half of the
    // repair. `SEAM_FLOOR` in the instrument was calibrated against the between-versus-within
    // column reading and against no other quantity. `regions.score` is the share of frame the large
    // regions cover — a different quantity that happens to share the same 0..1 range — so pointing
    // the floor at it would open a gate on grounds nobody measured, on every pair, silently.
    seamScore: ["measured", "structure.regions.line.<axis>.explains — how cleanly that line divides "
                            + "the picture, the between-versus-within reading of the work's own "
                            + "columns at that place. It is handed with the instrument's own floor "
                            + "UNAPPLIED, so the gate stays where the gate lives"],
    mask: ["module-rest", "a judge channel the module rests shut"],
    // THE WAVED RIBBON AND THE PARQUET, from the instruments lane's own manifests. No template names
    // these yet; the rows stand so a score that names them can be written, and so the register keeps
    // its promise that every handle says where it comes from. The wave's own two readings —
    // texture.type and texture.localStraightness — are stripped before the engine sees them, so the
    // composer can hand only nothing, which is the straight ribbon and the reference look.
    // THE FABRIC'S OWN DEPTH IS NOT A READING OF EITHER PHOTOGRAPH, and the woven instrument's own
    // manifest says so in as many words: this handle "reads nothing of the work: it is a property of
    // the FABRIC, the same class as the ribbon edge's own two waves and the contact shadow's own
    // reach, and it is the material speaking rather than the photograph". The bare `depth` row below
    // was written for the folding instrument, whose depth IS a corridor reading, and `sourceOf`
    // handed it to the weave as well because the two share a handle name. So the weave's own depth
    // carried a promise of a measurement that no work record holds and that nothing was ever going
    // to write, and it stood frozen at the instrument's rest with no sentence saying why. A scoped
    // row is the honest answer: the fabric rests where the fabric rests, and the plan says so.
    "weave.depth": ["unmeasured", "nothing of either work: the woven instrument's own manifest calls "
                                  + "this a property of the fabric rather than of the photograph, "
                                  + "so it stands at the material's own rest"],
    // THE RIBBON EDGE'S OWN WAVE HAS NOTHING IN THE RECORD TO READ. This row promised
    // `texture.type` at «рябь» with `1 - texture.localStraightness` as the depth, and neither field
    // reaches the engine: both are stripped before a work record leaves the lab, which this file
    // already says a few rows below about the same pair of fields. So the row promised a reading
    // that no pair in the world could supply, `fillPlan` never wrote one, and the handle stood at
    // the instrument's own rest for the whole passage with no sentence saying why — which is how
    // the wave came never to appear. Naming it `unmeasured` is the honest answer: the plan now says
    // the instrument publishes it and no measurement is written for it, and the day the two fields
    // survive the trip this row becomes `measured` again with the same words it always had.
    wave: ["unmeasured", "the ribbon edge's own ripple: texture.type and texture.localStraightness "
                         + "are the reading, and both are stripped before a work record reaches "
                         + "the engine"],
    wavePeriod: ["measured", "texture.spectralPeriodPx over the work's own frame side"],
    waveDrift: ["measured", "the same spectral period, as a share of it travelled in a second"],
    field: ["progress", "the passage's own travel, one envelope for the plane and the parquet"],
    parquetPeriod: ["measured", "structure.ownDevice.stepPx over the work's own frame side"],
    parquetTurn: ["measured", "structure.ownDevice.angleDeg, the angle that step was cut at"],
    // THE UNFOLD'S OTHER THREE. Its manifest now travels in the composer's own constants — the
    // settings record carries every instrument the composer CAN cast, not only the ones it casts
    // today — so the register names them, and the day a kind maps to this instrument a score for it
    // can be written. `panels` and `stagger` read the work; `tilt` is the plane's own attitude and
    // reads the same measured angle the parquet turns at.
    panels: ["measured", "two faces or four, from the departing work's own measured region count, "
                         + "structure.regions.count"],
    stagger: ["measured", "the golden-angle stagger of that count, charter shelf 13's stagger "
                          + "instrument on the sheet's own time axis"],
    tilt: ["measured", "structure.ownDevice.angleDeg, the angle the work's own step was cut at, "
                       + "which is the attitude the plane is laid away at"],
    // THE GLASS'S OWN FOUR, from the lens port's manifest. Its other five — the dial, the two
    // centres, the rim's weight and the judges' channel — are rows this register already carried,
    // and the two centres carry exactly the reading this instrument wants: the midpoint of the two
    // measured radial centres is the point the two works' own structure turns about, which is where
    // the glass rests.
    // A NOTE TRAVELS IN EVERY SCORE, so each of these four is a clause and the reasoning stays up
    // here where it costs the wire nothing. `fold` chooses among the three glasses by the readings
    // named: the mirrored wedges where the pair's rotational order reads, the wound glass where its
    // twirl does, the plain magnification where neither. `wedges` makes the fold repeat as often as
    // the work itself does. `power` brings a piece of the departing work to the size of the
    // arriving work's own piece.
    fold: ["measured", "the pair's own structure.rotational and structure.polar.twirl"],
    // WIDENED 2026-08-18 at the merge, for the fold: the glass folds its disc into as many mirrored
    // wedges as the work turns, and the kaleidoscope tiles its wedge outward the same number of
    // times. One measurement, two acts, one row. Where the record carries no rotational order the
    // handle is simply not driven and the module's own count stands, which is the register working.
    wedges: ["measured", "structure.rotational.n, the work's measured rotational order — how many "
                         + "mirrored wedges the disc folds into, and how often the fold repeats"],
    // THREE INSTRUMENTS DRIVE `twist` AND ALL THREE READ ONE MEASUREMENT, so one row serves them,
    // the same way `axis` serves the ribbons, the crease and the fold line. The glass winds by it,
    // the kaleidoscope LEANS its fold by it, and the corridor SHEARS its spiral by it — three acts
    // of one reading of how strongly a work's own making reads as a twirl. Nothing is renamed:
    // renaming one would be a second name for one measurement, which is the thing this register
    // exists to prevent.
    twist: ["measured", "structure.polar.twirl, how strongly the work's own making reads as a "
                        + "twirl — the glass's wind, the fold's lean and the corridor's shear"],
    // THE KALEIDOSCOPE'S OTHER TWO. Its `mix`, `clock`, `centreX`, `centreY`, `shade` and `mask`
    // already had rows, and `wedges` and `twist` are the two widened above.
    rings: ["measured", "structure.ownDevice.count where the work's own device is rings"],
    reach: ["measured", "structure.ownDevice.stepPx over the work's own frame side"],
    power: ["measured", "the ratio of the two works' measured ownDevice.stepPx"],
    // THE CORRIDOR'S OWN TWO, from the instrument that answers the `corridor` world this file has
    // named since stage 0 and had no instrument for. Its other eight are already named: `mix` and
    // `clock` are the transaction's, `seed` is the pair's die, `mask` the judges' channel, `depth`
    // reads the very corridor reading its row already cites, `centreX`/`centreY` the same two
    // radial centres they always did, and `twist` is the row widened above, which the corridor
    // shears its spiral by.
    //
    // BOTH ROWS ARE OF THE PAIR AND NOT OF ONE END OF IT. The lane wrote «the DEPARTING work's own
    // measured ring repeat» and «the DEPARTING work's own measured turn». A reading that names one
    // end of an edge casts that edge one way and something else the other way back, which is the
    // thing `always` repaired across this whole file: the reading is of the PAIR and carries no
    // direction, so a return casts as its outward pass did. `spokes` also read «and its ring count
    // where that turn reads under its floor» — a floor with no number left behind it in this file,
    // struck under his 08:47 word; where the turn is not recorded the handle is simply not driven.
    ribs: ["measured", "each work's own measured ring repeat, structure.ownDevice.count where it "
                       + "was cut as rings"],
    spokes: ["measured", "each work's own measured turn, structure.rotational.n"],
    flank: ["unmeasured", "how upright a tooth's flank stands. The work's own radial streak is "
                          + "measured in the polar block and reads on exactly this, but no scale "
                          + "between a streak reading and this handle is recorded, so the "
                          + "instrument's own default stands and the gap is named"],
    // THE DRIFTING INSTRUMENT'S OWN TWENTY-ONE, and it is the first instrument whose handles name a
    // WORK EACH: its two things travel one out of the frame and one into it, so where each stands,
    // how much emptiness each has and whether each carries a waterline are read per work and not
    // per pair. `A` is the departing work and `B` the arriving one throughout, which is the
    // module's own naming. Its other seven — the dial, the clock, the die, the ground's grain and
    // the three judges' channels — are rows this register already carried.
    //
    // SIX OF THE TWENTY-ONE NAME NO MEASUREMENT, and each says exactly what is missing rather than
    // resting quietly. Four are densities the module solves off a work's own PIXELS at build time —
    // the threshold at which the silhouette's area equals the measured figure share, and the density
    // nothing in the work reaches — and a work record carries the object's measured box and no
    // density reading at all. The other two are the module's own shares of a distance and a size
    // that the pair already sets through the handles beside them.
    homeAx: ["measured", "the centre of the departing work's own measured object box, "
                         + "structure.dominantObject.bbox, as a share of its frame"],
    homeAy: ["measured", "the centre of the departing work's own measured object box, "
                         + "structure.dominantObject.bbox, as a share of its frame"],
    homeBx: ["measured", "the centre of the arriving work's own measured object box, "
                         + "structure.dominantObject.bbox, as a share of its frame"],
    homeBy: ["measured", "the centre of the arriving work's own measured object box, "
                         + "structure.dominantObject.bbox, as a share of its frame"],
    voidShareA: ["measured", "motifs.voidShare of the departing work, the share of its frame its "
                             + "own measured open ground holds, which is how far a thing may "
                             + "travel before it stands on architecture instead of on emptiness"],
    voidShareB: ["measured", "motifs.voidShare of the arriving work, read the same way"],
    // The record now publishes the seam's own STRENGTH, lab/step1-motifs.py:347-360's score of how
    // far the two sides of a work's best-fit seam differ in light and in busy-ness, carried beside
    // the line itself as structure.horizon.seam (lab/build-workrecords-v1.py:121). `locusOf` above
    // still ranks a measured seam as whole evidence when it ranks the three loci — that is a
    // routing decision off the motif list and reads no strength — so this row and that one differ.
    seamA: ["measured", "the departing work's own measured seam strength, structure.horizon.seam"],
    seamB: ["measured", "the same of the arriving work"],
    horizon: ["measured", "how much of each work reads as grain rather than as line, "
                          + "texture.scoreFromCutLines — the weaker of the two, because the front "
                          + "is where the two grounds meet and either straight end rules it "
                          + "straight"],
    flight: ["unmeasured", "the module's own share of a distance the pair already sets: the reach "
                           + "is the smaller of the two works' measured open grounds, which reach "
                           + "the picture through voidShareA and voidShareB, so driving this too "
                           + "would count one measurement twice"],
    shrink: ["unmeasured", "how much size a thing gives up as it goes. Nothing in a work record "
                           + "bears on it: the record carries where the thing stands and how much "
                           + "emptiness is round it, and both already reach the picture"],
    thrA: ["unmeasured", "the density the departing work's silhouette is cut at, solved off that "
                         + "work's own pixels so its mask's area equals the measured figure share; "
                         + "a work record carries the object's box and no density reading"],
    thrB: ["unmeasured", "the same of the arriving work"],
    maxA: ["unmeasured", "the density nothing in the departing work reaches, read off its pixels "
                         + "at build; no density reading travels in a work record"],
    maxB: ["unmeasured", "the same of the arriving work"],
    voidAr: ["unmeasured", "the departing work's own ground colour, the mean outside its measured "
                           + "box, in three channels; the record carries its palette by name and "
                           + "rung and no channel value"],
    voidAg: ["unmeasured", "the same, the departing work's green channel"],
    voidAb: ["unmeasured", "the same, the departing work's blue channel"],
    voidBr: ["unmeasured", "the arriving work's own ground colour, red channel; no channel value "
                           + "travels in a work record"],
    voidBg: ["unmeasured", "the same, the arriving work's green channel"],
    voidBb: ["unmeasured", "the same, the arriving work's blue channel"],

    // ==== THE ARSENAL LANE, 2026-08-18, on his word of 18:39 ====================================
    // Six instruments carried across from lab/effects/. Their shared handles — `mix`, `clock`,
    // `seed`, `shade`, `travel`, `mask` — read what the rows above already name and join them.
    // What follows is what they read of their own, and the scoped keys are the names that turned
    // out to be TWO readings once six more instruments published handles.

    // ---- the interfering instrument ----
    periodA: ["measured", "the departing work's own measured period, texture.spectralPeriodPx over "
                          + "its own frame side, placed on the span in frame heights the handle "
                          + "itself publishes — the instrument is the one home of that span"],
    periodB: ["measured", "the arriving work's own measured period, read the same way"],
    contrast: ["measured", "how near the two works' own rhythms stand, the smaller count over the "
                           + "larger: two nearly equal periods make lobes worth handing the frame "
                           + "over in and the slow envelope owns the cut, two far apart make no "
                           + "envelope worth the name and the raw sum is the honester picture"],
    beatTilt: ["measured", "the angle the two works' own measured lattices stand apart — "
                           + "structure.ownDevice.angleDeg, or structure.grid.angleDeg where no "
                           + "step was recovered — folded back under a right angle, since a lattice "
                           + "angle is a line direction. The module pinned nine degrees; the third "
                           + "picture IS the two gratings interfering, so the angle is the pair's"],
    phase: ["unmeasured", "where in its own cycle each grating starts. Nothing in a work record "
                          + "bears on it: a record carries a period and an angle and no phase"],
    "beat.lead": ["unmeasured", "how far apart the lobes' own moments are set. It is charter shelf "
                                + "13's stagger on this instrument's own time axis, and the count "
                                + "it would be taken on is already spent on the two periods, so "
                                + "driving it would count one measurement twice"],

    // ---- the gate instrument ----
    jamb: ["measured", "the departing work's own measured gate, motifs.gateGap — one minus the "
                       + "busy-ness of the middle band over the denser flank, which is how plainly "
                       + "a hole stands between two masses"],
    teeth: ["measured", "the departing work's own repeat across the slot: its frame side over "
                        + "structure.grid.periodPx, a whole count, because a tooth is one"],
    swing: ["measured", "the share of the frame the departing work's own open ground holds, "
                        + "motifs.voidShare — a work with room around its masses lets them travel "
                        + "wide"],
    slotAxis: ["measured", "the departing work's own measured gate axis, motifs.gateAxis: lab/"
                          + "step1-motifs.py sweeps both the column and the row profile of the "
                          + "work's own busy field and keeps whichever scores better, so a work "
                          + "whose slot stands upright opens sideways and one whose slot lies "
                          + "across parts up and down"],
    slotPlace: ["measured", "where the departing work's own slot stands along its own axis, "
                            + "motifs.gatePlace — lab/step1-motifs.py's slot_on() sweeps the band "
                            + "centre across the middle half of the frame and keeps the "
                            + "best-scoring place, so the record now carries where the gate is "
                            + "rather than only how plainly it reads"],
    slotHalf: ["measured", "half the departing work's own slot width, motifs.gateHalf — the same "
                           + "slot_on() grows the band outward from its own best centre while the "
                           + "profile stays quiet, so the width is the slot's own rather than the "
                           + "motif's fixed band"],
    "gates.press": ["unmeasured", "how hard the two leaves press their teeth together. It is a "
                                  + "property of the joint rather than of either photograph"],
    "gates.lead": ["unmeasured", "how far apart the two leaves' own departures stand"],

    // ---- the grid-and-colour instrument ----
    countFrom: ["measured", "the departing work's own frame side over the step it was cut at, "
                            + "structure.ownDevice.stepPx, with structure.grid.periodPx where no "
                            + "device was derived — the count of its own lattice across the frame"],
    countTo: ["measured", "the arriving work's own count, read the same way, so the cut leaves one "
                          + "work's structure and arrives at the other's"],
    angleFrom: ["measured", "structure.ownDevice.angleDeg of the departing work, said as a position "
                            + "on a quarter turn; structure.grid.angleDeg where none"],
    angleTo: ["measured", "the same of the arriving work"],
    kindA: ["measured", "structure.ownDevice.kind of the departing work: rings are cut into rings, "
                        + "a grid into tiles, a banded work into strips, and a work whose device was "
                        + "never recovered is cut by its own colour, the one kind needing no lattice"],
    kindB: ["measured", "the same of the arriving work"],
    "grid-colour.stagger": ["measured", "the golden-angle stagger of the count the frame is actually "
                                        + "cut into, charter shelf 13's stagger instrument, so no "
                                        + "two pieces of the cascade leave together. The sheet's own "
                                        + "`stagger` takes the same shelf on its region count; this "
                                        + "one takes it on the lattice count, so the two are two "
                                        + "readings and two rows"],
    "grid-colour.lead": ["measured", "how far ahead of its own shapes the arriving palette comes — "
                                     + "charter shelf 11's colour herald — read as the distance "
                                     + "between the two works on palette.colourfulness. `lead` is "
                                     + "about how early the arriving work's PALETTE is full, so the "
                                     + "collection's own colourfulness ladder is the right family "
                                     + "for it, unlike the five tonal sites the judge seat's "
                                     + "standing correction of 2026-08-18/19 moved onto "
                                     + "luminance.level instead"],
    countBeatIn: ["unmeasured", "the stretch of the passage the count travels over. Where in a "
                                + "passage a structure moves is the score's shape, not the pair's"],
    countBeatOut: ["unmeasured", "the same at the far door"],
    angleBeatIn: ["unmeasured", "the stretch the angle travels over; the same reason"],
    angleBeatOut: ["unmeasured", "the same at the far door"],
    // THE SIX ROWS BELOW ARE READ ONLY WHERE THIS CUE OWNS LIGHT-COLOUR. Shelf 17's levels law
    // gives that level one active voice; where another cue of the same passage owns it instead this
    // one only accompanies, and `fillPlan`'s "grid-colour" branch leaves every one of the six unset
    // in that case, which is the manifest's own rest of 0 rather than a second silence typed here.
    colourPeriod: ["measured", "the departing work's own colour.sat, carried through BEAT_DIAL and "
                               + "spread — lab/step4-assembler.js:1966-2010, ported — read only "
                               + "where this cue owns LIGHT-COLOUR"],
    colourPhase: ["measured", "the voice's own place among this instrument's two, i/2 — the same "
                              + "index-over-count rule the assembler stands its own four voices a "
                              + "quarter turn apart by; the same LIGHT-COLOUR ownership gate"],
    colourAmp: ["measured", "the departing work's own colour.sat, VOICE_SHARE of it; the same "
                            + "LIGHT-COLOUR ownership gate"],
    lightPeriod: ["measured", "the departing work's own colour.contrast, carried through BEAT_DIAL "
                              + "and spread; the same LIGHT-COLOUR ownership gate"],
    lightPhase: ["measured", "the voice's own place among this instrument's two, i/2; the same "
                             + "LIGHT-COLOUR ownership gate"],
    lightAmp: ["measured", "the departing work's own colour.contrast, VOICE_SHARE of it; the same "
                           + "LIGHT-COLOUR ownership gate"],

    // ---- the parting-by-light instrument ----
    cellsA: ["measured", "the departing work's own grain said as cells across its frame — "
                         + "texture.spectralPeriodPx over frameSide, turned over — so a work made of "
                         + "coarse masses parts into few large areas and a fine-grained one into "
                         + "many small ones"],
    cellsB: ["measured", "the arriving work's own grain, read the same way"],
    // THE GAP ABOVE IS CLOSED. The level a work parts at is a level of TONE, and `luminance.level`
    // now carries exactly that — the work's own median luminance on a 128-cell grid,
    // lab/analyze/recipes.py:551-613 colour_stats()'s python port of `measure(image)` in
    // lab/effects/strata-light.js:108-113, the number that module solves and, unread, discards. It
    // is not `palette.colourfulness` (the judge seat's standing correction of 2026-08-18/19): that
    // field is the collection's own COLOURFULNESS ladder, half chroma and half hue spread, and would
    // put a colour number where this tone number belongs.
    levelA: ["measured", "the departing work's own `luminance.level` — its median luminance, a port "
                        + "of `measure(image)` in lab/effects/strata-light.js:108-113"],
    levelB: ["measured", "the same of the arriving work"],
    // THE TWELVE ROWS BELOW ARE READ ONLY WHERE THIS CUE OWNS LIGHT-COLOUR. Shelf 17's levels law
    // gives that level one active voice; where another cue of the same passage owns it instead this
    // one only accompanies, and `fillPlan`'s "strata-light" branch leaves every one of the twelve
    // unset in that case, which is the manifest's own rest of 0 rather than a second silence typed
    // here.
    colourPeriodA: ["measured", "the departing work's own colour.sat and colour.brightness, carried "
                                + "through BEAT_DIAL and spread — lab/step4-assembler.js:1966-2010, "
                                + "ported — read only where this cue owns LIGHT-COLOUR"],
    colourPeriodB: ["measured", "the same of the arriving work"],
    colourPhaseA: ["measured", "this voice's own place among the instrument's four, i/4 — "
                               + "step4-assembler.js:2000; the same LIGHT-COLOUR ownership gate"],
    colourPhaseB: ["measured", "the same rule at the arriving work's own slot"],
    colourAmpA: ["measured", "the departing work's own colour.sat, VOICE_SHARE of it; the same "
                             + "LIGHT-COLOUR ownership gate"],
    colourAmpB: ["measured", "the arriving work's own colour.sat, VOICE_SHARE of it"],
    lightPeriodA: ["measured", "the departing work's own colour.sat and colour.contrast, carried "
                               + "through BEAT_DIAL and spread; the same reason and the same "
                               + "LIGHT-COLOUR ownership gate"],
    lightPeriodB: ["measured", "the same of the arriving work"],
    lightPhaseA: ["measured", "this voice's own place among the instrument's four, i/4; the same "
                              + "LIGHT-COLOUR ownership gate"],
    lightPhaseB: ["measured", "the same rule at the arriving work's own slot"],
    lightAmpA: ["measured", "the departing work's own colour.contrast, VOICE_SHARE of it"],
    lightAmpB: ["measured", "the arriving work's own colour.contrast, VOICE_SHARE of it"],

    // ---- the parting-by-scale instrument ----
    // THE MODULE'S OWN SINGLE SHARED HANDLE (strata-scale.js:450-506) — one number for the whole
    // pair, because the split between the two strata is a property of the arrival itself and not a
    // travelling value. Charter shelf 12's spectral sentence is what it sets: the blurred mass of
    // the ARRIVING work grows first and its detail grows into it, and this handle is how long the
    // mass stands alone before the detail follows. It stood at the module's own rest with the note
    // that nothing of either photograph decides it; the record says otherwise, and this file was
    // already reading the field — the instrument's own `suits` row ranks the pair on
    // `texture.reliefEdge`, the scale a work parts at.
    handover: ["measured", "the ARRIVING work's own parting scale, texture.reliefEdge — how much of "
                           + "its own luminance its mass stratum carries — read as the share of the "
                           + "dial its detail needs, which is one minus that reading"],
    // EACH STRATUM'S OWN MEASURED CENTRE OF GRAVITY, off `texture.reliefCentreMassX`/
    // `reliefCentreDetailX` — lab/analyze/recipes.py's own port of the centre-of-gravity reading in
    // lab/effects/strata-scale.js's own `cut()` (strata-scale.js:279-287), threaded through
    // build-elements-v1.py and build-workrecords-v1.py exactly as `luminance.level` already is for
    // strata-light. Read PER WORK exactly as `levelA`/`levelB` above: A the departing work's own
    // pair of centres, B the arriving work's.
    massCentreXA: ["measured", "the departing work's own texture.reliefCentreMassX — the mass "
                               + "stratum's own measured centre of gravity"],
    massCentreXB: ["measured", "the same of the arriving work"],
    detailCentreXA: ["measured", "the departing work's own texture.reliefCentreDetailX — the "
                                 + "detail stratum's own measured centre of gravity"],
    detailCentreXB: ["measured", "the same of the arriving work"],

    // ---- the leaning instrument ----
    // TWO SCOPED ROWS AND THE REASON IN ONE LINE EACH. `tilt` above is the sheet's plane attitude
    // and reads a lattice ANGLE; this instrument's `tilt` is how far the plane lies into depth and
    // reads a corridor. `horizon` above is the drifting instrument's front straightness and reads a
    // texture score; this instrument's `horizon` is the line the plane turns about. Two names, four
    // readings, and no module is renamed to fit the table.
    "tilt.tilt": ["measured", "each work's own corridor reading, structure.polar.tunnel — a picture "
                              + "that already reads as depth is laid down further, and the lean "
                              + "travels from the departing work's reading to the arriving one's"],
    "tilt.horizon": ["measured", "each work's own measured horizon, structure.horizon.y, so the "
                                 + "plane's axis stands where the photograph already puts its own"],
    squeeze: ["measured", "the pair's own repeat said as cells across the frame's height, "
                          + "positioned about the handle's default by the two readings' ratio: a "
                          + "fine-grained picture stops resolving sooner as the far rows close up, "
                          + "so the camera stands further back for it"],
    columns: ["measured", "the band family each work's own structure was cut into — the same "
                          + "measured strip count the fabric's ribbons are cut on — which is how "
                          + "many columns the handover front is broken into"],
    "tilt.lead": ["unmeasured", "how far apart the front's own columns stand in their departures"],

    // ---- the waterline instrument ----
    // TWO SCOPED ROWS AGAIN, and the port spotted this one itself: the drifting instrument's
    // `seamA`/`seamB` carry `seam_horizon`, how STRONGLY a work reads a waterline, and these carry
    // `seam_y`, WHERE that line sits. Two numbers of one measure, two readings, two rows.
    // Its `depth` and its `swell` are the OTHER case and write no row at all: they read exactly
    // what `depth` and `swell` above already name, so they join those rows as the glass, the fold
    // and the corridor join `twist`.
    "waterline.seamA": ["measured", "the departing work's own measured horizon, structure.horizon.y "
                                    + "— where its mirror seam stands down its own frame, which is "
                                    + "the line the crossing leaves from"],
    "waterline.seamB": ["measured", "the arriving work's own measured horizon, which is the line the "
                                    + "crossing lands on"],
    "waterline.order": ["measured", "the golden-angle stagger of the departing work's own grain "
                                    + "count, charter shelf 13's stagger instrument, so no two "
                                    + "stretches of the tide arrive together. The mesh's own "
                                    + "`order` takes the same shelf on a ring count, so the two are "
                                    + "two readings and two rows"],
    "waterline.lead": ["unmeasured", "how far ahead of the sky the water hands over. The prophecy is "
                                     + "the instrument's own act rather than a fact about either "
                                     + "photograph"],
    line: ["unmeasured", "the lift of the waterline off the seam it is derived from. The seam itself "
                         + "travels, through the two rows above; this is the module's own offset "
                         + "from it and reads no photograph"],
    tideCells: ["measured", "the departing work's own grain said as cells across its frame, which "
                            + "is how finely the tide's own front is broken. Nothing in this tree "
                            + "records how many cells one step of this handle is worth, so that "
                            + "count is positioned about the handle's default by its ratio to the "
                            + "arriving work's own count — the same idiom `grain` takes on this "
                            + "very reading"],
    comb: ["module-rest", "a judge channel the module rests at 1, the swell's comb through the "
                          + "reflection"],
    raw: ["module-rest", "a judge channel the module rests shut: the walk with its response curve "
                         + "taken out"],
    settle: ["module-rest", "a judge channel the module rests at its own value"],
    shadeEdge: ["module-rest", "a judge channel the module rests at 1: the arriving work's own "
                               + "front shadow, kept apart from the waterline's so a spoiling of "
                               + "one cannot pass on the other"],
    shadeLine: ["module-rest", "a judge channel the module rests at 1: the waterline's own shadow"],

    // ---- the darkroom instrument (studio) ----
    // SIX ARE MEASURED, EACH NAMED IN pass-inst-studio.js's OWN HANDLES BLOCK AND FILLED BY THE
    // "studio" BRANCH OF `fillPlan` BELOW; the rest are the module's own eight-way choice of
    // instrument — which operation a visitor's own hand would have switched on, how far a zoom or a
    // fold or a hue turn should stand — and no reading in a work record answers a choice, so each
    // rests at the number the port names as the module's own (studio.js's own opening pose and its
    // own declared defaults) and says so rather than hiding it, exactly as gates' own `jamb`/
    // `teeth`/`swing` do for the same reason.
    "studio.panX": ["measured", "the midpoint of the two works' own measured radial centres, "
                                + "structure.radial.centre — the same reading hero's centreX and "
                                + "livemirror's fold both read, here spent on the crop's own pan"],
    "studio.panY": ["measured", "the midpoint of the two works' own measured radial centres, "
                                + "structure.radial.centre — the same reading hero's centreY and "
                                + "livemirror's fold both read, here spent on the crop's own pan"],
    "studio.foldX": ["measured", "the midpoint of the two works' own measured radial centres, "
                                 + "structure.radial.centre — the same reading livemirror's own fold "
                                 + "reads, here spent on the mirror operation's own fold line"],
    "studio.foldY": ["measured", "the midpoint of the two works' own measured radial centres, "
                                 + "structure.radial.centre — the same reading livemirror's own fold "
                                 + "reads, here spent on the mirror operation's own fold line"],
    "studio.kalN": ["measured", "structure.rotational.n, the pair's own measured rotational order, "
                                + "snapped onto the kaleidoscope operation's own count — the same "
                                + "reading kaleidoscope's own wedges handle reads"],
    "studio.tileN": ["measured", "the work's own frame side over structure.grid.periodPx, the count "
                                 + "of its own measured lattice across it — the same reading "
                                 + "parquet's own tiles handle reads, here spent on the tile "
                                 + "operation's own repeat count"],
    "studio.polarSpread": ["measured", "structure.polar.planet, how strongly the pair reads as a "
                                       + "little world — the same reading hero's own planet handle "
                                       + "reads, placed on the handle's own span the higher end down: "
                                       + "the stronger the reading the narrower the spread stands, "
                                       + "which is what the shader's own division by spread makes the "
                                       + "planet operation read as a world the sooner"],
    "studio.twirlAmt": ["unmeasured", "how far the twirl operation turns. structure.polar.twirl reads "
                                      + "how strongly the pair's own making already winds, but that "
                                      + "reading carries no SIGN — this handle's own span runs "
                                      + "negative to positive, either direction the same amount of "
                                      + "turn, and no measurement says which way a visitor's hand "
                                      + "would have gone — so it rests at the module's own default "
                                      + "rather than at a sign this file would have to choose"],
    "studio.cropOn": ["module-rest", "the module's own opening pose (studio.js, \"open on something "
                                     + "worth looking at\"): the zoom operation stands on"],
    "studio.zoom": ["module-rest", "the module's own opening pose's own zoom, 1.15 — no reading says "
                                   + "how far a visitor's own hand would have pulled it in"],
    "studio.twirlOn": ["module-rest", "the module's own opening pose: the twirl operation stands off "
                                      + "until a score switches it on"],
    "studio.polarOn": ["module-rest", "the module's own opening pose: the planet operation stands on"],
    "studio.polarFlip": ["module-rest", "the module's own declared default: ground in rather than "
                                        + "sky in — no reading says which way a visitor would flip it"],
    "studio.mirrorOn": ["module-rest", "the module's own opening pose: the mirror operation stands on"],
    "studio.mirrorMode": ["module-rest", "the module's own opening pose's own mode, left-right — no "
                                         + "reading says which of the mirror's three modes a visitor "
                                         + "would have chosen"],
    "studio.kalOn": ["module-rest", "the module's own declared default: the kaleidoscope operation "
                                    + "stands off until a score switches it on"],
    "studio.kalRot": ["module-rest", "the module's own rest of nothing turned — the kaleidoscope's "
                                     + "own drift off the handed second carries the operation's "
                                     + "breath instead, exactly as the module's own pointer-free rest "
                                     + "does"],
    "studio.ringOn": ["module-rest", "the module's own declared default: the endless zoom stands off "
                                     + "until a score switches it on"],
    "studio.ringTwist": ["module-rest", "the module's own declared default, 0.35 — no reading says "
                                        + "how far a visitor's own hand would have turned it"],
    "studio.ringSize": ["module-rest", "the module's own declared default, \"some\" — no reading says "
                                       + "which of the endless zoom's three ring sizes a visitor "
                                       + "would have chosen"],
    "studio.tileOn": ["module-rest", "the module's own declared default: the tile operation stands "
                                     + "off until a score switches it on"],
    "studio.colOn": ["module-rest", "the module's own declared default: the colour operation stands "
                                    + "off until a score switches it on"],
    "studio.hue": ["module-rest", "the module's own declared default of no turn at all — no reading "
                                  + "says which way round the wheel a visitor's own hand would have "
                                  + "turned it"],
    "studio.colLook": ["module-rest", "the module's own declared default, \"rich\" — no reading says "
                                      + "which of the colour operation's three looks a visitor would "
                                      + "have chosen"],
    // THE THREE ELEMENTS OF SHELF 14, and every row of the three is instrument-scoped. `sourceOf`
    // reads the scoped row first, so a name this file already carries in another instrument's unit
    // — `axis` above all — answers here in this instrument's own.
    "pour.columns": ["measured", "the work's own frame side over structure.grid.periodPx, the "
                                 + "count of its own measured lattice across it; the same off "
                                 + "structure.ownDevice.stepPx where no grid period was derived. "
                                 + "The picture lets go along the repeat it was made on"],
    "pour.repose": ["measured", "texture.detailPx of the two works over their own frame sides, "
                                + "read as a ratio: the heap is made of the arriving work, and a "
                                + "finer material heaps at a steeper angle than a coarse one"],
    "pour.stagger": ["measured", "structure.regions.score of the departing work — how much of the "
                                 + "difference between its own columns its region line explains, "
                                 + "which is how plainly it lets go region by region rather than "
                                 + "all at once. Under the crystallized arrival the same share is "
                                 + "the spread the order takes to travel out from the seed: the "
                                 + "furthest column's own delay comes to exactly this much of the "
                                 + "dial, and every nearer one waits its own share of it"],
    "livemirror.propagate": ["measured", "structure.rotational.score of the ARRIVING work — how "
                                         + "strongly it already reads as its own copies repeated "
                                         + "about a centre, which is the reading the charter's "
                                         + "PROPAGATED arrival is ranked on. It is how far apart "
                                         + "the mirrored copies' own exchanges stand, and the far "
                                         + "copy is the one that changes first"],
    "pour.seedPlace": ["measured", "texture.reliefCentreDetailX of the ARRIVING work — the centre "
                                   + "of gravity of its own detail stratum, where the grain of that "
                                   + "picture gathers thickest and so the least ordered place its "
                                   + "record names. It is `arrivalOf`'s own seed for the "
                                   + "crystallized arrival, handed on to the instrument that "
                                   + "spreads order out from it"],
    "pour.grain": ["measured", "texture.spectralPeriodPx of the two works over their own frame "
                               + "sides, read as a ratio — the departing work's own strongest "
                               + "repeat said as cells across the frame, which is the unit the "
                               + "material instrument's coarse grain is published in"],
    "veil.thickness": ["measured", "texture.scoreFromCutLines — how much of a work reads as grain "
                                   + "rather than as line. A work that IS texture makes a thick "
                                   + "air, because the veil reads a picture at a coarser scale of "
                                   + "its own material and a work of straight architecture has "
                                   + "little there to lose. It travels from the departing work's "
                                   + "reading to the arriving one's"],
    "veil.bodies": ["measured", "the work's own frame side over structure.grid.periodPx, the count "
                                + "of its own measured lattice across it; the same off "
                                + "structure.ownDevice.stepPx where no grid period was derived. "
                                + "The weather banks at the scale the work's own structure stands "
                                + "at"],
    "veil.depth": ["measured", "structure.polar.tunnel, how strongly a work already reads as a "
                               + "corridor — a picture that carries depth gets a deep stack and "
                               + "passes the sheets one at a time, one that reads flat gets them "
                               + "crowded into a single bank that parts once"],
    "veil.airAngle": ["measured", "structure.grid.angleDeg, the direction the work's own lattice "
                                  + "runs, and structure.ownDevice.angleDeg where the device "
                                  + "recovered one — the same recorded angle the parquet's own "
                                  + "`lattice` handle reads. The air moves along the work's own "
                                  + "grain"],
    "wind.rows": ["measured", "the pivot's band family, its measured count along the cut — the "
                              + "same reading `strips` names for the woven ribbon, under this "
                              + "instrument's own name because a row of this instrument is a row "
                              + "and not a ribbon: it is not woven with anything, it is bent"],
    "wind.axis": ["measured", "the banding axis cut-lines.json recorded, read into this "
                              + "instrument's own unit — half turns, the direction a row LIES in. "
                              + "The shared `axis` row names the same recorded measurement in the "
                              + "woven instrument's unit, which is a three-way code, so this "
                              + "handle takes a row of its own rather than a value in another "
                              + "instrument's scale"],
    "wind.bend": ["measured", "structure.banding.score — how plainly a work bands. A work that "
                              + "bands plainly has rows the air can catch; one that reads as a "
                              + "single field is barely moved, which is the picture saying what it "
                              + "is rather than a floor turning it away. It travels from the "
                              + "departing work's reading to the arriving one's"],
    "wind.gust": ["measured", "structure.grid.periodPx over the work's own frame side, read as a "
                              + "ratio between the two works — the repeat each carries along the "
                              + "row, so the body of air is as long as the thing it is blowing "
                              + "over"],
    "wind.lag": ["measured", "structure.grid.angleDeg read AGAINST the row axis above — the tangent "
                             + "of the angle between the work's own lattice and the direction its "
                             + "rows lie in, so the air comes in across the work's own grain "
                             + "rather than square to a direction nobody measured"]
  };

  // THE ROAD OPENS THE AUTHORED LINE. §4.7: the intent is the one written line a plan opens with,
  // naming this adventure and the shelves it draws from, and a generic line fails review by
  // definition. Under the plural-source law the first thing a person needs to know about a crossing
  // is which of the seven roads it took, so the road says so in its own words before the reading
  // that qualified it. The tonal and spectral genre opens with nothing, because two tonal grounds
  // handing over is what a crossing already is and a line saying so would say nothing.
  var ROAD_PHRASES = {
    "shared-ground": "Along what the two works share. ",
    "spin": "The radial work turns. ",
    "kaleidoscope": "The rings open. ",
    "symmetry-slide": "The parts slide along the works' own symmetry. ",
    "stripes": "The two band families cross into stripes. ",
    "box-fold": "The work folds along its own region lines. ",
    "dissimilar-mystery": "Along what the two works do not share. ",
    "tonal-and-spectral": ""
  };
  // What a further pass on one edge says for itself: charter shelf 16's family drift, in a clause.
  var RETURN_PHRASE = " Pass {passIndex}: same family, handles breathing.";

  var INTENT_TEMPLATES = {
    quiet: "{roadPhrase}The {pivotName} holds at {pivotStrength} and never moves, and the crossing is the one "
      + "held ground played through: {aCount} parts of the first work hand over to {bCount} of "
      + "the second along that cut, and the second work arrives {arrival}{locusPhrase}. "
      + "Shelves 9 the held pivot, 7 the arrival, 17 a quiet link.{registerPhrase}{returnPhrase}",
    "middle-travel": "{roadPhrase}The {pivotName} holds at {pivotStrength} and the ground stays while the "
      + "{axisName} travels from {fromValue} to {toValue}{centrePhrase}. One generator changes "
      + "over a held family, and the second work arrives {arrival}{locusPhrase}. Shelves 9 one "
      + "generator at a time, 12 the parts that become actors, 7 the arrival, 17 a "
      + "middle.{registerPhrase}{returnPhrase}",
    "middle-world": "{roadPhrase}The {pivotName} holds at {pivotStrength} and over it the flat picture "
      + "becomes a {worldName} the viewer stands inside: the {axisName} travels from {fromValue} "
      + "to {toValue}{centrePhrase}, and the second work arrives {arrival}{locusPhrase}. Shelves "
      + "8 the one folded space, 9 the held pivot, 7 the arrival, 17 a middle.{registerPhrase}{returnPhrase}",
    // THE FOLD HAS ITS OWN TWO LINES, because a crossing that folds the frame into a solid has no
    // polar world to name and the world's own templates ask for one. Added 2026-08-17 with the
    // panel road: the miracle these describe is the solid, and shelf 8's folded space is what both
    // cite. A plan shape with no template is a throw inside `declare`, so the suite now composes
    // every pair at every one of the five roles and the row that reads it is what caught this.
    "middle-fold": "{roadPhrase}The {pivotName} holds at {pivotStrength} and the flat picture "
      + "folds into a solid the viewer is carried round: {aCount} parts of the first work hand "
      + "over to {bCount} of the second along that cut, and the second work arrives "
      + "{arrival}{locusPhrase}. Shelves 8 the one folded space, 9 the held pivot, 7 the arrival, "
      + "17 a middle.{registerPhrase}{returnPhrase}",
    "culmination-fold": "{roadPhrase}The {pivotName} holds at {pivotStrength} and is the whole "
      + "ground of a long crossing: the flat picture folds into a solid the viewer is carried "
      + "round, {aCount} parts of the first work hand over to {bCount} of the second along that "
      + "cut, and the second work arrives {arrival}{locusPhrase}. Shelves 8 the one folded space, "
      + "9 the held pivot, 15 the far pair, 17 a culmination.{registerPhrase}{returnPhrase}",
    culmination: "{roadPhrase}The {pivotName} holds at {pivotStrength} and is the whole ground of a long "
      + "crossing: the {axisName} travels the wide distance from {fromValue} to "
      + "{toValue}{centrePhrase}, the flat picture opens into a {worldName}, and the second work "
      + "arrives {arrival}{locusPhrase}. Shelves 8 the one folded space, 9 the held pivot, 15 the "
      + "far pair, 17 a culmination.{registerPhrase}{returnPhrase}"
  };
  var PIVOT_NAMES = {
    banding: "vertical band family", grid: "tile grid", radial: "radial family",
    regions: "region division", texture: "grain",
    dominant_object: "figure against its ground", named_objects: "named objects",
    "tonal-and-spectral": "tonal zones and detail scales",
    "shared-palette-region": "shared palette region",
    "shared-rotational-order": "shared turn"
  };
  var AXIS_NAMES = {
    banding: "band family", dominant_object: "figure", grid: "tile grid",
    radial: "radial reading", regions: "region count", texture: "grain"
  };
  // THE CHARTER'S FIVE ARRIVALS (shelf 7). CRYSTALLIZED, PROPAGATED and INTERFERED joined
  // CARRIED and CONDENSED on 2026-08-26 (naряд S-06); `arrivalOf`, beside `workParts`, is what
  // ranks the five against a pair's own records and hands back the one that plays.
  var ARRIVAL_PHRASES = { CARRIED: "carried by the gesture already running",
                          CRYSTALLIZED: "by crystallizing from a seed",
                          CONDENSED: "by condensing",
                          PROPAGATED: "by propagating through its own mirrored copies",
                          INTERFERED: "by interfering with the departing work's own rhythm" };
  var LOCUS_PHRASES = {
    none: "", pole: " at its own pole {locusX}, {locusY}",
    "horizon-seam": " at its own horizon seam {locusX}, {locusY}",
    gate: " at its own gate {locusX}, {locusY}",
    "grain-seed": " at its own point of greatest disorder {locusX}, {locusY}"
  };
  var WORLD_NAMES = { sphere: "sphere", corridor: "corridor", "log-spiral": "log spiral" };
  var REGISTER_PHRASES = {
    none: "",
    discovery: " The register is discovery: the middle stands in neither work.",
    provocation: " The register is provocation: the two tonal grounds stand far apart.",
    apparition: " The register is apparition: the arriving figure gathers out of open ground."
  };
  var ENDS_LEGEND = {
    banding: ["score", "periodPx", "axis: 0 vertical, 1 horizontal"],
    radial: ["score", "centreX", "centreY", "subType indexes subTypes"],
    regions: ["score", "count"],
    grid: ["score", "periodPx", "angleDeg"],
    texture: ["score", "detailPx", "spectralPeriodPx"],
    dominant_object: ["score", "x0", "y0", "x1", "y1"]
  };
  // The fields §4.4 lets a score's camera carry, and the four a plan carries and a score never does.
  // `lead` says the flight itself is the transition: the camera spends the world voice of the levels
  // law and the instruments underneath hold a quiet register. It is written only where the
  // derivation asks for a led flight, so a score that does not ask carries the field nowhere and
  // reads exactly as it did.
  var CAMERA_ALLOWED = ["owner", "rests", "track", "lead"];
  var PLAN_ONLY_CUE_FIELDS = ["cast", "levelOwnership", "measuredHandles", "returnOf"];

  // THE ONE ROAD TO A HANDLE'S READING. The instrument's own row wins where it has one, and the
  // shared row answers otherwise — so an instrument that reads what everyone else reads writes no
  // row at all, and one that reads something else of its own cannot silently inherit another's.
  function sourceOf(iid, handle) {
    return HANDLE_SOURCE[iid + "." + handle] || HANDLE_SOURCE[handle];
  }

  function fill(template, fields) {
    return template.replace(/\{([A-Za-z]+)\}/g, function (whole, name) {
      var v = fields[name];
      if (v === undefined) throw new Error("pass-composer: the intent has no " + name);
      return typeof v === "string" ? v : pyText(v);
    });
  }

  // ---------------------------------------------------------------------------------------
  // one composer, made over the collection's own constants
  // ---------------------------------------------------------------------------------------

  function make(consts) {
    var MANIFESTS = consts.manifests;
    var INSTRUMENTS = consts.instruments;
    // THE COLLECTION'S FLOORS AND THRESHOLDS ARE NO LONGER READ, and a settings record may go on
    // carrying them. `consts.floors` held ten typed numbers — a cut-line floor per measure and a
    // «tight» floor for three of them — and `consts.thresholds` seven more, each of them a cut taken
    // over one collection of photographs, which is exactly the object charter shelf 20 names. Citing
    // the class is the whole argument; showing how the works on disk fell either side of a cut would
    // argue the point by committing the offence. Both were admission tests: a reading under a floor
    // was struck out of the travelling axes, and a measure both works did not clear its threshold on
    // was no ground — so a family of effect whose floor stands above the range its own reading can
    // reach is dead by construction, whatever pictures are hung.
    //
    // His word of 2026-08-18 09:51 and its sharpening at 09:53: a measurement ranks which genre of
    // crossing suits a pair and shapes the genre that wins, and it never admits and never rejects.
    // A cut taken over some collection answers neither question — it says how a reading stands among
    // other photographs, when what is being asked is how these two photographs stand to each other,
    // and the two numbers are in hand. So the composer reads the pair and nothing else, and it is
    // now free of the collection it happens to be shown with: any two photographs in the world get
    // a crossing, including two that belong to no collection at all.
    var PROVENANCE = consts.provenance;
    var SCORE_FENCE_BYTES = consts.scoreFenceBytes;
    // THE CLIENT'S OWN FENCE ON THE ONE FIELD §4.4 CALLS PROSE, and since 2026-08-18 it is a
    // SHAPING rather than a wall. A score whose intent ran past it was refused WHOLE with «intent is
    // no short text», so an intent nobody measured was a crossing nobody saw. The argument needs no
    // count: the intent is prose whose length is bounded above by nothing in this file, and prose
    // against a fixed cap runs past it whenever it is long enough — so crossings are lost for as
    // long as the cap is a wall. Raising the number from 400 to 600 moved the wall; it did not take
    // it down, and a moved wall refuses the next longer line. `realiseIntent` now FITS the line — it gives up
    // its own clauses in order and then trims at a word, and the plan records what it gave up — so
    // no crossing is ever lost to the length of its own sentence.
    //
    // The number belongs to the client, and the engine's bake publishes it out of
    // the served client's own `PASS_LIMITS` literal as `pass.capabilities.intentChars`, exactly as
    // it has always published the score's byte fence — so the site's staging step carries it into
    // these constants beside `scoreFenceBytes` and the number this file measures against is the
    // number the client applies rather than a second copy of it. What stands after the `||` is a
    // FALLBACK for a settings record built before that line landed; it is the number the client
    // applies today, and a record that carries the field overrides it without argument.
    //
    // UNJUSTIFIED, and precisely in its second half. The VALUE comes from the client and belongs to
    // it, which is a derivation; the `|| 600` beside it does not. That fallback stands for a
    // settings record built before the field existed, and 600 is the number the client happens to
    // apply today rather than anything this file can read — so a record published without the field
    // is measured against a number nobody here derived.
    var INTENT_FENCE_CHARS = consts.intentFenceChars || 600;

    var HANDLE_SPECS = {};
    var FILLS_THE_FRAME = {};
    Object.keys(MANIFESTS).forEach(function (iid) {
      var m = MANIFESTS[iid], specs = {};
      Object.keys(m.handles).forEach(function (h) {
        if (!m.handles[h].open) {
          specs[h] = [m.handles[h].min, m.handles[h].max, m.handles[h]["def"]];
        }
      });
      HANDLE_SPECS[iid] = specs;
      FILLS_THE_FRAME[iid] = !m.coverage.writes;
    });
    // KIND → THE INSTRUMENTS THAT CUT IT, derived from the record the composer was made over.
    // Every published instrument names its own cuts, so a landing one joins the candidates by
    // arriving and no table here can shadow it. The order is settled so a pinned die reproduces a
    // choice exactly; which of the candidates plays is decided per pair, below.
    var CUTS_ON = {};
    Object.keys(INSTRUMENTS).sort().forEach(function (iid) {
      if (!MANIFESTS[iid]) return;
      (INSTRUMENTS[iid].cuts || []).forEach(function (kind) {
        if (!CUTS_ON[kind]) CUTS_ON[kind] = [];
        if (CUTS_ON[kind].indexOf(iid) < 0) CUTS_ON[kind].push(iid);
      });
    });
    var BANDING = (MANIFESTS.weave.handles.axis.banding) || [];
    var AXIS_OF_BANDING = {};
    BANDING.forEach(function (name, i) { AXIS_OF_BANDING[name] = i; });
    // DERIVED — the meshing instrument's own published rung count, read off its manifest. A
    // constant that reads a published fact is not a static value, it is a cached read: the module
    // that changes its own reach re-bases this by itself and no copy of it can go stale.
    var RATIO_STEPS = MANIFESTS.gears.handles.ratio.rungs || 0;
    // DERIVED — THE MESHING PICTURE'S OWN SPAN, read off its manifest at the moment it is needed. A
    // typed 0.7 stood here as the size the picture stopped reading at; that is a fact about the
    // meshing instrument, and the instrument is the one home of it. Both are cached reads of a
    // published fact rather than values chosen here.
    var SIZE_MIN = HANDLE_SPECS.gears.size[0];
    // DERIVED — the other end of the same published span, read the same way.
    var SIZE_MAX = HANDLE_SPECS.gears.size[1];
    // THE COMPOSITE'S OWN TWO LEGIBILITY LEVELS, READ OFF THE INSTRUMENT'S OWN MANIFEST NOW THAT THE
    // WIRE CARRIES IT. A settings record does NOT ship a manifest whole: the site's staging step
    // projects each handle down to a fixed field list — `min`, `max`, `def`, `open`, `banding`,
    // `rungs` — and, until lab/work-readings-v1.py's `read_manifests` was widened to carry it,
    // `applied` was the one field dropped on the floor (tests/fixture_pass_works.json and
    // tests/fixture_pass_composed.json, both captures of the real record, carried exactly the six).
    // `SIZE_MIN` above survives because a span IS one of the six; `applied` used to be missing, so
    // `MANIFESTS.overlay.handles.exposure.applied` read `undefined` in every browser this file ran
    // in. A floor built on it read nought, `voiceFloor(0, cap)` returned nought, and the lift became
    // the identity — which is why the composite's two handles came out byte-identical either side of
    // the repair that was meant to raise them.
    //
    // A COPY of the instrument's own two numbers stood here as the stopgap while the wire was narrow:
    // `pass-inst-overlay.js` publishes `formsBeginAt: 0.5` on `exposure` (where the composite's forms
    // begin) and `edgeOfTheRegion: EDGE` on `presence`, `EDGE` being its own `0.045` (the softness of
    // the region's edge, under which the region never stands at all). The instrument was always their
    // one author; now that `applied` crosses the wire whole, the two are read off it rather than kept.
    var OVERLAY_FORMS_BEGIN_AT = MANIFESTS.overlay.handles.exposure.applied.formsBeginAt;
    var OVERLAY_REGION_EDGE = MANIFESTS.overlay.handles.presence.applied.edgeOfTheRegion;

    // A reading held to the span a number can honestly stand in.
    function clamp01(v) { return v < 0 ? 0 : (v > 1 ? 1 : v); }
    function readingOf(v) {
      var n = Number(v);
      return (n === n && isFinite(n)) ? clamp01(n) : 0;
    }

    // ---- THE LEVEL A CAMERA VOICE HAS TO CLEAR, AND THE LIFT THAT TAKES IT THERE ----
    // Two lines of arithmetic, kept here rather than inline in the camera lane below, because what
    // they claim is a claim about the ARITHMETIC and not about any pair: whatever grain two
    // photographs carry and whatever ceiling an axis publishes, the two functions together can
    // never write a pose past that axis's own ceiling, and never below the level the grain asks
    // for unless the grain asks for more than the ceiling holds. Stated as functions, that is
    // checkable over the whole span of numbers either argument can take, which is the only span
    // there is; a collection of photographs is one arbitrary handful of points inside it and
    // proves nothing about the rest.
    //
    // THE FLOOR IS PER AXIS, AND THAT IS THE WHOLE POINT OF THE `ceiling` ARGUMENT. A camera
    // excursion reads once the frame's own edge travels by at least ONE element of the pair's finer
    // grain. A rotation of θ about the frame's centre carries a point at the edge — half a frame
    // out — through θ · 0.5, so the excursion the grain asks for is θ ≥ 2 · grainFrac, an ANGLE.
    // An axis is written here as a SHARE of its own ceiling, so that same angle is a different
    // share on each axis: the share is 2 · grainFrac / (that axis's own ceiling), and an axis whose
    // ceiling is half of another's needs twice the share to travel the same angle. Handing the
    // ceiling in is what keeps that true for every axis instead of for the widest one only.
    //
    // WHY THE CLAMP IS THE HONEST ANSWER AT THE TOP. Where 2 · grainFrac exceeds the ceiling itself
    // the pair is asking for an excursion the axis is not allowed to make. The floor is held at 1 —
    // the axis flies to its own published ceiling and no further. That is a bound the camera lane
    // publishes, not a refusal: the passage still plays, and shelf 9's law is kept because nothing
    // is declined.
    //
    // THE FLOOR IS THE CLASS AND THE CAMERA IS ONE CASE OF IT (2026-08-24, on his word that the
    // colour voices have never once been seen). Every counted voice of shelf 17 has the same shape:
    // the voice writes on some handle with a published ceiling, there is a LEVEL below which nothing
    // of it can be read, and the pair's own reading says how far above that level it stands. Only
    // the level differs — an angle for the camera, a loudness for the colour and light voices, a
    // reach for the composite. So the arithmetic is stated once, in the general terms, and each lane
    // hands in its own level and its own ceiling. `voiceFloor` is that arithmetic; `camVoiceFloor`
    // is the camera's own level (`2 · grainFrac`, derived in the paragraphs above) put through it.
    function voiceFloor(needed, ceiling) {
      return (needed > 0 && ceiling > 0) ? clamp01(needed / ceiling) : 0;
    }
    function camVoiceFloor(grainFrac, ceiling) {
      return voiceFloor(2 * grainFrac, ceiling);
    }
    // WHAT THE LIFT IS, AND WHY IT CANNOT OVERSHOOT. The reading `share` is the pair's own call on
    // this axis, already a share of that axis's own ceiling and so already in [0, 1] by each axis's
    // own derivation. The lifted share is `floor + (1 − floor) · share`: the floor takes the bottom
    // of the span and the reading spends what is left of it. Read as a function of `share` with
    // `floor` fixed in [0, 1], it is a line from `floor` at share 0 to exactly 1 at share 1 —
    // increasing, so the readings still RANK; bounded below by `floor`, so the level is always
    // cleared; and bounded above by 1, so the pose never passes the axis's own ceiling. No input
    // can break either bound, because both endpoints of a straight line are inside [0, 1] whenever
    // `floor` is, and `clamp01` in `camVoiceFloor` is what makes `floor` so.
    //
    // IT IS RETURNED AS A MULTIPLIER rather than as the lifted share itself, so the caller can
    // scale a signed magnitude and carry every sign, every arc and every outbound-to-inbound
    // fraction through untouched. `magnitude = share · ceiling`, so `magnitude · lift` is exactly
    // `(floor + (1 − floor) · share) · ceiling` — the lifted share times the same ceiling, hence
    // at most the ceiling itself. Where there is no floor to clear, or no excursion to lift, the
    // multiplier is 1 and nothing moves.
    //
    // AND THE LIFT WAS ALREADY THE CLASS — nothing in it is a camera. It is written under the
    // general name from here, and the camera's own name stays bound to it so the lane below and the
    // module's own handed-out arithmetic both go on reading what they always read.
    // `voiceReach` IS THE LINE ITSELF and `voiceLift` is the same line handed back as a multiplier.
    // A lane that carries a signed magnitude (the camera's three axes) wants the multiplier so every
    // sign and every fraction rides through untouched; a lane that writes the share straight onto a
    // handle wants the line. They are one function read two ways, so neither lane can drift from the
    // other, and the multiplier form is exactly `voiceReach / share` wherever that division is safe.
    function voiceReach(floor, share) {
      return floor + (1 - floor) * clamp01(share);
    }
    function voiceLift(floor, share) {
      return (floor > 0 && share > 0) ? voiceReach(floor, share) / share : 1;
    }
    var camVoiceLift = voiceLift;

    // ---- the pair, derived from the two works rather than looked up ----

    // HOW STRONGLY A PAIR HOLDS EACH MEASURE — one reading per measure, and no verdict of any kind.
    //
    // The strength is the WEAKER of the two works' readings, which is the plainest honest answer to
    // «how much of this do the two photographs have between them»: a ground is only as good as the
    // end that carries it least. Every measure is present in every answer, and every one of them is
    // a candidate ground for every pair; the strength says which to reach for first.
    //
    // WHAT WENT, AND WHY IT COULD NEVER HAVE BEEN RIGHT. Two verdicts stood beside this reading.
    // `both` asked whether both works cleared the measure's discriminating threshold — a cut taken
    // over one collection of photographs. An admission test compares a pair's own reading against a
    // number derived from OTHER photographs, so it answers how a reading stands among strangers when
    // what is asked is how these two stand to each other; and both works having to clear it made the
    // ground scarcer than either work's own reading ever was, so pairs fell past every shared measure
    // onto one nominated ground with one cut and one instrument. `usable` asked whether both cleared
    // the measure's typed cut-line floor. Between them they turned a ranking question into an
    // admission test, which is the disease his word of 09:51 names. Both numbers were in hand all
    // along and the third was never a better answer to a question it does not ask. Both are gone;
    // what is left is the number itself.
    function groundReadings(a, b) {
      var per = {}, i, m, sa, sb;
      for (i = 0; i < MEASURES.length; i++) {
        m = MEASURES[i];
        sa = readingOf((a.measures || {})[m]);
        sb = readingOf((b.measures || {})[m]);
        per[m] = { min: r4(Math.min(sa, sb)), a: r4(sa), b: r4(sb) };
      }
      return { per: per };
    }

    // THE FOUR INSTRUMENTS THAT FOLD THE SPACE A WORK LIVES IN — shelf 8's folded space, the same
    // event shelf 6 says consumes the crossing's one miracle and never stacks. Naряд S-18
    // (2026-08-27) moves this off the manifest's shared `levels` array on purpose: that array also
    // carries shelf 17's own camera-ownership law, which several of these four handles genuinely
    // still need (their handles are declared at the WORLD level there, and `ownTheLevels` reads
    // that declaration to grant them the camera at all — stripping it would leave the fold itself
    // undriven, not merely uncounted). What moves is only the READING of «is this a fold», onto
    // the instrument's own identity — the box a picture folds into, the little world it curls into
    // (charter shelf 8's own ontology shift), the plane a frame lies down into, and the landscape a
    // frame opens into — kept here, beside the function it feeds, rather than smuggled through a
    // field that answers a different law.
    var WORLD_FOLD_INSTRUMENTS = ["boxfold", "planet", "tilt", "waterline"];
    function isWorldFold(iid) {
      return !!iid && WORLD_FOLD_INSTRUMENTS.indexOf(iid) >= 0;
    }

    // AN INSTRUMENT THAT FOLDS THE SPACE A WORK LIVES IN SPENDS THE CROSSING'S ONE MIRACLE — THE
    // FIRST TIME THIS WALK PLAYS IT. His word of 2026-08-26 20:17: a miracle is a wow, a concept,
    // it is subjective, and «если много раз повторяется то уже не чудо» — repeated, it stops being
    // one. So this no longer reads a mark true for the instrument's whole life on the site: it
    // reads `walkMiracles`, this composition's own reading of what the walk has already played
    // (set by `scoreFor`, exactly as `walkPlayed` is, from `01a-pass.js`'s `passWalkMiracles`). The
    // first time a fold plays on a walk it is the miracle; every repeat is an ordinary letter, and
    // the slot it no longer spends is free for another move in the same crossing. `isWorldFold`
    // above is unaffected by any of this — a road built around the fold (`mustFold`) still finds
    // the instrument that fold IS, whether or not this walk has already spent the miracle on it.
    function spendsTheMiracle(iid) {
      return isWorldFold(iid) && walkMiracles.indexOf(iid) < 0;
    }

    // Every instrument this collection publishes that cuts on a kind, in one settled order.
    function instrumentsOfKind(kind) {
      return (kind && CUTS_ON[kind]) ? CUTS_ON[kind] : [];
    }

    // Every instrument the collection publishes at all, in one settled order.
    var ALL_INSTRUMENTS = Object.keys(INSTRUMENTS).sort().filter(function (iid) {
      return !!MANIFESTS[iid];
    });

    // ---------------------------------------------------------------------------------------
    // HOW WELL AN INSTRUMENT SUITS A PAIR — the new shape of an instrument's answer
    // ---------------------------------------------------------------------------------------
    //
    // AN INSTRUMENT NO LONGER ANSWERS WHETHER IT TAKES A PAIR. It answers HOW WELL IT SUITS one, as
    // a reading between nothing and whole, with a sentence saying what it read. His word of
    // 2026-08-18 09:53: a measurement ranks which genre of crossing suits a pair and sets the
    // parameters inside the genre that wins — it never admits and it never rejects.
    //
    // THE SHAPE, so a port in flight can be brought to it: `suits(a, b) -> [fit, why]`, where
    //   fit  a number in 0…1. Nothing means this pair gives the instrument nothing to work with;
    //        whole means the pair is exactly what the instrument is for. A fit of nothing is still
    //        playable — it ranks last, and where every fit is nothing the die is even and something
    //        plays anyway.
    //   why  one sentence in the instrument's own terms, naming the readings it took. It travels on
    //        the plan whatever the fit, so a modest crossing explains itself the same way a strong
    //        one does.
    // The reading is of the PAIR and carries no direction, so the same instrument suits an edge
    // equally whichever way the visitor walks it; a return therefore casts as its outward pass did.
    //
    // WHAT THIS REPLACES. `INSTRUMENT_ASKS` returned [true|false, why]: the fold demanded a region
    // score over a typed floor and four faces, the parquet a device confidence over a typed 0.5.
    // A pair failing either was refused the instrument, and where it was the only one cutting the
    // ground's kind the whole crossing was refused with it. Both conditions were real readings
    // wearing an admission test's clothes — they are kept, in full, as the fit itself.
    var INSTRUMENT_SUITS = {
      // THE FOLD IS AN IMPOSSIBLE EVENT and it is placed on a work's own region line, so what it
      // suits is a pair one of whose works falls plainly into panels. The reading is the region
      // score of the better-divided work, and it is nothing where neither work offers a panel to
      // fold — which is structural rather than a floor: a solid with one face is no solid.
      boxfold: function (a, b) {
        var best = Math.max(readingOf(((a.structure || {}).regions || {}).score),
                            readingOf(((b.structure || {}).regions || {}).score));
        var faces = Math.max(facesOf(a), facesOf(b));
        if (faces < 2) {
          return [0, "neither work cuts into panels a solid could be built from, so the fold has "
                  + "nothing to crease; it reads regions at " + pyText(flt(r4(best)))];
        }
        return [best, "a work of the pair reads regions at " + pyText(flt(r4(best)))
                + " over " + faces + " faces"];
      },
      // THE PARQUET REVEALS HOW A WORK WAS MADE — his 19:13 word makes that a register of its own —
      // so what it suits is a pair whose making READS: the work's own device, the step it was cut at
      // and how confidently that step was recovered. The confidence IS the fit, which is what a
      // confidence is for; where no step was recovered there is nothing to open on.
      unfold: function (a, b) {
        var da = (a.structure || {}).ownDevice || {}, db = (b.structure || {}).ownDevice || {};
        var ca = readingOf(da.confidence), cb = readingOf(db.confidence);
        var dev = ca >= cb ? da : db, conf = Math.max(ca, cb);
        var step = Number(dev.stepPx) || 0;
        if (!(step > 0)) {
          return [0, "neither work carries a measured step of its own to open on"];
        }
        return [conf, "a work of the pair was cut as " + pyText(dev.kind || "a device")
                + " at a step of " + pyText(flt(r4(step))) + " px, read at "
                + pyText(flt(r4(conf)))];
      },
      // THE WATER IS ONE SHEET CARRYING TWO PICTURES, and the sheet is its own. All three handles
      // the composer drives on it read one family: how much of a work reads as grain rather than as
      // line (the swell), its own spectral period (where the crests stand) and its finest detail
      // (how far the water bends the light). So the fit is that family read on the pair.
      //
      // THE STRONGER END CARRIES IT, and the instrument's own construction is why. The swell TRAVELS
      // from the departing work's reading to the arriving one's — the water deepens or shallows
      // across the crossing — so the pair needs grain for the water to work with rather than grain
      // at both ends: a straight architecture under a swell the other work sets is the crossing,
      // not a failure of it. Its port says the same in its own words: water asks nothing of a pair
      // beyond that it have a ground at all, every photograph can be under water.
      //
      // WHAT STOOD HERE WAS NOTHING AT ALL. This instrument published no row, so `suitsPair` below
      // answered for it with its typed 0.5 on every pair alike. A constant reads neither record, so
      // its output is independent of both inputs over the WHOLE input space: it ranks identically
      // against every rival on every pair there can ever be, above the measured readings of
      // `overlay`, `tunnel` and `weave` wherever theirs fall under a half and below them wherever
      // they do not — permanently, and on no evidence either way. That is the defect whole, and how
      // often it was reached adds nothing to it. His word of 2026-08-18 15:13 names the class: no
      // static transitions.
      liquid: function (a, b) {
        var sa = readingOf((a.measures || {}).texture);
        var sb = readingOf((b.measures || {}).texture);
        return [Math.max(sa, sb), "the two works read as grain rather than as line at "
                + pyText(flt(r4(sa))) + " and " + pyText(flt(r4(sb)))
                + ", and the swell travels out to the deeper of the two"];
      },
      // A POUR NEEDS A PICTURE THAT WILL LET GO AND A MATERIAL TO HEAP. The departing work's own
      // region line says how plainly it comes apart into streams — a work that falls into regions
      // pours in streams, one that reads as a single mass drops all at once. And the two works'
      // detail scales say whether the material that FALLS is the material that HEAPS: the heap is
      // the arriving work and the stream is the departing one, so a pair whose grains stand close
      // reads as one substance changing rather than two pictures swapped. The reading is the mean
      // of the two, and where neither work carries a detail reading the second half reads nothing
      // rather than the whole it would read by default.
      pour: function (a, b) {
        var reg = readingOf(((a.structure || {}).regions || {}).score);
        var da = Number((a.texture || {}).detailPx) || 0;
        var db = Number((b.texture || {}).detailPx) || 0;
        var scales = (da > 0 && db > 0) ? tonalSpectral(a, b).spectral : 0;
        return [clamp01((reg + scales) / 2),
                "the departing work's own region line reads " + pyText(flt(r4(reg)))
                + ", so it comes apart in that many streams, and the two works' detail scales "
                + "stand at " + pyText(flt(r4(scales))) + " of each other, so the material that "
                + "falls is the material that heaps"];
      },
      // A VEIL IS WORTH WATCHING WHERE A WORK HAS SOMETHING TO LOSE TO IT. What the veil does to a
      // photograph is read it at a coarser scale of its own material, so the two works' own grain
      // readings say how much there is to take away — and the stronger end carries it, because the
      // works trade depths and one work with material in it is enough to make the coming-forward
      // read. How far apart their detail scales stand says how much passing each sheet actually
      // changes: two works of one grain would come forward through the same weather twice.
      veil: function (a, b) {
        var ga = readingOf((a.measures || {}).texture);
        var gb = readingOf((b.measures || {}).texture);
        var va = Number((a.texture || {}).detailPx) || 0;
        var vb = Number((b.texture || {}).detailPx) || 0;
        var apart = (va > 0 && vb > 0) ? 1 - tonalSpectral(a, b).spectral : 0;
        return [clamp01((Math.max(ga, gb) + apart) / 2),
                "the works read as grain rather than as line at " + pyText(flt(r4(ga))) + " and "
                + pyText(flt(r4(gb))) + ", which is what a coarsening has to take away, and their "
                + "detail scales stand " + pyText(flt(r4(apart))) + " apart, which is how much "
                + "coming forward through the sheets actually changes"];
      },
      // THE AIR CATCHES WHAT BANDS. The two works' own banding readings say how much row structure
      // there is for a gust to take, and the STRONGER end carries it — the front travels from one
      // work's rows to the other's, so one work of plain rows is enough to watch the air bend
      // something. How far apart their two lattices stand says whether the front comes in ACROSS
      // the picture's own grain, which is what makes a gust read as air rather than as a wipe.
      //
      // THE SECOND HALF IS READ ONLY WHERE BOTH WORKS CARRY A LATTICE AT ALL. An angle of zero is
      // a lattice running square, so `Number(...) || 0` cannot tell a measured horizontal grain
      // from a work that was never measured for one, and the gap between a real angle and an
      // absent one would be a reading of nothing dressed as a reading of half a right angle. The
      // work's own lattice PERIOD says whether the angle beside it is a measurement — the grid's
      // period first and the device's step where no grid period was derived, which is the order
      // this file's own fill branches already prefer them in. Where either work carries neither,
      // this half reads nothing and the pair ranks by its banding alone; nothing is turned away.
      wind: function (a, b) {
        var sa = readingOf(((a.structure || {}).banding || {}).score);
        var sb = readingOf(((b.structure || {}).banding || {}).score);
        function latticeOf(w) {
          var st = w.structure || {}, g = st.grid || {}, d = st.ownDevice || {};
          if (Number(g.periodPx) > 0) return Number(g.angleDeg) || 0;
          if (Number(d.stepPx) > 0) return Number(d.angleDeg) || 0;
          return null;
        }
        var aa = latticeOf(a), ab = latticeOf(b), across = 0;
        if (aa !== null && ab !== null) {
          var gap = (((aa - ab) % 180) + 180) % 180;
          across = Math.min(gap, 180 - gap) / 90;
        }
        return [clamp01((Math.max(sa, sb) + across) / 2),
                "the two works read banding at " + pyText(flt(r4(sa))) + " and "
                + pyText(flt(r4(sb))) + ", so the air has rows to catch at the stronger end, and "
                + "their two lattices stand " + pyText(flt(r4(across))) + " of a right angle "
                + "apart, which is how far across the picture's own grain the front comes in"];
      },
      // THE FLOOR IS TWO ROOMS AND THE CROSSING IS THE HANDOVER BETWEEN THEM. Both works are laid on
      // one mirrored floor tile for tile and the room changes hands as each sheet turns up, so what
      // the pair gives this instrument is TWO tile counts — and where they are the same count the
      // floor turns over into itself and there is nothing to watch. The count is the one the
      // instrument's own `tiles` handle is published in, taken the way its fill already takes it:
      // the work's own frame side over `structure.grid.periodPx`, and over
      // `structure.ownDevice.stepPx` where no grid period was derived. The order follows from the
      // two measurements' own resolutions: a device step is quantised to the device's own repeat, so
      // its range is coarser than the grid period's by construction, and reading the coarser one
      // first puts more works on one value whatever the works are. A floor laid from the coarser
      // reading is therefore the same floor more often, which is this same law read one level down,
      // at the parameter rather than at the choice.
      //
      // The distance is said across the handle's OWN published span, so nothing here invents a
      // scale. This instrument published no row either, and carried the same typed 0.5.
      parquet: function (a, b) {
        function floorOf(w) {
          var st = w.structure || {}, side = Number(w.frameSide) || 0;
          var step = Number((st.grid || {}).periodPx) || Number((st.ownDevice || {}).stepPx) || 0;
          var lo = num(HANDLE_SPECS.parquet.tiles[0]), hi = num(HANDLE_SPECS.parquet.tiles[1]);
          if (!(side > 0 && step > 0)) return num(HANDLE_SPECS.parquet.tiles[2]);
          return Math.min(hi, Math.max(lo, side / step));
        }
        var fa = floorOf(a), fb = floorOf(b);
        var span = num(HANDLE_SPECS.parquet.tiles[1]) - num(HANDLE_SPECS.parquet.tiles[0]);
        return [span > 0 ? Math.abs(fa - fb) / span : 0,
                "the two works cut their own floors into " + pyText(flt(r4(fa))) + " and "
                + pyText(flt(r4(fb))) + " tiles across, and the room changes hands by the "
                + "distance between them"];
      },
      // THE RIBBONS RUN ALONG A BAND FAMILY, so the weave suits a pair that both works band. The
      // weaker of the two readings is the fit, because a fabric is only as woven as its thinner end.
      //
      // THE WEAKER STAYS, AND THE INSTRUMENT'S OWN FILL IS THE REASON (2026-08-18, the choice sweep).
      // The min was read as a defeat by construction against `livemirror`'s max on the same family;
      // it is not one here, because this crossing genuinely needs both ends. The strip COUNT travels
      // from the departing work's family to the arriving one's — `nMul` is the ratio of the two
      // measured counts and it is written only where both carry one — and the fabric's speed is read
      // off that same count. The charter's own words for the alternative stand in that branch: a
      // bridge playing only one work's structure reads as artificial. So a fabric IS only as woven
      // as its thinner end, and the reading says what the picture does.
      weave: function (a, b) {
        var sa = readingOf(((a.structure || {}).banding || {}).score);
        var sb = readingOf(((b.structure || {}).banding || {}).score);
        return [Math.min(sa, sb), "the two works read banding at " + pyText(flt(r4(sa)))
                + " and " + pyText(flt(r4(sb)))];
      },
      // THE MESH TURNS ON RINGS AND WEDGES, so what it suits is a pair that reads radial at both
      // ends — a mesh played on one work's centre alone reads as laid on rather than found.
      //
      // THE WEAKER STAYS, AND THE INSTRUMENT'S OWN FILL IS THE REASON (2026-08-18, the choice sweep).
      // Every geometric handle of this instrument is a PAIR of ends and each end is one work's own
      // reading: how hard the wheels turn is the two radial scores, how far apart the teeth's own
      // moments stand is the golden-angle stagger of the two measured ring grains, how far a tooth
      // stands out of its pitch circle is the two ring merges, and the ratio and the size come off
      // the two measured ring counts together. A work reading nothing radial stops the mesh dead at
      // its own end of the crossing, so the pair is as meshed as its weaker end and the reading is
      // the honest one. It loses to the glass's and the spiral's max on the same number by
      // construction, and that is what it should do: those two rest on one point and this one turns
      // on two.
      gears: function (a, b) {
        var sa = readingOf(((a.structure || {}).radial || {}).score);
        var sb = readingOf(((b.structure || {}).radial || {}).score);
        return [Math.min(sa, sb), "the two works read radial at " + pyText(flt(r4(sa)))
                + " and " + pyText(flt(r4(sb)))];
      },
      // THE MATERIAL INSTRUMENT HANDS ONE TONAL WORLD AND ONE DETAIL SCALE OVER TO ANOTHER, so it
      // suits a pair whose two grounds stand close enough for the handover to read as one substance
      // changing rather than two pictures swapped. Both readings are of the pair by construction,
      // which is why this instrument suits every pair somewhat and no pair absolutely.
      matter: function (a, b) {
        var bridge = tonalSpectral(a, b);
        return [Math.min(bridge.tonal, bridge.spectral),
                "the two works' tonal grounds stand at " + pyText(flt(r4(bridge.tonal)))
                + " of each other and their detail scales at " + pyText(flt(r4(bridge.spectral)))];
      },
      // THE READY STORY IS A WHOLE PASSAGE IN ONE VOICE: the folds take the departing work apart
      // about its own measured centre, the rose window and the planet are where neither work is
      // legible, and the road walked back puts the arriving work together. How far that story
      // travels is a measurement — a pair that reads nothing polar turns back at the window and one
      // that reads it goes all the way to the planet — so the polar reading IS the fit, and the
      // stronger of the two works carries it, because one story is told about one centre.
      //
      // The port drafted this as [false, …] below `DEVICE_LEGIBLE` — the composer's own 0.5, which
      // `always` has since struck out of this file under his 09:53 word. The reading survives the
      // number: how far the story goes was never a question of admission, and the lane's own
      // sentence says so.
      hero: function (a, b) {
        var pa = readingOf(((a.structure || {}).polar || {}).planet);
        var pb = readingOf(((b.structure || {}).polar || {}).planet);
        return [Math.max(pa, pb), "the two works read as a planet at " + pyText(flt(r4(pa)))
                + " and " + pyText(flt(r4(pb))) + ", and the story travels as far out as the "
                + "stronger reading carries it"];
      },
      // THE THIRD PICTURE IS MADE OF TWO PALETTES, so what it suits is a pair whose two colours
      // stand APART: where the two works carry nearly one colour the composite is one work slightly
      // veiled and there is nothing to watch. The tonal bridge already in this file — a closeness
      // of the works' own measured tone, `luminance.level` since the judge seat's standing
      // correction of 2026-08-18/19 — stands in for the colour distance the lane said it was
      // waiting on, and the distance is its complement.
      //
      // The second half is charter shelf 10's: the third picture is the two works' INTERFERENCE, so
      // a pair carrying a measured lattice at one end at least has something to beat against, and
      // a pair carrying two beats hardest. The lane drafted this half as a floor on a measured step;
      // it is a ranking here, so a pair with no lattice anywhere still crosses and simply ranks
      // below one that has both.
      overlay: function (a, b) {
        var apart = 1 - tonalSpectral(a, b).tonal;
        var la = latticeOf(a) > 0 ? 1 : 0, lb = latticeOf(b) > 0 ? 1 : 0;
        var beat = (la + lb) / 2;
        return [apart * (0.5 + 0.5 * beat),
                "the two works' colour worlds stand " + pyText(flt(r4(apart)))
                + " apart, and " + (la + lb) + " of the two carry a measured lattice for the "
                + "third picture to beat against"];
      },
      // THE PICTURE CURLS INTO A LITTLE WORLD, and a world needs a horizon: the foot goes to the
      // centre, the sky becomes the ring and the light the whole stage stands in. A flat pattern
      // with no horizon curls into a disc of texture instead, which is a lesser thing. So the
      // reading is the world reading itself — how much of a sphere or a corridor the work already
      // is — held back where it reads more as a log-spiral (that is the spiral's world, not this
      // one) and held back again where no horizon was measured. ONE work is enough, because one
      // world is what the crossing curls into.
      //
      // The port wrote its ask as a pure function on the instrument that DECLINED the pair unless
      // one work answered all three questions, over a borrowed `WORLD_FLOOR = 0.20` its own report
      // says nobody measured for the polar readings. His words of 2026-08-18 08:47 and 09:53 strike
      // the floor and the decline together, and every one of the three questions survives as what
      // it always was: a reading that ranks. The two that were gates become MULTIPLIERS on the
      // world reading, so a pair with no horizon ranks the world below its rivals and still crosses.
      planet: function (a, b) {
        function worldOf(w) {
          var p = (w.structure || {}).polar || {};
          var world = Math.max(readingOf(p.planet), readingOf(p.tunnel));
          var twirl = readingOf(p.twirl);
          // the log-spiral's share of the same family, taken off rather than tested against: a work
          // reading equally as both is half a world here, and one reading only as a spiral is none.
          var mine = (world + twirl) > 0 ? world / (world + twirl) : 0;
          var hz = ((w.structure || {}).horizon || {}).y;
          var hasHorizon = (hz !== null && hz !== undefined);
          return world * mine * (hasHorizon ? 1 : 0.5);
        }
        var wa = worldOf(a), wb = worldOf(b);
        return [Math.max(wa, wb), "the two works read as little worlds of their own at "
                + pyText(flt(r4(wa))) + " and " + pyText(flt(r4(wb)))
                + " once the log-spiral's share of the same reading and a missing horizon are "
                + "taken off, and the crossing curls into the stronger"];
      },
      // THE MIRROR NEEDS A LINE TO FOLD ON, and the picture has to put that line where it is. It
      // cuts on panels — the fold partitions the frame into two or four mirrored ones — and the
      // fold lies ALONG the work's own structure rather than across it. So what it suits is a pair
      // carrying a line at all, and a line is whichever of the three readings speaks loudest: the
      // radial, the banding or the region score. ONE work is enough, because one fold has one line.
      //
      // The port drafted this as `[false, …]` where the strongest of those three readings fell
      // under the weakest of their three floors, and said in the same breath that on this
      // collection the ask declines nothing — which is what an admission test looks like when it
      // has nothing to admit. His word of 2026-08-18 09:53 keeps the reading and strikes both the
      // floor and the refusal: the strongest line the pair carries is the fit.
      livemirror: function (a, b) {
        function lineOf(w) {
          var s = w.structure || {};
          return Math.max(readingOf((s.radial || {}).score),
                          readingOf((s.banding || {}).score),
                          readingOf((s.regions || {}).score));
        }
        var la = lineOf(a), lb = lineOf(b);
        return [Math.max(la, lb), "the strongest line the two works carry — the loudest of each "
                + "one's radial, banding and region readings — stands at " + pyText(flt(r4(la)))
                + " and " + pyText(flt(r4(lb))) + ", and the fold lands along the stronger"];
      },
      // THE SPIRAL HAS A THROAT, AND THE THROAT STANDS WHERE THE PHOTOGRAPH PUTS IT. The copies are
      // annuli about a work's own measured radial centre: rings become the copies and spokes become
      // the spiral once the shear turns them, so what it suits is a pair one of whose works reads
      // radial. ONE work is enough and that is structural — a spiral has one throat and falls into
      // one centre, so the STRONGER of the two readings is the fit rather than the weaker.
      //
      // The port drafted this as a floor on `radial_tight`, returning [false, …] for every pair
      // under it and refusing the whole crossing where nothing else cut the ground's kind. His word
      // of 2026-08-18 09:53 keeps the reading and strikes the refusal: the reading was always the
      // useful half, and a pair with nothing radial simply ranks the spiral below its rivals.
      droste: function (a, b) {
        var sa = readingOf(((a.structure || {}).radial || {}).score);
        var sb = readingOf(((b.structure || {}).radial || {}).score);
        return [Math.max(sa, sb), "the two works read radial at " + pyText(flt(r4(sa)))
                + " and " + pyText(flt(r4(sb))) + ", and the dive falls into the stronger "
                + "one's own centre"];
      },
      // THE DRIFTING INSTRUMENT CUTS ON NAMED REGIONS — the things in the picture rather than the
      // pieces of the frame — so it suits a pair both of whose works carry named objects. The row
      // stands whether or not this collection publishes the instrument today: a landing instrument
      // joins the ranking by arriving, and it arrives with its reading already written.
      adrift: function (a, b) {
        var sa = readingOf((a.measures || {}).named_objects);
        var sb = readingOf((b.measures || {}).named_objects);
        return [Math.min(sa, sb), "the two works read named objects at " + pyText(flt(r4(sa)))
                + " and " + pyText(flt(r4(sb)))];
      },
      // THE WEDGE TILES OUTWARD INTO MIRRORED RINGS about ONE measured centre, so what it suits is a
      // pair that HAS the structure rather than a pair that carries it at both ends — and the fit is
      // the STRONGER reading, as the glass's and the spiral's are.
      //
      // WHAT WENT, AND WHAT THE INSTRUMENT'S OWN FILL SAYS. This read the WEAKER of the two radial
      // scores, on the sentence «a fold opening a structure only one work carries is laid on rather
      // than found» — and its own fill contradicts that sentence line for line. The wedge count is
      // the LARGER of the two measured rotational orders, the ring count the LARGER of the two
      // device counts, and the centre one point midway between the two: one rosette, taken from
      // whichever work carries the structure. Only the lean and the sample width travel end to end.
      // An instrument whose geometry is read off the stronger work cannot be RANKED by the weaker
      // one; the min against a rival's max on the same number is a loss by construction rather than
      // by merit — the minimum of two readings can never exceed the maximum of the same two, so the
      // fold could not hold the top of the reading on ANY pair whatever, not merely on the ones on
      // disk.
      //
      // WHAT ALSO WENT IS A TYPED HALF. The rings-against-spokes reading is the instrument's own —
      // rings open into a rosette and spokes turn instead, which is the same reading the genre
      // vocabulary tells the rosette and the spin apart by — but it stood as «× (0.5 + 0.5·rings)»,
      // a multiplier nobody measured, and it was what put this instrument behind the mesh on every
      // pair of the collection. His word of 2026-08-18 13:41 strikes an invented number. The
      // reading survives it whole and reads plainly instead: the fold opens out of the works that
      // turn on rings, so the strongest RING reading the pair carries is the fit, and a pair whose
      // two works both turn on spokes gives the rosette nothing — which ranks it last and plays it
      // anyway.
      //
      // The port declared this on its own manifest as two FLOORS and a direction: both works over
      // the collection's cut-line floor, the ARRIVING work over the tight floor with its subtype on
      // rings. All three go under his words of 09:51 and 09:53 and the reading survives all three.
      kaleidoscope: function (a, b) {
        function ringly(w) {
          return ((w.structure || {}).radial || {}).subType === "ring" ? 1 : 0;
        }
        var sa = readingOf(((a.structure || {}).radial || {}).score) * ringly(a);
        var sb = readingOf(((b.structure || {}).radial || {}).score) * ringly(b);
        return [Math.max(sa, sb), "the two works turn on rings at " + pyText(flt(r4(sa)))
                + " and " + pyText(flt(r4(sb))) + " — a work turning on spokes reads nothing here, "
                + "because spokes turn where rings open — and the rosette opens out of the stronger"];
      },
      // THE GLASS RESTS ON A POINT AND FOLDS ABOUT IT, so what it suits is a pair whose point is
      // the works' OWN: its place, its wedge count and its wind are all set about the pair's
      // measured radial centre, and where neither work reads radial that centre is a made-up point
      // rather than a reading. The reading is of the PAIR and carries no direction, so the glass
      // suits an edge the same whichever way the visitor walks it.
      //
      // The port drafted this as [false, …] below the collection's own tight radial floor, and the
      // draft would not have run at all: `suitsPair` hands an instrument two work records and
      // nothing else, so the floors it read would have been undefined and every pair casting the
      // glass would have thrown. The collection's floors are not read by this file in any case —
      // struck all ten under his 09:51 word, because a cut over some collection answers how a
      // reading stands among other photographs when what is asked is how these two stand to each
      // other. So the reading itself is the fit: the stronger radial score, because one glass rests
      // on one point.
      lens: function (a, b) {
        var sa = readingOf(((a.structure || {}).radial || {}).score);
        var sb = readingOf(((b.structure || {}).radial || {}).score);
        return [Math.max(sa, sb), "the two works read radial at " + pyText(flt(r4(sa))) + " and "
                + pyText(flt(r4(sb))) + ", and the glass rests on the point the stronger one's own "
                + "structure turns about"];
      },
      // THE CORRIDOR TAKES THE EYE INTO THE PICTURE'S OWN DEPTH, which is a different act from the
      // mesh turning rings against each other on the surface — two instruments cut on rings and
      // this is what tells them apart. So what it suits is a pair whose depth is there to be
      // entered, and the collection measures that directly: how strongly each work reads as a
      // corridor, and how much of that work's own depth reading the corridor IS rather than the
      // sphere or the log-spiral, since a photograph whose depth reads as a sphere should become a
      // planet instead. Both are of the pair, read on both works, with no direction on either.
      //
      // The port drafted this as [false, …] where neither work read the corridor as its strongest
      // depth over `floors.radial` — an admission test on two counts, and it would not have run
      // either: `suitsPair` hands an instrument two work records and no floors. His words of 09:51
      // and 09:53 strike the refusal; both readings survive, the second as the share it always was.
      tunnel: function (a, b) {
        function corridorOf(w) {
          var p = (w.structure || {}).polar || {};
          var mine = readingOf(p.tunnel);
          var whole = mine + readingOf(p.planet) + readingOf(p.twirl);
          var share = whole > 0 ? mine / whole : 0;
          return mine * share;
        }
        var ca = corridorOf(a), cb = corridorOf(b);
        return [Math.max(ca, cb), "the two works read as a corridor of their own at "
                + pyText(flt(r4(ca))) + " and " + pyText(flt(r4(cb)))
                + " once the sphere's and the log-spiral's share of the same depth is taken off, "
                + "and the eye travels into the stronger"];
      },
      // ---- THE ARSENAL LANE, 2026-08-18, on his word of 18:39 ----------------------------------
      // Six instruments carried across from lab/effects/, each ranking the pair on exactly the
      // measurements its own manifest's `suits.reads` names. Every one of them is a READING and
      // none of them can turn a pair away: his words of 09:51, 09:53 and 10:15 — any two
      // photographs in the world get a crossing, and a measurement only ranks which genre suits.
      // Where a reading comes out at nothing the sentence says what the pair will get instead.

      // THE THIRD PICTURE IS THE TWO WORKS' INTERFERENCE (charter shelf 10), so what this suits is
      // a pair whose own measured rhythms stand near one another: two nearly equal periods beat
      // into large slow lobes, and that envelope is the only structure here big enough to read as
      // a shape. The periods are said as counts across each work's own frame, which is the unit
      // that makes two differently-sized files comparable at all.
      beat: function (a, b) {
        function cellsOf(w) {
          var p = Number(((w || {}).texture || {}).spectralPeriodPx) || 0;
          var side = Number((w || {}).frameSide) || 0;
          return (p > 0 && side > 0) ? side / p : 0;
        }
        var ca = cellsOf(a), cb = cellsOf(b);
        if (!(ca > 0) || !(cb > 0)) {
          return [0, "one of the works carries no measured rhythm of its own, so the two gratings "
                  + "stand at the module's own periods and the handover reads fine and fast"];
        }
        var near = Math.min(ca, cb) / Math.max(ca, cb);
        return [near, "the two works' own rhythms read as " + pyText(flt(r4(ca))) + " and "
                + pyText(flt(r4(cb))) + " cells across their own frames, so their periods stand at "
                + pyText(flt(r4(near))) + " of each other — the nearer they stand the coarser and "
                + "slower the lobes the frame changes hands in"];
      },
      // THE DEPARTING WORK'S OWN SLOT IS WHAT PARTS, and the motif is measured directly:
      // lab/step1-motifs.py reads ворота off one picture's own pixels, and every work's record
      // carries its own `motifs.gateGap`. The fit is that reading. Where a work carries no gate the
      // fit is nothing and the slot stands in the middle of the frame at the motif's own band
      // width, which is the module's own answer for a source with no gate — a plainer crossing,
      // never a refused one.
      gates: function (a, b) {
        function gapOf(w) {
          var mot = (w || {}).motifs || {};
          var named = (mot.measured || []).indexOf(MOTIF_GATE) >= 0;
          var gap = readingOf(mot.gateGap);
          return named ? Math.max(gap, 0) : gap;
        }
        var ga = gapOf(a), gb = gapOf(b);
        var best = Math.max(ga, gb);
        if (!(best > 0)) {
          return [0, "neither work carries a measured gate, so the leaves part on the frame's own "
                  + "middle at the motif's own band width"];
        }
        return [best, "a work of the pair reads its own gate at " + pyText(flt(r4(best)))
                + " — the emptiness between two masses the second work comes through"];
      },
      // THE CUT STANDS AT ONE WORK'S OWN STRUCTURE AT THE NEAR DOOR AND AT THE OTHER'S AT THE FAR
      // ONE, so what it suits is a pair by how plainly EACH work publishes a lattice to be cut
      // along. The confidence its own device was recovered at is what that plainness is, and the
      // weaker of the two is the fit, because a bridge is only as good as the end that carries it
      // least. A pair with no measured structure still crosses, on the module's own fallback count.
      "grid-colour": function (a, b) {
        function latticeOf(w) {
          var st = (w || {}).structure || {}, dev = st.ownDevice || {}, grid = st.grid || {};
          if (Number(dev.stepPx) > 0) return readingOf(dev.confidence);
          if (Number(grid.periodPx) > 0) return readingOf(grid.score);
          return 0;
        }
        var la = latticeOf(a), lb = latticeOf(b);
        var fit = Math.min(la, lb);
        if (!(fit > 0)) {
          return [0, "a work of the pair publishes no lattice of its own, so the cut falls to the "
                  + "module's own count and reads as a grid laid over the photograph rather than "
                  + "found in it"];
        }
        return [fit, "the two works wear their own lattices at " + pyText(flt(r4(la))) + " and "
                + pyText(flt(r4(lb))) + ", so the cut leaves one work's own structure and arrives "
                + "at the other's"];
      },
      // EVERY PHOTOGRAPH HAS A TONE TO PART AT, which is charter shelf 12's own sentence about the
      // tonal decomposition: it applies to ANY pair by construction. So this suits every pair
      // somewhat and the reading only ranks how strongly — the further apart the two works stand,
      // the more the parting reads as one tonal world giving way to another rather than as one
      // picture sliding over itself.
      //
      // THE READING, off `luminance.level` — the median of each work's own luminance
      // (lab/analyze/recipes.py:551-613 colour_stats(), carried through build-workrecords-v1.py's
      // record) — the same field the instrument's own threshold handles (`levelA`/`levelB`) are
      // already driven from. `palette.colourfulness` stood here until tonight: it is where a work
      // sits on the collection's own colourfulness ladder, half chroma and half hue spread, and the
      // judge seat's standing correction of 2026-08-18/19 named it as the wrong family for a tonal
      // threshold. `luminance.level` is the genuine tone, so the fit and the handles now read the
      // same field.
      "strata-light": function (a, b) {
        var pa = readingOf((a.luminance || {}).level);
        var pb = readingOf((b.luminance || {}).level);
        var apart = Math.abs(pa - pb);
        return [apart, "the two works stand at " + pyText(flt(r4(pa))) + " and "
                + pyText(flt(r4(pb))) + " on their own measured tone, "
                + pyText(flt(r4(apart))) + " apart — and either way each parts at a level of its "
                + "own, since every photograph has one"];
      },
      // EVERY PHOTOGRAPH HAS BOTH A MASS SCALE AND A DETAIL SCALE OF ITS OWN, the same
      // by-construction reading `strata-light`'s own fit above takes on tone: this suits every pair
      // somewhat and only ranks how strongly, by how far apart the two works stand on how much of
      // their own luminance the mass scale loses — `texture.reliefEdge`, lab/analyze/recipes.py's
      // own port of `measure(image)` in lab/effects/strata-scale.js:138-141, the same field this
      // instrument's own manifest names in its `suits.reads`.
      "strata-scale": function (a, b) {
        var ea = readingOf((a.texture || {}).reliefEdge);
        var eb = readingOf((b.texture || {}).reliefEdge);
        var apart = Math.abs(ea - eb);
        return [apart, "the two works lose " + pyText(flt(r4(ea))) + " and " + pyText(flt(r4(eb)))
                + " of their own luminance to the mass scale, " + pyText(flt(r4(apart)))
                + " apart — and either way each parts into its own masses and its own detail, "
                + "since every photograph carries both"];
      },
      // THE WHOLE FRAME IS LAID DOWN AS ONE PLANE GOING AWAY, so what it suits is a pair with
      // depth to be revealed. The weaker of the two corridor readings is the fit, because a lean
      // built on a depth only one work carries is laid on rather than found; a measured horizon on
      // both works raises it, since that is the line the plane turns about. A pair reading no depth
      // at all still crosses on it, as a flat ground lying down and coming upright again.
      tilt: function (a, b) {
        var da = readingOf(((a.structure || {}).polar || {}).tunnel);
        var db = readingOf(((b.structure || {}).polar || {}).tunnel);
        var deep = Math.min(da, db);
        function hasLine(w) {
          var y = ((w.structure || {}).horizon || {}).y;
          return (y !== null && y !== undefined) ? 1 : 0;
        }
        var lines = hasLine(a) + hasLine(b);
        var fit = clamp01(deep * (0.5 + 0.25 * lines));
        return [fit, "the two works read as depth at " + pyText(flt(r4(da))) + " and "
                + pyText(flt(r4(db))) + ", and " + (lines === 2 ? "both stand" : lines === 1
                  ? "one stands" : "neither stands")
                + " a measured horizon of their own for the plane to turn about"];
      },
      // IT PARTS THE FRAME AT A LINE EACH WORK MEASURED FOR ITSELF and travels the crossing through
      // it, so what it suits is a pair whose works plainly carry their own waterline. The record
      // publishes the seam's PRESENCE and no strength of its own for it — the same reading
      // `locusOf` takes — so the motif list is the evidence, and a measured horizon on each work is
      // where the line leaves from and lands. Weaker of the two, because the line has to do both.
      // A pair carrying no seam at all is a fit of nothing rather than a refusal: the line stands
      // where the frame's own middle is and the crossing plays there.
      waterline: function (a, b) {
        function seamOf(w) {
          var mot = (w || {}).motifs || {};
          var named = (mot.measured || []).indexOf(MOTIF_SEAM) >= 0 ? 1 : 0;
          var y = ((w.structure || {}).horizon || {}).y;
          var placed = (y !== null && y !== undefined) ? 1 : 0;
          return named ? (placed ? 1 : 0.5) : (placed ? 0.25 : 0);
        }
        var sa = seamOf(a), sb = seamOf(b);
        var fit = Math.min(sa, sb);
        if (!(fit > 0)) {
          return [0, "neither work carries a measured waterline, so the line stands where the "
                  + "frame's own middle is and the crossing travels through that"];
        }
        return [fit, "the two works carry their own waterline at " + pyText(flt(r4(sa))) + " and "
                + pyText(flt(r4(sb))) + " — the line leaves one measured seam and lands on the "
                + "other"];
      },
      // THE CHAIN'S OWN EIGHT OPERATIONS READ BEST ON A PAIR WHOSE STRUCTURE ALREADY CARRIES THEIR
      // OWN VOCABULARY — a rotational order for the kaleidoscope, a little-world reading for the
      // planet fold, a measured lattice for the tile, a radial centre for the fold and the pan — the
      // same four readings pass-inst-studio.js's own `suits.reads` names. The fit is the mean of how
      // much of that vocabulary the STRONGER of the two works carries per reading, so a pair strong
      // in only one of the four still ranks above a pair strong in none, and a pair with none of it
      // still plays at the module's own opening pose (his word of 09:51 and 09:53: ranking only,
      // never a floor).
      studio: function (a, b) {
        var rot = Math.max(readingOf(((a.structure || {}).rotational || {}).score),
                           readingOf(((b.structure || {}).rotational || {}).score));
        var world = Math.max(readingOf(((a.structure || {}).polar || {}).planet),
                             readingOf(((b.structure || {}).polar || {}).planet));
        var grid = (latticeOf(a) > 0 || latticeOf(b) > 0) ? 1 : 0;
        var rad = Math.max(readingOf(((a.structure || {}).radial || {}).score),
                           readingOf(((b.structure || {}).radial || {}).score));
        var fit = clamp01((rot + world + grid + rad) / 4);
        return [fit, "the pair reads rotational order at " + pyText(flt(r4(rot)))
                + ", a little world at " + pyText(flt(r4(world))) + ", a measured lattice "
                + (grid ? "on a work of the pair" : "on neither work") + " and a radial centre at "
                + pyText(flt(r4(rad))) + " — the vocabulary the kaleidoscope, the planet, the tile "
                + "and the fold each turn on"];
      }
    };

    // An instrument the register above says nothing about suits every pair the same, and says so.
    // It is a reading and not a default: an instrument that has published no reading of its own has
    // none to rank by, which is a fact about the port rather than about the pair.
    function suitsPair(iid, a, b) {
      var ask = INSTRUMENT_SUITS[iid];
      if (!ask) {
        // DERIVED — an instrument that publishes no reading of a pair says so, and `rankUnread`
        // below places it where the pool it competes in actually landed for THIS pair. A typed 0.5
        // stood here and it is the middle of the SCALE, not of the pool: against rivals reading low
        // it towered and against rivals reading high it vanished, on every pair alike and
        // permanently, on no evidence either way.
        //
        // AND THE RULE IS WHAT IS REPAIRED, NOT THE INSTANCE. This file has already named the defect
        // twice in its own comments and closed it twice by giving one instrument a row — and the
        // rule then produced three more the night `pour`, `veil` and `wind` landed. Repairing the
        // instance leaves the rule standing to produce the next one, so the answer is returned
        // rather than typed: the comment that stood here already said the right one — no more and no
        // less than any other — and a number written in this file cannot mean it.
        return [null, "«" + iid + "» publishes no reading of a pair, so it suits this one no more "
                + "and no less than any other"];
      }
      var answer = ask(a, b);
      return [clamp01(Number(answer[0]) || 0), answer[1]];
    }

    // THE INSTRUMENT THIS PAIR CASTS ON A KIND, and it always casts one.
    //
    // Every published instrument is ranked, never filtered. Three questions stand between them and
    // each is a preference rather than a gate — a step that runs out of the first order falls to
    // the next and plays. The questions, in the order they are asked: can this voice be SEEN where
    // it is going (§7's coverage law, and only where this voice stands above a ground), does it cut
    // on this kind, and may this step spend what it spends. So the orders read:
    //
    //   1  it can be seen here, it cuts on this kind, and this step may spend what it spends
    //   2  it can be seen here and cuts on this kind, but it folds where shelf 17 gives no miracle
    //   3  it can be seen here, cuts on another kind, and this step may spend what it spends
    //   4  it can be seen here, cuts on another kind, and it folds the world
    //   5-8  the same four again for an instrument that would fill a frame already whole
    //   9  it is already spoken for by another voice of this same crossing
    //
    // Inside an order the die runs over the instruments' own readings of the pair, weighted by how
    // well each suits it — so the best-suited is the likeliest and a pinned seed reproduces the
    // casting exactly. Order 2 exists because shelf 17's budget is his law and a fold IS a miracle;
    // a step that reaches it says so on the plan and `tierFor` declares the tier that was actually
    // realised, which is the honest answer rather than a refusal.
    // IT IS ASKED OF EVERY KIND THE CUT CARRIES, and that is a repair rather than a widening. The
    // tonal and spectral pivot cuts on TWO kinds, a band and a scale, and this was asked of
    // `pivot.elementKind` alone, which is the band. So the scale half never reached an instrument at
    // all: nothing refused, nothing errored, and a whole way of crossing simply went unwalked while
    // every suite stayed green. It is why one instrument was carrying about a quarter of every
    // route's cues — on that ground it was the only one anything could reach.
    // `avoid` NAMES AN INSTRUMENT ALREADY SPOKEN FOR IN THIS CROSSING, and it stands aside rather
    // than taking the whole move down with it. One instrument carries one cue at a time — the host's
    // own law, since an instrument is one object with one pose — and the composer's answer to a
    // collision was to GIVE THE TRAVELLING MOVE UP: «the travelling axis cuts on the same instrument
    // as the pivot», and the second voice was gone. With one instrument reachable per kind that
    // collision was constant, and it is the direct mechanical cause of a passage playing on one
    // voice: with one instrument per kind, a second cue asking for that kind finds it taken on EVERY
    // pair, so the voice folds away by construction rather than by any property of the pictures. A
    // second instrument on the same kinds gives the collision somewhere to go, and every cue it
    // recovers is a cue the one-instrument rule was losing whatever was hanging on the wall.
    //
    // So a collision CHOOSES. The instrument already spoken for drops to the back of the ranking,
    // the next-best-suited takes the move, and only where it is the sole instrument in the whole
    // collection does the move fold into the voice it collided with.
    //
    // `avoid` TAKES A LIST AND NOT ONE NAME, since 2026-08-18. It named one instrument, which was
    // enough while only the travelling move called with it; the arrival has TWO voices already
    // spoken for beside it — the ground's and the travelling one's — and could name only the first,
    // so it cast against the second and then threw its own voice away rather than choosing again.
    // One list serves both callers because the fact is the same fact: these instruments are taken.
    //
    // `standsAbove` SAYS THIS VOICE WILL BE DRAWN OVER A GROUND THAT IS ALREADY WHOLE, and §7's
    // coverage law is what it reads. Only one cue of a stack may fill the frame — everything under
    // a second whole cue is drawn and never seen, which is what `placeTheStack` calls «two grounds»
    // — and each instrument's own manifest declares whether it fills one. Three of the fifteen do
    // not, so a stack of three voices needs two of those three, and a cast blind to the law breaks
    // it whenever the law applies — the composer then RETIRED the voice to pay for the breach. That
    // is why the arrival was handed to a name: «matter» is one of the three, so naming it answered
    // the law by ACCIDENT, and a name that satisfies a law by accident satisfies it for a reason
    // that changes on the next landing. The law is a preference here rather than a gate, in the same shape as the
    // other two: an instrument that fills the frame ranks after every one that does not, and where
    // the collection publishes nothing else it still plays and the loop's own answer stands.
    //
    // `mustFill` IS THE GROUND'S OWN COVERAGE LAW, ANSWERED AT THE CAST RATHER THAN AFTER IT
    // (2026-08-19, the class fix). `cueWindows` fixes the pivot cue's own window at `[0.0, 1.0]`
    // unconditionally — the first line of the function, before any branch — so the pivot plays the
    // whole pass, every time, on every plan, whatever the travelling and arriving voices' own
    // windows compose to. THE OTHER TWO ARE NO LONGER FIXED SHAPES (2026-08-19, the polyphony
    // wave; see `cueWindows` below) — travel's own close and arrival's own open are now read off
    // the pair, so they move pair to pair. Nothing here needed to change for that: pivot's window
    // was never derived FROM the other two, only compared against them, and it still promises the
    // whole pass regardless of what they compose to. §7's coverage law asks that nothing stand over
    // a bare cleared buffer, and the pivot is the one cue whose window can ever promise that for the
    // WHOLE pass; a passage that gives the ground to anything else is a passage the law cannot hold
    // for its own opening or its own close. So the pivot's own cast asks for a frame-filling
    // instrument as a preference this strong: a non-filling one ranks with an instrument already
    // spoken for, order 8, played only where the collection publishes no filling instrument
    // anywhere at all — which a one-cue plan is exempt from needing regardless (§7's own one-cue
    // exemption), so nothing is lost where that is the whole collection has.
    //
    // `clashLevels` IS THE LEVELS LAW, ANSWERED AT THE CAST RATHER THAN AFTER IT, AND — SINCE
    // 2026-08-19 — AT A MOMENT RATHER THAN FOR THE WHOLE PASS. Shelf 17 forbids two ACTIVE voices
    // on one level, and shelf 17 says in the same breath what "active" means: "transformation
    // inside transformation" is voices on DIFFERENT levels, and two voices on the SAME level that
    // never meet in time are exactly as lawful, because neither is ever active on it while the
    // other is. `ownTheLevels` used to relabel a second cue on a level "accompanies" the first
    // WITHOUT ASKING WHETHER THE TWO ARE EVER LIVE TOGETHER, and the label changed nothing the host
    // actually draws — the accompanying cue still renders its own take on the level it was told it
    // does not own, because no runtime ever reads that field to silence it. The only place the law
    // can actually hold is here, before the second voice is ever cast.
    //
    // BEFORE 2026-08-19 EXCLUDING ON THE LEVEL NAME ALONE WAS SOUND, because the three window
    // shapes were fixed: pivot's `[0, 1]` met every other cue's window by construction, and travel's
    // fixed close at 0.86 sat past arrival's own open at 0.62 or 0.10 whichever the plan carried, so
    // travel and arrival always met too — every pair of cast cues clashed on a shared level
    // whatever the pair, and the levels law degenerated into "no two voices may ever share a level
    // at all," which starves a three-voice cast (the report on this file's own record names the
    // instrument cluster it starves worst). Once travel's close and arrival's open are pair-composed
    // and can land in either order (`cueWindows` below), that degeneracy is gone, and the exclusion
    // has to ask the honest question instead: does the ALREADY-PLACED cue's own window meet the
    // CANDIDATE's own window. `clashLevels` (renamed `clashRecords` in the signature below) is now a
    // list of the already-placed cues' own `levels` AND `window` together — pivot's
    // `{levels: pivotLevels, window: [0, 1]}` always, plus travel's own record once travel is cast —
    // and the caller hands this call the CANDIDATE's own window alongside it (`candidateWindow`),
    // because whether a candidate clashes with what came before depends on when the candidate itself
    // would be live. Two windows `[a1, b1]` and `[a2, b2]` meet only where they share more than a
    // single instant — `a1 < b2 && a2 < b1` — so a cue that closes exactly where the next one opens
    // is a HANDOFF, not a clash, which is the release polyphony asks for: a voice can enter over
    // another's, leave before the passage ends, and hand a level over rather than being barred from
    // it. Pivot's own window is untouched by any of this ([0, 1] always), so pivot's own levels are
    // always folded into the overlap union the exclusion below builds — but since 2026-08-19 (the
    // ownership repair, see the note above the exclusion) carrying pivot's window alone no longer
    // excludes a candidate outright: what excludes it now is having NO level left outside that
    // union, so a candidate whose levels are a strict superset of pivot's still keeps the levels
    // pivot leaves free, and the change widens what every voice — travel, arrival, and anything
    // standing beside pivot itself — may share with what came before it.
    function castForKinds(kinds, fromW, toW, noMiracle, seed, key, slot, avoid, standsAbove,
                          mustFill, clashRecords, candidateWindow, mustFold) {
      var list = [].concat(kinds || []).filter(function (k) { return !!k; });
      var taken = [].concat(avoid === undefined || avoid === null ? [] : avoid)
        .filter(function (t) { return !!t; });
      var clash = [].concat(clashRecords === undefined || clashRecords === null ? [] : clashRecords);
      var win = candidateWindow || [0, 1];
      var cutters = [], said = [], tiers = [[], [], [], [], [], [], [], [], []],
          i, j, iid, answer, sawClash = false;
      for (j = 0; j < list.length; j++) {
        instrumentsOfKind(list[j]).forEach(function (iid2) {
          if (cutters.indexOf(iid2) < 0) cutters.push(iid2);
        });
      }
      for (i = 0; i < ALL_INSTRUMENTS.length; i++) {
        iid = ALL_INSTRUMENTS[i];
        // THE LEVELS LAW EXCLUDES OUTRIGHT ONLY WHERE THE CANDIDATE WOULD OWN NOTHING AT ALL
        // (2026-08-19, the ownership repair). Until today this test dropped a candidate the moment
        // it shared ANY level with ANY already-placed, time-overlapping voice, which is stricter
        // than what shelf 17 actually asks: shelf 17 bars two ACTIVE voices from claiming the SAME
        // level, not a voice from standing beside another on a level it does not itself drive. A
        // voice standing beside another on one level, with a level of its own left free by
        // everything already placed, is lawful — the level-ownership pass (`ownTheLevels`, below,
        // around this file's own record of it) is exactly the mechanism that settles who drives a
        // shared level AFTER the cast: the owner gets that level's full range of motion, and every
        // other cue placed on it keeps its handles for that level pinned to manifest rest, so the
        // two never actually collide at the handle a viewer would see move. What the law still
        // forbids outright is a candidate with NOTHING free to say for the window it would be
        // live: every level it declares already claimed by voices already placed, for the whole
        // stretch it would be live. So the test below unions the `levels` of every clash record
        // whose window overlaps the candidate's own window — the overlap test itself,
        // `num(win[0]) < num(rec.window[1]) && num(rec.window[0]) < num(win[1])`, is unchanged from
        // the polyphony wave above — and only excludes the candidate when EVERY level in
        // `MANIFESTS[iid].levels` sits inside that union. A candidate with even one level free of
        // the union stays in the ranking, and if chosen, owns that free level once `ownTheLevels`
        // runs. An instrument that declares no levels at all was never touched by this law before
        // today and still is not: an empty `levels` list would vacuously satisfy "every level is
        // covered," so the check requires at least one declared level before it can exclude. A
        // candidate `avoid` names may still play as the whole crossing's only voice, folded into a
        // collision — the "one instrument carries one cue" law leaves it that road, untouched by any
        // of this. Where every candidate is excluded the slot retires exactly as it does when the
        // collection casts nothing for it — the same road already walked below for "no instrument at
        // all".
        // THE SECOND CLAUSE THAT STOOD HERE IS GONE, BECAUSE ITS WHOLE PREMISE IS NOW FALSE. It
        // excluded a candidate that would stand beside another VOICE on an occupied level carrying
        // no pinning gate, and it kept a list — `PINNED_LEVELS` — of the levels that did have one.
        // That list held exactly one entry, LIGHT-COLOUR, because `singsLightColour` was the only
        // place a non-owner's handles were actually held at rest. On the other five levels nothing
        // pinned anything: a cue that did not own CELL still wrote every CELL-driving handle it had
        // and still drew its pattern.
        //
        // The gate now exists on every level. Each handle an instrument publishes declares, in that
        // instrument's own manifest, the structural level it drives, and `buildTemplate` takes the
        // handles of a level a cue does not own off that cue's track list — so a non-owner rests on
        // the level it lost and goes on playing the level it owns. With a gate on all six levels the
        // list of the gated ones is the list of all of them, and a clause that fires only for the
        // ungated ones can never fire. Keeping it would exclude candidates the law no longer needs
        // excluded, which starves the cast for nothing.
        //
        // THE GROUND'S OWN EXEMPTION GOES WITH IT, for the same reason and not as a loosening. The
        // ground held `ground: true` on its clash record so that the second clause would not count
        // it as a competitor: it holds its levels from the first frame to the last, so counting it
        // as one excluded every instrument sharing a level with it at every slot — the state that
        // left `adrift` and `gears` uncastable. With the second clause gone there is nothing left
        // for that mark to exempt the ground FROM. The collisions it was papering over — the ground
        // and a voice above it on one level — are the ones the handles now settle.
        //
        // WHAT STILL EXCLUDES A CANDIDATE OUTRIGHT, and it is one thing: a candidate with NOTHING
        // free to say. Every level it declares already claimed, across the window it would be live,
        // by voices already placed and by the ground. Such a cue would have every handle of its own
        // taken off its track list and would stand there playing nothing at all, so it is not cast.
        //
        // ONE FALSE DIAGNOSIS ON THE WAY, so it is not repeated. This law was withdrawn once on
        // 2026-08-19 for reddening `test_pass_composed.py`'s row about the gates instrument's own
        // slot. The cause was elsewhere entirely: the `clamp` wrapper the cue-course layer
        // introduced had taken a node's provenance note one level down, and that row skips any
        // node whose note does not open with «requested». With the note back on the outermost node
        // the row reads its full sweep again, with this law standing.
        if (clash.length) {
          var overlapLevels = [], overlapFolds = false;
          clash.forEach(function (rec) {
            if (num(win[0]) < num(rec.window[1]) && num(rec.window[0]) < num(win[1])) {
              (rec.levels || []).forEach(function (lv) {
                if (overlapLevels.indexOf(lv) < 0) overlapLevels.push(lv);
              });
              if (rec.folds) overlapFolds = true;
            }
          });
          var myLevels = MANIFESTS[iid].levels || [];
          var everyLevelTaken = myLevels.length && myLevels.every(function (lv) {
            return overlapLevels.indexOf(lv) >= 0;
          });
          // THE MIRACLE IS THE ONE SLOT NO OWNERSHIP CAN SHARE OUT. Every other level is settled
          // after the cast by `ownTheLevels` and kept by the handles themselves — one owner drives,
          // every other cue rests. Shelf 6 asks something else entirely of this one: a folded space,
          // a shift of what a thing is or a change of substance CONSUMES the crossing's single
          // impossible event and NEVER STACKS, and shelf 8 says at most one folded space per
          // crossing. Naряд S-18 (2026-08-27): this used to read the overlap for a shared WORLD
          // level, which was the manifest's own mark standing in for «this already-placed cue is
          // the miracle» — every clash record a cast slot builds now says so itself (`rec.folds`,
          // set beside it from `spendsTheMiracle`, the very reading this file uses everywhere else
          // a cast asks whether a candidate would spend the crossing's one impossible event), so
          // two folds are excluded from standing together whether or not this walk has already
          // spent either of them once before, and a fold that has already played once this walk and
          // reads as an ordinary letter no longer excludes a second candidate over this ground.
          var worldTaken = overlapFolds;
          if (everyLevelTaken || (worldTaken && spendsTheMiracle(iid))) {
            sawClash = true;
            continue;
          }
        }
        answer = suitsPair(iid, fromW, toW);
        var cuts = cutters.indexOf(iid) >= 0;
        // TWO READINGS OF THE SAME CANDIDATE, AND THEY ANSWER DIFFERENT LAWS. `isFold` is
        // structural and never reads the walk: it is what a road built around the fold (`mustFold`,
        // below) has to find, whether or not this walk has already spent tonight's miracle on it —
        // the box still folds into a box on its second play, it is only counted differently. `folds`
        // is `spendsTheMiracle`'s own history-aware reading and is what the ranking (`base`, below)
        // and every miracle-budget gate elsewhere in this file ask instead.
        var isFold = isWorldFold(iid);
        var folds = spendsTheMiracle(iid);
        // A ROAD THAT IS ITSELF THE FOLD CASTS AN INSTRUMENT THAT FOLDS (2026-08-19). `genreFor`'s
        // own note says it plainly: the box-fold road «cannot play at all without folding, because
        // the fold IS what it is», and shelf 6 says the folded space consumes the crossing's one
        // impossible event. Until today nothing carried that from the road to the cast — the road
        // declared `mustFold` and the ground was then ranked over every instrument cutting the
        // road's own kind, so the road could be picked and the frame never fold. It went unseen
        // because the levels law, in its stricter form, walled the other candidates out of that
        // ranking and left the folding one standing by default; the moment the law was read as it
        // is written, the fold started losing a contest it should never have been entered in.
        // WHAT QUALIFIES IS READ OFF THE MANIFEST rather than off a name: an instrument that
        // declares the world level folds the space a work lives in (`spendsTheMiracle`, above), and
        // one that cuts the road's own ground kind is the one this road is built around. Where the
        // pair carries no such instrument the caller casts again without this bound and records
        // that the road played unfolded, so a thin passage still plays and still says why.
        if (mustFold && !(isFold && cuts)) continue;
        var base = (cuts ? 0 : 2) + ((noMiracle && folds) ? 1 : 0);
        var order = (taken.indexOf(iid) >= 0) ? 8
          : ((mustFill && !FILLS_THE_FRAME[iid]) ? 8
             : ((standsAbove && FILLS_THE_FRAME[iid]) ? base + 4 : base));
        said.push({ instrument: iid, fit: answer[0] === null ? null : r4(answer[0]), cuts: cuts,
                    why: answer[1], order: order });
        tiers[order].push({ id: iid, fit: answer[0] });
      }
      for (i = 0; i < tiers.length; i++) {
        if (tiers[i].length) {
          return [dieWeighted(rankUnread(tiers[i]), seed, key + "|" + list.join("+") + "|" + slot,
                              1), said, cutters, false];
        }
      }
      // A COLLECTION WITH NO INSTRUMENT AT ALL is the one case with nothing to rank, and it is a
      // fact about the settings record rather than about the pair — UNLESS every candidate this
      // call ranked was excluded by the levels law instead, which is a fact about this slot on
      // this plan and the fourth element says so, so the caller can name the real reason.
      return [null, said, cutters, sawClash];
    }

    // The one key both directions of an edge roll the ground on.
    function groundKeyOf(a, b) {
      return a.id < b.id ? (a.id + "__" + b.id) : (b.id + "__" + a.id);
    }

    // THE LETTERS THIS WALK HAS ALREADY PLAYED, most recent first. Charter shelf 16 writes the dice
    // in order — base weights (structure fit) → LETTER COOLDOWNS → the day's weather → viewer memory
    // → roll — and this is that second step, which had nothing behind it until now: the composer
    // answered every edge of a walk as though it were the first one, so a letter that suits a whole
    // collection well carried step after step of one route. His 2026-08-17 19:13 word names the
    // failure from the other end («обидно» — one lovely move standing alone on a route) and his
    // 2026-08-24 word watching the live route names what it looks like: the effects repeat.
    //
    // THE READING IS THE WALK'S AND IT IS HANDED IN, never accumulated here. The walk already knows
    // what it played, in the client's own `passRoutePlayed`; the composer knowing it too would be a
    // second record of one fact, and a worse one — the walk composes a passage or two AHEAD of the
    // visitor to warm the instruments, and a ledger kept in here would count those speculative asks
    // as things the person saw. So this holds only what the current request said, set once per
    // passage, and `passageFor` with the same request answers the same way it always did.
    //
    // NOTHING HERE SCALES WITH THE COLLECTION. The list names letters, never pairs — the vocabulary
    // is fixed however many works hang — which is his 19:21 word about the product path.
    var walkPlayed = [];
    // …AND THE SAME WALK, STRONG MOVES ONLY (naряд S-18, 2026-08-27). `spendsTheMiracle` above
    // reads this rather than a manifest mark: the instruments named which fold beside its own
    // definition, and this is which of those folds the walk has already spent on THIS visit,
    // most recent first, exactly the shape `walkPlayed` and `roadPlayed` already are. It is set by
    // `scoreFor` for the length of one composition and never accumulated here, for the same reason
    // the other two are not.
    var walkMiracles = [];
    // WHAT ONE COOLING IS WORTH. The letter played on the passage just gone is the most cooled and
    // the one played longest ago is barely cooled at all, in even steps between: a letter at place k
    // of n keeps (k + 1) / (n + 1) of its own weight. NOTHING IS EVER ZERO, which is shelf 9's law
    // («a measurement ranks the genres», never gates) and the lab's own — a cooldown never empties a
    // pool. The strength of the cooling is therefore not a number this file invents: it is exactly
    // how much the walk chose to remember, which is the walk's own dramaturgy and one of the three
    // sources his 2026-08-19 11:58 word allows.
    //
    // THE ARITHMETIC HOLE HIS 2026-08-26 WORD NAMED, AND WHERE IT LIVED. «разнообразие необходимо,
    // вопрос в ранжировании» — the die stays, the cooling stays, and the fix is in how the four
    // multipliers of `dieWeighted` (:2654, below) weigh each other: fit (0..1, `genresFor` :4008),
    // this cooldown, `viewerBiasOf` (0.7..1.3) and `weatherBiasOf` (0.65..1.35). The last two carry
    // FIXED ranges — no request can push either under its own floor or over its own ceiling. This
    // cooldown did not: `n` in `(k + 1) / (n + 1)` was `walkPlayed.length`, the RAW LENGTH OF THE
    // WALK'S OWN LOG — and that log is deliberately unbounded (two paragraphs up: "there is no
    // length fence... the list is bounded by the walk's own length, which is the walk's business").
    // Every passage the visit plays pushes another entry for as long as the visit runs, so the
    // floor for the letter played most recently (k = 0) was `1 / (n + 1)` with no ceiling on n: the
    // longer a visit ran, the closer that floor sat to zero, without a bound below.
    //
    // A FLOOR WITH NO BOUND MAKES ANY FIT GAP INVERTIBLE. Take a road read at the best fit this file
    // ever hands out, 1.0, played on the passage just gone, against a rival read at 0.01 — a
    // hundredth of it. Weather and viewer sit at their neutral 1 for both, so only the cooldown
    // decides. At n = 99 the favoured road's weight, 1.0 × 1/100 = 0.01, ties the rival's; past
    // n = 100 the rival's steady 0.01 stands ahead of the favoured road's own share, which keeps
    // shrinking. A hundred logged letters is not a large walk — a dozen or two passages, each
    // carrying a genre and two or three instruments, cross it — and past that point NO fit gap
    // survives being the letter just played, however wide: the same arithmetic that inverts 1.0
    // against 0.01 at n = 100 inverts 1.0 against 0.0001 at n = 10000, because the floor never stops
    // falling. The hole is not that a low fit can win — shelf 9 already lets it (a measurement
    // ranks, never gates) — it is that NOTHING BOUNDED HOW BADLY IT COULD WIN, where the other two
    // riders on the same product each carry a floor no length of anything moves.
    //
    // THE FIX IS WHAT `n` COUNTS, NEVER A NEW FLOOR PICKED TO TASTE. `walkPlayed` is a LOG — one
    // entry per letter of every passage the visit has played, the same letter pushed again each time
    // the walk returns to it — and the law this cooldown states above (WHAT ONE COOLING IS WORTH)
    // was always about a letter's place AMONG THE LETTERS IN ROTATION, never about how long the log
    // that recorded them has grown. Read `n` as the count of DISTINCT letters the log holds
    // (`walkPlayedDistinct`, below) instead of the log's raw length, and `n` is bounded by the
    // walk's own vocabulary — the eight roads `genresFor` answers with, or the collection's own
    // fixed instrument list — a count fixed for the whole visit and never a function of how long the
    // visit has been running. A thousand passages that keep returning to one letter still read
    // n = 1; the floor for the letter just played is still 1/2, the floor a visit of ONE passage
    // would give it. The die still keeps every road on the board (k never removes a candidate, n
    // never reaches infinity) and the walk's own memory is read exactly as before — only what the
    // ratio is taken OVER changes, from a log that grows without end to a vocabulary that does not.
    //
    // THE LOG, KEPT ONCE PER LETTER — first occurrence only, which on a most-recent-first log is a
    // letter's own most recent play; everything after it is a repeat the cooldown never needed to
    // see twice. `coolOf` reads recency off this list and never off `walkPlayed` itself.
    function dedupeMostRecent(list) {
      var out = [], seen = {}, i, id;
      for (i = 0; i < list.length; i++) {
        id = list[i];
        if (!Object.prototype.hasOwnProperty.call(seen, id)) { seen[id] = true; out.push(id); }
      }
      return out;
    }
    var walkPlayedDistinct = [];
    // THE COOLDOWN'S OWN RATIO, cut out as pure arithmetic over two numbers — a place `at` (−1 for
    // "never played") and a pool size — so it is provable over the whole span either can take
    // (row 8j-2 of tests/test_pass_composed.py) rather than over whichever walk happens to be
    // running.
    function coolFactor(at, poolSize) {
      return at < 0 ? 1 : (at + 1) / (poolSize + 1);
    }
    function coolOf(id) {
      return coolFactor(walkPlayedDistinct.indexOf(id), walkPlayedDistinct.length);
    }
    // THE SAME COOLDOWN, OVER THE ROAD'S OWN POOL, AND NEVER THE MIXED ONE ABOVE. His adversarial
    // follow-up on this same fix (2026-08-26 night run, a live production walk) found what
    // `walkPlayedDistinct` actually holds: `walkMemory` is `01a-pass.js`'s flattened reading of a
    // step's road AND every instrument its stack carried, so a road's own cooldown, read off that
    // pool, divides by up to ~35 (eight roads plus roughly twenty-seven instruments) rather than the
    // eight `genresFor` ever answers with — the floor for a road just played sat near 1/36, not the
    // claimed 1/9, and his own live numbers showed a fitness gap of 0.88 against 0.14 inverting at a
    // pool no wider than six. Filtering the mixed list after the fact cannot fix it either: a road
    // and an instrument can share one spelling (`kaleidoscope` is both), so a name alone cannot say
    // which vocabulary it came from. `01a-pass.js`'s `passWalkGenres` reads the road off each step
    // and never the stack, so `walkGenres` — and `roadPlayedDistinct` below, its dedupe — can only
    // ever hold one of the eight roads, however many instruments the same steps cast. `pickGenre` is
    // the one caller that reads `coolOfRoad`; every instrument cast still reads `coolOf` above,
    // unchanged.
    var roadPlayedDistinct = [];
    function coolOfRoad(id) {
      return coolFactor(roadPlayedDistinct.indexOf(id), roadPlayedDistinct.length);
    }
    // THE SAME COOLDOWN, TAKEN OFF A RAW LIST HANDED IN rather than off the module's own held
    // `walkPlayedDistinct` — exposed beside `coolFactor` for the reason `camVoiceFloor` and the rest
    // travel beside the entry (:8996 below): a claim about numbers is answered over numbers, not
    // over a route. It is not a second cooldown; it is `coolOf`'s own two steps, dedupe then
    // `coolFactor`, run on a list a caller supplies.
    function walkCooldown(list, id) {
      var distinct = dedupeMostRecent(Array.isArray(list) ? list : []);
      return coolFactor(distinct.indexOf(id), distinct.length);
    }

    // THE VISIT'S OWN MEMORY OF ITSELF, beyond the one edge — charter shelf 16's fourth pipeline
    // step. `sessionMemory` (below, §4.8) is the return reference of ONE edge; this is the visit
    // standing back further: which letters (genres, instruments — the same vocabulary `coolOf`
    // already cools) it lingered on or visibly skipped anywhere this visit, and which works it has
    // already shown. It arrives on the request exactly as `walkMemory` does — set fresh by
    // `scoreFor` for the length of one composition, never accumulated in this file — and it is read
    // by the same die `coolOf` already sits inside, never a second pipeline of its own.
    var viewerMemory = null;
    // THE INSTANT THIS VISIT HAPPENS AT — charter shelf 16's third pipeline step, and it arrives the
    // way every other step of that pipeline arrives: the walk hands it in. It is set fresh by
    // `scoreFor` for the length of one composition and never accumulated here, exactly as
    // `walkPlayed` and `viewerMemory` are. Nothing in this file calls the clock, because a value the
    // composer takes for itself is a value nothing can pin, and shelf 16's own last two sentences
    // put the day in the VIEWER mode while a pinned seed is the JUDGING one. A request that names no
    // instant reads at the neutral, which is the neutral `coolOf` and `viewerBiasOf` already take.
    var visitClock = null;
    // THE BIAS ITSELF. Lingered letters gain, skipped letters cool, and NOTHING IS EVER ZERO — the
    // same law `coolOf` stands on, so the widest bound either way is 0.7/1.3, never 0. A letter this
    // file has never heard of from the visit (the ordinary case) reads at the neutral 1.
    function viewerBiasOf(id) {
      if (!viewerMemory) return 1;
      var amp = 0.3, bias = 1;
      if ((viewerMemory.lingered || []).indexOf(id) >= 0) bias *= (1 + amp);
      if ((viewerMemory.skipped || []).indexOf(id) >= 0) bias *= (1 - amp);
      return bias;
    }
    // HOW MANY TIMES ONE ID ALREADY STANDS IN A PLAIN LIST OF NAMES — `viewerMemory.seenWorks`'
    // own shape, read live and never counted anywhere but here.
    function countIn(list, id) {
      var n = 0, i;
      if (!Array.isArray(list)) return 0;
      for (i = 0; i < list.length; i++) if (list[i] === id) n++;
      return n;
    }

    // THE DAY'S WEATHER BIAS — charter shelf 16's third pipeline step. A bias read off the instant
    // the walk states on its own request: never a stored config, never a measurement of the
    // collection, never seeded from anything prepared ahead of the visit (his 2026-08-24 word,
    // shelf 21 — "ты НИЧЕГО не готовишь заранее"). Nothing about it is cached across calls, because
    // the day and the hour it answers for are exactly what changes visit to visit.
    //
    // AND THIS FILE CALLS NO CLOCK AT ALL, which is the repair of 2026-08-26. `new Date()` stood in
    // `weatherNow` below and was the last thing in the composer that a pinned run could not
    // reproduce; the instant now arrives on the request as `day` and the composition is a function
    // of the request alone. `new Date(visitClock)` below is the arithmetic that turns that stated
    // instant into a date and an hour, and it reads no clock: it is handed the number.
    //
    // THE VOCABULARY IS THE RECORD'S OWN. The eight hue names below are `palette.hues`' own alphabet
    // — every work in the collection already carries one or more of them — so the wheel invents no
    // vocabulary the works do not already speak; it only rotates which one the day currently answers
    // to.
    var WEATHER_HUE_WHEEL = ["red", "orange", "yellow", "green", "cyan", "blue", "violet", "magenta"];
    function weatherNow() {
      // ONE CLOCK FOR EVERY VIEWER. These four readings were taken off the LOCAL getters, so two
      // people meeting one crossing at one instant read two different hours, two different weights
      // and two different grounds, and the family a return is matched against moved with the offset
      // the machine happens to be set to. That offset is an input from none of the three sources
      // charter shelf 20 allows — a picture's own record, the dramaturgy of the walk, the session —
      // and it is not the day either: the day is one day everywhere, and local midnight is not.
      //
      // AND THE INSTANT ITSELF IS NOW HANDED IN RATHER THAN TAKEN. `new Date()` stood here, which is
      // the one thing in this file that no pinned run could reproduce: a value the composer takes
      // for itself is a value nothing can pin, so one request at one seed composed two different
      // scores an hour apart and the family a return is matched against moved with the hour. Shelf
      // 16 asks for both the day's bias and a seeded run that repeats, and its own last two
      // sentences say which answers where — seeds and determinism are the JUDGING mode, ephemerality
      // is the VIEWER mode. So the day is an input the walk states in the mode that has one, and
      // never a call made here: a public walk sends the instant it cast the pair and the composition
      // breathes with the day, a pinned walk sends none and the run reproduces to the pixel. The
      // contract's own line three paragraphs on — that the die carries no clock — is true of this
      // file now rather than aspirational, because there is no clock left inside it to read.
      var d = new Date(visitClock);
      var dayOfYear = Math.floor((d.getTime() - Date.UTC(d.getUTCFullYear(), 0, 1)) / 86400000);
      var hourFrac = (d.getUTCHours() + d.getUTCMinutes() / 60) / 24;
      var hueAt = ((dayOfYear + hourFrac) % WEATHER_HUE_WHEEL.length + WEATHER_HUE_WHEEL.length)
                  % WEATHER_HUE_WHEEL.length;
      return {
        hue: WEATHER_HUE_WHEEL[Math.floor(hueAt)],
        // LIGHT: the DAY'S own smooth curve and no one viewer's, 0 at the day's start and 1 at its
        // middle — read the way a photographer reads the day, never a brightness measured off any
        // photograph on file, and never off the hour the reader's own machine is set to.
        light: 0.5 + 0.5 * Math.cos(2 * Math.PI * (hourFrac - 0.5)),
        // TEMPO: the same one clock, a quarter turn out of phase with light, so the day's liveliest
        // hour is not simply its brightest one. It is the day's liveliest hour and not the
        // reader's: two people meeting this crossing at one instant now read one tempo.
        tempo: 0.5 + 0.5 * Math.sin(2 * Math.PI * (hourFrac - 0.5))
      };
    }
    // THE BIAS AGAINST ONE GROUND CANDIDATE (`groundCandidates`' own shape, below). Bounded to
    // [0.65, 1.35] on every branch — the same shape `coolOf` and `viewerBiasOf` already keep, so a
    // day never empties a ground and the pair's own strongest reading still wins where it is far
    // ahead. Three of the four candidate kinds already carry one of the day's three named voices
    // (palette, tempo, light — shelf 16's own parenthetical) and the fourth (`shared-measure`)
    // carries none of them, so it reads at the neutral 1 exactly as any candidate this file has
    // nothing to say about does.
    //
    // UNJUSTIFIED. Everything above argues the number's SHAPE — that it must stay under one so the
    // day never empties a pool — and an argument about a shape is not a derivation of a value. This
    // seat chose 0.35 and nothing measured it; every value under one satisfies the shape equally.
    var WEATHER_AMP = 0.35;
    function weatherBiasOf(item) {
      if (!item || !item.kind) return 1;
      // A REQUEST THAT NAMES NO DAY GETS NO DAY'S BIAS, and that is the neutral rather than a
      // refusal: the reading is 1 on every candidate, the pair's own strongest reading ranks the
      // pool alone, and the crossing plays. It is the same neutral `coolOf` gives a letter no walk
      // has played and `viewerBiasOf` gives a letter no visit has heard of.
      if (visitClock === null) return 1;
      var w = weatherNow();
      if (item.kind === "shared-palette-region") {
        var hues = item.hues || [];
        return 1 + WEATHER_AMP * (hues.indexOf(w.hue) >= 0 ? 1 : -1);
      }
      if (item.kind === "tonal-and-spectral") {
        var ladder = (item.bridge || {}).ladder || [];
        var avg = ((Number(ladder[0]) || 0) + (Number(ladder[1]) || 0)) / 2;
        var closeness = 1 - Math.min(1, Math.abs(avg - w.light));
        return 1 + WEATHER_AMP * (2 * closeness - 1);
      }
      if (item.kind === "shared-rotational-order") {
        return 1 + WEATHER_AMP * (2 * w.tempo - 1);
      }
      return 1;
    }

    // THE DIE OVER A RANKING. Each candidate carries a fit, the die lands somewhere in their summed
    // weight, and the best-suited holds the widest stretch of it. Where every fit is nothing the die
    // is even — nothing is refused for reading nothing, it is simply no likelier than its rivals.
    // The list is sorted by name first so a pinned seed reproduces the choice whatever order the
    // caller built it in.
    //
    // THE COOLDOWN MULTIPLIES THE FIT AND NEVER REPLACES IT: the pair's own reading still ranks the
    // pool and still holds the widest stretch of the weight where it is far ahead — what the cooling
    // does is narrow that stretch for a letter this walk has just played, so a near-rival takes the
    // die more often. A letter no walk has played keeps its whole weight.
    //
    // `letters === "road"` READS `coolOfRoad`'S OWN POOL rather than `coolOf`'s mixed one — the
    // 2026-08-26 night-run separation, above `coolOfRoad`. `pickGenre` passes `"road"`; the
    // instrument casts pass a plain `1` and keep reading `coolOf` exactly as before.
    //
    // IT COOLS LETTERS AND NOTHING ELSE, and the caller says which pool is which. Shelf 16's own
    // words are «letter cooldowns»: a genre and an instrument are letters of the vocabulary and a
    // person sees them repeat, while the GROUND a pair stands on is the pair's own structure and
    // not a letter at all. Two reasons hold them apart and both are law rather than tidiness. §4.8
    // says a return holds the family AND the pivot, so cooling the ground would make the walk unable
    // to keep the very thing it came back for. And one name — «tonal-and-spectral» — is both a genre
    // and a ground, so a pool told to cool indiscriminately would cool a pair's ground because a
    // passage elsewhere on the route happened to run on the genre that shares its name. The default
    // is not to cool, so a call site added later cannot cool a ground by forgetting to say so.
    // `viewerBiasOf` rides the same `letters` gate as `coolOf` — the visit's own lingered/skipped
    // reading is a reading of LETTERS too, never of a ground. `weatherBiasOf` rides no gate at all:
    // it reads `item.kind`, which only a ground candidate ever carries, so it is a no-op on every
    // genre and instrument pool by construction and never needs a flag to stay out of their way.
    function dieWeighted(list, seed, key, letters) {
      var pool = list.slice().sort(function (x, y) { return x.id < y.id ? -1 : (x.id > y.id ? 1 : 0); });
      var total = 0, i, w = [];
      for (i = 0; i < pool.length; i++) {
        w.push(Math.max(0, Number(pool[i].fit) || 0)
               * (letters ? (letters === "road" ? coolOfRoad(pool[i].id) : coolOf(pool[i].id))
                            * viewerBiasOf(pool[i].id) : 1)
               * weatherBiasOf(pool[i]));
        total += w[i];
      }
      if (!(total > 0)) return pool[dieAmong(seed, key, pool.length)].id;
      var at = dieAmong(seed, key, 1000000) / 1000000 * total, run = 0;
      for (i = 0; i < pool.length; i++) {
        run += w[i];
        if (at < run) return pool[i].id;
      }
      return pool[pool.length - 1].id;
    }

    // The tonal and spectral closeness of a pair — two readings the two works always carry, so this
    // answers for every pair in the world, including two records that share no measured structure
    // at all. A record missing either field reads as the plainest thing it can: the fields' own
    // neutral, which is what an unmeasured level and a one-pixel detail scale amount to.
    // THE LATTICE A WORK CARRIES, in the one unit the reading is already in: the step the work was
    // actually cut at, falling back to the repeat its own grid was measured at where no device was
    // recovered. `measuredParts` carries the same order of preference for the fill, which has one
    // work at a time; this one answers where the whole pair is in hand.
    function latticeOf(w) {
      var st = w.structure || {};
      return Number((st.ownDevice || {}).stepPx) || Number((st.grid || {}).periodPx) || 0;
    }

    function tonalSpectral(a, b) {
      // THE TONE, off `luminance.level` — the median of each work's own luminance
      // (lab/analyze/recipes.py:551-613 colour_stats(), carried through build-workrecords-v1.py's
      // record), rather than `palette.colourfulness` — half chroma_p90, half hue_entropy, which
      // this pivot read before tonight's rename exposed it as a colourfulness reading and not a
      // tone. Charter shelf 12 defines the tonal decomposition as luminance zones, so its tonal
      // half must read a tone, and `luminance.level` is the genuine one the record now carries.
      var ta = Number((a.luminance || {}).level) || 0;
      var tb = Number((b.luminance || {}).level) || 0;
      var fa = Number((a.texture || {}).detailPx) || 1, fb = Number((b.texture || {}).detailPx) || 1;
      var tonal = 1.0 - Math.min(1.0, Math.abs(ta - tb));
      var spectral = 1.0 - Math.min(1.0, Math.abs(Math.log2(Math.max(fa, 1e-6))
                                                  - Math.log2(Math.max(fb, 1e-6))) / 4.0);
      return { tonal: tonal, spectral: spectral, ladder: [ta, tb], detailPx: [fa, fb] };
    }

    // EVERY GROUND THIS PAIR COULD STAND ON, EACH WITH ITS OWN STRENGTH. Nothing is admitted and
    // nothing is turned away: the seven shared measures and the three pivots the elements builder
    // knows beside them are all candidates for every pair, and the strength says which to reach for
    // first. A candidate reading nothing is still a candidate — it is simply last.
    //
    // WHAT WENT. The ground was «the strongest shared measure AN INSTRUMENT CAN PLAY», and a pair
    // whose strongest shared measure cut on tiles, panels or named regions declined whole with
    // «pivot needs an instrument that cuts on …». Beneath that stood `holdable`, which asked three
    // admission questions at once — is the measure playable, can some instrument cast it for this
    // pair, do both works carry real elements — and `chooseGround`, which drew its pool from the
    // measures that cleared their typed floor. All four questions are now readings that RANK, and
    // the instrument's own casting, one step later, always answers with an instrument.
    function groundCandidates(a, b) {
      var all = groundReadings(a, b), out = [], i, m;
      for (i = 0; i < MEASURES.length; i++) {
        m = MEASURES[i];
        out.push({ id: m, kind: "shared-measure", measure: m, fit: num(all.per[m].min),
                   strength: all.per[m].min });
      }
      // THE SHARED TURN. Its strength is the weaker rotational reading where the two works turn on
      // one and the same order and both carry a wedge set to cut; where they do not, the turn is
      // not something this pair has between them and the reading is nothing. That is structural —
      // two works of different rotational order share no turn — and not a floor.
      var na = ((a.structure || {}).rotational || {}).n || 0;
      var nb = ((b.structure || {}).rotational || {}).n || 0;
      var turn = (na >= 3 && na === nb && setFor(a, "wedge") !== null && setFor(b, "wedge") !== null)
        ? Math.min(readingOf(((a.structure || {}).rotational || {}).score),
                   readingOf(((b.structure || {}).rotational || {}).score))
        : 0;
      out.push({ id: "shared-rotational-order", kind: "shared-rotational-order", fit: turn,
                 order: na, strength: r4(turn) });
      // THE SHARED PALETTE REGION. Its strength is the share of the departing work's own hues the
      // arriving work also carries, where both stand on one rung of the ladder.
      //
      // THE STRENGTH STOOD AT A TYPED NOTHING UNTIL NOW, and the reasoning was that the elements
      // builder reads no `strength` off this pivot's value. That was true of the builder and false
      // of everything else: `compose` opens the travelling voice's own window at
      // `clamp01(pivot.strength)`, so on every pair that crossed on this ground the travel opened at
      // exactly 0 — the same instant the ground opens — and two windows that begin together are the
      // tie that used to be settled by comparing cue ids as text. A number that could have been
      // written before either photograph was seen is charter shelf 21's own named failure, and this
      // one was reaching the composition by a road nobody had traced. The share above IS the
      // strength of a shared palette region, and every neighbouring candidate on this list already
      // publishes its own reading in both fields, so this one does too.
      // WHAT WENT, AND WHY IT COULD NOT STAND. This read `ra === rb` — the two works' ladder RUNGS,
      // equal or not — as a gate in front of the share, and one expression broke two laws.
      //
      // The rung is a bucket whose four coloured cuts are the collection's own top quarter on their
      // defining measure (the record builder's `classify_tone`), so which rung a photograph stands
      // on is a statement about the OTHER photographs it was measured beside. Hanging one more
      // picture moves an existing work's rung, and the die below reads the whole pool's weight as
      // one sum — so it moves not only whether these two cross on colour but which of the other
      // grounds the same die lands on, and with it the pivot's transform and the family §4.8 matches
      // a return against. A third photograph deciding a crossing between two others is charter
      // shelf 20's own sentence at the place where it decides one.
      //
      // And an equality between two bucket names is a GATE. A candidate whose weight is exactly
      // nothing holds a stretch of the die's running sum of exactly no width, so it is never rolled
      // while any rival reads anything: two works standing a hair apart on the ladder had this
      // ground REFUSED rather than ranked. That is the admission test `groundReadings` a few screens
      // above was already cured of, and his word of 2026-08-18 09:51 is the cure — a measurement
      // ranks which genre suits a pair and shapes the one that wins, and never admits.
      //
      // WHAT STANDS INSTEAD is the ladder's own CONTINUOUS coordinate, which the record already
      // carries as `palette.colourfulness`: half how much colour is present (the chroma at the
      // coloured end of the frame against a fixed perceptual anchor) and half how wide it is spread
      // (the normalised entropy of the work's own hue histogram). Both halves are read off one
      // picture's own pixels and both are 0 at grey and 1 at a frankly polychrome frame, so the
      // coordinate is in [0, 1] by construction and the closeness below is too. The rung itself
      // still travels on the candidate, where a person reads it — it names a palette world and
      // naming is what a name is for; it decides nothing here.
      var ra = (a.palette || {}).rung;
      var mine = (a.palette || {}).hues || [], theirs = (b.palette || {}).hues || [], hues = [];
      for (i = 0; i < mine.length; i++) if (theirs.indexOf(mine[i]) >= 0) hues.push(mine[i]);
      hues.sort();
      var wa = (a.palette || {}).colourfulness, wb = (b.palette || {}).colourfulness;
      var together = (typeof wa === "number" && typeof wb === "number")
        ? 1 - Math.abs(clamp01(wa) - clamp01(wb)) : 1;
      // WHERE EITHER WORK NAMES NO HUE THERE IS NOTHING TO NARROW, and the closeness stands alone.
      // Two grey frames share the grey end of the ladder whole, and the line this replaces wrote
      // them down to nothing because neither had a hue to overlap with the other's.
      var overlap = (mine.length && theirs.length) ? hues.length / mine.length : 1;
      var paletteShare = together * overlap;
      out.push({ id: "shared-palette-region", kind: "shared-palette-region",
                 fit: paletteShare, hues: hues, rung: ra, strength: r4(paletteShare) });
      // THE TONAL ZONES AND THE DETAIL SCALES. Two decompositions that read on any two photographs
      // by construction, so this candidate answers for every pair. It is ranked on its own reading
      // like every other and reached by the same code path — there is no «when nothing else, then
      // this» left anywhere in this file, on his word of 10:15.
      var bridge = tonalSpectral(a, b);
      out.push({ id: "tonal-and-spectral", kind: "tonal-and-spectral",
                 fit: Math.min(bridge.tonal, bridge.spectral), bridge: bridge,
                 strength: r4(r4(bridge.tonal) || 0.0) });
      return out;
    }

    // THE GROUND A CROSSING STANDS ON, ranked and rolled.
    //
    // THE DIE IS ROLLED ON THE EDGE'S OWN KEY AND NOT ON THE PASSAGE'S, so the two directions of one
    // edge choose the same ground. §4.8's kinship is that a return keeps the family, and the family
    // is read off the pivot's own transform; a ground that changed with the direction would make
    // every return unrelated by construction.
    //
    // `free` is the measure a GENRE needs left free to travel: a genre built on the pair's radial
    // reading cannot also hold it still, so that candidate stands down for this one crossing.
    // `prefer` names a ground the genre asks to stand on — a return holding the pivot of the pass it
    // answers uses it — and it wins wherever the pair carries it at all.
    function pivotOfPair(a, b, free, prefer, noMiracle, seed, groundKey) {
      var pool = groundCandidates(a, b), chosen = null, i;
      var open = pool.filter(function (c) { return c.measure !== free || free === undefined; });
      if (!open.length) open = pool;
      if (prefer && prefer !== free) {
        for (i = 0; i < open.length; i++) {
          if ((open[i].measure === prefer || open[i].id === prefer) && open[i].fit > 0) {
            chosen = open[i];
            break;
          }
        }
      }
      if (chosen === null) {
        var at = dieWeighted(open, seed || 0, (groundKey || (a.id + "__" + b.id)) + "|ground");
        for (i = 0; i < open.length; i++) if (open[i].id === at) chosen = open[i];
      }
      if (chosen === null) chosen = open[0];
      var v;
      if (chosen.kind === "shared-measure") {
        v = { strength: chosen.strength, measure: chosen.measure,
              cut: CUT_OF_MEASURE[chosen.measure][0],
              transform: CUT_OF_MEASURE[chosen.measure][1],
              elementKind: KIND_OF_MEASURE[chosen.measure] };
        return { kind: "shared-measure", value: v, rowStrength: chosen.strength, ranking: open };
      }
      if (chosen.kind === "shared-rotational-order") {
        v = { order: chosen.order, cut: "wedges", transform: "gear_mesh", elementKind: "wedge",
              strength: chosen.strength };
        return { kind: "shared-rotational-order", value: v, rowStrength: chosen.strength,
                 ranking: open };
      }
      if (chosen.kind === "shared-palette-region") {
        v = { rung: chosen.rung, hues: chosen.hues, cut: "colour_world",
              transform: "palette_handover", elementKind: "band" };
        return { kind: "shared-palette-region", value: v, rowStrength: chosen.strength,
                 ranking: open };
      }
      v = { tonalCloseness: r4(chosen.bridge.tonal), spectralCloseness: r4(chosen.bridge.spectral),
            ladder: chosen.bridge.ladder, detailPx: chosen.bridge.detailPx,
            cut: "tonal_zones_and_detail_scales",
            transform: "zone_handover_and_scale_growth", elementKind: "band" };
      return { kind: "tonal-and-spectral", value: v, rowStrength: chosen.strength,
               ranking: open };
    }

    // HOW READY THIS PAIR IS, which is a reading and never a verdict. A typed floor of 0.12 stood
    // in front of it and wrote any pair under it down to nothing — the only act a floor can perform.
    // What is left is the arithmetic: the weaker readiness, narrowed by how unevenly the two ends
    // are prepared. The guard on a zero denominator stays, because it is arithmetic rather than
    // judgement.
    //
    // A RECORD THAT CARRIES NO READINESS READS AT NOTHING, and does not throw. `passageFor`'s own
    // two refusals — the only two left in this file — ask a record for an `id` and for nothing else,
    // so a record carrying an id alone is a record this file has already agreed to compose over.
    // This reading indexed the field straight (`ra[0]`) and threw on exactly that record, and
    // charter shelf 21 says no branch may terminate in «no crossing»: a throw is worse than a
    // refusal, because a refusal at least names itself. Every neighbouring reading in this file
    // answers a missing field with that field's own neutral — `readingOf` for a share, `Number(x)
    // || 0` for a length, `null` for a horizon — and the neutral here is nothing: a pair whose
    // preparedness is exactly zero already reads at nothing by the line below, so a pair with no
    // readiness recorded at all reads the same and ranks last, and still crosses.
    function readinessOf(w) {
      var r = w && w.readiness;
      if (Object.prototype.toString.call(r) !== "[object Array]" || r.length < 2) return [0, 0];
      return [Number(r[0]) || 0, Number(r[1]) || 0];
    }
    function pairScore(ra, rb) {
      var sa = ra[0], pa = ra[1], sb = rb[0], pb = rb[1];
      if (pa <= 0 || pb <= 0) return 0.0;
      return Math.min(sa, sb) * (Math.min(pa, pb) / Math.max(pa, pb));
    }

    function pairOf(a, b, direction, seed, free, prefer, noMiracle) {
      // §4.3's PairDossier, in the shape `compose` reads it: the pivot the two works derive, the
      // two doors, this pair's readiness and the die the caller rolled. `free` is the measure the
      // chosen road needs left free to travel, so the ground never stands on it, and `prefer` the
      // one it asks to stand on.
      var chosen = pivotOfPair(a, b, free, prefer, noMiracle, seed, groundKeyOf(a, b));
      var kind = chosen.kind;
      var value = { strength: chosen.rowStrength };
      if (kind === "shared-measure") {
        value.measure = chosen.value.measure;
        value.cut = chosen.value.cut;
        value.transform = chosen.value.transform;
        value.elementKind = chosen.value.elementKind;
      } else {
        var tpl = PIVOT_SHAPES[kind];
        Object.keys(tpl).forEach(function (k) { value[k] = tpl[k]; });
      }
      if (chosen.value.spectralCloseness !== undefined) {
        value.spectralCloseness = chosen.value.spectralCloseness;
        value.tonalCloseness = chosen.rowStrength;
      }
      if (chosen.value.order !== undefined) value.order = chosen.value.order;
      var fromW = direction === "b-to-a" ? b : a;
      var toW = direction === "b-to-a" ? a : b;
      return {
        pair: { a: a.id, b: b.id },
        direction: direction,
        pivot: { kind: kind, value: value },
        doorFraming: { from: fromW.door, to: toW.door },
        readiness: r4(pairScore(readinessOf(fromW), readinessOf(toW))),
        seed: seed
      };
    }

    // ---- step one, the pivot ----

    function pivotOf(pair) {
      var v = pair.pivot.value;
      var strength = v.strength;
      return {
        kind: pair.pivot.kind,
        measure: v.measure === undefined ? null : v.measure,
        cut: v.cut === undefined ? null : v.cut,
        transform: v.transform === undefined ? null : v.transform,
        elementKind: v.elementKind === undefined ? null : v.elementKind,
        elementKinds: v.elementKinds === undefined ? null : v.elementKinds,
        strength: r4(strength ? strength : 0.0),
        held: true
      };
    }

    // EVERY KIND OF ELEMENT THIS PIVOT'S CUT YIELDS. The pivot's own shape says so; a shared measure
    // yields the one kind `KIND_OF_MEASURE` names for it.
    function pivotKindsOf(pivot) {
      if (pivot.elementKinds && pivot.elementKinds.length) return pivot.elementKinds;
      return [pivot.elementKind];
    }

    // ---- step two, the travelling axis ----

    // WHAT A WORK READS ON ONE AXIS. Every axis the record carries answers, whatever the number:
    // a reading is a reading, and a low one says the axis travels a little rather than that it may
    // not travel at all. A typed cut-line floor stood on this line and struck a whole axis out of
    // the crossing where either work read under it — the same floor whose three tight companions
    // stood above what any photograph in the collection could score. Only a MISSING field answers
    // with nothing now, and that is absence rather than judgement.
    function axisReading(work, axis) {
      var st = (work || {}).structure || {}, s, ends, t, rr;
      if (axis === "banding") {
        if (!st.banding) return null;
        s = st.banding.score;
        ends = { periodPx: r4(st.banding.periodPx), axis: st.banding.axis };
      } else if (axis === "radial") {
        rr = st.radial;
        if (!rr || !rr.centre) return null;
        s = rr.score;
        ends = { centre: [r4(rr.centre[0]), r4(rr.centre[1])], subType: rr.subType };
      } else if (axis === "regions") {
        if (!st.regions) return null;
        s = st.regions.score;
        ends = { count: st.regions.count };
      } else if (axis === "grid") {
        if (!st.grid) return null;
        s = st.grid.score;
        ends = { periodPx: r4(st.grid.periodPx), angleDeg: r4(st.grid.angleDeg) };
      } else if (axis === "texture") {
        t = work.texture;
        if (!t) return null;
        s = t.scoreFromCutLines;
        ends = { detailPx: r4(t.detailPx), spectralPeriodPx: r4(t.spectralPeriodPx) };
      } else if (axis === "dominant_object") {
        if (!st.dominantObject || !st.dominantObject.bbox) return null;
        s = st.dominantObject.score;
        ends = { box: st.dominantObject.bbox.map(function (x) { return r4(x); }) };
      } else {
        return null;
      }
      if (s === null || s === undefined) return null;
      return { score: r4(s), ends: ends };
    }

    function travellingAxis(aWork, bWork, pivot) {
      var held = pivot.measure, best = null, i, axis, ra, rb, delta;
      for (i = 0; i < TRAVEL_AXES.length; i++) {
        axis = TRAVEL_AXES[i];
        if (axis === held) continue;
        ra = axisReading(aWork, axis);
        rb = axisReading(bWork, axis);
        if (ra === null || rb === null) continue;
        delta = Math.abs(ra.score - rb.score);
        if (best === null || delta > best.delta || (delta === best.delta && axis > best.axis)) {
          best = { axis: axis, delta: r4(delta), from: ra, to: rb };
        }
      }
      return best;
    }

    // ---- step three, the actors ----

    function setFor(work, kind) {
      var i, sets = (work || {}).sets || [];
      for (i = 0; i < sets.length; i++) {
        if (sets[i].kind === kind) return sets[i];
      }
      return null;
    }

    // A work's own strongest cut, whatever kind it is — the actor a work can always be drawn from.
    // The set with the most real elements wins; where a work carries none, the widest set it has
    // stands, and the whole frame is a lawful element (§4.3's degenerate one).
    function anySetOf(work) {
      var sets = (work || {}).sets || [], best = null, i;
      for (i = 0; i < sets.length; i++) {
        if (best === null
            || (sets[i].realCount || 0) > (best.realCount || 0)
            || ((sets[i].realCount || 0) === (best.realCount || 0)
                && (sets[i].count || 0) > (best.count || 0))) best = sets[i];
      }
      return best;
    }

    // THE ACTORS, AND THERE ARE ALWAYS SOME. Two refusals stood in this function — a work with no
    // element set on the pivot's own cut, and a work offering only the whole frame along it — and
    // between them they were the reason `holdable` had to gate a ground before it was chosen. Both
    // are gone. A work that offers the whole frame along the cut hands over the whole frame, which
    // is exactly what a crossing between two photographs sharing no measured structure looks like;
    // a work with no set on the cut at all hands over its own strongest cut instead, and the plan
    // says which cut was wanted and which was drawn.
    function castActors(fromW, toW, pivot, axis) {
      var actors = [], kinds = pivotKindsOf(pivot), stood = [];
      var pairs = [["a", fromW], ["b", toW]], i, j, ref, work, drawn, found, tkind, role;
      for (i = 0; i < pairs.length; i++) {
        ref = pairs[i][0];
        work = pairs[i][1];
        drawn = 0;
        for (j = 0; j < kinds.length; j++) {
          found = setFor(work, kinds[j]);
          if (found === null) continue;
          actors.push({ ref: ref, set: found.index, role: "pivot-carrier", ids: null,
                        count: found.count, measuredGrain: found.measuredGrain,
                        mergeFactor: found.mergeFactor });
          drawn += 1;
          if (!found.realCount) {
            stood.push("work " + ref + " offers only the whole frame along the pivot's cut, so the "
                       + "whole frame is what hands over");
          }
        }
        if (!drawn) {
          found = anySetOf(work);
          if (found !== null) {
            actors.push({ ref: ref, set: found.index, role: "pivot-carrier", ids: null,
                          count: found.count, measuredGrain: found.measuredGrain,
                          mergeFactor: found.mergeFactor });
            stood.push("work " + ref + " carries no set on the pivot's cut, so its own «"
                       + found.kind + "» cut stands in");
          } else {
            stood.push("work " + ref + " carries no element set at all, so it crosses whole");
          }
        }
      }
      if (axis !== null) {
        tkind = KIND_OF_AXIS[axis.axis];
        if (tkind && kinds.indexOf(tkind) < 0) {
          for (i = 0; i < pairs.length; i++) {
            found = setFor(pairs[i][1], tkind);
            if (found === null) continue;
            if (!found.realCount) continue;
            actors.push({ ref: pairs[i][0], set: found.index, role: "traveller", ids: null,
                          count: found.count, measuredGrain: found.measuredGrain,
                          mergeFactor: found.mergeFactor });
          }
        }
      }
      var figures = [["a", fromW, "departing-figure"], ["b", toW, "arriving-figure"]];
      for (i = 0; i < figures.length; i++) {
        ref = figures[i][0];
        work = figures[i][1];
        role = figures[i][2];
        found = null;
        for (j = 0; j < kinds.length; j++) {
          var candidate = setFor(work, kinds[j]);
          if (candidate !== null && candidate.realCount) { found = candidate; break; }
        }
        if (found === null) continue;
        if (found.fig === null || found.fig === undefined) continue;
        actors.push({ ref: ref, set: found.index, role: role, ids: [found.fig], count: 1,
                      measuredGrain: null, mergeFactor: null });
      }
      return [actors, stood.length ? stood.join("; ") : null];
    }

    // ---- step four, the arrival ----

    // WHERE THE ARRIVING WORK CONDENSES, chosen by ranking the three loci the record can carry
    // against each other. A typed floor of 0.55 stood in front of the pole and decided the whole
    // question by itself: over it the arrival was a pole and under it the pole was struck out
    // however plainly the work turned. Now the pole's strength IS the work's own radial reading, a
    // measured seam and a measured gate each stand at whatever the record says of them, and the
    // strongest reading is the locus. Where the record carries none of the three the arrival is
    // carried by the gesture already running, which is a shape and not a refusal.
    //
    // THE WINNING READING'S OWN `fit` TRAVELS AS A THIRD ELEMENT (2026-08-19), beside the kind and
    // the point. It is what `compose` reads to place the arrival's own window edge — how confidently
    // the arriving work's own record names a destination is exactly the reading that belongs there,
    // and it is already computed here to pick the locus in the first place, so returning it copies
    // nothing.
    function locusOf(work) {
      var st = (work || {}).structure || {}, mot = work.motifs || {}, measured = mot.measured || [];
      var rr = st.radial || {}, pool = [], c, y, i, best;
      if (rr.score !== null && rr.score !== undefined && rr.centre) {
        c = mot.radialCentre || rr.centre;
        pool.push({ kind: "pole", at: [r4(c[0]), r4(c[1])], fit: readingOf(rr.score) });
      }
      if (measured.indexOf(MOTIF_SEAM) >= 0) {
        y = (st.horizon || {}).y;
        if (y !== null && y !== undefined) {
          // THE SEAM'S OWN STRENGTH, AND THE RECORD DOES PUBLISH ONE. This read `fit: 1` on the
          // reasoning that the motif list carries only what was measured, so a seam standing on it
          // reads whole. The list says the seam is THERE; how strongly it reads is a different fact
          // and `structure.horizon.seam` carries it — the same field `adrift`'s own seam handles are
          // driven from a few screens below, so the reading was in hand the whole time. A locus
          // published at a flat 1 put the arriving voice's own window at 0 on every pair that
          // carried a seam at all, which is a number that could have been written before either
          // photograph was seen. Where the record carries no strength the seam still stands and
          // `readingOf` answers for it exactly as it does for the pole and the gate.
          pool.push({ kind: "horizon-seam", at: [r4(0.5), r4(y)],
                      fit: readingOf((st.horizon || {}).seam) });
        }
      }
      if (measured.indexOf(MOTIF_GATE) >= 0 && (mot.gateGap || 0) > 0) {
        pool.push({ kind: "gate", at: [r4(0.5), r4(0.5)], fit: readingOf(mot.gateGap) });
      }
      best = null;
      for (i = 0; i < pool.length; i++) {
        if (best === null || pool[i].fit > best.fit) best = pool[i];
      }
      if (best === null || !(best.fit > 0)) return ["none", null, 0];
      return [best.kind, best.at, best.fit];
    }

    // WHETHER THE DEPARTING FIGURE STANDS ON THE LOCUS, asked of the figure's own measured box
    // rather than of a chosen radius. A typed 0.1 stood here as «near»; the box says where the
    // figure is, so the honest question is whether the locus falls inside it.
    function figureOnLocus(work, locus) {
      if (locus === null || locus === undefined) return false;
      var box = (((work || {}).structure || {}).dominantObject || {}).bbox;
      if (!box) return false;
      var x = num(locus[0]), y = num(locus[1]);
      return x >= box[0] && x <= box[2] && y >= box[1] && y <= box[3];
    }

    // THE ARRIVING WORK'S OWN FOLDED SPACE, where the crossing travels along the radial reading and
    // the arriving work reads on rings. A typed 0.55 gated it and is gone: what stands is the shape
    // of the thing — rings open into a world and spokes do not — and the polar record's own strongest
    // reading names which world it is. A record whose polar block says nothing has no world to open,
    // which is absence rather than a floor.
    function worldOf(work, axis) {
      if (axis === null || axis.axis !== "radial") return null;
      var rr = ((work || {}).structure || {}).radial || {};
      if (rr.subType !== "ring") return null;
      var polar = ((work || {}).structure || {}).polar || {}, keys = Object.keys(POLAR_WORLD).sort();
      var best = null, bestv = null, i, v;
      for (i = 0; i < keys.length; i++) {
        v = polar[keys[i]];
        if (v === null || v === undefined) continue;
        if (bestv === null || v > bestv || (v === bestv && keys[i] > best)) {
          best = keys[i];
          bestv = v;
        }
      }
      if (best === null || bestv <= 0) return null;
      return POLAR_WORLD[best];
    }

    // THE CROSSING'S REGISTER, ranked rather than gated. Two typed floors decided this — 0.6 of open
    // ground before an arrival could be an apparition, half the tonal ladder before a crossing could
    // be a provocation — and a precedence order settled the rest. Both floors are gone: the open
    // ground the arriving work measures IS how much of an apparition the arrival is, the tonal gap
    // IS how much of a provocation the crossing is, and the strongest reading names the register.
    // A crossing that opens a world is a discovery whole, because the world is either there or not.
    // THE TONAL GAP reads `luminance.level` — the median of each work's own luminance — rather than
    // `palette.colourfulness`, which stood here before the judge seat's standing correction of
    // 2026-08-18/19 gave the record a genuine tone to read: "half the tonal ladder" above is that
    // reading's own name for itself, and it names a tone now rather than a colourfulness.
    function registerOf(fromW, toW, arrival, world) {
      var pool = [], best = null, i, la, lb;
      // APPARITION NAMES A FIGURE GATHERING OUT OF OPEN GROUND, and that is what all three of
      // CONDENSED, CRYSTALLIZED and PROPAGATED are — a figure condensing at a locus, a seed
      // crystallizing, a copy propagating — never what CARRIED (nothing gathers, the gesture
      // already running just carries on) or INTERFERED (a pair-wide rhythm, not a figure) name
      // (P2 of the 2026-08-27 review, extending shelf 7's three new arrivals the same register
      // reading CONDENSED already had).
      if (arrival === "CONDENSED" || arrival === "CRYSTALLIZED" || arrival === "PROPAGATED") {
        pool.push({ name: "apparition", fit: readingOf((toW.motifs || {}).voidShare) });
      }
      if (world) pool.push({ name: "discovery", fit: 1 });
      la = (fromW.luminance || {}).level;
      lb = (toW.luminance || {}).level;
      if (la !== null && la !== undefined && lb !== null && lb !== undefined) {
        pool.push({ name: "provocation", fit: clamp01(Math.abs(la - lb)) });
      }
      for (i = 0; i < pool.length; i++) {
        if (best === null || pool[i].fit > best.fit) best = pool[i];
      }
      return (best && best.fit > 0) ? best.name : "none";
    }

    // ---- the voices, the levels, the tier ----

    // THE STEP'S ROLE NAMES THE TIER, and nothing else does. Charter shelf 15 makes a step's
    // function the walk's own reading and shelf 17 budgets by that function, so the walk's word is
    // the answer. A second test stood beside it — the pair's widest axis standing over a typed 0.5 —
    // and it OVERRODE the walk: a step the route called a middle became a culmination because two
    // numbers stood far apart. That number was this seat's own invention with no requirement behind
    // it, and it is gone; a step whose role the walk never stated reads as a middle, which is what
    // the entry has always defaulted it to.
    function voiceTheCues(hasTravel, hasArrival, world, role, folds) {
      // A CROSSING THAT FOLDS THE FRAME INTO A SOLID CARRIES ITS MIRACLE ON THE CUE THAT FOLDS IT,
      // wherever that cue stands. `world` is the other way a crossing spends the slot — the
      // arriving work's own space opening — and the two never stand together, which `compose`
      // settles before this is asked.
      var culmination = !!(world || folds) && hasArrival && role === "culmination";
      var voices = {}, any = false, k;
      if (folds === "pivot") voices.pivot = "miracle";
      else if (culmination) voices.pivot = "letter";
      else if (hasTravel || hasArrival) voices.pivot = "accompaniment";
      else voices.pivot = "letter";
      if (hasTravel) {
        voices.travel = (folds === "travel" || world) ? "miracle" : "letter";
      }
      if (hasArrival) voices.arrival = folds === "arrival" ? "miracle" : "letter";
      // A PLAN HAS TO CARRY AT LEAST ONE REAL MOVE, and a miracle is certainly one. This read
      // «letter» alone, so a crossing whose single move is the fold — a folding pivot with no
      // travel and no arrival beside it — had its miracle written back down to a letter and spent
      // nothing for the impossible thing it draws. Shelf 17 counts letters and miracles in separate
      // columns and its middle row takes no letters at all, so a lone miracle is a lawful plan.
      for (k in voices) if (voices[k] === "letter" || voices[k] === "miracle") any = true;
      if (!any) voices.pivot = "letter";
      // A CROSSING THAT FOLDS IS NEVER A QUIET ONE. Shelf 17 gives a quiet link no miracle at all,
      // so a plan whose single move is the fold sits at a middle even with nothing else beside it —
      // and the tier row that judges it is the one that takes a miracle.
      var tier = culmination ? "culmination"
        : ((!(hasTravel || hasArrival) && !folds) ? "quiet" : "middle");
      return [voices, tier];
    }

    // THE TIER A PLAN DECLARES IS THE TIER ITS VOICES ACTUALLY MAKE. §4.7 calls a disagreement
    // between the declared tier and the measured one a red, and the way to agree is to declare what
    // was realised: the tier the shape reached for is tried first, and where its row does not fit
    // the counts the tiers below it are tried in turn. A crossing that reached for a culmination
    // and made a middle is a middle, not a refusal — the visitor sees a passage either way, and the
    // plan says which one it is.
    //
    // What this replaces: a hard refusal. The three rows leave GAPS between them, and the reachable
    // count space is enumerable from `voiceTheCues`' own branches rather than from any collection —
    // a crossing whose frame folds under a pivot with an arrival beside it and no travelling move
    // makes one letter where the culmination row asks for two, which is a middle by the row's own
    // reading and was a glide by the code's. A refusal on a reachable gap is a defect on the gap's
    // own account, and the gap is reachable whatever pictures are hung.
    function tierFor(voices, tier, singsColour) {
      // `accs` SEEDS AT 1 FOR THE CAMERA, deliberately — docs/design/PASS-API-V1.md:463-472, "the
      // camera counts as one accompaniment, amended 2026-08-14 10:31".
      var letters = 0, accs = 1, miracles = 0, k, i, row;
      for (k in voices) {
        if (voices[k] === "letter") letters += 1;
        else if (voices[k] === "accompaniment") accs += 1;
        else if (voices[k] === "miracle") miracles += 1;
      }
      // THE COLOUR VOICE COUNTS ONCE, exactly, shelf 17's own words: colour is an accompaniment
      // voice (shelf 11) and «EVERYTHING counts; no "never counted" class exists». `singsColour` is
      // whether SOME cue of this cast declares the LIGHT-COLOUR level — read in `compose` off the
      // cues that survived its budget loop. However many cues declare it, `ownTheLevels` leaves
      // exactly one of them owning it and takes that level's handles off every other cue's track
      // list, so what reaches the picture is one colour voice however many of its own handles that
      // one owner drives underneath it — the voice is one, not a count of handles.
      if (singsColour) accs += 1;
      var counts = { letters: letters, accompaniments: accs, miracles: miracles };
      function fitsRow(r) {
        return letters >= r.letters[0] && letters <= r.letters[1]
          && accs >= r.accompaniments[0] && accs <= r.accompaniments[1]
          && miracles >= r.miracles[0] && miracles <= r.miracles[1];
      }
      for (i = 0; i < TIERS.length; i++) if (TIERS[i].tier === tier) row = TIERS[i];
      if (row && fitsRow(row)) return [row, counts];
      for (i = TIERS.length - 1; i >= 0; i--) {
        if (TIER_RANK[TIERS[i].tier] < TIER_RANK[tier] && fitsRow(TIERS[i])) {
          return [TIERS[i], counts];
        }
      }
      // NO ROW FITS THE COUNTS, AND THAT IS STILL NOT A REFUSAL. The three rows leave gaps between
      // them — a plan carrying more accompaniments than any row takes, say — and this answered with
      // nothing, which the composer turned into «the declared tier and the realised voices
      // disagree» and the visitor into a plain slide. The honest answer is the row the counts stand
      // NEAREST, measured as how far each count falls outside the row's own span, and the tier
      // declared is the one that was realised. §4.7 calls a plan whose declared tier its own voices
      // contradict a red; naming the nearest row is how the plan stops contradicting itself.
      var bestRow = TIERS[0], bestMiss = null;
      for (i = 0; i < TIERS.length; i++) {
        var r = TIERS[i];
        var miss = Math.max(0, r.letters[0] - letters) + Math.max(0, letters - r.letters[1])
          + Math.max(0, r.accompaniments[0] - accs) + Math.max(0, accs - r.accompaniments[1])
          + Math.max(0, r.miracles[0] - miracles) + Math.max(0, miracles - r.miracles[1]);
        if (bestMiss === null || miss < bestMiss) { bestMiss = miss; bestRow = r; }
      }
      return [bestRow, counts];
    }

    // ---- the meshing instrument's own numbers ----

    // THE MESHING TRAVEL, AND IT ALWAYS HAS NUMBERS. Three refusals stood here — a work with no ring
    // set, a ring count of nothing, and a travel that would run under the size the picture stops
    // reading at — and each of them cost the visitor the whole crossing. All three are now shapings:
    // a work with no measured ring count crosses on the count the instrument itself rests at, and a
    // travel that would run small is lifted onto the instrument's own published minimum, which is
    // where the pair simply stands further from the eye.
    //
    // THE MEASURED THING IS THE RATIO, AND ONLY THE RATIO. The size travels from one end of the
    // crossing to the other so that the pair's apparent tooth pitch holds while its radius grows
    // with the ring count — which is why the two ends stand in the ratio of the two works' own
    // measured ring counts. The two bounds it is fitted between, `SIZE_MIN` and `SIZE_MAX`, are the
    // meshing instrument's own published span for its `size` handle, read from its manifest.
    function meshingTravel(fromW, toW, pivot) {
      var ra = setFor(fromW, "ring"), rb = setFor(toW, "ring"), stood = [];
      var countFrom = ra ? Number(ra.measuredGrain) || 0 : 0;
      var countTo = rb ? Number(rb.measuredGrain) || 0 : 0;
      // WHERE A WORK CARRIES NO RING COUNT the ratio has one end missing, so the mesh rests at the
      // size the instrument rests at and the travel is even. That is the honest picture of a pair
      // with nothing radial to measure — a mesh that holds rather than one that grows — and the
      // plan says so.
      if (!(countFrom > 0) || !(countTo > 0)) {
        stood.push("one of the two works carries no measured ring count, so the mesh holds its own "
                   + "size across the crossing instead of growing with the counts");
        countFrom = countFrom > 0 ? countFrom : countTo;
        countTo = countTo > 0 ? countTo : countFrom;
        if (!(countFrom > 0)) { countFrom = 1; countTo = 1; }
      }
      var toRing = ((toW.structure || {}).radial || {}).subType === "ring";
      // A RING ARRIVAL PINS THE ARRIVING END ON THE INSTRUMENT'S OWN MINIMUM; a spoke arrival stands
      // where the instrument's own handle rests, which is the manifest's default rather than a
      // number chosen here.
      var sizeTo = toRing ? SIZE_MIN : HANDLE_SPECS.gears.size[2];
      var sizeFrom = sizeTo * (countFrom / countTo);
      if (sizeFrom > 0 && sizeFrom < SIZE_MIN) {
        var lift = SIZE_MIN / sizeFrom;
        sizeFrom = SIZE_MIN;
        sizeTo = sizeTo * lift;
      }
      if (sizeFrom < SIZE_MIN) sizeFrom = SIZE_MIN;
      if (sizeTo < SIZE_MIN) sizeTo = SIZE_MIN;
      var over = sizeFrom > SIZE_MAX;
      if (over) sizeFrom = SIZE_MAX;
      if (sizeTo > SIZE_MAX) sizeTo = SIZE_MAX;
      var raw = countTo / (countFrom + countTo);
      var step = roundToInt(raw * (RATIO_STEPS - 1));
      var ratio = r4(step / (RATIO_STEPS - 1));
      var frac = pivot.bandPeriodFrac;
      var lo = HANDLE_SPECS.gears.bandPeriod[0], hi = HANDLE_SPECS.gears.bandPeriod[1];
      var bandPeriod = frac ? r4(Math.min(hi, Math.max(lo, frac))) : null;
      return [{ sizeFrom: r4(sizeFrom), sizeTo: r4(sizeTo), ratio: ratio,
                bandPeriod: bandPeriod, overMax: over,
                measuredCounts: [countFrom, countTo] }, stood.length ? stood.join("; ") : null];
    }

    // THE DOOR IS THE INSTRUMENT'S OWN READING, and this composer only asks (his architecture
    // decision of 2026-08-17 18:00, carried in the charter's Model tail: the instrument reads its
    // doors at run time on the actual buffer; the composer emits the artistic request and bounds).
    //
    // What stood here before: a lookup into lab/data/mesh-doors.json, keyed by a rounded pose, which
    // answered with the nearest size whose doors that ONE measured frame had shown to be whole. It
    // was wrong twice over. It was a table with 1 996 rows whose key carries the pair's own camera
    // pan, so it scaled with the number of pairs (his 19:21 word); and it answered for a 1000 x 1000
    // frame while the visitor's buffer is whatever the phone in their hand reports.
    //
    // What the meshing instrument already does with the request, on the buffer it is drawing on:
    // engine/assets/pass-inst-gears.js `values` reads its own mask at both doors, and where the
    // requested size leaks it searches outward over the whole multiplier — the smaller side first,
    // two rungs of the mesh each way — and draws the first size whose doors are whole. It publishes
    // `sizeRequest`, the size drawn, `sizeRungs` and `doorHeld`, and where no whole size stands
    // within reach it refuses the frame in its own sentence (`doorWhyNo`). Its manifest declares
    // that reach — `size.applied.heldWholeAtADoor` — so the reach has one home and this file keeps
    // no copy of it.
    //
    // So the composer stamps the mesh record with WHO holds the door, and hands the size on as the
    // request it always was. `doorHeldAt` is a plan field and reaches no field of the score: the
    // score's own numbers are `sizeFrom`, `sizeTo`, `ratio` and `bandPeriod`, and they carry the
    // artistic request. The bounds are the handle's published span, which the instrument reads from
    // its own manifest — a copy of it here would be a copy that goes stale.
    function askTheDoors(mesh) {
      var out = {};
      Object.keys(mesh).forEach(function (k) { out[k] = mesh[k]; });
      out.doorHeldAt = "instrument";
      return [out, null];
    }

    // ---- the stack, the levels, the camera ----

    function placeTheStack(order, instrumentOf) {
      var i, stacks = {}, ground = [], named = [], rest = [];
      if (order.length < 2) {
        for (i = 0; i < order.length; i++) stacks[order[i]] = i;
        return [stacks, null];
      }
      for (i = 0; i < order.length; i++) {
        if (FILLS_THE_FRAME[instrumentOf[order[i]]]) ground.push(order[i]);
        named.push("«" + order[i] + "» played by «" + instrumentOf[order[i]] + "»");
      }
      var namedText = named.join(", ");
      if (!ground.length) {
        return [null, "the stack has no ground: no cue of this plan fills the frame, and the "
                + "lowest cue is drawn onto the cleared buffer with no blending — " + namedText];
      }
      if (ground.length > 1) {
        return [null, "the stack has two grounds: more than one cue fills the frame whole, and "
                + "everything beneath the upper one would be drawn and never seen — " + namedText];
      }
      for (i = 0; i < order.length; i++) if (order[i] !== ground[0]) rest.push(order[i]);
      stacks[ground[0]] = 0;
      for (i = 0; i < rest.length; i++) stacks[rest[i]] = i + 1;
      return [stacks, null];
    }

    // WHO DRIVES A LEVEL, AND WHEN. Shelf 17 allows one ACTIVE voice per structural level, and the
    // word that carries the whole law is «active». `castForKinds` already reads it that way: it
    // admits a candidate onto an occupied level provided the two windows never meet, because two
    // voices that are never live together are not two voices on one level. That release was
    // deliberate — the blanket exclusion it replaced starved a three-voice cast down to whatever
    // handful of instruments never touch the ground's own levels.
    //
    // THIS SETTLED OWNERSHIP WITH NO REFERENCE TO ANY WINDOW, AND TOOK THE RELEASE BACK IN SILENCE.
    // One owner per level over every holder, for the whole passage: so the very cue the cast let in
    // because its window does not meet another's had that level's handles stripped from it anyway,
    // for the whole passage, and its `levels` list emptied. The plain case is `overlay`, which
    // declares exactly one level and drives it with every handle it publishes but `mix`: cast as the
    // arrival beside a travelling voice whose window has already shut, it ended holding nothing,
    // drawing its picture and driving none of it. The same shape reached the GROUND, which is on
    // screen from the first frame to the last.
    //
    // So a level is settled among the cues whose windows actually MEET, and a cue is judged once per
    // level against the rivals it is live beside. Two cues that never overlap can each own the same
    // level in their own stretch of the passage, which is what the cast promised them.
    //
    // WHICH RIVAL WINS, AS A STATED RULE. Comparing cue ids as text stood here — `"arrival"` sorts
    // before `"travel"`, so the arrival won every tie — and that is alphabetical order standing in
    // for a rule nobody wrote. The rule is need:
    //
    //   1. ONLY A CUE THAT DRIVES A HANDLE ON THE LEVEL CONTENDS FOR IT. A cue can hold a level and
    //      move nothing on it — its manifest may declare a level no handle of its own drives, or
    //      every handle it has there may be one the register names no reading for, which
    //      `tracksFor` drops. Either way, owning it would silence whichever cue does drive it, for
    //      no picture at all. Where no holder drives it, the holders contend as they are and nobody
    //      is silenced, because there is nothing to silence.
    //   2. THE GROUND HOLDS THE SURFACE. Charter shelf 4 makes the pivot the pair's invariant shared
    //      part, held throughout, and the surface is the floor it holds.
    //   3. OTHERWISE THE CUE THAT NEEDS THE LEVEL MOST TAKES IT — the one with the fewest levels of
    //      its own it actually drives. A cue with one level has nowhere else to be; a cue with two
    //      keeps its voice either way. This is the sentence the alphabet was standing in for.
    //   4. EQUAL NEED GOES TO THE CUE THAT OPENS FIRST, which is the one that establishes the level.
    //   5. AND EQUAL OPENING GOES TO THE LOWER CUE OF THE STACK, which is a fact about the score
    //      rather than about the spelling of a name.
    function ownTheLevels(cues, pivotCueId) {
      var byLevel = {}, out = {}, i, j, cue, lv;
      for (i = 0; i < cues.length; i++) {
        cue = cues[i];
        out[cue.id] = {};
        for (j = 0; j < cue.levels.length; j++) {
          lv = cue.levels[j];
          if (!byLevel[lv]) byLevel[lv] = [];
          byLevel[lv].push(cue);
        }
      }
      Object.keys(byLevel).sort().forEach(function (level) {
        var holders = byLevel[level];
        holders.forEach(function (c) {
          var group = holders.filter(function (d) { return d === c || meets(c, d); });
          var owner = preferredOn(group, level, pivotCueId);
          out[c.id][level] = owner === c ? "owns" : ("accompanies:" + owner.id);
        });
      });
      // EVERY CUE IN A SCORE OWNS A LEVEL OR DRIVES A LEVELLED HANDLE, and this is where that stops
      // being a description and becomes a bound. A cue that owns nothing anywhere and drives nothing
      // of its own is drawing a picture and saying nothing with it. Where one ends that way it is
      // given back the level it needs most, taken from a rival that has somewhere else to be; a
      // rival with nowhere else to be keeps it, because moving the silence from one cue to another
      // answers nothing.
      for (i = 0; i < cues.length; i++) {
        cue = cues[i];
        if (ownsAnything(out[cue.id]) || !drivenLevelsOf(cue).length) continue;
        var want = needOrder(cue, out[cue.id]);
        for (j = 0; j < want.length; j++) {
          var lvl = want[j], holder = null, k;
          for (k = 0; k < cues.length; k++) {
            if (out[cues[k].id][lvl] === "owns" && meets(cue, cues[k])) holder = cues[k];
          }
          if (holder && drivenLevelsOf(holder).length > 1) {
            out[holder.id][lvl] = "accompanies:" + cue.id;
            out[cue.id][lvl] = "owns";
            break;
          }
        }
      }
      return out;
    }

    // Two cues are live together when their windows meet at all.
    function meets(a, b) {
      return num(a.window[0]) < num(b.window[1]) && num(b.window[0]) < num(a.window[1]);
    }

    // Whether this cue drives any handle at all on the named level, read off the tracks it was built
    // with and the level each of those handles publishes. A handle the register names no reading for
    // never reached the track list, so this reads what the cue can actually move rather than what
    // its manifest says it occupies.
    function drivesOn(cue, level) {
      var iid = cue.instrument.id, hs = Object.keys(cue.tracks || {}), i;
      for (i = 0; i < hs.length; i++) if (levelOf(iid, hs[i]) === level) return true;
      return false;
    }

    // The levels this cue actually moves something on, which is how much it needs any one of them.
    function drivenLevelsOf(cue) {
      var out = [], i;
      for (i = 0; i < cue.levels.length; i++) {
        if (drivesOn(cue, cue.levels[i]) && out.indexOf(cue.levels[i]) < 0) out.push(cue.levels[i]);
      }
      return out;
    }

    function ownsAnything(record) {
      var k;
      for (k in record) if (record[k] === "owns") return true;
      return false;
    }

    // The levels this cue drives, neediest first, skipping any it already owns.
    function needOrder(cue, record) {
      return drivenLevelsOf(cue).filter(function (lv) { return record[lv] !== "owns"; }).sort();
    }

    function preferredOn(group, level, pivotCueId) {
      var movers = group.filter(function (c) { return drivesOn(c, level); });
      var pool = movers.length ? movers : group, i, best;
      if (level === "SURFACE") {
        for (i = 0; i < pool.length; i++) if (pool[i].id === pivotCueId) return pool[i];
      }
      best = pool[0];
      for (i = 1; i < pool.length; i++) {
        if (needier(pool[i], best)) best = pool[i];
      }
      return best;
    }

    // Clauses 3, 4 and 5 of the rule above, in that order.
    function needier(a, b) {
      var na = drivenLevelsOf(a).length, nb = drivenLevelsOf(b).length;
      if (na !== nb) return na < nb;
      var oa = num(a.window[0]), ob = num(b.window[0]);
      if (oa !== ob) return oa < ob;
      return num(a.stack) < num(b.stack);
    }

    // THE CAMERA'S OWN FLIGHT, derived from the two works' door framings.
    //
    // THE DOLLY IS A NATURAL LOGARITHM AND NO OTHER BASE. What the score carries is `logScale`, and
    // the host applies exp of it (PASS-API-V1 §6, «logScale IS the logarithm ... the applied factor
    // is exp of it»; the proposed pose record of docs/immersive/wave-a/camera-drivers-conductor.md
    // writes the field as «ln(scale)»). Until 2026-08-17 this line wrote a base-2 logarithm into a
    // field the host exponentiates with base e, so the ratio the camera actually flew was the ratio
    // asked for raised to 1/ln 2 — a request for 1.3 times closer arrived as 1.45 times closer. The
    // two door framings differ by a ratio, and the logarithm of that ratio is what travels.
    //
    // THE DEMAND IS COMPRESSED, NEVER CLIPPED (2026-08-17 22:3x, on the judge's word, after this
    // lane measured the collection and the composer lane measured the saturation). A clamp is
    // CONSTANT on the whole half-line above its bound, so every demand past that bound arrives as the
    // same number — the ordering is destroyed there for every input, and the approach, the one thing
    // a person feels most directly, carries no reading of any pair on any of them. That is his 19:13
    // word about breadth failing in the plainest place there is.
    //
    // And no clamp point is the right one, because what the door framings ask for is the logarithm
    // of a ratio of two framings: it runs the whole real line and is bounded above by nothing, so
    // there is no knee to set a cap at and clamping is the wrong SHAPE whatever number it carries.
    // `CAP · a / (|a| + CAP)` is the same bound written as a limit instead of a wall — it keeps the
    // sign, it is monotone, so a pair asking for more still gets more than a pair asking for less,
    // and it APPROACHES the cap without ever reaching it. Both facts hold over the whole real line
    // and not over any set of photographs: the magnitude of the expression stays strictly under CAP
    // for every finite demand, so NOTHING can land on the bound where a clamp put everything past
    // it; and the map is strictly monotone, so two different demands stay two different approaches.
    // The bound is not loosened by a hair — it is held more tightly than the clamp held it.
    function cameraFlight(pair, axis, locus) {
      var doors = pair.doorFraming;
      var stepFrom = (doors.from || {}).stepPx, stepTo = (doors.to || {}).stepPx;
      var dolly = 0.0, panFrom = [0.0, 0.0], panTo = [0.0, 0.0], ca, cb, asked;
      if (stepFrom && stepTo && stepFrom > 0 && stepTo > 0) {
        asked = Math.log(stepTo / stepFrom);
        dolly = DOLLY_CAP * asked / (Math.abs(asked) + DOLLY_CAP);
      }
      if (axis !== null && axis.from.ends.centre !== undefined
          && axis.to.ends.centre !== undefined) {
        ca = axis.from.ends.centre;
        cb = axis.to.ends.centre;
        panFrom = [num(ca[0]) - 0.5, num(ca[1]) - 0.5];
        panTo = [num(cb[0]) - 0.5, num(cb[1]) - 0.5];
      } else if (locus !== null && locus !== undefined) {
        panFrom = [num(locus[0]) - 0.5, num(locus[1]) - 0.5];
        panTo = [panFrom[0], panFrom[1]];
      }
      return { panFrom: [r4(panFrom[0]), r4(panFrom[1])],
               panTo: [r4(panTo[0]), r4(panTo[1])],
               logScale: r4(dolly),
               carriesCentre: axis !== null && axis.from.ends.centre !== undefined };
    }

    // ---- the shape and its template ----

    // THE THREE WINDOWS, COMPOSED RATHER THAN HANDED OUT (2026-08-19, the polyphony wave). Pivot's
    // stays fixed at `[0, 1]` — charter shelf 4: the pivot is the pair's invariant shared part, held
    // throughout — but travel's own close and arrival's own open used to be fixed too, at 0.86 and
    // at 0.62 or 0.10, and that made every plan's three windows overlap by construction whatever the
    // pair. The levels law forbids two ACTIVE voices on a level, never two voices on a level that
    // are simply never live together, so windows this wide degenerate the law into "no two voices
    // may ever share a level at all" — starving a three-voice cast down to whatever handful of
    // instruments never touch the ground's own two levels (the report on this file's own record
    // names the cluster it starves worst). What is composed here instead is read off the pair:
    //
    //   · TRAVEL'S OWN OPEN is `pivot.strength` — how strongly the two works hold their shared
    //     ground (`pivotOf`, computed once at the top of `compose` and already the reading the
    //     ground itself was cast against). A pair whose ground holds strongly lets the ground solo
    //     longer before the travelling voice joins it; a weakly-held ground gives way sooner.
    //   · TRAVEL'S OWN CLOSE is that same open point carried forward by `reach` — `axis.delta`,
    //     clamped, the two works' own score gap on the travelling axis, the identical reading the
    //     camera's own dolly already reads off the pair a few screens up. `travelOpen +
    //     reach·(1 − travelOpen)`: a pair travelling far down its own axis keeps the travelling
    //     voice on screen for more of what room is left; a pair travelling little hands its level
    //     back sooner.
    //   · ARRIVAL'S OWN CLOSE stays `1.0` — the arriving work has to stand whole at the passage's own
    //     last instant, which is what "arrival" means.
    //   · ARRIVAL'S OWN OPEN is `1 − locusFit·(1 − before)`, where `locusFit` is `locusOf`'s own
    //     winning `fit` — how confidently the arriving work's own record names a destination — and
    //     `before` is the room already established (travel's own open where travel plays, pivot's
    //     otherwise). A confidently-located arrival can afford to open as early as that room allows;
    //     an unconfident one waits near the close it always had.
    //
    // Every one of those is a reading off the two works, off the ground the ground itself already
    // stood on, or off the room the earlier cue already opened — never a share of the passage
    // "nothing measures", so the three windows differ pair to pair because their sources do.
    //
    // THE RHYTHM, AND THE DEVIATION A FURTHER PASS PUTS ON IT, is unchanged by any of the above.
    // §4.8 lets the rhythm and the phases differ across a return, and charter shelf 13 states what a
    // living rhythm is: a base period plus a measured deviation, one instrument per time axis and
    // never two stacked. The base is now the composed window above rather than a typed one, but the
    // deviation still moves only where a cue OPENS, never where it closes — so both doors stand
    // exactly where they stood, the passage still ends when it ends, and the derived duration does
    // not move. What a window can actually breathe by is still THE ROOM IT HAS — the gap between
    // where it opens and where the cue before it opens — and `shift` is still a share of that room,
    // drawn on the die and read at the moment it is needed. A cue standing at the very start has no
    // room and does not move; one standing late has room and breathes in it, and no window can cross
    // the one before it, because the room is what bounds the move.
    function cueWindows(hasTravel, travelOpenBase, travelClose, arrivalOpenBase, shift) {
      var w = { pivot: [0.0, 1.0] }, s = shift || 0, before = 0.0;
      if (hasTravel) {
        w.travel = [travelOpenBase, travelClose];
        w.travel[0] = r4(w.travel[0] - s * (w.travel[0] - before));
        before = num(w.travel[0]);
      }
      w.arrival = [arrivalOpenBase, 1.0];
      w.arrival[0] = r4(w.arrival[0] - s * Math.max(0, w.arrival[0] - before));
      return w;
    }

    function shapeId(pivotInstr, pivotKind, travelInstr, arrivalInstr, voices, arrivalLeads,
                     world) {
      var parts = ["p", pivotInstr, pivotKind, voices.pivot.charAt(0)];
      if (travelInstr) parts = parts.concat(["t", travelInstr, voices.travel.charAt(0)]);
      if (arrivalInstr) parts = parts.concat(["r", arrivalInstr, arrivalLeads ? "lead" : "close"]);
      if (world) parts.push("w");
      return parts.join("-");
    }

    // THE COMPOSER LEAVES THE BALANCE ALONE AT A DOOR, and this is the one place it could reach it.
    // His architecture decision of 2026-08-17 18:00: at a door instant the state belongs to the
    // instrument's own reading of the buffer it is drawing on, and the composer emits the artistic
    // request and the bounds. The woven instrument's `bal` is exactly that state — the share of
    // every band each work holds — and its manifest declares it OPEN, which is the instrument's own
    // way of saying so: a score that names no track for it leaves the instrument deriving the
    // balance from `mix` through its own measured response curve, and a score that DOES name one
    // lands a door wherever its track says, where the doors lane measured 38.4176 of 255 of the
    // other photograph standing in a door that should have been whole.
    //
    // The list is read off the MANIFEST and the open ones are dropped here, so this line is what
    // makes the set of handles a cue drives; a fence standing beside a list that never carried the
    // handle would pass whatever it did. The manifest is the one home of the fact that a handle is
    // open, so nothing here keeps a copy of which one it is.
    // A HANDLE THE REGISTER CANNOT NAME A MEASUREMENT FOR IS NOT DRIVEN. His 19:13 word lifted to
    // the class at 19:21 holds in full: every parameter a score drives names the measurement it
    // reads, so a handle with no row in `HANDLE_SOURCE` gets no track and the instrument's own
    // published default stands. What this replaces is a refusal of the WHOLE crossing.
    function tracksFor(instr, cueId) {
      var manifest = MANIFESTS[instr].handles, handles = Object.keys(manifest).sort();
      var out = {}, i, h;
      for (i = 0; i < handles.length; i++) {
        h = handles[i];
        if (manifest[h].open) continue;
        if (!sourceOf(instr, h)) continue;
        out[h] = { node: cueId + "-" + h };
      }
      return out;
    }

    // THE STRUCTURAL LEVEL ONE HANDLE DRIVES, read off the instrument's own manifest. A handle that
    // drives no structural level — the crossing's own dial, the module's time, the score's die, the
    // fleet's judge channels — declares `null` and answers to no ownership at all.
    function levelOf(iid, handle) {
      var m = iid && MANIFESTS[iid];
      var spec = m && m.handles ? m.handles[handle] : null;
      return spec && spec.level ? spec.level : null;
    }

    // WHETHER THIS CUE MAY DRIVE THIS HANDLE, by shelf 17's levels law. A handle with no level of
    // its own is always driven; one that drives a level is driven only by the cue that owns that
    // level. `levelOwnership` is `ownTheLevels`'s own record, settled once per plan.
    function ownsLevelOf(cue, iid, handle) {
      var lv = levelOf(iid, handle);
      return !lv || !!(cue.levelOwnership && cue.levelOwnership[lv] === "owns");
    }

    // The track list a cue is left with once the levels law has run over it.
    function ownedTracks(iid, tracks, ownership) {
      var out = {}, hs = Object.keys(tracks), i, lv;
      for (i = 0; i < hs.length; i++) {
        lv = levelOf(iid, hs[i]);
        if (lv && ownership[lv] !== "owns") continue;
        out[hs[i]] = tracks[hs[i]];
      }
      return out;
    }

    // WHAT A CUE COSTS, AND IT IS THE INSTRUMENT'S OWN DECLARATION rather than this file's.
    //
    // §7 is unambiguous about who owns this: "an instrument's manifest declares textures, texture
    // slots, framebuffers, ping-pong pairs, programs, passes, per-frame samples and a byte estimate,
    // PER QUALITY VARIANT", the host grants against that declaration at `prepare`, counts what was
    // actually created against it at runtime, and conformance row 22 reds a declaration that
    // understates its bytes. The composer's job is to carry the declaration onto the cue, never to
    // author one — a cost the composer invented would be a number the host then measured a real
    // instrument against.
    //
    // WHAT STOOD HERE AND WHY IT COULD NOT STAND. One block, typed in this function, written into
    // all three quality blocks of every cue of every score: `bytesEstimate: 0` at every quality, the
    // same counts at every quality. Three things followed by construction and none of them about any
    // pair. No crossing could declare a cost different from any other, because one function wrote
    // them all. The quality ladder could not be walked on cost, because the three rungs it writes are
    // the same numbers. And row 22 had nothing to judge: a declaration of nought bytes is understated
    // by every real allocation there can ever be, so the row either never fires or fires on
    // everything, and neither reading is a test.
    //
    // WHAT IS OWED, AND BY WHOM. This function now reads the cue's own instrument's published
    // declaration for the variant asked. Two things have to land before it can read one, and neither
    // is this file's:
    //
    //   · THE INSTRUMENTS must publish real per-variant numbers. All 27 files carry a `resources`
    //     block today and all 27 carry the SAME one, `bytesEstimate` at nothing — a placeholder
    //     repeated fifty-four times, not twenty-seven measurements agreeing.
    //   · THE SITE'S STAGING STEP must carry the block into the settings record. It projects each
    //     manifest down to a fixed field list — api, coverage, cuts, handles, levels, roles — and
    //     `resources` is not on it, so no published manifest this file is ever handed carries one.
    //
    // UNTIL BOTH LAND the placeholder stands, and it stands where a reader can see it is one. It is
    // not a substitute invented here for a measurement: it is the fleet's own placeholder, named as
    // such, kept so no score loses a field it already carries, and it goes the moment the record
    // carries the real declaration — with no further change to this file.
    function resourcesBlock(iid, variant) {
      var own = ((MANIFESTS[iid] || {}).resources || {})[variant];
      if (own) {
        return { bytesEstimate: num(own.bytesEstimate) || 0,
                 framebuffers: num(own.framebuffers) || 0,
                 passes: num(own.passes) || 0,
                 pingPong: num(own.pingPong) || 0,
                 programs: num(own.programs) || 0,
                 textureSlots: num(own.textureSlots) || 0,
                 textures: num(own.textures) || 0,
                 variant: variant };
      }
      return { bytesEstimate: 0, framebuffers: 0, passes: 1, pingPong: 0, programs: 1,
               textureSlots: 2, textures: 0, variant: variant };
    }

    function buildTemplate(shape, spec) {
      var voices = spec.voices;
      var windows = cueWindows(spec.travel !== null, spec.travelOpenBase, spec.travelClose,
                               spec.arrivalOpenBase, spec.rhythmShift);
      var instrumentOf = {}, i, cueId, instr;
      for (i = 0; i < CUE_IDS.length; i++) {
        if (spec[CUE_IDS[i]]) instrumentOf[CUE_IDS[i]] = spec[CUE_IDS[i]];
      }
      var order = CUE_IDS.filter(function (c) { return instrumentOf[c] !== undefined; });
      var placed = placeTheStack(order, instrumentOf), gaveUp = [];
      // A STACK §7's PLACEMENT LAW WILL NOT TAKE GIVES UP ITS TOPMOST VOICE, and it never throws.
      // This threw — «a shape reached the template builder that the placement law refuses» — and a
      // throw on this road takes the whole visit's picture layer down, which is the one failure
      // worse than a plain slide. `compose` already answers the law before it gets here, so this
      // fires for a plan built by some other road; it fits the plan rather than dropping it, and a
      // one-cue stack is exempt by the contract's own sentence, so the loop always ends.
      while (placed[0] === null && order.length > 1) {
        gaveUp.push(order[order.length - 1]);
        delete instrumentOf[order[order.length - 1]];
        order = order.slice(0, -1);
        placed = placeTheStack(order, instrumentOf);
      }
      if (placed[0] === null) placed = [{ pivot: 0 }, null];
      var stacks = placed[0], cues = [];
      for (i = 0; i < CUE_IDS.length; i++) {
        cueId = CUE_IDS[i];
        instr = spec[cueId];
        if (!instr || gaveUp.indexOf(cueId) >= 0) continue;
        cues.push({
          id: cueId,
          instrument: { api: INSTRUMENTS[instr].api, id: instr },
          voice: voices[cueId],
          roles: spec.roles[cueId].slice(),
          // THE LEVEL A CROSSING GAVE UP IS OWNED BY NOBODY. `spec.colourVoice === false` is
          // `compose`'s own word that shelf 17's accompaniment ceiling was already spent by the
          // camera and the ground. The level leaves every cue's declared list, `ownTheLevels` gives
          // it to no one, `ownedTracks` takes its handles off the track lists, and each
          // instrument's own published default stands there — the same road every non-owner in this
          // score already takes. No cue, no instrument and no move is given up. A plan built by some
          // other road carries no such field and is unchanged.
          levels: INSTRUMENTS[instr].levels.filter(function (lv) {
            return spec.colourVoice !== false || lv !== "LIGHT-COLOUR";
          }),
          window: [flt(windows[cueId][0]), flt(windows[cueId][1])],
          works: ["a", "b"],
          stack: stacks[cueId],
          cameraAuthority: "stage",
          doors: { "in": { handle: "mix", value: 0, measured: true },
                   out: { handle: "mix", value: 1, measured: true } },
          tracks: tracksFor(instr, cueId),
          resources: { lean: resourcesBlock(instr, "lean"),
                       standard: resourcesBlock(instr, "standard"),
                       rich: resourcesBlock(instr, "rich") }
        });
      }
      // THE ENTRY DOOR — the charter's build ladder, step 0, and the oldest debt in the engine.
      // Every module was built permanently wet, so a voice could not join a running picture without
      // replacing it; the reserved dry `presence` is what closed that, and this is the plan's half
      // of the contract.
      //
      // A CUE THAT STANDS OVER ANOTHER NAMES ITS DOORS ON THE DRY, at nothing on both sides. The
      // host's own two door laws are chosen by where a voice stands (`pass-layer.js`'s `standsOver`
      // and `presenceWhyNo`): the LOWEST voice is drawn onto the cleared buffer with blending off
      // and must be the departing or the arriving work whole at its doors, while a voice standing
      // above one must be ABSENT at its doors so that what stands beneath shows whole and untouched.
      // A door record names one handle and two values, so an upper voice's door IS its dry — the
      // shape `tests/test_pass_seam.py` walks — and its crossing dial goes on running across its own
      // window like any other letter's, which is what keeps it off its own door proof mid-passage.
      //
      // IT FIRES EXACTLY WHERE THE RESERVED NAME IS MEANT. `sourceOf` answers `entry-door` only for
      // an instrument whose `presence` is the fleet's reserved dry; `overlay`'s own `presence` is a
      // LIGHT-COLOUR reading of the pair and carries a scoped row of its own, so its doors and its
      // scores are untouched by this and stay byte-identical.
      //
      // AND THE LOWEST CUE IS NEVER GIVEN A ZERO DOOR HERE. `stack` of nought is the ground — the
      // one cue that fills the frame — so the branch cannot write the door `presenceWhyNo` refuses.
      for (i = 0; i < cues.length; i++) {
        if (num(cues[i].stack) > 0 && cues[i].tracks.presence
            && (sourceOf(cues[i].instrument.id, "presence") || [])[0] === "entry-door") {
          cues[i].doors = { "in": { handle: "presence", value: 0, measured: true },
                            out: { handle: "presence", value: 0, measured: true } };
        }
      }
      var levels = ownTheLevels(cues, "pivot");
      for (i = 0; i < cues.length; i++) {
        cues[i].levelOwnership = levels[cues[i].id];
        // A NON-OWNER RESTS ON THE LEVEL IT LOST AND GOES ON PLAYING THE LEVEL IT OWNS. This is
        // shelf 17's levels law applied where a viewer can actually see it — at the handles. Every
        // handle an instrument publishes now declares, in that instrument's own manifest, the
        // structural level it drives; a cue that does not own that level has the handle taken off
        // its track list here, so the client writes the manifest's own default for it and the cue
        // is genuinely silent there. The cue goes on driving every handle whose level it does own,
        // and every handle that drives no structural level at all.
        //
        // WHAT THIS REPLACES. One level had this gate and five did not: `singsLightColour` held the
        // eighteen colour and light handles of three instruments, and on CELL, SURFACE, TEXTURE,
        // CELL CONTENT and WORLD nothing pinned anything — a cue that did not own CELL still wrote
        // every CELL-driving handle it had and still drew its pattern, so two patterns landed in one
        // passage and shelf 18's ban on pattern stacked on pattern was broken in the plain sense a
        // person sees on the screen. The gate is the same one; what changed is that the fact it
        // reads is published per handle instead of being known for one level in this file.
        cues[i].tracks = ownedTracks(cues[i].instrument.id, cues[i].tracks, levels[cues[i].id]);
        cues[i].levels = cues[i].levels.filter(function (lv) {
          return levels[cues[i].id][lv] === "owns";
        });
      }
      // THE WITNESS CAMERA'S OWN FLIGHT (charter shelf 2). THE TWO ENDS STAY HONEST — the
      // departing work stands at "a" and the arriving one rests at "b", each at the plain neutral
      // pose, pan and logScale at zero and pitch, yaw and roll at zero — and NOTHING BELOW EVER
      // TOUCHES THEM. Between them the flight now gets an outbound pose and an inbound pose on
      // EVERY pair, not only where the meshing instrument happens to play: until 2026-08-19 this
      // middle was built only where `spec.travel === "gears"`, so on every pair that did not carry
      // the gears instrument — most of the collection — the camera's own four points wrote the
      // same all-zero pose four times, which reads on screen as no camera at all. `fillPlan` below
      // fills BOTH middle points' every place — pan, logScale, pitch, yaw and roll — off the two
      // works' own measured record, so the placeholders here are only the shape of the two points;
      // what they carry is written once the two works' own record is in hand.
      var track = [{ at: "a", pan: { x: 0, y: 0 }, logScale: 0, pitch: 0, yaw: 0, roll: 0,
                     fov: null, owner: "stage" }];
      track.push({ at: "@atFrom", pan: { x: "@panFromX", y: "@panFromY" },
                   logScale: "@logScale", pitch: "@pitchFrom", yaw: "@yaw", roll: "@roll",
                   fov: null, owner: "stage" });
      track.push({ at: "@atTo", pan: { x: "@panToX", y: "@panToY" },
                   logScale: "@logScale", pitch: "@pitchTo", yaw: "@yaw", roll: "@roll",
                   fov: null, owner: "stage" });
      track.push({ at: "b", pan: { x: 0, y: 0 }, logScale: 0, pitch: 0, yaw: 0, roll: 0,
                   fov: null, owner: "stage" });
      var quality = {};
      ["lean", "standard", "rich"].forEach(function (v) {
        var perCue = {};
        cues.forEach(function (c) {
          perCue[c.id] = { resources: resourcesBlock(c.instrument.id, v) };
        });
        quality[v] = { renderScale: null, cues: perCue };
      });
      return {
        shape: shape,
        schema: SCHEMA,
        tier: spec.tier,
        duration: spec.duration,
        middle: spec.middle,
        budget: spec.budget,
        cues: cues,
        camera: { owner: "stage", rests: "b", track: track },
        interruption: { withinMs: 500, resolve: "nearest-door" },
        failLand: "arrive",
        quality: quality,
        intent: INTENT_TEMPLATES[spec.intentKey],
        intentKey: spec.intentKey,
        road: spec.road, role: spec.role, passIndex: spec.passIndex
      };
    }

    // ---------------------------------------------------------------------------------------
    // THE GENRES — the plural sources of a crossing's structure, ranked and never gated
    // ---------------------------------------------------------------------------------------
    //
    // HIS WORD NAMES THEM, AND HIS WORD IS THE BETTER NAME. 2026-08-18 09:53: «замеры просто
    // помогают ранжировать жанр перехода что больше подойдет и по каким параметрам» — the
    // measurements rank the GENRE of crossing that suits a pair better than the others, and set the
    // parameters inside the genre that wins. They never admit and they never reject. This file
    // called them «roads» until then; the word is his and it stays.
    //
    // HIS WORD OF 2026-08-17 18:56 STANDS UNDER IT: «the axes that differ most travel» is ONE lawful
    // derivation among several and never the whole formula. Equally lawful: a crossing along what
    // the pair SHARES, the shared measure held while everything outside it travels; one built from
    // HOW A WORK IS MADE — a radial work spins or opens into a rosette, a symmetric work slides its
    // parts along its own symmetry or becomes stripes, a work folding along strong directions folds
    // into a solid; and one along the pair's DISSIMILAR axes with the mystery in the middle.
    //
    // WHAT CHANGED ON 2026-08-18, AND IT IS THE WHOLE SHAPE. Each genre used to state the
    // measurements that QUALIFIED a pair for it and the ones that DISQUALIFIED it, and a pair that
    // qualified for none fell to one nominated road. Seven of the eight therefore carried an
    // admission test with a typed number inside it — a tight radial floor, a tight band floor, a
    // tight region floor, four faces, a similar span of 0.15, a mystery distance of 0.5 — and a
    // pair that read a hair under one was not merely ranked lower, it was struck out.
    //
    // Now EVERY GENRE IS A CANDIDATE FOR EVERY PAIR, and each answers with a FIT — a reading between
    // nothing and whole, taken off the two works' own records — plus the sentence saying what it
    // read. The die runs over the fits, so the best-suited is the likeliest, a pinned seed
    // reproduces the choice (charter shelf 16) and a fresh seed varies it. A fit of nothing means
    // this pair gives that genre nothing to work with; it is last, and it still plays where nothing
    // else stands higher. There is no fallback genre and no last candidate — his word of 10:15,
    // «я не просил запасную дорогу» — because the list is never empty: every genre always answers,
    // so nothing needs catching.
    //
    // A GENRE ANSWERS FIVE QUESTIONS AND NOTHING ELSE, and the machinery below it is unchanged:
    //   ground   the measure the crossing holds still, or null to let the pair's own ranking say
    //   free     the measure this genre needs left free to travel, so the ground never holds it
    //   axis     how the travelling axis is picked — a measure name pins it, "near" takes the
    //            closest reading of the two works, "far" the most distant
    //   miracle  whether this genre may spend the crossing's one miracle on a folded space
    //   moves    how many structural gestures it reaches for, before the role's budget cuts it back

    // The travelling axis, picked the way a genre asks. "far" is the reading this file has always
    // had — the axes that differ most travel. "near" runs the crossing along the pair's most similar
    // axis; a measure name pins the axis to that measure or answers with nothing.
    function travellingAxisOn(fromW, toW, held, pick) {
      if (!pick || pick === "far") return travellingAxis(fromW, toW, { measure: held });
      var best = null, bestRaw = 0, i, axis, ra, rb, delta;
      for (i = 0; i < TRAVEL_AXES.length; i++) {
        axis = TRAVEL_AXES[i];
        if (axis === held) continue;
        if (pick !== "near" && axis !== pick) continue;
        ra = axisReading(fromW, axis);
        rb = axisReading(toW, axis);
        if (ra === null || rb === null) continue;
        delta = Math.abs(ra.score - rb.score);
        if (best === null || delta < bestRaw || (delta === bestRaw && axis > best.axis)) {
          best = { axis: axis, delta: r4(delta), from: ra, to: rb };
          bestRaw = delta;
        }
      }
      return best;
    }

    // EVERY GENRE THIS PAIR COULD CROSS ON, EACH WITH ITS OWN FIT.
    //
    // Nothing is qualified and nothing is disqualified. Each genre reads the two records, answers
    // with how well it suits them and says what it read; the reading is the ranking, and the ranking
    // is all a measurement is for. Where a genre used to be struck out — «the strongest radial
    // reading is under the tight floor», «the closest axis is past the span a similar road runs
    // inside», «the departing work cuts into 3 real panels, under the 4 a box needs» — the same
    // sentence now rides a low fit, so a poor fit is still playable and still explains itself.
    //
    // A FIT OF NOTHING IS STRUCTURAL, NEVER A FLOOR. Two band families that run the same way give
    // the crossing nothing to cross, so `stripes` reads nothing for that pair; two that cross give
    // `symmetry-slide` no one symmetry to slide along, so it reads nothing. That is the pair
    // answering, not a bar this file set.
    function genresFor(fromW, toW) {
      var all = groundReadings(fromW, toW), genres = [], notes = [];
      function say(id, genre, fit, why) {
        genre.id = id;
        genre.fit = clamp01(fit);
        genre.why = why;
        genres.push(genre);
        notes.push({ genre: id, road: id, fit: r4(clamp01(fit)), why: why });
      }
      var rFrom = (fromW.structure || {}).radial || {}, rTo = (toW.structure || {}).radial || {};
      var bFrom = (fromW.structure || {}).banding || {}, bTo = (toW.structure || {}).banding || {};
      var gFrom = (fromW.structure || {}).regions || {};

      // 1 · ALONG WHAT THE PAIR SHARES. Two readings make it: the strongest ground the pair holds
      // between them, and how CLOSE their nearest other axis stands, since that axis is what the
      // crossing runs along. A pair whose every other axis stands far apart suits this genre less —
      // it does not fail it.
      var heldGround = null, i, m;
      for (i = 0; i < MEASURES.length; i++) {
        m = MEASURES[i];
        if (heldGround === null || num(all.per[m].min) > num(all.per[heldGround].min)) heldGround = m;
      }
      var nearAxis = heldGround === null ? null : travellingAxisOn(fromW, toW, heldGround, "near");
      if (nearAxis === null) {
        say("shared-ground", { ground: heldGround, free: null, axis: "near", miracle: false,
                               moves: 2 }, 0,
            "beside the shared " + pyText(heldGround) + " no axis reads on both works, so there is "
            + "no similar axis to run along");
      } else {
        var closeness = 1 - clamp01(num(nearAxis.delta));
        say("shared-ground", { ground: heldGround, free: null, axis: "near", miracle: false,
                               moves: 2 },
            num(all.per[heldGround].min) * closeness,
            "the pair holds " + heldGround + " at " + pyText(all.per[heldGround].min)
            + " and their " + nearAxis.axis + " readings stand "
            + pyText(nearAxis.delta) + " apart");
      }

      // 2 and 3 · BUILT FROM HOW A RADIAL WORK IS MADE. The radial reading has to stand on BOTH
      // works for the genre to suit — the bridge computes both structures and a radial crossing
      // played on one work's centre alone reads as laid on rather than found — so the fit is the
      // weaker of the two readings. Which of the two genres it is the ARRIVING work's own subtype
      // answers: rings open into a rosette, which is a folded space and the crossing's one miracle,
      // while spokes turn, which is a spin and no miracle at all.
      var radialAxis = travellingAxisOn(fromW, toW, null, "radial");
      var radialPair = Math.min(readingOf(rFrom.score), readingOf(rTo.score));
      var arrivesOnRings = rTo.subType === "ring";
      var radialFit = radialAxis === null ? 0 : radialPair;
      say("kaleidoscope", { ground: null, free: "radial", axis: "radial", miracle: true, moves: 3 },
          arrivesOnRings ? radialFit : 0,
          arrivesOnRings
            ? ("the arriving work reads radial at " + pyText(flt(r4(readingOf(rTo.score))))
               + " on rings and the pair holds radial at " + pyText(flt(r4(radialPair)))
               + ", so the rings open")
            : ("the arriving work's radial reading is on " + pyText(rTo.subType)
               + " rather than on rings, so there is nothing to open"));
      say("spin", { ground: null, free: "radial", axis: "radial", miracle: false, moves: 2 },
          arrivesOnRings ? 0 : radialFit,
          arrivesOnRings
            ? "the arriving work's radial reading is on rings, which open rather than turn"
            : ("the arriving work reads radial at " + pyText(flt(r4(readingOf(rTo.score))))
               + " on " + pyText(rTo.subType) + " and the pair holds radial at "
               + pyText(flt(r4(radialPair))) + ", so its own turn is what travels"));

      // 4 and 5 · BUILT FROM HOW A SYMMETRIC WORK IS MADE. A band family is a translational symmetry
      // the measure files actually carry, so it is the symmetry these two read. The fit is the
      // weaker of the two band readings, and it is nothing where a family carries no period at all —
      // a band family with no period is a score with nothing to slide. The two works' own band
      // DIRECTIONS say which of the two genres this pair suits: where they agree the parts slide
      // along that one symmetry and the fabric has nothing to cross, and where they cross it is the
      // other way about.
      var bandAxis = travellingAxisOn(fromW, toW, null, "banding");
      var bandPair = Math.min(readingOf(bFrom.score), readingOf(bTo.score));
      var periods = Number(bFrom.periodPx) > 0 && Number(bTo.periodPx) > 0;
      var bandFit = (bandAxis === null || !periods) ? 0 : bandPair;
      var sameWay = bFrom.axis === bTo.axis;
      say("symmetry-slide", { ground: null, free: "banding", axis: "banding", miracle: false,
                              moves: 2 },
          sameWay ? bandFit : 0,
          !periods ? "one of the two band families carries no measured period"
            : (sameWay
               ? ("both works band " + pyText(bFrom.axis) + ", at "
                  + pyText(flt(r4(Number(bFrom.periodPx) || 0))) + " and "
                  + pyText(flt(r4(Number(bTo.periodPx) || 0)))
                  + " px, and the pair holds banding at " + pyText(flt(r4(bandPair)))
                  + ", so the parts slide along one symmetry")
               : "the two band families run different ways, so there is no one symmetry to slide "
                 + "along"));
      say("stripes", { ground: null, free: "banding", axis: "banding", miracle: false, moves: 2 },
          sameWay ? 0 : bandFit,
          !periods ? "one of the two band families carries no measured period"
            : (sameWay ? "the two band families run the same way, so nothing crosses"
               : ("the two band families cross — " + pyText(bFrom.axis) + " against "
                  + pyText(bTo.axis) + " — and the pair holds banding at "
                  + pyText(flt(r4(bandPair))) + ", so the fabric becomes stripes")));

      // 6 · A WORK FOLDING ALONG STRONG DIRECTIONS FOLDS INTO A SOLID. The crease is placed on the
      // departing work's own measured region line, so the fit is that work's region reading. What
      // used to stand here was a chain of four admission tests — the region reading over a tight
      // floor, four faces, both works over the discriminating threshold, and a ground the pair could
      // hold — and one of them refused the genre for want of an instrument that cuts on panels, a
      // want this collection has not had since the folding instrument landed. A solid with one face
      // is no solid, so a work that falls into no panel at all reads nothing here; everything else
      // is a reading.
      var faces = facesOf(fromW);
      say("box-fold", { ground: "regions", free: null, axis: "far", miracle: true, mustFold: true,
                        moves: 3 },
          faces >= 2 ? readingOf(gFrom.score) : 0,
          faces >= 2
            ? ("the departing work reads regions at "
               + pyText(flt(r4(readingOf(gFrom.score)))) + " over " + faces + " faces")
            : ("the departing work cuts into " + faces + " panels, so there is nothing to fold "
               + "into a solid"));

      // 7 · ALONG THE PAIR'S DISSIMILAR AXES, WITH THE MYSTERY IN THE MIDDLE. The distance between
      // the pair's widest two readings IS the fit — a pair standing far apart suits this genre and a
      // pair standing close does not — where a typed 0.5 used to decide the question outright.
      var farAxis = travellingAxisOn(fromW, toW, heldGround, "far");
      say("dissimilar-mystery", { ground: null, free: null, axis: "far", miracle: true, moves: 2 },
          farAxis === null ? 0 : clamp01(num(farAxis.delta)),
          farAxis === null ? "no measure carries a reading on both works"
            : ("the two works read " + farAxis.axis + " " + pyText(farAxis.delta) + " apart"));

      // 8 · THE TONAL ZONES AND THE DETAIL SCALES. The highlights leave before the shadows, and the
      // arriving work's blurred mass grows first with its detail growing into it — two
      // decompositions that read on any two photographs by construction, which is why this genre
      // answers for every pair. It carried a special status until 2026-08-18: it was reached only
      // when every other road had turned the pair away, and a candidate reachable only after every
      // rival has refused is selected by those refusals and not by its own fit. They were never
      // choosing it — the floors pushed them there. Its
      // fit is the pair's own tonal and spectral closeness and it competes on that, like the seven
      // above it.
      var bridge = tonalSpectral(fromW, toW);
      say("tonal-and-spectral", { ground: null, free: null, axis: "far", miracle: true, moves: 2 },
          Math.min(bridge.tonal, bridge.spectral),
          "the two works' tonal grounds stand at " + pyText(flt(r4(bridge.tonal)))
          + " of each other and their detail scales at " + pyText(flt(r4(bridge.spectral))));

      return { genres: genres, notes: notes };
    }

    // How many real panels the departing work cuts into — the box law's faces, counted off the
    // work's own element sets rather than assumed. PANELS ONLY: a named region is a thing in the
    // picture and a panel is a piece of the frame, and it is pieces of the frame that become faces
    // of a solid. Counting named regions here let the road qualify on works the fold's own ground
    // could never be cast from.
    function facesOf(work) {
      var most = 0, i, s, sets = (work || {}).sets || [];
      for (i = 0; i < sets.length; i++) {
        s = sets[i];
        if (s.kind === "panel" && s.realCount > most) most = s.realCount;
      }
      return most;
    }

    // THE FAMILY A CROSSING BELONGS TO, IN THE WALK'S OWN WORDS. The name is not this file's to
    // invent: the walk reads it off the composed plan by the lab builder's own law — the transform
    // the pivot's cut implies, joined by a plus sign to the measure the passage travels, or «tone»
    // where nothing travels — and hands it straight back inside §4.8's return reference. A second
    // idea of what a family is would make every return unrecognisable, so this function computes
    // the SAME token from the same two readings, one step earlier: before a road is composed, so
    // the road that keeps a recorded family can be chosen rather than discovered afterwards.
    //
    // It carries no direction, and that is what makes a return kin: both halves — the pivot's
    // transform and the travelling measure — are read from both works at once.
    function familyToken(transform, axisName) {
      return String(transform || "tone_bridge") + "+" + String(axisName || "tone");
    }

    function familyOf(road, fromW, toW, seed) {
      // The ground is rolled on the edge's own key, so this predicts the same one `compose` will
      // stand on — and the same one whichever way the passage runs.
      var p = pivotOfPair(fromW, toW, road.free, road.ground, false, seed,
                          groundKeyOf(fromW, toW));
      var held = p.kind === "shared-measure" ? p.value.measure : null;
      var axis = travellingAxisOn(fromW, toW, held, road.axis);
      if (axis === null && road.axis !== "far" && road.axis !== "near") {
        axis = travellingAxisOn(fromW, toW, held, "far");
      }
      return familyToken(p.value.transform, axis ? axis.axis : null);
    }

    // The measure a transform implies, which is CUT_OF_MEASURE read the other way about. A return
    // whose recorded family names a transform can therefore ask for the ground that produced it.
    var MEASURE_OF_TRANSFORM = {};
    Object.keys(CUT_OF_MEASURE).forEach(function (m) {
      MEASURE_OF_TRANSFORM[CUT_OF_MEASURE[m][1]] = m;
    });

    // THE DIE, and the one place a road is rolled. The walk's own die (§4.4g: the visit's seed, the
    // pass index and the edge's key, in one number) is mixed with the edge's key, so two edges of
    // one walk running on one die still choose differently; a pinned seed reproduces every choice
    // exactly, which is charter shelf 16's judging mode, and a fresh seed varies it, which is the
    // viewer's.
    function dieAmong(seed, key, n) {
      var salt = key + "|" + Math.round(Number(seed) * 1e6), h = 2166136261, i;
      for (i = 0; i < salt.length; i++) {
        h = Math.imul(h ^ salt.charCodeAt(i), 16777619) >>> 0;
      }
      return n > 0 ? h % n : 0;
    }

    // ---------------------------------------------------------------------------------------
    // THE STEP'S ROLE IN THE WALK, and the visit's memory of this edge
    // ---------------------------------------------------------------------------------------
    //
    // Charter shelf 17 gives the voice budget of three roles by measurement — a quiet link carries
    // one letter, at most one accompaniment, no miracle and 2 to 4 seconds; a middle at most two
    // letters, at most two accompaniments, at most one miracle and 5 to 8 seconds; a culmination
    // two or three letters, at most three accompaniments, exactly one miracle and 9 to 14 seconds.
    // An entrance and a return are the walk's two ends and read as their own roles: shelf 15 maps
    // them onto the harmonic grammar, where a return is a landing at home and an entrance the
    // motion away that prepares. Their two numbers are this seat's and stand on the revisit list.
    //
    // The role does three things and no fourth. It BOUNDS what the composer emits, which is the
    // budget above — the letters it may spend and the tier it may reach. It says whether the step
    // may spend a miracle at all. And it names the register the composer reaches for — which roads
    // belong to a quiet link and which to a culmination — so two neighbouring edges of one walk stop
    // resembling each other even where the two pairs read alike.
    //
    // THE LENGTH IS A BAND AND NEVER A NUMBER, AND THE BAND IS THE TIER'S. Each role carried ONE
    // typed duration here until now — 5000, 3000, 6500, 11000, 4000 — and the composition read it
    // straight off, so two different pairs at one role ran the same number of milliseconds to the
    // millisecond. That is a parameter pinned to one value for the whole crossing, which is the
    // named failure. Shelf 17 names THREE bands of seconds and no more — 2 to 4 at a quiet tier,
    // 5 to 8 at a middle, 9 to 14 at a culmination — so a role gets no band of its own: it gets the
    // band of the tier it declares, read off `TIERS` above rather than copied beside it, and the
    // pair's own reading places the length inside that band (`compose`, where the length is taken).
    // A fourth band written here would be this seat naming a number the charter does not.
    var ROLE_BUDGETS = {
      "entrance":    { tier: "middle", miracle: false, letters: 2 },
      "quiet link":  { tier: "quiet", miracle: false, letters: 1 },
      "middle":      { tier: "middle", miracle: true, letters: 2 },
      "culmination": { tier: "culmination", miracle: true, letters: 3 },
      "return":      { tier: "quiet", miracle: false, letters: 1 }
    };
    // Shelf 17's band of seconds for a named tier, and the one road to it. `TIERS` is where the
    // three bands live; a caller naming a tier that has no row is answered with the middle's, the
    // same default every other reading of an unstated tier takes.
    function bandOfTier(tier) {
      var i;
      for (i = 0; i < TIERS.length; i++) if (TIERS[i].tier === tier) return TIERS[i].band;
      return TIERS[1].band;
    }
    // SHELF 17'S OWN CEILING FOR ONE COLUMN OF A NAMED TIER, and the one road to it. `TIERS` is
    // where the three rows live, so a ceiling is read off the row rather than copied beside it; a
    // caller naming a tier that has no row is answered with the middle's, the same default
    // `bandOfTier` above already takes.
    function ceilingOfTier(tier, column) {
      var i;
      for (i = 0; i < TIERS.length; i++) if (TIERS[i].tier === tier) return TIERS[i][column][1];
      return TIERS[1][column][1];
    }
    // WHERE A LENGTH LANDS INSIDE A BAND. It is a pure arithmetic and it travels beside the entry
    // with the others (the note over the export at the foot of this file), because what it claims is
    // a claim about NUMBERS: every band this table names, walked against every share between nothing
    // and whole, lands between the band's own two numbers. `clamp01` is the last thing that touches
    // the share, so a caller handing it anything at all cannot put the length outside; a share of 0
    // gives the floor exactly, a share of 1 the ceiling exactly, and the placement is monotone
    // between them because it is a straight line in the share.
    function lengthInBand(band, share) {
      return roundToInt(band[0] + clamp01(share) * (band[1] - band[0]));
    }
    // The register each role reaches for, as a list of roads in the order the role prefers them. A
    // role whose list catches none of the roads a pair qualifies for takes what qualifies and says
    // so on the plan, because a step of the walk still has to play.
    var ROLE_ROADS = {
      "entrance": ["stripes", "symmetry-slide", "spin", "dissimilar-mystery"],
      "quiet link": ["shared-ground", "symmetry-slide"],
      "middle": null,
      "culmination": ["kaleidoscope", "box-fold", "spin", "dissimilar-mystery"],
      "return": ["shared-ground", "symmetry-slide", "stripes"]
    };

    // One genre standing on a named ground, without touching the genre it was made from.
    function withGround(road, ground) {
      var out = {}, k;
      for (k in road) out[k] = road[k];
      out.ground = ground;
      out.free = road.free === ground ? null : road.free;
      return out;
    }

    // THE GENRE THIS PASSAGE RUNS ON: the fits the pair itself gave, the register the role reaches
    // for, what the visit already played on this edge, and the die over the ranking.
    //
    // NOTHING IS EVER EMPTY HERE. Every genre is a candidate for every pair, so the pool this walks
    // is the whole vocabulary and `order` below is the whole vocabulary too, best-suited first. Two
    // returns stood at the head of this function — one for a pair that qualified for no road, one
    // for a step with no miracle whose every qualifying road folded — and both handed back the
    // one nominated road as a consolation. Neither can arise now, and neither is written.
    function genreFor(fromW, toW, role, memory, seed, key) {
      var found = genresFor(fromW, toW);
      var pool = found.genres.slice(), reach = null, held = null, wanted, kept, i, fam;
      // A GENRE THAT MUST SPEND THE MIRACLE IS UNREACHABLE WHERE THE ROLE HAS NONE, and that is
      // shelf 17's own law rather than a number: a quiet link carries no miracle, and this seat
      // gives an entrance and a return none either. The other genres that MAY spend one simply do
      // not, where the reading that would fold the space does not stand; this one cannot play at all
      // without folding, because the fold IS what it is. So it stands down at those three roles and
      // the rest of the vocabulary — all seven of it — is still in hand.
      var spendsAMiracle = ROLE_BUDGETS[role] && ROLE_BUDGETS[role].miracle;
      if (!spendsAMiracle) {
        pool = pool.filter(function (r) { return !r.mustFold; });
      }
      // THE REGISTER THE ROLE REACHES FOR, which is charter shelf 15's reading of a step's function
      // and his law rather than this seat's taste. It ORDERS the pool and never empties it: where
      // none of the genres the register names suits this pair at all, the pool stands as it is and
      // the plan says the step played outside its own register.
      wanted = ROLE_ROADS[role];
      if (wanted) {
        kept = pool.filter(function (r) { return wanted.indexOf(r.id) >= 0 && r.fit > 0; });
        if (kept.length) {
          pool = kept;
        } else {
          reach = "the step is a " + role + " and no genre of that register suits this pair, so it "
            + "plays the genre that suits it best";
        }
      }
      if (!pool.length) pool = found.genres.slice();
      // THE VISIT'S MEMORY. §4.8: what holds across a return is the family AND the pivot, and
      // everything else — the order of the moves, the actors, the rhythm, the camera's route — may
      // differ. The genres read the direction — an arriving work reading on rings is not an arriving
      // work reading on rings the other way about — so the kinship is answered here, in three steps,
      // each weaker than the one before it and each still lawful:
      //
      //   1. a genre whose family IS the recorded one. The die is not rolled at all: kinship
      //      outranks variety, and the variety is carried by everything the family does not fix.
      //   2. failing that, a genre standing on the same PIVOT, which §4.8 accepts in the family's
      //      place.
      //   3. failing that, the ground the recorded transform implies is FORCED onto the genre the
      //      die picked, so the pivot holds even where no genre would have stood on it by itself.
      //
      // Where all three fail the crossing takes its own genre and says so, and the walk's own judge
      // is what reads that back.
      var wantTransform = memory && memory.family ? String(memory.family).split("+")[0] : null;
      var heldBy = null;
      if (memory && memory.family) {
        var whole = pool.concat(found.genres);
        for (i = 0; i < whole.length; i++) {
          if (familyOf(whole[i], fromW, toW, seed) === memory.family) {
            held = whole[i];
            heldBy = "family";
            break;
          }
        }
        if (held === null) {
          for (i = 0; i < whole.length; i++) {
            fam = familyOf(whole[i], fromW, toW, seed);
            if (fam.split("+")[0] === wantTransform) {
              held = whole[i];
              heldBy = "pivot";
              break;
            }
          }
          if (held !== null) {
            reach = "the visit remembers «" + String(memory.family) + "» on this edge and this "
              + "pair no longer reaches it the other way about, so the crossing keeps its pivot "
              + "and travels elsewhere";
          }
        }
        if (held === null && MEASURE_OF_TRANSFORM[wantTransform]) {
          held = withGround(pickGenre(pool, seed, key), MEASURE_OF_TRANSFORM[wantTransform]);
          heldBy = "ground";
          reach = "the visit remembers «" + String(memory.family) + "» on this edge and no genre "
            + "reaches it, so its ground is held under the genre the die picked";
        }
        if (held === null) {
          reach = "the visit remembers the family «" + String(memory.family) + "» on this edge and "
            + "this pair can hold neither it nor its pivot, so the crossing takes a genre of its own";
        }
      }
      var genre = held || pickGenre(pool, seed, key);
      // THE ORDER THE GENRES ARE TRIED IN. A genre can still turn out unplayable for this pair after
      // the die has picked it — §7's placement law refuses a stack whose lowest cue leaves the frame
      // open — and a step of the walk still has to play. So the die's own pick comes first and the
      // whole vocabulary follows, best-suited first, with the ones the register does not name behind
      // the ones it does. Nothing is left out of the order, because nothing was ever turned away.
      var ranked = found.genres.slice().sort(function (x, y) {
        if (y.fit !== x.fit) return y.fit - x.fit;
        return x.id < y.id ? -1 : (x.id > y.id ? 1 : 0);
      });
      var order = [genre], i2;
      for (i2 = 0; i2 < pool.length; i2++) if (order.indexOf(pool[i2]) < 0) order.push(pool[i2]);
      for (i2 = 0; i2 < ranked.length; i2++) {
        if (order.indexOf(ranked[i2]) < 0) order.push(ranked[i2]);
      }
      return { road: genre, genre: genre, order: order,
               family: familyOf(genre, fromW, toW, seed),
               notes: found.notes,
               qualified: ranked.map(function (r) { return r.id; }),
               ranking: ranked.map(function (r) { return { genre: r.id, fit: r4(r.fit) }; }),
               reach: reach, heldFamily: held ? memory.family : null, heldBy: heldBy };
    }

    // THE INSTRUMENT THAT FILLS THE FRAME AND SUITS THIS PAIR BEST. §7's coverage law asks the
    // lowest cue of a stack to leave nothing of the frame open, and an instrument declares in its
    // own manifest whether it does — so this ranks the ones that do and hands the best-suited over.
    // It is what a stack with no ground reaches for before any voice is given up.
    // `sole` NAMES THE LEVELS A VOICE ABOVE THE GROUND CANNOT GIVE UP — the ones it drives and has
    // no second level of its own to fall back on. A ground that declares one of them takes that
    // voice's only level and leaves it drawing a picture it drives nothing of, which is the one
    // thing no cue of a score may end up doing. The swap runs AFTER the voices above are cast, so
    // this is the only place that can know it.
    function bestFilling(fromW, toW, avoid, noMiracle, seed, key, sole) {
      var pool = [], i, iid;
      for (i = 0; i < ALL_INSTRUMENTS.length; i++) {
        iid = ALL_INSTRUMENTS[i];
        if (!FILLS_THE_FRAME[iid]) continue;
        if ((avoid || []).indexOf(iid) >= 0) continue;
        if (noMiracle && spendsTheMiracle(iid)) continue;
        if ((sole || []).length && (MANIFESTS[iid].levels || []).some(function (lv) {
          return sole.indexOf(lv) >= 0;
        })) continue;
        pool.push({ id: iid, fit: suitsPair(iid, fromW, toW)[0] });
      }
      if (!pool.length) return null;
      return dieWeighted(rankUnread(pool), seed, key + "|ground-fills", 1);
    }

    // WHERE AN UNREAD INSTRUMENT STANDS IN THE POOL IT COMPETES IN, which is the middle of what its
    // rivals read for this pair — a reading of the pair taken through the instruments that did read
    // it, and never a number written here. Where no instrument in the pool read the pair at all,
    // every fit is nothing and `dieWeighted`'s own even roll answers, which is what "no more and no
    // less than any other" means when there is nothing to be no more than.
    function rankUnread(pool) {
      var sum = 0, read = 0, i;
      for (i = 0; i < pool.length; i++) {
        if (typeof pool[i].fit === "number") { sum += pool[i].fit; read += 1; }
      }
      var middle = read ? sum / read : 0;
      for (i = 0; i < pool.length; i++) {
        if (typeof pool[i].fit !== "number") pool[i].fit = middle;
      }
      return pool;
    }

    // The die over a ranked pool of genres, weighted by how well each suits the pair.
    function pickGenre(pool, seed, key) {
      var at = dieWeighted(pool.map(function (r) { return { id: r.id, fit: r.fit }; }), seed, key,
                            "road");
      var i;
      for (i = 0; i < pool.length; i++) if (pool[i].id === at) return pool[i];
      return pool[0];
    }

    // ---- composing one ordered pair ----

    function compose(key, pair, fromW, toW, road, role, memory) {
      var pivot = pivotOf(pair), kind = pivot.elementKind, i, stood = [];
      if (pivot.measure === "banding") {
        var fracs = [];
        [fromW, toW].forEach(function (w) {
          var bp = ((w.structure || {}).banding || {}).periodPx;
          if (w.frameSide && bp) fracs.push(bp / w.frameSide);
        });
        if (fracs.length) pivot.bandPeriodFrac = r4(Math.min.apply(null, fracs));
      }
      // WHICH INSTRUMENT PLAYS THE GROUND, and one always does. Every published instrument is
      // ranked by how well it suits this pair; the instruments that cut the ground's own kind come
      // first, and where none does the best-suited plays the pair on its own cut. Two refusals
      // stood here — «pivot needs an instrument that cuts on tiles», and «no instrument that cuts on
      // panels can play this pair» — and between them they were 2 862 crossings the visitor never
      // saw, out of one collection alone. What each candidate answered stands on the plan.
      // THE PIVOT IS CAST OVER EVERY KIND ITS CUT CARRIES. `pivotKindsOf` is the one home of that
      // fact and the actors are already drawn from all of them; the casting asked about the first
      // alone, which left the tonal and spectral pivot's `scale` half unreachable by any
      // instrument.
      var pivotKinds = pivotKindsOf(pivot);
      // MUST-FILL, TRUE, ALWAYS. `cueWindows` fixes the pivot's own window at `[0, 1]` — the whole
      // pass — before it reads a single argument, so the pivot is the one cue every plan can ever
      // promise is live throughout, and §7's coverage law can only hold if whichever cue promises
      // that also fills the frame. See the note over `castForKinds` for the bound in full.
      // THE ROAD THAT IS THE FOLD BINDS THE GROUND (2026-08-19). `road.mustFold` already keeps the
      // box-fold road off every role whose budget carries no miracle (`genreFor`); this carries the
      // same declaration into the cast, so the road that promises the frame folds into a solid casts
      // the instrument that folds it. See the note in `castForKinds` for what qualifies.
      var castPivot = castForKinds(pivotKinds, fromW, toW, !(ROLE_BUDGETS[role] || {}).miracle,
                                   pair.seed, key, "pivot", null, false, true, null, [0, 1],
                                   !!road.mustFold);
      if (road.mustFold && castPivot[0] === null) {
        castPivot = castForKinds(pivotKinds, fromW, toW, !(ROLE_BUDGETS[role] || {}).miracle,
                                 pair.seed, key, "pivot", null, false, true, null, [0, 1], false);
        stood.push("the " + road.id + " road is the fold itself and no instrument that folds cuts "
                   + pivotKinds.join(" or ") + " for this pair, so the ground plays unfolded");
      }
      // THE MIRACLE'S OWN GATE ON THE GROUND, which the travelling move has had since 2026-08-19
      // and the cue that plays the WHOLE passage never had. `castForKinds` only DEMOTES a
      // world-declaring candidate by one order where the role spends no miracle (`base` there), so
      // on a pair whose kinds nothing else cuts well the ground could still open a world at a step
      // shelf 17 gives no miracle at all. The cast is asked again with the folding instrument set
      // aside, and only its answer is taken — where the collection publishes nothing else, or
      // nothing else that does not fold either, the first cast stands and the plan says the step
      // folded because nothing else could stand there. So this shapes the ground and never refuses
      // the crossing: there is no road out of here that leaves the pair without a passage.
      if (!(ROLE_BUDGETS[role] || {}).miracle && !road.mustFold && spendsTheMiracle(castPivot[0])) {
        var unfolded = castForKinds(pivotKinds, fromW, toW, true, pair.seed, key, "pivot",
                                    [castPivot[0]], false, true, null, [0, 1], false);
        if (unfolded[0] !== null && !spendsTheMiracle(unfolded[0])) {
          stood.push("«" + castPivot[0] + "» opens the world the works live in, which shelf 6 makes "
                     + "this crossing's one impossible event, and the step is a " + role
                     + ", which shelf 17 gives no miracle — so «" + unfolded[0] + "» takes the "
                     + "ground instead");
          castPivot = unfolded;
        } else {
          stood.push("«" + castPivot[0] + "» opens the world the works live in and the step is a "
                     + role + ", which shelf 17 gives no miracle, but this collection publishes no "
                     + "other instrument that can hold the ground for this pair, so it plays");
        }
      }
      var pivotInstr = castPivot[0];
      var castNotes = { pivot: castPivot[1] };
      if (pivotInstr !== null && castPivot[2].indexOf(pivotInstr) < 0) {
        stood.push("no instrument cuts on " + pivotKinds.join(" or ") + ", so «" + pivotInstr
                   + "» plays the ground on its own cut");
      }
      // THE LEVELS ALREADY SPOKEN FOR, read off the ground the instant it is cast — before the
      // travelling move or the arrival ever reach a candidate. Every later cast call narrows its own
      // candidates by this same list, widened by whatever it itself goes on to claim. Pivot's own
      // window is `[0, 1]` always, so it is recorded beside its levels rather than assumed.
      var pivotLevels = pivotInstr ? (MANIFESTS[pivotInstr].levels || []) : [];
      // THE GROUND IS NO LONGER MARKED APART. This record carried `ground: true` so the cast's
      // second clause would not count the ground as a competitor for a level: the ground holds its
      // levels from the first frame to the last, so counting it as one excluded every instrument
      // sharing a level with it at every slot, which left `adrift` and `gears` uncastable. That
      // second clause is retired (the note over `castForKinds`), because the collision it was
      // standing in for is settled at the handles now — a cue that does not own a level has that
      // level's handles taken off its track list and rests there. So the mark has nothing left to
      // exempt the ground from, and the ground is a record like any other: its levels and its
      // window, which is the whole passage.
      // `folds` TRAVELS BESIDE THE RECORD FOR THE SAME REASON THE LEVELS DO (naряд S-18): the
      // clash test above no longer reads a shared WORLD level to know whether an already-placed
      // cue is this crossing's miracle, it reads what that cue's own cast already decided.
      var pivotClashRecord = { levels: pivotLevels, window: [0, 1], folds: spendsTheMiracle(pivotInstr) };
      // THE RETURN-PASS SHIFT, READ ONCE HERE (2026-08-19) so the windows composed below and the
      // levels-law exclusion they inform can both know the ONE nonzero value this edge will ever
      // draw. `dieAmong` is deterministic on `(seed, key)` alone — `key` carries no pass index — so
      // `key + "|rhythm"` names exactly the value every RETURN pass to this edge reuses; the fresh
      // pass always plays at shift 0 (below, where `rhythmShift` is read off `passIndex`). Because a
      // window's own shift only ever moves its OPEN earlier (`cueWindows`'s own rule), the widest any
      // window can ever get is at this one value, so checking the levels law against it is checking
      // every pass this edge will ever render, not only the one composing right now.
      var R = r4(dieAmong(pair.seed, key + "|rhythm", 1000) / 1000.0);
      // TRAVEL'S OWN WINDOW OPENS AT THE GROUND'S OWN STRENGTH. `pivot.strength` is the reading the
      // ground was itself chosen against (`pivotOf`, the first line of this function) — how strongly
      // the two works hold what the ground holds. A strongly-held ground solos longer before the
      // travelling voice joins it; a weakly-held one gives way sooner. Clamped defensively the way
      // every other reading in this file is; `pivot.strength` is already `r4`-rounded off a fit.
      var travelOpenBase = clamp01(num(pivot.strength));
      var travelCloseBase = null, travelWindowBound = null;
      // THE ROAD PICKS THE TRAVELLING AXIS. "far" is the reading this file has always had; a genre
      // built on the pair's own device pins the axis to the measure it is built on; the genre along
      // what the pair shares runs along their closest reading instead.
      var axis = travellingAxisOn(fromW, toW, pivot.measure, road.axis);
      var travelInstr = null, travelDecline = null, tkind;
      if (axis === null && road.axis !== "far" && road.axis !== "near") {
        // The genre's own axis has gone out from under it — the ground took it. The pair still
        // crosses, on the widest axis it has, and the plan says the genre did not get its own.
        axis = travellingAxisOn(fromW, toW, pivot.measure, "far");
      }
      if (axis === null) {
        travelDecline = "no measure carries a reading on both works, so the crossing holds its "
          + "ground and travels nowhere";
      } else {
        tkind = KIND_OF_AXIS[axis.axis];
        // TRAVEL'S OWN WINDOW CLOSES AT ITS OPEN CARRIED FORWARD BY `reach` — `axis.delta`, clamped,
        // the two works' own score gap on the very axis this voice travels, the identical reading
        // the camera's own dolly reads off the pair below. A pair travelling far down its axis keeps
        // the travelling voice on screen for more of the room that is left after its own open; a
        // pair travelling little hands its level back sooner. See the note over `cueWindows` for the
        // formula's own shape.
        var reach = clamp01(num(axis.delta));
        travelCloseBase = r4(travelOpenBase + reach * (1 - travelOpenBase));
        // THE WORST-CASE WINDOW THIS SLOT WILL EVER RENDER, at this edge's one nonzero shift `R`
        // (the note over `R` above). Travel's own open only ever moves earlier under a shift, down
        // toward pivot's own open at 0, so `travelOpenBase * (1 - R)` is that floor; the close never
        // moves. This is the window the levels-law exclusion below checks against, so a candidate
        // ranked clear of a clash here stays clear of it on every pass this edge ever plays.
        var travelOpenAtR = r4(travelOpenBase * (1 - R));
        travelWindowBound = [travelOpenAtR, travelCloseBase];
        // THE GROUND'S OWN INSTRUMENT IS ALREADY SPOKEN FOR, so it stands aside here and the
        // travelling move takes the next one that suits the pair. It is discarded only where it is
        // the sole instrument the collection publishes.
        // THE LEVELS LAW NARROWS THE CANDIDATES BEFORE THE DIE EVER SEES THEM, AND NOW AT A MOMENT
        // RATHER THAN FOR THE WHOLE PASS (2026-08-19). Pivot's `[0, 1]` still meets every candidate's
        // own window by construction, so an instrument that would put a second live voice on a level
        // the ground already owns is still excluded outright; an instrument sharing a level with the
        // ground that the ground's own window never touches at the SAME time as this candidate's own
        // window is not excluded at all — see the note over `castForKinds`.
        var castTravel = castForKinds([tkind], fromW, toW,
                                      !(ROLE_BUDGETS[role] || {}).miracle, pair.seed, key,
                                      "travel", [pivotInstr], false, false, [pivotClashRecord],
                                      travelWindowBound);
        travelInstr = castTravel[0];
        castNotes.travel = castTravel[1];
        if (travelInstr !== null && castTravel[2].indexOf(travelInstr) < 0) {
          stood.push("no instrument cuts on " + pyText(tkind) + ", so «" + travelInstr
                     + "» carries the travelling move on its own cut");
        }
        if (travelInstr === null || travelInstr === undefined) {
          travelInstr = null;
          travelDecline = castTravel[3]
            ? "every instrument that could carry the travelling move would put a second live "
              + "voice on a level the ground's own «" + pivotInstr + "» already owns at the same "
              + "moment, so the travelling move stands down"
            : "this collection publishes no instrument at all";
        } else if (travelInstr === pivotInstr) {
          // The ground's instrument is the only one this collection has, so the travelling move
          // folds into the voice it collided with rather than standing beside it.
          travelInstr = null;
          travelDecline = "«" + pivotInstr + "» is the only instrument this collection publishes, "
            + "so the travelling move folds into the ground's own voice";
        } else if (spendsTheMiracle(travelInstr) && !(ROLE_BUDGETS[role] || {}).miracle) {
          // THE OTHER DOOR THE FOLD COULD COME THROUGH. Shelf 17 gives a quiet link no miracle, so
          // the travelling cue stands down rather than folding the world at a step that may not.
          travelInstr = null;
          travelDecline = "the travelling axis casts an instrument that folds the world, and the "
            + "step is a " + role + ", which shelf 17 gives no miracle";
        }
      }
      // ONCE THE TRAVEL DECISION IS FINAL, `beforeAtR` IS THE ROOM ARRIVAL'S OWN WINDOW HAS TO WORK
      // WITH — travel's own worst-case open where a travelling voice actually plays, pivot's own
      // open (0) otherwise. A travel move that got cast but was then declined by the budget loop
      // further down re-reads this against `null` windows harmlessly, because that loop only ever
      // retires a voice, never revives one the window math already accounted for.
      var beforeAtR = travelInstr !== null && travelWindowBound ? travelWindowBound[0] : 0;
      // THE ACTORS, AND THERE ARE ALWAYS SOME. What stood here was «actor refusal», which turned a
      // work offering only the whole frame along the pivot's cut into no crossing at all; the whole
      // frame is a lawful element and it is what hands over now.
      var cast = castActors(fromW, toW, pivot, axis);
      var actors = cast[0];
      if (cast[1]) stood.push(cast[1]);

      var arrived = locusOf(toW), locusKind = arrived[0], locus = arrived[1], locusFit = arrived[2];
      // THE ONE ARRIVAL DECISION, READ ONCE AND NEVER RECOMPUTED (P1 of the 2026-08-27 adversarial
      // review, naряд S-06's own repair). `arrivalOf`, beside `workParts`, is what ranks the
      // charter's five arrivals against a pair's own records; `fillPlan` already called it to name
      // the arrival the finished score declares, but this function still decided FOR ITSELF, on a
      // plain two-way read of `locusOf(toW)` alone, whether an arrival instrument ever gets cast
      // at all — so a pair `arrivalOf` ranked CRYSTALLIZED or PROPAGATED could declare an arrival
      // that no instrument ever played, because this function's own binary test never saw those
      // two names at all. `arrivalOf` asks for nothing this function cannot already hand it — its
      // two arguments are `measuredParts` of each work and the packed `locusOf` reading `workParts`
      // already builds from the very `arrived` triple two lines up — so it is called here directly,
      // on the same two works, and its one answer is what both this function and `fillPlan` now
      // carry; `arrivalOf` touches neither `sets` nor the pass count, so the same call in `fillPlan`
      // (fed by `workParts`, built for whichever cut this pass plays) always answers identically.
      var arrivalPlan = arrivalOf(
        { measured: measuredParts(fromW) },
        { measured: measuredParts(toW),
          locus: [LOCUS_KINDS.indexOf(locusKind)].concat(locus || [0, 0]).concat([r4(locusFit)]) });
      var arrival = arrivalPlan.mode;
      // THE POINT AND ITS KIND FOLLOW THE SAME DECISION NOW, rather than `locusOf(toW)`'s own point
      // regardless of which arrival plays. Where CONDENSED wins the two still agree exactly —
      // `arrivalOf`'s own CONDENSED candidate is packed straight off this same `arrived` triple —
      // so nothing moves for the case this file always had. Where CRYSTALLIZED wins instead, the
      // point becomes the arriving work's own region-line grain seed (P2 below), a point this file
      // had no use for before tonight.
      locusKind = arrivalPlan.locusKind;
      locus = arrivalPlan.locus;
      locusFit = arrivalPlan.fit;
      var arrivalInstr = null;
      // ARRIVAL'S OWN WINDOW OPENS AT `1 - locusFit*(1 - beforeAtR)` — `locusFit` now carries
      // `arrivalPlan.fit`, the winning arrival's own reading, whichever of the five plays: `locusOf`'s
      // reading where CONDENSED wins, the texture reading where CRYSTALLIZED does, and so on — how
      // confidently the arrival that will actually play reads. A confidently-read arrival can open as early as the room
      // already established allows (`beforeAtR`, above: travel's own worst-case open where travel
      // plays, pivot's otherwise); an unconfident one waits near the `1.0` it always closes at. Its
      // own worst-case-shifted open, `arrivalOpenAtR`, is built the same way travel's was — see the
      // note over `R` above — and is what the levels-law exclusion below is checked against.
      var baseArrivalOpen = r4(1 - locusFit * (1 - beforeAtR));
      var arrivalOpenAtR = r4(baseArrivalOpen - R * Math.max(0, baseArrivalOpen - beforeAtR));
      var arrivalWindowBound = [arrivalOpenAtR, 1.0];
      // THREE OF THE FIVE CAST AN INSTRUMENT (P2 of the 2026-08-27 review). CONDENSED always did;
      // CRYSTALLIZED and PROPAGATED join it here, because both name a real arriving figure — a
      // seed crystallizing, a copy propagating — that wants an actual voice exactly as CONDENSED's
      // figure always did. CARRIED casts nothing because it has nothing of its own to read
      // (`arrivalOf`'s own comment above); INTERFERED casts nothing either, because it is already
      // the shelf-7 arrival this module's own overlay shader plays directly off `arrival.mode`
      // (below, at the overlay and grid-colour branches), with no instrument of its own to cast.
      if (arrival === "CONDENSED" || arrival === "CRYSTALLIZED" || arrival === "PROPAGATED") {
        // THE ARRIVING WORK CONDENSES, AND THE INSTRUMENT THAT CONDENSES IT IS CAST like every
        // other voice: the whole collection is ranked on its own reading of this pair, the two
        // instruments already spoken for stand aside, and the die runs over what is left.
        //
        // WHAT WENT, AND WHY THE TWO WENT TOGETHER. The line here handed the slot to «matter» BY
        // NAME whenever «matter» was free — no fit consulted, no die rolled — and that is the class
        // his word of 2026-08-18 13:41 strikes: a special case where the general rule already
        // covers the ground. Handing a slot to one instrument BY NAME consults no fit and rolls no
        // die, so the choice carries no reading of either photograph at all — the strongest thing
        // that can be said about a decision, and it needs no count beside it. Beneath the name stood the second fault: the
        // fallback DROPPED the arrival whenever the cast collided with the ground or the travel,
        // rather than choosing the next-best — the same collision the travelling move was repaired
        // for at `castForKinds` above and the arrival never was. Each hid the other by construction:
        // striking the name alone sends every cue the name used to catch into the drop, and repairing
        // the drop alone leaves the name deciding before the drop is ever reached.
        //
        // So the name goes and the collision CHOOSES, on one call. Only where every instrument the
        // collection publishes is already spoken for does the arrival fold into the voice it
        // collided with, which is the same sentence the travelling move stands under.
        // THE LEVELS ALREADY SPOKEN FOR BY BOTH VOICES CAST SO FAR, EACH BESIDE ITS OWN WINDOW
        // (2026-08-19). The ground's `[0, 1]` meets everything regardless; the travelling move's
        // own worst-case window (`travelWindowBound`, above — the same one its own cast was checked
        // against) is what arrival's candidates are actually compared to now, so an arrival that
        // shares a level with the travelling voice is excluded only where their two windows would
        // genuinely overlap, never on the level name alone.
        var clashForArrival = [pivotClashRecord];
        if (travelInstr) {
          clashForArrival.push({ levels: MANIFESTS[travelInstr].levels || [],
                                 window: travelWindowBound, folds: spendsTheMiracle(travelInstr) });
        }
        var castArrival = castForKinds([], fromW, toW, !(ROLE_BUDGETS[role] || {}).miracle,
                                       pair.seed, key, "arrival", [pivotInstr, travelInstr],
                                       FILLS_THE_FRAME[pivotInstr]
                                       || FILLS_THE_FRAME[travelInstr],
                                       false, clashForArrival, arrivalWindowBound);
        arrivalInstr = castArrival[0];
        castNotes.arrival = castArrival[1];
        if (arrivalInstr === null && castArrival[3]) {
          stood.push("every instrument that could condense the arrival would put a second live "
                     + "voice on a level the ground or the travelling move already owns at the same "
                     + "moment, so the arrival stands down and the work carries over unaltered");
        }
        if (arrivalInstr !== null
            && (arrivalInstr === pivotInstr || arrivalInstr === travelInstr)) {
          stood.push("«" + arrivalInstr + "» is the only instrument this collection publishes, so "
                     + "the arrival folds into the voice it collided with");
          arrivalInstr = null;
        }
        // THE SAME GATE THE GROUND AND THE TRAVELLING MOVE STAND UNDER, and the arrival is the third
        // slot a cast reaches. `castForKinds` only DEMOTES a world-declaring candidate by one order
        // where the role spends no miracle, which is a ranking nudge and not a bound: it decides
        // which candidate is likeliest, never which may stand. So the gate is stated here as it is
        // stated for the other two, and the arrival that opens a world at a step shelf 17 gives no
        // miracle is asked to be cast again with that instrument set aside. Only where nothing else
        // the collection publishes can condense this arrival does it stand down, which is the same
        // sentence the travelling move already stands under and the same one the two lines above
        // say for a collision.
        if (arrivalInstr !== null && spendsTheMiracle(arrivalInstr)
            && !(ROLE_BUDGETS[role] || {}).miracle) {
          var castPlain = castForKinds([], fromW, toW, true, pair.seed, key, "arrival",
                                       [pivotInstr, travelInstr, arrivalInstr],
                                       FILLS_THE_FRAME[pivotInstr] || FILLS_THE_FRAME[travelInstr],
                                       false, clashForArrival, arrivalWindowBound);
          stood.push("the arrival casts «" + arrivalInstr + "», which opens the world the works "
                     + "live in, and the step is a " + role + ", which shelf 17 gives no miracle"
                     + (castPlain[0] !== null && !spendsTheMiracle(castPlain[0])
                        ? " — so «" + castPlain[0] + "» condenses the arrival instead"
                        : ", and no other instrument this collection publishes can condense this "
                          + "arrival, so the work carries over unaltered"));
          arrivalInstr = (castPlain[0] !== null && !spendsTheMiracle(castPlain[0]))
            ? castPlain[0] : null;
          if (arrivalInstr !== null) castNotes.arrival = castPlain[1];
        }
      }
      var departing = locusOf(fromW);
      // WHETHER THE ARRIVAL PLAYS ITS OWN DISASSEMBLY BEFORE ITS ASSEMBLY, and it reads the
      // departing work's own figure, as it always did — whether that figure already stands where
      // the departing work's own locus falls.
      //
      // PROPAGATED NO LONGER ASKS FOR IT (the 2026-08-27 audit's own finding on наряд S-06). The
      // clause struck here read `arrival === "PROPAGATED" || …`, put there to carry the наряд's
      // sentence «в зеркальных копиях дальняя меняется первой» — of the mirrored copies, the far
      // one changes first. It carried nothing of the kind. `arrivalLeads` orders THE ARRIVAL'S OWN
      // TWO HALVES, its disassembly against its assembly; the наряд's sentence orders TWO MIRRORED
      // COPIES OF ONE WORK against each other, which is a different pair of things and lives where
      // the copies do. It lives there now: `livemirror.propagate` above, the one instrument of the
      // fleet that makes mirrored copies, spreads their exchanges apart with the further copy
      // changing first. So this line answers only the question it was always answering.
      var arrivalLeads = !!arrivalInstr && figureOnLocus(fromW, departing[1]);

      // THE VISIT'S MEMORY, on this side of the line. §4.8 lets three fields cross — the family,
      // the seed and the pass index — and the family is what `genreFor` above holds. What the pass
      // index answers here is the rest of §4.8's own sentence: the cue order, the element
      // selection, the camera route, the rhythm and the phases may all differ, and three of those
      // are this file's to vary.
      //
      // THE ORDER OF THE MOVES turns over on a further pass, from the pass count and the die
      // together, so an edge that opened with its ground opens with its arrival the next time and
      // a later visit on another die opens the other way about again.
      //
      // WHICH WAY THE EARLIER PASS RAN IS NOT A FACT THIS SIDE HOLDS, and it is not one it needs.
      // §4.8's three fields carry no direction, deliberately: the family is exactly what a return
      // keeps, so a direction written inside it would make every return unrelated by construction.
      // A backward passage already differs by everything the direction itself turns over — the two
      // works swap ends, the actors swap their roles, each axis reads from the other work's number
      // and the camera's route reverses with them — and the pass count turns the order of the moves
      // on top of that. So one rule answers a return and a repeat, and each still differs from what
      // played before it.
      var passIndex = (memory && memory.passIndex)
        ? Math.max(0, Math.round(Number(memory.passIndex))) : 0;
      if (passIndex && arrivalInstr
          && (passIndex + dieAmong(pair.seed, key + "|moves", 2)) % 2 === 1) {
        arrivalLeads = !arrivalLeads;
      }

      // EVERY HANDLE THE CHOSEN INSTRUMENTS DRIVE HAS TO NAME ITS MEASUREMENT. His 19:13 word
      // lifted to the class at 19:21 binds the composer as much as the instrument: a score driving
      // a handle this file cannot say the provenance of would be a number nobody read reaching the
      // picture. The law holds in full — the handle is simply NOT DRIVEN, and the instrument's own
      // default stands where the composer has nothing to say.
      //
      // WHAT THIS REPLACES. The whole crossing was refused and the visitor got the walk's plain
      // glide, so an instrument that grew one unnamed handle cost the visitor every passage that
      // instrument could have played. Nothing about the law is loosened by this: no unnamed number
      // reaches the picture either way, and now the pair still crosses.
      var unnamedHandles = {};
      [pivotInstr, travelInstr, arrivalInstr].forEach(function (iid) {
        if (!iid || !MANIFESTS[iid]) return;
        Object.keys(MANIFESTS[iid].handles).forEach(function (h) {
          if (MANIFESTS[iid].handles[h].open || sourceOf(iid, h)) return;
          if (!unnamedHandles[iid]) unnamedHandles[iid] = [];
          if (unnamedHandles[iid].indexOf(h) < 0) unnamedHandles[iid].push(h);
        });
      });
      Object.keys(unnamedHandles).sort().forEach(function (iid) {
        stood.push("the instrument «" + iid + "» publishes «" + unnamedHandles[iid].sort().join("», «")
                   + "» and no measurement is written for them, so the score drives neither and the "
                   + "instrument's own default stands");
      });

      var cam = cameraFlight(pair, axis, locus);
      var mesh = null, why = null, made;
      if (pivotInstr === "gears" || travelInstr === "gears") {
        made = meshingTravel(fromW, toW, pivot);
        mesh = made[0];
        why = made[1];
        if (why) stood.push(why);
        made = askTheDoors(mesh);
        mesh = made[0];
      }

      // THE MIRACLE HAS TWO GATES BEFORE IT, and both are stated. The ROAD says whether a folded
      // space is what this derivation is for — a road that holds its ground spends no miracle on
      // one — and the ROLE says whether this step of the walk may spend one at all: shelf 17 gives
      // a quiet link none, a middle at most one and a culmination exactly one, and shelf 6 lets at
      // most one impossible event stand in any crossing whatever.
      var roleBudget = ROLE_BUDGETS[role] || ROLE_BUDGETS.middle;
      // THE BOX IS ITSELF THE MIRACLE, AND THERE IS ONLY ONE SLOT. Charter shelf 6: at most one
      // impossible event per crossing, a culmination carries exactly one, and a folded space, a
      // shift of what a thing is, or a change of substance CONSUMES the slot and never stacks. A
      // solid the frame turns into is a folded space by the plainest reading of shelf 8 — the
      // instruments lane's own manifest says as much by declaring the world level — so a crossing
      // that folds has spent its miracle, and the polar world of `worldOf` stands down beside it
      // rather than making a second impossible thing.
      //
      // WHAT A FOLD IS, IS WHAT THE INSTRUMENT DECLARES ABOUT ITSELF, never what it is called. This
      // read `=== "boxfold"` on all three cast slots, and the file already held the other, truer
      // definition four screens up: `spendsTheMiracle` asks the manifest whether the instrument
      // declares the WORLD level. That is the charter's own definition — shelf 6 says a folded
      // space, a shift of what a thing is or a change of substance consumes the slot and never
      // stacks, shelf 8 says at most one folded space per crossing and it IS the miracle — and the
      // manifest's world declaration is the one place an instrument says it does that. The name test
      // was the accident: this collection publishes four instruments that declare the world and the
      // name saw one of them, so the other three folded the space a work lives in, were voiced as
      // ordinary letters and were counted as no miracle at all.
      var folds = spendsTheMiracle(pivotInstr) || spendsTheMiracle(travelInstr)
        || spendsTheMiracle(arrivalInstr);
      var couldFold = travelInstr ? worldOf(toW, axis) : null;
      var mayFold = !!(road.miracle && roleBudget.miracle && !folds);
      var world = mayFold ? couldFold : null;
      var miracleDecline = (couldFold && !mayFold)
        ? (folds
           ? "the frame folds into a solid, which is this crossing's one miracle, so the arriving "
             + "work's own folded space stands down beside it"
           : (road.miracle
              ? ("the step is a " + role + " and shelf 17 spends no miracle there")
              : ("the " + road.id + " road holds its ground and spends no miracle on a folded "
                 + "space")))
        : null;
      var voices, tier, letters, accs, k, instrumentOf, stackOrder, placed, capped = [];
      // WHETHER THIS CROSSING STILL SPENDS ITS COLOUR VOICE. Shelf 17 counts the camera, the ground
      // and colour in one column, and the loop below may find all three standing against a ceiling
      // of two. The colour voice is the one of the three that is neither the camera nor the crossing
      // itself, so it is the one an accompaniment budget can spend: the level goes unowned, its
      // handles come off every track list, and the instruments' own published defaults stand there.
      // Every cue, every instrument and every move stands. It is re-read on every turn of the loop
      // because the loop can retire the very cue that sings it.
      var colourVoice = true, accCeiling = 0;
      // WHICH CUE FOLDS THE FRAME, or nothing — read off the manifest exactly as `folds` above is,
      // and never off a name. It is re-read on every turn of the budget loop below, because the loop
      // can retire the very cue that folds.
      var foldsOn = null, stackSwapped = false;

      // THE ROLE'S BUDGET IS A BOUND ON WHAT IS EMITTED, not a wish. Shelf 17 counts letters, and a
      // quiet link carries exactly one; a step whose pair offers more moves than its role may spend
      // gives them up here rather than at the gate. The travelling move goes first, because the
      // ground and the arrival are the two the charter names by role, and the plan records every
      // move it gave up so a thin passage can be read back to the reason it is thin.
      for (;;) {
        foldsOn = spendsTheMiracle(pivotInstr) ? "pivot"
          : (spendsTheMiracle(travelInstr) ? "travel"
             : (spendsTheMiracle(arrivalInstr) ? "arrival" : null));
        var voiced = voiceTheCues(travelInstr !== null, arrivalInstr !== null, world,
                                  role, foldsOn);
        voices = voiced[0];
        tier = voiced[1];
        if (travelInstr === null) delete voices.travel;
        if (arrivalInstr === null) delete voices.arrival;
        letters = 0;
        accs = 1;
        for (k in voices) {
          if (voices[k] === "letter") letters += 1;
          else if (voices[k] === "accompaniment") accs += 1;
        }
        // THE PLACEMENT LAW IS THE SECOND BOUND. §7's coverage law lets only the LOWEST cue leave
        // the frame open — nothing is drawn beneath it, so where its matter is absent the cleared
        // buffer shows — and it exempts a one-cue score, because nothing stands beneath that either.
        // A visitor would see a torn frame without it, so it is his requirement in the plainest
        // sense and it holds.
        //
        // WHAT IT NO LONGER DOES IS TAKE A VOICE DOWN AS ITS FIRST ANSWER. A stack whose cues all
        // write coverage has no ground, and this retired the travelling move for it — which is the
        // direct cause of a crossing playing on one voice. The law is answered by CHOOSING instead:
        // the ground is re-cast to an instrument that fills the frame, and only where the collection
        // publishes none at all does a move stand down. `stackSwapped` holds it to one attempt so
        // the loop always ends.
        instrumentOf = {};
        if (pivotInstr && voices.pivot) instrumentOf.pivot = pivotInstr;
        if (travelInstr && voices.travel) instrumentOf.travel = travelInstr;
        if (arrivalInstr && voices.arrival) instrumentOf.arrival = arrivalInstr;
        stackOrder = CUE_IDS.filter(function (c) { return instrumentOf[c] !== undefined; });
        placed = placeTheStack(stackOrder, instrumentOf);
        // WHETHER THIS CAST SINGS LIGHT-COLOUR, read here rather than after the loop, because the
        // count it changes is one the loop has to answer, and re-read on every turn because the
        // loop can retire the very cue that sings it. It is read off the cues that survived this
        // turn, never off the instrument variables alone.
        var singsHere = false, ci;
        for (ci = 0; ci < stackOrder.length; ci++) {
          if ((MANIFESTS[instrumentOf[stackOrder[ci]]].levels || []).indexOf("LIGHT-COLOUR") >= 0) {
            singsHere = true;
            break;
          }
        }
        // THE ACCOMPANIMENT CEILING IS THE THIRD BOUND, and it belongs to the tier this plan will
        // DECLARE rather than to the one the role reached for. §4.7 asks the declared tier and the
        // measured one to agree, so the ceiling that has to hold is the declared row's; and since
        // the three rows' accompaniment ceilings rise with the tier's own rank, and the rank test
        // below already holds the realised tier at or under the role's, the declared row's ceiling
        // is the tighter of the two and answering it answers both.
        accCeiling = ceilingOfTier(tier, "accompaniments");
        // THE COUNT SHAPES THE CROSSING WITHOUT TOUCHING A MOVE. Charter shelf 17 as amended on his
        // word of 2026-08-18 13:41: the counts shape a crossing that is already playing and never
        // refuse one. An accompaniment overrun is paid for with an ACCOMPANYING VOICE, which is what
        // the column counts — never with a letter, which would take a move away to settle a debt it
        // did not run up. The camera is a constant of every crossing by §4.4's own amendment and the
        // ground IS the crossing, so colour is the one of the three that can stand down, and it
        // stands down the way the levels law already stands a voice down: the level goes unowned.
        //
        // IT IS A READING OF THIS TURN AND NEVER A LATCH. Written as a one-way give-up it would
        // outlive the count that caused it: a turn that later retires the very cue that sang would
        // leave the crossing without a colour voice it could now afford. This line is a pure
        // function of the counts the turn it runs on actually carries, so the answer that stands is
        // the answer for the cast that stands, and the loop gains no new road out.
        colourVoice = !(singsHere && accs + 1 > accCeiling);
        var fits = placed[0] !== null
          && letters <= roleBudget.letters
          && accs + ((colourVoice && singsHere) ? 1 : 0) <= accCeiling
          && TIER_RANK[tier] <= TIER_RANK[roleBudget.tier];
        if (fits) break;
        if (placed[0] === null && !stackSwapped && stackOrder.length > 1) {
          stackSwapped = true;
          // THE GROUND SWAP IS THE THIRD DOOR THE MIRACLE COULD COME THROUGH, and it stood open.
          // `bestFilling` already sets a world-declaring instrument aside where the role spends no
          // miracle, but at a role that MAY spend one the slot is free by the role's reckoning even
          // when a voice above the ground has already taken it — and this swap runs after the
          // travelling move and the arrival are cast, so it could seat a second world instrument
          // under a first. Shelf 6 says the slot is consumed and never stacks, so a crossing whose
          // voices already fold asks for a ground that does not, on the same argument
          // `bestFilling` already takes: no new bound, the one it has, told the truth about what
          // the crossing has already spent.
          var alreadyFolds = spendsTheMiracle(travelInstr) || spendsTheMiracle(arrivalInstr);
          // THE LEVELS THE VOICES ABOVE CANNOT GIVE UP. A voice that drives exactly one level has
          // nowhere else to be, so a ground declaring that level annihilates it — the voice plays
          // on, drawing, driving nothing of its own. `soleAbove` is read off the voices already cast
          // and handed to the choice, so the ground that fills the frame is chosen from those that
          // leave every voice above it something to say.
          var soleAbove = [];
          [travelInstr, arrivalInstr].forEach(function (iid2) {
            if (!iid2 || !MANIFESTS[iid2]) return;
            var lv2 = (MANIFESTS[iid2].levels || []).filter(function (l) {
              return Object.keys(MANIFESTS[iid2].handles || {}).some(function (hh) {
                return levelOf(iid2, hh) === l;
              });
            });
            if (lv2.length === 1 && soleAbove.indexOf(lv2[0]) < 0) soleAbove.push(lv2[0]);
          });
          var fill1 = bestFilling(fromW, toW, [travelInstr, arrivalInstr],
                                  !roleBudget.miracle || alreadyFolds, pair.seed, key, soleAbove);
          if (fill1 && fill1 !== pivotInstr) {
            stood.push("the stack §7's coverage law asks for had " + placed[1].split(":")[0]
                       + ", so «" + fill1 + "» takes the ground and fills the frame instead of «"
                       + pivotInstr + "» — the voices above it stand");
            pivotInstr = fill1;
            continue;
          }
        }
        if (travelInstr !== null) {
          travelInstr = null;
          world = null;
          if (placed[0] === null && travelDecline === null) travelDecline = placed[1];
          capped.push("travel");
          continue;
        }
        if (arrivalInstr !== null) {
          arrivalInstr = null;
          arrivalLeads = false;
          capped.push("arrival");
          continue;
        }
        break;
      }

      // THE LOOP ABOVE ALWAYS REACHES A LAWFUL STACK, because a one-cue score is exempt from §7's
      // placement law by the contract's own sentence — nothing stands beneath it, so its alpha is
      // never read. Where the loop has retired both the travelling move and the arrival and the law
      // still says no, the ground plays alone and the plan says the law had to be answered that way.
      if (placed[0] === null) {
        stood.push(placed[1]);
        placed = [{ pivot: 0 }, null];
        stackOrder = ["pivot"];
      }
      var stacks = placed[0];
      // WHAT THE COUNT SHAPED, in the same place every other shaping this crossing took is written.
      // A thin passage reads back to the reason it is thin, and this one is thin in exactly one
      // way: it keeps every move, every cue and every instrument, and plays without its colour
      // voice. `capped` and `stood` are the two lists that already carry every other shaping.
      if (!colourVoice) {
        capped.push("colour");
        stood.push("shelf 17 gives a " + tier + " at most " + accCeiling + " accompanying voices "
                   + "and the camera and the ground already stand in them, so the crossing plays "
                   + "without its colour voice and keeps every move it makes");
      }
      // WHETHER THIS CAST SINGS LIGHT-COLOUR, read off the cues that actually survived the loop
      // above (`stackOrder`, never the instrument variables alone — a voice the loop retired must
      // not still be counted). Because the levels law now excludes a second LIGHT-COLOUR candidate
      // at the cast itself (the note over `castForKinds`), at most one surviving cue can ever answer
      // yes, so there is no ownership left to contend for by the time this asks.
      // AND IT ANSWERS TO THE LOOP'S OWN DECISION. Where the budget loop above gave the colour
      // voice up to hold shelf 17's accompaniment ceiling, no cue owns LIGHT-COLOUR any more, so
      // this reading has to say so too — otherwise the count taken here and the count the loop
      // answered would disagree by exactly the voice that was spent.
      var singsColour = false, colourCk;
      for (i = 0; colourVoice && i < stackOrder.length; i++) {
        colourCk = stackOrder[i];
        if (instrumentOf[colourCk]
            && (MANIFESTS[instrumentOf[colourCk]].levels || []).indexOf("LIGHT-COLOUR") >= 0) {
          singsColour = true;
          break;
        }
      }
      var reordered = stackOrder.filter(function (c, i2) { return stacks[c] !== i2; });

      var judged = tierFor(voices, tier, singsColour), row = judged[0], counts = judged[1];
      // THE STEP'S OWN LENGTH, COMPOSED FROM THE PAIR INSIDE THE BAND ITS TIER ALLOWS. The band is
      // the REALISED tier's, which `tierFor` has just settled: a role reaches for a tier and gets
      // the band of the tier it actually made, so a plan never declares a tier its length
      // contradicts — the disagreement §4.7 calls a red — and a role that reached its own tier is
      // answered by that tier's band without a second copy of it standing anywhere. What stood here
      // read ONE typed duration off whichever row answered, and since `cueWindows` fixes the pivot's
      // window at [0, 1] and every score carries a pivot, `Math.max(ends)` is exactly 1 on every
      // composition and the derived length was that typed number to the millisecond — one duration
      // for every pair the role ever plays.
      //
      // THE READING IS THE ONE THE PASSAGE ALREADY PUBLISHES AS `cameraReach`'s first number: the
      // camera's own dolly as a share of the bound it answers to. It is a reading of the two
      // works — `cameraFlight` takes it from their measured door steps, `log(stepTo / stepFrom)`
      // spent against `DOLLY_CAP` as a limit — and it is already in hand here, so no second
      // "how far apart" number is invented for the length (grammar law 5: one gesture, one scalar).
      // How far the eye has to travel in depth between the two pictures is how long the crossing
      // takes, and a pair whose two door steps say nothing crosses at the short end of its band
      // rather than not at all.
      //
      // THE BAND HOLDS FOR EVERY VALUE THE READING CAN TAKE, by the reading's own construction.
      // `cameraFlight` writes `dolly = DOLLY_CAP · asked / (|asked| + DOLLY_CAP)` where either
      // measured door step missing leaves it at exactly 0, so |dolly| = DOLLY_CAP · |asked| /
      // (|asked| + DOLLY_CAP) < DOLLY_CAP for every finite `asked` and the share below is at most 1
      // (`r4` can carry it onto the bound, never past it, and `clamp01` states that rather than
      // trusting it). A share of 0 gives the band's own floor, a share of 1 its own ceiling, and the
      // placement is monotone between them — so no pair in the world composes outside the band.
      var lengthShare = Math.abs(num(cam.logScale)) / DOLLY_CAP;
      var duration = lengthInBand(row.band, lengthShare);
      // The deviation this pass puts on the rhythm. It moves no window's close, so the ends below
      // read the same numbers whatever it is.
      // THE DEVIATION IS A SHARE OF THE ROOM EACH WINDOW HAS, drawn on the die, so a further pass
      // breathes in the room the passage actually has rather than in a room this file invented. The
      // die's granularity is mechanics — a thousand rungs across the share — and carries no
      // artistic value of its own. `R` (above, read once before travel was even cast) IS this
      // value — a fresh pass plays at 0, every return pass to this edge plays at the same `R`,
      // because `dieAmong` never read the pass index — so it is reused rather than redrawn.
      var rhythmShift = passIndex ? R : 0;
      var windows = cueWindows(travelInstr !== null, travelOpenBase, travelCloseBase,
                               baseArrivalOpen, rhythmShift);
      var ends = CUE_IDS.filter(function (c) { return voices[c] !== undefined; })
        .map(function (c) { return windows[c][1]; });
      // THE LENGTH IS FITTED INTO §2.5'S TRANSACTION BOUND, never refused for standing outside it.
      // §2.5's bound is the contract's own and it holds in full; what changed is that a passage
      // reaching past it is SHORTENED to the bound rather than not played, which is what a bound on
      // a duration can honestly do. The plan says it was shortened.
      var derivedMs = roundToInt(Math.max.apply(null, ends) * duration);
      if (derivedMs > TRANSACTION_MS) {
        stood.push("the crossing's own length came to " + derivedMs + " ms and §2.5 holds a "
                   + "transaction to " + TRANSACTION_MS + " ms, so it plays shortened");
        duration = Math.floor(duration * TRANSACTION_MS / derivedMs);
        derivedMs = roundToInt(Math.max.apply(null, ends) * duration);
      }
      if (!(derivedMs > 0)) {
        stood.push("the crossing's own length came to nothing, so it plays at the instant §2.5 "
                   + "calls a legal transition");
      }

      var roles = { pivot: voices.pivot === "accompaniment" ? ["surface", "breath"]
                    : ["surface", "mystery"] };
      if (travelInstr) roles.travel = world ? ["mystery", "world"] : ["mystery", "fragment"];
      if (arrivalInstr) roles.arrival = arrivalLeads ? ["disassembly", "assembly"] : ["assembly"];

      var register = registerOf(fromW, toW, arrival, world);
      // WHICH AUTHORED LINE THIS PLAN OPENS WITH. A folding crossing names the solid; a crossing
      // that opens the arriving work's own space names the world; one that only travels names the
      // axis; one that only holds names the ground. Every field each template asks for is set for
      // the shape that chooses it, which is what keeps `fill` from throwing on the product path.
      var intentKey = foldsOn
        ? (row.tier === "culmination" ? "culmination-fold" : "middle-fold")
        : (row.tier === "culmination" ? "culmination"
           : (world ? "middle-world" : (travelInstr ? "middle-travel" : "quiet")));
      var spec = {
        pivot: pivotInstr, travel: travelInstr, arrival: arrivalInstr,
        voices: voices, roles: roles, tier: row.tier, duration: duration,
        arrivalLeads: arrivalLeads,
        middle: world ? { kind: "world", world: world }
          : (travelInstr ? { kind: "surface" } : { kind: "none" }),
        budget: counts, intentKey: intentKey, road: road.id, role: role, passIndex: passIndex,
        rhythmShift: rhythmShift,
        // WHETHER THIS CROSSING STILL SPENDS ITS COLOUR VOICE (the budget loop above). It travels
        // here so the score and the counts say the same thing: a crossing that gave the voice up
        // must not go on emitting a cue that owns LIGHT-COLOUR, or the plan's declared tier and the
        // score's own voices would disagree again by another road.
        colourVoice: colourVoice,
        // THE WINDOWS' OWN BASE VALUES, carried to `buildTemplate` so it composes the same windows
        // from the same readings rather than re-deriving them from scratch with no access to the
        // two works' own records. `cueWindows` applies `rhythmShift` to these exactly once here and
        // exactly once there, and both calls are the same function on the same numbers.
        travelOpenBase: travelOpenBase, travelClose: travelCloseBase, arrivalOpenBase: baseArrivalOpen
      };
      var shape = shapeId(pivotInstr, pivotKindsOf(pivot).join("+"), travelInstr, arrivalInstr,
                          voices, arrivalLeads, world);
      var ground = null;
      for (i = 0; i < stackOrder.length; i++) if (stacks[stackOrder[i]] === 0) {
        ground = stackOrder[i];
        break;
      }
      return [{
        shape: shape, spec: spec, pivot: pivot, axis: axis, actors: actors,
        arrival: arrival, locusKind: locusKind, locus: locus, camera: cam,
        world: world, travelDecline: travelDecline, seed: pair.seed,
        readiness: pair.readiness, direction: pair.direction, mesh: mesh,
        register: register, gestures: Object.keys(voices).length,
        stacks: stacks, stackGround: ground, stackReordered: reordered.length > 0,
        a: pair.pair.a, b: pair.pair.b,
        // What the road, the role and the memory did to this derivation, on the plan where the
        // diagnostic surface can read it back. None of it reaches a score.
        road: road.id, genre: road.id, roadWhy: road.why, genreFit: r4(road.fit === undefined ? 0
                                                                      : road.fit),
        role: role, passIndex: passIndex,
        capped: capped, miracleDecline: miracleDecline, castNotes: castNotes,
        // EVERY SHAPING THIS CROSSING TOOK, in one place and in plain words. Each line here is a
        // sentence that used to be a refusal — a ground with no instrument, a work offering only
        // the whole frame, a mesh with no ring count, a handle nobody named, a length past §2.5's
        // bound — and it now says what was done instead. The list is empty for a crossing that
        // needed no shaping at all, which is most of them.
        stood: stood
      }, null];
    }

    // ---- the row and the per-work record the fill reads ----

    function encodeEnds(axis, reading) {
      var e = reading.ends;
      if (axis === "banding") {
        return [flt(reading.score), flt(e.periodPx), e.axis === "vertical" ? 0 : 1];
      }
      if (axis === "radial") {
        var at = SUBTYPES.indexOf(e.subType);
        return [flt(reading.score), flt(e.centre[0]), flt(e.centre[1]), at < 0 ? 2 : at];
      }
      if (axis === "regions") return [flt(reading.score), e.count];
      if (axis === "grid") return [flt(reading.score), flt(e.periodPx), flt(e.angleDeg)];
      if (axis === "texture") {
        return [flt(reading.score), flt(e.detailPx), flt(e.spectralPeriodPx)];
      }
      if (axis === "dominant_object") {
        return [flt(reading.score)].concat(e.box.map(function (x) { return flt(x); }));
      }
      return [flt(reading.score)];
    }

    // THE PER-WORK READINGS THE FILL DRIVES HANDLES FROM. Everything here comes off the work's own
    // record; the fill below names, handle by handle, which of these each one reads.
    function measuredParts(work) {
      var st = work.structure || {}, tex = work.texture || {}, mot = work.motifs || {};
      var side = Number(work.frameSide) || 0;
      var box = (st.dominantObject || {}).bbox || [0, 0, 0, 0];
      var ring = setFor(work, "ring"), strip = setFor(work, "strip");
      var spectral = Number(tex.spectralPeriodPx) || 0;
      return {
        // the work's own spectral period, said as cells across the frame's height — the very unit
        // the material instrument's coarse grain is published in
        grainCells: spectral > 0 && side > 0 ? side / spectral : 0,
        spectralPeriodPx: spectral,
        // HOW MUCH OF THE WORK READS AS GRAIN RATHER THAN AS LINE, and the finest detail it carries.
        // Both are in the trimmed record the engine already receives and neither was read here until
        // the water arrived; they are the two readings its swell and its refraction are placed by.
        textureScore: Number(tex.scoreFromCutLines) || 0,
        detailPx: Number(tex.detailPx) || 0,
        // the share of the frame the work's measured open ground holds
        voidShare: Number(mot.voidShare) || 0,
        // the share of the frame the work's dominant object holds, off its own measured box
        figureShare: Math.max(0, (box[2] - box[0])) * Math.max(0, (box[3] - box[1])),
        // WHERE THAT OBJECT STANDS IN THE FRAME — the centre of the same measured box, as a share
        // of the frame's own sides. It is where the drifting instrument seats each work's thing
        // before it carries it across the emptiness, and it is the same box the share above is
        // taken from, read for its place rather than for its size.
        figureCx: r4((num(box[0]) + num(box[2])) / 2),
        figureCy: r4((num(box[1]) + num(box[3])) / 2),
        // HOW PLAINLY THE WORK CARRIES A GATE — two masses with emptiness between them. The record
        // publishes this one as a NUMBER rather than only as a name on the motif list, which the
        // seam is not: `motifs.gateGap` is lab/step1-motifs.py's own measure, one minus the busy-ness
        // of the middle band over the busy-ness of the denser flank, and it stands on every work.
        // Both are read, because the list says the motif was recognised and the number says how
        // strongly.
        //
        // WHAT IS STILL MISSING, AND IT IS NOT FILLED HERE. The record says how plainly a gate reads
        // and NOWHERE says where that gate stands or how wide it is, so the gate instrument's slot
        // opens in the middle of the frame on every pair. The lane's report names the column a work
        // record would have to publish; inventing one here would be a number nobody measured.
        carriesGate: (mot.measured || []).indexOf(MOTIF_GATE) >= 0 ? 1 : 0,
        gateGap: Number(mot.gateGap) || 0,
        // WHERE THE DEPARTING WORK'S OWN SLOT STANDS, HOW WIDE IT IS AND WHICH WAY IT OPENS — the
        // three readings pass-inst-gates.js:604-638 named as missing until tonight. lab/step1-
        // motifs.py's slot_on() (ported from the archived lab/effects/gates.js, git show 9c3d139)
        // sweeps both axes of the work's own busy profile, keeps the better-scoring one and grows
        // the slot outward from its own best centre; lab/build-workrecords-v1.py carries the result
        // as `motifs.gatePlace`/`gateHalf`/`gateAxis` beside `gateGap`. `gateAxis` is folded to the
        // same 0/1 the banding branch of `encodeEnds` two screens up already uses: the axis that
        // opens sideways (a vertical band) is 1, the axis that parts up and down is 0.
        gatePlace: Number(mot.gatePlace) || 0,
        gateHalf: Number(mot.gateHalf) || 0,
        gateAxis: mot.gateAxis === "vertical" ? 1 : (mot.gateAxis === "horizontal" ? 0 : null),
        // how strongly the work reads as radial, and how many rings its own cut measured
        radialScore: Number((st.radial || {}).score) || 0,
        // THE POINT THE WORK'S OWN STRUCTURE TURNS ABOUT, in the same order of preference `locusOf`
        // reads it: the motif's own measured centre first and the radial reading's second. Five
        // instruments publish a handle that says it reads this, and until now the fill answered
        // them from the camera's own pan — which is the TRAVELLING AXIS'S two ends and equals the
        // radial centre only where that axis is radial. Every work of the collection carries this
        // one, so it answers for every pair and it answers with what the handles ask for.
        radialCx: Number(((work.motifs || {}).radialCentre
                          || (st.radial || {}).centre || [0.5, 0.5])[0]) || 0.5,
        radialCy: Number(((work.motifs || {}).radialCentre
                          || (st.radial || {}).centre || [0.5, 0.5])[1]) || 0.5,
        ringGrain: ring ? Number(ring.measuredGrain) || 0 : 0,
        // how much finer the work's own measured repeat is than the cut it was given
        ringMerge: ring ? Number(ring.mergeFactor) || 0 : 0,
        // the strip family the woven instrument cuts on
        strips: strip && strip.realCount ? Number(strip.count) || 0 : 0,
        // how strongly the work already reads as a corridor, and where its own horizon stands —
        // the two the folding instrument's perspective and its eye's ride are placed by
        tunnel: Number((st.polar || {}).tunnel) || 0,
        // HOW MUCH OF A LITTLE WORLD THE WORK ALREADY IS. The same polar family as `tunnel` above
        // and the reading the world-curling instrument is placed by: a picture that already turns
        // about a centre closes the whole way, one that barely does is left a bowed band.
        planet: Number((st.polar || {}).planet) || 0,
        // HOW MUCH THE WORK WINDS, and the order and confidence of its own turn. The three the
        // glass chooses between its own three glasses by, and the two the ready story's window is
        // cut at. All three are in the record the engine already receives.
        twirl: Number((st.polar || {}).twirl) || 0,
        rotationalN: Number((st.rotational || {}).n) || 0,
        rotationalScore: Number((st.rotational || {}).score) || 0,
        horizonY: ((st.horizon || {}).y === null || (st.horizon || {}).y === undefined)
          ? null : Number(st.horizon.y),
        // HOW STRONGLY THE WORK CARRIES A WATERLINE OF ITS OWN, off the record's own measured
        // strength rather than only its presence on the motif list. lab/step1-motifs.py:347-360
        // scores the seam it best fits by how far the two sides differ in light and in busy-ness,
        // and lab/build-workrecords-v1.py:121 carries that score beside the line itself as
        // `structure.horizon.seam`. `locusOf` still ranks a measured seam as whole evidence when it
        // ranks the three loci — that is a routing decision and reads the motif list, not this.
        seamStrength: Number((st.horizon || {}).seam) || 0,
        // the repeat the work carries ACROSS a crease, as a count over its own frame side
        gridCount: side > 0 && Number((st.grid || {}).periodPx) > 0
          ? side / Number(st.grid.periodPx) : 0,
        // how much of the difference between the work's own columns its region line explains
        regionScore: Number((st.regions || {}).score) || 0,
        // WHERE THE WORK'S OWN REGION LINE FALLS, AND HOW CLEANLY IT DIVIDES THE PICTURE — both
        // axes, because which one the fold reads is decided by the crease's own direction and not
        // here. `structure.regions.line.{x,y}.at` is the place along that axis, a share of the
        // frame; `.explains` is the between-versus-within column reading at that place, the plain
        // two-means split, and it is handed with the instrument's own floor UNAPPLIED so the gate
        // stays where the gate lives. Both are a Python mirror of `lab/effects/box.js`'s own
        // `seamOf`, verified against that file's published readings, and they landed in the record
        // on 2026-08-26. Until they did, this file could hand no line at all and said so.
        //
        // `.explains` IS NOT `regions.score` ABOVE, and the two must not be confused: the score is
        // the share of frame the large regions cover, a different quantity in the same 0..1 range.
        // Pointing the instrument's own floor at it would open a gate on grounds nobody measured.
        regionLineXAt: Number((((st.regions || {}).line || {}).x || {}).at),
        regionLineXExplains: Number((((st.regions || {}).line || {}).x || {}).explains),
        regionLineYAt: Number((((st.regions || {}).line || {}).y || {}).at),
        regionLineYExplains: Number((((st.regions || {}).line || {}).y || {}).explains),
        // the work's own device: how many regions it falls into, the step it was cut at and the
        // angle of that step — what a passage revealing the making has to read
        regionCount: Number((st.regions || {}).count) || 0,
        deviceStepPx: Number((st.ownDevice || {}).stepPx) || 0,
        // WHAT THE WORK'S OWN DEVICE IS AND HOW MANY TIMES IT REPEATS — the radial repeat the fold
        // tiles outward at, where that device is rings.
        deviceKind: String((st.ownDevice || {}).kind || ""),
        deviceCount: Number((st.ownDevice || {}).count) || 0,
        deviceAngleDeg: Number((st.ownDevice || {}).angleDeg) || 0,
        gridPeriodPx: Number((st.grid || {}).periodPx) || 0,
        gridAngleDeg: Number((st.grid || {}).angleDeg) || 0,
        frameSide: side,
        // how confidently the work's own device was recovered — how legibly its making reads
        deviceConfidence: Number((st.ownDevice || {}).confidence) || 0,
        // WHERE THE WORK STANDS ON THE COLLECTION'S OWN COLOURFULNESS LADDER — half chroma_p90, half
        // hue_entropy (lab/step1-tone-texture.py:236-238) — which is the reading the pair's colour
        // distance is taken between. It stood only inside `tonalSpectral`, where the whole pair is
        // in hand; the fill has one work at a time, so the reading belongs here beside the others.
        // RENAMED FROM `ladderPosition`/`luminance.ladderPosition` (the judge seat's standing
        // correction of 2026-08-18/19): the field never was a tone, and now reads `palette
        // .colourfulness`.
        colourfulness: Number((work.palette || {}).colourfulness) || 0,
        // THE TONE a work parts at, off `luminance.level` (lab/build-workrecords-v1.py, itself
        // lab/analyze/recipes.py:551-613 colour_stats()'s median luminance, a port of `measure(image)`
        // in lab/effects/strata-light.js:108-113): the reading the "strata-light" branch below drives
        // `levelA`/`levelB` from, one work at a time exactly as `colourfulness` above.
        level: Number((work.luminance || {}).level) || 0,
        // THE THREE COLOUR READINGS THE EIGHTEEN VOICE HANDLES ARE DRIVEN FROM — saturation,
        // brightness and tonal contrast, each read straight off the work's own pixels by
        // lab/analyze/recipes.py:526-585 colour_stats() and carried into this record's own
        // `colour` object by lab/build-workrecords-v1.py. Before U27's colour-and-light lane these
        // three were measured and thrown away: the record carried no colour reading at all, and
        // the eighteen handles below rested at their manifest default of 0 for every pair. The
        // derivation that turns them into a period, a phase and a loudness per voice is
        // lab/step4-assembler.js:1966-2010, ported into `fillPlan`'s "grid-colour" and
        // "strata-light" branches below.
        sat: Number((work.colour || {}).sat) || 0,
        brightness: Number((work.colour || {}).brightness) || 0,
        contrast: Number((work.colour || {}).contrast) || 0,
        // THE LATTICE THE WORK CARRIES, in one place and in one order of preference: the step the
        // work was actually cut at, falling back to the repeat its own grid was measured at. Three
        // handles of the interfering instrument read exactly this pair of numbers.
        latticePx: Number((st.ownDevice || {}).stepPx) || Number((st.grid || {}).periodPx) || 0,
        // AND THE ANGLE FOLLOWS THE SAME ORDER AS THE STEP, NOT THE STEP'S PRESENCE (2026-08-24).
        // It used to ask whether a DEVICE was recovered and then take that device's angle whatever
        // that angle read — and `structure.ownDevice.angleDeg` carries a direction only for a device
        // that HAS one. A ring pattern and a tile pattern have no direction to record, so the field
        // reads its own zero for EVERY ring-cut and every tile-cut work in any collection — not most
        // of them, all of them, by the measurement's own definition. So
        // every handle downstream of this field — the interfering instrument's `turn`, `mixTurn` and
        // `regionTurn`, the beat's own `beatTilt`, the leaning instrument's `tilt`, and the camera's
        // whole ROLL axis, which folds its sign straight out of this number — read the same 0 on
        // same 0 on every such pair and could not move. The work's own measured grid angle is a
        // reading of the same thing (which way this photograph's lattice runs) and is DEFINED
        // wherever a grid is, so it answers where the device's own angle says nothing — which is a
        // fact about the two fields' domains and not about any set of pictures. The device still
        // speaks first where it recovered a direction; nothing
        // is invented, and the fallback is the one this file already takes on the other side of the
        // same reading (`gcAngle` in the grid-and-colour branch, `latFrom`/`latTo` in the parquet).
        latticeAngleDeg: Number((st.ownDevice || {}).angleDeg)
          || Number((st.grid || {}).angleDeg) || 0,
        // THE SCALE A WORK PARTS AT, off `texture.reliefEdge`/`reliefCentreMassX`/
        // `reliefCentreDetailX` (lab/build-workrecords-v1.py, itself lab/analyze/recipes.py's own
        // `strata_scale_measure()`, a port of `measure(image)` and of the centre-of-gravity reading
        // in `cut()` — lab/effects/strata-scale.js:138-141 and :279-287): the reading the
        // "strata-scale" branch below drives `massCentreXA`/`massCentreXB`/`detailCentreXA`/
        // `detailCentreXB` from, one work at a time exactly as `level` above drives strata-light's.
        reliefEdge: Number((tex || {}).reliefEdge) || 0,
        reliefCentreMassX: Number((tex || {}).reliefCentreMassX) || 0.5,
        reliefCentreDetailX: Number((tex || {}).reliefCentreDetailX) || 0.5,
        // THE SAME DETAIL CENTRE, HANDED WITHOUT A FALLBACK, because one reader needs to know
        // whether the record carries the reading at all. `reliefCentreDetailX` above answers
        // strata-scale's own handle, which wants a place on every pair and takes the frame's own
        // middle where nothing was measured; the crystallized arrival wants the OPPOSITE answer —
        // a work whose detail stratum was never measured has no point of greatest disorder to seed
        // from, and saying «the middle» there would be a place nobody read. So the field is handed
        // raw, NaN and all, exactly as `regionLineXAt` two screens up is, and `arrivalOf` asks
        // `isFinite` of it.
        reliefCentreDetailXAt: Number((tex || {}).reliefCentreDetailX)
      };
    }

    function workParts(work, at) {
      var sets = {}, counts = {}, fig = {}, ends = {}, lists = {}, i, s, reading;
      // A RECORD THAT CARRIES NO CUTS AT ALL READS AS A WORK WITH NO CUTS, and does not throw. This
      // is `pairScore`'s own repair one screen down, in the same class and for the same reason:
      // `passageFor`'s two refusals ask a record for an `id` and for nothing else, so a record
      // carrying an id alone is one this file has agreed to compose over, and indexing an absent
      // field terminated it in a throw — worse than the refusal charter shelf 21 already forbids.
      // The neutral is the empty list, which is exactly what a record whose every set reads
      // `realCount: 0` already produces by the loop below: no element set on any kind, so the pair
      // crosses whole, which is a plainer crossing and never a refused one.
      var ownSets = Object.prototype.toString.call(work && work.sets) === "[object Array]"
        ? work.sets : [];
      for (i = 0; i < ownSets.length; i++) {
        s = ownSets[i];
        if (!s.realCount) continue;
        if (!lists[s.kind]) lists[s.kind] = [];
        lists[s.kind].push(s);
      }
      // A WORK MAY OFFER SEVERAL REAL CUTS OF ONE KIND, cut by different providers — the collection's
      // own records carry two sets of named regions, one hybrid and one semantic. Which of them acts
      // was the last of them and never moved. §4.8 lets the element selection differ across a
      // return, so the pass count and the die choose among a work's own cuts, and where the visit
      // remembers nothing the last one still acts and the passage is the passage.
      Object.keys(lists).sort().forEach(function (kind) {
        var list = lists[kind];
        var chose = list[(list.length - 1 + (at || 0)) % list.length];
        sets[kind] = chose.index;
        counts[kind] = chose.count;
        if (chose.fig !== null && chose.fig !== undefined) fig[kind] = chose.fig;
      });
      for (i = 0; i < TRAVEL_AXES.length; i++) {
        reading = axisReading(work, TRAVEL_AXES[i]);
        if (reading !== null) ends[TRAVEL_AXES[i]] = encodeEnds(TRAVEL_AXES[i], reading);
      }
      var found = locusOf(work), locusKind = found[0], locus = found[1], locusFit = found[2];
      var polar = (work.structure || {}).polar || {}, keys = Object.keys(POLAR_WORLD).sort();
      var best = null, bestv = null, v;
      for (i = 0; i < keys.length; i++) {
        v = polar[keys[i]];
        if (v === null || v === undefined) continue;
        if (bestv === null || v > bestv || (v === bestv && keys[i] > best)) {
          best = keys[i];
          bestv = v;
        }
      }
      return {
        sets: sets, counts: counts, fig: fig, ends: ends, measured: measuredParts(work),
        // THE FOURTH ELEMENT IS locusOf's OWN fit, ADDED FOR arrivalOf (naряд S-06). The first
        // three packed the kind and the point exactly as before; the fit itself stayed local to
        // `compose`'s own casting, and `arrivalOf` needs it in hand to rank CONDENSED against the
        // other four arrivals rather than only asking whether it is "none".
        locus: [LOCUS_KINDS.indexOf(locusKind)].concat(locus || [0, 0]).concat([r4(locusFit)]),
        world: (best && bestv && bestv > 0) ? WORLDS.indexOf(POLAR_WORLD[best]) : -1,
        providerOf: (function () {
          var out = {};
          ownSets.forEach(function (s2) { out[s2.index] = s2.provider; });
          return out;
        }())
      };
    }

    // THE FIVE ARRIVALS, RANKED RATHER THAN GATED (charter shelf 7, naряд S-06). Every arrival is
    // a candidate for every pair, exactly as a genre is (`genresFor`): each gets a fit read off
    // the pair's own measured records and never off a typed floor, and the strongest fit plays.
    //
    // CARRIED has nothing of its own to read — the gesture already running is always available —
    // so it stands at 0 and is what plays where none of the other four reads anything at all.
    //
    // CONDENSED reuses `locusOf`'s own reading of the arriving work's pole, seam or gate, already
    // packed into `toP.locus` by `workParts` above (its fourth element is that reading's own fit).
    //
    // CRYSTALLIZED reads the arriving work's own texture score — how much of it reads as grain
    // rather than as line, `measuredParts`'s own `textureScore` — as how strongly a seed at the
    // frame's own least-ordered place suits it; the seed at that peak of disorder is what the
    // pour's own seed-ordered release then radiates order out from, column by column.
    //
    // THE SEED STANDS WHERE THE WORK'S OWN GRAIN GATHERS THICKEST, and that is the whole repair of
    // 2026-08-27. Until tonight the place was `regionLineXAt`/`regionLineYAt` — the box law's own
    // seam, the between-versus-within column reading at `measuredParts:regionLine*`, which is the
    // work's own strongest DIVIDING line and therefore the most ORDERED place the record names.
    // The charter's shelf 7 asks for the opposite («CRYSTALLIZED from a seed at peak chaos») and so
    // does `LOCUS_PHRASES["grain-seed"]`, which prints «at its own point of greatest disorder» over
    // whatever this line hands it. So fit and place read two different things under one name: the
    // ranking read grain and the placement read structure.
    //
    // They read one thing now. `texture.reliefCentreDetailX` is the centre of gravity of the
    // work's own DETAIL stratum (lab/analyze/recipes.py's `strata_scale_measure()`, the same
    // reading `reliefEdge` and `textureScore` come off) — where the fine grain of the picture
    // actually gathers, which is the least-ordered place the record measures and the same family
    // of reading the fit already ranks on.
    //
    // AND IT IS A PLACE ACROSS THE FRAME'S WIDTH, WITH NO HEIGHT, because that is what was
    // measured. The relief reading cuts the picture into strata along one axis and takes its centre
    // of gravity along that axis alone; no record in this collection publishes a height for it. So
    // the seed stands at that width on the frame's own mid-height, and the mid-height is the same
    // "nothing was read here" neutral `radialCx`/`radialCy` already stand at — never a height
    // invented for the seed. The pour, which is the instrument that plays this arrival's own
    // spreading order, cuts the frame into COLUMNS and measures a column's distance from the seed
    // across the frame's width, so the axis the record measures is exactly the axis the picture
    // spends. A record carrying no relief reading at all seeds nowhere and reads "none", exactly as
    // a locus with nothing to report does above.
    //
    // PROPAGATED reads the arriving work's own rotational reading, `rotationalScore`, gated only
    // on there being more than one copy for the change to run through — `rotationalN >= 2` is an
    // existence question, the same kind `genresFor`'s own "arrives on rings" already reads, and
    // not a typed floor laid over a continuous number.
    //
    // INTERFERED reads the PAIR's own two rhythms — how near the two works' own measured lattices
    // stand, in period and in angle, `latticePx`/`latticeAngleDeg` — the same two numbers overlay's
    // own `scale` and `turn` handles already read off this pair for the same reason (charter shelf
    // 10: near-matched rhythms beat into a moiré, and near angles do too). A pair with no measured
    // lattice on either side reads nothing here, which is the honest answer and not a refusal.
    function arrivalOf(fromP, toP) {
      var mf = fromP.measured, mt = toP.measured;
      var locusKind = LOCUS_KINDS[num(toP.locus[0])];
      var locusAt = locusKind === "none" ? null : [toP.locus[1], toP.locus[2]];
      var locusFit = num(toP.locus[3]);
      var pool = [{ id: "CARRIED", fit: 0, kind: "none", at: null },
                  { id: "CONDENSED", fit: locusFit, kind: locusKind, at: locusAt }];
      var seedAt = isFinite(mt.reliefCentreDetailXAt)
        ? [r4(clamp01(mt.reliefCentreDetailXAt)), 0.5] : null;
      pool.push({ id: "CRYSTALLIZED", fit: readingOf(mt.textureScore),
                  kind: seedAt ? "grain-seed" : "none", at: seedAt });
      pool.push({ id: "PROPAGATED",
                  fit: mt.rotationalN >= 2 ? readingOf(mt.rotationalScore) : 0,
                  kind: "none", at: null });
      var haveLattice = mf.latticePx > 0 && mt.latticePx > 0;
      var ratio = haveLattice
        ? Math.min(mf.latticePx, mt.latticePx) / Math.max(mf.latticePx, mt.latticePx) : 0;
      var angleDelta = haveLattice
        ? Math.abs(mt.latticeAngleDeg - mf.latticeAngleDeg) % 180 : 90;
      // INTERFERED COMBINES ITS TWO READINGS BY THEIR OWN MINIMUM, NEVER THEIR PRODUCT (P4 of the
      // 2026-08-27 review). `ratio` (how near the two periods stand) and `1 - angleDelta/90` (how
      // near the two angles stand) are two READINGS of the same shape as every other candidate's
      // own single reading in this pool — each already a share of its own [0, 1] span — and this
      // is exactly the shape `genresFor` combines two such readings under, right above: the
      // "kaleidoscope"/"spin" pair takes `Math.min(readingOf(rFrom.score), readingOf(rTo.score))`,
      // "symmetry-slide"/"stripes" takes `Math.min(readingOf(bFrom.score), readingOf(bTo.score))`,
      // and "tonal-and-spectral" takes `Math.min(bridge.tonal, bridge.spectral)` — never a product
      // of two readings anywhere in that function. A PRODUCT OF TWO [0, 1] READINGS IS PROVABLY
      // NO GREATER THAN THEIR MINIMUM (`a*b <= min(a, b)` for any `a, b` in `[0, 1]`, with equality
      // only where one of them is exactly 1), so the product this line used to compute understated
      // INTERFERED against every other candidate in `pool` by construction, whatever the two
      // works' own readings actually were — a pair whose period and angle both stand at a genuine
      // 0.8 near-match scored 0.64, not 0.8, purely from the arithmetic and not from anything the
      // pair failed to read. This is provable from the shape of the formula alone, over the whole
      // span either reading can take, and needs no run over any particular collection to show it
      // (his 2026-08-19 word: corpus counts prove nothing a construction cannot already prove).
      // `Math.min` puts INTERFERED back on the same footing as CONDENSED, CRYSTALLIZED and
      // PROPAGATED, each already a bare reading with nothing multiplied into it.
      pool.push({ id: "INTERFERED",
                  fit: haveLattice ? Math.min(ratio, 1 - clamp01(angleDelta / 90)) : 0,
                  kind: "none", at: null });
      var best = pool[0], i;
      for (i = 1; i < pool.length; i++) { if (pool[i].fit > best.fit) best = pool[i]; }
      return { mode: best.id, locusKind: best.kind, locus: best.at, fit: best.fit };
    }

    function rowOf(plan) {
      var ax = plan.axis, mesh = plan.mesh, cam = plan.camera;
      return [
        0,
        ax ? TRAVEL_AXES.indexOf(ax.axis) : -1,
        flt(plan.pivot.strength),
        ax ? flt(ax.delta) : 0,
        flt(plan.seed),
        flt(plan.readiness),
        flt(cam.panFrom[0]), flt(cam.panFrom[1]), flt(cam.panTo[0]), flt(cam.panTo[1]),
        flt(cam.logScale),
        mesh ? flt(mesh.sizeFrom) : -1,
        mesh ? flt(mesh.sizeTo) : -1,
        mesh ? flt(mesh.ratio) : -1,
        (mesh && mesh.bandPeriod !== null && mesh.bandPeriod !== undefined)
          ? flt(mesh.bandPeriod) : -1,
        REGISTERS.indexOf(plan.register)
      ];
    }

    // ---- the fill, and the score it serialises into ----

    function fractional(v) { return v - Math.floor(v); }

    // The golden angle of a count: charter shelf 13's stagger instrument, which is what keeps no
    // two fragments of a cascade in line. The constant is the golden section itself and is
    // measured by nothing, because it is a number rather than a reading.
    //
    // CAPABILITY — the golden section itself, a fact about arithmetic. Nothing about any pair or any
    // machine could move it; what could change is only how many of its digits are written here.
    var GOLDEN = 0.6180339887;
    function goldenStagger(count) { return fractional(count * GOLDEN); }

    // `singsLightColour` STOOD HERE AND IS RETIRED INTO THE GENERAL RULE. It asked one question of
    // one level — does this cue own LIGHT-COLOUR — and it was the only place in the composer where
    // a non-owner's handles were actually held at rest. The question is the same for every level
    // now and it is asked in one place, `ownsLevelOf` beside `tracksFor`, off the level each handle
    // publishes in its own instrument's manifest. `buildTemplate` takes an unowned level's handles
    // off the cue's track list, so nothing this branch computes for such a handle would be written
    // anyway; the three guards below stand so the reading is not taken at all, and each asks
    // `ownsLevelOf` rather than naming a level here.

    // ---- the accompanying colour-and-light voices (lab/step4-assembler.js:1966-2010) ----
    //
    // THE EIGHTEEN VOICE HANDLES — grid-colour's six and strata-light's twelve — are what the lab
    // calls the accompanying voices: a colour voice and a light voice, singing the collection's own
    // saturation, brightness and contrast as a period, a phase and a loudness. The lab solved this
    // derivation once, on the assembler that composes a passage ahead of time; this ports its FIRST
    // pass only into the composer, which derives a passage at the instant two works meet and reads
    // it from the two works' own records rather than from a rendered probe. What is NOT ported is
    // named below, at the branches that use these helpers.
    //
    // BEAT_DIAL — the tempo one layer's own handle moves at, measured in the same units the layer's
    // period is published in. lab/step4-assembler.js:60-66: LEN = 6.0s, OVERLAP = LEN*2/3 = 4.0s,
    // LAYER = (LEN + OVERLAP)/2 = 5.0s, BEAT = LEN − LAYER = 1.0s, and BEAT_DIAL = BEAT / LAYER =
    // 0.2 — the same beat, measured in one layer's own handle travel rather than in seconds.
    //
    // UNJUSTIFIED. It is carried from the lab's own assembler word for word, and it was unmeasured
    // there: nothing in that file derives the fifth either. Carrying a number faithfully is not the
    // same as deriving it, and this line says which of the two happened.
    var BEAT_DIAL = 0.2;

    // VOICE_SHARE — how much of a work's own measure becomes a voice's loudness. Carried from
    // lab/step4-assembler.js:91, where its own comment names it plainly: "ЧЕТВЕРТЬ ЗДЕСЬ — ЧИСЛО
    // ВКУСА, поднято в отчёте" — a quarter is a number of taste, raised in a report rather than
    // measured. It is carried here as that same admitted number, not re-derived as if it were one.
    // UNJUSTIFIED, on the lab's own admission quoted above.
    var VOICE_SHARE = 0.25;

    // WHEN A VOICE IS SEEN, AND IT IS THE LAB'S OWN MEASUREMENT — the second pass of
    // lab/step4-assembler.js, ported here 2026-08-24 on his word watching the live route (the colour
    // does not visibly read during a crossing). The first pass alone stood here until now: amplitude
    // = VOICE_SHARE of the work's own measure, written and never checked. The lab does not stop
    // there. lab/step4-assembler.js:102-105 carries a MEASURED threshold — VISIBLE = 5/255, with
    // VOICE_TARGET the nearest distinguishable step above it, 6 of 255 — and beside it the reading
    // that set it: «замер 12.08 на паре «по цвету» — контраст второй работы 0,083, размах 0,0208,
    // вершина голоса 0,0187, то есть 4,77 из 255 при пороге 5». Its law follows in the same breath:
    // «Заявленный и неслышный голос — пустое утверждение разбора» — a declared and unseeable voice is
    // an empty claim, so the analysis does not declare one.
    //
    // WHAT WAS NOT PORTED WITH IT, AND WHY IT CAN BE NOW. The lab reaches the voice's own peak by
    // RENDERING the layer off-screen twice, with the voice and without, because it cannot predict
    // where the crest of the curve falls («Предсказать движение пикселей по числам голоса нельзя»).
    // The composer derives a passage at the instant two works meet and can render nothing — which is
    // why the note below this block said the loop stays in the lab. But the curve is written down:
    // lab/effects/grid-colour.js:343 drives every one of these voices as
    // `amp · sin(2π(u/period + phase)) · 4u(1−u)`, and the composer WRITES the period and the phase
    // itself, two lines above wherever it writes the amplitude. So the crest is closed-form in
    // numbers already in hand — the SAME curve the effect will draw, evaluated on the SAME two
    // numbers this file is about to write beside the amplitude, which is why no probe is needed and
    // why the answer is exact rather than approximate. The lab's own recorded reading of 12.08 —
    // amplitude 0,0208, peak 0,0187 — is the same arithmetic seen from the rendering side, and it is
    // quoted as the provenance of the threshold above rather than as evidence that this returns the
    // right number; what makes it right is that it is the curve's own maximum.
    //
    // CAPABILITY — six steps of an eight-bit channel, which is the smallest difference above the
    // threshold the eye reads on a rendered frame. It is a fact about the channel and about seeing,
    // and it is a measurement in the unit the eye reads rather than a distribution over anything.
    var VOICE_SEEN = 6 / 255;
    function voicePeak(period, phase) {
      if (!(period > 0)) return 0;
      var best = 0, i, u, v;
      // Walked rather than solved: the crest of a sine inside a parabolic window has no closed root,
      // and the walk is over a curve the composer already knows every number of. A thousand steps
      // resolve the crest to four decimal places, which is the precision a score is written at.
      for (i = 0; i <= 1000; i++) {
        u = i / 1000;
        v = Math.abs(Math.sin(2 * Math.PI * (u / period + (phase || 0)))) * 4 * u * (1 - u);
        if (v > best) best = v;
      }
      return best;
    }
    // THE LOUDNESS A VOICE ACTUALLY SINGS AT, by the lab's own three-part law
    // (lab/step4-assembler.js:2015-2031): a quarter of the work's own measure where that is already
    // seen; raised to the least amplitude that IS seen where it is not; and never past the work's own
    // measure, which is the ceiling — a voice cannot be louder than the thing it is a voice of.
    // Where even the ceiling cannot be seen the voice does not sing and `null` says so, and the
    // caller leaves its handles unwritten exactly as the lab's own mute does. That is not a crossing
    // refused: shelf 17's budget shapes a passage that is already playing, and a passage whose colour
    // voice stays silent still plays every other voice it has.
    //
    // WHAT WAS STILL WRONG WITH IT ON 2026-08-24, and it is the same defect the camera lane closed
    // this morning, met from the other side. Two things stood in `max(quarter, want)`:
    //
    //   1. A MAX IS A FLOOR THAT FLATTENS. Every voice whose quarter falls under `want` landed on
    //      exactly `want` — one number, identical on every pair, whatever the two works read. That
    //      is shelf 9's disease in miniature: the reading stopped ranking below the threshold. The
    //      straight line `floor + (1 − floor) · share` keeps the ranking all the way down, which is
    //      the whole reason the camera's own repair is a line and not a max.
    //   2. `want` IS A STILL-FRAME LEVEL AND A CROSSING IS NOT STILL. Six parts in 255 is what the
    //      lab measured on a held frame; a wobble that small, written over a picture that is itself
    //      moving, is inside the picture's own tonal spread and never reads. What it has to stand
    //      out of is the ground the two photographs put on the frame between them — the same
    //      sentence the camera lane writes about grain: below the pair's own reading there is
    //      nothing on screen to read the voice against.
    //
    // SO THE LEVEL IS THE PAIR'S OWN, and it is the WEAKER of the two works' readings of this same
    // measure — `groundReadings`' own law a few screens up, and the same shape as the camera's finer
    // grain: the end that carries least is what the voice must clear to be heard across both. It is
    // handed in by the caller because only the caller knows which measure this voice sings, and a
    // colour ground under a light voice is exactly the family mix-up the judge seat's standing
    // correction of 2026-08-18/19 names. Where a caller hands none, the lab's own `want` stands
    // alone and the arithmetic is unchanged in shape.
    //
    // THE CEILING IS THE WORK'S OWN MEASURE, unchanged: a voice cannot be louder than the thing it
    // is a voice of. So the loudness is bounded in [min(level, measure), measure], rises with the
    // work's own measure everywhere (the two pieces meet at `measure = level` with the same value),
    // and is never faked: where even the ceiling cannot clear the lab's own threshold the voice does
    // not sing and `null` says so, exactly as it always did.
    function voiceLoudness(measure, period, phase, ground) {
      var peak = voicePeak(period, phase);
      if (!(measure > 0) || !(peak > 0)) return null;
      // THE AMPLITUDE HAS TO CLEAR THE THRESHOLD AFTER IT IS WRITTEN DOWN, not before. A score keeps
      // four decimal places, so the least loudness that is seen is rounded UP to that place: rounded
      // to nearest, a voice raised to exactly the threshold lands a hundredth of a step under it on
      // the wire and is declared unseeable by its own law.
      var want = Math.ceil(VOICE_SEEN / peak * 10000) / 10000;
      if (want > measure) return null;
      var level = (ground > 0 && ground > want) ? ground : want;
      var floor = voiceFloor(level, measure);
      var v = measure * voiceReach(floor, VOICE_SHARE);
      if (r4(v) < want) v = want;
      return clamp01(v);
    }
    // ONE VOICE, WRITTEN OR LEFT SILENT — the one home of that decision, so a voice cannot be muted
    // by one instrument's branch and declared by another's. The three instruments that carry these
    // voices all publish the same three handles per voice, `<stem>Period<tail>` and its phase and its
    // amplitude, so one shape serves all three.
    // `ground` is the level this voice has to clear to be heard — the pair's own weaker reading of
    // the SAME measure the voice sings, handed in by the branch that knows which measure that is.
    function sayVoice(wanted, stem, tail, measure, period, phase, ground) {
      var amp = voiceLoudness(measure, period, phase, ground);
      if (amp === null) return false;
      wanted[stem + "Period" + tail] = flt(r4(period));
      wanted[stem + "Phase" + tail] = flt(r4(phase));
      wanted[stem + "Amp" + tail] = flt(r4(amp));
      return true;
    }

    // RATIOS and RATIO_BAND — the small-integer ratios an accompanying voice's period must not sit
    // near, and the band around each. lab/step4-assembler.js:84-85 (RATIOS, RATIO_BAND = 0.05),
    // serving the plan's own «Правила времени»: accompanying voices carry incommensurable periods
    // so they never repeat together exactly.
    //
    // CAPABILITY — which small whole-number ratios beat against each other, which is a fact about
    // arithmetic and about nothing else: two periods standing at one of these repeat together, and
    // that is true of any two periods anywhere.
    var VOICE_RATIOS = [1 / 1, 1 / 2, 1 / 3, 1 / 4, 1 / 5, 2 / 3, 2 / 5, 3 / 4, 3 / 5, 4 / 5];
    // UNJUSTIFIED — how near a ratio has to stand to one of those before it counts as that ratio.
    // It is carried from the lab, unmeasured there, and nothing here derives it: what it has to
    // satisfy is only that it be smaller than the gaps between the ratios above, and many values are.
    var VOICE_RATIO_BAND = 0.05;

    // aligned(p, q) — whether two periods sit within the band of one of the small-integer ratios
    // above, measured in the log so the answer does not depend on which of the two is divided by
    // which. Ported unchanged from lab/step4-assembler.js:1613-1620 (`aligned`).
    function voicesAligned(p, q) {
      var r = Math.log(p / q), band = Math.log(1 + VOICE_RATIO_BAND), i, v;
      for (i = 0; i < VOICE_RATIOS.length; i++) {
        v = Math.log(VOICE_RATIOS[i]);
        if (Math.abs(r - v) <= band || Math.abs(r + v) <= band) return VOICE_RATIOS[i];
      }
      return 0;
    }

    // spread(base) — nudges each of a set of periods up by one percent, as many times as it takes,
    // until it no longer sits in a small-integer ratio with any period already placed before it.
    // Ported unchanged from lab/step4-assembler.js:1622-1636 (`spread`).
    function voiceSpread(base) {
      var out = [], i, j, v, steps, hit;
      for (i = 0; i < base.length; i++) {
        v = base[i]; steps = 0;
        for (;;) {
          hit = 0;
          for (j = 0; j < i; j++) if (voicesAligned(v, out[j].value)) { hit = 1; break; }
          if (!hit || steps > 200) break;
          v *= 1.01;
          steps++;
        }
        out.push({ value: v, steps: steps });
      }
      return out;
    }

    // ONE SCALE, STATED ONCE, FROM A MEASURED RATIO TO A SHARE OF A HANDLE'S OWN SPAN. A handle
    // publishes a floor, a ceiling and a default; a work publishes a reading. What no file in this
    // tree records is how many units of a reading one step of a handle is worth — the gap
    // HANDLE_SOURCE calls «uncalibrated». What IS measured is the RATIO between the two works'
    // readings, and a ratio needs one number to become a position: how many doublings of the
    // reading cross the handle's whole span. That number is typed here, it is the only one of its
    // kind in this file, and it stands on the revisit list.
    // THE FAMILY BREATHES ON A FURTHER PASS, AND THE BREATH IS THE WALK'S. Charter shelf 16 and
    // §4.4f: an edge met again inside a visit holds its family and shifts its shaping numbers a
    // little. That roll has one home and it is not this file — the visit-memory lane landed it in
    // the walk, where the pass count lives, and it reads the list below as its list of what may
    // never move. So this file writes no drift and instead keeps that list honest: `measuredHandles`
    // on every cue names exactly the handles the composer asked for off the two works' records, and
    // a handle wrongly in it stands still where it should breathe while one wrongly out of it
    // breathes over a measurement nobody read (his 19:13 word lifted to the class at 19:21).
    //
    // What answers the return HERE is everything the family does not fix: the order of the moves,
    // the actors and the rhythm, each varied from the die and the pass count in `compose` above.

    // UNJUSTIFIED — and it is the most consequential unmarked number that stood in this file. It
    // carries no sentence anywhere and nothing derives it, while `acrossTheSpan` and `alongTheSpan`
    // below read it for EVERY travelling handle the composer writes: one unmeasured four sets how
    // far every handle in this file moves.
    //
    // WHAT IT DOES, said plainly so the next reader does not have to work it out. It says a ratio of
    // sixteen to one between the two works' readings uses the handle's whole published span, and
    // that any ratio wider than that is held at the span's own end. So it decides how sensitively
    // every travelling handle answers the pair: two pairs standing three to one and eight to one
    // apart land at different places on one handle precisely because of this number, and every pair
    // past sixteen to one lands on the same place — which is the clamp shape the camera lane has
    // already named once elsewhere, here at the far end of the scale rather than at the near one.
    //
    // Nothing in this tree measured it and no file records what it should be. What it has to satisfy
    // is only that it be positive, so the map is monotone in the ratio and lands on the handle's own
    // default where the ratio is one; every positive value satisfies that equally, and this seat
    // picked four.
    var OCTAVES_PER_SPAN = 4;

    // WHERE A READING STANDS IN ONE HANDLE'S OWN RANGE, READ OFF ONTO ANOTHER'S. Two handles of one
    // instrument that answer to the same thing — the count a fabric is cut into and the speed that
    // count travels at — carry their own published ranges, and a position in the first is a
    // position in the second. No number of this file's own enters, so nothing here can go stale
    // against a manifest that moves.
    function betweenSpans(instr, fromHandle, toHandle, value) {
      var a = HANDLE_SPECS[instr][fromHandle], b = HANDLE_SPECS[instr][toHandle];
      var lo = num(a[0]), hi = num(a[1]);
      var at = hi > lo ? (Math.min(hi, Math.max(lo, value)) - lo) / (hi - lo) : 0;
      return num(b[0]) + at * (num(b[1]) - num(b[0]));
    }

    function acrossTheSpan(instr, handle, from, to) {
      var spec = HANDLE_SPECS[instr][handle], lo = spec[0], hi = spec[1], mid = num(spec[2]);
      var d = Math.log2(Math.max(from, 1e-6) / Math.max(to, 1e-6)) / OCTAVES_PER_SPAN;
      d = Math.max(-1, Math.min(1, d)) / 2 * (hi - lo);
      return [flt(r4(Math.min(hi, Math.max(lo, mid + d)))),
              flt(r4(Math.min(hi, Math.max(lo, mid - d))))];
    }

    // THE SAME SCALE FOR A HANDLE THAT TAKES ONE NUMBER RATHER THAN TWO (2026-08-24). `acrossTheSpan`
    // answers a pair of ends; a handle a branch fills with a single value had nowhere to go and was
    // handed the raw reading, which `appliedValue` below then CLAMPED — and a clamp is the mechanism
    // behind «works the same on every picture». A reading that falls outside a handle's own published
    // range does not become that range's edge; every reading outside it becomes THE SAME edge,
    // whichever two photographs are standing there. Measured on the collection: the glass's own
    // magnification is the ratio of the two works' cutting steps, so every ordered pair whose
    // arriving work is cut finer than its departing one — half of them, by construction — asked for
    // a value under 1 and landed on exactly 1, the range's floor; the fold's own radial repeat asked
    // for a ring count in the tens against a ceiling of 2 and landed on 2 every time.
    //
    // The road out is the one already stated for the two-ended case, read for one end: what no file
    // records is how many units of a reading one step of a handle is worth, what IS measured is a
    // RATIO, and `OCTAVES_PER_SPAN` is the one number that turns a ratio into a position. So the
    // reading is placed about the handle's OWN default, a doubling at a time, and the whole span is
    // reachable. It is monotone in the ratio, it lands exactly on the default where the ratio is 1
    // — which is where the reading says the two ends of it are the same — and both its own ends stay
    // inside the handle's published range by the same `min`/`max` `acrossTheSpan` closes with.
    function alongTheSpan(instr, handle, ratio) {
      var spec = HANDLE_SPECS[instr][handle], lo = num(spec[0]), hi = num(spec[1]);
      var mid = num(spec[2]);
      var d = Math.log2(Math.max(ratio, 1e-6)) / OCTAVES_PER_SPAN;
      d = Math.max(-1, Math.min(1, d)) / 2 * (hi - lo);
      return Math.min(hi, Math.max(lo, mid + d));
    }

    function appliedValue(instr, handle, requested) {
      var spec = HANDLE_SPECS[instr][handle], lo = spec[0], hi = spec[1], dflt = spec[2];
      function tidy(v) {
        return Number.isInteger(num(v)) ? num(v) : flt(num(v));
      }
      if (requested === null || requested === undefined) return [tidy(dflt), tidy(dflt)];
      var v2 = num(requested);
      return [tidy(v2), tidy(Math.min(hi, Math.max(lo, v2)))];
    }

    function noteFor(handle, requested, applied, why) {
      if (requested === null || requested === undefined) {
        return "at the manifest default: " + why;
      }
      var same;
      if (Array.isArray(requested) && Array.isArray(applied)) {
        same = requested.length === applied.length;
        for (var i = 0; same && i < requested.length; i++) {
          if (num(requested[i]) !== num(applied[i])) same = false;
        }
      } else {
        same = num(requested) === num(applied);
      }
      if (same) return "requested " + pyText(requested) + " and applied, from " + why;
      return "requested " + pyText(requested) + ", applied " + pyText(applied)
        + " — the handle's own range does not reach the measured value. From " + why;
    }

    // ============================================================================================
    // THE PLAN'S MOTION PEAK — charter shelf 5, THE CONJUROR
    // ============================================================================================
    // The shelf's own sentence: "the content swap sits at the plan's motion peak, computable as
    // argmax of summed normalized parameter velocity, where the eye is led away". Everything below
    // is that sentence and nothing else. Nothing here is prepared before the visit, nothing is
    // indexed by the pair, and nothing is chosen at bake: the reading is taken off the score this
    // composition has just written, at the instant two photographs meet.
    //
    // THE SUM. Over the passage's own normalised time, every handle the plan drives has a rate of
    // change. Each is divided by that handle's OWN PUBLISHED RANGE — `HANDLE_SPECS[instrument][h]`,
    // the manifest's own min and max — so a handle that swings across a wide span does not drown
    // one that swings across a narrow one, and every term is in the same unit: fractions of a
    // handle's own range per unit of passage time. The sum of those terms is one dimensionless
    // reading of how fast the whole plan is moving at an instant.
    //
    // TWO HANDLES ARE OUT OF THE SUM, AND FOR ONE REASON: a measurement cannot read the thing it is
    // placing.
    //
    //   THE DOOR is the content swap itself — the cue's own `doors` record names the handle, and
    //   what it carries is the share of the arriving work standing in the frame. Counting its speed
    //   would make the shelf's law say the swap sits where the swap moves fastest, which says
    //   nothing. It is also where the eye is looking rather than where the eye is led away, which
    //   is the half of the sentence that names what the sum is for.
    //
    //   THE CAMERA's own track is the other. Its two middle points are what this reading PLACES, so
    //   their velocity is a consequence of the answer and never an input to it. The flight's
    //   magnitudes are read a few lines below off the same pair, after the two points are placed;
    //   the order is what keeps the loop out.
    //
    // A HANDLE WHOSE RANGE IS EMPTY, and an operator this file writes nowhere, each add nothing and
    // refuse nothing. The reading RANKS: a plan whose handles barely move still has a peak, and the
    // crossing still plays. There is no floor here and no threshold anywhere below.
    //
    // THE WALK STANDS STRICTLY INSIDE THE PASSAGE. The two ends are where the two works stand
    // still — the camera's own first and last points are the neutral rest pose, shelf 2's "resting
    // exactly when B stands" — so the instant the eye is led away is an instant INSIDE the
    // crossing rather than one of its two ends. A thousand steps is the same walk `voicePeak` above
    // already takes over a curve this file knows every number of, and for the same stated reason:
    // it resolves the crest to four decimal places, which is the precision a score is written at.
    //
    // THE PEAK IS A PLATEAU'S MIDDLE, not its first instant. Where several instants tie for the
    // maximum the peak is the middle of the first run of them, so a sum that never changes at all
    // reads as the passage's own middle rather than as its first step — the argmax of a flat
    // function is the whole span, and the whole span's middle is the honest name for it.
    //
    // CAPABILITY — the resolution of the walk, and it is a fact about the wire rather than a choice
    // about pictures: a score is written to four decimal places, and a thousand steps resolve the
    // peak to that precision. It is the same walk `voicePeak` above already takes, for the reason
    // stated there.
    var PEAK_STEPS = 1000;

    // THE FOUR NAMED CURVES AND THEIR DERIVATIVES, WRITTEN OUT. The four shapes are the drawing
    // host's own (`pass-layer.js`'s `CURVES`), carried here so the rate this file reads is the rate
    // the viewer actually sees:
    //
    //     linear(x) = x                 linear'(x) = 1
    //     smooth(x) = x²(3 − 2x)        smooth'(x) = 6x(1 − x)
    //     in(x)     = x²                in'(x)     = 2x
    //     out(x)    = 1 − (1 − x)²      out'(x)    = 2(1 − x)
    //
    // Every one of the four derivatives is bounded on nought to one, and 2 is the largest any of
    // them reaches — `in` at the close, `out` at the open, `smooth` 1.5 at the middle. That is the
    // first half of the bound the whole sum answers to.
    var PEAK_CURVES = {
      linear: [function (x) { return x; }, function () { return 1; }],
      smooth: [function (x) { return x * x * (3 - 2 * x); },
               function (x) { return 6 * x * (1 - x); }],
      "in": [function (x) { return x * x; }, function (x) { return 2 * x; }],
      out: [function (x) { return 1 - (1 - x) * (1 - x); },
            function (x) { return 2 * (1 - x); }]
    };

    // THE MONOTONE SPLINE'S OWN TANGENTS — `pass-layer.js`'s `splineSlopes`, Fritsch–Carlson,
    // carried over unchanged so the course this file differentiates is the course the host draws.
    function peakSlopes(pts) {
      var n = pts.length, d = [], m = [], i, h, a, b, s;
      for (i = 0; i < n - 1; i++) {
        h = num(pts[i + 1].at) - num(pts[i].at);
        d.push(h > 0 ? (num(pts[i + 1].value) - num(pts[i].value)) / h : 0);
      }
      for (i = 0; i < n; i++) m.push(i === 0 || i === n - 1 ? 0 : (d[i - 1] + d[i]) / 2);
      for (i = 0; i < n - 1; i++) {
        if (d[i] === 0) { m[i] = 0; m[i + 1] = 0; continue; }
        a = m[i] / d[i]; b = m[i + 1] / d[i];
        if (a < 0) { a = 0; m[i] = 0; }
        if (b < 0) { b = 0; m[i + 1] = 0; }
        s = a * a + b * b;
        if (s > 9) { s = 3 / Math.sqrt(s); m[i] = s * a * d[i]; m[i + 1] = s * b * d[i]; }
      }
      return m;
    }

    // ONE READING: a node's value at normalised passage time `u`, and its rate of change there,
    // handed back as `[value, slope]`. The slope is in the node's own units PER UNIT OF PASSAGE
    // TIME, so two handles living in windows of different lengths are already comparable before
    // either is divided by its own published range.
    //
    // THE DERIVATIVE OF EACH KIND, and every one of them is the derivative of the evaluator
    // `pass-layer.js` actually runs:
    //
    //   static      value is fixed              slope 0
    //   cueProgress p = (u·D − w₀)/(w₁ − w₀)    slope D/(w₁ − w₀) inside the window, 0 outside it,
    //                                           because the host clamps it and a clamped reading
    //                                           has stopped moving
    //   progress    u                           slope 1
    //   time        u·D                         slope D
    //   curve       c(x)                        slope c′(x)·x′, and 0 where x has left nought-to-one
    //   map         t₀ + (t₁ − t₀)(x − f₀)/(f₁ − f₀)
    //                                           slope (t₁ − t₀)/(f₁ − f₀)·x′; an empty `from` range
    //                                           is the node the host itself refuses, and it reads 0
    //   mix         a + (b − a)·t               slope a′ + (b′ − a′)·t + (b − a)·t′
    //   clamp       x held between min and max  slope x′ strictly between them, 0 at or past either
    //   spline      the Hermite piece between two points, with the tangents above:
    //                 H(s) = (2s³ − 3s² + 1)·vₐ + (s³ − 2s² + s)·h·mₐ
    //                      + (3s² − 2s³)·v_b   + (s³ − s²)·h·m_b
    //                 H′(x) = [ (6s² − 6s)·vₐ + (3s² − 4s + 1)·h·mₐ
    //                         + (6s − 6s²)·v_b + (3s² − 2s)·h·m_b ] / h  ·  x′
    //                                           and 0 before the first point and after the last,
    //                                           where the host holds the value
    //
    // A HOST SIGNAL A PLAN CANNOT KNOW — velocity, capability, noise, pointer — carries no shape
    // here. It is read at nought with no slope, because the composer is deciding at the instant two
    // works meet and the visitor has not moved yet. An operator this file writes nowhere is read
    // the same way. Neither refuses anything; both simply add nothing to the ranking.
    function peakRead(spec, u, cue, durSec, depth) {
      if (spec === null || spec === undefined) return [0, 0];
      if (typeof spec === "number" || isFlt(spec)) return [num(spec), 0];
      if (typeof spec !== "object") return [0, 0];
      depth = depth || 0;
      if (depth > 64) return [0, 0];
      if (spec.node) {
        var ref = (cue.nodes || {})[spec.node];
        return ref ? peakRead(ref, u, cue, durSec, depth + 1) : [0, 0];
      }
      if (spec.source !== undefined) {
        if (spec.source === "progress") return [u, 1];
        if (spec.source === "time") return [u * durSec, durSec];
        if (spec.source === "cueProgress") {
          var w = cue.window || [0, durSec];
          var w0 = num(w[0]), w1 = num(w[1]);
          if (!(w1 > w0)) return [0, 0];
          var p = (u * durSec - w0) / (w1 - w0);
          if (p <= 0) return [0, 0];
          if (p >= 1) return [1, 0];
          return [p, durSec / (w1 - w0)];
        }
        return [0, 0];
      }
      var r, ra, rb, rt, c, f, t, f0, f1, t0, t1, lo, hi;
      switch (spec.op) {
        case "static":
          return [num(spec.value), 0];
        case "curve":
          c = PEAK_CURVES[spec.name] || PEAK_CURVES.linear;
          r = peakRead(spec["in"], u, cue, durSec, depth + 1);
          if (r[0] <= 0) return [c[0](0), 0];
          if (r[0] >= 1) return [c[0](1), 0];
          return [c[0](r[0]), c[1](r[0]) * r[1]];
        case "map":
          r = peakRead(spec["in"], u, cue, durSec, depth + 1);
          f = spec.from || [0, 1]; t = spec.to || [0, 1];
          f0 = num(f[0]); f1 = num(f[1]); t0 = num(t[0]); t1 = num(t[1]);
          if (f1 - f0 === 0) return [0, 0];
          return [t0 + (t1 - t0) * ((r[0] - f0) / (f1 - f0)), (t1 - t0) / (f1 - f0) * r[1]];
        case "mix":
          ra = peakRead(spec.a, u, cue, durSec, depth + 1);
          rb = peakRead(spec.b, u, cue, durSec, depth + 1);
          rt = peakRead(spec.t, u, cue, durSec, depth + 1);
          return [ra[0] + (rb[0] - ra[0]) * rt[0],
                  ra[1] + (rb[1] - ra[1]) * rt[0] + (rb[0] - ra[0]) * rt[1]];
        case "clamp":
          r = peakRead(spec["in"], u, cue, durSec, depth + 1);
          lo = spec.min === undefined ? -Infinity : num(spec.min);
          hi = spec.max === undefined ? Infinity : num(spec.max);
          if (r[0] <= lo) return [lo, 0];
          if (r[0] >= hi) return [hi, 0];
          return r;
        case "spline":
          return peakSpline(spec, u, cue, durSec, depth);
        default:
          return [0, 0];
      }
    }

    function peakSpline(spec, u, cue, durSec, depth) {
      var pts = spec.points;
      if (Object.prototype.toString.call(pts) !== "[object Array]" || !pts.length) return [0, 0];
      var r = peakRead(spec["in"] === undefined ? { source: "progress" } : spec["in"],
                       u, cue, durSec, depth + 1);
      var x = r[0], n = pts.length, i;
      if (n === 1 || x <= num(pts[0].at)) return [num(pts[0].value), 0];
      if (x >= num(pts[n - 1].at)) return [num(pts[n - 1].value), 0];
      var m = peakSlopes(pts);
      for (i = 1; i < n - 1; i++) if (x <= num(pts[i].at)) break;
      var pa = pts[i - 1], pb = pts[i];
      var h = num(pb.at) - num(pa.at);
      if (!(h > 0)) return [num(pb.value), 0];
      var va = num(pa.value), vb = num(pb.value);
      var s = (x - num(pa.at)) / h, s2 = s * s, s3 = s2 * s;
      var value = (2 * s3 - 3 * s2 + 1) * va + (s3 - 2 * s2 + s) * h * m[i - 1]
                + (3 * s2 - 2 * s3) * vb + (s3 - s2) * h * m[i];
      var slope = ((6 * s2 - 6 * s) * va + (3 * s2 - 4 * s + 1) * h * m[i - 1]
                   + (6 * s - 6 * s2) * vb + (3 * s2 - 2 * s) * h * m[i]) / h;
      return [value, slope * r[1]];
    }

    // THE PEAK ITSELF. `at` is the instant in seconds, `share` the same instant as a share of the
    // passage, `top` the largest the sum reached and `flat` whether it ever changed at all.
    //
    // THE BOUND, BY CONSTRUCTION. Every term is |slope| divided by a published range that is
    // strictly positive, and every slope is a product of three bounded factors: a curve derivative
    // (at most 2), a handle's own travel across its published range (at most 1 after the division),
    // and the ratio of the passage's own length to the cue window's — which is finite because a
    // window with no length contributes nothing at all. So the sum is a finite sum of finite terms
    // for every cue table, and `top` is finite for every one of them.
    //
    // THE ARGMAX EXISTS FOR EVERY PASSAGE. The walk is a finite list of numbers, so it has a
    // largest; the run attaining it is non-empty, so its middle is a real index. A passage carrying
    // one cue that drives nothing but fixed readings sums to nought at every step, the run is the
    // whole interior, and the peak is the passage's own middle. Nothing here can return nothing,
    // and nothing here declines.
    function motionPeak(cues, durSec) {
      if (!(durSec > 0) || !cues || !cues.length) return { at: 0, share: 0.5, flat: true, top: 0 };
      var terms = [], i, k, u, s;
      for (k = 0; k < cues.length; k++) {
        (function (c) {
          var specs = HANDLE_SPECS[(c.instrument || {}).id] || {};
          // THE DOOR THE CUE'S OWN RECORD NAMES, AND THE CROSSING DIAL BESIDE IT. Both are out, and
          // for the one reason stated above: a measurement cannot read the thing it is placing. The
          // dial is the content swap the shelf places, whatever the door record happens to name —
          // and since the entry-door contract landed an upper voice's door record names its
          // reserved dry rather than its dial, so reading the record alone would have let the swap
          // back into the sum on exactly the voices that stand over another. The dry is out on its
          // own account: its arc is the PLAN's statement of when the voice is in the frame, not the
          // accompaniment's motion, and letting the plan's own shape decide the peak would be the
          // measurement reading its own author.
          var door = ((c.doors || {})["in"] || {}).handle;
          var tracks = c.tracks || {};
          Object.keys(tracks).sort().forEach(function (h) {
            if (h === door || h === "mix") return;
            if (h === "presence"
                && (sourceOf((c.instrument || {}).id, h) || [])[0] === "entry-door") return;
            var sp = specs[h];
            if (!sp) return;
            var range = Math.abs(num(sp[1]) - num(sp[0]));
            if (!(range > 0)) return;
            var node = (c.nodes || {})[(tracks[h] || {}).node];
            if (!node) return;
            terms.push([node, c, 1 / range]);
          });
        }(cues[k]));
      }
      var sums = [], top = -Infinity, low = Infinity;
      for (i = 1; i < PEAK_STEPS; i++) {
        u = i / PEAK_STEPS;
        s = 0;
        for (k = 0; k < terms.length; k++) {
          s += Math.abs(peakRead(terms[k][0], u, terms[k][1], durSec, 0)[1]) * terms[k][2];
        }
        sums.push(s);
        if (s > top) top = s;
        if (s < low) low = s;
      }
      var lo = -1, hi = 0;
      for (i = 0; i < sums.length; i++) {
        if (sums[i] >= top) { if (lo < 0) lo = i; hi = i; }
        else if (lo >= 0) break;
      }
      if (lo < 0) { lo = 0; hi = sums.length - 1; }
      var share = (lo + hi + 2) / 2 / PEAK_STEPS;
      return { at: share * durSec, share: share, flat: top === low, top: top };
    }

    function fillPlan(key, row, tpl, ctx) {
      var parts = key.split("__"), aId = parts[0], bId = parts[1], tag = parts[2];
      var direction = tag === "ab" ? "a->b" : "b->a";
      var fromId = tag === "ab" ? aId : bId, toId = tag === "ab" ? bId : aId;
      var fromP = ctx.fromParts, toP = ctx.toParts;
      var pivotKind = ctx.pivot[0], pivotMeasure = ctx.pivot[1], cut = ctx.pivot[2];
      var transform = ctx.pivot[3], elementKind = ctx.pivot[4], cutKinds = ctx.pivot[5];
      var duration = tpl.duration;

      var axis = null;
      if (num(row[1]) >= 0) {
        var name = TRAVEL_AXES[num(row[1])];
        axis = { measure: name, distance: row[3], legend: ENDS_LEGEND[name],
                 from: fromP.ends[name] === undefined ? null : fromP.ends[name],
                 to: toP.ends[name] === undefined ? null : toP.ends[name] };
      }

      var actors = [];
      function add(ref, wid, part, kind, role, ids) {
        if (part.sets[kind] === undefined) return;
        actors.push({ ref: ref, role: role,
                      elementSet: { workId: wid, provider: part.providerOf[part.sets[kind]],
                                    kind: kind },
                      elementIds: ids === null ? "all" : ids,
                      parts: part.counts[kind] });
      }
      cutKinds.forEach(function (k) {
        add("a", fromId, fromP, k, "pivot-carrier", null);
        add("b", toId, toP, k, "pivot-carrier", null);
      });
      if (axis !== null) {
        var tkind = KIND_OF_AXIS[axis.measure];
        if (tkind && cutKinds.indexOf(tkind) < 0) {
          add("a", fromId, fromP, tkind, "traveller", null);
          add("b", toId, toP, tkind, "traveller", null);
        }
      }
      [["a", fromId, fromP, "departing-figure"], ["b", toId, toP, "arriving-figure"]]
        .forEach(function (one) {
          var k = null, i;
          for (i = 0; i < cutKinds.length; i++) {
            if (one[2].fig[cutKinds[i]] !== undefined) { k = cutKinds[i]; break; }
          }
          if (k) add(one[0], one[1], one[2], k, one[3], [one[2].fig[k]]);
        });

      // THE ARRIVAL IS THE STRONGEST OF THE CHARTER'S FIVE (shelf 7), read off the pair's own
      // records by `arrivalOf` beside `workParts` above — the same ranking-not-gating shape
      // `genresFor` already gives the genres, extended from the two this file knew (CONDENSED,
      // CARRIED) to the five the charter names.
      var arrival = arrivalOf(fromP, toP);

      var castOf = { pivot: ["pivot-carrier"], travel: ["traveller"],
                     arrival: ["arriving-figure", "departing-figure"] };
      // THE POINT SEVEN INSTRUMENTS FOLD, REST AND TURN ABOUT — one road for one register row. The
      // row says «the midpoint of the two measured radial centres» and this is that midpoint,
      // taken from the two works' own records. It carries no direction, so an edge places its
      // centre in the same place whichever way the visitor walks it.
      //
      // WHAT IT REPLACES, AND WHY THAT WAS A STATIC PARAMETER IN DISGUISE. Four branches answered
      // this row from the CAMERA'S own pan — `row[6..9]`, which is the travelling axis's two ends
      // less a half. That equals the radial centre only where the travelling axis is radial; where
      // the axis carries no centre at all the pan is the origin and the row handed back exactly
      // 0.5 and 0.5, which is the module's own default, with a note claiming a measurement. Every
      // work of this collection carries a radial centre and the collection holds 45 distinct ones,
      // so the reading was there the whole time. The guard those branches carried — «either pan is
      // not negative» — dropped the centre for any pair whose two ends both sit left of the middle,
      // which no rule asks for. Both go.
      function centreOfThePair(wantedInto) {
        var cx = (fromP.measured.radialCx + toP.measured.radialCx) / 2;
        var cy = (fromP.measured.radialCy + toP.measured.radialCy) / 2;
        wantedInto.centreX = flt(r4(clamp01(cx)));
        wantedInto.centreY = flt(r4(clamp01(cy)));
      }
      // THE CAMERA'S OWN CENTRE OF A SINGLE WORK — `structure.radial.centre` (measuredParts()'s
      // `radialCx`/`radialCy`) where the work reads as radial at all (`radialScore > 0`), else the
      // centre of `structure.dominantObject.bbox` (measuredParts()'s `figureCx`/`figureCy`) where
      // that box is a real reading (`figureShare > 0`, since an absent box collapses to [0,0,0,0]
      // and a figureShare of exactly zero). Neither present answers null, which the caller below
      // reads as "this point contributes nothing to pan" rather than the frame's own middle.
      function camOwnCentre(m) {
        if (m.radialScore > 0) return [m.radialCx, m.radialCy];
        if (m.figureShare > 0) return [m.figureCx, m.figureCy];
        return null;
      }
      // PAN AT ONE MIDDLE POINT — the offset of one work's own centre from the frame's own middle,
      // (0.5, 0.5), scaled by `reach` alone (grammar law 5): the centre reading gives the
      // DIRECTION, `reach` alone gives how far the camera actually leans toward it.
      function camAxisPan(m, reach) {
        var c = camOwnCentre(m);
        return c ? [(c[0] - 0.5) * reach, (c[1] - 0.5) * reach] : [0, 0];
      }
      // PITCH AT ONE MIDDLE POINT — one work's own measured horizon, `structure.horizon.y`
      // (measuredParts()'s `horizonY`, null where the work carries none), offset from the frame's
      // own middle and scaled by `reach` and the one shared bound every axis answers to.
      function camAxisPitch(m, reach, camBound) {
        return m.horizonY === null ? 0 : (m.horizonY - 0.5) * reach * camBound;
      }
      var cues = [];
      tpl.cues.forEach(function (cue) {
        var c = copy(cue);
        c.window = [r4(num(cue.window[0]) * duration / 1000.0),
                    r4(num(cue.window[1]) * duration / 1000.0)];
        c.window = [flt(c.window[0]), flt(c.window[1])];
        c.cast = actors.filter(function (a) {
          return (castOf[c.id] || []).indexOf(a.role) >= 0;
        }).map(function (a) {
          return { ref: a.ref, workId: a.elementSet.workId, kind: a.elementSet.kind,
                   elementIds: a.elementIds };
        });
        var instr = c.instrument.id;
        var wanted = { seed: flt(r4(Math.min(8.0, Math.max(0.0, num(row[4]))))) };
        var mf = fromP.measured, mt = toP.measured;
        if (instr === "weave") {
          var n = 0;
          actors.forEach(function (a) {
            if (a.role === "pivot-carrier" && a.ref === "a") n += a.parts;
          });
          if (n) wanted.strips = n;
          // THE WOVEN BASKET, READ FROM BOTH WORKS (his word of 2026-08-17 19:13: every geometric
          // parameter a score drives is read from the work). The axis used to come off the
          // DEPARTING work's own banding alone, which collapses to that one work's own code and
          // leaves index 2 — "both", the basket, the instrument's own manifest default and his
          // named wow reference (pass-inst-weave.js:770-771) — unreachable on every cast. Where the
          // two works' own banding families genuinely disagree, the fabric honestly weaves both;
          // where they agree, it stands on the family they share; where only one work carries a
          // reading, the fabric stands on that one, exactly as it always did.
          var axFrom = fromP.ends.banding, axTo = toP.ends.banding;
          var codeFrom = (axFrom !== undefined && axFrom !== null && num(axFrom[2]) < BANDING.length)
            ? AXIS_OF_BANDING[BANDING[num(axFrom[2])]] : null;
          var codeTo = (axTo !== undefined && axTo !== null && num(axTo[2]) < BANDING.length)
            ? AXIS_OF_BANDING[BANDING[num(axTo[2])]] : null;
          if (codeFrom !== null && codeTo !== null) {
            wanted.axis = codeFrom === codeTo ? codeFrom : 2;
          } else if (codeFrom !== null) {
            wanted.axis = codeFrom;
          } else if (codeTo !== null) {
            wanted.axis = codeTo;
          }
          // THE STRIP COUNT TRAVELS FROM ONE WORK'S FAMILY TO THE OTHER'S. `strips` above is a
          // single number and it is the DEPARTING work's own count, so the fabric held that one
          // work's structure the whole way — the charter's own words for the defect: a bridge
          // playing only one work's structure reads as artificial. `nMul` multiplies the count in
          // the instrument itself, so driving it from 1 to the ratio of the two measured counts
          // makes the count travel exactly as the bridge law asks, alongside the handle. Nothing is
          // scaled and nothing is invented: the handle IS a multiplier and the two counts are
          // measured. Where the ratio runs past the handle's published span the instrument's own
          // range answers, and the note beside the node says so.
          if (n && mt.strips) wanted.nMul = [flt(1.0), flt(r4(mt.strips / n))];
          // HOW FAST THE FABRIC TRAVELS, read off the count it is cut into. Charter shelf 4: larger
          // fragments carry more inertia, so a coarse fabric of a few wide strips travels slowly
          // and a fine one quickly. The reading is placed by where the count stands inside the
          // strip handle's OWN published range, mapped onto the speed handle's own range — two
          // spans the instrument publishes and no third number, so nothing here goes stale and
          // nothing is invented. At the module's own default count this lands within a twelfth of
          // the module's own default speed.
          // 2026-08-19 AUDIT FIX (class A: the arriving work was never asked). `nMul` two lines
          // above already travels the fragment count itself from `n` to `mt.strips`, so a speed
          // read off the count and left at `n` alone stood still while the count it answers to kept
          // moving — the same gap `nMul`'s own fix closed for the count, unclosed here. Both ends
          // read the identical `betweenSpans` call `nMul`'s neighbour already uses, once per work.
          if (n && mt.strips) {
            wanted.speed = [flt(r4(betweenSpans("weave", "strips", "speed", n))),
                            flt(r4(betweenSpans("weave", "strips", "speed", mt.strips)))];
          } else if (n) {
            wanted.speed = flt(r4(betweenSpans("weave", "strips", "speed", n)));
          }
          // THE WAVE'S PERIOD, off each work's own measured spectral period as a share of that
          // work's own frame side (texture.spectralPeriodPx over frameSide) — the wavelength of
          // the very spectral band the wave's own depth gate reads. A work with no measured
          // spectral period has nothing to say here and the other work's reading stands alone
          // rather than a number being invented for it, exactly as the horizon's own fallback
          // above does for `dip`.
          var perFrom = mf.frameSide > 0 ? mf.spectralPeriodPx / mf.frameSide : 0;
          var perTo = mt.frameSide > 0 ? mt.spectralPeriodPx / mt.frameSide : 0;
          if (perFrom > 0 || perTo > 0) {
            var pFrom = perFrom > 0 ? perFrom : perTo;
            var pTo = perTo > 0 ? perTo : perFrom;
            var loWP = num(HANDLE_SPECS.weave.wavePeriod[0]);
            var hiWP = num(HANDLE_SPECS.weave.wavePeriod[1]);
            wanted.wavePeriod = [flt(r4(Math.min(hiWP, Math.max(loWP, pFrom)))),
                                 flt(r4(Math.min(hiWP, Math.max(loWP, pTo))))];
            // THE WAVE'S DRIFT READS THE SAME MEASUREMENT AS THE PERIOD, carrying no clock of its
            // own — the instrument's own manifest says so in as many words (pass-inst-weave.js
            // "it reads the SAME measurement as the period"). `betweenSpans` places the identical
            // reading onto the drift handle's own published span, exactly as `speed` above places
            // the strip count onto its own span.
            wanted.waveDrift = [flt(r4(betweenSpans("weave", "wavePeriod", "waveDrift", pFrom))),
                                flt(r4(betweenSpans("weave", "wavePeriod", "waveDrift", pTo)))];
          }
          // THE WAVE'S OWN DEPTH IS NOT WRITTEN HERE. Its register row asks for texture.type at
          // «рябь» and 1 - texture.localStraightness, and neither field reaches this file: the
          // trimmed work record the composer is handed carries no `texture.type` and no
          // `texture.localStraightness` on any work (checked across the collection's own
          // fixture), which this same register already said in as many words at the `wave` row
          // above and at "weave.depth" beside it. Writing a number for `wave` here would be a
          // number nobody measured, so the handle stays unwritten and the ribbon stands straight.
        } else if (instr === "gears") {
          if (num(row[11]) >= 0) {
            wanted.ratio = row[13];
            wanted.size = [row[11], row[12]];
            if (num(row[14]) >= 0) wanted.bandPeriod = row[14];
          }
          // WHERE THE WHEELS TURN: the midpoint of the two works' own measured radial centres. It
          // is a fact about the pair rather than about the mesh, so it stands outside the mesh's
          // own guard — a pair whose mesh was not derived still turns about its own centre.
          centreOfThePair(wanted);
          // HOW CLOSE THE DOORS STAND, off each work's own measured banding period as a share of
          // that work's own frame side — the narrower of the two, because the finer spacing is
          // the one the doors have to answer to. `row[14]` carries this same reading from
          // `meshingTravel`, but only where `pivot.measure` is «banding», which a mesh's own
          // radial pivot almost never is, so that guard stands closed on nearly every gears cue
          // and the handle was left frozen at the module's own rest. The two works' own banding
          // period is a fact about the pair, not about the mesh's own derivation, so it answers
          // here directly, outside that guard, exactly as the pair's own centre already does.
          if (wanted.bandPeriod === undefined) {
            var bandFracs = [];
            if (fromP.ends.banding && mf.frameSide > 0) {
              bandFracs.push(num(fromP.ends.banding[1]) / mf.frameSide);
            }
            if (toP.ends.banding && mt.frameSide > 0) {
              bandFracs.push(num(toP.ends.banding[1]) / mt.frameSide);
            }
            if (bandFracs.length) {
              var loBand = num(HANDLE_SPECS.gears.bandPeriod[0]);
              var hiBand = num(HANDLE_SPECS.gears.bandPeriod[1]);
              wanted.bandPeriod = flt(r4(Math.min(hiBand,
                Math.max(loBand, Math.min.apply(null, bandFracs)))));
            }
          }
          // HOW HARD THE WHEELS TURN, read off how strongly each work reads as radial. A work whose
          // rings and spokes are its own device drives the mesh; one that barely reads radial
          // barely turns, and the rate travels from the one to the other with the crossing.
          if (mf.radialScore > 0 || mt.radialScore > 0) {
            wanted.turn = [flt(r4(clamp01(mf.radialScore))), flt(r4(clamp01(mt.radialScore)))];
          }
          // HOW FAR APART THE TEETH'S OWN MOMENTS STAND — the stagger, which is charter shelf 13's
          // golden-angle instrument on the radial time axis: no two of a cascade's fragments align
          // when the stagger is the golden angle of the count. The count is the work's own measured
          // ring grain, so the number is the work's and the law is the shelf's.
          if (mf.ringGrain > 0 && mt.ringGrain > 0) {
            wanted.order = [flt(r4(goldenStagger(mf.ringGrain))),
                            flt(r4(goldenStagger(mt.ringGrain)))];
          }
          // HOW FAR A TOOTH STANDS OUT OF ITS PITCH CIRCLE, read off how much finer the work's own
          // measured ring repeat is than the cut it was given: a work whose measurement outruns its
          // cut carries the relief the teeth stand in. The handle's own range answers anything past
          // it.
          if (mf.ringMerge > 0 && mt.ringMerge > 0) {
            wanted.tooth = [flt(r4(clamp01(mf.ringMerge - 1))), flt(r4(clamp01(mt.ringMerge - 1)))];
          }
        } else if (instr === "boxfold") {
          // WHICH WAY THE SOLID TURNS, off the one recorded banding axis, so the crease crosses the
          // works' own structure instead of being laid across it.
          var bx = fromP.ends.banding;
          if (bx !== undefined && bx !== null) wanted.axis = num(bx[2]) ? 1 : 0;
          // HOW MANY FINGERS STAND ALONG THE CREASE: the departing work's own measured repeat
          // across it, its frame side over the grid period. The collection's own count field is
          // stripped before a record reaches the engine; the period it is derived from is not.
          if (mf.gridCount > 0) {
            wanted.fingers = Math.round(Math.min(HANDLE_SPECS.boxfold.fingers[1],
                                                 Math.max(HANDLE_SPECS.boxfold.fingers[0],
                                                          mf.gridCount)));
          }
          // HOW DEEP THE JOINT BITES, read from the finger count's own published range onto this
          // handle's and turned over: many fingers bite shallow, few bite deep, so the joint's own
          // travel holds whatever the count. Two published spans and no third number.
          if (wanted.fingers !== undefined) {
            var lo = num(HANDLE_SPECS.boxfold.lead[0]), hi = num(HANDLE_SPECS.boxfold.lead[1]);
            wanted.lead = flt(r4(lo + hi
              - betweenSpans("boxfold", "fingers", "lead", num(wanted.fingers))));
          }
          // HOW DEEP THE PERSPECTIVE IS, off each work's own corridor reading — the identical field
          // and the identical sense the tunnel, parquet, planet and tilt branches already read this
          // reading with, all of them arrays that travel from the departing work's own depth to the
          // arriving one's. 2026-08-19 AUDIT FIX (class A: the arriving work was never asked): this
          // branch alone left the box's own depth pinned to `mf.tunnel`, with no rationale distinct
          // from those siblings for holding it still; it now travels the same road they do.
          if (mf.tunnel > 0 || mt.tunnel > 0) {
            wanted.depth = [flt(r4(clamp01(mf.tunnel))), flt(r4(clamp01(mt.tunnel)))];
          }
          // HOW FAR THE EYE RIDES UP THROUGH THE QUARTER, off the departing work's own measured
          // horizon: the ride starts from where that work already stands. A work whose horizon was
          // never measured leaves the handle at the module's own rest.
          if (mf.horizonY !== null) wanted.dip = flt(r4(clamp01(mf.horizonY)));
          // THE CREASE'S OWN LINE, AND THIS IS THE ONE PLACE THAT CHANGED. The comment that stood
          // here said the position did not travel and named this line as the one place that would
          // change the day it did. It travels: the record now carries
          // `structure.regions.line.{x,y}.at` and `.explains`, so `seam` takes the departing work's
          // own measured place and `seamScore` the measured reading of how cleanly that place
          // divides the picture, in place of the written zero that used to send the crease back to
          // the box's own edge and say why.
          //
          // WHICH AXIS THE CREASE LIES ALONG, and it is the easy thing to get backwards. `wanted.axis`
          // two screens up is the engine's `flat`, and the instrument reads it as `flat = axis >= 0.5`
          // (pass-inst-boxfold.js). `lab/effects/box.js` writes the same expression as `vertical` and
          // calls `seamOf(src, !vertical)`; inside `seamOf`, `acrossX` false walks the frame's ROWS,
          // so a crease at or above a half is measured along Y and one below it along X. Where the
          // branch wrote no axis at all the instrument's own default of nought stands, which is below
          // a half, so the X reading is the one that answers — the same fallback, read the same way.
          //
          // THE FLOOR IS NOT APPLIED HERE. `explains` is handed as the record measured it and the
          // instrument's own `SEAM_FLOOR` decides what to do with it, which is where that gate has
          // always lived: a floor applied on this side would be this file deciding a question the
          // module publishes an answer to.
          //
          // AND A WORK CARRYING NO LINE LEAVES BOTH HANDLES ALONE, so the crease stands at the box's
          // own edge exactly as it did before the record carried a line — the module's own default,
          // reached by saying nothing rather than by writing a zero.
          var seamFlat = num(wanted.axis === undefined ? 0 : wanted.axis) >= 0.5;
          var seamAt = seamFlat ? mf.regionLineYAt : mf.regionLineXAt;
          var seamHow = seamFlat ? mf.regionLineYExplains : mf.regionLineXExplains;
          if (seamAt === seamAt && seamHow === seamHow) {
            wanted.seam = flt(r4(clamp01(seamAt)));
            wanted.seamScore = flt(r4(clamp01(seamHow)));
          }
        } else if (instr === "unfold") {
          // THE SHEET OPENS INTO THE WORK'S OWN PARQUET. Every handle here reads the departing
          // work's own device — the step it was cut at and the angle of that step — because the
          // whole point of this register is that the passage reveals how the work was made, and a
          // parquet laid at some other step would be revealing something else.
          //
          // TWO FACES OR FOUR, off the work's own measured region count: a work that falls into two
          // regions opens as two, one that falls into more opens as four.
          // THE WORK WHOSE MAKING IS REVEALED is the one that reads it most clearly, which is the
          // very work the ask above weighed. Every handle below reads that one work, so the parquet
          // a person sees is one work's own and not a blend of two.
          var made = mf.deviceConfidence >= mt.deviceConfidence ? mf : mt;
          if (made.regionCount > 0) wanted.panels = made.regionCount > 2 ? 1 : 0;
          // THE STAGGER is charter shelf 13's golden-angle instrument on the sheet's own time axis,
          // taken on that same region count, so no two panels of the cascade come round together.
          if (made.regionCount > 0) {
            wanted.stagger = flt(r4(Math.min(num(HANDLE_SPECS.unfold.stagger[1]),
                                             goldenStagger(made.regionCount)
                                             * num(HANDLE_SPECS.unfold.stagger[1]))));
          }
          // THE PLANE'S OWN STEP AND THE ANGLE IT WAS CUT AT. The step is said as a share of the
          // work's own frame side, which is the unit the handle is published in; where no device
          // was derived the grid's own period and angle answer, which is the same reading taken a
          // level out.
          var stepPx = made.deviceStepPx > 0 ? made.deviceStepPx : made.gridPeriodPx;
          // The angle follows whether a DIRECTION was recovered, not whether a step was — the same
          // repair `latticeAngleDeg` and `gcAngle` take, and for the same reason: a ring-cut or a
          // tile-cut work has no direction to record, so the device's own angle reads its zero for
          // every such work in any collection, by the measurement's own definition.
          var angle = made.deviceAngleDeg || made.gridAngleDeg;
          if (stepPx > 0 && made.frameSide > 0) {
            wanted.parquetPeriod = flt(r4(clamp01(stepPx / made.frameSide)));
          }
          // IN THE HANDLE'S OWN UNIT, WHICH IS DEGREES (2026-08-24). `fractional(|angle| / 90)` wrote
          // a number under 1 into a handle published over [0, 180] in degrees, so the floor was the
          // only part of the range the plane ever turned in; and being FRACTIONAL it sent an exact
          // quarter turn to the same value as no turn at all, which is where the four striped works
          // of the collection landed. A lattice angle is a LINE direction, defined up to half a turn,
          // so the honest fold is the work's own angle modulo 180 — the same fold this file already
          // writes for `mixTurn`, `regionTurn` and the parquet's own `lattice`, and it is onto the
          // handle's whole published range with 0 and 90 distinct.
          wanted.parquetTurn = flt(r4(Math.abs(angle) % 180.0));
          // THE PLANE IS LAID AWAY AT THE SAME MEASURED ANGLE, which is what puts the parquet in
          // perspective rather than flat to the eye. THIS handle is published as a SHARE over [0, 1]
          // rather than in degrees, so the same fold is said as a position on the half turn it is
          // defined over: monotone in the angle, onto the handle's own range, and again with a
          // quarter turn standing where a quarter turn belongs instead of back at nothing.
          wanted.tilt = flt(r4(clamp01((Math.abs(angle) % 180.0) / 180.0)));
          // HOW DEEP A ROOM THE SHEET OPENS INTO, and it is the one handle here that reads BOTH
          // works. The five above read one work by design — the making being revealed is one work's
          // — and that is why this branch, which has stood since the unfold landed, still played
          // nearly the same parquet on every pair: the collection's own device readings cluster, so
          // one work's step and angle land on the same few values. The room the sheet opens into is
          // not part of the making being revealed; it is the passage's own depth, and both works
          // stand in it. So it travels, at each work's own corridor reading — the same measurement
          // the box's perspective and the mirror floor's room already take.
          if (mf.tunnel > 0 && mt.tunnel > 0) {
            wanted.depth = [flt(r4(clamp01(mf.tunnel))), flt(r4(clamp01(mt.tunnel)))];
          }
        } else if (instr === "matter") {
          // HOW COARSE THE MATERIAL IS. The instrument publishes its coarse grain in cells across
          // the frame's height, and the work's own measured spectral period says how many cells
          // that work is made of. What no file in this tree records is how many cells one step of
          // the handle is worth — HANDLE_SOURCE has called this handle uncalibrated since it was
          // written — so what travels is the RATIO of the two works' readings, positioned about the
          // handle's own default across OCTAVES_PER_SPAN doublings.
          if (mf.grainCells > 0 && mt.grainCells > 0) {
            wanted.grain = acrossTheSpan("matter", "grain", mf.grainCells, mt.grainCells);
          }
          // HOW FAR THE PICTURE IS DRAGGED, read off the share of the frame each work's own
          // measured open ground holds: a work with room to move is dragged further. The reading
          // is already a share of the frame and the handle is already a share of its own range, so
          // no scale stands between them.
          if (mf.voidShare > 0 || mt.voidShare > 0) {
            wanted.loosen = [flt(r4(clamp01(mf.voidShare))), flt(r4(clamp01(mt.voidShare)))];
          }
          // HOW WIDE THE LOOSENED BAND IS, read off the share of the frame each work's own
          // dominant object holds: the material gathers over as much of the frame as the figure
          // that is arriving in it. A share against a share again, with nothing between them.
          if (mf.figureShare > 0 || mt.figureShare > 0) {
            wanted.gather = [flt(r4(clamp01(mf.figureShare))), flt(r4(clamp01(mt.figureShare)))];
          }
          // WHERE THE MATERIAL HAS DRIFTED TO — charter shelf 13's third rubato instrument, the
          // incommensurate period, on the material's own time axis. The two works' measured
          // spectral periods stand in a ratio that is almost never a whole number, and its
          // fractional part is a deviation that never comes back into step.
          if (mf.spectralPeriodPx > 0 && mt.spectralPeriodPx > 0) {
            wanted.drift = flt(r4(fractional(mf.spectralPeriodPx / mt.spectralPeriodPx)));
          }
        } else if (instr === "planet") {
          // THE FIVE HANDLES THE WORLD IS PLACED BY. Without this branch every one of them stands
          // at the instrument's own rest — `curl` at 0.82, which is his own taste-approved state of
          // 2026-08-08 11:39 — and not one measurement of either work reaches the picture. Each
          // reading below is a share already, and every handle here is a share of its own range, so
          // no scale stands between the measurement and the handle.
          //
          // HOW FAR THE STRIP IS BENT WHEN THE WORLD STANDS OPEN, off each work's own reading as a
          // little world: a picture that already turns about a centre closes the whole way and one
          // that barely does is left a bowed band. It travels from the departing work's reading to
          // the arriving one's, so the world the visitor leaves is not the world they arrive in.
          if (mf.planet > 0 || mt.planet > 0) {
            wanted.curl = [flt(r4(clamp01(mf.planet))), flt(r4(clamp01(mt.planet)))];
          }
          // WHICH OF THE TWO WORLDS — a sphere, or the same one turned inside out — off each work's
          // own corridor reading. The same measurement the folding instrument's perspective is
          // placed by, read here as the world's own inversion.
          if (mf.tunnel > 0 || mt.tunnel > 0) {
            wanted.depth = [flt(r4(clamp01(mf.tunnel))), flt(r4(clamp01(mt.tunnel)))];
          }
          // WHERE THE HORIZON STANDS — how much sky is pulled toward the centre — off each work's
          // own measured horizon. A work with no measured horizon has nothing to say here and the
          // other work's reading stands alone rather than a number being invented for it.
          if (mf.horizonY !== null || mt.horizonY !== null) {
            var hf = mf.horizonY === null ? mt.horizonY : mf.horizonY;
            var ht = mt.horizonY === null ? mf.horizonY : mt.horizonY;
            wanted.dip = [flt(r4(clamp01(hf))), flt(r4(clamp01(ht)))];
          }
          // HOW FAR THE WORLD IS TURNED, off how strongly each work reads as radial — the same
          // measurement, and the same sense, the meshing instrument's own turn is driven by.
          if (mf.radialScore > 0 || mt.radialScore > 0) {
            wanted.turn = [flt(r4(clamp01(mf.radialScore))), flt(r4(clamp01(mt.radialScore)))];
          }
          // HOW MANY ROWS ARE USED AND HOW HARD THE HORIZON IS PULLED, off the share of the frame
          // each work's own measured dominant object holds — the same reading, in the same unit,
          // the material instrument's gather is driven by.
          if (mf.figureShare > 0 || mt.figureShare > 0) {
            wanted.gather = [flt(r4(clamp01(mf.figureShare))), flt(r4(clamp01(mt.figureShare)))];
          }
        } else if (instr === "tunnel") {
          // THE CORRIDOR'S FIVE MEASURED HANDLES. The lane asked for no fill branch, and without one
          // the corridor stands at the module's own ten spokes, its own rib spacing and its own
          // shear for every pair alike.
          //
          // HOW CLOSE THE RIBS STAND ALONG THE CORRIDOR, at each work's own measured ring repeat
          // where it was cut as rings, positioned by the ratio of the two rather than by an equality
          // — a ring count is a count of rings across a frame and the handle is a share of its own
          // range, and no file in this tree records how many ribs one step of the handle is worth.
          var ribsFrom = mf.deviceKind === "rings" ? mf.deviceCount : 0;
          var ribsTo = mt.deviceKind === "rings" ? mt.deviceCount : 0;
          if (ribsFrom > 0 && ribsTo > 0) {
            wanted.ribs = acrossTheSpan("tunnel", "ribs", ribsFrom, ribsTo);
          }
          // HOW MANY SPOKES RUN DOWN IT, at the work's own measured turn. Where the collection
          // records no rotational order the handle is not driven and the module's own ten stand.
          if (mf.rotationalN > 0 || mt.rotationalN > 0) {
            wanted.spokes = Math.round(Math.max(mf.rotationalN, mt.rotationalN));
          }
          // HOW HARD THE SPIRAL SHEARS, at each work's own measured twirl — the same reading the
          // glass winds by and the fold leans by.
          if (mf.twirl > 0 || mt.twirl > 0) {
            wanted.twist = [flt(r4(clamp01(mf.twirl))), flt(r4(clamp01(mt.twirl)))];
          }
          // HOW FAR THE EYE TRAVELS IN, at each work's own corridor reading — the very measurement
          // this handle's register row already cites.
          if (mf.tunnel > 0 || mt.tunnel > 0) {
            wanted.depth = [flt(r4(clamp01(mf.tunnel))), flt(r4(clamp01(mt.tunnel)))];
          }
          // WHERE THE CORRIDOR FALLS AWAY TO: the midpoint of the two measured radial centres.
          centreOfThePair(wanted);
        } else if (instr === "kaleidoscope") {
          // THE FOLD'S FOUR MEASURED HANDLES. The lane asked for no fill branch, but without one
          // the fold stands at the module's own eight wedges, one ring and its own lean for every
          // pair alike, and its own report names what each handle reads.
          //
          // HOW MANY WEDGES THE FOLD TILES INTO, at the work's own measured rotational order. THE
          // COLLECTION CARRIES THAT ORDER FOR 3 WORKS IN 121, and where it carries none the handle
          // is simply not driven: the module's own eight stand, which is the vista preset his taste
          // approved on 2026-08-08. That is a gap in the measurement named as a gap, not a number
          // invented to cover it.
          //
          // THE ORDER IS HANDED STRAIGHT AND THAT STAYS RIGHT (checked 2026-08-24 against the
          // clamp-to-an-endpoint class repaired elsewhere in this branch). A wedge count and a
          // rotational order are the SAME count in the same unit — three wedges is threefold
          // symmetry — so the handle's own span holds the reading rather than standing in a
          // different scale from it, and a work turning oftener than the glass reaches is honestly
          // held at the glass's own reach. WHAT THIS HANDLE DEPENDS ON, named rather than argued:
          // it reads `structure.rotational.n` and it moves exactly as far as that field moves. No
          // sentence here can prove that field varies and none should try — how far it varies is a
          // property of the record builder's own reading and belongs in that tree, with an owner.
          // What is provable here is that no scale invented in this file can put variety into a
          // reading that has none.
          if (mf.rotationalN > 0 || mt.rotationalN > 0) {
            wanted.wedges = Math.round(Math.max(mf.rotationalN, mt.rotationalN));
          }
          // HOW FAR THE FOLD LEANS, at each work's own measured twirl — the same reading the glass
          // winds by and the corridor shears by, travelling from one work's to the other's.
          if (mf.twirl > 0 || mt.twirl > 0) {
            wanted.twist = [flt(r4(clamp01(mf.twirl))), flt(r4(clamp01(mt.twirl)))];
          }
          // HOW OFTEN THE FOLD REPEATS OUTWARD, at the work's own device count where that device is
          // rings. A work cut some other way lends nothing here and the module's own count stands.
          var ringsFrom = mf.deviceKind === "rings" ? mf.deviceCount : 0;
          var ringsTo = mt.deviceKind === "rings" ? mt.deviceCount : 0;
          // The handle's own manifest asks for that count «read onto this handle's own span», and
          // until tonight it was clamped into it instead: the span is 1 to 2 (his own «rings>2
          // washes to milk») and the ring counts on disk run from 5 to 23, so every pair carrying a
          // ring-cut work landed on exactly 2 — one repeat for the whole collection. Placed about
          // the module's own rest by the same ratio law, the repeat now answers to how coarse the
          // work's own rings actually are.
          if (ringsFrom > 0 || ringsTo > 0) {
            wanted.rings = Math.round(alongTheSpan(
              "kaleidoscope", "rings",
              Math.max(ringsFrom, ringsTo) / num(HANDLE_SPECS.kaleidoscope.rings[2])));
          }
          // HOW WIDE THE SAMPLE STANDS, at the work's own cutting step over its own frame side —
          // placed on the handle's own span by the RATIO of the two works' readings rather than
          // handed straight, for the reason the water's own crest and refraction state a few screens
          // down and measured here too: a step is a small share of a frame side (the collection's
          // run under a fifth of one) and this handle stands over 0.12 to 0.5, so the reading handed
          // straight fell under the floor and every pair alike came out at exactly 0.12.
          if (mf.deviceStepPx > 0 && mf.frameSide > 0 && mt.deviceStepPx > 0 && mt.frameSide > 0) {
            wanted.reach = acrossTheSpan("kaleidoscope", "reach",
                                         mf.deviceStepPx / mf.frameSide,
                                         mt.deviceStepPx / mt.frameSide);
          }
          // WHERE THE FOLD TURNS: the midpoint of the two works' own measured radial centres.
          centreOfThePair(wanted);
        } else if (instr === "parquet") {
          // THE MIRROR FLOOR'S THREE MEASURED HANDLES. The lane asked for no fill branch, but
          // without one `tiles` and `lattice` rest at the module's own floor for every pair alike,
          // which is the sameness the whole port exists to close, and its own report names exactly
          // what each reads.
          //
          // HOW MANY TILES ACROSS THE FLOOR, at the count of the work's own measured lattice —
          // the frame side over the grid's period. THE GRID IS READ FIRST HERE AND THE DEVICE
          // SECOND, the other way round from the unfold's parquet, and the reason is measured on
          // the two measurements' own resolutions: a device step is quantised to the device's own
          // repeat, so its range is coarser than the grid period's by construction and reading it
          // first puts more works on one value whatever the works are.
          var tilesFrom = mf.gridCount > 0 ? mf.gridCount
            : (mf.deviceStepPx > 0 && mf.frameSide > 0 ? mf.frameSide / mf.deviceStepPx : 0);
          var tilesTo = mt.gridCount > 0 ? mt.gridCount
            : (mt.deviceStepPx > 0 && mt.frameSide > 0 ? mt.frameSide / mt.deviceStepPx : 0);
          if (tilesFrom > 0 || tilesTo > 0) {
            wanted.tiles = [flt(r4(tilesFrom || tilesTo)), flt(r4(tilesTo || tilesFrom))];
          }
          // WHICH WAY THE FLOOR'S OWN LATTICE RUNS, at the angle the work's step was cut at — the
          // grid's angle first for the same measured reason, the device's where there is none.
          var latFrom = mf.gridAngleDeg || mf.deviceAngleDeg;
          var latTo = mt.gridAngleDeg || mt.deviceAngleDeg;
          if (latFrom || latTo) {
            wanted.lattice = [flt(r4(Math.abs(latFrom) % 180.0)), flt(r4(Math.abs(latTo) % 180.0))];
          }
          // HOW DEEP A ROOM THE PASSAGE STANDS IN, at each work's own corridor reading — the same
          // measurement the folding instrument's perspective is placed by.
          if (mf.tunnel > 0 || mt.tunnel > 0) {
            wanted.depth = [flt(r4(clamp01(mf.tunnel))), flt(r4(clamp01(mt.tunnel)))];
          }
        } else if (instr === "lens") {
          // THE FOUR GLASS HANDLES. Without this branch all four stand at the module's own rests —
          // the kaleidoscope, six wedges, full twist, a power of two — for every pair alike.
          //
          // WHICH OF THE THREE GLASSES THE PAIR IS SEEN THROUGH, and it is a RANKING between two
          // readings rather than a pair of floors: the mirrored wedges where the pair's own turn
          // reads loudest, the wound glass where its twirl does, and the plain magnification only
          // where neither reading stands at all — which is a fact about the pair and not a bar it
          // failed to clear.
          var rot = Math.max(mf.rotationalScore, mt.rotationalScore);
          var wind = Math.max(mf.twirl, mt.twirl);
          wanted.fold = (rot <= 0 && wind <= 0) ? 2 : (rot >= wind ? 0 : 1);
          // HOW OFTEN THE FOLD REPEATS, at the work's own measured rotational order, so the disc
          // folds as many times as the work itself turns. HANDED STRAIGHT, and the fold's own branch
          // above says why that is right here and wrong for its neighbours: a wedge count and a
          // rotational order are one count in one unit, so the span holds the reading instead of
          // standing in another scale from it. This handle reads `structure.rotational.n` and moves
          // exactly as far as that field moves, which is a record-side dependency and named as one.
          if (mf.rotationalN > 0 || mt.rotationalN > 0) {
            wanted.wedges = Math.round(Math.max(mf.rotationalN, mt.rotationalN));
          }
          // HOW FAR THE GLASS WINDS, at the work's own measured twirl, travelling from the
          // departing work's reading to the arriving one's.
          if (mf.twirl > 0 || mt.twirl > 0) {
            wanted.twist = [flt(r4(clamp01(mf.twirl))), flt(r4(clamp01(mt.twirl)))];
          }
          // HOW HARD THE GLASS MAGNIFIES, at the ratio of the two works' own cutting steps — which
          // is what brings a piece of the departing work to the size of the arriving work's own.
          // The ratio is placed ON the handle's span rather than handed to it: the span runs 1 to 4
          // about a rest of 2, so every ordered pair whose arriving work is cut finer than its
          // departing one — half of every pair in the world, by construction — asked for a number
          // under 1 and was clamped to exactly 1, the floor, whichever two photographs met. Placed
          // about the module's own rest a doubling at a time, a ratio of 1 lands on the rest and the
          // whole span answers to how far apart the two works' steps actually stand.
          if (mf.deviceStepPx > 0 && mt.deviceStepPx > 0) {
            wanted.power = flt(r4(alongTheSpan("lens", "power",
                                               mt.deviceStepPx / mf.deviceStepPx)));
          }
          // WHERE THE GLASS RESTS: the midpoint of the two works' own measured radial centres, the
          // same point the meshing instrument's own centre reads.
          centreOfThePair(wanted);
        } else if (instr === "liquid") {
          // THE WATER'S THREE HANDLES. Without this branch all three rest at the module's own
          // water — correct water, but the SAME water for every pair, which is the sameness the
          // whole port exists to close.
          //
          // HOW DEEP THE SWELL RUNS, off how much of each work reads as grain rather than as line.
          // A work that IS texture takes the deep swell; one of straight architecture takes the
          // shallow one. Both readings are shares already and the handle is a share of its own
          // range, so it is a share against a share with nothing between them.
          if (mf.textureScore > 0 || mt.textureScore > 0) {
            wanted.swell = [flt(r4(clamp01(mf.textureScore))), flt(r4(clamp01(mt.textureScore)))];
          }
          // HOW CLOSE THE CRESTS STAND, and HOW FAR THE WATER BENDS THE LIGHT. Both are read as a
          // POSITION on the handle's own range and never as an equality, and the reason is measured:
          // the module's three waves stand about one and a quarter frame sides long, while a work's
          // strongest spectral band is an order finer, so equality would crowd the crests elevenfold
          // past the handle's own reach. `acrossTheSpan` positions the two works about the handle's
          // own default by the RATIO of their readings, which is the same road the material
          // instrument's grain already travels and invents no scale of its own.
          if (mf.spectralPeriodPx > 0 && mt.spectralPeriodPx > 0
              && mf.frameSide > 0 && mt.frameSide > 0) {
            wanted.crest = acrossTheSpan("liquid", "crest", mf.spectralPeriodPx / mf.frameSide,
                                         mt.spectralPeriodPx / mt.frameSide);
          }
          if (mf.detailPx > 0 && mt.detailPx > 0 && mf.frameSide > 0 && mt.frameSide > 0) {
            wanted.refract = acrossTheSpan("liquid", "refract", mf.detailPx / mf.frameSide,
                                           mt.detailPx / mt.frameSide);
          }
        } else if (instr === "overlay") {
          // THE TWO HANDLES THE PLAN ITSELF NAMES. `blend` says which of his six approved rules the
          // two works meet under and `arrival` says whether charter shelf 7's interfered arrival is
          // the one this crossing makes. Neither reads a photograph, and the note that stood here
          // took that to mean neither could be answered — so both stayed at the instrument's own
          // rest, `arrival` at 0 on every cast, and the interfered arrival never happened at all.
          // Reading nothing of either work is not the same as having nothing to say: a plan's word
          // is still a word, and this plan has already said both.
          //
          // THE ARRIVAL IS THE ONE THE PLAN ALREADY DECIDED. `arrival.mode` is settled long before
          // this fill runs, by `arrivalOf` ranking the charter's five arrivals against the pair's
          // own records (naряд S-06). INTERFERED is the shelf-7 arrival this module's own shader
          // already carries, so the handle plays it exactly where the plan's own ranking named it
          // — never on CONDENSED, which used to stand in for it here and is its own separate
          // arrival with its own separate phrase.
          wanted.arrival = arrival.mode === "INTERFERED" ? 1 : 0;
          // AND THE RULE THE TWO WORKS MEET UNDER IS ROLLED ON THE PAIR'S OWN DIE, over the six the
          // instrument publishes. The list is his and the choice is the score's, which is what the
          // register row says; the die is the same one every other choice in this file is made on,
          // so a pinned seed reproduces it and two edges of one walk choose differently.
          wanted.blend = dieAmong(num(row[4]), key + "|overlay-blend",
                                  num(HANDLE_SPECS.overlay.blend[1]) + 1);
          //
          // HOW FAR THE COMPOSITE REACHES AND HOW MUCH OF THE FRAME IT STANDS ON, both off the one
          // reading that decides whether this crossing is worth watching: the two works' own colour
          // distance, taken between their measured colourfulness. Two palettes standing apart
          // make a third colour world; two standing close make one work slightly veiled, and the
          // composite reaches exactly as far as there is a third colour to reach for.
          //
          // AND THE READING IS A POSITION ABOVE THE LEVEL THE COMPOSITE READS FROM, not the whole
          // answer on its own (2026-08-24, the same repair the camera lane made this morning and the
          // colour voices took above). Handed straight, the apartness landed between 0.012 and 0.043
          // on every captured crossing against a handle that rests at 1 — a third picture reaching a
          // fortieth of the way, which is a voice shelf 17 counts and nobody can see. The level below
          // which there is nothing to see is the INSTRUMENT'S OWN and it publishes both halves of it:
          // `formsBeginAt` says where the composite's forms begin, and `edgeOfTheRegion` is the
          // softness of the region's own edge, under which the region never stands at all
          // (pass-inst-overlay.js's own `reach = presence · (1 + 2·EDGE) − EDGE`). Both stand at the
          // head of this closure beside `SIZE_MIN`, where the paragraph over them names the
          // instrument that authors each and says why these two are kept where a span is read.
          //
          // NOTHING IS DECLINED AND NOTHING IS FLATTENED. `voiceLift` is the same straight line the
          // camera flies on: the level takes the bottom of the span and the pair's own apartness
          // spends what is left, so the composite still RANKS by how far the two palettes stand
          // apart, reaches the handle's own ceiling exactly where they stand furthest, and never
          // passes it. The guard is on whether either work carries a colour reading at all — where
          // neither does, the instrument's own rest stands, which is the honest answer to «where did
          // this number come from». Two works whose palettes read exactly alike are no longer sent
          // past the guard to the manifest's full reach while a pair a hair apart got a fortieth of
          // it: the line is continuous through nought now.
          var apartHere = Math.min(1, Math.abs(mf.colourfulness - mt.colourfulness));
          if (mf.colourfulness > 0 || mt.colourfulness > 0) {
            var expCap = num(HANDLE_SPECS.overlay.exposure[1]);
            var presCap = num(HANDLE_SPECS.overlay.presence[1]);
            // THE TWO LEVELS ARE THE INSTRUMENT'S OWN, read off `MANIFESTS.overlay` at the head of
            // this closure now that the record's manifest projection carries `applied`. The
            // paragraph there says why the read went through a local copy for a night and does not
            // any more.
            var expFloor = voiceFloor(OVERLAY_FORMS_BEGIN_AT, expCap);
            var presFloor = voiceFloor(OVERLAY_REGION_EDGE, presCap);
            wanted.exposure = flt(r4(clamp01(expCap * voiceReach(expFloor, apartHere))));
            wanted.presence = flt(r4(clamp01(presCap * voiceReach(presFloor, apartHere))));
          }
          // CHARTER SHELF 10, IN THE TWO RHYTHMS THEMSELVES. The third picture is the two works'
          // interference, so how large the arriving work stands against the departing one is the
          // RATIO of their own cutting steps, and how far it is turned is the ANGLE between their
          // two lattices. Near-matched rhythms at a small angle are what yield the slow large beats.
          if (mf.latticePx > 0 && mt.latticePx > 0) {
            wanted.scale = flt(r4(mt.latticePx / mf.latticePx));
            wanted.turn = flt(r4(Math.abs(mt.latticeAngleDeg - mf.latticeAngleDeg) % 180.0));
          }
          // WHERE THE MIX FIELD LEANS, along the DEPARTING work's own structure: the step that work
          // was cut at, said as a fraction of its own frame side, and the angle that step was cut
          // at. So the field deciding which places of the frame belong to which work leans along
          // the work the visitor is leaving rather than across it.
          if (mf.latticePx > 0 && mf.frameSide > 0) {
            wanted.mixPeriod = flt(r4(clamp01(mf.latticePx / mf.frameSide)));
            wanted.mixTurn = flt(r4(Math.abs(mf.latticeAngleDeg) % 180.0));
          }
          // WHERE THE EXPOSURE'S REGION GROWS, along the ARRIVING work's own structure by the same
          // two readings — which is what makes the arrival that work's own rather than a shape laid
          // over it.
          if (mt.latticePx > 0 && mt.frameSide > 0) {
            wanted.regionPeriod = flt(r4(clamp01(mt.latticePx / mt.frameSide)));
            wanted.regionTurn = flt(r4(Math.abs(mt.latticeAngleDeg) % 180.0));
          }
        } else if (instr === "droste") {
          // THE SPIRAL'S FIVE. Without this branch the dive stood at the module's own four copies,
          // its own wind and its own speed for every pair alike: no branch means no track, no track
          // means `appliedValue` fills the handle from the manifest default, and a default is one
          // number for every pair there can ever be. Every row below is the sentence the handle
          // itself publishes.
          //
          // HOW MANY COPIES STAND INSIDE ONE FALL OF FORTY, off the two works' own measured ring
          // counts: a work of few rings dives in few large copies and one of many in many small
          // ones, which is the module's own sentence. The counts are positioned about the module's
          // own four by their RATIO rather than handed straight, and the reason is a statement about
          // two ranges: a ring count and a share-of-span handle are different scales, so a count
          // handed straight saturates for EVERY count above the span's own top — one value for all
          // of them, which is the sameness this branch exists to close. What no file records is how
          // many rings one copy is worth; what both records carry is which of the two works has more
          // of them.
          if (mf.ringGrain > 0 && mt.ringGrain > 0) {
            wanted.size = acrossTheSpan("droste", "size", mf.ringGrain, mt.ringGrain);
          }
          // HOW HARD THE PICTURE WINDS INTO ITS THROAT, at each work's own measured radial score —
          // the same reading and the same reasoning the mesh's own turn takes.
          if (mf.radialScore > 0 || mt.radialScore > 0) {
            wanted.turn = [flt(r4(clamp01(mf.radialScore))), flt(r4(clamp01(mt.radialScore)))];
          }
          // HOW FAST THE DIVE FALLS, read off the copy count against the instrument's own default
          // count, so one copy passes the eye in the same time whatever the pair. It is the road the
          // fabric's own speed already travels, on the same register row. 2026-08-19 AUDIT FIX
          // (class A: the arriving work was never asked). `wanted.size` above already travels from
          // the departing work's own ring count to the arriving work's; a speed placed by only its
          // first point held still while the count it answers to kept moving. Both ends of `size`
          // feed the same `betweenSpans` call the original single reading already used.
          if (wanted.size) {
            wanted.speed = [flt(r4(betweenSpans("droste", "size", "speed", num(wanted.size[0])))),
                            flt(r4(betweenSpans("droste", "size", "speed", num(wanted.size[1]))))];
          }
          // WHERE THE THROAT STANDS: the midpoint of the two works' own measured radial centres.
          centreOfThePair(wanted);
        } else if (instr === "hero") {
          // THE READY STORY'S SEVEN. Without this branch the whole story — how many mirrors the
          // window opens, how far out the arc travels, how hard it turns and where its courses
          // stand — was the module's own for every pair alike: no branch, no track, and the manifest
          // default is one number for every pair there can ever be.
          //
          // HOW MANY OF THE FOUR MIRRORS THE WINDOW OPENS, and HOW CONFIDENTLY that order reads.
          // Both are read on the ONE work whose turn reads most confidently, because they are one
          // measurement in two halves: an order and the confidence that order carries. Reading the
          // count off one work and its confidence off the other would make the window travel
          // between a count and a confidence that never belonged together. The count lands on the
          // module's own ladder of two, four, eight and sixteen wedges.
          var turned = mf.rotationalScore >= mt.rotationalScore ? mf : mt;
          if (turned.rotationalN > 0) {
            wanted.folds = Math.max(1, Math.min(4, Math.round(Math.log(turned.rotationalN)
                                                              / Math.LN2)));
            wanted.foldsScore = flt(r4(clamp01(turned.rotationalScore)));
          }
          // HOW FAR OUT ALONG THE STORY THE ARC TRAVELS, at the stronger of the two polar readings.
          // One story is told about one centre and it goes as far as the pair carries it, which is
          // the same sentence this instrument's own reading of a pair is written on.
          if (mf.planet > 0 || mt.planet > 0) {
            wanted.planet = flt(r4(clamp01(Math.max(mf.planet, mt.planet))));
          }
          // HOW FAR THE WINDOW TURNS AS IT OPENS, at each work's own measured radial score.
          if (mf.radialScore > 0 || mt.radialScore > 0) {
            wanted.turn = [flt(r4(clamp01(mf.radialScore))), flt(r4(clamp01(mt.radialScore)))];
          }
          // WHERE THE COURSES STAND, at each work's own ring step as a fraction of its own frame
          // side. A work cut some other way lends nothing here and the module's own courses stand.
          var courseFrom = (mf.deviceKind === "rings" && mf.frameSide > 0)
            ? mf.deviceStepPx / mf.frameSide : 0;
          var courseTo = (mt.deviceKind === "rings" && mt.frameSide > 0)
            ? mt.deviceStepPx / mt.frameSide : 0;
          if (courseFrom > 0 && courseTo > 0) {
            wanted.course = [flt(r4(courseFrom)), flt(r4(courseTo))];
          }
          // WHERE THE FOLDS TURN: the midpoint of the two works' own measured radial centres.
          centreOfThePair(wanted);
        } else if (instr === "livemirror") {
          // THE MIRROR'S THREE, AND THE ONE IT WILL NOT TAKE. Without this branch the fold stood at
          // the module's own both-folds-at-once, dead centre of the frame, on every pair alike — no
          // branch, no track, and the manifest default is one number for every pair there can ever
          // be.
          //
          // WHICH WAY THE PICTURE FOLDS ONTO ITSELF, off the one recorded banding axis. This
          // instrument's own manifest asks for the fold line to lie ALONG the works' own structure,
          // where the box asks for its crease to CROSS it — one measurement, two senses, which is
          // what the register row says in as many words — so this reads the same number the other
          // way about.
          var mx = fromP.ends.banding;
          if (mx !== undefined && mx !== null) wanted.axis = num(mx[2]) ? 0 : 1;
          // WHERE THE FOLD STANDS: the midpoint of the two works' own measured radial centres, which
          // is the line his standing verdict on this effect asks the fold to land on.
          centreOfThePair(wanted);
          // SHELF 7'S PROPAGATED ARRIVAL, WHERE IT REACHES PIXELS — «в зеркальных копиях дальняя
          // меняется первой», of the mirrored copies the far one changes first (наряд S-06). This
          // is the one instrument of the fleet that makes mirrored copies of a work, so it is the
          // one that can carry that sentence: at a spread above nothing a point standing in a
          // further copy exchanges before a point standing in the first one, and the whole frame
          // exchanges as one wherever the spread is nothing.
          //
          // THE SPREAD IS THE ARRIVING WORK'S OWN ROTATIONAL READING, which is the same number
          // `arrivalOf` ranked this arrival on: a work that plainly IS its own copies repeated
          // propagates the change through them over most of the crossing. So the reason this
          // arrival won and the depth of what it draws are one reading, not two.
          if (arrival.mode === "PROPAGATED" && mt.rotationalScore > 0) {
            wanted.propagate = flt(r4(Math.min(num(HANDLE_SPECS.livemirror.propagate[1]),
                                               clamp01(mt.rotationalScore))));
          }
          // THE MIRROR'S OWN LIFE IS NOT DRIVEN, AND THAT IS HIS VERDICT RATHER THAN A GAP. `drift`
          // publishes a measurement it would read — the fractional part of the two works' spectral
          // periods in ratio — and the instrument's own manifest answers it: the handle rests at
          // nothing because a wandering fold line does not land on the work's own structural line.
          // A reading may not overrule his verdict on the effect, so the reading is named here and
          // the handle stays where the instrument rests it.
        } else if (instr === "adrift") {
          // THE DRIFTING INSTRUMENT'S NINE, AND THEY NAME A WORK EACH. Every other branch of this
          // fill hands a pair of ends the passage travels between; this instrument holds two things
          // at once — one leaving the frame and one arriving in it — so where each stands, how much
          // emptiness each has and whether each carries a waterline are read on ITS OWN work and
          // handed as two numbers rather than as one journey.
          //
          // Without this branch the instrument would land and play the SAME crossing on every pair:
          // the two things would sit at the centre of the frame, cross three quarters of it and
          // hand over on the same front whichever two photographs met. That is the sameness his
          // word of 2026-08-18 15:13 names, and it is the reason a branch lands beside the record.
          //
          // WHERE EACH WORK'S THING STANDS, off the centre of its own measured object box. The
          // reading is already a share of the frame and the handle is published in shares of the
          // frame, so nothing stands between them.
          if (mf.figureShare > 0) {
            wanted.homeAx = flt(r4(clamp01(mf.figureCx)));
            wanted.homeAy = flt(r4(clamp01(mf.figureCy)));
          }
          if (mt.figureShare > 0) {
            wanted.homeBx = flt(r4(clamp01(mt.figureCx)));
            wanted.homeBy = flt(r4(clamp01(mt.figureCy)));
          }
          // HOW FAR EACH THING MAY TRAVEL BEFORE IT STANDS ON ARCHITECTURE INSTEAD OF ON EMPTINESS,
          // off the share of the frame each work's own measured open ground holds. The module takes
          // the smaller of the two, so a pair with one crowded work keeps both things near home.
          if (mf.voidShare > 0) wanted.voidShareA = flt(r4(clamp01(mf.voidShare)));
          if (mt.voidShare > 0) wanted.voidShareB = flt(r4(clamp01(mt.voidShare)));
          // HOW STRONGLY EACH WORK CARRIES A WATERLINE OF ITS OWN, which is how far the handover
          // front leans off the line the two things travel on. lab/step1-motifs.py:347-360 scores
          // this directly and lab/build-workrecords-v1.py:121 carries it beside the line as
          // `structure.horizon.seam`, so this reads the work's own measured strength rather than
          // only whether a seam was recognised.
          wanted.seamA = flt(r4(clamp01(mf.seamStrength)));
          wanted.seamB = flt(r4(clamp01(mt.seamStrength)));
          // HOW DEEPLY THE TWO GROUNDS INTERLOCK AT THE FRONT — a clean waterline at one end of the
          // handle and a band of fingers at the other. The front is where the two grounds MEET, so
          // the weaker of the two texture readings rules it: either work that reads as line rather
          // than as grain hands over on a line.
          if (mf.textureScore > 0 && mt.textureScore > 0) {
            wanted.horizon = flt(r4(clamp01(Math.min(mf.textureScore, mt.textureScore))));
          }
          // HOW COARSE THE GROUND'S OWN GRAIN IS, on the road the material instrument's grain
          // already travels: the two works' measured spectral periods in cells across the frame's
          // height, positioned about the handle's own default by their ratio, because no file in
          // this tree records how many cells one step of the handle is worth.
          if (mf.grainCells > 0 && mt.grainCells > 0) {
            wanted.grain = acrossTheSpan("adrift", "grain", mf.grainCells, mt.grainCells);
          }
        // ---- THE ARSENAL LANE, 2026-08-18 --------------------------------------------------
        // Six branches, one per instrument carried across today, and every one of them exists for
        // his shout of 15:13: НИКАКИХ СТАТИЧЕСКИХ ПЕРЕХОДОВ. An instrument that lands with a `cuts`
        // line and no branch here is cast for real pairs and plays ONE identical crossing on every
        // one of them, because `tracksFor` builds a track for each handle and `appliedValue` fills
        // an unasked track with the manifest default. Three instruments stood in exactly that state
        // this morning, and the claim needs no tally beside it: a handle with no branch takes the
        // manifest's own default, and a default is one number for every pair there can ever be. The
        // six branches below are what make each of these instruments read the pair in front of it.
        } else if (instr === "beat") {
          // THE TWO GRATINGS ARE THE TWO WORKS' OWN RHYTHMS. Each work's measured spectral period,
          // said as a share of its own frame side, is exactly the unit the two period handles are
          // published in — the instrument carries the span in frame heights on the handle itself,
          // so the reading is placed on it without a scale invented here. A record built before
          // that span travelled falls back to the ratio road the material instrument's grain takes.
          var beatSpan = ((MANIFESTS.beat.handles.periodA || {}).frameHeights) || null;
          function beatPlace(cells) {
            var share = cells > 0 ? 1 / cells : 0;      // cells across the frame -> frame heights
            if (!(share > 0)) return null;
            var lo = num(beatSpan[0]), hi = num(beatSpan[1]);
            return flt(r4(clamp01(hi > lo ? (share - lo) / (hi - lo) : 0)));
          }
          if (beatSpan && mf.grainCells > 0) wanted.periodA = beatPlace(mf.grainCells);
          if (beatSpan && mt.grainCells > 0) wanted.periodB = beatPlace(mt.grainCells);
          if (!beatSpan && mf.grainCells > 0 && mt.grainCells > 0) {
            var beatPair = acrossTheSpan("beat", "periodA", mf.grainCells, mt.grainCells);
            wanted.periodA = beatPair[0];
            wanted.periodB = beatPair[1];
          }
          // THE ANGLE THE TWO GRATINGS INTERFERE AT, which the module pinned at nine degrees and
          // this port publishes. The third picture IS the two works' gratings interfering, so the
          // angle between them is the pair's own fact: the difference of the two measured lattice
          // angles, folded back under a right angle because a lattice angle is a line direction and
          // two grating families never stand further apart than that. The handle's own range in
          // degrees is what the reading is held to, so nothing here needs a number of its own.
          if (mf.latticePx > 0 && mt.latticePx > 0) {
            var apart = Math.abs(mf.latticeAngleDeg - mt.latticeAngleDeg) % 180;
            if (apart > 90) apart = 180 - apart;
            wanted.beatTilt = flt(r4(Math.min(num(HANDLE_SPECS.beat.beatTilt[1]),
                                              Math.max(num(HANDLE_SPECS.beat.beatTilt[0]),
                                                       apart))));
          }
          // HOW MUCH OF THE CUT THE SLOW ENVELOPE OWNS, read off how near the two rhythms stand.
          // Two nearly equal periods make lobes worth handing the frame over in and the envelope
          // should own the cut; two far-apart periods make no envelope worth the name, and the raw
          // sum is the honester picture. It is the same reading the instrument's own `suits` takes.
          if (mf.grainCells > 0 && mt.grainCells > 0) {
            var nearBeat = Math.min(mf.grainCells, mt.grainCells)
                         / Math.max(mf.grainCells, mt.grainCells);
            wanted.contrast = flt(r4(clamp01(nearBeat)));
          }
        } else if (instr === "gates") {
          // HOW WIDE THE JAMB BITES, off each work's own measured gate. `motifs.gateGap` is the
          // collection's own measure — one minus the busy-ness of the middle band over the
          // busy-ness of the denser flank — so a work with a plain hole between two masses opens on
          // a wide jamb and one that barely reads a gate opens on a narrow one. 2026-08-19 AUDIT FIX
          // (class A, and the same fix repeats down this branch): every reading below named only
          // the DEPARTING work's own gate, with no rationale in this branch for holding the slot's
          // whole shape to that one work's opening rather than letting it travel to the arriving
          // work's own gate — unlike `unfold`'s or `hero`'s single-work reads, which say in as many
          // words why one work alone is read. Both works carry every one of these fields.
          var gatesClamp = function (spec, v) { return Math.min(num(spec[1]), Math.max(num(spec[0]), v)); };
          if (mf.gateGap > 0 || mt.gateGap > 0) {
            var jambSpec = HANDLE_SPECS.gates.jamb;
            wanted.jamb = [flt(r4(gatesClamp(jambSpec, mf.gateGap))),
                          flt(r4(gatesClamp(jambSpec, mt.gateGap)))];
          }
          // HOW MANY TEETH THE JAMB BREAKS INTO, off each work's own repeat across the slot: its
          // frame side over the grid period, which is the same count the folding instrument's
          // fingers are read from. A whole count, because a tooth is one; `parquet.tiles` is the
          // same file's own precedent for a count that travels as a two-point handle.
          if (mf.gridCount > 0 || mt.gridCount > 0) {
            var teethSpec = HANDLE_SPECS.gates.teeth;
            wanted.teeth = [Math.round(gatesClamp(teethSpec, mf.gridCount)),
                           Math.round(gatesClamp(teethSpec, mt.gridCount))];
          }
          // WHICH WAY THE SLOT STANDS, off the gate's OWN measured axis, motifs.gateAxis — the
          // slot's own reading rather than the banding axis this branch stood in for it before
          // tonight's port gave the record a reading of the gate itself. `measuredParts` already
          // folds it to the 0/1 this handle expects. LEFT AT THE DEPARTING WORK'S OWN READING,
          // deliberately and not by the same gap as its neighbours above: an axis is a discrete
          // orientation, not a share of a range, and a slot swapping which way it opens partway
          // through the passage would read as a cut, not a shape — the lattice-orientation floor
          // HARD GUARDS names for exactly this reason.
          if (mf.gateAxis !== null && mf.gateAxis !== undefined) wanted.slotAxis = mf.gateAxis;
          // WHERE THE SLOT STANDS AND HOW WIDE IT IS, off each work's own measured place and
          // half-width — lab/step1-motifs.py's slot_on(), swept and grown per work rather than read
          // at the collection-wide band the module used to pin every work to.
          if (mf.gatePlace > 0 || mt.gatePlace > 0) {
            var placeSpec = HANDLE_SPECS.gates.slotPlace;
            wanted.slotPlace = [flt(r4(gatesClamp(placeSpec, mf.gatePlace))),
                               flt(r4(gatesClamp(placeSpec, mt.gatePlace)))];
          }
          if (mf.gateHalf > 0 || mt.gateHalf > 0) {
            var halfSpec = HANDLE_SPECS.gates.slotHalf;
            wanted.slotHalf = [flt(r4(gatesClamp(halfSpec, mf.gateHalf))),
                              flt(r4(gatesClamp(halfSpec, mt.gateHalf)))];
          }
          // HOW FAR THE LEAVES SWING AS THEY GO, off the share of the frame each work's own open
          // ground holds: a work with room around its masses lets them travel wide.
          if (mf.voidShare > 0 || mt.voidShare > 0) {
            wanted.swing = [flt(r4(clamp01(mf.voidShare))), flt(r4(clamp01(mt.voidShare)))];
          }
        } else if (instr === "grid-colour") {
          // SHELF 7'S INTERFERED ARRIVAL, THE SAME PLAN'S WORD THE OVERLAY CARRIES. `arrival.mode`
          // is settled before this fill runs, and this handle now reads the same condition the
          // overlay's own `wanted.arrival` reads a few hundred lines up — INTERFERED, never
          // CONDENSED. THE REPAIR (P3 of the 2026-08-27 review): this comment always named
          // INTERFERED as the word this handle carries, but the line beneath it tested CONDENSED,
          // so the two instruments this crossing can put on the same charter-shelf-7 arrival
          // disagreed about which arrival they were both being asked to show — the overlay lit on
          // INTERFERED while grid-colour lit on CONDENSED, on the same pair, in the same crossing.
          // Nothing about grid-colour's own six other handles asks for CONDENSED particularly, so
          // there was no reading of the instrument itself to preserve; the comment's own word wins.
          wanted.arrival = arrival.mode === "INTERFERED" ? 1 : 0;
          // THE CUT STANDS AT ONE WORK'S OWN STRUCTURE AND ARRIVES AT THE OTHER'S — the module's
          // whole claim, and the four handles below are what makes it true of a PAIR rather than of
          // one work twice. Every one reads the work's own device first and its measured grid where
          // no device was recovered, which is the order `measuredParts` already prefers them in.
          function gcStep(m) { return m.deviceStepPx > 0 ? m.deviceStepPx : m.gridPeriodPx; }
          // The ANGLE asks whether the device recovered a DIRECTION, not whether it recovered a
          // step: a ring-cut work carries a step and no direction at all, so its device angle reads
          // its own zero by the measurement's own definition, and taking that zero over the work's
          // own measured grid angle held both these handles still on every such work in any
          // collection. Same repair, same reason as `latticeAngleDeg` above.
          function gcAngle(m) { return m.deviceAngleDeg || m.gridAngleDeg; }
          var stepF = gcStep(mf), stepT = gcStep(mt);
          if (stepF > 0 && mf.frameSide > 0) {
            wanted.countFrom = Math.round(Math.min(num(HANDLE_SPECS["grid-colour"].countFrom[1]),
                                                   Math.max(num(HANDLE_SPECS["grid-colour"]
                                                                .countFrom[0]),
                                                            mf.frameSide / stepF)));
          }
          if (stepT > 0 && mt.frameSide > 0) {
            wanted.countTo = Math.round(Math.min(num(HANDLE_SPECS["grid-colour"].countTo[1]),
                                                 Math.max(num(HANDLE_SPECS["grid-colour"]
                                                              .countTo[0]),
                                                          mt.frameSide / stepT)));
          }
          // THE ANGLE EACH WORK'S OWN STEP WAS CUT AT, said as a position on a quarter turn the way
          // the sheet's own parquet turn is, so the cut leans the way the photograph leans.
          // IN DEGREES, WHICH IS THE UNIT BOTH HANDLES PUBLISH (2026-08-24). They stand over
          // [0, 180] and their own manifest says «degrees; 0 upright, 90 flat», and this line wrote
          // `fractional(|angle| / 90)` — at most 1 into a range 180 wide, so the cut leaned by under
          // one degree however the photograph leaned, and an exact quarter turn came out at the same
          // nothing a work standing upright does. Both are gone: the angle is folded modulo 180,
          // because a lattice angle is a line direction defined up to half a turn, and written in
          // the handle's own unit.
          wanted.angleFrom = flt(r4(Math.abs(gcAngle(mf)) % 180.0));
          wanted.angleTo = flt(r4(Math.abs(gcAngle(mt)) % 180.0));
          // WHICH KIND OF CUT EACH WORK FALLS INTO, off the work's own measured device: a work cut
          // as rings is cut into rings here, one cut as a grid into tiles, one banded into strips,
          // and a work whose device was never recovered is cut by its own colour instead, which is
          // the one kind that needs no lattice at all.
          function gcKind(m) {
            if (m.deviceKind === "rings") return 1;
            if (m.deviceKind === "grid" || m.deviceKind === "tiles") return 2;
            if (m.deviceStepPx > 0 || m.gridPeriodPx > 0) return 0;
            return 3;
          }
          wanted.kindA = gcKind(mf);
          wanted.kindB = gcKind(mt);
          // HOW FAR APART THE PIECES' OWN DEPARTURES STAND — charter shelf 13's golden-angle stagger
          // on the count the frame is actually cut into, so no two pieces of the cascade leave
          // together.
          if (stepF > 0 && mf.frameSide > 0) {
            wanted.stagger = flt(r4(Math.min(num(HANDLE_SPECS["grid-colour"].stagger[1]),
                                             goldenStagger(mf.frameSide / stepF)
                                             * num(HANDLE_SPECS["grid-colour"].stagger[1]))));
          }
          // HOW FAR AHEAD OF ITS OWN SHAPES THE ARRIVING PALETTE COMES — charter shelf 11's colour
          // herald. The reading is the distance between the two works on the collection's own
          // COLOURFULNESS ladder, which is what `palette.colourfulness` publishes: two works
          // whose colour worlds stand far apart give the herald something to announce.
          wanted.lead = flt(r4(clamp01(Math.abs(mf.colourfulness - mt.colourfulness))));
          // THE COLOUR AND LIGHT VOICES — six handles, one set, because this instrument carries
          // BOTH works inside itself and publishes one set of voice fields rather than a pair the
          // way strata-light does (its own manifest, pass-inst-grid-colour.js:919-937). Driven from
          // the DEPARTING work's own readings: this voice is written onto the frame as it stands at
          // the passage's opening, and at that opening the frame IS the departing work's palette —
          // saturation for the colour voice, contrast for the light voice, the same pairing
          // lab/step4-assembler.js:1966-2010 gives each voice at its own layer A.
          //
          // The period offsets (2 for colour, 3 for light) and the amplitude law (VOICE_SHARE times
          // the work's own measure) are the assembler's layer-A slot exactly (its `seeds[0]` and
          // `seeds[1]`, step4-assembler.js:1973-1976). The phase law is the same rule at this
          // instrument's own scale: the assembler stands its four voices (two works × two voices) a
          // quarter turn apart, `i / 4`; this instrument carries only the two voices of ONE work, so
          // the same `i / N` rule with N = 2 stands them half a turn apart instead of a quarter —
          // not a new number, the same index-over-count law read at this instrument's own voice
          // count.
          //
          // SUNG ONLY WHERE THIS CUE OWNS THE LEVEL THESE SIX HANDLES DECLARE (shelf 17's levels
          // law, `ownsLevelOf` above, reading the level off this instrument's own manifest). Where
          // another cue of this same passage owns that level instead, this cue only ACCOMPANIES it
          // there and every one of the six handles is left unset — the manifest's own rest of 0,
          // not a second silence invented here.
          if (ownsLevelOf(cue, "grid-colour", "colourAmp")) {
            var gcBase = [BEAT_DIAL * (2 + mf.sat), BEAT_DIAL * (3 + mf.contrast)];
            var gcPeriods = voiceSpread(gcBase);
            // The period is settled first, because the loudness is read against the crest the period
            // and the phase put the voice's own curve at — `voiceLoudness` above, the lab's own
            // second pass. A voice the work cannot sing loudly enough to be seen leaves all three of
            // its handles unwritten, resting at the manifest's own 0, which is the lab's own mute.
            var gcColourPeriod = r4(Math.min(num(HANDLE_SPECS["grid-colour"].colourPeriod[1]),
                                             Math.max(num(HANDLE_SPECS["grid-colour"]
                                                          .colourPeriod[0]),
                                                      gcPeriods[0].value)));
            var gcLightPeriod = r4(Math.min(num(HANDLE_SPECS["grid-colour"].lightPeriod[1]),
                                            Math.max(num(HANDLE_SPECS["grid-colour"]
                                                         .lightPeriod[0]),
                                                     gcPeriods[1].value)));
            // THE LEVEL EACH VOICE HAS TO CLEAR, and it is the pair's own: the weaker of the two
            // works' readings of the same measure the voice sings, per `voiceLoudness` above. A
            // colour voice is levelled against colour and a light voice against light, never across.
            sayVoice(wanted, "colour", "", mf.sat, gcColourPeriod, 0,
                     Math.min(mf.sat, mt.sat));
            sayVoice(wanted, "light", "", mf.contrast, gcLightPeriod, 0.5,
                     Math.min(mf.contrast, mt.contrast));
          }
          // WHAT STAYS IN THE LAB, AND IT IS NOW ONLY THE PROBE. The assembler follows its first
          // pass with an audibility loop (`voiceMove`, `VOICE_TARGET`) that RENDERS the voice's
          // layer off-screen and measures how far it actually moved a real frame's pixels. The
          // composer derives a crossing at the instant a visit casts it and can render nothing, so
          // the RENDERING is not ported — but the loop's own decision is, and `sayVoice` above is
          // where it lives: the peak of `amp · sin(2π(u/period + phase)) · 4u(1−u)` is closed-form
          // in the period and the phase this branch has just written, so the voice's own level is
          // known without a probe frame. A voice that cannot clear the lab's threshold at the
          // loudest its own measure allows is left unwritten here, exactly as the lab's own mute
          // leaves it — its three handles rest at the manifest's own 0.
        } else if (instr === "strata-light") {
          // THE GRID EACH STRATUM IS CUT ON, off each work's own measured grain: a work made of
          // coarse masses parts into few large areas and a fine-grained one into many small ones.
          // It is read PER WORK rather than as a journey, because the two works part at the same
          // instant on their own sides of the passage — the departing one opening, the arriving one
          // closing — which is the same shape the drifting instrument's handles take.
          if (mf.grainCells > 0) {
            wanted.cellsA = Math.round(Math.min(num(HANDLE_SPECS["strata-light"].cellsA[1]),
                                                Math.max(num(HANDLE_SPECS["strata-light"].cellsA[0]),
                                                         mf.grainCells)));
          }
          if (mt.grainCells > 0) {
            wanted.cellsB = Math.round(Math.min(num(HANDLE_SPECS["strata-light"].cellsB[1]),
                                                Math.max(num(HANDLE_SPECS["strata-light"].cellsB[0]),
                                                         mt.grainCells)));
          }
          // `levelA` AND `levelB` — THE LEVEL EACH WORK PARTS AT, off each work's own median
          // luminance: `luminance.level` (lab/build-workrecords-v1.py), lab/analyze/recipes.py:
          // 551-613 colour_stats()'s python port of `measure(image)` in
          // lab/effects/strata-light.js:108-113 — the number that module solves at build time and,
          // unread, discards. Read PER WORK exactly as `cellsA`/`cellsB` above: A the DEPARTING
          // work's own level, B the ARRIVING work's. This is NOT `palette.colourfulness` (the judge
          // seat's standing correction of 2026-08-18/19): that field is the collection's own
          // COLOURFULNESS ladder, half chroma and half hue spread, and would put a colour number
          // where this tone number belongs.
          wanted.levelA = flt(r4(Math.min(num(HANDLE_SPECS["strata-light"].levelA[1]),
                                          Math.max(num(HANDLE_SPECS["strata-light"].levelA[0]),
                                                   mf.level))));
          wanted.levelB = flt(r4(Math.min(num(HANDLE_SPECS["strata-light"].levelB[1]),
                                          Math.max(num(HANDLE_SPECS["strata-light"].levelB[0]),
                                                   mt.level))));
          //
          // THE TWELVE COLOUR AND LIGHT VOICES, ported from lab/step4-assembler.js:1966-2010. This
          // instrument plays its module twice, once per work (pass-inst-strata-light.js:424-427):
          // layer A takes the DEPARTING work's own readings and layer B the ARRIVING work's, which
          // is `mf` and `mt` here exactly as every other reading in this branch already uses them.
          // Each work sings two voices, colour on its own saturation and light on its own contrast,
          // as the assembler's four seeds do (step4-assembler.js:1972-1981): `seeds[0]` colour/A on
          // sat, `seeds[1]` light/A on contrast, `seeds[2]` colour/B on sat, `seeds[3]` light/B on
          // contrast.
          //
          // PERIOD. Each seed's own measure sets a base period at BEAT_DIAL times (an index offset
          // of 2..5 plus that seed's own reading), and `voiceSpread` (the ported `spread`) nudges
          // each one off any small-integer ratio with an earlier one so the four voices never repeat
          // together — step4-assembler.js:1970-1971. The period offsets for the colour and light
          // voices use each work's saturation and brightness respectively (mirroring the assembler's
          // own `base` array exactly); the AMPLITUDE below uses saturation and contrast instead,
          // because that is the pairing the assembler's own `seeds[].measure` uses, and the two
          // arrays are not the same on purpose in the ported code either.
          //
          // SUNG ONLY WHERE THIS CUE OWNS THE LEVEL THESE TWELVE HANDLES DECLARE (shelf 17's
          // levels law, `ownsLevelOf` above, reading the level off this instrument's own manifest).
          // Where another cue of this same passage owns that level instead, this cue only
          // ACCOMPANIES it there and every one of the twelve handles is left unset — the manifest's
          // own rest of 0, not a second silence invented here.
          if (ownsLevelOf(cue, "strata-light", "colourAmpA")) {
            var slBase = [BEAT_DIAL * (2 + mf.sat), BEAT_DIAL * (3 + mf.brightness),
                          BEAT_DIAL * (4 + mt.sat), BEAT_DIAL * (5 + mt.contrast)];
            var slPeriods = voiceSpread(slBase);
            var slClamp = function (handle, v) {
              return r4(Math.min(num(HANDLE_SPECS["strata-light"][handle][1]),
                                 Math.max(num(HANDLE_SPECS["strata-light"][handle][0]), v)));
            };
            // PHASE. The four voices stand a quarter turn apart, `i / 4` — step4-assembler.js:2000.
            // Each is written only where the work whose measure it sings can be seen singing it —
            // `sayVoice` above, the lab's own second pass.
            // THE LEVEL EACH VOICE HAS TO CLEAR is the pair's own weaker reading of that voice's own
            // measure (`voiceLoudness` above), one level per family and the same one for both
            // layers: the two layers stand on the same frame, so what a voice must stand out of
            // there is what the two works put on it between them.
            var slColourGround = Math.min(mf.sat, mt.sat);
            var slLightGround = Math.min(mf.contrast, mt.contrast);
            sayVoice(wanted, "colour", "A", mf.sat,
                     slClamp("colourPeriodA", slPeriods[0].value), 0 / 4, slColourGround);
            sayVoice(wanted, "light", "A", mf.contrast,
                     slClamp("lightPeriodA", slPeriods[1].value), 1 / 4, slLightGround);
            sayVoice(wanted, "colour", "B", mt.sat,
                     slClamp("colourPeriodB", slPeriods[2].value), 2 / 4, slColourGround);
            sayVoice(wanted, "light", "B", mt.contrast,
                     slClamp("lightPeriodB", slPeriods[3].value), 3 / 4, slLightGround);
          }
        } else if (instr === "strata-scale") {
          // THE TWO STRATA'S OWN CENTRES OF GRAVITY, off each work's own measured reading —
          // lab/analyze/recipes.py's own port of strata-scale.js:279-287 (`cut()`'s own
          // `sum`/`cnt`/`centre`), carried through as `texture.reliefCentreMassX`/
          // `reliefCentreDetailX`. Read PER WORK exactly as strata-light's `levelA`/`levelB`: A the
          // departing work's own pair of centres, B the arriving work's.
          wanted.massCentreXA = flt(r4(clamp01(mf.reliefCentreMassX)));
          wanted.detailCentreXA = flt(r4(clamp01(mf.reliefCentreDetailX)));
          wanted.massCentreXB = flt(r4(clamp01(mt.reliefCentreMassX)));
          wanted.detailCentreXB = flt(r4(clamp01(mt.reliefCentreDetailX)));
          // HOW LONG THE ARRIVING WORK'S BLURRED MASS STANDS ALONE BEFORE ITS DETAIL GROWS INTO IT
          // — charter shelf 12's spectral sentence, composed rather than left at the module's rest.
          // The ARRIVING work's own parting scale is what answers, because it is that work's detail
          // that has to grow in: a work whose luminance lives mostly in its masses has little detail
          // to bring, so the two arrive nearly together, and a work whose luminance lives mostly in
          // its detail needs room for it. `reliefEdge` is how much the MASS stratum carries, so the
          // share the DETAIL needs is one minus it.
          //
          // NOTHING INVENTS A SCALE HERE. `readingOf`'s own clamp puts `reliefEdge` in [0, 1] and
          // the handle is published over [0, 1], so the reading is placed on the handle in the unit
          // it is already in — the same road `parquetPeriod`, `voidShareA`/`voidShareB` and
          // `seamA`/`seamB` already take. The map is monotone and covers the handle's whole span: a
          // work parting entirely into masses lands at one end and one parting entirely into detail
          // at the other.
          //
          // WHERE THE ARRIVING WORK CARRIES NO READING the handle is not driven at all and the
          // module's own rest stands, which is the honest answer and the one every other branch in
          // this file gives. Writing the reading's own zero would send the crossing to one end of
          // the span on the strength of a measurement nobody took.
          if (mt.reliefEdge > 0) {
            wanted.handover = flt(r4(clamp01(1 - mt.reliefEdge)));
          }
          //
          // THE TWELVE COLOUR AND LIGHT VOICES, the same derivation strata-light's own branch above
          // ports (lab/step4-assembler.js:1966-2010), read here for this instrument's own sibling in
          // the same family: layer A takes the DEPARTING work's own readings and layer B the
          // ARRIVING work's, colour on each work's own saturation and light on its own contrast —
          // the same pairing strata-light's branch above uses.
          //
          // SUNG ONLY WHERE THIS CUE OWNS THE LEVEL THESE TWELVE HANDLES DECLARE (shelf 17's
          // levels law, `ownsLevelOf` above, reading the level off this instrument's own manifest).
          // Where another cue of this same passage owns that level instead, this cue only
          // ACCOMPANIES it there and every one of the twelve handles is left unset — the manifest's
          // own rest of 0, not a second silence invented here.
          if (ownsLevelOf(cue, "strata-scale", "colourAmpA")) {
            var ssBase = [BEAT_DIAL * (2 + mf.sat), BEAT_DIAL * (3 + mf.brightness),
                          BEAT_DIAL * (4 + mt.sat), BEAT_DIAL * (5 + mt.contrast)];
            var ssPeriods = voiceSpread(ssBase);
            var ssClamp = function (handle, v) {
              return r4(Math.min(num(HANDLE_SPECS["strata-scale"][handle][1]),
                                 Math.max(num(HANDLE_SPECS["strata-scale"][handle][0]), v)));
            };
            // PHASE. The four voices stand a quarter turn apart, `i / 4` — step4-assembler.js:2000,
            // the same rule strata-light's own branch stands its four voices by, and each is written
            // only where it can be seen — `sayVoice` above.
            // The same per-family level strata-light's own branch hands its four voices.
            var ssColourGround = Math.min(mf.sat, mt.sat);
            var ssLightGround = Math.min(mf.contrast, mt.contrast);
            sayVoice(wanted, "colour", "A", mf.sat,
                     ssClamp("colourPeriodA", ssPeriods[0].value), 0 / 4, ssColourGround);
            sayVoice(wanted, "light", "A", mf.contrast,
                     ssClamp("lightPeriodA", ssPeriods[1].value), 1 / 4, ssLightGround);
            sayVoice(wanted, "colour", "B", mt.sat,
                     ssClamp("colourPeriodB", ssPeriods[2].value), 2 / 4, ssColourGround);
            sayVoice(wanted, "light", "B", mt.contrast,
                     ssClamp("lightPeriodB", ssPeriods[3].value), 3 / 4, ssLightGround);
          }
        } else if (instr === "tilt") {
          // HOW FAR THE PLANE LIES DOWN, off each work's own corridor reading: a picture that
          // already reads as depth is laid down further, and the lean travels from the departing
          // work's own reading to the arriving one's. It is the same measurement the box's
          // perspective and the mirror floor's room take, read here as the plane's own attitude.
          if (mf.tunnel > 0 || mt.tunnel > 0) {
            wanted.tilt = [flt(r4(clamp01(mf.tunnel))), flt(r4(clamp01(mt.tunnel)))];
          }
          // THE LINE THE PLANE TURNS ABOUT, off each work's own measured horizon, so the plane's
          // axis stands where the photograph already puts its own. A work that carries none leaves
          // the handle at the module's own rest.
          if (mf.horizonY !== null || mt.horizonY !== null) {
            var hf = mf.horizonY === null ? mt.horizonY : mf.horizonY;
            var ht = mt.horizonY === null ? mf.horizonY : mt.horizonY;
            wanted.horizon = [flt(r4(clamp01(hf))), flt(r4(clamp01(ht)))];
          }
          // HOW HARD THE FAR ROWS MAY CROWD, off the pair's own repeat said as cells across the
          // frame's height: a fine-grained picture stops resolving sooner as the rows close up, so
          // the camera stands further back for it. The two readings' ratio positions the handle
          // about its own default, the road the material instrument's grain already travels.
          if (mf.grainCells > 0 && mt.grainCells > 0) {
            wanted.squeeze = acrossTheSpan("tilt", "squeeze", mf.grainCells, mt.grainCells);
          }
          // HOW MANY COLUMNS THE FRONT IS BROKEN INTO, off the band family each work's own structure
          // was cut into — the same measured strip count the fabric's ribbons are cut on.
          // 2026-08-19 AUDIT FIX (class A: the arriving work was never asked). `squeeze` two lines
          // above already reads both works' own grain; `columns` sat right beside it reading only
          // `mf.strips`, with no rationale for stopping short of its neighbour. The
          // `X || Y` fallback-when-one-is-unmeasured idiom is `parquet.tiles`'s own, read verbatim.
          if (mf.strips > 0 || mt.strips > 0) {
            var columnsSpec = HANDLE_SPECS.tilt.columns;
            var columnsClamp = function (v) {
              return Math.round(Math.min(num(columnsSpec[1]), Math.max(num(columnsSpec[0]), v)));
            };
            wanted.columns = [columnsClamp(mf.strips || mt.strips), columnsClamp(mt.strips || mf.strips)];
          }
        } else if (instr === "waterline") {
          // THE TWO LINES THE CROSSING TRAVELS BETWEEN — each work's own measured horizon, which is
          // where its mirror seam stands down its own frame. This is the instrument's whole claim:
          // the line leaves one work's own seam and lands on the other's, and the instant it crosses
          // the frame's middle is the instant the two works change places. A work carrying no
          // measured line leaves its handle at the module's own fallback, the frame's own middle,
          // which is the module's own answer for a source with no seam.
          if (mf.horizonY !== null) wanted.seamA = flt(r4(clamp01(mf.horizonY)));
          if (mt.horizonY !== null) wanted.seamB = flt(r4(clamp01(mt.horizonY)));
          // HOW DEEP THE REFLECTION RUNS, off each work's own corridor reading — the same
          // measurement the box's perspective and the leaning plane's attitude take, read here as
          // how far down the water the mirrored mass reaches.
          if (mf.tunnel > 0 || mt.tunnel > 0) {
            wanted.depth = [flt(r4(clamp01(mf.tunnel))), flt(r4(clamp01(mt.tunnel)))];
          }
          // HOW MUCH THE WATER SWELLS, off how much of each work reads as grain rather than as
          // line: a picture made of texture makes a lively surface and one made of straight edges
          // makes a still one. The same reading the water instrument's own swell takes.
          if (mf.textureScore > 0 || mt.textureScore > 0) {
            wanted.swell = [flt(r4(clamp01(mf.textureScore))), flt(r4(clamp01(mt.textureScore)))];
          }
          // HOW RAGGED THE TIDE COMES IN — charter shelf 13's golden-angle stagger again, taken on
          // the departing work's own grain count, so no two stretches of the front arrive together.
          if (mf.grainCells > 0) {
            wanted.order = flt(r4(Math.min(num(HANDLE_SPECS.waterline.order[1]),
                                           Math.max(num(HANDLE_SPECS.waterline.order[0]),
                                                    goldenStagger(mf.grainCells)))));
          }
          // HOW FINELY THE TIDE'S OWN FRONT IS BROKEN, off the departing work's own grain said as
          // cells across its frame — the register's own row for `tideCells`. No file in this tree
          // records how many cells one step of this handle is worth, so the departing work's count
          // is positioned about the handle's own default by its ratio to the arriving work's own
          // count, the same uncalibrated-ratio idiom `grain` and `squeeze` already take on this
          // exact reading elsewhere in this file — read here for the departing side of that ratio,
          // which is `tideCells`'s own row.
          if (mf.grainCells > 0 && mt.grainCells > 0) {
            wanted.tideCells = acrossTheSpan("waterline", "tideCells",
                                              mf.grainCells, mt.grainCells)[0];
          }
        } else if (instr === "pour") {
          // THE POUR'S FOUR HANDLES. Without this branch all four rest at the instrument's own
          // pour — a correct pour, but the SAME pour for every pair, which is what this branch
          // exists to close.
          //
          // SHELF 7'S CRYSTALLIZED ARRIVAL, WHERE IT REACHES PIXELS. `arrival.mode` was settled
          // before this fill ran, by `arrivalOf` ranking the charter's five arrivals against the
          // pair's own records; this is the same road INTERFERED already takes to the overlay and
          // to the grid-and-colour cut. The heap this instrument builds IS the arriving work, so
          // the order its columns let go in is the order that work resolves in: under CRYSTALLIZED
          // the columns are released outward from the seed instead of on the die's own hash, and
          // the seed is `arrival.locus` — the arriving work's own point of greatest disorder, the
          // centre of gravity of its detail stratum (`arrivalOf`'s own note). The delay a column
          // waits is its distance from that seed times `stagger` below, so the spread is the same
          // measured share the pour already had and no second number is invented for it.
          //
          // THE HANDLES ARE DRIVEN ONLY WHERE THE ARRIVAL ACTUALLY NAMED A PLACE. A crystallized
          // arrival whose record carried no relief reading names none (`locusKind` "none"), and
          // there the instrument's own die order stands, which is the honest answer rather than an
          // order started from a place nobody measured.
          if (arrival.mode === "CRYSTALLIZED" && arrival.locusKind === "grain-seed"
              && arrival.locus) {
            wanted.arrival = 1;
            wanted.seedPlace = flt(r4(clamp01(num(arrival.locus[0]))));
          }
          //
          // HOW MANY COLUMNS THE PICTURE POURS IN, at the count of the departing work's own
          // measured lattice across the frame — the grid's period first and the device's step
          // where no grid period was derived. It is handed STRAIGHT rather than positioned,
          // because a column count and a lattice count are one count in one unit; the
          // instrument's own published range holds it, and the instrument rounds it to whole
          // columns and says so in its `applied` block.
          var pourCols = mf.gridCount > 0 ? mf.gridCount
            : (mf.deviceStepPx > 0 && mf.frameSide > 0 ? mf.frameSide / mf.deviceStepPx : 0);
          if (pourCols > 0) {
            wanted.columns = Math.round(Math.min(num(HANDLE_SPECS.pour.columns[1]),
                                        Math.max(num(HANDLE_SPECS.pour.columns[0]), pourCols)));
          }
          // THE ANGLE THE HEAP STANDS AT, off the two works' own finest detail as a RATIO and never
          // as an equality: what no file records is how many degrees of repose one point of detail
          // is worth, and what both records carry is which of the two materials is finer. Each
          // work's detail is said as a share of that work's OWN frame side first, so the ratio is
          // between two shares and not between two pixel counts taken on two different buffers.
          // The heap is the arriving work, so a ratio over one — the arriving work finer than the
          // departing one — walks the handle up and the heap stands steeper. `alongTheSpan` places
          // it about the instrument's own rest a doubling at a time, so the whole span is
          // reachable and a ratio of one lands exactly on the rest.
          if (mf.detailPx > 0 && mt.detailPx > 0 && mf.frameSide > 0 && mt.frameSide > 0) {
            wanted.repose = flt(r4(alongTheSpan("pour", "repose",
                                                (mf.detailPx / mf.frameSide)
                                                / (mt.detailPx / mt.frameSide))));
          }
          // HOW FAR APART THE COLUMNS' OWN RELEASES STAND, at the departing work's own region
          // score. Both are shares already and the handle is a share of its own range, so it is a
          // share against a share with nothing invented between them; the handle's own ceiling of
          // 0.9 is what holds it, because a stagger of one would leave the last column no travel.
          if (mf.regionScore > 0) {
            wanted.stagger = flt(r4(Math.min(num(HANDLE_SPECS.pour.stagger[1]),
                                             clamp01(mf.regionScore))));
          }
          // HOW COARSE THE MATERIAL IS, off the two works' own strongest repeats as a ratio, each
          // said as a share of its own work's frame side for the same reason the repose above is.
          // A coarse departing work — a long repeat — pours in few large crumbs, so the ratio is
          // taken the other way up from the repose: the arriving work's share over the departing
          // one's, which walks the handle DOWN toward the coarse end as the departing work's own
          // repeat grows.
          if (mf.spectralPeriodPx > 0 && mt.spectralPeriodPx > 0
              && mf.frameSide > 0 && mt.frameSide > 0) {
            wanted.grain = flt(r4(alongTheSpan("pour", "grain",
                                               (mt.spectralPeriodPx / mt.frameSide)
                                               / (mf.spectralPeriodPx / mf.frameSide))));
          }
        } else if (instr === "veil") {
          // THE VEIL'S FOUR HANDLES. Without this branch all four rest at the instrument's own
          // weather for every pair alike.
          //
          // HOW THICK THE AIR IS, TRAVELLING from the departing work's own grain reading to the
          // arriving one's — so the air itself changes across the crossing rather than standing
          // still while the works move through it. Both readings are shares and the handle is a
          // share of its own range, so it is a share against a share. The instrument keeps a floor
          // under every sheet, so a thickness of nothing is still a real veil and both doors stay
          // exact at every value this row can write.
          if (mf.textureScore > 0 || mt.textureScore > 0) {
            wanted.thickness = [flt(r4(clamp01(mf.textureScore))),
                                flt(r4(clamp01(mt.textureScore)))];
          }
          // HOW MANY BODIES OF VEIL STAND ACROSS THE FRAME, off the two works' own lattice counts
          // placed ACROSS the handle's own span by their ratio — the same road the water's crest
          // spacing travels, and for the same reason: a lattice count and a count of fog banks are
          // not one number, and saying they were would be a scale nobody measured.
          var vFrom = mf.gridCount > 0 ? mf.gridCount
            : (mf.deviceStepPx > 0 && mf.frameSide > 0 ? mf.frameSide / mf.deviceStepPx : 0);
          var vTo = mt.gridCount > 0 ? mt.gridCount
            : (mt.deviceStepPx > 0 && mt.frameSide > 0 ? mt.frameSide / mt.deviceStepPx : 0);
          if (vFrom > 0 && vTo > 0) {
            wanted.bodies = acrossTheSpan("veil", "bodies", vFrom, vTo);
          }
          // HOW FAR APART THE SHEETS STAND IN DEPTH, at the stronger of the two works' own corridor
          // readings — one stack serves both works, so the pair's own depth is what sets it, and
          // the work that carries depth is the one that has it to give. It is a single value and
          // not a travel: the stack's spread is what the two works' own travel is derived FROM, so
          // a spread that moved mid-pass would move the two works under the visitor.
          if (mf.tunnel > 0 || mt.tunnel > 0) {
            wanted.depth = flt(r4(clamp01(Math.max(mf.tunnel, mt.tunnel))));
          }
          // WHICH WAY THE WIND CARRIES THE SHEETS, along the departing work's own lattice angle —
          // the grid's angle first and the device's where the device recovered a direction, which
          // is the order this file already prefers them in everywhere else. What says the angle IS
          // a reading is the lattice's own PERIOD beside it, not the angle's own value: an angle of
          // exactly nothing is a lattice running square, so a test on the angle alone both drops
          // that real reading and lets an unmeasured work write one.
          var vAng = mf.gridPeriodPx > 0 ? mf.gridAngleDeg
            : (mf.deviceStepPx > 0 ? mf.deviceAngleDeg : null);
          if (vAng !== null) wanted.airAngle = flt(r4(Math.abs(vAng) % 180.0));
        } else if (instr === "wind") {
          // THE WIND'S FIVE HANDLES. Without this branch all five rest at the instrument's own
          // gust for every pair alike.
          //
          // HOW MANY ROWS THE PICTURE IS CUT INTO, at the pivot's own band family — the same count
          // the woven instrument's `strips` takes, off the actors this plan has already cast. It
          // is handed STRAIGHT for the same reason the pour's column count is: a row count and a
          // band count are one count in one unit.
          var rowN = 0;
          actors.forEach(function (a) {
            if (a.role === "pivot-carrier" && a.ref === "a") rowN += a.parts;
          });
          if (rowN) {
            wanted.rows = Math.round(Math.min(num(HANDLE_SPECS.wind.rows[1]),
                                     Math.max(num(HANDLE_SPECS.wind.rows[0]), rowN)));
          }
          // WHICH WAY THE ROWS LIE, off the recorded banding axis and TURNED INTO THIS
          // INSTRUMENT'S OWN UNIT. A vertical band family means the bands run up the frame, so the
          // rows lie that way and the handle stands at a quarter turn; a horizontal family leaves
          // it at nothing. The departing work's family speaks first and the arriving one's answers
          // where it carries none, which is the order the woven instrument's own axis already
          // prefers them in.
          var bandFrom = fromP.ends.banding, bandTo = toP.ends.banding;
          var windFrom = (bandFrom !== undefined && bandFrom !== null
                          && num(bandFrom[2]) < BANDING.length)
            ? AXIS_OF_BANDING[BANDING[num(bandFrom[2])]] : null;
          var windTo = (bandTo !== undefined && bandTo !== null && num(bandTo[2]) < BANDING.length)
            ? AXIS_OF_BANDING[BANDING[num(bandTo[2])]] : null;
          var windCode = windFrom !== null ? windFrom : windTo;
          if (windCode !== null) wanted.axis = flt(windCode === 0 ? 0.5 : 0.0);
          // HOW FAR THE AIR BENDS A ROW, TRAVELLING from the departing work's own banding score to
          // the arriving one's — the same recorded reading the axis two lines up came from, read
          // for its strength rather than for its direction. The bend rides the instrument's own
          // envelope, which is nothing at both doors, so this row cannot reach a landing whatever
          // it writes.
          if (bandFrom || bandTo) {
            wanted.bend = [flt(r4(bandFrom ? clamp01(num(bandFrom[0])) : 0)),
                           flt(r4(bandTo ? clamp01(num(bandTo[0])) : 0))];
          }
          // HOW LONG THE GUST'S OWN BODY IS, off the two works' own repeats along the row as a
          // ratio. It is a single value and not a travel: the front's own start and end are
          // derived FROM the body, so a body that moved mid-pass would move the front under the
          // visitor and the gust would stop being one gust crossing once.
          if (mf.gridPeriodPx > 0 && mt.gridPeriodPx > 0 && mf.frameSide > 0 && mt.frameSide > 0) {
            wanted.gust = flt(r4(alongTheSpan("wind", "gust",
                                              (mf.gridPeriodPx / mf.frameSide)
                                              / (mt.gridPeriodPx / mt.frameSide))));
          }
          // HOW FAR BEHIND THE NEAR ROWS THE FAR ROWS STAND, at the tangent of the angle between
          // the departing work's own lattice and the direction its rows lie in — which is exactly
          // what an angle of incidence means. Past forty-five degrees the tangent passes one and
          // the handle stands at its own ceiling; that ceiling is the instrument's and the row
          // stops there rather than inventing a scale to fit it. The lattice is read the way the
          // veil's own air angle reads it — the PERIOD beside the angle says whether the angle is a
          // reading — because a lag taken against an absent lattice is not a small error: an angle
          // defaulted to nothing against a quarter-turn row axis lands the tangent past its own
          // ceiling, so an unmeasured work would drive this handle to its extreme.
          var wAng = mf.gridPeriodPx > 0 ? mf.gridAngleDeg
            : (mf.deviceStepPx > 0 ? mf.deviceAngleDeg : null);
          if (wAng !== null) {
            var rowDeg = (wanted.axis === undefined ? 0 : num(wanted.axis)) * 180.0;
            var off = (((Math.abs(wAng) - rowDeg) % 180) + 180) % 180;
            if (off > 90) off = 180 - off;
            wanted.lag = flt(r4(clamp01(Math.tan(off * Math.PI / 180.0))));
          }
        } else if (instr === "studio") {
          // THE DARKROOM'S SIX. Without this branch every one of them stood at the module's own
          // number for every pair alike, which is the sameness his word of 2026-08-18 15:13 names.
          //
          // HOW MANY WEDGES THE KALEIDOSCOPE OPENS TO, at the pair's own measured rotational order —
          // the same reading kaleidoscope's own `wedges` handle reads (pass-composer.js's own
          // "kaleidoscope" branch above), placed on this handle's own count.
          if (mf.rotationalN > 0 || mt.rotationalN > 0) {
            wanted.kalN = Math.round(Math.max(mf.rotationalN, mt.rotationalN));
          }
          // HOW MANY TILES THE TILE OPERATION REPEATS ACROSS, at the count of the pair's own
          // measured lattice — the same construction parquet's own `tiles` handle reads (the grid
          // read first, the device second, for the same measured reason parquet's own branch names).
          var tilesFrom = mf.gridCount > 0 ? mf.gridCount
            : (mf.deviceStepPx > 0 && mf.frameSide > 0 ? mf.frameSide / mf.deviceStepPx : 0);
          var tilesTo = mt.gridCount > 0 ? mt.gridCount
            : (mt.deviceStepPx > 0 && mt.frameSide > 0 ? mt.frameSide / mt.deviceStepPx : 0);
          if (tilesFrom > 0 || tilesTo > 0) {
            wanted.tileN = Math.round(Math.max(tilesFrom, tilesTo));
          }
          // HOW WIDE THE PLANET OPERATION OPENS, at the stronger of the two works' own little-world
          // reading — the same reading hero's own `planet` handle reads — placed on THIS handle's
          // own span the OPPOSITE end down from how hero places it: hero's arc travels FURTHER OUT
          // the stronger the reading, and studio's own `spread` runs the other way in the shader's
          // own arithmetic (`stPolar`'s `v = r / spread`), so a NARROWER spread is what a stronger
          // reading asks for — the operation reads as a world the sooner.
          var world = Math.max(readingOf(mf.planet), readingOf(mt.planet));
          if (mf.planet > 0 || mt.planet > 0) {
            var spreadSpec = HANDLE_SPECS.studio.polarSpread;
            wanted.polarSpread = flt(r4(num(spreadSpec[1])
                                        - clamp01(world) * (num(spreadSpec[1]) - num(spreadSpec[0]))));
          }
          // WHERE THE CROP'S OWN PAN AND THE MIRROR'S OWN FOLD LINE STAND: the midpoint of the two
          // works' own measured radial centres, offset from the frame's own middle exactly as hero's
          // own `cenx`/`ceny` and livemirror's own fold line are placed (`centreOfThePair` above
          // gives the raw centre; the offset from 0.5 is this branch's own, the same subtraction
          // hero's `cxF`/`cyF` and livemirror's own fold each already take of it).
          centreOfThePair(wanted);
          var cx = num(wanted.centreX), cy = num(wanted.centreY);
          var panSpec = HANDLE_SPECS.studio.panX, foldSpec = HANDLE_SPECS.studio.foldX;
          wanted.panX = flt(r4(Math.min(num(panSpec[1]), Math.max(num(panSpec[0]), cx - 0.5))));
          wanted.panY = flt(r4(Math.min(num(panSpec[1]), Math.max(num(panSpec[0]), 0.5 - cy))));
          wanted.foldX = flt(r4(Math.min(num(foldSpec[1]), Math.max(num(foldSpec[0]), cx - 0.5))));
          wanted.foldY = flt(r4(Math.min(num(foldSpec[1]), Math.max(num(foldSpec[0]), 0.5 - cy))));
          // `centreX`/`centreY` themselves are not this instrument's own handles — `panX`/`panY` and
          // `foldX`/`foldY` above are — so they are cleared rather than left to be written as a
          // track this manifest never declared.
          delete wanted.centreX;
          delete wanted.centreY;
        }
        var measured = {}, nodes = {};

        // 2026-08-19 THE AUTHORED SHAPE (charter grammar law 3: "the authored shape is the
        // smoothing" — the score owes every dial and clock a shape now that it carries the ease
        // inside the track). Two envelopes, both read off the two works' own records (the first of
        // the three lawful sources; his word 2026-08-19 11:58) and NEVER off a number picked here.
        //
        // `reach` is grammar law 5's one envelope for this cue — the two works' own TONE apartness,
        // `luminance.level` — the identical field and the identical reading the witness camera's
        // own flight (a few screens below, `cmf.level`/`cmt.level`) already turns into its `reach`.
        // Reusing it here rather than a second "how far apart" number of this branch's own is law 5
        // itself: properties that belong to one gesture hang on one scalar so they cannot disagree.
        var reach = clamp01(Math.abs(mf.level - mt.level));
        // `share` is where the brighter work's own claim sits in the passage — the same tone-share
        // idiom the camera's own pitch split falls back to at 0.5 where the pair's own tone carries
        // nothing (both readings exactly absent), read here rather than duplicated because it is
        // the same fact about the same pair. It named `camLvlShare` until 2026-08-25, when the
        // motion peak took over placing the camera's excursion and that variable — which only ever
        // moved the excursion's two ends together — was deleted; the pitch's own `camLvlSum2` a few
        // screens below is the surviving one, and it is the same reading.
        var levelSum = mf.level + mt.level;
        var midShare = levelSum > 0 ? clamp01(mf.level / levelSum) : 0.5;

        // ---- THE CUE'S OWN COURSE: one gesture, one node, and a room that can be HELD ----
        //
        // WHAT STOOD HERE BEFORE AND WHY IT WAS NOT ENOUGH. Every driven handle authored its own
        // shape and its own middle, so a cue driving twelve handles carried twelve separate
        // journeys that happened to start and finish together and were free to disagree everywhere
        // between. Grammar law 5 asks for the opposite in as many words — properties that belong to
        // one gesture hang on one scalar so they cannot disagree — and the client has been able to
        // draw it from the start: a node declared by name stands wherever a node is expected
        // (`pass-layer.js`'s own note above `evalNode`, "one node therefore feeds several
        // channels"), so ONE course with twelve readers is a shape this road already reads.
        //
        // THE COURSE IS NORMALISED. Nought is the departing work's own reading of a handle and one
        // is the arriving work's, whichever way round those two numbers happen to run. Each handle
        // maps that single journey onto its own two measured ends, so the direction, the span and
        // the provenance all stay the handle's own and only the SHAPE is shared.
        //
        // THE ROOM, AND THE ROOM HELD (charter shelf 3, the enfilade: the middle is a room of its
        // own, belonging to neither work; shelf 13's rubato, the deviation that travels). `reach` —
        // the pair's own tone apartness, already read above — carries the course past one in the
        // direction of travel, which is the room itself, AND says how long the room is held: the
        // hold takes `reach` of the shorter leg, so two works standing far apart in tone stand
        // still in the middle for longer and two standing close barely pause. Its bound is the
        // shorter leg, so both legs keep a real journey however far apart the works stand.
        //
        // WHY A HELD PAIR OF POINTS IS A DWELL HERE AND NOT A STEP. The monotone spline this road
        // draws sets BOTH tangents of a flat segment to zero (`pass-layer.js`'s `splineSlopes`:
        // `if (d[i] === 0) { m[i] = 0; m[i + 1] = 0; }`), so the course arrives at the room with no
        // speed left and leaves it the same way — the movement is continuous in value and in speed
        // across the whole passage, which is what makes the hold read as the picture standing still
        // rather than as the picture being stopped.
        //
        // NOT ONE NUMBER HERE IS THIS BRANCH'S OWN: `reach` and `midShare` are the two the door and
        // the witness camera already read off this same pair, and the hold's bound is the shorter
        // leg itself. Where the pair's own record carries no tone apartness at all there is no
        // honest room and no honest hold, and every handle keeps the two-point shaped travel below
        // — his word of 2026-08-19, "if the records genuinely cannot supply a middle, leave it".
        //
        // THE WEIGHT FENCE NEEDS NOTHING NEW. `fitTheWeight`'s last rung sheds a spline to a
        // two-point `map` over its own first and last points; the course's own first and last
        // points are nought and one, so a shed course becomes a plain eased nought-to-one and every
        // reader goes on mapping it onto its own ends. The shape is what is lost, which is the rung
        // it was always meant to be, and the coupling and the measured ends both survive it.
        //
        // AND THE COURSE TAKES A NAME NO TRACK OF THIS CUE ALREADY CLAIMS. Every track's node is
        // named `<cue>-<handle>` (`tracksFor` above), so `<cue>-course` is a name the cue's own
        // course and a handle LITERALLY CALLED `course` both answer to — and the ready story
        // publishes one (`pass-inst-hero.js`, the work's own ring step). Cast on the pivot, both
        // wrote to `pivot-course`, the handle's own ride landed last, and its `in` — the course it
        // rides — pointed at the node it had just overwritten. The host's own graph walk read that
        // for what it was, «cue «pivot» draws a cycle: pivot-course → pivot-course», and refused the
        // score whole. Two things deriving one name collide whenever both are present, so the defect
        // fires on the first pair that casts the ready story on the pivot and on every one after it;
        // it stands on this file as it does on the last commit, so the collision is as old as the
        // shared course and not tonight's. It is closed HERE rather than by renaming that one handle,
        // because the defect is the collision and not the word: the course asks the cue which names
        // are already spoken for and takes one that is not, so no instrument landing a handle of any
        // name can ever take this node's name out from under it again.
        var courseName = c.id + "-course";
        var trackNames = {};
        Object.keys(c.tracks).forEach(function (h) {
          trackNames[(c.tracks[h] || {}).node || (c.id + "-" + h)] = true;
        });
        while (trackNames[courseName]) courseName = courseName + "-shared";
        var courseWanted = reach > 0 && mf.level > 0 && mt.level > 0;
        var courseTop = flt(r4(1 + reach));
        var courseLeg = Math.min(midShare, 1 - midShare);
        var holdFrom = r4(midShare - reach * courseLeg / 2);
        var holdTo = r4(midShare + reach * courseLeg / 2);
        // WHETHER THERE IS A CREST TO SUSPEND AT ALL — charter shelf 15: the crest law IS the
        // culmination's suspension. Until 2026-08-25 both halves of the hold were read from the two
        // works' tone apartness and from nothing else, and the step's own place in the walk never
        // reached this block: a quiet link between two tonally distant works dwelt at its middle,
        // and a culmination between two works standing close in tone passed through without one.
        // The hold is a musical event and tone is not what says whether one is owed.
        //
        // WHAT DECIDES IS THE STEP'S HARMONIC FUNCTION, which the request now carries beside its
        // name and which shelf 15's own map supplies where the walk states none. A DOMINANT is the
        // tension that demands resolution, and a suspension is what that demand sounds like held —
        // so a dominant suspends. A TONIC is the home the eye settles in, with nothing standing
        // unresolved to hold; a SUBDOMINANT prepares, and a preparation that dwells has stopped
        // preparing and arrived. Neither suspends. The function is what is read rather than the
        // name, because a non-crest dominant and a subdominant are both called a middle and those
        // two are exactly the pair this decision has to tell apart.
        //
        // TONE STILL SHAPES THE HOLD and is untouched: how long the room is held and where it sits
        // in the passage are the two works' own `luminance.level`, exactly as before. What changed
        // is that tone no longer decides WHETHER. Where the pair's own tone carries nothing at all
        // there is still no room and no hold — the course itself is not written (`courseWanted`
        // above) — because the room's own height, length and place are all read off that one
        // reading, and his word of 2026-08-19 stands: if the records genuinely cannot supply a
        // middle, leave it. Nothing here refuses a crossing; a step that does not suspend keeps the
        // course's plain passage through, which is what every step read before this line existed.
        var suspends = ctx.routeFunction === "dominant";
        var courseHolds = suspends && holdTo > holdFrom;
        var courseWritten = false;
        // Written on first use, so a cue whose handles all stand still never carries a course
        // nobody reads.
        function courseRead() {
          if (!courseWritten) {
            nodes[courseName] = {
              op: "spline",
              points: courseHolds
                ? [{ at: 0, value: 0 }, { at: flt(holdFrom), value: courseTop },
                   { at: flt(holdTo), value: courseTop }, { at: 1, value: 1 }]
                : [{ at: 0, value: 0 }, { at: flt(r4(midShare)), value: courseTop },
                   { at: 1, value: 1 }],
              in: { source: "cueProgress" },
              note: "the cue's one course, shared by every handle it drives: the room stands at "
                  + pyText(courseTop) + " of the travel, where the two works' own tone stands "
                  + pyText(flt(r4(reach))) + " apart, placed at " + pyText(flt(r4(midShare)))
                  + " by which of them reads brighter"
                  + (courseHolds
                     ? ", and is held from " + pyText(flt(holdFrom)) + " to " + pyText(flt(holdTo))
                       + " of the passage"
                     : (suspends
                        ? ", and passes through without a hold, the two works standing too close in "
                          + "tone for the shorter leg to spare one"
                        : ", and passes through without a hold: this step is a "
                          + ctx.routeFunction + " and shelf 15's crest is the culmination's own "
                          + "suspension, so there is no tension standing here to hold")),
            };
            courseWritten = true;
          }
          return { node: courseName };
        }

        // NO GUARD IS NEEDED HERE ANY MORE, and its absence is the repair rather than a loosening.
        // A throw stood here for a handle the register could not name a measurement for, and
        // `tracksFor` above now never builds a track for one — so no unnamed number can reach a
        // node whatever road the fill is called down. The law is enforced by construction instead
        // of by a refusal.
        Object.keys(c.tracks).sort().forEach(function (h) {
          var nodeName = (c.tracks[h] || {}).node || (c.id + "-" + h);
          var srcRow = sourceOf(c.instrument.id, h);
          var kind = srcRow[0], why = srcRow[1];
          var req = wanted[h] === undefined ? null : wanted[h];
          if (h === "mix") {
            // THE DOOR'S OWN SHAPE (shelf 18: the straight fade is the stock-video-editor feel
            // banned outright; shelf 7, CONDENSED arrival). Never `linear`. `arrival.mode` alone is
            // not a fair contest — `locusOf` hands CONDENSED to any pair where the arriving work's
            // own radial/seam/gate reading is merely present, which real photographs almost always
            // are to SOME small degree, so gating on presence would make "in" the door for nearly
            // every pair regardless of the collection. What decides instead is a RANKING between
            // the strength of that same locus reading (`condenseFit`, the arriving work's own
            // measured pole/seam/gate) and `reach` above — the two candidate stories for this
            // door's own shape, read off the arriving work's own record and the pair's own tone,
            // and the louder one plays. CONDENSED wins loud eases IN — slow while the order still
            // gathers, fast as it completes. Where reach outranks it (or the pair carries no locus
            // at all), the arriving work's tone reading brighter than the departing work's eases
            // OUT — the door decelerates as it lands in the brighter world, grammar law 4's
            // follow-through-then-stillness; where tone does not rise the door breathes evenly both
            // ways ("smooth").
            var condenseFit = arrival.locusKind === "pole" ? mt.radialScore
              : arrival.locusKind === "horizon-seam" ? mt.seamStrength
              : arrival.locusKind === "gate" ? mt.gateGap : 0;
            var doorShape = (arrival.mode === "CONDENSED" && condenseFit >= reach) ? "in"
              : (mt.level > mf.level ? "out" : "smooth");
            // THE DIAL'S OWN TWO ENDS COME OFF THE DIAL, not off the cue's door record. They were
            // read from `c.doors` while every cue's door record named `mix`; since the entry-door
            // contract landed an upper voice's door record names its reserved dry instead, and this
            // line would then have run the crossing dial from nothing to nothing — the voice would
            // have stood at its own departing pose for the whole window. `HANDLE_SPECS[instr].mix`
            // is the handle's own published floor and ceiling, which is what a door value always
            // was; for every cue whose door still names `mix` this writes the identical two numbers.
            var mixSpan = HANDLE_SPECS[instr].mix;
            nodes[nodeName] = { op: "mix", a: flt(num(mixSpan[0])), b: flt(num(mixSpan[1])),
                                t: { op: "curve", name: doorShape, in: { source: "cueProgress" } },
                                note: why };
            return;
          }
          // THE ENTRY DOOR'S RESERVED DRY — the charter's build ladder, step 0. A voice standing
          // over another is ABSENT at both of its doors and whole across its middle, so it joins a
          // running picture without replacing it and stands down the same way. Nothing is ever
          // weighed against anything: at no instant does this hold one picture against another,
          // which is what separates it from the opacity handle clause (a) removed.
          //
          // THE SHAPE IS THE ONE THE SEAM CHECK WALKS: a monotone spline over the cue's OWN
          // progress through (0, 0), (0.5, 1), (1, 0). The host's own spline sets both tangents of
          // a flat segment to zero, so the dry leaves nothing and returns to nothing with no speed
          // at either end — the join and the stand-down are continuous in value and in speed, which
          // is what makes them unseeable rather than merely small.
          //
          // THE LOWEST VOICE OWES THE OPPOSITE and gets it: nothing stands beneath it, so a door it
          // draws nothing at is a door the visitor sees the page through, and the host refuses such
          // a score outright (`presenceWhyNo`). It stands whole for its whole window — the handle's
          // own rest, written rather than left implied so the plan says what it means.
          if (kind === "entry-door") {
            if (num(c.stack) > 0) {
              nodes[nodeName] = {
                op: "spline", in: { source: "cueProgress" },
                points: [{ at: flt(0.0), value: flt(0.0) },
                         { at: flt(0.5), value: flt(1.0) },
                         { at: flt(1.0), value: flt(0.0) }],
                note: "requested nothing at this cue's own two doors and whole across its middle, "
                      + "because this voice stands over another. From " + why };
            } else {
              nodes[nodeName] = {
                op: "static", value: flt(1.0),
                note: "requested whole for the whole window, because this voice is the lowest of "
                      + "its stack and nothing stands beneath it. From " + why };
            }
            return;
          }
          if (kind === "host-clock") {
            nodes[nodeName] = { source: "time", note: why };
            return;
          }
          // A HANDLE THAT RIDES THE PASSAGE'S OWN TRAVEL, and it is the row's word that says so
          // rather than the handle's name. `mix` is the door and has its own shape, above; every
          // other `progress` handle crosses its own published span as the passage crosses, which is
          // exactly what its row promises. This is the branch whose absence held `parquet.spin` and
          // `unfold.field` still at their defaults for the whole passage while their rows said they
          // travelled.
          if (kind === "progress") {
            var pSpan = HANDLE_SPECS[instr][h];
            var pFrom = appliedValue(instr, h, pSpan[0])[1];
            var pTo = appliedValue(instr, h, pSpan[1])[1];
            nodes[nodeName] = {
              op: "map",
              in: { op: "curve", name: "smooth", in: { source: "cueProgress" } },
              from: [0, 1], to: [pFrom, pTo],
              note: "requested the passage's own travel across this handle's own published span, "
                    + "from " + pyText(pFrom) + " to " + pyText(pTo) + ", from " + why };
            return;
          }
          if (Array.isArray(req)) {
            var ends2 = req.map(function (v) { return appliedValue(instr, h, v); });
            measured[h] = req;
            var endA = ends2[0][1], endB = ends2[1][1], endAn = num(endA), endBn = num(endB);
            // THE TRAVELLING HANDLE'S OWN SHAPE, by the door's own discipline: read off the two
            // ends this handle already resolved above, so the shape is a fact about THIS handle's
            // own journey. Rising into a stronger arriving reading eases IN (built momentum);
            // falling from a stronger departing one eases OUT (grammar law 4's follow-through);
            // unchanged breathes evenly ("smooth") because there is no direction to lean toward.
            var travelShape = endAn === endBn ? "smooth" : (endBn > endAn ? "in" : "out");
            var noteText = noteFor(h, req, ends2.map(function (e) { return e[1]; }), why);

            // THE MIDDLE ROOM (charter shelf 3, the enfilade: "the middle is a room of its own...
            // belonging to neither work"). Depth and place both come off the two envelopes above,
            // never off a third number picked for this handle. Where the pair's own tone carries no
            // apartness (`reach` is exactly nothing, or either work's own tone is itself
            // unmeasured), OR where this handle's own two ends already resolved equal (nothing for
            // the room to stand apart from — an overshoot with no span is not a room, it is the
            // same point three times), there is no honest middle to give, and the handle keeps its
            // two points — his word 2026-08-19: "if the records genuinely cannot supply a
            // middle... leave it".
            var spanV = Math.abs(endBn - endAn);
            if (courseWanted && spanV > 0) {
              // THE HANDLE RIDES THE CUE'S OWN COURSE, mapped onto its own two measured ends. The
              // room's value is unchanged from the three-point spline this replaced: a course of
              // `1 + reach` read through the map lands at `endA + (endB - endA) * (1 + reach)`,
              // which for a rising handle is the higher end overshot by `reach` of its own span and
              // for a falling one the lower end undershot by the same — the identical number, now
              // arrived at once for the whole cue instead of once per handle.
              //
              // THE HANDLE'S OWN PUBLISHED RANGE STILL ANSWERS. Where the room carries the reading
              // past what the instrument publishes, the node is wrapped in the client's own `clamp`
              // rather than left to be clipped silently at the frame: `appliedValue` did that
              // clamping for the three-point spline's middle point, and the same two numbers do it
              // here, so a course shared by twelve handles cannot push any one of them past its own
              // manifest. Where the room stays inside the range no wrapper is written, and the node
              // is the map alone.
              //
              // THE NOTE STAYS ON THE OUTERMOST NODE, and that is not a detail. A node the composer
              // drove carries its provenance — where the number came from — and everything that
              // reads provenance reads it off the node the handle's own track names: the
              // diagnostic surface, and `test_pass_composed.py`'s own sweep, which walks a cue's
              // nodes and skips any whose note does not open with «requested». Writing the note on
              // the map and then wrapping the map in a clamp hid it one level down, and the sweep
              // went quietly blind to exactly the handles whose room overshoots their own range —
              // ten of the gates instrument's own slot readings vanished from a green row that way
              // before this line was written.
              var span = HANDLE_SPECS[instr][h];
              var roomV = endAn + (endBn - endAn) * num(courseTop);
              var ride = { op: "map", in: courseRead(), from: [0, 1], to: [endA, endB] };
              if (roomV < num(span[0]) || roomV > num(span[1])) {
                nodes[nodeName] = { op: "clamp", in: ride,
                                    min: appliedValue(instr, h, span[0])[1],
                                    max: appliedValue(instr, h, span[1])[1], note: noteText };
              } else {
                ride.note = noteText;
                nodes[nodeName] = ride;
              }
            } else {
              // THE PLAIN TWO-POINT TRAVEL, AND IT IS A `map` RATHER THAN A `mix` (2026-08-24).
              // A handle's two ends leave `appliedValue` MARKED — an integer where the composition
              // holds one and a marked float otherwise, which is what keeps this file's own writer
              // able to print 1.0 where Python prints 1.0. The drawing host reads a `mix` node's `a`
              // and `b` as NODES, through `evalNode`, and a marked float is an object with no `op`
              // on it: the host answered «the operator "undefined" is declared and drawn by no
              // evaluator yet», recorded a fallback and drew the manifest's own default instead. Its
              // own log names the handles it happened to — refract, reach, swell, crest, slotPlace,
              // slotHalf — which are exactly the handles the night's audit says give the water and
              // the fold their character, and it reached EVERY travelling handle whose two ends
              // resolved equal or whose pair carried no middle, not only those six.
              //
              // `map` is the operator that reads its ends as NUMBERS (`Number(t[0])`, which takes a
              // marked float through its own `valueOf`), and it is already the shape the branch
              // above writes for the same handle when the cue carries a course — so the two roads
              // now differ only in what they read, which is the whole difference between them.
              // NOTHING ABOUT THE MOTION CHANGES: `map` over `from: [0, 1]` onto `to: [endA, endB]`
              // is `endA + (endB − endA) · x` with `x` the same eased curve the `mix` handed its
              // `t`, which is the same arithmetic `mix` itself performs on the same two numbers.
              nodes[nodeName] = {
                op: "map",
                in: { op: "curve", name: travelShape, in: { source: "cueProgress" } },
                from: [0, 1], to: [endA, endB], note: noteText };
            }
            return;
          }
          var pairv = appliedValue(instr, h, req);
          if (req !== null) measured[h] = pairv[0];
          // A NODE THE COMPOSER DROVE CARRIES ITS PROVENANCE; A NODE LEFT AT THE INSTRUMENT'S OWN
          // DEFAULT CARRIES NONE. The note answers «where did this number come from», and for a
          // handle nobody drove the answer is already published, in the manifest, as the default
          // itself — so the sentence said only that the score had nothing to say. It also weighed:
          // a folding cue drives twelve handles and the boilerplate on the rest put 517 of the
          // collection's scores over the client's own byte fence, where a score is refused WHOLE.
          nodes[nodeName] = req === null
            ? { op: "static", value: pairv[1] }
            : { op: "static", value: pairv[1], note: noteFor(h, req, pairv[1], why) };
        });
        c.measuredHandles = measured;
        c.nodes = nodes;
        cues.push(c);
      });

      var camera = copy(tpl.camera);
      if (camera.track.length === 4) {
        var travel = null;
        cues.forEach(function (c) { if (c.id === "travel") travel = c; });
        // HOW LONG THE EXCURSION IS. `span` decides the LENGTH of the witness camera's excursion
        // and nothing about where it stands: where the plan travels on a cue of its own, the
        // travelling cue's own window gives that length; where it travels on no cue, the length is
        // half the passage.
        //
        // WHERE THE EXCURSION STANDS is decided below, by the plan's own motion peak — shelf 5's
        // conjuror law, computed rather than asserted. Until 2026-08-25 the two middle points
        // simply took `span`'s own two ends, and the comment that stood here called the travelling
        // cue's window "the composer's own reading of where that peak sits": no parameter velocity
        // was ever summed, normalised or maximised, and where a plan travelled on no cue this file
        // said outright that there was no motion peak it could name. `motionPeak` above names one
        // for every plan.
        //
        // AND THE TONE SPLIT IS GONE FROM THIS LINE, deliberately. `camLvlShare` — the two works'
        // own `luminance.level` read as a share — multiplied both ends of the no-travel span by the
        // same factor, so it moved the excursion's two ends TOGETHER and its length was exactly
        // half the passage whatever the share read. The moment the peak decides where the excursion
        // stands, that reading reaches nothing at all: a number taken off the two works that no
        // longer touches the plan, which is worse than no reading because it looks like one. It is
        // deleted rather than left standing. The length it produced is unchanged — half the
        // passage, the same half it always was — so nothing static is introduced here; what is
        // removed is a dead reading, and what the no-travel plan GAINED is a placement that is now
        // measured off the plan's own motion instead of sitting at a fixed share of the passage.
        //
        // THE OTHER HONEST ANSWER — routing the tone reading into the excursion's own LENGTH, where
        // a viewer would actually see it — is the better one and is not taken here: it re-bases
        // `tests/test_pass_peak.py`'s own length row, which asks for half the passage on a
        // no-travel plan, and that file stands outside this hand's write set.
        var span;
        if (travel) {
          span = travel.window;
        } else {
          span = [flt(0), flt(r4(0.5 * duration / 1000.0))];
        }
        // WHERE THE TWO MIDDLE POINTS STAND IN TIME — charter shelf 5, THE CONJUROR. `span` above
        // gives the excursion its LENGTH, measured: the travelling cue's own window, or half the
        // passage where the plan travels on no cue. That length is not touched here. What the shelf
        // decides is WHERE the excursion stands, and the answer is the plan's own motion peak — the
        // argmax of its summed normalised parameter velocity, `motionPeak` above.
        //
        // THE ROOM IS SHARED IN THE PEAK'S OWN PROPORTION. The excursion of length `L` leaves the
        // passage `D − L` of room over, and the two legs — the flight out of the departing pose and
        // the flight back into the arriving one — take that room in the same proportion the peak
        // takes the passage. Writing `q` for the peak's own share:
        //
        //     track[1].at = q · (D − L)          track[2].at = q · (D − L) + L
        //
        // FOUR THINGS FALL OUT OF THOSE TWO LINES BY ALGEBRA, for every `q` in nought to one and
        // every `L` no longer than `D`, so none of them needs a clamp and none can be lost to a
        // pair the collection happens not to carry:
        //
        //   · both points stand inside the passage — the first between nought and `D − L`, the
        //     second between `L` and `D`;
        //   · they keep their order and stand exactly `L` apart, so the excursion is the same
        //     journey the measurement above sized, moved rather than stretched;
        //   · the peak itself stands INSIDE the excursion, at the same share `q` of it as it holds
        //     of the passage — `qD − q(D − L) = qL` is never negative and `q(D − L) + L − qD =
        //     L(1 − q)` never is either, so the camera is out on its flight at the instant the
        //     plan moves fastest, which is the whole of what the shelf asks for;
        //   · the two legs are `q(D − L)` and `(1 − q)(D − L)`, which are equal only where the peak
        //     stands exactly at the passage's middle. Shelf 18's reading of 2026-08-19 — outbound
        //     and return taking different shares — therefore survives as a measured fact rather
        //     than as a shape this branch has to arrange.
        //
        // `L ≤ D` IS ALREADY TRUE OF EVERY `span` THIS BRANCH CAN BUILD: a cue window is composed
        // inside the passage, and the no-travel length is half of it. The guard below states it
        // anyway, so the arithmetic answers for values that never reach it.
        //
        // AND WHERE NO INSTANT IS LOUDER THAN ANOTHER the shelf names no peak, and the excursion is
        // left exactly where the measurement above put it — his word of 2026-08-19, "if the records
        // genuinely cannot supply a middle, leave it". That is not a crossing refused: the flight
        // still flies, the doors still open, and the passage plays whole.
        var camPeak = motionPeak(cues, duration / 1000.0);
        var camAt0 = num(span[0]), camAt1 = num(span[1]);
        var camLen = camAt1 - camAt0, camRoom = duration / 1000.0 - camLen;
        if (!camPeak.flat && camRoom >= 0) {
          camAt0 = camPeak.share * camRoom;
          camAt1 = camAt0 + camLen;
        }
        camera.track[1].at = flt(r4(camAt0));
        camera.track[2].at = flt(r4(camAt1));

        // THE FLIGHT ITSELF (charter shelf 2, grammar law 5). `cmf`/`cmt` are the two works' own
        // measured record — `measuredParts()` above, the same one every cue's handles already read
        // off `fromP.measured`/`toP.measured` — so every axis below reads a number already in the
        // record and nothing this file invents at the pair.
        var cmf = fromP.measured, cmt = toP.measured;

        // ONE ENVELOPE COUPLES EVERY AXIS. Grammar law 5: "properties that belong to one gesture
        // hang on one scalar, so they cannot disagree." `reach` is that one scalar — how far apart
        // this pair's own works stand — and every axis below takes its MAGNITUDE from `reach`
        // alone; each axis's own reading below contributes only its DIRECTION and its SHAPE across
        // the two middle points, never a second say in how far the flight travels. `reach` is not
        // a new distance: it is the same |A-B| apartness the grid-colour instrument's own `lead`
        // handle already reads off this pair (this file, the grid-colour branch a few screens
        // above), taken here on the two works' own TONE rather than on their colour spread.
        //
        // WHY TONE AND NOT COLOURFULNESS, decided at the judge seat 2026-08-19 02:20. The first
        // build of this flight reused `lead`'s reading whole, colour spread and all. A camera is
        // the WORLD voice of shelf 17 and it flies through LIGHT, so how far apart two works stand
        // in their own light is the apartness a flight answers to; how far apart they stand in the
        // spread of their hues is the palette's business and drives the palette's own handles.
        // `luminance.level` is the median of a work's own luminance, measured for the first time
        // tonight (lab/analyze/recipes.py, a port of lab/effects/strata-light.js:108-113), which is
        // why this reading could not have been taken before today.
        //
        // WHAT THIS REACH STILL DOES NOT READ, named rather than quietly missing: the passage's own
        // ROLE. Shelf 17 gives a culmination three accompaniments and a quiet link one, so a
        // culmination's camera ought to fly further than a quiet link's, and today it does not —
        // the tier reaches this flight nowhere. That waits on the same restructuring the colour
        // voice waits on, where the role's budget and the voices that spend it finally meet.
        var reach = clamp01(Math.abs(cmf.level - cmt.level));
        // THE ONE BOUND EVERY AXIS SHARES. `DOLLY_CAP` above already bounds the dolly's own
        // logarithm at 0.5 (1.65 times); sharing that one number across pitch, yaw and roll, read
        // as radians, and across pan, read as a frame fraction — where 0.5 is already the natural
        // distance from the frame's own centre to its edge — is what keeps the bound ONE number
        // the whole flight answers to rather than five this file would otherwise have to invent.
        var camBound = DOLLY_CAP;

        // PAN — toward the pivot's own centre. `structure.radial.centre` where the work has one
        // (measuredParts()'s own `radialScore` says whether it does), otherwise the centre of
        // `structure.dominantObject.bbox` (measuredParts()'s own `figureShare` says whether that
        // box is real rather than the record's [0,0,0,0] absence). A work with neither contributes
        // nothing to pan at its own point, which is the honest answer and not a gap filled with
        // the frame's own middle.
        var panFrom = camAxisPan(cmf, reach), panTo = camAxisPan(cmt, reach);
        camera.track[1].pan = { x: flt(r4(panFrom[0])), y: flt(r4(panFrom[1])) };
        camera.track[2].pan = { x: flt(r4(panTo[0])), y: flt(r4(panTo[1])) };

        // LOGSCALE — the two works' own grain, `texture.spectralPeriodPx` over the frame side
        // (measuredParts()'s own `grainCells`). Shelf 2 names a uniform zoom a straight line in
        // log-space, which is why this axis carries the LOGARITHM and not a linear scale. Standing
        // BACK is the one move that lets a coarse pattern — the work of the pair with the FEWER
        // cells across its own frame — read at all; standing IN only crops it further, so the sign
        // is not a choice between the two works but the one direction that serves either. The
        // reading holds through both middle points, exactly as the pre-existing gears-only flight
        // already held its own dolly at one value across its own two points.
        //
        // HOW FAR BACK, and until 2026-08-19 this line answered with the envelope's own full reach
        // whenever both works carried grain — the gate decided whether the dolly moved at all, and
        // `reach` alone decided how far, so two pairs whose grains stood a hair apart and two whose
        // grains stood worlds apart flew the same distance the instant both cleared the gate. That
        // is not what the paragraph above claims: standing back is what lets the COARSER work's
        // grain read, so how much further back is owed is a question the GAP between the two
        // grains has to answer, not a question the envelope alone can. `grainAsked` is that gap,
        // the two `grainCells` taken as a signed ratio the same way `cameraFlight`'s own dolly once
        // took the two doors' `stepPx` a few screens above; `grainShare` spends it against the
        // shared bound with the identical shape that line already established — `CAP · a / (|a| +
        // CAP)`, a limit and never a wall, reusing `camBound` itself rather than a second number —
        // so a pair whose grains stand worlds apart asks for nearly everything the envelope owns,
        // one whose grains stand close asks for almost none of it, and the rise between the two is
        // monotone with no pair ever clipped at the wall the gate used to leave every gated pair
        // standing against.
        //
        // `DOLLY_CAP` NO LONGER BINDS THIS AXIS ALONE, and that is worth naming because the axis was
        // built around that one bound (the comment above `DOLLY_CAP`'s own declaration). `logScale`
        // is now `reach * camBound * grainShare`, the product of TWO independent readings each
        // already short of its own ceiling before multiplication — `reach` (the pair's own tone
        // apartness, `clamp01`, never quite 1 for a real pair) and `grainShare` (this line's own
        // limit, never quite 1 either) — so their product falls short of `camBound` by more than
        // either factor alone does, and reaching `camBound` would need a THIRD reading pushing
        // `reach` itself toward 1 (the passage's own role, shelf 17's tier, still unread by `reach`
        // above) rather than anything this line could change. The construction that IS still a live
        // ceiling is `grainShare` itself, and it is a limit and not a wall by its own shape: for any
        // gap whatever, `|a| / (|a| + CAP)` is strictly under 1 and reaches 1 only in the limit, so
        // no pair is ever clipped and no pair ever spends the whole bound. That holds for every pair
        // of grains there is; no collection is consulted for it, and none could add to it.
        var logScale = 0;
        if (cmf.grainCells > 0 && cmt.grainCells > 0) {
          var grainAsked = Math.log(cmf.grainCells / cmt.grainCells);
          var grainShare = Math.abs(grainAsked) / (Math.abs(grainAsked) + camBound);
          logScale = -reach * camBound * grainShare;
        }
        camera.track[1].logScale = flt(r4(logScale));
        camera.track[2].logScale = flt(r4(logScale));

        // ROLL — the two works' own lattice angles, `structure.ownDevice.angleDeg` falling back to
        // `structure.grid.angleDeg` (measuredParts()'s own `latticeAngleDeg`). The camera's horizon
        // rolls toward the SIGNED difference between the two works' own lattices, the same fold
        // the beat instrument's own `beatTilt` already takes (this file, the beat branch: the raw
        // difference of the two `latticeAngleDeg` readings, folded back under a right angle because
        // a lattice angle is a line direction and two grating families never stand further apart
        // than that). His 2026-08-17 19:13 word: every geometric parameter is READ from the work,
        // and a sign is a direction, not a reading — so `rollDelta`'s own MAGNITUDE, folded to the
        // same 0..90 a line direction can never exceed (the comment above, unchanged), now grades
        // the excursion alongside its sign: two lattices barely off grade this near nothing, two
        // standing the full 90 degrees apart grade the whole span `reach` already bounds. `reach`
        // still spends its own span; this only decides how much of it the two works actually asked
        // for.
        var roll = 0;
        if (cmf.latticePx > 0 && cmt.latticePx > 0) {
          var rollDelta = (cmt.latticeAngleDeg - cmf.latticeAngleDeg) % 180;
          if (rollDelta > 90) rollDelta -= 180;
          if (rollDelta < -90) rollDelta += 180;
          if (rollDelta !== 0) {
            roll = reach * camBound * (rollDelta > 0 ? 1 : -1) * (Math.abs(rollDelta) / 90);
          }
        }

        // YAW — the departing work's own gate, `motifs.gateAxis` and `motifs.gatePlace`
        // (measuredParts()'s own `gateAxis`/`gatePlace`). The camera turns toward the slot the
        // work actually has — `gateAxis` says whether it has one at all, read the same way the
        // gates instrument's own `slotAxis` handle already reads it a few screens above — and
        // turns further the further that slot stands off the frame's own middle: `gatePlace` is a
        // FRAME FRACTION, where the slot sits along its own axis, so it runs 0 to 1 by what it is
        // and `gatePlace - 0.5` is already signed off the frame's own centre with a magnitude of at
        // most 0.5. That is the field's own definition and not a range read off any collection; a
        // collection can only ever occupy part of it. The same 19:13 word applies here: `gateOff`'s
        // own MAGNITUDE, not only
        // its sign, now grades the turn — a slot standing barely off-centre grades near nothing, one
        // standing at the frame's own edge (`gatePlace` at 0 or 1, `|gateOff|` at its own structural
        // ceiling of 0.5 — the identical 0..1 frame-fraction convention `horizonY - 0.5` reads a few
        // lines below) grades the whole span. How pronounced or how off-centre the quiet band sits
        // is what decides how much of `reach`'s own span this axis asks for.
        var yaw = 0;
        if (cmf.gateAxis !== null && cmf.gateAxis !== undefined && cmf.gatePlace > 0) {
          var gateOff = cmf.gatePlace - 0.5;
          if (gateOff !== 0) {
            yaw = reach * camBound * (gateOff > 0 ? 1 : -1) * (Math.abs(gateOff) / 0.5);
          }
        }

        // PITCH — the two works' own measured horizons, `structure.horizon.y`
        // (measuredParts()'s own `horizonY`, null where a work carries none). The eye level
        // travels from the departing work's own seam to the arriving work's, so pitch differs at
        // the two middle points by construction, exactly as pan does. A work with no horizon
        // contributes nothing to pitch AT ITS OWN POINT, which is measuredParts()'s own null read
        // honestly rather than defaulted to the frame's own middle. Its own magnitude candidate,
        // exactly as it always was; see below.
        var pitchFrom = camAxisPitch(cmf, reach, camBound);
        var pitchTo = camAxisPitch(cmt, reach, camBound);

        // THE PALINDROME BAN, CAMERA READING (charter shelf 18, 2026-08-19, "the seat, on his
        // delegation... this is not his own word and does not become one"). The end points stay
        // neutral (shelf 2's own rest on B, untouched above and below this block) and what the ban
        // forbids on the camera is the retrace: every rotational axis going out and coming straight
        // back the way it came. Three conditions carry the homecoming without the retrace, and all
        // three are read off the pair rather than invented.
        //
        // (i) ONE AXIS CARRIES THE EXCURSION. Roll, yaw and pitch above are still computed exactly
        // as they always were — nothing above this comment changed — and only now is one chosen:
        // the axis this pair calls for MOST STRONGLY plays and the other two are written zero at
        // both middle points, so a viewer reads one turn rather than three faint ones competing.
        //
        // THE THREE MAGNITUDES ARE NOT COMPARABLE AS RAW RADIANS, and comparing them raw was the
        // wrong contest even now that all three read a graded quantity off the pair rather than a
        // bare sign (roll's own lattice-angle gap above, yaw's own gate-offset gap above, pitch's
        // own horizon offset below): the three still answer to three different ceilings. Roll's and
        // yaw's own magnitude factors above (`|rollDelta| / 90`, `|gateOff| / 0.5`) are each already
        // normalised to their OWN reading's structural bound, so roll and yaw both still reach the
        // full `reach * camBound` at their own extreme — a lattice gap of the full 90 degrees a line
        // direction can ever stand apart, a gate sitting at the frame's own literal edge. Pitch's own
        // reading (`(horizonY - 0.5) * reach * camBound`) is bounded at HALF of that: horizonY is a
        // frame fraction, the same 0..1 the `- 0.5` a few lines below already assumes, the identical
        // convention `gatePlace - 0.5` and `figureCx - 0.5` read elsewhere in this file, so
        // `|horizonY - 0.5|` itself is bounded at 0.5 and pitch's own ceiling is `0.5 * camBound`
        // rather than `camBound`. Picking the largest raw radian value would still favour the axis
        // with the loosest ceiling over the axis this pair actually calls for, which is a different
        // question. So each candidate is read here as a SHARE of its own ceiling instead —
        // `magnitude / thatAxis'sOwnMaximum`, every ceiling read off the derivations directly above
        // rather than invented: roll's and yaw's own maximum is `camBound` itself; pitch's own
        // maximum is `0.5 * camBound`, the same halving `camAxisPitch`'s own `- 0.5` already carries.
        // Every derivation and every existing gate stands exactly as it did; what changed is that
        // roll and yaw now carry the graded quantity pitch always had, and what the three shares are
        // measured against.
        var pitchMag = Math.max(Math.abs(pitchFrom), Math.abs(pitchTo));
        var rollCap = camBound, yawCap = camBound, pitchCap = 0.5 * camBound;
        var rollShare = rollCap > 0 ? Math.abs(roll) / rollCap : 0;
        var yawShare = yawCap > 0 ? Math.abs(yaw) / yawCap : 0;
        var pitchShare = pitchCap > 0 ? pitchMag / pitchCap : 0;
        // A tie is broken on the pass's own die, salted by this cue's own key so the same two works
        // still answer differently across seeds — the same mechanism `rhythmShift` a few screens
        // above already draws from.
        var camCandidates = [["roll", rollShare], ["yaw", yawShare], ["pitch", pitchShare]];
        var camMaxShare = Math.max(camCandidates[0][1], camCandidates[1][1], camCandidates[2][1]);
        var camTied = camCandidates.filter(function (c) { return c[1] === camMaxShare; })
          .map(function (c) { return c[0]; });
        var camAxis = camTied.length === 1 ? camTied[0]
          : camTied[dieAmong(num(row[4]), key + "|camAxis", camTied.length)];

        // (i·b) AND THE AXIS THAT CARRIES IT HAS TO BE SEEN CARRYING IT — his word of 2026-08-24,
        // watching the live route: the camera's movement does not visibly read during a crossing.
        // Nothing above this comment is wrong. Every axis reads its own record correctly and the
        // contest between them is honest. What was missing is that the amplitude is a PRODUCT of
        // independent readings, each already short of its own ceiling before they meet — the pair's
        // own tone apartness in `reach`, which `clamp01` holds under 1, and the axis's own graded
        // magnitude, which its own derivation above holds under 1 — so the excursion is bounded by
        // the SMALLER of two fractions and collapses toward nothing however strongly the pair calls
        // for it. That is a fact about the shape of the product and not about any collection: two
        // factors under 1 multiply to less than either. The note above `reach` names the same gap
        // from the other side: shelf 17 gives a culmination more accompaniment than a quiet link and
        // the tier reaches this flight nowhere.
        //
        // SHELF 17'S BUDGET BECOMES A LEVEL AND NOT ONLY A COUNT, which is the half of it that was
        // never built. A voice that is counted against the budget and cannot be seen is a voice the
        // budget is spending on nothing — the same emptiness the lab names for the colour voices
        // («Заявленный и неслышный голос — пустое утверждение разбора») said of the camera.
        //
        // WHAT THE FLOOR IS READ FROM, and it is the two works and no number of this file's. A
        // camera excursion reads when the frame's own edge travels by at least ONE element of the
        // pair's finer measured grain: below that the pose has moved by less than the smaller
        // picture's own smallest feature, and there is nothing on screen to read the motion against.
        // The grain is `latticePx` — the step the work was actually cut at, the same reading roll's
        // own sign is folded from — as a share of that work's own frame side. The FINER of the two
        // sets the floor, because the finer grain is what registers the smallest motion; the coarser
        // would ask for a turn the pair never called for. The arithmetic from there is
        // `camVoiceFloor`'s own, stated where the function stands.
        //
        // AND IT IS THE CARRYING AXIS'S OWN CEILING THE FLOOR IS TAKEN AGAINST. The floor is a
        // SHARE, the contest above ranks SHARES, and a share only means anything beside the ceiling
        // it is a share of. The grain asks for an ANGLE — 2 · grainFrac — and the three axes do not
        // publish one ceiling between them: roll and yaw reach `camBound`, pitch reaches half of it,
        // exactly as the paragraph above the contest derives. A floor computed against `camBound`
        // and then spent on pitch would buy pitch only half the angle the grain asked for, which is
        // the whole failure this block exists to repair, reappearing on one axis in three. So the
        // ceiling that goes into the floor is the one belonging to the axis that WON the contest —
        // `camMaxShare` is that axis's own share by construction, since the contest picks the argmax
        // and this is its max — and the two always answer for the same axis.
        //
        // SHELF 9'S LAW HOLDS INSIDE IT. The readings still RANK — which axis carries is the contest
        // above, untouched, and how far above the floor it flies is still the pair's own reading.
        // No pair is refused, no crossing is declined, and no axis leaves its own published ceiling;
        // the floor only guarantees that the voice the passage chose can be seen at all. Both halves
        // of that are `camVoiceLift`'s own bounds, proved there over every number either argument
        // can hold rather than checked against whichever photographs are on disk.
        var camGrainA = cmf.frameSide > 0 && cmf.latticePx > 0 ? cmf.latticePx / cmf.frameSide : 0;
        var camGrainB = cmt.frameSide > 0 && cmt.latticePx > 0 ? cmt.latticePx / cmt.frameSide : 0;
        var camCap = camAxis === "roll" ? rollCap : (camAxis === "yaw" ? yawCap : pitchCap);
        var camFloor = (camGrainA > 0 && camGrainB > 0)
          ? camVoiceFloor(Math.min(camGrainA, camGrainB), camCap) : 0;
        // The lift is applied to the carrying axis's own magnitude, so every shape below — the
        // outbound-to-inbound fraction of condition (ii), the arc pitch already travels, the signs
        // each axis read off its own record — is carried through untouched and only scaled. The two
        // axes that lost the contest are scaled too and then written zero a few lines below, so the
        // multiply reaches them without reaching the score.
        var camLift = camVoiceLift(camFloor, camMaxShare);
        roll *= camLift;
        yaw *= camLift;
        pitchFrom *= camLift;
        pitchTo *= camLift;

        // (ii) NOT A MIRROR. Roll and yaw are each ONE pair fact and land the identical value at
        // both middle points by construction, so the outbound pose and the return pose of either
        // one, if left alone, are exactly each other's reflection — the mirror the ban names. The
        // return point is scaled down by a fraction read off the two works rather than left equal
        // to the outbound one: for roll, how closely the two works' own lattice PITCH agrees
        // (`latticePx`, the same field roll's own sign is already folded from), so two gratings cut
        // near the same scale return most of the excursion and two cut far apart return little of
        // it; for yaw, the ARRIVING work's own gate place, unread by yaw until now — yaw has always
        // read only the departing work's slot, the identical one-work-only defect the charter names
        // for the woven bridge a few screens above, so the return leg now answers to the work the
        // passage is actually arriving at. Pitch already differs at its own two points by
        // construction (two different horizons), so it is left as computed; the one coincidence
        // where two different works' horizons still land the same reading falls back to the two
        // works' own TONE share, the identical reading `span` above already turns to for the same
        // reason.
        var rollFraction = 1;
        if (cmf.latticePx > 0 && cmt.latticePx > 0) {
          rollFraction = Math.min(cmf.latticePx, cmt.latticePx)
            / Math.max(cmf.latticePx, cmt.latticePx);
        }
        var yawFraction = clamp01(cmt.gatePlace);
        var rollOut = 0, rollIn = 0, yawOut = 0, yawIn = 0, pitchOut = 0, pitchIn = 0;
        if (camAxis === "roll") {
          rollOut = roll;
          rollIn = roll * rollFraction;
        } else if (camAxis === "yaw") {
          yawOut = yaw;
          yawIn = yaw * yawFraction;
        } else {
          pitchOut = pitchFrom;
          pitchIn = pitchTo;
          if (pitchOut === pitchIn && pitchOut !== 0) {
            var camLvlSum2 = cmf.level + cmt.level;
            pitchIn = pitchOut * (camLvlSum2 > 0 ? cmf.level / camLvlSum2 : 0.5);
          }
        }
        // (iii) DIFFERENT SHARES OF THE PASSAGE is `span` above, at the top of this block — the
        // travelling cue's own asymmetric window, or the two works' own tone split where there is
        // none. Nothing here moves it a second time.
        camera.track[1].roll = flt(r4(rollOut));
        camera.track[2].roll = flt(r4(rollIn));
        camera.track[1].yaw = flt(r4(yawOut));
        camera.track[2].yaw = flt(r4(yawIn));
        camera.track[1].pitch = flt(r4(pitchOut));
        camera.track[2].pitch = flt(r4(pitchIn));
      }

      var world = null;
      if (tpl.middle.kind === "world" && num(toP.world) >= 0) world = WORLDS[num(toP.world)];
      var said = realiseIntent(tpl, row, axis, arrival, fromP, toP, cutKinds, pivotKind,
                               pivotMeasure, world);

      return {
        schema: SCHEMA,
        id: "sceneplan-v1/" + key,
        pair: { a: aId, b: bId },
        direction: direction,
        seed: row[4],
        tier: tpl.tier,
        duration: duration,
        pivot: { kind: pivotKind, measure: pivotMeasure, cut: cut, transform: transform,
                 elementKind: elementKind, value: { strength: row[2] }, held: true },
        travellingAxis: axis,
        actors: actors,
        arrival: arrival,
        middle: world ? { kind: "world", world: world } : tpl.middle,
        cues: cues,
        camera: camera,
        doors: { from: fromId, to: toId },
        quality: tpl.quality,
        interruption: tpl.interruption,
        failLand: tpl.failLand,
        readiness: row[5],
        register: REGISTERS[num(row[15])],
        intent: said[0],
        intentDropped: said[1],
        provenance: PROVENANCE
      };
    }

    function realiseIntent(tpl, row, axis, arrival, fromP, toP, cutKinds, pivotKind, pivotMeasure,
                           world) {
      var locus = arrival.locus || [0, 0];
      var aCount = 0, bCount = 0;
      cutKinds.forEach(function (k) {
        aCount += fromP.counts[k] === undefined ? 0 : fromP.counts[k];
        bCount += toP.counts[k] === undefined ? 0 : toP.counts[k];
      });
      var fields = {
        roadPhrase: ROAD_PHRASES[tpl.road] === undefined ? "" : ROAD_PHRASES[tpl.road],
        returnPhrase: tpl.passIndex
          ? RETURN_PHRASE.replace("{passIndex}", String(tpl.passIndex)) : "",
        pivotName: PIVOT_NAMES[pivotMeasure || pivotKind] || "shared ground",
        pivotStrength: row[2],
        arrival: ARRIVAL_PHRASES[arrival.mode],
        locusPhrase: LOCUS_PHRASES[arrival.locusKind]
          .replace("{locusX}", pyText(locus[0])).replace("{locusY}", pyText(locus[1])),
        aCount: aCount,
        bCount: bCount
      };
      if (axis !== null && axis.from && axis.to) {
        fields.axisName = AXIS_NAMES[axis.measure];
        fields.fromValue = axis.from[0];
        fields.toValue = axis.to[0];
        if (axis.measure === "radial") {
          fields.centrePhrase = ", with the camera panning so the meeting point travels from "
            + pyText(axis.from[1]) + ", " + pyText(axis.from[2]) + " to " + pyText(axis.to[1])
            + ", " + pyText(axis.to[2]);
        } else {
          fields.centrePhrase = "";
        }
      }
      if (world) fields.worldName = WORLD_NAMES[world];
      fields.registerPhrase = REGISTER_PHRASES[REGISTERS[num(row[15])]];
      // THE LINE IS FITTED TO THE FENCE IT HAS TO PASS, and it always fits. The client refuses a
      // score whose intent runs past its own cap WHOLE, with «intent is no short text». The line is
      // prose and its length is bounded above by nothing in this file, so an unbounded field against
      // a fixed cap refuses whenever it exceeds it — crossings are lost for as long as the cap is a
      // wall, and raising the cap moves the wall rather than taking it
      // down. So the line gives up its clauses in the order of what
      // a person can most afford to lose — the pass count, then the genre's own opening — and where
      // it still runs long it is TRIMMED at a word with an ellipsis. What was given up stands on the
      // plan, so a shortened line can always be read back to what it lost.
      var dropped = [], line = fill(tpl.intent, fields);
      if (line.length > INTENT_FENCE_CHARS && fields.returnPhrase) {
        fields.returnPhrase = "";
        dropped.push("returnPhrase");
        line = fill(tpl.intent, fields);
      }
      if (line.length > INTENT_FENCE_CHARS && fields.roadPhrase) {
        fields.roadPhrase = "";
        dropped.push("roadPhrase");
        line = fill(tpl.intent, fields);
      }
      if (line.length > INTENT_FENCE_CHARS) {
        var cut = line.slice(0, Math.max(0, INTENT_FENCE_CHARS - 1));
        var at = cut.lastIndexOf(" ");
        if (at > 0) cut = cut.slice(0, at);
        line = cut + "…";
        dropped.push("tail");
      }
      return [line, dropped];
    }

    function planDurationMs(plan) {
      if (typeof plan.duration === "number" || isFlt(plan.duration)) {
        return roundToInt(num(plan.duration));
      }
      var ends = [];
      (plan.cues || []).forEach(function (cue) {
        if (Array.isArray(cue.window) && cue.window.length === 2) ends.push(num(cue.window[1]));
      });
      if (!ends.length) return null;
      return roundToInt(Math.max.apply(null, ends) * 1000);
    }

    function serialise(plan) {
      // §4.7's mapping: every field §4.4 lists travels across unchanged, the four plan-only cue
      // fields stay behind, and the plan's id becomes the score's provenance source.
      // NEITHER OF THESE TWO REFUSALS CAN STAND ANY MORE, and neither needs to. A plan naming no
      // duration and no window is the instant §2.5 calls a legal transition, and a direction the
      // table does not map is the departing-to-arriving direction every passage runs by default.
      // Both were refusals of a well-formed plan, which is a crossing the visitor never saw for the
      // sake of a field.
      var duration = planDurationMs(plan);
      if (duration === null) duration = 0;
      var direction = plan.direction === "b->a" ? "b-to-a" : "a-to-b";
      var cues = plan.cues.map(function (cue) {
        var out = {};
        Object.keys(cue).forEach(function (k) {
          if (PLAN_ONLY_CUE_FIELDS.indexOf(k) < 0) out[k] = copy(cue[k]);
        });
        return out;
      });
      var camera = {};
      Object.keys(plan.camera || {}).forEach(function (k) {
        if (CAMERA_ALLOWED.indexOf(k) >= 0) camera[k] = copy(plan.camera[k]);
      });
      return [{
        schema: 2,
        intent: plan.intent,
        pair: copy(plan.pair),
        seed: plan.seed,
        duration: duration,
        direction: direction,
        interruption: copy(plan.interruption),
        failLand: plan.failLand,
        camera: camera,
        cues: cues,
        quality: copy(plan.quality),
        provenance: { source: plan.id,
                      measuredAt: (plan.provenance || {}).measuredAt,
                      by: (plan.provenance || {}).by }
      }, null];
    }

    // THE SCORE FITTED TO THE CLIENT'S OWN WEIGHT FENCE. Nothing that decides how the crossing
    // LOOKS is ever given up first: what goes is prose, in the order a person can most afford to
    // lose it — the per-node provenance notes, which say where a number came from and are read on
    // the diagnostic surface rather than by the eye, and then the authored line's tail. A score with
    // no fence published is left exactly as it was composed.
    function fitTheWeight(score) {
      if (!SCORE_FENCE_BYTES) return null;
      if (writeJsonTight(score).length <= SCORE_FENCE_BYTES) return null;
      var shed = [];
      (score.cues || []).forEach(function (c) {
        Object.keys(c.nodes || {}).forEach(function (n) {
          if (c.nodes[n] && c.nodes[n].note !== undefined) {
            delete c.nodes[n].note;
            shed.push("note:" + c.id + "." + n);
          }
        });
      });
      if (writeJsonTight(score).length <= SCORE_FENCE_BYTES) return shed;
      // THE LINE IS TRIMMED NEXT, because it is the one part of a score a person actually reads.
      var over = writeJsonTight(score).length - SCORE_FENCE_BYTES;
      if (typeof score.intent === "string" && score.intent.length > over) {
        var cut = score.intent.slice(0, Math.max(0, score.intent.length - over - 1));
        var at = cut.lastIndexOf(" ");
        if (at > 0) cut = cut.slice(0, at);
        score.intent = cut + "…";
        shed.push("intent");
      }
      if (writeJsonTight(score).length <= SCORE_FENCE_BYTES) return shed;
      // ONE RUNG LEFT BEFORE REFUSAL (2026-08-19). `op`/`points` were the one part of a score every
      // earlier rung left untouched, so a score that tripped the fence on its own SHAPE lost
      // everything rather than losing its shape gracefully. `fillPlan`'s own three-point middle
      // spline (charter shelf 3's room, "belonging to neither work") already falls back to a plain
      // two-point `op: "map"` whenever the pair's own record cannot honestly supply a middle — see
      // the `else` beside the spline a few screens up — so that two-point shape is one the fence
      // already tolerates on every score that never grew a middle in the first place. A spline still
      // standing here sheds to the SAME shape, reusing its own two ends (its first and last point,
      // untouched) and the same door rule the fill used to pick its shape in the first place: rising
      // eases `in`, falling eases `out`, unchanged holds `smooth`. Nothing is invented — the rule and
      // the two values both already lived on the node being shed.
      (score.cues || []).forEach(function (c) {
        Object.keys(c.nodes || {}).forEach(function (n) {
          var node = c.nodes[n];
          if (!node || node.op !== "spline" || !Array.isArray(node.points)
              || node.points.length < 2) {
            return;
          }
          var a = node.points[0].value, b = node.points[node.points.length - 1].value;
          var na = num(a), nb = num(b);
          var shape = na === nb ? "smooth" : (nb > na ? "in" : "out");
          // Shed to the SAME two-point shape the fill writes when a pair carries no middle, which is
          // a `map` over the two ends and not a `mix` — for the reason stated there: a `mix` reads
          // its ends as nodes and a marked float is not one, so a shed spline would have come out
          // silent on exactly the scores that were already heaviest.
          c.nodes[n] = {
            op: "map",
            in: { op: "curve", name: shape, in: { source: "cueProgress" } },
            from: [0, 1], to: [a, b] };
          shed.push("spline:" + c.id + "." + n);
        });
      });
      return shed;
    }

    // ---- the choice core: two works, a direction and a die ----

    function scoreFor(a, b, direction, seed, role, memory, played, viewer, routeFn, day, roadPlayed,
                      miraclesPlayed) {
      // Two works, a direction, the step's role, what the visit already played here and a die: the
      // whole crossing, decided here and now.
      //
      // AND WHAT THE WALK HAS ALREADY PLAYED ELSEWHERE. `played` is the letters of the passages
      // behind this one, most recent first (charter shelf 16's cooldowns, `coolOf` above). It is set
      // for the length of this one composition and read by every die struck inside it — the
      // ground, the instrument cast — so the whole choice answers to one reading of the walk
      // rather than to several. It is derived wholly from the request, so a request composed twice
      // still answers twice the same.
      //
      // AND THE SAME WALK, ROADS ONLY. `roadPlayed` is `01a-pass.js`'s second reading of it
      // (`passWalkGenres`, 2026-08-26 night-run separation, `coolOfRoad` above) — never mixed with
      // `played`, because `played` can carry an instrument's name and a road can share its spelling
      // (`kaleidoscope` is both). `pickGenre` is the one die that reads it; every other die inside
      // this composition still reads `played`/`walkPlayed` exactly as it always has.
      //
      // AND THE SAME WALK, STRONG MOVES ONLY. `miraclesPlayed` is `01a-pass.js`'s third reading of
      // it (`passWalkMiracles`, naряд S-18, 2026-08-27) — the walk's own log of which fold has
      // already spent the crossing's one miracle on this visit, never mixed with `played` or
      // `roadPlayed` for the same reason those two are kept apart: a fold's name is also a letter,
      // and mixing the two would make `spendsTheMiracle` cool on plays that were never the miracle.
      //
      // AND WHAT THE VISIT REMEMBERS OF ITSELF. `viewer` is charter shelf 16's fourth pipeline step
      // (`viewerBiasOf` above) — set fresh here for the length of this one composition exactly as
      // `walkPlayed` is, never accumulated in this file. Its absence (no field on the request) reads
      // as a visit with no memory of itself yet, which is the neutral case every die already answers
      // the same way it always has.
      walkPlayed = Array.isArray(played) ? played : [];
      walkPlayedDistinct = dedupeMostRecent(walkPlayed);
      roadPlayedDistinct = dedupeMostRecent(Array.isArray(roadPlayed) ? roadPlayed : []);
      walkMiracles = Array.isArray(miraclesPlayed) ? miraclesPlayed : [];
      viewerMemory = viewer || null;
      // AND THE INSTANT THE VISIT IS HAPPENING AT — charter shelf 16's third pipeline step, set
      // fresh here for the length of this one composition exactly as the two lines above are. Its
      // absence reads as a visit that stated no day, which is the neutral every die already answers
      // the same way, and it is what makes a pinned seed reproduce a run: every input the
      // composition reads is now on the request.
      visitClock = (typeof day === "number" && day === day && isFinite(day)) ? day : null;
      var tag = direction === "b-to-a" ? "ba" : "ab";
      var key = a.id + "__" + b.id + "__" + tag;
      var fromW = tag === "ab" ? a : b, toW = tag === "ab" ? b : a;
      var step = ROLE_BUDGETS[role] ? role : "middle";
      // THE STEP'S OWN HARMONIC FUNCTION, defaulted here as well as at the entry so both roads
      // answer alike. A direct four-value call to this function states no function and gets the
      // one its own defaulted role is the image of, which is what every passage read before the
      // field existed; the entry's fence has already held a stated one to the three.
      var stepFn = ROUTE_FUNCTIONS.indexOf(routeFn) >= 0 ? routeFn : FUNCTION_OF_ROLE[step];
      // Whether this step of the walk may spend the one miracle at all — shelf 17's budget, read
      // once here so the ground, the roads and the voicing all answer to one reading of it.
      var spendsAMiracle = !!ROLE_BUDGETS[step].miracle;
      var chosen = genreFor(fromW, toW, step, memory || null, seed, key);
      var dir = tag === "ab" ? "a-to-b" : "b-to-a";
      var tried = [], made = null, pair = null, ran = null, i3;
      // THE GENRES ARE WALKED BEST-SUITED FIRST AND THE FIRST ONE COMPOSES, because `compose` has no
      // road out any more: it always returns a plan. The loop stands because the ORDER is still a
      // ranking and a later lane may give a genre something it cannot carry; where every genre in
      // the vocabulary somehow answered with nothing, the ground genre composes last and its plan
      // is what plays.
      for (i3 = 0; i3 < chosen.order.length; i3++) {
        ran = chosen.order[i3];
        pair = pairOf(a, b, dir, seed, ran.free, ran.ground, !spendsAMiracle);
        made = compose(key, pair, fromW, toW, ran, step, memory || null);
        if (made[0] !== null) break;
        tried.push({ road: ran.id, why: made[1] });
      }
      chosen.road = ran;
      var plan = made[0];
      // WHICH OF A WORK'S OWN CUTS ACTS. Nothing recorded on this edge leaves it exactly where it
      // has always been; a further pass moves it by the die and the pass count, which is §4.8's
      // «the element selection may differ».
      //
      // A REVISITED WORK BECOMES A RECURRING CHARACTER (charter shelf 16's fourth step, the other
      // half of it). §4.8's pass count answers for repeats of ONE edge; `recurrence` answers for a
      // work the visit has already shown on a DIFFERENT edge entirely — `viewerMemory.seenWorks`,
      // read live off the request and never held here, is simply how many times each of this pair's
      // two ids already appears in what the visit has shown. A work meeting the visit again therefore
      // shows another of its own facets rather than the one it showed last time, by the same
      // mechanism a repeated edge already uses — one rule for both, exactly as §4.8's own kinship
      // step already reads a return and a repeat as one rule. A work the visit has not shown before
      // reads at 0, which is the plain unrecurring case exactly as it always was.
      var recurrence = countIn(viewerMemory && viewerMemory.seenWorks, fromW.id)
                      + countIn(viewerMemory && viewerMemory.seenWorks, toW.id);
      var cast = (plan.passIndex || recurrence)
        ? plan.passIndex + recurrence + dieAmong(seed, key + "|actors", 97) : 0;
      var tpl = buildTemplate(plan.shape, plan.spec);
      var row = rowOf(plan);
      var pv = plan.pivot;
      var ctx = {
        pivot: [pv.kind, pv.measure, pv.cut, pv.transform, pv.elementKind, pivotKindsOf(pv)],
        fromParts: workParts(fromW, cast),
        toParts: workParts(toW, cast),
        // THE STEP'S OWN PLACE IN THE WALK, carried into the fill because the crest law needs it
        // there (charter shelf 15, the culmination's suspension). `ctx` is what this file already
        // hands the fill; nothing new is built to carry two words across one call.
        role: step,
        routeFunction: stepFn
      };
      var filled = fillPlan(key, row, tpl, ctx);
      // THE FAMILY THE WALK WILL READ, read the same way the walk reads it: off the composed plan,
      // by the transform the pivot's cut implies and the measure the passage travels. It is handed
      // back here so the walk's edge record and this file's own kinship step name one thing.
      chosen.family = familyToken(filled.pivot.transform,
                                  filled.travellingAxis ? filled.travellingAxis.measure : null);
      var out = serialise(filled);
      // THE LAST FIELD A SCORE EVER GAINS IS WRITTEN BEFORE THE SCORE IS WEIGHED. A score is
      // weighed after the last field that will ever be written to it, or not at all: `fitTheWeight`
      // below tightens the score and `overTheFence` reads the tightened bytes, so a field added
      // after them leaves the published weight, the published text, the fence reading and the
      // record of what was shed all answering for a score the caller never receives. `passageFor`
      // wrote this one there, past the weighing, and while the client reads the weight rather than
      // enforcing it that costs a lying diagnostic; the day the fence is a wall again it costs a
      // crossing.
      //
      // WHAT THE READING IS, unchanged from the entry that used to hold it. `camera.lead` says the
      // flight itself is the transition: the anchor gives up its held middle and the pose travels
      // the whole duration. Its two homes are the quiet link and the return, which charter shelf 15
      // makes tonic and shelf 17 gives one move, at most one accompanying voice and no miracle — the
      // register a led passage wants underneath it, because the camera is the world voice and a led
      // flight spends it. The pair's own records have to give the flight somewhere to go, since a
      // still flight leads nothing. And under the levels law one voice holds one level, so a led
      // score may never also give a cue the WORLD level. All three readings are in hand here.
      var cameraTravels = plan.spec.travel === null && plan.spec.arrival === null;
      if (out[0] && cameraTravels && LED_ROLES.indexOf(step) >= 0 && !claimsTheWorld(out[0])) {
        out[0].camera.lead = true;
      }
      // THE SCORE IS FITTED TO THE CLIENT'S OWN WEIGHT FENCE, never handed over to be thrown away.
      // The client refuses a score over its published byte fence WHOLE, before any instrument sees
      // it, and a score's weight is dominated by prose whose length is bounded above by nothing —
      // the provenance note on every driven node, and the authored line. A whole score can therefore
      // be lost to prose, which follows from those two rules together and from no set of pictures:
      // the
      // provenance note on every driven node, and the authored line. So where a filled score stands
      // over the fence the notes go first, then the line is trimmed, until it fits. What was given
      // up stands beside it, so a fitted score can always be read back to what it lost.
      var shed = fitTheWeight(out[0]);
      var text = writeJson(out[0], 0);
      var tight = writeJsonTight(out[0]);
      return { key: key, score: out[0], json: text, bytes: tight.length,
               weightShed: shed,
               overTheFence: SCORE_FENCE_BYTES ? tight.length > SCORE_FENCE_BYTES : false,
               shape: plan.shape, plan: filled, version: COMPOSER_VERSION,
               // The derivation's own reading, for the diagnostic surface and for the walk's edge
               // record: which genre this passage ran on and how well it suited the pair, the whole
               // vocabulary ranked, what each genre read, and every shaping the crossing took.
               road: plan.road, genre: plan.genre, genreFit: plan.genreFit,
               ranking: chosen.ranking, stood: plan.stood,
               family: chosen.family, roads: chosen.qualified,
               roadNotes: chosen.notes, roadReach: chosen.reach,
               heldFamily: chosen.heldFamily, heldBy: chosen.heldBy, capped: plan.capped,
               roadDeclines: tried, miracleDecline: plan.miracleDecline,
               travelDecline: plan.travelDecline,
               // HOW FAR THIS PAIR'S OWN RECORDS SEND THE FLIGHT. The dolly comes from the two
               // works' measured door steps and the pan from their measured radial centres or the
               // arriving work's locus, so this is a reading of the pair and not a preference. It
               // is published as a reading, and it decides nothing.
               //
               // `cameraReach` gives the dolly as a share of its own bound so it survives a change
               // of unit in the camera flight section, which is another lane's half of this file.
               cameraReach: [r4(Math.abs(num(plan.camera.logScale)) / DOLLY_CAP),
                             r4(Math.hypot(
                               num(plan.camera.panTo[0]) - num(plan.camera.panFrom[0]),
                               num(plan.camera.panTo[1]) - num(plan.camera.panFrom[1])))],
               // WHETHER THE FLIGHT IS THE ONLY THING LEFT TO BE THE TRANSITION. A typed 0.1 stood
               // here — how far across the frame a flight had to travel before it could carry a
               // passage by itself — and it was this seat's own invention with no requirement of
               // his behind it. The plan already answers the question outright: a crossing whose
               // only cue is its held ground has NOTHING but the camera to be the transition, and
               // one that travels or arrives has the instruments underneath it. That reads the
               // passage rather than a number, and it needs no number at all.
               cameraTravels: cameraTravels };
    }

    // ---- THE ONE ENTRY A PASSAGE COMES THROUGH ----
    //
    // Every edge of the walk asks this one question, and `scoreFor` above is its inner core: the
    // request is read, defaulted and fenced here, and the four values the core has always taken are
    // handed on unchanged. Byte equality against the shipped score is preserved by construction —
    // a request carrying only the two records, a direction and a seed reaches `scoreFor` with
    // exactly those four values.
    //
    // THE REQUEST, field by field, with what a missing value means.
    //   workRecordA   the departing work's own record (§4.4c's per-work half). Required; absent is
    //                 a refusal, because there is no pair without it.
    //   workRecordB   the arriving work's record. Required, for the same reason.
    //   direction     "a-to-b" or "b-to-a" — the two distinct passages of one edge. Missing reads
    //                 as "a-to-b", which is the core's own rule.
    //   seed          the die, a number inside the span the meshing instrument publishes for its
    //                 own seed handle, fixing every random choice. Missing means the
    //                 walk rolled none and the passage runs on 0 — reproducible, which is the
    //                 judging mode of charter shelf 16.
    //   routeRole     the step's function in the walk's dramaturgy: entrance, quiet link, middle,
    //                 culmination or return (charter shelf 15 maps these onto the harmonic
    //                 functions — a quiet link and a return are tonic, an entrance and a middle
    //                 subdominant, a culmination dominant). Missing means the walk stated no
    //                 function and the passage is read as a middle; a name outside the five reads
    //                 as a middle too, with the unknown name recorded on the request.
    //   routeFunction the harmonic function that role is the image OF: tonic, subdominant or
    //                 dominant. It is on the request because the NAME alone cannot carry it — a
    //                 subdominant and a non-crest dominant are both called a middle — and those two
    //                 are the pair the composer most needs apart: one prepares, the other is a
    //                 tension that demands resolution. Missing means the walk stated no function
    //                 and it is read off the role by shelf 15's own map above, which is exactly how
    //                 every passage read before the field existed; a name outside the three reads
    //                 the same way, with the unknown name recorded on the request.
    //   sessionMemory the return reference of §4.8 — {family, seed, passIndex} naming the pass
    //                 already played on this edge in this visit, and nothing wider. Missing means
    //                 nothing has played on this edge yet. A field outside the three is IGNORED and
    //                 recorded: §4.8's fence keeps the walk's own edge record on the site's side of
    //                 the line, and it does that by not reading the field rather than by refusing
    //                 the crossing.
    //   cameraState   the pose the camera rests in as the passage starts; the flight departs from
    //                 it. Missing means the walk stated no pose and the flight departs from the
    //                 score's own rest, which is what every passage does today.
    //   buffer        the canvas as it stands at this instant: {width, height, dpr, orientation,
    //                 quality}. Missing means the buffer is unstated; the instrument then reads the
    //                 one it is drawing on, which is the truth in either case (his 18:00 decision).
    //   viewerMemory  the visit's own memory of itself, charter shelf 16's fourth pipeline step —
    //                 {lingered, skipped, seenWorks}, each a plain list of names, and nothing wider.
    //                 Missing means the visit remembers nothing of itself yet, which is the neutral
    //                 case `viewerBiasOf` and the recurrence fold above both already answer the same
    //                 way. A field outside the three is IGNORED and recorded, exactly as
    //                 `sessionMemory`'s fence already works.
    //   day           the instant the walk casts this pair, in milliseconds since the epoch in UTC —
    //                 charter shelf 16's third pipeline step, from which the day's palette, tempo and
    //                 light are read (§4.4g, added 2026-08-26). Missing means the walk stated no day
    //                 and the day's bias reads neutral on every candidate, which is the judging mode:
    //                 the client sends it only on an UNPINNED visit, so a pinned walk reproduces to
    //                 the pixel and a public one breathes with the day. A value that is no instant is
    //                 left unread and recorded, like every other field here.
    //
    // WHAT COMES BACK, AND IT IS ALWAYS A CROSSING. Two refusals stand in this entry and only two:
    // a request naming no departing record and one naming no arriving record, because there is no
    // PAIR without two photographs and nothing to compose between. Every other field that used to be
    // refused by name — a route role outside the five, a die outside the instrument's own span, a
    // session memory naming a fourth field — is now DEFAULTED, and what was read stands on the
    // request beside `unread`, so a walk that sends a stray value can still be found and fixed
    // without the visitor paying for it with a plain slide.
    //
    // On success: everything `scoreFor` hands back plus `request` — the request as it was read,
    // defaults filled in — and `applied`, which starts null. `applied` is the instrument's own
    // reading of the buffer it drew on, and it can only be known after the frame is drawn: the
    // caller writes it onto this record when the host reports, so one record carries the whole
    // passage — what was asked, what came back, and what was applied or refused mid-flight.
    var ROUTE_ROLES = ["entrance", "quiet link", "middle", "culmination", "return"];
    // THE THREE HARMONIC FUNCTIONS THE FIVE NAMES ARE THE IMAGE OF (charter shelf 15), and the one
    // home of that vocabulary on this side of the line. The client writes `routeFunction` beside
    // `routeRole` and has done since the harmonic layer landed; this file contained no occurrence
    // of the identifier at all, so the one distinction that layer was built to make was dropped
    // silently at the seam, with no diagnostic saying it had been.
    //
    // WHY THE NAME CANNOT CARRY IT. The map from a function to a name is not one-to-one: a
    // subdominant is always called a middle, and so is a dominant that does not stand at the
    // route's own crest (`passRoleOfFunction` in engine/client/01a-pass.js). So the two the
    // composer most needs apart — a preparation and a tension that demands resolution — both
    // arrive here under one word.
    var ROUTE_FUNCTIONS = ["tonic", "subdominant", "dominant"];
    // AND THE MAP THE OTHER WAY, which is what a step whose function goes unstated is read by. It
    // is not a new reading: it is shelf 15's own map, already written out word for word in the
    // request's own field list below — a quiet link and a return are tonic, an entrance and a
    // middle subdominant, a culmination dominant. A walk that states no function therefore reads
    // exactly as it read before this fence existed, which is the whole of what «missing means
    // unstated» has to mean here.
    var FUNCTION_OF_ROLE = { "entrance": "subdominant", "quiet link": "tonic",
                             "middle": "subdominant", "culmination": "dominant",
                             "return": "tonic" };
    // The two steps of the walk a camera-led passage belongs to, and the one home of that reading.
    var LED_ROLES = ["quiet link", "return"];

    // Does any cue of this score claim the world level? Under the levels law the world is the
    // camera's own, so a led flight and a world-level cue are two voices on one level.
    function claimsTheWorld(score) {
      var i, levels;
      for (i = 0; i < (score.cues || []).length; i++) {
        levels = score.cues[i].levels || [];
        if (levels.indexOf("WORLD") >= 0) return true;
      }
      return false;
    }
    var SESSION_MEMORY_FIELDS = ["family", "seed", "passIndex"];
    var VIEWER_MEMORY_FIELDS = ["lingered", "skipped", "seenWorks"];
    // The span the die is rolled inside, and the one home of that fact on this side of the line.
    // It is the meshing instrument's own `seed` handle span, read out of its manifest rather than
    // written down here, so a copy of it cannot go stale. The walk reads it back off this module.
    var SEED_SPAN = [MANIFESTS.gears.handles.seed.min, MANIFESTS.gears.handles.seed.max];

    function passageFor(request) {
      var req = request || {};
      var a = req.workRecordA, b = req.workRecordB;
      var role = req.routeRole === undefined || req.routeRole === null ? "middle" : req.routeRole;
      var direction = req.direction === "b-to-a" ? "b-to-a" : "a-to-b";
      var seed = req.seed === undefined || req.seed === null ? 0 : Number(req.seed);
      var memory = req.sessionMemory === undefined ? null : req.sessionMemory;
      var key = (a && a.id ? a.id : "?") + "__" + (b && b.id ? b.id : "?")
                + "__" + (direction === "b-to-a" ? "ba" : "ab");
      var unread = [];
      // A ROUTE ROLE OUTSIDE THE FIVE READS AS A MIDDLE, which is what a stated-nothing role has
      // always read as. The vocabulary still cannot drift — the composer answers to the five and
      // nothing else — and the stray name is recorded rather than charged to the visitor.
      if (ROUTE_ROLES.indexOf(role) < 0) {
        unread.push("routeRole «" + String(role) + "», which is none of " + ROUTE_ROLES.join(", ")
                    + ", so the step reads as a middle");
        role = "middle";
      }
      // THE STEP'S HARMONIC FUNCTION, FENCED THE WAY ITS OWN NAME ALREADY IS. It is read, it is
      // held to the three, and a stray value is RECORDED rather than charged to the visitor — the
      // same road `routeRole`, the die and the two memories all take, because a walk that sends a
      // value nobody expected must still get a crossing. Where the walk states nothing the role's
      // own function stands, so this fence changes no passage that was composing before it.
      var routeFn = req.routeFunction === undefined || req.routeFunction === null
        ? null : String(req.routeFunction);
      if (routeFn !== null && ROUTE_FUNCTIONS.indexOf(routeFn) < 0) {
        unread.push("routeFunction «" + routeFn + "», which is none of "
                    + ROUTE_FUNCTIONS.join(", ") + ", so the step's function is read off its role");
        routeFn = null;
      }
      if (routeFn === null) routeFn = FUNCTION_OF_ROLE[role];
      // A DIE OUTSIDE THE INSTRUMENT'S OWN SPAN IS WRAPPED INTO IT. The span is the meshing
      // instrument's own published one and it holds; a walk that rolls past it gets a die inside it
      // rather than no crossing.
      if (seed !== seed || !isFinite(seed) || seed < SEED_SPAN[0] || seed > SEED_SPAN[1]) {
        var span = SEED_SPAN[1] - SEED_SPAN[0];
        var wrapped = (seed !== seed || !isFinite(seed)) ? SEED_SPAN[0]
          : (span > 0 ? SEED_SPAN[0] + (((seed - SEED_SPAN[0]) % span) + span) % span
             : SEED_SPAN[0]);
        unread.push("seed " + String(req.seed) + ", outside " + SEED_SPAN[0] + "…" + SEED_SPAN[1]
                    + ", so the die is rolled at " + wrapped);
        seed = wrapped;
      }
      // A SESSION MEMORY WIDER THAN §4.8'S THREE FIELDS HAS ITS EXTRA FIELDS LEFT UNREAD. The fence
      // does its whole job that way: nothing outside the three crosses the line, and the crossing
      // still plays.
      if (memory !== null) {
        if (typeof memory !== "object" || Array.isArray(memory)) {
          unread.push("a session memory that is no record, so nothing has played on this edge");
          memory = null;
        } else {
          var odd = Object.keys(memory).filter(function (f) {
            return SESSION_MEMORY_FIELDS.indexOf(f) < 0;
          });
          if (odd.length) {
            var kept = {};
            SESSION_MEMORY_FIELDS.forEach(function (f) {
              if (memory[f] !== undefined) kept[f] = memory[f];
            });
            unread.push("session memory field(s) «" + odd.sort().join("», «") + "», outside the "
                        + "three §4.8 lets cross: " + SESSION_MEMORY_FIELDS.join(", "));
            memory = kept;
          }
        }
      }
      // WHAT THE WALK HAS PLAYED SO FAR, most recent letter first — charter shelf 16's letter
      // cooldowns, read here and handed to the choice core. It is a plain list of NAMES: the genres
      // and the instruments the passages behind this one carried, which is what a person actually
      // sees repeat. A list is all it is; there is no second field to invent, and nothing in it
      // scales with the collection.
      //
      // A LIST OF ANYTHING BUT NAMES IS LEFT UNREAD rather than refused, exactly as every other
      // field of this entry is now: the crossing still plays. There is no length fence, and that is
      // deliberate — the list is bounded by the walk's own length, which is the walk's business, and
      // a number invented here to bound it a second time would be one of the numbers his 09:57 word
      // strikes as a class.
      var played = [];
      if (req.walkMemory !== undefined && req.walkMemory !== null) {
        if (!Array.isArray(req.walkMemory)) {
          unread.push("a walk memory that is no list, so the walk has played nothing yet");
        } else {
          var strayLetters = 0, wm;
          for (wm = 0; wm < req.walkMemory.length; wm++) {
            if (typeof req.walkMemory[wm] === "string" && req.walkMemory[wm]) {
              played.push(req.walkMemory[wm]);
            } else {
              strayLetters += 1;
            }
          }
          if (strayLetters) {
            unread.push(strayLetters + " walk-memory entr(y/ies) naming no letter");
          }
        }
      }
      // THE SAME WALK, ROADS ONLY — the 2026-08-26 night-run separation above `coolOfRoad`.
      // `walkMemory` mixes a road's own genre with every instrument its stack carried, and the two
      // vocabularies can share a spelling (`kaleidoscope` is both), so a road's cooldown cannot be
      // read off that mixed list by filtering names after the fact. `01a-pass.js`'s `passWalkGenres`
      // reads the road alone off each step, never the stack, so this can only ever name one of the
      // eight roads `genresFor` answers with — fenced exactly as `walkMemory` is, for the same
      // reason: a stray entry is recorded and the crossing still plays.
      var roadPlayed = [];
      if (req.walkGenres !== undefined && req.walkGenres !== null) {
        if (!Array.isArray(req.walkGenres)) {
          unread.push("a walk-genres list that is no list, so no road has played yet");
        } else {
          var strayRoads = 0, wg;
          for (wg = 0; wg < req.walkGenres.length; wg++) {
            if (typeof req.walkGenres[wg] === "string" && req.walkGenres[wg]) {
              roadPlayed.push(req.walkGenres[wg]);
            } else {
              strayRoads += 1;
            }
          }
          if (strayRoads) {
            unread.push(strayRoads + " walk-genres entr(y/ies) naming no road");
          }
        }
      }
      // THE SAME WALK, STRONG MOVES ONLY — naряд S-18 (2026-08-27). His word of 2026-08-26 20:17:
      // a miracle is a wow, a concept, it is subjective, and repeated it stops being one. So
      // `spendsTheMiracle` no longer reads a mark an instrument's own manifest carries for its
      // whole life on the site; it reads which fold this walk has already spent, exactly the shape
      // `walkMemory` and `walkGenres` already are — a plain list of NAMES, fenced the same way, for
      // the same reason: a stray entry is recorded and the crossing still plays.
      var miraclesPlayed = [];
      if (req.walkMiracles !== undefined && req.walkMiracles !== null) {
        if (!Array.isArray(req.walkMiracles)) {
          unread.push("a walk-miracles list that is no list, so no strong move has played yet");
        } else {
          var strayMiracles = 0, wmi;
          for (wmi = 0; wmi < req.walkMiracles.length; wmi++) {
            if (typeof req.walkMiracles[wmi] === "string" && req.walkMiracles[wmi]) {
              miraclesPlayed.push(req.walkMiracles[wmi]);
            } else {
              strayMiracles += 1;
            }
          }
          if (strayMiracles) {
            unread.push(strayMiracles + " walk-miracles entr(y/ies) naming no move");
          }
        }
      }
      // THE VISIT'S OWN MEMORY OF ITSELF — charter shelf 16's fourth pipeline step. Three named
      // lists and nothing else, fenced exactly as `sessionMemory` is above: a field outside the
      // three is dropped and recorded rather than refusing the crossing, and each list is a plain
      // list of NAMES (a letter for `lingered`/`skipped`, a work id for `seenWorks`) with no length
      // fence of its own, for the same reason `walkMemory` carries none — the visit's own length is
      // the visit's business.
      function readNameList(v, label) {
        var out = [], stray = 0, i;
        if (v === undefined || v === null) return { list: out, note: null };
        if (!Array.isArray(v)) {
          return { list: out, note: "a " + label + " that is no list, so it reads as empty" };
        }
        for (i = 0; i < v.length; i++) {
          if (typeof v[i] === "string" && v[i]) out.push(v[i]); else stray += 1;
        }
        return { list: out,
                 note: stray ? (stray + " " + label + " entr(y/ies) naming nothing") : null };
      }
      var viewer = null;
      if (req.viewerMemory !== undefined && req.viewerMemory !== null) {
        if (typeof req.viewerMemory !== "object" || Array.isArray(req.viewerMemory)) {
          unread.push("a viewer memory that is no record, so the visit remembers nothing of itself "
                      + "yet");
        } else {
          var oddV = Object.keys(req.viewerMemory).filter(function (f) {
            return VIEWER_MEMORY_FIELDS.indexOf(f) < 0;
          });
          if (oddV.length) {
            unread.push("viewer memory field(s) «" + oddV.sort().join("», «") + "», outside the "
                        + "three shelf 16 lets cross: " + VIEWER_MEMORY_FIELDS.join(", "));
          }
          var lingeredR = readNameList(req.viewerMemory.lingered, "lingered");
          var skippedR = readNameList(req.viewerMemory.skipped, "skipped");
          var seenR = readNameList(req.viewerMemory.seenWorks, "seenWorks");
          [lingeredR, skippedR, seenR].forEach(function (r) { if (r.note) unread.push(r.note); });
          viewer = { lingered: lingeredR.list, skipped: skippedR.list, seenWorks: seenR.list };
        }
      }
      // THE DAY THIS VISIT HAPPENS ON — charter shelf 16's third pipeline step, read here and handed
      // to the choice core exactly as the walk memory and the viewer memory are. It is one number:
      // the instant, in milliseconds since the epoch in UTC, that the day and the hour are read off.
      // A walk that states none states none, and the day's bias reads at its own neutral — which is
      // the viewer mode where the walk rolls a fresh die anyway, and the judging mode where a pinned
      // seed has to reproduce its predecessor to the pixel (§4.4f). The client already draws the line
      // there and not here: `engine/client/01a-pass.js` sets `req.day` only on an unpinned visit.
      //
      // THE FIELD IS `day`, WHICH IS THE CONTRACT'S OWN NAME FOR IT. The block this was applied from
      // called it `dayOfVisit`; it was written before §4.4g's row landed, and the row that landed
      // (PASS-API-V1.md, 2026-08-26) and the client that writes it both say `day`. The wire's name is
      // the one that binds, so a field this entry read under any other name would read nothing at all
      // on every request the client actually sends.
      //
      // A VALUE THAT IS NO INSTANT IS LEFT UNREAD RATHER THAN REFUSED, exactly as every other field
      // of this entry is: it is recorded, the day reads at its neutral, and the crossing plays.
      var day = null;
      if (req.day !== undefined && req.day !== null) {
        var dv = Number(req.day);
        if (dv !== dv || !isFinite(dv)) {
          unread.push("day «" + String(req.day) + "», which names no instant, so the day's own bias "
                      + "reads neutral on every candidate");
        } else {
          day = dv;
        }
      }
      var read = { routeRole: role, routeFunction: routeFn,
                   direction: direction, seed: seed, sessionMemory: memory,
                   walkMemory: played.length ? played : null,
                   walkGenres: roadPlayed.length ? roadPlayed : null,
                   walkMiracles: miraclesPlayed.length ? miraclesPlayed : null,
                   viewerMemory: viewer,
                   day: day,
                   cameraState: req.cameraState === undefined ? null : req.cameraState,
                   buffer: req.buffer === undefined ? null : req.buffer,
                   unread: unread.length ? unread : null };
      function no(why) {
        return { key: key, declined: why, score: null, request: read, applied: null,
                 version: COMPOSER_VERSION };
      }
      // THE ONLY TWO REFUSALS LEFT IN THIS FILE, and both say the same thing: there is no PAIR.
      // A request with one record names one photograph, and a crossing is between two.
      if (!a || !a.id) return no("the passage request names no departing work record");
      if (!b || !b.id) return no("the passage request names no arriving work record");
      var made = scoreFor(a, b, direction, seed, role, memory, played, viewer, routeFn, day,
                          roadPlayed, miraclesPlayed);
      // THE PASSAGE THE CAMERA LEADS IS DECIDED IN THE CHOICE CORE, where the score is still being
      // built. It stood here, after the core had already weighed the score and published its bytes,
      // its text and its fence reading, so those three answered for a score without this field on
      // it. The reading itself is unchanged and its whole argument travels with it; what changed is
      // that a score is now weighed after the last field it will ever gain.
      made.request = read;
      made.applied = null;
      if (made.declined !== undefined) made.score = null;
      else made.declined = null;
      return made;
    }

    // THE THREE PURE ARITHMETICS TRAVEL BESIDE THE ENTRY, and they are here for one reason: what
    // each of them claims is a claim about NUMBERS, so it can be answered over the whole span of
    // numbers it takes rather than over whichever photographs are on disk. `r4` and the two writers
    // already stood here on the same footing. Nothing in the client calls the three below; they are
    // the module handing out its own arithmetic so a reader can put every value through it.
    return { passageFor: passageFor, scoreFor: scoreFor, routeRoles: ROUTE_ROLES.slice(),
             seedSpan: SEED_SPAN.slice(),
             version: COMPOSER_VERSION, writeJson: writeJson,
             motionPeak: motionPeak,
             writeJsonTight: writeJsonTight, r4: r4,
             camVoiceFloor: camVoiceFloor, camVoiceLift: camVoiceLift,
             voiceFloor: voiceFloor, voiceReach: voiceReach, voiceLift: voiceLift,
             voiceLoudness: voiceLoudness,
             // THE LETTER COOLDOWN'S OWN ARITHMETIC (:2501-2531 above) — a claim about a place and
             // a pool size, and about a raw walk-memory list reduced to one, so a reader can put
             // every value either takes through it rather than trusting a route's own die.
             coolFactor: coolFactor, walkCooldown: walkCooldown,
             // The band each route role names for its own length, and the arithmetic that places a
             // pair's reading inside one. Both travel for the same reason as the rest of this list:
             // the claim they carry is about numbers, so it is answered over every number they take.
             // Shelf 17's six structural levels, so a reader can put every handle every instrument
             // publishes through them and find the one that declares a seventh.
             levels: LEVELS.slice(),
             // THE FOUR INSTRUMENTS `spendsTheMiracle` READS BY IDENTITY (naряд S-18, 2026-08-27),
             // so a reader can ask which fold this walk has already spent without keeping its own
             // second copy of the list this file already holds.
             worldFoldInstruments: WORLD_FOLD_INSTRUMENTS.slice(),
             // THE REGISTER'S OWN WORD FOR EVERY HANDLE, so a reader can hold what a row PROMISES
             // against what the composition actually wrote. That comparison is the one thing
             // nothing checked: a row saying `measured` and a node standing at the instrument's own
             // default is a broken promise, and it shipped in silence because the only gate over it
             // read the note the writer had already declined to write.
             handleSource: (function () {
               var out = {}, k;
               for (k in HANDLE_SOURCE) out[k] = HANDLE_SOURCE[k][0];
               return out;
             }()),
             lengthInBand: lengthInBand,
             roleBands: (function () {
               var out = {}, r;
               for (r in ROLE_BUDGETS) out[r] = bandOfTier(ROLE_BUDGETS[r].tier).slice();
               return out;
             }()),
             tierBands: (function () {
               var out = {}, i2;
               for (i2 = 0; i2 < TIERS.length; i2++) out[TIERS[i2].tier] = TIERS[i2].band.slice();
               return out;
             }()) };
  }

  join({ version: COMPOSER_VERSION, make: make });
})();
