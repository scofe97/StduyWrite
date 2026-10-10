# 타입 스펙: type-sequence — HTTP 규칙 정책 아래서 curl 요청이 Envoy 를 거치며 http-request·http-response 흐름 기록이 남는 순서. 레인은 구성요소, 메시지는 요청·응답 한 번의 이동.
# 사실 출처: Cilium Up and Running 15장 cil15.txt 줄 593-616(http-visibility 정책: 80/TCP 를 Envoy 로), 623-637(http-request·http-response 출력, 200 229ms, ID:6576, 57222)
import sys
sys.path.insert(0, ".")
from dd import D, Seq, ACC, INFO, OK, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


class SeqKR(Seq):
    def lanes(s, names, xs, y0=104, lane_w=196):
        s.LX = {}
        for (nm, sub), x in zip(names, xs):
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            s.t(x, y0 + 20, nm, 12, INK, MONO, "middle", 600)
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

    def rec(s, a, txt, sub, y, c):
        x = s.LX[a]
        w = len(txt) * 7.4 + 24
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 11}" width="{w}" height="22" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 4, txt, 12, c, MONO, "middle", 600)
        s.t(x, y + 26, sub, 12, MUTED, MONO)


W, H = 920, 580
d = SeqKR(W, H, "CILIUM UP AND RUNNING · 15-01 §4", "HTTP 규칙 아래 요청이 남기는 흐름 기록",
          "curl 요청이 Envoy 를 거치며 요청과 응답이 각각 L7 흐름으로 기록된다", "curl 요청이 Envoy 를 거치며 요청과 응답이 각각 L7 흐름으로 기록된다")
A, B, C = "tmp-shell", "Envoy", "example.com"
d.lanes([(A, "l7-visibility · ID:6576"), (B, "80/TCP 를 넘겨받음"), (C, "world · :80")], [150, 460, 770])
d.rails(548)

d.msg(A, B, "GET http://example.com/", 188, MUTED, "ar", sub=":57222 → :80")
d.rec(B, "http-request FORWARDED", "HTTP/1.1 GET http://example.com/", 250, ACC)
d.msg(B, C, "요청 전달", 340, MUTED, "ar")
d.msg(C, B, "응답 200", 392, MUTED, "ar", dash="5 4")
d.rec(B, "http-response FORWARDED", "HTTP/1.1 200 229ms (GET http://example.com/)", 450, INFO)
d.msg(B, A, "응답 전달", 520, MUTED, "ar", dash="5 4")
d.save("15-01.l7-visibility-sequence.svg")
