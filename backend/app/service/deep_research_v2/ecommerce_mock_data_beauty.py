"""
电商运营分析 - Mock 数据集（美妆个护）

模拟一个护肤品牌"兰芮 L'ANRAY"的经营数据，包含：
- 商品数据（自家 + 竞品）
- 月度销售数据
- 各平台订单明细
- 用户评价
- 达人带货数据
- 价格监控

数据中埋了一些"问题"和"机会点"，方便AI分析时发现：
1. 精华液销量增长但差评率上升（肤感/过敏问题）
2. 竞品"薇诺娜"靠敏感肌概念快速抢占市场
3. 小红书达人ROI显著高于抖音达人
4. "成分党"搜索趋势上升，功效护肤成风口
5. 面膜品类价格战激烈，竞品疯狂降价
"""

import uuid
from datetime import datetime, timedelta
import random

random.seed(43)

# ============================================================
# 1. 商品数据
# ============================================================
PRODUCTS_BEAUTY = [
    # 自家商品
    {"id": "b001", "name": "兰芮玻尿酸水光精华液30ml", "brand": "兰芮", "category": "精华液",
     "price": 189.0, "cost": 62.0, "stock": 4500, "is_own": True},
    {"id": "b002", "name": "兰芮烟酰胺亮肤精华液30ml", "brand": "兰芮", "category": "精华液",
     "price": 219.0, "cost": 78.0, "stock": 2800, "is_own": True},
    {"id": "b003", "name": "兰芮神经酰胺修护面霜50g", "brand": "兰芮", "category": "面霜",
     "price": 159.0, "cost": 55.0, "stock": 3200, "is_own": True},
    {"id": "b004", "name": "兰芮玻尿酸补水面膜5片装", "brand": "兰芮", "category": "面膜",
     "price": 49.9, "cost": 14.0, "stock": 12000, "is_own": True},
    {"id": "b005", "name": "兰芮氨基酸温和洁面乳120g", "brand": "兰芮", "category": "洁面",
     "price": 69.0, "cost": 22.0, "stock": 6000, "is_own": True},
    # 竞品商品
    {"id": "b006", "name": "薇诺娜舒敏精华液30ml", "brand": "薇诺娜", "category": "精华液",
     "price": 228.0, "cost": 85.0, "stock": 8000, "is_own": False},
    {"id": "b007", "name": "薇诺娜特护霜50g", "brand": "薇诺娜", "category": "面霜",
     "price": 178.0, "cost": 62.0, "stock": 5000, "is_own": False},
    {"id": "b008", "name": "珀莱雅双抗精华液30ml", "brand": "珀莱雅", "category": "精华液",
     "price": 259.0, "cost": 95.0, "stock": 3500, "is_own": False},
    {"id": "b009", "name": "韩束补水面膜10片装", "brand": "韩束", "category": "面膜",
     "price": 39.9, "cost": 12.0, "stock": 20000, "is_own": False},
    {"id": "b010", "name": "至本舒颜修护洁面乳120g", "brand": "至本", "category": "洁面",
     "price": 59.0, "cost": 20.0, "stock": 10000, "is_own": False},
]

