"""플러그인 로딩 및 컴포넌트 추출 등록 절차 파이프라인."""
# 타입 스펙: type-process
# 사실 출처: 04-02.Plugins.md:100-104, 201-204 · 원문 07-plugins/README.md:34-60
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, INFO, KR, MONO

W, H = 976, 400
d = D(
    W, H,
    "PLUGIN LOADING · COMPONENT EXTRACTION",
    "플러그인 로딩 및 컴포넌트 추출 등록 절차",
    "패키지 탐색부터 매니페스트 읽기, 컴포넌트 추출, 세션 도구 편입까지의 대략적인 등록 흐름 (순서는 본문 확인 필요)",
    lead="플러그인이 로드될 때 매니페스트(있으면)를 읽고 각 서브 디렉터리의 컴포넌트를 추출해 세션에 등록합니다",
)

LABEL_W = 144
SLOT_W = 156
NODE_W = 136
NODE_H = 64
LANE_H = 88
HEADER_Y = 96
LANE0_Y = 128

# 1. 레인 배경 및 구분선
for k in range(2):
    y = LANE0_Y + k * LANE_H
    if k % 2 == 0:
        d.o.append(f'<rect x="{LABEL_W}" y="{y}" width="{W - LABEL_W - 12}" height="{LANE_H}" fill="rgba(245,245,243,0.02)"/>')
    d.line(16, y, W - 12, y, RULE, 0.8)

d.line(16, LANE0_Y + 2 * LANE_H, W - 12, LANE0_Y + 2 * LANE_H, RULE, 0.8)
d.line(LABEL_W, LANE0_Y, LABEL_W, LANE0_Y + 2 * LANE_H, RULE, 1.0)

# 레인 이름
lanes = [
    ("런타임", "로더 작업"),
    ("페이로드", "흐르는 값"),
]
for k, (title, sub) in enumerate(lanes):
    cy = LANE0_Y + k * LANE_H + LANE_H // 2
    d.t(24, cy - 6, title, 13, INK, KR, "start", 600)
    d.t(24, cy + 14, sub, 11.5, MUTED, KR, "start")

# 2. 단계 머리 (Step Header)
steps = [
    ("1 · 탐색", False, False),
    ("2 · 읽기", False, False),
    ("3 · 추출", True, False),
    ("4 · 편입", False, True),
]

for j, (st_name, is_focal, is_ok) in enumerate(steps):
    cx = LABEL_W + 16 + j * SLOT_W + NODE_W // 2
    c = ACC if is_focal else (OK if is_ok else INK)
    d.t(cx, HEADER_Y + 18, st_name, 12, c, KR, "middle", 600)

# 3. 페이로드 흐름 화살표 (노드보다 먼저 그린다)
for j in range(3):
    x_from = LABEL_W + 16 + j * SLOT_W + NODE_W
    x_to = LABEL_W + 16 + (j + 1) * SLOT_W
    y_mid = LANE0_Y + 1 * LANE_H + (LANE_H - NODE_H) // 2 + NODE_H // 2
    if j == 1:
        d.arrow([(x_from, y_mid), (x_to, y_mid)], ACC, "acc", 1.4, "5 4")
    elif j == 2:
        d.arrow([(x_from, y_mid), (x_to, y_mid)], OK, "ok", 1.4, "5 4")
    else:
        d.arrow([(x_from, y_mid), (x_to, y_mid)], MUTED, "ar", 1.4)

# 4. 그리드 노드 (3행 x 5열)
nodes_data = {
    # (lane, step): (title, sub, color, is_focal, is_mono_sub)  — 본문 04-02:92-94, 150-157, 200
    (0, 0): ("경로 지정", "--plugin-dir", INK, False, True),
    (1, 0): ("my-plugin/", "패키지 경로", INFO, False, False),

    (0, 1): ("매니페스트(있으면) 읽기", "plugin.json", INK, False, True),
    (1, 1): ("메타데이터", "name · version", INFO, False, True),

    (0, 2): ("컴포넌트 추출", "skills · agents", ACC, True, True),
    (1, 2): ("설정 추출", "hooks · mcp", ACC, True, True),

    (0, 3): ("세션 편입", "도구 등록", INK, False, False),
    (1, 3): ("/pr-review:check", "세션 도구", OK, False, False),
}

for (k, j), (title, sub, c, is_focal, is_mono_sub) in nodes_data.items():
    nx = LABEL_W + 16 + j * SLOT_W
    ny = LANE0_Y + k * LANE_H + (LANE_H - NODE_H) // 2
    if is_focal:
        d.tone(nx, ny, NODE_W, NODE_H, ACC, r=6, op="14", sw=1.4)
    elif c == OK:
        d.box(nx, ny, NODE_W, NODE_H, fill=PAPER2, stroke=OK, sw=1.0, r=6)
    elif c == INFO:
        d.box(nx, ny, NODE_W, NODE_H, fill=PAPER2, stroke=INFO, sw=0.9, r=6)
    else:
        d.box(nx, ny, NODE_W, NODE_H, fill=PAPER2, stroke=RULE, sw=0.9, r=6)

    cx = nx + NODE_W // 2
    d.t(cx, ny + 26, title, 12, INK if not is_focal else ACC, MONO if "/" in title else KR, "middle", 600)
    fam = MONO if is_mono_sub else KR
    d.t(cx, ny + 46, sub, 11, c if (is_focal or c in (OK, INFO)) else MUTED, fam, "middle")

# 5. 범례
d.legend(336, [
    ("컴포넌트 추출 (Focal)", ACC),
    ("데이터 페이로드", INFO),
    ("편입 완료", OK),
    ("점선: 대략의 순서", MUTED),
])

d.save("04-02.plugin-loading.svg")
