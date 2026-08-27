# Prover — `SPEC.md` § The pass — a composed crossing between two works (2026-08-27)

Prover skill version: live-spec pack `product-prover`, base `live-spec-base` v4.3.0.

Mode: CROSS-LINK over one added section (`SPEC.md:569-642`, `EX-PASS` / `EX-PASS-COMPOSER` /
`EX-PASS-LEVEL` / `EX-PASS-VOICE` / `EX-PASS-DOOR`, plus its index rows `SPEC.md:1911-1920`,
`:1967-1971`, `:2111`). Every mandatory Phase 3e sweep ran, scoped to the new section and its seams,
together with the whole-document quantifier re-verify. Phases 3a–3d ran over the section alone; the
other ~1,900 lines of `SPEC.md` were read for seams and contradictions, not re-proven.

Reviewer hat: formal-methods, clean context. This seat authored none of the text under review.

**Why this record exists.** An earlier наряд's commit message claimed "product-prover ran against the
new text and found two defects fixed in place". No such record exists: the newest file in
`docs/prover/` before this one is `2026-07-19-sound-greet.md`, and no `*-prover.log` names this
section. That claim was never real, and this file is the first genuine pass over this text.

## Phase 0 — Triage

`TRIAGE: PROCEED`. The section is operational product prose with entities, states, a lifecycle and
stated refusals.

The section claims a **shipped** system in the present tense ("A plan is refused where…", "is refused
before it plays"). `ARCHITECTURE.md`'s Nodes table carries no row for `engine/assets/pass-composer.js`
or any `engine/assets/pass-inst-*.js` — the whole pass/instrument layer is unpinned, which
`TEST_MATRIX.md` names for itself. Every finding below therefore stands on primary sources read
directly: `engine/assets/pass-composer.js`, `engine/assets/pass-layer.js`, `tests/test_pass_score.py`
and `docs/design/PASS-API-V1.md`, cited by `file:line`. Nothing here rests on the section's own prose.

## Opening assessment

The section sets out to place the pass layer among the rest of the exhibition and to close one named
confusion — that "level" answers three questions and never one. It does that job well: the
declaration / ownership / driving split at `SPEC.md:602-618` is exact, matches
`pass-composer.js:1332`, `:3866-3869` and `:4018` field for field, and the "four fields that live only
in the plan" count is literally true (`PLAN_ONLY_CUE_FIELDS` holds exactly `cast`, `levelOwnership`,
`measuredHandles`, `returnOf`). The `EX-PASS-VOICE` / `EX-STORY` and `EX-PASS-DOOR` / `EX-DOOR`
disambiguations are the right shape and read cleanly.

Two things need attention, and both are the same shape. First, the section states four build-time
refusals as facts of the shipped composer, and **not one of the four is discharged inside this
repository** — one was deliberately deleted from the composer with a recorded reason that inverts the
spec's own sentence, two live in a gate (`lab/sceneplan-build-check.py`) that does not exist in this
tree, and the fourth cannot fire because the code re-declares the tier instead of breaching it.
Second, the section closes the "level" confusion and leaves an identical, unclosed collision on
"role" and "tier" one paragraph later.

Confidence: **needs another iteration**. The level paragraph is ready to build against; the composer
and voice paragraphs describe a composer that is not the one shipped.

## Phase 1 — The model

**Entities.** Pass (optional composed transaction between two hung works) · Composer (reads two
ElementSets + the ordered pair's dossier, emits a ScenePlan) · ElementSet (a work's fragments along
one decompose axis, plus its complement) · ScenePlan (build-time, data-only) · Score (the serialised
wire record the host plays) · Cue (`voice`, `roles`, `levels`, `window`, `doors`, tracks) · Structural
level (six: `WORLD`, `SURFACE`, `CELL`, `CELL CONTENT`, `TEXTURE`, `LIGHT-COLOUR`) · Instrument (with
its manifest) · Pass door (`{from, to}`, each `hangGeometry` + `immersiveGeometry`).

