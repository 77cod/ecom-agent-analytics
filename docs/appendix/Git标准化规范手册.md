# Git 标准化规范手册

> 智能电商运营分析平台项目的 Git 操作规范，覆盖分支命名、提交格式、撤销操作、冲突解决和最佳实践。

---

## 一、分支命名规范

### 分支类型

| 分支类型 | 命名格式 | 用途 | 示例 |
|---------|---------|------|------|
| 主分支 | `main` 或 `master` | 稳定可发布的代码，只接受合并，不直接提交 | `main` |
| 开发分支 | `develop` | 集成各个功能分支，日常开发基准（视团队规模可选） | `develop` |
| 功能分支 | `feature/<功能简述>` | 开发新功能模块 | `feature/agent-dashboard` |
| 修复分支 | `fix/<问题简述>` | 修复 Bug | `fix/401-token-expiry` |
| 文档分支 | `docs/<文档简述>` | 编写或更新文档 | `docs/api-reference` |
| 重构分支 | `refactor/<模块名>` | 代码重构，不改变功能 | `refactor/agent-state` |
| 测试分支 | `test/<测试简述>` | 编写测试用例 | `test/planner-agent` |
| 发布分支 | `release/<版本号>` | 准备发布前的最终修复和版本号更新 | `release/v1.2.0` |
| 热修复分支 | `hotfix/<问题简述>` | 从 main 分支紧急修复线上问题 | `hotfix/login-crash` |

### 命名原则

- 全部小写，单词间用连字符 `-` 连接，不使用下划线或驼峰
- 简述部分用英文，保持简洁（3-5 个单词为宜）
- 包含任务编号时加在简述前：`feature/AG-42-add-search-filter`

### 操作示例

```bash
# 从 main 创建功能分支
git checkout main
git pull origin main
git checkout -b feature/agent-dashboard

# 从 main 创建热修复分支
git checkout main
git checkout -b hotfix/login-crash

# 完成功能后删除本地分支
git branch -d feature/agent-dashboard
```

---

## 二、Commit Message 格式

### 标准格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

### 各部分说明

| 部分 | 是否必填 | 说明 |
|------|---------|------|
| type | 是 | 提交类型，从下表中选取 |
| scope | 否 | 影响范围（模块/文件），小写英文 |
| subject | 是 | 简短描述（50 字以内），中文，不加句号 |
| body | 否 | 详细描述（每行 72 字以内），说明修改原因和内容 |
| footer | 否 | 关联 Issue 编号或破坏性变更说明 |

### Type 类型表

| Type | 全称 | 说明 | 示例 |
|------|------|------|------|
| `feat` | Feature | 新增功能 | `feat(agent): 添加 PlannerAgent 多步规划能力` |
| `fix` | Bug Fix | 修复缺陷 | `fix(auth): 修复 JWT Token 过期未自动刷新的问题` |
| `docs` | Documentation | 文档变更 | `docs(api): 补充分析接口的请求示例` |
| `refactor` | Refactor | 代码重构（不改变功能也不修 Bug） | `refactor(state): 将 AgentState 提取到公共模块` |
| `test` | Test | 添加或修改测试 | `test(planner): 添加提纲生成逻辑的单元测试` |
| `chore` | Chore | 构建流程或工具变更 | `chore(docker): 升级 Python 基础镜像到 3.12` |
| `style` | Style | 代码风格调整（空格/分号/引号等，不影响逻辑） | `style(frontend): 统一使用单引号` |
| `perf` | Performance | 性能优化 | `perf(search): 使用 Redis 缓存搜索结果减少 API 调用` |
| `ci` | CI | 持续集成配置变更 | `ci(github): 添加 PR 自动测试流水线` |
| `build` | Build | 构建系统或外部依赖变更 | `build(npm): 升级 Vite 到 5.0` |
| `revert` | Revert | 回退之前的提交 | `revert: 回退 feat(agent): 添加 PlannerAgent` |

### 提交示例

```bash
# 标准功能提交
git commit -m "feat(agent): 添加 SearcherAgent 实现多源信息搜索

支持同时搜索内部数据库和外部 API，返回聚合结果。
搜索结果会写入 AgentState.search_results 字段。"

# Bug 修复提交
git commit -m "fix(frontend): 修复 ECharts 图表容器卸载后未 dispose 导致内存泄漏

在 Chart 组件的 useEffect 返回函数中添加了 chart.dispose() 调用。"

# 文档提交
git commit -m "docs(readme): 更新 Docker 部署步骤，补充 Windows 注意事项"

# 包含破坏性变更
git commit -m "refactor(api): 重构分析接口的请求体结构

BREAKING CHANGE: depth 参数从字符串改为枚举，
客户端需更新请求格式为 \"basic\" | \"standard\" | \"deep\"。"
```

