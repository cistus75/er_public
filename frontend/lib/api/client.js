function getBaseUrl() {
  return (process.env.NEXT_PUBLIC_FASTAPI_BASE_URL ?? '').replace(/\/$/, '');
}

export async function apiClient(endpoint, options = {}) {
  const url = `${getBaseUrl()}${endpoint}`;
  const res = await fetch(url, options);

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `API 오류: ${res.status}`);
  }

  return res.json();
}
