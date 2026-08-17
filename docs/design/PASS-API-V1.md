# PASS API v1 — the transition contract

**Root.** His word 2026-08-13 23:03: a feature-preserving immersive edition of TLV Photos. The
existing product keeps the door, the walks 10 + 5 + 5, story, series, quiz, gift, zoom, sound,
share/history, every input method, resize/orientation/DPR, RTL, reduced motion, Save-Data,
analytics/A-B and the static layer. A crossing is a subordinate visual transaction A → B; it owns
none of those.

**Status, 2026-08-14 08:47.** Built and standing: the transaction of §2 with its watchdog, its
idempotence guard and its token check; the frame half of §1.2 and §7 — one canvas, one WebGL2
context with the drawing buffer unpreserved, the two source textures, the programme cache, the frame
loop, the clock handed down as transaction seconds, resize, the resolution ladder, the name-driven
uniform binding, the resource census and context loss and restoration; three instruments of §8 on
the host's frame, each with its manifest and every handle reachable from a score — the woven one,
`matter` at `a3416b7` on `pass-api-v1-ports` with 29 conformance rows green, and the meshing `gears`
at `6485972` on `pass-api-v1-gears` with 31 green; the score's road from a site's own `pass` record
onto a declared command; the driver graph of §5 — its sources, its ten operator kinds, named nodes
with references, and cycles refused with the ring named; the camera of §6 — the pose record, the
dolly in log space, one authority at every instant with the stage's flight held across an owned
window, the handoff measured at the window's own edge and the rest read off the pose; and the
interruption cadence of §2.5. Still written and unbuilt from the lock of 2026-08-13: the `pointer`
driver alone. The stack of more than one cue and the levels and tier-budget checks of §4.4 have
since landed in the renderer's file, and this sentence carried them as unbuilt until 2026-08-14
11:12.

**Added 2026-08-14 08:47 on his word of 08:39, and their state at 10:31.** Four sections were added:
§4.6 ElementSet with its one provider contract and its five providers, §4.7 ScenePlan and the
passage composer that emits it, §2.6 the return to the hang with its two exact geometries and its
chrome reveal, and §4.8 EdgeMemory with the hysteresis across a directed pair. The four stand at two
different states and the sentence that flattened them is corrected here.

§2.6 is built on this branch at `7ee2708`, with 21 conformance rows green and five red-on-bug
proofs. The fixed numbers are the seam threshold of 6 of 255 and the rest tolerance of 1e-6, and the
rest reads 0.000000000 from the arriving hang pose. Departure and arrival agree with the DOM well
inside the threshold; the pixel means themselves drift from run to run, so this block names the
threshold they are judged against instead of pinning one run's decimals. §11 carries the one
divergence between what §2.6 asks and what was built.

§4.6, §4.7 and §4.8 have offline builders and checks in the tlvphotos tree, and no engine code
answers to them. Their conformance rows in §9 are unwritten.

**Two measurements from 2026-08-14 worth carrying.** The immersive road's boot fell from 285 074 B
gzipped to 136 190 B once the score table and the plans moved onto a digest-pinned pack road, with
23 255 B gzipped fetched before the first crossing. And the woven instrument's band count stands at
a floor of 8 against this pair's measured 3, recorded as requested-against-applied across 1935 cues;
§11 carries that divergence with an owner.

This block read that no line of code answers to any of the four, which was true at 08:47 and is
false for §2.6 now. The superseded sentence is in `PASS-API-V1-HISTORY.md` with its date. Section 11
lists what is unbuilt with its owner.

**Amended 2026-08-14 09:52.** The first implementation built against §4.7 found three things the
contract left unsaid, and all three are now written into it: a plan cue may carry fields the score
cue lacks, the plan record carries an authored `intent` line and a derived `duration`, and the two
direction dialects are mapped onto each other. §4.7 also carries his word of 09:34 on how the making
grammar reads. The superseded text of each is in `PASS-API-V1-HISTORY.md`.

The failure this document has recorded before is a status line that claimed an implementation that
did not exist. The opposite error costs the same care: a status line that keeps calling a built
thing unbuilt is wrong in the other direction, and the correction above is that. This block states
the built half and the written half separately for both reasons.

Any line below that reads as a description of behaviour is a specification of behaviour to be built,
and the conformance rows of §9 are the evidence that will make each one true.

The superseded text of this block, with its date, is in `PASS-API-V1-HISTORY.md`. Every amendment
below carries the same pointer.

**Where it stands against what already exists.** The seam (`seam-v2`, `d20475c` and `f6f9d63`) built
the register of live settings, the frozen command, the generation counter, the score checker and the
diagnostic surface. Those stand. This document replaces the seam's single renderer entry point
`run(cmd, done)` with a transaction, and repairs three defects the review of 2026-08-13 23:16 proved
against the seam's own code (§10).

---

## 1. Two surfaces, and who may call them

### 1.1 ProductNavigationAdapter — the product's own hands

Only the product layer may call these. The renderer never holds a reference to this object.

| method | what it does | who calls it |
|---|---|---|
| `declare(a)` | opens a transaction: freezes settings, mints a generation, returns the command | the stepping road and every programmatic jump |
| `dock(cmd)` | makes the arriving work current — caption, counter, share, place marker, tone, image ladder, narrator | the host, exactly once per command |
| `glide(cmd)` | runs the walk's own scroll animation, the standing fallback | the host, when no renderer takes the command |
| `interrupt(reason)` | ends the transaction in flight from a product surface | zoom, quiz, gift, door, series, popstate, reset |
| `reframe(viewport)` | tells the transaction the frame changed size or orientation | the resize and orientation-change road |
| `curtain(on)` | covers the walk with the renderer's canvas, and hides the covered walk from the accessibility tree and from its own observers | the host only |
| `mark(name, cmd, why)` | writes a lifecycle mark under the seam's own prefix | the host only |
| `hangGeometry(workId)` | measures the work's real place in the exhibition layout off the DOM at this instant — position, crop, fit, pixel ratio, orientation | the stepping road at `declare`, and the resize and orientation road (§2.6) |

`hangGeometry` reads the DOM, so it belongs to the product layer like every other row of this table.

**The one declared exception to this section's fence, added 2026-08-14 10:31.** This paragraph read
that the host receives the measurement as data on the offer and holds no reference to the adapter.
The implementation of §2.6 at `7ee2708` hands it through a read-only hook the product owns, which
the host calls at `prepare` and at `reframe`, for the bundle-byte reason §2.6 states.

This seat's reading of the fence: it stands for the adapter as a whole, and every other row of the
table keeps it whole. A single read-only measurement callback that returns a record and mutates
nothing is a declared exception, and it is declared here rather than left as a quiet fact of the
code. Conformance row 51 is what will prove it mutates nothing. That row is unwritten, so the
exception rests on this declaration alone until the row exists, and §11 carries it.

`dock` takes the command and reads its destination from `cmd.to`. It takes no element argument, so
a caller cannot dock a work the command never named. See §10.2.

**Every command names a destination.** One road in the door ceremony declares a jump with no
destination at all, so a landing keyed on the destination has nothing to read and the visitor can
end on one work wearing another's caption — the very class of defect §10.1 repairs. The lock closes
it: `declare` refuses a command whose destination is absent, and a road that moves the visitor to
the door names **the door** as the destination. The door is a destination like any other, with its
own landing behaviour, which is to clear the walk's chrome.

**`declare` is serialised.** A declare arriving while another is running supersedes it explicitly and
records that it did. Two declares inside one frame make the second a refusal with its reason, which
closes the race where a deferred re-landing from the series room and a live step both open.

**The curtain covers more than pixels.** While a renderer holds the frame, the covered walk is
marked inert and hidden from the accessibility tree, and the caption's own size and change watchers
are suspended. Otherwise a visitor reading by screen reader hears layout churn on a work they can no
longer see, while sighted testing shows nothing wrong. Focus stays where the visitor left it and is
restored to the arriving work at the landing.

### 1.2 PassHost — the transaction the renderer joins

The host owns one visible canvas, one WebGL2 context, the frame loop, the clock, resize, the A and B
source textures, the shader/buffer/texture/framebuffer caches, the capability and quality profile,
telemetry, cleanup and context restoration.

An instrument may not: create a canvas, a context or a frame loop; attach a DOM, input or resize
listener; load image or network data; read wall-clock; touch the DOM or history; destroy a shared
GPU object. §7 states the fence and the check that proves it.

---

## 2. The transaction

### 2.1 States

```
        declare()                prepare() accepts        start()
 idle ───────────► offered ──────────────────► armed ─────────────► running
                      │                          │                     │
                      │ prepare() declines       │ cancel/interrupt    │ settle()  ──► docked ──► disposed
                      ▼                          ▼                     │ fail()    ──► recovered ──► disposed
                   glide                      cancelled ──► glide      │ cancel()  ──► cadence ──► docked/returned
```

`offered` and `armed` sit BEFORE takeover: the product still owns every pixel, and a decline costs
the visitor nothing. `running` sits after takeover: the renderer owns the frame, and every exit from
here lands the visitor on a valid full door.

### 2.2 The methods

Host → instrument. Every call carries the token; an instrument that receives a token other than its
own returns without acting.

| method | when | what the instrument promises |
|---|---|---|
| `prepare(offer)` | before takeover | answers `{take:true}` or `{take:false, why}` within `prepareBudgetMs`; allocates nothing the host did not grant; touches no pixel |
| `start(t0)` | at takeover | the first frame after this call is a complete picture of A at its door |
| `frame(state)` | once per animation frame | draws; returns nothing; never calls back into the product |
| `resize(viewport)` | frame size, orientation or pixel ratio changed | keeps playing at the new size, holding its own progress |
| `cancel(reason)` | an interruption | resolves every handle to its nearest door through its own envelope, then calls `settle()`; the host force-ends at the deadline |
| `dispose()` | after a terminal | releases everything it was granted and nothing it was not |
| `contextLost()` | the context went away | drops its own handles and stops drawing |
| `contextRestored(resources)` | the context came back | rebuilds from the granted resources or calls `fail("no rebuild")` |

Instrument → host. Both are generation-checked and both are idempotent.

| call | meaning | what the host does |
|---|---|---|
| `settle(token)` | the transition reached its end door | docks the arriving work, drops the curtain, disposes |
| `fail(token, why)` | the renderer cannot continue | hides the renderer at once, lands a valid full door by the frozen fail policy, **and docks the work that door belongs to** |

**Both calls carry the token they were given.** An instrument may be reused across commands, so a
closure captured in one command can be called during the next with the live generation still
matching. The token makes the intent explicit: a call whose token is not the running one is recorded
as stale and changes nothing.

**Failure docks too.** A landing that only drew pixels would leave caption, counter, share, place
marker, tone and narrator speaking the departing work while the arriving one stands on screen.
Every exit from `running` therefore ends in exactly one dock, of whichever work the visitor is
actually left looking at.

### 2.3 The generation rule

`cmd.gen` counts up, one per declared transaction. Every host → instrument call carries `cmd.gen`.
Every instrument → host call is checked against the live generation before it acts: a call from an
old generation is recorded as a stale call and dropped. An old callback therefore cannot settle a
new command, and this is a conformance row rather than a convention.

### 2.4 Idempotence

`settle`, `fail` and `cancel` each act once. A second call of any of them, inside the same
generation, is recorded on the diagnostic surface and changes nothing. The product's dock happens
exactly once per command, keyed on `cmd.gen` and `cmd.to` together.

### 2.5 Exits, and the door the visitor lands on

| exit | before or after takeover | what the visitor sees |
|---|---|---|
| `prepare` declines | before | the walk's own glide, unchanged |
| `prepare` exceeds `prepareBudgetMs` | before | the walk's own glide; the slow instrument is recorded |
| a superseding input | before | the old command aborts, the new one declares |
| a superseding input | after | `cancel("superseded")`, the cadence plays within the interruption budget, then the new command declares |
| `interrupt(reason)` | after | `cancel(reason)`, cadence, then the frozen land policy |
| `fail(why)` | after | the curtain drops within one frame and the frozen fail policy lands a full door |
| the watchdog fires | after | `fail("no settle")`, same landing |
| context lost | after | `contextLost()`, the curtain drops, the fail policy lands a full door |

**The fail policy is frozen on the command** as `failLand: "arrive" | "return"`, default `arrive`.
`arrive` lands the full canonical B; `return` lands the full canonical A. It is read from the frozen
snapshot, never from live configuration mid-transition, which is the same law the land policy
already obeys.

