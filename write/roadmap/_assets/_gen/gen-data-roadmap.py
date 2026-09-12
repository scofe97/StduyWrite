# write/roadmap/data-roadmap.md §도입 — 데이터·데이터베이스 학습 로드맵.
# 데이터는 05_data 에 모여 있지만 04_messaging·09_spring 과 맞닿아 문서를 roadmap/ 에 둔다.
# 판형은 network·os·go 와 같다 — 세로 척추에 국면과 단계를 걸고 개념을 좌우로 뻗는다.
#
# network 은 "책"이 노드였지만 여기는 자료 묶음이 노드다. 자체 노트 85편이 주력이고 책이 보조라,
#   출처 구분(자체 노트 · 정독 · 외부책)은 노드 스타일이 아니라 부제 mono 슬롯이 맡는다.
#   스타일로 올리면 배지 색·국면 accent·점선과 겹쳐 시각 어휘가 넷이 되고,
#   출처 구분의 SSOT 는 본문 §무엇을 골랐는가 표다. 도식이 없는 논점을 만들지 않는다.
#
# 절단선은 4단계 뒤에 긋는다 — 0~4 가 단일 DB, 5 부터가 분산이다. 본문이 "이 경계를 흐리면
#   단일 DB 의 격리 수준 문제를 분산 일관성 문제로 오해한다"고 못 박은 자리라, 이 선이 편집상 논점이다.
#   그래서 accent 도 분산 국면 하나에만 쓴다 — 파선과 accent 가 한 시선에 묶여 경계가 두 배가 된다.
#
# 6.5 Galera 는 점선 노드다. 본문이 "이 자리는 아직 비어 있습니다"라고 적었으므로
#   실선으로 그리면 없는 자료가 있는 것처럼 보인다.
# 0.3·0.7 은 소수 번호다. 장애로 올라오지 않고 설계 시점에 이미 정해져 있어 배지를 추천으로 낮췄다.
# 타입 스펙: type-tree — 부모(국면)에서 자식(단계)으로 갈라지는 계층. coral 은 분산 데이터 국면 하나에만.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

SX = 500
W = 1000
NODE_W, NODE_H = 320, 48          # 296 으로는 "0.7 · DDIA 4장 + Database Internals" 가 넘친다
CH_W, CH_H, CH_GAP = 232, 32, 8
BUS, ROW_GAP, PHASE_GAP = 184, 40, 36
NOTE_H = 76

BADGE = {"필수": INFO, "추천": OK, "선택": SOFT}

