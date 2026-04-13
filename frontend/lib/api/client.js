/**
 * lib/api/client.js
 * 인프라 계층 — 모든 외부 fetch 호출의 단일 진입점.
 * BASE_URL 조합, 공통 에러 파싱을 담당합니다.
 */

function getBaseUrl() {
  return (process.env.NEXT_PUBLIC_FASTAPI_BASE_URL ?? '').replace(/\/$/, '');
}

/**
 * @param {string} endpoint  — '/api/users/num/...' 형태의 경로
 * @param {RequestInit} [options]
 * @returns {Promise<any>}   — 파싱된 JSON 응답
 * @throws {Error}           — HTTP 에러 또는 네트워크 에러
 */
export async function apiClient(endpoint, options = {}) {
  const url = `${getBaseUrl()}${endpoint}`;
  const res = await fetch(url, options);

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `API 오류: ${res.status}`);
  }

  return res.json();
}
