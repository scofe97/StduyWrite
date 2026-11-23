# 타입 스펙: type-architecture
# 3절 Executor 0 의 의미 — Built-In Node 의 Executor 수와 Agent 유무에 따라 일반 빌드가 가는 곳 셋
"""01-01 일반 빌드가 가는 길 — 도식 생성기.

실행: cd ~/runners-high/write/07_devops/docs/jenkins/_assets && python3 -B _gen/gen-01-01.executor-zero.py
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import (D, PAPER2, INK, MUTED, RULE, ACC,  # noqa: E402
                BAD, WARN, INFO, KR, MONO)

W, H = 960, 440

d = D(
    W, H,
    "JENKINS · WHERE A BUILD RUNS",
    "Executor 수와 Agent 유무에 따라 일반 빌드가 가는 곳",
    "Built-In Node 의 Executor 가 2 이고 Agent 가 없으면 Controller 에서, Executor 가 0 이고 Agent 가 있으면 Agent 에서, 둘 다 없으면 큐에서 기다린다",
    lead="조건 셋마다 일반 빌드가 도는 곳이 다르고 Executor 0 에 Agent 가 있는 경우가 권장 경로"
)


def fam(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


# 출발 노드
d.box(40, 188, 152, 64, PAPER2, INFO, 1.2, 6)
d.t(116, 216, "일반 빌드", 14, INK, KR, "middle", 600)
d.t(116, 238, "Freestyle 등", 13, MUTED, KR)

# 갈래: 버스 x=232, 세 행 y=140, 220, 300 (중심선)
ys = [140, 220, 300]
d.line(232, 140, 232, 300, MUTED, 1.4)
d.path("M 192 220 H 232", MUTED, 1.4)
cases = [
    ("Executor 2 (기본값)", "Agent · 클라우드 없음", "Controller", "빌드가 Controller 파일에 접근", BAD),
    ("Executor 0 (권장)", "Agent · 클라우드 있음", "Agent", "빌드와 Controller 파일 분리", ACC),
    ("Executor 0 (권장)", "Agent · 클라우드 없음", "큐에서 대기", "Agent 가 붙을 때까지 시작하지 못함", WARN),
]
for y, (c1, c2, dest, eff, col) in zip(ys, cases):
    mk = {"": "ar"}.get("", "ar")
    mk = "acc" if col == ACC else ("bad" if col == BAD else "warn")
    d.arrow([(232, y), (520, y)], col, mk, 1.5)
    d.t(376, y - 26, c1, 13, INK, fam(c1), "middle", 600)
    d.t(376, y - 8, c2, 13, MUTED, fam(c2), "middle")
    if col == ACC:
        d.tone(520, y - 32, 400, 64, ACC, r=6, op="12", sw=1.4)
    else:
        d.tone(520, y - 32, 400, 64, col, r=6)
    d.t(536, y - 6, dest, 14, col, fam(dest), "start", 600)
    d.t(536, y + 18, eff, 13, INK, fam(eff), "start")

d.legend(380, [
    ("권장 경로", ACC),
    ("Controller 에서 실행", BAD),
    ("시작하지 못함", WARN),
    ("출발", INFO),
])

out = pathlib.Path(__file__).resolve().parent.parent / "01-01.executor-zero.svg"
d.save(str(out))
print("saved", out)
