# Coverage — what each instrument writes where its own matter is absent

**Root.** His word of 2026-08-14 08:39: a passage is several voices, with cues overlapping freely.
The measurement of 10:47 says what stops that from happening. The host draws three instruments in one
frame; every instrument writes `vec4(col, 1.0)`; so a visitor sees only the cue nearest the eye, and
the band family that the whole passage stands on is drawn under every frame from 1.17 s onward and
appears at no instant. On the worked pair that is 5.33 s of a 6.5 s pass — four fifths of its length.

**Where this document sits.** `PASS-API-V1.md` §7 states the law and §8 carries the manifest block
that declares it; both are read-only here and this document is the per-instrument specification §7
names. `lab/PASSAGE-COMPOSER.md` §2a is the artistic finding the law came from. For each of the three
landed instruments this document gives the quantity it already computes that says where its material
is, the alpha it should carry, what happens at its doors, and what the composed passage then looks
like. It changes no code.

**Where the code being cited lives.** The three instruments left `engine/assets/pass-layer.js` on
2026-08-14 at `b212ef3`, and each of them now travels in a version-pinned file of its own —
`engine/assets/pass-inst-<name>.js` — which the host loads at the address the site's own settings
record gives that instrument's name. Every shader citation below names the file its own instrument
travels in and every host citation is `pass-layer.js`, both as they stand with coverage landed. A reader following a citation
into the pre-coverage tree, or into the older monolithic file, will find the same lines at different
numbers.

**What is built, and what this document now records.** The specification was accepted on 2026-08-14
and built in the order §8 sets out. The three instruments carry their alpha and their `coverage`
block, the host composites straight source-over and refuses a stack whose floor writes coverage, and
conformance rows 52 to 55 are green in `tests/test_pass_coverage.py` with a red-on-bug proof each.
Every number in §5, §7 and §9 below is a measurement from that suite rather than a prediction, and
where a prediction was wrong the correction is marked as one.

---

## 1. The law, and the mechanism it replaces

**THE COVERAGE LAW**, in §7's own words. An instrument writes opaque where its own matter stands and
clear where its matter is absent. The frame it hands back is its elements together with the space
between them, and that space belongs to whatever plays underneath.

This is the charter's twelfth shelf at the level of one drawn frame. The complement law there says
every extracted element is stored with its complement so the whole frame is reconstructable at any
moment. An instrument drawing its own elements and leaving the complement clear is that same sentence
applied to pixels.

**The mechanism this replaces is banned in the charter's own words.** A score carries no field of
opacity, the engine hands out no handle for it, and a plan physically cannot fade layers. So there is
no per-cue weight of presence and no host-imposed alpha. Coverage is each instrument's own statement
about where its material is, computed from the same numbers that already decide what it paints.

**Coverage is published rather than invented, and it asks the host for nothing new.** Each of the
three shaders already computes, at every point of the frame, the quantity that separates the two works.
Today that quantity reaches the colour channel and stops. The change carries it one step further, into
the fourth component. No new mathematics enters any of the three shaders, and — this is what makes the
change landable at all — **no new uniform is needed.** The pack's uniform sources are a closed set:
the two source textures, their fits, the resolution, the transaction's seconds, a value the
instrument's own `values()` answers, and a handle. Every quantity this document names is computed
inside the fragment shader from uniforms already declared, so no manifest gains a `source` the host
would refuse at registration.

---

## 2. The woven instrument — `pass-inst-weave.js:56–153`

### 2.1 Where its matter stands

Its matter stands at every point of the frame, and the shader's own partition states it.

Two ribbon sets are computed. The vertical set takes its colour from `covV = sqcov(cV, dutyV, wV)`
(`:117`), a square-wave coverage over the strip period, used as the weight in
`colV = mix(texB(...), texA(...), covV)` (`:118`). The horizontal set is the same construction at
`:124–125`. Both branches of each mix are picture: `covV` chooses between work A and work B and never
between matter and void.

The two sets are then partitioned by `showV = step(ord * 0.996 + 0.002, choose)` (`:138`), which is 0
or 1 at every point, and `col = mix(colH, colV, showV)` (`:139`). Every point of the frame takes one
of the two sets. The union of the sets is the frame, so the fabric leaves no point unclaimed.

