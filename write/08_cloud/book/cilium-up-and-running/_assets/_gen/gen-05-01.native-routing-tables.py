# 타입 스펙: type-architecture — 노드 둘을 존으로 묶고 경로표 행·eth0 칩·PodCIDR 칩을 놓는다. 흐름은 왼쪽 노드 eth0 에서 오른쪽 노드 eth0 로 가로 한 줄. focal 은 10.10.0.32/27 하나(경로 행·화살표 라벨·목적지 PodCIDR 을 같은 색으로 묶는다).
# 사실 출처: Cilium Up and Running 5장 cil5.txt 줄 461-501(ciliumnodes PodCIDR 와 docker exec ip route). kind-worker=10.10.0.64/27, kind-worker2=10.10.0.32/27, 노드 IP 172.18.0.3·0.2 는 각 경로표의 via 값에서 읽는다. docs.cilium.io v1.20.2 network/concepts/routing(autoDirectNodeRoutes)
import sys
sys.path.insert(0, ".")
from dd import D, ACC, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 392
d = D(W, H, "CILIUM UP AND RUNNING · 05-01 §2", "native routing 에서 경로표가 PodCIDR 을 잇는 방식",
      "autoDirectNodeRoutes: true 가 상대 노드의 PodCIDR 을 경로표에 넣는다", "autoDirectNodeRoutes: true 가 상대 노드의 PodCIDR 을 경로표에 넣는다")

ZY, ZH = 104, 252
nodes = [
    (24, "kind-worker", "PodCIDR 10.10.0.64/27", None,
     [("10.10.0.0/27 via 172.18.0.4 dev eth0", False), ("10.10.0.32/27 via 172.18.0.2 dev eth0", True)],
     "eth0 172.18.0.3"),
    (544, "kind-worker2", "PodCIDR 10.10.0.32/27", ACC,
     [("10.10.0.0/27 via 172.18.0.4 dev eth0", False), ("10.10.0.64/27 via 172.18.0.3 dev eth0", False)],
     "eth0 172.18.0.2"),
]

for x0, name, pod, pod_c, routes, eth in nodes:
    d.o.append(f'<rect x="{x0}" y="{ZY}" width="352" height="{ZH}" rx="8" fill="#161B2204" stroke="{SOFT}" stroke-width="0.9" stroke-dasharray="4 4"/>')
    d.t(x0 + 16, ZY + 24, name, 14, INK, MONO, "start", 600)
    d.chip(x0 + 16 + 79, ZY + 52, pod, pod_c or MUTED, 11)
    d.box(x0 + 16, ZY + 76, 320, 104, PAPER2, RULE, 0.9, r=6)
    d.t(x0 + 32, ZY + 96, "ip route", 11, SOFT, MONO, "start")
    for k, (txt, hot) in enumerate(routes):
        d.t(x0 + 32, ZY + 124 + k * 32, txt, 12, ACC if hot else INK, MONO, "start", 600 if hot else 400)
    d.chip(x0 + 16 + 58, ZY + 228, eth, INFO, 11)

# 왼쪽 노드: 일치한 경로 행 → eth0
d.arrow([(98, ZY + 184), (98, ZY + 208)], ACC, "acc", 1.5)
# 하부 망을 가로지르는 한 줄
d.arrow([(158, ZY + 228), (562, ZY + 228)], ACC, "acc", 1.7)
d.t(460, ZY + 218, "dst 10.10.0.32/27", 12, ACC, MONO, "middle", 600)
d.t(460, ZY + 24, "같은 L2 망", 12, MUTED, KR)
d.save("05-01.native-routing-tables.svg")
