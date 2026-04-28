
"""
电商运营分析 V2.0 - 首席笔杆 Agent (LeadWriter)

职责：
1. 深度写作 - 将运营数据串联成逻辑严密的运营分析报告
2. Markdown排版 - 专业的格式排版
3. 图文混排 - 整合文字、图表、数据
4. 行动建议 - 基于数据洞察生成可执行的运营建议
"""

import uuid
from typing import Dict, Any, List
from datetime import datetime

from .base import BaseAgent
from ..state import ResearchState, ResearchPhase


class LeadWriter(BaseAgent):
    """
    首席笔杆 - 电商运营分析报告的撰写者

    特点：
    - 深度写作能力
    - 专业的电商运营分析报告风格
    - 逻辑严密的叙述结构
    - 数据驱动的行动建议生成
    """

    SECTION_WRITING_PROMPT = """你是一位顶级的电商运营分析师，擅长撰写深度运营分析报告。

## 分析主题
{query}

## 当前分析维度信息
标题: {section_title}
描述: {section_description}
类型: {section_type}

## 可用素材

### 相关事实
{facts}

### 数据点
{data_points}

### 已有洞察
{insights}

### 相关图表
{charts_info}

## 写作要求
1. **专业性**：使用电商运营术语（GMV/客单价/转化率/ROI/环比等），体现专业深度
2. **逻辑性**：论点清晰，论据充分，层层递进
3. **数据支撑**：关键观点必须有运营数据支撑，标注具体数值和变化幅度
4. **引用规范**：标注数据来源（店铺后台、平台数据、竞品监控等）
5. **图表整合**：在合适位置插入图表引用 ![图表标题](chart_id)
6. **字数控制**：本维度 500-1000 字
7. **不要重复标题**：正文开头不要再写维度标题

## 输出格式
```json
{{
    "content": "分析维度正文内容（Markdown格式，不包含维度标题）",
    "key_points": ["本维度的核心要点"],
    "citations": [
        {{"source": "来源名称", "url": "完整URL"}}
    ],
    "actionable_recommendations": ["基于本维度数据的具体运营建议"],
    "data_highlights": ["关键数据发现"]
}}
```

## 写作风格示例
- 好的开头："8月主营品类GMV达285万元，环比增长10.5%，其中直播渠道贡献45%销售额..."
- 避免的开头："关于主营品类的销售情况，首先我们来看..."
- 数据引用示例："客单价128元（环比+5元），转化率3.2%（环比+0.3pp）"

开始撰写："""

    SYNTHESIS_PROMPT = """你是首席运营分析师，需要将各分析维度整合成完整的电商运营分析报告。

## 分析主题
{query}

## 各分析维度内容
{sections_content}

## 收集的所有数据来源
{all_sources}

## 任务
1. 撰写运营概览（Executive Summary）
2. 整合各分析维度，确保逻辑连贯，使用层级编号
3. 基于所有数据洞察，生成可执行的运营行动建议
4. 撰写结论与展望
5. 整理数据来源列表

## 关键要求

### 1. 标题编号规则（必须严格遵守）
- 一级标题：1、2、3...（如：1 销售概况）
- 二级标题：1.1、1.2、2.1...（如：1.1 GMV趋势）
- 三级标题：1.1.1、1.1.2...（如：1.1.1 日销售额波动）
- **禁止标题重复**：每个标题必须唯一，不要在正文中重复维度标题

### 2. 数据标注规则
- 关键指标加粗：**GMV 285万元**、**客单价128元**
- 变化幅度标注：环比+10.5%、同比-3.2pp
- 数据来源标注：在数据后标注来源

### 3. 运营行动建议规则（重要！）
- 每条建议必须基于报告中的具体数据发现
- 建议要具体、可执行、有优先级
- 每条建议包含：行动内容、预期效果、优先级（高/中/低）

### 4. 报告结构规范
- 不要在报告开头使用 # 一级标题
- 直接从"运营概览"开始
- 各维度使用 ## 二级标题
- 子维度使用 ### 三级标题

## 输出格式
```json
{{
    "executive_summary": "运营概览（300-500字）",
    "full_report": "完整运营分析报告（Markdown格式，按下方结构生成）",
    "conclusions": ["核心结论1", "核心结论2"],
    "actionable_recommendations": [
        {{"action": "具体行动内容", "rationale": "基于的数据发现", "expected_impact": "预期效果", "priority": "高/中/低"}}
    ],
    "key_metrics_summary": {{
        "gmv": "总GMV及变化",
        "orders": "总订单量及变化",
        "aov": "客单价及变化",
        "top_product": "TOP1商品"
    }},
    "outlook": "未来展望",
    "references": [
        {{"id": 1, "title": "来源标题", "url": "完整URL", "author": "作者/机构", "date": "日期"}}
    ]
}}
```

## 报告结构模板
```markdown
## 运营概览

[300-500字的运营概览，包含核心KPI摘要]

---

## 1 [第一分析维度标题]

[维度引言段落]

### 1.1 [子维度标题]

[内容，包含数据如：GMV达285万元（环比+10.5%）]

### 1.2 [子维度标题]

#### 1.2.1 [三级标题]

[更详细的内容]

---

## 2 [第二分析维度标题]

### 2.1 [子维度标题]

...

---

## 运营行动建议

### 高优先级
1. **【行动标题】** - 具体行动内容...
   - 数据依据：...
   - 预期效果：...

### 中优先级
...

### 低优先级
...

---

## 结论与展望

### 核心结论
1. [结论1]
2. [结论2]

### 下月展望
[展望内容]

---

## 数据来源

1. [来源标题1](URL1)
2. [来源标题2](URL2)
...
```"""

    REVISION_PROMPT = """你是首席运营分析师，需要根据审核反馈修订运营分析报告。

## 原始报告
{original_content}

## 审核反馈
{feedback}

## 补充的新信息
{new_info}

## 任务
根据反馈修订运营分析报告，解决指出的问题。

## 修订原则
1. 针对性修改：只修改有问题的部分
2. 补充数据来源：对缺少数据支撑的观点补充来源
3. 修正错误：纠正数据错误或分析逻辑漏洞
4. 优化建议：使运营行动建议更加具体和可执行
5. 保持风格：修订后保持报告整体风格一致

输出JSON：
```json
{{
    "revised_content": "修订后的运营分析报告内容",
    "changes_made": ["修改1", "修改2"],
    "addressed_issues": ["已解决的问题ID"],
    "unable_to_address": ["无法解决的问题及原因"]
}}
```"""

    def __init__(self, llm_api_key: str, llm_base_url: str, model: str = "qwen-max"):
        super().__init__(
            name="LeadWriter",
            role="首席笔杆",
            llm_api_key=llm_api_key,
            llm_base_url=llm_base_url,
            model=model
        )

    async def process(self, state: ResearchState) -> ResearchState:
        """处理入口"""
        if state["phase"] == ResearchPhase.WRITING.value:
            return await self._write_report(state)
        elif state["phase"] == ResearchPhase.REVISING.value:
            return await self._revise_report(state)
        else:
            return state

    async def _write_report(self, state: ResearchState) -> ResearchState:
        """撰写报告"""
        # 发送 research_step 开始事件
        # 注意: step_type 必须是 "writing" 以匹配 graph.py 发送的 phase 事件
        self.add_message(state, "research_step", {
            "step_id": f"step_writing_{uuid.uuid4().hex[:8]}",
            "step_type": "writing",
            "title": "内容生成",
            "subtitle": "撰写运营分析报告",
            "status": "running",
            "stats": {"sections_count": len(state["outline"]), "word_count": 0}
        })

        self.add_message(state, "thought", {
            "agent": self.name,
            "content": "开始撰写电商运营分析报告..."
        })

        # 逐章节撰写
        for section in state["outline"]:
            if section.get("status") not in ["final", "drafted"]:
                await self._write_section(state, section)

        # 整合报告
        await self._synthesize_report(state)

        # 发送 research_step 完成事件
        word_count = len(state.get("final_report", ""))
        self.add_message(state, "research_step", {
            "step_type": "writing",
            "title": "内容生成",
            "subtitle": "撰写运营分析报告",
            "status": "completed",
            "stats": {
                "sections_count": len(state["outline"]),
                "word_count": word_count,
                "references_count": len(state.get("references", []))
            }
        })

        # 更新阶段
        state["phase"] = ResearchPhase.REVIEWING.value

        return state

    async def _write_section(self, state: ResearchState, section: Dict) -> None:
        """撰写单个章节"""
        section_id = section["id"]
        self.logger.info(f"Writing section: {section.get('title')}")

        self.add_message(state, "action", {
            "agent": self.name,
            "tool": "writing_section",
            "section": section.get("title")
        })

        # 收集相关素材
        related_facts = [f for f in state["facts"] if section_id in f.get("related_sections", [])]
        if not related_facts:
            # 如果没有特定关联，使用所有事实
            related_facts = state["facts"][:10]

        # 格式化事实
        facts_text = []
        for fact in related_facts:
            facts_text.append(f"- {fact.get('content')} (来源: {fact.get('source_name')}, 可信度: {fact.get('credibility_score')})")

        # 格式化数据点
        data_text = []
        for dp in state["data_points"][:10]:
            data_text.append(f"- {dp.get('name')}: {dp.get('value')} {dp.get('unit', '')} ({dp.get('year', 'N/A')})")

        # 格式化图表信息
        charts_info = []
        for chart in state["charts"]:
            if chart.get("section_id") == section_id:
                charts_info.append(f"- 图表: {chart.get('title')} (ID: {chart.get('id')})")

        prompt = self.SECTION_WRITING_PROMPT.format(
            query=state["query"],
            section_title=section.get("title", ""),
            section_description=section.get("description", ""),
            section_type=section.get("section_type", "mixed"),
            facts="\n".join(facts_text) if facts_text else "（暂无相关事实）",
            data_points="\n".join(data_text) if data_text else "（暂无数据点）",
            insights="\n".join([f"- {i}" for i in state["insights"][:5]]) if state["insights"] else "（暂无洞察）",
            charts_info="\n".join(charts_info) if charts_info else "（暂无图表）"
        )

        response = await self.call_llm(
            system_prompt="你是顶级的电商运营分析师，擅长撰写专业的运营分析报告。",
            user_prompt=prompt,
            json_mode=True,
            temperature=0.4,
            max_tokens=8000
        )

        result = self.parse_json_response(response)

        if result and result.get("content"):
            section_content = result["content"]
            state["draft_sections"][section_id] = section_content
            section["status"] = "drafted"

            # 收集引用
            for citation in result.get("citations", []):
                state["references"].append({
                    "id": len(state["references"]) + 1,
                    "marker": citation.get("marker"),
                    "source": citation.get("source"),
                    "url": citation.get("url", "")
                })

            # 发送章节内容到"过程报告" - 包含完整内容用于流式显示
            self.add_message(state, "section_content", {
                "agent": self.name,
                "section_id": section_id,
                "section_title": section.get("title"),
                "content": section_content,  # 完整章节内容
                "word_count": len(section_content),
                "key_points": result.get("key_points", [])
            })

            # 发送观察消息（显示在左侧步骤流程）
            self.add_message(state, "observation", {
                "agent": self.name,
                "content": f"章节「{section.get('title')}」撰写完成\n字数: {len(section_content)}\n要点: {', '.join(result.get('key_points', [])[:2]) if result.get('key_points') else '无'}"
            })

    async def _synthesize_report(self, state: ResearchState) -> None:
        """整合完整报告"""
        self.add_message(state, "thought", {
            "agent": self.name,
            "content": "正在整合各分析维度，生成完整运营分析报告..."
        })

        # 准备各章节内容
        sections_content = []
        for section in state["outline"]:
            section_id = section["id"]
            content = state["draft_sections"].get(section_id, "")
            if content:
                sections_content.append(f"## {section.get('title')}\n{content}")

        # 收集所有来源
        all_sources = []
        for ref in state["references"]:
            all_sources.append(f"- {ref.get('source')} ({ref.get('url', 'N/A')})")

        for fact in state["facts"]:
            source_entry = f"- {fact.get('source_name')} ({fact.get('source_url', 'N/A')})"
            if source_entry not in all_sources:
                all_sources.append(source_entry)

        prompt = self.SYNTHESIS_PROMPT.format(
            query=state["query"],
            sections_content="\n\n".join(sections_content) if sections_content else "（暂无章节内容）",
            all_sources="\n".join(all_sources[:30]) if all_sources else "（暂无来源）"
        )

        self.logger.info(f"[LeadWriter] 调用 LLM 整合报告...")
        response = await self.call_llm(
            system_prompt="你是资深的运营分析报告主编，擅长整合和打磨最终运营分析报告。",
            user_prompt=prompt,
            json_mode=True,
            temperature=0.3,
            max_tokens=8000
        )

        result = self.parse_json_response(response)
        self.logger.info(f"[LeadWriter] JSON 解析结果: {bool(result)}, keys: {result.keys() if result else 'N/A'}")

        executive_summary = ""
        conclusions = []

        if result and result.get("full_report"):
            state["final_report"] = result.get("full_report", "")
            executive_summary = result.get("executive_summary", "")
            conclusions = result.get("conclusions", [])
            self.logger.info(f"[LeadWriter] ✅ 报告整合成功，长度: {len(state['final_report'])}")

            # 更新参考文献
            for ref in result.get("references", []):
                if ref not in state["references"]:
                    state["references"].append(ref)
        else:
            # JSON 解析失败时的备选方案：使用已有章节内容组装报告
            self.logger.warning(f"[LeadWriter] ⚠️ JSON 解析失败，使用章节内容作为备选")
            fallback_report = f"# {state['query']} 运营分析报告\n\n"
            for section in state["outline"]:
                section_id = section["id"]
                content = state["draft_sections"].get(section_id, "")
                if content:
                    fallback_report += f"## {section.get('title', section_id)}\n\n{content}\n\n"
            state["final_report"] = fallback_report
            self.logger.info(f"[LeadWriter] 使用备选报告，长度: {len(state['final_report'])}")

        # 发送报告完成事件 - 包含完整报告内容用于前端流式显示
        actionable_recommendations = result.get("actionable_recommendations", []) if result else []
        key_metrics_summary = result.get("key_metrics_summary", {}) if result else {}
        self.add_message(state, "report_draft", {
            "agent": self.name,
            "content": state["final_report"],  # 完整报告内容
            "executive_summary": executive_summary,
            "conclusions": conclusions,
            "actionable_recommendations": actionable_recommendations,
            "key_metrics_summary": key_metrics_summary,
            "word_count": len(state["final_report"]),
            "references_count": len(state["references"])
        })

    async def _revise_report(self, state: ResearchState) -> ResearchState:
        """根据反馈修订报告"""
        self.add_message(state, "thought", {
            "agent": self.name,
            "content": "根据审核反馈修订运营分析报告..."
        })

        # 收集未解决的问题
        unresolved = [f for f in state["critic_feedback"] if not f.get("resolved")]
        feedback_text = []
        for issue in unresolved:
            feedback_text.append(f"- [{issue.get('severity')}] {issue.get('description')}\n  建议: {issue.get('suggestion')}")

        # 收集新信息（如果有补充搜索）
        new_facts = state["facts"][-5:] if state["facts"] else []
        new_info = "\n".join([f"- {f.get('content', '')[:200]}" for f in new_facts])

        prompt = self.REVISION_PROMPT.format(
            original_content=state.get("final_report", "")[:6000],
            feedback="\n".join(feedback_text) if feedback_text else "无具体反馈",
            new_info=new_info if new_info else "无补充信息"
        )

        response = await self.call_llm(
            system_prompt="你是负责修订运营分析报告的资深编辑。",
            user_prompt=prompt,
            json_mode=True,
            temperature=0.3,
            max_tokens=8000
        )

        result = self.parse_json_response(response)

        if result and result.get("revised_content"):
            state["final_report"] = result["revised_content"]

            # 标记已解决的问题
            for issue_id in result.get("addressed_issues", []):
                for feedback in state["critic_feedback"]:
                    if feedback.get("id") == issue_id:
                        feedback["resolved"] = True

            self.add_message(state, "revision_complete", {
                "agent": self.name,
                "changes_count": len(result.get("changes_made", [])),
                "addressed_issues": result.get("addressed_issues", []),
                "unable_to_address": result.get("unable_to_address", [])
            })

        # 回到审核阶段
        state["phase"] = ResearchPhase.REVIEWING.value

        return state
