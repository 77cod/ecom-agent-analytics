"""
电商运营分析 - Mock 数据集

模拟一个防晒衣品牌"夏日轻盈"的经营数据，包含：
- 商品数据（自家 + 竞品）
- 月度销售数据
- 各平台订单明细
- 用户评价
- 达人带货数据
- 价格监控

数据中埋了一些"问题"和"机会点"，方便AI分析时发现：
1. 主打商品销量连续2个月下滑
2. 竞品价格更低且在增长
3. 差评集中在"发货慢"和"尺码偏小"
4. 某个达人ROI特别高，值得追加投放
5. "冰感"关键词正在上升为新趋势
"""

import uuid
from datetime import datetime, timedelta
import random

random.seed(42)

# ============================================================
# 1. 商品数据
# ============================================================
PRODUCTS = [
    # 自家商品
    {"id": "p001", "name": "夏日轻盈冰感防晒衣-经典款", "brand": "夏日轻盈", "category": "防晒衣",
     "price": 129.0, "cost": 55.0, "stock": 3200, "is_own": True},
    {"id": "p002", "name": "夏日轻盈冰感防晒衣-升级款", "brand": "夏日轻盈", "category": "防晒衣",
     "price": 179.0, "cost": 72.0, "stock": 1800, "is_own": True},
    {"id": "p003", "name": "夏日轻盈冰感防晒衣-亲子款", "brand": "夏日轻盈", "category": "防晒衣",
     "price": 229.0, "cost": 95.0, "stock": 600, "is_own": True},
    {"id": "p004", "name": "夏日轻盈防晒冰袖", "brand": "夏日轻盈", "category": "防晒配件",
     "price": 29.9, "cost": 12.0, "stock": 5000, "is_own": True},
    {"id": "p005", "name": "夏日轻盈防晒渔夫帽", "brand": "夏日轻盈", "category": "防晒配件",
     "price": 49.9, "cost": 20.0, "stock": 2500, "is_own": True},
    # 竞品商品
    {"id": "p006", "name": "冰感科技超薄防晒衣", "brand": "冰感科技", "category": "防晒衣",
     "price": 99.0, "cost": 40.0, "stock": 5000, "is_own": False},
    {"id": "p007", "name": "冰感科技防晒衣pro版", "brand": "冰感科技", "category": "防晒衣",
     "price": 149.0, "cost": 60.0, "stock": 3000, "is_own": False},
    {"id": "p008", "name": "户外极客超轻防晒衣", "brand": "户外极客", "category": "防晒衣",
     "price": 159.0, "cost": 68.0, "stock": 2200, "is_own": False},
    {"id": "p009", "name": "户外极客防晒冰袖", "brand": "户外极客", "category": "防晒配件",
     "price": 19.9, "cost": 8.0, "stock": 8000, "is_own": False},
    {"id": "p010", "name": "都市轻行防晒衣", "brand": "都市轻行", "category": "防晒衣",
     "price": 199.0, "cost": 85.0, "stock": 1500, "is_own": False},
]


