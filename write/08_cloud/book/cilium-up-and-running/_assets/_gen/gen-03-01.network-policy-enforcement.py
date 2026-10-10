# 타입 스펙: type-sequence — L3/L4 정책 단계(타임아웃)와 L7 정책 단계(403)에서 두 클라이언트 요청의 결과가 갈린다.
# 사실 출처: cil3.txt 줄 755~917 (ch03-policy, curl --max-time 3 exit 28, 50x.html Access denied, index.html 허용), cil3.txt 줄 1099~1110 (policy-verdict:none INGRESS DENIED), github.com/cilium/proxy cilium/l7policy.cc (Http::Code::Forbidden, 기본 본문 "Access denied").
import sys
sys.path.insert(0, ".")
from dd import Seq, ACC, OK, WARN, BAD, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

def _kr(t):
    return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

class SeqKR(Seq):
    def lanes(s, names, y0=104, lane_w=210):
        s.LX = {}; n = len(names)
        span = (s.w - 48 - 24) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            s.t(x, y0 + 20, nm, 12, INK, MONO, "middle", 600)
            s.t(x, y0 + 37, sub, 12 if _kr(sub) == KR else 11, MUTED, _kr(sub))
        s.lane_top = y0 + 44
        return s.LX
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None, lx=None):
        x1, x2 = s.LX[a], s.LX[b]; dr = 1 if x2 > x1 else -1
        mk = {OK: "ok", WARN: "warn", BAD: "bad"}.get(c, mk)
        s.path(f"M {x1 + 10 * dr} {y} L {x2 - 12 * dr} {y}", c, 1.5, m=mk, dash=dash)
        s.t(lx if lx else (x1 + x2) / 2, y - 9, label, 11, c, _kr(label), "middle", 600)
    def state(s, a, txt, y, c):
        x = s.LX[a]
        w = len(txt) * (7.6 if _kr(txt) == MONO else 12.0) + 20
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 4, txt, 11, c, _kr(txt))

W, H = 920, 624
d = SeqKR(W, H, "CILIUM UP AND RUNNING · 03-01 §5", "정책 단계마다 요청의 결과가 갈린다",
          "L3/L4 규칙은 조용히 버리고 L7 규칙은 HTTP 응답으로 거절한다",
          "라벨 없는 클라이언트는 타임아웃, 허용되지 않은 경로는 403")

NAMES = [("unauthorized-client", "라벨 없음"), ("netshoot-client", "10.244.1.67"),
         ("cilium-envoy", "L7 프록시"), ("nginx-deployment", "app: nginx · :80")]
d.lanes(NAMES, y0=104, lane_w=176)
d.rails(ybot=592)

def banner(y, txt, c):
    d.box(24, y, 872, 28, PAPER, c, sw=1.0, r=4)
    d.t(460, y + 19, txt, 12, c, _kr(txt), "middle", 600)

U, N, E, S = "unauthorized-client", "netshoot-client", "cilium-envoy", "nginx-deployment"
banner(164, "ch03-policy · L3/L4", INFO)
d.msg(U, S, "SYN :80", 220, BAD)
d.state(S, "INGRESS DENIED", 252, BAD)
d.state(U, "exit 28", 252, BAD)
d.msg(N, S, "SYN :80", 296, OK, lx=448)
d.msg(S, N, "200", 332, OK, dash="4 4", lx=448)

banner(356, "ch03-policy + L7 · GET /index.html", ACC)
d.msg(N, E, "GET /50x.html", 420, WARN)
d.msg(E, N, "403 · Access denied", 456, WARN, dash="4 4")
d.msg(N, E, "GET /index.html", 500, OK)
d.msg(E, S, "GET /index.html", 532, OK)
d.msg(S, N, "200", 568, OK, dash="4 4", lx=448)

d.save("03-01.network-policy-enforcement.svg")
