# 타입 스펙: type-sequence — curl 클라이언트가 LB IP 로 요청을 보내고 Envoy 가 경로별 백엔드 서비스(/details, /, 미매핑)로 라우팅하는 시퀀스.
# 사실 출처: Cilium Up and Running 7장 cil7.txt 줄 139-156(basic-ingress paths), 250-252(172.18.255.200), 329-332(GET / -> 200), 336-347(GET /details/1 -> JSON), 357-358(GET /ratings -> 404)
import sys
sys.path.insert(0, ".")
from dd import D, Seq, ACC, OK, WARN, BAD, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


class IngressSeq(Seq):
    def lanes(s, names, xs, y0=104, lane_w=148):
        s.LX = {}
        for (nm, sub), x in zip(names, xs):
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 46, PAPER2, RULE, 1.0)
            s.t(x, y0 + 20, nm, 12, INK, _kr(nm), "middle", 600)
            s.t(x, y0 + 38, sub, 12, MUTED, _kr(sub))
        s.lane_top = y0 + 46

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        dr = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dr} {y} L {x2 - 12 * dr} {y}", c, 1.4, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 8, label, 12, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 17, sub, 12, MUTED, _kr(sub))

    def state(s, a, txt, y, c):
        x = s.LX[a]
        w = len(txt) * 7.6 + 20
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 11}" width="{w}" height="22" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 5, txt, 12, c, _kr(txt))


W, H = 920, 580
d = IngressSeq(W, H, "CILIUM UP AND RUNNING · 07-01 §2", "Cilium Ingress 경로 라우팅 시퀀스",
               "요청 경로(/, /details, /ratings)에 따른 Envoy 의 서비스 전달과 응답 코드",
               "eBPF 가 패킷을 Envoy 로 넘기고 Envoy 가 Ingress 규칙대로 백엔드를 고른다")

P1, P2, P3, P4, P5 = "curl 클라이언트", "LB 서비스 IP", "Envoy 프록시", "productpage", "details"
d.lanes([
    (P1, "외부 호스트"),
    (P2, "172.18.255.200"),
    (P3, "cilium-envoy"),
    (P4, "9080 · 메인 웹"),
    (P5, "9080 · 책 정보")
], [84, 260, 450, 650, 836], lane_w=140)

d.rails(540)

# 1. GET / -> productpage (200 OK)
d.msg(P1, P2, "GET /", 180, INFO, "info")
d.msg(P2, P3, "eBPF → TPROXY", 204, ACC, "acc")
d.state(P3, "경로 / 매칭", 228, ACC)
d.msg(P3, P4, "GET /", 252, OK, "ok")
d.msg(P4, P3, "200 OK", 276, OK, "ok", dash="5 4")
d.msg(P3, P1, "200 OK (웹 페이지)", 300, OK, "ok", dash="5 4")

# 2. GET /details/1 -> details (JSON 반환)
d.msg(P1, P2, "GET /details/1", 342, INFO, "info")
d.msg(P2, P3, "eBPF → TPROXY", 364, ACC, "acc")
d.state(P3, "경로 /details 매칭", 388, OK)
d.msg(P3, P5, "GET /details/1", 410, OK, "ok")
d.msg(P5, P3, "200 OK (JSON)", 434, OK, "ok", dash="5 4")
d.msg(P3, P1, "200 OK (도서 JSON)", 458, OK, "ok", dash="5 4")

# 3. GET /ratings -> 404 Not Found (미매핑 경로)
d.msg(P1, P2, "GET /ratings", 494, WARN, "warn")
d.msg(P2, P3, "eBPF → TPROXY", 516, ACC, "acc")
d.state(P3, "규칙 미정의", 536, BAD)
d.msg(P3, P1, "404 Not Found", 558, BAD, "bad", dash="5 4")

d.save("07-01.ingress-routing.svg")
