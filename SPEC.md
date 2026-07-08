# exhibition-engine — SPEC

## How to read
exhibition-engine turns a photographer's archive into a personal, ever-changing exhibition
assembled per visitor and deployed as flat files on an edge CDN with no server. This spec
states the **current truth** of what the engine is and what each part may claim. **The prose is
the meaning; the short codes at line-ends** (`EX-DOOR`, `INV-4`, `⟨DELTA⟩`) are quiet handles
for the prover and the test matrix — skim past them. **Edit history lives in `JOURNAL.md`,
not here.** Build order and future moves live in `NEXT_STEPS.md`; this document is what must
be TRUE. `⟨DELTA⟩` marks a place where the engine's current code diverges from the behavior
the clause describes — each one is listed in the Formal index for easy reconciliation.

## Layer map (how it stacks)
1. **The content contract** — what an instance must supply: the gallery data, the per-work
   feature vectors, the images, the site identity (`site.json`), and optional enrichment files.
   *Specified here in full.*
2. **The crawlable work page and the static bake** — a flat `/w/<slug>-<idtail>` page per work
   and the one local command that assembles the whole deployable site from the content directory.
   *Specified below (scenarios "Sharing a work" and "Baking the site").*
3. **The adaptive exhibition** — the single touchpoint at `/` where the personal, ever-changing
   walk lives, assembled per visitor from the kinship vectors. Door, gallery, sharing, the
   ambient narrator, the optional voice — all one surface, two faces.
   *Specified below (scenario "Arriving — the adaptive exhibition").*

---

## Purpose
Give any photographer's archive an exhibition that assembles itself. An instance supplies its
works, feature vectors, and identity; the engine bakes a fully static, edge-deployable site
where every visitor meets a threshold — a handful of works asking which feels closer — and the
gallery folds open from their pick, the works ordered by kinship into a considered arc. The
engine is generic: it knows no instance's name, brand, creator, or private content. Every
identity fact is a config value; every private note stays off the public bundle.

## Entities

**Work** — one finalist image. Attributes read from `gallery_data.json` items: `id` (unique
string), `img` (gallery-relative image path), native size (`w`, `h`), dominant colour (`dom` —
RGB triple, drives the breathing ground and door halos), `title` (the creator's own title, may
be empty), `section` (a grouping label), geo (`city`, `country`, both optional). The `sold`
flag (optional boolean — a quiet red dot in the caption zone when true) is present in
`exhibition.js` but currently not forwarded by the bake `⟨DELTA-5⟩`. `W`

**Feature Vector** — the ordered set of numeric axis values for one Work, from `vector.json`.
Each axis is a named key under `axes`; numeric values (int or float) enter the kinship math;
null or absent values are treated as 0 (neutral — "no radial structure" is a valid position).
The bake min-max normalizes each axis to [0,1] across the collection so no axis dominates by
scale; axis names NEVER appear in the bundle or the client — the visitor sees coordinate arrays,
never labels (`INV-1`). `FV`

**Instance** — one deployment of the engine: a content directory plus a `site.json` identity
file. The instance supplies everything the engine does not: works, vectors, images, door pool,
greeting strings, story notes. The engine supplies the client (JS, CSS, worker) and the bake
logic. An instance is self-contained: the engine's generic client renders it with no code
change. `I`

**Site Bundle** — the single self-contained static directory the bake emits, ready for an edge
CDN with no server. Every file in it is static (`INV-7`). `SB`

## The content contract

What the engine reads from the content directory (passed as `--content <dir>`):

- **`gallery/gallery_data.json`** — required. Object with `items`: the array of Works.
- **`vector.json`** — required. Object with `items`: per-work axis records
  `{id, axes: {name: value | {value: …}}}`.
- **`content_tags.json`** — required. Array of `{id, subject}`: the plain-language caption per
  work (what the work shows — for crawlers and alt text; never visibly rendered when
  `caption_visible` is false).
- **`gallery/assets/`** — required. The web-derivative images (paths relative to `gallery/`).
- **`gallery/shared/`** — required. The design-token CSS (`tokens.css`) the exhibition renders in.
- **`gallery/door_candidates.json`** — optional. Array of `{id, luma, warmth}`: the curated door
  pool, ordered (the order IS the curation voice; the pool's own order breaks every tie in the
  living hand). `luma` and `warmth` are [0,1] floats for the living hand's hour-lean
  (`EX-DOOR-3`); they never render. When absent, or thinner than `door_size` after filtering for
  living works, the door is skipped and the visitor lands on the diverse hang directly (`INV-14`).
- **`data/greetings.json`** — optional. The baked greeting-string cache (see `EX-GREET-BAKE`).
  Shape: `{fallback, aliases, langs: {code: {ask, exit, more, q_more, q_spent, share_label,
  share_copied, series, room_back, enjoy, dir, greet: {night, morning, day, evening}}}}`.
  Absent or malformed → the client stands on its built-in Russian lines; the door still opens.
- **`finalist_series.json`** — optional. Object with `series`: array of
  `{members: ["<prefix>_<id>.<ext>", …]}`. Series with 3 or more living members get a side
  room (`EX-SERIES`); shorter ones are silently dropped.
- **`data/time_of_day.json`** — optional. Object with `marks`: `{id: {marks: [daypart…]}}` where
  daypart is one of `day | zenith | sunset | night | free`. Absent or a missing entry → the
  work reads as `free` (the light-lean is a no-op; the arc unchanged — the byte-identical guard).
  Data, never rendered (`INV-1`). `EX-STORY-ORDER`
- **`story_notes.json`** — optional, INSTANCE-PRIVATE. Flat `{id: note}` map of per-work authored
  lines. NEVER shipped as a public static byte — the bake embeds them inside `_worker.js` (the
  one bundle file a Cloudflare Pages deployment does not serve as an asset) only when `ai_story`
  is enabled. Off means every story line is grounded in the public fields only. `EX-STORY-EDGE`

**Site identity** comes from `site.json` (passed as `--site <path>`): `site_name`, `creator`,
`root_title`, `root_description`, `collection_name`. These drive every baked HTML string. The
`site_url` comes from `--site-url`. `⟨DELTA-1⟩` **The door wordmark** is currently hardcoded
as a literal string in `exhibition.js` rather than injected from `site_name` at bake time — it
is the engine's only remaining instance-facing brand value that the bake does not parameterize.

---

## Invariants

**Safety — what must never happen**
- **No axis readout ever faces a visitor.** No axis name, score, coordinate, or confidence is
  ever rendered in any visitor-facing surface. Axis values travel as neutral coordinate arrays
  under the key `v`; no label follows them into the bundle. The exhibition behaves, it never
  explains. `INV-1`
- **The static face is complete without JavaScript.** `/` with JS disabled serves a real
  heading, indexable intro about the collection, a static grid of work thumbnails each linking
  to its `/w/` page, plus JSON-LD, OpenGraph tags, and the copyright — full, meaningful content
  for a crawler or a locked-down browser. `INV-2`
