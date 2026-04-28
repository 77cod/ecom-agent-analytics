
"""
电商运营分析 V2.0 - 分析架构师 Agent (ChiefArchitect)

职责：
1. 意图解码 - 深度理解用户的电商运营分析需求
2. 知识图谱初始化 - 识别关键品牌/商品/渠道和关系
3. 动态分析维度生成 - 创建可执行的运营分析计划
4. 进度监控 - 根据数据发现动态调整分析维度
"""

import uuid
from typing import Dict, Any, List
from datetime import datetime

from .base import BaseAgent
from ..state import ResearchState, ResearchPhase


class ChiefArchitect(BaseAgent):
    """
    分析架构师 - 运营分析规划的大脑

    特点：
    - 动态DAG调度
    - 大局观，能看到电商运营全貌
    - 根据数据发现调整分析计划
    """

    REVISION_PROMPT = """当前分析课题：{query}

现有分析大纲：
{current_outline}

新发现的事实：
{new_findings}

已完成章节数：{completed_sections}
已收集事实数：{facts_count}
已收集数据点：{data_points_count}

请判断是否需要修订分析大纲，输出JSON：
{{
  "needs_revision": true/false,
  "revision_reason": "如果需要修订，说明原因",
  "revised_outline": [如果需要修订，输出修订后的大纲，与初始大纲格式相同]
}}"""

    PLANNING_PROMPT = """分析课题：{query}

请为该电商运营分析课题生成分析维度和分析假设，输出JSON格式如下：

{{
  "hypothesis_1": "关于销售额/GMV趋势的假设（需要数据验证）",
  "hypothesis_2": "关于品类/商品表现的假设（需要数据验证）",
  "hypothesis_3": "关于竞品或渠道效果的假设（需要数据验证）",
  "sec_1_title": "销售概况",
  "sec_1_desc": "分析GMV、订单量、客单价趋势",
  "sec_1_query": "销售数据关键词",
  "sec_2_title": "商品排行",
  "sec_2_desc": "各商品销量、销售额排名及环比变化",
  "sec_2_query": "商品排行关键词",
  "sec_3_title": "评价分析",
  "sec_3_desc": "好评率、差评关键词、用户情感分析",
  "sec_3_query": "用户评价关键词",
  "sec_4_title": "竞品动态",
  "sec_4_desc": "竞品销量、价格、促销对比",
  "sec_4_query": "竞品信息关键词",
  "sec_5_title": "达人ROI",
  "sec_5_desc": "达人带货GMV、ROI分析",
  "sec_5_query": "达人带货关键词",
  "sec_6_title": "定价策略",
  "sec_6_desc": "价格带分布、折扣力度分析",
  "sec_6_query": "定价策略关键词",
  "questions": "核心问题1;核心问题2;核心问题3"
}}

分析假设示例：
- 假设本月GMV将环比增长，需要销售数据验证增速
- 假设某品类会成为爆款，需要找销量数据支持或反驳
- 假设促销活动会显著影响转化率，需要分析活动期间数据

请根据分析课题填写具体内容，每个字段都是字符串类型。"""

    def __init__(self, llm_api_key: str, llm_base_url: str, model: str = "qwen-max"):
        super().__init__(
            name="ChiefArchitect",
            role="分析架构师",
            llm_api_key=llm_api_key,
            llm_base_url=llm_base_url,
            model=model
        )

    def _convert_flat_to_outline(self, flat_result: Dict) -> Dict:
        """将扁平JSON格式转换为标准outline格式"""
        outline = []
        for i in range(1, 10):  # 最多支持9个章节
            title_key = f"sec_{i}_title"
            desc_key = f"sec_{i}_desc"
            query_key = f"sec_{i}_query"

            if title_key not in flat_result:
                break

            section = {
                "id": f"sec_{i}",
                "title": flat_result.get(title_key, f"章节{i}"),
                "description": flat_result.get(desc_key, ""),
                "section_type": "mixed",
                "requires_data": i <= 2,  # 前两章需要数据
                "requires_chart": i <= 2,
                "search_queries": [flat_result.get(query_key, flat_result.get(title_key, ""))]
            }
            outline.append(section)

        # 处理研究问题
        questions_str = flat_result.get("questions", "")
        if isinstance(questions_str, str):
            research_questions = [q.strip() for q in questions_str.split(";") if q.strip()]
        else:
            research_questions = []

        # 处理研究假设（假设驱动研究）
        hypotheses = []
        for i in range(1, 6):  # 最多5个假设
            h_key = f"hypothesis_{i}"
            if h_key in flat_result and flat_result[h_key]:
                hypotheses.append({
                    "id": f"h_{i}",
                    "content": flat_result[h_key],
                    "status": "unverified",  # unverified, supported, refuted, partially_supported
                    "evidence_for": [],
                    "evidence_against": []
                })

        return {
            "outline": outline,
            "research_questions": research_questions,
            "hypotheses": hypotheses,
            "key_entities": []
        }

    async def process(self, state: ResearchState) -> ResearchState:
        """
        处理入口

        根据当前阶段执行不同的规划任务
        """
        if state["phase"] == ResearchPhase.INIT.value:
            return await self._initial_planning(state)
        elif state["phase"] == ResearchPhase.REVIEWING.value:
            return await self._check_revision(state)
        else:
            return state

    async def _initial_planning(self, state: ResearchState) -> ResearchState:
        """初始规划"""
        self.logger.info(f"Starting initial planning for: {state['query'][:50]}...")

        # 发送 research_step 开始事件
        self.add_message(state, "research_step", {
            "step_id": f"step_planning_{uuid.uuid4().hex[:8]}",
            "step_type": "planning",
            "title": "研究计划",
            "subtitle": "分析问题，制定大纲",
            "status": "running",
            "stats": {}
        })

        # 发送状态消息
        self.add_message(state, "thought", {
            "agent": self.name,
            "content": "正在分析研究问题，构建知识图谱和研究大纲..."
        })

        # 调用LLM生成规划 - 带重试机制
        prompt = self.PLANNING_PROMPT.format(query=state["query"])
        result = None
        max_retries = 2

        for attempt in range(max_retries + 1):
            response = await self.call_llm(
                system_prompt="你是一位专业的电商运营分析师。请严格按照要求的JSON格式输出，不要添加任何额外内容。",
                user_prompt=prompt,
                json_mode=True,
                temperature=0.3,
                max_tokens=8000
            )

            # Debug: 记录原始响应
            self.logger.info(f"Raw LLM response length: {len(response)} (attempt {attempt + 1})")
            self.logger.debug(f"Raw LLM response (first 1000 chars): {response[:1000]}")

            result = self.parse_json_response(response)

            # 检查是否是扁平格式，需要转换
            if result and result.get("sec_1_title") and not result.get("outline"):
                result = self._convert_flat_to_outline(result)

            if result and result.get("outline") and len(result.get("outline", [])) >= 3:
                self.logger.info(f"Successfully parsed outline with {len(result['outline'])} sections")
                break

            # 诊断失败原因
            if not result:
                self.logger.warning(f"Attempt {attempt + 1}: JSON parsing failed completely")
            elif not result.get("outline"):
                self.logger.warning(f"Attempt {attempt + 1}: No 'outline' key in result. Keys: {list(result.keys())}")
            elif len(result.get("outline", [])) < 3:
                self.logger.warning(f"Attempt {attempt + 1}: Outline too short: {len(result.get('outline', []))} sections")

            if attempt < max_retries:
                self.logger.warning(f"Outline generation failed or incomplete, retrying... (attempt {attempt + 1})")
                # 简化提示词重试
                prompt = f"""请为"{state['query']}"生成电商运营分析大纲。

输出JSON格式：
{{"outline": [
    {{"id": "sec_1", "title": "分析维度标题", "description": "描述", "section_type": "mixed", "requires_data": true, "requires_chart": false, "search_queries": ["关键词1", "关键词2"]}},
    ...更多分析维度(共5-8个)...
], "research_questions": ["问题1", "问题2", "问题3"], "key_entities": []}}

要求：outline必须包含5-8个分析维度，覆盖销售概况、商品排行、评价分析、竞品动态、达人ROI、定价策略等方面。"""

        if not result:
            state["errors"].append("Failed to generate research plan after retries")
            self.logger.error(f"Raw LLM response: {response[:800]}")
            return state

        # Debug: log outline count
        self.logger.info(f"Parsed result keys: {list(result.keys())}")
        outline = result.get("outline", [])
        self.logger.info(f"Outline in result: {len(outline)} sections")
        if not outline:
            self.logger.warning(f"No outline found! Full parsed result: {str(result)[:500]}")

        # 更新状态
        state["key_entities"] = [e.get("name", "") for e in result.get("key_entities", []) if isinstance(e, dict)]
        state["mind_map"] = result.get("mind_map", {})
        state["research_questions"] = result.get("research_questions", [])
        state["hypotheses"] = result.get("hypotheses", [])  # 假设驱动研究
        state["knowledge_graph"] = {"nodes": [], "edges": []}  # 知识图谱初始化

        # 处理大纲 - 确保每个章节都有必要字段
        processed_outline = []
        for i, section in enumerate(outline):
            if not isinstance(section, dict):
                continue
            processed_section = {
                "id": section.get("id", f"sec_{i+1}"),
                "title": section.get("title", f"章节{i+1}"),
                "description": section.get("description", ""),
                "section_type": section.get("section_type", "mixed"),
                "requires_data": section.get("requires_data", False),
                "requires_chart": section.get("requires_chart", False),
                "priority": section.get("priority", i+1),
                "search_queries": section.get("search_queries", [section.get("title", "")]),
                "status": "pending"
            }
            # 确保 search_queries 是列表且非空
            if not isinstance(processed_section["search_queries"], list):
                processed_section["search_queries"] = [str(processed_section["search_queries"])]
            # 过滤空字符串，如果结果为空则使用章节标题
            processed_section["search_queries"] = [q for q in processed_section["search_queries"] if q and q.strip()]
            if not processed_section["search_queries"]:
                processed_section["search_queries"] = [processed_section["title"]]
            processed_outline.append(processed_section)

        state["outline"] = processed_outline
        self.logger.info(f"Processed outline: {len(processed_outline)} sections")

        # 发送大纲事件
        self.add_message(state, "outline", {
            "understanding": result.get("understanding", {}),
            "key_entities": result.get("key_entities", []),
            "outline": outline,
            "research_questions": state["research_questions"]
        })

        # 更新阶段
        state["phase"] = ResearchPhase.PLANNING.value

        # 发送 research_step 完成事件
        self.add_message(state, "research_step", {
            "step_type": "planning",
            "title": "研究计划",
            "subtitle": "分析问题，制定大纲",
            "status": "completed",
            "stats": {
                "sections_count": len(processed_outline),
                "questions_count": len(state["research_questions"])
            }
        })

        self.logger.info(f"Planning completed. Generated {len(outline)} sections.")

        return state

    async def _check_revision(self, state: ResearchState) -> ResearchState:
        """检查是否需要修订大纲"""
        # 收集新发现
        new_findings = []
        for fact in state["facts"][-10:]:  # 最近10条事实
            new_findings.append(f"- {fact.get('content', '')[:100]}")

        if not new_findings:
            return state

        # 统计进度
        completed = [s for s in state["outline"] if s.get("status") == "final"]

        prompt = self.REVISION_PROMPT.format(
            query=state["query"],
            current_outline=state["outline"],
            new_findings="\n".join(new_findings),
            completed_sections=len(completed),
            facts_count=len(state["facts"]),
            data_points_count=len(state["data_points"])
        )

        response = await self.call_llm(
            system_prompt="你是电商运营分析架构师，需要判断是否需要调整分析计划。",
            user_prompt=prompt,
            json_mode=True
        )

        result = self.parse_json_response(response)

        if result.get("needs_revision") and result.get("revised_outline"):
            state["outline"] = result["revised_outline"]
            self.add_message(state, "outline_revision", {
                "reason": result.get("revision_reason"),
                "new_outline": result["revised_outline"]
            })
            self.logger.info(f"Outline revised: {result.get('revision_reason')}")

        return state
