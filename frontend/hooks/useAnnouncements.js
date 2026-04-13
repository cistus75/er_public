'use client';

/**
 * hooks/useAnnouncements.js
 * 상태 계층 — 공지사항 목록을 fetch하는 커스텀 훅.
 * AnnouncementBar 컴포넌트의 데이터 의존성을 분리합니다.
 */

import { useEffect, useState } from 'react';

/**
 * @returns {string[]} 공지사항 메시지 배열
 */
export function useAnnouncements() {
  const [announcements, setAnnouncements] = useState([]);

  useEffect(() => {
    fetch('/announcement/announcements.json')
      .then((res) => (res.ok ? res.json() : { messages: [] }))
      .then((data) => setAnnouncements(data.messages || []))
      .catch((err) => console.error('공지사항 로드 오류:', err));
  }, []);

  return announcements;
}
