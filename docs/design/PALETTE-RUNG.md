# The palette rung, and two of shelf 12's open decompositions

Two designs. The first is a defect at the source: a work-record field whose definition is a statistic
over the collection, read by the composer to decide a crossing and by the harmonic layer to name a
key. The second is charter shelf 12 — what the complement law and the parting-by-scale handover would
each take.

Every anchor below is quoted with enough surrounding text to find it after a reflow. Where a line
number appears it is where the text stood at the time of writing.

The rows that prove the first design are in `tests/test_pass_palette.py`. All three are red against
the trees as they stand.

---

# Part one — `palette.rung`

## 1. The mechanism, end to end

### Where the rung is computed

`/Users/sashaabramovich/tlvphotos/lab/step1-tone-texture.py`, function `classify_tone(records)`. It
takes the whole collection and returns the thresholds it cut it at:

```python
def classify_tone(records):
    def q75(key):
        vals = sorted(r["tone"][key] for r in records)
        return vals[q_index(len(vals))]

    thr = {k: q75(k) for k in ("axis_ratio", "tone_hue_corr", "hue_R", "hue_entropy")}
    thr["chroma_present"] = NAIVE["chroma_present"]
    for r in records:
        t = r["tone"]
        if t["chroma_p90"] < thr["chroma_present"]:
            rung = "чёрно-белое"
        elif t["axis_ratio"] >= thr["axis_ratio"] and t["tone_hue_corr"] >= thr["tone_hue_corr"]:
            rung = "дутон"
        elif t["hue_R"] >= thr["hue_R"]:
            rung = "тонировка"
        elif t["hue_entropy"] >= thr["hue_entropy"]:
            rung = "полный цвет"
        else:
            rung = "ограниченный цвет"
```

with, in the same file:

```python
QUARTER = 0.25

def q_index(n):
    return min(n - 1, math.ceil(n * (1 - QUARTER)))
```

One of the five branches reads an absolute number: a picture whose ninetieth-percentile CIELAB chroma
falls under six chroma units is grey, and six chroma units is where the eye stops calling it colour.
**The other four read the collection.** Each threshold is the value standing at the top-quarter index
of every work's reading on that measure, sorted.

### How it reaches the engine

| step | file | what happens |
| --- | --- | --- |
| 1 | `tlvphotos/lab/step1-tone-texture.py`, `classify_tone` | `tone.rung` and `tone.rung_index` written per work |
| 2 | `tlvphotos/lab/data/tone-texture.json` | stored, with the thresholds beside them |
| 3 | `tlvphotos-u27/lab/build-elements-v1.py`, the `"palette"` literal | `"rung": tone["rung"]` into the dossier |
| 4 | `tlvphotos-u27/lab/build-workrecords-v1.py`, the `records[wid] = {...}` literal in `main()` | `"palette": {"rung": ..., "hues": ..., "hueConcentration": ..., "colourfulness": ...}` — the shipped block, four fields, everything else dropped |
| 5 | `work-records.json` → the instance's `site.json` under `pass.works` | |
| 6 | `engine/build.py`, the EX-PASS-RECORDS block | `records = block.pop("works")` → written out as `pass-workrecords.json`, a static asset |
| 7 | `engine/assets/worker.js` → the client → `passageFor` | the composer reads it |

The work-record builder lives in a third checkout, `~/tlvphotos-u27`, not in `~/tlvphotos`. Both are
read-only from here; the blocks in §5 are for their owners.

### Adding one photograph moves an existing work's rung — by construction

Let the collection hold `n` works and let their readings on one of the four measures, sorted
ascending, be `v[0] … v[n-1]`. The threshold is `v[q_index(n)]` and a work is on the high side of that
branch when its own reading is at or above it.

Hang one more photograph, `P`, whose reading on that measure sits at or above the current threshold.
The sorted list now holds `n + 1` values; every value that stood at or above the old threshold keeps
its own number and gains one rank, and the new threshold is `v'[q_index(n + 1)]`.

`q_index(n + 1) - q_index(n)` is `ceil(0.75(n+1)) - ceil(0.75n)` wherever neither is capped by `n-1`,
which is nought or one, and it is one for three values of `n` in every four. Where it is one, the new
threshold is the next distinct value up the list, which is strictly larger whenever the two are
distinct.

**Every existing work whose reading lies at or above the old threshold and below the new one changes
branch.** It was on the high side; it is now on the low side. Nothing about that photograph moved.
Its rung moved because another photograph was hung.

The argument holds for any `n`, any readings and any `P`. It is a statement about `q_index` and about
sorting, not about the works on any wall.

### The same formula at a small wall, which shelf 21 requires to work

`q_index(n) = min(n - 1, ceil(0.75n))`, and `ceil(0.75n)` is at or above `n - 1` for every `n` up to
seven. So on a wall of seven pictures or fewer **the threshold is the largest reading in the
collection**, and since the branch tests `>=`, at most one picture can stand on the high side of each
measure — whatever the pictures are.

