# exhibition-engine — NEXT STEPS (resume file)

_The GENERIC engine behind tlvphotos.com, founded as its own PRODUCT on Alexander's word
(2026-07-07 ~00:30): «движок должен быть генерный… установка Ollama, определение осей — весь
процесс объяснить пользователю и провести пользователя. Это огромное движение.» Named by his
decision answer: **exhibition-engine**. Method: the live-spec pack, loaded per session._

## ⚡ RESUME NOW (2026-07-10 ~09:45) — CUTOVER DONE: tlvphotos.com's deploy.sh now bakes via THIS engine; next lanes = publish pass (repo goes PUBLIC) + own-client catch-up

**On Alexander's morning word (drive to full parity), the flip landed in the instance repo
(`2fb243c` there): its `deploy.sh` calls `engine/build.py --content . --site site.json` — this
engine is now the ONLY baker of tlvphotos.com. Proof the same morning, all fresh: instance suite
30/30 · this suite 25/25 · byte-diff engine-bake vs the old build_site.py bake EMPTY (625/625) ·
the flipped recipe re-proven byte-identical before commit. The instance repo is RENAMED
`exhibition-engine-tlvphotos` (private); THIS repo goes PUBLIC after the publish pass below.**

**LANES (in order):**
1. **Publish pass (before the visibility flip — his final word flips it):** working docs
   (NEXT_STEPS, TRANSITION.md, PORT_REPORT.md, CHECKPOINT.md, tests/E3_REPORT.md) carry his name
   and machine paths — move their live state into the instance repo or scrub; `example/site.json`
   becomes a SYNTHETIC example (the real identity now lives in the instance repo); README per the
   publish gate (install, commands, when-to-use, a real run); license = his call; the two
   Alexander-comments in build.py/exhibition.js get neutral wording.
2. **Reverse the code flow:** point the instance's tests at the engine bake, retire its
   `scripts/build_site.py`.
3. **Own-client lane (unchanged, not blocking):** quiz_util `arm_of()` ↔ client `quizHash`
   alignment + parity row · `window.__tlvSeen`/`tlv.` prefixes · generic client catch-up
   (FOUC guard, single-answer worker model).
4. story_notes.json staleness watch (unchanged).

## superseded (2026-07-09 ~22:38) — CUTOVER GATE 1 GREEN: byte-diff EMPTY (625 files); his eye on the compare is the only gate left

**The fork below is RESOLVED by his word tonight («я не понимаю что такое сведение клиентских
ассетов… сделай синхрон, зачем ты меня спрашиваешь») — I picked, and the sync landed as three
contract moves (`f6adc3f`, suite 21/21, pushed), none of which de-generalizes the engine:**
1. **Instance client override** — `exhibition.js/.css` + the worker TEMPLATE come from the
   instance's assets dir when present (`client_asset()` in build.py); the `?v=` hash rides the
   SERVED client. tlvphoto ships its grown client byte-exact; the generic client serves new instances.
2. **Suppressed-at-default config** — a knob at its built-in default/empty is omitted from the
   served config.json (all client reads are fallback-guarded); `site_name` emits only with the
   engine's own client. SPEC + the two pinned rows (test_sound 1-2, test_quiz 5) updated in lockstep.
3. **Story notes content-contract** — `<content>/story_notes.json` (flat id→his-word note) rides
   into the worker fragments; tlvphoto's file generated from `alexander_labels_2026-07-04.json`
   (99 notes) beside the mapped quiz.json. tlvphoto also adopted ONE line: `quiz_win` joined its
   i18n chrome list (a localization improvement, invisible to current locales).
Plus the same-evening centering fix (`ba4025d`): measured frame stops (see tlvphoto NEXT_STEPS cont.70).

