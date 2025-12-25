# QadrisCorp — Infrastructure Resources

Version: 1.0  
Last Updated: 2025-12-25  
Scope: 公司基礎設施與硬體資源資訊

---

## 1. 主機列表

### 1.1 生產環境

| 主機名稱 | 用途 | 規格 | IP/位置 | 存取方式 | 備註 |
|----------|------|------|---------|----------|------|
| `{prod-server-1}` | {生產環境主服務} | {32 vCPU, 128GB RAM, 1TB SSD} | {10.0.0.x} | SSH | {24/7 運行} |
| `{prod-server-2}` | {生產環境備援} | {32 vCPU, 128GB RAM, 1TB SSD} | {10.0.0.x} | SSH | {熱備援} |

### 1.2 開發測試環境

| 主機名稱 | 用途 | 規格 | IP/位置 | 存取方式 | 備註 |
|----------|------|------|---------|----------|------|
| `{dev-server-1}` | {開發測試} | {16 vCPU, 64GB RAM, 500GB SSD} | {10.0.1.x} | SSH | {開發用} |
| `{test-server-1}` | {整合測試} | {16 vCPU, 64GB RAM, 500GB SSD} | {10.0.1.x} | SSH | {CI/CD} |

### 1.3 資料庫伺服器

| 主機名稱 | 用途 | 規格 | IP/位置 | 存取方式 | 備註 |
|----------|------|------|---------|----------|------|
| `{db-server-1}` | {主資料庫} | {16 vCPU, 128GB RAM, 2TB SSD} | {10.0.2.x} | 內網 3306 | MariaDB |
| `{db-server-2}` | {資料庫備援} | {16 vCPU, 128GB RAM, 2TB SSD} | {10.0.2.x} | 內網 3306 | Replica |

---

## 2. 雲端服務

| 服務 | 提供商 | 用途 | 資源識別 | 備註 |
|------|--------|------|----------|------|
| {S3} | {AWS} | {資料儲存} | {bucket: qadris-data} | {長期資料保存} |
| {EC2} | {AWS} | {彈性運算} | {instance-id: xxx} | {按需使用} |
| {RDS} | {AWS} | {雲端資料庫} | {db-identifier: xxx} | {備份用} |

---

## 3. 網路架構

```
Internet
    │
    ▼
┌─────────────┐
│   Firewall  │
└─────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│           DMZ (10.0.0.x)            │
│  ┌─────────┐  ┌─────────┐          │
│  │ Web     │  │ API     │          │
│  │ Server  │  │ Gateway │          │
│  └─────────┘  └─────────┘          │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│        Internal (10.0.1.x)          │
│  ┌─────────┐  ┌─────────┐          │
│  │ App     │  │ Worker  │          │
│  │ Server  │  │ Server  │          │
│  └─────────┘  └─────────┘          │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│        Database (10.0.2.x)          │
│  ┌─────────┐  ┌─────────┐          │
│  │ MariaDB │  │ Redis   │          │
│  │ Master  │  │ Cache   │          │
│  └─────────┘  └─────────┘          │
└─────────────────────────────────────┘
```

---

## 4. 存取方式

### 4.1 SSH 存取

```bash
# 開發環境
ssh {username}@{dev-server-ip}

# 需要 VPN 連線才能存取內網主機
```

### 4.2 VPN 設定

- VPN 類型：{OpenVPN / WireGuard}
- 設定檔取得：{聯繫 Infrastructure Team}
- 連線後可存取：10.0.x.x 網段

---

## 5. 監控與告警

| 工具 | 用途 | URL | 備註 |
|------|------|-----|------|
| {Grafana} | {監控儀表板} | {http://grafana.internal} | {需 VPN} |
| {Prometheus} | {指標收集} | {http://prometheus.internal} | {需 VPN} |
| {AlertManager} | {告警管理} | {http://alertmanager.internal} | {需 VPN} |

---

## 6. 聯絡資訊

| 問題類型 | 聯絡對象 | 聯絡方式 |
|----------|----------|----------|
| 主機問題 | Infrastructure Team | {Slack: #infra-support} |
| 網路問題 | Infrastructure Team | {Slack: #infra-support} |
| 權限申請 | Infrastructure Team | {透過 Issue} |

---

## Changelog

- 1.0 — 2025-12-25: 初版建立（模板）
