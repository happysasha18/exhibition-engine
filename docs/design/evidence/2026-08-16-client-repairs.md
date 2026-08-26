# U13 — four client repairs the input matrix measured

Run 2026-08-16 02:32 to 04:05 local, in the engine worktree
`/Users/sashaabramovich/exhibition-engine-clientfix` on branch `pass-api-v1-clientfix`, off
`pass-api-v1` at `53ccd56` (U11's door guard). Nothing outside that worktree was written; nothing
was merged, pushed or deployed.

U10's input matrix (`tlvphotos-immersive/docs/immersive/evidence/2026-08-15-input-matrix.md`) drove
sixty-four judged rows and parked nine defects, every one of them in the engine's own client. Four
of those are repaired here, each with a row that reddens when its repair is taken away.

## The four repairs

### 1 — the walk's rest record follows the dock

`engine/client/01a-pass.js:588`, inside `dock(cmd)`: `if (el && el.dataset &&
document.body.contains(el)) restingEl = el;`

`onViewportTurn` re-docks to `restingEl` (`engine/client/15-motion.js:204`), and `restingEl` was
written by the in-view watcher's organic intersection alone
(`engine/client/08-plaque-caption-io.js:105`). U10 §4b measured five rows red: after a device change
arrives mid-crossing, the NEXT one moves the walk to the DEPARTING work.

**The mechanism, measured rather than assumed.** A probe drove the synthetic walk at 390 × 844 with
a real renderer holding a scored crossing, turned the frame to landscape 1.2 s in, let the crossing
land, and turned it back:

| | |
|---|---|
| the walk stood on | `synth-13` (frame 1) |
| the crossing docked on | `synth-05` (frame 2), 0 px off centre |
| the record named, at the landing and a second later | **`synth-13`** |
| after the next turn the walk stood on | **`synth-13`** — thrown back, U10 §4b exactly |

The record is stale for one reason, and the probe reads it directly: the turn's own reflow brings
the arriving frame across the watcher's threshold INSIDE the watcher's 250 ms reflow guard
(`08-plaque-caption-io.js:104`), so the one report that would have named the arriving work is the
one report the guard swallows; the handoff then places the walk at that very same offset, no
threshold is crossed again, and no second report ever comes. With the dock correcting the record the
same drive holds the arriving work through the next turn.

A door landing carries no section of its own — `passResolveEl` hands back a plain `{id:"exh-fin"}`
marker — and the `dataset` check keeps it out of the record.

### 1b — the watcher leaves a foreign section alone while a renderer holds the command

`engine/client/08-plaque-caption-io.js:111`.

U10 §4a's side-effect — a turn mid-crossing warming a work eight frames away, 19 fresh requests —
was expected to fall with repair 1. **It does not, and the measurement says why**, so the repair
carries a second line and one half of the cost still stands.

The warming has two sources. The client's own half is this watcher: while a renderer holds the
command the walk's scroll stands still, so after the reflow it names a section the visitor is
neither on nor going to, and the report ran `landOn` whole for it — the picture ladder and the
one-ahead. The command's own destination still reports and still lands, exactly as before; every
other section, for the length of the flight, is the stale offset speaking and is now left alone.

Measured on the same probe, standing on frame 4 and turning mid-crossing, with each request's own
initiator read off the wire:

| | requests across the turn |
|---|---|
| with the line | 1 — `synth-07.png`, initiator `other` |
| without it (the control) | 2 — the same, plus `synth-24.png`, initiator **`script`** |

The `script` request is the client warming a work the visitor never approaches; it falls. The
`other` request is the browser's own lazy loading of a frame the new viewport brought near the
viewport — the same road U10 §6 names for the pictures that cross under Save-Data — and no client
repair can fell it. **Parked for the seat: the browser's own share of §4a's 19 requests stands.**

### 2 — a second gesture mid-crossing chains

`engine/client/15-motion.js:159-167`, inside `stepFrame`.

`EX-GLIDE` (`SPEC.md:1329-1331`) is the written law: a new input mid-transition chains to the next
frame and never re-rounds backward. The base was `glideGoal` while the walk's own animator ran and
`scrollY` otherwise; while a RENDERER holds the command the walk's scroll has not moved, so the
second gesture re-rounded onto the departing frame and re-declared the very step in flight — U10 §3,
four rows red, both behaviours alive behind a race. The base is now the running transaction's own
destination, which is the spec's own sentence. The walk's own glide road is untouched.

### 3 — the pack consults both device requests

`engine/client/01a-pass.js:373-379`, inside `passPackOpen`.

`passPackOpen` gated on a pack block existing and the layer being named; `passOpen` (`:842`) reads
the stillness request and the data request and stands the drawing machinery down under either. U10
§6 priced the gap: ten scene-plan shards, 443 844 B on disk and **36 420 B gzipped**, fetched under
Save-Data for crossings already refused — more, gzipped, than the 30 647 B standing the machinery
down saves. The pack now asks the same two questions and puts its refusal on the same surface, in
the same words: «save data», «reduced motion».

The seat's ruling of 08-16 01:44 is what settles this as a class rather than a fork: the stand-down
law's purpose covers optional prefetches as a class, and a shard fetched ahead of a crossing that
cannot play is one.

### 4 — the register collision ends inside the engine

`engine/client/01a-pass.js:75`: the register's setting `instruments` is now `instrumentNames`.

The bake writes the instrument ADDRESS record into the settings block under `pass.instruments`
(`engine/build.py:1473-1475`), and the register's site rung reads the settings block by name — so
every resolve handed a record to a check that wants a list and «setting `instruments`: wants a list»
went onto the refusal ring. The ring holds 64 rows; U10 §5 had to read the layer's own refusal one
step into the visit because the notes had pushed it off by the tenth.

**The boundary the ruling drew is kept.** Only the REGISTER's own name moved. The record keeps
`pass.instruments`, which is the landed contract of PASS-API §4.4d, and the site's own
`lab/delivery-check.py` still pins it (`:98` `PASS_BLOCK_NAMES`, `:459`). Nothing outside the
register ever read the setting: it is named in `PASS_REG` and nowhere else in the client, no shipped
score names it in `params` (the delivery pack's `templates.json` carries no `params` at all), and no
suite read it.

## The four red-on-bug proofs

Each repair was crippled ALONE — the file copied aside, the line put back to what it was, the client
re-assembled, the suite run, and the file restored from the copy. No git command restored anything.

| the row | its home | the scenario it reproduces | crippled |
|---|---|---|---|
| EX-PASS the walk's rest record follows the dock: the turn after a crossing holds the arriving work | `tests/test_pass.py` | a turn mid-crossing, then the next turn — U10 §4b | **red** |
| EX-PASS a second gesture while a renderer holds the command chains to the NEXT frame | `tests/test_pass.py` | a second gesture mid-crossing re-declaring the same step — U10 §3 | **red** |
| PASS-READER a visitor asking for stillness, or to save data, is sent neither the reader nor a shard | `tests/test_pass_reader.py` | a shard fetched under Save-Data — U10 §6 | **red** |
| EX-PASS the register names nothing the settings record already owns, so real refusals stand | `tests/test_pass.py` | the register note flooding the ring — U10 §5 | **red** |

What each crippled run said, in its own words:

- the dock: «the walk rested on synth-13 (frame 1), the host held the crossing to synth-05, a turn
  arrived mid-crossing, the crossing docked on synth-05 and the next turn left the walk on
  **synth-13**».
- the step: «from synth-09 the walk declared 2 steps while the host held the command: first to
  synth-13, then to **synth-13**» — the same step, twice, where the frames in order run
  `synth-09 · synth-13 · synth-20`.
- the pack: a visit that asked to save data fetched `pass-reader.js`, `manifest.json`, `head.json`,
  `templates.json` and a shard per landing.
- the register: «after ten steps the ring carries 13 refusals; notes about a setting the record
  owns: `{what: setting, name: instruments, source: site, why: wants a list}`; the register's names
  are [… `instruments` …]». On the synthetic walk the layer's own note still survived ten steps;
  the real route U10 drove mints about four such notes a step and had lost it by the tenth.

The first two rows are driven through the seam's own registration door with a host that TAKES the
command and holds it, and settles by the §2.2 road — handoff, curtain down, dock. It draws nothing:
what these rows read is the walk's side of the seam, and the renderer's picture has its own suites.
The frame heights the first row turns between are chosen so the turn reproduces U10's road exactly:
the walk's sections are one viewport tall, so a walk resting on frame 1 stands at scrollY = 900, and
halving the height mid-crossing puts that same offset on frame 2 — the arriving work — inside the
watcher's 250 ms guard.

## The runs

Taken under the quiet rule this seat set: ten cores, so a full run is taken at a one-minute load of
twenty or under, and the reading is recorded before and after.

| run | result | wall | load before → after | log |
|---|---|---|---|---|
| `python3 tests/test_pass.py` — the suite both motion rows and the register row live in | 28 of 28 | 63.3 s | — | — |
| `python3 tests/test_pass_reader.py` — the pack's own suite | 20 of 20 | 58.0 s | — | — |
| `python3 tests/test_budget.py` — the byte fences | 9 of 9 | 0.2 s | — | — |
| `python3 tests/run_all.py` — the full engine prover | **56 of 56 green** | **265 s** | **2.50 → 21.52** | `docs/design/evidence/2026-08-16-client-repairs-prover.log` |

The three suite walls are the full run's own recorded durations (`tests/suite_timings.json`), taken
under eight suites in parallel; run alone each takes longer.

The wall sits on U11's 254 s. No suite reddened, so no rerun was needed and no reading had to be
judged against the machine.

## The byte fences

Only one shipped file changed, and it is the bundle.

| file | gzipped | fence | before |
|---|---|---|---|
| `engine/assets/exhibition.js` | **68 634 B** | 69 000 B | 68 459 B |
| `engine/assets/exhibition.css` | 7 743 B | 9 000 B | unchanged |
| `engine/assets/pass-layer.js` | 23 327 B | 24 000 B | unchanged |
| `engine/assets/pass-reader.js` | 3 201 B | 3 500 B | unchanged |
| the four instrument files | 5 444 / 5 558 / 3 279 / 4 167 B | 6 000 / 6 100 / 3 550 / 4 500 B | unchanged |

The four repairs and their comments cost the bundle **175 gzipped bytes**, and 366 B of the fence
remain under it.

## Conclusion

A visitor who turns the phone while a crossing runs and then turns it again now stays on the work
the crossing arrived at. A second gesture mid-crossing advances a frame instead of re-declaring the
step already in flight, so `EX-GLIDE` holds on both roads rather than on one and a race. A visitor
who asks to save data, or for stillness, is sent neither the delivery pack's reader nor a single
shard, and the refusal says which request refused it. And the register no longer names what the
settings record owns, so the diagnostic surface carries real refusals instead of the same note four
times a step.

## Limitations, and what is parked

**Parked — the browser's own half of §4a.** A turn mid-crossing still reflows the walk's tall
document under a standing scroll offset, and the browser lazily fetches the frames that come near
the new viewport. The client's own share of that warming falls with repair 1b, measured above; the
browser's share is not the client's to refuse, and U10 §6 names the same road for the pictures that
cross under Save-Data. It is a real cost on a real turn and it is left for the seat.

**Not touched — the pose leak on four of five drawing buffers.** The instrument reads its doors in
CSS pixels while the shader binds the drawing buffer, whose size follows the device ratio and a
runtime ladder. It is parked for the seat, none of these four repairs touches it, and nothing here
moved it.

**Not touched — the three product questions U10 parked.** The still vistas the charter asks for
under reduced motion, the gracious line for a reach during a crossing, and the rows that need a real
device: all product or hardware questions, none of them a defect this unit was sent for.

**What the rows do not prove.** The first two rows drive a host that takes the command and draws
nothing, so they read the walk's side of the seam and never a pixel; the renderer's own behaviour
under a turn is `tests/test_pass_hang.py`'s row 7, which ran green here unchanged. The register row
is read on the synthetic walk, where about one note a step is minted rather than the four U10
measured on the real route — the ring's flooding is quoted from U10 rather than re-measured here.

**The merge belongs to the delivery seat.** Branch `pass-api-v1-clientfix`, base `53ccd56`.
