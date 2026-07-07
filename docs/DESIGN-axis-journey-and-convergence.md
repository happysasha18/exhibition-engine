# Exhibition Engine — the axis journey and the road to a hung exhibition

_Design document, 2026-07-07. Ordered by Alexander («по максимуму всё продумал… и поделился»).
Written before any spec: this is the thinking the engine's spec will grow from. Every claim about
the lived journey is traceable to tlvphoto's own files; design choices beyond that are marked
as proposals awaiting his word. Genre: each stage leads with the user's story, plain acceptance
criteria follow, formal anchors trail in parentheses._

The engine's promise is a guided journey: a photographer with an archive is taken by the hand
from a folder of images to a living exhibition. Two stretches of that road need real design —
everything else is plumbing that already exists and bakes byte-identical. The first stretch is
**the axis journey**: how a stranger arrives at a feature vocabulary that describes THEIR
photography. The second is **convergence**: how fourteen thousand images become a hung
exhibition of a hundred, a door of fifteen, a walk of ten. This document thinks both through
end to end.

---

## Part I — The axis journey: leading a person to their own vocabulary

### What actually happened at tlvphoto (the evidence)

The vocabulary that now powers the door, the hang and the stories was born in six moves over
two days:

1. **Ingest.** The Instagram export became a catalog of 14,493 records; perceptual hashing
   collapsed 661 near-duplicate groups; nothing was ever deleted (`build_catalog.py`,
   `phash_dups.py`).
2. **Free measurement.** CLIP embeddings for every image, then clustering found **76 visual
   themes** nobody had named yet — vortexes, mandalas, night facades (`embed_clip.py`,
   `cluster.py`).
3. **A proposed vocabulary.** A bank of candidate axes, each with a computable proxy:
   brightness, contrast, warmth, radial symmetry, swirl, busyness, edge character… **28
   survived**; each value carries its source and confidence (`compute_vector.py`).
4. **The correction loop, three rounds.** A local vision model proposed tags for all 121
   finalists; Alexander reviewed on a purpose-built page. Round one's fixed-chip UI failed
   (99 notes written, zero structured tags adopted). Round two's **strike-my-guess** UI worked:
   37 works corrected, and the corrections carried LESSONS, each one a rule («layering means
   overlap», «symmetry is a model: radial, axial, waved», «duotone is bw plus one colour»).
   Round three re-inferred the untouched works under the new rules and he spot-checked: 22
   further corrections. 59 of 121 works were touched by hand — every lesson baked into the
   next inference pass.
5. **Human wins, forever.** An authored value overrides a measured one at confidence 1.0 and
   is never re-inferred (INV-7). A measurement that has no anchor reports null, never zero —
   a mandala score on a picture with no detectable centre is a lie either way (INV-10).
6. **The vocabulary keeps growing.** Today, three days after the first round, a new axis was
   born the same way: time-of-day (night/day/zenith/sunset/unclear), proposed per-image by a
   local vision model, awaiting his correction pass. The journey has a rhythm; a new axis is
   simply one more verse of the same song.

### The productized loop

Everything above compresses into one loop the engine runs with the user, at every scale:

> **PROPOSE → MEASURE → SHOW → the human NAMES and CURATES → RE-INFER → CONVERGE.**

The engine proposes candidates; only measurable things become axes; the human sees real
pictures with the machine's guesses attached and strikes what is wrong in their own words;
the machine re-learns and tries again on what the human left untouched; the loop stops when
the striking stops.

### Stage design (the guided journey's stage 3, E5)

**Story A — «Show me what you noticed».**
A photographer has just ingested their archive. Before any talk of axes, the engine shows the
clusters it found — a page of theme cards, each a grid of eight representative images with a
proposed name. The user renames themes in their own words or merges and dismisses them.
*Acceptance:* every cluster is visible with real images; a rename persists; a dismissed theme
never leads a proposal again; the user's names are the only names any later surface speaks.
*Precondition:* embeddings and clustering are done (they need no human).
*Postcondition:* a named theme map exists, in the user's words.

