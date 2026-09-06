#!/usr/bin/env python3
"""SYNTHETIC WORK RECORDS — the corpus the composer's own laws are proven on.

WHY THIS FILE EXISTS.

  `tests/test_pass_composed.py` and `tests/test_pass_reads.py` used to prove the composer's laws by
  sweeping the photographs that hang today: 192 ordered pairs drawn from the 121 real per-work
  records in `tests/fixture_pass_works.json`, plus several double loops over all 121. A sweep of
  today's collection is not a proof of a general law. It proves nothing about a photograph that is
  not in it, its green moves when a photograph is added or removed, and it costs more every time the
  collection grows — which was the single biggest cost in the gate.

  His word of 2026-09-06 states the replacement: the laws of the composer and of the instruments'
  declared readings are checked on DETERMINISTIC SYNTHETIC WorkRecords built from the BOUNDARY VALUES
  of the measurements and from the BEHAVIOUR CLASSES the composer actually branches on; a small smoke
  on real records stays behind for schema and wiring; and adding a photograph to the collection must
  not multiply the cost of any of it.

WHAT A BOUNDARY IS HERE, AND WHERE EVERY NUMBER COMES FROM.

  Never from a figure invented in this file. A record's fields fall into a few kinds and each kind
  has its own boundary, read off the measurement's own definition or off a branch in
  `engine/assets/pass-composer.js`:

  · A READING between nothing and whole. `measures.*`, every `score`, every `reading`, `coherence`,
    `confidence`, `voidShare`, `colour.*`, `luminance.level`. The composer holds every one of them
    through `clamp01` (pass-composer.js:1621), so its own span is [0, 1] and its boundaries are 0, 1
    and the middle. Nothing else about a reading is a boundary.

  · AN ANGLE IN DEGREES. `guides.edge.angleDeg`, `structure.grid.angleDeg`, `door.angleDeg`. The
    composer folds edge angles modulo 180 (pass-composer.js:4649), so 0 and 180 are one point and
    90 is the far one: the boundaries are 0 and 90.

  · A LENGTH IN PIXELS. `periodPx`, `stepPx`, `detailPx`, `spectralPeriodPx`. Their meaningful
    boundaries are "no measured period at all" — zero, which the composer tests for by name
    (`Number(bFrom.periodPx) > 0`, pass-composer.js:4799) — one pixel, and the whole frame side.

  · A COUNT. `sets[].realCount`, `structure.regions.count`, `structure.rotational.n`, `door.pieces`.
    Their boundaries are the ones the composer's own branches name: `realCount >= 2` for a box's
    faces (`facesOf`, pass-composer.js:4896-4903), `n >= 3` and equal on both works for a shared turn
    (pass-composer.js:1766-1768), and one element versus many.

  · A VOTE. `matter.materialVotes` and `matter.substanceVotes.*` are held at `v / 3`
    (`voteConfidence`, pass-composer.js:4620-4623), so their span is 1 to 3 and the record's own
    scale is the boundary.

  · AN ENUM. `door.device`, `door.elementKind`, `structure.radial.subType`, `structure.banding.axis`,
    `motifs.gateAxis`, `sets[].kind`, `sets[].provider`, `palette.rung`, `matter.material`. There is
    no interior for an enum: every value it can hold is a boundary, and the classes below carry them.

  The one number that is neither is `frameSide`. It is a frame size in pixels and it is a divisor,
  never a threshold — nothing in the composer compares it to anything — so one value is taken for
  the whole corpus and every pixel length below is written as a share of it.

WHAT A BEHAVIOUR CLASS IS.

  A predicate in the composer's own source that a record can be on either side of, and that changes
  what comes out. They are not guessed: each class below names the line of `pass-composer.js` whose
  branch it stands on, in its own sentence. The genre choice alone supplies most of them — a work
  that arrives on rings against one that arrives on spokes (:4753), two band families running the
  same way against two that cross (:4801), a work with panels to fold against one with none (:4832),
  two works agreeing on what they are made of against two that share nothing (:4721).

WHAT THE SIZE OF THIS CORPUS IS A FUNCTION OF.

  The dimensions and the classes above, and nothing else. It does not grow when a photograph is
  added to the collection, because it never reads the collection.

  The ordered pair cases are chosen the same way, in two parts. The CONTRASTS are hand-named, one per
  class contrast a law has to hold across — two band families that cross, a work arriving on rings
  against one arriving on spokes, tone at one end of its span against tone at the other. The CONTROL
  COLUMN puts every class against `neutral`, in both directions, which isolates that class: a
  contrast moves two things at once by design, and a class against the control moves exactly what its
  own sentence says it moves. Together they are one pair per contrast plus two per class — never a
  cross product, and never a table of product pairs, because nothing in either names a photograph.
"""

# ---------------------------------------------------------------- the spans a field can stand in
# The frame every synthetic record is measured in. A divisor and never a threshold: no branch of the
# composer compares a frame side to anything, so the corpus takes one and writes every pixel length
# below as a share of it.
FRAME = 1440.0

# A reading's own span, held by `clamp01` at pass-composer.js:1621.
LOW, MID, HIGH = 0.0, 0.5, 1.0

# An angle's own span, folded modulo 180 at pass-composer.js:4649 so that 0 and 180 are one point.
ANG_ALIGNED, ANG_CROSSED = 0.0, 90.0

# A vote's own span, held at v / 3 by `voteConfidence`, pass-composer.js:4620-4623.
VOTE_LOW, VOTE_HIGH = 1, 3

# The nine element-set kinds a record can carry, read off `KIND_OF_MEASURE` and `setFor`'s callers
# (pass-composer.js:270-273, :3473). Every measure the composer can hold a ground on cuts on one of
# them, so a corpus that omits a kind hides every instrument cast on it.
SET_KINDS = ["band", "field", "panel", "region", "ring", "scale", "strip", "tile", "wedge"]

# The four providers a set names. The composer never branches on a provider, so this is carried for
# schema shape alone and one value stands for the corpus.
SET_PROVIDER = "structural"


def _sets(counts):
    """The `sets` block, one entry per kind, each with the real count the caller asks for.

    `count` and `realCount` are kept equal because nothing in the composer reads them apart except
    `anySetOf`'s tie-break (pass-composer.js:3485-3494), and `measuredGrain`/`mergeFactor` stand at
    the neutral 1 element per piece so a class that means to move a grain has to say so.
    """
    out = []
    for i, kind in enumerate(SET_KINDS):
        n = counts.get(kind, 0)
        out.append({"count": n, "fig": None, "index": i, "kind": kind,
                    "measuredGrain": float(n), "mergeFactor": 1.0,
                    "provider": SET_PROVIDER, "realCount": n})
    return out


