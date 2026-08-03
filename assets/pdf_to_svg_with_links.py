import fitz
import re
import sys

pdf_path = sys.argv[1]
svg_path = sys.argv[2]

doc = fitz.open(pdf_path)
page = doc[0]

# Get page dimensions
rect = page.rect
w, h = rect.width, rect.height

# Export page as SVG
svg = page.get_svg_image(matrix=fitz.Identity)

# Extract links from the PDF page
links = page.get_links()
print(f"Found {len(links)} links in PDF", file=sys.stderr)

if not links:
    with open(svg_path, "w") as f:
        f.write(svg)
    sys.exit(0)

# Parse the SVG viewBox to get the coordinate scale
vb_match = re.search(r'viewBox="([^"]+)"', svg)
if vb_match:
    vb = [float(x) for x in vb_match.group(1).split()]
    svg_w, svg_h = vb[2], vb[3]
else:
    wh_match = re.search(r'width="([\d.]+)pt".*height="([\d.]+)pt"', svg)
    svg_w = float(wh_match.group(1)) if wh_match else w
    svg_h = float(wh_match.group(2)) if wh_match else h

scale_x = svg_w / w
scale_y = svg_h / h

# Build <a> overlay elements for each link
overlays = []
for link in links:
    uri = link.get("uri") or link.get("page")
    if not uri:
        continue
    r = link["from"]  # fitz.Rect in PDF coordinates
    x = r.x0 * scale_x
    y = r.y0 * scale_y
    lw = (r.x1 - r.x0) * scale_x
    lh = (r.y1 - r.y0) * scale_y
    overlays.append(
        f'<a href="{uri}" target="_blank">'
        f'<rect x="{x:.2f}" y="{y:.2f}" width="{lw:.2f}" height="{lh:.2f}" '
        f'fill="transparent" stroke="none"/>'
        f'</a>'
    )

overlay_block = "\n".join(overlays)

# Remove full-page background rectangles: light-filled paths whose d starts at origin
def remove_bg_paths(s):
    out = []
    for part in re.split(r'(<path [^/]*/> ?)', s):
        d_match = re.search(r'\bd="M0[^"]*"', part)
        fill_match = re.search(r'fill="#(?:ffffff|f3f3f3)"', part)
        if d_match and fill_match:
            continue
        out.append(part)
    return ''.join(out)

svg = remove_bg_paths(svg)

# Inject overlays just before </svg>
svg_out = svg.replace("</svg>", f"{overlay_block}\n</svg>")

with open(svg_path, "w") as f:
    f.write(svg_out)

print(f"Written {svg_path} with {len(overlays)} link overlays", file=sys.stderr)
