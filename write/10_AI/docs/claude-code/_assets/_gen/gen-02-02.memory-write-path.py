# 사실 출처: 02-02.Memory.md:116-133 · 원문 README.md:477-492
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
    "MEMORY WRITE PATH · DATA FLOW",
    "대화 지시와 /memory 명령의 메모리 반영 경로",
    "자연어 지시 유형과 슬래시 명령에 따른 파일 저장소 및 세션 적재 흐름",
    lead="지시 방식에 따라 자동 메모리와 프로젝트 파일로 분기되어 반영됩니다"
)

# 1. 헤더 (단계 표시)
steps = [
    ("01", "INPUT", False),
    ("02", "ROUTE", False),
    ("03", "WRITE", True),
    ("04", "LOAD", False),
]

for j, (num, lab, focal) in enumerate(steps):
    cx = LABEL_W + j * STEP_W + STEP_W // 2
    c = ACC if focal else SOFT
    d.o.append(f'<rect x="{cx - 20}" y="{Y_START + 2}" width="40" height="16" rx="8" fill="{c}22" stroke="{c}" stroke-width="1.0"/>')
    d.t(cx, Y_START + 14, num, 9, c, MONO, "middle", 600)
    d.t(cx, Y_START + 28, lab, 10, ACC if focal else MUTED, MONO, "middle", 600)

# 2. 레인 구분선 및 라벨
lanes = [
    ("자연어 피드백", INFO),
    ("자연어 파일 지정", ACC),
    ("/memory 명령", OK),
]

for k, (name, col) in enumerate(lanes):
    ly = Y_LANES + k * LANE_H
    if k % 2 == 1:
        d.o.append(f'<rect x="{LABEL_W}" y="{ly}" width="{W - LABEL_W - 20}" height="{LANE_H}" fill="#161B22" opacity="0.6"/>')
    d.line(16, ly, W - 20, ly, RULE, 0.8)
    d.t(LABEL_W // 2, ly + LANE_H // 2 + 4, name, 12, col, KR, "middle", 600)

d.line(16, Y_LANES + N_LANES * LANE_H, W - 20, Y_LANES + N_LANES * LANE_H, RULE, 0.8)
d.line(LABEL_W, Y_START, LABEL_W, Y_LANES + N_LANES * LANE_H, RULE, 0.8)

# 3. 노드 정의 (lane, step, title, sub, focal)
NODE_W, NODE_H = 144, 48

nodes_data = [
    # Lane 0: 피드백 지시
    (0, 0, "선호·피드백 발화", "async/await 기억", False, INFO),
    (0, 1, "자동 메모리 분류", "피드백 항목 판정", False, INFO),
    (0, 2, "MEMORY.md 기록", "프로젝트 캐시 폴더", False, INFO),
    (0, 3, "세션 시작 시 로드", "MEMORY.md 앞부분", False, INFO),

    # Lane 1: 명시적 파일 지시 (Focal)
    (1, 0, "파일명 명시 발화", "CLAUDE.md 추가", False, ACC),
    (1, 1, "프로젝트 메모리", "대상 파일 식별", False, ACC),
    (1, 2, "./CLAUDE.md 기록", "팀 공유 규칙 추가", True, ACC),
    (1, 3, "세션 시작 시 로드", "CLAUDE.md 적재", False, ACC),

    # Lane 2: /memory 명령
    (2, 0, "/memory 명령", "터미널 CLI 실행", False, OK),
    (2, 1, "메모리 파일 메뉴", "정책·프로젝트·사용자·로컬", False, OK),
    (2, 2, "에디터 직접 편집", "GUI·CLI 편집기", False, OK),
    (2, 3, "저장 후 반영", "세션 반영", False, OK),
]

for k, j, title, sub, focal, col in nodes_data:
    cx = LABEL_W + j * STEP_W + STEP_W // 2
    x = cx - NODE_W // 2
    y = Y_LANES + k * LANE_H + (LANE_H - NODE_H) // 2

    if focal:
        d.tone(x, y, NODE_W, NODE_H, ACC, r=6, op="18", sw=1.4)
        d.t(cx, y + 20, title, 12, ACC, KR, "middle", 600)
        d.t(cx, y + 36, sub, 11, INK, KR, "middle")
    else:
        d.box(x, y, NODE_W, NODE_H, fill=PAPER2, stroke=RULE, sw=0.9, r=6)
        d.t(cx, y + 20, title, 12, INK, KR, "middle", 600)
        d.t(cx, y + 36, sub, 11, MUTED, KR, "middle")

# 4. 화살표 (레인 내부 수평 연결)
for k, col, mk in [(0, INFO, "info"), (1, ACC, "acc"), (2, OK, "ok")]:
    for j in range(N_STEPS - 1):
        cx1 = LABEL_W + j * STEP_W + STEP_W // 2
        cx2 = LABEL_W + (j + 1) * STEP_W + STEP_W // 2
        x1 = cx1 + NODE_W // 2
        x2 = cx2 - NODE_W // 2
        y = Y_LANES + k * LANE_H + LANE_H // 2
        d.arrow([(x1, y), (x2, y)], col, mk, sw=1.3)

# 5. 범례
d.legend(392, [
    ("선호·피드백 자동 기록", INFO),
    ("프로젝트 메모리 기록 (Focal)", ACC),
    ("에디터 직접 편집 경로", OK),
])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "02-02.memory-write-path.svg"))
d.save(out)
print(f"saved: {out}")
