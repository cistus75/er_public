// 클라이언트 컴포넌트로 선언하여 useState, useRouter 등의 훅 사용 가능
"use client";

import { useState } from 'react';
import { useRouter } from 'next/navigation'; // useRouter 훅 임포트
import Image from "next/image";
import styles from "./page.module.css"; // CSS 모듈 사용 시

export default function Home() {
  const [nickname, setNickname] = useState(''); // 닉네임 입력값을 위한 상태
  const router = useRouter(); // useRouter 훅 초기화
  
  // 폼 제출 핸들러 함수
  const handleSubmit = (event) => {
    event.preventDefault(); // 기본 폼 제출 동작(페이지 새로고침) 방지

    if (nickname.trim()) { // 닉네임이 비어있지 않은지 확인
      // dashboard 페이지로 이동하면서 닉네임을 쿼리 파라미터로 전달
      router.push(`/dashboard?nickname=${encodeURIComponent(nickname.trim())}`);
    } else {
      alert("분석할 닉네임을 입력해주세요.");
    }
  };

  return (
    <div className="content">
      {/* 폼에 onSubmit 핸들러 추가 */}
      <form onSubmit={handleSubmit} className={styles.searchForm}>
        <input
          type="text"
          className={styles.searchInput}
          placeholder="분석할 닉네임을 입력하세요"
          value={nickname} // input의 value를 상태와 연결
          onChange={(e) => setNickname(e.target.value)} // 입력값 변경 시 상태 업데이트
          required // 필수 입력 필드로 지정
        />
        <input type="submit" className={styles.submitBtn} value="분석하기" />
      </form>
    </div>
  );
}