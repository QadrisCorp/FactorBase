# QadrisCorp — Issue Standard

Version: 1.2  
Last Updated: 2025-12-25  
Scope: GitHub Issue 撰寫與管理的標準規範

---

## 1. 概述

本標準定義如何撰寫讓人類與 AI Agent 都能理解的 GitHub Issues，確保需求清楚、可追蹤、可實作。

---

## 2. Issue 類型

### 2.1 類型定義

| 類型 | Label | 用途 | 範例 |
|------|-------|------|------|
| **Epic** | `epic` | 大型功能，需拆分成多個 Feature | 「建立因子庫系統」 |
| **Feature** | `feature` | 新功能需求 | 「新增 RSI 因子計算」 |
| **Bug** | `bug` | 錯誤修復 | 「因子計算結果異常」 |
| **Task** | `task` | 技術任務（非功能性） | 「升級 pandas 版本」 |
| **Documentation** | `documentation` | 文件更新 | 「更新 API 文件」 |
| **Refactor** | `refactor` | 重構（不改變功能） | 「重構資料擷取模組」 |

### 2.2 優先級 Labels

| Label | 說明 |
|-------|------|
| `priority: critical` | 阻塞性問題，需立即處理 |
| `priority: high` | 重要功能，本週內處理 |
| `priority: medium` | 一般功能，本月內處理 |
| `priority: low` | 可延後處理 |

### 2.3 狀態 Labels

| Label | 說明 |
|-------|------|
| `status: ready` | 需求明確，可開始實作 |
| `status: in-progress` | 正在實作中 |
| `status: blocked` | 被其他 Issue 阻塞 |
| `status: review` | 等待 Review |

---

## 3. Issue 內容規範

### 3.1 Feature Issue 模板

```markdown
## 📋 功能描述

簡潔描述要實作的功能。

## 🎯 目標

- [ ] 目標 1
- [ ] 目標 2

## 📖 使用者故事

作為 {角色}，我希望 {功能}，以便 {價值}。

## 📐 技術規格

### 輸入
- 參數 1：型別、說明
- 參數 2：型別、說明

### 輸出
- 回傳值：型別、說明

### 範例
```python
# 使用範例
result = function_name(param1, param2)
```

## ✅ 驗收條件

- [ ] 條件 1
- [ ] 條件 2
- [ ] 單元測試通過
- [ ] 文件更新

## 🔗 相關資源

- product_spec.md: {章節連結}
- 相依 Issue: #{issue_number}

## 📝 備註

其他需要注意的事項。
```

### 3.2 Bug Issue 模板

```markdown
## 🐛 問題描述

簡潔描述遇到的問題。

## 🔄 重現步驟

1. 步驟 1
2. 步驟 2
3. 步驟 3

## ✅ 預期行為

描述正確的行為應該是什麼。

## ❌ 實際行為

描述目前錯誤的行為。

## 📋 環境資訊

- Python 版本：
- 作業系統：
- 相關套件版本：

## 📎 錯誤訊息 / Log

```
貼上錯誤訊息或相關 log
```

## 🔗 相關資源

- 相關程式碼：{檔案路徑}#L{行號}
- 相依 Issue: #{issue_number}
```

### 3.3 Task Issue 模板

```markdown
## 📋 任務描述

簡潔描述要執行的任務。

## 🎯 目標

- [ ] 目標 1
- [ ] 目標 2

## 📝 執行步驟

1. 步驟 1
2. 步驟 2
3. 步驟 3

## ✅ 完成條件

- [ ] 條件 1
- [ ] 條件 2

## 🔗 相關資源

- 相依 Issue: #{issue_number}
```

---

## 4. AI Agent 友善撰寫指引

### 4.1 讓 AI 能理解的關鍵要素

| 要素 | 說明 | 範例 |
|------|------|------|
| **明確的輸入輸出** | 清楚定義函數簽名 | `def calculate(data: pd.DataFrame) -> float` |
| **具體的驗收條件** | 可驗證的條件 | 「回傳值需介於 0-100 之間」 |
| **技術約束** | 使用的框架、版本 | 「使用 pandas 2.x」 |
| **參考程式碼** | 現有相關程式碼位置 | 「參考 `src/factors/base.py`」 |
| **測試案例** | 預期的測試情境 | 「輸入 [1,2,3]，預期輸出 2.0」 |

### 4.2 ⚠️ 避免的寫法

| ❌ 避免 | ✅ 改為 |
|---------|---------|
| 「做一個好用的功能」 | 「實作 RSI 因子計算，輸入 DataFrame，輸出 0-100 的數值」 |
| 「修好那個 bug」 | 「修復 `calculate_factor()` 在空資料時拋出的 KeyError」 |
| 「優化效能」 | 「將 `process_data()` 的執行時間從 10 秒降至 2 秒以內」 |
| 「參考之前的做法」 | 「參考 `src/factors/momentum.py` 的實作方式」 |

### 4.3 AI Agent 實作指引區塊

在 Issue 中可加入此區塊，給 AI Agent 明確指示：

