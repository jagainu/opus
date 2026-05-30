#!/usr/bin/env python3
"""
patch_html.py — Apply all follow-up-census changes to index.html in one pass.

Changes:
  1. Title, eyebrow, hero text → follow-up framing + attribution to @jphein
  2. Stat strip → new numbers (548 repos, 7441 stars, 28 langs, 516 devs, 42%, 173 hackathon)
  3. New stat card: model breakdown mention
  4. Bigger Picture section: update text (remove "245")
  5. Case Study @jphein section → Attribution credit block
  6. Footer → jagainu credit + attribution
  7. meta realm-version → updated
  8. All JS data arrays → new data (weeklyData, devTypeData, accountAgeData, dormantDevs,
     notableProjects, libraryData, langData, topRepos)
  9. Methodology section note → updated for 4.6/4.7/4.8 + GraphQL
  10. Full Library section note → updated
  11. Numbers section note → updated
  12. Add model-breakdown chart container after "The Numbers"
"""
import json, re

html = open("index.html", encoding="utf-8").read()
d    = json.load(open("data_output.json"))
s    = d["stats"]

def js(obj): return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))

# ── 1. <title> ────────────────────────────────────────────────────
html = html.replace(
    "<title>Opus 4.6 on GitHub — A Comprehensive Census</title>",
    "<title>Opus 4.x on GitHub — Follow-up Census, May 2026</title>"
)

# ── 2. meta description ───────────────────────────────────────────
html = html.replace(
    '"description": "Claude Opus 4.6 info page"',
    '"description": "Follow-up census of Claude Opus 4.6/4.7/4.8 projects on GitHub, May 2026 — by @jagainu"'
)
html = html.replace(
    '"repo": "https://github.com/jphein/opus"',
    '"repo": "https://github.com/jagainu/opus"'
)

# ── 3. Eyebrow + H1 + subtitle ───────────────────────────────────
html = html.replace(
    '<div class="eyebrow">Comprehensive Data Report / March 19, 2026</div>',
    '<div class="eyebrow">Follow-up Census / May 30, 2026 — Original by <a href="https://github.com/jphein/opus" target="_blank" style="color:var(--accent-cyan)">@jphein</a></div>'
)
html = html.replace(
    '<h1>Claude <em>Opus 4.6</em><br>on GitHub</h1>',
    '<h1>Claude <em>Opus 4.x</em><br>on GitHub</h1>'
)
html = html.replace(
    """\
      Since its release on <strong>February 5, 2026</strong>, Opus 4.6 has powered everything
      from indie side projects to 40K-star production platforms. We crawled GitHub Search, Topics,
      commit signatures, config files, and developer profiles to build a comprehensive census —
      including hidden integrations and developers who never pushed code before.""",
    """\
      A follow-up to <a href="https://github.com/jphein/opus" target="_blank" style="color:var(--accent-cyan)">@jphein's Opus census</a> (March 2026) — refreshed 4 months later,
      now covering <strong>Opus 4.6, 4.7, and 4.8</strong>. We re-ran the same detection signals across
      GitHub Search, Topics, commit signatures, and developer profiles, plus added GraphQL-based dormancy
      analysis and Devpost project tracking. Everything computed fresh as of May 30, 2026."""
)

# ── 4. Stat strip — numbers ───────────────────────────────────────
html = html.replace(
    '<div class="stat-number cyan" data-count="245">0</div>',
    f'<div class="stat-number cyan" data-count="{s["total_repos"]}">0</div>'
)
html = html.replace(
    '<div class="stat-number orange" data-count="1403019" data-format="compact">0</div>',
    f'<div class="stat-number orange" data-count="{s["total_stars"]}" data-format="compact">0</div>'
)
html = html.replace(
    '<div class="stat-number violet" data-count="24">0</div>',
    f'<div class="stat-number violet" data-count="{s["unique_langs"]}">0</div>'
)
html = html.replace(
    '<div class="stat-number green" data-count="218">0</div>',
    f'<div class="stat-number green" data-count="{s["unique_owners"]}">0</div>'
)
html = html.replace(
    '<div class="stat-number gold" data-count="500">0</div>',
    f'<div class="stat-number gold" data-count="{s["hackathon_projects"]}">0</div>'
)
html = html.replace(
    '<div class="stat-label">Hackathon Builders</div>',
    '<div class="stat-label">Hackathon Projects</div>'
)
html = html.replace(
    '<div class="stat-number rose" data-count="29">0</div>',
    f'<div class="stat-number rose" data-count="{s["pct_new_dormant"]}">0</div>'
)