**The watchdog.** The host ends any running transaction that has not settled by
`duration + settleSlackMs`. An instrument that never calls back therefore cannot strand the visitor.

**The three times carry ranges, so a legal value reads differently from a hung one.**
`duration` sits in 0…14 000 ms, `prepareBudgetMs` in 0…400, `settleSlackMs` in 0…2 000. A score
naming `duration: 0` is a legal instant transition and the diagnostic surface shows it as such; a
transaction that outlives its watchdog is shown as a hang with the instrument named. The two never
look alike.

### 2.6 Return to the hang

Added 2026-08-14 08:47 on his word of 08:39, and built the same day at `7ee2708`. The Status block
carries the measurements and §11 carries the one divergence between what this section asks and what
was built. This line read that nothing in the section was built, which was true when it was written
and false from `7ee2708` onward.

The passage becomes fullscreen while it plays. The work it leaves and the work it lands on both have
a real place in the exhibition layout, and the beginning and the end of the passage must be pixel-
accurate against those two places. A visitor who sees the picture shift by a few pixels at either
end has watched the machinery.

**Each door carries two exact geometries.**

- `hangGeometry` — the work's real position, crop, fit, pixel ratio and orientation in the exhibition
  layout, measured off the DOM at that instant by `adapter.hangGeometry(workId)` of §1.1.
- `immersiveGeometry` — the fullscreen scene state the passage plays in.

The two are named on the command's `doors` as `{ from:{hangGeometry, immersiveGeometry},
to:{hangGeometry, immersiveGeometry} }`. The from-door is read at `prepare` and the to-door is read
at `prepare` and again at `reframe`.

**How the measurement reaches the host was amended 2026-08-14 10:31.** This paragraph read that both
geometries were frozen onto the declared command and handed to the host as data on the offer. What
was built at `7ee2708` hands the measurement through a read-only hook the product owns, which the
host calls at `prepare` and at `reframe`. The reason is measured: freezing the record onto every
declared command costs bundle bytes, and the walk's bundle stands at 67 985 B against a 68 000 B
fence, so 15 B remain. §11 carries the divergence with its owner and §1.1 states the exception to
its own fence. The superseded sentence is in `PASS-API-V1-HISTORY.md` with its date.

**The flow, in order.**

1. The work hangs in the gallery at its own hang geometry.
2. The chrome enters a waiting state.
3. An exact handoff from the DOM to the fullscreen renderer: the first frame the instrument draws
   lays A's immersive frame onto A's hang geometry. §2.2's promise that the first frame after
   `start(t0)` is a complete picture of A at its door is read this way, and A's door is A's hang
   geometry.
4. The passage plays, with its world and its camera.
5. B reconstructs fullscreen.
6. The camera moves B continuously into its exact hang geometry.
7. A pixel-identical handoff from the canvas back to the DOM.
8. The chrome reveal.

**This amends §6's rest law.** §6 read that the last pose equals the neutral pose within 1e-6. The
arriving pose is now the pose that lays B's immersive frame exactly onto B's hang geometry, and the
neutral pose is the special case where the hang geometry is the whole frame. The tolerance stays at
1e-6 and row 9 of §9 keeps its wording and its reach, read under the amended law. §6 carries the
amendment in place and the superseded sentence is in `PASS-API-V1-HISTORY.md` with its date.

**Why the host reads the geometry as data.** §1.1 states that only the product layer may call the
adapter and that the renderer holds no reference to it, while his word of 08:39 has the host read
`hangGeometry(workId)` at `prepare` and re-read it at `reframe`. Both readings cannot stand
together. The reversible one is taken: the adapter gains the method and the product calls it, and
the host receives the measurement on the offer at `prepare` and again on `reframe`. The host has the
geometry at both instants his word named, and §1.1's fence keeps its full force. Reversing this
costs one field on the offer; reversing the other reading would cost the fence, and a fence that
opened once has opened.

**The handoff carries no opacity transition and no generic fade.** The DOM element is revealed and
the canvas released within one frame. No flash, no blank frame and no z-index leak. This is the same
law the charter's ban on the alpha crossfade states for arrival, applied at the seam between the two
renderers.

**`chromeReveal` is its own scoreable product choreography.** It runs after the handoff and exactly
once per command. Its parts are named so a score can time them: the title and plaque, the counter,
share, the sound control, the series and control affordances, and the focus and accessibility
handoff. Naming the parts lets a score time the landing. An unnamed reveal appears all at once.

**Audio state survives the passage.** Sound running when the passage began keeps running through it
and after it. The chrome appears after arrival and handoff, and at no earlier instant.

**A resize or an orientation change during a passage** recalculates the destination hang geometry
through `adapter.hangGeometry(cmd.to)`, hands it to the running transaction on `reframe(viewport)`,
and reframes the camera toward the new destination without a jump. §10.3's repair already routes the
orientation road to `reframe`, and this is the arriving half of it.

Conformance rows 38 through 44 carry this section.

---

## 3. `visualLayer=off` and the untouched walk

With the setting off, the host never prepares, never fetches the renderer's file, never creates a
context, and never draws a curtain. Every road between two works runs the walk's own glide.

**The landing gate applies only where a renderer took the command.** The seam put every in-view
report through a gate that admits one report per work per generation, which changed the shipped
behaviour: on `fe52eac` the watcher ran its whole body on every intersecting report, so a repeat
report after a rebuilt threshold or a language switch refilled the caption and its told line. With
the setting off, the gate stands aside and the watcher's road runs exactly as it does on the shipped
engine. The gate's claim of one landing per work per command binds the takeover road, which is where
two landings could actually happen.

The conformance row is an equivalence run all the same, because a claim of this shape is worth
measuring: the same scripted walk on `fe52eac` and on this branch with the setting off, comparing the
observable product state after each move and the full list of counting events. A difference is a red
that names the field it appeared in.

The same holds for reduced motion, Save-Data, a device with no WebGL2, a fetch that fails and a
renderer that throws on registration. Each of the six refusals is recorded with its reason.

---

## 4. The data objects

Pixels, knowledge about one work, knowledge about a pair, the elements a work breaks into, the plan
a passage plays and the site's own memory of an edge all stay apart.

**The pipeline, end to end.** A WorkDossier and a PairDossier feed a decomposition, which returns an
ElementSet per work (§4.6). The passage composer reads both ElementSets and emits a ScenePlan
(§4.7). The ScenePlan serialises into the score of §4.4, whose cues overlap freely and which the
PassHost plays. The passage ends by returning the arriving work to its exact place in the hang
(§2.6). The site's own walk keeps an EdgeMemory (§4.8) and hands the composer a `returnOf` record
when the visitor crosses an edge that has been crossed before.

The composer is the layer his word of 2026-08-14 08:39 named as missing. Before it, a pair went from
its dossier straight to a score, so nothing decided which parts of which work became actors, and the
answer defaulted to both works entire.

**Amended 2026-08-14 08:47.** The heading read "The four data objects" and the opening sentence
named three kinds. The superseded text is in `PASS-API-V1-HISTORY.md` with its date.

### 4.1 FrameSource — pixels and framing

```
{ workId, texture, width, height, orientation, uv:{u0,v0,u1,v1},
  fit:"cover"|"contain", coverCrop, standingFraming:{...}, decoded:true }
```

The host owns every FrameSource. It arms and decodes both works during `prepare`, so an instrument
that takes a command receives sources already decoded. The seam armed the arriving image inside the
landing itself; that is repaired here (§10.1).

### 4.2 WorkDossier — one work

Measurements, palette, structures, axes, motifs, optional offline masks and segments, safe crops.
Built at site-build time from `lab/data/recipes.json` and its siblings. Read-only in the browser.

### 4.3 PairDossier — one ordered pair

Shared invariants, seam and pivot candidates, the **directional** relation A→B distinct from B→A,
compatible doors, seed and provenance. The review of 2026-08-13 found no direction recorded anywhere
today although the charter's model requires an asymmetric relation; §11 carries it as a gap with an
owner.

**Amended 2026-08-14 08:47: where the direction lives.** §4.8 states it. A ScenePlan carries
`direction`, EdgeMemory keys an unordered edge with a direction beside it, and the two directed
plans of one pair hold the same family and the same pivot while everything else may differ. The
measured shape of today's gap: `lab/data/pair-shared.json` holds 7260 unordered pairs, each appearing
exactly once with no reverse row, so the pivot candidates on file read the same for both directions.

### 4.4 Score — the data a transition plays

A versioned record with an allow-list of fields, refused whole on any unknown field. The score names
no expression, no function and no executable string.

```
{ schema: 2, intent, pair:{a,b}, seed, duration, direction,
  interruption:{ withinMs, resolve:"nearest-door" },
  failLand:"arrive"|"return",
  camera:{ owner, rests, track:[...] },
  cues:[ ... ],
  quality:{ lean:{...}, standard:{...}, rich:{...} },
  provenance:{ source, measuredAt, by } }
```

Each cue:

```
{ id, instrument:{ id, api },
  voice:"letter"|"accompaniment"|"miracle",
  roles:["disassembly"|"mystery"|"assembly"|"world"|"surface"|"fragment"
        |"light-colour"|"breath"|"witness-camera"],
  levels:["WORLD"|"SURFACE"|"CELL"|"CELL CONTENT"|"TEXTURE"|"LIGHT-COLOUR", ...],
  window:[t0,t1], works:["a","b"], stack, cameraAuthority:"stage"|"own",
  doors:{ in:{handle,value,measured}, out:{handle,value,measured} },
  nodes:{ <name>: <driver node> },
  tracks:{ <handle>: <driver node or node reference> },
  resources:{ textures, textureSlots, framebuffers, pingPong, programs, passes,
              bytesEstimate, variant } }
