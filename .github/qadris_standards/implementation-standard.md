# QadrisCorp — Implementation Standard

Version: 1.0  
Last Updated: 2025-12-25  
Scope: 程式碼實作的標準流程與品質要求

---

## 1. 概述

本標準定義 QadrisCorp 專案在實作階段的流程、交付物與品質要求，適用於初版開發與後續迭代。

### 1.1 與其他標準的關係

```
issue-standard.md        → 定義「做什麼」（需求）
implementation-standard.md → 定義「怎麼做」（本文件）
architecture-standard.md → 定義「結構長什麼樣」
testing-standard.md      → 定義「測試怎麼寫」
pr-review-standard.md    → 定義「如何審查驗收」
```

---

## 2. 初版實作規範（First Version）

> ⚠️ **關鍵**：初版實作時，必須**同時產生程式碼與測試**，以便後續審查與驗證。

### 2.1 必要交付物

| 交付物 | 說明 | 對應審查階段 |
|--------|------|-------------|
| **程式碼** | 符合 `architecture-standard.md` 的目錄結構與命名 | 初版架構審查 |
| **測試程式碼** | 符合 `testing-standard.md` 的測試檔案 | 測試驗證 |
| **requirements.txt** | 依賴套件清單（如有新增） | 初版架構審查 |
| **.env.example** | 環境變數範本（如需要） | 初版架構審查 |

### 2.2 測試交付物結構

```
tests/
├── __init__.py
├── conftest.py              # pytest fixtures（如需要）
├── test_{模組名}.py         # 對應每個核心模組
└── fixtures/                # 測試資料（如需要）
    └── sample_data.json
```

### 2.3 最低測試覆蓋

| 測試類型 | 必要性 | 說明 |
|----------|--------|------|
| 正常案例測試 | ✅ 必要 | 主要功能的正常流程 |
| 邊界條件測試 | ✅ 必要 | 空資料、單一資料、極端值 |
| 錯誤處理測試 | ✅ 必要 | 例外狀況的處理 |
| 整合測試 | 選填 | 模組間互動（視專案需求） |

### 2.4 初版實作流程

```
1. 閱讀相關標準
   ├── architecture-standard.md（目錄結構）
   ├── testing-standard.md（測試規範）
   └── product_spec.md（功能需求）
        ↓
2. 建立目錄結構
   ├── src/{module}/
   └── tests/
        ↓
3. 實作核心程式碼
   └── 遵循命名規範、分層架構
        ↓
4. 同步撰寫測試 ← ⚠️ 不可跳過
   ├── 每完成一個函數，立即寫測試
   └── 使用 mock 處理外部依賴
        ↓
5. 執行測試確認通過
   └── pytest -v
        ↓
6. 自我檢查
   ├── 對照 architecture-standard.md checklist
   └── 對照 testing-standard.md checklist
```

### 2.5 初版自我檢查清單

實作完成後，AI Agent 或開發者應確認：

```
程式碼檢查：
- [ ] 目錄結構符合 architecture-standard.md
- [ ] 進入點明確（main.py / run.py / app.py）
- [ ] 無循環依賴
- [ ] 命名規範一致（snake_case / PascalCase）
- [ ] 有 type hints
- [ ] 公開介面有 docstrings

測試檢查：
- [ ] tests/ 目錄存在
- [ ] 測試檔案命名 test_{模組名}.py
- [ ] 正常案例測試存在
- [ ] 邊界條件測試存在
- [ ] 錯誤處理測試存在
- [ ] 外部依賴已 mock
- [ ] pytest 執行通過

設定檢查：
- [ ] requirements.txt 已更新（如有新依賴）
- [ ] .env.example 已建立（如有環境變數）
- [ ] .gitignore 適當設定
```

---

## 3. 迭代版本規範（Iteration）

### 3.1 功能新增

| 步驟 | 說明 | 必要 |
|------|------|------|
| 1. 閱讀現有程式碼 | 了解現有架構與命名 | ✅ |
| 2. 確認新增位置 | 依分層架構決定放置位置 | ✅ |
| 3. 實作新功能 | 遵循現有風格 | ✅ |
| 4. 新增對應測試 | 涵蓋新功能 | ✅ |
| 5. 執行全部測試 | 確保不破壞現有功能 | ✅ |
| 6. 更新文件 | README、API 文件（如適用） | 視情況 |

### 3.2 Bug 修復

| 步驟 | 說明 | 必要 |
|------|------|------|
| 1. 重現 Bug | 確認問題存在 | ✅ |
| 2. 寫失敗測試 | 先寫能重現 Bug 的測試 | ✅ |
| 3. 修復程式碼 | 讓測試通過 | ✅ |
| 4. 執行全部測試 | 確保不破壞現有功能 | ✅ |
| 5. 更新 Changelog | 記錄修復內容 | 視情況 |

### 3.3 重構

