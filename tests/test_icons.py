import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import brand  # noqa: E402
import make_icons  # noqa: E402


def test_writes_one_svg_per_app_plus_suite(tmp_path):
    written = make_icons.write_all(tmp_path)
    slugs = {a["slug"] for a in brand.load_products()["apps"]}
    assert {p.stem for p in written} == slugs | {"mosaik"}
    for p in written:
        root = ET.parse(p).getroot()
        assert root.get("viewBox") == "0 0 512 512"


def test_svgs_render_with_resvg(tmp_path):
    for svg in make_icons.write_all(tmp_path):
        png = svg.with_suffix(".png")
        subprocess.run(["resvg", "-w", "128", str(svg), str(png)], check=True)
        assert png.stat().st_size > 1000


def test_every_glyph_is_defined():
    for a in brand.load_products()["apps"]:
        assert a["glyph"] in make_icons.GLYPHS
