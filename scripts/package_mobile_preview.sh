#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PKG_DIR="$ROOT_DIR/artifacts/mobile-preview-package"
ZIP_PATH="$ROOT_DIR/artifacts/mobile-preview-package.zip"

rm -rf "$PKG_DIR" "$ZIP_PATH"
mkdir -p "$PKG_DIR"

cp -R "$ROOT_DIR/mobile" "$PKG_DIR/mobile"
cp "$ROOT_DIR/README.md" "$PKG_DIR/README-root.md"
cp "$ROOT_DIR/mobile/README.md" "$PKG_DIR/README-mobile.md"

cat > "$PKG_DIR/PREVIEW_GUIDE.md" <<'GUIDE'
# Nexis App Preview Package

This package is prepared for simulator preview handoff.

## Included
- `mobile/` React Native (Expo + TypeScript) project scaffold
- Login -> CustomizationWizard -> Wardrobe -> OutfitDetail flow
- Right-side live preview panels (Wizard + Wardrobe)

## Run locally
```bash
cd mobile
npm install
npm run web
```

Then open the web URL shown by Expo (or run `npm run start` for iOS/Android simulator).

## Notes
- Current repo environment may block npm registry access, so install should be run in your local dev machine / CI runner.
- Replace placeholder image URLs and API endpoints for production.
GUIDE

(cd "$ROOT_DIR/artifacts" && zip -r "mobile-preview-package.zip" "mobile-preview-package" >/dev/null)

echo "Created: $ZIP_PATH"
ls -lh "$ZIP_PATH"
