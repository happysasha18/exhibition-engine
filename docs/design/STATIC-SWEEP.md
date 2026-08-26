# Every number on the composition road, and what it stands on

Charter shelf 21's test — could this value have existed before the two pictures in front of it were
known? — applied to every named constant in `engine/assets/pass-composer.js`,
`engine/assets/pass-layer.js`, `engine/client/01a-pass.js`, and to the caps the instrument manifests
publish.

The product of this sweep is not this document. It is the state the three files end up in: **every
named constant carrying its own verdict where it stands.** `tests/test_pass_static.py` reds on every
one that does not, so the class stays closed rather than closed once.

---

## Why a verdict and not a repair list

A number with no sentence beside it reads as measured. That is the mechanism behind every defect
found on this road, and it has now been found five times in five different costumes: a seam score of
nought read as a measurement, a fit of one read as a reading, a strength of nothing read as a
strength, a dropped manifest field read as an instrument declaring nothing, a ladder bucket read as a
property of a photograph. In every case the number was doing exactly what it looked like it was doing,
and what it looked like was measured.

So the repair cannot be a list. A list closes the instances and leaves the rule, and the rule is that
the next number to land arrives naked and reads as measured too — which is exactly how the typed
answer for an instrument with no reading has now come back a third time (§5.3 below).

**The three verdicts.**

**DERIVED.** It answers a question a picture, the walk or the session can answer, and it does — or
the sentence says what it would read and why the derivation is not there yet.

**CAPABILITY.** It is a fact about the machine, the format, the browser or the arithmetic rather than
about pictures. No photograph could answer it, and no photograph should. The sentence says which of
the four, so nobody has to re-litigate it.

**UNJUSTIFIED.** Nobody measured it and nothing derives it. The sentence says plainly that it was
chosen, by whom, and that it stands on nothing. `DOLLY_CAP`'s own comment already does this; the rest
do not.

An UNJUSTIFIED mark is not a defect to be fixed before the file may ship. It is the truth said out
loud, which is what stops the number reading as measured. Several of these numbers should go on
standing exactly as they are — with a sentence.

---

## The convention the row checks

One of the three words, in capitals, in the comment block standing immediately above the declaration.
The row asks nothing more: no format, no tag, no registry, no new file. A word in a sentence.

```js
    // UNJUSTIFIED — how much the day's weather may narrow a ground's own reading. This seat chose
    // 0.35 and nothing measured it; what the number has to satisfy is only that it stays under one,
    // so the day never empties a pool, and every value under one satisfies that equally.
    var WEATHER_AMP = 0.35;
```

**Scope, which is the row's own definition.** A module-scope declaration whose name is in capitals and
whose value carries a digit, plus every numeric member of a module-scope object literal whose own name
is in capitals. Nothing inside a function — because a number that shapes a crossing and lives inside a
function is a number that has not been given a name yet, and **giving it a name is the repair for it**,
after which the row sees it by itself. That is what makes the row total rather than a filter: the
inline class in §5 is answered by naming, not by a second kind of check.

Out of scope by the owner's own boundary: a per-frame percentile over a visitor's own frame times, a
share over one picture's own pixels, a count of instruments or of test rows.

---

## 1. `engine/assets/pass-composer.js`