At `n = 1` it is worse than that. `q_index(1) = 0`, the threshold is the single work's own reading,
and the work clears its own threshold on every measure. **Any photograph that is not grey, alone on a
wall, is a duotone.** The same photograph beside a hundred others is whatever the hundred make it.

Charter shelf 21: the engine holds only the list of pictures that exist and derives everything from
that list, for any number of pictures. A field defined this way is not merely biased at a small wall,
it is undefined as a property of a photograph at any wall size.

### How it reaches a pair that neither photograph belongs to

`engine/assets/pass-composer.js`, in `groundCandidates`, under the comment opening `THE SHARED
PALETTE REGION. Its strength is the share of the departing work's own hues`:

```js
      var ra = (a.palette || {}).rung, rb = (b.palette || {}).rung;
      var mine = (a.palette || {}).hues || [], theirs = (b.palette || {}).hues || [], hues = [];
      for (i = 0; i < mine.length; i++) if (theirs.indexOf(mine[i]) >= 0) hues.push(mine[i]);
      hues.sort();
      var paletteShare = (ra === rb && mine.length) ? hues.length / mine.length : 0;
```

The candidate goes into `dieWeighted`, whose whole body is the reach:

```js
      for (i = 0; i < pool.length; i++) {
        w.push(Math.max(0, Number(pool[i].fit) || 0) * ... );
        total += w[i];
      }
      if (!(total > 0)) return pool[dieAmong(seed, key, pool.length)].id;
      var at = dieAmong(seed, key, 1000000) / 1000000 * total, run = 0;
      for (i = 0; i < pool.length; i++) {
        run += w[i];
        if (at < run) return pool[i].id;
      }
```

Two consequences, both by construction and neither about any particular pair.

**The palette ground becomes unreachable, not merely unlikely.** A candidate whose weight is exactly
nought occupies a stretch of the running sum of exactly nought width, so `at < run` is never first
satisfied there while any rival carries weight. The gate does not lower the odds; it removes the
ground.

**Every other ground moves too.** `at` is a fraction of `total`, and `total` is the sum over the whole
pool. Taking one candidate's weight out shrinks `total`, so the same die value lands at a different
point in the running sum and a *different structural measure* can win. The witness the test names
shows exactly that: with the two works labelled alike the pair crosses on one shared measure with the
family `tile_crossfade+texture`; with the same two works labelled one rung apart it crosses on
another shared measure with the family `object_reveal+texture`. Neither family has anything to do
with colour.

The family is what §4.8 matches a return against. So hanging one photograph on the wall can change,
for two other photographs, which ground they cross on, which transform their pivot makes, and whether
the way back is kin to the way out.

### And it reaches shelf 15's key

`engine/client/01a-pass.js`, the harmonic layer:

```js
    const world = pal ? (pal.hues.length ? pal.hues[0] : pal.rung) : null;
```

A work's palette world is the hue it leads with, **or its rung where it leads with no hue at all**.
`palette.hues` admits only colour clusters above a fixed saturation and above a fixed share of the
frame, and is capped at three, so a grey or near-grey photograph carries no hues and its key *is* its
rung. Two functions read that key:

```js
    function passKeysTwoAxesApart(a, b) {
      if (!a || !b) return false;
      return a.matter !== b.matter && a.palette !== b.palette;
    }
```

```js
      sum += at >= 0 ? pal.hold / (1 + at) : (pal.rung === key.palette ? pal.hold : 0);
```

So whether the allusion law fires between two works — the charter's two-axes-changed rule, which
shelf 15 makes the key change — can move when a third photograph is hung. That is the same defect
reaching a second law.

### The second law the same expression breaks, on its own account

`ra === rb` is an equality between two bucket names, and an equality is a **gate**. Two works standing
a hair apart on the ladder, in different buckets, read exactly nothing on this ground however much
hue they share; two works both dropped into the leftover bucket — the one the producer's own docstring
says does not discriminate — read as standing on one rung of the ladder.

This is the disease `groundReadings` a few screens above was already cured of, in that function's own
words: two verdicts asked whether both works cleared a threshold, and between them they turned a
ranking question into an admission test. His word of 2026-08-18 09:51 is that a measurement ranks
which genre suits a pair and shapes the one that wins, and never admits and never rejects. This line
kept the admission test.

**So the repair has two halves and both are needed.** Making the rung absolute stops the collection
deciding; it does not stop a name being used as a gate. Ranking on a coordinate instead of gating on
a name stops the gate; it does not stop the harmonic key moving when a photograph is hung.

## 2. What a rung is FOR, and the reading that answers the same question

