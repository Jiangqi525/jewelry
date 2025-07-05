from typing import List, Dict, Any
import datetime
from ganzhi_converter import GanZhiConverter


class JewelryRecommendationEngine:
    """珠宝推荐引擎，基于紫微斗数和风水理论为用户推荐合适的珠宝"""

    def __init__(self, jewelry_db: List[Dict], fees: Dict[str, float] = None):
        """
        初始化珠宝推荐引擎

        Args:
            jewelry_db: 珠宝数据库，每条记录包含id、名称、五行属性等信息
            fees: 推荐服务费用配置，默认为{"year": 0.0, "month_day": 10.0, "fengshui": 15.0}
        """
        self.db = jewelry_db
        self.fees = fees or {"year": 0.0, "month_day": 10.0, "fengshui": 15.0}

    def recommend_by_year(self, natal: Dict[str, Any]) -> List[Dict]:
        """
        按出生年五行局推荐珠宝

        Args:
            natal: 包含五行局信息的字典

        Returns:
            推荐的珠宝列表
        """
        bureau = natal.get("wuxing_bureau", "")
        wuxing = bureau[0] if bureau else None
        if not wuxing:
            return []
        return [j for j in self.db if j["wuxing"] == wuxing]

    def recommend_by_month_day(self, birth_date: Dict[str, Any],
                               life_number: int, digital_patterns: List[Dict[str, Any]]) -> List[Dict]:
        """
        按月日干支、生命数字、数字磁场推荐珠宝

        Args:
            birth_date: 包含月日干支信息的字典
            life_number: 生命数字
            digital_patterns: 数字磁场模式列表

        Returns:
            推荐的珠宝列表
        """
        recs = []
        mgz = birth_date.get("month_ganzhi", "")
        dgz = birth_date.get("day_ganzhi", "")

        # 1. 月日干支纳音五行
        for tag, gz in [("月", mgz), ("日", dgz)]:
            if gz:
                nayin = GanZhiConverter.NAYIN.get(gz, "")
                wux = nayin[-1] if nayin else None
                if wux:
                    recs += [j for j in self.db if j["wuxing"] == wux]

        # 2. 生命数字
        if life_number:
            recs += [j for j in self.db if life_number in j.get("digital_tags", [])]

        # 3. 数字磁场
        dpats = {p["pattern"] for p in digital_patterns} if digital_patterns else set()
        if dpats:
            recs += [j for j in self.db if dpats & set(j.get("digital_tags", []))]

        return self._dedupe_sort(recs)

    def recommend_by_fengshui(self, house_tags: List[str]) -> List[Dict]:
        """
        按风水住所标签推荐珠宝

        Args:
            house_tags: 风水住所标签列表

        Returns:
            推荐的珠宝列表
        """
        if not house_tags:
            return []
        recs = [j for j in self.db if set(house_tags) & set(j.get("fengshui_tags", []))]
        return self._dedupe_sort(recs)

    def _dedupe_sort(self, recs: List[Dict]) -> List[Dict]:
        """
        对推荐结果进行去重和排序

        Args:
            recs: 推荐结果列表

        Returns:
            去重和排序后的推荐结果
        """
        if not recs:
            return []

        seen = set()
        out = []
        for j in recs:
            if j["id"] not in seen:
                seen.add(j["id"])
                out.append(j)

        # 按价格等级(高>中>低)和数字标签数量排序
        tier_order = {"high": 0, "mid": 1, "low": 2}
        out.sort(key=lambda x: (
            tier_order.get(x["price_tier"], 3),
            -len(x.get("digital_tags", []))
        ))
        return out

    def get_fee(self, method: str) -> float:
        """
        获取推荐服务费用

        Args:
            method: 推荐方法，如"year"、"month_day"、"fengshui"

        Returns:
            对应的服务费用
        """
        return self.fees.get(method, 0.0)

    def recommend(self, natal: Dict[str, Any], birth_date: Dict[str, Any],
                  life_number: int, digital_patterns: List[Dict[str, Any]],
                  house_tags: List[str] = None) -> Dict[str, Any]:
        """
        生成综合推荐结果

        Args:
            natal: 命盘信息
            birth_date: 出生日期信息
            life_number: 生命数字
            digital_patterns: 数字磁场模式
            house_tags: 风水住所标签列表(可选)

        Returns:
            包含各种推荐结果的字典
        """
        # 年度推荐（免费）
        year_list = self.recommend_by_year(natal)

        # 月/日推荐（收费）
        month_day_list = self.recommend_by_month_day(birth_date, life_number, digital_patterns)

        # 风水推荐（收费，可选）
        feng_list = []
        if house_tags:
            feng_list = self.recommend_by_fengshui(house_tags)

        return {
            "natal_chart": natal,
            "year_recommend": {
                "items": year_list,
                "fee": self.get_fee("year")
            },
            "month_day_recommend": {
                "items": month_day_list,
                "fee": self.get_fee("month_day")
            },
            "fengshui_recommend": {
                "items": feng_list,
                "fee": self.get_fee("fengshui")
            }
        }
