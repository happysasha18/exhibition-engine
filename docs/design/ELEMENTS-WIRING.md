# The elements on the wire — three blocks ready to apply

Charter shelf 14 asks for matter verbs from the стихии. Water was already built twice
(`pass-inst-liquid.js`, `pass-inst-waterline.js`). The other three now exist as instruments:

| instrument | file | what it draws |
|---|---|---|
| `pour` | `engine/assets/pass-inst-pour.js` | the departing work falls a column at a time and heaps into the arriving one along its own angle of repose |
| `veil` | `engine/assets/pass-inst-veil.js` | four sheets of veil hang between the eye and the two works, which trade depths; each is seen through whatever veil stands in front of it |
| `wind` | `engine/assets/pass-inst-wind.js` | one gust crosses the rows of the picture, bending them, and the change of hands rides its front |

Each has its own suite (`tests/test_pass_pour.py`, `tests/test_pass_veil.py`,
`tests/test_pass_wind.py`) and each declares its own `cuts:` beside its `levels` and `roles`, so
none of them needs a row in the site's migration table.

None of them can play yet. What is missing is the composer's side, and this note carries it.

---

## Until the fill branch exists, the instrument must not reach the wire

An instrument plays only where `engine/assets/pass-composer.js` holds three things for it: a
suitability reading in `INSTRUMENT_SUITS`, a register row per handle in `HANDLE_SOURCE`, and a fill
branch in `fillPlan`. Without the fill branch every handle stands at its manifest default for every
pair alike, so **the instrument would play the same crossing on every pair of photographs in the
world** — the sameness his word of 2026-08-18 08:52 names, and the same defect the water and the
floor were found in on 2026-08-18 15:13 («no static transitions»): a cue chosen and shaped by a
constant that never looked at either photograph.

The suitability reading is the second half of it. `suitsPair` answers `0.5` with «publishes no
reading of a pair» for an instrument `INSTRUMENT_SUITS` says nothing about — a typed constant that
ranks above every measured reading on some pairs and below it on others, permanently, on no
evidence. That is the very row the water's own entry was written to close.

So these three instruments must not be published in a settings record until this note is applied.
**What holds them back is not a switch — it is that the site's staging step has not yet harvested
them.** The mechanics, checked rather than assumed:

- `engine/build.py:761` `_pass_instrument_sources()` globs `engine/assets/pass-inst-*.js` and takes
  every file it finds. So the bake already writes all three served files and already records them in
  `config.json`'s `pass.instruments` block, with their versions and digests. **Creating the files
  put them into the bake.** That alone is harmless: the record only tells a host where to fetch a
  file whose name a score's cue already named.
- What decides whether a cue can name them is the composer's own `consts`. `ALL_INSTRUMENTS` is
  `Object.keys(consts.instruments)` filtered by `consts.manifests`, and `CUTS_ON` is derived from
  the same record — both come from the site's staging step (tlvphotos `lab/jscomposer/dump-inputs.py`,
  which reads the same `engine/assets/pass-inst-*.js` files and takes each manifest's own `cuts`).
  The frozen fixture this tree tests against (`tests/fixture_pass_composed.json`) carries
  twenty-two instruments and none of these three, and `tests/test_pass_composed.py` treats a file
  that ships without being published as reported-beside-the-row rather than judged by it.
- **Therefore: in this tree, creating the three files puts nothing on the wire today.** The moment
  the site's staging step runs again it will harvest them by the same glob, publish their manifests
  and their `cuts`, and they will join `ALL_INSTRUMENTS` and `CUTS_ON` automatically — with a typed
  `0.5` fit and every handle at rest. There is no gate between the harvest and the cast. The order
  that has to hold is: **apply this note to the composer first, then let the site stage.**

---

## 1 · `pour`

### The suitability reading — `INSTRUMENT_SUITS`, beside `parquet`

A pour needs two things from a pair and reads one for each: a picture that will let go in pieces,
and a material that falls being the material that heaps. Both readings stand on any two photographs;
neither can remove a pair, and a pair that reads nothing ranks last and still plays where nothing
ranks higher.

```js
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
```

### The register rows — `HANDLE_SOURCE`

`mix`, `clock`, `seed`, `shade` and `mask` already carry rows of the right shape. Four new rows,
all instrument-scoped (`sourceOf` reads the scoped row first), because each of these names means
something of this instrument's own:

```js
    "pour.columns": ["measured", "the work's own frame side over structure.grid.periodPx, the "
                                 + "count of its own measured lattice across it; the same off "
                                 + "structure.ownDevice.stepPx where no grid period was derived. "
                                 + "The picture lets go along the repeat it was made on"],
    "pour.repose": ["measured", "texture.detailPx of the two works, read as a ratio: the heap is "
                                + "made of the arriving work, and a finer material heaps at a "
                                + "steeper angle than a coarse one"],
    "pour.stagger": ["measured", "structure.regions.score of the departing work — how much of the "
                                 + "difference between its own columns its region line explains, "
                                 + "which is how plainly it lets go region by region rather than "
                                 + "all at once"],
    "pour.grain": ["measured", "texture.spectralPeriodPx of the two works, read as a ratio — the "
                               + "departing work's own strongest repeat said as cells across the "
                               + "frame, which is the unit the material instrument's coarse grain "
                               + "is published in"],
```

### The fill branch — `fillPlan`, in the `instr ===` chain

