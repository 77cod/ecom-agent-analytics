# 《智能电商运营分析平台 从0到1完全学习手册》

> 一本 100% 基于真实项目的工程化学习教程 —— 从环境搭建到多智能体协作系统，手把手带你从 0 到 1 掌握全栈 AI 应用开发。

## 这本书能让你学到什么

- 7 个 AI Agent 如何协作完成复杂的运营分析任务
- React 19 + TypeScript + Ant Design 5 的企业级前端开发
- FastAPI + LangGraph 的后端架构设计与异步编程
- ECharts 交互式数据可视化与 SSE 流式推送
- PostgreSQL + Redis + Milvus 多数据库协同
- Docker Compose 一键部署微服务基础设施

## 📖 书籍目录

| 章节 | 文件 | 核心内容 | 适合谁 |
|------|------|----------|--------|
| 前言 | [00-前言.md](docs/00-前言.md) | 项目简介、学习路线、前置准备 | 所有人 |
| 第1章 | [01-项目全貌速览.md](docs/01-项目全貌速览.md) | 5分钟跑起来、技术栈全览、目录结构 | 新手入门 |
| 第2章 | [02-开发环境搭建全攻略.md](docs/02-开发环境搭建全攻略.md) | 工具安装、Docker启动、API配置 | 新手入门 |
| 第3章 | [03-项目架构与核心设计原理.md](docs/03-项目架构与核心设计原理.md) | 分层架构、Agent状态机、SSE原理 | 有基础者 |
| 第4章 | [04-核心代码逐行精讲.md](docs/04-核心代码逐行精讲.md) | 逐文件逐行精读后端+前端代码 | 所有人 |
| 第5章 | [05-项目调试与排错指南.md](docs/05-项目调试与排错指南.md) | 调试工具、日志排查、15+常见报错 | 遇到问题者 |
| 第6章 | [06-项目优化与功能扩展实战.md](docs/06-项目优化与功能扩展实战.md) | 添加新行业、新图表、性能优化 | 想扩展者 |
| 第7章 | [07-全流程复盘与结业指南.md](docs/07-全流程复盘与结业指南.md) | 知识体系复盘、实战任务、面试题 | 所有人 |

## 📚 附录

| 附录 | 文件 | 内容 |
|------|------|------|
| 术语表 | [appendix/术语表.md](docs/appendix/术语表.md) | 全书专业术语的中英文对照和解释 |
| 命令速查 | [appendix/常用命令速查手册.md](docs/appendix/常用命令速查手册.md) | Docker/Git/Python/Node 常用命令 |
| 报错排雷 | [appendix/常见报错排雷大全.md](docs/appendix/常见报错排雷大全.md) | 15+ 个真实错误及解决方案 |
| Git规范 | [appendix/Git标准化规范手册.md](docs/appendix/Git标准化规范手册.md) | 分支策略、提交规范、冲突解决 |

## 🚀 快速开始

### 30 秒体验

```bash
# 1. 启动基础设施
docker compose up -d

# 2. 配置 API Key
echo 'DASHSCOPE_API_KEY=你的key' > backend/.env

# 3. 启动后端
cd backend && pip install -r requirements.txt
python -m uvicorn app.app_main:app --reload --port 8000

# 4. 启动前端（新终端）
cd frontend && npm install && npm run dev

# 5. 打开浏览器
# http://localhost:5173
```

详细步骤见 [第 1 章](docs/01-项目全貌速览.md) 和 [第 2 章](docs/02-开发环境搭建全攻略.md)。

## 🎯 这个项目是做什么的

一句话：**选行业 → 输入运营分析问题 → 7 个 AI Agent 自动协作 → 生成分析报告 + 图表 + 运营看板**。

```
用户："分析美妆精华液本月销售趋势"
    │
    ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ ① Architect  │→│ ② DataQueryer│→│ ③ Analyst    │
│   分析架构师  │  │   数据查询员  │  │ + CodeWizard │
│   拆解问题   │  │   查数据库   │  │   分析+图表  │
└──────────────┘  └──────────────┘  └──────────────┘
                                            │
                    ┌───────────────────────┘
                    ▼
┌──────────────┐  ┌──────────────┐
│ ⑤ Critic    │←│ ④ Writer     │
│   毒舌审核   │  │   撰写报告   │
│   打分修订   │  │   整合全文   │
└──────────────┘  └──────────────┘
```

## 💡 怎么读这本书

- **想快速体验**：读第 1 章，30 分钟跑起来
- **想彻底搞懂**：按顺序从第 1 章读到第 7 章
- **遇到了 bug**：直接翻第 5 章和附录"报错排雷大全"
- **想加新功能**：看第 6 章的实战案例
- **准备面试**：看第 7 章的面试题

每一章都包含：**知识讲解 → 真实代码 → 动手操作 → 避坑提醒 → 要点回顾**。

## 📂 项目仓库

- GitHub: [https://github.com/77cod/ecom-agent-analytics](https://github.com/77cod/ecom-agent-analytics)

## 🔧 在 GitHub Pages 上看这本书

### 方法一：直接浏览（推荐）

所有章节都是标准 Markdown 文件，在 GitHub 上点击即可直接阅读，GitHub 会自动渲染格式。

### 方法二：部署为网页

```bash
# 安装 docsify（一个轻量的文档站点生成器）
npm install -g docsify-cli

# 在项目根目录执行
docsify init ./docs
docsify serve ./docs

# 打开 http://localhost:3000 即可看到书籍网站
```

或者使用 GitHub Pages：
1. 在仓库 Settings → Pages 中
2. Source 选择 `main` 分支，文件夹选 `/docs`
3. 保存后访问 `https://77cod.github.io/ecom-agent-analytics/`

---

> 翻开 [第 1 章](docs/01-项目全貌速览.md)，开始你的学习之旅！
