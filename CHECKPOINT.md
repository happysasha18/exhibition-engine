# gallery-engine extraction CHECKPOINT

Each step records the exact command run and its result.
Update this file after each step so a cut-off run can resume.

---

## Step 1 — git init

```
mkdir -p ~/gallery-engine && cd ~/gallery-engine && git init
```
Result: `Initialized empty Git repository in /Users/sashaabramovich/gallery-engine/.git/`
Status: DONE

---

## Step 2 — copy files from ~/tlvphoto

Files copied:
- `assets_src/exhibition.js` → `engine/assets/exhibition.js`
- `assets_src/exhibition.css` → `engine/assets/exhibition.css`
- `assets_src/favicon.svg` → `example/instance-assets/favicon.svg`
- `assets_src/favicon.png` → `example/instance-assets/favicon.png`
- `assets_src/apple-touch-icon.png` → `example/instance-assets/apple-touch-icon.png`
- `tests/headless.py` → `engine/harness/headless.py`

Status: DONE

---

## Step 3 — engine/build.py (generalized)

Created `engine/build.py` — generalized from `~/tlvphoto/scripts/build_site.py`.
Instance constants moved to `site.json`. Data paths resolve inside `--content`.
Instance assets resolve from `<content>/instance-assets/` or `--instance-assets`.

Status: DONE

---

## Step 4 — example/site.json

Created with the five tlvphoto instance keys.

Status: DONE

---

## Step 5 — byte-identical bake proof

Scratch directory: `/private/tmp/claude-501/-Users-sashaabramovich/0c0d7670-0735-46ba-915d-d1cfcf06c715/scratchpad`

Reference bake (original script via import trick):
```
python3 -c "
import sys
sys.path.insert(0, '/Users/sashaabramovich/tlvphoto/scripts')
import build_site
from pathlib import Path
build_site.OUT = Path('<scratch>/ref')
build_site.build('https://tlvphotos.com', ga_id='G-00J4KGDHCG')
"
```
Result: `ref bake done`

Engine bake:
```
python3 ~/gallery-engine/engine/build.py \
  --content ~/tlvphoto \
  --site ~/gallery-engine/example/site.json \
  --out <scratch>/eng \
  --site-url https://tlvphotos.com \
  --ga-id G-00J4KGDHCG \
  --instance-assets ~/tlvphoto/assets_src
```
Result: `baked 121 work pages + exhibition root → <scratch>/eng`

Diff:
```
diff -r <scratch>/ref <scratch>/eng
```
Result: (empty — exit code 0)

File count:
```
find <scratch>/eng -type f | wc -l
```
Result: 256

Status: DONE — BYTE-IDENTICAL

---

## Step 6 — README.md

Written at repo root: engine overview, content contract, site contract, bake command,
tests note, provenance line.

Status: DONE

---

## Step 7 — git commit

```
git add -A && git commit -m "gallery-engine v0: generic builder + exhibition renderer extracted from tlvphoto; bake proven byte-identical"
```
Result: `[main (root-commit) 1e65222] gallery-engine v0: ...`
10 files changed, 1582 insertions(+)

Status: DONE

---

## 2026-07-07 00:36 — re-sync client assets from instance repo (post-rename)

Repo was renamed from ~/gallery-engine to ~/exhibition-engine tonight.
Worker agent re-synced walk's client assets from ~/tlvphoto into engine.

### Files copied

| src | dst |
|-----|-----|
| ~/tlvphoto/assets_src/exhibition.js | engine/assets/exhibition.js |
| ~/tlvphoto/assets_src/exhibition.css | engine/assets/exhibition.css |
| ~/tlvphoto/assets_src/worker.js | engine/assets/worker.js (new file) |
| ~/tlvphoto/tests/headless.py | engine/harness/headless.py |

### md5 verification (src then dst — pairs must match)

```
dc104eb5879ab0c7e48095b3e7a89ab5  exhibition.js (src)
dc104eb5879ab0c7e48095b3e7a89ab5  exhibition.js (dst)
89ca8d4afd0dc895a16ff9766b6c2600  exhibition.css (src)
89ca8d4afd0dc895a16ff9766b6c2600  exhibition.css (dst)
a1cce6979a094670f5e82969b882e935  worker.js (src)
a1cce6979a094670f5e82969b882e935  worker.js (dst)
feecd1a7f3232ce265098cf358ca7ec0  headless.py (src)
feecd1a7f3232ce265098cf358ca7ec0  headless.py (dst)
```

All four pairs match.

### git status --short

```
 M CHECKPOINT.md
 M engine/assets/exhibition.css
 M engine/assets/exhibition.js
 M engine/harness/headless.py
?? NEXT_STEPS.md
?? engine/assets/worker.js
```

### Notes

WATCHED: Task brief listed headless.py destination as `engine/tests/headless.py` and WRITE-OWNERSHIP item 4 named that path. The engine repo uses `engine/harness/` (not `engine/tests/`) — headless.py already existed there from the original extraction (Step 2 above). Mirrored the repo's own layout and wrote to `engine/harness/headless.py` instead of inventing a second tests directory. Senior to confirm this is the right call; if `engine/tests/` is intentional, one more copy is needed.

Status: DONE — NOT COMMITTED (pending senior review)

## E2 port session — opened 2026-07-07 01:45 (the senior)
Goal: engine/build.py absorbs tlvphoto's day; byte-proof vs tlvphoto's own bake.
- Base fact: engine born from tlvphoto build_site @ a68c220 (2026-07-05 23:16); the day's diff =
  a68c220..HEAD on scripts/build_site.py (251 lines; /tmp/day.patch — does NOT apply, the
  parameterization rewrote context).
- Port shape: TODAY's tlvphoto build_site.py + the v0 parameterization transforms:
  (1) docstring → engine's; (2) ROOT/OUT → globals set in build(content_dir,out_dir);
  (3) CREATOR/SITE_NAME/ROOT_TITLE/ROOT_DESCRIPTION/COLLECTION_NAME ← site_config;
  (4) COPYRIGHT → global composed INSIDE build() (year+creator+site_name);
  (5) exhibition js/css/worker ← engine_assets_dir (copy_exhibition_assets), favicons ←
      instance_assets_dir (content/instance-assets first);
  (6) render_exhibition prose ← the three globals; (7) main() = engine CLI + --enable;
  (8) everything else verbatim (clean urls · consent · i18n source/worker/_routes · memory flag ·
      series block · pool tones · sign lines · hand pool).
- Proof: `python engine/build.py --content ~/tlvphoto --site example/site.json --out /tmp/ebake
  --site-url https://tlvphotos.com --ga-id G-00J4KGDHCG --enable ai_i18n --enable visitor_memory`
  then `diff -r /tmp/ebake ~/tlvphoto/site` → EMPTY.
- Content contract grew (document in README at E7): + data/greetings.json + finalist_series.json.
