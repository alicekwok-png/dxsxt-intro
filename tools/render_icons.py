#!/usr/bin/env python3
"""Render the web-app icon set (assets/icons/) from the official De Stijl logo.

Source: assets/logo/destijl_logo.png (the full "de stijl · Technology Network
int'l · 形品科技" artwork on white). Only the geometric mark on the left is
used for icons — the wordmark is unreadable at icon sizes. The mark is
located automatically as the left-most block of non-white columns.

Usage:  python3 tools/render_icons.py     (needs Pillow; build.py does not)
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
LOGO = ROOT / "assets" / "logo" / "destijl_logo.png"
MARK = ROOT / "assets" / "logo" / "destijl_mark.png"
OUT = ROOT / "assets" / "icons"
OUT.mkdir(parents=True, exist_ok=True)
WHITE = (255, 255, 255)


def is_ink(px):  # anything clearly darker / more saturated than paper
    return sum(px) < 720


def crop_mark(logo: Image.Image) -> Image.Image:
    """Return the left-most connected block of content (the geometric mark)."""
    rgb = logo.convert("RGB")
    w, h = rgb.size
    px = rgb.load()
    col_has_ink = [any(is_ink(px[x, y]) for y in range(h)) for x in range(w)]
    x0 = col_has_ink.index(True)
    x1 = x0
    gap = 0
    while x1 < w - 1 and gap < 20:          # stop at the first clear gap (>20px)
        x1 += 1
        gap = 0 if col_has_ink[x1] else gap + 1
    x1 -= gap
    rows = [y for y in range(h) if any(is_ink(px[x, y]) for x in range(x0, x1 + 1))]
    return rgb.crop((x0, min(rows), x1 + 1, max(rows) + 1))


def render(mark, size, pad_frac, path, transparent=False):
    inner = int(round(size * (1 - 2 * pad_frac)))
    w, h = mark.size
    s = inner / max(w, h)
    m = mark.resize((max(1, round(w * s)), max(1, round(h * s))), Image.LANCZOS)
    if transparent:
        m = m.convert("RGBA")
        # turn paper white into alpha so favicons sit cleanly on dark tabs
        pm = m.load()
        for y in range(m.height):
            for x in range(m.width):
                r, g, b, _ = pm[x, y]
                pm[x, y] = (r, g, b, 0 if (r + g + b) > 735 else 255)
        canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        canvas.alpha_composite(m, ((size - m.width) // 2, (size - m.height) // 2))
    else:
        canvas = Image.new("RGB", (size, size), WHITE)
        canvas.paste(m, ((size - m.width) // 2, (size - m.height) // 2))
    canvas.save(path, optimize=True)
    print(path.relative_to(ROOT), canvas.size)
    return canvas


mark = crop_mark(Image.open(LOGO))
mark.save(MARK, optimize=True)
print(MARK.relative_to(ROOT), mark.size)

render(mark, 180, 0.12, OUT / "apple-touch-icon.png")
render(mark, 192, 0.12, OUT / "icon-192.png")
icon512 = render(mark, 512, 0.12, OUT / "icon-512.png")
render(mark, 512, 0.22, OUT / "icon-512-maskable.png")
render(mark, 32, 0.04, OUT / "favicon-32.png", transparent=True)
render(mark, 16, 0.02, OUT / "favicon-16.png", transparent=True)
icon512.save(OUT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
print("assets/icons/favicon.ico")
