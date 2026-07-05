#!/usr/bin/env python3
"""gallery-engine static bake — generic builder that regenerates a deployable site bundle
from precomputed content data and a site.json instance config.

Reads only precomputed artifacts — no AI, no heavy compute:
  <content>/gallery/gallery_data.json  the AUTHORITATIVE work set (id, img, title, section, place, size)
  <content>/vector.json                axes['AX-6_palette'].value  → the palette swatches
  <content>/content_tags.json          id → subject (caption), tags
  <content>/gallery/door_candidates.json  (optional) door pool provenance

Emits <out>/ (self-contained static):
  index.html                 the adaptive EXHIBITION root (EX) — crawlable JS-off face + live walk
  exhibition.js  .css        the client walk + its converged-gallery styling
  exhibition_data.json       per-work normalized feature vectors (neutral coords, no axis names)
  w/<slug>-<idtail>.html     one crawlable work page each
  sitemap.xml  robots.txt    exhibition root + every work page
  config.json                feature flags (AI OFF) + the exhibition feel-knobs (A/B) + site_url
  api/.gitkeep               reserved empty namespace for later serverless AI
  gallery/                   shared images + design tokens (copied)

Deterministic: same inputs → same bytes. The visible page never prints an axis readout;
the caption lives in <meta>/alt/JSON-LD only (caption_visible:false).

Usage:
  python engine/build.py \\
      --content ~/tlvphoto \\
      --site ~/gallery-engine/example/site.json \\
      --out /tmp/site \\
      --site-url https://tlvphotos.com \\
      --ga-id G-00J4KGDHCG

Instance assets (favicon.svg/png, apple-touch-icon.png) are looked up in:
  1. <content>/instance-assets/   (if present)
  2. --instance-assets <dir>       (if passed)
  (whichever is found first wins; both absent → skip, bundle has no favicons)

Extracted 2026-07-06 from the private tlvphoto instance; bake proven byte-identical.
"""
import argparse
import hashlib
import html
import json
import re
import shutil
from pathlib import Path

# Set by build() — module-level so helper functions can read them without threading a param
# through every call (mirrors the original structure exactly).
OUT = None              # type: Path
ROOT = None             # type: Path  — the content directory
CREATOR = ""
SITE_NAME = ""
ROOT_TITLE = ""         # site_name + " — " + creator (pre-composed for the exhibition <title>)
ROOT_DESCRIPTION = ""   # the root page description (instance-specific prose)
COLLECTION_NAME = ""    # name for the CollectionPage JSON-LD entry

DEFAULT_FLAGS = {
    "ai_greeting": False,     # canned greeting only; serverless Haiku swaps in later behind /api
    "ai_assemble": False,     # deterministic client-side kinship only
    "caption_visible": False, # the machine caption stays in meta/alt/JSON-LD, never visible
}


# ---------------------------------------------------------------- data helpers

def load_json(path):
    with open(ROOT / path, encoding="utf-8") as fh:
        return json.load(fh)


def slugify(text, maxwords=6):
    """ASCII slug; Hebrew/emoji/punctuation collapse away → '' so the caller falls back."""
    if not text:
        return ""
    t = re.sub(r"[^a-z0-9]+", "-", text.lower())
    t = re.sub(r"-+", "-", t).strip("-")
    if not t:
        return ""
    return "-".join(t.split("-")[:maxwords])


def id_tail(work_id):
    return hashlib.sha1(str(work_id).encode("utf-8")).hexdigest()[:4]


def work_slug(title, caption, work_id):
    base = slugify(title) or slugify(caption) or "photograph"
    return f"{base}-{id_tail(work_id)}"


def place_of(item):
    return " — ".join(p for p in (item.get("city"), item.get("country")) if p)


def indexable_title(item, caption):
    """The crawlable title — never empty: his title → caption → section+place → default."""
    if (item.get("title") or "").strip():
        return item["title"].strip()
    if caption.strip():
        return caption.strip()
    loc = place_of(item)
    if loc:
        return f"{item['section'].title()} — {loc}"
    return f"Photograph — {SITE_NAME}"


