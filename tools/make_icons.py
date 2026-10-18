"""Erzeugt die Mosaik-Icons als SVG (512×512) aus products.json."""
import sys
from pathlib import Path

import brand

S = 'stroke="#fff" stroke-width="28" stroke-linecap="round" stroke-linejoin="round" fill="none"'
F = 'fill="#fff"'

GLYPHS = {
    "text": f'<path {S} d="M136 176H376M136 236H376M136 296H376M136 356H296"/>',
    "tabelle": f'<rect {S} x="128" y="144" width="256" height="224" rx="20"/>'
               f'<path {S} d="M128 219H384M128 293H384M213 144V368M299 144V368"/>',
    "praesentation": f'<rect {S} x="120" y="136" width="272" height="184" rx="16"/>'
                     f'<path {S} d="M256 320V380M200 380H312M184 280V248M240 280V208M296 280V228"/>',
    "bild": f'<rect {S} x="128" y="152" width="256" height="208" rx="20"/><circle {F} cx="204" cy="216" r="22"/>'
            f'<path {S} d="M148 340L232 264L292 318L324 290L364 330"/>',
    "grafik": f'<path {S} d="M136 360C200 120 312 392 376 152"/>'
              f'<rect {F} x="116" y="340" width="40" height="40" rx="8"/><rect {F} x="356" y="132" width="40" height="40" rx="8"/>',
    "video": f'<rect {S} x="120" y="160" width="272" height="192" rx="24"/><path {F} d="M232 212L308 256L232 300Z"/>',
    "foto": f'<circle {S} cx="256" cy="256" r="112"/><circle {F} cx="256" cy="256" r="48"/>',
    "pdf": f'<path {S} d="M168 120H304L360 176V392H168ZM304 120V176H360M208 256H320M208 312H320"/>',
    "effekte": f'<path {F} d="M256 112L284 228L400 256L284 284L256 400L228 284L112 256L228 228Z"/>'
               f'<circle {F} cx="372" cy="148" r="16"/>',
    "layout": f'<rect {S} x="128" y="128" width="256" height="256" rx="16"/><path {S} d="M128 208H384M256 208V384"/>',
    "cad": f'<path {S} d="M144 368V144L368 368ZM144 288A80 80 0 0 1 224 368"/>',
    "audio": f'<path {S} d="M160 216V296M208 168V344M256 128V384M304 184V328M352 232V280"/>',
}


def app_svg(app: dict) -> str:
    top, bottom = app["color"], brand.darken(app["color"], 0.25)
    gid = f"g-{app['slug']}"
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">'
        f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{top}"/><stop offset="1" stop-color="{bottom}"/></linearGradient></defs>'
        f'<rect width="512" height="512" rx="112" fill="url(#{gid})"/>'
        f'{GLYPHS[app["glyph"]]}</svg>\n'
    )


def suite_svg(products: dict) -> str:
    tiles = []
    size, gap, x0, y0 = 80, 16, 72, 120
    for i, app in enumerate(products["apps"]):
        col, row = i % 4, i // 4
        x, y = x0 + col * (size + gap), y0 + row * (size + gap)
        tiles.append(f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="16" fill="{app["color"]}"/>')
    bg = products["suite"]["background"]
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">'
        f'<rect width="512" height="512" rx="112" fill="{bg}"/>{"".join(tiles)}</svg>\n'
    )


def write_all(out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    products = brand.load_products()
    written = []
    for app in products["apps"]:
        p = out_dir / f"{app['slug']}.svg"
        p.write_text(app_svg(app), encoding="utf-8")
        written.append(p)
    p = out_dir / "mosaik.svg"
    p.write_text(suite_svg(products), encoding="utf-8")
    written.append(p)
    return written


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else brand.ROOT / "icons"
    for path in write_all(target):
        print(path)
