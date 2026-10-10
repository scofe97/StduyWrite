# 타입 스펙: type-architecture — 세 테스트 클러스터(red·green·blue)의 clustermesh-apiserver(etcd·kvstoremesh)와 노드 cilium-agent 간 상태 동기화 및 L3 데이터패스 아키텍처.
# 사실 출처: Cilium Up and Running 9장 cil9.txt 줄 222-246(메타데이터 전파), 253-270(노드 L3 데이터패스), 315-328(API Server·etcd 구조), 390-399(세 클러스터 설정 표) / docs.cilium.io v1.20 clustermesh/intro
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 600
d = D(W, H, "CILIUM UP AND RUNNING · 09-01", "세 클러스터의 Cluster Mesh 아키텍처",
      "각 클러스터의 API 서버가 메타데이터를 내보내고 상대가 읽어 하나의 망을 만든다",
      "중앙 조정자 없이 각 클러스터의 etcd 를 상호 조회하고 노드 간 직접 통신합니다")

CLUSTERS = [
    ("red", "id 1", "10.1.0.0/16", "10.89.0.14", 24, INFO),
    ("green", "id 2", "10.2.0.0/16", "10.89.0.16", 330, ACC),
    ("blue", "id 3", "10.3.0.0/16", "10.89.0.20", 636, OK),
]
ZONE_W, ZONE_H = 260, 384
ZONE_Y = 96

for name, cid, pod_cidr, node_ip, zx, col in CLUSTERS:
    # 클러스터 경계 상자
    d.box(zx, ZONE_Y, ZONE_W, ZONE_H, PAPER2, RULE, sw=0.9, r=8)
    d.chip(zx + 52, ZONE_Y + 22, f"cluster {name}", col, size=11)
    d.t(zx + ZONE_W - 14, ZONE_Y + 18, f"{cid} · {pod_cidr}", 11, MUTED, MONO, "end")
    d.t(zx + ZONE_W - 14, ZONE_Y + 34, f"node {node_ip}", 11, SOFT, MONO, "end")

    # clustermesh-apiserver Pod 영역
    pod_y = ZONE_Y + 48
    d.box(zx + 14, pod_y, ZONE_W - 28, 154, PAPER, RULE, sw=0.8, r=6)
    d.t(zx + 24, pod_y + 18, "apiserver Pod", 11, INK, MONO, "start", 600)

    # 1) apiserver 컨테이너
    d.box(zx + 22, pod_y + 28, ZONE_W - 44, 30, PAPER2, RULE, sw=0.7, r=4)
    d.t(zx + ZONE_W / 2, pod_y + 48, "apiserver (K8s 연동)", 11, INK, KR, "middle", 600)

    # 2) etcd 컨테이너 (focal)
    d.tone(zx + 22, pod_y + 64, ZONE_W - 44, 38, col, r=4, op="14", sw=1.2)
    d.t(zx + ZONE_W / 2, pod_y + 88, "etcd :32379", 12, col, MONO, "middle", 600)

    # 3) kvstoremesh 컨테이너
    d.box(zx + 22, pod_y + 108, ZONE_W - 44, 30, PAPER2, RULE, sw=0.7, r=4)
    d.t(zx + ZONE_W / 2, pod_y + 128, "kvstoremesh (캐시)", 11, INK, KR, "middle", 600)

    # worker 노드 및 cilium-agent
    node_y = ZONE_Y + 218
    d.box(zx + 14, node_y, ZONE_W - 28, 148, PAPER, RULE, sw=0.8, r=6)
    d.t(zx + 24, node_y + 20, f"{name}-worker 노드", 11, INK, KR, "start", 600)

    # cilium-agent
    d.box(zx + 22, node_y + 32, ZONE_W - 44, 46, PAPER2, RULE, sw=0.7, r=4)
    d.t(zx + ZONE_W / 2, node_y + 53, "cilium-agent", 12, INK, MONO, "middle", 600)
    d.t(zx + ZONE_W / 2, node_y + 68, "eBPF 데이터패스", 11, MUTED, KR, "middle")

    # 로컬 etcd 조회 수직 연결선 (cilium-agent -> etcd)
    cx_etcd = zx + ZONE_W - 36
    d.arrow([(cx_etcd, node_y + 32), (cx_etcd, pod_y + 102)], SOFT, "soft", sw=1.1, dash="3 3")

    # workload Pod
    d.box(zx + 22, node_y + 88, ZONE_W - 44, 44, PAPER2, OK if name == "red" else RULE, sw=0.8, r=4)
    d.t(zx + ZONE_W / 2, node_y + 115, "workload Pod", 12, INK, MONO, "middle", 600)

# 클러스터 간 mTLS 연결선 (green kvstoremesh -> red etcd & blue etcd)
# green kvstoremesh: x=352..568, center y = 96 + 48 + 123 = 267
# red etcd: x=46..238, center y = 96 + 48 + 83 = 227
# blue etcd: x=658..850, center y = 227
# Gap red-green is 284..330 (center 307)
# Gap green-blue is 590..636 (center 613)
d.path("M 352 267 H 307 V 227 H 238", MUTED, 1.3, m="ar")
d.t(307, 252, "mTLS", 11, MUTED, KR, "middle")

d.path("M 568 267 H 613 V 227 H 658", MUTED, 1.3, m="ar")
d.t(613, 252, ":32379", 11, MUTED, MONO, "middle")

# 하부 L3 언더레이 네트워크
L3_Y = 496
d.box(24, L3_Y, 872, 40, PAPER2, RULE, sw=0.9, r=6)
d.t(44, L3_Y + 25, "L3 언더레이 네트워크", 12, INK, KR, "start", 600)
d.t(230, L3_Y + 25, "터널 또는 네이티브 라우팅 (노드 간 직접 통신)", 11, MUTED, KR, "start")
d.t(876, L3_Y + 25, "게이트웨이 없음", 12, OK, KR, "end", 600)

for zx in [154, 460, 766]:
    d.arrow([(zx, ZONE_Y + ZONE_H), (zx, L3_Y)], OK, "ok", sw=1.2)

d.legend(556, [
    ("red (id 1)", INFO),
    ("green (id 2)", ACC),
    ("blue (id 3)", OK),
    ("L3 데이터패스", OK),
])
d.save("09-01.chapter-overview.svg")
