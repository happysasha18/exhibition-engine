# exhibition-engine — NEXT STEPS (resume file)

_The generic engine behind an adaptive photography-exhibition site. It was extracted from a
private production instance and founded as its own product: a static gallery-site builder plus an
adaptive-exhibition renderer, with the guided-journey product vision below. Method: the live-spec
pack, loaded per session._

## RESUME NOW — cutover done; the engine is the sole baker of the production instance

The production instance now bakes only through this engine: its `deploy.sh` calls
`engine/build.py --content . --site site.json`. Proof at cutover, all fresh: the instance suite
green, this engine's suite green, and a byte-diff of the engine bake against the instance's own
prior bake was EMPTY. The instance lives in its own private repo; this repo is being prepared to
go PUBLIC.

**LANES (in order):**
1. **Publish pass (before the visibility flip — the owner's word flips it):** scrub the working
   docs of personal name and machine paths; make `example/site.json` a synthetic example (the real
   identity lives in the instance repo); rewrite `README.md` per the publish gate; neutralize the
   personal comments in `build.py` / `exhibition.js`. License is the owner's call.
   _Status: in progress (this pass)._
2. **Reverse the code flow:** point the instance's tests at the engine bake, retire the instance's
   own legacy `build_site.py`.
3. **Own-client lane (not blocking):** align `tests/quiz_util.py` `arm_of()` with the client's own
   `quizHash` (they currently disagree — the util keeps an older avalanche formula while the client
   draws the arm with a Knuth-finalizer hash; same token, different arm) and add a JS↔Python parity
   test; generalize residual instance-prefixed localStorage keys in the client; catch the generic
   client up to the instance client (header FOUC guard, single-answer worker model).
4. **`story_notes.json` staleness watch:** the instance's story-notes file is a mapped snapshot of
   authored labels; if the labels change, regenerate it (the byte-proof catches drift in `_worker.js`).

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
