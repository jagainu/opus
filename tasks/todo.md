# Opus Census — 追跡調査（follow-up）2026-05 リフレッシュ

> jphein/opus を **帰属明示の追跡調査**として最新化。fork=jagainu/opus, branch=refresh-census-2026-05。
> 公開: GitHub Pages on fork → jagainu.github.io/opus（PRはしない）。著者表記=jagainu。

## Phase 1: データ収集（自動・実証済み3系統）
- [ ] 1a. GitHub repos 本スケール取得（`fetch_census.py --pages 3`）→ candidates.json
- [ ] 1b. 分類パス：候補を keep/drop + category 判定（実プロジェクト vs 単なる言及のノイズ除去）
- [ ] 1c. 各リポの created_at / owner を補完（週次・モデル別チャート用）
- [ ] 1d. 休眠復活分析：owner ごとに GraphQL contributionsCollection（年次）→ 復活フラグ集計
- [ ] 1e. Devpost：Playwright + JSON XHR で opus 4.6/4.7/4.8 プロジェクト + winner 収集

## Phase 2: 集計データ生成（index.html 用の配列を再生成）
- [ ] 2a. libraryData（厳選後の全リポ、stars/lang/lc/signal/desc）
- [ ] 2b. weeklyData（2〜5月の週次作成数、4.7/4.8リリースの山）
- [ ] 2c. 言語分布 / スター階層 / カテゴリ / **モデル別(4.6/4.7/4.8)** 分布
- [ ] 2d. dormantDevs / accountAgeData / devTypeData（休眠復活データ）
- [ ] 2e. hackathon winners（Devpost winner フラグから）

## Phase 3: サイト改修（index.html）
- [ ] 3a. タイトル・ヘッダを「追跡調査」フレームに（@jphein の census を4ヶ月後に更新と明記）
- [ ] 3b. ヘッドライン数字を最新値に差し替え
- [ ] 3c. チャート群を再生成データに差し替え（モデル別チャート追加）
- [ ] 3d. **「Case Study: @jphein」セクション(501行)を削除** → 原典への帰属クレジットブロックに置換
- [ ] 3e. methodology を更新（GraphQL休眠検出・Devpost JSON・4.7/4.8追加を反映）
- [ ] 3f. フッター/メタに jagainu 表記 + 原典リンク

## Phase 4: ドキュメント & 公開
- [ ] 4a. README.md を追跡調査として全面改稿（@jphein原典クレジット明記）
- [ ] 4b. all-ways-to-access-*.md を 4.8 まで更新（任意）
- [ ] 4c. ローカル動作確認（Playwright スクショ）
- [ ] 4d. コミット → push → GitHub Pages 有効化 → jagainu.github.io/opus 確認

## 帰属ポリシー（厳守）
- "forked from jphein/opus" を残す（出自の正直さ）
- README & サイトに「Original census by @jphein (Jeffrey Hein), March 2026」を明記
- 彼の個人的物語（Case Study）は載せない＝乗っ取らない
- ライセンス無し前提 → GitHub機能内(fork+Pages)に留め、強い帰属で運用

## Review（完了時に追記）
-
