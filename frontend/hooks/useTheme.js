'use client';

import { useEffect, useState } from 'react';

export function useTheme() {
  const [theme, setTheme] = useState(undefined);

  // 초기 렌더링에서는 서버와 클라이언트의 테마가 달라지지 않도록 값을 비워 둡니다.
  useEffect(() => {
    const savedTheme = localStorage.getItem('theme') || 'light';
    setTheme(savedTheme);
  }, []);

  // 테마를 DOM과 localStorage에 함께 저장해 다음 방문에도 유지합니다.
  useEffect(() => {
    if (theme) {
      document.documentElement.className = theme;
      localStorage.setItem('theme', theme);
    }
  }, [theme]);

  const toggleTheme = () => {
    setTheme((prev) => (prev === 'light' ? 'dark' : 'light'));
  };

  return { theme, toggleTheme };
}
