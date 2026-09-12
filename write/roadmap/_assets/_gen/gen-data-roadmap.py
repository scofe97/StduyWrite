# write/roadmap/data-roadmap.md §학습 순서 — 데이터 학습 로드맵.
#
# 자료 규칙이 다르다 — 소장 책 넷과 05_data/book 의 DDIA 2판 정독 노트만 쓴다.
#   05_data 의 자체 노트(01_foundation·02_relational·03_persistence·06_operations)는
#   도구와 프레임워크를 익힌 기록이라 순서를 정하는 근거로 삼지 않는다.
#   그래서 척추가 SQL·JPA·QueryDSL 이 아니라 DDIA 2판의 14장 흐름이 된다.
# 절단선은 4단계 뒤에 긋는다 — 1~4 가 노드 한 대 안에서 끝나는 일,
#   5 부터가 노드가 둘 이상일 때만 생기는 문제다.
#
# 판형은 roadmap.sh 계열이다 — 세로 척추에 단계를 걸고 개념을 좌우로 뻗되,
#   노드마다 우선순위 점을 찍는다.
# 노드의 주인공은 개념이고 책은 그 개념을 다루는 자리다. 정독 노트 편수는 도식에 적지 않는다.
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
    ("1 · 데이터 시스템의 축", "무엇을 재고 무엇을 지킬 것인가",
     [("운영 시스템과 분석 시스템", "DDIA 1장", "필수"),
      ("분산과 단일 노드", "DDIA 1장", "필수"),
      ("클라우드와 셀프 호스팅", "DDIA 1장", "추천")],
     [("응답 시간과 처리량", "DDIA 2장", "필수"),
      ("신뢰성과 내결함성", "DDIA 2장", "필수"),
      ("확장성과 유지보수성", "DDIA 2장", "필수"),
      ("데이터와 법 · 사회", "DDIA 1·14장", "선택")]),

    ("2 · 데이터 모델", "무엇으로 표현하고 어떻게 묻는가",
     [("관계형과 문서 모델", "DDIA 3장", "필수"),
      ("정규화 · 비정규화 · 조인", "DDIA 3장", "필수"),
      ("그래프 데이터 모델", "DDIA 3장", "추천")],
     [("스키마 유연성과 모델 선택", "DDIA 3장", "필수"),
      ("분석용 스키마 — 별 · 눈송이", "DDIA 3장", "추천"),
      ("이벤트 소싱 · CQRS", "DDIA 3장", "추천")]),

    ("3 · 저장 엔진과 인덱스", "디스크 위에 어떻게 눕히는가",
     [("OLTP 저장과 인덱스 기초", "DDIA 4장", "필수"),
      ("B-tree 기초와 구현", "Database Internals 2·4장", "필수"),
      ("LSM 과 로그 구조 저장", "Database Internals 7장", "필수"),
      ("B-tree 와 LSM 비교", "DDIA 4장", "필수")],
     [("파일 포맷과 B-tree 변형", "Database Internals 3·6장", "추천"),
      ("WAL 과 세그먼트 로그", "PoDS 3·4장", "추천"),
      ("보조 인덱스와 인메모리", "DDIA 4장", "필수"),
      ("컬럼 지향 저장", "DDIA 4장", "추천"),
      ("다차원 · 전문 · 벡터 인덱스", "DDIA 4장", "추천"),
      ("전문 검색 엔진의 색인", "Elasticsearch 3·4·7장", "선택")]),

    ("4 · 인코딩과 데이터플로우", "프로세스 경계를 넘길 때",
     [("인코딩과 호환성 기초", "DDIA 5장", "필수"),
      ("JSON · XML · 이진 변형", "DDIA 5장", "필수"),
      ("Protocol Buffers 와 Avro", "DDIA 5장", "필수")],
     [("DB · REST · RPC 데이터플로우", "DDIA 5장", "필수"),
      ("durable execution", "DDIA 5장", "추천"),
      ("이벤트 기반 아키텍처", "DDIA 5장", "추천")]),

    ("5 · 복제와 샤딩", "같은 데이터를 여러 곳에 두면",
     [("단일 리더 복제", "DDIA 6장", "필수"),
      ("복제 로그와 노드 장애", "DDIA 6장", "필수"),
      ("복제 지연과 일관성 보장", "DDIA 6장", "필수"),
      ("다중 리더와 쓰기 충돌", "DDIA 6장", "추천"),
      ("리더리스 복제와 정족수", "DDIA 6장", "필수")],
     [("키 범위 샤딩", "DDIA 7장 · PoDS 20장", "필수"),
      ("해시 샤딩과 일관 해싱", "DDIA 7장", "필수"),
      ("요청 라우팅과 리밸런싱", "DDIA 7장 · PoDS 19장", "필수"),
      ("샤딩과 보조 인덱스", "DDIA 7장", "추천"),
      ("복제 일관성의 구현", "Database Internals 11·12장", "추천")]),

    ("6 · 트랜잭션과 격리", "동시에 건드리면 무엇이 깨지는가",
     [("ACID 와 트랜잭션 개요", "DDIA 8장", "필수"),
      ("약한 격리와 스냅샷 격리", "DDIA 8장", "필수"),
      ("Write Skew 와 직렬화", "DDIA 8장", "필수")],
     [("트랜잭션 처리와 복구", "Database Internals 5장", "추천"),
      ("분산 트랜잭션과 2PC", "DDIA 8장 · PoDS 21장", "필수"),
      ("분산 트랜잭션 구현", "Database Internals 13장", "추천")]),

    ("7 · 분산의 문제", "믿을 수 없는 것 위에 짓기",
     [("부분 실패와 비신뢰 네트워크", "DDIA 9장", "필수"),
      ("불신뢰 시계", "DDIA 9장", "필수"),
      ("진실 · 거짓 · 시스템 모델", "DDIA 9장", "필수"),
      ("분산 시스템 검증", "DDIA 9장", "추천")],
     [("장애 감지", "Database Internals 9장 · PoDS 7장", "필수"),
      ("리더 선출", "Database Internals 10장 · PoDS 6장", "필수"),
      ("임차와 상태 감시", "PoDS 26·27장", "추천"),
      ("가십 전파와 창발 리더", "PoDS 28·29장", "선택")]),

    ("8 · 일관성과 합의", "무엇을 합의하고 무엇을 포기하는가",
     [("선형성", "DDIA 10장", "필수"),
      ("선형성의 비용과 CAP", "DDIA 10장", "필수"),
      ("ID 생성기와 논리 시계", "DDIA 10장 · PoDS 22·23장", "필수"),
      ("시계 경계 대기", "PoDS 24장", "선택")],
     [("합의와 코디네이션 서비스", "DDIA 10장", "필수"),
      ("합의 알고리즘", "Database Internals 14장", "필수"),
      ("Paxos 와 Replicated Log", "PoDS 11·12장", "추천"),
      ("일관 코어", "PoDS 25장", "추천"),
      ("버전 값과 버전 벡터", "PoDS 17·18장", "추천")]),

    ("9 · 배치와 스트림", "쌓인 것과 흐르는 것",
     [("Unix 도구와 배치 개요", "DDIA 11장", "필수"),
      ("분산 FS 와 오브젝트 스토어", "DDIA 11장", "필수"),
      ("MapReduce 와 잡 오케스트레이션", "DDIA 11장", "추천"),
      ("데이터플로우 엔진", "DDIA 11장", "추천")],
     [("메시지 브로커와 로그 기반", "DDIA 12장", "필수"),
      ("데이터베이스와 스트림 · CDC", "DDIA 12장", "필수"),
      ("CEP · 윈도우 · 조인", "DDIA 12장", "필수"),
      ("시간 추론과 내결함성", "DDIA 12장", "추천"),
      ("파생 데이터와 DB 언번들링", "DDIA 13장", "추천")]),
]

