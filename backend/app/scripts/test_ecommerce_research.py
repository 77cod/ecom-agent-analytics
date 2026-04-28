"""
电商运营分析 V2.0 端到端测试

测试电商版多智能体协作流程：
1. ChiefArchitect - 规划分析维度
2. DataQueryer - 查询电商 mock 数据
3. DataAnalyst - 提取结构化数据
4. CodeWizard - 数据可视化
5. LeadWriter - 撰写运营分析报告
6. CriticMaster - 审核质量

使用方法：
    python -m scripts.test_ecommerce_research
"""

import os
import sys
import asyncio
import json
import logging
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger("Ecommerce_Test")


def print_json(data, indent=2):
    """格式化打印 JSON"""
    print(json.dumps(data, ensure_ascii=False, indent=indent))


async def test_data_queryer_only():
    """只测试 DataQueryer（不调AI，纯看数据查询逻辑）"""
    print("\n" + "=" * 60)
    print("1. 测试 DataQueryer 直接数据查询")
    print("=" * 60)

    from service.deep_research_v2.state import create_initial_state
    from service.deep_research_v2.agents.data_queryer import DataQueryer

    dashscope_key = os.getenv("DASHSCOPE_API_KEY")
    if not dashscope_key:
        print("跳过（无 DASHSCOPE_API_KEY）")
        return False
    queryer = DataQueryer(dashscope_key, "https://dashscope.aliyuncs.com/compatible-mode/v1", "qwen-max")

    state = create_initial_state("防晒衣销售分析", "test-ecommerce-1")

    # 模拟大纲（电商分析维度）
    state["outline"] = [
        {"id": "sec_1", "title": "销售概况", "description": "分析各月销售额和趋势",
         "status": "pending", "section_type": "mixed", "requires_chart": True, "search_queries": []},
        {"id": "sec_2", "title": "商品排行", "description": "各商品销量排名和环比变化",
         "status": "pending", "section_type": "mixed", "requires_chart": True, "search_queries": []},
        {"id": "sec_3", "title": "用户评价", "description": "好评率、差评关键词分析",
         "status": "pending", "section_type": "qualitative", "requires_chart": False, "search_queries": []},
        {"id": "sec_4", "title": "竞品分析", "description": "竞品销量和价格对比",
         "status": "pending", "section_type": "mixed", "requires_chart": True, "search_queries": []},
        {"id": "sec_5", "title": "达人带货", "description": "达人合作ROI分析",
         "status": "pending", "section_type": "quantitative", "requires_chart": True, "search_queries": []},
    ]

    state["phase"] = "researching"
    result = await queryer.process(state)

    facts = result.get("facts", [])
    data_points = result.get("data_points", [])

    print(f"\n查询结果:")
    print(f"  事实数: {len(facts)}")
    print(f"  数据点数: {len(data_points)}")

    if facts:
        print(f"\n前10条事实:")
        for i, f in enumerate(facts[:10]):
            print(f"  [{i+1}] {f['content'][:80]}...")
            if f.get("data_points"):
                for dp in f["data_points"]:
                    print(f"      数据点: {dp.get('name')} = {dp.get('value')} {dp.get('unit', '')}")

    print("\n✅ DataQueryer 直接查询测试完成!")
    return True


async def test_ecommerce_full_workflow():
    """测试完整的电商分析流程"""
    print("\n" + "=" * 60)
    print("2. 电商运营分析端到端测试")
    print("=" * 60)

    dashscope_key = os.getenv("DASHSCOPE_API_KEY")
    if not dashscope_key:
        print("跳过（无 DASHSCOPE_API_KEY）")
        return False

    from service.deep_research_v2.service import DeepResearchV2Service

    service = DeepResearchV2Service(
        llm_api_key=dashscope_key,
        search_api_key="mock",
        model="qwen-max",
        max_iterations=1
    )

    query = "防晒衣品牌'夏日轻盈'的8月经营分析，重点关注销售额趋势、商品表现和竞品动态"
    print(f"\n分析查询: {query}")
    print("-" * 60)

    events = []
    phases_seen = set()
    error_count = 0
    reports = ""

    start_time = datetime.now()

    try:
        async for sse_data in service.research(query):
            if sse_data.startswith("data: "):
                data_str = sse_data[6:].strip()
                if data_str == "[DONE]":
                    break

                try:
                    event = json.loads(data_str)
                    events.append(event)
                    event_type = event.get("type", "")

                    if event_type == "phase":
                        phase = event.get("phase", "")
                        phases_seen.add(phase)
                        print(f"\n--- {phase}: {event.get('content', '')}")

                    elif event_type == "outline":
                        outline = event.get("outline", [])
                        print(f"\n分析维度:")
                        for i, s in enumerate(outline, 1):
                            print(f"  {i}. {s.get('title')}")

                    elif event_type == "thought":
                        content = event.get("content", {}).get("content", "")
                        if content:
                            print(f"  -> {content}")

                    elif event_type == "observation":
                        obs = event.get("content", {})
                        facts = obs.get("facts_count", 0)
                        insights = obs.get("insights", [])
                        print(f"  -> 提取了 {facts} 条事实")
                        if insights:
                            for ins in insights[:2]:
                                print(f"     洞察: {ins}")

                    elif event_type == "chart":
                        title = event.get("title", "未知")
                        print(f"   [图表] {title}")

                    elif event_type == "research_complete":
                        reports = event.get("final_report", "")
                        quality = event.get("quality_score", 0)
                        facts_count = event.get("facts_count", 0)
                        charts_count = event.get("charts_count", 0)
                        print(f"\n分析完成:")
                        print(f"  质量: {quality}")
                        print(f"  事实: {facts_count}")
                        print(f"  图表: {charts_count}")
                        print(f"  报告: {len(reports)} 字符")

                    elif event_type == "error":
                        error_count += 1
                        print(f"  **错误: {event.get('content', '')}")

                except json.JSONDecodeError:
                    pass

    except Exception as e:
        print(f"\n异常: {e}")
        import traceback
        traceback.print_exc()
        return False

    elapsed = (datetime.now() - start_time).total_seconds()

    print("\n" + "=" * 60)
    print("测试结果")
    print("=" * 60)
    print(f"耗时: {elapsed:.0f}秒")
    print(f"事件: {len(events)}")
    print(f"阶段: {', '.join(sorted(phases_seen))}")
    print(f"错误: {error_count}")

    has_report = len(reports) > 100
    print(f"\n生成报告: {'是' if has_report else '否'}")

    if reports:
        print(f"\n报告预览（前500字）:")
        print("-" * 40)
        print(reports[:500])

    if has_report and error_count == 0:
        print("\n✅ 测试通过!")
        return True
    else:
        print("\n❌ 测试未完全通过")
        return False


async def main():
    print("=" * 60)
    print("电商运营分析系统 V2.0 测试")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # 步骤1: 测试 DataQueryer 数据查询
    q1 = await test_data_queryer_only()

    # 步骤2: 完整流程（需要 API Key）
    q2 = await test_ecommerce_full_workflow()

    print("\n" + "=" * 60)
    print("总结")
    print("=" * 60)
    print(f"DataQueryer 直接查询: {'通过' if q1 else '失败'}")
    print(f"端到端分析流程: {'通过' if q2 else '跳过/失败'}")


if __name__ == "__main__":
    asyncio.run(main())
