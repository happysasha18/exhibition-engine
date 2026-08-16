# Family breath at fill time — the contract field and the client's roll (U16)

Branch `pass-api-v1-familybreath`, worktree `/Users/sashaabramovich/exhibition-engine-familybreath`,
based on `pass-api-v1` at `ce2c709`. Code, contract and suites landed at **`730b970`**; this record
is the commit after it.

Root: the delivery seat's unit brief of 2026-08-16 08:20
(`/Users/sashaabramovich/tlvphotos/docs/immersive/briefs/2026-08-16-U16-family-breath-engine.md`),
which carries the seat's ruling of 08:11 — the roll lives at fill time on the play side, the composer
writes each row's bounds, pack digests stay unmoved, and a judging run pins the seed.

## 1. What stood before

A pack row and a table row carry measured numbers, and the fill writes them exactly. So a pair
flipped four times inside one visit played one score, byte for byte — the site's own U9 measurement
(§4 of `docs/immersive/evidence/2026-08-15-return-and-chrome.md` in the site tree). The charter asks
for the opposite: within a session a flipped pair plays the same passage FAMILY with small parameter
shifts each pass — variation, never repetition and never total novelty (`lab/CROSSING-BRIEF.md` §16).

## 2. The contract section

`docs/design/PASS-API-V1.md` §4.4f, lines 593–662, *Family bounds, and the roll at fill time*.

**The field's shape.** A row MAY carry a family-bounds record:

```
{ spans: { <slot>: [low, high], ... }, seed: true|false }
```

- `spans` names, per SLOT the row already fills, the closed span the fill may roll that slot's value
  inside. A slot is exactly one handle a cue drives, so the addressing is the row's own: the inline
  road (§4.4c) names a slot by its name, the pack road (§4.4d) by the slot's ordinal in its shape's
  `slots` list, written as a string key. A slot the record does not name fills as it fills today.
- `seed: true` re-rolls the score's own `seed` field each pass. A seed has no meaningful span, so it
  is a yes-or-no; a cue's own seed HANDLE, where one is a slot, is bounded like any other handle and
  its whole range as its span is what re-rolling means for it.
- Both fields are optional; the record is refused whole on any other field, as a score is.

**Why the bounds live on the ROW.** What a handle may do is what that pair's own measurement
supports, and no two pairs support the same spans. The template holds no bounds, so a pack's
addresses and digests do not move for this: a row grew, and a row is the one place per-pair numbers
have always lived. The pack road recognises the record by its being the row's LAST entry and a record
rather than a number, so the pack keeps ONE row shape and a row that carries no bounds is the row it
has always been.

