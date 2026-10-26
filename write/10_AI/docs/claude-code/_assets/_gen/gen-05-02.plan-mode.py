"""계획 모드의 쓰기 차단과 승인 후 구현 전환 흐름.

# 타입 스펙: type-swimlane
"""
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 448
d = D(
    W, H,
    "PLANNING MODE WORKFLOW",
    "계획 수립 단계의 쓰기 차단과 승인 후 구현 전환",
    "사용자 지시부터 읽기 전용 탐색, 계획서 검토, 승인 후 구현 전환까지의 흐름",
    lead="모든 파일 쓰기를 잠근 상태로 계획을 검토하고, 사용자 승인 후에만 구현 단계로 전환합니다"
)

LABEL_W = 140
LANE_TOP = 104
LANE0_H = 112
LANE1_H = 128
LANE0_BOT = LANE_TOP + LANE0_H        # 216
LANE1_BOT = LANE0_BOT + LANE1_H        # 344

# 레인 배경 및 구분선
d.box(LABEL_W, LANE_TOP, W - LABEL_W - 20, LANE0_H, fill="rgba(245,245,243,0.02)", stroke=RULE, sw=0.8, r=0)
d.box(LABEL_W, LANE0_BOT, W - LABEL_W - 20, LANE1_H, fill=PAPER, stroke=RULE, sw=0.8, r=0)
d.line(20, LANE_TOP, W - 20, LANE_TOP, RULE, 0.8)
d.line(20, LANE0_BOT, W - 20, LANE0_BOT, RULE, 0.8)
d.line(20, LANE1_BOT, W - 20, LANE1_BOT, RULE, 0.8)
d.line(LABEL_W, LANE_TOP, LABEL_W, LANE1_BOT, RULE, 1.0)

# 레인 라벨
d.t(80, LANE_TOP + 44, "USER", 9, SOFT, MONO, "middle", 600)
d.t(80, LANE_TOP + 68, "사용자", 14, INK, KR, "middle", 600)

d.t(80, LANE0_BOT + 52, "CLAUDE", 9, SOFT, MONO, "middle", 600)
d.t(80, LANE0_BOT + 76, "Claude Code", 14, INK, KR, "middle", 600)

def step_box(x, y, w, h, title, sub, focal=False):
    if focal:
        d.tone(x, y, w, h, ACC, r=6, op="14", sw=1.4)
    else:
        d.box(x, y, w, h, fill=PAPER2, stroke=RULE, sw=1.0, r=6)
    tc = ACC if focal else INK
    sc = ACC if focal else MUTED
    d.t(x + w / 2, y + 26, title, 13, tc, KR, "middle", 600)
    d.t(x + w / 2, y + 46, sub, 12, sc, KR, "middle")

# 노드 좌표 (모두 4의 배수)
# User 레인 노드: Y = 128, H = 64
# Claude 레인 노드: Y = 248, H = 64
step_box(156, 128, 132, 64, "계획 모드 진입", "/plan · plan 모드")
step_box(304, 248, 140, 64, "코드베이스 탐색", "읽기 전용 · 쓰기 차단")
step_box(464, 248, 140, 64, "구현 계획서 수립", "작업 순서 · 변경 목록")
step_box(624, 128, 132, 64, "계획 검토 및 판정", "승인 또는 계획 유지")
step_box(756, 248, 132, 64, "구현 전환", "편집 승인 방식 선택", focal=True)

# 화살표 1: N1 (User) -> N2 (Claude 탐색)
# N1 우측 (288, 160) -> H to 374 -> V to 248
d.path("M 288 160 H 366 Q 374 160 374 168 V 248", MUTED, 1.4, m="ar")

# 화살표 2: N2 (탐색) -> N3 (계획서 생성)
d.arrow([(444, 280), (464, 280)], MUTED, "ar", 1.4)

# 화살표 3: N3 (계획서 생성) -> N4 (User 검토)
# N3 우측 (604, 280) -> H to 690 -> V to 192 (N4 밑면)
d.path("M 604 280 H 682 Q 690 280 690 272 V 192", MUTED, 1.4, m="ar")

# 화살표 4 (focal): N4 (User 승인) -> N5 (Claude 구현 전환)
# N4 우측 (756, 160) -> H to 842 -> V to 248 (N5 윗면)
d.path("M 756 160 H 814 Q 822 160 822 168 V 248", ACC, 1.6, m="acc")
d.t(806, 150, "승인 (Yes …)", 11, ACC, KR, "middle", 600)

# 화살표 5: N4 (User 수정 요구) -> N3 (계획서 갱신) 되먹임 루프
# N4 좌측 (624, 168) -> H to 534 -> V to 248 (N3 윗면)
d.path("M 624 168 H 542 Q 534 168 534 176 V 248", SOFT, 1.2, m="soft", dash="4 3")
d.t(526, 204, "No, keep planning", 11, SOFT, KR, "end")

# 범례
d.legend(388, [
    ("계획 수립 및 읽기 전용 탐색", MUTED),
    ("구현 전환 및 코드 수정 (focal)", ACC),
    ("계획 유지 피드백 루프", SOFT),
])

d.save("05-02.plan-mode.svg")
