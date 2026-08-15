# U6 — the play side reads the delivery pack

Run 2026-08-15, engine tree `/Users/sashaabramovich/exhibition-engine-packreader`, branch
`pass-api-v1-packreader`, from `54034c1` on `pass-api-v1`. Four commits carry the work — `670dd60`
the reader and the fence, `6fad45a` its suite, `f38b08e` the warming repair, `ee6735a` the
contract — and the branch ends at the commit carrying this record. Nothing was merged, pushed or
deployed, and nothing outside this worktree was written.

The site composes a score for every ordered pair, ships them as a pack of static files, and writes
the pack's addresses into its settings record under `pass.packs`. Until this unit no byte a visitor
ran read that name: the client's only fill road was `passFillScore`, which reads `pass.scoreTables`
and `pass.scoreTemplates`, and the string `packs` appeared nowhere under `engine/client/`. So every
crossing on the staged road fell back to the walk's own glide in silence, and a full nineteen-step
route drive asked the wire for no shard at all — measured three ways in the site tree's
`docs/immersive/evidence/2026-08-14-walk-slice-three-works.md` §2.

This unit writes the reader, warms its shards at the landing, and raises the client's score fence to
a measured baseline that the site side can read as a capability.

## 1 — the mechanism

**The reader travels as its own file, and the bundle keeps the door.** The walk's own bundle stood at
67 985 B gzipped against a 68 000 B fence — 15 B of headroom — and the host at 23 327 B against
24 000, which is 673 B. The reader weighs 3 201 B gzipped: 200 times the bundle's headroom and 4.6
times the host's, so neither could carry it. It therefore ships as `engine/assets/pass-reader.js`,
fetched once by the bundle the way `pass-layer.js` already is, on a walk whose settings record
actually names a pack and whose layer is on. A visit that never draws never asks for it.

What stays in the bundle is the part that cannot live outside it, 474 B gzipped in all:

| where | what it does |
|---|---|
| `engine/client/01a-pass.js:328` | `PASS_PACK_SRC = "pass-reader.js"` — the address |
| `:351` `passPackOpen` | asks for the reader once, and only when `pass.packs` is non-empty and `visualLayer` is `pass` |
| `:334` `passPackSet` | the reader hands over a factory; the bundle calls it with the pack addresses and one way to speak, so the bundle stays the one owner of the settings block and of the diagnostic surface |
| `:377` `passWarm` | the landing hook: the work's id, the reader opened, the work warmed |
| `:742`, inside `passLandGate` | where the landing hook is called — every road that makes a work current comes through here |
| `:402`, inside `passScoreFor` | the one synchronous question a declare puts to the reader, after `pass.scores` and before `passFillScore` |
| `:849`, inside `passReport` | the reader's own record, folded onto the existing diagnostic surface under `pack` |

**How a shard is fetched.** `engine/assets/pass-reader.js`:

1. `packOpen` (`:143`) fetches the pack's `manifest.json` at `base + "manifest.json"` and weighs it
   against the digest the settings record carries. That digest **is** the manifest's own SHA-256, so
   the record roots the whole chain. The manifest then carries the SHA-256 of every other file in the
   pack, and `head.json`, `templates.json` and `authored.json` are fetched and weighed against it
   (`fetchJson`, `:100`).
2. `warm(workId)` (`:293`) is called by the bundle at every landing. It asks once per work; a work
   already asked for is never asked again, and a file refused once stays refused for the visit — the
   same law §7 states for an instrument file.
3. `shardAsk` (`:194`) fetches `base + "rows/" + workId + ".json"` and weighs it against the
   manifest's own record for that path. A work the manifest's `worksWithAShard` does not name carries
   no shard at all, and that is recorded **without a request** — the manifest is the pack's own answer
   to the question, so no round trip is spent learning it.
4. `scoreFor(key)` (`:260`) reads only what has already arrived. It never fetches.

**How the row's own shape template is picked.** `fillFrom` (`:220`). A row is a flat list whose first
entry indexes the head's `shapes`; that name keys `templates`; the template carries a `score` and a
list of `slots`, each an addressed path into it. The score is deep-copied and `row[i + 1]` is written
at `slots[i]` (`setAt`, `:67`). This is the play side of `fill_from_row` in the site's own
`lab/build-delivery-v1.py:175` — the same paths, the same order, the same assignment.