```markdown
## 🤖 AI Agent 實作指引

### 實作順序
1. 先閱讀 `src/factors/base.py` 了解基底類別
2. 在 `src/factors/` 下建立新檔案
3. 繼承 `BaseFactor` 類別
4. 實作 `calculate()` 方法
5. 在 `tests/` 下建立對應測試

### 程式碼風格
- 遵循現有程式碼風格
- 使用 type hints
- 加入 docstring

### 禁止事項
- 不要修改 `BaseFactor` 基底類別
- 不要新增額外的依賴套件

### 測試要求
- 正常案例測試
- 邊界條件測試（空資料、單一資料點）
- 例外處理測試
```

---

## 5. 從 Product Spec 拆分 Issues

### 5.1 拆分原則

```
product_spec.md
    │
    ├── 功能需求 3.1 → Epic Issue
    │       ├── 子功能 3.1.1 → Feature Issue
    │       ├── 子功能 3.1.2 → Feature Issue
    │       └── 子功能 3.1.3 → Feature Issue
    │
    ├── 功能需求 3.2 → Epic Issue
    │       └── ...
    │
    └── 技術架構 4.x → Task Issues (setup)
```

### 5.2 拆分粒度指引

| Issue 大小 | 建議工時 | 說明 |
|------------|----------|------|
| 太大 | > 8 小時 | 應拆分成多個 Issues |
| 適中 | 2-8 小時 | 理想大小 |
| 太小 | < 1 小時 | 可合併或直接處理 |

### 5.3 Issue 關聯

```markdown
## 🔗 Issue 關聯

- **Epic**: #10 建立因子庫系統
- **Blocks**: #12 因子回測功能（需先完成本 Issue）
- **Blocked by**: #8 資料擷取模組（需等待完成）
- **Related**: #15 效能優化
```

---

## 6. AI Agent 友善的 Issue 撰寫

> 💡 實作流程請參考 `implementation-standard.md`

### 6.1 給 AI Agent 的 Issue 範例

```markdown
---
title: 實作 RSI 技術指標因子
labels: feature, priority: high, status: ready
assignees: copilot
---

## 📋 功能描述

實作 RSI (Relative Strength Index) 技術指標因子，繼承 `BaseFactor` 類別。

## 🎯 目標

- [ ] 建立 `RSIFactor` 類別
- [ ] 實作 `calculate()` 方法
- [ ] 支援可配置的計算週期

## 📐 技術規格

### 類別定義
```python
class RSIFactor(BaseFactor):
    def __init__(self, period: int = 14):
        """
        Args:
            period: RSI 計算週期，預設 14
        """
        pass
    
    def calculate(self, data: pd.DataFrame) -> pd.Series:
        """
        計算 RSI 值
        
        Args:
            data: 包含 'close' 欄位的 DataFrame
            
        Returns:
            RSI 值序列，範圍 0-100
        """
        pass
```

### RSI 計算公式
```
RSI = 100 - (100 / (1 + RS))
RS = 平均漲幅 / 平均跌幅
```

## ✅ 驗收條件

- [ ] `RSIFactor` 類別繼承 `BaseFactor`
- [ ] RSI 值範圍在 0-100 之間
- [ ] 支援 period 參數配置
- [ ] 處理資料不足的情況（回傳 NaN）
- [ ] 單元測試覆蓋率 > 80%
- [ ] 通過 `pytest tests/test_rsi_factor.py`

## 🤖 AI Agent 實作指引

> 詳細實作流程請參考 `implementation-standard.md`

### 實作順序
1. 閱讀 `src/factors/base.py` 了解 `BaseFactor` 介面
2. 在 `src/factors/technical/` 建立 `rsi.py`
3. 實作 `RSIFactor` 類別
4. 在 `tests/factors/` 建立 `test_rsi_factor.py`
5. 執行測試確認通過

### 參考資源
- 基底類別：`src/factors/base.py`
- 類似實作：`src/factors/technical/momentum.py`
- 測試範例：`tests/factors/test_momentum_factor.py`

### 禁止事項
- 不要使用 ta-lib 套件（改用 pandas 實作）
- 不要修改 `BaseFactor` 基底類別
```

---

## 7. Issue 管理流程

### 7.1 生命週期

```
建立 → 標記 Ready → 指派 → In Progress → Review → 關閉
  │                                           │
  └─── Blocked ←──────────────────────────────┘
```

### 7.2 關閉 Issue 的條件

- [ ] 所有驗收條件已達成
- [ ] 相關測試通過
- [ ] PR 已合併
- [ ] 文件已更新（如適用）

---

## 8. 禁止事項

- **禁止**：Issue 標題過於模糊（如「修 bug」、「新功能」）
- **禁止**：缺少驗收條件
- **禁止**：單一 Issue 包含多個不相關的功能
- **禁止**：缺少足夠的技術細節讓實作者理解
- **禁止**：Issue 之間有循環依賴

---

## Changelog

- 1.2 — 2025-12-25: 將實作相關內容移至 `implementation-standard.md`，本文件專注於 Issue 撰寫
- 1.1 — 2025-12-25: 新增「初版交付物定義」
- 1.0 — 2025-12-25: 初版建立
