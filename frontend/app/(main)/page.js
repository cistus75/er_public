"use client";

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Image from "next/image";
import styles from "./page.module.css";

export default function Home() {
  const [nickname, setNickname] = useState('');
  const router = useRouter();
  
  const handleSubmit = (event) => {
    event.preventDefault();

    if (nickname.trim()) {
      router.push(`/dashboard?nickname=${encodeURIComponent(nickname.trim())}`);
    } else {
      alert("분석할 닉네임을 입력해주세요.");
    }
  };

  return (
    <div className="content">
      <form onSubmit={handleSubmit} className={styles.searchForm}>
        <input
          type="text"
          className={styles.searchInput}
          placeholder="분석할 닉네임을 입력하세요"
          value={nickname}
          onChange={(e) => setNickname(e.target.value)}
          required
        />
        <input type="submit" className={styles.submitBtn} value="분석하기" />
      </form>
    </div>
  );
}
