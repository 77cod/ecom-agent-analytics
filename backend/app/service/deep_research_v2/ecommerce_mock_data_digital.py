"""
电商运营分析 - Mock 数据集（数码家电）

模拟一个TWS耳机品牌"聆韵 LINGVIBE"的经营数据，包含：
- 商品数据（自家 + 竞品）
- 月度销售数据
- 各平台订单明细
- 用户评价
- 达人带货数据
- 价格监控

数据中埋了一些"问题"和"机会点"，方便AI分析时发现：
1. 主力降噪耳机销量被竞品ANC耳机反超
2. 学生群体购买力上升但平价产品线缺货
3. B站/知乎数码测评达人ROI极高，抖音泛娱乐达人效果差
4. "空间音频""自适应降噪"搜索趋势上升
5. 竞品QCY靠极致性价比在下沉市场爆发
"""

import uuid
from datetime import datetime, timedelta
import random

random.seed(44)

# ============================================================
# 1. 商品数据
# ============================================================
PRODUCTS_DIGITAL = [
    # 自家商品
    {"id": "d001", "name": "聆韵ANC主动降噪耳机 Pro", "brand": "聆韵", "category": "TWS耳机",
     "price": 399.0, "cost": 168.0, "stock": 3500, "is_own": True},
    {"id": "d002", "name": "聆韵运动挂脖式蓝牙耳机", "brand": "聆韵", "category": "运动耳机",
     "price": 199.0, "cost": 72.0, "stock": 5000, "is_own": True},
    {"id": "d003", "name": "聆韵TWS半入耳青春版", "brand": "聆韵", "category": "TWS耳机",
     "price": 149.0, "cost": 52.0, "stock": 800, "is_own": True},  # 缺货！
    {"id": "d004", "name": "聆韵10000mAh超薄充电宝", "brand": "聆韵", "category": "充电宝",
     "price": 79.0, "cost": 28.0, "stock": 10000, "is_own": True},
    {"id": "d005", "name": "聆韵桌面无线快充充电器", "brand": "聆韵", "category": "充电配件",
     "price": 59.0, "cost": 19.0, "stock": 4000, "is_own": True},
    # 竞品商品
    {"id": "d006", "name": "Soundcore ANC降噪耳机 A40", "brand": "Soundcore", "category": "TWS耳机",
     "price": 349.0, "cost": 140.0, "stock": 8000, "is_own": False},
    {"id": "d007", "name": "QCY TWS降噪耳机 T13", "brand": "QCY", "category": "TWS耳机",
     "price": 99.0, "cost": 38.0, "stock": 25000, "is_own": False},  # 极致性价比
    {"id": "d008", "name": "漫步者运动蓝牙耳机", "brand": "漫步者", "category": "运动耳机",
     "price": 179.0, "cost": 65.0, "stock": 7000, "is_own": False},
    {"id": "d009", "name": "倍思超薄充电宝10000mAh", "brand": "倍思", "category": "充电宝",
     "price": 69.0, "cost": 25.0, "stock": 15000, "is_own": False},
    {"id": "d010", "name": "小米无线充电器20W", "brand": "小米", "category": "充电配件",
     "price": 49.0, "cost": 18.0, "stock": 20000, "is_own": False},
]

