from enum import Enum
from typing import Tuple, List, Dict, Optional
from datetime import datetime
from lunarcalendar import Converter, Solar, Lunar


class Palace(Enum):
    """十二宫位枚举"""
    LIFE = "命宫"
    SIBLINGS = "兄弟"
    SPOUSE = "夫妻"
    CHILDREN = "子女"
    WEALTH = "财帛"
    HEALTH = "疾厄"
    TRAVEL = "迁移"
    FRIENDS = "交友"
    CAREER = "事业"
    PROPERTY = "田宅"
    BLESS = "福德"
    PARENTS = "父母"


class GanZhiConverter:
    """天干地支转换工具类"""
    TIAN_GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    DI_ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

    @staticmethod
    def get_gan_zhi(year: int) -> str:
        """根据年份计算天干地支"""
        # 公元4年是甲子年
        tian_gan_index = (year - 4) % 10
        di_zhi_index = (year - 4) % 12
        return GanZhiConverter.TIAN_GAN[tian_gan_index] + GanZhiConverter.DI_ZHI[di_zhi_index]

    @staticmethod
    def get_hour_zhi(hour: int) -> str:
        """
        支持两种输入：
        1. 现代24小时制（0-23）
        2. 古代地支时辰（'子','丑'...）
        """
        if isinstance(hour, int):
            # 现代24小时制
            return GanZhiConverter.DI_ZHI[((hour + 1) % 24) // 2]
        elif hour in GanZhiConverter.DI_ZHI:
            # 已经是地支时辰
            return hour
        else:
            raise ValueError(f"无效的时辰格式: {hour}")


class LifePalaceCalculator:
    """紫微斗数命盘计算器"""

    @staticmethod
    def calc_life_body_palace(month: int, hour_zhi: str) -> Tuple[Palace, Palace]:
        # 参数验证增强
        if not (1 <= month <= 12):
            raise ValueError(f"月份必须在1-12之间，当前值: {month}")

        if hour_zhi not in GanZhiConverter.DI_ZHI:
            raise ValueError(f"无效的时辰地支: {hour_zhi}")

        # 地支到数字映射
        HZ_NUM = {z: i for i, z in enumerate(GanZhiConverter.DI_ZHI)}

        # 命宫计算（更精确的公式）
        base_idx = 2  # 寅宫索引（正月）
        month_idx = (base_idx + month - 1) % 12
        hour_steps = HZ_NUM[hour_zhi]
        life_idx = (month_idx - hour_steps) % 12

        # 身宫计算
        body_idx = (base_idx + hour_steps) % 12

        palaces = list(Palace)
        return palaces[life_idx], palaces[body_idx]

    @staticmethod
    def solar_to_lunar(
            year: int,
            month: int,
            day: int,
            hour: int = 12
    ) -> Tuple[int, int, str]:
        """
        使用LunarCalendar库将阳历转换为农历

        Args:
            year: 阳历年份
            month: 阳历月份
            day: 阳历日期
            hour: 小时，用于计算时辰 (0-23)

        Returns:
            (农历月份, 农历日期, 时辰地支) 元组
        """
        # 创建阳历日期对象
        solar_date = Solar(year, month, day)

        # 转换为农历日期
        lunar_date = Converter.Solar2Lunar(solar_date)

        # 获取农历月份和日期
        lunar_month = lunar_date.month
        lunar_day = lunar_date.day

        # 计算时辰地支
        hour_zhi = GanZhiConverter.get_hour_zhi(hour)

        return lunar_month, lunar_day, hour_zhi

    @staticmethod
    def calc_life_body_palace_by_solar(
            year: int,
            month: int,
            day: int,
            hour: int = 12
    ) -> Tuple[Palace, Palace]:
        """
        根据阳历日期和时间计算命宫与身宫

        Args:
            year: 阳历年份
            month: 阳历月份
            day: 阳历日期
            hour: 小时 (0-23)

        Returns:
            (命宫, 身宫) 元组
        """
        # 将阳历转换为农历
        lunar_month, _, hour_zhi = LifePalaceCalculator.solar_to_lunar(
            year, month, day, hour
        )

        # 计算命宫和身宫
        return LifePalaceCalculator.calc_life_body_palace(lunar_month, hour_zhi)

    @staticmethod
    def get_palace_name(palace: Palace) -> str:
        """获取宫位名称"""
        return palace.value

    @staticmethod
    def get_all_palaces() -> List[Palace]:
        """获取所有宫位"""
        return list(Palace)


# 示例用法
if __name__ == "__main__":
    # 使用农历月份和时辰地支计算
    life_palace, body_palace = LifePalaceCalculator.calc_life_body_palace(5, "卯")
    print(f"命宫: {life_palace.value}, 身宫: {body_palace.value}")

    # 使用阳历日期和时间计算
    life_palace, body_palace = LifePalaceCalculator.calc_life_body_palace_by_solar(
        2023, 6, 15, 10
    )
    print(f"命宫: {life_palace.value}, 身宫: {body_palace.value}")

    # 演示阳历转农历
    lunar_month, lunar_day, hour_zhi = LifePalaceCalculator.solar_to_lunar(
        2023, 6, 15, 10
    )
    print(f"阳历 2023-6-15 转换为农历: 农历{lunar_month}月{lunar_day}日，时辰: {hour_zhi}")