#!/usr/bin/env python3
"""
add_i18n.py — Add Japanese/English toggle to index.html.

Approach:
  1. Add data-i18n="key" attributes to all translatable HTML elements
  2. Inject a TRANSLATIONS object + toggle button + applyLang() into the JS
  3. Static data (repo names, descriptions in library) stays untouched

Only UI chrome is translated:
  - eyebrow, h1 subtitle, section headers (h2), section notes
  - stat labels, chart titles, flagship labels, filter/search UI
  - CAT_LABELS, SIGNAL_LABELS (JS objects)
  - footer
"""
import re

html = open("index.html", encoding="utf-8").read()

# ── Step 1: add data-i18n attrs to HTML elements ──────────────────

REPLACEMENTS = [
    # eyebrow
    ('Follow-up Census / May 30, 2026 — Original by',
     'data-i18n="eyebrow" Follow-up Census / May 30, 2026 — Original by'),

    # h1 subtitle
    ('<p class="subtitle">',
     '<p class="subtitle" data-i18n="subtitle">'),

    # stat labels
    ('<div class="stat-label">Public Repos</div>',
     '<div class="stat-label" data-i18n="stat_repos">Public Repos</div>'),
    ('<div class="stat-label">Combined Stars</div>',
     '<div class="stat-label" data-i18n="stat_stars">Combined Stars</div>'),
    ('<div class="stat-label">Languages</div>',
     '<div class="stat-label" data-i18n="stat_langs">Languages</div>'),
    ('<div class="stat-label">Developers</div>',
     '<div class="stat-label" data-i18n="stat_devs">Developers</div>'),
    ('<div class="stat-label">Hackathon Projects</div>',
     '<div class="stat-label" data-i18n="stat_hackathon">Hackathon Projects</div>'),
    ('<div class="stat-label">% New/Dormant Devs</div>',
     '<div class="stat-label" data-i18n="stat_dormant">% New/Dormant Devs</div>'),

    # section headers
    ('<h2>The Flagship</h2>',      '<h2 data-i18n="h2_flagship">The Flagship</h2>'),
    ('<h2>The Numbers</h2>',       '<h2 data-i18n="h2_numbers">The Numbers</h2>'),
    ('<h2>Who\'s Building</h2>',   '<h2 data-i18n="h2_building">Who\'s Building</h2>'),
    ('<h2>The Hackathon</h2>',     '<h2 data-i18n="h2_hackathon">The Hackathon</h2>'),
    ('<h2>Top Repositories</h2>',  '<h2 data-i18n="h2_top">Top Repositories</h2>'),
    ('<h2>Notable Projects</h2>',  '<h2 data-i18n="h2_notable">Notable Projects</h2>'),
    ('<h2>The Bigger Picture</h2>','<h2 data-i18n="h2_bigger">The Bigger Picture</h2>'),
    ('<h2>Original Census</h2>',   '<h2 data-i18n="h2_original">Original Census</h2>'),
    ('<h2>How We Found Them</h2>', '<h2 data-i18n="h2_method">How We Found Them</h2>'),
    ('<h2>The Full Library</h2>',  '<h2 data-i18n="h2_library">The Full Library</h2>'),

    # section notes (use class+content match)
    ('plus GraphQL contribution analysis of 516 developers across 548 repos. Covering Opus 4.6 (257 repos), 4.7 (264 repos), 4.8 (27 repos). All charts computed dynamically. Model split: Opus 4.6 — 257 repos, 4.7 — 264 repos, 4.8 — 27 repos.',
     'plus GraphQL contribution analysis of 516 developers across 548 repos. Covering Opus 4.6 (257 repos), 4.7 (264 repos), 4.8 (27 repos). All charts computed dynamically. Model split: Opus 4.6 — 257 repos, 4.7 — 264 repos, 4.8 — 27 repos.</p>\n    <p class="section-note" data-i18n="note_numbers" style="display:none">'),

    # flagship badge
    ('<div class="flagship-badge">Anthropic Official · 100% AI-Authored</div>',
     '<div class="flagship-badge" data-i18n="badge_flagship">Anthropic Official · 100% AI-Authored</div>'),

    # flagship stat labels
    ('<span class="flagship-stat-label">Stars</span>',
     '<span class="flagship-stat-label" data-i18n="fsl_stars">Stars</span>'),
    ('<span class="flagship-stat-label">Forks</span>',
     '<span class="flagship-stat-label" data-i18n="fsl_forks">Forks</span>'),
    ('<span class="flagship-stat-label">Commits</span>',
     '<span class="flagship-stat-label" data-i18n="fsl_commits">Commits</span>'),
    ('<span class="flagship-stat-label">Rust</span>',
     '<span class="flagship-stat-label" data-i18n="fsl_lang">Rust</span>'),
    ('<span class="flagship-stat-label">Projects Compiled</span>',
     '<span class="flagship-stat-label" data-i18n="fsl_compiled">Projects Compiled</span>'),
    ('<span class="flagship-stat-label">Original Repos</span>',
     '<span class="flagship-stat-label" data-i18n="fsl_orig_repos">Original Repos</span>'),
    ('<span class="flagship-stat-label">Original Stars</span>',
     '<span class="flagship-stat-label" data-i18n="fsl_orig_stars">Original Stars</span>'),
    ('<span class="flagship-stat-label">Original Devs</span>',
     '<span class="flagship-stat-label" data-i18n="fsl_orig_devs">Original Devs</span>'),
    ('<span class="flagship-stat-label">Published</span>',
     '<span class="flagship-stat-label" data-i18n="fsl_published">Published</span>'),

    # original census badge
    ('<div class="flagship-badge">Original Author · March 2026</div>',
     '<div class="flagship-badge" data-i18n="badge_original">Original Author · March 2026</div>'),
]

