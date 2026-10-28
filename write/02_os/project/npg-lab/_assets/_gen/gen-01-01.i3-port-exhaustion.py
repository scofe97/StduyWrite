# 01-01-i3-port-exhaustion — 48개 닫힘이 TIME_WAIT 60초로 누적되어 출발 포트 28,232개를 채운 흐름
# 본문 요구(01-01 I3 부하 시험만 하면 포트가 바닥난다): I3 흐름: 동시 50 가운데 48 을 닫아 TIME_WAIT 가 출발 포트를 채우기까지
# 타입 스펙: type-swimlane — 손님·프록시·출발 포트 세 가로 레인 위 4단계 시간 흐름. focal 은 포트 28,232개 고갈과 dial 실패.
# 사실 출처: ch08-port-exhaustion-time-wait.md:9,19,23,24,26,45,49,59-63,68-76,82-85,91,101-105
import sys
from pathlib import Path

# _assets 및 _gen 경로 등록
ASSETS_DIR = Path(__file__).resolve().parent.parent
GEN_DIR = Path(__file__).resolve().parent
if str(ASSETS_DIR) not in sys.path:
    sys.path.insert(0, str(ASSETS_DIR))
if str(GEN_DIR) not in sys.path:
    sys.path.insert(0, str(GEN_DIR))

from dd import D, INK, MUTED, SOFT, RULE, PAPER, PAPER2, ACC, WARN, OK, BAD, KR, MONO

W = 960
H = 496

# 4열 격자 치수 (모두 4의 배수)
X0 = 136
CW = 188
GAP = 16
STRIDE = CW + GAP  # 204

# 레인 치수 (모두 4의 배수)
LANE_TOP = 140
LANE_H = 92
BOX_H = 72
BOX_Y_OFF = 10

def col_cx(c):
    return X0 + c * STRIDE + CW // 2

def col_x(c):
    return X0 + c * STRIDE

def lane_top(r):
    return LANE_TOP + r * LANE_H

def box_y(r):
    return lane_top(r) + BOX_Y_OFF

def draw_port_bar(d, x, y, current, total=28232, color=MUTED):
    bx = x + 16
    bw = CW - 32  # 156
    bh = 10
    d.box(bx, y, bw, bh, fill="#0A0D12", stroke=RULE, sw=0.8, r=3)
    fill_w = max(4, int(bw * current / total))
    if current > 0:
        d.box(bx, y, min(fill_w, bw), bh, fill=color, stroke=color, sw=0.8, r=3)

d = D(
    W,
    H,
    "SWIMLANE · CH08 I3 DIAGNOSIS",
    "동시 50 중 48을 닫아 포트를 채우기까지",
    "동시 50 요청 중 48개가 닫혀 TIME_WAIT 60초 동안 누적되고 28,232개 출발 포트가 바닥나 dial 실패(UF 502)로 이어진 흐름",
    lead="요청마다 48개 소켓을 닫아 TIME_WAIT 가 누적되고, 28,232개 포트 고갈로 dial 실패(UF 502)가 발생합니다."
)

# 1. 단계 열 머리 (Stage Headers)
stages = [
    "1단계: 48 닫힘",
    "2단계: 새 연결",
    "3단계: 포트 누적",
    "4단계: 포트 고갈",
]

for c, st_title in enumerate(stages):
    cx = col_cx(c)
    d.t(cx, 124, st_title, 13, ACC if c == 3 else INK, KR, "middle", 600)

# 2. 레인 구분선 및 레인 라벨
lane_labels = [
    ("손님", "npgload -c 50"),
    ("프록시", "Transport 풀"),
    ("출발 포트", "호스트 28,232개"),
]

d.line(24, LANE_TOP, 936, LANE_TOP, RULE, 0.8)

for r, (l_title, l_sub) in enumerate(lane_labels):
    lt = lane_top(r)
    lb = lt + LANE_H
    d.line(24, lb, 936, lb, RULE, 0.8)
    d.t(24, lt + 38, l_title, 13, INK, KR, "start", 600)
    d.t(24, lt + 58, l_sub, 11, MUTED, MONO, "start")

