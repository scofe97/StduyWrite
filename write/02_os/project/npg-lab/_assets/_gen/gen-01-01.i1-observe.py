# 01-01-i1-observe — I1 장애 관측 신호 6단계와 가설 검증 흐름
# 본문 요구(01-01 I1 slow search starves lookup): 장애 관측 신호 1~6단계를 거치며 가설을 검증하고, 버린 가설과 남긴 결론을 분기 흐름으로 보인다.
# 타입 스펙: type-flowchart
# 사실 출처: ch08-slow-search-starves-lookup.md:25-30·57-58
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
    "FLOWCHART · CH08 I1 DIAGNOSIS",
    "I1 장애 관측 신호와 가설 검증 흐름",
    "단건 조회 지연 장애에서 수집한 6단계 관측 신호와 가설의 채택·폐기 판정 과정",
    lead="증상 → 줄 위치 → 주기 → 창구 계산 → 끊는 쪽 → 취소"
)

# ── 1행: 단계 1 ~ 3 ──────────────────────────────────────────────

# 1단계 (Col 0) — 증상
x0 = col_x(0)
d.box(x0, ROW1_Y, CW, BOX1_H, fill=PAPER2, stroke=RULE, sw=0.9, r=6)
d.t(x0 + 16, ROW1_Y + 26, "1단계 · 프록시", 14, INK, KR, "start", 600)
d.tone(x0 + CW - 52, ROW1_Y + 12, 40, 20, INFO, 4, "22", 1.0)
d.t(x0 + CW - 32, ROW1_Y + 26, "증상", 13, INFO, KR, "middle", 600)
d.line(x0 + 12, ROW1_Y + 40, x0 + CW - 12, ROW1_Y + 40, RULE, 0.6)
d.t(x0 + 16, ROW1_Y + 62, "inflight 지속 상승", 13, INK, KR, "start", 600)
d.t(x0 + 16, ROW1_Y + 86, "도착률 불변 · 체류시간 증가", 13, MUTED, KR, "start")

