#!/usr/bin/env python3
"""The one gate command — run every suite in parallel (E3).

Adapted from the reference instance's run_all.py for exhibition-engine.
Each suite is isolated (its own baked TMP, its own http port, its own headless Chrome).

Usage: python tests/run_all.py [--jobs 8]
Exit 0 only if EVERY suite exits 0.
"""
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
TIMINGS_PATH = HERE / "suite_timings.json"

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
    "pass_matter",
    "pass_gears",
    "pass_stack",
    "pass_pack",
    "pass_adrift",
    "pass_unfold",
    "pass_coverage",
    "pass_composed",
    "pass_memory",
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
]


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


def ordered_suites():
    """Queue order: longest-first, from the last FULL run's recorded durations in
    tests/suite_timings.json. A suite absent from the record (never timed, e.g. brand new)
    sorts first — unknown cost is assumed expensive, so a new suite never lands at the tail
    behind a stale queue. With no record yet, keep today's declaration order exactly."""
    if not TIMINGS_PATH.exists():
        return list(SUITES)
    timings = json.loads(TIMINGS_PATH.read_text())
    unknown = [s for s in SUITES if s not in timings]
    known = sorted((s for s in SUITES if s in timings), key=lambda s: timings[s], reverse=True)
    return unknown + known


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=8,
                    help="parallel suites (each spawns its own Chrome); default 8")
    ap.add_argument("--no-record-timings", action="store_true",
                    help="run the full gate without rewriting suite_timings.json (release/CI)")
    args = ap.parse_args()

    # BEFORE A SINGLE SUITE IS SPAWNED. Both of these answer off a directory listing, and both make
    # a claim that already stands true rather than adding a new demand of anyone.
    check_roster()
    check_pass_fixture()

    t0 = time.time()
    queue = ordered_suites()
    running = {}    # name → Popen
    starts = {}     # name → monotonic start, paired at harvest for that suite's duration
    results = {}    # name → (rc, tail)
    durations = {}  # name → suite wall time in seconds
    logs = {}       # name → Path, this suite's combined stdout+stderr

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
    failed = [n for n in SUITES if results[n][0] != 0]
    for n in SUITES:
        rc, tail = results[n]
        print(f"[{'OK ' if rc == 0 else 'RED'}] {n}: {tail}")
    print(f"\n{len(SUITES) - len(failed)}/{len(SUITES)} suites green · wall {wall:.0f}s"
          + (f" · RED: {', '.join(failed)}" if failed else ""))

    # Timing report: slowest suite first, so a stretched wall points straight at its cause.
    print("\nsuite timings, slowest first:")
    for n in sorted(durations, key=durations.get, reverse=True):
        print(f"  {n}: {durations[n]:.1f}s")

    # This runner has no suite-selection flag — every invocation covers the full SUITES set, so
    # every run is a FULL run and the committed record is always safe to replace here, unless the
    # caller asked to skip the rewrite (release/CI, where a clean checkout shouldn't get dirtied).
    if not args.no_record_timings:
        TIMINGS_PATH.write_text(json.dumps(durations, indent=2, sort_keys=True) + "\n")

    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