**Story B — «Propose a vocabulary, in candidates».**
The engine ships an axis bank — the 28 proxies that survived at tlvphoto, organized in
families (tone and light · colour · symmetry · rotational structure · composition · emissive).
For a NEW archive the bank is a starting deck, and the engine deals it honestly: it measures
every candidate axis over the archive and shows the DISTRIBUTION — an axis where the archive
barely varies is folded away as useless for THIS body of work; an axis where the archive
spreads wide is promoted as discriminating. The web may suggest style words for candidate
axes; measurement decides what stays.
*Acceptance:* every axis in the deck has a computable proxy; every proposed axis shows its
real spread over the user's own images; a flat axis is folded automatically and can be
unfolded by hand; nothing enters the vocabulary that cannot be measured (a thing worth saying
that resists measurement becomes a tag, and tags live outside kinship math).
*Postcondition:* a candidate vocabulary with live distributions, awaiting correction.

**Story C — «Let me strike what's wrong».**
The engine runs its vision model over the curated set and opens the correction page: works
grouped by the machine's guess (wrong ones jump to the eye inside a uniform group), each with
a strike-my-guess control and a provenance chip naming who said it — measured, model, or the
user's own earlier word. The UI lesson is law: the user corrects by striking and rephrasing
freely; fixed choice chips are offered only where the value set is genuinely closed.
*Acceptance:* an authored correction wins over any measurement forever (confidence 1.0);
a measurement without an anchor shows null and asks nothing; the page works offline; the
correction leaves as a file the engine can read back (today Save-JSON; the local
pseudo-backend replaces the Downloads dance when it lands).
*Postcondition:* a correction file, plus the round's lessons stated in plain sentences.

**Story D — «Learn my lessons and try again».**
Corrections carry rules, and rules retrain the prompt: the engine folds the round's lessons
into the inference instructions and re-runs ONLY the works the human never touched, then asks
for a spot-check. Rounds repeat while the correction rate stays high.
*Acceptance:* re-inference never overwrites an authored value; each round's correction rate
is measured and shown; the loop proposes to stop when a spot-check round corrects under
roughly one work in ten (the exact threshold is his to set — tlvphoto converged in three
rounds: 37 → 22 → done); the lessons file persists as part of the instance, so a future
re-run starts wise.
*Postcondition:* a vector layer over the curated set, every value carrying source and
confidence — the same shape tlvphoto's `vector.json` carries today.

**Story E — «A new axis can be born any day».**
Months later the user wants a new dimension (tlvphoto's time-of-day is the precedent: EXIF
was useless because the work is heavily composited, so the model reads the picture itself).
The engine treats a new axis as one more pass of the same loop over the existing curated set:
propose per-work values, open the correction page, fold the corrections, done.
*Acceptance:* adding an axis touches no existing authored value; the new axis declares its
consumers (which surfaces will read it) before it runs, so an axis nobody reads is refused.

---

## Part II — Convergence: from an archive to a hung exhibition

### The funnel, with tlvphoto's real numbers

| Stage | Count | Who decides |
|---|---|---|
| Raw archive | ~14,500 | nobody — it all comes in |
| After near-dup collapse | ~13,800 | the machine proposes, groups stay inspectable |
| Visual themes | 76 | the machine finds, the human names |
| **Finalists** | **121** | **the human picks, the engine assists** |
| Door pool | 15 (5 poles × 3) | the human curates from engine proposals |
| One visitor's walk | ~10 | the machine deals, live, from the pool and vectors |

