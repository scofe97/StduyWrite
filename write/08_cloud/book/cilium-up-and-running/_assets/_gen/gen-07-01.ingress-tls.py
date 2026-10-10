# 타입 스펙: type-sequence — HTTPS 클라이언트가 mkcert demo-cert 로 TLS 핸드셰이크를 맺고 Envoy 가 복호화하여 백엔드 Pod 에 평문 HTTP 로 전달하는 시퀀스.
# 사실 출처: Cilium Up and Running 7장 cil7.txt 줄 391-404(mkcert *.cilium.rocks), 420-423(secret demo-cert), 433-462(tls-ingress.yaml), 470-472(172.18.255.201), 497-501(curl resolve cacert)
import sys
sys.path.insert(0, ".")
from dd import D, Seq, ACC, OK, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


class TlsSeq(Seq):
    def lanes(s, names, xs, y0=104, lane_w=176):
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
d = TlsSeq(W, H, "CILIUM UP AND RUNNING · 07-01 §3", "Cilium Ingress TLS 종단 시퀀스",
           "Envoy 가 클라이언트와 TLS 를 맺고 내부 백엔드로는 평문 HTTP 를 보낸다",
           "Secret 에 저장된 인증서로 외부 암호 통신을 끝내 백엔드의 인증서 부담을 던다")

P1, P2, P3, P4 = "curl 클라이언트", "LB 서비스 IP", "Envoy 프록시", "details 백엔드"
d.lanes([
    (P1, "mkcert CA 신뢰"),
    (P2, "172.18.255.201:443"),
    (P3, "Secret: demo-cert"),
    (P4, "9080 · 평문 HTTP")
], [116, 360, 600, 816], lane_w=168)

d.rails(540)

# 1. TLS 핸드셰이크
d.msg(P1, P2, "TLS Client Hello", 182, INFO, "info")
d.msg(P2, P3, "eBPF → TPROXY", 206, ACC, "acc")
d.state(P3, "SNI 로 인증서 선택", 232, ACC)
d.msg(P3, P1, "핸드셰이크 응답 · 인증서", 258, OK, "ok", dash="5 4")
d.state(P1, "CA 검증 완료", 284, OK)

# 2. 암호화된 HTTPS 요청 및 복호화
d.msg(P1, P2, "HTTPS 암호화 요청", 324, INFO, "info")
d.msg(P2, P3, "eBPF → TPROXY", 348, ACC, "acc")
d.state(P3, "TLS 복호화 (TLS 종단)", 374, OK)

# 3. 내부 백엔드로 평문 HTTP 전달 및 응답
d.msg(P3, P4, "평문 HTTP GET /details/1", 406, OK, "ok")
d.msg(P4, P3, "HTTP 200 (도서 JSON)", 436, OK, "ok", dash="5 4")

# 4. Envoy 가 암호화하여 응답 반환
d.state(P3, "TLS 암호화", 468, OK)
d.msg(P3, P1, "HTTPS 암호화 응답 (200 JSON)", 498, OK, "ok", dash="5 4")

d.save("07-01.ingress-tls.svg")
