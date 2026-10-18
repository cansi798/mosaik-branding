import sys
from pathlib import Path

from pypdf import PdfReader

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import brand  # noqa: E402
import make_pdf  # noqa: E402


def test_pdf_contains_all_apps_tiers_and_contact(tmp_path):
    pdf = make_pdf.build(tmp_path / "Mosaik-Suite.pdf")
    reader = PdfReader(str(pdf))
    assert 1 <= len(reader.pages) <= 2
    text = " ".join(" ".join(page.extract_text() for page in reader.pages).split())
    for app in brand.load_products()["apps"]:
        assert app["name"] in text
    req = brand.load_requirements()
    for tier in req["tiers"].values():
        assert tier["label"] in text
        assert f'{tier["ram_gb"]} GB' in text
    assert "info@waybuild.de" in text
    assert "WordCraft" not in text and "ArtCraft" not in text
