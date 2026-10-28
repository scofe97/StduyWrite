# 01-01-i2-race — 서버가 1초에 닫은 연결로 POST 가 나가 EOF → 502 가 되기까지의 경합 흐름
# 본문 요구(01-01 I2 요약): 백엔드가 1초에 닫은 연결과 프록시의 POST 재사용 사이의 경합 메커니즘을 3개 참여자 레인과 시간 축으로 보인다.
# 타입 스펙: type-swimlane
# 사실 출처: ch08-server-idle-close-post-502.md:17·18·24·25·26·27·28·30·44·45·46·47·50·51·52·96·102·103
import sys
from pathlib import Path

# _assets 및 _gen 경로 등록
ASSETS_DIR = Path(__file__).resolve().parent.parent
GEN_DIR = Path(__file__).resolve().parent
if str(ASSETS_DIR) not in sys.path:
    sys.path.insert(0, str(ASSETS_DIR))
if str(GEN_DIR) not in sys.path:
    sys.path.insert(0, str(GEN_DIR))

from dd import D, INK, MUTED, SOFT, RULE, PAPER2, ACC, WARN, INFO, KR, MONO

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
    "SWIMLANE · CH08 I2 DIAGNOSIS",
    "서버가 1초에 닫은 연결과 POST 경합",
    "fakeinv 백엔드가 1초 만료로 닫은 빈 연결을 프록시가 재사용해 POST 502가 발생한 흐름",
    lead="서버의 FIN 이 프록시에 닿기 전 100ms 지연 틈새로 POST 가 나가 백엔드 기록 없이 502 로 드러납니다.",
)

# 1. 단계 열 머리 (Stage Headers)
stages = [
    "t0 이전 응답",
    "풀 보관 (idle)",
    "t0+1000 닫힘",
    "위험 구간 (focal)",
    "EOF → 502",
]

for c, st_title in enumerate(stages):
    cx = col_cx(c)
    d.t(cx, 124, st_title, 13, INK, KR, "middle", 600)

