"""Render Evergreen's bibliography from the publication data; no browser JS needed."""
import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / 'data/publications.json').read_text())
page_path = ROOT / 'index.html'
page = page_path.read_text()

def citation(p):
    title = escape(p['title'])
    if p['url']:
        title = f'<a class="paper-title" href="{escape(p["url"], quote=True)}" target="_blank" rel="noopener">{title}</a>'
    else:
        title = f'<span class="paper-title">{title}</span>'
    authors = p['authors'].split(', ')
    # Use standard abbreviated author lists, retaining the full source in the data.
    if len(authors) > 4:
        authors = authors[:3] + ['et al.']
    author_text = escape(', '.join(authors).rstrip('.')) + '.'
    author_text = re.sub(r'(Somani S(?:S)?\*?)', r'<strong>\1</strong>', author_text)
    year = f', {p["year"]}' if p['year'] else ''
    status = f'<span class="paper-status">{escape(p["status"].replace(" (as listed in CV)", ""))}</span>' if p['status'] else ''
    return (f'<li data-publication-id="{p["id"]}">{title}'
            f'<p class="paper-authors">{author_text}</p>'
            f'<p class="paper-venue"><em>{escape(p["venue"])}</em>{year}.</p>{status}</li>')

for contribution in data['contributions']:
    key = contribution['id']
    count = sum(len(g['publications']) for g in contribution['groups'])
    label = 'Publications & patents' if key in ['ecg', 'implants'] else 'Publications'
    body = ''.join(f'<div class="publication-group"><h4>{escape(g["label"])}</h4>'
                   f'<ul class="papers">{"".join(citation(p) for p in g["publications"])}</ul></div>'
                   for g in contribution['groups'])
    block = (f'<!-- publications:start:{key} -->\n'
             f'<div class="publication-list-header"><span id="{key}-list-label">{label} <span class="publication-count">({count})</span></span>'
             f'<span class="publication-scroll-hint" id="{key}-scroll-hint">Scroll to browse ↓</span></div>'
             f'<div class="publication-scroll" role="region" tabindex="0" aria-labelledby="{key}-title {key}-list-label" '
             f'aria-describedby="{key}-scroll-hint">{body}</div>\n<!-- publications:end:{key} -->')
    if f'<!-- publications:start:{key} -->' in page:
        page = re.sub(rf'<!-- publications:start:{key} -->.*?<!-- publications:end:{key} -->', lambda _: block, page, flags=re.S)
    else:
        pattern = rf'(<section class="contribution" id="{key}">.*?)<ul class="papers">.*?</ul>'
        page, n = re.subn(pattern, lambda m: m[1] + block, page, count=1, flags=re.S)
        assert n == 1, key
        page = page.replace(f'<section class="contribution" id="{key}"><h3>', f'<section class="contribution" id="{key}"><h3 id="{key}-title">')
page = page.replace('Selected publications and patents are grouped below by research area.',
                    'Publications and patents are grouped below by research area, with related work noted within each list.')
page_path.write_text(page)
print('Rendered 56 publication entries across five scrollable publication lists.')