def _base(wid):
    """One synthetic WorkRecord carrying every field the real records carry, each at the middle of
    its own span. Nothing here is a boundary and nothing here is a class: this is the record a class
    below departs from, so that a class's own overrides are the only thing that can explain a
    difference in what the composer answers.

    THE SHAPE IS THE REAL RECORD'S SHAPE, field for field. `tests/test_pass_composed.py` and
    `tests/test_pass_reads.py` each keep a smoke on the real fixture that proves it still is.
    """
    return {
        "id": wid,
        "frameSide": FRAME,
        # A reading of the whole frame's light and colour. Held through `clamp01`, so the middle.
        "colour": {"brightness": MID, "contrast": MID, "sat": MID},
        "luminance": {"level": MID},
        "palette": {"colourfulness": MID, "hueConcentration": MID, "hues": ["blue"],
                    "rung": "полный цвет"},
        # The door the site's own staging step wrote for this work. `level` holds one value in every
        # real record, so the corpus holds that one.
        "door": {"angleDeg": ANG_ALIGNED, "device": "tiles", "elementKind": "tile",
                 "level": "CELL", "pieces": 144.0, "stepPx": FRAME / 12.0},
        # The compact edge guide `guideAgreement` reads (pass-composer.js:4645-4651).
        "guides": {"edge": {"angleDeg": ANG_ALIGNED, "coherence": MID, "cross": MID,
                            "density": MID, "straightness": MID}},
        # What the work is made of and depicts. The base shares NO label with any other base record,
        # so `matterAgreement` reads nothing unless a class says it should — see MATTER_SHARED below.
        "matter": {"material": None, "materialSecond": None, "materialVotes": VOTE_LOW,
                   "substance": [], "substanceVotes": {}},
        # The seven shared measures `groundReadings` ranks a ground on (pass-composer.js:255-256).
        "measures": {"banding": MID, "dominant_object": MID, "grid": MID, "named_objects": MID,
                     "radial": MID, "regions": MID, "texture": MID},
        # The motifs a slot, a pole and a seam are placed on.
        "motifs": {"gateAxis": "horizontal", "gateGap": MID, "gateHalf": 0.25, "gatePlace": MID,
                   "gateScore": MID, "measured": [], "radialCentre": [MID, MID],
                   "voidShare": MID},
        "readiness": [MID, FRAME / 4.0, "horizontal"],
        # Every kind carries elements, so no instrument is hidden behind a missing cut. Two panels is
        # the boundary `facesOf` names for a solid (pass-composer.js:4900).
        "sets": _sets({"band": 2, "field": 1, "panel": 2, "region": 2, "ring": 2, "scale": 2,
                       "strip": 2, "tile": 4, "wedge": 4}),
        "structure": {
            "banding": {"axis": "horizontal", "periodPx": FRAME / 4.0, "score": MID},
            # No `score` beside the box, exactly as the real records carry none.
            "dominantObject": {"bbox": [0.25, 0.25, 0.75, 0.75]},
            "grid": {"angleDeg": ANG_ALIGNED, "periodPx": FRAME / 12.0, "phase": MID,
                     "score": MID},
            "horizon": {"seam": MID, "y": MID},
            "ownDevice": {"angleDeg": ANG_ALIGNED, "confidence": MID, "count": 12.0,
                          "kind": "tiles", "pieces": 144.0, "stepPx": FRAME / 12.0},
            "polar": {"planet": MID, "radial_streak": MID, "tunnel": MID, "twirl": MID},
            "radial": {"centre": [MID, MID], "score": MID, "subType": "angular"},
            "regions": {"boxes": [{"areaFrac": 0.25, "bbox": [0.0, 0.0, MID, 1.0]},
                                  {"areaFrac": 0.25, "bbox": [MID, 0.0, 1.0, 1.0]}],
                        "count": 2,
                        "line": {"x": {"at": MID, "explains": MID},
                                 "y": {"at": MID, "explains": MID}},
                        "score": MID},
            # Three is the order a shared turn needs on both works (pass-composer.js:1766).
            "rotational": {"n": 3, "score": MID},
        },
        "symmetry": {
            "centre": [MID, MID],
            "glide": None,
            "pointGroupOrder": 2,
            # `strongestReflection` reads `reading` and never `diffScore` (pass-composer.js:4595).
            "reflection": {
                "leftOntoRight": {"axisX": MID, "diffScore": MID, "inRecipe": False,
                                  "reading": MID},
                "topOntoBottom": {"axisY": MID, "diffScore": MID, "inRecipe": False,
                                  "reading": MID},
                "mainDiagonal": {"diffScore": MID, "inRecipe": False, "reading": MID},
                "antiDiagonal": {"diffScore": MID, "inRecipe": False, "reading": MID},
            },
            "rotation": {"halfTurnDiffScore": MID, "halfTurnReading": MID, "order": 3,
                         "reading": MID, "wedgesMirrored": False},
            "translation": {
                "banding": {"axis": "horizontal", "periodPx": FRAME / 4.0, "reading": MID},
                "grid": {"angleDeg": ANG_ALIGNED, "periodPx": FRAME / 12.0, "reading": MID},
                "sliceRepeat": {"axis": None, "periodPx": 0, "reading": MID},
            },
        },
        "texture": {"detailPx": 8.0, "reliefCentreDetailX": MID, "reliefCentreMassX": MID,
                    "reliefEdge": MID, "scoreFromCutLines": MID, "spectralPeriodPx": FRAME / 16.0},
    }


def _put(record, path, value):
    """Sets one dotted path on a record, refusing a path the base does not already carry — so a
    class can never quietly invent a field the real records have no room for."""
    segs = path.split(".")
    cur = record
    for seg in segs[:-1]:
        cur = cur[seg]
    if segs[-1] not in cur:
        raise KeyError("synthetic class writes a field the base record does not carry: %s" % path)
    cur[segs[-1]] = value


