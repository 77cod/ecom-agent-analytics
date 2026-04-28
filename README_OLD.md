# 智能电商运营分析平台

基于多智能体协作（Multi-Agent）的电商运营深度研究平台。用户选择行业后输入问题，7 个 AI Agent 协作完成从问题分析、数据查询、可视化到报告生成的全流程，最终输出可交互的运营看板。

## 系统架构

```
┌─────────────┐     SSE 流式     ┌──────────────────────────────────┐
│   React 19  │ ◄────────────── │        FastAPI (Python)          │
│  Ant Design │                 │                                  │
│   ECharts   │                 │  ┌────────────────────────────┐  │
│   Valtio    │                 │  │   DeepResearch Graph       │  │
└──────┬──────┘                 │  │                            │  │
       │                        │  │ Plan → Query → Analyze     │  │
       │ 行业选择                │  │   → Write → Review → Done │  │
       │ fashion/beauty/        │  │                            │  │
       │ digital/food           │  └────────────┬───────────────┘  │
       │                        │               │                  │
       ▼                        │  ┌────────────▼───────────────┐  │
┌──────────────┐                │  │      7 个 AI Agent          │  │
│  运营看板     │                │  │  ChiefArchitect (规划)      │  │
│  KPI + 图表  │                │  │  DataQueryer (数据查询)     │  │
│  竞品/达人   │                │  │  DataAnalyst (数据分析)     │  │
└──────────────┘                │  │  CodeWizard (代码+图表)     │  │
                                │  │  LeadWriter (报告撰写)      │  │
                                │  │  CriticMaster (对抗审核)    │  │
                                │  │  DeepScout (网络搜索)       │  │
                                │  └────────────────────────────┘  │
                                │                                  │
                                │  PostgreSQL + Redis + Milvus     │
                                └──────────────────────────────────┘
```

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | React 19 / TypeScript / Vite / Ant Design 5 / ECharts / Valtio |
| 后端 | FastAPI / LangGraph / SQLAlchemy / Python 3.10+ |
| 数据库 | PostgreSQL 15 / Redis 7 / Milvus 2.3 (向量) / Elasticsearch 8 |
| AI | 阿里百炼 DashScope (DeepSeek-V3.2 / Qwen-Plus / Qwen-Max) |
| 基础设施 | Docker Compose |

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/77cod/ecom-agent-analytics.git
cd ecom-agent-analytics
```

### 2. 启动基础设施

```bash
docker compose up -d
```

这会在后台启动 PostgreSQL、Redis、Milvus、Elasticsearch、MinIO、etcd。

### 3. 配置环境变量

**后端** (`backend/.env`)：
```env
DASHSCOPE_API_KEY=your-dashscope-api-key
BOCHA_API_KEY=your-bocha-search-key
DATABASE_URL=postgresql://postgres:postgres123@localhost:5432/industry_assistant
```

**前端** (`frontend/.env`)：
```env
VITE_TITLE=智能电商运营分析平台
VITE_API_BASE=http://localhost:8000/
```

### 4. 安装依赖

```bash
# 后端
cd backend
pip install -r requirements.txt

# 前端
cd frontend
npm install
```

### 5. 启动服务

```bash
# 终端 1 - 后端
cd backend
python -m uvicorn app.app_main:app --reload --port 8000

# 终端 2 - 前端
cd frontend
npm run dev
```

访问 `http://localhost:5173` 即可使用。

## Agent 流水线

