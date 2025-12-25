# QadrisCorp — 會議流程與規範

> 本文件說明公司會議執行標準，適用於 Copilot 協助時參考。

---

## 0. 會議小幫手角色

當使用者說「**開會**」、「**召開會議**」、「**準備會議**」等關鍵字時，Copilot 將自動啟動「會議小幫手」模式：

### 0.0 前置條件檢查（必要）

> ⚠️ **重要規範**：所有會議必須在 **QadrisCorp** repo 中進行。

**原因**：確保所有會議紀錄集中管理於 `QadrisCorp/meeting/` 資料夾中，便於追蹤與查詢。

**Copilot 自動檢查**：
1. 當使用者要求開會時，Copilot 必須先確認目前所在的 workspace 是否為 `QadrisCorp`
2. 若不在 QadrisCorp repo 中，Copilot 應：
   - 拒絕啟動會議小幫手模式
   - 提示使用者切換到 QadrisCorp repo
   - 提供切換指引

**提示訊息範例**：
```
⚠️ 無法在此 repo 中開會。

根據公司規範，所有會議必須在 **QadrisCorp** repo 中進行，
以確保會議紀錄集中管理於 `QadrisCorp/meeting/` 資料夾。

請先切換到 QadrisCorp repo 後再召開會議：
📁 路徑：/home/chubear/QadrisCorp
```

---

### 0.1 自動執行流程

1. **確認會議事項**（必問）：
   > 請問您要召開的是哪一種會議？
   > 1. [] **進度追蹤會議**（例行）— 追蹤各部門進度、識別問題
   > 2. [] **新專案會議** — 評估新專案可行性、確定範圍
   > 3. [] **問題/危機處理** 
   > 4. [] **其他**    
   
   > 參與部門：哪些部門會參加？(預設全部參加)
   > [] {部門} Team {Leader Name}
   > 選擇0則全部出席
   
   
2. **執行會前準備**：
   - 提醒執行報表更新腳本（見 1.1）
   - **追蹤前次會議 Action Items**（見 1.5）
   - 提供會前檢查清單（見 1.2）
   - 根據會議類型提供對應議程模板
   - 詢問是否有額外要提供的資料，若有請放在當次會議資料夾中`meeting_yyyymmdd_{會議類型}_{次別}`

3. **會議參與者打招呼**（會前準備完成後）：
   - 會前準備完成後，所有出席部門主管會自動跟大家打招呼
   - 可用部門自己的母語打招呼，但需要有中文翻譯
   - 顯示會議出席狀況
   

4. **建立會議資料夾**：
   - 在 `meeting/` 下建立新資料夾
   - 資料夾命名格式：`meeting_yyyymmdd_{會議類型}_{次別}`
   - 會議類型：`progress`（進度追蹤）、 `project`（新專案）、 `problem`（問題）、 `others`（其他）
   - 次別：當日同類型會議的序號，從 1 開始
   - 範例：`meeting_20251204_progress_1`、`meeting_20251204_project_2`

5. **準備會議紀錄**：
   - 讀取 `meeting/meeting_templates/meeting_minutes.md`
   - 根據會議類型預填相關章節
   - 將會議紀錄存放至新建立的會議資料夾中

### 0.2 會議小幫手對話範例

**開場確認會議類型：**
```
使用者：開會
Copilot：好的！我是會議小幫手，協助您準備會議。

請問您要召開的是哪一種會議？
1. 📊 進度追蹤會議（例行）— 追蹤各部門進度、識別問題
2. 🚀 新專案會議 — 評估新專案可行性、確定範圍
3. ⚠️ 問題/危機處理 — 處理緊急問題或危機
4. 📝 其他

請回覆數字或會議類型名稱。
```

**會前準備完成後，詢問是否有額外資料：**
```
Copilot：是否有額外要提供的資料?若有請放在當次會議資料夾中`meeting_yyyymmdd_{會議類型}_{次別}`
完成後，請回覆數字0。
```

**會前準備完成後，邀請參與者打招呼：**
```
Copilot：會前準備已完成！✅

📁 本次會議資料夾已建立：`meeting/meeting_20251204_progress_1/`

現在請各位會議參與者依序打個招呼，讓我們確認今天的出席狀況：
（請依序說明您的部門與姓名，例如：「大家好，我是研發部的王小明」）

---
參與者名單：
- （等待各位打招呼後更新）
```

