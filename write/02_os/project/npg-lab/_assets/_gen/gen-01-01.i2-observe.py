# 01-01-i2-observe — I2 장애 관측 신호 8단계와 가설 검증 흐름
# 본문 요구(01-01 I2 가끔 POST 만 502 가 난다): 장애 관측 신호 1~8단계를 거치며 가설을 검증하고, 버린 가설과 남긴 결론을 분기 흐름으로 보인다.
# 타입 스펙: type-flowchart
# 사실 출처: ch08-server-idle-close-post-502.md:22-31
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
    "FLOWCHART · CH08 I2 DIAGNOSIS",
    "I2 장애 관측 신호와 가설 검증 흐름",
    "간헐적 POST 502 장애에서 수집한 8단계 관측 신호와 가설의 채택·폐기 판정 과정",
    lead="초록 그래프 → 쉰 연결 → 미도달 → FIN 경합 → 보관 차이 → 재시도"
)

# ── 1행: 단계 1 ~ 4 ──────────────────────────────────────────────

# 1단계 (Col 0) — 모니터링 가설 버림
x0 = col_x(0)
d.box(x0, ROW1_Y, CW, BOX1_H, fill=PAPER2, stroke=RULE, sw=0.9, r=6)
d.t(x0 + 16, ROW1_Y + 26, "1단계 · 모니터링", 14, INK, KR, "start", 600)
d.tone(x0 + CW - 52, ROW1_Y + 12, 40, 20, WARN, 4, "22", 1.0)
d.t(x0 + CW - 32, ROW1_Y + 26, "버림", 13, WARN, KR, "middle", 600)
d.line(x0 + 12, ROW1_Y + 40, x0 + CW - 12, ROW1_Y + 40, RULE, 0.6)
d.t(x0 + 16, ROW1_Y + 62, "1초 그래프 거의 초록", 13, INK, KR, "start", 600)
d.t(x0 + 16, ROW1_Y + 86, "실패 없음 ✗ · UC 44/1813", 12, MUTED, KR, "start")