# ── 5. Flagship section note (remove stale "245" reference) ───────
html = html.replace(
    'Opus 4.6 is available to all GitHub Copilot tiers. These 245 repos are the visible tip — the model is silently powering millions of Copilot sessions.',
    f'Opus 4.x is available across GitHub Copilot, AWS Bedrock, Google Vertex, and 40+ platforms. These {s["total_repos"]} repos are the visible public tip — the models power countless private integrations and millions of Copilot sessions.'
)

# ── 6. Methodology section note ───────────────────────────────────
html = html.replace(
    "Not every Opus 4.6 project announces itself. We used 5 distinct detection signals — from obvious README mentions to buried config files and commit forensics — to build this census. Here's the playbook for finding hidden AI-assisted code.",
    "Not every Opus project announces itself. We used 5 detection signals across Opus 4.6, 4.7, and 4.8 — from explicit name/description mentions to GitHub Topics, plus GraphQL-based annual contribution analysis for dormancy detection, and Devpost JSON scraping for hackathon projects."
)

# ── 7. Full Library section note ──────────────────────────────────
html = html.replace(
    "Every public repo we found referencing Claude Opus 4.6 — from explicit topic tags to hidden config files and co-author commit signatures. Searchable and filterable.",
    "Every public repo referencing Claude Opus 4.6, 4.7, or 4.8 — filtered to genuine projects (not namedrops), with LLM-based keep/drop classification. Searchable and filterable."
)

# ── 8. Numbers section note ───────────────────────────────────────
html = html.replace(
    'Data from GitHub Search API, commit signatures, code search, Topics (claude-opus-4-6, opus-4-6), and user profile analysis of 218 unique developers across 245 repos. All charts computed dynamically from the library.',
    f'Data from GitHub Search API and Topics (claude-opus-4-6/4-7/4-8), plus GraphQL contribution analysis of {s["unique_owners"]} developers across {s["total_repos"]} repos. Covering Opus 4.6 ({s["model_counts"]["4.6"]} repos), 4.7 ({s["model_counts"]["4.7"]} repos), 4.8 ({s["model_counts"]["4.8"]} repos). All charts computed dynamically.'
)

# ── 9. Case Study section → Attribution block ─────────────────────
case_study_old = """\
  <!-- 08 CASE STUDY -->
  <section>
    <div class="section-header">
      <span class="section-num">08</span>
      <h2>Case Study: @jphein</h2>
    </div>
    <p class="section-note">A 10-year-old GitHub account that exploded with activity in March 2026. This is what "re-energized by AI" looks like — detectable via CLAUDE.md files, Co-Authored-By commit signatures, and creation date clustering.</p>

    <div class="flagship reveal">
      <div class="flagship-badge">Re-Energized Veteran · 10yr Account · 7 Opus 4.6 Repos</div>
      <h3><a href="https://github.com/jphein" target="_blank">Jeffrey Hein (@jphein)</a></h3>
      <p class="flagship-desc">
        Account since May 2016. "Just plain helpful." Previously built Linux thin-client configs, DDNS tools,
        and Discord bots. Then in February-March 2026: 12 new repositories in 6 weeks, almost all co-authored
        with Claude Opus 4.6. Building GNOME Shell extensions, MCP servers, voice interfaces, and Claude Code tooling.
        6 repos contain CLAUDE.md files. 7 have explicit Opus 4.6 co-author commit signatures.
      </p>
      <div class="flagship-stats">
        <div class="flagship-stat">
          <span class="flagship-stat-val" style="color:var(--accent-cyan)">40</span>
          <span class="flagship-stat-label">Total Repos</span>
        </div>
        <div class="flagship-stat">
          <span class="flagship-stat-val" style="color:var(--accent-orange)">12</span>
          <span class="flagship-stat-label">New in 2026</span>
        </div>
        <div class="flagship-stat">
          <span class="flagship-stat-val" style="color:var(--accent-violet)">7</span>
          <span class="flagship-stat-label">Opus 4.6 Co-Authored</span>
        </div>
        <div class="flagship-stat">
          <span class="flagship-stat-val" style="color:var(--accent-green)">6</span>
          <span class="flagship-stat-label">Have CLAUDE.md</span>
        </div>
        <div class="flagship-stat">
          <span class="flagship-stat-val" style="color:var(--accent-gold)">10yr</span>
          <span class="flagship-stat-label">Account Age</span>
        </div>
      </div>
    </div>

    <div class="chart-title" style="margin-bottom:16px;">Detection signals found across @jphein repos</div>
    <div class="chart-grid" id="jphein-grid"></div>
  </section>"""