**States and transitions of one pass.**
1. *not offered* — `visualLayer=off`; exits only to the plain `EX-GLIDE` glide.
2. *offered* — `visualLayer=on`; exits to *declined* (reduced motion, Save-Data, no WebGL2, failed
   fetch of the renderer file, a renderer throwing at registration) or to *composed*.
3. *composed* — a ScenePlan stands; exits to *refused* (the section's four build-time refusals) or to
   *serialised*.
4. *serialised* — a score stands; exits to *playing* or, on the host's own shed path, to *declined*.
5. *playing* — holds the frame; exits to a dock at the arriving work, or to *declined* mid-flight.

**Actors.** The composer (build time, automated) casts actors and voices cues. The build gate
(`lab/sceneplan-build-check.py`) judges the plan. The host (`pass-layer.js`) plays the score and owns
the decline. The instrument reads its own mask at both doors on the buffer. The visitor initiates
nothing — a pass is a consequence of a walk step.

**Composition boundary.** The composer emits the artistic request and never geometry; the instrument
owns its doors at run time; the host binds by declared manifest name. That boundary is stated and it
holds in the code.

### What I assumed

- I read "is refused" throughout the section as a claim about behaviour that exists today, because the
  surrounding prose is in the present indicative and the section says it states "what a reader of THIS
  spec must already know". If the section meant these as the target contract rather than as shipped
  behaviour, say so and F1/F2/F5 become one finding about tense instead of four about discharge.
- I treated `lab/sceneplan-build-check.py` as genuinely absent from this repository rather than
  renamed: `lab/` holds exactly one file, `beauty-score.json`.
- I read the section's silence on the pass's accessibility and analytics clauses as deliberate,
  because the section states the pass "owns none of" the exhibition's other faces and changes not one
  pixel of them. I did not file a declared-cross-cutting-law finding on that basis; see the sweep table.
- I found no authoritative surface for instrument manifests named in this document. If one exists in
  the product, the section's door-refusal sentence does not register with it.

## Phase 2–3 — Findings

| ID | Finding | kind | folded / rejected | status |
|---|---|---|---|---|
| F1 | The composer does not refuse an actor-less plan; it was removed on purpose | defect | — | open |
| F2 | Three of `INV-109`'s four build-time refusals have no enforcer in this repository | defect | — | open |
| F3 | The tier does not bound a score; the score's voices re-name the tier | defect | — | open |
| F4 | A third accompaniment voice — the colour voice — is counted by the code and named by neither document | defect | — | open |
| F5 | The camera accompaniment is counted unconditionally, where both documents say "whenever named" | defect | — | open |
| F6 | "Role" collides three ways, and the thing that actually sets the tier is never named | defect | — | open |
| F7 | A score whose duration falls in no band is exempt from the budget, unstated | defect | — | open |
| F8 | `TEST_MATRIX.md`'s PASS-02 and PASS-12 fences would red the shipped composer | recommendation · now | — | open |

---

**F1 — The composer does not refuse an actor-less plan, and its own recorded reason is the inverse of
the spec's sentence**

> "A plan is refused where no actor names any element of either work — a passage between two whole,
> uncut frames is not what a composer is for." — SPEC.md:592-593, `EX-PASS-COMPOSER`; restated in the
> index row at SPEC.md:1968 and in `INV-109` at SPEC.md:2111 ("an actor-less plan")

`pass-composer.js:4787-4790` deletes that refusal by name and records why:

> "THE ACTORS, AND THERE ARE ALWAYS SOME. What stood here was «actor refusal», which turned a work
> offering only the whole frame along the pivot's cut into no crossing at all; **the whole frame is a
> lawful element** and it is what hands over now."

`castActors` returns actors unconditionally and the plan proceeds. A visitor walking a pair whose
pivot cut no instrument can cut therefore *does* get a composed crossing between two whole frames —
exactly the passage the spec says a composer is not for. Anyone reading this section to decide whether
a pair will cross gets the wrong answer for that whole class of pairs, and anyone writing the test
`TEST_MATRIX.md` PASS-02 asks for will red the shipped composer on its first run.

Replace SPEC.md:592-593 with the decision the code actually records: "Every ordered pair composes; a
work offering only its whole frame along the pivot's cut casts that whole frame as its element, and
the plan records which cut it wanted and which it got." Strike "an actor-less plan" from `INV-109`'s
enumeration at SPEC.md:2111 and from the index row at SPEC.md:1968. If the refusal is wanted back,
that is a product decision for Alexander and a change to `pass-composer.js:4787`, not a spec edit —
his word of 2026-08-18 09:51, quoted in the composer at `:325-330`, is that any two photographs get a
crossing, which reads against the refusal.

`defect · direct-contradiction (contradiction)`

---

**F2 — Three of `INV-109`'s four build-time refusals have no enforcer anywhere in this repository**

> "…or any refusal at build time (an actor-less plan, a door the instrument's manifest leaves blank, a
> levels-law contention, a tier-budget breach) all leave `EX-GLIDE`'s one-frame glide running exactly
> as this spec states it" — SPEC.md:2111, `INV-109`

