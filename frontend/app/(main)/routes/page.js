// app/(main)/routes/page.js
'use client';

/**
 * 변경사항:
 *  - getRouteById API 함수 적용으로 인라인 fetch 로직 제거
 *  - 에러 처리가 apiClient에서 통합 관리됨
 */

import styles from './page.module.css';
import { useState } from 'react';
import { getRouteById } from '@/lib/api/routeApi';

import RouteSearch from '../components/RouteSearch';
import RouteSummary from '../components/route/RouteSummary';
import RoutePath from '../components/route/RoutePath';
import RouteItems from '../components/route/RouteItems';
import RouteTraits from '../components/route/RouteTraits';
import RouteSkillOrder from '../components/route/RouteSkillOrder';
import LoadingWastingTime from '../components/LoadingWastingTime';

export default function RouteSearchPage() {
  const [mvpData, setMvpData] = useState(null);
  const [fullApiData, setFullApiData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleRouteSearch = async (routeId) => {
    setLoading(true);
    setError(null);
    setMvpData(null);
    setFullApiData(null);

    try {
      const data = await getRouteById(routeId);
      setMvpData(data);
      setFullApiData(data);
    } catch (err) {
      setError(err.message || `'${routeId}'번 루트를 찾을 수 없습니다.`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main style={{ padding: '2rem' }}>
      <h1 style={{ textAlign: 'center', font: '1.5rem', fontWeight: 'bold' }}>
        이터널 리턴 루트 분석기
      </h1>

      <RouteSearch onSearch={handleRouteSearch} />

      <div className={styles.infoArea}>
        {loading && <LoadingWastingTime message="분석 중 입니다..." />}
        {error && <p style={{ color: 'red' }}>오류: {error}</p>}

        {mvpData && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', color: 'white' }}>
            <RouteSummary data={mvpData} />
          </div>
        )}
        {fullApiData && (
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