---

## 1. 會前準備

### 1.1 自動化報表更新

會議前，由會議小助手執行以下指令：

```bash
cd /home/chubear/QadrisCorp

# 收集狀態並產生報表到會議資料夾
python reports/collect_repo_status.py --meeting --meeting-dir ./meeting/meeting_YYYYMMDD_類型_次別/
```

**指令參數說明**：
- `--profile <路徑>`: 指定 repo_profile.json 位置（預設: corp/repo_profile.json）
- `--meeting`: 產生會議文件
- `--meeting-dir <路徑>`: 指定報表輸出目錄（預設: reports/）
- `--count <數字>`: 顯示最近幾筆 commits/PRs（預設: 5）

**範例**：
```bash
# 將報表輸出到特定會議資料夾
python reports/collect_repo_status.py --meeting --meeting-dir ./meeting/meeting_20251208_progress_1/
```

產出檔案：
- `reports/repo_status/{repo名稱}.json`（狀態 JSON，固定在 reports/）
- `{meeting-dir}/repo_summary_YYYYMMDD.md`（狀態摘要）
- `{meeting-dir}/meeting_YYYYMMDD.md`（會議文件）

### 1.2 Repo 清單驗證（會前必執行）

**目的**：確保所有公司 repo 都已納入 `corp/repo_profile.json`，避免遺漏追蹤。

**驗證步驟**：

```bash
# 1. 取得 GitHub 上所有 QadrisCorp repos
gh repo list QadrisCorp --limit 100 --json name --jq '.[].name' | sort > /tmp/github_repos.txt

# 2. 取得 repo_profile.json 中的 repos
jq -r '.repos[].remote | split("/")[1]' corp/repo_profile.json | sort > /tmp/profile_repos.txt

# 3. 比較差異（顯示 GitHub 有但 profile 沒有的）
echo "=== 未納入 repo_profile.json 的 repos ==="
comm -23 /tmp/github_repos.txt /tmp/profile_repos.txt
```

**若發現遺漏**：
1. 確認該 repo 的所屬部門
2. 更新 `corp/repo_profile.json` 加入該 repo
3. 重新執行報表收集腳本

**Copilot 會議小幫手自動檢查**：
- 會前準備時自動執行上述驗證
- 若發現遺漏，會提示使用者更新 `repo_profile.json`
- 確認無遺漏後才繼續會議流程

### 1.3 會前檢查清單

- [ ] **追蹤前次會議 Action Items**（見 1.5）
- [ ] **驗證 repo 清單完整性**（見 1.2）
- [ ] 執行報表更新腳本
- [ ] 將報表上傳至公司 Wiki / Notion / SharePoint
- [ ] 在會議邀請中附上報表連結
- [ ] 各部門負責人已閱讀報表並準備：
  - 重點更新
  - 跨部門需求
  - 阻礙項目

### 1.4 Infrastructure Team 系統狀態報告（會前必執行）

**目的**：每次會議開始前，Infrastructure Team (Opskova) 需先報告系統運行狀況，確保所有人了解基礎設施現況。

**報告時機**：會議正式開始前，在所有部門報告之前

**報告內容**：

#### 1.4.1 各主機運作狀況

針對每台主機（如 BearQadris）報告：

| 項目 | 檢查內容 |
|------|----------|
| 主機名稱 | 主機識別名稱 |
| 運行狀態 | 正常 / 異常 / 維護中 |
| CPU 使用率 | 目前負載百分比 |
| 記憶體使用率 | 目前使用百分比 |
| 磁碟使用率 | 各分區使用百分比 |
| 網路狀態 | 連線正常 / 異常 |
| 最近重開機時間 | uptime |
| 異常事件 | 近期是否有異常紀錄 |

**檢查指令範例**：
```bash
# 系統基本狀態
uptime
free -h
df -h
top -bn1 | head -20

# 網路狀態
ping -c 3 8.8.8.8
```

#### 1.4.2 Docker 運行狀況（如有）

| 項目 | 檢查內容 |
|------|----------|
| Docker 服務狀態 | 運行中 / 停止 |
| 運行中容器數量 | 容器清單與狀態 |
| 容器健康狀態 | healthy / unhealthy |
| 資源使用 | CPU / Memory 使用情況 |
| 近期異常 | 容器重啟 / 錯誤日誌 |

