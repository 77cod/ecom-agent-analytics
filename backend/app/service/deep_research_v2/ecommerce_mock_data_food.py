"""
电商运营分析 - Mock 数据集（食品饮料）

模拟一个茶饮品牌"茶屿 CHAYU"的经营数据，包含：
- 商品数据（自家 + 竞品）
- 月度销售数据
- 各平台订单明细
- 用户评价
- 达人带货数据
- 价格监控

数据中埋了一些"问题"和"机会点"，方便AI分析时发现：
1. 夏季冷泡茶热销但毛利低，拉低整体客单价
2. 竞品CHALI茶里通过联名款实现高溢价策略
3. 茶礼盒（高毛利产品）中秋前自然增长
4. 抖音食品达人ROI极高，泛娱乐主播ROI惨淡
5. "无糖茶""养生茶"搜索趋势持续上升
6. 竞品小罐茶以高端定位切入礼品市场
"""

import uuid
from datetime import datetime, timedelta
import random

random.seed(45)

# ============================================================
# 1. 商品数据
# ============================================================
PRODUCTS_FOOD = [
    # 自家商品
    {"id": "f001", "name": "茶屿桂花乌龙冷泡茶 10包装", "brand": "茶屿", "category": "袋泡茶",
     "price": 39.9, "cost": 12.0, "stock": 15000, "is_own": True},
    {"id": "f002", "name": "茶屿蜜桃乌龙冷泡茶 10包装", "brand": "茶屿", "category": "袋泡茶",
     "price": 39.9, "cost": 12.5, "stock": 12000, "is_own": True},
    {"id": "f003", "name": "茶屿东方美人大师茶礼盒 48g", "brand": "茶屿", "category": "茶礼盒",
     "price": 288.0, "cost": 95.0, "stock": 2000, "is_own": True},
    {"id": "f004", "name": "茶屿无糖菊花枸杞茶 20包装", "brand": "茶屿", "category": "养生茶",
     "price": 49.9, "cost": 15.0, "stock": 8000, "is_own": True},
    {"id": "f005", "name": "茶屿陈皮普洱熟茶 7颗装", "brand": "茶屿", "category": "普洱",
     "price": 69.0, "cost": 22.0, "stock": 3500, "is_own": True},
    # 竞品商品
    {"id": "f006", "name": "CHALI茶里蜜桃乌龙 15包装", "brand": "CHALI茶里", "category": "袋泡茶",
     "price": 49.0, "cost": 15.0, "stock": 20000, "is_own": False},
    {"id": "f007", "name": "CHALI茶里故宫联名礼盒", "brand": "CHALI茶里", "category": "茶礼盒",
     "price": 368.0, "cost": 120.0, "stock": 5000, "is_own": False},  # 高溢价联名
    {"id": "f008", "name": "小罐茶特级铁观音 10罐装", "brand": "小罐茶", "category": "高端茶",
     "price": 500.0, "cost": 150.0, "stock": 3000, "is_own": False},
    {"id": "f009", "name": "乐乐茶冷泡精选 10包装", "brand": "乐乐茶", "category": "袋泡茶",
     "price": 35.0, "cost": 11.0, "stock": 10000, "is_own": False},
    {"id": "f010", "name": "吴裕泰茉莉花茶 100g", "brand": "吴裕泰", "category": "传统茶",
     "price": 89.0, "cost": 35.0, "stock": 5000, "is_own": False},
]

