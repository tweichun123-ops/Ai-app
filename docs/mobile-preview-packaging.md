# Mobile preview packaging

To produce a simulator handoff package (zip):

```bash
./scripts/package_mobile_preview.sh
```

Output:

- `artifacts/mobile-preview-package.zip`

The package includes:

- `mobile/` Expo project scaffold
- Root and mobile readme snapshots
- `PREVIEW_GUIDE.md` with run instructions

If npm registry is blocked in the current environment, run `npm install` / `npm run web` on a local development machine.
