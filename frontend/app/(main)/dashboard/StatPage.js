'use client';

/**
 * StatPage.js
 * 프레젠테이션 계층 — 랭크 / 앙평 / 일반 탭의 통합 UI 컴포넌트.
 *
 * 기존 RankPage.js + NormalPage.js를 하나로 병합합니다.
 * 두 컴포넌트의 차이는 설정값(문자열, tierStat 유무)뿐이므로,
 * DashboardContent에서 props로 주입하는 방식으로 통합했습니다.
 *
 * Props:
 *  stat              — 주 통계 객체 (rankStat | normalStat)
 *  comparisonStat    — 다이아+ 캐릭터 통계 (선택)
 *  tierStat          — 티어 평균 통계. undefined이면 티어 테이블을 렌더링하지 않습니다.
 *                      null이면 "데이터 부족" 메시지를 표시합니다. (랭크 전용)
 *  ai                — AI 분석 텍스트
 *  loading           — 로딩 상태
 *  noRecordMessage   — no_record일 때 표시할 메시지
 *  mainTooltip       — 내 평균 지표 테이블의 툴팁
 *  comparisonTooltip — 다이아+ 캐릭터 테이블의 툴팁
 *  noComparisonMessage — 비교 데이터 부족 시 메시지
 *  noMostPlayedMessage — 모스트 캐릭터 없을 때 안내 메시지
 *  aiTitle           — AI 분석 박스 제목
 *  aiVer             — AI 아이콘 버전 ('adina' | 'bianca')
 */

import { useState, useCallback } from 'react';
import styles from './pageComp.module.css';

import StatTable from '../components/StatTable';
import AIAnalysis from '../components/AIAnalysis';
import MostPlayed from '../components/MostPlayed';
import { getCharacterInfo } from '@/lib/characterData';
import {
  mapStatToViewModel,
  mapComparisonStatToViewModel,
  buildBaseStatsMap,
} from '@/lib/mappers/statMapper';

export default function StatPage({
  stat,
  comparisonStat,
  tierStat,             // undefined → 섹션 비표시 | null → 부족 메시지 | object → 데이터 표시
  ai,
  loading,
  noRecordMessage,
  mainTooltip,
  comparisonTooltip,
  noComparisonMessage,
  noMostPlayedMessage,
  aiTitle,
  aiVer = 'adina',
}) {
  // ✅ Hook은 조건부 return 이전 최상단에 위치합니다.
  const [isDetailedVisible, setIsDetailedVisible] = useState(false);
  const toggleDetailedVisibility = useCallback(() => {
    setIsDetailedVisible((prev) => !prev);
  }, []);

  if (!stat) {
    return <div>데이터를 불러오는 중입니다...</div>;
  }

  if (stat['no_record']) {
    return <div className={styles.noRecord}>{noRecordMessage}</div>;
  }

  // ── 도메인 계층 위임 ──
  const myData = mapStatToViewModel(stat);
  const baseStatsMap = buildBaseStatsMap(myData);

  const comparisonData = comparisonStat
    ? mapComparisonStatToViewModel(comparisonStat, baseStatsMap)
    : null;

  // tierStat이 undefined이면 티어 테이블 자체를 숨깁니다 (일반 모드).
  const hasTierSection = tierStat !== undefined;
  const tierData = hasTierSection && tierStat
    ? mapComparisonStatToViewModel(tierStat, baseStatsMap)
    : null;

  const mostPlayedChars = stat.recent_most_3_characters;
  const mostCharInfo = getCharacterInfo(stat.most_used_character_code);

  return (
    <>
      <div className={styles['table-section']}>
        {/* 내 평균 지표 */}
        <StatTable
          title="내 평균 지표"
          data={myData}
          tooltipText={mainTooltip}
          isDetailedVisible={isDetailedVisible}
          onToggleDetailed={toggleDetailedVisibility}
          btnVisible={true}
        />

        {/* 다이아+ 캐릭터 평균 지표 */}
        {comparisonData ? (
          <StatTable
            title={`다이아+ ${mostCharInfo.name} 평균 지표`}
            data={comparisonData}
            tooltipText={comparisonTooltip}
            isDetailedVisible={isDetailedVisible}
            onToggleDetailed={toggleDetailedVisibility}
          />
        ) : (
          <StatTable
            title="모스트 다이아+ 평균 지표"
            data={[{ label: noComparisonMessage, value: '' }]}
            tooltipText={comparisonTooltip}
            isDetailedVisible={isDetailedVisible}
            onToggleDetailed={toggleDetailedVisibility}
          />
        )}

        {/* 티어 평균 지표 — 랭크 모드에서만 (tierStat prop이 존재할 때) */}
        {hasTierSection && (
          tierData ? (
            <StatTable
              title="티어 평균 지표"
              data={tierData}
              tooltipText="나와 동일한 티어의 평균 지표를 나타냅니다. 미스릴 이상은 통합하여 나타냅니다."
              isDetailedVisible={isDetailedVisible}
              onToggleDetailed={toggleDetailedVisibility}
            />
          ) : (
            <StatTable
              title="티어 평균 지표"
              data={[{ label: '랭크 플레이 기록이나 티어 데이터가 부족합니다.', value: '' }]}
              tooltipText="나와 동일한 티어의 평균 지표를 나타냅니다. 미스릴 이상은 통합하여 나타냅니다."
              isDetailedVisible={isDetailedVisible}
              onToggleDetailed={toggleDetailedVisibility}
            />
          )
        )}
      </div>

      <div className={styles['bottom-section']}>
        <div className={styles['bottom-section-left']}>
          {mostPlayedChars && mostPlayedChars.length > 0 ? (
            <MostPlayed characters={mostPlayedChars} />
          ) : (
            <div className={styles.noDataModule}>
              <p>최근 플레이한 캐릭터 정보가 없습니다.</p>
              <p>{noMostPlayedMessage}</p>
            </div>
          )}
        </div>
        <div className={styles['bottom-section-right']}>
          <AIAnalysis
            title={aiTitle}
            analysis={ai}
            loading={loading}
            ver={aiVer}
          />
        </div>
      </div>
    </>
  );
}
