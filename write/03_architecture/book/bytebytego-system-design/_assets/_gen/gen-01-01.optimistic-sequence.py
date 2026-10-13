# 타입 스펙: type-sequence — 두 사용자가 version=1 인 같은 행을 읽고 한쪽만 version=2 로 갱신되며, 실패한 쪽이 다시 읽어 version=3 으로 갱신하는 왕복.
# 사실 출처: 추출본 v1.txt 1623~1670행(version 열 추가 · 읽은 version 보다 1 큰 값 검증 · 검증 실패 시 다시 읽음 · 객실 예약 예시), 낙관적 잠금 설명 그림 쪽 66.
#   Jakarta Persistence 3.2 `@Version` 문서(갱신 시 버전 불일치를 낙관적 잠금 실패로 판정). available=5·4·3 은 예시 값.
# Layout conventions: 레인 3·폭 200, 호출·반환 한 쌍의 stride 72(호출 y, 반환 y+28), 쌍 6개, 첫 쌍 y=196. 모든 좌표 4의 배수.
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

    def state(s, a, txt, y, c, dx=0):
        x = s.LX[a] + dx
        w = len(txt) * (12 if any("가" <= ch <= "힣" for ch in txt) else 7.8) + 20
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 4, txt, 12, c, _kr(txt))


W, H = 880, 700
d = SeqKR(W, H, "BYTEBYTEGO · 01-01 §3",
          "version 열이 두 번째 갱신을 거절한다",
          "두 사용자가 version=1 을 읽고 UPDATE 를 보내면 먼저 도착한 쪽만 1 row 를 바꿉니다",
          "객실 수 5 → 4 → 3 · version 1 → 2 → 3")
U1, DB, U2 = "사용자 1", "room 테이블", "사용자 2"
LX = d.lanes([(U1, "먼저 UPDATE"), (DB, "id = 7"), (U2, "다시 읽고 UPDATE")], 100, 200)
d.rails(H - 80)

Y0, S = 200, 72
pairs = [
    (U1, "SELECT", "available=5 · version=1", MUTED, MUTED),
    (U2, "SELECT", "available=5 · version=1", MUTED, MUTED),
    (U1, "UPDATE version=2 WHERE version=1", "1 row", OK, OK),
    (U2, "UPDATE version=2 WHERE version=1", "0 rows", ACC, BAD),
    (U2, "SELECT", "available=4 · version=2", MUTED, MUTED),
    (U2, "UPDATE version=3 WHERE version=2", "1 row", OK, OK),
]
for k, (u, call, ret, cc, rc) in enumerate(pairs):
    y = Y0 + k * S
    d.msg(u, DB, call, y, cc, "acc" if cc == ACC else ("ok" if cc == OK else "ar"))
    d.msg(DB, u, ret, y + 28, rc, "bad" if rc == BAD else ("ok" if rc == OK else "ar"), dash="5 4")

# DB 레인 옆 상태 칩
d.state(DB, "version=2", Y0 + 2 * S + 52, OK, dx=-100)
d.state(DB, "version=3", Y0 + 5 * S + 52, OK, dx=-100)

d.legend(H - 56, [("갱신됨", OK), ("거절됨", BAD), ("거절당한 UPDATE", ACC)])
d.save("01-01.optimistic-sequence.svg")
