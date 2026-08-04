'use client';

import { useEffect, useState } from 'react';
import { getUserId, getUserStat } from '@/lib/api/userApi';

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

    // 검색어가 바뀌면 이전 요청이 늦게 끝나도 현재 화면을 덮어쓰지 않도록 합니다.
    return () => {
      cancelled = true;
    };
  }, [nickname]);

  return { data, loading, error };
}