**檢查指令範例**：
```bash
# Docker 狀態
docker ps -a
docker stats --no-stream
docker system df
```

#### 1.4.3 專案資料夾管理（如有）

| 項目 | 檢查內容 |
|------|----------|
| 專案資料夾清單 | 目前管理的專案目錄 |
| Git 同步狀態 | 各 repo 是否與 remote 同步 |
| 磁碟空間 | 專案目錄佔用空間 |
| 權限狀態 | 資料夾權限是否正確 |

**檢查指令範例**：
```bash
# 專案資料夾狀態
ls -la /home/chubear/ | grep -E "^d"
du -sh /home/chubear/*/ 2>/dev/null | sort -h | tail -20
```

#### 1.4.4 報告格式範例

```
🔧 Infrastructure Team 系統狀態報告

📍 主機：BearQadris
├── 運行狀態：✅ 正常
├── Uptime：XX days
├── CPU：XX%
├── Memory：XX% (XX GB / XX GB)
├── Disk：XX% (XX GB / XX GB)
└── 網路：✅ 正常

🐳 Docker 狀態：
├── 服務狀態：✅ 運行中
├── 運行容器：X 個
└── 異常容器：無

📁 專案資料夾：
├── 管理專案數：XX 個
├── Git 同步：✅ 全部同步
└── 磁碟佔用：XX GB

⚠️ 近期異常事件：
├── （無異常 / 列出異常事件）
```

---

### 1.5 前次會議 Action Items 追蹤（會前必執行）

**目的**：確保前幾次會議的待辦事項有持續追蹤，避免任務遺漏或延宕。

**追蹤範圍**：預設追蹤最近 3 次會議的 Action Items（可依需求調整）

#### 1.5.1 自動追蹤流程

Copilot 會議小幫手會自動執行：

1. **掃描近期會議資料夾**：
   - 讀取 `meeting/` 下最近 3 個會議資料夾
   - 尋找各資料夾中的 `action_items.md` 或從 `meeting_minutes.md` 提取 Action Items

2. **彙整未完成項目**：
   - 收集所有狀態為 ⬜ 未開始、⏳ 進行中、🔄 延期 的項目
   - 標註逾期項目（Due Date 已過但未完成）

3. **產生追蹤報告**：
   - 輸出至會議資料夾 `action_items_followup.md`

#### 1.5.2 追蹤報告格式

```markdown
# 📋 前次會議 Action Items 追蹤報告

> 產生時間：{{YYYY-MM-DD HH:MM}}
> 追蹤範圍：最近 3 次會議

---

## 🔴 逾期項目（需優先處理）

| # | 來源會議 | Action Item | Owner | 部門 | 原 Due Date | 逾期天數 | Status |
|---|----------|-------------|-------|------|-------------|----------|--------|
| 1 | 12/10 進度會議 | {{項目}} | {{Name}} | {{Dept}} | 12/12 | 3 天 | ⏳ 進行中 |

---

## 🟡 進行中項目

| # | 來源會議 | Action Item | Owner | 部門 | Due Date | Status | 備註 |
|---|----------|-------------|-------|------|----------|--------|------|
| 1 | 12/12 進度會議 | {{項目}} | {{Name}} | {{Dept}} | 12/18 | ⏳ 進行中 | |

---

## ⬜ 未開始項目

| # | 來源會議 | Action Item | Owner | 部門 | Due Date | Status |
|---|----------|-------------|-------|------|----------|--------|
| 1 | 12/12 進度會議 | {{項目}} | {{Name}} | {{Dept}} | 12/20 | ⬜ 未開始 |

---

## ✅ 已完成項目（本週）

| # | 來源會議 | Action Item | Owner | 完成日期 |
|---|----------|-------------|-------|----------|
| 1 | 12/10 進度會議 | {{項目}} | {{Name}} | 12/14 |

---

## 📊 統計摘要

| 狀態 | 數量 |
|------|------|
| 🔴 逾期 | X |
| 🟡 進行中 | X |
| ⬜ 未開始 | X |
| ✅ 已完成 | X |
| **總計** | **X** |
```

#### 1.5.3 會議中追蹤流程