**The grooves are a shading term.** `grooveV`, `grooveH`, `diveV`, `diveH` (`:141–144`) gather into
`shade` (`:145`), gated by `shadeGate` (`:146`), and reach the picture only through
`col *= 1.0 - basket * shadeGate * min(shade, 0.62)` (`:147`). They darken where two ribbons meet and
where one dives under the other. Darkening is a statement about light rather than about absence, and
writing it into the alpha would punch the fabric with a hole at every ribbon edge.

### 2.2 The alpha it should carry

    gl_FragColor = vec4(col, 1.0);          // :148, unchanged

Unchanged, and stated as a decision rather than left as a default. Its manifest declares

    coverage: { writes: false,
                how: "the fabric partitions the frame between its two ribbon sets, so no point of
                      the frame is left unclaimed" }

**The reason.** The woven instrument owns SURFACE for the whole pass and carries the pivot — the band
family both works hold. It is the ground the other two voices play over, and in the composed passage
it is the score's `stack: 0`, the cue laid down first. There is nothing beneath it but the cleared
drawing buffer, which the context holds at opaque black (`alpha: false`, `pass-layer.js:118`;
`preserveDrawingBuffer: false`, `:119`). An alpha below 1 anywhere in this instrument shows that black
through the frame.

### 2.3 Its doors

Both doors are opaque because the alpha is the constant 1.

At `mix = 0` the derived balance gives `duty = 1`, and `sqcov` returns `1.0` on its own first guard
(`if (d >= 1.0) return 1.0;`, `:77`), so `covV` and `covH` are 1 at every point and both sets read
`texA`. At `mix = 1` the duty is 0, `sqcov` returns `0.0` (`:78`), and both sets read `texB`. The
strip travel is 0 at both ends (`amp` through the `weave` gate, `:216`), the edge breath is 0
(`alive`, `:94`) and the shading is 0 (`shadeGate`, `:146`). Each door is one whole work under the
constant centre crop of 1.29 the travel is paid for with.

---

## 3. `matter` — `pass-inst-matter.js:80–157`

### 3.1 Where its matter stands

The quantity is `cov`, at `:446`:

    float d = (F - uTau) / (grad * h);
    float cov = clamp(0.5 + d, 0.0, 1.0);

`F` (`:441`) is the field — six parts a plain ladder across the frame, four parts two grains of value
noise. `uTau` is the threshold, which travels from a tenth below the field's whole range to a tenth
above it as the dial runs (`tau`, `:534`). `d` is the signed distance from the threshold measured in
points, since `h = 1.0 / uRes.y` (`:435`) and `grad` is the field's own gradient length (`:444`). So
`cov` is a one-point antialiased mask: 1 where the point still stands on work A's side of the front, 0
where the front has passed it and work B has arrived.

`col = mix(colB, colA, cov)` (`:460`) reads it as the share of A. `1.0 - cov` is therefore the share
of B: the territory the arriving work has taken. That territory is what this instrument builds. The
quantity is the lab module's own, under the module's own name (`lab/effects/matter.js:115`).

### 3.2 The alpha it should carry

    gl_FragColor = vec4(col, 1.0 - cov);    // replacing :472

    coverage: { writes: true,
                how: "1.0 - cov, the share of the arriving work at the travelling threshold" }

**The reason, in three parts.**

Its entry door then costs nothing. At `mix = 0` the threshold stands a tenth below the field, `cov` is
1 at every point and the alpha is 0 at every point. The instant the cue's window opens the frame does
not change, which is what makes a cue joinable part-way into a pass and what row 8 measures at a
window edge.

Its exit door is then whole. At `mix = 1` the threshold stands a tenth above the field, `cov` is 0 at
every point and the alpha is 1 at every point, with the colour `mix(colB, colA, 0) = colB`.

Between them the instrument publishes what it has actually built. Work B grows out of the frame
beneath it rather than being pasted over it, which is §2a's third consequence: a work that condenses
at a locus needs the world it condenses out of to remain on screen while it does.

**The opposite choice fails all three.** An alpha of `cov` would open the cue as a total replacement
and close it showing nothing at all.

### 3.3 Its doors

At `mix = 1` the alpha is 1 at every point, the drag is 0 (`loosen` carries the factor `4·d·(1-d)`,
`:536`) and the contact shadow is 0 (`guard` through `smoothstep(1, 0.91, d)`, `:537`). Door B is
`texB` whole and opaque under the crop of 1.17, unchanged from what it is today, and it is what the
composed passage's own door B is measured against.

At `mix = 0` the alpha is 0 at every point. The instrument contributes nothing and the door belongs to
whatever plays underneath. This is safe wherever the score gives it something underneath, which is the
placement rule of §6. In the composed passage `matter` opens at 4.03 s with two cues already standing
beneath it.

---

## 4. The meshing instrument — `pass-inst-gears.js:83–182`

### 4.1 Where its matter stands

The quantity is `cov`, at `:779`, built from the same shape:

    float M = (RA - rA) - (RB - rB) + uSpread * (ord - 0.5);
    float d = M / (grad * h);
    float cov = clamp(0.5 + d, 0.0, 1.0);

`RA` and `RB` (`:762–763`) are the two rims with their teeth standing on them, the second wheel's
teeth being the first's turned inside out. `M` (`:771`) is how far inside wheel A's rim the point lies
against how far inside wheel B's, with the tooth handover spread across the mesh (`:767–769`). `grad`
is the field's exact gradient (`:774–777`), `h = 2.0 / uRes.y` (`:745`), so `d` is again a signed
distance in points and `cov` is a one-point mask: 1 for the points wheel A owns, 0 for the points
wheel B owns. `col = mix(colB, colA, cov)` (`:787`) reads it. The name and the line came across from
`lab/effects/gears.js:136`.

The line where the two rims meet — the row of interlocking teeth, which is what the eye actually sees
here — is the boundary of that mask. Publishing `1.0 - cov` as the alpha makes that line the edge of
the instrument's own matter, which is what it already is geometrically.

### 4.2 The alpha it should carry

    gl_FragColor = vec4(col, 1.0 - cov);    // replacing :800

    coverage: { writes: true,
                how: "1.0 - cov, the share of the frame inside the arriving wheel's rim" }

**The reason** is §3.2's, unchanged: this instrument and `matter` share one construction — a signed
field, a one-point coverage taken from it, and the two works mixed by that coverage — so one sentence
covers both. The territory of the arriving wheel is the instrument's matter; the territory of the
departing wheel is what stood on screen before this cue opened.

### 4.3 Its doors

The doors are exact by construction rather than by margin. `reachFor` (`:899–914`) bisects on the
distance the wheel pair is carried out until `doorsHold` (`:895–898`) reports that all four corners of
the frame satisfy the door condition with the teeth and the spread allowed for. At `mix = 1`,
`xc = -reach` (`:972`) puts every point of the frame inside wheel B's rim: `cov` is 0 at every point,
the alpha is 1 at every point, the tangential sweep is 0 (`off`, `:987`) and the contact shadow is 0
(`guard`, `:988`). Door B is `texB` whole and opaque under the crop of 1.13.

At `mix = 0`, `xc = +reach` puts every point inside wheel A's rim, `cov` is 1 at every point and the
alpha is 0 at every point. The same condition as `matter`'s entry door applies. In the composed
passage it opens at 1.17 s with the band family already standing beneath it.

---

## 5. The composed passage under this specification

The worked pair is `17847744487144891 → 17897050660015868`, played by the score in
`tests/test_pass_stack.py`: the band family at SURFACE for the whole pass, the travel at CELL from
1.17 to 5.59 s, the arrival at TEXTURE from 4.03 to 6.5 s, and the camera as the stage's own voice.
Each cue drives its `mix` from `cueProgress`, so each runs its own door-to-door dial across its own
window. Every number in the table is that arithmetic.

**The last column is measured rather than predicted.** The share is the fraction of frame points where
the stacked frame and the ground drawn alone agree within 6 of 255 in every channel — `agree_share()`
in `tests/test_pass_coverage.py`, over 390×844 screenshots, run by `python3
tests/test_pass_coverage.py`. It answers whether the cue beneath reaches the eye, it falls as the
voices above claim territory, and before coverage it was nil at every instant below.

| second | band family, duty | travel, dial and pair placement | arrival, dial and threshold | the ground's share |
|---|---|---|---|---|
| 0.000 | 1.0000 — work A whole | not live | not live | door A, the pivot alone |
| 1.170 | 0.8201 | 0.0000, `xc = +reach` | not live | 100.0% |
| 2.000 | 0.7223 | 0.0832, `xc = +0.834·reach` | not live | 100.0% |
| 2.500 | 0.6234 | 0.1498, `xc = +0.700·reach` | not live | 100.0% |
| 3.000 | 0.5087 | 0.2380 | not live | 100.0% |
| 3.500 | 0.4374 | 0.3350 | not live | 96.9% |
| 4.030 | 0.3695 | 0.4788, `xc = +0.043·reach` | 0.0000, `tau = -0.100` | 61.4% |
| 4.500 | 0.3006 | 0.6420 | 0.1913 | 15.6% |
| 5.000 | 0.2181 | 0.8310, `xc = -0.662·reach` | 0.4122, `tau = +0.395` | 15.8% |
| 5.590 | 0.1414 | 1.0000, `xc = -reach` | 0.5387, `tau = +0.546` | 26.6% |
| 6.500 | 0.0000 — work B whole | not live | 1.0000, `tau = +1.100` | door B, the arrival opaque |

**A correction to this document's own prediction.** An earlier draft said that at 2 seconds the mesh
line would be entering from one edge. It is not. The meshing instrument claims no point of the frame
until about 3.5 seconds: `reachFor` carries the wheel pair far enough out that at a dial of 0.0832 the
meeting line still stands beyond the frame's edge. So the travelling voice's window opens at 1.17 s
and the voice has nothing to show for the first 2.3 seconds of it. That is the score's business rather
than the instrument's — the dial curve and the reach are what set it — and it is recorded here because
the measurement found it where the reasoning had not.

**At 2 seconds** a visitor sees the vertical band family across the whole frame and nothing else: work
A's ribbons holding about 72 percent of each period with work B's narrow between them, warped by the
two width breaths and sliding along their own axis at an amplitude of 0.060 frame heights. Before
coverage this instant was one flat photograph — the meshing instrument at a low dial, drawing work A
across the whole frame, with the band family underneath it and invisible. The pivot is now the picture.

**At 4.03 seconds**, where the arrival's window opens, three voices are readable at once: the band
family's ribbons carrying work A down one side, the wheel's rim sweeping through the frame, and work
B's glass grid standing inside the arriving rim. This is the instant the whole law was for, and the
frame moved by mean 68.63 of 255 against the same instant before coverage.

**At 5 seconds** the arrival's front stands as a ragged vertical boundary about a third of the way
across the frame — the field is six parts a ladder in `uv.x`, so `F = tau` falls near
`x = (tau - 0.4·g) / 0.6` for a grain value `g` — with the grain crumbling along it and work B whole
and opaque behind it. Through the rest, the meshing instrument's rings carry work B, and the band
family holds 15.8 percent of the frame in the strip the rings have not taken. The ground thins as the
two upper voices approach their doors, which is the right shape for an arrival: the pivot is visible
through the middle of the passage and gives way as the passage lands.

**Both doors are exactly what they were before coverage.** At 0.000 s only the pivot is live, it is the bottom
cue, blending is off, and it writes work A whole. At 6.500 s the pivot and the arrival are live; the
arrival stands topmost at its exit door with alpha 1 at every point, so door B is `matter`'s own
canonical frame and the pivot beneath it reaches no point. Row 7's comparison against the canonical
files, within the seam threshold of 6 of 255, reads the same pixels it reads now.

---

## 6. The blend the host enables, and what it costs

**The frame needs straight source-over, and premultiplied alpha is refused.**

    gl0.blendFunc(gl0.SRC_ALPHA, gl0.ONE_MINUS_SRC_ALPHA);

The host writes `gl0.blendFunc(gl0.ONE, gl0.ONE_MINUS_SRC_ALPHA)` today (`pass-layer.js:359`), which
is source-over on premultiplied colour. That form cannot be used here, and the reason is in the host's
own draw path. One and the same fragment shader serves two jobs. Laid over another cue it must
contribute only its own matter. Laid down first — as the bottom cue of a stack, or as the whole of a
one-cue score — it must write the picture it writes today, and there blending is disabled
(`pass-layer.js:361`), so the fourth component is never read. A shader emitting `rgb * a` would then
write black wherever its alpha is below 1, and a one-cue `matter` score would go black across the
field.

Under straight source-over the colour channel of all three shaders stays exactly the expression it is
today. The change is one component wide. That is what makes the one-cue row hold by construction
rather than by measurement luck.

**No separate alpha equation is needed.** The context is created with `alpha: false`
(`pass-layer.js:118`), so the destination alpha never reaches the page and no blend factor here reads
it. Adding `blendFuncSeparate` would change nothing and should be left out.

**The blend belongs to the host and stays out of the manifest.** The manifest already carries what an
instrument can honestly declare about itself — `coverage:{writes, how}`, §8's own block. The blend is
a property of how a whole stack is composited, one choice for the frame rather than one per cue, and a
manifest naming its own blend would hand an instrument a multiply or an add, either of which lets one
cue darken or brighten what plays beneath it. That is an imposed weight arriving by another road, and
the charter bans the class rather than the spelling. So `coverage` declares, and the host composites.

**A one-cue score does no blending at all, and that is the law rather than a convenience.** The host
already skips it: `drawPose` is called with `drew > 0` (`pass-layer.js:1894`), where `drew` counts
what has already been laid down in this frame (`pass-layer.js:1873`), and on the first call of a frame
it takes the `else` branch and disables blending (`pass-layer.js:361`). So the bottom cue of any
stack — one cue or three — meets a context in exactly the state `stageBuild` left it
(`gl.disable(gl.BLEND)`, `pass-layer.js:152`), and its
alpha never reaches the frame. Three things follow and each should be written down rather than left to
be rediscovered:

- a single opaque cue costs nothing and is byte-identical to what it draws now, which is row 54;
- an instrument declaring `writes: true` plays alone exactly as it does today, because its alpha is
  never read when nothing is stacked;
- the skip is per frame and keyed on what has been drawn, so it holds under a resize, under the
  resolution ladder and under a cue whose window has not opened.

**The placement rule the declaration exists to check.** §8 states that an instrument declaring
`writes: false` may be drawn only as the cue nearest the eye. Read against the host's own draw order
that sentence is inverted, and the composed passage is the counter-example: the stack is drawn
ascending, the cue nearest the eye is laid down last, and the instrument that fills the frame whole is
the woven one at `stack: 0` — the cue farthest from the eye. An opaque cue nearest the eye is exactly
the defect of 10:47. The rule that holds is the mirror of it, in two halves:

- **in a score of more than one cue, the lowest-stack cue must declare `writes: false`**, because
  nothing is drawn beneath it and its gaps would show the cleared buffer;
- **every cue above the lowest must declare `writes: true`**, because a frame-filling cue anywhere
  above the floor is drawn over voices that are then never seen.

A one-cue score is exempt from both, since it never blends. This is built as `coverageWhyNo` in the
host, called from `scoreWhyNo`, refusing the command with its reason the way the camera-authority
check already does. `PASS-API-V1.md` is read-only from this branch, so §8's sentence still points the
other way; the divergence is recorded in §10 for its owner.

**What it costs.** One raster blend per fragment for every cue past the first in a frame: at 390×844
points, a device pixel ratio of 2 and the ladder's top step, 1.32 M fragments a cue. It adds no pass,
no target, no texture and no program, so every manifest's `resources` record stays as it is —
`textures: 0`, `framebuffers: 0`, `programs: 1`, `passes: 1`, `bytesEstimate: 0` — and §7's summed
grant across the stack is unchanged. In the pack's own bytes the change is one expression per shader
and one `coverage` block per manifest.

---

## 7. Conformance rows 52 to 55, and what each measures

§9 carries the four rows, one line each. They are written and green in `tests/test_pass_coverage.py`,
each with a red-on-bug proof that reverts one rule in the suite's own copy of the built pack — the
source tree is never written to. A crippled pack weighs differently and the host refuses a pack whose
digest disagrees, so each revert re-stamps the host with the digest of the bytes the bench will serve.
The suite runs 18 rows. What each of the four reads, with the number it read:

**52 — a cue that writes coverage lets the cue beneath it reach the frame.** Three frames of the
composed passage at 2.000 s with the clock pinned: the whole stack, the pivot cue alone, the travel
cue alone. The row asserts that the stack agrees with the pivot alone across a majority of the frame
and differs from the travel alone by more than the seam threshold. It read 100.0 percent agreement
with the ground and mean 42.478 of 255 against the travel. Reverting the travel's alpha to `1.0` drops
the ground to 18.5 percent and makes the stack identical to the travel again at worst channel 0.

**53 — both doors stay whole when cues are stacked**, and an alpha at a door is 0 at every point or 1
at every point. Two rows. Door A at 0.000 s against the ground drawn alone and door B at 6.500 s
against the arrival drawn alone both read mean 0.000000, worst channel 0 — pixel-exact, which is what
those two constants mean once the frames are composited. Beside them the entry doors: at 1.170 s the
travel opens and the frame is the ground untouched, at 4.030 s the arrival opens and the frame is the
ground and the travel untouched, both at worst channel 0. Inverting the travel's coverage to `cov`
makes it open at alpha 1 instead and moves 1.170 s by mean 36.860 of 255.

**54 — a one-cue score is unchanged to the pixel.** Each of the three instruments alone, at all seven
instants, drawn by the tree as it stood before coverage and by the tree as it stands now: 21
comparisons, worst channel 0. Both trees are baked the way `engine/build.py` bakes them, the pack
first and the host stamped with the digest of the bytes that will actually be served, so the
comparison is two builds rather than a build against a source. Removing the host's skip — enabling
blending for a frame's first cue — moves a one-cue arrival by mean 127.159 of 255. This is the row
that keeps the law free where nothing is stacked.

**55 — no instrument writes a weight of presence over its whole frame.** A uniform weight `w` would
make the stack the exact blend `w·T + (1-w)·P` at every point for one number `w`. The row fits the
best such `w` in closed form and reads the residual: 39.70 channel units at 4.030 s and 21.64 at
5.000 s, where a crossfade would leave nothing. Replacing the mask with one number over the whole
frame — the meshing instrument's own `uOff`, which is spatially constant and moves with the dial —
drops the residual to 0.30, which is the banned crossfade answering to its own name.

**The row is read where the mask is partial, and that is a real limit.** At 2.000 s the travelling
voice claims no point of the frame, so the stack simply is the ground, every model fits it with `w=0`,
and the instant separates a mask from a weight not at all. The first draft of this row measured there
and passed vacuously in both directions. It now reads 4.030 s and 5.000 s and says why.

---

## 8. The order of work, and the reason for it

**The woven instrument first.** It carries the passage's ground, and its coverage statement is the one
that matters most: it is the bottom cue, there is nothing beneath it but the cleared buffer, and an
alpha below 1 anywhere in it empties the frame rather than revealing anything. Its work is the
`coverage:{writes:false, how}` block, one line of comment on the alpha it already writes, and row 53's
half that proves the constant. Settling it first means the two instruments that must leave room for
the ground are afterwards measured against a ground already known to be whole.

**The meshing instrument second.** Its window holds 4.42 s of the 6.5 s pass — 68 percent, and the
longest stretch over which the ground is hidden today. One expression in its shader gives the band
family back from 1.17 s onward, and its coverage boundary is the mesh line, which is the passage's own
subject. It is also the first change whose effect can be photographed: row 52 at 2.000 s.

**`matter` last.** It holds the final 2.47 s and it holds door B, so it is the one whose coverage
touches a door measured against a canonical file. Its change turns the arrival from a paste into a
condensation and removes the jump at 4.03 s where its window opens. Leaving it last means door B is
disturbed only once the other two are proved.

The host's one blend line and the §8 placement rule land with the meshing instrument, since that is
the first cue drawn over another under this law.

---

## 9. The risks, read off the code

**9.1 `matter` loses its contact shadow — measured, and the loss is nearly total.** Drawn alone,
switching the arrival's shadow off moves its own frame by mean 3.6917 of 255, worst channel 64. Inside
the stack the same switch moves the frame by mean 0.0968, worst channel 16 — about a fortieth of the
footprint survives, and only where it falls inside the arriving work's own territory. The row is
`risk 9.1` in `tests/test_pass_coverage.py`, taken at 5.000 s with the `shade` handle at 1 against 0.
The mechanism is the line below.

Its shadow rides `cov`:

    col *= 1.0 - 0.32 * uGuard * cov * exp(-max(d, 0.0) / 7.0);            // :461

`cov` is 1 on the side the coverage makes clear, and `exp(-max(d, 0.0) / 7.0)` reaches about seven
points into that side, so the whole shadow band sits where the alpha is 0 and is discarded. The
meshing instrument's equivalent rides the other factor — `(1.0 - cov) * exp(-max(-d, 0.0) / 7.0)`
(`:789`) — so it falls on the side the coverage keeps and survives untouched. The two modules stand
their contact shadow on opposite sides of their own front, so one coverage rule treats them
differently. Casting the shadow onto what plays beneath would need a multiply blend, which is refused
in §6 for the reason given there. The shadow stays where the alpha is 1 and is lost where the alpha is
0; whether that loss is acceptable at the front is a question for his eye rather than for this
document.

**9.2 The travel cue leaves its window at full opacity — measured at 14.56 of 255.** Across
5.58 → 5.60 s the frame moves by mean 14.5592, worst channel 220, against mean 6.3848, worst channel
232, on the tree before coverage. Coverage did not create the step and it did not much enlarge the
worst channel; what it did was spread the step across the frame, since the ground now shows where the
travel stops covering. The number is the row `risk 9.2` in `tests/test_pass_coverage.py`.

At 5.590 s its dial is exactly 1.000 and
`xc = -reach`, so its alpha is 1 at every point and it is drawing work B whole. One frame later it is
outside its window and draws nothing. Beneath it stand the band family at a duty of 0.1414 and the
arrival at a threshold of 0.546, which claims a little over half the frame — so across the rest, the
picture changes in one frame from work B whole to the band family. Today `matter`'s opaque frame hides
this; coverage exposes it. This is the score's business rather than the instrument's: the travel's
window closes before the pass does. The composer's answers are to run the travel to the pass's end, or
to close its window where the arrival is already opaque. Row 8 should be read at this edge with the
cue's actual handles rather than at a door.

**9.3 The one-point seam carries a quarter share of the departing work.** Where an instrument's alpha
lies between 0 and 1 the colour it writes is `mix(colB, colA, cov)` rather than the arriving colour
alone, so at an alpha of 0.5 the composited result carries a quarter of work A that a correct
antialiased edge would not. The band is about one point wide, because `d` is a distance in points. It
cannot reach any measured row, since every measured row sits at a door where the alpha is 0 or 1 at
every point. Repairing it would mean writing a second colour expression for the blended case, which
would change what the same shader draws as a bottom cue, so it is left as a named artefact.

**9.4 The woven instrument has no absence to publish.** A reader taking the law to mean that every
instrument has gaps will look for gaps in the weave and find the groove terms at `:141–144`. Those are
a shading term: they reach the picture through a multiply at `:147` and never touch the alpha. Writing
them into the alpha would punch a hole at every ribbon edge, and the bottom cue would show the cleared
buffer through the holes. The honest statement for this instrument is a constant, and row 55 is what
keeps that constant from drifting into a weight.

**9.5 A cue opened away from its door pops in proportion.** Coverage makes the 1.17 s and 4.03 s
openings free only because both cues stand at `mix = 0` there, where the alpha is 0 everywhere. A
score is free to open a cue at any dial, and such a cue appears with whatever coverage that dial
gives. Coverage turns a total replacement into a partial one and does not remove it. The window-edge
reading in row 8 is what makes that visible rather than a surprise.

**9.6 The meshing field is ill-conditioned near a wheel centre.** `rA` and `rB` are floored at `1e-5`
(`:750–751`) and `grad` at `1e-5` (`:777`); where a centre stands inside the frame the gradient
collapses and `d` swings, so a coverage mask taken from it would flicker at a point. The composed
passage does not reach it: `reachFor` carries both centres well off the frame at either door, and the
score holds `size` above 0.7 for its own measured reason. A smaller pair, or a `centreX` near an edge,
brings it into reach, and this is the one place where the mask is a worse object than the colour it
feeds today.

---

## 10. What this document does not settle

**§8's placement sentence points the wrong way.** It states that an instrument declaring
`writes: false` may be drawn only as the cue nearest the eye. §6 gives the reading the host's own draw
order supports, and the composed passage is the counter-example that decides it: the woven instrument
fills the frame and stands at `stack: 0`. `PASS-API-V1.md` is read-only from this branch, so the
correction is carried here and belongs in the contract at the same time as the first instrument's
coverage lands.

**Three things need his eye, each with its number.** The arrival's contact shadow is all but gone
inside a stack — mean 0.0968 of 255 surviving against 3.6917 drawn alone — and whether the front
should carry something in its place is a question about how it reads. The step where the travel leaves
its window stands at mean 14.5592 of 255 and belongs to the score, since that window closes before the
pass does. And the travelling voice now shows nothing for the first 2.3 seconds of its own window,
which is the dial curve against `reachFor`'s placement rather than anything coverage did.

**The template question stays open.** Two of the three instruments share one construction and the
third is a constant, so this document sets no template for a fourth. An instrument arriving with a
different construction states its own coverage under §1's law and its own `coverage:{writes, how}`
block, and the four rows judge it the same way.
