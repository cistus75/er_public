'use client';

/**
 * hooks/useUserStat.js
 * 상태 계층 — 유저 닉네임을 받아 userId 조회 → 통계 조회를 수행하는 커스텀 훅.
 * DashboardContent의 11개 useState + fetch 로직을 캡슐화합니다.
 */

import { useEffect, useState } from 'react';
import { getUserId, getUserStat } from '@/lib/api/userApi';

/**
 * @param {string|null} nickname
 * @returns {{ data: object|null, loading: boolean, error: string|null }}
 */
export function useUserStat(nickname) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!nickname) {
      setError('닉네임 정보가 없습니다. 다시 검색해주세요.');
      setLoading(false);
      return;
    }

    let cancelled = false;

    const fetchData = async () => {
      setLoading(true);
      setError(null);
      setData(null);

      try {
        const userId = await getUserId(nickname);
        const statData = await getUserStat(userId);

        if (!cancelled) {
          setData(statData);
        }
      } catch (err) {
        console.error('데이터 불러오기 오류:', err);
        if (!cancelled) {
          setError(err.message);
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    };

    fetchData();

    // 검색어가 바뀌면 이전 요청 결과를 무시합니다 (race condition 방지)
    return () => {
      cancelled = true;
    };
  }, [nickname]);

  return { data, loading, error };
}