**PROOF (2026-07-09 ~22:30):** `engine/build.py --content ~/tlvphoto --site example/site.json
--site-url https://tlvphotos.com --ga-id G-00J4KGDHCG --enable ai_i18n --enable visitor_memory
--enable ai_story --enable quiz --display-max 1000 --instance-assets ~/tlvphoto/assets_src`
→ `diff -rq /tmp/eb ~/tlvphoto/site` **EMPTY, 625 files each side** (tlvphoto side baked by its
own build_site.py with the same prod flags). Engine suite 21/21 on the synthetic fixture (no
override → generic client, so the engine's own lane stays proven).

**LEFT (his gates + owed rows):**
- **His eye on the compare, then the prod flip on his OK** (TRANSITION E8's last step): deploy the
  ENGINE-baked bundle to tlvphotos.com, then reverse the code flow (engine → instance).
- **Engine-own client catch-up** (not blocking, its own lane): the generic exhibition.js/css are
  BEHIND tlvphoto's on content (header FOUC guard, comment rewrites) and the generic worker.js
  still judges by the OLD accept-set model — modernize to the canonical single-answer model
  (INV-64) + port the FOUC guard; engine quiz tests ride along.
- **OWED cleanup (unchanged):** `window.__tlvSeen` + residual `tlv.` localStorage prefixes in the
  generic client — generalize in a focused pass.
- **tests/quiz_util.py `arm_of()` disagrees with the generic client's own hash** (found during the
  quiz-funnel port, 2026-07-10 ~04:00): the util keeps tlvphoto's avalanche formula while the
  engine client draws the arm with its Knuth-finalizer `quizHash` — same token, different arm.
  Pre-existing; the FL tests bypass the util with tokens verified against the client's formula.
  Fix = one owner: align the util to the client's formula (or export the client's hash like
  tlvphoto's `TLVQuiz._hash` parity row) + a JS↔Python parity test.
- **story_notes.json staleness:** the file is a mapped SNAPSHOT of his labels; if he edits notes,
  regenerate (the byte-proof catches drift in _worker.js).

## superseded below (2026-07-09 ~16:10) — PARITY CATCH-UP landed; cutover (regenerate prod FROM the engine) is next

**Four features ported from tlvphoto to full parity, each through the engine's own suite — `run_all.py`
21/21 green (wall ~126s, senior re-run via `.venv`). NOT yet pushed; commit batch pending.**
- **Chip glint** (`EX-QUIZ-GLINT`): a soft one-time light sweeps the plaque «question?» chip as it appears.
- **3 walk fixes**: the cold-arrival line (`#ex-loading`, text from config `loading_line`), finale caption
  clears on the closing screen, door rebuilds without a re-fade on aspect change.
- **Image ladder** (`EX-LADDER`/`INV-63`): the display-cap bake writes clean 640/960/1280 tiers + per-work
  `srcset`; a `.venv` with Pillow was added so the tier bake is really tested.
- **4-option quiz redesign** (`INV-64/65/66`): tap-of-four card over the visible photo, one-per-show pick +
  cooldown, private single answer judged at the edge, tint + lock + RTL, `quiz_win`/`quiz_wrong`. Ported by a
  Sonnet worker on a written brief (`.quiz-4option-port-checkpoint.md`), senior-verified by deed. `test_quiz`
  rewritten to the 4-option model. The worker also fixed a pre-existing shim gap (`_copy_assets_capped` was not
  re-exported → `test_site` was silently red before this session; now green).
- SPEC.md folded to shipped truth (the quiz section + `EX-QUIZ-ONCE`/`GLINT`/`LADDER` + `INV-63/64/65/66`).

**OWED cleanup (his word 2026-07-09 — recorded here rather than racing the worker):** two pre-existing
tlvphoto literals in the engine (NOT from this session) — `window.__tlvSeen` (the EX-MEMORY coat-check hook,
`exhibition.js` ~816/1675) and any residual `tlv.` localStorage prefixes — generalize in a focused pass.

**NEXT MOVEMENT — the cutover (his word 2026-07-09, «перегенерить сайт опираясь только на репо движка + мои
данные»):** this is TRANSITION.md's E8. Plan the senior self-drives after the parity push:
1. map tlvphoto's content into the engine content-contract (incl. a 4-option `quiz.json`);
2. gate 1 — bake `engine/build.py --content ~/tlvphoto …` and prove BYTE-IDENTICAL vs tlvphoto's own bake
   (empty diff) — fix any generalization drift to zero;
3. show Alexander the compare (engine-built vs live) BEFORE any prod touch;
4. on his OK, deploy the engine-baked bundle to tlvphotos.com; then reverse the code flow (engine → instance).
Two hard gates: empty byte-diff before prod is touched, and his eye on the compare before the flip.

### CUTOVER — PROGRESS 2026-07-09 ~18:10: byte-diff 253 → 6 (all mechanical + content buckets DONE)
Reconciled + VERIFIED against `~/tlvphoto/site`, each committed+pushed (engine suite 21/21):
- 122 images — the mark-split (`copy_gallery(mark_text=None)`, served base is CLEAN). `ac6cda3`
- 122 work pages — served-dims OG + artform/ImageObject JSON-LD + srcset attr in render_work. `ac6cda3`
- robots AI-blocks; audio copytree. `ac6cda3`
- index.html served-dims + `?v=<hash>` asset-version + `loading_line` (site.json); sitemap `<lastmod>`. `9d6bc2a`
- 4-option quiz content-contract: mapped `~/tlvphoto/quiz.json` (tlvphoto `08527b0`) → exhibition_data.json
  + the quiz-prize derivative now byte-identical; i18n quizzes array. `d4b11a8`

**The 6 that REMAIN are ALL one class: the engine's GENERALIZATIONS vs tlvphoto's EXACT current bytes —
this IS the «show the comparison» content, HIS gate, NOT more auto-hammering.** They are:
- `exhibition.js` + `exhibition.css` + `_worker.js` — client assets. The engine's are generalized
  (`window.EXQuiz`↔`TLVQuiz`, slug `ID_RE` `/^[a-z0-9…]/i` ↔ numeric `/^\d{5,25}$/`, and _worker.js is on
  a DIFFERENT quiz-judging model than tlvphoto's shipped one) AND tlvphoto has the swipe fix the engine
  doesn't. A verbatim clobber REVERTS the engine's generalizations and BREAKS its own tests (measured).
  **_worker.js finding (2026-07-09 ~19:10):** the divergence includes the EDGE QUIZ-JUDGE itself — the
  engine is a rewrite to a single exact `answer:"City"`, tlvphoto's shipped worker judges by an `accept:[…]`
  spelling-set + normalize. Different code AND different private bake shape (the mapped quiz.json gives the
  engine `answer`; tlvphoto bakes `accept`). The engine's own quiz tests encode the single-answer model, so
  this file is a genuine which-model-is-canonical call, part of the fork — not a rename.
  **LOOP PAUSED here (2026-07-09 ~19:10):** all safe autonomous work done (253→6); everything left needs his
  fork pick. Resume: he answers a/b/c → do the per-file merge that way → re-prove byte-diff to empty → show him.
- `config.json` — engine emits 5 knobs tlvphoto omits: `glide_ms`, `quiz.placement`, `sound_url`,
  `sound_credit`, `site_name`.
- `i18n_source.json` — one line: engine localizes `quiz_win`, tlvphoto doesn't.
- `index.html` — ONLY the `?v=` hash, which is derived from exhibition.js/css → resolves the instant those match.

**THE FORK (his call):** (a) hammer the engine DOWN to tlvphoto's exact bytes (de-generalizes the engine,
drops its improvements, drops the swipe) — wrong for a product engine; (b) bring tlvphoto UP to the engine
(adopt generalized tokens + quiz_win localization; port the swipe into the engine) — the cutover's actual
direction, but the token rename touches tlvphoto's LIVE client; (c) bake-time token substitution (engine
keeps generalized source, build.py stamps the instance's tokens at bake) — most work, cleanest long-term.
**SAFE autonomous step — DONE `a7259e7`:** the swipe fix is now in the engine's own assets (glide 8/8, suite
21/21). It no longer contributes to the byte-diff. IMPORTANT finding: the exhibition.js/css gap is NOT only
generalization tokens — tlvphoto also has later CONTENT the engine lacks (e.g. the header FOUC guard
`html.js .ex-head{display:none}`, reworded comments). So the reconciliation is a per-file MERGE (engine is
behind on content AND ahead on generalizations), and the fork picks HOW to merge. **Autonomous-safe work is
now EXHAUSTED — the remaining 6 all wait on his fork call.**
_(superseded plan line below — index/sitemap/quiz are now DONE)_ Next tick: index+sitemap (mechanical), then the quiz content-contract, then surface the
asset-token + config decisions to Alexander (they touch tlvphoto's live code / the engine's identity).

