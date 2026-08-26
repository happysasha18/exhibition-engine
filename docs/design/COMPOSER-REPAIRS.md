# Four repairs to the passage composer

Four defects in `engine/assets/pass-composer.js`, each with the block that closes it, the argument
that the block holds for any two pictures and any collection, and what the applier must check once it
is in.

**The file was being edited while this was written.** Every anchor below is quoted with enough
surrounding text to find it after a reflow, and every one is pinned by the sentence the file's own
comment opens with rather than by a line number. Where a line number appears it is where the text
stood at the time of writing and is a hint, not an address. The applier should search for the quoted
text.

The rows that prove all four are in `tests/test_pass_lawful.py`. Every one of them is red against the
file as it stands.

---

## R1 — the accompaniment budget, and a plan that declares a tier its own counts contradict

### What is broken

Three places could hold charter shelf 17's accompaniment budget and none does.

The budget loop in `compose` tests two things and not the third. Its condition reads

```js
        var fits = placed[0] !== null
          && letters <= roleBudget.letters
          && TIER_RANK[tier] <= TIER_RANK[roleBudget.tier];
        if (fits) break;
```

Letters are bounded, the tier's rank is bounded, accompaniments are not in the condition at all, so
no voice is ever given up for an accompaniment overrun. `ROLE_BUDGETS` carries no accompaniment
column for it to read.

`tierFor` then answers with a row the counts do not satisfy. Its last branch, opening on the sentence
`NO ROW FITS THE COUNTS, AND THAT IS STILL NOT A REFUSAL`, scans the three rows for the one the
counts stand nearest and returns it, and `compose` writes that row's tier onto the plan. The plan
then declares a tier its own voice counts contradict.

The host reckons the budget and refuses nothing, by design and dated: `engine/client/01a-pass.js`,
the note opening `THE WEIGHT IS A READING AND NO LONGER A WALL`, and the same lane's treatment of
every other reading.

The build-time plan gate the contract names lives in the tlvphotos tree. `PASS-API-V1.md` says so in
as many words in §4.4: the gate that judges a plan is `lab/sceneplan-build-check.py`, on a branch of
another repository, and it has never lived in the engine. A score composed in a browser never reaches
it.

### The construction that reaches it, with no sample anywhere

At any role but a culmination, `voiceTheCues` voices the pivot an accompaniment as soon as either a
travelling move or an arrival exists:

```js
      if (folds === "pivot") voices.pivot = "miracle";
      else if (culmination) voices.pivot = "letter";
      else if (hasTravel || hasArrival) voices.pivot = "accompaniment";
      else voices.pivot = "letter";
```

`tierFor` seeds the count at one for the camera, which is `PASS-API-V1.md` §4.4's own amendment of
2026-08-14 10:31, and adds one more where any surviving cue declares the LIGHT-COLOUR level:

```js
      var letters = 0, accs = 1, miracles = 0, k, i, row;
      ...
      if (singsColour) accs += 1;
```

That is three accompaniments against a middle row's ceiling of two and a quiet row's ceiling of one.
No row fits. The nearest-row scan ties the middle and the culmination — the middle misses by one on
accompaniments, the culmination by one on miracles — and the strict `<` in

```js
        if (bestMiss === null || miss < bestMiss) { bestMiss = miss; bestRow = r; }
```

keeps the first, which is the middle. The plan declares a middle carrying three accompaniments.

**The pivot is the only cue that can ever be voiced an accompaniment.** Reading `voiceTheCues` over
its whole domain: the travel is a miracle or a letter, the arrival is a miracle or a letter, and only
the pivot has an accompaniment branch. So the count is exactly

```
accompaniments = 1 (the camera) + (the pivot is an accompaniment ? 1 : 0) + (any cue sings colour ? 1 : 0)
```

and its whole range is one to three. That is the entire reachable space, and it is read off the
function's own branches rather than off any set of photographs.

### Why neither obvious repair is the repair

`PASS-API-V1.md` §4.7: the declared tier and the measured one must agree, a disagreement is a red,
and neither value silently wins.

Charter shelf 17 as amended on his word of 2026-08-18 13:41: the counts shape a crossing that is
already playing and never refuse one — no pair and no crossing fails to qualify on a count.

Retiring a move until the count fits is out. The three accompaniments are the camera, the ground and
colour. The camera is a constant of every crossing by the shelf's own amendment. The ground is the
crossing — retiring it leaves nothing to cross on. Retiring the travelling move or the arrival to pay
for an accompaniment overrun takes a letter to settle an accompaniment debt and costs the crossing
its character, which the second sentence forbids.

Widening a row is out. The three rows are shelf 17's own numbers. A fourth row, or a wider ceiling,
is this seat naming a number the charter does not.

**What is left is the only thing the accompaniment budget can lawfully spend: an accompanying
voice.** Shelf 17's own list of them is camera, light sweep, colour, breath or drift, focus pull,
rubato-jitter. Of the three the composer ever counts, the colour voice is the one that is neither the
camera nor the crossing itself, and it is the one the composition already owns outright: the levels
law leaves exactly one cue owning LIGHT-COLOUR and takes that level's handles off every other cue's
track list. Owning it by nobody is a decision the composition is already free to make, and it costs
no cue, no instrument, no move and no letter. The picture loses one accompanying colour sweep, which
is precisely what an accompaniment budget is a budget over.

So the shape of the repair is: the ceiling enters the loop, and its answer is to give up the colour
voice rather than a move. That is a count shaping a crossing that is already playing, which is the
charter's own sentence for what a count may do.

### The blocks

**R1-a. A reader for shelf 17's own ceilings.** Put it immediately after `bandOfTier`, whose comment
opens `Shelf 17's band of seconds for a named tier, and the one road to it.` The new function reads
the same table for the same reason.

Find:

```js
    function bandOfTier(tier) {
      var i;
      for (i = 0; i < TIERS.length; i++) if (TIERS[i].tier === tier) return TIERS[i].band;
      return TIERS[1].band;
    }
```

Add directly beneath it:

```js
    // SHELF 17'S OWN CEILING FOR ONE COLUMN OF A NAMED TIER, and the one road to it. `TIERS` is
    // where the three rows live, so a ceiling is read off the row rather than copied beside it; a
    // caller naming a tier that has no row is answered with the middle's, the same default
    // `bandOfTier` above already takes.
    function ceilingOfTier(tier, column) {
      var i;
      for (i = 0; i < TIERS.length; i++) if (TIERS[i].tier === tier) return TIERS[i][column][1];
      return TIERS[1][column][1];
    }
```

**R1-b. The give-up, declared beside the other things the loop can turn over.** Find, in `compose`:

