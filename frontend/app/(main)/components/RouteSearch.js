import React, { useState } from 'react';
import styles from './RouteSearch.module.css'

function RouteSearch({ onSearch }) {
  const [inputNumber, setInputNumber] = useState('');

  function handleSubmit(e) {
    e.preventDefault(); // form의 기본 새로고침 동작 방지
    onSearch(inputNumber);
  }

  return (
    <form onSubmit={handleSubmit} className={styles.searchForm}>
      <input 
        type="number" 
        value={inputNumber}
        onChange={(e) => setInputNumber(e.target.value)}
        placeholder="루트 번호를 입력하세요"
        className={styles.searchInput}
      />
      <button type="submit" className={styles.searchBtn}>검색</button>
    </form>
  );
}

export default RouteSearch;