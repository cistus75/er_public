import asyncio
import logging
import time
from collections import Counter
from statistics import mean

import httpx

from ..common.utils import get_character_role, calculate_stat_grades, calculate_cobalt_stat_grades, get_character_name

logger = logging.getLogger(__name__)


class GameStatsAnalyzer:
    def __init__(self, userId, client: httpx.AsyncClient, season_id: int):
        self.ranked_matches = []
        self.normal_matches = []
        self.cobalt_matches = []
        self.userId = userId
        self.client = client
        self.season_id = season_id
        self.retry_count = 0  # 429 등 재시도 횟수 추적

    async def get_user_games_page(self, next_param=None):
        """사용자의 특정 페이지 게임 목록을 비동기로 가져옵니다."""
        url = f"/v1/user/games/uid/{self.userId}"
        params = {"next": next_param} if next_param else {}

        retries = 5
        for i in range(retries):
            try:
                response = await self.client.get(url, params=params)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:
                    self.retry_count += 1 # 재시도 카운트 증가
                    wait_time = (2 ** i) * 0.5
                    logger.warning(
                        "API 호출 제한(429) 발생. %.2f초 후 재시도 (시도 %d/%d) | userId=%s",
                        wait_time,
                        i + 1,
                        retries,
                        self.userId,
                    )
                    await asyncio.sleep(wait_time)
                else:
                    logger.error(
                        "HTTP 오류 발생 | status=%d | userId=%s",
                        e.response.status_code,
                        self.userId,
                    )
                    raise
            except httpx.RequestError:
                logger.exception("API 요청 실패 | userId=%s", self.userId)
                raise

        logger.error(
            "재시도 횟수(%d) 초과. 게임 목록 조회를 중단합니다. | userId=%s",
            retries,
            self.userId,
        )
        return None

    async def collect_match_data(self, max_games_per_mode: int = 20):
        """
        지정 시즌의 랭크/일반/코발트 게임 데이터를 모드별로 최대 N개 수집합니다.
        수집은 최대 20초 또는 7페이지 이내로 제한합니다.
        """
        logger.info(
            "매치 데이터 수집 시작 | userId=%s | season=%d | 모드별 최대 %d게임",
            self.userId,
            self.season_id,
            max_games_per_mode,
        )

        max_time_sec = 20
        ranked_games: list = []
        normal_games: list = []
        cobalt_games: list = []
        next_param = None
        found_modes: set = set()
        start_time = time.time()

        for page in range(3):
            # 모든 모드 목표 달성 시 조기 종료
            if (
                len(ranked_games) >= max_games_per_mode
                and len(normal_games) >= max_games_per_mode
                and len(cobalt_games) >= max_games_per_mode
            ):
                logger.debug("모든 모드 목표 게임 수 달성. 수집 조기 종료.")
                break

            elapsed = time.time() - start_time
            if elapsed > max_time_sec:
                logger.warning(
                    "매치 수집 시간 제한(%ds) 초과로 중단 | page=%d | userId=%s",
                    max_time_sec,
                    page,
                    self.userId,
                )
                break

            data = await self.get_user_games_page(next_param)

            if not data or not data.get("userGames"):
                logger.debug("게임 목록 응답 없음. 수집 종료 | page=%d", page)
                break

            games_page = data.get("userGames", [])
            next_param = data.get("next")

            for game in games_page:
                season_id = game.get("seasonId")
                matching_mode = game.get("matchingMode")
                found_modes.add(matching_mode)

                if matching_mode == 2 and len(normal_games) < max_games_per_mode:
                    normal_games.append(game)
                elif (
                    season_id == self.season_id
                    and matching_mode == 3
                    and len(ranked_games) < max_games_per_mode
                ):
                    ranked_games.append(game)
                elif matching_mode == 6 and len(cobalt_games) < max_games_per_mode:
                    cobalt_games.append(game)

            if not next_param:
                break

        self.ranked_matches = ranked_games
        self.normal_matches = normal_games
        self.cobalt_matches = cobalt_games

        logger.info(
            "매치 데이터 수집 완료 | userId=%s | 랭크=%d | 일반=%d | 코발트=%d | 발견 모드=%s",
            self.userId,
            len(self.ranked_matches),
            len(self.normal_matches),
            len(self.cobalt_matches),
            found_modes,
        )

        if not self.normal_matches and 2 not in found_modes:
            logger.info(
                "일반 게임 없음: API 응답 내 해당 시즌 일반 게임 기록 미존재 | userId=%s",
                self.userId,
            )

    # ------------------------------------------------------------------
    # Private 통계 계산 메서드
    # ------------------------------------------------------------------

    def _calculate_kda(self, matches: list) -> dict:
        if not matches:
            return {"kda": 0.0, "avg_kills": 0.0, "avg_assists": 0.0, "avg_deaths": 0.0}

        total_kills = sum(m.get("playerKill", 0) for m in matches)
        total_assists = sum(m.get("playerAssistant", 0) for m in matches)
        total_deaths = sum(m.get("playerDeaths", 0) for m in matches)
        num_games = len(matches)

        kda_value = (
            (total_kills + total_assists) / total_deaths
            if total_deaths > 0
            else float(total_kills + total_assists)
        )
        return {
            "kda": round(kda_value, 2),
            "avg_kills": round(total_kills / num_games, 1),
            "avg_assists": round(total_assists / num_games, 1),
            "avg_deaths": round(total_deaths / num_games, 1),
        }

    def get_account_level(self) -> int:
        if self.ranked_matches:
            return self.ranked_matches[0].get("accountLevel", 0)
        if self.normal_matches:
            return self.normal_matches[0].get("accountLevel", 0)
        return 0

    def _calculate_average_rank(self, matches: list) -> float:
        if not matches:
            return 0.0
        ranks = [m.get("gameRank", 0) for m in matches if m.get("gameRank", 0) > 0]
        return round(mean(ranks), 1) if ranks else 0.0

    def _calculate_win_rate(self, matches: list) -> float:
        if not matches:
            return 0.0
        wins = sum(1 for m in matches if m.get("gameRank", 0) == 1)
        return round((wins / len(matches)) * 100, 1)

    def _calculate_cobalt_win_rate(self, matches: list) -> float:
        if not matches:
            return 0.0
        wins = sum(1 for m in matches if m.get("victory", 0) == 1)
        return round((wins / len(matches)) * 100, 1)

    def _calculate_top3_rate(self, matches: list) -> float:
        if not matches:
            return 0.0
        top3 = sum(1 for m in matches if 1 <= m.get("gameRank", 0) <= 3)
        return round((top3 / len(matches)) * 100, 1)

    def _calculate_average_team_kills(self, matches: list) -> float:
        if not matches:
            return 0.0
        return round(mean(m.get("teamKill", 0) for m in matches), 1)

    def _calculate_average_damage_dealt(self, matches: list) -> float:
        if not matches:
            return 0.0
        return round(mean(m.get("damageToPlayer", 0) for m in matches), 2)

    def _calculate_average_damage_received(self, matches: list) -> float:
        if not matches:
            return 0.0
        return round(mean(m.get("damageFromPlayer", 0) for m in matches), 2)

    def _calculate_avg_self_heal(self, matches: list) -> float:
        if not matches:
            return 0.0
        return round(mean(m.get("healAmount", 0) for m in matches), 2)

    def _calculate_avg_team_heal(self, matches: list) -> float:
        if not matches:
            return 0.0
        return round(mean(m.get("teamRecover", 0) for m in matches), 2)

    def _calculate_avg_protect_absorb(self, matches: list) -> float:
        if not matches:
            return 0.0
        return round(mean(m.get("protectAbsorb", 0) for m in matches), 2)

    def _calculate_average_game_time(self, matches: list) -> float:
        if not matches:
            return 0.0
        return round(mean(m.get("playTime", 0) for m in matches) / 60, 2)

    def _calculate_average_monster_kills(self, matches: list) -> float:
        if not matches:
            return 0.0
        return round(mean(m.get("monsterKill", 0) for m in matches), 1)

    def _get_most_used_character_and_usage(self, matches: list) -> tuple:
        if not matches:
            return None, {}
        characters = [m.get("characterNum") for m in matches if m.get("characterNum")]
        if not characters:
            return None, {}
        count = Counter(characters)
        return count.most_common(1)[0][0], dict(count)

    def _analyze_recent_top_3_characters(self, matches: list, mode: str = "ranked") -> list:
        if not matches:
            return []
        characters_played = [m.get("characterNum") for m in matches if m.get("characterNum")]
        if not characters_played:
            return []

        character_counts = Counter(characters_played)
        top_3_char_codes = [code for code, _ in character_counts.most_common(3)]

        top_3_stats = []
        for char_code in top_3_char_codes:
            char_matches = [m for m in matches if m.get("characterNum") == char_code]
            num_games = len(char_matches)
            if num_games == 0:
                continue

            if mode == "cobalt":
                wins = sum(1 for m in char_matches if m.get("victory", 0) == 1)
                top3 = wins # 코발트 모드는 4:4 이므로 승리가 곧 Top 3 진입과 동일하게 처리 (혹은 무의미)
            else:
                wins = sum(1 for m in char_matches if m.get("gameRank", 0) == 1)
                top3 = sum(1 for m in char_matches if 1 <= m.get("gameRank", 0) <= 3)
            total_team_kills = sum(m.get("teamKill", 0) for m in char_matches)
            total_damage = sum(m.get("damageToPlayer", 0) for m in char_matches)

            top_3_stats.append(
                {
                    "characterCode": char_code,
                    "characterName": get_character_name(char_code),
                    "totalGames": num_games,
                    "winRate": round((wins / num_games) * 100, 1),
                    "top3Rate": round((top3 / num_games) * 100, 1),
                    "avgTK": round(total_team_kills / num_games, 1),
                    "avgDamage": round(total_damage / num_games, 2),
                }
            )
        return top_3_stats

    def _cal_phase_kill_death(self, matches: list) -> dict:
        if not matches:
            return {}
        n = len(matches)
        return {
            "p1_kills": sum(m.get("killsPhaseOne", 0) for m in matches) / n,
            "p2_kills": sum(m.get("killsPhaseTwo", 0) for m in matches) / n,
            "p3_kills": sum(m.get("killsPhaseThree", 0) for m in matches) / n,
            "p1_deaths": sum(m.get("deathsPhaseOne", 0) for m in matches) / n,
            "p2_deaths": sum(m.get("deathsPhaseTwo", 0) for m in matches) / n,
            "p3_deaths": sum(m.get("deathsPhaseThree", 0) for m in matches) / n,
        }

    def _cal_vision_score(self, matches: list) -> float:
        if not matches:
            return 0.0
        total = sum(m.get("viewContribution", 0) for m in matches)
        return round(total / len(matches), 2)

    def _cal_avg_clutch(self, matches: list) -> float:
        if not matches:
            return 0.0
        total = sum(m.get("clutchCount", 0) for m in matches)
        return round(total / len(matches), 2)

    def _cal_avg_terminate(self, matches: list) -> float:
        if not matches:
            return 0.0
        total = sum(m.get("terminateCount", 0) for m in matches)
        return round(total / len(matches), 2)

    def _cal_avg_credit_gain(self, matches: list) -> float:
        if not matches:
            return 0.0
        return round(mean(m.get("totalGainVFCredit", 0) for m in matches), 2)

    def _cal_avg_camera_add(self, matches: list) -> float:
        if not matches:
            return 0.0
        return round(mean(m.get("addTelephotoCamera", 0) for m in matches), 1)

    def _cal_avg_camera_remove(self, matches: list) -> float:
        if not matches:
            return 0.0
        return round(mean(m.get("removeTelephotoCamera", 0) for m in matches), 1)

    def _cal_avg_use_cctv(self, matches: list) -> float:
        if not matches:
            return 0.0
        return round(mean(m.get("useSecurityConsole", 0) for m in matches), 1)

    def _cal_avg_recon_drone(self, matches: list) -> float:
        if not matches:
            return 0.0
        return round(mean(m.get("useReconDrone", 0) for m in matches), 1)

    def _cal_avg_emp_drone(self, matches: list) -> float:
        if not matches:
            return 0.0
        return round(mean(m.get("useEmpDrone", 0) for m in matches), 1)

    # ------------------------------------------------------------------
    # Public 통계 조회 메서드
    # ------------------------------------------------------------------

    def get_detailed_stats(self, mode: str = "ranked") -> dict:
        """
        지정 모드의 집계 통계를 딕셔너리로 반환합니다.

        Args:
            mode: 'ranked' | 'normal' | 'cobalt'

        Returns:
            통계 딕셔너리. 게임 기록이 없으면 {"no_record": True}.
        """
        if mode == "cobalt":
            matches_to_analyze = self.cobalt_matches
            if not matches_to_analyze:
                logger.info("코발트 게임 기록 없음 | userId=%s", self.userId)
                return {"no_record": True}

            kda_stats = self._calculate_kda(matches_to_analyze)
            most_char, char_usage = self._get_most_used_character_and_usage(matches_to_analyze)
            recent_top_3_chars = self._analyze_recent_top_3_characters(matches_to_analyze, mode="cobalt")
            kd_phase = self._cal_phase_kill_death(matches_to_analyze)
            character_role = get_character_role(most_char)

            stat = {
                "userId": self.userId,
                "no_record": False,
                "mode": mode,
                "account_level": self.get_account_level(),
                "total_games_analyzed": len(matches_to_analyze),
                "kda": kda_stats["kda"],
                "average_kills": kda_stats["avg_kills"],
                "average_assists": kda_stats["avg_assists"],
                "average_deaths": kda_stats["avg_deaths"],
                "kd_phase": kd_phase,
                "win_rate_percentage": self._calculate_cobalt_win_rate(matches_to_analyze),
                "average_damage_to_players": self._calculate_average_damage_dealt(matches_to_analyze),
                "avg_damage_from_players": self._calculate_average_damage_received(matches_to_analyze),
                "avg_self_heal": self._calculate_avg_self_heal(matches_to_analyze),
                "avg_team_heal": self._calculate_avg_team_heal(matches_to_analyze),
                "avg_protect_absorb": self._calculate_avg_protect_absorb(matches_to_analyze),
                "average_game_time_minutes": self._calculate_average_game_time(matches_to_analyze),
                "avg_credit_gain": self._cal_avg_credit_gain(matches_to_analyze),
                "avg_camera_add": self._cal_avg_camera_add(matches_to_analyze),
                "avg_camera_remove": self._cal_avg_camera_remove(matches_to_analyze),
                "most_used_character_code": most_char,
                "most_used_character_name": get_character_name(most_char) if most_char else "없음",
                "character_usage_by_code": char_usage,
                "recent_most_3_characters": recent_top_3_chars,
                "character_role": character_role,
            }
            stat["stat_grades"] = calculate_cobalt_stat_grades(stat, character_role)
            return stat

        if mode == "ranked":
            matches_to_analyze = self.ranked_matches
        elif mode == "normal":
            matches_to_analyze = self.normal_matches
        else:
            raise ValueError("mode는 'ranked', 'normal' 또는 'cobalt' 이어야 합니다.")

        if not matches_to_analyze:
            logger.info("%s 게임 기록 없음 | userId=%s", mode, self.userId)
            return {"no_record": True}

        kda_stats = self._calculate_kda(matches_to_analyze)
        most_char, char_usage = self._get_most_used_character_and_usage(matches_to_analyze)
        recent_top_3_chars = self._analyze_recent_top_3_characters(matches_to_analyze, mode=mode)

        win_rate = self._calculate_win_rate(matches_to_analyze)
        avg_rank = self._calculate_average_rank(matches_to_analyze)
        avg_monster = self._calculate_average_monster_kills(matches_to_analyze)
        avg_credit = self._cal_avg_credit_gain(matches_to_analyze)
        avg_vision = self._cal_vision_score(matches_to_analyze)
        avg_camera = self._cal_avg_camera_add(matches_to_analyze)

        rank_var = (8 - avg_rank) * (1 / 7.0 * 100)
        form_score = (
            (win_rate * 7)
            + rank_var
            + (kda_stats["kda"] * 15)
            + avg_monster
            + (avg_credit / 300)
            + (avg_vision * 1.5)
            + (avg_camera * 10)
        )
        character_role = get_character_role(most_char)

        stat = {
            "userId": self.userId,
            "no_record": False,
            "mode": mode,
            "account_level": self.get_account_level(),
            "total_games_analyzed": len(matches_to_analyze),
            "kda": kda_stats["kda"],
            "average_kills": kda_stats["avg_kills"],
            "average_assists": kda_stats["avg_assists"],
            "average_deaths": kda_stats["avg_deaths"],
            "average_rank": avg_rank,
            "win_rate_percentage": win_rate,
            "top3_rate_percentage": self._calculate_top3_rate(matches_to_analyze),
            "average_team_kills": self._calculate_average_team_kills(matches_to_analyze),
            "average_damage_to_players": self._calculate_average_damage_dealt(matches_to_analyze),
            "avg_damage_from_players": self._calculate_average_damage_received(matches_to_analyze),
            "avg_self_heal": self._calculate_avg_self_heal(matches_to_analyze),
            "avg_team_heal": self._calculate_avg_team_heal(matches_to_analyze),
            "avg_protect_absorb": self._calculate_avg_protect_absorb(matches_to_analyze),
            "average_game_time_minutes": self._calculate_average_game_time(matches_to_analyze),
            "avg_clutch": self._cal_avg_clutch(matches_to_analyze),
            "avg_terminate": self._cal_avg_terminate(matches_to_analyze),
            "avg_credit_gain": avg_credit,
            "avg_camera_add": avg_camera,
            "avg_camera_remove": self._cal_avg_camera_remove(matches_to_analyze),
            "avg_use_cctv": self._cal_avg_use_cctv(matches_to_analyze),
            "avg_recon_drone": self._cal_avg_recon_drone(matches_to_analyze),
            "avg_emp_drone": self._cal_avg_emp_drone(matches_to_analyze),
            "average_monster_kills": avg_monster,
            "most_used_character_code": most_char,
            "most_used_character_name": get_character_name(most_char) if most_char else "없음",
            "character_usage_by_code": char_usage,
            "recent_most_3_characters": recent_top_3_chars,
            "avg_vision_score": avg_vision,
            "form_score": form_score,
            "character_role": character_role,
        }
        stat["stat_grades"] = calculate_stat_grades(stat, character_role)
        return stat