```
用户输入 "分析美妆精华液销售趋势"
    │
    ▼
┌─────────────────┐
│ ChiefArchitect   │  分析问题 → 生成分析维度 + 研究假设
│ (deepseek-v3.2)  │  输出: outline, hypotheses, key_entities
└────────┬────────┘
         ▼
┌─────────────────┐
│ DataQueryer      │  根据大纲查询 mock 电商数据
│ (qwen-plus)      │  按行业自动切换数据集
└────────┬────────┘
         ▼
┌─────────────────┐
│ DataAnalyst      │  提取结构化指标 (GMV/ROI/转化率/好评率)
│ + CodeWizard     │  生成 Python 代码 → 执行 → ECharts + matplotlib 图表
│ (deepseek-v3.2)  │
└────────┬────────┘
         ▼
┌─────────────────┐
│ LeadWriter       │  逐章节撰写 Markdown 运营分析报告
│ (deepseek-v3.2)  │
└────────┬────────┘
         ▼
┌─────────────────┐
│ CriticMaster     │  对抗式审核: 幻觉检测、逻辑校验、证据核实
│ (deepseek-v3.2)  │  评分 < 6.0 → 打回修订 (最多 3 轮)
└────────┬────────┘
         ▼
    SSE 流式输出 → 前端渲染 → 运营看板
```

## 四个行业与 Mock 数据

| 行业 | 品牌 | 品类 | 数据集 |
|------|------|------|--------|
| 服装鞋包 | 夏日轻盈 | 防晒衣/冰袖/渔夫帽 | `ecommerce_mock_data.py` |
| 美妆个护 | 兰芮 L'ANRAY | 精华液/面霜/面膜 | `ecommerce_mock_data_beauty.py` |
| 数码家电 | 聆韵 LINGVIBE | TWS降噪耳机/充电宝 | `ecommerce_mock_data_digital.py` |
| 食品饮料 | 茶屿 CHAYU | 冷泡茶/茶礼盒/养生茶 | `ecommerce_mock_data_food.py` |

每个数据集包含：10 商品 + 月度销售 + 100 订单 + 20 评价 + 7 达人 + 价格监控 + 热词趋势 + 退货记录，且埋有预设的分析故事线（竞品反超、达人ROI差异、品类趋势等）。

## API 概览

| 端点 | 用途 | 响应 |
|------|------|------|
| `POST /auth/login` | 用户登录 | JWT Token |
| `GET /sessions` | 会话列表 | Session[] |
| `POST /sessions/:id/messages` | 发送消息 | 流式 SSE |
| `POST /research/stream` | 深度研究 | SSE 流式 |
| `POST /research/resume/:id` | 恢复研究 | SSE 流式 |
| `POST /research/cancel/:id` | 取消研究 | JSON |
| `GET /research/checkpoint/:id` | 检查点信息 | JSON |
| `GET /knowledge-bases` | 知识库列表 | KnowledgeBase[] |
| `POST /knowledge-bases/:id/documents` | 上传文档 | JSON |
| `GET /news/list` | 行业资讯 | 分页列表 |
| `GET /database/tables` | 数据库表列表 | TableInfo[] |
| `POST /database/text2sql` | 自然语言查表 | SQL + Data |
| `POST /chat/completion` | RAG 对话 | SSE 流式 |

## 目录结构

```
├── backend/
│   └── app/
│       ├── app_main.py               # FastAPI 入口
│       ├── config/                   # 行业/LLM 配置
│       ├── core/                     # 数据库、Redis、鉴权
│       ├── models/                   # SQLAlchemy ORM
│       ├── router/                   # 11 个路由模块
│       ├── schemas/                  # Pydantic 模型
│       ├── service/
│       │   └── deep_research_v2/     # ★ 多智能体核心
│       │       ├── agents/           # 7 个 Agent
│       │       ├── state.py          # 全局状态
│       │       ├── graph.py          # 工作流编排
│       │       └── service.py        # SSE 服务
│       └── scripts/                  # 测试/种子数据
├── frontend/
│   └── src/
│       ├── api/                      # API 层
│       ├── components/               # Chart/Markdown/Sender
│       ├── layout/base/              # 侧边栏布局
│       ├── pages/
│       │   ├── chat/                 # 聊天 + 深度研究
│       │   ├── dashboard/            # 运营看板
│       │   ├── knowledge/            # 知识库管理
│       │   ├── database/             # 数据库浏览器
│       │   └── news/                 # 行业资讯
│       └── store/                    # Valtio 状态
└── docker-compose.yml                # 基础设施
```

## License

MIT
