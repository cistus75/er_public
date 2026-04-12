import Image from "next/image";

export default function MaintenancePage() {
  return (
    <div style={styles.container}>
      <div style={styles.content}>
        {/* 이미지 영역 */}
        <div style={styles.imageWrapper}>
          <Image 
            // ✅ 파일명 변경: fix_adina.png (확장자가 jpg라면 .jpg로 바꿔주세요)
            src="/images/fix_adina.png"
            alt="수리 중인 아디나"
            width={180} 
            height={180}
            priority 
          />
        </div>

        {/* 텍스트 영역 */}
        <h1 style={styles.title}>운명을 재계산 중입니다...</h1>
        
        <p style={styles.description}>
          "별의 흐름이 바뀌어 시스템을 수정하고 있어요."
        </p>
        
        <div style={styles.messageBox}>
          <p style={styles.text}>
            백엔드 구조를 일부 수정하는 중입니다. 
          </p>
          <p style={styles.subText}>
            (기존 백엔드 구조 일부 수정 중)
          </p>
          <p style={styles.footerText}>
            빠르게 작업을 마치고 다시 돌아오겠습니다!<br />
            조금만 기다려주세요.
          </p>
        </div>
      </div>
    </div>
  );
}

// 스타일 (배경색 등은 아디나와 어울리는 톤 유지)
const styles = {
  container: {
    minHeight: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#15161f", 
    color: "#ffffff",
    padding: "20px",
  },
  content: {
    maxWidth: "500px",
    textAlign: "center",
  },
  imageWrapper: {
    marginBottom: "30px",
    display: "flex",
    justifyContent: "center",
  },
  title: {
    fontSize: "2rem",
    fontWeight: "800",
    marginBottom: "10px",
    color: "#FCD34D", // 별 색깔(노랑) 포인트
  },
  description: {
    fontSize: "1.3rem",
    fontStyle: "italic",
    marginBottom: "30px",
    color: "#c7d2fe",
  },
  messageBox: {
    backgroundColor: "rgba(255, 255, 255, 0.05)",
    padding: "30px",
    borderRadius: "15px",
    border: "1px solid rgba(255, 255, 255, 0.1)",
  },
  text: {
    fontSize: "1rem",
    lineHeight: "1.6",
    marginBottom: "10px",
  },
  subText: {
    fontSize: "0.85rem",
    color: "#9ca3af",
    marginBottom: "20px",
  },
  footerText: {
    fontWeight: "bold",
    color: "#ffffff",
  },
};