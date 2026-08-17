#!/usr/bin/env python3
"""The byte-budget fence — the delivery-separability guard (INV-30).

The input-modality axis ships inside the single assembled bundle the build already produces: every
visitor loads every pole's code (finger, pointer, keyboard) whatever their platform. That monolithic
delivery is the chosen one — a split by platform or a per-pole lazy load would cost real complexity
against the one-page architecture for a slim saving. The SPEC says a byte-budget watcher guards the
choice: it reds once the bundle grows past its fence, and only then does a platform-split or lazy-load
delivery earn its build. This suite IS that watcher — it measures the SHIPPED bundle and reds on bloat.

What it measures: the gzip size (level 6 — plain `gzip -c`, deterministic mtime) of the engine's
assembled `exhibition.js` and `exhibition.css` AS SHIPPED. The bake comment-strips BOTH on the way
out (build.py: strip_js_comments / strip_css_comments — the visitor gets code and rules, not prose),
so each is measured through its own stripper. Measuring the engine's own assets, treated exactly as
the bake treats them, guards both repos' delivery.

The fence is infrastructure rather than red-first behaviour: it is GREEN while the bundle stays under
the fence and reds only when a future change balloons it past the headroom. The fence is set at the
current measured size plus ~10-15% headroom, rounded up — enough that ordinary growth does not flake it,
tight enough that a real jump (a whole new feature's worth of code, a heavy dependency) trips it and
sends the delivery question back to the SPEC's non-goal.

Moved 2026-08-13, with its reason, because the fence did its job. The transition seam (EX-PASS) took
the bundle from ≈60_100 B to ≈65_334 B and tripped the 65_000 B fence. The delivery question the
fence exists to raise was ANSWERED rather than waved through: the drawing layer now ships as its own
file, `pass-layer.js`, fetched by the client only when the visualLayer setting asks for it, the
device reports WebGL2, and the visit runs neither reduced motion nor Save-Data. What stays in the
bundle is the CONTRACT — the settings register, the one transition command, the landing owner and the
door that decides whether to fetch anything at all — which cannot live outside it, since it is what
makes the decision. So the JS fence tracks the new baseline at 67_000 B (about 2.5% headroom,
deliberately tight), and the separately delivered file gets a fence of its own from day one.

Measured 2026-07-21: JS gzip ≈ 92_967 B (raw). CSS as-shipped 2026-07-23: gzip ≈ 7_415 B
(comment-stripped; the commented source is ≈ 18_801 B — comments were ~60% of the served weight).
JS as-shipped 2026-07-27: gzip ≈ 57_311 B (comment-stripped; the commented source is ≈ 104_495 B —
line-opening comments were ~45% of the served weight). The raw fence had 50 B of headroom left when
the strip landed, which is what sent the same lever the stylesheet already rides over to the script.

Run: python tests/test_budget.py   (exit 0 = under fence)
"""
import gzip
import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# The source of truth is the engine's assembled bundle. In the engine repo it sits under
# ROOT/engine/assets; in the site repo it lives in the sibling engine checkout. Resolve either.
_CANDIDATES = [ROOT / "engine" / "assets", Path.home() / "exhibition-engine" / "engine" / "assets"]
ASSETS = next((c for c in _CANDIDATES if (c / "exhibition.js").exists()), _CANDIDATES[0])

