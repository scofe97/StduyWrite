# write/roadmap/spring-roadmap.md §학습 순서 — Spring 학습 로드맵.
#
# 축은 "왜 그렇게 동작하는가"다. API 를 만드는 법이 아니라 컨테이너가 빈을 만들고
#   프록시가 감싸고 DispatcherServlet 이 흘려보내고 TransactionManager 가 경계를 긋는
#   내부 흐름을 순서대로 연다.
# 절단선은 4단계 뒤에 긋는다 — 1~4 가 Spring Framework 가 직접 하는 일,
#   5 부터가 Boot 가 조립하고 운영으로 잇는 일이다.
#
# 판형은 roadmap.sh 계열이다 — 세로 척추에 단계를 걸고 개념을 좌우로 뻗되,
#   노드마다 우선순위 점을 찍는다.
# 노드의 주인공은 개념이고 책은 그 개념을 다루는 자리다. 책 줄이 비면 아직 자료가 없다는 뜻이고,
#   소장 목록이 늘면 그 줄만 채운다. 정독 노트 편수는 도식에 적지 않는다 —
#   "어디를 펴야 하는가"에 답하지 않는 정보이고, 노트 링크는 본문 단계 표가 맡는다.
# 타입 스펙: type-tree — 부모(단계)에서 자식(개념)으로 갈라지는 계층.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

SX = 500
W = 1000
NODE_W, NODE_H = 320, 52
CH_W, CH_H, CH_GAP = 268, 46, 10
BUS, ROW_GAP, PHASE_GAP = 184, 44, 40
NOTE_H = 76
ELBOW = 14

MARK = {"필수": INFO, "추천": OK, "선택": SOFT, "대체": ACC}

# (단계 제목, 단계 부제, [왼쪽], [오른쪽])
#   개념 노드 = (개념, 책 챕터 — 없으면 빈 문자열, 우선순위)
stages = [
    ("1 · 컨테이너와 빈", "객체를 누가 만들고 누가 쥐는가",
     [("IoC 와 DI — 제어의 역전", "Spring Start Here 2·3장", "필수"),
      ("BeanDefinition 이 먼저다", "", "필수"),
      ("빈 팩토리와 컨텍스트", "Spring Start Here 2장", "필수"),
      ("컴포넌트 스캔과 등록", "Spring Start Here 2장", "필수")],
     [("주입 방식과 순환 참조", "Spring Start Here 3장", "필수"),
      ("스코프와 생명주기", "Spring Start Here 5장", "필수"),
      ("추상화로 갈아 끼우기", "Spring Start Here 4장", "추천"),
      ("Spring 이 쓰는 디자인 패턴", "", "추천")]),

    ("2 · 프록시와 AOP", "부가기능은 어떻게 끼어드는가",
     [("횡단 관심사란 무엇인가", "Spring Start Here 6장", "필수"),
      ("동적 프록시와 CGLIB", "", "필수"),
      ("빈 후처리기가 끼워 넣는다", "", "필수")],
     [("@Aspect 와 포인트컷", "Spring Start Here 6장", "필수"),
      ("자기 호출이 프록시를 지나침", "", "필수"),
      ("템플릿·콜백과 ThreadLocal", "", "추천"),
      ("위빙 네 방식과 AspectJ", "", "선택")]),

    ("3 · 요청 처리", "HTTP 한 건이 컨트롤러에 닿기까지",
     [("WAS 와 서블릿 컨테이너", "", "필수"),
      ("DispatcherServlet 흐름", "Spring in Action 2장", "필수"),
      ("핸들러 매핑과 어댑터", "", "필수"),
      ("메시지 컨버터와 Jackson", "Spring in Action 7장", "필수")],
     [("예외 처리 — @ControllerAdvice", "", "필수"),
      ("검증 · 바인딩 · 타입 변환", "Spring in Action 2장", "필수"),
      ("파일 업로드와 멀티파트", "", "추천"),
      ("메시지와 국제화", "", "선택")]),

    ("4 · 트랜잭션과 이벤트", "DB 경계를 어디에 긋는가",
     [("@Transactional 내부 구조", "Spring Start Here 13장", "필수"),
      ("전파 · 격리 · 동기화", "Spring Start Here 13장", "필수"),
      ("영속성 컨텍스트와 N+1", "Spring in Action 3장", "필수"),
      ("MyBatis 와 JPA 혼용", "", "추천")],
     [("두 리스너의 차이", "", "필수"),
      ("커밋 전후 Phase 와 전파", "", "필수"),
      ("죽은 트랜잭션 피하기", "", "필수"),
      ("Spring Data 리포지토리", "Spring Start Here 14장", "추천")]),

    ("5 · 부트가 조립하는 세계", "라이브러리만 넣었는데 빈이 생긴다",
     [("스타터와 BOM 버전 관리", "", "필수"),
      ("자동 구성과 @Conditional", "", "필수"),
      ("순서 · 게이트 · 기본값", "", "필수"),
      ("커스텀 스타터 만들기", "", "추천")],
     [("외부 설정 우선순위", "Spring in Action 6장", "필수"),
      ("@ConfigurationProperties", "Spring in Action 6장", "필수"),
      ("프로필로 환경 가르기", "", "필수"),
      ("설정과 비밀 관리", "Cloud Native Spring 4·14장", "추천")]),

    ("6 · 외부 통신과 회복탄력성", "남의 서버가 안 죽는다는 보장은 없다",
     [("클라이언트 네 갈래 비교", "", "필수"),
      ("WebClient 빌드와 요청", "", "필수"),
      ("응답 처리와 에러 · 재시도", "", "필수"),
      ("OpenFeign 선언형 호출", "", "추천")],
     [("서킷 브레이커 상태 전이", "Cloud Native Spring 9장", "필수"),
      ("재시도 · 백오프 · 지터", "", "필수"),
      ("격벽과 속도 제한", "", "추천"),
      ("API 게이트웨이", "Cloud Native Spring 9장", "추천")]),

    ("7 · 비동기와 실시간", "요청 스레드 밖에서 도는 일",
     [("@Async 와 스레드 풀", "Spring in Action 9장", "필수"),
      ("스케줄링과 Quartz", "", "필수"),
      ("캐시 추상화", "", "추천"),
      ("배치 — 잡과 스텝", "Spring Batch 2~4장", "선택")],
     [("Reactor 와 백프레셔", "Spring in Action 11장", "추천"),
      ("WebFlux 두 모델", "Spring in Action 12장", "추천"),
      ("Netty 파이프라인", "", "선택"),
      ("SSE · WebSocket · STOMP", "", "추천")]),

    ("8 · 보안과 운영", "누가 들어오고 무엇이 보이는가",
     [("필터 체인이 먼저다", "Spring Security 5장", "필수"),
      ("인증과 사용자 · 비밀번호", "Spring Security 3·4·6장", "필수"),
      ("엔드포인트 인가", "Spring Security 7·8장", "필수"),
      ("CSRF 와 CORS", "Spring Security 9·10장", "추천")],
     [("메서드 수준 보안", "Spring Security 11·12장", "추천"),
      ("OAuth 2 와 OIDC", "Spring Security 13~16장", "추천"),
      ("액츄에이터 엔드포인트", "Spring in Action 15장", "필수"),
      ("마이크로미터와 메트릭", "Spring in Action 16·17장", "필수")]),

    ("9 · 테스트와 배포", "고쳐도 안 깨진다는 것을 어떻게 아는가",
     [("테스트 피라미드와 슬라이스", "Spring Start Here 15장", "필수"),
      ("Mockito 와 MockMvc", "", "필수"),
      ("Testcontainers 로 진짜 DB", "", "필수"),
      ("WireMock 과 외부 시스템", "", "추천")],
     [("ArchUnit 가드레일", "", "추천"),
      ("보안 설정 테스트", "Spring Security 18장", "추천"),
      ("bootJar 와 Layered JAR", "Spring in Action 18장", "필수"),
      ("컨테이너화와 배포", "Cloud Native Spring 6·7장", "추천"),
      ("지속 배포와 GitOps", "Cloud Native Spring 15장", "선택")]),
]