```js
      var voices, tier, letters, accs, k, instrumentOf, stackOrder, placed, capped = [];
      // WHICH CUE FOLDS THE FRAME, or nothing — read off the manifest exactly as `folds` above is,
```

Replace the first of those two lines with:

```js
      var voices, tier, letters, accs, k, instrumentOf, stackOrder, placed, capped = [];
      // WHETHER THIS CROSSING STILL SPENDS ITS COLOUR VOICE. Shelf 17 counts the camera, the ground
      // and colour in one column, and the loop below may find all three standing against a ceiling
      // of two. The colour voice is the one of the three that is neither the camera nor the crossing
      // itself, so it is the one an accompaniment budget can spend: the level goes unowned, its
      // handles come off every track list, and the instruments' own published defaults stand there.
      // Every cue, every instrument and every move stands. It is re-read on every turn of the loop
      // because the loop can retire the very cue that sings it.
      var colourVoice = true, accCeiling = 0;
```

**R1-c. The ceiling enters the loop's own condition, and the shaping runs before any retirement.**
Find, inside the budget loop:

```js
        stackOrder = CUE_IDS.filter(function (c) { return instrumentOf[c] !== undefined; });
        placed = placeTheStack(stackOrder, instrumentOf);
        var fits = placed[0] !== null
          && letters <= roleBudget.letters
          && TIER_RANK[tier] <= TIER_RANK[roleBudget.tier];
        if (fits) break;
```

Replace with:

```js
        stackOrder = CUE_IDS.filter(function (c) { return instrumentOf[c] !== undefined; });
        placed = placeTheStack(stackOrder, instrumentOf);
        // WHETHER THIS CAST SINGS LIGHT-COLOUR, read here rather than after the loop, because the
        // count it changes is one the loop has to answer, and re-read on every turn because the
        // loop can retire the very cue that sings it. It is read off the cues that survived this
        // turn, never off the instrument variables alone.
        var singsHere = false, ci;
        for (ci = 0; ci < stackOrder.length; ci++) {
          if ((MANIFESTS[instrumentOf[stackOrder[ci]]].levels || []).indexOf("LIGHT-COLOUR") >= 0) {
            singsHere = true;
            break;
          }
        }
        // THE ACCOMPANIMENT CEILING IS THE THIRD BOUND, and it belongs to the tier this plan will
        // DECLARE rather than to the one the role reached for. §4.7 asks the declared tier and the
        // measured one to agree, so the ceiling that has to hold is the declared row's; and since
        // the three rows' accompaniment ceilings rise with the tier's own rank, and the rank test
        // below already holds the realised tier at or under the role's, the declared row's ceiling
        // is the tighter of the two and answering it answers both.
        accCeiling = ceilingOfTier(tier, "accompaniments");
        // THE COUNT SHAPES THE CROSSING WITHOUT TOUCHING A MOVE. Charter shelf 17 as amended on his
        // word of 2026-08-18 13:41: the counts shape a crossing that is already playing and never
        // refuse one. An accompaniment overrun is paid for with an ACCOMPANYING VOICE, which is what
        // the column counts — never with a letter, which would take a move away to settle a debt it
        // did not run up. The camera is a constant of every crossing by §4.4's own amendment and the
        // ground IS the crossing, so colour is the one of the three that can stand down, and it
        // stands down the way the levels law already stands a voice down: the level goes unowned.
        //
        // IT IS A READING OF THIS TURN AND NEVER A LATCH. Written as a one-way give-up it would
        // outlive the count that caused it: a turn that later retires the very cue that sang would
        // leave the crossing without a colour voice it could now afford. This line is a pure
        // function of the counts the turn it runs on actually carries, so the answer that stands is
        // the answer for the cast that stands, and the loop gains no new road out.
        colourVoice = !(singsHere && accs + 1 > accCeiling);
        var fits = placed[0] !== null
          && letters <= roleBudget.letters
          && accs + ((colourVoice && singsHere) ? 1 : 0) <= accCeiling
          && TIER_RANK[tier] <= TIER_RANK[roleBudget.tier];
        if (fits) break;
```

**R1-c-2. What the count shaped, said on the plan.** Immediately after the loop, find the block that
answers the placement law with a one-cue stack and the reading that follows it:

```js
      var stacks = placed[0];
      // WHETHER THIS CAST SINGS LIGHT-COLOUR, read off the cues that actually survived the loop
```

Insert between those two lines:

```js
      // WHAT THE COUNT SHAPED, in the same place every other shaping this crossing took is written.
      // A thin passage reads back to the reason it is thin, and this one is thin in exactly one
      // way: it keeps every move, every cue and every instrument, and plays without its colour
      // voice. `capped` and `stood` are the two lists that already carry every other shaping.
      if (!colourVoice) {
        capped.push("colour");
        stood.push("shelf 17 gives a " + tier + " at most " + accCeiling + " accompanying voices "
                   + "and the camera and the ground already stand in them, so the crossing plays "
                   + "without its colour voice and keeps every move it makes");
      }
```

**R1-d. The reading after the loop answers to the loop's own decision.** Find, just below the loop,
the block opening `WHETHER THIS CAST SINGS LIGHT-COLOUR, read off the cues that actually survived`,
and change its loop header:

```js
      for (i = 0; i < stackOrder.length; i++) {
```

to:

```js
      for (i = 0; colourVoice && i < stackOrder.length; i++) {
```

**R1-e. The give-up travels to the score on the plan's own spec.** Find, in the `spec` record:

```js
        budget: counts, intentKey: intentKey, road: road.id, role: role, passIndex: passIndex,
        rhythmShift: rhythmShift,
```

Replace with:

```js
        budget: counts, intentKey: intentKey, road: road.id, role: role, passIndex: passIndex,
        rhythmShift: rhythmShift,
        // WHETHER THIS CROSSING STILL SPENDS ITS COLOUR VOICE (the budget loop above). It travels
        // here so the score and the counts say the same thing: a crossing that gave the voice up
        // must not go on emitting a cue that owns LIGHT-COLOUR, or the plan's declared tier and the
        // score's own voices would disagree again by another road.
        colourVoice: colourVoice,
```

**R1-f. The score stops owning the level the crossing gave up.** Find, in `buildTemplate`:

```js
          levels: INSTRUMENTS[instr].levels.slice(),
```

Replace with:

