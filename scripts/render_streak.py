"""
Contributions / active days / current / longest streak card. Reads
data.json produced by fetch_github.py.

Usage: python render_streak.py data.json assets/streak.svg
"""
import json
import sys
from lib.svg_utils import svg_open, svg_close, card_bg, esc, write_svg
from lib.theme import CARD_WIDTH, TEXT, TEXT_MUTED, EMBER, MOSS, LINE

HEIGHT = 140


def render(data: dict) -> str:
    stats = [
        (data["total_contributions"], "CONTRIBUTIONS", TEXT),
        (data["active_days"], "JOURS ACTIFS", TEXT),
        (data["current_streak"], "SÉRIE ACTUELLE", EMBER),
        (data["longest_streak"], "RECORD", MOSS),
    ]

    out = svg_open(CARD_WIDTH, HEIGHT, "Contributions, jours actifs et séries")
    out += card_bg(CARD_WIDTH, HEIGHT)

    col_w = CARD_WIDTH / len(stats)
    for i, (value, label, color) in enumerate(stats):
        cx = col_w * i + col_w / 2
        out += (
            f'<text x="{cx:.1f}" y="70" font-size="32" font-weight="700" '
            f'text-anchor="middle" fill="{color}">{esc(value)}</text>\n'
        )
        out += (
            f'<text x="{cx:.1f}" y="96" font-size="10" letter-spacing="1.5" '
            f'text-anchor="middle" fill="{TEXT_MUTED}">{esc(label)}</text>\n'
        )
        if i > 0:
            out += (
                f'<line x1="{col_w*i:.1f}" y1="26" x2="{col_w*i:.1f}" '
                f'y2="{HEIGHT-26}" stroke="{LINE}" stroke-width="1"/>\n'
            )
    out += (
        f'<text x="{CARD_WIDTH/2:.0f}" y="{HEIGHT-14}" font-size="9" '
        f'text-anchor="middle" fill="{TEXT_MUTED}" opacity="0.7">'
        f'sur les 12 derniers mois · séries en jours</text>\n'
    )
    out += svg_close()
    return out


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        data = json.load(f)
    write_svg(sys.argv[2], render(data))
