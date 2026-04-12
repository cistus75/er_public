import os
import json
import random
import asyncio
import httpx
from datetime import datetime, timedelta, timezone # [수정] 날짜 계산용 모듈
from dateutil import parser 
from dotenv import load_dotenv
from pymongo import MongoClient
import sys

load_dotenv()

# ==========================================
# [설정]
# ==========================================
BASE_URL = "https://open-api.bser.io"
API_KEY = os.getenv("OPEN_API_KEY")
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "er-user-insight" 
COLLECTION_NAME = "raw_games" 

# 필터링 조건
TARGET_SEASON_ID = 37        
TARGET_TEAM_MODE = 3         
TARGET_MATCHING_MODE = 3     
TARGET_SERVER_NAME = "Asia"  

# 테스트 목표 및 수집 설정
SCAN_LIMIT = 60000
CHUNK_SIZE = 50   
RATE_LIMIT = 40
DAYS_LIMIT = 7  # [추가] 7일 제한 설정
# ==========================================

REQUIRED_FIELDS = [
    # 1. 식별 및 게임 환경
    'gameId',             # 게임 고유 ID
    'nickname',           # 유저 닉네임
    'seasonId',           # 시즌 ID
    'serverName',         # 서버 (Asia)
    'startDtm',           # 게임 시작 시간 (핫픽스/기간 필터링용)
    'matchingMode',       # 매칭 모드 (2:일반, 3:랭크)
    'matchingTeamMode',   # 팀 모드 (3:스쿼드)
    'versionSeason',      # 시즌 버전 (예: 9)
    'versionMajor',       # 메이저 버전 (예: 4)

    # 2. 성적 및 캐릭터
    'characterNum',       # 플레이한 캐릭터 코드
    'mmrBefore',          # 게임 시작 전 MMR
    'gameRank',           # 최종 등수
    'playTime',           # 플레이 시간 (초 단위)

    # 3. 전투 지표
    'playerKill',         # 개인 킬
    'playerAssistant',    # 어시스트
    'playerDeaths',       # 사망
    'teamKill',           # 팀 전체 킬 (TK)
    'monsterKill',        # 야생동물 처치 수
    'damageToPlayer',     # 적에게 가한 피해량 
    'damageFromPlayer',   # 적으로부터 받은 피해량 

    # 4. 시야 지표
    'viewContribution',       # 시야 기여도 점수
    'useSecurityConsole',     # CCTV 작동 횟수
    'addTelephotoCamera',     # 망원 카메라 설치 횟수
    'removeTelephotoCamera',  # 망원 카메라 파괴 횟수
    'useReconDrone',          # 정찰 드론 사용 횟수
    'useEmpDrone',            # EMP 드론 사용 횟수

    # 5. 운영 및 특수 지표
    'totalGainVFCredit',  # 총 획득 크레딧 
    'teamRecover',        # 아군 치유량 
    'clutchCount',        # 클러치 횟수 
    'terminateCount'      # 터미네이트 횟수 
]

async def get_ranker_latest_game_id(client: httpx.AsyncClient, ranker: dict, semaphore: asyncio.Semaphore):
    async with semaphore:
        try:
            nick_res = await client.get("/v1/user/nickname", params={"query": ranker['nickname']})
            if nick_res.status_code != 200: return None
            data = nick_res.json()
            uid = data.get('user', {}).get('userId')
            if not uid: return None

            games_res = await client.get(f"/v1/user/games/uid/{uid}")
            if games_res.status_code != 200: return None
            user_games = games_res.json().get("userGames", [])
            if user_games: return user_games[0]['gameId']
        except: pass
    return None

async def get_start_id(client: httpx.AsyncClient):
    print(f"⚓ [{TARGET_SERVER_NAME}] Top 30 랭커의 최신 게임을 전수 조사합니다...")
    try:
        rank_res = await client.get(f"/v1/rank/top/{TARGET_SEASON_ID}/{TARGET_TEAM_MODE}/10")
        if rank_res.status_code != 200: 
            print(f"❌ 랭커 목록 조회 실패: {rank_res.status_code}")
            return None
        
        target_rankers = rank_res.json().get("topRanks", [])[:30] 
        sem = asyncio.Semaphore(10)
        tasks = [get_ranker_latest_game_id(client, ranker, sem) for ranker in target_rankers]
        results = await asyncio.gather(*tasks)
        valid_ids = [gid for gid in results if gid is not None]
        
        if not valid_ids:
            print("❌ 유효한 시작점을 하나도 찾지 못했습니다.")
            return None
            
        max_id = max(valid_ids)
        print(f"✅ 최신 시작점 확보 완료: {max_id}")
        return max_id
    except Exception as e:
        print(f"⚠️ 시작점 탐색 중 에러: {e}")
    return None