The shipped pack carries **twenty-five** shapes. The client's inline road takes one template per
INSTRUMENT, and that assumption does not hold for a pack: two pairs of one shard routinely stand on
two different shapes. A row whose shape names no template, whose value count does not match the
shape's slot count, or whose slot path reaches nothing refuses the WHOLE score with its reason — the
fill runs on a copy, so a row refused halfway leaves nothing behind, which is the law
`passFillScore` already keeps.

The pair key is the crossing's own `<departing>__<arriving>`. The composer keys its rows in one
canonical order with a tag saying which way the crossing runs, and both directions live in the
DEPARTING work's shard, so both candidates — `<a>__<b>__ab` and `<b>__<a>__ba` — are looked for
there, and the plain `<a>__<b>` form the weave table uses is looked for beside them. Nothing is
inferred about the order the two ids were written in.

**A failed or missing fetch glides, with its reason.** `scoreFor` answers null, `passScoreFor` falls
through to `passFillScore`, that answers null too, the command freezes no score, no cue names an
instrument, the host takes nothing and the walk's own glide lands the step — which is exactly the
product's behaviour with no renderer at all. The reason goes onto the bundle's existing refusal list
through the `note` hook the bundle handed the reader, so it reads on `passReport().refusals` as
`{what: "pack", …}`, and the reader's whole record — every pack, its state, and every shard this
visit asked for — reads at `passReport().pack`. Each reason is put on the surface once, never once
per crossing. The reasons seen in the suite, in the reader's own words:

    rows/<work>.json: the server answered 404
    rows/<work>.json: its bytes weigh to 3cef160df47bc435…, and the pack's manifest says bc66b971166369a5…
    the pack carries no shard for this work — it stands outside the N the pack was built over
    its shard had not arrived when the crossing was declared
    the pack's shard for this work carries no row for this pair

**A pack whose head names no shapes is not filled**, and says so: its rows are of another form, and
only its `authored.json` is read from it. That is how the shipped `scores` pack — the weave
instrument's own table, whose rows are named-slot records — is handled beside the composer's
`scenePlans` pack in one settings record.

## 2 — the warming design

`passScoreFor` answers synchronously inside `declare`, and a crossing is declared the instant the
visitor moves, so a fetch begun there could never arrive in time. The shard holding a work's
OUTGOING crossings is therefore asked for when the walk LANDS on that work — the fork U5 named.

The landing hook sits in `passLandGate` (`01a-pass.js:742`), which is the one owner of «this work is
now current»: the in-view watcher, the transition's own dock, a restored place and a programmatic
jump all arrive there, so the entry hang warms as surely as a stepped-to work does. A landing that
happens before the reader itself has arrived is remembered and warmed the moment it joins
(`passPackWarm`, `:334`).

**A landing that arrives while the pack is still opening is held, never dropped.** This was a real
defect, found by the shipped-pack check of §5 and repaired at `f38b08e`: `packOpen` returned at once
for a pack already in flight, and the caller's `shardAsk` was then skipped because the pack was not
yet `read`. The first landing of a visit opens the pack, and every landing during that open — the
ones whose shards a visitor needs first — was lost. Each now waits in the pack's own queue and is
answered the moment the open settles, either way (`packSettled`, `pass-reader.js:137`). The suite row
«a landing that arrives while the pack is still opening is held, never dropped» hands a fresh reader
three works in one breath and requires all three shards.

Nothing blocks. `scoreFor` performs no fetch — proved by a row that reads the file's own text: no
`fetch(` stands anywhere between `scoreFor` and `warm`.

## 3 — the fence, and where it is published

`PASS_LIMITS.bytes` rises from 8192 B to **12 288 B** (`engine/client/01a-pass.js:45`), written as an
observed baseline with its evidence in the lines above it.

**The evidence.** Built from the site's own sources with
`EXHIBITION_ENGINE_ROOT=/Users/sashaabramovich/exhibition-engine-pass-api-v1 python3
lab/build-delivery-v1.py <out> --report` in `/Users/sashaabramovich/tlvphotos-immersive` at
`11842cb`, which reproduced the addresses U5 measured — `plans/v2-b27cc41a8bf15346/` and
`scores/v1-1e4e2f3fd153c86f/`. Every one of the pack's rows was then filled by `fill_from_row` and
weighed as `JSON.stringify` writes it, which is the measure `passScoreCheck` applies:

| | scores | median | longest | over 8192 B | over 12 288 B |
|---|---|---|---|---|---|
| the shipped `scenePlans` pack | 7708 | 7029 B | **10 851 B** | 1783 (23.1%) | 0 |

At 8192 B, 1783 composed passages were refused before any instrument saw them. At 12 288 B the
longest score the composer has ever written passes with 1 437 B to spare, and the whole pack clears.
The number moves what a visitor can be shown; the command above is what re-measures it.

