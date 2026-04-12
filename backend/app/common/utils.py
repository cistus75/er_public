import os

# ✨ 1. 캐릭터 맵을 파일 상단에 딕셔너리로 직접 정의
# (코드는 str 형태로 저장하여 JSON 및 MongoDB 호환성을 높임)
CHARACTER_MAP = {
    "1": "재키",
    "2": "아야",
    "3": "피오라",
    "4": "매그너스",
    "5": "자히르",
    "6": "나딘",
    "7": "현우",
    "8": "하트",
    "9": "아이솔",
    "10": "리 다이린",
    "11": "유키",
    "12": "혜진",
    "13": "쇼우",
    "14": "키아라",
    "15": "시셀라",
    "16": "실비아",
    "17": "아드리아나",
    "18": "쇼이치",
    "19": "엠마",
    "20": "레녹스",
    "21": "로지",
    "22": "루크",
    "23": "캐시",
    "24": "아델라",
    "25": "버니스",
    "26": "바바라",
    "27": "알렉스",
    "28": "수아",
    "29": "레온",
    "30": "일레븐",
    "31": "리오",
    "32": "윌리엄",
    "33": "니키",
    "34": "나타폰",
    "35": "얀",
    "36": "이바",
    "37": "다니엘",
    "38": "제니",
    "39": "카밀로",
    "40": "클로에",
    "41": "요한",
    "42": "비앙카",
    "43": "셀린",
    "44": "에키온",
    "45": "마이",
    "46": "에이든",
    "47": "라우라",
    "48": "띠아",
    "49": "펠릭스",
    "50": "엘레나",
    "51": "프리야",
    "52": "아디나",
    "53": "마커스",
    "54": "칼라",
    "55": "에스텔",
    "56": "피올로",
    "57": "마르티나",
    "58": "헤이즈",
    "59": "아이작",
    "60": "타지아",
    "61": "이렘",
    "62": "테오도르",
    "63": "이안",
    "64": "바냐",
    "65": "데비&마를렌",
    "66": "아르다",
    "67": "아비게일",
    "68": "알론소",
    "69": "레니",
    "70": "츠바메",
    "71": "케네스",
    "72": "카티야",
    "73": "샬럿",
    "74": "다르코",
    "75": "르노어",
    "76": "가넷",
    "77": "유민",
    "78": "히스이",
    "79": "유스티나",
    "80": "이슈트반",
    "81": "니아",
    "82": "슈린",
    "83": "헨리",
    "84": "블레어",
    "85": "미르카",
    "86": "펜리르",
    "87": "코렐라인"
}

def load_character_map():
    """
    미리 정의된 CHARACTER_MAP 딕셔너리를 반환합니다.
    """
    # ✨ 2. 이제 함수는 파일을 읽는 대신, 이 딕셔너리를 즉시 반환합니다.
    return CHARACTER_MAP

def get_tier(mmr, rank=None):
    """
    MMR과 Rank를 기반으로 정확한 티어를 반환합니다.
    """
    if mmr is None: return 'unranked'
    
    if mmr >= 7800:
        if rank is not None and rank <= 300: return 'immortal'
        if rank is not None and rank <= 1000: return 'titan'
        return 'mithril' # 7800 이상이지만 랭크 정보가 없거나 1000위 밖
    elif mmr >= 7100: return 'mithril' # mmr 7100 ~ 7799 구간
    elif mmr >= 6400: return 'meteorite'
    elif mmr >= 5000: return 'diamond'
    elif mmr >= 3600: return 'platinum'
    elif mmr >= 2400: return 'gold'
    elif mmr >= 1400: return 'silver'
    elif mmr >= 600: return 'bronze'
    elif mmr >= 0: return 'iron'
    else : return 'unrank'


# ==============================================================================
# 캐릭터 역할 매핑
# ==============================================================================

