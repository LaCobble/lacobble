"""
Top languages across every owned repo (public and private), each repo
weighted equally (see summarize() in fetch_github.py), one bar per language, colored from the brand palette rather than GitHub's
per-language rainbow so the card matches the rest of the page.

Usage: python render_langs.py data.json assets/langs.svg
"""
import json
import sys
from lib.svg_utils import svg_open, svg_close, card_bg, esc, write_svg
from lib.theme import CARD_WIDTH, TEXT, TEXT_MUTED, LINE, LANG_COLORS

ROW_H = 30
PAD_TOP = 30
PAD_BOTTOM = 18


def render(data: dict) -> str:
    langs = data["languages"] or [{"name": "pas encore de code", "share": 0,
                                    "repos": 0}]
    height = PAD_TOP + ROW_H * len(langs) + PAD_BOTTOM + 14

    out = svg_open(CARD_WIDTH, height, "Langages les plus utilisés, en part moyenne par dépôt")
    out += card_bg(CARD_WIDTH, height)

    label_w = 150
    bar_x = label_w + 20
    bar_max_w = CARD_WIDTH - bar_x - 90

    for i, lang in enumerate(langs):
        y = PAD_TOP + i * ROW_H
        pct = lang["share"]
        bar_w = max(4, bar_max_w * pct)
        color = LANG_COLORS[min(i, len(LANG_COLORS) - 1)]

        out += (
            f'<text x="24" y="{y+15}" font-size="12.5" fill="{TEXT}">'
            f'{esc(lang["name"])}</text>\n'
        )
        out += (
            f'<rect x="{bar_x}" y="{y+4}" width="{bar_max_w}" height="8" '
            f'rx="4" fill="{LINE}"/>\n'
        )
        out += (
            f'<rect x="{bar_x}" y="{y+4}" width="{bar_w:.1f}" height="8" '
            f'rx="4" fill="{color}"/>\n'
        )
        out += (
            f'<text x="{bar_x + bar_max_w + 12}" y="{y+12}" font-size="11" '
            f'text-anchor="start" fill="{TEXT_MUTED}">{pct*100:.0f}%</text>\n'
        )
    out += (
        f'<text x="24" y="{height - 16}" font-size="9" fill="{TEXT_MUTED}" '
        f'opacity="0.7">part moyenne du code de chaque dépôt · '
        f'{data.get("repo_count", 0)} dépôts, publics et privés</text>\n'
    )
    out += svg_close()
    return out


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        data = json.load(f)
    write_svg(sys.argv[2], render(data))
