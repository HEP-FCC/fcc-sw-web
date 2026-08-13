# FCC Software Website

Standard `github-pages`-site. All dependencies (`jquery`, `bootstrap`) are
included in the repository and any change will be automatically deployed to
<https://hep-fcc.github.io/fcc-sw-web/>.


## Updating the Publications & Talks Page

Publications and talks live as individual Markdown files in `collections/_pubs_talks/`.

### Adding a publication from arXiv

Use the helper script, passing an arXiv ID or URL:

```sh
python assets/add_arxiv_pub.py <arxiv_id_or_url>
# e.g. python assets/add_arxiv_pub.py https://arxiv.org/abs/2603.15493
```

This creates a file with `type: publication`. The `citation` field is set to `arXiv:ID (year)` and should be updated manually once the paper is published in a journal.

### Adding a conference talk

Create a file named `YYMMDD_EventName.md` in `collections/_pubs_talks/`.

For an event with multiple talks, use the `event` format with a `sessions` list:

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

For a single standalone talk, use the flat format:

```yaml
---
name: "LastName, I.: Talk title (Event Name)"
date: March 23, 2025
link: https://...
---
```

Session/talk names follow the `LastName, Initial.: Title` convention. The documents page splits on `:` so only the title portion is hyperlinked.

## Local Testing

Assuming you have a working Jeykll development environment, you can change content and for local testing, serve the page with

```sh
    bundle exec jekyll serve --baseurl=
```

and point your browser to `localhost:4000`.


## Deployment

### Development

To build the website run:
```sh
    bundle exec jekyll build --baseurl='/devel' --destination=<DEST>
```

> `<DEST>` is name of the directory into which the build site will be saved to

and upload the resulting directory:
```sh
rsync -avh <DEST>/ lxplus:/eos/project/f/fccsw-web/www/devel/ --delete
```

### Production

Merging to `main` triggers an automatic GitHub Pages deployment to
`https://hep-fcc.github.io/fcc-sw-web/`, which is also reachable via:

* `https://cern.ch/fccsw` — redirect at `/eos/project/f/fccsw-web/www/index.html`
* `https://fccsw.web.cern.ch/` — redirect at `/eos/project/f/fccsw-web/www/index.html`
