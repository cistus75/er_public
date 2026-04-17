// frontend/app/badges/page.js

import styles from "./page.module.css";
import clsx from 'clsx';

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

    const tierClassMap = {
        1: styles.tier1,
        2: styles.tier2,
        3: styles.tier3,
        4: styles.tier4
    };

    const tierNameMap = {
        1: "Tier 1: Bronze",
        2: "Tier 2: Silver",
        3: "Tier 3: Gold",
        4: "Tier 4: Master"
    };

    return (
        <main className={styles.badgesPage}>
            <div className={styles.badgeContent}>
                <header className={styles.badgeTitle}>
                    <h1>뱃지 도감</h1>
                    <p style={{ color: 'var(--tip-text)', marginTop: '8px' }}>
                        루미아 섬의 진정한 생존자임을 증명하는 명예의 훈장들입니다.
                    </p>
                </header>

                <div className={styles.groupList}>
                    {Object.entries(groupedBadges).map(([group, badges]) => (
                        <section key={group} className={styles.groupContainer}>
                            <h2 className={styles.groupName}>
                                {group}
                            </h2>
                            <div className={styles.badgeGrid}>
                                {badges.map((badge, index) => (
                                    <div 
                                        key={index} 
                                        className={clsx(styles.badgeCard, tierClassMap[badge.tier])}
                                    >
                                        <div className={styles.badgeName}>{badge.name}</div>
                                        <div className={styles.badgeTier}>
                                            {tierNameMap[badge.tier]}
                                        </div>
                                        <div className={styles.badgeCondition}>
                                            {badge.condition}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </section>
                    ))}
                </div>
            </div>
        </main>
    );
}