```

**Accompaniment is said in two senses, and they are different questions, stated 2026-08-14 12:40.**
`voice:"accompaniment"` is what a cue counts as in the tier budget. Accompanying on a level is a
statement about one level in the plan's `levelOwnership` record. A cue voiced `letter` or `miracle`
in the budget may still accompany on a level it does not own, and that is the ordinary case rather
than an exception. Reading the second sense off the first is the conflation that refused every
composed plan as a score.

**`voice` and `roles` are two different questions and both are asked.** `voice` says what the cue
counts as in the budget — a structural gesture, an accompanying voice, or the one impossible event.
`roles` says what the cue does dramatically inside the pass. The budget check reads `voice`; the
composition check reads `roles`. Writing only one of them made the tier budgets uncheckable, which
the adversarial review of 2026-08-13 23:30 proved by writing a legal score that broke them.

**Amended 2026-08-14 08:47: `roles` carries nine values.** The enumeration read
`disassembly`, `mystery`, `assembly`, and a ScenePlan cue carries one or more of the nine of §4.7. A
cue naming `world` or `witness-camera` would have been refused whole against the old three, which
would have left the ScenePlan with no serialised form. The superseded line is in
`PASS-API-V1-HISTORY.md`. The rest of the allow-list is untouched: a score is still refused whole on
any unknown field, and no field was added to the cue record.

**`levels` is a list**, because a real instrument occupies more than one at once — the woven
instrument moves at SURFACE while each strip turns at CELL, which is exactly why it reads as alive.

**A cue's `levels` names the levels it OWNS, amended 2026-08-14 12:40.** A level a cue plays over
without owning stays out of that list. The levels law is then checkable in its own terms: two cues
that own one level in overlapping windows are a red, because the law is about two voices contending
on one level, and a cue that accompanies there is not contending.

The accompaniment relation lives in the plan's own `levelOwnership` record of §4.7 and reaches no
score. The rule read that a cue declares itself the accompaniment of another, and the first composed
plans exposed the conflation: the plan says per level who owns and who accompanies, while this rule
read a cue's whole `voice`, so every composed plan was refused as a score. Voicing a cue
`accompaniment` to get it through would corrupt the budget, since the cue in question is the
passage's one impossible event. The worked pair now emits its ground at SURFACE, its travel at CELL
and its arrival at TEXTURE, each naming only what it owns. The superseded sentence is in
`PASS-API-V1-HISTORY.md` with its date.

**The levels check runs at build time, and the host no longer carries it.** It read a field the
score's closed allow-list does not hold, so the host had nothing to judge.

The gate that judges a plan is `lab/sceneplan-build-check.py`, in the tlvphotos tree on the branch
`immersive-alpha-sceneplan`, and that is where the law is enforced. An earlier brief placed this
gate in the engine with a row count beside it. It has never lived in the engine, and the count came
with the same mistake, so neither is repeated here. Row 17 names the build-time home.

**The tier budget check.** From `voice`, `levels`, `window`, the score's `duration` and the score's
`camera` record: a quiet link carries one letter, at most one accompaniment, no miracle, 2–4 s; a
middle carries at most two letters, at most two accompaniments, at most one miracle, 5–8 s; a
culmination carries two or three letters, at most three accompaniments, exactly one miracle,
9–14 s; and held time stays under a third of the pass. Everything counts, and no cue is exempt.

**The camera counts as one accompaniment, amended 2026-08-14 10:31.** The check read the cues alone
and counted from their `voice` fields. The camera is carried in the score's own `camera` record
instead of as a cue, so it never reached the count, and a passage with two accompaniment cues and a
camera passed as carrying two. The charter's shelf 17 settles what the answer is: its list of
accompaniment voices opens with the camera, and the shelf's own words are that everything counts and
no never-counted class exists.

So the budget's counts read the cues together with the camera record. A score naming a camera track
carries one accompaniment before a single cue is counted. The composer's first real run against
§4.4 found this, and the superseded paragraph is in `PASS-API-V1-HISTORY.md` with its date.

### 4.4a Two schema versions live at once

The seam's checker demands `schema: 1` against a five-field allow-list. A score written at
`schema: 2` fails it outright, so shipping version 2 while the version-1 checker stands would refuse
every new score. The lock states the road:

- the checker accepts both versions and says which one it read;
- a version-1 score is read forward — its five fields map onto the version-2 envelope, its `params`
  become the default cue's tracks, and the reader records that it did so;
- a version-2 score is refused whole on any unknown field, exactly as version 1 is;
- a stored or shared address carrying a version-1 score therefore keeps working, which matters
  because such an address can already exist in a visitor's session store;
- a conformance row feeds one score of each version through the checker and proves both land.

### 4.4b Every handle a score can drive, a score does drive

The reference instrument keeps two handles that run on their own eased clock and answer to no
track — the strip-count breath and the press response. Under a scored run they keep moving on wall
time, so the same seed gives a different picture. A port therefore exposes every handle to the
score, and the conformance row for determinism is the proof: two runs of one seeded score, compared
frame by frame, must match to the pixel. A handle that keeps its own clock makes that row red, and
the row names the handle.

### 4.4c One template per instrument, one row per ordered pair

**RETIRED 2026-08-17 by his word of 19:21, and §4.4d with it.** Both sections answer one question —
where does the score for THIS pair come from — and both answer it with a table keyed by the pair.
That table is quadratic in the collection, and the collection grows to thousands of works, so
nothing on the product path may carry it. §4.4g below is the road that replaced them. The two
sections stand unedited underneath because a shipped preview was built on them and a stored address
can still name one of their scores; nothing in the walk reads either road any more, and the two
suites that guarded them — `tests/test_pass_reader.py` whole and the PASS-TABLE rows of
`tests/test_pass_weave.py` — retired in the same commit that deleted the code. `tests/test_pass_composed.py`
is what proves the road in their place.


A score per pair covers nothing on a walk that deals its works afresh each visit. The walk orders
its ten works by its own arc, so a pair scored ahead of time essentially never comes up; and a
collection of 121 works holds about fourteen thousand ordered pairs, which one whole score each
would make some fifty megabytes of settings file. The preview of 2026-08-14 showed exactly this: a
renderer registered, a score on file, and not one crossing played.

So a site may carry, beside `pass.scores`:

- `pass.scoreTemplates[<instrument>]` — one score with its per-pair numbers left empty and its
  slots named. Everything that does not depend on which two works are in hand lives here: the cue,
  its roles and levels and window, the doors, the camera, the quality variants, the interruption
  and the whole driver graph. Each slot names the cue and the static node its number fills, and may
  name a score-level field carrying the same number.
- `pass.scoreTables[<instrument>]` — one row per ordered pair, keyed the way `pass.scores` is,
  holding only that pair's measured numbers, plus the pair's own readiness.

At the moment a transition is declared, the product fills the template's named slots from the row
and hands the resulting score to the host. Filling named slots is a data operation: nothing is
measured in the browser, so §4.5's law that measurement and casting happen at build time keeps its
full force. A pair with no row hands back no score at all and the walk's own glide runs, which is
what a pair with no score has always meant. A row is refused WHOLE, with its reason, when it names
a slot the template lacks, when a field of it is no number, or when its readiness stands under the
table's own floor — the same floor the build-time walk applies, carried in the table so the refusal
needs no measurement either.

The conformance rows: a pair with a row produces a score the host accepts; a pair without one
produces none; a bad row is refused and recorded; and the filled score is identical, field for
field, to the score the per-pair builder wrote for the one pair that has both.

### 4.4d The delivery pack, and the reader that plays it

**RETIRED 2026-08-17 with §4.4c; see §4.4g.** `pass-reader.js` is deleted, no bake serves it, and no
site step stages a pack. What follows is the record of the road as it stood.

§4.4c's inline road holds while a site scores by hand. It stops holding the moment a composer scores
every pair: the composed pack of 2026-08-15 carries 7708 serialised scores, and a settings file
parsed at boot by every visitor cannot carry them. It also takes ONE TEMPLATE PER INSTRUMENT, and a
composed pack does not have that shape — it factors by PASSAGE SHAPE, twenty-five of them, and each
pair's row names its own. So a site ships the scores as a pack of static files and its settings
record carries the pack's addresses alone, under `pass.packs`, one entry per pack:

- `base` — the address every file of the pack stands under, carrying the pack's version and the
  first sixteen characters of its digest, so a stale file has no fresh address to answer at;
- `digest` — `sha256:` and the pack's own digest, which is the SHA-256 of its `manifest.json`;
- `manifest`, `head`, `templates`, `authored` and `rows` — the file names, `rows` carrying
  `{departing}` where the departing work's id goes.

A pack's `head.json` names its passage shapes; `templates.json` carries one score per shape with its
per-pair leaves left open and each open leaf addressed by the path that reaches it; a shard,
`rows/<departing work>.json`, carries every row that DEPARTS that work, each row opening with its own
shape's index into the head's list; and `authored.json` carries whole scores that stand as authored,
keyed by the ordered pair.

**The reader travels as its own file.** The walk's own bundle carries the door — the address, the one
synchronous question a declare puts to it, and the landing that warms — and the reading itself lives
in `pass-reader.js`, fetched once, only on a walk whose settings record actually names a pack and
whose layer is on. This is the division §12 states for the picture, applied to the same fence for the
same reason: the reader weighs 3 201 B gzipped and the bundle had 15 B of headroom.

**Warming is at the LANDING, and nothing ever waits on the wire.** `passScoreFor` answers
synchronously inside `declare`, and a crossing is declared the instant the visitor moves, so a fetch
begun there could never arrive in time. The shard holding a work's outgoing crossings is therefore
asked for when the walk LANDS on that work. A crossing whose shard has arrived plays; one whose shard
has not glides, with the reason on the diagnostic surface. Each work is asked for once, and a file
refused once stays refused for the visit — the same law §7 states for an instrument file.

**Every fetched file is weighed before it is read.** The settings record's digest weighs the pack's
manifest, and the manifest weighs every other file in the pack: one chain, rooted in the record the
bake wrote. A file whose bytes weigh to anything else is refused with both digests named, unread.

**A pack whose head names no shapes is not filled here**, and says so: its rows are of another form,
and only its authored scores are read.

The conformance rows are `tests/test_pass_reader.py`: a crossing takes its score from the pack; the
row's own shape picks its template while a second row of the same shard picks the other; the filled
score is the pack's own score to the last leaf; only the works the walk landed on are ever asked for;
a landing during the pack's own open is held rather than dropped; a missing shard glides with the
server's answer recorded; a tampered shard is refused with both digests; a score over the fence is
refused with the size it was measured at; and a pack-served score draws a frame byte-identical to the
same score served inline. Four of them carry a red-on-bug proof that serves a crippled copy of the
reader, or of the walk's own bundle, and passes when the answer moves.

### 4.4e The client's limits, published as a capability

A limit is part of the CAPABILITY: raising one is a rebuild, never a setting. A site that composes
scores has to know what the client will accept, because a score past the fence is refused before any
instrument sees it and the composer that wrote it never hears. So the bake reads the limits out of
the served client and writes them into the settings record under `pass.capabilities`:

- `scoreBytes` — the whole weight a score may have, measured as the length of the score written out
  as JSON, which is the very measure the client applies.

The number is READ rather than restated, so the published number and the applied number are one
number. `scoreBytes` stands at **12 288 B as an observed baseline with its evidence**: the composed
pack of 2026-08-15 carries 7708 filled scores whose median weighs 7029 B and whose longest weighs
10 851 B, and the 8192 B that stood before refused 1783 of them — 23.1 percent — unread.

### 4.4f Family bounds, and the roll at fill time

A pair flipped twice inside one visit plays one score, byte for byte, because a row carries measured
numbers and the fill writes them exactly. The charter asks for the opposite: the same passage family
each time, with small shifts pass by pass — variation, never repetition and never total novelty. So a
row MAY carry a FAMILY-BOUNDS record, and the fill rolls the handles that record names.

**Where the bounds live: on the ROW, beside its measured numbers.** They belong to the pair, because
what a handle may do is what that pair's own measurement supports, and no two pairs support the same
spans. The template holds no bounds; no new file and no addressing scheme arrive for them, and the
pack's own digest moves with any rebuild, as it always has. A row grew, and a row is the one
place per-pair numbers have always lived (§4.4c).

**The record.**

```
{ spans: { <slot>: [low, high], ... }, seed: true|false }
```

- `spans` names, per SLOT the row already fills, the closed span the fill may roll that slot's value
  inside. A slot is exactly one handle a cue drives — the inline road names it by the slot's own name
  (§4.4c), the pack road by the slot's ordinal in its shape's `slots` list (§4.4d), written as a
  string key. A slot the record does not name fills exactly as it fills today.
- `seed: true` re-rolls the score's own `seed` field each pass. A seed has no meaningful span — it is
  re-rolled or it is not — so it is a yes-or-no rather than a pair of numbers. A cue's own seed
  HANDLE, where one is a slot, is bounded like any other handle, and its whole range as its span is
  what re-rolling means for it.
- Both fields are optional and the record is refused whole on any other field, exactly as a score is.

**The order of writing is stated, because two of these can reach one field.** The row's measured
numbers are written first, then the rolled values at the slots the record bounds, then the score's own
`seed` when `seed: true` asks for it. A slot may name a score-level field of its own (§4.4c), so a
slot named `seed` writes `score.seed` too — and where both roads reach that field, the re-roll is last
and stands. The conformance row reads exactly that case, so the precedence is a fact rather than an
accident of the code.

**The roll is per PASS, and its seed is stated.** The fill derives one seed for the crossing being
declared from three things — the visit's own seed, the pass index (the generation `declare` mints),
and the pair's key — and each bounded slot's value is drawn from that seed and the slot's own name.
So the same pair flipped twice in one visit fills two kin scores whose bounded handles differ, and
the same crossing met again in a later visit differs again, while everything the record does not
bound stays identical: the same family, the same cues, the same instruments, the same stack.

**The visit's seed is read once and is pinnable.** The register carries `familySeed`: zero, its
default, means this visit rolls its own seed, which is the public bar — every public run exists once.
Any other number pins it, and a run at a pinned seed reproduces its predecessor to the pixel, which
is the judging mode. `familySeed` resolves on the session, site and default rungs alone; a per-pair
score has no business setting the mode a whole visit is judged in. The seeded road of §4.4b keeps its
full force: a score whose row carries no bounds is unaffected, and a pinned visit makes a bounded one
just as reproducible.

**A bad bounds record refuses the ROW, whole.** A span that is no low-to-high pair of finite numbers,
a slot the shape or template does not carry, an unknown field, and a rolled value that lands outside
its own span all refuse the whole row with the reason on the diagnostic surface, and the crossing
takes the walk's own glide. Half a rolled score is the one outcome no road here produces — the same
law §4.4c states for a row and §4.4 for a score.

**What the diagnostic surface carries**: the visit's seed and whether it was pinned, and per rolled
crossing the pair, the pass index, the seed the roll ran on, the spans it read and the value it
applied to each bounded slot. The applied values are readable beside the spans they were drawn from,
so a picture that looks wrong can be read back to the number that made it.

**The conformance rows** stood in `tests/test_pass_reader.py` for the pack road (retired
2026-08-17 with the road; see §4.4g) and
`tests/test_pass_weave.py` for the inline one: a bounded pair flipped twice in one visit fills two
scores that differ in the bounded handles alone, each inside its span; a pinned visit fills the same
crossing byte-identically twice; a row with no bounds fills byte-identically to the fill that stood
before this section; a malformed span refuses the row and names it. Two carry a red-on-bug proof that
serves a crippled copy of the walk's own bundle — one with the roll removed, which reproduces the
defect this section repairs, and one whose roll answers outside the span it was given, which the
refusal must catch.

### 4.5 The private fence

`quiz.json` and `story_notes.json` in the site's content root are keyed by the same work-id strings
as the measurement files. A join written as "everything about work X" pulls quiz answers and story
fragments into renderer data. The fence is therefore an explicit allow-list of dossier fields plus a
deny-list check: the build refuses to emit a dossier carrying any key from the private set, and a
conformance row proves the refusal by planting a private key and watching the build red.

Visitor identity, remembered place and the counting wire stay out of renderer data by the same rule.

**Free text is fenced by where it is written, since a key check cannot read it.** `intent` and
`provenance` are prose, so a private sentence could travel inside them. Both are authored at build
time and never assembled from visitor state at run time; the build refuses a score whose free text
was not present in the authored source file, and the diagnostic surface shows free text only when
the diagnostics setting is on. A conformance row plants a story fragment into an authored intent
line and watches the build red.

### 4.6 ElementSet, and the one provider contract

Added 2026-08-14 08:47 on his word of 08:39. No engine code answers to this section; offline
builders and checks stand in the tlvphotos tree, and the measurement files it reads exist and are
named below.

A work enters a passage as a set of elements that become actors. The charter's shelf 12 is the
source: a work disassembles along five axes and its fragments become the actors of the crossing. A
whole photograph is the degenerate member of that set, and §4.7 states where the degenerate case is
refused.

```
{ schema, workId, provider, providerVersion, seed,
  elements:[ { id, kind, level, geometry, weight, motifRef?, maskRef? } ],
  complement, coverage, provenance:{ source, measuredAt, by } }
