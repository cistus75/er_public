'use client';

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

  // 공지가 표시 영역보다 길 때만 스크롤 애니메이션을 적용합니다.
  useEffect(() => {
    if (announcementRef.current && announcements.length > 0) {
      const element = announcementRef.current;
      const container = element.parentElement;
      setIsScrolling(element.scrollWidth > container.clientWidth);
    }
  }, [currentAnnouncementIndex, announcements]);

  // 현재 공지를 기준으로 타이머를 다시 만들어 오래된 인덱스를 사용하지 않도록 합니다.
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
