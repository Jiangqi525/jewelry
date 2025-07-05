# ziwei/algorithm/main.py
import json
from zhongzhou_calculator import ZhongZhouCalculator
from numerology import NumerologyAnalyzer
from jewelry_recommendation import JewelryRecommendationEngine

# 珠宝数据库
jewelry_db = [
    {
        "id": 1, "name": "红宝石吊坠", "wuxing": "火",
        "digital_tags": [3, 9, "天医"], "price_tier": "high",
        "fengshui_tags": ["南", "火"]
    },
    {
        "id": 2, "name": "黄水晶手链", "wuxing": "土",
        "digital_tags": [5, 8, "延年"], "price_tier": "mid",
        "fengshui_tags": ["东南", "土"]
    },
    {
        "id": 3, "name": "青金石耳环", "wuxing": "金",
        "digital_tags": [1, 7, "绝命"], "price_tier": "low",
        "fengshui_tags": ["西", "金"]
    },
    {
        "id": 4, "name": "绿幽灵手串", "wuxing": "木",
        "digital_tags": [2, 4, "生气"], "price_tier": "mid",
        "fengshui_tags": ["东", "木"]
    },
    {
        "id": 5, "name": "黑玛瑙戒指", "wuxing": "水",
        "digital_tags": [1, 6, "天医"], "price_tier": "high",
        "fengshui_tags": ["北", "水"]
    }
]

# 自定义收费
fees = {"year": 0.0, "month_day": 12.5, "fengshui": 20.0}


def main():
    try:
        """主程序入口"""
        # 出生数据
        birth = {
            "year": 1990,
            "month": 7,
            "day": 7,
            "hour": 0,  # 整数类型（0-23）
            "gender": "male"
        }

        # 1. 计算中州派命盘
        calc = ZhongZhouCalculator()
        natal_chart = calc.calculate(birth)
        print("=== 中州派命盘分析 ===")
        print(json.dumps(natal_chart, ensure_ascii=False, indent=2))
        print("\n")

        # 2. 分析数字能量
        life_number = NumerologyAnalyzer.calculate_life_number(birth)
        digital_patterns = NumerologyAnalyzer.analyze_patterns(birth)
        print("=== 数字能量分析 ===")
        print(f"生命数字: {life_number}")
        print("数字磁场模式:")
        for p in digital_patterns:
            print(f"  - {p['combo']}: {p['pattern']}({p['wuxing']}) - {p['description']}")
        print("\n")

        # 3. 生成珠宝推荐
        engine = JewelryRecommendationEngine(jewelry_db, fees)
        house_tags = ["东南", "土"]  # 示例风水标签
        recommendation = engine.recommend(
            natal_chart, birth, life_number, digital_patterns, house_tags
        )

        print("=== 珠宝推荐结果 ===")
        for typ, data in recommendation.items():
            if typ == "natal_chart":
                continue
            print(f"\n{typ}:")
            print(f"  费用: ¥{data['fee']}")
            print("  推荐珠宝:")
            for i, item in enumerate(data["items"], 1):
                print(f"    {i}. {item['name']} - {item['wuxing']}属性")
                print(f"       数字标签: {item['digital_tags']}")
                print(f"       价格等级: {item['price_tier']}")
                print(f"       风水标签: {item['fengshui_tags']}")
    except Exception as e:
        import traceback
        print(f"程序运行出错: {str(e)}")
        print("详细错误信息:")
        traceback.print_exc()
        print("\n建议检查以下内容:")
        print("1. 出生日期是否有效（如1990年2月30日）")
        print("2. 时辰格式是否正确（0-23整数或地支字符串）")
        print("3. 依赖库是否安装（pip install lunarcalendar）")


if __name__ == "__main__":
    main()