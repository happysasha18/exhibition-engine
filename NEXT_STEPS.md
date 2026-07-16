# exhibition-engine — NEXT STEPS (resume file)

_The generic engine behind an adaptive photography-exhibition site. It was extracted from a
private production instance and founded as its own product: a static gallery-site builder plus an
adaptive-exhibition renderer, with the guided-journey product vision below. Method: the live-spec
pack, loaded per session._

## 2026-07-16 (evening, second landing) — the variant frame (EX-AB / INV-90 / INV-91)

The experiment frame is engine-generic now: the served `experiments` registry (arms · flag · metric ·
salt) deals each visitor one arm at boot, synchronously ahead of any beat, off the visitor seed (the
seed read mints the coat-check token when none exists — this closed a real visit-1→2 arm-flip); every
dealt arm and the declared story variant ride EVERY registry beat as dimensions; `validate_experiments`
in build.py refuses a degenerate registry (under two arms, a salt collision). quiz_arm rides the frame
with its salt/split pinned. Tests: test_pulse 13/13 (4 new browser rows), test_compose VF5a/b; suite
32/32. The read side stays instance-owned (tlvphotos ga_report/morning meter, INV-92 there). SPEC:
"Experiments — the variant frame" + prover/design-review records dated 2026-07-16.

## 2026-07-16 (evening) — the pack's push gates adopted

The live-spec 2.1.0 ratchet kit is vendored here (`scripts/spec-style-lint.py` and kin, source-pin
manifest at `scripts/ratchet-manifest.json`): SPEC.md is the gated doc, caps seeded at adoption
(26 style errors / 10 redundancy-open) — growth past that size reds, the backlog never blocks.
`tests/test_ratchet_lock.py` joined SUITES (it self-runs pytest; a `--force` ratchet re-install
rewrites the file — re-append its `__main__` block). The repo's first pre-push hook is wired:
`guardrails/pre-push` runs gate m (the vendored `check-muted-launch.sh`, INV-157 — the harness
already launches muted) and gate r (the ratchet caps); the full browser suite stays the standing
manual commit gate. The instance repo (tlvphotos) adopted the same gates the same evening.

## RESUME NOW — cutover done; the engine is the sole baker of the production instance

The production instance now bakes only through this engine: its `deploy.sh` calls
`engine/build.py --content . --site site.json`. Proof at cutover, all fresh: the instance suite
green, this engine's suite green, and a byte-diff of the engine bake against the instance's own
prior bake was EMPTY. The instance lives in its own private repo; this repo is being prepared to
go PUBLIC.

**LANES (in order):**
1. **Publish pass — DONE 2026-07-10 (docs scrubbed, synthetic example, README per the publish gate,
   MIT license added on the owner's default call).** The visibility flip itself waits on the owner's
   word; the plan on his word is a fresh public history (one starting commit from the current tree;
   the full history stays private).
2. **Reverse the code flow — DONE 2026-07-10 (in the instance repo):** its tests bake via this
   engine through one shared helper; its legacy `build_site.py` is retired.
3. **Own-client lane — DONE 2026-07-10:** `EXQuiz._hash` exported, the test util mirrors the
   client's exact hash, a JS↔Python parity suite guards the seam (suite is now 26); residual
   instance prefixes generalized to `ex.*`; the FOUC guard and the single-answer judge were verified
   already present (only a stale comment corrected).
4. **`story_notes.json` staleness watch (unchanged):** the instance's story-notes file is a mapped
   snapshot of authored labels; if the labels change, regenerate it (the byte-proof catches drift
   in `_worker.js`).
5. **NEW — `tests/make_synthetic.py` is STALE and destructive (found 2026-07-10):** running it
   emits a smaller `greetings.json` (drops `quiz_ask`/`gift_*`/`enjoy`) and unexpectedly rewrites
   `engine/harness/headless.py` and a `tokens.css`; it already clobbered an uncommitted harness fix
   once. Owner row: bring the generator back in sync with the fixture it claims to generate, and
   stop it writing outside the fixture tree.

## The product (the vision the spec grows from)

Not a code dump — a guided journey. A photographer with an archive is taken by the hand end to end,
each stage explained before it runs:
1. install the local model runtime (Ollama) — why, what it costs, what it enables;
2. ingest the archive (export → catalog → dedup) — the user understands what the engine learned;
3. define the axes — the feature vocabulary of their own photography (the engine proposes, measures,
   and shows the distribution; the human names and curates);
4. pick finalists and curate the door pool;
5. bake the exhibition (door → hang → walk) and deploy.

Every step is plain words, a checkpoint, and resumable. The engine ships with the live-spec method
as its working skeleton.

## Forward queue (each row = one story via the pipeline)

- **E4. Guided journey, stages 1–2 (runtime + ingest):** the explain-then-run walkthrough (CLI
  prompts or a local page), an Ollama install check, and the archive content-contract.
- **E5. Guided journey, stage 3 (axes):** productize the axis definition/measure/curate loop — the
  heart of the journey; needs its own spec movement and prototypes.
- **E6. Design-spec workflow:** how a user's look-and-feel prototypes enter their instance.
- **E7. Publish gate + public repo:** the publish-skill walk (the owner's word before anything goes
  out). _In progress._
- **E8. Transition:** the production instance adopts the engine end to end (mostly landed at
  cutover; the reverse code-flow in lane 2 finishes it).

## Resume cold

Read this file, `SPEC.md`, and the test suite. The engine bakes with
`engine/build.py --content <content-dir> --site <site.json>`; see `README.md` for the full command
and the content contract. Run the suite with `.venv/bin/python tests/run_all.py`. Method: load the
live-spec pack (`live-spec-base` plus the working skills) per session.
