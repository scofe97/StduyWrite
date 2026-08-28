# 07-01 §namespaced 타입과 cluster-scoped 타입
# 본문·옛 도식: 일부 타입은 namespace 안에 존재하고(Pods·ConfigMaps·Secrets·Events·PVC),
#   일부는 namespace 밖 클러스터 수준에 존재한다(Nodes·PersistentVolumes·StorageClasses·
#   Namespaces). 확인은 kubectl api-resources 의 NAMESPACED 열.
# 타입 스펙: type-nested.md — 어느 경계 *안* 에 있느냐가 그대로 답이라 위치로 말한다.
#           같은 타입 목록이 namespace 마다 반복되는 것도 사실이므로 두 벌을 그린다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 620
d = D(W, H, "KUBERNETES IN ACTION · 07-01",
      "어느 경계 안에 있느냐가 타입의 성질이다",
      "Pod·ConfigMap 처럼 namespace 안에 사는 타입은 namespace 마다 따로 존재하고, "
      "Node·PersistentVolume 처럼 클러스터 수준에 사는 타입은 하나뿐이다.",
      lead="kubectl api-resources 의 NAMESPACED 열이 이 구분을 그대로 알려준다")

OUTER = (48, 196, 904, 300)
NSA, NSB = (250, 308), (560, 308)
NW, NH = 260, 180
CLUSTER_Y = 448

ddx.band(d, 104, 564, "namespace 를 지우면 그 안의 것은 함께 사라지고, 밖의 것은 남는다")

ox, oy, ow, oh = OUTER
d.o.append(f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" rx="8" '
           f'fill="{INFO}06" stroke="{INFO}" stroke-width="1.2" stroke-dasharray="7 6"/>')
ddx.ring_label(d, ox, oy, "Kubernetes cluster", 11, INFO, off=16)

NAMESPACED = ["Pods", "ConfigMaps", "Secrets", "Events", "PersistentVolumeClaims"]
for (cx, cy), name in zip((NSA, NSB), ("Namespace A", "Namespace B")):
    d.o.append(f'<rect x="{cx-NW//2}" y="{cy-NH//2}" width="{NW}" height="{NH}" rx="6" '
               f'fill="{OK}0A" stroke="{OK}" stroke-width="1.2"/>')
    d.t(cx, cy - NH // 2 + 24, name, 12, OK, KR, "middle", 600)
    for i, t in enumerate(NAMESPACED):
        d.t(cx, cy - NH // 2 + 52 + i * 24, t, 11, MUTED, MONO)

# 760 에 가운데 정렬하면 왼쪽 끝이 Namespace B 상자(~690)를 파고든다 — 오른쪽으로 민다.
d.t(800, 262, "같은 타입이 namespace 마다", 11, SOFT, KR)
d.t(800, 282, "따로 존재한다", 11, SOFT, KR)

CLUSTER = ["Nodes", "PersistentVolumes", "StorageClasses", "Namespaces"]
for i, t in enumerate(CLUSTER):
    x = 60 + i * 224
    d.box(x, CLUSTER_Y - 26, 208, 52, PAPER2, WARN, 1.1, 6)
    d.t(x + 104, CLUSTER_Y + 5, t, 12, WARN, MONO)
# CLUSTER_Y-44 는 namespace 상자(218~398)의 아래 변을 지나 글자가 관통했다.
# 상자 아래와 클러스터 칸 위(422) 사이 빈 구간에 둔다.
d.t(48, CLUSTER_Y - 34, "namespace 밖 — 클러스터 수준에 하나씩만 있다", 11, WARN, KR, "start")

d.t(36, 524, "namespace 안에 사는 타입은 이름이 namespace 안에서만 고유하면 되고, 밖에 사는 "
             "타입은 클러스터 전체에서 고유해야 한다.", 12, MUTED, KR, "start")
d.legend(580, [("namespace 안에 사는 타입", OK), ("클러스터 수준에 사는 타입", WARN),
               ("물리 클러스터", INFO)])
d.save("07-01-namespaced-vs-cluster-scoped.svg")
print("ok namespaced-vs-cluster-scoped")
