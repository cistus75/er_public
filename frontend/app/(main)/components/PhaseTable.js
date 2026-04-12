// CSS 모듈 파일을 다시 임포트합니다.
import styles from './StatTable.module.css';

// 개별 스탯 행(row)을 렌더링하는 헬퍼 함수
// styles 객체를 인자로 받아 className을 적용합니다.
const renderStatRows = (data, styles) => {
  if (!data || data.length === 0) {
    return (
      <tr className={styles.tr}>
        <td colSpan="2" className={`${styles.td} ${styles.noData}`}>데이터가 없습니다.</td>
      </tr>
    );
  }

  return data.map((item, index) => {
    let comparisonElement = null;
    let colorClass = ''; // 스타일 객체가 아닌 클래스명 문자열

    if (item.baseValue !== undefined && item.baseValue !== null) {
      const currentValue = parseFloat(String(item.value).replace(/[^0-9.-]+/g, ""));
      const baseValue = parseFloat(String(item.baseValue).replace(/[^0-9.-]+/g, ""));

      if (!isNaN(currentValue) && !isNaN(baseValue)) {
        const diff = currentValue - baseValue;

        if (diff !== 0) {
          const sign = diff > 0 ? '+' : '';
          
          const lowerIsBetter = ['평균 사망', '평균 순위', '평균 받은 피해량'];
          const isLowerBetterStat = lowerIsBetter.includes(item.label);

          if ((diff > 0 && !isLowerBetterStat) || (diff < 0 && isLowerBetterStat)) {
            colorClass = styles.positive; // .positive 클래스
          } else {
            colorClass = styles.negative; // .negative 클래스
          }

          comparisonElement = (
            // className을 사용하도록 수정
            <span className={`${styles.comparison} ${colorClass}`}>
              ({sign}{diff.toFixed(2)})
            </span>
          );
        }
      }
    }

    return (
      <tr key={`${item.label}-${index}`} className={styles.tr}>
        <td className={`${styles.td} ${styles.statLabel}`}>{item.label}</td>
        <td className={`${styles.td} ${styles.statValue}`}>
          {comparisonElement}
          <span className={styles.statValueSpan}>{item.value}</span>
        </td>
      </tr>
    );
  });
};

export default function PhaseTable({ title, data, tooltipText }) {

  // style 속성 대신 className을 사용하고, 
  // <table> 구조 대신 <button>과 <table>을 분리합니다.
  return (
    <div className={styles.tableContainer}>
      <div className={styles.titleContainer}>
        {/* 툴팁 <span>을 <h3>의 자식으로 이동시켰습니다. */}
        <h3 className={styles.tableTitle}>
          {title}
          {tooltipText && (
            <span className={styles.tooltip}>{tooltipText}</span>
          )}
        </h3>
      </div>

      <div className={styles.tableWrapper}>
        {/* --- 수정된 부분: 데이터가 비었을 때와 아닐 때를 분기 --- */}
        {data.length === 0 ? (
          // 모든 데이터가 비어있으면 "데이터가 없습니다."만 표시
          <table className={styles.statTable}>
            <tbody>
              {renderStatRows([], styles)}
            </tbody>
          </table>
        ) : (
          // 데이터가 하나라도 있으면 기존 로직 수행
          <>
            {/* Core Stats (항상 표시) */}
            <table className={styles.statTable}>
              <tbody>
                {/* core 데이터가 없으면 여기서 "데이터가 없습니다." 표시됨 */}
                {renderStatRows(data, styles)}
              </tbody>
            </table>
          </>
        )}
        {/* ----------------------------------------- */}
      </div>
    </div>
  );
}