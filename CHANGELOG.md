# CHANGELOG (更新日誌)

所有本專案的重要變更都將記錄於此檔案。
本格式基於 [Keep a Changelog](https://keepachangelog.com/zh-TW/1.0.0/)。

## [1.1.0] - 2026-08-02

### 新增 (Added)
- 新增「個人求卦歷史紀錄」區塊 (LocalStorage 本地保留 10 筆歷史紀錄與快速檢視) (Closes #10)。
- 新增「一鍵複製卦辭」與 Web Audio API 「古磬 432Hz 起卦音效」 (Closes #9)。

- 支援 PWA (Progressive Web App) 手機端獨立 App 與離線快取支援 (`manifest.json`, `sw.js`) (Closes #8)。

- 新增「卦象典雅圖卡導出/分享」功能 (Canvas PNG 動態生成) (Closes #7)。

- 導入「動爻與之卦（本卦 ➔ 變卦）」演算機制 (Closes #6)。

- 支援「自訂數字求卦 (Custom Numbers Input)」功能 (Closes #5)。

- 新增 GitHub Issue 與 Pull Request 標準驗收範本 (`.github/ISSUE_TEMPLATE`, `.github/PULL_REQUEST_TEMPLATE.md`) (Closes #4)。

- 導入 API 參數嚴格型別校驗與 Fail-Fast 錯誤處理機制 (Closes #3)。

- 新增 GitHub Actions CI 自動化測試工作流程 (`.github/workflows/ci.yml`) (Closes #2)。

- 導入 TDD (Test-Driven Development) 單元測試架構 (`tests/test_app.py`) (Closes #1)。

- 在 `requirements.txt` 新增 `pytest` 套件支援。
- 新增首頁、版本查詢 API、隨機起卦、卦象解讀與 400 邊界條件之自動化測試。

### 變更 (Changed)

- 全面優化前端視覺風格：去除傳統紫色/霓虹等俗套 AI 質感，改為**東方禪意極簡美學 (Modern Eastern Zen Minimalism)**。
- 引入 Google Fonts `Noto Serif TC` (明體/宋體) 與 `Cinzel` 字型，提升古典經典人文韻味。
- 後端與前端全面整合 **易經 Unicode 六十四卦爻符 (䷀~䷿)** 與古籍卡片排版。
- 增加太極起卦/籌策算卦動態視覺效果與沉浸式儀式感。

## [1.0.0] - 2026-08-02


### 新增 (Added)
- 新增動態通訊埠自動搜尋機制（優先固定 5001，衝突時自動順延至 5002+）。
- 新增語意化版本號與 Git Short Commit Hash 控制機制（支援 `/api/version` 與頁尾標籤顯示）。
- 新增全域與多 AI Agent 規範文件：`AGENTS.md`、`CLAUDE.md` 與 `GEMINI.md`。
- 新增通用 Prompt 範本 `AI_PROMPT_TEMPLATE.md`。

### 變更 (Changed)
- 更新 [README.md](file:///d:/github/chiisen/VibeCodingDivinationByNumbers/README.md) 與 [運行說明.md](file:///d:/github/chiisen/VibeCodingDivinationByNumbers/%E9%81%8B%E8%A1%8C%E8%AA%AA%E6%98%8E.md) 的 Port 與版本說明。
