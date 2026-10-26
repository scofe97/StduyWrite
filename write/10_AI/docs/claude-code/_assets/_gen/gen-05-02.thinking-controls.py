"""확장된 생각 조절 인터페이스와 안전 분류기 플래그 처리 파이프라인.

# 타입 스펙: type-process
"""
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import D, ACC, OK, WARN, BAD, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 464
d = D(
    W, H,
    "THINKING CONTROLS · PROCESS PIPELINE",
    "생각 깊이 조절 인터페이스와 안전 분류기 처리 절차",
    "입력 인터페이스부터 우선순위 판정, 안전 심사, 최종 추론 예산 할당까지의 단계별 흐름",
    lead="노력 값은 환경 변수가 --effort 보다 우선하고, 사이버보안 요청은 폴백, 생물학 요청은 거절로 처리됩니다"
)

LABEL_W = 144
SLOT_W = 196
NODE_W = 168
NODE_H = 56
LANE_H = 84
HEADER_Y = 94
LANE0_Y = 124

# 1. 레인 배경 및 구분선 (3 레인)
for k in range(3):
    y = LANE0_Y + k * LANE_H
    if k % 2 == 0:
        d.o.append(f'<rect x="{LABEL_W}" y="{y}" width="{W - LABEL_W - 16}" height="{LANE_H}" fill="rgba(245,245,243,0.02)"/>')
    d.line(16, y, W - 16, y, RULE, 0.8)

d.line(16, LANE0_Y + 3 * LANE_H, W - 16, LANE0_Y + 3 * LANE_H, RULE, 0.8)
d.line(LABEL_W, LANE0_Y, LABEL_W, LANE0_Y + 3 * LANE_H, RULE, 1.0)

# 레인 이름
lanes = [
    ("인터페이스", "입력 수단"),
    ("정책·분류기", "우선순위 심사"),
    ("추론 엔진", "런타임 예산"),
]
for k, (title, sub) in enumerate(lanes):
    cy = LANE0_Y + k * LANE_H + LANE_H // 2
    d.t(24, cy - 8, title, 13, INK, KR, "start", 600)
    d.t(24, cy + 14, sub, 11, MUTED, KR, "start")

# 2. 단계 머리 (Step Header)
steps = [
    ("1 · 입력 접수", False, False),
    ("2 · 순위 판정", False, False),
    ("3 · 안전 심사", False, False),
    ("4 · 실행", True, False),
]

for j, (st_name, is_focal, is_ok) in enumerate(steps):
    cx = LABEL_W + 16 + j * SLOT_W + NODE_W // 2
    c = ACC if is_focal else (OK if is_ok else INK)
    d.t(cx, HEADER_Y + 16, st_name, 12, c, KR, "middle", 600)

# 3. 연결 화살표 (z-order: 노드보다 먼저 그린다)
# Step 0 (0,0) -> Step 1 (0,1): 수평
x0_r = LABEL_W + 16 + NODE_W
x1_l = LABEL_W + 16 + 1 * SLOT_W
y_lane0 = LANE0_Y + (LANE_H - NODE_H) // 2 + NODE_H // 2
d.arrow([(x0_r, y_lane0), (x1_l, y_lane0)], MUTED, "ar", 1.4)

# Step 1: (0,1) -> (1,1): 수직 하강
x1_c = LABEL_W + 16 + 1 * SLOT_W + NODE_W // 2
y1_bot0 = LANE0_Y + (LANE_H - NODE_H) // 2 + NODE_H
y1_top1 = LANE0_Y + 1 * LANE_H + (LANE_H - NODE_H) // 2
d.arrow([(x1_c, y1_bot0), (x1_c, y1_top1)], MUTED, "ar", 1.4)

# Step 1 (1,1) -> Step 2 (1,2): 수평
x1_r = LABEL_W + 16 + 1 * SLOT_W + NODE_W
x2_l = LABEL_W + 16 + 2 * SLOT_W
y_lane1 = LANE0_Y + 1 * LANE_H + (LANE_H - NODE_H) // 2 + NODE_H // 2
d.arrow([(x1_r, y_lane1), (x2_l, y_lane1)], MUTED, "ar", 1.4)

