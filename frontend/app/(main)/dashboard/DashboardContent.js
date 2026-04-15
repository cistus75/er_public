'use client';

import Image from 'next/image';
import styles from './page.module.css';
import { useState } from 'react';
import { useSearchParams } from 'next/navigation';
import { rankImgs } from '@/public/rank/rankImgs';
import { useUserStat } from '@/hooks/useUserStat';

import StatPage from './StatPage';
import CobaltPage from './CobaltPage';
import LoadingWastingTime from '../components/shared/LoadingWastingTime';

// ── 탭별 설정 상수 ─────────────────────────────────────────
// 문자열 리터럴을 렌더링 로직에서 분리합니다.
const TAB_CONFIG = {
  rank: {
    mainTooltip: '최근 랭크 게임 20판의 데이터로 평균 지표를 나타냅니다.',
    comparisonTooltip:
      '최근 랭크 게임에서 가장 많이 사용한 실험체의 다이아 이상 구간에서의 평균 지표를 나타냅니다.',
    noComparisonMessage: '최근 랭크 게임 기록이 부족합니다.',
    noRecordMessage: '랭크 게임 플레이 데이터가 없습니다.',
    noMostPlayedMessage: '랭크 게임을 플레이하면 정보가 표시됩니다.',
    aiTitle: '아디나의 수정구슬',
    aiVer: 'adina',
  },
  angpyeong: {
    mainTooltip: '최근 랭크 게임 20판의 데이터로 평균 지표를 나타냅니다.',
    comparisonTooltip:
      '최근 랭크 게임에서 가장 많이 사용한 실험체의 다이아 이상 구간에서의 평균 지표를 나타냅니다.',
    noComparisonMessage: '최근 랭크 게임 기록이 부족합니다.',
    noRecordMessage: '랭크 게임 플레이 데이터가 없습니다.',
    noMostPlayedMessage: '랭크 게임을 플레이하면 정보가 표시됩니다.',
    aiTitle: '비앙카의 혈액샘플',
    aiVer: 'bianca',
  },
  normal: {
    mainTooltip: '최근 일반 게임 20판의 데이터로 평균 지표를 나타냅니다.',
    comparisonTooltip:
      '최근 일반 게임에서 가장 많이 사용한 실험체의 다이아 이상 구간에서의 평균 지표를 나타냅니다.',
    noComparisonMessage: '최근 일반 게임 기록이 부족합니다.',
    noRecordMessage: '일반 게임 플레이 데이터가 없습니다.',
    noMostPlayedMessage: '일반 게임을 플레이하면 정보가 표시됩니다.',
    aiTitle: '아디나의 수정구슬',
    aiVer: 'adina',
  },
};

const GUIDE_TEXT = {
  rank:      '최근 랭크 게임 20판의 지표를 분석합니다. 분석되는 게임 판 수에는 차이가 있을 수 있습니다.',
  angpyeong: '표독한 비앙카가 최근 랭크 게임 20판의 지표를 분석합니다. 하지만 가끔은...',
  normal:    '최근 일반 게임 20판의 지표를 분석합니다. 분석되는 게임 판 수에는 차이가 있을 수 있습니다.',
  cobalt:    '최근 코발트 게임 20판의 지표를 분석합니다. 분석되는 게임 판 수에는 차이가 있을 수 있습니다.',
};

const TABS = [
  { key: 'rank',      label: '랭크' },
  { key: 'normal',    label: '일반' },
  { key: 'angpyeong', label: '앙평' },
  { key: 'cobalt',    label: '코발트' },
];
// ────────────────────────────────────────────────────────────