# 2. 레인 구분선 및 레인 라벨
lane_labels = [
    ("백엔드", "fakeinv"),
    ("프록시", "npgproxy v0"),
    ("손님", "npgload"),
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

# --- Col 0 (t0 이전 응답) ---
# Lane 0 (백엔드)
d.box(col_x(0), box_y(0), CW, BOX_H, PAPER2, RULE, 0.9, 6)
d.t(col_cx(0), box_y(0) + 26, "t0 응답 전송", 11, INK, KR, "middle", 600)
d.t(col_cx(0), box_y(0) + 46, "HTTP 200", 11, MUTED, MONO, "middle")

# 백엔드 → 프록시 응답 전달
d.arrow([(col_cx(0), box_y(0) + BOX_H), (col_cx(0), box_y(1))], c=INFO, m="info", sw=1.3)

# Lane 1 (프록시)
d.box(col_x(0), box_y(1), CW, BOX_H, PAPER2, RULE, 0.9, 6)
d.t(col_cx(0), box_y(1) + 26, "t0+100 수신", 11, INK, KR, "middle", 600)
d.t(col_cx(0), box_y(1) + 46, "idle=0 시작", 11, MUTED, KR, "middle")

# 프록시 → 손님 응답 전달
d.arrow([(col_cx(0), box_y(1) + BOX_H), (col_cx(0), box_y(2))], c=MUTED, m="ar", sw=1.3)

# Lane 2 (손님)
d.box(col_x(0), box_y(2), CW, BOX_H, PAPER2, RULE, 0.9, 6)
d.t(col_cx(0), box_y(2) + 26, "응답 수신", 11, INK, KR, "middle", 600)
d.t(col_cx(0), box_y(2) + 46, "HTTP 200 수신", 11, MUTED, MONO, "middle")

# --- Col 1 (풀 보관 idle) ---
# Lane 0 (백엔드: 숨긴 조건 idle_close 1s)
d.tone(col_x(1), box_y(0), CW, BOX_H, INFO, 6, "10", 1.0)
d.t(col_cx(1), box_y(0) + 26, "idle_close 1s", 11, INFO, MONO, "middle", 600)
d.t(col_cx(1), box_y(0) + 46, "타이머 대기 중", 11, MUTED, KR, "middle")

# Lane 1 (프록시)
d.box(col_x(1), box_y(1), CW, BOX_H, PAPER2, RULE, 0.9, 6)
d.t(col_cx(1), box_y(1) + 26, "풀 보관 (idle x)", 11, INK, KR, "middle", 600)
d.t(col_cx(1), box_y(1) + 46, "IdleConnTimeout 90s", 11, MUTED, MONO, "middle")

# Lane 2 (손님)
d.box(col_x(1), box_y(2), CW, BOX_H, PAPER2, RULE, 0.9, 6)
d.t(col_cx(1), box_y(2) + 26, "단건 조회 GET", 11, INK, KR, "middle", 600)
d.t(col_cx(1), box_y(2) + 46, "121건 성공", 11, MUTED, KR, "middle")

# --- Col 2 (t0+1000 닫힘) ---
# Lane 0 (백엔드)
d.box(col_x(2), box_y(0), CW, BOX_H, PAPER2, RULE, 0.9, 6)
d.t(col_cx(2), box_y(0) + 26, "t0+1000 close()", 11, WARN, MONO, "middle", 600)
d.t(col_cx(2), box_y(0) + 46, "서버 먼저 닫음", 11, WARN, KR, "middle")

# 백엔드 → 프록시 (FIN 전송 중, netem 100ms)
d.arrow([(col_cx(2), box_y(0) + BOX_H), (col_cx(2), box_y(1))], c=WARN, m="warn", sw=1.3)

# Lane 1 (프록시)
d.box(col_x(2), box_y(1), CW, BOX_H, PAPER2, RULE, 0.9, 6)
d.t(col_cx(2), box_y(1) + 26, "FIN 아직 미도착", 11, INK, KR, "middle", 600)
d.t(col_cx(2), box_y(1) + 46, "연결 유효 판단", 11, MUTED, KR, "middle")

# 손님 → 프록시 (장비 등록 POST 전송)
d.arrow([(col_cx(2), box_y(2)), (col_cx(2), box_y(1) + BOX_H)], c=MUTED, m="ar", sw=1.3)

# Lane 2 (손님)
d.box(col_x(2), box_y(2), CW, BOX_H, PAPER2, RULE, 0.9, 6)
d.t(col_cx(2), box_y(2) + 26, "장비 등록 POST", 11, INK, KR, "middle", 600)
d.t(col_cx(2), box_y(2) + 46, "rate 1 poisson", 11, MUTED, MONO, "middle")

# --- Col 3 (경합 구간 - FOCAL) ---
# Lane 0 (백엔드)
d.box(col_x(3), box_y(0), CW, BOX_H, PAPER2, RULE, 0.9, 6)
d.t(col_cx(3), box_y(0) + 26, "t0+200+x POST 도착", 11, INK, KR, "middle", 600)
d.t(col_cx(3), box_y(0) + 46, "이미 닫힘 · 기록 없음", 11, MUTED, KR, "middle")

# 프록시 → 백엔드 (POST 전송)
d.arrow([(col_cx(3), box_y(1)), (col_cx(3), box_y(0) + BOX_H)], c=ACC, m="acc", sw=1.4)

# Lane 1 (프록시 - FOCAL: 백엔드는 닫았고 FIN은 못 받음)
d.tone(col_x(3), box_y(1), CW, BOX_H, ACC, 6, "14", 1.6)
d.t(col_cx(3), box_y(1) + 26, "idle 800~1000ms", 11, ACC, MONO, "middle", 600)
d.t(col_cx(3), box_y(1) + 46, "502 9건 (807~973ms)", 12, ACC, KR, "middle", 600)

# Lane 2 (손님)
d.box(col_x(3), box_y(2), CW, BOX_H, PAPER2, RULE, 0.9, 6)
d.t(col_cx(3), box_y(2) + 26, "장비 등록 POST", 11, INK, KR, "middle", 600)
d.t(col_cx(3), box_y(2) + 46, "reused=true", 11, MUTED, MONO, "middle")

# --- Col 4 (EOF → 502) ---
# Lane 0 (백엔드)
d.box(col_x(4), box_y(0), CW, BOX_H, PAPER2, RULE, 0.9, 6)
d.t(col_cx(4), box_y(0) + 26, "FIN → 프록시", 11, INK, KR, "middle", 600)
d.t(col_cx(4), box_y(0) + 46, "t0+1100 도착", 11, MUTED, KR, "middle")

# 백엔드 → 프록시 (EOF)
d.arrow([(col_cx(4), box_y(0) + BOX_H), (col_cx(4), box_y(1))], c=WARN, m="warn", sw=1.3)

# Lane 1 (프록시 - WARN)
d.box(col_x(4), box_y(1), CW, BOX_H, PAPER2, RULE, 0.9, 6)
d.t(col_cx(4), box_y(1) + 26, "EOF (flags=UC)", 11, WARN, MONO, "middle", 600)
d.t(col_cx(4), box_y(1) + 46, "POST 재시도 불가", 11, WARN, KR, "middle", 600)

# 프록시 → 손님 (502 반환)
d.arrow([(col_cx(4), box_y(1) + BOX_H), (col_cx(4), box_y(2))], c=WARN, m="warn", sw=1.4)

# Lane 2 (손님 - WARN)
d.box(col_x(4), box_y(2), CW, BOX_H, PAPER2, RULE, 0.9, 6)
d.t(col_cx(4), box_y(2) + 26, "502 Bad Gateway", 12, WARN, MONO, "middle", 600)
d.t(col_cx(4), box_y(2) + 46, "등록 실패 (9건)", 11, WARN, KR, "middle", 600)

# 4. 범례 (Legend)
d.legend(428, [("핵심 경합 (focal)", ACC), ("장애 관측값", WARN), ("숨긴 주입 조건", INFO)])
d.t(932, 450, "주입 조건 (진단 뒤 공개): idle_close 1s · netem 100ms", 11, SOFT, KR, "end")

d.save("01-01-i2-race.svg")
