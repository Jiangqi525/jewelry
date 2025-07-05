from typing import Dict, List, Tuple
from palace import LifePalaceCalculator

# 月份地支映射表
month_zhi_map = ["寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥", "子", "丑"]

class StarSystem:
    MAJOR = ["紫微", "天机", "太阳", "武曲", "天同", "廉贞",
             "天府", "太阴", "贪狼", "巨门", "天相", "天梁", "七杀", "破军"]
    AUX = ["文昌", "文曲", "左辅", "右弼", "禄存", "天魁", "天钺",
           "天马", "擎羊", "陀罗", "火星", "铃星", "地空", "地劫"]

    # 星曜五行（含双属性），可考虑存入数据库
    WUXING = {
        "紫微": ["土"], "天机": ["木"], "太阳": ["火"], "武曲": ["金"], "天同": ["水"], "廉贞": ["火", "水"],
        "天府": ["土"], "太阴": ["水"], "贪狼": ["木", "水"], "巨门": ["土"], "天相": ["水"], "天梁": ["土"],
        "七杀": ["金"], "破军": ["水"],
        "文昌": ["木"], "文曲": ["水"], "左辅": ["土"], "右弼": ["土"],
        "天魁": ["金"], "天钺": ["金"], "禄存": ["土"], "天马": ["火"],
        "擎羊": ["金"], "陀罗": ["金"], "火星": ["火"], "铃星": ["火"], "地空": ["土"], "地劫": ["土"]
    }

    @staticmethod
    def get_star_wuxing(star_name: str) -> List[str]:
        """获取星曜的五行属性"""
        return StarSystem.WUXING.get(star_name, [])

    @staticmethod
    def is_major_star(star_name: str) -> bool:
        """判断是否为主星"""
        return star_name in StarSystem.MAJOR

    @staticmethod
    def is_aux_star(star_name: str) -> bool:
        """判断是否为辅星"""
        return star_name in StarSystem.AUX


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
        """根据小时计算地支时辰"""
        # 23:00-1:00为子时，1:00-3:00为丑时，依此类推
        index = ((hour - 1) % 24) // 2
        return GanZhiConverter.DI_ZHI[index]

    @staticmethod
    def get_month_zhi(month: int) -> str:
        """根据农历月份计算地支月建"""
        # 寅月为正月，依此类推
        index = (month - 1) % 12
        return GanZhiConverter.DI_ZHI[index]


def arrange_major_stars(day: int, bureau: int, yin_yang: str = "阳男") -> Dict[str, int]:
    """
    排布十四主星（考虑阴阳属性）

    Args:
        day: 农历日期
        bureau: 局数（五行局数字）
        yin_yang: 阴阳属性（"阳男", "阴女", "阴男", "阳女"）

    Returns:
        包含所有主星星曜及其位置的字典
    """
    # 计算紫微星位置
    zi_pos = (bureau * ((day - 1) % bureau)) % 12

    # 紫微系（根据阴阳属性决定方向）
    major = {}
    seq1 = ["紫微", "天机", "太阳", "武曲", "天同", "廉贞"]

    # 阳男阴女顺行，阴男阳女逆行
    direction = 1 if yin_yang in ["阳男", "阴女"] else -1

    for i, s in enumerate(seq1):
        major[s] = (zi_pos + direction * i) % 12

    # 天府系（与紫微系方向相反）
    tianfu_pos = (zi_pos + 6) % 12
    seq2 = ["天府", "太阴", "贪狼", "巨门", "天相", "天梁", "七杀", "破军"]

    for i, s in enumerate(seq2):
        major[s] = (tianfu_pos - direction * i) % 12

    return major