The actor-less refusal is gone (F1). The other three:

- **the levels-law contention.** `pass-layer.js:1752-1767` states the law moved out of the host on
  2026-08-14 and names its new home: "tlvphotos-sceneplan, `lab/sceneplan-build-check.py`".
  `PASS-API-V1.md:513-516` says the same and adds that the gate lives "in the tlvphotos tree on the
  branch `immersive-alpha-sceneplan`". This repo's `lab/` holds one file, `beauty-score.json`.
- **the blank-door refusal.** `PASS-API-V1.md`'s conformance row 19 places it at build time, in the
  same absent gate. `manifestWhyNo` (`pass-layer.js:342-364`) judges a manifest at registration for
  preserved buffers, missing passes, unnamed uniforms, unknown types and unsuppliable sources — it
  never reads a score's doors against the manifest. `TEST_MATRIX.md`'s PASS-14 says the same in its
  own words: "this repo's suite carries no row that names it".
- **the tier-budget breach.** See F3: `tierFor` cannot breach.

An engineer reading `INV-109` builds against a walk that is protected by four gates and is in fact
protected by none of them inside this tree. The concrete failure is a plan that owns one level twice
in overlapping windows reaching a visitor unrefused, because the only reader of `levelOwnership`
(`pass-composer.js:3866-3869`) asks whether *this* cue owns a level and never gathers a level's
holders to compare them.

Add one sentence to the section, after SPEC.md:597, naming where each refusal is enforced and that the
gate is out of tree: "Three of these refusals — the blank door, the levels contention and the tier
breach — are judged by the plan gate at build time, which lives outside this engine
(`lab/sceneplan-build-check.py`, tlvphotos tree); no engine-side code re-checks them." Then either
(a) open a queue row to bring the gate into this repo, which is my preference since the engine is the
primary and the gate guards the engine's own output, or (b) mark the three refusals `[default]` as
out-of-tree and let the tlvphotos suite own them, which is cheaper and leaves this repo's suite unable
to prove its own invariant.

`defect · unenforceable-promise (discharge)`

---

**F3 — The tier does not bound a score's voices; the voices re-name the tier**

> "The tier a pass plays at (quiet, middle, culmination) bounds how many of each a score carries on
> BOTH ends, not as a ceiling alone: a quiet-tier score carries no miracle, a middle-tier score at
> most one, and a culmination-tier score exactly one — never zero" — SPEC.md:624-627, `EX-PASS-VOICE`