# ---------------------------------------------------------------- the classes
# Each entry is (name, the sentence saying which boundary or branch this record stands for, the
# fields it moves off the base). The name is the record's own id inside the corpus, so a red row
# prints the class it broke on.
#
# THE LIST IS A FUNCTION OF THE COMPOSER'S OWN BRANCHES AND OF THE MEASUREMENT SPANS, and of nothing
# else. Adding a photograph to the collection adds no entry here; adding a branch to the composer
# does.
CLASSES = [
    ("neutral",
     "every measurement at the middle of its own span and every enum at its first value — the "
     "record every other class departs from, so a difference in what the composer answers can only "
     "be explained by the fields that class moved",
     {}),

    ("floor",
     "every reading at the bottom of the span `clamp01` holds it in (pass-composer.js:1621), and "
     "every measured period at zero — the record that gives every genre and every instrument the "
     "least a record can give",
     {"colour.brightness": LOW, "colour.contrast": LOW, "colour.sat": LOW,
      "luminance.level": LOW, "palette.colourfulness": LOW, "palette.hueConcentration": LOW,
      "measures.banding": LOW, "measures.dominant_object": LOW, "measures.grid": LOW,
      "measures.named_objects": LOW, "measures.radial": LOW, "measures.regions": LOW,
      "measures.texture": LOW,
      "motifs.gateGap": LOW, "motifs.gateHalf": LOW, "motifs.gatePlace": LOW,
      "motifs.gateScore": LOW, "motifs.voidShare": LOW,
      "structure.banding.score": LOW, "structure.banding.periodPx": 0.0,
      "structure.grid.score": LOW, "structure.grid.phase": LOW,
      "structure.horizon.seam": LOW, "structure.ownDevice.confidence": LOW,
      "structure.polar.planet": LOW, "structure.polar.radial_streak": LOW,
      "structure.polar.tunnel": LOW, "structure.polar.twirl": LOW,
      "structure.radial.score": LOW, "structure.regions.score": LOW,
      "structure.regions.line.x.explains": LOW, "structure.regions.line.y.explains": LOW,
      "structure.rotational.score": LOW,
      "guides.edge.coherence": LOW, "guides.edge.cross": LOW, "guides.edge.density": LOW,
      "guides.edge.straightness": LOW,
      "texture.reliefEdge": LOW, "texture.scoreFromCutLines": LOW,
      "symmetry.rotation.reading": LOW, "symmetry.rotation.halfTurnReading": LOW,
      "symmetry.translation.sliceRepeat.reading": LOW}),

    ("ceiling",
     "every reading at the top of the same span — the record that gives every genre and every "
     "instrument the most a record can give",
     {"colour.brightness": HIGH, "colour.contrast": HIGH, "colour.sat": HIGH,
      "luminance.level": HIGH, "palette.colourfulness": HIGH, "palette.hueConcentration": HIGH,
      "measures.banding": HIGH, "measures.dominant_object": HIGH, "measures.grid": HIGH,
      "measures.named_objects": HIGH, "measures.radial": HIGH, "measures.regions": HIGH,
      "measures.texture": HIGH,
      "motifs.gateGap": HIGH, "motifs.gateScore": HIGH, "motifs.voidShare": HIGH,
      "structure.banding.score": HIGH, "structure.grid.score": HIGH,
      "structure.horizon.seam": HIGH, "structure.ownDevice.confidence": HIGH,
      "structure.polar.planet": HIGH, "structure.polar.radial_streak": HIGH,
      "structure.polar.tunnel": HIGH, "structure.polar.twirl": HIGH,
      "structure.radial.score": HIGH, "structure.regions.score": HIGH,
      "structure.regions.line.x.explains": HIGH, "structure.regions.line.y.explains": HIGH,
      "structure.rotational.score": HIGH,
      "guides.edge.coherence": HIGH, "guides.edge.cross": HIGH, "guides.edge.density": HIGH,
      "guides.edge.straightness": HIGH,
      "texture.reliefEdge": HIGH, "texture.scoreFromCutLines": HIGH,
      "symmetry.reflection.leftOntoRight.reading": HIGH,
      "symmetry.reflection.topOntoBottom.reading": HIGH,
      "symmetry.reflection.mainDiagonal.reading": HIGH,
      "symmetry.reflection.antiDiagonal.reading": HIGH,
      "symmetry.rotation.reading": HIGH, "symmetry.rotation.halfTurnReading": HIGH,
      "symmetry.translation.sliceRepeat.reading": HIGH}),

    ("rings-arrival",
     "the arriving side of `arrivesOnRings` (pass-composer.js:4753): a work whose radial reading is "
     "on rings, which is the only way a kaleidoscope is reached and the only way a spin is refused",
     {"structure.radial.subType": "ring", "structure.radial.score": HIGH,
      "measures.radial": HIGH, "door.device": "rings", "door.elementKind": "ring",
      "structure.ownDevice.kind": "rings", "motifs.radialCentre": [MID, MID]}),

    ("spokes-arrival",
     "the other side of the same branch: a work whose radial reading is on spokes, which turns "
     "rather than opens, so the pair reaches spin and never a kaleidoscope",
     {"structure.radial.subType": "angular", "structure.radial.score": HIGH,
      "measures.radial": HIGH, "structure.rotational.n": 6, "symmetry.rotation.order": 6}),

    ("bands-across",
     "one side of `sameWay` (pass-composer.js:4801): a work whose band family runs horizontally, "
     "with a measured period so `periods` holds (pass-composer.js:4799)",
     {"structure.banding.axis": "horizontal", "structure.banding.periodPx": FRAME / 8.0,
      "structure.banding.score": HIGH, "measures.banding": HIGH,
      "symmetry.translation.banding.axis": "horizontal",
      "door.device": "stripes", "door.elementKind": "strip",
      "structure.ownDevice.kind": "stripes", "readiness": [HIGH, FRAME / 8.0, "horizontal"]}),

    ("bands-upright",
     "the other side of `sameWay`: a work whose band family runs vertically, so paired with "
     "`bands-across` the two families cross and the fabric becomes stripes rather than a slide",
     {"structure.banding.axis": "vertical", "structure.banding.periodPx": FRAME / 8.0,
      "structure.banding.score": HIGH, "measures.banding": HIGH,
      "symmetry.translation.banding.axis": "vertical",
      "door.device": "stripes", "door.elementKind": "strip",
      "structure.ownDevice.kind": "stripes", "readiness": [HIGH, FRAME / 8.0, "vertical"]}),

    ("bands-upright-offset",
     "a SECOND work banding vertically, with its measured centres and dividing lines at the far end "
     "of the frame. One record on a side of an enum branch is one reading, and a handle driven only "
     "under that branch then has nothing to be told apart by: `livemirror`'s `centreY` is filled "
     "only where the departing work bands vertically (pass-composer.js:8531, :8571), so a single "
     "vertical record left that handle standing still on every seat the corpus could offer",
     {"structure.banding.axis": "vertical", "structure.banding.periodPx": FRAME / 8.0,
      "structure.banding.score": HIGH, "measures.banding": HIGH,
      "symmetry.translation.banding.axis": "vertical",
      "readiness": [HIGH, FRAME / 8.0, "vertical"],
      "structure.regions.line.x.at": 0.95, "structure.regions.line.y.at": 0.95,
      "structure.regions.line.x.explains": HIGH, "structure.regions.line.y.explains": HIGH,
      "motifs.radialCentre": [0.95, 0.95], "structure.radial.centre": [0.95, 0.95],
      "symmetry.centre": [0.95, 0.95]}),

    ("bands-without-period",
     "the boundary `periods` tests by name (pass-composer.js:4799): a band family carrying no "
     "measured period at all, which is a score with nothing to slide",
     {"structure.banding.periodPx": 0.0, "structure.banding.score": HIGH,
      "measures.banding": HIGH, "symmetry.translation.banding.periodPx": 0.0}),

    ("one-panel",
     "the boundary `facesOf` names (pass-composer.js:4896-4903): a work cutting into fewer than the "
     "two panels a solid needs, so the box-fold genre reads nothing off it",
     {"sets": _sets({"band": 2, "field": 1, "panel": 1, "region": 2, "ring": 2, "scale": 2,
                     "strip": 2, "tile": 4, "wedge": 4}),
      "structure.regions.count": 1, "measures.regions": HIGH,
      "structure.regions.score": HIGH}),

    ("many-panels",
     "the other side of the same boundary: a work cutting into many real panels with its region "
     "reading at the top of its span, which is everything a box-fold asks for",
     {"sets": _sets({"band": 4, "field": 1, "panel": 8, "region": 4, "ring": 4, "scale": 4,
                     "strip": 4, "tile": 16, "wedge": 6}),
      "structure.regions.count": 8, "measures.regions": HIGH,
      "structure.regions.score": HIGH,
      "structure.regions.line.x.explains": HIGH, "structure.regions.line.y.explains": HIGH}),

    ("no-elements",
     "the degenerate cut §4.3 allows: a work carrying no real element on any kind, so every actor "
     "the composer draws is the whole frame",
     {"sets": _sets({}), "structure.regions.count": 0}),

    ("matter-known",
     "one side of `matterAgreement` (pass-composer.js:4624-4642): a work naming what it is made of "
     "and depicts, at the top of the record's own three-vote scale",
     {"matter.material": "решётка", "matter.materialSecond": "створки",
      "matter.materialVotes": VOTE_HIGH, "matter.substance": ["бетон", "металл"],
      "matter.substanceVotes": {"бетон": VOTE_HIGH, "металл": VOTE_HIGH}}),

    ("matter-known-faintly",
     "the same labels at the bottom of the same vote scale, so a pair of these two agrees on what "
     "it is made of while the confidence that carries the agreement is the least it can be",
     {"matter.material": "решётка", "matter.materialSecond": "створки",
      "matter.materialVotes": VOTE_LOW, "matter.substance": ["бетон", "металл"],
      "matter.substanceVotes": {"бетон": VOTE_LOW, "металл": VOTE_LOW}}),

    ("matter-other",
     "the far side of the same reading: a work naming a material and substances no other class here "
     "names, so `matterAgreement` reads nothing for any pair it stands in",
     {"matter.material": "нить", "matter.materialSecond": "плёнка",
      "matter.materialVotes": VOTE_HIGH, "matter.substance": ["вода"],
      "matter.substanceVotes": {"вода": VOTE_HIGH}}),

    ("sphere",
     "the polar world `POLAR_WORLD` maps to a sphere (pass-composer.js:250): the planet reading at "
     "the top of its span and its two siblings at the bottom, so the world a fold opens is decided",
     {"structure.polar.planet": HIGH, "structure.polar.tunnel": LOW,
      "structure.polar.twirl": LOW, "structure.polar.radial_streak": LOW}),

    ("corridor",
     "the same map's corridor: the tunnel reading at the top of its span and its siblings at the "
     "bottom",
     {"structure.polar.tunnel": HIGH, "structure.polar.planet": LOW,
      "structure.polar.twirl": LOW, "structure.polar.radial_streak": HIGH,
      "structure.radial.subType": "ring", "door.device": "rings", "door.elementKind": "ring",
      "structure.ownDevice.kind": "rings"}),

    ("log-spiral",
     "the same map's log spiral: the twirl reading at the top of its span and its siblings at the "
     "bottom",
     {"structure.polar.twirl": HIGH, "structure.polar.planet": LOW,
      "structure.polar.tunnel": LOW, "structure.polar.radial_streak": LOW,
      "structure.radial.subType": "ring", "door.device": "rings", "door.elementKind": "ring",
      "structure.ownDevice.kind": "rings"}),

    ("dark",
     "the bottom of `luminance.level`, the tone half of `tonalSpectral` (pass-composer.js:3166)",
     {"luminance.level": LOW, "colour.brightness": LOW, "palette.rung": "чёрно-белое",
      "colour.sat": LOW, "palette.colourfulness": LOW, "palette.hues": []}),

    ("bright",
     "the top of the same reading, so a pair of dark against bright stands the whole span of the "
     "tonal bridge apart",
     {"luminance.level": HIGH, "colour.brightness": HIGH, "palette.rung": "полный цвет",
      "colour.sat": HIGH, "palette.colourfulness": HIGH,
      "palette.hues": ["red", "orange", "yellow"]}),

    ("fine-grain",
     "the bottom of `texture.detailPx`, the spectral half of `tonalSpectral` "
     "(pass-composer.js:3169): one pixel of detail, the finest a grain can be measured at",
     {"texture.detailPx": 1.0, "texture.spectralPeriodPx": 2.0,
      "texture.scoreFromCutLines": HIGH, "measures.texture": HIGH}),

    ("coarse-grain",
     "the top of the same reading: a detail scale of a sixteenth of the frame, which is four "
     "octaves off `fine-grain` and so the whole span `tonalSpectral` divides by",
     {"texture.detailPx": 16.0, "texture.spectralPeriodPx": FRAME / 4.0,
      "texture.scoreFromCutLines": HIGH, "measures.texture": HIGH}),

    ("mirrored",
     "the top of `strongestReflection` (pass-composer.js:4595-4602) and of `rotationReading` "
     "beside it: a work whose wallpaper-group readings are as strong as they can be",
     {"symmetry.reflection.leftOntoRight.reading": HIGH,
      "symmetry.reflection.topOntoBottom.reading": HIGH,
      "symmetry.reflection.mainDiagonal.reading": HIGH,
      "symmetry.reflection.antiDiagonal.reading": HIGH,
      "symmetry.reflection.leftOntoRight.inRecipe": True,
      "symmetry.reflection.topOntoBottom.inRecipe": True,
      "symmetry.rotation.reading": HIGH, "symmetry.rotation.halfTurnReading": HIGH,
      "symmetry.rotation.wedgesMirrored": True, "symmetry.pointGroupOrder": 4,
      "structure.rotational.score": HIGH}),

    ("unmirrored",
     "the bottom of the same two readings, including the negative reading `readingOf` floors at "
     "nothing (pass-composer.js:4604-4611)",
     {"symmetry.reflection.leftOntoRight.reading": -1.0,
      "symmetry.reflection.topOntoBottom.reading": -1.0,
      "symmetry.reflection.mainDiagonal.reading": -1.0,
      "symmetry.reflection.antiDiagonal.reading": -1.0,
      "symmetry.rotation.reading": -1.0, "symmetry.rotation.halfTurnReading": -1.0,
      "symmetry.pointGroupOrder": 1, "structure.rotational.score": -1.0,
      "structure.rotational.n": 2, "symmetry.rotation.order": 2}),

    ("gridded",
     "the top of the grid reading with a measured period and an aligned angle — the tile cut a "
     "grid ground is drawn on",
     {"measures.grid": HIGH, "structure.grid.score": HIGH,
      "structure.grid.periodPx": FRAME / 24.0, "structure.grid.angleDeg": ANG_ALIGNED,
      "symmetry.translation.grid.periodPx": FRAME / 24.0,
      "symmetry.translation.grid.angleDeg": ANG_ALIGNED,
      "door.device": "tiles", "door.elementKind": "tile", "door.pieces": 576.0,
      "structure.ownDevice.kind": "tiles", "structure.ownDevice.pieces": 576.0}),

    ("gridded-askew",
     "the same reading at the other end of the angle span (pass-composer.js:4649 folds an angle "
     "modulo 180, so 90 degrees is as far from aligned as an angle gets)",
     {"measures.grid": HIGH, "structure.grid.score": HIGH,
      "structure.grid.periodPx": FRAME / 24.0, "structure.grid.angleDeg": ANG_CROSSED,
      "symmetry.translation.grid.angleDeg": ANG_CROSSED,
      "guides.edge.angleDeg": ANG_CROSSED, "guides.edge.coherence": HIGH,
      "guides.edge.straightness": HIGH, "door.angleDeg": ANG_CROSSED,
      "structure.ownDevice.angleDeg": ANG_CROSSED}),

    ("edges-agreeing",
     "the top of `guideAgreement` (pass-composer.js:4645-4651): a coherent, straight edge field at "
     "the aligned end of the angle span, which is the only way that reading answers at all",
     {"guides.edge.coherence": HIGH, "guides.edge.straightness": HIGH,
      "guides.edge.angleDeg": ANG_ALIGNED, "guides.edge.density": HIGH,
      "guides.edge.cross": LOW}),

    ("named-objects",
     "the top of `measures.named_objects` with the region cut to carry it — the one shared measure "
     "whose cut is a named region rather than a piece of the frame (pass-composer.js:270-271)",
     {"measures.named_objects": HIGH, "measures.dominant_object": HIGH,
      "structure.dominantObject.bbox": [0.1, 0.1, 0.9, 0.9],
      "sets": _sets({"band": 2, "field": 1, "panel": 2, "region": 8, "ring": 2, "scale": 2,
                     "strip": 2, "tile": 4, "wedge": 4})}),

    ("gate-across",
     "one side of `motifs.gateAxis`, the slot a gate is placed on, with the gate reading at the top "
     "of its span so the motif is measured rather than absent",
     {"motifs.gateAxis": "horizontal", "motifs.gateScore": HIGH, "motifs.gatePlace": 0.25,
      "motifs.gateHalf": 0.02, "motifs.gateGap": HIGH, "motifs.measured": ["ворота"]}),

    ("gate-upright",
     "the other side of the same enum, with the slot at the far end of its own place span",
     {"motifs.gateAxis": "vertical", "motifs.gateScore": HIGH, "motifs.gatePlace": 0.75,
      "motifs.gateHalf": 0.27, "motifs.gateGap": LOW, "motifs.measured": ["ворота"]}),

    ("seam",
     "the top of `structure.horizon.seam` with the motif measured beside it — the locus a crossing "
     "crystallizes on where a work carries a horizon seam (`LOCUS_KINDS`, pass-composer.js:237)",
     {"structure.horizon.seam": HIGH, "structure.horizon.y": 0.3,
      "motifs.measured": ["горизонт-шов"], "motifs.voidShare": LOW}),

    ("void",
     "the top of `motifs.voidShare` with the object-in-emptiness motif measured beside it",
     {"motifs.voidShare": HIGH, "motifs.measured": ["объект в пустоте"],
      "measures.dominant_object": HIGH, "structure.dominantObject.bbox": [0.45, 0.45, 0.55, 0.55],
      "structure.horizon.seam": LOW}),

    ("slice-repeat",
     "the top of `symmetry.translation.sliceRepeat`, the one translation reading the base leaves "
     "without an axis at all",
     {"symmetry.translation.sliceRepeat.axis": "x",
      "symmetry.translation.sliceRepeat.periodPx": FRAME / 8.0,
      "symmetry.translation.sliceRepeat.reading": HIGH}),
    ("coarse-floor",
     "the bottom of the tile count a floor can be cut into — `pass-inst-parquet.js:384` publishes "
     "the span as 3 to 11 tiles across, and a work whose measured period is a third of its own "
     "frame side stands at the bottom of it while the base record stands at the top",
     {"structure.grid.periodPx": FRAME / 3.0, "structure.ownDevice.stepPx": FRAME / 3.0,
      "door.stepPx": FRAME / 3.0, "door.pieces": 9.0, "structure.ownDevice.pieces": 9.0,
      "structure.ownDevice.count": 3.0, "symmetry.translation.grid.periodPx": FRAME / 3.0,
      "measures.grid": HIGH, "structure.grid.score": HIGH}),

    ("no-horizon",
     "the absence the composer tests by name rather than by magnitude: `structure.horizon.y` at "
     "null, which halves `planet` (pass-composer.js:2091), steps `tilt` down "
     "(pass-composer.js:2358) and takes the seam locus away (pass-composer.js:3588)",
     {"structure.horizon.y": None, "structure.horizon.seam": LOW, "motifs.measured": []}),

    ("no-lattice",
     "neither of the two lattices a work can carry: `structure.grid.periodPx` and "
     "`structure.ownDevice.stepPx` both at zero, which is the boundary `wind`, `overlay`, "
     "`grid-colour` and the parquet floor all test by name (pass-composer.js:1914, :2062, :2296, "
     ":1947), and a door step of zero so no camera dolly is derived either "
     "(pass-composer.js:4134-4139)",
     {"structure.grid.periodPx": 0.0, "structure.ownDevice.stepPx": 0.0, "door.stepPx": 0.0,
      "symmetry.translation.grid.periodPx": 0.0, "structure.grid.score": LOW,
      "measures.grid": LOW, "structure.ownDevice.confidence": LOW}),

    ("no-relief",
     "the second absence the composer tests with `isFinite` rather than with a number: a work "
     "carrying no measured relief centre, so a crossing cannot crystallize on one "
     "(pass-composer.js:6814, :6937)",
     {"texture.reliefCentreDetailX": None, "texture.reliefCentreMassX": None,
      "texture.reliefEdge": LOW}),

    # THE FIVE BELOW ISOLATE ONE INSTRUMENT'S OWN DECLARED READING AT ITS BOUNDARY. A handle can only
    # be read where the instrument that publishes it is cast, and an instrument is only cast where its
    # own `suits` outranks its rivals on the same cut. So each of these records puts ONE instrument's
    # declared reading at the top of its span while holding the readings its rivals on the same cut
    # declare at their own bottom — which is a boundary construction, not a search for a pair that
    # happened to cast something. The rivals are read off `INSTRUMENT_SUITS`
    # (pass-composer.js:1799-2417), never guessed.
    ("bare-dark",
     "the bottom of `luminance.level` on a work carrying neither lattice nor horizon and no measured "
     "relief — so on a pair of this against `bare-bright`, `strata-light`'s own reading "
     "(pass-composer.js:2325) stands at the top of its span while `grid-colour` (:2293), `matter` "
     "(:2024), `strata-scale` (:2340) and `waterline` (:2376), the other four that cut on bands, "
     "each read their own zero",
     {"luminance.level": LOW, "colour.brightness": LOW, "colour.sat": LOW, "colour.contrast": LOW,
      "palette.colourfulness": LOW, "palette.hues": [], "palette.rung": "чёрно-белое",
      "structure.grid.periodPx": 0.0, "structure.ownDevice.stepPx": 0.0, "door.stepPx": 0.0,
      "symmetry.translation.grid.periodPx": 0.0, "structure.grid.score": LOW,
      "measures.grid": LOW, "structure.ownDevice.confidence": LOW,
      "structure.horizon.y": None, "structure.horizon.seam": LOW, "motifs.measured": [],
      "texture.reliefEdge": MID}),

    ("bare-bright",
     "the top of the same reading on the same kind of record, so the pair of the two stands the "
     "whole span of `luminance.level` apart with every rival on the band cut reading nothing",
     {"luminance.level": HIGH, "colour.brightness": HIGH, "colour.sat": LOW, "colour.contrast": LOW,
      "palette.colourfulness": LOW, "palette.hues": [], "palette.rung": "чёрно-белое",
      "structure.grid.periodPx": 0.0, "structure.ownDevice.stepPx": 0.0, "door.stepPx": 0.0,
      "symmetry.translation.grid.periodPx": 0.0, "structure.grid.score": LOW,
      "measures.grid": LOW, "structure.ownDevice.confidence": LOW,
      "structure.horizon.y": None, "structure.horizon.seam": LOW, "motifs.measured": [],
      "texture.reliefEdge": MID}),

    ("lattice-dim",
     "the bottom of `colour.sat` and of `colour.contrast` — the two readings `grid-colour`'s six "
     "colour-and-light voice handles declare (pass-composer.js:1008-1021) — on a work carrying the "
     "measured lattice that instrument's own fit needs (:2293)",
     {"colour.sat": LOW, "colour.contrast": LOW, "colour.brightness": LOW,
      "palette.colourfulness": LOW, "palette.rung": "чёрно-белое", "palette.hues": [],
      "structure.ownDevice.confidence": HIGH, "measures.grid": HIGH,
      "structure.grid.score": HIGH}),

    ("lattice-vivid",
     "the top of the same two readings on the same kind of record, so the two of them walk the whole "
     "span those six handles are driven across",
     {"colour.sat": HIGH, "colour.contrast": HIGH, "colour.brightness": HIGH,
      "palette.colourfulness": HIGH, "palette.rung": "полный цвет",
      "palette.hues": ["red", "green", "blue"],
      "structure.ownDevice.confidence": HIGH, "measures.grid": HIGH,
      "structure.grid.score": HIGH}),

    # WHERE A MEASURED CENTRE STANDS is its own dimension, and every reading in the family is a
    # fraction of the frame — a radial centre, a mirror centre, the dividing line a region cut falls
    # on, the centre of a work's own relief. The span of a fraction of the frame is the frame: the
    # two records below put the whole family at either end of it, which is what gives every handle
    # that reads a centre something to answer to.
    ("centre-near",
     "every measured centre and dividing line at the low end of the frame — the bottom of the span "
     "a fraction of the frame stands in",
     {"motifs.radialCentre": [0.05, 0.05], "structure.radial.centre": [0.05, 0.05],
      "symmetry.centre": [0.05, 0.05],
      "structure.regions.line.x.at": 0.05, "structure.regions.line.y.at": 0.05,
      "symmetry.reflection.leftOntoRight.axisX": 0.05,
      "symmetry.reflection.topOntoBottom.axisY": 0.05,
      "texture.reliefCentreMassX": 0.05, "texture.reliefCentreDetailX": 0.05,
      "structure.horizon.y": 0.05, "structure.dominantObject.bbox": [0.0, 0.0, 0.2, 0.2],
      "structure.ownDevice.count": 1.0, "measures.radial": HIGH,
      "structure.radial.score": HIGH}),

    ("centre-far",
     "the same family at the high end of the same span, so a pair of the two walks the whole frame "
     "and no handle that reads a centre is left with one value to look at",
     {"motifs.radialCentre": [0.95, 0.95], "structure.radial.centre": [0.95, 0.95],
      "symmetry.centre": [0.95, 0.95],
      "structure.regions.line.x.at": 0.95, "structure.regions.line.y.at": 0.95,
      "symmetry.reflection.leftOntoRight.axisX": 0.95,
      "symmetry.reflection.topOntoBottom.axisY": 0.95,
      "texture.reliefCentreMassX": 0.95, "texture.reliefCentreDetailX": 0.95,
      "structure.horizon.y": 0.95, "structure.dominantObject.bbox": [0.8, 0.8, 1.0, 1.0],
      "structure.ownDevice.count": 64.0, "measures.radial": HIGH,
      "structure.radial.score": HIGH}),

    ("rings-few",
     "a work cut as rings whose device carries the fewest elements a device can carry, so a pair of "
     "this against `rings-many` gives every handle that reads a ring count two counts rather than "
     "one count twice",
     {"structure.radial.subType": "ring", "structure.radial.score": HIGH,
      "measures.radial": HIGH, "door.device": "rings", "door.elementKind": "ring",
      "structure.ownDevice.kind": "rings", "structure.ownDevice.count": 2.0,
      "structure.ownDevice.pieces": 2.0, "door.pieces": 2.0,
      "sets": _sets({"band": 2, "field": 1, "panel": 2, "region": 2, "ring": 2, "scale": 2,
                     "strip": 2, "tile": 4, "wedge": 4})}),

    ("rings-many",
     "the same cut with the device at the many end of its own count",
     {"structure.radial.subType": "ring", "structure.radial.score": HIGH,
      "measures.radial": HIGH, "door.device": "rings", "door.elementKind": "ring",
      "structure.ownDevice.kind": "rings", "structure.ownDevice.count": 64.0,
      "structure.ownDevice.pieces": 4096.0, "door.pieces": 4096.0,
      "structure.ownDevice.stepPx": FRAME / 64.0, "door.stepPx": FRAME / 64.0,
      "sets": _sets({"band": 2, "field": 1, "panel": 2, "region": 2, "ring": 64, "scale": 2,
                     "strip": 2, "tile": 4, "wedge": 8})}),

    ("seam-fine",
     "a measured horizon seam — which is what `waterline`'s own four-valued fit asks for at both "
     "ends (pass-composer.js:2376-2382) — on a work at the fine end of the grain span, so a pair of "
     "this against `seam` gives that instrument's `tideCells` two counts to stand between rather "
     "than one count twice",
     {"structure.horizon.seam": HIGH, "structure.horizon.y": 0.7,
      "motifs.measured": ["горизонт-шов"], "motifs.voidShare": LOW,
      "texture.detailPx": 1.0, "texture.spectralPeriodPx": 2.0,
      "texture.scoreFromCutLines": HIGH, "measures.texture": HIGH}),
]


