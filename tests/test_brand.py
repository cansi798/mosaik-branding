import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import brand  # noqa: E402

FORBIDDEN = ("RAM", "Modell", "Server", "Port", "Release")


def test_twelve_apps_with_unique_slugs_and_names():
    apps = brand.load_products()["apps"]
    assert len(apps) == 12
    assert len({a["slug"] for a in apps}) == 12
    assert len({a["name"] for a in apps}) == 12
    for a in apps:
        assert a["name"].startswith("Mosaik ")
        assert re.fullmatch(r"[a-z]+", a["slug"]), a["slug"]
        assert a["repo"] == f"cansi798/mosaik-{a['slug']}"


def test_colors_have_enough_contrast_for_white_symbols():
    for a in brand.load_products()["apps"]:
        assert brand.contrast_with_white(a["color"]) >= 3.0, a["slug"]


def test_visible_texts_avoid_jargon():
    for a in brand.load_products()["apps"]:
        for field in ("short", "description", "ki"):
            for word in FORBIDDEN:
                assert word not in a[field], (a["slug"], field, word)


def test_requirements_are_ascending():
    req = brand.load_requirements()
    tiers = [req["tiers"][k] for k in ("standard", "kompakt", "pro")]
    rams = [t["ram_gb"] for t in tiers]
    assert rams == sorted(rams) and rams[0] == req["base"]["ram_gb"]
    assert tiers[0]["extra_disk_gb"] == 0
