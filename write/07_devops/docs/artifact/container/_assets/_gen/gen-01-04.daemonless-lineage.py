# 타입 스펙: type-timeline
# 01-04.daemonless-lineage — 격리·표준·빌더의 등장 계보
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 700

d = D(
    W, H,
    "CONTAINER · 01-04",
    "격리·표준·빌더의 등장 계보",
    "UNIX V7 chroot 에서 Linux namespace·cgroups, Docker 단일 데몬, OCI 표준 분리, kaniko 와 K8s dockershim 제거, kaniko 보관과 포크 전환까지의 계보 연표. 연표 끝에는 데몬 없는 빌드의 세 갈래(사용자 공간 스냅숏, rootless 실행·user namespace, Dockerfile 없는 빌드)를 모았다",
    lead="커널 격리, root 데몬, OCI 표준의 시점과 데몬 없는 빌드의 세 갈래",
)

AXIS_Y = 264

# ── 좌측 레인 머리 ───────────────────────────────────────────────────
d.box(16, 132, 108, 56, PAPER2, INFO, 1.0, 6)
d.t(70, 156, "격리 · 표준", 13, INFO, KR, "middle", 600)
d.t(70, 176, "커널 · OCI", 13, MUTED, KR, "middle")

d.box(16, 336, 108, 56, PAPER2, OK, 1.0, 6)
d.t(70, 360, "런타임 · 빌더", 13, OK, KR, "middle", 600)
d.t(70, 380, "엔진 · CI", 13, MUTED, KR, "middle")

# ── 시간축 기준선 (축 단절 // 두 곳: V7→2.4.19, 2008→2013; 2013~2025 비례) ──
d.line(136, AXIS_Y, 184, AXIS_Y, MUTED, 1.6)
# 축 단절 1 (//)
d.line(188, AXIS_Y + 8, 194, AXIS_Y - 8, MUTED, 1.4)
d.line(196, AXIS_Y + 8, 202, AXIS_Y - 8, MUTED, 1.4)

d.line(208, AXIS_Y, 320, AXIS_Y, MUTED, 1.6)
# 축 단절 2 (//)
d.line(324, AXIS_Y + 8, 330, AXIS_Y - 8, MUTED, 1.4)
d.line(332, AXIS_Y + 8, 338, AXIS_Y - 8, MUTED, 1.4)

# 2013 ~ 2025 실선 (오른쪽 끝 세 갈래 분기점까지)
d.line(344, AXIS_Y, 966, AXIS_Y, MUTED, 1.6)

# ── 사건 정의 ────────────────────────────────────────────────────────
# 상단 레인: 커널 격리와 OCI 표준
UPPER = [
    # (dot_x, card_x, card_y, card_w, color, date_txt, label_txt, label_fam)
    (160, 136, 92, 92, INFO, "UNIX V7", "chroot", MONO),
    (232, 176, 172, 112, INFO, "Linux 2.4.19", "mount ns", MONO),
    (304, 244, 92, 148, INFO, "2008.01 · 2.6.24", "cgroups · PID ns", MONO),
    (368, 316, 172, 132, INFO, "2013.02 · 3.8", "user ns 비특권", KR),
    (472, 424, 92, 100, INFO, "2015.06", "OCI 설립", KR),
    (560, 488, 172, 192, INFO, "2017.07", "OCI image·runtime 1.0", MONO),
    (732, 644, 92, 180, INFO, "2021.05", "OCI distribution 1.0", MONO),
]

# 하단 레인: 런타임·빌더·CI 변화
LOWER = [
    # (dot_x, card_x, card_y, card_w, color, date_txt, label_txt, label_fam)
    (384, 288, 300, 204, WARN, "2013.03", "Docker v0.1 · root 데몬", KR),
    (596, 532, 300, 128, OK, "2018.04", "kaniko 공개", KR),
    (776, 668, 380, 212, BAD, "2022.05", "K8s 1.24 dockershim 제거", KR),
    (908, 792, 300, 156, WARN, "2025.06", "kaniko 보관 · 포크", KR),
]

