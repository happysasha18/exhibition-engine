#!/usr/bin/env python3
"""The one gate command, in three modes (plan row S-114).

Each suite is isolated: its own copy of the base stage, its own http port, its own headless Chrome.

Usage: python tests/run_all.py [--mode row|integration|release] [--jobs 8]
                              [--acceptance a,b,c] [--changed path ...]
Exit 0 only if every suite that RAN exits 0, and only if the roster, the frozen cast, the skip
ratchet and the expected-red list all say the run may go green.

WHY THERE ARE MODES AT ALL, AND WHY THE DEFAULT IS STILL THE WHOLE ROSTER. `TEST_MATRIX.md` is a
catalogue of requirements and of the proof each one owes; it was being read as a list of runs owed
after every commit, so a one-line edit stood behind the better part of an hour of browsers. What a
fact owes is named by its PROOF LAYER, and the five layers are stated in the same words here, in
`TEST_MATRIX.md` and in `.live-spec/profile.md`. The two narrow modes exist for work in progress and
each one PRINTS what it left out and why. Naming no mode still runs everything, because the safe
answer must be the one nobody has to remember to ask for, and a push certifies on that.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
TIMINGS_PATH = HERE / "suite_timings.json"
SKIP_RATCHET_PATH = HERE / "skip_ratchet.json"
VERDICTS_PATH = HERE / "suite_verdicts.json"

# Every suite's own final line answers "how many rows did I SKIP" in one of a small number of
# shapes already in use across tests/ — "N passed / M failed / K skipped", "rows: N pass, M fail,
# K skip", "N passed, M failed, K skipped" — all of them a digit immediately followed by the word
# "skip", "skips" or "skipped". Reading that line off the suite's own captured log costs nothing a
# suite was not already going to print, and needs no suite to change how it reports itself.
SKIP_COUNT_RE = re.compile(r"(\d+)\s+skip(?:s|ped)?\b", re.IGNORECASE)

# SUITES must match the set of test_*.py files in tests/ exactly (gate INV-5r).
# Add a suite name here AS SOON as tests/test_<name>.py is created.
SUITES = [
    "site", "exhibition", "door", "vector", "back", "greet",
    "series", "motion", "consistency", "reset", "load", "ladder", "share", "glide",
    "pulse", "hand", "i18n", "lang", "lang_geo", "memory", "protect", "sound", "guard", "bundle_fresh", "quiz",
    "quiz_copy", "compose", "dead", "quiz_flow", "parity", "zoom", "return", "gesture",
    "wheel", "glide_speed", "beat_css", "a11y", "about",
    "story_edge", "story_lead", "pass", "pass_api", "pass_direction", "pass_weave", "pass_drivers",
    "pass_hang",
    "pass_arrival_arc",
    "pass_arrival_reach",
    "pass_crest_law",
    "pass_step_sequencer",
    "pass_polyphony_presence",
    "pass_seam_readers",
    "pass_sources_hold",
    "pass_matter",
    "pass_gears",
    "pass_stack",
    "pass_pack",
    "pass_adrift",
    "pass_unfold",
    "pass_coverage",
    "pass_composed",
    "pass_memory",
    "pass_verdict",
    "pass_layer",
    "pass_hand",
    "pass_gestures",
    "pass_boxfold",
    "pass_droste",
    "pass_planet",
    "pass_overlay",
    "pass_liquid",
    "pass_hero",
    "pass_lens",
    "pass_parquet",
    "pass_tunnel",
    "pass_kaleidoscope",
    "pass_route",
    "pass_phone",
    "pass_livemirror",
    # THE ARSENAL LANE, 2026-08-18, on his word of 18:39: every effect the lab holds belongs in the
    # engine's arsenal, with all its handles. Six instruments carried across from lab/effects/ —
    # `box` was already here under the name `boxfold`, and three names are held out by dated words
    # of his (see the lane's report). The two hyphenated names are the file stems exactly: the
    # identity gate above reads `test_<name>.py` off disk, so the list and the files cannot drift.
    "pass_beat",
    "pass_gates",
    "pass_grid-colour",
    "pass_strata-light",
    "pass_tilt",
    "pass_waterline",
    # THE OWNER'S WORD OF 2026-08-18 23:21 — every instrument the lab holds but the shards belongs
    # in the arsenal. `studio`, the darkroom chain, was the first of the two named modules this lane
    # carried. `strata-scale` was reported stopped on a wall — that report was wrong: its threshold
    # and its per-stratum centre of gravity are reductions over ONE photograph, exactly the per-work
    # fact `luminance.level` already ported for `strata-light`, and lab/analyze/recipes.py now
    # solves both at build time (`strata_scale_measure()`) the same way.
    "pass_studio",
    "pass_strata-scale",
    # 2026-08-25 — THE SUITES WRITTEN TONIGHT TO PROVE TONIGHT'S WORK, registered in the same pass
    # that finally gave gate INV-5r above its code. They had been shipping unregistered: every one
    # of them ran, green or red, standalone, and none of them ran here — so a full gate would have
    # reported green with ten proofs unexecuted. That is worse than a missing test: a missing test
    # is visible in the tree and an unregistered one is not.
    #
    # Three carry the instruments that landed today; the rest carry the laws, the readings, the
    # seams and the client's own reading of a score. Five are RED as they are registered, and they
    # are registered red on purpose — `pass_lawful` is written red by its own author, each row
    # standing until its repair lands, and a red this gate reports is the point of running it.
    #
    # `pass_score`, `pass_cover` and `pass_palette` are here because the check below found them.
    # All three landed while the first nine were being registered, and all three would have gone
    # the same way those nine did. The gate named each within seconds of the suite appearing, which
    # is the whole argument for giving that sentence code: the drift is not a one-off to be swept
    # up, it is continuous, and a roster kept by hand is a roster that is wrong most of the time.
    "pass_pour",
    "pass_veil",
    "pass_wind",
    "pass_viewer",
    "pass_harmony",
    "pass_roll",
    "pass_score",
    "pass_cover",
    "pass_peak",
    "pass_seam",
    "pass_lawful",
    "pass_palette",
    "pass_static",
    "pass_levels",
    "pass_matter_gate",
    "pass_door",
    # 2026-08-28 — S-20's own suite, registered in the pass that wrote it. One law with seven
    # readers: how a measured response table is read BETWEEN its own twenty-one points, which is
    # where the fleet's speed used to step.
    "pass_feel",
    # P1.2 (2026-08-28) — the joint phrase planner's own five legality rules, its score and its
    # widened return, registered in the pass that wrote it.
    "pass_bundle",
    # P1.3 (2026-08-28) — record.symmetry and record.matter/record.substance, read by no line
    # before this phase, connected into genresFor's own ranking, registered in the pass that wrote
    # it.
    "pass_p13",
    # Cause A (2026-08-31, V2-CONVERGENCE-PLAN-2026-08-31.md Phase 1) — the casting tier ladder
    # ranks instead of gating, registered in the pass that wrote it.
    "pass_cast_tiers",
    # Cause B (2026-08-31/09-01, V2-CONVERGENCE-PLAN-2026-08-31.md Phase 2) — the fleet-wide,
    # by-construction proof that a crop cancels at a real door (box-fold and hero's own repair),
    # registered in the pass that wrote it. Droste's own row was left red on purpose here until
    # 2026-09-02, when its own crop-class bug (the same shape as cause B, in a file Phase 2 never
    # looked at) was found and fixed — see tests/test_pass_door_orientation.py.
    "pass_door_invariant",
    # 2026-09-02 — the orientation companion to pass_door_invariant: every instrument driven through
    # a real portrait/landscape door, catching the axis-stretch class cause B's own fix never
    # reached (droste, planet). Registered in the pass that wrote it.
    "pass_door_orientation",
    # 2026-09-02 — PASS-VOICE-DOOR-SNAP: a non-primary voice interrupted mid-cadence used to snap to
    # its door in the walk's own first frame instead of walking there like the primary, registered
    # in the pass that wrote it.
    "pass_voice_cadence_walk",
    # 2026-09-03 — S-31: the route-wire fence (tests/dump_route_wire_fence.py, 27de269) shipped
    # standalone, never through this one gate command. Registered in the pass that wired it in.
    "route_wire_fence",
    # 2026-09-03 — S-73: fourteen instruments' declared `reads:` lines, each of them proven until
    # now by grepping the same sentence back out of the built file. One driver varies every declared
    # measurement across two real works and reads which handle and which fit actually answer.
    # Registered in the pass that wrote it.
    "pass_reads",
    # DR-5 (2026-09-04): the darkroom's in-browser analyser port (busyness, lines, mirror axis).
    # Registered by the seat at DR-5's accept step.
    "darkroom_measure",
    # DR-6 (2026-09-04): the darkroom's bench, which instruments a work's own matter affords.
    # Registered by the seat at DR-6's accept step.
    "darkroom_bench",
    # DR-7/8/9 (2026-09-04): the darkroom's taste — resistance, instrument exchange, one miracle.
    # Registered by the seat at DR-9's accept step (the file DR-7 opened, DR-8 and DR-9 extended).
    "darkroom_taste",
    # EX-HAND U5 (2026-09-04): the hand as unfold's clock — the progress profile the hand drives.
    # Registered by the seat at the merge of U1/U3/U5 into main.
    "pass_hand_profile",
    # S-110 (2026-09-05): the device is read once while the page loads, and the row it publishes is
    # the ceiling a crossing is cast under. Registered in the pass that wrote it.
    "pass_device",
    # S-37 (2026-09-05): the whisper law — a work at rest breathes, and a still taken at any instant
    # is still the work. Registered in the pass that wrote it.
    "pass_whisper",
    # S-39 (2026-09-05): the gallery conductor — one soloist, at most two neighbours, everything
    # else still or paused, and a crossing in flight taking the solo. Registered in the pass that
    # wrote it.
    "pass_conductor",
    # S-40 (2026-09-05): the six matter families, each by its own row of the matter table — a work
    # of each stands, breathes on its family's own letter, and a still of it is still the work.
    # Registered in the pass that wrote it.
    "pass_families",
    # S-47 (2026-09-05): the result's life — the link word, the film compiled through the crossing
    # skeleton, and the seam check and the no-cut lint run on every compiled film. Registered in the
    # pass that wrote it.
    "darkroom_film",
    # S-112 (2026-09-05): the standing work is drawn breathing on the walk — the voice from S-37,
    # the seat from S-39 and the box from S-91 reaching the picture a visitor is looking at.
    # Registered in the pass that wrote it.
    "pass_standing",
    # S-114 (2026-09-06): the gate's own laws — the five proof layers stated in one vocabulary in
    # three homes, the three modes and the full-roster default, what widens a selection and what may
    # never narrow one, the one immutable base stage, and the absence of a product pair table.
    # Registered in the pass that wrote it.
    "gate_modes",
]

# EXPECTED_RED names every suite this tree currently ships red on purpose, one reason each. A
# suite that reds with no entry here is a surprise, and a surprise reds the whole run — that is
# S-26's third arm: a list of expected-red rows with a reason for each, so a row outside the list
# going red is the thing that must not pass in silence.
#
# The comments in SUITES above once named five suites red on purpose the night they were
# registered (2026-08-25): `pass_lawful` (its own four laws, until Phase 8's enforcement landed),
# `pass_score` / `pass_cover` / `pass_palette` (found unregistered by check_roster(), and would
# have shipped the same way), and `pass_droste` (left red on purpose until its crop-class bug was
# found and fixed on 2026-09-02). Run individually on 2026-09-03, all five now pass — the repairs
# those comments point to have since landed — so nothing is named here right now. Add a suite here,
# with its own one-line reason, the day it ships red on purpose again.
EXPECTED_RED = {}

# ---------------------------------------------------------------- the five proof layers (S-114)
# THE SAME FIVE NAMES, IN THE SAME WORDS, that `.live-spec/profile.md` and `TEST_MATRIX.md` carry.
# Three homes, one vocabulary; `tests/test_gate_modes.py` holds the standing verdict that they have
# not drifted apart, and the plan row's own acceptance reads all three.
LAYER_STATIC = "static/source contract"
LAYER_NODE = "pure Node/function composition"
LAYER_RUNTIME = "browser runtime contract"
LAYER_PIXEL = "pixel/WebGL/layout/interaction"
LAYER_DEVICE = "live-device runtime observation"
PROOF_LAYERS = (LAYER_STATIC, LAYER_NODE, LAYER_RUNTIME, LAYER_PIXEL, LAYER_DEVICE)

# NO SUITE IN THIS TREE STANDS AT `LAYER_DEVICE`, and that is the honest state rather than a gap.
# A live-device fact is read in the visitor's own browser after a deploy (`lab/perf.html`,
# `lab/perf-serve.py`); the builder host is never the device (plan row S-113), so a suite here that
# claimed that layer would be claiming exactly the measurement the owner banned.


def layer_of(name):
    """This suite's proof layer, read off the suite's OWN SOURCE rather than off a hand-kept table.

    A table of 122 names mapping suite to layer would be wrong within the week — the same drift
    `check_roster` below exists to stop, in a second place. What a suite actually needs is a fact
    about what it does: a suite that constructs `headless.Browser` needs a browser, and no sentence
    anywhere can make that untrue. So the reading is:

      · it constructs a Browser and reads pixels back (a screenshot, or Pillow over one) — the fact
        is about the picture or the hand, so `pixel/WebGL/layout/interaction`;
      · it constructs a Browser and does not — the fact is about what the runtime does, so
        `browser runtime contract`;
      · it runs `node` — the REAL shipped block is run against stated inputs, so
        `pure Node/function composition`;
      · neither — it reads the source, so `static/source contract`.

    The order matters and is not arbitrary: a suite that drives a browser AND shells out to node is
    at the browser layer, because the browser is the part that cannot be spared.
    """
    src = (HERE / f"test_{name}.py").read_text(encoding="utf-8", errors="replace")
    if "Browser(" in src:
        reads_pixels = ("captureScreenshot" in src or "from PIL" in src
                        or "import PIL" in src or "Image.open" in src)
        return LAYER_PIXEL if reads_pixels else LAYER_RUNTIME
    if '"node"' in src or "'node'" in src:
        return LAYER_NODE
    return LAYER_STATIC


# ---------------------------------------------------------------- what widens a selection to all
# A CHANGE TO ONE OF THESE REACHES EVERY SUITE, so no narrow mode may stand over one. They are the
# shared renderer and composer, the thing that bakes the stage every browser suite stands on, the
# driver every browser suite is driven by, and this runner itself. The list is short on purpose: a
# long one is a list of guesses, and each name here is a file that literally every suite of some
# layer loads or is built by.
CROSS_CUTTING = (
    "engine/assets/pass-layer.js",     # the host: every passage every browser suite plays
    "engine/assets/pass-composer.js",  # the composer: every score every suite reads or drives
    "engine/assets/exhibition.js",     # the walk itself, which every browser suite enters through
    "engine/build.py",                 # the bake every stage is made by
    "tests/engine_build.py",           # the shared stage builder
    "tests/headless.py",               # the browser driver
    "tests/run_all.py",                # this file
)

# THE ARCHITECTURAL INVARIANTS EVERY MODE CARRIES, however small the change. Each is a law of the
# engine already derived from SPEC.md rather than a favourite suite: the four pass laws, the
# coverage law, the levels law, the matter gate, the route wire fence, and this runner's own laws.
# They are here because a change that looks local can still break a law that holds everywhere, and
# because a narrow mode with nothing constant in it is a narrow mode that proves only what its
# author already suspected.
ARCH_INVARIANTS = ("pass_lawful", "pass_coverage", "pass_levels", "pass_matter_gate",
                   "route_wire_fence", "gate_modes")


def suites_naming(paths):
    """Every suite whose own source names one of these paths — evidence, never a guess from a name.

    A suite is selected because its text mentions the file that changed, by repo-relative path or by
    basename. That is a fact about the suite, and it is the reason the selection is printed: a reader
    can check it. Matching on a suite's NAME instead ("pass_hero must be about hero") is the guess
    this project has already been burned by, and it is not done here.
    """
    hit = {}
    for suite in SUITES:
        src = (HERE / f"test_{suite}.py").read_text(encoding="utf-8", errors="replace")
        for p in paths:
            if p in src or Path(p).name in src:
                hit.setdefault(suite, []).append(p)
    return hit


def select(mode, acceptance, changed):
    """Which suites this run covers, and — for every suite it does not — the reason it does not.

    Returns `(chosen, why, omitted_reason)`: an ordered list, a map from suite to the sentence that
    put it there, and one sentence covering everything left out. Nothing is ever dropped silently:
    a run that cannot ATTRIBUTE a changed path to any suite widens to the whole roster and says so,
    because an unattributable change is exactly the one a narrow selection would step over.
    """
    if mode == "release":
        return list(SUITES), {s: "release · the whole roster" for s in SUITES}, None

    changed = list(changed or [])
    acceptance = [a for a in (acceptance or []) if a]
    unknown = [a for a in acceptance if a not in SUITES]
    if unknown:
        print(f"gate · --acceptance names {', '.join(unknown)}, which no suite answers to. A row's "
              f"acceptance that names nothing runnable is a row with no acceptance.")
        raise SystemExit(2)

    crossing = [p for p in changed if any(c in p for c in CROSS_CUTTING)]
    if crossing:
        why = f"{mode} · widened to the whole roster: {', '.join(crossing)} is shared by every suite"
        return list(SUITES), {s: why for s in SUITES}, None

    docs = [p for p in changed if p.endswith(".md")]
    code = [p for p in changed if not p.endswith(".md")]

    named = suites_naming(code) if code else {}
    unattributed = [p for p in code if not any(p in v for v in named.values())]
    if unattributed:
        why = (f"{mode} · widened to the whole roster: no suite's own source names "
               f"{', '.join(unattributed)}, so nothing here can say what proves it")
        return list(SUITES), {s: why for s in SUITES}, None

    why = {}
    for s in acceptance:
        why[s] = f"{mode} · named by the row's own acceptance"
    for s, paths in named.items():
        why.setdefault(s, f"{mode} · its own source names {', '.join(sorted(set(paths)))}")

    # INTEGRATION TAKES THE WHOLE OF EVERY LAYER IT TOUCHES, which is what makes it wider than a row
    # gate rather than a row gate with more names in it. A row proves its own change; an integration
    # proves that everything standing at the same rung of proof still stands.
    if mode == "integration":
        touched = sorted({layer_of(s) for s in named} | {layer_of(s) for s in acceptance})
        for s in SUITES:
            if layer_of(s) in touched:
                why.setdefault(s, f"integration · every proof at the «{layer_of(s)}» layer, "
                                  f"which this change touches")

    for s in ARCH_INVARIANTS:
        if s in SUITES:
            why.setdefault(s, f"{mode} · an architectural invariant every mode carries")

    chosen = [s for s in SUITES if s in why]
    left = [s for s in SUITES if s not in why]
    reason = None
    if left:
        reason = (f"left out: {len(left)} suite(s) — no changed path is named in their own source, "
                  f"they are not this row's acceptance, and they are not architectural invariants"
                  + (f". The {len(docs)} changed document(s) reach no suite's source at all"
                     if docs and not code else "")
                  + f": {', '.join(left)}")
    return chosen, why, reason


def check_roster():
    """Gate INV-5r, in code: SUITES names exactly the `test_*.py` files in tests/.

    The line above SUITES has CLAIMED this since this runner was written and nothing enforced it.
    On 2026-08-25 the two lists stood nine apart — nine suites written that night to prove that
    night's work, none of them named here — and the drift was invisible precisely because the only
    thing asserting the rule was a sentence in a comment. A gate anchored on comment text passes
    vacuously, and this is the code that makes the sentence true.

    It runs BEFORE the first suite is spawned. The comparison is a directory listing, so it costs
    nothing worth measuring, and a run must never begin in a state where its own roster is wrong:
    the whole verdict of a full run is «every suite green», which means nothing at all if the set
    of suites is not the set of suites that exist.

    Both directions are named, because they are different faults. A name here with no file is a
    run that dies on a missing path. A file with no name here is the silent one: it never runs, it
    never reports, and the gate goes green over it.
    """
    on_disk = sorted(p.stem[len("test_"):] for p in HERE.glob("test_*.py"))
    absent = [s for s in sorted(SUITES) if s not in on_disk]
    unlisted = [s for s in on_disk if s not in SUITES]
    twice = sorted({s for s in SUITES if SUITES.count(s) > 1})
    if not absent and not unlisted and not twice:
        return
    print("gate INV-5r · the suite roster and the suites on disk disagree, so this run is refused "
          "before it starts")
    print(f"  SUITES names {len(SUITES)}; tests/ holds {len(on_disk)} test_*.py file(s)")
    if unlisted:
        print(f"  on disk and named by no SUITES entry, so never run and never reported: "
              f"{', '.join(unlisted)}")
    if absent:
        print(f"  named in SUITES with no tests/test_<name>.py behind it: {', '.join(absent)}")
    if twice:
        print(f"  named in SUITES more than once, so run more than once: {', '.join(twice)}")
    print("  Register each unlisted suite in SUITES, or drop the stale name. A proof that is never "
          "executed reports as green.")
    raise SystemExit(2)


def check_pass_fixture():
    """The frozen instrument cast in the two pass fixtures still names every instrument that ships.

    Same spirit as INV-5r above and the same argument: it is a quarter of a second answering a
    question that otherwise costs a full browser suite to discover. `tests/test_pass_composed.py`
    carries the standing verdict on this, and it is the right place for it — but that suite bakes a
    site and drives a browser to reach it, so learning there that a fixture needs regenerating is
    minutes of Chrome to be told to run a script. Asking here means a run does not start against a
    stale cast at all.

    Three answers, kept apart: the cast matches, the cast has drifted, or the site's staging step
    could not be reached. Only a DRIFT refuses the run. An unreachable staging step is not a fault
    in this tree — the harvest lives in the site's tree, which a checkout here need not have — so it
    is said plainly and the run goes on, with `test_pass_composed.py` still standing behind it.
    """
    script = HERE / "build_pass_fixture_consts.py"
    if not script.exists():
        return
    done = subprocess.run([sys.executable, str(script), "--check"],
                          capture_output=True, text=True)
    if done.returncode == 0:
        return
    if done.returncode in (3, 5):
        # NEITHER OF THESE IS A FAULT IN THIS TREE, so neither stops the run — but both are said in
        # full rather than swallowed. 3 is the site's staging step out of reach, which a checkout
        # here need not have. 5 is that staging step reading a field as absent that the instrument
        # publishes: the fixture standing on disk is the last one written before the harvest went
        # unreliable, so it is the better of the two available answers, and the repair belongs
        # upstream. What must not happen quietly is a run proceeding as though the cast had been
        # confirmed when it could not be.
        print("note · the frozen instrument cast was NOT confirmed before this run"
              + (" (the site's staging step is out of reach)" if done.returncode == 3
                 else " (the site's staging step is dropping published fields)") + ":")
        for line in done.stdout.strip().splitlines():
            print("  " + line)
        return
    print("gate · the frozen instrument cast in the pass fixtures does not answer for the "
          "instruments this tree ships, so this run is refused before it starts")
    for line in done.stdout.strip().splitlines():
        print("  " + line)
    raise SystemExit(2)


def suite_skip_count(log_text):
    """This suite's own SKIP tally, read off the last line of its captured output that reports one
    (see SKIP_COUNT_RE above). A suite with no such line never uses SKIP at all, so it counts zero
    — there is no suite whose skip count matters but whose own log never states it."""
    for line in reversed(log_text.splitlines()):
        m = SKIP_COUNT_RE.search(line)
        if m:
            return int(m.group(1))
    return 0


def check_skip_ratchet(total_skips):
    """The skip ratchet: tests/skip_ratchet.json holds the total SKIP count this runner last
    accepted, across every suite. A SKIP is an abstention, not a pass — today this file exits 0
    however many rows skip, and nothing catches that count creeping up. Same shape as check_roster
    and check_pass_fixture above: read the prior state, compare, refuse on regression.

    Three answers. No prior file (first run ever): seed it at the current count and say so — a
    cold start is not a regression, so it must not report red. The count held or fell: the file is
    the ratchet, so it is rewritten to the new, no-worse number — a shrink is never required, but
    it is always kept once it happens, or a later run at the old higher count would wrongly read as
    growth. The count rose: the run is refused, naming what grew and the before/after numbers — a
    weaker proof must not report green just because every suite that DID run happened to pass.

    Returns True when the run may go green on this account, False when it may not.
    """
    if not SKIP_RATCHET_PATH.exists():
        SKIP_RATCHET_PATH.write_text(json.dumps({"total_skips": total_skips}, indent=2) + "\n")
        print(f"\nskip ratchet · no prior tests/skip_ratchet.json — seeded at {total_skips} "
              f"skip(s), nothing to compare against yet")
        return True
    prior = json.loads(SKIP_RATCHET_PATH.read_text())["total_skips"]
    if total_skips > prior:
        print(f"\ngate · the skip ratchet — this run skipped {total_skips}, up from {prior} held "
              f"by tests/skip_ratchet.json. A SKIP is an abstention, not a pass: more of them means "
              f"fewer checks actually ran, so this run may not report green over that growth.")
        return False
    if total_skips < prior:
        print(f"\nskip ratchet · {total_skips} skip(s), down from {prior} — "
              f"tests/skip_ratchet.json lowered to match")
    SKIP_RATCHET_PATH.write_text(json.dumps({"total_skips": total_skips}, indent=2) + "\n")
    return True


def check_expected_red(failed):
    """S-26's third arm: compare this run's actually-red suites against EXPECTED_RED above.

    A suite in `failed` with no entry in EXPECTED_RED is a surprise regression — this run must not
    report green over it, so it is refused, naming the surprise. A suite named in EXPECTED_RED that
    came back green is only good news: it is printed so the entry can be retired, but it never
    fails the run on its own — expected-red suites already keep the run from going green on the
    account of their own row; nothing further is owed for one of them turning green.

    Returns True when this run may go green on this account, False when a surprise red stands.
    """
    surprises = [n for n in failed if n not in EXPECTED_RED]
    stale = [n for n in EXPECTED_RED if n not in failed]
    for n in stale:
        print(f"\nnote · {n} is in EXPECTED_RED ({EXPECTED_RED[n]}) but came back green this run "
              f"— consider removing it from EXPECTED_RED")
    if surprises:
        print(f"\ngate · {len(surprises)} suite(s) went red with no reason named in EXPECTED_RED: "
              f"{', '.join(surprises)}. Either fix them, or name each in EXPECTED_RED with why it "
              f"is red on purpose.")
        return False
    return True


def record_verdicts(results):
    """Write each suite's own verdict to tests/suite_verdicts.json, beside the timings and the
    ratchet this runner already keeps.

    It exists for a reader outside this tree: ~/tlvphotos/scripts/plan_checks.py computes a plan
    row's status at every session start, and a row whose criterion is "this suite passes" had no
    cheap way to ask. Asking whether the test FILE exists goes green on an empty file; running the
    suite from that table drives Chrome at every session start. This record is the third answer —
    the run that already happened says how it went, and the reader spends one file read.

    The entry is per suite and merged into whatever stands, rather than replacing the file: this
    runner's own invocation may cover a subset (the site's twin takes an `only` batch), and a suite
    absent from this run keeps the last verdict actually recorded for it. Each entry carries the
    head the tree stood on and when, so a reader can see a verdict is old without treating age as
    failure — nothing here judges staleness, it only records enough for someone else to.
    """
    head = subprocess.run(["git", "-C", str(HERE.parent), "rev-parse", "--short", "HEAD"],
                          capture_output=True, text=True)
    record = json.loads(VERDICTS_PATH.read_text()) if VERDICTS_PATH.exists() else {}
    when = time.strftime("%Y-%m-%d %H:%M")
    for name, (rc, _tail) in results.items():
        record[name] = {"passed": rc == 0,
                        "head": head.stdout.strip() or "unknown",
                        "when": when}
    VERDICTS_PATH.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")


def ordered_suites(suites):
    """Queue order: longest-first, from the last FULL run's recorded durations in
    tests/suite_timings.json. A suite absent from the record (never timed, e.g. brand new)
    sorts first — unknown cost is assumed expensive, so a new suite never lands at the tail
    behind a stale queue. With no record yet, keep today's declaration order exactly."""
    if not TIMINGS_PATH.exists():
        return list(suites)
    timings = json.loads(TIMINGS_PATH.read_text())
    unknown = [s for s in suites if s not in timings]
    known = sorted((s for s in suites if s in timings), key=lambda s: timings[s], reverse=True)
    return unknown + known