```js
          // THE LEVEL A CROSSING GAVE UP IS OWNED BY NOBODY. `spec.colourVoice === false` is
          // `compose`'s own word that shelf 17's accompaniment ceiling was already spent by the
          // camera and the ground. The level leaves every cue's declared list, `ownTheLevels` gives
          // it to no one, `ownedTracks` takes its handles off the track lists, and each
          // instrument's own published default stands there — the same road every non-owner in this
          // score already takes. No cue, no instrument and no move is given up. A plan built by some
          // other road carries no such field and is unchanged.
          levels: INSTRUMENTS[instr].levels.filter(function (lv) {
            return spec.colourVoice !== false || lv !== "LIGHT-COLOUR";
          }),
```

### The argument, over the whole reachable space

`accompaniments = 1 + p + c`, where `p` is one when the pivot is voiced an accompaniment and `c` is
one when a surviving cue owns LIGHT-COLOUR. Both are read off `voiceTheCues`' own branches, so the
enumeration below is complete for any two pictures and any collection.

Where the culmination reading holds — `(world || folds) && hasArrival && role === "culmination"` —
`voiceTheCues` voices the pivot a letter or a miracle, so `p` is nought and the count is at most two
against the culmination row's ceiling of three. Nothing is shaped and nothing needs to be.

Where it does not hold and a folding cue stands on the pivot, the pivot is a miracle, `p` is nought,
the tier reads middle and the count is at most two against the middle's ceiling of two. Nothing is
shaped.

Where it does not hold and either a travelling move or an arrival stands, the pivot is an
accompaniment, `p` is one, the tier reads middle, and the count is two or three. Where it is three
the block gives up the colour voice and it is two, inside the middle's ceiling.

Where neither a travelling move nor an arrival nor a fold stands, the pivot is a letter, `p` is
nought, the tier reads quiet and the count is one or two. Where it is two the block gives up the
colour voice and it is one, inside the quiet row's ceiling.

The letters column holds by the same reading. Three letters with no miracle is unreachable: the pivot
is a letter beside a travel and an arrival only under the culmination reading, and that reading
requires either a fold or an opened world, each of which makes one of the three a miracle. So the
letters count never exceeds two where the miracle count is nought, and the middle row takes both.

The miracle count is nought or one and never two, because `folds` names at most one cue and `world`
is only ever set where `folds` is null.

Every reachable triple therefore satisfies the row of the tier the plan declares, and `tierFor`'s
nearest-row branch becomes unreachable from `compose`. It is left standing because `tierFor` must
stay total for a voice record handed to it by some other road, and because a branch that cannot be
reached is not a branch that may return nothing.

The shaping never refuses. Giving up a level is a decision of the composition, never of an
instrument, so it is available on every pair without exception: there is no candidate to search for
and nothing to fall back from.

The loop gains no new road out. R1-c adds no `continue` and no `break`; it adds one assignment and
one term to a condition that was already there, so the loop's own termination argument — the
travelling move goes, then the arrival, then the bottom `break` — is untouched.

One path reaches the counts without a further turn of the loop: the placement law's own fallback
below it, which forces a one-cue stack where the loop retired everything it could and the law still
said no. `colourVoice` there is the last turn's reading, and it can only be false where the last turn
carried more accompaniments than the fallback does. Since a false reading only ever lowers the count,
the declared row can only be satisfied more easily, so the invariant holds on that path too.

### What the applier must check

`tests/test_pass_composed.py`'s role row — one pair at the five route roles, each inside shelf 17's
budget for that role — should go from passing on the letters alone to passing on all three columns.
It may legitimately move.

Any row pinning a score's `cues[].levels` or `levelOwnership` for a passage whose cast includes
`grid-colour`, `overlay`, `strata-light`, `strata-scale` or `studio` may legitimately move: those are
the instruments that declare LIGHT-COLOUR. No row pinning a passage cast entirely from the other
instruments may move, because `colourVoice` stays true there and the filter is a no-op.

`plan.capped` gains the entry `colour` on shaped passages, and `plan.stood` gains one sentence. A row
asserting `capped` is empty on a specific pair may legitimately move; a row asserting it names only
`travel` or `arrival` must be read again.

`shape` is deliberately left alone. Two plans that differ only in whether the colour voice stands
share a `shapeId`, which is a diagnostic imprecision rather than a defect — the template is built
from `spec`, not from the name. If the applier wants the name to tell them apart, it is one clause in
`shapeId`, and it moves every `shape` string on shaped passages.

`MANIFESTS[iid].levels` and `INSTRUMENTS[iid].levels` are read by R1-c and R1-f respectively. They
are two views of one manifest and they agree in the settings record the site ships. If a bake ever
lets them drift, the count and the score drift with them, and the R1 row in
`tests/test_pass_lawful.py` reds — which is the row working.

---

## R2 — the score is weighed, judged, and then a field is added to it

### The invariant

**A score is weighed after the last field that will ever be written to it, or not at all.**

Everything the composer publishes about a score's weight — the tightened byte count, the pretty text,
the fence reading and the record of what was shed to fit — is a statement about one exact object. A
field written after those four are taken makes all four statements about an object nobody receives.

### What is broken

`scoreFor` ends:

```js
      var shed = fitTheWeight(out[0]);
      var text = writeJson(out[0], 0);
      var tight = writeJsonTight(out[0]);
      return { key: key, score: out[0], json: text, bytes: tight.length,
               weightShed: shed,
               overTheFence: SCORE_FENCE_BYTES ? tight.length > SCORE_FENCE_BYTES : false,
```

`passageFor` then writes onto the same object:

```js
      if (made.score && made.cameraTravels && LED_ROLES.indexOf(role) >= 0
          && !claimsTheWorld(made.score)) {
        made.score.camera.lead = true;
      }
```

So on every camera-led passage, `bytes` is short by the width of that field, `json` is the text of a
score that has no `lead` in it, `overTheFence` answers for the shorter object, and `weightShed` names
what was shed to reach a size the score does not have.

Today the client treats weight as a reading — `engine/client/01a-pass.js`, the note opening `THE
WEIGHT IS A READING AND NO LONGER A WALL` — so the cost is a lying diagnostic, and the diagnostic
surface at the same file's `composer.passages` rows publishes both wrong numbers. The client also
recomputes the weight itself off the raw score, so the two readings of one score disagree.

The day the fence is a wall again it is a lost crossing, and the R2 fence row in
`tests/test_pass_lawful.py` demonstrates exactly that by standing the fence one byte under the
score's true weight: the composer says the score fits and sheds nothing, and the score handed back is
over.

### The blocks

**R2-a. The decision moves to where the score is still being built.** In `scoreFor`, find:

```js
      var out = serialise(filled);
      // THE SCORE IS FITTED TO THE CLIENT'S OWN WEIGHT FENCE, never handed over to be thrown away.
```

