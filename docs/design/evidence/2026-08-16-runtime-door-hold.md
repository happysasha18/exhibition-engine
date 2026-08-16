# U15 — the door is held at run time, on the grid the shader actually draws on

Run 2026-08-16, 03:15–04:05 local. U11 taught the meshing instrument to read its own doors and refuse
a leaking one. U12 then swept the frames a visitor holds and found that the reading was taken on the
wrong grid: the doors were read on the CSS frame while the shader samples on the drawing buffer, and
on four of the five buffers a phone draws a 390 × 844 CSS frame on, the sizes the composer serialises
leak. This unit moves the reading onto that buffer and, where the size handed in leaks there, moves
the instrument to the nearest size whose door is whole, keeping the request on the record.

## The trees

Engine: `/Users/sashaabramovich/exhibition-engine-doorhold`, a worktree of
`/Users/sashaabramovich/exhibition-engine-pass-api-v1`, branch `pass-api-v1-doorhold`, from
`pass-api-v1` at `53ccd565647e356affe3f21a3b4229dc1fc137c8` (`53ccd56`), which carries U11's guard:

    6a73c74  The meshing instrument reads its doors on the buffer it draws on and holds a leaking
             one to the nearest whole size
    9e60c1e  The meshing instrument's two byte fences move to its own measurement, with a dated
             note beside each
    HEAD     this record

Nothing was merged, pushed or deployed. The site tree `/Users/sashaabramovich/tlvphotos-immersive`
was read and never written: `lab/data/mesh-doors.json`, `lab/data/mesh-doors-request.json` and
`lab/data/mesh-doors-frames.json` are the measurements this unit answers and is measured against.

## 1 — what was decided, and by whose word

The seat's ruling of 2026-08-16 02:44, from U7's own accepted law that the door's wholeness outranks
the ratio's fidelity with the loss recorded: the door is held at run time on the grid the shader
binds; the composer's serialised size stays the request; the instrument moves to the nearest size
whose door is whole on the drawn buffer; U11's guard refuses only where no whole size stands near; no
serialised per-frame table is built. Everything below follows that ruling, and the three things it
left open were settled from written sources rather than by taste:

**What "the nearest size" is.** The drawn pose depends on the size only through the whole multiplier
both tooth counts come from — `k` at `engine/assets/pass-inst-gears.js:457`, with `n1`, `n2`, `R1`
and `R2` following from it — so every size inside one step of that multiplier draws one and the same
door. The search steps over multipliers, not over sizes, and the applied size is the size the chosen
multiplier stands at. U12's own rig stepped in hundredths of a size and confirmed each candidate with
a full-frame read; stepping in rungs reaches the same set of distinct doors and reads each of them
once.

**How far "near" reaches: two rungs.** Two written requirements bound it from opposite sides. The
hold has to close the doors the buffers actually leak — on the 780 × 1688 buffer 76.4% of the 632
leaking instants stand one rung from a whole door and 98.6% within two. And U11's refusal has to
stand: the door its guard refuses, the pose the composer's record measured at a size of 1.473, has
its nearest whole size three rungs away (1.213, which is the size the composer's own table hands
instead). A reach of three would draw where U11 refuses, so two rungs is the widest reach that
satisfies both, and it is what the file carries as `DOOR_HOLD` at line 360.

**Which side is tried first.** The smaller size, then the larger, at each distance — the order U12's
own closing search runs in (`lab/sweep-mesh-doors-frames.js`, `closeAll`).

## 2 — the mechanism, with file and line

**The host names the buffer.** `engine/assets/pass-layer.js:1903` — the frame state's `viewport` now
carries `bufferW`/`bufferH` beside the CSS `w`/`h`, and they are the same two numbers the host binds
as the `resolution` uniform source at line 327. The contract records it in
`docs/design/PASS-API-V1.md:1070`, §7, dated 2026-08-16. This is the host contract U11's own
limitation named as a unit of its own.

**The instrument reads there.** `pass-inst-gears.js:716` carries the buffer into the pose;
`doorGridOf` at line 396 answers with the buffer where one is handed and the CSS frame where none
is — a bench pose carries none — and says which of the two it read, so the refusal names a buffer or
a frame truthfully. `doorWhyNoOf` at line 402 reads on that grid: the sample positions are the
buffer's, the anti-aliasing width is the shader's own `2 / uRes.y`, and the aspect the samples are
mapped through is the buffer's own, which is exactly what the shader computes from `uRes`.

**The hold.** `values` at line 524. It asks `posed` (line 437, the old `values` body with the size as
a parameter) for the pose at the size handed in, reads its door, and returns at once where nothing
leaks — which is every pose away from a door, since `doorWhyNoOf` reads nothing there. Where the door
leaks, the loop at line 531 steps outward over the whole multiplier, one rung under and one rung
over, then two, skipping a candidate whose counts are the ones already refused and any size outside
the handle's own 0.3 to 8, and answers with the first pose whose door is whole on that same buffer.