CUT_AFTER = 3          # 4단계 뒤에 "Framework 가 하는 일" ↔ "Boot 가 조립하는 일" 절단선
NOTES = {
    3: "1~4단계는 Spring Framework 가 직접 하는 일이고 5단계부터는 Boot 가 조립해 운영으로 잇는 일이다.",
    7: "보안과 검증은 소장 책만 있고 정독 노트가 없다. 그 자리는 책과 공식 문서가 받는다.",
}


def row_h(left, right):
    n = max(len(left), len(right))
    return max(NODE_H, n * CH_H + (n - 1) * CH_GAP) + 28


ROOT_Y = 116 + 190
y = ROOT_Y + 52 + PHASE_GAP
for i, (_t, _s, left, right) in enumerate(stages):
    y += row_h(left, right) + ROW_GAP
    if i in NOTES:
        y += NOTE_H
    if i == CUT_AFTER:
        y += 56
H = y + 84

d = D(W, H, "WRITE · SPRING ROADMAP",
      "Spring 학습 로드맵",
      "API 를 만드는 법이 아니라 왜 그렇게 동작하는지를 여는 순서다. 컨테이너가 빈을 만들고 프록시가 "
      "감싸고 DispatcherServlet 이 흘려보내고 TransactionManager 가 경계를 긋는 데까지 간 뒤, Boot 의 "
      "자동 구성과 통신·보안·운영·테스트로 넓힌다. 점 색이 우선순위이고, 책 줄이 비면 자료가 없는 자리다.",
      "노드는 개념, 아래 줄은 그 개념을 다루는 책의 장입니다")

