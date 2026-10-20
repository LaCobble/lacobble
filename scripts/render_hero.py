"""
Top-of-page banner: handle, role, and focus areas as pills. Static text,
but drawn as an SVG so it gets the brand font and the blinking cursor
GitHub would otherwise strip.

Usage: python render_hero.py assets/hero.svg
"""
import sys
from lib.svg_utils import svg_open, svg_close, card_bg, esc, write_svg
from lib.theme import CARD_WIDTH, TEXT, EMBER, MOSS, LINE

HEIGHT = 180
HANDLE = "LaCobble"
ROLE = "CYBERSECURITY ENGINEER"
FOCUS = ["application security", "iOS security", "cryptography", "networking"]


def render() -> str:
    out = svg_open(CARD_WIDTH, HEIGHT, f"{HANDLE}, cybersecurity engineer")
    out += card_bg(CARD_WIDTH, HEIGHT)
    # the heading bracket, scaled up - same signature as every section
    out += (
        f'<path d="M 28 36 L 28 78 L 46 78" fill="none" stroke="{EMBER}" '
        f'stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>\n'
    )
    out += (
        f'<text x="60" y="62" font-size="30" font-weight="700" '
        f'fill="{TEXT}">{esc(HANDLE)}</text>\n'
    )
    # 0.6em per glyph at 30px, plus a gap
    cursor_x = 60 + len(HANDLE) * 18 + 12
    out += (
        f'<rect x="{cursor_x}" y="40" width="14" height="24" fill="{EMBER}">'
        f'<animate attributeName="opacity" values="1;1;0;0;1" '
        f'dur="1.2s" repeatCount="indefinite"/></rect>\n'
    )
    out += (
        f'<text x="60" y="90" font-size="12" letter-spacing="2.5" '
        f'fill="{EMBER}">{esc(ROLE)}</text>\n'
    )
    out += (
        f'<line x1="28" y1="112" x2="{CARD_WIDTH - 28}" y2="112" '
        f'stroke="{LINE}" stroke-width="1"/>\n'
    )
    x = 28
    for tag in FOCUS:
        w = len(tag) * 6.6 + 22  # 0.6em per glyph at 11px, plus padding
        out += (
            f'<rect x="{x:.0f}" y="128" width="{w:.0f}" height="26" rx="13" '
            f'fill="none" stroke="{MOSS}" stroke-opacity="0.6"/>\n'
        )
        out += (
            f'<text x="{x + w / 2:.0f}" y="145" font-size="11" '
            f'text-anchor="middle" fill="{TEXT}">{esc(tag)}</text>\n'
        )
        x += w + 10
    out += svg_close()
    return out


if __name__ == "__main__":
    write_svg(sys.argv[1], render())