- **Crawlable title is never empty.** Every work page ships a non-empty `<title>`, `og:title`,
  JSON-LD name, and `<h1>` heading via the fallback chain: **creator's title → caption →
  section+place → "Photograph — {site_name}"**. `INV-3`
- **One page per work, no orphan, no phantom.** Every work in `gallery_data.json` has exactly
  one crawlable page; the bake emits no work page for an id absent from that set, and skips no
  id present in it. `INV-4`
- **Canonical and listed once.** Every page declares its own canonical URL; `sitemap.xml` lists
  the exhibition root plus every work page, nothing else; `robots.txt` permits crawling on
  production and disallows on a preview host. `INV-5`
- **Every work is discoverable as an image.** `sitemap.xml` carries each work page's photograph
  as an `<image:image>` entry so a search engine can index all works. `INV-6`
- **The bundle is self-contained and static.** No file in the deployable bundle needs a running
  server to render. AI endpoints are an optional later layer behind the reserved `/api/*`
  namespace, never a prerequisite for the site to work. `INV-7`
- **AI ships off.** `config.json` ships with every AI feature flag false. Every visitor surface
  renders fully with AI off; a failed or absent AI response falls back to the static content. `INV-8`
- **Content is data, not baked prose.** Every piece of visitor text is read from the precomputed
  JSON at bake time; the bake never hand-authors per-work prose into the HTML, so a future
  `/api/*` endpoint reads the SAME data with no migration. `INV-9`
- **The bake is reproducible.** The same content inputs produce the same bundle bytes — no
  wall-clock timestamps in output content, no randomness baked in. Same inputs → same bytes. `INV-10`