CHARACTER_ROLE_MAP: dict[int, str] = {
    # 탱커
    4: "탱커", 13: "탱커", 20: "탱커", 30: "탱커", 45: "탱커",
    50: "탱커", 53: "탱커", 55: "탱커", 68: "탱커", 76: "탱커",
    # 전사
    1: "전사", 3: "전사", 7: "전사", 10: "전사", 11: "전사",
    14: "전사", 22: "전사", 27: "전사", 28: "전사", 29: "전사",
    33: "전사", 35: "전사", 39: "전사", 44: "전사", 46: "전사",
    47: "전사", 49: "전사", 56: "전사", 59: "전사", 63: "전사",
    65: "전사", 67: "전사", 71: "전사", 74: "전사", 78: "전사",
    80: "전사", 82: "전사", 84: "전사",
    # 암살자
    18: "암살자", 23: "암살자", 37: "암살자",
    # 스킬 딜러
    5: "스킬 딜러", 12: "스킬 딜러", 15: "스킬 딜러", 16: "스킬 딜러",
    17: "스킬 딜러", 19: "스킬 딜러", 24: "스킬 딜러", 26: "스킬 딜러",
    34: "스킬 딜러", 36: "스킬 딜러", 42: "스킬 딜러", 43: "스킬 딜러",
    48: "스킬 딜러", 51: "스킬 딜러", 52: "스킬 딜러", 58: "스킬 딜러",
    60: "스킬 딜러", 61: "스킬 딜러", 64: "스킬 딜러", 66: "스킬 딜러",
    75: "스킬 딜러", 77: "스킬 딜러", 79: "스킬 딜러", 81: "스킬 딜러",
    83: "스킬 딜러",
    # 원거리 딜러
    2: "원거리 딜러", 6: "원거리 딜러", 8: "원거리 딜러", 9: "원거리 딜러",
    21: "원거리 딜러", 25: "원거리 딜러", 31: "원거리 딜러", 32: "원거리 딜러",
    38: "원거리 딜러", 40: "원거리 딜러", 54: "원거리 딜러", 57: "원거리 딜러",
    62: "원거리 딜러", 70: "원거리 딜러", 72: "원거리 딜러",
    # 지원가
    41: "지원가", 69: "지원가", 73: "지원가",
}

_DEALER_ROLES = {"전사", "암살자", "스킬 딜러", "원거리 딜러"}


def get_character_role(character_code: int | None) -> str:
    """캐릭터 코드를 역할 문자열로 변환합니다."""
    if character_code is None:
        return "알 수 없음"
    return CHARACTER_ROLE_MAP.get(int(character_code), "알 수 없음")


# ==============================================================================
# 등급 계산 헬퍼
# ==============================================================================

def _g_high(v: float, s: float, a: float, b: float, c: float) -> str:
    """값이 클수록 좋은 지표의 등급을 반환합니다."""
    if v >= s: return "S"
    if v >= a: return "A"
    if v >= b: return "B"
    if v >= c: return "C"
    return "D"


def _g_low(v: float, s: float, a: float, b: float, c: float) -> str:
    """값이 작을수록 좋은 지표의 등급을 반환합니다."""
    if v <= s: return "S"
    if v <= a: return "A"
    if v <= b: return "B"
    if v <= c: return "C"
    return "D"


def _best_worst(grades: dict[str, str]) -> tuple[dict, dict]:
    """등급 딕셔너리에서 최고·최저 항목을 반환합니다."""
    order = {"S": 5, "A": 4, "B": 3, "C": 2, "D": 1}
    sorted_items = sorted(grades.items(), key=lambda x: order.get(x[1], 0))
    worst_field, worst_grade = sorted_items[0]
    best_field, best_grade = sorted_items[-1]
    return (
        {"field": best_field, "grade": best_grade},
        {"field": worst_field, "grade": worst_grade},
    )


# ==============================================================================
# 랭크/일반 모드 등급 계산
# ==============================================================================

