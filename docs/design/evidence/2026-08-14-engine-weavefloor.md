# Engine-side weave floors and capture-fixture refresh — unit U3 (engine half)

Written 2026-08-14, on branch `pass-api-v1-weavefloor` in
`/Users/sashaabramovich/exhibition-engine-weavefloor`. The unit started at `f51cc96` and the work of
it stands in four commits on top of that one. No merge into `pass-api-v1`, no push, no deploy; the
merge belongs to the delivery seat.

## Base and result

    integration branch   pass-api-v1                      f51cc96   clean at start
    lane branch          pass-api-v1-weavefloor                     the result, its tip below
    site reference       ~/tlvphotos-immersive            a1c5dea   read only
    the lab module       lab/effects/weave.js             148affb   the source of the floors

The three commits of the work, and a fourth that carries this file:

    75b5645  The woven instrument's four band-count gates stand at three, as the lab module's do
    018ad75  Three bands are held against the lab module and read by the collection's own banding measure
    12b9099  The coverage bench's frozen score follows the composer's own: the meshing cue opens at the door and the ground asks for three bands
             The engine-side weave floors and the refreshed capture score, with the three-band
             acceptance measured — this file, the log beside it and the runner's own timing record.
             It is the branch tip, and a commit cannot carry its own hash in its own text.

## The exact commands

    git -C /Users/sashaabramovich/exhibition-engine-pass-api-v1 worktree add \
      /Users/sashaabramovich/exhibition-engine-weavefloor -b pass-api-v1-weavefloor f51cc96
    python3 tests/test_pass_weave.py
    python3 tests/test_pass_coverage.py
    python3 tests/run_all.py > docs/design/evidence/2026-08-14-engine-weavefloor-prover.log

The weave suite ran twice and the coverage suite twice: once each to read what the change did, once
each on the state that stands. No other suite was run on its own, nothing was linted or formatted,
no dependency was touched, and no git command restored or reset a working tree.

## What moved in the instrument

`engine/assets/pass-inst-weave.js` carries the lab module's mathematics character for character, and
four gates between the handle and the shader still stood where the module had left them. They now
read three, which is what the module reads:

    gate                                          was    now
    the declared param range, params.strips         6      3
    the published handle range, handles.strips      6      3
    the frame number clamp in values()              6      3
    the shader floor, max(N, uNv * (1 - 0.25*b))    5      3

The published record moved with them: `applied.floor` from 6 to 3 and `applied.drawnFloor` from 5 to
3, so the number the manifest publishes and the number the frame draws are one number at three bands
as at six. The shader's own text is now identical to the module's, line for line, across all 96
lines of it. The manifest's note that carried the reasons was rewritten from the module's own block:
why three and not lower, why three and not higher, the published limits, and the plain sentence that
the floor buys reachability and not strength. The engine-side figure of 0.82 at three bands, which
that note used to quote as measured, is stated as retired on the record of the module's own sweep.
The provenance commit moved from `547a100` to `148affb`, the commit whose mathematics this file now
carries.

## The frozen capture score

`tests/test_pass_coverage.py` benches a copy of the composer's score frozen in its own source, and
the copy had gone stale. The meshing cue's window read

    before   [1.17, 5.59] of a 6500 ms pass   =   0.18 - 0.86
    after    [0.00, 5.59] of a 6500 ms pass   =   0.00 - 0.86

which is the window the site's plans, its serialised scores and its staging bake have all carried
since site commit `24f0b45`. Three further fields were refreshed against the same serialised score,
`lab/data/sceneplan-scores/17847744487144891__17897050660015868__ab.json`: the ground's band-count
handle from 12 to 6, the seed each cue is handed from 1.983657397 to the 1.9837 the serialiser
writes, and the interruption budget from 320 to 500 ms. The score's own top-level seed keeps its
full 1.983657397, which is what the score carries.

The band-count handle is worth its own sentence. It stood at 12 because a handle of 6 and a handle
of 12 drew the same six bands while the instrument's floor stood at 6, so the fixture wrote down the
number that reproduced the frame rather than the number the score carries. With the floors lowered,
a handle of 6 on this 390 point frame draws three bands, which is the family the composer measured
and asked for. The score's own plan requests 3, and on a 390 point frame a handle of 3 and a handle
of 6 both draw three bands, so this figure survives the composer's next serialisation either way.

Two instants in the suite were derived rather than written down. The travelling voice's entry door
is now read at its window's own opening, and so is the red-on-bug proof that stands on it; a row
naming the second it used to open at would have gone on measuring an instant that is no longer a
door. With the window moved onto the pass's own entry door, that frame answers in the entry-door row
and in the door row alike, and both rows say so.

## What the refreshed bench measures

Every figure below is from the run that stands, and every row is measured rather than asserted.

    door A at 0.000 s against the ground drawn alone      mean 0.000000   worst channel 0
    door B at 6.500 s against the arrival drawn alone     mean 0.000000   worst channel 0
    the travel's entry door at 0.000 s                    mean 0.000000   worst channel 0
    the arrival's entry door at 4.030 s                   mean 0.000000   worst channel 0

At 2.000 s the stack agrees with the ground drawn alone across 100.0% of the frame and differs from
the travelling voice drawn alone by mean 51.468 of 255, worst channel 235. At 5.000 s the ground
still reaches 16.3% of the frame. The share the ground reaches across the middle:

    1.17s 100.0%   2.00s 100.0%   2.50s 100.0%   3.00s 95.9%   3.50s 79.1%
    4.03s  24.0%   4.50s  12.5%   5.00s  16.3%   5.59s 24.4%

