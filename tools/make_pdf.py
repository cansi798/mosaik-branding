"""Erzeugt dist/Mosaik-Suite.pdf aus products.json, requirements.json und den Icons."""
import html
import sys
from pathlib import Path
from string import Template

from weasyprint import HTML

import brand


def _app_tile(app: dict) -> str:
    e = html.escape
    return (
        f'<div class="app"><img src="icons/{e(app["slug"])}.svg"><div>'
        f'<b>{e(app["name"])}</b><div class="short">{e(app["short"])}</div>'
        f'<div class="ki"><i>KI:</i> {e(app["ki"])}</div></div></div>'
    )


def _tier_card(key: str, tier: dict) -> str:
    e = html.escape
    items = "".join(f"<li>{e(x)}</li>" for x in tier["examples"])
    extra = f' · + {tier["extra_disk_gb"]} GB Speicherplatz' if tier["extra_disk_gb"] else ""
    css = "tier dark" if key == "pro" else "tier"
    return (
        f'<div class="{css}"><h3>{e(tier["label"])}</h3><ul>{items}</ul>'
        f'<div class="req">Ab {tier["ram_gb"]} GB Arbeitsspeicher{extra}</div></div>'
    )


def render_html() -> str:
    products, req = brand.load_products(), brand.load_requirements()
    suite = products["suite"]
    os_min = req["os_min"]
    os_note = (
        f"Voraussetzungen: {os_min['windows']}, {os_min['macos']} oder {os_min['linux']}; "
        f"mindestens {req['base']['ram_gb']} GB Arbeitsspeicher und {req['base']['disk_gb']} GB freier Speicherplatz."
    )
    template = Template((brand.ROOT / "tools" / "pdf_template.html").read_text(encoding="utf-8"))
    return template.substitute(
        background=suite["background"],
        suite_name=html.escape(suite["name"]),
        claim=html.escape(suite["claim"]),
        apps="".join(_app_tile(a) for a in products["apps"]),
        tiers="".join(_tier_card(k, t) for k, t in req["tiers"].items()),
        os_note=html.escape(os_note),
        email=html.escape(suite["email"]),
        vendor=html.escape(suite["vendor"]),
        website=html.escape(suite["website"]),
    )


def build(out: Path) -> Path:
    out.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=render_html(), base_url=str(brand.ROOT)).write_pdf(str(out))
    return out


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else brand.ROOT / "dist" / "Mosaik-Suite.pdf"
    print(build(target))
