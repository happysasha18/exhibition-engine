# exhibition-engine

A static gallery-site builder and adaptive-exhibition renderer.

exhibition-engine turns a directory of precomputed image data into one self-contained static website bundle. You can deploy the bundle anywhere. The builder uses only the Python 3 standard library. It needs no `pip install`.

The bundle serves two faces on the same URL. The first face is a crawlable static site: real HTML with a heading, an indexable meta description, and a grid that links every work to its own page. This face is readable with JavaScript turned off and can be indexed by search engines. The second face is a client-side exhibition walk. A script called `exhibition.js` re-renders the page into an interactive walk after the page loads. A visitor taps any image and the page reassembles into an arc of related works. Works are related by min-max-normalized feature vectors read from the content's `vector.json`.

This tool is for you if you have a curated set of images with precomputed per-work feature vectors, and you want a self-contained, deployable, search-indexable exhibition site with an adaptive walk.

To start, see the requirements and the real example run below.

## When to use it, and when it does not apply

Use exhibition-engine when you already have a curated image set and precomputed per-work feature vectors, and you need a deployable, search-indexable site with an adaptive browsing experience.

The engine consumes precomputed content. It does not compute feature vectors. It does not curate the image set. It does not manage a photo archive. Those steps happen upstream and produce the content directory that the engine reads.

## Requirements and install

The builder requires Python 3. There is no package to install; the builder relies only on the Python 3 standard library.

The test suite requires an additional virtual environment that includes Pillow.

There is no separate install step for the builder itself. Clone the repository and run the build command.

## Real example run

The repository ships a synthetic example. `tests/fixture_content/` is a complete synthetic content directory. `example/site.json` is a synthetic site identity file. The command below is the honest example run against that fixture data.

Command:

```
python3 engine/build.py \
    --content tests/fixture_content \
    --site example/site.json \
    --out /tmp/site \
    --site-url https://example.com \
    --ga-id G-XXXXXXXXXX
```

Output:

```
baked 24 work pages + exhibition root → /tmp/site
site_url=https://example.com  robots=ALLOW (prod)
```

The command exits with status 0. The output bundle at `/tmp/site` contains:

- `index.html`
- `config.json`
- `exhibition_data.json`
- `exhibition.js`
- `exhibition.css`
- `sitemap.xml`
- `robots.txt`
- the favicon files
- a `gallery/` directory
- an `api/` directory
- one page per work under `w/`

## Command-line flags

| Flag | Required | Description |
|---|---|---|
| `--content` | yes | Path to the content directory. |
| `--site` | yes | Path to the `site.json` identity file. |
| `--out` | yes | Path to the output bundle directory. |
| `--site-url` | yes | The canonical site URL. |
| `--ga-id` | no | A Google Analytics measurement id. Defaults to empty, which means no analytics tag is added. |
| `--enable NAME` | no, repeatable | Turns on an optional feature. Known names include `ai_i18n`, `visitor_memory`, `ai_story`, and `quiz`. |
| `--instance-assets DIR` | no | A fallback directory for the favicon set. |
| `--display-max N` | no | An integer cap on the displayed image size. |

## Content contract

The content directory passed to `--content` must provide the following files and folders:

```
gallery/gallery_data.json     list of work objects (items array)
gallery/door_candidates.json  (optional) ordered list of door-pool candidates
gallery/assets/<section>/     image files referenced by gallery_data.json
gallery/shared/               design tokens (tokens.css and similar)
vector.json                   per-work feature axes
content_tags.json             per-work subject captions
instance-assets/              favicon.svg, favicon.png, apple-touch-icon.png
```

Field reference for each file:

**`gallery_data.json` items**
- `id` (string)
- `img` (relative path under `gallery/`)
- `title` (string, may be empty)
- `section` (string)
- `city` (string, optional)
- `country` (string, optional)
- `w` (int)
- `h` (int)
- `dom` (dominant RGB triple, optional)

**`vector.json` items**
- `id` (string)
- `axes` (a dict of `{name: {value, source, confidence}}`; `value` is numeric for any axis that drives kinship)

**`content_tags.json` items**
- `id` (string)
- `subject` (string caption)

**`door_candidates.json` items**
- `id` (string)
- `img` (string, informational only; the engine re-resolves the image from `gallery_data.json`)

**`instance-assets/`**
- `favicon.svg`, `favicon.png`, `apple-touch-icon.png`, provided by the site operator. The engine copies these files to the bundle root.

## Site contract

`site.json` provides the site's identity values:

```json
{
  "site_name":        "MERIDIAN GALLERY",
  "creator":          "Jordan Rivera",
  "root_title":       "MERIDIAN GALLERY — Jordan Rivera",
  "root_description": "A personal, ever-changing exhibition ...",
  "collection_name":  "MERIDIAN GALLERY — the exhibition",
  "loading_line":     "a personalized photography exhibition"
}
```

These values flow into the page title, the meta description, `og:site_name`, `og:title`, the JSON-LD `WebSite.name` and `CollectionPage.name`, and the H1 heading.

## The instance-override model

One generic engine drives many sites. Each site is defined by three inputs.

First, a content directory holds the images and the precomputed data. Second, a `site.json` file holds the identity strings. Third, an optional instance asset override lets a site ship its own look.

The engine looks for the favicon set first in the content directory's `instance-assets/` folder. If that folder is absent, the engine falls back to the directory passed with `--instance-assets`.

The client assets, `exhibition.js`, `exhibition.css`, and the worker template, are taken from the instance's asset directory when present. Otherwise the engine serves its own generic client.

To stand up a new site, supply a content directory and a `site.json` file. You can optionally override the client assets and the favicon set.

## Additional mechanics

**Threshold door.** A small pool of works greets the first visit. Tapping one starts the walk. This pool is baked into `exhibition_data.json`.

**Unfold cap.** An "open more" control appends more works along the current arc, in steps. This control retires after a configurable number of unfolds, so the arc ends cleanly.

**Door-gallery loop.** The door and the gallery share the same walk engine. The door is the pre-tap state of that engine.

**Feel knobs.** Spread size, row size, cold-spread strategy, arc shape, transition timing, kinship axes, unfold step, maximum unfolds, and door size all live in `config.json` inside the bundle. You can tune these values without rebuilding the site.

**FOUC guard.** An inline script marks the page as JavaScript-alive before the body parses, so CSS hides the static grid before it paints. If the walk does not come alive within 2.5 seconds, for example because of broken or missing JavaScript or data, the static face is restored.

## Running the tests

```
.venv/bin/python tests/run_all.py
```

The suite runs 25 suites. It combines string-level checks with headless-Chrome browser tests driven by `engine/harness/headless.py`. All 25 suites currently pass.

## Provenance

The engine was extracted from a private production instance. Its bake was proven byte-identical against the reference implementation's output, using the same content directory and the same flags.

## License

No license is declared yet.
