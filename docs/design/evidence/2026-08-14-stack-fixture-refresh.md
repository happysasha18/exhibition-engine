# The stack bench's frozen passage follows the serialised score — 2026-08-14

The stack suite, `tests/test_pass_stack.py`, plays the worked pair's composed passage from a copy of
the score frozen in its own source, so it can run without the site tree. That copy had gone stale
against what the site now serialises. This unit refreshes it from the site's current serialised
score and leaves every row's threshold where it stood.

## Where it stands

| | |
|---|---|
| Repository | `/Users/sashaabramovich/exhibition-engine-stackfix`, a worktree of `/Users/sashaabramovich/exhibition-engine-pass-api-v1` |
| Branch | `pass-api-v1-stackfix` |
| Base | `8bd4932` — the tip of `pass-api-v1` |
| Result | `4582452` (the suite refresh) and this file's own commit |
| Source of the numbers | `/Users/sashaabramovich/tlvphotos-immersive/lab/data/sceneplan-scores/17847744487144891__17897050660015868__ab.json`, as re-serialised at site commit `7464c50` on `immersive-alpha` |
| Pattern followed | engine commit `12b9099`, where the coverage bench was refreshed against the same score |

## The frozen fields, before and after

Every figure below is read off the serialised score named above with
`python3 -c "import json; d=json.load(open(PATH)); ..."`, cue by cue, and written into the suite's
own constants block.

| Field | Before | After | The score's own |
|---|---|---|---|
| The meshing cue's window, `W_TRAVEL` | `[1.17, 5.59]` | `[0.00, 5.59]` | `cues[travel].window = [0.0, 5.59]` |
| The ground's band-count handle, `PIVOT_STRIPS` | `12` | `3` | `pivot-strips = 3` |
| The travelling voice's size ramp, `SIZE_FROM`/`SIZE_TO` | `0.7 → 1.8019`, a `segment` node on a smooth shape | `1.9919 → 0.7`, the score's own `mix` node over `cueProgress` | `travel-size = mix(a 1.9919, b 0.7, t cueProgress)` |
| The seed each cue is handed | `1.983657397` on all three cues | `CUE_SEED = 1.9837` on all three cues | `pivot-seed = travel-seed = arrival-seed = 1.9837` |
| The score's top-level seed, `SEED` | `1.983657397` | unchanged | `seed = 1.983657397` |

Two of these carry a consequence worth stating.

**The camera followed the window on its own.** The suite places the camera track's two middle points
at the travelling cue's window edges rather than writing seconds, so moving that window moved the
camera's middle points from 1.17 and 5.59 to 0.00 and 5.59 — which is exactly where the serialised
camera track carries them.

**The band count is the score's, not the floor's.** The woven instrument draws
`clamp(strips * nMul * clamp(cssWidth/1000, 0.5, 1), 3, 64)` bands
(`engine/assets/pass-inst-weave.js:220`). On the 390-point frame every instrument suite measures on,
the middle term clamps to 0.5, so a handle of 3 lands on the floor and draws three bands — the family
the composer measured. A handle of 12 drew six. The floor itself fell from 6 to 3 earlier the same
day, which is why the stale handle had to sit at twice the family's own number.

**The size ramp could be carried whole here.** The coverage bench keeps the pre-fix direction on
purpose: the score's own ramp stands the meshing pair large at the entry door, which reds a row there
proving an entry door free at every point, and that row may not be weakened. This suite asks nothing
of that kind of the meshing voice, so the score's own ramp is carried. Measured rather than assumed:
the door row photographs the three-cue pass at 0.00 s and a one-cue pass of the ground alone at the
same instant, both at 390×844, and differences them channel by channel — mean 0.0000 of 255, worst
channel 0. The travelling voice, now live at the door, adds nothing at all there, because its shader
publishes the arriving work's absence as its own alpha and that work is absent everywhere at the
entry door.

## Instants derived from the windows

The brief asks that an instant the suite reads be derived from the score's windows rather than named
in seconds. Four places were changed:

- `INSTANTS`, the grid the pass is photographed at, is now the set of the score's own door and window
  edges — `W_PIVOT[0]`, `W_TRAVEL[0]`, `W_ARRIVAL[0]`, `W_TRAVEL[1]`, `W_PIVOT[1]` — together with
  three middle readings, 1.17, 2.5 and 5.0 s. It reads 0.00, 1.17, 2.50, 4.03, 5.00, 5.59, 6.50 today.
  1.17 s used to be the travelling voice's opening and stays in the grid as a middle reading.
- `MEET`, where all three voices are live, is computed from the three windows — the last opening to
  the first closing, 4.03…5.59 s — and `MEET_MID`, its midpoint at 4.81 s, is the instant the rows
  that need all three cues live now read: the resource sum and census row, the one-canvas row, and
  the repeatability row. They named 5.0 and 4.5 s before.
- The door row samples the one-cue pass at `W_PIVOT[0]` and reads the three-cue capture from the same
  key, instead of naming 0.0.
- The two rows whose text quoted 4.03…5.59 s now format those figures from the windows themselves.

One divergence is left standing, deliberately, and is named in the suite's own comment: the banding
**axis**. The score asks for 0 and this copy carries 2, as the coverage bench also does against the
same score. It is not among the fields this refresh was asked for, and the coverage bench at
`12b9099` — the pattern this unit follows — kept it likewise. It belongs to whoever owns the
composer's own axis reading.

No row's threshold, expectation or reach was weakened. Nothing was added to the matrix and no test
was removed.

## The commands, in order

```
git -C /Users/sashaabramovich/exhibition-engine-pass-api-v1 worktree add \
  /Users/sashaabramovich/exhibition-engine-stackfix -b pass-api-v1-stackfix
cd /Users/sashaabramovich/exhibition-engine-stackfix
python3 tests/test_pass_stack.py
python3 tests/run_all.py > docs/design/evidence/2026-08-14-stack-fixture-prover.log 2>&1
```

## What the runs said

The stack suite alone, run first: **23 passed / 0 failed / 0 skipped**. Every browser row and all
four red-on-bug proofs ran; none was pinned to a skip.

The full prover, one run, its own runner owning its concurrency: **55/55 suites green, wall 249 s**,
exit 0. `pass_stack` reads 23 passed / 0 failed / 0 skipped inside it, and `pass_coverage`, which
holds the other frozen copy of the same score, stays at 18 passed / 0 failed / 0 skipped.

The log is kept at
`/Users/sashaabramovich/exhibition-engine-stackfix/docs/design/evidence/2026-08-14-stack-fixture-prover.log`.

Running the full prover rewrites `tests/suite_timings.json`, the queue order the runner reads from
the last full green run; that file is committed here with the run that produced it.

## Conclusion

The stack bench now benches the passage the site serialises: the meshing cue opens on the pass's own
entry door, the ground asks for the three bands the composer measured, the travelling voice's size
ramps the score's own way from 1.9919 down to 0.7, and every cue carries the seed the serialiser
writes. Both suites that hold a frozen copy of this score are green together, and the branch is ready
for the delivery seat to merge.

## Limitations

- The two photographs the bench draws with are the walk's own stand-ins, not the worked pair's files,
  which are not in this tree. What the rows measure is the stack — which cue draws when, in what
  order, on one canvas — and that is a property of the score.
- The frozen copy stays a copy. It goes stale again the next time the composer re-serialises, and
  nothing in this tree watches the site's score for it; the two benches holding a copy are
  `tests/test_pass_stack.py` and `tests/test_pass_coverage.py`.
- The banding axis divergence above is recorded, not resolved.
- The branch is committed only. No merge, no push, no deploy was performed.
