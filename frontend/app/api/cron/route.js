// app/api/cron/route.ts
import { NextResponse } from 'next/server';

export async function GET() {
  // 환경 변수에서 백엔드 헬스체크 URL을 가져옵니다.
  const rawBaseUrl = process.env.NEXT_PUBLIC_FASTAPI_BASE_URL || '';
  const healthCheckUrl = `${rawBaseUrl.replace(/\/$/, '')}/health`


  try {
    // 백엔드로 헬스체크 요청 전송
    await fetch(healthCheckUrl);
    
    // 성공 응답 반환
    return NextResponse.json({ status: 'ok', message: 'Backend pinged successfully' });

  } catch (error) {
    console.error('Error pinging backend:', error);
    return NextResponse.json({ status: 'error', message: 'Error pinging backend' }, { status: 500 });
  }
}