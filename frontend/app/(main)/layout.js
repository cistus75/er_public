// frontend/app/layout.js (전체 수정본)

import { Analytics as VercelAnalytics } from '@vercel/analytics/react';
import Analytics from './components/Analytics'; // Google Analytics 컴포넌트
import localFont from "next/font/local";
import ClientLayout from "./ClientLayout";
import "../globals.css";

const geistSans = localFont({
  src: "./fonts/GeistVF.woff",
  variable: "--font-geist-sans",
  weight: "100 900",
});
const geistMono = localFont({
  src: "./fonts/GeistMonoVF.woff",
  variable: "--font-geist-mono",
  weight: "100 900",
});

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <head>
        {/* 👇 이 부분을 추가해주세요 */}
        <script src="https://cdn.tailwindcss.com"></script>
      </head>
      <body className={`${geistSans.variable} ${geistMono.variable}`}>
        <ClientLayout>
          {children}
        </ClientLayout>
        
        {/* 분석 스크립트들을 body 태그가 끝나기 직전에 추가합니다. */}
        <VercelAnalytics />
        <Analytics />
      </body>
    </html>
  );
}