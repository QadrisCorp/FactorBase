# QadrisCorp — {PROJECT_NAME} Copilot Instructions
Version: 1.0  
Last Updated: {DATE}  
Scope: 本文件為「本專案專用」的 Copilot 行為規範。  
All Copilot outputs must follow QadrisCorp’s global governance and this project’s rules.

---

# 1. Project Summary（專案摘要）

**專案名稱：** {PROJECT_NAME}  
**專案目的：** {DESCRIPTION}  
**主要功能或目標：**
- {Goal_1}
- {Goal_2}
- {Goal_3}

**專案 Owner Team：** {Product / Data / Application / Research / Trading / Infrastructure / Sales}  
**Supporting Teams：** {Teams}  

（註：此為專案的定位與範圍，不取代 Product Spec。）

---

# 2. Project Boundaries（專案邊界）

本專案必須同時遵守：

- 《company_policy.md》  
- 《collaborative_rules.md》  
- 《copilot-instructions-global.md》  
- 七大部門 Agent（含別名）：  
  | 部門 Agent | 別名 |
  |------------|------|
  | @Product | @Prod |
  | @Application | @App |
  | @Data | — |
  | @Research | @Res |
  | @Trading | — |
  | @Infrastructure | @Dev |
  | @Sales | — |

本文件只定義「本專案特有」的要求，不覆蓋全域規範。

---

# 3. Project Architecture（專案架構）

（請依專案內容填寫）

## 3.1 技術棧（Tech Stack）
- Backend: {FastAPI / Flask / Node.js …}
- Frontend: {HTML / React / Vue …}
- Database: {MySQL / MariaDB / PostgreSQL …}
- Data Source: {DataRetriever / MeasureRetriever / External API …}

## 3.2 專案資料流（Data Flow）
- Source → {Stage 1} → {Stage 2} → Output  
- Example:  
TWSE API → DataRetriever → std tables → Application API → Frontend

## 3.3 專案目錄結構（若已固定）
/api
/frontend
/docs
/scripts
/tests


---

# 4. Project-specific Rules（本專案專屬規則）

（根據專案需求填寫）

## 4.1 專案開發限制
- 本專案 **不可使用未經 Data Team 定義的欄位**
- 本專案 **不可創造新資料來源**
- 本專案 **不可修改 global DECIMAL 精度**
- 本專案前後端需依 {Product} 設計稿

## 4.2 專案行為規範
- 所有 API 必須符合 schema（詳細定義見 `/api/schemas.py`）
- 所有前端頁面需採用 {UI Guideline}
- 若為 Data-heavy 專案 → 必須引用 Data Team 欄位表
- 若為 Research 專案 → 必須引用 Research 因子定義書

---

# 5. Deliverable Standards（輸出成果標準）

所有 Copilot 產出需符合：

## 5.1 程式碼
- 必須可運行  
- 必須具備註解與型別標註  
- 結構需遵守專案既有模式（如 service/router/schema 三層架構）  

## 5.2 文件
- 需為完整 Markdown  
- 必須附帶說明、流程、步驟  
- API/Schema 必須包含欄位表與 JSON 示例

## 5.3 架構/流程
- 需提供清楚的 UML / Mermaid 圖  
- 設計決策需具備 rationale（為何如此設計）

---

# 6. When Responding as Copilot（Copilot 回覆注意事項）

1. 若使用者說「寫程式」  
   → 需依本專案技術棧與既有架構產生。

2. 若需求跨部門  
   → Copilot 需提醒：依《collaborative_rules.md》送出正式 Request。

3. 若需求缺乏資訊  
   → 回覆需要補充（清單化）。

4. 若需求與角色不符  
   → 引導使用者呼叫對應部門 Agent（例如：@Data）。

---

# 7. Project-level Forbidden Actions（本專案禁止行為）

你不得：

- 換用不相符的技術棧（如專案是 FastAPI 卻產生 Flask）
- 創造不存在的欄位/表格/API
- 假設資料來源未經定義
- 發明本專案不存在的模組
- 修改資料庫 schema（除非本專案由 Data Team 主導）
- 定義策略邏輯（除非 Research 為 Owner）

---

# 8. Testing（測試）

（依《copilot-instructions-global.md》Section 9 通用規範，並補充專案特定要求）

## 8.1 測試框架與位置
- 測試框架：PyTest
- 測試目錄：`/tests`

## 8.2 專案特定測試範圍

需覆蓋的測試項目（依專案填寫）：

| 測試項目 | 說明 |
|----------|------|
| {模組/類別 1} | {測試重點} |
| {模組/類別 2} | {測試重點} |
| 錯誤處理 | 例外狀況與邊界條件 |

## 8.3 Mock 策略

本專案需 mock 的外部依賴：
- {資料庫連線}
- {外部 API 請求}
- {其他外部服務}

## 8.4 測試執行指令

```bash
# 執行所有測試
pytest tests/

# 執行特定測試檔案
pytest tests/test_{模組名}.py
```

---

# 9. Versioning（版本控管）

每次修訂需更新：

- Version  
- Last Updated  
- Changelog  

---

# Changelog
- 1.1 — {DATE}: 新增 Section 8 Testing 測試規範。
- 1.0 — {DATE}: 建立本專案初始 Copilot Instructions。

---

# End of File
