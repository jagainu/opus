#!/usr/bin/env python3
"""Merge vets_*.json and compute summary stats for the dashboard."""
import json, glob
from collections import Counter

all_vets = []
for f in sorted(glob.glob("vets_*.json")):
    all_vets.extend(json.load(open(f)))

print(f"total owners analyzed: {len(all_vets)}")
flags = Counter(r["flag"] for r in all_vets)
print(f"flags: {dict(flags)}")
print()

def y26(r): return r["years"].get("2026") or r["years"].get(2026) or 0
def dormant(r): return sum(r["years"].get(str(yr), 0) or 0 for yr in [2021,2022,2023,2024])

reawakened = [r for r in all_vets if r["flag"] == "reawakened"]
print(f"=== REAWAKENED ({len(reawakened)}) ===")
for r in sorted(reawakened, key=lambda x: -y26(x)):
    print(f"  {r['login']:<30} created:{r['created'][:4]}  dormant(21-24):{dormant(r):>4}  2026:{y26(r):>5}")

veteran_active = [r for r in all_vets if r["flag"] == "veteran_active"]
print(f"\n=== VETERAN_ACTIVE top 10 ===")
for r in sorted(veteran_active, key=lambda x: -y26(x))[:10]:
    print(f"  {r['login']:<30} created:{r['created'][:4]}  2026:{y26(r):>5}")

new_devs = [r for r in all_vets if r["flag"] == "new_2025_26"]
print(f"\n=== NEW 2025-26 ({len(new_devs)}) ===")

# accountAgeData buckets
age_buckets = {"pre-2010":0,"2010-14":0,"2015-19":0,"2020-22":0,"2023-24":0,"2025-26":0}
for r in all_vets:
    yr = int(r["created"][:4]) if r.get("created") else 2026
    if yr < 2010: age_buckets["pre-2010"] += 1
    elif yr <= 2014: age_buckets["2010-14"] += 1
    elif yr <= 2019: age_buckets["2015-19"] += 1
    elif yr <= 2022: age_buckets["2020-22"] += 1
    elif yr <= 2024: age_buckets["2023-24"] += 1
    else: age_buckets["2025-26"] += 1
print(f"\n=== account age buckets ===")
for k,v in age_buckets.items():
    print(f"  {k}: {v}")

pct = round((flags["reawakened"] + flags["new_2025_26"]) / len(all_vets) * 100)
print(f"\n% new/dormant: {pct}%")

output = {
    "total": len(all_vets),
    "flags": dict(flags),
    "pct_new_dormant": pct,
    "reawakened": reawakened,
    "veteran_active": veteran_active,
    "new_devs": new_devs,
    "age_buckets": age_buckets,
}
json.dump(output, open("veterans_summary.json","w"), indent=2)
print(f"\n→ saved veterans_summary.json")
