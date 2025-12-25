# QadrisCorp — Internal Repositories

Version: 1.0  
Last Updated: 2025-12-25  
Scope: 公司內部可用的 Repositories 與工具

---

## 1. 資料擷取類

### 1.1 DataRetriever

| 項目 | 說明 |
|------|------|
| **Repo** | QadrisCorp/DataRetriever |
| **用途** | 通用資料擷取框架，提供基底類別供繼承 |
| **維護團隊** | Data Team |
| **狀態** | ✅ 穩定 |
| **Python 版本** | 3.9+ |

**安裝方式**：
```bash
pip install git+ssh://git@github.com/QadrisCorp/DataRetriever.git
```

**使用範例**：
```python
from data_retriever import DataRetriever

class MyRetriever(DataRetriever):
    def fetch(self, query: str) -> pd.DataFrame:
        # 實作資料擷取邏輯
        pass
```

**主要類別**：
- `DataRetriever`: 基底類別
- `CachedRetriever`: 帶快取的擷取器
- `BatchRetriever`: 批次擷取器

---

### 1.2 MeasureRetriever

| 項目 | 說明 |
|------|------|
| **Repo** | QadrisCorp/MeasureRetriever |
| **用途** | 財務指標資料擷取，繼承自 DataRetriever |
| **維護團隊** | Data Team |
| **狀態** | ✅ 穩定 |
| **相依** | DataRetriever |

**安裝方式**：
```bash
pip install git+ssh://git@github.com/QadrisCorp/MeasureRetriever.git
```

**使用範例**：
```python
from measure_retriever import MeasureRetriever

mr = MeasureRetriever()

# 取得單一指標
roe_data = mr.get_measure("ROE", start_date="2024-01-01", end_date="2024-12-31")

# 取得多個指標
measures = mr.get_measures(["ROE", "ROA", "EPS"], stock_ids=["2330", "2317"])
```

**可用指標**：
| 指標代碼 | 說明 | 頻率 |
|----------|------|------|
| ROE | 股東權益報酬率 | 季 |
| ROA | 資產報酬率 | 季 |
| EPS | 每股盈餘 | 季 |
| PE | 本益比 | 日 |
| PB | 股價淨值比 | 日 |
| {更多指標} | {請參考完整文件} | — |

---

### 1.3 QadrisWebAPI

| 項目 | 說明 |
|------|------|
| **Repo** | QadrisCorp/QadrisWebAPI |
| **用途** | 公司內部 REST API 服務 |
| **維護團隊** | Application Team |
| **狀態** | ✅ 穩定 |
| **Base URL** | `http://api.qadris.internal` (需 VPN) |

**認證方式**：
```python
import requests

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}
```

**主要端點**：
| 端點 | 方法 | 用途 |
|------|------|------|
| `/api/v1/stocks` | GET | 取得股票列表 |
| `/api/v1/stocks/{stock_id}` | GET | 取得單一股票資訊 |
| `/api/v1/prices` | GET | 取得價格資料 |
| `/api/v1/measures/{measure_id}` | GET | 取得指標資料 |

**Python Client**：
```python
from qadris_api import QadrisClient

client = QadrisClient(api_token="your_token")
stocks = client.get_stocks(market="TW")
prices = client.get_prices(stock_id="2330", start_date="2024-01-01")
```

---

## 2. 因子庫類

### 2.1 QadrisFactorBase

| 項目 | 說明 |
|------|------|
| **Repo** | QadrisCorp/QadrisFactorBase |
| **用途** | 因子定義與計算框架 |
| **維護團隊** | Research Team |
| **狀態** | 🚧 開發中 |
| **相依** | DataRetriever, MeasureRetriever |

**使用範例**：
```python
from qadris_factor_base import BaseFactor, FactorRegistry

class MomentumFactor(BaseFactor):
    def calculate(self, data: pd.DataFrame) -> pd.Series:
        return data['close'].pct_change(periods=20)

# 註冊因子
FactorRegistry.register(MomentumFactor)
```

---

## 3. 工具類

### 3.1 {QadrisUtils}

| 項目 | 說明 |
|------|------|
| **Repo** | {QadrisCorp/QadrisUtils} |
| **用途** | {公司通用工具函數} |
| **維護團隊** | {Application Team} |
| **狀態** | {✅ 穩定} |

**主要功能**：
- 日期處理工具
- 資料驗證工具
- 日誌設定工具

---

## 4. 使用建議

### 4.1 選擇指南

| 需求 | 建議使用 |
|------|----------|
| 擷取財務指標 | MeasureRetriever |
| 擷取價格資料 | QadrisWebAPI |
| 自定義資料擷取 | 繼承 DataRetriever |
| 因子計算 | QadrisFactorBase |
| 一般工具函數 | QadrisUtils |

### 4.2 相依關係圖

```
QadrisFactorBase
    │
    ├── MeasureRetriever
    │       │
    │       └── DataRetriever
    │
    └── QadrisWebAPI (API 呼叫)
```

---

## 5. 權限與存取

| Repo | 存取等級 | 申請方式 |
|------|----------|----------|
| DataRetriever | 全公司可讀 | — |
| MeasureRetriever | 全公司可讀 | — |
| QadrisWebAPI | 需申請 | Infrastructure Team |
| QadrisFactorBase | Research + Data Team | 跨部門申請 |

---

## Changelog

- 1.0 — 2025-12-25: 初版建立
