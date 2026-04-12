import os
import asyncio
import logging
from datetime import datetime, timedelta, timezone
from dateutil import parser 
from dotenv import load_dotenv
from pymongo import MongoClient, UpdateOne
import httpx
import sys

# Rate Limiting & Retry 적용 라이브러리
from aiolimiter import AsyncLimiter
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type, RetryError

load_dotenv()

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("DataCollector")

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
DAYS_LIMIT = 7  

# ER API Limit: 1초당 50회 제한 (안전하게 45회로 제한)
rate_limiter = AsyncLimiter(45, 1)
# ==========================================

REQUIRED_FIELDS = [
    # 1. 식별 및 게임 환경
    'gameId',             
    'nickname',           
    'seasonId',           
    'serverName',         
    'startDtm',           
    'matchingMode',       
    'matchingTeamMode',   
    'versionSeason',      
    'versionMajor',       

    # 2. 성적 및 캐릭터
    'characterNum',       
    'mmrBefore',          
    'gameRank',           
    'playTime',           

    # 3. 전투 지표
    'playerKill',         
    'playerAssistant',    
    'playerDeaths',       
    'teamKill',           
    'monsterKill',        
    'damageToPlayer',     
    'damageFromPlayer',   

    # 4. 시야 지표
    'viewContribution',       
    'useSecurityConsole',     
    'addTelephotoCamera',     
    'removeTelephotoCamera',  
    'useReconDrone',          
    'useEmpDrone',            

    # 5. 운영 및 특수 지표
    'totalGainVFCredit',  
    'teamRecover',        
    'clutchCount',        
    'terminateCount'      
]

# 재시도 대상이 되는 예외 조건
class RateLimitException(Exception): pass

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=(retry_if_exception_type((httpx.RequestError, RateLimitException))),
    reraise=True
)
async def fetch_with_retry(client: httpx.AsyncClient, url: str, params: dict = None):
    async with rate_limiter:
        response = await client.get(url, params=params)
        if response.status_code == 429:
            logger.warning(f"Rate Limit 429 발생: {url} -> 재시도 예약")
            raise RateLimitException("429 Too Many Requests")
        response.raise_for_status()
        return response

async def get_ranker_latest_game_id(client: httpx.AsyncClient, ranker: dict):
    try:
        nick_res = await fetch_with_retry(client, "/v1/user/nickname", params={"query": ranker['nickname']})
        data = nick_res.json()
        uid = data.get('user', {}).get('userId')
        if not uid: return None

        games_res = await fetch_with_retry(client, f"/v1/user/games/uid/{uid}")
        user_games = games_res.json().get("userGames", [])
        if user_games: 
            return user_games[0]['gameId']
    except Exception as e:
        logger.error(f"랭커({ranker.get('nickname')}) 최신 게임 조회 실패: {e}")
    return None

async def get_start_id(client: httpx.AsyncClient):
    logger.info(f"⚓ [{TARGET_SERVER_NAME}] Top 30 랭커의 최신 게임을 전수 조사합니다...")
    try:
        rank_res = await fetch_with_retry(client, f"/v1/rank/top/{TARGET_SEASON_ID}/{TARGET_TEAM_MODE}/10")
        target_rankers = rank_res.json().get("topRanks", [])[:30] 
        
        tasks = [get_ranker_latest_game_id(client, ranker) for ranker in target_rankers]
        results = await asyncio.gather(*tasks)
        valid_ids = [gid for gid in results if gid is not None]
        
        if not valid_ids:
            logger.error("유효한 시작점을 하나도 찾지 못했습니다.")
            return None
            
        max_id = max(valid_ids)
        logger.info(f"✅ 최신 시작점 확보 완료: {max_id}")
        return max_id
    except Exception as e:
        logger.error(f"시작점 탐색 중 에러 발생: {e}", exc_info=True)
    return None