| constant | verdict | on what |
| --- | --- | --- |
| `ESCAPES` | CAPABILITY | JSON's own escape table — the format says which code points must be written which way |
| `SCHEMA` | CAPABILITY | the score's wire format version, §4.4a; two live at once and this names which is written |
| `TIER_RANK` | **DERIVED** | shelf 17's three rows in their own order. §4a gives the block |
| `TRANSACTION_MS` | **DERIVED** | the top of shelf 17's longest band. §4a gives the block |
| `DOLLY_CAP` | UNJUSTIFIED | already argued in its own prose; it needs the word and one new sentence (§3.1) |
| `INTENT_FENCE_CHARS` | UNJUSTIFIED | the value comes from the client, and the `\|\| 600` fallback beside it does not |
| `RATIO_STEPS` | **DERIVED** | the meshing instrument's own published `rungs`; already derived, needs only the word |
| `SIZE_MIN` / `SIZE_MAX` | **DERIVED** | the same instrument's own published span for its `size` handle; already derived |
| `WEATHER_AMP` | UNJUSTIFIED | see §3.2 |
| `GOLDEN` | CAPABILITY | the golden section — a fact about arithmetic, and its own comment already says so |
| `BEAT_DIAL` | UNJUSTIFIED | carried from the lab's assembler, unmeasured there |
| `VOICE_SHARE` | UNJUSTIFIED | its own comment already admits it: a quarter is a number of taste |
| `VOICE_SEEN` | CAPABILITY | the smallest distinguishable step of an eight-bit channel above the threshold the eye reads |
| `VOICE_RATIOS` | CAPABILITY | which period ratios beat against each other — a fact about arithmetic |
| `VOICE_RATIO_BAND` | UNJUSTIFIED | how near a ratio counts as near; carried from the lab, unmeasured |
| `OCTAVES_PER_SPAN` | UNJUSTIFIED | see §3.3 — the most consequential unmarked number in the file |

### 1.1 `RATIO_STEPS`, `SIZE_MIN`, `SIZE_MAX` — the shape every DERIVED constant should have

```js
    var RATIO_STEPS = MANIFESTS.gears.handles.ratio.rungs || 0;
    var SIZE_MIN = HANDLE_SPECS.gears.size[0];
    var SIZE_MAX = HANDLE_SPECS.gears.size[1];
```

These three are already right. They read the instrument's own published manifest, so a module that
changes its own reach re-bases them by itself and no copy can go stale. They need one word each, and
they are worth naming here as the pattern: **a constant that reads a published fact is not a static
value, it is a cached read.** Every DERIVED block below has this shape.

---

## 2. `engine/assets/pass-layer.js` and `engine/client/01a-pass.js`

| constant | verdict | on what |
| --- | --- | --- |
| `DURATION_MIN` / `DURATION_MAX` | **DERIVED** | §2.5's range, and its ceiling is shelf 17's longest band — one number with three homes today |
| `PREPARE_MIN` / `PREPARE_MAX` | UNJUSTIFIED | §2.5 published 400 ms; no measurement stands behind it |
| `SLACK_MIN` / `SLACK_MAX` | UNJUSTIFIED | the same, for the settle slack |
| `STEPS` | UNJUSTIFIED | see §3.4 |
| `DPR_CAP` | CAPABILITY | the buffer's own ceiling — beyond two the memory buys nothing the eye reads |
| `P95_DROP` | CAPABILITY | thirty frames a second is 33 ms; the release envelope's own number |
| `P95_RAISE`, `WIN_DROP`, `WIN_RAISE`, `KEEP` | UNJUSTIFIED | the hysteresis gap and the three window lengths; chosen |
| `UTYPE` | CAPABILITY | GLSL's own type names, as a lookup |
| `TAU` | CAPABILITY | arithmetic |
| `CAM_OPTIONAL` | CAPABILITY | which camera axes a score may leave unnamed — the contract's own fact |
| `CAM_TURN_FOV` | UNJUSTIFIED | see §3.5 |
| `CAM_REST_TOL` | CAPABILITY | floating point, and its own comment already argues exactly that |
| `CAM_HANDOFF_TOL` | UNJUSTIFIED | a thousandth of a normalised pan is a visible-motion bar, not a float epsilon |
| `REACH_HALVINGS` | CAPABILITY | twenty-four halvings of a unit interval land below any pixel on any screen |
| `HANG_SHARE` | UNJUSTIFIED | the share of a pass the rise and fall take where a score names neither |
| `HELD_MAX` | **DERIVED** | charter shelf 17's own held-time third. §4b gives the sentence |
| `CADENCE_MIN` / `CADENCE_MAX` | UNJUSTIFIED | §2.5's interruption range; chosen |
| `LAST_RESORT_REST_HANDLES` | CAPABILITY | a flag table, not a magnitude |
| `DEAD_AIR_MS` | UNJUSTIFIED | how long a command waits for its instruments; chosen |
| `INST_RETRY_MAX`, `INST_RETRY_BASE_MS` | UNJUSTIFIED | a retry policy; chosen |
| `PASS_LIMITS` | CAPABILITY (four), see §3.6 | already carries the word; two of its seven have been retired and two need re-reading |
| `RECORDS_RETRY_MAX`, `RECORDS_RETRY_BASE_MS` | UNJUSTIFIED | chosen |
| `PASS_EDGE.visitWindowSeconds` | UNJUSTIFIED | half an hour; chosen |
| `PASS_EDGE.cooldownSeconds` | UNJUSTIFIED | a day expressed in seconds — the unit is a fact, the choice of a day is not |
| `PASS_EDGE.driftSpan` | UNJUSTIFIED | how far a family may breathe pass to pass — shelf 16's own idea, this seat's number |
| `PASS_EDGE.driftOpensOver` | UNJUSTIFIED | over how many passes it opens; chosen |
| `PASS_EDGE.dice` | UNJUSTIFIED | its own comment already says it is not a measured floor |
| `PASS_EDGE.keep`, `PASS_EDGE.traceHandles` | UNJUSTIFIED | storage and trace bounds; chosen |
| `PASS_PREWARM_STEPS` | UNJUSTIFIED | how many edges ahead to warm; chosen |
| `PASS_CHROME_MS` | UNJUSTIFIED | six authored timings; taste, and worth saying so rather than reading as measured |
| `PASS_LAYER_HOLD_MS` | UNJUSTIFIED | the window a gesture may land inside a layer's own load; chosen |
| `PASS_OFFER_THROW_MAX` | UNJUSTIFIED | chosen |

