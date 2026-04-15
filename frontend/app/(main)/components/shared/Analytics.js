// frontend/app/components/Analytics.js (전체 수정본)

'use client'

import Script from 'next/script'

export default function Analytics() {
  const gaId = process.env.NEXT_PUBLIC_GA_ID;

  if (!gaId) {
    return null;
  }
  return (
    <>
      <Script
        strategy="afterInteractive" // ✨ 'lazyOnload'에서 변경
        src={`https://www.googletagmanager.com/gtag/js?id=${gaId}`}
      />
      <Script id="ga-analytics" strategy="afterInteractive"> {/* ✨ 'lazyOnload'에서 변경 */}
        {`
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());

          gtag('config', '${gaId}');
        `}
      </Script>
    </>
  )
}