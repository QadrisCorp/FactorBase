FactorBase

FactorBase 是一套針對「因子投資文獻 × 因子定義 × measure 計算方法」所設計的專業知識庫（Factor Knowledge Base），用於支援研究與系統開發。

🎯 專案目的（Project Purpose）

因子投資領域中，同一因子常被使用不同的 measure 衡量，例如：

Value → PB、EP、CP、BM 等

Momentum → MOM12M、MOM6M、MOM12M_excl1M

Quality → ROE、GM、Accruals 等

文獻中 measure 的定義不僅多樣，計算方式也不一致：

使用不同的時間窗：TTM / MRQ / 12M / 36M

使用不同資料來源：財報、價格、法人預估

使用不同標準化方法：rank / z-score / winsorize

因此需要一個統一的資料庫，提供：

因子分類（Factors）

measure 定義（Measures）

因子文獻（Papers）

文獻與 measure 的關聯（PaperMeasures）

FactorBase 是這些資料的唯一權威來源（Single Source of Truth）。

📚 系統內容（Components）
1. Papers — 因子研究文獻

儲存每篇文獻的：

標題、作者、年份、期刊

市場（US、TW、JP…）

研究重點摘要

因子結果與顯著性

研究是否可複製（replicability）

2. Factors — 因子層級定義

提供統一的因子分類，如：

Value

Size

Momentum

Profitability

Investment

Quality

Sentiment

3. Measures — measure 計算定義

每一個 measure 的 JSON 包含：

measure 名稱（PB、ROE_TTM、MOM12M…）

所屬因子

計算公式（pseudo-code 或 formula tree）

參數（window, frequency, normalization）

使用資料來源

4. PaperMeasures — 文獻 × measure 關聯

例如：

Fama & French (1993) → 使用 Size（ME）、Value（BM）

Novy-Marx (2013) → 使用 Gross Profitability

Carhart (1997) → 使用 Momentum（MOM12M_ex1M）

🗄 資料表 Schema（SQL）

位於 sql/create_tables.sql：

papers

factors

measures

paper_measures

（若你需要，我可以直接產生完整 SQL 版本）

🧩 與 Qadris 生態系整合

FactorBase 與以下模組自然整合：

MeasureDefinitionManager

從 FactorBase 自動載入 measure 定義

MeasureRetriever

透過 measure_id 提供欄位查詢與資料取得

FactorBackTesting

回測結果可自帶文獻引用與因子方法解釋

Copilot / Agents

可自動回答：

「請列出所有在台股文獻中常用的 Value measure」

🚀 未來功能（Roadmap）

FactorBase Web API

文獻自動解析（PDF → measure 抽取）

因子熱度分析（最常使用的 measure 統計）

與 QadrisWebAPI 整合成對外商用 API

✨ 範例：Measure JSON（PB measure）
{
  "measure_id": "PB",
  "factor": "Value",
  "description": "Price-to-Book ratio",
  "formula": {
    "type": "ratio",
    "numerator": "market_cap",
    "denominator": "book_value_equity",
    "window": "MRQ"
  },
  "data_source": ["market_quotes", "financial_statements"],
  "frequency": "daily",
  "normalization": "zscore_cross_sectional"
}

✨ 範例：Paper Metadata JSON
{
  "title": "Common risk factors in the returns on stocks and bonds",
  "authors": "Fama, Eugene; French, Kenneth",
  "year": 1993,
  "journal": "Journal of Financial Economics",
  "market": "US",
  "abstract": "...",
  "conclusion_sign": "positive",
  "replicable": "yes"
}