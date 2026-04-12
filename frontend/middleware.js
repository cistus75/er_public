// frontend/middleware.js

import { NextResponse } from 'next/server';

export function middleware(request) {
  const ip = request.ip || request.headers.get('x-forwarded-for');
  
  // 환경변수가 없으면 빈 배열 처리
  const bypassIps = process.env.MAINTENANCE_BYPASS_IPS?.split(',') || [];

  // 현재 요청하려는 주소
  const { pathname } = request.nextUrl;

  // 점검 모드 체크
  const isMaintenanceMode = process.env.MAINTENANCE_MODE === 'true';

  // [수정된 핵심 로직]
  // 1. 점검 모드가 켜져 있어야 함
  // 2. 내 IP가 우회 목록에 없어야 함
  // 3. 점검 페이지 자체가 아니어야 함
  // 4. ✨ 중요: 이미지 폴더(/images)는 납치하지 마!
  // 5. ✨ 중요: 넥스트 내부 시스템 파일(/_next)도 건드리지 마!
  if (
    isMaintenanceMode &&
    !bypassIps.includes(ip) &&
    !pathname.startsWith('/maintenance') &&
    !pathname.startsWith('/images') &&      // 👈 [해결사] 여기입니다!
    !pathname.startsWith('/_next') &&       // Next.js 시스템 파일 통과
    !pathname.startsWith('/favicon.ico')    // 파비콘 통과
  ) {
    const url = request.nextUrl.clone();
    url.pathname = '/maintenance';
    return NextResponse.rewrite(url);
  }

  return NextResponse.next();
}

// 미들웨어가 실행될 경로 범위 (이미지 등 정적 파일도 체크해야 하므로 범위 유지)
export const config = {
  matcher: '/:path*',
};