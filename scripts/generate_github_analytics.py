#!/usr/bin/env python3
"""Generate self-hosted GitHub profile analytics SVGs for the profile README."""
import json, os, urllib.request, html
from datetime import datetime, timezone

USER = "KishanHP1808"
TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
OUT = "assets/profile"
os.makedirs(OUT, exist_ok=True)

def request(url, data=None):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "profile-analytics-generator"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode())

def main():
    profile = request(f"https://api.github.com/users/{USER}")
    repos = request(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner")
    gql = request("https://api.github.com/graphql", json.dumps({"query": """query { user(login: "KishanHP1808") { contributionsCollection { contributionCalendar { totalContributions weeks { contributionDays { date contributionCount } } } } } }"""}).encode())
    if gql.get("errors"):
        raise RuntimeError("GitHub GraphQL error: " + str(gql["errors"]))
    calendar = gql["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    days = [d for week in calendar["weeks"] for d in week["contributionDays"]]
    today = datetime.now(timezone.utc).date()
    days = [d for d in days if (today - datetime.fromisoformat(d["date"]).date()).days < 365]
    metrics = [
      ("PUBLIC REPOSITORIES", len([r for r in repos if not r.get("fork")])),
      ("STARS EARNED", sum(r.get("stargazers_count", 0) for r in repos)),
      ("FOLLOWERS", profile.get("followers", 0)),
      ("CONTRIBUTIONS (1 YEAR)", calendar["totalContributions"]),
      ("PUBLIC FORKS", sum(r.get("forks_count", 0) for r in repos)),
      ("ACCOUNT CREATED", profile.get("created_at", "")[:4])
    ]
    def txt(x,y,value,size=15,color="#24292f",weight=400):
        return f'<text x="{x}" y="{y}" fill="{color}" font-family="Segoe UI,Arial,sans-serif" font-size="{size}" font-weight="{weight}">{html.escape(str(value))}</text>'
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="900" height="270" viewBox="0 0 900 270"><rect width="900" height="270" rx="18" fill="#fff"/><rect x="1" y="1" width="898" height="268" rx="17" fill="none" stroke="#d0d7de"/>',txt(30,43,USER+" · GitHub Overview",23,"#1f2328",700),txt(30,70,"Live data from GitHub · refreshed automatically",13,"#656d76")]
    for (label,value),(x,y) in zip(metrics,[(30,112),(320,112),(610,112),(30,205),(320,205),(610,205)]):
        parts += [f'<rect x="{x}" y="{y-25}" width="260" height="68" rx="10" fill="#f6f8fa"/>',txt(x+15,y,value,25,"#0969da",700),txt(x+15,y+24,label,12,"#656d76")]
    parts.append("</svg>")
    with open(f"{OUT}/overview.light.svg","w",encoding="utf-8") as f: f.write("".join(parts))
    colors=["#ebedf0","#9be9a8","#40c463","#30a14e","#216e39"]
    parts=['<svg xmlns="http://www.w3.org/2000/svg" width="900" height="190" viewBox="0 0 900 190"><rect width="900" height="190" rx="18" fill="#fff"/><rect x="1" y="1" width="898" height="188" rx="17" fill="none" stroke="#d0d7de"/>',txt(28,38,"Contribution History",22,"#1f2328",700),txt(28,59,"Daily contributions · trailing 12 months",12,"#656d76")]
    cell,gap,left,top=12,3,35,78
    for i,d in enumerate(days):
        date=datetime.fromisoformat(d["date"])
        x=left+(i//7)*(cell+gap); y=top+date.weekday()*(cell+gap)
        n=d["contributionCount"]; level=0 if n==0 else 1 if n<3 else 2 if n<6 else 3 if n<10 else 4
        parts.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2" fill="{colors[level]}"><title>{d["date"]}: {n} contributions</title></rect>')
    parts += [txt(28,176,f'{calendar["totalContributions"]} contributions in the last year',12,"#656d76"),"</svg>"]
    with open(f"{OUT}/contributions.light.svg","w",encoding="utf-8") as f: f.write("".join(parts))

if __name__ == "__main__": main()
