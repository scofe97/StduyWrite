"""저작물·생성물 분리와 pre-commit 검증 흐름 파이프라인."""
# 타입 스펙: type-process
# 사실 출처: C2 45-70행 · dalcom-skills .pre-commit-config.yaml:40-100 · scripts/plugin-surfaces.mjs:7-13
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, BAD, INFO, KR, MONO

W, H = 976, 480
d = D(
    W, H,
    "PIPELINE · PROCESS",
    "저작물·생성물 분리와 pre-commit 검증 흐름",
    "저작물 편집부터 렌더 스크립트 실행, 생성물 도출, pre-commit --check 의 불일치 검증과 차단 흐름",
    lead="사람이 쓰는 저작물에서 스크립트가 생성물을 도출하고, pre-commit --check 가 변경 불일치를 감지해 커밋을 차단합니다",
)

LABEL_W = 136
NODE_W = 150
NODE_H = 64
LANE_H = 88
HEADER_Y = 96
LANE0_Y = 128

# 1. 레인 배경 및 구분선
for k in range(3):
    y = LANE0_Y + k * LANE_H
    if k % 2 == 0:
        d.o.append(f'<rect x="{LABEL_W}" y="{y}" width="{W - LABEL_W - 12}" height="{LANE_H}" fill="rgba(245,245,243,0.02)"/>')
    d.line(16, y, W - 12, y, RULE, 0.8)

d.line(16, LANE0_Y + 3 * LANE_H, W - 12, LANE0_Y + 3 * LANE_H, RULE, 0.8)
d.line(LABEL_W, LANE0_Y, LABEL_W, LANE0_Y + 3 * LANE_H, RULE, 1.0)

# 레인 이름
lanes = [
    ("저작자", "수동 편집"),
    ("스크립트", "파생 생성"),
    ("pre-commit", "게이트 검증"),
]
for k, (title, sub) in enumerate(lanes):
    cy = LANE0_Y + k * LANE_H + LANE_H // 2
    d.t(24, cy - 6, title, 13, INK, KR, "start", 600)
    d.t(24, cy + 14, sub, 11, MUTED, KR, "start")

# 단계별 X 좌표 (1~4단계 간격 158px, 4~5단계는 판정 분기 라벨 공간을 위해 192px)
step_x = [148, 306, 464, 622, 814]

# 2. 단계 머리 (Step Header)
steps = [
    ("1 · 저작", False, False),
    ("2 · 렌더", False, False),
    ("3 · 커밋", False, False),
    ("4 · 검증", True, False),
    ("5 · 판정", False, False),
]

for j, (st_name, is_focal, is_ok) in enumerate(steps):
    cx = step_x[j] + NODE_W // 2
    c = ACC if is_focal else (OK if is_ok else INK)
    d.t(cx, HEADER_Y + 18, st_name, 12, c, KR, "middle", 600)

# 3. 흐름 화살표 (노드보다 먼저 그린다)
y_mid0 = LANE0_Y + 0 * LANE_H + (LANE_H - NODE_H) // 2 + NODE_H // 2  # 172
y_mid1 = LANE0_Y + 1 * LANE_H + (LANE_H - NODE_H) // 2 + NODE_H // 2  # 260
y_mid2 = LANE0_Y + 2 * LANE_H + (LANE_H - NODE_H) // 2 + NODE_H // 2  # 348

# Step 0 -> Step 1 (저작자: 저작물 -> 스크립트: render)
x_f0 = step_x[0] + NODE_W
x_t1 = step_x[1]
x_mid01 = x_f0 + (x_t1 - x_f0) // 2
d.arrow([(x_f0, y_mid0), (x_mid01, y_mid0), (x_mid01, y_mid1), (x_t1, y_mid1)], MUTED, "ar", 1.4)

# Step 1 -> Step 2 (스크립트: render -> 저작자: 커밋 시도)
x_f1 = step_x[1] + NODE_W
x_t2 = step_x[2]
x_mid12 = x_f1 + (x_t2 - x_f1) // 2
d.arrow([(x_f1, y_mid1), (x_mid12, y_mid1), (x_mid12, y_mid0), (x_t2, y_mid0)], OK, "ok", 1.4)

