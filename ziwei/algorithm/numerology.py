from typing import List, Dict, Any

class NumerologyAnalyzer:
    """数字能量学分析"""
    # 数字磁场模式
    DIGITAL_PATTERNS = {
        "天医": {
            "combos": {"13", "31", "68", "86", "49", "94", "27", "72"},
            "wuxing": "火",
            "desc": "主财富、婚姻"
        },
        "延年": {
            "combos": {"19", "91", "87", "78", "43", "34", "26", "62"},
            "wuxing": "金",
            "desc": "主能力、责任"
        },
        "绝命": {
            "combos": {"12", "21", "96", "69", "48", "84", "37", "73"},
            "wuxing": "水",
            "desc": "主投资、风险"
        },
        "生气": {
            "combos": {"14", "41", "67", "76", "39", "93", "28", "82"},
            "wuxing": "木",
            "desc": "主贵人、机会"
        }
    }

    @staticmethod
    def calculate_life_number(birth_date: Dict[str, int]) -> int:
        """计算生命数字"""
        digits = [int(d) for d in f"{birth_date['year']}{birth_date['month']:02d}{birth_date['day']:02d}"]
        s = sum(digits)
        while s > 9:
            s = sum(int(d) for d in str(s))
        return s

    @classmethod
    def analyze_patterns(cls, birth_date: Dict[str, int]) -> List[Dict[str, Any]]:
        """分析数字组合磁场"""
        date_str = f"{birth_date['year']}{birth_date['month']:02d}{birth_date['day']:02d}"
        res = []
        for i in range(len(date_str) - 1):
            combo = date_str[i:i+2]
            for name, info in cls.DIGITAL_PATTERNS.items():
                if combo in info["combos"]:
                    res.append({
                        "combo": combo,
                        "pattern": name,
                        "wuxing": info["wuxing"],
                        "description": info["desc"]
                    })
        return res
