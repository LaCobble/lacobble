"""
Runs the whole pipeline: fetch GitHub data once, render every SVG from
it. This is what .github/workflows/stats.yml calls once a day.

Usage: python build_all.py [github-login]
"""
import json
import os
import sys

import requests

from fetch_github import fetch, summarize
from render_apps import load as load_apps, render as render_apps
from render_hero import render as render_hero
from render_langs import render as render_langs
from render_heading import render as render_heading
from lib.svg_utils import write_svg

ASSETS = os.path.join(os.path.dirname(__file__), "..", "assets")
APPS = os.path.join(os.path.dirname(__file__), "..", "apps.toml")

HEADINGS = {
    "hd-projects.svg": "projects",
    "hd-stack.svg": "stack",
}


def fetch_avatar(login: str) -> bytes | None:
    """The public avatar, for the hero's ASCII portrait. A failed download
    only drops the portrait - it shouldn't fail the whole daily run."""
    try:
        resp = requests.get(f"https://github.com/{login}.png?size=400",
                            timeout=30)
        resp.raise_for_status()
        return resp.content
    except requests.RequestException as e:
        print(f"  avatar download failed, hero without portrait: {e}")
        return None


def main():
    login = sys.argv[1] if len(sys.argv) > 1 else "LaCobble"

    print(f"fetching language data for {login}...")
    raw = fetch(login)
    data = summarize(raw)

    # keep the raw numbers around for debugging / the next run's diff
    with open(os.path.join(ASSETS, "data.json"), "w") as f:
        json.dump(data, f, indent=2)

    print("rendering data widgets...")
    write_svg(os.path.join(ASSETS, "hero.svg"),
              render_hero(fetch_avatar(login)))
    write_svg(os.path.join(ASSETS, "langs.svg"), render_langs(data))
    write_svg(os.path.join(ASSETS, "apps.svg"), render_apps(load_apps(APPS)))

    print("rendering section headings...")
    for filename, label in HEADINGS.items():
        write_svg(os.path.join(ASSETS, filename), render_heading(label))

    print("done.")


if __name__ == "__main__":
    main()
