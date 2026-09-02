#!/usr/bin/env python3
"""PASS-API-V1 — the return to the hang: the two ends of a passage, measured.

Run: python3 tests/test_pass_hang.py

Root: his word 2026-08-14 08:39. A passage takes the frame and gives it back, and until now nothing
guaranteed the two ends lined up. These rows measure both ends against the DOM the walk actually
hangs, rather than asserting that they agree.

WHAT IS COMPARED, AND AGAINST WHAT.

  The departure. The walk stands on the departing work. The renderer takes the frame and draws its
  first frame. Those two pictures are photographed and compared inside the project's seam threshold
  of 6 of 255 — the same bar tests/test_pass_weave.py judges a door by. A first frame that stood at
  the whole frame instead of on the work's own box would miss it by the width of the picture.

  The arrival. The renderer's last frame stands on the arriving work's hang box; the handoff then
  releases the canvas and reveals the DOM. Both are photographed and compared over the canvas's OWN
  rect — the region the renderer actually drew, which is the region a seam could show in.

  The comparison is always made on the canvas's rect rather than on the whole viewport, because
  outside it the renderer never claimed anything and the walk's own chrome is free to differ.

The score below is this file's own: one cue naming the woven instrument, every handle tracked so the
picture is a function of progress alone. It needs no lab tree, so these rows never skip for a
missing read-only source.

REAL_ROWS (added 2026-08-31, Phase 2 item 5's own verification standard). The same two doors, driven
instead by a real, planner-composed score that casts box-fold, hero and liquid — `REAL_SCORES` below,
found by the real `pass-composer.js` against the real 121-work fleet, never hand-typed. Two red-on-bug
rows follow, re-serving the same site with box-fold's or hero's own pre-repair instrument file swapped
in and re-driving the identical real bundle through a fresh browser session: a crop that fails to
cancel at a real door reddens there and nowhere else.

BOX-FOLD'S REAL-PAIR ROWS READ 37.5/255 UNTIL 2026-09-02, AND WHAT THAT ACTUALLY WAS. The reading was
diagnosed on 2026-09-01 as a CONSTANT ~3px positional offset — the stripe test pattern this fixture
serves has an exact, measurable period, and the period matched DOM to canvas exactly, ruling out a
scale or crop error and clearing cause B's own crop-cancellation channel. The offset itself was then
laid at cause F's door, box-fold being the fleet's only `cameraAuthority:"own"` instrument.

BOTH READINGS WERE ARTEFACTS OF THE PICTURE THE FIXTURE DEALS. The synthetic work is a diagonal
stripe on the rule `(x + y) % 20 < 4`, and every point of it depends on x + y ALONE — so the pattern
cannot tell a picture from its own transpose, and a reflection about the anti-diagonal reads back as
a pure shift of x + y. Re-measured on 2026-09-02 with a two-axis ramp in place of the stripe, the
frame's four corners came back (1,1), (1,0), (0,1), (0,0) against a DOM standing at (0,0), (1,0),
(0,1), (1,1): box-fold's landed face carried the work REFLECTED ABOUT ITS OWN ANTI-DIAGONAL, and only
where the composer drives `axis` at 1, the crease lying flat. The three pixels were 126 - s wrapped
into the stripe's own period of 20, exactly. Repaired in `pass-inst-boxfold.js` — the picture is
pasted onto the face by which way the crease lies, the same decision `posed`'s own `pt` already made
about the geometry — and proven by arithmetic, no image and no browser in it, in
`tests/test_pass_boxfold.py`'s own flat-door row and its red-on-bug beside it. Both doors here now
read 0.56-0.61 of 255, the same number hero and liquid give.

A LIMIT OF THIS FILE'S OWN RED-ON-BUG RIG, READ HONESTLY RATHER THAN HIDDEN. The site fixture deals
its own pair of placeholder images at random per browser session; a high-frequency image makes a
small positional error obvious in a pixel mean, a smooth one can mask the same error entirely, and —
as the paragraph above records at some cost — a symmetric one can disguise what KIND of error it is.
A run where a red-on-bug row here reads unexpectedly green is that randomness, not a claim the
underlying bug returned: `tests/test_pass_door_invariant.py`'s own red-on-bug row (arithmetic on four
numbers) and `tests/test_pass_boxfold.py`'s own flat-door red-on-bug (the doors read against their
own source files, on the bench's fixed photographs) are the deterministic proofs, and are what to
trust if this file's own red-on-bug rows ever disagree with them.
"""
import base64
import hashlib
import json
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
import engine_build as build_site  # noqa: E402
from headless import serve, Browser, chrome_available  # noqa: E402

SITE_URL = "https://synth.example.com"
VW, VH = 1000, 900
SEAM = 6.0          # the project's seam threshold, 6 of 255 (TRANSITION-STAGE-V0 §1)
DUR = 2400          # the pass this file measures, in milliseconds
# The rise and the fall this file's score names, in seconds. They are named rather than left to the
# default share so the descent onto the arriving box is a wide, unhurried window: the reframe rows
# turn the frame INSIDE that descent, which is the only stretch where the destination box is what
# the camera is actually reading. A turn during the plateau would move nothing, and a row that
# turned there could not tell a carried reframe from an uncarried one.
RISE, FALL = 0.4, 0.9
TURN_AT = 0.75      # where in the pass the reframe rows turn the frame — inside the fall
REST_TOL = 1e-6     # §6's rest tolerance, now read against the hang pose
# How much more sharply the pose may turn across a reframe than it turns in the same flight
# undisturbed. The bar is the flight's own sharpest turn, times this. A carried reframe adds no
# corner at all; a cut one adds exactly one.
JUMP_FACTOR = 3.0

# THE UNDISTURBED FLIGHT'S OWN SHARPEST TURN, in pose units per second squared, measured on this
# walk on 2026-08-14 and written down here.
#
# WHY IT IS WRITTEN DOWN RATHER THAN RE-FLOWN. Until 2026-08-14 a control flight was flown on every
# run and its reading became the denominator of both reframe rows, so the bar travelled with
# whatever that one flight happened to read. Two things made the reading swing. The turn was
# measured as a bare second difference between three samples, which grows with the SQUARE of the gap
# between them; and that gap, in headless Chrome, runs about 8 ms at its middle, reaches 50 ms when
# a frame stalls on an idle machine and passes 200 ms on a loaded one, so a single stall during the
# sharpest stretch multiplied the reading by 35 and more.
# Seven runs read the control at 0.0916, 0.0938, 0.2222, 0.2529, 0.2848, 0.3739 and 0.5956 — a
# factor of 6.5 between the smallest and the largest — and one of the seven went red at 3.12 times a
# control that had landed low. The reading now divides by the gap, so it is the second derivative of
# the pose against the pass's own clock rather than a reading of the frame rate, and the number it
# is compared against stands still.
#
# WHAT IT IS A PROPERTY OF. The pose between the two hangs is a monotone spline through four points
# this file itself fixes — the departing box, the whole frame twice, the arriving box — flown over
# the rise and fall this file's own score names, at this file's own viewport. Its sharpest turn
# belongs to that curve, so it is the same number wherever the same score is flown. What remains of
# the run-to-run spread is where the frames happen to fall around the spline's own knots, which the
# measurements below bound.
#
# THE VALUE AND ITS HEADROOM. On an unloaded machine seven undisturbed flights read this turn at
# 98.85, 103.25, 104.02, 104.64, 104.75, 106.16 and 106.42 — a band four percent wide. The number
# below is the bottom of that band, rounded down, so the bar it sets is the tightest the measurement
# supports rather than a comfortable one. Twenty runs on a loaded machine then read the orientation
# row between 97.40 and 103.81 and the resize row between 58.34 and 106.40, and all forty flights
# passed; the highest reading yet taken stands 2.8 times under the 3.0× bar of 300. Load pushes the
# reading DOWN rather than up, which is what the one-sided guard further down rests on.
#
# PROVED AGAINST THE DEFECT on 2026-08-14 by cutting the carry in reseatHang, so the reframe is cut
# instead of carried: the orientation row read 821.58 on panY at 1.848 s, the instant the frame
# turns, and the resize row 399.73 — each of them over the bar, because a step taken inside one
# frame is divided by that one frame's gap squared.
CTRL_TURN = 100.0

results = []


