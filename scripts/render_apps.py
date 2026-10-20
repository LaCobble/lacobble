"""
The iOS app catalogue as a grid of tiles, grouped by category. Reads the
hand-curated apps.toml at the repo root - no API call, so a private repo
never shows up here unless it was added on purpose.

Usage: python render_apps.py ../apps.toml assets/apps.svg
"""
import sys
import tomllib

from lib.svg_utils import svg_open, svg_close, card_bg, esc, write_svg
from lib.theme import CARD_WIDTH, TEXT, TEXT_MUTED, EMBER, LINE, BG

PAD = 24
COLS = 3
GAP = 10
TILE_H = 46
LABEL_H = 30
SECTION_GAP = 4


def load(path: str) -> list:
    with open(path, "rb") as f:
        return tomllib.load(f)["app"]


def group(apps: list) -> dict:
    """Categories in order of first appearance, apps in file order."""
    groups: dict[str, list] = {}
    for app in apps:
        groups.setdefault(app["category"], []).append(app)
    return groups


def render(apps: list) -> str:
    groups = group(apps)
    tile_w = (CARD_WIDTH - 2 * PAD - (COLS - 1) * GAP) / COLS
    rows = sum(-(-len(g) // COLS) for g in groups.values())
    height = (PAD + 16 + len(groups) * (LABEL_H + SECTION_GAP)
              + rows * (TILE_H + GAP) + PAD - SECTION_GAP)

    out = svg_open(CARD_WIDTH, height, f"{len(apps)} iOS apps, by category")
    out += card_bg(CARD_WIDTH, height)
    out += (
        f'<text x="{PAD}" y="{PAD + 6}" font-size="10" letter-spacing="1.5" '
        f'fill="{TEXT_MUTED}">{len(apps)} NATIVE iOS APPS</text>\n'
    )

    y = PAD + 16
    for category, members in groups.items():
        out += (
            f'<text x="{PAD}" y="{y + 20}" font-size="10.5" font-weight="700" '
            f'letter-spacing="1.5" fill="{EMBER}">{esc(category.upper())}</text>\n'
        )
        y += LABEL_H
        for i, app in enumerate(members):
            col, row = i % COLS, i // COLS
            x = PAD + col * (tile_w + GAP)
            ty = y + row * (TILE_H + GAP)
            out += (
                f'<rect x="{x:.1f}" y="{ty}" width="{tile_w:.1f}" '
                f'height="{TILE_H}" rx="6" fill="{BG}" stroke="{LINE}"/>\n'
            )
            out += (
                f'<text x="{x + 12:.1f}" y="{ty + 20}" font-size="12" '
                f'font-weight="700" fill="{TEXT}">{esc(app["name"])}</text>\n'
            )
            out += (
                f'<text x="{x + 12:.1f}" y="{ty + 35}" font-size="9.5" '
                f'fill="{TEXT_MUTED}">{esc(app["line"])}</text>\n'
            )
        y += -(-len(members) // COLS) * (TILE_H + GAP) + SECTION_GAP

    out += svg_close()
    return out


if __name__ == "__main__":
    write_svg(sys.argv[2], render(load(sys.argv[1])))
