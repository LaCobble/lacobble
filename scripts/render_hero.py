"""
Top-of-page banner: handle, role, focus areas as pills, and the GitHub
avatar as ASCII art on the right. Drawn as an SVG so it gets the brand
font and the blinking cursor GitHub would otherwise strip.

Usage: python render_hero.py assets/hero.svg [avatar.png]
"""
import sys
from lib.svg_utils import svg_open, svg_close, card_bg, esc, write_svg
from lib.theme import CARD_WIDTH, TEXT, EMBER, MOSS, LINE, BG
from render_portrait import portrait

HEIGHT = 216
HANDLE = "LaCobble"
ROLE = "CYBERSECURITY ENGINEER · CTF PLAYER"
FOCUS = ["application security", "iOS security", "cryptography", "networking"]

# portrait box, right-hand side
PORTRAIT_W = 132
PORTRAIT_X = CARD_WIDTH - 16 - PORTRAIT_W
PORTRAIT_Y = 14


def render(avatar: bytes | None = None) -> str:
    out = svg_open(CARD_WIDTH, HEIGHT, f"{HANDLE}, cybersecurity engineer and CTF player")
    out += card_bg(CARD_WIDTH, HEIGHT)
    # the heading bracket, scaled up - same signature as every section
    out += (
        f'<path d="M 28 44 L 28 86 L 46 86" fill="none" stroke="{EMBER}" '
        f'stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>\n'
    )
    out += (
        f'<text x="60" y="70" font-size="30" font-weight="700" '
        f'fill="{TEXT}">{esc(HANDLE)}</text>\n'
    )
    # 0.6em per glyph at 30px, plus a gap
    cursor_x = 60 + len(HANDLE) * 18 + 12
    out += (
        f'<rect x="{cursor_x}" y="48" width="14" height="24" fill="{EMBER}">'
        f'<animate attributeName="opacity" values="1;1;0;0;1" '
        f'dur="1.2s" repeatCount="indefinite"/></rect>\n'
    )
    out += (
        f'<text x="60" y="98" font-size="11" letter-spacing="2" '
        f'fill="{EMBER}">{esc(ROLE)}</text>\n'
    )
    text_right = PORTRAIT_X - 20
    out += (
        f'<line x1="28" y1="120" x2="{text_right}" y2="120" '
        f'stroke="{LINE}" stroke-width="1"/>\n'
    )

    # pills, wrapping to a new row when the next one wouldn't fit
    x, y = 28, 136
    for tag in FOCUS:
        w = len(tag) * 6.6 + 22  # 0.6em per glyph at 11px, plus padding
        if x + w > text_right:
            x, y = 28, y + 34
        out += (
            f'<rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="26" rx="13" '
            f'fill="none" stroke="{MOSS}" stroke-opacity="0.6"/>\n'
        )
        out += (
            f'<text x="{x + w / 2:.0f}" y="{y + 17}" font-size="11" '
            f'text-anchor="middle" fill="{TEXT}">{esc(tag)}</text>\n'
        )
        x += w + 10

    if avatar:
        out += (
            f'<rect x="{PORTRAIT_X - 6}" y="{PORTRAIT_Y - 4}" '
            f'width="{PORTRAIT_W + 12}" height="{HEIGHT - 2 * PORTRAIT_Y + 8}" '
            f'rx="6" fill="{BG}" stroke="{LINE}"/>\n'
        )
        out += portrait(avatar, PORTRAIT_X, PORTRAIT_Y,
                        PORTRAIT_W, HEIGHT - 2 * PORTRAIT_Y)
    out += svg_close()
    return out


if __name__ == "__main__":
    avatar = None
    if len(sys.argv) > 2:
        with open(sys.argv[2], "rb") as f:
            avatar = f.read()
    write_svg(sys.argv[1], render(avatar))