export default function DashboardContent() {
  const searchParams = useSearchParams();
  const nickname = searchParams.get('nickname');

  const [gameType, setGameType] = useState('rank');
  const [nameVisible, setNameVisible] = useState(true);

  const { data, loading, error } = useUserStat(nickname);

  if (loading) {
    return <LoadingWastingTime message="데이터를 불러오는 중 입니다..." />;
  }

  if (error || !data?.rank) {
    const errorMessage = error || '데이터를 불러올 수 없습니다. 닉네임을 다시 확인해주세요.';
    return (
      <div style={{ color: 'var(--text-color)', textAlign: 'center', marginTop: '50px' }}>
        {errorMessage}
      </div>
    );
  }

  const {
    rank_stat: rankStat,
    normal_stat: normalStat,
    cobalt_stat: cobaltStat,
    badges,
    rank: rankData,
    rank_ai_analysis: rankAiAnalysis,
    normal_ai_analysis: normalAiAnalysis,
    angpyeong_ai_analysis: angpyeongAiAnalysis,
    cobalt_ai_analysis: cobaltAiAnalysis,
    tier_stats: tierStats,
    rank_most_char_dia_stats: diaRankCharStats,
    normal_most_char_dia_stats: diaNormalCharStats,
    tier,
  } = data;

  const renderStatContent = () => {
    const config = TAB_CONFIG[gameType];

    switch (gameType) {
      case 'rank':
      case 'angpyeong':
        return (
          <StatPage
            stat={rankStat}
            comparisonStat={diaRankCharStats}
            tierStat={tierStats}        // undefined가 아닌 값 → 티어 섹션 표시
            ai={gameType === 'angpyeong' ? angpyeongAiAnalysis : rankAiAnalysis}
            loading={loading}
            {...config}
          />
        );
      case 'normal':
        return (
          <StatPage
            stat={normalStat}
            comparisonStat={diaNormalCharStats}
                                        // tierStat 미전달 → undefined → 티어 섹션 숨김
            ai={normalAiAnalysis}
            loading={loading}
            {...config}
          />
        );
      case 'cobalt':
        return (
          <CobaltPage
            cobaltStat={cobaltStat}
            ai={cobaltAiAnalysis}
            loading={loading}
          />
        );
      default:
        return null;
    }
  };

  return (
    <div className={styles['contents']}>
      {/* ── 유저 정보 영역 ── */}
      <div className={styles['user-info']}>
        <div className={styles['rank-area']}>
          {tier && <Image src={rankImgs[tier]} alt="User Tier" width={80} height={80} />}
        </div>
        <div className={styles['name-level-area']}>
          <div className={styles['nickname-area']}>
            <span className={styles['nickname-text']}>{nameVisible ? nickname : '_____'}</span>
            <input
              type="checkbox"
              onChange={(e) => setNameVisible(e.target.checked)}
              checked={nameVisible}
            />
          </div>
          <div className={styles['score-area']}>
            <span className={styles['level-text']}>
              Score : {nameVisible ? (rankData?.mmr || 'Unranked') : '_____'}
            </span>
          </div>
          <div className={styles['score-area']}>
            <span className={styles['level-text']}>
              {nameVisible
                ? rankStat?.account_level || normalStat?.account_level || cobaltStat?.account_level || '-'
                : '_'}{' '}
              Lvl
            </span>
          </div>
          <div className={styles['rank-text-area']}>
            <span className={styles['level-text']}>
              Rank : {nameVisible ? (rankData?.rank || '-') : '_____'}
            </span>
          </div>
        </div>
        <div className={styles['badge-area']}>
          {badges?.slice(0, 10).map((badge, index) => (
            <div key={index} className={styles['badge-item']}>
              {badge.img ? (
                <Image src={badge.img} alt={badge.alt} width={70} height={70} />
              ) : (
                badge.name
              )}
              <span className={styles['badge-tooltip']}>{badge.alt}</span>
            </div>
          ))}
        </div>
      </div>

      {/* ── 탭 전환 영역 ── */}
      <div className={styles['middle-container']}>
        <div className={styles['toggle']}>
          {TABS.map(({ key, label }) => (
            <button
              key={key}
              className={`${styles['toggle-button']} ${gameType === key ? styles.active : ''}`}
              onClick={() => setGameType(key)}
            >
              {label}
            </button>
          ))}
        </div>
        <div className={styles['guide']}>{GUIDE_TEXT[gameType]}</div>
      </div>

      {/* ── 탭 콘텐츠 ── */}
      <div className={styles['detail']}>{renderStatContent()}</div>
    </div>
  );
}
