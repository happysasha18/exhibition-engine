# U26 — the panels instrument: «unfold» carried onto the host's frame

Run 2026-08-17, 17:25–19:10 local. The owner's word of 17:06 asked for more spectacle at speed, and
the composer's own census named where the spectacle is being refused: 1 296 declined pairs say
`pivot needs an instrument that cuts on panels, for region_dissolve and object_reveal`, the largest
single want in the collection after the missing stack ground, and a further 866 travelling axes are
dropped for the same reason (`lab/data/sceneplans/index.json`, `declinesByReason` and
`travelDeclineCensus`). This unit ports `lab/effects/unfold.js` into a WebGL instrument the host can
play, registered by the contract.

## The trees

Engine: `/Users/sashaabramovich/exhibition-engine-unfold`, a worktree of
`/Users/sashaabramovich/exhibition-engine-pass-api-v1`, branch `pass-api-v1-unfold`, cut from
integration head `3665da0`. One commit stands on it:

    HEAD     The panels instrument arrives: «unfold» plays on the host's frame, the first port whose
             module carried no shader — the instrument, its suite, its bench, its two byte fences,
             the three fleet-counting rows read per instrument, and this record

Nothing was merged, pushed or deployed. The site trees were read and never written:
`/Users/sashaabramovich/tlvphotos/lab/effects/unfold.js` is the module this port was read from,
`/Users/sashaabramovich/tlvphotos/lab/photos/` holds the two photographs the bench stands on, and
`/Users/sashaabramovich/tlvphotos-immersive/lab/data/` holds the census, the module contract and the
arsenal verdicts quoted below. The composer side is untouched by design: the plans that need panels
begin composing when the seat merges this branch and the composer re-runs its census.

## 1 — the thing this port had to answer first

Every instrument landed before this one — `weave`, `matter`, `gears`, `adrift` — came from a lab
module that already held its own WebGL context and its own fragment shader, so the port carried a
shader across and the two roads of the comparison ran one sampler through one rasteriser.

`unfold` holds none. It draws with CSS 3D: a stage with a perspective, a sheet cut into four hinged
panels, seven faces, four gradient shades and three gradient creases, and the browser's own
compositor is what projects them. Read that way it was unregistrable — §7 supplies a manifest with
passes and uniforms and nothing else, and `manifestWhyNo` refuses a manifest with no pass by name
("declares no pass"). The brief asked either for lawful passes and uniforms or for a precise record
of why there could be none.

**The shape it was given.** A CSS 3D transform chain is affine in a panel's own two coordinates and
the perspective divides exactly once, so the map from a point of a panel to a point of the frame is a
HOMOGRAPHY — and a homography is invertible. The shader therefore reads the chain backwards. For one
point of the frame it solves, for each panel, the two-by-two system

    (bu.x + s.x·bu.z/d)·u + (bv.x + s.x·bv.z/d)·v = s.x·(1 − a.z/d) − a.x
    (bu.y + s.y·bu.z/d)·u + (bv.y + s.y·bv.z/d)·v = s.y·(1 − a.z/d) − a.y

where `a` is the panel's own origin and `bu`, `bv` its two edges after the sheet's lean and growth,
`d` is the perspective distance and `s` the frame point measured from the mount's centre
(`engine/assets/pass-inst-unfold.js`, `lands`). It keeps the panels the point actually lands on and
takes the one nearest the eye, then lays the sheet's backing and the standing panel over them in the
order the module builds them in. The arithmetic of the chain is the module's own, term for term; only
its direction is reversed.

The result is one pass, twelve uniforms bound by name, two source-texture slots, no framebuffer and
no extra texture — the same allocation the three leanest landed instruments declare.

**Where the sheet's own size is known.** The module cover-fits the file over the mount and cuts the
sheet into quarters, so the sheet is exactly the seating the host already computes and hands down as
`fitA`/`fitB`. The shader recovers the sheet's width and height from that seating and the frame's own
two numbers, and every measurement written in the module's units — one point, two points, the mount's
width and height — is written in the same units against `resolution`. That is why the growth law, the
corner's own foreshortening and the viewing distance stand in the shader rather than in `values()`:
they read the frame's size, and a pose function cannot.

## 2 — a one-work module played as a crossing, and the one number that is the port's own

`lab/data/module-contract.json` records `unfold` as `needsTwoWorks: false`, and the module takes one
picture. A cue of this engine carries two works and two doors, so the port had to say where the second
work enters. It enters at the one instant the module's own construction offers: the far door of the
fold, where the sheet stands closed and the frame holds a single flat quarter of the file at exactly
the framing the whole work stood at. Both works reach that instant as one flat full-frame picture, so
the exchange between them is a dissolve of two flat pictures and nothing is folded while it happens.

