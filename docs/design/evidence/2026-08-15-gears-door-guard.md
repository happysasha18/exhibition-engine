# U11 — the meshing instrument refuses a leaking door itself

Run 2026-08-15, 22:04–22:40 local. The composer stopped handing this instrument a size whose door
leaks on 2026-08-14; the instrument still accepted one, so the door law lived on one side of the
wire only. It now lives on both. The instrument reads its own mask at its own doors and refuses a
pose whose door is two works at once, naming the alpha it measured.

## The trees

Engine: `/Users/sashaabramovich/exhibition-engine-doorguard`, a worktree of
`/Users/sashaabramovich/exhibition-engine-pass-api-v1`, branch `pass-api-v1-doorguard`, from
`pass-api-v1` at `bad44a6`:

    9263afb  The meshing instrument reads its own doors and refuses a pose whose door leaks
    6fd0375  The gears suite proves the door refusal, red on the bug the composer's record measured
    HEAD     this record

Nothing was merged, pushed or deployed. The site tree `/Users/sashaabramovich/tlvphotos-immersive`
was read and never written: the composer's record `lab/data/mesh-doors.json`, its request file and
the U4 evidence are the sources this unit measures itself against.

## 1 — what the instrument now refuses, and in what words

The check is `doorWhyNoOf` at `engine/assets/pass-inst-gears.js:356`. It reads the shader's own
`cov`, carried across from that file's own FRAG line for line as `covAt` at line 327, and it is
reached from two places: `values` publishes its answer on the pose surface at line 461, bound to no
uniform, and `frame` refuses to draw on it at lines 625–626, handing the host the reason through
`st.fail` instead. The host lands the transaction on that reason and the walk's own glide carries
the visitor, which is the product's own behaviour with no renderer.

A refusal reads the way the host's own manifest refusals read — what is wrong, in measured numbers,
on the frame it was measured on. The wording, at the entry door and at the exit door:

    the entry door leaks: at a size of 1.473 this instrument's own mask draws an alpha of
    0.153454 on 1 point of a 390 x 844 frame, where the entry door's own law asks for 0 at
    every point

    the exit door leaks: at a size of S this instrument's own mask draws an alpha of A on N
    points of a W x H frame, where the exit door's own law asks for 1 at every point

The alpha named is the alpha that door DRAWS at its worst point, which is why the entry door's
number falls from 1 and the exit door's rises from 0.

## 2 — where it looks, and why the centre alone is not the refusal

`reachFor` places the wheel pair on the reading that the field's extremes over the frame stand at
the frame's four corners. That reading holds while both wheel centres stand off the frame. Inside
it the field's gradient goes to infinity at a centre, `cov` falls off 1 within about a pixel of it,
and one point of the wrong work stands in a door. So the centres are where a leak can stand, and
the check reads the pixels within three of either centre — `DOOR_READ` at line 323 — clipped to the
frame, which costs at most 98 mask readings and measures 0.5 ms at the worst pose read here. Away
from a door it reads nothing at all: a mixture of the two works is the picture there rather than a
fault.

**The centre-inside-frame condition is not itself the refusal, because it over-refuses.** Two door
poses this engine's own suites drive stand a wheel centre inside the frame and leak nothing:

| the pose | the centre inside the frame | what the mask reads |
|---|---|---|
| `test_pass_stack.py`'s exit door at size 0.7 | wheel A at x −0.150 of a half-width of 0.462 | alpha 0 on 0 points |
| `test_pass_gears.py`'s door row at size 2 on the 1:4 rung | wheel A at x 0.286 | alpha 0 on 0 points |

Whether the leak stands depends on whether a tooth's own flank is live at that point, which only
the mask answers. Refusing on the centre alone would have reddened both suites and refused two
poses that draw a whole work.

## 3 — the reading is the same reading the whole frame gives

The composer's record answers 1996 poses by sweeping every one of the 329 160 points of a 390 × 844
frame. The instrument reads 98 of them. Over **2 759 poses taken from that record — all 759 leaking
ones and 2 000 whole ones — the two readings never disagreed**: the same poses refused, the same
point counts, and the same alpha to six decimals, which is also the number the record itself
publishes. The furthest a leaking point ever stood from its own centre was **1.56 px**, and the
radius read carries about twice that.

## 4 — the red-on-bug proof

The row is `PASS-GEARS a door the instrument cannot keep whole is refused, with the alpha it
measured`, `tests/test_pass_gears.py:286`. It is stated against the composer's own pose rather than
this suite's: pair `17843080526947498__17894700938773432__ab`, pose key
`0.166667|0.833300|0.350000|0.475000|1.269800|1.473000|4.500000`, which the U4 record names in its
own red-on-bug row and measures at an alpha of 0.153454 on one point of its entry door.

