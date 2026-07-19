# Prover — EX-SOUND-GREET / INV-101 first-visit greeting (2026-07-19)

Mode: CROSS-LINK (one clause, four owning seams). Reviewer hat: formal-methods.

## The change under review
`EX-SOUND-GREET` / `INV-101`: the resting sound control's glyph becomes a music note (was the play
triangle). On the visitor's first VISIBLE arrival — the player retracts under the door, so the wait
gates on `getComputedStyle(box).opacity>0.5 && !body.ex-door` — a localized word («sound?», English
fallback) breathes in beside the note, holds, then settles away, leaving the bare note. The once-ness
is written to `ex.sound` (`greeted`) the moment the word first shows, so a return visit meets only the
note. Reduced motion / Save-Data stand the choreography down entirely (note rests unmarked, so a later
ordinary visit may still greet once).

## Entities / states / transitions
- `greeted` (bool, seeded from `pref.greeted`, `false` on a fresh/cleared `ex.sound`) → `waitVisible()`
  rAF loop (capped ~600 tries / ~10s) polls the visible-gate → `greetOnce()`: sets `greeted=true`,
  `persist()`s immediately, appends `.exsnd-greet` (aria-hidden), fires the `exsnd-greet-io` keyframe →
  `animationend` self-removes the span. The bare `.exsnd-note` glyph is present in the button markup
  throughout — it is never created or destroyed by the greeting, only the transient span layers beside it.
- Guard order in the IIFE: `if (greeted || REDUCED || dataSaver()) return;` gates entry to the whole
  wait loop, not just the append — so reduced-motion/Save-Data visitors never even start polling.

## Findings
| Finding | folded / rejected | why |
|---|---|---|
| **EX-SOUND control it extends** — does the note-glyph swap break the playing-state visual (the equalizer bars vs. the note)? | folded (already correct, no change needed) | CSS rule `#ex-sound.playing .exsnd-note{ display:none; }` (exhibition.css:445) hides the note once `.playing` is added by `start()`; the equalizer (`.exsnd-eq`) is the only playback indicator, matching the pre-existing INV-1 contract ("the equalizer bars, not the button, signal actual playback"). The greeting span is a sibling, unaffected by the playing class. Verified live: `.exsnd-note` markup coexists with `.exsnd-eq` in the button, no selector collision. |
| **EX-I18N** — does the word actually localize via `SNDT.sound_greet`, with `SOUND_GREET_EN` as a true fallback (not a silent dead key)? | folded | `98-sound.js`: `g.textContent = SNDT.sound_greet \|\| SOUND_GREET_EN;` — same fallback shape as `a11y_volume`/`a11y_sound` two lines above it, so it rides the existing EX-I18N wiring (deferred locale fetch, KV-cached) rather than inventing a second path. `SOUND_GREET_EN = "sound?"` declared once in `01-knobs-lang-history.js`, source-tongue literal. No dead key: absent a translation the English literal always renders. |
| **EX-ARRIVE / visibility timing** — does the greeting truly wait for the player to be visible on the walk, and does the door retract it? | folded | `waitVisible()` reads `getComputedStyle(box).opacity>0.5 && !document.body.classList.contains("ex-door")` every rAF tick — it does not fire on cold load (box is under the door, opacity 0, `ex-door` class present) and only proceeds once the walk is entered. Browser row (test_sound.py, EX-SOUND-GREET first-visit row) confirms: `greeted` flips true and `.exsnd-note` renders only after `enter_walk()` — i.e., past the door, never before. The ~10s / 600-try cap (silent give-up, no error) matches the "never left the door" case the comment names — a visitor who abandons at the door simply never greets that load, and `greeted` stays false for the NEXT arrival to retry, since nothing persists until the word actually shows. |
| **`ex.sound` persistence** — is `greeted` written the moment the word shows (not on some later event), and does a return visit that stays fully silent (never toggles sound on) still carry it forward? | folded | `greetOnce()` calls `persist()` synchronously right after setting `greeted=true`, before the DOM append — so the write is not contingent on the animation completing or the visitor doing anything else. `persist()` always serializes `{v, on: desired, vol: target, greeted}` together — a silent visitor who never toggles `on` still gets `greeted:true` written into the same JSON object test_sound.py's new browser row confirms directly: reload+re-enter after a first-visit-only load (no toggle) shows no `.exsnd-greet` on the second walk entry, proving the flag survives with no sound ever turned on. |

No unresolved `⟨DECIDE⟩` found in the `EX-SOUND-GREET` clause or its two index rows (SPEC.md:662-672,
:1553, :1677) — `sound?` is stated as a fixed source-tongue literal, not a placeholder; the visible-gate,
the once-ness write point, and the reduced-motion/Save-Data stand-down are all fully specified with no
open taste question left in the prose.

## Safety / liveness / composition
- Safety: `greeted` can only ever be consumed once per stored pref (`if (greeted) return;` at both the
  outer gate and inside `greetOnce`); the visible-gate ANDs two independent conditions, so a reduced/
  Save-Data visitor's early return means the wait loop never starts at all — no dangling rAF chain.
- Liveness: an ordinary visitor who reaches the walk always resolves within ~10s (opacity settles well
  before the cap in practice) or gives up silently without corrupting `greeted` — a later visit gets
  another chance since nothing was written.
- Composition: greeting is layered strictly beside the existing control (sibling span, self-removing on
  `animationend`) — it touches no existing playback state machine (`desired`/`playing`/`armed`), and
  `persist()`'s shape simply gained one field, read-compatible with pre-`INV-101` prefs (`pref.greeted`
  undefined ⇒ falsy ⇒ greets once on the first load after the upgrade, the intended migration behavior).

## PASSES cross-link. No unresolved ⟨DECIDE⟩.