# ---------------------------------------------------------------- real, planner-composed scores
# ITEM 5'S OWN REAL-PAIR EVIDENCE (Phase 2, 2026-08-31). Three scores read straight off the real
# `pass-composer.js` — `composer.passageFor({workRecordA, workRecordB, routeRole, direction, seed})`
# against `joined.make(fix.consts)`, where `fix` is `tests/fixture_pass_works.json`, the same 121
# real per-work records `tests/test_pass_composed.py` measures against — searched (never hand-typed,
# never a synthetic cue) until each cast the named instrument. Found on the FIRST pair tried:
#
#   boxfold: pair 17843080526947498 / 17843153263050281, routeRole "middle", direction "a-to-b",
#            seed 0 — cast [boxfold, matter, strata-light]
#   liquid:  the same pair, routeRole "entrance", direction "a-to-b", seed 6.5
#            — cast [liquid, grid-colour]
#   hero:    pair 17843153263050281 / 17843154031050281, routeRole "entrance", direction "a-to-b",
#            seed 0.5 — cast [hero, grid-colour]
#
# RE-DERIVED 2026-09-02, AND WHY THE THREE REQUESTS MOVED. The block below was frozen on 2026-08-31
# and the composer has moved under it since: replayed today, none of the three recorded requests
# returns the score that was frozen for it, so what the rows drove was a corpus of three scores no
# route composes any more. Re-derived here off the composer as it stands, by the same search the
# note above describes — the same pair first, every route role, both directions, the seed span in
# half steps, taking the first request that casts the named instrument — with ONE criterion added
# and said out loud: a bundle of a single cue is passed over, because a one-cue score carries no
# secondary window for the seam file's own door rows to straddle and those rows would silently
# vanish rather than fail. Hero's own pair moved for exactly that reason: no multi-cue bundle of the
# original pair casts it.
#
# WHAT THE RE-DERIVATION ALSO CARRIES. Hero's frozen bundle seated hero — an instrument that fills
# the frame and publishes no `presence` — at stack 0 with a window of 0.6 s inside a 7.4 s passage,
# so for the other 6.8 s the frame stood on no floor at all and the picture cut at both of hero's
# window edges (176 of 255 over 91.6 per cent of the frame). That was a composer defect and it is
# repaired at its source (`placeTheStack` in `pass-composer.js`: the ground is the pivot, the one cue
# whose window runs the whole passage), so no bundle re-derived today can carry it.
#
# Each is the composer's own `made.json` (its Python-parity JSON writer's text, plain numbers, no
# retyping) for that request, unedited. The rows below drive each through the same real DOM, the
# same `declare`/`offer`, and the same two pins (`progressPin:0`/`clockPin:0` for the departing door,
# `progressPin:1`/`clockPin:duration` for the arriving one) row 8 and row 1 already use for the
# synthetic weave score — so a crop that fails to cancel at a real door reddens here exactly as it
# would on a real route, on a bundle nobody hand-picked to make the point.
REAL_SCORE_JSON = {
    "boxfold": r'''{"camera":{"owner":"stage","rests":"b","track":[{"at":"a","fov":null,"logScale":0,"owner":"stage","pan":{"x":0,"y":0},"pitch":0,"roll":0,"yaw":0},{"at":2.0559,"fov":null,"logScale":0.0,"owner":"stage","pan":{"x":-0.0126,"y":-0.0126},"pitch":0.0,"roll":0.0,"yaw":0.0459},{"at":3.2775,"fov":null,"logScale":0.0,"owner":"stage","pan":{"x":0.0,"y":0.0},"pitch":0.0,"roll":0.0,"yaw":0.0313},{"at":"b","fov":null,"logScale":0,"owner":"stage","pan":{"x":0,"y":0},"pitch":0,"roll":0,"yaw":0}]},"cues":[{"cameraAuthority":"own","doors":{"in":{"handle":"mix","measured":true,"value":0},"out":{"handle":"mix","measured":true,"value":1}},"id":"pivot","instrument":{"api":1,"id":"boxfold"},"levels":["WORLD","CELL"],"nodes":{"pivot-axis":{"note":"requested 1 and applied, from the banding axis cut-lines.json recorded \u2014 which way the ribbons run, which way the solid turns so its crease crosses that, and which way the picture folds onto itself so the fold line lies along it","op":"static","value":1},"pivot-course":{"in":{"source":"cueProgress"},"note":"the cue's one course, shared by every handle it drives: the room stands at 1.084 of the travel, where the two works' own tone stands 0.084 apart, placed at 0.4311 by which of them reads brighter, and passes through without a hold: this step is a subdominant and shelf 15's crest is the culmination's own suspension, so there is no tension standing here to hold","op":"spline","points":[{"at":0,"value":0},{"at":0.4311,"value":1.084},{"at":1,"value":1}]},"pivot-depth":{"from":[0,1],"in":{"node":"pivot-course"},"note":"requested [0.4217, 0.3561] and applied, from each work's own corridor reading, structure.polar.tunnel \u2014 how far the perspective runs, and how deep a room the floor stands in","op":"map","to":[0.4217,0.3561]},"pivot-dip":{"note":"requested 0.6973 and applied, from the departing work's own measured horizon, structure.horizon.y","op":"static","value":0.6973},"pivot-fingers":{"note":"requested 14 and applied, from the departing work's repeat across the crease: its frame side over structure.grid.periodPx","op":"static","value":14},"pivot-lead":{"note":"requested 0.0 and applied, from the finger count, read off its own range onto this one and turned over","op":"static","value":0},"pivot-mask":{"op":"static","value":0},"pivot-mix":{"a":0.0,"b":1.0,"note":"the pass's own progress, door to door","op":"mix","t":{"in":{"source":"cueProgress"},"name":"in","op":"curve"}},"pivot-seam":{"note":"requested 0.6172 and applied, from structure.regions.line.<axis>.at \u2014 where along the crease's own direction the departing work falls into two regions, as a share of its own frame. The handle's published span is the measurement's own search window, the middle half of the work, so the reading is placed on it in the unit it is already in","op":"static","value":0.6172},"pivot-seamScore":{"note":"requested 0.5233 and applied, from structure.regions.line.<axis>.explains \u2014 how cleanly that line divides the picture, the between-versus-within reading of the work's own columns at that place. It is handed with the instrument's own floor UNAPPLIED, so the gate stays where the gate lives","op":"static","value":0.5233},"pivot-seed":{"note":"requested 0.0 and applied, from the ordered pair's own seed","op":"static","value":0},"pivot-shade":{"op":"static","value":1},"pivot-travel":{"op":"static","value":1}},"resources":{"lean":{"bytesEstimate":2000248,"framebuffers":0,"passes":1,"pingPong":0,"programs":1,"textureSlots":2,"textures":0,"variant":"lean"},"rich":{"bytesEstimate":32000248,"framebuffers":0,"passes":1,"pingPong":0,"programs":1,"textureSlots":2,"textures":0,"variant":"rich"},"standard":{"bytesEstimate":8000248,"framebuffers":0,"passes":1,"pingPong":0,"programs":1,"textureSlots":2,"textures":0,"variant":"standard"}},"roles":["surface","mystery"],"stack":0,"tracks":{"axis":{"node":"pivot-axis"},"depth":{"node":"pivot-depth"},"dip":{"node":"pivot-dip"},"fingers":{"node":"pivot-fingers"},"lead":{"node":"pivot-lead"},"mask":{"node":"pivot-mask"},"mix":{"node":"pivot-mix"},"seam":{"node":"pivot-seam"},"seamScore":{"node":"pivot-seamScore"},"seed":{"node":"pivot-seed"},"shade":{"node":"pivot-shade"},"travel":{"node":"pivot-travel"}},"voice":"miracle","window":[0.0,7.377],"works":["a","b"]},{"cameraAuthority":"stage","doors":{"in":{"handle":"presence","measured":true,"value":0},"out":{"handle":"presence","measured":true,"value":0}},"id":"travel","instrument":{"api":1,"id":"matter"},"levels":["SURFACE","TEXTURE"],"nodes":{"travel-clock":{"note":"the second the host hands down","source":"time"},"travel-course":{"in":{"source":"cueProgress"},"note":"the cue's one course, shared by every handle it drives: the room stands at 1.084 of the travel, where the two works' own tone stands 0.084 apart, placed at 0.4311 by which of them reads brighter, and passes through without a hold: this step is a subdominant and shelf 15's crest is the culmination's own suspension, so there is no tension standing here to hold","op":"spline","points":[{"at":0,"value":0},{"at":0.4311,"value":1.084},{"at":1,"value":1}]},"travel-drift":{"note":"requested 0.0 and applied, from the fractional part of the two works' measured spectral periods in ratio is the reading, and it is deliberately not driven: a wandering fold line does not land on the work's own structural line","op":"static","value":0},"travel-gather":{"from":[0,1],"in":{"node":"travel-course"},"note":"requested [0.0119, 0.2168] and applied, from the share of the frame each work's own measured dominant object holds","op":"map","to":[0.0119,0.2168]},"travel-grain":{"from":[0,1],"in":{"in":{"source":"cueProgress"},"name":"smooth","op":"curve"},"note":"requested [0.45, 0.45] and applied, from the two works' own measured spectral periods, said in cells across the frame's height, positioned about the handle's default by their ratio","op":"map","to":[0.45,0.45]},"travel-loosen":{"in":{"from":[0,1],"in":{"node":"travel-course"},"op":"map","to":[0.7884,0.0005]},"max":1,"min":0,"note":"requested [0.7884, 0.0005] and applied, from the share of the frame each work's own measured open ground holds","op":"clamp"},"travel-mix":{"a":0.0,"b":1.0,"note":"the pass's own progress, door to door","op":"mix","t":{"in":{"source":"cueProgress"},"name":"in","op":"curve"}},"travel-presence":{"in":{"source":"cueProgress"},"note":"requested nothing at this cue's own two doors and whole across its middle, because this voice stands over another. From the entry-door contract's reserved dry: nothing at the cue's own two doors, whole across its middle, so a voice joins a running picture without replacing it and stands down the same way. The lowest voice of a stack owes the opposite and stands whole throughout, because nothing stands beneath it","op":"spline","points":[{"at":0.0,"value":0.0},{"at":0.5,"value":1.0},{"at":1.0,"value":0.0}]},"travel-seed":{"note":"requested 0.0 and applied, from the ordered pair's own seed","op":"static","value":0},"travel-shade":{"op":"static","value":1},"travel-travel":{"op":"static","value":1}},"resources":{"lean":{"bytesEstimate":2000084,"framebuffers":0,"passes":1,"pingPong":0,"programs":1,"textureSlots":2,"textures":0,"variant":"lean"},"rich":{"bytesEstimate":32000084,"framebuffers":0,"passes":1,"pingPong":0,"programs":1,"textureSlots":2,"textures":0,"variant":"rich"},"standard":{"bytesEstimate":8000084,"framebuffers":0,"passes":1,"pingPong":0,"programs":1,"textureSlots":2,"textures":0,"variant":"standard"}},"roles":["mystery","fragment"],"stack":1,"tracks":{"clock":{"node":"travel-clock"},"drift":{"node":"travel-drift"},"gather":{"node":"travel-gather"},"grain":{"node":"travel-grain"},"loosen":{"node":"travel-loosen"},"mix":{"node":"travel-mix"},"presence":{"node":"travel-presence"},"seed":{"node":"travel-seed"},"shade":{"node":"travel-shade"},"travel":{"node":"travel-travel"}},"voice":"letter","window":[2.1976,3.4192],"works":["a","b"]},{"cameraAuthority":"stage","doors":{"in":{"handle":"presence","measured":true,"value":0},"out":{"handle":"presence","measured":true,"value":0}},"id":"arrival","instrument":{"api":1,"id":"strata-light"},"levels":["LIGHT-COLOUR"],"nodes":{"arrival-clock":{"note":"the second the host hands down","source":"time"},"arrival-colourAmpA":{"note":"requested 0.394 and applied, from the departing work's own colour.sat, VOICE_SHARE of it; the same LIGHT-COLOUR ownership gate","op":"static","value":0.394},"arrival-colourAmpB":{"note":"requested 0.4017 and applied, from the arriving work's own colour.sat, VOICE_SHARE of it","op":"static","value":0.4017},"arrival-colourPeriodA":{"note":"requested 0.4788 and applied, from the departing work's own colour.sat and colour.brightness, carried through BEAT_DIAL and spread \u2014 lab/step4-assembler.js:1966-2010, ported \u2014 read only where this cue owns LIGHT-COLOUR","op":"static","value":0.4788},"arrival-colourPeriodB":{"note":"requested 1.0692 and applied, from the same of the arriving work","op":"static","value":1.0692},"arrival-colourPhaseA":{"note":"requested 0.0 and applied, from this voice's own place among the instrument's four, i/4 \u2014 step4-assembler.js:2000; the same LIGHT-COLOUR ownership gate","op":"static","value":0},"arrival-colourPhaseB":{"note":"requested 0.5 and applied, from the same rule at the arriving work's own slot","op":"static","value":0.5},"arrival-lightAmpA":{"note":"requested 0.392 and applied, from the departing work's own colour.contrast, VOICE_SHARE of it","op":"static","value":0.392},"arrival-lightAmpB":{"note":"requested 0.4143 and applied, from the arriving work's own colour.contrast, VOICE_SHARE of it","op":"static","value":0.4143},"arrival-lightPeriodA":{"note":"requested 0.6741 and applied, from the departing work's own colour.sat and colour.contrast, carried through BEAT_DIAL and spread; the same reason and the same LIGHT-COLOUR ownership gate","op":"static","value":0.6741},"arrival-lightPeriodB":{"note":"requested 1.2601 and applied, from the same of the arriving work","op":"static","value":1.2601},"arrival-lightPhaseA":{"note":"requested 0.25 and applied, from this voice's own place among the instrument's four, i/4; the same LIGHT-COLOUR ownership gate","op":"static","value":0.25},"arrival-lightPhaseB":{"note":"requested 0.75 and applied, from the same rule at the arriving work's own slot","op":"static","value":0.75},"arrival-mask":{"op":"static","value":0},"arrival-mix":{"a":0.0,"b":1.0,"note":"the pass's own progress, door to door","op":"mix","t":{"in":{"source":"cueProgress"},"name":"in","op":"curve"}},"arrival-presence":{"in":{"source":"cueProgress"},"note":"requested nothing at this cue's own two doors and whole across its middle, because this voice stands over another. From the entry-door contract's reserved dry: nothing at the cue's own two doors, whole across its middle, so a voice joins a running picture without replacing it and stands down the same way. The lowest voice of a stack owes the opposite and stands whole throughout, because nothing stands beneath it","op":"spline","points":[{"at":0.0,"value":0.0},{"at":0.5,"value":1.0},{"at":1.0,"value":0.0}]}},"resources":{"lean":{"bytesEstimate":2000088,"framebuffers":0,"passes":1,"pingPong":0,"programs":1,"textureSlots":2,"textures":0,"variant":"lean"},"rich":{"bytesEstimate":32000088,"framebuffers":0,"passes":1,"pingPong":0,"programs":1,"textureSlots":2,"textures":0,"variant":"rich"},"standard":{"bytesEstimate":8000088,"framebuffers":0,"passes":1,"pingPong":0,"programs":1,"textureSlots":2,"textures":0,"variant":"standard"}},"roles":["assembly"],"stack":2,"tracks":{"clock":{"node":"arrival-clock"},"colourAmpA":{"node":"arrival-colourAmpA"},"colourAmpB":{"node":"arrival-colourAmpB"},"colourPeriodA":{"node":"arrival-colourPeriodA"},"colourPeriodB":{"node":"arrival-colourPeriodB"},"colourPhaseA":{"node":"arrival-colourPhaseA"},"colourPhaseB":{"node":"arrival-colourPhaseB"},"lightAmpA":{"node":"arrival-lightAmpA"},"lightAmpB":{"node":"arrival-lightAmpB"},"lightPeriodA":{"node":"arrival-lightPeriodA"},"lightPeriodB":{"node":"arrival-lightPeriodB"},"lightPhaseA":{"node":"arrival-lightPhaseA"},"lightPhaseB":{"node":"arrival-lightPhaseB"},"mask":{"node":"arrival-mask"},"mix":{"node":"arrival-mix"},"presence":{"node":"arrival-presence"}},"voice":"letter","window":[3.2274,7.377],"works":["a","b"]}],"direction":"a-to-b","duration":7377,"failLand":"arrive","intent":"The work folds along its own region lines. The region division holds at 0.2979 and the flat picture folds into a solid the viewer is carried round: 6 parts of the first work hand over to 2 of the second along that cut, and the second work arrives by condensing at its own pole 0.5, 0.5. Shelves 8 the one folded space, 9 the held pivot, 7 the arrival, 17 a middle. The register is provocation: the two tonal grounds stand far apart.","interruption":{"resolve":"nearest-door","withinMs":500},"pair":{"a":"17843080526947498","b":"17843153263050281"},"provenance":{"by":null,"measuredAt":null,"source":"sceneplan-v1/17843080526947498__17843153263050281__ab"},"quality":{"lean":{"cues":{"arrival":{"resources":{"bytesEstimate":2000088,"framebuffers":0,"passes":1,"pingPong":0,"programs":1,"textureSlots":2,"textures":0,"variant":"lean"}},"pivot":{"resources":{"bytesEstimate":2000248,"framebuffers":0,"passes":1,"pingPong":0,"programs":1,"textureSlots":2,"textures":0,"variant":"lean"}},"travel":{"resources":{"bytesEstimate":2000084,"framebuffers":0,"passes":1,"pingPong":0,"programs":1,"textureSlots":2,"textures":0,"variant":"lean"}}},"renderScale":null},"rich":{"cues":{"arrival":{"resources":{"bytesEstimate":32000088,"framebuffers":0,"passes":1,"pingPong":0,"programs":1,"textureSlots":2,"textures":0,"variant":"rich"}},"pivot":{"resources":{"bytesEstimate":32000248,"framebuffers":0,"passes":1,"pingPong":0,"programs":1,"textureSlots":2,"textures":0,"variant":"rich"}},"travel":{"resources":{"bytesEstimate":32000084,"framebuffers":0,"passes":1,"pingPong":0,"programs":1,"textureSlots":2,"textures":0,"variant":"rich"}}},"renderScale":null},"standard":{"cues":{"arrival":{"resources":{"bytesEstimate":8000088,"framebuffers":0,"passes":1,"pingPong":0,"programs":1,"textureSlots":2,"textures":0,"variant":"standard"}},"pivot":{"resources":{"bytesEstimate":8000248,"framebuffers":0,"passes":1,"pingPong":0,"programs":1,"textureSlots":2,"textures":0,"variant":"standard"}},"travel":{"resources":{"bytesEstimate":8000084,"framebuffers":0,"passes":1,"pingPong":0,"programs":1,"textureSlots":2,"textures":0,"variant":"standard"}}},"renderScale":null}},"schema":2,"seed":0.0}''',
    "hero": r'''{"camera":{"owner":"stage","rests":"b","track":[{"at":"a","fov":null,"logScale":0,"owner":"stage","pan":{"x":0,"y":0},"pitch":0,"roll":0,"yaw":0},{"at":1.5777,"fov":null,"logScale":0.0,"owner":"stage","pan":{"x":0.0,"y":0.0},"pitch":0.0,"roll":0.0391,"yaw":0.0},{"at":1.6582,"fov":null,"logScale":0.0,"owner":"stage","pan":{"x":0.0,"y":0.0},"pitch":0.0,"roll":0.0318,"yaw":0.0},{"at":"b","fov":null,"logScale":0,"owner":"stage","pan":{"x":0,"y":0},"pitch":0,"roll":0,"yaw":0}]},"cues":[{"cameraAuthority":"stage","doors":{"in":{"handle":"mix","measured":true,"value":0},"out":{"handle":"mix","measured":true,"value":1}},"id":"pivot","instrument":{"api":1,"id":"hero"},"levels":["SURFACE"],"nodes":{"pivot-centreX":{"note":"requested 0.5 and applied, from the midpoint of the two measured radial centres","op":"static","value":0.5},"pivot-centreY":{"note":"requested 0.5 and applied, from the midpoint of the two measured radial centres","op":"static","value":0.5},"pivot-clock":{"note":"the second the host hands down","source":"time"},"pivot-course":{"in":{"source":"cueProgress"},"note":"the cue's one course, shared by every handle it drives: the room stands at 1.056 of the travel, where the two works' own tone stands 0.056 apart, placed at 0.5439 by which of them reads brighter, and passes through without a hold: this step is a subdominant and shelf 15's crest is the culmination's own suspension, so there is no tension standing here to hold","op":"spline","points":[{"at":0,"value":0},{"at":0.5439,"value":1.056},{"at":1,"value":1}]},"pivot-mask":{"op":"static","value":0},"pivot-mix":{"a":0.0,"b":1.0,"note":"the pass's own progress, door to door","op":"mix","t":{"in":{"source":"cueProgress"},"name":"in","op":"curve"}},"pivot-planet":{"note":"requested 0.2728 and applied, from structure.polar.planet, how strongly the pair's works read as a planet, which places the far end of the arc","op":"static","value":0.2728},"pivot-turn":{"from":[0,1],"in":{"node":"pivot-course"},"note":"requested [0.1358, 0.2348] and applied, from each work's own measured radial score, so a work whose rings are its own device drives the turn \u2014 the mesh's rotation and the spiral's wind \u2014 and one that barely reads radial barely turns and barely winds","op":"map","to":[0.1358,0.2348]}},"resources":{"lean":{"bytesEstimate":2666791,"framebuffers":0,"passes":1,"pingPong":0,"programs":1,"textureSlots":2,"textures":0,"variant":"lean"},"rich":{"bytesEstimate":42666791,"framebuffers":0,"passes":1,"pingPong":0,"programs":1,"textureSlots":2,"textures":0,"variant":"rich"},"standard":{"bytesEstimate":10666791,"framebuffers":0,"passes":1,"pingPong":0,"programs":1,"textureSlots":2,"textures":0,"variant":"standard"}},"roles":["surface","breath"],"stack":0,"tracks":{"centreX":{"node":"pivot-centreX"},"centreY":{"node":"pivot-centreY"},"clock":{"node":"pivot-clock"},"mask":{"node":"pivot-mask"},"mix":{"node":"pivot-mix"},"planet":{"node":"pivot-planet"},"turn":{"node":"pivot-turn"}},"voice":"accompaniment","window":[0.0,5.881],"works":["a","b"]},{"cameraAuthority":"stage","doors":{"in":{"handle":"presence","measured":true,"value":0},"out":{"handle":"presence","measured":true,"value":0}},"id":"travel","instrument":{"api":1,"id":"grid-colour"},"levels":["CELL"],"nodes":{"travel-angleBeatIn":{"op":"static","value":0},"travel-angleBeatOut":{"op":"static","value":1},"travel-angleFrom":{"note":"requested 166.0 and applied, from structure.ownDevice.angleDeg of the departing work, said as a position on a quarter turn; structure.grid.angleDeg where none","op":"static","value":166},"travel-angleTo":{"note":"requested 31.0 and applied, from the same of the arriving work","op":"static","value":31},"travel-arrival":{"note":"requested 0 and applied, from nothing of either photograph: charter shelf 7 names the five arrivals \u2014 the interfered one the overlay and the grid-and-colour cut carry, the crystallized one the pour's own column order carries \u2014 and a score names which of them this crossing makes, so this is a plan's word","op":"static","value":0},"travel-clock":{"note":"the second the host hands down","source":"time"},"travel-countBeatIn":{"op":"static","value":0},"travel-countBeatOut":{"op":"static","value":1},"travel-countFrom":{"note":"requested 77 and applied, from the departing work's own frame side over the step it was cut at, structure.ownDevice.stepPx, with structure.grid.periodPx where no device was derived \u2014 the count of its own lattice across the frame","op":"static","value":77},"travel-countTo":{"note":"requested 63 and applied, from the arriving work's own count, read the same way, so the cut leaves one work's structure and arrives at the other's","op":"static","value":63},"travel-kindA":{"note":"requested 2 and applied, from structure.ownDevice.kind of the departing work: rings are cut into rings, a grid into tiles, a banded work into strips, and a work whose device was never recovered is cut by its own colour, the one kind needing no lattice","op":"static","value":2},"travel-kindB":{"note":"requested 2 and applied, from the same of the arriving work","op":"static","value":2},"travel-mask":{"op":"static","value":0},"travel-mix":{"a":0.0,"b":1.0,"note":"the pass's own progress, door to door","op":"mix","t":{"in":{"source":"cueProgress"},"name":"in","op":"curve"}},"travel-presence":{"in":{"source":"cueProgress"},"note":"requested nothing at this cue's own two doors and whole across its middle, because this voice stands over another. From the entry-door contract's reserved dry: nothing at the cue's own two doors, whole across its middle, so a voice joins a running picture without replacing it and stands down the same way. The lowest voice of a stack owes the opposite and stands whole throughout, because nothing stands beneath it","op":"spline","points":[{"at":0.0,"value":0.0},{"at":0.5,"value":1.0},{"at":1.0,"value":0.0}]},"travel-shade":{"op":"static","value":1},"travel-stagger":{"note":"requested 0.7121 and applied, from the golden-angle stagger of the count the frame is actually cut into, charter shelf 13's stagger instrument, so no two pieces of the cascade leave together. The sheet's own `stagger` takes the same shelf on its region count; this one takes it on the lattice count, so the two are two readings and two rows","op":"static","value":0.7121}},"resources":{"lean":{"bytesEstimate":2000160,"framebuffers":0,"passes":1,"pingPong":0,"programs":1,"textureSlots":2,"textures":0,"variant":"lean"},"rich":{"bytesEstimate":32000160,"framebuffers":0,"passes":1,"pingPong":0,"programs":1,"textureSlots":2,"textures":0,"variant":"rich"},"standard":{"bytesEstimate":8000160,"framebuffers":0,"passes":1,"pingPong":0,"programs":1,"textureSlots":2,"textures":0,"variant":"standard"}},"roles":["mystery","fragment"],"stack":1,"tracks":{"angleBeatIn":{"node":"travel-angleBeatIn"},"angleBeatOut":{"node":"travel-angleBeatOut"},"angleFrom":{"node":"travel-angleFrom"},"angleTo":{"node":"travel-angleTo"},"arrival":{"node":"travel-arrival"},"clock":{"node":"travel-clock"},"countBeatIn":{"node":"travel-countBeatIn"},"countBeatOut":{"node":"travel-countBeatOut"},"countFrom":{"node":"travel-countFrom"},"countTo":{"node":"travel-countTo"},"kindA":{"node":"travel-kindA"},"kindB":{"node":"travel-kindB"},"mask":{"node":"travel-mask"},"mix":{"node":"travel-mix"},"presence":{"node":"travel-presence"},"shade":{"node":"travel-shade"},"stagger":{"node":"travel-stagger"}},"voice":"letter","window":[5.5517,5.6322],"works":["a","b"]}],"direction":"a-to-b","duration":5881,"failLand":"arrive","intent":"Along what the two works do not share. The tonal zones and detail scales holds at 0.944 and the ground stays while the band family travels from 0.1442 to 0.3884. One generator changes over a held family, and the second work arrives by condensing at its own pole 0.5, 0.5. Shelves 9 one generator at a time, 12 the parts that become actors, 7 the arrival, 17 a middle. The register is provocation: the two tonal grounds stand far apart.","interruption":{"resolve":"nearest-door","withinMs":500},"pair":{"a":"17843153263050281","b":"17843154031050281"},"provenance":{"by":null,"measuredAt":null,"source":"sceneplan-v1/17843153263050281__17843154031050281__ab"},"quality":{"lean":{"cues":{"pivot":{"resources":{"bytesEstimate":2666791,"framebuffers":0,"passes":1,"pingPong":0,"programs":1,"textureSlots":2,"textures":0,"variant":"lean"}},"travel":{"resources":{"bytesEstimate":2000160,"framebuffers":0,"passes":1,"pingPong":0,"programs":1,"textureSlots":2,"textures":0,"variant":"lean"}}},"renderScale":null},"rich":{"cues":{"pivot":{"resources":{"bytesEstimate":42666791,"framebuffers":0,"passes":1,"pingPong":0,"programs":1,"textureSlots":2,"textures":0,"variant":"rich"}},"travel":{"resources":{"bytesEstimate":32000160,"framebuffers":0,"passes":1,"pingPong":0,"programs":1,"textureSlots":2,"textures":0,"variant":"rich"}}},"renderScale":null},"standard":{"cues":{"pivot":{"resources":{"bytesEstimate":10666791,"framebuffers":0,"passes":1,"pingPong":0,"programs":1,"textureSlots":2,"textures":0,"variant":"standard"}},"travel":{"resources":{"bytesEstimate":8000160,"framebuffers":0,"passes":1,"pingPong":0,"programs":1,"textureSlots":2,"textures":0,"variant":"standard"}}},"renderScale":null}},"schema":2,"seed":0.5}''',
    "liquid": r'''{"camera":{"owner":"stage","rests":"b","track":[{"at":"a","fov":null,"logScale":0,"owner":"stage","pan":{"x":0,"y":0},"pitch":0,"roll":0,"yaw":0},{"at":0.7967,"fov":null,"logScale":0.0,"owner":"stage","pan":{"x":-0.0126,"y":-0.0126},"pitch":0.0,"roll":0.0,"yaw":0.0459},{"at":4.4852,"fov":null,"logScale":0.0,"owner":"stage","pan":{"x":0.0,"y":0.0},"pitch":0.0,"roll":0.0,"yaw":0.0313},{"at":"b","fov":null,"logScale":0,"owner":"stage","pan":{"x":0,"y":0},"pitch":0,"roll":0,"yaw":0}]},"cues":[{"cameraAuthority":"stage","doors":{"in":{"handle":"mix","measured":true,"value":0},"out":{"handle":"mix","measured":true,"value":1}},"id":"pivot","instrument":{"api":1,"id":"liquid"},"levels":["TEXTURE"],"nodes":{"pivot-clock":{"note":"the second the host hands down","source":"time"},"pivot-course":{"in":{"source":"cueProgress"},"note":"the cue's one course, shared by every handle it drives: the room stands at 1.084 of the travel, where the two works' own tone stands 0.084 apart, placed at 0.4311 by which of them reads brighter, and passes through without a hold: this step is a subdominant and shelf 15's crest is the culmination's own suspension, so there is no tension standing here to hold","op":"spline","points":[{"at":0,"value":0},{"at":0.4311,"value":1.084},{"at":1,"value":1}]},"pivot-crest":{"from":[0,1],"in":{"in":{"source":"cueProgress"},"name":"smooth","op":"curve"},"note":"requested [0.702, 0.702] and applied, from texture.spectralPeriodPx over the work's own frame side, read as a position on the handle's own range","op":"map","to":[0.702,0.702]},"pivot-mask":{"op":"static","value":0},"pivot-mix":{"a":0.0,"b":1.0,"note":"the pass's own progress, door to door","op":"mix","t":{"in":{"source":"cueProgress"},"name":"in","op":"curve"}},"pivot-refract":{"from":[0,1],"in":{"node":"pivot-course"},"note":"requested [0.575, 0.325] and applied, from texture.detailPx over the work's own frame side, read as a position on the handle's own range","op":"map","to":[0.575,0.325]},"pivot-seed":{"note":"requested 6.5 and applied, from the ordered pair's own seed","op":"static","value":6.5},"pivot-shade":{"op":"static","value":1},"pivot-swell":{"from":[0,1],"in":{"node":"pivot-course"},"note":"requested [0.2935, 0.0576] and applied, from texture.scoreFromCutLines, how much of the work reads as grain rather than as line","op":"map","to":[0.2935,0.0576]},"pivot-travel":{"op":"static","value":1}},"resources":{"lean":{"bytesEstimate":2666747,"framebuffers":0,"passes":1,"pingPong":0,"programs":1,"textureSlots":2,"textures":0,"variant":"lean"},"rich":{"bytesEstimate":42666747,"framebuffers":0,"passes":1,"pingPong":0,"programs":1,"textureSlots":2,"textures":0,"variant":"rich"},"standard":{"bytesEstimate":10666747,"framebuffers":0,"passes":1,"pingPong":0,"programs":1,"textureSlots":2,"textures":0,"variant":"standard"}},"roles":["surface","breath"],"stack":0,"tracks":{"clock":{"node":"pivot-clock"},"crest":{"node":"pivot-crest"},"mask":{"node":"pivot-mask"},"mix":{"node":"pivot-mix"},"refract":{"node":"pivot-refract"},"seed":{"node":"pivot-seed"},"shade":{"node":"pivot-shade"},"swell":{"node":"pivot-swell"},"travel":{"node":"pivot-travel"}},"voice":"accompaniment","window":[0.0,7.377],"works":["a","b"]},{"cameraAuthority":"stage","doors":{"in":{"handle":"presence","measured":true,"value":0},"out":{"handle":"presence","measured":true,"value":0}},"id":"arrival","instrument":{"api":1,"id":"grid-colour"},"levels":["CELL"],"nodes":{"arrival-angleBeatIn":{"op":"static","value":0},"arrival-angleBeatOut":{"op":"static","value":1},"arrival-angleFrom":{"note":"requested 0.0 and applied, from structure.ownDevice.angleDeg of the departing work, said as a position on a quarter turn; structure.grid.angleDeg where none","op":"static","value":0},"arrival-angleTo":{"note":"requested 166.0 and applied, from the same of the arriving work","op":"static","value":166},"arrival-arrival":{"note":"requested 0 and applied, from nothing of either photograph: charter shelf 7 names the five arrivals \u2014 the interfered one the overlay and the grid-and-colour cut carry, the crystallized one the pour's own column order carries \u2014 and a score names which of them this crossing makes, so this is a plan's word","op":"static","value":0},"arrival-clock":{"note":"the second the host hands down","source":"time"},"arrival-countBeatIn":{"op":"static","value":0},"arrival-countBeatOut":{"op":"static","value":1},"arrival-countFrom":{"note":"requested 11 and applied, from the departing work's own frame side over the step it was cut at, structure.ownDevice.stepPx, with structure.grid.periodPx where no device was derived \u2014 the count of its own lattice across the frame","op":"static","value":11},"arrival-countTo":{"note":"requested 77 and applied, from the arriving work's own count, read the same way, so the cut leaves one work's structure and arrives at the other's","op":"static","value":77},"arrival-kindA":{"note":"requested 2 and applied, from structure.ownDevice.kind of the departing work: rings are cut into rings, a grid into tiles, a banded work into strips, and a work whose device was never recovered is cut by its own colour, the one kind needing no lattice","op":"static","value":2},"arrival-kindB":{"note":"requested 2 and applied, from the same of the arriving work","op":"static","value":2},"arrival-mask":{"op":"static","value":0},"arrival-mix":{"a":0.0,"b":1.0,"note":"the pass's own progress, door to door","op":"mix","t":{"in":{"source":"cueProgress"},"name":"in","op":"curve"}},"arrival-presence":{"in":{"source":"cueProgress"},"note":"requested nothing at this cue's own two doors and whole across its middle, because this voice stands over another. From the entry-door contract's reserved dry: nothing at the cue's own two doors, whole across its middle, so a voice joins a running picture without replacing it and stands down the same way. The lowest voice of a stack owes the opposite and stands whole throughout, because nothing stands beneath it","op":"spline","points":[{"at":0.0,"value":0.0},{"at":0.5,"value":1.0},{"at":1.0,"value":0.0}]},"arrival-shade":{"op":"static","value":1},"arrival-stagger":{"note":"requested 0.0729 and applied, from the golden-angle stagger of the count the frame is actually cut into, charter shelf 13's stagger instrument, so no two pieces of the cascade leave together. The sheet's own `stagger` takes the same shelf on its region count; this one takes it on the lattice count, so the two are two readings and two rows","op":"static","value":0.0729}},"resources":{"lean":{"bytesEstimate":2000160,"framebuffers":0,"passes":1,"pingPong":0,"programs":1,"textureSlots":2,"textures":0,"variant":"lean"},"rich":{"bytesEstimate":32000160,"framebuffers":0,"passes":1,"pingPong":0,"programs":1,"textureSlots":2,"textures":0,"variant":"rich"},"standard":{"bytesEstimate":8000160,"framebuffers":0,"passes":1,"pingPong":0,"programs":1,"textureSlots":2,"textures":0,"variant":"standard"}},"roles":["assembly"],"stack":1,"tracks":{"angleBeatIn":{"node":"arrival-angleBeatIn"},"angleBeatOut":{"node":"arrival-angleBeatOut"},"angleFrom":{"node":"arrival-angleFrom"},"angleTo":{"node":"arrival-angleTo"},"arrival":{"node":"arrival-arrival"},"clock":{"node":"arrival-clock"},"countBeatIn":{"node":"arrival-countBeatIn"},"countBeatOut":{"node":"arrival-countBeatOut"},"countFrom":{"node":"arrival-countFrom"},"countTo":{"node":"arrival-countTo"},"kindA":{"node":"arrival-kindA"},"kindB":{"node":"arrival-kindB"},"mask":{"node":"arrival-mask"},"mix":{"node":"arrival-mix"},"presence":{"node":"arrival-presence"},"shade":{"node":"arrival-shade"},"stagger":{"node":"arrival-stagger"}},"voice":"letter","window":[2.4654,7.377],"works":["a","b"]}],"direction":"a-to-b","duration":7377,"failLand":"arrive","intent":"The two band families cross into stripes. The region division holds at 0.2979 and never moves, and the crossing is the one held ground played through: 6 parts of the first work hand over to 2 of the second along that cut, and the second work arrives by condensing at its own pole 0.5, 0.5. Shelves 9 the held pivot, 7 the arrival, 17 a quiet link. The register is provocation: the two tonal grounds stand far apart.","interruption":{"resolve":"nearest-door","withinMs":500},"pair":{"a":"17843080526947498","b":"17843153263050281"},"provenance":{"by":null,"measuredAt":null,"source":"sceneplan-v1/17843080526947498__17843153263050281__ab"},"quality":{"lean":{"cues":{"arrival":{"resources":{"bytesEstimate":2000160,"framebuffers":0,"passes":1,"pingPong":0,"programs":1,"textureSlots":2,"textures":0,"variant":"lean"}},"pivot":{"resources":{"bytesEstimate":2666747,"framebuffers":0,"passes":1,"pingPong":0,"programs":1,"textureSlots":2,"textures":0,"variant":"lean"}}},"renderScale":null},"rich":{"cues":{"arrival":{"resources":{"bytesEstimate":32000160,"framebuffers":0,"passes":1,"pingPong":0,"programs":1,"textureSlots":2,"textures":0,"variant":"rich"}},"pivot":{"resources":{"bytesEstimate":42666747,"framebuffers":0,"passes":1,"pingPong":0,"programs":1,"textureSlots":2,"textures":0,"variant":"rich"}}},"renderScale":null},"standard":{"cues":{"arrival":{"resources":{"bytesEstimate":8000160,"framebuffers":0,"passes":1,"pingPong":0,"programs":1,"textureSlots":2,"textures":0,"variant":"standard"}},"pivot":{"resources":{"bytesEstimate":10666747,"framebuffers":0,"passes":1,"pingPong":0,"programs":1,"textureSlots":2,"textures":0,"variant":"standard"}}},"renderScale":null}},"schema":2,"seed":6.5}''',
}
REAL_SCORES = {k: json.loads(v) for k, v in REAL_SCORE_JSON.items()}


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


