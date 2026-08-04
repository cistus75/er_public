'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Image from 'next/image';
import Link from 'next/link';
import { useTheme } from '@/hooks/useTheme';
import Sidebar from './components/shared/Sidebar';
import AnnouncementBar from './components/shared/AnnouncementBar';
import modalStyles from './ClientLayout.module.css';

export default function ClientLayout({ children }) {
  const [nickname, setNickname] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [isSidebarOpen, setSidebarOpen] = useState(false);
  const router = useRouter();

  const { theme, toggleTheme } = useTheme();

  const handleSubmit = (event) => {
    event.preventDefault();
    if (nickname.trim()) {
      router.push(`/dashboard?nickname=${encodeURIComponent(nickname.trim())}`);
    } else {
      setShowModal(true);
    }
  };

  const openSidebar = () => setSidebarOpen(true);
  const closeSidebar = () => setSidebarOpen(false);

  // 저장된 테마를 읽기 전에는 렌더링하지 않아 서버와 화면이 달라지는 문제를 막습니다.
  if (theme === undefined) {
    return null;
  }

  return (
    <div>
      <div className="layout-wrapper">
        <header style={{ paddingLeft: '5px', paddingRight: '20px' }}>
          <div className="left" style={{ marginTop: '20px' }}>
            <Link href="/">
              <Image
                src="/miro_logo.png"
                alt="miro logo"
                width={50}
                height={50}
                className="logo"
                style={{ objectFit: 'contain' }}
                unoptimized={true}
              />
            </Link>
          </div>
          <div className="center">
            <form onSubmit={handleSubmit} className="search-form-small">
              <input
                type="text"
                className="search-input-small"
                placeholder="닉네임을 입력하세요"
                value={nickname}
                onChange={(e) => setNickname(e.target.value)}
                required
              />
            </form>
          </div>
          <div className="right">
            <button onClick={openSidebar} className="darkmode-button">
              <Image
                src={theme === 'dark' ? '/menu_white.png' : '/menu_black.png'}
                alt="메뉴 열기"
                width={40}
                height={40}
                style={{ objectFit: 'contain' }}
                unoptimized={true}
              />
            </button>
          </div>
        </header>

        <div className="announcement-area">
          <AnnouncementBar />
        </div>

        <main className="content">{children}</main>

        <footer>
          <div className="copyright">
            이 사이트는 이터널 리턴의 API를 활용해 제작되었으며,&nbsp;
            <a
              href="https://support.playeternalreturn.com/hc/ko/articles/49090866623257-API"
              target="_blank"
              rel="noopener noreferrer"
            >
              API 이용 약관
            </a>
            을 준수하고 있습니다. 상세한 정보는&nbsp;
            <a
              href="https://support.playeternalreturn.com/hc/ko/articles/49090866623257-API"
              target="_blank"
              rel="noopener noreferrer"
            >
              공식 개발자 페이지
            </a>
            에서 확인하실 수 있습니다.
          </div>
        </footer>
      </div>

      {showModal && (
        <div className={modalStyles.modalOverlay}>
          <div className={modalStyles.modalBox}>
            <h3 className={modalStyles.modalTitle}>입력 오류</h3>
            <p className={modalStyles.modalText}>분석할 닉네임을 입력해주세요.</p>
            <button
              onClick={() => setShowModal(false)}
              className={modalStyles.modalButton}
            >
              닫기
            </button>
          </div>
        </div>
      )}

      <Sidebar
        isOpen={isSidebarOpen}
        onClose={closeSidebar}
        currentTheme={theme}
        toggleTheme={toggleTheme}
      />
    </div>
  );
}
