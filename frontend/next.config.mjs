/** @type {import('next').NextConfig} */
const nextConfig = {
  // 이 곳에 Next.js 14 버전에 필요한 설정들을 추가하세요.
  
  // Vercel Analytics를 사용하기 위한 설정
  analyticsId: process.env.VERCEL_ANALYTICS_ID,
  // 예시:
  // experimental: {
  //   serverActions: true, // App Router에서 서버 액션을 사용하려면 필요할 수 있습니다.
  // },
  // images: {
  //   remotePatterns: [ // 외부 이미지 사용 시 도메인 설정
  //     {
  //       protocol: 'https',
  //       hostname: 'example.com',
  //     },
  //   ],
  // },
  // output: 'standalone', // Docker 등으로 배포 시 유용
  // ... 기타 설정들
};

export default nextConfig;