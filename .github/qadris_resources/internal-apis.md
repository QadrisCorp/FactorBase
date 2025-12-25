# QadrisCorp — Internal APIs

Version: 1.0  
Last Updated: 2025-12-25  
Scope: 公司內部 API 服務資訊

---

## 1. QadrisWebAPI

### 1.1 基本資訊

| 項目 | 說明 |
|------|------|
| **Base URL** | `http://api.qadris.internal` |
| **版本** | v1 |
| **認證** | Bearer Token |
| **回應格式** | JSON |
| **需求** | VPN 連線 |

### 1.2 認證方式

```python
import requests

# 方式 1: Header
headers = {
    "Authorization": "Bearer {your_api_token}",
    "Content-Type": "application/json"
}

response = requests.get(
    "http://api.qadris.internal/api/v1/stocks",
    headers=headers
)

# 方式 2: 使用 Python Client
from qadris_api import QadrisClient

client = QadrisClient(api_token=os.getenv("QADRIS_API_TOKEN"))
```

### 1.3 端點列表

#### 股票相關

| 端點 | 方法 | 說明 | 參數 |
|------|------|------|------|
| `/api/v1/stocks` | GET | 取得股票列表 | market, sector, limit |
| `/api/v1/stocks/{stock_id}` | GET | 取得單一股票資訊 | — |
| `/api/v1/stocks/{stock_id}/profile` | GET | 取得公司基本資料 | — |

**範例**：
```python
# 取得台股列表
response = client.get("/api/v1/stocks", params={"market": "TW", "limit": 100})

# 回應格式
{
    "status": "success",
    "data": [
        {"stock_id": "2330", "name": "台積電", "market": "TW"},
        {"stock_id": "2317", "name": "鴻海", "market": "TW"}
    ],
    "total": 1000,
    "page": 1
}
```

#### 價格相關

| 端點 | 方法 | 說明 | 參數 |
|------|------|------|------|
| `/api/v1/prices` | GET | 取得價格資料 | stock_id, start_date, end_date |
| `/api/v1/prices/latest` | GET | 取得最新價格 | stock_ids |

**範例**：
```python
# 取得歷史價格
response = client.get("/api/v1/prices", params={
    "stock_id": "2330",
    "start_date": "2024-01-01",
    "end_date": "2024-12-31"
})

# 回應格式
{
    "status": "success",
    "data": [
        {"date": "2024-01-02", "open": 580, "high": 585, "low": 578, "close": 583, "volume": 10000},
        ...
    ]
}
```

#### 指標相關

| 端點 | 方法 | 說明 | 參數 |
|------|------|------|------|
| `/api/v1/measures` | GET | 取得可用指標列表 | category |
| `/api/v1/measures/{measure_id}` | GET | 取得指標資料 | stock_ids, start_date, end_date |

**範例**：
```python
# 取得 ROE 資料
response = client.get("/api/v1/measures/ROE", params={
    "stock_ids": "2330,2317",
    "start_date": "2024-01-01"
})
```

### 1.4 錯誤處理

| HTTP 狀態碼 | 說明 | 處理方式 |
|-------------|------|----------|
| 200 | 成功 | — |
| 400 | 參數錯誤 | 檢查請求參數 |
| 401 | 未授權 | 檢查 API Token |
| 403 | 禁止存取 | 確認權限 |
| 404 | 資源不存在 | 確認資源 ID |
| 429 | 請求過多 | 降低請求頻率 |
| 500 | 伺服器錯誤 | 聯繫 App Team |

**錯誤回應格式**：
```json
{
    "status": "error",
    "error": {
        "code": "INVALID_PARAMETER",
        "message": "Invalid date format",
        "details": {"field": "start_date", "expected": "YYYY-MM-DD"}
    }
}
```

### 1.5 Rate Limiting

| 等級 | 限制 | 備註 |
|------|------|------|
| 標準 | 100 requests/min | 一般使用 |
| 進階 | 500 requests/min | 需申請 |

---

## 2. {其他內部 API}

### 2.1 {DataService API}

| 項目 | 說明 |
|------|------|
| **Base URL** | `{http://data.qadris.internal}` |
| **用途** | {大量資料批次處理}|
| **維護團隊** | {Data Team} |

---

## 3. API Token 取得

### 3.1 申請流程

1. 在 QadrisCorp/infrastructure-requests 開 Issue
2. 說明用途與預計使用量
3. Infrastructure Team 審核後發放

### 3.2 Token 使用

```bash
# 環境變數設定
export QADRIS_API_TOKEN="your_token_here"
```

```python
# Python 使用
import os
api_token = os.getenv("QADRIS_API_TOKEN")
```

---

## 4. 使用最佳實踐

### 4.1 錯誤重試

```python
import time
from requests.exceptions import RequestException

def api_call_with_retry(client, endpoint, params, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = client.get(endpoint, params=params)
            return response
        except RequestException as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # 指數退避
            else:
                raise
```

### 4.2 批次請求

```python
# 避免：逐一請求
for stock_id in stock_ids:
    data = client.get(f"/api/v1/prices", params={"stock_id": stock_id})

# 建議：批次請求
data = client.get("/api/v1/prices", params={"stock_ids": ",".join(stock_ids)})
```

---

## Changelog

- 1.0 — 2025-12-25: 初版建立