The design law of the whole funnel: **the engine narrows, the human decides.** Every automated
stage produces proposals with provenance; every human stage leaves a record of what was picked
and why it was reachable (tlvphoto's `finalists_provenance.json` traces each finalist to its
source cluster and theme — that pattern becomes the engine's standard).

### Stage design

**Story F — «Help me pick finalists out of thousands».**
Nobody reviews fourteen thousand images. The engine deals the archive cluster by cluster:
each theme's representatives first, near-duplicates pre-collapsed to their best member, the
user picks with one keystroke per image. As picks accumulate the engine reports COVERAGE —
which named themes are represented, which stand empty — and warns when two picks are
near-duplicates of each other. Sections (tlvphoto's constructed/coda/found) are the user's
own invention; the engine records them and never proposes its own.
*Acceptance:* every archive image is reachable but the default road is theme-by-theme;
a pick records its provenance (cluster, theme, dup-group); the coverage report updates live;
finishing does not require touching every theme — an empty theme is a statement too.
*Postcondition:* a finalists set with provenance, the exhibition's body.

**Story G — «Build me a door of honest contrasts».**
The door needs a small pool of works so unlike each other that a stranger's pick actually
says something. The engine proposes poles by farthest-point sampling over the vector layer
(the same math the cold hang uses today), then shows the proposal as a board: candidate
poles, three works each, with the axes that drive the contrast named in plain words. The
human renames the poles, swaps works, deletes and adds. Pole names are the user's language
(tlvphoto's warm/nocturnal/geometric/soft/vivid were curated by hand).
*Acceptance:* the proposed poles are maximally spread by measurable axes; the human's final
pool overrides any proposal; the baked pool carries its measurements invisibly (visitors
never see numbers); pool size and pole count are instance config.
*Postcondition:* a door pool the walk's living hand deals from.

**Story H — «Hang it and let it live».**
From here the built machinery takes over: the hang, the kinship walk, the series rooms, the
seen-list memory, the stories. Convergence design adds one thing: a REHEARSAL — before going
live the engine walks its own exhibition headlessly (cold arrival, pick, unfold, return
visit) and shows the user what a stranger will meet, as screenshots. The user's eye is the
last gate, on real renders.
*Acceptance:* the rehearsal runs the instance's own bake, on synthetic visitors, and produces
a visual report; going live is a separate, explicit step that never runs unasked.

### How Part I feeds Part II

The vocabulary pays for itself down the funnel: clusters propose finalists (F), farthest-point
over axes proposes the door (G), kinship over axes deals the hang and orders the walk (H),
and per-work marks like time-of-day give the told story its objective plot. An axis that
feeds none of these is dead weight — which is why Story E demands every new axis name its
consumers before it earns compute.

---

## Open decisions (his word shapes the spec)

1. **The v1 deck.** Ship all 28 surviving axes as the starting bank, or a core dozen (tone,
   warmth, saturation, radial, busyness, edge character…) with the rest behind an
   «unfold more» — my lean: core dozen, the full bank one click away. ⟨DECIDE⟩
2. **Journey surface.** The guided journey as CLI prompts, or as a local page the CLI opens
   (theme cards, correction pages and boards all want a browser anyway) — my lean: a local
   page per stage, one thin CLI that opens them in order. ⟨DECIDE⟩
3. **Correction persistence.** Keep Save-JSON→Downloads for v1, or pull the local
   pseudo-backend forward (his 2026-07-07 wish, queued at tlvphoto) so every review page
   writes straight into the instance — my lean: pseudo-backend first, it removes the
   journey's clumsiest gesture for every stage at once. ⟨DECIDE⟩
4. **Convergence threshold.** The stop-proposal number for correction rounds (draft: a
   spot-check round correcting under ~10% proposes to stop). ⟨DECIDE⟩
5. **Model floor.** The journey assumes a local Ollama vision model (qwen3-vl-class). Does
   v1 also offer an API-model road for machines too small to run one? ⟨DECIDE⟩

_Sources: tlvphoto's scripts and data files (`build_catalog.py`, `phash_dups.py`,
`embed_clip.py`, `cluster.py`, `compute_vector.py`, `vector.json`, correction rounds of
2026-07-04, `finalists_provenance.json`, `door_candidates.json`); the engine's own
NEXT_STEPS product vision (his words, 2026-07-07 night); today's time-of-day marking run._