---

## 三、.gitignore 要点

本项目推荐的基础 `.gitignore` 配置：

```gitignore
# --- Python ---
__pycache__/
*.py[cod]
*.so
*.egg-info/
dist/
build/
.eggs/
*.egg
.venv
venv/
env/

# --- Node ---
node_modules/
dist/
.vite/

# --- Environment ---
.env
.env.local
.env.*.local
*.pem
*.key

# --- IDE ---
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store
Thumbs.db

# --- Docker ---
docker-compose.override.yml

# --- Database ---
*.db
*.sqlite3
data/postgres/
data/redis/

# --- Logs ---
logs/
*.log
npm-debug.log*

# --- Test ---
.coverage
htmlcov/
.pytest_cache/
```

---

## 四、撤销操作指南

### 场景 1：撤销工作区未暂存的改动

```bash
# 撤销单个文件
git checkout -- <文件名>

# 撤销所有改动（危险，不可恢复）
git checkout -- .
```

### 场景 2：撤销暂存区（git add 之后）

```bash
# 撤销单个文件的暂存
git reset HEAD <文件名>

# 撤销所有暂存，文件改动保留在工作区
git reset HEAD
```

### 场景 3：撤销最近一次提交（保留改动）

```bash
# 撤销 commit，改动回到暂存区
git reset --soft HEAD~1

# 撤销 commit，改动回到工作区（未暂存）
git reset --mixed HEAD~1
```

### 场景 4：彻底丢弃最近一次提交

```bash
# 撤销 commit 并丢弃所有改动（危险，不可恢复）
git reset --hard HEAD~1
```

> **注意：** 如果已推送到远程，永远不要使用 `git reset --hard` 来撤销已推送的提交，这会影响其他协作者。请使用 `git revert`。

### 场景 5：安全的远程撤销（git revert）

```bash
# 创建一个反向提交来撤销指定提交
git revert <commit-hash>

# 撤销最近一次提交（不改变历史，生成新提交）
git revert HEAD
```

### 场景 6：修改最后一次提交信息

```bash
# 修正提交信息（未推送时）
git commit --amend -m "新的提交信息"

# 追加遗漏的文件到上一次提交
git add 遗漏的文件
git commit --amend --no-edit
```

---

## 五、合并冲突解决步骤

### 冲突产生场景

当两个分支对同一文件的同一行做了不同修改，合并时 Git 无法自动决定保留哪个版本。

### 冲突标记识别

```
<<<<<<< HEAD
当前分支（你的改动）
=======
要合并进来的分支（他人的改动）
>>>>>>> feature/other-branch
```

### 逐步解决流程

```bash
# 1. 确保当前分支代码是最新的
git checkout main
git pull origin main

# 2. 尝试合并目标分支
git merge feature/agent-dashboard

# 3. Git 提示冲突
# Auto-merging src/pages/Analysis.tsx
# CONFLICT (content): Merge conflict in src/pages/Analysis.tsx
# Automatic merge failed; fix conflicts and then commit the result.

# 4. 查看所有冲突文件
git status

# 5. 逐个打开冲突文件，手动编辑
# 在 VS Code 中，冲突区域会有彩色标记，可以点击按钮选择：
#   - Accept Current Change（保留当前分支的版本）
#   - Accept Incoming Change（采用合并分支的版本）
#   - Accept Both Changes（两者都保留）

# 6. 编辑完成后，标记文件为已解决
git add src/pages/Analysis.tsx

# 7. 所有冲突解决后，完成合并
git commit -m "merge: 合并 feature/agent-dashboard 分支并解决冲突"

# 8. 推送到远程
git push origin main
```

### 不想现在解决冲突时的做法

```bash
# 中止本次合并，回到合并前的状态
git merge --abort
```

### 在 VS Code 中解决冲突（推荐）

1. 打开 Source Control 面板（Ctrl+Shift+G）
2. 冲突文件会高亮显示，文件旁边有红色 `C` 标记
3. 点击文件进入编辑器，冲突区域上方会出现三个按钮：
   - **Accept Current Change** -- 采用当前分支的版本
   - **Accept Incoming Change** -- 采用合并进来的版本
   - **Accept Both Changes** -- 两段代码都保留，你的在前
