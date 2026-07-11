# Adoption plan & run record — exhibition-engine → live-spec (2026-07-12, first adoption)

Route: the engine host had NO `.live-spec/` records → UNDER-ATTACHED → this is the FIRST adoption
(ADOPT.md), not the catch-up walk (MIGRATION.md). The pair's other half, tlvphotos, already named this
debt in its own catch-up plan ("The engine half … per pair routing it is UNDER-ATTACHED: its walk opens
with full adoption … its own plan, its own gate"). Worker session; adoption commit stays LOCAL (no push).

The engine is a WELL-RUN host authored in the method — git with a clean baseline, a condensed `SPEC.md`
(112 anchors), a real 27-suite browser harness, and a `NEXT_STEPS.md` resume file. Per ADOPT.md Phase 3,
a host already in live-spec shape is NOT rewritten: adoption is light and births only the records the
host owes. Nothing in the host tree was moved or deleted (INV-7); no host `.md` was edited.

## Walk of ADOPT.md, phase by phase (each with its done-state as met here)

- Phase 0 (version-control gate): MET before the run — git repo on `main`, 70 commits, clean baseline
  `63b74b5`, heavy artifacts already gitignored (`.venv/`, `__pycache__/`, `*.pyc`). Remote OUTCOME =
  EXISTS: `github.com/happysasha18/exhibition-engine` (PRIVATE; public flip owner-gated). Recorded.
- Phase 0.5 (cruft sweep): not executed — no owner OK to delete, and no obvious regenerable junk beyond
  the already-ignored caches. Offer left to the owner; deletion without the OK is not taken.
- Phase 1 (orient): personal profile FOUND and loaded (`~/.claude/live-spec/profile.md`). Founding
  questions that a worker cannot answer are HALTed as open host-profile lines (see HALTs below). Existing
  docs read: SPEC.md, README.md, NEXT_STEPS.md, `.publish-pass-checkpoint.md` — all CURRENT and already in
  method shape; no re-engineering backlog.
- Phase 2 (inventory): surfaces + entities recorded in the pre-inventory (from `find`/`grep`, not the old
  prose). SURFACE_REGISTRY.md executable gate does NOT yet exist → gap row.
- Phase 3 (re-engineer docs): NOT NEEDED — the canonical claims already live in `SPEC.md`, native to the
  method. The host deliberately folds ARCHITECTURE / TEST_MATRIX / ROADMAP / JOURNAL into the one
  condensed SPEC + NEXT_STEPS; those absences are named as gap rows, NOT filled with empty shells
  (owner-gated per the run briefing).
- Phase 4 (attic): nothing superseded → no attic needed at adoption.
- Phase 5 (architecture → matrix): the engine has no separate ARCHITECTURE.md / TEST_MATRIX.md; the
  27-suite harness already covers the spec facts. Deriving the split docs is a future owner-gated row.
- Phase 6 (attach record): records born (below); this file carries the run's journal narrative because
  the host keeps no separate JOURNAL.md yet (gap row). Host now on the standard pipeline.

## Records born this run (paths)
- `.live-spec/profile.md` — host overrides (spec.file: SPEC.md · push.self-certify · remote) + open
  owner-lines (project.kind, budget.pressure).
- `.live-spec/installed.md` — M-7 installed-set record (pack 1.0.14 + the eight skill versions).
- `.live-spec/PROBLEMS.md` — seeded from two documented open issues.
- `.live-spec/adopt/2026-07-12-pre-inventory.md` — fingerprints + anchor multiset + surface inventory.
- `.live-spec/adopt/2026-07-12-post-inventory.md` — the delta proof.
- `.live-spec/adopt/2026-07-12-adopt-plan.md` — this file.
- `.live-spec/checkpoints/` — gitignored working-checkpoint home (with a `.gitkeep`).
- `.gitignore` — two lines added: `.live-spec/checkpoints/` and `.adopt-checkpoint.md`.

## Catch-up gap rows — what the engine still owes the method (each an owner-gated future row)

1. **Single condensed SPEC deviation** — the host keeps ONE `SPEC.md` in place of the canonical
   `PRODUCT_SPEC.md` + `ARCHITECTURE.md` + `TEST_MATRIX.md`. Recorded as `spec.file: SPEC.md` in the host
   profile. Splitting into the separate canonical docs is the owner's call; do not create empty shells.
2. **No `ARCHITECTURE.md`** — named nodes/seams with an owning node per spec fact are not a separate doc.
   Owner-gated split (part of row 1).
3. **No `TEST_MATRIX.md`** — the 27-suite harness exists but there is no node×fact matrix with pinned
   levels and per-fact traceability as a standing test. Owner-gated to derive.
4. **No `SURFACE_REGISTRY.md` (or E-10 gate)** — surfaces render but no executable completeness gate marks
   an unregistered surface RED. Owner-gated to add (doc form is the fallback).
5. **No `ROADMAP.md`** — the forward queue lives inside `NEXT_STEPS.md` (lanes + E4–E8). Folding is
   deliberate; a separate one-wish-one-row queue is owner-gated.
6. **No `JOURNAL.md`** — dated history-with-why lives in git messages + `NEXT_STEPS.md`; this adoption's
   entry is recorded HERE. A standing JOURNAL.md is owner-gated.
7. **`tests/make_synthetic.py` stale/destructive** — carried into PROBLEMS.md as the standing owner-row.
8. **Residual `tlvphoto` bare word in SPEC.md** — publish-hygiene item for the public flip; PROBLEMS.md.

## HALTed owner-calls (open lines, never invented)
- `project.kind` — ADOPT.md requires it, ALWAYS asked, never inferred (INV-36). No recorded word. OPEN in
  the host profile.
- `budget.pressure` (ECONOMY rung) — no host-scope recorded word. OPEN; runs on personal default meanwhile.
- The doc-split rows (1–6 above) — each waits on the owner's word; recorded as gaps, not acted on.

## Run journal entry (Phase 6.2)
2026-07-12 — First live-spec adoption of exhibition-engine. Born the `.live-spec/` record set (host
profile, installed-set at pack 1.0.14, seeded PROBLEMS, pre/post inventories, this plan). No host file
moved, deleted, or edited (INV-7). Remote outcome: EXISTS (private; public flip owner-gated). Provenance:
the host was already native-live-spec (condensed SPEC), so there is no re-engineered reconcile backlog —
only the named doc-split gap rows, all owner-gated. HALTs held for the owner: project.kind, budget.pressure.
Suite verdict at adoption recorded in the post-inventory. Commit stays local per worker discipline.

## First recommended action after adoption
Run `product-prover` on `SPEC.md` — it has no recorded prover pass under the currently installed prover
version (product-prover 1.0.0), so the full lens set has not been met on this host's spec.
