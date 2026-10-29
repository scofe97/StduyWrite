# 01-02-failure-names — 네 가지 업스트림 실패 분류와 상태 코드 및 장애 장면 맵
# 본문 요구: 뿌리 「업스트림 실패」에서 갈래 넷(UF·UC·UT·UO), 상태 코드(502·503·504), 01-01 장면 잎(I1·I2·I3). focal 은 같은 502 가 UF·UC 로 갈리는 자리.
# 타입 스펙: type-tree
# 사실 출처: 0012-upstream-deadlines-and-pool.md:11-16,81-86, 0013-upstream-retry-and-idempotency.md:9-18, reason.go:16-38,40-65, accesslog.go:54-61
import sys
from pathlib import Path

# _assets 및 _gen 경로 등록
ASSETS_DIR = Path(__file__).resolve().parent.parent
GEN_DIR = Path(__file__).resolve().parent
if str(ASSETS_DIR) not in sys.path:
    sys.path.insert(0, str(ASSETS_DIR))
if str(GEN_DIR) not in sys.path:
    sys.path.insert(0, str(GEN_DIR))

from dd import D, INK, MUTED, SOFT, RULE, PAPER2, ACC, WARN, BAD, INFO, OK, KR, MONO

W = 960
H = 492

d = D(
    W,
    H,
    "TREE · UPSTREAM FAILURE TAXONOMY",
    "업스트림 실패 분류와 상태 코드 체계",
    "뿌리 업스트림 실패에서 UF·UC·UT·UO 네 갈래와 상태 코드 및 01-01 장애 장면 매핑",
    lead="같은 502 상태 코드라도 연결 전 실패(UF)와 연결 후 단절(UC)로 갈립니다.",
)

# 상단 구분선 (4의 배수)
d.line(24, 92, 936, 92, RULE, 0.8)

# 열 및 행 좌표 정의 (모두 4의 배수)
X_ROOT = 24
W_ROOT = 144

X_COL1 = 208
W_COL1 = 176

X_COL2 = 416
W_COL2 = 240

X_COL3 = 696
W_COL3 = 240

