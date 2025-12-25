# QadrisCorp — Database Resources

Version: 1.0  
Last Updated: 2025-12-25  
Scope: 公司資料庫資訊

---

## 1. 資料庫列表

### 1.1 生產環境

| 名稱 | 類型 | 用途 | Host | Port | 備註 |
|------|------|------|------|------|------|
| qadris_main | MariaDB | 主要業務資料 | {db.qadris.internal} | 3306 | 主資料庫 |
| qadris_main_replica | MariaDB | 讀取備援 | {db-replica.qadris.internal} | 3306 | 唯讀 |
| qadris_factor | PostgreSQL | 因子資料 | {factor-db.qadris.internal} | 5432 | Research 專用 |
| qadris_cache | Redis | 快取服務 | {cache.qadris.internal} | 6379 | — |

### 1.2 開發環境

| 名稱 | 類型 | 用途 | Host | Port | 備註 |
|------|------|------|------|------|------|
| qadris_dev | MariaDB | 開發測試 | {dev-db.qadris.internal} | 3306 | 可自由操作 |
| qadris_test | MariaDB | 自動化測試 | {test-db.qadris.internal} | 3306 | CI/CD 用 |

---

## 2. 資料庫 Schema

### 2.1 qadris_main

#### 股票基本資料

```sql
-- stocks 表
CREATE TABLE stocks (
    stock_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    market VARCHAR(10) NOT NULL,        -- TW, US, HK
    sector VARCHAR(50),
    industry VARCHAR(50),
    listed_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

| 欄位 | 型別 | 說明 |
|------|------|------|
| stock_id | VARCHAR(20) | 股票代碼（主鍵） |
| name | VARCHAR(100) | 股票名稱 |
| market | VARCHAR(10) | 市場代碼 |
| sector | VARCHAR(50) | 產業類別 |
| industry | VARCHAR(50) | 細分產業 |
| listed_date | DATE | 上市日期 |

#### 價格資料

```sql
-- prices 表
CREATE TABLE prices (
    stock_id VARCHAR(20),
    date DATE,
    open DECIMAL(12,4),
    high DECIMAL(12,4),
    low DECIMAL(12,4),
    close DECIMAL(12,4),
    volume BIGINT,
    adj_close DECIMAL(12,4),
    PRIMARY KEY (stock_id, date),
    FOREIGN KEY (stock_id) REFERENCES stocks(stock_id)
);
```

| 欄位 | 型別 | 說明 |
|------|------|------|
| stock_id | VARCHAR(20) | 股票代碼 |
| date | DATE | 交易日期 |
| open | DECIMAL(12,4) | 開盤價 |
| high | DECIMAL(12,4) | 最高價 |
| low | DECIMAL(12,4) | 最低價 |
| close | DECIMAL(12,4) | 收盤價 |
| volume | BIGINT | 成交量 |
| adj_close | DECIMAL(12,4) | 調整後收盤價 |

#### 財務指標

```sql
-- measures 表
CREATE TABLE measures (
    stock_id VARCHAR(20),
    measure_id VARCHAR(20),
    date DATE,
    value DECIMAL(20,6),
    PRIMARY KEY (stock_id, measure_id, date),
    FOREIGN KEY (stock_id) REFERENCES stocks(stock_id)
);
```

### 2.2 qadris_factor

#### 因子定義

```sql
-- factors 表
CREATE TABLE factors (
    factor_id VARCHAR(50) PRIMARY KEY,
    factor_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),               -- momentum, value, quality, etc.
    description TEXT,
    formula TEXT,
    created_by VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 因子值

```sql
-- factor_values 表
CREATE TABLE factor_values (
    factor_id VARCHAR(50),
    stock_id VARCHAR(20),
    date DATE,
    value DECIMAL(20,10),
    PRIMARY KEY (factor_id, stock_id, date)
);
```

---

## 3. 連線方式

### 3.1 Python (SQLAlchemy)

```python
from sqlalchemy import create_engine
import os

# MariaDB
engine = create_engine(
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# PostgreSQL
engine = create_engine(
    f"postgresql://{os.getenv('PG_USER')}:{os.getenv('PG_PASSWORD')}"
    f"@{os.getenv('PG_HOST')}:{os.getenv('PG_PORT')}/{os.getenv('PG_NAME')}"
)
```

### 3.2 Python (直接連線)

```python
import pymysql

connection = pymysql.connect(
    host=os.getenv('DB_HOST'),
    port=int(os.getenv('DB_PORT', 3306)),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME'),
    charset='utf8mb4'
)
```

### 3.3 Redis

```python
import redis

r = redis.Redis(
    host=os.getenv('REDIS_HOST'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    db=0,
    decode_responses=True
)
```

---

## 4. 環境變數設定

```bash
# MariaDB (qadris_main)
DB_HOST=db.qadris.internal
DB_PORT=3306
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=qadris_main

# PostgreSQL (qadris_factor)
PG_HOST=factor-db.qadris.internal
PG_PORT=5432
PG_USER=your_username
PG_PASSWORD=your_password
PG_NAME=qadris_factor

# Redis
REDIS_HOST=cache.qadris.internal
REDIS_PORT=6379
```

---

## 5. 使用最佳實踐

### 5.1 連線池

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    connection_string,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800
)
```

### 5.2 讀寫分離

```python
# 寫入使用主資料庫
write_engine = create_engine(f"mysql+pymysql://...@db.qadris.internal/...")

# 讀取使用備援資料庫
read_engine = create_engine(f"mysql+pymysql://...@db-replica.qadris.internal/...")
```

### 5.3 查詢優化

```python
# 避免：SELECT *
cursor.execute("SELECT * FROM prices WHERE stock_id = '2330'")

# 建議：指定欄位
cursor.execute("SELECT date, close, volume FROM prices WHERE stock_id = '2330'")

# 建議：使用 LIMIT
cursor.execute("SELECT date, close FROM prices WHERE stock_id = '2330' ORDER BY date DESC LIMIT 100")
```

---

## 6. 權限申請

| 資料庫 | 申請方式 | 審核者 |
|--------|----------|--------|
| qadris_main (唯讀) | Issue 申請 | Data Team |
| qadris_main (讀寫) | 需主管核准 | Data Team + Manager |
| qadris_factor | Issue 申請 | Research Team |
| qadris_dev | 自動取得 | — |

---

## Changelog

- 1.0 — 2025-12-25: 初版建立
