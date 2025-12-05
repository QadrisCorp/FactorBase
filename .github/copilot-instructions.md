# QadrisCorp — FactorBase Copilot Instructions
Version: 1.0  
Last Updated: 2025-12-05  
Scope: 本文件為「FactorBase 專案專用」的 Copilot 行為規範。  
All Copilot outputs must follow QadrisCorp's global governance and this project's rules.

---

# 1. Project Summary（專案摘要）

**專案名稱：** FactorBase  
**專案目的：** 系統化整理所有因子文獻、因子定義與 measure 計算方法的知識庫，提供研究、回測、系統開發與 AI Agent 的共同資料來源（Single Source of Truth）。

**主要功能或目標：**
- 收集並結構化整理所有因子相關文獻（Papers）
- 定義標準化的因子分類（Factors）
- 統一定義各種 measure（Measures）
- 建立文獻與 measure 的關聯地圖（PaperMeasures）
- 提供 API / DB / JSON 介面供各團隊與 Copilot 使用

**專案 Owner Team：** Research  
**Supporting Teams：** Data, Application

（註：此為專案的定位與範圍，不取代 Product Spec。）

---

# 2. Project Boundaries（專案邊界）

本專案必須同時遵守：

- 《company_policy.md》  
- 《collaborative_rules.md》  
- 《copilot-instructions-global.md》  
- 七大部門 Agent：  
  - @Product  
  - @Application  
  - @Data  
  - @Research  
  - @Trading  
  - @Infrastructure  
  - @Sales

本文件只定義「本專案特有」的要求，不覆蓋全域規範。

---

# 3. Project Architecture（專案架構）

## 3.1 技術棧（Tech Stack）
- Backend: Python + FastAPI（第三階段）
- Database: MySQL / SQLite（第一階段可用 SQLite 快速驗證）
- Data Format: JSON / YAML（measure 定義、paper metadata）
- Integration: MeasureDefinitionManager, MeasureRetriever, FactorBackTesting

## 3.2 專案資料流（Data Flow）

```
論文 PDF / BibTeX / 網頁
       ↓
  [papers.json / yaml]
       ↓
  papers table (DB)
       ↓
[factors.json] → factors table
       ↓
[measures/*.json] → measures table
       ↓
paper_measures table (關聯)
       ↓
MeasureDefinitionManager / MeasureRetriever / FactorBackTesting
       ↓
FastAPI endpoints (第三階段)
```

## 3.3 專案目錄結構

```
FactorBase/
├── README.md                     # 專案總說明
├── papers/                       # 論文相關資料
│   ├── raw_pdf/                  # 原始 PDF
│   └── metadata/                 # paper_{id}.json / yaml
├── factors/                      # 因子分類與說明
│   └── factors.json
├── measures/                     # measure 定義標準化 JSON
│   ├── value/
│   ├── momentum/
│   ├── profitability/
│   └── investment/
├── relations/                    # 論文 × measure 關聯
│   └── paper_measures.json
├── sql/                          # 資料庫 Schema
│   └── create_tables.sql
├── scripts/                      # Python 腳本
│   ├── import_paper.py
│   ├── import_measure.py
│   ├── link_paper_measure.py
│   └── export_api_schema.py
├── tests/                        # 測試程式碼
│   └── ...
├── docs/                         # 文件目錄
│   └── ...
└── .github/
    └── copilot-instructions.md   # 本文件
```

---

# 4. Project-specific Rules（本專案專屬規則）

## 4.1 專案開發限制

- 本專案的 **measure 定義必須包含完整欄位**：
  - `measure_id`：唯一識別碼
  - `factor`：所屬因子
  - `formula`：計算公式（含 type、分子、分母、時間窗）
  - `data_source`：資料來源
  - `frequency`：更新頻率
  - `normalization`：標準化方式
- 本專案 **不可自行定義新的底層資料欄位**（需透過 Data Team）
- 本專案 **measure_id / measure_name 必須與 MeasureDefinitionManager 對應**
- Paper metadata **必須包含**：title, authors, year, market, conclusion_sign, replicable

## 4.2 專案行為規範

- 所有 measure JSON 必須符合 FactorBase-implement.md 定義的格式
- 所有 paper metadata JSON 必須符合 FactorBase-implement.md 定義的格式
- 新增 measure 時需標註文獻來源（paper_id）
- 新增 paper 時需標註使用的 measure 與 factor

## 4.3 因子分類標準（Factors Taxonomy）

本專案採用以下核心因子分類：

| Factor | 說明 |
|--------|------|
| Value | 基於公司估值相對於基本面指標的相對便宜程度 |
| Size | 基於公司市值大小 |
| Momentum | 基於過去報酬的持續性 |
| Profitability | 基於公司獲利能力 |
| Investment | 基於公司資本支出與資產成長 |
| Quality | 綜合獲利穩定性、財務健康度等 |
| Low Volatility | 基於價格波動性 |
| Liquidity | 基於交易流動性 |
| Sentiment | 基於市場情緒指標 |

---

# 5. Deliverable Standards（輸出成果標準）

所有 Copilot 產出需符合：

## 5.1 程式碼
- 必須可運行
- 必須具備註解與型別標註（type hints）
- 匯入腳本需支援 JSON/YAML → DB 雙向同步
- 需遵守 PEP8 規範

