# QadrisCorp — Copilot Instructions Standard

Version: 1.1  
Last Updated: 2025-12-25  
Scope: 建立或更新專案 copilot-instructions.md 的標準流程

---

## 1. 概述

每個 QadrisCorp 專案都必須擁有專屬的 `.github/copilot-instructions.md` 檔案，以確保 Copilot 能正確理解專案上下文並提供精準的協助。

---

## 2. 資訊來源優先順序

> ⚠️ **核心原則**：程式碼是唯一的真相來源（Single Source of Truth）

| 優先順序 | 來源 | 權威性 | 用途 |
|:--------:|------|--------|------|
| 1 | **程式碼本身** | 最高（必須依據） | 技術架構、模組名稱、API、資料流 |
| 2 | README.md | 中（概念參考） | 專案目的、使用場景、快速理解 |
| 3 | product_spec.md | 低（設計參考） | 原始設計意圖（可能與實作有差異） |

### 為什麼程式碼優先？

- **README.md**：給人類閱讀，偏概念性描述
- **product_spec.md**：設計階段文件，實作後通常不再更新
- **程式碼**：永遠是最新、最準確的實作狀態

---

## 3. 前置條件

在建立或更新 `copilot-instructions.md` **之前**，Copilot **必須**：

1. **完整閱讀專案程式碼**（必要）
   - 瀏覽專案目錄結構
   - 閱讀進入點檔案（main.py, run.py, app.py 等）
   - 閱讀核心模組程式碼
   - 了解資料流與模組相依性
   - 識別使用的技術棧（語言、框架、資料庫等）

2. **閱讀輔助文件**（如存在）
   - README.md：了解專案目的與使用場景
   - product_spec.md：了解原始設計意圖（注意：以程式碼為準）

3. **讀取模板檔案**
   - `.github/qadris_templates/copilot-instructions-template.md`

---

## 4. 標準流程

### 步驟 1：完整閱讀專案程式碼

```
必須分析：
- [ ] 目錄結構（實際架構）
- [ ] 進入點檔案（main.py, run.py, app.py 等）
- [ ] 核心模組（識別主要功能）
- [ ] requirements.txt / pyproject.toml（技術棧）
- [ ] 測試檔案（了解測試範圍）
- [ ] 設定檔（.env.example, config.py 等）
```

### 步驟 2：閱讀輔助文件（如存在）

| 文件 | 取用資訊 | 注意事項 |
|------|----------|----------|
| README.md | 專案目的、使用場景 | 概念性描述，可能簡化 |
| product_spec.md | 原始設計意圖 | 可能過時，以程式碼為準 |
| doc/*.md | 特定模組說明 | 需驗證與程式碼一致 |

### 步驟 3：收集專案資訊

**資訊來源對照表**（從哪裡取什麼）：

| 項目 | 主要來源 | 輔助來源 | 備註 |
|------|----------|----------|------|
| 專案名稱 | repo 名稱 | README.md | — |
| 專案目的 | README.md | product_spec.md | 概念性描述 |
| Owner Team | 專案類型判斷 | README.md | — |
| Supporting Teams | 相依性分析 | — | 看 import 了哪些內部專案 |
| 技術架構 | **程式碼分析** | product_spec.md | ⚠️ 必須從程式碼確認 |
| 資料流 | **程式碼分析** | product_spec.md | ⚠️ 必須從程式碼確認 |
| 模組名稱 | **程式碼（準確）** | ❌ 不可從文件取 | ⚠️ 絕對禁止猜測 |
| API/函數名稱 | **程式碼（準確）** | ❌ 不可從文件取 | ⚠️ 絕對禁止猜測 |
| 專案特有限制 | 專案需求 | product_spec.md | — |
| 測試範圍 | 測試程式碼 | — | 看 mock 了什麼 |

### 步驟 4：依模板產生內容

使用 `.github/qadris_templates/copilot-instructions-template.md` 作為基礎，填入收集到的資訊。

**必填區塊**：
- 專案概要（Section 1）
- 技術架構（Section 2）

**選填區塊**（依專案需要）：
- 專案專屬規則（Section 3）
- 測試範圍（Section 4）

### 步驟 5：放置檔案

將產生的檔案放置於：
```
{專案根目錄}/.github/copilot-instructions.md
```

### 步驟 6：驗證內容

檢查清單：
- [ ] 所有 `{placeholder}` 都已替換為實際內容
- [ ] Owner Team 與 Supporting Teams 正確
- [ ] 技術架構描述準確（與程式碼一致）
- [ ] 資料流描述清楚（與程式碼一致）
- [ ] 所有模組、API 名稱都來自程式碼（非文件）
- [ ] 無自行創造的模組或 API 名稱

---

## 5. 更新時機

以下情況需要更新 `copilot-instructions.md`：

| 情況 | 需更新的區塊 |
|------|-------------|
| 新增主要功能 | 專案概要、技術架構 |
| 變更技術棧 | 技術架構 |
| 修改資料流 | 技術架構 |
| 新增開發限制 | 專案專屬規則 |
| 新增外部依賴 | 測試範圍 |

---

## 6. 禁止事項

- **禁止**：未閱讀專案程式碼就產生 copilot-instructions.md
- **禁止**：僅依據 README.md 或 product_spec.md 產生內容（必須驗證程式碼）
- **禁止**：創造不存在的模組、API、欄位名稱
- **禁止**：從文件中複製模組/API 名稱而未驗證程式碼
- **禁止**：複製其他專案的 copilot-instructions.md 而不修改
- **禁止**：遺漏必填區塊
- **禁止**：保留未替換的 `{placeholder}`

---

## 7. 範例

### 7.1 專案概要範例

```markdown
## 1. 專案概要

| 項目 | 說明 |
|------|------|
| **專案名稱** | TWMarketWatch |
| **專案目的** | 台灣股市即時監控與報價推播系統 |
| **Owner Team** | Application |
| **Supporting Teams** | Data, Infrastructure |

**主要功能：**
- 即時股價監控與警示
- 歷史走勢圖表
- 自訂監控清單
```

### 7.2 技術架構範例

```markdown
## 2. 技術架構

| 層級 | 技術 |
|------|------|
| Backend | FastAPI |
| Frontend | React + TypeScript |
| Database | MariaDB |
| Data Source | DataRetriever (股價資料) |

**資料流：**
```
DataRetriever → API Server → WebSocket → Frontend
```
```

---

## Changelog

- 1.1 (2025-12-25): 新增資訊來源優先順序、強化程式碼優先原則
- 1.0 (2025-12-25): 初版建立
