# PROBLEMS — exhibition-engine

Seeded at first adoption (2026-07-12) from issues already documented in the tree. Each line cites where
the evidence lives; nothing here is asserted from memory.

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