def score(duration=DUR, rise=RISE, fall=FALL, chrome=None):
    """One cue, the woven instrument, every handle on a track. `axis` stands at 0 — the up-and-down
    weave — so the picture never turns on its own clock, and the three voices that used to drift are
    pinned, so one instant of one seed is one picture."""
    cam = {"owner": "stage", "rests": "b", "track": []}
    if rise is not None or fall is not None:
        cam["hang"] = {}
        if rise is not None:
            cam["hang"]["rise"] = rise
        if fall is not None:
            cam["hang"]["fall"] = fall
    s = {
        "schema": 2,
        "intent": "the return to the hang, measured at both of its ends",
        "pair": {"a": "a", "b": "b"},
        "seed": 3,
        "duration": duration,
        "interruption": {"withinMs": 200, "resolve": "nearest-door"},
        "failLand": "arrive",
        "camera": cam,
        "cues": [{
            "id": "hang-main",
            "instrument": {"id": "weave", "api": 1},
            "voice": "letter",
            "roles": ["disassembly", "assembly"],
            "levels": ["SURFACE", "CELL"],
            "window": [0, duration / 1000.0],
            "works": ["a", "b"],
            "cameraAuthority": "stage",
            "doors": {"in": {"handle": "mix", "value": 0, "measured": True},
                      "out": {"handle": "mix", "value": 1, "measured": True}},
            "nodes": {"prog": {"source": "progress"}, "sec": {"source": "time"},
                      "zero": {"op": "static", "value": 0}, "one": {"op": "static", "value": 1},
                      "many": {"op": "static", "value": 28}},
            "tracks": {"mix": {"node": "prog"}, "clock": {"node": "sec"},
                       "strips": {"node": "many"}, "axis": {"node": "zero"},
                       "speed": {"node": "one"}, "seed": {"node": "zero"},
                       "nMul": {"node": "one"}, "press": {"node": "one"}},
        }],
        "provenance": {"source": "tests/test_pass_hang.py", "measuredAt": "2026-08-14",
                       "by": "the return-to-the-hang rows"},
    }
    if chrome is not None:
        s["chromeReveal"] = chrome
    return s


