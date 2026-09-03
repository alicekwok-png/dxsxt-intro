#!/usr/bin/env python3
"""Build script for the DxSxT Network landing page.

Reads src/index_template.html (a raw HTML fragment with __TOKEN__
placeholders — no <!doctype>/<html>/<head>/<body>, since it is designed
to be embedded by a page wrapper), injects base64-encoded images from
assets/ plus a few hand-generated inline SVG charts, and writes the
finished, self-contained page to dist/index.html.

Usage:
    python3 build.py
"""
import base64
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src" / "index_template.html"
ASSETS = ROOT / "assets"
OUT = ROOT / "dist" / "index.html"


def b64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")


base = SRC.read_text(encoding="utf-8")

# ---------- RWA log-scale bar chart ----------
chart_rwa = '''
<svg viewBox="0 0 520 200" role="img" aria-label="RWA 代幣化資產規模：2026年中314億美元，2030年預測16兆美元，2034年預測30兆美元">
  <g font-family="IBM Plex Mono, monospace">
    <line x1="110" y1="12" x2="110" y2="185" stroke="#22304f" stroke-width="1"></line>
    <!-- row 1: 2026 actual -->
    <text x="0" y="34" fill="#aeb8d1" font-size="11">2026 年中</text>
    <text x="0" y="46" fill="#6d7791" font-size="9">實際 ACTUAL</text>
    <rect x="110" y="24" width="47" height="24" rx="6" fill="#4f8dff"><title>2026年中實際規模：約314億美元（扣除穩定幣）</title></rect>
    <text x="165" y="41" fill="#f4f6fb" font-size="13" font-weight="600">$31.4B</text>

    <!-- row 2: 2030 forecast BCG -->
    <text x="0" y="99" fill="#aeb8d1" font-size="11">2030</text>
    <text x="0" y="111" fill="#6d7791" font-size="9">BCG 預測</text>
    <rect x="110" y="89" width="304" height="24" rx="6" fill="#4f8dff" opacity=".45" stroke="#4f8dff" stroke-width="1" stroke-dasharray="3 3"><title>波士頓諮詢公司（BCG）預測2030年市場總規模達16兆美元</title></rect>
    <text x="422" y="106" fill="#f4f6fb" font-size="13" font-weight="600">$16T</text>

    <!-- row 3: 2034 forecast StanChart -->
    <text x="0" y="164" fill="#aeb8d1" font-size="11">2034</text>
    <text x="0" y="176" fill="#6d7791" font-size="9">渣打預測</text>
    <rect x="110" y="154" width="330" height="24" rx="6" fill="#4f8dff" opacity=".45" stroke="#4f8dff" stroke-width="1" stroke-dasharray="3 3"><title>渣打銀行（Standard Chartered）預測2034年市場總規模達30兆美元</title></rect>
    <text x="448" y="171" fill="#f4f6fb" font-size="13" font-weight="600">$30T</text>

    <g>
      <rect x="0" y="192" width="9" height="9" fill="#4f8dff"></rect>
      <text x="14" y="200" fill="#6d7791" font-size="9">現況 Actual</text>
      <rect x="90" y="192" width="9" height="9" fill="#4f8dff" opacity=".45" stroke="#4f8dff" stroke-dasharray="2 2"></rect>
      <text x="104" y="200" fill="#6d7791" font-size="9">第三方預測 Forecast</text>
    </g>
  </g>
</svg>
'''

# ---------- GameFi linear bar chart ----------
chart_gamefi = '''
<svg viewBox="0 0 520 160" role="img" aria-label="Web3遊戲市場總市值：2024年318億美元，2036年預測2181億美元">
  <g font-family="IBM Plex Mono, monospace">
    <line x1="110" y1="12" x2="110" y2="145" stroke="#22304f" stroke-width="1"></line>
    <text x="0" y="34" fill="#aeb8d1" font-size="11">2024</text>
    <text x="0" y="46" fill="#6d7791" font-size="9">實際 · +60.5% YoY</text>
    <rect x="110" y="24" width="48" height="24" rx="6" fill="#1fae82"><title>2024年Web3遊戲代幣總市值：約318億美元，按年+60.5%</title></rect>
    <text x="166" y="41" fill="#f4f6fb" font-size="13" font-weight="600">$31.8B</text>

    <text x="0" y="99" fill="#aeb8d1" font-size="11">2036</text>
    <text x="0" y="111" fill="#6d7791" font-size="9">FMI 預測</text>
    <rect x="110" y="89" width="330" height="24" rx="6" fill="#1fae82" opacity=".45" stroke="#1fae82" stroke-width="1" stroke-dasharray="3 3"><title>Future Market Insights預測2036年Web3遊戲市場規模達2,181億美元</title></rect>
    <text x="448" y="106" fill="#f4f6fb" font-size="13" font-weight="600">$218.1B</text>

    <g>
      <rect x="0" y="132" width="9" height="9" fill="#1fae82"></rect>
      <text x="14" y="140" fill="#6d7791" font-size="9">現況 Actual</text>
      <rect x="90" y="132" width="9" height="9" fill="#1fae82" opacity=".45" stroke="#1fae82" stroke-dasharray="2 2"></rect>
      <text x="104" y="140" fill="#6d7791" font-size="9">第三方預測 Forecast</text>
    </g>
  </g>
</svg>
'''