A rung names a palette world: the region of colour space a picture lives in. Grey; a picture whose
colour lies on one line through the neutral point; a picture whose colour sits in one hue; a picture
whose palette is wide. That is a fact about a photograph, and every measure it is read from is already
a fact about a photograph, read off that photograph's own pixels:

| measure | what it is | range |
| --- | --- | --- |
| `chroma_p90` | ninetieth percentile of CIELAB chroma over the frame | chroma units, absolute |
| `axis_ratio` | one minus the ratio of the two eigenvalues of the colour cloud's second-moment matrix | 0 to 1 by construction |
| `tone_hue_corr` | absolute correlation between lightness and the signed projection of colour on the cloud's principal axis | 0 to 1 by construction |
| `hue_entropy` | entropy of the chroma-weighted hue histogram, divided by the log of its bin count | 0 to 1 by construction |
| `hue_R` | resultant length of the same histogram | 0 to 1 by construction |

Only the cuts read the collection. The readings never did.

**The continuous coordinate already exists, and it already ships.** The same producer computes:

```python
    amount = min(1.0, chroma_p90 / 40.0)
    spread = hue_entropy
    ladder_position = 0.5 * amount + 0.5 * spread
```

Half how much colour is present, against a fixed perceptual anchor; half how wide it is spread,
already normalised. Both halves are nought at grey and one at a frankly polychrome frame, so the
coordinate lies in `[0, 1]` by construction for any photograph, on any wall, alone or beside a
thousand. And `tlvphotos-u27/lab/build-elements-v1.py` publishes it into the dossier under the name
`colourfulness`, which `build-workrecords-v1.py` carries onto the wire — so the composer has it in
hand today, at `palette.colourfulness`, and `measuredParts` already reads it.

**A correction, and it is mine.** `docs/design/COMPOSER-REPAIRS.md` listed `palette.colourfulness`
beside `palette.rung` as a field whose definition is a statistic over the collection. That is wrong.
It is `ladder_position` renamed, and the formula above touches no other photograph. I took the claim
from the composer's own comments, which describe the field in five or six places as where a work sits
on the collection's own colourfulness ladder — a description that is false as of the producer on
disk. The buckets on that ladder are collection-relative; the coordinate along it is not, and the
comments conflate them. Reading a comment instead of the producer is exactly the failure shelf 20's
own repair is about, and it is corrected in that document.

The wrong description travels, so it is worth pinning. In `pass-composer.js` it stands in the
`HANDLE_SOURCE` row for `grid-colour`'s `lead`, in `measuredParts` where `colourfulness` is read, and
in four or five comments recording the 2026-08-18/19 move of the tonal readings onto
`luminance.level` — search for the phrase about the collection's own colourfulness ladder. It stands
again in `pass-inst-strata-light.js` and in `tests/test_pass_strata-light.py`, where a row asserts the
instrument reads `luminance.level` *because* colourfulness reads a collection ladder. The move onto
`luminance.level` was right for its own reason — shelf 12 defines the tonal decomposition as luminance
zones, so a tonal reading must read a tone and not a colourfulness — and that reason stands on its
own. Only the sentence about the ladder goes.

**What is lost.** Nothing the composer was using. The five names stay: they are a vocabulary a person
can say, the diagnostic surface prints them, and the harmonic layer names a key with one. What
changes is that the name becomes a fact about one photograph.

**What is gained.** Two works a hair apart in colour space stop reading exactly nothing. Two grey
frames read as sharing the grey end of the ladder rather than as sharing nothing, because neither has
a hue to overlap. Hanging a photograph cannot move an existing crossing. And a wall of two pictures
gets rungs that mean what they say.

## 3. Everything that reads it

**In the composer, `engine/assets/pass-composer.js`:**

- `groundCandidates`, the shared palette region — reads both rungs as an equality gate, and carries
  `rung: ra` onto the candidate. **This is the only place a rung decides anything.**
- `pivotOfPair`, the `shared-palette-region` branch — carries `rung: chosen.rung` into the pivot's
  value, where it is a diagnostic and reaches no handle and no score field.
- The `voidAr` handle-provenance prose names the field as one the record carries and no channel
  reads. Documentation of absence.

**In the harmonic layer, `engine/client/01a-pass.js`:** `passPaletteOf` reads it, `passWorkKey` makes
it the palette axis of a work with no hue, `passKeyName` prints it, `passSameKey` and
`passKeysTwoAxesApart` compare it, and `passStandingIn` scores a match on it as the work's whole hold.
Everything downstream — modulation, the pivot work, era and reprise detection, the `standing` array
and the diagnostic surface — reads those.

**In `engine/assets/exhibition.js`:** the same code. That file is generated — `engine/build.py`
reassembles it from the fragments in `engine/client/` as the first act of every bake, and the two
blocks are byte-identical. **It is not a second place to edit.**

