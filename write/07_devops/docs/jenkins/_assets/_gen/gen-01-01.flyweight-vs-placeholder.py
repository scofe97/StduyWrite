# 타입 스펙: type-sequence
# 5절 Flyweight 와 일반 Task — Pipeline 빌드 하나가 OneOffExecutor 의 flyweight task 로 시작해 node 블록에서 PlaceholderTask 를 큐에 넣고 Agent 의 정규 Executor 를 점유하는 시간순
"""01-01 한 빌드가 두 Task 가 되는 순서 — 도식 생성기.

실행: cd ~/runners-high/write/07_devops/docs/jenkins/_assets && python3 -B _gen/gen-01-01.flyweight-vs-placeholder.py
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import (Seq, PAPER2, INK, MUTED, RULE, ACC,  # noqa: E402
                OK, INFO, KR, MONO)


def _kr(txt):
    """한글이 섞이면 한글 스택으로. Seq 프리미티브가 MONO 를 하드코딩하는 자리를 덮는다."""
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


class SeqKR(Seq):
    def lanes(s, names, y0=104, lane_w=212):
        s.LX = {}
        n = len(names)
        span = (s.w - 48 - 24) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 48, PAPER2, RULE, 1.0)
            s.t(x, y0 + 21, nm, 14, INK, _kr(nm), "middle", 600)
            s.t(x, y0 + 40, sub, 13, MUTED, _kr(sub))
        s.lane_top = y0 + 48
        return s.LX

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        d = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * d} {y} L {x2 - 12 * d} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 10, label, 13, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 20, sub, 13, MUTED, _kr(sub))

    def state(s, a, txt, y, c):
        x = s.LX[a]
        han = sum(1 for ch in str(txt) if "가" <= ch <= "힣")
        w = han * 13.0 + (len(txt) - han) * 7.8 + 20
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 12}" width="{w}" height="24" rx="4" '
                   f'fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 5, txt, 13, c, _kr(txt))


W, H = 960, 604

d = SeqKR(
    W, H,
    "JENKINS · FLYWEIGHT TASK AND PLACEHOLDER TASK",
    "Pipeline 빌드 하나가 두 Task 가 되는 순서",
    "Pipeline 빌드는 Controller 의 OneOffExecutor 에서 flyweight task 로 시작하고 node 블록에서 PlaceholderTask 를 큐에 넣어 Agent 의 정규 Executor 하나를 점유한다",
    lead="첫 Task 는 Controller 에 남은 채 node 블록이 큐에 넣은 둘째 Task 가 Agent 슬롯을 잡는다"
)

d.lanes([
    ("Queue", "대기열"),
    ("Controller", "OneOffExecutor"),
    ("Agent", "정규 Executor"),
], y0=104, lane_w=212)
d.rails(560)

d.msg("Queue", "Controller", "1. 빌드 시작", 196, INFO, "info", sub="flyweight task")
d.state("Controller", "Task 1 · WorkflowJob", 244, INFO)
# Task 1 은 빌드가 끝날 때까지 Controller 에 남는다
bx = d.LX["Controller"]
d.o.append(f'<rect x="{bx - 6}" y="262" width="12" height="290" rx="2" fill="{INFO}33" stroke="{INFO}" stroke-width="1.0"/>')
d.msg("Controller", "Queue", "2. node 블록 진입", 316, ACC, "acc", sub="PlaceholderTask 를 큐에 넣음")
d.msg("Queue", "Agent", "", 396, INFO, "info")
d.t(600, 386, "3. 슬롯 배정", 13, INFO, KR, "middle", 600)
d.t(600, 416, "정규 Executor 1개", 13, MUTED, KR)
d.state("Agent", "Task 2 · PlaceholderTask", 444, OK)
ax = d.LX["Agent"]
d.o.append(f'<rect x="{ax - 6}" y="458" width="12" height="42" rx="2" fill="{OK}33" stroke="{OK}" stroke-width="1.0"/>')
d.state("Agent", "4. 블록 끝 · 슬롯 비움", 520, OK)

d.legend(560, [
    ("Task 1 (빌드가 끝날 때까지 Controller 에 남음)", INFO),
    ("큐에 새로 넣는 Task", ACC),
    ("Agent 슬롯 점유 구간", OK),
])

out = pathlib.Path(__file__).resolve().parent.parent / "01-01.flyweight-vs-placeholder.svg"
d.save(str(out))
print("saved", out)
