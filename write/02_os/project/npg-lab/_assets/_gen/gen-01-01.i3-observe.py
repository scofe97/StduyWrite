# 01-01-i3-observe — I3 포트 고갈 장애 관측 신호 7단계와 가설 검증 흐름
# 본문 요구(01-01 I3 port exhaustion): 장애 관측 신호와 가설의 채택·폐기 과정을 보이고 원인 기본값과 보정 사실을 분기 흐름으로 밝힌다.
# 타입 스펙: type-flowchart
# 사실 출처: ch08-port-exhaustion-time-wait.md:17-27,33
import sys
from pathlib import Path

# _assets 및 _gen 경로 등록
ASSETS_DIR = Path(__file__).resolve().parent.parent
GEN_DIR = Path(__file__).resolve().parent
if str(ASSETS_DIR) not in sys.path:
    sys.path.insert(0, str(ASSETS_DIR))
if str(GEN_DIR) not in sys.path:
    sys.path.insert(0, str(GEN_DIR))

from dd import D, INK, MUTED, SOFT, RULE, PAPER2, ACC, OK, WARN, INFO, KR, MONO

W = 960
H = 568

# 3열 격자 치수 (모두 4의 배수)
X0 = 44
CW = 264
GAP_X = 40

# 행 Y 좌표 및 높이 (모두 4의 배수)
ROW1_Y = 112
BOX1_H = 104

ROW2_Y = 264
BOX2_H = 104

BRANCH_Y = 408
BRANCH_H = 80

LEGEND_Y = 520


def col_x(c):
    return X0 + c * (CW + GAP_X)


def col_cx(c):
    return col_x(c) + CW // 2


d = D(
    W,
    H,
    "FLOWCHART · CH08 I3 DIAGNOSIS",
    "I3 장애 관측 신호와 가설 검증 흐름",
    "부하 시험 포트 고갈 장애에서 수집한 관측 신호와 가설의 채택·폐기 판정 과정",
    lead="증상 → 종료 주체 → 처리량 검증 → 대기열 검증 → 재사용 반증 → 기본값 대조",
)

# ── 1행: 단계 1 ~ 3 ──────────────────────────────────────────────

# 1단계 (Col 0) — 증상 및 포트 고갈 (남김)
x0 = col_x(0)
d.box(x0, ROW1_Y, CW, BOX1_H, fill=PAPER2, stroke=RULE, sw=0.9, r=6)
d.t(x0 + 16, ROW1_Y + 26, "1단계 · 포트 고갈", 14, INK, KR, "start", 600)
d.tone(x0 + CW - 52, ROW1_Y + 12, 40, 20, OK, 4, "22", 1.0)
d.t(x0 + CW - 32, ROW1_Y + 26, "남김", 13, OK, KR, "middle", 600)
d.line(x0 + 12, ROW1_Y + 40, x0 + CW - 12, ROW1_Y + 40, RULE, 0.6)
d.t(x0 + 16, ROW1_Y + 62, "16:47:20 · UF 37381", 12, INK, MONO, "start", 600)
d.t(x0 + 16, ROW1_Y + 86, "TIME_WAIT 출발 포트 소진", 13, MUTED, KR, "start")

