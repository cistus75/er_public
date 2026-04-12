"use client";

import React, { useState, useEffect, useRef } from 'react';
import styles from "./AnnouncementBar.module.css";

const AnnouncementBar = () => {
  const [announcements, setAnnouncements] = useState([]);
  const [currentAnnouncementIndex, setCurrentAnnouncementIndex] = useState(0);
  const [animationStyle, setAnimationStyle] = useState({});
  const [isScrolling, setIsScrolling] = useState(false); // 스크롤 여부 상태 추가
  const announcementRef = useRef(null);

  useEffect(() => {
    fetch('/announcement/announcements.json')
      .then(response => {
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return response.json();
      })
      .then(data => setAnnouncements(data.messages || []))
      .catch(error => console.error('Error fetching announcements:', error));
  }, []);

  // 공지사항이 바뀔 때마다 스크롤이 필요한지 확인하는 로직
  useEffect(() => {
    if (announcementRef.current && announcements.length > 0) {
      const element = announcementRef.current;
      const container = element.parentElement;
      
      const isOverflowing = element.scrollWidth > container.clientWidth;
      setIsScrolling(isOverflowing);

      if (isOverflowing) {
        // 스크롤이 필요할 경우, 애니메이션 스타일 계산
        const scrollDistance = container.clientWidth + element.scrollWidth;
        const speed = 80;
        const duration = Math.max(scrollDistance / speed, 5);

        setAnimationStyle({
          animationName: styles.marquee,
          animationDuration: `${duration}s`,
          animationIterationCount: '1', // 한 번만 실행하고 끝나면 다음으로 넘어감
        });
      } else {
        // 스크롤이 필요 없으면 애니메이션 스타일 초기화
        setAnimationStyle({});
      }
    }
  }, [currentAnnouncementIndex, announcements]);

  // 스크롤이 없는 공지사항을 위한 타이머 로직
  useEffect(() => {
    let timerId = null;
    // 공지사항이 여러 개이고, 스크롤 중이 아닐 때만 5초 타이머 설정
    if (announcements.length > 1 && !isScrolling) {
      timerId = setTimeout(() => {
        setCurrentAnnouncementIndex(prevIndex => (prevIndex + 1) % announcements.length);
      }, 5000); // 5초
    }
    // 컴포넌트가 언마운트되거나 의존성이 변경될 때 타이머 정리
    return () => clearTimeout(timerId);
  }, [isScrolling, currentAnnouncementIndex, announcements.length]);


  // 스크롤 애니메이션이 끝났을 때 다음 공지사항으로 넘기는 함수
  const handleAnimationEnd = () => {
    // 스크롤 중인 경우에만 다음 인덱스로 업데이트
    if (isScrolling && announcements.length > 1) {
      setCurrentAnnouncementIndex(prevIndex => (prevIndex + 1) % announcements.length);
    }
  };

  if (announcements.length === 0) {
    return null;
  }

  return (
    <div className={styles.announcementBar}>
      <p 
        key={currentAnnouncementIndex}
        ref={announcementRef}
        className={`${styles.announcementText} ${isScrolling?styles.scrollingText:''}`}
        style={animationStyle}
        onAnimationEnd={handleAnimationEnd}
      >
        {announcements[currentAnnouncementIndex]}
      </p>
    </div>
  );
};

export default AnnouncementBar;

