#!/usr/bin/env python3
"""Render the web-app icon set (assets/icons/) from the De Stijl mark.

The mark is a Mondrian-style composition of thin rules, dark bars and
red / yellow / blue blocks, so it is drawn here as vector geometry (also
written out as assets/icons/source-mark.svg) and rasterised with Pillow.
Coordinates were measured from the official 1920x1920 logo artwork.

Usage:  python3 tools/render_icons.py     (needs Pillow; build.py does not)
"""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "icons"
OUT.mkdir(parents=True, exist_ok=True)

DARK, RED, YELLOW, BLUE, WHITE = "#3b3336", "#e8424b", "#f2c22e", "#4fb0ea", "#ffffff"
THIN = 6  # rule thickness in artwork units

# (x0, y0, x1, y1, colour) in the 1920-unit artwork space
SHAPES = [
    (395 - THIN / 2, 515, 395 + THIN / 2, 985, DARK),       # thin vertical rule, left
    (518 - THIN / 2, 625, 518 + THIN / 2, 1325, DARK),      # thin vertical rule, centre
    (168, 1108 - THIN / 2, 710, 1108 + THIN / 2, DARK),     # thin horizontal rule
    (250, 858, 515, 858 + THIN, DARK),                      # outline box: top
    (250, 985 - THIN, 515, 985, DARK),                      # outline box: bottom
    (250, 858, 250 + THIN, 985, DARK),                      # outline box: left
    (253, 892, 356, 983, RED),                              # red block
    (395, 665, 443, 985, DARK),                             # dark vertical bar
    (518, 858, 710, 930, DARK),                             # dark horizontal bar, right
    (521, 933, 585, 1105, YELLOW),                          # yellow block
    (330, 1045, 518, 1105, DARK),                           # dark horizontal bar, left
    (428, 1111, 515, 1195, BLUE),                           # blue block
]
BBOX = (168, 515, 710, 1325)  # extent of the mark

# ---- SVG source for reference / future re-renders ----
svg = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="%d %d %d %d">' % (
    BBOX[0], BBOX[1], BBOX[2] - BBOX[0], BBOX[3] - BBOX[1])]
for x0, y0, x1, y1, c in SHAPES:
    svg.append('  <rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"/>' % (x0, y0, x1 - x0, y1 - y0, c))
svg.append("</svg>")
(OUT / "source-mark.svg").write_text("\n".join(svg) + "\n", encoding="utf-8")

SS = 4  # supersampling factor


def render(size, pad_frac, path, bg=WHITE):
    """Draw the mark centred on a size x size canvas with pad_frac padding."""
    big = size * SS
    mode = "RGBA" if bg is None else "RGB"
    im = Image.new(mode, (big, big), (0, 0, 0, 0) if bg is None else bg)
    d = ImageDraw.Draw(im)
    bw, bh = BBOX[2] - BBOX[0], BBOX[3] - BBOX[1]
    inner = big * (1 - 2 * pad_frac)
    s = inner / max(bw, bh)
    ox = (big - bw * s) / 2 - BBOX[0] * s
    oy = (big - bh * s) / 2 - BBOX[1] * s
    for x0, y0, x1, y1, c in SHAPES:
        d.rectangle([x0 * s + ox, y0 * s + oy, x1 * s + ox, y1 * s + oy], fill=c)
    im = im.resize((size, size), Image.LANCZOS)
    im.save(path, optimize=True)
    print(path.relative_to(ROOT), im.size)
    return im


render(180, 0.12, OUT / "apple-touch-icon.png")
render(192, 0.12, OUT / "icon-192.png")
icon512 = render(512, 0.12, OUT / "icon-512.png")
render(512, 0.22, OUT / "icon-512-maskable.png")
render(32, 0.04, OUT / "favicon-32.png", bg=None)
render(16, 0.02, OUT / "favicon-16.png", bg=None)
icon512.save(OUT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
print("assets/icons/favicon.ico")
