/**
 * lib/mappers/statMapper.js
 * 도메인 계층 — 백엔드 API 응답을 StatTable이 소비하는 ViewModel 포맷으로 변환합니다.
 *
 * 이 파일을 두면:
 *  - 백엔드 필드명 변경 시 이 파일만 수정하면 됩니다.
 *  - RankPage / NormalPage의 중복 매핑 로직이 하나로 통합됩니다.
 */

// ─────────────────────────────────────────────
// 유틸리티
// ─────────────────────────────────────────────

/**
 * ViewModel 섹션 배열을 label → value Map으로 변환합니다. (빠른 조회용)
 * @param {Array<{label: string, value: any}>} items
 * @returns {Map<string, any>}
 */
function toMap(items) {
  return new Map((items ?? []).map((item) => [item.label, item.value]));
}

/**
 * ViewModel 전체를 섹션별 Map으로 변환합니다.
 * (비교 테이블에서 내 평균과 비교값을 매핑할 때 사용)
 * @param {{ core: any[], combat: any[], operation: any[], vision: any[] }} viewModel
 * @returns {{ core: Map, combat: Map, operation: Map, vision: Map }}
 */
export function buildBaseStatsMap(viewModel) {
  return {
    core: toMap(viewModel.core),
    combat: toMap(viewModel.combat),
    operation: toMap(viewModel.operation),
    vision: toMap(viewModel.vision),
  };
}

/**
 * baseStatsMap의 특정 섹션으로 baseValue를 주입하는 매퍼 팩토리입니다.
 * @param {Map} sectionMap
 * @returns {(item: object) => object}
 */
function withBase(sectionMap) {
  return (item) => ({ ...item, baseValue: sectionMap.get(item.label) });
}

// ─────────────────────────────────────────────
// 내 평균 지표 매퍼 (랭크 / 일반 공통)
// ─────────────────────────────────────────────

/**
 * 랭크 또는 일반 통계(stat)를 StatTable ViewModel로 변환합니다.
 * 두 모드의 필드 구조가 동일하므로 하나의 함수로 통합됩니다.
 *
 * @param {object} stat  — rank_stat 또는 normal_stat
 * @returns {{ core: any[], combat: any[], operation: any[], vision: any[] }}
 */
export function mapStatToViewModel(stat) {
  return {
    core: [
      { label: '승률',       value: `${stat['win_rate_percentage']}%` },
      { label: 'Top 3',      value: `${stat['top3_rate_percentage']}%` },
      { label: '평균 순위',  value: `${stat['average_rank']}위` },
      { label: '평균 TK',    value: stat['average_team_kills'] },
      { label: '평균 딜량',  value: stat['average_damage_to_players'] },
      { label: '평균 KDA',   value: stat['kda'] },
      { label: '폼 점수',   value: Math.round(stat['form_score'] * 100) / 100 },
    ],
    combat: [
      { label: '평균 처치',          value: stat['average_kills'] },
      { label: '평균 사망',          value: stat['average_deaths'] },
      { label: '평균 어시스트',      value: stat['average_assists'] },
      { label: '평균 받은 피해량',   value: stat['avg_damage_from_players'] },
      { label: '평균 아군 치유량',   value: stat['avg_team_heal'] },
      { label: '평균 클러치 횟수',   value: stat['avg_clutch'] },
      { label: '평균 터미네이트 횟수', value: stat['avg_terminate'] },
    ],
    operation: [
      { label: '평균 동물 처치',   value: stat['average_monster_kills'] },
      { label: '평균 게임 시간',   value: `${stat['average_game_time_minutes']}분` },
      { label: '평균 크레딧 획득량', value: stat['avg_credit_gain'] },
      { label: 'DPC',               value: '업데이트 예정' },
    ],
    vision: [
      { label: '평균 시야 점수',       value: stat['avg_vision_score'] },
      { label: '평균 카메라 설치',     value: stat['avg_camera_add'] },
      { label: '평균 카메라 파괴',     value: stat['avg_camera_remove'] },
      { label: '평균 정찰 드론 사용',  value: stat['avg_recon_drone'] },
      { label: '평균 emp 드론 사용',   value: stat['avg_emp_drone'] },
      { label: '평균 cctv 작동',       value: stat['avg_use_cctv'] },
    ],
  };
}

