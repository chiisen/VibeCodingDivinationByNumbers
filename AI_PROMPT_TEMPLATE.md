# Universal AI Collaboration & Handoff Setup Prompt

> **使用說明**：複製本文件內容發送給任何 AI Agent（如 Claude, Gemini, ChatGPT, Codex 等），AI 會自動掃描當前專案的技術棧與目錄，並生成適用於該專案的標準化 AI 協作規範文件。

---

## Role & Goal
你是一位專業的 DevOps 與 AI 協作架構師（AI Collaboration Architect）。
請針對當前專案的程式語言與技術棧，產出/更新一套**標準化且可無縫交接的 AI 協作規範文件** (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`)。

---

## 🎯 核心工作流程規範 (Issue & PR Flow)

無論專案為何，AI Agent 與開發者皆須遵循以下規範：

1. **Issue 導向 (Issue-Driven)**：
   - 所有的 Feature、Fix 或 Refactor 任務都必須先有 GitHub Issue。
   - 任務執行前，AI 必須確認發起標準與驗證條件 (DoD)。
2. **分支開發 (Branch Strategy)**：
   - 禁止直接 commit/push 至主分支 (`main` / `master`)。
   - 分支命名規範：`feat/<issue_id>-<desc>` 或 `fix/<issue_id>-<desc>`。
3. **規範化 Commit (Conventional Commits)**：
   - 格式：`<type>(<scope>): <subject>`（例如 `feat(auth): 新增使用者登入`）。
   - 說明與 Commit 訊息一律使用 **正體中文 (繁體中文)**。
4. **Pull Request (PR) 合併**：
   - PR 描述中必須包含：變更摘要、單元測試/驗證命令與結果，並加上 `Closes #<issue_id>` 自動關閉對應 Issue。
5. **分支保護 (Branch Protection)**：
   - `main` 分支禁止直接 push。
   - 所有變更必須透過 PR 合併。
   - PR 需通過 CI 檢查（如有）才能合併。

---

## 📁 待生成之規範文件架構 (Target Files)

請自動偵測當前專案的技術棧（如 `package.json`, `requirements.txt`, `composer.json`, `go.mod` 等），並在根目錄生成以下三個檔案：

### 1. `AGENTS.md` (全域 AI 規範主檔案 - 主大腦)
- **專案簡介與技術棧**：自動填入當前專案使用的語言、框架與關鍵套件。
- **常用開發指令**：自動整理當前專案的安裝、啟動、測試、Lint 與 Build 指令。
- **GitHub Issue & PR 完整流程規範**：明確說明 Issue 發起、Branch 命名、Commit 格式與 PR 驗證步驟。
- **AI 開發四大原則 (Karpathy Principles)**：
  - **謀定而後動**：修改前說明假設與影響範圍。
  - **簡潔至上 (KISS)**：僅撰寫解決當前問題所需的最小代碼。
  - **微創異動**：僅修改與任務相關的檔案，維護專案既有風格。
  - **目標導向驗證**：異動後必須執行專案的 Lint 與 Test 指令。
- **跨 AI 任務交接協議 (Handoff Protocol)**：說明如何在 `.agent_task_state.md` 紀錄任務狀態（🚩目標 / ✅已完成 / 🚀下一步）。

### 2. `CLAUDE.md` (Claude / Cursor 專用接入檔)
- 指引 Claude 進入專案時優先閱讀 `AGENTS.md`。
- 提供適用於 Claude Code / Cursor 的快捷命令選單。

### 3. `GEMINI.md` (Gemini / Antigravity 專用接入檔)
- 指引 Gemini 進入專案時優先閱讀 `AGENTS.md`。
- 針對不同作業系統（如 Windows PowerShell / Linux Bash）的指令差異提供防錯提醒。

---

## 🔢 版本管理規範

- 根目錄維護 `VERSION` 檔案（語意化版本號，如 `1.0.0`）。
- AI 讀取 `VERSION` 並顯示於頁面標題與頁腳（如需 Web 應用）。
- 每次發佈前更新版本號並同步 `CHANGELOG.md`。
- 版本號遵循 [語意化版本](https://semver.org/lang/zh-TW/)：`MAJOR.MINOR.PATCH`。

---

## 📝 變更日誌規範 (CHANGELOG)

- 根目錄維護 `CHANGELOG.md`，格式遵循 [Keep a Changelog](https://keepachangelog.com/zh-TW/1.1.0/)。
- 每個 PR 合併後必須更新對應版本的變更記錄。
- 變更類型分類：
  - `### 新增` (Added)：新功能
  - `### 變更` (Changed)：現有功能變更
  - `### 修復` (Fixed)：Bug 修復
  - `### 重構` (Refactored)：代碼重構（不影響功能）
  - `### 移除` (Removed)：移除功能
- 格式範例：
  ```markdown
  ## [1.0.0] - 2026-08-02
  ### 新增
  - 新增使用者登入功能
  ### 修復
  - 修復密碼驗證錯誤
  ```

---

## 🧠 AI 記憶持久化規範

### 會話間記憶
- 使用 `.agent_task_state.md` 記錄任務狀態。
- 格式：3-Bullet 閃電報（🚩目標 / ✅進展 / 🚀下一步）。
- 更新時機：子任務完成、Bug 修復、會話結束前。

### 跨 AI 交接
- 新 AI 啟動時讀取 `.agent_task_state.md` 恢復上下文。
- 交接訊息需包含：當前任務、已完成項目、待辦事項、技術決策紀錄。

### 記憶文件大小限制
- `.agent_task_state.md` 限制 50 行以內。
- 超出時進行壓縮，保留最關鍵資訊。

---

## 📋 文件優先權規範

當多個 AI 配置文件共存時，遵循以下優先權：

| 文件 | 用途 | 適用 AI | 優先權 |
|------|------|---------|--------|
| `AGENTS.md` | 通用規範（主大腦） | 所有 AI | 1 |
| `CLAUDE.md` | Claude/Cursor 專用 | Claude Code | 2 |
| `GEMINI.md` | Gemini 專用 | Gemini | 2 |
| `AI_PROMPT_TEMPLATE.md` | 模板來源 | 建立配置時 | 3 |

**規則**：專案配置 > 全域配置 > 模板預設

---

## 📋 Issue 模板規範

建議建立 `.github/ISSUE_TEMPLATE/` 目錄，包含以下模板：

### 功能需求模板 (`feature.md`)
```markdown
## 功能描述
簡述新功能的需求

## 使用案例
- 使用者可以...

## 驗收標準
- [ ] 功能正常運作
- [ ] 通過測試
- [ ] 更新文件

## 技術建議（選填）
建議的實作方式
```

### Bug 報告模板 (`bug.md`)
```markdown
## 問題描述
簡述遇到的問題

## 重現步驟
1. 執行...
2. 點擊...
3. 看到錯誤...

## 預期行為
應該發生什麼

## 實際行為
實際發生什麼

## 環境資訊
- OS: Windows 11
- 瀏覽器: Chrome 120
- Python: 3.11.9
```

### 重構任務模板 (`refactor.md`)
```markdown
## 重構目標
簡述重構的目的

## 影響範圍
- 涉及檔案：...

## 驗證方式
- [ ] 功能不受影響
- [ ] 通過所有測試
- [ ] 效能無明顯下降
```

---

## 📁 目標文件架構

```
專案根目錄/
├── AGENTS.md                  # 通用 AI 規範（主大腦）
├── CLAUDE.md                  # Claude/Cursor 專用
├── GEMINI.md                  # Gemini 專用
├── AI_PROMPT_TEMPLATE.md      # 模板來源（本文件）
├── VERSION                    # 版本號（如 1.0.0）
├── CHANGELOG.md               # 變更日誌
├── CONTRIBUTING.md            # 貢獻指南
├── ARCHITECTURE.md            # 架構文檔
├── .agent_task_state.md       # AI 任務狀態（會話間記憶）
├── docs/
│   ├── API.md                 # API 文檔
│   └── DECISIONS.md           # 架構決策紀錄 (ADR)
└── .github/
    └── ISSUE_TEMPLATE/        # Issue 模板
        ├── feature.md
        ├── bug.md
        └── refactor.md
```

---

## ⚠️ 硬性要求 (Hard Constraints)

1. **自動偵測環境**：請根據當前專案實際檔案自動填入具體指令（如 `npm test`, `pytest`, `go test ./...` 等），嚴禁使用萬用占位符。
2. **正體中文**：所有產出文件的說明與範例統一採用 **正體中文 (繁體中文)**。
3. **簡潔清晰**：善用 Markdown 標題、表格與 Alert 區塊 (`> [!IMPORTANT]`)，提升 AI 閱讀效率。
4. **文件同步**：當專案結構變更時，必須同步更新相關規範文件。
5. **版本同步**：每次發佈前，必須同步更新 `VERSION` 與 `CHANGELOG.md`。

---

## 🚀 請立刻開始執行

請掃描當前專案目錄，並立刻產出/更新 `AGENTS.md`、`CLAUDE.md` 與 `GEMINI.md`！
