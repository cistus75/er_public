'use client';

import styles from "./pageComp.module.css";

import { useState, useCallback } from 'react';
import StatTable from "../components/StatTable";
import PhaseTable from "../components/PhaseTable";
import AIAnalysis from "../components/AIAnalysis";
import MostPlayed from "../components/MostPlayed";

export default function CobaltPage({cobaltStat, ai, loading }) {
    if(!cobaltStat){
        return <div>데이터를 불러오는 중입니다...</div>;
    }  
    
    if(cobaltStat['no_record']){
        return <div className={styles.noRecord}>코발트 플레이 데이터가 없습니다.</div>
    }


    const cobaltStatData = !cobaltStat.no_record ? {
    core: [
      { label: '승률', value: `${cobaltStat['win_rate_percentage']}%` },
      { label: '평균 TK', value: cobaltStat['average_team_kills'] },
      { label: '평균 딜량', value: cobaltStat['average_damage_to_players'] },
      { label: '평균 KDA', value: cobaltStat['kda'] }
    ],
    combat: [
      { label: '평균 처치', value: cobaltStat['average_kills'] },
      { label: '평균 사망', value: cobaltStat['average_deaths'] },
      { label: '평균 어시스트', value: cobaltStat['average_assists'] },
      { label: '평균 받은 피해량', value: cobaltStat['avg_damage_from_players'] },
      { label: '평균 아군 치유량', value: cobaltStat['avg_team_heal'] }
    ],
    operation: [
      { label: '평균 게임 시간', value: `${cobaltStat['average_game_time_minutes']}분` },
      { label: '평균 크레딧 획득량', value: cobaltStat['avg_credit_gain']}
    ],
    vision: [
      { label: '평균 시야 점수', value: cobaltStat['avg_vision_score'] },
      { label: '평균 카메라 설치', value: cobaltStat['avg_camera_add']},
      { label: '평균 카메라 파괴', value: cobaltStat['avg_camera_remove']}
    ]
  } : { core: [], combat: [], operation: [], vision: [] };
    const cobaltPhaseData = !cobaltStat['no_record'] ? [
        {label: '페이즈1 평균 처치', value: cobaltStat['kd_phase']['p1_kills'].toFixed(2)},
        {label: '페이즈1 평균 사망', value: cobaltStat['kd_phase']['p1_deaths'].toFixed(2)},
        {label: '페이즈2 평균 처치', value: cobaltStat['kd_phase']['p2_kills'].toFixed(2)},
        {label: '페이즈2 평균 사망', value: cobaltStat['kd_phase']['p2_deaths'].toFixed(2)},
        {label: '페이즈3 평균 처치', value: cobaltStat['kd_phase']['p3_kills'].toFixed(2)},
        {label: '페이즈3 평균 사망', value: cobaltStat['kd_phase']['p3_deaths'].toFixed(2)},
    ] : [];
    
    const mostPlayedChars = cobaltStat?.recent_most_3_characters;

    const [isDetailedVisible, setIsDetailedVisible] = useState(false);

    const toggleDetailedVisibility = useCallback(() => {
        setIsDetailedVisible(prev => !prev);
    }, []);

    return (
        <>
            <div className={styles['table-section']}>
                <StatTable
                    title="내 평균 지표"
                    data={cobaltStatData} // 수정한 부분
                    tooltipText="최근 코발트 게임 20판의 데이터로 평균 지표를 나타냅니다."
                    isDetailedVisible={isDetailedVisible}
                    onToggleDetailed={toggleDetailedVisibility}
                    btnVisible={true}
                />
                <PhaseTable
                    title="페이즈별 지표"
                    data={cobaltPhaseData}
                    tooltipText={"최근 코발트 게임 20판의 페이즈별 평균 지표를 나타냅니다."}
                />
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
                    <AIAnalysis
                        title="아디나의 수정구슬"
                        analysis={ai}
                        loading={loading}
                        ver='adina'
                    />
                </div>
            </div>
        </>
    )
}