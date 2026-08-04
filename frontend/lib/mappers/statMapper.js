// 백엔드 필드와 화면 모델 사이의 변환을 한 곳에서 관리합니다.
function toMap(items) {
  return new Map((items ?? []).map((item) => [item.label, item.value]));
}

export function buildBaseStatsMap(viewModel) {
  return {
    core: toMap(viewModel.core),
    combat: toMap(viewModel.combat),
    operation: toMap(viewModel.operation),
    vision: toMap(viewModel.vision),
  };
}

function withBase(sectionMap) {
  return (item) => ({ ...item, baseValue: sectionMap.get(item.label) });
}

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
