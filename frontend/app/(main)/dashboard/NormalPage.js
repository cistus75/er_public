'use client';

import styles from "./pageComp.module.css";

import { useState, useCallback } from 'react';
import StatTable from "../components/StatTable";
import AIAnalysis from "../components/AIAnalysis";
import MostPlayed from "../components/MostPlayed";

export default function NormalPage({ normalStat, diaNormalCharStats, ai, loading }) {
    if(!normalStat){
        return <div>데이터를 불러오는 중입니다...</div>;
    }  
    if(normalStat['no_record']){
        return <div className={styles.noRecord}>일반 게임 플레이 데이터가 없습니다.</div>
    }

    const my_normal_data = !normalStat.no_record ? {
    core: [
      { label: '승률', value: `${normalStat['win_rate_percentage']}%` },
      { label: 'Top 3', value: `${normalStat['top3_rate_percentage']}%` },
      { label: '평균 순위', value: `${normalStat['average_rank']}위` },
      { label: '평균 TK', value: normalStat['average_team_kills'] },
      { label: '평균 딜량', value: normalStat['average_damage_to_players'] },
      { label: '평균 KDA', value: normalStat['kda'] },
      { label: '폼 점수', value: Math.round(normalStat['form_score']*100)/100}
    ],
    combat: [
      { label: '평균 처치', value: normalStat['average_kills'] },
      { label: '평균 사망', value: normalStat['average_deaths'] },
      { label: '평균 어시스트', value: normalStat['average_assists'] },
      { label: '평균 받은 피해량', value: normalStat['avg_damage_from_players'] },
      { label: '평균 아군 치유량', value: normalStat['avg_team_heal'] },
      { label: '평균 클러치 횟수', value: normalStat['avg_clutch']},
      { label: '평균 터미네이트 횟수', value: normalStat['avg_terminate']}
    ],
    operation: [
      { label: '평균 동물 처치', value: normalStat['average_monster_kills'] },
      { label: '평균 게임 시간', value: `${normalStat['average_game_time_minutes']}분` },
      { label: '평균 크레딧 획득량', value: normalStat['avg_credit_gain']},
      { label: 'DPC', value: "업데이트 예정"}
    ],
    vision: [
      { label: '평균 시야 점수', value: normalStat['avg_vision_score'] },
      { label: '평균 카메라 설치', value: normalStat['avg_camera_add']},
      { label: '평균 카메라 파괴', value: normalStat['avg_camera_remove']},
      { label: '평균 정찰 드론 사용', value: normalStat['avg_recon_drone']},
      { label: '평균 emp 드론 사용', value: normalStat['avg_emp_drone']},
      { label: '평균 cctv 작동', value: normalStat['avg_use_cctv']}
    ]
  } : { core: [], combat: [], operation: [], vision: [] };

  // 1. my_normal_data를 섹션별 Map으로 변환합니다. (빠른 조회를 위함)
  //    (데이터가 없는 경우를 대비해 || []로 안전장치 추가)위로
  const baseStatsMap = {
    core: new Map(
      my_normal_data.core?.map(item => [item.label, item.value]) || []
    ),
    combat: new Map(
      my_normal_data.combat?.map(item => [item.label, item.value]) || []
    ),
    operation: new Map(
      my_normal_data.operation?.map(item => [item.label, item.value]) || []
    ),
    vision: new Map(
      my_normal_data.vision?.map(item => [item.label, item.value]) || []
    )
  };

  // 2. Map 객체를 받아, { ...item, baseValue }를 반환하는 
  //    매핑 함수를 생성하는 팩토리(Factory) 함수입니다.
  const createBaseValueMapper = (sectionMap) => (item) => {
    // sectionMap (예: baseStatsMap.core)에서 item.label로 값을 찾습니다.
    return { ...item, baseValue: sectionMap.get(item.label) };
  };

  const diaNormalStatsData = diaNormalCharStats ? {
    core: [
      { label: '승률', value: `${(diaNormalCharStats['win_rate'] * 100).toFixed(2)}%` },
      { label: 'Top 3', value: `${(diaNormalCharStats['top3_rate'] * 100).toFixed(2)}%` },
      { label: '평균 순위', value: `${diaNormalCharStats['average_rank']}위` },
      { label: '평균 TK', value: diaNormalCharStats['average_team_kills'] },
      { label: '평균 딜량', value: diaNormalCharStats['average_damage_to_players'] },
      { label: '평균 KDA', value: diaNormalCharStats['kda'] },
      { label: '\u00A0', value:'\u00A0'}
    ].map(createBaseValueMapper(baseStatsMap.core)),
    combat: [
      { label: '평균 처치', value: diaNormalCharStats['average_kills'] },
      { label: '평균 사망', value: diaNormalCharStats['average_deaths'] },
      { label: '평균 어시스트', value: diaNormalCharStats['average_assists'] },
      { label: '평균 받은 피해량', value: diaNormalCharStats['average_damage_taken'] },
      { label: '평균 아군 치유량', value: diaNormalCharStats['average_team_heal'] },
      { label: '평균 클러치 횟수', value: diaNormalCharStats['avg_clutch']},
      { label: '평균 터미네이트 횟수', value: diaNormalCharStats['avg_terminate']}
    ].map(createBaseValueMapper(baseStatsMap.combat)),
    operation: [
      { label: '평균 동물 처치', value: diaNormalCharStats['average_monster_kills'] },
      {
        label: '평균 게임 시간', value: diaNormalCharStats['average_game_duration_minutes'] ?
          `${diaNormalCharStats['average_game_duration_minutes'].toFixed(1)}분` : 'N/A'
      },
      { label: '평균 크레딧 획득량', value: diaNormalCharStats['avg_credit_gain']},
      { label: 'DPC', value: "업데이트 예정"}
    ].map(createBaseValueMapper(baseStatsMap.operation)),
    vision:[
      { label: '평균 시야 점수', value: diaNormalCharStats['average_vision_score'] },
      { label: '평균 카메라 설치', value: diaNormalCharStats['avg_camera_add']},
      { label: '평균 카메라 파괴', value: diaNormalCharStats['avg_camera_remove']},
      { label: '평균 정찰 드론 사용', value: diaNormalCharStats['avg_recon_drone']},
      { label: '평균 emp 드론 사용', value: diaNormalCharStats['avg_emp_drone']},
      { label: '평균 cctv 작동', value: diaNormalCharStats['avg_use_cctv']}
    ].map(createBaseValueMapper(baseStatsMap.vision))
  } : { core: [], combat: [], operation: [], vision: [] };

  const mostPlayedChars = normalStat.recent_most_3_characters;

  const [isDetailedVisible, setIsDetailedVisible] = useState(false);

  const toggleDetailedVisibility = useCallback(() => {
    setIsDetailedVisible(prev => !prev);
  }, []);

    return (
        <>
            <div className={styles['table-section']}>
                <StatTable
                    title="내 평균 지표"
                    data={my_normal_data} // 수정한 부분
                    tooltipText="최근 일반 게임 20판의 데이터로 평균 지표를 나타냅니다."
                    isDetailedVisible={isDetailedVisible}
                    onToggleDetailed={toggleDetailedVisibility}
                    btnVisible={true}
                />

                {/* '일반'일 때 일반 관련 테이블 표시 (수정한 부분) */}
                {
                    diaNormalStatsData ? (
                        <StatTable title={"다이아+ "+diaNormalCharStats["character_name"]+" 평균 지표"} data={diaNormalStatsData}
                            tooltipText="최근 일반 게임에서 가장 많이 사용한 실험체의 다이아 이상 구간에서의 평균 지표를 나타냅니다."
                            isDetailedVisible={isDetailedVisible}
                            onToggleDetailed={toggleDetailedVisibility} />
                    ) : (
                        <StatTable title="모스트 다이아+ 평균 지표" data={[{ label: '최근 일반 게임 기록이 부족합니다.', value: '' }]}
                            tooltipText="최근 일반 게임에서 가장 많이 사용한 실험체의 다이아 이상 구간에서의 평균 지표를 나타냅니다."
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
                            <p>일반 게임을 플레이하면 정보가 표시됩니다.</p>
                        </div>
                    )}
                </div>
                <div className={styles['bottom-section-right']}>
                    {/* AIAnalysis 컴포넌트에 title과 analysis를 조건부로 전달 (수정한 부분) */}
                    <AIAnalysis
                        title="아디나의 수정구슬"
                        analysis={ai}
                        loading={loading}
                        ver= 'adina'
                    />
                </div>
            </div>
        </>
    )
}