# 3. 셀 상자 및 내용 (3행 x 4열)

# --- Col 0 (1단계: 48 닫힘) ---
# Lane 0 (손님)
d.box(col_x(0), box_y(0), CW, BOX_H, PAPER2, RULE, 0.9, 6)
d.t(col_cx(0), box_y(0) + 28, "요청 50 완료", 13, INK, KR, "middle", 600)
d.t(col_cx(0), box_y(0) + 50, "다음 요청 대기", 13, MUTED, KR, "middle")

# 요청 완료 화살표 (손님 → 프록시)
d.arrow([(col_cx(0), box_y(0) + BOX_H), (col_cx(0), box_y(1))], c=MUTED, m="ar", sw=1.3)

# Lane 1 (프록시)
d.box(col_x(0), box_y(1), CW, BOX_H, PAPER2, RULE, 0.9, 6)
d.t(col_cx(0), box_y(1) + 24, "호스트당 빈 연결 2", 12, INK, KR, "middle", 600)
d.t(col_cx(0), box_y(1) + 42, "풀 2 · 48 닫힘", 13, WARN, KR, "middle", 600)
d.t(col_cx(0), box_y(1) + 58, "pconn.close", 11, MUTED, MONO, "middle")

# 소켓 닫힘 화살표 (프록시 → 포트)
d.arrow([(col_cx(0), box_y(1) + BOX_H), (col_cx(0), box_y(2))], c=WARN, m="warn", sw=1.3)

# Lane 2 (출발 포트)
d.box(col_x(0), box_y(2), CW, BOX_H, PAPER2, RULE, 0.9, 6)
d.t(col_cx(0), box_y(2) + 24, "48 → TIME_WAIT", 12, INK, MONO, "middle", 600)
draw_port_bar(d, col_x(0), box_y(2) + 33, 48, 28232, MUTED)

# --- Col 1 (2단계: 새 연결) ---
# Lane 0 (손님)
d.box(col_x(1), box_y(0), CW, BOX_H, PAPER2, RULE, 0.9, 6)
d.t(col_cx(1), box_y(0) + 28, "다음 50 요청", 13, INK, KR, "middle", 600)
d.t(col_cx(1), box_y(0) + 50, "첫 9초 200 OK (16:47)", 12, OK, KR, "middle", 600)

# 요청 재전송 화살표 (손님 → 프록시)
d.arrow([(col_cx(1), box_y(0) + BOX_H), (col_cx(1), box_y(1))], c=MUTED, m="ar", sw=1.3)

# Lane 1 (프록시)
d.box(col_x(1), box_y(1), CW, BOX_H, PAPER2, RULE, 0.9, 6)
d.t(col_cx(1), box_y(1) + 24, "풀 2 + 신규 48", 13, INK, KR, "middle", 600)
d.t(col_cx(1), box_y(1) + 42, "새 연결 1,364/s", 13, WARN, KR, "middle", 600)
d.t(col_cx(1), box_y(1) + 58, "17:53:45", 11, MUTED, MONO, "middle")

# 연결 누적 화살표 (프록시 → 포트)
d.arrow([(col_cx(1), box_y(1) + BOX_H), (col_cx(1), box_y(2))], c=WARN, m="warn", sw=1.3)

# Lane 2 (출발 포트)
d.box(col_x(1), box_y(2), CW, BOX_H, PAPER2, RULE, 0.9, 6)
d.t(col_cx(1), box_y(2) + 24, "TIME_WAIT 2,079", 12, INK, MONO, "middle", 600)
draw_port_bar(d, col_x(1), box_y(2) + 33, 2079, 28232, WARN)
d.t(col_cx(1), box_y(2) + 59, "17:53:40", 11, MUTED, MONO, "middle")

# --- Col 2 (3단계: 포트 누적) ---
# Lane 0 (손님)
d.box(col_x(2), box_y(0), CW, BOX_H, PAPER2, RULE, 0.9, 6)
d.t(col_cx(2), box_y(0) + 28, "부하 -c 50", 13, INK, KR, "middle", 600)
d.t(col_cx(2), box_y(0) + 50, "요청 4,707/s", 13, MUTED, KR, "middle")

