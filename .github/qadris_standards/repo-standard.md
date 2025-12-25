# QadrisCorp — Repository Creation Standard

Version: 1.0  
Last Updated: 2025-12-24  
Scope: 新建 GitHub Repository 的標準流程

---

## 1. 新增 Repo 流程

當使用者要求新增 repo 時，Copilot **必須**依序執行以下步驟：

### 步驟 1：在 GitHub 建立 Private Repo

```bash
gh repo create QadrisCorp/{repo_name} --private --description "{repo_description}"
```

- 使用 GitHub CLI 建立私有 repo
- 若未安裝 `gh`，請先執行 `sudo apt install gh` 並完成 `gh auth login`

### 步驟 2：建立本地資料夾

- 在與 QadrisCorp 同層目錄下建立與 repo 相同名稱的資料夾
- 路徑範例：若 QadrisCorp 位於 `/home/chubear/QadrisCorp`，新 repo `NewProject` 應建立於 `/home/chubear/NewProject`

```bash
mkdir -p /home/chubear/{repo_name}
```

### 步驟 3：初始化 Git 並連結 Remote

```bash
cd /home/chubear/{repo_name}
git init
git remote add origin git@github.com:QadrisCorp/{repo_name}.git
```

### 步驟 4：確認連結正確

```bash
git remote -v
```

應顯示：
```
origin  git@github.com:QadrisCorp/{repo_name}.git (fetch)
origin  git@github.com:QadrisCorp/{repo_name}.git (push)
```

### 步驟 5：同步公司治理檔案

使用 `sync_qadris_governance.py` 自動同步治理檔案：

```bash
# 建立 .github 目錄
mkdir -p /home/chubear/{repo_name}/.github

# 使用同步工具自動複製所有必要的治理檔案
python /home/chubear/QadrisCorp/sync_qadris_governance.py -r {repo_name} --no-push

# 複製 .vscode
cp -r /home/chubear/QadrisCorp/.vscode /home/chubear/{repo_name}/

# 複製初始版 copilot-instructions.md
cp /home/chubear/{repo_name}/.github/qadris_templates/copilot-instructions-initial.md \
   /home/chubear/{repo_name}/.github/copilot-instructions.md
```

> **注意**：初始版 `copilot-instructions.md` 會在專案規劃階段使用。待 `product_spec.md` 與程式架構確定後，再依 `copilot-instructions-template.md` 產生完整版。

### 步驟 6：初始提交

```bash
git add .
git commit -m "chore: 初始化專案結構與公司治理檔案"
git push -u origin main
```

---

## 2. 必要檔案清單

新 Repo 必須包含以下檔案：

| 檔案/目錄 | 說明 | 來源 |
|-----------|------|------|
| `.github/copilot-instructions.md` | 專案 Copilot 規範 | 初始版 → 完整版 |
| `.github/qadris_governance/` | 公司治理文件 | sync 工具同步 |
| `.github/qadris_standards/` | 標準規範文件 | sync 工具同步 |
| `.github/qadris_templates/` | 模板文件 | sync 工具同步 |
| `.github/agents/` | 部門 Agent 文件 | sync 工具同步 |
| `.github/ISSUE_TEMPLATE/` | Issue 模板 | sync 工具同步 |
| `.github/PULL_REQUEST_TEMPLATE.md` | PR 模板 | sync 工具同步 |
| `.vscode/` | VS Code 設定 | 手動複製 |
| `README.md` | 專案說明文件 | 依模板建立 |
| `.gitignore` | Git 忽略規則 | 依專案類型建立 |
| `.env.example` | 環境變數範本 | 依專案需求建立 |

---

## 3. README.md 建立

使用 `.github/qadris_templates/README_TEMPLATE.md` 作為起始模板。

必須包含的區塊：
- 專案名稱與簡介
- 安裝與環境設定
- 使用方式
- 專案架構
- 開發指南

---

## 4. copilot-instructions.md 建立（兩階段流程）

### 階段一：初始版（建 Repo 時）

使用 `.github/qadris_templates/copilot-instructions-initial.md` 直接複製。

用途：
- 讓 AI 從討論階段就遵循公司規範
- 引導產生 `product_spec.md`

### 階段二：完整版（架構確定後）

待 `product_spec.md` 與程式架構確定後，請 AI 依 `.github/qadris_templates/copilot-instructions-template.md` 產生完整版。

必須填寫的項目：
- 專案名稱與目的
- Owner Team
- 技術架構
- 專案專屬規則

---

## 5. .gitignore 建議

### Python 專案

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
.env

# IDE
.idea/
*.swp
*.swo

# Test
.pytest_cache/
.coverage
htmlcov/

# Build
dist/
build/
*.egg-info/
```

### Node.js 專案

```gitignore
# Node
node_modules/
npm-debug.log
yarn-error.log

# Environment
.env
.env.local

# Build
dist/
build/
```

---

## 6. 快速建立腳本

一鍵執行所有步驟（需在 QadrisCorp 目錄下執行）：

```bash
#!/bin/bash
REPO_NAME=$1
REPO_DESC=$2

if [ -z "$REPO_NAME" ]; then
    echo "Usage: ./create_repo.sh <repo_name> [description]"
    exit 1
fi

# Step 1: Create GitHub repo
gh repo create QadrisCorp/$REPO_NAME --private --description "$REPO_DESC"

# Step 2: Create local folder
mkdir -p /home/chubear/$REPO_NAME

# Step 3: Initialize git
cd /home/chubear/$REPO_NAME
git init
git remote add origin git@github.com:QadrisCorp/$REPO_NAME.git

# Step 4: Sync governance files
mkdir -p .github
python /home/chubear/QadrisCorp/sync_qadris_governance.py -r $REPO_NAME --no-push

# Step 5: Copy .vscode
cp -r /home/chubear/QadrisCorp/.vscode .

# Step 6: Initial commit
git add .
git commit -m "chore: 初始化專案結構與公司治理檔案"
git push -u origin main

echo "✅ Repository $REPO_NAME created successfully!"
```

---

## Changelog

### v1.0 (2025-12-24)
- 初版建立
- 定義六步驟建立流程
- 新增必要檔案清單
- 新增 .gitignore 範例
- 新增快速建立腳本
