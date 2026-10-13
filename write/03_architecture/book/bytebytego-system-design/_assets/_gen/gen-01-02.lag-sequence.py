# 타입 스펙: type-sequence — 주 DB 에 쓴 직후 복제본을 읽으면 주문이 없고, 복제가 도착한 뒤 읽으면 있는 왕복.
# 사실 출처: 추출본 v1.txt 2607~2650행과 쪽 105 그림(Order Service 가 주 DB 에 쓰고 복제본에서 읽음, 복제는 비동기로 뒤처질 수 있음 "seconds or even minutes behind", 읽기 직후 주문이 안 보임). 주문 번호 1001 · 0 rows · 1 row 는 예시 값.
# Layout conventions: 레인 3·폭 200, 호출·반환 한 쌍의 stride 72(호출 y, 반환 y+28), 첫 쌍 y=200. 모든 좌표 4의 배수.
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
        lo, hi = sorted((x1, x2))
        mids = [x for x in s.LX.values() if lo + 40 < x < hi - 40]
        if mids:
            # 중간 레인 레일이 라벨을 가르지 않게 출발 쪽 구간의 가운데에 단다
            near = min(mids, key=lambda x: abs(x - x1))
            lx = (x1 + near) / 2
        else:
            lx = (x1 + x2) / 2
        s.t(lx, y - 9, label, 12, c, _kr(label), "middle", 600)

    def state(s, a, txt, y, c, dx=0):
        x = s.LX[a] + dx
        w = len(txt) * (12 if any("가" <= ch <= "힣" for ch in txt) else 7.8) + 20
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" fill="{PAPER}"/>')
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 4, txt, 12, c, _kr(txt))


W, H = 880, 576
d = SeqKR(W, H, "BYTEBYTEGO · 01-02 §3",
          "쓴 직후 복제본을 읽으면 주문이 보이지 않는다",
          "복제가 복제본에 닿기 전의 읽기는 0 rows 이고, 닿은 뒤의 읽기는 1 row 입니다",
          "주문 번호 1001 은 예시 값입니다")
SV, PR, RP = "주문 서비스", "주 DB", "복제본"
LX = d.lanes([(SV, "읽기·쓰기 요청"), (PR, "쓰기"), (RP, "읽기")], 100, 200)
d.rails(H - 80)

Y0, S = 200, 72
d.msg(SV, PR, "INSERT order 1001", Y0, MUTED, "ar")
d.msg(PR, SV, "OK", Y0 + 28, OK, "ok", dash="5 4")
d.msg(SV, RP, "SELECT id=1001", Y0 + S, MUTED, "ar")
d.msg(RP, SV, "0 rows", Y0 + S + 28, BAD, "bad", dash="5 4")
d.msg(PR, RP, "복제 · 주문 1001", Y0 + 2 * S + 8, ACC, "acc")
d.msg(SV, RP, "SELECT id=1001", Y0 + 3 * S, MUTED, "ar")
d.msg(RP, SV, "1 row", Y0 + 3 * S + 28, OK, "ok", dash="5 4")

d.state(RP, "1001 없음", Y0 + S + 54, BAD, dx=0)
d.state(RP, "1001 있음", Y0 + 2 * S + 40, OK, dx=0)

d.legend(H - 56, [("응답 · 반영됨", OK), ("읽었는데 없음", BAD), ("복제 도착", ACC)])
d.save("01-02.lag-sequence.svg")
