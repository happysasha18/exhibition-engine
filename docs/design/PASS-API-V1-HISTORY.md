# PASS API v1 — superseded text

PASS-API-V1.md is amended in place. When a line there is superseded, the old text moves here with
its date and the reason it was replaced, so the contract carries one reading and the record keeps
the other. Appending a new paragraph while stale text stands is the failure this file exists to
prevent; the charter records it costing `lab/CROSSING-BRIEF.md` its reliability on 2026-08-08.

Entries are newest first. Each names the section it came from, the date it was superseded, and the
word that superseded it.

---

## 2026-08-14 10:31 — the camera in the budget, and how the geometry travels

Root: the composer's first real run against §4.4, and the implementation of §2.6 at `7ee2708`.

### From §4.4, the tier budget check

> **The tier budget check.** From `voice`, `levels`, `window` and the score's `duration`: a quiet link
> carries one letter, at most one accompaniment, no miracle, 2–4 s; a middle carries at most two
> letters, at most two accompaniments, at most one miracle, 5–8 s; a culmination carries two or three
> letters, at most three accompaniments, exactly one miracle, 9–14 s; and held time stays under a
> third of the pass. Everything counts, and no cue is exempt.

Replaced because the check counted voices from the cues alone. The camera is carried in the score's
`camera` record instead of as a cue, so it never reached the count, and a passage with two
accompaniment cues and a camera passed as carrying two. The charter's shelf 17 opens its list of
accompaniment voices with the camera, and its own words are that everything counts and no
never-counted class exists. The budget numbers are unchanged; what changed is what the count reads.

### From §2.6, how the two geometries reach the host

> The two are carried on the command's `doors` as `{ from:{hangGeometry, immersiveGeometry},
> to:{hangGeometry, immersiveGeometry} }`. The from-door is measured at `declare` and handed to the
> host on the offer at `prepare`; the to-door is measured at `declare` and re-measured on `reframe`.

Replaced because what was built at `7ee2708` hands the measurement through a read-only hook the
product owns, which the host calls at `prepare` and at `reframe`. Freezing the record onto every
declared command costs bundle bytes and the walk's bundle stands at 67 985 B against a 68 000 B
fence. The divergence is recorded in §11 with an owner rather than closed by the document adopting
what the code happened to do.

### From §1.1, the placement of the measurement

> The host receives the measurement as data on the offer at `prepare` and again on `reframe`, and
> holds no reference to the adapter. §2.6 states why the reading was placed this way.

Replaced by the declared exception now written in §1.1. That paragraph was itself written at 08:47
to resolve a conflict between his word and §1.1's fence, and the reading it chose was the one the
implementation then found too expensive in bundle bytes. The fence stands for the adapter as a
whole; one read-only measurement callback is the single exception, and conformance row 51 proves it
mutates nothing.

### From the Status block

> No
> line of code answers to any of the four today.

Replaced because it was true at 08:47 and is false for §2.6 at `7ee2708`. The four sections stand at
two different states, and the block now names each state separately.

---

## 2026-08-14 09:52 — what the first implementation found

Root: three design gaps the first serialiser built against §4.7 proved, reported through the
coordinator, plus his word of 2026-08-14 09:34 on how the making grammar reads.

### From §4.7, the ScenePlan record

Superseded record header:

> ```
> { schema, id, pair:{a,b}, direction:"a->b"|"b->a", seed, tier:"quiet"|"middle"|"culmination",
>   returnOf?:{ family, seed, passIndex },
> ```

Replaced because the record carried no `intent` line, while the charter requires every crossing plan
to open with an authored one and fails an empty or generic one by definition, and because `duration`
was unstated although the implementation derives it from the last cue window.

### From §4.7, the cue mapping

> **How a ScenePlan cue maps onto §4.4's cue.** The serialised cue keeps every field §4.4 lists and
> gains none.

That sentence stands, and it fenced only the score cue. The text around it left the plan cue
unfenced, and a reader concluded the two were one record. §4.7 now states that a plan cue may carry
fields the score cue lacks, names `cast` as the first of them, and states that every such field
resolves away at serialisation.

### From §4.7, the direction dialect

No text was superseded here; the mapping was absent. The plan writes `a->b` and the score writes
`a-to-b`. Both stay, because the score's form already ships and a stored address can carry it. The
mapping is now written into §4.7 so a third form never appears.

### From the Status block

The instrument sentence read:

> the first instrument, the
> woven one of §8, with its manifest and with every one of its nine handles reachable from a score;

Replaced because three instruments now stand on the host's frame, all green: the woven one, `matter`
at `a3416b7` on `pass-api-v1-ports` with 29 conformance rows, and the meshing `gears` at `6485972`
on `pass-api-v1-gears` with 31.

### His word of 2026-08-14 09:34, added rather than superseding

No text was replaced. §4.7 gains one paragraph confirming that no rule of the contract requires a
sequence of roles or a minimum count of them, and one naming the four optional registers — discovery,
provocation, feedback, apparition. The correction is recorded in the tlvphotos tree at
`docs/V2-STATUS.md` and its working consequences at `lab/PASSAGE-COMPOSER.md` §1a, commit `f2cdb11`.

---

## 2026-08-14 08:47 — the passage composer amendment

Root: his word of 2026-08-14 08:39, which named the missing layer between the PairDossier and the
score — the passage composer — and asked for four contracts to be written into the API: ElementSet
with one provider contract, ScenePlan, the return to the hang, and EdgeMemory with hysteresis.

### From the Status block

Superseded stamp and closing sentences:

> **Status, 2026-08-14 06:00.**

> Still written and unbuilt: the
> `pointer` driver, a stack of more than one cue, and the levels and tier-budget checks of §4.4.
> Section 11 lists what is declared-and-unbuilt with its owner.

Replaced because four sections of written-and-unbuilt contract were added and the sentence naming
what is unbuilt would otherwise have been short by all four.

### From §4, the heading and the opening sentence

> ## 4. The four data objects
>
> Pixels, knowledge about one work, and knowledge about a pair stay apart.

Replaced because the section now holds seven data objects: the four that were there, plus
ElementSet, ScenePlan and EdgeMemory.

### From §4.4, the cue record's `roles` line

> ```
>   roles:["disassembly"|"mystery"|"assembly"],
> ```

Replaced because a ScenePlan cue carries one of nine roles and the score is the ScenePlan's
serialised form. A score whose cue names `world` or `witness-camera` would have been refused whole
against the three-value enumeration, which would have made the serialisation impossible to write.

### From §6, the rest law

> **Rest on B.** The last pose equals the neutral pose within tolerance, and the check reads the pose
> rather than the picture, so it stays honest when the picture changes.

Replaced because the passage runs fullscreen and B has a real place in the exhibition layout to
return to. The arriving pose is the pose that lays B's immersive frame onto B's hang geometry. The
neutral pose remains the special case where the hang geometry is the whole frame, so every score on
file keeps the reading it was written under. The tolerance is unchanged at 1e-6, and the second
clause of the superseded sentence — the check reading the pose rather than the picture — was
carried across into the amended text word for word.

### From §11, the declared-and-unbuilt table

> | PairDossier direction A→B against B→A | recorded nowhere today | site build |

Replaced because §4.8 now states where the direction is recorded and what holds across it, and the
row points there.