## 5.2 JSON 定義檔

**Measure JSON 範例：**
```json
{
  "measure_id": "PB",
  "factor": "Value",
  "description": "Price to Book ratio = Market cap / Book equity",
  "formula": {
    "type": "ratio",
    "numerator": "market_value_equity",
    "denominator": "book_value_equity",
    "window": "MRQ"
  },
  "data_source": ["marketstddb.md_ta_dailyquotes", "financials.bs_quarterly"],
  "frequency": "daily",
  "normalization": "zscore_cross_sectional",
  "notes": "常用於 Value 因子排序"
}
```

**Paper JSON 範例：**
```json
{
  "paper_id": 1,
  "title": "Common risk factors in the returns on stocks and bonds",
  "authors": "Fama, Eugene F.; French, Kenneth R.",
  "year": 1993,
  "journal": "Journal of Financial Economics",
  "market": "US",
  "asset_class": "Equity",
  "abstract": "...",
  "conclusion_sign": "positive",
  "replicable": "yes",
  "notes": ""
}
```

## 5.3 SQL Schema
- 必須符合 FactorBase-implement.md 定義的四張表結構
- 表格：`papers`, `factors`, `measures`, `paper_measures`

## 5.4 文件
- 需為完整 Markdown
- API 文件需包含 endpoint、參數、回傳格式

---

# 6. When Responding as Copilot（Copilot 回覆注意事項）

1. 若使用者說「新增 measure」  
   → 需產生符合本專案格式的 JSON，並提醒需標註文獻來源。

2. 若使用者說「新增論文」  
   → 需產生 paper metadata JSON，並詢問該論文使用的 factors / measures。

3. 若需求涉及 **資料欄位定義**  
   → 提醒：需向 @Data 部門提出正式 Request。

4. 若需求涉及 **策略回測邏輯**  
   → 提醒：本專案提供 measure 定義，實際策略邏輯由 @Research 負責。

5. 若需求涉及 **API 建置**  
   → 提醒：API 由 @Application 部門實作，本專案提供 Schema 與資料定義。

6. 若需求缺乏資訊  
   → 回覆需要補充的項目（清單化）。

---

# 7. Project-level Forbidden Actions（本專案禁止行為）

你不得：

- 創造不存在的 measure 定義格式
- 假設 measure 的計算公式（需有文獻依據）
- 發明本專案不存在的因子分類
- 修改 MeasureDefinitionManager / MeasureRetriever 的介面（屬 Data Team）
- 定義策略邏輯（屬 Research）
- 建立 API endpoint（屬 Application，第三階段）
- 直接存取底層資料庫（需透過 Retriever 介面）

---

# 8. Testing（測試）

## 8.1 測試框架與位置
- 測試框架：PyTest
- 測試目錄：`/tests`

## 8.2 專案特定測試範圍

| 測試項目 | 說明 |
|----------|------|
| `import_paper.py` | 測試 paper JSON 匯入是否正確 |
| `import_measure.py` | 測試 measure JSON 匯入是否正確 |
| `link_paper_measure.py` | 測試 paper-measure 關聯建立 |
| JSON 格式驗證 | 確保 JSON 符合定義的 schema |
| 資料完整性 | 確保 foreign key 關聯正確 |

## 8.3 Mock 策略

本專案需 mock 的外部依賴：
- 資料庫連線（使用 SQLite in-memory 或 mock）
- MeasureDefinitionManager 介面（若有整合測試）

## 8.4 測試執行指令

```bash
# 執行所有測試
pytest tests/

# 執行特定測試檔案
pytest tests/test_import_paper.py
pytest tests/test_import_measure.py
```

---

# 9. Integration with Qadris Ecosystem（與 Qadris 生態系整合）

## 9.1 MeasureDefinitionManager
- FactorBase 的 `measure_id` 需與 MeasureDefinitionManager 的 measure 名稱對應
- MeasureDefinitionManager 可從 FactorBase 讀取 measure 定義 JSON

## 9.2 MeasureRetriever
- FactorBase 提供 measure 的 metadata（公式、來源、標準化方式）
- MeasureRetriever 提供實際資料取得

## 9.3 FactorBackTesting
- 回測報告可自動引用 FactorBase 的文獻來源
- 根據使用的 `measure_id` 列出相關 paper 資訊

## 9.4 Copilot Agents
- @Research 可查詢：「列出所有 Value 因子的 measure」
- @Data 可查詢：「PB 這個 measure 的計算公式是什麼？」
- @Application 可查詢：「FactorBase API 需要哪些 endpoint？」

---

# 10. Milestones（里程碑）

依據 meeting_minutes.md：

| Milestone | 內容 | 預計完成日 |
|-----------|------|-----------|
| M1 | 建立 Repo + Schema + 基礎資料 | 2025-12-19 |
| M2 | 與 MeasureDefinitionManager 整合 | 2025-12-26 |
| M3 | FastAPI endpoints + 文件化 | 2026-01-09 |

---

# 11. Versioning（版本控管）

每次修訂需更新：

- Version  
- Last Updated  
- Changelog  

---

# Changelog

- 1.0 — 2025-12-05: 建立本專案初始 Copilot Instructions。

---

# End of File
