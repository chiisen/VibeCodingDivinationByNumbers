# CLAUDE.md - Anthropic Claude / Cursor 專用接入指南

> **導讀**：本檔案為 Claude (Claude Code / Cursor) 的專用配置檔。
> 專案全域規範請參閱 [AGENTS.md](file:///d:/github/chiisen/VibeCodingDivinationByNumbers/AGENTS.md)。

---

## 🚀 常用開發命令 (Commands)

```bash
# 啟動虛擬環境與安裝套件
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

# 啟動 Flask 伺服器 (自動尋找可用 Port，優先使用 5001)
.\.venv\Scripts\python.exe app.py

# 指定 Port 啟動
$env:PORT=5001; .\.venv\Scripts\python.exe app.py

# 執行 TDD 單元測試
.\.venv\Scripts\python.exe -m pytest

```

---

## 📌 Claude 工作指南

1. **優先遵照全域規範**：請隨時參考 [AGENTS.md](file:///d:/github/chiisen/VibeCodingDivinationByNumbers/AGENTS.md) 的 Issue ➔ PR 開發流程與 Karpathy 原則。
2. **Issue 到 PR 快速步驟**：
   - 收到任務後，確認對應的 Issue 編號。
   - 建立分支：`git checkout -b feat/#<issue-id>-<desc>`。
   - 修改並測試程式碼：執行 `.\.venv\Scripts\python.exe app.py` 驗證。
   - 提交 commit：`git commit -m "feat(scope): 繁體中文說明"`。
   - 發起 PR 並寫明 `Closes #<issue-id>`。
3. **交接準備**：若暫時中斷任務，請更新 `.agent_task_state.md` 供下一位 AI 接手。
