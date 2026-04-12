// app/maintenance/layout.js

export const metadata = {
  title: "점검 중 - 시스템 재구축",
  robots: "noindex, nofollow", // 검색엔진 수집 차단
};

export default function MaintenanceLayout({ children }) {
  return (
    <html lang="ko">
      <body style={{ margin: 0, padding: 0, backgroundColor: "#15161f" }}>
        {children}
      </body>
    </html>
  );
}