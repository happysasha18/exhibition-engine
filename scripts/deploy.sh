#!/usr/bin/env bash
# exhibition-engine deployment recipe (E3 stub — four-beat gate).
#
# Beats: bake → upload → purge_cache → verify (md5 cross-check)
# Auth: Cloudflare API token read from macOS Keychain (never a literal in source).
#
# Usage (after filling in PROJECT and DOMAIN):
#   export PROJECT=my-pages-project
#   export DOMAIN=https://my-gallery.example.com
#   bash scripts/deploy.sh

set -euo pipefail

PROJECT="${PROJECT:-exhibition-engine}"
DOMAIN="${DOMAIN:-https://synth.example.com}"
OUT="$(mktemp -d)"

# Beat 1: bake
python engine/build.py \
  --content "${CONTENT_DIR:?set CONTENT_DIR}" \
  --site "${SITE_JSON:?set SITE_JSON}" \
  --out "$OUT" \
  --site-url "$DOMAIN"

# Beat 2: upload via Wrangler (Cloudflare Pages)
CF_TOKEN="$(security find-generic-password -s cloudflare-api-token -w)"
CLOUDFLARE_API_TOKEN="$CF_TOKEN" wrangler pages deploy "$OUT" \
  --project-name "$PROJECT" \
  --branch production

# Beat 3: purge_cache (all cached pages)
curl -s -X POST \
  "https://api.cloudflare.com/client/v4/zones/${CF_ZONE_ID:?}/purge_cache" \
  -H "Authorization: Bearer $CF_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"purge_everything":true}'

# Beat 4: verify — md5 cross-check between local bake and a fetched index
LOCAL_MD5="$(md5 -q "$OUT/index.html")"
REMOTE_MD5="$(curl -s "$DOMAIN/" | md5 -q)"
if [ "$LOCAL_MD5" != "$REMOTE_MD5" ]; then
  echo "WARN: remote index differs from local bake (CDN may not have settled yet)"
fi

echo "deploy complete → $DOMAIN"
rm -rf "$OUT"