**A note on the shared declaration lines.** `DPR_CAP = 2, P95_DROP = 33, P95_RAISE = 22, WIN_DROP =
45, WIN_RAISE = 120, KEEP = 240` is one statement carrying two capabilities and four chosen numbers,
and one comment cannot carry two verdicts honestly. The applier should split it, one verdict per line.
The same holds for `DURATION_MIN, DURATION_MAX`, `PREPARE_MIN, PREPARE_MAX`, `SLACK_MIN, SLACK_MAX`,
`CADENCE_MIN, CADENCE_MAX` and `INST_RETRY_MAX, INST_RETRY_BASE_MS` — splitting them is itself part of
the repair, because a shared line is how a capability and a taste number came to look alike.

---

## 3. The ones worth an argument

### 3.1 `DOLLY_CAP` — UNJUSTIFIED, and now in tension with a whole frame

The comment already says the number is unmeasured. Two things should be added with the word.

The honest bound is named in the comment itself and it is not a number this file can hold: what the
frame can carry is the buffer's own oversampling, a property of the device the composer cannot see.
That derivation exists — `pass-layer.js`'s `camFit` and `REACH_HALVINGS` compute exactly how much of a
pose the carrier can carry — but on the other side of the architecture line, which is where his
decision of 2026-08-17 18:00 puts it. So this is a constant whose derivation is known, lives
elsewhere, and cannot be moved here.

And it is now in real tension with a whole frame: the camera lane has found that the great majority of
corner poses ask for more excursion than a covered frame can carry. A cap that most poses exceed is
not bounding a rare demand; it is bounding the ordinary one. That belongs in the sentence, because the
next reader will otherwise assume a cap this often reached was chosen against something.

### 3.2 `WEATHER_AMP` and its unnamed twin

`WEATHER_AMP = 0.35` bounds the day's bias to a fifth either way of neutral. Its comment argues the
bound's SHAPE — that a day never empties a ground — and that argument is sound and holds for every
value under one. It says nothing about why 0.35 rather than 0.2, because nothing does.

Its twin is unnamed. `viewerBiasOf` opens `var amp = 0.3` inside the function, doing the same job for
the visit's own lingered and skipped letters. Two numbers of the same kind, one named and one not, and
the unnamed one is invisible to every sweep. Naming it is the repair (§5.2).

### 3.3 `OCTAVES_PER_SPAN` — the most consequential unmarked number here

```js
    var OCTAVES_PER_SPAN = 4;
```

No sentence at all, and `acrossTheSpan` reads it for **every travelling handle the composer writes**:

```js
      var d = Math.log2(Math.max(from, 1e-6) / Math.max(to, 1e-6)) / OCTAVES_PER_SPAN;
      d = Math.max(-1, Math.min(1, d)) / 2 * (hi - lo);
```

