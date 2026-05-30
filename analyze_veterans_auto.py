#!/usr/bin/env python3
"""
analyze_veterans_auto.py — machine-detect dormant-reawakening developers.

For each GitHub owner in owners_chunk_N.json, query annual contribution
counts (2018-2026) via GraphQL. Flag accounts where:
  - Account created >= 3 years before 2026
  - 2021+2022+2023+2024 contributions < DORMANT_THRESH
  - 2026 contributions > REAWAKEN_THRESH

Usage:
  python analyze_veterans_auto.py --chunk owners_chunk_0.json --out vets_0.json
"""
import argparse, json, subprocess, time, sys

DORMANT_THRESH  = 20   # total contributions over 2021-2024
REAWAKEN_THRESH = 50   # 2026 contributions to count as reawakened
YEARS = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026]


def query_contributions(login: str, year: int) -> int | None:
    from_dt = f"{year}-01-01T00:00:00Z"
    to_dt   = f"{year}-12-31T23:59:59Z"
    gql = f"""
    query {{
      user(login: "{login}") {{
        createdAt
        contributionsCollection(from: "{from_dt}", to: "{to_dt}") {{
          contributionCalendar {{ totalContributions }}
        }}
      }}
    }}"""
    r = subprocess.run(
        ["gh", "api", "graphql", "-f", f"query={gql}"],
        capture_output=True, text=True, timeout=30,
    )
    if r.returncode != 0 or not r.stdout:
        return None
    try:
        d = json.loads(r.stdout)
        user = d.get("data", {}).get("user")
        if not user:
            return None
        count = user["contributionsCollection"]["contributionCalendar"]["totalContributions"]
        # stash createdAt on the first year query so caller can read it
        query_contributions._last_created = user.get("createdAt", "")
        return count
    except Exception:
        return None


def classify(login: str) -> dict:
    results = {"login": login, "years": {}, "created": "", "flag": ""}
    query_contributions._last_created = ""

    for year in YEARS:
        c = query_contributions(login, year)
        results["years"][year] = c
        if year == YEARS[0]:
            results["created"] = query_contributions._last_created[:10]
        time.sleep(0.5)   # be gentle — GraphQL rate limit is 5000 pts/hr

    y = results["years"]
    dormant_total = sum(v or 0 for k, v in y.items() if k in (2021, 2022, 2023, 2024))
    reawaken_2026 = y.get(2026) or 0

    created_year = int(results["created"][:4]) if results["created"] else 9999
    account_age  = 2026 - created_year

    if account_age >= 3 and dormant_total <= DORMANT_THRESH and reawaken_2026 >= REAWAKEN_THRESH:
        results["flag"] = "reawakened"
    elif account_age >= 3 and reawaken_2026 >= REAWAKEN_THRESH:
        results["flag"] = "veteran_active"
    elif created_year >= 2025:
        results["flag"] = "new_2025_26"
    else:
        results["flag"] = "regular"

    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chunk", required=True)
    ap.add_argument("--out",   required=True)
    args = ap.parse_args()

    owners = json.load(open(args.chunk))
    results = []
    for i, login in enumerate(owners):
        sys.stderr.write(f"  [{i+1}/{len(owners)}] {login}\n")
        results.append(classify(login))
        # write incrementally so partial results survive interruption
        json.dump(results, open(args.out, "w"), indent=2)

    counts = {}
    for r in results:
        counts[r["flag"]] = counts.get(r["flag"], 0) + 1
    sys.stderr.write(f"\nDone: {counts}\n")


if __name__ == "__main__":
    main()