# Both served assets are comment-stripped at bake — the visitor downloads code and rules, not prose.
# The fence must measure THOSE shipped artifacts, so it borrows the very strippers the build uses (one
# home for each transform, no drift). build.py sits one level up from the engine's assets dir.
def _load_strip():
    spec = importlib.util.spec_from_file_location("_engine_build", ASSETS.parent / "build.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.strip_css_comments, mod.strip_js_comments


strip_css_comments, strip_js_comments = _load_strip()

# fence value + one-line reason, per asset. current × ~1.1–1.15, rounded to a round number above it.
# The transform is the exact bake-time treatment of the served asset (None = shipped verbatim).
FENCES = {
    # 2026-08-14, night — MOVED FROM 67 000 B TO 68 000 B, MEASURED AT 67 279 B. What arrived is the
    # fill: a walk that deals its works afresh each visit can now carry a crossing on ANY of its
    # steps, because the settings file may hold one score template per instrument plus a row of
    # measured numbers per ordered pair, and the adapter fills the template's named slots from the
    # row at declare time. In stripped source bytes the whole addition is 1 858 B — 544 B gzipped —
    # and it buys every step of every deal; the alternative, a whole score for each of the ~14 000
    # ordered pairs of a 121-work collection, is ~50 MB of settings file and was never servable.
    # It could not live in pass-layer.js instead: that file is fetched lazily, and the score must be
    # frozen onto the command the moment the transition is declared, which happens first.
    # 2026-08-15 — MOVED FROM 68 000 B TO 69 000 B, MEASURED AT 68 459 B. What arrived is the door
    # to the DELIVERY PACK, and the fence did its job before it arrived: the bundle stood at 67 985 B
    # with 15 B of headroom, so the delivery question was answered rather than waved through. The
    # reader itself — the fetch, the digest chain over a pack's own files, the per-shape template
    # pick and the fill — travels in its own file, pass-reader.js below, weighing 3 125 B gzipped:
    # 200 times the headroom this fence had left, and 4.6 times the host's own 673 B, so neither
    # could have carried it. What lands HERE is 474 B, and it is the part that cannot live outside
    # the bundle: the address the reader is fetched from, the ONE synchronous question a declare
    # puts to it (passScoreFor answers inside declare, and a fetch begun there could never arrive in
    # time), and the landing that warms the next crossing's shard. The bundle keeps the contract and
    # the picture keeps travelling, which is the same division pass-layer.js stands on.
    # 2026-08-16 — MOVED FROM 69 000 B TO 70 000 B, MEASURED AT 69 614 B, with 386 B under it. What
    # arrived is the FAMILY ROLL of §4.4f: a pack row or a table row may name, per slot it already
    # fills, the span the fill may roll that slot inside, and the fill rolls it once per pass from a
    # seed made of the visit, the pass index and the pair. Before it, a pair flipped twice inside one
    # visit played one score byte for byte — the site's own U9 measurement read exactly that on four
    # flips of one pair — and the charter asks for the same family with small shifts each pass.
    # In stripped source bytes the whole addition is 3 449 B, 980 B gzipped: the `familySeed` setting
    # and its rungs, the visit's own seed read once, the two integer mixes the roll runs on, the
    # bounds check with a reason per refusal, the application on the inline road, and the roll's own
    # rows on the diagnostic surface.
    # THE DELIVERY QUESTION THIS FENCE EXISTS TO FORCE, ANSWERED. The roll cannot travel in
    # pass-reader.js, the way the pack's fetch and digest chain do. It is called from INSIDE the
    # declare that mints a pass — passFillScore fills a table row there, and no reader file is
    # fetched at all on a site that scores by §4.4c's template and table, so a roll living in the
    # reader would leave the inline road filling flat. Nor can it live in both: two copies would be
    # two ideas of what a family is, and the contract has one. So the reader is HANDED this roll in
    # its environment record (the `breath` entry), the bundle keeps the one implementation, and what
    # crosses the wire for a pack-served walk is the call, not a second copy.
    # 2026-08-17, evening — THE COMPOSED ROAD REPLACED THE PACK ROADS, and the fence stays at
    # 70 000 B. Three roads left the bundle — the settings record's own per-pair scores, the reader's
    # door with the shard warming, and the template-and-table fill — and one arrived: the composer's
    # door, the passage request the walk builds per edge, the die it rolls for it, and the applied
    # reading written back at the landing. The family roll of §4.4f stays here, since the die the
    # walk rolls is made of the same visit seed, pass index and pair key.
    # 2026-08-17, night — THE VISIT'S OWN MEMORY ARRIVED AND THE FENCE MOVES TO 74 000 B, measured
    # at 73 909 B against 69 715 B the evening before: 4 194 B gzipped, 15 957 B of stripped code.
    # WHERE THOSE BYTES WENT, so the next reader does not have to guess: the whole of PASS-API-V1
    # §4.8 on the site's side — the edge record with its store, its pruning and its bounded keep;
    # the family and the pivot read off a plan; the trace a pass is remembered by; the two refusals,
    # each with the sentence it is named in; the family drift of charter shelf 16; and the visit
    # window with its cooldowns.
    # NONE OF IT CAN TRAVEL IN ANOTHER FILE. §4.8 draws the same fence §4.5 draws for visitor
    # identity: the record is TLV's own and the engine never sees it, so it cannot move into
    # pass-composer.js; and it answers inside `declare`, synchronously, where nothing may wait on the
    # wire, so it cannot be fetched.
    # THE FENCE SITS JUST ABOVE WHAT WAS MEASURED, the way the 70 000 it replaces stood 285 B over
    # its own 69 715. 91 B of headroom is not room to grow in — it is a gate, and the next feature's
    # worth of bytes reds it and comes here to say what it bought.
    #
    # 2026-08-18 — MOVED FROM 74 000 B TO 74 800 B, MEASURED AT 74 694 B (U27 stage 2), and the fence
    # did exactly what the paragraph above says it would: it reddened at 74 694 and the bytes came
    # here to say what they bought. THE WALK NOW STATES WHAT EACH STEP OF THE ROUTE IS FOR. The hang
    # was already ordered by kinship, so the distance the route crosses at each step is a number the
    # walk had already measured; charter shelf 15's grammar is read off that curve — the widest step
    # is the crest, the step leading into it prepares it, a step above both its neighbours is a
    # motion away, everything else is a home the eye settles in — and two roles that are facts about
    # the visit rather than about the route's shape outrank it, a return on an edge this visit has
    # walked and an entrance at its first crossing. The role goes onto the passage request, which is
    # what bounds the composer: what the walk authors is what the crossing is composed inside.
    # 785 B gzipped for the whole of it, and the diagnostic surface's own route block is part of
    # that number rather than left out of the reckoning.
    # THE DELIVERY QUESTION, ASKED AND ANSWERED. None of it can travel in another file. The curve is
    # read off `order` and `shown`, which are the walk's own state in this bundle and nowhere else,
    # and the role is answered inside `declare`, synchronously, where nothing may wait on the wire.
    "exhibition.js": (74_800,"the walk's own bundle: contract and chrome, comment-stripped as shipped; the picture (pass-layer.js) since 2026-08-13 and the passage composer (pass-composer.js) since 2026-08-17 travel separately, and the visit's own seed and its edge memory stay here because the die every crossing is rolled with is made inside declare and the edge record is the site's own", strip_js_comments),
    "exhibition.css": (9_000, "single served stylesheet, comment-stripped as shipped; ~21% over the 2026-07-23 gzip of ~7_415 B", strip_css_comments),
    # 2026-08-14, morning: the stub became a host with a frame half and one real instrument (the
    # woven one), measured at 11 628 B gzipped against the 4 000 B a 167 B stub stood behind.
    #
    # 2026-08-14, afternoon — MOVED AGAIN, TO 21 000 B, MEASURED AT 18 174 B. What arrived is the
    # second half of the woven slice: the transition's nonlinear travel and its camera. In stripped
    # source bytes, measured region by region:
    #   · the driver graph of §5, 8 928 B — the sources (progress, cueProgress, time, velocity,
    #     capability, noise), the operators (named curve, monotone Fritsch-Carlson spline, map, add,
    #     multiply, mix, clamp, hold/segment, ramp/slew, oscillate), named nodes with references, and
    #     the cycle refusal that names the ring;
    #   · the camera of §6, 5 341 B — the pose record, the dolly in log space, the single authority
    #     per instant with the stage's flight held across an owned window, the capability gate, the
    #     handoff measured at the window's own edge, and the rest read off the pose;
    #   · the interruption cadence of §2.5 inside the transaction region, which grew from 15 017 B to
    #     18 858 B — every handle to its nearest door on its own envelope, the deadline the host
    #     force-ends at, and the last frame drawn ON the door.
    # This file is fetched ONLY on a visit that actually draws — reduced motion, Save-Data, no WebGL2
    # and visualLayer:off never ask for it — so its bytes never touch the walk's own bundle above,
    # which stands untouched at 66 735 B against its own 67 000 B fence.
    # 2026-08-14, evening — THE FENCE STANDS AT 21 000 B, MEASURED AT 19 712 B. A second instrument
    # arrived, the matter one of §8, carried over from lab/effects/matter.js: its shader, its
    # response curve of twenty-one measured shares, its field constants, its numbers of one frame
    # and its manifest of nine handles and fourteen name-bound uniforms. In stripped source bytes
    # the whole addition is 1 538 B gzipped, and 1 288 B of the fence remain under it. The number
    # did not move; only this reason did, so the file's own record names both instruments it holds.
    # 2026-08-14, 10:05 — MOVED FROM 21 000 B TO 27 000 B, MEASURED AT 24 270 B, with 2 730 B under
    # it. Two things arrived at once and this is the single move that carries both, sized after the
    # merge rather than estimated before it.
    #   · THE THIRD INSTRUMENT, the meshing one of §8, carried over from lab/effects/gears.js: its
    #     shader, its seating of a work in the frame, its measured response curve, its ladder of
    #     small whole ratios, and a manifest of fifteen handles and nineteen name-bound uniforms. It
    #     is the instrument that carries a radial field from an angular reading to a ring reading,
    #     which is the travel the demonstration pair asks for.
    #   · THE RETURN TO THE HANG of §2.6, the frame half of it: the two exact door geometries, the
    #     anchor that lays the renderer's first frame onto the departing work's real box, the carry
    #     that reseats the picture without moving it, and the rest read against the arriving hang
    #     pose instead of the neutral one.
    # THE REASON THIS NUMBER WILL KEEP MOVING, AND THE REPAIR THAT STOPS IT. Each instrument that
    # lands adds its own shader and manifest to this one file, and 25 lab modules stand on disk. His
    # word of 2026-08-14 08:39 already states the shape that ends it: the engine knows no TLV effect
    # name and loads a version-pinned opaque effect pack, and tlvphotos owns that pack and its
    # manifests. Under that shape this file holds the host alone and its fence stops tracking the
    # effect farm. The split is queued behind the first composed passage.
    # WHAT THIS FILE COSTS A VISITOR: it is fetched only on a visit that actually draws. Reduced
    # motion, Save-Data, a device with no WebGL2 and the layer switched off never ask for it, and
    # the walk's own bundle above stands apart at 67 985 B against its own 68 000 B fence.
    # 2026-08-14, midday — MOVED DOWN FROM 27 000 B TO 24 000 B, MEASURED AT 21 528 B, with 2 472 B
    # under it. THE REPAIR THE NOTE ABOVE KEPT NAMING HAS LANDED, and this fence stops tracking the
    # effect farm. The three instruments left this file for pass-pack.js, which the host fetches by
    # address and loads once its bytes weigh to the digest the build stamped into the host. What
    # stands here is the host alone, and the fence moves DOWN to match, which is what keeps it
    # biting: an instrument landing in the pack no longer moves this number at all, and it is the
    # pack's own fence below that answers for the picture's weight.
    # 2026-08-14, afternoon — the single pack became a file per instrument, and this fence stayed at
    # 24 000 B. The host grew by the loader that reads the site's own record and asks for one file
    # per name, from 21 528 B to 22 503 B, and it still names no instrument.
    # 2026-08-17, evening — MOVED FROM 24 000 B TO 24 100 B, MEASURED AT 24 027 B, with 73 B under
    # it (U27 stage 1, the camera lane). THE BAND IS 73 B AND THAT IS THE WHOLE POINT: a fence
    # carrying a spare kilobyte stops being a gate, because the next kilobyte arrives unremarked and
    # by then nobody remembers the slack was left on purpose. 73 B is the room a gzip stream needs
    # for a version of zlib that packs a shade differently, and nothing more; the next thing that
    # lands here has to say what it is worth. WHAT FILLED THE 638 B between 23 389 and 24 027, and
    # it is all host — no instrument and no effect name came with it:
    #   · TWO NEW PLACES ON THE POSE, orbit and tilt, each carried in its own coordinate — the orbit
    #     in angle, which is the charter's own second case of a straight line in another coordinate
    #     system — with their own entries in the neutral pose, the capability gate and the applied
    #     transform, and the host's own lens where a score names no field of view.
    #   · EACH PLACE ON ITS OWN POINTS. A place is carried through the points that name it rather
    #     than only where every point names it, which is what lets one flight carry several arcs —
    #     the dolly rising and falling at the two edges while the tilt holds a plane at an angle
    #     across a window of its own.
    #   · THE CAMERA-LED PASSAGE, where the flight itself is the transition: the anchor drops its
    #     held middle and travels the whole duration, and a cue claiming the world level beside it
    #     is refused before the command is taken.
    #   · THE SEATING ON THE FRAME STATE, `fitA` and `fitB`, which the doors lane asked for: the
    #     instruments read their seating back inside their shaders and could not reach it in script,
    #     so they bounded it by a worst case and could only over-hold.
    #   · THE BENCH ENTRIES those four are read through — the flight between the two hangs, the
    #     transform a pose becomes, the record one voice is handed, the pose distance and the list
    #     of places. They are diagnostics-only in use and ship in the file all the same, which is
    #     why they are named here rather than left out of the reckoning.
    # WHAT A VISITOR PAYS is unchanged in kind: this file is fetched only on a visit that actually
    # draws, and reduced motion, Save-Data, a device with no WebGL2 and the layer switched off never
    # ask for it at all.
    # 2026-08-18 — MOVED FROM 24 100 B TO 24 200 B, MEASURED AT 24 107 B (U27 stage 2). The camera
    # lane set 24 100 against its own 24 027 and the merge of the four stage-1 lanes carried 80 B
    # more into this file: `2131c38`, where a reading is forgotten when the grid it was taken on
    # moves and the record names the passage's own grid rather than the live canvas. Nothing of
    # stage 2 is in this file at all. The band is 93 B — see THE BAND, below.
    "pass-layer.js": (24_200,"the host's own file, fetched only when a walk asks for it: the state machine, the frame half, the driver graph, the camera with its two turning axes and its led flight, the interruption cadence, the return to the hang and the instrument loader — no instrument and no effect name", strip_js_comments),
    # 2026-08-14, afternoon — ONE FENCE PER INSTRUMENT, each at its own measurement plus about a
    # tenth, by the same rule §12 states for the renderer's own file.
    #
    # WHY THESE ARE FOUR NUMBERS AND NOT ONE. The single pack of the morning broke its own fence the
    # day it was raised: a fourth instrument landed, the pack measured 53 732 B raw against a 38 000
    # B fence, and no fourth instrument of that family fitted at any size. A fence over a bag of
    # instruments answers a question nobody can act on — it says the bag is too heavy and names no
    # instrument. One fence per instrument makes the unit honest: one instrument, one number, and a
    # move here answers one question — is THIS picture worth its bytes to a phone.
    #
    # WHAT A VISIT ACTUALLY PAYS. Each instrument travels as its own file and a visit fetches only
    # the ones its own score names. The composer's census says most passages carry one to three
    # cues, so a one-cue passage pays 4 069 B gzipped where the single pack cost 11 465 B, and the
    # worked pair's three-cue passage pays 11 822 B for the three it names rather than 11 465 B for
    # a farm of four it draws three of. The saving grows with every instrument that lands: the
    # twenty-five lab modules on disk would each have added their whole weight to every visit under
    # the single pack, and add nothing at all to a visit whose score never names them.
    #
    # None of these files reaches a visit that does not draw: reduced motion, Save-Data, a device
    # with no WebGL2 and the layer switched off never ask for the host, and nothing is asked for
    # before a score names it.
    # 2026-08-17 — THE DELIVERY PACK'S READER LEFT, AND ITS 4 000 B FENCE WITH IT (U27 stage 0).
    # pass-reader.js fetched a pack of prebaked per-pair scores; his word of 19:21 retired the pack
    # itself — the collection grows to thousands of works and nothing on the product path may scale
    # with the number of pairs — so the file, its fence and its suite go together. What answers for
    # a pair now is pass-composer.js below, fenced at 20 000 B: one file for the whole collection
    # rather than one shard per departing work.
    # 2026-08-17 — THE CHOICE CORE ARRIVES, MEASURED AT 17 040 B GZIPPED, and it is fenced at
    # 20 000 B. It is the passage composer of the site's own lab/build-sceneplan-v1.py carried into
    # JavaScript: two per-work records and a seed in, the §4.4 score out. His law of 2026-08-14
    # 16:14 is why it exists at all — a crossing is decided at show time and the product carries no
    # table of pairs, so the deciding has to stand where the visit stands. The file is the whole
    # decision: the pivot, the travelling axis, the actors, the arrival, the voices, the levels
    # law, the camera flight, the meshing instrument's own door reading, the shape's template and
    # the fill, plus Python's own number printing so a score written here and a score written by
    # the build are the same bytes. It is UNWIRED as it lands — no bake copies it and no walk asks
    # for it — and it is fenced here so its weight is on the record from its first day.
    # 2026-08-17, evening — IT IS WIRED, and the fence holds unmoved (U27 stage 0). The bake carries
    # it beside pass-layer.js, the walk asks its one entry on every edge, and the prebaked door
    # lookup left it: what the composer emits for the meshing travel is the artistic request, and
    # the instrument holds its own doors on the buffer it draws on (his architecture decision of
    # 18:00). A visit fetches this ONE file for the whole collection where it used to fetch a
    # reader plus a shard per departing work.
    # ------------------------------------------------------------------------------------------
    # THE BAND, stated once for every gzipped fence this block moves on 2026-08-18 (U27 stage 2).
    # A gzipped figure is not exactly reproducible: a different version of zlib packs a shade
    # differently, so a fence set ON the measurement would redden on another machine for no change
    # at all. The rule applied here, so a later reader can re-derive every number rather than trust
    # it: THE FENCE IS THE MEASUREMENT ROUNDED UP TO THE NEXT HUNDRED, and where that would leave
    # under 75 B it takes the hundred above instead. Every band below therefore lies between 73 and
    # 116 B — room for the compressor and for nothing else. A plain byte count of generated text
    # reproduces exactly and would take a tighter fence; none of these is one.
    #
    # 2026-08-18 — MOVED FROM 20 000 B TO 23 900 B, MEASURED AT 23 784 B (U27 stage 2). Stage 1's
    # composer lane rewrote what this file decides and the fence was never moved with it: the seven
    # roads that are the plural sources of a crossing's structure, each stating in its own lines the
    # readings that qualify a pair for it; the route role, which bounds what is emitted and names the
    # register the composer reaches for; the visit's memory, answered in three steps so a return
    # keeps its family or its pivot; the nine handles that gained the measurement they read; and the
    # camera-led passage. 6 744 gzipped bytes for all of it, on the ONE file a visit fetches for the
    # whole collection.
    # IT WAS EXPECTED TO MOVE AGAIN AT THE NEXT MERGE, and it did, within the hour: 23 900 B became
    # 25 700 B, MEASURED AT 25 609 B, when the composer lane closed stage 1 with the box-fold road.
    # 1 825 gzipped bytes bought the road built from how a work is made when it folds along strong
    # directions — the crease placed on the departing work's own measured region line, the five
    # conditions of the charter's box law answered, and the one miracle it spends guarded where it
    # can be reached. What it buys on the route is measured rather than argued: pairs reaching the
    # culmination tier go from 112 to 571, and 207 ordered pairs of the collection take the box-fold
    # road at a middle where none could before. Band 91 B.
    "pass-composer.js": (25_700,"the choice core, and the one entry every edge of the walk comes through: two per-work records and the walk's own die composed into a §4.4 score at the instant the pair is cast, so no table of pairs travels; fetched once at the walk's first landing", strip_js_comments),
    # 2026-08-18 — MOVED FROM 6 000 B TO 7 300 B, MEASURED AT 7 222 B (U27 stage 2). The runtime-door
    # work of stage 0 landed in this file and its fence was never moved with it: the instrument reads
    # its own doors on the buffer it draws on and reports what it applied or the refusal it named
    # (his architecture decision of 2026-08-17 18:00), which is the runtime truth the walk writes
    # onto the passage record. 1 778 gzipped bytes, and only a visit whose own score names this
    # instrument pays them. Band 78 B.
    "pass-inst-adrift.js": (7_300,"the adrift instrument, measured at 7 222 B: a dense thing leaves across an empty field and the field itself changes hands along a measured front — its shader, its two silhouettes, its contact shadow, its response curves, its door reading on the buffer it draws on, and its manifest", strip_js_comments),
    # 2026-08-15 — MOVED FROM 5 000 B TO 6 100 B, MEASURED AT 5 551 B. The meshing instrument now
    # reads its own doors: at either door it evaluates its own mask around each wheel's centre — the
    # one place a leak can stand — and refuses a pose whose door is two works at once, with the alpha
    # it measured in the reason. That is 1 019 gzipped bytes, and it is what makes the coverage law
    # this instrument's manifest publishes true by the instrument's own reading rather than by an
    # argument made upstream of it. The file reaches only a visit whose own score names it.
    # 2026-08-16 — moved from 6 100 B to 6 600 B, measured at 6 026 B. The door reading moved off the
    # CSS frame onto the drawing buffer the shader samples on, and a door whose size leaks there is
    # held to the nearest whole size rather than refused, with the composer's request kept beside the
    # size applied. What a visit pays for the whole instrument is 6 026 B gzipped, and only a visit
    # whose own score names it pays them.
    # 2026-08-18 — TIGHTENED FROM 6 600 B TO 6 200 B, MEASURED AT 6 127 B (U27 stage 2). Nothing
    # arrived: this is the one instrument fence stage 1 left UNDER its own number, and 473 B of slack
    # on a 6 KB file is 8 per cent — the share the visit-memory lane's own fence was tightened for on
    # the judge's ruling, and the share at which a fence stops being a gate and becomes a comment.
    # Band 73 B.
    "pass-inst-gears.js": (6_200,"the meshing instrument, measured at 6 127 B: two wheels meshing along the line their rims meet, one work riding each — its shader, its ladder of small whole ratios, its response curve, the door reading on the buffer it draws on that holds a leaking size whole, and its manifest of fifteen handles and nineteen name-bound uniforms", strip_js_comments),
    # 2026-08-17 — A FENCE FROM DAY ONE for the panels instrument, at the measured 4 754 gzipped
    # bytes plus about a tenth, by the rule §7 states for each instrument. It is the first port
    # whose lab module carried no shader: the module draws with CSS 3D and the compositor projects
    # it, so what this file carries is the inverse of that transform chain — a two-by-two solve per
    # panel across four panels and the sheet's own plane, with each panel's shade and crease. A
    # visit pays these bytes only when its own score names this instrument.
    # 2026-08-18 — MOVED FROM 5 250 B TO 9 600 B, MEASURED AT 9 517 B (U27 stage 2), and this is the
    # largest move in the block. What arrived is the PROCESS REGISTER the charter names by example:
    # past the sheet's own rectangle the plane goes on, and what continues is the sheet's own law —
    # each panel already the mirror of the quarter it closes onto — running off to a real horizon at
    # the work's own cutting step and the work's own angle, with the world's own light beyond it.
    # Beside it stand the runtime door reading, the camera's tilt subtracted from the plane's own
    # pitch so one voice holds the world level, the seating read off the frame state, and the
    # measured response curve on the one handle whose value is a position. 4 763 gzipped bytes.
    # IS IT WORTH THEM? The charter's own answer is that this is one of the two registers a crossing
    # carries — «some transformations simply reveal the making, e.g. an unfold that becomes an
    # infinite parquet while the 3D camera shows the plane at an angle» — so these bytes are the
    # register itself and not an ornament on one. Band 83 B.
    "pass-inst-unfold.js": (9_600,"the unfold instrument, measured at 9 517 B: one work folds shut along its own mirrored panels until the single photograph it was cut from stands alone, the two works exchange on that photograph, and the other opens out — and past the sheet's own edge that same law runs on into a parquet at the work's own cutting step and angle, away to a real horizon; its inverted transform chain, its growth law, its world, its response curve, its door reading and its manifest", strip_js_comments),
    # 2026-08-18 — MOVED FROM 3 550 B TO 4 700 B, MEASURED AT 4 588 B (U27 stage 2). The runtime door
    # reading and its report, as on the adrift: 1 367 gzipped bytes on the smallest instrument that
    # ships, and on the one this collection casts most often. Band 112 B.
    "pass-inst-matter.js": (4_700,"the matter instrument, measured at 4 588 B: one work loosens into a grain dragged along a seeded field and the other condenses out of it — its shader, its response curve, its door reading on the buffer it draws on, and its manifest", strip_js_comments),
    # 2026-08-18 — MOVED FROM 4 500 B TO 7 800 B, MEASURED AT 7 722 B (U27 stage 2). Two things
    # arrived and both are repairs rather than features. The runtime door reading and its report, as
    # above. And THE STRAIGHT RIBBON, restored: a later copy had rewritten the woven edge wavy with
    # eleven literals that read nothing off any photograph, and the wave is now a handle resting at
    # zero, gated on the collection's own texture reading and given its depth by how far a work's own
    # lines depart from straight. At zero every wave term degenerates to nothing and the pre-wave
    # frame is what the shader computes — measured at 0.0033 of 255 against the module as it stood
    # before the regression. 3 653 gzipped bytes for the door reading and for the reference look
    # coming back. Band 78 B.
    "pass-inst-weave.js": (7_800, "the woven instrument, measured at 7 722 B: a band family warping across the frame — its shader, its seating of a work in the frame, its response curve, the turn of the weave, the wave that plays only where the work carries one, its door reading on the buffer it draws on, and its manifest", strip_js_comments),
    # 2026-08-18 — A FENCE FROM DAY ONE for the box instrument, at the measured 8 289 B plus a band
    # of 111 B (U27 stage 2). It ships and it had no fence, which the pack suite's own «a fence is
    # written for every instrument that ships» row is there to catch. The frame is one face of a
    # solid: the box turns a quarter with true perspective while the camera rides up through the turn
    # and slides sideways, the standing face gives way to the one coming round, and they meet at a
    # finger joint with a contact shadow along it — the crease placed on the departing work's own
    # measured region line, which is the first of the charter's five box conditions. A visit pays
    # these bytes only when its own score names this instrument, and no score does until the composer
    # names an instrument for the panel cut.
    "pass-inst-boxfold.js": (8_400, "the box instrument, measured at 8 289 B: one face of a solid turning a quarter under true perspective, creasing on the departing work's own measured region line, with its finger joint, its contact shadow, its per-pixel homography and its manifest", strip_js_comments),
}

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def gz(path, transform=None):
    """gzip size at level 6 (plain `gzip -c`), mtime zeroed so the count is deterministic. `transform`
    (when given) is the bake-time text treatment, so the fence measures the SHIPPED bytes, not source."""
    data = path.read_bytes()
    if transform is not None:
        data = transform(data.decode("utf-8")).encode("utf-8")
    return len(gzip.compress(data, compresslevel=6, mtime=0))


for fname, (fence, reason, transform) in FENCES.items():
    p = ASSETS / fname
    if not p.exists():
        check(f"BUDGET {fname}: asset present to measure", False, f"missing at {p}")
        continue
    size = gz(p, transform)
    check(f"BUDGET {fname}: gzip {size} B under the {fence} B fence ({reason})",
          size <= fence,
          f"gzip={size} B  fence={fence} B  ({'under' if size <= fence else 'OVER — bundle ballooned'})")

# EX-STORY-FILL ratchet: SPEC.md states a browser's story requests stay under the edge's
# per-address hourly ceiling — "two walks in one hour are 18, and five one-work asks at three
# rungs are 15, reaching 33 against the per-address ceiling of 40." Read every number OUT OF
# THE SOURCE (never hardcoded) so a knob raised past the ceiling reds this row rather than
# leaving that sentence false.
WORKER_JS = ASSETS / "worker.js"                              # RL_PER_HOUR (the edge's own fence)
STORY_VOICE_JS = ASSETS.parent / "client" / "09-story-voice.js"  # SOLO_PER_HOUR, STORY_RETRY_MS
BUILD_PY = ASSETS.parent / "build.py"                          # bake's default config: max_unfolds

_rl_m = _solo_m = _retry_m = _maxu_m = None
if WORKER_JS.exists():
    _rl_m = re.search(r"RL_PER_HOUR\s*=\s*(\d+)", WORKER_JS.read_text())
if STORY_VOICE_JS.exists():
    _voice_src = STORY_VOICE_JS.read_text()
    _solo_m = re.search(r"SOLO_PER_HOUR\s*=\s*(\d+)", _voice_src)
    _retry_m = re.search(r"STORY_RETRY_MS\s*=\s*\[([^\]]*)\]", _voice_src)
if BUILD_PY.exists():
    _maxu_m = re.search(r'"max_unfolds":\s*(\d+)', BUILD_PY.read_text())

if not (_rl_m and _solo_m and _retry_m and _maxu_m):
    check("BUDGET EX-STORY-FILL: an hour's story requests stay under the edge's per-address ceiling",
          False,
          f"could not read RL_PER_HOUR({WORKER_JS.exists()}) SOLO_PER_HOUR/STORY_RETRY_MS"
          f"({STORY_VOICE_JS.exists()}) max_unfolds({BUILD_PY.exists()}) — see paths in test source")
else:
    rl_per_hour = int(_rl_m.group(1))
    solo_per_hour = int(_solo_m.group(1))
    rungs = len([x for x in _retry_m.group(1).split(",") if x.strip()]) + 1  # ask + its re-asks
    max_unfolds = int(_maxu_m.group(1))
    total = 2 * (1 + max_unfolds) * rungs + solo_per_hour * rungs
    check(f"BUDGET EX-STORY-FILL: two walks + the hour's solo asks ({total}) stay under "
          f"RL_PER_HOUR ({rl_per_hour})",
          total <= rl_per_hour,
          f"rungs={rungs} (len(STORY_RETRY_MS)+1) max_unfolds={max_unfolds} "
          f"SOLO_PER_HOUR={solo_per_hour} RL_PER_HOUR={rl_per_hour} — "
          f"2*(1+max_unfolds)*rungs + SOLO_PER_HOUR*rungs = {total}")

fails = [r for r in results if r[1] == "FAIL"]
for name, st, detail in results:
    print(f"[{st}] {name}" + (f"  — {detail}" if detail else ""))
print(f"\n{len(results)} rows: {len(results) - len(fails)} pass, {len(fails)} fail")
sys.exit(1 if fails else 0)