It says that a ratio of sixteen to one between the two works' readings uses the handle's whole span,
and any wider ratio is clamped to it. So it decides how sensitively every travelling handle answers
the pair — a pair reading three to one apart and a pair reading eight to one apart land at different
places on the same handle precisely because of this number, and every pair past sixteen to one lands
on the same place, which is the clamp defect the camera lane has already named once elsewhere.

Nothing derives it. Mark it UNJUSTIFIED with what it does, because the sentence is what tells the next
reader that the sensitivity of every handle in the file rests on one unmeasured four.

### 3.4 `STEPS` — UNJUSTIFIED, and nearly a ladder

```js
    var STEPS = [1.0, 0.85, 0.72, 0.60, 0.50];
```

The comment beside it argues the ms numbers that walk the ladder and says nothing about the rungs. The
five are very nearly geometric: each is about 0.85 of the one above, so each rung costs about
five-sevenths of the pixels of the one above it, which is a sensible shape for a ladder. They are not
exactly geometric, so they were hand-rounded.

**No block.** A ladder of render scales decides what a real visitor's device actually draws, and
replacing hand-rounded numbers with computed ones changes that on every device for a tidiness gain.
Mark it UNJUSTIFIED, say that it is nearly a geometric ladder of one ratio, and leave the decision to
whoever owns the carrier.

### 3.5 `CAM_TURN_FOV` — a convention is not a measurement

Its comment gives a ground: 0.9 radians is 51.6 degrees across the frame's height, the ordinary lens a
room is photographed with. That is a photographic convention. It is neither a reading of the two
pictures nor a fact about the machine, so under these three verdicts it is UNJUSTIFIED — and the
sentence beside it is already most of what the mark asks for. Adding the word costs nothing and stops
a convention reading as a measurement, which is the whole point.

This is the case the three verdicts handle least comfortably, and it is worth saying so rather than
inventing a fourth. A convention held by people who photograph rooms is a better ground than a number
picked at random, and the mark does not say otherwise. It says only that nothing here measured it.

### 3.6 `PASS_LIMITS` — already marked, and two members need re-reading

Its comment already carries the word CAPABILITY and already argues four of the seven: `camera` and
`curve` fence how much a track may carry, `instruments` how many a transition may name, `text` fences
a name. Those four are capabilities and the sentence says so.

`bytes` and `intent` were both set from tallies over a collection of photographs and both have been
retired from deciding anything in the client, which its comment now records — the last of that class on
this road. They are two literals held in step with the wire until a rebuild retires them, and the
comment says exactly that. Nothing to add.

`phases: 3` carries no argument of its own and is not one of the four the comment defends. It should
be named: either it is the contract's own count of phase windows (a capability) or it is a chosen
ceiling, and the comment does not say which.

---

## 4. The blocks

### 4a. `TIER_RANK` and `TRANSACTION_MS` read shelf 17's own table

Both are copies of numbers that already live in `TIERS` one screen above them. Find:

```js
  var TIER_RANK = { quiet: 0, middle: 1, culmination: 2 };
  var TRANSACTION_MS = 14000;
```

Replace with:

```js
  // DERIVED — the three tiers in their own order, so a role can be asked whether a realised tier
  // reaches it. It reads `TIERS` above rather than restating it, so a row added, removed or reordered
  // there carries this with it and no second copy of shelf 17's ladder can go stale.
  var TIER_RANK = (function () {
    var out = {}, i;
    for (i = 0; i < TIERS.length; i++) out[TIERS[i].tier] = i;
    return out;
  }());
  // DERIVED — the transaction's own ceiling, which is the top of shelf 17's longest band: a
  // culmination runs nine to fourteen seconds and the transaction ends where the longest crossing
  // does. It stood here as a typed 14000, a third copy of one number that also lives in `TIERS`
  // above and in `pass-layer.js`'s own §2.5 range, and three copies of one fact drift. Read from the
  // table, so a change to the charter's own bands carries the ceiling with it.
  var TRANSACTION_MS = (function () {
    var top = 0, i;
    for (i = 0; i < TIERS.length; i++) if (TIERS[i].band[1] > top) top = TIERS[i].band[1];
    return top;
  }());
```

