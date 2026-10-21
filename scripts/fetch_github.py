"""
Pulls the language numbers langs.svg needs, once a day, via the GitHub
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

import requests

API_URL = "https://api.github.com/graphql"

QUERY = """
query($login: String!) {
  user(login: $login) {
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

    resp = requests.post(
        API_URL,
        json={"query": QUERY, "variables": {"login": login}},
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
        "languages": languages,
        "repo_count": counted,
    }


if __name__ == "__main__":
    login = sys.argv[1] if len(sys.argv) > 1 else "LaCobble"
    raw = fetch(login)
    print(json.dumps(summarize(raw), indent=2))
