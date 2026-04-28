
"""
电商运营分析 V2.0 - 数据分析师 Agent (DataAnalyst)

职责：
1. 从电商运营数据中提取结构化指标
2. 构建商品/品牌/渠道知识图谱(实体+关系)
3. 生成电商可视化图表配置(ECharts)
4. 识别运营数据趋势和洞察
"""

import uuid
from typing import Dict, Any, List
from datetime import datetime

from .base import BaseAgent
from ..state import ResearchState, ResearchPhase


class DataAnalyst(BaseAgent):
    """
    数据分析师 - 专注于电商运营数据提取、知识图谱和可视化

    特点：
    - 从运营数据中提取结构化指标（GMV/客单价/转化率/退货率/ROI）
    - 构建品牌-商品-渠道知识图谱
    - 生成ECharts可视化配置
    - 识别运营趋势和洞察
    """

    # 数据提取 Prompt
    DATA_EXTRACTION_PROMPT = """你是专业的电商数据分析师，擅长从运营数据中提取结构化指标。

## 分析主题
{query}

## 运营数据
{search_results}

## 任务
从以上运营数据中提取所有可量化的电商指标，包括：
1. GMV/销售额数据（金额、单位、时间段）
2. 订单量/客单价数据（数量、金额、环比变化）
3. 转化率/退货率数据（百分比）
4. 商品排行数据（商品名、销量、排名）
5. 达人ROI数据（GMV/投入比）
6. 评价情感数据（好评率、差评率、关键词）

## 输出要求
请输出JSON格式：
```json
{{
    "data_points": [
        {{
            "id": "dp_001",
            "name": "8月商品GMV",
            "value": 2850000,
            "unit": "元",
            "year": 2025,
            "source": "店铺后台数据",
            "category": "gmv",
            "confidence": 0.95
        }}
    ],
    "time_series": [
        {{
            "id": "ts_001",
            "metric": "商品月销售额",
            "unit": "元",
            "data": [
                {{"year": 2025, "month": 6, "value": 2100000}},
                {{"year": 2025, "month": 7, "value": 2580000}},
                {{"year": 2025, "month": 8, "value": 2850000}}
            ],
            "source": "店铺后台数据"
        }}
    ],
    "distributions": [
        {{
            "id": "dist_001",
            "name": "渠道销售额占比",
            "year": 2025,
            "data": [
                {{"category": "直播带货", "value": 45, "unit": "%"}},
                {{"category": "天猫旗舰店", "value": 30, "unit": "%"}},
                {{"category": "抖音商城", "value": 25, "unit": "%"}}
            ],
            "source": "渠道数据"
        }}
    ],
    "insights": [
        "8月商品GMV达285万元，环比增长10.5%",
        "直播带货贡献45%销售额，是核心渠道"
    ]
}}
```

注意：
- 只提取有明确来源的数据
- confidence表示数据可信度(0-1)
- 如果没有找到相关数据，返回空数组"""

    # 知识图谱构建 Prompt
    KNOWLEDGE_GRAPH_PROMPT = """你是电商知识图谱专家，擅长从运营数据中提取品牌、商品、渠道实体和关系。

## 分析主题
{query}

## 文本内容
{content}

## 任务
从以上内容中提取实体和关系，构建电商运营知识图谱。

## 实体类型定义
- brand: 品牌（如：我方品牌、竞品品牌A、竞品品牌B）
- product: 商品（如：主推爆款、经典款、入门款热销品）
- channel: 渠道（如：直播带货、天猫旗舰店、抖音商城）
- feature: 特性（如：UPF50+、透气、轻量化）
- competitor: 竞品（如：竞品A品牌、竞品B品牌）
- kol: 达人（如：李佳琦、某头部主播）
- metric: 指标（如：GMV、客单价、转化率）

## 输出要求
请输出JSON格式：
```json
{{
    "nodes": [
        {{"id": "brand_1", "name": "我方品牌", "type": "brand", "importance": 10}},
        {{"id": "product_1", "name": "主推热销款", "type": "product", "importance": 8}},
        {{"id": "channel_1", "name": "直播带货", "type": "channel", "importance": 9}},
        {{"id": "kol_1", "name": "达人A", "type": "kol", "importance": 7}}
    ],
    "edges": [
        {{"source": "brand_1", "target": "product_1", "relation": "出品"}},
        {{"source": "product_1", "target": "channel_1", "relation": "销售于"}},
        {{"source": "kol_1", "target": "product_1", "relation": "带货"}},
        {{"source": "kol_1", "target": "channel_1", "relation": "直播于"}}
    ]
}}
```

注意：
- importance范围1-10，表示节点重要性
- 品牌(brand)和核心指标(metric)的importance最高
- 提取5-15个最重要的实体
- 关系要简洁，2-4个字"""

    # 图表生成 Prompt（保持原始版本，由LLM根据数据自行适配）
    CHART_GENERATION_PROMPT = """你是数据可视化专家，擅长生成ECharts图表配置。

## 研究主题
{query}

## 可用数据
{data}

## 任务
根据数据生成合适的ECharts图表配置，选择最能展示数据特点的图表类型。

## 图表类型选择规则
- 时间序列数据 → line (折线图)
- 分类比较数据 → bar (柱状图)
- 占比分布数据 → pie (饼图)
- 进度/百分比 → horizontal_bar (横向进度条)
- 多维对比 → radar (雷达图)

## 设计要求
1. 配色使用简约专业色系：
   - 主色：#1677ff (蓝)
   - 辅助色：#52c41a (绿), #722ed1 (紫), #fa8c16 (橙), #eb2f96 (粉)
2. 标题简洁明了
3. 不要过多装饰，保持简约

## 输出要求
请输出JSON格式：
```json
{{
    "charts": [
        {{
            "id": "chart_001",
            "title": "中国AI市场规模",
            "subtitle": "2020-2024年市场规模（亿元）",
            "type": "line",
            "echarts_option": {{
                "grid": {{"left": "3%", "right": "4%", "bottom": "3%", "containLabel": true}},
                "xAxis": {{
                    "type": "category",
                    "data": ["2020", "2021", "2022", "2023", "2024"],
                    "axisLine": {{"lineStyle": {{"color": "#e8e8e8"}}}},
                    "axisLabel": {{"color": "#666"}}
                }},
                "yAxis": {{
                    "type": "value",
                    "axisLine": {{"show": false}},
                    "splitLine": {{"lineStyle": {{"color": "#f0f0f0"}}}}
                }},
                "series": [{{
                    "type": "line",
                    "data": [3200, 4100, 5200, 6800, 8500],
                    "smooth": true,
                    "symbol": "circle",
                    "symbolSize": 8,
                    "itemStyle": {{"color": "#1677ff"}},
                    "lineStyle": {{"width": 3}},
                    "areaStyle": {{"color": {{"type": "linear", "x": 0, "y": 0, "x2": 0, "y2": 1, "colorStops": [{{"offset": 0, "color": "rgba(22,119,255,0.2)"}}, {{"offset": 1, "color": "rgba(22,119,255,0)"}}]}}}}
                }}]
            }}
        }},
        {{
            "id": "chart_002",
            "title": "细分领域市场份额",
            "subtitle": "2024年各技术领域占比",
            "type": "horizontal_bar",
            "echarts_option": {{
                "grid": {{"left": "25%", "right": "15%", "top": "5%", "bottom": "5%"}},
                "xAxis": {{"type": "value", "show": false, "max": 100}},
                "yAxis": {{
                    "type": "category",
                    "data": ["计算机视觉", "自然语言处理", "机器学习平台", "智能语音", "其他"],
                    "axisLine": {{"show": false}},
                    "axisTick": {{"show": false}},
                    "axisLabel": {{"color": "#333", "fontSize": 13}}
                }},
                "series": [{{
                    "type": "bar",
                    "data": [
                        {{"value": 32, "itemStyle": {{"color": "#1677ff"}}}},
                        {{"value": 28, "itemStyle": {{"color": "#722ed1"}}}},
                        {{"value": 24, "itemStyle": {{"color": "#1677ff"}}}},
                        {{"value": 10, "itemStyle": {{"color": "#52c41a"}}}},
                        {{"value": 6, "itemStyle": {{"color": "#fa8c16"}}}}
                    ],
                    "barWidth": 12,
                    "label": {{
                        "show": true,
                        "position": "right",
                        "formatter": "{{c}}%",
                        "color": "#666"
                    }},
                    "backgroundStyle": {{"color": "#f5f5f5"}},
                    "showBackground": true
                }}]
            }}
        }}
    ]
}}
```"""

    def __init__(self, llm_api_key: str, llm_base_url: str, model: str = "qwen-max"):
        super().__init__(
            name="DataAnalyst",
            role="数据分析师",
            llm_api_key=llm_api_key,
            llm_base_url=llm_base_url,
            model=model
        )

    async def process(self, state: ResearchState) -> ResearchState:
        """处理入口"""
        if state["phase"] == ResearchPhase.ANALYZING.value:
            return await self._analyze_data(state)
        return state

    async def _analyze_data(self, state: ResearchState) -> ResearchState:
        """执行数据分析"""
        self.logger.info("Starting data analysis...")

        # 发送开始事件
        self.add_message(state, "research_step", {
            "step_id": f"step_analyze_{uuid.uuid4().hex[:8]}",
            "step_type": "analyzing",
            "title": "数据分析",
            "subtitle": "生成可视化",
            "status": "running",
            "stats": {"results_count": 0, "charts_count": 0, "entities_count": 0}
        })

        # 1. 提取结构化数据
        extracted_data = await self._extract_data(state)

        # 2. 构建知识图谱
        knowledge_graph = await self._build_knowledge_graph(state)

        # 3. 生成可视化图表
        charts = await self._generate_charts(state, extracted_data)

        # 更新状态
        if knowledge_graph:
            state["knowledge_graph"] = knowledge_graph
            # 发送知识图谱事件
            self.add_message(state, "knowledge_graph", {
                "graph": knowledge_graph,
                "stats": {
                    "entities_count": len(knowledge_graph.get("nodes", [])),
                    "relations_count": len(knowledge_graph.get("edges", []))
                }
            })

        if charts:
            state["charts"].extend(charts)
            self.logger.info(f"[DataAnalyst] 生成了 {len(charts)} 个 ECharts 图表，准备发送 charts 事件")
            for i, chart in enumerate(charts):
                self.logger.info(f"[DataAnalyst] 图表 {i+1}: id={chart.get('id')}, title={chart.get('title')}, has_echarts_option={bool(chart.get('echarts_option'))}")
            # 发送图表事件
            self.add_message(state, "charts", {
                "charts": charts
            })
            self.logger.info(f"[DataAnalyst] ✅ charts 事件已发送")

        # 发送完成事件
        self.add_message(state, "research_step", {
            "step_type": "analyzing",
            "title": "数据分析",
            "subtitle": "生成可视化",
            "status": "completed",
            "stats": {
                "results_count": len(state.get("facts", [])),
                "charts_count": len(charts) if charts else 0,
                "entities_count": len(knowledge_graph.get("nodes", [])) if knowledge_graph else 0
            }
        })

        return state

    async def _extract_data(self, state: ResearchState) -> Dict[str, Any]:
        """从搜索结果中提取结构化数据"""
        self.logger.info("Extracting structured data...")

        # 收集搜索结果
        search_results_text = []
        for fact in state.get("facts", [])[:20]:
            search_results_text.append(f"- {fact.get('content', '')} (来源: {fact.get('source_name', '未知')})")

        if not search_results_text:
            self.logger.info("No facts to extract data from")
            return {"data_points": [], "time_series": [], "distributions": [], "insights": []}

        prompt = self.DATA_EXTRACTION_PROMPT.format(
            query=state["query"],
            search_results="\n".join(search_results_text)
        )

        response = await self.call_llm(
            system_prompt="你是专业的电商数据分析师，擅长从运营数据中提取结构化指标。请输出JSON格式。",
            user_prompt=prompt,
            json_mode=True,
            temperature=0.2
        )

        result = self.parse_json_response(response)

        # 更新数据点到状态
        if result.get("data_points"):
            for dp in result["data_points"]:
                state["data_points"].append(dp)

        # 更新洞察
        if result.get("insights"):
            state["insights"].extend(result["insights"])

        self.logger.info(f"Extracted {len(result.get('data_points', []))} data points, {len(result.get('time_series', []))} time series")

        return result

    async def _build_knowledge_graph(self, state: ResearchState) -> Dict[str, Any]:
        """构建知识图谱"""
        self.logger.info("Building knowledge graph...")

        # 收集内容
        content_parts = []
        for fact in state.get("facts", [])[:15]:
            content_parts.append(fact.get("content", ""))

        if not content_parts:
            self.logger.info("No content for knowledge graph")
            return {"nodes": [], "edges": []}

        prompt = self.KNOWLEDGE_GRAPH_PROMPT.format(
            query=state["query"],
            content="\n".join(content_parts)
        )

        response = await self.call_llm(
            system_prompt="你是电商知识图谱专家，擅长从运营数据中提取品牌/商品/渠道实体和关系。请输出JSON格式。",
            user_prompt=prompt,
            json_mode=True,
            temperature=0.2
        )

        result = self.parse_json_response(response)

        # 添加节点大小（基于importance）
        if result.get("nodes"):
            for node in result["nodes"]:
                importance = node.get("importance", 5)
                node["size"] = 20 + importance * 3  # 20-50 range

        self.logger.info(f"Built knowledge graph with {len(result.get('nodes', []))} nodes, {len(result.get('edges', []))} edges")

        return result

    async def _generate_charts(self, state: ResearchState, extracted_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """生成可视化图表"""
        self.logger.info("[DataAnalyst] ========== 开始生成 ECharts 可视化图表 ==========")

        # 准备数据
        data_for_charts = {
            "data_points": extracted_data.get("data_points", []),
            "time_series": extracted_data.get("time_series", []),
            "distributions": extracted_data.get("distributions", []),
            "existing_data_points": state.get("data_points", [])[:10]
        }

        # 如果没有足够数据，跳过
        total_data = (len(data_for_charts["data_points"]) +
                     len(data_for_charts["time_series"]) +
                     len(data_for_charts["distributions"]))

        self.logger.info(f"[DataAnalyst] 图表数据统计: data_points={len(data_for_charts['data_points'])}, time_series={len(data_for_charts['time_series'])}, distributions={len(data_for_charts['distributions'])}, total={total_data}")

        if total_data == 0:
            self.logger.warning("[DataAnalyst] ⚠️ 没有足够数据生成图表，跳过")
            return []

        prompt = self.CHART_GENERATION_PROMPT.format(
            query=state["query"],
            data=str(data_for_charts)
        )

        response = await self.call_llm(
            system_prompt="你是电商数据可视化专家，擅长生成电商运营ECharts图表配置。请输出JSON格式。",
            user_prompt=prompt,
            json_mode=True,
            temperature=0.3
        )

        result = self.parse_json_response(response)
        charts = result.get("charts", [])

        # 为每个图表添加唯一ID
        for chart in charts:
            if not chart.get("id"):
                chart["id"] = f"chart_{uuid.uuid4().hex[:8]}"

        self.logger.info(f"Generated {len(charts)} charts")

        return charts

    async def analyze_for_section(self, state: ResearchState, section_title: str) -> Dict[str, Any]:
        """为特定章节分析数据（可被其他Agent调用）"""
        self.logger.info(f"Analyzing data for section: {section_title}")

        # 收集与该章节相关的事实
        related_facts = [f for f in state.get("facts", [])
                        if section_title in str(f.get("related_sections", []))]

        if not related_facts:
            related_facts = state.get("facts", [])[:10]

        # 简化的数据提取
        search_results_text = [f"- {f.get('content', '')}" for f in related_facts]

        prompt = f"""分析以下内容，提取与"{section_title}"相关的关键数据：

{chr(10).join(search_results_text)}

输出JSON格式：
{{
    "key_metrics": [
        {{"name": "指标名", "value": "值", "unit": "单位"}}
    ],
    "trend": "上升/下降/稳定",
    "summary": "一句话总结"
}}"""

        response = await self.call_llm(
            system_prompt="你是电商数据分析师，提取运营关键指标。",
            user_prompt=prompt,
            json_mode=True,
            temperature=0.2
        )

        return self.parse_json_response(response)
