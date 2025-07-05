import datetime
from typing import Tuple

class GanZhiConverter:
    TIAN_GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    DI_ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

    # 完整纳音五行表
    NAYIN = {
        "甲子": "海中金", "乙丑": "海中金", "丙寅": "炉中火", "丁卯": "炉中火",
        "戊辰": "大林木", "己巳": "大林木", "庚午": "路旁土", "辛未": "路旁土",
        "壬申": "剑锋金", "癸酉": "剑锋金", "甲戌": "山头火", "乙亥": "山头火",
        "丙子": "涧下水", "丁丑": "涧下水", "戊寅": "城头土", "己卯": "城头土",
        "庚辰": "白蜡金", "辛巳": "白蜡金", "壬午": "杨柳木", "癸未": "杨柳木",
        "甲申": "泉中水", "乙酉": "泉中水", "丙戌": "屋上土", "丁亥": "屋上土",
        "戊子": "霹雳火", "己丑": "霹雳火", "庚寅": "松柏木", "辛卯": "松柏木",
        "壬辰": "长流水", "癸巳": "长流水", "甲午": "砂中金", "乙未": "砂中金",
        "丙申": "山下火", "丁酉": "山下火", "戊戌": "平地木", "己亥": "平地木",
        "庚子": "壁上土", "辛丑": "壁上土", "壬寅": "金箔金", "癸卯": "金箔金",
        "甲辰": "覆灯火", "乙巳": "覆灯火", "丙午": "天河水", "丁未": "天河水",
        "戊申": "大驿土", "己酉": "大驿土", "庚戌": "钗钏金", "辛亥": "钗钏金",
        "壬子": "桑柘木", "癸丑": "桑柘木", "甲寅": "大溪水", "乙卯": "大溪水",
        "丙辰": "沙中土", "丁巳": "沙中土", "戊午": "天上火", "己未": "天上火",
        "庚申": "石榴木", "辛酉": "石榴木", "壬戌": "大海水", "癸亥": "大海水"
    }

    # 纳音五行到五行局的映射
    WUXING_BUREAU = {
        "海中金": "金四局", "炉中火": "火六局", "大林木": "木三局", "路旁土": "土五局",
        "剑锋金": "金四局", "山头火": "火六局", "涧下水": "水二局", "城头土": "土五局",
        "白蜡金": "金四局", "杨柳木": "木三局", "泉中水": "水二局", "屋上土": "土五局",
        "霹雳火": "火六局", "松柏木": "木三局", "长流水": "水二局", "砂中金": "金四局",
        "山下火": "火六局", "平地木": "木三局", "壁上土": "土五局", "金箔金": "金四局",
        "覆灯火": "火六局", "天河水": "水二局", "大驿土": "土五局", "钗钏金": "金四局",
        "桑柘木": "木三局", "大溪水": "水二局", "沙中土": "土五局", "天上火": "火六局",
        "石榴木": "木三局", "大海水": "水二局"
    }

    @staticmethod
    def get_year_ganzhi(year: int) -> Tuple[str, str]:
        """计算年干支，返回(天干地支, 五行局)"""
        base_year = 1900
        offset = year - base_year
        tg = GanZhiConverter.TIAN_GAN[(offset % 10 + 6) % 10]
        dz = GanZhiConverter.DI_ZHI[(offset % 12 + 0) % 12]
        gz = tg + dz
        nayin = GanZhiConverter.NAYIN.get(gz, "土")
        bureau = GanZhiConverter.WUXING_BUREAU.get(nayin, "土五局")
        return gz, bureau

    @staticmethod
    def get_month_ganzhi(year_gz: str, month: int) -> str:
        """计算月干支（以立春后为新正月）"""
        tg_idx = GanZhiConverter.TIAN_GAN.index(year_gz[0])
        # 正月干支 = 当年天干 + 2（丙）再顺推(month-1)
        idx = (tg_idx + 2 + month - 1) % 10
        dz_idx = (month + 1) % 12  # 正月对应寅（索引2）
        return GanZhiConverter.TIAN_GAN[idx] + GanZhiConverter.DI_ZHI[dz_idx]

    @staticmethod
    def get_day_ganzhi(date: datetime.date) -> str:
        """计算日干支（以1899-12-22为甲子日基准）"""
        base = datetime.date(1899, 12, 22)
        diff = (date - base).days
        tg = GanZhiConverter.TIAN_GAN[diff % 10]
        dz = GanZhiConverter.DI_ZHI[diff % 12]
        return tg + dz

    @staticmethod
    def get_hour_ganzhi(day_gz: str, hour_zhi: str) -> str:
        """计算时干支（五鼠遁法）"""
        HOUR_DZ = GanZhiConverter.DI_ZHI
        hz_idx = HOUR_DZ.index(hour_zhi)
        TG_BASE = {"甲": 1, "乙": 1, "丙": 3, "丁": 3, "戊": 5,
                   "己": 5, "庚": 7, "辛": 7, "壬": 9, "癸": 9}
        base = TG_BASE.get(day_gz[0], 1)
        tg = GanZhiConverter.TIAN_GAN[(base + hz_idx) % 10]
        return tg + hour_zhi
