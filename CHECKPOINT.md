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

(To be filled in after commit)