# ============================================================
# 2. 月度销售汇总（2024年3月-8月，共6个月）
# ============================================================
MONTHLY_SALES = [
    # 自家品牌 - 经典款
    {"product_id": "p001", "year": 2024, "month": 3, "sales_qty": 850, "sales_amount": 109650.0, "channel": "天猫"},
    {"product_id": "p001", "year": 2024, "month": 4, "sales_qty": 1200, "sales_amount": 154800.0, "channel": "天猫"},
    {"product_id": "p001", "year": 2024, "month": 5, "sales_qty": 2100, "sales_amount": 270900.0, "channel": "天猫"},
    {"product_id": "p001", "year": 2024, "month": 6, "sales_qty": 3500, "sales_amount": 451500.0, "channel": "天猫"},
    {"product_id": "p001", "year": 2024, "month": 7, "sales_qty": 3800, "sales_amount": 490200.0, "channel": "天猫"},
    {"product_id": "p001", "year": 2024, "month": 8, "sales_qty": 2800, "sales_amount": 361200.0, "channel": "天猫"},  # 下滑！
    # 自家品牌 - 经典款(抖音)
    {"product_id": "p001", "year": 2024, "month": 3, "sales_qty": 200, "sales_amount": 25800.0, "channel": "抖音"},
    {"product_id": "p001", "year": 2024, "month": 4, "sales_qty": 450, "sales_amount": 58050.0, "channel": "抖音"},
    {"product_id": "p001", "year": 2024, "month": 5, "sales_qty": 800, "sales_amount": 103200.0, "channel": "抖音"},
    {"product_id": "p001", "year": 2024, "month": 6, "sales_qty": 1500, "sales_amount": 193500.0, "channel": "抖音"},
    {"product_id": "p001", "year": 2024, "month": 7, "sales_qty": 2200, "sales_amount": 283800.0, "channel": "抖音"},
    {"product_id": "p001", "year": 2024, "month": 8, "sales_qty": 1800, "sales_amount": 232200.0, "channel": "抖音"},  # 下滑

    # 自家品牌 - 升级款
    {"product_id": "p002", "year": 2024, "month": 5, "sales_qty": 300, "sales_amount": 53700.0, "channel": "天猫"},
    {"product_id": "p002", "year": 2024, "month": 6, "sales_qty": 600, "sales_amount": 107400.0, "channel": "天猫"},
    {"product_id": "p002", "year": 2024, "month": 7, "sales_qty": 900, "sales_amount": 161100.0, "channel": "天猫"},
    {"product_id": "p002", "year": 2024, "month": 8, "sales_qty": 750, "sales_amount": 134250.0, "channel": "天猫"},

    # 竞品 - 冰感科技超薄款（快速上升！）
    {"product_id": "p006", "year": 2024, "month": 3, "sales_qty": 600, "sales_amount": 59400.0, "channel": "天猫"},
    {"product_id": "p006", "year": 2024, "month": 4, "sales_qty": 1100, "sales_amount": 108900.0, "channel": "天猫"},
    {"product_id": "p006", "year": 2024, "month": 5, "sales_qty": 2000, "sales_amount": 198000.0, "channel": "天猫"},
    {"product_id": "p006", "year": 2024, "month": 6, "sales_qty": 3200, "sales_amount": 316800.0, "channel": "天猫"},
    {"product_id": "p006", "year": 2024, "month": 7, "sales_qty": 4000, "sales_amount": 396000.0, "channel": "天猫"},  # 反超！
    {"product_id": "p006", "year": 2024, "month": 8, "sales_qty": 4200, "sales_amount": 415800.0, "channel": "天猫"},  # 继续涨！

    # 竞品 - 冰感科技抖音
    {"product_id": "p006", "year": 2024, "month": 6, "sales_qty": 1800, "sales_amount": 178200.0, "channel": "抖音"},
    {"product_id": "p006", "year": 2024, "month": 7, "sales_qty": 2800, "sales_amount": 277200.0, "channel": "抖音"},
    {"product_id": "p006", "year": 2024, "month": 8, "sales_qty": 3500, "sales_amount": 346500.0, "channel": "抖音"},
]


# ============================================================
# 3. 订单明细（最近100条订单）
# ============================================================
def _gen_orders():
    """生成模拟订单数据"""
    channels = ["天猫", "京东", "抖音", "拼多多", "小红书"]
    cities = ["上海", "北京", "广州", "深圳", "杭州", "成都", "武汉",
              "南京", "重庆", "苏州", "西安", "长沙", "东莞", "郑州", "佛山"]
    statuses = ["已完成", "已完成", "已完成", "已完成", "已完成",
                "已完成", "已完成", "已完成", "退货中", "已退货"]

    orders = []
    base_date = datetime(2024, 8, 20)
    product_ids = ["p001", "p002", "p003", "p004", "p005"]

    for i in range(100):
        pid = random.choice(product_ids)
        product = next(p for p in PRODUCTS if p["id"] == pid)
        qty = random.choices([1, 1, 1, 1, 2, 2, 3], weights=[30, 30, 15, 10, 8, 5, 2])[0]
        date = base_date - timedelta(days=random.randint(0, 60))
        channel = random.choice(channels)
        city = random.choice(cities)
        status = random.choice(statuses)
        total = round(product["price"] * qty, 2)
        is_refund = status in ("退货中", "已退货")

        orders.append({
            "order_id": f"ORD2024{i+1:04d}",
            "product_id": pid,
            "product_name": product["name"],
            "brand": product["brand"],
            "category": product["category"],
            "price": product["price"],
            "quantity": qty,
            "total_amount": total,
            "channel": channel,
            "city": city,
            "order_date": date.strftime("%Y-%m-%d"),
            "status": status,
            "is_refund": is_refund,
        })

    return orders

