# Prover record — EX-ZOOM pinch entry/exit symmetry (INV-82, INV-83)

Date: 2026-07-15 · Mode: CROSS-LINK (the new zoom-symmetry clauses against EX-SERIES, EX-CHROME/INV-77,
EX-COMPOSE/INV-67, EX-PROTECT, and the existing zoom invariants INV-75/76/81). Reviewer: fresh-context
product-prover pass. Every finding folded into SPEC.md the same session.

| # | Severity | Seam | Finding | Folded? |
|---|---|---|---|---|
| 1 | must-fix | INV-83 vs EX-SERIES/EX-DOOR | close target said "the walk" but the zoom opens over walk / door window / side-room print; × already returns to the room | FOLDED — INV-83 + prose + success measure now say "the surface it was opened over" |
| 2 | must-fix | INV-67 one-face law | zoom is a face yet opens OVER another face; "two never summoned together" was false | FOLDED — INV-67 row + one-face prose name the zoom as the one face that stands over another |
| 3 | must-fix | INV-83 nested popstate | zoom step must sit above the beneath-face's step; topmost consumes Back; no walk_exit miscount | FOLDED — INV-83 row + prose state the nesting, top-consumes-Back, and no walk_exit/series beat |
| 4 | must-fix | INV-82 entry-scale vs INV-81 | two drivers of the same scale value unreconciled | FOLDED — INV-82 makes entry a position/origin animation only; live pinch distance is sole scale authority |
| 5 | recommendation | INV-77 "nothing moves" | picture now scales up on open | FOLDED — INV-77 narrowed to "no control or layout shifts (the entry scale-up is the sole motion)" |
| 6 | recommendation | INV-75 stale close list | omitted pinch-out + Back | FOLDED — INV-75 row appends "a full pinch-out, or the browser Back (INV-82, INV-83)" |
| 7 | recommendation | INV-82 "not a fade" vs reduced-motion fade | contradiction | FOLDED — INV-82 splits it: the picture scales (never fades), only the dark backdrop fades |
| 8 | question | rotation under zoom vs scale-back-to-place | which place on close | FOLDED — INV-82: close scales to the source's freshly-measured place, taken as the beneath-face re-centre, one settle |
| 9 | question | dismiss "on its own" vs "on release" + hysteresis | ambiguous gesture | FOLDED — INV-82: commits on release below threshold; below-1× previews; pinch back above threshold cancels |
| 10 | recommendation | missing fences INV-67, INV-46 | — | FOLDED — EX-ZOOM regression fences now cite INV-46 (side room step/lock) and INV-67 (one-face) |

**Sound (confirmed, no hole):** INV-76 recentres at 1× before dismiss can begin (panned state resolves
cleanly); backdrop-tap-vs-pan closed by the existing facet; accessibility core (role=dialog aria-modal,
× ≥44px + aria-label, present throughout, Esc) carried; reduced-motion instant-swap restores INV-81;
one-step-per-face (INV-18e) consistent. Open minor thread: focus-trap behaviour during the entry
scale-up left unstated (not gating).