# (제목, 부제 mono, 배지, 왼쪽 개념, 오른쪽 자료 밖 키워드, 점선 여부)
# 칩은 좌우 각 4개 상한. 본문 표가 5행인 자리는 한 칩에 · 로 묶는다.
phases = [
    ("쿼리와 영속성", "0~3단계", INFO, [
        ("0 · sql-mysql + 인덱스 이론", "12편 + 1편 · 자체 노트", "필수",
         ["DDL·DML·JOIN·SUBQUERY·CTE", "MySQL 과 InnoDB", "정규화와 비정규화",
          "EXPLAIN · IOT · 페이지네이션"],
         ["커버링 인덱스 · 선택도", "실행 계획 캐시 · 통계 갱신"], False),

        ("0.3 · DDIA 2판 3장", "6편 · 정독 노트", "추천",
         ["관계형 · 문서 · 그래프 모델", "정규화 · 비정규화 · 조인",
          "분석용 스키마 별·눈송이·OBT", "이벤트 소싱 · CQRS"],
         ["다중 모델 DB", "OBT 와 스토리지 비용"], False),

        ("0.7 · DDIA 4장 + Database Internals", "6편 + 1~7장 · 정독 · 외부책", "추천",
         ["OLTP 저장과 인덱스 기초", "LSM 저장 엔진과 컴팩션",
          "B-tree 와 LSM 비교", "컬럼 지향 · 벡터 인덱스"],
         ["쓰기 증폭 · 읽기 증폭", "fsync 와 그룹 커밋"], False),

        ("1 · jdbc + jpa 01~03번대", "11편 + 9편 · 자체 노트", "필수",
         ["DataSource 와 커넥션 풀", "영속성 컨텍스트", "엔티티·연관관계 매핑",
          "프록시와 N+1 · Projection"],
         ["풀 크기 산정 · 커넥션 누수", "쓰기 지연 · flush 시점"], False),

        ("2 · sql-mysql 04 + jpa 04번대", "5편 · 자체 노트", "필수",
         ["트랜잭션과 격리 수준", "InnoDB MVCC", "동시성 제어와 락",
          "스프링 트랜잭션과 전파"],
         ["갭 락 · 넥스트 키 락", "데드락 감지 · 락 대기 타임아웃"], False),

        ("3 · querydsl", "18편 · 6.12 기준", "추천",
         ["기본 문법 · 조인 · 동적 쿼리", "프로젝션과 DTO 매핑",
          "페이징과 fetch join 함정", "PathBuilder · JPAExpressions"],
         ["APT 와 Q 타입 생성 실패", "window 함수 부재"], False),
    ]),

    ("운영과 테스트", "4단계", INFO, [
        ("4 · 06_operations", "6편 · 2026-07", "추천",
         ["DB 덤프와 로컬 이관", "로컬 개발환경 운영 모델",
          "임베디드 DB 테스트", "테스트 트랜잭션"],
         ["Testcontainers", "마이그레이션 도구"], False),
    ]),

    ("분산 데이터", "5~7단계", ACC, [
        ("5 · DDIA 2판 6~8장", "14편 · 복제 · 샤딩 · 2PC", "필수",
         ["복제 개요와 단일 리더", "복제 지연과 일관성 보장",
          "다중 리더 · 쓰기 충돌 · 리더리스", "샤딩과 리밸런싱 · 2PC"],
         ["읽기 전용 복제본 라우팅", "페일오버 자동화"], False),

        ("6 · DDIA 2판 9~10장", "8편 · 네트워크 · 시계 · 합의", "필수",
         ["부분 실패와 비신뢰 네트워크", "불신뢰 시계 · 시스템 모델",
          "선형성과 그 비용 · CAP", "합의와 코디네이션 서비스"],
         ["Raft · Paxos 구현 차이", "쿼럼 산정"], False),

        ("6+ · Patterns of Distributed Systems", "32장 · 외부책", "추천",
         ["Majority Quorum · High-Water Mark", "Paxos · Replicated Log",
          "Lamport · Hybrid Clock", "Consistent Core · Lease"],
         ["이론을 구현 패턴으로 되짚기"], False),

        ("6.5 · Galera 멀티마스터", "제품 자료 없음 · MariaDB", "선택",
         ["wsrep · 인증 기반 복제", "flow control"],
         ["split-brain · 쿼럼 상실", "이론축은 PoDS 8 · 11 · 12장"], True),

        ("7 · DDIA 2판 5장과 11~13장", "17편 · 인코딩 · 배치 · 스트림", "추천",
         ["인코딩과 호환성 · Avro", "배치 처리와 오브젝트 스토어",
          "스트림 전송 · DB 와 스트림", "데이터 통합 · DB 언번들링"],
         ["CDC 구현", "Outbox 패턴"], False),
    ]),
]

NOTES = {
    "쿼리와 영속성":
        "느린 쿼리는 0단계, N+1 은 1단계, 락 대기는 2단계가 첫 자리다. 번호는 의존 순서이지 진도가 아니다.",
    "분산 데이터":
        "실습 표가 여기서부터 비어 있다. 노드를 여럿 띄우는 일은 이 카테고리가 아니라 운영 클러스터에서 일어난다.",
}
CUT_AFTER = "운영과 테스트"          # 이 국면 뒤에 단일DB ↔ 분산 절단선을 긋는다


def row_h(left, right):
    n = max(len(left), len(right))
    return max(NODE_H, n * CH_H + (n - 1) * CH_GAP) + 24