for old, new in REPLACEMENTS:
    if old in html:
        html = html.replace(old, new, 1)
    else:
        print(f"  WARN: not found: {old[:60]!r}")

# ── Step 2: add data-i18n to chart-title divs (by content) ────────
CHART_TITLES = {
    'Repos created per week (since release)': 'ct_weekly',
    'Language distribution (14 languages)':  'ct_lang',
    'Star distribution':                      'ct_stars',
    'Project categories':                     'ct_cats',
    'Developer type breakdown':               'ct_devtype',
    'Account age distribution':               'ct_age',
}
for text, key in CHART_TITLES.items():
    old = f'<div class="chart-title">{text}</div>'
    new = f'<div class="chart-title" data-i18n="{key}">{text}</div>'
    html = html.replace(old, new, 1)

CHART_TITLES_STYLE = {
    'Dormant accounts awakened — old GitHub accounts, barely used until Opus 4.6': 'ct_dormant',
    'Brand new accounts — created in 2026, building with AI from day one':          'ct_new',
}
for text, key in CHART_TITLES_STYLE.items():
    html = html.replace(
        f'<div class="chart-title" style',
        f'<div class="chart-title" data-i18n="{key}" style', 1
    )

# ── Step 3: inject toggle button (after <body>) ────────────────────
toggle_btn_css = """
  .lang-toggle { position: fixed; top: 16px; right: 16px; z-index: 999;
    background: var(--surface-2); border: 1px solid var(--border);
    color: var(--text-dim); font-family: var(--font-mono); font-size: 10px;
    padding: 6px 12px; cursor: pointer; letter-spacing: 1px;
    text-transform: uppercase; transition: all 0.2s; border-radius: 2px; }
  .lang-toggle:hover { border-color: var(--accent-cyan); color: var(--accent-cyan); }
"""
html = html.replace(
    "  ::-webkit-scrollbar { width: 6px; }",
    "  ::-webkit-scrollbar { width: 6px; }\n" + toggle_btn_css
)

html = html.replace(
    "<div class=\"container\">",
    '<button class="lang-toggle" id="lang-toggle" onclick="toggleLang()">日本語</button>\n<div class="container">',
    1
)

