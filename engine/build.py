#!/usr/bin/env python3
"""exhibition-engine static bake — the GENERIC builder: a deployable exhibition bundle from a
content directory + a site.json instance identity. Absorbed the instance's full day 2026-07-07
(clean addresses, consent, the any-locale worker, visitor memory, series rooms, the living hand,
the quiet copyright) — proven byte-identical against the instance's own bake (see CHECKPOINT).

Content contract (<content>/): gallery/gallery_data.json + gallery/assets + gallery/shared ·
vector.json · content_tags.json · gallery/door_candidates.json (optional) · data/greetings.json ·
finalist_series.json (optional).

Usage:
  python engine/build.py --content <dir> --site example/site.json --out <dir> \
      --site-url https://… [--ga-id G-…] [--enable ai_i18n] [--instance-assets <dir>]
"""
import argparse
import datetime
import hashlib
import html
import json
import re
import shutil
from pathlib import Path

# Set by build() — module-level so helpers read them without threading params (the original's shape)
OUT = None               # the output bundle dir
ROOT = None              # the CONTENT dir
CREATOR = ""
SITE_NAME = ""
ROOT_TITLE = ""
ROOT_DESCRIPTION = ""
COLLECTION_NAME = ""
COPYRIGHT = ""           # composed in build() — the year is the bake run's own
_ENGINE_ASSETS = None
_INSTANCE_ASSETS = None

