# 타입 스펙: type-gantt
# 7절 agent 를 둔 자리에 따라 Executor 슬롯을 잡는 구간 — stage 를 가로로 놓고 점유 구간을 띠로 보인다
"""01-02 agent 지시어 위치와 슬롯 점유 구간 — 도식 생성기.

실행: cd ~/runners-high/write/07_devops/docs/jenkins/_assets && python3 -B _gen/gen-01-02.agent-scope.py
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import (D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC,  # noqa: E402
                OK, WARN, KR, MONO)

W = 960
TX, CW = 272, 208                    # 타임라인 시작 x, stage 칸 폭
HY = 100                             # 헤더 y
ROW1, ROW2, RH = 152, 236, 72        # 행 존 y, 행 높이
BAR_H = 40
LEG_Y = ROW2 + RH + 28
H = LEG_Y + 48

d = D(
    W, H,
    "JENKINS · AGENT SCOPE AND EXECUTOR HOLD",
    "agent 위치에 따른 Executor 점유 구간",
    "최상위 agent any 는 첫 stage 부터 마지막 stage 까지 Executor 하나를 잡고, 최상위 agent none 에 stage 별 agent 를 두면 그 stage 가 도는 동안만 잡으며 input 지시어의 승인 대기는 agent 블록 진입 전이라 잡지 않는다",
    lead="승인을 stage 의 input 지시어로 받는 파이프라인에서 Executor 를 잡고 있는 구간입니다",
)


def row_zone(y):
    d.o.append(f'<rect x="24" y="{y}" width="{W - 48}" height="{RH}" rx="8" '
               f'fill="{INK}05" stroke="{INK}1A" stroke-width="0.8"/>')


def bar(x, w, y, c, label=None, anchor="start"):
    d.tone(x, y, w, BAR_H, c, r=4, op="1F", sw=1.2)
    if label:
        tx = x + 12 if anchor == "start" else x + w - 12
        d.t(tx, y + 25, label, 13, INK, KR, anchor, 600)


# ── 헤더: stage 칸 ──────────────────────────────────────────────────
d.t(24, HY + 24, "stage 순서 →", 13, MUTED, KR, "start")
for i, name in enumerate(["Build", "승인 대기 (input)", "Deploy"]):
    x = TX + i * CW
    fam = MONO if name.isascii() else KR
    if i == 1:
        d.tone(x + 4, HY, CW - 8, 36, ACC, r=6, op="12", sw=1.4)
        d.t(x + CW // 2, HY + 24, name, 14, ACC, fam, "middle", 600)
    else:
        d.box(x + 4, HY, CW - 8, 36, PAPER2, RULE, 1.0, 6)
        d.t(x + CW // 2, HY + 24, name, 14, INK, fam, "middle", 600)

# ── 행 존 + 칸 구분선 ───────────────────────────────────────────────
row_zone(ROW1)
row_zone(ROW2)
for i in (1, 2):
    x = TX + i * CW
    d.line(x, ROW1 + 8, x, ROW2 + RH - 8, RULE, 1.0, "3 6")

# ── 행 1: 최상위 agent any ──────────────────────────────────────────
y1 = ROW1 + 16
d.t(40, y1 + 18, "agent any", 14, INK, MONO, "start", 600)
d.t(40, y1 + 38, "최상위에 선언", 13, MUTED, KR, "start")
bar(TX + 4, 3 * CW - 8, y1, WARN, "Executor 1개 점유")
d.t(TX + 3 * CW - 16, y1 + 25, "마지막 stage 까지", 13, INK, KR, "end", 600)
d.chip(TX + CW + CW // 2, y1 + BAR_H // 2, "승인 대기 중에도 점유", ACC, 13)

# ── 행 2: 최상위 agent none + stage 별 agent ───────────────────────
y2 = ROW2 + 16
d.t(40, y2 + 18, "agent none", 14, INK, MONO, "start", 600)
d.t(40, y2 + 38, "stage 마다 agent 선언", 13, MUTED, KR, "start")
bar(TX + 4, CW - 8, y2, OK, "Executor 점유")
d.o.append(f'<rect x="{TX + CW + 4}" y="{y2}" width="{CW - 8}" height="{BAR_H}" rx="4" '
           f'fill="none" stroke="{MUTED}" stroke-width="1" stroke-dasharray="4 4"/>')
d.t(TX + CW + CW // 2, y2 + 25, "점유 없음", 13, MUTED, KR, "middle")
bar(TX + 2 * CW + 4, CW - 8, y2, OK, "Executor 점유")

d.legend(LEG_Y, [
    ("agent any 점유", WARN),
    ("stage 별 agent 점유", OK),
    ("점유 없음", MUTED),
    ("대기 중 점유", ACC),
])

out_path = pathlib.Path(__file__).resolve().parent.parent / "01-02.agent-scope.svg"
d.save(str(out_path))
print("saved", out_path)