# ============================================================
# 2. 月度销售汇总（2024年3月-8月）
# ============================================================
MONTHLY_SALES_FOOD = [
    # 自家品牌 - 桂花乌龙冷泡茶
    {"product_id": "f001", "year": 2024, "month": 3, "sales_qty": 1200, "sales_amount": 47880.0, "channel": "天猫"},
    {"product_id": "f001", "year": 2024, "month": 4, "sales_qty": 2200, "sales_amount": 87780.0, "channel": "天猫"},
    {"product_id": "f001", "year": 2024, "month": 5, "sales_qty": 4500, "sales_amount": 179550.0, "channel": "天猫"},
    {"product_id": "f001", "year": 2024, "month": 6, "sales_qty": 8500, "sales_amount": 339150.0, "channel": "天猫"},
    {"product_id": "f001", "year": 2024, "month": 7, "sales_qty": 12000, "sales_amount": 478800.0, "channel": "天猫"},
    {"product_id": "f001", "year": 2024, "month": 8, "sales_qty": 10500, "sales_amount": 418950.0, "channel": "天猫"},
    # 自家品牌 - 桂花乌龙冷泡茶(抖音)
    {"product_id": "f001", "year": 2024, "month": 3, "sales_qty": 500, "sales_amount": 19950.0, "channel": "抖音"},
    {"product_id": "f001", "year": 2024, "month": 4, "sales_qty": 1000, "sales_amount": 39900.0, "channel": "抖音"},
    {"product_id": "f001", "year": 2024, "month": 5, "sales_qty": 2000, "sales_amount": 79800.0, "channel": "抖音"},
    {"product_id": "f001", "year": 2024, "month": 6, "sales_qty": 4500, "sales_amount": 179550.0, "channel": "抖音"},
    {"product_id": "f001", "year": 2024, "month": 7, "sales_qty": 7000, "sales_amount": 279300.0, "channel": "抖音"},
    {"product_id": "f001", "year": 2024, "month": 8, "sales_qty": 6500, "sales_amount": 259350.0, "channel": "抖音"},

    # 自家品牌 - 茶礼盒（高毛利，中秋前自然增长）
    {"product_id": "f003", "year": 2024, "month": 6, "sales_qty": 300, "sales_amount": 86400.0, "channel": "天猫"},
    {"product_id": "f003", "year": 2024, "month": 7, "sales_qty": 600, "sales_amount": 172800.0, "channel": "天猫"},
    {"product_id": "f003", "year": 2024, "month": 8, "sales_qty": 1200, "sales_amount": 345600.0, "channel": "天猫"},  # 中秋爆发

    # 竞品 - CHALI茶里蜜桃乌龙
    {"product_id": "f006", "year": 2024, "month": 3, "sales_qty": 3000, "sales_amount": 147000.0, "channel": "天猫"},
    {"product_id": "f006", "year": 2024, "month": 4, "sales_qty": 4500, "sales_amount": 220500.0, "channel": "天猫"},
    {"product_id": "f006", "year": 2024, "month": 5, "sales_qty": 6500, "sales_amount": 318500.0, "channel": "天猫"},
    {"product_id": "f006", "year": 2024, "month": 6, "sales_qty": 9000, "sales_amount": 441000.0, "channel": "天猫"},
    {"product_id": "f006", "year": 2024, "month": 7, "sales_qty": 13000, "sales_amount": 637000.0, "channel": "天猫"},  # 远超我方
    {"product_id": "f006", "year": 2024, "month": 8, "sales_qty": 15000, "sales_amount": 735000.0, "channel": "天猫"},

    # 竞品 - CHALI茶里故宫联名礼盒（高溢价爆发）
    {"product_id": "f007", "year": 2024, "month": 7, "sales_qty": 800, "sales_amount": 294400.0, "channel": "天猫"},
    {"product_id": "f007", "year": 2024, "month": 8, "sales_qty": 2500, "sales_amount": 920000.0, "channel": "天猫"},  # 联名爆款！
]