# 1단계 → 2단계 화살표
d.arrow([(x0 + CW, ROW1_Y + BOX1_H // 2), (col_x(1), ROW1_Y + BOX1_H // 2)], c=MUTED, m="ar", sw=1.3)

# 2단계 (Col 1) — 종료 주체 판정 (남김)
x1 = col_x(1)
d.box(x1, ROW1_Y, CW, BOX1_H, fill=PAPER2, stroke=RULE, sw=0.9, r=6)
d.t(x1 + 16, ROW1_Y + 26, "2단계 · 종료 주체", 14, INK, KR, "start", 600)
d.tone(x1 + CW - 52, ROW1_Y + 12, 40, 20, OK, 4, "22", 1.0)
d.t(x1 + CW - 32, ROW1_Y + 26, "남김", 13, OK, KR, "middle", 600)
d.line(x1 + 12, ROW1_Y + 40, x1 + CW - 12, ROW1_Y + 40, RULE, 0.6)
d.t(x1 + 16, ROW1_Y + 62, "TIME_WAIT 프록시 누적", 12, INK, KR, "start", 600)
d.t(x1 + 16, ROW1_Y + 86, "프록시가 먼저 닫음", 13, MUTED, KR, "start")

# 2단계 → 3단계 화살표
d.arrow([(x1 + CW, ROW1_Y + BOX1_H // 2), (col_x(2), ROW1_Y + BOX1_H // 2)], c=MUTED, m="ar", sw=1.3)

# 3단계 (Col 2) — 처리량 제한 가설 (버림)
x2 = col_x(2)
d.box(x2, ROW1_Y, CW, BOX1_H, fill=PAPER2, stroke=RULE, sw=0.9, r=6)
d.t(x2 + 16, ROW1_Y + 26, "3단계 · 처리량 가설", 14, INK, KR, "start", 600)
d.tone(x2 + CW - 52, ROW1_Y + 12, 40, 20, WARN, 4, "22", 1.0)
d.t(x2 + CW - 32, ROW1_Y + 26, "버림", 13, WARN, KR, "middle", 600)
d.line(x2 + 12, ROW1_Y + 40, x2 + CW - 12, ROW1_Y + 40, RULE, 0.6)
d.t(x2 + 16, ROW1_Y + 62, "MaxConnsPerHost 0", 12, INK, MONO, "start", 600)
d.t(x2 + 16, ROW1_Y + 86, "처리량 제한 ✗ (상한 없음)", 13, WARN, KR, "start")

# 3단계 → 4단계 꺾은 화살표 (오른쪽 아래에서 왼쪽 2행 시작으로)
d.arrow([
    (col_cx(2), ROW1_Y + BOX1_H),
    (col_cx(2), 240),
    (col_cx(0), 240),
    (col_cx(0), ROW2_Y),
], c=MUTED, m="ar", sw=1.3)

# ── 2행: 단계 4 ~ 6 ──────────────────────────────────────────────

# 4단계 (Col 0) — 대기열 위치 가설 (버림)
d.box(x0, ROW2_Y, CW, BOX2_H, fill=PAPER2, stroke=RULE, sw=0.9, r=6)
d.t(x0 + 16, ROW2_Y + 26, "4단계 · 대기열 가설", 14, INK, KR, "start", 600)
d.tone(x0 + CW - 52, ROW2_Y + 12, 40, 20, WARN, 4, "22", 1.0)
d.t(x0 + CW - 32, ROW2_Y + 26, "버림", 13, WARN, KR, "middle", 600)
d.line(x0 + 12, ROW2_Y + 40, x0 + CW - 12, ROW2_Y + 40, RULE, 0.6)
d.t(x0 + 16, ROW2_Y + 62, "초당 1000 · 열린 연결 ~10", 12, INK, MONO, "start", 600)
d.t(x0 + 16, ROW2_Y + 86, "손님 적재 ✗ (-c 50)", 13, WARN, KR, "start")

# 4단계 → 5단계 화살표
d.arrow([(x0 + CW, ROW2_Y + BOX2_H // 2), (col_x(1), ROW2_Y + BOX2_H // 2)], c=MUTED, m="ar", sw=1.3)

# 5단계 (Col 1) — 연결 재사용 검증 (반증)
d.box(x1, ROW2_Y, CW, BOX2_H, fill=PAPER2, stroke=RULE, sw=0.9, r=6)
d.t(x1 + 16, ROW2_Y + 26, "5단계 · 재사용 검증", 14, INK, KR, "start", 600)
d.tone(x1 + CW - 52, ROW2_Y + 12, 40, 20, WARN, 4, "22", 1.0)
d.t(x1 + CW - 32, ROW2_Y + 26, "반증", 13, WARN, KR, "middle", 600)
d.line(x1 + 12, ROW2_Y + 40, x1 + CW - 12, ROW2_Y + 40, RULE, 0.6)
d.t(x1 + 16, ROW2_Y + 62, "새 연결 1,364/초 · 동시 50", 12, INK, MONO, "start", 600)
d.t(x1 + 16, ROW2_Y + 86, "재사용 ✗ (관찰 반대)", 13, WARN, KR, "start")

# 5단계 → 6단계 화살표
d.arrow([(x1 + CW, ROW2_Y + BOX2_H // 2), (col_x(2), ROW2_Y + BOX2_H // 2)], c=MUTED, m="ar", sw=1.3)

# 6단계 (Col 2) — 기본값 대조 (focal 색상 강조, 남김)
d.tone(x2, ROW2_Y, CW, BOX2_H, ACC, 6, "14", 1.6)
d.t(x2 + 16, ROW2_Y + 26, "6단계 · 기본값 대조", 14, ACC, KR, "start", 600)
d.tone(x2 + CW - 52, ROW2_Y + 12, 40, 20, ACC, 4, "22", 1.0)
d.t(x2 + CW - 32, ROW2_Y + 26, "남김", 13, ACC, KR, "middle", 600)
d.line(x2 + 12, ROW2_Y + 40, x2 + CW - 12, ROW2_Y + 40, RULE, 0.6)
d.t(x2 + 16, ROW2_Y + 62, "MaxIdleConnsPerHost 2", 12, INK, MONO, "start", 600)
d.t(x2 + 16, ROW2_Y + 86, "호스트당 2개 유지 · 닫힘", 13, ACC, KR, "start", 600)

# ── 3행: 곁가지 (보정 꼬리표 / 8단계 풀 역할) ───────────────────────

# 보정 꼬리표 (Cols 0-1) — 사실 관계 2가지 교정
w_cor = 2 * CW + GAP_X
d.box(x0, BRANCH_Y, w_cor, BRANCH_H, fill=PAPER2, stroke=RULE, sw=0.9, r=6)
d.t(x0 + 16, BRANCH_Y + 24, "보정 꼬리표", 13, INFO, KR, "start", 600)
d.tone(x0 + w_cor - 52, BRANCH_Y + 10, 40, 20, INFO, 4, "22", 1.0)
d.t(x0 + w_cor - 32, BRANCH_Y + 24, "보정", 12, INFO, KR, "middle", 600)
d.line(x0 + 12, BRANCH_Y + 36, x0 + w_cor - 12, BRANCH_Y + 36, RULE, 0.6)
d.t(x0 + 16, BRANCH_Y + 52, "자원: fd 아닌 포트 소진", 13, INK, KR, "start", 600)
d.t(x0 + 16, BRANCH_Y + 68, "cannot assign requested address", 11, MUTED, MONO, "start")
d.t(x0 + 296, BRANCH_Y + 52, "기점: 프록시 dial 실패", 13, INK, KR, "start", 600)
d.t(x0 + 296, BRANCH_Y + 68, "dial 실패 → UF 502", 12, MUTED, KR, "start")

# 6단계 곁가지 아래 화살표
d.arrow([(col_cx(2), ROW2_Y + BOX2_H), (col_cx(2), BRANCH_Y)], c=WARN, m="warn", sw=1.3, dash="4 4")

# 8단계 곁가지 상자 (Col 2) — 풀 역할 오해 (버린 가설)
d.tone(x2, BRANCH_Y, CW, BRANCH_H, WARN, 6, "10", 1.1)
d.t(x2 + 16, BRANCH_Y + 24, "8단계 · 풀 역할", 13, WARN, KR, "start", 600)
d.tone(x2 + CW - 52, BRANCH_Y + 10, 40, 20, WARN, 4, "22", 1.0)
d.t(x2 + CW - 32, BRANCH_Y + 24, "버림", 13, WARN, KR, "middle", 600)
d.line(x2 + 12, BRANCH_Y + 36, x2 + CW - 12, BRANCH_Y + 36, RULE, 0.6)
d.t(x2 + 16, BRANCH_Y + 52, "풀은 길목 아닌 지름길", 13, INK, KR, "start", 600)
d.t(x2 + 16, BRANCH_Y + 68, "50 = 풀 2 + 새 연결 48", 12, MUTED, MONO, "start")

# ── 범례 (Legend) ────────────────────────────────────────────────
d.legend(LEGEND_Y, [
    ("핵심 원인", ACC),
    ("가설 남김", OK),
    ("가설 버림", WARN),
    ("원인 보정", INFO),
])

d.save("01-01-i3-observe.svg")
