#!/usr/bin/env python3
"""
build_data.py — Generate all JS data arrays for index.html from collected data.

Outputs: data_output.json with all arrays ready to embed.
"""
import json
from collections import Counter, defaultdict
from datetime import date, datetime

kept      = json.load(open("kept.json"))
vets      = json.load(open("veterans_summary.json"))
devpost   = json.load(open("devpost_summary.json"))
devpost_r = json.load(open("devpost_raw.json"))

# ── 1. weeklyData ────────────────────────────────────────────────
# Count repos created per calendar week, from 2026-02-01 to today
weekly = defaultdict(int)
for r in kept:
    d = r.get("created","")[:10]
    if not d or d < "2026-02-01":
        continue
    dt = datetime.strptime(d, "%Y-%m-%d")
    # ISO week start (Monday)
    week_start = dt - __import__("datetime").timedelta(days=dt.weekday())
    weekly[week_start.strftime("%Y-%m-%d")] += 1

# Sort and format as [{week, count}]
weeklyData = [{"week": k, "count": v} for k, v in sorted(weekly.items())]

# ── 2. Language distribution ──────────────────────────────────────
lang_counts = Counter(r["lang"] or "(none)" for r in kept)
langData = [{"lang": l, "count": c} for l, c in lang_counts.most_common(18)]

# ── 3. Category distribution ──────────────────────────────────────
cat_counts = Counter(r.get("cat","other") for r in kept)
CAT_LABELS = {
    "game":"Games","guide":"Guides/Books","bench":"Benchmarks",
    "agent":"Agents","sdk":"SDKs/Frameworks","infra":"Infrastructure",
    "tool":"Tools/CLIs","app":"Apps","other":"Other"
}
ACCENT = ["#22d3ee","#fb923c","#a78bfa","#4ade80","#f472b6","#fbbf24","#38bdf8","#34d399","#94a3b8"]
categoryData = [
    {"cat": c, "label": CAT_LABELS.get(c, c), "count": n, "color": ACCENT[i % len(ACCENT)]}
    for i, (c, n) in enumerate(cat_counts.most_common())
]

# ── 4. Model distribution (4.6 / 4.7 / 4.8) ──────────────────────
model_map = {
    "explicit":  "4.6", "topic46": "4.6",
    "explicit7": "4.7", "topic47": "4.7",
    "explicit8": "4.8", "topic48": "4.8",
}
model_counts = Counter()
for r in kept:
    model_counts[model_map.get(r["signal"], "4.6")] += 1
modelData = [{"model": m, "count": model_counts[m]} for m in ["4.6","4.7","4.8"]]

# ── 5. Star distribution ──────────────────────────────────────────
buckets = {"10k+":0,"1k-10k":0,"100-1k":0,"10-99":0,"1-9":0,"0":0}
for r in kept:
    s = r["stars"]
    if s >= 10000:   buckets["10k+"] += 1
    elif s >= 1000:  buckets["1k-10k"] += 1
    elif s >= 100:   buckets["100-1k"] += 1
    elif s >= 10:    buckets["10-99"] += 1
    elif s >= 1:     buckets["1-9"] += 1
    else:            buckets["0"] += 1
starData = [{"range": k, "count": v} for k, v in buckets.items()]

# ── 6. Developer type data ────────────────────────────────────────
flags = vets["flags"]
devTypeData = [
    {"type": "New developers (2025-26)",       "count": flags.get("new_2025_26",0),    "color": "#22d3ee"},
    {"type": "Reawakened veterans",             "count": flags.get("reawakened",0),     "color": "#fb923c"},
    {"type": "Active veterans (pre-2023)",      "count": flags.get("veteran_active",0), "color": "#a78bfa"},
    {"type": "Regular active",                  "count": flags.get("regular",0),        "color": "#4ade80"},
]

# ── 7. Account age buckets ────────────────────────────────────────
ab = vets["age_buckets"]
accountAgeData = [{"range": k, "count": v} for k, v in ab.items()]

# ── 8. Dormant devs (top reawakened, for display) ─────────────────
def y26(r): return r["years"].get("2026") or r["years"].get(2026) or 0
dormantDevs = sorted(
    [{"login": r["login"], "created": r["created"][:4], "contributions_2026": y26(r)}
     for r in vets["reawakened"]],
    key=lambda x: -x["contributions_2026"]
)[:15]

# ── 9. Headline stats ─────────────────────────────────────────────
total_stars      = sum(r["stars"] for r in kept)
unique_owners    = len(set(r["owner"] for r in kept))
unique_langs     = len(set(r["lang"] for r in kept if r["lang"]))
pct_new_dormant  = vets["pct_new_dormant"]
hackathon_count  = devpost["total_unique"]
winner_count     = devpost["winner_count"]

# ── 10. Top repos (top 15 by stars) ──────────────────────────────
topRepos = [
    {"name": r["name"], "stars": r["stars"], "lang": r["lang"],
     "lc": r["lc"], "desc": r["desc"], "url": r["url"], "cat": r.get("cat","other")}
    for r in kept[:15]
]

# ── 11. Hackathon winners from Devpost ────────────────────────────
hackathonWinners = [
    {"name": w["name"], "tagline": w["tagline"], "url": w["url"],
     "members": w.get("members",[]), "tags": w.get("tags",[])[:5],
     "likes": w.get("like_count",0)}
    for w in devpost["winners"]
]

# ── 12. Notable projects (hand-picked: top 3/cat that have desc) ──
notable = []
seen_cats = Counter()
for r in kept:
    c = r.get("cat","other")
    if seen_cats[c] < 3 and r["desc"] and r["stars"] >= 2:
        notable.append({"name":r["name"],"desc":r["desc"],"cat":c,
                         "stars":r["stars"],"url":r["url"],"lang":r["lang"]})
        seen_cats[c] += 1
    if sum(seen_cats.values()) >= 24:
        break

# ── Output ────────────────────────────────────────────────────────
out = {
    "generated": str(date.today()),
    "stats": {
        "total_repos":    len(kept),
        "total_stars":    total_stars,
        "unique_langs":   unique_langs,
        "unique_owners":  unique_owners,
        "pct_new_dormant": pct_new_dormant,
        "hackathon_projects": hackathon_count,
        "hackathon_winners":  winner_count,
        "model_counts":   dict(model_counts),
    },
    "weeklyData":      weeklyData,
    "langData":        langData,
    "categoryData":    categoryData,
    "modelData":       modelData,
    "starData":        starData,
    "devTypeData":     devTypeData,
    "accountAgeData":  accountAgeData,
    "dormantDevs":     dormantDevs,
    "topRepos":        topRepos,
    "hackathonWinners":hackathonWinners,
    "notableProjects": notable,
    "libraryData":     kept,
}
json.dump(out, open("data_output.json","w"), indent=2, ensure_ascii=False)

print("=== DATA SUMMARY ===")
s = out["stats"]
print(f"repos:         {s['total_repos']}")
print(f"total stars:   {s['total_stars']:,}")
print(f"languages:     {s['unique_langs']}")
print(f"owners:        {s['unique_owners']}")
print(f"% new/dormant: {s['pct_new_dormant']}%")
print(f"models:        {s['model_counts']}")
print(f"weekly bins:   {len(weeklyData)} weeks")
print(f"hackathon:     {hackathon_count} projects, {winner_count} winners")
print(f"top repos:     {topRepos[0]['name']} ({topRepos[0]['stars']} ★)")
print(f"dormant devs:  {dormantDevs[0]['login']} ({dormantDevs[0]['contributions_2026']} contribs 2026)")
print(f"\n→ data_output.json written")
