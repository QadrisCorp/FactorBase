# 📝 會議記錄：新專案會議

- **日期**：2025-12-05
- **時間**：02:07 ~ 02:45 UTC
- **地點 / 會議室**：線上會議
- **主持人**：CEO
- **紀錄人**：Copilot 會議小幫手
- **參與部門**：全部門
- **出席名單**：
  - Product & UX Team：Helena
  - Application Team：Apprex
  - Data Team：Qadriaw
  - Research Team：Fama
  - Trading Team：Renaisk
  - Infrastructure & DevOps Team：Opskova
  - Sales & Marketing Team：Leon
- **缺席名單**：
  - 無

---

## 1️⃣ 會議目的

> 討論新專案可行性、確定範圍與負責人

- 待 CEO / 發起人提出新專案內容

---

## 2️⃣ 會議類型

- [ ] 進度追蹤會議（例行）
- [x] 新專案會議
- [ ] 問題／危機處理
- [ ] 其他

---

## 3️⃣ 議程（Agenda）

1. CEO / 發起人提出新專案想法
2. 各部門回應
3. 跨部門討論
4. 會議總結與下一步動作
5. 臨時動議（如有）

---

## 4️⃣ 公司現況摘要（會前報告）

### 📈 各 Repository 狀態總覽

| Department | Repository | Issues | PRs | Active Branch |
|------------|------------|--------|-----|---------------|
| CEO | QadrisCorp | 0 | 1 | main |
| CEO | vscode_workspace | 0 | 0 | main |
| Data | DataRetriever | 1 | 0 | main |
| Data | IndiStockDataImporter | 0 | 0 | main |
| Data | MeasureDefinitionManager | 2 | 0 | main |
| Data | MeasureRetriever | 12 | 0 | main |
| Data | RawDataImporter | 1 | 0 | main |
| Data | StdDataImporter | 1 | 0 | main |
| Data | TWFinCrawler | 0 | 0 | main |
| Data | TableSync | 0 | 0 | main |
| Product | Proxy | 1 | 0 | main |
| Product | QadrisWebAPI | 7 | 0 | main |
| Product | TWMarketWatch | 0 | 0 | main |
| Research | GroupTesting | 0 | 0 | main |
| Trading | QadrisAccountingSystem | 0 | 0 | main |
| Trading | QadrisTradingSystem | 1 | 0 | main |

---

## 5️⃣ 新專案討論紀錄

### 5.1 CEO / 發起人提案內容

- **專案名稱**：**FactorBase — 因子知識庫**
- **專案背景與目的**：
  - FactorBase 是一套系統化整理所有因子文獻、因子定義與 measure 計算方法的知識庫
  - 提供研究、回測、系統開發與 AI Agent 的共同資料來源（Single Source of Truth）
  - 解決因子投資領域中「同一因子被不同 measure 衡量」的混亂問題
- **核心功能**：
  1. 收集並結構化整理所有因子相關文獻（Papers）
  2. 定義標準化的因子分類（Factors）
  3. 統一定義各種 measure（Measures）
  4. 建立文獻與 measure 的關聯地圖（PaperMeasures）
  5. 提供 API / DB / JSON 介面供各團隊與 Copilot 使用
- **商業目標 / 成功指標 (KPI)**：
  - 建立 Single Source of Truth，統一因子定義
  - 支援 MeasureDefinitionManager、MeasureRetriever、FactorBackTesting
  - 未來可商品化為對外 API
- **預估時程 / 優先順序**：
  - 第一階段（1-2 週）：建立四個資料表、手動輸入 10-20 個 measures
  - 第二階段：建立匯入工具、與 MeasureDefinitionManager 整合
  - 第三階段：加入 API、整合 FactorBackTesting 報告

### 5.2 各部門回應重點

#### Product & UX Team (Helena)
- **影響與機會**：（待回應）
- **所需資源**：（待回應）
- **風險 / 前置條件**：（待回應）

#### Application Team (Apprex)
- **影響與機會**：（待回應）
- **所需資源**：（待回應）
- **風險 / 前置條件**：（待回應）

#### Data Team (Qadriaw)
- **影響與機會**：（待回應）
- **所需資源**：（待回應）
- **風險 / 前置條件**：（待回應）