1. **會議開始時**：先報告 Action Items 追蹤狀況
2. **逾期項目**：要求 Owner 說明原因並更新預計完成日
3. **進行中項目**：確認進度是否如預期
4. **新 Action Items**：本次會議產生的新項目

#### 1.5.4 檢查指令範例

```bash
# 列出最近的會議資料夾
ls -d meeting/meeting_* | sort -r | head -5

# 搜尋未完成的 Action Items
grep -r "⬜\|⏳\|🔄" meeting/meeting_*/action_items.md 2>/dev/null
grep -r "⬜\|⏳\|🔄" meeting/meeting_*/meeting_minutes.md 2>/dev/null
```

---

## 2. 會議類型

### 2.1 進度追蹤會議（例行）

**目的**：追蹤各部門工作進度、識別問題、協調跨部門議題

**議程**：
1. 各部門報告
   - 近期完成事項
   - 進行中事項
   - 問題 / 風險
   - 待辦事項
2. 跨部門協助需求收斂
3. 各部門提出解決方案
4. 臨時動議

### 2.2 新專案會議

**目的**：評估新專案可行性、確定範圍與負責人

**議程**：
1. CEO / 發起人提出想法
   - 商業目標
   - 成功指標 (KPI)
   - 預估時程與優先順序
2. 各部門回應
   - 對本部門的影響
   - 所需資源 / 人力
   - 風險與前置條件
3. 跨部門討論
   - 初步範圍 (Scope)
   - 大致 Milestone
   - 指定專案負責人 (PM / Owner)
4. 會議總結
   - 是否立案
   - 下一步動作

---

## 3. 會議紀錄規範

### 3.1 紀錄模板位置

- 會議紀錄：`meeting/meeting_templates/meeting_minutes.md`
- 行動項目：`meeting/meeting_templates/action_items.md`

### 3.2 會議檔案存放規範

**資料夾結構：**
```
meeting/
├── meeting_20251204_progress_1/    # 2025/12/04 第1次進度追蹤會議
│   ├── meeting_minutes.md          # 會議紀錄
│   └── action_items.md             # 行動項目
├── meeting_20251204_project_1/     # 2025/12/04 第1次新專案會議
│   ├── meeting_minutes.md
│   └── action_items.md
└── meeting_templates/              # 模板（保持不變）
    ├── meeting_minutes.md
    └── action_items.md
```

**資料夾命名規則：**
- 格式：`meeting_yyyymmdd_{type}_{seq}`
- `type`：`progress`（進度追蹤）或 `project`（新專案）
- `seq`：當日同類型會議的次別，從 1 開始

### 3.3 紀錄要求

- **會中**：紀錄人直接編輯會議紀錄模板
- **會後 24 小時內**：
  - 完成會議紀錄並上傳
  - Action Item Owner 在對應 repo 建立 Issue
  - 將 Issue 連結補回會議紀錄

### 3.4 行動項目 (Action Items) 規範

每個 Action Item 必須包含：
- 具體工作內容（動詞開頭）
- Owner（實際負責人，非部門名稱）
- Due Date（具體日期）
- Status（⬜ 未開始 / ⏳ 進行中 / ✅ 完成）
- 相關連結（Issue / PR / Doc）

### 3.5 Issue 發布建議（OmniQ 自動分析）

會議結束時，OmniQ 會自動分析 Action Items 並提供 Issue 發布建議，協助 CEO 決定如何整合發布 Issue。

#### 3.5.1 分析原則

1. **整合相關任務**：高度相關的 Action Items 應整合為單一 Issue，避免碎片化
2. **識別依賴關係**：分析 Action Items 間的執行順序與依賴
3. **指定目標 Repo**：根據任務性質指定應發布的 Repo
4. **排除非程式任務**：會議安排、口頭確認等不需發 Issue

#### 3.5.2 Issue 關係類型

| 關係類型 | 說明 | GitHub 語法 |
|----------|------|-------------|
| **Parent** | 主任務，包含多個子任務 | 使用 Task List：`- [ ] #123` |
| **Blocked by** | 被其他 Issue 阻擋，需等待完成 | `Blocked by #123` 或 `Depends on #123` |
| **Blocks** | 阻擋其他 Issue | `Blocks #456` |
| **Related** | 相關但無依賴關係 | `Related to #123` |

#### 3.5.3 建議格式

