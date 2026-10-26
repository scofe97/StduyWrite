# 08-01.i1-slow-search — 검색 하나가 백엔드 공유 창구를 채워 단건 조회까지 멈춘 흐름
# 본문 요구(08-01 I1 slow search starves lookup): 느린 검색이 같은 창구를 쓰는 단건 조회까지 막은 메커니즘을 3개 참여자 레인과 5개 시간 단계로 보인다.
# 타입 스펙: type-swimlane — 손님·프록시·창구 세 가로 레인 위 5단계 시간 흐름. focal 은 검색 40 > 창구 32 칸.
# 사실 출처: ch08-slow-search-starves-lookup.md:15·16·26·27·28·29·30·46·47·54·55·57·58
import sys
from pathlib import Path

# _assets 및 _gen 경로 등록
ASSETS_DIR = Path(__file__).resolve().parent.parent
GEN_DIR = Path(__file__).resolve().parent
if str(ASSETS_DIR) not in sys.path:
    sys.path.insert(0, str(ASSETS_DIR))
if str(GEN_DIR) not in sys.path:
    sys.path.insert(0, str(GEN_DIR))

from dd import D, INK, MUTED, SOFT, RULE, PAPER2, ACC, WARN, KR, MONO

W = 960
H = 484

# 5열 격자 치수 (모두 4의 배수)
X0 = 128
CW = 148
GAP = 16
STRIDE = CW + GAP  # 164

# 레인 치수 (모두 4의 배수)
LANE_TOP = 140
LANE_H = 88
BOX_H = 64
BOX_Y_OFF = 12

def col_cx(c):
    return X0 + c * STRIDE + CW // 2

def col_x(c):
    return X0 + c * STRIDE

def lane_top(r):
    return LANE_TOP + r * LANE_H

def box_y(r):
    return lane_top(r) + BOX_Y_OFF

d = D(
    W,
    H,
    "SWIMLANE · CH08 I1 DIAGNOSIS",
    "검색 하나가 단건 조회까지 멈춘 흐름",
    "fakeinv 백엔드의 느린 검색 쿼리가 공유 창구 32칸을 채워 5ms 단건 조회까지 30초 손님 타임아웃으로 무너진 흐름",
    lead="검색 지연 주입 뒤 공유 일꾼 32칸이 잠식되고, 단건 조회가 8초 주기로 밀리다 전면 타임아웃으로 이어집니다."
)

# 1. 단계 열 머리 (Stage Headers)
stages = [
    "장애 전",
    "14:46:16 주입",
    "창구 잠식",
    "단건 조회 밀림",
    "붕괴 (30s)",
]

for c, st_title in enumerate(stages):
    cx = col_cx(c)
    fam = MONO if c == 1 else KR
    d.t(cx, 124, st_title, 13, INK, fam, "middle", 600)

# 2. 레인 구분선 및 레인 라벨
lane_labels = [
    ("손님", "npgload"),
    ("프록시", "npgproxy v0"),
    ("백엔드", "fakeinv 창구 32"),
]

# 상단 구분선
d.line(24, LANE_TOP, 932, LANE_TOP, RULE, 0.8)

for r, (l_title, l_sub) in enumerate(lane_labels):
    lt = lane_top(r)
    lb = lt + LANE_H
    d.line(24, lb, 932, lb, RULE, 0.8)
    d.t(24, lt + 36, l_title, 13, INK, KR, "start", 600)
    d.t(24, lt + 56, l_sub, 11, MUTED, MONO, "start")

# 3. 셀 상자 및 내용 (3행 x 5열)

# --- Col 0 (장애 전) ---
# Lane 0 (손님)
d.box(col_x(0), box_y(0), CW, BOX_H, PAPER2, RULE, 0.9, 6)
d.t(col_cx(0), box_y(0) + 26, "get 50/s · search 5/s", 11, MUTED, MONO, "middle")
d.t(col_cx(0), box_y(0) + 46, "p50 6ms · p99 8ms", 11, INK, MONO, "middle", 600)

# 요청 흐름 화살표 (손님 → 프록시)
d.arrow([(col_cx(0), box_y(0) + BOX_H), (col_cx(0), box_y(1))], c=MUTED, m="ar", sw=1.3)

# Lane 1 (프록시)
d.box(col_x(0), box_y(1), CW, BOX_H, PAPER2, RULE, 0.9, 6)
d.t(col_cx(0), box_y(1) + 26, "v0 DefaultTransport", 11, INK, MONO, "middle", 600)
d.t(col_cx(0), box_y(1) + 46, "기한 없음", 12, MUTED, KR, "middle")

# 요청 흐름 화살표 (프록시 → 백엔드)
d.arrow([(col_cx(0), box_y(1) + BOX_H), (col_cx(0), box_y(2))], c=MUTED, m="ar", sw=1.3)

