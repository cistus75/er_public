/**
 * lib/api/routeApi.js
 * 인프라 계층 — 루트(Route) 관련 API 함수 모음.
 */

import { apiClient } from './client';

/**
 * 루트 ID로 루트 데이터를 조회합니다.
 * @param {string|number} routeId
 * @returns {Promise<object>}
 */
export async function getRouteById(routeId) {
  return apiClient(`/api/routes/${routeId}`);
}
