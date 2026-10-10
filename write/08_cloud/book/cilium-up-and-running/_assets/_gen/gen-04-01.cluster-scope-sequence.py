# 타입 스펙: type-sequence — Cluster Scope 에서 operator 가 CiliumNode 에 노드 몫을 적고 에이전트가 Pod IP 를 내주다 소진되는 순서.
# 사실 출처: 추출본 cil4.txt 줄 214-218 · 267-283 · 296-334, docs.cilium.io/en/stable/network/concepts/ipam/cluster-pool/ (spec.ipam.podCIDRs).
import sys
sys.path.insert(0, ".")
from dd import D, Seq, ACC, OK, WARN, INFO, BAD, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO

class SeqKR(Seq):
    def lanes(s, names, y0=104, lane_w=210):
        s.LX = {}; n = len(names)
        span = (s.w - 48 - 24) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            s.t(x, y0 + 20, nm, 12, INK, _kr(nm), "middle", 600)
            s.t(x, y0 + 37, sub, 11, MUTED, _kr(sub))
        s.lane_top = y0 + 44
        return s.LX
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]; d_ = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * d_} {y} L {x2 - 12 * d_} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 12 if _kr(label) == KR else 11, c, _kr(label), "middle", 600)
        if sub: s.t(mx, y + 17, sub, 12 if _kr(sub) == KR else 11, MUTED, _kr(sub))

W, H = 920, 548
d = SeqKR(W, H, "CILIUM UP AND RUNNING · 04-01 §3", "Cluster Scope 의 대역 기록과 소진",
          "operator 가 CiliumNode 에 노드 몫을 적고 에이전트가 그 안에서 Pod 주소를 냅니다",
          "기본 풀 10.0.0.0/8 · 작은 풀(/28 × 2, 노드 몫 /29) 실습")
L = d.lanes([("cilium-operator", "Deployment"), ("CiliumNode", "kind-worker"),
             ("cilium-agent", "DaemonSet"), ("Pod", "netshoot-client")], y0=100, lane_w=180)
YB = 490
d.rails(462)
d.msg("cilium-operator", "CiliumNode", "spec.ipam.podCIDRs", 196, INFO, "info", sub="10.0.1.0/24")
d.msg("CiliumNode", "cilium-agent", "watch", 248, ACC, "acc", sub="자기 노드 대역 수신")
d.msg("Pod", "cilium-agent", "IP 요청", 300, MUTED, "ar")
d.msg("cilium-agent", "Pod", "10.0.1.235", 352, OK, "ok", sub="netshoot-client")
d.line(24, 400, 448 - 100, 400, RULE, 0.8, "4 6")
d.line(448 + 100, 400, W - 48, 400, RULE, 0.8, "4 6")
d.chip(448, 400, "작은 풀 · 노드 몫 /29", SOFT, size=12)
d.msg("Pod", "cilium-agent", "IP 요청", 444, MUTED, "ar")
d.state("cilium-agent", "6/6 allocated", 478, WARN)
d.state("Pod", "ContainerCreating", 478, BAD)
d.legend(YB + 8, [("대역 기록", INFO), ("에이전트가 읽음", ACC), ("Pod IP 할당", OK), ("소진", WARN), ("멈춤", BAD)])
d.save("04-01.cluster-scope-sequence.svg")