```

`kind` is one of `strip`, `wedge`, `ring`, `tile`, `panel`, `band` (a tonal zone), `scale` (a detail
scale), `field` (chromatic), `region` (semantic or author-drawn).

`level` is the structural level the element occupies, from the levels law of shelf 17 that §4.4
already checks: WORLD, SURFACE, CELL, CELL CONTENT, TEXTURE, LIGHT-COLOUR. An element declares the
one level it sits on; a cue that casts several elements declares the levels it occupies, and that
list is what row 17 reads.

`geometry` is the element's place in the work's own frame, in the units its measurements are written
in. `weight` is the share of the frame the element holds, which is how the composer casts a leading
actor apart from an accompanying one. `motifRef` points into the motif list of `lab/data/motifs.json`
where the element carries one; `maskRef` points at an offline mask where one exists.

**The complement law, carried from shelf 12.** Every set stores its complement, so the whole frame
is reconstructable at any instant. The charter states it for the semantic axis; it binds every
provider here, because a passage that drops the parts it did not name leaves holes, and the eye
reads a hole as damage. `coverage` records the fraction of the frame the named elements hold, and
`complement` carries the remainder as one element of kind `region`.

The law already has a working implementation to cite. `lab/data/objects-pass2.json` derives the
complement on a 32-cell grid and stores it as a region of its own beside the named ones, for all 121
works. A provider returning a set whose elements and complement fail to reconstruct the frame is a
red, and conformance row 32 measures the reconstruction against the source.

**One provider contract serves five providers.**

`decompose(workDossier, request) -> ElementSet | decline{why}`

| provider | what it reads | where its data lives |
|---|---|---|
| `structural` | strips, axes, horizon, symmetry, tiles, contrast regions | `lab/data/recipes.json`, all 121 works, and `lab/data/motifs.json` |
| `semantic` | named classes with per-region boxes and confidences | `lab/data/objects-pass2.json`, all 121 works |
| `hybrid` | both of the above at once | both files |
| `author` | hand-drawn masks and regions | no file today; see §11 |
| `fallback` | tonal zones plus detail scales | derived from each work's own measurements |

**`structural`** reads the measurements that already stand: mirror scores per axis, fold order,
rotational count and score, polar strength, droste factor, slice period, colour including the pushed
value, busyness and source region. Beside them `lab/data/motifs.json` carries, per work, the figure
and void shares, the radial centre and the seam position, measured 2026-08-13 against four stated
thresholds.

**`semantic`** reads `lab/data/objects-pass2.json`: five named classes, per-region boxes with
confidences, and the derived complement, extracted by `qwen3-vl:8b` under prompt version
`objects-pass2-v3` and measured 2026-08-12. `lab/data/material-subject.json` stands beside it with
the construction matter and the depicted substance per work — the two layers of the charter's shelf
1 — voted three times at temperature zero against a fixed vocabulary shuffled per work, with a label
kept only on two votes of three.

The measurements exist and the provider that reads them is unbuilt. Its owner is the site build,
which already writes every file above; §11 carries the row. The charter's PARKED list holds the
semantic *extraction* pipeline, and the extraction of 2026-08-12 answered that item, so the block
the earlier text of §11 recorded is lifted.

**`hybrid`** runs structural and semantic together. Where the two overlap, semantic wins, and the
merge records that it did: the resulting set names both the element it kept and the element it
displaced, so a reader of the diagnostic surface can see which axis drew each boundary.

**`author`** carries hand-drawn masks and regions where artistic direction asks for them. It is
declared and unbuilt, and no file backs it today. Its owner is the author's seat, which the charter
seats on Fable.

**`fallback` is the majority road on this collection, and it answers the same provider contract as
the other four.** It
returns tonal zones and detail scales, which apply to any pair by construction, so it serves every
work whatever the pair holds in common. Shelf 12 names exactly this pair — tonal and
spectral — as the lawful universal bridge for pairs sharing nothing.

The measured reason it ranks beside the structural provider:
`lab/data/pair-shared.json` holds all 7260 unordered pairs of the 121 works, and 4793 of them —
66.02 percent — carry `shared_measure: null`, meaning no measure of the seven-measure table holds on
both works at once. A reader who takes the structural road for the normal one has designed for a
third of the traffic. Conformance row 34 therefore asks the fallback provider for an ElementSet on
every ordered pair in the collection and reds on a single decline.

**Declining, and the order of the fall.** A provider that cannot serve a work returns
`decline{why}`, and the composer falls to the next provider in the request's own order. The order is
the request's own word, so a passage that asks for the semantic
read first and a passage that excludes it are both expressible. Every decline is recorded with its
reason on the diagnostic surface, the same way §3's six refusals are. Conformance row 33 plants a
declining provider and follows the fall.

### 4.7 ScenePlan — the passage composer's output

Added 2026-08-14 08:47 on his word of 08:39. No engine code answers to this section; the composer's
own builders and checks stand in the tlvphotos tree.

ScenePlan is data-only and versioned. It sits between the PairDossier and the score's cues: the
passage composer emits a ScenePlan, and the score of §4.4 is that plan's serialisation for the host.

```
{ schema, id, pair:{a,b}, direction:"a->b"|"b->a", seed, tier:"quiet"|"middle"|"culmination",
  intent, duration,
  returnOf?:{ family, seed, passIndex },
  pivot:{ kind, value, held:true },
  actors:[ { ref:"a"|"b", elementSet, elementIds:[...], role } ],
  middle:{ kind:"world"|"surface"|"none", world? },
  cues:[ ... ], camera:{ ... }, doors:{ from, to },
  quality:{ lean, standard, rich }, interruption, failLand, provenance }