ORDERS = _gen_orders()


# ============================================================
# 4. 用户评价（含好评和差评，有故事性）
# ============================================================
REVIEWS = [
    # 正面评价
    {"id": "r001", "product_id": "p001", "rating": 5, "content": "很薄很透气，夏天穿完全不热，防晒效果也不错",
     "date": "2024-07-15", "source": "天猫"},
    {"id": "r002", "product_id": "p001", "rating": 5, "content": "第二次买了，给爸妈也各买了一件，冰感效果明显",
     "date": "2024-07-20", "source": "天猫"},
    {"id": "r003", "product_id": "p001", "rating": 4, "content": "质量不错，颜色好看，就是有点薄，不过防晒衣本来就这样的",
     "date": "2024-07-22", "source": "天猫"},
    {"id": "r004", "product_id": "p002", "rating": 5, "content": "升级款面料更好，摸起来很舒服，版型也好看",
     "date": "2024-08-01", "source": "天猫"},
    {"id": "r005", "product_id": "p004", "rating": 5, "content": "冰袖很实用，开车必备，性价比很高",
     "date": "2024-08-05", "source": "天猫"},
    {"id": "r006", "product_id": "p001", "rating": 5, "content": "跟着抖音博主买的，确实不错，推荐",
     "date": "2024-08-10", "source": "抖音"},
    {"id": "r007", "product_id": "p002", "rating": 4, "content": "价格小贵但品质对得起价格，UPF50+认证靠谱",
     "date": "2024-08-12", "source": "天猫"},
    {"id": "r008", "product_id": "p005", "rating": 5, "content": "帽子好看又防晒，去海边玩了三天没晒黑",
     "date": "2024-08-15", "source": "京东"},
    {"id": "r009", "product_id": "p001", "rating": 5, "content": "冰感效果真的绝，在太阳底下走明显感觉比没穿凉快",
     "date": "2024-08-18", "source": "天猫"},
    {"id": "r010", "product_id": "p003", "rating": 4, "content": "亲子款设计很贴心，孩子很喜欢，面料安全放心",
     "date": "2024-08-20", "source": "天猫"},

    # 差评（有故事性）
    {"id": "r011", "product_id": "p001", "rating": 2, "content": "尺码偏小！按照身高体重买的L码，结果穿不上，换货又等了5天",
     "date": "2024-08-08", "source": "天猫"},
    {"id": "r012", "product_id": "p001", "rating": 1, "content": "发货太慢了，下单后4天才发货，等了一周才收到，夏天都快过了",
     "date": "2024-08-11", "source": "天猫"},
    {"id": "r013", "product_id": "p001", "rating": 2, "content": "和描述不太一致，说是冰感但穿着感觉一般，不如同事买的冰感科技",
     "date": "2024-08-14", "source": "天猫"},
    {"id": "r014", "product_id": "p001", "rating": 1, "content": "洗了一次就起球了，质量堪忧，这个价位不如买别的牌子",
     "date": "2024-08-16", "source": "抖音"},
    {"id": "r015", "product_id": "p002", "rating": 2, "content": "升级款也没觉得哪里升级了，价格贵了50块，性价比不高",
     "date": "2024-08-19", "source": "天猫"},
    {"id": "r016", "product_id": "p001", "rating": 1, "content": "客服态度差，问尺码问题半天不回，回复了也很敷衍",
     "date": "2024-08-21", "source": "京东"},
    {"id": "r017", "product_id": "p004", "rating": 2, "content": "冰袖用了一周就起毛了，质量不行",
     "date": "2024-08-22", "source": "天猫"},
    {"id": "r018", "product_id": "p001", "rating": 3, "content": "一般般吧，没有想象中好，凑合穿",
     "date": "2024-08-23", "source": "天猫"},
    {"id": "r019", "product_id": "p001", "rating": 2, "content": "和图片有色差，实物偏黄，不太喜欢",
     "date": "2024-08-25", "source": "抖音"},
    {"id": "r020", "product_id": "p002", "rating": 1, "content": "这个价格我在冰感科技可以买两件了，性价比差太多",
     "date": "2024-08-26", "source": "天猫"},
]