def visible_title(item):
    """The VISIBLE heading — his own title only; empty for title-less works (wordless ethos).
    When empty, the page ships a non-empty *visually-hidden* <h1> (see h1_title)."""
    return (item.get("title") or "").strip()


def h1_title(item):
    """The heading text — his title, else a quiet section+place label. NEVER the caption
    (caption_visible:false keeps the machine caption to meta/alt/JSON-LD only), so no machine
    prose ever reaches the page body, visible or hidden."""
    if (item.get("title") or "").strip():
        return item["title"].strip()
    loc = place_of(item)
    return f"{item['section'].title()} — {loc}" if loc else item["section"].title()


def palette_of(work_id, palettes, dom_fallback):
    cols = palettes.get(work_id)
    if not cols:
        cols = [dom_fallback] if dom_fallback else []
    return [tuple(int(c) for c in rgb) for rgb in cols]


def hexcolor(rgb):
    return "#%02x%02x%02x" % rgb


def esc(s):
    return html.escape(s or "", quote=True)


# ---------------------------------------------------------------- rendering

STYLE = """
*{box-sizing:border-box}
body{margin:0;background:#0d0d0f;color:#e9e9ee;font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}
a{color:inherit}
.visually-hidden{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}
.wrap{max-width:1100px;margin:0 auto;padding:clamp(20px,4vw,56px)}
.work{max-width:760px}
.work img{width:100%;height:auto;display:block;border-radius:4px;background:#161619}
.work h1{font-weight:500;font-size:clamp(20px,3vw,30px);margin:.9em 0 .3em}
.palette{display:flex;gap:0;height:34px;margin:1.1em 0;border-radius:4px;overflow:hidden}
.palette span{flex:1 1 0}
.meta{color:#9a9aa6;font-size:14px;margin-top:1.2em}
.enter{display:inline-block;margin-top:1.6em;padding:.6em 1.2em;border:1px solid #3a3a42;border-radius:999px;text-decoration:none;color:#cfcfda}
.enter:hover{border-color:#6a6a78}
.lede{color:#b9b9c4;font-size:clamp(16px,2.2vw,19px);max-width:640px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:12px;margin-top:2.4em}
.grid a{display:block;aspect-ratio:1;border-radius:4px;overflow:hidden;background:#161619}
.grid img{width:100%;height:100%;object-fit:cover;display:block}
.site-h1{font-weight:600;font-size:clamp(26px,5vw,44px);margin:0 0 .3em}
"""


GA_ID = ""   # set by build(ga_id=…) — empty ⇒ NO analytics tag anywhere (config, never hardcode)


def ga_snippet():
    if not GA_ID:
        return ""
    return (
        f'<script async src="https://www.googletagmanager.com/gtag/js?id={esc(GA_ID)}"></script>\n'
        "<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}"
        f"gtag('js',new Date());gtag('config','{esc(GA_ID)}');</script>\n"
    )


def head(title, description, canonical, og_image, og_type, jsonld, extra_og="", extra_head=""):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.png" type="image/png" sizes="64x64">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{esc(canonical)}">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{esc(canonical)}">
<meta property="og:image" content="{esc(og_image)}">
<meta property="og:image:alt" content="{esc(description)}">
{extra_og}<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(description)}">
<meta name="twitter:image" content="{esc(og_image)}">
<script type="application/ld+json">
{json.dumps(jsonld, ensure_ascii=False, indent=0, sort_keys=True)}
</script>
<style>{STYLE}</style>
{ga_snippet()}{extra_head}</head>
"""


def render_work(item, caption, palette, site_url):
    wid = item["id"]
    slug = work_slug(item.get("title", ""), caption, wid)
    canonical = f"{site_url}/w/{slug}.html"
    img_rel = f"/gallery/{item['img']}"          # gallery/assets/<section>/<id>.jpg → /gallery/assets/...
    og_image = f"{site_url}/gallery/{item['img']}"
    idx_title = indexable_title(item, caption)
    vis_title = visible_title(item)
    alt = caption or idx_title
    loc = place_of(item)

    jsonld = {
        "@context": "https://schema.org",
        "@type": "VisualArtwork",
        "name": idx_title,
        "image": og_image,
        "url": canonical,
        "creator": {"@type": "Person", "name": CREATOR},
        "copyrightHolder": {"@type": "Person", "name": CREATOR},
    }
    if caption:
        jsonld["description"] = caption
    if loc:
        jsonld["contentLocation"] = loc

    extra_og = (
        f'<meta property="og:image:width" content="{item.get("w","")}">\n'
        f'<meta property="og:image:height" content="{item.get("h","")}">\n'
    )

    # heading: his title visible; otherwise a non-empty visually-hidden h1 (crawler + a11y), page stays
    # wordless. The hidden h1 is a section+place label, never the caption (caption_visible:false).
    if vis_title:
        h1 = f'<h1>{esc(vis_title)}</h1>'
    else:
        h1 = f'<h1 class="visually-hidden">{esc(h1_title(item))}</h1>'

    swatches = "".join(
        f'<span style="background:{hexcolor(c)}"></span>' for c in palette
    )
    meta_bits = []
    if loc:
        meta_bits.append(esc(loc))
    meta = f'<p class="meta">{" · ".join(meta_bits)}</p>' if meta_bits else ""

    body = f"""<body>