### CUTOVER — MEASURED STATE 2026-07-09 ~17:10 (gate 1 is RED; the engine is materially BEHIND tlvphoto)
Baked the engine against live tlvphoto content with tlvphoto's real prod flags and diffed vs tlvphoto's
own fresh bake (`~/tlvphoto/site`, rebaked minutes earlier by the swipe deploy — a valid baseline):
```
~/tlvphoto/.venv/bin/python engine/build.py --content ~/tlvphoto --site example/site.json --out /tmp/eb \
  --site-url https://tlvphotos.com --ga-id G-00J4KGDHCG --enable ai_i18n --enable visitor_memory \
  --enable ai_story --enable quiz --display-max 1000 --instance-assets ~/tlvphoto/assets_src
diff -rq /tmp/eb ~/tlvphoto/site
```
**Result: 253 files differ — NOT byte-identical.** The "full parity" note above (cont.68 catch-up) was
optimistic; build.py-side parity was NOT reached. The drift, by bucket (each = a reconciliation row):
1. **Image pipeline — 122 JPGs differ (same 1000×1000 dims, SAME Pillow 12.2.0 → different bytes).** So it
   is CODE drift in the engine's resize/mark/encode path, NOT a Pillow-version issue (ruled out by baking
   the engine under tlvphoto's own `.venv`, Pillow 12.2.0 — still 122 differ). The engine's OWN `.venv` also
   carries Pillow **11.3.0** on an older Python that can't even fetch 12.2.0 — a second, separate env gap to
   pin once the code path matches. Find the exact divergence by diffing the resize/mark functions.
