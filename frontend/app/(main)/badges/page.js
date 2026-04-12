// frontend/app/badges/page.js

import styles from "./page.module.css";
import clsx from 'clsx';
// 뱃지 데이터를 페이지 상단에 정의합니다.키위새는 멸종했다아마도아마도아마도
const badgeData = [
    { "group": "레벨 뱃지", "name": "신입 연구원", "tier": 1, "condition": "레벨 1 달성" },
    { "group": "레벨 뱃지", "name": "견습 연구원", "tier": 1, "condition": "레벨 30 달성" },
    { "group": "레벨 뱃지", "name": "정식 연구원", "tier": 1, "condition": "레벨 50 달성" },
    { "group": "레벨 뱃지", "name": "수석 연구원", "tier": 2, "condition": "레벨 100 달성" },
    { "group": "레벨 뱃지", "name": "알파 개발자", "tier": 2, "condition": "레벨 200 달성" },
    { "group": "레벨 뱃지", "name": "오메가 설계자", "tier": 3, "condition": "레벨 300 달성" },
    { "group": "레벨 뱃지", "name": "위클라인 관리자", "tier": 3, "condition": "레벨 400 달성" },
    { "group": "레벨 뱃지", "name": "영원한 탐구자", "tier": 4, "condition": "레벨 500 달성" },
    { "group": "레벨 뱃지", "name": "시작, 끝", "tier": 4, "condition": "레벨 600 달성" },

    { "group": "승률 뱃지", "name": "참가상", "tier": 1, "condition": "승률 0% 달성" },
    { "group": "승률 뱃지", "name": "연쇄 생존마", "tier": 1, "condition": "승률 10% 이상 달성" },
    { "group": "승률 뱃지", "name": "우승 청부사", "tier": 2, "condition": "승률 20% 이상 달성" },
    { "group": "승률 뱃지", "name": "그 긴거", "tier": 3, "condition": "승률 30% 이상 달성" },
    { "group": "승률 뱃지", "name": "전장의 설계자", "tier": 3, "condition": "승률 40% 이상 달성" },
    { "group": "승률 뱃지", "name": "시작이 반이다", "tier": 4, "condition": "승률 50% 이상 달성" },
    { "group": "승률 뱃지", "name": "오토암즈", "tier": 4, "condition": "승률 70% 이상 달성" },
    { "group": "승률 뱃지", "name": "레이더", "tier": 4, "condition": "승률 100% 달성" },

    { "group": "랭크 뱃지", "name": "사관 생도", "tier": 1, "condition": "골드 달성" },
    { "group": "랭크 뱃지", "name": "광물의 왕", "tier": 2, "condition": "미스릴 달성" },
    { "group": "랭크 뱃지", "name": "곰의 일족", "tier": 2, "condition": "데미갓 달성" },
    { "group": "랭크 뱃지", "name": "용의 일족", "tier": 3, "condition": "이터니티 달성" },
    { "group": "랭크 뱃지", "name": "하이 랭커", "tier": 3, "condition": "랭크 100위 이내" },
    { "group": "랭크 뱃지", "name": "찬탈자", "tier": 4, "condition": "랭크 10위 이내" },
    { "group": "랭크 뱃지", "name": "천상천하 유아독존", "tier": 4, "condition": "랭크 1위 달성" },

    { "group": "MMR 뱃지", "name": "브론즈", "tier": 1, "condition": "브론즈 티어 달성" },
    { "group": "MMR 뱃지", "name": "실버", "tier": 1, "condition": "실버 티어 달성" },
    { "group": "MMR 뱃지", "name": "골드", "tier": 1, "condition": "골드 티어 달성" },
    { "group": "MMR 뱃지", "name": "플래", "tier": 2, "condition": "플래티넘 티어 달성" },
    { "group": "MMR 뱃지", "name": "다이아", "tier": 2, "condition": "다이아 티어 달성" },
    { "group": "MMR 뱃지", "name": "메라", "tier": 3, "condition": "메테오라이트 티어 달성" },
    { "group": "MMR 뱃지", "name": "미스릴", "tier": 3, "condition": "미스릴 티어 달성" },
    { "group": "MMR 뱃지", "name": "데미갓", "tier": 4, "condition": "데미갓 달성" },
    { "group": "MMR 뱃지", "name": "이터니티", "tier": 4, "condition": "이터니티 달성" },
    { "group": "MMR 뱃지", "name": "만점 클럽", "tier": 4, "condition": "MMR 10,000점 이상" },

    { "group": "KDA 뱃지", "name": "무력의 증명", "tier": 1, "condition": "KDA 2.0 이상 달성" },
    { "group": "KDA 뱃지", "name": "섬의 종결자", "tier": 2, "condition": "KDA 3.0 이상 달성" },
    { "group": "KDA 뱃지", "name": "루미아의 지배자", "tier": 3, "condition": "KDA 4.0 이상 달성" },
    { "group": "KDA 뱃지", "name": "플래닛 킬러", "tier": 4, "condition": "KDA 5.0 이상 달성" },

    { "group": "어시스트 뱃지", "name": "협력자", "tier": 2, "condition": "평균 어시스트 3회 이상" },
    { "group": "어시스트 뱃지", "name": "최고의 서포터", "tier": 3, "condition": "평균 어시스트 4회 이상" },
    { "group": "어시스트 뱃지", "name": "진정한 지원가", "tier": 4, "condition": "평균 어시스트 5회 이상" },

    { "group": "사망 뱃지", "name": "좀비", "tier": 1, "condition": "평균 데스 3회 이상" },
    { "group": "사망 뱃지", "name": "불사 대마왕", "tier": 4, "condition": "죽음을 거부하기" },

    { "group": "팀 킬 뱃지", "name": "최초의 살인자", "tier": 1, "condition": "평균 팀 킬 3.0 이상" },
    { "group": "팀 킬 뱃지", "name": "세븐 폴드", "tier": 2, "condition": "평균 팀 킬 6.0 이상" },
    { "group": "팀 킬 뱃지", "name": "트럭 운전수", "tier": 3, "condition": "평균 팀 킬 9.0 이상" },
    { "group": "팀 킬 뱃지", "name": "안젤라 윈슬레어", "tier": 4, "condition": "평균 팀 킬 12.0 이상" },
    { "group": "팀 킬 뱃지", "name": "잭 더 리퍼", "tier": 4, "condition": "평균 팀 킬 15.0 이상" },

    { "group": "생존 시간 뱃지", "name": "스피드 러너", "tier": 1, "condition": "평균 게임 시간 7분 미만" },
    { "group": "생존 시간 뱃지", "name": "루미아 관광객", "tier": 1, "condition": "평균 게임 시간 7분 이상" },
    { "group": "생존 시간 뱃지", "name": "루미아 유학생", "tier": 2, "condition": "평균 게임 시간 10분 이상" },
    { "group": "생존 시간 뱃지", "name": "루미아 현지인", "tier": 2, "condition": "평균 게임 시간 13분 이상" },
    { "group": "생존 시간 뱃지", "name": "루미아 원주민", "tier": 3, "condition": "평균 게임 시간 16분 이상" },
    { "group": "생존 시간 뱃지", "name": "종막", "tier": 4, "condition": "평균 게임 시간 19분 이상" },

    { "group": "탑 3 뱃지", "name": "불변의 생존가", "tier": 2, "condition": "Top 3 달성률 50% 이상" },
    { "group": "탑 3 뱃지", "name": "포디움", "tier": 3, "condition": "Top 3 달성률 55% 이상" },
    { "group": "탑 3 뱃지", "name": "관측자", "tier": 4, "condition": "Top 3 달성률 60% 이상" },

    { "group": "평균 순위 뱃지", "name": "꾸준한 생존자", "tier": 1, "condition": "평균 순위 5위 이하" },
    { "group": "평균 순위 뱃지", "name": "생존의 대가", "tier": 2, "condition": "평균 순위 4위 이하" },
    { "group": "평균 순위 뱃지", "name": "결승 내정자", "tier": 3, "condition": "평균 순위 3위 이하" },
    { "group": "평균 순위 뱃지", "name": "정점", "tier": 4, "condition": "평균 순위 1.9위 이하" }
];

