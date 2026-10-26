# 사실 출처: 05-05.Interactive Features·Output Styles·Status Line·Settings.md:258-300 · 원문 chunk-05-05.md:367-390
# 타입 스펙: type-data-flow
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, INFO, KR, MONO

W, H = 960, 448
LABEL_W = 148
N_STEPS = 4
N_LANES = 3
STEP_W = (W - LABEL_W - 28) // N_STEPS  # 196
LANE_H = 76
Y_START = 104
HEADER_H = 34
Y_LANES = Y_START + HEADER_H  # 138

d = D(
    W, H,
    "STATUS LINE · DATA FLOW",
    "상태줄 JSON 파이프라인과 출력 흐름",
    "세션 이벤트 발생 시 표준 입력 JSON 전달 및 스크립트 파싱·렌더링",
    lead="세션 이벤트에 따라 JSON이 stdin으로 전달되고 jq 추출을 거쳐 한 줄로 렌더링됩니다"
)

# 1. 헤더 (단계 표시)
steps = [
    ("01", "OBJECT", False),
    ("02", "PAYLOAD", True),
    ("03", "PARSE", False),
    ("04", "RENDER", False),
]

for j, (num, lab, focal) in enumerate(steps):
    cx = LABEL_W + j * STEP_W + STEP_W // 2
    c = ACC if focal else SOFT
    d.o.append(f'<rect x="{cx - 24}" y="{Y_START + 2}" width="48" height="16" rx="8" fill="{c}22" stroke="{c}" stroke-width="1.0"/>')
    d.t(cx, Y_START + 14, num, 9, c, MONO, "middle", 600)
    d.t(cx, Y_START + 28, lab, 10, ACC if focal else MUTED, MONO, "middle", 600)

# 2. 레인 구분선 및 라벨
lanes = [
    ("모델 식별", INFO),
    ("컨텍스트", ACC),
    ("누적 비용", OK),
]

for k, (name, col) in enumerate(lanes):
    ly = Y_LANES + k * LANE_H
    if k % 2 == 1:
        d.o.append(f'<rect x="{LABEL_W}" y="{ly}" width="{W - LABEL_W - 20}" height="{LANE_H}" fill="#161B22" opacity="0.6"/>')
    d.line(16, ly, W - 20, ly, RULE, 0.8)
    d.t(LABEL_W // 2, ly + LANE_H // 2 + 4, name, 12, col, KR, "middle", 600)

d.line(16, Y_LANES + N_LANES * LANE_H, W - 20, Y_LANES + N_LANES * LANE_H, RULE, 0.8)
d.line(LABEL_W, Y_START, LABEL_W, Y_LANES + N_LANES * LANE_H, RULE, 0.8)

# 3. 노드 정의 (lane, step, title, sub, focal, col, is_mono)
NODE_W, NODE_H = 150, 48

nodes_data = [
    # Lane 0: 모델 식별 (INFO)
    (0, 0, "model", "모델 설정", False, INFO, True),
    (0, 1, ".model.id", "모델 식별자", False, INFO, True),
    (0, 2, "jq -r", "모델 ID 추출", False, INFO, True),
    (0, 3, "%s", "모델 ID 칸", False, INFO, True),

    # Lane 1: 컨텍스트 지표 (ACC - Focal)
    (1, 0, "context_window", "컨텍스트 창", False, ACC, True),
    (1, 1, ".used_percentage", "사용 비율", True, ACC, True),
    (1, 2, "jq -r", "사용률 추출", False, ACC, True),
    (1, 3, "ctx %.0f%%", "사용률 칸", False, ACC, True),

    # Lane 2: 비용 집계 (OK)
    (2, 0, "cost", "비용과 시간", False, OK, True),
    (2, 1, ".total_cost_usd", "비용 달러 값", False, OK, True),
    (2, 2, "jq -r", "비용 추출", False, OK, True),
    (2, 3, "$%.2f", "비용 칸", False, OK, True),
]

for k, j, title, sub, focal, col, is_mono in nodes_data:
    cx = LABEL_W + j * STEP_W + STEP_W // 2
    x = cx - NODE_W // 2
    y = Y_LANES + k * LANE_H + (LANE_H - NODE_H) // 2

    title_fam = MONO if is_mono else KR

    if focal:
        d.tone(x, y, NODE_W, NODE_H, ACC, r=6, op="18", sw=1.4)
        d.t(cx, y + 20, title, 12, ACC, title_fam, "middle", 600)
        d.t(cx, y + 36, sub, 11, INK, KR, "middle")
    else:
        d.box(x, y, NODE_W, NODE_H, fill=PAPER2, stroke=RULE, sw=0.9, r=6)
        d.t(cx, y + 20, title, 12, INK, title_fam, "middle", 600)
        d.t(cx, y + 36, sub, 11, MUTED, KR, "middle")

# 4. 화살표 (레인 내부 수평 연결)
for k, col, mk in [(0, INFO, "info"), (1, ACC, "acc"), (2, OK, "ok")]:
    for j in range(N_STEPS - 1):
        cx1 = LABEL_W + j * STEP_W + STEP_W // 2
        cx2 = LABEL_W + (j + 1) * STEP_W + STEP_W // 2
        x1 = cx1 + NODE_W // 2 + 3
        x2 = cx2 - NODE_W // 2 - 4
        y = Y_LANES + k * LANE_H + LANE_H // 2
        d.arrow([(x1, y), (x2, y)], col, mk, 1.2)

d.legend(396, [
    ("컨텍스트 지표 (Focal)", ACC),
    ("모델 식별 지표", INFO),
    ("비용 집계 지표", OK),
    ("파이프라인 단계", SOFT),
])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "05-05.statusline-json.svg"))
d.save(out)
print(f"saved: {out}")
