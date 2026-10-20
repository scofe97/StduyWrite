# 타입 스펙: type-data-flow — PostgreSQL 커밋 즉시 Redis 캐시 키를 DEL 하고 WAL → Debezium → Kafka → 색인 소비자로 이어지는 비동기 전파 및 지연 중 요청의 DB 재검증 거절 갈래.
# 사실 출처: 강의 요약 §3.6·§3.11·§3.12(캐시 무효화와 CDC 검색 색인 파이프라인), 자료조사 보고서 research-A-booking.md #15·#24(Debezium, Kafka, Elasticsearch 및 DB 재검증 거절),
#   본문 01-01.md 6절(t0 커밋, 즉시 캐시 키 삭제, WAL 실시간 추적, 수 초 지연 색인 갱신 및 DB 재검증으로 이중 예약 차단).
# Layout formulas(type-data-flow §2): LABEL_W 140, SLOT 136, NSTEP 6, W = 984, Y0 = 84, HEAD = 48, LANE = 100, H = 588, NW 116, NH 68, 모든 좌표 4의 배수.
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

LABEL_W = 140
SLOT = 136
NSTEP = 6
W = LABEL_W + NSTEP * SLOT + 28  # 984
Y0 = 84
HEAD = 48
LANE = 100
NW = 116
NH = 68
H = 588

d = D(
    W, H,
    "SYSTEM DESIGN COURSE · 01-01 §6",
    "커밋 뒤 캐시 삭제와 색인 갱신이 시간차로 일어난다",
    "PostgreSQL 트랜잭션 커밋 즉시 Redis 캐시 키를 삭제하고, WAL 변경 로그를 Debezium 과 Kafka 로 전달해 수 초 뒤 Elasticsearch 색인을 비동기 갱신합니다.",
    "색인 지연 중 잔여석을 보고 진입한 요청도 DB 최종 검증에서 거절됩니다."
)

def cx(j): return LABEL_W + j * SLOT + SLOT // 2
def nx(j): return cx(j) - NW // 2
def lane_top(k): return Y0 + HEAD + k * LANE
def ny(k): return lane_top(k) + 16

# 1. 레인 배경 및 구분선
d.box(0, lane_top(0), W, LANE, PAPER2, RULE, 0.8)
d.box(0, lane_top(1), W, LANE, PAPER, RULE, 0.8)
d.box(0, lane_top(2), W, LANE, PAPER2, RULE, 0.8)
d.line(LABEL_W, lane_top(0), LABEL_W, lane_top(3), RULE, 1.0)

# 2. 단계 헤더 (Step Chips)
STEPS = [
    ("01", "커밋 t0"),
    ("02", "캐시 삭제"),
    ("03", "WAL 캡처"),
    ("04", "카프카 중계"),
    ("05", "색인 갱신"),
    ("06", "시차 검증"),
]

for j, (num, lab) in enumerate(STEPS):
    focal = j == 5
    c = ACC if focal else (OK if j == 0 else MUTED)
    d.tone(cx(j) - 18, Y0 + 4, 36, 18, c, r=9, op="22", sw=1.0)
    d.t(cx(j), Y0 + 17, num, 11, c, MONO, "middle", 600)
    d.t(cx(j), Y0 + 36, lab, 13, c, KR, "middle", 600 if focal else 400)

# 3. 레인 라벨 (좌측 열)
LANES = [
    ("저장소 (SSOT)", "PostgreSQL"),
    ("캐시 & CDC", "Redis · Debezium"),
    ("검색 계층", "Kafka · ES"),
]