CARD_H = 56

# ── 지시선 먼저 (z-order) ─────────────────────────────────────────────
for dot_x, cx, cy, cw, c, _, _, _ in UPPER:
    d.line(dot_x, cy + CARD_H, dot_x, AXIS_Y - 5, c, 1.1)

for dot_x, cx, cy, cw, c, _, _, _ in LOWER:
    d.line(dot_x, AXIS_Y + 5, dot_x, cy, c, 1.1)

# ── 상단 카드 및 축 점 ────────────────────────────────────────────────
for dot_x, cx, cy, cw, c, dt, lb, lfam in UPPER:
    d.box(cx, cy, cw, CARD_H, PAPER2, c, 1.0, 6)
    d.o.append(f'<circle cx="{dot_x}" cy="{AXIS_Y}" r="4.5" fill="{c}" stroke="{PAPER}" stroke-width="1.2"/>')
    d.t(cx + cw // 2, cy + 22, dt, 13, c, MONO, "middle", 600)
    d.t(cx + cw // 2, cy + 44, lb, 13, INK, lfam, "middle")

# ── 하단 카드 및 축 점 ────────────────────────────────────────────────
for dot_x, cx, cy, cw, c, dt, lb, lfam in LOWER:
    d.tone(cx, cy, cw, CARD_H, c, 6, "10", 1.1)
    d.o.append(f'<circle cx="{dot_x}" cy="{AXIS_Y}" r="4.5" fill="{c}" stroke="{PAPER}" stroke-width="1.2"/>')
    d.t(cx + cw // 2, cy + 22, dt, 13, c, MONO, "middle", 600)
    d.t(cx + cw // 2, cy + 44, lb, 13, INK, lfam, "middle")

# ── 연표 끝 → 데몬 없는 빌드의 세 갈래 (주황 강조 focal) ──────────────
d.o.append(f'<circle cx="972" cy="{AXIS_Y}" r="6" fill="{ACC}" stroke="{PAPER}" stroke-width="1.5"/>')
d.arrow([(972, AXIS_Y + 6), (972, 456), (500, 456), (500, 476)], ACC, "acc", 1.6)

# 세 갈래 강조 영역
d.tone(16, 480, 968, 152, ACC, 8, "12", 1.4)
d.t(500, 504, "데몬 없는 빌드의 세 갈래", 13, ACC, KR, "middle", 600)

# 내부 분기 트리 (수직 → 수평 버스 → 3등분 화살표)
d.line(500, 512, 500, 524, ACC, 1.4)
d.line(180, 524, 820, 524, ACC, 1.4)

BRANCHES = [
    # (card_x, center_x, title, tools)
    (28, 180, "사용자 공간 스냅숏", "kaniko (2018.04)"),
    (348, 500, "rootless 실행 · user namespace", "BuildKit rootless · Buildah"),
    (668, 820, "Dockerfile 없는 빌드", "Jib · ko · Buildpacks(kpack)"),
]

for bx, cx, title, tools in BRANCHES:
    d.arrow([(cx, 524), (cx, 544)], ACC, "acc", 1.4)
    d.box(bx, 548, 304, 68, PAPER2, ACC, 1.1, 6)
    d.t(cx, 574, title, 13, ACC, KR, "middle", 600)
    d.t(cx, 598, tools, 12, INK, MONO, "middle")

# ── 범례 ────────────────────────────────────────────────────────────
LEG_Y = 652
d.legend(LEG_Y, [
    ("격리·표준", INFO),
    ("런타임·빌더", OK),
    ("데몬·보관 제약", WARN),
    ("런타임 제거", BAD),
    ("데몬 없는 세 갈래", ACC),
])

out_path = sys.argv[1] if len(sys.argv) > 1 else str(pathlib.Path(__file__).resolve().parent.parent / "01-04.daemonless-lineage.svg")
d.save(out_path)
print("ok gen-01-04.daemonless-lineage")