**What stays on the record.** The pose surface carries `size` — the size drawn — beside
`sizeRequest`, the size handed in; `sizeRungs`, how many rungs apart they stand and in which
direction; and `doorHeld`, the leak the request would have drawn, in the refusal's own words. Where
nothing within reach is whole, `doorWhyNo` carries U11's sentence with a clause naming the reach, the
host lands the transaction on it, and the walk's own glide carries the visitor. The manifest
publishes the move where a composer reads it, at line 600: `heldWholeAtADoor` beside the size
handle's own range, naming the reach, the grid and the field the request is kept in.

**Why the move costs the picture nothing where it is made.** A door is one whole work by the very law
being kept, so no tooth of either wheel is on screen at that instant to show which multiplier drew
it. The size the score asked for is untouched everywhere else in the pass; what moves is where the
mesh line starts its ramp on the frame after the door.

## 3 — what one door instant costs

Measured in the browser the suite runs, on this machine, over 2 000 calls of the same pure function
the drawing road calls (`PASS-GEARS the door is read on the buffer the shader draws on`):

| the door instant | ms |
|---|---|
| leaks, and is held (the reading, then two candidate poses read) | **0.0060** |
| whole, both wheel centres off the buffer — nothing to read | 0.0010 |
| away from a door — no reading at all | 0.0012 |

The two cases the browser row does not stand at, measured in Node against the same shipped file: a
whole door with a wheel centre inside the buffer, which is the full 98-point reading finding nothing,
costs **0.0041 ms**, and a door where nothing within reach is whole — the reading plus four candidate
poses, ending in the refusal — costs **0.0223 ms**. The frame budget is 16.7 ms at 60 a second, and a
pass reads its doors twice.

## 4 — what the hold closes, over the composer's own 3 992 door instants

Every door instant of `lab/data/mesh-doors-request.json` at the size
`lab/data/mesh-doors.json` holds for it, geometry on the 390 × 844 CSS frame and the door read on the
buffer named, at the seed the composer serialises:

| buffer | ladder step | leaking | worst | held whole | one rung / two | still refused | size move, median / max |
|---|---|---|---|---|---|---|---|
| 780 × 1688 | 1.00 | 632 | 0.457750 | **623** | 483 / 140 | 9 | 0.151 / 0.555 |
| 663 × 1435 | 0.85 | 645 | 0.496265 | **560** | 442 / 118 | 85 | 0.169 / 0.647 |
| 562 × 1215 | 0.72 | 649 | 0.494285 | **590** | 505 / 85 | 59 | 0.169 / 0.921 |
| 468 × 1013 | 0.60 | 597 | 0.491809 | **542** | 439 / 103 | 55 | 0.158 / 0.921 |
| 390 × 844 | 0.50 | 0 | 0 | 0 | — | 0 | — |

The 780 × 1688 row reproduces U12 §3 exactly — 632 leaking instants, worst 0.457750 — which is the
check that the reading moved onto the right grid rather than onto some other one. The three middle
buffers differ from U12's own counts because U12 read each buffer as if it were the CSS frame, so its
geometry came from the buffer's aspect; here the geometry comes from the CSS frame and only the
reading is on the buffer, which is what the host actually does.

The same sweep at the seed the host binds today, which is 0 for every pass it drives (U11's parked
note, still standing): 635 leaking and 9 refused on 780 × 1688, 656 and 86 on 663 × 1435, 648 and 59
on 562 × 1215, 610 and 58 on 468 × 1013, and on 390 × 844 — whole at the composer's own seeds — 25
leaking, 24 held and **1 refused**. That one is the door the real transaction road meets U11's
refusal on, and the row of §6 stands on it.

**The size the composition pays.** A median move of 0.151 to 0.169 against the size handle's range of
0.3 to 8, which is the discipline the composer's own table already keeps on its one frame (0.140).
The 2 158-instant frame-independent table U12 costed moves a median of 1.590 and needs 837 floor
requests to arrive five times larger; this costs a tenth of that and needs no table at all.

**What it does not close.** Between 9 and 85 door instants per buffer stand with no whole size within
two rungs, and there the pass is refused and the walk's own glide carries the visitor, which is the
ruling's own answer for that case. §8 states the fork.

## 5 — the ladder step: the buffer moved between a pass's two doors

