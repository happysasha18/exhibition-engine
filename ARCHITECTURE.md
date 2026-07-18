# exhibition-engine — Architecture

How the product is BUILT: the named nodes the spec's facts live in. Written from the proven
SPEC.md. One node = one name = one responsibility — the one-surface-one-name rule, applied to
structure.

**When this doc changes:** a large or surface-class wish updates it BEFORE the matrix is
touched; a bug or small wish only cites the existing node it lands in. Re-proven only when it
changes.

**This doc is ITERATIVE. Never written milestones ahead.** It maps the product as it stands. A
node exists for what ships today. This is the FOUNDING pass — current-to-shipped only, no
speculative future nodes.

---

## The shape at a glance

A build-time Python bake reads a content directory plus `site.json` on the author's machine and
emits a self-contained static Site Bundle. A CDN (Cloudflare Pages) serves every visitor byte —
the site is complete and crawlable without JavaScript. A generic browser client wakes on top of
the static face and runs the adaptive walk (door, gallery, zoom, story, series, quiz, sound). One
narrow edge worker (`_worker.js`) answers `/api/story`, `/api/quiz`, and `/api/i18n`; it alone
holds the model API key and the private per-work story fragments and quiz answers, injected only
at bake time and never shipped as a static asset. A Python test harness drives a real headless
Chrome against the baked bundle to prove all of the above.

## Nodes

Every spec fact is OWNED by exactly one node. Pins are `file:line` from a command actually run
against this checkout.