DEFAULT_FLAGS = {
    "ai_greeting": False,     # canned greeting only; serverless Haiku swaps in later behind /api  (INV-19)
    "ai_assemble": False,     # deterministic client-side kinship only                              (INV-19)
    "ai_i18n": False,         # the any-locale worker (EX-I18N); ships false, flipped at deploy    (INV-19)
    "ai_story": False,        # the told story — runtime Haiku narrator (EX-STORY); ships false     (INV-19)
    "visitor_memory": False,  # the coat-check token + seen-list edge (EX-MEMORY); flipped at deploy
    "caption_visible": False, # the machine caption stays in meta/alt/JSON-LD, never visible        (RESOLVED 2026-07-05)
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
    """The crawlable title — never empty (INV-23): his title → caption → section+place → default."""
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
.sign{color:#7c7c88;font-size:12.5px;margin-top:2.4em}
"""


GA_ID = ""   # set by build(ga_id=…) — empty ⇒ NO analytics tag anywhere (config, never hardcode)


def ga_snippet():
    if not GA_ID:
        return ""
    # consent speaks FIRST (EX-PULSE): the museum runs no ads — every advertising storage/use
    # denied; analytics measurement granted [default — no cookie wall on a quiet museum]
    return (
        f'<script async src="https://www.googletagmanager.com/gtag/js?id={esc(GA_ID)}"></script>\n'
        "<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}"
        "gtag('consent','default',{'ad_storage':'denied','ad_user_data':'denied',"
        "'ad_personalization':'denied','analytics_storage':'granted'});"
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
    canonical = f"{site_url}/w/{slug}"   # clean address (WP-CLEAN); the file stays .html on disk
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
<p class="sign">{COPYRIGHT}</p>
</article>
</main>
</body>
</html>
"""
    doc = head(idx_title, caption or idx_title, canonical, og_image, "article", jsonld, extra_og) + body
    return slug, doc


def exhibition_vectors(vector_items):
    """Per-work kinship vector for the client walk — deterministic, INV-1-safe.

    Every axis of vector.json that is numeric in ANY work becomes a coordinate (the radial family
    is null on non-radial images → treated as 0, a meaningful 'no radial structure'). Each coordinate
    is min-max normalized across the collection to [0,1] so no axis dominates by scale. The output uses
    a NEUTRAL key ('v') and bare coordinate arrays — no axis name, no labelled score ever reaches a
    file the visitor can read (INV-1). Returns (vectors {id:[floats]}, version tag).
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
    # version changes whenever the axis SET changes → old localStorage arcs are discarded (INV-26)
    version = hashlib.sha1((",".join(axes)).encode("utf-8")).hexdigest()[:8]
    return vectors, version


def render_exhibition(items, captions, slugs, site_url):
    """The exhibition root `/` (EX). ONE surface, two faces (INV-25): the served HTML is the crawlable
    JS-off face — a real heading, indexable intro about the COLLECTION (never a work's vector), and a
    static index linking every work to its /w/ page; `exhibition.js` then re-renders it into the live
    adaptive walk. Carries its own root og:image (a fixed representative work so a shared homepage link
    unfurls) + canonical + WebSite/CollectionPage JSON-LD."""
    canonical = f"{site_url}/"
    hero = items[0]                                   # deterministic representative work (INV-21)
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
    # progressive enhancement keeps a bounded worst case, never a blank page (INV-25/CS-8).
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
            f'<a href="/w/{slugs[it["id"]]}"><img src="/gallery/{esc(it["img"])}" '
            f'alt="{esc(alt)}" loading="lazy"></a>'
        )
    grid = "".join(cards)
    body = f"""<body>
<div class="ex-head">
<h1 class="site-h1">{esc(SITE_NAME)}</h1>
<span class="ex-hint" id="ex-hint">an exhibition that assembles itself around you</span>
</div>
<div class="ex-stage" id="ex-stage"></div>
<main class="wrap" id="ex-static">
<p class="lede">{esc(desc)}</p>
<nav class="grid" aria-label="All works">{grid}</nav>
<p class="sign">{COPYRIGHT}</p>
</main>
<script src="/exhibition.js" defer></script>
</body>
</html>
"""
    return head(title, desc, canonical, og_image, "website", jsonld, extra_head=extra_head) + body


# ---------------------------------------------------------------- bundle

def copy_gallery():
    """Copy the shared images + design tokens into the bundle (self-contained, INV-18). The old
    Room/Door prototypes are RETIRED — the exhibition (EX) is now the single converged front door,
    so no prototype HTML ships; only the assets and the shared tokens the exhibition renders in."""
    dst = OUT / "gallery"
    src = ROOT / "gallery"
    (dst).mkdir(parents=True, exist_ok=True)
    if (src / "gallery_data.json").exists():
        shutil.copy2(src / "gallery_data.json", dst / "gallery_data.json")
    for sub in ("assets", "shared"):
        if (src / sub).exists():
            shutil.copytree(src / sub, dst / sub, dirs_exist_ok=True)


def copy_exhibition_assets():
    """The exhibition client (JS+CSS) comes from the ENGINE's own assets; favicons from the
    instance's assets dir (absent → the bundle simply has none). Source files, never inlined."""
    for name in ("exhibition.js", "exhibition.css"):
        shutil.copy2(_ENGINE_ASSETS / name, OUT / name)
    for name in ("favicon.svg", "favicon.png", "apple-touch-icon.png"):
        cand = _INSTANCE_ASSETS / name if _INSTANCE_ASSETS else None
        if cand and cand.exists():
            shutil.copy2(cand, OUT / name)


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def door_pool(items_by_id, captions):
    """The door pool (EX-DOOR): the door-candidates provenance ids intersected with the LIVING
    gallery works — an id that left the gallery silently drops out. Each entry carries the alt
    text a door work needs (his title → caption → quiet label; the door asks wordlessly, but a
    keyboard/screen-reader visitor still meets real words). Returns [] when the source is absent."""
    src = ROOT / "gallery" / "door_candidates.json"
    if not src.exists():
        return []
    pool = []
    for e in json.loads(src.read_text(encoding="utf-8")):
        item = items_by_id.get(e.get("id"))
        if not item:
            continue                                   # not a living work → drop (thin-pool degrade)
        cap = captions.get(item["id"], "")
        pool.append({"id": item["id"], "alt": indexable_title(item, cap),
                     # the candidates' own tone numbers ride along for the living hand's
                     # hour-lean (EX-DOOR-3) — data, never rendered (INV-1)
                     "luma": round(float(e.get("luma", 0.5)), 3),
                     "warmth": round(float(e.get("warmth", 0.5)), 3)})
    return pool


def greetings():
    """The door's greeting strings (EX-GREET-BAKE): the committed cache authored by
    scripts/gen_greetings.py — Haiku at AUTHORING time (drafts stand in until the key lands);
    the bake only READS it (INV-21). Absent or malformed → None: no greet block ships and the
    client stands on its built-in lines — the door never blocks entry (EX-GREET)."""
    src = ROOT / "data" / "greetings.json"
    try:
        g = json.loads(src.read_text(encoding="utf-8"))
        langs = g["langs"]
        assert g["fallback"] in langs
        for L in langs.values():
            assert L["ask"].strip() and "skip" not in L           # skip retired (EX-DOOR-2a)
            assert L["exit"].strip() and "{n}" in L["more"]       # the walk's closing copy
            assert L["q_more"].strip() and L["q_spent"].strip()   # (his word 2026-07-06)
            assert all(L["greet"][p] for p in ("night", "morning", "day", "evening"))
        return {"fallback": g["fallback"], "aliases": g.get("aliases", {}), "langs": langs}
    except Exception:
        return None


def tod_marks_load():
    """EX-STORY-ORDER: the authored time-of-day marks (id → {"marks":[…]}), an OPTIONAL instance
    file. Absent/malformed → {} (every work reads `free`, the arc unchanged). The marks are a public
    axis (day/zenith/sunset/night/free) — data for the light-lean, never rendered (INV-1)."""
    src = ROOT / "data" / "time_of_day.json"
    try:
        return json.loads(src.read_text(encoding="utf-8")).get("marks", {}) or {}
    except Exception:
        return {}


def story_notes_load():
    """EX-STORY-EDGE (ST3): the PRIVATE per-work authored notes (id → note text), an OPTIONAL,
    INSTANCE-OWNED file kept OUT of the public bundle — it is baked only INTO _worker.js and only
    when the story ships. Absent → no notes: fragments carry the public grounding (title/place/
    subject/light) alone. The engine never hardcodes an instance's note filename — an instance
    supplies `<content>/story_notes.json` (a flat {id: note} map); the raw notes stay off every
    public byte. (Proposal (b) in PORT_REPORT: this keeps the private notes instance-private.)"""
    src = ROOT / "story_notes.json"
    try:
        raw = json.loads(src.read_text(encoding="utf-8"))
    except Exception:
        return {}
    notes = raw.get("notes", raw) if isinstance(raw, dict) else {}
    return {str(k): str(v).strip() for k, v in notes.items() if str(v).strip()}


def build(site_url, ga_id="", enable=None, content_dir=None, out_dir=None,
          engine_assets_dir=None, instance_assets_dir=None, site_config=None):
    """``enable``: flag names switched ON for this bake; every worker flag ships false by
    default, the flip is a deploy argument. Identity comes from site.json — the engine knows
    no instance."""
    global GA_ID, OUT, ROOT, CREATOR, SITE_NAME, ROOT_TITLE, ROOT_DESCRIPTION
    global COLLECTION_NAME, COPYRIGHT, _ENGINE_ASSETS, _INSTANCE_ASSETS
    GA_ID = ga_id
    OUT = out_dir
    ROOT = content_dir
    _ENGINE_ASSETS = engine_assets_dir
    _INSTANCE_ASSETS = instance_assets_dir
    SITE_NAME = site_config["site_name"]
    CREATOR = site_config["creator"]
    ROOT_TITLE = site_config["root_title"]
    ROOT_DESCRIPTION = site_config["root_description"]
    COLLECTION_NAME = site_config["collection_name"]
    COPYRIGHT = f"© {datetime.date.today().year} {CREATOR} · {SITE_NAME}"
    if OUT.exists():
        shutil.rmtree(OUT)                             # a fresh bundle, deterministic
    OUT.mkdir(parents=True)
    flags = dict(DEFAULT_FLAGS)
    for name in (enable or []):
        if name not in flags:
            raise SystemExit(f"unknown flag: {name} (the bake owns the schema)")
        flags[name] = True
    gallery = load_json("gallery/gallery_data.json")
    items = sorted(gallery["items"], key=lambda i: i["id"])  # deterministic order (INV-21)
    vector = {it["id"]: it for it in load_json("vector.json")["items"]}
    captions = {c["id"]: (c.get("subject") or "").strip() for c in load_json("content_tags.json")}

    palettes = {}
    for wid, rec in vector.items():
        ax6 = rec.get("axes", {}).get("AX-6_palette")
        if ax6 and ax6.get("value"):
            palettes[wid] = ax6["value"]

    # fresh bundle
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    # work pages
    slugs = {}
    for it in items:
        cap = captions.get(it["id"], "")
        pal = palette_of(it["id"], palettes, it.get("dom"))
        slug, doc = render_work(it, cap, pal, site_url)
        slugs[it["id"]] = slug
        write(OUT / "w" / f"{slug}.html", doc)

    # the exhibition root `/` (EX) — crawlable JS-off face + the client walk
    write(OUT / "index.html", render_exhibition(items, captions, slugs, site_url))
    copy_exhibition_assets()

    # the client walk's baked data: per-work normalized kinship vectors (neutral coords, INV-1) +
    # a lean work list (id, image, its /w/ slug, dims, dominant colour for the reactive ground)
    vectors, ex_version = exhibition_vectors(load_json("vector.json")["items"])
    # EX-STORY-ORDER (INV-47): the authored light marks lean the told story's order (a work reads as
    # a SET, `free` = unconstrained). OPTIONAL instance data — absent → every work is `free`, the
    # light-lean a no-op and the arc unchanged (the byte-identical guard, ST1). Data, never rendered.
    tod_marks = tod_marks_load()
    tod_of = lambda wid: (tod_marks.get(str(wid), {}) or {}).get("marks") or ["free"]
    ex_works = [{
        "id": it["id"],
        "img": f"/gallery/{it['img']}",
        "slug": f"/w/{slugs[it['id']]}",     # clean address (WP-CLEAN)
        "w": it.get("w", ""), "h": it.get("h", ""),
        "dom": it.get("dom"),
        # the hang's caption zone (EX-HANG): his title + the archive's facts — presentation,
        # never a readout (INV-1 as amended 2026-07-06); machine captions stay meta-only
        "title": (it.get("title") or "").strip(),
        "sec": it.get("section", ""),
        "place": place_of(it),
        "tod": tod_of(it["id"]),             # the light marks (EX-STORY-ORDER) — data, never rendered
    } for it in items]
    # (per-work series mark joins after the series block computes below)
    # EX-SERIES (INV-46): real series only (3+), the variant from the series' own size,
    # NEVER the machine's theme label (INV-1) — the guest reads only «серия · N»
    ser_src = load_json("finalist_series.json").get("series", [])
    id_of = lambda m: m.split("_", 1)[1].rsplit(".", 1)[0]
    live_ids = {it["id"] for it in items}
    ex_series = []
    ser_of = {}
    for srec in ser_src:
        members = [id_of(m) for m in srec.get("members", []) if id_of(m) in live_ids]
        if len(members) < 3:
            continue
        idx = len(ex_series)
        ex_series.append({"variant": "polaroids" if len(members) >= 8 else "lane",
                          "members": members})
        for mid in members:
            ser_of[mid] = idx
    for w in ex_works:
        if w["id"] in ser_of:
            w["ser"] = ser_of[w["id"]]                 # the pill's own mark (EX-SERIES)
    exdata = {"version": ex_version, "works": ex_works, "series": ex_series,
              # the walk's own face signs off with the same composed line (EX-COPY)
              "copyright": COPYRIGHT,
              "v": {it["id"]: vectors[it["id"]] for it in items if it["id"] in vectors},
              # the threshold's pool ships INSIDE this one artifact — one fetch, under the same
              # bounded arrival INV-25 grants the walk (EX-DOOR; prover F1)
              "door": {"pool": door_pool({it["id"]: it for it in items}, captions)}}
    # the greeting rides the SAME artifact — one fetch, INV-25's bounded arrival (EX-GREET)
    greet = greetings()
    if greet:
        exdata["greet"] = greet
    write(OUT / "exhibition_data.json",
          json.dumps(exdata, ensure_ascii=False, indent=0, sort_keys=True) + "\n")

    # sitemap: exhibition root + every work page, each once; each work carries its photograph as an
    # <image:image> so Google Images can discover all works (INV-53 — the SEO audit's #1 photo-site win)
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"'
          ' xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">',
          f"  <url><loc>{esc(site_url)}/</loc></url>"]
    for it in items:
        wu = f"{site_url}/w/{slugs[it['id']]}"
        img = f"{site_url}/gallery/{it['img']}"
        sm.append(f"  <url><loc>{esc(wu)}</loc>"
                  f"<image:image><image:loc>{esc(img)}</image:loc></image:image></url>")
    sm.append("</urlset>")
    write(OUT / "sitemap.xml", "\n".join(sm) + "\n")

    # robots: disallow on a preview host, allow on production
    is_preview = "pages.dev" in site_url
    if is_preview:
        robots = f"User-agent: *\nDisallow: /\nSitemap: {site_url}/sitemap.xml\n"
    else:
        robots = f"User-agent: *\nAllow: /\nSitemap: {site_url}/sitemap.xml\n"
    write(OUT / "robots.txt", robots)

    # config.json — flags (AI OFF) + the exhibition feel-knobs (every one A/B-tunable, INV-28) +
    # site_url + experiment registry seam
    config = dict(flags)
    config["exhibition"] = {
        "spread_size": 10,       # works in the hang (3–12) — never the whole catalogue
        "cold_spread": "diverse",  # the silent-entry hang: 'diverse' (farthest-point) | 'first'
        "arc_shape": "widening",   # how the arc samples near→far: 'widening' (holds contrast) | 'nearest'
        "tempo": 1.35,           # the ONE motion multiplier over the --d-* tokens (EX-MOTION, design 04)
        # transition_ms LEFT the schema with the tempo law (EX-MOTION tombstone, 2026-07-06) —
        # the crossing rides the cross token (1.2s × tempo)
        "kinship_axes": "all",   # which axes drive distance: 'all' | [indices] (core-vs-descriptive)
        "unfold_step": 5,        # works appended per «ещё 5» along the current arc
        "max_unfolds": 2,        # unfold steps before «ещё 5» retires — the arc ENDS (INV-30)
        "door_size": 5,          # works at the threshold, 3–5 (EX-DOOR)
        "greeting": "ask",       # where the door's greeting hangs: ask (his pick) | top | off (EX-GREET)
        # row_size LEFT the schema with the grid wall (EX-WALL tombstone, 2026-07-06)
        # the told story's feel-knobs (EX-STORY-AB / EX-STORY-ORDER, INV-47) — on/off is the top-level
        # ai_story flag (INV-19); these are the A/B tunables (INV-28). params_version feeds the story
        # cache key so a knob flip never serves a stale order (prover ST4).
        "story": {
            "variant": "B",        # the writing mode that ships first: B (cheap light/hour plot)
            "light_weight": 0.6,   # how hard the light leans the order: 0 = pure kinship, high = a strict march
            "params_version": 1,   # bump on any light_weight/prompt/marks change → the cache key moves
        },
        # EX-SOUND (INV-48): the ambient loop. sound_url is the audio file (empty = player hidden,
        # the default — the gallery engine ships OFF; an instance opts in by setting this path).
        # sound_credit holds the artist credit shown in the tray (all optional; missing = no credit shown).
        "sound_url": "",           # path to the .m4a / .ogg — empty means no player renders
        "sound_credit": {          # the tray's attribution — instance fills its own
            "artist": "",          # artist/band name (shown bold)
            "title": "",           # track/album title (shown in «»)
            "url": "",             # artist website (shown as a link)
        },
    }
    config["site_url"] = site_url
    config["ga_measurement_id"] = ga_id   # analytics id lives in config, never in a template
    config["experiments"] = {}      # variant → flag → metric (empty registry)
    write(OUT / "config.json", json.dumps(config, ensure_ascii=False, indent=2, sort_keys=True) + "\n")

    # reserved empty /api namespace for later serverless AI (CS-7)
    write(OUT / "api" / ".gitkeep", "")

    # ---- EX-STORY-EDGE (INV-47, ST3): the PRIVATE per-work story fragments ----------
    # title/place/subject/light are public grounding; the note is the instance's own words (the model
    # adapts, never quotes). Fragments are EMBEDDED into _worker.js (the one bundle file Cloudflare
    # Pages never serves as an asset), NEVER a public static byte, and only when the story ships — so
    # raw notes never leave the edge. Deterministic (sorted) so the bake stays reviewable.
    story_notes = story_notes_load()
    story_fragments = {}
    if flags["ai_story"]:
        for it in items:
            wid = str(it["id"])
            frag = {"title": (it.get("title") or "").strip(),
                    "place": place_of(it),
                    "subject": captions.get(it["id"], ""),
                    "tod": tod_of(it["id"])}
            note = story_notes.get(wid, "")
            if note:
                frag["note"] = note                    # private — off the bundle, only into _worker.js
            story_fragments[wid] = frag

    # ---- EX-I18N (INV-42) / EX-STORY-EDGE: the edge worker ships ONLY under its flags ----------
    # The worker reads /i18n_source.json from its own deployment (deterministic, sorted — prover I4);
    # the story fragments are baked INTO the worker file; _routes.json keeps every static byte pure
    # CDN (only /api/* invokes it).
    if flags["ai_i18n"] or flags["visitor_memory"] or flags["ai_story"]:
        worker_src = (_ENGINE_ASSETS / "worker.js").read_text(encoding="utf-8")
        worker_src = worker_src.replace(
            '/*__STORY_FRAGMENTS__*/{}/*__/STORY_FRAGMENTS__*/',
            json.dumps(story_fragments, ensure_ascii=False, sort_keys=True))
        worker_src = worker_src.replace(
            '/*__STORY_PV__*/"0"/*__/STORY_PV__*/',
            json.dumps(str(config["exhibition"]["story"]["params_version"])))
        write(OUT / "_worker.js", worker_src)
        write(OUT / "_routes.json",
              json.dumps({"version": 1, "include": ["/api/*"], "exclude": []}) + "\n")
    if flags["ai_i18n"]:
        en = ((greet or {}).get("langs") or {}).get("en") or {}
        i18n_src = {
            "version": ex_version,
            "strings": {k: en.get(k, "") for k in
                        ("ask", "exit", "more", "q_more", "q_spent",
                         "share_label", "share_copied", "series", "room_back")},
            "greet": en.get("greet") or {},
            # brand + the © signature are EXCLUDED by construction (never translatable)
            "titles": {it["id"]: it["title"].strip()
                       for it in items if (it.get("title") or "").strip()},
        }
        write(OUT / "i18n_source.json",
              json.dumps(i18n_src, ensure_ascii=False, indent=0, sort_keys=True) + "\n")

    # shared images + design tokens (the exhibition renders in them)
    copy_gallery()

    return {"works": len(items), "site_url": site_url, "preview": is_preview}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--content", required=True, help="the content directory")
    ap.add_argument("--site", required=True, help="site.json — the instance identity")
    ap.add_argument("--out", required=True, help="output bundle directory")
    ap.add_argument("--site-url", required=True)
    ap.add_argument("--ga-id", default="")
    ap.add_argument("--enable", action="append", default=[],
                    help="switch a config flag ON for this bake (deploy sets values)")
    ap.add_argument("--instance-assets", default=None,
                    help="favicons dir (fallback when <content>/instance-assets is absent)")
    args = ap.parse_args()
    content_dir = Path(args.content).resolve()
    out_dir = Path(args.out).resolve()
    with open(args.site, encoding="utf-8") as fh:
        site_config = json.load(fh)
    inst = content_dir / "instance-assets"
    if not inst.exists():
        inst = Path(args.instance_assets).resolve() if args.instance_assets else None
    engine_assets = Path(__file__).resolve().parent / "assets"
    summary = build(args.site_url.rstrip("/"), ga_id=args.ga_id, enable=args.enable,
                    content_dir=content_dir, out_dir=out_dir,
                    engine_assets_dir=engine_assets, instance_assets_dir=inst,
                    site_config=site_config)
    print(f"baked {summary['works']} work pages + exhibition root → {out_dir}")
    print(f"site_url={summary['site_url']}  robots={'DISALLOW (preview)' if summary['preview'] else 'ALLOW (prod)'}")


if __name__ == "__main__":
    main()
