# 06-03 §5 — cluster-proportional 오토스케일러가 클러스터 크기에서 복제본 수를 정하는 방식.
# 원문 근거: "By default, it will always maintain at least two replicas, and will set the replicas
#            such that there is one per 256 cores or one per 16 nodes in the cluster, whichever is
#            larger." 이 규칙만 원서 것이고, 노드당 코어 수는 원서에 없다.
#            그래서 두 계열(노드당 8코어 · 32코어)을 가정으로 명시하고 그 가정 위에서만 그린다.
#            값 = max(2, ceil(노드/16), ceil(노드×코어/256)) 로 산출한다. 눈대중 좌표 없음.
# 타입 스펙: type-line — 순차 지표 위의 추세이고, 두 계열이 갈리는 지점이 논지다.
#           축약: 스펙의 plot 여백(left 80 · bottom 60 · top 40)은 1000×500 기준인데 이 저장소의
#                 D() 머리글이 위쪽 90px 을 쓰므로 plot 을 아래로 밀고 캔버스를 560 으로 늘린다.
import sys, math; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, RULE, RULE as R, INFO, KR, MONO

W, H = 1000, 620
d = D(W, H, "LEARNING COREDNS · 06-03 §5",
      "클러스터가 커질 때 복제본이 어떻게 느는가",
      "가로축은 노드 수, 세로축은 CoreDNS 복제본 수다. 최소 둘을 깔고 16노드당 하나와 256코어당 하나 중 "
      "큰 쪽을 따르므로, 노드가 굵을수록 코어 규칙이 먼저 이긴다.",
      "노드당 코어 수는 원서에 없어 가정으로 둔 값입니다")

NODES = [8, 16, 32, 64, 128, 256]
SERIES = [(8, INFO, "노드당 8코어"), (32, ACC, "노드당 32코어")]
PX0, PX1, PY0, PY1 = 100, 940, 118, 418
YMAX = 32


def replicas(n, cores_per_node):
    return max(2, math.ceil(n / 16), math.ceil(n * cores_per_node / 256))


def px(i):
    return PX0 + i * (PX1 - PX0) / (len(NODES) - 1)


def py(v):
    return PY1 - v * (PY1 - PY0) / YMAX


for g in (0, 8, 16, 24, 32):
    d.line(PX0, py(g), PX1, py(g), RULE, 0.8)
    d.t(PX0 - 14, py(g) + 4, str(g), 12, SOFT, MONO, "end")
d.t(PX0 - 14, py(32) - 20, "복제본", 12, SOFT, KR, "end")

for i, n in enumerate(NODES):
    d.t(px(i), PY1 + 26, str(n), 12, SOFT, MONO)
d.t(PX1, PY1 + 48, "노드 수", 12, SOFT, KR, "end")

for cores, color, label in SERIES:
    pts = " ".join(f"{px(i):.1f},{py(replicas(n, cores)):.1f}" for i, n in enumerate(NODES))
    sw = 1.8 if color is ACC else 1.2
    d.o.append(f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linejoin="round"/>')
    if color is ACC:
        for i, n in enumerate(NODES):
            d.o.append(f'<circle cx="{px(i):.1f}" cy="{py(replicas(n, cores)):.1f}" r="4" fill="{color}"/>')

d.line(PX0, py(2), PX1, py(2), MUTED, 1.0, "5 4")
d.t(PX1 - 6, py(2) - 10, "최소 2 — 작은 클러스터는 여기 붙어 있다", 12, MUTED, KR, "end")

d.t(20, 508, "노드당 32코어면 256코어 규칙이 8노드마다 하나를 요구해 16노드 규칙보다 먼저 이긴다", 13, MUTED, KR, "start")
d.t(20, 532, "실제 필요는 워크로드가 정하므로 이 곡선은 출발점이지 답이 아니다", 13, MUTED, KR, "start")

d.legend(560, [("노드당 32코어", ACC), ("노드당 8코어", INFO)])
d.save("06-03.autoscale-curve.svg")
