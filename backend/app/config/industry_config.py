
"""
行业配置 - 定义各行业的搜索关键词
"""
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class IndustryConfig:
    """行业配置"""
    id: str
    name: str
    description: str
    news_keywords: List[str]
    bidding_keywords: List[str]
    research_keywords: List[str]


# 预定义的电商品类配置
INDUSTRY_CONFIGS: Dict[str, IndustryConfig] = {
    "fashion": IndustryConfig(
        id="fashion",
        name="服装鞋包",
        description="防晒衣、连衣裙、运动鞋、箱包等品类运营分析",
        news_keywords=[
            "防晒衣 市场趋势",
            "女装 爆款",
            "运动鞋 销量",
            "服装 直播带货",
            "鞋包 竞品分析",
            "服饰 达人种草",
        ],
        bidding_keywords=["服装供应链", "服饰代工", "面料采购", "鞋类代工"],
        research_keywords=["服装", "鞋包", "防晒衣", "连衣裙", "运动鞋"],
    ),
    "beauty": IndustryConfig(
        id="beauty",
        name="美妆个护",
        description="护肤品、彩妆、洗发水、身体护理等品类运营分析",
        news_keywords=[
            "护肤品 市场趋势",
            "彩妆 爆款",
            "面膜 销量",
            "美妆 直播带货",
            "精华 竞品分析",
            "个护 达人种草",
        ],
        bidding_keywords=["化妆品代工", "护肤品原料", "彩妆OEM", "个护代工"],
        research_keywords=["美妆", "护肤", "彩妆", "面膜", "精华液"],
    ),
    "digital": IndustryConfig(
        id="digital",
        name="数码家电",
        description="手机、耳机、小家电、智能穿戴等品类运营分析",
        news_keywords=[
            "TWS耳机 市场趋势",
            "小家电 爆款",
            "智能手表 销量",
            "数码 直播带货",
            "手机配件 竞品分析",
            "家电 达人种草",
        ],
        bidding_keywords=["电子产品代工", "小家电OEM", "数码配件采购"],
        research_keywords=["数码", "家电", "耳机", "智能手表", "小家电"],
    ),
    "food": IndustryConfig(
        id="food",
        name="食品饮料",
        description="零食、茶饮、保健品、预制菜等品类运营分析",
        news_keywords=[
            "零食 市场趋势",
            "茶饮 爆款",
            "保健品 销量",
            "食品 直播带货",
            "预制菜 竞品分析",
            "饮料 达人种草",
        ],
        bidding_keywords=["食品代工", "饮料OEM", "零食采购", "保健品代工"],
        research_keywords=["食品", "饮料", "零食", "茶饮", "保健品"],
    ),
}

# 默认品类
DEFAULT_INDUSTRY_ID = "fashion"


def get_industry_config(industry_id: Optional[str] = None) -> IndustryConfig:
    """
    获取行业配置

    Args:
        industry_id: 行业ID，如果为空则返回默认行业

    Returns:
        行业配置
    """
    if not industry_id:
        industry_id = DEFAULT_INDUSTRY_ID

    config = INDUSTRY_CONFIGS.get(industry_id)
    if not config:
        logger.warning(f"[industry_config] 未找到行业配置: {industry_id}, 使用默认行业")
        config = INDUSTRY_CONFIGS[DEFAULT_INDUSTRY_ID]

    logger.info(f"[industry_config] 获取行业配置: {config.name} ({config.id})")
    return config


def get_all_industries() -> List[Dict]:
    """
    获取所有行业列表

    Returns:
        行业列表
    """
    return [
        {
            "id": config.id,
            "name": config.name,
            "description": config.description,
        }
        for config in INDUSTRY_CONFIGS.values()
    ]