The direction of causation is backwards. `tierFor` (`pass-composer.js:3407-3452`) takes the tier the
walk step reached for, counts the realised voices, and where the declared tier's row does not fit
**walks down to the highest lower-ranked row that does** (`:3432-3437`); where no row fits at all it
returns the row the counts stand *nearest*, with the counts still outside it (`:3438-3452`). The
function's own comment says so: "A crossing that reached for a culmination and made a middle is a
middle, not a refusal." Nothing is ever refused.

So "a culmination-tier score carries exactly one miracle, never zero" is true of shipped scores only
because a zero-miracle culmination is silently relabelled a middle — never because the count was
bounded. A reader who takes the sentence at face value writes the gate `TEST_MATRIX.md` PASS-12 asks
for ("a culmination score that carries none [is] red") and reds a composer that is behaving as
designed. On the nearest-row path the sentence is not true even by relabelling: the plan declares a
tier whose row its own counts fall outside, which is precisely the disagreement `PASS-API-V1.md` §4.7
calls a red — the composer can emit a plan the build gate must reject.

Rewrite SPEC.md:624-627 to state the mechanism: "A score's voices decide the tier it is declared at.
The step's route role reaches for a tier; where the realised counts do not fit that tier's row the
next lower row that fits is declared instead, and where no row fits the nearest one is. The rows are:
quiet — one letter, at most one accompaniment, no miracle; middle — at most two letters, at most two
accompaniments, at most one miracle; culmination — two or three letters, at most three
accompaniments, exactly one miracle." Then decide separately whether the nearest-row path may emit a
plan the build gate reds — my read is that it may not, and the fix is a queue row against
`pass-composer.js:3438`, not against the spec.

`defect · unenforceable-promise (discharge)`

---

**F4 — A third accompaniment voice is counted by the shipped budget and named by neither document**

> "…together with the camera's own track, which counts as one accompaniment whenever the score names
> one." — SPEC.md:626-627, `EX-PASS-VOICE`

`tierFor` adds a second uncounted accompaniment: `if (singsColour) accs += 1;`
(`pass-composer.js:3423`). `singsColour` is true when any surviving cue's instrument manifest declares
the `LIGHT-COLOUR` level (`:5203-5211`). The comment at `:3416-3422` grounds it in charter shelf 11
and shelf 17's "EVERYTHING counts". The string `singsColour` appears nowhere in
`docs/design/PASS-API-V1.md`, and §4.4's budget paragraph (`:520-533`) enumerates the cues and the
camera and stops.

Consequence: anyone — a person or a later session — computing a score's accompaniment count from
either document gets a number one lower than the composer's whenever a colour instrument is cast. At
the middle tier's ceiling of two accompaniments that is the difference between a plan that fits its
row and one that is walked down a tier, which changes the passage's duration band and so the length
the visitor actually sees.

Add the colour voice to SPEC.md:626-627: "…together with two voices that are not cues — the camera's
own track, and the colour voice, counted once when any cast instrument's manifest declares
`LIGHT-COLOUR`." Add the same sentence to `PASS-API-V1.md` §4.4 beside the camera amendment, so the
contract and the spec agree.

`defect · missing-rule (invariant)`

---

**F5 — The camera accompaniment is counted unconditionally, where the spec and the contract both make
it conditional**

> "…the camera's own track, which counts as one accompaniment whenever the score names one." —
> SPEC.md:626-627; and "with the camera counted as one accompaniment wherever the score names a camera
> track" — `PASS-API-V1.md`, conformance row 18

`tierFor` seeds `accs = 1` before it looks at anything (`pass-composer.js:3410-3411`), with the
comment "`accs` SEEDS AT 1 FOR THE CAMERA, deliberately". No camera is consulted. `serialise`
(`:8752-8755`) builds `camera` from `plan.camera || {}` filtered through `CAMERA_ALLOWED`, so a plan
carrying no camera serialises `camera: {}` — a score naming no camera track, whose budget was
nonetheless charged one accompaniment.