def arrange_aux_stars(year_gz: str, month_zhi: str, hour_zhi: str) -> Dict[str, int]:
    """
    排布辅星（根据年份、月份和时辰计算）

    Args:
        year_gz: 年份天干地支，如"甲子"
        month_zhi: 月份地支，如"寅"
        hour_zhi: 时辰地支，如"子"

    Returns:
        包含所有辅星星曜及其位置的字典
    """
    # 提取年份天干
    year_gan = year_gz[0]

    # 计算禄存星位置
    LU_CUN_TABLE = {
        "甲": 2,  # 寅
        "乙": 3,  # 卯
        "丙": 4,  # 辰
        "丁": 6,  # 午
        "戊": 7,  # 未
        "己": 8,  # 申
        "庚": 9,  # 酉
        "辛": 10,  # 戌
        "壬": 0,  # 子
        "癸": 1  # 丑
    }
    lu_cun_pos = LU_CUN_TABLE.get(year_gan, 0)

    # 优化天马星计算
    tian_ma_pos = 0
    if month_zhi in ["寅", "申", "巳", "亥"]:
        # 寅申巳亥年出生，天马在出生月份的对冲宫位
        tian_ma_map = {"寅": 6, "申": 0, "巳": 9, "亥": 3}
        tian_ma_pos = tian_ma_map.get(month_zhi, 0)
    else:
        # 其他年份，天马在命宫
        tian_ma_pos = LifePalaceCalculator.calc_life_body_palace(
            month_zhi_map.index(month_zhi) + 1, hour_zhi
        )[0].value

    # 计算文昌文曲位置
    WEN_CHANG_TABLE = {
        "甲": 0,  # 子
        "乙": 11,  # 亥
        "丙": 10,  # 戌
        "丁": 9,  # 酉
        "戊": 8,  # 申
        "己": 7,  # 未
        "庚": 6,  # 午
        "辛": 5,  # 巳
        "壬": 4,  # 辰
        "癸": 3  # 卯
    }
    wen_chang_pos = WEN_CHANG_TABLE.get(year_gan, 0)
    wen_qu_pos = (wen_chang_pos + 6) % 12  # 文曲对冲文昌

    # 计算左辅右弼位置
    ZUO_FU_TABLE = {
        "甲": 1,  # 丑
        "乙": 0,  # 子
        "丙": 11,  # 亥
        "丁": 10,  # 戌
        "戊": 9,  # 酉
        "己": 8,  # 申
        "庚": 7,  # 未
        "辛": 6,  # 午
        "壬": 5,  # 巳
        "癸": 4  # 辰
    }
    zuo_fu_pos = ZUO_FU_TABLE.get(year_gan, 0)
    you_bi_pos = (zuo_fu_pos + 6) % 12  # 右弼对冲左辅

    # 计算擎羊陀罗位置
    QING_YANG_TABLE = {
        "甲": 0,  # 子
        "乙": 11,  # 亥
        "丙": 10,  # 戌
        "丁": 9,  # 酉
        "戊": 8,  # 申
        "己": 7,  # 未
        "庚": 6,  # 午
        "辛": 5,  # 巳
        "壬": 4,  # 辰
        "癸": 3  # 卯
    }
    qing_yang_pos = QING_YANG_TABLE.get(year_gan, 0)
    tuo_luo_pos = (qing_yang_pos + 6) % 12  # 陀罗对冲擎羊

    # 计算火铃星位置
    HUO_LING_TABLE = {
        "甲": 7,  # 未
        "乙": 8,  # 申
        "丙": 9,  # 酉
        "丁": 10,  # 戌
        "戊": 11,  # 亥
        "己": 0,  # 子
        "庚": 1,  # 丑
        "辛": 2,  # 寅
        "壬": 3,  # 卯
        "癸": 4  # 辰
    }
    huo_pos = HUO_LING_TABLE.get(year_gan, 0)
    ling_pos = (huo_pos + 6) % 12  # 铃星对冲火星

    # 计算地空地劫位置（固定位置）
    DI_KONG_POS = 9  # 戌宫
    DI_JIE_POS = 3  # 卯宫

    # 计算天魁天钺位置
    TIAN_KUI_TABLE = {
        "甲": 1,  # 丑
        "乙": 0,  # 子
        "丙": 9,  # 酉
        "丁": 8,  # 申
        "戊": 7,  # 未
        "己": 6,  # 午
        "庚": 5,  # 巳
        "辛": 4,  # 辰
        "壬": 11,  # 亥
        "癸": 10  # 戌
    }
    tian_kui_pos = TIAN_KUI_TABLE.get(year_gan, 0)
    tian_yue_pos = (tian_kui_pos + 6) % 12  # 天钺对冲天魁

    # 组装所有辅星位置
    aux_stars = {
        "文昌": wen_chang_pos,
        "文曲": wen_qu_pos,
        "左辅": zuo_fu_pos,
        "右弼": you_bi_pos,
        "天魁": tian_kui_pos,
        "天钺": tian_yue_pos,
        "禄存": lu_cun_pos,
        "天马": tian_ma_pos,
        "擎羊": qing_yang_pos,
        "陀罗": tuo_luo_pos,
        "火星": huo_pos,
        "铃星": ling_pos,
        "地空": DI_KONG_POS,
        "地劫": DI_JIE_POS
    }

    return aux_stars


def arrange_all_stars(day: int, bureau: str, year_gz: str, month_zhi: str, hour_zhi: str) -> Dict[str, int]:
    """
    排布所有星曜（主星和辅星）

    Args:
        day: 农历日期
        bureau: 局数
        year_gz: 年份天干地支
        month_zhi: 月份地支
        hour_zhi: 时辰地支

    Returns:
        包含所有星曜及其位置的字典
    """
    # 排布主星
    major_stars = arrange_major_stars(day, bureau)

    # 排布辅星
    aux_stars = arrange_aux_stars(year_gz, month_zhi, hour_zhi)

    # 合并所有星曜
    all_stars = {**major_stars, **aux_stars}

    return all_stars