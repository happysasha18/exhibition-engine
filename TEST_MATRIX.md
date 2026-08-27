# exhibition-engine — TEST MATRIX (projection of SPEC.md's pass/composer section)

No `TEST_MATRIX.md` existed in this repo before this file. This is not a matrix for the whole of
`SPEC.md` (2,132 lines, most of it already proven by the suite under other names) — it is the
first matrix, seeded to close наряд S-16's own gap: `SPEC.md`'s `### The pass — a composed
crossing between two works` (added by this наряд, `EX-PASS` / `EX-PASS-COMPOSER` / `EX-PASS-LEVEL`
/ `EX-PASS-VOICE` / `EX-PASS-DOOR`) is new, and charter shelves **1 (Matter), 3 (Enfilade), 4
(Polyphony) and 12 (Five decompositions)** — `~/tlvphotos/lab/CROSSING-BRIEF.md` — are named by no
test in `tests/` today (checked: `grep -rn "shelf 1[^0-9]\|shelf 3[^0-9]\|shelf 4[^0-9]\|shelf 12\b"
tests/*.py` returns nothing). Extending this matrix to the rest of `SPEC.md`'s surfaces is separate,
later work — this file does not claim that coverage and a reader should not infer it.

**Where the facts come from.** Every row below projects a sentence that already stands in
`SPEC.md`'s new section, or in `docs/design/PASS-API-V1.md` §4.4/§4.6/§4.7/§8/§9 which that section
names as the pass's full contract (SPEC.md says plainly: "this section does not repeat or shadow
it"). A row citing a PASS-API-V1 section number is projecting a fact `SPEC.md` incorporates by
naming that document as the contract, not reaching past the spec.