The best single whole-frame weight explaining the stack is 0.6814 at 4.030 s and 0.9356 at 5.000 s,
leaving residuals of 39.76 and 20.77 channel units against a seam threshold of 6. A one-cue score is
unchanged to the pixel across 21 comparisons, worst channel 0. The step where the travelling voice
leaves its window, 5.58 to 5.60 s, moves the frame by mean 15.8160 of 255 under coverage and by the
same 15.8160 before it.

## The three-band acceptance

The conformance rows held the instrument against the lab module on the two doors and the woven
middle, and not one of those poses asked for three bands, so the pose the whole change exists for
went unmeasured. Two poses were added, one per frame the count has to hold on, and each is read on
the worked pair's own two works — the band family the passage stands on was measured on those two
and on no others. The pose is pinned the way the module's own rig pins it, through the module's
declared handles alone: the ribbon axis standing up and down, the dial at the middle, and the clock
held at the second where the module's own strip-count breath crosses 1, so the drawn count is the
handle times the frame's width term with nothing drifting under the shot. The module is driven, its
pose is read, and the host is handed that pose, so what is compared is two roads of one frame.

    frame        handle   drawn by the      drawn by the    drawn      vertical family
                          instrument        lab module      period     read on the drawn frame
    1440 x 900        3          3.00            3.00     480.0 px     480.0 px, strength 0.6638
     390 x 844        6          3.00            3.00     130.0 px     130.2 px, strength 0.5853

On both frames the strongest family of either axis is the vertical one, at the same period and the
same strength. The host's frame and the lab module's frame agree at three bands: mean 0.0080 of 255
with a worst channel of 37 on the wide frame, and mean 0.0117 with a worst channel of 11 on the
phone, against the carrier check's own bar of 1.5.

The drawn frame is read by the collection's own banding measure, `measure_banding` in
`lab/cut-lines.py`, imported and not copied — the very function that read 0.8807 and 0.8437 off the
two photographs. Where the peak lands is what the added rows judge. How strong the family reads is
reported beside it and is not judged, because it moves with the second the pose is held at: the
module's own sweep at the pair's seed read 0.4149 on the wide frame and 0.3735 on the phone at
another second, and the floor was lowered to buy reachability, never a strength.

## The runs

    python3 tests/test_pass_weave.py        47 passed / 0 failed / 0 skipped
    python3 tests/test_pass_coverage.py     18 passed / 0 failed / 0 skipped
    python3 tests/run_all.py                55/55 suites green, wall 252 s

The weave suite stood at 43 rows before this unit and stands at 47: the four added rows are the
three-band acceptance, two per frame. The coverage suite stood at 18 rows and stands at 18. The full
run's log is saved beside this file at
`docs/design/evidence/2026-08-14-engine-weavefloor-prover.log`.

## The byte fences

    pass-inst-weave.js, built                 12 830 B   against 13 900   1 070 B under
    pass-inst-weave.js, gzipped at level 6     4 167 B   against  4 500     333 B under

The gzip figure is taken over the comment-stripped text the bake ships, which is how
`tests/test_budget.py` measures it. The port is byte-neutral: at `f51cc96` the same two measurements
read 12 834 B stripped and 4 171 B gzipped, so the lowered floors cost nothing and the rewritten
note costs nothing either, comments not travelling to a visitor.

## Conclusion

The engine instrument now reaches three bands, and it reaches them by the lab module's own numbers
rather than by a second set: the shader text is identical line for line, the four gates read the
same floor, and the host's frame and the module's frame agree to hundredths of a channel at the
count the change exists for. The composed passage's ground is drawn at the pair's own period on both
frames it has to hold on, 480 px of 1440 and 130 px of 390, and the frozen capture score no longer
opens the meshing cue a fifth of the way into a pass the site opens at the door.

## Limitations, and what was set aside

THE TRAVELLING VOICE'S SIZE RAMP IS LEFT AS THIS BENCH HAS CARRIED IT, and the divergence is a
finding rather than a closed question. The serialised score ramps the size from the first work's
measured ring reading down to the second's, 1.8019 to 0.7, through a plain mix; the bench ramps it
the other way through a smoothed segment. Carried across as the score has it, and measured, the
meshing instrument's entry door stops being free at every point: at 1.8019 its wheel pair stands
large enough that the meeting line reaches inside the frame at the door, and door A at 0.000 s then
reads mean 0.000052 of 255 with a worst channel of 18 — one pixel of the arriving work at an alpha
of about 0.07 where the law says every point is 0. That is a reading about the score the composer
serialises, not about the coverage law this suite proves, and the row it reddens is one this unit
may not weaken. The direction therefore stays as it stood and the question goes to whoever owns the
composer's own ramp, in the site tree, which is outside this unit's write set.

`tests/test_pass_stack.py` carries its own frozen copy of the same passage — the window at
[1.17, 5.59], the band-count handle at 12, the size ramp at 0.7 to 1.8019 and the full seed in every
cue. This unit's brief names the coverage fixture and no other, so the stack suite is untouched; it
is green at 23 rows. One passage frozen in two files is a second home for one fact, and the delivery
seat should know it stands.

The composer's re-serialisation of its plans, which the restart handoff lists under this unit, is
site-tree work and is not part of this brief. Until it runs, the site's serialised score keeps a
band-count handle of 6 with the note that a request of 3 was raised to it by a floor that no longer
stands; on a 390 point frame the two handles draw the same three bands, so nothing a visitor sees
waits on it.

The engine's own `values()` keeps one line the lab module has no counterpart for: it answers a
reduced-motion pose with a turn held at zero. That line predates this unit and was left alone.

Nothing left the machine, and nothing outside this worktree was written.
