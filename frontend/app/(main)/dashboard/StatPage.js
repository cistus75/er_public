'use client';

// 랭크와 일반 탭은 같은 레이아웃을 공유하고, 차이점은 props로 주입합니다.

import { useState, useCallback } from 'react';
import styles from './pageComp.module.css';

import StatTable from '../components/dashboard/StatTable';
import AIAnalysis from '../components/dashboard/AIAnalysis';
import MostPlayed from '../components/dashboard/MostPlayed';
import { getCharacterInfo } from '@/lib/characterData';
import {
  mapStatToViewModel,
  mapComparisonStatToViewModel,
  buildBaseStatsMap,
} from '@/lib/mappers/statMapper';

export default function StatPage({
  stat,
  comparisonStat,
  tierStat,
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

  const myData = mapStatToViewModel(stat);
  const baseStatsMap = buildBaseStatsMap(myData);

  const comparisonData = comparisonStat
    ? mapComparisonStatToViewModel(comparisonStat, baseStatsMap)
    : null;

  // 일반 모드에는 티어 비교 데이터가 없으므로 해당 표를 숨깁니다.
  const hasTierSection = tierStat !== undefined;
  const tierData = hasTierSection && tierStat
    ? mapComparisonStatToViewModel(tierStat, baseStatsMap)
    : null;

  const mostPlayedChars = stat.recent_most_3_characters;
  const mostCharInfo = getCharacterInfo(stat.most_used_character_code);

  return (
    <>
      <div className={styles['table-section']}>
        <StatTable
          title="내 평균 지표"
          data={myData}
          tooltipText={mainTooltip}
          isDetailedVisible={isDetailedVisible}
          onToggleDetailed={toggleDetailedVisibility}
          btnVisible={true}
        />

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
