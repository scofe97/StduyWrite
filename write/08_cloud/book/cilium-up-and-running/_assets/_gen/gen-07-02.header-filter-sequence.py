# 타입 스펙: type-sequence — 클라이언트·Gateway(Envoy)·echo-1 세 레인. 먼저 /cilium-add-a-request-header 요청 헤더 추가, 이어서 /multiple 응답 헤더 추가. 레인은 장치, 메시지는 요청·응답 한 번의 이동.
# 사실 출처: Cilium Up and Running 7장 cil7.txt 줄 1175·1190(RequestHeaderModifier, My-Cilium-Header-Name: my-cilium-header-value), 1235-1245(ResponseHeaderModifier, /multiple, x-header-add-1·2)
import sys
sys.path.insert(0, ".")
from dd import D, Seq, ACC, OK, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO


def _kr(t):
    return KR if any("가" <= c <= "힣" for c in str(t)) else MONO


class S(Seq):
    def lanes(s, names, xs, y0=96, lane_w=200):
        s.LX = {}
        for (nm, sub), x in zip(names, xs):
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            s.t(x, y0 + 20, nm, 12, INK, _kr(nm), "middle", 600)
            s.t(x, y0 + 37, sub, 11, MUTED, _kr(sub))
        s.lane_top = y0 + 44

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        dr = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dr} {y} L {x2 - 12 * dr} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 12, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 18, sub, 12, MUTED, _kr(sub))

    def state(s, a, txt, y, c):
        x = s.LX[a]
        w = len(txt) * 7.4 + 22
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 4, txt, 12, c, _kr(txt))


W, H = 920, 624
d = S(W, H, "CILIUM UP AND RUNNING · 07-02 §5", "헤더 필터가 바꾸는 요청과 응답",
      "요청 헤더는 백엔드로 가기 전에, 응답 헤더는 클라이언트로 가기 전에 더해진다", "요청 헤더는 백엔드로 가기 전에, 응답 헤더는 클라이언트로 가기 전에 더해진다")
A, B, C = "curl 클라이언트", "Gateway · Envoy", "echo-1"
d.lanes([(A, "172.18.255.200 호출"), (B, "HTTPRoute 필터"), (C, "port 8080")], [130, 460, 790])
d.rails(584)

d.msg(A, B, "GET /cilium-add-a-request-header", 188, MUTED, "ar")
d.state(B, "add my-cilium-header-name", 224, ACC)
d.msg(B, C, "My-Cilium-Header-Name", 270, ACC, "acc", sub="my-cilium-header-value")
d.msg(C, B, "echo 본문 · 받은 헤더", 330, MUTED, "ar", dash="5 4")
d.msg(B, A, "200 OK", 372, MUTED, "ar", dash="5 4")

d.msg(A, B, "GET /multiple", 430, MUTED, "ar")
d.msg(B, C, "GET /multiple", 468, MUTED, "ar")
d.msg(C, B, "200 OK", 506, MUTED, "ar", dash="5 4")
d.state(B, "add X-Header-Add-1 · 2", 536, OK)
d.msg(B, A, "x-header-add-1: header-add-1", 574, OK, "ok", dash="5 4", sub="x-header-add-2: header-add-2")
d.save("07-02.header-filter-sequence.svg")
