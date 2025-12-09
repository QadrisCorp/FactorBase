# FactorBase

**因子知識庫 — Qadris Factor System 文獻概念層**

[![Layer](https://img.shields.io/badge/Layer-1%20Concept-blue)](https://github.com/QadrisCorp)
[![Status](https://img.shields.io/badge/Status-Active-green)](https://github.com/QadrisCorp/FactorBase)
[![Owner](https://img.shields.io/badge/Owner-Research%20Team-orange)](https://github.com/QadrisCorp)

---

## 📘 專案定位

FactorBase 是 **Qadris Factor System 四層架構**中的「文獻概念層」（Concept Layer），負責系統化整理因子文獻與概念定義的知識圖譜（Knowledge Graph）。

### 四層架構

| 層級 | Repository | 職責 |
|:----:|:-----------|:-----|
| **1** | **FactorBase** | 📚 文獻概念層 — 純知識圖譜（本專案） |
| 2 | MeasureRetriever | 🔧 實作層 — 公司級公式庫 |
| 3 | FactorBackTest | ⚡ 執行層 — Stateless 回測引擎 |
| 4 | QadrisFactorBase | 🎯 產品層 — Metadata 中心與整合 |

---

## 🎯 主要功能

- 📄 **Paper**：收集並結構化整理所有因子相關文獻
- 📊 **Factor**：定義標準化的因子分類（Value, Momentum, Profitability 等）
- 📐 **Concept Measure**：定義文獻中描述的衡量方式（BM, EP, ROE 等）
- 🔗 **Paper–Measure**：建立文獻與 Measure 的關聯地圖

---

## 🚫 明確排除（屬於其他層級）

| 不處理項目 | 負責層級 |
|:-----------|:---------|
| 資料表與欄位 Mapping | MeasureRetriever |
| 實際計算邏輯（Winsorization 等）| MeasureRetriever |
| 市場特定參數設定 | MeasureRetriever |
| 更新頻率（daily/monthly）| MeasureRetriever |
| 回測執行與結果 | FactorBackTest |
| Concept ↔ Implement Mapping | QadrisFactorBase |

---

## 📁 專案結構

```
FactorBase/
├── README.md                         # 本文件
├── papers/                           # 📄 論文相關資料
│   ├── metadata/                     # paper_001.json ~ paper_007.json
│   ├── raw_pdf/                      # 原始 PDF（選用）
│   └── README.md
├── factors/                          # 📊 因子分類
│   ├── factors.json                  # 5 個核心因子定義
│   └── README.md
├── measures/                         # 📐 Concept Measure 定義
│   ├── index.json                    # Measure 索引
│   ├── value/                        # BM, EP, CP, PB, SP
│   ├── momentum/                     # MOM_12M, MOM_6M, MOM_1M, HIGH_52W
│   ├── profitability/                # ROE, ROA, GP_TA, OP_BE, GM
│   ├── investment/                   # AG, INV_TA, CAPEX_TA, NSI
│   └── size/                         # ME, LN_ME
├── relations/                        # 🔗 關聯表
│   └── paper_measures.json           # Paper-Measure 對應（20 筆）
├── docs/                             # 📖 文件
│   └── schemas/                      # JSON Schema 定義
│       ├── paper_schema.json
│       ├── measure_schema.json
│       └── paper_measure_schema.json
├── scripts/                          # 🔧 工具腳本
│   ├── query_factorbase.py           # 查詢工具
│   └── validate_json.py              # JSON 驗證工具
└── .github/
    └── copilot-instructions.md       # Copilot 行為規範
```

---

## 📊 目前資料統計

| 類型 | 數量 | 說明 |
|:-----|:----:|:-----|
| Papers | 7 | 經典因子研究文獻 |
| Factors | 5 | Value, Size, Momentum, Profitability, Investment |
| Measures | 19 | 跨 5 個因子類別 |
| Paper-Measure Links | 20 | 文獻與 Measure 關聯 |

---

## 📄 資料格式範例

### Paper JSON

```json
{
  "paper_id": "paper_001",
  "title": "Common risk factors in the returns on stocks and bonds",
  "authors": "Fama, Eugene F.; French, Kenneth R.",
  "year": 1993,
  "journal": "Journal of Financial Economics",
  "doi": "10.1016/0304-405X(93)90023-5",
  "bibtex": "@article{fama1993common,...}",
  "market": "US",
  "conclusion_sign": "positive",
  "replicable": "yes"
}
```

### Concept Measure JSON

```json
{
  "measure_id": "BM",
  "measure_name": "BM",
  "display_name": "Book to Market Ratio",
  "factor": "Value",
  "description": "Book value of equity / Market capitalization",
  "formula": {
    "type": "ratio",
    "numerator": "book_value_equity",
    "denominator": "market_value_equity",
    "window": "MRQ"
  },
  "normalization": "zscore_cross_sectional",
  "original_paper_id": "paper_001"
}
```

### Paper-Measure Link

```json
{
  "paper_id": "paper_001",
  "measure_id": "BM",
  "role": "primary_sorting_variable",
  "significance": "positive",
  "notes": "用於建構 HML 因子"
}
```

---

## 🔧 使用方式

### 查詢 Measure

```bash
python scripts/query_factorbase.py --measure BM
```

### 查詢 Paper 使用的 Measures

```bash
python scripts/query_factorbase.py --paper paper_001
```

### 列出所有 Value 因子的 Measures

```bash
python scripts/query_factorbase.py --factor Value
```

### 驗證 JSON 格式

```bash
python scripts/validate_json.py
```

---

## 📚 收錄文獻

| Paper ID | 標題 | 作者 | 年份 |
|:---------|:-----|:-----|:----:|
| paper_001 | Common risk factors in the returns on stocks and bonds | Fama & French | 1993 |
| paper_002 | On Persistence in Mutual Fund Performance | Carhart | 1997 |
| paper_003 | A five-factor asset pricing model | Fama & French | 2015 |
| paper_004 | The other side of value: The gross profitability premium | Novy-Marx | 2013 |
| paper_005 | Digesting anomalies: An investment approach | Hou, Xue & Zhang | 2015 |
| paper_006 | Value and Momentum Everywhere | Asness, Moskowitz & Pedersen | 2013 |
| paper_007 | Quality Minus Junk | Asness, Frazzini & Pedersen | 2019 |

---

## 🔗 與其他 Repository 的關係

```
FactorBase (概念層)
    │
    ├──→ QadrisFactorBase (產品層)
    │        ├── Concept ↔ Implement Mapping
    │        └── Study Implementation 管理
    │
    └──→ MeasureRetriever (實作層)
             ├── 實際資料表 Mapping
             └── 計算邏輯實作
```

---

## 📋 儲存策略

**Phase 1（現階段）**：JSON 檔案為主
- 易於版本控制與人工審核
- Git 追蹤所有變更
- Copilot Agent 可直接讀取

**Phase 2（未來可選）**：SQLite 輔助
- 方便複雜查詢與統計分析

---

## 👥 維護團隊

- **Owner**：Research Team (@Fama)
- **Supporting**：Data Team, Application Team

---

## 📜 版本歷史

| 版本 | 日期 | 說明 |
|:-----|:-----|:-----|
| 2.0 | 2025-12-09 | 配合 QadrisFactorBase 四層架構重構 |
| 1.0 | 2025-12-05 | 初始版本 |

---

## 📄 授權

© 2025 QadrisCorp. All rights reserved.


