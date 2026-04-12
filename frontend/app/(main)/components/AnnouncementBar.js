"use client";

import React, { useState, useEffect, useRef } from 'react';
import styles from "./AnnouncementBar.module.css";

const AnnouncementBar = () => {
  const [announcements, setAnnouncements] = useState([]);
  const [currentAnnouncementIndex, setCurrentAnnouncementIndex] = useState(0);
  const [isScrolling, setIsScrolling] = useState(false);
  const announcementRef = useRef(null);

  useEffect(() => {
    fetch('/announcement/announcements.json')
      .then(response => response.ok ? response.json() : { messages: [] })
      .then(data => setAnnouncements(data.messages || []))
      .catch(error => console.error('Error fetching announcements:', error));
  }, []);

  // 텍스트 길이에 따른 스크롤 여부 체크 (기존 로직 유지)
  useEffect(() => {
    if (announcementRef.current && announcements.length > 0) {
      const element = announcementRef.current;
      const container = element.parentElement;
      setIsScrolling(element.scrollWidth > container.clientWidth);
    }
  }, [currentAnnouncementIndex, announcements]);

  // 자동 넘김 로직 (사용자가 수동으로 넘길 수도 있으므로 유지 혹은 시간 조절)
  useEffect(() => {
    if (announcements.length <= 1) return;
    
    const timer = setTimeout(() => {
      handleNext();
    }, 5000); 

    return () => clearTimeout(timer);
  }, [currentAnnouncementIndex, announcements]);

  const handlePrev = () => {
    setCurrentAnnouncementIndex(prev => 
      prev === 0 ? announcements.length - 1 : prev - 1
    );
  };

  const handleNext = () => {
    setCurrentAnnouncementIndex(prev => 
      (prev + 1) % announcements.length
    );
  };

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
        <button onClick={handlePrev} className={styles.arrowBtn}>{"<"}</button>
        <span className={styles.pageIndicator}>
          <strong>{currentAnnouncementIndex + 1}</strong>/{announcements.length}
        </span>
        <button onClick={handleNext} className={styles.arrowBtn}>{">"}</button>
      </div>
    </div>
  );
};

export default AnnouncementBar;