def stages_built_now():
    """How many distinct base stages the shared cache has ever baked, or None if it cannot say.

    `tests/engine_build.py` keeps one immutable stage per distinct bake request and hands every
    suite its own copy. Reading this number before and after a run is how a full gate proves
    STRUCTURALLY that it baked once rather than once per browser suite — a count of builds, never a
    count of seconds. A tree whose shim predates that cache answers None, and the run says so
    instead of printing a zero it cannot stand behind.
    """
    try:
        sys.path.insert(0, str(HERE))
        import engine_build
        return engine_build.stages_built()
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=("row", "integration", "release"), default="release",
                    help="row: this row's acceptance, the suites naming what changed, and the "
                         "architectural invariants. integration: that, plus every proof at each "
                         "layer the change touches. release (the default): the whole roster.")
    ap.add_argument("--acceptance", default="",
                    help="comma-separated suite names this row's own definition of done names")
    ap.add_argument("--changed", nargs="*", default=None,
                    help="the write-set: repo-relative paths this work actually changed. Given "
                         "explicitly rather than guessed; with none given, read off git.")
    # SEQUENTIAL BY DEFAULT, on his word of 06.09.2026: "запускается последовательно по умолчанию;
    # параллельность не должна быть способом «доказать под нагрузкой»". Eight Chromes on one machine
    # is a load test wearing a gate's clothes — it is how a suite comes back red for being crowded
    # rather than for being wrong, which is how this row's own predecessor (S-113) started. Asking
    # for parallelism is still allowed and still useful while work is in progress; it is never what a
    # verdict rests on.
    ap.add_argument("--jobs", type=int, default=1,
                    help="parallel suites (each spawns its own Chrome); default 1, one at a time")
    ap.add_argument("--no-record-timings", action="store_true",
                    help="run the full gate without rewriting suite_timings.json (release/CI)")
    args = ap.parse_args()

    # BEFORE A SINGLE SUITE IS SPAWNED. Both of these answer off a directory listing, and both make
    # a claim that already stands true rather than adding a new demand of anyone. THEY RUN IN EVERY
    # MODE: a narrow run over a wrong roster is as worthless as a full one.
    check_roster()
    check_pass_fixture()

    changed = args.changed
    if changed is None and args.mode != "release":
        done = subprocess.run(["git", "-C", str(HERE.parent), "diff", "--name-only", "HEAD"],
                              capture_output=True, text=True)
        changed = [ln for ln in done.stdout.splitlines() if ln.strip()]
        print(f"write-set · not given, so read off git: "
              f"{', '.join(changed) if changed else '(nothing uncommitted)'}")
    chosen, why, omitted = select(args.mode,
                                  [a.strip() for a in args.acceptance.split(",")],
                                  changed)

    # THE SELECTION IS ALWAYS PRINTED, WITH THE REASON EACH SUITE IS IN IT, and the omission is
    # printed too. A selector nobody can read is a selector that skips checks in silence, and the
    # whole point of naming modes was to stop that rather than to industrialise it.
    print(f"mode · {args.mode} · {len(chosen)} of {len(SUITES)} suite(s) selected")
    if args.mode != "release":
        # A release run's 123 identical reasons would be noise, and its omission is the empty set;
        # a narrow run's reasons are the whole point, so they print one to a line with the layer
        # each suite stands at.
        for s in chosen:
            print(f"  [{layer_of(s)}] {s}: {why[s]}")
    print("  " + (omitted or "left out: nothing — this selection is the whole roster"))
    stages_before = stages_built_now()

    t0 = time.time()
    queue = ordered_suites(chosen)
    running = {}    # name → Popen
    starts = {}     # name → monotonic start, paired at harvest for that suite's duration
    results = {}    # name → (rc, tail)
    durations = {}  # name → suite wall time in seconds
    logs = {}       # name → Path, this suite's combined stdout+stderr
    skips = {}      # name → this suite's own SKIP tally, for the ratchet below

    # Each child's output is captured to its own file, not a subprocess.PIPE: a pipe has a small
    # kernel buffer (~64KB), and nothing here reads it while the child runs — only poll() is
    # called until exit. A suite that prints more than that fill the pipe and blocks on write(),
    # while this process is blocked waiting for an exit that write() is blocked on: a deadlock. A
    # file has no such bound, so the child can never stall on it.
    log_dir = Path(tempfile.mkdtemp(prefix="run_all_logs_"))

    def harvest(block=False):
        for name, proc in list(running.items()):
            rc = proc.wait() if block else proc.poll()
            if rc is None:
                continue
            durations[name] = time.monotonic() - starts[name]
            out = logs[name].read_text(encoding="utf-8", errors="replace")
            lines = out.strip().splitlines()
            tail = lines[-1] if lines else "(no output)"
            skips[name] = suite_skip_count(out)
            # a RED suite keeps its whole verdict: the failing rows print with the gate line,
            # so the log itself says WHAT failed (never just the suite's name)
            if rc != 0:
                tail += "\n" + "\n".join("      " + l for l in lines if "FAIL" in l or "Traceback" in l or "Error" in l)
            results[name] = (rc, tail)
            del running[name]

    while queue or running:
        while queue and len(running) < args.jobs:
            name = queue.pop(0)
            starts[name] = time.monotonic()
            log_path = log_dir / f"{name}.log"
            logs[name] = log_path
            with open(log_path, "wb") as logf:
                running[name] = subprocess.Popen(
                    [sys.executable, str(HERE / f"test_{name}.py")],
                    stdout=logf, stderr=subprocess.STDOUT)
        harvest()
        time.sleep(0.2)
    harvest(block=True)
    shutil.rmtree(log_dir, ignore_errors=True)

    wall = time.time() - t0
    failed = [n for n in chosen if results[n][0] != 0]
    for n in chosen:
        rc, tail = results[n]
        print(f"[{'OK ' if rc == 0 else 'RED'}] {n}: {tail}")
    print(f"\n{len(chosen) - len(failed)}/{len(chosen)} suites green · wall {wall:.0f}s"
          + (f" · RED: {', '.join(failed)}" if failed else ""))

    # HOW MANY BASE STAGES THIS RUN HAD TO BAKE. Every browser suite stands on a copy of an immutable
    # stage the shared cache keeps, one per distinct bake request, so a full gate that reports ONE
    # here has proved structurally that it baked once and not once per suite. It is a count of
    # builds. Nothing here is a duration and nothing here is a budget: how fast this machine bakes is
    # the machine's business (plan row S-113).
    stages_after = stages_built_now()
    if stages_before is None or stages_after is None:
        print("\nbase stages · the shared stage cache could not be read, so this run cannot say how "
              "many stages it baked")
    else:
        print(f"\nbase stages · {stages_after - stages_before} baked by this run "
              f"({stages_after} distinct stages in the cache)")

    # Timing report: slowest suite first, so a stretched wall points straight at its cause. It is a
    # READING and never a gate: no row anywhere passes or fails on a number in this block.
    print("\nsuite timings, slowest first (a reading, never a gate):")
    for n in sorted(durations, key=durations.get, reverse=True):
        print(f"  {n}: {durations[n]:.1f}s")

    # ONLY A RELEASE RUN REWRITES THE RECORD, because only a release run covers the whole roster: a
    # narrow run's durations would leave every unrun suite's entry standing at its old value beside
    # a handful of fresh ones, and `ordered_suites` would then queue a stale mixture. The caller may
    # also decline the rewrite outright (release/CI, where a clean checkout should not get dirtied).
    if not args.no_record_timings and args.mode == "release":
        TIMINGS_PATH.write_text(json.dumps(durations, indent=2, sort_keys=True) + "\n")

    # Every run records its verdicts, including a run that goes red: a red verdict is the one a
    # reader most needs, and a record only written on green would read as "never run" for exactly
    # the suite that just failed.
    record_verdicts(results)

    # The skip ratchet runs AFTER every suite is harvested, because its number is the sum of what
    # every suite already reported of itself (see suite_skip_count()) — there is nothing to compare
    # until the whole run has spoken. It joins check_roster() and check_pass_fixture() in deciding
    # this run's exit code, same as any other gate here: a growth here is refused same as a RED
    # suite is, not layered on top as a separate kind of failure.
    # THE RATCHET IS A WHOLE-ROSTER FACT AND ONLY A RELEASE RUN HOLDS ONE. A narrow run's total is
    # lower simply because fewer suites spoke, and letting that lower the recorded number would make
    # the very next full run read as GROWTH and refuse itself. So a narrow run abstains out loud
    # rather than writing a number it cannot stand behind — and abstaining is not passing: the
    # ratchet's own claim is untouched and the next release run still answers for it.
    total_skips = sum(skips.values())
    if args.mode == "release":
        ratchet_ok = check_skip_ratchet(total_skips)
    else:
        ratchet_ok = True
        print(f"\nskip ratchet · not read: this run covered {len(chosen)} of {len(SUITES)} suites, "
              f"and the ratchet's number is the whole roster's. This run skipped {total_skips}; the "
              f"record is left exactly as it stood.")

    # EXPECTED_RED runs last, same reason as the skip ratchet: it reads what every suite already
    # reported of itself. A suite named in EXPECTED_RED keeps this run from going green on the
    # account of its own row without also being a fresh SystemExit-worthy surprise — only a red
    # suite with NO entry there is.
    expected_red_ok = check_expected_red(failed)

    sys.exit(1 if (not expected_red_ok or not ratchet_ok) else 0)


if __name__ == "__main__":
    main()