# ---------------------------------------------------------------- bake once
build_site.SITE_CONFIG = dict(build_site.SITE_CONFIG)
build_site.SITE_CONFIG["pass"] = {"visualLayer": "pass", "diagnostics": "on"}

TMP = Path(tempfile.mkdtemp(prefix="synth_passhang_"))
build_site.OUT = TMP
build_site.build(SITE_URL)
LAYER = (TMP / "pass-layer.js").read_text(encoding="utf-8")
BUNDLE = (TMP / "exhibition.js").read_text(encoding="utf-8")

# ---------------------------------------------------------------- string rows

check("PASS-HANG the adapter measures the work's own box, never the section around it",
      "function hangGeometry(" in BUNDLE and 'querySelector("img.work")' in BUNDLE,
      "the section is a full-viewport grid cell and says nothing about where the work hangs in it")

check("PASS-HANG the geometry carries the layout's own crop, fit, radius and transform",
      all(s in BUNDLE for s in ["getComputedStyle(im)", "objectFit", "borderTopLeftRadius",
                                "crop: 1", "orientation:"]),
      "a layout that began to crop or to transform must say so here rather than blur the seam")

check("PASS-HANG one canvas plane carries the whole source between the two measured boxes",
      all(s in LAYER for s in ["function planeAt(", "rec.hangA", "rec.hangB",
                               "function planeApply(", "c.style.left", "c.style.width",
                               "c.style.borderRadius"]),
      "the carrier itself travels hang A → scene → hang B; an instrument's centre crop cannot "
      "masquerade as the work leaving the wall")

check("PASS-HANG the door is not a cloned DOM image and no opacity bridge exists",
      'document.createElement("img")' not in LAYER and "function doorBridge(" not in LAYER
      and ".style.opacity" not in LAYER,
      "the exact instrument door stays on the same WebGL carrier from first pixel to last")

check("PASS-HANG the carrier publishes the preceding scene and the normalised host pointer",
      all(s in LAYER for s in ["sceneTexture", "sceneAvailable", "function carryScene(",
                               'case "pointer"', "rec.cmd.interaction"]),
      "a later material voice can read the frame beneath it, and interaction arrives from the "
      "product without another listener")

check("PASS-HANG the flight is anchored at both hangs, with the score's track riding on it",
      "function anchorPose(" in LAYER and "function camCompose(" in LAYER,
      "a score that rests at its neutral must leave both ends exact")

check("PASS-HANG the rest is read against the arriving work's hang pose",
      "rec.hangPoseB || CAM_NEUTRAL" in LAYER and 'on: rec.hangPoseB ? "hang" : "neutral"' in LAYER,
      "§6's 1e-6 stands, now read against the hang pose; the neutral pose is its special case")

check("PASS-HANG the first frame is drawn before the canvas is shown",
      LAYER.index("playFrame(rec, 0, 0, 0, null)") < LAYER.index("stageShow(true)"),
      "showing an unpainted canvas puts one frame of its clear colour between the walk and the pass")

# Read inside `finish`'s OWN region: `handoff` appears elsewhere in the file too (the under-cover
# placement), so a whole-file index would compare two lines that have nothing to do with the
# landing. The hide and the transform-clear are read inside `stageHideAfterPresent`'s own region —
# `finish` only ever schedules that pair, it never calls either of them directly, so the door frame
# `cadenceLand` drew just before gets a real browser frame before the canvas actually goes away.
FINISH = LAYER.split("function finish(")[1].split("function settle(")[0]
HIDE_AFTER_PRESENT = LAYER.split("function stageHideAfterPresent(")[1].split("\n  }\n")[0]
check("PASS-HANG the handoff reveals the DOM before the canvas is even scheduled to release",
      'im.style.transition = "none"' in BUNDLE and "function handoff(cmd, place)" in BUNDLE
      and "hooks.handoff(rec.cmd)" in FINISH and "stageHideAfterPresent(rec.caps)" in FINISH
      and FINISH.index("hooks.handoff(rec.cmd)") < FINISH.index("stageHideAfterPresent(rec.caps)"),
      "no opacity transition, no generic fade — the DOM is revealed before the canvas's release is "
      "even scheduled")
check("PASS-HANG the canvas hides and its transform clears together, only once presented",
      "requestAnimationFrame(" in HIDE_AFTER_PRESENT
      and HIDE_AFTER_PRESENT.index("stageShow(false)") < HIDE_AFTER_PRESENT.index("camApply(null"),
      "the hide and the transform-clear stand inside the SAME deferred callback, so a browser "
      "frame is guaranteed between the door frame's draw and the hide, and the transform is still "
      "cleared only once the canvas is gone — no frame that draws neither picture")

check("PASS-HANG the chrome is revealed once, after the landing, with its parts named",
      "function chromeReveal(" in BUNDLE and BUNDLE.count("chromeReveal(cmd);") == 1
      and "passDockKeys[key]" in BUNDLE
      and all(p in BUNDLE for p in ["plaque", "counter", "share", "sound", "series", "focus"]),
      "the six named parts, and one caller — dock, which already keeps the single ledger that says "
      "whether this command has landed, so the reveal is once because the landing is once")

check("PASS-HANG a score may name the chrome's own timing",
      '"chromeReveal"' in BUNDLE and "PASS_CHROME_MS" in BUNDLE,
      "scoreable timing with a working default where the score names nothing")

# ---------------------------------------------------------------- browser rows

ROWS = [
    "PASS-HANG row 8 · the first drawn frame coincides with the DOM's A, measured pixel-wise",
    "PASS-HANG row 1 · the renderer's door B agrees with the DOM's hang B, measured pixel-wise",
    "PASS-HANG row 1 · the pass rests ON the arriving work's hang pose, not on the whole frame",
    "PASS-HANG row 2 · no blank frame is drawn across a whole passage",
    "PASS-HANG row 2 · the canvas is released at the landing and leaks no z-index",
    "PASS-HANG row 3 · the product landing happens exactly once, on every exit including failures",
    "PASS-HANG row 4 · the chrome appears after the arrival, never before",
    "PASS-HANG row 5 · focus and the accessibility tree each change exactly once",
    "PASS-HANG row 6 · audio, history, the story portion and the caption stay coherent",
    "PASS-HANG row 7 · a resize mid-passage reframes without a jump and still lands on the box",
    "PASS-HANG row 7 · an orientation change mid-passage does the same",
    "PASS-HANG row 7 · a moved destination moves the picture at no instant, and still lands exactly",
    "PASS-HANG row 51 · the hangGeometry measurement callback mutates nothing",
    "PASS-HANG row A3 · an interruption with no usable coverage door still resolves the camera onto "
    "the exact arriving hang, never freezing short of it",
    "PASS-HANG row A3 · that resolution still lands exactly once, and the handoff carries the "
    "resolved pose rather than the one the interruption caught",
]