# ============================================================
# 2. 月度销售汇总（2024年3月-8月）
# ============================================================
MONTHLY_SALES_DIGITAL = [
    # 自家品牌 - ANC降噪耳机Pro
    {"product_id": "d001", "year": 2024, "month": 3, "sales_qty": 1800, "sales_amount": 718200.0, "channel": "天猫"},
    {"product_id": "d001", "year": 2024, "month": 4, "sales_qty": 2400, "sales_amount": 957600.0, "channel": "天猫"},
    {"product_id": "d001", "year": 2024, "month": 5, "sales_qty": 3200, "sales_amount": 1276800.0, "channel": "天猫"},
    {"product_id": "d001", "year": 2024, "month": 6, "sales_qty": 4500, "sales_amount": 1795500.0, "channel": "天猫"},
    {"product_id": "d001", "year": 2024, "month": 7, "sales_qty": 5000, "sales_amount": 1995000.0, "channel": "天猫"},
    {"product_id": "d001", "year": 2024, "month": 8, "sales_qty": 4200, "sales_amount": 1675800.0, "channel": "天猫"},  # 下滑！
    # 自家品牌 - ANC降噪耳机Pro(京东)
    {"product_id": "d001", "year": 2024, "month": 3, "sales_qty": 1200, "sales_amount": 478800.0, "channel": "京东"},
    {"product_id": "d001", "year": 2024, "month": 4, "sales_qty": 1800, "sales_amount": 718200.0, "channel": "京东"},
    {"product_id": "d001", "year": 2024, "month": 5, "sales_qty": 2500, "sales_amount": 997500.0, "channel": "京东"},
    {"product_id": "d001", "year": 2024, "month": 6, "sales_qty": 3300, "sales_amount": 1316700.0, "channel": "京东"},
    {"product_id": "d001", "year": 2024, "month": 7, "sales_qty": 3800, "sales_amount": 1516200.0, "channel": "京东"},
    {"product_id": "d001", "year": 2024, "month": 8, "sales_qty": 3100, "sales_amount": 1236900.0, "channel": "京东"},  # 下滑

    # 自家品牌 - 青春版（缺货影响）
    {"product_id": "d003", "year": 2024, "month": 3, "sales_qty": 600, "sales_amount": 89400.0, "channel": "天猫"},
    {"product_id": "d003", "year": 2024, "month": 4, "sales_qty": 900, "sales_amount": 134100.0, "channel": "天猫"},
    {"product_id": "d003", "year": 2024, "month": 5, "sales_qty": 1500, "sales_amount": 223500.0, "channel": "天猫"},
    {"product_id": "d003", "year": 2024, "month": 6, "sales_qty": 2200, "sales_amount": 327800.0, "channel": "天猫"},
    {"product_id": "d003", "year": 2024, "month": 7, "sales_qty": 3100, "sales_amount": 461900.0, "channel": "天猫"},
    {"product_id": "d003", "year": 2024, "month": 8, "sales_qty": 800, "sales_amount": 119200.0, "channel": "天猫"},  # 断崖下跌！缺货

    # 竞品 - Soundcore ANC A40
    {"product_id": "d006", "year": 2024, "month": 3, "sales_qty": 2200, "sales_amount": 767800.0, "channel": "天猫"},
    {"product_id": "d006", "year": 2024, "month": 4, "sales_qty": 3000, "sales_amount": 1047000.0, "channel": "天猫"},
    {"product_id": "d006", "year": 2024, "month": 5, "sales_qty": 4000, "sales_amount": 1396000.0, "channel": "天猫"},
    {"product_id": "d006", "year": 2024, "month": 6, "sales_qty": 5200, "sales_amount": 1814800.0, "channel": "天猫"},
    {"product_id": "d006", "year": 2024, "month": 7, "sales_qty": 6200, "sales_amount": 2163800.0, "channel": "天猫"},  # 反超
    {"product_id": "d006", "year": 2024, "month": 8, "sales_qty": 7500, "sales_amount": 2617500.0, "channel": "天猫"},  # 持续增长

    # 竞品 - QCY T13（下沉市场爆发）
    {"product_id": "d007", "year": 2024, "month": 6, "sales_qty": 8000, "sales_amount": 792000.0, "channel": "拼多多"},
    {"product_id": "d007", "year": 2024, "month": 7, "sales_qty": 12000, "sales_amount": 1188000.0, "channel": "拼多多"},
    {"product_id": "d007", "year": 2024, "month": 8, "sales_qty": 18000, "sales_amount": 1782000.0, "channel": "拼多多"},  # 爆发！
]


