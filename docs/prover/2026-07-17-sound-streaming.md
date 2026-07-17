# Prover — EX-SOUND streaming swap (2026-07-17)

Mode: CROSS-LINK (single-module behaviour change, one clause, one test). Short-form record
(SPEC INV-61): the delta swaps the ambient player's playback mechanism from a Web Audio
full-decode (`decodeAudioData` → looping `AudioBufferSourceNode`) to a streaming `<audio>`
element routed through a `MediaElementAudioSourceNode` → gain node for the fade. Design derives
from the recorded wish (instant response over gapless; a faint loop seam accepted; pause/resume
simplifies to the element's own `currentTime`). No fork.

## Regression fences — the neighbouring promises this delta must not break

| Fence | Clause | Verdict |
| --- | --- | --- |
| Player OFF by default; no cold-load fetch; arm on first gesture for a return-ON | `INV-27` `INV-48` | HELD — turn-on still gated on the deliberate tap; a return-ON still arms on the first gesture (autoplay is blocked; both the element's `play()` and the context's `resume()` need it) |
| The player retracts under every covering face (door, side room, cards, zoom) | `INV-77` | HELD — the `#ex-sound` box, its classes, and the retract CSS are untouched; the delta lives inside the playback functions only |
| A missing / failed file fails SILENT | `INV-1` | HELD — a media error hides the player with no throw and no beat (a missing audio file is expected-silent, not the error beat's `script`/`promise` fault) |
| The choice persists in `ex.sound` | `EX-SOUND` | HELD — `persist()` unchanged |
| Two beats ride the existing wire (`sound_on` / `sound_off`) | `EX-PULSE` `INV-41` | HELD — the `pulse()` calls in `setDesired` unchanged |
| The box arrives on the breath | `EX-ARRIVE` | HELD — box creation + `requestAnimationFrame(...add("show"))` unchanged |
| Volume slider ≥44px, default 0.3 | `EX-SOUND` | HELD — DOM/CSS unchanged |
| Plays continuously across the whole single-page walk, never torn down on a face change | `INV-48` | HELD — one persistent element + graph; face changes never touch it |

## New seam — the one thing the delta introduces

`MediaElementAudioSourceNode`. Two constraints the code must respect, both checked at the code step:
- A `MediaElementSource` may be created ONCE per element, and once created the element's audio
  routes ONLY through the graph — so the gain node MUST connect to `ctx.destination` or the sound
  is silent. Create it lazily, once, on the first `prepare()`.
- The AudioContext still needs a gesture-time `resume()` (unchanged from the decode path).

## Edges folded into the code step

- A fast off→on toggle during the fade-out must cancel the pending `pause()` (the element must not
  pause after the visitor re-enabled it). Guarded by re-reading `desired` before pausing + a cleared
  timer.
- The fade-out advances `currentTime` while ramping to zero — the playhead moving during an audible
  fade is natural; the resume continues from the faded-out point. Acceptable.

## Open ⟨DECIDE⟩ touched: none. Findings: none blocking; edges above fold into code.
