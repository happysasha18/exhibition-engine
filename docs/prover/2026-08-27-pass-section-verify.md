# Prover — verification of `docs/prover/2026-08-27-pass-section.md`'s folds (2026-08-27)

Prover skill version: live-spec pack `product-prover`, base `live-spec-base` v4.3.0.

Mode: a narrow verification pass, not a re-review. It re-reads only the corrected section body
(`SPEC.md:569-669`), its own index rows (`SPEC.md:1937-1951`, `:1998-2003`), `INV-109`
(`SPEC.md:2143`), and the touched paragraphs of `docs/design/PASS-API-V1.md` §4.4 and its conformance
rows 18 and 19. Every claim below is checked against `engine/assets/pass-composer.js`,
`engine/assets/pass-layer.js`, `tests/test_pass_lawful.py` and the out-of-tree gate, by `file:line`.
The rest of `SPEC.md` was read for contradiction against the folded sentences only.

Reviewer hat: formal-methods. This seat authored neither the section nor its corrections.

**What this pass verifies.** The first record (`2026-08-27-pass-section.md`) filed F1–F8. A follow-up
session folded F1–F7 into `SPEC.md` and `docs/design/PASS-API-V1.md`, and while re-reading its own
work caught a third issue in `EX-PASS-DOOR` on its own initiative. This pass re-derives each fold
from primary sources rather than from the follow-up's account of it. Findings continue the first
record's numbering, so `F1`–`F8` keep their meaning and this pass opens at `F9`.

## Phase 0 — Triage

`TRIAGE: PROCEED`. The corrected section is still operational product prose with entities, states and
stated refusals.

The section still claims a shipped system in the present tense, and `ARCHITECTURE.md` still carries no
node for `engine/assets/pass-composer.js` or `pass-layer.js`. Every verdict below therefore rests on
the code and on a green suite run, never on the document's own word — including the code's own
comments, three of which turned out to state the opposite of what the code beside them does.

One source the first pass could not reach is reachable now: the out-of-tree plan gate. It was read
directly, at `/Users/sashaabramovich/tlvphotos-sceneplan` (a worktree of the tlvphotos repository
standing on branch `immersive-alpha-sceneplan`), together with `lab/sceneplan-check.py` beside it.

## Opening assessment

Four of the seven folds hold. The camera's unconditional count (F5), the row table and the first two
steps of the tier chain (F3), the route-role / cue-role split and its unstated-role default (F6), and
the duration bands with `duration: 0` inside them (F7) all match the code exactly, and the
`EX-PASS-DOOR` fix the follow-up made on its own initiative is right — `manifestWhyNo` genuinely
judges at registration and never reads a score's doors.

Three folds are wrong, and each is wrong in the same way: a sentence was rewritten to match one
reader of the law while the other readers of that law went unread. F1's fix struck the actor refusal
from `SPEC.md` while it still stands in `PASS-API-V1.md` §4.7, in its conformance row 35, in
`TEST_MATRIX.md`, and in both tlvphotos gates. F2's fix named a real gate at a real path on a real
branch — and that gate carries no blank-door row, while it does carry the actor refusal F1 just
deleted, and it judges a different composer's plans entirely. F4's fix wrote the colour voice's
condition as the instrument's manifest, where the code reads the surviving cast's own levels and this
repository's own green test already reads it correctly.

Confidence: **needs a third pass.** The section is closer than it was, and the remaining defects are
now concentrated in one place — the enforcement story `INV-109` tells.

## Phase 1 — The model, as the corrections leave it

The entities and the pass's own lifecycle are unchanged from the first record; nothing in the fold
moved a state or a transition. One actor changed, and it is where most of this pass's findings live.

**The build gate, split in two.** The first record modelled one absent gate. There are two, both
present, both in `lab/` on branch `immersive-alpha-sceneplan`:

- `lab/sceneplan-build-check.py` — the builder's own check. Twenty-three rows. It carries the actor
  refusal (`:111-141`), the levels contention (`:143-183`) and the tier agreement (`:186-206`).
- `lab/sceneplan-check.py` — the score-side gate. It carries the blank-door refusal (`:603-609`), and
  restates the actor refusal (row 35), the tier agreement (row 36) and the levels law (row 37).

**What those gates read.** Both expand `lab/build-sceneplan-v1.py`'s own table rows into plans
(`sceneplan-build-check.py:99-109`, `plans[key] = B.fill_plan(key, rows[key], templates, table)`).
Neither tree holds `pass-composer.js` or `pass-layer.js` — `git ls-files` in the sceneplan worktree
returns nothing for either name. The gates judge a Python builder's plan corpus. They have never seen
this engine's composed plans.