# ============================================================
# 2. 月度销售汇总（2024年3月-8月）
# ============================================================
MONTHLY_SALES_BEAUTY = [
    # 自家品牌 - 玻尿酸精华液
    {"product_id": "b001", "year": 2024, "month": 3, "sales_qty": 1200, "sales_amount": 226800.0, "channel": "天猫"},
    {"product_id": "b001", "year": 2024, "month": 4, "sales_qty": 1800, "sales_amount": 340200.0, "channel": "天猫"},
    {"product_id": "b001", "year": 2024, "month": 5, "sales_qty": 2600, "sales_amount": 491400.0, "channel": "天猫"},
    {"product_id": "b001", "year": 2024, "month": 6, "sales_qty": 3500, "sales_amount": 661500.0, "channel": "天猫"},
    {"product_id": "b001", "year": 2024, "month": 7, "sales_qty": 4200, "sales_amount": 793800.0, "channel": "天猫"},
    {"product_id": "b001", "year": 2024, "month": 8, "sales_qty": 3800, "sales_amount": 718200.0, "channel": "天猫"},  # 环比下滑！
    # 自家品牌 - 玻尿酸精华液(抖音)
    {"product_id": "b001", "year": 2024, "month": 3, "sales_qty": 400, "sales_amount": 75600.0, "channel": "抖音"},
    {"product_id": "b001", "year": 2024, "month": 4, "sales_qty": 700, "sales_amount": 132300.0, "channel": "抖音"},
    {"product_id": "b001", "year": 2024, "month": 5, "sales_qty": 1200, "sales_amount": 226800.0, "channel": "抖音"},
    {"product_id": "b001", "year": 2024, "month": 6, "sales_qty": 1800, "sales_amount": 340200.0, "channel": "抖音"},
    {"product_id": "b001", "year": 2024, "month": 7, "sales_qty": 2400, "sales_amount": 453600.0, "channel": "抖音"},
    {"product_id": "b001", "year": 2024, "month": 8, "sales_qty": 2100, "sales_amount": 396900.0, "channel": "抖音"},  # 环比下滑

    # 自家品牌 - 面霜
    {"product_id": "b003", "year": 2024, "month": 5, "sales_qty": 800, "sales_amount": 127200.0, "channel": "天猫"},
    {"product_id": "b003", "year": 2024, "month": 6, "sales_qty": 1200, "sales_amount": 190800.0, "channel": "天猫"},
    {"product_id": "b003", "year": 2024, "month": 7, "sales_qty": 1500, "sales_amount": 238500.0, "channel": "天猫"},
    {"product_id": "b003", "year": 2024, "month": 8, "sales_qty": 1400, "sales_amount": 222600.0, "channel": "天猫"},

    # 竞品 - 薇诺娜舒敏精华液（快速上升！）
    {"product_id": "b006", "year": 2024, "month": 3, "sales_qty": 2500, "sales_amount": 570000.0, "channel": "天猫"},
    {"product_id": "b006", "year": 2024, "month": 4, "sales_qty": 3200, "sales_amount": 729600.0, "channel": "天猫"},
    {"product_id": "b006", "year": 2024, "month": 5, "sales_qty": 4300, "sales_amount": 980400.0, "channel": "天猫"},
    {"product_id": "b006", "year": 2024, "month": 6, "sales_qty": 5500, "sales_amount": 1254000.0, "channel": "天猫"},
    {"product_id": "b006", "year": 2024, "month": 7, "sales_qty": 7200, "sales_amount": 1641600.0, "channel": "天猫"},  # 反超！
    {"product_id": "b006", "year": 2024, "month": 8, "sales_qty": 8500, "sales_amount": 1938000.0, "channel": "天猫"},  # 继续爆发

    # 竞品 - 薇诺娜舒敏精华液(抖音)
    {"product_id": "b006", "year": 2024, "month": 6, "sales_qty": 2200, "sales_amount": 501600.0, "channel": "抖音"},
    {"product_id": "b006", "year": 2024, "month": 7, "sales_qty": 3500, "sales_amount": 798000.0, "channel": "抖音"},
    {"product_id": "b006", "year": 2024, "month": 8, "sales_qty": 4800, "sales_amount": 1094400.0, "channel": "抖音"},
]


