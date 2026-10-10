# 타입 스펙: type-sequence — KPR 에서 에이전트가 API 서버에 실제 주소로 접속해 서비스 맵을 채우고 첫 요청이 소켓 단계에서 변환되는 순서
# 사실 출처: 추출본 cil6.txt 줄 253-277(k8sServiceHost), 369-417(service list·/proc), 442-445 / docs.cilium.io v1.20 kubeproxy-free(Socket LoadBalancer)
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
d = SeqKR(W, H, "CILIUM UP AND RUNNING · 06-01 §3", "KPR 기동과 첫 요청의 순서",
          "에이전트가 API 서버 실제 주소로 맵을 채우고 소켓이 백엔드에 붙습니다",
          "kind 클러스터 · kube-proxy 없음")
L = d.lanes([("kube-apiserver", "kind-control-plane"), ("cilium-agent", "DaemonSet"),
             ("서비스 맵", "eBPF"), ("netshoot-client", "Pod")], y0=100, lane_w=180)
d.rails(462)
d.msg("cilium-agent", "kube-apiserver", "kind-control-plane:6443", 196, INFO, "info", sub="VIP 거치지 않음")
d.msg("kube-apiserver", "cilium-agent", "Service · 백엔드", 248, INFO, "info", sub="10.96.45.144 · 2개")
d.msg("cilium-agent", "서비스 맵", "맵 적재", 300, ACC, "acc", sub="10.0.1.199 · 10.0.2.208")
d.line(24, 352, 448 - 90, 352, RULE, 0.8, "4 6")
d.line(448 + 90, 352, W - 48, 352, RULE, 0.8, "4 6")
d.chip(448, 352, "첫 요청", SOFT, size=12)
d.msg("netshoot-client", "서비스 맵", "connect 10.96.45.144:80", 404, MUTED, "ar")
d.msg("서비스 맵", "netshoot-client", "소켓 → 10.0.2.208:80", 456, OK, "ok", sub="rem_address D002000A:0050")
d.legend(492, [("API 서버 통신", INFO), ("맵 적재", ACC), ("소켓 변환", OK)])
d.save("06-01.kpr-api-server-sequence.svg")
