"""
The GitHub avatar as ASCII art, drawn into a box of the hero banner.
Brightness picks the character on CHAR_RAMP and its color on
PORTRAIT_COLORS, so the portrait stays in the brand palette whatever
the avatar's own colors are.

One <text> per row with a <tspan> per color run keeps the SVG small;
JetBrains Mono being embedded, every glyph advances exactly 0.6em so
the columns line up.

Usage: python render_portrait.py avatar.png assets/portrait.svg
"""
import io
import sys

from PIL import Image, ImageOps

from lib.svg_utils import svg_open, svg_close, card_bg, esc, write_svg
from lib.theme import PORTRAIT_RAMP, PORTRAIT_COLORS

FONT_SIZE = 4.2
CHAR_W = FONT_SIZE * 0.6
LINE_H = FONT_SIZE * 0.92

# The subject sits in the middle of the avatar; crop to its head and
# shoulders so it isn't lost in the background at this resolution.
# (left, top, right, bottom) as fractions of the image.
CROP = (0.3525, 0.175, 0.6725, 0.625)

# The avatar's subject is a dark silhouette against neon light: invert so
# the subject is drawn in the dense, bright characters instead of left as
# a hole in the background.
INVERT = True


def portrait(avatar: bytes, x: float, y: float, w: float, h: float) -> str:
    img = Image.open(io.BytesIO(avatar)).convert("L")
    iw, ih = img.size
    img = img.crop((int(CROP[0] * iw), int(CROP[1] * ih),
                    int(CROP[2] * iw), int(CROP[3] * ih)))
    cols = int(w / CHAR_W)
    rows = int(h / LINE_H)
    img = ImageOps.autocontrast(img.resize((cols, rows), Image.LANCZOS),
                                cutoff=2)
    if INVERT:
        img = ImageOps.invert(img)

    steps = len(PORTRAIT_RAMP)
    out = (
        f'<g font-size="{FONT_SIZE}" xml:space="preserve" '
        f'aria-hidden="true">\n'
    )
    for row in range(rows):
        out += f'<text x="{x:.1f}" y="{y + (row + 1) * LINE_H:.1f}">'
        run_color, run = None, ""
        for col in range(cols):
            level = min(steps - 1, img.getpixel((col, row)) * steps // 256)
            color = PORTRAIT_COLORS[level]
            if color != run_color and run:
                out += f'<tspan fill="{run_color}">{esc(run)}</tspan>'
                run = ""
            run_color = color
            run += PORTRAIT_RAMP[level]
        out += f'<tspan fill="{run_color}">{esc(run)}</tspan></text>\n'
    out += "</g>\n"
    return out


if __name__ == "__main__":
    with open(sys.argv[1], "rb") as f:
        avatar = f.read()
    size = 200
    out = svg_open(size, size, "Avatar as ASCII art")
    out += card_bg(size, size)
    out += portrait(avatar, 10, 10, size - 20, size - 20)
    out += svg_close()
    write_svg(sys.argv[2], out)
