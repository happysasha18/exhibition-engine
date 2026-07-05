# gallery-engine

A static gallery-site builder and adaptive-exhibition renderer, extracted from the
private tlvphoto instance.

## What it is

gallery-engine produces a fully self-contained static site bundle from precomputed
image data. The bundle has two faces on the same URL:

- A **crawlable static face**: real HTML with a heading, an indexable description,
  and a grid linking every work to its own page — readable with JavaScript off,
  indexed by search engines.
- A **client-side exhibition walk**: `exhibition.js` re-renders the page into a
  kinship walk after page load. A visitor taps any image and the exhibition
  reassembles itself into an arc of related works. Works are related by
  min-max-normalized feature vectors computed from the content's `vector.json`.

Additional mechanics:
- **Threshold door** (EX-DOOR): a small pool of works greets the first visit;
  tapping one starts the walk. The pool is baked into `exhibition_data.json`.
- **Unfold cap**: "open more" appends works along the current arc in steps, retiring
  after a configurable number of unfolds. The arc ends cleanly.
- **Door-gallery loop**: the door and the gallery share the same walk engine; the door
  is just the pre-tap state.
- All feel-knobs (spread size, row size, cold-spread strategy, arc shape, transition
  timing, kinship axes, unfold step, max unfolds, door size) live in `config.json`
  in the bundle — tunable without a rebuild.

The FOUC guard ensures the static face never flashes when JavaScript is available:
an inline script marks the page as JS-alive before `<body>` parses, so CSS hides
the static grid pre-paint. A 2.5s fallback restores the static face if the walk
does not come alive (broken/missing JS or data).

## Content contract

A content directory must provide these files:

```
gallery/gallery_data.json     list of work objects — items array
gallery/door_candidates.json  (optional) ordered list of door-pool candidates
gallery/assets/<section>/     image files referenced by gallery_data.json
gallery/shared/               design tokens (tokens.css, etc.)
vector.json                   per-work feature axes
content_tags.json             per-work subject captions
instance-assets/              favicon.svg, favicon.png, apple-touch-icon.png
```

Schemas (one-line):

- `gallery_data.json` items: `id` (str) · `img` (relative path under gallery/) ·
  `title` (str, may be empty) · `section` (str) · `city` (str, optional) ·
  `country` (str, optional) · `w` (int) · `h` (int) · `dom` (dominant RGB triple,
  optional)
- `vector.json` items: `id` (str) · `axes` dict of `{name: {value, source, confidence}}`
  where value is numeric for any axis that drives kinship
- `content_tags.json` items: `id` (str) · `subject` (str caption)
- `door_candidates.json` items: `id` (str) · `img` (str, informational only — the
  engine re-resolves from gallery_data)
- `instance-assets/`: `favicon.svg`, `favicon.png`, `apple-touch-icon.png` — provided
  by the site operator; the engine copies them to the bundle root

## Site contract

A `site.json` file provides the five instance-specific identity keys:

```json
{
  "site_name":        "my-gallery",
  "creator":          "Photographer Name",
  "root_title":       "my-gallery — Photographer Name",
  "root_description": "A personal, ever-changing exhibition ...",
  "collection_name":  "my-gallery — the exhibition"
}
```

These values flow into `<title>`, `<meta description>`, `og:site_name`,
`og:title`, JSON-LD `WebSite.name`, `CollectionPage.name`, and the `<h1>`.

## How to bake

```sh
python3 engine/build.py \
    --content /path/to/content \
    --site /path/to/site.json \
    --out /path/to/output \
    --site-url https://example.com \
    --ga-id G-XXXXXXXXXX
```

Instance assets (favicons) are looked up first in `<content>/instance-assets/`;
if that directory is absent, pass `--instance-assets <dir>` as a fallback:

```sh
python3 engine/build.py \
    --content ~/tlvphoto \
    --site example/site.json \
    --out /tmp/site \
    --site-url https://tlvphotos.com \
    --ga-id G-00J4KGDHCG \
    --instance-assets ~/tlvphoto/assets_src
```

The builder requires only the Python standard library — no `pip install`.

## Tests

No engine-local test suite yet. The private tlvphoto instance has a 75-test suite
(string-level + headless-Chrome browser tests via `engine/harness/headless.py`) that
covers the shipped behaviour. An engine-local suite is the next movement before any
public release.

## Provenance

Extracted 2026-07-06 from the private tlvphoto instance. Bake proven byte-identical:
`diff -r <ref-bake> <engine-bake>` returned empty against the reference output of the
original `build_site.py` on the same content and flags.
