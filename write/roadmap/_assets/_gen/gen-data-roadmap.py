# write/roadmap/data-roadmap.md §학습 순서 — 데이터·데이터베이스 학습 로드맵.
#
# 순서 규칙은 장애 순서를 거꾸로 놓는 것이다 — 코드가 만드는 쿼리에서 시작해
#   그것이 흔들릴 때 한 층씩 내려간다. 그래서 SQL 이 1단계이고 합의가 9단계다.
# 절단선은 7단계 뒤에 긋는다 — 1~7 이 단일 DB, 8 부터가 노드 둘 이상이다.
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
    ("1 · SQL 과 인덱스", "코드가 만드는 쿼리를 읽는다",
     [("DDL · DML · JOIN · CTE", "", "필수"),
      ("MySQL 과 InnoDB · 정규화와 비정규화", "", "필수"),
      ("EXPLAIN · IOT · 페이지네이션", "", "필수")],
     [("인덱스 이론 · 커버링 · 선택도", "DDIA 4장", "필수"),
      ("GroupBy · OrderBy 함정", "", "추천"),
      ("쿼리 최적화 체크리스트", "", "추천")]),

    ("2 · 데이터 모델", "조인 횟수는 모델이 정한다",
     [("관계형 vs 문서 모델", "DDIA 3장", "추천"),
      ("정규화 · 비정규화 · 조인", "DDIA 3장", "추천"),
      ("그래프 모델 · 스키마 유연성", "DDIA 3장", "선택")],
     [("분석용 스키마 — 별 · 눈송이 · OBT", "DDIA 3장", "선택"),
      ("이벤트 소싱 · CQRS · DataFrame", "DDIA 3장", "선택"),
      ("NoSQL 비교", "", "선택")]),

    ("3 · 저장 엔진", "인덱스를 탄다는 말의 실체",
     [("OLTP 저장과 인덱스 기초", "DDIA 4장", "추천"),
      ("LSM 저장 엔진 · B-tree 와 비교", "Database Internals 2~4·7장", "추천"),
      ("보조 인덱스 · 인메모리 저장", "DDIA 4장", "추천")],
     [("컬럼 지향 저장 · 다차원 · 벡터 인덱스", "DDIA 4장", "선택"),
      ("WAL · 페이지 분할 · 복구", "Database Internals 3·5장", "추천"),
      ("인코딩과 호환성 · Avro · Protobuf", "DDIA 5장", "추천")]),

    ("4 · 영속성 계층", "코드가 SQL 로 번역되는 자리",
     [("커넥션 풀 · DataSource", "", "필수"),
      ("JdbcTemplate · 스프링 예외 추상화", "", "필수"),
      ("드라이버 wrap 로깅과 운영 비용", "", "추천")],
     [("ORM · 영속성 컨텍스트 · 식별자 전략", "", "필수"),
      ("엔티티 · 연관관계 · 상속 · 값 타입", "", "필수"),
      ("프록시와 N+1 · Projection · 페이징", "", "필수")]),

    ("5 · 트랜잭션과 락", "동시에 만졌을 때 무엇이 보이는가",
     [("ACID · 격리 수준 · 스냅샷 격리", "DDIA 8장", "필수"),
      ("InnoDB MVCC · 동시성 제어와 락", "", "필수"),
      ("Write Skew · 직렬화 가능성", "DDIA 8장", "추천")],
     [("스프링 트랜잭션 · 전파 · 롤백 규칙", "", "필수"),
      ("낙관적 락 · 비관적 락", "", "필수"),
      ("분산 트랜잭션 · 2PC", "DDIA 8장", "추천")]),

    ("6 · QueryDSL", "동적 쿼리를 타입 안전하게",
     [("기본 문법 · 조인 · 동적 쿼리", "", "추천"),
      ("프로젝션과 DTO 매핑", "", "추천"),
      ("페이징과 fetch join 함정", "", "필수")],
     [("PathBuilder · JPAExpressions", "", "추천"),
      ("벌크 연산 · SQL 함수 · window 대체", "", "추천"),
      ("6.12 와 7.x 마이그레이션", "", "선택")]),

    ("7 · 운영과 테스트", "운영 스키마로 재현하기",
     [("DB 덤프와 로컬 이관", "", "추천"),
      ("로컬 개발환경 운영 모델", "", "추천")],
     [("임베디드 DB 테스트 · 테스트 트랜잭션", "", "추천"),
      ("Testcontainers · 마이그레이션 도구", "", "선택")]),

    ("8 · 복제와 샤딩", "노드가 둘 이상이 되면",
     [("단일 리더 복제 · 복제 로그", "DDIA 6장", "필수"),
      ("복제 지연과 일관성 보장", "DDIA 6장", "필수"),
      ("다중 리더 · 쓰기 충돌 해소", "DDIA 6장", "추천"),
      ("리더리스 복제 · 정족수", "DDIA 6장", "추천")],
     [("키 범위 샤딩 · 해시 샤딩 · 일관 해싱", "DDIA 7장", "필수"),
      ("요청 라우팅과 리밸런싱", "DDIA 7장", "필수"),
      ("샤딩과 보조 인덱스", "DDIA 7장", "추천"),
      ("Galera 멀티마스터 · wsrep", "", "선택")]),

    ("9 · 분산의 문제와 합의", "믿을 수 없는 것 위에서 합의하기",
     [("부분 실패와 비신뢰 네트워크", "DDIA 9장", "필수"),
      ("불신뢰 시계 · 진실과 거짓", "DDIA 9장", "필수"),
      ("시스템 모델과 검증", "DDIA 9장", "추천")],
     [("선형성과 그 비용 · CAP", "DDIA 10장", "필수"),
      ("ID 생성기와 논리 시계", "DDIA 10장", "추천"),
      ("합의와 코디네이션 서비스", "DDIA 10장", "필수"),
      ("Paxos · Raft · quorum 패턴", "Patterns of Distributed Sys 8·11·14장", "추천")]),

    ("10 · 배치와 스트림", "쌓아 두고 흘려보내기",
     [("배치 처리 개요 · Unix 도구", "DDIA 11장", "추천"),
      ("분산 파일시스템 · 오브젝트 스토어", "DDIA 11장", "추천"),
      ("MapReduce 와 데이터플로우 엔진", "DDIA 11장", "선택")],
     [("메시지 브로커와 로그 기반 브로커", "DDIA 12장", "추천"),
      ("DB 와 스트림 · CDC", "DDIA 12장", "추천"),
      ("CEP · 윈도우 · 조인 · 시간 추론", "DDIA 12장", "추천"),
      ("데이터 통합 · DB 언번들링", "DDIA 13장", "선택")]),
]

CUT_AFTER = 6          # 7단계 뒤에 단일 DB ↔ 노드 둘 이상 절단선
NOTES = {
    6: "1~7단계는 손으로 확인하며 배우고 8단계부터는 대부분 읽어서 배운다. 실습이 여기서 끊긴다.",
    9: "메시지 브로커의 구현과 운영은 04_messaging 이 88편으로 맡는다. 여기는 왜 필요한가까지다.",
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

d = D(W, H, "WRITE · DATA ROADMAP",
      "데이터·데이터베이스 학습 로드맵",
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
        ("04_messaging", "브로커 운영 · Outbox · CDC 구현"),
        ("spring-roadmap", "트랜잭션의 프레임워크 축"),
        ("03_architecture", "시스템 설계 트레이드오프"),
        ("DDIA 1·2·14장", "설계 축과 윤리 — 순서가 없습니다")]):
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
        d.t(SX, y + 17, "1~7단계가 단일 DB · 8단계부터 노드가 둘 이상", 13, WARN, KR)
        y += 56

d.legend(H - 60, [("필수", INFO), ("추천", OK), ("선택", SOFT), ("대체 선택지", ACC),
                  ("단일 DB 와 분산의 경계", WARN)])
d.save("data-roadmap.svg")