# ── Step 4: inject TRANSLATIONS + applyLang() before </script> ────
translations_js = r"""
// ── i18n ──────────────────────────────────────────────────────────
var LANG = 'en';

var TRANSLATIONS = {
  en: {
    toggle_btn:    '日本語',
    eyebrow:       'Follow-up Census / May 30, 2026 — Original by',
    subtitle:      'A follow-up to <a href="https://github.com/jphein/opus" target="_blank" style="color:var(--accent-cyan)">@jphein’s Opus census</a> (March 2026) — refreshed 4 months later, now covering <strong>Opus 4.6, 4.7, and 4.8</strong>. We re-ran the same detection signals across GitHub Search, Topics, commit signatures, and developer profiles, plus added GraphQL-based dormancy analysis and Devpost project tracking. Everything computed fresh as of May 30, 2026.',
    stat_repos:    'Public Repos',
    stat_stars:    'Combined Stars',
    stat_langs:    'Languages',
    stat_devs:     'Developers',
    stat_hackathon:'Hackathon Projects',
    stat_dormant:  '% New/Dormant Devs',
    h2_flagship:   'The Flagship',
    h2_numbers:    'The Numbers',
    h2_building:   "Who's Building",
    h2_hackathon:  'The Hackathon',
    h2_top:        'Top Repositories',
    h2_notable:    'Notable Projects',
    h2_bigger:     'The Bigger Picture',
    h2_original:   'Original Census',
    h2_method:     'How We Found Them',
    h2_library:    'The Full Library',
    badge_flagship:'Anthropic Official · 100% AI-Authored',
    badge_original:'Original Author · March 2026',
    fsl_stars:     'Stars',
    fsl_forks:     'Forks',
    fsl_commits:   'Commits',
    fsl_lang:      'Rust',
    fsl_compiled:  'Projects Compiled',
    fsl_orig_repos:'Original Repos',
    fsl_orig_stars:'Original Stars',
    fsl_orig_devs: 'Original Devs',
    fsl_published: 'Published',
    ct_weekly:     'Repos created per week (since release)',
    ct_lang:       'Language distribution (14 languages)',
    ct_stars:      'Star distribution',
    ct_cats:       'Project categories',
    ct_devtype:    'Developer type breakdown',
    ct_age:        'Account age distribution',
    ct_dormant:    'Dormant accounts awakened — old GitHub accounts, barely used until Opus 4.6',
    ct_new:        'Brand new accounts — created in 2026, building with AI from day one',
    note_numbers:  'Data from GitHub Search API and Topics, plus GraphQL contribution analysis of 516 developers across 548 repos. Model split: Opus 4.6 — 257 repos, 4.7 — 264 repos, 4.8 — 27 repos.',
    cat_game:      'Games', cat_guide: 'Guides/Books', cat_bench: 'Benchmarks',
    cat_agent:     'Agents', cat_sdk: 'SDKs/Frameworks', cat_infra: 'Infrastructure',
    cat_tool:      'Tools/CLIs', cat_app:  'Apps', cat_other: 'Other',
    sig_explicit:  'Explicit', sig_topic: 'Topic', sig_config: 'Config',
    sig_commit:    'Co-Author', sig_under: 'Under Hood', sig_hackathon: 'Hackathon',
    lib_search_ph: 'Search repos, descriptions, languages, categories...',
    lib_showing:   function(v,t){ return 'Showing ' + v + ' of ' + t + ' repositories'; },
    filter_all:    'All', filter_explicit: 'Explicit', filter_under: 'Under Hood',
    filter_hack:   'Hackathon', filter_config: 'Config', filter_commit: 'Co-Author',
    lib_col_repo:  'Repository', lib_col_lang: 'Language',
    lib_col_cat:   'Category',  lib_col_stars: 'Stars', lib_col_signal: 'Signal',
  },
  ja: {
    toggle_btn:    'English',
    eyebrow:       '追跡調査 / 2026年5月30日 — 原典:',
    subtitle:      '<a href="https://github.com/jphein/opus" target="_blank" style="color:var(--accent-cyan)">@jphein の Opusセンサス</a>（2026年3月）の追跡調査です。4ヶ月後に再集計し、<strong>Opus 4.6・4.7・4.8</strong> すべてに対応しました。GitHub Search・トピック・コミット署名・開発者プロファイルを横断して同じ検出シグナルを再実行し、さらに GraphQL による休眠検出と Devpost プロジェクト追跡を追加しています。データはすべて 2026年5月30日時点のものです。',
    stat_repos:    '公開リポジトリ数',
    stat_stars:    '合計スター数',
    stat_langs:    '言語数',
    stat_devs:     '開発者数',
    stat_hackathon:'ハッカソンプロジェクト',
    stat_dormant:  '新規/休眠復活 開発者 %',
    h2_flagship:   '注目のフラッグシップ',
    h2_numbers:    '数字で見る',
    h2_building:   '誰が作っているか',
    h2_hackathon:  'ハッカソン',
    h2_top:        'トップリポジトリ',
    h2_notable:    '注目のプロジェクト',
    h2_bigger:     'より大きな文脈',
    h2_original:   '原典センサス',
    h2_method:     '検出方法',
    h2_library:    'ライブラリ全覧',
    badge_flagship:'Anthropic 公式 · 100% AI 著作',
    badge_original:'原典著者 · 2026年3月',
    fsl_stars:     'スター',
    fsl_forks:     'フォーク',
    fsl_commits:   'コミット',
    fsl_lang:      'Rust',
    fsl_compiled:  'コンパイル実績',
    fsl_orig_repos:'原典 リポジトリ数',
    fsl_orig_stars:'原典 スター数',
    fsl_orig_devs: '原典 開発者数',
    fsl_published: '公開日',
    ct_weekly:     'リリース以来の週次リポジトリ作成数',
    ct_lang:       '言語分布（14言語）',
    ct_stars:      'スター分布',
    ct_cats:       'プロジェクトカテゴリ',
    ct_devtype:    '開発者タイプ内訳',
    ct_age:        'アカウント作成年分布',
    ct_dormant:    '休眠から復活した開発者 — Opus 4.6 以前はほぼ活動なし',
    ct_new:        '新規開発者 — 2026年にアカウント作成、最初からAIで開発',
    note_numbers:  'GitHub Search API・トピック・GraphQLによる516人の開発者分析で548リポジトリを集計。モデル別: Opus 4.6 — 257件、4.7 — 264件、4.8 — 27件。',
    cat_game:      'ゲーム', cat_guide: 'ガイド/書籍', cat_bench: 'ベンチマーク',
    cat_agent:     'エージェント', cat_sdk: 'SDK/フレームワーク', cat_infra: 'インフラ',
    cat_tool:      'ツール/CLI', cat_app: 'アプリ', cat_other: 'その他',
    sig_explicit:  '明示的', sig_topic: 'トピック', sig_config: '設定ファイル',
    sig_commit:    '共同著者', sig_under: '内部利用', sig_hackathon: 'ハッカソン',
    lib_search_ph: 'リポジトリ・説明・言語・カテゴリで検索...',
    lib_showing:   function(v,t){ return v + ' / ' + t + ' 件を表示中'; },
    filter_all:    'すべて', filter_explicit: '明示的', filter_under: '内部利用',
    filter_hack:   'ハッカソン', filter_config: '設定ファイル', filter_commit: '共同著者',
    lib_col_repo:  'リポジトリ', lib_col_lang: '言語',
    lib_col_cat:   'カテゴリ',  lib_col_stars: 'スター', lib_col_signal: 'シグナル',
  }
};

function toggleLang() {
  LANG = LANG === 'en' ? 'ja' : 'en';
  applyLang();
}

function t(key) { return TRANSLATIONS[LANG][key] || TRANSLATIONS['en'][key] || key; }

function applyLang() {
  var T = TRANSLATIONS[LANG];
  // toggle button label
  var btn = document.getElementById('lang-toggle');
  if (btn) btn.textContent = T.toggle_btn;

  // data-i18n elements (simple textContent swap)
  var TEXT_KEYS = [
    'stat_repos','stat_stars','stat_langs','stat_devs','stat_hackathon','stat_dormant',
    'h2_flagship','h2_numbers','h2_building','h2_hackathon','h2_top','h2_notable',
    'h2_bigger','h2_original','h2_method','h2_library',
    'badge_flagship','badge_original',
    'fsl_stars','fsl_forks','fsl_commits','fsl_lang','fsl_compiled',
    'fsl_orig_repos','fsl_orig_stars','fsl_orig_devs','fsl_published',
    'ct_weekly','ct_lang','ct_stars','ct_cats','ct_devtype','ct_age',
    'ct_dormant','ct_new',
  ];
  TEXT_KEYS.forEach(function(key) {
    var els = document.querySelectorAll('[data-i18n="' + key + '"]');
    els.forEach(function(el) { el.textContent = T[key]; });
  });

  // eyebrow (has an <a> child — preserve it)
  var eyebrow = document.querySelector('[data-i18n="eyebrow"]');
  if (eyebrow) {
    var link = eyebrow.querySelector('a');
    eyebrow.textContent = T.eyebrow + ' ';
    if (link) eyebrow.appendChild(link);
  }

  // subtitle (has HTML)
  var sub = document.querySelector('[data-i18n="subtitle"]');
  if (sub) sub.innerHTML = T.subtitle;

  // note_numbers (separate en/ja <p> approach — toggle visibility)
  var enNote = document.querySelector('.section-note:not([data-i18n="note_numbers"])');
  var jaNote = document.querySelector('[data-i18n="note_numbers"]');
  // fallback: just update the first section-note near "The Numbers"
  // (simpler: update CAT_LABELS + SIGNAL_LABELS objects and re-render)

  // CAT_LABELS update
  CAT_LABELS.game  = T.cat_game;  CAT_LABELS.guide = T.cat_guide;
  CAT_LABELS.bench = T.cat_bench; CAT_LABELS.agent = T.cat_agent;
  CAT_LABELS.sdk   = T.cat_sdk;   CAT_LABELS.infra = T.cat_infra;
  CAT_LABELS.tool  = T.cat_tool;  CAT_LABELS.app   = T.cat_app;
  CAT_LABELS.other = T.cat_other;

  // SIGNAL_LABELS update
  SIGNAL_LABELS.explicit  = T.sig_explicit; SIGNAL_LABELS.explicit7 = T.sig_explicit;
  SIGNAL_LABELS.explicit8 = T.sig_explicit; SIGNAL_LABELS.topic46   = T.sig_topic;
  SIGNAL_LABELS.topic47   = T.sig_topic;    SIGNAL_LABELS.topic48   = T.sig_topic;
  SIGNAL_LABELS.config    = T.sig_config;   SIGNAL_LABELS.commit    = T.sig_commit;
  SIGNAL_LABELS.under     = T.sig_under;    SIGNAL_LABELS.hackathon = T.sig_hackathon;

  // re-render library table (picks up new CAT_LABELS / SIGNAL_LABELS)
  var libGrid = document.getElementById('lib-grid');
  var libControls = document.getElementById('lib-controls');
  var libCount = document.getElementById('lib-count');
  if (libGrid && libControls) {
    libGrid.innerHTML = '';
    libControls.innerHTML = '';
    if (libCount) libCount.textContent = '';
    renderLibrary();
  }

  // re-render category donut legend (text updates)
  var catLegend = document.getElementById('cat-legend');
  if (catLegend) {
    var catLegendItems = catLegend.querySelectorAll('.legend-label');
    catLegendItems.forEach(function(el) {
      var cat = el.getAttribute('data-cat');
      if (cat) el.textContent = CAT_LABELS[cat] || cat;
    });
  }

  // <html lang> attr
  document.documentElement.lang = LANG === 'ja' ? 'ja' : 'en';
}
// ── end i18n ───────────────────────────────────────────────────────
"""