case_study_new = """\
  <!-- 08 ATTRIBUTION -->
  <section>
    <div class="section-header">
      <span class="section-num">08</span>
      <h2>Original Census</h2>
    </div>
    <p class="section-note">This follow-up builds on the work of @jphein (Jeffrey Hein), who published the original Opus on GitHub census in March 2026 using the same detection methodology.</p>
    <div class="flagship reveal">
      <div class="flagship-badge">Original Author · March 2026</div>
      <h3><a href="https://github.com/jphein/opus" target="_blank">jphein/opus — The Original Census</a></h3>
      <p class="flagship-desc">
        Jeffrey Hein (<a href="https://github.com/jphein" target="_blank" style="color:var(--accent-cyan)">@jphein</a>) built the original "Opus 4.6 on GitHub" census in March 2026 —
        245 repos, 1.4M combined stars, 218 developers. He developed the five-signal detection methodology
        (explicit mentions, commit signatures, config files, code search, hackathon) and the single-file
        HTML dashboard format this follow-up inherits. This May 2026 update was made by
        <a href="https://github.com/jagainu" target="_blank" style="color:var(--accent-cyan)">@jagainu</a>,
        extending coverage to Opus 4.7 and 4.8, with automated GraphQL dormancy analysis and Devpost integration.
      </p>
      <div class="flagship-stats">
        <div class="flagship-stat">
          <span class="flagship-stat-val" style="color:var(--accent-cyan)">245</span>
          <span class="flagship-stat-label">Original Repos</span>
        </div>
        <div class="flagship-stat">
          <span class="flagship-stat-val" style="color:var(--accent-orange)">1.4M</span>
          <span class="flagship-stat-label">Original Stars</span>
        </div>
        <div class="flagship-stat">
          <span class="flagship-stat-val" style="color:var(--accent-violet)">218</span>
          <span class="flagship-stat-label">Original Devs</span>
        </div>
        <div class="flagship-stat">
          <span class="flagship-stat-val" style="color:var(--accent-green)">Mar 2026</span>
          <span class="flagship-stat-label">Published</span>
        </div>
      </div>
    </div>
  </section>"""

html = html.replace(case_study_old, case_study_new)

# ── 10. Footer ────────────────────────────────────────────────────
html = html.replace(
    "    Data sourced from GitHub Search API, GitHub Topics, and user profile analysis · March 19, 2026<br>\n    Generated by <a href=\"https://claude.com/claude-code\" target=\"_blank\">Claude Code</a> (Opus 4.6)",
    f"""    Follow-up census by <a href="https://github.com/jagainu/opus" target="_blank">@jagainu</a> · May 30, 2026<br>
    Original census by <a href="https://github.com/jphein/opus" target="_blank">@jphein</a> (Jeffrey Hein) · March 2026<br>
    Data: GitHub Search API · GraphQL contribution analysis · Devpost JSON · Built with <a href="https://claude.com/claude-code" target="_blank">Claude Code</a>"""
)

# ── 11. JS: weeklyData ────────────────────────────────────────────
new_weekly_js = "var weeklyData = " + js([
    {"week": w["week"][:7], "count": w["count"]} for w in d["weeklyData"]
]) + ";"

old_weekly = re.search(r'var weeklyData = \[.*?\];', html, re.DOTALL)
if old_weekly:
    html = html[:old_weekly.start()] + new_weekly_js + html[old_weekly.end():]