# 1단계 → 2단계 화살표
d.arrow([(x0 + CW, ROW1_Y + BOX1_H // 2), (col_x(1), ROW1_Y + BOX1_H // 2)], c=MUTED, m="ar", sw=1.3)

# 2단계 (Col 1) — 줄은 백엔드
x1 = col_x(1)
d.box(x1, ROW1_Y, CW, BOX1_H, fill=PAPER2, stroke=RULE, sw=0.9, r=6)
d.t(x1 + 16, ROW1_Y + 26, "2단계 · 대기열", 14, INK, KR, "start", 600)
d.tone(x1 + CW - 52, ROW1_Y + 12, 40, 20, OK, 4, "22", 1.0)
d.t(x1 + CW - 32, ROW1_Y + 26, "남김", 13, OK, KR, "middle", 600)
d.line(x1 + 12, ROW1_Y + 40, x1 + CW - 12, ROW1_Y + 40, RULE, 0.6)
d.t(x1 + 16, ROW1_Y + 62, "queued 860→2933 · conns 2966", 12, INK, MONO, "start", 600)
d.t(x1 + 16, ROW1_Y + 86, "줄은 백엔드", 13, MUTED, KR, "start")

# 2단계 → 3단계 화살표
d.arrow([(x1 + CW, ROW1_Y + BOX1_H // 2), (col_x(2), ROW1_Y + BOX1_H // 2)], c=MUTED, m="ar", sw=1.3)

# 3단계 (Col 2) — 8s 주기
x2 = col_x(2)
d.box(x2, ROW1_Y, CW, BOX1_H, fill=PAPER2, stroke=RULE, sw=0.9, r=6)
d.t(x2 + 16, ROW1_Y + 26, "3단계 · 주기성", 14, INK, KR, "start", 600)
d.tone(x2 + CW - 52, ROW1_Y + 12, 40, 20, OK, 4, "22", 1.0)
d.t(x2 + CW - 32, ROW1_Y + 26, "남김", 13, OK, KR, "middle", 600)
d.line(x2 + 12, ROW1_Y + 40, x2 + CW - 12, ROW1_Y + 40, RULE, 0.6)
d.t(x2 + 16, ROW1_Y + 62, "get n=0 · 15:07:20·28·36", 12, INK, MONO, "start", 600)
d.t(x2 + 16, ROW1_Y + 86, "8s 주기 반환 (창구 연동)", 13, MUTED, KR, "start")

# 3단계 → 4단계 꺾은 화살표 (오른쪽 아래에서 왼쪽 2행 시작으로)
d.arrow([
    (col_cx(2), ROW1_Y + BOX1_H),
    (col_cx(2), 240),
    (col_cx(0), 240),
    (col_cx(0), ROW2_Y)
], c=MUTED, m="ar", sw=1.3)

# ── 2행: 단계 4 ~ 6 ──────────────────────────────────────────────

# 4단계 (Col 0) — 창구 잠식 (focal 색상 강조)
d.tone(x0, ROW2_Y, CW, BOX2_H, ACC, 6, "14", 1.6)
d.t(x0 + 16, ROW2_Y + 26, "4단계 · 창구 잠식", 14, ACC, KR, "start", 600)
d.tone(x0 + CW - 52, ROW2_Y + 12, 40, 20, ACC, 4, "22", 1.0)
d.t(x0 + CW - 32, ROW2_Y + 26, "남김", 13, ACC, KR, "middle", 600)
d.line(x0 + 12, ROW2_Y + 40, x0 + CW - 12, ROW2_Y + 40, RULE, 0.6)
d.t(x0 + 16, ROW2_Y + 62, "검색 5/s × 8s = 40", 13, INK, MONO, "start", 600)
d.t(x0 + 16, ROW2_Y + 86, "40 > 창구 32 (줄 누적)", 13, ACC, KR, "start", 600)

# 4단계 → 5단계 화살표
d.arrow([(x0 + CW, ROW2_Y + BOX2_H // 2), (col_x(1), ROW2_Y + BOX2_H // 2)], c=MUTED, m="ar", sw=1.3)

# 5단계 (Col 1) — 종료 주체 판정
d.box(x1, ROW2_Y, CW, BOX2_H, fill=PAPER2, stroke=RULE, sw=0.9, r=6)
d.t(x1 + 16, ROW2_Y + 26, "5단계 · 종료 주체", 14, INK, KR, "start", 600)
d.tone(x1 + CW - 52, ROW2_Y + 12, 40, 20, OK, 4, "22", 1.0)
d.t(x1 + CW - 32, ROW2_Y + 26, "남김", 13, OK, KR, "middle", 600)
d.line(x1 + 12, ROW2_Y + 40, x1 + CW - 12, ROW2_Y + 40, RULE, 0.6)
d.t(x1 + 16, ROW2_Y + 62, "DC 49150 · UT 0", 13, INK, MONO, "start", 600)
d.t(x1 + 16, ROW2_Y + 86, "손님 30s에 포기 (timeout)", 13, MUTED, KR, "start")

# 5단계 → 6단계 화살표
d.arrow([(x1 + CW, ROW2_Y + BOX2_H // 2), (col_x(2), ROW2_Y + BOX2_H // 2)], c=MUTED, m="ar", sw=1.3)

# 6단계 (Col 2) — 취소 처리 판정
d.box(x2, ROW2_Y, CW, BOX2_H, fill=PAPER2, stroke=RULE, sw=0.9, r=6)
d.t(x2 + 16, ROW2_Y + 26, "6단계 · 취소 처리", 14, INK, KR, "start", 600)
d.tone(x2 + CW - 52, ROW2_Y + 12, 40, 20, OK, 4, "22", 1.0)
d.t(x2 + CW - 32, ROW2_Y + 26, "남김", 13, OK, KR, "middle", 600)
d.line(x2 + 12, ROW2_Y + 40, x2 + CW - 12, ROW2_Y + 40, RULE, 0.6)
d.t(x2 + 16, ROW2_Y + 62, "worked_after_cancel 26204", 12, INK, MONO, "start", 600)
d.t(x2 + 16, ROW2_Y + 86, "취소 받고 무시 (ctx 무시)", 13, MUTED, KR, "start")

# ── 3행: 곁가지 (버린 가설 / 절반의 가설) ───────────────────────

# 5단계 곁가지 아래 화살표
d.arrow([(col_cx(1), ROW2_Y + BOX2_H), (col_cx(1), BRANCH_Y)], c=WARN, m="warn", sw=1.3, dash="4 4")

# 5단계 곁가지 상자 (버린 가설)
d.tone(x1, BRANCH_Y, CW, BRANCH_H, WARN, 6, "10", 1.1)
d.t(x1 + 16, BRANCH_Y + 24, "버린 가설", 13, WARN, KR, "start", 600)
d.tone(x1 + CW - 52, BRANCH_Y + 10, 40, 20, WARN, 4, "22", 1.0)
d.t(x1 + CW - 32, BRANCH_Y + 24, "버림", 13, WARN, KR, "middle", 600)
d.line(x1 + 12, BRANCH_Y + 36, x1 + CW - 12, BRANCH_Y + 36, RULE, 0.6)
d.t(x1 + 16, BRANCH_Y + 52, "끊는 쪽 = 프록시 ✗", 13, INK, KR, "start", 600)
d.t(x1 + 16, BRANCH_Y + 68, "UT 0 (응답 기한 무제한)", 12, MUTED, KR, "start")

# 6단계 곁가지 아래 화살표
d.arrow([(col_cx(2), ROW2_Y + BOX2_H), (col_cx(2), BRANCH_Y)], c=MUTED, m="ar", sw=1.3, dash="4 4")

# 6단계 곁가지 상자 (절반의 가설)
d.box(x2, BRANCH_Y, CW, BRANCH_H, fill=PAPER2, stroke=RULE, sw=0.9, r=6)
d.t(x2 + 16, BRANCH_Y + 24, "절반의 가설", 13, MUTED, KR, "start", 600)
d.tone(x2 + CW - 52, BRANCH_Y + 10, 40, 20, SOFT, 4, "22", 1.0)
d.t(x2 + CW - 32, BRANCH_Y + 24, "절반", 13, MUTED, KR, "middle", 600)
d.line(x2 + 12, BRANCH_Y + 36, x2 + CW - 12, BRANCH_Y + 36, RULE, 0.6)
d.t(x2 + 16, BRANCH_Y + 52, "취소를 모른다 (절반 타당)", 13, INK, KR, "start", 600)
d.t(x2 + 16, BRANCH_Y + 68, "Go 서버 ctx 취소 전달됨", 12, MUTED, KR, "start")

# ── 범례 (Legend) ────────────────────────────────────────────────
d.legend(LEGEND_Y, [
    ("핵심 병목", ACC),
    ("가설 남김", OK),
    ("가설 버림", WARN),
    ("관측 증상", INFO),
])

d.save("01-01-i1-observe.svg")
