# {PROJECT_NAME} — Copilot Instructions

Version: 1.0  
Last Updated: {DATE}  
Scope: 本專案專屬 Copilot 規範

---

## ⚠️ 必讀前置條件（Required Pre-read）

**Copilot 在回應任何請求前，必須先讀取：**

- `.github/qadris_governance/copilot-instructions-global.md` — 全公司通用規範（含規範文件索引）

此為全公司通用規範，所有回應都必須遵守。若無法讀取，需告知使用者。

---

本文件僅定義「本專案特有」的規範，全域規範請參閱上述文件。

---

## 1. 專案概要

| 項目 | 說明 |
|------|------|
| **專案名稱** | {PROJECT_NAME} |
| **專案目的** | {DESCRIPTION} |
| **Owner Team** | {Product / Data / Application / Research / Trading / Infrastructure / Sales} |
| **Supporting Teams** | {Teams} |

**主要功能：**
- {Goal_1}
- {Goal_2}

---

## 2. 專案設定 (Project Config)

> 此區塊定義本專案特有的設定，AI Agent 在開發時需遵守。

### 2.1 內部資源使用
| 設定 | 值 | 說明 |
|------|---|------|
| **使用內部資源** | {YES/NO} | 本專案是否整合公司內部工具/API/資料庫 |
| **相依內部工具** | {工具清單或 NONE} | 例：MeasureRetriever, QadrisWebAPI |
| **資料庫存取** | {資料庫清單或 NONE} | 例：qadris_main, qadris_factor |

### 2.2 技術堆疊
| 設定 | 值 |
|------|---|
| **主要語言** | {Python / TypeScript / ...} |
| **框架** | {FastAPI / Next.js / ...} |
| **Python 版本** | {3.11+} |
| **Package Manager** | {pip / poetry / npm / pnpm} |

### 2.3 專案特定規則
- {RULE_1}
- {RULE_2}

---

## 3. 技術架構

| 層級 | 技術 |
|------|------|
| Backend | {FastAPI / Flask / ...} |
| Frontend | {React / Vue / HTML / ...} |
| Database | {MySQL / MariaDB / ...} |
| Data Source | {DataRetriever / MeasureRetriever / ...} |

**資料流：**
```
{Source} → {Process} → {Output}
```

---

## 4. 專案專屬規則

> 以下為本專案特有的限制與規範，不覆蓋全域規範。

### 4.1 開發限制

- {限制 1，例如：不可使用未定義欄位}
- {限制 2}

### 4.2 禁止行為

- {禁止 1，例如：不可換用其他框架}
- {禁止 2}

---

## 5. 測試範圍（專案特定）

> 通用測試規範請參閱 `testing-standard.md`

本專案需 Mock 的外部依賴：
- {資料庫連線}
- {外部 API}

---

## Changelog

- 1.0 — {DATE}: 初版建立
