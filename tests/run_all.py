#!/usr/bin/env python3
"""The one gate command — run every suite in parallel (E3).

Adapted from the reference instance's run_all.py for exhibition-engine.
Each suite is isolated (its own baked TMP, its own http port, its own headless Chrome).

Usage: python tests/run_all.py [--jobs 8]
Exit 0 only if EVERY suite exits 0.
"""
import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
TIMINGS_PATH = HERE / "suite_timings.json"

# SUITES must match the set of test_*.py files in tests/ exactly (gate INV-5r).
# Add a suite name here AS SOON as tests/test_<name>.py is created.
SUITES = [
    "site", "exhibition", "door", "vector", "back", "greet",
    "series", "motion", "consistency", "reset", "load", "ladder", "share", "glide",
    "pulse", "hand", "i18n", "lang", "lang_geo", "memory", "protect", "sound", "guard", "quiz",
    "quiz_copy", "shim", "compose", "dead", "quiz_flow", "parity", "zoom", "return", "gesture",
    "wheel", "glide_speed", "ratchet_lock", "beat_css", "assembly", "a11y", "about", "budget",
    "harness_drift", "story_edge", "story_lead", "pass", "pass_api", "pass_weave", "pass_drivers",
]


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
    args = ap.parse_args()

    t0 = time.time()
    queue = ordered_suites()
    running = {}    # name → Popen
    starts = {}     # name → monotonic start, paired at harvest for that suite's duration
    results = {}    # name → (rc, tail)
    durations = {}  # name → suite wall time in seconds

    def harvest(block=False):
        for name, proc in list(running.items()):
            rc = proc.wait() if block else proc.poll()
            if rc is None:
                continue
            durations[name] = time.monotonic() - starts[name]
            out = proc.stdout.read().decode(errors="replace")
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
            running[name] = subprocess.Popen(
                [sys.executable, str(HERE / f"test_{name}.py")],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        harvest()
        time.sleep(0.2)
    harvest(block=True)

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
    # every run is a FULL run and the committed record is always safe to replace here.
    TIMINGS_PATH.write_text(json.dumps(durations, indent=2, sort_keys=True) + "\n")

    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