The row `PASS-GEARS the buffer moves between a pass's two doors and the exit door still holds`,
`tests/test_pass_gears.py:1098`, on the real transaction road. The pose is the composer's own
18061740532199044__18083437520477697__ab, whose two doors are both whole on the buffer the pass
starts at and whose exit door leaks on every one of the four lower steps of the host's ladder.

    the entry door drew on 390x844 at scale 1 (state running, 1 cue)
    the exit door  drew on 281x608 at scale 0.72 (state running, 1 cue)
    the exit size the composer serialised, read on the entry door's own buffer → nothing said
    the same size read on the buffer the exit door was drawn on →
      «the exit door leaks: at a size of 0.7 this instrument's own mask draws an alpha of
       0.701753 on 5 points of a 281 x 608 buffer, where the exit door's own law asks for 1
       at every point»
    where it moves 1 rung down to 0.636556 and keeps the request at 0.7
    refused on the road: nothing

The step is moved by the host's own governor, not by a test seam: the row hands the resolution
governor the frame times of a slow device through `bench.ladder`, and the governor walks its own
ladder down. The grid the exit door was drawn on therefore did not exist when the entry door was
drawn, and no serialised table could have been solved for it.

## 6 — the red-on-bug proofs

**One — the buffer a phone actually draws.** `PASS-GEARS the buffer the phone actually draws: the
leaking door is held and the pass plays`, `tests/test_pass_gears.py:1050`. The frame is taken to
780 × 1688 and the pass whose exit door leaks worst on that buffer is offered to the host: nothing
refused, one cue drawn, the picture standing against the arriving work's own file at a mean of 0.0928
of 255 against the project's seam of 6, and the instrument's own record reading «the exit door leaks:
at a size of 0.7 … an alpha of 0.542909 on 2 points of a 780 x 1688 buffer» and moving one rung down
to 0.371324 with the request kept at 0.7.

**Two — what it reddens on.** Both switch-offs were made on a copy of the file taken first and
restored from that copy afterwards, and the gears suite was run whole each time.

*The hold switched off* — the search loop's own bound alone, everything else standing: **36 passed /
3 failed**, and the three failing rows are the three this unit added. The 780 × 1688 row then reads
`refused ["recovered: the exit door leaks … an alpha of 0.542909 on 2 points of a 780 x 1688 buffer …
and no whole size stands within 2 rungs of the mesh"]` and the picture lands **146.7084 of 255** from
the arriving work, because the pass was refused and the visitor got the walk instead. The ladder row
reddens the same way with its own alpha of 0.701753 on 281 × 608.

*The reading put back on the CSS frame* — one condition inside `doorGridOf`: **36 passed / 3 failed**,
the same three rows. The instrument then says nothing on any buffer, holds nothing, and the door that
draws 0.542909 where the law asks for 1 is drawn as two works — while the picture measure stays green
at a mean of 0.0928, which is precisely why the instrument's own reading is the row that catches it:
two wrong points of 1 316 640 do not move a mean.