Insert between those two lines:

```js
      // THE LAST FIELD A SCORE EVER GAINS IS WRITTEN BEFORE THE SCORE IS WEIGHED. A score is
      // weighed after the last field that will ever be written to it, or not at all: `fitTheWeight`
      // below tightens the score and `overTheFence` reads the tightened bytes, so a field added
      // after them leaves the published weight, the published text, the fence reading and the
      // record of what was shed all answering for a score the caller never receives. `passageFor`
      // wrote this one there, past the weighing, and while the client reads the weight rather than
      // enforcing it that costs a lying diagnostic; the day the fence is a wall again it costs a
      // crossing.
      //
      // WHAT THE READING IS, unchanged from the entry that used to hold it. `camera.lead` says the
      // flight itself is the transition: the anchor gives up its held middle and the pose travels
      // the whole duration. Its two homes are the quiet link and the return, which charter shelf 15
      // makes tonic and shelf 17 gives one move, at most one accompanying voice and no miracle — the
      // register a led passage wants underneath it, because the camera is the world voice and a led
      // flight spends it. The pair's own records have to give the flight somewhere to go, since a
      // still flight leads nothing. And under the levels law one voice holds one level, so a led
      // score may never also give a cue the WORLD level. All three readings are in hand here.
      var cameraTravels = plan.spec.travel === null && plan.spec.arrival === null;
      if (out[0] && cameraTravels && LED_ROLES.indexOf(step) >= 0 && !claimsTheWorld(out[0])) {
        out[0].camera.lead = true;
      }
```

**R2-b. One reading of "the flight is the only thing left".** Find, in the same return record:

```js
               cameraTravels: (plan.spec.travel === null && plan.spec.arrival === null) };
```

Replace with:

```js
               cameraTravels: cameraTravels };
```

**R2-c. The entry stops writing to a weighed score.** In `passageFor`, find and delete:

```js
      if (made.score && made.cameraTravels && LED_ROLES.indexOf(role) >= 0
          && !claimsTheWorld(made.score)) {
        made.score.camera.lead = true;
      }
```

Put in its place:

```js
      // THE PASSAGE THE CAMERA LEADS IS DECIDED IN THE CHOICE CORE, where the score is still being
      // built. It stood here, after the core had already weighed the score and published its bytes,
      // its text and its fence reading, so those three answered for a score without this field on
      // it. The reading itself is unchanged and its whole argument travels with it; what changed is
      // that a score is now weighed after the last field it will ever gain.
```

The long comment above the deleted lines, opening `THE PASSAGE THE CAMERA LEADS. The camera lane
built the capability`, moves to `scoreFor` with the code — R2-a carries its substance.

### The argument

`LED_ROLES` and `claimsTheWorld` both live in the same `make()` scope as `scoreFor`. `claimsTheWorld`
is a function declaration and hoists; `LED_ROLES` is a `var` assigned while `make()` runs, and
`scoreFor` is only ever called after `make()` has returned. Neither is undefined at the moment
`scoreFor` reads it.

`step` is `scoreFor`'s own defaulted role — `ROLE_BUDGETS[role] ? role : "middle"`. `passageFor`
already narrows an unknown role to `middle` before calling, so on the entry's road `step` and `role`
are the same value. A direct call to `scoreFor` with a role outside the five now reads it as a middle
and leads nothing, which is stricter than the entry and correct: `middle` is not a led role.

After the block the invariant holds by inspection of the order of statements: `serialise`, then the
last write, then `fitTheWeight`, then the two texts, then the return. Nothing between the weighing
and the return touches the score.

### What the applier must check

Every row asserting `bytes` or byte equality on a **quiet link** or a **return** whose passage is
camera-led legitimately moves, by the width of the added field. No row on an entrance, a middle or a
culmination may move, because those roles are not in `LED_ROLES`.

`tests/test_pass_composed.py`'s `spelled` versus `core` row — `passageFor` spelled out against
`scoreFor` called with four values — must be read again. It compares a request-defaulted call with a
bare one, and `scoreFor` now decides the lead itself. The row should stay green because `passageFor`
hands `scoreFor` the same defaulted role, but the row's reason changes and it deserves a look.

The client's `passScoreCheck` recomputes the weight off the raw score. Its reading and the composer's
`bytes` should now agree on every passage. Nothing in the client needs changing.

---

## R3 — the wall clock inside the die that names the family a return is matched against

### What is broken

`weatherNow` calls `new Date()` and reads the local year, hour and minute:

```js
    function weatherNow() {
      var d = new Date();
      var startOfYear = new Date(d.getFullYear(), 0, 1);
      var dayOfYear = Math.floor((d.getTime() - startOfYear.getTime()) / 86400000);
      var hourFrac = (d.getHours() + d.getMinutes() / 60) / 24;
```

`weatherBiasOf` multiplies that reading into every weight the die runs on:

```js
        w.push(Math.max(0, Number(pool[i].fit) || 0)
               * (letters ? coolOf(pool[i].id) * viewerBiasOf(pool[i].id) : 1)
               * weatherBiasOf(pool[i]));
```

`pivotOfPair` rolls the ground through that same die, the pivot's own transform is read off the
chosen ground, and `scoreFor` computes the family token from it:

```js
      chosen.family = familyToken(filled.pivot.transform,
                                  filled.travellingAxis ? filled.travellingAxis.measure : null);
```

Three consequences follow from that chain, each by construction and none by sampling.

**A pinned seed does not reproduce a run across an hour boundary.** `PASS-API-V1.md` calls that the
judging mode in three places — §4.4f's `familySeed`, §4.4g's own sentence that the die is made of the
visit's seed, the pass index and the edge's key so there is one idea of a seed and no clock in
either, and conformance row 10, that a seeded run repeats to the pixel. Row 48 rests on the same
thing across a return.

**Charter shelf 16 asks for both the day's weather bias and the seeded judging mode, and nobody wrote
which wins where they meet.** The shelf lists the day's weather as the third step of its dice
pipeline, and two sentences later says that seeds and determinism are the judging mode while
ephemerality is the viewer mode.

**The composition depends on the viewer's timezone.** Because the getters are local, two viewers at
one instant get two different hours, therefore two different weights, therefore two different
grounds, therefore two different families. The viewer's machine offset is an input from none of the
three sources charter shelf 20 allows: a picture's own record, the dramaturgy of the walk, the
session.

### The collision, named plainly, and the resolution

The collision is real. Shelf 16 asks the engine to bias the roll by the day and asks a pinned seed to
reproduce a run exactly, and it never says which answers first when a pinned run crosses an hour
boundary.

