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
  var INSTRUMENT_OF_KIND = {
    strip: "weave", band: "matter", scale: "matter", ring: "gears", wedge: "gears",
    tile: null, panel: null, region: null, field: null
  };
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
  var TRANSACTION_MS = 14000;
  var DOOR_HOLD = 0.08;
  var DOLLY_CAP = 0.5;
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
    axis: ["measured", "the banding axis cut-lines.json recorded"],
    size: ["measured", "the two works' measured ring counts"],
    ratio: ["measured", "the two works' measured ring counts, on seven steps"],
    bandPeriod: ["measured", "the pivot's own period as a fraction of frame height"],
    centreX: ["measured", "the midpoint of the two measured radial centres"],
    centreY: ["measured", "the midpoint of the two measured radial centres"],
    shade: ["module-rest", "a judge channel the module rests at 1"],
    travel: ["module-rest", "a judge channel the module rests at 1"],
    grain: ["uncalibrated", "the spectral reading exists in tone-texture.json; no scale between "
                            + "a detail size in pixels and this handle's 0 to 1 is recorded"],
    order: ["uncalibrated", "the rotational order exists in cut-lines.json; no scale between a "
                            + "turn count and this handle's 0 to 1 is recorded"],
    gather: ["uncalibrated", "the arriving figure's share exists in motifs.json; no scale "
                             + "between a share of frame and this handle's 0 to 1 is recorded"],
    loosen: ["uncalibrated", "the void share exists in motifs.json; no scale between it and "
                             + "this handle's 0 to 1 is recorded"],
    nMul: ["unmeasured", "no measurement in this tree bears on it"],
    press: ["unmeasured", "the hand's own pressure, which no build-time file measures"],
    speed: ["unmeasured", "no measurement in this tree bears on it"],
    drift: ["unmeasured", "no measurement in this tree bears on it"],
    tooth: ["unmeasured", "no measurement in this tree bears on it"],
    turn: ["unmeasured", "no measurement in this tree bears on it"],
    flank: ["unmeasured", "no measurement in this tree bears on it"]
  };

  var INTENT_TEMPLATES = {
    quiet: "The {pivotName} holds at {pivotStrength} and never moves, and the crossing is the one "
      + "held ground played through: {aCount} parts of the first work hand over to {bCount} of "
      + "the second along that cut, and the second work arrives {arrival}{locusPhrase}. "
      + "Shelves 9 the held pivot, 7 the arrival, 17 a quiet link.{registerPhrase}",
    "middle-travel": "The {pivotName} holds at {pivotStrength} and the ground stays while the "
      + "{axisName} travels from {fromValue} to {toValue}{centrePhrase}. One generator changes "
      + "over a held family, and the second work arrives {arrival}{locusPhrase}. Shelves 9 one "
      + "generator at a time, 12 the parts that become actors, 7 the arrival, 17 a "
      + "middle.{registerPhrase}",
    "middle-world": "The {pivotName} holds at {pivotStrength} and over it the flat picture "
      + "becomes a {worldName} the viewer stands inside: the {axisName} travels from {fromValue} "
      + "to {toValue}{centrePhrase}, and the second work arrives {arrival}{locusPhrase}. Shelves "
      + "8 the one folded space, 9 the held pivot, 7 the arrival, 17 a middle.{registerPhrase}",
    culmination: "The {pivotName} holds at {pivotStrength} and is the whole ground of a long "
      + "crossing: the {axisName} travels the wide distance from {fromValue} to "
      + "{toValue}{centrePhrase}, the flat picture opens into a {worldName}, and the second work "
      + "arrives {arrival}{locusPhrase}. Shelves 8 the one folded space, 9 the held pivot, 15 the "
      + "far pair, 17 a culmination.{registerPhrase}"
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
  // The three fields §4.4 lets a score's camera carry, and the four a plan carries and a score
  // never does.
  var CAMERA_ALLOWED = ["owner", "rests", "track"];
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
    var BANDING = (MANIFESTS.weave.handles.axis.banding) || [];
    var AXIS_OF_BANDING = {};
    BANDING.forEach(function (name, i) { AXIS_OF_BANDING[name] = i; });
    var RATIO_STEPS = MANIFESTS.gears.handles.ratio.rungs || 0;
    var SIZE_MAX = HANDLE_SPECS.gears.size[1];

    // ---- the pair, derived from the two works rather than looked up ----

    function sharedMeasure(a, b) {
      // pair-shared.py's own reading: the measures both works clear their discriminating
      // threshold on, and among those the one the WEAKER work carries most strongly.
      var held = [], per = {}, i, m, sa, sb;
      for (i = 0; i < MEASURES.length; i++) {
        m = MEASURES[i];
        sa = a.measures[m];
        sb = b.measures[m];
        per[m] = { min: r4(Math.min(sa, sb)), both: sa >= THRESHOLDS[m] && sb >= THRESHOLDS[m] };
        if (per[m].both) held.push(m);
      }
      if (!held.length) return null;
      var best = held[0];
      for (i = 1; i < held.length; i++) {
        if (per[held[i]].min > per[best].min) best = held[i];
      }
      return { measure: best, strength: per[best].min, held: held };
    }

    function pivotOfPair(a, b) {
      // The four pivots in the elements builder's own order of precedence.
      var shared = sharedMeasure(a, b), v, na, nb, strength, ra, rb, hues, i;
      if (shared) {
        v = { strength: shared.strength, measure: shared.measure,
              cut: CUT_OF_MEASURE[shared.measure][0],
              transform: CUT_OF_MEASURE[shared.measure][1],
              elementKind: KIND_OF_MEASURE[shared.measure] };
        return { kind: "shared-measure", value: v, rowStrength: r4(shared.strength) };
      }
      na = a.structure.rotational.n || 0;
      nb = b.structure.rotational.n || 0;
      if (na >= 3 && na === nb) {
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

    function pairOf(a, b, direction, seed) {
      // §4.3's PairDossier, in the shape `compose` reads it: the pivot the two works derive, the
      // two doors, this pair's readiness and the die the caller rolled.
      var chosen = pivotOfPair(a, b);
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

    function voiceTheCues(hasTravel, hasArrival, world, distance) {
      var culmination = !!world && hasArrival && distance >= CULMINATION_DISTANCE;
      var voices = {}, any = false, k;
      if (culmination) voices.pivot = "letter";
      else if (hasTravel || hasArrival) voices.pivot = "accompaniment";
      else voices.pivot = "letter";
      if (hasTravel) voices.travel = world ? "miracle" : "letter";
      if (hasArrival) voices.arrival = "letter";
      for (k in voices) if (voices[k] === "letter") any = true;
      if (!any) voices.pivot = "letter";
      var tier = culmination ? "culmination"
        : (!(hasTravel || hasArrival) ? "quiet" : "middle");
      return [voices, tier];
    }

    function tierFor(voices, tier) {
      var letters = 0, accs = 1, miracles = 0, k, row, i;
      for (k in voices) {
        if (voices[k] === "letter") letters += 1;
        else if (voices[k] === "accompaniment") accs += 1;
        else if (voices[k] === "miracle") miracles += 1;
      }
      var counts = { letters: letters, accompaniments: accs, miracles: miracles };
      for (i = 0; i < TIERS.length; i++) if (TIERS[i].tier === tier) row = TIERS[i];
      if (letters >= row.letters[0] && letters <= row.letters[1]
          && accs >= row.accompaniments[0] && accs <= row.accompaniments[1]
          && miracles >= row.miracles[0] && miracles <= row.miracles[1]) {
        return [row, counts];
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

    function cameraFlight(pair, axis, locus) {
      var doors = pair.doorFraming;
      var stepFrom = (doors.from || {}).stepPx, stepTo = (doors.to || {}).stepPx;
      var dolly = 0.0, panFrom = [0.0, 0.0], panTo = [0.0, 0.0], ca, cb;
      if (stepFrom && stepTo && stepFrom > 0 && stepTo > 0) {
        dolly = Math.max(-DOLLY_CAP, Math.min(DOLLY_CAP, Math.log2(stepTo / stepFrom)));
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

    function cueWindows(shapeHasTravel, arrivalLeads, travelInstrument) {
      var w = { pivot: [0.0, 1.0] };
      if (shapeHasTravel) {
        w.travel = travelInstrument === "gears" ? [0.0, 0.86] : [0.18, 0.86];
      }
      w.arrival = arrivalLeads ? [0.10, 1.0] : [0.62, 1.0];
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

    function tracksFor(instr, cueId) {
      var out = {}, handles = INSTRUMENTS[instr].handles, i;
      for (i = 0; i < handles.length; i++) out[handles[i]] = { node: cueId + "-" + handles[i] };
      return out;
    }

    function resourcesBlock(variant) {
      return { bytesEstimate: 0, framebuffers: 0, passes: 1, pingPong: 0, programs: 1,
               textureSlots: 2, textures: 0, variant: variant };
    }

    function buildTemplate(shape, spec) {
      var voices = spec.voices;
      var windows = cueWindows(spec.travel !== null, spec.arrivalLeads, spec.travel);
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
        intentKey: spec.intentKey
      };
    }

    // ---- composing one ordered pair ----

    function compose(key, pair, fromW, toW, floors) {
      var pivot = pivotOf(pair), kind = pivot.elementKind, i;
      if (pivot.measure === "banding") {
        var fracs = [];
        [fromW, toW].forEach(function (w) {
          if (w.frameSide) fracs.push(w.structure.banding.periodPx / w.frameSide);
        });
        if (fracs.length) pivot.bandPeriodFrac = r4(Math.min.apply(null, fracs));
      }
      var pivotInstr = INSTRUMENT_OF_KIND[kind];
      if (pivotInstr === null || pivotInstr === undefined) {
        return [null, "pivot needs " + (MISSING_INSTRUMENT[kind]
                                        || ("an instrument that cuts on " + pyText(kind)))];
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
      var axis = travellingAxis(fromW, toW, pivot, floors);
      var travelInstr = null, travelDecline = null, tkind;
      if (axis === null) {
        travelDecline = "no measure carries a usable reading on both works";
      } else {
        tkind = KIND_OF_AXIS[axis.axis];
        travelInstr = INSTRUMENT_OF_KIND[tkind];
        if (travelInstr === null || travelInstr === undefined) {
          travelInstr = null;
          travelDecline = "the travelling axis needs "
            + (MISSING_INSTRUMENT[tkind] || ("an instrument that cuts on " + pyText(tkind)));
        } else if (travelInstr === pivotInstr) {
          travelInstr = null;
          travelDecline = "the travelling axis cuts on the same instrument as the pivot";
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

      var world = travelInstr ? worldOf(toW, floors, axis) : null;
      var distance = axis ? num(axis.delta) : 0.0;
      var voiced = voiceTheCues(travelInstr !== null, arrivalInstr !== null, world, distance);
      var voices = voiced[0], tier = voiced[1];
      if (travelInstr === null) delete voices.travel;
      if (arrivalInstr === null) delete voices.arrival;

      var instrumentOf = {};
      if (pivotInstr && voices.pivot) instrumentOf.pivot = pivotInstr;
      if (travelInstr && voices.travel) instrumentOf.travel = travelInstr;
      if (arrivalInstr && voices.arrival) instrumentOf.arrival = arrivalInstr;
      var stackOrder = CUE_IDS.filter(function (c) { return instrumentOf[c] !== undefined; });
      var placed = placeTheStack(stackOrder, instrumentOf);
      if (placed[0] === null) return [null, placed[1]];
      var stacks = placed[0];
      var reordered = stackOrder.filter(function (c, i2) { return stacks[c] !== i2; });

      var judged = tierFor(voices, tier), row = judged[0], counts = judged[1];
      if (row === null) {
        return [null, "the declared tier " + tier + " and the realised voices disagree: "
                + counts.letters + " letters, " + counts.accompaniments + " accompaniments, "
                + counts.miracles + " miracles"];
      }
      var windows = cueWindows(travelInstr !== null, arrivalLeads, travelInstr);
      var ends = CUE_IDS.filter(function (c) { return voices[c] !== undefined; })
        .map(function (c) { return windows[c][1]; });
      var derivedMs = roundToInt(Math.max.apply(null, ends) * row.duration);
      if (!(derivedMs > 0 && derivedMs <= TRANSACTION_MS)) {
        return [null, "the derived duration " + derivedMs + " ms stands outside §2.5's "
                + "transaction bound of " + TRANSACTION_MS + " ms"];
      }

      var roles = { pivot: voices.pivot === "accompaniment" ? ["surface", "breath"]
                    : ["surface", "mystery"] };
      if (travelInstr) roles.travel = world ? ["mystery", "world"] : ["mystery", "fragment"];
      if (arrivalInstr) roles.arrival = arrivalLeads ? ["disassembly", "assembly"] : ["assembly"];

      var register = registerOf(fromW, toW, arrival, world);
      var intentKey = row.tier === "culmination" ? "culmination"
        : (world ? "middle-world" : (travelInstr ? "middle-travel" : "quiet"));
      var spec = {
        pivot: pivotInstr, travel: travelInstr, arrival: arrivalInstr,
        voices: voices, roles: roles, tier: row.tier, duration: row.duration,
        arrivalLeads: arrivalLeads,
        middle: world ? { kind: "world", world: world }
          : (travelInstr ? { kind: "surface" } : { kind: "none" }),
        budget: counts, intentKey: intentKey
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
        a: pair.pair.a, b: pair.pair.b
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

    function workParts(work, floors) {
      var sets = {}, counts = {}, fig = {}, ends = {}, i, s, reading;
      for (i = 0; i < work.sets.length; i++) {
        s = work.sets[i];
        if (!s.realCount) continue;
        sets[s.kind] = s.index;
        counts[s.kind] = s.count;
        if (s.fig !== null && s.fig !== undefined) fig[s.kind] = s.fig;
      }
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
        sets: sets, counts: counts, fig: fig, ends: ends,
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
        } else if (instr === "gears" && num(row[11]) >= 0) {
          wanted.ratio = row[13];
          wanted.centreX = flt(r4((num(row[6]) + num(row[8])) / 2.0 + 0.5));
          wanted.centreY = flt(r4((num(row[7]) + num(row[9])) / 2.0 + 0.5));
          wanted.size = [row[11], row[12]];
          if (num(row[14]) >= 0) wanted.bandPeriod = row[14];
        }
        var measured = {}, nodes = {};
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
          nodes[nodeName] = { op: "static", value: pairv[1],
                              note: noteFor(h, req, pairv[1], why) };
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
        intent: realiseIntent(tpl, row, axis, arrival, fromP, toP, cutKinds, pivotKind,
                              pivotMeasure, world),
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
      return fill(tpl.intent, fields);
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

    function scoreFor(a, b, direction, seed) {
      // Two works, a direction and a die: the whole crossing, decided here and now.
      var tag = direction === "b-to-a" ? "ba" : "ab";
      var key = a.id + "__" + b.id + "__" + tag;
      var pair = pairOf(a, b, tag === "ab" ? "a-to-b" : "b-to-a", seed);
      var fromW = tag === "ab" ? a : b, toW = tag === "ab" ? b : a;
      var made = compose(key, pair, fromW, toW, FLOORS);
      if (made[0] === null) return { key: key, declined: made[1] };
      var plan = made[0];
      var tpl = buildTemplate(plan.shape, plan.spec);
      var row = rowOf(plan);
      var pv = plan.pivot;
      var ctx = {
        pivot: [pv.kind, pv.measure, pv.cut, pv.transform, pv.elementKind, pivotKindsOf(pv)],
        fromParts: workParts(fromW, FLOORS),
        toParts: workParts(toW, FLOORS)
      };
      var filled = fillPlan(key, row, tpl, ctx);
      var out = serialise(filled);
      if (out[0] === null) return { key: key, declined: out[1] };
      var text = writeJson(out[0], 0);
      var tight = writeJsonTight(out[0]);
      return { key: key, score: out[0], json: text, bytes: tight.length,
               overTheFence: SCORE_FENCE_BYTES ? tight.length > SCORE_FENCE_BYTES : false,
               shape: plan.shape, plan: filled, version: COMPOSER_VERSION };
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
    //   seed          the die, a number in 0…8 that fixes every random choice. Missing means the
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
    var SESSION_MEMORY_FIELDS = ["family", "seed", "passIndex"];

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
      if (seed !== seed || seed < 0 || seed > 8) {
        return no("the passage request's seed " + String(req.seed) + " stands outside 0…8");
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
      var made = scoreFor(a, b, direction, seed);
      made.request = read;
      made.applied = null;
      if (made.declined !== undefined) made.score = null;
      else made.declined = null;
      return made;
    }

    return { passageFor: passageFor, scoreFor: scoreFor, routeRoles: ROUTE_ROLES.slice(),
             version: COMPOSER_VERSION, writeJson: writeJson,
             writeJsonTight: writeJsonTight, r4: r4 };
  }

  join({ version: COMPOSER_VERSION, make: make });
})();
