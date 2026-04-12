import os
import sys
from pymongo import MongoClient
from datetime import datetime, timedelta, timezone # [수정] timezone 추가
from dotenv import load_dotenv

# 1. 환경 변수 로드
load_dotenv()

# 2. 경로 설정 (utils 모듈 import용)
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

# 캐릭터 맵 로드 함수
try:
    from utils import load_character_map
except ImportError:
    def load_character_map():
        return {} 

# --- 설정 ---
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "er-user-insight"
MMR_THRESHOLD_FOR_CHAR_STATS = 5000 
DATA_RANGE_DAYS = 7

def main():
    if not MONGO_URI:
        print("❌ 에러: MONGO_URI 환경 변수가 설정되지 않았습니다.")
        return

    client = None
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        
        raw_games_collection = db['raw_games']
        high_mmr_char_stats_collection = db['high_mmr_char_stats']
        tier_overall_stats_collection = db['tier_overall_stats']

        print("✅ MongoDB에 성공적으로 연결되었습니다.")

        character_map = load_character_map()
        
        # [수정 포인트] UTC 타임존을 명시하여 MongoDB 데이터와 포맷 일치시킴
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=DATA_RANGE_DAYS)
        print(f"📅 통계 집계 기준일: {cutoff_date} (이후 데이터만 사용)")

        # [진단용] 실제로 조건에 맞는 데이터가 있는지 먼저 카운트 (디버깅 핵심)
        matched_count = raw_games_collection.count_documents({'userGames.0.startDtm': {'$gte': cutoff_date}})
        print(f"🔍 대상 데이터 수: {matched_count}건")

        if matched_count == 0:
            print("⚠️ 경고: 집계할 최신 데이터가 없습니다. 날짜 형식이 올바른지 확인해주세요.")
            return

        # [기본 파이프라인]
        base_pipeline = [
            # userGames.0.startDtm은 우리가 인덱스를 걸어둔 필드입니다.
            {'$match': {'userGames.0.startDtm': {'$gte': cutoff_date}}},
            {'$unwind': '$userGames'},
        ]
        
        # [티어 계산 단계]
        tier_calculation_stage = {
            '$addFields': {
                'tier': {
                    '$switch': {
                        'branches': [
                            {'case': {'$gte': ['$userGames.mmrBefore', 7100]}, 'then': 'mithril'},
                            {'case': {'$gte': ['$userGames.mmrBefore', 6400]}, 'then': 'meteorite'},
                            {'case': {'$gte': ['$userGames.mmrBefore', 5000]}, 'then': 'diamond'},
                            {'case': {'$gte': ['$userGames.mmrBefore', 3600]}, 'then': 'platinum'},
                            {'case': {'$gte': ['$userGames.mmrBefore', 2400]}, 'then': 'gold'},
                            {'case': {'$gte': ['$userGames.mmrBefore', 1400]}, 'then': 'silver'},
                            {'case': {'$gte': ['$userGames.mmrBefore', 600]}, 'then': 'bronze'}
                        ],
                        'default': 'iron'
                    }
                }
            }
        }

        # --- 공통 그룹화 로직 ---
        common_group_stage = {
            'total_games': {'$sum': 1},
            'total_wins': {'$sum': {'$cond': [{'$eq': ['$userGames.gameRank', 1]}, 1, 0]}},
            'total_top3': {'$sum': {'$cond': [{'$lte': ['$userGames.gameRank', 3]}, 1, 0]}},
            'avg_rank': {'$avg': '$userGames.gameRank'},
            'avg_team_kills': {'$avg': '$userGames.teamKill'},
            'avg_play_time': {'$avg': '$userGames.playTime'},
            'avg_kills': {'$avg': '$userGames.playerKill'},
            'avg_assists': {'$avg': '$userGames.playerAssistant'},
            'avg_deaths': {'$avg': '$userGames.playerDeaths'},
            'avg_damage': {'$avg': '$userGames.damageToPlayer'},
            'avg_damage_taken': {'$avg': '$userGames.damageFromPlayer'},
            'avg_monsters': {'$avg': '$userGames.monsterKill'},
            'avg_team_heal': {'$avg': '$userGames.teamRecover'},
            'avg_vision_score': {'$avg': '$userGames.viewContribution'},
            
            # 신규 지표
            'avg_clutch': {'$avg': '$userGames.clutchCount'},
            'avg_terminate': {'$avg': '$userGames.terminateCount'},
            'avg_credit_gain': {'$avg': '$userGames.totalGainVFCredit'},
            
            # 카메라 & 드론
            'avg_camera_add': {'$avg': '$userGames.addTelephotoCamera'}, 
            'avg_camera_remove': {'$avg': '$userGames.removeTelephotoCamera'},
            'avg_use_cctv': {'$avg': '$userGames.useSecurityConsole'},
            'avg_recon_drone': {'$avg': '$userGames.useReconDrone'},
            'avg_emp_drone': {'$avg': '$userGames.useEmpDrone'}
        }
        
        # --- 공통 데이터 다듬기($project) 로직 ---
        common_project_stage = {
            'win_rate': {'$round': [{'$divide': ['$total_wins', '$total_games']}, 4]},
            'top3_rate': {'$round': [{'$divide': ['$total_top3', '$total_games']}, 4]},
            'average_rank': {'$round': ['$avg_rank', 2]},
            'average_team_kills': {'$round': ['$avg_team_kills', 2]},
            'average_game_duration_minutes': {'$round': [{'$divide': ['$avg_play_time', 60]}, 1]},
            'kda': {
                '$round': [
                    {'$divide': [
                        {'$add': ['$avg_kills', '$avg_assists']}, 
                        {'$max': ['$avg_deaths', 1]}
                    ]}, 
                    2
                ]
            },
            'average_kills': {'$round': ['$avg_kills', 2]},
            'average_deaths': {'$round': ['$avg_deaths', 2]},
            'average_assists': {'$round': ['$avg_assists', 2]},
            'average_damage_to_players': {'$round': ['$avg_damage', 0]},
            'average_damage_taken': {'$round': ['$avg_damage_taken', 0]},
            'average_monster_kills': {'$round': ['$avg_monsters', 1]},
            'average_team_heal': {'$round': ['$avg_team_heal', 0]},
            
            'average_vision_score': {'$round': ['$avg_vision_score', 1]},
            'avg_clutch': {'$round': ['$avg_clutch', 1]},
            'avg_terminate': {'$round': ['$avg_terminate', 1]},
            'avg_credit_gain': {'$round': ['$avg_credit_gain', 0]},
            'avg_camera_add': {'$round': ['$avg_camera_add', 1]},
            'avg_camera_remove': {'$round': ['$avg_camera_remove', 1]},
            'avg_use_cctv': {'$round': ['$avg_use_cctv', 1]},
            'avg_recon_drone': {'$round': ['$avg_recon_drone', 1]},
            'avg_emp_drone': {'$round': ['$avg_emp_drone', 1]}
        }

        # --- 3. [1/2] 상위 MMR 캐릭터별 통계 ---
        print(f"\n[1/2] {MMR_THRESHOLD_FOR_CHAR_STATS} MMR 이상 캐릭터별 통계 계산 중...")
        
        high_mmr_char_pipeline = base_pipeline + [
            {'$match': {'userGames.mmrBefore': {'$gte': MMR_THRESHOLD_FOR_CHAR_STATS}}},
            {'$group': {
                **common_group_stage,
                '_id': '$userGames.characterNum'
            }},
            {'$project': {
                **common_project_stage,
                '_id': 0,
                'character_code': '$_id',
                'character_name': {'$literal': "Unknown"},
                'tier_group': {'$literal': f"MMR {MMR_THRESHOLD_FOR_CHAR_STATS}+"},
                'total_games_for_pick_rate': '$total_games'
            }}
        ]
        
        high_mmr_char_results = list(raw_games_collection.aggregate(high_mmr_char_pipeline))
        
        if high_mmr_char_results:
            total_games_in_pool = sum(stat['total_games_for_pick_rate'] for stat in high_mmr_char_results)
            
            for stat in high_mmr_char_results:
                char_code = str(stat['character_code'])
                stat['character_name'] = character_map.get(char_code, f"Char-{char_code}")
                stat['pick_rate'] = round(stat['total_games_for_pick_rate'] / total_games_in_pool, 4) if total_games_in_pool > 0 else 0
                del stat['total_games_for_pick_rate']

            high_mmr_char_stats_collection.delete_many({})
            high_mmr_char_stats_collection.insert_many(high_mmr_char_results)
            print(f"✅ 캐릭터별 통계 {len(high_mmr_char_results)}개 저장 완료.")
        else:
            print(f"ℹ️ 해당 기간/MMR 구간의 데이터가 없어 캐릭터 통계를 생성하지 않았습니다.")

        # --- 4. [2/2] 티어별 종합 통계 ---
        print("\n[2/2] 티어별 종합 통계 계산 중...")
        
        tier_overall_pipeline = base_pipeline + [
            tier_calculation_stage,
            {'$group': {
                **common_group_stage,
                '_id': '$tier'
            }},
            {'$project': {
                **common_project_stage,
                '_id': 0, 
                'tier': '$_id'
            }}
        ]
        
        tier_overall_results = list(raw_games_collection.aggregate(tier_overall_pipeline))
        
        if tier_overall_results:
            tier_overall_stats_collection.delete_many({})
            tier_overall_stats_collection.insert_many(tier_overall_results)
            print(f"✅ 티어별 종합 통계 {len(tier_overall_results)}개 저장 완료.")
        else:
            print("ℹ️ 티어별 통계를 생성할 데이터가 없습니다.")

    except Exception as e:
        print(f"❌ 스크립트 실행 중 오류 발생: {e}")
    finally:
        if client:
            client.close()
            print("\nMongoDB 연결 종료.")

if __name__ == "__main__":
    main()