def calculate_stat_grades(stat: dict, character_role: str) -> dict:
    """
    랭크·일반 모드 stat 딕셔너리를 기반으로 지표별 S~D 등급을 계산합니다.

    Returns:
        {
            "grades": {"승률": "A", "KDA": "C", ...},
            "best":   {"field": "승률", "grade": "A"},
            "worst":  {"field": "KDA", "grade": "C"},
        }
    """
    g: dict[str, str] = {}

    g["승률"]          = _g_high(stat.get("win_rate_percentage", 0),  30,   20,   12.5, 10)
    g["Top3 진입률"]   = _g_high(stat.get("top3_rate_percentage", 0), 60,   50,   40,   30)
    g["평균 순위"]     = _g_low( stat.get("average_rank", 99),         3.0,  3.5,  4.0,  5.0)
    g["KDA"]           = _g_high(stat.get("kda", 0),                   4.0,  3.0,  2.0,  1.5)
    g["평균 처치"]     = _g_high(stat.get("average_kills", 0),         5.0,  4.0,  3.0,  2.0)
    g["평균 사망"]     = _g_low( stat.get("average_deaths", 99),        1.5,  2.0,  3.0,  4.0)
    g["평균 어시스트"] = _g_high(stat.get("average_assists", 0),        6.0,  5.0,  3.5,  2.0)
    g["평균 동물 처치"]= _g_high(stat.get("average_monster_kills", 0), 49,   40,   35,   25)
    g["평균 게임 시간"]= _g_high(stat.get("average_game_time_minutes", 0), 18, 17, 15,   12)
    g["평균 시야 점수"]= _g_high(stat.get("avg_vision_score", 0),       30,   25,   20,   10)

    damage = stat.get("average_damage_to_players", 0)
    if character_role in ("전사", "암살자"):
        g["평균 딜량"] = _g_high(damage, 17000, 14000, 11000, 8000)
    elif character_role == "스킬 딜러":
        g["평균 딜량"] = _g_high(damage, 21000, 18000, 14000, 10000)
    elif character_role == "원거리 딜러":
        g["평균 딜량"] = _g_high(damage, 19000, 16000, 13000, 10000)
    elif character_role == "탱커":
        g["평균 받은 피해"] = _g_high(stat.get("avg_damage_from_players", 0), 25000, 20000, 15000, 10000)
    elif character_role == "지원가":
        g["평균 아군 치유량"] = _g_high(stat.get("avg_team_heal", 0), 10000, 8000, 5000, 3000)

    best, worst = _best_worst(g)
    return {"grades": g, "best": best, "worst": worst}


# ==============================================================================
# 코발트 모드 등급 계산
# ==============================================================================

def calculate_cobalt_stat_grades(stat: dict, character_role: str) -> dict:
    """
    코발트 프로토콜 모드 stat 딕셔너리를 기반으로 지표별 S~D 등급을 계산합니다.
    """
    g: dict[str, str] = {}

    g["승률"]          = _g_high(stat.get("win_rate_percentage", 0), 65,  58,  50,  45)
    g["KDA"]           = _g_high(stat.get("kda", 0),                  3.5, 3.0, 2.5, 2.0)
    g["평균 처치"]     = _g_high(stat.get("average_kills", 0),        8.0, 7.0, 6.0, 4.0)
    g["평균 사망"]     = _g_low( stat.get("average_deaths", 99),       6.0, 6.5, 7.0, 8.5)
    g["평균 어시스트"] = _g_high(stat.get("average_assists", 0),      12.0, 10.0, 8.0, 4.0)
    g["평균 보호막 흡수"] = _g_high(stat.get("avg_protect_absorb", 0), 8000, 5500, 4000, 2000)

    kd = stat.get("kd_phase", {})
    g["페이즈1 처치"] = _g_high(kd.get("p1_kills", 0),  2.0, 1.5, 1.0, 0.6)
    g["페이즈1 사망"] = _g_low( kd.get("p1_deaths", 99), 1.5, 2.0, 2.5, 3.0)
    g["페이즈2 처치"] = _g_high(kd.get("p2_kills", 0),  2.0, 1.5, 1.0, 0.6)
    g["페이즈2 사망"] = _g_low( kd.get("p2_deaths", 99), 1.5, 2.0, 2.5, 3.0)
    g["페이즈3 처치"] = _g_high(kd.get("p3_kills", 0),  2.0, 1.5, 1.0, 0.6)
    g["페이즈3 사망"] = _g_low( kd.get("p3_deaths", 99), 1.5, 2.0, 2.5, 3.0)

    damage = stat.get("average_damage_to_players", 0)
    if character_role in ("전사", "암살자"):
        g["평균 딜량"] = _g_high(damage, 29000, 27000, 25000, 20000)
    elif character_role == "스킬 딜러":
        g["평균 딜량"] = _g_high(damage, 36000, 33000, 30000, 25000)
    elif character_role == "원거리 딜러":
        g["평균 딜량"] = _g_high(damage, 37000, 34000, 31000, 26000)
    elif character_role == "탱커":
        g["평균 받은 피해"] = _g_high(stat.get("avg_damage_from_players", 0), 25000, 22000, 18000, 14000)
    elif character_role == "지원가":
        g["평균 아군 치유량"] = _g_high(stat.get("avg_team_heal", 0), 8000, 6000, 4000, 2000)

    best, worst = _best_worst(g)
    return {"grades": g, "best": best, "worst": worst}