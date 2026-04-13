/**
 * lib/api/userApi.js
 * 인프라 계층 — 유저 관련 API 함수 모음.
 */

import { apiClient } from './client';

/**
 * 닉네임으로 유저 ID를 조회합니다.
 * @param {string} nickname
 * @returns {Promise<number>} userId
 */
export async function getUserId(nickname) {
  const data = await apiClient(`/api/users/num/${encodeURIComponent(nickname)}`);
  return data.userId;
}

/**
 * 유저 ID로 전체 통계를 조회합니다.
 * @param {number} userId
 * @returns {Promise<object>} userStatData
 */
export async function getUserStat(userId) {
  return apiClient(`/api/users/stat/${userId}`);
}
