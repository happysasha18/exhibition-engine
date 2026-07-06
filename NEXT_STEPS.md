# exhibition-engine — NEXT STEPS (resume file)

_The GENERIC engine behind tlvphotos.com, founded as its own PRODUCT on Alexander's word
(2026-07-07 ~00:30): «движок должен быть генерный… установка Ollama, определение осей — весь
процесс объяснить пользователю и провести пользователя. Это огромное движение.» Named by his
decision answer: **exhibition-engine**. Method: the live-spec pack, loaded per session._

## LIVE STATE (2026-07-07 night — FOUNDED as a lane beside tlvphoto)

- Repo renamed `~/gallery-engine` → `~/exhibition-engine` (his name). Born 2026-07-06 morning as a
  byte-identical extraction (`1e65222`); tlvphoto then landed A DAY of changes — the drift list
  lives at `~/tlvphoto/docs/engine-drift-2026-07-07.md` (worker-made, senior-verified).
- Tonight's re-sync: the walk's client assets (exhibition.js/css, worker.js, the headless harness)
  copied VERBATIM from tlvphoto (worker run, md5-verified — see CHECKPOINT.md). NOT yet re-proven
  as a byte-identical bake — build.py generalization is the real work (below).
- **The two-lane law (his word):** tlvphoto keeps living on its own scripts; the engine grows
  BESIDE it; the transition happens once, deliberately — see TRANSITION.md. Nothing in tlvphoto
  points at the engine yet.

## THE PRODUCT (his vision, captured 2026-07-07 — the spec grows from THIS)

Not a code dump — **a guided journey**: a photographer with an archive is TAKEN BY THE HAND
end-to-end, each stage EXPLAINED before it runs:
1. install the local model runtime (Ollama) — why, what it costs, what it enables;
2. ingest the archive (export → catalog → dedup) — the user understands what the engine learned;
3. **define the axes** — the feature vocabulary of THEIR photography (the engine proposes,
   measures, shows; the human names and curates — the tlvphoto axis journey, productized);
4. pick finalists, curate the door pool;
5. bake the exhibition (door → hang → walk, all of tonight's tlvphoto behaviors) and deploy.
The design-spec workflow (norm cards, prototypes) rides the method. Every step: plain words,
a checkpoint, resumable. The engine ships with the live-spec method as its working skeleton.

## FORWARD QUEUE (each row = one story via the pipeline; E-rows)

E1. **Adopt the method IN this repo** — live-spec adoption pass: SPEC.md seed (the journey above
    as scenarios), ARCHITECTURE skeleton, TEST_MATRIX seed, its own `.live-spec/` profile. The
    founding kind question rides here (recommendation: a guided generator — CLI + skill hybrid).
E2. **build.py absorbs tlvphoto's day** — generalize what the instance hardcoded tonight
    (copyright line, clean addresses, i18n source/worker emission, consent snippet, config flags)
    behind the五 instance strings contract; re-prove the bake BYTE-IDENTICAL against tlvphoto's
    own (the drift report's re-sync list is the checklist).
E3. **The engine's own test suite** — adopt tlvphoto's 13 suites with an engine-side import shim
    + fixture content (a tiny synthetic archive, clearly labelled), so the engine is green
    WITHOUT Alexander's private content.
E4. **The guided journey, stage 1–2** (runtime + ingest): the explain-then-run walkthrough
    (CLI prompts or a local page), Ollama install check, archive contract.
E5. **The guided journey, stage 3** (axes): productize the axis definition/measure/curate loop —
    the heart; needs its own spec movement + prototypes.
E6. **Design-spec workflow** — how a user's norm cards/prototypes enter their instance.
E7. **Publish gate + GitHub public** (the publish skill walk; his word before anything goes out).
E8. **TRANSITION** — tlvphoto adopts the engine (see TRANSITION.md; his word opens it).

## Resume cold
Read this file + CHECKPOINT.md + ~/tlvphoto/docs/engine-drift-2026-07-07.md. The engine bakes
with `engine/build.py --content <dir>`; tlvphoto content = `~/tlvphoto`. Suite: none yet (E3).
Method: load the live-spec pack (`~/.claude/skills/live-spec-base` + working skills) per session.
