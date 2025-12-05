FactorBase：專案定位（正式版）

FactorBase 是一套系統化整理所有因子文獻、因子定義與 measure 計算方法的知識庫，提供研究、回測、系統開發與 AI Agent 的共同資料來源（Single Source of Truth）。

它的任務包括：

收集並結構化整理所有因子相關文獻（Papers）

定義標準化的因子分類（Factors）

統一定義各種 measure（Measures）

建立文獻與 measure 的關聯地圖（PaperMeasures）

提供 API / DB / JSON 介面供 Data Team、Research Team、Application Team 與 Copilot 使用

它未來可直接支援：

Qadris MeasureDefinitionManager（自動載入 measure 公式）

MeasureRetriever（欄位列表與單位標準化）

FactorBackTesting（直接引用文獻來源）

Copilot Agents（根據因子分類自動推薦 measure）

Web API（外部研究者或內部團隊查詢因子定義）

📂 FactorBase — 專案資料夾結構（可直接放進 GitHub）
FactorBase/
│
├─ papers/                # 論文相關資料
│   ├─ raw_pdf/           # 原始 PDF
│   ├─ metadata/          # paper_xxx.json
│
├─ factors/               # 因子分類與說明
│   ├─ factors.json
│
├─ measures/              # measure 定義標準化 JSON
│   ├─ value/
│   ├─ momentum/
│   ├─ profitability/
│   └─ investment/
│
├─ relations/             # 論文 × measure 關聯
│   ├─ paper_measures.json
│
├─ sql/
│   ├─ create_tables.sql  # FactorBase 資料表
│
├─ scripts/
│   ├─ import_paper.py
│   ├─ import_measure.py
│   ├─ link_paper_measure.py
│   ├─ export_api_schema.py
│
└─ README.md              # 專案總說明（自動生成版如下）