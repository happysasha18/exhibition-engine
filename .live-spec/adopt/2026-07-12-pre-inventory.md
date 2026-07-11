# Pre-adoption inventory — exhibition-engine (taken 2026-07-12 00:1x, baseline commit 63b74b5)

Restore command: `git reset --hard 63b74b5` (tree was clean at adoption start; the records below are
the ONLY additions this run makes). Before-and-after self-test per SPEC INV-92: the post-inventory
must show the tree unchanged except the born `.live-spec/` files and the two `.gitignore` lines, and
the suite must read at least as green as this baseline.

## Document fingerprints (tracked .md, md5) at baseline
2669b899476486a699898095d4ad6a5f  NEXT_STEPS.md
712f0f7136a4f50f4bef9cb63de413e9  README.md
8c24dd24447f7ac0ecd9623f2201adbc  SPEC.md

(The engine tracks only these three .md files — a well-run condensed host. No ARCHITECTURE.md /
TEST_MATRIX.md / ROADMAP.md / JOURNAL.md / SURFACE_REGISTRY.md exist; see the adopt plan's gap rows.)

## Spec anchor multiset (INV-*/EX-* counts in SPEC.md) — top of the distribution
112 distinct anchors total. Top counts:
  19 EX-DOOR-2
  13 INV-1
   9 EX-COMPOSE
   8 EX-DOOR-3
   7 INV-33
   7 INV-30
   6 INV-8
   6 INV-25
   6 EX-SOUND
   6 EX-LOAD
   5 INV-7 / INV-32 / INV-26 / INV-20 / INV-14 / INV-10 / EX-PROTECT-GIFT / EX-HANG / EX-DOOR
(full multiset reproducible by: `grep -oE '\b(INV|EX)-[A-Z0-9-]+' SPEC.md | sort | uniq -c | sort -rn`)

## Surface & entity inventory (from commands, not the old prose)
Engine source tree (find engine -type f):
- `engine/build.py` — the generic gallery-site builder + exhibition renderer entrypoint.
- `engine/harness/headless.py` — the browser test harness.
- `engine/assets/worker.js` — Cloudflare worker (registry beats, gift/series/lang).
- `engine/assets/exhibition.js` / `exhibition.css` — the client renderer (door → hang → walk) + styles.
- `scripts/build.sh`-equivalents: `scripts/deploy.sh`, `scripts/gen_greetings.py`.
- `example/site.json` + `example/instance-assets/` — synthetic example content.
User-facing surfaces (rendered by exhibition.js / baked by build.py): the door, the hang (gallery),
the walk, the quiz funnel, the share/gift flow, the language pick, the series lift. These are specced
in SPEC.md under EX-DOOR* / EX-HANG / EX-COMPOSE / EX-QUIZ* / EX-SHARE / EX-PULSE / EX-LOAD / EX-SOUND
anchors. NOTE: there is no SURFACE_REGISTRY.md executable gate yet — named as a gap row.
Tests: 27 `tests/test_*.py` suites driven by `tests/run_all.py`.

## Suite verdict at baseline
`.venv/bin/python tests/run_all.py` — LOG tail: **26/27 suites green · wall 298s · RED: glide**, with the
one expected pinned compose CH6 skip at 1280px (compose: 16 pass / 0 fail / 1 skip). The single RED
(`glide`) is the documented CPU-load flake: `tests/test_glide.py` re-run in isolation immediately after
passed **12/12, 0 fail, 0 skip** (exit 0). Effective baseline = green; the glide flake is carried in
PROBLEMS.md (WATCHED 2026-07-12). No push is taken this run regardless (worker discipline).