# ---------- Vesting unlock chart ----------
steps = [
    ("TGE", 0, "發行時 · 全數鎖倉"),
    ("+12mo", 10, "滿一年 · 首次解鎖10%"),
    ("+14mo", 30, "其後每月 +10%"),
    ("+16mo", 50, ""),
    ("+18mo", 70, ""),
    ("+21mo", 100, "全數解鎖"),
]
slot_w = 880 / 6
bars = []
grid = []
for pct in (25, 50, 75, 100):
    y = 170 - pct * 1.5
    grid.append(f'<line x1="60" y1="{y}" x2="940" y2="{y}" stroke="#1a2440" stroke-width="1"></line>')
    grid.append(f'<text x="48" y="{y+4}" text-anchor="end" fill="#6d7791" font-size="9" font-family="IBM Plex Mono, monospace">{pct}%</text>')
for i, (label, val, note) in enumerate(steps):
    cx = 60 + slot_w * (i + 0.5)
    bw = 60
    h = val * 1.5
    y = 170 - h
    op = 0.35 + 0.65 * (val / 100)
    bars.append(f'''
    <g>
      <rect x="{cx-bw/2:.1f}" y="{y:.1f}" width="{bw}" height="{h:.1f}" rx="5" fill="#e3ac35" opacity="{op:.2f}"><title>{label}：累計解鎖 {val}% {("· "+note) if note else ""}</title></rect>
      <text x="{cx:.1f}" y="{y-8:.1f}" text-anchor="middle" fill="#f4f6fb" font-size="12" font-weight="600" font-family="IBM Plex Mono, monospace">{val}%</text>
      <text x="{cx:.1f}" y="188" text-anchor="middle" fill="#aeb8d1" font-size="10.5" font-family="IBM Plex Mono, monospace">{label}</text>
    </g>''')

chart_vesting = f'''
<svg viewBox="0 0 1000 205" role="img" aria-label="代幣解鎖時間表：發行滿一年解鎖10%，其後每月解鎖10%直至100%">
  <g>{''.join(grid)}</g>
  <line x1="60" y1="170" x2="940" y2="170" stroke="#22304f" stroke-width="1"></line>
  {''.join(bars)}
</svg>
'''

# ---------- image tokens ----------
repl = {
    '__HERO_B64__': b64(ASSETS / 'hero.jpg'),
    '__ROADMAP_B64__': b64(ASSETS / 'roadmap.jpg'),
    '__CORE_B64__': b64(ASSETS / 'engine.jpg'),          # Dual-Burn Design card — jet-engine visual
    '__TANK_B64__': b64(ASSETS / 'bank.jpg'),             # Licensed Custody card — bank + $ visual
    '__CONTRACT_B64__': b64(ASSETS / 'contract.jpg'),     # Smart Circuit Breakers card
    '__PILLAR_B64__': b64(ASSETS / 'pillar.jpg'),         # Perpetual Floor Support card
    '__LOGO_MARK_B64__': b64(ASSETS / 'logo' / 'mark_crop.png'),
    '__LOGO_WORD_B64__': b64(ASSETS / 'logo' / 'wordmark_white_crop.png'),
    '__CHART_RWA__': chart_rwa,
    '__CHART_GAMEFI__': chart_gamefi,
    '__CHART_VESTING__': chart_vesting,
}
for k, v in repl.items():
    base = base.replace(k, v)

remaining = [k for k in repl if k in base]
if remaining:
    raise SystemExit(f"Unreplaced tokens left in output: {remaining}")

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(base, encoding="utf-8")
print(f"Built {OUT} ({len(base):,} bytes)")
