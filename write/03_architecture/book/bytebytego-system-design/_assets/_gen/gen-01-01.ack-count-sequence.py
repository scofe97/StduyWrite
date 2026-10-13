# 타입 스펙: type-sequence — 한 번의 쓰기에 대해 세 노드 중 몇 개의 저장 확인을 받고 응답하느냐(1/3 · 2/3 · 3/3)에 따라 응답 시점이 세 번 갈린다.
# 사실 출처: 추출본 v1.txt 1673~1681행과 쪽 67 그림(옵션 1: 세 노드 모두 저장 후 성공 · 옵션 2: 주 노드와 보조 하나 · 옵션 3: 주 노드만. 옵션 2·3 은 결과적 일관성). 노드 이름은 그림의 Primary data node·Secondary data node 1·2.
# Layout conventions: 레인 4·폭 170, 메시지 stride 56(y=192부터 8개), 상태 칩은 주 노드 생명선 위, 응답 화살표 24px 아래. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, Seq, ACC, OK, WARN, INFO, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


class SeqKR(Seq):
    def lanes(s, names, y0=104, lane_w=210):
        s.LX = {}
        n = len(names)
        span = (s.w - 48 - 24) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            s.t(x, y0 + 20, nm, 13, INK, _kr(nm), "middle", 600)
            s.t(x, y0 + 37, sub, 12, MUTED, _kr(sub))
        s.lane_top = y0 + 44
        return s.LX

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None, lx=None):
        x1, x2 = s.LX[a], s.LX[b]
        d_ = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * d_} {y} L {x2 - 12 * d_} {y}", c, 1.5, m=mk, dash=dash)
        s.t(lx if lx is not None else (x1 + x2) / 2, y - 9, label, 12, c, _kr(label), "middle", 600)

    def state(s, a, txt, y, c, dx=0):
        x = s.LX[a] + dx
        w = len(txt) * (12 if any("가" <= ch <= "힣" for ch in txt) else 7.8) + 20
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 4, txt, 12, c, _kr(txt))


W, H = 920, 688
d = SeqKR(W, H, "BYTEBYTEGO · 01-01 §4",
          "저장 확인을 몇 개 기다리고 응답하는가",
          "같은 쓰기 하나에 응답 시점이 세 곳이며, 늦게 응답할수록 읽는 쪽이 최신 값을 볼 가능성이 커집니다",
          "확인 1/3 · 2/3 · 3/3")
SV, P, S1, S2 = "클라이언트", "주 노드", "보조 노드 1", "보조 노드 2"
d.lanes([(SV, "쓰기 요청"), (P, "primary"), (S1, "secondary 1"), (S2, "secondary 2")], 100, 170)
d.rails(H - 100)

Y0, S = 196, 56
steps = [
    (SV, P, "write", MUTED, "ar", None),
    (P, S1, "replicate", MUTED, "ar", None),
    (P, S2, "replicate", MUTED, "ar", None),
    (P, SV, "옵션 3 · 응답", WARN, "warn", "5 4"),
    (S1, P, "ack", MUTED, "ar", "5 4"),
    (P, SV, "옵션 2 · 응답", INFO, "info", "5 4"),
    (S2, P, "ack", MUTED, "ar", "5 4"),
    (P, SV, "옵션 1 · 응답", ACC, "acc", "5 4"),
]
for k, (a, b, label, c, mk, dash) in enumerate(steps):
    far = S2 in (a, b)
    d.msg(a, b, label, Y0 + k * S, c, mk, dash, lx=(d.LX[S1] + d.LX[S2]) / 2 if far else None)

# 확인 수 칩: 응답 화살표 24px 아래, 주 노드 생명선 위에 둔다
d.state(P, "확인 1/3", Y0 + 3 * S + 24, WARN, dx=-0)
d.state(P, "확인 2/3", Y0 + 5 * S + 24, INFO)
d.state(P, "확인 3/3", Y0 + 7 * S + 24, ACC)

d.legend(H - 44, [("옵션 3 · 지연 최저", WARN), ("옵션 2", INFO), ("옵션 1 · 지연 최고", ACC)])
d.save("01-01.ack-count-sequence.svg")