async def fetch_game(client: httpx.AsyncClient, game_id: int, semaphore: asyncio.Semaphore):
    async with semaphore:
        try:
            res = await client.get(f"/v1/games/{game_id}")
            if res.status_code == 200:
                data = res.json()
                if data.get('code') == 200: return ('OK', data)
                elif data.get('code') == 404: return ('404', None)
            elif res.status_code == 429:
                await asyncio.sleep(1)
                return ('429', None)
        except: pass
        return ('ERR', None)

async def main():
    if not API_KEY or not MONGO_URI:
        print("❌ API KEY 또는 MONGO URI 없음")
        return
        
    mongo_client = MongoClient(MONGO_URI)
    db = mongo_client[DB_NAME]
    collection = db[COLLECTION_NAME]
    
    # [추가] 7일 제한 날짜 계산
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=DAYS_LIMIT)
    print(f"📅 데이터 수집 제한일: {cutoff_date.strftime('%Y-%m-%d')} (이전 데이터는 수집 중단)")
    
    headers = {"x-api-key": API_KEY, "accept": "application/json"}
    
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=15.0) as client:
        current_id = await get_start_id(client)
        if not current_id: return
        
        semaphore = asyncio.Semaphore(RATE_LIMIT)
        print(f"\n🚀 스캔 시작! {current_id}번부터 역순으로 {SCAN_LIMIT}개 탐색")
        print(f"📦 청크 단위({CHUNK_SIZE}개)로 DB에 순차 저장합니다.")
        print("=" * 60)

        stop_collecting = False # [추가] 중단 플래그

        for start_offset in range(0, SCAN_LIMIT, CHUNK_SIZE):
            if stop_collecting: # [추가] 중단 체크
                print("🛑 7일 이전 데이터 도달! 전체 수집을 안전하게 종료합니다.")
                break

            chunk_collected = []
            chunk_ids = range(current_id - start_offset, current_id - start_offset - CHUNK_SIZE, -1)
            
            tasks = [fetch_game(client, gid, semaphore) for gid in chunk_ids]
            results = await asyncio.gather(*tasks)
            
            for status, data in results:
                if status != 'OK' or not data or "userGames" not in data:
                    continue
                
                meta = data['userGames'][0]
                
                # [추가] 날짜 확인 로직 (7일 컷)
                try:
                    if meta.get('startDtm'):
                        game_dtm = parser.parse(meta['startDtm'])
                        if game_dtm < cutoff_date:
                            stop_collecting = True 
                            continue 
                except: pass

                # 4가지 핵심 필터링 조건
                is_target = (
                    meta.get('serverName') == TARGET_SERVER_NAME and
                    meta.get('seasonId') == TARGET_SEASON_ID and 
                    meta.get('matchingMode') == TARGET_MATCHING_MODE and 
                    meta.get('matchingTeamMode') == TARGET_TEAM_MODE
                )

                if not is_target:
                    continue

                processed_game = []
                for p in data['userGames']:
                    filtered = {k: p.get(k) for k in REQUIRED_FIELDS if k in p}
                    
                    # [수정] startDtm을 문자열 -> Date 객체로 확실히 변환
                    if 'startDtm' in filtered:
                        try: 
                            if isinstance(filtered['startDtm'], str):
                                filtered['startDtm'] = parser.parse(filtered['startDtm'])
                        except: pass
                    
                    processed_game.append(filtered)
                
                chunk_collected.append(
                    {
                        "_id": meta['gameId'], 
                        "gameData": {"userGames": processed_game}
                    }
                )

            if chunk_collected:
                for game_doc in chunk_collected:
                    collection.update_one(
                        {"userGames.0.gameId": game_doc["_id"]},
                        {"$set": game_doc["gameData"]}, 
                        upsert=True
                    )
                print(f"📦 ID {chunk_ids[0]}~{chunk_ids[-1]} 구간: {len(chunk_collected)}건 저장 완료.")
            else:
                print(f"📦 ID {chunk_ids[0]}~{chunk_ids[-1]} 구간: 조건 맞는 데이터 없음.")

            await asyncio.sleep(0.3)

    mongo_client.close()
    print("\n🏁 모든 데이터 수집 및 저장 완료.")

    sys.exit(0)

if __name__ == "__main__":
    asyncio.run(main())