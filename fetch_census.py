#!/usr/bin/env python3
"""
fetch_census.py — Automated GitHub census fetcher for the Opus dashboard.

Replaces the manual curation step with a deterministic pipeline:
  1. Query GitHub Search API across all detection signals, sorted by stars
  2. Dedupe by full_name, keeping the strongest signal
  3. Map language -> GitHub Linguist color
  4. Filter obvious noise (forks, archived, no description)
  5. Emit candidates.json (for the classify stage) + a stats summary

The LLM "classify" stage (keep/drop + category) runs separately on candidates.json.

Usage:
  python3 fetch_census.py --pages 3            # ~300 repos/signal max
  python3 fetch_census.py --pages 1 --quick    # fast smoke test
"""
import argparse
import json
import subprocess
import sys
import time

# Detection signals -> GitHub repository-search queries (high rate limit: 30/min).
# Each repo is tagged with the FIRST signal (by this priority order) that finds it.
SIGNALS = [
    ("explicit",  '"opus 4.6" in:name,description fork:false archived:false'),
    ("explicit7", '"opus 4.7" in:name,description fork:false archived:false'),
    ("explicit8", '"opus 4.8" in:name,description fork:false archived:false'),
    ("topic46",   'topic:claude-opus-4-6 fork:false'),
    ("topic47",   'topic:claude-opus-4-7 fork:false'),
    ("topic48",   'topic:claude-opus-4-8 fork:false'),
]

# Standard GitHub Linguist colors for languages that appear in this domain.
LANG_COLORS = {
    "Python": "#3572A5", "JavaScript": "#f1e05a", "TypeScript": "#3178c6",
    "Rust": "#dea584", "Go": "#00ADD8", "Shell": "#89e051", "HTML": "#e34c26",
    "CSS": "#563d7c", "C": "#555555", "C++": "#f34b7d", "C#": "#178600",
    "Java": "#b07219", "Kotlin": "#A97BFF", "Swift": "#F05138", "Ruby": "#701516",
    "Dart": "#00B4AB", "Svelte": "#ff3e00", "Vue": "#41b883", "PHP": "#4F5D95",
    "R": "#198CE7", "Crystal": "#000100", "Lua": "#000080", "Zig": "#ec915c",
    "Jupyter Notebook": "#DA5B0B", "Elixir": "#6e4a7e", "Haskell": "#5e5086",
    "Nix": "#7e7eff", "Makefile": "#427819", "Dockerfile": "#384d54",
}


def gh_search(query, pages, per_page=100):
    """Paginate the repository search API, sorted by stars desc."""
    items = []
    for page in range(1, pages + 1):
        try:
            out = subprocess.run(
                ["gh", "api", "-X", "GET", "search/repositories",
                 "-f", f"q={query}", "-f", "sort=stars", "-f", "order=desc",
                 "-f", f"per_page={per_page}", "-f", f"page={page}"],
                capture_output=True, text=True, timeout=60,
            )
            if out.returncode != 0:
                sys.stderr.write(f"  ! page {page} failed: {out.stderr.strip()[:120]}\n")
                break
            data = json.loads(out.stdout)
            batch = data.get("items", [])
            items.extend(batch)
            if len(batch) < per_page:
                break  # last page
            time.sleep(2.2)  # stay under 30 req/min
        except subprocess.TimeoutExpired:
            sys.stderr.write(f"  ! page {page} timed out\n")
            break
    return items


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", type=int, default=2, help="max pages per signal (100/page)")
    ap.add_argument("--quick", action="store_true", help="1 page, first 2 signals only")
    ap.add_argument("--out", default="candidates.json")
    args = ap.parse_args()

    signals = SIGNALS[:2] if args.quick else SIGNALS
    pages = 1 if args.quick else args.pages

    pool = {}  # full_name -> record (first signal wins = strongest)
    for signal, query in signals:
        sys.stderr.write(f"[{signal}] {query}\n")
        for it in gh_search(query, pages):
            name = it["full_name"]
            if name in pool:
                continue  # already tagged by a stronger signal
            lang = it.get("language") or ""
            pool[name] = {
                "name": name,
                "owner": it["owner"]["login"],
                "stars": it.get("stargazers_count", 0),
                "lang": lang,
                "lc": LANG_COLORS.get(lang, "#666"),
                "signal": signal,
                "desc": (it.get("description") or "").strip(),
                "created": (it.get("created_at") or "")[:10],
                "url": it.get("html_url", ""),
                "archived": it.get("archived", False),
                "fork": it.get("fork", False),
            }
        sys.stderr.write(f"  pool size: {len(pool)}\n")

    # Light deterministic filter; the heavy keep/drop judgment is the LLM stage.
    candidates = [r for r in pool.values() if r["desc"] and not r["fork"]]
    candidates.sort(key=lambda r: r["stars"], reverse=True)

    with open(args.out, "w") as f:
        json.dump(candidates, f, indent=2, ensure_ascii=False)

    # Summary
    by_signal = {}
    by_lang = {}
    for r in candidates:
        by_signal[r["signal"]] = by_signal.get(r["signal"], 0) + 1
        key = r["lang"] or "(none)"
        by_lang[key] = by_lang.get(key, 0) + 1
    total_stars = sum(r["stars"] for r in candidates)

    sys.stderr.write("\n=== SUMMARY ===\n")
    sys.stderr.write(f"candidates written: {len(candidates)} -> {args.out}\n")
    sys.stderr.write(f"combined stars: {total_stars:,}\n")
    sys.stderr.write(f"by signal: {by_signal}\n")
    top_langs = sorted(by_lang.items(), key=lambda x: -x[1])[:8]
    sys.stderr.write(f"top languages: {top_langs}\n")
    sys.stderr.write("\ntop 15 candidates (pre-classification):\n")
    for r in candidates[:15]:
        sys.stderr.write(f"  {r['stars']:>6}  {r['lang'] or '-':<12} {r['name']}\n")


if __name__ == "__main__":
    main()