<main class="wrap">
<article class="work">
<img src="{esc(img_rel)}" alt="{esc(alt)}" width="{item.get('w','')}" height="{item.get('h','')}">
{h1}
<div class="palette" aria-hidden="true">{swatches}</div>
{meta}
<a class="enter" href="/">Enter the exhibition &rarr;</a>
</article>
</main>
</body>
</html>
"""
    doc = head(idx_title, caption or idx_title, canonical, og_image, "article", jsonld, extra_og) + body
    return slug, doc


def exhibition_vectors(vector_items):
    """Per-work kinship vector for the client walk — deterministic.

    Every axis of vector.json that is numeric in ANY work becomes a coordinate (the radial family
    is null on non-radial images → treated as 0, a meaningful 'no radial structure'). Each coordinate
    is min-max normalized across the collection to [0,1] so no axis dominates by scale. The output uses
    a NEUTRAL key ('v') and bare coordinate arrays — no axis name, no labelled score ever reaches a
    file the visitor can read. Returns (vectors {id:[floats]}, version tag).
    """
    axes = sorted({k for it in vector_items for k, v in it["axes"].items()
                   if isinstance((v.get("value") if isinstance(v, dict) else v), (int, float))})
    raw = {}
    for it in vector_items:
        row = []
        for ax in axes:
            v = it["axes"].get(ax)
            val = v.get("value") if isinstance(v, dict) else v
            row.append(float(val) if isinstance(val, (int, float)) else 0.0)
        raw[it["id"]] = row
    n = len(axes)
    mins = [min(raw[i][j] for i in raw) for j in range(n)]
    maxs = [max(raw[i][j] for i in raw) for j in range(n)]
    vectors = {}
    for wid, row in raw.items():
        vectors[wid] = [round((row[j] - mins[j]) / (maxs[j] - mins[j]), 6) if maxs[j] > mins[j] else 0.0
                        for j in range(n)]
    # version changes whenever the axis SET changes → old localStorage arcs are discarded
    version = hashlib.sha1((",".join(axes)).encode("utf-8")).hexdigest()[:8]
    return vectors, version


def render_exhibition(items, captions, slugs, site_url):
    """The exhibition root `/` (EX). ONE surface, two faces: the served HTML is the crawlable
    JS-off face — a real heading, indexable intro about the COLLECTION (never a work's vector), and a
    static index linking every work to its /w/ page; `exhibition.js` then re-renders it into the live
    adaptive walk. Carries its own root og:image (a fixed representative work so a shared homepage link
    unfurls) + canonical + WebSite/CollectionPage JSON-LD."""
    canonical = f"{site_url}/"
    hero = items[0]                                   # deterministic representative work
    og_image = f"{site_url}/gallery/{hero['img']}"
    title = ROOT_TITLE
    desc = ROOT_DESCRIPTION
    jsonld = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "WebSite", "name": SITE_NAME, "url": canonical,
             "author": {"@type": "Person", "name": CREATOR}},
            {"@type": "CollectionPage", "name": COLLECTION_NAME, "url": canonical,
             "about": desc, "isPartOf": canonical,
             "creator": {"@type": "Person", "name": CREATOR}},
        ],
    }
    # The FOUC guard: with JS on, the crawler's static index must NEVER paint (Alexander saw all 121
    # works flash for seconds — evening review 2026-07-05). The inline script marks <html> as js-alive
    # BEFORE <body> parses, so CSS hides the static face pre-paint; if the walk hasn't come alive
    # within 2.5s (broken/missing JS or data), the mark is removed and the static face returns —
    # progressive enhancement keeps a bounded worst case, never a blank page.
    extra_head = ('<script>document.documentElement.classList.add("js");'
                  'setTimeout(function(){if(!document.body||!document.body.classList.contains("ex-live"))'
                  'document.documentElement.classList.remove("js")},2500);</script>\n'
                  '<link rel="stylesheet" href="/gallery/shared/tokens.css">\n'
                  '<link rel="stylesheet" href="/exhibition.css">\n')
    cards = []
    for it in items:
        cap = captions.get(it["id"], "")
        alt = cap or indexable_title(it, cap)
        cards.append(
            f'<a href="/w/{slugs[it["id"]]}.html"><img src="/gallery/{esc(it["img"])}" '
            f'alt="{esc(alt)}" loading="lazy"></a>'
        )
    grid = "".join(cards)
    body = f"""<body>
<div class="ex-head">
<h1 class="site-h1">{esc(SITE_NAME)}</h1>
<span class="ex-hint" id="ex-hint">an exhibition that assembles itself around you</span>
</div>
<div class="ex-stage" id="ex-stage"></div>
<div class="ex-more-wrap" id="ex-more-wrap">
<button class="ex-more" id="ex-more" type="button" hidden>open more &darr;</button>
</div>
<main class="wrap" id="ex-static">
<p class="lede">{esc(desc)}</p>
<nav class="grid" aria-label="All works">{grid}</nav>
</main>
<script src="/exhibition.js" defer></script>
</body>
</html>
"""
    return head(title, desc, canonical, og_image, "website", jsonld, extra_head=extra_head) + body


# ---------------------------------------------------------------- bundle

def copy_gallery(out_dir, content_dir):
    """Copy the shared images + design tokens into the bundle (self-contained). The old
    Room/Door prototypes are RETIRED — the exhibition (EX) is now the single converged front door,
    so no prototype HTML ships; only the assets and the shared tokens the exhibition renders in."""
    dst = out_dir / "gallery"
    src = content_dir / "gallery"
    (dst).mkdir(parents=True, exist_ok=True)
    if (src / "gallery_data.json").exists():
        shutil.copy2(src / "gallery_data.json", dst / "gallery_data.json")
    for sub in ("assets", "shared"):
        if (src / sub).exists():
            shutil.copytree(src / sub, dst / sub, dirs_exist_ok=True)


def copy_exhibition_assets(out_dir, engine_assets_dir, instance_assets_dir):
    """Copy the exhibition client (JS + CSS) to the bundle root, and instance assets.
    Kept as source files (not inlined) so they are lintable and cache-friendly; every feel-knob
    is read from config.json at runtime, not substituted at bake time."""
    for name in ("exhibition.js", "exhibition.css"):
        shutil.copy2(engine_assets_dir / name, out_dir / name)
    for name in ("favicon.svg", "favicon.png", "apple-touch-icon.png"):
        src = instance_assets_dir / name if instance_assets_dir else None
        if src and src.exists():
            shutil.copy2(src, out_dir / name)


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def door_pool(items_by_id, captions, content_dir):
    """The door pool (EX-DOOR): the door-candidates provenance ids intersected with the LIVING
    gallery works — an id that left the gallery silently drops out. Each entry carries the alt
    text a door work needs (his title → caption → quiet label; the door asks wordlessly, but a
    keyboard/screen-reader visitor still meets real words). Returns [] when the source is absent."""
    src = content_dir / "gallery" / "door_candidates.json"
    if not src.exists():
        return []
    pool = []
    for e in json.loads(src.read_text(encoding="utf-8")):
        item = items_by_id.get(e.get("id"))
        if not item:
            continue                                   # not a living work → drop (thin-pool degrade)
        cap = captions.get(item["id"], "")
        pool.append({"id": item["id"], "alt": indexable_title(item, cap)})
    return pool


def build(site_url, ga_id="", content_dir=None, out_dir=None,
          engine_assets_dir=None, instance_assets_dir=None, site_config=None):
    """Build the site bundle.

    Args:
        site_url: base URL (https://...) — used for canonicals, og:image, sitemap, robots
        ga_id: GA4 measurement id (G-…); empty = no analytics tag
        content_dir: Path to content directory (holds gallery/, vector.json, etc.)
        out_dir: Path to write the output bundle into
        engine_assets_dir: Path to engine/assets/ (holds exhibition.js, exhibition.css)
        instance_assets_dir: Path to instance assets dir (holds favicons)
        site_config: dict with keys: site_name, creator, root_title, root_description,
                     collection_name  (unused here — root_title/desc are derived from
                     site_name+creator exactly as the original did; collection_name goes into JSON-LD)
    """
    global GA_ID, OUT, ROOT, CREATOR, SITE_NAME, ROOT_TITLE, ROOT_DESCRIPTION, COLLECTION_NAME
    GA_ID = ga_id
    OUT = out_dir
    ROOT = content_dir

    # Instance identity from site.json
    SITE_NAME = site_config["site_name"]
    CREATOR = site_config["creator"]
    ROOT_TITLE = site_config["root_title"]
    ROOT_DESCRIPTION = site_config["root_description"]
    COLLECTION_NAME = site_config["collection_name"]

    gallery = load_json("gallery/gallery_data.json")
    items = sorted(gallery["items"], key=lambda i: i["id"])  # deterministic order
    vector = {it["id"]: it for it in load_json("vector.json")["items"]}
    captions = {c["id"]: (c.get("subject") or "").strip() for c in load_json("content_tags.json")}

    palettes = {}
    for wid, rec in vector.items():
        ax6 = rec.get("axes", {}).get("AX-6_palette")
        if ax6 and ax6.get("value"):
            palettes[wid] = ax6["value"]

    # fresh bundle
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)

    # work pages
    slugs = {}
    for it in items:
        cap = captions.get(it["id"], "")
        pal = palette_of(it["id"], palettes, it.get("dom"))
        slug, doc = render_work(it, cap, pal, site_url)
        slugs[it["id"]] = slug
        write(out_dir / "w" / f"{slug}.html", doc)

    # the exhibition root `/` (EX) — crawlable JS-off face + the client walk
    write(out_dir / "index.html", render_exhibition(items, captions, slugs, site_url))
    copy_exhibition_assets(out_dir, engine_assets_dir, instance_assets_dir)

    # the client walk's baked data: per-work normalized kinship vectors (neutral coords) +
    # a lean work list (id, image, its /w/ slug, dims, dominant colour for the reactive ground)
    vectors, ex_version = exhibition_vectors(load_json("vector.json")["items"])
    ex_works = [{
        "id": it["id"],
        "img": f"/gallery/{it['img']}",
        "slug": f"/w/{slugs[it['id']]}.html",
        "w": it.get("w", ""), "h": it.get("h", ""),
        "dom": it.get("dom"),
    } for it in items]
    exdata = {"version": ex_version, "works": ex_works,
              "v": {it["id"]: vectors[it["id"]] for it in items if it["id"] in vectors},
              # the threshold's pool ships INSIDE this one artifact — one fetch, under the same
              # bounded arrival the walk grants (EX-DOOR; prover F1)
              "door": {"pool": door_pool({it["id"]: it for it in items}, captions, content_dir)}}
    write(out_dir / "exhibition_data.json",
          json.dumps(exdata, ensure_ascii=False, indent=0, sort_keys=True) + "\n")

    # sitemap: exhibition root + every work page, each once
    urls = [f"{site_url}/"] + [f"{site_url}/w/{slugs[it['id']]}.html" for it in items]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append(f"  <url><loc>{esc(u)}</loc></url>")
    sm.append("</urlset>")
    write(out_dir / "sitemap.xml", "\n".join(sm) + "\n")

    # robots: disallow on a preview host, allow on production
    is_preview = "pages.dev" in site_url
    if is_preview:
        robots = f"User-agent: *\nDisallow: /\nSitemap: {site_url}/sitemap.xml\n"
    else:
        robots = f"User-agent: *\nAllow: /\nSitemap: {site_url}/sitemap.xml\n"
    write(out_dir / "robots.txt", robots)

    # config.json — flags (AI OFF) + the exhibition feel-knobs (every one A/B-tunable) +
    # site_url + experiment registry seam
    config = dict(DEFAULT_FLAGS)
    config["exhibition"] = {
        "spread_size": 10,       # works on the wall (3–12) — a gallery hang, never the whole catalogue
        "row_size": 4,           # works per row on a laptop/wide screen — the wall's rhythm
        "cold_spread": "diverse",  # how the first spread is chosen: 'diverse' (farthest-point) | 'first'
        "arc_shape": "widening",   # how a tap's arc samples near→far: 'widening' (holds contrast) | 'nearest'
        "transition_ms": 620,    # reflow duration = the tap-lock window (feel of the reassembly)
        "kinship_axes": "all",   # which axes drive distance: 'all' | [indices] (core-vs-descriptive)
        "unfold_step": 5,        # works appended per "open more" along the current arc
        "max_unfolds": 2,        # unfold steps before "more" retires — the arc ENDS
        "door_size": 5,          # works at the threshold, 3–5 (EX-DOOR)
    }
    config["site_url"] = site_url
    config["ga_measurement_id"] = ga_id   # analytics id lives in config, never in a template
    config["experiments"] = {}      # variant → flag → metric (empty registry)
    write(out_dir / "config.json", json.dumps(config, ensure_ascii=False, indent=2, sort_keys=True) + "\n")

    # reserved empty /api namespace for later serverless AI
    write(out_dir / "api" / ".gitkeep", "")

    # shared images + design tokens (the exhibition renders in them)
    copy_gallery(out_dir, content_dir)

    return {"works": len(items), "site_url": site_url, "preview": is_preview}


def main():
    # Engine root: the parent of this file's parent (gallery-engine/)
    _engine_dir = Path(__file__).resolve().parent
    _engine_assets_default = _engine_dir / "assets"

    ap = argparse.ArgumentParser(
        description="gallery-engine static bake — builds a deployable site bundle from content data"
    )
    ap.add_argument("--content", required=True,
                    help="path to content directory (holds gallery/, vector.json, content_tags.json, etc.)")
    ap.add_argument("--site", required=True,
                    help="path to site.json (instance config: site_name, creator, …)")
    ap.add_argument("--out", required=True,
                    help="output directory (written fresh each run)")
    ap.add_argument("--site-url", default="https://example.com",
                    help="base URL for absolute og:image / canonical (use the *.pages.dev host for preview)")
    ap.add_argument("--ga-id", default="",
                    help="GA4 measurement id (G-…); empty = no analytics tag baked")
    ap.add_argument("--instance-assets", default=None,
                    help="directory holding favicon.svg/png, apple-touch-icon.png (fallback if not in <content>/instance-assets/)")
    args = ap.parse_args()

    content_dir = Path(args.content).resolve()
    out_dir = Path(args.out).resolve()
    site_url = args.site_url.rstrip("/")

    with open(args.site, encoding="utf-8") as fh:
        site_config = json.load(fh)

    # Instance assets: prefer <content>/instance-assets/, fall back to --instance-assets
    instance_assets_dir = content_dir / "instance-assets"
    if not instance_assets_dir.exists() and args.instance_assets:
        instance_assets_dir = Path(args.instance_assets).resolve()
    elif not instance_assets_dir.exists():
        instance_assets_dir = None

    summary = build(
        site_url,
        ga_id=args.ga_id,
        content_dir=content_dir,
        out_dir=out_dir,
        engine_assets_dir=_engine_assets_default,
        instance_assets_dir=instance_assets_dir,
        site_config=site_config,
    )
    print(f"baked {summary['works']} work pages + exhibition root → {out_dir}")
    print(f"site_url={summary['site_url']}  robots={'DISALLOW (preview)' if summary['preview'] else 'ALLOW (prod)'}")


if __name__ == "__main__":
    main()
