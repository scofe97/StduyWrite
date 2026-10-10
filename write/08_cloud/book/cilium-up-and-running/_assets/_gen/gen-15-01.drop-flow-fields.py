# 타입 스펙: type-data-flow — 거부된 흐름 한 건의 JSON 필드(출발·도착·verdict·사유)가 허용 정책의 어느 칸으로 옮겨 가는지. 실제 값이 단계마다 움직인다.
# 사실 출처: Cilium Up and Running 15장 cil15.txt 줄 351-377(JSON 출력 값), 381-403(필드를 정책으로 옮김)
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 462
d = D(W, H, "CILIUM UP AND RUNNING · 15-01 §2", "거부된 흐름 한 건의 필드",
      "JSON 의 출발·도착·사유가 허용 정책의 어느 칸으로 옮겨 가는지",
      "JSON 의 출발·도착·사유가 허용 정책의 어느 칸으로 옮겨 가는지")

d.chip(210, 100, "hubble observe -n webshop -t drop -o json", SOFT, size=10)

# 출발 / 도착
d.box(24, 128, 270, 150, PAPER2, RULE, 0.9, r=6)
d.t(40, 152, "source", 11, SOFT, MONO, "start", 600)
d.t(40, 180, "pod_name", 11, MUTED, MONO, "start")
d.t(40, 200, "frontend-6f947cd9db-7v7t5", 11, INK, MONO, "start")
d.t(40, 226, "labels", 11, MUTED, MONO, "start")
d.t(40, 246, "k8s:app=frontend", 11, ACC, MONO, "start", 600)
d.t(40, 268, "10.0.0.248 : 48248", 11, INK, MONO, "start")

d.tone(325, 156, 270, 94, BAD, r=6, op="14", sw=1.2)
d.t(460, 184, "verdict", 11, MUTED, MONO)
d.t(460, 206, "DROPPED", 14, BAD, MONO, "middle", 600)
d.t(460, 230, "POLICY_DENIED", 12, BAD, MONO, "middle", 600)

d.box(626, 128, 270, 150, PAPER2, RULE, 0.9, r=6)
d.t(642, 152, "destination", 11, SOFT, MONO, "start", 600)
d.t(642, 180, "pod_name", 11, MUTED, MONO, "start")
d.t(642, 200, "recommendationservice-5df568d8b9-fpnzs", 10, INK, MONO, "start")
d.t(642, 226, "labels", 11, MUTED, MONO, "start")
d.t(642, 246, "k8s:app=recommendationservice", 11, OK, MONO, "start", 600)
d.t(642, 268, "10.0.2.211 : 8080", 11, INK, MONO, "start")

d.arrow([(294, 203), (325, 203)], MUTED, "ar", sw=1.3)
d.arrow([(595, 203), (626, 203)], MUTED, "ar", sw=1.3)

# 정책 칸으로
d.t(24, 316, "허용 정책 초안", 11, SOFT, KR, "start", 600)
d.box(24, 328, 872, 56, PAPER2, RULE, 0.9, r=6)
d.t(40, 352, "endpointSelector", 11, MUTED, MONO, "start")
d.t(40, 372, "app=frontend", 12, ACC, MONO, "start", 600)
d.t(312, 352, "toEndpoints", 11, MUTED, MONO, "start")
d.t(312, 372, "app=recommendationservice", 12, OK, MONO, "start", 600)
d.t(660, 352, "toPorts", 11, MUTED, MONO, "start")
d.t(660, 372, "8080 / TCP", 12, INK, MONO, "start", 600)
d.arrow([(160, 278), (160, 328)], ACC, "acc", sw=1.3)
d.arrow([(760, 278), (760, 316), (460, 316), (460, 328)], OK, "ok", sw=1.3)

d.legend(420, [("출발 Pod", ACC), ("도착 Pod", OK), ("거부 판정", BAD)])
d.save("15-01.drop-flow-fields.svg")
