# QadrisCorp — Architecture Standard

Version: 1.0  
Last Updated: 2025-12-25  
Scope: 專案架構設計與目錄結構的標準規範

---

## 1. 概述

本標準定義 QadrisCorp 專案的架構設計原則與目錄結構規範，確保各專案具備一致性、可維護性與可擴展性。

---

## 2. 目錄結構標準

### 2.1 Python Package 專案

適用於：可被其他專案 import 的套件

```
{project_name}/
├── .github/                    # GitHub 與 Copilot 設定
│   ├── copilot-instructions.md
│   ├── qadris_governance/
│   ├── qadris_standards/
│   └── qadris_templates/
├── .vscode/                    # VS Code 設定
├── src/                        # 原始碼（推薦使用 src layout）
│   └── {package_name}/
│       ├── __init__.py
│       ├── core/               # 核心邏輯
│       ├── models/             # 資料模型
│       ├── utils/              # 工具函數
│       └── exceptions.py       # 自定義例外
├── tests/                      # 測試程式碼
│   ├── __init__.py
│   ├── conftest.py
│   └── test_*.py
├── doc/                        # 文件目錄
│   └── product_spec.md
├── .env.example                # 環境變數範本
├── .gitignore
├── pyproject.toml              # 專案設定（推薦）
├── requirements.txt            # 依賴套件
└── README.md
```

### 2.2 API Service 專案

適用於：提供 REST API 或 gRPC 服務的專案

```
{project_name}/
├── .github/
├── .vscode/
├── app/                        # 應用程式主目錄
│   ├── __init__.py
│   ├── main.py                 # 進入點
│   ├── api/                    # API 路由
│   │   ├── __init__.py
│   │   ├── routes/
│   │   └── dependencies.py
│   ├── core/                   # 核心邏輯
│   │   ├── __init__.py
│   │   └── config.py
│   ├── models/                 # 資料模型
│   │   ├── __init__.py
│   │   ├── schemas.py          # Pydantic schemas
│   │   └── database.py         # ORM models
│   ├── services/               # 業務邏輯層
│   └── utils/
├── tests/
├── doc/
├── .env.example
├── requirements.txt
└── README.md
```

### 2.3 CLI Tool 專案

適用於：命令列工具

```
{project_name}/
├── .github/
├── .vscode/
├── src/
│   └── {tool_name}/
│       ├── __init__.py
│       ├── cli.py              # CLI 進入點
│       ├── commands/           # 子命令
│       ├── core/               # 核心邏輯
│       └── utils/
├── tests/
├── doc/
├── .env.example
├── requirements.txt
└── README.md
```

### 2.4 Data Pipeline 專案

適用於：資料處理、ETL 專案

```
{project_name}/
├── .github/
├── .vscode/
├── src/
│   └── {pipeline_name}/
│       ├── __init__.py
│       ├── extractors/         # 資料擷取
│       ├── transformers/       # 資料轉換
│       ├── loaders/            # 資料載入
│       ├── models/             # 資料模型
│       └── utils/
├── tests/
├── doc/
├── config/                     # 設定檔目錄
│   ├── config.yaml
│   └── logging.yaml
├── data/                       # 本地資料（應在 .gitignore）
│   ├── raw/
│   ├── processed/
│   └── output/
├── .env.example
├── requirements.txt
└── README.md
```

---

## 3. 分層架構原則

### 3.1 標準分層

```
┌─────────────────────────────────────┐
│           API / CLI Layer           │  ← 對外介面
├─────────────────────────────────────┤
│          Service Layer              │  ← 業務邏輯
├─────────────────────────────────────┤
│           Core Layer                │  ← 核心功能
├─────────────────────────────────────┤
│          Models Layer               │  ← 資料模型
├─────────────────────────────────────┤
│          Utils / Common             │  ← 共用工具
└─────────────────────────────────────┘
```

### 3.2 相依性規則

| 層級 | 可依賴 | 不可依賴 |
|------|--------|----------|
| API/CLI | Service, Core, Models, Utils | — |
| Service | Core, Models, Utils | API/CLI |
| Core | Models, Utils | API/CLI, Service |
| Models | Utils | API/CLI, Service, Core |
| Utils | — | 所有其他層 |

### 3.3 層級職責

| 層級 | 職責 | 範例 |
|------|------|------|
| **API/CLI** | 接收請求、參數驗證、回應格式化 | FastAPI routes, Click commands |
| **Service** | 業務邏輯、流程編排 | 交易處理、報表產生 |
| **Core** | 核心演算法、領域邏輯 | 因子計算、策略執行 |
| **Models** | 資料結構定義 | Pydantic, SQLAlchemy models |
| **Utils** | 通用工具函數 | 日期處理、檔案操作 |