# ============================================================
# 3. 订单明细（最近100条订单）
# ============================================================
def _gen_orders_food():
    channels = ["天猫", "京东", "抖音", "拼多多", "小红书"]
    cities = ["上海", "北京", "广州", "深圳", "杭州", "成都", "武汉",
              "南京", "重庆", "苏州", "西安", "长沙", "昆明", "福州", "厦门"]
    statuses = ["已完成", "已完成", "已完成", "已完成", "已完成",
                "已完成", "已完成", "已完成", "退货中", "已退货"]

    orders = []
    base_date = datetime(2024, 8, 20)
    product_ids = ["f001", "f002", "f003", "f004", "f005"]

    for i in range(100):
        pid = random.choice(product_ids)
        product = next(p for p in PRODUCTS_FOOD if p["id"] == pid)
        qty = random.choices([1, 1, 1, 2, 2, 3, 5], weights=[25, 25, 15, 12, 8, 10, 5])[0]
        date = base_date - timedelta(days=random.randint(0, 60))
        channel = random.choice(channels)
        city = random.choice(cities)
        status = random.choice(statuses)
        total = round(product["price"] * qty, 2)
        is_refund = status in ("退货中", "已退货")

        orders.append({
            "order_id": f"FOOD2024{i+1:04d}",
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

ORDERS_FOOD = _gen_orders_food()


# ============================================================
# 4. 用户评价（含好评和差评，有故事性）
# ============================================================
REVIEWS_FOOD = [
    # 正面评价
    {"id": "fr001", "product_id": "f001", "rating": 5, "content": "冷泡太方便了！丢瓶矿泉水泡一会就能喝，桂花香很自然",
     "date": "2024-07-15", "source": "天猫"},
    {"id": "fr002", "product_id": "f001", "rating": 5, "content": "夏天喝这个太舒服了，比奶茶健康多了，已经第三次回购",
     "date": "2024-07-20", "source": "天猫"},
    {"id": "fr003", "product_id": "f001", "rating": 4, "content": "桂花味清香不腻，就是10包装太少了，喝得快的两周就没了",
     "date": "2024-07-22", "source": "天猫"},
    {"id": "fr004", "product_id": "f003", "rating": 5, "content": "礼盒超精致，送长辈非常合适，东方美人的味道很正",
     "date": "2024-08-01", "source": "京东"},
    {"id": "fr005", "product_id": "f004", "rating": 5, "content": "无糖菊花枸杞茶真的很养生，办公室必备，喝了不上火",
     "date": "2024-08-05", "source": "天猫"},
    {"id": "fr006", "product_id": "f001", "rating": 5, "content": "跟着抖音直播买的，桂花乌龙真的超好喝，强烈安利",
     "date": "2024-08-10", "source": "抖音"},
    {"id": "fr007", "product_id": "f002", "rating": 4, "content": "蜜桃味很天然不是那种香精味，甜度刚好，冷泡出味快",
     "date": "2024-08-12", "source": "天猫"},
    {"id": "fr008", "product_id": "f005", "rating": 5, "content": "陈皮普洱一颗一颗的特别方便，泡出来的茶汤红亮，味道醇厚",
     "date": "2024-08-15", "source": "京东"},
    {"id": "fr009", "product_id": "f001", "rating": 5, "content": "无糖茶终于有好喝的了！戒糖人士的福音，不用喝白开水了",
     "date": "2024-08-18", "source": "小红书"},
    {"id": "fr010", "product_id": "f003", "rating": 4, "content": "礼盒设计很有东方美学的感觉，茶叶品质也不错，就是价格偏高",
     "date": "2024-08-20", "source": "天猫"},

    # 差评（有故事性）
    {"id": "fr011", "product_id": "f001", "rating": 2, "content": "桂花味太淡了，泡了10分钟还跟白水一样，和CHALI的差远了",
     "date": "2024-08-08", "source": "天猫"},
    {"id": "fr012", "product_id": "f001", "rating": 1, "content": "茶包泡久了有酸味，像是加了香精而不是天然桂花，失望",
     "date": "2024-08-11", "source": "天猫"},
    {"id": "fr013", "product_id": "f002", "rating": 2, "content": "蜜桃味像劣质果汁的味，喝了喉咙不舒服，不如买CHALI的",
     "date": "2024-08-14", "source": "天猫"},
    {"id": "fr014", "product_id": "f001", "rating": 1, "content": "包装太简陋了跟几块钱的一样，39.9的茶包包装太掉档次",
     "date": "2024-08-16", "source": "京东"},
    {"id": "fr015", "product_id": "f004", "rating": 2, "content": "说是菊花枸杞但菊花的量很少，全是枸杞味，配料表没写清楚",
     "date": "2024-08-19", "source": "天猫"},
    {"id": "fr016", "product_id": "f001", "rating": 1, "content": "客服态度特别差，说好的冷泡茶但没写清楚冷水泡多久，问也不说",
     "date": "2024-08-21", "source": "京东"},
    {"id": "fr017", "product_id": "f006", "rating": 4, "content": "CHALI的蜜桃乌龙香气更浓郁，茶屿的相比之下太淡了",
     "date": "2024-08-22", "source": "天猫"},
    {"id": "fr018", "product_id": "f002", "rating": 3, "content": "一般般，没有惊艳的感觉，可能是之前期望太高了",
     "date": "2024-08-23", "source": "天猫"},
    {"id": "fr019", "product_id": "f001", "rating": 2, "content": "茶包线太短了，杯子高一点就够不到底，细节做工不行",
     "date": "2024-08-25", "source": "抖音"},
    {"id": "fr020", "product_id": "f003", "rating": 1, "content": "288的礼盒还不如168的CHALI联名款有面子，性价比不行",
     "date": "2024-08-26", "source": "天猫"},
]


# ============================================================
# 5. 达人带货数据
# ============================================================
KOL_DATA_FOOD = [
    {"kol_name": "茶圈老罗", "platform": "抖音", "followers": 55_0000, "product_id": "f003",
     "commission_rate": 0.12, "estimated_sales": 500, "estimated_gmv": 144000.0,
     "fee": 6000, "roi": 24.00, "cooperation_date": "2024-07-08", "niche": "茶文化"},

    {"kol_name": "吃货小马甲", "platform": "抖音", "followers": 280_0000, "product_id": "f001",
     "commission_rate": 0.15, "estimated_sales": 4000, "estimated_gmv": 159600.0,
     "fee": 15000, "roi": 10.64, "cooperation_date": "2024-07-12", "niche": "美食探店"},

    {"kol_name": "办公室好物推荐", "platform": "小红书", "followers": 72_0000, "product_id": "f004",
     "commission_rate": 0.12, "estimated_sales": 2500, "estimated_gmv": 124750.0,
     "fee": 8000, "roi": 15.59, "cooperation_date": "2024-07-18", "niche": "职场好物"},

    {"kol_name": "健康管理师小雅", "platform": "小红书", "followers": 48_0000, "product_id": "f004",
     "commission_rate": 0.10, "estimated_sales": 1800, "estimated_gmv": 89820.0,
     "fee": 5000, "roi": 17.96, "cooperation_date": "2024-07-22", "niche": "健康养生"},

    {"kol_name": "打工人生活日记", "platform": "抖音", "followers": 35_0000, "product_id": "f001",
     "commission_rate": 0.10, "estimated_sales": 1200, "estimated_gmv": 47880.0,
     "fee": 4000, "roi": 11.97, "cooperation_date": "2024-08-01", "niche": "打工日常"},

    {"kol_name": "全网最红美食家", "platform": "抖音", "followers": 2500_0000, "product_id": "f002",
     "commission_rate": 0.25, "estimated_sales": 2000, "estimated_gmv": 79800.0,
     "fee": 150000, "roi": 0.53, "cooperation_date": "2024-08-05", "niche": "泛娱乐美食"},  # ROI极低！

    # 竞品合作的达人
    {"kol_name": "故宫文化传播", "platform": "抖音", "followers": 600_0000, "product_id": "f007",
     "commission_rate": 0.20, "estimated_sales": 3000, "estimated_gmv": 1104000.0,
     "fee": 50000, "roi": 22.08, "cooperation_date": "2024-08-01", "niche": "文化IP"},  # 竞品联名
]


# ============================================================
# 6. 竞品价格监控
# ============================================================
PRICE_MONITORING_FOOD = [
    {"product_id": "f001", "competitor_product": "CHALI茶里蜜桃乌龙 15包装", "our_price": 39.9,
     "comp_price": 49.0, "price_diff": 9.1, "date": "2024-08-01"},
    {"product_id": "f001", "competitor_product": "乐乐茶冷泡精选 10包装", "our_price": 39.9,
     "comp_price": 35.0, "price_diff": -4.9, "date": "2024-08-15"},
    {"product_id": "f001", "competitor_product": "CHALI茶里蜜桃乌龙 15包装", "our_price": 39.9,
     "comp_price": 45.0, "price_diff": 5.1, "date": "2024-08-15"},  # 竞品降价
    {"product_id": "f003", "competitor_product": "CHALI茶里故宫联名礼盒", "our_price": 288.0,
     "comp_price": 368.0, "price_diff": 80.0, "date": "2024-08-15"},
    {"product_id": "f003", "competitor_product": "小罐茶特级铁观音 10罐装", "our_price": 288.0,
     "comp_price": 500.0, "price_diff": 212.0, "date": "2024-08-15"},
]


# ============================================================
# 7. 热词趋势数据
# ============================================================
TREND_KEYWORDS_FOOD = [
    {"keyword": "冷泡茶", "search_index": 150, "month": 3, "year": 2024},
    {"keyword": "冷泡茶", "search_index": 220, "month": 4, "year": 2024},
    {"keyword": "冷泡茶", "search_index": 380, "month": 5, "year": 2024},
    {"keyword": "冷泡茶", "search_index": 620, "month": 6, "year": 2024},
    {"keyword": "冷泡茶", "search_index": 850, "month": 7, "year": 2024},
    {"keyword": "冷泡茶", "search_index": 800, "month": 8, "year": 2024},

    {"keyword": "无糖茶饮", "search_index": 300, "month": 3, "year": 2024},
    {"keyword": "无糖茶饮", "search_index": 420, "month": 4, "year": 2024},
    {"keyword": "无糖茶饮", "search_index": 580, "month": 5, "year": 2024},
    {"keyword": "无糖茶饮", "search_index": 720, "month": 6, "year": 2024},
    {"keyword": "无糖茶饮", "search_index": 880, "month": 7, "year": 2024},
    {"keyword": "无糖茶饮", "search_index": 950, "month": 8, "year": 2024},  # 持续飙升

    {"keyword": "养生茶", "search_index": 250, "month": 3, "year": 2024},
    {"keyword": "养生茶", "search_index": 310, "month": 4, "year": 2024},
    {"keyword": "养生茶", "search_index": 390, "month": 5, "year": 2024},
    {"keyword": "养生茶", "search_index": 480, "month": 6, "year": 2024},
    {"keyword": "养生茶", "search_index": 560, "month": 7, "year": 2024},
    {"keyword": "养生茶", "search_index": 620, "month": 8, "year": 2024},  # 秋季上升
]


# ============================================================
# 8. 退货明细
# ============================================================
REFUNDS_FOOD = [
    {"order_id": "FOOD20240008", "product_id": "f001", "reason": "味道太淡/不如预期",
     "refund_amount": 39.9, "date": "2024-08-09"},
    {"order_id": "FOOD20240015", "product_id": "f001", "reason": "有酸味/疑似变质",
     "refund_amount": 39.9, "date": "2024-08-14"},
    {"order_id": "FOOD20240023", "product_id": "f002", "reason": "口感差/喉咙不适",
     "refund_amount": 39.9, "date": "2024-08-18"},
    {"order_id": "FOOD20240037", "product_id": "f001", "reason": "包装简陋/破损",
     "refund_amount": 39.9, "date": "2024-08-22"},
    {"order_id": "FOOD20240048", "product_id": "f004", "reason": "配料比例不符描述",
     "refund_amount": 49.9, "date": "2024-08-23"},
    {"order_id": "FOOD20240055", "product_id": "f003", "reason": "送礼不够档次",
     "refund_amount": 288.0, "date": "2024-08-25"},
    {"order_id": "FOOD20240073", "product_id": "f001", "reason": "茶包线太短使用不便",
     "refund_amount": 39.9, "date": "2024-08-27"},
]


# ============================================================
# 辅助方法
# ============================================================
def get_food_mock_data() -> dict:
    """获取食品饮料行业 mock 数据"""
    return {
        "products": PRODUCTS_FOOD,
        "monthly_sales": MONTHLY_SALES_FOOD,
        "orders": ORDERS_FOOD,
        "reviews": REVIEWS_FOOD,
        "kol_data": KOL_DATA_FOOD,
        "price_monitoring": PRICE_MONITORING_FOOD,
        "trend_keywords": TREND_KEYWORDS_FOOD,
        "refunds": REFUNDS_FOOD,
    }


def print_food_data_summary():
    """打印数据摘要"""
    data = get_food_mock_data()
    print("=" * 50)
    print("食品饮料 Mock 数据摘要（茶屿 CHAYU）")
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
    print("  1. 冷泡茶夏季热销但毛利低（cost 12 售价 39.9），拉低整体客单价")
    print("  2. 竞品CHALI茶里通过故宫联名礼盒实现368元高溢价")
    print("  3. 茶礼盒（毛利67%）中秋前自然增长（300→600→1200件）")
    print("  4. 抖音食品达人ROI优秀（茶圈老罗 ROI 24），泛娱乐达人全军覆没")
    print("  5. '无糖茶饮''养生茶'搜索趋势持续上升")
    print("  6. 差评集中在口味淡/包装差，需提升产品力和包装设计")
    print("=" * 50)


if __name__ == "__main__":
    print_food_data_summary()