2. **Work pages — 122 `w/*.html` differ**, all from build.py emission the engine lacks: served-dims OG
   (engine emits 1440, tlvphoto 1000 — INV-56/57 `served_dims`), `"artform":"Photography"` + the ImageObject
   JSON-LD (INV-58), and the `srcset`/`sizes` image-ladder attribute on `<img>` (INV-63). (The tier FILES
   `-640/-960/-1280.jpg` ARE produced — 0 missing — only the HTML attribute is absent.)
3. **robots.txt** — engine missing the 21 AI-scraper `Disallow` blocks (tlvphoto `51f4f74`, cont.64).
4. **config.json** — engine emits EXTRA generalization keys tlvphoto's does not: `glide_ms`, `quiz.placement`,
   `sound_credit`, `sound_url`, `site_name`. CONTRACT DECISION (his, or a defensible default): either tlvphoto
   adopts these keys (invisible), or the engine SUPPRESSES empty/instance-default keys from the emitted config.
5. **`gallery/audio/`** — absent from the engine bake: the ambient-sound files aren't in the content-contract.
6. **Also differ:** `_worker.js`, `exhibition.js`, `exhibition.css`, `exhibition_data.json`, `i18n_source.json`,
   `index.html`, `sitemap.xml` — from the same build.py + asset generalization drift (e.g. `window.EXQuiz` vs
   tlvphoto's `window.TLVQuiz`, slug-vs-numeric `ID_RE`, quiz-model wording). The swipe fix (tlvphoto `b7f6042`,
   live on prod 2026-07-09) is ALSO fresh asset drift the engine does not yet have — fold it in the asset re-sync.

