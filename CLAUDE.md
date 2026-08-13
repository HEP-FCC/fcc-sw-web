# FCC PS&C Website — Claude Notes

## Building the site locally

```bash
conda run -n webdev bundle exec jekyll serve
conda run -n webdev env JEKYLL_ENV=production bundle exec jekyll build
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

## Updating the PS&C organization grid

The homepage shows a Bootstrap grid of PSC groups rendered from `_data/psc_groups.yml`.
The SVG (`assets/img/PSC_Organization.svg`) is kept as source material but is no longer
embedded on the page.

To update the grid after regenerating the SVG from a new PDF:

```bash
python3 assets/extract_psc_groups.py
```

This rewrites `_data/psc_groups.yml`. After running, manually:
1. Fix any garbled title strings (GMS group IDs sometimes bleed into extracted text).
2. Restore the `split: true` entry for the DIGI-RECO SW / High Level Reco cell (row 3, column 2):
```yaml
- split: true
  sub:
    - subtitle: "DIGI-RECO SW"
      gms_link: "https://gms.web.cern.ch/group/fcc-ped-softwareandcomputing-digireco/details"
    - subtitle: "High Level Reco"
      gms_link: "https://gms.web.cern.ch/group/fcc-ped-physicsgroup-highlevelreco/details"
```
3. Restore the `local_link: "/mdi"` on the MDI entry so the title links to the internal page.

To add an internal page link to any card, add `local_link: "/page-path"` to its entry in the YAML.
The card title will become a link; the GMS mailing list link appears below it.

## Layout conventions

- The `site` layout hides the sidebar by default. Add `show_sidebar: true` to front matter to show it.
- The `main` layout (homepage only) always shows the two-column layout with the meetings iframe.
