"""
DeepResearch V2.0 - 数据查询员 Agent (DataQueryer)

职责：
1. 理解用户问题，确定需要查询哪些数据
2. 从 mock 数据集中查询商品/订单/评价/竞品数据
3. 用AI分析查询结果，提取结构化事实
4. 替代原 DeepScout 的网络搜索功能

数据来源：ecommerce_mock_data.py（模拟电商数据库）
"""

import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime

from .base import BaseAgent
from ..state import ResearchState, ResearchPhase
from ..ecommerce_mock_data import get_all_mock_data, get_mock_data_for_industry


class DataQueryer(BaseAgent):
    """
    数据查询员 - 电商数据查询专家

    特点：
    - 从 mock 数据中查询需要的字段
    - 支持多维度查询（商品/订单/评价/达人/竞品）
    - AI驱动：理解自然语言问题，自动匹配数据
    - 返回结构化事实，供下游Agent分析
    - 支持按行业切换 mock 数据集
    """

    DATA_ANALYSIS_PROMPT = """你是一位电商数据分析师，需要根据用户问题从数据中提取信息。

## 研究问题
{query}

## 当前分析维度
标题: {section_title}
描述: {section_description}

## 可用数据
{available_data}

## 任务
根据用户问题和当前分析维度，从可用数据中提取相关信息。

输出JSON格式：
```json
{{
    "extracted_facts": [
        {{
            "content": "提取的事实陈述（具体、有数据支撑）",
            "source_name": "数据来源（如'月度销售数据'）",
            "source_url": "",
            "source_type": "report",
            "credibility_score": 0.9,
            "importance": "high/medium/low",
            "data_points": [
                {{"name": "指标名", "value": "数值", "unit": "单位", "year": 2024}}
            ]
        }}
    ],
    "key_insights": ["关键洞察"],
    "missing_info": ["如果要更深入分析，还需要什么数据"]
}}

## 评分标准
- 来源为 mock 数据，可信度统一给 0.9
- importance 根据与分析维度的相关性判断
- data_points 中的 unit 尽量给标准单位（元、件、%等）
"""

    def __init__(self, llm_api_key: str, llm_base_url: str, model: str = "qwen-max", use_mock: bool = True, industry_id: str = "fashion"):
        super().__init__(
            name="DataQueryer",
            role="数据查询员",
            llm_api_key=llm_api_key,
            llm_base_url=llm_base_url,
            model=model
        )
        self.use_mock = use_mock
        self._current_industry = industry_id
        # 加载对应行业的 mock 数据
        self.mock_data = get_mock_data_for_industry(industry_id)
        self.logger.info(f"DataQueryer 初始化完成，行业={industry_id}，已加载 {self._count_all_data()} 条数据 (mock={use_mock})")

    def switch_industry(self, industry_id: str) -> int:
        """切换行业数据集

        Args:
            industry_id: 行业标识（fashion/beauty/digital/food）

        Returns:
            int: 新数据集的数据总条数
        """
        if industry_id != self._current_industry:
            self._current_industry = industry_id
            self.mock_data = get_mock_data_for_industry(industry_id)
            self.logger.info(f"DataQueryer 切换到行业={industry_id}，已加载 {self._count_all_data()} 条数据")
        return self._count_all_data()

    def _count_all_data(self) -> int:
        """统计所有数据条数"""
        total = 0
        for key, value in self.mock_data.items():
            if isinstance(value, list):
                total += len(value)
        return total

    async def process(self, state: ResearchState) -> ResearchState:
        """处理入口 - 根据大纲分析维度查询数据"""
        if state["phase"] not in [ResearchPhase.PLANNING.value, ResearchPhase.RESEARCHING.value]:
            return state

        # 从 state 中获取行业ID并自动切换数据集
        industry_id = state.get("industry_id", "fashion")
        if industry_id != self._current_industry:
            self.switch_industry(industry_id)
            self.logger.info(f"DataQueryer 从 state 检测到行业变化: {self._current_industry} -> {industry_id}")

        state["phase"] = ResearchPhase.RESEARCHING.value

        # 发送开始事件
        self.add_message(state, "research_step", {
            "step_id": f"step_query_{uuid.uuid4().hex[:8]}",
            "step_type": "searching",
            "title": "数据查询",
            "subtitle": "查询电商数据",
            "status": "running",
            "stats": {"sections_count": 0, "results_count": 0}
        })

        self.add_message(state, "thought", {
            "agent": self.name,
            "content": f"正在查询电商数据，分析 {len(state['outline'])} 个维度..."
        })

        # 找到待分析的维度
        pending_sections = [s for s in state["outline"] if s.get("status") == "pending"]

        if not pending_sections:
            self.logger.info("没有待分析的维度")
            return state

        # 逐个维度查询数据
        for section in pending_sections[:5]:
            await self._query_section(state, section)

        # 发送完成事件
        self.add_message(state, "research_step", {
            "step_type": "searching",
            "title": "数据查询",
            "subtitle": "查询电商数据",
            "status": "completed",
            "stats": {
                "results_count": len(state.get("facts", [])),
                "data_points": len(state.get("data_points", [])),
            }
        })

        return state

    async def _query_section(self, state: ResearchState, section: Dict) -> None:
        """查询单个分析维度的数据"""
        section_title = section.get("title", "")
        section_desc = section.get("description", "")
        section_id = section.get("id", "")

        self.logger.info(f"查询维度: {section_title}")

        self.add_message(state, "action", {
            "agent": self.name,
            "tool": "query_data",
            "section": section_title,
        })

        # 1. 直接规则匹配（mock 数据已结构化，无需 AI）
        direct_results = self._direct_query(section_title, section_desc)
        if direct_results:
            self._add_facts_to_state(state, direct_results, section_id)

        # 2. AI 深度分析 — 仅真实爬虫数据时启用（非结构化文本需要 AI 提取）
        if not self.use_mock:
            ai_facts = await self._ai_analyze(state, section)
            if ai_facts:
                self._add_facts_to_state(state, ai_facts, section_id)

        # 标记该维度已查询
        section["status"] = "researching"

    def _direct_query(self, title: str, desc: str) -> List[Dict]:
        """根据维度标题直接匹配查询（规则匹配，不调AI）"""
        facts = []

        # 定义每个数据维度的查询规则
        query_rules = {
            "销售额": self._query_sales,
            "销售": self._query_sales,
            "销量": self._query_sales,
            "收入": self._query_sales,
            "趋势": self._query_trends,
            "增长": self._query_trends,
            "商品": self._query_products,
            "品类": self._query_products,
            "产品": self._query_products,
            "排行": self._query_ranking,
            "TOP": self._query_ranking,
            "评价": self._query_reviews,
            "口碑": self._query_reviews,
            "评论": self._query_reviews,
            "竞品": self._query_competitors,
            "竞争": self._query_competitors,
            "对手": self._query_competitors,
            "达人": self._query_kol,
            "带货": self._query_kol,
            "KOL": self._query_kol,
            "价格": self._query_price,
            "定价": self._query_price,
            "退货": self._query_refunds,
            "退款": self._query_refunds,
            "售后": self._query_refunds,
            "渠道": self._query_channels,
            "平台": self._query_channels,
            "搜索": self._query_trends,
            "热词": self._query_trends,
            "趋势词": self._query_trends,
        }

        matched = False
        for keyword, query_func in query_rules.items():
            if keyword in title or keyword in desc:
                result = query_func()
                if result:
                    facts.extend(result)
                    matched = True

        # 如果没匹配到任何规则，返回通用概览
        if not matched:
            summary = self._query_summary()
            if summary:
                facts.extend(summary)

        return facts

    # ----- 各个维度的查询方法 -----

    def _query_sales(self) -> List[Dict]:
        """查询销售额相关数据"""
        sales = self.mock_data["monthly_sales"]
        facts = []

        # 自家品牌各月总销售额
        own_sales = [s for s in sales if any(p["id"] == s["product_id"] and p["is_own"] for p in self.mock_data["products"])]

        # 按月份汇总
        monthly_total = {}
        for s in own_sales:
            key = f"{s['year']}-{s['month']:02d}"
            monthly_total[key] = monthly_total.get(key, 0) + s["sales_amount"]

        months = sorted(monthly_total.keys())
        if months:
            # 最近两个月对比
            latest = months[-1]
            prev = months[-2] if len(months) >= 2 else None

            # 8月总销售额
            aug_total = sum(s["sales_amount"] for s in own_sales if s["month"] == 8)
            jul_total = sum(s["sales_amount"] for s in own_sales if s["month"] == 7)

            facts.append({
                "content": f"2024年8月总销售额: {aug_total:.0f}元，较7月({jul_total:.0f}元)变化: {(aug_total-jul_total)/jul_total*100:.1f}%",
                "source_name": "月度销售数据",
                "source_type": "report",
                "credibility_score": 0.9,
                "importance": "high",
                "data_points": [
                    {"name": "8月销售额", "value": round(aug_total, 2), "unit": "元", "year": 2024},
                    {"name": "7月销售额", "value": round(jul_total, 2), "unit": "元", "year": 2024},
                    {"name": "月度环比", "value": round((aug_total-jul_total)/jul_total*100, 1), "unit": "%", "year": 2024},
                ]
            })

            # 各渠道销售额
            channels = {}
            for s in own_sales:
                if s["month"] == 8:
                    channels[s["channel"]] = channels.get(s["channel"], 0) + s["sales_amount"]
            if channels:
                channel_str = "、".join([f"{ch}: {val:.0f}元" for ch, val in sorted(channels.items(), key=lambda x: -x[1])])
                facts.append({
                    "content": f"8月各渠道销售额: {channel_str}",
                    "source_name": "月度销售数据",
                    "source_type": "report",
                    "credibility_score": 0.9,
                    "importance": "medium",
                    "data_points": [{"name": f"{ch}销售额", "value": round(val, 2), "unit": "元", "year": 2024} for ch, val in channels.items()]
                })

        return facts

    def _query_products(self) -> List[Dict]:
        """查询商品相关数据"""
        facts = []
        products = self.mock_data["products"]
        sales = self.mock_data["monthly_sales"]

        # 自家商品列表
        own = [p for p in products if p["is_own"]]
        facts.append({
            "content": f"自家在售商品: {', '.join([p['name'] for p in own])}，共{len(own)}个SKU",
            "source_name": "商品数据",
            "source_type": "report",
            "credibility_score": 0.9,
            "importance": "high",
            "data_points": [{"name": "SKU数", "value": len(own), "unit": "个"}]
        })

        # 各商品8月销量
        for p in own:
            aug_sales = [s for s in sales if s["product_id"] == p["id"] and s["month"] == 8]
            total_qty = sum(s["sales_qty"] for s in aug_sales)
            total_amt = sum(s["sales_amount"] for s in aug_sales)

            # 同比上月
            jul_sales = [s for s in sales if s["product_id"] == p["id"] and s["month"] == 7]
            jul_qty = sum(s["sales_qty"] for s in jul_sales)

            if jul_qty > 0:
                change = (total_qty - jul_qty) / jul_qty * 100
                facts.append({
                    "content": f"{p['name']}（¥{p['price']}）: 8月销量{total_qty}件，销售额{total_amt:.0f}元，环比{jul_qty}件变化{change:+.1f}%",
                    "source_name": "月度销售数据",
                    "source_type": "report",
                    "credibility_score": 0.9,
                    "importance": "high",
                    "data_points": [
                        {"name": f"{p['name']}销量", "value": total_qty, "unit": "件", "year": 2024},
                        {"name": f"{p['name']}销售额", "value": round(total_amt, 2), "unit": "元", "year": 2024},
                        {"name": f"{p['name']}环比", "value": round(change, 1), "unit": "%", "year": 2024},
                    ]
                })

        return facts

    def _query_ranking(self) -> List[Dict]:
        """查询商品排行"""
        facts = []
        sales = self.mock_data["monthly_sales"]
        products = self.mock_data["products"]

        # 8月各商品销量排行（含竞品）
        aug_sales = [s for s in sales if s["month"] == 8]
        product_sales = {}
        for s in aug_sales:
            pid = s["product_id"]
            product_sales[pid] = product_sales.get(pid, 0) + s["sales_qty"]

        # 排序
        ranked = sorted(product_sales.items(), key=lambda x: -x[1])

        rank_str = []
        for i, (pid, qty) in enumerate(ranked[:8]):
            p = next((x for x in products if x["id"] == pid), None)
            if p:
                brand_tag = "【自】" if p["is_own"] else "【竞】"
                rank_str.append(f"{i+1}. {brand_tag}{p['brand']}-{p['name']}: {qty}件(¥{p['price']})")

        facts.append({
            "content": "8月商品销量排行TOP8:\n" + "\n".join(rank_str),
            "source_name": "月度销售数据",
            "source_type": "report",
            "credibility_score": 0.9,
            "importance": "high",
            "data_points": [
                {"name": f"{'自' if next((x for x in products if x['id']==pid), None) and next((x for x in products if x['id']==pid)).get('is_own') else '竞'}-{next((x for x in products if x['id']==pid), {}).get('name','')}销量", "value": qty, "unit": "件", "year": 2024}
                for pid, qty in ranked[:6]
            ]
        })

        return facts

    def _query_reviews(self) -> List[Dict]:
        """查询评价数据"""
        facts = []
        reviews = self.mock_data["reviews"]

        positive = [r for r in reviews if r["rating"] >= 4]
        negative = [r for r in reviews if r["rating"] <= 2]
        total = len(reviews)

        if total:
            good_ratio = len(positive) / total * 100
            bad_ratio = len(negative) / total * 100

            facts.append({
                "content": f"共{total}条评价，好评{len(positive)}条({good_ratio:.0f}%)，差评{len(negative)}条({bad_ratio:.0f}%)",
                "source_name": "用户评价数据",
                "source_type": "report",
                "credibility_score": 0.9,
                "importance": "high",
                "data_points": [
                    {"name": "评价总数", "value": total, "unit": "条"},
                    {"name": "好评率", "value": round(good_ratio, 1), "unit": "%"},
                    {"name": "差评率", "value": round(bad_ratio, 1), "unit": "%"},
                ]
            })

            # 差评关键词
            if negative:
                bad_contents = [r["content"] for r in negative]
                facts.append({
                    "content": f"差评原文: {'; '.join(bad_contents[:5])}（请AI根据差评内容提取关键词和共性问题）",
                    "source_name": "用户评价数据",
                    "source_type": "report",
                    "credibility_score": 0.9,
                    "importance": "high",
                })

            # 好评关键词
            if positive:
                good_contents = [r["content"] for r in positive[:3]]
                facts.append({
                    "content": f"好评原文: {'; '.join(good_contents)}（请AI根据好评内容提取关键词和共性特征）",
                    "source_name": "用户评价数据",
                    "source_type": "report",
                    "credibility_score": 0.9,
                    "importance": "medium",
                })

        return facts

    def _query_competitors(self) -> List[Dict]:
        """查询竞品数据"""
        facts = []
        products = self.mock_data["products"]
        sales = self.mock_data["monthly_sales"]

        competitors = [p for p in products if not p["is_own"]]
        comp_names = ", ".join([f"{p['brand']}-{p['name']}(¥{p['price']})" for p in competitors])
        facts.append({
            "content": f"识别到{len(competitors)}个竞品: {comp_names}",
            "source_name": "商品数据",
            "source_type": "report",
            "credibility_score": 0.9,
            "importance": "high",
        })

        # 竞品销量趋势
        comp_sales = [s for s in sales if any(p["id"] == s["product_id"] and not p["is_own"] for p in products)]
        for p in competitors:
            p_sales = [s for s in comp_sales if s["product_id"] == p["id"]]
            if p_sales:
                total_qty = sum(s["sales_qty"] for s in p_sales if s["month"] == 8)
                prev_qty = sum(s["sales_qty"] for s in p_sales if s["month"] == 7)
                change = ((total_qty - prev_qty) / prev_qty * 100) if prev_qty > 0 else 0
                facts.append({
                    "content": f"竞品{p['brand']}-{p['name']}(¥{p['price']}): 8月销量{total_qty}件，环比{change:+.1f}%",
                    "source_name": "月度销售数据",
                    "source_type": "report",
                    "credibility_score": 0.9,
                    "importance": "high",
                    "data_points": [
                        {"name": f"{p['brand']}-{p['name']}销量", "value": total_qty, "unit": "件", "year": 2024},
                        {"name": f"{p['brand']}环比", "value": round(change, 1), "unit": "%"},
                    ]
                })

        return facts

    def _query_kol(self) -> List[Dict]:
        """查询达人带货数据"""
        facts = []
        kol_data = self.mock_data["kol_data"]

        if kol_data:
            facts.append({
                "content": f"共有{len(kol_data)}条达人合作记录，平台涵盖抖音、小红书",
                "source_name": "达人带货数据",
                "source_type": "report",
                "credibility_score": 0.9,
                "importance": "medium",
            })

            # ROI排序
            sorted_kol = sorted(kol_data, key=lambda x: -x["roi"])
            best = sorted_kol[0]
            worst = sorted_kol[-1]

            facts.append({
                "content": f"ROI最高: {best['kol_name']}({best['followers']/10000:.0f}万粉) ROI={best['roi']}，合作费{best['fee']}元，预估GMV{best['estimated_gmv']:.0f}元",
                "source_name": "达人带货数据",
                "source_type": "report",
                "credibility_score": 0.9,
                "importance": "high",
                "data_points": [
                    {"name": f"{best['kol_name']}ROI", "value": best['roi'], "unit": ""},
                    {"name": f"{best['kol_name']}GMV", "value": best['estimated_gmv'], "unit": "元"},
                ]
            })

            facts.append({
                "content": f"ROI最低: {worst['kol_name']}({worst['followers']/10000:.0f}万粉) ROI={worst['roi']}，合作费{worst['fee']}元，预估GMV{worst['estimated_gmv']:.0f}元，需评估是否续约",
                "source_name": "达人带货数据",
                "source_type": "report",
                "credibility_score": 0.9,
                "importance": "medium",
                "data_points": [
                    {"name": f"{worst['kol_name']}ROI", "value": worst['roi'], "unit": ""},
                    {"name": f"{worst['kol_name']}GMV", "value": worst['estimated_gmv'], "unit": "元"},
                ]
            })

            # 竞品达人
            comp_kol = [k for k in kol_data if k["product_id"] == "p006"]
            if comp_kol:
                facts.append({
                    "content": f"竞品'冰感科技'合作的达人: {', '.join([k['kol_name'] for k in comp_kol])}，其中{comp_kol[0]['kol_name']}({comp_kol[0]['followers']/10000:.0f}万粉)预估带货{comp_kol[0]['estimated_sales']}件",
                    "source_name": "达人带货数据",
                    "source_type": "report",
                    "credibility_score": 0.9,
                    "importance": "high",
                })

        return facts

    def _query_price(self) -> List[Dict]:
        """查询价格对比数据"""
        facts = []
        price_data = self.mock_data["price_monitoring"]

        for p in price_data:
            direction = "低于" if p["price_diff"] < 0 else "高于"
            facts.append({
                "content": f"我们的{p['product_id']}(¥{p['our_price']}) {direction}竞品{p['competitor_product']}(¥{p['comp_price']})，差价{abs(p['price_diff'])}元",
                "source_name": "价格监控数据",
                "source_type": "report",
                "credibility_score": 0.9,
                "importance": "medium",
                "data_points": [
                    {"name": "我们的价格", "value": p["our_price"], "unit": "元"},
                    {"name": "竞品价格", "value": p["comp_price"], "unit": "元"},
                    {"name": "价差", "value": p["price_diff"], "unit": "元"},
                ]
            })

        return facts

    def _query_refunds(self) -> List[Dict]:
        """查询退货数据"""
        facts = []
        refunds = self.mock_data["refunds"]

        if refunds:
            total_amt = sum(r["refund_amount"] for r in refunds)
            # 退货原因统计
            reasons = {}
            for r in refunds:
                cause = r["reason"]
                reasons[cause] = reasons.get(cause, 0) + 1
            top_reason = sorted(reasons.items(), key=lambda x: -x[1])[0]

            facts.append({
                "content": f"共{len(refunds)}笔退货，退货总金额{total_amt:.0f}元。主要退货原因: {top_reason[0]}({top_reason[1]}次)",
                "source_name": "退货数据",
                "source_type": "report",
                "credibility_score": 0.9,
                "importance": "medium",
                "data_points": [
                    {"name": "退货笔数", "value": len(refunds), "unit": "笔"},
                    {"name": "退货金额", "value": round(total_amt, 2), "unit": "元"},
                ]
            })

        return facts

    def _query_channels(self) -> List[Dict]:
        """查询渠道数据"""
        facts = []
        sales = self.mock_data["monthly_sales"]

        # 各渠道8月销售
        channel_sales = {}
        for s in sales:
            if s["month"] == 8:
                channel_sales[s["channel"]] = channel_sales.get(s["channel"], 0) + s["sales_amount"]

        if channel_sales:
            total = sum(channel_sales.values())
            channel_ranks = sorted(channel_sales.items(), key=lambda x: -x[1])
            rank_str = " > ".join([f"{ch}({val/total*100:.0f}%)" for ch, val in channel_ranks])
            facts.append({
                "content": f"8月各渠道销售额占比: {rank_str}",
                "source_name": "月度销售数据",
                "source_type": "report",
                "credibility_score": 0.9,
                "importance": "high",
                "data_points": [
                    {"name": f"{ch}占比", "value": round(val/total*100, 1), "unit": "%", "year": 2024}
                    for ch, val in channel_ranks
                ]
            })

        return facts

    def _query_trends(self) -> List[Dict]:
        """查询搜索趋势数据"""
        facts = []
        keywords = self.mock_data["trend_keywords"]

        # 按关键词分组
        kw_groups = {}
        for k in keywords:
            kw_groups.setdefault(k["keyword"], []).append(k)

        for kw, data in kw_groups.items():
            data.sort(key=lambda x: x["month"])
            values = [d["search_index"] for d in data]
            start_val = values[0]
            end_val = values[-1]
            growth = (end_val - start_val) / start_val * 100

            trend_line = " → ".join([str(d["search_index"]) for d in data])
            direction = "上升" if growth > 0 else "下降"
            facts.append({
                "content": f"搜索词'{kw}'搜索趋势(3-8月): {trend_line}，整体{direction}{abs(growth):.0f}%",
                "source_name": "搜索趋势数据",
                "source_type": "report",
                "credibility_score": 0.9,
                "importance": "high",
                "data_points": [
                    {"name": f"'{kw}'搜索量", "value": v, "unit": "搜索指数", "year": 2024, "month": data[i]["month"]}
                    for i, v in enumerate(values)
                ]
            })

        return facts

    def _query_summary(self) -> List[Dict]:
        """通用数据概览"""
        products = self.mock_data["products"]
        sales = self.mock_data["monthly_sales"]
        reviews = self.mock_data["reviews"]

        own_count = sum(1 for p in products if p["is_own"])
        comp_count = sum(1 for p in products if not p["is_own"])

        # 总销售额
        own_sales = [s for s in sales if any(p["id"] == s["product_id"] and p["is_own"] for p in products)]
        total_revenue = sum(s["sales_amount"] for s in own_sales)

        return [{
            "content": f"数据概览: 自家商品{own_count}个，竞品{comp_count}个，总销售额{total_revenue:.0f}元，评价{len(reviews)}条",
            "source_name": "数据概览",
            "source_type": "report",
            "credibility_score": 0.9,
            "importance": "high",
        }]

    async def _ai_analyze(self, state: ResearchState, section: Dict) -> List[Dict]:
        """用AI做深度分析，发现数据中的趋势和洞察"""
        section_title = section.get("title", "")
        section_desc = section.get("description", "")

        # 构造AI分析用的数据摘要
        data_summary = self._build_data_summary()

        prompt = self.DATA_ANALYSIS_PROMPT.format(
            query=state["query"],
            section_title=section_title,
            section_description=section_desc,
            available_data=data_summary
        )

        response = await self.call_llm(
            system_prompt="你是电商数据分析师，擅长从数据中发现业务洞察。",
            user_prompt=prompt,
            json_mode=True,
            temperature=0.3,
            max_tokens=8000
        )

        result = self.parse_json_response(response)
        if not result:
            return []

        facts = result.get("extracted_facts", [])

        # 提取数据点
        for fact in facts:
            for dp in fact.get("data_points", []):
                if "id" not in dp:
                    dp["id"] = f"dp_{uuid.uuid4().hex[:8]}"

        return facts

    def _build_data_summary(self) -> str:
        """构造给AI看的数据摘要"""
        data = self.mock_data
        lines = []

        # 商品
        own = [p for p in data["products"] if p["is_own"]]
        comp = [p for p in data["products"] if not p["is_own"]]
        lines.append("【商品数据】")
        own_products_str = ', '.join([p['name'] + '¥' + str(p['price']) for p in own])
        lines.append(f'自家商品: {own_products_str}')
        comp_products_str = ', '.join([p['brand'] + '-' + p['name'] + '¥' + str(p['price']) for p in comp])
        lines.append(f'竞品商品: {comp_products_str}')

        # 月度销售
        lines.append("\n【月度销售数据(自家)】")
        own_sales = [s for s in data["monthly_sales"] if any(p["id"] == s["product_id"] and p["is_own"] for p in data["products"])]
        for s in own_sales:
            lines.append(f"  {s['year']}年{s['month']}月 {s['channel']}: {s['product_id']} 销量{s['sales_qty']} 金额{s['sales_amount']}")

        # 竞品月度销售
        comp_sales = [s for s in data["monthly_sales"] if any(p["id"] == s["product_id"] and not p["is_own"] for p in data["products"])]
        if comp_sales:
            lines.append("\n【月度销售数据(竞品)】")
            for s in comp_sales:
                lines.append(f"  {s['year']}年{s['month']}月 {s['channel']}: {s['product_id']} 销量{s['sales_qty']} 金额{s['sales_amount']}")

        # 评价摘要
        reviews = data["reviews"]
        positive = [r for r in reviews if r["rating"] >= 4]
        negative = [r for r in reviews if r["rating"] <= 2]
        lines.append(f"\n【评价数据】共{len(reviews)}条，好评{len(positive)}条，差评{len(negative)}条")
        if negative:
            lines.append(f"差评内容: {'; '.join([r['content'] for r in negative[:5]])}")

        # 达人数据
        kol = data["kol_data"]
        if kol:
            lines.append("\n【达人带货数据】")
            for k in kol:
                lines.append(f"  {k['kol_name']}({k['platform']}, {k['followers']/10000:.0f}万粉) GMV{k['estimated_gmv']:.0f} 费用{k['fee']} ROI={k['roi']}")

        # 价格监控
        price = data["price_monitoring"]
        if price:
            lines.append("\n【价格监控】")
            for p in price:
                lines.append(f"  {p['product_id']} vs {p['competitor_product']}: 我们¥{p['our_price']} vs 竞品¥{p['comp_price']}")

        # 退货
        refunds = data["refunds"]
        if refunds:
            lines.append(f"\n【退货数据】共{len(refunds)}笔")
            for r in refunds:
                lines.append(f"  {r['order_id']}: {r['reason']} ¥{r['refund_amount']}")

        # 搜索趋势
        keywords = data["trend_keywords"]
        if keywords:
            lines.append("\n【搜索趋势】")
            kw_groups = {}
            for k in keywords:
                kw_groups.setdefault(k["keyword"], []).append(k)
            for kw, vals in kw_groups.items():
                vals.sort(key=lambda x: x["month"])
                trend = " → ".join([str(v["search_index"]) for v in vals])
                lines.append(f"  '{kw}': {trend}")

        return "\n".join(lines)

    def _add_facts_to_state(self, state: ResearchState, facts: List[Dict], section_id: str) -> None:
        """将查询结果添加到state"""
        for fact in facts:
            if not fact.get("content"):
                continue

            fact_entry = {
                "id": f"fact_{uuid.uuid4().hex[:8]}",
                "content": fact["content"],
                "source_url": fact.get("source_url", ""),
                "source_name": fact.get("source_name", "电商数据"),
                "source_type": fact.get("source_type", "report"),
                "credibility_score": fact.get("credibility_score", 0.9),
                "extracted_at": datetime.now().isoformat(),
                "related_sections": [section_id],
                "verified": True,
                "metadata": {},
            }
            state["facts"].append(fact_entry)

            # 提取数据点
            for dp in fact.get("data_points", []):
                data_point = {
                    "id": f"dp_{uuid.uuid4().hex[:8]}",
                    "name": dp.get("name", ""),
                    "value": dp.get("value", ""),
                    "unit": dp.get("unit", ""),
                    "year": dp.get("year"),
                    "source": "电商mock数据",
                    "confidence": 0.9,
                }
                state["data_points"].append(data_point)

        # 发送查询进度
        self.add_message(state, "search_progress", {
            "agent": self.name,
            "results_count": len(facts),
            "section_id": section_id,
        })
