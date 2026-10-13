# 타입 스펙: type-sequence — 같은 주문 1001 이 오케스트레이션에서는 모든 호출과 응답이 오케스트레이터를 지나고 코레오그래피에서는 서비스끼리 직접 이어지는 두 판을 위아래로 쌓는다.
# 사실 출처: 추출본 v1.txt 1014~1055행과 쪽 38 그림(오케스트레이터가 서비스를 invoke·reply 로 부르는 중앙 조율 구조, 코레오그래피는 서비스끼리 point-to-point). 서비스 이름·주문 번호 1001 은 본문 예시 값이고 두 판의 메시지 개수는 우열을 뜻하지 않는다.
# Layout conventions: 레인 4·폭 180, 호출·반환 stride 28, 첫 판 첫 호출 y=188, 둘째 판 첫 호출 y=468. 모든 좌표 4의 배수.
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

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        d_ = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * d_} {y} L {x2 - 12 * d_} {y}", c, 1.5, m=mk, dash=dash)
        s.t((x1 + x2) / 2, y - 9, label, 12, c, _kr(label), "middle", 600)


W, H = 880, 640
d = SeqKR(W, H, "BYTEBYTEGO · 05-01 §5",
          "조율자를 지나는 호출과 서비스끼리 직접 잇는 호출",
          "조율자가 모든 호출과 응답을 받는 판과 서비스가 다음 서비스를 직접 부르는 판입니다",
          "서비스 이름과 주문 번호 1001 은 예시 값입니다")

# 판 1 — 오케스트레이션
d.t(24, 104, "오케스트레이션", 13, ACC, KR, "start", 600)
OR, PY, ST, SH = "오케스트레이터", "결제", "재고", "배송"
d.lanes([(OR, "조율"), (PY, "서비스"), (ST, "서비스"), (SH, "서비스")], 112, 180)
d.rails(344)
Y = 188
d.msg(OR, PY, "charge 1001", Y, MUTED, "ar")
d.msg(PY, OR, "paid", Y + 28, OK, "ok", dash="5 4")
d.msg(OR, ST, "reserve 1001", Y + 56, MUTED, "ar")
d.msg(ST, OR, "reserved", Y + 84, OK, "ok", dash="5 4")
d.msg(OR, SH, "ship 1001", Y + 112, MUTED, "ar")
d.msg(SH, OR, "shipped", Y + 140, OK, "ok", dash="5 4")

# 판 2 — 코레오그래피
d.t(24, 376, "코레오그래피", 13, INFO, KR, "start", 600)
OD = "주문"
d.lanes([(OD, "서비스"), (PY, "서비스"), (ST, "서비스"), (SH, "서비스")], 384, 180)
d.rails(568)
Y = 468
d.msg(OD, PY, "charge 1001", Y, INFO, "info")
d.msg(PY, ST, "reserve 1001", Y + 28, INFO, "info")
d.msg(ST, SH, "ship 1001", Y + 56, INFO, "info")
d.msg(SH, OD, "shipped 1001", Y + 84, INFO, "info")

d.legend(H - 56, [("호출", MUTED), ("응답", OK), ("서비스끼리 호출", INFO)])
d.save("05-01.orchestration-sequence.svg")