async def fetch_game(client: httpx.AsyncClient, game_id: int):
    try:
        res = await fetch_with_retry(client, f"/v1/games/{game_id}")
        data = res.json()
        if data.get('code') == 200: 
            return ('OK', data)
        elif data.get('code') == 404: 
            return ('404', None)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return ('404', None)
        logger.error(f"Game {game_id} API HTTP 오류: {e}")
    except Exception as e:
        logger.error(f"Game {game_id} 데이터 수집 중 시스템 오류: {e}")
    return ('ERR', None)

async def main():
    if not API_KEY or not MONGO_URI:
        logger.critical("API KEY 또는 MONGO URI 없음")
        return
        
    mongo_client = MongoClient(MONGO_URI)
    db = mongo_client[DB_NAME]
    collection = db[COLLECTION_NAME]
    
    # 7일 제한 날짜 계산 및 시간대 강제 부여(UTC)
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=DAYS_LIMIT)
    logger.info(f"📅 데이터 수집 제한일: {cutoff_date.strftime('%Y-%m-%d %H:%M:%S')} UTC (이전 데이터는 수집 중단)")
    
    headers = {"x-api-key": API_KEY, "accept": "application/json"}
    
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=15.0) as client:
        current_id = await get_start_id(client)
        if not current_id: return
        
        logger.info(f"\n🚀 스캔 시작! {current_id}번부터 역순으로 {SCAN_LIMIT}개 탐색")
        logger.info(f"📦 청크 단위({CHUNK_SIZE}개)로 DB에 순차 저장합니다 (Bulk Write).")
        logger.info("=" * 60)

        stop_collecting = False

        for start_offset in range(0, SCAN_LIMIT, CHUNK_SIZE):
            if stop_collecting:
                logger.info("🛑 7일 이전 데이터 도달! 전체 수집을 안전하게 종료합니다.")
                break

            chunk_ids = range(current_id - start_offset, current_id - start_offset - CHUNK_SIZE, -1)
            
            tasks = [fetch_game(client, gid) for gid in chunk_ids]
            results = await asyncio.gather(*tasks)
            
            bulk_ops = []
            
            for status, data in results:
                if status != 'OK' or not data or "userGames" not in data:
                    continue
                
                meta = data['userGames'][0]
                
                # 날짜 파싱 및 타임존 일치
                if meta.get('startDtm'):
                    try:
                        game_dtm = parser.parse(meta['startDtm'])
                        if game_dtm.tzinfo is None:
                            game_dtm = game_dtm.replace(tzinfo=timezone.utc)
                        if game_dtm < cutoff_date:
                            stop_collecting = True 
                            continue 
                    except Exception as e:
                        logger.warning(f"날짜 파싱 실패 (게임ID: {meta.get('gameId')}): {e}")

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
                    
                    if 'startDtm' in filtered:
                        try:
                            dt = parser.parse(filtered['startDtm'])
                            if dt.tzinfo is None:
                                dt = dt.replace(tzinfo=timezone.utc)
                            filtered['startDtm'] = dt
                        except: pass
                    
                    processed_game.append(filtered)
                
                # Bulk API를 위한 UpdateOne 생성
                bulk_ops.append(
                    UpdateOne(
                        {"userGames.0.gameId": meta['gameId']},
                        {"$set": {"userGames": processed_game}},
                        upsert=True
                    )
                )

            if bulk_ops:
                try:
                    result = collection.bulk_write(bulk_ops, ordered=False)
                    logger.info(f"📦 ID {chunk_ids[0]}~{chunk_ids[-1]} 구간: {result.upserted_count + result.modified_count}건 반영 완료 (Bulk)")
                except Exception as e:
                    logger.error(f"MongoDB Bulk Write 에러 발생: {e}")
            else:
                logger.info(f"📦 ID {chunk_ids[0]}~{chunk_ids[-1]} 구간: 조건 맞는 데이터 없음.")

    mongo_client.close()
    logger.info("🏁 모든 데이터 수집 및 안전하게 저장 완료.")
    sys.exit(0)

if __name__ == "__main__":
    asyncio.run(main())