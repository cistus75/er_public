'use client';

import { useState, useCallback } from 'react';
import styles from "./pageComp.module.css";

import StatTable from "../components/StatTable";
import AIAnalysis from "../components/AIAnalysis";
import MostPlayed from "../components/MostPlayed";

export default function RankPage({ gameType, rankStat, diaRankCharStats, tierStats, rankAi, angpyeongAi, loading }) {
  if (!rankStat) {
    return <div>데이터를 불러오는 중입니다...</div>;
  }

  if (rankStat['no_record']) {
    return <div className={styles.noRecord}>랭크 게임 플레이 데이터가 없습니다.</div>
  }

  const my_rank_data = !rankStat.no_record ? {
    core: [
      { label: '승률', value: `${rankStat['win_rate_percentage']}%` },
      { label: 'Top 3', value: `${rankStat['top3_rate_percentage']}%` },
      { label: '평균 순위', value: `${rankStat['average_rank']}위` },
      { label: '평균 TK', value: rankStat['average_team_kills'] },
      { label: '평균 딜량', value: rankStat['average_damage_to_players'] },
      { label: '평균 KDA', value: rankStat['kda'] },
      { label: '폼 점수', value: Math.round(rankStat['form_score']*100)/100}
    ],
    combat: [
      { label: '평균 처치', value: rankStat['average_kills'] },
      { label: '평균 사망', value: rankStat['average_deaths'] },
      { label: '평균 어시스트', value: rankStat['average_assists'] },
      { label: '평균 받은 피해량', value: rankStat['avg_damage_from_players'] },
      { label: '평균 아군 치유량', value: rankStat['avg_team_heal'] },
      { label: '평균 클러치 횟수', value: rankStat['avg_clutch']},
      { label: '평균 터미네이트 횟수', value: rankStat['avg_terminate']}
    ],
    operation: [
      { label: '평균 동물 처치', value: rankStat['average_monster_kills'] },
      { label: '평균 게임 시간', value: `${rankStat['average_game_time_minutes']}분` },
      { label: '평균 크레딧 획득량', value: rankStat['avg_credit_gain']},
      { label: 'DPC', value: "업데이트 예정"}
    ],
    vision: [
      { label: '평균 시야 점수', value: rankStat['avg_vision_score'] },
      { label: '평균 카메라 설치', value: rankStat['avg_camera_add']},
      { label: '평균 카메라 파괴', value: rankStat['avg_camera_remove']},
      { label: '평균 정찰 드론 사용', value: rankStat['avg_recon_drone']},
      { label: '평균 emp 드론 사용', value: rankStat['avg_emp_drone']},
      { label: '평균 cctv 작동', value: rankStat['avg_use_cctv']}
    ]
  } : { core: [], combat: [], operation: [], vision: [] };

  // 1. my_rank_data를 섹션별 Map으로 변환합니다. (빠른 조회를 위함)
  //    (데이터가 없는 경우를 대비해 || []로 안전장치 추가)
  const baseStatsMap = {
    core: new Map(
      my_rank_data.core?.map(item => [item.label, item.value]) || []
    ),
    combat: new Map(
      my_rank_data.combat?.map(item => [item.label, item.value]) || []
    ),
    operation: new Map(
      my_rank_data.operation?.map(item => [item.label, item.value]) || []
    ),
    vision: new Map(
      my_rank_data.vision?.map(item => [item.label, item.value]) || []
    )
  };

  // 2. Map 객체를 받아, { ...item, baseValue }를 반환하는 
  //    매핑 함수를 생성하는 팩토리(Factory) 함수입니다.
  const createBaseValueMapper = (sectionMap) => (item) => {
    // sectionMap (예: baseStatsMap.core)에서 item.label로 값을 찾습니다.
    return { ...item, baseValue: sectionMap.get(item.label) };
  };

  const diaRankStatsData = diaRankCharStats ? {
    core: [
      { label: '승률', value: `${(diaRankCharStats['win_rate'] * 100).toFixed(2)}%` },
      { label: 'Top 3', value: `${(diaRankCharStats['top3_rate'] * 100).toFixed(2)}%` },
      { label: '평균 순위', value: `${diaRankCharStats['average_rank']}위` },
      { label: '평균 TK', value: diaRankCharStats['average_team_kills'] },
      { label: '평균 딜량', value: diaRankCharStats['average_damage_to_players'] },
      { label: '평균 KDA', value: diaRankCharStats['kda'] },
      { label: '\u00A0', value:'\u00A0'}
    ].map(createBaseValueMapper(baseStatsMap.core)),
    combat: [
      { label: '평균 처치', value: diaRankCharStats['average_kills'] },
      { label: '평균 사망', value: diaRankCharStats['average_deaths'] },
      { label: '평균 어시스트', value: diaRankCharStats['average_assists'] },
      { label: '평균 받은 피해량', value: diaRankCharStats['average_damage_taken'] },
      { label: '평균 아군 치유량', value: diaRankCharStats['average_team_heal'] },
      { label: '평균 클러치 횟수', value: diaRankCharStats['avg_clutch']},
      { label: '평균 터미네이트 횟수', value: diaRankCharStats['avg_terminate']}
    ].map(createBaseValueMapper(baseStatsMap.combat)),
    operation: [
      { label: '평균 동물 처치', value: diaRankCharStats['average_monster_kills'] },
      {
        label: '평균 게임 시간', value: diaRankCharStats['average_game_duration_minutes'] ?
          `${diaRankCharStats['average_game_duration_minutes'].toFixed(1)}분` : 'N/A'
      },
      { label: '평균 크레딧 획득량', value: diaRankCharStats['avg_credit_gain']},
      { label: 'DPC', value: "업데이트 예정"}
    ].map(createBaseValueMapper(baseStatsMap.operation)),
    vision:[
      { label: '평균 시야 점수', value: diaRankCharStats['average_vision_score'] },
      { label: '평균 카메라 설치', value: diaRankCharStats['avg_camera_add']},
      { label: '평균 카메라 파괴', value: diaRankCharStats['avg_camera_remove']},
      { label: '평균 정찰 드론 사용', value: diaRankCharStats['avg_recon_drone']},
      { label: '평균 emp 드론 사용', value: diaRankCharStats['avg_emp_drone']},
      { label: '평균 cctv 작동', value: diaRankCharStats['avg_use_cctv']}
    ].map(createBaseValueMapper(baseStatsMap.vision))
  } : { core: [], combat: [], operation: [], vision: [] };

  const tierStatsData = tierStats ? {
    core: [
      { label: '승률', value: `${(tierStats['win_rate'] * 100).toFixed(2)}%` },
      { label: 'Top 3', value: `${(tierStats['top3_rate'] * 100).toFixed(2)}%` },
      { label: '평균 순위', value: `${tierStats['average_rank']}위` },
      { label: '평균 TK', value: tierStats['average_team_kills'] },
      { label: '평균 딜량', value: tierStats['average_damage_to_players'] },
      { label: '평균 KDA', value: tierStats['kda'] },
      { label: '\u00A0', value:'\u00A0'}
    ].map(createBaseValueMapper(baseStatsMap.core)),
    combat: [
      { label: '평균 처치', value: tierStats['average_kills'] },
      { label: '평균 사망', value: tierStats['average_deaths'] },
      { label: '평균 어시스트', value: tierStats['average_assists'] },
      { label: '평균 받은 피해량', value: tierStats['average_damage_taken'] },
      { label: '평균 아군 치유량', value: tierStats['average_team_heal'] },
      { label: '평균 클러치 횟수', value: tierStats['avg_clutch']},
      { label: '평균 터미네이트 횟수', value: tierStats['avg_terminate']}
    ].map(createBaseValueMapper(baseStatsMap.combat)),
    operation: [
      { label: '평균 동물 처치', value: tierStats['average_monster_kills'] },
      {
        label: '평균 게임 시간', value: tierStats['average_game_duration_minutes'] ?
          `${tierStats['average_game_duration_minutes'].toFixed(1)}분` : 'N/A'
      },
      { label: '평균 크레딧 획득량', value: tierStats['avg_credit_gain']},
      { label: 'DPC', value: "업데이트 예정"}
    ].map(createBaseValueMapper(baseStatsMap.operation)),
    vision: [
      { label: '평균 시야 점수', value: tierStats['average_vision_score'] },
      { label: '평균 카메라 설치', value: tierStats['avg_camera_add']},
      { label: '평균 카메라 파괴', value: tierStats['avg_camera_remove']},
      { label: '평균 정찰 드론 사용', value: tierStats['avg_recon_drone']},
      { label: '평균 emp 드론 사용', value: tierStats['avg_emp_drone']},
      { label: '평균 cctv 작동', value: tierStats['avg_use_cctv']}
    ].map(createBaseValueMapper(baseStatsMap.vision))
  } : { core: [], combat: [], operation: [], vision: [] };

  const mostPlayedChars = rankStat.recent_most_3_characters;

  const getAnalysisText = () => {
    switch (gameType) {
      case 'rank':
        return rankAi;
      case 'angpyeong':
        return angpyeongAi;
      default:
        return '';
    }
  };

  const [isDetailedVisible, setIsDetailedVisible] = useState(false);

  const toggleDetailedVisibility = useCallback(() => {
    setIsDetailedVisible(prev => !prev);
  }, []);

  return (
    <>
      <div className={styles['table-section']}>
        <StatTable
          title="내 평균 지표"
          data={my_rank_data}
          tooltipText="최근 랭크 게임 20판의 데이터로 평균 지표를 나타냅니다."
          isDetailedVisible={isDetailedVisible}
          onToggleDetailed={toggleDetailedVisibility}
          btnVisible = {true}
        />

        {/* '랭크' 또는 '앙평'일 때 랭크 관련 테이블 표시 (수정한 부분) */}

        {
          diaRankStatsData ? (
            <StatTable title={"다이아+ " + diaRankCharStats["character_name"] + " 평균 지표"} 
              data={diaRankStatsData}
              tooltipText="최근 랭크 게임에서 가장 많이 사용한 실험체의 다이아 이상 구간에서의 평균 지표를 나타냅니다."
              isDetailedVisible={isDetailedVisible}
              onToggleDetailed={toggleDetailedVisibility} />
          ) : (
            <StatTable title="모스트 다이아+ 평균 지표" 
              data={[{ label: '최근 랭크 게임 기록이 부족합니다.', value: '' }]}
              tooltipText="최근 랭크 게임에서 가장 많이 사용한 실험체의 다이아 이상 구간에서의 평균 지표를 나타냅니다."
              isDetailedVisible={isDetailedVisible}
              onToggleDetailed={toggleDetailedVisibility} />
          )
        }

        {
          tierStatsData ? (
            <StatTable title="티어 평균 지표" 
              data={tierStatsData} 
              tooltipText="나와 동일한 티어의 평균 지표를 나타냅니다. 미스릴 이상은 통합하여 나타냅니다."
              isDetailedVisible={isDetailedVisible}
              onToggleDetailed={toggleDetailedVisibility} />
          ) : (
            <StatTable title="티어 평균 지표" 
              data={[{ label: '랭크 플레이 기록이나 티어 데이터가 부족합니다.', 
              value: '' }]} 
              tooltipText="나와 동일한 티어의 평균 지표를 나타냅니다. 미스릴 이상은 통합하여 나타냅니다."
              isDetailedVisible={isDetailedVisible}
              onToggleDetailed={toggleDetailedVisibility} />
          )
        }
      </div>
      <div className={styles['bottom-section']}>
        <div className={styles['bottom-section-left']}>
          {mostPlayedChars && mostPlayedChars.length > 0 ? (
            <MostPlayed characters={mostPlayedChars} />
          ) : (
            <div className={styles.noDataModule}>
              <p>최근 플레이한 캐릭터 정보가 없습니다.</p>
              <p>랭크 게임을 플레이하면 정보가 표시됩니다.</p>
            </div>
          )}
        </div>
        <div className={styles['bottom-section-right']}>
          {/* AIAnalysis 컴포넌트에 title과 analysis를 조건부로 전달 (수정한 부분) */}
          <AIAnalysis
            title={gameType === 'angpyeong' ? "비앙카의 혈액샘플" : "아디나의 수정구슬"}
            analysis={getAnalysisText()}
            loading={loading}
            ver={gameType === 'angpyeong' ? 'bianca' : 'adina'}
          />
        </div>
      </div>
    </>
  )
}