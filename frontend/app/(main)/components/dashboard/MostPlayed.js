import Image from 'next/image';
import styles from './MostPlayed.module.css';
import { getCharacterInfo } from '@/lib/characterData';

export default function MostPlayed({ characters }) {

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