**The resolution: the two are not in conflict once the shelf's own last two sentences are read.** The
shelf itself already splits the modes — seeds and determinism are the judging mode, ephemerality is
the viewer mode, and every public run exists once. A day's weather bias is an input of the viewer
mode. What made them collide was not the shelf; it was the engine reading the day for itself.

A composer that calls the clock cannot be in the judging mode at all, because the clock is not on the
request and nothing pinned can pin it. The same shelf's pipeline is a list of things the walk hands
the die — cooldowns come from what the walk played, the viewer memory from what the visit did — and
the day is the one member of that list the composer conjured for itself. `PASS-API-V1.md` §4.4g says
the same in its own words: the die is made of three things, and there is no clock in either.

**So the day is an input, not a call.** The walk states the day on the request exactly as it states
the seed, the walk memory and the viewer memory. In the viewer mode the walk stamps the real instant
and the bias plays. In the judging mode the run bar stamps a fixed instant, or none, and the run
reproduces. A request that names no day reads at the neutral bias of one, which is the neutral
`coolOf` and `viewerBiasOf` already take and which no other reading in this file treats as a refusal.
Nothing is refused, nothing is added to the vocabulary, and shelf 16 gets both of the things it asks
for, each in its own mode.

### R3-a — the timezone dependence, which is not a matter of taste and goes now

Find:

```js
    function weatherNow() {
      var d = new Date();
      var startOfYear = new Date(d.getFullYear(), 0, 1);
      var dayOfYear = Math.floor((d.getTime() - startOfYear.getTime()) / 86400000);
      var hourFrac = (d.getHours() + d.getMinutes() / 60) / 24;
```

Replace with:

```js
    function weatherNow() {
      // ONE CLOCK FOR EVERY VIEWER. These four readings were taken off the LOCAL getters, so two
      // people meeting one crossing at one instant read two different hours, two different weights
      // and two different grounds, and the family a return is matched against moved with the offset
      // the machine happens to be set to. That offset is an input from none of the three sources
      // charter shelf 20 allows — a picture's own record, the dramaturgy of the walk, the session —
      // and it is not the day either: the day is one day everywhere, and local midnight is not.
      var d = new Date();
      var dayOfYear = Math.floor((d.getTime() - Date.UTC(d.getUTCFullYear(), 0, 1)) / 86400000);
      var hourFrac = (d.getUTCHours() + d.getUTCMinutes() / 60) / 24;
```

The two comments immediately below, `LIGHT: a smooth day curve` and `TEMPO: the same clock`, keep
their arithmetic and lose their claim to read the viewer's own daylight. Their first lines should
read that the curve is the day's own and not any one viewer's.

The block is arithmetic only: `hourFrac` stays in `[0, 1)`, `dayOfYear` stays a whole number of days,
and the hue wheel's modulo is unchanged. Nothing about the bias's bounds moves — `weatherBiasOf`
stays inside `[1 - WEATHER_AMP, 1 + WEATHER_AMP]` on every branch, as its own comment already argues.

### R3-b — the day arrives on the request

This one changes the contract: `PASS-API-V1.md` §4.4g's request table gains a row. It is written out
in full so it can be applied as one piece, and the contract's owner should see it before it lands.

**R3-b-1. The visit's own instant, beside the other two things `scoreFor` sets fresh.** Find:

```js
    var viewerMemory = null;
```

Replace with:

```js
    var viewerMemory = null;
    // THE INSTANT THIS VISIT HAPPENS AT — charter shelf 16's third pipeline step, and it arrives the
    // way every other step of that pipeline arrives: the walk hands it in. It is set fresh by
    // `scoreFor` for the length of one composition and never accumulated here, exactly as
    // `walkPlayed` and `viewerMemory` are. Nothing in this file calls the clock, because a value the
    // composer takes for itself is a value nothing can pin, and shelf 16's own last two sentences
    // put the day in the VIEWER mode while a pinned seed is the JUDGING one. A request that names no
    // instant reads at the neutral, which is the neutral `coolOf` and `viewerBiasOf` already take.
    var visitClock = null;
```

**R3-b-2. `weatherNow` reads it.** After R3-a the function opens `var d = new Date();`. Change that
one line to:

```js
      var d = new Date(visitClock);
```

**R3-b-3. No day, no weather.** Find:

```js
    function weatherBiasOf(item) {
      if (!item || !item.kind) return 1;
      var w = weatherNow();
```

Replace with:

```js
    function weatherBiasOf(item) {
      if (!item || !item.kind) return 1;
      // A REQUEST THAT NAMES NO DAY GETS NO DAY'S BIAS, and that is the neutral rather than a
      // refusal: the reading is 1 on every candidate, the pair's own strongest reading ranks the
      // pool alone, and the crossing plays. It is the same neutral `coolOf` gives a letter no walk
      // has played and `viewerBiasOf` gives a letter no visit has heard of.
      if (visitClock === null) return 1;
      var w = weatherNow();
```

**R3-b-4. The core takes it.** Find:

```js
    function scoreFor(a, b, direction, seed, role, memory, played, viewer) {
```

Replace with:

```js
    function scoreFor(a, b, direction, seed, role, memory, played, viewer, day) {
```

and find, in the same function:

```js
      walkPlayed = Array.isArray(played) ? played : [];
      viewerMemory = viewer || null;
```

Replace with:

```js
      walkPlayed = Array.isArray(played) ? played : [];
      viewerMemory = viewer || null;
      // AND THE INSTANT THE VISIT IS HAPPENING AT — charter shelf 16's third pipeline step, set
      // fresh here for the length of this one composition exactly as the two lines above are. Its
      // absence reads as a visit that stated no day, which is the neutral every die already answers
      // the same way, and it is what makes a pinned seed reproduce a run: every input the
      // composition reads is now on the request.
      visitClock = (typeof day === "number" && day === day && isFinite(day)) ? day : null;
```

**R3-b-5. The entry reads and fences it.** In `passageFor`, find the closing brace of the viewer
memory fence and the line that follows:

```js
      var read = { routeRole: role, direction: direction, seed: seed, sessionMemory: memory,
```

Insert immediately above it:

```js
      // THE DAY THIS VISIT HAPPENS ON — charter shelf 16's third pipeline step, read here and handed
      // to the choice core exactly as the walk memory and the viewer memory are. It is one number:
      // the instant, in milliseconds, that the day and the hour are read off. A walk that states
      // none states none, and the day's bias reads at its own neutral — which is the viewer mode
      // where the walk rolls a fresh die anyway, and the judging mode where a pinned seed has to
      // reproduce its predecessor to the pixel (§4.4f). A value that is no instant is left unread
      // rather than refused, exactly as every other field of this entry is.
      var dayOfVisit = null;
      if (req.dayOfVisit !== undefined && req.dayOfVisit !== null) {
        var dv = Number(req.dayOfVisit);
        if (dv !== dv || !isFinite(dv)) {
          unread.push("a day of visit that names no instant, so the day's own bias reads neutral");
        } else {
          dayOfVisit = dv;
        }
      }
```