DOOR_PRESENT_ROW = ("PASS-HANG row A3, mechanism · the cadence's door frame gets a real browser "
                     "frame before the canvas hides")

HOOKS = """window.HOOKS = function () {
  var A = window.__exPass.adapter;
  return { dock: A.dock, glide: A.glide, curtain: A.curtain, mark: A.mark,
           hangGeometry: A.hangGeometry, handoff: A.handoff };
};
window.__marks = function (name, gen) {
  return window.__exPass.report().events.filter(function (e) {
    return e.name === name && (gen === undefined || e.gen === gen); }).length;
};
0"""


def png(br, path):
    d = br._cmd("Page.captureScreenshot", format="png", captureBeyondViewport=False)
    Path(path).write_bytes(base64.b64decode(d["data"]))
    return path


def js(br, expr):
    return json.loads(br.evaluate("JSON.stringify((function(){%s})())" % expr))


def canvas_box(br):
    """The canvas's rect as it actually stands, transform and all — the region the renderer claims."""
    return js(br, "var c=document.querySelector('canvas');"
                  "if(!c) return null;"
                  "var b=c.getBoundingClientRect();"
                  "return {x:b.left, y:b.top, w:b.width, h:b.height,"
                  " iw:innerWidth, ih:innerHeight, vis:c.style.visibility,"
                  " z:getComputedStyle(c).zIndex};")


def crop_of(path, box, shot_scale, inset=2):
    """Both pictures cropped to the same region, in shot pixels. The inset drops the outermost ring
    of points: at the very edge of the canvas the renderer's own bilinear sample and the browser's
    image scaler read half a point differently, and that ring says nothing about the seating."""
    from PIL import Image
    im = Image.open(path).convert("RGB")
    s = shot_scale
    x0 = max(0, int(round(box["x"] * s)) + inset)
    y0 = max(0, int(round(box["y"] * s)) + inset)
    x1 = min(im.width, int(round((box["x"] + box["w"]) * s)) - inset)
    y1 = min(im.height, int(round((box["y"] + box["h"]) * s)) - inset)
    if x1 - x0 < 8 or y1 - y0 < 8:
        return None
    return im.crop((x0, y0, x1, y1))


def apart(a, b):
    from PIL import Image, ImageChops, ImageStat  # noqa: F401
    if a is None or b is None or a.size != b.size:
        return 255.0, 255.0
    st = ImageStat.Stat(ImageChops.difference(a, b))
    return sum(st.mean) / 3.0, max(m for _, m in st.extrema)


def region_stats(path, box, shot_scale):
    """The mean and the spread of one region — how a blank frame is told from a drawn one."""
    from PIL import ImageStat
    im = crop_of(path, box, shot_scale)
    if im is None:
        return None
    st = ImageStat.Stat(im)
    return {"mean": sum(st.mean) / 3.0, "spread": sum(st.stddev) / 3.0}


def shot_scale(br, path):
    from PIL import Image
    return Image.open(path).width / float(br.evaluate("String(innerWidth)"))


def wait_state(br, want, tries=80):
    for _ in range(tries):
        if js(br, "return window.__exPass.host.report().state;") == want:
            return True
        br.sleep(0.05)
    return False


def enter(br, base):
    if br.evaluate("String(!!document.querySelector('.exd-window'))") == "true":
        br.click(".exd-window", settle=1.4)
    for _ in range(25):
        if br.evaluate("String(document.documentElement.classList.contains('ex-walk') "
                       "&& !document.documentElement.classList.contains('ex-face'))") == "true":
            break
        br.sleep(0.2)
    br.sleep(0.4)
    br.key("ArrowDown")            # the one step that makes the client fetch pass-layer.js
    for _ in range(30):
        if br.evaluate("String(!!(window.__exPass && window.__exPass.host))") == "true":
            br.evaluate(HOOKS)
            return True
        br.sleep(0.2)
    return False


def rest_at(br, a):
    """Put the walk back on the departing work, chrome settled, nothing in flight.

    Ending whatever is in flight FIRST is the whole point of this helper. A pass still running would
    place the walk at its own arriving work the moment it reached the middle of its passage, and the
    next row would then measure a departing work that stands a viewport away from the eye — which is
    a real reading of a walk that was never put back, not a defect in what it reads.

    THE WORK'S OWN REVEAL IS IN FLIGHT TOO. Marking a frame seen starts the walk's reveal — the
    picture fades up over the ground across the reveal token's own duration — so a helper that
    returned the moment the SCROLL held handed the next row a half-faded photograph and called it
    the DOM's own picture. A row comparing the renderer's pixels against it then read the fade, at
    whatever share of it the screenshot happened to land on. So the reveal is waited out here, where
    every row that asks for a resting walk gets the wait, rather than in the one row that noticed."""
    js(br, "window.__exPass.adapter.interrupt('rest'); return null;")
    wait_state(br, "idle")
    top = 9999.0
    for _ in range(10):
        # The walk has its own snap-back guard and its own notion of which frame is resting, so a
        # scroll written once can be written back. The place is therefore READ AFTER it has had time
        # to settle, and asked for again until it holds.
        js(br, "var A=document.querySelector('.exh-frame[data-id=\"%s\"]');"
               "A.classList.add('seen');"
               "scrollTo(0, Math.round(scrollY + A.getBoundingClientRect().top"
               " + (A.getBoundingClientRect().height - innerHeight)/2)); return null;" % a)
        br.sleep(0.35)
        top = float(js(br, "return document.querySelector('.exh-frame[data-id=\"%s\"]')"
                           ".getBoundingClientRect().top;" % a))
        if abs(top) < 3:
            return rest_revealed(br, a)
    return False


def rest_revealed(br, a, tries=40, nap=0.1):
    """Wait until the resting work's own reveal has finished — the picture stands at full strength,
    not part way up its fade. Read off the computed style, so the walk's own token owns the duration
    and this waits exactly as long as that token asks for."""
    for _ in range(tries):
        op = js(br, "var I=document.querySelector('.exh-frame[data-id=\"%s\"] img.work');"
                    "return I ? Number(getComputedStyle(I).opacity) : 1;" % a)
        if op >= 0.999:
            return True
        br.sleep(nap)
    return False


def declare_and_offer(br, a, b, cause):
    # THE SCORE ARRIVES ON THE DECLARE (PASS-API §1.1). Until U27 stage 0 this suite wrote the score
    # into the settings record under `pass.scores`, keyed by ordered pair — a road the no-pair-table
    # law of 2026-08-17 19:21 retired along with the delivery pack, because a score per pair in the
    # settings file is quadratic in the collection. What a walk derives for a real pair now comes
    # out of the composer; what this suite needs is one FIXED score whose numbers it can read back,
    # so it hands the score to the declare, which is the road §1.1 has always named for a
    # programmatic caller.
    return js(br, """
      var A = document.querySelector('.exh-frame[data-id="%s"]');
      var B = document.querySelector('.exh-frame[data-id="%s"]');
      var cmd = window.__exPass.adapter.declare({fromEl:A, toEl:B, dir:1, span:100,
                                                 kind:'step', cause:'%s', velocity:0,
                                                 score: window.__hangScore || null});
      window.__cmd = cmd;
      var took = cmd ? window.__exPass.layer().offer(cmd, window.HOOKS()) : false;
      return {got: !!cmd, took: took, gen: cmd ? cmd.gen : null,
              hasScore: !!(cmd && cmd.score)};
    """ % (a, b, cause))


def real_door_check(br, A, B, real_score, tag):
    """Row 8 (the departure) and row 1 (the arrival), mirrored exactly, but driven by a real,
    planner-composed score instead of this file's own synthetic weave one. Returns
    `(depart, arrive)`, each `None` or an `(mean, worst)` pair of 255 — the same shape `apart()`
    always answers with, so a caller reads it exactly as row 8/row 1 do."""
    dur = real_score["duration"]
    br.evaluate("window.__hangScore = " + json.dumps(real_score) + "; 0")

    # ---- the departure ---------------------------------------------------------------------
    rest_at(br, A)
    br.evaluate("window.__exPass.host.configure({prepareBudgetMs:400, settleSlackMs:2000,"
                " clockPin:0, progressPin:0, fixedScale:true}); 0")
    before = png(br, SHOTS / (tag + "-depart-dom.png"))
    scale = shot_scale(br, before)
    r = declare_and_offer(br, A, B, tag + "-depart")
    running = wait_state(br, "running")
    br.sleep(0.6)
    box = canvas_box(br)
    after = png(br, SHOTS / (tag + "-depart-canvas.png"))
    depart = None
    if r["took"] and running and box and box["vis"] == "visible":
        depart = apart(crop_of(before, box, scale), crop_of(after, box, scale))
    js(br, "window.__exPass.adapter.interrupt('%s-depart-done'); return null;" % tag)
    wait_state(br, "idle")
    br.sleep(0.3)

    # ---- the arrival -------------------------------------------------------------------------
    rest_at(br, A)
    br.evaluate("window.__exPass.host.configure({prepareBudgetMs:400, settleSlackMs:4000,"
                " clockPin:%f, progressPin:1, fixedScale:true}); 0" % (dur / 1000.0))
    r = declare_and_offer(br, A, B, tag + "-arrive")
    running = wait_state(br, "running")
    br.sleep(0.8)
    box = canvas_box(br)
    canvas_shot = png(br, SHOTS / (tag + "-arrive-canvas.png"))
    js(br, "window.__exPass.adapter.handoff(window.__cmd);"
           "window.__exPass.bench.show(false); return null;")
    br.sleep(0.4)
    dom_shot = png(br, SHOTS / (tag + "-arrive-dom.png"))
    arrive = None
    if r["took"] and running and box:
        arrive = apart(crop_of(canvas_shot, box, scale), crop_of(dom_shot, box, scale))
    js(br, "window.__exPass.adapter.interrupt('%s-arrive-done'); return null;" % tag)
    wait_state(br, "idle")
    br.sleep(0.3)
    return depart, arrive


REAL_ROWS = [
    "PASS-HANG real-pair · boxfold's own real bundle: departing door agrees with the DOM's hang A",
    "PASS-HANG real-pair · boxfold's own real bundle: arriving door agrees with the DOM's hang B",
    "PASS-HANG real-pair · hero's own real bundle: departing door agrees with the DOM's hang A",
    "PASS-HANG real-pair · hero's own real bundle: arriving door agrees with the DOM's hang B",
    "PASS-HANG real-pair · liquid's own real bundle: departing door agrees with the DOM's hang A",
    "PASS-HANG real-pair · liquid's own real bundle: arriving door agrees with the DOM's hang B",
    "PASS-HANG red-on-bug · boxfold's pre-repair crop reddens this same real-pair door check",
    "PASS-HANG red-on-bug · hero's pre-repair crop reddens this same real-pair door check",
]


def git_show(relpath):
    import subprocess as _sp
    try:
        r = _sp.run(["git", "show", "HEAD:%s" % relpath], cwd=str(ROOT),
                    capture_output=True, text=True, timeout=30)
        return r.stdout if r.returncode == 0 else None
    except Exception:
        return None


if not chrome_available():
    for r in ROWS + REAL_ROWS + [DOOR_PRESENT_ROW]:
        skip(r, "Chrome not installed (pinned expected skip)")