# ============================================================
# 3. 订单明细（最近100条订单）
# ============================================================
def _gen_orders_digital():
    channels = ["天猫", "京东", "抖音", "拼多多", "小红书"]
    cities = ["上海", "北京", "广州", "深圳", "杭州", "成都", "武汉",
              "南京", "重庆", "苏州", "西安", "长沙", "郑州", "东莞", "佛山"]
    statuses = ["已完成", "已完成", "已完成", "已完成", "已完成",
                "已完成", "已完成", "已完成", "退货中", "已退货"]

    orders = []
    base_date = datetime(2024, 8, 20)
    product_ids = ["d001", "d002", "d003", "d004", "d005"]

    for i in range(100):
        pid = random.choice(product_ids)
        product = next(p for p in PRODUCTS_DIGITAL if p["id"] == pid)
        qty = random.choices([1, 1, 1, 1, 2, 2, 3], weights=[35, 30, 15, 8, 7, 3, 2])[0]
        date = base_date - timedelta(days=random.randint(0, 60))
        channel = random.choice(channels)
        city = random.choice(cities)
        status = random.choice(statuses)
        total = round(product["price"] * qty, 2)
        is_refund = status in ("退货中", "已退货")

        orders.append({
            "order_id": f"DG2024{i+1:04d}",
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

ORDERS_DIGITAL = _gen_orders_digital()


# ============================================================
# 4. 用户评价（含好评和差评，有故事性）
# ============================================================
REVIEWS_DIGITAL = [
    # 正面评价
    {"id": "dr001", "product_id": "d001", "rating": 5, "content": "降噪效果惊艳！地铁上基本听不到噪音，音质也不错",
     "date": "2024-07-15", "source": "天猫"},
    {"id": "dr002", "product_id": "d001", "rating": 5, "content": "和airpods pro比降噪只差一点点，但便宜太多，性价比极高",
     "date": "2024-07-20", "source": "天猫"},
    {"id": "dr003", "product_id": "d001", "rating": 4, "content": "整体满意，就是低频降噪不如预期，通话质量还可以",
     "date": "2024-07-22", "source": "天猫"},
    {"id": "dr004", "product_id": "d002", "rating": 5, "content": "跑步用很好，甩不掉也很轻，续航8小时够用",
     "date": "2024-08-01", "source": "京东"},
    {"id": "dr005", "product_id": "d003", "rating": 5, "content": "149元这音质绝了，学生党首选，可惜现在缺货了",
     "date": "2024-08-05", "source": "天猫"},
    {"id": "dr006", "product_id": "d001", "rating": 5, "content": "看了B站UP主测评买的，果然没让人失望，支持国产",
     "date": "2024-08-10", "source": "B站"},
    {"id": "dr007", "product_id": "d001", "rating": 4, "content": "APP功能丰富，EQ调节好用，就是固件升级有点慢",
     "date": "2024-08-12", "source": "天猫"},
    {"id": "dr008", "product_id": "d004", "rating": 5, "content": "超薄设计放口袋刚好，充耳机能用5次，出门必备",
     "date": "2024-08-15", "source": "京东"},
    {"id": "dr009", "product_id": "d001", "rating": 5, "content": "空间音频效果很好，看电影有电影院的感觉",
     "date": "2024-08-18", "source": "天猫"},
    {"id": "dr010", "product_id": "d003", "rating": 4, "content": "性价比确实高，但经常缺货，想再买一个给朋友也下不了单",
     "date": "2024-08-20", "source": "天猫"},

    # 差评（有故事性）
    {"id": "dr011", "product_id": "d001", "rating": 2, "content": "用了两个月左耳不出声了，质量堪忧，品控需要加强",
     "date": "2024-08-08", "source": "天猫"},
    {"id": "dr012", "product_id": "d001", "rating": 1, "content": "降噪效果和描述差距大，广告说的46dB降噪实测根本达不到",
     "date": "2024-08-11", "source": "京东"},
    {"id": "dr013", "product_id": "d001", "rating": 2, "content": "朋友买的Soundcore A40降噪明显更好，价格还便宜50块",
     "date": "2024-08-14", "source": "天猫"},
    {"id": "dr014", "product_id": "d001", "rating": 1, "content": "蓝牙连接不稳定，户外经常断连，跑步根本没法用",
     "date": "2024-08-16", "source": "京东"},
    {"id": "dr015", "product_id": "d002", "rating": 2, "content": "挂脖设计不太舒服，线材太硬了，运动的时候会打到脖子",
     "date": "2024-08-19", "source": "天猫"},
    {"id": "dr016", "product_id": "d001", "rating": 1, "content": "品控太差了，盒子盖松垮垮的，完全没有399该有的质感",
     "date": "2024-08-21", "source": "京东"},
    {"id": "dr017", "product_id": "d003", "rating": 2, "content": "抢了两周才买到，结果到手发现有一边声音小，退货了",
     "date": "2024-08-22", "source": "天猫"},
    {"id": "dr018", "product_id": "d001", "rating": 3, "content": "一般般吧，听起来和百元耳机差别不大，降噪开了也一般",
     "date": "2024-08-23", "source": "天猫"},
    {"id": "dr019", "product_id": "d005", "rating": 2, "content": "充电速度不稳定，有时候快有时候慢，不如小米的稳定",
     "date": "2024-08-25", "source": "京东"},
    {"id": "dr020", "product_id": "d001", "rating": 1, "content": "这个价格选择太多了，Soundcore和漫步者都比这个靠谱",
     "date": "2024-08-26", "source": "天猫"},
]


# ============================================================
# 5. 达人带货数据
# ============================================================
KOL_DATA_DIGITAL = [
    {"kol_name": "数码评测君", "platform": "B站", "followers": 120_0000, "product_id": "d001",
     "commission_rate": 0.12, "estimated_sales": 3000, "estimated_gmv": 1197000.0,
     "fee": 15000, "roi": 79.80, "cooperation_date": "2024-07-05", "niche": "数码评测"},

    {"kol_name": "科技美学小K", "platform": "知乎", "followers": 85_0000, "product_id": "d001",
     "commission_rate": 0.15, "estimated_sales": 1800, "estimated_gmv": 718200.0,
     "fee": 12000, "roi": 59.85, "cooperation_date": "2024-07-12", "niche": "数码科技"},

    {"kol_name": "大耳朵评测", "platform": "B站", "followers": 250_0000, "product_id": "d003",
     "commission_rate": 0.10, "estimated_sales": 2500, "estimated_gmv": 372500.0,
     "fee": 20000, "roi": 18.63, "cooperation_date": "2024-07-18", "niche": "音频评测"},

    {"kol_name": "科技搞机少女", "platform": "小红书", "followers": 38_0000, "product_id": "d001",
     "commission_rate": 0.12, "estimated_sales": 600, "estimated_gmv": 239400.0,
     "fee": 5000, "roi": 47.88, "cooperation_date": "2024-07-22", "niche": "数码好物"},

    {"kol_name": "学生党数码", "platform": "抖音", "followers": 45_0000, "product_id": "d003",
     "commission_rate": 0.10, "estimated_sales": 1500, "estimated_gmv": 223500.0,
     "fee": 6000, "roi": 37.25, "cooperation_date": "2024-08-01", "niche": "学生平价"},

    {"kol_name": "泛娱乐大V老赵", "platform": "抖音", "followers": 1500_0000, "product_id": "d001",
     "commission_rate": 0.20, "estimated_sales": 1200, "estimated_gmv": 478800.0,
     "fee": 120000, "roi": 3.99, "cooperation_date": "2024-08-05", "niche": "泛娱乐"},  # ROI极低

    # 竞品合作的达人
    {"kol_name": "耳机圈老王", "platform": "B站", "followers": 80_0000, "product_id": "d006",
     "commission_rate": 0.15, "estimated_sales": 4000, "estimated_gmv": 1396000.0,
     "fee": 18000, "roi": 77.56, "cooperation_date": "2024-08-01", "niche": "HiFi评测"},  # 竞品
]


# ============================================================
# 6. 竞品价格监控
# ============================================================
PRICE_MONITORING_DIGITAL = [
    {"product_id": "d001", "competitor_product": "Soundcore ANC降噪耳机 A40", "our_price": 399.0,
     "comp_price": 349.0, "price_diff": -50.0, "date": "2024-08-01"},
    {"product_id": "d001", "competitor_product": "Soundcore ANC降噪耳机 A40", "our_price": 399.0,
     "comp_price": 329.0, "price_diff": -70.0, "date": "2024-08-15"},  # 竞品降价
    {"product_id": "d001", "competitor_product": "QCY TWS降噪耳机 T13", "our_price": 399.0,
     "comp_price": 99.0, "price_diff": -300.0, "date": "2024-08-15"},  # 巨大价差
    {"product_id": "d002", "competitor_product": "漫步者运动蓝牙耳机", "our_price": 199.0,
     "comp_price": 179.0, "price_diff": -20.0, "date": "2024-08-15"},
    {"product_id": "d004", "competitor_product": "倍思超薄充电宝10000mAh", "our_price": 79.0,
     "comp_price": 69.0, "price_diff": -10.0, "date": "2024-08-15"},
]


# ============================================================
# 7. 热词趋势数据
# ============================================================
TREND_KEYWORDS_DIGITAL = [
    {"keyword": "ANC主动降噪", "search_index": 280, "month": 3, "year": 2024},
    {"keyword": "ANC主动降噪", "search_index": 350, "month": 4, "year": 2024},
    {"keyword": "ANC主动降噪", "search_index": 480, "month": 5, "year": 2024},
    {"keyword": "ANC主动降噪", "search_index": 620, "month": 6, "year": 2024},
    {"keyword": "ANC主动降噪", "search_index": 750, "month": 7, "year": 2024},
    {"keyword": "ANC主动降噪", "search_index": 720, "month": 8, "year": 2024},

    {"keyword": "空间音频耳机", "search_index": 120, "month": 3, "year": 2024},
    {"keyword": "空间音频耳机", "search_index": 200, "month": 4, "year": 2024},
    {"keyword": "空间音频耳机", "search_index": 360, "month": 5, "year": 2024},
    {"keyword": "空间音频耳机", "search_index": 520, "month": 6, "year": 2024},
    {"keyword": "空间音频耳机", "search_index": 680, "month": 7, "year": 2024},
    {"keyword": "空间音频耳机", "search_index": 780, "month": 8, "year": 2024},  # 持续上升

    {"keyword": "学生党蓝牙耳机", "search_index": 200, "month": 3, "year": 2024},
    {"keyword": "学生党蓝牙耳机", "search_index": 280, "month": 4, "year": 2024},
    {"keyword": "学生党蓝牙耳机", "search_index": 350, "month": 5, "year": 2024},
    {"keyword": "学生党蓝牙耳机", "search_index": 500, "month": 6, "year": 2024},
    {"keyword": "学生党蓝牙耳机", "search_index": 650, "month": 7, "year": 2024},
    {"keyword": "学生党蓝牙耳机", "search_index": 820, "month": 8, "year": 2024},  # 开学季上升
]


# ============================================================
# 8. 退货明细
# ============================================================
REFUNDS_DIGITAL = [
    {"order_id": "DG20240010", "product_id": "d001", "reason": "左耳无声/单耳故障",
     "refund_amount": 399.0, "date": "2024-08-09"},
    {"order_id": "DG20240018", "product_id": "d001", "reason": "降噪效果不符预期",
     "refund_amount": 399.0, "date": "2024-08-14"},
    {"order_id": "DG20240022", "product_id": "d001", "reason": "蓝牙断连频繁",
     "refund_amount": 399.0, "date": "2024-08-18"},
    {"order_id": "DG20240035", "product_id": "d003", "reason": "左右音量不一致",
     "refund_amount": 149.0, "date": "2024-08-22"},
    {"order_id": "DG20240050", "product_id": "d001", "reason": "做工瑕疵/盒子松动",
     "refund_amount": 399.0, "date": "2024-08-23"},
    {"order_id": "DG20240062", "product_id": "d005", "reason": "充电速度不稳定",
     "refund_amount": 59.0, "date": "2024-08-25"},
    {"order_id": "DG20240085", "product_id": "d002", "reason": "佩戴不舒适/线材偏硬",
     "refund_amount": 199.0, "date": "2024-08-27"},
]


# ============================================================
# 辅助方法
# ============================================================
def get_digital_mock_data() -> dict:
    """获取数码家电行业 mock 数据"""
    return {
        "products": PRODUCTS_DIGITAL,
        "monthly_sales": MONTHLY_SALES_DIGITAL,
        "orders": ORDERS_DIGITAL,
        "reviews": REVIEWS_DIGITAL,
        "kol_data": KOL_DATA_DIGITAL,
        "price_monitoring": PRICE_MONITORING_DIGITAL,
        "trend_keywords": TREND_KEYWORDS_DIGITAL,
        "refunds": REFUNDS_DIGITAL,
    }


def print_digital_data_summary():
    """打印数据摘要"""
    data = get_digital_mock_data()
    print("=" * 50)
    print("数码家电 Mock 数据摘要（聆韵 LINGVIBE）")
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
    print("  1. 主力ANC降噪耳机销量被Soundcore A40反超")
    print("  2. 青春版因缺货断崖式下跌（3100→800件），错失学生市场")
    print("  3. QCY以99元极致性价比在拼多多月销18000件")
    print("  4. B站/知乎数码测评达人ROI极高（数码评测君 ROI 79.8）")
    print("  5. 泛娱乐大V老赵坑位费12万ROI仅3.99，需调整KOL策略")
    print("  6. '空间音频''学生党蓝牙耳机'搜索趋势上升")
    print("=" * 50)


if __name__ == "__main__":
    print_digital_data_summary()