**Where the row travels through the record shape.** The measured numbers are written first, then the
rolled values at the bounded slots, then the score's own `seed` when the record asks for it. A slot
may name a score-level field of its own, so a slot named `seed` writes `score.seed` too — and where
both roads reach that field, the re-roll is last and stands. The precedence is a conformance row
rather than an accident of the code (§7, the inline road's first row).

## 3. The mechanism, with files and lines

**One roll, in the walk's own bundle** — `engine/client/01a-pass.js`:

| what | where |
|---|---|
| `familySeed`, the register's own setting, on the session/site/default rungs | 82–89 |
| the visit's seed, read once and held; pinned when the setting is not zero | 322–332 |
| `passMix` / `passText` — the two integer mixes the roll runs on | 334–344 |
| `passBreath` — the checked record, the per-slot roll, the diagnostic row | 345–384 |
| the inline road applying the roll after every measured number | 405–425 |
| the reader handed the same roll in its environment record (`breath`) | 462–468 |
| the roll's own block on the diagnostic surface | 995–1001 |

**The pack's reader reads the row and never mints a seed** — `engine/assets/pass-reader.js`:

| what | where |
|---|---|
| `breath`, taken from the environment record the bundle hands over | 80–84 |
| the row's last entry recognised as a family record, and the slot count adjusted | 228–239 |
| the rolled values written at the same slot paths the measured ones are written at | 258–284 |
| `breathes` on the reader's own half of the diagnostic surface | 371–374 |

**The seed of a pass** is `mix(mix(visit, pass index), pair key)`, and each bounded slot draws from
`mix(pass seed, slot name)`. The pass index is the generation `declare` mints, so:

- a pair flipped twice inside one visit rolls twice, because the index moved;
- two fills of one row inside ONE declared pass are the same score, because a crossing has one score
  however often it is asked for;
- the same crossing met in a later visit differs, because the visit's seed differs;
- a pinned visit reproduces at every index, because nothing here reads a clock.

**Refusals.** A record that is not a record, an unknown field, a `seed` that is no yes-or-no, a span
that is no low-to-high pair of finite numbers, a bounded slot the template or shape lacks, and a
rolled value landing outside its own span each refuse the WHOLE row with the reason on the diagnostic
surface, and the crossing takes the walk's own glide. Half a rolled score is produced by no road.

**The diagnostic record** carries the visit's seed and whether it was pinned, and per rolled crossing
the pair, the pass index, the seed that pass ran on, the spans read and the value applied to each
bounded slot — for example, from the pack-road run below:

```
{"pair":"synth-07__synth-24","at":4,"visit":2521437387,"pinned":false,"seed":3624592801,
 "scoreSeed":0.9993875280488282,"spans":{"2":[3,9]},"applied":{"2":6.762971106916666}}
```

## 4. The proofs on the pack road — `tests/test_pass_reader.py`, 27 rows green

Six rows are new (the file's rows 21–26 by print order):

1. **A bounded pair flipped twice in one visit fills two kin scores differing in the bounded handles
   alone.** The seed node filled at 6.762971106916666 and 7.313170047942549, both inside 3.0…9.0; the
   score's own seed at 0.9993875280488282 and 0.13675955636426806; every other field identical field
   for field — same shape, same cue, same instrument, same stack, same duration.
2. **A pinned visit fills the same bounded crossing byte-identically.** Two whole visits pinned at
   778811 met the crossing at pass indices 4, 5 and 6 and filled it identically at each, while the
   rolled values across those indices were 5.493821, 6.233794 and 8.865107 — reproducible without
   being frozen.
3. **A row carrying no family bounds fills exactly as it filled before §4.4f** — A→C in the same
   pack equals the pack's own score for that pair to the last leaf.
4. **A high-to-low span refuses the row and names it**: «the span for «2» is no low-to-high pair of
   numbers», and the crossing glides.
5. **A rolled value outside its own span refuses the row and names the span**: with the roll crippled
   to answer 2.0 for a span of 3.0…9.0, the surface reads «the rolled «2» 2 stands outside its span
   3…9» and no score reaches the command.
6. Red-on-bug · **the span check removed**: the same broken roll fills the score and the bounded node
   reads 2, outside the 3.0…9.0 the row named — so row 5 is held by that check and by nothing else.
7. Red-on-bug · **the roll disabled**: with the walk handing the reader a roll that answers no
   values, two declares over one pair fill two byte-identical scores, the bounded node reading 7.7701
   twice. That is the U9 defect, reproduced on demand.

The twenty-one rows that stood before are untouched and green, including the frame-for-frame row
between the pack road and the inline road.

## 5. The proofs on the inline road — `tests/test_pass_weave.py`, 49 rows green

Two rows are new:

- **A row carrying family bounds fills the same way twice inside one pass, and differently inside its
  span on the next.** The bounded seed node filled at 4.6190279467076065 twice inside one pass and at
  4.5898062776818875 after a declare, both inside 4.5102…5.3102, every other field identical. The
  same row asks for the score's own seed to re-roll: 0.3930223002098501 against 0.4697088575921953
  across the two passes, which is the precedence §2 states, read rather than argued.
- **A family bound naming a slot the template lacks refuses the row, and names it**: «its family
  bounds name «tilt», a slot the template lacks».

## 6. Suites and the prover

- `tests/test_pass_reader.py` — 27 rows: 27 pass, 0 fail, 0 skip.
- `tests/test_pass_weave.py` — 49 passed, 0 failed, 0 skipped.
- `tests/test_budget.py` — 9 rows, 9 pass.
- **The full engine prover: `56/56 suites green · wall 261s`**, exit 0, on a quiet machine.
  Log: `docs/design/evidence/2026-08-16-family-breath-prover.log` (the verdict line is line 58).

## 7. The byte fences

| shipped file | measured | fence | headroom |
|---|---|---|---|
| `exhibition.js` | 69 614 B gzipped (was 68 634) | 69 000 → **70 000** | 386 B |
| `pass-reader.js` | 3 522 B gzipped (was 3 201) | 3 500 → **4 000** | 478 B |
| `exhibition.css`, `pass-layer.js`, the four instruments | unchanged | unchanged | unchanged |

Both moves carry their reason in `tests/test_budget.py` beside the number, and the bundle's move
answers the delivery question the fence exists to force: the roll is called from inside `declare` on
both fill roads, and a site scoring by §4.4c's template and table fetches no reader file at all, so
the roll cannot travel in `pass-reader.js`; nor can it exist twice, because two copies would be two
ideas of what a family is. The reader is handed the one roll (1 318 B of stripped source landed
there, 321 B gzipped, and it is the READING of the row rather than the rolling). The bundle's
addition is 3 449 B of stripped source, 980 B gzipped. §12 of the contract carries the re-measured
headroom with its date.

## 8. Conclusion

A row may now say what breathes, the fill rolls it once per pass, and both fill roads roll by one
rule and one seed ladder. A public visit's every run exists once; a judging run pins `familySeed` and
reproduces to the pixel; a row with no bounds is untouched; and a bad bound or a broken roll refuses
the row rather than drawing a picture nobody can read back to a number.

## 9. Limitations, and what this unit did not do

1. **No row in any shipped pack carries bounds yet.** Writing them from each pair's own measured
   ranges is U17's work on the site side; until it lands, every shipped row fills exactly as before
   and this section changes no visitor's picture.
2. **The visit's seed is read once per page life.** A `familySeed` written mid-visit takes effect on
   the next load, which is what keeps one visit inside one family. Stated in the code beside the read.
3. **A visit is a page life, not a session store entry.** A reload rolls a new visit seed. That
   matches "the same crossing met in a later visit differs again" and is the cheapest honest reading;
   a session-stored visit seed would be a different product decision and nobody has asked for one.
4. **The seed handle still does not reach the meshing instrument's shader** — the open item the seat
   holds from U15 §8. Where a score's seed is re-rolled, the instruments that read `seed` see the new
   number and that instrument does not; this unit did not touch it, and it is why the proofs read the
   FILLED SCORE rather than a drawn frame for the seed.
5. **The spans are checked for being spans, never for being sensible.** That a handle may breathe
   only inside what its own measurement supports is the composer's law, and U17's gate is where it is
   enforced; the client refuses a malformed span and an out-of-span roll, and takes a lawful-looking
   wide span at its word.
6. **No deploy, no merge, no push.** The merge into `pass-api-v1` belongs to the delivery seat, and
   U17 waits on it.