else:
    SHOTS = Path(tempfile.mkdtemp(prefix="synth_hangshots_"))
    with serve(TMP) as base:
        with Browser(width=VW, height=VH) as br:
            br.navigate(base + "/")
            br.clear_storage()
            br.navigate(base + "/")
            br.sleep(0.8)
            armed = enter(br, base)
            WORKS = js(br, "return [].slice.call(document.querySelectorAll('.exh-frame'))"
                           ".map(function(e){return e.dataset.id;}).slice(0,2);")
            ok_pair = armed and len(WORKS) == 2 and all(WORKS)

            if not ok_pair:
                for r in ROWS + REAL_ROWS + [DOOR_PRESENT_ROW]:
                    skip(r, f"the walk never registered a host, or hung no pair: "
                            f"armed={armed} works={WORKS}")
            else:
                A, B = WORKS[0], WORKS[1]
                PAIR = A + "__" + B
                br.navigate(base + "/")
                br.sleep(0.8)
                enter(br, base)
                br.evaluate(HOOKS)
                # The one score every row below declares with, put on the page once.
                br.evaluate("window.__hangScore = " + json.dumps(score()) + "; 0")

                # ---- row 51 · the one declared exception carries its own evidence ------------
                # §1.1 fences the adapter: only the product may call it and the renderer holds no
                # reference to it. §2.6 was built with the product handing the host ONE read-only
                # hook, which the host calls at `prepare` and at `reframe`, and the contract now
                # declares that a single exception. What makes it an exception rather than a hole is
                # that the call changes nothing — so it is measured here rather than asserted.
                #
                # The command is the easiest half and the strongest: the callback is handed a work
                # id and nothing else, so it never receives a command and cannot touch one. The DOM
                # and the product's own observable state are compared across three calls.
                mut = js(br, """
                  var A = window.__exPass.adapter;
                  function store() {
                    try {
                      return Object.keys(window.localStorage).sort().map(function (k) {
                        return k + "=" + window.localStorage.getItem(k); }).join("\\u0001");
                    } catch (e) { return "unreadable"; }
                  }
                  function snap() {
                    var f = document.activeElement;
                    return {
                      dom: document.documentElement.outerHTML,
                      focus: f ? (f.tagName + "#" + (f.id || "") + "." + (f.className || "")) : null,
                      scroll: Math.round(window.scrollX) + "," + Math.round(window.scrollY),
                      title: document.title, url: location.href, store: store(),
                    };
                  }
                  var before = snap();
                  var g1 = A.hangGeometry(%r);
                  var g2 = A.hangGeometry(%r);
                  var g3 = A.hangGeometry(%r);
                  var after = snap();
                  var moved = Object.keys(before).filter(function (k) {
                    return before[k] !== after[k]; });
                  return { moved: moved, arity: A.hangGeometry.length,
                           measured: !!(g1 && g1.w > 0 && g1.h > 0 && g2 && g2.w > 0 && g2.h > 0),
                           repeats: JSON.stringify(g1) === JSON.stringify(g3),
                           domBytes: before.dom.length };
                """ % (A, B, A))
                check(ROWS[12],
                      mut["moved"] == [] and mut["arity"] == 1 and mut["measured"] is True
                      and mut["repeats"] is True,
                      "three calls of the measurement hook across a live walk, on both works. The "
                      "callback takes %d argument — a work id, never a command, so a command cannot "
                      "be touched by it. Across the calls the DOM (%d characters), the focused "
                      "element, the scroll position, the title, the address and the whole of local "
                      "storage are identical; what moved: %s. Both works measured a real box, and "
                      "one work read twice returned the same record."
                      % (mut["arity"], mut["domBytes"], mut["moved"] or "nothing"))

                # ---- row 8 · the departure ------------------------------------------------
                # The walk stands on A with its chrome up. The renderer takes the frame, held at its
                # own first instant, and the two pictures are compared over the region the renderer
                # actually drew. Nothing here is stubbed: this is the real declare, the real offer
                # and the real first frame.
                rest_at(br, A)
                br.evaluate("window.__exPass.host.configure({prepareBudgetMs:400, settleSlackMs:2000,"
                            " clockPin:0, progressPin:0, fixedScale:true}); 0")
                before = png(br, SHOTS / "depart-dom.png")
                scale = shot_scale(br, before)
                # The work's own reveal is read beside the place: a picture caught part way up its
                # fade would read as a seam that is no seam, and this row names what it stood at.
                where = js(br, "var F=document.querySelector('.exh-frame[data-id=\"%s\"]');"
                               "var I=F.querySelector('img.work');"
                               "return {scrollY: Math.round(scrollY),"
                               " aTop: Math.round(F.getBoundingClientRect().top),"
                               " revealed: I ? Number(getComputedStyle(I).opacity) : null};" % A)
                r = declare_and_offer(br, A, B, "hang-depart")
                running = wait_state(br, "running")
                br.sleep(0.6)
                box = canvas_box(br)
                read = js(br, "var h=window.__exPass.host.report().hang;"
                              "return {a: h && h.a, scrollY: Math.round(scrollY)};")
                after = png(br, SHOTS / "depart-canvas.png")
                if not (r["took"] and running and box and box["vis"] == "visible"):
                    check(ROWS[0], False,
                          f"the pass never took the frame: took={r['took']} running={running} box={box}")
                else:
                    ca, cb = crop_of(before, box, scale), crop_of(after, box, scale)
                    m, mx = apart(ca, cb)
                    check(ROWS[0], m <= SEAM,
                          f"the first drawn frame against the DOM's A over the renderer's own rect: "
                          f"mean {m:.4f} of 255 (threshold {SEAM}), worst channel {mx}; "
                          f"crops {ca and ca.size} vs {cb and cb.size} from box={box}; "
                          f"the walk stood at {where} before the offer and at {read} after it")
                js(br, "window.__exPass.adapter.interrupt('row8-done'); return null;")
                wait_state(br, "idle")
                br.sleep(0.3)

                # ---- row 1 · the arrival --------------------------------------------------
                # Held at its own last instant, the renderer stands on B's hang box. The handoff then
                # places the walk, reveals the DOM and releases the canvas; the same region is read
                # again. A seam would show here and nowhere else.
                rest_at(br, A)
                br.evaluate("window.__exPass.host.configure({prepareBudgetMs:400, settleSlackMs:4000,"
                            " clockPin:%f, progressPin:1, fixedScale:true}); 0" % (DUR / 1000.0))
                r = declare_and_offer(br, A, B, "hang-arrive")
                running = wait_state(br, "running")
                br.sleep(0.8)
                box = canvas_box(br)
                canvas_shot = png(br, SHOTS / "arrive-canvas.png")
                rep = js(br, "return window.__exPass.host.report();")
                # the handoff itself: the DOM revealed, the canvas released, inside one task
                js(br, "window.__exPass.adapter.handoff(window.__cmd);"
                       "window.__exPass.bench.show(false); return null;")
                br.sleep(0.4)
                dom_shot = png(br, SHOTS / "arrive-dom.png")
                if not (r["took"] and running and box):
                    check(ROWS[1], False, f"the pass never took the frame: took={r['took']} running={running}")
                else:
                    m, mx = apart(crop_of(canvas_shot, box, scale), crop_of(dom_shot, box, scale))
                    check(ROWS[1], m <= SEAM,
                          f"the renderer's door B against the DOM's hang B over the renderer's own "
                          f"rect: mean {m:.4f} of 255 (threshold {SEAM}), worst channel {mx}")
                hang = rep.get("hang") or {}
                poseB, camera = hang.get("poseB"), (rep.get("camera") or {}).get("pose")
                near = (poseB and camera
                        and max(abs((camera.get(k) or 0) - (poseB.get(k) or 0))
                                for k in ("panX", "panY", "logScale")) <= REST_TOL)
                check(ROWS[2],
                      bool(poseB) and bool(hang.get("b")) and near,
                      f"the box the pass arrived on: {hang.get('b')}; the pose it asks for: {poseB}; "
                      f"the pose actually applied: {camera}")
                js(br, "window.__exPass.adapter.interrupt('row1-done'); return null;")
                wait_state(br, "idle")
                br.sleep(0.3)

                # ---- row 2 · no blank frame, and no canvas left behind ---------------------
                # A whole passage at its own pace, sampled as fast as the harness can photograph. A
                # blank frame is the canvas's own clear colour standing where a picture should be:
                # nearly uniform, and nearly black. Every frame photographed must carry a picture.
                #
                # THE ROW JUDGES THE FRAMES IT SAW, NEVER HOW MANY IT SAW. It used to ask for three
                # of them, and three was the machine's number rather than the product's: a
                # screenshot costs far more on a machine running several suites at once, while the
                # passage's own duration does not stretch to match, so the same build was
                # photographed eight times when the machine was quiet and twice when it was busy —
                # and the row read that difference as a defect in the renderer. A count raced
                # against a clock is not a measurement. What the row is about — that no frame the
                # canvas showed was the clear colour — holds on two frames exactly as it holds on
                # eight. A run that caught no frame at all measured nothing and says so by name,
                # rather than passing on an empty hand.
                rest_at(br, A)
                br.evaluate("window.__exPass.host.configure({prepareBudgetMs:400, settleSlackMs:2000,"
                            " clockPin:null, progressPin:null, fixedScale:true}); 0")
                r = declare_and_offer(br, A, B, "hang-frames")
                samples, blanks = [], []
                for _ in range(14):
                    st = js(br, "return {state: window.__exPass.host.report().state,"
                                " box: (function(){var c=document.querySelector('canvas');"
                                " if(!c||c.style.visibility!=='visible') return null;"
                                " var b=c.getBoundingClientRect();"
                                " return {x:b.left,y:b.top,w:b.width,h:b.height};})()};")
                    if st["box"]:
                        p = png(br, SHOTS / ("frame-%02d.png" % len(samples)))
                        s = region_stats(p, st["box"], scale)
                        if s:
                            samples.append(s)
                            # the clear colour is #08080a: nearly black and perfectly flat
                            if s["mean"] < 12.0 and s["spread"] < 3.0:
                                blanks.append(s)
                    if st["state"] == "idle":
                        break
                wait_state(br, "idle")
                br.sleep(0.4)
                if not samples:
                    skip(ROWS[3],
                         "this run photographed no frame of the pass at all — the canvas never "
                         "stood while the harness was looking, so there is nothing to read; the "
                         "row measures the frames it catches and refuses to answer on none")
                else:
                    check(ROWS[3], not blanks,
                          f"{len(samples)} frames caught across the pass, none of them the clear "
                          f"colour" if not blanks else
                          f"{len(samples)} frames caught across the pass, {len(blanks)} of them "
                          f"blank — {blanks[:1]}")
                left = canvas_box(br)
                curtained = br.evaluate("String(document.body.classList.contains('ex-pass-curtain'))")
                check(ROWS[4],
                      bool(left) and left["vis"] == "hidden" and curtained == "false",
                      f"after the landing the canvas is {left and left['vis']} at z-index "
                      f"{left and left['z']}, and the curtain class is {curtained}")

                # ---- row 3 · one landing per command, on every exit ------------------------
                # Four exits, four commands: the pass that runs its course, one cut short by a
                # product surface, one whose renderer fails, and one whose renderer never calls back
                # at all. Each must land exactly one dock and reveal the chrome exactly once.
                exits = {}
                for name, drive in (
                        ("settle", None),
                        ("interrupt", "window.__exPass.adapter.interrupt('row3-cut');"),
                        ("fail", "window.__exPass.host.fail(window.__cmd.gen, 'row3-fail');"),
                        ("watchdog", None)):
                    rest_at(br, A)
                    if name == "watchdog":
                        br.evaluate("window.__exPass.host.configure({prepareBudgetMs:400,"
                                    " settleSlackMs:20, clockPin:0, progressPin:0}); 0")
                    else:
                        br.evaluate("window.__exPass.host.configure({prepareBudgetMs:400,"
                                    " settleSlackMs:2000, clockPin:null, progressPin:null}); 0")
                    got = declare_and_offer(br, A, B, "hang-exit-" + name)
                    if drive:
                        br.sleep(0.5)
                        br.evaluate(drive + " 0")
                    wait_state(br, "idle")
                    br.sleep(0.6)
                    exits[name] = js(br, "var g=window.__cmd.gen;"
                                         "return {gen:g, docks:window.__marks('dock',g),"
                                         " chrome:window.__marks('chrome',g),"
                                         " handoffs:window.__marks('handoff',g),"
                                         " took:%s};" % ("true" if got["took"] else "false"))
                bad = {k: v for k, v in exits.items() if not (v["docks"] == 1 and v["chrome"] == 1)}
                check(ROWS[5], not bad, f"per exit: {exits}")

                # ---- row 4 · the chrome comes after the arrival ----------------------------
                # Read WHILE the pass is running, then again after it lands. The order is read off
                # the lifecycle marks rather than from the clock, so a fast machine cannot make it
                # look right by accident.
                rest_at(br, A)
                br.evaluate("window.__exPass.host.configure({prepareBudgetMs:400, settleSlackMs:4000,"
                            " clockPin:0, progressPin:0}); 0")
                declare_and_offer(br, A, B, "hang-chrome")
                wait_state(br, "running")
                br.sleep(0.5)
                during = js(br, "var g=window.__cmd.gen;"
                                "return {chrome: window.__marks('chrome',g),"
                                " dock: window.__marks('dock',g),"
                                " state: window.__exPass.host.report().state};")
                br.evaluate("window.__exPass.host.configure({progressPin:null, clockPin:null}); 0")
                js(br, "window.__exPass.adapter.interrupt('row4-land'); return null;")
                wait_state(br, "idle")
                br.sleep(0.6)
                order = js(br, """
                  var g = window.__cmd.gen;
                  var evs = window.__exPass.report().events.filter(function(e){return e.gen===g;});
                  var at = function (n) {
                    for (var i=0;i<evs.length;i++) if (evs[i].name===n) return i;
                    return -1; };
                  return {handoff: at('handoff'), dock: at('dock'), chrome: at('chrome'),
                          parts: evs.filter(function(e){return e.name.indexOf('chrome-')===0;})
                                    .map(function(e){return e.name;}),
                          names: evs.map(function(e){return e.name;})};
                """)
                check(ROWS[6],
                      during["chrome"] == 0 and during["state"] == "running"
                      and order["handoff"] >= 0 and order["dock"] > order["handoff"]
                      and order["chrome"] > order["dock"] and len(order["parts"]) == 6,
                      f"while running the chrome had fired {during['chrome']} times; after landing "
                      f"the order is handoff@{order['handoff']} → dock@{order['dock']} → "
                      f"chrome@{order['chrome']}, parts={order['parts']}")

                # ---- row 5 · focus and the accessibility tree, once each -------------------
                rest_at(br, A)
                br.evaluate("""
                  window.__watch = {focus: 0, aria: 0};
                  document.addEventListener('focusin', function () { window.__watch.focus++; }, true);
                  window.__mo = new MutationObserver(function (recs) {
                    recs.forEach(function (m) {
                      if (m.attributeName === 'aria-hidden') window.__watch.aria++; }); });
                  window.__mo.observe(document.getElementById('ex-stage'), {attributes: true});
                  document.body.focus(); 0""")
                br.evaluate("window.__exPass.host.configure({prepareBudgetMs:400, settleSlackMs:2000,"
                            " clockPin:null, progressPin:null}); 0")
                declare_and_offer(br, A, B, "hang-focus")
                wait_state(br, "idle")
                br.sleep(0.8)
                w = js(br, "window.__mo.disconnect();"
                           "return {focus: window.__watch.focus, aria: window.__watch.aria,"
                           " on: document.activeElement ? document.activeElement.dataset.id : null,"
                           " inert: !!document.getElementById('ex-stage').inert};")
                check(ROWS[7],
                      w["focus"] == 1 and w["aria"] == 2 and w["on"] == B and w["inert"] is False,
                      f"focus moved {w['focus']} time(s) and rests on {w['on']} (the arriving work "
                      f"is {B}); the stage's aria-hidden changed {w['aria']} times — once on, once "
                      f"off; inert now {w['inert']}")

                # ---- row 6 · what a passage owns none of ----------------------------------
                rest_at(br, A)
                start = js(br, """
                  var snd = document.getElementById('ex-sound');
                  var au = document.querySelector('audio');
                  return {history: history.length, hash: location.hash,
                          sound: snd ? snd.className : null,
                          playing: au ? !au.paused : null,
                          told: (document.querySelector('.exh-capzone .told')||{}).textContent || ''};
                """)
                declare_and_offer(br, A, B, "hang-coherent")
                wait_state(br, "idle")
                br.sleep(0.9)
                end = js(br, """
                  var snd = document.getElementById('ex-sound');
                  var au = document.querySelector('audio');
                  var cap = document.querySelector('.exh-capzone');
                  return {history: history.length, hash: location.hash,
                          sound: snd ? snd.className : null,
                          playing: au ? !au.paused : null,
                          share: (document.querySelector('.ex-share')||{dataset:{}}).dataset.share,
                          place: (function () {
                            // the remembered place carries the bundle's own namespace, so the key is
                            // found rather than spelled out here
                            for (var i = 0; i < sessionStorage.length; i++) {
                              var k = sessionStorage.key(i);
                              if (k.indexOf('place') < 0) continue;
                              try { return JSON.parse(sessionStorage.getItem(k)).id; } catch (e) {}
                            }
                            return null; })(),
                          title: cap ? (cap.querySelector('.title')||{}).textContent : null,
                          shown: cap ? cap.classList.contains('show') : false};
                """)
                check(ROWS[8],
                      end["history"] == start["history"] and end["hash"] == start["hash"]
                      and end["sound"] == start["sound"] and end["playing"] == start["playing"]
                      and end["share"] == B and end["place"] == B and end["shown"] is True
                      and bool(end["title"]),
                      f"history {start['history']}→{end['history']}, hash {start['hash']!r}→"
                      f"{end['hash']!r}, sound {start['sound']!r}→{end['sound']!r}, playing "
                      f"{start['playing']}→{end['playing']}; the caption stands on {end['share']} "
                      f"({end['title']!r}) and the remembered place is {end['place']}")

                # ---- row 7 · the viewport and orientation matrix ---------------------------
                # A real turn of the frame, mid-passage, on the walk's own resize road. The applied
                # pose is sampled every step; the largest step across the change is the jump, and
                # the landing must still stand on the box the new layout hangs.
                def one_flight(turn=None):
                    """One whole pass, with the applied pose sampled throughout. `turn` gives the
                    frame's new size, applied a quarter of the way in on the walk's own resize road.
                    Returns the largest step the pose took between two samples, and how it landed."""
                    rest_at(br, A)
                    br.evaluate("window.__exPass.host.configure({prepareBudgetMs:400,"
                                " settleSlackMs:4000, clockPin:null, progressPin:null,"
                                " fixedScale:true}); 0")
                    # Only poses belonging to the transaction in flight are sampled. The diagnostic
                    # surface keeps the LAST run's camera readable after it has gone, so a sampler
                    # that took whatever it found would count the step from the previous landing to
                    # this pass's first frame as a jump — a jump between two transactions, which is
                    # no jump at all.
                    # SAMPLED EVERY ANIMATION FRAME, from inside the page. A sampler driven from
                    # outside returns every thirty or forty milliseconds, and a pose that stepped
                    # once within a single frame would be spread across that whole gap and read as
                    # ordinary travel. One sample a frame is what makes a step visible as a step.
                    #
                    # EACH SAMPLE CARRIES THE SECOND THE RENDERER DREW IT AT. The pose and the
                    # `clock` handle are written by one call of the renderer's own frame, so the two
                    # are read together here and the series below stands on the pass's own clock
                    # instead of on the sampler's. That clock is what the turn is measured against,
                    # and it is also how a sample that read a frame already seen is recognised: the
                    # sampler and the renderer hold separate animation-frame callbacks, so the
                    # sampler can run twice over one drawn frame.
                    br.evaluate("""
                      window.__poses = [];
                      (function tick() {
                        window.__raf = requestAnimationFrame(tick);
                        var r = window.__exPass.host.report();
                        if (r.active && r.state === 'running' && r.camera && r.camera.pose) {
                          window.__poses.push({gen: r.gen, pose: r.camera.pose,
                                               sec: r.handles ? r.handles.clock : null});
                        }
                      })(); 0""")
                    got = declare_and_offer(br, A, B, "hang-reframe")
                    wait_state(br, "running")
                    br.sleep(DUR * TURN_AT / 1000.0)
                    if turn:
                        br._cmd("Emulation.setDeviceMetricsOverride", width=turn[0], height=turn[1],
                                deviceScaleFactor=1, mobile=False)
                        br.sleep(0.35)
                    landed = wait_state(br, "idle", tries=160)
                    br.sleep(0.5)
                    out = js(br, """
                      cancelAnimationFrame(window.__raf);
                      var r = window.__exPass.host.report();
                      var gen = window.__cmd.gen;
                      var p = window.__poses.filter(function (s) {
                        return s.gen === gen && typeof s.sec === 'number'; });
                      // ONE SAMPLE PER DRAWN FRAME. A second already seen is a second read of one
                      // frame, and a repeated pose would read as a stop followed by a step.
                      var q = [];
                      for (var i = 0; i < p.length; i++) {
                        if (!q.length || p[i].sec > q[q.length - 1].sec) q.push(p[i]);
                      }
                      // HOW SHARPLY THE POSE TURNS, in pose units per second squared — the second
                      // derivative of the pose against the pass's own clock, taken on the uneven
                      // grid the frames actually landed on.
                      //
                      // The rise and the fall are real motion, and fast motion, so the plain step
                      // between two frames is large by nature and says nothing about continuity: a
                      // reframe's own step hides inside it. A STEP, though, is a corner, and a
                      // corner shows in the second derivative while smooth travel does not, however
                      // fast that travel is. This is what tells a reframe carried across from a
                      // reframe cut.
                      //
                      // DIVIDING BY THE GAP IS WHAT MAKES THE READING A PROPERTY OF THE FLIGHT. A
                      // bare second difference between three samples grows with the square of the
                      // gap between them, so the same smooth curve read at a 33 ms gap reads four
                      // times what it reads at 16 ms, and the frame rate here swings by that much
                      // within one run. Divided, it is the curve's own turn: the same number at any
                      // frame rate. It also sharpens the corner a cut reframe leaves, because a
                      // step taken inside one frame is divided by that one frame's gap squared.
                      var worst = 0, at = null, key = null, gaps = [];
                      for (var i = 2; i < q.length; i++) {
                        var h1 = q[i-1].sec - q[i-2].sec, h2 = q[i].sec - q[i-1].sec;
                        gaps.push(h2);
                        if (!(h1 > 0 && h2 > 0)) continue;
                        ['panX','panY','logScale'].forEach(function (k) {
                          var a = q[i-2].pose[k]||0, b = q[i-1].pose[k]||0, c = q[i].pose[k]||0;
                          var d = Math.abs(2 * ((c - b) / h2 - (b - a) / h1) / (h1 + h2));
                          if (d > worst) { worst = d; at = q[i].sec; key = k; } }); }
                      gaps.sort(function (a, b) { return a - b; });
                      // A flight too short to hold three frames leaves no turn to report. The two
                      // stand-ins keep the row's own line printable, and the frame count below is
                      // what the row reds on in that case.
                      return {worst: worst, at: at === null ? -1 : at,
                              key: key === null ? "none" : key, n: q.length, read: p.length,
                              gap: {min: gaps.length ? gaps[0] : 0,
                                    mid: gaps.length ? gaps[Math.floor(gaps.length / 2)] : 0,
                                    max: gaps.length ? gaps[gaps.length - 1] : 0},
                              rest: r.rest,
                              hang: r.hang, events: r.events.filter(function (e) {
                                return e.name === 'reframe-hang'; }).length};
                    """)
                    if turn:
                        br._cmd("Emulation.setDeviceMetricsOverride", width=VW, height=VH,
                                deviceScaleFactor=1, mobile=False)
                        br.sleep(0.4)
                    out["took"] = bool(got["took"])
                    out["landed"] = landed
                    return out

                # THE CONTROL, now the witness of the written-down number rather than the bar itself.
                # The rise and the fall are real motion — the pose travels the whole way from the
                # departing box to the whole frame inside a fifth of the pass — so a bare number
                # would say nothing about continuity. The undisturbed flight is what the reframed
                # ones are read against: a reframe that put a step into the flight shows as a turn
                # beyond the one the flight already takes.
                #
                # The flight is still flown, and its reading still printed, because a number written
                # into a test goes stale the day the walk's geometry or this file's score changes,
                # and a stale one nobody reads would let both rows pass on the wrong bar.
                #
                # THE GUARD IS ONE-SIDED, and this is the reason. The turn is a maximum over the
                # frames of one flight, taken where the spline's own knots are, so a flight sampled
                # coarsely reads the knot across a wider window and comes in BELOW the true turn: on
                # a loaded machine, where a frame can take 200 ms, forty runs read the control
                # between 54.68 and 106.98. A low reading is a reading of the load. A reading above
                # the written-down number is what no sampling can produce, so that is the side the
                # guard watches, and a bar gone stale upwards is also the only direction in which a
                # stale bar would be too generous.
                CTRL_BAND = 2.0
                control = one_flight(None)
                CTRL = control["worst"]
                ctrl_fresh = CTRL <= CTRL_TURN * CTRL_BAND

                def reframe_case(row, w2, h2):
                    out = one_flight((w2, h2))
                    rest = out.get("rest") or {}
                    hangb = (out.get("hang") or {}).get("b") or {}
                    # the destination was recalculated against the NEW frame, and the pass landed on
                    # it: the box the walk hangs in is centred in the frame that now stands
                    centred = abs(hangb.get("x", -999) + hangb.get("w", 0) / 2.0 - w2 / 2.0) <= 2
                    # the rise and the fall the score named are the ones the flight actually flew
                    edge = (out.get("hang") or {}).get("edge") or {}
                    scored_edges = (abs(edge.get("rise", -1) - RISE) < 1e-9
                                    and abs(edge.get("fall", -1) - FALL) < 1e-9)
                    g = out["gap"]
                    # HOW MANY FRAMES THE FLIGHT DREW IS THE MACHINE'S NUMBER, NOT THE PRODUCT'S.
                    # The paragraph above the control already says why — a frame can take 200 ms on
                    # a loaded machine — and that is exactly why the turn guard was made one-sided.
                    # The row then asked for five frames anyway, which put the same load back in as
                    # a verdict by another door: a flight the machine drew four times is not a
                    # product that turned too sharply. Three frames is what a second derivative
                    # needs to exist at all, so below three there is no turn to read and the row
                    # says so by name; at three or more it judges the turn, one-sided as before,
                    # and the frame count stays in the line as an observation.
                    if out["n"] < 3:
                        skip(row,
                             f"this run drew {out['n']} distinct frame(s) of the flight "
                             f"({out['read']} reads) — fewer than the three a second derivative "
                             f"stands on, so the flight carries no turn to read. How many frames a "
                             f"flight draws is decided by the machine, so the reading is left "
                             f"unmade rather than answered")
                        return
                    check(row,
                          scored_edges and ctrl_fresh and
                          out["took"] and out["landed"] and out["events"] >= 1
                          and out["worst"] <= CTRL_TURN * JUMP_FACTOR and rest.get("rested") is True
                          and rest.get("on") == "hang" and centred,
                          f"{out['n']} frames sampled ({out['read']} reads), {out['events']} "
                          f"reframe(s) recorded; the sharpest the pose turned was "
                          f"{out['worst']:.3f} units per second squared, on {out['key']} at "
                          f"{out['at']:.3f} s, against the written-down {CTRL_TURN} (bar "
                          f"{JUMP_FACTOR}×, so {CTRL_TURN * JUMP_FACTOR:.1f}); the undisturbed "
                          f"flight read {CTRL:.3f} this run, under the {CTRL_BAND}× staleness "
                          f"ceiling: {ctrl_fresh}; the gaps between frames ran "
                          f"{g['min'] * 1000:.1f}/{g['mid'] * 1000:.1f}/{g['max'] * 1000:.1f} ms "
                          f"(least, middle, most); it rested {rest.get('off')} from the "
                          f"{rest.get('on')} pose (tolerance {rest.get('tol')}) on the box "
                          f"{hangb}, centred in the new frame: {centred}; the score's own rise and "
                          f"fall were flown: {edge}")

                reframe_case(ROWS[9], 760, 900)      # a plain resize: the frame narrows
                reframe_case(ROWS[10], 900, 760)     # an orientation change: the frame turns

                # THE RESEAT, ISOLATED. The two rows above turn a real frame on a real walk, and on
                # a walk that hangs its works small and centred the destination's pose hardly moves
                # when the frame changes — the step a cut reframe would leave is a quarter of what
                # the flight is travelling anyway, and no sampler can pick it out of that. Here the
                # two boxes are stated and far apart, and the real reseat runs between them: the
                # picture must not move at the instant the destination does, and the flight must
                # still land on the box that now stands.
                r = js(br, """
                  var s = %s;
                  var box = function (x, y, w, h) {
                    return {workId:'b', x:x, y:y, w:w, h:h, fit:'fill', crop:1, radius:2,
                            transform:null, dpr:1, orientation:'landscape'}; };
                  var got = window.__exPass.bench.hangReseat(
                    s, %d,
                    box(468, 418, 64, 64),        // where the departing work hangs
                    box(468, 418, 64, 64),        // where the arriving work hung
                    box(60, 700, 420, 300),       // and where it hangs after the frame changed
                    %f);
                  var worst = 0;
                  ['panX','panY','logScale'].forEach(function (k) {
                    var d = Math.abs((got.after[k]||0) - (got.before[k]||0));
                    if (d > worst) worst = d; });
                  var landed = 0;
                  ['panX','panY','logScale'].forEach(function (k) {
                    var d = Math.abs((got.end[k]||0) - (got.wants[k]||0));
                    if (d > landed) landed = d; });
                  return {moved: worst, landed: landed, carry: got.carry,
                          before: got.before, after: got.after, end: got.end, wants: got.wants};
                """ % (json.dumps(score()), DUR, DUR * TURN_AT / 1000.0))
                check(ROWS[11],
                      r["moved"] <= REST_TOL and r["landed"] <= REST_TOL,
                      f"at the instant the destination moved, the picture moved {r['moved']:.9f} "
                      f"(tolerance {REST_TOL}); by the end it stood {r['landed']:.9f} from the box "
                      f"that now hangs. The carry the reseat took up: {r['carry']}")

                # ---- row A3 · an interruption with no usable coverage door -------------------------
                # `landingDoorOf` (pass-layer.js) answers null for a cue whose `doors` names no pair
                # of handles — a real, lawful score (the coverage door is the CUE's own opt-in, never
                # a requirement any score must carry). Before this наряд, `cadenceStart` froze the
                # passage's own clock at wherever the interruption caught it whenever that door came
                # back null, which is a bug in the CAMERA's own resolution and not in the cue's: the
                # camera's target is the arriving work's measured hang box, read straight off the DOM
                # and owed independently of whether the cue happens to name a coverage door at all.
                # This score is the SAME fixture `score()` builds, less the one field that makes the
                # door resolvable, so the only thing that changed between the two is the exact defect
                # this row exists to catch.
                nodoor = score()
                del nodoor["cues"][0]["doors"]
                rest_at(br, A)
                br.evaluate("window.__exPass.host.configure({prepareBudgetMs:400,"
                            " settleSlackMs:4000, clockPin:null, progressPin:null,"
                            " fixedScale:true}); 0")
                br.evaluate("window.__hangScoreSaved = window.__hangScore;"
                            "window.__hangScore = " + json.dumps(nodoor) + "; 0")
                got = declare_and_offer(br, A, B, "hang-nodoor")
                running = wait_state(br, "running")
                # Cut it well inside the flight — a third of the way through DUR — so a camera that
                # only ever froze in place is caught nowhere near the arriving hang.
                br.sleep(DUR * 0.35 / 1000.0)
                # THE CADENCE'S DEADLINE TIMER IS A REAL-TIME `setTimeout`, INDEPENDENT OF THE FRAME
                # LOOP: `cadenceEnd` runs either when the envelope reaches its own end (a frame,
                # where `rec.lastSeconds` is already the fully-advanced target) or when this timer
                # fires first (the score's own 200ms `interruption.withinMs`, on whatever
                # `rec.lastSeconds` the last natural frame left behind). Found this наряд: this exact
                # row flaked once under the full parallel suite's own real load — off by 0.0031
                # against the 1e-6 tolerance, the deadline road landing short because `cadenceStart`
                # left its own final-frame `seconds` field undefined for a no-door cue (fixed
                # alongside, in `cadenceStart`: that field now marches to the passage's true end the
                # same way `toSeconds` already did). A busy CI machine reproduces the deadline road by
                # its own real load; this row does not manufacture a synthetic stand-in for that load.
                #
                # THE SAME LANDING, WATCHED FOR A DIFFERENT DEFECT (mechanism row, below): this
                # interruption is the one real, no-held-command road that both (a) starts a real
                # landing cadence (the camera is nowhere near the hang, exactly what this row was
                # built to force) and (b) actually hides the canvas at the end — unlike a fold/swipe,
                # which hands the canvas straight to the command that superseded it and never hides
                # it at all. `cadenceLand` (inside `finish`) draws the cadence's last frame — the one
                # standing ON the door — then in the same synchronous call used to hide the canvas
                # right there; a browser only composites what a task leaves standing at its end, so
                # that draw was skipped outright. Watched here by counting real
                # `requestAnimationFrame` ticks between the `cadence-end` log row (the door frame's
                # own draw) and the instant the canvas actually goes hidden. No threshold, no
                # magnitude — a hide at the same tick as the draw is the bug; any later tick is fixed.
                js(br, """
                  window.__rafTicks = 0;
                  var _raf = window.requestAnimationFrame;
                  window.requestAnimationFrame = function (cb) {
                    return _raf.call(window, function (t) { window.__rafTicks++; return cb(t); });
                  };
                  window.__doorTick = null;
                  var _push = Array.prototype.push;
                  Array.prototype.push = function (row) {
                    if (row && row.name === "cadence-end" && window.__doorTick === null) {
                      window.__doorTick = window.__rafTicks;
                    }
                    return _push.apply(this, arguments);
                  };
                  window.__hideTick = null;
                  window.__mo = new MutationObserver(function () {
                    var c = document.querySelector("canvas");
                    if (c && getComputedStyle(c).visibility === "hidden"
                        && window.__hideTick === null) {
                      window.__hideTick = window.__rafTicks;
                    }
                  });
                  window.__mo.observe(document.body, {attributes: true,
                                                       attributeFilter: ["style"],
                                                       subtree: true, childList: true});
                  return null;
                """)
                js(br, "window.__exPass.adapter.interrupt('a3-nodoor'); return null;")
                landed = wait_state(br, "idle", tries=200)
                br.sleep(0.2)
                rep = js(br, "return window.__exPass.host.report();")
                br.evaluate("window.__hangScore = window.__hangScoreSaved; 0")
                hang = rep.get("hang") or {}
                rest = rep.get("rest") or {}
                poseB, camera = hang.get("poseB"), (rep.get("camera") or {}).get("pose")
                near = bool(poseB) and bool(camera) and max(
                    abs((camera.get(k) or 0) - (poseB.get(k) or 0))
                    for k in ("panX", "panY", "logScale")) <= REST_TOL
                if not (got["took"] and running and landed):
                    check(ROWS[13], False,
                          f"the interruption never reached a landing to measure: "
                          f"took={got['took']} running={running} landed={landed}")
                    check(ROWS[14], False, "no landing to measure — see the row above")
                    skip(DOOR_PRESENT_ROW, "no landing to measure — see the row above")
                else:
                    check(ROWS[13],
                          rest.get("rested") is True and rest.get("on") == "hang" and near,
                          f"a cue with no coverage door, interrupted a third of the way in: "
                          f"rest={rest}, the pose it was asked to rest on: {poseB}, the pose "
                          f"actually applied: {camera}")
                    # ---- row A3, second half · one landing, and the resolved pose survives it ------
                    # The same measurement `finish` computes is read back after the handoff — the
                    # renderer's own state is idle, the canvas released — so this proves the gate
                    # actually held the handoff back rather than only correcting a number nobody
                    # then acted on.
                    left = canvas_box(br)
                    check(ROWS[14],
                          rep.get("state") == "idle" and bool(left)
                          and left.get("vis") == "hidden"
                          and "camera-not-rested" not in [e.get("name") for e in
                                                          (rep.get("events") or [])[-6:]],
                          f"state={rep.get('state')} canvas={left} last events="
                          f"{[e.get('name') for e in (rep.get('events') or [])[-6:]]}")
                    mech = js(br, "return {doorTick: window.__doorTick,"
                                  " hideTick: window.__hideTick};")
                    check(DOOR_PRESENT_ROW,
                          mech.get("doorTick") is not None and mech.get("hideTick") is not None
                          and mech["hideTick"] > mech["doorTick"],
                          f"door tick {mech.get('doorTick')}, hide tick {mech.get('hideTick')} — a "
                          f"hide at the same tick as the draw means the browser never composited "
                          f"the door frame at all: the last thing the visitor saw was whatever the "
                          f"previous, still-in-flight frame had drawn")

                # ---- REAL_ROWS · a real, planner-composed pair casting box-fold, hero and liquid --
                # Phase 2 item 5's own verification standard: the same door check row 8/row 1 give
                # the synthetic weave score, given instead to a bundle nobody hand-picked (see
                # REAL_SCORES above). This is the SAME site and the SAME browser session, so it costs
                # nothing beyond three more passages driven through the rig already open.
                REAL_RESULTS = {}
                for _name, _r8, _r1 in (("boxfold", 0, 1), ("hero", 2, 3), ("liquid", 4, 5)):
                    _depart, _arrive = real_door_check(br, A, B, REAL_SCORES[_name], "real-" + _name)
                    REAL_RESULTS[_name] = (_depart, _arrive)
                    check(REAL_ROWS[_r8],
                          _depart is not None and _depart[0] <= SEAM,
                          f"{_name}'s own real bundle, departing door against the DOM's hang A: "
                          f"{'mean %.4f of 255 (threshold %s), worst channel %s' % (_depart[0], SEAM, _depart[1]) if _depart else 'the pass never took the frame'}")
                    check(REAL_ROWS[_r1],
                          _arrive is not None and _arrive[0] <= SEAM,
                          f"{_name}'s own real bundle, arriving door against the DOM's hang B: "
                          f"{'mean %.4f of 255 (threshold %s), worst channel %s' % (_arrive[0], SEAM, _arrive[1]) if _arrive else 'the pass never took the frame'}")

