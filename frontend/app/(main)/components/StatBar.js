import styles from './StatBar.module.css';

export default function StatBar({ label, value, max, unit }) {
  return (
    <div className={styles.statBlock}>
      <span className={styles.label}>{label}</span>
      <div className={styles.barWrapper}>
        <div className={styles.barFill} style={{ width: `${value/max*100}%` }}></div>
      </div>
      <span className={styles.value}>{value === 0 ? '-' : `${value.toFixed(1)}${unit}`}</span>
    </div>
  );
}