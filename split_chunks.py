#!/usr/bin/env python3
"""Split candidates.json into N chunks for parallel classification agents."""
import json, math, sys

N = int(sys.argv[1]) if len(sys.argv) > 1 else 6
data = json.load(open("candidates.json"))
size = math.ceil(len(data) / N)
for i in range(N):
    chunk = data[i*size:(i+1)*size]
    if not chunk:
        continue
    # Keep only the fields the classifier needs to judge + identity
    slim = [{"name": r["name"], "stars": r["stars"], "lang": r["lang"],
             "signal": r["signal"], "desc": r["desc"]} for r in chunk]
    json.dump(slim, open(f"chunk_{i}.json", "w"), indent=1, ensure_ascii=False)
    print(f"chunk_{i}.json: {len(slim)} repos")
print(f"total: {len(data)} across {N} chunks (~{size}/chunk)")
