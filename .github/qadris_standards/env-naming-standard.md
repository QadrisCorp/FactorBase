# 環境變數命名標準

> 所有 QadrisCorp repo 的 `.env` 檔案必須遵循此命名規範。

---

## 資料庫連線

| 變數名稱 | 說明 | 範例 |
|----------|------|------|
| `DB_HOST` | 資料庫主機位址 | `bear.dottdot.com` |
| `DB_PORT` | 資料庫連接埠 | `43306` |
| `DB_USER` | 資料庫使用者名稱 | `datateam` |
| `DB_PASSWORD` | 資料庫密碼 | `your_password` |
| `DB_NAME` | 資料庫名稱 | `indistockdb` |

### 多資料庫連線

若專案需連接多個資料庫，使用 `{PURPOSE}_DB_*` 前綴區分：

| 情境 | 命名格式 | 範例 |
|------|----------|------|
| 單一/主要資料庫 | `DB_*` | `DB_HOST`, `DB_NAME` |
| 額外資料庫 | `{PURPOSE}_DB_*` | `MEASURE_DB_HOST`, `STOCK_DB_NAME` |

**命名規則**：
- 主要/預設資料庫：使用 `DB_*`（無前綴）
- 額外資料庫：使用 `{PURPOSE}_DB_*` 前綴
- 前綴應為**用途描述**（如 `MEASURE`、`STOCK`、`LOG`），而非資料庫類型

```env
# 主要資料庫（無前綴）
DB_HOST=db.example.com
DB_PORT=3306
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=main_database

# Measure 專用資料庫
MEASURE_DB_HOST=measure-db.example.com
MEASURE_DB_PORT=3306
MEASURE_DB_USER=measure_user
MEASURE_DB_PASSWORD=measure_password
MEASURE_DB_NAME=measure_database

# 日誌資料庫（另一個範例）
LOG_DB_HOST=log-db.example.com
LOG_DB_PORT=3306
LOG_DB_USER=log_user
LOG_DB_PASSWORD=log_password
LOG_DB_NAME=log_database
```

---

## API 服務連線

| 變數名稱 | 說明 | 範例 |
|----------|------|------|
| `{SERVICE}_URL` | 服務完整 URL | `MEASURE_MANAGER_URL=http://localhost:8001` |
| `{SERVICE}_API_KEY` | API 金鑰 | `OPENAI_API_KEY=sk-xxx` |

---

## 應用程式設定

| 變數名稱 | 說明 | 範例 |
|----------|------|------|
| `DEBUG` | 除錯模式 | `true` / `false` |
| `LOG_LEVEL` | 日誌等級 | `INFO` / `DEBUG` / `WARNING` |
| `APP_ENV` | 執行環境 | `development` / `production` |

---

## Google Sheets API

| 變數名稱 | 說明 | 範例 |
|----------|------|------|
| `GSHEET_API_KEY_PATH` | API 金鑰檔案路徑 | `./client_secret.json` |
| `GSHEET_KEY` | Google Sheets 文件 ID | `11I6ni15-xxx` |

---

## ❌ 禁止使用的命名

以下命名方式**不符合標準**，請勿使用：

| 錯誤命名 | 正確命名 |
|----------|----------|
| `host` | `DB_HOST` |
| `port` | `DB_PORT` |
| `username` | `DB_USER` |
| `pwd` / `pass` | `DB_PASSWORD` |
| `database` | `DB_NAME` |
| `MYSQL_HOST` | `DB_HOST` |
| `MARIADB_HOST` | `DB_HOST` |

---

## .env.example 範本

每個 repo 都應提供 `.env.example`：

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=your_database

# Application Settings
DEBUG=false
LOG_LEVEL=INFO

# API Services (if needed)
# MEASURE_MANAGER_URL=http://localhost:8001
```

---

## 更新日期

- 2025-12-24：新增多資料庫命名規範（`{PURPOSE}_DB_*` 格式）
- 2025-12-18：初版建立
