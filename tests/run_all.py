#!/usr/bin/env python3
"""The one gate command — run every suite in parallel (E3).

Adapted from ~/tlvphoto/tests/run_all.py for exhibition-engine.
Each suite is isolated (its own baked TMP, its own http port, its own headless Chrome).

Usage: python tests/run_all.py [--jobs 4]
Exit 0 only if EVERY suite exits 0.
"""
import argparse
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent

# SUITES must match the set of test_*.py files in tests/ exactly (gate INV-5r).
# Add a suite name here AS SOON as tests/test_<name>.py is created.
SUITES = [
    "site", "exhibition", "door", "vector", "back", "greet",
    "series", "motion", "reset", "load", "share", "glide",
    "pulse", "hand", "i18n", "lang", "memory",
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=4,
                    help="parallel suites (each spawns its own Chrome); default 4")
    args = ap.parse_args()

    t0 = time.time()
    queue = list(SUITES)
    running = {}    # name → Popen
    results = {}    # name → (rc, tail)

    def harvest(block=False):
        for name, proc in list(running.items()):
            rc = proc.wait() if block else proc.poll()
            if rc is None:
                continue
            out = proc.stdout.read().decode(errors="replace")
            tail = out.strip().splitlines()[-1] if out.strip() else "(no output)"
            results[name] = (rc, tail)
            del running[name]

    while queue or running:
        while queue and len(running) < args.jobs:
            name = queue.pop(0)
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
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