The refusal now names the size it measured beside the fence it applied
(`01a-pass.js:240`): `weighs 15576 bytes, over the 12288 a score may weigh`. A reason giving only the
fence left the one number its author has to act on unsaid.

**Where it is published.** `engine/build.py:687`, `pass_capabilities()`, READS the number out of the
served client with a regex over the `PASS_LIMITS` literal and writes it into `config.json` under
`pass.capabilities` (`:1482`), beside the instrument record that already travels there:

    "pass": { "visualLayer": "pass", "capabilities": {"scoreBytes": 12288}, "instruments": {…} }

It is read rather than restated, so the published number and the applied number are one number and a
copy cannot drift. A site's build-time script reaches it either way: from a baked `config.json`, or
by importing `engine/build.py` and calling `pass_capabilities()` — the road `tests/test_budget.py`
already uses to import that module. U7 measures against that number. The contract states it at
`docs/design/PASS-API-V1.md` §4.4e, and the pack and its reader at §4.4d.

## 4 — the proof

`tests/test_pass_reader.py`, **19 rows, 19 pass, 0 fail, 0 skip**. Every browser row bakes a
synthetic site, writes a pack of static files beside it, serves the pair, and drives the walk's own
`declare` — the same door the stepping input knocks on. Nothing is stubbed. The pack carries two
shapes whose scores differ in band count, seed and duration, and one shard holds two pairs, one on
each shape.

The four red-on-bug proofs each serve a CRIPPLED copy of one file, take the same measurement, and
pass when the answer MOVES. The file is set aside as a copy first and restored from that copy after;
no git command restores anything.

| the proof | what is crippled | what it reddens on |
|---|---|---|
| a digest mismatch refuses the shard | the reader's `if (want && got !== want)` → `if (false)` | with the comparison in place a shard whose bytes changed after the manifest weighed them is refused unread and the crossing glides; with it gone the very same bytes fill a score and the crossing takes it |
| a missing shard glides with its reason | the reader's `note(name, why);` removed | with the note in place a dropped shard glides AND says «the server answered 404»; with it gone the same step still glides and the diagnostic surface carries nothing at all — which is the silence this unit was sent to end |
| a score over the fence is refused with its measured size | the walk's own bundle, `bytes > PASS_LIMITS.bytes` → `false` | with the fence in place a 15 576 B score reaching the client from the pack is refused with its own weight named; with the comparison gone the same score is taken whole |
| the warmed-shard road serves a crossing | the reader's `pk.head.shapes[row[0]]` → `pk.head.shapes[0]` | with the row's own first entry read, the pair fills the shape it names and draws a frame byte-identical to the same score served inline; with the index ignored the same pair fills a 6500 ms score and the frame moves |

The pixel row itself: the pass held at 2.50 s of a 6500 ms score with the host's clock and progress
pinned, photographed on the walk's own road twice — once with the score fetched from the pack, once
with the same score written into the settings file — and **the two frames are byte-identical**.

The other rows: a crossing takes its score from the pack; the row's own shape picks its template
while a second row of the same shard picks the other (3000 ms/eight bands against 6500 ms/three
bands, in both directions); the filled score equals the pack's own score to the last leaf; only the
works the walk landed on were ever asked for; a landing during the pack's own open is held; and the
bake serves the reader and publishes the fence.

## 5 — the reader against the shipped pack

The suite stands on a synthetic pack, because the site tree is read-only source material and a suite
that could only run beside it would prove nothing on its own. So the shipped pack was driven
separately, as evidence: the real `plans/v2-b27cc41a8bf15346/` staged beside a synthetic site, the
reader loaded in a browser through its own factory, twenty-six pairs sampled — **one per shape,
covering all twenty-five, plus the longest filled score of the whole pack** — each fetched through
the reader's own digest chain and compared against `fill_from_row`'s answer in Python.

    checked 26 filled scores against fill_from_row: 0 differ
    pack state read, 11 shards read
    the reader's own refusals: none

The rig is `real-pack-check.py` in this run's scratch directory and is not committed: it reads the
site tree, which this unit may not depend on. Its whole method is the paragraph above, and the
command that rebuilds the pack it reads is in §3.

## 6 — the suites, and the byte fences

Suites run as the work went: `budget`, `assembly`, `dead`, `pass_api`, `pass_weave` and
`pass_reader`, each green on its own, then the full engine prover.