Then extend `read` and the call. Find:

```js
      var read = { routeRole: role, direction: direction, seed: seed, sessionMemory: memory,
                   walkMemory: played.length ? played : null,
                   viewerMemory: viewer,
```

Replace with:

```js
      var read = { routeRole: role, direction: direction, seed: seed, sessionMemory: memory,
                   walkMemory: played.length ? played : null,
                   viewerMemory: viewer,
                   dayOfVisit: dayOfVisit,
```

And find:

```js
      var made = scoreFor(a, b, direction, seed, role, memory, played, viewer);
```

Replace with:

```js
      var made = scoreFor(a, b, direction, seed, role, memory, played, viewer, dayOfVisit);
```

**R3-b-6. The contract.** `PASS-API-V1.md` §4.4g's request table gains one row, and the paragraph
below it that names what may be defaulted gains the field:

```
| `dayOfVisit` | the instant, in milliseconds, that charter shelf 16's day-weather step reads its date and hour off | the walk stated no day; the day's bias reads at its own neutral and the passage is reproducible from the request alone |
```

The section's sentence about the die — that it is made of the visit's seed, the pass index and the
edge's key, so there is one idea of a seed and no clock in either — is what this row makes true, and
it should say so.

### The argument

After R3-a, `weatherNow` reads the same instant the same way on every machine on earth, so the
composition is a function of the request and the instant alone. The timezone is gone as an input, and
that half of the repair needs no decision from anyone: the offset was a fourth source and shelf 20
allows three.

After R3-b, the composition is a function of the request alone. Two calls with the same request are
byte-identical whenever they were made, which is `PASS-API-V1.md` row 10 and row 48 and §4.4f's
pinned-visit sentence, all at once. Shelf 16's day still plays wherever the walk names a day, which is
every public run.

Nothing here can refuse. The day only ever multiplies a weight, and the weight already stands inside
`[1 - WEATHER_AMP, 1 + WEATHER_AMP]` with `WEATHER_AMP` under one, so no candidate is ever emptied
and the die always lands. With no day the multiplier is exactly one, which is the pool the die ran on
before shelf 16's third step was written at all.

### What the applier must check

Every row that composes twice and compares — the pinned-repeat rows in
`tests/test_pass_composed.py`, and any golden pinned to a composed score's bytes — becomes stable
across an hour boundary and across machines. Those rows may have been quietly flaky and are not
re-based by this; they simply stop being able to flake.

Any capture or golden taken at a particular local hour may legitimately move once, to the value the
same instant reads in one clock. No capture may move a second time.

R3-b changes `scoreFor`'s arity. Every direct caller in the tree passes four values and is unaffected
(the ninth reads `undefined` and the day reads neutral), but a caller that already passes eight
should be read.

R3-b makes `scoreFor` called with four values reproducible where today it is not. The
`spelled`-versus-`core` row in `tests/test_pass_composed.py` compares exactly those two roads and
should be read together with R2's note on the same row.

---

## R4 — charter shelf 20, broken inside the composer's own comments

### The rule and its reach

Shelf 20 bans any measurement, statistic or distribution computed across the photographs from
justifying, tuning, calibrating or validating any behaviour of the engine or any claim about it, and
it binds code, comments, documents, tests and anything reported to him. Its reason is structural: the
engine composes for any set of pictures, and the works on disk are one arbitrary handful of points
inside every possible pair times every effect times every parameter, so a count saying that some of
them did something is a fact about them and evidence of nothing beyond them.

Every claim is proved from the formula's own construction — its bounds, its clamps, the monotonicity
of how it combines, the definition and the range of each field it reads — and where the arithmetic
takes numbers with known spans it is checked over the whole span.

Real photographs keep one lawful use: a smoke check that the code runs and writes plausible output.
That is never called coverage and never reported as a share.

### The sweep

`tests/test_pass_lawful.py`'s R4 rows read the composer's own source and the contract's own text and
name every place a tally stands as an argument. They print the line and the rule and never the tally,
for the same reason this document does not: printing it would break the shelf here.

Run the rows for the live list. The locations at the time of writing, by the sentence each comment
block opens with, are grouped below by the class of argument each one is standing in for. The line
numbers are hints; the opening sentences are the addresses.

### Class 1 — a tally standing in for the proof that a formula reads nothing

The largest class. Each of these is a comment explaining a repair already made, and each argues its
case by saying how often the old code misbehaved over the works on disk. In every one of them the
misbehaviour is a property of the formula over its whole domain, and the count is strictly weaker
than the argument that was available all along.