**Three — U11's refusal still stands.** `PASS-GEARS a door the instrument cannot keep whole is
refused, with the alpha it measured` stayed green through this unit and through both switch-offs. At
the pose the composer's record names, at the size it asked for, the instrument still says «the entry
door leaks: at a size of 1.473 … an alpha of 0.153454 on 1 point of a 390 x 844 frame … and no whole
size stands within 2 rungs of the mesh», and stays silent at the whole size the composer hands, at
the pose's own exit door, away from either door, and at this suite's own two doors.

**The row's road half moved to another pose of the same record, and the reason is worth recording.**
The host binds `uSeed` at 0 in every pass it drives — U11 parked that defect and it still stands —
and the door reading takes its seed from the same pose, so both the reading and the drawing on the
road stand at seed 0. At that seed a whole size stands one rung from 1.473, so the road now holds
that door instead of refusing it. Of the composer's own 3 992 door instants exactly one is refused on
the road at that seed — the exit door of 17994945094661841__18023729152236427__ba at the size 0.84
the table holds — and the row is stated against it: the host lands the transaction on «recovered: the
exit door leaks … an alpha of 0.999436 on 1 point of a 390 x 844 buffer … and no whole size stands
within 2 rungs of the mesh», state idle, while the whole size draws its one cue and keeps running.

## 7 — the runs, the fences

**The gears suite: `python3 tests/test_pass_gears.py` — 39 of 39 green**, 50 s, no skip. Three rows
are new and one string row was restated for the manifest's new publication.

**The coverage suite: `python3 tests/test_pass_coverage.py` — 18 of 18 green.** The pack suite: 24 of
24. The budget suite: 9 of 9.

**The full engine prover: `python3 tests/run_all.py` — 56 of 56 suites green, wall 255 s**, no red
and no skip. The log is
`/Users/sashaabramovich/exhibition-engine-doorhold/docs/design/evidence/2026-08-16-runtime-door-hold-prover.log`.
The one-minute load stood at **5.21 before the run and 12.59 after it** on a ten-core machine, inside
the quiet rule this seat set, and the wall stands beside U11's 254 s and U13's 265 s.

**The byte fences.** Both moved by the rule the file states — its own measurement plus about a tenth
— with a dated note beside each. U11 had already moved both on 2026-08-15, and these numbers are
against U11's, not against the older ones the brief carried.

| the fence | U11's | now | the file |
|---|---|---|---|
| the built file, raw | 18 300 B, measured 16 592 B | **20 000 B, measured 18 190 B** | `tests/test_pass_pack.py` |
| the shipped bytes, gzipped | 6 100 B, measured 5 551 B | **6 600 B, measured 6 026 B** | `tests/test_budget.py` |

What a visit pays for the whole instrument is **6 026 gzipped bytes**, 475 more than before, and only
a visit whose own score names this instrument pays them.

## 8 — the fork this leaves for the delivery seat

The reach of two rungs is the widest that keeps U11's refusal standing, and it leaves 9 to 85 door
instants per buffer refused rather than held. Two ways forward, and the numbers each would be taken
on:

**Leave it.** The refused instants land on the walk's own glide, which is the product's behaviour
with no renderer and is what the visitor already gets when a device declines the picture. The cost is
between 0.2% and 2.1% of door instants per buffer, and it falls hardest on the lower ladder steps,
which is to say on the slower devices.

**Widen the reach and restate U11's row.** Three rungs closes 97 to 99% of what the four buffers leak
and would draw the door U11's guard refuses, so the row that proves the guard would have to be stated
against a pose no size makes whole at all — of which the composer's record holds none, so the row
would have to be stated against a pose of its own making rather than against the record. That is a
real loss of anchoring and is why it was not taken here.

Either way the composition's own answer — what the composer's table should hold, and whether it grows
a column at all — is untouched by this unit: nothing was written into any table, and the instrument
now keeps its doors whole whatever the table holds.

## Conclusion

The door law this instrument publishes is now kept on the grid the law is actually decided on. The
reading moved from the CSS frame onto the drawing buffer the host binds, which costs one reading of
at most 98 points per door instant and 0.006 ms when it has to act; a door whose serialised size
leaks there is moved to the nearest size whose door is whole, within two rungs of the mesh, with the
composer's request and the leak it would have drawn both kept on the instrument's record; and where
nothing within two rungs is whole, U11's refusal stands unchanged. Across the composer's own 3 992
door instants this closes 623 of the 632 leaking on the buffer a phone draws at full quality, at a
median size move of 0.151 — a tenth of what the frame-independent table U12 costed, and without a
table at all. The gears suite stands at 39 of 39 and the full prover at 56 of 56.

## Limitations, and what was set aside

**Between 9 and 85 door instants per buffer are refused rather than held**, because no size within
two rungs makes them whole. Before this unit those doors were drawn leaking, since the CSS frame read
them whole; now the pass lands on the walk's own glide instead. That is the ruling's own answer for
the case, and the fork of §8 is where it can be revisited.

**The reach cannot be widened without restating U11's row.** Three rungs would close more doors and
would also draw the door U11's guard refuses, so the two cannot both be had as they stand. Which of
them the product wants is the delivery seat's call, and the numbers for it are in §4: a rung is worth
roughly 0.1 of the size handle.

**The hold can land below the composer's own floor.** The size handle's published range is 0.3 to 8
and the hold stays inside it, but the composer's own range starts at 0.7 — the worst case measured
here applies 0.371324 against a request of 0.7. At the door itself the frame is one whole work, so
nothing of the pair is on screen to show it; the frame after the door is drawn from the score's own
size again.

**The geometry is still solved on the CSS frame.** `values` derives the aspect, the placement and the
wheel centres from `cssWidth`/`cssHeight`, while the shader's own `uAspect` comes from the buffer.
The two agree to the rounding of the buffer's dimensions and this unit did not touch it, since moving
the geometry onto the buffer would move every drawn frame rather than the doors alone.

**PARKED — the `seed` handle still never reaches this instrument's shader**, so every pass the host
drives draws and reads at seed 0 whatever its score says. U11 parked it; it is what moved this unit's
road-side refusal onto another pose of the same record (§6), and the numbers of §4 are given at both
seeds because of it.

**The reading is double precision on the CPU; the shader is highp float on the GPU.** U11's note
stands unchanged: the two agreed to six decimals across every pose measured, and they are not the
same arithmetic. A hold decided on the CPU reading is a hold on that reading.

**Device pixel ratios above 2 are not measured**, because the host caps the ratio at 2. The buffers
of §4 are the five a 390 × 844 CSS frame reaches at that cap; a wider CSS frame reaches other buffers
and each is one more line of the same sweep.

**Nothing was measured about how the moved size reads to the eye**, because at a door there is
nothing of the pair on screen. Whether the ramp starting from a size one rung away is visible on the
frames just after a door is a taste question and was not taken here.
