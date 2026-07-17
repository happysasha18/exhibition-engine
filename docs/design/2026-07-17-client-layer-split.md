# Client layer split — plan of record (2026-07-17)

The client `engine/assets/exhibition.js` (~4000 lines) is one async IIFE. The owner asked to split it
into layers. This note is the plan a later refactor run executes. Classified **refactor / infra**:
behaviour is preserved and proven, not changed.

## The shape that decides everything

The whole client is a single closure with pervasive shared state and deliberate forward references
(handlers run after full evaluation, so `pulse()` can read `abArms`/`storyVariant`/`quizStage` declared
later). Reordering declarations is the risk. Slicing the file in place is safe. Two build-time consumers
read the file as a string: `build.py` (cache-bust hash, `@@NS@@` namespace substitution, engine-vs-instance
identity check) and nine test suites that read the source path directly. So the served artifact stays one
file.

## Mechanism

The served `engine/assets/exhibition.js` stays a **committed, generated** file. Add:

- `engine/client/` — ordered raw line-slice fragments (`00-prelude.js` … `98-sound.js`, `99-close.js`), no
  wrappers or headers so the join is byte-identical.
- `engine/assemble_client.py` — reads an explicit ordered manifest (a list, not a glob), joins with `""`,
  writes `exhibition.js`.
- `tests/test_assembly.py` — re-assembles in a temp dir and asserts byte-equality with the committed file;
  added to `run_all.py` SUITES and `guardrails/pre-push`. Drift reds the gate.

`build.py` is untouched: the `@@NS@@` tokens live inside fragments and ride the join verbatim; the hash and
identity seams keep working; the nine source-reading suites keep working. Zero build.py churn, zero test churn.

## The twenty latent layers

Prelude/pulse-core (1–230) · knobs/language/history (232–341) · kinship data + orderings (343–441) ·
quiz seed + A/B frame + story flags (443–555) · arrival facts + assembleOrder (557–603) · door dealing +
circle + layout + walk state (605–906) · ground tone + load ladder + preload + door warm (908–1140) ·
door face + ceremony + crossing + popstate (1142–1636) · plaque/caption/io observer (1638–1798) · story
voice (1800–1921) · share + toast (1923–1989) · protect + gift (1991–2111) · zoom/inspect + grab guard +
pinch refusal (2113–2661) · quiz card (2663–2893) · walk render (2895–2951) · motion: glide + chrome guard +
wheel + keys + touch (2953–3366) · renderHang + series room (3368–3555) · place/hash-arrival/boot (3557–3652) ·
i18n + visitor memory + language mark (3654–3848) · sound player (3850–4016).

## Couplings that resist a clean cut (kept honest)

1. The walk-state triple `pick/order/shown` (885–906) is its own micro-layer — written and read across many.
2. The ceremony lock `busy`/`cerGen`/`veil` (1372–1389) is shared by the door crossing and the series room.
3. The face registry: `faceStands()` hardcodes six flags owned by five layers; the motion layer reads
   everyone's flags. A registry (`registerFace`) is a later, byte-changing step.
4. The IntersectionObserver (1654–1713) is a hub touching eight concerns; it lives in one slice, others accept it.
5. Quiz, story, and protect are each 2–3 non-contiguous islands and stay that way.
6. `@@NS@@` in identifier position means no fragment is parseable JS before substitution — no per-file linting.

## Staged order (one commit each, suite green + byte-parity between every pair)

1. Scaffolding: empty-manifest assembler + `test_assembly.py` + SUITES entry + pre-push line.
2. Sound (3850–4016) — already a self-contained nested IIFE, the safest first cut and the template.
3. i18n/memory/lang, then place/hash/boot.
4. renderHang + series. 5. motion (keep the `wheelWalkStep` block whole — `test_wheel` extracts it).
6. quiz card, walk render. 7. zoom/protect/input. 8. share/toast, gift. 9. plaque/io, story voice.
10. door face (the riskiest region, done once the process is drilled). 11. door deal + walk-state,
ground/ladder. 12. the head (knobs, data, quiz-seed, prelude, close) last — monolith gone.
13. Optional, each its own spec'd change: face registry, an explicit state object, a GENERATED banner.

## Proof

Every slicing commit: `assemble_client.py && git diff --exit-code exhibition.js` — the assembled file is
byte-identical (shasum before/after recorded). Since build bakes from the same bytes, every baked bundle is
byte-identical for every flag combination by construction. Full suite green identically at each commit. A
later byte-changing step proves by the full suite green plus a before/after bundle `diff -r` whose only
permitted delta is exhibition.js and its `?v=` hash.

## What the split does NOT buy (honest limit)

Not real modules — fragments still share one closure, so a variable typo still resolves against the whole
scope. No per-file lintability (the `@@NS@@` tokens forbid it). The three tangled concerns (quiz, story,
protect) stay multi-fragment. What it buys: ~20 files of one concern each, a provably-identical serving
artifact at every step, and a scaffold for the real decouplings later, one at a time, with the suite as judge.
