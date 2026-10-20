"""
The last 365 days, one character per day, quiet-to-loud on the shared
CHAR_RAMP. Same visual language as a contribution graph, but it's text -
so it reads fine even if someone's on a screen reader or a very old
browser.

Usage: python render_year.py data.json assets/year.svg
"""
import json
import sys
from datetime import date

from lib.svg_utils import svg_open, svg_close, card_bg, esc, write_svg
from lib.theme import CARD_WIDTH, TEXT_MUTED, CHAR_RAMP, RAMP_COLORS

COLS = 53  # weeks
ROWS = 7   # days
CELL = 10.5
PAD_TOP = 40
PAD_LEFT = 32
PAD_BOTTOM = 34

MONTHS = ["janv", "févr", "mars", "avr", "mai", "juin",
          "juil", "août", "sept", "oct", "nov", "déc"]


def thresholds(days: list) -> list:
    """
    Quartiles of the non-empty days, like GitHub's own graph. Splitting
    on max_count instead lets a single huge day flatten the rest of the
    year into the bottom step.
    """
    counts = sorted(d["count"] for d in days if d["count"] > 0)
    if not counts:
        return [1, 1, 1]
    return [counts[len(counts) * q // 4] for q in (1, 2, 3)]


def level(count: int, cuts: list) -> int:
    if count == 0:
        return 0
    return 1 + sum(1 for c in cuts if count >= c)


def render(data: dict) -> str:
    days = data["days"]
    cuts = thresholds(days)
    height = PAD_TOP + ROWS * CELL + PAD_BOTTOM

    out = svg_open(CARD_WIDTH, height, "L'année écoulée, un caractère par jour")
    out += card_bg(CARD_WIDTH, height)

    # GitHub's calendar already starts on a Sunday, so day i sits at
    # column i // 7, row i % 7
    last_month = None
    for i, d in enumerate(days):
        col, row = divmod(i, ROWS)
        x = PAD_LEFT + col * CELL
        y = PAD_TOP + row * CELL
        lvl = level(d["count"], cuts)
        out += (
            f'<text x="{x:.1f}" y="{y:.1f}" font-size="10" '
            f'text-anchor="middle" fill="{RAMP_COLORS[lvl]}">'
            f'{esc(CHAR_RAMP[lvl])}</text>\n'
        )
        # month label above the first column that holds the 1st..7th
        month = date.fromisoformat(d["date"]).month
        if row == 0 and month != last_month:
            if last_month is not None or date.fromisoformat(d["date"]).day <= 7:
                out += (
                    f'<text x="{x - 3:.1f}" y="{PAD_TOP - 14}" font-size="9" '
                    f'fill="{TEXT_MUTED}">{MONTHS[month - 1]}</text>\n'
                )
            last_month = month

    # legend: moins · : + # @ plus
    ly = height - 14
    lx = CARD_WIDTH - 24
    out += (
        f'<text x="{lx}" y="{ly}" font-size="9" text-anchor="end" '
        f'fill="{TEXT_MUTED}">plus</text>\n'
    )
    lx -= 36
    for ch, color in reversed(list(zip(CHAR_RAMP, RAMP_COLORS))):
        out += (
            f'<text x="{lx}" y="{ly}" font-size="10" text-anchor="middle" '
            f'fill="{color}">{esc(ch)}</text>\n'
        )
        lx -= 12
    out += (
        f'<text x="{lx - 2}" y="{ly}" font-size="9" text-anchor="end" '
        f'fill="{TEXT_MUTED}">moins</text>\n'
    )
    out += (
        f'<text x="{PAD_LEFT - 4}" y="{ly}" font-size="9" '
        f'fill="{TEXT_MUTED}">{data["total_contributions"]} contributions '
        f'sur 12 mois</text>\n'
    )

    out += svg_close()
    return out


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        data = json.load(f)
    write_svg(sys.argv[2], render(data))