OmniQ 在會議紀錄中新增以下章節：

```markdown
## 📌 Issue 發布建議

> OmniQ 整合分析：將相關 Action Items 合併發布為 Issue，減少碎片化。

### 建議 Issue 清單

| Issue | 整合項目 | Repo | Owner | 關係 |
|-------|----------|------|-------|------|
| Issue A | #1 + #2 | RepoName | Team | Parent of B |
| Issue B | #3 | RepoName | Team | Blocked by A |
| Issue C | #4 | RepoName | Team | - |
| *(不發 Issue)* | #5 | - | - | 非程式任務 |

### Issue 依賴關係圖

​```
Issue A (#1+#2)
    │
    ├──► Issue B (#3)  [Blocked by A]
    │
    └──► Issue C (#4)  [Related]
​```

### 各 Issue 建議內容

#### Issue A: [標題]

- **Repo**: `QadrisCorp/RepoName`
- **整合項目**: #1, #2
- **Owner**: Team Name
- **關係**: Parent of Issue B
- **建議 Labels**: `enhancement`, `priority:high`

**建議 Issue Body**:
​```markdown
## 概述
[整合的任務說明]

## 子任務
- [ ] 任務 1 內容
- [ ] 任務 2 內容

## 驗收條件
- [ ] 條件 1
- [ ] 條件 2

## 相關資訊
- 會議紀錄: meeting/meeting_yyyymmdd_type_seq/meeting_minutes.md
​```
```

#### 3.5.4 依賴關係判斷規則

| 情境 | 關係類型 | 範例 |
|------|----------|------|
| B 需要 A 的產出才能開始 | B **Blocked by** A | Schema 定義 → 架構文件 |
| A 包含多個可拆分的子任務 | A 為 **Parent** | 大功能拆分為多個子任務 |
| A 和 B 相關但可平行進行 | **Related** | 同專案不同模組 |
| A 和 B 完全獨立 | 無關係 | 不同專案的任務 |

#### 3.5.5 Repo 指定規則

| 任務類型 | 建議 Repo |
|----------|-----------|
| 架構設計、策略邏輯 | 對應專案 Repo（如 FactorBackTest） |
| 資料 Schema 定義 | 對應專案 Repo 或 Data 相關 Repo |
| 產品規格更新 | QadrisFactorBase 或對應產品 Repo |
| 跨專案協調 | QadrisCorp（公司層級追蹤） |
| 基礎設施 | InfraDevOps |

#### 3.5.6 不發 Issue 的情況

以下類型的 Action Items 不需發布為 Issue：
- 會議安排（如：召開下次會議）
- 口頭確認或溝通任務
- 已有對應 Issue 的追蹤項目
- 一次性行政任務

---

## 4. 會議參與者建議

| 會議類型 | 參與者 |
|----------|--------|
| 部門內部檢視 | 部門成員 |
| 全公司進度追蹤 | 全部門主管 + CEO |
| 新專案會議 | 相關部門 + CEO |

---

## 5. Copilot 協助指引

當使用者要求 Copilot 協助會議相關事項時：

1. **準備會議**：
   - 提醒執行報表更新腳本
   - 提供會議模板位置
   - 建立會議資料夾（格式：`meeting_yyyymmdd_{type}_{seq}`）

2. **會前準備完成後**：
   - 邀請會議參與者打招呼
   - 確認出席名單
   - 記錄參與者資訊

3. **建立會議紀錄**：
   - 讀取 `meeting/meeting_templates/meeting_minutes.md`
   - 依照模板格式產生內容
   - **存放至對應的會議資料夾**

4. **建立行動項目**：
   - 讀取 `meeting/meeting_templates/action_items.md`
   - 確保每個 Action Item 都有 Owner 和 Due Date
   - **存放至對應的會議資料夾**

5. **會後追蹤**：
   - 提醒建立對應 Issue
   - 協助更新 Action Items 狀態

---

## 6. 相關檔案

| 檔案 | 路徑 |
|------|------|
| 報表產生器 | `reports/generate_report.py` |
| 狀態收集器 | `reports/collect_repo_status.py` |
| 會議紀錄模板 | `meeting/meeting_templates/meeting_minutes.md` |
| 行動項目模板 | `meeting/meeting_templates/action_items.md` |

---

*最後更新：2025-12*
