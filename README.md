# Opus 4.x on GitHub — Follow-up Census, May 2026

A follow-up to [@jphein's Opus census](https://github.com/jphein/opus) (March 2026), refreshed 4 months later and extended to cover **Opus 4.6, 4.7, and 4.8**.

**Live site:** [jagainu.github.io/opus](https://jagainu.github.io/opus/)
**Original census:** [jphein/opus](https://github.com/jphein/opus) by Jeffrey Hein (@jphein), March 2026

---

## What Changed from the Original

| | Original (Mar 2026) | This follow-up (May 2026) |
|---|---|---|
| Models covered | Opus 4.6 only | **4.6 + 4.7 + 4.8** |
| Repos tracked | 245 | **548** |
| Combined stars | 1.4M | 7,441 (noise-filtered) |
| Developers | 218 | **516** |
| % New/Dormant | 29% | **42%** |
| Hackathon projects | 500 builders | **173 projects, 21 winners** |
| Dormancy detection | Manual user list | **GraphQL contributionsCollection (automated)** |
| Devpost scraping | Manual | **Playwright + JSON XHR (automated)** |

## The Numbers

- **548** public repos tracked
- **7,441** combined stars (noise-filtered; excludes namedrops like gpt4free)
- **28** programming languages
- **516** unique developers
- **42%** new or previously dormant developers
- **59** reawakened veterans (dormant 2021–2024, active 2026)
- **173** Devpost hackathon projects, **21** winners

## Detection Methodology

Same 5-signal approach as the original, now automated end-to-end:

| Signal | Method |
|--------|--------|
| `explicit` | Repo name/description mentions Opus 4.6, 4.7, or 4.8 |
| `topic` | GitHub topic tags `claude-opus-4-6/4-7/4-8` |
| LLM classification | keep/drop + category for all 621 raw candidates |
| GraphQL dormancy | `contributionsCollection` per year per developer |
| Devpost | Playwright + JSON XHR scraping for hackathon projects & winners |

## Attribution

Original census concept, detection methodology, and dashboard design by **Jeffrey Hein ([@jphein](https://github.com/jphein))**, March 2026.

This follow-up was built by **[@jagainu](https://github.com/jagainu)** using Claude Code, extending the original with automated data pipelines, multi-model coverage (4.6/4.7/4.8), and updated data as of May 30, 2026.

## Tech

- Zero dependencies — pure HTML/CSS/JS in a single `index.html`
- All charts rendered via DOM + inline SVG
- Dark editorial theme: JetBrains Mono + Instrument Serif
- Data pipeline: Python scripts (`fetch_census.py`, `analyze_veterans_auto.py`, `build_data.py`)