def corpus():
    """The whole synthetic corpus, as {id: WorkRecord}. Fixed, deterministic, and sized by the list
    of classes above — never by how many photographs the collection holds."""
    out = {}
    for name, _why, overrides in CLASSES:
        rec = _base(name)
        for path, value in overrides.items():
            _put(rec, path, value)
        out[name] = rec
    return out


def why(name):
    """The sentence this record stands for, so a red row can print it."""
    for cname, sentence, _ in CLASSES:
        if cname == name:
            return sentence
    raise KeyError(name)


# ---------------------------------------------------------------- the pair cases
# THE ORDERED PAIRS THE LAWS ARE CHECKED ON. Chosen the same way the records are: one pair per class
# contrast a law has to hold across, each with the sentence saying which contrast it is. This is NOT
# the cross product of the corpus and it is NOT a table of product pairs — nothing here names two
# photographs, and nothing here grows when a photograph is added to the collection.
#
# DIRECTION IS PART OF THE CASE. `passageFor` reads `direction` to decide which record departs and
# which arrives (pass-composer.js:4753 turns on the ARRIVING work alone), so a contrast whose two
# sides differ by which work arrives carries both directions as two cases.
CONTRASTS = [
    ("floor", "ceiling", "a-to-b",
     "every reading at the bottom of its span crossing to every reading at the top — the widest "
     "contrast the corpus can state, and the one every travelling axis reads its whole delta on"),
    ("ceiling", "floor", "b-to-a",
     "the same contrast walked the other way, so the direction the composer reads "
     "(pass-composer.js:10754) is a case of its own rather than an assumption"),
    ("neutral", "floor", "a-to-b",
     "the middle of every span against the bottom of it — half the width of the case above"),
    ("neutral", "ceiling", "a-to-b",
     "the middle of every span against the top of it — the other half"),

    ("spokes-arrival", "rings-arrival", "a-to-b",
     "the arriving work reads radial on rings, which is the one equality that opens a kaleidoscope "
     "and refuses a spin (pass-composer.js:4753)"),
    ("rings-arrival", "spokes-arrival", "a-to-b",
     "the same two works with the ring on the departing side, so the pair reaches spin instead"),

    ("neutral", "bands-across", "a-to-b",
     "two band families running the same way, so the parts slide along one symmetry "
     "(pass-composer.js:4801)"),
    ("bands-across", "bands-upright", "a-to-b",
     "two band families that cross, so the fabric becomes stripes instead"),
    ("bands-upright", "bands-across", "b-to-a",
     "the same crossing families the other way about"),
    ("bands-upright-offset", "bands-upright", "a-to-b",
     "two works banding the same way with their dividing lines at opposite ends of the frame, which "
     "is what a handle filled only under a vertical fold is told apart by"),
    ("bands-without-period", "bands-across", "a-to-b",
     "one family carrying no measured period at all, the boundary `periods` tests by name "
     "(pass-composer.js:4799)"),

    ("many-panels", "neutral", "a-to-b",
     "a departing work with panels to fold, which is everything the box-fold genre and every "
     "world-folding instrument ask for (pass-composer.js:4832)"),
    ("one-panel", "many-panels", "a-to-b",
     "a departing work under the two faces a solid needs, with the arriving work over it — so the "
     "genre reads nothing off the pair while the instrument register still can"),
    ("no-elements", "many-panels", "a-to-b",
     "a departing work carrying no real element on any cut, so every actor drawn is the whole "
     "frame (§4.3's degenerate element, pass-composer.js:3516)"),

    ("matter-known", "matter-known-faintly", "a-to-b",
     "two works agreeing on what they are made of, with the vote confidence at the bottom of the "
     "record's own three-vote scale (pass-composer.js:4620-4623)"),
    ("matter-known", "matter-other", "a-to-b",
     "two works sharing no material and no substance, so `matterAgreement` reads nothing"),

    ("dark", "bright", "a-to-b",
     "the whole span of the tonal bridge (pass-composer.js:3166), and with it the whole span of "
     "`strata-light`'s own reading and of `overlay`'s colour distance"),
    ("bright", "dark", "b-to-a",
     "the same span the other way, so a reading taken off the departing work is told apart from "
     "one taken off the arriving work"),
    ("ceiling", "dark", "a-to-b",
     "the top of every reading arriving at the bottom of the tonal span with the rest of the record "
     "still standing — which is the whole of `strata-light`'s own declared reading "
     "(pass-composer.js:2325) on a pair its rivals read little of"),
    ("fine-grain", "coarse-grain", "a-to-b",
     "four octaves of detail scale, which is the whole span `tonalSpectral` divides by "
     "(pass-composer.js:3169)"),

    ("sphere", "corridor", "a-to-b",
     "the two polar worlds `POLAR_WORLD` maps first (pass-composer.js:250), one departing and one "
     "arriving"),
    ("corridor", "log-spiral", "a-to-b",
     "the corridor against the log spiral, which is the share `planet` takes off its own reading "
     "(pass-composer.js:2086-2090)"),
    ("log-spiral", "sphere", "a-to-b",
     "the third of the three, so no world is left unwalked"),

    ("mirrored", "many-panels", "a-to-b",
     "a fold with the wallpaper-group reflection reading at the top of its span, which is the "
     "corroboration `corroboratedFit` adds on top of the structural fit (pass-composer.js:4844)"),
    ("unmirrored", "many-panels", "a-to-b",
     "the same fold with the reflection reading below zero, where `readingOf` floors it — so the "
     "corroboration adds nothing and the structural fit stands alone"),
    ("edges-agreeing", "many-panels", "a-to-b",
     "the same fold with the measured edge directions agreeing, the second corroboration "
     "(pass-composer.js:4854)"),

    ("gridded", "coarse-floor", "a-to-b",
     "the two ends of the tile count a floor can be cut into, `pass-inst-parquet.js:384`'s own "
     "published span"),
    ("gridded-askew", "gridded", "a-to-b",
     "the two ends of the lattice angle span, which is what `wind` reads as how far across the "
     "grain a front comes in (pass-composer.js:1909-1922)"),
    ("no-lattice", "gridded", "a-to-b",
     "one work carrying neither lattice, so `wind`'s second half, `overlay`'s beat and "
     "`grid-colour`'s whole fit each read their own zero"),

    ("named-objects", "void", "a-to-b",
     "the top of `measures.named_objects` against a work whose figure is a speck in emptiness — "
     "`adrift`'s own reading at both ends of its span"),
    ("gate-across", "gate-upright", "a-to-b",
     "the two values of `motifs.gateAxis`, with the slot at either end of its own place span"),
    ("seam", "no-horizon", "a-to-b",
     "a measured horizon seam arriving at a work carrying no horizon at all, which is the "
     "four-valued ladder `waterline` reads (pass-composer.js:2376-2382)"),
    ("no-horizon", "seam", "a-to-b",
     "the same ladder with the sides swapped"),
    ("no-relief", "neutral", "a-to-b",
     "a departing work with no measured relief centre, so a crossing cannot crystallize on one "
     "(pass-composer.js:6937)"),
    ("slice-repeat", "neutral", "a-to-b",
     "the one translation reading the base record leaves without an axis, given one"),

    # THE WITNESS CAMERA'S FOUR AXES, AND WHY EACH NEEDS A PAIR OF ITS OWN. The flight's whole
    # excursion is scaled by its REACH, which is the two works' own |luminance.level| gap
    # (pass-composer.js:9397); each axis on top of that reads a DIFFERENT measurement — roll the
    # lattice-angle gap, yaw the gate's own offset from the middle, pitch the horizon's place, the
    # dolly the two grains in ratio, the pan the measured centre (:5680-5799). So an axis is visible
    # only on a pair that stands apart in tone AND in that axis's own reading: two works differing in
    # tone alone fly nothing at all, and two differing in structure alone are scaled to nothing. Each
    # pair below is one axis's own two readings put at the ends of their spans together.
    ("dark", "gridded-askew", "a-to-b",
     "tone at one end of its span against a lattice turned the whole width of the angle span, which "
     "is what the flight's roll reads"),
    ("dark", "gate-upright", "a-to-b",
     "tone at one end of its span against a gate slot at the far end of its own place, which is what "
     "the flight's yaw reads"),
    ("dark", "centre-far", "a-to-b",
     "tone at one end of its span against a horizon and a measured centre at the far end of the "
     "frame, which is what the flight's pitch and its pan read"),
    ("bright", "centre-near", "a-to-b",
     "the same two readings at the other end of both spans"),
    ("dark", "coarse-grain", "a-to-b",
     "tone at one end of its span against a grain four octaves away, which is what the flight's "
     "dolly reads"),
    ("bright", "fine-grain", "a-to-b",
     "the same two readings the other way about"),

    ("bare-dark", "bare-bright", "a-to-b",
     "the whole span of `luminance.level` on a pair where every rival on the band cut reads nothing, "
     "so the crossing is `strata-light`'s own and its two level handles are driven at the two ends "
     "of the reading they declare"),
    ("bare-bright", "bare-dark", "a-to-b",
     "the same span the other way, so the handle that reads the departing work and its twin that "
     "reads the arriving one are told apart"),
    ("lattice-dim", "lattice-vivid", "a-to-b",
     "the whole span of `colour.sat` and `colour.contrast` on two works that both carry the lattice "
     "`grid-colour`'s own fit needs"),
    ("lattice-vivid", "lattice-dim", "a-to-b",
     "the same span the other way"),
    ("centre-near", "centre-far", "a-to-b",
     "the whole span a measured centre stands in, walked from one end of the frame to the other"),
    ("rings-few", "rings-many", "a-to-b",
     "the two ends of a ring device's own count, both works cut as rings so every handle that reads "
     "a ring is driven"),
    ("rings-many", "rings-few", "a-to-b",
     "the same two ends the other way"),
    ("seam", "seam-fine", "a-to-b",
     "two measured horizon seams at the two ends of the grain span, which is the pair "
     "`waterline`'s own `tideCells` stands its count between"),
    ("seam-fine", "seam", "a-to-b",
     "the same two ends the other way"),
]



