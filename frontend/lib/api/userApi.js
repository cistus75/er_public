import { apiClient } from './client';

export async function getUserId(nickname) {
  const data = await apiClient(`/api/users/num/${encodeURIComponent(nickname)}`);
  return data.userId;
}

export async function getUserStat(userId) {
  return apiClient(`/api/users/stat/${userId}`);
}