**In the instruments:** `pass-inst-grid-colour.js` names `palette.rung` in one handle's manifest
prose as a field it deliberately does not read. A declared non-reader; nothing to change.

**In the tests:** `fixture_pass_works.json` and `fixture_pass_composed.json` carry real rung strings.
`test_pass_composed.py` sets a placeholder rung in its full record and ships an empty palette block in
its bare one. `test_pass_lawful.py` sets placeholder rungs on two constructed records.
`test_pass_harmony.py` never sets a rung at all, so the branch in `passWorkKey` that names a key from
one is untested there — worth a row of its own once the definition is settled.

**Producer side:** `step1-tone-texture.py` writes it, `step1-axes.py` copies it into `work-axes.json`
and runs the discrimination table over it, `build-elements-v1.py` puts it in the dossier and again in
one element-set provenance record (dropped before the wire), and `build-workrecords-v1.py` ships it.

**Nothing else reads a palette rung.** Every other `rung` in either tree is the render-quality ladder,
the story-retry ladder, or a handle's enum steps.

## 4. The harmonic layer needs no change

Its use of the rung is to NAME the palette world of a work that leads with no hue. That is what a name
is for, and once §5's producer block makes the name a fact about one photograph the layer is lawful
exactly as it stands. This is worth saying out loud because the layer is the loudest reader: it would
be a mistake to teach it a coordinate when what it wants is a word.

## 5. The blocks

### 5a. Producer — the rung is named from one picture's own readings

`/Users/sashaabramovich/tlvphotos/lab/step1-tone-texture.py`. Replace `classify_tone` whole:

```python
def classify_tone(records):
    """The ladder's rung, named from ONE picture's own five readings and from nothing else.

    WHAT THIS REPLACES, AND WHY IT COULD NOT STAND. Four of the five cuts were the
    collection's own top quarter on their defining measure: `sorted()` over every
    work's reading and the value at the top-quarter index. So the rung a photograph
    stood on was not a fact about that photograph — it was a statement about the
    other photographs it happened to be measured beside, and hanging one more
    picture moved it. It moved a crossing with it: the engine's own
    `groundCandidates` compares two works' rungs, so a third photograph could change
    which ground two others cross on, and the walk's harmonic layer names a work's
    key by its rung where the work leads with no hue, so a third photograph could
    change whether the allusion law fires between two others. Charter shelf 20
    forbids a statistic over the collection deciding any behaviour of the engine;
    shelf 21 asks the engine to work with any number of pictures, and at a wall of
    seven or fewer the top-quarter index IS the maximum, so at most one picture
    could stand on the high side of each measure however the pictures looked. Alone
    on a wall, every picture that was not grey came out a duotone.

    THE ANCHORS ARE ALREADY WRITTEN AND THEY WERE ALREADY ABSOLUTE. NAIVE holds
    round numbers chosen for what they MEAN, written down before any distribution
    was looked at (cut-lines.py's discipline), and every measure they are compared
    against is already a per-picture reading with its own natural range: CIELAB
    chroma units, a ratio of two eigenvalues, an absolute correlation, a resultant
    length and a normalised entropy, the last four of them in 0..1 by construction.

    WHAT WAS SAID AGAINST THEM DOES NOT SURVIVE THE SHELF. The first draft used
    them and was replaced because the shares they produced ran past a quarter of the
    collection on one value — the project's own discrimination rule. That rule is a
    tally over the collection deciding a behaviour, which is the class shelf 20
    strikes, so it cannot be the reason a per-picture reading gives way to one that
    is not. Whether a rung is rare on some particular wall is a fact about that wall.
    """
    thr = {
        "chroma_present": NAIVE["chroma_present"],
        "axis_ratio": NAIVE["axis_ratio_line"],
        "tone_hue_corr": NAIVE["tone_hue_corr"],
        "hue_R": NAIVE["hue_R_tint"],
        "hue_entropy": NAIVE["hue_entropy_narrow"],
    }
    for r in records:
        t = r["tone"]
        if t["chroma_p90"] < thr["chroma_present"]:
            rung = "чёрно-белое"
        elif t["axis_ratio"] >= thr["axis_ratio"] and t["tone_hue_corr"] >= thr["tone_hue_corr"]:
            rung = "дутон"
        elif t["hue_R"] >= thr["hue_R"]:
            rung = "тонировка"
        elif t["hue_entropy"] >= thr["hue_entropy"]:
            rung = "полный цвет"
        else:
            rung = "ограниченный цвет"
        t["rung"] = rung
        t["rung_index"] = RUNGS.index(rung)
    return {k: round(float(v), 4) for k, v in thr.items()}
```

The five branches are untouched; only where their cuts come from changes. `NAIVE` already carries all
five anchors, under names that say what each boundary means: chroma below which the eye reads grey,
the colour cloud collapsed onto one line, hue actually following lightness, colour sitting in one hue,
and the palette confined to a sector. Read the last as the boundary rather than as the side of it: a
hue entropy at or above it is a wide palette.