The hand therefore runs in three parts. The first work folds shut over the first forty-six
hundredths; the two works exchange across the eight hundredths in the middle, on the closed sheet;
the second work opens out over the last forty-six. The module's own response curve runs once over
each half, so equal movements of the hand are equal felt change on both sides of the exchange, which
is what the curve exists for.

`HOLD = 0.08` is the width of that rest and is the ONLY number in this file the module did not
measure. It is said to be the port's own in the source, and a row holds it to that: the string `HOLD`
appears nowhere in the lab module. At the engine's own 6.5 s pass it is half a second of held
photograph.

Everything else is carried digit for digit and a row weighs each of them against the module's own
text: `MAXA = 84`, `EDGE = 1.16`, `PULL = 1.8`, `PERSP_FLAT = 4.4`, `PERSP_DEEP = 2.6`, `HOME = 80`,
`MIRROR = 14`, the shades' opening weights of `.28` and `.30`, the crease's `.85`, the four shade
laws, the backing's own fade, the gate `4·fold·(1 − fold)` and the sway's three terms. The response
curve is the module's twenty-one-mark table, matched number for number, half the change standing at
0.5086.

## 3 — what the manifest declares

    id "unfold", api 1, arity 2
    roles     ["disassembly", "mystery", "assembly"]
    levels    ["CELL", "CELL CONTENT"]
    handles   mix, clock, tilt, shade, depth, stagger, panels, mask     — eight
    doors     in  { mix 0, work a }      out { mix 1, work b }
    framings  { "0": { coverCrop: 1 }, "1": { coverCrop: 1 } }
    coverage  { writes: false, … }
    passes    one, twelve uniforms, all bound by declared name
    resources 0 textures, 2 texture slots, 0 framebuffers, 1 programme, 1 pass, at three tiers
    provenance lab/effects/unfold.js at 4c7dfe4, sha256 28688b86…

**The levels, and the reading is said to be derived.** CELL is carried from the module's own row in
`lab/data/module-contract.json` (`"level": "CELL"`) rather than re-decided. CELL CONTENT is read off
the construction: each panel shows its own quarter of the work while it lies flat and the mirror of
the closing quarter once it has turned, and at the far door the whole frame is one quarter standing
alone — a named region's content changing inside the region. The census records CELL CONTENT as the
one level no landed instrument publishes. SURFACE is not claimed: what covers the frame here is the
works' own pictures cut and carried, and claiming it would put this voice on the level all three
landed instruments already hold, where the levels law allows a single owner.

