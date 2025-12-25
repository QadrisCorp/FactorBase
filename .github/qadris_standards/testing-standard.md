# QadrisCorp — Testing Standard

Version: 1.0  
Last Updated: 2025-12-24  
Scope: 所有專案的測試規範

---

## 1. 測試框架

- 統一使用 **PyTest**
- 測試檔案放置於 `/tests` 目錄
- 測試檔案命名：`test_{模組名}.py`

---

## 2. 測試原則

- 對外部服務（資料庫、API、網路請求）使用 **mock/stub**
- 測試需可獨立運行，不依賴外部環境
- 測試函數命名：`test_{功能描述}_{情境}`
- 禁止在測試中進行實際外部連線

---

## 3. 測試類型

| 類型 | 說明 | 必要性 |
|------|------|--------|
| 單元測試 | 單一函數/方法 | 必要 |
| 整合測試 | 模組間互動 | 視專案需求 |
| 錯誤處理測試 | 例外狀況與邊界條件 | 必要 |

---

## 4. 程式碼變更與測試

| 變更類型 | 測試要求 |
|----------|----------|
| 新增功能 | 新增對應測試 |
| 修改功能 | 更新對應測試 |
| 修復 Bug | 新增重現該 Bug 的測試 |
| 重構程式碼 | 確保既有測試通過 |

---

## 5. 測試執行

- 撰寫程式碼後，**必須執行測試**確認通過
- 提交前需確保所有測試通過
- 若測試失敗，需修復後再提交

---

## 6. 測試目錄結構

```
project/
├── src/
│   └── module_name/
│       └── __init__.py
└── tests/
    ├── __init__.py
    ├── conftest.py          # pytest fixtures
    ├── test_module_name.py
    └── fixtures/            # 測試資料
        └── sample_data.json
```

---

## 7. PyTest 常用指令

```bash
# 執行所有測試
pytest

# 執行特定檔案
pytest tests/test_module.py

# 執行特定測試函數
pytest tests/test_module.py::test_function_name

# 顯示詳細輸出
pytest -v

# 顯示 print 輸出
pytest -s

# 產生覆蓋率報告
pytest --cov=src --cov-report=html
```

---

## 8. Mock/Stub 範例

```python
from unittest.mock import Mock, patch

def test_api_call_success():
    """測試 API 呼叫成功情境"""
    with patch('module.requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"data": "test"}
        
        result = fetch_data()
        
        assert result == {"data": "test"}
        mock_get.assert_called_once()

def test_database_query():
    """測試資料庫查詢（使用 mock）"""
    mock_db = Mock()
    mock_db.query.return_value = [{"id": 1, "name": "test"}]
    
    result = get_records(mock_db)
    
    assert len(result) == 1
    mock_db.query.assert_called_once()
```

---

## Changelog

### v1.0 (2025-12-24)
- 從 `copilot-instructions-global.md` Section 10 抽出為獨立 Standard
- 新增 Section 6 測試目錄結構
- 新增 Section 7 PyTest 常用指令
- 新增 Section 8 Mock/Stub 範例