Two companions in the same file, both required for the same reason:

- The module docstring's `rung` entry says the other named rungs are read against the collection's own
  top quarter, and the `DISCRIMINATION` paragraph makes that a virtue. Both must go with the code.
- The run log and the stats block count how many works landed on each rung and flag a rung carrying
  more than a quarter. That is a tally over the collection, reported. The log should name the rung
  each work got; how many got each is not a fact about the engine.

`step1-axes.py`'s discrimination table over `tone.rung` is the same tally under another roof and goes
with them.

### 5b. Composer — the reading ranks, and it reads no name

`engine/assets/pass-composer.js`, in `groundCandidates`. Find the block whose comment opens `THE
SHARED PALETTE REGION. Its strength is the share of the departing work's own hues` and whose code
reads:

```js
      var ra = (a.palette || {}).rung, rb = (b.palette || {}).rung;
      var mine = (a.palette || {}).hues || [], theirs = (b.palette || {}).hues || [], hues = [];
      for (i = 0; i < mine.length; i++) if (theirs.indexOf(mine[i]) >= 0) hues.push(mine[i]);
      hues.sort();
      var paletteShare = (ra === rb && mine.length) ? hues.length / mine.length : 0;
```

Replace those five lines with:

```js
      // WHAT WENT, AND WHY IT COULD NOT STAND. This read `ra === rb` — the two works' ladder RUNGS,
      // equal or not — as a gate in front of the share, and one expression broke two laws.
      //
      // The rung is a bucket whose four coloured cuts are the collection's own top quarter on their
      // defining measure (the record builder's `classify_tone`), so which rung a photograph stands
      // on is a statement about the OTHER photographs it was measured beside. Hanging one more
      // picture moves an existing work's rung, and the die below reads the whole pool's weight as
      // one sum — so it moves not only whether these two cross on colour but which of the other
      // grounds the same die lands on, and with it the pivot's transform and the family §4.8 matches
      // a return against. A third photograph deciding a crossing between two others is charter
      // shelf 20's own sentence at the place where it decides one.
      //
      // And an equality between two bucket names is a GATE. A candidate whose weight is exactly
      // nothing holds a stretch of the die's running sum of exactly no width, so it is never rolled
      // while any rival reads anything: two works standing a hair apart on the ladder had this
      // ground REFUSED rather than ranked. That is the admission test `groundReadings` a few screens
      // above was already cured of, and his word of 2026-08-18 09:51 is the cure — a measurement
      // ranks which genre suits a pair and shapes the one that wins, and never admits.
      //
      // WHAT STANDS INSTEAD is the ladder's own CONTINUOUS coordinate, which the record already
      // carries as `palette.colourfulness`: half how much colour is present (the chroma at the
      // coloured end of the frame against a fixed perceptual anchor) and half how wide it is spread
      // (the normalised entropy of the work's own hue histogram). Both halves are read off one
      // picture's own pixels and both are 0 at grey and 1 at a frankly polychrome frame, so the
      // coordinate is in [0, 1] by construction and the closeness below is too. The rung itself
      // still travels on the candidate, where a person reads it — it names a palette world and
      // naming is what a name is for; it decides nothing here.
      var ra = (a.palette || {}).rung;
      var mine = (a.palette || {}).hues || [], theirs = (b.palette || {}).hues || [], hues = [];
      for (i = 0; i < mine.length; i++) if (theirs.indexOf(mine[i]) >= 0) hues.push(mine[i]);
      hues.sort();
      var wa = (a.palette || {}).colourfulness, wb = (b.palette || {}).colourfulness;
      var together = (typeof wa === "number" && typeof wb === "number")
        ? 1 - Math.abs(clamp01(wa) - clamp01(wb)) : 1;
      // WHERE EITHER WORK NAMES NO HUE THERE IS NOTHING TO NARROW, and the closeness stands alone.
      // Two grey frames share the grey end of the ladder whole, and the line this replaces wrote
      // them down to nothing because neither had a hue to overlap with the other's.
      var overlap = (mine.length && theirs.length) ? hues.length / mine.length : 1;
      var paletteShare = together * overlap;
```

`rb` is no longer read and is gone from the declaration.

### The argument, over the whole span

`together` is `1 - |wa - wb|` with both arguments clamped into `[0, 1]`, so it lies in `[0, 1]` for
any two numbers whatever, and it is 1 exactly when the two works stand at the same place in colour
space and 0 exactly when one is grey and the other frankly polychrome. It is monotone in the distance
between them: a pair standing closer always reads at least as high as a pair standing further apart.

`overlap` is a share of a count by a count, so it lies in `[0, 1]`, and it is 1 where one work's hues
are all carried by the other.

