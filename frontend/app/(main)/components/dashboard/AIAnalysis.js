// AIAnalysis.js 수정된 코드

'use client';
import Image from 'next/image';
import styles from './AIAnalysis.module.css';

// 1. 함수의 인자로 'title'을 추가해줍니다.
export default function AIAnalysis({ title, analysis, loading, ver = 'adina' }) {
  
  return (
    <div className={styles.container}>
      <div className={styles.titleContainer}>
        <div className={styles.iconContainer}>
          <Image 
            src={ver == 'adina' ? "/images/ai_adina.png" : "/images/ai_bianca.png"}
            alt="AI Icon" 
            width={40} 
            height={40} 
            className={styles.titleIcon}
          />
          {/* 2. 하드코딩된 텍스트 대신 props로 받은 'title'을 사용합니다. */}
          <span className={styles.title}>{title}</span>
          <span className={styles.tooltip}>
            본 시스템은 매우 불안정하고, 신뢰성이 없는 순전 재미용임를 알립니다. AI의 한계로 인해 잘못된 정보를 제공할 수 있습니다.
          </span>
        </div>
        
      </div>
      <div className={styles.content}>
        {loading ? (
          <div className={styles.loading}>아디나가 분석 중이다요!</div>
        ) : (
          <p className={styles.analysisText}>{analysis}</p>
        )}
      </div>
    </div>
  );
}