**Verified**: applied to a scratch copy, every passage composed over the five route roles is
byte-identical to the file as it stands, and the exported `tierBands` are unchanged. The block is a
rename of a fact, not a change to one — which it must be, since both values are already what the
table says.

`pass-layer.js`'s `DURATION_MAX` is the third copy. It cannot read `TIERS` — it is on the other side
of the line and the layer must enforce §2.5 whatever the composer thinks — so it stays a literal, and
its sentence should name the other two homes so a future drift is visible. `tests/test_pass_static.py`
row two holds the composer's two together and reds if they part.

### 4b. `HELD_MAX` carries its shelf

Find, in `pass-layer.js`:

```js
  var HELD_MAX = 1 / 3;
```

Replace with:

```js
  // DERIVED — charter shelf 17's own held-time law, in the shelf's own words: held time, the vistas
  // and the crests together, stays under a third of the crossing. It is written as a third rather
  // than as 0.3333 so the shelf's own sentence is legible in the number, and the shelf is the one
  // home of the fact. The shelf's numbers were agent-authored in `ae2b5da` and amended on his word of
  // 2026-08-18 to shape a crossing rather than refuse one, which the shelf records; that provenance
  // belongs to the shelf and not to this line.
  var HELD_MAX = 1 / 3;
```

### 4c. Marking the rest

Every remaining row of §1 and §2 is one sentence carrying one word, written where the constant stands.
They are not reproduced here one by one because the sentence is the repair and the table above says
what each must say. Two rules for whoever writes them:

**A CAPABILITY sentence names which of the four it is** — the machine, the format, the browser or the
arithmetic — and what would have to change for the number to change. `CAM_REST_TOL`'s comment is the
model: it says the check reads the pose rather than the picture, so the number is a computation
tolerance and not a matter of taste.

**An UNJUSTIFIED sentence names who chose it and says it stands on nothing.** `VOICE_SHARE`'s comment
is the model: it quotes the lab's own admission that a quarter is a number of taste and says it is
carried here as that same admitted number, not re-derived as if it were one. What an UNJUSTIFIED
sentence must not do is argue the number's *shape* and let that read as arguing the number —
`WEATHER_AMP`'s comment does exactly that today, and it is why that number reads as settled.

---

## 5. The numbers with no name, and the repair that is naming them

The row in `tests/test_pass_static.py` sees named constants. A bare literal inline in an expression is
invisible to it, and to every reader who is not looking straight at that line. **The repair for an
inline number that shapes a crossing is to give it a name**, after which it falls inside the row by
itself. These are the ones on this road today.

### 5.1 `interruption: { withinMs: 500 }` — composer, in the plan's own record

Every plan the composer writes carries the same 500. `pass-layer.js` clamps it into `[CADENCE_MIN,
CADENCE_MAX]` and travels every handle to the landing door inside it. It is the one number that decides
what an interrupted crossing feels like, it is the same on a two-second quiet link and a fourteen-second
culmination, and it is written inline in a record literal where nothing will ever find it.

**Verdict: UNJUSTIFIED, and it should be named first.** A derivation is available in principle — an
interruption cadence could be a share of the crossing's own length, which the plan has in hand — but
every share is itself a number nobody measured, so deriving it would trade one unjustified number for
another while looking like progress. Name it, mark it, and leave the derivation to whoever can measure
what an interrupted crossing should feel like.

```js
  // UNJUSTIFIED — how long an interrupted crossing has to travel its handles to the door the visit
  // is landing on (§2.5, charter shelf 19). This seat chose half a second; nothing measured it, and
  // it is the same half second on the shortest quiet link and the longest culmination. A share of
  // the crossing's own length is derivable from the plan and would answer better, but every share is
  // itself a number nobody has measured, so naming this one is the honest step and deriving it is
  // not.
  var INTERRUPTION_MS = 500;
```

and in the plan record, `interruption: { withinMs: INTERRUPTION_MS, resolve: "nearest-door" }`.

### 5.2 `viewerBiasOf`'s `amp` — composer

```js
      var amp = 0.3, bias = 1;
```

