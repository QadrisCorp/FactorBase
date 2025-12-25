# GitHub Actions Workflow 建立標準

> 所有 QadrisCorp repo 的 CI/CD workflow 必須遵循此規範。
> AI agent 協助建立 workflow 時，必須依照本文件指引。

---

## 目錄結構

```
.github/
└── workflows/
    ├── ci.yml              # 主要 CI 流程（必要）
    ├── test.yml            # 測試流程（選用）
    ├── deploy.yml          # 部署流程（選用）
    └── release.yml         # 發布流程（選用）
```

---

## 檔案命名規則

| 用途 | 檔案名稱 | 說明 |
|------|----------|------|
| 持續整合 | `ci.yml` | Lint、測試、建置 |
| 單元測試 | `test.yml` | 獨立測試流程 |
| 部署 | `deploy.yml` | 部署至各環境 |
| 發布 | `release.yml` | 版本發布 |
| 排程任務 | `scheduled-{task}.yml` | 定時執行任務 |
| 手動觸發 | `manual-{task}.yml` | 需手動觸發的任務 |

---

## Workflow 命名規則

```yaml
name: CI                    # 簡潔明確的名稱
# 或
name: Deploy to Production  # 說明目標環境
```

---

## 觸發條件標準

### 主要分支保護

```yaml
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]
```

### 路徑過濾（推薦）

```yaml
on:
  push:
    paths:
      - 'src/**'
      - 'tests/**'
      - 'pyproject.toml'
      - 'requirements*.txt'
    paths-ignore:
      - '**.md'
      - 'docs/**'
```

---

## 必要的 Jobs

### Python 專案

```yaml
jobs:
  lint:
    name: Lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install ruff
      - name: Run linter
        run: ruff check .

  test:
    name: Test
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      - name: Run tests
        run: pytest --cov=src --cov-report=xml
```

### Node.js 專案

```yaml
jobs:
  lint:
    name: Lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - name: Install dependencies
        run: npm ci
      - name: Run linter
        run: npm run lint

  test:
    name: Test
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v4
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - name: Install dependencies
        run: npm ci
      - name: Run tests
        run: npm test
```

---

## Secrets 與環境變數

### 命名規則

| 類型 | 命名格式 | 範例 |
|------|----------|------|
| API 金鑰 | `{SERVICE}_API_KEY` | `OPENAI_API_KEY` |
| 存取權杖 | `{SERVICE}_TOKEN` | `GITHUB_TOKEN` |
| 密碼 | `{SERVICE}_PASSWORD` | `DB_PASSWORD` |
| 憑證 | `{SERVICE}_CREDENTIALS` | `GCP_CREDENTIALS` |

### 使用方式

```yaml
env:
  DB_HOST: ${{ secrets.DB_HOST }}
  DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
```

### ❌ 禁止事項

- **禁止** 在 workflow 中硬編碼敏感資訊
- **禁止** 將 secrets 輸出至 logs
- **禁止** 在 PR 中暴露 secrets

---

## 快取策略

### Python

```yaml
- name: Cache pip packages
  uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements*.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-
```

### Node.js

```yaml
- name: Setup Node.js
  uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'npm'  # 內建快取
```

---

## 分支策略與環境

| 分支 | 環境 | 觸發條件 |
|------|------|----------|
| `main` | Production | Push / Manual |
| `develop` | Staging | Push |
| `feature/*` | Development | PR |

### 環境保護

```yaml
jobs:
  deploy-prod:
    environment:
      name: production
      url: https://app.qadris.com
    runs-on: ubuntu-latest
    steps:
      # ...
```

---

## 通知設定

### 失敗通知（推薦）

```yaml
- name: Notify on failure
  if: failure()
  uses: slackapi/slack-github-action@v1
  with:
    channel-id: 'ci-alerts'
    slack-message: '❌ CI failed on ${{ github.repository }}'
  env:
    SLACK_BOT_TOKEN: ${{ secrets.SLACK_BOT_TOKEN }}
```

---

## 版本鎖定

### ✅ 正確做法

```yaml
- uses: actions/checkout@v4          # 使用主版本
- uses: actions/setup-python@v5
```

### ❌ 避免

```yaml
- uses: actions/checkout@main        # 不穩定
- uses: actions/checkout@latest      # 不存在
```

---

## Workflow 模板

### 最小 Python CI

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install ruff pytest
      
      - name: Lint
        run: ruff check .
      
      - name: Test
        run: pytest
```

### 最小 Node.js CI

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Lint
        run: npm run lint
      
      - name: Test
        run: npm test
```

---

## Checklist

AI agent 建立 workflow 前，確認以下項目：

- [ ] 檔案放置於 `.github/workflows/` 目錄
- [ ] 檔案命名符合規範
- [ ] 使用正確的觸發條件
- [ ] 包含 lint 和 test jobs
- [ ] Secrets 使用 `${{ secrets.XXX }}` 格式
- [ ] Actions 版本已鎖定（使用 `@v4` 格式）
- [ ] 設定適當的快取策略
- [ ] 敏感資訊未硬編碼