Whether this bites today depends on whether every composed plan carries a camera; I did not find a
guarantee that it does, and the conditional is written into both documents, so the code and the
documents disagree either way. If every plan does carry a camera, the conditional is dead prose that
will mislead the first person who composes a camera-less plan.

Pick one and make all three agree. Either (a) drop the condition from SPEC.md:626-627 and
`PASS-API-V1.md` row 18 — "the camera's own track always counts as one accompaniment" — which matches
the shipped code and is my preference if every plan carries a camera; or (b) gate `tierFor`'s seed on
the camera record being non-empty, which matches the documents and is the right answer if a camera-less
plan is legal. Answering this needs one fact I could not settle from the code: is a plan with no
camera lawful?

`defect · internal-conflict (consistency)`

---

**F6 — The section closes the "level" collision and leaves an identical "role" collision one
paragraph later**

> "'Level' names three different questions, and answering one with another is the exact defect this
> paragraph closes." — SPEC.md:602-603
>
> "`roles` asks a different question — what a cue does dramatically inside the pass, drawn from a set
> of nine named roles" — SPEC.md:627-629

The section names two senses of "role" (a cue's nine dramatic roles; and, by implication, none other)
and one unexplained "tier a pass plays at". There is a third sense in the shipped code, and it is the
one that matters most: the **walk step's route role**, `ROUTE_ROLES = ["entrance", "quiet link",
"middle", "culmination", "return"]` (`pass-composer.js:9083`). It is passed into `voiceTheCues` as
`role` (`:3364`), and `role === "culmination"` is what makes a pass a culmination
(`:3369`, `:5288`). Three of its five values are spelled the same as the three tier names, and the
composer's own comment at `:3357-3363` says "THE STEP'S ROLE NAMES THE TIER, and nothing else does."

So the section states what a tier bounds without ever stating what chooses a tier, and the thing that
chooses it shares a word with the nine dramatic roles and shares its values with the tier names. This
is the same defect the level paragraph was written to close, left open on the neighbouring concept.
The reader who has to hold "level ×3" straight is handed "role ×2 + tier" with no help at all.

Add a fourth paragraph to the section, in the shape of the level paragraph: "'Role' names two
different questions on a pass. A **route role** is what the walk's own step is — entrance, quiet link,
middle, culmination or return — and the step's route role is what a pass reaches for as its tier, and
nothing else is. A **cue role** is what one cue does dramatically inside the pass, drawn from a set of
nine. A step's route role and a cue's dramatic role share the word and share nothing else." Then
amend SPEC.md:624 to open "The tier a pass reaches for is its step's route role" rather than leaving
the tier's source unstated.

`defect · confusing-for-users (cognitive-load)`

---

**F7 — A score whose duration falls in no tier band is exempt from the budget, and the section states
the budget without the exemption**

> "The tier a pass plays at (quiet, middle, culmination) bounds how many of each a score carries on
> BOTH ends" — SPEC.md:624-625

The host's budget is keyed on duration, not on the declared tier: `TIERS` in `pass-layer.js:1779-1786`
carries `lo`/`hi` seconds per row (2–4, 5–8, 9–14), and the comment above it at `:1776-1778` states
the exemption in as many words — "A duration falling in NO band names no tier, and the budget then
stands aside with that reason recorded. §2.5 makes `duration: 0` a legal instant transition and the
bands leave gaps between them, so a score outside every band is a score the tier rules say nothing
about." A legal instant transition is reachable from the composer's own serialiser: `planDurationMs`
returns `null` for a plan with no duration and no cue windows, and `serialise` writes `duration = 0`
(`pass-composer.js:8737-8746`). The gaps between bands (4–5 s, 8–9 s) are reachable too, since the
composer fits a length inside a band by a reading of the pair (`:5214-5232`).

An operator reading this section believes every played score was budget-checked. In fact an instant
transition, and any score landing in a between-bands gap, plays with the budget standing aside — so
the "never zero miracles at a culmination" property the section states as absolute has a silent hole
the diagnostic surface records and the spec does not mention.

Add the exemption to SPEC.md after :627: "The budget is read against the score's own duration, and a
duration falling in no tier's band — the legal instant transition among them — leaves the budget
standing aside, with that reason recorded on the diagnostic surface."

`defect · missing-scenario (state-space)`

---

**F8 — Two `TEST_MATRIX.md` rows project sentences that are false of the shipped composer, so writing
them reds working code**

> "A composed ScenePlan names at least one actor drawn from A's own ElementSet and at least one from
> B's. / Never: A plan whose every actor is a whole, uncut frame is never turned into a playable
> score" — `TEST_MATRIX.md`, PASS-02
>
> "Never: A composed score never exceeds its own tier's miracle bound in either direction (a `quiet`
> score that carries one, or a `culmination` score that carries none, are both red)" — PASS-12

Both fences project spec sentences this pass finds false (F1, F3). PASS-02 is marked "Declared and
unbuilt", so no one has run it yet; PASS-12 claims partial coverage by `test_pass_lawful.py`'s R1. The
person who picks up either row next writes a test against a composer that deliberately behaves the
other way, and spends the session deciding whether the code or the test is wrong.

Hold both rows until F1 and F3 are folded, then re-derive them from the corrected sentences rather
than editing the fences in place — the matrix is a projection and it should be re-projected, not
patched. This is a recommendation rather than a defect because the rows block nothing today and the
fix is downstream of the spec edits.

`recommendation · now · internal-conflict (consistency)`

## Phase 3.5 — Acknowledged gaps

The section itself flags none — no Open Item, no TBD, no unanswered rhetorical question, no
in-progress marker. Its neighbouring artifacts flag two, and both are already named honestly there
rather than hidden: `TEST_MATRIX.md` states that no architecture node owns
`engine/assets/pass-composer.js` or any `pass-inst-*.js`, and that eight of its fourteen rows are
"declared and unbuilt". Neither is a finding of this pass; both are the author's own known issues,
carried here so a later session does not re-file them.

`acknowledged · hard-to-operate (ops-ux)`

## Phase 3e — Mandatory sweep verdicts

One verdict per sweep. The section registers one surface, the pass, so the table is one row.

| Surface | Declared cross-cutting laws | Edge-condition completeness | Cross-surface policy uniformity | Lifecycle | Unwritten seams |
|---|---|---|---|---|---|
| The pass (`EX-PASS`) | N/A — `SPEC.md` keeps no declared-laws home naming its cross-cutting laws with their nets; the pass section is not the place to open one, and the gap belongs to a FULL pass over `SPEC.md` | hit — F7 (a duration in no band is an unanswered range gap; the section names the budget without its own exemption) | clean — the pass declares itself subordinate to every sibling surface and changing no pixel of them (`SPEC.md:575-578`), and that policy is stated over the whole enumerated set rather than one member | clean — the pass's own enter / play / decline / dock lifecycle is stated, and re-entry is the next walk step, which `EX-GLIDE` owns | hit — F2 (the refusals' enforcement seam between this engine and the out-of-tree plan gate is unwritten) |

Quantifier re-verify, run over the whole document as the mode requires. Four universals in the new
section were checked against the surface set that now includes the pass: "owns none of the door, the
story, …" (`:575-578`) — the enumeration is complete against `SPEC.md`'s own section list at :213–:1633,
with no surface omitted; "never zero" (`:626`) — falsified, F3; "whenever the score names one"
(`:627`) — falsified, F5; "no expression, no function and no executable string" (`:597`) — holds,
`serialise` (`pass-composer.js:8746-8770`) copies only data fields through a closed key filter.
`INV-109`'s four-member refusal list (`:2111`) is the fifth, falsified by F1 and F2.

Class lens: swept — one class filed, **"a build-time refusal stated as a fact of the shipped composer
with no enforcer in this tree"**. Four instances, and they are exactly `INV-109`'s four members: the
actor-less plan (F1, deleted from the composer on purpose), the blank door (F2, absent gate), the
levels contention (F2, absent gate), the tier breach (F3, structurally cannot fire). The class is
filed once as F1+F2+F3 rather than as four point findings. Its architectural cause is real and named
in F2: the plan gate that discharges three of the four lives outside the repository whose spec
promises them, and no node in `ARCHITECTURE.md` owns the pass layer to have caught it.

## Phase 4 — Human and operational factors

Domain language: the section's visible vocabulary is the product's own — pass, composer, pivot, actor,
middle, cue, voice, door. No internal identifier leaks into prose a person reads. `levelOwnership`,
`hangGeometry` and `immersiveGeometry` appear as backticked field names inside a contract sentence,
which is the right register for a spec and not user-facing text.

Observability: the section names the diagnostic surface nowhere, though `PASS-API-V1.md` §9 owns it
and the code records declines, strips, sheds and budget stand-asides on it. An operator reading this
section alone does not learn that a decline, a strip or a budget exemption is visible anywhere. One
sentence pointing at §9's diagnostic surface would close it. Filed as an observation rather than a
finding, since the section explicitly delegates its full contract to that document.

Scale: no ceiling is stated for the number of cues, actors or elements a plan may carry, and none is
needed at the composer's shipped vocabulary of three cues (`CUE_IDS`, `pass-composer.js:235`). The
score's own byte fence (`SCORE_FENCE_BYTES`, `:8775-8800`) is the real ceiling and it sheds prose
before pictures, which is the right order.

Security and privacy: genuinely out of scope. A score carries no visitor data, and "no expression, no
function and no executable string" (`:597`) is the one security-shaped claim, verified above.

## Phase 5 — Closing summary

**Top three to fix before anything is built against this section.**
1. F1 — the actor-less refusal the section states does not exist and was deleted on purpose; the
   spec's sentence and `INV-109`'s enumeration both have to change.
2. F3 — the tier does not bound a score; state the walk-down mechanism instead, and decide separately
   whether the nearest-row path may emit a plan the build gate reds.
3. F2 — say where the three out-of-tree refusals are enforced, or bring the gate into this repo.

**Properties the section should state explicitly.** Paste-ready:
- "Every ordered pair composes; a work offering only its whole frame along the pivot's cut casts that
  whole frame as its element."
- "A score's realised voices decide the tier it is declared at; the step's route role is only what it
  reaches for."
- "The accompaniment count is the accompaniment-voiced cues plus the camera's track plus the colour
  voice, counted once when any cast instrument declares `LIGHT-COLOUR`."
- "A duration falling in no tier band leaves the budget standing aside, with that reason recorded."
- "A step's route role and a cue's dramatic role share the word and share nothing else."

**Open questions — the two I could not settle by inspection.**
1. Is a plan with no camera record lawful? F5's fix depends on it, and only the pass's author knows.
2. Were the four refusals in `INV-109` written as the target contract or as shipped behaviour? If
   target, the fix is one tense change plus a `[target]` marker rather than four rewrites.

**Queued for a taste call.** F8 alone.

**`[default]` census.** The new section carries no `[default]`-tagged sentence — zero, so no oldest-five
list. That is itself worth a glance: a section this size that answered every question it raised with a
decided sentence and never once tagged a value as retunable is either unusually well settled or has
values in it nobody has been asked to approve. F5's camera condition and F3's nearest-row behaviour
are the two I would expect to have been tagged.

## Verdict

**NEEDS ANOTHER ITERATION.** Six defects, one recommendation, one class swept. The level paragraph —
the confusion this section was written to close — is correct and ready to build against. The composer
and voice paragraphs describe a composer that is not the one shipped, and `INV-109` promises four
gates this repository does not hold. No finding is folded; every row above is open.