**The coverage, and the placement it buys.** `writes: false`, and it is a decision rather than a
default. The growth law grows the sheet by exactly what each turning panel gives up, so the standing
picture covers the frame at every point of the travel and no transparency is ever drawn. Under the
placement rule (§8 as amended 2026-08-14 14:05, and the host's own `coverageWhyNo`) that makes this
instrument lawful as the LOWEST cue of a stack and as a whole one-cue score. The census counts 1 320
plans declined for having no such ground — `weave` is the only instrument that could stand there
before this one — so the same port answers that want as well as the panel want.

**Both doors take no crop.** The module's repair of 2026-08-13 made the sheet the file COVER-fitted
and put the room the lean needs on a gate that stands at nothing at either end, so a door is the file
with no crop and no upscale to lose sharpness in. `framings` publishes 1 at both ends, where `weave`
publishes 1.29, `gears` its own and `adrift` 1.17.

## 4 — the numbers

Measured on the phone frame the project measures on, 390 × 844 at a device ratio of one, with the
clock held at 7.0 s. Bench: `tests/fixture_pass_unfold.html`, captures in
`tests/captures/pass-unfold/`.

**The doors, against their own files.** The threshold is the project's seam of 6.0 of 255.

| door | against | mean of 255 | worst channel |
|---|---|---|---|
| 0 | `towers.jpg`, cover-fitted, no crop | **1.4714** | 45 |
| 1 | `glassgrid.jpg`, cover-fitted, no crop | **0.2613** | 9 |

And each door is far from the other work: 67.4642 and 67.2061 of 255, against a bar of 40.

For the reading this replaces: `lab/data/arsenal-verdicts.json` still carries the module's
pre-repair verdict — `doorA 10.83`, `doorB 42.46`, `fill 0.2715`, `clean false`, against a door bar of
6.0. Those are the numbers the module's own header names as repaired on 2026-08-13. This port's doors
are 1.4714 and 0.2613, and its frame is filled at every sampled pose, so that row on the site side is
stale rather than contradicted; it is left for its owner.

**The closed sheet, against the single photograph.**

| pose | against | mean of 255 | worst channel |
|---|---|---|---|
| hand 0.46 | the top-left quarter of `towers.jpg`, cover-fitted | **0.1085** | 10 |
| hand 0.54 | the top-left quarter of `glassgrid.jpg`, cover-fitted | **1.0139** | 40 |

**The exchange.** At the middle of the hand the frame stands **0.6784** of 255 from the two quarters
averaged, 28.3264 from the first alone and 28.3405 from the second. The sheet has stood shut since
0.46 and stays shut until 0.54, so the whole exchange happens on one flat picture.

**Frame agreement against the lab module.** Two roads of one frame, the port's own `values()`
answering the raw fold and that same raw fold handed to the module through its own `rawFold` seam, so
both stand at ONE fold rather than at two readings of one dial.

| pose | raw fold | mean of 255 | worst channel |
|---|---|---|---|
| door 0 | 0.0000 | 0.6772 | 16 |
| hand 0.46, the closed sheet | 1.0000 | 0.6367 | 67 |
| hand 0.54, the closed sheet | 1.0000 | 1.0068 | 18 |
| door 1 | 0.0000 | 1.2215 | 30 |
| hand 0.20 | 0.4724 | 4.0035 | 130 |
| hand 0.32 | 0.6566 | 3.1790 | 121 |
| hand 0.68 | 0.6566 | 1.2452 | 80 |
| hand 0.80 | 0.4724 | 1.4344 | 37 |

**The bars, and why one of them is this port's own.** At the four poses where the sheet stands square
the port meets the project's OWN two-roads bar of 1.5 of 255 and takes no bar of its own. Through the
fold it sets one: **5.0**, the worst reading of 4.0035 plus about a quarter, measured 2026-08-17.

What that number is made of is stated. The lab road here is the browser's compositor: it downscales
the file with its own filter, antialiases seven panel edges and rasterises seven gradients, and this
shader draws each edge at one point with no coverage of its own. The worst single channel through the
fold, 130, lies along those edges. That is what puts the reading above the 0.0000 the last port
reached, and this is the first port whose two roads run different samplers.

What makes the bar mean something is the red-on-bug set: one broken rule moves the same number to
51.9694, ten times the bar.

**The frame is covered.** The port publishes a panel map on its `mask` handle — which panel stands at
each point of the frame, and where in it, as colour — leaving black exactly where no panel stands. It
is black at **0.0000%** of the frame at all eight poses. That is the growth law measured on the
picture rather than argued.

**The placement.** The host reads `coverage.writes` as `false` and places by it. Laid lowest with a
coverage-writing voice above, `coverageWhyNo` returns null and the host takes the score. Laid over a
floor that is itself lawful, it is refused by name: `cue «ground» stands over another cue and its
instrument «unfold» fills the frame whole — everything beneath it would be drawn and never seen`.

**The doors inside that stack.** Played as the ground with `matter` standing over it, each end of the
pass belongs to the voice that declared it, and both are whole.

| door | what stands there | against | mean of 255 | worst channel |
|---|---|---|---|---|
| 0 | this instrument, through a voice carrying no matter at all | `towers.jpg`, no crop | **1.4714** | 45 |
| 1 | the arriving voice, opaque on its own framing | `glassgrid.jpg` at that voice's crop of 1.17 | **0.0920** | 1 |

The crop is read off the arriving voice's own manifest at run time rather than written into the row,
so what is compared is the door that voice publishes.

**The rest.** A seeded run repeats to the pixel (mean 0.0, worst channel 0) — the module's own
fifteen-second breath and its two pointer listeners are gone, and the one place time reaches the
picture reads the `clock` handle. Ten runs leave textures, programmes and framebuffers where they
started. One canvas, one context, two source textures, one pass a frame, the drawing buffer
unpreserved. The census grants exactly what the manifest declares and overruns nothing. Every handle
reaches the picture: tilt 15.09, shade 6.18, depth 27.97, stagger 83.37 and the panel count 80.96 of
255, against the seam of 6.

## 5 — the four red-on-bug proofs

Each reverts one rule this port states, in the artifact the browser actually loads, and reads the
number that moved. The served file is changed and the record is re-stamped with the digest of the
bytes served, which is what the build does; the file on disk is never touched, so no working tree can
be left changed by a proof.

| the rule reverted | reading with it standing | reading with it broken |
|---|---|---|
| the growth law: the sheet is grown until what still stands covers the frame | 0.0000% of the frame unclaimed | **2.73%** bare |
| the corner's own foreshortening: a turned panel is counted for what it covers on the screen | 0.0000% unclaimed at the eye's nearest with both pairs turning | **0.2060%** bare |
| the mirror is taken on over the first fourteen degrees of turn | door 0 at 1.4714 of 255 from its own file | **55.9023** |
| the sheet is the seating the host hands down | the two roads at 3.1790 of 255 through the fold | **51.9694** |

The third of these reproduces the module's own recorded defect. Before the repair of 2026-08-13 every
panel carried the same region and door 0 stood a picture REBUILT from the top-left quarter; the
arsenal read 10.83 and 42.46 of 255 against a bar of 6.0. Taking the mirror on at once puts the port
back in that state and the door reads 55.9023.

The second is the module's own comment made measurable: counting the plain cosine at the far corner
"opened a triangle of bare frame in that corner (measured 0.9653 of the frame filled, with the eye at
its nearest and both pairs turning together)". Read at exactly those settings — `depth` at 1 and
`stagger` at nothing — the port with the correction removed leaves 0.2060% of the frame bare and with
it standing leaves none.

