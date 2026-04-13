'use client';

/**
 * hooks/useTheme.js
 * 상태 계층 — 라이트/다크 테마를 관리하는 커스텀 훅.
 * ClientLayout의 테마 관련 useState + useEffect 로직을 캡슐화합니다.
 */

import { useEffect, useState } from 'react';

/**
 * @returns {{ theme: string|undefined, toggleTheme: () => void }}
 *   theme이 undefined이면 아직 localStorage를 읽기 전(SSR 하이드레이션 이전)입니다.
 */
export function useTheme() {
  const [theme, setTheme] = useState(undefined);

  // 마운트 시 localStorage에서 테마를 읽습니다.
  useEffect(() => {
    const savedTheme = localStorage.getItem('theme') || 'light';
    setTheme(savedTheme);
  }, []);

  // theme이 변경될 때마다 <html> className과 localStorage를 동기화합니다.
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
