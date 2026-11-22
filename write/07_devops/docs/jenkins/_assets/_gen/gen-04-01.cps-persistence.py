# 타입 스펙: type-data-flow
# 2절 CPS 변환과 실행 상태 저장 — 실행 중 상태가 디스크에 쓰이고 재기동 뒤 복구되는 흐름
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, PAPER, PAPER2, KR, MONO

W, H = 960, 464

d = D(
    W, H,
    "JENKINS · PIPELINE DURABILITY",
    "CPS 변환과 실행 상태 저장 흐름",
    "실행 중인 continuation 객체와 라이브 자원이 program.dat와 workflow/로 영속화되고 재기동 후 rehydrate로 복구되는 데이터 흐름",
    lead="힙의 continuation 객체와 라이브 자원 보관증(pickle)이 디스크에 쓰이고 재기동 뒤 복원됩니다"
)

# ── 3단계 컬럼 (단계 헤더) ────────────────────────────────────────────────
LABEL_W = 152
COL_W = 228
COL_GAP = 28
X0 = 24
X_STEPS = X0 + LABEL_W + 8  # 184

STEPS = [
    ("01 실행 중", "힙 메모리", INFO, False),
    ("02 디스크 저장", "builds/{number}/", ACC, True),
    ("03 재기동 후 재개", "새 JVM", OK, False),
]

HEADER_Y = 96
HEADER_H = 40