The twin of `WEATHER_AMP`, doing the same job for the visit's own memory, inside a function where no
sweep can see it. Lift it beside `WEATHER_AMP` as `VIEWER_AMP` and mark both UNJUSTIFIED. Two numbers
of one kind should stand together, if only so the next reader asks why they differ.

### 5.3 `suitsPair`'s typed answer — DERIVED, and the same defect for the third time

```js
    function suitsPair(iid, a, b) {
      var ask = INSTRUMENT_SUITS[iid];
      if (!ask) {
        return [0.5, "«" + iid + "» publishes no reading of a pair, so it suits this one no more "
                + "and no less than any other"];
      }
```

An instrument that publishes no reading of a pair ranks at a typed 0.5 against measured rivals — on
every pair, in both directions, permanently, on no evidence. The file has already named this defect
twice in its own comments and repaired it twice by giving that one instrument a row. Repairing the
instance leaves the rule, and **the rule has just produced three more**: `pour`, `veil` and `wind`
have landed with manifests and no `suits` row, and each is ranked today by this number. Row three of
`tests/test_pass_static.py` reds on exactly that.

The comment's own sentence says what the right answer is — no more and no less than any other — and
0.5 is not it. It is the middle of the SCALE, and what the sentence promises is the middle of the
POOL: where the instruments that did read this pair actually landed. That is a reading of the pair,
taken through its rivals' readings of it, and it is derivable with nothing new.

**Block, three parts.** First, the function stops typing a number:

```js
      if (!ask) {
        // DERIVED — an instrument that publishes no reading of a pair says so, and `rankUnread`
        // below places it where the pool it competes in actually landed for THIS pair. A typed 0.5
        // stood here and it is the middle of the SCALE, not of the pool: against rivals reading low
        // it towered and against rivals reading high it vanished, on every pair alike, and the file
        // has already named that defect twice and repaired it one instrument at a time. The comment
        // that stood here already said the right answer — no more and no less than any other — and
        // a number typed in this file cannot mean it.
        return [null, "«" + iid + "» publishes no reading of a pair, so it suits this one no more "
                + "and no less than any other"];
      }
```

Second, one helper beside `bestFilling`:

```js
    // WHERE AN UNREAD INSTRUMENT STANDS IN THE POOL IT COMPETES IN, which is the middle of what its
    // rivals read for this pair — a reading of the pair taken through the instruments that did read
    // it, and never a number written here. Where no instrument in the pool read the pair at all,
    // every fit is nothing and `dieWeighted`'s own even roll answers, which is what "no more and no
    // less than any other" means when there is nothing to be no more than.
    function rankUnread(pool) {
      var sum = 0, read = 0, i;
      for (i = 0; i < pool.length; i++) {
        if (typeof pool[i].fit === "number") { sum += pool[i].fit; read += 1; }
      }
      var middle = read ? sum / read : 0;
      for (i = 0; i < pool.length; i++) {
        if (typeof pool[i].fit !== "number") pool[i].fit = middle;
      }
      return pool;
    }
```

Third, the two pools that reach a die read it. In `bestFilling`:

```js
      return dieWeighted(rankUnread(pool), seed, key + "|ground-fills", 1);
```

and in `castForKinds`, where the candidates are split into tiers and the first non-empty tier is
rolled:

```js
          return [dieWeighted(rankUnread(tiers[i]), seed, key + "|" + list.join("+") + "|" + slot,
                              1), said, cutters, false];
```

The diagnostic line just above it must stop rounding a null:

```js
        said.push({ instrument: iid, fit: answer[0] === null ? null : r4(answer[0]), cuts: cuts,
                    why: answer[1], order: order });
```

**Verified**: applied to a scratch copy, it runs on every composed passage without throwing, and it
moves the cast wherever one of the three unread instruments stands in the pool — which is the point.

**What the applier must check.** This one changes compositions, unlike §4a. Every golden pinned to a
passage whose pool contained `pour`, `veil` or `wind` legitimately moves. It should land separately
from the comment-only marks, which move nothing at all. And it does not excuse the three missing rows:
an instrument that says nothing about which pairs it suits is a gap in that instrument, and row three
goes on reding until each has one.

### 5.4 The die's own resolution

