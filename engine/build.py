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
import sys
from pathlib import Path

# A caller that imports this module (rather than running it as `python engine/build.py`, which
# auto-prepends this file's own directory) does not necessarily have engine/ on sys.path — the
# site's own release pipeline imports build.py this way and this import broke it. Put this file's
# own directory on sys.path explicitly rather than assuming the caller did.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import assemble_client  # engine/assemble_client.py — sibling module

# Set by build() — module-level so helpers read them without threading params (the original's shape)
OUT = None               # the output bundle dir
ROOT = None              # the CONTENT dir
CREATOR = ""
SITE_NAME = ""
ROOT_TITLE = ""
ROOT_DESCRIPTION = ""
COLLECTION_NAME = ""
LOADING_LINE = ""        # EX-LOAD: the cold-arrival line, instance-supplied (generic default)
HINT_LINE = ""           # the JS-off subtitle under the site name, instance-supplied (default in build)
OG_IMAGE_ID = ""         # INV-25: the work a shared homepage link unfurls with; blank = first (INV-21)
COPYRIGHT = ""           # composed in build() — the year is the bake run's own (static faces)
COPYRIGHT_NO_ABOUT = ""  # the same line where an about link would point at the page in hand (INV-103)
_ENGINE_ASSETS = None
_INSTANCE_ASSETS = None
_NAMESPACE = "ex"        # EX-NS: storage-key/global/perf-mark namespace; instance overrides via site.json

DEFAULT_FLAGS = {
    "ai_greeting": False,     # canned greeting only; serverless Haiku swaps in later behind /api  (INV-19)
    "ai_assemble": False,     # deterministic client-side kinship only                              (INV-19)
    "ai_i18n": False,         # the any-locale worker (EX-I18N); ships false, flipped at deploy    (INV-19)
    "ai_story": False,        # the told story — runtime Haiku narrator (EX-STORY); ships false     (INV-19)
    "visitor_memory": False,  # the coat-check token + seen-list edge (EX-MEMORY); flipped at deploy
    "caption_visible": False, # the machine caption stays in meta/alt/JSON-LD, never visible        (RESOLVED 2026-07-05)
    "quiz": False,            # per-work question + signed wallpaper gift (EX-QUIZ / INV-59); ships false (INV-19)
    "door_diversity": False,  # EX-DOOR-3 diverse door: the pool spans the whole living gallery, a FRESH
                              # spread set is dealt every open, ≥ a place-group fraction guaranteed among
                              # the shown windows (an instance sets the group in site.json). OFF → the
                              # curated door_candidates pool, byte-identical (INV-19)
}


# ---------------------------------------------------------------- data helpers

def validate_experiments(experiments, reserved=()):
    """EX-AB (INV-90): the bake refuses a degenerate experiment registry — an arms list under two
    words never splits, and a salt shared inside the registry (or colliding with another draw key
    hashed off the same visitor seed: a work id, the literal "once") deals correlated draws."""
    seen = {}
    for name, entry in (experiments or {}).items():
        arms = (entry or {}).get("arms")
        if not isinstance(arms, list) or len(arms) < 2:
            raise SystemExit(
                f"experiments[{name!r}]: arms must list at least two closed words (EX-AB/INV-90)")
        salt = (entry or {}).get("salt") or name
        if salt in seen:
            raise SystemExit(
                f"experiments[{name!r}]: salt {salt!r} already used by experiment {seen[salt]!r} — "
                f"one shared key deals correlated draws (EX-AB/INV-90)")
        if salt == "once" or salt in reserved:
            raise SystemExit(
                f"experiments[{name!r}]: salt {salt!r} collides with another draw key off the same "
                f"seed (EX-AB/INV-90)")
        seen[salt] = name


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


def compose_sign(year, creator, site_name, instagram=None, about_word=None):
    """EX-COPY (INV-28): the one quiet signature. The copyright line — composed from the bake
    run's own year, the creator, and the site name — with up to two OPTIONAL links trailing it.

    ``instagram`` (a full URL or a bare @handle) trails the creator's own social page: it leaves
    the site, so it opens in a new tab under `noopener noreferrer`. ``about_word`` trails the
    about page (EX-ABOUT / INV-103) at the bare `/about`: it stays INSIDE the site, so it opens
    in place. An instance that names neither gets the plain line, untouched.

    The about link is the caller's choice per SURFACE, not a global: the walk's closing screen
    already carries its own about line in the visitor's own tongue, so the signature composed for
    the client artifact passes no ``about_word`` and a visitor never meets two doors to one page
    side by side (INV-103)."""
    line = f"© {year} {creator} · {site_name}"
    handle = (instagram or "").strip()
    if handle:
        url = handle if handle.startswith("http") else "https://instagram.com/" + handle.lstrip("@")
        line += (f' · <a class="sign-ig" href="{esc(url)}" target="_blank"'
                 f' rel="noopener noreferrer">Instagram</a>')
    word = (about_word or "").strip()
    if word:
        line += f' · <a class="sign-about" href="/about">{esc(word)}</a>'
    return line


def about_path(lang, fallback="en"):
    """The address of the about page in one language (EX-ABOUT / INV-102). The fallback tongue
    keeps the bare `about`, so every static face and every shared link can point at one stable
    address; the others sit one level down. A page of prose carries no script, so it cannot
    translate itself on arrival — one baked page per tongue is how a scriptless page speaks
    several languages (INV-16)."""
    return "about" if lang == fallback else f"about/{lang}"


