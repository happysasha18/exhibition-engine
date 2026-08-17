# U24 — the choice core runs in the browser, and its scores are the build's own bytes

Run 2026-08-17, 17:24–17:54 local. Engine lane `/Users/sashaabramovich/exhibition-engine-jscomposer`,
a worktree of `/Users/sashaabramovich/exhibition-engine-pass-api-v1`, branch
`pass-api-v1-jscomposer`, cut from the integration head `3665da0`. Site lane
`/Users/sashaabramovich/tlvphotos-jscomposer`, branch `immersive-alpha-jscomposer`, cut from
`immersive-alpha` at `618d21c`; the equality harness and its readings live there.

Root: his law of 2026-08-14 16:14 and his word of 2026-08-17 17:06 — a pair's crossing is decided
at show time and the product carries no table of pairs. The unit brief is
`/Users/sashaabramovich/tlvphotos/docs/immersive/briefs/2026-08-17-U24-composer-in-browser.md`.

## 1. What stood before

The whole decision lived in the site's build. `lab/build-sceneplan-v1.py` reads four measurement
files, composes every ordered pair the pair table carries, and writes one template per passage
shape and one numeric row per pair; `lab/sceneplan-to-score.py` turns a filled plan into the §4.4
score a host plays. The product then shipped rows: a table of 6 304 pairs over 116 works, fetched
by a phone. That table is quadratic in the collection, which is the shape his law refuses.

The choice itself was already stdlib arithmetic over records that describe ONE work each —
`compose()` at `lab/build-sceneplan-v1.py:1723`, about 933 lines, opening no image and reading no
clock. Nothing in it needed a build.

## 2. What landed

`engine/assets/pass-composer.js`, an engine-owned asset beside the instruments, carrying its own
version literal `COMPOSER_VERSION = "1"` and its own byte fence. It is handed the two works'
records, a direction and a seed, and it answers with the score, its compact weight, and the shape
it chose — or with a decline in the composer's own sentence.

It carries the whole road: the pair's own pivot derived from the two works (the shared measure
against the collection's discriminating thresholds, then the shared turn, the shared palette
region, and the tonal-and-spectral bridge, in the elements builder's own order of precedence), the
travelling axis, the actors, the arrival and its locus, the voices and the tier, the levels law,
the camera flight, the meshing instrument's own door reading, the passage shape and its template,
the fill, and the serialisation.

Three habits of Python are carried across with it, because byte equality lives in them: a value
Python holds as a float is marked as one and printed with its trailing zero and its negative zero;
`round` is half to even on the double's exact value; and the score is written with sorted keys, one
space of indent and unicode as itself. A non-integral number reaching the writer unmarked stops the
run by name rather than being guessed at.

Nothing about an instrument is written into the file. The manifests, the cut-line floors, the
thresholds, the door record, the score fence and the provenance sentence are handed to `make()` as
the collection's own constants, so each of those numbers keeps its one home.

**The file is unwired.** It is not in `engine/build.py`'s served list, no client fragment names it,
and no walk asks it for anything. The pack ships exactly as it shipped. Wiring is the next unit,
and this record is the proof it is gated on.

## 3. The equality, pair for pair

The harness lives in the site lane at `lab/jscomposer/` and ships nowhere:

| file | what it does |
| --- | --- |
| `dump-inputs.py` | writes the per-work records and the collection constants, calling the composer's own readers rather than restating them |
| `python-expected.py` | composes every ordered pair the Python way and writes each score's own SHA-256 and its two lengths, and every decline's own sentence |
| `equality.js` | loads the engine module the way the bake serves it and holds every answer against Python's |
| `in-browser.py` | runs the same module inside headless Chrome and checks the scores it composes there |

The numbers, from `lab/data/jscomposer/equality-reading.json`:

* **10 558** ordered pairs asked — every pair the pair table carries, over 121 works.
* **6 304** the Python composer accepts. JavaScript composed all 6 304, and every one of them is
  **byte-identical**: same SHA-256 over `json.dumps(score, ensure_ascii=False, indent=1,
  sort_keys=True)`, and the same compact weight `passScoreCheck` measures. **Mismatches: 0.**
* **4 254** the Python composer declines. JavaScript declines all 4 254, each with the **same
  sentence, character for character**. Differences: 0. Pairs composed on one side and declined on
  the other: 0 both ways.
* The two worked pairs of `lab/PASSAGE-COMPOSER.md` §2 are also compared as whole text, not only as
  a digest, and the files match with no difference at all.

The road the expected side walks is the shipping road, and it is shown to be: filling every row
from the SHIPPED `lab/data/sceneplans/templates.json` and `table.json` lands on the same 6 304
digests (`python-expected.py --verify-shipped`, "6 304 identical, 0 different").

That the JavaScript derives the pivot from the two works rather than reading a row is what makes
this a proof of his law rather than a port of a lookup: 10 558 answers agree, and no pair table was
opened on the JavaScript side.

