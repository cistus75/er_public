// frontend/app/(main)/layout.js

import { Analytics as VercelAnalytics } from '@vercel/analytics/react';
import Analytics from './components/Analytics';
import localFont from 'next/font/local';
import ClientLayout from './ClientLayout';
import '../globals.css';

const geistSans = localFont({
  src: './fonts/GeistVF.woff',
  variable: '--font-geist-sans',
  weight: '100 900',
});
const geistMono = localFont({
  src: './fonts/GeistMonoVF.woff',
  variable: '--font-geist-mono',
  weight: '100 900',
});

export default function RootLayout({ children }) {
  return (
    <html lang="ko">
      <body className={`${geistSans.variable} ${geistMono.variable}`}>
        <ClientLayout>{children}</ClientLayout>
        <VercelAnalytics />
        <Analytics />
      </body>
    </html>
  );
}