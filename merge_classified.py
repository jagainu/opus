#!/usr/bin/env python3
"""Merge classified_*.json back onto candidates.json, validating integrity."""
import json, glob

cands = {r["name"]: r for r in json.load(open("candidates.json"))}
VALID_CATS = {"game","guide","bench","agent","sdk","infra","tool","app","other"}

decisions = {}
dupes, badcat = [], []
for f in sorted(glob.glob("classified_*.json")):
    for d in json.load(open(f)):
        n = d["name"]
        if n in decisions:
            dupes.append(n)
        decisions[n] = d
        if d.get("cat") not in VALID_CATS:
            badcat.append((n, d.get("cat")))

missing = [n for n in cands if n not in decisions]   # candidate never classified
extra   = [n for n in decisions if n not in cands]    # classified but not a candidate (hallucinated name)

kept = []
for n, c in cands.items():
    d = decisions.get(n)
    if not d or not d.get("keep"):
        continue
    kept.append({
        "name": c["name"], "owner": c["owner"], "stars": c["stars"],
        "lang": c["lang"], "lc": c["lc"], "signal": c["signal"],
        "created": c["created"], "url": c["url"],
        "cat": d["cat"], "desc": d["desc"] or c["desc"],
    })
kept.sort(key=lambda r: r["stars"], reverse=True)
json.dump(kept, open("kept.json", "w"), indent=2, ensure_ascii=False)

print(f"candidates:        {len(cands)}")
print(f"classified:        {len(decisions)}")
print(f"  duplicates:      {len(dupes)} {dupes[:5]}")
print(f"  missing(unclass):{len(missing)} {missing[:10]}")
print(f"  extra(halluc.):  {len(extra)} {extra[:5]}")
print(f"  bad category:    {len(badcat)} {badcat[:5]}")
print(f"KEPT:              {len(kept)}")
print(f"DROPPED:           {len(decisions) - len(extra) - len(kept)}")
print(f"kept combined stars: {sum(r['stars'] for r in kept):,}")
from collections import Counter
print("kept by cat:   ", dict(Counter(r['cat'] for r in kept)))
print("kept by signal:", dict(Counter(r['signal'] for r in kept)))
print("\ntop 12 kept:")
for r in kept[:12]:
    print(f"  {r['stars']:>6}  {r['cat']:<6} {r['lang'] or '-':<11} {r['name']}")
