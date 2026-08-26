# U22 — the visitor's place survives Back and Forward

Run 2026-08-17 from 17:10 to 17:37 local in the engine worktree
`/Users/sashaabramovich/exhibition-engine-placefix` on branch `pass-api-v1-placefix`, cut from the
integration head `3665da0`. Nothing outside that worktree was written; nothing was merged, pushed or
deployed, and no git command restored anything.

Root: U19's recorded defect
(`tlvphotos-immersive/docs/immersive/evidence/2026-08-17-sound-share-history.md` §5, accepted by the
delivery seat 08-17 16:14). U19 measured, on `/immersive/` at 390×844: the place marker names
`17984585281991307` while the visitor walks, names `17961191066787693` once the Back road has
rendered the door, and the walk restores at that work with `scrollY 0` after Forward.

## 1. The cause, measured before anything was repaired

The defect lives in the client both roads share, so it was reproduced on the ROOT road — `/` with
the visual layer off, the synthetic fixture `tests/engine_build.py` builds, at 390×844. The probe
walked to the fourth frame, pressed the browser's Back, and pressed Forward.

```
in the walk       {"at_door": false, "place": {"v":"2a63192e","id":"synth-24"}, "scrollY": 2532, "in_view": "synth-24"}
the door stands   {"at_door": true,  "place": {"v":"2a63192e","id":"synth-05"}, "scrollY": 0,    "in_view": "synth-05"}
after forward     {"at_door": false, "place": {"v":"2a63192e","id":"synth-05"}, "scrollY": 0,    "in_view": "synth-05"}
```

U19's reading, on V1's own road, work for work. `synth-05` is the walk's FIRST frame.

The same probe read the exit control's road beside it, and that reading is what named the second
half of the cause:

```
in the walk               place synth-13   scrollY 2532
exit control · the door   place synth-02   scrollY 0
exit control · Back       place synth-02   scrollY 8440 (the closing screen — the exit was pressed from there)
```

**The marker is rewritten on BOTH roads**, and the scroll place survives on one of them. So the one
recorded defect has two limbs, and each has its own cause.

### Limb one — the marker is rewritten while the door stands over the walk

`engine/client/08-plaque-caption-io.js:58` wrote the per-tab place marker for every work the in-view
watcher reported, with no reading of which surface the visitor stands on. Every render of the door
rests the door at its own top (`07-door-face-ceremony.js:457` and `:513`, `scrollTo(0, 0)`), and the
walk's tall document is still there underneath — so the walk's first frames cross the watcher's
threshold under a scroll the HOUSE wrote, `landOn` runs for them, and the marker names the walk's
first work. The place the visitor left is gone before any return can restore it.

The same function already reads the standing surface twice for the same reason: the picture ladder
at `:52` (`if (!busy && !atDoor)`) and the live accent at `:60` (`if (!atDoor) ground(w.dom)`, «a
late callback must never re-live the tone ON the door»). The marker was the one product effect in
`landOn` that ran unconditioned.

### Limb two — the browser's Back road onto the door remembers no place

`doorReturn` (`07-door-face-ceremony.js:439`), the exit control's own road, measures the walk's
nearest centered stop into `walkY` before it rests the door at its top (`:449-450`). The popstate
road that renders the door (`:461` onward) rendered, scrolled to zero and returned, and never took
that reading. `walkY` therefore stood at its initial `0`, and the Forward step that returns to the
walk — `scrollTo(0, walkY)` at `:527` — put the visitor at the top of the walk.

The two roads are the same leave under the spec's own sentence:

> Every way the door face can render counts as that render — the exit control, the browser's own
> Back landing on the door, and a reload landing on the returned-to door behave alike
> (`SPEC.md:258-262`)

> `walk_exit` | the walk leaves for the door — the exit control OR the browser's own Back, ONCE per
> leave (a Back-exit counts no less than a button-exit) (`SPEC.md:1455`)

The pulse and the exit count were already ported to the Back road (`:494`). The place reading was
left behind.

## 2. The design judgment, and the law it stands on

The brief named two candidate shapes: a guard on the watcher while the door stands, and a marker
written from the walk's own state rather than from view reports. **The guard is the lawful one**,
and three sentences decide it.

**The engine already freezes the walk's place when a face rises, and the marker is that place.**
`faceSync` (`engine/client/15-motion.js:252-258`) reads `faceStands()` and, on the rise from no face
to a face, writes `guardHold = scrollY` — «a face rose — remember the place beneath». The snap-back
guard then holds the walk there for the length of the stand. `SPEC.md:1220-1227` is the law behind
it: «While a face stands over the walk — the re-opened door, the side room, a question card, the
gift card — the page beneath stays the walk's own tall document, holding its scroll place.» The walk
holds its scroll place beneath a standing face; its place MARKER holds by the same sentence. The
guard makes the two records agree, and it uses the predicate the engine already owns.

**`landOn` is the one owner of «this work is now current».** Its own header says so
(`08-plaque-caption-io.js:30-33`), and `ARCHITECTURE.md:36` puts INV-13 and INV-18 in the door and
gallery-walk component the function belongs to. A marker written from a second reader of the walk's
state would make a second owner of one fact, and the two would drift the first time a beat fell
between them. The guard keeps one owner and teaches it when to speak.

