import { NextResponse } from 'next/server';

export async function GET() {
  const rawBaseUrl = process.env.NEXT_PUBLIC_FASTAPI_BASE_URL || '';
  const healthCheckUrl = `${rawBaseUrl.replace(/\/$/, '')}/health`


  try {
    await fetch(healthCheckUrl);
    
    return NextResponse.json({ status: 'ok', message: 'Backend pinged successfully' });

  } catch (error) {
    console.error('Error pinging backend:', error);
    return NextResponse.json({ status: 'error', message: 'Error pinging backend' }, { status: 500 });
  }
}
