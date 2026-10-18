"""Gemeinsamer Zugriff auf products.json und requirements.json."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_products() -> dict:
    return json.loads((ROOT / "products.json").read_text(encoding="utf-8"))


def load_requirements() -> dict:
    return json.loads((ROOT / "requirements.json").read_text(encoding="utf-8"))


def _luminance(hex_color: str) -> float:
    h = hex_color.lstrip("#")
    channels = [int(h[i : i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contrast_with_white(hex_color: str) -> float:
    return 1.05 / (_luminance(hex_color) + 0.05)


def darken(hex_color: str, amount: float) -> str:
    h = hex_color.lstrip("#")
    r, g, b = (int(int(h[i : i + 2], 16) * (1 - amount)) for i in (0, 2, 4))
    return f"#{r:02X}{g:02X}{b:02X}"
