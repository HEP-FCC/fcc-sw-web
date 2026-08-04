#!/usr/bin/env python3
"""
Add a publication from arXiv to the FCC PSC website collection.

Usage:
    python assets/add_arxiv_pub.py <arxiv_id_or_url>

Examples:
    python assets/add_arxiv_pub.py 2603.15493
    python assets/add_arxiv_pub.py https://arxiv.org/abs/2603.15493

The citation field uses arXiv as the source. Update it manually if the paper
is later published in a journal.
"""

import sys
import re
import os
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

COLLECTION_DIR = os.path.join(os.path.dirname(__file__), '..', 'collections', '_pubs_talks')


def extract_arxiv_id(arg):
    m = re.search(r'(\d{4}\.\d{4,5})', arg)
    if not m:
        raise ValueError(f"Could not extract arXiv ID from: {arg}")
    return m.group(1)


def fetch_metadata(arxiv_id):
    url = f"https://export.arxiv.org/api/query?id_list={arxiv_id}"
    with urllib.request.urlopen(url) as resp:
        xml_data = resp.read()
    ns = {'a': 'http://www.w3.org/2005/Atom'}
    root = ET.fromstring(xml_data)
    entry = root.find('a:entry', ns)
    if entry is None:
        raise ValueError(f"No arXiv entry found for ID: {arxiv_id}")
    title = re.sub(r'\s+', ' ', entry.find('a:title', ns).text).strip()
    published = entry.find('a:published', ns).text
    authors = [a.find('a:name', ns).text.strip() for a in entry.findall('a:author', ns)]
    return {'title': title, 'published': published, 'authors': authors}


def format_date(published):
    dt = datetime.fromisoformat(published.replace('Z', '+00:00'))
    return f"{dt.strftime('%B')} {dt.day}, {dt.year}"


def format_citation(authors, arxiv_id):
    def last_initial(name):
        parts = name.rsplit(' ', 1)
        last = parts[-1]
        first = parts[0] if len(parts) > 1 else ''
        initial = f"{first[0]}." if first else ''
        return f"{last}, {initial}" if initial else last

    if len(authors) == 1:
        author_str = last_initial(authors[0])
    elif len(authors) == 2:
        author_str = f"{last_initial(authors[0])} and {last_initial(authors[1])}"
    else:
        author_str = f"{last_initial(authors[0])} et al."

    year = f"20{arxiv_id[:2]}"
    return f"{author_str}, arXiv:{arxiv_id} ({year})"


def make_filename(published, authors, title):
    dt = datetime.fromisoformat(published.replace('Z', '+00:00'))
    date_prefix = dt.strftime('%y%m%d')
    last_name = re.sub(r'[^\w]', '', authors[0].rsplit(' ', 1)[-1]) if authors else 'Unknown'
    words = re.sub(r'[^\w]', ' ', title).split()
    topic = '_'.join(words[:2]) if len(words) >= 2 else (words[0] if words else 'paper')
    return f"{date_prefix}_{last_name}_{topic}.md"


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <arxiv_id_or_url>")
        sys.exit(1)

    arxiv_id = extract_arxiv_id(sys.argv[1])
    print(f"Fetching metadata for arXiv:{arxiv_id} ...")
    meta = fetch_metadata(arxiv_id)

    date_str = format_date(meta['published'])
    citation = format_citation(meta['authors'], arxiv_id)
    filename = make_filename(meta['published'], meta['authors'], meta['title'])
    arxiv_url = f"https://arxiv.org/abs/{arxiv_id}"

    content = f"""---
type: publication
name: "{meta['title']}"
date: {date_str}
link: {arxiv_url}
citation: "{citation}"
---
"""

    output_path = os.path.normpath(os.path.join(COLLECTION_DIR, filename))

    print(f"Title:    {meta['title']}")
    print(f"Authors:  {', '.join(meta['authors'])}")
    print(f"Date:     {date_str}")
    print(f"Citation: {citation}")
    print(f"File:     {filename}")
    print()

    with open(output_path, 'w') as f:
        f.write(content)

    print(f"Created: {output_path}")


if __name__ == '__main__':
    main()
