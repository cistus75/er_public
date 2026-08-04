import { NextResponse } from 'next/server';

export function middleware(request) {
  let ip = request.ip || request.headers.get('x-forwarded-for') || '127.0.0.1';
  if (ip.includes(',')) {
    ip = ip.split(',')[0].trim();
  }
  
  const { pathname } = request.nextUrl;

  const bypassIpsStr = process.env.MAINTENANCE_BYPASS_IPS || '';
  const bypassIps = bypassIpsStr ? bypassIpsStr.split(',').map(s => s.trim()).filter(Boolean) : [];
  const isMaintenanceMode = process.env.MAINTENANCE_MODE === 'true';

  if (
    isMaintenanceMode &&
    !bypassIps.includes(ip) &&
    !pathname.startsWith('/maintenance')
  ) {
    const maintenanceUrl = new URL('/maintenance', request.url);
    return NextResponse.rewrite(maintenanceUrl);
  }

  return NextResponse.next();
}

// 정적 파일과 시스템 경로는 점검 모드 리다이렉트 대상에서 제외합니다.
export const config = {
  matcher: [
    '/((?!api|_next/static|_next/image|favicon.ico|favicon.png|images|maintenance|robots.txt).*)',
  ],
};
