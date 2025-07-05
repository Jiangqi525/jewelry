# ziwei/algorithm/zhongzhou_calculator.py
import datetime
from typing import Dict
from ganzhi_converter import GanZhiConverter
from palace import Palace, LifePalaceCalculator
from star_system import arrange_major_stars, arrange_aux_stars, StarSystem
from four_transform import FourTransform
from sixty_pattern import PatternAnalyzer


def parse_hour(hour_input):
    """将用户输入的时辰（地支或数字）转换为整数"""
    if isinstance(hour_input, int):
        return hour_input
    try:
        # 地支转数字：子=0, 丑=2, 寅=4...
        return GanZhiConverter.DI_ZHI.index(hour_input) * 2
    except ValueError:
        raise ValueError(f"无效的时辰格式: {hour_input}")


class ZhongZhouCalculator:
    def analyze_wuxing(self, major_pos: dict) -> dict:
        """分析五行平衡"""
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

            # 提取出生日期信息
            year = birth["year"]
            month = birth["month"]
            day = birth["day"]
            hour = birth["hour"]

            # 计算年干支与五行局
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

            # 计算月、日、时干支
            mgz = GanZhiConverter.get_month_ganzhi(ygz, month)
            # 获取月支
            month_zhi = mgz[1]

            dt = datetime.date(year, month, day)
            dgz = GanZhiConverter.get_day_ganzhi(dt)

            # 处理时辰，转换为地支
            if isinstance(hour, int):
                # 24小时制转地支时辰
                hour_zhi_map = {
                    23: "子", 0: "子", 1: "丑", 2: "丑", 3: "寅", 4: "寅",
                    5: "卯", 6: "卯", 7: "辰", 8: "辰", 9: "巳", 10: "巳",
                    11: "午", 12: "午", 13: "未", 14: "未", 15: "申", 16: "申",
                    17: "酉", 18: "酉", 19: "戌", 20: "戌", 21: "亥", 22: "亥"
                }
                hour_zhi = hour_zhi_map.get(hour % 24, "子")
            else:
                hour_zhi = hour  # 已经是地支字符串

            # 计算时干支
            hgz = GanZhiConverter.get_hour_ganzhi(dgz, hour_zhi)

            # 将阳历转换为农历
            hour_int = parse_hour(hour)
            lunar_month, lunar_day, _ = LifePalaceCalculator.solar_to_lunar(
                year, month, day, hour_int
            )

            # 使用农历月份和时辰地支计算命宫与身宫
            life_palace, body_palace = LifePalaceCalculator.calc_life_body_palace(
                lunar_month, hour_zhi
            )

            # 获取性别和年干阴阳属性
            gender = birth.get("gender", "male")
            year_gan = ygz[0]
            yang_tians = ["甲", "丙", "戊", "庚", "壬"]
            is_yang = year_gan in yang_tians
            yin_yang = ("阳" if is_yang else "阴") + ("男" if gender == "male" else "女")

            # 星曜排布
            major_pos = arrange_major_stars(lunar_day, bureau_number)
            # 修复：传递正确的参数给 arrange_aux_stars
            aux_pos = arrange_aux_stars(ygz, month_zhi, hour_zhi)

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

    def generate_report(self, birth: Dict) -> str:
        """
        生成命盘报告文本

        Args:
            birth: 包含出生年、月、日、时的字典

        Returns:
            格式化的命盘报告字符串
        """
        # 计算命盘
        natal_chart = self.calculate(birth)

        # 构建报告
        report = f"中州派紫微斗数命盘分析报告\n"
        report += "=" * 50 + "\n"
        report += f"出生时间: {birth['year']}年{birth['month']}月{birth['day']}日{birth['hour']}时\n"
        report += f"年干支: {natal_chart['year_ganzhi']}\n"
        report += f"月干支: {natal_chart['month_ganzhi']}\n"
        report += f"日干支: {natal_chart['day_ganzhi']}\n"
        report += f"时干支: {natal_chart['hour_ganzhi']}\n"
        report += f"五行局: {natal_chart['wuxing_bureau']}\n"
        report += f"命宫: {natal_chart['life_palace']}\n"
        report += f"身宫: {natal_chart['body_palace']}\n\n"

        # 主星分布
        report += "主星分布:\n"
        for star, position in natal_chart['major_pos'].items():
            report += f"  {star}: {position}宫\n"

        # 辅星分布
        report += "\n辅星分布:\n"
        for star, position in natal_chart['aux_pos'].items():
            report += f"  {star}: {position}宫\n"

        # 四化星
        report += "\n四化星:\n"
        for star, transform in natal_chart['four_trans'].items():
            report += f"  {star}: {transform}\n"

        # 格局分析
        report += "\n格局分析:\n"
        for pattern in natal_chart['patterns']:
            report += f"  {pattern}\n"

        # 五行分析
        wx = natal_chart['wuxing_analysis']
        report += "\n五行平衡分析:\n"
        report += f"  五行分布: {wx['count']}\n"
        report += f"  五行比例: {wx['ratio']}\n"
        report += f"  最强五行: {wx['strongest']}\n"
        report += f"  最弱五行: {wx['weakest']}\n"
        report += f"  缺失五行: {wx['deficiency']}\n"

        return report


class TimeConverter:
    """时辰转换工具类"""
    DI_ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

    @staticmethod
    def to_24h_format(time_input):
        """统一处理时辰输入为24小时制整数"""
        if isinstance(time_input, int) and 0 <= time_input <= 23:
            return time_input
        if time_input in TimeConverter.DI_ZHI:
            return TimeConverter.DI_ZHI.index(time_input) * 2
        raise ValueError(f"无效的时辰格式: {time_input}")

    @staticmethod
    def to_di_zhi(hour: int) -> str:
        """24小时制转地支时辰"""
        hour_zhi_map = {
            23: "子", 0: "子", 1: "丑", 2: "丑", 3: "寅", 4: "寅",
            5: "卯", 6: "卯", 7: "辰", 8: "辰", 9: "巳", 10: "巳",
            11: "午", 12: "午", 13: "未", 14: "未", 15: "申", 16: "申",
            17: "酉", 18: "酉", 19: "戌", 20: "戌", 21: "亥", 22: "亥"
        }
        return hour_zhi_map.get(hour % 24, "子")

    # 从五行局中提取数字部分，支持更多格式
    def extract_bureau_number(bureau: str) -> int:
        chinese_numerals = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
                            '六': 6, '七': 7, '八': 8, '九': 9, '十': 10}

        # 尝试提取阿拉伯数字
        digits = ''.join(filter(str.isdigit, bureau))
        if digits:
            return int(digits)

        # 尝试提取中文数字
        for char in bureau:
            if char in chinese_numerals:
                return chinese_numerals[char]

        # 默认值（根据五行）
        wuxing_map = {"金": 4, "木": 3, "水": 2, "火": 6, "土": 5}
        for wx in wuxing_map:
            if wx in bureau:
                return wuxing_map[wx]

        raise ValueError(f"无法从五行局中提取数字: {bureau}")