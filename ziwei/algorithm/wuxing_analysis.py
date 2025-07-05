# ziwei/algorithm/zhongzhou_calculator.py
import datetime
from typing import Dict
from ganzhi_converter import GanZhiConverter
from palace import Palace, LifePalaceCalculator
from star_system import arrange_major_stars, arrange_aux_stars
from four_transform import FourTransform
from sixty_pattern import PatternAnalyzer


class ZhongZhouCalculator:
    def analyze_wuxing(self, major_pos: dict) -> dict:
        """分析五行平衡"""
        # 避免循环导入，直接在函数内部导入需要的模块
        from star_system import StarSystem

        cnt = {"金": 0, "木": 0, "水": 0, "火": 0, "土": 0}
        for star in StarSystem.MAJOR:
            if star in major_pos:
                wux = StarSystem.WUXING.get(star, ["土"])
                for w in wux:
                    cnt[w] += 1 / len(wux)  # 双五行分摊

        total = sum(cnt.values())
        ratio = {k: v / total for k, v in cnt.items()}
        strongest = max(ratio, key=ratio.get)
        weakest = min(ratio, key=ratio.get)
        deficiency = [k for k, v in ratio.items() if v < 0.15] or ["无"]

        return {
            "count": cnt,
            "ratio": ratio,
            "strongest": strongest,
            "weakest": weakest,
            "deficiency": deficiency
        }

    def calculate(self, birth: Dict) -> Dict:
        """
        计算完整中州派紫微斗数命盘

        Args:
            birth: 包含出生年、月、日、时的字典

        Returns:
            包含完整命盘信息的字典

        Raises:
            ValueError: 缺少必要参数或参数错误
            RuntimeError: 命盘计算过程中发生错误
        """
        try:
            # 校验必要参数
            required_keys = ["year", "month", "day", "hour"]
            for key in required_keys:
                if key not in birth:
                    raise ValueError(f"缺少必要参数: {key}")

            # 计算干支
            year = birth["year"]
            month = birth["month"]
            day = birth["day"]
            hour = birth["hour"]

            # 年干支与五行局
            ygz, bureau = GanZhiConverter.get_year_ganzhi(year)
            print(f"年干支: {ygz}, 五行局: {bureau}")  # 添加调试信息

            # 确保五行局有效
            if not bureau:
                raise ValueError(f"无效的五行局: {bureau}")

            # 从五行局中提取数字部分，支持中文数字
            chinese_numerals = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
                                '六': 6, '七': 7, '八': 8, '九': 9, '十': 10}

            # 尝试提取阿拉伯数字
            digits = ''.join(filter(str.isdigit, bureau))

            # 如果没有找到阿拉伯数字，尝试提取中文数字
            if not digits:
                chinese_digits = [chinese_numerals.get(c) for c in bureau if c in chinese_numerals]
                if chinese_digits:
                    digits = str(chinese_digits[0])

            if not digits:
                raise ValueError(f"五行局中未找到数字: {bureau}")

            bureau_number = int(digits)
            print(f"提取的五行局数字: {bureau_number}")  # 添加调试信息

            mgz = GanZhiConverter.get_month_ganzhi(ygz, month)
            dt = datetime.date(year, month, day)
            dgz = GanZhiConverter.get_day_ganzhi(dt)
            hgz = GanZhiConverter.get_hour_ganzhi(dgz, hour)

            # 将阳历转换为农历
            lunar_month, lunar_day, hour_zhi = LifePalaceCalculator.solar_to_lunar(
                year, month, day, hour
            )

            # 使用农历月份和时辰地支计算命宫与身宫
            life_palace, body_palace = LifePalaceCalculator.calc_life_body_palace(
                lunar_month, hour_zhi
            )

            # 星曜排布
            major_pos = arrange_major_stars(day, bureau_number)
            aux_pos = arrange_aux_stars(ygz, hour)

            # 四化星
            trans = FourTransform.calc(ygz, ygz[0])  # 简化为年干四化

            # 六十星系格局
            patterns = PatternAnalyzer.identify(major_pos)

            # 五行平衡分析
            wuxing_analysis = self.analyze_wuxing(major_pos)

            return {
                "year_ganzhi": ygz,
                "month_ganzhi": mgz,
                "day_ganzhi": dgz,
                "hour_ganzhi": hgz,
                "wuxing_bureau": bureau,
                "life_palace": life_palace.value,
                "body_palace": body_palace.value,
                "major_pos": major_pos,
                "aux_pos": aux_pos,
                "four_trans": trans,
                "patterns": patterns,
                "wuxing_analysis": wuxing_analysis
            }
        except ValueError as e:
            raise ValueError(f"参数错误: {str(e)}") from e
        except Exception as e:
            raise RuntimeError(f"命盘计算失败: {str(e)}") from e