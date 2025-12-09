# QadrisCorp — FactorBase Copilot Instructions
Version: 2.0  
Last Updated: 2025-12-09  
Scope: 本文件為「FactorBase 專案專用」的 Copilot 行為規範。  
All Copilot outputs must follow QadrisCorp's global governance and this project's rules.

---

# 1. Project Summary（專案摘要）

**專案名稱：** FactorBase  
**專案目的：** 作為 Qadris Factor System 四層架構中的「文獻概念層」（Concept Layer），系統化整理因子文獻與概念定義的知識圖譜（Knowledge Graph）。

**四層架構定位：**
| 層級 | Repository | 職責 |
|:-----|:-----------|:-----|
| 1️⃣ | **FactorBase** | 文獻概念層 — 純知識圖譜（本專案） |
| 2️⃣ | MeasureRetriever | 實作層 — 公司級公式庫 |
| 3️⃣ | FactorBackTest | 執行層 — Stateless 回測引擎 |
| 4️⃣ | QadrisFactorBase | 產品層 — Metadata 中心與整合 |

**主要功能或目標：**
- 收集並結構化整理所有因子相關文獻（Papers）
- 定義標準化的因子分類（Factors）
- 定義「概念層」的 Measure（Concept Measures）— 僅描述學術定義，不含實作細節
- 建立文獻與 measure 的關聯地圖（PaperMeasures）
- 提供 JSON 介面供 QadrisFactorBase 與 Copilot Agents 使用

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

## 4.1 FactorBase 職責邊界

**✅ FactorBase 負責（概念層）：**
- Paper：研究來源（標題、作者、年份、DOI、BibTeX 等）
- Factor：因子概念歸類（Value, Momentum, Profitability 等）
- Concept Measure：文獻中描述的衡量方式定義（PB, EP, BM, Mom12-1 等）
- Paper–Measure：紀錄特定研究使用了哪些 Concept Measure

**❌ FactorBase 明確排除（屬於 MeasureRetriever 實作層）：**
- 資料表與欄位 Mapping（如 `marketstddb.xxx`）
- 實際計算邏輯（Winsorization, 標準化程式碼等）
- 市場特定參數設定
- 更新頻率設定（daily/monthly 等由實作層決定）

## 4.2 Paper 欄位規範

Paper metadata **必須包含**：
- `paper_id`：唯一識別碼
- `title`：論文標題
- `authors`：作者（分號分隔）
- `year`：發表年份
- `journal`：期刊名稱
- `doi`：DOI 識別碼（可為 null）
- `arxiv_id`：arXiv ID（可為 null）
- `ssrn_id`：SSRN ID（可為 null）
- `bibtex`：BibTeX 引用格式
- `market`：研究市場（US, TW, Global 等）
- `asset_class`：資產類別
- `conclusion_sign`：結論方向（positive, negative, mixed, none）
- `replicable`：可複製性（yes, no, unknown）

## 4.3 Concept Measure 欄位規範

Measure 定義 **應包含**（概念層）：
- `measure_id`：唯一識別碼
- `measure_name`：Measure 名稱
- `display_name`：顯示名稱
- `factor`：所屬因子
- `description`：文字描述
- `formula`：計算公式定義
  - `type`：公式類型（ratio, difference, percentile 等）
  - `numerator`：分子（概念名稱）
  - `denominator`：分母（概念名稱）
  - `window`：時間窗口（TTM, MRQ, 12M 等）— 依論文定義
- `normalization`：標準化方式（論文建議）
- `original_paper_id`：首次定義此 measure 的論文
- `notes`：學術備註

Measure 定義 **不應包含**（屬 MeasureRetriever）：
- ❌ `data_source`：實際資料表名稱
- ❌ `frequency`：更新頻率（daily/monthly）

## 4.4 因子分類標準（Factors Taxonomy）

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

**Measure JSON 範例（概念層）：**
```json
{
  "measure_id": "BM",
  "measure_name": "BM",
  "display_name": "Book to Market Ratio",
  "factor": "Value",
  "description": "Book to Market ratio = Book value of equity / Market capitalization. Higher BM indicates value stocks.",
  "formula": {
    "type": "ratio",
    "numerator": "book_value_equity",
    "denominator": "market_value_equity",
    "window": "MRQ"
  },
  "normalization": "zscore_cross_sectional",
  "original_paper_id": "paper_001",
  "notes": "Fama-French 三因子模型中 HML 因子的核心 sorting variable。見 Fama-French (1993)。"
}
```

**Paper JSON 範例（含 DOI/BibTeX）：**
```json
{
  "paper_id": "paper_001",
  "title": "Common risk factors in the returns on stocks and bonds",
  "authors": "Fama, Eugene F.; French, Kenneth R.",
  "year": 1993,
  "journal": "Journal of Financial Economics",
  "volume": "33",
  "issue": "1",
  "pages": "3-56",
  "doi": "10.1016/0304-405X(93)90023-5",
  "arxiv_id": null,
  "ssrn_id": null,
  "bibtex": "@article{fama1993common,\n  title={Common risk factors in the returns on stocks and bonds},\n  author={Fama, Eugene F and French, Kenneth R},\n  journal={Journal of Financial Economics},\n  volume={33},\n  number={1},\n  pages={3--56},\n  year={1993},\n  publisher={Elsevier}\n}",
  "market": "US",
  "asset_class": "Equity",
  "abstract": "This paper identifies five common risk factors...",
  "conclusion_sign": "positive",
  "replicable": "yes",
  "notes": "Seminal paper introducing the three-factor model."
}
```

**Paper-Measure 關聯 JSON 範例：**
```json
{
  "paper_measure_links": [
    {
      "paper_id": "paper_001",
      "measure_id": "BM",
      "role": "primary_sorting_variable",
      "significance": "positive",
      "notes": "用於建構 HML 因子"
    },
    {
      "paper_id": "paper_001",
      "measure_id": "ME",
      "role": "primary_sorting_variable",
      "significance": "negative",
      "notes": "用於建構 SMB 因子"
    }
  ]
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

- 2.0 — 2025-12-09: 配合 QadrisFactorBase 四層架構重新定義
  - 新增四層架構說明與職責邊界
  - Paper JSON 新增 DOI / arXiv / SSRN / BibTeX 欄位
  - Measure JSON 移除 data_source / frequency（移至 MeasureRetriever）
  - 新增 Paper-Measure 關聯 JSON 範例
  - 新增 original_paper_id 欄位
- 1.0 — 2025-12-05: 建立本專案初始 Copilot Instructions。

---

# End of File
