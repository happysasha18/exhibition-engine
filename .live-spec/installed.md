# Installed set — live-spec pack (recorded 2026-07-12, first adoption of exhibition-engine)

Package VERSION at record time: **1.0.14** (read from ~/live-spec/VERSION).

Skills as installed on the working machine (~/.claude/skills/), the authoritative set (version line
under `metadata:` in each SKILL.md frontmatter, SPEC M-7):

- live-spec-base 1.0.2
- spec-author 1.0.0
- product-prover 1.0.0
- build-pipeline 1.0.1
- test-author 1.0.1
- communicator 1.0.3
- feedback-intake 1.0.0
- publish 1.0.0

Prior record: none existed (this is the engine's first adoption — no installed-set record was present).

## Vendored pack files

One pack file is carried in this tree as a byte-identical copy, recorded here with the pack version it
came from. A guard holds the identity: `tests/test_harness_drift.py`.

- `tests/headless_harness.py` — the canonical browser test harness core, vendored 2026-07-27 from
  `~/live-spec/templates/headless_harness.py` at package VERSION **4.3.0**, md5
  `8f199e1066dd645450c50bb10c920e99`. The engine's own driving methods live in `tests/headless.py`,
  a subclass over that core. The skills record above stands at 1.0.14: this walk vendored the harness
  template alone and ran no skills update.

Reference-snapshot drift (informational): the engine's read-only pack snapshot at
`~/tlvphotos/.claude/skills/` is OLDER than the authoritative machine set — live-spec-base 1.0.1,
build-pipeline 1.0.0, test-author 1.0.0, communicator 1.0.2 (spec-author / product-prover /
feedback-intake / publish match at 1.0.0). The machine set above is authoritative for this host;
the snapshot is a cloud-session convenience and refreshes on the owner's word.
