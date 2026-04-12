#브론즈 뱃지, 실버 뱃지, 골드 뱃지, 백야 뱃지 4종류 존재.
#브론즈(1티어) 각 1점, 실버(2티어) 각 3점, 골드(3티어) 각 5점, 백야(4티어) 각 10점.
#점수에 따라 등급 뱃지 추가 부여.


#아래의 코드는 순서대로 하단의 역할을 가짐.

#뱃지 이름
#뱃지 조건 설명
#뱃지 분류
#뱃지 티어
#뱃지 우선도
#뱃지 이미지 url
#뱃지 달성 조건





badge_rules = [


# 레벨 뱃지

    {
        "name" : "신입 연구원",  
        "alt" : "신입 연구원\n\n갓 입사한 신입 연구원의 열정이 담긴 뱃지\n 어디선가 도망치라는 소리가 흐릿하게 들려온다\n\n바닥에 흩어진 종이 뭉치들처럼\n그의 앞날을 암시하는 것이리라",  
        # 1 레벨 달성
        "group" : "level",  
        "tier" : 1,  
        'step' : 1,
        "img" : "/badge/1.png",  
        "condition" : (lambda stats, rank : stats["account_level"] >= 1)
    },
    {
        "name" : "견습 연구원",  
        "alt" : "견습 연구원\n\n이제 막 적응하기 시작한 견습 연구원의 사원증\n\n불안과 한탄이 그를 삼키기 시작했지만\n그는 아직도 이유를 깨닫지 못했다",  
        # 30 레벨 달성
        "group" : "level",  
        "tier" : 1,  
        'step' : 2,  
        "img" : "/badge/1.png",  
        "condition" : (lambda stats, rank : stats["account_level"] >= 30)
    },
    {
        "name" : "정식 연구원",  
        "alt" : "정식 연구원\n\n얼마 전 승진한 정식 연구원의 증거\n희미한 혈향이 주위를 맴돈다\n\n한때는 선배들도 함께하던 연구실이었다\n지금은 그 누구도 없다",  
        # 50 레벨 달성
        "group" : "level",  
        "tier" : 1,  
        'step' : 3,  
        "img" : "/badge/1.png",  
        "condition" : (lambda stats, rank : stats["account_level"] >= 50)
    },
    {
        "name" : "수석 연구원",  
        "alt" : "수석 연구원\n\n이미 감정을 잃은 수석 연구원의 증표\n\n그는 항상 동요하지 않고 연구를 했다고 한다\n다만 결코 칭송 받진 못했다",
        # 100 레벨 달성  
        "group" : "level",  
        "tier" : 2,  
        'step' : 4,  
        "img" : "/badge/2.png",  
        "condition" : (lambda stats, rank : stats["account_level"] >= 100)
    },
    {
        "name" : "알파 개발자",  
        "alt" : "알파 개발자\n\n폐기된 프로젝트의 관리자\n\n그 부산물들이 늘 주위를 맴돈다\n그리고 vf는 더 이상 위대하지 않으리라\n",  
        # 200 레벨 달성
        "group" : "level",  
        "tier" : 2,  
        'step' : 5,  
        "img" : "/badge/2.png",  
        "condition" : (lambda stats, rank : stats["account_level"] >= 200)
    },
    {
        "name" : "오메가 설계자",  
        "alt" : "오메가 설계자\n\n라자러스 실험을 설계한 장본인\n\n파기된 프로젝트지만 기록은 남아있다\n하지만 그의 기억은 남아있을까",  
        # 300 레벨 달성
        "group" : "level",  
        "tier" : 3,  
        'step' : 6,  
        "img" : "/badge/3.png",  
        "condition" : (lambda stats, rank : stats["account_level"] >= 300)
    },
    {
        "name" : "위클라인 관리자",  
        "alt" : "위클라인 관리자\n\nEXP-W의 총 관리자\n\n1차 실험이 실패한 뒤로 깊은 상심에 빠졌다\n 다만 상부의 명령으로 움직일 뿐이다",  
        # 400 레벨 달성
        "group" : "level",  
        "tier" : 3,  
        'step' : 7,  
        "img" : "/badge/3.png",  
        "condition" : (lambda stats, rank : stats["account_level"] >= 400)
    },
    {
        "name" : "영원한 탐구자",  
        "alt" : "영원한 탐구자\n\n지식을 탐구하는 것만이 유일한 구원이라 믿는 자\n\n실험의 부작용으로 영원을 살아간다\n그럼에도 아직 알지 못하는 것들이 많다",
        # 500 레벨 달성
        "group" : "level",  
        "tier" : 4,  
        'step' : 8,  
        "img" : "/badge/4.png",  
        "condition" : (lambda stats, rank : stats["account_level"] >= 500)
    },
    {
        "name" : "시작, 끝",  
        "alt" : "시작, 끝\n\n이걸 보셨다면 시스템에 일시적인 문제가 발생한 것이 분명합니다.\n\n일반적으로는 달성 불가능한 조건이므로, 이것을 마주했다면 버그나 치트 사용 등이 의심됩니다.",  
        # 1000 레벨 달성
        "group" : "level",  
        "tier" : 4,  
        'step' : 9,  
        "img" : "/badge/4.png",  
        "condition" : (lambda stats, rank : stats["account_level"] >= 1000)
    },

        
#승률 뱃지


    {
        'name' : '참가상',
        'alt' : '참가상\n\n중요한 것은 꺾이지 않는 마음\n\n그는 승리 대신 꾸준함을 선택했다\n실험 기록이 그의 열정을 기록한다',
        # 승률 0% 
        "group" : "win_rate",  
        "tier" : 1,  
        'step' : 1,  
        'img' : '/badge/1.png',
        'condition' : (lambda stats, rank : stats['win_rate_percentage'] == 0)
    },
    {
        'name' : '연쇄 생존마',
        'alt' : '연쇄 생존마\n\n부러지지도 꺾이지도 않는 자\n\n어떤 상황에도 동요하지 않는다\n그저 해야 할 일을 할 뿐',
        # 승률 10% 이상
        "group" : "win_rate",  
        "tier" : 1,  
        'step' : 2,  
        'img' : '/badge/1.png',
        'condition' : (lambda stats, rank : stats['win_rate_percentage'] >= 10)
    },
    {
        'name' : '우승 청부사',
        'alt' : '우승 청부사\n\n언제나 그의 수정구엔 의뢰서가 넘쳤났다\n\n지킬 것을 잃은 뒤 흥미는 없다\n수정구 구석엔 되돌아올 수 없는 것이 있다',
        # 승률 20% 이상
        "group" : "win_rate",  
        "tier" : 2,    
        'step' : 3,
        'img' : '/badge/2.png',
        'condition' : (lambda stats, rank : stats['win_rate_percentage'] >= 20)
    },
    {
        'name' : '그 긴거',
        'alt' : '그 긴거\n\n과거 그 누구보다 찬란했던 이가 남긴 문장\n\n양궁장과 학교, 호텔과 모래사장의 사진\n그리고 위대한 군주의 말까지 존재한다',
        # 승률 30% 이상
        "group" : "win_rate",  
        "tier" : 3,  
        'step' : 4,  
        'img' : '/badge/3.png',
        'condition' : (lambda stats, rank : stats['win_rate_percentage'] >= 30)
    },
    {
        'name' : '전장의 설계자',
        'alt' : '전장의 설계자\n\n모든 변수는 이미 계획 안에 있다\n\n수정구는 더 이상 미래를 비추지 않는다\n단지 그가 그린 미래를 확인할 뿐',
        # 승률 40% 이상
        "group" : "win_rate",  
        "tier" : 3,  
        'step' : 5,  
        'img' : '/badge/3.png',
        'condition' : (lambda stats, rank : stats['win_rate_percentage'] >= 40)
    },
    {
        'name' : '시작이 반이다',
        'alt' : '시작이 반이다\n\n시작은 그 무엇과 비교할 수 없는 재화다\n\n다만 가만히 있는다고 해서 남은 반이 채워지진 않으리라',
        # 승률 50% 이상
        "group" : "win_rate",  
        "tier" : 4,  
        'step' : 6,  
        'img' : '/badge/4.png',
        'condition' : (lambda stats, rank : stats['win_rate_percentage'] >= 50)
    },    
    {
        'name' : '오토암즈',
        'alt' : '오토암즈\n\n움직이지 않는 팔을 대체하기 위한 물건\n\n희미하게 딸깍거리는 소리가 들려온다\n이 물건을 사용하던 이들은 어느 순간 사라졌다',
        # 승률 70% 이상
        "group" : "win_rate",  
        "tier" : 4,  
        'step' : 7,  
        'img' : '/badge/4.png',
        'condition' : (lambda stats, rank : stats['win_rate_percentage'] >= 70)
    },
    {
        'name' : '레이더',
        'alt' : '레이더\n\n다른 사람의 위치를 파악하는 용도의 물건\n\n겉보기에는 평범하지만 무언가 특별하다\n구석에는 아주 작게 "1" "0" "0" 이라는 숫자가 쓰여 있다',
        # 승률 100%
        "group" : "win_rate",  
        "tier" : 4,  
        'step' : 8,  
        'img' : '/badge/4.png',
        'condition' : (lambda stats, rank : stats['win_rate_percentage'] == 100)
    },


# 랭크 뱃지

    {  
        'name' : '사관 생도',
        'alt' : '사관 생도\n\n돌아오지 않을 과거를 추억하는 옷\n\n훈련에 열심히 참여한 우수 생도들에게 주어진 보상이다\n제작 업체가 전소되어 다시 구할 방법은 없다',
        # 골드 달성
        'group' : 'rank',
        'tier' : 1,  
        'step' : 1,
        'img' : '/badge/1.png',
        'condition':(lambda stats, rank : rank['mmr'] >= 2400)
    },
    {  
        'name' : '광물의 왕',
        'alt' : '광물의 왕\n\n반짝이는 잿빛을 간직한 자들의 왕관\n\n색은 변하지 않고 영원히 빛난다\n곧 재는 재로 먼지는 먼지로 변하리라',
        # 미스릴 달성
        'group' : 'rank',
        'tier' : 2,  
        'step' : 2,
        'img' : '/badge/2.png',
        'condition':(lambda stats, rank : rank['mmr'] >= 7100)
    },
    {   
        'name' : '곰의 일족',
        'alt' : '곰의 일족\n\n절망의 끝에 도달하기 직전의 폰\n\n아직 영광을 누리진 못했다\n검열 삭제 흔적의 일부가 조각되어 있다',
        # 데미갓 달성
        'group' : 'rank',
        'tier' : 2,  
        'step' : 3,
        'img' : '/badge/2.png',
        'condition':(lambda stats, rank : rank['rank'] <= 1000 and rank['mmr'] >= 7800)
    },
    {  
        'name' : '용의 일족',
        'alt' : '용의 일족\n\n절망의 끝에 도달해 영광을 얻은 폰\n무한한 영광이 이 말을 기다린다\n검열 삭제의 추억이 주변을 감싼다',
        # 이터니티 달성
        'group' : 'rank',
        'tier' : 3,  
        'step' : 4,
        'img' : '/badge/3.png',
        'condition':(lambda stats, rank : rank['rank'] <= 300 and rank['mmr'] >= 7800)
    },
    {  
        'name' : '하이 랭커',
        'alt' : '하이 랭커\n\n정점으로 향하는 여정에 선 이들에게 주어진 증표\n\n앞으로 남은 길은 지금까지보다 험난하다\n다만 포기하는 자는 없으리라',
        # in 100
        'group' : 'rank',
        'tier' : 3,  
        'step' : 5,
        'img' : '/badge/3.png',
        'condition':(lambda stats, rank : rank['rank'] <= 100 and rank['mmr'] >= 7800)
    },
    {  
        'name' : '찬탈자',
        'alt' : '찬탈자\n\n유일한 자리를 노리는 자들\n\n여기까지 와서 꺾이진 않는다\n이 앞, 영광 있다',
        # in 10
        'group' : 'rank',
        'tier' : 4,  
        'step' : 6,
        'img' : '/badge/4.png',
        'condition':(lambda stats, rank : rank['rank'] <= 10 and rank['mmr'] >= 7800)
    },
    {  
        'name' : '천상천하 유아독존',
        'alt' : '천상천하 유아독존\n\n홀로 오롯히 선 자를 상징하는 물건\n\n하늘 위와 하늘 아래\n오직 그만이 존귀함을 말할 수 있다',
        # 1등
        'group' : 'rank',
        'tier' : 4,  
        'step' : 7,
        'img' : '/badge/4.png',
        'condition':(lambda stats, rank : rank['rank'] == 1 and rank['mmr'] >= 7800)
    },


# mmr 뱃지 

    {  
        'name' : '브론즈',
        'alt' : '브론즈의 긍지\n\n처음으로 발을 들인 자의 긍지\n\n앞으로 남은 길은 미지수다\n그러나 긍지만은 빛나리라',
        # 브론즈 티어
        'group' : 'mmr',
        'tier' : 1,  
        'step' : 1,
        'img' : '/badge/1.png',
        'condition':(lambda stats, rank : rank['mmr'] >= 600)
    },
    {  
        'name' : '실버',
        'alt' : '실버의 재능\n\n47번의 도전에도 꺾이지 않은 재능\n\n아직 증명하진 못했다\n하지만 미래에도 그러진 않을 것이다 ',
        # 실버 티어
        'group' : 'mmr',
        'tier' : 1,  
        'step' : 2,
        'img' : '/badge/1.png',
        'condition':(lambda stats, rank : rank['mmr'] >= 1400)
    },
    {  
        'name' : '골드',
        'alt' : '골드의 영광\n\n초신성과 함께 나타난 영광스러운 별의 파편\n\n고대부터 탐욕의 상징이었다\n어쩐지 사관 학교 입학증이 선물로 온다',
        # 골드 티어
        'group' : 'mmr',
        'tier' : 1,  
        'step' : 3,
        'img' : '/badge/1.png',
        'condition':(lambda stats, rank : rank['mmr'] >= 2400)
    },
    {  
        'name' : '플래',
        'alt' : '플래티넘의 증명\n\n역경을 겪고 결국 증명한 자들의 증표\n\n아름다우나 부서지지 않는다\n산화되지 않는 희망을 상징한다',
        # 플래 티어
        'group' : 'mmr',
        'tier' : 2,  
        'step' : 4,
        'img' : '/badge/2.png',
        'condition':(lambda stats, rank : rank['mmr'] >= 3600)
    },
    {  
        'name' : '다이아',
        'alt' : '다이아의 품격\n\n결코 깨지지 않는 품격을 상징하는 메달\n\n그 어떤 상황에 놓여도 부셔지지 않는다\n찬란한 품격은 세공으로도 가릴 수 없다',
        # 다이아 티어
        'group' : 'mmr',
        'tier' : 2,  
        'step' : 5,
        'img' : '/badge/2.png',
        'condition':(lambda stats, rank : rank['mmr'] >= 5000)
    },
    {  
        'name' : '메라',
        'alt' : '메테오라이트의 다짐\n\n운석이 충돌해도 말릴 수 없는 이의 다짐\n\n그의 마음은 굳게 정해졌다\n앞으로 나아가는 것엔 틀림이 없으리라',
        # 메라 티어
        'group' : 'mmr',
        'tier' : 3,  
        'step' : 6,
        'img' : '/badge/3.png',
        'condition':(lambda stats, rank : rank['mmr'] >= 6400)
    },
    {  
        'name' : '미스릴',
        'alt' : '미스릴의 맹세\n\n불변하는 맹세와 함께 수여된 증표\n\n잿빛으로 빛나는 맹세의 증표는 꺾이는 일이 없다\n맹세의 증명은 처음부터 정해져 있었다',
        # 미스릴 티어
        'group' : 'mmr',
        'tier' : 3,  
        'step' : 7,
        'img' : '/badge/3.png',
        'condition':(lambda stats, rank : rank['mmr'] >= 7100)
    },
    {
        'name' : '데미갓',
        'alt' : '데미갓의 왕좌\n\n죽음은 존재하나 가깝지 않은 이들을 위한 의자\n\n절반이나마 영원의 피를 이었다\n황금의 일족은 그를 상징하기엔 아직 부족하다',
        # 데미갓 달성
        'group' : 'mmr',
        'tier' : 4,  
        'step' : 8,
        'img' : '/badge/4.png',
        'condition':(lambda stats, rank : rank['rank'] <= 1000 and rank['mmr'] >= 7800)
    },
    {  
        'name' : '이터니티',
        'alt' : '이터니티의 별\n\n스스로 영원해진 별들을 위한 자리\n\n그들은 인간의 증명으로 제단할 수 없다\n영원함이 그들을 기억한다',
        # 이터니티 달성
        'group' : 'mmr',
        'tier' : 4,  
        'step' : 9,
        'img' : '/badge/4.png',
        'condition':(lambda stats, rank : rank['rank'] <= 300 and rank['mmr'] >= 7800)
    },
    {  
        'name' : '만점 클럽',
        'alt' : '만점 클럽\n\n증명한 자들을 위한 제단\n\n"만"이란 모든 것을 의미한다\n영원한 영광이 그들을 감싼다',
        # 1만점 달성
        'group' : 'mmr_sp',
        'tier' : 4,  
        'step' : 1,
        'img' : '/badge/4.png',
        'condition':(lambda stats, rank : rank['rank'] <= 300 and rank['mmr'] >= 10000)
    },


# kda 뱃지

    {  
        'name' : '무력의 증명',
        'alt' : '무력의 증명\n\n스스로의 무력을 증명한 자들을 위한 상징\n\n그 힘은 결코 패배하지 않는다\n수련에 대한 믿음의 보상이었을까',
        # kda 2.0 달성
        'group' : 'kda',
        'tier' : 1,  
        'step' : 1,
        'img' : '/badge/1.png',
        'condition':(lambda stats, rank : stats['kda'] >= 2)
    },
    {  
        'name' : '섬의 종결자',
        'alt' : '섬의 종결자\n\n한 조각의 희망도 남기지 않는 무자비한 파괴자\n\n명예를 알았으나 지금은 아니다\n더 이상의 믿음은 자유를 방해할 뿐이다',
        # kda 3.0 달성
        'group' : 'kda',
        'tier' : 2,  
        'step' : 2,
        'img' : '/badge/2.png',
        'condition':(lambda stats, rank : stats['kda'] >= 3)
    },
    {  
        'name' : '루미아의 지배자',
        'alt' : '루미아의 지배자\n\n섬을 반으로 가른 자들에게 주어지는 명예\n\n어쩐지 태양 바퀴의 모임에서 제안이 들어올 듯 하다',
        # kda 4.0 달성
        'group' : 'kda',
        'tier' : 3,  
        'step' : 3,
        'img' : '/badge/3.png',
        'condition':(lambda stats, rank : stats['kda'] >= 4)
    },
    {  
        'name' : '플래닛 킬러',
        'alt' : '플래닛 킬러\n\n섬을 넘어 행성을 가른 자들에게 주어진 이름\n\n매캐한 향기가 그들에게서 느껴진다\n고작 섬 하나 정도야 어렵지 않으리라',
        # kda 6.0 달성
        'group' : 'kda',
        'tier' : 4,  
        'step' : 4,
        'img' : '/badge/4.png',
        'condition':(lambda stats, rank : stats['kda'] >= 5)
    },


# 어시 뱃지

    {  
        'name' : '협력자',
        'alt' : '협력자\n\n아군을 도왔음을 증명하는 뱃지\n\n어떤 위협 앞에서도 동료를 지킨다\n그것이 형용할 수 없는 아득함임에도',
        # 어시 3회 이상
        'group' : 'assist',
        'tier' : 2,  
        'step' : 1,
        'img' : '/badge/2.png',
        'condition':(lambda stats, rank : stats['average_assists'] >= 3)
    },
    {  
        'name' : '최고의 서포터',
        'alt' : '최고의 서포터\n\n오래전 백의의 천사가 사용한 낡은 천\n\n가장 앞에 섰으나 그 헌신을 잃지는 않았다\n모든 승리의 그림자에 함께하리라',
        # 어시 4회 이상
        'group' : 'assist',
        'tier' : 3,  
        'step' : 2,
        'img' : '/badge/3.png',
        'condition':(lambda stats, rank : stats['average_assists'] >= 4)
    },
    {   
        'name' : '진정한 지원가',
        'alt' : '진정한 지원가\n\n피해의 근원을 제거하는 것을 업으로 삼은 이들\n\n아군에게 들어갈 피해를 치유하는 것이 아니다\n아군에게 피해를 입히는 근원을 제거한다',
        # 어시 5회 이상
        'group' : 'assist',
        'tier' : 4,  
        'step' : 3,
        'img' : '/badge/4.png',
        'condition':(lambda stats, rank : stats['average_assists'] >= 5)
    },


# 사망 뱃지

    {  
        'name' : '좀비',
        'alt' : '좀비\n\n생명을 잃은 이들에게 전하는 안식\n\n죽고 죽어 일백 번을 죽었다\n하지만 백골이 진토되도 의지는 계승된다',
        # 평균 3회 사망
        'group' : 'death',
        'tier' : 1,  
        'step' : 1,
        'img' : '/badge/1.png',
        'condition':(lambda stats, rank : stats['average_deaths'] >= 3)
    },

    {  
        'name' : '불사 대마왕',
        'alt' : '불사 대마왕\n\n죽지 않는 위대한 자의 왕관\n다섯 반지와 열 트로피가 그 업적을 대변한다\n\n그는 신을 노래할 필요가 없다\n그 이름이 곧 신의 노래이니',
        # 죽지 않음
        'group' : 'death',
        'tier' : 4,  
        'step' : 2,
        'img' : '/badge/4.png',
        'condition':(lambda stats, rank : stats['average_deaths'] == 0)
    },


# tk 뱃지

    {  
        'name' : '최초의 살인자',
        'alt' : '최초의 살인자\n\n인류 최초의 살인자의 후예\n\n죄가 네 문 앞에 도사리고 앉아 그를 노린다\n그는 죄에 굴레를 씌워야 한다',
        # tk 3.0 달성
        'group' : 'tk',
        'tier' : 1,  
        'step' : 1,
        'img' : '/badge/1.png',
        'condition':(lambda stats, rank : stats['average_team_kills'] >= 3)
    },
    {  
        'name' : '세븐 폴드',
        'alt' : '세븐 폴드\n\n벌을 짊어진 이의 무게\n\n그를 죽이는 자들에겐 일곱 갑절의 벌을 내린다\n이건 축복일까 저주일까',
        # tk 6.0 달성
        'group' : 'tk',
        'tier' : 2,  
        'step' : 2,
        'img' : '/badge/2.png',
        'condition':(lambda stats, rank : stats['average_team_kills'] >= 6)
    },
    {  
        'name' : '트럭 운전수',
        'alt' : '트럭 운전수\n\n핸들이 고장난 8톤 트럭의 운전수\n\n치이면 지금과는 다른 세계로 갈 것 같다\n상태를 명확히 표시하는 이능이 있다',
        # tk 9.0 달성
        'group' : 'tk',
        'tier' : 3,  
        'step' : 3,
        'img' : '/badge/3.png',
        'condition':(lambda stats, rank : stats['average_team_kills'] >= 9)
    },
    {  
        'name' : '안젤라 윈슬레어',
        'alt' : '안젤라 윈슬레어\n\n잔혹한 살인마의 첫 제물\n\n조각조각 나뉘었을 것이 틀림없다\n다만 아직 가죽 한 조각도 찾지 못했다',
        # tk 12.0 달성
        'group' : 'tk',
        'tier' : 4,  
        'step' : 4,
        'img' : '/badge/4.png',
        'condition':(lambda stats, rank : stats['average_team_kills'] >= 12)
    },
    {  
        'name' : '잭 더 리퍼',
        'alt' : '잭 더 리퍼\n\n베일에 감싸인 수수께끼의 살인마\n\n그가 지나친 자리엔 침묵만 남아 있다\n탐정의 시가 향기가 그 뒤에 따라온다',
        # tk 15.0 달성
        'group' : 'tk',
        'tier' : 4,  
        'step' : 5,
        'img' : '/badge/4.png',
        'condition':(lambda stats, rank : stats['average_team_kills'] >= 15)
    },


# 생존 시간 뱃지

    {  
        'name' : '스피드 러너',
        'alt' : '스피드 러너\n\n오로지 속도만을 추구하는 이들\n\n수단과 방법을 가리지 않는 일이 비일비재하다\n속도를 늦추는 것은 그들의 죄악이다',
        # 7분 미만 생존
        'group' : 'time',
        'tier' : 1,  
        'step' : 1,
        'img' : '/badge/1.png',
        'condition':(lambda stats, rank : stats['average_game_time_minutes'] < 7)
    },
    {  
        'name' : '루미아 관광객',
        'alt' : '루미아 관광객\n\n루미아 섬의 관광객\n\n특별 세일 문구에 속아 넘어왔다\n무사히 집에 돌아가는 것이 소원이다',
        # 7분 이상 생존
        'group' : 'time',
        'tier' : 1,  
        'step' : 2,
        'img' : '/badge/1.png',
        'condition':(lambda stats, rank : stats['average_game_time_minutes'] >= 7)
    },
    {  
        'name' : '루미아 유학생',
        'alt' : '루미아 유학생\n\n루미아 섬의 유학생\n\n재단의 지원을 받아 섬으로 건너왔다\n다행히 아직 비밀을 눈치채진 못했다',
        # 10분 이상 생존
        'group' : 'time',
        'tier' : 2,  
        'step' : 3,
        'img' : '/badge/2.png',
        'condition':(lambda stats, rank : stats['average_game_time_minutes'] >= 10)
    },
    {  
        'name' : '루미아 현지인',
        'alt' : '루미아 현지인\n\n루미아 섬의 현지인\n\n섬에서 긴 시간을 보낸 이\n실험의 성과는 언제쯤 나올지 알 수 없다',
        # 13분 이상 생존
        'group' : 'time',
        'tier' : 2,  
        'step' : 4,
        'img' : '/badge/2.png',
        'condition':(lambda stats, rank : stats['average_game_time_minutes'] >= 13)
    },
    {  
        'name' : '루미아 원주민',
        'alt' : '루미아 원주민\n\n루미아 섬의 원주민\n\n섬과 처음부터 함께 했다\n섬의 끝은 여전히 알 수 없다',
        # 16분 이상 생존
        'group' : 'time',
        'tier' : 3,  
        'step' : 5,
        'img' : '/badge/3.png',
        'condition':(lambda stats, rank : stats['average_game_time_minutes'] >= 16)
    },
    {  
        'name' : '종막',
        'alt' : '종막\n\n끝을 목격한 자\n\n더 이상 넘길 페이지는 없다\n무대는 저물고 막은 끝을 마주한다',
        # 19분 이상 생존
        'group' : 'time',
        'tier' : 4,  
        'step' : 6,
        'img' : '/badge/4.png',
        'condition':(lambda stats, rank : stats['average_game_time_minutes'] >= 19)
    },


# 탑 3 뱃지

    {  
        'name' : '불변의 생존가',
        'alt' : '불변의 생존가\n\n폭풍을 이겨낸 자\n\n수많은 변수들 사이에서 살아남았다\n유일한 상수는 오롯이 자신뿐이다',
        # 
        'group' : 'top3',
        'tier' : 2,  
        'step' : 1,
        'img' : '/badge/2.png',
        'condition':(lambda stats, rank : stats['top3_rate_percentage'] >= 50)
    },
    {  
        'name' : '포디움',
        'alt' : '포디움\n\n단상에 오른 자\n\n세계에서 최소 3등을 차지한 자를 위한 명예\n메달은 도금이라 씹으면 이가 깨질 듯 하다',
        # 
        'group' : 'top3',
        'tier' : 3,  
        'step' : 2,
        'img' : '/badge/3.png',
        'condition':(lambda stats, rank : stats['top3_rate_percentage'] >= 55)
    },
        {  
        'name' : '관측자',
        'alt' : '관측자\n\n섬의 마지막을 관측하는 자\n\n그에게 금지구역이란 집과 다를 바 없다\n나머지 둘은 잠시 머무는 손님이리라',
        # 
        'group' : 'top3',
        'tier' : 4,  
        'step' : 3,
        'img' : '/badge/4.png',
        'condition':(lambda stats, rank : stats['top3_rate_percentage'] >= 60)
    },


# 평균 순위 뱃지

    {  
        'name' : '꾸준한 생존자',
        'alt' : '꾸준한 생존자\n\n꾸준한 생존의 비법은 운동이라 말하고 다닌다\n\n정작 운동하는 모습을 본 사람은 없다\n하지만 거짓은 중요하지 않다 오직 결과만이 존재할 뿐',
        # 평순 5 이상
        'group' : 'average_rank',
        'tier' : 1,  
        'step' : 1,
        'img' : '/badge/1.png',
        'condition':(lambda stats, rank : stats['average_rank'] <= 5)
    },
    {  
        'name' : '생존의 대가',
        'alt' : '생존의 대가\n\n오랜 서바이벌 경험 끝에 대가의 반열에 오른 자\n\n항상 절반은 재칠 수 있다며 자신한다\n실제로도 그러할 것이다',
        # 평순 4 이상
        'group' : 'average_rank',
        'tier' : 2,  
        'step' : 2,
        'img' : '/badge/2.png',
        'condition':(lambda stats, rank : stats['average_rank'] <= 4)
    },
    {  
        'name' : '결승 내정자',
        'alt' : "결승 내정자\n\n얼마 전 '위'에서 연락 받은 이\n\n그의 실력은 하위 라운드의 수준은 아니다\n내정된 이유는 분명히 존재하리라",
        # 평순 3 이상
        'group' : 'average_rank',
        'tier' : 3,  
        'step' : 3,
        'img' : '/badge/3.png',
        'condition':(lambda stats, rank : stats['average_rank'] <= 3)
    },
    {  
        'name' : '정점',
        'alt' : '정점\n\n더 이상 어떤 것도 필요없다\n\n오직 스스로가 가장 높은 곳에 서리라',
        # 평순 1.9 이상
        'group' : 'average_rank',
        'tier' : 4,  
        'step' : 4,
        'img' : '/badge/4.png',
        'condition':(lambda stats, rank : stats['average_rank'] <= 1.9)
    }






]


def get_badges(stat, rank):
    # rank 정보가 없을 경우를 대비한 기본값 처리
    if not rank:
        rank = {"mmr": 0, "rank": 999999}
    # rank 딕셔너리에 필수 키가 없을 경우 기본값으로 보완 (KeyError 방어)
    rank.setdefault("mmr", -1)
    rank.setdefault("rank", 999999)
        
    earned_badges = []
    # 1. 조건에 맞는 모든 뱃지를 리스트에 추가
    for rule in badge_rules:
        if stat and rank and rule["condition"](stat, rank):
            earned_badges.append(rule)

    earned_by_group = {}
    # 2. 같은 그룹 내에서는 step이 가장 높은 뱃지만 남기기
    for badge in earned_badges:
        group = badge.get("group", "default")
        existing = earned_by_group.get(group)
        
        if not existing or badge["step"] > existing["step"]:
            earned_by_group[group] = badge
            
    # 3. 그룹별로 필터링된 뱃지들을 리스트로 변환
    final_badges = list(earned_by_group.values())
    
    # 4. tier와 step 모두 내림차순(높은게 먼저)으로 정렬
    final_badges.sort(key=lambda x: (-x['tier'], -x['step']))
    
    return final_badges