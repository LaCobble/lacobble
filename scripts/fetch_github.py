"""
Pulls the raw numbers the widgets need, once a day, via the GitHub
GraphQL API. Needs a token in the GH_TOKEN env var (the workflow passes
in the GH_PAT secret - see .github/workflows/stats.yml). The token needs
the `repo` scope so private repos count toward the language totals; only
byte totals per language leave the API, never a private repo's name.

Run standalone for debugging:
    GH_TOKEN=ghp_xxx python fetch_github.py > data.json
"""
import json
import os
import sys
from datetime import date, timedelta

import requests

API_URL = "https://api.github.com/graphql"

QUERY = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      contributionCalendar {
        weeks {
          contributionDays { date contributionCount }
        }
      }
    }
    repositories(first: 100, ownerAffiliations: OWNER, isFork: false) {
      nodes {
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name color } }
        }
      }
    }
  }
}
"""


def fetch(login: str) -> dict:
    token = os.environ.get("GH_TOKEN")
    if not token:
        raise SystemExit("GH_TOKEN env var is required")

    to = date.today()
    frm = to - timedelta(days=365)
    variables = {
        "login": login,
        "from": f"{frm.isoformat()}T00:00:00Z",
        "to": f"{to.isoformat()}T23:59:59Z",
    }
    resp = requests.post(
        API_URL,
        json={"query": QUERY, "variables": variables},
        headers={"Authorization": f"bearer {token}"},
        timeout=30,
    )
    resp.raise_for_status()
    payload = resp.json()
    if "errors" in payload:
        raise SystemExit(f"GraphQL error: {payload['errors']}")
    return payload["data"]["user"]


def summarize(raw: dict) -> dict:
    """Reduce the raw GraphQL payload to exactly what the renderers need."""
    days = []
    for week in raw["contributionsCollection"]["contributionCalendar"]["weeks"]:
        for d in week["contributionDays"]:
            days.append({"date": d["date"], "count": d["contributionCount"]})

    # streaks
    current = longest = running = 0
    for d in days:
        if d["count"] > 0:
            running += 1
            longest = max(longest, running)
        else:
            running = 0
    # current streak = trailing run ending on the last day with data.
    # The workflow runs at 04:15 UTC, when today is still empty - an empty
    # today doesn't break the streak, it just isn't over yet.
    trailing = days[:-1] if days and days[-1]["count"] == 0 else days
    for d in reversed(trailing):
        if d["count"] > 0:
            current += 1
        else:
            break

    # languages, as each repo's share of its own code averaged over every
    # repo. Summing raw bytes lets one repo with a committed virtualenv or
    # vendored SDK outweigh dozens of real projects.
    lang_share: dict[str, dict] = {}
    counted = 0
    for repo in raw["repositories"]["nodes"]:
        edges = repo["languages"]["edges"]
        repo_bytes = sum(e["size"] for e in edges)
        if not repo_bytes:
            continue
        counted += 1
        for edge in edges:
            name = edge["node"]["name"]
            entry = lang_share.setdefault(
                name, {"share": 0.0, "color": edge["node"]["color"], "repos": 0}
            )
            entry["share"] += edge["size"] / repo_bytes
            entry["repos"] += 1

    languages = sorted(
        ({"name": k, **v, "share": v["share"] / counted}
         for k, v in lang_share.items()),
        key=lambda x: x["share"],
        reverse=True,
    )[:6]

    return {
        "days": days,
        "current_streak": current,
        "longest_streak": longest,
        "total_contributions": sum(d["count"] for d in days),
        "active_days": sum(1 for d in days if d["count"] > 0),
        "languages": languages,
        "repo_count": counted,
    }


if __name__ == "__main__":
    login = sys.argv[1] if len(sys.argv) > 1 else "LaCobble"
    raw = fetch(login)
    print(json.dumps(summarize(raw), indent=2))
