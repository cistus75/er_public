import os
import httpx
import re

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

def get_latest_character_map(api_key, db_collection):
    """
    ER API에서 최신 캐릭터 맵을 가져와 MongoDB에 갱신합니다.
    API 호출 실패 시, 하드코딩된 CHARACTER_MAP을 Fallback으로 사용합니다.
    """
    base_map = CHARACTER_MAP.copy()
    if not api_key or db_collection is None:
        return base_map
        
    try:
        headers = {"x-api-key": api_key, "accept": "application/json"}
        # 1. 메타 데이터 조회
        char_res = httpx.get("https://open-api.bser.io/v1/data/Character", headers=headers, timeout=10.0)
        char_res.raise_for_status()
        char_data = char_res.json()
        if char_data.get('code') != 200:
            return base_map
            
        # 2. 한국어 경로 조회
        l10n_res = httpx.get("https://open-api.bser.io/v1/l10n/Korean", headers=headers, timeout=10.0)
        l10n_res.raise_for_status()
        l10n_path = l10n_res.json().get('data', {}).get('l10Path')
        
        if not l10n_path:
            return base_map
            
        # 3. 실제 텍스트 로드 및 정규식 치환
        txt_res = httpx.get(l10n_path, timeout=10.0)
        txt_res.raise_for_status()
        
        lines = txt_res.text.splitlines()
        for line in lines:
            if line.startswith("Character/Name/"):
                parts = re.split(r' [┃=] ', line)
                if len(parts) == 2:
                    code_part = parts[0].replace("Character/Name/", "").strip()
                    name = parts[1].strip()
                    base_map[code_part] = name
                    
        # MongoDB에 저장 (콜렉터가 수집 후 백엔드용으로 갱신)
        db_collection.update_one({'_id': 'character_map'}, {'$set': {'map': base_map}}, upsert=True)
        return base_map
        
    except Exception as e:
        print(f"⚠️ 최신 캐릭터 맵 동기화 실패 (Fallback 사용): {e}")
        return base_map

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