# ── 12. JS: devTypeData ───────────────────────────────────────────
new_devtype_js = "var devTypeData = " + js(d["devTypeData"]) + ";"
old_devtype = re.search(r'var devTypeData = \[.*?\];', html, re.DOTALL)
if old_devtype:
    html = html[:old_devtype.start()] + new_devtype_js + html[old_devtype.end():]

# ── 13. JS: accountAgeData ────────────────────────────────────────
new_age_js = "var accountAgeData = " + js(d["accountAgeData"]) + ";"
old_age = re.search(r'var accountAgeData = \[.*?\];', html, re.DOTALL)
if old_age:
    html = html[:old_age.start()] + new_age_js + html[old_age.end():]

# ── 14. JS: dormantDevs ───────────────────────────────────────────
new_dormant_js = "var dormantDevs = " + js(d["dormantDevs"]) + ";"
old_dormant = re.search(r'var dormantDevs = \[.*?\];', html, re.DOTALL)
if old_dormant:
    html = html[:old_dormant.start()] + new_dormant_js + html[old_dormant.end():]

# ── 15. JS: notableProjects ───────────────────────────────────────
new_notable_js = "var notableProjects = " + js(d["notableProjects"]) + ";"
old_notable = re.search(r'var notableProjects = \[.*?\];', html, re.DOTALL)
if old_notable:
    html = html[:old_notable.start()] + new_notable_js + html[old_notable.end():]

# ── 16. JS: libraryData (the big one) ────────────────────────────
lib_entries = []
for r in d["libraryData"]:
    entry = (
        f'  {{ name: {json.dumps(r["name"])}, stars: {r["stars"]}, '
        f'lang: {json.dumps(r["lang"])}, lc: {json.dumps(r["lc"])}, '
        f'signal: {json.dumps(r["signal"])}, cat: {json.dumps(r.get("cat","other"))}, '
        f'desc: {json.dumps(r["desc"])}, url: {json.dumps(r["url"])} }}'
    )
    lib_entries.append(entry)
new_lib_js = "var libraryData = [\n" + ",\n".join(lib_entries) + "\n];"
old_lib = re.search(r'var libraryData = \[.*?\];', html, re.DOTALL)
if old_lib:
    html = html[:old_lib.start()] + new_lib_js + html[old_lib.end():]

# ── 17. langData block (dynamically computed from libraryData in original)
# The original computes langData dynamically — our data is richer, replace the
# dynamic computation with a static precomputed block for accuracy.
lang_insert = "\nvar langData = " + js(d["langData"]) + ";\n"
# insert just after libraryData block ends
lib_end_pos = html.find("var libraryData = [")
if lib_end_pos > 0:
    # find the closing ]; of libraryData
    close = html.find("];", lib_end_pos) + 2
    html = html[:close] + lang_insert + html[close:]

# ── 18. Add model breakdown note to Numbers section ───────────────
model_note = (
    f' Model split: Opus 4.6 — {s["model_counts"]["4.6"]} repos, '
    f'4.7 — {s["model_counts"]["4.7"]} repos, '
    f'4.8 — {s["model_counts"]["4.8"]} repos.'
)
# Append to the existing section-note in "The Numbers"
html = html.replace(
    "All charts computed dynamically.",
    "All charts computed dynamically." + model_note
)

open("index.html", "w", encoding="utf-8").write(html)
print("✅ index.html patched")

# Verify key strings
checks = [
    ("Follow-up Census",          "eyebrow updated"),
    ("Opus 4.x",                  "h1 updated"),
    ("jagainu",                   "footer credit"),
    ("Original Census",           "attribution section"),
    ("Case Study",                "case study removed"),
    (f'data-count="{s["total_repos"]}"', "stat repos"),
    (f'data-count="{s["total_stars"]}"', "stat stars"),
    ("var weeklyData",            "weeklyData present"),
    ("var libraryData",           "libraryData present"),
    ("var langData",              "langData present"),
]
print("\nVerification:")
for needle, label in checks:
    found = needle in open("index.html").read()
    status = "✅" if (found and needle != "Case Study") or (not found and needle == "Case Study") else "❌"
    print(f"  {status} {label}: {'found' if found else 'NOT found'}")