Their product lies in `[0, 1]` and is the fit the die reads, so nothing here can hand the die a
negative weight or one that swamps the pool. The candidate is nought only where the two works
genuinely share no colour world — one grey and one polychrome, or two hue lists that do not meet at
all — and never because of a bucket boundary.

Nothing refuses. A record carrying no `colourfulness` reads `together` at the neutral 1 and the named
hues rank the candidate alone, which is what this line did minus its gate — so a record built before
the field existed still composes, and composes the way it always did. A record carrying no hues at all
reads `overlap` at 1 and the colour-world closeness ranks it alone.

No value here could have existed before the two pictures were known: both readings are read off the
two records in front of the composer, and neither is looked up.

### What the applier must check

Any row pinning a composed score for a pair whose two works stand on different rungs legitimately
moves: that pair could not reach the shared palette region before and can now. No row on a pair whose
works carry no `palette` block may move, because `together` and `overlap` both read their neutral
there and the fit is 1 — which differs from today's 0, so a pair carrying hues but no palette block at
all is the one shape to re-read. `test_pass_composed.py`'s bare record ships an empty palette block
and is exactly that case.

`plan.pivot.value.rung` still carries a name and still reaches the plan. Nothing that reads it needs
changing.

The two blocks are independent. Applying 5b alone closes the composer's half — the test's first two
rows go green — and leaves the harmonic key moving with the wall. Applying 5a alone closes the key and
leaves the gate. Neither is harmful without the other.

## 6. A second field of exactly the same class, found while sweeping

`tlvphotos-u27/lab/build-elements-v1.py`:

```python
def count_by_detail(dossier, med, middle):
    busy = float(dossier["structure"]["busy"] or 0.0)
    return middle * busy / float(med["busy"])
```

The divisor is the collection's median busyness, read out of the grid-derivation file. It is the
fallback for a ring count where a work carries no device and no rotational order above two, and for a
tile count where the work's device is not tiles — both recorded on the set as `grain against the
collection`. Those counts become `sets[].count`, `sets[].realCount` and `sets[].measuredGrain` on the
wire.

The composer reads them everywhere: `workParts` and `castActors` cast the actors from them,
`meshingTravel` takes the two ends of its size travel from `measuredGrain`, and the `tooth` handle
reads `mergeFactor`. So a tile grid's piece count — the geometry of the crossing, not merely which
ground it stands on — moves when another photograph joins the collection.

Same class as the rung, wider reach, and the median is a plain statistic over the collection rather
than a quantile. It needs its own repair and it is not designed here; the reading that replaces it has
to come from the work's own busyness against something absolute, and the honest first question is
what `middle` and the median were standing in for. Raised so it is not lost.

---

# Part two — two of charter shelf 12's open decompositions

Shelf 12 names five axes a work disassembles along. Semantic is parked by his own word and stays
parked; the other four reach the composer. Two things inside them are open and neither needs
semantics.

## 7. `strata-scale`'s handover — shelf 12's spectral sentence, never composed

### What is broken

Shelf 12's spectral line: detail scales, the blurred mass of B grows first and detail grows into it.

The instrument realises that sentence exactly. `pass-inst-strata-scale.js` splits the dial's travel
between two strata:

```js
    function detailShareOf(handover) {
      var pin = feelHandoverOf(clamp01(typeof handover === "number" ? handover : FEEL_H_U0));
      return DETAIL_SHARE + (pin - 0.5) * 2 * HANDOVER_REACH;
    }
```

and reads the split into the two strata's travel:

```js
        detailU: [clamp01(dA / share) * TRAVEL, clamp01(dB / share) * TRAVEL],
        massU: [clamp01((dA - share) / (1 - share)) * TRAVEL,
                clamp01((dB - share) / (1 - share)) * TRAVEL],
