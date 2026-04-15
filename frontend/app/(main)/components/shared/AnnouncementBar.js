'use client';

/**
 * AnnouncementBar.js
 * 프레젠테이션 계층 — 상단 공지사항 배너.
 *
 * 변경사항:
 *  - useAnnouncements 훅으로 데이터 fetch 분리
 *  - handleNext/handlePrev를 useCallback으로 메모이제이션 (stale closure 수정)
 *  - useEffect 의존성 배열에 handleNext 추가 (ESLint exhaustive-deps 준수)
 */

import React, { useState, useEffect, useRef, useCallback } from 'react';
import styles from './AnnouncementBar.module.css';
import { useAnnouncements } from '@/hooks/useAnnouncements';

const AnnouncementBar = () => {
  const announcements = useAnnouncements();
  const [currentAnnouncementIndex, setCurrentAnnouncementIndex] = useState(0);
  const [isScrolling, setIsScrolling] = useState(false);
  const announcementRef = useRef(null);

  const handleNext = useCallback(() => {
    setCurrentAnnouncementIndex((prev) => (prev + 1) % announcements.length);
  }, [announcements.length]);

  const handlePrev = useCallback(() => {
    setCurrentAnnouncementIndex((prev) =>
      prev === 0 ? announcements.length - 1 : prev - 1
    );
  }, [announcements.length]);

  // 텍스트 길이에 따른 스크롤 여부 체크
  useEffect(() => {
    if (announcementRef.current && announcements.length > 0) {
      const element = announcementRef.current;
      const container = element.parentElement;
      setIsScrolling(element.scrollWidth > container.clientWidth);
    }
  }, [currentAnnouncementIndex, announcements]);

  // 자동 넘김 (stale closure 수정: handleNext를 의존성 배열에 포함)
  useEffect(() => {
    if (announcements.length <= 1) return;
    const timer = setTimeout(handleNext, 5000);
    return () => clearTimeout(timer);
  }, [currentAnnouncementIndex, announcements.length, handleNext]);

  if (announcements.length === 0) return null;

  return (
    <div className={styles.announcementBar}>
      <div className={styles.textContainer}>
        <p
          key={currentAnnouncementIndex}
          ref={announcementRef}
          className={`${styles.announcementText} ${isScrolling ? styles.scrollingText : ''}`}
        >
          {announcements[currentAnnouncementIndex]}
        </p>
      </div>
      <div className={styles.controls}>
        <button onClick={handlePrev} className={styles.arrowBtn}>{'<'}</button>
        <span className={styles.pageIndicator}>
          <strong>{currentAnnouncementIndex + 1}</strong>/{announcements.length}
        </span>
        <button onClick={handleNext} className={styles.arrowBtn}>{'>'}</button>
      </div>
    </div>
  );
};

export default AnnouncementBar;