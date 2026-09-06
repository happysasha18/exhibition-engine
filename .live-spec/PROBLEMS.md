# PROBLEMS — exhibition-engine

Seeded at first adoption (2026-07-12) from issues already documented in the tree. Each line cites where
the evidence lives; nothing here is asserted from memory.

- WATCHED 2026-09-06 ~21:39 · `pass_seam`'s interruption-cadence row reds inside the full sequential
  gate and passes alone. The gate at `2025333` read 121/122 with `pass_seam` 26 passed / 1 failed:
  "no cadence frame was caught: {'got': True, 'took': True, 'gen': 30} running=True box=None
  report={'cadence': None, 'state': 'idle'}". The same suite run alone on the same commit read
  27 passed / 0 failed, and that run's own line says the cadence landed on door «out» in 2026 ms
  against the score's declared interruption window of 2000 ms. So the row's pass rests on the host
  reaching its own door inside a window it clears by 26 ms on a quiet machine. The row cuts the
  passage after 1.5 s of WALL time (`CUT_AT`) with the clock deliberately unpinned, which is what
  makes it read differently on a busy machine. Parked, not dammed, per the same treatment the
  2026-07-12 glide-timing entry below got: a re-run gates any commit, and a SECOND occurrence owns
  it with a cut driven by the passage's own progress rather than by wall time. What must NOT be
  done to it is widening the 2000 ms: that is the builder's clock deciding a product law, which
  plan row S-113 exists to remove. Source: this session's own two sequential runs, logs in the
  session scratchpad, and `tests/test_pass_seam.py:930-960`.

- OWNER-ROW 2026-07-10 · `tests/make_synthetic.py` is STALE and destructive — running it emits a smaller
  `greetings.json` (drops `quiz_ask`/`gift_*`/`enjoy`) and unexpectedly rewrites `engine/harness/headless.py`
  and a `tokens.css`; it already clobbered an uncommitted harness fix once. Fix owed: bring the generator
  back in sync with the fixture it claims to generate, and stop it writing outside the fixture tree.
  Source: NEXT_STEPS.md lane 5.
- WATCHED 2026-07-12 · glide-timing flake under full-suite CPU load — the full `run_all.py` reported
  `RED: glide` (26/27 green), but `tests/test_glide.py` in isolation passed 12/12 immediately after. Same
  flaky-harness family the pair's other host documented (animation-timing face; RED once under load, green
  alone). Parked, not dammed: a re-run gates any commit; if it fires a SECOND time on this host, own it
  with a glide-suite settle poll. Source: this adoption run's `.venv/bin/python tests/run_all.py` +
  isolation re-run.
- RESOLVED 2026-07-12 (was WATCHED 2026-07-10) · residual bare word `tlvphoto` in `SPEC.md` (7
  occurrences) — provenance/example text carried from the private instance, left in place during the
  publish scrub (NOT in that sweep's target set) and flagged to the owner. Not a defect in behaviour; a
  publish-hygiene item for the public flip. Fixed in commit `1fbf763`: heading + every provenance cite
  now uses the engine's own public commits, no instance crowned. Source: `.publish-pass-checkpoint.md`
  notes + `grep -c tlvphoto SPEC.md`.

- 2026-07-12 · env drift: a build worker installed Pillow 11.3.0 into this repo's .venv mid-run (the ladder browser rows need it; without it they pin to SKIP). The dependency is real and now present; the drift to watch: the venv's package set is not recorded anywhere — a fresh machine re-hits the silent SKIP. Owner row candidate: record/require test deps explicitly.
