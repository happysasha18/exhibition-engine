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
  `.venv/bin/python tests/run_all.py` (27 suites; one pinned compose CH6 skip at 1280px is expected).
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

## Open lines — the owner's word is needed (HALTed at adoption, never invented)

- `project.kind: ⟨owner⟩` — ADOPT.md requires this and it is ALWAYS asked, never inferred (SPEC INV-36:
  no line may say what a host IS from examples). No recorded owner word covers it. The tree reads as a
  static gallery-site builder plus an adaptive-exhibition renderer with a guided-journey product vision
  (README/NEXT_STEPS), but the KIND line is the owner's to set.
- `budget.pressure: ⟨owner⟩` — the ECONOMY rung (full · lean · tight, SPEC T-19) has no host-scope
  recorded word for this host. Runs on the personal-profile default until the owner sets it here.