# Step 2 -> Step 3 (저작자: 커밋 시도 -> pre-commit: --check focal in)
x_f2 = step_x[2] + NODE_W
x_t3 = step_x[3]
x_mid23 = x_f2 + (x_t3 - x_f2) // 2
d.arrow([(x_f2, y_mid0), (x_mid23, y_mid0), (x_mid23, y_mid2), (x_t3, y_mid2)], ACC, "acc", 1.4)

# Step 3 -> Step 4 (판정 분기: focal out)
x_f3 = step_x[3] + NODE_W
x_t4 = step_x[4]
x_mid34 = x_f3 + (x_t4 - x_f3) // 2

# Pass branch (exit 0): Lane 2 Step 3 -> Lane 0 Step 4
d.arrow([(x_f3, y_mid2), (x_mid34, y_mid2), (x_mid34, y_mid0), (x_t4, y_mid0)], OK, "ok", 1.4)
d.t(x_mid34 + 8, 260, "일치", 11, OK, KR, "start", 600)

# Block branch (exit 1): Lane 2 Step 3 -> Lane 2 Step 4
d.arrow([(x_f3, y_mid2), (x_t4, y_mid2)], BAD, "bad", 1.4)
d.t(x_mid34, y_mid2 + 18, "불일치", 11, BAD, KR, "middle", 600)

# 4. 그리드 노드
nodes_data = {
    # Step 0: 저작자, 1
    (0, 0): ("저작물", "SKILL.md · plugins.json", INFO, False, True),

    # Step 1: 스크립트, 2
    (1, 1): ("render-*.mjs", "openai.yaml · 색인 · 표", OK, False, False),

    # Step 2: 저작자, 3
    (0, 2): ("커밋 시도", "git commit", INK, False, True),

    # Step 3: pre-commit, 4
    (2, 3): ("--check × 3", "재계산 대 디스크", ACC, True, False),

    # Step 4: 저작자, 5 / pre-commit, 5
    (0, 4): ("커밋 통과", "exit 0", OK, False, True),
    (2, 4): ("커밋 차단", "exit 1", BAD, False, True),
}

for (k, j), (title, sub, c, is_focal, is_mono_sub) in nodes_data.items():
    nx = step_x[j]
    ny = LANE0_Y + k * LANE_H + (LANE_H - NODE_H) // 2
    ncx = nx + NODE_W // 2

    if is_focal:
        d.tone(nx, ny, NODE_W, NODE_H, ACC, 6, "14", 1.4)
    elif c == OK:
        d.tone(nx, ny, NODE_W, NODE_H, OK, 6, "14", 1.2)
    elif c == BAD:
        d.tone(nx, ny, NODE_W, NODE_H, BAD, 6, "14", 1.2)
    elif c == INFO:
        d.tone(nx, ny, NODE_W, NODE_H, INFO, 6, "14", 1.0)
    else:
        d.box(nx, ny, NODE_W, NODE_H, PAPER2, RULE, 1.0)

    # 텍스트
    fam_title = MONO if "/" in title or "SKILL" in title or "exit" in title or "render" in title or "--check" in title else KR
    fam_sub = MONO if is_mono_sub or "/" in sub or ":" in sub or "render" in sub or "exit" in sub else KR
    fsize_sub = 11 if any('가' <= ch <= '힣' for ch in sub) else 10.0
    d.t(ncx, ny + 26, title, 12, c, fam_title, "middle", 600)
    d.t(ncx, ny + 47, sub, fsize_sub, MUTED, fam_sub, "middle")

# 5. 범례
d.legend(426, [
    ("저작물 (수동 편집)", INFO),
    ("생성물 및 통과 (exit 0)", OK),
    ("사전 커밋 게이트 (검증)", ACC),
    ("불일치 차단 (exit 1)", BAD),
])

d.save("01-01.generated-pipeline.svg")
