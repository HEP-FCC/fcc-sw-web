#!/usr/bin/env python3
"""
Extract PSC group boxes from PSC_Organization.svg and write _data/psc_groups.yml.

Usage:
    python3 assets/extract_psc_groups.py

Re-run whenever the SVG is regenerated from a new PDF to update the data file.
The output YAML may need manual tweaking for the split box and boxes with internal links.
"""

import re, os

SVG_PATH  = os.path.join(os.path.dirname(__file__), '..', 'assets', 'img', 'PSC_Organization.svg')
YAML_PATH = os.path.join(os.path.dirname(__file__), '..', '_data', 'psc_groups.yml')

# Box colors used for PSC group cells (not legend, not black, not red lines)
BOX_COLORS = {'#fce5cd', '#f3f3f3', '#ead1dc', '#ea9999', '#c9daf8', '#d9d2e9'}


def extract_colored_boxes(svg):
    """Return list of (x1,y1,x2,y2, fill) for colored box backgrounds."""
    boxes = []
    for sx, sy, tx, ty, d, fill in re.findall(
        r'<path transform="matrix\(([0-9.]+),0,0,([0-9.]+),([0-9.-]+),([0-9.-]+)\)" '
        r'd="M([^"]+)" fill="(#[a-f0-9]{6})"',
        svg
    ):
        if fill not in BOX_COLORS:
            continue
        sx, sy, tx, ty = float(sx), float(sy), float(tx), float(ty)
        nums = re.findall(r'[0-9.]+', d)
        if len(nums) < 4:
            continue
        x1, y1, x2, y2 = float(nums[0]), float(nums[1]), float(nums[2]), float(nums[3])
        px1 = sx*x1 + tx; py1 = sy*y1 + ty
        px2 = sx*x2 + tx; py2 = sy*y2 + ty
        w = abs(px2 - px1); h = abs(py2 - py1)
        if w < 20 or h < 20:   # skip thin lines / noise
            continue
        boxes.append((min(px1,px2), min(py1,py2), max(px1,px2), max(py1,py2), fill))
    return boxes


def extract_text_chars(svg):
    """Return list of (x, y, char) for all text characters."""
    chars = []
    for char, x, y in re.findall(
        r'<use data-text="(.)" xlink:href="#[^"]+" '
        r'transform="matrix\([^,]+,[^,]+,[^,]+,[^,]+,([0-9.]+),([0-9.]+)\)"[^/]*/>',
        svg
    ):
        chars.append((float(x), float(y), char))
    return chars


def extract_links(svg):
    """Return list of (href, x, y, w, h) for all link rects."""
    return [
        (href, float(x), float(y), float(w), float(h))
        for href, x, y, w, h in re.findall(
            r'<a href="([^"]+)"[^>]*>'
            r'<rect x="([0-9.]+)" y="([0-9.]+)" width="([0-9.]+)" height="([0-9.]+)"',
            svg)
    ]


def chars_in_box(chars, x1, y1, x2, y2, margin=5):
    return [(x, y, c) for x, y, c in chars
            if x1 - margin <= x <= x2 + margin and y1 - margin <= y <= y2 + margin]


def links_in_box(links, x1, y1, x2, y2, margin=5):
    found = {}
    for href, lx, ly, lw, lh in links:
        if x1 - margin <= lx <= x2 + margin and y1 - margin <= ly <= y2 + margin:
            found[href] = found.get(href, (lx, ly))
    return list(found.keys())


def chars_to_text(chars):
    """Reconstruct text from character positions."""
    if not chars:
        return ''
    lines = {}
    for x, y, c in chars:
        ky = round(y)
        key = next((k for k in lines if abs(k - ky) <= 2), ky)
        lines.setdefault(key, []).append((x, c))
    text_lines = []
    for y in sorted(lines):
        line = ''.join(c for _, c in sorted(lines[y]))
        # Skip lines that look like GMS group IDs
        if line.startswith('fcc-ped-') or line.startswith('eco') or len(line) < 2:
            continue
        text_lines.append(line.strip())
    return ' '.join(text_lines)


def write_yaml(groups):
    with open(YAML_PATH, 'w') as f:
        for g in groups:
            f.write('- title: "{}"\n'.format(g['title'].replace('"', '\\"')))
            if g.get('split'):
                f.write('  split: true\n')
                for sub in g.get('sub', []):
                    f.write('  # sub: {!r}\n'.format(sub))
            if g.get('gms_link'):
                f.write('  gms_link: "{}"\n'.format(g['gms_link']))
            if g.get('local_link'):
                f.write('  local_link: "{}"\n'.format(g['local_link']))
            f.write('\n')


def main():
    svg = open(SVG_PATH).read()
    all_chars = extract_text_chars(svg)
    all_links = extract_links(svg)
    boxes = extract_colored_boxes(svg)

    # Sort boxes by row (y) then column (x)
    boxes.sort(key=lambda b: (round(b[1]/50)*50, b[0]))

    print(f"Found {len(boxes)} colored boxes:\n")
    groups = []
    for x1, y1, x2, y2, fill in boxes:
        chars = chars_in_box(all_chars, x1, y1, x2, y2)
        text  = chars_to_text(chars)
        hrefs = links_in_box(all_links, x1, y1, x2, y2)
        gms   = [h for h in hrefs if 'gms.web.cern.ch' in h]
        local = [h for h in hrefs if 'gms.web.cern.ch' not in h]

        g = {'title': text, 'fill': fill, 'bbox': (round(x1), round(y1), round(x2), round(y2))}
        if gms:   g['gms_link']   = gms[0]
        if local: g['local_link'] = local[0]
        groups.append(g)

        print(f"Box fill={fill}  x={x1:.0f}-{x2:.0f} y={y1:.0f}-{y2:.0f}")
        print(f"  Title: {text!r}")
        if gms:   print(f"  GMS:   {gms[0]}")
        if local: print(f"  Local: {local[0]}")
        print()

    write_yaml(groups)
    print(f"Wrote {len(groups)} groups to {YAML_PATH}")


if __name__ == '__main__':
    main()
