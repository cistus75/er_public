'use client';

import Image from "next/image";
import styles from "./page.module.css";
import { useEffect, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import { rankImgs } from '@/public/rank/rankImgs';

import RankPage from "./RankPage";
import NormalPage from "./NormalPage";
import CobaltPage from "./CobaltPage";

import LoadingWastingTime from "../components/LoadingWastingTime";

export default function DashboardContent() {
  const searchParams = useSearchParams();
  const nickname = searchParams.get('nickname');

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const [gameType, setGameType] = useState('rank'); 

  const [rankStat, setRankStat] = useState(null);
  const [normalStat, setNormalStat] = useState(null);
  const [cobaltStat, setCobaltStat] = useState(null);
  const [badges, setBadges] = useState(null);
  const [rankData, setRankData] = useState(null);
  const [tier, setTier] = useState(null);
  const [rankAiAnalysis, setRankAiAnalysis] = useState('');
  const [normalAiAnalysis, setNormalAiAnalysis] = useState('');
  const [angpyeongAiAnalysis, setAngpyeongAiAnalysis] = useState('');
  const [cobaltAiAnalysis, setCobaltAiAnalysis] = useState('');
  
  const [tierStats, setTierStats] = useState(null); 
  const [diaRankCharStats, setDiaRankCharStats] = useState(null);
  const [diaNormalCharStats, setDiaNormalCharStats] = useState(null);

  const [nameVisible, setNameVisible] = useState(true);

  const rawBaseUrl = process.env.NEXT_PUBLIC_FASTAPI_BASE_URL || '';
  const FASTAPI_BASE_URL = rawBaseUrl.replace(/\/$/, '');
  // const FASTAPI_BASE_URL = 'https://er-public.onrender.com';

  useEffect(() => {
    if (!nickname) {
      setError("닉네임 정보가 없습니다. 다시 검색해주세요.");
      setLoading(false);
      return;
    }

    const fetchUserData = async () => {
      setLoading(true);
      setError(null);
      try {
        const userIdResponse = await fetch(`${FASTAPI_BASE_URL}/api/users/num/${nickname}`);
        if (!userIdResponse.ok) throw new Error('유저 번호를 가져오는데 실패했습니다.');
        const userIdData = await userIdResponse.json();
        const fetchedUserId = userIdData.userId;

        const userStatResponse = await fetch(`${FASTAPI_BASE_URL}/api/users/stat/${fetchedUserId}`);
        if (!userStatResponse.ok) throw new Error('유저 통계를 가져오는데 실패했습니다.');
        
        const userStatData = await userStatResponse.json();
        
        setRankStat(userStatData.rank_stat || null);
        setNormalStat(userStatData.normal_stat || null);
        setCobaltStat(userStatData.cobalt_stat || null);
        // console.log(`!rank_stat = ${!userStatData.rank_stat}`);
        if(!userStatData.rank_stat){
          console.log(userStatData.rankStat);
        }
        // console.log(`!rankStat = ${!rankStat}`);
        setBadges(userStatData.badges);
        setRankData(userStatData.rank);
        setRankAiAnalysis(userStatData.rank_ai_analysis);
        setNormalAiAnalysis(userStatData.normal_ai_analysis);
        setAngpyeongAiAnalysis(userStatData.angpyeong_ai_analysis);
        setCobaltAiAnalysis(userStatData.cobalt_ai_analysis);
        setTierStats(userStatData.tier_stats)
        setDiaRankCharStats(userStatData.rank_most_char_dia_stats)
        setDiaNormalCharStats(userStatData.normal_most_char_dia_stats)
        setTier(userStatData.tier)
      } catch (err) {
        console.error('데이터 불러오기 오류:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchUserData();
  }, [nickname]);

  // useEffect(() => {
  //   console.log('✅ rankStat이 업데이트 됨:', rankStat);
  // }, [rankStat]);

  if (loading) {
    return <LoadingWastingTime message="데이터를 불러오는 중 입니다..."/>;
  }
  
  if (error || !rankData) {
    // 1. 어떤 데이터가 비어있는지 담을 배열을 생성합니다.
    const missingData = [];
    if (!rankData) missingData.push('랭크 정보(rankData)');
    if (!rankStat) missingData.push('랭크 통계(rankStat)');
    if (!normalStat) missingData.push('일반 통계(normalStat)');
    if (!cobaltStat) missingData.push('코발트 통계(cobltStat)');

    // 2. 상황에 맞는 에러 메시지를 생성합니다.
    const errorMessage = missingData.length > 0 
      ? `다음 데이터를 불러오는 데 실패했습니다: ${missingData.join(', ')}`
      : '데이터를 불러올 수 없습니다. 닉네임을 다시 확인해주세요.';

    return (
      <div style={{ color: 'black', textAlign: 'center', marginTop: '50px' }}>
        {/* 3. 백엔드 에러가 있으면 먼저 보여주고, 없으면 생성된 메시지를 보여줍니다. */}
        {error || errorMessage}
      </div>
    );
  }

  // const PageComponents = {
  //   rank : <RankPage
  //                   gameType={gameType}
  //                   mainStat={rankStat}
  //                   diaRankCharStats={diaRankCharStats}
  //                   tierStats={tierStats}
  //                   rankAi={rankAiAnalysis}
  //                   angpyeongAi={angpyeongAiAnalysis}
  //                   loading={loading}
  //               />,
  //   normal : <NormalPage
  //                   gameType={gameType}
  //                   mainStat={normalStat}
  //                   diaNormalCharStats={diaNormalCharStats}
  //                   ai={normalAiAnalysis}
  //                   loading={loading}
  //               />,
  //   cobalt : <CobaltPage 
  //                   cobaltStat = {cobaltStat}
  //                   ai = {cobaltAiAnalysis}
  //                   loading={loading}
  //                 />
  // }
  // console.log()
  // PageComponents.angpyeong = PageComponents.rank;
  // const StatContent = PageComponents[gameType];
  const renderStatContent = () => {
    switch (gameType) {
      case 'rank':
      case 'angpyeong':
        return <RankPage
          gameType={gameType}
          rankStat={rankStat} // 'mainStat'으로 prop 이름 통일
          diaRankCharStats={diaRankCharStats}
          tierStats={tierStats}
          rankAi={rankAiAnalysis}
          angpyeongAi={angpyeongAiAnalysis}
          loading={loading}
        />;
      case 'normal':
        return <NormalPage
          normalStat={normalStat}
          diaNormalCharStats={diaNormalCharStats}
          ai={normalAiAnalysis}
          loading={loading}
        />;
      case 'cobalt':
        return <CobaltPage 
          cobaltStat={cobaltStat} // 'mainStat'으로 prop 이름 통일
          ai={cobaltAiAnalysis}
          loading={loading}
        />;
      default:
        return null; // 기본값
    }
  };


  const ChangeNameVisible = (event) =>{
    setNameVisible(event.target.checked);
  };

  const guide = () => {
    switch (gameType){
      case 'rank':
        return "최근 랭크 게임 20판의 지표를 분석합니다. 분석되는 게임 판 수에는 차이가 있을 수 있습니다.";
      case 'angpyeong':
        return "표독한 비앙카가 최근 랭크 게임 20판의 지표를 분석합니다. 하지만 가끔은...";
      case 'normal':
        return "최근 일반 게임 20판의 지표를 분석합니다. 분석되는 게임 판 수에는 차이가 있을 수 있습니다.";
      case 'cobalt':
        return "최근 코발트 게임 20판의 지표를 분석합니다. 분석되는 게임 판 수에는 차이가 있을 수 있습니다.";
      default:
        return "";
    }
  }

return (
    <div className={styles['contents']}>
      <div className={styles['user-info']}>
        <div className={styles['rank-area']}>
          {tier && ( <Image src={rankImgs[tier]} alt="User Tier" width={80} height={80} /> )}
        </div>
        <div className={styles['name-level-area']}>
          <div className={styles['nickname-area']}>
            <span className={styles['nickname-text']}>{nameVisible ? nickname : "_____"}</span>
            <input type="checkbox" onChange={ChangeNameVisible} checked={nameVisible}></input>
          </div>
          <div className={styles['score-area']}>
            <span className={styles['level-text']}>Score : {nameVisible ? (rankData?.mmr || 'Unranked') : "_____"}</span>
          </div>
          <div className={styles['score-area']}>
            <span className={styles['level-text']}>{nameVisible ? (rankStat?.account_level || normalStat?.account_level || cobaltStat?.account_level || '-') : "_"} Lvl</span>
          </div>
          <div className={styles['rank-text-area']}>
            <span className={styles['level-text']}>Rank : {nameVisible ? (rankData?.rank || '-') : "_____"}</span>
          </div>
        </div>
        <div className={styles['badge-area']}>
          {badges?.slice(0, 10).map((badge, index) => (
            <div key={index} className={styles['badge-item']}> 
              {badge.img ? <Image src={badge.img} alt={badge.alt} width={70} height={70} /> : badge.name}
              <span className={styles['badge-tooltip']}>
                {badge.alt}
              </span>
            </div>
          ))}
        </div>
      </div>

      <div className={styles['middle-container']}>
        <div className={styles['toggle']}>
          <button
            className={`${styles['toggle-button']} ${gameType === 'rank' ? styles.active : ''}`}
            onClick={() => setGameType('rank')}
          >
            랭크
          </button>
          <button
            className={`${styles['toggle-button']} ${gameType === 'normal' ? styles.active : ''}`}
            onClick={() => setGameType('normal')}
          >
            일반
          </button>
          <button
            className={`${styles['toggle-button']} ${gameType === 'angpyeong' ? styles.active : ''}`}
            onClick={() => setGameType('angpyeong')}
          >
            앙평
          </button>
          <button
            className={`${styles['toggle-button']} ${gameType === 'cobalt' ? styles.active : ''}`}
            onClick={() => setGameType('cobalt')}
          >
            코발트
          </button>
        </div>
        <div className={styles['guide']}>
          {guide()}
        </div>
      </div>

      <div className={styles['detail']}>
        {renderStatContent()}
      </div>
    </div>
  );
}

