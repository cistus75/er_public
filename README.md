# 아디나의 수정구슬
### 이터널 리턴 최근 전적 분석 서비스

> 최근 전적 기반의 실시간 지표 분석과 AI 개인화 피드백을 제공하는 웹 서비스

>  본 레포는 테스트 서버 및 포트폴리오용으로 정리된 버전입니다.

**개발 기간** : 2025.05 ~ 2026.05.17 <br>
**운영 기간** : 2025.08.29 ~ 2026.05.17

<br>

## Tech Stack

**Frontend**
![Next.js](https://img.shields.io/badge/Next.js_14-000000?style=flat-square&logo=nextdotjs&logoColor=white)
![React](https://img.shields.io/badge/React_18-61DAFB?style=flat-square&logo=react&logoColor=black)
![CSS](https://img.shields.io/badge/CSS-1572B6?style=flat-square&logo=css3&logoColor=white)
![Chart.js](https://img.shields.io/badge/Chart.js-FF6384?style=flat-square&logo=chartdotjs&logoColor=white)

**Backend**
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python_3-3776AB?style=flat-square&logo=python&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=flat-square&logo=mongodb&logoColor=white)

**AI & External API**
![Gemini](https://img.shields.io/badge/Google_Gemini-8E75B2?style=flat-square&logo=googlegemini&logoColor=white)

**Deploy**
![Vercel](https://img.shields.io/badge/Vercel-000000?style=flat-square&logo=vercel&logoColor=white)
![Render](https://img.shields.io/badge/Render-46E3B7?style=flat-square&logo=render&logoColor=black)

<br>

## 프로젝트 배경

기존의 주류 전적 검색 사이트는 **시즌 전체 통합 전적**을 기준으로 지표를 제공합니다.
이로 인해 시즌이 변경된 이후 하위 티어에서 플레이한 기록이 함께 집계되어, 현재 실력과 맞지 않는 부정확한 지표가 노출되는 문제가 있습니다.

이 프로젝트는 **최근 전적만을 기준으로 정확한 지표를 제공**하고, AI를 통한 개인화된 피드백으로 실질적인 플레이 개선을 돕기 위해 제작되었습니다.

<br>

## 주요 기능

- **전적 검색** : 닉네임 기반의 최근 전적 조회
- **지표 시각화** : KDA, 승률, 픽률 등 주요 지표를 차트로 시각화
- **AI 기반 피드백** : 전적 데이터를 분석하여 개인화된 플레이 개선 피드백 제공
- **뱃지 시스템** : 전적 기반의 업적/뱃지 부여 시스템

<br>

## 사이트 스크린샷

| 메인 | 로딩 | 분석 결과 |
|------|------|------|
| <img width="400" src="https://github.com/user-attachments/assets/0f356864-4495-40f5-a379-930492f9b6f1" /> | <img width="400" src="https://github.com/user-attachments/assets/c40ea309-ff5c-43ba-85de-edd1b43d319f" /> | <img width="400" src="https://github.com/user-attachments/assets/c29604bc-53fc-4010-9b28-d1e5fff0dfd4" /> |
| 닉네임 검색 페이지 | 데이터 로딩 화면 | 전적 분석 결과 페이지 |

| 상세 지표 | 사이드바 | 뱃지 도감 | 패치노트 |
|------|------|------|------|
| <img width="300" src="https://github.com/user-attachments/assets/495c0a49-8a80-4db3-a475-006181009ae6" /> | <img width="300" src="https://github.com/user-attachments/assets/4cbc87c0-ba28-4209-bc40-489ecd7ed62c" /> | <img width="300" src="https://github.com/user-attachments/assets/da7ed5a5-fab5-4584-9d88-224fd9453544" /> | <img width="300" src="https://github.com/user-attachments/assets/85557840-7216-4f6d-8a08-34df652f41cd" /> |
| 상세 지표 비교 | 추가 메뉴 | 뱃지 획득 조건 | 게임 업데이트 내역 |


<br>

## 서비스 현황

> 서비스 종료 기준 누적 활성 유저 **2.6만 명** (2025.05 ~ 2026.05)

<img width="2035" height="341" alt="유저수" src="https://github.com/user-attachments/assets/6d01d135-bcb6-4b76-ae0a-c341fcac765d" />

<br>

## 🔧 트러블슈팅

### 1. 계층적 아키텍처 도입을 통한 리팩토링
- **문제** : `main.py`에 대부분의 기능이 집중되어 코드가 비대해지고, 팀원 간 병합 과정에서 다량의 충돌 및 롤백이 발생해 생산성이 저하됨
- **해결** : SoC 원칙에 따라 `common` / `db` / `core` / `services` 계층으로 모듈화
- **결과** : `main.py`는 모듈 연결 역할만 수행하게 되어 병합 충돌 및 생산성 저하 이슈 해결

---

### 2. 외부 API 변경으로 인한 데이터 수집기 구조 개편
- **문제** : 공식 API가 불변값인 `userNum` 방식에서 가변값인 `userId` 방식으로 변경되어 기존 스노우볼링 방식의 수집기가 완전히 마비됨
- **해결** : 매치마다 1씩 증가하는 불변값인 `gameId`를 활용해 최신 gameId부터 역순으로 수집하는 브루트포스 방식으로 재설계
- **결과** : 수집기 마비 문제를 해결하고, 기존의 상위권 지표 편향 문제까지 해소하여 데이터 일반성 향상

---

### 3. 예산 제약 상황에서의 비용 최적화
- **문제** : 수익원 없이 고정 서버비와 AI API 비용을 감당해야 했으며, Render 무료 플랜의 절전 모드로 인해 사용자 속도 저하 발생
- **해결** : 인프라 전체를 Vercel / Render / MongoDB 무료 플랜으로 구성. AI API 비용은 Google 프로모션 크레딧으로 충당하고, 크레딧 만료 후 다수의 무료 플랜 키로 대응. Uptime 봇으로 주기적 핑을 전송해 서버 절전 방지
- **결과** : 비용 없이 서비스 운영, 절전 모드로 인한 사용자 불편 해소

---

### 4. 운영 / 테스트 환경 분리
- **문제** : 무료 플랜의 단일 서버 제약으로 라이브 서버에 직접 배포 및 테스트를 진행하여 유저에게 버그 노출 및 서버 중단 이슈가 발생함
- **해결** : 계정을 물리적으로 분리해 별도의 테스트 서버를 구축하고, QA를 통과한 코드만 라이브 환경에 배포하는 프로세스 수립
- **결과** : 치명적 버그의 라이브 배포 차단, 피크 타임 점검 시간 최소화

---

### 5. AI API Rate Limit 우회
- **문제** : AI API 마이그레이션 및 유저 수 증가로 요청 한도 초과 문제 발생
- **해결** : 다수의 무료 플랜 API 키를 확보하여 라운드 로빈 방식으로 분배하고, 실패 시 다음 키로 자동 재시도하는 로직 구현
- **결과** : 추가 비용 없이 AI 기능을 안정적으로 서비스

---

### 6. 로딩 속도 개선
- **문제** : 로딩 단계가 지나치게 길어 사용자 이탈 발생
- **해결** : 로그를 통해 AI 분석 생성 단계가 병목 원인임을 확인. 지표 페이지 우선 로딩을 시도했으나 오히려 추가 대기가 발생해 UX상 이점이 없다고 판단. 대신 로딩 화면에 게임 TMI를 표시하여 대기 시간의 지루함을 최소화하는 방향으로 해결
- **결과** : 로딩 대기로 인한 사용자 이탈 현상 감소

<br>

## 서비스 종료

팀원 중 한 명의 입대와 나머지 개발자의 학업 일정 과중으로 지속적인 서비스 관리가 어려워짐. 수익 없이 AI API를 무료로 제공하던 방식이 반복적인 마이그레이션으로 한계에 도달하여 서비스를 종료함.


## 개발자

| [cistus75](https://github.com/cistus75) |
|:------|
| 백엔드 · 기획 · 운영 · QA · CS |

| [mileuTheDeveloper](https://github.com/mileuTheDeveloper) |
|:------|
| 프론트엔드 · 운영 · QA |