// ─────────────────────────────────────────────
// 비교 지표 매퍼 (다이아+ 캐릭터 / 티어 평균 공통)
// ─────────────────────────────────────────────

/**
 * 다이아+ 캐릭터 통계 또는 티어 평균 통계를 비교 ViewModel로 변환합니다.
 * baseStatsMap을 주입하면 각 항목에 baseValue가 추가되어 StatTable에서 차이값을 표시합니다.
 *
 * 백엔드 필드 차이 (내 평균 vs 비교 지표):
 *  - 시야 점수: avg_vision_score → average_vision_score
 *  - 게임 시간: average_game_time_minutes → average_game_duration_minutes
 *  - 받은 피해: avg_damage_from_players → average_damage_taken
 *
 * @param {object} charStat   — rank_most_char_dia_stats / normal_most_char_dia_stats / tier_stats
 * @param {object} baseStatsMap — buildBaseStatsMap(myStatViewModel) 결과
 * @returns {{ core: any[], combat: any[], operation: any[], vision: any[] }}
 */
export function mapComparisonStatToViewModel(charStat, baseStatsMap) {
  return {
    core: [
      { label: '승률',       value: `${(charStat['win_rate'] * 100).toFixed(2)}%` },
      { label: 'Top 3',      value: `${(charStat['top3_rate'] * 100).toFixed(2)}%` },
      { label: '평균 순위',  value: `${charStat['average_rank']}위` },
      { label: '평균 TK',    value: charStat['average_team_kills'] },
      { label: '평균 딜량',  value: charStat['average_damage_to_players'] },
      { label: '평균 KDA',   value: charStat['kda'] },
      { label: '\u00A0',     value: '\u00A0' },
    ].map(withBase(baseStatsMap.core)),
    combat: [
      { label: '평균 처치',          value: charStat['average_kills'] },
      { label: '평균 사망',          value: charStat['average_deaths'] },
      { label: '평균 어시스트',      value: charStat['average_assists'] },
      { label: '평균 받은 피해량',   value: charStat['average_damage_taken'] },
      { label: '평균 아군 치유량',   value: charStat['average_team_heal'] },
      { label: '평균 클러치 횟수',   value: charStat['avg_clutch'] },
      { label: '평균 터미네이트 횟수', value: charStat['avg_terminate'] },
    ].map(withBase(baseStatsMap.combat)),
    operation: [
      { label: '평균 동물 처치', value: charStat['average_monster_kills'] },
      {
        label: '평균 게임 시간',
        value: charStat['average_game_duration_minutes']
          ? `${charStat['average_game_duration_minutes'].toFixed(1)}분`
          : 'N/A',
      },
      { label: '평균 크레딧 획득량', value: charStat['avg_credit_gain'] },
      { label: 'DPC',               value: '업데이트 예정' },
    ].map(withBase(baseStatsMap.operation)),
    vision: [
      { label: '평균 시야 점수',       value: charStat['average_vision_score'] },
      { label: '평균 카메라 설치',     value: charStat['avg_camera_add'] },
      { label: '평균 카메라 파괴',     value: charStat['avg_camera_remove'] },
      { label: '평균 정찰 드론 사용',  value: charStat['avg_recon_drone'] },
      { label: '평균 emp 드론 사용',   value: charStat['avg_emp_drone'] },
      { label: '평균 cctv 작동',       value: charStat['avg_use_cctv'] },
    ].map(withBase(baseStatsMap.vision)),
  };
}
