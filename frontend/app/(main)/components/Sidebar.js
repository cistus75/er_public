// app/components/Sidebar.js
"use client";

import React from 'react';
import styles from './Sidebar.module.css';
import Link from 'next/link';

// ClientLayout으로부터 필요한 상태와 함수를 props로 전달받습니다.
const Sidebar = ({ isOpen, onClose, currentTheme, toggleTheme }) => {
  if (!isOpen) {
    return null;
  }

  return (
    <div className={styles.overlay} onClick={onClose}>
      <div className={styles.sidebar} onClick={(e) => e.stopPropagation()}>
        <h2 style={{all:'revert'}}>메뉴다요!</h2>
        {/* 여기에 다른 메뉴들을 추가할 수 있습니다. */}
        <ul className={styles.sidebarList}>
          <li><Link href="/routes">루트 검색</Link></li>
          <li><Link href='/patchnotes'>패치노트</Link></li>
          <li><Link href='/badges'>뱃지 일람</Link></li>
          <li><Link href='https://forms.gle/E5YcNN7ZAwQJMVhh7'>문의/제보</Link></li>
        </ul>
        {/* 다크모드 토글 기능 */}
        <div className={styles.sidebarFooter}>
            <div className={styles.settingItem}>
                <span>테마</span>
                <button onClick={toggleTheme} className={styles.themeToggleButton}>
                    {currentTheme === 'light' ? 'Light Mode' : 'Dark Mode'}
                </button>
            </div>
            <button onClick={onClose} className={styles.closeButton}>닫기</button>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;