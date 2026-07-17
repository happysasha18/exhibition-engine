# Prover — EX-STORY-BEAT / INV-89 cold-test unified + grace (2026-07-17)

Mode: CROSS-LINK (one surface, the door-pick crossing). Reviewer hat: formal-methods.

## The change under review
INV-89's loading beat gains a **unified cold-test** (`beatDone = picDone && storyDone`, was mutually
exclusive) and a **grace window** (`beat_grace` ≈ 0.45s ×tempo): a near-instant open where both sides
settle within grace shows NO centre pulse; the pulse builds only when a side still travels past grace.

## Entities / states / transitions
- `picDone` — the picked work's room-tier decode has resolved (or the guest is under Save-Data / reduced,
  where the picture side is never awaited). `storyDone` — the arc's first portion settled, or the voice is
  off. `beatDone = picDone && storyDone`.
- pick → arm `storyDone` (voice on) and `picDone` (`!dataSaver && !REDUCED`) independently → wordmark beat
  (0.92): if `!beatDone`, arm a grace timer → grace (0.92+`beat_grace`): if still `!beatDone`, `beatFly()` →
  reveal beat (1.78): `beatDone||REDUCED` ⇒ `land()`, else hold to settle-or-`beat_hold`-cap → `land()`.

## Findings (folded into the code brief before implementation)
| # | Finding | Verdict |
|---|---------|---------|
| F1 | **Save-Data leak.** Unifying naively (always read `rim.decode()`) would fetch the room-tier image early even under Save-Data with the voice on — violating the Save-Data class law (EX-LOAD-3, one `saveData` home). FOLD: `picDone` is awaited only when `!dataSaver() && !REDUCED`; otherwise `picDone=true` (no early fetch, no block). | folded |
| F2 | **Stranded grace timer.** A grace timer firing after `ceremonyCancel` (Back mid-beat) would build a pulse into a torn-down ceremony. FOLD: the grace timer rides `cerAfter` (pushed to `cerTimers`, cleared by cancel) AND double-guards with the generation `ok()` check and a fresh `!beatDone` read. | folded |
| F3 | **Voice-on picture correctness (the latent defect this fixes).** Today, voice-on keys `beatDone` on the story alone; a fast story + slow picture reveals onto a plate. The unify makes voice-on wait for the picture too — strictly more correct, no regression to the story-hold rows (their fixture picture is warm). | folded (this IS the fix) |
| F4 | **Site SPEC drift (pre-existing, fixed in this change).** `~/tlvphotos/SPEC.md` INV-89 still said "story OFF ⇒ no pulse element" and "the hold waits only on the story, never on pixels" — stale since the morning story-off loader shipped in the engine. Brought current to shipped truth in the same edit. | folded |

## Safety / liveness / composition
- Safety: `beatFly` builds at most one clone (`if (beatEl) return`); `ceremonyCancel`→`beatKill` tears it
  down; the grace timer is gen-guarded (F2). No pulse survives a cancel.
- Liveness: reveal always fires — `land()` at 1.78 when done, else at the `beat_hold` cap. Grace never gates
  the reveal (independent path). Fails-open preserved.
- Composition: reduced motion ⇒ `land()` at 1.78 regardless, `beatFly` self-guards REDUCED — no pulse.
  Save-Data ⇒ picture side never awaited (F1); voice-on story pulse unchanged (costs no extra network).
  `INV-25` warm-open-at-once preserved (both sides already settled ⇒ `beatDone` at the 0.92 beat ⇒ no grace,
  no pulse). One history step, in-flight lock, Back-cancel all unchanged.

## Open ⟨DECIDE⟩ / taste
- `beat_grace` default 0.45s ×tempo is a `[default]` (his tune). Raising it toward the 0.86 reveal-gap makes
  the beat skip ALL opens under the reveal point; lowering it keeps the pulse earlier. His eye owed on a real
  machine — motion feel is his meter.
- Queued (not this change): EX-STORY-BEAT/INV-89 lives in BOTH the engine and site SPECs (one-home smell).
  A later restructure row consolidates; not touched here to keep the delta scoped.