# Step 2: (1,2) -> (2,2): 수직 하강
x2_c = LABEL_W + 16 + 2 * SLOT_W + NODE_W // 2
y2_bot1 = LANE0_Y + 1 * LANE_H + (LANE_H - NODE_H) // 2 + NODE_H
y2_top2 = LANE0_Y + 2 * LANE_H + (LANE_H - NODE_H) // 2
d.arrow([(x2_c, y2_bot1), (x2_c, y2_top2)], WARN, "warn", 1.4)

# Step 2 (2,2) -> Step 3 (2,3): 수평 (폴백을 거쳐 실행)
x2_r = LABEL_W + 16 + 2 * SLOT_W + NODE_W
x3_l = LABEL_W + 16 + 3 * SLOT_W
y_lane2 = LANE0_Y + 2 * LANE_H + (LANE_H - NODE_H) // 2 + NODE_H // 2
d.arrow([(x2_r, y_lane2), (x3_l, y_lane2)], ACC, "acc", 1.4)

# Step 2 (1,2) -> (1,3): 생물학 플래그는 폴백 없이 거절
d.arrow([(x2_r, y_lane1), (x3_l, y_lane1)], BAD, "bad", 1.4)

# Step 0 (1,0) -> Step 1 (1,1): 환경 변수도 노력 수준에 들어간다
x0_r1 = LABEL_W + 16 + NODE_W
d.arrow([(x0_r1, y_lane1), (x1_l, y_lane1)], MUTED, "ar", 1.4)

# 4. 노드 정의 (lane, step): (title, sub, color, is_focal)
nodes_data = {
    # 본문 05-02:128-150 · 01-01:191 (환경 변수가 --effort 보다 우선)
    (0, 0): ("추론 입력", "--effort", INK, False),
    (0, 3): ("ultrathink", "프롬프트 내 키워드", INK, False),
    (1, 0): ("환경 변수", "CLAUDE_CODE_EFFORT_LEVEL", INK, False),

    (0, 1): ("명시값 우선순위", "환경 변수 > --effort", INK, False),
    (1, 1): ("노력 수준 결정", "low ~ max 5단계", INK, False),

    (1, 2): ("안전 분류기", "모델별 폴백 상이", WARN, False),
    (1, 3): ("생물학 → 거절", "폴백 없음", BAD, False),
    (2, 2): ("사이버 → Opus 4.8", "재실행 · switchModelsOnFlag", WARN, False),

    (2, 3): ("추론 실행", "사고 블록 · 응답", ACC, True),
}

for (k, j), (title, sub, c, is_focal) in nodes_data.items():
    nx = LABEL_W + 16 + j * SLOT_W
    ny = LANE0_Y + k * LANE_H + (LANE_H - NODE_H) // 2
    ncx = nx + NODE_W // 2

    if is_focal:
        d.tone(nx, ny, NODE_W, NODE_H, ACC, 6, "14", 1.4)
    elif c == WARN:
        d.tone(nx, ny, NODE_W, NODE_H, WARN, 6, "14", 1.2)
    elif c == BAD:
        d.tone(nx, ny, NODE_W, NODE_H, BAD, 6, "14", 1.2)
    elif c == OK:
        d.tone(nx, ny, NODE_W, NODE_H, OK, 6, "14", 1.2)
    else:
        d.box(nx, ny, NODE_W, NODE_H, PAPER2, RULE, 1.0)

    tc = ACC if is_focal else (c if c != INK else INK)
    d.t(ncx, ny + 25, title, 12.5, tc, KR, "middle", 600)
    d.t(ncx, ny + 45, sub, 11, MUTED, KR if any("가" <= ch <= "힣" for ch in sub) else MONO, "middle")

# 범례
d.legend(404, [
    ("설정 및 순위 판정", MUTED),
    ("안전 심사 및 폴백", WARN),
    ("거절 (폴백 없음)", BAD),
    ("추론 실행 (focal)", ACC),
])

d.save("05-02.thinking-controls.svg")