```

The arriving work's masses come home when its dial falls to `share`; its detail comes home only at the
end. **`share` is the size of the gap between the two** — how long B's blurred mass stands alone
before the detail grows into it. A larger `share` and the shelf's sentence reads strongly; a smaller
one and the two arrive almost together.

`handover` is the handle that sets it, over the whole range from 0.15 to 0.65, and the composer's
`HANDLE_SOURCE` row reads:

```js
    handover: ["module-rest", "the module's own single shared handle; nothing of either photograph "
                              + "decides how the dial's own travel is shared between the two strata, "
                              + ...
```

so the score ships a static value on every pair and the shelf's own sentence is the module's default
rather than a composed choice. Whichever two photographs are crossing, the mass stands alone for the
same fraction of the crossing.

### Why the row's argument does not survive the record

The row says nothing of either photograph decides it. The record carries `texture.reliefEdge` — the
scale a work parts at, how much of its own luminance its mass stratum carries — and **this very file
already reads it, in this very instrument's own `suits` row**:

```js
      "strata-scale": function (a, b) {
        var ea = readingOf((a.texture || {}).reliefEdge);
        var eb = readingOf((b.texture || {}).reliefEdge);
        var apart = Math.abs(ea - eb);
```

A reading that says how far a work parts into masses and detail is exactly a reading of how much of
the dial its detail needs. The composer was ranking the instrument on it and then declining to drive
the instrument's one shared handle from it.

The row is also the odd one out among its own kind. Every other `module-rest` row in the table is one
of two things: a judge channel, which rests because resting is what it is for, or one of the studio
instrument's operation switches, which the branch's own note cites as the precedent. The studio
switches are on-or-off selectors with no measurement that could answer them. `handover` is a
continuous share, and the record carries a share that says exactly what it needs — so the precedent
does not reach it.

### The block

**7a.** In `HANDLE_SOURCE`, under the comment opening `---- the parting-by-scale instrument ----`,
replace the `handover` row and the paragraph above it with:

```js
    // THE MODULE'S OWN SINGLE SHARED HANDLE (strata-scale.js:450-506) — one number for the whole
    // pair, because the split between the two strata is a property of the arrival itself and not a
    // travelling value. Charter shelf 12's spectral sentence is what it sets: the blurred mass of
    // the ARRIVING work grows first and its detail grows into it, and this handle is how long the
    // mass stands alone before the detail follows. It stood at the module's own rest with the note
    // that nothing of either photograph decides it; the record says otherwise, and this file was
    // already reading the field — the instrument's own `suits` row ranks the pair on
    // `texture.reliefEdge`, the scale a work parts at.
    handover: ["measured", "the ARRIVING work's own parting scale, texture.reliefEdge — how much of "
                           + "its own luminance its mass stratum carries — read as the share of the "
                           + "dial its detail needs, which is one minus that reading"],
```

**7b.** In the fill branch, find:

```js
          wanted.massCentreXB = flt(r4(clamp01(mt.reliefCentreMassX)));
          wanted.detailCentreXB = flt(r4(clamp01(mt.reliefCentreDetailX)));
```

and insert after them:

```js
          // HOW LONG THE ARRIVING WORK'S BLURRED MASS STANDS ALONE BEFORE ITS DETAIL GROWS INTO IT
          // — charter shelf 12's spectral sentence, composed rather than left at the module's rest.
          // The ARRIVING work's own parting scale is what answers, because it is that work's detail
          // that has to grow in: a work whose luminance lives mostly in its masses has little detail
          // to bring, so the two arrive nearly together, and a work whose luminance lives mostly in
          // its detail needs room for it. `reliefEdge` is how much the MASS stratum carries, so the
          // share the DETAIL needs is one minus it.
          //
          // NOTHING INVENTS A SCALE HERE. `readingOf`'s own clamp puts `reliefEdge` in [0, 1] and
          // the handle is published over [0, 1], so the reading is placed on the handle in the unit
          // it is already in — the same road `parquetPeriod`, `voidShareA`/`voidShareB` and
          // `seamA`/`seamB` already take. The map is monotone and covers the handle's whole span: a
          // work parting entirely into masses lands at one end and one parting entirely into detail
          // at the other.
          //
          // WHERE THE ARRIVING WORK CARRIES NO READING the handle is not driven at all and the
          // module's own rest stands, which is the honest answer and the one every other branch in
          // this file gives. Writing the reading's own zero would send the crossing to one end of
          // the span on the strength of a measurement nobody took.
          if (mt.reliefEdge > 0) {
            wanted.handover = flt(r4(clamp01(1 - mt.reliefEdge)));
          }
```

Also strike the paragraph at the foot of the branch opening `` `handover` IS NOT DRIVEN HERE, and
that is a fact about the module rather than a gap ``, which the block contradicts.

### The argument

`reliefEdge` is a share, clamped into `[0, 1]` by `readingOf` on every road that reads it and
defaulted to nought by `measuredParts` where the record says nothing. `1 - reliefEdge` is therefore in
`[0, 1]`, which is the handle's own published span, and `clamp01` states that rather than trusting it.
The handle is driven only where a reading exists, so the untouched case is the module's own rest
rather than an end of the span.

The value is a reading of the arriving photograph and of nothing else. Whether the photographs on any
particular wall spread across the span is a fact about that wall and decides nothing here; what the
block claims is that every value the handle can take is reachable from some reading, and that follows
from the map being the identity on `[0, 1]` after one reflection.

### What the applier must check

Every composed score carrying a `strata-scale` cue changes: `handover` moves from a static with no
note to a static with a provenance note naming what it read. Any golden pinned to such a score
legitimately moves. `test_pass_composed.py`'s geometry sweep asks that every handle the composer
drives names the measurement it reads in the score's own note, and that the ones which do not say
why they do not; `handover` moves from the second list to the first, so that row must be read.

`tests/test_pass_strata-scale.py`, if it pins the handle's value or its absence, moves with it.

## 8. The complement law — what it would take, and why no block is offered

### Where it stands

Charter shelf 12 states it inside the semantic bracket: every extracted object is stored with its
complement so the full frame is reconstructable at any moment. `PASS-API-V1.md` §4.6 lifts it to
every provider:

> **The complement law, carried from shelf 12.** Every set stores its complement, so the whole frame
> is reconstructable at any instant. The charter states it for the semantic axis; it binds every
> provider here, because a passage that drops the parts it did not name leaves holes, and the eye
> reads a hole as damage. `coverage` records the fraction of the frame the named elements hold, and
> `complement` carries the remainder as one element of kind `region`.

and gives it a conformance row:

> 32. an ElementSet plus its complement reconstructs the source frame within the seam threshold

**Three facts about where that stands today.**

Row 32 is unwritten. The word `complement` does not appear anywhere in `tests/` or `scripts/`, and its
only occurrence inside `engine/` is an unrelated arithmetic sense in the composer's prose — a distance
described as the complement of a closeness.

§4.6 says so itself, in its own opening sentence: no engine code answers to that section.

And the engine could not check it as things stand even if a row were written. The ElementSet §4.6
describes carries `complement` and `coverage`; the trimmed record the engine actually receives keeps
eight fields per set — kind, index, count, realCount, measuredGrain, mergeFactor, fig, provider — and
neither of those two is among them. The law is stated in two documents and expressible in none of the
data the engine holds.

The offline half is computed for one provider only, on a grid, and is itself unchecked — the lab's own
arsenal-gaps note of 2026-08-12 records that no check reads that file and that the complement has no
law over it.

### The half that IS enforced

The same shelf read at the level of one drawn frame is §7's coverage law, and that one holds. Only the
lowest cue of a stack may leave the frame open, `placeTheStack` refuses a stack that puts two whole
cues on top of one another, and the composer answers a refusal by re-casting the ground rather than
retiring a voice. The contract states the identity in as many words: the complement of a cue's matter
is the region the cue beneath it fills.

So what is missing is the law over a work's own decomposition, not the law over a drawn frame.

### What it would take, on each side

**The record builder** keeps one number per set. `coverage` — the share of the frame the named
elements hold — is already derivable where the set was cut and is already computed for the semantic
provider. Adding it to the eight fields the builder keeps is the whole wire cost: one number per set,
and the record grows by nothing that scales with the collection.

**The engine** gains conformance row 32 as a written row. With `coverage` on the wire the bookkeeping
half is checkable without a renderer — the named elements' coverage and the complement's account for
the whole frame, within the seam threshold, for every set of every record the settings record ships —
and that is the half that catches a builder writing a decomposition that drops matter. The pixel half
stays where §4.6 puts it, offline, because reconstructing a frame needs the frame.

**The composer gains nothing, and that is the answer rather than an omission.** Two reasons, and both
are standing law rather than preference. A coverage reading may not gate a cast: a measurement ranks
and never refuses, and a cast that declined a set for its coverage would be a branch ending in a
thinner crossing for a bookkeeping fault the visitor did not cause. And the drawn-frame form of the
law is already enforced where it belongs. A complement check inside the composer would be a new gate,
which is exactly what these repairs are forbidden to add.

### Why no block

A block here would be one line in a tree I cannot verify against, plus a test row that must sit red
until another tree ships a field. A row nobody can turn green is noise on every run, and it would sit
beside rows that are red because something is wrong. The row itself is small once the field ships —
for every set of every record, the named elements' coverage plus the complement's accounts for the
frame within the seam threshold, and a set that names no complement reds — and it should be written
in the same change that puts `coverage` on the wire, by whoever owns that change.

What this section is for is that the gap should stop being invisible. It is stated in the charter, in
§4.6, in §7 and in a conformance row, and the only place it is enforced is the one place that was
never in doubt.

---

## The rows

`tests/test_pass_palette.py`. Three rows, all red today.

Row one is the law, behaviourally: two records are held fixed, the rung name is walked through all
twenty-five ways the ladder could label them, and every die is asked. A crossing between two pictures
may not move when a field only the rest of the collection decides is moved. It reds today on a witness
where the two labellings cross the same pair on two different shared measures with two unrelated
families.

Row two is the second half: a pair that shares its hues outright and stands at one place in colour
space must be able to cross on the shared palette region. The row names the die that reaches it under
one labelling and finds none under the other.

Row three watches the producer, because a definition that changes on one side and not the other is
worse than either. It is a source row — what is wrong in the producer is not what it returns for one
work but what it reads to decide, and a value already baked into a record carries no trace of the set
it was decided against. It skips cleanly where that tree is not on the machine.

Both engine-side rows were verified against a scratch copy of the composer with block 5b applied: both
go green, and row three stays red because the producer block belongs to another tree.
