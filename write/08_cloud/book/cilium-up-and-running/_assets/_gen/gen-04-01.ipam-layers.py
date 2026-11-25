# 타입 스펙: type-layers — 클러스터 풀 → 노드 PodCIDR → Pod IP 세 단계 대역 분할(Cluster Scope 기본값 예).
# 사실 출처: 추출본 ch04.txt 줄 249-258 · 267-268 · 280-283, Helm 레퍼런스 ipam.operator.clusterPoolIPv4PodCIDRList 기본 10.0.0.0/8.
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, INFO, SOFT, MUTED, INK, PAPER2, RULE, KR, MONO

W, H = 920, 444
d = D(W, H, "CILIUM UP AND RUNNING · 04-01 §1", "클러스터 풀에서 Pod IP 까지 세 단계",
      "큰 풀을 노드 몫으로 나누고 노드 몫 안에서 주소 하나씩 내줍니다",
      "Cluster Scope 기본값 10.0.0.0/8 · 마스크 /24 기준")

LX, LW, LH, STRIDE, Y0 = 32, 856, 72, 96, 100
layers = [
    ("1단계", "클러스터 풀", "10.0.0.0/8", "clusterPoolIPv4PodCIDRList", INFO),
    ("2단계", "노드 PodCIDR", "10.0.1.0/24", "kind-worker · CiliumNode", "focal"),
    ("3단계", "Pod IP", None, None, None),
]
for i, (tag, name, val, sub, mark) in enumerate(layers):
    y = Y0 + i * STRIDE
    if mark == "focal":
        d.tone(LX, y, LW, LH, ACC, r=6, op="12", sw=1.4)
        nc = ACC
    elif mark == INFO:
        d.tone(LX, y, LW, LH, INFO, r=6, op="10", sw=1.0)
        nc = INFO
    else:
        d.box(LX, y, LW, LH, PAPER2, RULE, 0.9, 6)
        nc = INK
    d.t(LX + 16, y + 28, tag, 11, SOFT, KR, "start")
    d.t(LX + 52, y + 44, name, 16, nc, KR, "start", 600)
    if val:
        d.t(LX + 300, y + 44, val, 16, nc, MONO, "start", 600)
    if sub:
        d.t(LX + LW - 16, y + 44, sub, 10, MUTED, MONO, "end")

yl3 = Y0 + 2 * STRIDE
for cx, txt, c in [(LX + 372, "10.0.1.235 Pod", OK), (LX + 566, "10.0.1.133 router", MUTED), (LX + 724, "10.0.1.238 health", MUTED)]:
    d.chip(cx, yl3 + 40, txt, c, size=11)

for i, lab in enumerate(["cilium-operator 가 /24 로 분할 (모드마다 배분 주체가 다름)", "cilium-agent 가 주소 하나씩 배정"]):
    y = Y0 + i * STRIDE + LH
    cx = LX + 120
    d.arrow([(cx, y + 3), (cx, y + STRIDE - LH - 3)], MUTED, "ar", 1.4)
    d.t(cx + 14, y + 17, lab, 13, MUTED, KR, "start")

d.legend(H - 48, [("전체 풀", INFO), ("노드 몫(갈림길)", ACC), ("Pod IP", OK), ("노드 인프라 예약", MUTED)])
d.save("04-01.ipam-layers.svg")
