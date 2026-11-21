"""Update the activity section of the profile README.

Reads every repo the token can see (including private ones), counts Aakash's
commits in the last 12 months, and writes totals grouped by PUBLIC project
labels. Private repo names, code, and commit messages are never written out:
any repo not listed in PROJECTS is counted under "Other repos" (or "Public forks").
"""
import json
import os
import re
import sys
import urllib.request
from collections import defaultdict
from datetime import datetime, timedelta, timezone

USER = "AakashAmorce"
TOKEN = os.environ["STATS_TOKEN"]
README = "README.md"
API = "https://api.github.com"

# repo name -> public project label (edit freely; unlisted repos stay anonymous)
PROJECTS = {
    "limnal": "Limnal Research",
    "expected-return-dynamic": "Limnal Research",
    "macro_project": "Limnal Research",
    "dts_py": "Limnal Research",
    "dts_project": "Limnal Research",
    "cot_report": "Limnal Research",
    "cftc_project": "Limnal Research",
    "CFTCPositioningandTrend": "Limnal Research",
    "crisk_project": "Limnal Research",
    "JCDataML": "TPO Watch",
    "rent-robin": "Rent Facts",
    "rentfacts": "Rent Facts",
    "lineup": "Lineup",
    "sisturn": "Sisturn",
}
SKIP = {"desktop-tutorial", USER, "limnal-research-overview",
        "tpo-watch-overview", "rent-facts-overview"}
OTHER = "Other repos"


def get(path, params=""):
    """GET a JSON list, following pagination."""
    url = f"{API}{path}?per_page=100{params}"
    out = []
    while url:
        req = urllib.request.Request(url, headers={
            "Authorization": f"Bearer {TOKEN}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        })
        try:
            with urllib.request.urlopen(req) as r:
                data = json.load(r)
                link = r.headers.get("Link", "")
        except urllib.error.HTTPError as e:
            if e.code in (404, 409):  # empty repo or no access
                return out
            raise
        out.extend(data if isinstance(data, list) else [data])
        m = re.search(r'<([^>]+)>; rel="next"', link)
        url = m.group(1) if m else None
    return out


def get_obj(path):
    req = urllib.request.Request(f"{API}{path}", headers={
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/vnd.github+json",
    })
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def main():
    since_dt = datetime.now(timezone.utc) - timedelta(days=365)
    since = since_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    repos = get("/user/repos", "&affiliation=owner")

    commits = defaultdict(int)
    last = {}
    langs = defaultdict(int)
    for repo in repos:
        name = repo["name"]
        if name in SKIP:
            continue
        label = PROJECTS.get(name)
        if label is None:
            label = "Public forks" if (repo["fork"] and not repo["private"]) else OTHER
        full = repo["full_name"]
        cs = get(f"/repos/{full}/commits", f"&author={USER}&since={since}")
        if cs:
            commits[label] += len(cs)
            d = cs[0]["commit"]["author"]["date"][:10]
            last[label] = max(last.get(label, ""), d)
            for lang, n in get_obj(f"/repos/{full}/languages").items():
                langs[lang] += n

    total = sum(commits.values())
    order = sorted(commits, key=lambda k: (k == OTHER, -commits[k]))
    lines = [
        f"**{total:,} commits in the last 12 months.** The count covers the "
        f"{len([r for r in repos if r['name'] not in SKIP])} repos "
        "I own, public and private.",
        "",
        "| Project | Commits (12 mo) | Last commit |",
        "|---|---:|---|",
    ]
    lines += [f"| {k} | {commits[k]:,} | {last[k]} |" for k in order]
    lang_total = sum(langs.values()) or 1
    top = sorted(langs.items(), key=lambda kv: -kv[1])[:6]
    lines += ["", "Languages in the repos I committed to, by amount of code: " + " · ".join(
        f"{k} {v * 100 / lang_total:.0f}%" for k, v in top)]
    lines += ["", f"_Updated {datetime.now(timezone.utc):%b %d, %Y} by a "
              "GitHub Action. It counts commits and languages, and it "
              "publishes only the totals above._"]

    text = open(README, encoding="utf-8").read()
    new = re.sub(r"(<!-- STATS:START -->\n).*?(\n<!-- STATS:END -->)",
                 lambda m: m.group(1) + "\n".join(lines) + m.group(2),
                 text, flags=re.S)
    if new == text:
        print("No change")
        return 0
    open(README, "w", encoding="utf-8").write(new)
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
