from enum import Enum
from typing import List, Dict, Callable
from star_system import StarSystem


class SixtyPattern(Enum):
    ZIWEI_TIANFU = "紫府朝垣"
    JIYUE_TONGLIANG = "机月同梁"
    TAIYANG_TAIYIN = "太阳太阴"
    WUQU_TIANXIANG = "武曲天相"
    QISHA_POJUN = "七杀破军"
    ZIWEI_TIANJI = "紫微天机"
    ZIWEI_TAIYANG = "紫微太阳"
    ZIWEI_LIANZHEN = "紫微廉贞"
    TIANFU_TAIYIN = "天府太阴"
    TIANFU_TANLANG = "天府贪狼"
    TIANFU_JUMEN = "天府巨门"
    TIANJI_TAIYIN = "天机太阴"
    TIANJI_JUMEN = "天机巨门"
    TAIYANG_LIANZHEN = "太阳廉贞"
    WUQU_LIANZHEN = "武曲廉贞"
    WUQU_TANLANG = "武曲贪狼"
    TIANXIANG_TANLANG = "天相贪狼"
    TIANLIANG_TANLANG = "天梁贪狼"
    QISHA_LIANZHEN = "七杀廉贞"


class PatternAnalyzer:
    RULES = {
        SixtyPattern.ZIWEI_TIANFU: {
            "stars": ("紫微", "天府"),
            "check": lambda a, b: abs(a - b) == 6,
            "wuxing": "土",
            "score": 0.9,
            "desc": "紫府朝垣格，主富贵双全，一生顺遂"
        },
        SixtyPattern.JIYUE_TONGLIANG: {
            "stars": ("天机", "太阴", "天同", "天梁"),
            "check": lambda a, b, c, d: all(p % 3 == 0 for p in {a, b, c, d}),
            "wuxing": "水木",
            "score": 0.8,
            "desc": "机月同梁格，主聪明巧智，适合文职或技术工作"
        },
        SixtyPattern.TAIYANG_TAIYIN: {
            "stars": ("太阳", "太阴"),
            "check": lambda a, b: abs(a - b) == 6,
            "wuxing": "火水",
            "score": 0.7,
            "desc": "太阳太阴格，主阴阳调和，一生多贵人相助"
        },
        SixtyPattern.WUQU_TIANXIANG: {
            "stars": ("武曲", "天相"),
            "check": lambda a, b: abs(a - b) == 3,
            "wuxing": "金水",
            "score": 0.75,
            "desc": "武曲天相格，主刚毅果决，适合从事金融或管理工作"
        },
        SixtyPattern.QISHA_POJUN: {
            "stars": ("七杀", "破军"),
            "check": lambda a, b: abs(a - b) == 3,
            "wuxing": "金",
            "score": 0.65,
            "desc": "七杀破军格，主人生多变，需经历磨练方能成功"
        },
        SixtyPattern.ZIWEI_TIANJI: {
            "stars": ("紫微", "天机"),
            "check": lambda a, b: abs(a - b) == 1,
            "wuxing": "土木",
            "score": 0.85,
            "desc": "紫微天机格，主智慧过人，善于谋略规划"
        },
        SixtyPattern.ZIWEI_TAIYANG: {
            "stars": ("紫微", "太阳"),
            "check": lambda a, b: abs(a - b) == 2,
            "wuxing": "土火",
            "score": 0.85,
            "desc": "紫微太阳格，主贵气十足，适合从政或公众事业"
        },
        SixtyPattern.ZIWEI_LIANZHEN: {
            "stars": ("紫微", "廉贞"),
            "check": lambda a, b: abs(a - b) == 5,
            "wuxing": "土火水",
            "score": 0.8,
            "desc": "紫微廉贞格，主才华横溢，但需注意人际关系"
        },
        SixtyPattern.TIANFU_TAIYIN: {
            "stars": ("天府", "太阴"),
            "check": lambda a, b: abs(a - b) == 3,
            "wuxing": "土水",
            "score": 0.75,
            "desc": "天府太阴格，主温和富态，擅长理财持家"
        },
        SixtyPattern.TIANFU_TANLANG: {
            "stars": ("天府", "贪狼"),
            "check": lambda a, b: abs(a - b) == 4,
            "wuxing": "土木水",
            "score": 0.7,
            "desc": "天府贪狼格，主多才多艺，交际能力强"
        },
        SixtyPattern.TIANFU_JUMEN: {
            "stars": ("天府", "巨门"),
            "check": lambda a, b: abs(a - b) == 5,
            "wuxing": "土",
            "score": 0.65,
            "desc": "天府巨门格，主性格耿直，适合法律或研究工作"
        },
        SixtyPattern.TIANJI_TAIYIN: {
            "stars": ("天机", "太阴"),
            "check": lambda a, b: abs(a - b) == 2,
            "wuxing": "木水",
            "score": 0.7,
            "desc": "天机太阴格，主心思细腻，适合艺术或策划工作"
        },
        SixtyPattern.TIANJI_JUMEN: {
            "stars": ("天机", "巨门"),
            "check": lambda a, b: abs(a - b) == 4,
            "wuxing": "木土",
            "score": 0.6,
            "desc": "天机巨门格，主口才出众，适合销售或教育工作"
        },
        SixtyPattern.TAIYANG_LIANZHEN: {
            "stars": ("太阳", "廉贞"),
            "check": lambda a, b: abs(a - b) == 3,
            "wuxing": "火水",
            "score": 0.7,
            "desc": "太阳廉贞格，主热情积极，但需注意情绪管理"
        },
        SixtyPattern.WUQU_LIANZHEN: {
            "stars": ("武曲", "廉贞"),
            "check": lambda a, b: abs(a - b) == 2,
            "wuxing": "金水火",
            "score": 0.7,
            "desc": "武曲廉贞格，主坚毅果敢，适合军警或工程工作"
        },
        SixtyPattern.WUQU_TANLANG: {
            "stars": ("武曲", "贪狼"),
            "check": lambda a, b: abs(a - b) == 1,
            "wuxing": "金木水",
            "score": 0.65,
            "desc": "武曲贪狼格，主敢作敢为，适合创业或冒险事业"
        },
        SixtyPattern.TIANXIANG_TANLANG: {
            "stars": ("天相", "贪狼"),
            "check": lambda a, b: abs(a - b) == 2,
            "wuxing": "水木",
            "score": 0.6,
            "desc": "天相贪狼格，主八面玲珑，适合公关或外交工作"
        },
        SixtyPattern.TIANLIANG_TANLANG: {
            "stars": ("天梁", "贪狼"),
            "check": lambda a, b: abs(a - b) == 5,
            "wuxing": "土水木",
            "score": 0.6,
            "desc": "天梁贪狼格，主聪明伶俐，但需注意脚踏实地"
        },
        SixtyPattern.QISHA_LIANZHEN: {
            "stars": ("七杀", "廉贞"),
            "check": lambda a, b: abs(a - b) == 1,
            "wuxing": "金火",
            "score": 0.55,
            "desc": "七杀廉贞格，主性格刚烈，需注意克制冲动"
        }
    }

    @staticmethod
    def identify(major_pos: Dict[str, int]) -> List[Dict]:
        """
        识别命盘中的六十星系格局

        Args:
            major_pos: 主星星曜位置字典，格式为 {星曜名称: 宫位索引}

        Returns:
            包含所有识别到的格局信息的列表，每个格局包含名称、五行、评分和描述
        """
        identified_patterns = []

        for pattern, rule in PatternAnalyzer.RULES.items():
            stars = rule["stars"]
            required_stars = set(stars)
            present_stars = required_stars & set(major_pos.keys())

            # 检查是否所有格局所需星曜都存在
            if present_stars != required_stars:
                continue

            # 获取星曜位置
            positions = [major_pos[star] for star in stars]

            # 检查格局规则
            check_func = rule["check"]
            if check_func(*positions):
                identified_patterns.append({
                    "name": pattern.value,
                    "wuxing": rule["wuxing"],
                    "score": rule["score"],
                    "desc": rule["desc"]
                })

        return identified_patterns