# 1단계 → 2·3단계 화살표
d.arrow([(x0 + CW, ROW1_Y + BOX1_H // 2), (col_x(1), ROW1_Y + BOX1_H // 2)], c=MUTED, m="ar", sw=1.3)

# 2·3단계 (Col 1) — 접근 로그 및 유휴 경계 (focal 색상 강조)
x1 = col_x(1)
d.tone(x1, ROW1_Y, CW, BOX1_H, ACC, 6, "14", 1.6)
d.t(x1 + 16, ROW1_Y + 26, "2·3단계 · 접근 로그", 14, ACC, KR, "start", 600)
d.tone(x1 + CW - 52, ROW1_Y + 12, 40, 20, ACC, 4, "22", 1.0)
d.t(x1 + CW - 32, ROW1_Y + 26, "남김", 13, ACC, KR, "middle", 600)
d.line(x1 + 12, ROW1_Y + 40, x1 + CW - 12, ROW1_Y + 40, RULE, 0.6)
d.t(x1 + 16, ROW1_Y + 62, "502 9건 POST · reused", 12, INK, MONO, "start", 600)
d.t(x1 + 16, ROW1_Y + 86, "idle 807~973ms (1초 가까이)", 12, ACC, KR, "start", 600)

# 2·3단계 → 4단계 화살표
d.arrow([(x1 + CW, ROW1_Y + BOX1_H // 2), (col_x(2), ROW1_Y + BOX1_H // 2)], c=MUTED, m="ar", sw=1.3)

# 4단계 (Col 2) — 백엔드 요청 수 대조
x2 = col_x(2)
d.box(x2, ROW1_Y, CW, BOX1_H, fill=PAPER2, stroke=RULE, sw=0.9, r=6)
d.t(x2 + 16, ROW1_Y + 26, "4단계 · 백엔드 대조", 14, INK, KR, "start", 600)
d.tone(x2 + CW - 52, ROW1_Y + 12, 40, 20, OK, 4, "22", 1.0)
d.t(x2 + CW - 32, ROW1_Y + 26, "남김", 13, OK, KR, "middle", 600)
d.line(x2 + 12, ROW1_Y + 40, x2 + CW - 12, ROW1_Y + 40, RULE, 0.6)
d.t(x2 + 16, ROW1_Y + 62, "프록시 1813 − 백엔드 1770", 12, INK, MONO, "start", 600)
d.t(x2 + 16, ROW1_Y + 86, "43 ≈ UC 44 (미도달)", 13, MUTED, KR, "start")

# 4단계 → 5단계 꺾은 화살표 (오른쪽 아래에서 왼쪽 2행 시작으로)
d.arrow([
    (col_cx(2), ROW1_Y + BOX1_H),
    (col_cx(2), 240),
    (col_cx(0), 240),
    (col_cx(0), ROW2_Y)
], c=MUTED, m="ar", sw=1.3)

# ── 2행: 단계 5 ~ 8 ──────────────────────────────────────────────

# 5단계 (Col 0) — 유휴 연결 보관
d.box(x0, ROW2_Y, CW, BOX2_H, fill=PAPER2, stroke=RULE, sw=0.9, r=6)
d.t(x0 + 16, ROW2_Y + 26, "5단계 · 유휴 보관", 14, INK, KR, "start", 600)
d.tone(x0 + CW - 52, ROW2_Y + 12, 40, 20, OK, 4, "22", 1.0)
d.t(x0 + CW - 32, ROW2_Y + 26, "남김", 13, OK, KR, "middle", 600)
d.line(x0 + 12, ROW2_Y + 40, x0 + CW - 12, ROW2_Y + 40, RULE, 0.6)
d.t(x0 + 16, ROW2_Y + 62, "IdleConnTimeout 90s", 13, INK, MONO, "start", 600)
d.t(x0 + 16, ROW2_Y + 86, "서버 선행 close · FIN 경합", 13, MUTED, KR, "start")

# 5단계 → 6단계 화살표
d.arrow([(x0 + CW, ROW2_Y + BOX2_H // 2), (col_x(1), ROW2_Y + BOX2_H // 2)], c=MUTED, m="ar", sw=1.3)

# 6단계 (Col 1) — 서버 보관 시간 차이
d.box(x1, ROW2_Y, CW, BOX2_H, fill=PAPER2, stroke=RULE, sw=0.9, r=6)
d.t(x1 + 16, ROW2_Y + 26, "6단계 · 보관 불일치", 14, INK, KR, "start", 600)
d.tone(x1 + CW - 52, ROW2_Y + 12, 40, 20, OK, 4, "22", 1.0)
d.t(x1 + CW - 32, ROW2_Y + 26, "남김", 13, OK, KR, "middle", 600)
d.line(x1 + 12, ROW2_Y + 40, x1 + CW - 12, ROW2_Y + 40, RULE, 0.6)
d.t(x1 + 16, ROW2_Y + 62, "idle_close 1s vs 90s", 13, INK, MONO, "start", 600)
d.t(x1 + 16, ROW2_Y + 86, "서버 IdleTimeout 흉내", 13, MUTED, KR, "start")

# 6단계 → 7·8단계 화살표
d.arrow([(x1 + CW, ROW2_Y + BOX2_H // 2), (col_x(2), ROW2_Y + BOX2_H // 2)], c=MUTED, m="ar", sw=1.3)

# 7·8단계 (Col 2) — 재시도 판정 (shouldRetryRequest / isReplayable)
d.box(x2, ROW2_Y, CW, BOX2_H, fill=PAPER2, stroke=RULE, sw=0.9, r=6)
d.t(x2 + 16, ROW2_Y + 26, "7·8단계 · 재시도 판정", 14, INK, KR, "start", 600)
d.tone(x2 + CW - 52, ROW2_Y + 12, 40, 20, OK, 4, "22", 1.0)
d.t(x2 + CW - 32, ROW2_Y + 26, "남김", 13, OK, KR, "middle", 600)
d.line(x2 + 12, ROW2_Y + 40, x2 + CW - 12, ROW2_Y + 40, RULE, 0.6)
d.t(x2 + 16, ROW2_Y + 62, "GET 0 / POST 9 대조", 12, INK, KR, "start", 600)
d.t(x2 + 16, ROW2_Y + 86, "shouldRetry: GET 재전송", 12, MUTED, MONO, "start")

# ── 3행: 곁가지 (보정된 가설 둘) ─────────────────────────

# 5단계 곁가지 아래 화살표
d.arrow([(col_cx(0), ROW2_Y + BOX2_H), (col_cx(0), BRANCH_Y)], c=SOFT, m="soft", sw=1.3, dash="4 4")

# 5단계 곁가지 상자 (보정된 가설)
d.box(x0, BRANCH_Y, CW, BRANCH_H, fill=PAPER2, stroke=RULE, sw=0.9, r=6)
d.t(x0 + 16, BRANCH_Y + 24, "보정된 가설", 13, MUTED, KR, "start", 600)
d.tone(x0 + CW - 52, BRANCH_Y + 10, 40, 20, SOFT, 4, "22", 1.0)
d.t(x0 + CW - 32, BRANCH_Y + 24, "보정", 13, MUTED, KR, "middle", 600)
d.line(x0 + 12, BRANCH_Y + 36, x0 + CW - 12, BRANCH_Y + 36, RULE, 0.6)
d.t(x0 + 16, BRANCH_Y + 52, "CLOSE_WAIT 장기 잔류 ✗", 13, INK, KR, "start", 600)
d.t(x0 + 16, BRANCH_Y + 68, "readLoop FIN 즉시 회수", 12, MUTED, KR, "start")

# 7·8단계 곁가지 아래 화살표
d.arrow([(col_cx(2), ROW2_Y + BOX2_H), (col_cx(2), BRANCH_Y)], c=SOFT, m="soft", sw=1.3, dash="4 4")

# 7·8단계 곁가지 상자 (보정된 가설 — 기록 I2:39 창의 보정)
d.box(x2, BRANCH_Y, CW, BRANCH_H, fill=PAPER2, stroke=RULE, sw=0.9, r=6)
d.t(x2 + 16, BRANCH_Y + 24, "보정된 가설", 13, MUTED, KR, "start", 600)
d.tone(x2 + CW - 52, BRANCH_Y + 10, 40, 20, SOFT, 4, "22", 1.0)
d.t(x2 + CW - 32, BRANCH_Y + 24, "보정", 13, MUTED, KR, "middle", 600)
d.line(x2 + 12, BRANCH_Y + 36, x2 + CW - 12, BRANCH_Y + 36, RULE, 0.6)
d.t(x2 + 16, BRANCH_Y + 52, "모든 멱등 재전송 ✗", 13, INK, KR, "start", 600)
d.t(x2 + 16, BRANCH_Y + 68, "PUT·DELETE 제외 (RFC 차이)", 12, MUTED, KR, "start")

# ── 범례 (Legend) ────────────────────────────────────────────────
d.legend(LEGEND_Y, [
    ("핵심 경계", ACC),
    ("가설 남김", OK),
    ("가설 버림", WARN),
    ("가설 보정", SOFT),
])

d.save("01-01-i2-observe.svg")