```

**`intent` is the authored line the plan opens with, added 2026-08-14 09:52.** The charter requires
every crossing plan to carry one written line naming this adventure and the shelves it draws from,
and states that a plan whose intent line is empty or generic fails review by definition. The first
implementation found the field missing from the record.

The line is authored at build time, under §4.5's fence. §4.5 forbids free text assembled from
visitor state at run time and refuses a score whose free text was absent from the authored source
file, and `intent` obeys that rule word for word. The authored line carries into the score's own
`intent` field of §4.4 unchanged, so one sentence serves the plan, the score and the run bar.

What the line may say is bounded by his word of 2026-08-14 09:34. It may describe what happens on
screen and what the passage draws from the charter's shelves. A claim about how a work was actually
made belongs in it only where he has documented that himself, because the measurement files read the
finished picture and a measured period is an affordance the passage draws on. Conformance row 50
refuses an empty or generic line.

**`duration` is derived, and the record names the derivation.** The field is `duration`, in
milliseconds, on the plan and on the score alike; §2.5 gives the unit and the range. The first
composer wrote it as `durationMs` and is renaming, and the name is fixed here so no third form
appears. Its value is the end of the last cue window. The first implementation computes it that way,
and stating it here means a reader sees where the number comes from. The derived value is what
serialises into the score's `duration`, and it must land inside §2.5's range of 0 to 14 000 ms,
where §4.4's tier budget check reads it.

**`pivot` is the pair's shared invariant, held throughout.** The charter's own law stands behind it:
the pivot is the pair's invariant shared part, and everything outside the pivot travels. `held` is
written `true` and stays `true`; a plan that lets the pivot travel has no pivot.

The idea has prior art on disk, and the contract names it as the pivot's provenance.
`lab/data/pair-shared.json` carries, for each of the 7260 unordered pairs, the shared measure, that
measure's strength, the cut the measure implies and the transform the cut implies. The mapping on
file reads: regions to regions to `region_dissolve`; named objects to named boxes to
`object_by_object`; texture to grain to `grain_wipe`; banding to bands to `band_slide`; radial to
rings or spokes to `radial_unfold`; dominant object to figure and ground to `object_reveal`; grid to
tiles to `tile_crossfade`. That is a first version of the road from a pair's invariant to its
actors, and the `pivot` and `actors` fields here are its successor.

The one thing that file lacks is the direction. Its 7260 rows are unordered — each unordered pair
appears exactly once and no row's reverse is present — so A to B and B to A read from one row. That
is precisely the gap §11 has carried since the review of 2026-08-13, and §4.8 closes it.

**The camera's resting pose is resolved at run time, and no plan carries it.** `camera` on the plan
names the flight; the pose it rests on is the arriving work's hang pose, resolved when the passage
runs. No file carries a per-direction hang geometry, and none should: §2.6 measures the geometry off
the DOM at `prepare` and again at `reframe`, so a plan that carried the pose would be carrying a
copy that goes stale on the first resize, orientation change or layout shift. The first composer
wrote the neutral frame into its plans for want of this sentence.

**`middle` is the third constructed event.** It is a world or a surface built from both works'
elements and belonging to neither, which is the charter's enfilade: a room of its own with two
doors, the door out of A speaking A's language and the door into B speaking B's. `middle.kind` may
be `none`, and a quiet link is where that reading is usual.

**Cue roles are nine, and a cue may carry more than one:** `disassembly`, `mystery`, `assembly`,
`world`, `surface`, `fragment`, `light-colour`, `breath`, `witness-camera`. §4.4's enumeration was
amended on the same date to carry all nine.

**Cues may overlap freely.** The grammar is not reduced to fixed linear phase windows. A single cue
may cover the whole passage, as the woven instrument does today. Different scores may carry separate
departure, mystery and arrival mechanisms, or fold all three into one continuous gesture, and both
are legal shapes.

**No rule of this contract requires a sequence of roles or a minimum count of them.** His word of
2026-08-14 09:34 settles how the making grammar reads, and this sentence carries it into the API.
The charter's line about one work's mechanism coming apart while the other's assembles points a
direction for the eye and carries no factual claim about how any photograph was made. Taking apart,
the middle and arriving are available gestures. A passage carried by a single continuous move is a
complete answer, and a plan that names one role is as legal as a plan that names six.

Four registers are available where a pair rewards them, each optional and none owed: discovery,
provocation, feedback, apparition. They name what a passage may reach for; no check counts them and
no plan owes any of them. `docs/V2-STATUS.md` in the tlvphotos tree carries the correction
as it was given. The working consequences are written at `lab/PASSAGE-COMPOSER.md` §1a, commit
`f2cdb11`, which stands in the composer's own tree and has not reached the tlvphotos tree read
here.

The levels law keeps its full reach across that freedom, and the two rules answer different
questions. Overlap in time is free. Overlap on one structural level in overlapping windows is a red
under row 17 unless one cue declares itself the accompaniment of the other. Conformance row 37
proves both halves at once, so a later reading of "freely" cannot quietly retire row 17.

**A plan cue and a score cue are two records, amended 2026-08-14 09:52.** The text here fenced the
score cue and left the plan cue unfenced, and a reader concluded the two were one record, which the
first serialiser proved they are not. A plan cue may carry fields the score cue lacks, and every such
field resolves away at serialisation, so nothing of it reaches the host.

`cast` is the first of them. It holds the element ids that cue casts, drawn from the plan's own
`actors`. A later field may join it under the same rule: it lives in the plan, it resolves at
serialisation, and the score's allow-list stays closed against it.

**`levelOwnership` is the second, added 2026-08-14 12:40.** It records, per level, which cue owns
that level and which cues accompany on it. §4.4's levels rule reads ownership alone, so the
accompaniment relation has a home in the plan and reaches no score. The plan gate judges the law
against this record at build time.

**The plan-only fields, named as one set.** `cast`, `levelOwnership`, `measuredHandles` and
`returnOf` live in the plan and resolve away at serialisation by design. None of them reaches a
score and none of them travels.

`measuredHandles` is named here as a member of that set on the word of 2026-08-14 12:40. Its shape
is the plan gate's to define and this contract does not fix it; what this contract fixes is that it
stays in the plan. §11 carries the definition with an owner.

**How a ScenePlan cue maps onto §4.4's cue.** The serialised cue keeps every field §4.4 lists and
gains none. `id`, `instrument`, `voice`, `roles`, `levels`, `window`, `works`, `stack`,
`cameraAuthority`, `doors`, `nodes`, `tracks` and `resources` travel across unchanged. The actor
casting resolves at serialisation: the geometries of the elements a cue casts are written into that
cue's `nodes` and `tracks` as static nodes, exactly as §4.4c's table fills a template's named slots,
and the ScenePlan's `id` is written into the score's `provenance.source`. The score's allow-list
therefore stays closed and every existing checker keeps working. `returnOf` stays in the plan and
reaches no score, which is the fence §4.8 states, and `cast` resolves the same way.

**The delivery road ships serialised scores, added 2026-08-14 12:40.** The plan form is a
build-time artefact and never travels. Shipping the plan form would put a build-time record on the
wire, and §4.8's fence is where that costs most: three fields of the edge memory ever cross, and a
plan on the wire is exactly how that fence would leak, since `returnOf` is a plan field. Conformance
row 56 reds if any plan-only field reaches a shipped file.

**Direction is written in two dialects, and the mapping is stated.** The plan writes `a->b` and
`b->a`; the score of §4.4 writes `a-to-b` and `b-to-a`. Both stay. The score's form already ships
and a stored or shared address can carry it, which is the same reason §4.4a reads a version-1 score
forward. The serialiser maps `a->b` onto `a-to-b` and `b->a` onto `b-to-a`, and the mapping is
written here so a third form never appears.

**The declared tier and the measured one must agree.** §4.4's budget check infers the tier from the
score's duration and its voice counts, while a ScenePlan declares `tier` outright. A disagreement
between the two is a red, and conformance row 36 measures it. Neither value silently wins.

**The correction, made mechanical.** The defect his word of 2026-08-14 named is a passage where two
whole photographs become fullscreen strips: one instrument, both works entire, for the whole
crossing. The refusal that closes it reads on the plan's actors.

**A ScenePlan is refused when no actor names any element of either work — when every actor is a
whole frame.** A plan must name at least one actor drawn from A's ElementSet and at least one drawn
from B's. Conformance row 35 carries it, in his own naming of the row: the scene plan contains real
actors, never one accidental fullscreen cue.

The lawful whole-passage cue survives this untouched. A cue may still span the entire passage. The
refusal removes a plan that names no element at all. The woven instrument keeps its whole-passage
cue on the day its port names A's strips and B's strips as its actors.

**What the refusal binds, and what it leaves alone.** The scores shipping today are filled from the
template and the table of §4.4c and no ScenePlan stands behind them, so the refusal binds a composed
ScenePlan only. Until the composer lands, §4.4c keeps producing scores under its own rules and the
crossing standing on the live preview keeps playing. The alternative reading would refuse every
score on file today and stop the shipped crossing, which no word of 2026-08-14 asked for. This is
the reversible choice of the two, and the day the composer lands is the day the woven instrument's
port owes its actors; §11 carries that port with its owner.

**Where the composer runs is undecided.** §12 splits the bundle from the renderer's own file by what
a visit that never draws needs. The composer reads dossiers and emits data, and it is needed only on
a visit that draws, which argues for the renderer's file; its size is unmeasured, so the split stays
open here and §11 carries the question with its owner.

### 4.8 EdgeMemory, and the hysteresis across a directed pair

Added 2026-08-14 08:47 on his word of 08:39. No engine code answers to this section, and the walk
that would hold the record is unbuilt.

Hysteresis is mandatory. A to B and B to A are distinct directed ScenePlans, and `direction` on the
plan is what distinguishes them.

**EdgeMemory is TLV's own private record, held by the walk in the site's layer.** The engine never
sees it. The engine receives `returnOf` inside a ScenePlan and nothing else of it. That boundary is
the same one §4.5 draws for visitor identity, remembered place and the counting wire, and it is
drawn here for the same reason: an edge record is a fact about one visitor's session.

```
{ edgeKey: the unordered pair key, direction, family, pivot, seed,
  passCount, lastAt, cooldown, provenance:{ previousScenePlanId } }