shutil.rmtree(TMP, ignore_errors=True)

# ---------------------------------------------------------------- red-on-bug, box-fold and hero
# THE SAME REAL BUNDLES, AGAINST THE PRE-REPAIR INSTRUMENT FILES. A fresh copy of the already-built
# site, with exactly one instrument file swapped for the bytes this branch's own parent commit
# shipped (`git show HEAD:...` — never a second guess at what the bug looked like), served and
# driven through the identical `real_door_check` rig in a fresh browser session. If the row above
# reads green on the repaired files and this one reads red on the bytes it replaced, the row is
# proof of the repair; if it stayed green here too, it would be proving nothing.
if not chrome_available():
    for r in REAL_ROWS[6:]:
        skip(r, "Chrome not installed (pinned expected skip)")
elif "REAL_RESULTS" not in dir() or not ok_pair:
    for r in REAL_ROWS[6:]:
        skip(r, "the main run never reached a hung pair to compare against")
else:
    for _iid, _row, _instfile in (("boxfold", REAL_ROWS[6], "pass-inst-boxfold.js"),
                                  ("hero", REAL_ROWS[7], "pass-inst-hero.js")):
        _pre = git_show("engine/assets/" + _instfile)
        if _pre is None:
            skip(_row, "could not read this branch's own parent commit for the pre-repair bytes")
            continue
        _bugdir = Path(tempfile.mkdtemp(prefix="synth_hangbug_"))
        try:
            build_site.OUT = _bugdir
            build_site.build(SITE_URL)
            (_bugdir / _instfile).write_text(_pre, encoding="utf-8")
            _cfg = json.loads((_bugdir / "config.json").read_text(encoding="utf-8"))
            _cfg["pass"]["instruments"][_iid]["digest"] = hashlib.sha256(
                _pre.encode("utf-8")).hexdigest()
            (_bugdir / "config.json").write_text(json.dumps(_cfg), encoding="utf-8")
            with serve(_bugdir) as _bugbase:
                with Browser(width=VW, height=VH) as _br2:
                    _br2.navigate(_bugbase + "/")
                    _br2.clear_storage()
                    _br2.navigate(_bugbase + "/")
                    _br2.sleep(0.8)
                    _armed = enter(_br2, _bugbase)
                    _works2 = js(_br2, "return [].slice.call(document.querySelectorAll('.exh-frame'))"
                                       ".map(function(e){return e.dataset.id;}).slice(0,2);")
                    if not (_armed and len(_works2) == 2 and all(_works2)):
                        skip(_row, f"the bug site never registered a host, or hung no pair: "
                                  f"armed={_armed} works={_works2}")
                    else:
                        _A2, _B2 = _works2[0], _works2[1]
                        _br2.navigate(_bugbase + "/")
                        _br2.sleep(0.8)
                        enter(_br2, _bugbase)
                        _br2.evaluate(HOOKS)
                        _bd, _ba = real_door_check(_br2, _A2, _B2, REAL_SCORES[_iid],
                                                   "bug-real-" + _iid)
                        _worst = max((_bd[0] if _bd else 255.0), (_ba[0] if _ba else 255.0))
                        check(_row, _worst > SEAM,
                              f"pre-repair {_iid}: departing door {_bd}, arriving door {_ba} — the "
                              f"worse of the two stands {_worst:.4f} of 255 against the same "
                              f"{SEAM} threshold the repaired file passes at "
                              f"{REAL_RESULTS.get(_iid)}")
        finally:
            shutil.rmtree(_bugdir, ignore_errors=True)

