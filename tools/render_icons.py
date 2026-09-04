#!/usr/bin/env python3
"""Render the web-app icon set (assets/icons/) from the official De Stijl logo.

Source: assets/logo/destijl_logo.png (the full "de stijl · Technology Network
int'l · 形品科技" artwork on white). Home-screen / PWA icons (180px and up)
use the complete logo, cropped to its content box, as the user asked. The
16/32px favicons use only the geometric mark on the left (auto-located as
the left-most block of non-white columns) because the wordmark is
unreadable that small.

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


def crop_content(logo: Image.Image) -> Image.Image:
    """Return the whole artwork trimmed to its non-white bounding box."""
    rgb = logo.convert("RGB")
    w, h = rgb.size
    px = rgb.load()
    xs = [x for x in range(w) if any(is_ink(px[x, y]) for y in range(h))]
    ys = [y for y in range(h) if any(is_ink(px[x, y]) for x in range(w))]
    return rgb.crop((min(xs), min(ys), max(xs) + 1, max(ys) + 1))


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


logo = Image.open(LOGO)
full = crop_content(logo)
mark = crop_mark(logo)
mark.save(MARK, optimize=True)
print(MARK.relative_to(ROOT), mark.size, "| full logo", full.size)

render(full, 180, 0.08, OUT / "apple-touch-icon.png")
render(full, 192, 0.08, OUT / "icon-192.png")
icon512 = render(full, 512, 0.08, OUT / "icon-512.png")
render(full, 512, 0.18, OUT / "icon-512-maskable.png")
render(mark, 32, 0.04, OUT / "favicon-32.png", transparent=True)
render(mark, 16, 0.02, OUT / "favicon-16.png", transparent=True)
render(mark, 48, 0.06, OUT / "favicon-48.png").save(OUT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
(OUT / "favicon-48.png").unlink()
print("assets/icons/favicon.ico")