## 6 — the byte fences, set from measurement

| fence | file | measured | set at | note |
|---|---|---|---|---|
| `tests/test_pass_pack.py` | `pass-inst-unfold.js`, served bytes | 15 082 B | 16 600 B | measurement plus about a tenth, 2026-08-17 |
| `tests/test_budget.py` | the same file, gzipped | 4 754 B | 5 250 B | measurement plus about a tenth, 2026-08-17 |

Both notes name what the bytes are: the inverse of a CSS 3D transform chain — a two-by-two solve per
panel across four panels and the sheet's own plane, with each panel's shade and crease — which is
what puts this file between `weave` (4 069 B gzipped) and `adrift` (5 444 B). It is fetched by the
host, after the host, and only on a visit whose own score names it.

## 7 — what changed on this branch

    engine/assets/pass-inst-unfold.js      new — the instrument
    tests/test_pass_unfold.py              new — its suite: 42 rows, 4 of them red-on-bug proofs,
                                           all 42 green on 2026-08-17
    tests/fixture_pass_unfold.html         new — the bench that stands both roads at one pose
    tests/run_all.py                       one line: the suite joins the runner's list
    tests/test_pass_pack.py                one row and its dated note: the served-byte fence
    tests/test_budget.py                   one row and its dated note: the gzipped fence
    tests/test_pass_stack.py               one row, read per instrument (see below)
    tests/test_pass_coverage.py            two rows, read per instrument (see below)
    docs/design/evidence/2026-08-17-unfold-port.md   this record

**The three rows that counted a fleet of three.** `PASS-STACK the ground fills the frame and the
voices above it write coverage` and its two partners in the coverage suite asserted
`PACK.count("gl_FragColor = vec4(col, 1.0)") == 1` and `== 2` for the masked ones — occurrence counts
over the whole pack, taken when three instruments shipped. They stayed right through `adrift`, whose
alpha is neither literal, and they go red the moment a second frame-filling instrument lands. What
the law actually says is a PAIRING: an instrument declaring `writes: false` writes the constant 1, and
one declaring `writes: true` writes an alpha its own shader computed. The three rows now read that
pairing off each instrument's own file and name every instrument on both sides, so the next port moves
no count. Each carries a dated note saying why it moved.

**The consumer suites, re-run on this branch.** `site` 54/54, `pass` 28/28, `pass_api` 28/28,
`pass_pack` 25/25, `pass_weave` 49/49, `pass_matter` 29/29, `pass_gears` 39/39, `pass_adrift` 40/40,
`pass_reader` 27/27, `pass_drivers` 20/20, `pass_hang` 22/22, `pass_stack` 23/23 and `pass_coverage`
18/18 after the three rows above were repaired, `budget` 10/10, and `pass_unfold` 42/42.

## 8 — what waits on the delivery seat

**The merge, and then the census.** The composer casts an instrument from a table of its own, and the
manifest is read only for what an instrument can be driven by: `lab/build-sceneplan-v1.py` carries `CAST_IDS = ("weave", "matter", "gears")` at line 353,
`INSTRUMENT_CUTS` at 357 with a row per instrument saying what it is cast for, and
`INSTRUMENT_OF_KIND` at 601 where `"panel"` stands at `None` — that `None` is the literal that emits
all 1 296 declines. Those three lines are the composer side this unit deliberately did not touch. The
seat schedules the change and the re-run; the second-order effect worth knowing before it does is
that freeing `panel` also frees the 866 travelling axes counted under the same want, and that this
instrument's `writes: false` makes it a lawful stack ground, which is the other 1 320.

**The stale arsenal row.** `lab/data/arsenal-verdicts.json` still holds the module's pre-repair
verdict (`doorA 10.83`, `doorB 42.46`, `fill 0.2715`, `clean false`). The module was repaired on
2026-08-13 and this port measures 1.4714, 0.2613 and a frame filled at every pose. The row is on the
site side and is left for its owner.

**The two-roads bar.** 5.0 of 255 through the fold is this port's own number, set from measurement on
one bench with one pair on 2026-08-17. It is the first bar in this family that is a difference of
samplers rather than of mathematics, and it is stated here so a later reading can move it with its
own measurement rather than inherit it silently.
