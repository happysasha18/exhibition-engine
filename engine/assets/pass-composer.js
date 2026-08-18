/*!pass-composer.js*/
// The passage composer's choice core, in the browser — PASS-API-V1 §4.7 composed at show time.
//
// ROOT. His law of 2026-08-14 16:14 and his word of 2026-08-17 17:06: a pair's crossing is
// decided when the pair is shown, and the product carries no table of pairs. The site's
// lab/build-sceneplan-v1.py already holds the whole decision — the pivot, the travelling axis,
// the actors, the arrival, the voices, the levels, the camera and the two doors — and it holds it
// in stdlib arithmetic over records that describe ONE work each. This file is that decision,
// carried across a line: two per-work records and a seed in, the §4.4 score out, byte for byte
// what lab/sceneplan-to-score.py writes for the same pair.
//
// WHAT IT MEASURES: nothing. Every number it reads was measured once, per work, and written down.
// It opens no image, reads no clock and asks no network. The pair step is arithmetic over the two
// records, which is why it can run at the instant a walk casts the pair.
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

  var SCHEMA = 1;
  var CUE_IDS = ["pivot", "travel", "arrival"];
  var TRAVEL_AXES = ["banding", "dominant_object", "grid", "radial", "regions", "texture"];
  var LOCUS_KINDS = ["none", "pole", "horizon-seam", "gate"];
  var WORLDS = ["sphere", "corridor", "log-spiral"];
  var POLAR_WORLD = { planet: "sphere", tunnel: "corridor", twirl: "log-spiral" };
  var SUBTYPES = ["angular", "ring", "none"];
  var REGISTERS = ["none", "discovery", "provocation", "apparition"];
  var PIVOT_KINDS = ["shared-measure", "shared-rotational-order", "shared-palette-region",
                     "tonal-and-spectral-bridge"];
  var MEASURES = ["banding", "grid", "regions", "dominant_object", "texture", "radial",
                  "named_objects"];
  var SHARED_MEASURES = ["banding", "dominant_object", "grid", "named_objects", "radial",
                         "regions", "texture"];
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
  // The three pivots that are not a shared measure carry their cut, transform and element kind on
  // the pivot's own shape rather than on the pair.
  var PIVOT_SHAPES = {
    "shared-rotational-order": { cut: "wedges", transform: "gear_mesh", elementKind: "wedge" },
    "shared-palette-region": { cut: "colour_world", transform: "palette_handover",
                               elementKind: "band" },
    "tonal-and-spectral-bridge": { cut: "tonal_zones_and_detail_scales",
                                   transform: "zone_handover_and_scale_growth",
                                   elementKind: "band" }
  };
  var PIVOT_KINDS_OF_CUT = { "tonal-and-spectral-bridge": ["band", "scale"] };
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
  // WHERE SEVERAL CUT ON ONE KIND the choice is made the way the seven roads are chosen: from the
  // pair's own measurements first — each instrument states what a pair must read for it to be worth
  // casting — and from the die among whatever qualifies. The two panel instruments are genuinely
  // different acts and their measurements say so: folding into a solid is an impossible event that
  // spends the one miracle and claims the world, while opening into a parquet reveals the making and
  // claims no world at all, so a step whose role spends no miracle reaches the panel kind through
  // the unfold and through nothing else.
  var MISSING_INSTRUMENT = {
    tile: "an instrument that cuts on tiles, for tile_crossfade",
    panel: "an instrument that cuts on panels, for region_dissolve and object_reveal",
    region: "an instrument that cuts on named regions, for object_by_object",
    field: "an instrument that cuts on the whole frame, which is the degenerate element"
  };
  var KIND_OF_AXIS = { banding: "strip", radial: "ring", regions: "panel", grid: "tile",
                       texture: "scale", dominant_object: "panel" };
  var TIERS = [
    { tier: "quiet", letters: [1, 1], accompaniments: [0, 1], miracles: [0, 0], duration: 3000 },
    { tier: "middle", letters: [0, 2], accompaniments: [0, 2], miracles: [0, 1], duration: 6500 },
    { tier: "culmination", letters: [2, 3], accompaniments: [0, 3], miracles: [1, 1],
      duration: 11000 }
  ];
  // The three tiers in order, so a role can be asked whether a realised tier reaches it.
  var TIER_RANK = { quiet: 0, middle: 1, culmination: 2 };
  var TRANSACTION_MS = 14000;
  var DOOR_HOLD = 0.08;
  // How far the camera may come in or pull back on the score's own track, as a natural logarithm:
  // 0.5 bounds the approach at 1.65 times, and it bounds a magnification of the RENDERED canvas,
  // because the host applies the dolly as one transform over the buffer the instrument drew on.
  // Since 2026-08-17 it is a LIMIT the demand is compressed toward rather than a wall it is cut at;
  // `cameraFlight` below carries that and the measurement behind it.
  //
  // THE NUMBER IS UNMEASURED AND IT IS ON HIS LIST FOR GATE 1 (U27 stage 1, the camera lane,
  // 2026-08-17 22:2x). It was written when this field held a base-2 logarithm, so it bounded the
  // approach at 1.41 times and now bounds it at 1.65; and the measurement over the 121 works' own
  // door steps says no number here can be the honest bound. What the door framings ASK for has a
  // median of 2.05 times, a nine-tenths point of 6.44 and a worst of 86.3 — a smooth tail with no
  // knee to set a cap at — while what the FRAME can carry is the buffer's own oversampling,
  // min(dpr, 2) times the resolution step, which is 1.00 times on any dpr-1 frame and falls to 1.00
  // on a dpr-2 phone at the governor's floor. The bound is therefore a property of the device the
  // composer cannot see (his architecture decision of 18:00), and the defect the composer lane
  // measured — 63.9 per cent of ordered pairs landing on one number, so the approach carries no
  // reading of any pair — belongs to the CLIPPING rather than to this value. The report names the
  // repair and its numbers; nothing is guessed here in the meantime.
  var DOLLY_CAP = 0.5;
  // How far across the frame a flight has to travel before it can carry a passage by itself, said
  // as a share of the frame. Nothing measures it, and it is the one number deciding how many of a
  // route's quiet links and returns are camera-led — the revisit list carries it.
  var LEAD_SHARE = 0.1;
  var SIZE_FLOOR = 0.7;
  var CULMINATION_DISTANCE = 0.5;
  var LOCUS_NEAR = 0.1;
  var VOID_SHARE_FLOOR = 0.6;
  var LADDER_DISTANCE = 0.5;
  var READY_FLOOR = 0.12;
  var MOTIF_SEAM = "горизонт-шов";
  var MOTIF_GATE = "ворота";

  var HANDLE_SOURCE = {
    mix: ["transaction", "the pass's own progress, door to door"],
    clock: ["transaction", "the second the host hands down"],
    seed: ["measured", "the ordered pair's own seed"],
    strips: ["measured", "the pivot's band family, its measured count along the cut"],
    // WIDENED 2026-08-17 for the box: for the woven instrument `axis` is which way the ribbons run,
    // for the folding one it is which way the solid turns — the crease upright or lying flat. Both
    // derive from the one recorded banding axis, so the crease crosses the works' own structure
    // rather than being laid across it, and one row serves both because one measurement does.
    axis: ["measured", "the banding axis cut-lines.json recorded — which way the ribbons run, and "
                       + "which way the solid turns so its crease crosses that"],
    size: ["measured", "the two works' measured ring counts"],
    ratio: ["measured", "the two works' measured ring counts, on seven steps"],
    bandPeriod: ["measured", "the pivot's own period as a fraction of frame height"],
    centreX: ["measured", "the midpoint of the two measured radial centres"],
    centreY: ["measured", "the midpoint of the two measured radial centres"],
    shade: ["module-rest", "a judge channel the module rests at 1"],
    travel: ["module-rest", "a judge channel the module rests at 1"],
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
    speed: ["measured", "the strip count against the instrument's own default count, so one strip "
                        + "crosses one strip's width in the same time whatever the pair"],
    drift: ["measured", "the fractional part of the two works' measured spectral periods in "
                        + "ratio, charter shelf 13's incommensurate-period instrument"],
    tooth: ["measured", "how much finer each work's measured ring repeat is than the cut it was "
                        + "given, which is the relief a tooth stands in"],
    turn: ["measured", "each work's own measured radial score, so a work whose rings are its own "
                       + "device drives the mesh and one that barely reads radial barely turns"],
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
    depth: ["measured", "the departing work's own corridor reading, structure.polar.tunnel"],
    dip: ["measured", "the departing work's own measured horizon, structure.horizon.y"],
    lead: ["measured", "the finger count, read off its own range onto this one and turned over"],
    fingers: ["measured", "the departing work's repeat across the crease: its frame side over "
                          + "structure.grid.periodPx"],
    // THE ONE REAL GAP. Where along the turn the departing work falls into two regions is measured
    // in lab/cut-lines.py and STRIPPED before the engine sees it: a work record carries
    // structure.regions.count and .score and no position at all. So this file can hand no line. The
    // instrument keeps its own edge, and `seamScore` is handed under the instrument's own floor so
    // it says as much rather than folding on a line nobody measured — which is the first of the
    // charter's five box conditions, honestly unmet rather than quietly claimed.
    seam: ["unmeasured", "where the work's region line stands; the position is stripped before a "
                         + "record reaches the engine"],
    seamScore: ["measured", "structure.regions.score, handed at nothing while the line itself "
                            + "does not travel"],
    mask: ["module-rest", "a judge channel the module rests shut"],
    // THE WAVED RIBBON AND THE PARQUET, from the instruments lane's own manifests. No template names
    // these yet; the rows stand so a score that names them can be written, and so the register keeps
    // its promise that every handle says where it comes from. The wave's own two readings —
    // texture.type and texture.localStraightness — are stripped before the engine sees them, so the
    // composer can hand only nothing, which is the straight ribbon and the reference look.
    wave: ["measured", "texture.type at «рябь», with 1 - texture.localStraightness as the depth"],
    wavePeriod: ["measured", "texture.spectralPeriodPx over the work's own frame side"],
    waveDrift: ["measured", "the same spectral period, as a share of it travelled in a second"],
    field: ["transaction", "the passage's own travel, one envelope for the plane and the parquet"],
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
    flank: ["unmeasured", "how upright a tooth's flank stands. The work's own radial streak is "
                          + "measured in the polar block and reads on exactly this, but no scale "
                          + "between a streak reading and this handle is recorded, so the "
                          + "instrument's own default stands and the gap is named"]
  };

  // THE ROAD OPENS THE AUTHORED LINE. §4.7: the intent is the one written line a plan opens with,
  // naming this adventure and the shelves it draws from, and a generic line fails review by
  // definition. Under the plural-source law the first thing a person needs to know about a crossing
  // is which of the seven roads it took, so the road says so in its own words before the reading
  // that qualified it. The universal bridge opens with nothing, so a crossing that takes it reads
  // exactly as it read before the roads existed.
  var ROAD_PHRASES = {
    "shared-ground": "Along what the two works share. ",
    "spin": "The radial work turns. ",
    "kaleidoscope": "The rings open. ",
    "symmetry-slide": "The parts slide along the works' own symmetry. ",
    "stripes": "The two band families cross into stripes. ",
    "box-fold": "The work folds along its own region lines. ",
    "dissimilar-mystery": "Along what the two works do not share. ",
    "bridge": ""
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
    "tonal-and-spectral-bridge": "tonal zones and detail scales",
    "shared-palette-region": "shared palette region",
    "shared-rotational-order": "shared turn"
  };
  var AXIS_NAMES = {
    banding: "band family", dominant_object: "figure", grid: "tile grid",
    radial: "radial reading", regions: "region count", texture: "grain"
  };
  var ARRIVAL_PHRASES = { CARRIED: "carried by the gesture already running",
                          CONDENSED: "by condensing" };
  var LOCUS_PHRASES = {
    none: "", pole: " at its own pole {locusX}, {locusY}",
    "horizon-seam": " at its own horizon seam {locusX}, {locusY}",
    gate: " at its own gate {locusX}, {locusY}"
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
    var FLOORS = consts.floors;
    var THRESHOLDS = consts.thresholds;
    var PROVENANCE = consts.provenance;
    var SCORE_FENCE_BYTES = consts.scoreFenceBytes;
    // THE CLIENT'S OWN FENCE ON THE ONE FIELD §4.4 CALLS PROSE. A score whose intent runs past it is
    // refused WHOLE with «intent is no short text», so an intent nobody measured is a crossing
    // nobody sees: stage 0 found 1 004 of 6 304 composed crossings standing over the 400 the client
    // then applied, every one of them refused before an instrument saw it, and raised the client's
    // cap to 600. The number belongs to the client, and the engine's bake now publishes it out of
    // the served client's own `PASS_LIMITS` literal as `pass.capabilities.intentChars`, exactly as
    // it has always published the score's byte fence — so the site's staging step carries it into
    // these constants beside `scoreFenceBytes` and the number this file measures against is the
    // number the client applies rather than a second copy of it. What stands after the `||` is a
    // FALLBACK for a settings record built before that line landed; it is the number the client
    // applies today, and a record that carries the field overrides it without argument.
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
    var RATIO_STEPS = MANIFESTS.gears.handles.ratio.rungs || 0;
    var SIZE_MAX = HANDLE_SPECS.gears.size[1];

    // ---- the pair, derived from the two works rather than looked up ----

    // WHAT A PAIR SHARES, READ TWO WAYS, AND WHY THE SECOND ONE HAD TO ARRIVE.
    //
    // `both` is pair-shared.py's own reading: both works clear the measure's DISCRIMINATING
    // threshold, which the collection's builder sets at that measure's top quartile. That reading
    // answers «is this one of the pair's standout measures», and it is the right question for
    // ranking. It is the wrong question for whether a ground exists, and the numbers say so
    // plainly: a top quartile is cleared by 31 of the 121 works for EVERY measure by construction,
    // so both works clear any one measure on about 6 percent of ordered pairs — and 83 percent of
    // all compositions fell past every shared measure to the universal tonal-and-spectral bridge,
    // whose cut is a band, whose instrument is the material one. Seven roads, one cut, one
    // instrument: his 19:13 word about a route's breadth failed at the ground rather than at the
    // road, and no amount of choosing between roads could have reached it.
    //
    // `usable` is the measure's OWN cut-line floor — the bar that says this reading means something
    // at all, and the very bar `axisReading` already applies to the TRAVELLING axis. That asymmetry
    // was the defect in one sentence: a measure good enough to travel on was not good enough to
    // hold. Measured over the collection, the floor is cleared by both works on 85.6 percent of
    // pairs for banding, 76.7 for radial and 48.0 for regions — the three cuts that almost never
    // got chosen — while grid, texture and the dominant object stay rare, which is a fact about
    // what the works carry rather than a rule this file imposes.
    function sharedMeasures(a, b) {
      var held = [], usable = [], per = {}, i, m, sa, sb, floor;
      for (i = 0; i < MEASURES.length; i++) {
        m = MEASURES[i];
        sa = a.measures[m];
        sb = b.measures[m];
        floor = FLOORS[m];
        per[m] = { min: r4(Math.min(sa, sb)),
                   both: sa >= THRESHOLDS[m] && sb >= THRESHOLDS[m],
                   usable: floor !== undefined && floor !== null && sa >= floor && sb >= floor };
        if (per[m].both) held.push(m);
        if (per[m].usable) usable.push(m);
      }
      return { held: held, usable: usable, per: per };
    }

    // A measure whose cut an instrument in this collection can actually play. KIND_OF_MEASURE says
    // which element kind a measure cuts on and INSTRUMENT_OF_KIND which instrument cuts on that
    // kind; four kinds have none and MISSING_INSTRUMENT names each of the four.
    // The instrument that cuts on a kind AND that this collection actually publishes a manifest
    // for. INSTRUMENT_OF_KIND names the wish; MANIFESTS is the fact.
    // AN INSTRUMENT THAT DECLARES THE WORLD LEVEL SPENDS THE CROSSING'S ONE MIRACLE. Folding the
    // space a work lives in is a world act — shelf 8's folded space, which shelf 6 says consumes
    // the slot and never stacks — and the instrument's own manifest is what declares it, so this
    // reads the manifest instead of keeping a list of names. It is the same fact the host reads
    // when it refuses a world-level cue beside a camera-led flight.
    function spendsTheMiracle(iid) {
      var m = iid && MANIFESTS[iid];
      return !!(m && (m.levels || []).indexOf("WORLD") >= 0);
    }

    // Every instrument this collection publishes that cuts on a kind, in one settled order.
    function instrumentsOfKind(kind) {
      return (kind && CUTS_ON[kind]) ? CUTS_ON[kind] : [];
    }

    // Whether ANY published instrument cuts on a kind at all. `noMiracle` narrows the question to
    // the instruments a step with no miracle to spend may reach.
    function instrumentOfKind(kind, noMiracle) {
      var all = instrumentsOfKind(kind), i;
      for (i = 0; i < all.length; i++) {
        if (!noMiracle || !spendsTheMiracle(all[i])) return all[i];
      }
      return null;
    }

    // How legibly a work's own making reads, before a passage may set out to reveal it. Every work
    // of the collection carries the reading; nothing measures where the line between legible and not
    // should fall, so this is the plainest meaning of a confidence — likelier right than wrong — and
    // it stands on the revisit list.
    var DEVICE_LEGIBLE = 0.5;

    // WHAT A PAIR MUST READ FOR AN INSTRUMENT TO BE WORTH CASTING, where several cut on one kind.
    // An instrument named here states its own condition in its own terms; one not named asks
    // nothing and is always a candidate on the kinds it cuts. These are the measurements that make
    // the two panel instruments two different acts rather than two spellings of one.
    var INSTRUMENT_ASKS = {
      // THE FOLD IS AN IMPOSSIBLE EVENT, so the charter's five-condition box law is what qualifies
      // it: the departing work's own region division has to be strong enough to place a crease on,
      // over enough real panels to be the walls of a solid. This was stated on the box-fold ROAD
      // alone, which left every other road free to reach the same ground and fold a work whose
      // regions read at nothing.
      boxfold: function (a, b, floors) {
        // READ OF THE PAIR AND NOT OF ONE END OF IT. A ground is the pair's, and the family read
        // off it has to be the same one whichever way the visitor walks, so an ask that read the
        // departing work alone would let a ground be held in one direction and refuse to cast in
        // the other — 61 ordered pairs declined exactly that way before this was straightened.
        var best = Math.max(Number(((a.structure || {}).regions || {}).score) || 0,
                            Number(((b.structure || {}).regions || {}).score) || 0);
        var faces = Math.max(facesOf(a), facesOf(b));
        if (best < floors.regions_tight) {
          return [false, "neither work reads regions over the tight floor of "
                  + pyText(flt(floors.regions_tight)) + "; the stronger reads "
                  + pyText(flt(r4(best)))];
        }
        if (faces < BOX_FACES) {
          return [false, "neither work cuts into the " + BOX_FACES + " real panels a box needs; "
                  + "the finer cuts into " + faces];
        }
        return [true, "a work of the pair reads regions at " + pyText(flt(r4(best)))
                + " over " + faces + " faces"];
      },
      // THE PARQUET REVEALS HOW A WORK WAS MADE — his 19:13 word makes that a register of its own —
      // so what qualifies it is whether the making READS: the work's own device, the step it was cut
      // at and how confidently that step was recovered. A passage that sets out to show the making
      // of a work nobody could read the making of would be showing nothing.
      unfold: function (a, b, floors) {
        // THE MAKING THIS PASSAGE REVEALS IS THE ONE THAT READS. Of the two works, the parquet
        // opens on whichever carries its own device most legibly — the fill below reads the same
        // work — so the ask is of the pair and the ground it gates is direction-free.
        var da = (a.structure || {}).ownDevice || {}, db = (b.structure || {}).ownDevice || {};
        var ca = Number(da.confidence) || 0, cb = Number(db.confidence) || 0;
        var dev = ca >= cb ? da : db, conf = Math.max(ca, cb);
        var step = Number(dev.stepPx) || 0;
        if (!(step > 0)) {
          return [false, "neither work carries a measured step of its own to open on"];
        }
        if (conf < DEVICE_LEGIBLE) {
          return [false, "the clearer of the two devices reads at " + pyText(flt(r4(conf)))
                  + ", under the " + pyText(flt(DEVICE_LEGIBLE)) + " a making has to read at "
                  + "before a passage sets out to reveal it"];
        }
        return [true, "a work of the pair was cut as " + pyText(dev.kind || "a device")
                + " at a step of " + pyText(flt(r4(step))) + " px, read at "
                + pyText(flt(r4(conf)))];
      }
    };

    // THE INSTRUMENT THIS PAIR CASTS ON A KIND. Where one cuts on it, that one. Where several do,
    // the role's budget narrows them, each candidate's own reading of the pair narrows them again,
    // and the die chooses among whatever is left — the same shape the seven roads are chosen by, so
    // a pinned seed reproduces the casting exactly and a fresh seed varies it.
    // Whether SOME instrument could cast this kind for this pair, with no die rolled — the
    // question a ground has to answer before it is a ground. Direction-free: an instrument whose
    // reading is of the departing work is asked of both orderings.
    function castableOnKind(kind, a, b, floors, noMiracle) {
      var all = instrumentsOfKind(kind), i, ask;
      for (i = 0; i < all.length; i++) {
        if (noMiracle && spendsTheMiracle(all[i])) continue;
        ask = INSTRUMENT_ASKS[all[i]];
        if (!ask) return true;
        if (ask(a, b, floors)[0] || ask(b, a, floors)[0]) return true;
      }
      return false;
    }

    function castOnKind(kind, fromW, toW, floors, noMiracle, seed, key, slot) {
      var all = instrumentsOfKind(kind), pool = [], said = [], i, ask;
      for (i = 0; i < all.length; i++) {
        if (noMiracle && spendsTheMiracle(all[i])) {
          said.push({ instrument: all[i], ok: false,
                      why: "it spends the one miracle and this step has none to spend" });
          continue;
        }
        ask = INSTRUMENT_ASKS[all[i]];
        if (!ask) { pool.push(all[i]); said.push({ instrument: all[i], ok: true, why: null }); continue; }
        var answer = ask(fromW, toW, floors);
        said.push({ instrument: all[i], ok: answer[0], why: answer[1] });
        if (answer[0]) pool.push(all[i]);
      }
      if (!pool.length) return [null, said];
      return [pool[dieAmong(seed, key + "|" + kind + "|" + slot, pool.length)], said];
    }

    function playable(measure) {
      return !!instrumentOfKind(KIND_OF_MEASURE[measure]);
    }

    // A measure this PAIR can actually stand on: an instrument cuts on it, and both works carry
    // real elements along that cut. A cut one of the two works offers only as the whole frame is a
    // ground the actors cannot be drawn from — the refusal `castActors` names two steps later — and
    // a ground a pair cannot hold is not the pair's ground. Both readings come off the works' own
    // element sets.
    function holdable(a, b, measure, noMiracle) {
      var kind = KIND_OF_MEASURE[measure];
      if (!playable(measure)) return false;
      // A GROUND IS ONLY A GROUND WHERE SOME INSTRUMENT CAN ACTUALLY CAST IT. The gate belongs
      // HERE and not on a road alone: once an instrument that folds cuts on a kind, any road can
      // land on that ground by simply holding the strongest shared measure, and a quiet link would
      // fold the world without ever naming the road that does it. It asks the same question
      // `castOnKind` asks at casting time — the role's budget, then each candidate's own reading —
      // and it asks it of BOTH orderings of the pair, because a ground is the pair's and the family
      // read off it has to be the same one whichever way the visitor walks.
      if (!castableOnKind(kind, a, b, FLOORS, noMiracle)) return false;
      var sa = setFor(a, kind), sb = setFor(b, kind);
      return !!(sa && sa.realCount && sb && sb.realCount);
    }

    // The one key both directions of an edge roll the ground on.
    function groundKeyOf(a, b) {
      return a.id < b.id ? (a.id + "__" + b.id) : (b.id + "__" + a.id);
    }

    // The measure the WEAKER work carries most strongly, among those that pass the filter.
    function strongestHeld(shared, only) {
      var best = null, i, m;
      for (i = 0; i < shared.held.length; i++) {
        m = shared.held[i];
        if (only && !only(m)) continue;
        if (best === null || shared.per[m].min > shared.per[best].min) best = m;
      }
      return best;
    }

    // THE GROUND, CHOSEN AMONG EVERY GROUND THIS PAIR CAN HOLD. Where one measure qualifies it is
    // the ground; where several do, the die chooses, weighted by how strongly the weaker work
    // carries each — so the strongest shared ground stays the likeliest and a pair with a strong
    // band and a weak radial stops landing on the same cut as a pair with the reverse. This is the
    // rule his 18:56 word asks for one level below the roads: the arsenal stays full and the
    // options in hand are plentiful, and a road that chose a different derivation reaches the eye
    // as a different passage because it stands on a different cut.
    //
    // THE DIE IS ROLLED ON THE EDGE'S OWN KEY AND NOT ON THE PASSAGE'S, so the two directions of one
    // edge choose the same ground. §4.8's kinship is that a return keeps the family, and the family
    // is read off the pivot's own transform; a ground that changed with the direction would make
    // every return unrelated by construction.
    function chooseGround(shared, only, seed, groundKey) {
      var pool = [], weight = 0, i, m;
      for (i = 0; i < shared.usable.length; i++) {
        m = shared.usable[i];
        if (only && !only(m)) continue;
        pool.push(m);
        weight += Math.max(num(shared.per[m].min), 0.0001);
      }
      if (!pool.length) return null;
      if (pool.length === 1) return pool[0];
      pool.sort();
      var at = dieAmong(seed, groundKey + "|ground", 100000) / 100000 * weight, run = 0;
      for (i = 0; i < pool.length; i++) {
        run += Math.max(num(shared.per[pool[i]].min), 0.0001);
        if (at < run) return pool[i];
      }
      return pool[pool.length - 1];
    }

    // THE GROUND A CROSSING STANDS ON. Every measure both works clear their own discriminating
    // threshold on is an invariant the pair shares — that is what the threshold means — and the
    // charter's law is that the pivot is the pair's invariant shared part, held throughout, with
    // everything outside it travelling. WHICH of the shared measures to hold was read here, before
    // this lane, as «the strongest», and a pair whose strongest shared measure cuts on tiles,
    // panels or named regions declined whole with «pivot needs an instrument that cuts on …»:
    // 2 862 of the 14 520 ordered pairs of the real collection, measured by this lane's sweep. So
    // the ground is the strongest shared measure AN INSTRUMENT CAN PLAY. Nothing else about the
    // pivot moves — an unplayable measure is still shared, it is simply not the part this crossing
    // stands on, and where nothing playable is shared the three grounds below answer in their own
    // order of precedence, ending at the tonal and spectral bridge that shelf 12 names the lawful
    // universal bridge for pairs with nothing in common.
    //
    // `free` is the measure a ROAD needs left free to travel: a road built on the pair's radial
    // reading cannot also hold it still. The ground then stands on the next playable shared measure,
    // or on one of the three below. `prefer` names a measure the road asks to stand on — a return
    // holding the pivot of the pass it answers uses it — and it wins wherever the pair can hold it.
    function pivotOfPair(a, b, free, prefer, noMiracle, seed, groundKey) {
      // The four pivots in the elements builder's own order of precedence.
      var all = sharedMeasures(a, b), v, na, nb, strength, ra, rb, hues, i;
      var best = null;
      if (prefer && prefer !== free && all.per[prefer] && all.per[prefer].usable
          && holdable(a, b, prefer, noMiracle)) {
        best = prefer;
      }
      if (best === null) {
        best = chooseGround(all, function (m) {
          return m !== free && holdable(a, b, m, noMiracle);
        }, seed || 0, groundKey || (a.id + "__" + b.id));
      }
      var shared = best === null ? null : { measure: best, strength: all.per[best].min };
      if (shared) {
        v = { strength: shared.strength, measure: shared.measure,
              cut: CUT_OF_MEASURE[shared.measure][0],
              transform: CUT_OF_MEASURE[shared.measure][1],
              elementKind: KIND_OF_MEASURE[shared.measure] };
        return { kind: "shared-measure", value: v, rowStrength: r4(shared.strength) };
      }
      na = a.structure.rotational.n || 0;
      nb = b.structure.rotational.n || 0;
      // The shared turn cuts on wedges, so it is a ground only where both works actually carry a
      // wedge set — the same reading `compose` makes two steps later, made here where it can still
      // be answered by standing on the next ground instead of by refusing the pair.
      if (na >= 3 && na === nb && setFor(a, "wedge") !== null && setFor(b, "wedge") !== null) {
        strength = r4(Math.min(a.structure.rotational.score || 0,
                               b.structure.rotational.score || 0));
        v = { order: na, cut: "wedges", transform: "gear_mesh", elementKind: "wedge",
              strength: strength };
        return { kind: "shared-rotational-order", value: v, rowStrength: r4(strength) };
      }
      ra = a.palette.rung;
      rb = b.palette.rung;
      hues = [];
      for (i = 0; i < (a.palette.hues || []).length; i++) {
        if ((b.palette.hues || []).indexOf(a.palette.hues[i]) >= 0) hues.push(a.palette.hues[i]);
      }
      hues.sort();
      if (ra === rb && hues.length) {
        // The palette pivot's own strength stands on the pair's record and never on the pivot's
        // value, so the row's strength is zero — the elements builder reads `strength` off the
        // value and finds none. Carried here as it stands there.
        v = { rung: ra, hues: hues, cut: "colour_world", transform: "palette_handover",
              elementKind: "band" };
        return { kind: "shared-palette-region", value: v, rowStrength: r4(0.0) };
      }
      var ta = Number(a.luminance.ladderPosition), tb = Number(b.luminance.ladderPosition);
      var fa = Number(a.texture.detailPx || 1), fb = Number(b.texture.detailPx || 1);
      var tonal = 1.0 - Math.min(1.0, Math.abs(ta - tb));
      var spectral = 1.0 - Math.min(1.0, Math.abs(Math.log2(Math.max(fa, 1e-6))
                                                  - Math.log2(Math.max(fb, 1e-6))) / 4.0);
      v = { tonalCloseness: r4(tonal), spectralCloseness: r4(spectral), ladder: [ta, tb],
            detailPx: [fa, fb], cut: "tonal_zones_and_detail_scales",
            transform: "zone_handover_and_scale_growth", elementKind: "band" };
      return { kind: "tonal-and-spectral-bridge", value: v, rowStrength: r4(r4(tonal) || 0.0) };
    }

    function pairScore(ra, rb) {
      var sa = ra[0], pa = ra[1], sb = rb[0], pb = rb[1];
      if (sa < READY_FLOOR || sb < READY_FLOOR) return 0.0;
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
        readiness: r4(pairScore(fromW.readiness, toW.readiness)),
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
        strength: r4(strength ? strength : 0.0),
        held: true
      };
    }

    function pivotKindsOf(pivot) {
      return PIVOT_KINDS_OF_CUT[pivot.kind] || [pivot.elementKind];
    }

    // ---- step two, the travelling axis ----

    function axisReading(work, axis, floors) {
      var st = work.structure, s, ends, t, rr;
      if (axis === "banding") {
        s = st.banding.score;
        ends = { periodPx: r4(st.banding.periodPx), axis: st.banding.axis };
      } else if (axis === "radial") {
        rr = st.radial;
        s = rr.score;
        ends = { centre: [r4(rr.centre[0]), r4(rr.centre[1])], subType: rr.subType };
      } else if (axis === "regions") {
        s = st.regions.score;
        ends = { count: st.regions.count };
      } else if (axis === "grid") {
        s = st.grid.score;
        ends = { periodPx: r4(st.grid.periodPx), angleDeg: r4(st.grid.angleDeg) };
      } else if (axis === "texture") {
        t = work.texture;
        s = t.scoreFromCutLines;
        ends = { detailPx: r4(t.detailPx), spectralPeriodPx: r4(t.spectralPeriodPx) };
      } else if (axis === "dominant_object") {
        s = st.dominantObject.score;
        ends = { box: st.dominantObject.bbox.map(function (x) { return r4(x); }) };
      } else {
        return null;
      }
      if (s === null || s === undefined || s < floors[axis]) return null;
      return { score: r4(s), ends: ends };
    }

    function travellingAxis(aWork, bWork, pivot, floors) {
      var held = pivot.measure, best = null, i, axis, ra, rb, delta;
      for (i = 0; i < TRAVEL_AXES.length; i++) {
        axis = TRAVEL_AXES[i];
        if (axis === held) continue;
        ra = axisReading(aWork, axis, floors);
        rb = axisReading(bWork, axis, floors);
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
      var i;
      for (i = 0; i < work.sets.length; i++) {
        if (work.sets[i].kind === kind) return work.sets[i];
      }
      return null;
    }

    function castActors(fromW, toW, pivot, axis) {
      var actors = [], kinds = pivotKindsOf(pivot), sides = { a: false, b: false };
      var pairs = [["a", fromW], ["b", toW]], i, j, ref, work, drawn, anySet, found, tkind, role;
      for (i = 0; i < pairs.length; i++) {
        ref = pairs[i][0];
        work = pairs[i][1];
        drawn = 0;
        anySet = false;
        for (j = 0; j < kinds.length; j++) {
          found = setFor(work, kinds[j]);
          if (found === null) continue;
          anySet = true;
          if (!found.realCount) continue;
          actors.push({ ref: ref, set: found.index, role: "pivot-carrier", ids: null,
                        count: found.count, measuredGrain: found.measuredGrain,
                        mergeFactor: found.mergeFactor });
          drawn += 1;
        }
        if (!anySet) return [null, "no element set on the pivot's own cut for work " + ref];
        if (!drawn) return [null, "work " + ref + " offers only the whole frame along the pivot's cut"];
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
      for (i = 0; i < actors.length; i++) sides[actors[i].ref] = true;
      if (!sides.a || !sides.b) return [null, "no actor was drawn from one of the two works"];
      return [actors, null];
    }

    // ---- step four, the arrival ----

    function locusOf(work, floors) {
      var st = work.structure, mot = work.motifs || {}, measured = mot.measured || [];
      var rr = st.radial, c, y;
      if (rr.score !== null && rr.score !== undefined && rr.score >= floors.radial_tight) {
        c = mot.radialCentre || rr.centre;
        return ["pole", [r4(c[0]), r4(c[1])]];
      }
      if (measured.indexOf(MOTIF_SEAM) >= 0) {
        y = (st.horizon || {}).y;
        if (y !== null && y !== undefined) return ["horizon-seam", [r4(0.5), r4(y)]];
      }
      if (measured.indexOf(MOTIF_GATE) >= 0 && (mot.gateGap || 0) > 0) {
        return ["gate", [r4(0.5), r4(0.5)]];
      }
      return ["none", null];
    }

    function figureOnLocus(work, locus) {
      if (locus === null || locus === undefined) return false;
      var box = work.structure.dominantObject.bbox;
      var cx = (box[0] + box[2]) / 2.0, cy = (box[1] + box[3]) / 2.0;
      return Math.hypot(cx - num(locus[0]), cy - num(locus[1])) <= LOCUS_NEAR;
    }

    function worldOf(work, floors, axis) {
      if (axis === null || axis.axis !== "radial") return null;
      var rr = work.structure.radial;
      if (rr.subType !== "ring" || rr.score < floors.radial_tight) return null;
      var polar = work.structure.polar || {}, keys = Object.keys(POLAR_WORLD).sort();
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

    function registerOf(fromW, toW, arrival, world) {
      var voidShare, la, lb;
      if (arrival === "CONDENSED") {
        voidShare = (toW.motifs || {}).voidShare;
        if (voidShare !== null && voidShare !== undefined && voidShare >= VOID_SHARE_FLOOR) {
          return "apparition";
        }
      }
      if (world) return "discovery";
      la = (fromW.luminance || {}).ladderPosition;
      lb = (toW.luminance || {}).ladderPosition;
      if (la !== null && la !== undefined && lb !== null && lb !== undefined
          && Math.abs(la - lb) >= LADDER_DISTANCE) {
        return "provocation";
      }
      return "none";
    }

    // ---- the voices, the levels, the tier ----

    // THE STEP'S ROLE NAMES THE TIER; THE DISTANCE ONLY GUESSED IT. A crossing carrying a folded
    // space and an arrival is a culmination when the WALK says this step is one — that is what
    // charter shelf 15 means by a step's function, and shelf 17 budgets by that function. The
    // distance test stays for a step whose role the walk never stated: with no role in hand the
    // only reading of a culmination the composer ever had was the pair standing far apart, and that
    // reading is kept where it is still the only one there is.
    function voiceTheCues(hasTravel, hasArrival, world, distance, role, folds) {
      // A CROSSING THAT FOLDS THE FRAME INTO A SOLID CARRIES ITS MIRACLE ON THE CUE THAT FOLDS IT,
      // wherever that cue stands. `world` is the other way a crossing spends the slot — the
      // arriving work's own space opening — and the two never stand together, which `compose`
      // settles before this is asked.
      var culmination = !!(world || folds) && hasArrival
        && (role === "culmination" || distance >= CULMINATION_DISTANCE);
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
    // What this replaces: a hard refusal. It cost 73 ordered pairs of the real collection at a
    // culmination, every one of them a crossing whose frame folds under a pivot with an arrival
    // beside it and no travelling move — one letter where the culmination row asks for two, which
    // is a middle by the row's own reading and was a glide by the code's.
    function tierFor(voices, tier) {
      var letters = 0, accs = 1, miracles = 0, k, i, row;
      for (k in voices) {
        if (voices[k] === "letter") letters += 1;
        else if (voices[k] === "accompaniment") accs += 1;
        else if (voices[k] === "miracle") miracles += 1;
      }
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
      return [null, counts];
    }

    // ---- the meshing instrument's own numbers ----

    function meshingTravel(fromW, toW, pivot) {
      var ra = setFor(fromW, "ring"), rb = setFor(toW, "ring");
      if (ra === null || rb === null) {
        return [null, "the meshing travel needs a measured ring count and one work has no ring set"];
      }
      var countFrom = ra.measuredGrain, countTo = rb.measuredGrain;
      if (countFrom <= 0 || countTo <= 0) {
        return [null, "the meshing travel needs a measured ring count above zero on both works"];
      }
      var toRing = toW.structure.radial.subType === "ring";
      var sizeTo = toRing ? SIZE_FLOOR : 4.5;
      var sizeFrom = sizeTo * (countFrom / countTo);
      // THE MEASURED THING IS THE RATIO, AND ONLY THE RATIO. The size travels from one end of the
      // crossing to the other so that the pair's apparent tooth pitch holds while its radius grows
      // with the ring count — which is why the two ends stand in the ratio of the two works' own
      // measured ring counts. Where the departing end would fall under the floor, the whole travel
      // is lifted by the one factor that puts it exactly on the floor: the measured ratio is
      // untouched and the pair simply stands further from the eye.
      //
      // What stood here refused instead. A ring arrival pins the arriving end ON the floor, so
      // every pair whose departing work carries FEWER rings than its arriving one had nowhere to
      // go and the meshing travel refused outright — 712 of the 947 ordered pairs the kaleidoscope
      // road qualifies for over the real collection, measured by this lane's own sweep. The floor
      // is a floor on what the eye can read, not a reason to refuse a pair.
      if (sizeFrom > 0 && sizeFrom < SIZE_FLOOR) {
        var lift = SIZE_FLOOR / sizeFrom;
        sizeFrom = SIZE_FLOOR;
        sizeTo = sizeTo * lift;
      }
      if (sizeFrom < SIZE_FLOOR || sizeTo < SIZE_FLOOR) {
        return [null, "the meshing travel would go under size " + pyText(flt(SIZE_FLOOR))
                + ", where the band period holds as a number while the picture's apparent "
                + "period departs from it"];
      }
      var over = sizeFrom > SIZE_MAX;
      if (over) sizeFrom = SIZE_MAX;
      var raw = countTo / (countFrom + countTo);
      var step = roundToInt(raw * (RATIO_STEPS - 1));
      var ratio = r4(step / (RATIO_STEPS - 1));
      var frac = pivot.bandPeriodFrac;
      var lo = HANDLE_SPECS.gears.bandPeriod[0], hi = HANDLE_SPECS.gears.bandPeriod[1];
      var bandPeriod = frac ? r4(Math.min(hi, Math.max(lo, frac))) : null;
      return [{ sizeFrom: r4(sizeFrom), sizeTo: r4(sizeTo), ratio: ratio,
                bandPeriod: bandPeriod, overMax: over,
                measuredCounts: [countFrom, countTo] }, null];
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

    function ownTheLevels(cues, pivotCueId) {
      var byLevel = {}, out = {}, i, j, cue, lv;
      for (i = 0; i < cues.length; i++) {
        cue = cues[i];
        for (j = 0; j < cue.levels.length; j++) {
          lv = cue.levels[j];
          if (!byLevel[lv]) byLevel[lv] = [];
          byLevel[lv].push(cue);
        }
        out[cue.id] = {};
      }
      Object.keys(byLevel).sort().forEach(function (level) {
        var holders = byLevel[level], owner = null, pool, k;
        if (level === "SURFACE") {
          for (k = 0; k < holders.length; k++) {
            if (holders[k].id === pivotCueId) { owner = holders[k]; break; }
          }
          if (owner === null) owner = earliest(holders);
        } else {
          pool = holders.filter(function (c) { return c.id !== pivotCueId; });
          owner = earliest(pool.length ? pool : holders);
        }
        for (k = 0; k < holders.length; k++) {
          out[holders[k].id][level] = holders[k] === owner ? "owns" : ("accompanies:" + owner.id);
        }
      });
      return out;
    }

    function earliest(cues) {
      var best = cues[0], i;
      for (i = 1; i < cues.length; i++) {
        var a = cues[i], b = best;
        if (num(a.window[0]) < num(b.window[0])
            || (num(a.window[0]) === num(b.window[0]) && a.id < b.id)) best = a;
      }
      return best;
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
    // lane measured the collection and the composer lane measured the saturation). A clamp put
    // 9 280 of the 14 520 ordered pairs on exactly the same number: three passages in five approached
    // identically, and the approach — the one thing a person feels most directly — carried no reading
    // of any pair. That is his 19:13 word about breadth failing in the plainest place there is.
    //
    // What the door framings ask for has a median of 2.05 times, a nine-tenths point of 6.44 and a
    // worst of 86.3: a smooth tail with no knee, so no clamp point is the right one and clamping is
    // the wrong shape whatever number it carries. `CAP · a / (|a| + CAP)` is the same bound written
    // as a limit instead of a wall — it keeps the sign, it is monotone, so a pair asking for more
    // still gets more than a pair asking for less, and it APPROACHES the cap without ever reaching
    // it. Measured over the same 14 520 pairs: nothing lands on the bound where 9 280 did, distinct
    // approaches rise from 3 453 to 5 957, and the worst magnification falls to 1.568 times from
    // 1.649. The bound is not loosened by a hair — it is held more tightly than the clamp held it.
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

    // THE RHYTHM, AND THE DEVIATION A FURTHER PASS PUTS ON IT. §4.8 lets the rhythm and the phases
    // differ across a return, and charter shelf 13 states what a living rhythm is: a base period
    // plus a measured deviation, one instrument per time axis and never two stacked. The base is
    // the window each shape has always had. The deviation is drawn from the die and the pass count,
    // and it moves only where a cue OPENS, never where it closes — so both doors stand exactly
    // where they stood, the passage still ends when it ends, and the derived duration does not
    // move. RHYTHM_REACH is a share of the passage that nothing measures; the revisit list has it.
    var RHYTHM_REACH = 0.05;

    function cueWindows(shapeHasTravel, arrivalLeads, travelInstrument, shift) {
      var w = { pivot: [0.0, 1.0] }, s = shift || 0;
      if (shapeHasTravel) {
        w.travel = travelInstrument === "gears" ? [0.0, 0.86] : [0.18, 0.86];
        w.travel[0] = r4(Math.max(0.0, Math.min(0.5, w.travel[0] + s)));
      }
      w.arrival = arrivalLeads ? [0.10, 1.0] : [0.62, 1.0];
      w.arrival[0] = r4(Math.max(0.0, Math.min(0.9, w.arrival[0] - s)));
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
    function tracksFor(instr, cueId) {
      var manifest = MANIFESTS[instr].handles, handles = Object.keys(manifest).sort();
      var out = {}, i, h;
      for (i = 0; i < handles.length; i++) {
        h = handles[i];
        if (manifest[h].open) continue;
        out[h] = { node: cueId + "-" + h };
      }
      return out;
    }

    function resourcesBlock(variant) {
      return { bytesEstimate: 0, framebuffers: 0, passes: 1, pingPong: 0, programs: 1,
               textureSlots: 2, textures: 0, variant: variant };
    }

    function buildTemplate(shape, spec) {
      var voices = spec.voices;
      var windows = cueWindows(spec.travel !== null, spec.arrivalLeads, spec.travel,
                               spec.rhythmShift);
      var instrumentOf = {}, i, cueId, instr;
      for (i = 0; i < CUE_IDS.length; i++) {
        if (spec[CUE_IDS[i]]) instrumentOf[CUE_IDS[i]] = spec[CUE_IDS[i]];
      }
      var order = CUE_IDS.filter(function (c) { return instrumentOf[c] !== undefined; });
      var placed = placeTheStack(order, instrumentOf);
      if (placed[0] === null) {
        throw new Error("a shape reached the template builder that the placement law refuses: "
                        + shape + " — " + placed[1]);
      }
      var stacks = placed[0], cues = [];
      for (i = 0; i < CUE_IDS.length; i++) {
        cueId = CUE_IDS[i];
        instr = spec[cueId];
        if (!instr) continue;
        cues.push({
          id: cueId,
          instrument: { api: INSTRUMENTS[instr].api, id: instr },
          voice: voices[cueId],
          roles: spec.roles[cueId].slice(),
          levels: INSTRUMENTS[instr].levels.slice(),
          window: [flt(windows[cueId][0]), flt(windows[cueId][1])],
          works: ["a", "b"],
          stack: stacks[cueId],
          cameraAuthority: "stage",
          doors: { "in": { handle: "mix", value: 0, measured: true },
                   out: { handle: "mix", value: 1, measured: true } },
          tracks: tracksFor(instr, cueId),
          resources: { lean: resourcesBlock("lean"), standard: resourcesBlock("standard"),
                       rich: resourcesBlock("rich") }
        });
      }
      var levels = ownTheLevels(cues, "pivot");
      for (i = 0; i < cues.length; i++) {
        cues[i].levelOwnership = levels[cues[i].id];
        cues[i].levels = cues[i].levels.filter(function (lv) {
          return levels[cues[i].id][lv] === "owns";
        });
      }
      var track = [{ at: "a", pan: { x: 0, y: 0 }, logScale: 0, pitch: 0, yaw: 0, roll: 0,
                     fov: null, owner: "stage" }];
      if (spec.travel === "gears") {
        track.push({ at: "@atFrom", pan: { x: "@panFromX", y: "@panFromY" },
                     logScale: "@logScale", pitch: 0, yaw: 0, roll: 0, fov: null,
                     owner: "stage" });
        track.push({ at: "@atTo", pan: { x: "@panToX", y: "@panToY" },
                     logScale: "@logScale", pitch: 0, yaw: 0, roll: 0, fov: null,
                     owner: "stage" });
      }
      track.push({ at: "b", pan: { x: 0, y: 0 }, logScale: 0, pitch: 0, yaw: 0, roll: 0,
                   fov: null, owner: "stage" });
      var quality = {};
      ["lean", "standard", "rich"].forEach(function (v) {
        var perCue = {};
        cues.forEach(function (c) { perCue[c.id] = { resources: resourcesBlock(v) }; });
        quality[v] = { renderScale: null, cues: perCue };
      });
      return {
        shape: shape,
        schema: SCHEMA,
        tier: spec.tier,
        duration: spec.duration,
        middle: spec.middle,
        budget: spec.budget,
        heldFraction: flt(r4(2 * DOOR_HOLD)),
        doorHold: flt(DOOR_HOLD),
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
    // THE ROADS — the plural sources of a crossing's structure
    // ---------------------------------------------------------------------------------------
    //
    // His word of 2026-08-17 18:56, standing in the charter's Model: «the axes that differ most
    // travel» is ONE lawful derivation among several and never the whole formula. Equally lawful:
    // a road along what the pair SHARES, the shared measure held while everything outside it
    // travels; a road built from HOW A WORK IS MADE — a radial work spins or opens into a
    // kaleidoscope, a symmetric work slides its parts along its own symmetry or becomes stripes, a
    // work folding along strong directions folds into a box under the five-condition box law; and a
    // road along the pair's DISSIMILAR axes with the mystery in the middle.
    //
    // Each road below states, in its own lines, the measurements that QUALIFY a pair for it and the
    // ones that DISQUALIFY it, and every one of those readings comes off the two works' own records
    // — nothing pairwise is written down and nothing scales with the number of pairs (his 19:21
    // word). Where several roads qualify the die chooses among them, so a pinned seed reproduces
    // the choice exactly and a fresh seed varies it (charter shelf 16). Where none qualifies the
    // tonal and spectral bridge stands as the last candidate — shelf 12 names it the lawful
    // universal bridge for pairs with nothing in common — so no pair is left without a road.
    //
    // A ROAD ANSWERS FIVE QUESTIONS AND NOTHING ELSE, and the machinery below it is unchanged:
    //   ground   the measure the crossing holds still, or null to let the pair's own precedence say
    //   free     the measure this road needs left free to travel, so the ground never holds it
    //   axis     how the travelling axis is picked — a measure name pins it, "near" takes the
    //            closest reading of the two works, "far" the most distant
    //   miracle  whether this road may spend the crossing's one miracle on a folded space
    //   moves    how many structural gestures it reaches for, before the role's budget cuts it back

    // How close two readings of one axis stand before the road between them counts as a road along
    // the pair's SIMILAR axes. Nothing measures this number; it is the working span of a similar
    // road and it stands on the revisit list.
    var SIMILAR_DELTA = 0.15;
    // The faces a box needs before a work can fold into one: four walls read off the departing
    // work's own region lines, under the five-condition box law of 12.08 23:49.
    var BOX_FACES = 4;

    // The travelling axis, picked the way a road asks. "far" is the reading this file has always
    // had — the axes that differ most travel — and it is delegated unchanged so the road that keeps
    // it composes exactly what stage 0 composed. "near" runs the road along the pair's most similar
    // axis; a measure name pins the axis to that measure or answers with nothing.
    function travellingAxisOn(fromW, toW, held, floors, pick) {
      if (!pick || pick === "far") return travellingAxis(fromW, toW, { measure: held }, floors);
      var best = null, bestRaw = 0, i, axis, ra, rb, delta;
      for (i = 0; i < TRAVEL_AXES.length; i++) {
        axis = TRAVEL_AXES[i];
        if (axis === held) continue;
        if (pick !== "near" && axis !== pick) continue;
        ra = axisReading(fromW, axis, floors);
        rb = axisReading(toW, axis, floors);
        if (ra === null || rb === null) continue;
        delta = Math.abs(ra.score - rb.score);
        if (best === null || delta < bestRaw || (delta === bestRaw && axis > best.axis)) {
          best = { axis: axis, delta: r4(delta), from: ra, to: rb };
          bestRaw = delta;
        }
      }
      return best;
    }

    // The road every pair keeps when nothing else qualifies: the pair's own ground, the axes that
    // differ most travelling, and the tonal and spectral bridge underneath it where the two works
    // share no measure at all. This is the derivation stage 0 landed, whole.
    var BRIDGE_ROAD = { id: "bridge", ground: null, free: null, axis: "far", miracle: true,
                        moves: 2, why: "no road built on the pair's own structure qualifies, so "
                        + "the crossing runs on the universal bridge" };

    function roadsFor(fromW, toW, floors) {
      var shared = sharedMeasures(fromW, toW), roads = [], notes = [];
      function no(id, why) { notes.push({ road: id, ok: false, why: why }); }
      function yes(id, road, why) {
        road.id = id;
        road.why = why;
        roads.push(road);
        notes.push({ road: id, ok: true, why: why });
      }
      var rFrom = fromW.structure.radial || {}, rTo = toW.structure.radial || {};
      var bFrom = fromW.structure.banding || {}, bTo = toW.structure.banding || {};
      var gFrom = fromW.structure.regions || {};

      // 1 · A ROAD ALONG WHAT THE PAIR SHARES. It qualifies on two measurements at once: the two
      // works clear one and the same discriminating threshold on a measure an instrument can cut
      // on, which is the ground; and some OTHER axis reads on both works with their two scores
      // standing close, which is the axis the road runs along. A pair whose every other axis stands
      // far apart has no similar road to run — that pair's road is a road along its differences.
      var heldGround = strongestHeld(shared, playable);
      var nearAxis = heldGround === null ? null
        : travellingAxisOn(fromW, toW, heldGround, floors, "near");
      if (heldGround === null) {
        no("shared-ground", "the two works clear no common measure this collection cuts on");
      } else if (nearAxis === null) {
        no("shared-ground", "beside the shared " + heldGround + " no axis reads on both works");
      } else if (num(nearAxis.delta) > SIMILAR_DELTA) {
        no("shared-ground", "the closest axis is " + nearAxis.axis + " at " + pyText(nearAxis.delta)
           + " apart, past the " + pyText(flt(SIMILAR_DELTA)) + " a similar road runs inside");
      } else {
        yes("shared-ground", { ground: heldGround, free: null, axis: "near", miracle: false,
                               moves: 2 },
            "both works clear " + heldGround + " at " + pyText(shared.per[heldGround].min)
            + " and their " + nearAxis.axis + " readings stand only "
            + pyText(nearAxis.delta) + " apart");
      }

      // 2 and 3 · A ROAD BUILT FROM HOW A RADIAL WORK IS MADE. The radial reading has to stand on
      // BOTH works above the cut-line floor, because the bridge computes both structures and a
      // radial road playing one work's centre alone reads as artificial (the charter's own words);
      // and at least one of the two has to carry it above the tight floor, which is where the
      // measure stops being a trace and becomes the work's own device. Which of the two roads it is
      // the ARRIVING work's own subtype answers: rings open into a kaleidoscope — a folded space,
      // and that is the crossing's one miracle — while spokes turn, which is a spin and no miracle
      // at all.
      var radialAxis = travellingAxisOn(fromW, toW, null, floors, "radial");
      var radialTop = Math.max(Number(rFrom.score || 0), Number(rTo.score || 0));
      if (radialAxis === null) {
        no("spin", "the radial measure fails the cut-line floor on one of the two works");
        no("kaleidoscope", "the radial measure fails the cut-line floor on one of the two works");
      } else if (radialTop < floors.radial_tight) {
        no("spin", "the strongest radial reading of the pair is " + pyText(flt(r4(radialTop)))
           + ", under the tight floor of " + pyText(flt(floors.radial_tight)));
        no("kaleidoscope", "the strongest radial reading of the pair is "
           + pyText(flt(r4(radialTop))) + ", under the tight floor of "
           + pyText(flt(floors.radial_tight)));
      } else if (rTo.subType === "ring" && Number(rTo.score || 0) >= floors.radial_tight) {
        // THE WORK THAT OPENS IS THE ARRIVING ONE, so it is the arriving work's own reading that
        // has to clear the tight floor. `worldOf` below reads exactly the same two numbers off the
        // same work, so a pair that qualifies here is a pair whose folded space actually stands —
        // which is what makes this road the one a culmination reaches for.
        yes("kaleidoscope", { ground: null, free: "radial", axis: "radial", miracle: true,
                              moves: 3 },
            "the arriving work reads radial at " + pyText(flt(r4(Number(rTo.score || 0))))
            + " on rings, over the tight floor, and both works carry a radial reading, so the "
            + "rings open");
        no("spin", "the arriving work's radial reading is on rings, which open rather than turn");
      } else {
        yes("spin", { ground: null, free: "radial", axis: "radial", miracle: false, moves: 2 },
            "the arriving work reads radial at " + pyText(flt(r4(Number(rTo.score || 0))))
            + " on " + pyText(rTo.subType) + ", so its own turn is what travels");
        no("kaleidoscope", "the arriving work's radial reading is on "
           + pyText(rTo.subType) + " rather than on rings, so there is nothing to open");
      }

      // 4 and 5 · A ROAD BUILT FROM HOW A SYMMETRIC WORK IS MADE. A band family is a translational
      // symmetry the measure files actually carry, so it is the symmetry this road reads. It has to
      // stand on both works above the cut-line floor, one of them above the tight floor, and both
      // periods have to be real numbers of pixels — a band family with no period is a score with
      // nothing to slide. The two works' own band DIRECTIONS then say which road it is: where they
      // agree the parts slide along that one symmetry, and where they cross the fabric becomes
      // stripes.
      var bandAxis = travellingAxisOn(fromW, toW, null, floors, "banding");
      var bandTop = Math.max(Number(bFrom.score || 0), Number(bTo.score || 0));
      if (bandAxis === null) {
        no("symmetry-slide", "the banding measure fails the cut-line floor on one of the two works");
        no("stripes", "the banding measure fails the cut-line floor on one of the two works");
      } else if (bandTop < floors.banding_tight) {
        no("symmetry-slide", "the strongest band reading of the pair is "
           + pyText(flt(r4(bandTop))) + ", under the tight floor of "
           + pyText(flt(floors.banding_tight)));
        no("stripes", "the strongest band reading of the pair is " + pyText(flt(r4(bandTop)))
           + ", under the tight floor of " + pyText(flt(floors.banding_tight)));
      } else if (!(Number(bFrom.periodPx) > 0) || !(Number(bTo.periodPx) > 0)) {
        no("symmetry-slide", "one of the two band families carries no measured period");
        no("stripes", "one of the two band families carries no measured period");
      } else if (bFrom.axis === bTo.axis) {
        yes("symmetry-slide", { ground: null, free: "banding", axis: "banding", miracle: false,
                                moves: 2 },
            "both works band " + pyText(bFrom.axis) + ", at "
            + pyText(flt(r4(Number(bFrom.periodPx)))) + " and "
            + pyText(flt(r4(Number(bTo.periodPx)))) + " px, so the parts slide along one symmetry");
        no("stripes", "the two band families run the same way, so nothing crosses");
      } else {
        yes("stripes", { ground: null, free: "banding", axis: "banding", miracle: false,
                         moves: 2 },
            "the two band families cross — " + pyText(bFrom.axis) + " against "
            + pyText(bTo.axis) + " — so the fabric becomes stripes");
        no("symmetry-slide", "the two band families run different ways, so there is no one "
           + "symmetry to slide along");
      }

      // 6 · A WORK FOLDING ALONG STRONG DIRECTIONS FOLDS INTO A BOX. The charter's five-condition
      // box law of 12.08 23:49 pardons the box on measurement rather than on argument, and its
      // FIRST condition is the one a composer can answer: the crease is placed on the departing
      // work's own measured region line. So the qualification is the departing work's region
      // reading above the tight floor and a cut of at least four faces on its own record. The other
      // four conditions — live pictures on every face, a contact shadow on every edge, true
      // perspective, an exact landing — belong to an instrument that cuts on panels, and this
      // collection has none. The road is therefore disqualified by its instrument and not by its
      // measurements, and it says so: the day such an instrument lands, this road goes live on one
      // line of INSTRUMENT_OF_KIND.
      if (!(Number(gFrom.score || 0) >= floors.regions_tight)) {
        no("box-fold", "the departing work reads regions at "
           + pyText(flt(r4(Number(gFrom.score || 0)))) + ", under the tight floor of "
           + pyText(flt(floors.regions_tight)) + ", so there is no measured line to crease on");
      } else if (facesOf(fromW) < BOX_FACES) {
        no("box-fold", "the departing work cuts into " + facesOf(fromW) + " real panels, under the "
           + BOX_FACES + " faces a box needs");
      } else if (!(shared.per.regions && shared.per.regions.both)) {
        no("box-fold", "the two works do not both clear the region measure's own discriminating "
           + "threshold, so the region division is no ground this pair shares");
      } else if (!holdable(fromW, toW, "regions")) {
        // A ROAD THAT CANNOT HOLD ITS OWN GROUND IS NOT A ROAD. The ground it stands on is the
        // region division, which cuts on panels, and a work with no real panel set of its own has
        // nothing for the fold to be placed on — the road would run under its own name and fold
        // nothing at all.
        no("box-fold", "one of the two works carries no real panel set, so the region division has "
           + "no faces to fold on this pair");
      } else if (!instrumentOfKind("panel")) {
        no("box-fold", "the measurements qualify, and the road needs "
           + MISSING_INSTRUMENT.panel);
      } else {
        yes("box-fold", { ground: "regions", free: null, axis: "far", miracle: true,
                          mustFold: true, moves: 3 },
            "the departing work reads regions at "
            + pyText(flt(r4(Number(gFrom.score || 0)))) + " over " + facesOf(fromW) + " faces");
      }

      // 7 · A ROAD ALONG THE PAIR'S DISSIMILAR AXES, WITH THE MYSTERY IN THE MIDDLE. It qualifies
      // where the axes really do stand apart: the widest reading of the pair has to clear the same
      // distance a culmination is measured by, so the middle has something to be a mystery about.
      // Its shaping is the one this file has always had, which is why a pair that takes this road
      // composes what stage 0 composed for it.
      var farAxis = travellingAxisOn(fromW, toW, heldGround, floors, "far");
      if (farAxis === null) {
        no("dissimilar-mystery", "no measure carries a usable reading on both works");
      } else if (num(farAxis.delta) < CULMINATION_DISTANCE) {
        no("dissimilar-mystery", "the widest axis is " + farAxis.axis + " at "
           + pyText(farAxis.delta) + " apart, under the "
           + pyText(flt(CULMINATION_DISTANCE)) + " a mystery middle asks for");
      } else {
        yes("dissimilar-mystery", { ground: null, free: null, axis: "far", miracle: true,
                                    moves: 2 },
            "the two works read " + farAxis.axis + " " + pyText(farAxis.delta) + " apart");
      }

      return { roads: roads, notes: notes };
    }

    // How many real panels the departing work cuts into — the box law's faces, counted off the
    // work's own element sets rather than assumed. PANELS ONLY: a named region is a thing in the
    // picture and a panel is a piece of the frame, and it is pieces of the frame that become faces
    // of a solid. Counting named regions here let the road qualify on works the fold's own ground
    // could never be cast from.
    function facesOf(work) {
      var most = 0, i, s;
      for (i = 0; i < work.sets.length; i++) {
        s = work.sets[i];
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

    function familyOf(road, fromW, toW, floors, seed) {
      // The ground is rolled on the edge's own key, so this predicts the same one `compose` will
      // stand on — and the same one whichever way the passage runs.
      var p = pivotOfPair(fromW, toW, road.free, road.ground, false, seed,
                          groundKeyOf(fromW, toW));
      var held = p.kind === "shared-measure" ? p.value.measure : null;
      var axis = travellingAxisOn(fromW, toW, held, floors, road.axis);
      if (axis === null && road.axis !== "far" && road.axis !== "near") {
        axis = travellingAxisOn(fromW, toW, held, floors, "far");
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
    // The role does two things and no third. It BOUNDS what the composer emits, which is the budget
    // above. And it names the register the composer reaches for — which roads belong to a quiet
    // link and which to a culmination — so two neighbouring edges of one walk stop resembling each
    // other even where the two pairs read alike.
    var ROLE_BUDGETS = {
      "entrance":    { tier: "middle", duration: 5000, miracle: false, letters: 2 },
      "quiet link":  { tier: "quiet", duration: 3000, miracle: false, letters: 1 },
      "middle":      { tier: "middle", duration: 6500, miracle: true, letters: 2 },
      "culmination": { tier: "culmination", duration: 11000, miracle: true, letters: 3 },
      "return":      { tier: "quiet", duration: 4000, miracle: false, letters: 1 }
    };
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

    // THE ROAD THIS PASSAGE RUNS ON: what qualifies, what the role reaches for, what the visit
    // already played on this edge, and the die over whatever is left.
    // One road standing on a named ground, without touching the road it was made from.
    function withGround(road, ground) {
      var out = {}, k;
      for (k in road) out[k] = road[k];
      out.ground = ground;
      out.free = road.free === ground ? null : road.free;
      return out;
    }

    function roadFor(fromW, toW, floors, role, memory, seed, key) {
      var found = roadsFor(fromW, toW, floors);
      var pool = found.roads.slice(), reach = null, held = null, wanted, kept, i, fam;
      if (!pool.length) {
        return { road: BRIDGE_ROAD, order: [BRIDGE_ROAD],
                 family: familyOf(BRIDGE_ROAD, fromW, toW, floors, seed), notes: found.notes,
                 qualified: [], reach: null, heldFamily: null, heldBy: null };
      }
      // A ROAD THAT MUST SPEND THE MIRACLE IS UNREACHABLE WHERE THE ROLE HAS NONE. The other roads
      // that MAY spend one simply do not, when the reading that would fold the space does not stand;
      // this one cannot play at all without folding, because the fold IS what it is. Shelf 17 gives
      // a quiet link no miracle, and this seat gives an entrance and a return none either, so the
      // road leaves the pool at those three roles — the pool AND the fallback order, so a step that
      // spends no miracle cannot arrive at it by falling through.
      var spendsAMiracle = ROLE_BUDGETS[role] && ROLE_BUDGETS[role].miracle;
      if (!spendsAMiracle) {
        found.roads = found.roads.filter(function (r) { return !r.mustFold; });
        pool = pool.filter(function (r) { return !r.mustFold; });
        if (!pool.length) {
          return { road: BRIDGE_ROAD, order: [BRIDGE_ROAD],
                   family: familyOf(BRIDGE_ROAD, fromW, toW, floors, seed), notes: found.notes,
                   qualified: [], reach: "the step is a " + role + " and every road this pair "
                     + "qualifies for spends the one miracle shelf 17 does not give it",
                   heldFamily: null, heldBy: null };
        }
      }
      wanted = ROLE_ROADS[role];
      if (wanted) {
        kept = pool.filter(function (r) { return wanted.indexOf(r.id) >= 0; });
        if (kept.length) {
          kept.sort(function (x, y) { return wanted.indexOf(x.id) - wanted.indexOf(y.id); });
          pool = kept;
        } else {
          reach = "the step is a " + role + " and no road this pair qualifies for belongs to that "
            + "register, so it plays the road it has";
        }
      }
      // THE VISIT'S MEMORY. §4.8: what holds across a return is the family AND the pivot, and
      // everything else — the order of the moves, the actors, the rhythm, the camera's route — may
      // differ; the walk refuses a passage that shares neither. Before this lane the two held only
      // because the derivation read the pair and never the direction, so kinship was an accident of
      // there being one road. The roads read the direction — an arriving work reading on rings is
      // not an arriving work reading on rings the other way about — so the kinship is answered here
      // instead, in three steps, each weaker than the one before it and each still lawful:
      //
      //   1. a road this pair still qualifies for whose family IS the recorded one. The die is not
      //      rolled at all: kinship outranks variety, and the variety is carried by everything the
      //      family does not fix — the order of the moves, the actors and the rhythm below.
      //   2. failing that, a road standing on the same PIVOT, which §4.8 accepts in the family's
      //      place. The recorded family's first half is the pivot's own transform, so the three
      //      fields that cross carry this without §4.8 widening by a field.
      //   3. failing that, the ground the recorded transform implies is FORCED onto the road the
      //      die picked, so the pivot holds even where no road would have stood on it by itself.
      //
      // Where all three fail the crossing takes its own road and says so, and the walk's own judge
      // is what decides whether that is a passage it will play.
      var wantTransform = memory && memory.family ? String(memory.family).split("+")[0] : null;
      var heldBy = null;
      if (memory && memory.family) {
        var whole = pool.concat(found.roads).concat([BRIDGE_ROAD]);
        for (i = 0; i < whole.length; i++) {
          if (familyOf(whole[i], fromW, toW, floors, seed) === memory.family) {
            held = whole[i];
            heldBy = "family";
            break;
          }
        }
        if (held === null) {
          for (i = 0; i < whole.length; i++) {
            fam = familyOf(whole[i], fromW, toW, floors, seed);
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
          held = withGround(pool[dieAmong(seed, key, pool.length)],
                            MEASURE_OF_TRANSFORM[wantTransform]);
          heldBy = "ground";
          reach = "the visit remembers «" + String(memory.family) + "» on this edge and no road "
            + "reaches it, so its ground is held under the road the die picked";
        }
        if (held === null) {
          reach = "the visit remembers the family «" + String(memory.family) + "» on this edge and "
            + "this pair can hold neither it nor its pivot, so the crossing takes a road of its own";
        }
      }
      var at = dieAmong(seed, key, pool.length);
      var road = held || pool[at];
      // THE ORDER THE ROADS ARE TRIED IN. A road can still turn out unplayable for this pair after
      // the die has picked it — the placement law of §7's coverage rule refuses a stack whose
      // lowest cue leaves the frame open, and a cut can turn out to hold only the whole frame — and
      // a step of the walk still has to play. So the die's own pick comes first, the rest of the
      // qualifying pool follows in the die's own rotation, and the universal bridge closes the
      // list: that is his brief's «where none qualifies, the tonal and spectral bridge stays the
      // last candidate, so no pair is left without a road», read one step further out.
      var order = [road], i2;
      for (i2 = 0; i2 < pool.length; i2++) {
        var next = pool[(at + i2) % pool.length];
        if (order.indexOf(next) < 0) order.push(next);
      }
      // A road the role's register does not name still beats no crossing at all, so the roads this
      // pair qualifies for outside the register follow, and only then the bridge.
      for (i2 = 0; i2 < found.roads.length; i2++) {
        if (order.indexOf(found.roads[i2]) < 0) order.push(found.roads[i2]);
      }
      if (order.indexOf(BRIDGE_ROAD) < 0) order.push(BRIDGE_ROAD);
      return { road: road, order: order, family: familyOf(road, fromW, toW, floors, seed),
               notes: found.notes,
               qualified: found.roads.map(function (r) { return r.id; }),
               reach: reach, heldFamily: held ? memory.family : null, heldBy: heldBy };
    }

    // ---- composing one ordered pair ----

    function compose(key, pair, fromW, toW, floors, road, role, memory) {
      var pivot = pivotOf(pair), kind = pivot.elementKind, i;
      if (pivot.measure === "banding") {
        var fracs = [];
        [fromW, toW].forEach(function (w) {
          if (w.frameSide) fracs.push(w.structure.banding.periodPx / w.frameSide);
        });
        if (fracs.length) pivot.bandPeriodFrac = r4(Math.min.apply(null, fracs));
      }
      // WHICH INSTRUMENT PLAYS THE GROUND. Several may cut on its kind, so the pair's own readings
      // and the die decide between them; what each candidate answered stands on the plan.
      var castPivot = castOnKind(kind, fromW, toW, floors, !(ROLE_BUDGETS[role] || {}).miracle,
                                 pair.seed, key, "pivot");
      var pivotInstr = castPivot[0];
      var castNotes = { pivot: castPivot[1] };
      if (pivotInstr === null || pivotInstr === undefined) {
        if (!instrumentsOfKind(kind).length) {
          return [null, "pivot needs " + (MISSING_INSTRUMENT[kind]
                                          || ("an instrument that cuts on " + pyText(kind)))];
        }
        return [null, "no instrument that cuts on " + pyText(kind) + " can play this pair: "
                + castPivot[1].map(function (n) { return "«" + n.instrument + "» " + n.why; })
                  .join("; ")];
      }
      if (kind === "wedge") {
        var refs = [["a", fromW], ["b", toW]];
        for (i = 0; i < refs.length; i++) {
          if (setFor(refs[i][1], "wedge") === null) {
            return [null, "the shared turn cuts on wedges and work " + refs[i][0]
                    + " has no wedge set: rotational order 2 is the measurement floor"];
          }
        }
      }
      // THE ROAD PICKS THE TRAVELLING AXIS. "far" is the reading this file has always had and the
      // pair that takes a road carrying it composes exactly what stage 0 composed; a road built on
      // the pair's own device pins the axis to the measure it is built on; a road along what the
      // pair shares runs along their closest reading instead.
      var axis = travellingAxisOn(fromW, toW, pivot.measure, floors, road.axis);
      var travelInstr = null, travelDecline = null, tkind;
      if (axis === null && road.axis !== "far" && road.axis !== "near") {
        // The road's own axis has gone out from under it — the ground took it, or a reading fell
        // under a floor between the qualification and here. The pair still crosses, on the widest
        // axis it has, and the plan says the road did not get its own.
        axis = travellingAxisOn(fromW, toW, pivot.measure, floors, "far");
      }
      if (axis === null) {
        travelDecline = "no measure carries a usable reading on both works";
      } else {
        tkind = KIND_OF_AXIS[axis.axis];
        var castTravel = castOnKind(tkind, fromW, toW, floors,
                                    !(ROLE_BUDGETS[role] || {}).miracle, pair.seed, key, "travel");
        travelInstr = castTravel[0];
        castNotes.travel = castTravel[1];
        if (travelInstr === null || travelInstr === undefined) {
          travelInstr = null;
          travelDecline = "the travelling axis needs "
            + (MISSING_INSTRUMENT[tkind] || ("an instrument that cuts on " + pyText(tkind)));
        } else if (travelInstr === pivotInstr) {
          travelInstr = null;
          travelDecline = "the travelling axis cuts on the same instrument as the pivot";
        } else if (spendsTheMiracle(travelInstr) && !(ROLE_BUDGETS[role] || {}).miracle) {
          // THE OTHER DOOR THE FOLD COULD COME THROUGH. The ground is gated where it is chosen, and
          // the travelling axis is gated here: a step whose role carries no miracle cannot fold the
          // world on its travelling cue either, whichever measure happens to cut on it.
          travelInstr = null;
          travelDecline = "the travelling axis cuts on an instrument that folds the world, and the "
            + "step is a " + role + ", which shelf 17 gives no miracle";
        }
      }
      var cast = castActors(fromW, toW, pivot, axis);
      if (cast[0] === null) return [null, "actor refusal: " + cast[1]];
      var actors = cast[0];

      var arrived = locusOf(toW, floors), locusKind = arrived[0], locus = arrived[1];
      var arrival = locusKind !== "none" ? "CONDENSED" : "CARRIED";
      var arrivalInstr = arrival === "CONDENSED" ? "matter" : null;
      if (arrivalInstr === pivotInstr) arrivalInstr = null;
      var departing = locusOf(fromW, floors);
      var arrivalLeads = !!arrivalInstr && figureOnLocus(fromW, departing[1]);

      // THE VISIT'S MEMORY, on this side of the line. §4.8 lets three fields cross — the family,
      // the seed and the pass index — and the family is what `roadFor` above holds. What the pass
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

      // EVERY HANDLE THE CHOSEN INSTRUMENTS PUBLISH HAS TO NAME ITS MEASUREMENT, and the question
      // is asked here, where it can still be answered with a refusal. His 19:13 word lifted to the
      // class at 19:21 binds the composer as much as the instrument: a score driving a handle this
      // file cannot say the provenance of would be a number nobody read reaching the picture. An
      // instrument that grows a handle before the register names it therefore stands down, with the
      // handle named, and the visitor lands on the walk's own glide.
      var unnamedHandle = null;
      [pivotInstr, travelInstr, arrivalInstr].forEach(function (iid) {
        if (!iid || unnamedHandle || !MANIFESTS[iid]) return;
        Object.keys(MANIFESTS[iid].handles).forEach(function (h) {
          if (MANIFESTS[iid].handles[h].open || HANDLE_SOURCE[h] || unnamedHandle) return;
          unnamedHandle = "the instrument «" + iid + "» publishes the handle «" + h
            + "» and no measurement is written for it";
        });
      });
      if (unnamedHandle) return [null, unnamedHandle];

      var cam = cameraFlight(pair, axis, locus);
      var mesh = null, why = null, made;
      if (pivotInstr === "gears" || travelInstr === "gears") {
        made = meshingTravel(fromW, toW, pivot);
        mesh = made[0];
        why = made[1];
        if (mesh !== null) {
          made = askTheDoors(mesh);
          mesh = made[0];
          why = made[1];
        }
        if (mesh === null) {
          if (pivotInstr === "gears") return [null, why];
          travelInstr = null;
          travelDecline = why;
        }
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
      var folds = pivotInstr === "boxfold" || travelInstr === "boxfold"
        || arrivalInstr === "boxfold";
      var couldFold = travelInstr ? worldOf(toW, floors, axis) : null;
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
      var distance = axis ? num(axis.delta) : 0.0;
      var voices, tier, letters, accs, k, instrumentOf, stackOrder, placed, capped = [];
      // WHICH CUE FOLDS THE FRAME, or nothing. It is re-read on every turn of the budget loop
      // below, because the loop can retire the very cue that folds.
      var foldsOn = null;

      // THE ROLE'S BUDGET IS A BOUND ON WHAT IS EMITTED, not a wish. Shelf 17 counts letters, and a
      // quiet link carries exactly one; a step whose pair offers more moves than its role may spend
      // gives them up here rather than at the gate. The travelling move goes first, because the
      // ground and the arrival are the two the charter names by role, and the plan records every
      // move it gave up so a thin passage can be read back to the reason it is thin.
      for (;;) {
        foldsOn = pivotInstr === "boxfold" ? "pivot"
          : (travelInstr === "boxfold" ? "travel"
             : (arrivalInstr === "boxfold" ? "arrival" : null));
        var voiced = voiceTheCues(travelInstr !== null, arrivalInstr !== null, world, distance,
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
        // THE PLACEMENT LAW IS THE SECOND BOUND, and it retires a move for the same reason the
        // budget does. §7's coverage law lets only the LOWEST cue leave the frame open, and this
        // collection's one instrument that fills the frame whole is the woven one; a stack of the
        // meshing and the material instruments therefore has no ground, and the contract's own
        // sentence exempts a one-cue score because nothing stands beneath it. So a plan the law
        // refuses gives up its travelling move and then its arrival — exactly what a refused
        // meshing travel or an axis cutting on the pivot's own instrument already do here — rather
        // than refusing the visitor a crossing. The plan carries what it gave up and why.
        instrumentOf = {};
        if (pivotInstr && voices.pivot) instrumentOf.pivot = pivotInstr;
        if (travelInstr && voices.travel) instrumentOf.travel = travelInstr;
        if (arrivalInstr && voices.arrival) instrumentOf.arrival = arrivalInstr;
        stackOrder = CUE_IDS.filter(function (c) { return instrumentOf[c] !== undefined; });
        placed = placeTheStack(stackOrder, instrumentOf);
        var fits = placed[0] !== null
          && letters <= roleBudget.letters
          && TIER_RANK[tier] <= TIER_RANK[roleBudget.tier];
        if (fits) break;
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

      if (placed[0] === null) return [null, placed[1]];
      var stacks = placed[0];
      var reordered = stackOrder.filter(function (c, i2) { return stacks[c] !== i2; });

      var judged = tierFor(voices, tier), row = judged[0], counts = judged[1];
      if (row === null) {
        return [null, "the declared tier " + tier + " and the realised voices disagree: "
                + counts.letters + " letters, " + counts.accompaniments + " accompaniments, "
                + counts.miracles + " miracles"];
      }
      // THE STEP'S OWN LENGTH. Shelf 17 gives each role a band of seconds and the role names the
      // length it takes inside that band; where the pair could not reach its role's tier the
      // realised tier's own length stands instead, so a plan never declares a tier its duration
      // contradicts — the disagreement §4.7 calls a red.
      var duration = row.tier === roleBudget.tier ? roleBudget.duration : row.duration;
      // The deviation this pass puts on the rhythm. It moves no window's close, so the ends below
      // read the same numbers whatever it is.
      var rhythmShift = passIndex
        ? r4((dieAmong(pair.seed, key + "|rhythm", 2001) / 1000.0 - 1.0) * RHYTHM_REACH) : 0;
      var windows = cueWindows(travelInstr !== null, arrivalLeads, travelInstr, rhythmShift);
      var ends = CUE_IDS.filter(function (c) { return voices[c] !== undefined; })
        .map(function (c) { return windows[c][1]; });
      var derivedMs = roundToInt(Math.max.apply(null, ends) * duration);
      if (!(derivedMs > 0 && derivedMs <= TRANSACTION_MS)) {
        return [null, "the derived duration " + derivedMs + " ms stands outside §2.5's "
                + "transaction bound of " + TRANSACTION_MS + " ms"];
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
        rhythmShift: rhythmShift
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
        road: road.id, roadWhy: road.why, role: role, passIndex: passIndex,
        capped: capped, miracleDecline: miracleDecline, castNotes: castNotes
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
        // the share of the frame the work's measured open ground holds
        voidShare: Number(mot.voidShare) || 0,
        // the share of the frame the work's dominant object holds, off its own measured box
        figureShare: Math.max(0, (box[2] - box[0])) * Math.max(0, (box[3] - box[1])),
        // how strongly the work reads as radial, and how many rings its own cut measured
        radialScore: Number((st.radial || {}).score) || 0,
        ringGrain: ring ? Number(ring.measuredGrain) || 0 : 0,
        // how much finer the work's own measured repeat is than the cut it was given
        ringMerge: ring ? Number(ring.mergeFactor) || 0 : 0,
        // the strip family the woven instrument cuts on
        strips: strip && strip.realCount ? Number(strip.count) || 0 : 0,
        // how strongly the work already reads as a corridor, and where its own horizon stands —
        // the two the folding instrument's perspective and its eye's ride are placed by
        tunnel: Number((st.polar || {}).tunnel) || 0,
        horizonY: ((st.horizon || {}).y === null || (st.horizon || {}).y === undefined)
          ? null : Number(st.horizon.y),
        // the repeat the work carries ACROSS a crease, as a count over its own frame side
        gridCount: side > 0 && Number((st.grid || {}).periodPx) > 0
          ? side / Number(st.grid.periodPx) : 0,
        // how much of the difference between the work's own columns its region line explains
        regionScore: Number((st.regions || {}).score) || 0,
        // the work's own device: how many regions it falls into, the step it was cut at and the
        // angle of that step — what a passage revealing the making has to read
        regionCount: Number((st.regions || {}).count) || 0,
        deviceStepPx: Number((st.ownDevice || {}).stepPx) || 0,
        deviceAngleDeg: Number((st.ownDevice || {}).angleDeg) || 0,
        gridPeriodPx: Number((st.grid || {}).periodPx) || 0,
        gridAngleDeg: Number((st.grid || {}).angleDeg) || 0,
        frameSide: side,
        // how confidently the work's own device was recovered — how legibly its making reads
        deviceConfidence: Number((st.ownDevice || {}).confidence) || 0
      };
    }

    function workParts(work, floors, at) {
      var sets = {}, counts = {}, fig = {}, ends = {}, lists = {}, i, s, reading;
      for (i = 0; i < work.sets.length; i++) {
        s = work.sets[i];
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
        reading = axisReading(work, TRAVEL_AXES[i], floors);
        if (reading !== null) ends[TRAVEL_AXES[i]] = encodeEnds(TRAVEL_AXES[i], reading);
      }
      var found = locusOf(work, floors), locusKind = found[0], locus = found[1];
      var polar = work.structure.polar || {}, keys = Object.keys(POLAR_WORLD).sort();
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
        locus: [LOCUS_KINDS.indexOf(locusKind)].concat(locus || [0, 0]),
        world: (best && bestv && bestv > 0) ? WORLDS.indexOf(POLAR_WORLD[best]) : -1,
        providerOf: (function () {
          var out = {};
          work.sets.forEach(function (s2) { out[s2.index] = s2.provider; });
          return out;
        }())
      };
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

    function clamp01(v) { return v < 0 ? 0 : (v > 1 ? 1 : v); }
    function fractional(v) { return v - Math.floor(v); }

    // The golden angle of a count: charter shelf 13's stagger instrument, which is what keeps no
    // two fragments of a cascade in line. The constant is the golden section itself and is
    // measured by nothing, because it is a number rather than a reading.
    var GOLDEN = 0.6180339887;
    function goldenStagger(count) { return fractional(count * GOLDEN); }

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

      var locusKind = LOCUS_KINDS[num(toP.locus[0])];
      var arrival = { mode: locusKind !== "none" ? "CONDENSED" : "CARRIED",
                      locusKind: locusKind,
                      locus: locusKind === "none" ? null : [toP.locus[1], toP.locus[2]] };

      var castOf = { pivot: ["pivot-carrier"], travel: ["traveller"],
                     arrival: ["arriving-figure", "departing-figure"] };
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
          var ax = fromP.ends.banding;
          if (ax !== undefined && ax !== null) {
            if (num(ax[2]) < BANDING.length) wanted.axis = AXIS_OF_BANDING[BANDING[num(ax[2])]];
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
          if (n) wanted.speed = flt(r4(betweenSpans("weave", "strips", "speed", n)));
        } else if (instr === "gears") {
          if (num(row[11]) >= 0) {
            wanted.ratio = row[13];
            wanted.centreX = flt(r4((num(row[6]) + num(row[8])) / 2.0 + 0.5));
            wanted.centreY = flt(r4((num(row[7]) + num(row[9])) / 2.0 + 0.5));
            wanted.size = [row[11], row[12]];
            if (num(row[14]) >= 0) wanted.bandPeriod = row[14];
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
          // HOW DEEP THE PERSPECTIVE IS, off the departing work's own corridor reading: a picture
          // that already reads as depth is turned in a deeper box.
          if (mf.tunnel > 0) wanted.depth = flt(r4(clamp01(mf.tunnel)));
          // HOW FAR THE EYE RIDES UP THROUGH THE QUARTER, off the departing work's own measured
          // horizon: the ride starts from where that work already stands. A work whose horizon was
          // never measured leaves the handle at the module's own rest.
          if (mf.horizonY !== null) wanted.dip = flt(r4(clamp01(mf.horizonY)));
          // THE CREASE'S OWN LINE DOES NOT TRAVEL, so the instrument is told so rather than being
          // let fold on a line nobody measured. A work record carries the region split's COUNT and
          // its SCORE and no position at all, so `seam` is left at the instrument's own edge and
          // `seamScore` is handed at nothing — under the module's own floor, which is the reading
          // that sends the crease back to that edge and says why. The day the position travels,
          // this is the one place that changes.
          wanted.seamScore = flt(r4(0.0));
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
          var angle = made.deviceStepPx > 0 ? made.deviceAngleDeg : made.gridAngleDeg;
          if (stepPx > 0 && made.frameSide > 0) {
            wanted.parquetPeriod = flt(r4(clamp01(stepPx / made.frameSide)));
          }
          wanted.parquetTurn = flt(r4(clamp01(fractional(Math.abs(angle) / 90.0))));
          // THE PLANE IS LAID AWAY AT THE SAME MEASURED ANGLE, which is what puts the parquet in
          // perspective rather than flat to the eye.
          wanted.tilt = flt(r4(clamp01(fractional(Math.abs(angle) / 90.0))));
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
        }
        var measured = {}, nodes = {};
        // THE LAST GUARD, and it should never fire: `compose` above refuses a plan whose
        // instruments publish a handle this register does not name, by name and before the fill, so
        // the passage takes the walk's own glide instead of throwing inside `declare`. This stands
        // because the fill is reachable from the choice core directly and a throw here is a louder
        // failure than a wrong number.
        var unnamed = Object.keys(c.tracks).filter(function (h) { return !HANDLE_SOURCE[h]; });
        if (unnamed.length) {
          throw new Error("the instrument «" + c.instrument.id + "» publishes the handle «"
                          + unnamed[0] + "» and no measurement is written for it: every geometric "
                          + "and temporal parameter names the measurement it reads");
        }
        Object.keys(c.tracks).sort().forEach(function (h) {
          var nodeName = (c.tracks[h] || {}).node || (c.id + "-" + h);
          var why = HANDLE_SOURCE[h][1];
          var req = wanted[h] === undefined ? null : wanted[h];
          if (h === "mix") {
            nodes[nodeName] = { op: "mix", a: c.doors["in"].value, b: c.doors.out.value,
                                t: { source: "cueProgress" }, note: why };
            return;
          }
          if (h === "clock") {
            nodes[nodeName] = { source: "time", note: why };
            return;
          }
          if (Array.isArray(req)) {
            var ends2 = req.map(function (v) { return appliedValue(instr, h, v); });
            measured[h] = req;
            nodes[nodeName] = { op: "mix", a: ends2[0][1], b: ends2[1][1],
                                t: { source: "cueProgress" },
                                note: noteFor(h, req, ends2.map(function (e) { return e[1]; }),
                                              why) };
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
        var span = travel ? travel.window
          : [flt(r4(duration / 4000.0)), flt(r4(3 * duration / 4000.0))];
        camera.track[1].at = span[0];
        camera.track[1].pan = { x: row[6], y: row[7] };
        camera.track[1].logScale = row[10];
        camera.track[2].at = span[1];
        camera.track[2].pan = { x: row[8], y: row[9] };
        camera.track[2].logScale = row[10];
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
      // THE LINE IS MEASURED AGAINST THE FENCE IT HAS TO PASS. The clauses this lane added are the
      // ones that go first, in the order of what a person can most afford to lose: the pass count,
      // then the road's own opening. What was there before this lane is never touched, so a line
      // that fitted still fits and a line that would not have fitted arrives shortened rather than
      // refused whole. Which clauses were dropped stands on the plan.
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
      var duration = planDurationMs(plan);
      if (duration === null) return [null, "the plan names no duration and no cue names a window"];
      var direction = plan.direction === "a->b" ? "a-to-b"
        : (plan.direction === "b->a" ? "b-to-a" : null);
      if (direction === null) {
        return [null, "direction " + pyText(plan.direction) + " is none the table maps"];
      }
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

    // ---- the choice core: two works, a direction and a die ----

    function scoreFor(a, b, direction, seed, role, memory) {
      // Two works, a direction, the step's role, what the visit already played here and a die: the
      // whole crossing, decided here and now.
      var tag = direction === "b-to-a" ? "ba" : "ab";
      var key = a.id + "__" + b.id + "__" + tag;
      var fromW = tag === "ab" ? a : b, toW = tag === "ab" ? b : a;
      var step = ROLE_BUDGETS[role] ? role : "middle";
      // Whether this step of the walk may spend the one miracle at all — shelf 17's budget, read
      // once here so the ground, the roads and the voicing all answer to one reading of it.
      var spendsAMiracle = !!ROLE_BUDGETS[step].miracle;
      var chosen = roadFor(fromW, toW, FLOORS, step, memory || null, seed, key);
      var dir = tag === "ab" ? "a-to-b" : "b-to-a";
      var tried = [], made = null, pair = null, ran = null, i3;
      for (i3 = 0; i3 < chosen.order.length; i3++) {
        ran = chosen.order[i3];
        pair = pairOf(a, b, dir, seed, ran.free, ran.ground, !spendsAMiracle);
        made = compose(key, pair, fromW, toW, FLOORS, ran, step, memory || null);
        if (made[0] !== null) break;
        tried.push({ road: ran.id, why: made[1] });
      }
      if (made[0] === null) {
        return { key: key, declined: made[1], road: ran.id, family: chosen.family,
                 roads: chosen.qualified, roadNotes: chosen.notes, roadDeclines: tried };
      }
      chosen.road = ran;
      var plan = made[0];
      // WHICH OF A WORK'S OWN CUTS ACTS. Nothing recorded on this edge leaves it exactly where it
      // has always been; a further pass moves it by the die and the pass count, which is §4.8's
      // «the element selection may differ».
      var cast = plan.passIndex
        ? plan.passIndex + dieAmong(seed, key + "|actors", 97) : 0;
      var tpl = buildTemplate(plan.shape, plan.spec);
      var row = rowOf(plan);
      var pv = plan.pivot;
      var ctx = {
        pivot: [pv.kind, pv.measure, pv.cut, pv.transform, pv.elementKind, pivotKindsOf(pv)],
        fromParts: workParts(fromW, FLOORS, cast),
        toParts: workParts(toW, FLOORS, cast)
      };
      var filled = fillPlan(key, row, tpl, ctx);
      // THE FAMILY THE WALK WILL READ, read the same way the walk reads it: off the composed plan,
      // by the transform the pivot's cut implies and the measure the passage travels. It is handed
      // back here so the walk's edge record and this file's own kinship step name one thing.
      chosen.family = familyToken(filled.pivot.transform,
                                  filled.travellingAxis ? filled.travellingAxis.measure : null);
      var out = serialise(filled);
      if (out[0] === null) return { key: key, declined: out[1] };
      var text = writeJson(out[0], 0);
      var tight = writeJsonTight(out[0]);
      return { key: key, score: out[0], json: text, bytes: tight.length,
               overTheFence: SCORE_FENCE_BYTES ? tight.length > SCORE_FENCE_BYTES : false,
               shape: plan.shape, plan: filled, version: COMPOSER_VERSION,
               // The derivation's own reading, for the diagnostic surface and for the walk's edge
               // record: which road this passage ran on, the family the walk hands back on a
               // return, every road the pair qualified for, and why each of the rest did not.
               road: plan.road, family: chosen.family, roads: chosen.qualified,
               roadNotes: chosen.notes, roadReach: chosen.reach,
               heldFamily: chosen.heldFamily, heldBy: chosen.heldBy, capped: plan.capped,
               roadDeclines: tried, miracleDecline: plan.miracleDecline,
               travelDecline: plan.travelDecline,
               // HOW FAR THIS PAIR'S OWN RECORDS SEND THE FLIGHT. The dolly comes from the two
               // works' measured door steps and the pan from their measured radial centres or the
               // arriving work's locus, so this is a reading of the pair and not a preference. A
               // flight that barely moves cannot carry a passage on its own, and the entry reads
               // this before it asks for a led one.
               //
               // WHAT IS READ IS THE PAN AND NOT THE APPROACH, and the reason is measured: the
               // dolly stands AT its own cap for three quarters of the collection, because the two
               // works' door steps stand far enough apart that the clamp saturates. A number that
               // is the same for three pairs in four carries no reading of any pair, so it cannot
               // decide anything; the pan travels the frame and does differ pair by pair. The
               // approach is also what every flight makes anyway, since the anchor runs between the
               // two hangs whether the camera leads or accompanies. `cameraReach` publishes both,
               // the dolly as a share of its own cap so it survives a change of unit in the camera
               // flight section, which is another lane's half of this file.
               cameraReach: [r4(Math.abs(num(plan.camera.logScale)) / DOLLY_CAP),
                             r4(Math.hypot(
                               num(plan.camera.panTo[0]) - num(plan.camera.panFrom[0]),
                               num(plan.camera.panTo[1]) - num(plan.camera.panFrom[1])))],
               cameraTravels: Math.hypot(
                 num(plan.camera.panTo[0]) - num(plan.camera.panFrom[0]),
                 num(plan.camera.panTo[1]) - num(plan.camera.panFrom[1])) >= LEAD_SHARE };
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
    //                 function and the passage is read as a middle. Stage 0 records it and derives
    //                 nothing from it; a name outside the five is a refusal, so the vocabulary
    //                 cannot drift.
    //   sessionMemory the return reference of §4.8 — {family, seed, passIndex} naming the pass
    //                 already played on this edge in this visit, and nothing wider. Missing means
    //                 nothing has played on this edge yet. A field outside the three is a refusal:
    //                 §4.8's fence keeps the walk's own edge record on the site's side of the line.
    //   cameraState   the pose the camera rests in as the passage starts; the flight departs from
    //                 it. Missing means the walk stated no pose and the flight departs from the
    //                 score's own rest, which is what every passage does today.
    //   buffer        the canvas as it stands at this instant: {width, height, dpr, orientation,
    //                 quality}. Missing means the buffer is unstated; the instrument then reads the
    //                 one it is drawing on, which is the truth in either case (his 18:00 decision).
    //
    // WHAT COMES BACK. On a refusal, {key, declined, request} and no score. On success, everything
    // `scoreFor` hands back plus `request` — the request as it was read, defaults filled in — and
    // `applied`, which starts null. `applied` is the instrument's own reading of the buffer it drew
    // on, and it can only be known after the frame is drawn: the caller writes it onto this record
    // when the host reports, so one record carries the whole passage — what was asked, what came
    // back, and what was applied or refused.
    var ROUTE_ROLES = ["entrance", "quiet link", "middle", "culmination", "return"];
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
      var read = { routeRole: role, direction: direction, seed: seed, sessionMemory: memory,
                   cameraState: req.cameraState === undefined ? null : req.cameraState,
                   buffer: req.buffer === undefined ? null : req.buffer };
      function no(why) {
        return { key: key, declined: why, score: null, request: read, applied: null,
                 version: COMPOSER_VERSION };
      }
      if (!a || !a.id) return no("the passage request names no departing work record");
      if (!b || !b.id) return no("the passage request names no arriving work record");
      if (ROUTE_ROLES.indexOf(role) < 0) {
        return no("the passage request names the route role «" + String(role)
                  + "», which is none of " + ROUTE_ROLES.join(", "));
      }
      if (seed !== seed || seed < SEED_SPAN[0] || seed > SEED_SPAN[1]) {
        return no("the passage request's seed " + String(req.seed) + " stands outside "
                  + SEED_SPAN[0] + "…" + SEED_SPAN[1]);
      }
      if (memory !== null) {
        if (typeof memory !== "object" || Array.isArray(memory)) {
          return no("the passage request's session memory is no record");
        }
        var odd = Object.keys(memory).filter(function (f) {
          return SESSION_MEMORY_FIELDS.indexOf(f) < 0;
        });
        if (odd.length) {
          return no("the passage request's session memory names «" + odd[0] + "», outside the "
                    + "three fields §4.8 lets cross: " + SESSION_MEMORY_FIELDS.join(", "));
        }
      }
      var made = scoreFor(a, b, direction, seed, role, memory);
      // THE PASSAGE THE CAMERA LEADS. The camera lane built the capability and asks one field for
      // it: `camera.lead` says the flight itself is the transition, the anchor gives up its held
      // middle and the pose travels the whole duration without ever standing still. Choosing it is
      // a reading of the step's function in the route, which is why it belongs here rather than in
      // the choice core — the core never sees the role.
      //
      // The two homes are the quiet link and the return. Charter shelf 15 makes both TONIC, the
      // home the eye settles in, and shelf 17 gives a quiet link one move from the vocabulary, at
      // most one accompanying voice and no miracle — which is exactly the register a led passage
      // wants underneath it, because the camera is the world voice and a led flight spends it. A
      // culmination spends its voices elsewhere, and its miracle is the accent.
      //
      // Two readings gate it beyond the role. The pair's own records have to give the flight
      // somewhere to go, since a still flight leads nothing. And under the levels law one voice
      // holds one level, so a led score may never also give a cue the WORLD level: the host refuses
      // that combination before the command is taken and names the cue, and this side never emits
      // it.
      if (made.score && made.cameraTravels && LED_ROLES.indexOf(role) >= 0
          && !claimsTheWorld(made.score)) {
        made.score.camera.lead = true;
      }
      made.request = read;
      made.applied = null;
      if (made.declined !== undefined) made.score = null;
      else made.declined = null;
      return made;
    }

    return { passageFor: passageFor, scoreFor: scoreFor, routeRoles: ROUTE_ROLES.slice(),
             seedSpan: SEED_SPAN.slice(),
             version: COMPOSER_VERSION, writeJson: writeJson,
             writeJsonTight: writeJsonTight, r4: r4 };
  }

  join({ version: COMPOSER_VERSION, make: make });
})();
