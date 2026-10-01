# MRRTC website

Monadnock Region Rail Trail Collaborative. Single-file static site (images embedded).

## Publish on GitHub Pages
1. Put `index.html` and `.nojekyll` at the repo root.
2. Settings > Pages > Deploy from branch > `main` / root.
3. When going live, remove the `noindex` meta tag in `index.html`.

## Editing
Edit `index.html` directly. Run `python3 mrrtc_smoke_test.py index.html` before pushing; it must print ALL PASS (includes a no-white-tail check on every page).