LX, LY, LW, LH = 40, 96, 380, 190
d.box(LX, LY, LW, LH, PAPER2, RULE, 1.0)
d.t(LX + 16, LY + 24, "읽는 법", 13, INK, KR, "start", 600)
for i, (lab, txt) in enumerate([("필수", "빼면 뒤가 막힙니다"),
                                ("추천", "빼도 되지만 손해가 큽니다"),
                                ("선택", "목표가 생겼을 때만"),
                                ("대체", "같은 자리 — 하나만 고릅니다")]):
    cy = LY + 54 + i * 26
    c = MARK[lab]
    d.o.append(f'<circle cx="{LX + 24}" cy="{cy}" r="5" fill="{c}"/>')
    d.t(LX + 40, cy + 4, lab, 12, c, KR, "start", 600)
    d.t(LX + 78, cy + 4, txt, 12, MUTED, KR, "start")
d.t(LX + 16, LY + 172, "책 줄이 비면 아직 자료가 없는 자리 — 개념이 먼저입니다", 12, SOFT, KR, "start")

RX, RY, RW, RH = 580, 96, 380, 190
d.box(RX, RY, RW, RH, PAPER, RULE, 0.9)
d.o.append(f'<rect x="{RX}" y="{RY}" width="{RW}" height="{RH}" rx="6" fill="none" '
           f'stroke="{SOFT}" stroke-width="0.9" stroke-dasharray="4 4"/>')
d.t(RX + 16, RY + 24, "여기서 다루지 않는 것", 13, INK, KR, "start", 600)
for i, (who, what) in enumerate([
        ("jvm-roadmap", "GC · 클래스 로딩 · 힙 덤프"),
        ("data-roadmap", "SQL 실행 계획과 분산 일관성"),
        ("observability-roadmap", "PromQL · SLO · 알림 설계"),
        ("k8s-roadmap", "오브젝트와 클러스터 내부 구조")]):
    cy = RY + 56 + i * 33
    d.t(RX + 16, cy, who, 13, MUTED, KR, "start", 600)
    d.t(RX + 16, cy + 16, what, 12, SOFT, KR, "start")

d.box(SX - 130, ROOT_Y, 260, 52, PAPER2, RULE, 1.0)
d.t(SX, ROOT_Y + 32, "여기서 시작합니다", 14, INK, KR, "middle", 600)
d.line(SX, ROOT_Y + 52, SX, H - 120, RULE, 1.4)


def draw_stage(title, sub, left, right, y):
    h = row_h(left, right)
    mid = y + h / 2
    for side, items in (("left", left), ("right", right)):
        sign = -1 if side == "left" else 1
        bus = SX + sign * BUS
        top = mid - (len(items) * CH_H + (len(items) - 1) * CH_GAP) / 2
        d.line(SX + sign * (NODE_W / 2), mid, bus, mid, RULE, 1.0)
        for i, (concept, book, mark) in enumerate(items):
            cy = top + i * (CH_H + CH_GAP) + CH_H / 2
            bx = bus + (sign * ELBOW) - (CH_W if side == "left" else 0)
            c = MARK[mark]
            d.line(bus, mid, bus, cy, RULE, 1.0)
            d.line(bus, cy, bus + sign * ELBOW, cy, RULE, 1.0)
            d.box(bx, cy - CH_H / 2, CH_W, CH_H, PAPER2, RULE, 0.9)
            d.o.append(f'<circle cx="{bx + 15}" cy="{cy - 8}" r="4.5" fill="{c}"/>')
            d.t(bx + 28, cy - 4, concept, 12, INK, KR, "start")
            d.t(bx + 28, cy + 14, book if book else "책 없음 — 채울 자리", 10,
                SOFT if book else MARK["선택"], MONO, "start")
    d.box(SX - NODE_W / 2, mid - NODE_H / 2, NODE_W, NODE_H, PAPER, INFO, 1.2)
    d.t(SX, mid - 4, title, 14, INK, KR, "middle", 600)
    d.t(SX, mid + 16, sub, 11, SOFT, KR)
    return h


def draw_note(text, y):
    d.o.append(f'<rect x="110" y="{y}" width="780" height="{NOTE_H - 12}" rx="6" '
               f'fill="{PAPER}" stroke="{RULE}" stroke-width="0.9" stroke-dasharray="2 4"/>')
    d.t(130, y + 26, "메모", 11, SOFT, MONO, "start")
    d.t(130, y + 46, text, 13, MUTED, KR, "start")
    return NOTE_H


y = ROOT_Y + 52 + PHASE_GAP
for i, (title, sub, left, right) in enumerate(stages):
    y += draw_stage(title, sub, left, right, y) + ROW_GAP
    if i in NOTES:
        y += draw_note(NOTES[i], y)
    if i == CUT_AFTER:
        d.line(40, y + 12, W - 40, y + 12, WARN, 1.4, "6 5")
        d.o.append(f'<rect x="{SX - 265}" y="{y}" width="530" height="22" rx="4" fill="{PAPER}"/>')
        d.t(SX, y + 17, "1~4단계는 Framework 가 하는 일 · 5단계부터는 Boot 가 조립하는 일", 13, WARN, KR)
        y += 56

d.legend(H - 60, [("필수", INFO), ("추천", OK), ("선택", SOFT), ("대체 선택지", ACC),
                  ("Framework 와 Boot 의 경계", WARN)])
d.save("spring-roadmap.svg")