# ---------------------------------------------------------------- TEST_MATRIX.md PASS-08, shelf 3
#
# Nothing new is measured here. The three "row 7" rows above already prove EX-PASS-DOOR's live
# re-measure law — a resize, an orientation change and a moved destination mid-pass all reframe the
# arriving hang with no jump (PASS-API-V1.md §2.6, conformance rows 38-44). This row names shelf 3
# (Enfilade) explicitly and reads its verdict off those three by name, so TEST_MATRIX.md's PASS-08
# can cite a real row instead of an implicit one.
_shelf3_witnesses = [n for n in ROWS if n.startswith("PASS-HANG row 7")]
_shelf3_seen = {n: s for n, s, _ in results if n in _shelf3_witnesses}
if len(_shelf3_seen) < len(_shelf3_witnesses):
    check("PASS-08 (EX-PASS-DOOR, shelf 3 — Enfilade) · resize, orientation and a moved destination "
          "mid-pass all reframe the arriving hang with no jump", False,
          "one or more of the witness rows above never ran")
elif all(s == "SKIP" for s in _shelf3_seen.values()):
    _why = next((d for n, s, d in results if n in _shelf3_witnesses and s == "SKIP"), "")
    skip("PASS-08 (EX-PASS-DOOR, shelf 3 — Enfilade) · resize, orientation and a moved destination "
         "mid-pass all reframe the arriving hang with no jump", "witness rows skipped: " + _why)
else:
    _ok = all(s == "PASS" for s in _shelf3_seen.values())
    check("PASS-08 (EX-PASS-DOOR, shelf 3 — Enfilade) · resize, orientation and a moved destination "
          "mid-pass all reframe the arriving hang with no jump", _ok,
          "" if _ok else
          ("witness rows: " + ", ".join(n + "=" + s for n, s in _shelf3_seen.items())))

passed = sum(1 for _, s, _ in results if s == "PASS")
failed = sum(1 for _, s, _ in results if s == "FAIL")
skipped = sum(1 for _, s, _ in results if s == "SKIP")
print()
for name, status, detail in results:
    line = f"{status}  {name}"
    if detail:
        line += f"   — {detail}"
    print(line)
print(f"\n{passed} passed / {failed} failed / {skipped} skipped")
sys.exit(1 if failed else 0)
