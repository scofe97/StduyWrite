# write/roadmap/jvm-roadmap.md §학습 순서 — JVM 학습 로드맵.
#
# 이 로드맵은 반대다 — 정독 노트가 171편으로 가장 두껍고 책은 셋뿐이다.
#   그래서 아래 줄에 적는 것은 책 이름과 장이고, 어느 노트인지는 본문 단계 표가 짚는다.
#
# 판형은 roadmap.sh 계열이다 — 세로 척추에 단계를 걸고 개념을 좌우로 뻗되,
#   노드마다 우선순위 점을 찍는다. 단계에만 배지를 달던 앞 판은 한 단계 안에서
#   무엇이 뼈대이고 무엇이 곁가지인지 말하지 못했다.
#
# 노드의 주인공은 개념이고 책은 그 개념을 다루는 자리다. 책 줄이 비면 아직 자료가 없다는 뜻이고,
#   소장 목록이 늘면 그 줄만 채운다. 정독 노트 편수는 도식에 적지 않는다 —
#   "어디를 펴야 하는가"에 답하지 않는 정보다. 노트 링크는 본문 단계 표가 맡는다.
#
# 대체(ACC)는 같은 자리를 두 자료가 대신 채우는 경우다. 둘 다 읽으라는 뜻이 아니다.
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
    ("1 · 실행 모델", "코드가 JVM 안에서 어디에 놓이는가",
     [("런타임 데이터 영역", "심층 자바 가상 머신 2장", "필수"),
      ("객체 레이아웃 · 헤더 · 접근 방식", "심층 자바 가상 머신 2장", "필수"),
      ("스택 프레임 · 피연산자 스택", "심층 자바 가상 머신 8장", "필수")],
     [("OutOfMemoryError 를 영역별로 재현", "심층 자바 가상 머신 2장", "필수"),
      ("컨테이너 네이티브 메모리와 OOMKilled", "심층 자바 가상 머신 2장", "필수"),
      ("힙 밖 — Metaspace · direct", "Java Performance 8장", "추천")]),

    ("2 · 클래스 로딩", "무엇이 언제 타입이 되는가",
     [("클래스 파일 구조 · 상수 풀", "심층 자바 가상 머신 6장", "필수"),
      ("바이트코드 명령어", "심층 자바 가상 머신 6장", "추천"),
      ("로딩 시점과 생명주기", "심층 자바 가상 머신 7장", "필수"),
      ("로딩 · 검증 · 준비 · 해석 · 초기화", "심층 자바 가상 머신 7장", "필수")],
     [("클래스 로더와 부모 위임 모델", "심층 자바 가상 머신 7장", "필수"),
      ("모듈 시스템과 로더 변화 · JPMS", "심층 자바 가상 머신 7장", "추천"),
      ("톰캣 로더 · 격리 · TCCL · 로더 누수", "심층 자바 가상 머신 9장", "추천"),
      ("Spring Boot 실행 JAR 와 로딩", "심층 자바 가상 머신 9장", "추천")]),

    ("3 · 실행 엔진과 컴파일", "같은 바이트코드가 왜 다르게 도는가",
     [("메서드 호출 · 정적·동적 디스패치", "심층 자바 가상 머신 8장", "필수"),
      ("invokedynamic · 동적 타입 지원", "심층 자바 가상 머신 8장", "추천"),
      ("스택 기반 해석 실행 엔진", "심층 자바 가상 머신 8장", "추천"),
      ("javac 컴파일 과정 · 구문 설탕", "심층 자바 가상 머신 10장", "추천")],
     [("JIT · 인터프리터 · 계층형 컴파일", "심층 자바 가상 머신 11장", "필수"),
      ("핫스폿 탐지 · 컴파일 대상", "심층 자바 가상 머신 11장", "필수"),
      ("인라인 · 탈출 분석 · 공통식 제거", "심층 자바 가상 머신 11장", "추천"),
      ("code cache · deoptimization", "Java Performance 4장", "추천"),
      ("GraalVM · AOT · native image", "Java Performance 4장", "선택")]),

    ("4 · 가비지 컬렉션", "무엇을 죽었다 하고 언제 멈추는가",
     [("대상이 죽었는가 — 도달성과 참조 네 종", "심층 자바 가상 머신 3장", "필수"),
      ("GC 알고리즘 — 마크·복사·정리·세대", "심층 자바 가상 머신 3장", "필수"),
      ("핫스팟 구현 — 안전 지점 · 카드 테이블", "심층 자바 가상 머신 3장", "추천"),
      ("클래식 컬렉터 · Parallel · CMS", "심층 자바 가상 머신 3장", "추천")],
     [("G1 — Region · full GC 실패", "Java Performance 6장", "필수"),
      ("ZGC · Shenandoah 같은 저지연 컬렉터", "Java Performance 6장", "추천"),
      ("힙과 세대 크기 · metaspace 튜닝", "Java Performance 5장", "필수"),
      ("TLAB · humongous · tenuring", "Java Performance 6장", "추천"),
      ("GC 선택 · graceful degradation", "심층 자바 가상 머신 3장", "추천")]),

    ("5 · 동시성", "메모리 모델이 무엇을 보장하는가",
     [("자바 메모리 모델과 하드웨어 효율", "심층 자바 가상 머신 12장", "필수"),
      ("volatile · happens-before", "심층 자바 가상 머신 12장", "필수"),
      ("스레드 구현 · 스케줄링 · 상태", "심층 자바 가상 머신 12장", "필수"),
      ("가상 스레드 · 구조적 동시성", "심층 자바 가상 머신 12장", "추천")],
     [("스레드 안전성 다섯 등급", "심층 자바 가상 머신 13장", "필수"),
      ("동기화와 락 · 락 최적화", "심층 자바 가상 머신 13장", "필수"),
      ("Executor · 스레드 풀 크기", "Java Performance 9장", "필수"),
      ("ForkJoinPool · work stealing", "Java Performance 9장", "추천"),
      ("CAS · false sharing · 동기화 비용", "Java Performance 9장", "추천")]),

    ("6 · 성능 측정과 튜닝", "추측하지 않고 재는 법",
     [("무엇을 측정할까 — 벤치마크와 지표", "Java Performance 2장", "필수"),
      ("변동성과 통계 · 일찍 자주", "Java Performance 2장", "필수"),
      ("JMH 로 마이크로벤치마크", "Java Performance 2장", "필수"),
      ("OS 레벨 도구 · JDK 기본 도구", "Java Performance 3장", "필수")],
     [("프로파일러 두 방식", "Java Performance 3장", "필수"),
      ("Java Flight Recorder · JMC", "Java Performance 3장", "추천"),
      ("힙 분석 · retained · OOM 진단", "Java Performance 7장", "필수"),
      ("메모리 적게 쓰기 · 객체 재사용", "Java Performance 7장", "추천"),
      ("footprint · NMT · large pages", "Java Performance 8장", "추천"),
      ("JDBC · JPA · String · Stream 비용", "Java Performance 11·12장", "추천")]),

    ("7 · 장애 진단", "증상에서 원인으로 좁히는 절차",
     [("조사 기법의 지형과 네 시나리오", "Troubleshooting Java 1장", "추천"),
      ("디버거 · 조건부·비중단 중단점", "Troubleshooting Java 2·3장", "추천"),
      ("로그로 조사하기 · 로그가 만드는 문제", "Troubleshooting Java 4장", "필수"),
      ("스레드 락 · 대기 · wait·notify 함정", "Troubleshooting Java 7장", "필수")],
     [("스레드 덤프 획득과 데드락 추적", "Troubleshooting Java 8장", "필수"),
      ("힙 덤프 · referrers · OQL", "Troubleshooting Java 10장", "필수"),
      ("GC 로그로 진단하는 네 시나리오", "Troubleshooting Java 11장", "필수"),
      ("분산 추적 · trace ID 와 span", "Troubleshooting Java 12장", "추천"),
      ("cascading · retry · timeout", "Troubleshooting Java 12장", "추천"),
      ("서비스 간 데이터 불일치와 재생", "Troubleshooting Java 13장", "선택")]),
]

