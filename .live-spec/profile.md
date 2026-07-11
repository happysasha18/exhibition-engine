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
- `remote: exists` — origin = github.com/happysasha18/exhibition-engine, PRIVATE. The public-visibility
  flip waits on the owner's explicit word (recorded in NEXT_STEPS lane 1 and the run journal).

## Open lines — the owner's word is needed (HALTed at adoption, never invented)

- `project.kind: ⟨owner⟩` — ADOPT.md requires this and it is ALWAYS asked, never inferred (SPEC INV-36:
  no line may say what a host IS from examples). No recorded owner word covers it. The tree reads as a
  static gallery-site builder plus an adaptive-exhibition renderer with a guided-journey product vision
  (README/NEXT_STEPS), but the KIND line is the owner's to set.
- `budget.pressure: ⟨owner⟩` — the ECONOMY rung (full · lean · tight, SPEC T-19) has no host-scope
  recorded word for this host. Runs on the personal-profile default until the owner sets it here.
