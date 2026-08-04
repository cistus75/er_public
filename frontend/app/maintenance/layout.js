
export const metadata = {
  title: "아디나의 수정구슬 | 미로",
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
