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

若專案需連接多個資料庫，使用前綴區分：

```env
# 主要資料庫
DB_HOST=bear.dottdot.com
DB_PORT=43306
DB_USER=datateam
DB_PASSWORD=datateam
DB_NAME=indistockdb

# 次要資料庫（使用前綴）
SECONDARY_DB_HOST=other.host.com
SECONDARY_DB_PORT=3306
SECONDARY_DB_USER=other_user
SECONDARY_DB_PASSWORD=other_pass
SECONDARY_DB_NAME=otherdb
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

- 2025-12-18：初版建立
