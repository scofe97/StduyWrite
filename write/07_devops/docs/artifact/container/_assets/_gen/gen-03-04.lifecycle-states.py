# 타입 스펙: type-state
# 03-04.lifecycle-states — OCI runtime-spec v1.3.0 의 컨테이너 4상태, 5연산, 6훅 지점
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 960, 456

d = D(
    W,
    H,
    "DEVOPS · CONTAINER · 03-04",
    "컨테이너 생애 주기와 상태 전이",
    "OCI runtime-spec v1.3.0 의 네 상태, 다섯 기본 연산, 여섯 훅 실행 지점",
    lead="creating → created → running → stopped 전이와 create·start·delete 지점의 훅 순서",
)

# 상태 박스 규격 (모든 좌표 4의 배수)
BW, BH = 136, 64
SY = 204
SX = [92, 324, 556, 788]  # 간격 96px (cx: 160, 392, 624, 856)
SCX = [x + BW // 2 for x in SX]
CY = SY + BH // 2  # 236

# ── 전이 화살표 (노드보다 먼저 그린다) ──
# 시작 점 -> creating
d.o.append(f'<circle cx="24" cy="{CY}" r="6" fill="{INK}"/>')
d.arrow([(30, CY), (SX[0] - 2, CY)], INFO, "info", 1.4)
d.t(58, CY - 10, "create", 12, INFO, MONO, "middle", 600)

# creating -> created
d.arrow([(SX[0] + BW, CY), (SX[1] - 2, CY)], WARN, "warn", 1.4)
d.t(276, CY - 10, "환경 완료", 13, WARN, KR, "middle", 600)

# created -> running
d.arrow([(SX[1] + BW, CY), (SX[2] - 2, CY)], OK, "ok", 1.5)
d.t(508, CY - 10, "start", 12, OK, MONO, "middle", 600)

# running -> stopped (프로세스 종료 또는 kill)
d.arrow([(SX[2] + BW, CY), (SX[3] - 2, CY)], BAD, "bad", 1.4)
d.t(740, CY - 10, "kill · 종료", 13, BAD, KR, "middle", 600)

# created -> stopped (start 전 kill 또는 프로세스 종료 — 왼쪽으로 분리)
BY_Y = 296
BY_END_X = SX[3] + 28  # 816
d.arrow([(SCX[1], SY + BH), (SCX[1], BY_Y), (BY_END_X, BY_Y), (BY_END_X, SY + BH + 2)], BAD, "bad", 1.3, "5 4")
d.t((SCX[1] + BY_END_X) // 2, BY_Y + 20, "start 전 kill · 종료", 13, BAD, KR, "middle")

# stopped -> 종료 점 (delete + poststop — 오른쪽 선 x=884, 라벨은 y=324 이후 배치해 y=296 선과 분리)
DEL_X = SCX[3] + 28  # 884
END_Y = 368
d.arrow([(DEL_X, SY + BH), (DEL_X, END_Y - 12)], MUTED, "ar", 1.4)
d.t(DEL_X - 10, 328, "delete", 12, INK, MONO, "end", 600)
d.t(DEL_X - 10, 348, "poststop 훅", 13, MUTED, KR, "end")
# 종료 고리 점
d.o.append(f'<circle cx="{DEL_X}" cy="{END_Y}" r="8" fill="none" stroke="{MUTED}" stroke-width="1.5"/>')
d.o.append(f'<circle cx="{DEL_X}" cy="{END_Y}" r="4.5" fill="{INK}"/>')

# 훅 상단 주석 박스 연결선 (점선)
GAP1_CX = (SX[0] + BW + SX[1]) // 2  # 276
GAP2_CX = (SX[1] + BW + SX[2]) // 2  # 508
d.line(GAP1_CX, 180, GAP1_CX, CY - 24, INFO, 1.2, "4 3")
d.line(GAP2_CX, 180, GAP2_CX, CY - 24, OK, 1.2, "4 3")

# ── 상단 훅 배지 ──
# 1) create 훅 (Gap 1 위)
d.box(176, 96, 200, 84, PAPER2, INFO, 1.0, 6)
d.t(276, 114, "create 시점 훅", 13, INFO, KR, "middle", 600)
d.t(276, 134, "prestart (폐기)", 13, BAD, MONO, "middle")
d.t(276, 152, "createRuntime", 12, INK, MONO, "middle")
d.t(276, 170, "createContainer", 12, INK, MONO, "middle")

# 2) start 훅 (Gap 2 위)
d.box(416, 96, 184, 84, PAPER2, OK, 1.0, 6)
d.t(508, 114, "start 시점 훅", 13, OK, KR, "middle", 600)
d.t(508, 140, "startContainer (전)", 13, INK, MONO, "middle")
d.t(508, 162, "poststart (후)", 13, INK, MONO, "middle")

# ── 상태 노드 4개 ──
STATES = [
    (0, "creating", "환경 생성 중", INFO, False),
    (1, "created", "프로세스 대기", WARN, False),
    (2, "running", "명령 실행 중", ACC, True),
    (3, "stopped", "프로세스 종료", MUTED, False),
]

for idx, name, sub, tone, is_focal in STATES:
    x = SX[idx]
    if is_focal:
        d.tone(x, SY, BW, BH, ACC, 8, "14", 1.4)
        tc = ACC
    elif tone == MUTED:
        d.box(x, SY, BW, BH, PAPER2, MUTED, 1.1, 8)
        tc = INK
    else:
        d.tone(x, SY, BW, BH, tone, 8, "12", 1.2)
        tc = tone
    d.t(x + BW // 2, SY + 26, name, 14, tc, MONO, "middle", 600)
    d.t(x + BW // 2, SY + 48, sub, 13, INK if is_focal else MUTED, KR, "middle")

# 전 상태 공통 연산 안내 (주석)
d.box(24, 340, 260, 36, PAPER2, RULE, 0.9, 6)
d.t(154, 362, "state 연산: 모든 상태 조회 가능", 13, MUTED, KR, "middle")

LEG_Y = 408
d.legend(
    LEG_Y,
    [
        ("생성 · 훅", INFO),
        ("실행 대기", WARN),
        ("실행 중", ACC),
        ("시작 · 정상", OK),
        ("중단 · 폐기", BAD),
    ],
)

out_path = sys.argv[1] if len(sys.argv) > 1 else str(pathlib.Path(__file__).resolve().parent.parent / "03-04.lifecycle-states.svg")
d.save(out_path)
print("ok gen-03-04.lifecycle-states")