```

`edgeKey` is unordered and `direction` sits beside it, so one edge holds both of its directed
crossings. `lab/data/pair-shared.json` keys the same way and carries no direction at all, which is
the gap this record closes.

**What crosses the boundary.** When the visitor returns B to A, the walk hands the composer
`returnOf:{ family, seed, passIndex }` naming the previous pass. Those three fields are the whole of
what crosses. `passCount`, `lastAt`, `cooldown` and `previousScenePlanId` stay in the site's layer,
and conformance row 49 plants an EdgeMemory field into a ScenePlan and reds on it.

**What holds across the return.** The crossing stays recognisably related to the one before it: the
same family and the same pivot. The cue order, the element selection, the camera route, the rhythm
and the phases may all differ. This is the charter's shelf 16 read at the scale of one edge — the
backward door is kin to the forward one.

**Two refusals, each with its own check.**

An automatic reversed video is refused. A backward plan that replays the forward pass frame for
frame carries no authorship, and conformance row 46 plays a pair forward, plays it back, and reds on
a time-reversed match.

An unrelated novelty is refused. A backward plan sharing neither the family nor the pivot of the
recorded pass has lost the kinship shelf 16 asks for, and conformance row 47 reds on it. Row 45
states the positive form: B to A after A to B keeps the family and the pivot of the recorded pass.

**Repetition and determinism.** Repeated crossings of one edge vary only declared handles and
deterministic history indices. An exact repeat stays reproducible for the same visit, the same seed
and the same history, which keeps §4.4b's seeded-repeat row honest across a return; conformance row
48 measures it.

**What stays a product jump.** Browser-history restoration and layout jumps stay product jumps and
fallbacks. An authored directed passage is invoked by a real adjacent walk command and by nothing
else, so a restored history entry lands the visitor without playing a crossing that was never
declared.

**Both directions keep doors that match to the pixel.** The two geometries of §2.6 are measured per
direction, and neither direction inherits the other's arriving geometry.

---

### 4.4g The passage request, and the one entry a passage comes through

Added 2026-08-17 (U27 stage 0) on his word of 19:21 and his architecture decision of 18:00. This is
the road §4.4c and §4.4d were retired for.

**Nothing pairwise is written down.** The score that plays on an edge is DERIVED, in the browser, at
the instant the walk casts the pair, from the two works' own records. A record describes ONE work —
its light, palette, texture, geometric structure, motifs and safe crops, plus its element sets'
counts and grains — so what the settings record carries is linear in the collection: 121 works weigh
33 000 B gzipped under `pass.works`, where the per-pair rows they replace weighed 1 862 611 B. The
collection's own constants travel beside them under `pass.composer`: the instrument manifests, the
cut-line floors, the discriminating thresholds, the score fence and the provenance sentence.

**The composer travels as its own file**, `pass-composer.js`, fetched once per visit at the walk's
first landing on a visit whose settings record actually carries the records and whose layer is on.
This is the division §12 states for the picture, applied for the same reason. Warming stays at the
LANDING and nothing ever waits on the wire: the passage is derived synchronously inside `declare`, so
a crossing declared before the composer has arrived glides, with the reason on the diagnostic
surface — exactly what a pair with no score has always meant.

**The one entry is `passageFor(request)`**, and the request is the whole of what a passage is asked
for:

| field | what it is | what a missing value means |
| --- | --- | --- |
| `workRecordA` | the departing work's own record | a refusal: there is no pair without it |
| `workRecordB` | the arriving work's record | a refusal, for the same reason |
| `direction` | `a-to-b` or `b-to-a`, the two distinct passages of one edge | reads as `a-to-b` |
| `seed` | the die, inside the span the meshing instrument publishes for its own `seed` handle | the walk rolled none; the passage runs on 0, reproducible |
| `routeRole` | entrance, quiet link, middle, culmination or return (charter shelf 15 maps these onto the harmonic functions) | the walk stated no function; read as a middle |
| `sessionMemory` | §4.8's return reference `{family, seed, passIndex}`, and nothing wider | nothing has played on this edge yet |
| `cameraState` | the pose the camera rests in as the passage starts; the flight departs from it | the walk stated no pose; the flight departs from the score's own rest |
| `buffer` | the canvas as it stands: width, height, dpr, orientation, quality tier | unstated; the instrument reads the one it is drawing on |

A name outside the five route roles, a session memory naming a field outside §4.8's three, and a die
outside the instrument's span are each a named refusal, so the vocabulary cannot drift and §4.8's
fence cannot leak. What comes back carries the score, the request as it was read, and `applied` —
what the instrument applied on the buffer it drew on, or the refusal it named — which the walk writes
onto the record at the landing, because it cannot be known before the frame is drawn.

**The edge is named in one order whichever way the visitor walks it** — the two ids sorted — and
`direction` says which way this passage runs, so A to B and B to A are two distinct passages of one
edge and the site's own edge record of §4.8 has a stable key to hang on.

**The die is the walk's own.** It is made of the visit's own seed (pinned by the `familySeed`
setting or rolled once), the pass index the declare has already minted, and the edge's key — the
same three §4.4f's family roll is made of, so there is one idea of a seed and no clock in either.
Charter shelf 16: a pinned seed reproduces a run exactly, which is the judging mode; the public walk
rolls a fresh one each time, which is the viewer mode.

**The composer holds no door.** The meshing instrument reads its own mask at both doors on the buffer
it is drawing on, holds its size whole within the reach its manifest publishes, and publishes what it
moved and why; the composer emits the artistic request and the bounds live in the manifest. The
prebaked door table this replaced was keyed by the pair's own camera pose — pair-scaled — and
answered for one 1000 x 1000 frame.

**The equality this road was landed on.** Every one of the 6 304 ordered pairs the shipped table
carries composes through this entry to the byte-identical score the prebaked pack shipped, and every
one of its 4 254 declines carries the same sentence character for character; 161 of the 6 304 differ
from the shipped bytes in the meshing travel's two door-instant sizes alone, which is the measured
cost of the 18:00 decision and nothing else. The conformance rows are `tests/test_pass_composed.py`.

## 5. Driver AST v1 — data only

**Sources.** `progress` (the transaction's own 0…1), `cueProgress`, `time` (transaction seconds,
handed down by the host), `velocity` (the hand's normalised speed), `pointer` (declared; one
normalised host signal arrives later), `capability`, `noise(seed, stream)`.

**Operators.** named curve, monotone spline, `map`, `add`, `multiply`, `mix`, `clamp`,
`hold`/`segment`, `ramp`/`slew`, and — added by the review of 2026-08-13 — **`oscillate`**
(`{rate, phase, shape:"sin"|"tri"|"cubed-sin"}`), because almost every instrument's breath is a
periodic function of unbounded time and every named curve in the codebase is a bounded monotone
shape.

**The graph is a graph.** A cue may declare `nodes` by name and a track may reference a node by
name. One node therefore feeds several channels, which is what the law "one envelope couples the
axes" requires: the balance that drives duty, travel amplitude and the geometric cap at once is one
node with three readers. Cycles are refused at validation.

No `eval`, no `new Function`, no string that is executed. A conformance row greps the built client
for both and reds on either.

**Built, 2026-08-14:** the sources `progress`, `cueProgress`, `time`, `velocity`, `capability` and
`noise(seed, stream)`; the operators named curve (the lab engine's own four, carried across
unchanged), monotone spline (Fritsch–Carlson, the whole-track course his word of 2026-08-11 named
after judging speed steps at segment joints), `map`, `add`, `multiply`, `mix`, `clamp`,
`hold`/`segment`, `ramp`/`slew` and `oscillate` with its three shapes; named nodes with references;
and cycles refused at validation with the ring written out. `oscillate` reads its rate in cycles a
second and its phase in radians, so an instrument's own voice — `sin(t · 0.021 · TAU + 1.1)` — is
carried into a score digit for digit rather than through a conversion nobody can check by eye.

**Declared and falling back to base:** `pointer`, and `capability` variants beyond the three named
tiers. Every fallback is recorded with its reason on the diagnostic surface.

**`ramp`/`slew` is the one node that remembers**, since a rate limit is a statement about how fast a
value may travel and nothing can say that from one instant alone. It carries its own value forward,
keyed per transaction, and a run with a pinned clock holds it perfectly still — which is what keeps
the seeded-repeat row honest.

---

## 6. The camera

One continuous voice with its own arc, resting exactly on B.

```
{ at, pan:{x,y}, logScale, pitch, yaw, roll, orbit, tilt, fov, owner:"stage"|"cue:<id>" }
```

Dolly travels in **log space** and is interpolated there; the existing lab engine interpolates raw
scale on both of its paths, which the charter's own law contradicts, so the lock states log space and
a check proves it. `logScale` is the NATURAL logarithm and no other base, because the applied factor
is exp of it: a base-2 logarithm written into that field flies the ratio asked for raised to 1/ln 2.

**Orbit and tilt, added 2026-08-17 (U27 stage 1).** The charter's shelf 2 names two cases of a
nonlinear camera being a straight line in another coordinate system, and until now the record carried
only one of them. `orbit` is the point of view's azimuth about the subject and `tilt` its elevation,
both in radians, both carried in their own coordinate. They are a different move from `yaw` and
`pitch` and the applied transform says which is which: orbit and tilt act before the pan, so they
turn the scene about the frame's own centre and the pan then carries the turned subject to its place
— the point of view travels around the work while the work holds its framing — where yaw, pitch and
roll act after the pan and let the scene swing across the frame. A turn is seen through a projection:
where a score names no `fov` the host applies its own, since without one an orbit is an affine squash
rather than a turn. Both axes need the perspective road, so §7's `lean` variant drops them and
records the fallback, as it does for pitch, yaw and the field of view. Both hangs are flat and
square-on, so both axes stand at zero at either end of a flight and the rest of §6 is unchanged.

**Each place is carried through the points that name it, added 2026-08-17.** A place used to be
carried only where EVERY point of the track named a number for it, so one axis could not be given
timing of its own without giving every other axis a point at the same second — and a flight of
several arcs could not be written down at all. Each place is now splined through its own points, so
one unbroken flight can rise and fall its dolly at the two edges while the tilt holds a plane at an
angle across a window of its own and the orbit sweeps once through the middle. A track that names
every place at every point reads exactly as it did, which is what every composed score does.

**A camera-led passage, added 2026-08-17.** `camera.lead` declares that the flight itself is the
transition: the camera's travel through the scene is what carries the visitor from one work to the
other, and the instruments underneath hold a quiet register. Two things follow. The anchor between
the two hangs loses its held middle — three points instead of four, the departing hang, the whole
frame at the halfway second and the arriving hang — so the pose travels the whole duration and never
stands still, a flight that stopped mid-passage being the passage stopping. And the camera spends the
WORLD voice of the levels law, so a score that declares `lead` and then gives a cue the world level
is refused before the command is taken, with the cue named. The two ends are the same two hangs
either way, so a led passage lands pixel-exactly like any other.

**One authority at a time.** The score names the owner per window. A cue that carries the camera by
its own device declares `cameraAuthority:"own"`, and the stage's flight holds still across that
window. Handoffs are continuous: at a handoff instant the two poses must agree within a stated
tolerance, and a conformance row measures the pose across the handoff frame by frame.

**Rest on B, amended 2026-08-14 08:47.** The last pose equals the pose that lays B's immersive frame
exactly onto B's hang geometry, within tolerance. The check reads the pose rather than the picture,
so it stays honest when the picture changes.

The neutral pose is the special case where B's hang geometry is the whole frame. §6 read that the
last pose equals the neutral pose, full stop; the superseded sentence is in `PASS-API-V1-HISTORY.md`
with its date. It was amended because the passage plays fullscreen while the arriving work has a
real place in the exhibition layout to return to, and a pose resting on the neutral frame would put
the visitor a few pixels off the hang at every landing. The tolerance stays 1e-6, row 9 of §9 keeps
its wording, and §2.6 states the geometry the arriving pose is measured against.

**Where a cue's own device carries the camera.** Some instruments move the point of view by their
own construction — a floor's pitch, a box turning, a depth of tilt. Such a cue declares
`cameraAuthority:"own"` and, on its window, reports its pose to the host each frame. The host holds
its own flight still across that window and applies the reported pose. The separation the charter
asks for is kept this way: the pose is one record, applied once, by the host; what the instrument
does to its surface inside the frame stays its own business and never doubles as a camera move.

**A cue that owns the camera and then fails** hands authority back to the host at the pose it last
reported, and the host resolves from there to the frozen fail policy's door. Authority never lapses
into nobody's hands.

**The log-space rule binds every path.** Where an instrument's own dial travels linearly in scale
today, its port converts at the boundary, and the check reads the pose across the whole pass rather
than only the stage-driven part.

**Doors are cross-checked against the manifest at validation.** A score may name an entry or exit
door only where the instrument's own manifest publishes a framing for it. A score naming a door the
manifest leaves blank is refused at build time, with the instrument and the door named.

---

## 7. GPU and resources

The host grants; the instrument declares and spends what it was granted.

An instrument's manifest declares textures, texture slots, framebuffers, ping-pong pairs, programs,
passes, per-frame samples and a **byte estimate**, per quality variant. At `prepare` the host
compares the declaration against the budget for the chosen variant and may grant it, grant a lower
variant, or decline. At runtime the host counts what was actually created against what was declared,
and a difference is visible on the diagnostic surface as a lie.

**Counting objects misses the size of them.** One texture holding a hundred layers counts the same
as one small texture. The host therefore measures bytes as well as objects: every allocation it
grants is sized from its dimensions, layer count and format, and the sum is compared against the
manifest's byte estimate. A declaration that understates its bytes is the same kind of red as a
declaration that understates its count.

**Layered textures and ping-pong pairs are declared as what they are**, since two instruments in the
lab need exactly those and cannot be described honestly by a plain object count.

One canvas and one context is law. Every extra temporary target, mask, data texture and pass is
declared, measured and visible. No single combined shader: the render graph is built from manifests.

**The uniform contract is name-driven.** The lab carrier's draw call names exactly the six uniforms
of one instrument, so nothing else can ride it. The host binds by name from the manifest: an
instrument declares its uniforms with their types and sources, and the host supplies them. Binding
by position or by a hardcoded list is refused at registration.

**Shader version.** An instrument may ship source already written at GLSL ES 3.00. The host's
translator stamps a version header only when none is present; two lab modules carry their own header
today and would receive a second one, which is a build-time red rather than a runtime surprise.

**`preserveDrawingBuffer` stays off.** Seven lab modules request it. A manifest that asks for it is
refused, and the port carries the redraw the flag was standing in for.

**The quality tier gains a consumer.** The setting is built and read by nothing. The host reads it
at `prepare`, picks the variant, and records the decision with its reason.

**Quality variants.** `lean`, `standard`, `rich` hold the same cues, windows and roles; they differ
in render scale, the list of secondary voices and the granularity of pieces. The degrade ladder
lightens the score first, then drops accompaniment voices to 30 frames a second while the leading
gesture keeps 60, then eases resolution toward 0.75 of device pixels, and stops at a floor below
which the plain fallback plays instead of a thin miracle.

**The frame state names the drawing buffer, added 2026-08-16.** The state handed to `frame` carries
the CSS frame as `viewport.w`/`viewport.h` and the drawing buffer as `viewport.bufferW`/
`viewport.bufferH` — the same two numbers the host binds as the `resolution` uniform source. The
buffer is the CSS frame times the device ratio times the live resolution step, so it is settled
after any plan is serialised and it moves while a pass plays. An instrument whose own law depends on
where a sample lands reads it there: the meshing instrument's doors are read on the buffer, because
a leak is one sample landing on a singular point and the sample positions come from the buffer.

**The frame state names both works' seating, added 2026-08-17 (U27 stage 1).** It carries `fitA` and
`fitB`, the instrument's own `fit` answered on the buffer above — the very numbers the draw binds as
the `fitA`/`fitB` uniform sources. An instrument cover-fits a work into the frame and then pulls in
by its own framing headroom, so its geometry is a function of that seating; the unfold and the adrift
both read the seating BACK out of the uniform inside their shaders, and neither could reach it in
script at all. Both therefore bounded their geometry by the worst seating a cover fit can hand and
could only over-hold, never hold exactly. Asked for here, on the same buffer, through the same
function the draw calls, so an instrument's script and its shader work from ONE seating rather than
from two guesses at it.

**The instrument reports what it applied, added 2026-08-17.** His architecture decision of that day
at 18:00 makes the instrument's own run-time reading on the actual buffer the truth of a passage: the
composer emits the artistic request and its bounds, and what was really drawn is known only inside
the frame. The frame state therefore carries `reportApplied(record)` beside `reportPose(pose)`. An
instrument calls it at a door instant with its own numbers, and calls it before it refuses, so the
applied state on the way to a refusal is carried too. A refusal itself keeps its own road —
`st.fail(st.token, why)` is unchanged and this channel replaces nothing.

The host stores the record as it arrives and reads nothing in it. Each voice's row of the diagnostic
surface publishes it as `applied`, beside the `handles` the host itself resolved: the run-time truth
and the plan's intention, readable against each other on one row. The row survives the landing, so a
walk that asks what happened once the host is idle again still finds it. The walk writes it onto the
passage record the request came from, which is where a reader of one edge looks.

The five instruments agree on one plain shape, kept in their own files rather than in the host:
`door` (`"in"` or `"out"`), `buffer` (the two numbers the reading was taken on), `reads` (the handle
the reading is about), `request` (the value handed in), `applied` (the value drawn), `moved` (how far
the two stand apart), `unit` (what `moved` is counted in — rungs, bands, cells, degrees), `held` (the
leak the request would have drawn, in the instrument's own words, or nothing) and `whyNo` (the
refusal, where no whole value stood within reach). The host would carry any other shape unchanged.

**The pack boundary, added 2026-08-14 13:26 and built at `b212ef3`.** The instruments live in
`engine/assets/pass-pack.js`; the host lives in `engine/assets/pass-layer.js` and loads the pack by
address, checking its declared version and a digest of the bytes that arrived, then registers what
it finds by manifest name.

**The host knows no instrument name.** Row 57 greps the built host for each of the three and reds on
any occurrence. Measured 2026-08-14: the built host carries zero occurrences of `weave`, `matter`
and `gears`, and the pack carries eight, seven and six.

*The host owns:* the state machine, the watchdog, the idempotence guard, the cadence, the frame
loop, the GPU and resource machinery, the driver evaluator, the camera, the census, the diagnostic
surface's renderer half, and the pack loader with its version and digest check.

*The pack owns:* the instruments — their shaders, their response curves and their manifests — and
nothing else.

**The version and the digest.** The version lives in one literal inside the pack, so one edit moves
it and no second copy can disagree. The digest is taken over the built, comment-stripped bytes, the
same bytes the byte fence measures, so the two read one artefact. The baking order is fixed: the
pack is baked first and the host second, because the host's copy of the digest is computed from the
pack that already exists. A pack whose digest or declared version disagrees with the address is
refused, and row 60 carries the refusal.

**The uniform sources are a closed set.** A uniform may be sourced from the two source textures,
their fits, the resolution, the transaction's seconds, a value the instrument answers, or a handle.
Anything else is refused at registration, which is the same law §7 already states for binding by
name rather than by position, carried across the pack boundary. Row 59 carries it.

**The coverage law, added 2026-08-14 12:40.** The host draws several cues in one frame. An
instrument writes opaque where its own matter stands and clear where its matter is absent. The frame
it hands back is its elements together with the space between them, and that space belongs to
whatever plays underneath.

This is the charter's twelfth shelf read at the level of one drawn frame. Every element is stored
with its complement so the whole frame is reconstructable; the complement of a cue's matter is the
region the cue beneath it fills.

No per-cue weight of presence. No alpha imposed by the host. The charter bans that mechanism in its
own words, and a stack leaning on it would be the crossfade under another name.

**The finding that forced it.** Every instrument wrote an opaque frame, so a visitor saw only the
cue nearest the eye. On the worked pair the band family is drawn under every frame from 1.17 seconds
onward and is seen at no instant, and three voices read as one. The law is the artistic finding of
2026-08-14 rather than a housekeeping rule.

**Where the alpha comes from.** The alpha each instrument writes rests on a quantity its own shader
already computes, so the law adds no new mathematics to any port. The woven instrument stays at a
constant 1, having no absence to write. `matter` and the meshing instrument each write one minus
their own mask, whose boundary is the material's own edge.

**The blend is straight source-over on the source alpha, and premultiplied alpha is refused with a
measured reason.** The first cue laid down meets blending disabled, and multiplying colour by alpha
would go black wherever alpha stands below 1. Colour channels stay untouched, which is what makes
the one-cue row of 54 hold by construction rather than by measurement.

**Both doors stay whole, and the reason differs per instrument.** The woven one's alpha is a
constant. `matter`'s mask is zero everywhere at its exit door. The meshing instrument's own door
placement puts all four corners inside the door condition. Row 53 measures the three together.

The per-instrument specification is `docs/design/COVERAGE.md` on the branch `pass-api-v1-coverage`,
committed at `aa495fb`, 460 lines, with every claim carrying the line it was read from. Verified
present at that commit on 2026-08-14 before being cited here. This section states the law and that
file carries the per-instrument detail. Conformance rows 52 to 55 and 61 carry it.

**Context loss.** `contextLost()` drops instrument handles and the curtain; `contextRestored()`
rebuilds from granted resources or fails. A census row proves that texture, program and framebuffer
counts return to their baseline after repeated runs.

---

## 8. Instrument manifest

```
{ id, api, arity:1|2, roles, params:{...}, handles:{...},
  neutrals:{...}, doors:{...}, framings:{...}, drivers:[...],
  camera:{ needs, authority }, passes:[...],
  coverage:{ writes:true|false, how },
  resources:{ lean:{...}, standard:{...}, rich:{...} },
  capabilities:[...], decline:[...], provenance:{ labPath, commit },
  readiness:"production-ready"|"needs-port"|"lab-only"|"failed-proof" }