# ============================================================
# 5. 达人带货数据
# ============================================================
KOL_DATA = [
    {"kol_name": "户外运动小鱼儿", "platform": "抖音", "followers": 85_0000, "product_id": "p001",
     "commission_rate": 0.15, "estimated_sales": 1200, "estimated_gmv": 154800.0,
     "fee": 8000, "roi": 19.35, "cooperation_date": "2024-07-10", "niche": "户外运动"},

    {"kol_name": "时尚穿搭琳达", "platform": "抖音", "followers": 220_0000, "product_id": "p001",
     "commission_rate": 0.20, "estimated_sales": 800, "estimated_gmv": 103200.0,
     "fee": 15000, "roi": 6.88, "cooperation_date": "2024-07-20", "niche": "时尚穿搭"},

    {"kol_name": "小李测评", "platform": "抖音", "followers": 150_0000, "product_id": "p002",
     "commission_rate": 0.18, "estimated_sales": 450, "estimated_gmv": 80550.0,
     "fee": 12000, "roi": 6.71, "cooperation_date": "2024-08-01", "niche": "好物推荐"},

    {"kol_name": "宝妈生活日记", "platform": "小红书", "followers": 35_0000, "product_id": "p003",
     "commission_rate": 0.12, "estimated_sales": 180, "estimated_gmv": 41220.0,
     "fee": 3000, "roi": 13.74, "cooperation_date": "2024-07-25", "niche": "母婴亲子"},

    {"kol_name": "大学生日常", "platform": "小红书", "followers": 12_0000, "product_id": "p001",
     "commission_rate": 0.10, "estimated_sales": 90, "estimated_gmv": 11610.0,
     "fee": 1500, "roi": 7.74, "cooperation_date": "2024-08-05", "niche": "学生日常"},

    {"kol_name": "健身教练阿强", "platform": "抖音", "followers": 300_0000, "product_id": "p005",
     "commission_rate": 0.15, "estimated_sales": 600, "estimated_gmv": 29940.0,
     "fee": 20000, "roi": 1.50, "cooperation_date": "2024-08-10", "niche": "健身"},  # ROI低

    # 竞品合作的达人
    {"kol_name": "美妆大号莎莎", "platform": "抖音", "followers": 500_0000, "product_id": "p006",
     "commission_rate": 0.25, "estimated_sales": 5000, "estimated_gmv": 495000.0,
     "fee": 50000, "roi": 9.90, "cooperation_date": "2024-08-01", "niche": "美妆"},  # 竞品大投入！
]


