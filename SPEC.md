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
where every visitor meets a threshold — a handful of works asking which feels closer? — and the
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
[14,30]px). A resize recomputes live; a re-render happens only when count or orientation changes. A relayout
re-render rebuilds the windows with no entry fade; the fade belongs to a fresh open alone
(`EX-DOOR-2c`'s rise token — shipped 2026-07-09, the law written 2026-07-10). `EX-DOOR-2b`

**The windows are fully visible at once** (`EX-DOOR-2c`): no dimming at rest. The pointer is
answered by a **halo alone** — no brighten, no lift (hover-only on pointer devices,
`focus-visible` on keyboard). The halo's colour is the work's `liveAccent` tone, not the raw
dominant (a near-black dominant is invisible on the dark ground). There is no pick-highlight;
the pick answers with the ceremony. The window's own picture loads by the walk's in-flight ladder —
a plate in the work's raw tone, a wordless bar past a long wait, an accelerated reveal — its facts at
home in `EX-LOAD-2`; the halo (`liveAccent`) and the plate (raw `dom`) are two colour laws standing
together on the one window.

**The pool is curated and the hand lives** (`EX-DOOR-2d`, `EX-DOOR-3`): the pool's ORDER is
the curation — the file's order is the tie-break voice. Each **cold arrival deals a fresh hand**
of `door_size` works from the pool, chosen by three quiet voices: **novelty** (works the guest
has not met, from the coat-check seen-list when available or the local walk's own seen, come
first); **the hour** (the hand leans toward the daypart's tone using the candidates' own baked
`luma`/`warmth` numbers — darker for night, warmer for evening, brighter for morning and day;
a configuration knob, never a new fetch); **curation** (the pool's own order breaks every tie).
**His law:** a new hand repeats at most ⌊`door_size`/3⌋ works from the previous hand (stored in
`ex.hand`) — a returning visitor never meets the same threshold twice (`INV-20`). The re-opened
door (after the exit) shows the **standing hand** (the session's set is fresh-quiz-only in the
re-open sense: the pick is fresh, not the set mid-session; see `INV-16`). `EX-DOOR-3` `INV-20`

**The full circle retires the hand** (`EX-DOOR-4`): the standing-set law above holds everywhere
short of one carve-out. A walk comes **full circle** when every work of its current hang —
`order.slice(0, shown)`, the spread plus every unfold taken — has actually stood in view (the
walk's own in-session seen marks, counted the moment they are made so the record's debounced
flush never delays a circle, joined with the persisted seen copy in `ex.seenc` so a reload still
knows). The next time the door renders over a circled, not-yet-answered walk, the standing hand
**retires** and `EX-DOOR-3` deals a fresh one on the spot — novelty then naturally reaches past
the circled works, and at most ⌊`door_size`/3⌋ of the old hand may return. Every way the door
face can render counts as that render — the exit control, the browser's own Back landing on the
door, and a reload landing on the returned-to door behave alike; on this one point the history's
"as it stood" (`INV-32a`) yields, the fresh hand standing as the standing hand from that moment
on. An unconsumed circle also **outranks the reload refresh**: the reload law (`EX-DOOR-RELOAD`,
≥60/≤40) governs every reload with no circle pending, and governs the fresh hand's own later
reloads. **One circle, one deal:** the fresh hand is remembered together with the circle that
earned it (the walk's pick and its shown count, on the versioned `ex.hand` record), so walking
back and forth between the same circled walk and the door never re-rolls the door — the next deal
waits for the next circle, and a new pick or an unfold after the circle reopens the count (the
hang grew, so the circle is no longer closed). A hand stored by an older client carries no circle
memory — it reads as "no circle consumed" (one deal may fire once and writes the remembered
shape); a stale-versioned hand is dropped whole, as the walk's own state law already does
(`INV-26`). Where the museum's memory is off (`visitor_memory`), the walk's own in-session marks
still count the circle while they are at hand; with nothing left to count — a reload with no
stored seen record — the door keeps the standing-set law, quietly. `EX-DOOR-4` `INV-71`

**The diverse door (the `door_diversity` flag, default off — the curated hand above stands
byte-identical, `INV-19`).** An instance may turn the threshold from the curated pool to a diverse
door drawn from the WHOLE living gallery. With it on, three standing laws yield FOR THE DOOR alone:
every open deals a FRESH set — a cold arrival, a reload, and a return from a walk alike (this
overrides the session-held hand of `EX-DOOR-2d`/`INV-16`, the gentle reload of
`EX-DOOR-RELOAD`/`INV-19`, and the circle's deal-once of `EX-DOOR-4`/`INV-71`, all for the door
alone; the walk saved behind a pick still persists untouched). The set is chosen for even SPREAD
across the five measured axes (brightness, warmth, colourfulness, detail, symmetry): the picks seed
near the gallery's centre — a random one of the closest few, the per-open variety seed — and each
next pick is the work farthest from those already chosen. At least a configured fraction of the
SHOWN windows come from a named PLACE group — an instance sets both the group's keywords and the
fraction (default `0.6`) in its `door_diversity` site config — reached by swapping the
least-distinctive non-place pick for the place candidate that best keeps the spread until the
fraction holds. The ORDER varies too: a random axis and direction each open. The count follows the
viewport's fit (`EX-DOOR-2b`) and the place fraction holds among exactly those shown. `EX-DOOR-3`

**Novelty across visits — the door remembers what it has dealt (`fresh_min`, default `0.6`).** The
farthest-point spread on its own gravitates to the same extreme works — the parameter poles are
always the farthest points — so a returning visitor, most visibly on a phone where only three
windows show, would meet the same faces open after open. To prevent that the door keeps a local
memory of every work it has DEALT (independent of what the visitor actually walked — a
browser-local list, versioned so a new gallery build voids it, capped, forgotten by `?reset` with
everything else, `EX-RESET`; a second tab is the usual last-writer, `INV-26`). Each open then
guarantees that **at least `fresh_min` of the windows dealt for the current fit are works NOT in
that memory** — at the default `0.6`, two of three on a phone and three of five on a wide screen
have not been dealt recently — while the place fraction still holds. Because the two fractions
together can ask for more than the windows exist (`0.6n + 0.6n > n`), at least
`⌈fresh_min·n⌉ + ⌈place_min·n⌉ − n` of the shown windows must be BOTH unseen AND place; the deal
honours all three counts JOINTLY (it only adds a work while the remaining slots can still reach
every count), preferring unseen works throughout — a set is typically wholly fresh while the pool
is deep. This novelty floor is the diverse door's own repeat bound and SUPERSEDES the curated
door's at-most-⌊door_size/3⌋-repeat law (`EX-DOOR-3`/`INV-20`) here, as `EX-DOOR-3` already
supersedes that clause's dealing for the diverse door. When the unseen pool can no longer supply
the fresh floor — or the unseen-place overlap the two fractions jointly demand — the memory is
cleared and a **new round** begins over the whole pool: the just-dealt set REPLACES the emptied
memory (a normal open instead UNIONS its set in) so the very next open still differs. Over a round
the door thus walks the whole gallery before any work returns, then walks it again — bounded
repetition, never the same few. On a gallery no larger than the door's own window count there is no
round at all (the whole pool shows every time). *Facets:* the door looks the same, its works and
their order differ each open and rarely repeat within a round; performance — the deal and its one
memory read/write run once per open over the gallery, never on a resize. *Non-goals:* a single
fixed "best" door (variety is the point); a fraction the data cannot support (it is capped by how
many place works exist); a memory that outlives the browser or the `?reset` (it is local and
forgettable). *Success measure:* five cold opens give five different sets, each with at least the
place fraction from the place group and at least `fresh_min` works not dealt since the last round
reset, in a varying order `[default]`. `EX-DOOR-3` `INV-20` `INV-74`

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
immediately — persists across visits (`ex.lang`), and outranks the browser setting everywhere a
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

**The one-frame walk** (`EX-GLIDE`): the walk advances **one work at a time**. Every input — an
arrow key, a wheel notch, a touch swipe, done HOWEVER — makes **exactly ONE** ideal transition to
the adjacent frame in that direction. It **always starts smooth and always lands smooth, CENTERED**
on the target work; it **never rests between frames** and **never drifts or floats afterwards**.
The transition is a **sine in-out** (the calmest classic curve — lowest peak speed, both ends soft;
monotonic 0→1, so it provably **cannot overshoot** and always lands centered, no bounce), over
`glide_ms` (config, default 520ms) scaled by `tempo/1.35` capped ×1.5 — the docking rides the one
clock (`INV-33`), reduced motion collapses it near-instant. **Force is IGNORED in phase 1**: one
fixed curve for every input, always exactly one frame. (A **phase-2 hook** is left in the animator —
force will later seed the same transition faster off the start, capped at one extra frame — but is
NOT built here.) A **second input mid-transition chains** to the *next* frame — it steps from where
the running transition is headed, never re-rounds backward. A sub-2px move is skipped.

The input surfaces split. **Desktop** (wheel + keys) is owned by the **JS animator**, which
`preventDefault`s to kill native free-scroll — so no lingering momentum can float after the stop.
A mouse notch is one event; a trackpad swipe is a decaying burst — a **lock coalesces the burst to
ONE step**, and an idle timer (~150ms) clears the lock when all motion stops. A **new swipe fired
during the previous swipe's momentum tail is NOT dropped**: it shows up as a **rising `|deltaY|`**
over the decaying envelope (`fresh = !lock || mag > peak·1.3 + 1`), which re-arms a second step; the
plain tail stays coalesced. **Paging keys** (`Space`, `↓`, `→`, `↑`, `←`, `PageDown`, `PageUp`, and
`Shift+Space`) make the same one transition — all four arrows page: ↓ and → walk forward, ↑ and ← walk back (his
2026-07-09 note, landed 2026-07-10; physical directions in every locale `[default]`) — one step per press, chaining from the running
transition's heading; a held key is one frame per press. **Touch** docks under native momentum via
**CSS scroll-snap** (`scroll-snap-type:y mandatory` + `scroll-snap-align:start` +
`scroll-snap-stop:always`, scoped to `@media (hover:none)`): **no JS ever writes the scroll position
on touch**, so a swipe never flies through, never rests between works, and the iOS jerk-fix holds by
construction. The cold **door ignores a wheel** — the animator owns the walk only, never the door,
the ceremony, or the side room.

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
share button replaces the retired ↗ corner link; the walk no longer links out per frame. Since
2026-07-09 it is ONE control FLOATING over the walk as fixed chrome (never riding a frame, so
nothing drifts with a scroll): its target follows the work IN VIEW; it shows with a work, leaves
on the closing screen, and hides with the rest of the walk chrome at the door. The round floating chrome sits on
ONE vertical rail: the link and the sound player centre on the same x from the right edge at every
width and orientation (his 2026-07-10 landscape note), and the toast answers right-aligned just above
the link button it belongs to, never far away over the work. `EX-SHARE-BTN`

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
editing, filter, or cut). Arrives by the house breath on `--tone`-tinted text.

**A plot per opened portion** (`EX-STORY`, resolves `⟨DELTA-16⟩`): the story's unit is the PORTION
just opened — the cold first spread is itself the first portion, then each «ещё N». Every portion
asks `/api/story` for ITS OWN ordered ids alone (never the grown `0..shown` set), under its own
cache key, so a line already read is never re-requested and never shifts under the eye, and no
portion is ever named a «part N» of another. A portion counts as told only once its plot has come
back: the told-key is stamped on a SERVED plot alone, so a refused or failed portion stays OWED and
is re-asked at the next natural beat — a further unfold, or a return to the walk. The edge's own
wait carries any `Retry-After`: a re-ask inside the window is refused server-side before any model
call, so the client holds no backoff clock and re-asks freely. A fresh door pick resets the story
(no portion or line leaks across picks). A mid-visit language switch keeps every already-told line
in its first tongue (`respeak()` re-labels chrome only, never the told lines); only a portion opened
after the switch reads the new language. This settles the earlier `story-unfold-recovery` open call
(the same-sitting follow-on and the return visit meet one law — a portion is its own plot, so there
is no thread to keep and no arc to re-voice).

**The voice lives at the edge** (`EX-STORY-EDGE`): the walk sends the ordered ids + variant +
language to `/api/story`; the worker reads the PRIVATE story fragments (title/place/subject/light
are public grounding; the `story_notes.json` note is the instance's own words, adapted never
quoted) and calls a small model (Haiku); the answer is kept in KV forever under a key of the
**ordered id sequence + variant + language + params_version** (bumped whenever
`story.light_weight`, the prompt, or the marks change — so a knob flip never serves a stale
order). Each opened portion is its own ordered sequence, so each portion's plot lands under its own
key and serves free from cache on a re-ask (`⟨DELTA-16⟩`). One model call per distinct portion, $0 after. A failed or absent voice is SILENCE — the
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
in `ex.sound`. A return visit with preference ON **arms** on the first gesture (the browser
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
pinch-zoom / `gesturestart`) the engine intercepts. A **desktop right-click** (a fine pointer)
opens the **gift ceremony** (below) — the picture is offered, never dumped. A **drag or a touch
grab** shows a **quiet, localized gift line** on the existing share toast instead — the instance's
`enjoy` string from the greeting cache plus the site host appended in code (e.g. «enjoy ·
example.com»), arriving on the house breath and leaving by itself. For a pinch-zoom the walk refuses the browser
zoom across the **whole surface**, not only over a work: a browser zoom scales the visual viewport
out from under the JS scroll animator and the fixed chrome, so the measured centering drifts and the
fixed controls float and the walk desyncs. `gesturestart` / `gesturechange` / `gestureend` are
`preventDefault`ed document-wide (Safari's gesture events), a two-finger `touchmove` is refused
(Blink's pinch), and the viewport meta pins the page to scale 1 on Blink. iOS ignores that meta,
so double-tap-to-zoom is refused by `touch-action:manipulation` on the walk body, and a pinch that
drops back to one finger re-takes the paginated walk so its tail cannot free-scroll. EX-CHROME's
one-page-shape law extends to the zoom axis. It stays silent — a pinch is exploratory, not a save, so no toast. A
**soft CSS layer**
rests on every `img.work`: `user-select:none`, `-webkit-user-drag:none` (no drag ghost),
`-webkit-touch-callout:none` (kills the iOS long-press save sheet). This is a gift and a gentle
nudge, never hard DRM — devtools, view-source, and screenshots still work, said plainly.
`EX-PROTECT` `INV-49`

### The gift ceremony

The picture is never dumped by a blunt auto-download. A desktop right-click on a work, and a won
quiz, both **open a solemn card** — a thumbnail rising into place on the reveal clock (`EX-ARRIVE`),
the localized ask («like it?» / `gift_ask`), a **yes** button («a gift :)» / `gift_yes`) and a
quiet **no** («not now» / `gift_no`), the gracious `enjoy · host` line, and an optional buy line
(`gift_buy`, empty by default). The file is handed over **only on the yes** — never automatically.
Esc or a click outside closes it. `EX-PROTECT-GIFT`

### The clean image, the marked take

The **shown** image is clean — no watermark burned into what a visitor looks at. The site-host mark
is stamped **only on a taken copy**: a grab-download marks the picture **client-side via canvas**
(the host from config drawn bottom-right, a soft shadow under a bone fill) at the moment of the
yes; a browser that refuses the canvas still receives the clean file (never blocked). The **served
gallery copies** carry no mark unless the deploy caps them (`--display-max`), in which case the same
host mark is baked server-side (`_stamp`). The **quiz prize** is a pre-marked gallery derivative
and goes out raw. The download filename is a **slug of the site name** from config (e.g.
`<site>-<original>.jpg`, `<site>-wallpaper.jpg`) — no hardcoded brand. The mark text is the site
host from config, never a literal. `EX-PROTECT-RES` `INV-56`

### The work's question and its gift

An instance may attach a **quiz** to any work through an optional `<content>/quiz.json`
(`{"quizzes": {"<id>": {"prompt", "options"[4], "answer", "prize"}}}`). The question is a
**four-option guess**: the **prompt and the four option labels are public** — baked onto the work,
the chip label localized — while the **one correct answer is private**, together with the prize
path, baked **only into `_worker.js`** (the one bundle Pages never serves) and only when the `quiz`
flag ships on; flag off ⇒ no quiz key on any work and the walk is byte-identical. A quiz-bearing work
advertises a subtle **«question?» chip** (`quiz_ask`, localized) on its plaque, over which a soft
one-time glint runs as it appears (`EX-QUIZ-GLINT`). Tapping the chip opens a **compact card that
sits over the still-visible photograph** — a light scrim for legibility, never a black curtain — with
the prompt and the **four options in a 2×2 grid**. The card's accent is the **focused work's own live
tint** (the per-work accent the walk already computes) so it reads with the picture in view, and its
`dir` mirrors the active locale (Hebrew mirrors). **One tap locks** the answer — the un-chosen options
dim, no re-pick. The tapped option POSTs to `/api/quiz`; the edge **normalizes both sides hard**
(NFKC-fold, lower-case, letters only) and compares against the private single answer. **The answer is
judged at the edge, never a served byte, never a model call**; the client sends the **raw** tapped
value, so client↔edge normalization is **parity by construction**. The judge runs under the quiz's
**own** hourly per-IP attempt fence (`q:<hour>:<ip>`, separate from the model rate-limit and day
budget), which **degrades gracefully when no KV namespace is bound** (a preview/local deploy still
judges). A **miss** (or an unreachable edge) shows **one** gentle localized line (`quiz_wrong`) and
then the card **fades out, leaving the photograph** — no hint trail, the answer never reaches the DOM.
A **hit** shows a localized praise line (`quiz_win`), is remembered per work in visitor memory, and
opens the **gift ceremony** at the prize's better resolution. **Exactly one question appears per show**
(`EX-QUIZ-ONCE`): the chip is placed on ONE work chosen per walk over the eligible set — works that
are both **reachable on this walk AND not already answered** — and, after a show that asked, the chip
stays silent while less than the **cooldown window** has passed (`quiz_cooldown_hours`, default **6h**,
a config knob; `quiz_probability` is **retired** — one-per-show supersedes the old per-work coin). The
quiz never appears on a button-only screen (door, closing). Every visitor-facing quiz + gift chrome
string (`quiz_wrong`, `quiz_win`, and the gift ceremony strings below) resolves through the
**localized string set** (`EX-I18N`) with **English source-tongue fallbacks** in the client — no
non-English literal ever ships; the **question content** stays instance-supplied. Off / no answer /
unknown id ⇒ the route 404s and the walk loses nothing.
`EX-QUIZ` `EX-QUIZ-EDGE` `EX-QUIZ-PRIZE` `EX-QUIZ-ONCE` `EX-QUIZ-GLINT` `INV-59` `INV-60` `INV-64` `INV-65` `INV-66`

**The faces meet — input, chrome, and viewport when surfaces stand together (the 2026-07-09 bug class
closed as law: every stateful surface composes with each neighbour it can meet).** *Regression fences
first (each citing the clause it guards): reaching the closing screen still clears the plaque (EX-HANG);
an answered question still drops its chip (EX-QUIZ-REPLY); a viewport aspect change still rebuilds the
door without the entry fade (EX-DOOR-2b); the share button still leaves on the closing screen and the
door still hides it (EX-SHARE-BTN); every motion rides the one tempo (INV-33).* The laws of the meetings:
- **One face stands over the walk at a time.** The faces are the side room (EX-SERIES), the question
  card (EX-QUIZ-REPLY), and the gift card (EX-PROTECT-GIFT); each opens only from a surface the others
  cover, so two can never be summoned together. The one legal hand-off is the win: the question card
  passes INTO the gift ceremony as one continuous standing — ownership crosses in the same breath, and
  Esc always answers the face that stands at that moment.
- **A standing face owns the input.** While any face stands, the walk beneath holds its frame: keys,
  wheel, and touch all rest until the last face leaves (the face's own scroll stays native). A question
  always stands over the work it asks about; the room never slides away beneath a standing face. (The
  keyboard path is the 2026-07-10 find — wheel and touch were already caught by the overlay guards; the
  side room already held keys through its own lock.)
- **The last face leaves into a fresh-measured room.** When the last standing face leaves — a card
  closing, the side room closing, the gift ending a win hand-off — the resting frame re-centres to the
  work that stood beneath the face, measured against the live viewport, so a rotation that happened
  under a face is honoured the moment the walk is bare again. This re-centre is INSTANT and discharged
  under the leaving face's own fade — it is a correction with no designed motion of its own, so it can
  never race a glide for the scroll position (INV-33 is untouched and reduced motion changes nothing
  here); the bare viewport re-dock with no face standing keeps EX-GLIDE's own quiet glide. An input
  arriving in the same beat runs from the corrected centre.
- **The card is viewport-honest.** The card lays itself out from the live viewport alone (full-viewport
  flex centring), so a mid-question rotation reflows it centred with its options intact. A tap already
  given survives any rotation locked (EX-QUIZ-REPLY's one-tap law), and a rotation under an open card
  writes no second cooldown stamp — the stamp belongs to the open alone (EX-QUIZ-ONCE).
- **The side room covers the walk's chrome; the player rides above the room alone.** Under the opaque
  side room the share button, the caption, and the counter sleep, invisible and unclickable — so the
  copied link can only ever name a work in view (EX-SHARE-BTN kept by construction). The sound player
  stays visible and TAPPABLE above the side room (EX-SOUND — house chrome over the walk's faces). A
  standing card covers the player too: the music keeps playing, and the player's buttons rest until
  the card leaves. The side room grows no question chip and can open no card: the ask lives on the
  plaque, and the plaque sleeps beneath (EX-QUIZ-PICK).
- **The side room reflows with the viewport.** The table lays its prints in viewport fractions, so a
  rotation re-lays them. A print lifted to the light re-centres to the new viewport; a centre measured
  before the rotation never survives it.
- **The closing screen is a stop of its own.** The quiet re-dock after a viewport change counts the
  closing screen among its landings, so a rotation at the walk's end leaves the visitor at the end.

*Facets:* phone rotation is the law's home case; the keyboard is the input law's very subject;
performance — one instant re-centre per face-leave, no re-render. *Non-goals:* how rotation FEELS on a real device
(his phone stays that gate — the pinned real-device list names it); the gift ceremony's internals
(EX-PROTECT-GIFT unchanged); a landscape-specific layout for the card or the room. *Success measure:*
a visitor mid-question rotates the phone — the card stays centred and locked, the room beneath holds
still, and when the card leaves the frame re-centres; a key pressed during a question moves nothing;
a lifted print re-centres on rotation `[default]`. `EX-COMPOSE` `INV-67`

**One page shape for the browser on every face (the 2026-07-10 rotation find, closed as law).**
*Regression fences first (each citing the clause it guards): a standing face still owns the input
(EX-COMPOSE); the last face still leaves into a fresh-measured room (EX-COMPOSE); the side room
still covers the walk's chrome (EX-COMPOSE); every motion still rides the one tempo (INV-33).* The
browser owns its own frame — the address bar and tab strip come and go on the browser's own
judgment, and the house cannot command them. What the house CAN do is show the browser the same page
on every face, so that judgment falls the same way everywhere:
- **The walk's document is the page, whatever face stands.** While a face stands over the walk — the
  re-opened door, the side room, a question card, the gift card — the page beneath stays the walk's
  own tall document, holding its scroll place. For locking purposes the STANDING DOOR is a face like
  the others (EX-COMPOSE's list gains it for this law alone): it rests the walk's input the same way,
  while its own controls — the windows, Back, the language mark — stay live, and the leaving door
  keeps the rest through its whole ceremony (EX-DOOR-2e). A face locks the visitor out by resting the
  input (keys, wheel, touch) and by hiding the root scrollbar for its stay WITHOUT moving the
  page (the gutter keeps its width, so nothing behind a translucent card shifts on open or close).
  A moving finger the face EATS AT THE SOURCE: a drag over a standing face lets the browser scroll
  only while the finger stands on a part of the face that can truly take the movement along the drag's
  own axis — the side room's polaroid lane along its length, a text field — and everywhere else the
  move is consumed before the browser turns it into page scroll, so the walk beneath never receives
  the drag at all (EX-COMPOSE's carve-out, narrowed from «anywhere on the face» to the genuinely
  scrollable parts; the 2026-07-11 field find walked through the broad reading — a drag on the
  question card's translucent scrim slid the walk hundreds of pixels behind it and jerked it back on
  lift). A lane that runs out does not hand the leftover to the page: the chain stops at the face's
  edge. Any scroll that lands regardless is snapped back in the same beat, a correction with no
  designed motion of its own (INV-33 untouched) — with drags eaten at the source, this guard is the
  BACKSTOP for what source-eating cannot reach: a dragged desktop scrollbar, the phone's own
  rubber-band. The guard corrects only at input REST: while a pointer or touch is DOWN it HOLDS — a
  correction written mid-touch is a per-frame fight the visitor sees as the whole screen trembling
  (the 2026-07-10 phone find); the guard settles ONCE, when the last finger lifts, and because the
  face already ate the drag, the settle answers a few rubber-band pixels, never a long slide. The
  guard answers only scroll the house
  did not write itself — the door ceremony's glide to the picked work, the Back restore, and the
  face-leave re-centre all pass. EX-COMPOSE's «the room never slides away beneath a standing face» is
  discharged at the source for touch (the face eats the drag) and by the guard for everything else
  (the dragged desktop scrollbar, the rubber-band's leftover) — resting finger or moving, the walk
  beneath a face stands still. The overflow cut on the page root is retired as a locking
  device: it is exactly what told the browser the page stood still and handed the frame back on
  rotation.
- **A rotation meets the same page on every face.** Because every face keeps the same tall, in-place
  document, a rotation at the re-opened door, in the side room, under a card, or bare mid-walk hands
  the browser the same material — whatever the browser then does with its frame, it does it uniformly
  across faces, today's and future ones alike. A face built later inherits this law by construction:
  it locks by resting input, and the page beneath it stays the walk's document.
- **The cold door is the browser's own moment.** Before the first pick nothing has scrolled and the
  walk's tall document is not yet built; the browser shows its frame as on any fresh page, and the
  house does not fight it. The walk's first steps are what tuck the frame away, and from there the
  law above keeps every face equal.

*Facets:* phone is the law's home case; touch and keyboard — the input rest covers both, the touch
half now eating drags at the source (EX-COMPOSE's carve-out narrowed above); empty/error/loading —
the cold door is the named empty case above;
accessibility — the hidden scrollbar lives only while a face stands, and the bare walk keeps the
browser's own bar `[default]`; performance — the lock swap adds no render work, and the snap-back
guard listens only while a face stands `[default]`. *Fit:* no arrival, step, or exit changes on any
journey — the law only steadies the browser's frame around them. *Non-goals:* forcing the browser's
frame to hide (the browser owns it); a dynamic-viewport (dvh) relayout of the frames (the measured
stops already absorb the height difference, EX-GLIDE); an installable app shell. *Success measure:*
one rotation behaviour on every face — rotating at the re-opened door or in the side room leaves the
browser's tabs exactly as a rotation inside a room does `[default]` (a real-device fact; the owner's
phone is the gate). And the still walk is machine-proven: a slow drag over any standing face moves
the page beneath by zero pixels and leaves no jump on lift (the moving-finger row beside the
resting-finger one); the trembling's absence on the owner's phone stays a real-device gate.
`EX-CHROME` `INV-70`

### The loading breath

Wherever a frame in view holds a work whose pixels have not arrived, the frame — after a short
grace beat (~350ms×tempo, so a healthy network never sees it flash) — breathes a **thin hairline**
in the current accent tone, centered where the work will hang, breathing at tempo: solemn,
minimal, wordless. The work reveals the moment pixels land — the room's own quiet fade. A failed
image retires the breath; the caption and counter still hold the frame; no error face. `EX-LOAD`

### The in-flight ladder — a frame in flight wears the work's own tone

The lone-hairline breath (`EX-LOAD` above) **grows into a tone ladder**. Stepping onto a work whose
pixels are still crossing the wire, the visitor meets neither a black hole nor a spinner: after the
grace beat (`load_plate_grace`, ~0.35s×tempo, so a healthy line never sees it) the frame settles into
the work's **own dominant tone** — a plate in the same per-work `dom` colour the ground and door halos
already wear (used **raw**, not the lightness-raised `liveAccent` a halo needs against the dark ground).
On a genuinely long wait (`load_bar_wait`, ~1.5s×tempo) a **thin wordless bar** joins on the plate — an
eased indeterminate crawl in the accent, never a percentage, never a digit (`INV-1`) — so the plate is
never mistaken for the picture; on a silent stall it simply holds there (the honest indefinite state —
the ladder owns no timeout, the browser's fetch does). The photograph fades in **over** the plate the
moment pixels land: **crisp** when it beat the plate (`load_reveal_fast`, the soft token) and **graceful**
when the plate stood (`load_reveal`, the reveal token). The arm **reads the settled state first**: a warm
image (`complete`, real pixels) reveals at once with no plate and no clock; an already-errored one retires
at once — never a wait on a spent event — and it arms **once** per frame-taking-view, so a post-reveal
tier swap (`INV-63`) never returns a shown photo to the plate. This supersedes the breath's lone hairline
and re-carries all its promises whole (no empty frame, wordless, retire-on-load-or-error, one reused
overlay per call-site); the one non-goal that changed — a wordless bar past the long
wait — is amended by name, numbers still forbidden. **The door's five windows ride this same ladder**
(the walk's own arm at a second call-site, `EX-DOOR-2c`): a window whose baked light derivative is late
wears the work's own raw `dom` as a plate inside the window, adds the same wordless bar past the same long
wait, and fades the photograph in over the plate on arrival — the same knobs, none added; five plates may
fly at once (a plate per window, not the walk's single reused overlay), each reading the settled state the
way the walk's arm does, so a cached window reveals at once with no plate and a relayout re-render or a
fresh full-circle deal re-flashes none. The window's breathe-in entrance and its `liveAccent` halo stand
untouched while the plate speaks the raw tone inside. **Outside the ladder:** the crossing warms the picked
work, so the room opens without a plate (only a cache-evicted or slow first image falls through here); the
side room's lane/polaroid members keep their own lazy render. So the ladder governs the **walk's in-view
frame and the door's windows only**, and continues behind any standing face; the door emits **no walk
loading marks** — it stays off the walk's counter — and does not preload (`EX-LOAD-3` is the walk's alone).
The knobs ride `config.exhibition` (`INV-28`), each a beat ×tempo (`INV-33`); the order
`load_plate_grace` < `load_bar_wait` is law, clamped at boot. `EX-LOAD-2` `INV-72`

### The next work quietly preloads — the walk arrives warm

While a work rests in view, the exhibition quietly fetches the **next** work of the walk at the tier the
device would pick (the same `srcset`/`sizes` the in-view img uses, `INV-63`), so by the time the visitor
steps on, its pixels are already warm and the ladder above never even shows its plate. Exactly
`preload_ahead` works ahead are warmed (default **1** — one ahead, the bounded reach; the whole arc is
never prefetched, `INV-25`/`INV-30`). "Next" **follows the feet**, not a fixed arrow: it is the next work
in the visitor's current direction of travel — a backward step re-aims the warm-ahead to the work further
back, and a `#w-` landing (`EX-SHARE-IN`) starts a fresh one-ahead from the landing frame once it rests,
forward by default until a step declares a direction. The preload is **best-effort and silent**: a failed
or slow preload costs nothing (the in-view ladder still catches the frame when it is stepped to), and a
preload in flight is abandoned cleanly on a turn or jump (no stranded fetch fighting the in-view image).
Client-only — no bake output (the tone and tiers are already baked), no worker, no flag. `EX-LOAD-3` `INV-73`

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

**The site outlives its model account — a dead balance reads as a quiet English day (his 2026-07-10
words: «если закончились деньги на ИИ — всё на английском остаётся» · «приветствия просто "привет"»).**
*Regression fences first (each citing the clause it guards): the three money fences above stand
untouched (EX-EDGE-GUARD); the baked seven still never touch the model (INV-42); a cached locale or
walk still answers at $0 (INV-42/INV-47); the story's absence is still silence, never a broken frame
(EX-STORY-EDGE); with the flags off nothing changes (INV-19).* When the model ACCOUNT itself is dead —
Anthropic answers a committed call with a billing, credit, or auth refusal (a 4xx other than 429: the
low-balance 400, a revoked key's 401/403) — the edge treats the rest of the hour like a capped day, and
remembers: the death is flagged in KV for about an hour `[default — a config knob]`, and while the flag
stands no model call is attempted or charged. Behind the flag the i18n route serves the baked ENGLISH
straight (the bots' own path), never cached under the asked locale — a real speaker still earns a real
translation once the account lives again; the story route is silence. In this English day the greeting
is one PLAIN neutral hello line, with no daypart variants and no flourish (his word: «просто привет»)
— the line lives as a new reviewed `plain` field in the one greetings source (English is the day's only
tongue, so the English field is the load-bearing one; the shape check grows with it). The baked seven
never meet this day at all, and the client changes nothing — the worker's payload is the whole story.
Two calls dying together raise the same flag once (the write is idempotent), and the dying call itself
stays charged — the cap's charge-on-commit law is untouched. Transient troubles stay transient: a 429,
a 5xx, or a network failure keeps today's behaviour — one failed call, the existing `model unavailable`
answer — and never raises the flag. *Facets:* nothing new
faces the visitor beyond the quiet English; performance — one KV read the routes already pay.
*Non-goals:* retry heroics; an operator alert (the traffic report shows the flag when he looks);
reviving the account mid-hour (the flag expires by itself). *Success measure:* with the model answering
a dead-balance refusal, a non-baked-locale visitor walks a fully English site greeted by a plain hello
— no Russian literal, no broken line, and not one further model call charged that hour `[default]`.
`EX-EDGE-DEAD` `INV-68`

### Visitor memory

When `visitor_memory` is on, a first visit **mints a random token** (`ex.visitor` in
`localStorage` — a random string, never anything identifying) and, as the visitor walks, the
frames they actually met collect and report quietly to `/api/visitor` (debounced at ~3s,
fire-and-forget; a failed report is silently dropped). The edge keeps **ONE record per token** —
seen-work ids, merged across visits, capped at ~500 newest, expiring after ~180 days of silence —
and hands it back on boot so the door's novelty voice can prefer unseen works. The local
seen-list (`ex.seenc`) mirrors the report for sessions without server memory. Forgetting is
whole: `?reset` wipes the token and the local list (`INV-25`). `EX-MEMORY` `INV-43`

### Analytics — the event registry

The walk counts its beats for the site owner — the **event registry**. Events ride the ONE
sanctioned analytics wire, the baked GA tag, if `ga_measurement_id` is configured; no tag baked →
total silence, the walk never errors. An event carries at most the plain beat name, the work's
public id, and a word from a closed BAKED ladder (an arm, a stage, a kind, a tongue) — never free
text, never a vector (`INV-1`). **Consent defaults declare first**: advertising storage/use DENIED;
analytics measurement GRANTED; no cookie banner (a quiet exhibition). The wire carries exactly the
REGISTRY's beats — the table below is the one home of what the exhibition measures, and a standing
test holds it in BOTH directions: a beat in the code missing from the registry is red, a registry
line with no live emitter is red (born of a real drift — `series_open` once shipped onto the wire
with no spec sentence, which the old "five beats" prose could not see). `EX-PULSE` `INV-41`

| beat | when it lays | carries |
|---|---|---|
| `door_pick` | a window opens the room | the work |
| `walk_unfold` | the «more» control grows the hang | — (dimensions ride) |
| `walk_exit` | the walk leaves for the door — the exit control OR the browser's own Back, ONCE per leave (a Back-exit counts no less than a button-exit; the funnel undercounted history leaves until this port) | — (dimensions ride) |
| `share_copy` | the link button copies | the work |
| `share_arrive` | an arrival by a shared link | the work |
| `sound_on` / `sound_off` | the ambient player toggles (EX-SOUND's own clause) | — |
| `series_open` | the side room opens | the work whose series opened |
| `series_lift` | a print lifted to the light in the side room — every lift counts, setting it back down does not `[default]` | the lifted work |
| `gift_download` | a gift file actually leaves for the visitor's device (on the prize's yes this beat lands BESIDE the quiz funnel's `gift` stage — a beat and a dimension marking one moment, never a double event) | the work + `gift_kind` from the closed pair `quiz_prize` / `grab` |
| `lang_pick` | the guest chooses the exhibition's tongue at the door | `lang` — a code from the baked list (the guest's own outsider tongue reports as `other`, so the ladder stays closed) `[default]` |

When a told story, the quiz arm, or the quiz stage walks beside the guest, each rides
`walk_unfold`/`walk_exit` as a **dimension** (EX-STORY-AB, EX-QUIZ-AB, EX-QUIZ-FLOW) — a new beat
only when it IS its own moment, otherwise a dimension on an existing beat, never silently. **The
named silences** (deliberate, so the honest picture stays honest by decision rather than omission):
the walk's individual steps and wheel turns; the sound volume drag; a pinch on a work; the door's
idle hint; the side room's close (its open already counts the visit) `[default]`. `⟨DELTA-12⟩`

### The reset address

Opening the exhibition root with `?reset` in the address **wipes the browser's own trace** before
anything restores — named keys only: `ex.exhibition`, `ex-tempo` (in `localStorage`) and
`ex.place`, the hash hand-over marker (in `sessionStorage`), then `ex.visitor`, `ex.hand`,
`ex.seenc`, `ex.lang`, `ex.sound` (in `localStorage`). The param strips itself via
`replaceState` — no history step laid, Back stays honest. A storage refusal never blocks the
arrival. Idempotent: with nothing stored it does the same, silently. The worst a hostile
`?reset` link costs its clicker is their own walk position — nothing of anyone else's, nothing
server-side. `EX-RESET` `INV-35`

### Performance timings

Every live walk lays quiet performance marks at its beats — arrival, data landed, door shown,
pick, hang rendered, the breath, an image landing, reveal, caption, unfold, exit — named `ex:*`
in the browser's own `performance` timeline. Nothing faces the visitor (`INV-1`); nothing leaves
the tab (`INV-7`). With **`?timings`** in the address the console narrates the beats as they land;
`EXTimings()` returns the marks as data. `EX-TIMING` `INV-38`

### Motion, feel, and appearance

**One tempo, five duration tokens** (`EX-MOTION`): every CSS duration and JS wait on the walk's
surfaces multiplies by `--tempo` (config `exhibition.tempo`, default 1.35). Five named tokens:
soft `.6s` (captions, hovers, toasts) · reveal `2s` (a work entering) · rise `1.4s` (the door's
windows) · ground `1.7s` (the tone shift) · cross `1.2s` (the door ceremony). Entries are
**fade alone** — rise/lift transforms are not used. No hardcoded duration may bypass the clock
(`INV-22`).

**Reduced motion** (`EX-MOTION-R`): under `prefers-reduced-motion: reduce` the tempo collapses
to `0.05` — every move lands near-instant, nothing breaks. Reduced-motion always wins over a
visitor's `localStorage['ex-tempo']` override. A visitor or a test may pin the tempo via
`localStorage['ex-tempo']`, clamped to [0.05, 3] (`INV-23`).

**Every appearing element arrives by the house breath, never pops** (`EX-ARRIVE`): any UI element
whose first visible entry could appear sudden carries an opacity-from-zero fade riding `--d-soft`.
The idiom: keep the layout toggle (the absent element costs no layout), then
`requestAnimationFrame(() => el.classList.add('show'))` so the next-frame paint sees `opacity:1`
after the CSS transition fires. Dropdowns that also close by removing `.show` use
`setTimeout(hideAfterFade, d_soft_ms)` so opacity returns to 0 before the layout collapses
(`INV-24`).

**The feel is configuration, not hardcode** (`INV-31`): every feel knob lives in `config.json`
under `exhibition`. An unrecognized value renders the default, never a crash or a blank.

**A knob at its built-in default (or empty) is SUPPRESSED from the emitted config** (2026-07-09):
the served `config.json` carries only what the instance actually set. Safe because every client
read is fallback-guarded (`glide_ms`→520, `quiz.placement`→plaque, sound off without a URL);
`site_name` is emitted only when the ENGINE's own client ships (an instance client that carries
its own wordmark doesn't read it).

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
| `sound_url` | absent | path to the .m4a file; absent/empty = no player |
| `sound_credit.artist` | absent | artist name for the credit tray (joins with `sound_url`) |
| `sound_credit.title` | absent | track title for the credit tray |
| `sound_credit.url` | absent | artist website for the credit tray |
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
- the exhibition client (`exhibition.js`, `exhibition.css`) and the worker TEMPLATE (`worker.js`)
  — the instance's own copies WIN when its assets dir carries them (2026-07-09: an instance that
  grew its client first keeps shipping it byte-exact; the generic client serves everyone else);
  the `?v=` asset hash is computed over the SERVED client, whichever side supplied it
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
| `EX-DOOR-4` | The full circle retires the hand: seeing every hung work earns a fresh deal on the next door render (all three renders alike), one circle one deal (the consumed circle rides the versioned hand), the standing-set law holds short of a circle |
| `EX-DOOR-RELOAD` | Face survives a reload; gentle hand refresh (≥60% kept, ≤40% new) |
| `EX-GREET` | The door greeting in the visitor's language at their hour |
| `EX-GREET-LIVE` | The greeting re-speaks when the daypart changes |
| `EX-GREET-BAKE` | The baked string cache; the gen command; the fallback |
| `EX-LANG` | The corner language selector on the door |
| `EX-HANG` | The gallery: one work per viewport, caption in the margin |
| `EX-ACCENT` | The breathing ground and live accent |
| `EX-GLIDE` | One input → one centered frame — sine in-out, no drift; desktop animator, touch snap |
| `EX-CHROME` | One page shape for the browser on every face: the root overflow cut is retired as a lock; every standing face (the re-opened door included) rests input + hides the scrollbar gutter-stable, with a snap-back guard correcting any scroll the house did not write |
| `EX-SHARE-BTN` | The floating share button (fixed chrome): copies the in-view work's room permalink, never navigates |
| `EX-SHARE-IN` | The permalink arrival: `#w-<id>` as a handed-over pick |
| `EX-SHARE` | The share feature as a whole |
| `EX-SOUND` | The ambient loop: off by default, lazy fetch, credit from config |
| `EX-SOUND-PAUSE` | Pause holds the moment; resume continues from it |
| `EX-PROTECT` | The gracious deterrent (desktop right-click → gift ceremony; drag/touch → gift toast; pinch → silent refuse) |
| `EX-PROTECT-GIFT` | The gift ceremony: the picture is offered on a solemn card, handed over only on a yes |
| `EX-PROTECT-RES` | The clean shown image; the site-host mark rides only a taken copy (client canvas / prize / capped serve) |
| `EX-QUIZ` | The work's public four-option question + plaque chip (placement config knob; one per show) |
| `EX-QUIZ-EDGE` | The tapped option judged at the edge against the single private answer; own attempt fence; never a served byte, never a model call |
| `EX-QUIZ-PRIZE` | The prize is a marked gallery derivative; the master never ships |
| `EX-QUIZ-ONCE` | Exactly one question per show, over the reachable∧unanswered set, silenced by a cooldown window |
| `EX-QUIZ-GLINT` | A soft one-time light sweeps the chip as the question appears; only the chip; off under reduced-motion |
| `EX-QUIZ-AB` | `quiz_arm` (on/control, 50/50, session-stable) rides the existing walk beats as a dimension; null when the flag is off |
| `EX-QUIZ-FLOW` | `quiz_stage` (shown → opened → won\|lost → gift) rides the same two beats as a running-max dimension; never a sixth beat; the stage wipes with the walk |
| `EX-LADDER` | The responsive 640/960/1280 image ladder: a phone pulls light, a wide/retina screen sharp; base is the fallback |
| `EX-LOAD` | The loading breath: solemn hairline while pixels travel; a cold-arrival line before the walk is live (instance text) |
| `EX-LOAD-2` | The in-flight ladder: black → the work's own tone-plate (past the grace) → plate+bar (past the long wait) → the photo fades in over it, crisp when it beat the plate, graceful when it stood; the arm reads the settled state and arms once; supersedes the lone breath hairline. Runs at two call-sites — the walk's in-view frame (one reused overlay) and the door's five windows (a plate per window, no walk marks, no preload); the crossing and side room stay outside |
| `EX-LOAD-3` | The one-ahead preload: the next work in the direction of travel is warmed at the device tier while a work rests — exactly `preload_ahead` (1), never the arc; best-effort, silent, cancelled and re-aimed on a turn or `#w-` jump |
| `EX-SERIES` | The series side room: pill, crossing, lane / polaroids, honest close |
| `EX-STORY` | The told story: one line per work, leaned by light, degrades to silence |
| `EX-STORY-ORDER` | The light-lean: kinship + hour-discontinuity over time-of-day marks |
| `EX-STORY-LINE` | Each line's laws: ≤12 words, associative, note-grounded, no technique |
| `EX-STORY-EDGE` | The voice at the edge: `/api/story`, private fragments, KV cache |
| `EX-STORY-AB` | `story_variant` rides the GA beats as a dimension |
| `EX-I18N` | The any-language layer: one deferred fetch per new locale, KV-cached |
| `EX-EDGE-GUARD` | Three money fences before any model call |
| `EX-MEMORY` | The coat-check token: seen-work ids at the edge, anonymous |
| `EX-PULSE` | The event registry: eleven beats on the GA wire, held both ways by a standing test |
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
| `INV-56` | The shown image is clean; the site-host mark rides only a taken copy (client canvas on grab, baked on the prize, baked when the serve is capped). Mark text is the config host, never a literal |
| `INV-59` | The quiz answer is judged at the edge against a private accept-set — never a served byte, never a model call; normalization is hard (NFKC-fold, lower-case, letters only) and parity-by-construction (the client sends the raw answer); its own per-IP hourly attempt fence, separate from the model rate-limit and day budget, degrades gracefully to unlimited when no KV is bound so a preview/local deploy still judges |
| `INV-60` | The quiz flag off is byte-identical to a quiz-less walk; on / no answer / unknown id degrades to silence, the walk loses nothing |
| `INV-63` | The responsive image ladder: the display-cap bake writes clean 640/960/1280 tiers next to each served image (downscale-only, no mark on a served tier); the walk img offers them via a per-work `srcset` + `sizes`, the base `src` the untouched fallback; joins only when the cap runs, else byte-identical |
| `INV-64` | The quiz is a four-option guess: prompt + four option labels public, the ONE correct answer + prize private in `_worker.js`; the tapped option judged at the edge (never a served byte, never a model call); one tap locks |
| `INV-65` | A miss shows one localized line then the card fades, leaving the photograph; a hit shows a localized praise line then the gift ceremony; the card sits over the visible photo (light scrim), tints to the work, mirrors the active locale's `dir` |
| `INV-66` | Exactly one question per show — the chip placed on one work chosen per walk over the reachable∧unanswered set — and silenced while less than the cooldown window (`quiz_cooldown_hours`, ~6h) has passed since a show that asked; `quiz_probability` retired |
| `INV-62` | The quiz A/B arm (`quiz_arm`: on/control, 50/50, session-stable off the visitor token) rides the existing `walk_unfold`/`walk_exit` beats as a dimension; null when the flag is off so the payload stays byte-for-byte today's |
| `INV-67` | Faces-meet composition law: a standing face (quiz card, gift card, side room) owns the walk's input; the last face leaving discharges an instant re-centre to the live viewport; the card is viewport-honest; the closing screen is a stop |
| `INV-68` | Dead model account: a non-429 4xx flags the hour in KV; behind the flag i18n serves baked English with a plain hello uncached under the asked locale; story is silence; nothing further charged |
| `INV-69` | The quiz funnel stage (`quiz_stage`: shown → opened → won\|lost → gift) is session-scoped and runs monotonically upward — it never lowers; "gift" advances only from "won"; the stage rides `walk_unfold`/`walk_exit` as a dimension alongside the arm (no sixth beat, INV-41 stands); the stage wipes with the walk (?reset); control and flag-off visitors carry no stage |
| `INV-70` | One page shape for the browser on every face: every standing face (the re-opened door, side room, question card, gift card) locks the walk by resting input plus a snap-back guard that corrects any scroll the house did not write (the ceremony glide, Back restore, and face-leave re-centre all pass), while the root scrollbar hides gutter-stable (no reflow) and the walk's own tall document stays in place beneath; the root overflow cut is retired as a locking device; a later face inherits the law by construction |
| `INV-72` | The in-flight ladder: a walk frame whose pixels are late wears the work's RAW baked `dom` tone (a plate) past `load_plate_grace`, a wordless bar (no digit, no percentage — INV-1) joins past `load_bar_wait`, and the photo fades in OVER the plate — `load_reveal_fast` when it beat the plate, `load_reveal` when the plate stood; the arm reads the already-settled state (`complete`/`naturalWidth`, the errored case) and resolves synchronously (warm ⇒ reveal at once, no plate/clock; pre-errored ⇒ retire, caption+counter hold), arming ONCE per frame-taking-view so a post-reveal tier swap never re-plates; ONE reused overlay for the single in-view frame; every duration a beat ×tempo (INV-33) and `load_plate_grace` < `load_bar_wait` clamped at boot; runs at a SECOND call-site — the door's five windows (`EX-DOOR-2c`), each its own `.exd-plate` (five may fly at once, never the walk's single overlay), reading the settled state so a cached window / relayout re-render / fresh full-circle deal re-flashes no plate, the window's entrance and `liveAccent` halo standing while the plate speaks the raw `dom`; the door emits no walk marks and does not preload; the crossing and the side room stay outside — the ladder governs the walk's in-view frame and the door windows only and continues behind any standing face; supersedes EX-LOAD/INV-37's lone hairline, its promises re-carried whole |
| `INV-73` | The one-ahead preload: while a work rests in view the NEXT work in the current direction of travel is fetched at the device tier (the walk's own `srcset`/`sizes`, INV-63) — exactly `preload_ahead` (default 1) ahead, never the arc (INV-25/INV-30); best-effort and silent (a failed preload surfaces nothing and the in-view ladder still catches the step), abandoned cleanly on a turn or `#w-` jump and re-aimed to the new direction of travel; client-only, no bake output, no worker, no flag |
| `INV-71` | The full circle retires the hand: once every work of the standing walk's current hang (`order.slice(0, shown)`, spread + unfolds) has stood in view — counted the moment the mark is made, in-session marks joined with the persisted seen copy — the next door render (the exit control, a browser-Back onto the door, or a returned-door reload, all alike) retires the standing hand and deals a fresh `EX-DOOR-3` hand; the consumed circle (pick + shown) rides the versioned `ex.hand` so one circle earns exactly one deal (door↔walk never re-rolls, a new pick or a post-circle unfold reopens the count); an unconsumed circle outranks the reload refresh once, then the reload law resumes; a circle-less older hand reads as no circle consumed and a stale-versioned hand drops whole (`INV-26`); on this one point `INV-32a`'s as-it-stood yields; short of a circle the standing-set law (`INV-16`/`EX-DOOR-2d`) holds |
| `INV-74` | The diverse door keeps a browser-local, versioned, `?reset`-forgettable memory of the works it has DEALT, and every open guarantees at least `fresh_min` of the windows dealt for the current fit are works not dealt since the last round reset — jointly with the place fraction, so at least `⌈fresh_min·n⌉+⌈place_min·n⌉−n` shown windows are both unseen and place; when the unseen pool cannot supply the fresh floor or that overlap the memory clears and a new round begins, the just-dealt set replacing it (a normal open unions in). This novelty floor supersedes the curated door's ⌊door_size/3⌋-repeat law (`INV-20`) here |

### Reconciliation log — how each behavior above landed in code

These are places where the engine's code diverged from the behavior specified above, and how each
divergence was closed. Most rows record a feature proven first on a live instance and then generalized
into the engine; each cites the engine commit that landed it.

| Code | Description |
|------|-------------|
| `⟨DELTA-1⟩` | **RESOLVED** — `build.py` writes `site_name` from `site_config` into `config.json`; `exhibition.js` reads `cfg.site_name` via `textContent` (no literal). `test_site.py` asserts both. |
| `⟨DELTA-2⟩` | **RESOLVED** — `engine/build.py` gains `_stamp`, `_copy_assets_capped`, updated `copy_gallery(display_max, mark_text)`, `build(display_max)`, and `--display-max` CLI arg. Mark text is `site_url`-derived (no instance literal). `test_site.py` asserts INV-56 (pinned skip when Pillow absent). |
| `⟨DELTA-3⟩` | No `dateCreated` in the work-page JSON-LD `VisualArtwork` record. The engine's generic Work entity has no date field in `gallery_data.json`; an instance may extend the content contract to add one. |
| `⟨DELTA-4⟩` | **RESOLVED** — `series_open` now carries the work whose series opened and stands as a full registry line (no longer an engine-native afterthought); the two-way registry guard (`⟨DELTA-12⟩`) makes any future beat/spec drift red. |
| `⟨DELTA-5⟩` | The `sold` flag and its red dot in the caption zone are implemented in `exhibition.js` but the bake does not forward the `sold` field from `gallery_data.json` items into `exhibition_data.json`. The red dot is currently always hidden. Reconcile: add `"sold": bool(it.get("sold"))` to `ex_works` in `build.py`. |
| `⟨DELTA-6⟩` | **RESOLVED** — the quiz (`EX-QUIZ`/`INV-59`/`INV-60`), the gift ceremony (`EX-PROTECT-GIFT`), and the client-side mark-split on take (`EX-PROTECT-RES`/`INV-56`) are ported and generalized: quiz data is an instance-supplied `<content>/quiz.json`, placement + probability are `exhibition.quiz` config knobs, the download filename is a slug of the config `site_name`, and the mark text is the config host — no work id, host, or brand literal in the engine. `test_quiz.py` (11 rows) + updated `test_protect.py` assert them. |
| `⟨DELTA-7⟩` | **DEFERRED (minor)** — the quiz *prompt* localization (an instance's `quizzes` block in its `i18n_source.json` + the worker's `translate` merge) is not ported; the public prompt ships in the base language only. The chip label (`quiz_ask`) IS localized. Low value until an instance needs translated prompts; the mechanism is a small additive follow-on. |
| `⟨DELTA-8⟩` | **RESOLVED** — a quiz+door fix batch proven on a live instance (2026-07-08), generic parts ported: (1) the `/api/quiz` attempt fence degrades gracefully when no KV is bound (`overQuizRate` returns unlimited instead of throwing — preview/local judges); (2) `normAnswer` NFKC-folds + lower-cases + keeps letters only, with the client sending the raw answer (parity by construction); (3) all quiz+gift chrome (`quiz_submit`, `quiz_wrong`, `gift_ask`/`gift_yes`/`gift_no`/`gift_buy`) joins the localized string set (worker `shape`/`validate` + `i18n_source`) with English client fallbacks; (4) a wrong answer shows one localized line then closes (~1s), no hint trail; (5) reopening resets the card; (6) the card's accent is the focused work's live tint. `test_quiz.py` asserts them. The door-variety + load-flash-banner deltas are instance-surface-specific and were NOT ported (no clean generic equivalent). |
| `⟨DELTA-9⟩` | **RESOLVED** — the quiz funnel (`EX-QUIZ-FLOW`/`INV-69`) and A/B arm dimension (`EX-QUIZ-AB`/`INV-62`) ported: `quiz_arm` and `quiz_stage` ride the existing `walk_unfold`/`walk_exit` beats; `quizStageUp` is session-scoped and monotone; the stage wipes with `?reset`; `openGift` accepts an optional `onYes` callback so the quiz-win path stamps "gift" without touching the shared ceremony. Engine storage key: `ex.quizstage` (dot convention). `test_quiz_flow.py` (4 browser rows FL1–FL4; FL5–FL6 omitted — engine carries no `ga_report.py`) asserts them. |
| `⟨DELTA-10⟩` | **RESOLVED** — one page shape for the browser (`EX-CHROME`/`INV-70`, landed in engine commit `5a2d36a`): the root overflow cut is retired as a lock; `faceSync` mirrors any standing face onto `html.ex-face` (scrollbar-gutter stable, scrollbar hidden), rests keys/wheel/touch behind the face (EX-COMPOSE's own-scroll carve-out via `FACE_SEL`), and a `scroll` guard snaps back any scroll the house did not write, while the house's own writes re-freeze `guardHold`. The client already carried the `ex.*` / `ex-face` naming, so the js/css landed byte-parallel — no renames, no meaning drift. `test_compose.py` gains CH1–CH6. CH6 (the side room's lane scrolls native) pins **SKIP** in the synthetic fixture — its lane series has 3 members that fit the 1280px viewport, so the lane is not horizontally scrollable and the carve-out is untestable here; it exercises on real content with a wider lane. **Follow-on (a touch-device field find; engine commit `d758b7d`):** a resting finger is NOT input rest — while a pointer/touch is DOWN the guard HOLDS (an active touch rubber-bands the page a few px; correcting mid-touch made the finger drag again next frame, a per-frame fight the visitor saw as the whole screen trembling) and settles ONCE on lift, without reopening the foreign-scroll snap-back (CH3) or the face's own native scroll (CH6). The EX-CHROME clause gains the input-REST sentence; `test_compose.py` gains **CH7** (guard-writes-during-hold → 0, one settle on lift). The engine carries no `TEST_MATRIX.md`/`docs/prover` — the matrix CH7 row and prover finding from this feature's derivation fold into the SPEC clause + the CH7 test here. |
| `⟨DELTA-11⟩` | **RESOLVED** — the full circle retires the hand (`EX-DOOR-4`/`INV-71`, landed in engine commit `b0954e9`): a walk whose whole hang has stood in view earns a fresh `EX-DOOR-3` deal on the next door render, with the four prover findings folded — an unconsumed circle wins once then the reload law resumes (F1), the exit control / browser-Back / returned-door reload behave alike and `INV-32a`'s as-it-stood yields (F2), the circle counts marks the moment they are made via an in-session `walkSeen` set written synchronously in the intersection callback so the debounced flush never delays it (F3), and a circle-less older hand reads as no circle consumed while a stale-versioned hand drops whole (F4). The consumed circle (pick + shown) rides the versioned `ex.hand` record so one circle earns one deal. The client already carried the `ex.*` / `__exSeen` naming, so the js port reduced to prefix renames onto the engine convention (`ex.hand`, `ex.seenc`). `test_door.py` gains rows 25–29 (all red-first vs HEAD). |
| `⟨DELTA-13⟩` | **RESOLVED** — the in-flight ladder + the one-ahead preload (`EX-LOAD-2`/`INV-72`, `EX-LOAD-3`/`INV-73`, landed in engine commit `59a11a1`): the lone loading-breath hairline grows to black → the work's raw `dom` tone-plate → plate+bar → accelerated reveal, armed from the same in-view IntersectionObserver that grounds the tone (`arm()` reads the settled state — F1 — and arms once — F6), and the next work preloads one-ahead along the direction of travel (`preloadAhead`/`travelDir`, cancelled + re-aimed on a turn/`#w-` — F5). Five knobs join `config.exhibition` (`load_plate_grace` .35 / `load_bar_wait` 1.5 / `load_reveal` 2.0 / `load_reveal_fast` .6 / `preload_ahead` 1), all client-fallback-guarded; the client clamps `load_plate_grace` < `load_bar_wait` at boot (F7). No bake output — works already carry `dom` and `srcset`. The client already carried the `ex.*` / `ex:*` / `__exSeen` naming, so the port reduced to prefix renames onto the engine convention (`ex:plate`, `__exPreload`). `test_ladder.py` is new (15 rows, 14 browser + 1 traceability — 8 red-first vs HEAD); `test_load.py`'s three EX-LOAD browser rows swing breath→plate (1 red-first); `tests/headless.py` gains a network-log road (`net_capture`/`net_log`/`net_clear`) for the preload. All 15 ladder rows pin **SKIP** when Pillow is absent (the tier bake the composition row needs). |
| `⟨DELTA-12⟩` | **RESOLVED** — every registry beat now on the wire (`EX-PULSE`/`INV-41`, landed in engine commit `6f29d51`): `pulse()` gains a third `extra` arg for a closed-ladder word; `gift_download` fires from `giftDownload` on both kinds (`quiz_prize` when preMarked, `grab` on a right-click) carrying the work id (threaded through `openGift`'s new `workId` arg + the contextmenu `fr.dataset.id`, the two quiz gift calls); `series_lift` on each polaroid LIFT (not set-down); `series_open` now carries `focusedId`; `lang_pick` at the door tongue pick (the baked code, or `other` for an outsider tongue — never a raw locale); and `walk_exit` also fires on a browser-Back leave (the `popstate` door branch, guarded by `wasWalk = !atDoor` so control (pushState) and history (popstate) never double-count). `test_pulse.py` is re-authored to 9 rows including a TWO-WAY registry guard (every code emitter names a registry beat AND every registry beat has a live emitter, portable via a first-arg `pulse()` parser). The guard exposed a pre-existing engine gap: `sound_on`/`sound_off` were emitted (EX-SOUND) but absent from the EX-PULSE table — the table now lists all **eleven** beats. **Deliberately narrower here:** the engine carries no read side (`ga_report.py`, `ga_register_dimensions.py`), so the "read side keeps pace" string row is omitted here — same convention as `⟨DELTA-9⟩`'s FL5/FL6. Six rows red-first vs HEAD. |
| `⟨DELTA-14⟩` | **RESOLVED** — a drag over a standing face no longer slides the room beneath it (`EX-CHROME`/`INV-70`, the layer above `⟨DELTA-10⟩`'s resting-finger follow-on, landed in engine commit `2a9d65b`): the face now EATS a moving finger AT THE SOURCE. The touchmove branch tracks the gesture (`fX`/`fY`/`fDecided`), picks a verdict ONCE on the first ~4px, and holds it to the lift — the walk gets no page scroll unless the finger stands on a part of the face that truly scrolls along the drag's own axis, tested by `faceConsumes` (a genuinely-scrollable ancestor — inputs/textareas/contenteditable, or `scrollWidth`/`scrollHeight` past client+1 with `overflow` auto|scroll in the gesture's axis — stopping at `FACE_SEL`). The old carve-out narrows from «anywhere on a face» to those parts; the side-room lane gains `overscroll-behavior:contain` so a run-out never chains to the page; the snap-back guard demotes to the BACKSTOP for what source-eating cannot reach (a dragged desktop scrollbar, the rubber-band's leftover), its yield-while-held/settle-once-on-lift shape unchanged. The client already carried the `FACE_SEL` / guard naming, so the js/css landed with no renames or meaning drift. `test_compose.py` gains **CH8** (a slow real drag on the quiz scrim AND the side-room backdrop off the lane → zero page drift while held, no post-lift jerk — red-first vs HEAD showed 285px slide behind both) and **CH9** (drag ALONG the lane scrolls the lane, drag ACROSS it moves neither). **CH9 pins SKIP in the synthetic fixture** at every honest viewport (its 3-member lane series does not overflow even at 390px — `sw==cw`), so the along-precondition never arms and the across-half is untestable here — same standing condition as CH6; it exercises on real content with a wider lane. The engine carries no `TEST_MATRIX.md`/`docs/prover` — the two matrix rows and prover findings from this feature's derivation (F1 decide-once, F2 overscroll-contain, F3 facets, F4 sound-chrome-by-class, F5–F8 unchanged fences) fold into the SPEC clause + the CH8/CH9 tests here. |
| `⟨DELTA-15⟩` | **RESOLVED** — the door's five windows ride the walk's in-flight tone-plate ladder (`EX-LOAD-2`/`INV-72` at a second call-site, `EX-DOOR-2c`, landed in engine commit `a43ff3a`): a window whose baked derivative is late wears the work's OWN raw `dom` as a plate inside the window, adds the same wordless bar past the same long wait, and fades the photo in over the plate on arrival — the same knobs, none added. The walk's in-flight core is factored into one `ladderFlight` helper reused by the walk (its single `#ex-plate`) and the door (a `.exd-plate` PER window, five at once) — one implementation of the timings/classes, never a second copy of the knobs; `armClear` clears the timer list in place (`.length = 0`) so the factored closure keeps its reference. `doorArm` reads the SETTLED STATE the way the walk's arm does (`img.complete` — the crux, the settled-read seam its prover pass flagged): a cached window reveals at once with no plate, so a relayout re-render (`EX-DOOR-2b`) or a fresh full-circle deal (`EX-DOOR-4`) re-flashes none; the door emits no walk marks (off the counter) and does not preload (`EX-LOAD-3` stays the walk's). CSS: a door-scoped `.exd-plate` (inset, behind the photo which gains `z-index:1`), the shared `.ex-bar` rules generalized (`#ex-plate .ex-bar, .exd-plate .ex-bar`), the bar's tint taking `var(--glow, var(--accent,…))` so a window's bar rides its own halo colour. The crossing (`EX-DOOR-2e`) and the side room stay outside the ladder — the boundary moved from «the door keeps its own image handling» to «the door windows ride it», reconciled in the `EX-LOAD-2` clause, the `EX-DOOR-2c` pointer, and the `INV-72` line. `test_ladder.py` gains **DL1** (a slow window ⇒ raw-`dom` plate + wordless bar; a fast window ⇒ no plate) and **DL2** (the entrance + `liveAccent` halo compose with the plate; a cached re-render re-flashes no plate) — both red-first vs HEAD (no `.exd-plate` machinery). The engine carries no `ARCHITECTURE.md`/`TEST_MATRIX.md`/`docs/prover` — the boundary-doc, two matrix rows, and prover cross-link from this feature's derivation (the F1/F6 settled-read and re-render seam) fold into the SPEC clause + DL1/DL2 here. No pinned skip needed: the synthetic fixture's door pool works carry real `dom` tones (Pillow present), so both DL halves arm honestly. |
| `⟨DELTA-16⟩` | **RESOLVED** — the told story: a plot per opened portion, read lines never shift (`EX-STORY`/`INV-47`, landed in engine commit `8392e8d`): `tellStory` now works PER PORTION — the cold first spread, then each «ещё N» — instead of over the grown `0..shown` set. `storyPortions(n)` cuts the order into the unfolding's own portions; `askPortion(lo,hi)` asks `/api/story` for that portion's OWN ordered slice under its own cache key. The old single `storyKey`/`storyGen` pair is replaced by two sets, `toldPortions` (stamped ONLY once a plot has come back — a served answer) and `askingPortions` (in-flight, never double-asked): a refused or failed portion leaves its key UN-stamped, so it stays OWED and is re-asked at the next natural beat — a further unfold, or a return to the walk (a `tellStory()` call added to the popstate return-to-walk branch). Because each request names only its own works, a line already read is never re-requested and never shifts; because the told-key is stamped on a served plot alone, the earlier felt «open more» bug (the key burned before the fetch, the portion silent forever) is closed. `storyReset()` (called at a fresh door pick, beside `shown = SPREAD`) clears the sets + lines so no portion leaks across picks. Verified behaviour of the engine's generic client: a mid-visit language switch keeps already-told lines in their first tongue — `respeak()` re-labels chrome only and never touches `STORYLINES` or re-asks — while a portion opened after the switch reads `viewerLang()` live and gets the new tongue; no `«part N»` naming rides any surface. The engine carries no `TEST_MATRIX.md`/`docs/prover` — the four portion matrix rows + the four prover clarifications from this feature's derivation (X2 the client re-asks freely while the server fence carries the wait; X4 the cold spread is itself the first portion; X5 the language-switch behaviour; X6 the cache key is each portion's ordered slice) fold into the `EX-STORY` clause + the tests here. **Deliberately narrower here:** the engine had NO client-voice story suite (its story tests were the worker-edge `test_dead` + a `test_exhibition` byte-check), so the suite rows accompanying this feature are adapted to the synthetic fixture and folded into `test_exhibition.py` (the suite that already owns the `EX-STORY` client byte-row) rather than a new suite — the suite count stays 27. Five portion rows: the no-`«part N»` lint is a model-free ratchet (green both ways); the follow-on-scoped-ask + no-re-ask + refused-portion-recovery rows are **red-first vs HEAD** (pre-fix sent the grown 15-id set, re-asked the read ids, and burned the key on the 404 → silent forever); the return-re-shows-byte-identical row is a standing behaviour row (green both ways). No pinned skip: the fixture's 24-work pool overflows the 10-spread, so «ещё N» arms honestly. |
