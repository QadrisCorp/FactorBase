# FactorBase Paper Import Log

本檔案記錄所有論文新增的歷史紀錄。

---

## Log Format

| 欄位 | 說明 |
|------|------|
| Date | 新增日期 |
| Paper ID | 論文識別碼 |
| Title | 論文標題 |
| Authors | 作者 |
| Year | 年份 |
| Source | 來源（PDF/DOI/Manual） |
| Measures Linked | 關聯的 Measures 數量 |
| Added By | 新增者（Agent/User） |
| Status | 狀態（success/failed） |

---

## Import History

### 2025-12-09

| Date | Paper ID | Title | Authors | Year | Source | Measures Linked | Added By | Status |
|------|----------|-------|---------|------|--------|-----------------|----------|--------|
| 2025-12-09 | paper_010 | The Volatility Effect: Lower Risk without Lower Return | Blitz, David C.; van Vliet, Pim | 2007 | PDF | 2 | @Research Agent | ✅ success |
| 2025-12-09 | paper_009 | The Volatility Effect Revisited | Blitz, van Vliet, Baltussen | 2019 | PDF | 2 | @Research Agent | ✅ success |
| 2025-12-09 | paper_008 | Factor Momentum and the Momentum Factor | Ehsani, Sina; Linnainmaa, Juhani T. | 2019 | PDF | 5 | @Research Agent | ✅ success |

---

## Initial Papers (Pre-log)

以下論文在 log 機制建立前已存在：

| Paper ID | Title | Year |
|----------|-------|------|
| paper_001 | Common risk factors in the returns on stocks and bonds | 1993 |
| paper_002 | On Persistence in Mutual Fund Performance | 1997 |
| paper_003 | A Five-Factor Asset Pricing Model | 2015 |
| paper_004 | The Other Side of Value: The Gross Profitability Premium | 2013 |
| paper_005 | Digesting Anomalies: An Investment Approach | 2015 |
| paper_006 | Asset Growth and the Cross-Section of Stock Returns | 2008 |
| paper_007 | Quality Minus Junk | 2019 |

---

## Notes

- 所有新增的論文應在此 log 中記錄
- PDF 檔案存放於 `papers/raw/`
- Metadata JSON 存放於 `papers/metadata/`
- 驗證結果由 `scripts/validate_json.py` 產生