# ── 전체 높이를 먼저 셈한다. 상수 y 를 두면 국면마다 칩 수가 달라 한 자리만 깨진다
ROOT_Y = 116 + 180
y = ROOT_Y + 48 + PHASE_GAP
for name, _s, _c, steps in phases:
    y += NODE_H + ROW_GAP
    for st in steps:
        y += row_h(st[3], st[4]) + ROW_GAP
    if NOTES.get(name):
        y += NOTE_H
    y += PHASE_GAP - ROW_GAP
    if name == CUT_AFTER:
        y += 56
H = y + 80

d = D(W, H, "WRITE · DATA ROADMAP",
      "데이터·데이터베이스 학습 로드맵",
      "코드가 만드는 쿼리에서 시작해 분산 일관성까지 무엇을 어떤 순서로 읽는가. 척추에 국면 셋과 "
      "단계 열하나를 걸고, 자료 묶음을 노드로, 그 자료가 다루는 개념을 왼쪽에 자료 밖 키워드를 "
      "오른쪽에 뻗었다. 0~4단계가 단일 DB 이고 5단계부터가 분산이다. 배지는 필수·추천·선택 셋이다.",
      "0~4 가 단일 DB, 5 부터가 분산입니다. 번호는 의존 순서이지 진도가 아닙니다")

# ── 좌상단 읽는 법 상자
LX, LY, LW, LH = 40, 96, 336, 180
d.box(LX, LY, LW, LH, PAPER2, RULE, 1.0)
d.t(LX + 16, LY + 24, "읽는 법", 13, INK, KR, "start", 600)
for i, (lab, txt) in enumerate([("필수", "빼면 뒤가 막힙니다"),
                                ("추천", "빼도 되지만 손해가 큽니다"),
                                ("선택", "목표가 생겼을 때만")]):
    cy = LY + 56 + i * 28
    c = BADGE[lab]
    d.o.append(f'<rect x="{LX + 16}" y="{cy - 9}" width="34" height="17" rx="4" '
               f'fill="{c}22" stroke="{c}" stroke-width="0.9"/>')
    d.t(LX + 33, cy + 3, lab, 11, c, KR)
    d.t(LX + 60, cy + 3, txt, 13, MUTED, KR, "start")
d.t(LX + 16, LY + 148, "0~4 는 손으로 확인 · 5~7 은 읽어서", 12, SOFT, KR, "start")
d.t(LX + 16, LY + 166, "점선 — 자료가 아직 빈 자리", 12, SOFT, KR, "start")

# ── 우상단 인접 로드맵 상자. 척추에 못 걸지만 없으면 존재하지 않게 되는 것들
RX, RY, RW, RH = 624, 96, 336, 180
d.box(RX, RY, RW, RH, PAPER, RULE, 0.9)
d.o.append(f'<rect x="{RX}" y="{RY}" width="{RW}" height="{RH}" rx="6" fill="none" '
           f'stroke="{SOFT}" stroke-width="0.9" stroke-dasharray="4 4"/>')
d.t(RX + 16, RY + 24, "여기서 다루지 않는 것", 13, INK, KR, "start", 600)
for i, (who, what) in enumerate([
        ("04_messaging", "브로커 운영 · Outbox · CDC 구현"),
        ("spring-roadmap", "트랜잭션의 프레임워크 축"),
        ("03_architecture", "시스템 설계 트레이드오프"),
        ("DDIA 1·2·14장", "설계 축과 윤리 — 순서가 없습니다")]):
    cy = RY + 56 + i * 32
    d.t(RX + 16, cy, who, 13, MUTED, KR, "start", 600)
    d.t(RX + 16, cy + 16, what, 12, SOFT, KR, "start")

# ── 척추
d.box(SX - 130, ROOT_Y, 260, 48, PAPER2, RULE, 1.0)
d.t(SX, ROOT_Y + 30, "여기서 시작합니다", 14, INK, KR, "middle", 600)
d.line(SX, ROOT_Y + 48, SX, H - 116, RULE, 1.4)


