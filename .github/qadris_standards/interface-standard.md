# QadrisCorp — Interface Standard

Version: 1.0  
Last Updated: 2025-12-26  
Scope: 對外介面（CLI、API、SDK）架構與實作規範

---

## 1. 概述

本標準定義 QadrisCorp 專案中各類對外介面的架構、命名規範與實作流程，包含：

- **CLI（Command Line Interface）**：命令列介面
- **API（Application Programming Interface）**：REST API 服務
- **SDK（Software Development Kit）**：程式化整合介面

### 1.1 共通原則

| 原則 | 說明 |
|------|------|
| 一致性 | 同類介面採用相同的設計模式與命名風格 |
| 自文件化 | 介面本身即文件（help、OpenAPI spec） |
| 版本化 | API/SDK 需有版本管理機制 |
| 錯誤處理 | 統一的錯誤回應格式與狀態碼 |
| 可測試性 | 所有介面需可自動化測試 |

---

# Part A: CLI Standard（命令列介面）

## 2. CLI 技術選型

| 項目 | 選擇 | 說明 |
|------|------|------|
| CLI 框架 | [Typer](https://typer.tiangolo.com/) | 基於 type hints 的現代 CLI 框架 |
| 輸出美化 | [Rich](https://rich.readthedocs.io/) | 終端輸出格式化、表格、進度條 |
| 進入點 | `pyproject.toml` `[project.scripts]` | 標準 Python 打包方式 |

---

## 3. CLI 目錄結構

### 3.1 標準結構

```
{package}/
└── cli/
    ├── __init__.py        # 模組匯出
    ├── app.py             # Typer app 初始化
    ├── main.py            # CLI 進入點、命令註冊
    └── commands/          # 命令模組目錄
        ├── __init__.py    # 命令匯出
        ├── {command1}.py  # 命令群組 1
        ├── {command2}.py  # 命令群組 2
        └── ...
```

### 3.2 檔案職責

| 檔案 | 職責 |
|------|------|
| `cli/__init__.py` | 匯出 `app` 與 `main`，供外部使用 |
| `cli/app.py` | 建立 Typer app 實例、Rich console、共用工具函數 |
| `cli/main.py` | CLI 進入點，匯入並註冊所有命令 |
| `cli/commands/*.py` | 按功能分類的命令實作 |

### 3.3 命令分組原則

| 分組類型 | 說明 | 範例 |
|----------|------|------|
| 狀態查詢類 | 查看系統/資料狀態的唯讀命令 | `status`、`info`、`health` |
| 資料操作類 | 匯入、匯出、同步等資料變更命令 | `import`、`export`、`sync` |
| 報告產出類 | 產生報告、摘要的命令 | `report`、`summary` |
| 設定管理類 | 查看或修改設定的命令 | `config-show`、`config-set` |
| 清單列舉類 | 列出資源清單的命令 | `list-*`、`show-*` |

> **原則**：相關功能放同一檔案，單一檔案不超過 5 個命令。命令過多時應拆分。

---

## 4. CLI 實作規範

### 4.1 app.py 範本

```python
"""
Typer app 初始化

建立並設定 Typer 應用程式實例
"""

import sys

try:
    import typer
    from rich.console import Console
    HAS_TYPER = True
except ImportError:
    HAS_TYPER = False


def check_typer():
    """檢查 typer 是否已安裝"""
    if not HAS_TYPER:
        print("錯誤: 請先安裝 typer 和 rich 套件")
        print("執行: pip install typer rich")
        sys.exit(1)


# 建立 Typer app 實例
if HAS_TYPER:
    app = typer.Typer(
        name="{app_name}",
        help="{app_description}",
        add_completion=False
    )
    console = Console()
else:
    app = None
    console = None
```

### 4.2 main.py 範本

```python
"""
命令列介面主程式
"""

import logging

from .app import app, check_typer

# 匯入命令以註冊到 app
from .commands import (
    command1,
    command2,
    # ...
)

# 設定 logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """CLI 進入點"""
    check_typer()
    app()


if __name__ == "__main__":
    main()
```

### 4.3 命令檔案範本

```python
"""
{命令群組描述}
"""

import typer
from rich.table import Table

from ..app import app, console, check_typer
from ...config.settings import Settings
from ...services.some_service import SomeService


@app.command()
def my_command(
    option1: bool = typer.Option(False, "--option1", "-o", help="選項說明"),
    argument1: str = typer.Argument(..., help="參數說明"),
):
    """命令說明（顯示於 --help）"""
    check_typer()
    
    try:
        # 業務邏輯
        settings = Settings()
        service = SomeService(settings)
        result = service.do_something()
        
        # 輸出結果
        console.print(f"[green]成功！[/green]")
        
    except Exception as e:
        console.print(f"[red]錯誤: {e}[/red]")
        raise typer.Exit(1)
```

---

## 5. CLI 命名規範

### 5.1 命令命名

| 規則 | 範例 | 說明 |
|------|------|------|
| 動詞開頭 | `import-all`、`list-tickers` | 表達動作 |
| kebab-case | `config-show` | Typer 自動轉換 |
| 簡潔明確 | `status` 而非 `show-current-status` | 避免冗長 |

### 5.2 選項命名

| 類型 | 長選項 | 短選項 | 範例 |
|------|--------|--------|------|
| 布林開關 | `--flag/--no-flag` | `-f` | `--verbose/--no-verbose` |
| 單一值 | `--option` | `-o` | `--output`, `-o` |
| 多重值 | `--items` | `-i` | `--ticker`, `-t`（可重複） |

### 5.3 常用短選項保留

| 短選項 | 保留用途 |
|--------|----------|
| `-h` | `--help`（Typer 預設） |
| `-v` | `--verbose` 或 `--version` |
| `-f` | `--full` 或 `--force` |
| `-o` | `--output` |
| `-q` | `--quiet` |

---

## 6. CLI 輸出規範

### 6.1 Rich 樣式

| 情境 | 樣式 | 範例 |
|------|------|------|
| 成功訊息 | `[green]` | `[green]匯入完成！[/green]` |
| 錯誤訊息 | `[red]` | `[red]錯誤: {e}[/red]` |
| 警告訊息 | `[yellow]` | `[yellow]警告: 資料不完整[/yellow]` |
| 資訊提示 | `[cyan]` | `[cyan]正在處理...[/cyan]` |
| 強調項目 | `[bold]` | `[bold]重要[/bold]` |

### 6.2 表格輸出

```python
from rich.table import Table

table = Table(title="標題")
table.add_column("欄位1", style="cyan")
table.add_column("欄位2", style="green")
table.add_row("值1", "值2")
console.print(table)
```

### 6.3 進度條

```python
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    TaskProgressColumn(),
    console=console,
) as progress:
    task = progress.add_task("處理中...", total=100)
    for i in range(100):
        progress.update(task, advance=1)
```

---

## 7. CLI 錯誤處理

### 7.1 標準模式

```python
@app.command()
def my_command():
    """命令說明"""
    check_typer()
    
    try:
        # 業務邏輯
        pass
    except SpecificError as e:
        console.print(f"[red]特定錯誤: {e}[/red]")
        raise typer.Exit(2)  # 特定錯誤碼
    except Exception as e:
        console.print(f"[red]錯誤: {e}[/red]")
        raise typer.Exit(1)  # 一般錯誤碼
```

### 7.2 Exit Code 規範

| Code | 意義 |
|------|------|
| 0 | 成功 |
| 1 | 一般錯誤 |
| 2 | 使用錯誤（參數錯誤等） |

---

## 8. CLI pyproject.toml 設定

```toml
[project.scripts]
{command_name} = "{package}.cli.main:main"
```

範例：

```toml
[project.scripts]
indistock = "indistockdataimporter.cli.main:main"
```

---

# Part B: API Standard（REST API 服務）

## 9. API 技術選型

| 項目 | 選擇 | 說明 |
|------|------|------|
| Web 框架 | [FastAPI](https://fastapi.tiangolo.com/) | 現代 async Python web 框架 |
| 資料驗證 | [Pydantic](https://docs.pydantic.dev/) | 型別安全的資料模型 |
| 文件 | OpenAPI (Swagger) | FastAPI 自動產生 |
| ASGI Server | [Uvicorn](https://www.uvicorn.org/) | 高效能 ASGI 伺服器 |

---

## 10. API 目錄結構

### 10.1 標準結構

```
{project_name}/
├── app/                        # 應用程式主目錄
│   ├── __init__.py
│   ├── main.py                 # FastAPI app 進入點
│   ├── routers/                # API 路由模組
│   │   ├── __init__.py
│   │   ├── {resource1}.py      # 資源路由 1
│   │   ├── {resource2}.py      # 資源路由 2
│   │   └── ...
│   ├── schemas/                # Pydantic 模型
│   │   ├── __init__.py
│   │   ├── {resource1}.py      # 資源 schema
│   │   ├── common.py           # 共用 schema
│   │   └── ...
│   ├── services/               # 業務邏輯層
│   │   ├── __init__.py
│   │   └── {service}.py
│   ├── models/                 # 資料庫模型（如適用）
│   │   ├── __init__.py
│   │   └── database.py
│   ├── core/                   # 核心設定
│   │   ├── __init__.py
│   │   ├── config.py           # 設定管理
│   │   └── dependencies.py     # 依賴注入
│   └── utils/                  # 工具函數
├── tests/
│   └── api/
│       ├── __init__.py
│       ├── conftest.py
│       └── test_{resource}.py
├── .env.example
├── requirements.txt
└── README.md
```

### 10.2 檔案職責

| 檔案/目錄 | 職責 |
|-----------|------|
| `main.py` | FastAPI app 初始化、router 註冊、middleware 設定 |
| `routers/` | API 端點定義，按資源分類 |
| `schemas/` | 請求/回應的 Pydantic 模型定義 |
| `services/` | 業務邏輯實作（與 API 層分離） |
| `core/config.py` | 環境變數與設定管理 |
| `core/dependencies.py` | FastAPI 依賴注入函數 |

---

## 11. API 實作規範

### 11.1 main.py 範本

```python
"""
FastAPI Application Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import resource1, resource2

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS 設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 註冊路由
app.include_router(resource1.router, prefix="/api/v1", tags=["resource1"])
app.include_router(resource2.router, prefix="/api/v1", tags=["resource2"])


@app.get("/health")
async def health_check():
    """健康檢查端點"""
    return {"status": "healthy", "version": settings.APP_VERSION}
```

### 11.2 Router 範本

```python
"""
{Resource} API Router

提供 {resource} 相關的 CRUD 操作端點
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.schemas.resource import (
    ResourceCreate,
    ResourceUpdate,
    ResourceResponse,
    ResourceListResponse,
)
from app.services.resource_service import ResourceService
from app.core.dependencies import get_resource_service

router = APIRouter()


@router.get("/", response_model=ResourceListResponse)
async def list_resources(
    skip: int = Query(0, ge=0, description="跳過筆數"),
    limit: int = Query(100, ge=1, le=1000, description="回傳上限"),
    service: ResourceService = Depends(get_resource_service),
):
    """
    列出所有資源
    
    - **skip**: 分頁起始位置
    - **limit**: 每頁筆數（最大 1000）
    """
    items = service.list_resources(skip=skip, limit=limit)
    return ResourceListResponse(items=items, total=len(items))


@router.get("/{resource_id}", response_model=ResourceResponse)
async def get_resource(
    resource_id: str,
    service: ResourceService = Depends(get_resource_service),
):
    """
    取得單一資源
    
    - **resource_id**: 資源唯一識別碼
    """
    resource = service.get_resource(resource_id)
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource {resource_id} not found",
        )
    return resource


@router.post("/", response_model=ResourceResponse, status_code=status.HTTP_201_CREATED)
async def create_resource(
    data: ResourceCreate,
    service: ResourceService = Depends(get_resource_service),
):
    """
    建立新資源
    """
    return service.create_resource(data)


@router.put("/{resource_id}", response_model=ResourceResponse)
async def update_resource(
    resource_id: str,
    data: ResourceUpdate,
    service: ResourceService = Depends(get_resource_service),
):
    """
    更新資源
    """
    resource = service.update_resource(resource_id, data)
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource {resource_id} not found",
        )
    return resource


@router.delete("/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resource(
    resource_id: str,
    service: ResourceService = Depends(get_resource_service),
):
    """
    刪除資源
    """
    success = service.delete_resource(resource_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource {resource_id} not found",
        )
```

### 11.3 Schema 範本

```python
"""
{Resource} Pydantic Schemas

定義 API 請求與回應的資料結構
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class ResourceBase(BaseModel):
    """資源基礎欄位"""
    name: str = Field(..., min_length=1, max_length=100, description="資源名稱")
    description: Optional[str] = Field(None, max_length=500, description="描述")


class ResourceCreate(ResourceBase):
    """建立資源請求"""
    pass


class ResourceUpdate(BaseModel):
    """更新資源請求（所有欄位可選）"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class ResourceResponse(ResourceBase):
    """資源回應"""
    id: str = Field(..., description="資源 ID")
    created_at: datetime = Field(..., description="建立時間")
    updated_at: Optional[datetime] = Field(None, description="更新時間")

    class Config:
        from_attributes = True


class ResourceListResponse(BaseModel):
    """資源列表回應"""
    items: List[ResourceResponse]
    total: int = Field(..., description="總筆數")
```

---

## 12. API 命名規範

### 12.1 URL 路徑命名

| 規則 | 範例 | 說明 |
|------|------|------|
| 複數名詞 | `/users`、`/orders` | 資源集合用複數 |
| kebab-case | `/user-profiles` | 多單字用連字號 |
| 階層結構 | `/users/{id}/orders` | 表達資源關係 |
| 版本前綴 | `/api/v1/users` | API 版本化 |

### 12.2 HTTP 方法對應

| 方法 | 用途 | URL 範例 | 說明 |
|------|------|----------|------|
| GET | 讀取 | `GET /users` | 列表 |
| GET | 讀取 | `GET /users/{id}` | 單筆 |
| POST | 建立 | `POST /users` | 新增 |
| PUT | 完整更新 | `PUT /users/{id}` | 全量更新 |
| PATCH | 部分更新 | `PATCH /users/{id}` | 增量更新 |
| DELETE | 刪除 | `DELETE /users/{id}` | 移除 |

### 12.3 Query Parameter 命名

| 類型 | 命名 | 範例 |
|------|------|------|
| 分頁 | `skip`, `limit` 或 `page`, `page_size` | `?skip=0&limit=20` |
| 排序 | `sort_by`, `order` | `?sort_by=created_at&order=desc` |
| 篩選 | 欄位名稱 | `?status=active&category=tech` |
| 搜尋 | `q` 或 `search` | `?q=keyword` |

---

## 13. API 回應格式

### 13.1 成功回應

```json
// 單一資源
{
    "id": "abc123",
    "name": "Example",
    "created_at": "2025-01-01T00:00:00Z"
}

// 資源列表
{
    "items": [...],
    "total": 100,
    "skip": 0,
    "limit": 20
}
```

### 13.2 錯誤回應

```python
# schemas/common.py
from pydantic import BaseModel
from typing import Optional, List


class ErrorDetail(BaseModel):
    """錯誤詳情"""
    loc: Optional[List[str]] = None  # 錯誤位置
    msg: str                          # 錯誤訊息
    type: str                         # 錯誤類型


class ErrorResponse(BaseModel):
    """統一錯誤回應格式"""
    error: str                        # 錯誤代碼
    message: str                      # 人可讀訊息
    details: Optional[List[ErrorDetail]] = None
```

```json
// 錯誤回應範例
{
    "error": "RESOURCE_NOT_FOUND",
    "message": "找不到指定的資源",
    "details": [
        {
            "loc": ["path", "resource_id"],
            "msg": "Resource with id 'xyz' not found",
            "type": "value_error"
        }
    ]
}
```

### 13.3 HTTP 狀態碼規範

| 狀態碼 | 用途 |
|--------|------|
| 200 OK | 成功取得/更新 |
| 201 Created | 成功建立 |
| 204 No Content | 成功刪除 |
| 400 Bad Request | 請求格式錯誤 |
| 401 Unauthorized | 未認證 |
| 403 Forbidden | 無權限 |
| 404 Not Found | 資源不存在 |
| 409 Conflict | 資源衝突 |
| 422 Unprocessable Entity | 驗證失敗 |
| 500 Internal Server Error | 伺服器錯誤 |

---

## 14. API 錯誤處理

### 14.1 Exception Handler

```python
# app/core/exceptions.py
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


class AppException(Exception):
    """應用程式自定義例外"""
    def __init__(self, error: str, message: str, status_code: int = 400):
        self.error = error
        self.message = message
        self.status_code = status_code


async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.error,
            "message": exc.message,
        },
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "VALIDATION_ERROR",
            "message": "請求資料驗證失敗",
            "details": exc.errors(),
        },
    )


# main.py 中註冊
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
```

---

## 15. API 版本化

### 15.1 URL 版本化（推薦）

```python
# 在 URL 路徑中包含版本
app.include_router(v1_router, prefix="/api/v1")
app.include_router(v2_router, prefix="/api/v2")
```

### 15.2 版本升級原則

| 情境 | 處理方式 |
|------|----------|
| 新增欄位（回應） | 不需升版，向後相容 |
| 新增選填參數（請求） | 不需升版，向後相容 |
| 移除欄位 | 需升版 |
| 變更欄位類型 | 需升版 |
| 變更 URL 結構 | 需升版 |

---

# Part C: SDK Standard（程式化整合介面）

## 16. SDK 設計原則

### 16.1 SDK 特性

| 特性 | 說明 |
|------|------|
| 封裝 | 隱藏 API 實作細節 |
| 型別安全 | 提供完整型別提示 |
| 錯誤處理 | 統一的例外類別 |
| 可測試 | 支援 mock/stub |

### 16.2 SDK 目錄結構

```
{package}/
└── sdk/
    ├── __init__.py           # 公開介面匯出
    ├── client.py             # 主要 Client 類別
    ├── models.py             # 資料模型
    ├── exceptions.py         # 例外類別
    └── _internal/            # 內部實作（不公開）
        ├── __init__.py
        ├── http.py           # HTTP 通訊
        └── auth.py           # 認證處理
```

### 16.3 SDK Client 範本

```python
"""
{Service} SDK Client

提供程式化存取 {Service} 服務的介面
"""

from typing import List, Optional
from .models import Resource, ResourceCreate
from .exceptions import SDKError, NotFoundError
from ._internal.http import HTTPClient


class ServiceClient:
    """
    {Service} SDK 主要入口
    
    Example:
        >>> client = ServiceClient(api_key="your-api-key")
        >>> resources = client.list_resources()
        >>> resource = client.get_resource("id-123")
    """
    
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.example.com/v1",
        timeout: int = 30,
    ):
        """
        初始化 SDK Client
        
        Args:
            api_key: API 金鑰
            base_url: API 基礎 URL
            timeout: 請求逾時秒數
        """
        self._http = HTTPClient(
            base_url=base_url,
            api_key=api_key,
            timeout=timeout,
        )
    
    def list_resources(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Resource]:
        """
        列出所有資源
        
        Args:
            skip: 跳過筆數
            limit: 回傳上限
            
        Returns:
            資源列表
        """
        response = self._http.get(
            "/resources",
            params={"skip": skip, "limit": limit},
        )
        return [Resource(**item) for item in response["items"]]
    
    def get_resource(self, resource_id: str) -> Resource:
        """
        取得單一資源
        
        Args:
            resource_id: 資源 ID
            
        Returns:
            資源物件
            
        Raises:
            NotFoundError: 資源不存在
        """
        response = self._http.get(f"/resources/{resource_id}")
        return Resource(**response)
    
    def create_resource(self, data: ResourceCreate) -> Resource:
        """
        建立新資源
        
        Args:
            data: 建立資料
            
        Returns:
            建立的資源
        """
        response = self._http.post("/resources", json=data.model_dump())
        return Resource(**response)
```

---

# Part D: 共通規範

## 17. 文件規範

### 17.1 CLI 文件

- 每個命令需有 docstring（顯示於 `--help`）
- 每個選項/參數需有 `help` 說明
- README 需包含安裝與使用範例

### 17.2 API 文件

- 使用 FastAPI 自動產生的 OpenAPI 文件
- 每個端點需有 docstring
- Schema 欄位需有 `description`
- 提供 `/docs`（Swagger UI）與 `/redoc`（ReDoc）

### 17.3 SDK 文件

- 每個公開方法需有完整 docstring（Google style）
- 提供 Example 使用範例
- 使用 type hints

---

## 18. 測試規範

### 18.1 CLI 測試

```python
from typer.testing import CliRunner
from app.cli.main import app

runner = CliRunner()


def test_command_success():
    result = runner.invoke(app, ["command", "--option"])
    assert result.exit_code == 0
    assert "expected output" in result.stdout


def test_command_error():
    result = runner.invoke(app, ["command", "--invalid"])
    assert result.exit_code != 0
```

### 18.2 API 測試

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_list_resources():
    response = client.get("/api/v1/resources")
    assert response.status_code == 200
    assert "items" in response.json()


def test_create_resource():
    response = client.post(
        "/api/v1/resources",
        json={"name": "test", "description": "test desc"},
    )
    assert response.status_code == 201
    assert response.json()["name"] == "test"


def test_resource_not_found():
    response = client.get("/api/v1/resources/nonexistent")
    assert response.status_code == 404
```

### 18.3 SDK 測試

```python
import pytest
from unittest.mock import Mock, patch
from app.sdk import ServiceClient
from app.sdk.exceptions import NotFoundError


def test_list_resources():
    with patch.object(ServiceClient, '_http') as mock_http:
        mock_http.get.return_value = {"items": [{"id": "1", "name": "test"}]}
        
        client = ServiceClient(api_key="test")
        resources = client.list_resources()
        
        assert len(resources) == 1
        assert resources[0].name == "test"


def test_get_resource_not_found():
    with patch.object(ServiceClient, '_http') as mock_http:
        mock_http.get.side_effect = NotFoundError("Resource not found")
        
        client = ServiceClient(api_key="test")
        
        with pytest.raises(NotFoundError):
            client.get_resource("nonexistent")
```

---

## 19. 新增介面流程

### 19.1 新增 CLI 命令

1. 開啟對應的 `commands/{group}.py`
2. 新增 `@app.command()` 裝飾的函數
3. 在 `commands/__init__.py` 中匯出（如需要）
4. 測試 `--help` 與執行結果

### 19.2 新增 API 端點

1. 在 `routers/{resource}.py` 新增端點
2. 在 `schemas/{resource}.py` 定義 request/response schema
3. 在 `services/{service}.py` 實作業務邏輯
4. 撰寫測試
5. 確認 `/docs` 顯示正確

### 19.3 新增 SDK 方法

1. 在 `sdk/client.py` 新增方法
2. 在 `sdk/models.py` 新增資料模型（如需要）
3. 撰寫 docstring 與 type hints
4. 撰寫測試

---

## 20. 檢查清單

### 20.1 CLI 檢查清單

- [ ] 命令可正常執行
- [ ] `--help` 顯示正確說明
- [ ] 錯誤處理正確（Exit code）
- [ ] 輸出格式一致（Rich 樣式）
- [ ] 有對應測試

### 20.2 API 檢查清單

- [ ] 端點符合 RESTful 設計
- [ ] Schema 驗證正確
- [ ] 錯誤回應格式統一
- [ ] `/docs` 文件正確
- [ ] 有對應測試
- [ ] 狀態碼使用正確

### 20.3 SDK 檢查清單

- [ ] 型別提示完整
- [ ] Docstring 完整（含 Example）
- [ ] 例外處理適當
- [ ] 有對應測試