# THE CONTROL COLUMN. Every class above stands against `neutral`, in both directions, and that is not
# a cross product: it is N pairs beside the N records, one per class, and it is what ISOLATES a
# dimension. A contrast above moves two things at once by design — `dark` against `bright` moves the
# whole tonal span — while a class against the control moves exactly what that class's own sentence
# says it moves and nothing else, so a reading that comes out different can only be that class's
# doing. Both directions are cases, because a handle that reads the DEPARTING work and its twin that
# reads the ARRIVING one are told apart by nothing else.
def _control_pairs():
    out = []
    for name, sentence, _ in CLASSES:
        if name == "neutral":
            continue
        out.append(("neutral", name, "a-to-b",
                    "the control against one class alone, arriving: " + sentence))
        out.append((name, "neutral", "a-to-b",
                    "the same class against the control, departing: " + sentence))
    return out


PAIRS = CONTRASTS + _control_pairs()


def pairs():
    """The ordered pair cases, as (departing id, arriving id, direction). Fixed and named."""
    return [(a, b, d) for a, b, d, _why in PAIRS]


def contrasts():
    """The class CONTRASTS alone, without the control column.

    A run with a rule PLANTED walks these. A plant is judged on whether an answer MOVES, and one
    breach is a move — so a planted run needs the cases where two classes stand against each other,
    not also the column that isolates each class against the control. It is a named subset of the
    same list rather than a count somebody chose, so a plant and the standing run are still walking
    the same kind of thing; the one row that compares a COUNT across the two runs reads a share
    instead, and says so at its own site.
    """
    return [(a, b, d) for a, b, d, _why in CONTRASTS]


