# exhibition-engine — host profile (live-spec settings ladder, host scope)

Host overrides only. Settings about the human (language, proactivity) live in the personal profile
(`~/.claude/live-spec/profile.md`), which this host file overrides per the settings ladder (SPEC E-13).
Mode/trust move only on the owner's word (INV-9).

- `spec.file: SPEC.md` — this host keeps ONE condensed spec named `SPEC.md` (not `PRODUCT_SPEC.md`);
  every pack guide reads "PRODUCT_SPEC.md" as this file (SPEC canonical-set rule). Present in the tree
  at adoption (1175 lines, 112 distinct INV/EX anchors). The single-condensed-doc shape (no separate
  ARCHITECTURE.md / TEST_MATRIX.md / ROADMAP.md / JOURNAL.md) is a deliberate host deviation, recorded
  as named catch-up rows — splitting the docs is a future owner-gated row, not an empty-shell now.
- `push.self-certify: on` — pushes run on the agent's OWN certification once the suite log's own tail
  reads all-green (owner's word 2026-07-10, «пуш делай сам»). Suite command:
  `.venv/bin/python tests/run_all.py` — with no `--mode` that is the RELEASE gate, the full roster,
  which is what a push certifies on. The two narrower modes (`--mode row`, `--mode integration`) name
  what they left out and why, and they are for work in progress, never for a push. The suite count is
  not written down here on purpose: the roster gate reads it off disk (`check_roster`), and a number
  in prose beside it would be a second, drifting copy. Skips are held by the ratchet, not by a
  sentence naming which ones are expected.
  This host still NEVER pushes on this record alone during an adoption run — the adoption commit stays
  local (worker discipline).
- `revert.states-its-reason: required` — A REVERT OF SUBSTANTIVE WORK STATES ITS REASON, in the commit
  message, in the revert's own words. `git revert`'s boilerplate ("Revert «…». This reverts commit …")
  says only what was undone and never why, and a bare revert is indistinguishable from an accident:
  the next reader cannot tell a repair from a regression, and the work has to be re-derived from
  scratch before anyone can decide whether it should stand. One sentence closes that — what went
  wrong, and what would have to be true to land it again. This binds the revert alone, not the
  original commit, and it is a rule about the MESSAGE and never a gate on the act: reverting fast is
  often right, and saying why costs a line. Written 2026-09-01 on the V2 convergence plan's Phase 5
  item 3, after two substantive breadth commits (`3b8cb45`, `d4d21ed`) were reverted the same night
  with git boilerplate and no stated reason, and a later phase had to re-read both diffs to work out
  whether either should come back. (The plan named "the engine's own contributing norms" as the home
  for this rule; no such document exists in this tree, and this file is where the sibling rule
  `push.self-certify` already stands, so it lands here.)
- `remote: exists` — origin = github.com/happysasha18/exhibition-engine, PRIVATE. The public-visibility
  flip waits on the owner's explicit word (recorded in NEXT_STEPS lane 1 and the run journal).

- `project.kind: reusable browser-based generative exhibition/rendering engine with a static site
  shell, compile-time per-image WorkRecords, and runtime WebGL composition` — the owner's own word,
  06.09.2026, given verbatim and recorded verbatim. It stood open as `⟨owner⟩` from adoption until
  that day, because ADOPT.md asks this line and never infers it (SPEC INV-36: no line may say what a
  host IS from examples).

## The five proof layers

WHAT THIS SECTION IS FOR. A project of the kind above proves different facts by very different
means, and until 06.09.2026 it had no word for that difference — so `TEST_MATRIX.md`'s catalogue of
requirements was being read as an obligation to drive every browser in the roster after any change
at all. A catalogue of requirements and their proofs is not a list of runs owed after every commit.
These five names say what KIND of proof a fact needs, and `TEST_MATRIX.md` and `tests/run_all.py`
carry the same five in the same words, so the three documents cannot drift into three vocabularies.

1. **static/source contract** — the fact stands in the source and is read off it: a declaration, a
   roster, a manifest, a shape, a name. No process is started to prove it.
2. **pure Node/function composition** — the fact is a function of its inputs and is proven by running
   the REAL shipped block in Node against inputs the test states. No browser is part of the claim.
3. **browser runtime contract** — the fact is about what the page's own runtime does: state, events,
   the host's own report, what a module publishes at load. A browser is needed; pixels are not.
4. **pixel/WebGL/layout/interaction** — the fact is about the picture or the hand: a real render path,
   a pixel landing, camera and canvas geometry, touch and mouse, DOM layout, context loss and
   fallback. Only a real browser can answer it.
5. **live-device runtime observation** — the fact is about a real device and is read in the visitor's
   own browser after a deploy (`lab/perf.html`, `lab/perf-serve.py`). No suite in this tree answers
   for it and none may pretend to: the builder host is never the device (S-113).

A browser is owed ONLY by layers 3 and 4 — that is, only where the assertion is genuinely about DOM,
WebGL, canvas, a gesture, layout or a pixel landing. A fact that is legality, ranking, tier
selection, voices and roles, handle derivation, a measurement read, a deterministic seed or a
route-memory decision is layer 2, and putting it in a browser proves nothing extra and costs a Chrome.

## Open lines — the owner's word is needed (HALTed at adoption, never invented)

- `budget.pressure: ⟨owner⟩` — the ECONOMY rung (full · lean · tight, SPEC T-19) has no host-scope
  recorded word for this host. Runs on the personal-profile default until the owner sets it here.