for k, (a, b) in enumerate(LANES):
    mid_y = lane_top(k) + LANE // 2
    d.t(LABEL_W // 2, mid_y - 6, a, 13, INK, KR, "middle", 600)
    d.t(LABEL_W // 2, mid_y + 12, b, 12, MUTED, KR, "middle")

# 4. 연결 화살표 (직교 배선)
# (1) PostgreSQL 커밋 → WAL 기록 (수평)
d.path(f"M {nx(0) + NW + 2} {ny(0) + 34} L {nx(1) - 6} {ny(0) + 34}", INFO, 1.4, m="info")

# (2) PostgreSQL 커밋 → Redis 캐시 삭제 (직교 L)
d.path(f"M {cx(0) + 20} {ny(0) + NH + 2} L {cx(0) + 20} {ny(1) + 34} L {nx(1) - 6} {ny(1) + 34}", WARN, 1.4, m="warn")
d.t(cx(0) + 24, ny(1) + 24, "즉시 DEL", 12, WARN, KR, "start", 600)

# (3) WAL 기록 → Debezium CDC (직교 L)
d.path(f"M {nx(1) + NW + 2} {ny(0) + 34} L {cx(2)} {ny(0) + 34} L {cx(2)} {ny(1) - 6}", INFO, 1.4, m="info")

# (4) Debezium CDC → Kafka (직교 L)
d.path(f"M {nx(2) + NW + 2} {ny(1) + 34} L {cx(3)} {ny(1) + 34} L {cx(3)} {ny(2) - 6}", INFO, 1.4, m="info")

# (5) Kafka → Elasticsearch (수평)
d.path(f"M {nx(3) + NW + 2} {ny(2) + 34} L {nx(4) - 6} {ny(2) + 34}", INFO, 1.4, m="info")

# (6) 갈래: 색인 지연 중 검색 노출 → DB 재검증 거절 (직교 L, focal)
d.path(f"M {nx(4) + NW + 2} {ny(2) + 34} L {cx(5)} {ny(2) + 34} L {cx(5)} {ny(0) + NH + 8}", ACC, 1.6, m="acc")
d.t(cx(5) - 8, ny(1) + 40, "빈 방 노출 후 예약 진입", 12, ACC, KR, "end", 600)

# 5. 노드 배치
# [Step 01] PostgreSQL 커밋
d.box(nx(0), ny(0), NW, NH, PAPER2, OK, 1.2)
d.t(cx(0), ny(0) + 18, "예약 커밋 (t0)", 12, OK, KR, "middle", 600)
d.t(cx(0), ny(0) + 36, "reservations", 11, INK, MONO, "middle")
d.t(cx(0), ny(0) + 52, "재고 109 → 110", 11, MUTED, KR, "middle")

# [Step 02] WAL 기록
d.box(nx(1), ny(0), NW, NH, PAPER2, INFO, 1.0)
d.t(cx(1), ny(0) + 18, "WAL 로그 기록", 12, INFO, KR, "middle", 600)
d.t(cx(1), ny(0) + 36, "재고 변경 레코드", 11, INK, KR, "middle")
d.t(cx(1), ny(0) + 52, "커밋 로그 보관", 11, MUTED, KR, "middle")

# [Step 02] Redis 캐시 삭제
d.box(nx(1), ny(1), NW, NH, PAPER2, WARN, 1.2)
d.t(cx(1), ny(1) + 18, "Redis 캐시 무효화", 12, WARN, KR, "middle", 600)
d.t(cx(1), ny(1) + 36, "DEL 캐시 키", 11, INK, MONO, "middle")
d.t(cx(1), ny(1) + 52, "hotel_42:7:12-26", 11, MUTED, MONO, "middle")

# [Step 03] Debezium CDC
d.box(nx(2), ny(1), NW, NH, PAPER2, INFO, 1.0)
d.t(cx(2), ny(1) + 18, "Debezium CDC", 12, INFO, KR, "middle", 600)
d.t(cx(2), ny(1) + 36, "WAL 실시간 캡처", 11, INK, KR, "middle")
d.t(cx(2), ny(1) + 52, "JSON 이벤트 추출", 11, MUTED, KR, "middle")

# [Step 04] Apache Kafka
d.box(nx(3), ny(2), NW, NH, PAPER2, INFO, 1.0)
d.t(cx(3), ny(2) + 18, "Apache Kafka", 12, INFO, KR, "middle", 600)
d.t(cx(3), ny(2) + 36, "토픽 이벤트 발행", 11, INK, KR, "middle")
d.t(cx(3), ny(2) + 52, "파티션 순서 보장", 11, MUTED, KR, "middle")

# [Step 05] Elasticsearch (수 초 지연)
d.box(nx(4), ny(2), NW, NH, PAPER2, WARN, 1.2)
d.t(cx(4), ny(2) + 18, "Elasticsearch", 12, WARN, KR, "middle", 600)
d.t(cx(4), ny(2) + 36, "색인 비동기 갱신", 11, INK, KR, "middle")
d.t(cx(4), ny(2) + 52, "수 초 뒤 매진 반영", 11, WARN, KR, "middle")

# [Step 06] DB 재검증 거절 (focal)
d.tone(nx(5), ny(0), NW, NH, ACC, r=6, op="18", sw=1.4)
d.t(cx(5), ny(0) + 18, "DB 재검증 거절", 12, ACC, KR, "middle", 600)
d.t(cx(5), ny(0) + 36, "110 + 1 > 110", 11, ACC, MONO, "middle")
d.t(cx(5), ny(0) + 52, "이중 예약 거절", 11, ACC, KR, "middle")

# 6. 하단 시간축 (Time Axis)
TIME_Y = 444
d.line(LABEL_W, TIME_Y, W - 28, TIME_Y, RULE, 1.0)
d.t(LABEL_W // 2, TIME_Y + 4, "소요 시간축", 12, SOFT, KR, "middle", 600)

TIME_TICKS = [
    (0, "t0 (커밋)"),
    (1, "직후"),
    (4, "수 초 뒤"),
    (5, "시차 유입"),
]

for j in range(NSTEP):
    d.line(cx(j), TIME_Y - 4, cx(j), TIME_Y + 4, SOFT, 1.0)

for j, tick in TIME_TICKS:
    d.t(cx(j), TIME_Y + 16, tick, 11, SOFT, KR, "middle")

# 7. 범례
d.legend(508, [
    ("커밋 완료 (t0)", OK),
    ("즉시 무효화 · 지연 갱신", WARN),
    ("비동기 파이프라인 (CDC)", INFO),
    ("DB 재검증 거절 (focal)", ACC),
])

out_path = Path(__file__).parent.parent / "01-01.after-commit-sync.svg"
d.save(str(out_path))
