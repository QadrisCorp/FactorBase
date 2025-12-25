# QadrisCorp — Credentials Guide

Version: 1.0  
Last Updated: 2025-12-25  
Scope: 憑證取得方式與管理規範（不含實際密碼）

---

## ⚠️ 安全警告

- **禁止**在程式碼中 hardcode 任何憑證
- **禁止**將憑證提交到 Git
- **必須**使用環境變數或安全的憑證管理服務

---

## 1. 憑證類型總覽

| 憑證類型 | 用途 | 取得方式 | 有效期 |
|----------|------|----------|--------|
| API Token | QadrisWebAPI 認證 | 申請 Issue | 1 年 |
| Database Credentials | 資料庫存取 | 申請 Issue | 永久（可撤銷） |
| SSH Key | 主機存取 | 自行產生 + 註冊 | 永久（可撤銷） |
| AWS Credentials | 雲端服務 | Infrastructure Team | 定期輪換 |

---

## 2. API Token

### 2.1 申請流程

1. 在 `QadrisCorp/infrastructure-requests` 開 Issue
2. 使用模板：「API Token 申請」
3. 填寫：
   - 用途說明
   - 預計使用的端點
   - 預計請求頻率
4. Infrastructure Team 審核（約 1-2 工作天）
5. Token 會透過安全通道發送

### 2.2 使用方式

```python
import os

# 從環境變數讀取
api_token = os.getenv("QADRIS_API_TOKEN")

if not api_token:
    raise ValueError("QADRIS_API_TOKEN environment variable not set")
```

### 2.3 .env 設定

```bash
# .env（不要提交到 Git）
QADRIS_API_TOKEN=your_token_here
```

```bash
# .env.example（提交到 Git，作為範本）
QADRIS_API_TOKEN=
```

---

## 3. Database Credentials

### 3.1 申請流程

1. 在 `QadrisCorp/infrastructure-requests` 開 Issue
2. 使用模板：「資料庫存取申請」
3. 填寫：
   - 需要存取的資料庫
   - 需要的權限（唯讀 / 讀寫）
   - 用途說明
4. Data Team + 主管審核
5. 憑證透過安全通道發送

### 3.2 使用方式

```python
import os

db_config = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}
```

### 3.3 .env 設定

```bash
# .env
DB_HOST=db.qadris.internal
DB_PORT=3306
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=qadris_main
```

---

## 4. SSH Key

### 4.1 產生 SSH Key

```bash
# 產生新的 SSH Key
ssh-keygen -t ed25519 -C "your_email@qadris.com"

# 或使用 RSA
ssh-keygen -t rsa -b 4096 -C "your_email@qadris.com"
```

### 4.2 註冊公鑰

1. 複製公鑰內容：
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```
2. 在 `QadrisCorp/infrastructure-requests` 開 Issue
3. 附上公鑰內容與需要存取的主機列表
4. Infrastructure Team 會將公鑰加入授權列表

### 4.3 SSH Config 設定

```bash
# ~/.ssh/config
Host qadris-dev
    HostName dev-server.qadris.internal
    User your_username
    IdentityFile ~/.ssh/id_ed25519

Host qadris-prod
    HostName prod-server.qadris.internal
    User your_username
    IdentityFile ~/.ssh/id_ed25519
```

---

## 5. AWS Credentials

### 5.1 取得方式

AWS 憑證由 Infrastructure Team 管理，使用 IAM Role 方式：

1. 開發環境：透過 AWS CLI 設定
2. 生產環境：使用 EC2 Instance Profile

### 5.2 本地開發設定

```bash
# 安裝 AWS CLI
pip install awscli

# 設定憑證
aws configure
# 輸入 Access Key ID
# 輸入 Secret Access Key
# 輸入 Default region (ap-northeast-1)
```

### 5.3 程式碼使用

```python
import boto3

# AWS SDK 會自動從環境變數或 ~/.aws/credentials 讀取憑證
s3 = boto3.client('s3')
```

---

## 6. 憑證管理最佳實踐

### 6.1 環境變數管理

```python
# config.py
import os
from dataclasses import dataclass

@dataclass
class Config:
    # API
    api_token: str = os.getenv("QADRIS_API_TOKEN", "")
    
    # Database
    db_host: str = os.getenv("DB_HOST", "localhost")
    db_port: int = int(os.getenv("DB_PORT", 3306))
    db_user: str = os.getenv("DB_USER", "")
    db_password: str = os.getenv("DB_PASSWORD", "")
    db_name: str = os.getenv("DB_NAME", "")
    
    def validate(self):
        """驗證必要的憑證是否已設定"""
        missing = []
        if not self.api_token:
            missing.append("QADRIS_API_TOKEN")
        if not self.db_user:
            missing.append("DB_USER")
        if missing:
            raise ValueError(f"Missing required credentials: {', '.join(missing)}")

config = Config()
```

### 6.2 .gitignore 設定

```gitignore
# 憑證檔案
.env
.env.local
.env.*.local
*.pem
*.key

# AWS
.aws/

# SSH（私鑰）
id_rsa
id_ed25519
```

### 6.3 憑證輪換

| 憑證類型 | 建議輪換週期 | 輪換方式 |
|----------|-------------|----------|
| API Token | 每年 | 申請新 Token，更新環境變數 |
| Database Password | 每半年 | 聯繫 Data Team |
| SSH Key | 視需要 | 產生新 Key 並註冊 |
| AWS Credentials | 自動 | 由 IAM Role 管理 |

---

## 7. 緊急情況處理

### 7.1 憑證外洩

如果懷疑憑證外洩：

1. **立即**聯繫 Infrastructure Team（Slack: #security-urgent）
2. **不要**嘗試自行撤銷（可能造成服務中斷）
3. 提供外洩情況說明
4. 等待 Infrastructure Team 指示

### 7.2 聯絡方式

| 情況 | 聯絡管道 | 回應時間 |
|------|----------|----------|
| 一般申請 | Issue | 1-2 工作天 |
| 緊急申請 | Slack #infra-support | 4 小時內 |
| 安全事件 | Slack #security-urgent | 立即 |

---

## Changelog

- 1.0 — 2025-12-25: 初版建立