# Lane 2 (백엔드)
d.box(col_x(0), box_y(2), CW, BOX_H, PAPER2, RULE, 0.9, 6)
d.t(col_cx(0), box_y(2) + 26, "workers=32", 11, INK, MONO, "middle", 600)
d.t(col_cx(0), box_y(2) + 46, "search 30ms · get 5ms", 11, MUTED, MONO, "middle")

# --- Col 1 (14:46:16) ---
# Lane 0
d.box(col_x(1), box_y(0), CW, BOX_H, PAPER2, RULE, 0.9, 6)
d.t(col_cx(1), box_y(0) + 36, "부하 동일", 12, INK, KR, "middle")

# Lane 1
d.box(col_x(1), box_y(1), CW, BOX_H, PAPER2, RULE, 0.9, 6)
d.t(col_cx(1), box_y(1) + 26, "상한 없음", 12, INK, KR, "middle")
d.t(col_cx(1), box_y(1) + 46, "즉시 전달", 12, MUTED, KR, "middle")

# Lane 2
d.box(col_x(1), box_y(2), CW, BOX_H, PAPER2, RULE, 0.9, 6)
d.t(col_cx(1), box_y(2) + 26, "search_latency=8s", 11, INK, MONO, "middle", 600)
d.t(col_cx(1), box_y(2) + 46, "workers=32", 11, MUTED, MONO, "middle")

# --- Col 2 (창구 잠식 - FOCAL) ---
# Lane 0
d.box(col_x(2), box_y(0), CW, BOX_H, PAPER2, RULE, 0.9, 6)
d.t(col_cx(2), box_y(0) + 36, "부하 지속", 12, INK, KR, "middle")

# Lane 1
d.box(col_x(2), box_y(1), CW, BOX_H, PAPER2, RULE, 0.9, 6)
d.t(col_cx(2), box_y(1) + 26, "inflight 누적", 12, INK, KR, "middle")
d.t(col_cx(2), box_y(1) + 46, "백엔드 대기 누적", 12, MUTED, KR, "middle")

# Lane 2 (FOCAL: 검색이 창구를 채움)
d.tone(col_x(2), box_y(2), CW, BOX_H, ACC, 6, "14", 1.6)
d.t(col_cx(2), box_y(2) + 26, "검색 5/s × 8s = 40", 11, ACC, MONO, "middle", 600)
d.t(col_cx(2), box_y(2) + 46, "40 > 창구 32", 13, ACC, KR, "middle", 600)

# --- Col 3 (단건 조회 밀림) ---
# Lane 0
d.box(col_x(3), box_y(0), CW, BOX_H, PAPER2, RULE, 0.9, 6)
d.t(col_cx(3), box_y(0) + 26, "get p99 2s→5s→8s", 11, INK, MONO, "middle", 600)
d.t(col_cx(3), box_y(0) + 46, "n=0 (8초 주기)", 12, MUTED, KR, "middle")

# Lane 1
d.box(col_x(3), box_y(1), CW, BOX_H, PAPER2, RULE, 0.9, 6)
d.t(col_cx(3), box_y(1) + 26, "inflight 913", 11, INK, MONO, "middle", 600)
d.t(col_cx(3), box_y(1) + 46, "HeapAlloc 약 47MB", 11, MUTED, MONO, "middle")

# Lane 2
d.box(col_x(3), box_y(2), CW, BOX_H, PAPER2, RULE, 0.9, 6)
d.t(col_cx(3), box_y(2) + 26, "8초 주기 반환", 12, INK, KR, "middle")
d.t(col_cx(3), box_y(2) + 46, "queued 증가", 12, MUTED, KR, "middle")

# --- Col 4 (붕괴) ---
# Lane 0
d.box(col_x(4), box_y(0), CW, BOX_H, PAPER2, RULE, 0.9, 6)
d.t(col_cx(4), box_y(0) + 26, "30s timeout", 12, INK, MONO, "middle", 600)
d.t(col_cx(4), box_y(0) + 46, "손님 포기", 12, MUTED, KR, "middle")

# Lane 1 (WARN: DC 49150, UT 0)
d.box(col_x(4), box_y(1), CW, BOX_H, PAPER2, RULE, 0.9, 6)
d.t(col_cx(4), box_y(1) + 26, "DC 49150", 12, WARN, MONO, "middle", 600)
d.t(col_cx(4), box_y(1) + 46, "UT 0 (기한 없음)", 12, WARN, KR, "middle", 600)

# Lane 2 (WARN: worked_after_cancel 26204)
d.box(col_x(4), box_y(2), CW, BOX_H, PAPER2, RULE, 0.9, 6)
d.t(col_cx(4), box_y(2) + 20, "queued 2933", 11, INK, MONO, "middle")
d.t(col_cx(4), box_y(2) + 38, "worked_after_cancel", 11, WARN, MONO, "middle", 600)
d.t(col_cx(4), box_y(2) + 54, "26204 (취소 무시)", 12, WARN, KR, "middle", 600)

# 4. 범례 (Legend)
d.legend(428, [("핵심 병목 (focal)", ACC), ("장애 관측값", WARN)])

d.save("08-01-i1-slow-search.svg")
