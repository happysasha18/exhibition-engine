# Post-adoption inventory — exhibition-engine (2026-07-12, first adoption)

Before-and-after self-test (SPEC INV-92): the run must have added ONLY the `.live-spec/` record set and
the two `.gitignore` lines — no host file moved, deleted, or edited (INV-7).

## Tree delta (git status --porcelain, verified)
```
 M .gitignore                 (added 2 lines: .adopt-checkpoint.md ignore; .live-spec/checkpoints/* + !.gitkeep)
?? .live-spec/                (new record set)
```
No other path changed. The three tracked host `.md` files keep their baseline md5 (unmodified):
- NEXT_STEPS.md  2669b899476486a699898095d4ad6a5f
- README.md      712f0f7136a4f50f4bef9cb63de413e9
- SPEC.md        8c24dd24447f7ac0ecd9623f2201adbc

## Files born (the whole added set)
- .live-spec/profile.md
- .live-spec/installed.md
- .live-spec/PROBLEMS.md
- .live-spec/adopt/2026-07-12-pre-inventory.md
- .live-spec/adopt/2026-07-12-adopt-plan.md
- .live-spec/adopt/2026-07-12-post-inventory.md  (this file)
- .live-spec/checkpoints/.gitkeep  (dir keeper; actual checkpoints are gitignored)
- .adopt-checkpoint.md at repo root stays UNTRACKED (gitignored), not part of the commit.

## Ignore rules verified (git check-ignore)
- `.adopt-checkpoint.md` → ignored (correct).
- `.live-spec/checkpoints/<anyfile>` → ignored (correct).
- `.live-spec/checkpoints/.gitkeep` → NOT ignored (tracked, keeps the dir on a clone).

## Suite verdict (unchanged from baseline)
26/27 suites green · one expected compose CH6 skip · the lone RED (`glide`) is the CPU-load flake,
green 12/12 in isolation (recorded in the pre-inventory and PROBLEMS.md). Adoption changed no source or
test, so the suite reads exactly as at baseline. Post ≥ pre: met.
