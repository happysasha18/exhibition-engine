#!/usr/bin/env python3
"""S-115 — the route reads as an adventure between works, and the arsenal is honestly reachable.
Run: python3 tests/test_pass_route_direction.py

Root: his word of 07.09.2026 10:08. The route looks like a few repeated moves laid over a large
arsenal. The camera rarely reads as a live spatial gesture; parquet, the lattice and the colour
operations rarely reach the eye; polyphony sometimes exists on paper while the voices do not differ;
one gesture repeats under several names.

WHAT THIS FILE HOLDS, AND IT IS FOUR SEPARATE FACTS PER INSTRUMENT, never one. An instrument is NOT
"used" because a score names it. It is used when all four of these are true, and each of them fails
in its own way:

  1. the chooser can actually cast it at runtime, over a corpus the collection does not decide;
  2. what it is cast with carries at least one handle away from its own published neutral;
  3. that handle reaches the renderer, read off the instrument's own applied row;
  4. a viewer can see a distinguishable gesture at the passage's peak, read off pixels.

A file that checked only the first would report a full arsenal over a route where nothing moves. The
rows below are grouped by which of the four they answer, and each says which.

This file is being built under S-115 and its rows arrive in stages; a stage not yet written prints as
a SKIP naming what it is waiting for, never as a green.
"""
import sys

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


skip("ROUTE the arsenal's four facts, instrument by instrument",
     "S-115 stage 1 — the audit harness is not written yet")

passed = sum(1 for _, s, _ in results if s == "PASS")
failed = sum(1 for _, s, _ in results if s == "FAIL")
skipped = sum(1 for _, s, _ in results if s == "SKIP")
print()
for name, status, detail in results:
    print(f"{status:5s} {name}   — {detail}")
print(f"\n{passed} passed / {failed} failed / {skipped} skipped")
sys.exit(1 if failed else 0)