CUT_AFTER = 3          # 4단계 뒤에 "노드 한 대" ↔ "노드 둘 이상" 절단선
NOTES = {
    3: "1~4단계는 노드 한 대 안에서 끝나고 5단계부터는 노드가 둘 이상일 때만 생기는 문제다.",
    7: "자료를 소장 책 넷과 DDIA 2판 정독 노트로 한정했다. 05_data 의 자체 노트는 순서의 근거로 쓰지 않는다.",
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
      "데이터 학습 로드맵",
      "DDIA 2판의 열네 장을 척추로 삼고 Database Internals 와 Patterns of Distributed Systems 로 "
      "구현 층을 덧댄다. 데이터 시스템의 축에서 시작해 모델·저장 엔진·인코딩을 지나 복제와 샤딩, "
      "트랜잭션, 분산의 문제, 합의, 배치와 스트림으로 간다. 점 색이 우선순위다.",
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
d.t(LX + 16, LY + 172, "소장 책과 정독 노트만 걸었습니다 — 자체 노트는 제외", 12, SOFT, KR, "start")

RX, RY, RW, RH = 580, 96, 380, 190
d.box(RX, RY, RW, RH, PAPER, RULE, 0.9)
d.o.append(f'<rect x="{RX}" y="{RY}" width="{RW}" height="{RH}" rx="6" fill="none" '
           f'stroke="{SOFT}" stroke-width="0.9" stroke-dasharray="4 4"/>')
d.t(RX + 16, RY + 24, "여기서 다루지 않는 것", 13, INK, KR, "start", 600)
for i, (who, what) in enumerate([
        ("도구와 문법", "SQL · MySQL · JDBC · JPA · QueryDSL"),
        ("spring-roadmap", "@Transactional 과 영속성 컨텍스트"),
        ("observability-roadmap", "지표 · 로그 · 트레이스의 일반 이론"),
        ("05_data MOC", "자체 노트가 어느 폴더에 있는가")]):
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
        d.o.append(f'<rect x="{SX - 225}" y="{y}" width="450" height="22" rx="4" fill="{PAPER}"/>')
        d.t(SX, y + 17, "1~4단계는 노드 한 대 · 5단계부터는 노드 둘 이상", 13, WARN, KR)
        y += 56

d.legend(H - 60, [("필수", INFO), ("추천", OK), ("선택", SOFT), ("대체 선택지", ACC),
                  ("단일 노드와 분산의 경계", WARN)])
d.save("data-roadmap.svg")
