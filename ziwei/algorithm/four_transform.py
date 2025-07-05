from typing import Dict, List, Tuple


class FourTransform:
    # 年干四化表，可考虑存入数据库
    YEAR = {
        "甲": ("廉贞", "破军", "武曲", "太阳"),
        "乙": ("天机", "天梁", "紫微", "太阴"),
        "丙": ("天同", "天机", "文昌", "廉贞"),
        "丁": ("太阴", "天同", "天机", "巨门"),
        "戊": ("贪狼", "太阴", "右弼", "天机"),
        "己": ("武曲", "贪狼", "天梁", "文曲"),
        "庚": ("太阳", "武曲", "太阴", "天同"),
        "辛": ("巨门", "太阳", "文曲", "文昌"),
        "壬": ("天梁", "紫微", "左辅", "武曲"),
        "癸": ("破军", "巨门", "太阴", "贪狼")
    }

    # 宫干自化表，可考虑存入数据库
    PALACE = {
        "甲": ("廉贞", "太阳"),
        "乙": ("天机", "太阴"),
        "丙": ("天同", "廉贞"),
        "丁": ("太阴", "巨门"),
        "戊": ("贪狼", "天机"),
        "己": ("武曲", "文曲"),
        "庚": ("太阳", "天同"),
        "辛": ("巨门", "文昌"),
        "壬": ("天梁", "武曲"),
        "癸": ("破军", "贪狼")
    }

    @staticmethod
    def calc(year_gz: str, palace_gan: str) -> dict:
        """
        计算四化星

        Args:
            year_gz: 年份天干地支，如"甲子"
            palace_gan: 宫位天干，如"甲"

        Returns:
            包含四化星信息的字典，键为四化类型，值为对应的星曜
        """
        # 参数验证
        if not year_gz or len(year_gz) < 1:
            raise ValueError("年份不能为空")

        if palace_gan not in FourTransform.PALACE:
            raise ValueError(f"无效的宫位天干: {palace_gan}")

        res = {}
        year_gan = year_gz[0]

        # 年干四化
        if year_gan in FourTransform.YEAR:
            for t, star in zip(["禄", "权", "科", "忌"], FourTransform.YEAR[year_gan]):
                res[f"年干{t}"] = star

        # 宫干自化 - 修正为处理两种自化
        if palace_gan in FourTransform.PALACE:
            stars = FourTransform.PALACE[palace_gan]
            if len(stars) >= 1:
                res["自化禄"] = stars[0]
            if len(stars) >= 2:
                res["自化忌"] = stars[1]

        return res

    @staticmethod
    def get_valid_year_gans() -> List[str]:
        """获取所有有效的年干"""
        return list(FourTransform.YEAR.keys())

    @staticmethod
    def get_valid_palace_gans() -> List[str]:
        """获取所有有效的宫干"""
        return list(FourTransform.PALACE.keys())