---

## 4. 命名規範

### 4.1 目錄與檔案命名

| 類型 | 規範 | 範例 |
|------|------|------|
| 目錄名 | snake_case | `data_loader/`, `factor_base/` |
| Python 檔案 | snake_case | `data_retriever.py`, `base_factor.py` |
| 測試檔案 | test_ 前綴 | `test_data_retriever.py` |
| 設定檔 | 依類型 | `config.yaml`, `.env.example` |

### 4.2 Python 命名

| 類型 | 規範 | 範例 |
|------|------|------|
| 模組 | snake_case | `data_retriever` |
| 類別 | PascalCase | `DataRetriever`, `BaseFactor` |
| 函數/方法 | snake_case | `get_data()`, `calculate_factor()` |
| 常數 | UPPER_SNAKE_CASE | `DEFAULT_TIMEOUT`, `MAX_RETRIES` |
| 變數 | snake_case | `factor_value`, `start_date` |
| 私有成員 | _前綴 | `_internal_cache`, `_validate()` |

### 4.3 特殊檔案命名

| 檔案 | 用途 |
|------|------|
| `__init__.py` | 模組初始化、公開介面定義 |
| `__main__.py` | 模組可執行進入點 |
| `conftest.py` | pytest fixtures |
| `exceptions.py` | 自定義例外類別 |
| `constants.py` | 常數定義 |
| `types.py` | 型別定義（TypedDict, Protocol 等） |

---

## 5. Config 管理

### 5.1 設定來源優先順序

```
1. 環境變數（最高優先）
2. .env 檔案
3. config.yaml / config.py
4. 程式碼預設值（最低優先）
```

### 5.2 設定檔組織

| 設定類型 | 建議方式 | 範例 |
|----------|----------|------|
| 敏感資訊 | 環境變數 + .env | API keys, passwords |
| 部署設定 | 環境變數 | 環境名稱、服務 URL |
| 應用設定 | config.yaml | 功能開關、業務參數 |
| 程式設定 | config.py | 常數、預設值 |

### 5.3 設定檔範例

```python
# config.py
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    # 環境
    ENV = os.getenv("ENV", "development")
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    
    # 路徑
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    
    # 資料庫
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///local.db")
    
    # 外部服務
    API_KEY = os.getenv("API_KEY")  # 必填，無預設值
    API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))
```

---

## 6. 模組設計原則

### 6.1 單一職責原則

每個模組應只負責一個明確的功能領域。

```python
# ✅ 正確：職責明確
# data_retriever.py - 只負責資料擷取
# data_transformer.py - 只負責資料轉換
# data_loader.py - 只負責資料載入

# ❌ 錯誤：職責混雜
# data_handler.py - 同時處理擷取、轉換、載入
```

### 6.2 介面設計

```python
# 使用抽象基底類別定義介面
from abc import ABC, abstractmethod

class DataSource(ABC):
    """資料來源的抽象介面"""
    
    @abstractmethod
    def fetch(self, query: str) -> pd.DataFrame:
        """擷取資料"""
        pass
    
    @abstractmethod
    def validate(self, data: pd.DataFrame) -> bool:
        """驗證資料"""
        pass
```

### 6.3 依賴注入

```python
# ✅ 正確：透過參數注入依賴
class FactorCalculator:
    def __init__(self, data_source: DataSource):
        self._data_source = data_source

# ❌ 錯誤：直接實例化依賴
class FactorCalculator:
    def __init__(self):
        self._data_source = PostgresDataSource()  # 緊耦合
```

---

## 7. 禁止事項

- **禁止**：在 utils/ 放置業務邏輯
- **禁止**：循環依賴（A import B, B import A）
- **禁止**：跨層直接存取（API 直接存取 Models，跳過 Service）
- **禁止**：在模組內 hardcode 設定值
- **禁止**：使用 `from module import *`
- **禁止**：在 `__init__.py` 放置大量邏輯

---

## 8. 檢查清單

建立新專案時，確認以下項目：

- [ ] 選擇適合的專案類型模板
- [ ] 目錄結構符合標準
- [ ] 命名規範一致
- [ ] 分層架構清楚
- [ ] 設定管理方式確定
- [ ] 無循環依賴
- [ ] 進入點明確（main.py / run.py / cli.py）

---

## Changelog

- 1.0 — 2025-12-25: 初版建立
