import os
import asyncio
from collections import Counter
from statistics import mean
from dotenv import load_dotenv

import httpx
import time

# --- 환경 변수 로드 ---
load_dotenv()
API_KEY = os.getenv("OPEN_API_KEY")
if not API_KEY:
    raise ValueError("OPEN_API_KEY가 .env 파일에 설정되어 있지 않습니다.")

class GameStatsAnalyzer:
    def __init__(self, userId, client: httpx.AsyncClient, season_id: int):
        self.ranked_matches = [] # 랭크 게임 데이터 저장커위커커위커위커
        self.normal_matches = [] # 일반 게임 데이터 저장커위커
        self.userId = userId
        self.client = client
        self.season_id = season_id

    async def get_user_games_page(self, next_param=None):
        """사용자의 특정 페이지 게임 목록을 비동기로 가져옵니다."""
        url = f"/v1/user/games/uid/{self.userId}"
        params = {'next': next_param} if next_param else {}
        
        retries = 5
        for i in range(retries):
            try:
                response = await self.client.get(url, params=params)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:
                    wait_time = (2 ** i) * 0.5
                    print(f"❌ API 호출 제한(429) 발생! {wait_time:.2f}초 후 재시도...")
                    await asyncio.sleep(wait_time)
                else:
                    print(f"❌ HTTP 에러 발생: {e}")
                    raise
            except httpx.RequestError as e:
                print(f"❌ API 요청 실패: {e}")
                raise
        
        print("❌ 재시도 횟수 초과. API 요청을 중단합니다.")
        return None

    async def collect_match_data(self, max_games_per_mode=20):
        """
        사용자의 '지정된 시즌'의 랭크/일반 게임 데이터를 목표 개수만큼 동시에 수집합니다.
        """
        print(f"시즌 {self.season_id}의 최근 랭크/일반 게임 수집 시작 (모드별 최대 {max_games_per_mode}개)...")
        
        max_time_sec_to_collect = 20

        ranked_games = []
        normal_games = []
        cobalt_games = []
        next_param = None
        
        # --- ✨ 변경점 1: 진단을 위해 발견된 게임 모드를 기록할 집합(set) 추가 ---
        found_modes = set()

        start_time = time.time()

        for _ in range(7): 
            if len(ranked_games) >= max_games_per_mode and len(normal_games) >= max_games_per_mode and len(cobalt_games) >= max_games_per_mode:
                break
            
            elapsed_time = time.time() - start_time
            if elapsed_time > max_time_sec_to_collect:
                print(f'===== 매치 수집 시작 후 {max_time_sec_to_collect}초 경과로 중단')
                break

            data = await self.get_user_games_page(next_param)
            
            if not data or not data.get('userGames'):
                break 

            games_page = data.get('userGames', [])
            next_param = data.get('next')
            
            for game in games_page:
                season_id = game.get("seasonId")
                
                matching_mode = game.get("matchingMode")
                # print(f"game.get('matchingMode') : {game.get("matchingMode")}, matching_mode = {matching_mode}")
                found_modes.add(matching_mode) # 발견된 모드를 기록
                
                if matching_mode == 2 and len(normal_games) < max_games_per_mode:
                    normal_games.append(game)
                
                elif season_id == self.season_id and matching_mode == 3 and len(ranked_games) < max_games_per_mode:
                    ranked_games.append(game)

                elif matching_mode == 6 and len(cobalt_games) < max_games_per_mode:
                    cobalt_games.append(game)

            if not next_param:
                break

        self.ranked_matches = ranked_games
        self.normal_matches = normal_games
        self.cobalt_matches = cobalt_games

        print(f"✅ 수집 완료: 시즌 {self.season_id} 랭크 {len(self.ranked_matches)}개, 일반 {len(self.normal_matches)}개")
        
        # --- ✨ 변경점 2: 수집 과정에서 발견된 모든 게임 모드를 출력 ---
        print(f"ℹ️ API 응답에서 발견된 게임 모드: {found_modes} (2: 일반, 3: 랭크, 6: 코발트)")

        # --- ✨ 변경점 3: 일반 게임이 수집되지 않았을 경우, 원인에 대한 안내 메시지 출력 ---
        if not self.normal_matches and 2 not in found_modes:
            print("⚠️ 일반 게임이 수집되지 않았습니다. API가 반환한 최근 게임 내에 해당 시즌의 일반 게임 기록이 없는 것으로 보입니다.")


    def _calculate_kda(self, matches):
        if not matches: return {'kda': 0.0, 'avg_kills': 0.0, 'avg_assists': 0.0, 'avg_deaths': 0.0}
        total_kills = sum(m.get("playerKill", 0) for m in matches)
        total_assists = sum(m.get("playerAssistant", 0) for m in matches)
        total_deaths = sum(m.get("playerDeaths", 0) for m in matches)
        
        num_games = len(matches)
        if num_games == 0: return {'kda': 0.0, 'avg_kills': 0.0, 'avg_assists': 0.0, 'avg_deaths': 0.0}
        kda_value = (total_kills + total_assists) / total_deaths if total_deaths > 0 else float(total_kills + total_assists)

        return {
            'kda': round(kda_value, 2),
            'avg_kills': round(total_kills / num_games, 1),
            'avg_assists': round(total_assists / num_games, 1),
            'avg_deaths': round(total_deaths / num_games, 1)
        }

    def get_account_level(self):
        if self.ranked_matches:
            return self.ranked_matches[0].get("accountLevel", 0)
        if self.normal_matches:
            return self.normal_matches[0].get("accountLevel", 0)
        return 0

    def _calculate_average_rank(self, matches):
        if not matches: return 0.0
        ranks = [m.get("gameRank", 0) for m in matches if m.get("gameRank", 0) > 0]
        return round(mean(ranks), 1) if ranks else 0.0
    
    def _calculate_win_rate(self, matches):
        if not matches: return 0.0
        wins = sum(1 for m in matches if m.get("gameRank", 0) == 1)
        return round((wins / len(matches)) * 100, 1) if matches else 0.0
    
    def _calculate_cobalt_win_rate(self, matches):
        if not matches : return 0.0
        wins = sum(1 for m in matches if m.get("victory", 1) == 1)
        return round((wins / len(matches)) * 100, 1) if matches else 0.0

    def _calculate_top3_rate(self, matches):
        if not matches: return 0.0
        top3 = sum(1 for m in matches if 1 <= m.get("gameRank", 0) <= 3)
        return round((top3 / len(matches)) * 100, 1) if matches else 0.0

    def _calculate_average_team_kills(self, matches):
        if not matches: return 0.0
        team_kills = [m.get("teamKill", 0) for m in matches]
        return round(mean(team_kills), 1) if team_kills else 0.0

    def _calculate_average_damage_dealt(self, matches):
        if not matches: return 0
        damages = [m.get("damageToPlayer", 0) for m in matches]
        return round(mean(damages), 2) if damages else 0
    
    def _calculate_average_damage_received(self, matches):
        if not matches : return 0
        damages = [m.get("damageFromPlayer", 0) for m in matches]
        return round(mean(damages), 2) if damages else 0
    
    def _calculate_avg_self_heal(self, matches):
        if not matches : return 0
        heal = [m.get("healAmount", 0) for m in matches]
        return round(mean(heal), 2) if heal else 0

    def _calculate_avg_team_heal(self, matches):
        if not matches : return 0
        heal = [m.get("teamRecover", 0) for m in matches]
        return round(mean(heal), 2) if heal else 0
    
    def _calculate_avg_protect_absorb(self, matches):
        if not matches : return 0
        heal = [m.get("protectAbsorb", 0) for m in matches]
        return round(mean(heal), 2) if heal else 0
    
    def _calculate_average_game_time(self, matches):
        if not matches: return 0.0
        play_times = [m.get("playTime", 0) for m in matches]
        return round(mean(play_times) / 60, 2) if play_times else 0.0

    def _calculate_average_monster_kills(self, matches):
        if not matches: return 0.0
        monster_kills = [m.get("monsterKill", 0) for m in matches]
        return round(mean(monster_kills), 1) if monster_kills else 0.0

    def _get_most_used_character_and_usage(self, matches):
        if not matches: return None, {}
        characters = [m.get("characterNum", 0) for m in matches if m.get("characterNum")]
        if not characters: return None, {}
        count = Counter(characters)
        return count.most_common(1)[0][0], dict(count)

    def _analyze_recent_top_3_characters(self, matches):
        if not matches: return []
        characters_played = [m.get("characterNum") for m in matches if m.get("characterNum")]
        if not characters_played: return []
        
        character_counts = Counter(characters_played)
        top_3_char_codes = [char_code for char_code, count in character_counts.most_common(3)]

        top_3_stats = []
        for char_code in top_3_char_codes:
            char_matches = [m for m in matches if m.get("characterNum", 0) == char_code]
            num_games = len(char_matches)
            if num_games == 0: continue

            wins = sum(1 for m in char_matches if m.get("gameRank", 0) == 1)
            top3 = sum(1 for m in char_matches if 1 <= m.get("gameRank", 0) <= 3)
            total_team_kills = sum(m.get("teamKill", 0) for m in char_matches)
            total_damage = sum(m.get("damageToPlayer", 0) for m in char_matches)

            char_stat = {
                "characterCode": char_code,
                "totalGames": num_games,
                "winRate": round((wins / num_games) * 100, 1),
                "top3Rate": round((top3 / num_games) * 100, 1),
                "avgTK": round(total_team_kills / num_games, 1),
                "avgDamage": round(total_damage / num_games, 2)
            }
            top_3_stats.append(char_stat)
        return top_3_stats
    
    def _cal_phase_kill_death(self, matches):
        if not matches: return {}
        kd_phase = {
            "p1_kills" : sum((m['killsPhaseOne'] for m in matches))/len(matches),
            "p2_kills" : sum((m['killsPhaseTwo'] for m in matches))/len(matches),
            "p3_kills" : sum((m['killsPhaseThree'] for m in matches))/len(matches),
            "p1_deaths" : sum((m['deathsPhaseOne'] for m in matches))/len(matches),
            "p2_deaths" : sum((m['deathsPhaseTwo'] for m in matches))/len(matches),
            "p3_deaths" : sum((m['deathsPhaseThree'] for m in matches))/len(matches)
            }
        return kd_phase
    
    def _cal_vision_score(self,matches):
        if not matches: return 0
        total = sum(m.get("viewContribution", 0) for m in matches)
        return round((float(total)/len(matches)), 2)    
    def _cal_avg_clutch(self, matches):
        if not matches: return 0
        total = sum(m.get("clutchCount", 0) for m in matches)
        print(f"clutch total : {total}")
        return round((float(total)/len(matches)), 2)
    
    def _cal_avg_terminate(self, matches):
        if not matches: return 0
        total = sum(m.get("terminateCount", 0) for m in matches)
        print(f"terminate total : {total}")
        return round((float(total)/len(matches)), 2)
    
    def _cal_avg_credit_gain(self, matches):
        if not matches: return 0
        total = sum(m.get("totalGainVFCredit", 0) for m in matches)
        return round((float(total) / len(matches)), 2)

    def _cal_avg_camera_add(self, matches):
        if not matches: return 0
        total = sum(m.get("addTelephotoCamera", 0) for m in matches)
        return round((float(total) / len(matches)), 1)
    
    def _cal_avg_camera_remove(self, matches):
        if not matches: return 0
        total = sum(m.get("removeTelephotoCamera", 0) for m in matches)
        return round((float(total) / len(matches)), 1)
    
    def _cal_avg_use_cctv(self, matches):
        if not matches: return 0
        total = sum(m.get("useSecurityConsole", 0) for m in matches)
        return round((float(total) / len(matches)), 1)
    
    def _cal_avg_recon_drone(self, matches):
        if not matches: return 0.0
        total = [m.get("useReconDrone", 0) for m in matches]
        return round(mean(total), 1) if total else 0.0
    
    def _cal_avg_emp_drone(self, matches):
        if not matches: return 0.0
        total = [m.get("useEmpDrone", 0) for m in matches]
        return round(mean(total), 1) if total else 0.0
    
    def get_detailed_stats(self, mode='ranked'):
        if mode == 'cobalt':
            matches_to_analyze = self.cobalt_matches
            if not matches_to_analyze:
                print('no cobalt matches')
                return {"no_record" : True}
            kda_stats = self._calculate_kda(matches_to_analyze)
            most_char, char_usage = self._get_most_used_character_and_usage(matches_to_analyze)
            recent_top_3_chars = self._analyze_recent_top_3_characters(matches_to_analyze)
            kd__phase = self._cal_phase_kill_death(matches_to_analyze)
            return {
                "userId": self.userId,
                "no_record" : False,
                "mode": mode,
                "account_level": self.get_account_level(),
                "total_games_analyzed": len(matches_to_analyze),
                "kda": kda_stats['kda'],
                'average_kills': kda_stats['avg_kills'],
                'average_assists': kda_stats['avg_assists'],
                'average_deaths': kda_stats['avg_deaths'],
                "kd_phase" : kd__phase,
                "win_rate_percentage": self._calculate_cobalt_win_rate(matches_to_analyze),
                "average_damage_to_players": self._calculate_average_damage_dealt(matches_to_analyze),
                "avg_damage_from_players" : self._calculate_average_damage_received(matches_to_analyze),
                "avg_self_heal" : self._calculate_avg_self_heal(matches_to_analyze),
                "avg_team_heal" : self._calculate_avg_team_heal(matches_to_analyze),
                "avg_protect_absorb" : self._calculate_avg_protect_absorb(matches_to_analyze),
                "average_game_time_minutes": self._calculate_average_game_time(matches_to_analyze),
                "avg_credit_gain" : self._cal_avg_credit_gain(matches_to_analyze),
                "avg_camera_add" : self._cal_avg_camera_add(matches_to_analyze),
                "avg_camera_remove" : self._cal_avg_camera_remove(matches_to_analyze),
                "most_used_character_code": most_char,
                "character_usage_by_code": char_usage,
                "recent_most_3_characters": recent_top_3_chars,
            }
        if mode == 'ranked':
            matches_to_analyze = self.ranked_matches
        elif mode == 'normal':
            matches_to_analyze = self.normal_matches
        else:
            raise ValueError("mode는 'ranked', 'normal' 또는 'cobalt' 이어야 합니다.")

        if not matches_to_analyze:
            print('no ',mode,'matches')
            return {"no_record" : True}

        kda_stats = self._calculate_kda(matches_to_analyze)
        most_char, char_usage = self._get_most_used_character_and_usage(matches_to_analyze)
        recent_top_3_chars = self._analyze_recent_top_3_characters(matches_to_analyze)

        win_rate = self._calculate_win_rate(matches_to_analyze)
        avg_rank = self._calculate_average_rank(matches_to_analyze)
        dpc = 1
        avg_monster = self._calculate_average_monster_kills(matches_to_analyze)
        avg_credit = self._cal_avg_credit_gain(matches_to_analyze)
        avg_vision = self._cal_vision_score(matches_to_analyze)
        avg_camera = self._cal_avg_camera_add(matches_to_analyze)

        rank_var = (8-avg_rank) * (1 / 7.0*100)
        

        form_score = (win_rate*7)+rank_var+(kda_stats['kda'] * 15) + (dpc * 1) + (avg_monster * 1) + (avg_credit / 300) + (avg_vision * 1.5) + (avg_camera * 10)

        return {
            "userId": self.userId,
            "no_record" : False,
            "mode": mode,
            "account_level": self.get_account_level(),
            "total_games_analyzed": len(matches_to_analyze),
            "kda": kda_stats['kda'],
            'average_kills': kda_stats['avg_kills'],
            'average_assists': kda_stats['avg_assists'],
            'average_deaths': kda_stats['avg_deaths'],
            "average_rank": avg_rank,
            "win_rate_percentage": win_rate,
            "top3_rate_percentage": self._calculate_top3_rate(matches_to_analyze),
            "average_team_kills": self._calculate_average_team_kills(matches_to_analyze),
            "average_damage_to_players": self._calculate_average_damage_dealt(matches_to_analyze),
            "avg_damage_from_players" : self._calculate_average_damage_received(matches_to_analyze),
            "avg_self_heal" : self._calculate_avg_self_heal(matches_to_analyze),
            "avg_team_heal" : self._calculate_avg_team_heal(matches_to_analyze),
            "avg_protect_absorb" : self._calculate_avg_protect_absorb(matches_to_analyze),
            "average_game_time_minutes": self._calculate_average_game_time(matches_to_analyze),
            "avg_clutch" : self._cal_avg_clutch(matches_to_analyze),
            "avg_terminate" : self._cal_avg_terminate(matches_to_analyze),
            "avg_credit_gain" : avg_credit,
            "avg_camera_add" : avg_camera,
            "avg_camera_remove" : self._cal_avg_camera_remove(matches_to_analyze),
            "avg_use_cctv" : self._cal_avg_use_cctv(matches_to_analyze),
            "avg_recon_drone" : self._cal_avg_recon_drone(matches_to_analyze),
            "avg_emp_drone" : self._cal_avg_emp_drone(matches_to_analyze),
            "average_monster_kills": avg_monster,
            "most_used_character_code": most_char,
            "character_usage_by_code": char_usage,
            "recent_most_3_characters": recent_top_3_chars,
            "avg_vision_score": avg_vision,
            "form_score" : form_score
        }
