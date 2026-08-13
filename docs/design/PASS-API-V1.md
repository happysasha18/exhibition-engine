# PASS API v1 — the transition contract

**Root.** His word 2026-08-13 23:03: a feature-preserving immersive edition of TLV Photos. The
existing product keeps the door, the walks 10 + 5 + 5, story, series, quiz, gift, zoom, sound,
share/history, every input method, resize/orientation/DPR, RTL, reduced motion, Save-Data,
analytics/A-B and the static layer. A crossing is a subordinate visual transaction A → B; it owns
none of those.

**Status, 2026-08-13 23:30.** This document is a written contract and nothing in it is built yet. The
renderer's file `engine/assets/pass-layer.js` is still the 19-line stub that declines every command,
and the host described here has no file on disk. Section 11 lists what is declared-and-unbuilt; that
list is a subset of "unbuilt", because at this moment the whole contract is.

Any line below that reads as a description of behaviour is a specification of behaviour to be built,
and the conformance rows of §9 are the evidence that will make each one true.

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

## 4. The four data objects

Pixels, knowledge about one work, and knowledge about a pair stay apart.

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
  roles:["disassembly"|"mystery"|"assembly"],
  levels:["WORLD"|"SURFACE"|"CELL"|"CELL CONTENT"|"TEXTURE"|"LIGHT-COLOUR", ...],
  window:[t0,t1], works:["a","b"], stack, cameraAuthority:"stage"|"own",
  doors:{ in:{handle,value,measured}, out:{handle,value,measured} },
  nodes:{ <name>: <driver node> },
  tracks:{ <handle>: <driver node or node reference> },
  resources:{ textures, textureSlots, framebuffers, pingPong, programs, passes,
              bytesEstimate, variant } }
```

**`voice` and `roles` are two different questions and both are asked.** `voice` says what the cue
counts as in the budget — a structural gesture, an accompanying voice, or the one impossible event.
`roles` says what the cue does dramatically inside the pass. The budget check reads `voice`; the
composition check reads `roles`. Writing only one of them made the tier budgets uncheckable, which
the adversarial review of 2026-08-13 23:30 proved by writing a legal score that broke them.

**`levels` is a list**, because a real instrument occupies more than one at once — the woven
instrument moves at SURFACE while each strip turns at CELL, which is exactly why it reads as alive.
The levels law is then checkable: two cues whose level lists intersect, in overlapping windows, are
a red unless one of them declares itself the accompaniment of the other.

**The tier budget check.** From `voice`, `levels`, `window` and the score's `duration`: a quiet link
carries one letter, at most one accompaniment, no miracle, 2–4 s; a middle carries at most two
letters, at most two accompaniments, at most one miracle, 5–8 s; a culmination carries two or three
letters, at most three accompaniments, exactly one miracle, 9–14 s; and held time stays under a
third of the pass. Everything counts, and no cue is exempt.

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

---

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

**Built in the alpha:** `static`, `phase`/`time` curves and splines, `oscillate`, `velocity`
response, node references. **Declared and falling back to base:** `pointer`, `capability` variants
beyond the three named tiers. Every fallback is recorded with its reason on the diagnostic surface.

---

## 6. The camera

One continuous voice with its own arc, resting exactly on B.

```
{ at, pan:{x,y}, logScale, pitch, yaw, roll, fov, owner:"stage"|"cue:<id>" }
```

Dolly travels in **log space** and is interpolated there; the existing lab engine interpolates raw
scale on both of its paths, which the charter's own law contradicts, so the lock states log space and
a check proves it.

**One authority at a time.** The score names the owner per window. A cue that carries the camera by
its own device declares `cameraAuthority:"own"`, and the stage's flight holds still across that
window. Handoffs are continuous: at a handoff instant the two poses must agree within a stated
tolerance, and a conformance row measures the pose across the handoff frame by frame.

**Rest on B.** The last pose equals the neutral pose within tolerance, and the check reads the pose
rather than the picture, so it stays honest when the picture changes.

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

**Context loss.** `contextLost()` drops instrument handles and the curtain; `contextRestored()`
rebuilds from granted resources or fails. A census row proves that texture, program and framebuffer
counts return to their baseline after repeated runs.

---

## 8. Instrument manifest

```
{ id, api, arity:1|2, roles, params:{...}, handles:{...},
  neutrals:{...}, doors:{...}, framings:{...}, drivers:[...],
  camera:{ needs, authority }, passes:[...],
  resources:{ lean:{...}, standard:{...}, rich:{...} },
  capabilities:[...], decline:[...], provenance:{ labPath, commit },
  readiness:"production-ready"|"needs-port"|"lab-only"|"failed-proof" }
```

The lab modules are source material. Their own canvas, context, frame loop and pointer code is not a
production port; a port is the instrument's mathematics carried onto the host's frame with a
manifest and a passing conformance run.

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
17. two cues whose level lists intersect in overlapping windows are a red, unless one declares
    itself the other's accompaniment
18. the tier budget holds: letters, accompaniments, miracles, duration and held time
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
| the interruption cadence — every handle to its nearest door within its own envelope | declared in the score, unbuilt in both repositories; today only a hard stop exists | the host, this branch |
| `pointer` driver | declared; one normalised host signal arrives later; instruments attach no listeners | a later branch |
| PairDossier direction A→B against B→A | recorded nowhere today | site build |
| offline masks and segments | parked until the semantic pass is promoted | parked |
| the byte fence for the renderer's own file | 4 000 B today, holding a 167 B stub; a real host and instrument will need a larger number with its reason written into the test | this branch |

**The interruption field is accepted and its fallback is recorded.** A score may name
`interruption` today. Until the cadence is built, the host accepts the field, plays a hard resolve,
and records the fallback with its reason on the diagnostic surface — the same treatment every
unbuilt driver kind gets. Silence about an unbuilt field is what makes an unbuilt field dangerous.

## 12. Where the code lives, and what fits

**Bundle headroom, measured 2026-08-13 23:16 on `pass-api-v1`:** the walk's bundle is 64 828 B
gzipped against a 67 000 B fence, so 2 172 B gzipped remain — about 7 500 B of source at this
bundle's own ratio. The seam's own product-side fragment already costs about 4 800 B, and the
machinery described here is larger than that, so the whole transaction cannot live in the bundle.

**The split is therefore stated, and it is the delivery answer the fence exists to force.**

*In the bundle, the product's own authority:* `declare` with its freeze and generation, `dock`,
`glide`, `interrupt`, `reframe`, `curtain`, `mark`, and the register of live settings that already
stands. These are the promises the product makes about itself, and they must hold on a visit where
the renderer's file never arrives.

*In the renderer's own file:* the host — the state machine, the watchdog, the idempotence guard, the
cadence, the frame loop, the GPU and resource machinery, the driver evaluator, the camera, the
census and the diagnostic surface's renderer half. None of it is needed on a visit that never draws.

**The renderer file's fence moves with its reason written into the test**, the same way the bundle's
did on 2026-08-13. A host plus one instrument will not fit 4 000 B, and the number that replaces it
is measured rather than guessed, at the first landing of a real instrument.
