# GEMINI.md - Google Gemini / Antigravity 專用接入指南

> **導讀**：本檔案為 Gemini / Antigravity 的專用配置檔。
> 專案全域規範請參閱 [AGENTS.md](file:///d:/github/chiisen/VibeCodingDivinationByNumbers/AGENTS.md)。

---

## 🪟 Windows / PowerShell 環境規範

1. **Python 執行環境**：
   - 專案已配備 `.venv` 虛擬環境，請優先使用 `.\.venv\Scripts\python.exe` 執行。
   - 若遇到 `pyenv` 版本問題，使用 `pyenv local 3.11.9` 設定。

2. **Port 衝突與編碼處理**：
   - 伺服器已自動設定為「優先使用 Port 5001，若被佔用則自動順延 (5002...)」。
   - `print` 輸出避免使用非 CP950 支援之特殊的Emoji以防止 Windows 終端機 UnicodeEncodeError。

3. **Git Issue & TDD 測試流程**：
   - 開發時嚴禁直接變更主分支 `main`，必須依照 [AGENTS.md](file:///d:/github/chiisen/VibeCodingDivinationByNumbers/AGENTS.md) 建立 `feat/#<issue-id>` 分支。
   - 實施 TDD 流程：先於 `tests/test_app.py` 撰寫測試，開發後執行 `.\.venv\Scripts\python.exe -m pytest` 確保綠燈。
   - 所有 commit 訊息與文件回覆必須使用 **正體中文 (繁體中文)**。