`dieAmong(seed, key, 1000000)` in `dieWeighted`, and `4294967296` in the client's `passMix`. Both are
the resolution of an integer roll — the first a millionth of the summed weight, the second two to the
thirty-second. **CAPABILITY**, both: facts about integer arithmetic and nothing else. They deserve a
name and a word for the same reason as the rest, and no derivation.

---

## 6. The instrument manifests' published caps

The rule first, because it is one rule with two halves and the halves have different verdicts.

**A handle's `min` and `max` are a CAPABILITY of that instrument.** They are the module's own
declaration of how far it can draw the thing that handle drives, in the module's own units. No
photograph could answer how far a shader may push its own dial, and the composer's own law already
treats them that way: a reading that is a share is placed on a handle that is a share, in the unit it
is already in, and nothing here invents a scale. A cap that is wrong is a fact about the module and is
repaired in the module.

**A handle's `def` is the module's own rest, and it is a number that shapes a crossing whenever the
composer drives nothing.** That is not a capability: it is what plays. The composer already knows
which ones those are — `HANDLE_SOURCE`'s `module-rest` rows name every handle riding on a default,
with a sentence each. All but one fall into two lawful groups: a judge channel, which rests because
resting is what it is for, and the studio instrument's operation switches, which are on-or-off
selectors with no measurement that could answer them. Both are honest CAPABILITY marks. The one that
is neither is `strata-scale`'s `handover`, designed in `docs/design/PALETTE-RUNG.md` §7.

**The rule to write into `HANDLE_SOURCE`'s own header**, so the next handle to land is judged rather
than defaulted: a `module-rest` row is lawful where the handle is a judge channel or a selector with
nothing to read, and is UNJUSTIFIED where the handle is a continuous value the record could answer.

### 6.1 What the fleet sweep found, and it is worse than the rule predicted

A sweep of all 27 published manifests, loaded and read rather than grepped, turns up four things.

**Every instrument declares the same cost, and it declares nothing.** All 27 manifests publish one
byte-identical `resources` block, and it is identical across `lean`, `standard` and `rich`:

```
textures: 0, textureSlots: 2, framebuffers: 0, pingPong: 0, programs: 1, passes: 1, bytesEstimate: 0
```

One distinct declaration in the whole fleet, repeated fifty-four times more. Two consequences follow
by construction, neither of them about any pair.

The quality ladder declares no cost difference between its rungs, so `resourcesBlock(variant)` writes
the same numbers into all three quality blocks of every score, and the tier a device lands on cannot
be chosen on what a crossing would cost — because nothing published says one crossing costs more than
another. That is a whole declared capability standing at a constant.

And `bytesEstimate: 0` is not an omission, it is a false declaration. `PASS-API-V1.md`'s conformance
row 22 reads that a resource declaration understating its bytes reds, alongside one understating its
counts. Every instrument in the fleet understates its bytes, by all of them. Either row 22 is unwritten
or it passes vacuously, and both readings are worth someone's attention.

**Verdict: UNJUSTIFIED, all seven numbers, in all 27 files.** They are not capabilities — a capability
is a fact about the machine, and a zero written where a real byte count belongs is a fact about
nobody. The mark should say that the block is a placeholder carried across the fleet unchanged, so it
stops reading as twenty-seven independent measurements agreeing.

**One instrument's clock runs past the transaction it plays inside.** Every `clock` handle in the
fleet publishes a span of 0 to 14 seconds, which `kaleidoscope.js`'s own comment names as §2.5's
transaction bound. `hero`'s publishes 0 to 3600. A score cannot drive a clock past the transaction's
own end — the transaction is over — so the span above 14 is unreachable by construction, and a handle
whose published span is mostly unreachable is a cap that says something false about the module.
Whether the repair is the manifest or the bound is the module owner's call; that it is one of these is
not.

**`planet.js` publishes `suits:` twice in one object literal** — a literal block naming the fields it
reads, and later `suits: suitsPair` naming a function. The second silently wins, which is what a
duplicate key in an object literal does, and the first is dead text that reads as live. Not a number,
but exactly the mechanism this sweep is about: a declaration that reads as doing something and does
nothing.