# ============================================================
# 3. 订单明细（最近100条订单）
# ============================================================
def _gen_orders_beauty():
    channels = ["天猫", "京东", "抖音", "拼多多", "小红书"]
    cities = ["上海", "北京", "广州", "深圳", "杭州", "成都", "武汉",
              "南京", "重庆", "苏州", "西安", "长沙", "郑州", "青岛", "厦门"]
    statuses = ["已完成", "已完成", "已完成", "已完成", "已完成",
                "已完成", "已完成", "已完成", "退货中", "已退货"]

    orders = []
    base_date = datetime(2024, 8, 20)
    product_ids = ["b001", "b002", "b003", "b004", "b005"]

    for i in range(100):
        pid = random.choice(product_ids)
        product = next(p for p in PRODUCTS_BEAUTY if p["id"] == pid)
        qty = random.choices([1, 1, 1, 1, 2, 2, 3], weights=[30, 30, 15, 10, 8, 5, 2])[0]
        date = base_date - timedelta(days=random.randint(0, 60))
        channel = random.choice(channels)
        city = random.choice(cities)
        status = random.choice(statuses)
        total = round(product["price"] * qty, 2)
        is_refund = status in ("退货中", "已退货")

        orders.append({
            "order_id": f"BTY2024{i+1:04d}",
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

ORDERS_BEAUTY = _gen_orders_beauty()


# ============================================================
# 4. 用户评价（含好评和差评，有故事性）
# ============================================================
REVIEWS_BEAUTY = [
    # 正面评价
    {"id": "br001", "product_id": "b001", "rating": 5, "content": "用了半个月，皮肤真的变水润了，吸收很快不油腻",
     "date": "2024-07-15", "source": "天猫"},
    {"id": "br002", "product_id": "b001", "rating": 5, "content": "适合油皮不会闷，质地很清爽，已回购第三次了",
     "date": "2024-07-20", "source": "天猫"},
    {"id": "br003", "product_id": "b001", "rating": 4, "content": "补水效果不错，就是有点小贵，双十一期待大促价格",
     "date": "2024-07-22", "source": "天猫"},
    {"id": "br004", "product_id": "b003", "rating": 5, "content": "面霜质地超舒服，不厚重不油腻，干皮救星",
     "date": "2024-08-01", "source": "天猫"},
    {"id": "br005", "product_id": "b004", "rating": 5, "content": "面膜精华液很多，敷完脸滑滑的，性价比很高",
     "date": "2024-08-05", "source": "天猫"},
    {"id": "br006", "product_id": "b001", "rating": 5, "content": "跟着小红书博主种草的，用了一周就很惊艳，痘印淡了不少",
     "date": "2024-08-10", "source": "小红书"},
    {"id": "br007", "product_id": "b002", "rating": 4, "content": "美白效果暂时没看到，不过肤感很好，再用一瓶看看",
     "date": "2024-08-12", "source": "天猫"},
    {"id": "br008", "product_id": "b005", "rating": 5, "content": "氨基酸洁面用着很舒服，洗完不紧绷，会继续回购",
     "date": "2024-08-15", "source": "京东"},
    {"id": "br009", "product_id": "b001", "rating": 5, "content": "成分党来评价：玻尿酸+神经酰胺的组合非常科学，配方干净",
     "date": "2024-08-18", "source": "天猫"},
    {"id": "br010", "product_id": "b003", "rating": 4, "content": "修护效果不错，红血丝淡了一些，可能需要长期用",
     "date": "2024-08-20", "source": "天猫"},

    # 差评（有故事性）
    {"id": "br011", "product_id": "b001", "rating": 2, "content": "用了一段时间脸上长闭口了，可能不适合敏感肌，停用试试",
     "date": "2024-08-08", "source": "天猫"},
    {"id": "br012", "product_id": "b001", "rating": 1, "content": "有酒精味！敏感肌用着脸发红刺痛，赶紧退货了",
     "date": "2024-08-11", "source": "天猫"},
    {"id": "br013", "product_id": "b001", "rating": 2, "content": "和朋友用的薇诺娜比差远了，肤感不如人家温和，不会回购",
     "date": "2024-08-14", "source": "天猫"},
    {"id": "br014", "product_id": "b002", "rating": 1, "content": "用了两周脸变黄了整个人都不好了，看成分表里有不太好吸收的成分",
     "date": "2024-08-16", "source": "抖音"},
    {"id": "br015", "product_id": "b003", "rating": 2, "content": "面霜太香了，香精味熏得头疼，护肤品为什么要放这么多香精",
     "date": "2024-08-19", "source": "天猫"},
    {"id": "br016", "product_id": "b001", "rating": 1, "content": "客服专业度不够，问了成分问题一问三不知，对品牌专业度失望",
     "date": "2024-08-21", "source": "京东"},
    {"id": "br017", "product_id": "b004", "rating": 2, "content": "面膜精华液比以前少了，感觉缩水了，不如韩束实惠",
     "date": "2024-08-22", "source": "天猫"},
    {"id": "br018", "product_id": "b001", "rating": 3, "content": "效果一般跟几十块钱的差不多，不知道这价格贵在哪",
     "date": "2024-08-23", "source": "天猫"},
    {"id": "br019", "product_id": "b002", "rating": 2, "content": "瓶子里面的滴管不好用，设计有缺陷，精华经常滴不出来",
     "date": "2024-08-25", "source": "抖音"},
    {"id": "br020", "product_id": "b003", "rating": 1, "content": "这个价位不如买薇诺娜特护霜，人家专门做敏感肌的",
     "date": "2024-08-26", "source": "天猫"},
]


# ============================================================
# 5. 达人带货数据
# ============================================================
KOL_DATA_BEAUTY = [
    {"kol_name": "护肤研发师小林", "platform": "小红书", "followers": 65_0000, "product_id": "b001",
     "commission_rate": 0.15, "estimated_sales": 2500, "estimated_gmv": 472500.0,
     "fee": 12000, "roi": 39.38, "cooperation_date": "2024-07-05", "niche": "成分科普"},

    {"kol_name": "美妆界的码农", "platform": "抖音", "followers": 320_0000, "product_id": "b001",
     "commission_rate": 0.20, "estimated_sales": 1800, "estimated_gmv": 340200.0,
     "fee": 35000, "roi": 9.72, "cooperation_date": "2024-07-15", "niche": "美妆评测"},

    {"kol_name": "精致女生vivi", "platform": "小红书", "followers": 180_0000, "product_id": "b002",
     "commission_rate": 0.18, "estimated_sales": 1200, "estimated_gmv": 262800.0,
     "fee": 18000, "roi": 14.60, "cooperation_date": "2024-07-20", "niche": "精致护肤"},

    {"kol_name": "成分控Ni", "platform": "小红书", "followers": 42_0000, "product_id": "b003",
     "commission_rate": 0.12, "estimated_sales": 800, "estimated_gmv": 127200.0,
     "fee": 6000, "roi": 21.20, "cooperation_date": "2024-07-25", "niche": "成分党"},

    {"kol_name": "大学生寝室好物", "platform": "抖音", "followers": 25_0000, "product_id": "b004",
     "commission_rate": 0.10, "estimated_sales": 3500, "estimated_gmv": 174650.0,
     "fee": 8000, "roi": 21.83, "cooperation_date": "2024-08-01", "niche": "学生平价"},

    {"kol_name": "知名网红李姐", "platform": "抖音", "followers": 800_0000, "product_id": "b005",
     "commission_rate": 0.25, "estimated_sales": 2200, "estimated_gmv": 151800.0,
     "fee": 100000, "roi": 1.52, "cooperation_date": "2024-08-08", "niche": "全品类"},  # ROI极低

    # 竞品合作的达人
    {"kol_name": "皮肤科刘医生", "platform": "抖音", "followers": 400_0000, "product_id": "b006",
     "commission_rate": 0.22, "estimated_sales": 6000, "estimated_gmv": 1368000.0,
     "fee": 45000, "roi": 30.40, "cooperation_date": "2024-08-01", "niche": "医学护肤"},  # 竞品大投入！
]


# ============================================================
# 6. 竞品价格监控
# ============================================================
PRICE_MONITORING_BEAUTY = [
    {"product_id": "b001", "competitor_product": "薇诺娜舒敏精华液30ml", "our_price": 189.0,
     "comp_price": 228.0, "price_diff": 39.0, "date": "2024-08-01"},
    {"product_id": "b001", "competitor_product": "薇诺娜舒敏精华液30ml", "our_price": 189.0,
     "comp_price": 199.0, "price_diff": 10.0, "date": "2024-08-15"},  # 竞品降价了！
    {"product_id": "b001", "competitor_product": "珀莱雅双抗精华液30ml", "our_price": 189.0,
     "comp_price": 259.0, "price_diff": 70.0, "date": "2024-08-15"},
    {"product_id": "b003", "competitor_product": "薇诺娜特护霜50g", "our_price": 159.0,
     "comp_price": 178.0, "price_diff": 19.0, "date": "2024-08-15"},
    {"product_id": "b004", "competitor_product": "韩束补水面膜10片装", "our_price": 49.9,
     "comp_price": 39.9, "price_diff": -10.0, "date": "2024-08-15"},  # 竞品面膜更便宜
]


# ============================================================
# 7. 热词趋势数据
# ============================================================
TREND_KEYWORDS_BEAUTY = [
    {"keyword": "成分党护肤", "search_index": 180, "month": 3, "year": 2024},
    {"keyword": "成分党护肤", "search_index": 260, "month": 4, "year": 2024},
    {"keyword": "成分党护肤", "search_index": 410, "month": 5, "year": 2024},
    {"keyword": "成分党护肤", "search_index": 580, "month": 6, "year": 2024},
    {"keyword": "成分党护肤", "search_index": 750, "month": 7, "year": 2024},
    {"keyword": "成分党护肤", "search_index": 820, "month": 8, "year": 2024},

    {"keyword": "敏感肌护肤", "search_index": 250, "month": 3, "year": 2024},
    {"keyword": "敏感肌护肤", "search_index": 380, "month": 4, "year": 2024},
    {"keyword": "敏感肌护肤", "search_index": 550, "month": 5, "year": 2024},
    {"keyword": "敏感肌护肤", "search_index": 720, "month": 6, "year": 2024},
    {"keyword": "敏感肌护肤", "search_index": 880, "month": 7, "year": 2024},
    {"keyword": "敏感肌护肤", "search_index": 920, "month": 8, "year": 2024},  # 持续飙升

    {"keyword": "玻尿酸精华", "search_index": 320, "month": 3, "year": 2024},
    {"keyword": "玻尿酸精华", "search_index": 450, "month": 4, "year": 2024},
    {"keyword": "玻尿酸精华", "search_index": 520, "month": 5, "year": 2024},
    {"keyword": "玻尿酸精华", "search_index": 600, "month": 6, "year": 2024},
    {"keyword": "玻尿酸精华", "search_index": 650, "month": 7, "year": 2024},
    {"keyword": "玻尿酸精华", "search_index": 580, "month": 8, "year": 2024},  # 热度下降
]


# ============================================================
# 8. 退货明细
# ============================================================
REFUNDS_BEAUTY = [
    {"order_id": "BTY20240012", "product_id": "b001", "reason": "过敏不适",
     "refund_amount": 189.0, "date": "2024-08-10"},
    {"order_id": "BTY20240019", "product_id": "b001", "reason": "使用后长痘/闭口",
     "refund_amount": 189.0, "date": "2024-08-16"},
    {"order_id": "BTY20240025", "product_id": "b001", "reason": "肤感不如预期",
     "refund_amount": 189.0, "date": "2024-08-20"},
    {"order_id": "BTY20240033", "product_id": "b002", "reason": "使用后脸色发黄",
     "refund_amount": 219.0, "date": "2024-08-22"},
    {"order_id": "BTY20240048", "product_id": "b003", "reason": "香精味太重过敏",
     "refund_amount": 159.0, "date": "2024-08-23"},
    {"order_id": "BTY20240056", "product_id": "b001", "reason": "包装破损",
     "refund_amount": 189.0, "date": "2024-08-25"},
    {"order_id": "BTY20240072", "product_id": "b004", "reason": "效果差不如预期",
     "refund_amount": 49.9, "date": "2024-08-27"},
]


# ============================================================
# 辅助方法
# ============================================================
def get_beauty_mock_data() -> dict:
    """获取美妆个护行业 mock 数据"""
    return {
        "products": PRODUCTS_BEAUTY,
        "monthly_sales": MONTHLY_SALES_BEAUTY,
        "orders": ORDERS_BEAUTY,
        "reviews": REVIEWS_BEAUTY,
        "kol_data": KOL_DATA_BEAUTY,
        "price_monitoring": PRICE_MONITORING_BEAUTY,
        "trend_keywords": TREND_KEYWORDS_BEAUTY,
        "refunds": REFUNDS_BEAUTY,
    }


def print_beauty_data_summary():
    """打印数据摘要"""
    data = get_beauty_mock_data()
    print("=" * 50)
    print("美妆个护 Mock 数据摘要（兰芮 L'ANRAY）")
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
    print("  1. 精华液销量增长但差评率上升（肤感/过敏/长闭口）")
    print("  2. 竞品'薇诺娜'靠敏感肌定位快速抢占市场")
    print("  3. 小红书达人ROI远超抖音（护肤研发师小林 ROI 39.38）")
    print("  4. 知名网红李姐坑位费10万ROI仅1.52，需重新评估KOL策略")
    print("  5. '成分党'和'敏感肌护肤'搜索趋势持续上升")
    print("=" * 50)


if __name__ == "__main__":
    print_beauty_data_summary()
