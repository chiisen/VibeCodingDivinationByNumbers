# VibeCodingDivinationByNumbers

Vibe Coding Divination By Numbers

[PRD](PRD.md)

# PYTHON 🎯 核心功能（已完成）
隨機數字生成 - 生成兩個 1-100 的隨機數字
易經占卜解讀 - 根據數字總和模 64 對應易經六十四卦
前端網頁介面 - 美觀的響應式設計，支援各種設備
AJAX 互動 - 無需刷新頁面的即時占卜體驗
# 📁 專案結構
VibeCodingDivinationByNumbers/
├── app.py                 # Flask 後端應用
├── requirements.txt       # Python 依賴套件
├── 運行說明.md           # 使用說明文件
├── templates/
│   └── index.html        # 前端 HTML 模板
└── static/
    ├── style.css         # CSS 樣式文件
    └── script.js         # JavaScript 功能文件

# 🚀 技術特點
後端：Flask 框架，包含完整的易經六十四卦資料
前端：響應式設計，流暢動畫效果，支援鍵盤快捷鍵
API：RESTful 設計，包含錯誤處理機制
體驗：載入動畫、數字動畫、淡入效果等
# 使用方式
執行 python app.py 啟動應用
訪問 http://localhost:5000
點擊「開始占卜」按鈕
查看隨機數字和易經解讀結果
可重複進行占卜
# 響應式設計
支援桌面、平板、手機等各種設備
優雅的漸層背景和卡片式設計
觸摸設備優化