| Node | Responsibility (one line) | Owns spec facts (anchors) | Pinned to (file:line) |
|---|---|---|---|
| The bake (`engine/build.py`) | Reads the content dir + `site.json`, renders every static page and JSON contract, copies and caps client assets, and — only when the private-fragment source files are present — injects them into the worker template | `BK`, `SB`, `WP`, `WP-CLEAN`, INV-3, INV-4, INV-5, INV-6, INV-7, INV-9, INV-10, INV-32, INV-56, INV-63 | `engine/build.py:713` (`def build`) |
| The door + gallery walk (`exhibition.js` — door/deal/glide) | The threshold render, the living-hand deal, one-input-one-frame navigation, the loading ladder that arms the frame | `EX-DOOR*`, `EX-GREET*`, `EX-RETURN`, `EX-HANG`, `EX-CAPTION`, `EX-GLIDE`, `EX-LOAD`, `EX-LOAD-2`, `EX-LOAD-3`, `EX-ACCENT`, INV-11..INV-21, INV-71, INV-74, INV-84, INV-86, INV-94, INV-97, INV-98 | `engine/assets/exhibition.js:625` (`function dealHand`), `:1296` (`function doorPick`), `:2785` (`function glideToFrame`), `:913` (`function ladderFlight`) |
| The zoom / gracious deterrent (`exhibition.js` — inspect + protect) | Pinch-to-inspect (open/pan/dismiss, mirrored entry-exit), and the desktop right-click / drag / touch gift ceremony that stands between a visitor and the master file | `EX-PROTECT*`, `EX-ZOOM` (INV-75..INV-77, INV-81..INV-87, INV-93), INV-49, INV-56 | `engine/assets/exhibition.js:2273` (`function zoomPick`), `:1910` (`function openGift`) |
| The story + series (`exhibition.js` — told story + side room) | The narrator layer (fetch, cadence, degrade-to-silence) and the series side room (pill, crossing, lane, close) | `EX-STORY*`, `EX-STORY-BEAT`, `EX-SERIES`, INV-46, INV-47, INV-88, INV-89 | `engine/assets/exhibition.js:1729` (`function tellStory`), `:3180` (`function openSide`) |
| The quiz (`exhibition.js` — chip + card + funnel) | The public four-option chip, the card open/submit/close flow, the funnel stage and A/B arm dimension | `EX-QUIZ*`, INV-59, INV-60, INV-62, INV-64..INV-69 | `engine/assets/exhibition.js:2497` (`function quizCardOpen`), `:64` (`function quizStageUp`) |
| The chrome + compose (`exhibition.js` — sound, faceSync, pulse) | The ambient player, the one-page-shape face lock shared by every standing face, and the analytics event registry | `EX-CHROME`, `EX-SOUND*`, `EX-PULSE`, `EX-AB`, `EX-MEMORY`, `EX-EDGE-GUARD` (client half), INV-22..INV-25, INV-27, INV-41, INV-43, INV-67, INV-70, INV-90, INV-91, INV-96 | `engine/assets/exhibition.js:2889` (`function faceSync`), `:75` (`function pulse`), `:3866` (`(function sound()`) |
| The client styles (`exhibition.css`) | Motion tokens, face-lock/scrollbar-gutter rules, the loading-ladder plate/bar visuals, door/zoom/quiz/side-room layout | `EX-MOTION`, `EX-MOTION-R`, `EX-ARRIVE`, `EX-BOOT` (with the bake's inline `js` mark), INV-22, INV-23, INV-70, INV-95 | `engine/assets/exhibition.css:1` |
| The client assembler (`engine/assemble_client.py` + `engine/client/`) | The served `exhibition.js` is a committed, GENERATED file: 21 ordered raw line-slice fragments in `engine/client/` joined verbatim (empty-string concat) by an explicit manifest into `engine/assets/exhibition.js`. A byte-parity test and a pre-push gate red on any drift, so the generated file is never hand-edited — edits land in a fragment. `build.py` is untouched (the `@@NS@@` tokens ride the join). | (infrastructure — preserves the client byte-for-byte, owns no spec anchor) | `engine/assemble_client.py:1`, `engine/client/`, `tests/test_assembly.py:1` |
| The edge worker (`engine/assets/worker.js`) | Answers `/api/story`, `/api/quiz`, `/api/i18n`, `/api/geo`; holds the model API key, the baked-in private story fragments and quiz answers, the KV cache, and the three money fences. `/api/geo` returns the arriving country (`{c}` from `request.cf.country`, `cf-ipcountry` fallback), `no-store`, dispatched before the `/api/i18n` 404 gate — used only to narrow the language corner (`EX-LANG-GEO`), never stored, never on a beat | `EX-STORY-EDGE`, `EX-QUIZ-EDGE`, `EX-I18N`, `EX-LANG-GEO`, `EX-EDGE-GUARD`, INV-26, INV-51, INV-59, INV-68 | `engine/assets/worker.js:92` (`export default {`), `:372` (`async function quiz`), `:188` (`async function story`), `function geo(req)` |
| The test harness (`engine/harness/headless.py`) | Serves a baked bundle locally and drives it with a real headless Chrome (DOM reads, gesture simulation) for every browser-level test row | (infrastructure — proves the anchors above, owns none itself) | `engine/harness/headless.py:230` (`class Browser`) |
| The test suite (`tests/run_all.py` + `tests/test_*.py`) | Runs all 34 named suites and gates green/red; each `test_*.py` traces to the anchors it asserts | (infrastructure — traceability lives per-suite, not summarized here) | `tests/run_all.py:20` (`SUITES = [...]`) |
| The ratchet/gate tooling (`scripts/`) | Spec style + redundancy lint, the ratchet manifest, the deploy recipe, the greeting-cache generator | (governs the SPEC/bundle, not a spec anchor itself) | `scripts/spec-style-lint.py:249` (`def lint`), `scripts/deploy.sh:1` |

## Seams

| Seam | Between | What crosses | Format owner |
|---|---|---|---|
| content → bake | the instance's content dir (`gallery/gallery_data.json`, `site.json`, optional `story_notes.json`/`quiz.json`) · the bake | the content contract: gallery items, captions, private story notes, private quiz answers | the instance (content dir), format defined by the bake |
| bake → client | the bake · the door/gallery/zoom/story/quiz/chrome client | `exhibition_data.json` (works, captions, palettes) + `config.json` (flags, feel-knobs, the `experiments` registry — `quiz_arm` and `quiz_chip_copy` when the quiz ships, each `arms·flag·metric·salt`, `EX-QUIZ-COPY`/`EX-AB` — and the `lang_geo` country→tongues map from `site.json`, `EX-LANG-GEO`) | the bake (`engine/build.py:855`, `:1011`) |
| bake → worker | the bake · the edge worker | the worker TEMPLATE (`engine/assets/worker.js`) rewritten at bake time: `STORY_FRAGMENTS` and `QUIZ_ANSWERS` markers replaced with the instance's private data, emitted only as `_worker.js` | the bake (`engine/build.py:1050`, `:1056`) |
| bake → routing | the bake · Cloudflare Pages | `_routes.json` restricts the worker to `/api/*` so every other path is served as a pure static CDN byte | the bake (`engine/build.py:1059`) |
| client → worker | the door/story/quiz/chrome client · the edge worker | `/api/story`, `/api/quiz`, `/api/i18n` JSON requests and responses | the worker (`engine/assets/worker.js:294` `storyShape`, `:441` `shape`) |
| the private-fragment seam | the bake · the worker | story notes and the single quiz answer are baked ONLY into `_worker.js`'s inline markers; they are never present in `exhibition_data.json`, `config.json`, or any other served static byte | the bake, enforced by INV-59/INV-60 |
| worker → KV | the edge worker · Cloudflare KV | translation cache, coat-check seen-ids, rate/day/dead-model counters | the worker |
| suite → client/worker | the test harness · the baked bundle served locally | DOM reads and simulated gestures over a real headless Chrome session | the harness (`engine/harness/headless.py`) |

## Runtime view

| Flow | The walk through the nodes | Where it can fail | If it fails |
|---|---|---|---|
| Bake | the author runs `engine/build.py` against a content dir (seam: content → bake) → it renders `index.html`, `/w/<slug>.html` pages, writes `exhibition_data.json`/`config.json` (seam: bake → client), copies/caps gallery assets and client assets, and — if private files are present — rewrites `_worker.js` with the private fragments (seam: bake → worker) and writes `_routes.json` (seam: bake → routing) | a missing/malformed content file; Pillow absent for the display-cap bake | the display-cap/mark step is pinned SKIP when Pillow is absent (INV-56 tests skip cleanly); a missing optional file (story_notes/quiz.json) degrades the bundle to byte-identical without the feature (INV-60) |
| Deploy | `scripts/deploy.sh` uploads the Site Bundle to Cloudflare Pages and purges cache | an upload/purge failure | the deploy script's own verify beat (md5 cross-check) catches a partial upload before it is called done |
| Client boot | a visitor's browser loads the static `index.html` (already a complete face without JS, INV-2) → the breathing boot face holds the cold arrival (EX-BOOT/INV-95) while the client JS wakes and marks the walk live | JS fails to load or errors; the wake mark never lands on a genuinely hung ride | INV-30/INV-95: the `js` mark falls only on the script's own load error or a ~12s last-net cap, returning the full static face as the bounded worst case — no broken half-JS state |
| The door → pick → glide | the door deals a hand (seam: bake → client data) → a visitor picks a work → `doorPick` starts the ceremony → `glideToFrame` drives exactly one centered frame per input gesture (seam: client-internal, EX-GLIDE) | a thin/missing content pool; a device rotation mid-glide | INV-14: a thin pool still yields a diverse hang; INV-86: a rotation mid-glide cancels to a clean dock at the target frame |
| Zoom-to-inspect | a pinch or trackpad-pinch is detected on a picture (seam: client-internal, EX-ZOOM) → the layer opens over the standing face, tracked as one history step | the viewport changes while zoomed | INV-82/INV-86: close re-measures the source live and scales back to its place in the new viewport |
| The told story / series | the client calls `/api/story` (seam: client → worker) for a lean narration; the worker checks the money fences, calls the model, and caches in KV | the model account is dead (non-429 4xx); the fetch fails outright | INV-68: a dead-account flag serves baked English with a plain hello, no further charge; EX-STORY/INV-47: any story failure degrades to silence, the walk loses nothing |
| The quiz | the chip opens the card (seam: client-internal) → the tapped answer posts to `/api/quiz` (seam: client → worker) → the worker judges it against the private answer baked into `_worker.js` | the attempt-fence trips; no KV bound (preview/local) | INV-59: the fence degrades to unlimited when no KV is bound so a preview/local deploy still judges; a miss shows one localized line and closes, the walk loses nothing |

## Placement view — the tiers and their technology

| Node | Runs at | Load-bearing technology |
|---|---|---|
| The bake | build-time, the author's machine (or CI) | python3, Pillow (optional, for the display-cap/mark step) |
| The Site Bundle (HTML, `exhibition_data.json`, `config.json`, sitemap, gallery assets, `exhibition.js`/`.css`) | static files on a CDN | Cloudflare Pages |
| The door/gallery/zoom/story/quiz/chrome client | the visitor's browser | vanilla JS (no framework), vanilla CSS |
| The edge worker (`_worker.js`) | edge worker, routed only to `/api/*` via `_routes.json` | Cloudflare Pages Functions / Workers runtime + Workers KV |
| Secrets (the Anthropic API key, the private story fragments, the private quiz answers) | live ONLY inside the deployed `_worker.js` and its KV bindings — never in the Site Bundle, never in a served static asset | injected at bake time from instance-owned files kept out of the public bundle (`engine/build.py:645`, `:665`) |
| The test harness + suite | the author's machine / CI | python3 + a real local headless Chrome via CDP (`engine/harness/headless.py`) |

## Quality budgets

| Budget | Number | Instrumentation home | Watcher |
|---|---|---|---|
| Full-suite wall time | measured per run, not a fixed target | `tests/run_all.py` prints `wall {seconds}s` alongside the green/red count on every run (`tests/run_all.py:70`) | read by eye at every run; no red-past-N gate is wired |
| Suite count | 32 named suites (`tests/run_all.py:20`) | the `SUITES` list itself, cross-checked against `test_*.py` files present (INV-5r) | `tests/run_all.py` fails the run if the two sets diverge |
| Client JS bundle size | 231,673 bytes (3,803 lines), `engine/assets/exhibition.js` | `wc -c` on the source file — no build/minify step exists, so the served byte count equals the source byte count | none wired; a budget with no watcher |
| Client CSS bundle size | 50,465 bytes (663 lines), `engine/assets/exhibition.css` | `wc -c` on the source file | none wired; a budget with no watcher |
| Edge worker size | 26,417 bytes (502 lines), `engine/assets/worker.js` template (grows with injected private fragments per instance) | `wc -c` on the template source | none wired; a budget with no watcher |
| Paint / interaction timings (first frame, glide latency) | no honest number exists | none — `EX-TIMING`'s `?timings` narrates performance marks live in a running session but nothing aggregates or stores them | none; said by name rather than given a vanity metric |

## Feature coverage

Kept light at founding: the Formal index's clause anchors (`EX-*`) already name every feature-level
surface and are mapped to their owning node in the Nodes table above. A per-feature `[feature: F-x]`
tag layer is not in use in this SPEC — the anchor-to-node mapping above stands in for it.

## Decisions — where they live

| Decision | Status | Lives at |
|---|---|---|
| Worker private data is bake-injected, never a static asset | resolved | SPEC.md `EX-STORY-EDGE`, `EX-QUIZ-EDGE`, INV-59, INV-60; `engine/build.py:1018-1059` |
| No build/minify step for `exhibition.js`/`.css` — the source byte count is the served byte count | resolved (as-shipped) | this doc's Quality budgets section |
| Reconciled feature deltas between a proving instance and the generic engine | resolved / tracked per-row | SPEC.md "Reconciliation log" (`⟨DELTA-1⟩` through `⟨DELTA-15⟩`), SPEC.md:1501 |

## Prover record

| Date | Doc version proven | Record |
|---|---|---|
| — | v0.1 (founding) | unproven — this is the founding pass, not yet reviewed by product-prover |

---

*Coverage rule (walked at matrix derivation): every spec anchor appears in some node's "owns"
column — an orphan fact means a missing node or a missing assignment; a node owning nothing traces
to no spec backing and is itself a finding.*