export default function BadgesPage() {
    // 뱃지 데이터를 'group' 기준으로 그룹화합니다.
    const groupedBadges = badgeData.reduce((acc, badge) => {
        (acc[badge.group] = acc[badge.group] || []).push(badge);
        return acc;
    }, {});

    // 티어별 배경색을 정의합니다.
    const tierColor = {
        1: 'bg-orange-200 text-orange-800',                     // Bronze (밝은 오렌지 브라운)
        2: 'bg-slate-200 text-slate-800',                       // Silver (연한 회색-푸른 톤)
        3: 'bg-amber-200 text-amber-800',         // Gold (밝은 황금색)
        4: 'bg-gradient-to-br from-white to-slate-200 text-gray-800 border border-gray-300 shadow-lg shadow-cyan-500/40'      // Platinum (거의 흰색 + 테두리)
    }

    return (
        <main className={styles.badgesPage}>
            <div className={clsx(styles.badgeContent, "max-w-4xl mx-auto rounded-xl shadow-lg p-8")}>
                <h1 className={clsx(styles.badgeTitle, "text-3xl font-bold mb-6 text-center")}>뱃지 조건</h1>
                <div className="space-y-6">
                    {/* 그룹화된 뱃지 데이터를 순회하며 JSX로 렌더링합니다. */}
                    {Object.entries(groupedBadges).map(([group, badges]) => (
                        <div key={group} className="mb-8">
                            <h2 className={clsx(styles.badgeTitle, "text-2xl font-bold mb-4 border-b-2 border-gray-300 pb-2")}>
                                {group}
                            </h2>
                            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                                {badges.map((badge, index) => (
                                    <div key={index} className={`flex flex-col p-4 rounded-lg shadow-md ${tierColor[badge.tier]}`}>
                                        <div className="text-lg font-bold text-gray-900">{badge.name}</div>
                                        <div className="text-sm text-gray-700 mt-1">티어 {badge.tier}</div>
                                        <div className="text-sm text-gray-600 mt-2">조건: {badge.condition}</div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </main>
    );
}