| Where | The rule it argues for | The argument that replaces the tally |
| --- | --- | --- |
| `suitsPair`, the water row, `WHAT STOOD HERE WAS NOTHING AT ALL` | an instrument with no row gets a real reading rather than a typed constant | a constant reads neither record, so its output is independent of both inputs over the whole input space. It therefore ranks identically against every rival on every pair there can ever be — that is the defect, whole, and how often it was reached adds nothing to it. |
| the genre table's tonal-and-spectral row, `IT IS NOT A BRIDGE AND IT IS NOT A FALLBACK` | the ground is a candidate ranked on its own reading, not a road reached last | when a candidate is reachable only after every other has refused, it is selected by the refusals and not by its own fit — a fact about the control flow, true whatever the pool contains. |
| `genresFor`, the same road's row | the same | the same, one level out. |
| `groundReadings`, `WHAT WENT, AND WHY IT COULD NEVER HAVE BEEN RIGHT` | a reading ranks and never admits | an admission test compares a pair's reading against a number derived from other photographs, which answers how a reading stands among strangers when what is asked is how these two stand to each other. Both numbers are already in hand; the third is not a better answer to a question it does not ask. |
| `make(consts)`, `THE COLLECTION'S FLOORS AND THRESHOLDS ARE NO LONGER READ` | the floors and thresholds are not read | a quantile over a collection is exactly the object shelf 20 names. Citing the class is the whole argument; showing how many works cleared it argues the point by committing the offence. |
| `suitsPair`, the glass row, `THE GLASS RESTS ON A POINT AND FOLDS ABOUT IT` | the reading itself is the fit | as above, plus the construction fact that already stands in the comment: `suitsPair` is handed two work records and nothing else, so a floor it tried to read would be undefined. That is a defect provable from the signature. |
| `suitsPair`, the fold row, `THE WEDGE TILES OUTWARD INTO MIRRORED RINGS` | an instrument whose geometry is read off the stronger work is not ranked by the weaker | the comment's own next sentence is the proof: a minimum taken against a rival's maximum on the same number is a loss by construction rather than by merit, for every pair. Nothing about a collection is needed. |
| `standsAbove`, `THE INSTRUMENT THIS PAIR CASTS ON A KIND` | the coverage law is answered by choosing, never by retiring | a cast blind to a law breaks it whenever the law applies, and a name that satisfies a law by accident satisfies it for a reason that can change on the next landing. Both are statements about the rule, not about a run. |
| the arrival cast, `THE ARRIVING WORK CONDENSES, AND THE INSTRUMENT THAT CONDENSES IT IS CAST` | the name goes and the collision chooses | handing a slot to one instrument by name consults no fit and rolls no die, so the choice carries no reading of any pair at all — the strongest possible statement, and it needs no count. The paired defect, that the fallback dropped the arrival on a collision instead of choosing the next best, is likewise a branch that exists or does not. |
| `tierFor`, `THE TIER A PLAN DECLARES IS THE TIER ITS VOICES ACTUALLY MAKE` | a plan declares what it realised rather than refusing | the three rows leave gaps between them, and the reachable count space is enumerable from `voiceTheCues`' own branches — R1 above does exactly that. A refusal on a reachable gap is a defect on the gap's own account. |
| `cameraFlight`, `THE DEMAND IS COMPRESSED, NEVER CLIPPED` | a limit rather than a wall | a clamp is constant on the whole half-line above its bound, so it destroys the ordering there for every input; the compressed form is strictly monotone and never reaches its bound for any finite demand. Both facts are proved over the whole real line. The tail's shape is a property of the collection and belongs to nothing here. |
| `DOLLY_CAP` | the number is unmeasured and the bound belongs to the device | the two sentences that already stand — that the bound the frame can carry is the buffer's own oversampling, a property the composer cannot see — carry the whole argument. What the door framings ask for is a fact about photographs and cannot bound anything. |
| the cue course, `AND THE COURSE TAKES A NAME NO TRACK OF THIS CUE ALREADY CLAIMS` | the course takes an unclaimed name | two things that derive the same name collide whenever both are present, and the host's graph walk refuses a cycle by its own rule. A name collision is a defect on the first pair it reaches. |
| `scoreFor`, `THE SCORE IS FITTED TO THE CLIENT'S OWN WEIGHT FENCE` | a score is fitted rather than thrown away | the client refuses a score over its fence whole, and a score's weight is dominated by prose whose length is unbounded above by construction — the per-node note and the authored line. That a whole score can be lost to prose is provable from the two rules together. |
| `realiseIntent`, `THE LINE IS FITTED TO THE FENCE IT HAS TO PASS` | the line is shed and trimmed rather than refused | the same shape: an unbounded field against a fixed cap refuses whenever it exceeds it, and raising a cap moves a wall rather than removing one. |
| the arsenal lane's own header, `Six branches, one per instrument carried across today` | every landed instrument needs a fill branch | an instrument with no branch has every handle filled from the manifest default, so it plays one identical crossing on every pair by construction of `tracksFor` and `appliedValue`. That is the whole claim; how many parameters happened to move on some pairs is a weaker version of it. |
| the fill branches for the ready story, the mirror, the spiral, the fold and their neighbours | each branch exists so the instrument reads the pair | the same argument, per instrument: no branch means no track, no track means the default, and the default is one number for every pair. |

### Class 2 — a tally standing in for a field's own definition

These argue that one measured field is the right one to read by counting how the works on disk happen
to fall on it. In every case the field's own definition and range say the same thing about any set of
photographs whatever.

| Where | The rule it argues for | The argument that replaces the tally |
| --- | --- | --- |
| `measuredParts`, `AND THE ANGLE FOLLOWS THE SAME ORDER AS THE STEP, NOT THE STEP'S PRESENCE` | the angle follows whether a DIRECTION was recovered, not whether a step was | `structure.ownDevice.angleDeg` carries a direction only for a device that has one. A ring pattern has no direction to record, so the field reads its own zero for every ring-cut work in any collection — not most of them, all of them, by the measurement's own definition. The work's own measured grid angle is a reading of the same thing and is defined wherever a grid is, so it answers where the device says nothing. |
| the parquet fill, the same repair | the same | the same sentence, per branch. |
| the grid-and-colour fill, `gcAngle` | the same | the same sentence, per branch. |
| the mirror floor fill, `HOW MANY TILES ACROSS THE FLOOR` | the grid's period is read first and the device's step second | the device step is quantised to the device's own repeat, so its range is coarser than the grid period's by construction of the two measurements; reading the coarser one first puts more works on one value whatever the works are. That is a statement about the two measurements' resolutions. |
| the unfold fill, the same choice one level out | the same | the same. |
| `suitsPair`, the slot row, `THE DEPARTING WORK'S OWN SLOT IS WHAT PARTS` | the fit is the work's own gate reading | the fit is `motifs.gateGap`, and where a work carries no gate the fit is nothing and the slot stands at the motif's own band width. Both halves are read off the field's definition and the module's own answer for a source with no gate. How many works carry a gate decides nothing. |
| the droste fill, `HOW MANY COPIES STAND INSIDE ONE FALL OF FORTY` | the two ring counts are positioned by their ratio rather than handed straight | a ring count and a share-of-span handle are different scales, so handing the count in saturates for every count above the span's top — a statement about two ranges, checkable over the whole of both. What no record carries is how many rings one copy is worth; what both records carry is which work has more. That is the whole argument. |

### Class 3 — where the argument cannot survive without the tally, and that is the finding

Two rules rest on the collection rather than on their own construction, and saying so is the honest
answer rather than rewriting the comment.

**The fold's wedge count and the mirror's fold count, at `THE FOLD'S FOUR MEASURED HANDLES` and `HOW
OFTEN THE FOLD REPEATS`.** The rule itself is sound and needs no collection: a wedge count and a
rotational order are the same count in the same unit, so the handle's own span holds the reading
rather than standing in a different scale from it, and a work turning oftener than the glass reaches
is held at the glass's own reach. What cannot survive is the complaint attached to it — that this
handle stands still on most pairs because the measurement reads one value on most works. That is a
fact about the works on disk and about the record builder's own reading, not about this file. It
belongs in the record builder's tree with an owner, and here it should be one sentence naming the
dependency: the handle reads `structure.rotational.n`, and it moves exactly as far as that field
moves. No sentence here can prove that field varies, and none should try.

