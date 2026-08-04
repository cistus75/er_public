"use client";

import React from 'react';
import styles from './Sidebar.module.css';
import Link from 'next/link';

const Sidebar = ({ isOpen, onClose, currentTheme, toggleTheme }) => {
  if (!isOpen) {
    return null;
  }

  return (
    <div className={styles.overlay} onClick={onClose}>
      <div className={styles.sidebar} onClick={(e) => e.stopPropagation()}>
        <h2 style={{all:'revert'}}>메뉴다요!</h2>
        <ul className={styles.sidebarList}>
          <li><Link href='/patchnotes'>패치노트</Link></li>
          <li><Link href='/badges'>뱃지 일람</Link></li>
          <li><Link href='https://eternity-tracker.vercel.app/'>이터니티 점수컷</Link></li>
          <li><Link href='https://forms.gle/E5YcNN7ZAwQJMVhh7'>문의/제보</Link></li>
        </ul>
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
