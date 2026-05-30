#!/usr/bin/env python3
import json, math, sys
N = int(sys.argv[1]) if len(sys.argv) > 1 else 6
owners = json.load(open("owners.json"))
size = math.ceil(len(owners) / N)
for i in range(N):
    chunk = owners[i*size:(i+1)*size]
    if not chunk:
        continue
    json.dump(chunk, open(f"owners_chunk_{i}.json", "w"))
    print(f"owners_chunk_{i}.json: {len(chunk)}")
