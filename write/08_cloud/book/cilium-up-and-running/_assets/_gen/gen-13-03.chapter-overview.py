# 타입 스펙: type-sequence — HTTPS 요청 하나가 Pod → 노드 Envoy(TLS 종료·L7 규칙 판정) → 업스트림(새 TLS) → 응답으로 오가는 시퀀스.
# 사실 출처: Cilium Up and Running 13장 cil13.txt 줄 1085-1156(internal-ca-bundle 마운트), 1158-1224(terminatingTLS·originatingTLS 정책, curl 200 OK), 948-1004(public-ca-bundle), 1057-1081(cilium-io-cert) / docs.cilium.io v1.20 security/tls-visibility
import sys
sys.path.insert(0, ".")
from dd import Seq, ACC, OK, INFO, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


class SeqKR(Seq):
    """한글 라벨은 한글 스택으로, 제품·명령 값은 mono 로 내보내는 Seq."""
    def lanes(s, names, xs, y0=104, lane_w=196):
        s.LX = {}
        for (nm, sub), x in zip(names, xs):
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            s.t(x, y0 + 20, nm, 12, INK, _kr(nm), "middle", 600)
            s.t(x, y0 + 37, sub, 12, MUTED, _kr(sub))
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
        w = len(txt) * 7.4 + 20
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" fill="{PAPER}"/>')
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 4, txt, 12, c, _kr(txt))


W, H = 920, 580
d = SeqKR(W, H, "CILIUM UP AND RUNNING · 13-03", "HTTPS 요청이 Envoy 에서 끊겼다 다시 맺어지는 흐름",
          "Pod 는 내부 CA 가 서명한 인증서로 Envoy 와 TLS 를 맺고, Envoy 는 공개 CA 로 검증하는 새 TLS 로 업스트림에 간다",
          "Pod 는 내부 CA 가 서명한 인증서로 Envoy 와 TLS 를 맺고, Envoy 는 공개 CA 로 검증하는 새 TLS 로 업스트림에 간다")

A, B, C = "클라이언트 Pod", "노드 Envoy", "업스트림 서버"
d.lanes([(A, "test · netshoot"), (B, "노드마다 하나"), (C, "cilium.io:443")],
        [150, 460, 770])
d.rails(548)

d.msg(A, B, "HTTPS 요청 시작", 176, MUTED, "ar", sub="curl -sI https://cilium.io/blog/")
d.msg(B, A, "서버 인증서 제시", 224, ACC, "acc", sub="cilium-io-cert · 서명 internal-ca")
d.state(A, "ca-certificates.crt 로 검증 통과", 268, OK)
d.msg(A, B, "HEAD /blog/", 316, MUTED, "ar", sub="TLS 안쪽 HTTP 요청")
d.state(B, "path /blog/.* 일치", 360, ACC)
d.msg(B, C, "새 TLS 연결 후 전달", 408, INFO, "info", sub="public-ca-bundle 로 서버 검증")
d.msg(C, B, "HTTP 응답", 456, MUTED, "ar", dash="5 4", sub="업스트림 TLS 세션")
d.msg(B, A, "HTTP/1.1 200 OK", 504, OK, "ok", dash="5 4", sub="클라이언트 TLS 세션")

d.save("13-03.chapter-overview.svg")