**No architecture node owns this surface yet.** `ARCHITECTURE.md`'s Nodes table has no row for
`engine/assets/pass-composer.js` or any `engine/assets/pass-inst-*.js` file — the whole pass/instrument
layer is unassigned. Rows below name the file each fact actually lives in (read, not edited, under
this наряд's own fence) so a test can be aimed correctly; assigning the node itself is `architect`'s
next pass, named here as a gap rather than papered over.

**The level convention this project already keeps for this surface** (read off the shipped suite,
not invented here): a data or logic fact about a composed plan or score is proven by extracting the
REAL block of shipped source (`engine/assets/pass-composer.js`) and running it in Node — never a
hand-retyped mirror of its logic (`test_pass_score.py`'s and `test_pass_lawful.py`'s own words for
this: "the checker is run, not described"). A visual fact is proven by compiling the real
shader/drawing code in a headless-Chrome WebGL context and reading the rendered framebuffer back
(`test_pass_layer.py`, `test_pass_matter.py`). A diagnostic-surface fact (what the gated inspector
shows, PASS-API-V1 §9) is DOM-text level, read off that surface's own real markup. Rows below are
pinned to one of these three rungs — **node**, **pixel**, or **DOM-text** — never a plain string
match on source.

---

## §1 — Entities (from `SPEC.md`'s new section)

- **Pass** — the optional composed visual transaction between two hung works (`EX-PASS`).
- **Composer** — reads two ElementSets + a pair dossier, emits a ScenePlan (`EX-PASS-COMPOSER`).
- **ElementSet** — a work's fragments along one decompose axis, plus their complement (PASS-API §4.6).
- **ScenePlan / score** — the composer's plan (data-only, build-time) and its serialised, wire-shipped
  form (`EX-PASS-COMPOSER`).
- **Cue** — one timed unit of a score: `voice`, `roles`, `levels`, `window`, `doors`, tracks.
- **Level** (three readings — `EX-PASS-LEVEL`): **declared** (an instrument manifest's own claim),
  **owned** (a cue's `levels` list, checked for contention), **driven** (what a cue's built tracks
  actually move).
- **Voice** (pass sense) — a cue's budget class, `letter | accompaniment | miracle`, distinct from
  the exhibition's narrator voice (`EX-STORY`) (`EX-PASS-VOICE`).
- **Door** (pass sense) — a command's `{from, to}` geometry pair, distinct from the exhibition's own
  entry door (`EX-DOOR`) (`EX-PASS-DOOR`).

## §2 — State space

Axes, named before any cell is filled (a flat element × outcome grid would hide the data axis the
way the pack's own method warns against):

- **`visualLayer`**: `on` | `off`.
- **Pass outcome** (only reachable with `visualLayer: on`): `takes-the-frame` | `declines-before-takeover`
  | `refused-at-build` (four sub-states: actor-less plan · a door the instrument's manifest leaves
  blank · a levels-law contention · a tier-budget breach).
- **Decompose provider requested**: `structural` | `semantic` | `hybrid` | `author` | `fallback`, each
  independently `answers` or `declines`.
- **Tier**: `quiet` | `middle` | `culmination`.
- **Level reading asked of one structural level**: `declared` | `owned` | `driven` — independent axes;
  a level can be declared by an instrument and driven by a cue that never owns it.

A row that must hold across every state on an axis is an invariant and owns its own test rather than
one cell per state (`INV-109` is this matrix's own instance of that rule).

## §3 — Matrix rows

| ID | Spec anchor | Shelf | Fact (what it does) | Never (the regression fence) | Level | Status today | Home |
|---|---|---|---|---|---|---|---|
| PASS-01 | `EX-PASS` / `INV-109` | — (infra, gates every row below) | With `visualLayer: off`, or any decline/refusal before or during takeover, the walk plays exactly `EX-GLIDE`'s one-frame glide. | No partial, half-drawn, or one-frame-late pass state ever reaches the visitor when the pass does not take the frame; not one pixel differs from the plain glide. | pixel (headless Chrome, pixel-diff against the plain-glide baseline) | Built — PASS-API-V1.md's status block: "decline before takeover runs the legacy glide and changes no pixel" (conformance row 4). Existing partial coverage in `tests/test_pass_api.py`; no row cites `visualLayer` by name today. | `tests/test_pass_api.py` (extend) |
| PASS-02 | `EX-PASS-COMPOSER` | 12 — Five decompositions | A composed ScenePlan names at least one actor drawn from A's own ElementSet and at least one from B's. | A plan whose every actor is a whole, uncut frame is never turned into a playable score — the exact "two whole photographs as fullscreen strips" defect PASS-API-V1 §4.7 names by its own history. | node (extracted composer logic run in Node over a synthetic plan object) | Declared and unbuilt — PASS-API-V1 §4.7: "No engine code answers to this section." `pass-composer.js`'s shipped `CUE_IDS` are `pivot`/`travel`/`arrival` only; no generic multi-actor cast exists yet. Owed a real test the day ElementSet casting lands. | new file, e.g. `tests/test_pass_elements.py` |
| PASS-03 | `EX-PASS-COMPOSER` | 12 | An ElementSet plus its own `complement` reconstructs the source frame within the seam threshold (PASS-API §4.6, conformance row 32). | A provider that names elements without folding the untouched remainder into `complement` leaves a hole — the eye reads a hole as damage, which is the charter's own reason for the law. | pixel (reconstructed composite vs. the source file, seam threshold 6/255) | Declared and unbuilt — offline builder lives in the tlvphotos tree (`lab/data/objects-pass2.json`); no engine-side provider exists. | new file, e.g. `tests/test_pass_elements.py` |
| PASS-04 | `EX-PASS-COMPOSER` | 12 | The `fallback` decompose provider (tonal zones + detail scales) answers for every work on disk — never `decline{why}` — because a frame has a luminance range and a detail scale by construction. | No pair the engine ever composes falls through with zero decomposition; `fallback` is the road every pair is owed. | node (property test: iterate every work `gallery_data.json` supplies, assert `fallback` never declines) | Declared and unbuilt — PASS-API §4.6 "the road that answers for every pair" is unbuilt in engine. | new file, e.g. `tests/test_pass_elements.py` |
| PASS-05 | `EX-PASS-COMPOSER` | 12 | When a decompose provider declines, the composer falls to the next provider in the REQUEST's own order, and the diagnostic surface records the decline with its reason (PASS-API §4.6, conformance row 33). | The fall-through order is never silently reordered by anything but the request itself; a decline is never left unrecorded. | DOM-text (the gated inspector's own decline/fallback-reason list) | Declared and unbuilt. | new file, e.g. `tests/test_pass_elements.py` |
| PASS-06 | `EX-PASS-COMPOSER` | 3 — Enfilade | A ScenePlan's `middle` field is one of `none` \| `world` \| `surface`; a quiet-tier link's usual reading is `none`. | A plan never carries a `middle.kind` outside the closed three-value set, and a quiet link is never forced to build a middle it has no field for. | node (data-shape assertion on a composed plan object) | Declared and unbuilt — `pass-composer.js`'s shipped `CUE_IDS` (`pivot`/`travel`/`arrival`) carry no `middle` cue today. | new file, e.g. `tests/test_pass_middle.py` |
| PASS-07 | `EX-PASS-COMPOSER` | 3 | A built `middle` — a world or surface made from both works' elements — belongs to neither work outright: its door out speaks A's own visual language, its door in speaks B's. | A built middle never reuses A's whole hang frame as its own exit face, or B's as its own entry face — it is a third, constructed event, not a relabelled copy of either door. | pixel (headless Chrome: sample the middle's own frame against A's and B's raw hang frames, assert neither similarity crosses the seam threshold) | Declared and unbuilt (same gap as PASS-06). | new file, e.g. `tests/test_pass_middle.py` |
| PASS-08 | `EX-PASS-DOOR` | 3 | A resize or orientation change mid-pass re-measures the destination `hangGeometry` live off the DOM and reframes the camera toward it with no jump (PASS-API §2.6, conformance rows 38–44). | The arrival pose is never carried as a stale copy from an earlier measurement; a mid-pass viewport change never lands the visitor off-position. | pixel + geometry (relative-position assertion at ≥2 viewport sizes, per this pack's geometry rule) | **Built** — PASS-API-V1.md's status block: "§2.6 is built on this branch at `7ee2708`, with 21 conformance rows green." | `tests/test_pass_hang.py` (already covers this — cite shelf 3 explicitly there rather than opening a new file) |
| PASS-09 | `EX-PASS-LEVEL` | 4 — Polyphony | Two cues that both OWN one structural level in overlapping windows are refused; a cue that plays over a level without owning it is not read as contending for it. | A cue's ownership of a level is never inferred from what it merely touches, and an accompanying cue is never refused for standing beside the owner it accompanies. | node (`ownTheLevels`/the levels-law checker, extracted from `pass-composer.js` and run over synthetic overlapping cues) | **Built** — `pass-composer.js` implements `levelOwnership`, the ownership contention law, and the plan-only `levelOwnership` record (grep-verified: the record is written per composed plan). No test names shelf 4 or the ownership/driving distinction today. | new file, e.g. `tests/test_pass_levels.py`, or extend `tests/test_pass_lawful.py` |
| PASS-10 | `EX-PASS-LEVEL` | 4 | A cue's DRIVEN levels — read off the tracks it was actually built with — may differ from its OWNED levels: a cue can own a level and drive nothing on it, or drive a level it does not own. | The ownership check never substitutes "what a cue can move" for "what a cue has claimed," and the driving read never substitutes a manifest's declared level for the tracks a cue actually built (`drivesOn`'s own stated purpose in the source: "reads what the cue can actually move rather than what its manifest says it occupies"). | node (`drivesOn`/`drivenLevelsOf`, extracted and run over cues with tracks that touch a level they do not own) | **Built** — confirmed at `pass-composer.js`'s own `drivesOn`/`drivenLevelsOf`/`levelOf` functions. Untested by any file today. | new file, e.g. `tests/test_pass_levels.py` |
| PASS-11 | `EX-PASS-VOICE` | 4 | A cue's `voice` (budget class) and its `roles` (dramatic function) are two different questions, checked separately; a score naming only one is uncheckable by the other. | The tier-budget check never reads `roles` in place of `voice`, and the composition check never reads `voice` in place of `roles` — the exact conflation PASS-API §4.4 records as having once refused every composed plan as a score. | node | Built (the two fields and their separate checks exist in the shipped composer per PASS-API's own status block). Partially covered by `test_pass_lawful.py`'s R1 (tier budget) but that row does not test the `voice`/`roles` conflation itself. | extend `tests/test_pass_lawful.py`, or new `tests/test_pass_levels.py` |
| PASS-12 | `EX-PASS-VOICE` | 1 — Matter (the miracle as matter's one licensed break) | The tier budget bounds a score's miracle count exactly: zero in `quiet`, at most one in `middle`, exactly one in `culmination` — the one slot the charter licenses a substance change to consume. | A composed score never exceeds its own tier's miracle bound in either direction (a `quiet` score that carries one, or a `culmination` score that carries none, are both red). | node (the shipped `TIERS` table in `pass-composer.js`, run over synthetic cue sets at each tier) | **Built** — `pass-composer.js`'s own `TIERS` table (`quiet`/`middle`/`culmination`, `miracles: [0,0]`/`[0,1]`/`[1,1]`) matches PASS-API §4.4's tier budget check verbatim. Covered generically by `test_pass_lawful.py`'s R1, which cites shelf 17 (the budget's own home) but never shelf 1 (matter's own claim on the miracle slot) or shelf 6 (the miracle law itself). | extend `tests/test_pass_lawful.py` (add the shelf-1/shelf-6 framing as its own row, not folded into R1's shelf-17 framing) |
| PASS-13 | `EX-PASS-VOICE` | 1 | An instrument's manifest `readiness` is one of `production-ready` \| `needs-port` \| `lab-only` \| `failed-proof`; only a `production-ready` instrument's matter may be cast into a shipped score (PASS-API §8: "a port is the instrument's mathematics carried onto the host's frame with a manifest and a passing conformance run"). | A score never casts an instrument whose manifest reads anything but `production-ready` — the matter a crossing plays with is never a lab sketch shipped by accident. | node (manifest census: enumerate every `MANIFESTS[iid]` in `pass-composer.js`, assert `readiness` is one of the four named values, cross-check against what a real score names) | Built (the manifest and its `readiness` field exist and are read by the shipped host). Untested as a standing gate — no row asserts every manifest's `readiness` is one of the closed four, or that only `production-ready` ones reach a shipped score. | new file, e.g. `tests/test_pass_matter_gate.py`, distinct from the existing per-instrument `test_pass_matter.py` (which tests the `matter` INSTRUMENT by name, not the charter's shelf-1 concept) |
| PASS-14 | `EX-PASS-DOOR` | 3 | A pass naming a door its own instrument's manifest leaves blank is refused before it plays (PASS-API §9, conformance row 19). | A score is never handed to an instrument for a door field that instrument's own manifest never declared. | node (manifest-vs-score cross-check, extracted checker run over a synthetic score naming an undeclared door) | Declared; the check is named in PASS-API's conformance list (row 19) but this repo's suite carries no row that names it. | new file or extend `tests/test_pass_score.py` |

## §4 — What this matrix does not cover

Every other clause of `SPEC.md`'s new pass section — the allow-list strip law, the two schema
versions, EdgeMemory/hysteresis, the driver AST, the camera, GPU/resources — already has a home
named in PASS-API-V1.md §9's own conformance list and, in several cases, a green test file in this
repo (`test_pass_drivers.py`, `test_pass_hang.py`, `test_pass_score.py`, `test_pass_api.py`). This
matrix does not re-derive those rows; it names only what was missing for наряд S-16: the composer,
the three readings of "level," and charter shelves 1, 3, 4 and 12.
