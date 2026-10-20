"""
Small, dependency-free helpers used by every render_*.py script.
Keeping these in one place is what makes the five widgets look like they
belong to the same page instead of five separate experiments.
"""
import base64
import os
from xml.sax.saxutils import escape

from lib.theme import BG, BG_CARD, LINE, FONT_STACK

FONT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "fonts")
FONT_FILE = os.path.join(FONT_DIR, "JetBrainsMono-Regular.woff2")
FONT_FILE_BOLD = os.path.join(FONT_DIR, "JetBrainsMono-Bold.woff2")


def esc(text: str) -> str:
    """Escape text for safe inclusion inside an SVG <text> node."""
    return escape(str(text))


def embedded_font_css() -> str:
    """
    Returns an @font-face block with the font inlined as base64, or an
    empty string if the font files haven't been added yet (see
    fonts/README.md). SVG's own <style> tag survives GitHub's markdown
    sanitizer even though a page-level <style> would not - this is the
    same trick the reference profile uses for its section headings.
    """
    blocks = []
    if os.path.exists(FONT_FILE):
        with open(FONT_FILE, "rb") as f:
            data = base64.b64encode(f.read()).decode("ascii")
        blocks.append(
            "@font-face{font-family:'JetBrains Mono';font-weight:400;"
            f"src:url(data:font/woff2;base64,{data}) format('woff2');}}"
        )
    if os.path.exists(FONT_FILE_BOLD):
        with open(FONT_FILE_BOLD, "rb") as f:
            data = base64.b64encode(f.read()).decode("ascii")
        blocks.append(
            "@font-face{font-family:'JetBrains Mono';font-weight:700;"
            f"src:url(data:font/woff2;base64,{data}) format('woff2');}}"
        )
    return "".join(blocks)


def svg_open(width: int, height: int, title: str) -> str:
    """Opening <svg> tag + base <style> block shared by all widgets."""
    return f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}"
     xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{esc(title)}">
  <title>{esc(title)}</title>
  <style>
    {embedded_font_css()}
    text {{ font-family: {FONT_STACK}; }}
  </style>
  <rect width="{width}" height="{height}" rx="10" fill="{BG}"/>
'''


def svg_close() -> str:
    return "</svg>\n"


def card_bg(width: int, height: int, pad: int = 1) -> str:
    """Inner panel shared by every card (hero, headings, langs)."""
    return (
        f'<rect x="{pad}" y="{pad}" width="{width - 2*pad}" '
        f'height="{height - 2*pad}" rx="9" fill="{BG_CARD}" '
        f'stroke="{LINE}" stroke-width="1"/>\n'
    )


def write_svg(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  wrote {path}")