Y_ROWS = [128, 204, 280, 356]
H_NODE = 64
MID_ROWS = [y + H_NODE // 2 for y in Y_ROWS]  # 160, 236, 312, 388

# 1. 연결선 (Z-order: 노드보다 먼저 그림)
# (1) Root -> Col 1 연결선 (트리 버스)
X_BUS1 = 188
Y_ROOT_MID = (MID_ROWS[0] + MID_ROWS[3]) // 2  # (160 + 388) // 2 = 274 -> 272 (4의 배수)

# Root 에서 Bus1 로
d.line(X_ROOT + W_ROOT, Y_ROOT_MID, X_BUS1, Y_ROOT_MID, c=MUTED, sw=1.2)
# Bus1 수직선
d.line(X_BUS1, MID_ROWS[0], X_BUS1, MID_ROWS[3], c=MUTED, sw=1.2)
# Bus1 에서 Col 1 각 행으로
for mid_y in MID_ROWS:
    d.line(X_BUS1, mid_y, X_COL1, mid_y, c=MUTED, sw=1.2)

# (2) Col 1 -> Col 2 연결선 (수평 연결)
for i, mid_y in enumerate(MID_ROWS):
    c = ACC if i < 2 else MUTED
    d.line(X_COL1 + W_COL1, mid_y, X_COL2, mid_y, c=c, sw=1.4 if i < 2 else 1.2)

# (3) Col 2 -> Col 3 연결선 (수평 연결)
for i, mid_y in enumerate(MID_ROWS):
    c = ACC if i < 2 else MUTED
    d.line(X_COL2 + W_COL2, mid_y, X_COL3, mid_y, c=c, sw=1.4 if i < 2 else 1.2)

# 2. focal 영역 (같은 502 가 UF·UC 로 갈리는 자리 강조)
# y=120 시작, 라벨은 y=112 (상단 구분선 92와 20px 간격 유지)
d.tone(408, 120, 256, 156, ACC, r=8, op="08", sw=1.6)
d.t(536, 112, "focal · 같은 502 분기", 13, ACC, KR, "middle", 600)

# 3. 노드 렌더링
# --- Col 0: 뿌리 (Root) ---
d.box(X_ROOT, 236, W_ROOT, 72, fill=PAPER2, stroke=RULE, sw=1.0, r=6)
d.t(X_ROOT + W_ROOT // 2, 264, "업스트림 실패", 14, INK, KR, "middle", 600)
d.t(X_ROOT + W_ROOT // 2, 286, "ReverseProxy 에러", 13, MUTED, MONO, "middle")

# --- Col 1: 실패 양상 (4 갈래) ---
# Row 0: 연결을 못 맺음
d.box(X_COL1, Y_ROWS[0], W_COL1, H_NODE, fill=PAPER2, stroke=RULE, sw=0.9, r=6)
d.t(X_COL1 + W_COL1 // 2, Y_ROWS[0] + 28, "연결을 못 맺음", 14, INK, KR, "middle", 600)
d.t(X_COL1 + W_COL1 // 2, Y_ROWS[0] + 48, "dial 단계 실패", 13, MUTED, KR, "middle")

# Row 1: 연결 뒤 응답 없이 끊김
d.box(X_COL1, Y_ROWS[1], W_COL1, H_NODE, fill=PAPER2, stroke=RULE, sw=0.9, r=6)
d.t(X_COL1 + W_COL1 // 2, Y_ROWS[1] + 28, "연결 뒤 끊김", 14, INK, KR, "middle", 600)
d.t(X_COL1 + W_COL1 // 2, Y_ROWS[1] + 48, "응답 전 EOF 단절", 13, MUTED, KR, "middle")

# Row 2: 기한 넘김
d.box(X_COL1, Y_ROWS[2], W_COL1, H_NODE, fill=PAPER2, stroke=RULE, sw=0.9, r=6)
d.t(X_COL1 + W_COL1 // 2, Y_ROWS[2] + 28, "기한 넘김", 14, INK, KR, "middle", 600)
d.t(X_COL1 + W_COL1 // 2, Y_ROWS[2] + 48, "15초 응답 초과", 13, MUTED, KR, "middle")

# Row 3: 줄이 가득
d.box(X_COL1, Y_ROWS[3], W_COL1, H_NODE, fill=PAPER2, stroke=RULE, sw=0.9, r=6)
d.t(X_COL1 + W_COL1 // 2, Y_ROWS[3] + 28, "줄이 가득", 14, INK, KR, "middle", 600)
d.t(X_COL1 + W_COL1 // 2, Y_ROWS[3] + 48, "검색 칸 8 + 줄 7 가득", 13, MUTED, KR, "middle")

# --- Col 2: 원인 코드 & HTTP 상태 코드 ---
# Row 0: UF -> 502
d.tone(X_COL2, Y_ROWS[0], W_COL2, H_NODE, ACC, r=6, op="14", sw=1.4)
d.t(X_COL2 + W_COL2 // 2, Y_ROWS[0] + 28, "UF · 502 Bad Gateway", 13, ACC, MONO, "middle", 600)
d.t(X_COL2 + W_COL2 // 2, Y_ROWS[0] + 48, "ReasonConnFail", 13, ACC, MONO, "middle")

# Row 1: UC -> 502
d.tone(X_COL2, Y_ROWS[1], W_COL2, H_NODE, ACC, r=6, op="14", sw=1.4)
d.t(X_COL2 + W_COL2 // 2, Y_ROWS[1] + 28, "UC · 502 Bad Gateway", 13, ACC, MONO, "middle", 600)
d.t(X_COL2 + W_COL2 // 2, Y_ROWS[1] + 48, "ReasonConnReset", 13, ACC, MONO, "middle")

# Row 2: UT -> 504
d.tone(X_COL2, Y_ROWS[2], W_COL2, H_NODE, WARN, r=6, op="10", sw=1.0)
d.t(X_COL2 + W_COL2 // 2, Y_ROWS[2] + 28, "UT · 504 Gateway Timeout", 13, WARN, MONO, "middle", 600)
d.t(X_COL2 + W_COL2 // 2, Y_ROWS[2] + 48, "ReasonTimeout", 13, WARN, MONO, "middle")

# Row 3: UO -> 503
d.tone(X_COL2, Y_ROWS[3], W_COL2, H_NODE, INFO, r=6, op="10", sw=1.0)
d.t(X_COL2 + W_COL2 // 2, Y_ROWS[3] + 28, "UO · 503 Service Unavailable", 13, INFO, MONO, "middle", 600)
d.t(X_COL2 + W_COL2 // 2, Y_ROWS[3] + 48, "ReasonOverflow", 13, INFO, MONO, "middle")

# --- Col 3: 01-01 장애 장면 (잎) ---
# Row 0: I3 포트 고갈
d.box(X_COL3, Y_ROWS[0], W_COL3, H_NODE, fill=PAPER2, stroke=RULE, sw=0.9, r=6)
d.t(X_COL3 + W_COL3 // 2, Y_ROWS[0] + 28, "I3 포트 고갈", 14, INK, KR, "middle", 600)
d.t(X_COL3 + W_COL3 // 2, Y_ROWS[0] + 48, "TIME_WAIT 28,213개", 13, MUTED, MONO, "middle")

# Row 1: I2 쉰 연결 경합
d.box(X_COL3, Y_ROWS[1], W_COL3, H_NODE, fill=PAPER2, stroke=RULE, sw=0.9, r=6)
d.t(X_COL3 + W_COL3 // 2, Y_ROWS[1] + 28, "I2 쉰 연결 경합", 14, INK, KR, "middle", 600)
d.t(X_COL3 + W_COL3 // 2, Y_ROWS[1] + 48, "POST 502 · idle EOF", 13, MUTED, MONO, "middle")

# Row 2: I1 느린 검색
d.box(X_COL3, Y_ROWS[2], W_COL3, H_NODE, fill=PAPER2, stroke=RULE, sw=0.9, r=6)
d.t(X_COL3 + W_COL3 // 2, Y_ROWS[2] + 28, "I1 느린 검색", 14, INK, KR, "middle", 600)
d.t(X_COL3 + W_COL3 // 2, Y_ROWS[2] + 48, "초당 55건 UT", 13, MUTED, KR, "middle")

# Row 3: I1 대기열 넘침
d.box(X_COL3, Y_ROWS[3], W_COL3, H_NODE, fill=PAPER2, stroke=RULE, sw=0.9, r=6)
d.t(X_COL3 + W_COL3 // 2, Y_ROWS[3] + 28, "I1 프록시 줄 넘침", 14, INK, KR, "middle", 600)
d.t(X_COL3 + W_COL3 // 2, Y_ROWS[3] + 48, "초당 4.38건 UO", 13, MUTED, KR, "middle")

# 4. 범례 (Legend)
d.legend(448, [("핵심 분기 (focal: 502 갈래)", ACC), ("기한 초과 (504)", WARN), ("대기열 포화 (503)", INFO)])

d.save("01-02-failure-names.svg")