**`palette.rung` is a field whose definition is a statistic over the collection.**
`groundCandidates` reads it directly as a gate on the shared-palette-region candidate:

```js
      var paletteShare = (ra === rb && mine.length) ? hues.length / mine.length : 0;
```

Two works read as sharing a palette region only when they stand on the same rung — and which rung a
work stands on is a statement about the other photographs it was measured beside. This is shelf 20
broken at the source rather than in a comment: adding a photograph to the collection can move a
work's rung and therefore change which ground an unrelated pair crosses on, with neither picture
touched. It is outside these four repairs and it is designed in
`docs/design/PALETTE-RUNG.md`, with a block for each side of the line and rows in
`tests/test_pass_palette.py`.

**Corrected 2026-08-25.** This entry named `palette.colourfulness` beside the rung, on the strength
of the composer's own comments, which describe that field in several places as where a work sits on
the collection's own colourfulness ladder. **That description is false as of the producer on disk.**
The field is the ladder's continuous coordinate — half the work's own chroma against a fixed
perceptual anchor, half the normalised entropy of its own hue histogram — and it touches no other
photograph. The buckets on that ladder are collection-relative; the coordinate along it is not, and
the comments conflate them, which is a class-1 comment repair rather than a field defect. Trusting a
comment instead of reading the producer is precisely the failure shelf 20's own repair is about, and
this entry made it.

### Class 4 — lawful, and worth saying so

A count of the instruments the arsenal publishes — how many declare the world level, how many fill
the frame — is a fact about the engine's own code, not about photographs, and shelf 20 does not touch
it. It is still worth writing as a set rather than a number, because a number goes stale the moment
an instrument lands and a set is re-read at runtime.

A measurement in the unit the eye reads — a channel difference out of 255, a seam threshold — is a
perceptual fact about a rendered frame and not a distribution over the collection.

### The contract's own text

`PASS-API-V1.md` carries the same class in its own sections, and the R4 contract row names the lines.
They fall into the same classes: the byte fence and the intent fence are both argued from how many
shipped scores were refused, where the argument is that an unbounded field against a fixed cap
refuses whenever it exceeds it; the majority-road note in §4.6 argues from how many pairs share no
measure, where the argument is that the two decompositions the fallback reads are defined on any
photograph by construction; and conformance rows 34 and the equality notes in §4.4g state their reach
as the whole collection, where under shelf 20 they are smoke checks and must be labelled as such.

Row 34 deserves a line of its own. It reads that the fallback provider returns an ElementSet for
every ordered pair in the collection and that a single decline reds. Under shelf 20 that is a smoke
check, not coverage. The construction proof is one sentence and is already in the composer's own
comment: the tonal zones and the detail scales are two decompositions that read on any two
photographs, so the provider answers for every pair there can ever be. The row should keep running
and should say what it is.

### What the applier must check

Nothing behavioural. Every site in classes 1, 2 and 4 is a comment; rewriting it changes no byte the
composer emits, and the R2 and R3 rows would catch it if it did.

The two class-3 findings are not comment work and should not be closed by rewriting a comment. The
first is a record-side gap named as one. The second is a defect in what the composer reads and needs
its own repair, raised with the owner of the record builder.

---

## The rows

`tests/test_pass_lawful.py`. Seven behavioural rows and two source rows; eight red today and one
skipped. The skipped one is R1's red-on-bug proof, which arms itself the moment R1-c lands: it plants
both halves of that block — the assignment that gives the colour voice up and the term that puts the
ceiling into the loop's own condition — and requires the R1 row to go red again.

The plant takes both halves deliberately. Restoring either alone leaves a composer that still ends
inside a lawful row, because the loop answers the remaining bound by retiring a move instead; a
plant that could not tell those apart would prove the counts hold without proving which road the
composition took to hold them.

The four repairs were applied to a scratch copy of the composer and the seven behavioural rows were
run against it. All seven go green, and the red-on-bug row reds when the plant is applied. The two
source rows stay red, because R4 is a sweep of comments and none of them was rewritten.

Every behavioural row runs the composer under `node` in a `vm` sandbox and touches no browser, so the
file contends with nothing else in the tree.

The rows compose over two sources. The first is a handful of records built inside the test file out
of the fields' own definitions, each field set inside its own declared range and no photograph
consulted — so what those rows claim is a claim about the arithmetic. The second is the real per-work
records the settings record ships, read as a smoke input under shelf 20's one lawful use. No row
reports a count, a share or a percentage of either source; where a row fails it names one witness.

The R4 rows are the only ones written against source text rather than behaviour, and they say so.
There is no behaviour to ask: a tally standing as an argument in a comment changes nothing the
composer computes, which is exactly why nothing caught it. They join each run of comment lines into
one block before reading it, so a tally wrapped across two lines is still one tally, and they map the
match back to the line it came from.

---

## Found while reading, outside the four

**A work record without a `readiness` field throws rather than composing.** `pairOf` reads
`fromW.readiness` and hands it to `pairScore`, which indexes it:

```js
    function pairScore(ra, rb) {
      var sa = ra[0], pa = ra[1], sb = rb[0], pb = rb[1];
```

A record carrying only an id — which `passageFor`'s own two refusals accept, since it names an id —
reaches this and throws. Charter shelf 21 says no branch inside the engine may terminate in no
crossing, and a throw is worse than a refusal: on the client's road it is caught and the visitor gets
the walk's plain glide, and on any other road it takes the picture layer down. The neighbouring
readings in this file all answer a missing field with the field's own neutral; this one does not. It
belongs to whoever owns `pairOf`.

**`made.json` is stale as well as `made.bytes`.** R2's block closes it along with the weight, but it
is worth naming separately: any consumer that ships or stores `passageFor(...).json` rather than
`.score` ships a score with no `camera.lead` on it, so a camera-led passage would not lead. Nothing in
this tree does — `engine/client/01a-pass.js` reads `.score` — but the published text and the published
object disagreeing is the kind of thing a later road picks up by accident.

**R2 turned out larger than described.** The task named `overTheFence` and `weightShed`; the same
write also invalidates `bytes` and `json`, and the client independently recomputes the weight off the
raw score, so two readings of one score disagree today on every led passage.

**R1 turned out smaller than described, once the space was enumerated.** The overrun has exactly one
shape — the camera, the ground and colour standing against a ceiling of two — because the pivot is the
only cue `voiceTheCues` can ever voice an accompaniment. That is what makes a repair possible that
costs the crossing no move at all.