## 4. In a real browser

`python3 lab/jscomposer/in-browser.py`, run 17:49 local under one of the machine's two browser
slots: the module is served with its namespace token resolved, exactly as the bake serves an engine
asset, loaded in headless Chrome beside the records the sample names, and asked for **200** pairs —
the two worked ones and 198 sampled across the whole table. All **200** scores composed in the
browser hash to the bytes Python wrote. Reading: `lab/data/jscomposer/in-browser-reading.json`
(that run predates the stamp field the script writes now, so the file's `readAt` stands empty).

## 5. The red proofs

`node lab/jscomposer/equality.js --plants` runs eight planted divergences, each one number or one
rule changed in a COPY of the module, and holds each run's colour against the colour it was planted
to produce. Reading: `lab/data/jscomposer/planted-reading.json`.

| plant | what it changes | expected | scores identical | declines matched |
| --- | --- | --- | --- | --- |
| `strips` | the strip count reads the arriving work's parts | red | 3 200 / 6 304 | 4 254 / 4 254 |
| `sizefloor` | the meshing travel may go under its measured floor | red | 6 112 / 6 304 | 3 445 / 4 254 |
| `window` | the meshing cue opens at 0.18 of the pass again | red | 5 912 / 6 304 | 4 254 / 4 254 |
| `rounding` | a measured number is rounded to five places | red | 587 / 6 304 | 2 862 / 4 254 |
| `tiebreak` | the travelling axis breaks its tie the other way | red | 6 302 / 6 304 | 4 254 / 4 254 |
| `floatprint` | an integral float loses its trailing zero | red | 0 / 6 304 | 4 254 / 4 254 |
| `culmination` | a far pair is a culmination at 0.4 instead of 0.5 | red | 6 297 / 6 304 | 4 254 / 4 254 |
| `doorhold` | the doors are held for 0.09 of the pass | **green** | 6 304 / 6 304 | 4 254 / 4 254 |

Seven redden. The eighth is green on purpose and it is the reach of this harness said out loud: the
door hold reaches the plan's own budget and no field of the score, so a run that compares scores
cannot feel it. Anything living outside the score is outside what these numbers prove.

## 6. The byte fence

`tests/test_budget.py` carries the file at **20 000 B** gzipped, measured at **17 040 B** as the
bake would serve it — comment-stripped, gzip level 6, mtime zeroed. `python3 tests/test_budget.py`:
10 rows, 10 pass, 0 fail. The two suites that enumerate `engine/assets/` (`test_pass_pack.py`,
`test_pass_coverage.py`) select on the `pass-inst-` prefix, so an unwired asset of another name
neither enrols nor reds.

The per-work record it reads weighs **2 239 B** a work before compression — 270 855 B for all 121 —
against the 1 862 611 B of pair rows the shipped table stands on today.

## 7. Decisions taken here, with their sources

1. **One engine tree named.** Both sides read `~/exhibition-engine-jscomposer` through
   `EXHIBITION_ENGINE_ROOT`. The composer refuses to choose between trees that publish different
   manifests (`_engine_roots`, `lab/build-sceneplan-v1.py:99`), so the tree the module stands in is
   the tree its numbers come from.
2. **Two lanes, and the seat merges both.** The main site tree is held by another unit, so the site
   half runs in the worktree `tlvphotos-jscomposer` on `immersive-alpha-jscomposer`. The precedent
   is U2, which ran its site lab in `tlvphotos-weavefloor` on `immersive-alpha-weavefloor` and left
   the merge to the delivery seat. This lane merges the same way the engine lane does.
3. **The per-work record carries the per-work readings.** Each element set arrives with its part
   count, its count of real elements, the element the work's dominant object stands on, and its
   measured grain, rather than with every element's geometry. That is §4.4c's own split — a fact
   depending on one work is written once — and it is what keeps a record at 2.3 KB.
4. **The seed is an input.** It reaches the score, so both sides roll one die; who rolls it, and
   from what, is the walk's own question and stays outside this unit.
5. **The derived inputs are not committed.** `work-records.json`, `consts.json` and
   `python-expected.json` are rebuilt by the two Python scripts in about ten seconds from files the
   repository already carries; the readings, which are small and are the evidence, are committed.

## 8. What waits on the seat

* **The door record is still handed in.** `holdTheDoors` reads the meshing instrument's own door
  measurement, keyed by pose, out of `lab/data/mesh-doors.json`. It is the instrument's number
  rather than the composer's, and in the product it can arrive two ways: the instrument answers for
  its own doors at run time, or the record travels beside the pack. That is an architecture choice
  for the wiring unit and it is parked here rather than decided.
* **The wiring unit's shape.** This module answers `scoreFor(recordA, recordB, direction, seed)`.
  What a walk hands it, and where the per-work records are fetched from, is the next unit's brief.
