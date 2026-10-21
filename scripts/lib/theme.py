"""
Design tokens for the La_Cobble profile graphics.

Identity: "la taniere, la nuit" - a dark den at night, warm rather than
neon-hacker. One ember accent for emphasis, one moss accent for the
terminal/data feel, used sparingly so nothing competes with the ember.
"""

# --- Color tokens -----------------------------------------------------
BG = "#12100D"          # near-black warm brown - the den
BG_CARD = "#1B1712"     # slightly lifted panel background
LINE = "#2E2820"        # hairline borders / grid dividers
TEXT = "#EDE6DA"        # warm off-white, primary text
TEXT_MUTED = "#9C9284"  # secondary text, captions
EMBER = "#E3873E"       # campfire orange - the one loud accent
MOSS = "#7A9471"        # muted green - terminal / data accent
ALERT = "#C4563D"       # rare use only (e.g. "no data" states)

# --- Type tokens --------------------------------------------------------
# JetBrains Mono if embedded (see fonts/README.md), falling back to the
# closest system monospace stack so the page still looks intentional
# even before you've added the font file.
FONT_STACK = (
    "'JetBrains Mono','SF Mono','Cascadia Code',Consolas,"
    "ui-monospace,monospace"
)

# Standard card width shared by every widget so the profile grid lines up.
CARD_WIDTH = 620

# Bar colors for langs.svg, ember fading into moss - the brand palette
# rather than GitHub's per-language rainbow.
LANG_COLORS = [EMBER, "#C9915C", "#A8977A", MOSS, "#5F7358", "#4F4840"]

# ASCII portrait in the hero banner: brightness picks a character on the
# ramp and a color, dark to light, so the avatar renders in the palette.
PORTRAIT_RAMP = " .:-=+*#%@"
PORTRAIT_COLORS = ["#1B1712", "#3A332A", "#4F4840", "#6B5E4D", "#8A7356",
                   "#A9784A", "#C98143", EMBER, "#E9B98A", TEXT]
