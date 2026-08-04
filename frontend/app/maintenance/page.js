import Image from "next/image";

export default function MaintenancePage() {
  return (
    <div style={styles.container}>
      <div style={styles.content}>
        <div style={styles.imageWrapper}>
          <Image 
            src="/images/fix_adina.png"
            alt="수리 중인 아디나"
            width={180} 
            height={180}
            priority 
          />
        </div>

        <h1 style={styles.title}>운명을 재계산 중입니다...</h1>
        
        <p style={styles.description}>
          "별의 흐름이 바뀌어 시스템을 수정하고 있어요."
        </p>
        
        <div style={styles.messageBox}>
          <p style={styles.text}>
            API 이슈로 서비스를 일시적으로 중단합니다.
          </p>
          <p style={styles.subText}>
            (LLM api 작업 중...)
          </p>
          <p style={styles.footerText}>
            솔직히 언제 될진 모르겠습니다. 쌀먹의 한계라서요.<br />
            광고 없이 서비스를 제공하려니 문제가 좀 생기네요.<br />
            가능한 빠르게 작업을 마치고 다시 돌아오겠습니다.
          </p>
        </div>
      </div>
    </div>
  );
}

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
    color: "#FCD34D",
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
