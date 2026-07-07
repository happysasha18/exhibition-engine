# PORT REPORT — engine catches up to the live site (two features)

_Date 2026-07-07 · a real PORT movement, not a verbatim chore. The engine trailed the live
tlvphoto site by two whole features. This record is file-by-file: what was ported (with which
generic renames), the three judgment proposals (a/b/c) — **each awaiting Alexander / senior
sign-off** — and the suite result. Nothing was pushed. The tlvphoto repo was read-only throughout._

Source of truth read from (never written): `~/tlvphoto/assets_src/exhibition.{css,js}`,
`~/tlvphoto/assets_src/worker.js`, `~/tlvphoto/scripts/build_site.py`,
`~/tlvphoto/gallery/shared/tokens.css`.

---

## What was ported — file by file

The engine's three asset files were byte-identical to tlvphoto's **except** the two feature deltas
(a diff confirmed every differing hunk was a feature hunk — no engine-only content existed to
preserve), so the faithful port was a verbatim carry of those files, plus wiring in the builder.

### FEATURE 1 — the appearance law (EX-ARRIVE)
Every appearing element arrives on the house breath, never pops.

- **`engine/assets/exhibition.css`** — carried: `.exd-lang` / `.exl-list` born at `opacity:0` +
  `.show`; `#ex-toast` `.show`; the loader `#ex-breath` `exb-enter` keyframe handing off to
  `exb-breathe`; the series pill `exs-fade`; the closing screen `.exh-fin` staggered `.show` reveal
  (question → choices → signature, each on `--d-soft`, reduced-motion honored).
- **`engine/assets/exhibition.js`** — carried: the `.show`/rAF breath-in for the toast, the closing
  screen, the language mark, and the language dropdown's open/close by breath (`listOpen`/`listClose`
  with a tempo-scaled hide timer).
- **Renames:** none needed. Every appearance-law token is already engine-generic
  (`exd-`/`exl-`/`exs-`/`exb-`/`exh-` = exhibition prefixes). Nothing tlvphoto-specific to generalize.

### FEATURE 2 — the told story (client + edge mechanism)
- **`engine/assets/exhibition.js`** — carried the whole client slice: the deterministic light-lean
  `storyOrder`/`hourGap` + `SPINE`, `assembleOrder` (used by restore, door-pick, hash-arrival — off
  ⇒ byte-identical arc, ST1), the `.told` plaque slot fill (`fillTold`), the `/api/story` fetch
  (`tellStory`, gen- and set-guarded, re-tells over the grown set on «ещё 5»), `--tone` set in
  `ground()` (`×0.66`), `story_variant` riding the existing `walk_unfold`/`walk_exit` GA beats
  (no sixth beat), and the `w.sold` red-dot markup.
- **`engine/assets/exhibition.css`** — carried the wall-label plaque: `.told` (serif italic,
  `:empty`-hidden, `exs-fade` in), `.dot` (red sold marker), the `--tone` color-mix tint on title /
  told / meta, the left hairline + readability scrim.
- **`engine/assets/worker.js`** — carried the entire `/api/story` edge route: `STORY_FRAGMENTS` /
  `STORY_PARAMS_VERSION` bake stubs, shaped-input validation, sha256 ordered-sequence KV cache key,
  single-flight lock, Haiku `narrate` over ONLY the private fragments, strict `storyShape` /
  `validateStory`, degrade-to-silence on every failure path.
