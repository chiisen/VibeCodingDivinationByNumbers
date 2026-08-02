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
   - 分支命名規範：`feat/#<issue_id>-<desc>` 或 `fix/#<issue_id>-<desc>`。
3. **規範化 Commit (Conventional Commits)**：
   - 格式：`<type>(<scope>): <subject>`（例如 `feat(auth): 新增使用者登入`）。
   - 說明與 Commit 訊息一律使用 **正體中文 (繁體中文)**。
4. **Pull Request (PR) 合併**：
   - PR 描述中必須包含：變更摘要、單元測試/驗證命令與結果，並加上 `Closes #<issue_id>` 自動關閉對應 Issue。

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

## ⚠️ 硬性要求 (Hard Constraints)

1. **自動偵測環境**：請根據當前專案實際檔案自動填入具體指令（如 `npm test`, `pytest`, `go test ./...` 等），嚴禁使用萬用占位符。
2. **正體中文**：所有產出文件的說明與範例統一採用 **正體中文 (繁體中文)**。
3. **簡潔清晰**：善用 Markdown 標題、表格與 Alert 區塊 (`> [!IMPORTANT]`)，提升 AI 閱讀效率。

---

## 🚀 請立刻開始執行

請掃描當前專案目錄，並立刻產出/更新 `AGENTS.md`、`CLAUDE.md` 與 `GEMINI.md`！