**`params: {}` is empty in `strata-light` and `strata-scale`** while both publish 22 handles. A
reader asking what either instrument's parameters are is told: none.

### 6.2 What the sweep did not confirm

The fan-out reported that an instrument publishing no `cuts` line is named UNPLACED by the settings
build and filtered out of `ALL_INSTRUMENTS`, and that twelve of the 27 publish no `cuts`. The second
half is confirmed — `boxfold`, `gears`, `hero`, `liquid`, `livemirror`, `matter`, `overlay`,
`parquet`, `planet`, `tunnel`, `unfold` and `weave` declare none. **The first half is not**, and the
evidence is against it: several of those twelve are cast in ordinary compositions, so a missing `cuts`
line evidently makes an instrument a non-cutter and not an absent one. It is recorded here as
unconfirmed rather than repeated as fact, because a claim that twelve instruments are unreachable
would be the single largest finding of the night if it were true, and it should be established rather
than inherited.

### 6.3 The verdict convention inside the instrument files

The fleet carries hundreds of module-scope constants and most already carry a sentence — often a good
one, citing the lab module the number came from digit for digit. What almost none of them carry is the
KIND of that provenance, which is the whole point of the mark: `MEASURED`, `CAPABILITY` and `CHOSEN`
read very differently and today they all read the same.

Two patterns are worth naming because they are already right and should be the model. The `0.5/255`
family — `DOOR_SHOW`, `DOOR_OPEN` — appears in fourteen instruments and is everywhere justified as
half a level of 255, the eight-bit channel's own quantum, held against the charter's own door bar.
That is a textbook CAPABILITY sentence. And the response curves — `FEEL_*`, `CURVES`, `CURVE_BANDS`,
`CURVE_MEASURED_ON` — carry the measurement they were fitted on, sometimes in the constant's own name.
That is a textbook DERIVED sentence.

Against them stand constants published straight onto a handle's own bounds with no sentence at all:
`weave`'s `WAVE_PERIOD_MIN`, `WAVE_PERIOD_MAX` and `WAVE_DRIFT_MAX`, which become the `wavePeriod` and
`waveDrift` spans; `overlay`'s `PERIOD_MIN`/`PERIOD_MAX` and `SCALE_MIN`/`SCALE_MAX`; `lens`'s whole
resting block; `tunnel`'s `REPS_*` and `Z0`; and `veil`'s `DEPTH_MARGIN`, which is bare in the file and
then published into the manifest as part of a field literally named `reachIsDerived`. A number called
derived that carries no derivation is the sharpest form of the mechanism this sweep exists for.

**Extending row one to the 27 instrument files is the right end state and is not proposed as one
change.** It would red on hundreds of constants at once, which is a wall rather than a signal. The
staged shape: mark the three road files first (row one as it stands), then the handle-bound constants
— the ones that become a published `min`, `max` or `def`, which is where a module's number reaches a
crossing — then the rest.

## 7. The rows

`tests/test_pass_static.py`. Five rows: one drift guard that passes today, four that red.

**Row one** reds on every named constant on the three road files whose comment carries none of the
three words. It names the file, the line, the constant, and whether it has no sentence at all or a
sentence that names no verdict. Today it names 47. **This is the row that keeps the class closed** —
a number that lands tomorrow with no sentence beside it reds on the run it lands, which is the only
thing that stops this sweep being a document about a moment.

**Row two** is a drift guard rather than a defect row, and it passes today: the composer's transaction
ceiling and the top of shelf 17's longest band are one number, and it reds if the two ever part. It is
the guard for §4a's block — the block gives the number one home, and this row notices if a second one
grows back.

**Row three** reds on every instrument the arsenal publishes that publishes no reading of a pair.
Today it names three, and §5.3 is why that matters.

**Row four** reds because the whole fleet declares one byte-identical cost block, repeated across all
27 instruments and all three quality variants.

**Row five** reds on a handle whose published span runs past the transaction it plays inside.

Rows four and five load each instrument file and read the manifest it actually registers, rather than
grepping for it, so a module that changes its own declaration re-bases them by itself.

**What no row here does** is extend row one across the 27 instrument files. §6.3 says why: it would
red on hundreds of constants at once, which is a wall rather than a signal, and the staged shape is
written there.