```

The lab modules are source material. Their own canvas, context, frame loop and pointer code is not a
production port; a port is the instrument's mathematics carried onto the host's frame with a
manifest and a passing conformance run.

**`coverage` declares whether the instrument writes coverage, added 2026-08-14 12:40.** `writes` is
`true` where the instrument leaves the space between its elements clear, under §7's coverage law,
and `how` names the mechanism its port uses. The host reads this at `prepare` and records the
decision with its reason, the same way it records the quality variant.

**Where a cue declaring `writes:false` may stand, amended 2026-08-14 14:05.** In a stack of more
than one cue, the lowest cue may declare that it writes no coverage, and every cue above it declares
that it writes coverage. A one-cue score is exempt, since nothing stands beneath it. Row 61 reds on
an opaque cue standing above another.

This paragraph read that an instrument declaring `writes:false` may be drawn only as the cue nearest
the eye. That is the mirror of the rule that holds, and it would have refused the arrangement that
works while permitting the defect of 10:47. The woven instrument has no absence: its two ribbon sets
partition the frame and both branches of every mix are picture, so it writes a whole frame honestly
and declares `writes:false`. It is also the ground of the composed passage and sits at the bottom of
the stack, farthest from the eye. The superseded sentence is in `PASS-API-V1-HISTORY.md` with its
date.

---

## 9. Diagnostics and conformance

**The gated inspector shows** every parameter with its origin, requested and applied value; drivers
and their evaluated values; cues, roles, camera authority and pose; the quality and capability
decision; the texture, program and framebuffer census; generations, lifecycle, fallback reasons and
timing. It never shows story text, quiz answers, visitor identity or anything the counting wire
carries; it reads its own lists and nothing else.

**Conformance gates.** Each is a row that reds when its rule is removed.

1. dock happens exactly once per command, keyed on generation and destination
2. a stale callback settles nothing
3. a superseding input aborts the first command and the second declares cleanly
4. decline before takeover runs the legacy glide and changes no pixel
5. error after takeover hides the renderer within one frame and lands a full door
6. the watchdog ends a transaction that never settles
7. endpoint doors match their canonical files within the seam threshold
8. cue handoffs match frame to frame within the seam threshold
9. camera authority is single at every instant, and the pose rests on B
10. a seeded run repeats to the pixel
11. resize, orientation change and context loss keep the transaction alive or land it cleanly
12. reduced motion, Save-Data and `visualLayer=off` reproduce today's walk
13. no forbidden ownership: no canvas, context, frame loop or listener inside an instrument
14. no resource leak after repeated runs
15. the console stays clean
16. captures and goldens exist for every landed instrument
17. two cues that OWN one level in overlapping windows are a red, judged at build time by the plan
    gate rather than by the host, and read against the plan's `levelOwnership` record; a cue that
    accompanies on a level it does not own is no contention (amended 2026-08-14 12:40)
18. the tier budget holds: letters, accompaniments, miracles, duration and held time, with the
    camera counted as one accompaniment wherever the score names a camera track — a score carrying
    two accompaniment cues, a camera and a middle tier reads red (extended 2026-08-14 10:31)
19. a score naming a door the instrument's manifest leaves blank is refused at build time
20. a version-1 score and a version-2 score both pass the checker, and the reader says which it read
21. an authored intent line carrying a private sentence reds the build
22. a resource declaration understating its bytes reds, alongside one understating its counts
23. every declared command names a destination, and the door counts as one
24. a second declare inside one frame is refused with its reason
25. every exit from a running transaction ends in exactly one dock, failures included
26. a settle or fail carrying another command's token changes nothing
27. the covered walk is inert, hidden from the accessibility tree, and its caption watchers are
    suspended while a renderer holds the frame; focus returns to the arriving work at the landing
28. a legal instant transition and a hung instrument read differently on the diagnostic surface
29. the full engine prover is green
30. the full tlvphotos prover is green against the pinned staging engine
31. a 120-second phone profile, when a physical device is available

**Rows 32 to 49 were added 2026-08-14 08:47 on his word of 08:39, row 50 on 2026-08-14 09:52 and
row 51 on 10:31.** Rows 38 to 44 are written and green, in `tests/test_pass_hang.py` at `7ee2708`.
Rows 32 to 37, 45 to 51 are unwritten. This note read that every one of them was unwritten, which
was true at 08:47. They are the evidence for §4.6, §4.7, §2.6 and §4.8, and each reds
when its rule is removed, like every row above it.

32. an ElementSet plus its complement reconstructs the source frame within the seam threshold
33. a provider that cannot serve a work declines with its reason, and the composer falls to the next
    provider in the request's own order
34. the fallback provider returns an ElementSet for every ordered pair in the collection, a single
    decline reading red
35. the scene plan contains real actors, never one accidental fullscreen cue: a ScenePlan naming no
    element of either work is refused, and one naming at least one element of each is accepted
36. a ScenePlan's declared tier agrees with the serialised score's duration band and voice counts
37. two cues overlapping in time pass, and two cues intersecting on one structural level in
    overlapping windows still red under row 17
38. the renderer's door for B agrees with the DOM's hang geometry for B, to the pixel
39. the handoff from canvas to DOM shows no flash, no blank frame and no z-index leak
40. `chromeReveal` runs exactly once per command
41. the chrome appears after arrival and handoff, and at no earlier instant
42. focus and the accessibility tree change exactly once across a passage
43. audio, history, story and caption stay coherent across a passage
44. the viewport and orientation matrix passes: a resize or orientation change mid-passage
    recalculates the destination hang geometry and reframes the camera with no jump
45. B to A after A to B keeps the family and the pivot of the recorded pass
46. a backward plan that replays the forward pass frame for frame is refused
47. a backward plan sharing neither the family nor the pivot of the recorded pass is refused
48. a repeat crossing of one edge, under the same visit, seed and history, repeats to the pixel
49. no EdgeMemory field beyond `family`, `seed` and `passIndex` reaches a ScenePlan or a score
50. a ScenePlan whose `intent` line is empty or generic is refused, and an authored line reaches the
    score's own `intent` unchanged (added 2026-08-14 09:52)
51. the `hangGeometry` measurement callback mutates nothing — the product's own state, the DOM and
    the command are byte-identical across a call, which is what makes §1.1's declared exception an
    exception rather than a hole (added 2026-08-14 10:31)
52. a cue that writes coverage lets the cue beneath it reach the frame, measured on a stack where
    the lower cue would otherwise be drawn and never seen (added 2026-08-14 12:40)
53. both doors stay whole within the seam threshold when cues are stacked under the coverage law
54. a one-cue score is unchanged to the pixel under the coverage law, so the law costs nothing where
    nothing is stacked
55. no instrument writes a weight of presence over its whole frame, and no alpha is imposed by the
    host
56. no plan-only field — `cast`, `levelOwnership`, `measuredHandles`, `returnOf` — reaches a shipped
    file, which is the fence §4.8 depends on
57. the built host contains no instrument name: a grep for each of the three reds on any occurrence
    (added 2026-08-14 13:26; measured that day at zero occurrences in the host against eight, seven
    and six in the pack)
58. the monolithic file and the host-plus-pack, stood side by side on one score, agree to the pixel —
    mean 0.000000 and worst channel 0 of 255 at all three sampled instants
59. a uniform sourced from outside the closed set of §7 is refused at registration
60. a pack whose digest or declared version disagrees with its address is refused, and the walk's own
    glide lands with the reason recorded
61. in a stack of more than one cue, only the lowest cue may declare `coverage:{writes:false}`: an
    opaque cue standing above another reds, and a one-cue score is exempt (added 2026-08-14 14:05)

The existing prover is never weakened to make a new picture pass. Lifecycle evidence is added first;
an old check changes only when the replacement is proved equivalent.

**The blast radius, named in advance.** The tlvphotos suite holds a hard fence asserting that door
windows and frames carry no transform. A geometric transition moves exactly those elements. The
repair is to scope that assertion by the visual-layer setting, so it keeps its full force on the walk
as shipped and states its own condition where a transition plays. Scoping a check by a declared
condition preserves its reach; loosening its threshold would not, and is refused.

**Pinning the site's prover to this branch.** The site's build resolves the engine through one
literal home path, repeated in nine places across seven files, so the site's prover has never seen
the seam. The lock adds one environment name, `EXHIBITION_ENGINE_ROOT`, defaulting to today's path,
read wherever that literal stands. A run against this branch then sets the name and changes no file;
the default keeps every existing run byte-identical.

---

## 10. The three defects this lock repairs

**10.1 A takeover produced no dock.** When a renderer took a command, the motion fragment returned
before the scroll animation, so nothing wrote the scroll position, so the in-view watcher never
fired, so nothing made B current. The renderer's `done` flushed a held observer report which, under
the default land policy, never existed. The repair: `settle()` is the dock. The host calls
`adapter.dock(cmd)` on settle, and the in-view watcher keeps its own job for the walk's own glide.
`prepare` also owns arming and decoding both sources, so B's pixels are ready before takeover
instead of being armed inside the landing.

**10.2 Exactly-once could not be built on element plus generation.** The seam's landing gate deduped
by element and generation and never checked the command's declared destination, so on a chained
A → B → C the middle work docked under the last generation and then the last work docked as well —
two docks for one gesture. The repair: `dock(cmd)` reads `cmd.to` and takes no element, and the key
is generation together with destination.

**10.3 Cancel was reachable only from the scroll loop.** The one caller of the abort sat inside the
glide's own animation step. During a takeover that loop does not run, so a closer look, a question,
a gift or a door opening mid-flight never reached the renderer, and a rotation superseded the command
instead of resizing it. The repair: `adapter.interrupt(reason)` is called by every product surface
that stands in front of the walk, and the orientation road calls `adapter.reframe(viewport)`, which
resizes a running transaction rather than replacing it.

---

## 11. Declared and unbuilt, with owners

| item | state | owner |
|---|---|---|
| the interruption cadence — every handle to its nearest door within its own envelope | built 2026-08-14: the whole transition picks the door its own door-handle stands nearer, every handle then walks to the value IT takes at that door on its own named curve, and the host force-ends at the deadline with the last frame drawn ON the door | closed |
| the cadence ahead of a *supersede* | a superseded transition puts every handle on its door in one step instead of walking there, because the product's `declare` is synchronous and this branch left the product side untouched. Every handle still lands at a door and the record says `forced` | the bundle, a later branch |
| `pointer` driver | declared; one normalised host signal arrives later; instruments attach no listeners | a later branch |
| PairDossier direction A→B against B→A | amended 2026-08-14: §4.8 states where the direction is recorded and what holds across it. `lab/data/pair-shared.json` is unordered — 7260 rows, no row's reverse present — so the direction lives in EdgeMemory and in the ScenePlan's own `direction` field. Unbuilt | site build, with the walk |
| offline masks and segments | amended 2026-08-14: the extraction landed. `lab/data/objects-pass2.json` carries five named classes with per-region boxes, confidences and a complement on a 32-cell grid, for all 121 works, measured 2026-08-12 by `qwen3-vl:8b`. The provider that reads them is unbuilt | site build |
| the `structural` element provider | unbuilt; `lab/data/recipes.json` and `lab/data/motifs.json` stand, all 121 works | site build |
| the `semantic` element provider | unbuilt; its data stands, as the row above records | site build |
| the `hybrid` element provider | unbuilt; blocked on neither file, since both stand. Semantic wins where the two overlap and the merge records that it did | site build |
| the `fallback` element provider — tonal zones plus detail scales | unbuilt, and the majority road: 4793 of 7260 pairs, 66.02 percent, share no measure | site build |
| the `author` element provider — hand-drawn masks and regions | declared and unbuilt; no file backs it today | the author's seat (Fable) |
| the passage composer that emits a ScenePlan (§4.7) | declared and unbuilt. Until it lands, §4.4c's template and table stay the road that produces scores | a later branch |
| where the passage composer runs — the bundle or the renderer's own file | undecided; its size is unmeasured, and §12's split is the question it answers | a later branch, at the composer's first landing |
| the woven instrument's ElementSet-naming port | the instrument plays two whole works today. Its port names A's strips and B's strips as actors at the composer's landing, which is what row 35 asks of it | the instrument's port, at the composer's landing |
| the return to the hang (§2.6) — `hangGeometry`, the two exact geometries, the canvas-to-DOM handoff | built 2026-08-14 at `7ee2708`: 21 conformance rows green, five red-on-bug proofs, departure and arrival agreeing with the DOM inside the seam threshold of 6 of 255, and the rest at 0.000000000 against 1e-6. The row named one run's pixel means until 11:12; they drift per run and the threshold is the judged fact | closed, except the divergence in the row below and the flake in the row under it |
| §2.6's row 7, the orientation change mid-passage | observed flaky 2026-08-14 11:12: one run of `tests/test_pass_hang.py` failed it with the pose turning 0.629031 against the undisturbed flight's 0.186345 on a 3.0× bar, and a re-run passed 21 of 21. A row that reds intermittently proves nothing on the run where it passes | the hang suite's owner, before §2.6 is called closed |
| how the two geometries reach the host | §2.6 asks them to arrive as data frozen onto the command's `doors`. What was built hands the measurement through a read-only hook the product owns, which the host calls at `prepare` and at `reframe`, because freezing the record onto every declared command costs bundle bytes and the walk's bundle stands at 67 985 B against a 68 000 B fence — 15 B remaining. §1.1 declares the exception and row 51, unwritten, is what will prove the callback mutates nothing. The two readings are reconciled by that declaration and the divergence stays open as a design question | a later branch, when the bundle has room |
| `chromeReveal` as a scoreable product choreography with its six named parts | built 2026-08-14 at `7ee2708`: the chrome is revealed once, after the landing, with its parts named — plaque, counter, focus, share, sound and series — and a score may name the chrome's own timing | closed |
| EdgeMemory (§4.8) | declared and unbuilt; held by the walk in the site's layer, and the engine sees only `returnOf` | the walk, in tlvphotos |
| the instruments leaving the renderer's own file | landed 2026-08-14 at `b212ef3`: the three instruments live in `engine/assets/pass-pack.js`, the host loads it by address under a version and digest rule, the built host carries no instrument name, and the old file and the new pair agree to the pixel. §7 states the boundary and §12 the fences | closed |
| who owns the pack and its manifests | his brief has tlvphotos owning them; the engine bakes the pack today, so the boundary stands in the code while the ownership does not. The handover needs three decisions: the file's shape, the version and digest rule, and where the address is recorded | tlvphotos, on his brief; unscheduled |
| the pack loads through a blob script | no content-security policy is set by the engine today, so nothing refuses it now. A policy added later must name this road, or the picture stops loading on the deployment that adds it | whoever adds the first content-security policy |
| the digest check fails closed with no subtle-crypto | a browser offering no subtle-crypto cannot verify the digest, so the pack is refused and the walk's own glide lands with the reason recorded. This costs the picture on a plain-http deployment, where subtle-crypto is unavailable by the browser's own rule | a later branch, with the deployment's owner |
| a conformance row reads a build-time gate in the tlvphotos tree | the row degrades to a named skip when that tree is absent, so an engine-only checkout reports a skip rather than a pass. A skip that reads as a pass is the failure to watch for here | the suite's owner |
| the shape of the plan's `measuredHandles` field | named 2026-08-14 as a plan-only field that never travels, with its shape left to the plan gate. This contract fixes only that it stays in the plan; what it holds is undefined here | the plan gate's owner |
| the woven instrument's band count | the floor stands at 8 against this pair's measured 3, recorded as requested-against-applied across 1935 cues. It is the first place his brief's requirement that every meaningful number carry both values actually bites, and the divergence between what the pair measures and what the instrument will draw is unresolved | the instrument's port, with his eye on the motion |
| the version-pinned opaque effect pack (§12) | declared and unbuilt. The engine knows no TLV effect name and loads the pack; tlvphotos owns it and its manifests, and the renderer's file then holds the host alone. It is what stops the renderer file's fence tracking the effect farm — 25 lab modules on disk, and headroom after each move smaller than one instrument costs. Queued behind the first composed passage playing | a later branch, on his word of 2026-08-14 08:39 |
| the byte fence for the renderer's own file | moved again 2026-08-14 at `83ddc82`, sized after the merge of three instruments and the return to the hang: 102 000 B raw (measured 92 669) and 27 000 B gzipped (measured 24 270), each with its breakdown written into its test. The row read 42 000 B raw and 13 000 B gzipped until 11:12 | closed, and §12 states what ends the moving |

**The interruption field is read and what happened is recorded.** A score names `interruption` with
its own `withinMs`, and the host reads it. The diagnostic surface then carries the whole cadence: the
reason, the door it walked to, the budget it had, the milliseconds it actually took, and, per handle,
what the door wanted against where the handle finished. A cadence that had to be forced says so.
Silence about a field is what makes a field dangerous.

**The two tolerances the camera is judged by are stated, not implied.** The pose rests on the
arriving work within 1e-6 — on the arriving work's hang geometry, since the amendment of
2026-08-14 08:47 to §6 — and two authorities agree across a handoff within 1e-3. Both are
computation tolerances rather than matters of taste: the check reads the pose, a spline evaluated at
its own last point returns that point, and the handoff is measured at the window's own edge rather
than at whichever frame landed past it — so a slower device cannot read as a bigger discontinuity.

## 12. Where the code lives, and what fits

**Bundle headroom, measured 2026-08-14 at `83ddc82` on `pass-api-v1`** by running
`tests/test_budget.py` in this worktree: the walk's own bundle is 67 985 B gzipped against a
68 000 B fence. **15 B remain.** The machinery described here is larger than that by orders, so the
whole transaction cannot live in the bundle.

**Re-measured 2026-08-16 on `pass-api-v1-familybreath`**, again by running `tests/test_budget.py` in
the worktree: the bundle is 69 614 B gzipped against a fence moved to 70 000 B, so **386 B remain**.
The fence moved because the family roll of §4.4f landed in the bundle — 980 B gzipped — and the
delivery question it forces was answered rather than waved through: the roll is called from inside
`declare` on BOTH fill roads, and a site scoring by §4.4c's template and table fetches no reader file
at all, so the roll cannot travel in `pass-reader.js` and cannot exist twice. The reader is handed it.
The 68 000 B reading below is superseded and kept for its reasoning.

**Re-measured 2026-08-17 on `u27-base` after stage 0's seam**, by running `tests/test_budget.py` in
the worktree: the fence stands unmoved at 70 000 B. Three roads left the bundle — the settings
record's own per-pair scores, the pack reader's door with its shard warming, and the
template-and-table fill — and one arrived: the composer's door, the passage request the walk builds
per edge, the die it rolls for it, and the applied reading written back at the landing. The visit's
own seed stays in the bundle for the reason stated above, which is unchanged: the die every crossing
is rolled with is made inside `declare`.

Fifteen bytes is a live constraint rather than a rounding note. Any bundle-side line added today
breaks that fence, and a reader who adds one should expect the red. The section's earlier figure —
64 828 B against a 67 000 B fence, measured 2026-08-13 23:16 — is superseded; both numbers moved,
and the superseded text is in `PASS-API-V1-HISTORY.md` with its date.

**The split is therefore stated, and it is the delivery answer the fence exists to force.**

*In the bundle, the product's own authority:* `declare` with its freeze and generation, `dock`,
`glide`, `interrupt`, `reframe`, `curtain`, `mark`, and the register of live settings that already
stands. These are the promises the product makes about itself, and they must hold on a visit where
the renderer's file never arrives.

*In the renderer's own file:* the host — the state machine, the watchdog, the idempotence guard, the
cadence, the frame loop, the GPU and resource machinery, the driver evaluator, the camera, the
census, the diagnostic surface's renderer half, and the pack loader. None of it is needed on a visit
that never draws.

*In the pack, fetched after the host on a visit that draws:* the instruments, with their shaders,
their response curves and their manifests. §7 states the boundary and what each side owns.

**The renderer file's fence moves with its reason written into the test**, the same way the bundle's
did on 2026-08-13. This section used to promise that the number would be measured at the first
landing of a real instrument. That landing has happened three times over, so the promise is replaced
by the record.

**The split landed at `b212ef3`, and this section now describes what stands.** The three
instruments left the renderer's own file for `engine/assets/pass-pack.js`, which the host loads by
address under the version and digest rule of §7. Until 2026-08-14 13:26 this section described the
split as the delivery answer it was waiting for; the superseded text is in `PASS-API-V1-HISTORY.md`
with its date.

**The proof that the split changed no pixel.** The old monolithic file and the new host-plus-pack
were stood side by side on one score and read a mean of 0.000000 with a worst channel of 0 of 255,
at all three sampled instants. A delivery change that moves a pixel is a product change wearing a
build change's clothes, so this is the row that licenses the split rather than the byte counts.
Row 58 carries it.

**The four fences, measured 2026-08-14 13:26 in this worktree.** The gzipped figures come from
`python3 tests/test_budget.py`, which strips comments as the shipped file is stripped; the raw
figures come from building the site and sizing the artefacts, against constants carried in
`tests/test_pass_api.py` and `tests/test_pass_pack.py`. The unit is bytes.

| file | measured | fence | headroom |
|---|---|---|---|
| the host, built raw | 78 237 B | 86 000 B, down from 102 000 | 7 763 B |
| the host, gzipped | 21 669 B | 24 000 B, down from 27 000 | 2 331 B |
| the pack, raw | 34 589 B | 38 000 B, new on its first day | 3 411 B |
| the pack, gzipped | 7 894 B | 8 700 B, new | 806 B |
| the walk's own bundle | 67 985 B | 68 000 B, untouched | 15 B |

**Both host fences moved DOWN**, which is the fact worth reading twice. Every earlier move of this
fence went up, because each landing instrument wrote its shader into the one file. The fences now
track the host and have stopped tracking the effect farm, so a fourth instrument moves the pack's
fence and leaves the host's alone.

The walk's own bundle is untouched at 15 B of headroom. That is a live constraint: a bundle-side
line added today breaks that fence, and a reader who adds one should expect the red.

**The ownership half is not done, and it is a handover rather than a promise.** His brief has
tlvphotos owning the pack and its manifests. Today the engine still bakes it, so the boundary stands
in the code while the ownership does not. Three things the handover needs, and each is a decision
rather than a task: the file's shape, the version and digest rule, and where the address is
recorded. §11 carries it as a row with an owner.