**Safety — the live walk**
- **One arc is bounded.** One arc never shows more than `spread_size + max_unfolds × unfold_step`
  works (20 on today's defaults). The whole catalogue is never reachable by pressing "more." `INV-11`
- **Old walk state → clean start.** A state written by a different axis-set version is discarded
  and the visitor starts clean (the cold door). A stored arc referencing a work id no longer in
  the gallery drops the missing ids; an arc emptied this way also starts clean. `INV-12`
- **Place memory is per-tab.** Two windows sharing a domain never stomp each other's scroll
  position; the place marker lives in `sessionStorage`. `INV-13`
- **The door never blocks entry.** A missing, malformed, or thin door pool silently degrades to
  the diverse hang within the same bounded arrival moment — never a blank threshold. `INV-14`
- **The walk ends.** After `max_unfolds` «ещё N» steps the control retires quietly for the
  current arc; the way deeper is a fresh pick at the door. `INV-15`
- **No one-way doors.** Any face the visitor can enter, they can leave and re-enter. The
  door↔gallery loop is a law: exiting the gallery returns to the door; a pick starts a fresh
  arc; back from a re-opened door returns to the walk untouched. `INV-16`
- **No dead void.** Every control the visitor needs — the door works, the closing screen's
  buttons — lives in the first viewport or visibly past the fold. `INV-17`
- **Back is honest.** Steps are laid per face (door | walk | side-room), never per frame. A
  door step carries the spread it showed; back from the gallery returns to the door AS IT STOOD;
  back from a re-opened door returns to the walk untouched at the same place. `INV-18`
- **The face the tab stood on survives a reload.** A door face stays the door on reload (gently
  refreshed: ≥60% of the hand held, ≤40% swapped in); the walk stays the walk and restores
  its place. `INV-19`
- **The living hand repeats at most ⌊door_size/3⌋ works from the previous hand.** A returning
  visitor never meets the same threshold twice. When the pool is exactly `door_size`, the law
  stands down gracefully. `INV-20`
- **The door locks the page behind it.** While the door face stands, the walk beneath it does
  not scroll and is not reachable. `INV-21`
- **One tempo rules every motion.** Every CSS duration and JS wait on the walk's surfaces
  multiplies by `--tempo`. No hardcoded duration may bypass the clock. `INV-22`
- **Reduced motion: the tempo collapses to 0.05.** Under `prefers-reduced-motion: reduce` every
  move lands near-instant; reduced-motion always wins over a visitor's tempo override. `INV-23`
- **Every appearing element arrives by the house breath, never pops.** Any UI element whose
  first visible entry could appear sudden carries an opacity-from-zero fade riding the tempo. `INV-24`
- **The coat-check token is anonymous.** The token is a random string (no name, no email, no
  identifying data); what the edge stores per token is seen-work ids only. Forgetting is whole:
  `?reset` wipes the token. `INV-25`
- **The model routes are never a money tap.** Three fences precede every Anthropic call: a bot
  check (no UA or a known crawler → English from the baked source, no model call, not cached
  under the asked locale); a per-IP hourly rate limit; a hard daily cap across all model routes. `INV-26`
- **Sound is off on a fresh visit.** No audio fetches on cold load. The loop fetches only on
  the visitor's first deliberate turn-on. `INV-27`
- **The archive signs its rooms.** Every public face carries exactly one quiet copyright line —
  composed at bake time from `creator` and `site_name`; the year is the bake run's own; a
  January rebake re-years it automatically. `INV-28`
- **The share toast is never a silent failure.** When the browser refuses the clipboard, the
  toast carries the link itself, stays until dismissed, and must be hand-copyable. `INV-29`
- **The JS-off static face is fully formed before JS wakes.** An inline script marks
  `<html class="js">` before `<body>` parses, hiding the crawler's static index pre-paint; if
  the walk hasn't come alive within 2.5 seconds, the mark is removed and the full static face
  returns — a bounded worst case, never a blank page. `INV-30`

---

## Arriving — the adaptive exhibition

A visitor (or a crawler) hits the instance's root URL — the strongest URL on the site. There is
**one touchpoint**: `/` IS the exhibition. No cover page, no separate door page, no "enter"
click. The exhibition is this surface, assembled from the visitor's own signals. `EX`

**One surface, two faces — progressive enhancement.** With **JavaScript off** `/` renders a
**static, crawlable layer**: a heading (`site_name`), an indexable description
(`root_description`), a static grid of work thumbnails each linking to its `/w/` page, a
copyright line, and the full JSON-LD (`WebSite` / `CollectionPage`) and OpenGraph metadata —
complete and meaningful with no JS (`INV-2`). With **JavaScript on** the same URL comes alive:
the static index is hidden before first paint by the inline script (`INV-30`); if the walk
does not arrive within 2.5 seconds (broken or missing JS, failed data fetch), the static face
returns. The crawlable static index links every work so a crawler discovers them all —
regardless of whether the walk ever wakes. `INV-30`

### The door

**On a cold arrival** (no stored walk, or the visitor's first visit) the live face opens with
the **door**: `door_size` of the instance's works in one calm line asking the configured question
(the `ask` string from the greeting cache, e.g. «что ближе сейчас»). The pick IS the entry — a
tap on any door work begins the gallery. There is no "skip" or "enter silently" affordance: the
pick is the only way in (`EX-DOOR-2a`). A missing or thin pool silently lands the visitor on
the diverse hang directly (`INV-14`). `EX-DOOR`

**One line, always** (`EX-DOOR-2b`): the windows hang in a single line — a **row** when
`W/H > 1.02`, a **column** when portrait — and never wrap to a second line. Windows **shrink
first, count drops second**: row — up to `door_size` windows while each gets ≥118px, else 4,
else 3, floor 76px; column — up to 3 windows capped within 52% of height, dropping to 2 below
104px. Gaps breathe with the viewport (row 3vw clamped [16,44]px; column 2.5vh clamped
[14,30]px). A resize recomputes live; a re-render happens only when count or orientation changes.

**The windows are fully visible at once** (`EX-DOOR-2c`): no dimming at rest. The pointer is
answered by a **halo alone** — no brighten, no lift (hover-only on pointer devices,
`focus-visible` on keyboard). The halo's colour is the work's `liveAccent` tone, not the raw
dominant (a near-black dominant is invisible on the dark ground). There is no pick-highlight;
the pick answers with the ceremony.

**The pool is curated and the hand lives** (`EX-DOOR-2d`, `EX-DOOR-3`): the pool's ORDER is
the curation — the file's order is the tie-break voice. Each **cold arrival deals a fresh hand**
of `door_size` works from the pool, chosen by three quiet voices: **novelty** (works the guest
has not met, from the coat-check seen-list when available or the local walk's own seen, come
first); **the hour** (the hand leans toward the daypart's tone using the candidates' own baked
`luma`/`warmth` numbers — darker for night, warmer for evening, brighter for morning and day;
a configuration knob, never a new fetch); **curation** (the pool's own order breaks every tie).
**His law:** a new hand repeats at most ⌊`door_size`/3⌋ works from the previous hand (stored in
`tlv.hand`) — a returning visitor never meets the same threshold twice (`INV-20`). The re-opened
door (after the exit) shows the **standing hand** (the session's set is fresh-quiz-only in the
re-open sense: the pick is fresh, not the set mid-session; see `INV-16`). `EX-DOOR-3` `INV-20`

**The crossing — ceremony B «через чёрное»** (`EX-DOOR-2e`): a tap answers by the whole room
dimming — the veil takes the door (`.33s×tempo`) → the wordmark alone drifts to the center of
the black and lets go (~`.9s`) → the room's tone rises first (`.53s` onto the picked work's
darkened ground, ~`1.2s` mark) → the first work reveals separately (~`1.78s`, the reveal fade
keeps its full `1.5s×tempo`) → the caption last (`+.15s`). Every beat ×tempo (`INV-22`). ONE
history step is laid when the walk arrives. Any navigation mid-ceremony cancels it cleanly — the
arriving face wins, no stranded veil.

**The idle hint** (`EX-DOOR-2g`): a cold door left untouched for ~3s×tempo breathes the FIRST
window's halo ONCE — rising and resting in one cycle — and repeats gently every ~7s×tempo until
any interaction. Touch devices hint too — they have no hover to discover by. The re-opened door
never hints (the visitor already knows the game). Under reduced motion the hint is suppressed.

**The door locks the page** (`INV-21`): while the door face stands (cold arrival or re-opened),
the walk beneath it does not scroll and is not reachable until the visitor picks.

### The greeting

**On a cold arrival the threshold speaks first — one quiet line** in the visitor's own language,
tuned to their time of day by the device clock (no geolocation, no IP lookup, no server). The
greeting hangs above the ask line by default (configurable: `"ask"` | `"top"` | `"off"` via
`exhibition.greeting`). The whole door face follows the visitor's language: the ask renders
from the same strings block; RTL locales turn the face right-to-left with the correct `dir`
attribute and `lang`. The re-opened door keeps the localized ask but does not greet again — a
museum greets on arrival, not on every pass through the lobby. An unknown or uncovered language
falls back to the cache's configured `fallback` code (default `en`). `EX-GREET`

**The greeting tracks the live hour** (`EX-GREET-LIVE`): a door left open across a daypart
boundary re-greets itself on `visibilitychange`/`focus` and on a once-a-minute backstop. Only a
genuine daypart crossing (night→morning→day→evening) triggers a fresh line; same daypart → the
chosen line is left alone, no flicker.

**The greeting strings are baked, not live** (`EX-GREET-BAKE`): the strings live in the
committed `data/greetings.json` cache, authored at authoring time by the instance's own gen
script (e.g. `scripts/gen_greetings.py`) calling a small model; the bake only READS the cache
(`INV-10`). The bundle ships no API key and no runtime language call for the baked languages.
Languages × dayparts (night 0–6, morning 6–12, day 12–18, evening 18–24) × a few variants per
cell (default 3; the shown variant is date-seeded so two A/B windows on the same day see the
same line). Absent or malformed → no greet block, the door stands on RU built-in strings and
never blocks entry. The `skip` key must NOT appear in any language block (it is retired —
`EX-DOOR-2a`).

**The door-reload** (`INV-19` / `EX-DOOR-RELOAD`): reloading while the door stands (specifically,
when the stored history state marks the door was reached by EXITING a walk — the `returned`
flag) holds the door face rather than dropping into the walk behind it. The hand refreshes
gently: ≥60% of the standing set is kept, ≤40% swapped in — the threshold feels alive on reload
yet cannot be reloaded into a tour of the whole pool. Repeated reloads hold the door.

### The language selector

The door face carries a quiet corner mark showing the current language's short code. A tap opens
a list of baked languages plus the browser's own locale when it falls outside the baked set (when
`ai_i18n` is on). A pick re-speaks the threshold at once — the ask and greeting update
immediately — persists across visits (`tlv.lang`), and outranks the browser setting everywhere a
language is read. RTL locales turn the door face right-to-left. `?reset` forgets the choice and
the browser's own tongue returns. `EX-LANG`

### The gallery

**Behind the door the visitor is INSIDE the gallery** — the Room's museum hang. The hang's law:
**one work per viewport, the image untouched, all text in the dark margin.** The visitor scrolls
through `spread_size` works (default 10, config range 3–12) seeded by their door pick: the
picked work hangs first, the rest ordered by kinship distance (arc shape configurable:
`"widening"` holds contrast by widening the sampling step; `"nearest"` draws neighbours in
tightly). Each frame composes the Room's language: the **caption zone** in the bottom-left
margin — the work's own title (or a quiet *untitled*), the section · place, an optional sold dot,
an optional told-story line, and an optional series pill; the **counter** (`01 / 10`) top-left;
the share button in the frame's margin; the **ground breathing** the current work's dominant
tone. `EX-HANG`

**The breathing ground and the live accent** (`EX-ACCENT`): the focused work's dominant colour
(`dom`) is raised to a readable luminance (target Y≈170, mixed 80/20 with the raised dominant
and bone brass `#b3a284`; a near-black dominant falls back to bone whole) and set as `--accent`
and `--accent-2` on `:root`; the ground (`--ground`) is a darkened mix of the dominant and the
neutral dark base. At rest — the door face, the work pages — the accent is bone brass `#b3a284`.
In the hang the accent is **alive**, changing work to work; the closing screen wears the tone of
the last work the visitor saw. The `--tone` variable (the accent at ×0.66) tints the
told-story line on the wall label. The accent is presentation, never a readout (`INV-1`: no
number faces the visitor, the tone just IS).

**The amortized scroll** (`EX-GLIDE`): while the hand moves, the room moves exactly with it —
nothing yanks. A beat of **TRUE stillness** (~280ms of unchanged scroll position, sampled per
animation frame, never inferred from event timing: momentum on iOS and Mac trackpads delivers
scroll events in bursts with long gaps, which makes a timer fight the still-moving native scroll)
triggers the glide to the nearest frame: **sine in-out** (the calmest classic curve — lowest
peak speed, both ends soft, no bounce), over `950ms + 0.75ms/px` of distance, capped at 2400ms,
scaled by `tempo/1.35` capped ×1.25 — the docking itself stays visibly slow. A **back-correction**
(settling against the hand's last direction) takes a third longer — the room never tugs back
briskly. On **touch**: a flick that entered the next frame by more than ~12% settles forward in
the direction of travel; only a barely-begun drift settles back. Pointer devices use plain-nearest.
Any new input (wheel, touch, a key) cancels the glide mid-flight — the museum never wrestles.
A sub-2px correction is skipped. **Paging keys** (`Space`, `↓`, `↑`, `PageDown`, `PageUp`, and
`Shift+Space`) glide by frame on keyboard — the same soft breath, one step per press, chaining
from the running glide's heading.

**Back is honest** (`INV-18`): `(a)` crossing the door lays ONE history step — back from the
gallery returns to the **door AS IT STOOD** (the step carries the spread it showed); `(b)` the
exit control (always «выход», localized) re-opens the door and lays a step — back from that door
returns to the **walk untouched at the same place**; `(c)` the walk owns a **per-tab place
memory** (`sessionStorage`) — any return to the walk (back, the work page's plain link, a reload)
lands on the **exact frame the visitor left**; `(d)` a superseded arc never resurrects — back
passes through old walk steps but renders the **current walk**; `(e)` steps are laid **per face,
never per frame** — scroll is the walk, not history.

**The arc unfolds, it doesn't reset, and it ends.** The closing screen (a full-viewport rest
after the last frame) carries «ещё {n}» while the budget lasts and the exit always (`INV-17`).
Each «ещё» appends `unfold_step` works (default 5) along the current arc without re-shuffling
what the visitor has already seen. After `max_unfolds` steps (default 2) the control retires
quietly; the closing screen shows «дальше — новый выбор» (localized). The unfold budget is
**derived** from the stored `shown` count — never trusted from storage — so a tampered value
can never grant unlimited "more" (`INV-11`). The closing screen's copy — the exit word, the
more-line, both questions — speaks the visitor's language from the same greeting strings cache;
built-in Russian stands under a missing cache. `INV-15` `INV-29`

### Sharing from the walk

On every frame of the hang a quiet **share button** waits (a link glyph, ~36px, hover-revealed
on pointer devices, always visible on touch, ≥44px touch target). A click **copies, never
navigates**: the frame's **room permalink** — the canonical root plus
`?utm_source=share&utm_medium=referral` plus `#w-<id>`, clean of whatever params the sharer's
own address carries — onto the clipboard and answers with a quiet **toast** in the visitor's
language (the `share_copied` string from the greeting cache; built-in Russian fallback). The UTM
attribution separates shared arrivals from direct/bot noise in the walk's own analytics. If the
clipboard is refused, the toast carries the link itself and stays until dismissed (`INV-29`). The
share button replaces the retired ↗ corner link; the walk no longer links out per frame. `EX-SHARE-BTN`

**The permalink arrival** (`EX-SHARE-IN`): opening the exhibition root with `#w-<id>` treats the
hash as a handed-over pick. `(a)` If the work is among the frames already shown — an instant
jump, the arc unchanged, «выставка не рвётся». `(b)` Otherwise — the shared work acts as a pick:
fresh-top arc, the door passed, no greeting; the door stays one exit away. `(c)` Unknown or
malformed id changes nothing. The hash is **consumed once per hand-over** (per-tab, stored in
`sessionStorage`); the room's own place memory wins once the hash is spent; a reload before
walking repeats the same honest arrival. No history step of its own. `EX-SHARE-IN` `EX-SHARE`

### The told story

When `ai_story` is on, a quiet voice walks beside the guest — one short associative line under
each work in the wall label's told-slot, the lines leaning into a small arc. The voice never
describes the photograph and never explains the machine (`INV-1`). The walk without the voice is
still the whole walk — the story is a layer over the hang, not a gate. `EX-STORY`

**The order is leaned by light** (`EX-STORY-ORDER`): beside kinship (the arc's own metric) the
story adds one soft term — the hour-discontinuity over the authored time-of-day mark SETS
(`data/time_of_day.json`) — weighted by `story.light_weight` (0 = pure kinship, high = a strict
light march). Computed **deterministically in code**: the model writes lines, never the sequence,
so the same pick yields the same order and a stable cache key. The four daypart labels —
`day`, `zenith`, `sunset`, `night` — form a light axis (0–2); a `free` work is a zero-cost
wildcard dropped wherever the arc needs a breath or the turn. With the voice off the arc stands
exactly as it does today (the byte-identical guard).

**Each line** (`EX-STORY-LINE`): at most a dozen words; slightly abstract and associative, never
a plain description of the photograph; grows from the instance's own authored note when one
exists (adapts his words, never quotes them raw) and stamps `source: note`; with no note writes
from the title, place, subject, and light marks only. Never invents a name, person, event,
weather, or history the fragments do not hold. Never names technique (no camera, lens, exposure,
editing, filter, or cut). Arrives by the house breath on `--tone`-tinted text. When the walk
unfolds «ещё N» the voice extends over the grown set (its own cache key).

**The voice lives at the edge** (`EX-STORY-EDGE`): the walk sends the ordered ids + variant +
language to `/api/story`; the worker reads the PRIVATE story fragments (title/place/subject/light
are public grounding; the `story_notes.json` note is the instance's own words, adapted never
quoted) and calls a small model (Haiku); the answer is kept in KV forever under a key of the
**ordered id sequence + variant + language + params_version** (bumped whenever
`story.light_weight`, the prompt, or the marks change — so a knob flip never serves a stale
order). One model call per distinct walk, $0 after. A failed or absent voice is SILENCE — the
walk carries no lines and loses nothing (CS-8, `INV-8`).

**No story ships variant-blind** (`EX-STORY-AB`): every story carries its `story_variant` in the
generated JSON and as a dimension on the walk's existing GA beats (`walk_unfold` / `walk_exit`)
— no sixth beat added. The mode is chosen by `story.variant` in config; variant B (the cheap
light/hour plot) ships first.

### The ambient player

When `sound_url` in config is non-empty, a quiet control appears in the top-right corner —
separate from the share button at the frame's bottom. It offers ONE ambient loop. **OFF by
default** (`INV-27`): a cold arrival is silent and the audio fetches ONLY on the visitor's first
deliberate turn-on. A tap starts it: decoded via Web Audio into a gapless looping
`AudioBufferSourceNode` under a **fade-in (~1.2s×tempo)** on a gain ramp; a second tap
**fades out (~0.8s×tempo)**; leaving to a `/w/` page or unload fades to zero best-effort
(`pagehide`). Volume defaults to 0.3 with a touch-friendly slider (≥44px). The choice persists
in `tlv.sound`. A return visit with preference ON **arms** on the first gesture (the browser
blocks autoplay without one) rather than fetching on cold load. On hover / while playing a thin
credit tray shows the instance's configured `sound_credit.artist`, `sound_credit.title`, and
`sound_credit.url` — no hardcoded artist name or link. A missing or failed file **fails SILENT**
(`INV-1`). Two beats ride the existing GA wire: `sound_on`, `sound_off`. The player plays
continuously across the whole single-page walk — door, crossing, side room, scroll — never torn
down on a face change. `EX-SOUND` `INV-48`

**Pause holds the moment** (`EX-SOUND-PAUSE`): off is a **pause** that records the loop's offset
(clocked from the source's start time); on **resumes from it**, never from the beginning. In-memory
within a session — a fresh page load starts the loop from the top. `INV-52`

### The gracious deterrent

When a visitor tries to **grab a hung work** (right-click / `contextmenu`, drag / `dragstart`, or
pinch-zoom / `gesturestart`) the engine intercepts. For a grab: `preventDefault` and show a
**quiet, localized gift line** on the existing share toast — the instance's `enjoy` string from
the greeting cache plus the site host appended in code (e.g. «enjoy · example.com»), arriving on
the house breath and leaving by itself. For a pinch-zoom: `preventDefault` silently — a pinch is
exploratory, not a save, so no toast. A **soft CSS layer** rests on every `img.work`:
`user-select:none`, `-webkit-user-drag:none` (no drag ghost), `-webkit-touch-callout:none`
(kills the iOS long-press save sheet). This is a gift and a gentle nudge, never hard DRM —
devtools, view-source, and screenshots still work, said plainly. `EX-PROTECT` `INV-49`

### The loading breath

Wherever a frame in view holds a work whose pixels have not arrived, the frame — after a short
grace beat (~350ms×tempo, so a healthy network never sees it flash) — breathes a **thin hairline**
in the current accent tone, centered where the work will hang, breathing at tempo: solemn,
minimal, wordless. The work reveals the moment pixels land — the room's own quiet fade. A failed
image retires the breath; the caption and counter still hold the frame; no error face. `EX-LOAD`

### The series side room

Where a hung work belongs to a series of 3 or more living members, its caption zone grows a
quiet **series pill** («серия · N», localized — the `series` string from the greeting cache, never
the machine's theme label). A tap opens the side room **through the same black crossing** the
door uses — a shortened breath of the entry ceremony; the cancel law carries it (any arriving
face wins, no stranded veil). The room's variant matches the series' own character: a **large
series** (8+) lays prints on a polaroid scatter (a tap lifts one to the light); a **small one**
shows a lane (scrolled sideways). Three honest ways to close: the back chip, Esc, and the
browser's Back — all landing the guest on the **exact frame they left** (the walk holds its
place beneath, locked). The side room lays ONE history step; the page locks beneath it (`INV-21`).
The `series_open` analytics beat rides the GA wire on open. `EX-SERIES` `INV-46`

### The any-language layer

When `ai_i18n` is on, a visitor whose browser speaks a locale outside the baked set gets the walk
in the baked fallback **instantly**, and quietly after first paint the site asks its own worker
(`/api/i18n?lang=…&v=…`) for that locale's full string set — the door ask, the greeting dayparts,
the closing copy, the share pair, the enjoy line, and every work title. The worker generates the
set **once** via a small model (Haiku, museum tone, strict shape — a malformed answer is never
served), keeps it forever in KV under `lang+version` (titles change → version bumps →
regeneration; never pre-generate all languages), and answers everyone after from the cache at
$0. The browser keeps its own copy too (`localStorage` keyed by language+version) so a returning
visitor pays no fetch. When the strings land mid-visit, the standing surfaces re-speak **quietly**
(the door re-renders its ask and greeting; the closing screen updates) with no layout jump. A dead
worker changes nothing but the extra languages — the baked seven stand unaffected. `EX-I18N`

### The edge guard

Before any Anthropic call three fences are decided at the edge (`INV-26`): `(1)` a **bot** (no
`user-agent`, or a known crawler/tool agent) is served English straight from the baked source
with no model call — and that English is NOT cached under the asked locale, so a real speaker
still earns a real translation later; `(2)` a single **IP is rate-limited** to `RL_PER_HOUR`
model-triggering requests per hour (a self-expiring KV counter); `(3)` a hard **daily cap** on
model calls across all routes — past it, i18n degrades to the English source and the story route
to silence (`INV-8`; absence loses nothing). Never a CAPTCHA or a login wall; bots are welcome to
the static walk and the work pages. `EX-EDGE-GUARD` `INV-51`

### Visitor memory

When `visitor_memory` is on, a first visit **mints a random token** (`tlv.visitor` in
`localStorage` — a random string, never anything identifying) and, as the visitor walks, the
frames they actually met collect and report quietly to `/api/visitor` (debounced at ~3s,
fire-and-forget; a failed report is silently dropped). The edge keeps **ONE record per token** —
seen-work ids, merged across visits, capped at ~500 newest, expiring after ~180 days of silence —
and hands it back on boot so the door's novelty voice can prefer unseen works. The local
seen-list (`tlv.seenc`) mirrors the report for sessions without server memory. Forgetting is
whole: `?reset` wipes the token and the local list (`INV-25`). `EX-MEMORY` `INV-43`

### Analytics

The walk reports **five beats** (plus one additional) to the ONE sanctioned analytics wire — the
baked GA tag, if `ga_measurement_id` is configured. No tag baked → total silence; the walk never
errors. Events carry at most the plain beat name and the work's public id — never a vector
(`INV-1`). **Consent defaults declare first**: advertising storage/use DENIED; analytics
measurement GRANTED; no cookie banner (a quiet museum). When a told story walks beside the guest,
`story_variant` rides the existing beats as a dimension (no new beat added). `EX-PULSE` `INV-41`

| Beat | When |
|------|------|
| `door_pick` | a door work is tapped and the ceremony begins |
| `walk_unfold` | the visitor taps «ещё N» |
| `walk_exit` | the visitor taps the exit and returns to the door |
| `share_copy` | the share button is clicked |
| `share_arrive` | a visitor arrived by a room permalink |
| `series_open` | a series side room is opened (engine-native; absent from the tlvphoto spec reference `⟨DELTA-4⟩`) |

### The reset address

Opening the exhibition root with `?reset` in the address **wipes the browser's own trace** before
anything restores — named keys only: `tlv.exhibition`, `tlv-tempo` (in `localStorage`) and
`tlv.place`, the hash hand-over marker (in `sessionStorage`), then `tlv.visitor`, `tlv.hand`,
`tlv.seenc`, `tlv.lang`, `tlv.sound` (in `localStorage`). The param strips itself via
`replaceState` — no history step laid, Back stays honest. A storage refusal never blocks the
arrival. Idempotent: with nothing stored it does the same, silently. The worst a hostile
`?reset` link costs its clicker is their own walk position — nothing of anyone else's, nothing
server-side. `EX-RESET` `INV-35`

### Performance timings

Every live walk lays quiet performance marks at its beats — arrival, data landed, door shown,
pick, hang rendered, the breath, an image landing, reveal, caption, unfold, exit — named `tlv:*`
in the browser's own `performance` timeline. Nothing faces the visitor (`INV-1`); nothing leaves
the tab (`INV-7`). With **`?timings`** in the address the console narrates the beats as they land;
`TLVTimings()` returns the marks as data. `EX-TIMING` `INV-38`

### Motion, feel, and appearance

**One tempo, five duration tokens** (`EX-MOTION`): every CSS duration and JS wait on the walk's
surfaces multiplies by `--tempo` (config `exhibition.tempo`, default 1.35). Five named tokens:
soft `.6s` (captions, hovers, toasts) · reveal `2s` (a work entering) · rise `1.4s` (the door's
windows) · ground `1.7s` (the tone shift) · cross `1.2s` (the door ceremony). Entries are
**fade alone** — rise/lift transforms are not used. No hardcoded duration may bypass the clock
(`INV-22`).

**Reduced motion** (`EX-MOTION-R`): under `prefers-reduced-motion: reduce` the tempo collapses
to `0.05` — every move lands near-instant, nothing breaks. Reduced-motion always wins over a
visitor's `localStorage['tlv-tempo']` override. A visitor or a test may pin the tempo via
`localStorage['tlv-tempo']`, clamped to [0.05, 3] (`INV-23`).

**Every appearing element arrives by the house breath, never pops** (`EX-ARRIVE`): any UI element
whose first visible entry could appear sudden carries an opacity-from-zero fade riding `--d-soft`.
The idiom: keep the layout toggle (the absent element costs no layout), then
`requestAnimationFrame(() => el.classList.add('show'))` so the next-frame paint sees `opacity:1`
after the CSS transition fires. Dropdowns that also close by removing `.show` use
`setTimeout(hideAfterFade, d_soft_ms)` so opacity returns to 0 before the layout collapses
(`INV-24`).

**The feel is configuration, not hardcode** (`INV-31`): every feel knob lives in `config.json`
under `exhibition`. An unrecognized value renders the default, never a crash or a blank.

| Knob | Default | Range / options |
|------|---------|-----------------|
| `spread_size` | 10 | 3–12 |
| `cold_spread` | `"diverse"` | `"diverse"` (farthest-point) \| `"first"` |
| `arc_shape` | `"widening"` | `"widening"` \| `"nearest"` |
| `tempo` | 1.35 | the ONE motion multiplier |
| `kinship_axes` | `"all"` | `"all"` \| index array |
| `unfold_step` | 5 | works per «ещё N» |
| `max_unfolds` | 2 | 0–5 |
| `door_size` | 5 | 3–5 |
| `greeting` | `"ask"` | `"ask"` \| `"top"` \| `"off"` |
| `sound_url` | `""` | path to the .m4a file; empty = no player |
| `sound_credit.artist` | `""` | artist name for the credit tray |
| `sound_credit.title` | `""` | track title for the credit tray |
| `sound_credit.url` | `""` | artist website for the credit tray |
| `story.variant` | `"B"` | `"A"` \| `"B"` \| `"C"` |
| `story.light_weight` | 0.6 | 0 = pure kinship; high = strict light march |
| `story.params_version` | 1 | bump on prompt/weight/marks change |

**The archive signs its rooms** (`EX-COPY` / `INV-28`): every public face carries one quiet
signature line: «© {bake-year} {creator} · {site_name}» — composed once at bake time from
`site_config["creator"]` and `site_config["site_name"]`; the year is the bake run's own.
Faces: the walk's **closing screen**, every **work page**, and the **JS-off static index**.
The door carries no signature. The line stays in its own Latin across every locale; the i18n
layer does not translate it. `EX-COPY`

**Persistence** (`INV-12`): the walk remembers, client-side only, the visitor's arc and scroll
position. A return visit continues from where they were — the door does not re-ask on its own.
A stored arc whose version does not match the current axis set is discarded and the visitor meets
the door fresh. The unfold budget is DERIVED from the stored `shown` count, never trusted. No
visitor state leaves the browser unless `visitor_memory` is on (`EX-MEMORY`).

---

## Sharing a work — the crawlable page

Someone lands on `/w/<slug>-<idtail>` — from a search result, a shared link, a card unfurled in
a chat. They meet one work on its own page: the image (full width, its alt text the caption or
the indexable title), the **creator's title** as the heading (when the creator gave one), the
**dominant palette** as a row of colour swatches, the **place** if the archive knows it, a return
link to `/`, and the copyright. The page is stateless static HTML — no session state, no
`localStorage`, renders identically on every load. Script-free (`INV-2`). `WP`

**The heading:** the creator's title is visible when present; otherwise a non-empty
visually-hidden `<h1>` (section+place label, never the machine caption — `caption_visible:false`
keeps the caption off the visible page body) serves crawlers and assistive voice. The page stays
wordless visually when the creator left no title. Never empty (`INV-3`).

**The URL scheme: `/w/<slug>-<idtail>`** — a readable slug from the creator's title (or caption
when empty; "photograph" when both are empty) plus a 4-char stable id-tail (SHA-1 of the work
id). Canonical and permanent; the id-tail prevents slug collision and survives a title edit. Every
baked reference to a work — canonical, `og:url`, JSON-LD `url`, sitemap entry, the static index
links — is the **extensionless** clean form (the host serves clean→`.html`). `WP-CLEAN`

**Structured record:** JSON-LD `VisualArtwork` with `name` (the resolved title), `image`
(absolute URL), `url` (canonical), `creator` and `copyrightHolder` (from `site_config["creator"]`),
`description` (the caption, when present), `contentLocation` (the place, when known).
OpenGraph + Twitter `summary_large_image` cards with `og:image` as the **absolute** derivative
URL plus `og:image:width`/`height` (from the stored size) and `og:image:alt` (the caption or
title) — so a shared link unfurls with the photograph. `INV-32` `⟨DELTA-3⟩` No `dateCreated`
field: the generic Work entity has no date field in the content contract; an instance may enrich
this in a future extension.

**The caption** (the `subject` field from `content_tags.json`) feeds `<meta name=description>`,
the image `alt`, the JSON-LD description, and the share card; it is invisible on the page itself
when `caption_visible` is false (the default). The page is wordless for the eye; the text is
fully present for machines and assistive voices.

---

## Baking the site

An instance owner runs **one local command** and the whole deployable site is regenerated from
the content directory. This is the **bake**: `engine/build.py --content <dir> --site <site.json>
--out <dir> --site-url https://…`. Same inputs → same bundle (`INV-10`). `BK`

The **site bundle** emitted contains:
- `index.html` — the crawlable static face of the exhibition, progressively enhanced into the
  live walk by `exhibition.js`
- `/w/<slug>.html` files — every work page (one per work, no extras, no gaps — `INV-4`)
- `exhibition.js` + `exhibition.css` — the engine's client assets, copied verbatim from
  `engine/assets/`
- `exhibition_data.json` — the walk's baked kinship vectors, work list, series, copyright,
  greeting strings, and the door pool — **one artifact, one fetch**, under the bounded arrival
  (`INV-30`); no second request for any of it
- `sitemap.xml` — root plus every work page, each with an `<image:image>` (`INV-6`)
- `robots.txt` — disallow on `*.pages.dev` preview hosts, allow on production
- `config.json` — feature flags (all AI off, `INV-8`) + feel knobs + `site_url` + `ga_measurement_id`
- `gallery/` — images and the shared design tokens
- `/api/.gitkeep` — the reserved empty namespace for future serverless AI (`INV-7`)
- favicons — from the instance's `instance-assets/` dir when present
- When `ai_i18n`, `visitor_memory`, or `ai_story` is enabled:
  - `_worker.js` — the edge worker, with private story fragments baked in (`INV-1`)
  - `_routes.json` — routes only `/api/*` to the worker; all other paths stay pure CDN
  - `i18n_source.json` — the English string base the i18n worker translates from (public)

**The exhibition vectors** are computed by the bake from `vector.json`: every numeric axis across
all works min-max normalized to [0,1], output as neutral coordinate arrays under the key `v`. The
**version tag** is a SHA-1 of the sorted axis names — it changes whenever the axis set changes,
which causes old stored arcs to be discarded at next visit (`INV-12`). No axis name travels into
the bundle (`INV-1`).

**Config flags** live in `config.json` at the bundle root. The bake owns the flag schema; deploy
only sets values (via `--enable <flag>` at bake time or by editing the produced config). Every AI
flag ships false (`INV-8`); a feature turns on by flipping a flag and re-baking, never by
editing code.

**Reproducibility** (`INV-10`): items are sorted by id, the vector version is a content hash,
the copyright year is `datetime.date.today().year` (consistent within one bake session), no
wall-clock timestamps appear in bundle content.

**The deploy boundary:** `robots.txt` is the only file that differs between a preview host and
production. The production `site_url` drives canonical and `og:url` fields. The `_routes.json`
and `_worker.js` pair keeps every static byte on the pure CDN path; only `/api/*` ever invokes
the worker.

---

## Glossary
- **Work** — one finalist image in the content directory's gallery (`W`).
- **Feature Vector** — the ordered normalized axis values for one Work, used for kinship math
  in the browser (`FV`).
- **Instance** — one deployment: a content directory plus `site.json` identity (`I`).
- **Site Bundle** — the static deployable directory the bake emits (`SB`).
- **Bake** — the single local command that regenerates the bundle from the content directory
  (`BK`).
- **Exhibition** — the single adaptive touchpoint at `/`: one surface, two faces — static with JS
  off, live adaptive walk with JS on (`EX`).
- **Door** — the exhibition's threshold on a cold arrival: `door_size` works in one calm line,
  the pick IS the entry (`EX-DOOR`).
- **Gallery** — the museum walk behind the door: one work per viewport, caption in the margin,
  counter, breathing ground (`EX-HANG`).
- **Arc** — the kinship-ordered sequence of works assembled from the door pick (`EX-HANG`).
- **Closing screen** — the full-viewport rest after the last frame: «ещё N» while the budget
  lasts, the exit always (`INV-15` / `INV-17`).
- **Cold spread** — the diverse or configured-first hang shown when no pick has been made;
  the default hang when the door pool is absent or thin (`INV-14`).
- **Door pool** — the instance's curated `door_candidates.json`: the works that may stand at
  the threshold, ordered; the order is the curation voice (`EX-DOOR`).
- **Living hand** — the fresh set of `door_size` works dealt from the pool on each cold arrival:
  novelty + hour + curation, under the ≤⌊door_size/3⌋-repeat law (`EX-DOOR-3` / `INV-20`).
- **Room permalink** — the shareable deep link into the walk:
  `{root_url}/?utm_source=share&utm_medium=referral#w-<id>` (`EX-SHARE`).
- **Gracious deterrent** — the quiet answer to a grab: the `enjoy` toast plus the site host,
  never a scold (`EX-PROTECT`).
- **Told story** — one short associative line per work, written on demand at the edge, cached in
  KV, degrading to silence (`EX-STORY` / `INV-47`).
- **Ambient player** — one optional gapless loop, off by default, lazy-fetched on turn-on,
  credit from config (`EX-SOUND`).
- **Loading breath** — the solemn hairline shown while a frame's pixels travel; wordless,
  retired the moment pixels land (`EX-LOAD`).
- **Coat-check token** — an anonymous random id minted per browser; the edge keeps seen-work ids
  under it for the door's novelty voice (`EX-MEMORY` / `INV-25`).
- **Caption** — plain-language prose of what a work shows, from `content_tags.json`; for
  machines and assistive voices only by default (`CAP`).
- **Work page** — the flat crawlable `/w/<slug>-<idtail>` page for one work (`WP`).

---

## Formal index

### Entities

| Code | Entity |
|------|--------|
| `W` | Work — one finalist image |
| `FV` | Feature Vector — the normalized axis values for one work |
| `I` | Instance — content dir + `site.json` identity |
| `SB` | Site Bundle — the bake's output directory |
| `BK` | Bake — the one local command |
| `EX` | Exhibition — the adaptive touchpoint at `/` |
| `WP` | Work Page — the crawlable `/w/` page for one work |
| `CAP` | Caption — plain-language description, for machines only by default |
| `TS` | Told Story — the optional narrator layer (`EX-STORY`) |

### Clause anchors

| Anchor | What it covers |
|--------|----------------|
| `EX` | The exhibition root — one surface, two faces |
| `EX-DOOR` | The threshold on a cold arrival; thin/missing pool degrades |
| `EX-DOOR-2a` | Entry by pick only; no skip affordance |
| `EX-DOOR-2b` | One line, always (the layout algorithm) |
| `EX-DOOR-2c` | Full-bright windows; halo-only pointer; liveAccent |
| `EX-DOOR-2d` | Curated pool; the pool's order is the curation voice |
| `EX-DOOR-2e` | Ceremony B «через чёрное» |
| `EX-DOOR-2f` | The door locks the page (no scroll-behind) |
| `EX-DOOR-2g` | The idle hint — behavior, never a word |
| `EX-DOOR-3` | The living hand: novelty + hour + curation + ≤⌊door_size/3⌋-repeat law |
| `EX-DOOR-RELOAD` | Face survives a reload; gentle hand refresh (≥60% kept, ≤40% new) |
| `EX-GREET` | The door greeting in the visitor's language at their hour |
| `EX-GREET-LIVE` | The greeting re-speaks when the daypart changes |
| `EX-GREET-BAKE` | The baked string cache; the gen command; the fallback |
| `EX-LANG` | The corner language selector on the door |
| `EX-HANG` | The gallery: one work per viewport, caption in the margin |
| `EX-ACCENT` | The breathing ground and live accent |
| `EX-GLIDE` | The amortized scroll settle — sine in-out, never a snap |
| `EX-SHARE-BTN` | The per-frame share button: copies the room permalink, never navigates |
| `EX-SHARE-IN` | The permalink arrival: `#w-<id>` as a handed-over pick |
| `EX-SHARE` | The share feature as a whole |
| `EX-SOUND` | The ambient loop: off by default, lazy fetch, credit from config |
| `EX-SOUND-PAUSE` | Pause holds the moment; resume continues from it |
| `EX-PROTECT` | The gracious deterrent (grab → gift toast; pinch → silent refuse) |
| `EX-LOAD` | The loading breath: solemn hairline while pixels travel |
| `EX-SERIES` | The series side room: pill, crossing, lane / polaroids, honest close |
| `EX-STORY` | The told story: one line per work, leaned by light, degrades to silence |
| `EX-STORY-ORDER` | The light-lean: kinship + hour-discontinuity over time-of-day marks |
| `EX-STORY-LINE` | Each line's laws: ≤12 words, associative, note-grounded, no technique |
| `EX-STORY-EDGE` | The voice at the edge: `/api/story`, private fragments, KV cache |
| `EX-STORY-AB` | `story_variant` rides the GA beats as a dimension |
| `EX-I18N` | The any-language layer: one deferred fetch per new locale, KV-cached |
| `EX-EDGE-GUARD` | Three money fences before any model call |
| `EX-MEMORY` | The coat-check token: seen-work ids at the edge, anonymous |
| `EX-PULSE` | Six analytics beats on the GA wire (five + `series_open`) |
| `EX-TIMING` | Performance marks for the builder; `?timings` narrates them |
| `EX-RESET` | `?reset` wipes named keys; idempotent |
| `EX-MOTION` | One tempo, five duration tokens, fade-only entries |
| `EX-MOTION-R` | Reduced-motion collapse (tempo → 0.05; always wins) |
| `EX-ARRIVE` | The house breath: every appearing element fades in, never pops |
| `EX-ACCENT` | Bone at rest; the focused work's liveAccent tone in the hang |
| `EX-COPY` | The quiet copyright line on every public face |
| `WP` | The crawlable work page |
| `WP-CLEAN` | Extensionless clean addresses in every baked reference |

### Invariants

| Anchor | What it guards |
|--------|----------------|
| `INV-1` | No axis readout ever faces a visitor |
| `INV-2` | Static face complete without JavaScript |
| `INV-3` | Crawlable title never empty (fallback chain) |
| `INV-4` | One page per work, no orphan, no phantom |
| `INV-5` | Canonical and listed once (sitemap, robots) |
| `INV-6` | Every work discoverable as an image (image sitemap) |
| `INV-7` | Bundle self-contained and static; `/api/*` reserved |
| `INV-8` | AI ships off; all features degrade gracefully to static content |
| `INV-9` | Content is data, not baked prose |
| `INV-10` | Bake is reproducible (same inputs → same bytes) |
| `INV-11` | One arc bounded: `spread_size + max_unfolds × unfold_step` |
| `INV-12` | Old or mismatched walk state → clean start |
| `INV-13` | Place memory is per-tab (`sessionStorage`) |
| `INV-14` | Door never blocks entry (thin/missing pool → diverse hang) |
| `INV-15` | The walk ends (`max_unfolds` cap retires «ещё N») |
| `INV-16` | No one-way doors (door↔gallery loop) |
| `INV-17` | No dead void (controls in first viewport or visibly past fold) |
| `INV-18` | Back is honest (steps per face, not per frame) |
| `INV-19` | Face survives a reload (door stays door; walk stays walk) |
| `INV-20` | Living hand repeats ≤⌊door_size/3⌋ from the previous hand |
| `INV-21` | Door locks the page behind it (no scroll-behind) |
| `INV-22` | One tempo rules every motion (no hardcoded speeds) |
| `INV-23` | Reduced-motion collapses the tempo to 0.05 |
| `INV-24` | Every appearing element arrives by the house breath |
| `INV-25` | Coat-check token is anonymous (random string, seen-ids only) |
| `INV-26` | Model routes never a money tap (three fences: bot / IP / daily cap) |
| `INV-27` | Sound is off on a fresh visit; no audio fetches on cold load |
| `INV-28` | Archive signs its rooms (one quiet copyright per public face) |
| `INV-29` | Share toast never a silent failure (carries the link when clipboard refused) |
| `INV-30` | JS-off static face formed before JS wakes; 2.5s watchdog returns it |
| `INV-31` | The feel is configuration, never hardcode |
| `INV-32` | Work page carries `og:image` (absolute URL, width, height) |
| `INV-35` | `?reset` wipes named keys, idempotent, never blocks the arrival |
| `INV-38` | Performance marks are invisible to visitors; nothing leaves the tab |
| `INV-41` | Analytics consent declared first; no tag → total silence |
| `INV-43` | Coat-check: fire-and-forget reports; drop on failure |
| `INV-46` | Series side room degrades cleanly when series are absent |
| `INV-47` | The told story degrades to silence; the walk loses nothing |
| `INV-48` | Ambient player: OFF by default; lazy fetch only on turn-on |
| `INV-49` | The gracious deterrent is a gift, never a scold; no hard DRM |
| `INV-51` | Edge guard: three fences before any model call |
| `INV-52` | Sound pause holds the offset; resume continues from it |

### Deltas from the tlvphoto reference implementation

These are places where the engine's current code diverges from the behavior described above,
requiring reconciliation:

| Code | Description |
|------|-------------|
| `⟨DELTA-1⟩` | The door wordmark is hardcoded as a literal string in `exhibition.js` rather than injected from `site_name` at bake time. Every other instance-facing string is config-driven; this one is not. Reconcile: bake should substitute the wordmark from `site_config["site_name"]`. |
| `⟨DELTA-2⟩` | No display-cap on work images. The engine's bake copies images as-is into the bundle; the tlvphoto reference spec (`EX-PROTECT-RES`) capped the long edge of web derivatives at a display size to limit what a grab yields. This cap logic is not yet in `engine/build.py`. |
| `⟨DELTA-3⟩` | No `dateCreated` in the work-page JSON-LD `VisualArtwork` record. The engine's generic Work entity has no date field in `gallery_data.json`; an instance may extend the content contract to add one. |
| `⟨DELTA-4⟩` | The `series_open` analytics beat is implemented in `exhibition.js` but was not part of tlvphoto's spec. It is specified above as an engine-native sixth beat (`EX-PULSE`). |
| `⟨DELTA-5⟩` | The `sold` flag and its red dot in the caption zone are implemented in `exhibition.js` but the bake does not forward the `sold` field from `gallery_data.json` items into `exhibition_data.json`. The red dot is currently always hidden. Reconcile: add `"sold": bool(it.get("sold"))` to `ex_works` in `build.py`. |