| 步驟 | 說明 | 必要 |
|------|------|------|
| 1. 確認測試覆蓋 | 重構前確保有足夠測試 | ✅ |
| 2. 小步重構 | 每次只改一小部分 | ✅ |
| 3. 頻繁執行測試 | 每次修改後執行測試 | ✅ |
| 4. 保持功能不變 | 重構不改變外部行為 | ✅ |
| 5. 更新文件 | 如有架構變更 | 視情況 |

---

## 4. 程式碼品質要求

### 4.1 Type Hints

```python
# ✅ 正確
def calculate_factor(data: pd.DataFrame, period: int = 14) -> pd.Series:
    pass

# ❌ 錯誤
def calculate_factor(data, period=14):
    pass
```

### 4.2 Docstrings

公開介面（public functions, classes）必須有 docstring：

```python
def calculate_factor(data: pd.DataFrame, period: int = 14) -> pd.Series:
    """
    計算技術指標因子。
    
    Args:
        data: 包含 'close' 欄位的價格資料
        period: 計算週期，預設 14
        
    Returns:
        因子值序列
        
    Raises:
        ValueError: 當資料不足時
        
    Example:
        >>> result = calculate_factor(price_data, period=20)
    """
    pass
```

### 4.3 Logging

```python
import logging

logger = logging.getLogger(__name__)

def process_data(data: pd.DataFrame) -> pd.DataFrame:
    logger.info(f"Processing {len(data)} rows")
    
    try:
        result = transform(data)
        logger.debug(f"Transform completed: {result.shape}")
        return result
    except Exception as e:
        logger.error(f"Transform failed: {e}")
        raise
```

### 4.4 錯誤處理

```python
# ✅ 正確：明確的錯誤處理
def fetch_data(symbol: str) -> pd.DataFrame:
    if not symbol:
        raise ValueError("Symbol cannot be empty")
    
    try:
        data = api.get(symbol)
    except ConnectionError as e:
        logger.error(f"API connection failed: {e}")
        raise
    except TimeoutError as e:
        logger.warning(f"API timeout, retrying: {e}")
        data = api.get(symbol, timeout=60)
    
    if data.empty:
        raise ValueError(f"No data found for {symbol}")
    
    return data

# ❌ 錯誤：吞掉例外
def fetch_data(symbol: str) -> pd.DataFrame:
    try:
        return api.get(symbol)
    except:
        return pd.DataFrame()  # 隱藏錯誤
```

---

## 5. AI Agent 實作指引

### 5.1 Cloud Agent vs Local Agent

| 情境 | 建議使用 | 原因 |
|------|----------|------|
| 初版開發（需大量思考） | Cloud Agent | 較強的推理能力 |
| 簡單修改、Bug 修復 | Local Agent | 快速回應 |
| 需要多檔案協作 | Cloud Agent | 較好的上下文理解 |
| 需要執行測試驗證 | Local Agent | 可直接執行 |
| 需要遵循複雜規範 | Cloud Agent | 較好的指令遵循 |

### 5.2 AI Agent 必讀標準

實作前，AI Agent 必須閱讀：

| 實作類型 | 必讀標準 |
|----------|----------|
| 初版開發 | architecture-standard.md, testing-standard.md, product_spec.md |
| 功能新增 | 現有程式碼, testing-standard.md |
| Bug 修復 | 現有程式碼, 相關測試 |
| 重構 | architecture-standard.md, 現有測試 |

### 5.3 實作完成後

AI Agent 實作完成後，應主動：

1. **執行測試**：`pytest -v`
2. **報告結果**：告知測試通過/失敗狀況
3. **列出交付物**：說明產生了哪些檔案
4. **提示下一步**：建議進行架構審查或測試驗證

---

## 6. 禁止事項

- **禁止**：只產生程式碼不產生測試
- **禁止**：跳過測試直接提交 PR
- **禁止**：吞掉例外不處理
- **禁止**：使用 `from module import *`
- **禁止**：在程式碼中 hardcode 敏感資訊
- **禁止**：不讀現有程式碼就直接修改
- **禁止**：重構時改變外部行為

---

## 7. 完整開發流程圖

```
┌─────────────────────────────────────────────────────────────┐
│ Phase 1: 需求 (issue-standard.md)                           │
│ └── Issue 撰寫 → 明確的需求描述                             │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ Phase 2: 實作 (implementation-standard.md) ← 本文件         │
│ ├── 閱讀標準與需求                                          │
│ ├── 建立目錄結構 (architecture-standard.md)                │
│ ├── 實作程式碼                                              │
│ ├── 同步撰寫測試 (testing-standard.md)                     │
│ └── 執行測試確認通過                                        │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ Phase 3: 審查 (pr-review-standard.md)                       │
│ ├── 初版架構審查 (Section 1)                               │
│ └── 測試驗證 (Section 3)                                   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ Phase 4: 文件                                               │
│ ├── README.md (readme-standard.md)                         │
│ └── copilot-instructions.md (copilot-instructions-standard)│
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ Phase 5: 提交 PR                                            │
└─────────────────────────────────────────────────────────────┘
```

---

## Changelog

- 1.0 — 2025-12-25: 初版建立，從 issue-standard.md 獨立出實作相關規範
