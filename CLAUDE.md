# FCC PSC Website — Claude Notes

## Building the site locally

Use the `webdev` conda environment:

```bash
conda run -n webdev bundle exec jekyll serve
conda run -n webdev bundle exec jekyll build
```

## Adding publications from arXiv

Use the script `assets/add_arxiv_pub.py`:

```bash
python assets/add_arxiv_pub.py <arxiv_id_or_url>
# e.g. python assets/add_arxiv_pub.py https://arxiv.org/abs/2603.15493
```

This creates a file in `collections/_pubs_talks/` with `type: publication`. The `citation` field uses `arXiv:ID (year)` and should be updated manually once the paper is published in a journal.

## Adding conference talks (events with sessions)

Create a file in `collections/_pubs_talks/` named `YYMMDD_EventName.md`.

Use the Indico timetable API to fetch session/contribution data:
```bash
curl -s "https://indico.cern.ch/export/timetable/<event_id>.json" -o /tmp/event.json
```

Session block IDs in the timetable URL (`#b-<id>-...`) correspond to `sessionSlotId` in the JSON. Presenters are in the `presenters` field (not `speakers`).

**Event format** (multiple talks):
```yaml
---
type: event
name: "FCC Week 2026"
date: June 8, 2026
link: https://indico.cern.ch/event/1552126/
sessions:
  - link: https://indico.cern.ch/event/1552126/contributions/<id>/
    name: "LastName, I.: Talk title"
---
```

**Flat format** (single talk, no sessions):
```yaml
---
name: "LastName, I.: Talk title (Event Name)"
date: March 23, 2015
link: https://...
---
```

Session names use `LastName, Initial.: Title` format. The documents page splits the author and title so only the title is hyperlinked.

## Converting a PDF to SVG with preserved links

Use the script `assets/pdf_to_svg_with_links.py` (requires `fcc-web` conda environment with `pymupdf`):

```bash
conda activate fcc-web
python assets/pdf_to_svg_with_links.py <input.pdf> <output.svg>
```

## Adding internal links to text in the PSC Organization SVG

The SVG at `assets/img/PSC_Organization.svg` has transparent `<rect>` overlays (added by `pdf_to_svg_with_links.py`) that cover text lines and link to external GMS group pages. To add an additional internal link for a text label:

**Step 1 — find the y-coordinates of the text characters:**
```python
import re
svg = open('assets/img/PSC_Organization.svg').read()
uses = re.findall(r'<use data-text=\"(.)\" xlink:href=\"#[^\"]+\" transform=\"matrix\([^,]+,[^,]+,[^,]+,[^,]+,([0-9.]+),([0-9.]+)\)\"', svg)
lines = {}
for char, x, y in uses:
    xf, yf = float(x), float(y)
    if 35 <= xf <= 210 and 220 <= yf <= 310:   # adjust range to the box of interest
        lines.setdefault(round(yf, 1), []).append((xf, char))
for y in sorted(lines):
    print(f'y={y}: {"".join(c for x,c in sorted(lines[y]))}')
```

**Step 2 — find the existing GMS link rect** for that text (via `grep`) to get its x, width, and y values.

**Step 3 — add a new rect** covering the text lines that sit ABOVE the existing GMS rect. The text baselines are roughly 24px above the GMS rect's y. Add the new link just before the existing one in the SVG:

```xml
<a href="/target-page" target="_top"><rect x="35.34" y="232.00" width="165.82" height="34.34" fill="transparent" stroke="none"/></a>
<a href="https://gms.web.cern.ch/..." target="_blank"><rect x="35.34" y="266.34" width="165.82" height="12.75" fill="transparent" stroke="none"/></a>
```

Key points:
- Use `target="_top"` for internal links (SVG is embedded via `<object>`, so `_top` navigates the parent page).
- Height of the new rect = GMS rect y − new rect y (so they meet without overlapping).
- The existing MDI text `/mdi` link uses x=35.34, y=232.00, width=165.82, height=34.34 as a reference.

## Layout conventions

- The `site` layout hides the sidebar by default. Add `show_sidebar: true` to front matter to show it.
- The `main` layout (homepage only) always shows the two-column layout with the meetings iframe.