### What I assumed

- I read `SPEC.md:601-603` ("the refusals a composed plan can still meet … are all judged by the plan
  gate") as a claim about a plan composed by `EX-PASS-COMPOSER`, this engine's composer, because that
  is the paragraph the sentence sits in and the entity it names. If it was meant as a claim about the
  tlvphotos builder's plans instead, F10 and F11 collapse into one sentence about which composer the
  paragraph is describing — but then the section states no enforcement at all for the composer it is
  actually about, which is a larger gap rather than a smaller one.
- I treated the two worktrees `~/tlvphotos-sceneplan` (on `immersive-alpha-sceneplan`) and
  `~/tlvphotos` (on `wip/2026-08-06-darkroom`) as one repository. `git ls-tree -r immersive-alpha-sceneplan`
  from `~/tlvphotos` lists `lab/sceneplan-build-check.py`, so the citation's path and branch are
  confirmed from the main clone as well as from the worktree.
- I could not settle whether the nearest-row branch of `tierFor` is reachable on the product path.
  The budget loop (`pass-composer.js:5050-5172`) constrains letters, accompaniments and tier rank
  before `tierFor` is ever called, and every construction I tried ended at a fitting row. F13 is filed
  on the contradiction between two sentences rather than on a witness, and it says so.
- I read the section's silence on accessibility and analytics as deliberate, on the same ground the
  first record gave.

## Phase 2–3 — Findings

| ID | Finding | kind | folded / rejected | status |
|---|---|---|---|---|
| F9 | The actor refusal F1 struck from `SPEC.md` still stands in the contract, the matrix and both gates | defect | — | open |
| F10 | The blank-door refusal is attributed to a gate that carries no such row | defect | — | open |
| F11 | The named gate judges another composer's plans; nothing judges this engine's | defect | — | open |
| F12 | `INV-109` says this repository's suite proves none of the three; `test_pass_lawful.py` R1 proves one, green today | defect | — | open |
| F13 | `INV-109` says a tier is never breached; `EX-PASS-VOICE` says the counts stand outside the declared row | defect | — | open |
| F14 | The colour voice's condition is the manifest in both documents and the surviving cast's own levels in the code | defect | — | open |
| F15 | "counts in every one of those sums" is true of one of the three readers of the budget | defect | — | open |
| F16 | `EX-PASS-ROLE`'s "and nothing else is" is false — the pair's own shape picks the tier a pass reaches for | defect | — | open |
| F17 | The no-band exemption's recorded reason is not always the no-band one | recommendation · now | — | open |

Verified clean, and named here so a third pass does not re-derive them: F5 (the camera counts
unconditionally, and every composed score really does carry a camera record), F3's row table and its
first two branches, F6's route-role vocabulary and its unstated-role default, F7's bands and
`duration: 0`, and the follow-up's own `EX-PASS-DOOR` fix. Each is worked below the findings.

---

**F9 — The actor refusal F1 struck from `SPEC.md` still stands in the contract, in the matrix, and in
both of the gates F2's fix just named as the authority**

> "Every ordered pair composes: a work that offers only its whole frame along the pivot's cut casts
> that whole frame as its element… No pair is refused for the elements it could not be cut into." —
> SPEC.md:592-595; and "The build-time refusals are three, and none is the composer's" — SPEC.md:2143,
> `INV-109`

The fold is right about this engine. `castActors` (`pass-composer.js:3176-3237`) returns actors
unconditionally, `compose` has exactly one `return` and it is never null (`:5312`), and the deleted
refusal's own note stands at `:4787-4790`. That half is verified.

But the sentence's twin was never folded, and it stands in four other places:

- `PASS-API-V1.md:1087-1091` — "**A ScenePlan is refused when no actor names any element of either
  work — when every actor is a whole frame.** A plan must name at least one actor drawn from A's
  ElementSet and at least one drawn from B's." That document is the one `SPEC.md:580-582` names as the
  pass's full contract and "the live record of what stands built".
- `PASS-API-V1.md:1680-1681`, conformance row 35, which carries it in the person's own naming.
- `TEST_MATRIX.md:61`, whose `refused-at-build` state still enumerates four sub-states opening with
  "actor-less plan", against `INV-109`'s new three; and PASS-02, whose Never-clause still fences it.
- Both out-of-tree gates. `lab/sceneplan-build-check.py:111-141` reds
  `"<key> draws only whole frames from work <side>"`, and its own docstring (`:13`) names the actor
  refusal as the first of the four rules it owns. `lab/sceneplan-check.py:23-27` carries the same as
  its row 35.

So the composer now emits, by design, exactly the plan the gate the spec names as its own authority
reds. An engineer wiring this engine's composer into the tlvphotos build takes a pair whose pivot cut
no instrument can cut, gets a lawful plan by `SPEC.md:592`, and watches
`python3 lab/sceneplan-build-check.py` exit 1 naming that pair — with `SPEC.md` and `PASS-API-V1.md`
telling him opposite things about which of the two is wrong.

Fold F1 across the contract in the same landing. Strike `PASS-API-V1.md:1087-1091` and rewrite
conformance row 35 to the decision the composer records, cite `pass-composer.js:4787-4790` beside it
as `SPEC.md:592-595` now does, and cut `TEST_MATRIX.md:61`'s fourth sub-state. Then the gates: either
(a) delete the actor row from both gate scripts, which is the answer if the composer's recorded
decision is the product's, and it is a change in the tlvphotos tree that this repository can only
request; or (b) keep the gates and say in `SPEC.md` that a plan lawful for this composer can still be
refused downstream, which reads to me as the wrong answer because it re-opens the refusal the
2026-08-18 09:51 word closed. My preference is (a), and either way the four unfolded homes above have
to move.

`defect · direct-contradiction (contradiction)`

---

**F10 — The blank-door refusal is pinned to a gate that carries no such row; it lives in the gate's
neighbour**

> "The refusals a composed plan can still meet — a door the instrument's manifest leaves blank, a
> levels-law contention, and a declared tier its own voices contradict — are all judged by the plan
> gate at build time, and that gate lives outside this engine (`lab/sceneplan-build-check.py`…)" —
> SPEC.md:599-602; restated at `SPEC.md:1999`, `:2003`, and in `INV-109` at `:2143`; and
> `PASS-API-V1.md` conformance row 19

The citation is real: `lab/sceneplan-build-check.py` exists on branch `immersive-alpha-sceneplan`, and
two of the three refusals are genuinely its rows — the levels contention at `:143-183` ("two cues
sharing a level in overlapping windows: one accompanies the other") and the tier agreement at
`:186-206`. That much of F2's fix is verified.

The blank door is not among its twenty-three rows. Its only manifest-shaped row is `:379-394`, which
asks that every handle a template *tracks* is published and that open handles are left alone — a
different question. The blank-door refusal is in the file beside it: `lab/sceneplan-check.py:603-609`
reads each cue's `doors` entry against `manifest.dial.doors` and reds a value the manifest does not
publish. That file's own header (`:6-9`) draws the boundary: `sceneplan-build-check.py` judges the
builder's build, and `sceneplan-check.py` judges the score a stranger would read.

Anyone following `SPEC.md:602` to see how a blank door is caught opens the wrong file, finds nothing,
and concludes the refusal is unenforced — which is what the first record concluded, and it was half
right for the wrong reason.

Split the citation. `SPEC.md:599-603` should read: "…a levels-law contention and a declared tier its
own voices contradict are judged by `lab/sceneplan-build-check.py`, and a door the instrument's
manifest leaves blank by `lab/sceneplan-check.py` beside it — both in the tlvphotos tree on branch
`immersive-alpha-sceneplan`." Carry the same split into the two index rows (`:1999`, `:2003`) and into
`INV-109` (`:2143`).

`defect · unenforceable-promise (discharge)`

---

**F11 — The gate the section names judges a different composer's plans, so nothing judges the plans
`EX-PASS-COMPOSER` actually emits**

> "No engine-side code re-checks them, so this repository states the law and another tree enforces
> it." — SPEC.md:603

The first clause is true and I verified it: `scoreWhyNo` (`pass-layer.js:1904-1963`) refuses a cycle,
two camera authorities, a led flight claiming the world, one instrument on two cues and a coverage
break, and its closing note (`:1956-1962`) states in as many words that "THE TIER BUDGET IS RECKONED
AND RECORDED, AND IT REFUSES NOTHING"; the levels law's move out is recorded at `:1752-1767`; and
`manifestWhyNo` never reads a score's doors (F-clean, below).

The second clause does not follow. Both gates build their plan corpus from
`lab/build-sceneplan-v1.py`'s table (`sceneplan-build-check.py:99-109`,
`plans[key] = B.fill_plan(key, rows[key], templates, table)`), and neither tlvphotos worktree carries
`pass-composer.js` or `pass-layer.js` at all. The engine's own road is
`compose` → `fillPlan` → `serialise` → the score → the host, and no gate stands anywhere on it.

The operational consequence is the one the first record named and the fold was meant to close, and it
is still live. A plan that owns one level twice in overlapping windows reaches a visitor unrefused:
the only engine-side reader of `levelOwnership` (`pass-composer.js:3866-3869`) asks whether *this* cue
owns a level and never gathers a level's holders, and the gate that does gather them
(`sceneplan-build-check.py:161-181`) is looking at a different corpus. An operator reading
`SPEC.md:603` believes another tree is watching. Nothing is.

Say what is true, and open the row that fixes it. `SPEC.md:603` should read: "No engine-side code
re-checks them, and the out-of-tree gate reads the tlvphotos builder's own plans rather than this
composer's, so no gate today stands on the road a composed score actually travels." Then open a queue
row to put one there — my preference is to port the three rows into this repository's suite beside
`tests/test_pass_lawful.py`, which already proves the tier agreement over every composed passage (F12)
and is therefore the cheapest of the three to complete.

`defect · unenforceable-promise (discharge)`

---

**F12 — `INV-109` says this repository's suite proves none of the three refusals; one of them it
proves today, and the row is green**

> "…all three judged by the plan gate that lives outside this engine…, so this repository's own suite
> proves none of them" — SPEC.md:2143, `INV-109`

`tests/test_pass_lawful.py` R1 asks exactly the tier question of every composed passage: it walks the
built fixtures and eight real works, both directions, all five route roles, calls
`composer.passageFor` and reds on any plan whose declared tier its own score's counts do not satisfy
(`:270-297`, the row at `:425-445`). It is not a sample and not a tally — it names one witness or
none. `python3 tests/test_pass_lawful.py` reports `16 pass, 0 fail, 0 skip`, R1 among them.

So the sentence is false on the third refusal, and it is false in the direction that costs most: a
later session reading `INV-109` deletes or skips the only row this repository holds over the pass
budget, on the document's own word that it proves nothing.

There is a second, sharper reading in that same test. `countsOf` (`:237-247`) counts the colour voice
off `c.levels` — the score's own cue levels — rather than off the instrument's manifest. That is the
correct reading, and it is the one both documents now get wrong (F14).

Rewrite the clause: "…so this repository's suite proves the tier agreement alone
(`tests/test_pass_lawful.py` R1, over every composed passage), and neither the blank door nor the
levels contention." Then reconcile `TEST_MATRIX.md` PASS-12, which still describes R1 as covering the
budget "generically", and PASS-14, which still reads "declared; this repo's suite carries no row that
names it" — true for the door, and now to be re-pinned at `lab/sceneplan-check.py:603-609` rather than
at nothing.

`defect · direct-contradiction (contradiction)`

---

**F13 — `INV-109` says a tier that does not fit is re-declared rather than breached; `EX-PASS-VOICE`
says the counts stand outside the row it declares**

> "a tier that does not fit its counts is re-declared rather than breached (`EX-PASS-VOICE`)" —
> SPEC.md:2143
>
> "where no row fits at all, the row the counts stand NEAREST is declared and the counts stand where
> they are, outside it" — SPEC.md:636-637, `EX-PASS-VOICE`

Both sentences landed in one fold, and they cannot both hold. A plan whose counts stand outside the
row it declares is precisely the breach `PASS-API-V1.md:1080-1082` calls a red ("The declared tier and
the measured one must agree… Neither value silently wins") and precisely what
`sceneplan-build-check.py:197-199` and `test_pass_lawful.py` R1 both test for. `INV-109` promises that
state is unreachable; `EX-PASS-VOICE` describes the branch that reaches it.

The chain itself is otherwise exact, and I verified each link. The three rows at `SPEC.md:632-634`
match `TIERS` (`pass-composer.js:333-345`) bound for bound. "The row the step reached for is tried
first" is `:3430-3431`. "The highest lower row that does fit" is `:3432-3437` — the loop walks `TIERS`
downward from its top and takes the first row of strictly lower rank that fits, which is the highest
such row, given `TIER_RANK` is built from `TIERS`' own ascending order (`:349-353`). The nearest-row
arithmetic is `:3444-3452`.

Two smaller inaccuracies ride in the same sentence, and the fix should take them together. The third
branch's guard is not "where no row fits at all" — the second loop only ever considers rows of
*lower* rank, so the branch also fires where a higher row fits and none below does. And where a row
does fit, its miss is zero and the nearest-row search returns it, so "the counts stand where they are,
outside it" is false on that path.

I could not build a witness that reaches the third branch: the budget loop
(`pass-composer.js:5050-5172`) holds letters under the role's own bound, accompaniments under the
declared row's ceiling, and the realised tier at or under the role's, and every shape I traced ended
at a fitting row. So the branch may be dead code the spec is now documenting as behaviour. Decide it
one way: either (a) `tierFor`'s third branch is unreachable, in which case strike `SPEC.md:636-637`
entirely and keep `INV-109`'s sentence, which is my preference and also removes the contradiction
without a code change; or (b) it is reachable, in which case keep the sentence, fix its guard to "where
neither that row nor any lower one fits", and strike "re-declared rather than breached" from
`INV-109` — and then the composer can emit a plan the gate must red, which is a defect against
`pass-composer.js:3444`, not against the spec. Answering this needs one fact I could not settle:
is there any cast for which the budget loop exits at `:5171`'s bare `break` with counts no row takes?

`defect · internal-conflict (consistency)`

---

**F14 — The colour voice's condition is the instrument's manifest in both documents and the surviving
cast's own levels in the code, and a crossing that stands the voice down is counted one too many**

> "…and the colour voice, counted once wherever any cast instrument's manifest declares the
> `LIGHT-COLOUR` level, however many of them declare it." — SPEC.md:640-641; the same words at
> `SPEC.md:2001` and in `PASS-API-V1.md` §4.4's new paragraph and conformance row 18

The count is right; the condition is not. `singsColour` is read under a guard the documents do not
carry: `for (i = 0; colourVoice && i < stackOrder.length; i++)` (`pass-composer.js:5203-5211`). Where
the budget loop has already given the colour voice up to hold shelf 17's accompaniment ceiling —
`colourVoice = !(singsHere && accs + 1 > accCeiling)` at `:5115` — `singsColour` is false and
`tierFor` adds nothing, even though the instrument is cast and its manifest declares the level. The
level is then stripped from every cue's `levels` list on the score (`:3971-3974`).

That stand-down is reachable on the plainest crossing there is. A quiet-tier plan has one cue and
`accCeiling` 1 (`ceilingOfTier`, `:4406-4414`), `accs` seeds at 1 for the camera, so a pivot
instrument declaring `LIGHT-COLOUR` trips `1 + 1 > 1` and the voice stands down. A middle-tier plan
standing at its ceiling of two does the same.

Anyone computing a score's accompaniment count from either document gets one more than the composer
on every such crossing — the same error the first record's F4 found in the other direction, now
re-introduced with the opposite sign. This repository's own test already reads it correctly, off the
score's cue levels (`tests/test_pass_lawful.py:237-247`), so the documents disagree with a green row
in the suite.

Rewrite `SPEC.md:640-641`, `SPEC.md:2001` and `PASS-API-V1.md`'s new paragraph to the code's own
condition: "…and the colour voice, counted once wherever a cue that survives the cast still claims
the `LIGHT-COLOUR` level — a crossing that gave the voice up to hold its accompaniment ceiling claims
it nowhere, and counts nothing for it." Note that this makes the condition readable off the score
alone, which is what lets a checker discharge it.

`defect · direct-contradiction (contradiction)`

---

**F15 — "counts in every one of those sums" is true of exactly one of the three readers of the tier
budget**

> "Two voices that are not cues count in every one of those sums: the camera's own track… and the
> colour voice…" — SPEC.md:638-641; and conformance row 18, `PASS-API-V1.md:1647-1651`

Three things read the tier budget, and only the composer counts a colour voice.

- The composer's `tierFor` counts it (`pass-composer.js:3423`), under F14's real condition.
- The host's `budgetOfScore` (`pass-layer.js:1819-1872`) counts letters, accompaniments and miracles
  off the cues, adds one for the camera where a track stands (`:1832-1835`), and never mentions
  `LIGHT-COLOUR` — the string appears nowhere in that file.
- Both out-of-tree gates count `accompaniment` cues plus one for the camera and stop
  (`sceneplan-build-check.py:191`; `sceneplan-check.py:690-703`). Neither names `LIGHT-COLOUR` at all.

Conformance row 18 is the sharper half. That row is the contract's statement of what the gate
enforces, and it now demands a count the gate does not take. Today the disagreement bites nothing,
because every row's accompaniment floor is 0 (`pass-composer.js:333-345`), so dropping one
accompaniment can never fall out of a row's bottom. The day a floor is raised, the gate and the
composer disagree by one on every colour-singing crossing.

State which reader each sentence is about. `SPEC.md:638-641` should open "Two voices that are not cues
count in the composer's own sum:" and add one sentence naming that the host's reckoning and the
build gate both count the camera alone. In `PASS-API-V1.md` row 18, either drop the colour clause —
my preference, because a conformance row should describe what its checker checks — or open a queue row
against the two gate scripts to add it, which is a change in the tlvphotos tree.

`defect · internal-conflict (consistency)`

---

**F16 — `EX-PASS-ROLE` is right that route role and cue role share only a word, and wrong that the
route role alone names the tier**

> "a step's route role is what its pass reaches for as a tier, and nothing else is" — SPEC.md:651-652,
> `EX-PASS-ROLE`; restated at `SPEC.md:1948-1951` and `:2002`

The paragraph's own job is done well, and I want to say so before the finding. It does not repeat the
"level" conflation on "role": `ROUTE_ROLES` is enumerated exactly as `pass-composer.js:9083` holds it,
the cue role's nine are the contract's own nine (`PASS-API-V1.md:1010-1012`), and the two are held
apart by their questions rather than by their names. The unstated-role default is verified twice —
`passageFor` at `:9128` (`req.routeRole` absent reads `"middle"`) and `scoreFor` at `:8881`
(`ROLE_BUDGETS[role] ? role : "middle"`).

"And nothing else is" is the false clause. The tier a pass reaches for is `voiceTheCues`' second
return value (`pass-composer.js:3389-3391`):

```
var tier = culmination ? "culmination"
  : ((!(hasTravel || hasArrival) && !folds) ? "quiet" : "middle");
```

with `culmination = !!(world || folds) && hasArrival && role === "culmination"` (`:3369`). The route
role gates the culmination and nothing more; between quiet and middle the choice is made by the pair's
own shape — whether a travelling move or an arrival was cast, and whether anything folds. And the
role's other function is a ceiling, not a naming: `ROLE_BUDGETS` (`:4391-4397`) maps each route role to
a top tier, and the budget loop holds the realised tier at or under it
(`TIER_RANK[tier] <= TIER_RANK[roleBudget.tier]`, `:5119`).

So a step the walk calls a culmination, on a pair whose cast folds nothing and opens no world, reaches
for a middle. A reader who takes the sentence at face value writes the obvious check — a `culmination`
step declares a `culmination` tier — and reds a composer behaving exactly as designed. The composer's
own comment at `:3357-3363` says the same false thing, which is presumably where the sentence came
from; the code three lines below it says otherwise.

Rewrite `SPEC.md:651-652`: "…and a step's route role sets the ceiling of the tier its pass may reach
for and is the only thing that opens the culmination; between a quiet and a middle the pair's own cast
decides, by whether a travelling move or an arrival stands and whether anything folds." Carry the same
correction into the glossary line at `:1948-1951` and the index row at `:2002`, and into
`SPEC.md:631-632`, which still reads "the step's route role (below) is only what the crossing reaches
for".

`defect · direct-contradiction (contradiction)`

---

**F17 — The no-band exemption is real, and the reason it records is not always the one the section
names**

> "…a duration falling in no tier's band — the legal instant transition at `duration: 0` among them,
> and the gaps the three bands leave between them — leaves the budget standing aside, with that reason
> recorded on the diagnostic surface." — SPEC.md:641-645

The exemption itself is verified. `budgetOfScore`'s `TIERS` (`pass-layer.js:1780-1787`) carries
`lo`/`hi` of 2–4, 5–8 and 9–14 seconds, the band lookup at `:1838-1841` leaves `tier` null outside
them, and `whyNoTier` is written at `:1853-1857`. `duration: 0` survives to the lookup because
`DURATION_MIN` is 0 (`:41`), so the clamp at `:1821` does not lift it into a band.

Two details are off. The held-time ceiling returns before `whyNoTier` is ever written (`:1847-1852`
stands ahead of `:1853-1857`): a score in the 4–5 s or 8–9 s gap whose cues cover less than two thirds
of it records the held-time reason, and the no-band reason is never written at all. And "leaves the
budget standing aside" implies the budget otherwise stands: it never does. `scoreWhyNo` calls no
budget at all, and its closing note (`:1956-1962`) says the reckoning "REFUSES NOTHING" and lives on
the diagnostic surface. The only consumers of `budgetOfScore` are two diagnostic records (`:2358`,
`:3756`) and a test hook (`:4285`).

This is filed as a recommendation rather than a defect because the sentence is true of the case it
names — `duration: 0` does record `whyNoTier` — and no reader acts on the distinction today.

Replace the clause with: "…a duration falling in no tier's band names no tier, and the tier rules
then say nothing about the score, with that reason recorded on the diagnostic surface beside the
held-time reading, which is read first. No reading of the budget ever refuses a score."

`recommendation · now · missing-scenario (state-space)`

---

### Verified clean

**F5's fold — the camera counts unconditionally, and the justification holds.** `tierFor` seeds
`accs = 1` before it looks at anything (`pass-composer.js:3408-3410`). The added justification "since
every composed plan carries a camera record" is true of the road the score travels:
`buildTemplate` writes `camera: { owner: "stage", rests: "b", track: [4 points] }` on every plan it
builds (`:4050-4076`), `fillPlan` only edits that track's poses, and `serialise`'s `CAMERA_ALLOWED`
filter (`:1331`, `:8751-8754`) passes `owner`, `rests` and `track` through — so the serialised score
always names a track. The first record's open question ("is a plan with no camera lawful?") is
answered: not on this road. One observation, no finding — the host still counts the camera
conditionally on `track.length > 0` (`pass-layer.js:1834`), and its comment still reads "wherever the
score names a camera track". The two agree in outcome because the antecedent is always true.

**The follow-up's own `EX-PASS-DOOR` fix — verified independently, and it is right.**

> "…never by the host mid-flight, which judges a manifest at registration and never reads a score's
> doors against it." — SPEC.md:667-669

`manifestWhyNo` (`pass-layer.js:342-364`) reads `inst.manifest` alone: a preserved drawing buffer, no
declared pass, an unnamed uniform, an unknown uniform type, an unsuppliable source. It takes no score
and no cue. Both call sites are registration (`:1672`, `:3985`). Nothing else in that file reads a
cue's `doors` against a manifest — `doorHandles` (`:2541-2543`) silently ignores a door naming a
handle the manifest does not publish, which is the opposite of a refusal. The self-caught fix is
accurate and I would not change a word of it.

One observation for a bug row rather than a spec finding: `landingDoorOf` (`:2613-2635`) reads
`v.inst.manifest.handles[k].min` at `:2629` with no guard on `k` being published, so a score naming a
blank door would throw there on an interruption rather than degrade. That is code, and it routes to a
bug row by the three-source lens, not into this section.

## Phase 3.5 — Acknowledged gaps

The corrected section flags none — no Open Item, no TBD, no unanswered rhetorical question. The two
its neighbours flag are unchanged from the first record and are not re-filed here:
`TEST_MATRIX.md` still states that no architecture node owns `pass-composer.js`, and that eight of its
fourteen rows are declared and unbuilt. Both are the author's own known issues.

`acknowledged · hard-to-operate (ops-ux)`

## Phase 3e — Mandatory sweep verdicts

Scoped to the corrections, one row for the one surface the section registers.

| Surface | Declared cross-cutting laws | Edge-condition completeness | Cross-surface policy uniformity | Lifecycle | Unwritten seams |
|---|---|---|---|---|---|
| The pass (`EX-PASS`) | N/A — `SPEC.md` still keeps no declared-laws home; unchanged by this fold and still a FULL-pass matter | hit — F13 (the third branch's guard names a condition that is not the branch's own), F17 (the band gap's recorded reason) | hit — F15 (one budget rule stated over three readers that do not all take it) | clean — the fold moved no state and no transition | hit — F9, F10, F11 (the seam between this engine and the two out-of-tree gates is now written, and written wrong: wrong file for one refusal, wrong corpus for all three, and a fourth refusal the gates hold that the spec denies) |

Quantifier re-verify, over the sentences the fold introduced. "every ordered pair composes"
(`:592`) — holds against `pass-composer.js:5312`, the composer's one return. "always counts as one
accompaniment" (`:639`) — holds, `:3410`. "however many of them declare it" (`:641`) — the count holds,
the condition does not, F14. "count in every one of those sums" (`:638`) — falsified, F15. "and nothing
else is" (`:652`) — falsified, F16. "the build-time refusals are three" (`:2143`) — falsified, F9: the
gates hold four. "this repository's own suite proves none of them" (`:2143`) — falsified, F12.

Class lens: swept — two classes filed. The first is **"a claim pinned to an enforcer nobody read"**:
F10 (the wrong file), F11 (the wrong corpus), F12 (the suite row that exists), F15 (the gates that
count no colour voice). All four say what some gate does without opening it, and all four are wrong
in the direction that flatters the document. Its cause is structural and worth naming: the fold's only
primary source for the gate was a code comment in `pass-layer.js:1752-1767` and a paragraph in
`PASS-API-V1.md:513-516`, both of which name one file for one law, and the fold generalized one
citation to three refusals. The second class is **"a correction folded into `SPEC.md` alone while its
twin stands unfolded"**: F9 (the actor refusal in the contract, the matrix and two gates), and F12's
`TEST_MATRIX.md` rows. `SPEC.md` was edited; the documents `SPEC.md` defers to were not.

## Phase 4 — Human and operational factors

Domain language: unchanged and still clean. The new `EX-PASS-ROLE` paragraph reads in the product's
own words, and the backticked route-role values are wire names inside a contract sentence, which is
the right register.

Observability: improved by the fold. `SPEC.md:644-645` now names the diagnostic surface where the
first record found no pointer to it at all. The pointer is right; what is recorded there is F17's
detail.

Traceability: the fold added `file:line` pins to `PASS-API-V1.md` (`:3409-3411`, `:3416-3423`), which
is the right habit and both land on the lines they name. That makes the two wrong claims beside them
(F14, F15) findable, which is the pins doing their job.

Scale, security and privacy: unchanged from the first record, and the fold touched neither.

## Phase 5 — Closing summary

**Top three to fix before a third pass is worth running.**
1. F9 — fold F1 across `PASS-API-V1.md` §4.7, conformance row 35, `TEST_MATRIX.md:61` and PASS-02, and
   decide what happens to the actor row in the two gates. Right now `SPEC.md` and the contract it
   defers to say opposite things about the same plan.
2. F11 with F10 — the enforcement sentence is the load-bearing one and it is wrong twice: the wrong
   file for the door, and a corpus that is not this composer's for all three. Say what is true, then
   open the row that makes it true.
3. F16 — the tier's source is stated as the route role alone and it is not; the pair's own cast picks
   between quiet and middle.

**Properties the section should state explicitly.** Paste-ready:
- "A plan lawful for this composer is not yet a plan the tlvphotos gates accept; the actor refusal
  still stands there."
- "The colour voice is counted wherever a surviving cue still claims `LIGHT-COLOUR`, and a crossing
  that gave the voice up to hold its accompaniment ceiling counts nothing for it."
- "The composer counts the colour voice; the host's reckoning and the build gates count the camera
  alone."
- "A step's route role sets the ceiling of the tier its pass may reach for and opens the culmination;
  the pair's own cast decides between a quiet and a middle."
- "No reading of the tier budget ever refuses a score."

**Open questions — the two I could not settle by inspection.**
1. Is `tierFor`'s nearest-row branch reachable? F13's fix forks on it, and answering it needs either a
   witness cast or a proof that the budget loop cannot exit past a fitting row.
2. Should the actor refusal come out of the two tlvphotos gates, or should `SPEC.md` say a plan lawful
   here can be refused there? That is a product decision about which tree owns the law, and only
   Alexander settles it.

**Queued for a taste call.** F17 alone, and F8 from the first record, which the fold did not touch.

**`[default]` census.** The corrected section still carries no `[default]`-tagged sentence. Two values
the fold decided without tagging are worth his glance: the choice to state the colour voice as
unconditional (F14) and the choice to state the nearest-row branch as behaviour rather than as dead
code (F13).

## Verdict

**NEEDS A THIRD PASS.** Eight new defects, one recommendation, two classes swept. Four of the seven
folds hold as written and are named clean above, and the `EX-PASS-DOOR` correction the follow-up made
on its own initiative is right — it was the most careful edit of the batch. The three that fail all
fail the same way, and it is the way the first record's F2 warned about: a law's enforcement was
written down without opening the enforcer. The section is now precise about what this engine does and
still wrong about who checks it, which is a better failure than the one it started with, and not yet a
section anything should be built against. No finding above is folded; every row is open.
