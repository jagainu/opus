#!/usr/bin/env python3
"""Fix JS issues in index.html after the follow-up census patch."""
import json, re

html = open("index.html", encoding="utf-8").read()
data = json.load(open("data_output.json"))

def js(obj): return json.dumps(obj, ensure_ascii=False)

# ── Fix 1: SIGNAL_LABELS/CLASSES — add new signal aliases ─────────
# explicit7/explicit8/topic46/47/48 all map to "Explicit" display label
old_signal_labels = """\
var SIGNAL_LABELS = {
  explicit: 'Explicit',
  config: 'Config',
  commit: 'Co-Author',
  under: 'Under Hood',
  hackathon: 'Hackathon'
};
var SIGNAL_CLASSES = {
  explicit: 'signal-explicit',
  config: 'signal-config',
  commit: 'signal-commit',
  under: 'signal-under',
  hackathon: 'signal-hackathon'
};"""
new_signal_labels = """\
var SIGNAL_LABELS = {
  explicit: 'Explicit', explicit7: 'Explicit', explicit8: 'Explicit',
  topic46: 'Topic', topic47: 'Topic', topic48: 'Topic',
  config: 'Config', commit: 'Co-Author', under: 'Under Hood', hackathon: 'Hackathon'
};
var SIGNAL_CLASSES = {
  explicit: 'signal-explicit', explicit7: 'signal-explicit', explicit8: 'signal-explicit',
  topic46: 'signal-config', topic47: 'signal-config', topic48: 'signal-config',
  config: 'signal-config', commit: 'signal-commit',
  under: 'signal-under', hackathon: 'signal-hackathon'
};"""
html = html.replace(old_signal_labels, new_signal_labels)

# ── Fix 2: r._cat → r.cat throughout renderLibrary ────────────────
# (the data has 'cat' not '_cat')
html = html.replace("CAT_LABELS[r._cat] || r._cat", "CAT_LABELS[r.cat] || r.cat")
html = html.replace("r._cat || 'zzz'", "r.cat || 'zzz'")
html = html.replace("(CAT_LABELS[d._cat] || '')", "(CAT_LABELS[d.cat] || '')")

# ── Fix 3: signalCounts — aggregate new signal names ──────────────
old_signal_counts = """\
  var signalCounts = { explicit: 0, under: 0, commit: 0, config: 0, hackathon: 0 };
  libraryData.forEach(function(r) { signalCounts[r.signal]++; });"""
new_signal_counts = """\
  var signalCounts = { explicit: 0, under: 0, commit: 0, config: 0, hackathon: 0 };
  libraryData.forEach(function(r) {
    var sig = r.signal;
    // normalise new signal names into the 5 original buckets
    if (sig === 'explicit7' || sig === 'explicit8') sig = 'explicit';
    if (sig === 'topic46' || sig === 'topic47' || sig === 'topic48') sig = 'config';
    if (signalCounts[sig] !== undefined) signalCounts[sig]++;
  });"""
html = html.replace(old_signal_counts, new_signal_counts)

# ── Fix 4: renderHackathonWinners — use Devpost data ──────────────
winners = data["hackathonWinners"][:12]  # top 12 by likes
new_render_hackathon = """\
function renderHackathonWinners() {
  var c = document.getElementById('hackathon-winners');
  if (!c) return;
  var winners = """ + js(winners) + """;
  var title = el('div', { style: { fontSize: '9px', letterSpacing: '3px', textTransform: 'uppercase', color: 'var(--accent-gold)', marginBottom: '16px', marginTop: '24px' }, textContent: 'Hackathon Winners (Devpost)' });
  c.appendChild(title);
  winners.forEach(function(w, i) {
    var colors = ['var(--accent-gold)','#c0c0c0','#cd7f32','var(--accent-cyan)','var(--accent-violet)','var(--accent-green)','var(--accent-orange)'];
    var col = colors[i % colors.length];
    var badge = el('span', { style: { display: 'inline-block', fontSize: '9px', letterSpacing: '2px', textTransform: 'uppercase', color: col, border: '1px solid ' + col, padding: '2px 8px', marginRight: '10px', fontFamily: 'var(--font-mono)' }, textContent: w.likes ? w.likes + ' \\u2665' : 'Winner' });
    var name = el('a', { href: w.url, target: '_blank', style: { fontFamily: 'var(--font-serif)', fontSize: '16px', color: 'var(--text-main)', textDecoration: 'none' }, textContent: w.name });
    var tags = (w.tags || []).slice(0, 4).map(function(t) {
      return el('span', { style: { fontSize: '9px', color: 'var(--text-dim)', border: '1px solid var(--border)', padding: '1px 6px', marginLeft: '4px', borderRadius: '2px' }, textContent: t });
    });
    var tagRow = el('div', { style: { marginTop: '4px' } }, tags);
    var desc = el('div', { style: { fontSize: '11px', color: 'var(--text-dim)', lineHeight: '1.6', marginTop: '4px' }, textContent: w.tagline || '' });
    var row = el('div', { style: { padding: '12px 0', borderBottom: '1px solid var(--border)' } }, [el('div', {}, [badge, name]), desc, tagRow]);
    c.appendChild(row);
  });
}"""

old_render_hackathon = re.search(
    r'function renderHackathonWinners\(\) \{.*?\n\}', html, re.DOTALL
)
if old_render_hackathon:
    html = html[:old_render_hackathon.start()] + new_render_hackathon + html[old_render_hackathon.end():]

# ── Fix 5: renderJpheinGrid — remove dead call (grid element gone) ─
html = html.replace("  renderJpheinGrid();\n", "")

# ── Fix 6: filterMap — add explicit7/8/topic aliases to 'Explicit' ─
old_filter = "'Explicit': 'explicit', 'Under Hood': 'under', 'Hackathon': 'hackathon', 'Config': 'config', 'Co-Author': 'commit'"
new_filter = "'Explicit': ['explicit','explicit7','explicit8'], 'Under Hood': 'under', 'Hackathon': 'hackathon', 'Config': ['config','topic46','topic47','topic48'], 'Co-Author': 'commit'"
html = html.replace(old_filter, new_filter)

# and fix the filter match (activeFilter may now be an array)
old_match = "var matchesFilter = !activeFilter || d.signal === activeFilter;"
new_match = "var matchesFilter = !activeFilter || (Array.isArray(activeFilter) ? activeFilter.indexOf(d.signal) !== -1 : d.signal === activeFilter);"
html = html.replace(old_match, new_match)

# ── Fix 7: hackathon-box text (stale "321 projects" reference) ────
html = html.replace(
    "321 projects across 14 hackathons worldwide: London, Toronto, Cambridge, Maryland, USC, UW Seattle, Georgia Tech, Rice, UCSD, UF, SK AI Summit Korea, and more. From medical AI to financial modeling to educational tools.",
    f"173 projects tracked on Devpost referencing Claude Opus — 21 hackathon winners across multiple events. Tags: python, typescript, react, claude, fastapi, next.js and more."
)

open("index.html", "w", encoding="utf-8").write(html)
print("✅ fix_js.py applied")

# Verification
checks = [
    ("explicit7: 'Explicit'",          "SIGNAL_LABELS extended"),
    ("CAT_LABELS[r.cat] || r.cat",     "r._cat → r.cat fixed"),
    ("normalise new signal names",     "signalCounts normalised"),
    ("Devpost",                        "renderHackathonWinners updated"),
    ("Array.isArray(activeFilter)",    "filter array match fixed"),
]
content = open("index.html").read()
for needle, label in checks:
    print(f"  {'✅' if needle in content else '❌'} {label}")
