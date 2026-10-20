"""
Section headings as SVG.

GitHub strips <style> and custom fonts from README markdown itself, so
the only way to put your own typeface on a heading is to draw the text
inside an image. Each heading is a small, cheap SVG - no photo, no API
call, just text set in the brand font with a hairline rule and a
matching bracket, so every section opens the same way.

Usage: python render_heading.py "about" "hd-about.svg"
"""
import sys
from lib.svg_utils import svg_open, svg_close, card_bg, esc, write_svg
from lib.theme import CARD_WIDTH, TEXT, TEXT_MUTED, EMBER, LINE

HEIGHT = 46


def render(label: str) -> str:
    label_up = label.upper()
    out = svg_open(CARD_WIDTH, HEIGHT, f"section: {label}")
    out += card_bg(CARD_WIDTH, HEIGHT)
    # ember corner bracket - the recurring signature element, echoed
    # in every heading so the eye learns to spot a new section starting
    out += (
        f'<path d="M 18 14 L 18 32 L 30 32" fill="none" '
        f'stroke="{EMBER}" stroke-width="2" stroke-linecap="round" '
        f'stroke-linejoin="round"/>\n'
    )
    out += (
        f'<text x="42" y="29" font-size="15" font-weight="700" '
        f'letter-spacing="3" fill="{TEXT}">{esc(label_up)}</text>\n'
    )
    # JetBrains Mono advances 0.6em per glyph: 9px at 15px, plus the 3px
    # letter-spacing
    cursor_x = 42 + len(label_up) * 12 + 8
    # blinking terminal cursor - SMIL animation, no JS needed and it
    # survives GitHub's markdown sanitizer since it's baked into the SVG
    out += (
        f'<rect x="{cursor_x}" y="18" width="8" height="13" fill="{EMBER}">'
        f'<animate attributeName="opacity" values="1;1;0;0;1" '
        f'dur="1.2s" repeatCount="indefinite"/></rect>\n'
    )
    out += (
        f'<line x1="{CARD_WIDTH - 24}" y1="23" x2="{cursor_x + 20}" '
        f'y2="23" stroke="{LINE}" stroke-width="1"/>\n'
    )
    out += svg_close()
    return out


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: render_heading.py <label> <out-path>")
        sys.exit(1)
    write_svg(sys.argv[2], render(sys.argv[1]))
