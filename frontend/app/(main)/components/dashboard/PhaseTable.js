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

export default function PhaseTable({ title, data, tooltipText }) {

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
        {data.length === 0 ? (
          <table className={styles.statTable}>
            <tbody>
              {renderStatRows([], styles)}
            </tbody>
          </table>
        ) : (
          <>
            <table className={styles.statTable}>
              <tbody>
                {renderStatRows(data, styles)}
              </tbody>
            </table>
          </>
        )}
      </div>
    </div>
  );
}