```js
        } else if (instr === "pour") {
          // THE POUR'S FOUR HANDLES. Without this branch all four rest at the instrument's own
          // pour — a correct pour, but the SAME pour for every pair, which is what this branch
          // exists to close.
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
          // is worth, and what both records carry is which of the two materials is finer. The heap
          // is the arriving work, so a ratio over one — the arriving work finer than the departing
          // one — walks the handle up and the heap stands steeper. `alongTheSpan` places it about
          // the instrument's own rest a doubling at a time, so the whole span is reachable and a
          // ratio of one lands exactly on the rest.
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
          // HOW COARSE THE MATERIAL IS, off the two works' own strongest repeats as a ratio. A
          // coarse departing work — a long repeat — pours in few large crumbs, so the ratio is
          // taken the other way up from the repose: the arriving work's period over the departing
          // one's, which walks the handle DOWN toward the coarse end as the departing work's own
          // repeat grows.
          if (mf.spectralPeriodPx > 0 && mt.spectralPeriodPx > 0) {
            wanted.grain = flt(r4(alongTheSpan("pour", "grain",
                                               mt.spectralPeriodPx / mf.spectralPeriodPx)));
          }
```

Where the handle travels: `columns`, `stagger` and `grain` are single values — the pour is one
event with one material, and a column count that moved mid-pass would re-cut the frame under the
visitor. `repose` is a single value for the same reason: the heap's own ceiling is derived from it,
so a repose that travelled would move the ceiling the exit door stands on. All four rest at the
instrument's own defaults where the pair carries no reading.

---

## 2 · `veil`

### The suitability reading — `INSTRUMENT_SUITS`

```js
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
```

### The register rows — `HANDLE_SOURCE`

`mix`, `clock`, `seed` and `mask` already carry rows. Four new ones, instrument-scoped:

```js
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
```

### The fill branch — `fillPlan`

```js
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
          // is the order this file already prefers them in everywhere else.
          var vAng = mf.gridAngleDeg || mf.deviceAngleDeg;
          if (vAng) wanted.airAngle = flt(r4(Math.abs(vAng) % 180.0));
```

---

## 3 · `wind`

### The suitability reading — `INSTRUMENT_SUITS`

```js
      // THE AIR CATCHES WHAT BANDS. The two works' own banding readings say how much row structure
      // there is for a gust to take, and the STRONGER end carries it — the front travels from one
      // work's rows to the other's, so one work of plain rows is enough to watch the air bend
      // something. How far apart their two lattices stand says whether the front comes in ACROSS
      // the picture's own grain, which is what makes a gust read as air rather than as a wipe.
      wind: function (a, b) {
        var sa = readingOf(((a.structure || {}).banding || {}).score);
        var sb = readingOf(((b.structure || {}).banding || {}).score);
        var aa = Number(((a.structure || {}).grid || {}).angleDeg) || 0;
        var ab = Number(((b.structure || {}).grid || {}).angleDeg) || 0;
        var gap = (((aa - ab) % 180) + 180) % 180;
        var across = Math.min(gap, 180 - gap) / 90;
        return [clamp01((Math.max(sa, sb) + across) / 2),
                "the two works read banding at " + pyText(flt(r4(sa))) + " and "
                + pyText(flt(r4(sb))) + ", so the air has rows to catch at the stronger end, and "
                + "their two lattices stand " + pyText(flt(r4(across))) + " of a right angle "
                + "apart, which is how far across the picture's own grain the front comes in"];
      },
```

### The register rows — `HANDLE_SOURCE`

`mix`, `clock`, `seed`, `shade`, `travel` and `mask` already carry rows. Four new ones, all
instrument-scoped. `axis` in particular MUST be scoped: the shared `axis` row names the right
measurement, but the woven instrument's `axis` is an enum of three band-family codes and this one's
is a direction in half turns, so an unscoped row would hand a code to a handle that expects an
angle — the exact class the scoped rows were introduced for on 2026-08-18.

```js
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
                             + "rather than square to a direction nobody measured"],
```

### The fill branch — `fillPlan`

```js
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
          var codeFrom = (bandFrom !== undefined && bandFrom !== null
                          && num(bandFrom[2]) < BANDING.length)
            ? AXIS_OF_BANDING[BANDING[num(bandFrom[2])]] : null;
          var codeTo = (bandTo !== undefined && bandTo !== null && num(bandTo[2]) < BANDING.length)
            ? AXIS_OF_BANDING[BANDING[num(bandTo[2])]] : null;
          var windCode = codeFrom !== null ? codeFrom : codeTo;
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
          // stops there rather than inventing a scale to fit it.
          var wAng = mf.gridAngleDeg || mf.deviceAngleDeg;
          if (wAng || wanted.axis !== undefined) {
            var rowDeg = (wanted.axis === undefined ? 0 : num(wanted.axis)) * 180.0;
            var off = (((Math.abs(wAng) - rowDeg) % 180) + 180) % 180;
            if (off > 90) off = 180 - off;
            wanted.lag = flt(r4(clamp01(Math.tan(off * Math.PI / 180.0))));
          }
```

---

## What was checked before this note was written

- Every block above was run against stub records — one pair with readings and one pair with none —
  and answers numbers rather than throwing. On records carrying nothing at all, every suitability
  reading answers a fit of nothing with its sentence, and every fill branch writes no handle, so
  every handle rests at the instrument's own default. Nothing here refuses a pair.
- The three instruments' own doors were walked over the whole span of every handle that could move
  one, on four buffers each, by their own suites: 800 poses for the pour, 2 400 for the veil, 1 728
  for the wind, none leaking. So a handle this note drives to any value in its published range
  still lands both doors on a whole work.
- `HANDLE_SPECS` is derived from each manifest at `make` time, so the three `HANDLE_SPECS.<id>`
  reads above need nothing added by hand — they exist the moment the record publishes the manifest.