**PLAN (drive to empty diff, then his eye — prod flip is his OK only):** reconcile bucket-by-bucket, re-run the
byte-proof after each. Buckets 2+3 are clean mechanical ports FROM tlvphoto's `build_site.py` INTO the engine's
`build.py` (a Sonnet worker on a pinned brief; senior VERIFIES the byte-proof — never trust a worker's "empty
diff", check every file per the restructure-safety rule). Bucket 1 (image bytes) + bucket 4 (config contract)
are senior judgment. Bucket 5 = extend the content-contract to carry audio. Only when `diff -rq` is EMPTY do we
show Alexander the compare; prod is untouched until then.

## LIVE STATE (2026-07-07 night — FOUNDED as a lane beside tlvphoto)

- Repo renamed `~/gallery-engine` → `~/exhibition-engine` (his name). Born 2026-07-06 morning as a
  byte-identical extraction (`1e65222`); tlvphoto then landed A DAY of changes — the drift list
  lives at `~/tlvphoto/docs/engine-drift-2026-07-07.md` (worker-made, senior-verified).
- Tonight's re-sync: the walk's client assets (exhibition.js/css, worker.js, the headless harness)
  copied VERBATIM from tlvphoto (worker run, md5-verified — see CHECKPOINT.md). NOT yet re-proven
  as a byte-identical bake — build.py generalization is the real work (below).
- **The two-lane law (his word):** tlvphoto keeps living on its own scripts; the engine grows
  BESIDE it; the transition happens once, deliberately — see TRANSITION.md. Nothing in tlvphoto
  points at the engine yet.

## THE PRODUCT (his vision, captured 2026-07-07 — the spec grows from THIS)

Not a code dump — **a guided journey**: a photographer with an archive is TAKEN BY THE HAND
end-to-end, each stage EXPLAINED before it runs:
1. install the local model runtime (Ollama) — why, what it costs, what it enables;
2. ingest the archive (export → catalog → dedup) — the user understands what the engine learned;
3. **define the axes** — the feature vocabulary of THEIR photography (the engine proposes,
   measures, shows; the human names and curates — the tlvphoto axis journey, productized);
4. pick finalists, curate the door pool;
5. bake the exhibition (door → hang → walk, all of tonight's tlvphoto behaviors) and deploy.
The design-spec workflow (norm cards, prototypes) rides the method. Every step: plain words,
a checkpoint, resumable. The engine ships with the live-spec method as its working skeleton.

## FORWARD QUEUE (each row = one story via the pipeline; E-rows)

E1. **Adopt the method IN this repo** — live-spec adoption pass: SPEC.md seed (the journey above
    as scenarios), ARCHITECTURE skeleton, TEST_MATRIX seed, its own `.live-spec/` profile. The
    founding kind question rides here (recommendation: a guided generator — CLI + skill hybrid).
E2. ✅ **DONE 2026-07-07 ~01:50 — build.py absorbed tlvphoto's day WHOLE**: the generic bake now
    carries clean addresses, consent, the any-locale worker, visitor memory, the living hand's
    pool tones, series rooms, the quiet copyright — **proven BYTE-IDENTICAL against tlvphoto's
    own live bake (259 files, empty diff; the proof command in CHECKPOINT)**. Identity via
    site.json (example updated to TLV PHOTOS); favicons via --instance-assets. Was: — generalize what the instance hardcoded tonight
    (copyright line, clean addresses, i18n source/worker emission, consent snippet, config flags)
    behind the五 instance strings contract; re-prove the bake BYTE-IDENTICAL against tlvphoto's
    own (the drift report's re-sync list is the checklist).
E3. ✅ **DONE 2026-07-07 ~10:58 — the engine is green ALONE: 17/17 suites on a synthetic
    archive** (24 synthetic works, one series, zero private content; worker slices 1+2,
    senior-verified — assertions never weakened, instance-specific values parameterized from
    the fixture manifest; report `tests/E3_REPORT.md`). Byte-proof RE-TAKEN same hour against
    the instance's own bake after the day's changes: 256 files, empty diff. **⇒ BOTH bars of
    the SHRUNK transition gate (his 2026-07-07 pick) are green — E8 cutover opens on his word.**
    Standing law: re-run the byte-proof after every engine change (command in CHECKPOINT §5)
    and re-sync walk assets verbatim from the instance same session. Known engine gaps, honest:
    no vector-COMPUTATION stage yet (fixture ships ready vectors; the compute stage is
    instance-side — that's E5's axis journey), and the new-user path E4–E6 is still vision.
E4. **The guided journey, stage 1–2** (runtime + ingest): the explain-then-run walkthrough
    (CLI prompts or a local page), Ollama install check, archive contract.
E5. **The guided journey, stage 3** (axes): productize the axis definition/measure/curate loop —
    the heart; needs its own spec movement + prototypes.
E6. **Design-spec workflow** — how a user's norm cards/prototypes enter their instance.
E7. **Publish gate + GitHub public** (the publish skill walk; his word before anything goes out).
E8. **TRANSITION** — tlvphoto adopts the engine (see TRANSITION.md; his word opens it).

## Resume cold
Read this file + CHECKPOINT.md + ~/tlvphoto/docs/engine-drift-2026-07-07.md. The engine bakes
with `engine/build.py --content <dir>`; tlvphoto content = `~/tlvphoto`. Suite: none yet (E3).
Method: load the live-spec pack (`~/.claude/skills/live-spec-base` + working skills) per session.
