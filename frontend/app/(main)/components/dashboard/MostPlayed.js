import Image from 'next/image';
import styles from './MostPlayed.module.css';
// ✨ 1. 새로 만든 characterData.js 파일에서 헬퍼 함수를 import 합니다.
import { getCharacterInfo } from '@/lib/characterData';

// 'characters' 라는 이름으로 실제 데이터를 받아옵니다.
export default function MostPlayed({ characters }) {

  // 데이터가 없거나 비어있으면 안내 메시지를 표시합니다.
  if (!characters || !Array.isArray(characters) || characters.length === 0) {
    return (
      <div className={styles.container}>
        <h3 className={styles.title}>최근 모스트 3</h3>
        <p className={styles.noData}>최근 플레이 기록이 부족합니다.</p>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <h3 className={styles.title}>최근 모스트 3</h3>
      <div className={styles.charList}>
        {characters.map((charData, index) => {
          // ✨ 2. characterCode를 사용해 캐릭터 이름과 이미지 정보를 가져옵니다.
          const info = getCharacterInfo(charData.characterCode);

          return (
            <div key={index} className={styles.charCard}>
              <Image src={info.image} alt={info.name} width={70} height={70} className={styles.charImage} quality={100}/>
              
              <div className={styles.charInfo}>
                <div className={styles.rowTop}>
                  <span className={styles.charName}>{info.name}</span>
                  <span className={styles.charGames}>{charData.totalGames}판</span>
                </div>
                <div className={styles.rowBottom}>
                  {/* 백엔드에서 받아온 실제 데이터를 사용합니다. */}
                  <span>승률 {charData.winRate}%</span>
                  <span>Top 3 {charData.top3Rate || 'N/A'}%</span>
                  <span>평균 TK: {charData.avgTK || 'N/A'}</span>
                  <span>평균 딜량: {charData.avgDamage || 'N/A'}</span>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
