# MRRTC website

Monadnock Region Rail Trail Collaborative. Single-file static site (images embedded).

Last updated: 2026-10-18

## Publish on GitHub Pages
1. Put `index.html` and `.nojekyll` at the repo root.
2. Settings > Pages > Deploy from branch > `main` / root.
3. When going live, remove the `noindex` meta tag in `index.html`.

## Editing
Edit `index.html` directly. Run `python3 mrrtc_smoke_test.py index.html` before pushing; it must print ALL PASS (includes a no-white-tail check on every page).

## Interactive trail map
The repo also hosts the interactive trail map as separate pages named `map_vX.Y.html`. The newest is `map_v2.2.html` (2026-10-18).
- Each new version gets a new file name so browsers do not show a saved old copy. Do not overwrite or rename an older map file.
- A `map_vX.Y_test.html` file is an identical copy of the same version, used to try it on the live site first.
- The version label shows in the map's bottom-right corner. If it does not match the file name, the browser is showing an old copy.
- Older files (`map5.html`, `map_v2.1.html`, `map_v2.1_test.html`) are kept for reference.
- The map is rebuilt from an export of the board's Google My Map. The rebuild script and steps live in the Project (`MRRTC_map_refresh_guide.md`).

## Change log
- 2026-10-18: Added the interactive trail map section and `map_v2.2.html`.