#### Research Team (Fama)
- **影響與機會**：（待回應）
- **所需資源**：（待回應）
- **風險 / 前置條件**：（待回應）

#### Trading Team (Renaisk)
- **影響與機會**：（待回應）
- **所需資源**：（待回應）
- **風險 / 前置條件**：（待回應）

#### Infrastructure & DevOps Team (Opskova)
- **影響與機會**：（待回應）
- **所需資源**：（待回應）
- **風險 / 前置條件**：（待回應）

#### Sales & Marketing Team (Leon)
- **影響與機會**：（待回應）
- **所需資源**：（待回應）
- **風險 / 前置條件**：（待回應）

### 5.3 討論結論（新專案）

- **是否立案**：
  - [x] 是，成立專案：**FactorBase — 因子知識庫**
  - [ ] 否，暫緩／取消，原因：（待確認）
- **預計負責人（PM / Owner）**：**Fama (Research Team)**
- **技術協作**：Qadriaw (Data Team) + Apprex (Application Team)
- **初步 Milestones**：
  - M1：建立 Repo + Schema + 基礎資料，預計完成日：2025-12-19
  - M2：與 MeasureDefinitionManager 整合，預計完成日：2025-12-26
  - M3：FastAPI endpoints + 文件化，預計完成日：2026-01-09

---

## 6️⃣ 跨部門議題與決策

| # | 議題 | 涉及部門 | 決策 / 解法摘要 | 後續負責人 |
|---|------|----------|----------------|------------|
| 1 | （待記錄） | | | |

---

## 7️⃣ 行動項目（Action Items）摘要

| # | Action Item | Owner | Due Date | Status |
|---|-------------|-------|----------|--------|
| 1 | 建立 GitHub Repo `QadrisCorp/FactorBase` | CEO 小幫手 | 2025-12-05 | ✅ 完成 |
| 2 | 建立資料庫 Schema（`create_tables.sql`）| Qadriaw (Data) | 2025-12-12 | ⬜ |
| 3 | 定義 Factors Taxonomy（3-5 個核心因子）| Fama (Research) | 2025-12-12 | ⬜ |
| 4 | 建立 10-20 個代表性 Measures 定義 JSON | Fama (Research) + Qadriaw (Data) | 2025-12-19 | ⬜ |
| 5 | 整理 5-10 篇關鍵文獻（Papers metadata）| Fama (Research) | 2025-12-19 | ⬜ |
| 6 | 寫 `import_paper.py` / `import_measure.py` 腳本 | Apprex (Application) | 2025-12-19 | ⬜ |
| 7 | 與 MeasureDefinitionManager 整合測試 | Qadriaw (Data) | 2025-12-26 | ⬜ |

---

## 8️⃣ 臨時動議

- （待記錄）

---

## 9️⃣ 風險與阻礙（需追蹤）

| # | 風險 / 阻礙 | 影響 | 應對策略 | Owner |
|---|-------------|------|----------|-------|
| 1 | （待記錄） | | | |

---

## 🔚 會議結論摘要

> 讓之後回頭看這份紀錄時，可以 10 秒看懂這場會議的重點。

1. ✅ **立案通過**：FactorBase — 因子知識庫專案正式成立
2. 📌 **PM 指定**：Fama (Research Team) 擔任專案負責人
3. 🔧 **技術選型**：第一階段使用 JSON + SQLite 快速驗證
4. 📂 **Repo 建立**：CEO 小幫手立即建立 `QadrisCorp/FactorBase`
5. 🤝 **跨部門協作**：Research（定義）+ Data（Schema）+ Application（腳本）

---

## 📎 附件 / 相關連結

- 會議報表：`reports/meeting_20251205.md`
- 狀態摘要：`reports/repo_summary_20251205.md`
- **FactorBase Repo**：https://github.com/QadrisCorp/FactorBase
- 專案概念文件：`FactorBase-concept.md`
- 專案實作文件：`FactorBase-implement.md`
- 專案 README：`FactorBase-README.md`

---

_本紀錄由 Copilot 會議小幫手 撰寫_
_最後更新：2025-12-05 02:45 UTC_