# 요청 전달 화살표 (손님 → 프록시)
d.arrow([(col_cx(2), box_y(0) + BOX_H), (col_cx(2), box_y(1))], c=MUTED, m="ar", sw=1.3)

# Lane 1 (프록시)
d.box(col_x(2), box_y(1), CW, BOX_H, PAPER2, RULE, 0.9, 6)
d.t(col_cx(2), box_y(1) + 24, "재사용 3,346/s", 13, INK, KR, "middle", 600)
d.t(col_cx(2), box_y(1) + 42, "닫힘 ≫ 해제", 13, WARN, KR, "middle", 600)
d.t(col_cx(2), box_y(1) + 58, "60s 유지", 13, MUTED, KR, "middle")

# 포트 잠식 화살표 (프록시 → 포트)
d.arrow([(col_cx(2), box_y(1) + BOX_H), (col_cx(2), box_y(2))], c=WARN, m="warn", sw=1.3)

# Lane 2 (출발 포트)
d.box(col_x(2), box_y(2), CW, BOX_H, PAPER2, RULE, 0.9, 6)
d.t(col_cx(2), box_y(2) + 24, "TIME_WAIT 28,213", 12, WARN, MONO, "middle", 600)
draw_port_bar(d, col_x(2), box_y(2) + 33, 28213, 28232, WARN)
d.t(col_cx(2), box_y(2) + 59, "18,731→28,213", 11, WARN, MONO, "middle")

# --- Col 3 (4단계: 포트 고갈 - FOCAL) ---
# Lane 2 (출발 포트 - FOCAL: 포트 28,232개 완전 소진)
d.tone(col_x(3), box_y(2), CW, BOX_H, ACC, 6, "14", 1.6)
d.t(col_cx(3), box_y(2) + 24, "포트 28,232 고갈", 13, ACC, KR, "middle", 600)
draw_port_bar(d, col_x(3), box_y(2) + 33, 28232, 28232, ACC)
d.t(col_cx(3), box_y(2) + 59, "32768–60999", 11, ACC, MONO, "middle")

# 역방향 에러 전파 화살표: 포트 고갈로 프록시 dial 실패 (포트 → 프록시)
d.arrow([(col_cx(3), box_y(2)), (col_cx(3), box_y(1) + BOX_H)], c=ACC, m="acc", sw=1.4)

# Lane 1 (프록시 - WARN: 새 연결 불가 및 dial 실패)
d.box(col_x(3), box_y(1), CW, BOX_H, PAPER2, RULE, 0.9, 6)
d.t(col_cx(3), box_y(1) + 24, "새 연결 0 · dial 실패", 13, WARN, KR, "middle", 600)
d.t(col_cx(3), box_y(1) + 42, "cannot assign", 11, WARN, MONO, "middle")
d.t(col_cx(3), box_y(1) + 58, "requested address", 11, WARN, MONO, "middle")

# 역방향 에러 전파 화살표: UF 502 반환 (프록시 → 손님)
d.arrow([(col_cx(3), box_y(1)), (col_cx(3), box_y(0) + BOX_H)], c=BAD, m="bad", sw=1.4)

# Lane 0 (손님 - 결과 칸: UF 502 급증 및 누적 결과)
d.box(col_x(3), box_y(0), CW, BOX_H, PAPER2, BAD, 1.2, 6)
d.t(col_cx(3), box_y(0) + 24, "502 (UF)", 13, BAD, MONO, "middle", 600)
d.t(col_cx(3), box_y(0) + 42, "UF 약 750/s (17:53)", 12, WARN, KR, "middle")
d.t(col_cx(3), box_y(0) + 58, "37,381 / 88,831 (16:47)", 11, BAD, MONO, "middle", 600)

# 4. 범례 (Legend)
d.legend(440, [("핵심 고갈 (focal)", ACC), ("장애·에러", WARN), ("502 반환", BAD), ("정상", OK)])

d.save("01-01-i3-port-exhaustion.svg")
