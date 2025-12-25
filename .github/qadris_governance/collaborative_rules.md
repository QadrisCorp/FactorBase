# QadrisCorp — Collaborative Rules（跨部門協作規範）
Version: 2.2  
Last Updated: 2025-12-05  
Purpose: 本文件專注於跨部門協作流程、需求文件、移交規則與衝突處理。  
Note: 所有角色與權責請參照《company_policy.md》，本文件不再重複描述。

---

# 1. General Principles（總則）

1. 所有協作必須遵守：  
   - `company_policy.md`（最高規範）  
   - 各部門 Agent 規範（以部門為名的 `*.agent.md`）  
2. 任何跨部門需求皆需正式文件，不可使用口頭/Chat。  
3. Product Spec 為所有協作流程的起點。  
4. 各部門只能依照其職責參與，不得越權。  
5. CEO 為最終仲裁者。

---

# 2. High-Level Workflow（工作流程）

完整流程：
Product → Data → Research → Data → Application → DevOps → Sales  
↓  
Trading

原則：

- 工作依序向下推進  
- 不得跳過任何中間部門  
- Trading 需在 Research 完成後方可接手  
- Sales 在完成後參與對外呈現  
- 跨部門合作須明確標註 Owner / Supporting Teams  

---

# 3. Request Workflow（需求提出流程）

所有新需求由 Product 部門主導。

## A. 發起（Product 或 CEO）

文件需包含：

- 功能概述  
- 目標客群  
- 欄位與前端需求  
- 是否涉及 Data/Research/Trading  
- 初步 UI Flow（若需要）

## B. 標註 Owner / Supporting Teams

- Owner Team  
- Supporting Teams

## C. Team 參與定位

| 部門（Agent） | 角色 |
|------|------|
| Product | 定義做什麼、如何呈現 |
| Data | 欄位定義、資料可行性 |
| Research | 指標與策略邏輯 |
| Application | 系統實作 |
| Infrastructure | 部署、CI/CD |
| Trading | 策略落地 |
| Sales | 對外溝通 |

---

# 4. Boundary Rules（越權界線）

各部門不得：

- Application → 修改資料庫（屬 Data）  
- Data → 決定前端呈現（屬 Product）  
- Research → 建 API（屬 Application）  
- Trading → 更改 signal（屬 Research）  
- Ops → 調整邏輯程式碼  
- Sales → 重寫 Spec  

跨權限需求必須提出正式 Request。

---

# 5. Unified Data Access Interface（統一資料存取介面）

## 5.1 強制規定

所有跨部門系統在正式資料存取時：

- **必須使用** MeasureRetriever 或 DataRetriever 取得資料
- **不得** 直接查詢底層資料庫（`marketrawdb_*`、`marketstddb`、`indistockdb` 等）
- **不得** 自行建立資料連線繞過 Retriever 介面

## 5.2 漸進式推動策略

| 階段 | 適用範圍 | 執行方式 | 目標時程 |
|------|----------|----------|----------|
| **新專案** | 所有新建專案 | 強制使用 MeasureRetriever/DataRetriever | 立即生效 |
| **既有專案** | 已運行系統 | 列出清單，排定遷移計畫逐步導入 | 依專案規模評估 |

### 既有專案遷移流程

1. **盤點階段：** 列出所有直接存取資料庫的系統與連線點
2. **評估階段：** 依影響範圍與複雜度排序優先級
3. **遷移階段：** 逐一替換為 Retriever 介面
4. **驗證階段：** 確認功能正常、效能無異常
5. **下線階段：** 移除舊有直接連線權限

## 5.3 例外申請流程

以下情境可申請例外直接存取底層資料庫：

- **維運需求：** 資料庫維護、效能調校
- **緊急排查：** 生產環境問題緊急處理
- **資料遷移：** 大規模資料搬移作業

### 例外申請 Request 格式

```markdown
## Request Title: 資料庫直接存取例外申請

**Requestor:** {申請人/部門}  
**申請類型:** 維運 / 緊急排查 / 資料遷移 / 其他  
**目標資料庫:** {database name}  
**存取目的:**  
{詳述為何需要直接存取}  

**預計時間:** {開始 ~ 結束}  
**影響範圍:**  
{說明對其他系統的影響}  

**核准:** {Data Team 負責人簽核}  
```

## 5.4 違規處理

- 未經核准直接存取底層資料庫，視為越權行為
- 需回溯說明並補申請
- 重複違規將升級至 CEO 裁決

---

# 6. Communication Format（跨部門文件格式）

所有跨部門文件必須使用 Markdown。格式如下：

Request Title
Requestor:
Owner Team:
Supporting Teams:
Summary:
(3–5 句話)

Background:
Requirements:
Expected Output:
Impact:

Data

API

Frontend

Trading

Deployment

Docs/Sales

Deadline:
(Optional)


---

# 7. Handover Rules（移交規則）

每次部門移交必須附上：

- 完整文件（Spec/schema/flow/strategy spec）  
- MVP 或範例輸出  
- 測試資料/案例  
- 版本標記與 Changelog  

移交不完整，接手 Team 有權拒收。

---

# 8. Repository Rules（專案協作）

- main 永遠可部署  
- 所有工作用 feature branch  
- **所有程式碼變更必須先建立 Issue，並透過 Pull Request 合併，禁止直接 push 到 main 或受保護分支**  
- 每一個 PR 必須關聯至少一個 Issue（例如 `Fixes #123`）  
- PR 至少需一位 Reviewer  
- PR 必須附帶文件或規格更新  

推薦 Repo 結構：

- Product → `docs/product/`  
- Data → `docs/data/` + `/schemas/`  
- Research → `research/`  
- Application → `api/`、`frontend/`  
- Trading → `trading/`  
- DevOps → `deploy/`  
- Sales → `docs/marketing/`

---

# 9. Conflict Resolution（衝突處理）

若出現衝突：

1. 回到 Product Spec  
2. 由 Owner Team 審查  
3. Supporting Team 提建議  
4. 無法決策 → CEO 裁決  

---

# 10. 與 OmniQ（CEO Office）的協作

## 10.1 OmniQ 的角色

OmniQ 是 CEO 的幕僚長，負責：
- 跨部門資訊彙整
- 會議管理與追蹤
- 行政性任務處理
- 協調部門間資訊傳遞

## 10.2 各部門與 OmniQ 的協作方式

1. **資訊提供**：當 OmniQ 需要彙整部門狀態時，各部門應配合提供：
   - 專案進度
   - 阻礙與風險
   - 資源需求

2. **專業決策**：OmniQ 不介入部門專業決策，各部門仍保有：
   - 技術選型權
   - 實作方式決定權
   - 部門內部流程自主權

3. **跨部門協調**：當需要跨部門協調時：
   - 可透過 OmniQ 協助彙整資訊
   - 實際決策仍需相關部門直接溝通
   - OmniQ 可協助安排會議或追蹤進度

4. **行政支援**：OmniQ 可協助：
   - 會議紀錄與追蹤
   - 行動項目提醒
   - 公司文件維護

---

# 11. Versioning

每次更新需版本號 + 日期 + Changelog。

---

# Changelog

- 2.2 — 2025-12-05: 新增與 OmniQ（CEO Office）的協作規範（Section 10）
- 2.1 — 2025-12-01: 新增統一資料存取介面規範（Section 5），包含漸進式推動策略、既有專案遷移流程與例外申請流程
- 2.0 — 2025-12-01: 初始版本

---

# End of Document