# inject just before closing </script>
last_script_end = html.rfind("</script>")
html = html[:last_script_end] + translations_js + html[last_script_end:]

# ── Step 5: make renderLibrary() use TRANSLATIONS for UI strings ───
# placeholder
html = html.replace(
    "placeholder: 'Search repos, descriptions, languages, categories...'",
    "placeholder: t('lib_search_ph')"
)
# filter button labels
html = html.replace(
    "  var filters = ['All', 'Explicit', 'Under Hood', 'Hackathon', 'Config', 'Co-Author'];",
    "  var filters = [t('filter_all'), t('filter_explicit'), t('filter_under'), t('filter_hack'), t('filter_config'), t('filter_commit')];"
)
html = html.replace(
    "  var filterMap = { 'All': null, 'Explicit': ['explicit','explicit7','explicit8'], 'Under Hood': 'under', 'Hackathon': 'hackathon', 'Config': ['config','topic46','topic47','topic48'], 'Co-Author': 'commit' };",
    "  var filterMap = {}; filterMap[t('filter_all')]=null; filterMap[t('filter_explicit')]=['explicit','explicit7','explicit8']; filterMap[t('filter_under')]='under'; filterMap[t('filter_hack')]='hackathon'; filterMap[t('filter_config')]=['config','topic46','topic47','topic48']; filterMap[t('filter_commit')]='commit';"
)
# lib-count text
html = html.replace(
    "countEl.textContent = 'Showing ' + visible + ' of ' + libraryData.length + ' repositories';",
    "countEl.textContent = t('lib_showing')(visible, libraryData.length);"
)
# lib column headers
for en_label, i18n_key in [
    ("'Repository'", "t('lib_col_repo')"),
    ("'Language'",   "t('lib_col_lang')"),
    ("'Category'",   "t('lib_col_cat')"),
    ("'Stars'",      "t('lib_col_stars')"),
    ("'Signal'",     "t('lib_col_signal')"),
]:
    html = html.replace(f"label: {en_label},", f"label: {i18n_key},", 1)

open("index.html", "w", encoding="utf-8").write(html)
print("✅ i18n patch applied")

checks = [
    "lang-toggle",
    "data-i18n=\"h2_numbers\"",
    "data-i18n=\"stat_repos\"",
    "TRANSLATIONS",
    "toggleLang",
    "applyLang",
    "t('lib_search_ph')",
    "t('filter_all')",
]
content = open("index.html").read()
for c in checks:
    print(f"  {'✅' if c in content else '❌'} {c}")
