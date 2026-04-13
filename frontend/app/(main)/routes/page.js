// app/(main)/routes/page.js
'use client';

import styles from './page.module.css'
import { useState } from 'react';

// 각 UI 섹션을 담당할 전문 컴포넌트들을 모두 import 합니다.
import RouteSearch from '../components/RouteSearch';
import RouteSummary from '../components/route/RouteSummary';
import RoutePath from '../components/route/RoutePath';
import RouteItems from '../components/route/RouteItems';
import RouteTraits from '../components/route/RouteTraits';
import RouteSkillOrder from '../components/route/RouteSkillOrder';

import LoadingWastingTime from '../components/LoadingWastingTime';

export default function RouteSearchPage() {
  // 데이터, 로딩, 에러 상태를 모두 이 페이지(메인 PD)에서 관리합니다.
  const [mvpData, setMvpData] = useState(null);
  const [fullApiData, setFullApiData] = useState(null); // 확장용 원본 데이터
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // RouteSearch 컴포넌트가 호출할 검색 처리 함수
  const handleRouteSearch = async (routeId) => {
    setLoading(true);
    setError(null);
    setMvpData(null);
    setFullApiData(null); // 이전 결과 초기화

    const rawBaseUrl = process.env.NEXT_PUBLIC_FASTAPI_BASE_URL || '';
    const FASTAPI_BASE_URL = rawBaseUrl.replace(/\/$/, '');

    try {
      const res = await fetch(`${FASTAPI_BASE_URL}/api/routes/${routeId}`);
      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.detail || `'${routeId}'번 루트를 찾을 수 없습니다.`);
      }
      const data = await res.json();
      
      // MVP 데이터와 전체 데이터를 분리하여 상태에 저장 (지금은 동일)
      setMvpData(data); 
      setFullApiData(data); // 나중을 위해 전체 데이터도 저장

    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main style={{ padding: '2rem' }}>
      <h1 style={{textAlign:'center', font:'1.5rem',fontWeight:'bold'}}>이터널 리턴 루트 분석기</h1>
      
      {/* 검색창(입력 담당) 컴포넌트 */}
      <RouteSearch onSearch={handleRouteSearch} />

      <div className={styles.infoArea}>
        {loading && <LoadingWastingTime message="분석 중 입니다..."/>}
        {error && <p style={{ color: 'red' }}>오류: {error}</p>}
        
        {/* 데이터가 있을 때만 결과 컴포넌트들을 렌더링합니다. */}
        {mvpData && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', color: 'white' }}>
            <RouteSummary data={mvpData} />
          </div>
        )}
        {fullApiData &&(
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', color: 'white' }}>
                <RoutePath apiData={fullApiData} />
                <RouteItems apiData={fullApiData} />
                <RouteTraits apiData={fullApiData} />
                <RouteSkillOrder apiData={fullApiData} />
            </div>
        )}
      </div>
    </main>
  );
}