# ============================================================
# 6. 竞品价格监控
# ============================================================
PRICE_MONITORING = [
    {"product_id": "p001", "competitor_product": "冰感科技超薄防晒衣", "our_price": 129.0,
     "comp_price": 99.0, "price_diff": -30.0, "date": "2024-08-01"},
    {"product_id": "p001", "competitor_product": "冰感科技超薄防晒衣", "our_price": 129.0,
     "comp_price": 89.0, "price_diff": -40.0, "date": "2024-08-15"},  # 竞品降价了！
    {"product_id": "p001", "competitor_product": "户外极客超轻防晒衣", "our_price": 129.0,
     "comp_price": 159.0, "price_diff": 30.0, "date": "2024-08-15"},
    {"product_id": "p002", "competitor_product": "冰感科技防晒衣pro版", "our_price": 179.0,
     "comp_price": 149.0, "price_diff": -30.0, "date": "2024-08-15"},
    {"product_id": "p004", "competitor_product": "户外极客防晒冰袖", "our_price": 29.9,
     "comp_price": 19.9, "price_diff": -10.0, "date": "2024-08-15"},
]


# ============================================================
# 7. 热词趋势数据
# ============================================================
TREND_KEYWORDS = [
    {"keyword": "冰感防晒衣", "search_index": 100, "month": 3, "year": 2024},
    {"keyword": "冰感防晒衣", "search_index": 185, "month": 4, "year": 2024},
    {"keyword": "冰感防晒衣", "search_index": 320, "month": 5, "year": 2024},
    {"keyword": "冰感防晒衣", "search_index": 510, "month": 6, "year": 2024},
    {"keyword": "冰感防晒衣", "search_index": 680, "month": 7, "year": 2024},
    {"keyword": "冰感防晒衣", "search_index": 720, "month": 8, "year": 2024},

    {"keyword": "防晒衣女", "search_index": 200, "month": 3, "year": 2024},
    {"keyword": "防晒衣女", "search_index": 310, "month": 4, "year": 2024},
    {"keyword": "防晒衣女", "search_index": 480, "month": 5, "year": 2024},
    {"keyword": "防晒衣女", "search_index": 620, "month": 6, "year": 2024},
    {"keyword": "防晒衣女", "search_index": 750, "month": 7, "year": 2024},
    {"keyword": "防晒衣女", "search_index": 710, "month": 8, "year": 2024},  # 搜索热度开始降了

    {"keyword": "冰袖", "search_index": 80, "month": 3, "year": 2024},
    {"keyword": "冰袖", "search_index": 140, "month": 4, "year": 2024},
    {"keyword": "冰袖", "search_index": 200, "month": 5, "year": 2024},
    {"keyword": "冰袖", "search_index": 310, "month": 6, "year": 2024},
    {"keyword": "冰袖", "search_index": 380, "month": 7, "year": 2024},
    {"keyword": "冰袖", "search_index": 340, "month": 8, "year": 2024},
]


# ============================================================
# 8. 退货明细
# ============================================================
REFUNDS = [
    {"order_id": "ORD20240015", "product_id": "p001", "reason": "尺码偏小",
     "refund_amount": 129.0, "date": "2024-08-12"},
    {"order_id": "ORD20240022", "product_id": "p001", "reason": "质量问题（起球）",
     "refund_amount": 129.0, "date": "2024-08-18"},
    {"order_id": "ORD20240031", "product_id": "p001", "reason": "与描述不符",
     "refund_amount": 129.0, "date": "2024-08-19"},
    {"order_id": "ORD20240045", "product_id": "p002", "reason": "性价比低",
     "refund_amount": 179.0, "date": "2024-08-22"},
    {"order_id": "ORD20240052", "product_id": "p004", "reason": "质量差（起毛）",
     "refund_amount": 29.9, "date": "2024-08-23"},
    {"order_id": "ORD20240067", "product_id": "p001", "reason": "色差严重",
     "refund_amount": 129.0, "date": "2024-08-25"},
    {"order_id": "ORD20240078", "product_id": "p001", "reason": "发货太慢不想要了",
     "refund_amount": 129.0, "date": "2024-08-27"},
]


# ============================================================
# 辅助方法：获取所有数据
# ============================================================
def get_all_mock_data() -> dict:
    """获取全部mock数据（默认服装鞋包/防晒衣），供DataQueryer使用"""
    return {
        "products": PRODUCTS,
        "monthly_sales": MONTHLY_SALES,
        "orders": ORDERS,
        "reviews": REVIEWS,
        "kol_data": KOL_DATA,
        "price_monitoring": PRICE_MONITORING,
        "trend_keywords": TREND_KEYWORDS,
        "refunds": REFUNDS,
    }