for j, (title, sub, col, focal) in enumerate(STEPS):
    cx = X_STEPS + j * (COL_W + COL_GAP)
    if focal:
        d.tone(cx, HEADER_Y, COL_W, HEADER_H, ACC, r=6, op="18", sw=1.4)
        d.t(cx + COL_W // 2, HEADER_Y + 16, title, 12, ACC, KR, "middle", 600)
        d.t(cx + COL_W // 2, HEADER_Y + 32, sub, 11, INK, MONO if "{" in sub else KR, "middle")
    else:
        d.box(cx, HEADER_Y, COL_W, HEADER_H, PAPER2, RULE, 1.0)
        d.t(cx + COL_W // 2, HEADER_Y + 16, title, 12, col, KR, "middle", 600)
        d.t(cx + COL_W // 2, HEADER_Y + 32, sub, 11, MUTED, KR, "middle")

# ── 3개 레인 배경 및 라벨 ────────────────────────────────────────────────
LANE_H = 80
LANE_Y0 = 148

LANES = [
    ("프로그램 상태", "CONTINUATION", INK),
    ("라이브 자원", "LIVE RESOURCES", WARN),
    ("실행 기록", "FLOW NODE", INFO),
]

for k, (name, key, col) in enumerate(LANES):
    ly = LANE_Y0 + k * LANE_H
    bg = PAPER2 if k % 2 == 1 else PAPER
    d.o.append(f'<rect x="{X0}" y="{ly}" width="{W - X0 * 2}" height="{LANE_H}" rx="6" fill="{bg}" stroke="{RULE}" stroke-width="0.8"/>')
    d.t(X0 + LABEL_W // 2, ly + 32, name, 13, col, KR, "middle", 600)
    d.t(X0 + LABEL_W // 2, ly + 50, key, 11, MUTED, MONO, "middle")
    d.line(X0 + LABEL_W, ly, X0 + LABEL_W, ly + LANE_H, RULE, 0.8)

# ── 노드 데이터 ──────────────────────────────────────────────────────────
CARD_W = 216
CARD_H = 56
CARD_OFF_Y = 12

NODES = [
    # Lane 0: 프로그램 상태
    (0, 0, "continuation 객체 그래프", "CPS VM thread 해석", INFO, False),
    (0, 1, "program.dat", "미래 상태 직렬화", ACC, True),
    (0, 2, "StepExecution.onResume", "중단 지점 재개", OK, False),

    # Lane 1: 라이브 자원
    (1, 0, "라이브 자원", "Executor · 워크스페이스", WARN, False),
    (1, 1, "pickle 보관증 치환", "Pickle API 치환", WARN, False),
    (1, 2, "병렬 rehydrate", "실물 자원 복원", OK, False),

    # Lane 2: 실행 기록
    (2, 0, "실행 step 계층", "순차 명령문 실행", INFO, False),
    (2, 1, "workflow/ 디렉터리", "FlowNode XML 기록", INFO, False),
    (2, 2, "과거 기록 보존", "Blue Ocean · API 조회", INFO, False),
]

for k, j, title, sub, col, focal in NODES:
    nx = X_STEPS + j * (COL_W + COL_GAP) + (COL_W - CARD_W) // 2
    ny = LANE_Y0 + k * LANE_H + CARD_OFF_Y
    if focal:
        d.tone(nx, ny, CARD_W, CARD_H, ACC, r=6, op="18", sw=1.4)
        d.t(nx + CARD_W // 2, ny + 22, title, 13, ACC, MONO if "." in title else KR, "middle", 600)
        d.t(nx + CARD_W // 2, ny + 42, sub, 11, INK, KR, "middle")
    elif col == OK:
        d.tone(nx, ny, CARD_W, CARD_H, OK, r=6, op="12", sw=1.2)
        d.t(nx + CARD_W // 2, ny + 22, title, 13, OK, MONO if "." in title else KR, "middle", 600)
        d.t(nx + CARD_W // 2, ny + 42, sub, 11, MUTED, KR, "middle")
    elif col == WARN:
        d.tone(nx, ny, CARD_W, CARD_H, WARN, r=6, op="12", sw=1.2)
        d.t(nx + CARD_W // 2, ny + 22, title, 13, WARN, KR, "middle", 600)
        d.t(nx + CARD_W // 2, ny + 42, sub, 11, MUTED, KR, "middle")
    else:
        d.box(nx, ny, CARD_W, CARD_H, PAPER, col if col == INFO else RULE, 1.0)
        d.t(nx + CARD_W // 2, ny + 22, title, 13, INK, MONO if "/" in title else KR, "middle", 600)
        d.t(nx + CARD_W // 2, ny + 42, sub, 11, MUTED, KR, "middle")

# ── 화살표 (수평 및 수직 연결) ─────────────────────────────────────────
for k in range(3):
    cy = LANE_Y0 + k * LANE_H + CARD_OFF_Y + CARD_H // 2
    nx0 = X_STEPS + 0 * (COL_W + COL_GAP) + (COL_W - CARD_W) // 2
    nx1 = X_STEPS + 1 * (COL_W + COL_GAP) + (COL_W - CARD_W) // 2
    nx2 = X_STEPS + 2 * (COL_W + COL_GAP) + (COL_W - CARD_W) // 2

    c01 = ACC if k == 0 else (WARN if k == 1 else INFO)
    m01 = "acc" if k == 0 else ("warn" if k == 1 else "info")
    d.arrow([(nx0 + CARD_W + 2, cy), (nx1 - 4, cy)], c01, m01, 1.4)

    c12 = ACC if k == 0 else (WARN if k == 1 else INFO)
    m12 = "acc" if k == 0 else ("warn" if k == 1 else "info")
    d.arrow([(nx1 + CARD_W + 2, cy), (nx2 - 4, cy)], c12, m12, 1.4)

# 수직 화살표 1: Step 1 에서 pickle 보관증 -> program.dat (보관증 포함 기록)
nx1 = X_STEPS + 1 * (COL_W + COL_GAP) + (COL_W - CARD_W) // 2
vx1 = nx1 + CARD_W // 2
y_lane1_top = LANE_Y0 + 1 * LANE_H + CARD_OFF_Y
y_lane0_bot = LANE_Y0 + 0 * LANE_H + CARD_OFF_Y + CARD_H
d.arrow([(vx1, y_lane1_top - 2), (vx1, y_lane0_bot + 4)], WARN, "warn", 1.4)

# 수직 화살표 2: Step 2 에서 병렬 rehydrate -> StepExecution.onResume (자원 복원 성공 시 재개)
nx2 = X_STEPS + 2 * (COL_W + COL_GAP) + (COL_W - CARD_W) // 2
vx2 = nx2 + CARD_W // 2
y_lane1_top_s2 = LANE_Y0 + 1 * LANE_H + CARD_OFF_Y
y_lane0_bot_s2 = LANE_Y0 + 0 * LANE_H + CARD_OFF_Y + CARD_H
d.arrow([(vx2, y_lane1_top_s2 - 2), (vx2, y_lane0_bot_s2 + 4)], OK, "ok", 1.4)

# ── 범례 ────────────────────────────────────────────────────────────────
LEG_Y = 404
d.legend(LEG_Y, [
    ("프로그램 영속화", ACC),
    ("라이브 자원 치환", WARN),
    ("실물 복원 및 재개", OK),
    ("실행 기록", INFO),
])

out_path = sys.argv[1] if len(sys.argv) > 1 else str(pathlib.Path(__file__).resolve().parent.parent / "04-01.cps-persistence.svg")
d.save(out_path)
print("ok gen-04-01.cps-persistence")
