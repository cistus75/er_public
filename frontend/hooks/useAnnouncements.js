'use client';

import { useEffect, useState } from 'react';

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
