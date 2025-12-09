# FactorBase
# FactorBase：因子知識庫（Concept Layer）

FactorBase 是 Qadris 因子研究體系中的「文獻概念層」，負責管理所有因子研究的核心知識本體（Knowledge Graph）。  
本 repo **完全不處理計算、資料欄位、回測或實作邏輯**，僅專注於文獻與概念的結構化管理。

---

## 📘 1. 系統定位

FactorBase 的目標是：

- 將所有因子研究文獻整理成結構化資料  
- 建立標準化的因子定義（factor）  
- 建立文獻中的衡量方法（concept measure）  
- 建立「文獻使用了哪些衡量方式」的對應（paper-measure mapping）  

FactorBase 是整個 Qadris Factor 系統的知識根基，後續的實作（MeasureRetriever）與產品整合（QadrisFactorBase）皆依賴此層的定義。

---

## 📚 2. FactorBase 管理的核心實體

### **2.1 Paper（研究來源）**
包含：
- 研究標題
- 作者
- 發表年份
- 研究摘要
- DOI / URL（若有）

此表即 Qadris 的文獻資料庫。

---

### **2.2 Factor（因子概念）**
例如：
- Value
- Momentum
- Profitability
- Investment
- Size
- Low-volatility

FactorBase 不負責公式、計算或市場差異，僅負責概念定義。

---

### **2.3 Concept Measure（概念衡量方式）**
例如：
- PB、PE、BM
- Earnings-to-Price
- Mom12-1
- ROE, ROA

此層負責定義在文獻中出現的衡量方式，但不負責實作。

---

### **2.4 Paper–Measure Mapping**
描述「某篇 paper 使用了哪些 concept measure」。

範例：
Paper: Fama & French (1992)
Concept measures: BM, Earnings-to-Price, Size


---

## 🚫 3. FactorBase 不處理
請注意，FactorBase 明確不處理：

- 實際資料欄位（如 TSE 表格欄位）
- 計算邏輯（winsorize、rolling、標準化等）
- 市場區分（TW / US…）
- 實作 measure
- 回測設定
- 回測結果

這些由 **MeasureRetriever** 與 **QadrisFactorBase** 與 **FactorBackTest** 分層處理。

---

## 🗂 4. 目錄結構（建議）
FactorBase/
├── data/
│ ├── papers.csv
│ ├── factors.csv
│ ├── concept_measures.csv
│ └── paper_measure_map.csv
├── docs/
│ └── schema_design.md
└── README.md


---

## 🧭 5. 與其他 Repo 的關係

| Repo | 功能 | 與 FactorBase 的關係 |
|------|------|----------------------|
| MeasureRetriever | 計算邏輯與實作 measure | 依照 FactorBase 的概念定義 |
| FactorBackTest | 回測引擎 | 不直接互動 |
| QadrisFactorBase | 產品與 metadata 中心 | 使用 FactorBase 定義進行 mapping 與研究編排 |

---

## 📄 6. 授權與貢獻
歡迎提交 PR、Issue，以完善因子研究知識庫。

---

# 📘 FactorBase 是 Qadris 因子研究的概念中心。  


