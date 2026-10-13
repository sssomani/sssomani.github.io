# Sulaiman Somani, MD

Personal academic website at https://sssomani.github.io/.

Static HTML and CSS, hosted by GitHub Pages from the root of the `master` branch. No framework, package installation, analytics, or external fonts.

## Edit

- `index.html`: biography, education, and research summaries.
- `academic.css`: typography, Cardinal red accents, sticky navigation, and responsive layout.
- `data/publications.json`: bibliography grouped by contribution to science.

After editing the bibliography, run `python3 scripts/render_publications.py` and commit both the data and regenerated HTML. The browser does not need JavaScript.

## Preview

Run `python3 -m http.server 8766 --bind 127.0.0.1` from this directory and open http://127.0.0.1:8766/.

## Publish

Push changes to `master`. In repository Settings → Pages, use **Deploy from a branch**, **master**, **/ (root)**. `.nojekyll` serves these static files directly. Keep HTTPS enforcement enabled. No custom domain is required.
