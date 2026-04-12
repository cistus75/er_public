"use client";

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Image from 'next/image';
import Link from 'next/link'; // ✨ Link 컴포넌트 추가
import Sidebar from './components/Sidebar'; // ✨ Sidebar 컴포넌트 임포트느려허접커커커위위위커커커
import AnnouncementBar from './components/AnnouncementBar';

export default function ClientLayout({ children }) {
  const [nickname, setNickname] = useState('');
  const [showModal, setShowModal] = useState(false);
  const router = useRouter();
  const [theme, setTheme] = useState(undefined);
  const [isSidebarOpen, setSidebarOpen] = useState(false);

  useEffect(() => {
    const savedTheme = localStorage.getItem('theme') || 'light';
    setTheme(savedTheme);
  }, []);

  useEffect(() => {
    if (theme) {
      document.documentElement.className = theme;
      localStorage.setItem('theme', theme);
    }
  }, [theme]);

  const handleSubmit = (event) => {
    event.preventDefault();
    if (nickname.trim()) {
      router.push(`/dashboard?nickname=${encodeURIComponent(nickname.trim())}`);
    } else {
      setShowModal(true);
    }
  };

  const toggleTheme = () => {
    setTheme(theme === 'light' ? 'dark' : 'light');
  };
  // ✨ 사이드바를 열고 닫는 함수
  const openSidebar = () => setSidebarOpen(true);
  const closeSidebar = () => setSidebarOpen(false);

  if (theme === undefined) {
    return null;
  }
  
  return (
    <div>
      <div className="layout-wrapper">
        <header style={{ paddingLeft: '5px', paddingRight: '20px' }}>
          <div className='left' style={{ marginTop: '20px' }}>
            <Link href="/"> {/* ✨ Link 컴포넌트로 Image를 감싸고 href를 메인 페이지('/')로 설정 */}
              <Image
                src="/miro_logo.png" // ✨ public 폴더의 파일을 직접 가리키도록 수정
                alt="miro logo"
                width={50}
                height={50}
                className="logo"
                style={{ objectFit: "contain" }}
                unoptimized={true}
              />
            </Link>
          </div>
          <div className='center'>
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
          <div className='right'>
            <button onClick={openSidebar} className="darkmode-button">
              <Image
                src={theme === 'dark' ? '/menu_white.png' : '/menu_black.png'}
                alt="dark mode"
                width={40}
                height={40}
                style={{ objectFit: "contain" }}
                unoptimized={true}
              />
            </button>
          </div>
        </header>
        <div className='announcement-area'>
          <AnnouncementBar/>
        </div>

        <main className="content">
          {children}
        </main>

        <footer>
          <div className="copyright">
            이 사이트는 이터널 리턴의 API를 활용해 제작되었으며,&nbsp; 
            <a href="https://support.playeternalreturn.com/hc/ko/articles/49090866623257-API" target="_blank" rel="noopener noreferrer">
              API 이용 약관
            </a>
            을 준수하고 있습니다.  상세한 정보는&nbsp;
            <a href="https://support.playeternalreturn.com/hc/ko/articles/49090866623257-API" target="_blank" rel="noopener noreferrer">
                공식 개발자 페이지
            </a>
            에서 확인하실 수 있습니다.
          </div>
        </footer>
      </div>

      {showModal && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-lg shadow-xl dark:bg-gray-800 text-center">
            <h3 className="text-lg font-bold text-gray-900 dark:text-gray-100 mb-4">입력 오류</h3>
            <p className="text-sm text-gray-500 dark:text-gray-400 mb-6">분석할 닉네임을 입력해주세요.</p>
            <button
              onClick={() => setShowModal(false)}
              className="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 transition-colors"
            >
              닫기
            </button>
          </div>
        </div>
      )}

      {/* ✨ Sidebar 컴포넌트 렌더링 및 props 전달 */}
      <Sidebar
        isOpen={isSidebarOpen}
        onClose={closeSidebar}
        currentTheme={theme}
        toggleTheme={toggleTheme}
      />
      
    </div>
  );
}