def get_mock_data_for_industry(industry_id: str) -> dict:
    """根据行业ID返回对应的mock数据集

    Args:
        industry_id: 行业标识，可选值：
            - 'fashion'（默认）: 服装鞋包 - 防晒衣品牌"夏日轻盈"
            - 'beauty': 美妆个护 - 护肤品牌"兰芮 L'ANRAY"
            - 'digital': 数码家电 - TWS耳机品牌"聆韵 LINGVIBE"
            - 'food': 食品饮料 - 茶饮品牌"茶屿 CHAYU"

    Returns:
        dict: mock数据字典，如果行业不存在则返回默认fashion数据
    """
    industry_map = {
        "fashion": get_all_mock_data,
        "beauty": None,   # lazy import
        "digital": None,
        "food": None,
    }

    # 默认返回 fashion
    if industry_id not in industry_map:
        return get_all_mock_data()

    if industry_id == "fashion":
        return get_all_mock_data()

    # Lazy import 对应行业的 mock 数据模块（兼容多种导入方式）
    if industry_id == "beauty":
        try:
            from .ecommerce_mock_data_beauty import get_beauty_mock_data
        except ImportError:
            try:
                from app.service.deep_research_v2.ecommerce_mock_data_beauty import get_beauty_mock_data
            except ImportError:
                import ecommerce_mock_data_beauty
                get_beauty_mock_data = ecommerce_mock_data_beauty.get_beauty_mock_data
        return get_beauty_mock_data()
    elif industry_id == "digital":
        try:
            from .ecommerce_mock_data_digital import get_digital_mock_data
        except ImportError:
            try:
                from app.service.deep_research_v2.ecommerce_mock_data_digital import get_digital_mock_data
            except ImportError:
                import ecommerce_mock_data_digital
                get_digital_mock_data = ecommerce_mock_data_digital.get_digital_mock_data
        return get_digital_mock_data()
    elif industry_id == "food":
        try:
            from .ecommerce_mock_data_food import get_food_mock_data
        except ImportError:
            try:
                from app.service.deep_research_v2.ecommerce_mock_data_food import get_food_mock_data
            except ImportError:
                import ecommerce_mock_data_food
                get_food_mock_data = ecommerce_mock_data_food.get_food_mock_data
        return get_food_mock_data()

    return get_all_mock_data()


def print_data_summary():
    """打印数据摘要"""
    data = get_all_mock_data()
    print("=" * 50)
    print("电商 Mock 数据摘要")
    print("=" * 50)
    print(f"商品数: {len(data['products'])}（自家{sum(1 for p in data['products'] if p['is_own'])}个，竞品{sum(1 for p in data['products'] if not p['is_own'])}个）")
    print(f"月度销售记录: {len(data['monthly_sales'])} 条")
    print(f"订单明细: {len(data['orders'])} 条")
    print(f"用户评价: {len(data['reviews'])} 条（好评{sum(1 for r in data['reviews'] if r['rating'] >= 4)}个，差评{sum(1 for r in data['reviews'] if r['rating'] <= 2)}个）")
    print(f"达人数据: {len(data['kol_data'])} 条")
    print(f"价格监控: {len(data['price_monitoring'])} 条")
    print(f"热搜词趋势: {len(data['trend_keywords'])} 条")
    print(f"退货记录: {len(data['refunds'])} 条")
    print()
    print("数据中的故事线：")
    print("  1. 主打商品8月销量下滑（经典款从3800→2800）")
    print("  2. 竞品'冰感科技'价格更低且销量正在快速上升")
    print("  3. 差评集中在'尺码偏小'和'发货慢'")
    print("  4. 达人'户外运动小鱼儿' ROI 高达19.35，值得追加")
    print("  5. '冰感'关键词搜索量持续上升中")
    print("=" * 50)


if __name__ == "__main__":
    print_data_summary()