4. 全部解决后点击 Stage Changes（+ 号），然后正常 commit

---

## 六、最佳实践

### 1. 频繁提交，原子化

- 每个提交只做一件事：一个功能、一个修复、一个重构
- 不要在一个提交中混入不相关的改动
- 每完成一个逻辑单元就提交一次，便于回溯和代码审查

```bash
# 好的做法
git commit -m "feat: 添加登录表单组件"
git commit -m "feat: 添加登录 API 调用逻辑"
git commit -m "feat: 添加 JWT Token 存储和自动附加"

# 不好的做法
git commit -m "完成登录功能和一些其他小改动"
```

### 2. 提交前自查

```bash
# 查看本次改动了哪些文件
git status

# 对比暂存区和最后一次提交的差异
git diff --staged

# 逐行确认改动，避免误提交调试代码、API Key、临时文件
```

### 3. 编写有意义的提交信息

- Subject 行回答"这个提交做了什么"
- Body 回答"为什么这样做"和"有什么需要注意的"
- 使用祈使语气的动词（添加、修复、重构），而非过去式

```bash
# 好的提交信息
feat(agent): 添加搜索结果去重逻辑

重复的搜索结果浪费 Token 且干扰模型判断。
采用 URL 哈希+L2 文本相似度双重去重策略，
相似度阈值设为 0.85。

# 差的提交信息
fix bug
update code
wip
```

### 4. 推送前检查

```bash
# 查看本地未推送的提交
git log origin/main..HEAD

# 确保没有不合规的提交信息
git log --oneline -5

# 确认没有提交敏感文件（.env、密钥等）
git diff --name-only origin/main..HEAD
```

### 5. 保持分支整洁

```bash
# 定期从 main 同步最新代码到功能分支
git checkout feature/my-branch
git merge main
# 或使用 rebase 保持线性历史
git rebase main

# 功能完成后及时删除本地分支
git branch -d feature/my-branch

# 清理远程已删除的分支引用
git remote prune origin
```

### 6. 使用 rebase 保持提交历史整洁（可选进阶）

```bash
# 将最近 3 个提交合并为一个
git rebase -i HEAD~3

# 在交互式编辑器中：
# pick abc1234 第一个提交
# squash def5678 第二个提交  -> 合并到第一个
# squash ghi9012 第三个提交  -> 合并到第一个
# 保存退出后编辑合并后的提交信息

# 注意：不要对已推送到远程的提交做 rebase
```

### 7. 代码审查清单

在提交 Pull Request 前，逐项确认：

- [ ] 分支命名符合 `feature/xxx`、`fix/xxx` 等规范
- [ ] 提交信息格式正确，type 和描述清晰
- [ ] 没有提交 `.env`、`node_modules`、`__pycache__` 等敏感或自动生成文件
- [ ] 所有代码通过 lint 检查（ESLint、ruff）
- [ ] TypeScript 类型检查通过（`npx tsc --noEmit`）
- [ ] Python 类型检查通过（`mypy app/`）
- [ ] 相关测试已添加且全部通过（`pytest` / `npm test`）
- [ ] 没有遗留的 `console.log` 或 `print()` 调试代码
- [ ] API 变更已同步更新 FastAPI 自动生成的文档

---

## 七、常见工作流速查

### 开始一个新功能

```bash
git checkout main
git pull origin main
git checkout -b feature/new-feature
# ... 编码 ...
git add .
git commit -m "feat(scope): 描述"
git push origin feature/new-feature
# 去 GitHub/GitLab 创建 Pull Request
```

### 修复一个 Bug

```bash
git checkout main
git pull origin main
git checkout -b fix/bug-description
# ... 修复 ...
git add .
git commit -m "fix(scope): 描述"
git push origin fix/bug-description
```

### 紧急线上修复

```bash
git checkout main
git pull origin main
git checkout -b hotfix/critical-fix
# ... 修复 ...
git add .
git commit -m "fix: 描述"

# 合并到 main
git checkout main
git merge hotfix/critical-fix
git push origin main

# 如果还有 develop 分支，也要同步合并
git checkout develop
git merge main
git push origin develop
```

### 同步其他人的更新

```bash
# 方式 1：产生合并提交
git checkout main
git pull origin main

# 方式 2：保持线性历史（推荐）
git checkout main
git pull --rebase origin main
```