def pair_why(a, b, direction):
    """The sentence one pair case stands for, so a red row can print it."""
    for pa, pb, pd, sentence in PAIRS:
        if (pa, pb, pd) == (a, b, direction):
            return sentence
    raise KeyError((a, b, direction))


# The one place in a work record where the KEYS are a measurement rather than a schema: a work is
# voted to be made of the substances it is made of, so the key set moves with the photograph.
OPEN_MAPS = {"matter.substanceVotes"}


def field_paths(record):
    """Every field path a record carries, as a set of dotted names with list indices collapsed.

    The schema smoke in both suites compares a real record's paths against the synthetic base's, so
    a field the site starts writing — or stops writing — shows up as a difference rather than as a
    handle that quietly reads nothing.
    """
    out = set()

    def walk(value, path):
        if path in OPEN_MAPS:
            # A map whose KEYS are data — the substances a work was voted to be made of — so the key
            # set is a reading and not a schema. The path stands for the whole map.
            out.add(path + ".{}")
        elif isinstance(value, dict):
            for k, v in value.items():
                walk(v, path + "." + k if path else k)
        elif isinstance(value, list):
            out.add(path + "[]")
            for v in value:
                walk(v, path + "[]")
        elif path:
            out.add(path)

    walk(record, "")
    return out


BASE_PATHS = field_paths(_base("shape"))