**The full engine prover: `python3 tests/run_all.py` — 56 of 56 suites green, wall 255 s, no red and
no skip.** The census rises from 55 to 56 with `pass_reader`, registered in the runner's own
`SUITES` list. The log is `docs/design/evidence/2026-08-15-pack-reader-prover.log`. It was taken on a
shared machine whose load ran between 12 and 42 through the run, and every suite came back green
anyway — the clean full run U5 was owed on this tree.

| file | gzipped as shipped | fence | state |
|---|---|---|---|
| `exhibition.js` | 68 459 B | **69 000 B** (was 68 000) | 541 B under |
| `pass-reader.js` | 3 201 B | **3 500 B** (new) | 299 B under |
| `pass-layer.js` | 23 327 B | 24 000 B | 673 B under, untouched |
| `exhibition.css` | 7 743 B | 9 000 B | untouched |
| `pass-inst-adrift.js` | 5 444 B | 6 000 B | untouched |
| `pass-inst-gears.js` | 4 594 B | 5 000 B | untouched |
| `pass-inst-matter.js` | 3 279 B | 3 550 B | untouched |
| `pass-inst-weave.js` | 4 167 B | 4 500 B | untouched |

**The host stayed under its own fence and never moved**: the reader is not in it, so its 673 B of
headroom stands exactly where it stood. The bundle's fence moved by the file's own rule — the fence
did its job at 15 B of headroom, the delivery question it exists to raise was answered rather than
waved through (the reader travels), and the fence now tracks the new baseline tightly, which is the
same move `test_budget.py` records for 2026-08-13 and 2026-08-14. `pass-reader.js` gets its own fence
from day one at its measurement plus about a tenth, the rule §12 states for the host and §7 for each
instrument.

## Conclusion

A crossing on the immersive road can now be played from the composed pack. The pair's shard is
fetched when the walk lands on the departing work, weighed against the pack's own manifest, and the
row's own shape template is filled at the moment the crossing is declared — and the resulting score
is the composer's own, to the last leaf, over all twenty-five shapes of the shipped pack. A shard
that fails to arrive, fails its digest, or holds no row for the pair leaves the walk's own glide
where it always was, with the reason on the diagnostic surface instead of silence. The score fence
stands at a measured 12 288 B and is published where the site can read it.

## Limitations, what is parked, and the forks

**The stack placement law still refuses most composed plans.** 5428 of the 7708 serialised plans put
a coverage-writing cue lowest, which the host refuses whole — 70.4 percent, counted by a mirror of
the host's own `stackOrder` and `coverageWhyNo` run over the shipped pack and checked against the
host's live refusals on U5's route. Nothing in this unit touches it: a pair whose plan the host
refuses now reaches the host and is refused there, where before it never reached it at all. It is
U7's, and the seat's ruling of 08-15 20:36 already names the answer.

**Five of the 121 hung works stand outside the composer's 116**, so their shards do not exist. The
reader answers that without a round trip — the manifest's own `worksWithAShard` — and records «the
pack carries no shard for this work». Bringing those works into the pair table is U7's.

**The reader file itself travels unweighed, like the host.** `pass-layer.js` is fetched by a plain
relative script tag with no digest, and `pass-reader.js` travels the same way for the same reason:
both are the engine's own files, written by the same bake, served from the same origin as the page
that asks for them. The digest chain in this unit weighs the SITE's files — the pack — which the
engine does not write and cannot otherwise trust. **The fork**, if a unit ever wants it: give the
bake a record for its own served files the way it already records each instrument's digest, and have
the bundle weigh the reader before running it — which would need the fetch-and-weigh road in the
bundle, and the bundle is where the byte fence bites hardest.

**A pack whose head names no shapes is read for its authored scores alone.** The shipped `scores`
pack — the weave instrument's table, 12 210 rows over 111 shards — fills by the named-slot rule the
bundle's own `passFillScore` already carries, not by the shape-factored rule the reader implements.
Its authored score for the worked pair is served; its rows are not. **The fork:** a later unit may
hand that pack's head and templates to `passFillScore`'s road, which would put a plain woven crossing
on pairs the composer declined. How many pairs that is has not been counted here — the two tables'
keys were never intersected — and the count is worth taking before the build is.

**`tests/suite_timings.json` is rewritten by every full run** and is committed with this branch's
run, which was taken on a machine carrying another session's load. The durations in it are therefore
long, and they set the runner's queue order rather than any verdict.

**One frame, one cast, one device.** The pixel row holds at 390 × 844 on this machine's Chrome, on a
score the suite writes itself. What a composed pack draws on a real phone is U8's.
