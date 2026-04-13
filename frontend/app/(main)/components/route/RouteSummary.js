'use client';
import Image from 'next/image';
import { rankImgs } from '@/public/rank/rankImgs';
import styles from './Routes.module.css'

// 날짜 포맷팅 헬퍼 함수
function formatDate(epochTime) {
  if (!epochTime) return '알 수 없음';

  // ✨ 수정: API가 이미 밀리초(ms) 단위로 값을 주므로 * 1000을 제거합니다.
  const date = new Date(epochTime); 
  
  return date.toLocaleString('ko-KR', { 
    year: 'numeric', month: '2-digit', day: '2-digit', 
    hour: '2-digit', minute: '2-digit' 
  });
}

// ✨ 객체일 수 있는 값을 안전하게 텍스트로 변환하는 헬퍼 함수
function getDisplayValue(value, fallback = 'N/A') {
    if (value === null || value === undefined) {
        return fallback;
    }
    // 값이 객체이고 내부에 'value'나 'average' 같은 속성이 있다면 그것을 사용
    if (typeof value === 'object') {
        return value.value || value.average || JSON.stringify(value);
    }
    // 객체가 아니면(숫자나 문자열) 그대로 반환
    return value;
}

export default function RouteSummary({ data }) {
  if (!data) return null;

  const tierImageSrc = rankImgs[data.creatorTier?.toLowerCase()] || rankImgs["unrank"];

  return (
    <section className={styles.sec}>
      <h2 style={{ fontSize: '1.8rem', margin: '0 0 1.5rem 0' }}>
        {data.routeName || '이름 없는 루트'}
      </h2>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '1rem' }}>
        
        {/* 제작자 티어 */}
        <div>
          <p style={{ margin: 0 }}>제작자</p>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '1.2rem' }}>
            <Image src={tierImageSrc} alt={`${data.creatorTier} 티어`} width={24} height={24} />
            {/* <span style={{ textTransform: 'capitalize' }}>{getDisplayValue(data.creatorTier)}</span> */}
          </div>
        </div>
        
        {/* 루트 승률 (안전하게 값 표시) */}
        <div>
          <p style={{ margin: 0 }}>승률</p>
          <p style={{ margin: 0, fontSize: '1.2rem', fontWeight: 'bold' }}>{getDisplayValue(data.winRate)}%</p>
        </div>
        
        {/* 루트 추천수 (안전하게 값 표시) */}
        <div>
          <p style={{ margin: 0 }}>추천</p>
          <p style={{ margin: 0, fontSize: '1.2rem', fontWeight: 'bold' }}>{getDisplayValue(data.likes)}</p>
        </div>
        
        {/* 최종 업데이트 */}
        <div>
          <p style={{ margin: 0 }}>최종 업데이트</p>
          <p style={{ margin: 0, fontSize: '1.2rem' }}>{formatDate(data.lastUpdated)}</p>
        </div>
      </div>
    </section>
  );
}