- **`tests/fixture_content/gallery/shared/tokens.css`** — added `--told: #cbc3b6` (the narrator
  line's resting bone). `--tone` is a **runtime** value (set by JS per focused work) — tlvphoto's
  tokens file carries only `--told` too, so no static `--tone` token was added.
- **`engine/build.py`** — wired the bake generically:
  - added the `ai_story` flag (ships **false**, flipped at deploy — INV-19);
  - added the `story` config block (`variant`/`light_weight`/`params_version`);
  - added an **optional** `data/time_of_day.json` load (`tod_marks_load`) → `tod` baked onto each
    work (absent ⇒ every work `free`, the light-lean a no-op, arc unchanged — ST1);
  - added the `STORY_FRAGMENTS` bake + `__STORY_FRAGMENTS__` / `__STORY_PV__` marker replacement,
    gated on `ai_story`, embedded into `_worker.js` only (never a public byte);
  - worker copy now also fires under `ai_story`.

**Renames applied vs deferred to proposal (a):** the appearance law needed none. The told story
carries tlvphoto-named surfaces (`window.TLVStory`, the `TLV_I18N` KV binding, the `__STORY_*`
markers, the numeric `ID_RE`). These were carried **as-is** because the engine's *pre-existing*
code already uses the same un-generalized names throughout (`TLV PHOTOS` wordmark, `tlv.*` storage
keys, `TLVTimings`, `__tlvSeen`, `env.TLV_I18N`). Renaming only the new feature's half would have
broken the one-name-per-surface rule and created fresh inconsistency, so the whole rename is raised
as proposal (a) rather than done piecemeal.

### Additional pure-motion delta carried (not one of the two features)
`exhibition.js` also differed by the glide **v5** launch weight (`LAUNCH = 1.4`, "casts off like a
ship from the pier"). This is pure scroll motion, no content, no judgment — carried verbatim to keep
the engine in sync. The `glide` suite stays green.

---

## Three judgment proposals — AWAITING ALEXANDER / SENIOR SIGN-OFF

### (a) TLV-specific bake markers + names → propose generic engine names
The story mechanism carries several tlvphoto-shaped identifiers. Proposed generic names:

| tlvphoto / current | proposed engine name | note |
|---|---|---|
| `__STORY_FRAGMENTS__` / `__STORY_PV__` markers | keep — already generic (`STORY_*`, no "tlv") | lowest-risk; recommend keep as-is |
| `env.TLV_I18N` (KV binding) | `env.EX_KV` (or `env.EDGE_KV`) | shared by i18n + memory + story; a rename touches worker + deploy binding |
| `window.TLVStory` / `window.TLVTimings` / `window.__tlvSeen` | `window.EXStory` / `EXTimings` / `__exSeen` | the whole global surface, not just story |
| `tlv.*` localStorage keys, `TLV PHOTOS` wordmark | `<instance>.*` / from `site.json` | belongs to the wider parameterization movement |
| `ID_RE = /^\d{5,25}$/` (edge id grammar) | accept the engine's id grammar (slugs), e.g. `/^[\w-]{1,64}$/` | **real gap**: synthetic ids are `synth-01`, so `/api/story` 400s them today; it degrades to silence (CS-8) but the story can never speak for slug-id instances |

**Recommendation:** the rename is one coherent job with the engine's existing un-generalized names —
do it as its own small movement (the E8 parameterization), **not** half-done in this port. The one
item worth fixing sooner is `ID_RE`, since it silently disables the story for any slug-id instance.

### (b) Do the private per-work STORY_FRAGMENTS (raw authored notes) belong in a shared engine?
**Recommendation: no — the mechanism ships in the engine, the raw notes stay instance-private.**
tlvphoto reads notes from `alexander_labels_2026-07-04.json` (his own words). I did **not** hardcode
that filename. The engine now reads notes from an **optional, instance-owned** `<content>/story_notes.json`
(a flat `{id: note}` map), absent ⇒ fragments carry only public grounding (title/place/subject/light).
The notes are baked **into `_worker.js` only** (the one bundle Pages never serves) and only when
`ai_story` is on — so raw notes never become a public byte. This keeps the engine generic and the
private authored notes with the instance, matching the "engine public / content private" split.

### (c) capzone / title sizing deltas — intentional engine default, or staleness?
| delta (engine → tlvphoto) | read | recommendation |
|---|---|---|
| capzone `max-width` **38vw → 42vw** | **intentional, feature-coupled** — the plaque widened to hold the told line (`.told` is `max-width:34ch`) | adopt (carried) |
| title clamp **2.4vw/34px → 2.2vw/30px** | **intentional, feature-coupled** — the name yields a touch so the plaque hierarchy reads name < told < facts | adopt (carried) |
| mobile title **18px → 22px** | **general readability improvement (staleness)** — not story-specific; the engine should carry it regardless | adopt (carried), reconcile as a plain default |

All three tlvphoto values were carried (the told-story CSS is structurally one block). None looks like
a divergent engine default worth preserving; all three are coherent. Flagged only so senior can veto
any one.

---

## Suite result

`python3 tests/run_all.py` → **17/17 suites green · wall 139s** (site 30 · exhibition 9 · door 28 ·
vector 6 · back 7 · greet 11 · series 6 · motion 10 · reset 4 · load 6 · share 12 · glide 8 ·
pulse 3 · hand 5 · i18n 7 · lang 4 · memory 4).

**Fixture / test touches (no assertion weakened):**
- `fixture_content/gallery/shared/tokens.css` — added `--told` so the plaque's color-mix resolves.
- `tests/test_exhibition.py` — the "TS deferred — no told-story control (html + client js)" row was
  a scaffold guard asserting the feature was **absent**. It has legitimately landed, so its
  client-JS-absence clause is now false. I **re-aimed** the row at the standing invariant it really
  protects (INV-1: the narrator's words are client-rendered and must never appear in the crawlable
  served HTML) and kept that half. This is a guard flip on a now-obsolete deferral, not a weakening
  of a live invariant. Flagged for senior confirmation.

Story bake verified with an `--enable ai_story` bake: markers replaced (0 left), `STORY_FRAGMENTS`
populated with public grounding, `STORY_PARAMS_VERSION="1"`, `/api/story` route present, `tod` baked
onto works, `_routes.json` written. Default bake (story off) is byte-unchanged from before.