CUT_AFTER = 4          # 5단계 뒤에 "JVM 이 하는 일" ↔ "내가 재고 고치는 일" 절단선
NOTES = {
    4: "1~5단계는 JVM 이 하는 일이고 6단계부터는 그것을 재고 고치는 일이다.",
    6: "정독 노트 171편이 이 로드맵의 자료다. 책은 셋뿐이라 아래 줄이 장 번호만 가리킨다.",
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

d = D(W, H, "WRITE · JVM ROADMAP",
      "JVM 학습 로드맵",
      "애플리케이션이 여는 socket 에서 커널 패킷 경로로 내려간 뒤 Kubernetes 데이터패스로 다시 "
      "올라간다. 척추에 단계 여덟을 걸고 개념을 좌우로 뻗었다. 노드의 주인공은 개념이고 아래 줄은 "
      "그 개념을 다루는 책의 장이다. 점 색이 우선순위이고, 책 줄이 비면 아직 자료가 없는 자리다.",
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
        ("spring-roadmap", "프레임워크의 DI · AOP · 트랜잭션"),
        ("os-roadmap", "cgroup 이 재는 RSS 와 커널 메모리"),
        ("data-roadmap", "JDBC · JPA 의 쿼리와 트랜잭션 설계"),
        ("01_language/java", "언어 문법 · 컬렉션 · 디자인 패턴")]):
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
        d.o.append(f'<rect x="{SX - 235}" y="{y}" width="470" height="22" rx="4" fill="{PAPER}"/>')
        d.t(SX, y + 17, "1~5단계는 JVM 이 하는 일 · 6단계부터는 재고 고치는 일", 13, WARN, KR)
        y += 56

d.legend(H - 60, [("필수", INFO), ("추천", OK), ("선택", SOFT), ("대체 선택지", ACC),
                  ("동작과 진단의 경계", WARN)])
d.save("jvm-roadmap.svg")