def draw_step(title, sub, badge, left, right, dashed, y):
    h = row_h(left, right)
    mid = y + h / 2
    for side, items in (("left", left), ("right", right)):
        if not items:
            continue
        sign = -1 if side == "left" else 1
        bus = SX + sign * BUS
        top = mid - (len(items) * CH_H + (len(items) - 1) * CH_GAP) / 2
        d.line(SX + sign * (NODE_W / 2), mid, bus, mid, RULE, 1.0)
        for i, label in enumerate(items):
            cy = top + i * (CH_H + CH_GAP) + CH_H / 2
            bx = bus + (sign * 34) - (CH_W if side == "left" else 0)
            d.line(bus, mid, bus, cy, RULE, 1.0)
            d.line(bus, cy, bus + sign * 34, cy, RULE, 1.0)
            d.box(bx, cy - CH_H / 2, CH_W, CH_H, PAPER2, RULE, 0.9)
            d.t(bx + CH_W / 2, cy + 5, label, 13, MUTED, KR, "middle")
    # 자료가 빈 자리는 점선으로 — 실선이면 없는 것이 있어 보인다
    if dashed:
        d.o.append(f'<rect x="{SX - NODE_W/2}" y="{mid - NODE_H/2}" width="{NODE_W}" '
                   f'height="{NODE_H}" rx="6" fill="{PAPER}" stroke="{SOFT}" '
                   f'stroke-width="1.0" stroke-dasharray="4 4"/>')
    else:
        d.box(SX - NODE_W / 2, mid - NODE_H / 2, NODE_W, NODE_H, PAPER, RULE, 1.0)
    c = BADGE[badge]
    d.o.append(f'<rect x="{SX - NODE_W/2 + 12}" y="{mid - NODE_H/2 + 8}" width="34" height="17" '
               f'rx="4" fill="{c}22" stroke="{c}" stroke-width="0.9"/>')
    d.t(SX - NODE_W / 2 + 29, mid - NODE_H / 2 + 20, badge, 11, c, KR)
    d.t(SX + 12, mid - 4, title, 13, INK, KR, "middle", 600)
    d.t(SX, mid + 16, sub, 12, SOFT, MONO)
    return h


def draw_note(text, y):
    d.o.append(f'<rect x="110" y="{y}" width="780" height="{NOTE_H - 12}" rx="6" '
               f'fill="{PAPER}" stroke="{RULE}" stroke-width="0.9" stroke-dasharray="2 4"/>')
    d.t(130, y + 26, "메모", 11, SOFT, MONO, "start")
    d.t(130, y + 46, text, 13, MUTED, KR, "start")
    return NOTE_H


def draw_phase(name, stage, color, steps, y):
    if color is ACC:
        d.tone(SX - NODE_W / 2, y, NODE_W, NODE_H, ACC, 6, "16", 1.4)
    else:
        d.box(SX - NODE_W / 2, y, NODE_W, NODE_H, PAPER, color, 1.2)
    d.t(SX, y + 22, name, 15, ACC if color is ACC else INK, KR, "middle", 600)
    d.t(SX, y + 40, stage, 12, SOFT, MONO)
    y += NODE_H + ROW_GAP
    for st in steps:
        y += draw_step(*st, y) + ROW_GAP
    if NOTES.get(name):
        y += draw_note(NOTES[name], y)
    return y + PHASE_GAP - ROW_GAP


y = ROOT_Y + 48 + PHASE_GAP
for ph in phases:
    y = draw_phase(*ph, y)
    if ph[0] == CUT_AFTER:
        # 단일 DB 와 분산을 가르는 선. 이 로드맵의 편집상 논점이다
        d.line(40, y + 20, W - 40, y + 20, WARN, 1.4, "6 5")
        d.o.append(f'<rect x="{SX - 200}" y="{y + 8}" width="400" height="22" rx="4" fill="{PAPER}"/>')
        d.t(SX, y + 25, "0~4단계가 단일 DB · 아래부터 노드가 둘 이상", 13, WARN, KR)
        y += 56

d.legend(H - 68, [("필수", INFO), ("추천", OK), ("선택", SOFT), ("분산 구간", ACC),
                  ("단일 DB 와 분산의 경계", WARN)])
d.save("data-roadmap.svg")
