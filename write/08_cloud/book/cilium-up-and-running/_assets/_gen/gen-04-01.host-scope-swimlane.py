# 타입 스펙: type-swimlane — Host Scope 에서 kube-controller-manager 가 Node 에 적은 PodCIDR 이 에이전트와 Pod 로 내려가는 순서.
# 사실 출처: 추출본 cil4.txt 줄 136-139 · 169-188, docs.cilium.io/en/stable/network/concepts/ipam/kubernetes/ (--allocate-node-cidrs, spec.podCIDRs).
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 520
d = D(W, H, "CILIUM UP AND RUNNING · 04-01 §2", "Host Scope 의 대역 전달 순서",
      "쿠버네티스가 Node 에 적은 값을 에이전트가 읽어 Pod 주소로 씁니다",
      "kind 클러스터 · kind-worker 노드 기준")

LBL_X, LBL_W, BODY_X, BODY_W, LANE_H, STRIDE, Y0 = 24, 152, 180, 716, 80, 92, 100
lanes = [
    ("kube-controller-manager", "컨트롤 플레인", INFO),
    ("Node", "kind-worker", INFO),
    ("cilium-agent", "노드 데몬", ACC),
    ("Pod", "netshoot-client", OK),
]
for i, (nm, sub, c) in enumerate(lanes):
    y = Y0 + i * STRIDE
    d.box(LBL_X, y, LBL_W, LANE_H, PAPER2, RULE, 0.9, 6)
    d.t(LBL_X + LBL_W / 2, y + 36, nm, 10, c, MONO, "middle", 600)
    d.t(LBL_X + LBL_W / 2, y + 56, sub, 12, MUTED, KR, "middle")
    d.box(BODY_X, y, BODY_W, LANE_H, PAPER2, RULE, 0.9, 6)

SW, SH = 152, 56
steps = [
    (0, 196, "PodCIDR 할당", "10.244.1.0/24", INFO),
    (1, 368, "Node 에 기록", "spec.podCIDRs", INFO),
    (2, 540, "대역 수신", "10.244.1.0/24", "focal"),
    (3, 712, "IP 배정", "10.244.1.20", OK),
]
for ln, x, t1, t2, c in steps:
    y = Y0 + ln * STRIDE + (LANE_H - SH) // 2
    if c == "focal":
        d.tone(x, y, SW, SH, ACC, r=4, op="14", sw=1.4); cc = ACC
    else:
        d.box(x, y, SW, SH, PAPER, c, 1.0, 4); cc = c
    d.t(x + SW / 2, y + 24, t1, 12, cc, KR, "middle", 600)
    d.t(x + SW / 2, y + 44, t2, 11, INK, MONO, "middle")

for k in range(3):
    ln0, x0 = steps[k][0], steps[k][1]
    ln1, x1 = steps[k + 1][0], steps[k + 1][1]
    ya = Y0 + ln0 * STRIDE + LANE_H // 2
    yb = Y0 + ln1 * STRIDE + (LANE_H - SH) // 2
    d.arrow([(x0 + SW, ya), (x1 + SW // 2, ya), (x1 + SW // 2, yb)], INFO if k < 2 else ACC, "info" if k < 2 else "acc", 1.5)

d.legend(Y0 + 4 * STRIDE + 8, [("쿠버네티스", INFO), ("Cilium 에이전트", ACC), ("Pod", OK)])
d.save("04-01.host-scope-swimlane.svg")
