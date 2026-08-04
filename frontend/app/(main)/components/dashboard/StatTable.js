import styles from './StatTable.module.css';

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
    let colorClass = '';

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
            colorClass = styles.positive;
          } else {
            colorClass = styles.negative;
          }

          comparisonElement = (
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

export default function StatTable({ title, data, tooltipText, 
  isDetailedVisible, onToggleDetailed, btnVisible = false }) {
  const { core = [], combat = [], operation = [], vision = [] } = data || {};

  const isAllDataEmpty = core.length === 0 && combat.length === 0 && operation.length === 0 && vision.length === 0;

  const arrowClassDetailed = isDetailedVisible 
    ? `${styles.arrow} ${styles.arrowOpen}` 
    : styles.arrow;

  return (
    <div className={styles.tableContainer}>
      <div className={styles.titleContainer}>
        <h3 className={styles.tableTitle}>
          {title}
          {tooltipText && (
            <span className={styles.tooltip}>{tooltipText}</span>
          )}
        </h3>
      </div>

      <div className={styles.tableWrapper}>
        {isAllDataEmpty ? (
          <table className={styles.statTable}>
            <tbody>
              {renderStatRows([], styles)}
            </tbody>
          </table>
        ) : (
          <>
            <table className={styles.statTable}>
              <tbody>
                {renderStatRows(core, styles)}
              </tbody>
            </table>

            {btnVisible ? <button 
              onClick={onToggleDetailed}
              className={styles.toggleButton}
            >
              상세 지표
              <span className={arrowClassDetailed}>
                ▼
              </span>
            </button> : <button className={styles.toggleButton}><span>&nbsp;</span></button>}
            
            {isDetailedVisible && (
              <table className={`${styles.statTable} ${styles.detailedStatsPanel}`}>
                <tbody className={styles.categoryBody}>
                  <tr className={styles.subheadingTr}>
                    <th colSpan="2" className={styles.subheading}>Combat</th>
                  </tr>
                  {renderStatRows(combat, styles)}
                </tbody>

                <tbody className={styles.categoryBody}>
                  <tr className={styles.subheadingTr}>
                    <th colSpan="2" className={styles.subheading}>Operation</th>
                  </tr>
                  {renderStatRows(operation, styles)}
                </tbody>
                <tbody className={styles.categoryBody}>
                  <tr className={styles.subheadingTr}>
                    <th colSpan="2" className={styles.subheading}>Vision</th>
                  </tr>
                  {renderStatRows(vision, styles)}
                </tbody>
              </table>
            )}
          </>
        )}
      </div>
    </div>
  );
}
