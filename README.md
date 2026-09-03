# DxSxT Network — Investor Landing Page

Single-page investor presentation for **DxSxT Network** (De Stijl Technology
Network International), an RWA (Real World Assets) × GameFi project.

Bilingual (Cantonese/Chinese + English), dark-theme, self-contained static
HTML — no build framework, no runtime dependencies.

## Quick start

```bash
python3 build.py
open dist/index.html   # or just double-click it
```

`build.py` reads `src/index_template.html`, injects the images from
`assets/` as base64 data URIs plus a few hand-authored inline SVG charts,
and writes a single self-contained `dist/index.html` — ready to open
directly or deploy to any static host (GitHub Pages, Netlify, Vercel, S3,
etc.). No dependencies beyond the Python standard library.

## Project layout

| Path | Purpose |
|---|---|
| `src/index_template.html` | Source of truth — edit this |
| `assets/` | Source images (jpg/png) |
| `build.py` | Build script — regenerates `dist/index.html` |
| `dist/index.html` | Generated output — do not hand-edit |
| `docs/video-storyboard.md` | A 120-second promo video storyboard/shot list, related content but not part of the build |

See [`CLAUDE.md`](./CLAUDE.md) for the full content/style ruleset (terminology,
tone, disclaimers, palette) that this project follows — useful context for
Claude Code or anyone else picking this up.

## Deploying to GitHub Pages

```bash
# from repo root, after running build.py
git add -A && git commit -m "Update build"
git push
```

Then in the repo's Settings → Pages, set the source to the `dist/` folder
on your default branch (or copy `dist/index.html` into a `docs/` folder /
`gh-pages` branch, whichever your Pages setup expects).