The row asks five things at once, and every one of them held:

    the pose the record names, at the size it asked for → «the entry door leaks: at a size of
      1.473 this instrument's own mask draws an alpha of 0.153454 on 1 point of a 390 x 844
      frame, where the entry door's own law asks for 0 at every point»
    the whole size the composer hands instead (1.213), at the same entry door → nothing said
    the same pose's own exit door (4.5)                                      → nothing said
    the leaking size itself, away from either door                           → nothing said
    this suite's own entry door and its own exit door                        → nothing said
    on the real transaction road: the leaking ramp is refused with the reason and the host
      lands the transaction on it, while the whole size draws its one cue and keeps running

**What it reddens on.** With the door reading switched off — one line inside `doorWhyNoOf`, the
instrument back to accepting any pose at its doors, the file set aside as a copy first and restored
from that copy afterwards — the suite came back **34 passed / 1 failed**, and the failing row was
this one alone. Its report then read `«None»` where the alpha stands and `nothing refused` where
the host's own refusal stands.

**The row that already existed cannot see this defect, and that is why this one is needed.** `both
doors stand whole at every size the travel passes through` stayed green through the whole red run.
It reads the mask's mean and spread over the frame, and one point at an alpha of 0.15 moves the
mean of 329 160 points by 0.0000005 against a bar of 0.005.

**One number in the row is not 0.153454, and the reason is worth recording.** On the real
transaction road the refusal reads an alpha of 0.171665 — the same pose and the same size, read at
seed 0. The instrument does not echo its `seed` handle into the pose it hands the host, so `uSeed`
binds 0 there; see the parked item below. The check reads the seed from the pose exactly where the
host binds the uniform from, so the reading and the drawing cannot see two seeds whichever way that
is settled.

## 5 — the runs

**The gears suite: `python3 tests/test_pass_gears.py` — 35 of 35 green**, 43 s, no skip.

**The full engine prover: `python3 tests/run_all.py` — 56 of 56 suites green, wall 254 s**, no red
and no skip. The log is `docs/design/evidence/2026-08-15-gears-door-guard-prover.log`. The
one-minute load stood at **5.52 before the run and 13.74 after it** on a ten-core machine, inside
the quiet rule this seat set, and the wall matches the 255 s the run at `bad44a6` took.

## 6 — the byte fences

The instrument grew by the mask it now reads and the sentence it says. Both of its fences moved by
the rule each file states — its own measurement plus about a tenth — with a dated note beside each.

| the fence | before | now | the file |
|---|---|---|---|
| the built file, raw | 14 800 B, measured 13 472 B | **18 300 B, measured 16 592 B** | `tests/test_pass_pack.py` |
| the shipped bytes, gzipped | 5 000 B, measured 4 532 B | **6 100 B, measured 5 551 B** | `tests/test_budget.py` |

What a visit pays is **1 019 gzipped bytes**, and only a visit whose own score names this
instrument pays them: the file is fetched by name, after the host, and never at all under reduced
motion, Save-Data, no WebGL2 or the layer switched off.

## Conclusion

The door law this instrument's manifest publishes is now true by the instrument's own reading. It
refuses the pose the composer's record measured, with that record's own number in the reason,
without moving any pose the composer now hands or any pose this engine's own suites drive: the
gears suite stands at 35 of 35 and the full prover at 56 of 56. The measurement U4 handed over is
closed on the engine side, and the composer's guard is now a second line rather than the only one.

## Limitations, and what was set aside

**The door is read on the frame the pose carries, not on the buffer the shader draws into.** The
check reads `cssWidth` and `cssHeight` — the CSS frame the host hands the instrument — while the
shader's own `h` comes from `uRes`, the drawing buffer after the device ratio and the resolution
ladder. On a finer grid the field crosses over inside a smaller pixel, so a door whole here is not
thereby whole on every buffer. Reading the buffer would need the instrument to be told its size,
which is the host's own contract and a unit of its own.

**One frame, one aspect.** The placement `reachFor` solves depends on the aspect, and so does where
a centre lands. The refusal names the frame it read, and sweeping the frames a visitor can hold
remains the unit U4's own record already asked for.

**The reading is double precision on the CPU; the shader is highp float on the GPU.** The two
agreed to six decimals across every pose measured here and across the two rigs U4 ran, and they are
not the same arithmetic.

**PARKED — the `seed` handle never reaches this instrument's own shader.** `pass-inst-gears.js`
does not carry `seed` into the pose it hands `st.draw`, so the host resolves `handle:seed` to
nothing and binds `uSeed` at 0 in every pass it drives. The three sibling instruments — weave,
matter and adrift — all echo it. Repairing it changes what every meshing pass draws, which is
outside what this unit was asked to change, so it is named here for a unit of its own.

**PARKED — the instrument refuses rather than repairs.** It could move to the nearest size whose
door it keeps whole, the way the composer does. Which of the two the product wants at the
instrument's own doors is a taste call and was not taken here.

**`reachFor` itself is untouched.** It still solves the placement on the four-corner reading; what
is new is that the instrument no longer trusts that reading blindly at its own doors.

**`tests/test_pass_stack.py` still carries the stale frozen copy** of the worked passage that U4's
record hands to U4b. This unit read it and wrote nothing about it.