def pick_hero(items, og_image_id=None):
    """INV-25: the root's own og:image — the one work a shared homepage link unfurls with. The
    instance names it in site.json as `og_image_id`; an instance that names none, or that names an
    id no longer in the gallery, gets the first work in the deterministic order (INV-21). Either way
    the choice is fixed for a given bake, so the bake stays reproducible."""
    if not items:
        return None
    wanted = (str(og_image_id).strip() if og_image_id is not None else "")
    if wanted:
        for it in items:
            if str(it.get("id")) == wanted:
                return it
    return items[0]


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
.sign a{color:inherit;text-decoration:underline;text-underline-offset:2px}
.about{max-width:62ch;padding-left:max(clamp(20px,4vw,56px),env(safe-area-inset-left));padding-right:max(clamp(20px,4vw,56px),env(safe-area-inset-right))}
.about h1{font-weight:400;font-size:clamp(22px,3.4vw,30px);line-height:1.25;margin:1.5em 0 1.1em}
.about p{max-width:60ch;line-height:1.75;margin:0 0 1.15em}
.about-back{display:inline-flex;align-items:center;gap:.5em;padding:.55em 1.1em;border:1px solid #3a3a42;border-radius:999px;text-decoration:none;color:#cfcfda;min-height:44px;font-size:14px}
.about-back::before{content:"←"}
[dir=rtl] .about-back::before{content:"→"}
@media (hover:hover){.about-back:hover{border-color:#6a6a78;color:#e9e9ee}}
.about-back:focus-visible{outline:2px solid #b3a284;outline-offset:3px}
.about-back.is-press{border-color:#6a6a78;background:rgba(255,255,255,.05)}
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


def og_image_tags(og_image, description):
    """The share-picture tags, emitted ONLY when the page has a picture. The about page is prose
    and carries none, and a page that names an empty image unfurls as a BROKEN card rather than a
    plain one — so the tags are omitted whole and the caller drops the Twitter card to its text
    form (INV-102)."""
    if not og_image:
        return ""
    return (f'<meta property="og:image" content="{esc(og_image)}">\n'
            f'<meta property="og:image:alt" content="{esc(description)}">\n')


def head(title, description, canonical, og_image, og_type, jsonld, extra_og="", extra_head="",
         lang="en", direction=""):
    """``lang``/``direction``: the document's own tongue and reading direction. They default to
    the values every page carried before the about page existed, so a caller that passes neither
    bakes a byte-identical head (INV-102)."""
    dir_attr = f' dir="{esc(direction)}"' if direction else ""
    card = "summary_large_image" if og_image else "summary"
    image_tags = og_image_tags(og_image, description)
    twitter_image = (f'<meta name="twitter:image" content="{esc(og_image)}">\n'
                     if og_image else "")
    return f"""<!doctype html>
<html lang="{esc(lang)}"{dir_attr}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
<meta name="generator" content="exhibition-engine · https://github.com/happysasha18/exhibition-engine">
<!-- Built with exhibition-engine, an open-source exhibition-site generator: https://github.com/happysasha18/exhibition-engine -->
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.png" type="image/png" sizes="64x64">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{esc(canonical)}">
<meta property="og:site_name" content="{esc(SITE_NAME)}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{esc(canonical)}">
{image_tags}{extra_og}<meta name="twitter:card" content="{card}">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(description)}">
{twitter_image}<script type="application/ld+json">
{json.dumps(jsonld, ensure_ascii=False, indent=0, sort_keys=True)}
</script>
<style>{STYLE}</style>
{ga_snippet()}{extra_head}</head>
"""


def render_work(item, caption, palette, site_url, display_max=None):
    wid = item["id"]
    slug = work_slug(item.get("title", ""), caption, wid)
    canonical = f"{site_url}/w/{slug}"   # clean address (WP-CLEAN); the file stays .html on disk
    img_rel = f"/gallery/{item['img']}"          # gallery/assets/<section>/<id>.jpg → /gallery/assets/...
    og_image = f"{site_url}/gallery/{item['img']}"
    idx_title = indexable_title(item, caption)
    vis_title = visible_title(item)
    alt = caption or idx_title
    loc = place_of(item)
    ow, oh = served_dims(item.get("w"), item.get("h"), display_max)   # dims of the SERVED image (INV-56)
    # the image as an ImageObject with its served dimensions — qualifies the work for Google Images
    # rich treatment (INV-58); artform names the medium (a real VisualArtwork property)
    img_obj = {"@type": "ImageObject", "url": og_image, "contentUrl": og_image}
    if ow and oh:
        img_obj["width"], img_obj["height"] = ow, oh

    jsonld = {
        "@context": "https://schema.org",
        "@type": "VisualArtwork",
        "name": idx_title,
        "artform": "Photography",
        "image": img_obj,
        "url": canonical,
        "creator": {"@type": "Person", "name": CREATOR},
        "copyrightHolder": {"@type": "Person", "name": CREATOR},
    }
    if caption:
        jsonld["description"] = caption
    if loc:
        jsonld["contentLocation"] = loc

    extra_og = (
        f'<meta property="og:image:width" content="{ow}">\n'
        f'<meta property="og:image:height" content="{oh}">\n'
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

    # EX-LADDER (INV-63): when the display cap runs (deploy), the work img offers the 640/960/1280
    # ladder; the base `src` stays the untouched fallback. No cap (test bake) ⇒ the img is byte-identical.
    ladder = (f' srcset="{esc(srcset_of(img_rel))}" sizes="{WORK_SIZES}"' if display_max else "")

    body = f"""<body>
<main class="wrap">
<article class="work">
<img src="{esc(img_rel)}"{ladder} alt="{esc(alt)}" width="{item.get('w','')}" height="{item.get('h','')}">
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


def render_exhibition(items, captions, slugs, site_url, display_max=None):
    """The exhibition root `/` (EX). ONE surface, two faces (INV-25): the served HTML is the crawlable
    JS-off face — a real heading, indexable intro about the COLLECTION (never a work's vector), and a
    static index linking every work to its /w/ page; `exhibition.js` then re-renders it into the live
    adaptive walk. Carries its own root og:image (a fixed representative work so a shared homepage link
    unfurls) + canonical + WebSite/CollectionPage JSON-LD."""
    canonical = f"{site_url}/"
    hero = pick_hero(items, OG_IMAGE_ID)              # the instance's pick, else first (INV-21/25)
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
    # The FOUC guard: with JS on, the crawler's static index must NEVER paint (without it every
    # work flashes on screen for seconds before the walk takes over). The inline script marks <html> as js-alive
    # BEFORE <body> parses, so CSS hides the static face pre-paint; the mark stays through however
    # long the script's ride takes (EX-BOOT/INV-95: the loading breath holds, no stopwatch dumps a
    # slow-network visitor into the static grid mid-ride) — only the script's own onerror (below) or
    # a generous 12s last-net cap on a genuinely HUNG ride removes it, so progressive enhancement
    # keeps a bounded worst case, never a blank page (INV-25/CS-8).
    # cache-bust the code URLs by content hash — the fix that reaches the BROWSER cache: the HTML is
    # served fresh (max-age=0), so a returning visitor always gets the current ?v= and thus fresh
    # JS/CSS the instant a deploy changes them. Hash the SERVED bytes (engine assets + content tokens).
    av = hashlib.sha1(
        client_asset("exhibition.js").read_bytes()      # the SERVED client (instance override wins)
        + client_asset("exhibition.css").read_bytes()
        + (ROOT / "gallery" / "shared" / "tokens.css").read_bytes()
    ).hexdigest()[:8]
    extra_head = ('<script>document.documentElement.classList.add("js");'
                  'setTimeout(function(){if(!document.body||!document.body.classList.contains("ex-live"))'
                  'document.documentElement.classList.remove("js")},12000);</script>\n'
                  f'<link rel="stylesheet" href="/gallery/shared/tokens.css?v={av}">\n'
                  f'<link rel="stylesheet" href="/exhibition.css?v={av}">\n')
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
<span class="ex-hint" id="ex-hint">{esc(HINT_LINE)}</span>
</div>
<div class="ex-stage" id="ex-stage"></div>
<div id="ex-loading" aria-hidden="true"><span>{esc(LOADING_LINE)}</span></div>
<main class="wrap" id="ex-static">
<p class="lede">{esc(desc)}</p>
<nav class="grid" aria-label="All works">{grid}</nav>
<p class="sign">{COPYRIGHT}</p>
</main>
<script src="/exhibition.js?v={av}" defer onerror="document.documentElement.classList.remove('js')"></script>
</body>
</html>
"""
    hw, hh = served_dims(hero.get("w"), hero.get("h"), display_max)   # homepage OG image dims (SEO)
    hero_og = (f'<meta property="og:image:width" content="{hw}">\n'
               f'<meta property="og:image:height" content="{hh}">\n') if hw and hh else ""
    return head(title, desc, canonical, og_image, "website", jsonld,
                extra_og=hero_og, extra_head=extra_head) + body


ABOUT_PARA_KEYS = ("about_1", "about_2", "about_3", "about_4")
# the page copy the CLIENT never reads — stripped from the greet block that rides
# exhibition_data.json, so page prose is not weight on every arrival (INV-104)
ABOUT_PAGE_KEYS = ("about_title",) + ABOUT_PARA_KEYS + ("about_back",)


def about_langs(greet):
    """The languages that get a page (EX-ABOUT / INV-102), in the dictionary's own order.

    The FALLBACK tongue is the floor: the signature's link is language-blind and always points at
    the bare `/about`, so a bundle whose fallback carries no `about_title` would link a page that
    was never baked. No copy there ⇒ NO page in any language and no entry anywhere, the bundle
    byte-identical to a bake without the feature. Above that floor a language earns its own page
    by carrying its own `about_title`."""
    if not greet:
        return []
    fallback = greet.get("fallback")
    langs = greet.get("langs") or {}
    if not (langs.get(fallback) or {}).get("about_title", "").strip():
        return []
    return [L for L, blk in langs.items() if (blk.get("about_title") or "").strip()]


def render_about(site_url, about, lang, langs, fallback, direction=""):
    """The about page (EX-ABOUT / INV-102): one flat page that stands OUTSIDE the exhibition and
    says what it is. The rooms never explain — the threshold asks wordlessly and every room
    answers by behaving — so the account of the exhibition lives here, in the site's own service
    voice, the voice the greeting and the signature already use. No photograph stands on it: the
    exhibition hangs one picture at a time in a room built for it, and a page of prose is not that
    room. No share picture either, or the link unfurls as a broken card.

    ``about``: the copy for ONE language — `about_title`, `about_1`..`about_4`, `about_back` —
    read from the instance's dictionary (INV-20; the bake hand-writes none of it). ``langs``: the
    tongues that HAVE a page, so the sibling set names only pages that exist."""
    canonical = f"{site_url}/{about_path(lang, fallback)}"
    # every sibling named for a crawler, plus x-default on the fallback page (INV-102)
    alts = "".join(
        f'<link rel="alternate" hreflang="{esc(L)}" '
        f'href="{esc(site_url)}/{about_path(L, fallback)}">\n' for L in langs)
    if langs:
        alts += (f'<link rel="alternate" hreflang="x-default" '
                 f'href="{esc(site_url)}/{about_path(fallback, fallback)}">\n')
    title = (about.get("about_title") or "").strip()
    paras = [(about.get(k) or "").strip() for k in ABOUT_PARA_KEYS]
    paras = [p for p in paras if p]
    back = (about.get("about_back") or "").strip()
    desc = paras[0] if paras else title
    jsonld = {
        "@context": "https://schema.org",
        "@type": "AboutPage",
        "name": title,
        "url": canonical,
        "isPartOf": f"{site_url}/",
        "about": {"@type": "CollectionPage", "name": COLLECTION_NAME, "url": f"{site_url}/"},
        "author": {"@type": "Person", "name": CREATOR},
    }
    body_paras = "".join(f"<p>{esc(p)}</p>\n" for p in paras)
    # the return control (EX-ABOUT / INV-102/103): a real anchor to "/" so the page works with
    # scripting off. The inline script upgrades a same-site arrival into a step back through the
    # visitor's OWN history; a direct or external arrival still follows the address to "/". It
    # stands at the TOP of the page, above the heading, in the page's own flow. The script stays
    # under 500 bytes and is inert when the control itself is absent (no `back` word).
    back_ctl = (f'<a class="about-back" id="about-back" href="/">{esc(back)}</a>\n' if back else "")
    back_script = (
        '<script>(function(){var a=document.getElementById("about-back");if(!a)return;'
        'a.addEventListener("click",function(e){if(document.referrer.indexOf(location.origin+"/")===0'
        '&&history.length>1){e.preventDefault();history.back();}});'
        '["pointerdown","pointerup","pointercancel","pointerleave"].forEach(function(t){'
        'a.addEventListener(t,function(){a.classList.toggle("is-press",t==="pointerdown");});});'
        '})();</script>\n'
        if back else "")
    body = f"""<body>
<main class="wrap about">
{back_ctl}<h1>{esc(title)}</h1>
{body_paras}<p class="sign">{COPYRIGHT_NO_ABOUT}</p>
{back_script}</main>
</body>
</html>
"""
    return head(title, desc, canonical, "", "article", jsonld,
                extra_og=alts, extra_head='<meta name="robots" content="index,follow">\n',
                lang=lang, direction=direction) + body


# ---------------------------------------------------------------- bundle

MARK_FONT = "/System/Library/Fonts/Supplemental/Arial.ttf"


def _stamp(im, text):
    """Draw a small tidy mark bottom-right — the site host, bone ~40% over a soft shadow
    (EX-PROTECT-RES / INV-56). A grabbed image carries the site's name."""
    from PIL import ImageDraw, ImageFont
    w, h = im.size
    draw = ImageDraw.Draw(im, "RGBA")
    size = max(13, int(w * 0.020))
    try:
        font = ImageFont.truetype(MARK_FONT, size)
    except Exception:
        font = ImageFont.load_default()
    box = draw.textbbox((0, 0), text, font=font)
    tw = box[2] - box[0]
    pad = int(w * 0.018)
    x = w - tw - pad
    y = h - (box[3] - box[1]) - pad - box[1]
    draw.text((x + 1, y + 1), text, font=font, fill=(0, 0, 0, 80))      # soft shadow
    draw.text((x, y), text, font=font, fill=(235, 231, 222, 105))       # bone, ~40%


# EX-LADDER (INV-63): the responsive-image ladder — DOWNSCALE ONLY from the display source. Alongside
# each served base image the bake writes `<id>-640/-960/-1280.<ext>`, all CLEAN (no mark — the mark
# rides only a taken copy / the prize). The browser picks a tier by viewport×DPR: a phone pulls 640
# (fast), a wide/retina screen pulls 1280 (sharp). Tiers + srcset join ONLY when the display cap runs
# (deploy); a no-cap bake (tests) is byte-identical to a ladder-less walk.
DISPLAY_TIERS = (640, 960, 1280)
# Each surface that hangs a work wears the `sizes` its own CSS box asks for. A door window's box is
# the layout's live size, so that one is written at render time rather than baked here.
WALK_SIZES = "88vw"          # the walk's img — CSS max-width:88vw
LANE_SIZES = "64vw"          # a series lane picture — CSS max-width:64vw
PRINT_SIZES = "(max-width:640px) 110px, 150px"   # a polaroid on the table — the clamp's own ceiling


WORK_SIZES = "(min-width: 800px) 760px, 100vw"


def served_dims(w, h, cap):
    """The dimensions the bundle actually serves — the display cap applied (INV-56), aspect kept — so
    the OG image hints match the served bytes. No cap, or already within it ⇒ the original dims."""
    try:
        w, h = int(w), int(h)
    except (TypeError, ValueError):
        return w, h
    if not cap or max(w, h) <= cap:
        return w, h
    if w >= h:
        return cap, max(1, round(h * cap / w))
    return max(1, round(w * cap / h)), cap


def tier_url(img_rel, w):
    """'<dir>/<id>.jpg' → '<dir>/<id>-<w>.jpg' (EX-LADDER). The base file stays the untouched fallback."""
    stem, dot, ext = img_rel.rpartition(".")
    return f"{stem}-{w}.{ext}" if dot else img_rel


def srcset_of(img_rel):
    """The srcset string over the 640/960/1280 ladder for a served image path (EX-LADDER). The tier
    files are written by the display-cap copy path (deploy); no cap ⇒ this is never emitted."""
    return ", ".join(f"{tier_url(img_rel, w)} {w}w" for w in DISPLAY_TIERS)


def _copy_assets_capped(asrc, adst, cap, mark_text=None):
    """Copy the gallery images into the bundle, downscaling any whose LONG EDGE exceeds cap
    (PIL / Pillow, LANCZOS) and, when mark_text is given, stamping a small bottom-right site
    mark on the BASE file (EX-PROTECT-RES / INV-56). Alongside each base image it writes the
    responsive ladder tiers `<id>-640/-960/-1280.<ext>` — DOWNSCALE ONLY (a smaller source is never
    upscaled) and always CLEAN, no mark (EX-LADDER / INV-63). A smaller image is not upscaled;
    non-images copy verbatim. The repo originals are untouched — only the served copy is capped/marked."""
    from PIL import Image
    for p in sorted(asrc.rglob("*")):
        if p.is_dir():
            continue
        out = adst / p.relative_to(asrc)
        out.parent.mkdir(parents=True, exist_ok=True)
        if p.suffix.lower() in (".jpg", ".jpeg", ".png"):
            src_im = Image.open(p).convert("RGB")
            # the ladder tiers first — each downscaled from the SOURCE (best quality per width), CLEAN,
            # progressive; thumbnail never upscales, so a tier's long edge is ≤ its nominal width.
            for w in DISPLAY_TIERS:
                tier = src_im.copy()
                if max(tier.size) > w:
                    tier.thumbnail((w, w), Image.LANCZOS)
                tier.save(out.with_name(f"{out.stem}-{w}{out.suffix}"), quality=84, progressive=True)
            # the base fallback file — capped to the display cap, marked only if asked (never a tier)
            base = src_im
            if max(base.size) > cap:
                base.thumbnail((cap, cap), Image.LANCZOS)
            if mark_text:
                _stamp(base, mark_text)
            base.save(out, quality=88)
        else:
            shutil.copy2(p, out)


def copy_gallery(display_max=None, mark_text=None):
    """Copy the shared images + design tokens into the bundle (self-contained, INV-18). The old
    Room/Door prototypes are RETIRED — the exhibition (EX) is now the single converged front door,
    so no prototype HTML ships; only the assets and the shared tokens the exhibition renders in.
    display_max: cap the served images' long edge (px) — the deploy passes it, tests bake verbatim
    (no cap) so they stay fast. Originals untouched; only the bundle copy is capped and marked."""
    dst = OUT / "gallery"
    src = ROOT / "gallery"
    (dst).mkdir(parents=True, exist_ok=True)
    if (src / "gallery_data.json").exists():
        shutil.copy2(src / "gallery_data.json", dst / "gallery_data.json")
    # shared = design tokens · audio = the ambient loop the sound player fetches on turn-on (EX-SOUND)
    for sub in ("shared", "audio"):
        if (src / sub).exists():
            shutil.copytree(src / sub, dst / sub, dirs_exist_ok=True)
    if (src / "assets").exists():
        if display_max:
            _copy_assets_capped(src / "assets", dst / "assets", int(display_max), mark_text=mark_text)
        else:
            shutil.copytree(src / "assets", dst / "assets", dirs_exist_ok=True)


def _clamp_int(x, dflt, lo, hi):
    """The same clamp the client applies to a feel-knob (clampInt in engine/client/01-knobs-lang-
    history.js), read back here so a number derived from a knob — the walk's own records cap, below
    — never drifts from what the walk itself will actually deal (2026-08-19). A knob absent or not a
    number falls back to `dflt`; a knob present is clamped into [lo, hi], exactly as the client
    clamps the SAME config value at read time."""
    try:
        n = int(x)
    except (TypeError, ValueError):
        try:
            n = int(float(x))
        except (TypeError, ValueError):
            return dflt
    return max(lo, min(hi, n))


def pass_capabilities():
    """EX-PASS §4.4d — THE CLIENT'S OWN LIMITS, PUBLISHED SO THE COMPOSER CAN MEASURE AGAINST THEM.

    A limit is part of the client's CAPABILITY: raising one is a rebuild, never a setting, and the
    one home of the number is the `PASS_LIMITS` literal in engine/client/01a-pass.js. A site that
    composes scores has to know what the client will accept — a score written past the fence is
    refused before any instrument sees it, and the composer that wrote it never hears — so the
    number is READ BACK OUT of the served client here and written into the settings record. Reading
    it rather than restating it is what keeps the published number and the applied number one
    number; a second copy could only drift.

    `scoreBytes` is the whole weight a score may have, measured the way passScoreCheck measures it:
    the length of the score written out as JSON. It is an observed baseline with its evidence, and
    the evidence stands beside the literal it is read from.

    `intentChars` is the length of the ONE field §4.4 calls prose — the authored line a score opens
    with — and it is published here for the same reason and by the same road, added 2026-08-17 (U27
    stage 1). A score whose intent runs past it is refused WHOLE, with «intent is no short text», and
    stage 0 found what an unmeasured prose fence costs: 1 004 of 6 304 composed crossings wrote a
    line longer than the 400 the client then applied, and every one of them was refused before an
    instrument saw it. The client's cap was raised to 600 on that finding. The composer that writes
    the line could not measure it, because the number reached the settings record nowhere; now it
    does, and the number the composer measures against and the number the client applies are one
    number rather than two copies. A composer handed no capability falls back to what the client
    applies today, which is a fallback and not a second home."""
    src = client_asset("exhibition.js").read_text(encoding="utf-8")
    found = re.search(r"PASS_LIMITS\s*=\s*\{[^}]*\bbytes:\s*(\d+)", src)
    if not found:
        raise SystemExit("engine/assets/exhibition.js declares no PASS_LIMITS.bytes — the site has "
                         "no score fence to measure against")
    prose = re.search(r"PASS_LIMITS\s*=\s*\{[^}]*\bintent:\s*(\d+)", src)
    if not prose:
        raise SystemExit("engine/assets/exhibition.js declares no PASS_LIMITS.intent — the site has "
                         "no fence on a score's authored line to measure against")
    return {"scoreBytes": int(found.group(1)), "intentChars": int(prose.group(1))}


def client_asset(name):
    """One client source file (exhibition.js/css, the worker template): the INSTANCE's own copy
    wins when its assets dir carries one — an instance that grew its client first keeps shipping
    it byte-exact while the generic client serves everyone else. Engine's own copy otherwise."""
    cand = _INSTANCE_ASSETS / name if _INSTANCE_ASSETS else None
    return cand if (cand and cand.exists()) else _ENGINE_ASSETS / name


# The instrument record this bake produced: name → {src, version, digest}, filled by
# copy_exhibition_assets and read at the config assembly. One home for one fact.
_PASS_INSTRUMENTS = {}


def _pass_instrument_sources():
    """Every instrument file that ships, one path each. An instrument the INSTANCE carries wins over
    the engine's own copy of the same name, which is client_asset's rule applied file by file; an
    instrument only the instance carries ships too, so a site can bring instruments of its own."""
    names = {}
    for d in (_ENGINE_ASSETS, _INSTANCE_ASSETS):
        if not d:
            continue
        for p in d.glob("pass-inst-*.js"):
            names[p.name] = p
    return list(names.values())


def apply_namespace(text, ns):
    """Resolve the client's namespace tokens to the instance's namespace (EX-NS). The engine client
    carries its namespace-bearing literals as tokens — storage-key prefix ``@@NS@@.``, hyphen key
    ``@@NS@@-``, perf-mark prefix ``@@NS@@:`` with its strip length ``@@NS_MARK_LEN@@`` (len(ns)+1,
    for the trailing colon — derived, never hardcoded), window globals ``@@NS_UPPER@@*`` / ``__@@NS@@*``,
    and the history-state key ``@@NS@@``. DOM ids/CSS classes are NOT tokenized (both instances share
    them). An instance client that ships its own copy has no tokens, so this is a byte no-op on it."""
    return (text.replace("@@NS_MARK_LEN@@", str(len(ns) + 1))
                .replace("@@NS_UPPER@@", ns.upper())
                .replace("@@NS@@", ns))


def strip_css_comments(css):
    """Drop /* ... */ comments from the SERVED stylesheet — they are inert to the browser, so the
    visitor downloads only the rules. The source keeps every comment; only this build copy is
    stripped (the byte-budget fence measures this same stripped output, so it guards real rules, not
    prose). A string literal ('...' / "...") is honoured, so a `content` value that bears /* is
    never mistaken for a comment. Blank lines the strip leaves behind are collapsed."""
    out = []
    i, n, quote = 0, len(css), None
    while i < n:
        c = css[i]
        if quote:
            out.append(c)
            if c == "\\" and i + 1 < n:                 # an escaped char rides whole
                out.append(css[i + 1]); i += 2; continue
            if c == quote:
                quote = None
            i += 1; continue
        if c in "\"'":
            quote = c; out.append(c); i += 1; continue
        if c == "/" and i + 1 < n and css[i + 1] == "*":
            j = css.find("*/", i + 2)
            i = (j + 2) if j != -1 else n               # an unterminated comment drops the tail
            continue
        out.append(c); i += 1
    stripped = "".join(out)
    stripped = re.sub(r"[ \t]+(\n)", r"\1", stripped)   # trailing whitespace off each line
    stripped = re.sub(r"\n{3,}", "\n\n", stripped)      # a run of blank lines → one
    return stripped


def _pattern_end(js, start):
    """The index just past a regular-expression literal opening at ``start``, or None when the run
    is not one after all (no closing `/` before the line ends — patterns never span lines, so that
    `/` was a division). A `[...]` class holds its own `/`; an escape rides whole; flags ride too."""
    i, n, in_class = start + 1, len(js), False
    while i < n:
        c = js[i]
        if c == "\\":
            i += 2; continue
        if c == "\n":
            return None
        if c == "[":
            in_class = True
        elif c == "]":
            in_class = False
        elif c == "/" and not in_class:
            i += 1
            while i < n and js[i].isalpha():
                i += 1
            return i
        i += 1
    return None


def strip_js_comments(js):
    """Drop the client's own prose from the SERVED script — it is inert to the browser, so the
    visitor downloads only the code. The source keeps every comment; only this build copy is
    stripped, and the byte-budget fence measures this same stripped output, so the fence guards real
    code rather than explanation. The same lever the stylesheet already rides (strip_css_comments,
    2026-07-23), applied to the bigger of the two files.

    A `/*! ... */` comment is KEPT — the long-standing convention for a marker that must survive
    minification. The assembler writes one per client fragment, so a string-level test can scope
    itself to a fragment's own region by structure instead of by hunting a sentence in prose.

    Deliberately conservative: only a comment that OPENS its line — the first non-whitespace on it —
    is dropped, whole. A trailing `// ...` after code is copied VERBATIM, so an apostrophe inside it
    can never be read as the start of a string. Quotes, template literals and regular-expression
    literals are all tracked: a line inside a template that happens to begin with `//` (a URL, say)
    is never mistaken for a comment, and a quote character inside a pattern like `/[<>&"]/` never
    opens a string. A `/` is read as a pattern only where an expression may begin — after an
    operator, an opening bracket, a separator, or one of the keywords that take one."""
    # where a `/` opens a pattern rather than dividing
    RE_OK_CHARS = set("(,=:[!&|?{};+-*%~^<>\n")
    RE_OK_WORDS = ("return", "typeof", "instanceof", "in", "of", "new", "delete", "void",
                   "case", "do", "else", "yield", "await")
    out = []
    i, n, quote, line_start = 0, len(js), None, True
    prev = ""                                           # last significant character emitted as code

    def pattern_may_open():
        if not prev or prev in RE_OK_CHARS:
            return True
        if prev.isalnum() or prev in "_$":              # an identifier or a number — division,
            tail = "".join(out)[-16:]                   # unless the identifier is a keyword
            word = re.search(r"([A-Za-z_$]+)\s*$", tail)
            return bool(word and word.group(1) in RE_OK_WORDS)
        return False

    while i < n:
        c = js[i]
        if quote:
            out.append(c)
            if c == "\\" and i + 1 < n:                 # an escaped char rides whole
                out.append(js[i + 1]); i += 2; continue
            if c == quote:
                quote = None
            i += 1; continue
        if c in "\"'`":
            quote = c; out.append(c); i += 1; line_start = False; continue
        if c == "\n":
            out.append(c); i += 1; line_start = True; continue
        if line_start and c in " \t":
            out.append(c); i += 1; continue
        if c == "/" and i + 1 < n and js[i + 1] == "/":
            j = js.find("\n", i)
            end = n if j == -1 else j
            if line_start:                              # the whole line is prose — drop it
                while out and out[-1] in " \t":
                    out.pop()                           # its indent goes with it
                i = n if j == -1 else j + 1
            else:                                       # trailing prose stays, copied VERBATIM so a
                out.append(js[i:end])                   # `don't` inside it never opens a string
                i = end
            continue
        if c == "/" and i + 1 < n and js[i + 1] == "*":
            j = js.find("*/", i + 2)
            end = n if j == -1 else j + 2               # an unterminated comment drops the tail
            if js[i + 2:i + 3] == "!":                  # a keep-marker rides through untouched
                out.append(js[i:end]); i = end; line_start = False; continue
            if line_start:
                while out and out[-1] in " \t":
                    out.pop()
                i = end
                while i < n and js[i] in " \t":
                    i += 1
                if i < n and js[i] == "\n":
                    i += 1
                continue
            out.append(js[i:end])                       # trailing block comment, verbatim
            i = end
            line_start = False
            continue
        if c == "/" and pattern_may_open():
            end = _pattern_end(js, i)                   # a regular-expression literal, copied whole
            if end is not None:
                out.append(js[i:end])
                i = end; line_start = False; prev = "/"
                continue
        out.append(c); i += 1; line_start = False
        if not c.isspace():
            prev = c
    stripped = "".join(out)
    stripped = re.sub(r"[ \t]+(\n)", r"\1", stripped)   # trailing whitespace off each line
    stripped = re.sub(r"\n{3,}", "\n\n", stripped)      # a run of blank lines → one
    return stripped


def copy_exhibition_assets():
    """The exhibition client (JS+CSS) — instance override first, engine's own otherwise (see
    client_asset); favicons from the instance's assets dir (absent → the bundle simply has none).
    The served JS is passed through the namespace substitution (EX-NS): the engine client's tokens
    resolve to the instance's namespace; a token-free instance client is byte-copied unchanged.
    Both files are comment-stripped on the way out (strip_js_comments / strip_css_comments): the
    visitor gets code and rules only, the source stays fully commented."""
    js_path = client_asset("exhibition.js")
    js_src = js_path.read_text(encoding="utf-8")
    if "@@NS@@" in js_src or "@@NS_UPPER@@" in js_src:
        js_src = apply_namespace(js_src, _NAMESPACE)
    write(OUT / "exhibition.js", strip_js_comments(js_src))
    css_src = client_asset("exhibition.css").read_text(encoding="utf-8")
    write(OUT / "exhibition.css", strip_css_comments(css_src))
    # EX-PASS: the drawing layer travels as its own file, fetched by the client only when a walk
    # asks for it. Absent from the assets dir, the bundle simply has none and every transition
    # rides the walk's own glide.
    #
    # EVERY INSTRUMENT TRAVELS AS ITS OWN FILE, AND THE SITE'S RECORD NAMES WHAT EXISTS (§7). The
    # engine knows no effect name, so nothing here is stamped into the host: the host is told
    # neither an address nor a name at bake. What the bake produces instead is a RECORD — one entry
    # per instrument, keyed by the instrument's own name, carrying the address the file is served
    # at, the version it declares and the digest its served bytes weigh to. That record joins the
    # site's own `pass` block in config.json (see the `pass` seam at the config assembly below),
    # which is the same block that already carries the score tables and the score templates. A cue
    # names an instrument, the host looks the name up in the record, and fetches that one file.
    #
    # WHY ONE FILE EACH. One file holding the farm makes a visit pay for twenty-five instruments to
    # see one crossing, and it makes one byte fence answer for a number nobody can act on. One file
    # per instrument makes the fence the honest unit and makes a visit pay for its own passage.
    #
    # THE FILE'S NAME IS THE INSTRUMENT'S NAME, and it is read from the file name alone — the source
    # `pass-inst-<name>.js` serves as `pass-inst-<name>.js` and is recorded under `<name>`. The host
    # refuses a file whose instrument declares a different name than the one it was fetched for, so
    # a file name and the instrument inside it cannot drift apart unnoticed.
    #
    # The version has one home, each file's own `INSTRUMENT_VERSION` literal, read back out here.
    # The digest is taken over the bytes actually written, never over the source: a digest over a
    # file no visitor fetches would weigh the wrong thing.
    global _PASS_INSTRUMENTS
    _PASS_INSTRUMENTS = {}
    for inst_path in sorted(_pass_instrument_sources()):
        name = inst_path.name[len("pass-inst-"):-len(".js")]
        inst_src = inst_path.read_text(encoding="utf-8")
        found = re.search(r'var\s+INSTRUMENT_VERSION\s*=\s*"([^"]+)"', inst_src)
        if not found:
            raise SystemExit("%s declares no INSTRUMENT_VERSION — the site has no version to pin"
                             % inst_path.name)
        if "@@NS@@" in inst_src or "@@NS_UPPER@@" in inst_src:
            inst_src = apply_namespace(inst_src, _NAMESPACE)
        write(OUT / inst_path.name, strip_js_comments(inst_src))
        _PASS_INSTRUMENTS[name] = {
            "src": inst_path.name,
            "version": found.group(1),
            "digest": hashlib.sha256((OUT / inst_path.name).read_bytes()).hexdigest(),
        }

    # EX-PASS §4.4d: the passage composer travels the same way — its own file, fetched by the bundle
    # once per visit at the walk's first landing, on a walk whose settings record actually carries
    # the per-work records it reads. A bake without it simply serves none, the bundle's fetch answers
    # 404, the refusal lands on the diagnostic surface and every crossing keeps the walk's own glide.
    for _name in ("pass-layer.js", "pass-composer.js", "darkroom-measure.js"):
        _p = client_asset(_name)
        if not _p.exists():
            continue
        _src = _p.read_text(encoding="utf-8")
        if "@@NS@@" in _src or "@@NS_UPPER@@" in _src:
            _src = apply_namespace(_src, _NAMESPACE)
        write(OUT / _name, strip_js_comments(_src))
    for name in ("favicon.svg", "favicon.png", "apple-touch-icon.png"):
        cand = _INSTANCE_ASSETS / name if _INSTANCE_ASSETS else None
        if cand and cand.exists():
            shutil.copy2(cand, OUT / name)


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def door_pool(items_by_id, captions, diverse=False, place_keywords=None):
    """The door pool (EX-DOOR): the door-candidates provenance ids intersected with the LIVING
    gallery works — an id that left the gallery silently drops out. Each entry carries the alt
    text a door work needs (his title → caption → quiet label; the door asks wordlessly, but a
    keyboard/screen-reader visitor still meets real words). Returns [] when the source is absent.

    With ``diverse`` ON (EX-DOOR-3, the door_diversity flag) the pool spans the WHOLE living gallery
    instead of the curated candidates: each entry carries the FIVE spread axes
    (luma/warmth/colorful/edge/sym) and a ``place`` flag (the work's city matches the instance's
    place group — ``place_keywords`` from site.json, matched case-insensitively as substrings), so
    the client deals a fresh, evenly-spread, place-guaranteed set every open. Data, never rendered
    (INV-1). OFF → the curated candidates below, byte-identical."""
    if diverse:
        kws = [k.lower() for k in (place_keywords or [])]
        pool = []
        for item in sorted(items_by_id.values(), key=lambda i: i["id"]):   # deterministic (INV-21)
            cap = captions.get(item["id"], "")
            city = (item.get("city") or "").lower()
            pool.append({"id": item["id"], "alt": indexable_title(item, cap),
                         "luma": round(float(item.get("luma", 0.5)), 3),
                         "warmth": round(float(item.get("warmth", 0.5)), 3),
                         "colorful": round(float(item.get("colorful", 0.5)), 3),
                         "edge": round(float(item.get("edge", 0.5)), 3),
                         "sym": round(float(item.get("sym", 0.5)), 3),
                         "place": bool(city and any(k in city for k in kws))})
        return pool
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


def quiz_load():
    """EX-QUIZ-PICK (INV-64/66): the per-work quiz data, an OPTIONAL, INSTANCE-OWNED file. The
    engine hardcodes no work id and no answer — an instance supplies `<content>/quiz.json`:

        {"quizzes": {"<workid>": {"prompt": "…", "options": ["A","B","C","D"],
                                  "answer": "A", "prize": "gallery/<file>"}}}

    Returns {id: entry}. The PUBLIC half (prompt + options[4]) rides the walk's baked data; the
    PRIVATE half (single answer + prize path) is baked only INTO _worker.js and only when the quiz
    ships — so the answer never becomes a public byte. The old free-text fields (hints, accept) are
    RETIRED (INV-64 supersedes them). Absent/malformed → {}: quiz on but no data ⇒ the walk is
    byte-identical (no quiz key on any work, QUIZ_ANSWERS stays {} and the route 404s, INV-60)."""
    src = ROOT / "quiz.json"
    try:
        raw = json.loads(src.read_text(encoding="utf-8"))
    except Exception:
        return {}
    quizzes = raw.get("quizzes", raw) if isinstance(raw, dict) else {}
    out = {}
    for wid, q in quizzes.items():
        if not isinstance(q, dict):
            continue
        out[str(wid)] = q
    return out


def _bake_quiz_prizes(quiz_private, site_url):
    """EX-QUIZ-PRIZE (EX-PROTECT-RES / INV-56): bake the prize wallpaper derivative for each quiz
    work — a display-grade copy of the work with the site host stamped bottom-right (the same mark
    the grab-download and the served cap use). The print master NEVER enters the bundle; only the
    baked derivative ships (INV-18). Source is the already-baked gallery derivative (the web-size
    copy) when present, else the repo original. Pillow absent → verbatim copy (still a derivative).
    mark_text is the site host, exactly like the served-image cap (site-driven, never a literal)."""
    gallery_data = json.loads((ROOT / "gallery" / "gallery_data.json").read_text(encoding="utf-8"))
    items_by_id = {str(it["id"]): it for it in gallery_data["items"]}
    mark_text = re.sub(r"^https?://", "", site_url).rstrip("/")
    for work_id, priv in sorted(quiz_private.items()):
        prize_path = priv.get("prize", "")
        if not str(prize_path).startswith("gallery/"):
            continue
        item = items_by_id.get(str(work_id))
        if not item:
            continue
        src_img = OUT / "gallery" / item["img"]
        if not src_img.exists():
            src_img = ROOT / "gallery" / item["img"]
        if not src_img.exists():
            continue
        dst = OUT / prize_path
        dst.parent.mkdir(parents=True, exist_ok=True)
        try:
            from PIL import Image
            im = Image.open(src_img).convert("RGB")
            _stamp(im, mark_text)
            im.save(dst, quality=88)
        except Exception:
            shutil.copy2(src_img, dst)


def build(site_url, ga_id="", enable=None, content_dir=None, out_dir=None,
          engine_assets_dir=None, instance_assets_dir=None, site_config=None,
          display_max=None):
    """``enable``: flag names switched ON for this bake; every worker flag ships false by
    default, the flip is a deploy argument. Identity comes from site.json — the engine knows
    no instance. ``display_max``: cap the served images' long edge (px) — the deploy passes it,
    tests omit it so the bake stays fast (EX-PROTECT-RES / INV-56)."""
    # EX-BUNDLE-FRESH: reassemble engine/assets/exhibition.js from its engine/client/ fragments
    # before anything else in the bake reads it — client_asset() below falls back to exactly
    # this file. Before this call the served bundle could silently go stale relative to its own
    # fragments: a real incident shipped an hours-stale bundle because nobody remembered to
    # re-run `python engine/assemble_client.py` by hand after a fragment fix. Calling assemble()
    # directly (not assemble_client.main()) skips its argparse, which would otherwise collide
    # with this script's own CLI args. Idempotent — a bake over unchanged fragments writes back
    # the same bytes — so every bake, test or deploy, always serves its own fragments fresh.
    assemble_client.OUT_PATH.write_text(assemble_client.assemble(), encoding="utf-8")
    global GA_ID, OUT, ROOT, CREATOR, SITE_NAME, ROOT_TITLE, ROOT_DESCRIPTION
    global COLLECTION_NAME, LOADING_LINE, COPYRIGHT, COPYRIGHT_NO_ABOUT
    global _ENGINE_ASSETS, _INSTANCE_ASSETS, _NAMESPACE
    global HINT_LINE, OG_IMAGE_ID
    GA_ID = ga_id
    OUT = out_dir
    ROOT = content_dir
    _ENGINE_ASSETS = engine_assets_dir
    _INSTANCE_ASSETS = instance_assets_dir
    # EX-NS: the instance's namespace for storage keys / globals / perf marks / history-state. The
    # engine's own example bakes under "ex" (default); an instance declares its own in site.json.
    _NAMESPACE = (site_config.get("namespace") or "ex").strip()
    SITE_NAME = site_config["site_name"]
    CREATOR = site_config["creator"]
    ROOT_TITLE = site_config["root_title"]
    ROOT_DESCRIPTION = site_config["root_description"]
    COLLECTION_NAME = site_config["collection_name"]
    LOADING_LINE = site_config.get("loading_line") or "loading the exhibition"
    # The one-line subtitle under the site name on the crawlable JS-off face. Instance copy since
    # 1.14.0; the engine's own words stand for an instance that names none.
    HINT_LINE = site_config.get("hint_line") or "an exhibition that assembles itself around you"
    OG_IMAGE_ID = site_config.get("og_image_id") or ""
    # The copy dictionary is read HERE, before the signature is composed and before any page is
    # written, because the signature's about link is a word FROM it (EX-ABOUT / INV-103).
    greet = greetings()
    about_set = about_langs(greet)
    about_word = ""
    if about_set:
        fb = greet["fallback"]
        about_word = (greet["langs"][fb].get("about") or "").strip()
    _year = datetime.date.today().year
    # two signatures, one law: the STATIC faces carry the about link, the client artifact does
    # not — the walk's closing screen has its own about line in the visitor's own tongue, and two
    # doors to one page side by side is what INV-103 forbids.
    COPYRIGHT = compose_sign(_year, CREATOR, SITE_NAME,
                             site_config.get("instagram"), about_word=about_word)
    COPYRIGHT_NO_ABOUT = compose_sign(_year, CREATOR, SITE_NAME,
                                      site_config.get("instagram"))
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
        slug, doc = render_work(it, cap, pal, site_url, display_max=display_max)
        slugs[it["id"]] = slug
        write(OUT / "w" / f"{slug}.html", doc)

    # the exhibition root `/` (EX) — crawlable JS-off face + the client walk
    write(OUT / "index.html", render_exhibition(items, captions, slugs, site_url, display_max=display_max))

    # the about page (EX-ABOUT / INV-102): one flat page per tongue that HAS copy, the fallback at
    # the bare `/about`. No copy in the fallback tongue ⇒ about_set is empty ⇒ nothing here runs
    # and the bundle is byte-identical to a bake without the feature.
    for lang in about_set:
        blk = greet["langs"][lang]
        write(OUT / f"{about_path(lang, greet['fallback'])}.html",
              render_about(site_url, blk, lang, about_set, greet["fallback"],
                           direction="rtl" if blk.get("dir") == "rtl" else ""))

    copy_exhibition_assets()

    # the client walk's baked data: per-work normalized kinship vectors (neutral coords, INV-1) +
    # a lean work list (id, image, its /w/ slug, dims, dominant colour for the reactive ground)
    vectors, ex_version = exhibition_vectors(load_json("vector.json")["items"])
    # EX-STORY-ORDER (INV-47): the authored light marks lean the told story's order (a work reads as
    # a SET, `free` = unconstrained). OPTIONAL instance data — absent → every work is `free`, the
    # light-lean a no-op and the arc unchanged (the byte-identical guard, ST1). Data, never rendered.
    tod_marks = tod_marks_load()
    tod_of = lambda wid: (tod_marks.get(str(wid), {}) or {}).get("marks") or ["free"]
    # EX-QUIZ-PICK (INV-64/66): the instance's per-work quiz data (optional). Split here: the PUBLIC
    # prompt+options[4] ride the walk (below), the PRIVATE single answer+prize go only into _worker.js.
    # The old free-text fields (hints, accept) are RETIRED — INV-64 supersedes them.
    quiz_all = quiz_load()
    quiz_public = {wid: {"prompt": q.get("prompt", ""), "options": list(q.get("options", []))}
                   for wid, q in quiz_all.items()
                   if q.get("prompt") and isinstance(q.get("options"), list) and len(q["options"]) == 4}
    quiz_private = {wid: {"answer": q.get("answer", ""), "prize": q.get("prize", "")}
                    for wid, q in quiz_all.items() if q.get("answer") and q.get("prize")}
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
        # N7-A11Y (OS-A2 / CS-5 / INV-102): each walk record carries the work's accessible description —
        # the SAME string its /w page + the static-index alt render (`captions[id]`, else the indexable
        # title). The client's one alt helper reads this at every img site; never rendered as visible copy.
        "desc": captions.get(it["id"], "") or indexable_title(it, captions.get(it["id"], "")),
        "tod": tod_of(it["id"]),             # the light marks (EX-STORY-ORDER) — data, never rendered
    } for it in items]
    # EX-QUIZ-PICK (INV-64/60): the public quiz data joins only when the quiz flag is on; flag off →
    # no quiz key on any work, the walk is byte-identical to a quiz-less walk. PUBLIC prompt +
    # options[4] only — no answer, no prize path, no hints (INV-64 supersedes the hint trail).
    if flags["quiz"]:
        for w in ex_works:
            q = quiz_public.get(str(w["id"]))
            if q:
                w["quiz"] = q                # PUBLIC prompt + options only — no answer, no prize
    # EX-LADDER (INV-63): the responsive srcset joins each work only when the display cap runs (the
    # deploy, which also writes the tier files) — no cap ⇒ no srcset key, the walk data is byte-identical.
    if display_max:
        for w in ex_works:
            w["srcset"] = srcset_of(w["img"])
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
              # the walk's own face signs off with the same composed line (EX-COPY) — WITHOUT the
              # about link, because the closing screen carries its own (INV-103)
              "copyright": COPYRIGHT_NO_ABOUT,
              "v": {it["id"]: vectors[it["id"]] for it in items if it["id"] in vectors},
              # the threshold's pool ships INSIDE this one artifact — one fetch, under the same
              # bounded arrival INV-25 grants the walk (EX-DOOR; prover F1)
              "door": {"pool": door_pool(
                  {it["id"]: it for it in items}, captions,
                  diverse=flags["door_diversity"],
                  place_keywords=(site_config.get("door_diversity") or {}).get("place_keywords"))}}
    # the greeting rides the SAME artifact — one fetch, INV-25's bounded arrival (EX-GREET).
    # The about PAGE copy is stripped on the way out (INV-104): the client reads exactly one word
    # of it — the entry word its closing screen puts on the link — and prose no code reads is
    # weight on the one artifact every visitor fetches before the first picture hangs.
    if greet:
        client_greet = dict(greet)
        client_greet["langs"] = {
            L: {k: v for k, v in blk.items() if k not in ABOUT_PAGE_KEYS}
            for L, blk in greet["langs"].items()}
        exdata["greet"] = client_greet
    # the tongues that HAVE a page, so the closing screen can link the visitor's own (INV-103)
    if about_set:
        exdata["about"] = {"fallback": greet["fallback"], "langs": about_set}
    # EX-LADDER (INV-63): the `sizes` each hanging surface wears — joins only alongside the per-work
    # srcset (i.e. when the display cap runs), so a no-cap bake stays byte-identical.
    if display_max:
        exdata["walk_sizes"] = WALK_SIZES
        exdata["lane_sizes"] = LANE_SIZES
        exdata["print_sizes"] = PRINT_SIZES
    write(OUT / "exhibition_data.json",
          json.dumps(exdata, ensure_ascii=False, indent=0, sort_keys=True) + "\n")

    # sitemap: exhibition root + every work page, each once; each carries a <lastmod> (the bake date, so
    # a fresh deploy re-dates the map) + its photograph as an <image:image> for Google Images (INV-53)
    lastmod = datetime.date.today().isoformat()
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"'
          ' xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">',
          f"  <url><loc>{esc(site_url)}/</loc><lastmod>{lastmod}</lastmod></url>"]
    for it in items:
        wu = f"{site_url}/w/{slugs[it['id']]}"
        img = f"{site_url}/gallery/{it['img']}"
        sm.append(f"  <url><loc>{esc(wu)}</loc><lastmod>{lastmod}</lastmod>"
                  f"<image:image><image:loc>{esc(img)}</image:loc></image:image></url>")
    # the about pages join the map once each — no <image:image>, since no picture stands on them
    for lang in about_set:
        au = f"{site_url}/{about_path(lang, greet['fallback'])}"
        sm.append(f"  <url><loc>{esc(au)}</loc><lastmod>{lastmod}</lastmod></url>")
    sm.append("</urlset>")
    write(OUT / "sitemap.xml", "\n".join(sm) + "\n")

    # robots: preview host is closed entirely; production welcomes SEARCH crawlers (his traffic)
    # AND the AI SEARCH/answer bots that retrieve to cite a live query (so the exhibition can be
    # found and cited by ChatGPT/Perplexity), but blocks AI-TRAINING scrapers from harvesting the
    # photographs into model datasets (his protection stance — pairs with the mark-split/gift
    # ceremony). Regular search bots (Googlebot/Bingbot/…) stay allowed under "*"; so do the
    # retrieval bots, which are simply left OFF the block list below.
    is_preview = "pages.dev" in site_url
    if is_preview:
        robots = f"User-agent: *\nDisallow: /\nSitemap: {site_url}/sitemap.xml\n"
    else:
        # AI-TRAINING crawlers — feed a model's training set → blocked (protect the photographs).
        # The retrieval/answer bots that only fetch to cite a live query (ChatGPT-User,
        # OAI-SearchBot, PerplexityBot) are deliberately NOT here, so "*" allows them.
        training_bots = [
            "GPTBot",                                              # OpenAI training crawler
            "ClaudeBot", "anthropic-ai", "Claude-Web",            # Anthropic training / legacy
            "Google-Extended",                                     # Gemini training+grounding (Googlebot still indexes for search + AI Overviews)
            "Applebot-Extended",                                   # Apple training opt-out (NOT Applebot — search stays)
            "CCBot",                                               # Common Crawl (feeds many AI training sets)
            "Bytespider",                                          # ByteDance training
            "Amazonbot", "cohere-ai",                              # Amazon / Cohere training
            "meta-externalagent", "FacebookBot",                   # Meta AI training
            "ImagesiftBot", "Diffbot", "Omgilibot", "YouBot", "Timpibot",  # image/data scrapers
        ]
        header = (
            f"# {SITE_NAME} crawl policy\n"
            "# ALLOWED: normal search crawlers + AI SEARCH bots that retrieve to cite a live query\n"
            "#   (ChatGPT-User, OAI-SearchBot, PerplexityBot) — so the exhibition is found & cited.\n"
            "# BLOCKED: AI-TRAINING crawlers that would harvest the photographs into model datasets.\n\n"
        )
        blocks = "".join(f"User-agent: {b}\nDisallow: /\n\n" for b in training_bots)
        robots = f"{header}User-agent: *\nAllow: /\n\n{blocks}Sitemap: {site_url}/sitemap.xml\n"
    write(OUT / "robots.txt", robots)

    # config.json — flags (AI OFF) + the exhibition feel-knobs (every one A/B-tunable, INV-28) +
    # site_url + experiment registry seam
    config = dict(flags)
    config["exhibition"] = {
        "spread_size": 10,       # works in the hang (3–12) — never the whole catalogue
        "cold_spread": "diverse",  # the silent-entry hang: 'diverse' (farthest-point) | 'first'
        "arc_shape": "widening",   # how the arc samples near→far: 'widening' (holds contrast) | 'nearest'
        "tempo": 1.35,           # the ONE motion multiplier over the --d-* tokens (EX-MOTION, design 04)
        "glide_ms": 520,         # EX-GLIDE (INV-39): the one-frame dock clock (120–2000, ×tempo at runtime)
        # transition_ms LEFT the schema with the tempo law (EX-MOTION tombstone, 2026-07-06) —
        # the crossing rides the cross token (1.2s × tempo)
        "kinship_axes": "all",   # which axes drive distance: 'all' | [indices] (core-vs-descriptive)
        "unfold_step": 5,        # works appended per «ещё 5» along the current arc
        # EX-STORY-LEAD: how many works of the FIRST spread the opening plot covers (1–12). The rest
        # of that spread is told by a second plot, asked as the visitor comes near it, so a visit that
        # rests in the opening works never buys the whole spread's telling.
        "story_lead": 3,
        "max_unfolds": 2,        # unfold steps before «ещё 5» retires — the arc ENDS (INV-30)
        "door_size": 5,          # works at the threshold, 3–5 (EX-DOOR)
        "greeting": "ask",       # where the door's greeting hangs: ask (his pick) | top | off (EX-GREET)
        # EX-LOAD-2/-3 (INV-72/INV-73): the in-flight ladder + the one-ahead preload. Each duration
        # is a beat ×tempo (INV-33); ORDER IS LAW — load_plate_grace < load_bar_wait, clamped at boot
        # in the client (a bar never before its plate). All client-fallback-guarded, so a bake that
        # leaves them at these defaults behaves identically whether or not they ride config.
        "load_plate_grace": 0.35,  # black → tone-plate; also the fast/slow split for the reveal
        "load_bar_wait": 1.5,      # plate → plate+bar (a genuinely long wait, well past the plate)
        "load_reveal": 2.0,        # the reveal token — the graceful settle when the plate stood
        "load_reveal_fast": 0.6,   # the soft token — the crisp settle when the photo beat the plate
        "preload_ahead": 1,        # works warmed ahead along the feet (0–1) — never the whole arc
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
        # sound_url / sound_credit ride site.json (EX-NS-style instance identity): the engine's own
        # example ships neither (player OFF), an instance opts in by declaring them in site.json.
        "sound_url": (site_config.get("sound_url") or ""),   # path to the .m4a / .ogg — empty means no player renders
        "sound_credit": (site_config.get("sound_credit") or {  # the tray's attribution — instance fills its own in site.json
            "artist": "",          # artist/band name (shown bold)
            "title": "",           # track/album title (shown in «»)
            "url": "",             # artist website (shown as a link)
        }),
        # EX-QUIZ-PICK (INV-64/66): the quiz's PLACEMENT config knob — an instance tunes which
        # surfaces carry the «question?» chip, with NO code change (INV-28). ONE question per
        # show is chosen deterministically from the eligible set (INV-66 supersedes the old
        # per-walk probability coin — quiz_probability is RETIRED). The cooldown key lives at
        # the exhibition level (quiz_cooldown_hours), set when the quiz ships (see below).
        "quiz": {
            "placement": ["plaque"],
        },
    }
    # A knob at its built-in default (or empty) is SUPPRESSED from the emitted config: every
    # client read is fallback-guarded (glide_ms→520, placement→plaque, sound off when no URL),
    # so the served config carries only what the instance actually set — no dead keys.
    ex_cfg = config["exhibition"]
    if ex_cfg.get("glide_ms") == 520:
        del ex_cfg["glide_ms"]
    if not ex_cfg.get("sound_url"):
        ex_cfg.pop("sound_url", None)
        ex_cfg.pop("sound_credit", None)
    if ex_cfg.get("quiz") == {"placement": ["plaque"]}:
        del ex_cfg["quiz"]
    # site_name exists for the ENGINE client's door wordmark (INV-28); an instance that ships
    # its OWN client (see client_asset) doesn't read it — emit only with the engine's client.
    if client_asset("exhibition.js") == _ENGINE_ASSETS / "exhibition.js":
        config["site_name"] = SITE_NAME
    config["site_url"] = site_url
    config["ga_measurement_id"] = ga_id   # analytics id lives in config, never in a template
    # EX-LANG-GEO (INV-45/INV-1): the arriving-country → languages map that narrows the language
    # corner. An instance declares it in site.json; the engine's own example ships none, so the
    # corner stands at [English, browser locale] on the client's graceful default. Emitted ONLY when
    # set, so a mapless bake keeps config.json byte-identical (INV-19). The country is used only to
    # pick chips — it never enters a beat, so no analytics seam rides here (INV-1).
    if site_config.get("lang_geo"):
        config["lang_geo"] = site_config["lang_geo"]
    # EX-PASS: the transition seam's site rung. The bake passes the block through as DATA and judges
    # nothing in it — every name, range and limit is checked in the client at read time, and a value
    # the register refuses falls back to its default with the refusal on the diagnostic surface. An
    # absent block leaves every setting on its built-in default, so a site that sets nothing behaves
    # exactly as it did before the seam.
    if isinstance(site_config.get("pass"), dict) and site_config["pass"]:
        config["pass"] = dict(site_config["pass"])
    # EX-PASS-RECORDS (2026-08-19): `works` LEAVES config.json. Until today the site's `pass` block
    # carried `works` straight through — one record per work of the whole collection — so the very
    # first file a visitor's browser parses grew with the collection: his word of 2026-08-19 13:36,
    # «какой размер по устройству?? почему это должно зависеть от числа работ?». The records still
    # exist and the passage composer still reads them, but they now travel as a STATIC ASSET beside
    # the other baked files — pass-workrecords.json — fetched by no browser on the walk. Only the
    # Worker reads it, answering a selection's own ids at /api/pass/records. What config.json keeps
    # in `works`'s place is `records`: the route, and a constant — the walk's own ceiling on how many
    # ids one answer may ever carry, never a count that follows the collection.
    if isinstance(config.get("pass"), dict) and "works" in config["pass"]:
        block = config["pass"]
        records = block.pop("works")
        if not isinstance(records, dict):
            raise SystemExit("site.json's pass.works is not an id → record map — the bake "
                             "has nothing to key a lookup by")
        records_text = json.dumps(records, ensure_ascii=False, indent=0, sort_keys=True) + "\n"
        records_bytes = records_text.encode("utf-8")
        write(OUT / "pass-workrecords.json", records_text)
        # THE WALK'S OWN CEILING, DERIVED RATHER THAN TYPED TWICE. The door deals `spread_size`
        # works, and the visitor may add `unfold_step` more, up to `max_unfolds` times (his 13:39
        # word the same day, and the shape engine/client/01-knobs-lang-history.js:77-79 already
        # clamps this exact way — SPREAD, UNFOLD, MAXU). `cap` is read off the SAME config knobs by
        # the SAME bounds and defaults, never a second number typed here: a site that raises
        # spread_size or max_unfolds moves the route's own ceiling with it, in one place,
        # automatically. Where a site names none of them, the built-in defaults give 10 + 2*5 = 20.
        _ex = config.get("exhibition") or {}
        _spread = _clamp_int(_ex.get("spread_size"), 10, 3, 12)
        _unfold = _clamp_int(_ex.get("unfold_step"), 5, 1, 12)
        _maxu = _clamp_int(_ex.get("max_unfolds"), 2, 0, 5)
        # THE STAMP IS WHAT MAKES A LONG CACHE SAFE (2026-08-19). The route's answer may be held for
        # a day — the map behind it only changes when the site is rebuilt — and that is exactly the
        # hole: a visitor who returns the day after a rebake would be handed yesterday's measurements
        # for today's photographs, and a crossing composed off a stale reading is wrong in a way
        # nothing on the page shows. So the address carries the map's own digest: the same selection
        # asks at the same address for as long as the records stand, and the instant they change the
        # address changes with them. The Worker reads only `ids`, so the stamp costs it nothing.
        block["records"] = {
            "route": "/api/pass/records",
            "cap": _spread + _maxu * _unfold,
            "stamp": hashlib.sha256(records_bytes).hexdigest()[:12],
        }
    # THE SITE NAMES WHAT EXISTS (§7). Beside everything the site wrote, the `pass` block carries the
    # instrument record: one entry per instrument, keyed by its own name, with the address it is
    # served at, the version it declares and the digest its served bytes weigh to. The host reads the
    # instrument names out of the score's cues and their addresses out of this record, so the engine
    # holds no instrument name and no instrument address of its own.
    #
    # A site may write entries of its own for instruments this bake does not carry, and they pass
    # through untouched like every other value in the block. An entry whose name this bake DID write
    # a file for takes the bake's own numbers: the bake weighed the bytes it served, and a digest
    # from anywhere else would weigh a file no visitor fetches.
    if _PASS_INSTRUMENTS:
        block = config.get("pass")
        if not isinstance(block, dict):
            block = {}
        record = dict(block.get("instruments") or {})
        record.update(_PASS_INSTRUMENTS)
        block["instruments"] = record
        config["pass"] = block
    # AND THE CLIENT NAMES WHAT IT CAN TAKE (§4.4d). Beside the instrument record stands the
    # capability record: the limits the client applies, read out of the served client itself. The
    # site composes against them — a score longer than `scoreBytes` is refused before any instrument
    # sees it — and a site that reads the published number never has to keep a copy of it.
    if isinstance(config.get("pass"), dict) and config["pass"]:
        config["pass"]["capabilities"] = pass_capabilities()
    config["experiments"] = {}      # variant → flag → metric (empty registry)
    # EX-QUIZ-ONCE (INV-66) + EX-QUIZ-COPY: config seams join ONLY when the quiz is on —
    # flag off leaves config.json byte-for-byte today's (INV-60 fence).
    # quiz_cooldown_hours: how long after one show the chip stays silent (~6h, tunable).
    # quiz_probability is GONE (INV-66 supersedes the per-walk coin with one-per-show).
    if flags["quiz"]:
        config["exhibition"]["quiz_cooldown_hours"] = 6
        # EX-QUIZ-PRIZE (INV-56/INV-28): the prize wallpaper's DOWNLOAD filename. The engine derives it
        # client-side from the site-name slug (DL_BASE + "-wallpaper.jpg"); an instance that ships a
        # specific wallpaper file (e.g. a versioned name) sets quiz_prize_name in site.json — emitted
        # ONLY when set, so the engine's own bake keeps the derived default (byte-identical).
        if site_config.get("quiz_prize_name"):
            config["exhibition"]["quiz_prize_name"] = site_config["quiz_prize_name"]
        # the quiz_arm split (on/control) RETIRED 2026-07-28 on the owner's word (first said 2026-07-23):
        # traffic is small, no split test is needed, so every visitor with the flag on is eligible
        # (SPEC.md carries the dated tombstone). validate_experiments still refuses a registry entry
        # under two arms — the rule stays; an experiment leaves rather than shrinking to one arm.
        # The quiz_chip_copy split (place/place_prize) RETIRED 2026-07-28 the same way and on the same
        # reason: the owner read both wordings and adopted one, and the traffic this instance carries
        # could not settle a two-arm test in any useful time. The chip now speaks one sentence off the
        # ordinary localized set (`quiz_ask`, EX-QUIZ-COPY/INV-100); SPEC.md carries the tombstone.
        # No experiment rides the quiz any more, so the registry stays empty under this flag.
    # EX-DOOR-3 (door_diversity): tell the client to deal a fresh, evenly-spread, place-guaranteed set
    # every open, and the place fraction to guarantee among the shown windows. Flag off → the key is
    # absent and the client falls back to the curated hand (INV-19, byte-identical config).
    if flags["door_diversity"]:
        dd = site_config.get("door_diversity") or {}
        config["exhibition"]["door_diversity"] = {
            "place_min_fraction": float(dd.get("place_min_fraction", 0.6)),
            # INV-75: the fraction of each open that must be works not dealt since the last round reset
            "fresh_min": float(dd.get("fresh_min", 0.6)),
        }
    # EX-AB (INV-90): the bake refuses a degenerate experiment registry before it can serve
    validate_experiments(config["experiments"],
                         reserved={str(it["id"]) for it in items})
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
    # EX-QUIZ-EDGE (INV-59): the PRIVATE accept-sets + prize paths bake into the non-served worker,
    # never a public byte. Only when the quiz ships; flag off ⇒ QUIZ_ANSWERS stays {} and the route
    # 404s (INV-60). Keyed by string work id, sorted so the bake stays reviewable.
    quiz_answers = quiz_private if flags["quiz"] else {}
    if flags["ai_i18n"] or flags["visitor_memory"] or flags["ai_story"] or flags["quiz"]:
        worker_src = client_asset("worker.js").read_text(encoding="utf-8")
        # EX-NS: the worker's KV binding rides the namespace (@@NS_UPPER@@_I18N → EX_I18N / TLV_I18N);
        # a token-free instance worker is byte-copied unchanged (same rule as the client at write_js).
        if "@@NS@@" in worker_src or "@@NS_UPPER@@" in worker_src:
            worker_src = apply_namespace(worker_src, _NAMESPACE)
        worker_src = worker_src.replace(
            '/*__STORY_FRAGMENTS__*/{}/*__/STORY_FRAGMENTS__*/',
            json.dumps(story_fragments, ensure_ascii=False, sort_keys=True))
        worker_src = worker_src.replace(
            '/*__STORY_PV__*/"0"/*__/STORY_PV__*/',
            json.dumps(str(config["exhibition"]["story"]["params_version"])))
        worker_src = worker_src.replace(
            '/*__QUIZ_ANSWERS__*/{}/*__/QUIZ_ANSWERS__*/',
            json.dumps(quiz_answers, ensure_ascii=False, sort_keys=True))
        write(OUT / "_worker.js", worker_src)
        write(OUT / "_routes.json",
              json.dumps({"version": 1, "include": ["/api/*"], "exclude": []}) + "\n")
    if flags["ai_i18n"]:
        en = ((greet or {}).get("langs") or {}).get("en") or {}
        i18n_src = {
            "version": ex_version,
            "strings": {k: en.get(k, "") for k in
                        ("ask", "exit", "more", "q_more", "q_spent",
                         "share_label", "share_copied", "series", "room_back",
                         # EX-PROTECT / EX-QUIZ visitor-facing chrome joins the localized set so
                         # every quiz + gift string speaks the guest's tongue for ALL locales
                         # (the client keeps ENGLISH source-tongue fallbacks); the QUESTION content
                         # stays instance-supplied, never in this chrome set
                         "enjoy", "quiz_ask",
                         "quiz_submit", "quiz_win", "quiz_wrong",
                         "gift_ask", "gift_yes", "gift_no", "gift_buy")},
            "greet": en.get("greet") or {},
            # EX-EDGE-DEAD (INV-68): the dead-account English day greets with this ONE plain line
            "plain": en.get("plain") or "hello",
            # brand + the © signature are EXCLUDED by construction (never translatable)
            "titles": {it["id"]: it["title"].strip()
                       for it in items if (it.get("title") or "").strip()},
            # EX-QUIZ-PICK (EX-I18N): public quiz prompts localized like titles — id-keyed. The
            # options stay English and ride each work's quiz.options (INV-64 English labels), never
            # translated. Absent when the quiz is off (byte-identical to a quiz-less i18n source).
            "quizzes": [{"id": wid, "prompt": q["prompt"]}
                        for wid, q in sorted(quiz_public.items())] if flags["quiz"] else [],
        }
        write(OUT / "i18n_source.json",
              json.dumps(i18n_src, ensure_ascii=False, indent=0, sort_keys=True) + "\n")

    # shared images + design tokens (the exhibition renders in them). The SERVED base image is CLEAN
    # (the mark-split, EX-PROTECT-RES / INV-56): the shown walk image carries no mark — the site host
    # is stamped only on a TAKEN copy (client-side canvas on download) and on the quiz prize below.
    # So the base gallery is copied/capped WITHOUT a mark (mark_text=None), like the instance's bake.
    copy_gallery(display_max=display_max, mark_text=None)

    # EX-QUIZ-PRIZE (EX-PROTECT-RES / INV-56): the signed wallpaper derivative for each quiz work —
    # baked AFTER the gallery so its source is the display-grade copy, never the print master (INV-18).
    if flags["quiz"]:
        _bake_quiz_prizes(quiz_private, site_url)

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
    ap.add_argument("--display-max", type=int, default=None,
                    help="cap the served images' long edge in px (EX-PROTECT-RES/INV-56); the deploy passes it, tests omit it")
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
                    site_config=site_config, display_max=args.display_max)
    print(f"baked {summary['works']} work pages + exhibition root → {out_dir}")
    print(f"site_url={summary['site_url']}  robots={'DISALLOW (preview)' if summary['preview'] else 'ALLOW (prod)'}")


if __name__ == "__main__":
    main()