**U13's own repair 1b is this shape.** `08-plaque-caption-io.js:111`, landed 08-16: while a renderer
holds the command, «every other section, for the length of the flight, is the stale offset speaking
and is now left alone». The stale offset speaking while the door rests at its top is the same kind of
report, and it earns the same answer.

The predicate is `faceStands()` whole — `atDoor || busy || sideOpen || quizOpen || giftOpen ||
zoomOpen` — rather than `atDoor` alone. The door is the face that scrolls the document beneath it
today, and the class the law names is every standing face; `placeCaption`, seven lines below in the
same file, already guards on exactly this predicate (`:181`, «the walk's own frame only»). The pass
layer's crossings are outside the predicate, so a composed crossing still lands and still reports —
U19's own share-follows-the-eye row depends on that and stays green.

**The guard costs one write, and that write is put back where it belongs.** The whole door ceremony
runs under `busy`, so the picked work's first report is held with the rest. Measured: after a fresh
pick the marker read `null` where it had named the picked work. The visible outcome was unchanged
(the pick is the walk's first frame, so a return with no marker lands on it anyway), and a walk that
has forgotten where it stands still breaks INV-32c's own sentence — «the walk owns a per-tab place
memory». So the ceremony writes the place at its hand-over, the same explicit write the `#w-`
hand-over already makes at its jump (`17-place-hash-boot.js:51`, «the consuming jump writes the place
marker so the room's memory agrees with the eye»).

## 3. The three repairs

| # | file and line | what it now does |
|---|---|---|
| 1 | `engine/client/08-plaque-caption-io.js:64`, inside `landOn` | the in-view report writes the place marker only while the walk is the standing surface (`if (!faceStands())`) |
| 2 | `engine/client/07-door-face-ceremony.js:500-510`, inside the `popstate` door branch | a Back-leave from the walk measures the walk's nearest centered stop into `walkY`, inside the `wasWalk` block that already pulses `walk_exit` and counts the exit |
| 3 | `engine/client/07-door-face-ceremony.js:422`, inside the ceremony's `capBeat` | the hand-over writes the place marker for the picked work at the moment the walk is bare |

`engine/assets/exhibition.js` is regenerated from the fragments by `engine/assemble_client.py`;
`tests/test_assembly.py` proves the reproduction byte for byte (5 of 5 green).

## 4. What the repaired road does

The same probe, after the repair, on the same root road at 390×844:

```
in the walk       place synth-13   scrollY 2532   in view synth-13
the door stands   place synth-13   scrollY 0      (the door rests at its top, the walk holds beneath)
after forward     place synth-13   scrollY 2532   in view synth-13
```

Three further readings taken in the same drive:

| the sequence | what the road did |
|---|---|
| the exit control's road: walk, exit, Back | the marker holds at the work the visitor left through the door's whole stand |
| the door reloaded while it holds (INV-19), then Forward | the walk returns to `synth-13` at `scrollY 2532` — the durable marker carries the place across a page lifetime the `walkY` variable does not survive |
| the walk reloaded after the whole round trip | `synth-13` again — INV-32c's own road |

## 5. The red-on-bug proofs

Each repair was crippled ALONE — the fragment copied aside, the line put back to what it was, the
client re-assembled, `tests/test_back.py` run, the fragment restored from the copy. Each anchor was
held to the same rule: present exactly once, replaced once, and a missing anchor stops the proof.
No git command restored anything.

| the defect planted | the row that failed | what the crippled run said |
|---|---|---|
| the watcher writes the marker while a face stands | INV-32(b/c) browser Back to the door holds the place | `place_holds=False` — the marker was rewritten under the standing door |
| the Back road onto the door forgets the walk's place | INV-32(b/c) browser Back to the door holds the place | `lands_on=synth-02 want=synth-13 scrollY=0 want=2700` — U19 §5's reading, work for work |
| the ceremony's hand-over writes no place | INV-32(c) the hand-over writes the walk's place at the pick | `marker=None picked=synth-05` |

The readings above are the suite's own, taken at its 1280×900 window, where the fourth frame's
centered stop is `scrollY 2700`; the probe readings of §1 and §4 are at 390×844, where the same stop
is `2532`. Both windows are the root road.

**3 of 3 rows failed when the thing they watch was broken**, and each defect took down exactly one
row. The first two are separate limbs of one row, and the readings show they are independent: with
the watcher guard alone removed the row still landed on the right work at the right scroll and failed
only on the held marker; with the place reading alone removed the marker held and the landing failed.

Two rows were added to `tests/test_back.py`, the suite INV-32 already lives in:

- `INV-32(b/c) browser Back to the door holds the place; Forward lands on the work left, at its own
  scroll place`
- `INV-32(c) the hand-over writes the walk's place at the pick, before the visitor moves a frame`

The suite now carries nine rows, up from seven.

## 6. The runs

Taken under the quiet rule this seat keeps: ten cores, a full run taken while the one-minute load
stands at twenty or under, with the reading recorded on both sides.

| run | result | wall | load before → after | log |
|---|---|---|---|---|
| `python3 tests/test_assembly.py` — the fragment split's own net | 5 of 5 | 0.2 s | — | — |
| `python3 tests/test_back.py` — the suite INV-32 lives in, with both new rows | **9 of 9** | 47.8 s | — | — |
| `python3 tests/test_budget.py` — the byte fences | 9 of 9 | 0.2 s | — | — |
| `python3 tests/run_all.py` — the full engine prover | **56 of 56 suites green** | **315 s** | **8.17 → 34.47** | `docs/design/evidence/2026-08-17-place-across-history-prover.log` |

The three suite walls are the full run's own recorded durations (`tests/suite_timings.json`), taken
under eight suites in parallel; run alone each takes longer. The full run was started at 17:23:21 with
the one-minute load at 8.17 and ended at 17:28:36; the closing reading of 34.47 is the run's own heat
still decaying at the moment it finished. No suite reddened, so no rerun was needed and no reading had
to be judged against the machine. The wall sits beside U13's 265 s over the same 56 suites, and the
whole gap is the machine rather than this diff — the suites this unit touched cost 48 s of it.

Two readings inside the log carry this unit's own rows: `[OK ] back: 9 rows: 9 pass, 0 fail, 0 skip`
and `[OK ] assembly: 5 rows: 5 pass, 0 fail, 0 skip`.

## 7. The root road, and V1's own behaviour

V1's own road is `/` with the visual layer off — the road every engine suite drives, and the road
every measurement above was taken on. Three readings hold it:

1. **The six INV-32 rows that stood before this unit still stand**, unedited, in the same suite:
   (a) the door as it stood, (b) the re-opened door's Back, (c) the place across a reload, (d) the
   superseded arc, (e) «ещё 5» lays no step, (f) the work page's plain link. All six green in every
   run above, including the three crippled ones.
2. **The full engine prover** drives the root road across every suite it carries — the door, the
   memory, the reset, the glide, the motion, the compose and the pass suites among them — and it came
   back **56 of 56 suites green** with the two new rows counted. Every suite that reads the door, the
   history road or the walk's own place stands green: `door: 42 passed`, `memory`, `reset`, `return`,
   `exhibition: 16 passed`, `compose`, `pass: 28 passed`.
3. **The diff's own reach is three edits.** One conditional around one `sessionStorage` write inside
   `landOn`; two lines inside the `wasWalk` block of the `popstate` door branch, a branch that runs
   only when the browser's Back or Forward lands on a door step; one `sessionStorage` write at the
   end of the door ceremony. Nothing in the rendering, the layout, the timing, the ladder or the
   input roads is touched, and no code path that runs while the walk stands bare and no history step
   is travelled changes at all.

## 8. The byte fences

Only one shipped file changed, and it is the bundle.

| file | gzipped as shipped | fence | before (`3665da0`) |
|---|---|---|---|
| `engine/assets/exhibition.js` | **69 623 B** | 70 000 B | 69 614 B |
| `engine/assets/exhibition.css` | 7 743 B | 9 000 B | unchanged |
| `engine/assets/pass-layer.js` | 23 341 B | 24 000 B | unchanged |
| `engine/assets/pass-reader.js` | 3 522 B | 4 000 B | unchanged |
| the four instrument files | 5 444 / 6 026 / 3 279 / 4 167 B | 6 000 / 6 600 / 3 550 / 4 500 B | unchanged |

The three repairs and their comments cost the bundle **9 gzipped bytes**, and 377 B of the fence
remain under it.

## 9. Conclusion

A visitor who walks to a work, presses the browser's Back to the door and presses Forward comes back
to that work, at the scroll place they left it at. The per-tab place marker holds for the length of
any standing face rather than following the covered document's own frames past the eye, so the same
place also survives a reload taken while the door holds. The exit control and the browser's Back now
remember the walk alike, which is the sentence the spec already carried for the pulse and the exit
count.

## 10. Limitations, and what is parked

**The site-side re-drive is the seat's own routing.** U19's recorded row stands on `/immersive/` and
reads the marker there; this unit proves the repair on the root road the client shares, and the brief
routes the re-drive after the merge.

**Two other unconditioned effects in `landOn` stay as they were.** The coat-check report
(`window.__NS_Seen(w.id)`) and the circle's own `walkSeen.add` at `:47` still run for a frame the
watcher reports while a face stands, so a work the door scrolls past can count as met. It is a
different law (EX-MEMORY / EX-DOOR-4) with its own rows, no measurement in hand says it misbehaves,
and widening this unit to reach it would have gone past the defect it was sent for. **Recorded for
the seat.**

**What the rows do not prove.** They read the marker, the frame in view and `scrollY` on the root
road at 390×844 with the synthetic fixture. The composed crossing's own behaviour under the guard is
carried by the pass suites in the full prover rather than by a row of this unit's own.

**The merge belongs to the delivery seat.** Branch `pass-api-v1-placefix`, base `3665da0`.
