# The transition — how tlvphoto will one day ride this engine (and not a day sooner)

_His law, 2026-07-07 night: two lanes until the cutover is EARNED. This note is the thinking he
asked for («продумать когда транзишен»); the cutover itself is queue row E8 and opens on his word._

## The two lanes, until then

- **Lane 1 — tlvphoto (production).** Lives on its OWN `scripts/build_site.py` + its own suite.
  Every visitor-facing change keeps landing HERE first — the live site never waits for the engine.
- **Lane 2 — exhibition-engine (the product).** Grows beside it; borrows tlvphoto's shipped truth
  (verbatim asset re-syncs, the drift report as the checklist) but never writes back into it.
  The flow of code is ONE-WAY (instance → engine) until cutover; after cutover it reverses
  (engine → instance) and never mixes.

## What the cutover must have EARNED first (the gate, all four)

1. **Byte-identical proof, continuously** — `engine/build.py --content ~/tlvphoto` reproduces
   tlvphoto's own bake bit-for-bit (256+ files, empty diff), re-proven after every engine change
   (a standing check, not a one-time demo).
2. **The engine is green ALONE** — its own suite passes on a synthetic labelled archive, no
   private content required (E3): a user without Alexander's photos gets a working product.
3. **The generic seam holds a SECOND instance** — at least one toy instance (different photos,
   different axes, different strings) bakes and walks correctly; one consumer is no proof of
   genericity.
4. **The method travels** — the guided journey (install → ingest → axes → curate → bake) runs
   end-to-end at least once by the book, because the transition swaps not just code but the way
   the site is WORKED ON.

## The cutover itself (when his word opens E8)

- One movement, reversible: tlvphoto pins an engine VERSION (a tag, not "latest"), replaces
  `scripts/build_site.py` with the engine call behind the five instance strings + content dir,
  keeps its own tests running against the engine-built bundle for a full cycle.
- tlvphoto's suite stays the arbiter: the cutover lands only with tlvphoto's own gate green on
  the engine-built site AND the live deploy byte-verified, like every landing before it.
- Rollback = one commit revert (the old script stays in the attic, never deleted).

## What never transitions

Alexander's content, curation, taste files, decision archives, keys — the instance is private
by construction; the engine repo carries none of it (the publish gate at E7 re-checks this
before anything goes public).
