"""
Runs the whole pipeline: fetch GitHub data once, render every SVG from
it. This is what .github/workflows/stats.yml calls once a day.

Usage: python build_all.py [github-login]
"""
import json
import os
import sys

from fetch_github import fetch, summarize
from render_streak import render as render_streak
from render_langs import render as render_langs
from render_year import render as render_year
from render_heading import render as render_heading
from lib.svg_utils import write_svg

ASSETS = os.path.join(os.path.dirname(__file__), "..", "assets")

HEADINGS = {
    "hd-about.svg": "à propos",
    "hd-stack.svg": "stack",
    "hd-projects.svg": "projets",
    "hd-stats.svg": "stats",
    "hd-about-this-page.svg": "cette page",
}


def main():
    login = sys.argv[1] if len(sys.argv) > 1 else "LaCobble"

    print(f"fetching contribution + language data for {login}...")
    raw = fetch(login)
    data = summarize(raw)

    # keep the raw numbers around for debugging / the next run's diff
    with open(os.path.join(ASSETS, "data.json"), "w") as f:
        json.dump(data, f, indent=2)

    print("rendering data widgets...")
    write_svg(os.path.join(ASSETS, "streak.svg"), render_streak(data))
    write_svg(os.path.join(ASSETS, "langs.svg"), render_langs(data))
    write_svg(os.path.join(ASSETS, "year.svg"), render_year(data))

    print("rendering section headings...")
    for filename, label in HEADINGS.items():
        write_svg(os.path.join(ASSETS, filename), render_heading(label))

    print("done.")


if __name__ == "__main__":
    main()
