# 타입 스펙: type-sequence — 참여자 셋(요청 A · Redis · 요청 B), 메시지 여섯. 둘 다 3 을 읽고 둘 다 4 를 써서 카운터가 4 에 머문다. focal 은 요청 B 의 덮어쓰기.
# 사실 출처: 추출본 v2.txt 1213~1226행(읽기 → counter+1 비교 → 쓰기, 카운터 3 에서 두 요청이 4 를 쓰고 정답은 5).
#   원자 INCR 로 막는 방식은 Redis INCR 문서(https://redis.io/docs/latest/commands/incr/) Pattern: rate limiter.
# Layout conventions: 레인 폭 176·중심 x=120·480·840, 메시지 stride 56(y=196부터), 상태 칩 y=548·584, 레일 하단 H-80. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO


def _kr(t):
    return KR if any("가" <= c <= "힣" for c in str(t)) else MONO


def _w(t, size):
    return sum(size * (1.0 if "가" <= c <= "힣" else 0.62) for c in str(t)) + 12


class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]; dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.o.append(f'<rect x="{mx - _w(label, 12)/2}" y="{y - 23}" width="{_w(label, 12)}" height="18" fill="{PAPER}"/>')
        s.t(mx, y - 9, label, 12, c, _kr(label), "middle", 600)
        if sub:
            s.o.append(f'<rect x="{mx - _w(sub, 13)/2}" y="{y + 5}" width="{_w(sub, 13)}" height="20" fill="{PAPER}"/>')
            s.t(mx, y + 19, sub, 13, MUTED, _kr(sub))


W, H = 960, 688
d = SeqKR(W, H, "SYSTEM DESIGN INTERVIEW · 04-02 §4",
          "두 요청이 3 을 읽고 둘 다 4 를 쓰면 카운터는 4",
          "카운터가 3 일 때 요청 A 와 B 가 쓰기 전에 둘 다 읽으면 각자 3 + 1 = 4 를 써서, 두 건이 들어왔는데 정답 5 가 아닌 4 가 남는다.",
          "읽고 · 비교하고 · 쓰는 사이")

NAMES = (("요청 A", "서버 1"), ("Redis", "counter = 3"), ("요청 B", "서버 2"))
d.LX = {"요청 A": 120, "Redis": 480, "요청 B": 840}
for nm, sub in NAMES:
    x = d.LX[nm]
    d.box(x - 88, 100, 176, 44, PAPER2, RULE, 1.0)
    d.t(x, 120, nm, 13, INK, _kr(nm), "middle", 600)
    d.t(x, 137, sub, 12, MUTED, _kr(sub))
d.lane_top = 144
d.rails(H - 80)

A, R, B = "요청 A", "Redis", "요청 B"
d.msg(A, R, "GET counter", 196, INFO, "info")
d.msg(R, A, "= 3", 252, INFO, "info", dash="5 4")
d.msg(B, R, "GET counter", 308, WARN, "warn")
d.msg(R, B, "= 3", 364, WARN, "warn", dash="5 4")
d.msg(A, R, "SET counter 4", 420, INFO, "info", sub="3 + 1")
d.msg(B, R, "SET counter 4", 476, ACC, "acc", sub="3 + 1")
d.state(R, "counter = 4", 548, BAD)
d.state(R, "정답 5", 584, OK)

d.legend(H - 56, [("요청 A", INFO), ("요청 B", WARN), ("덮어쓴 쓰기", ACC), ("남은 값", BAD), ("정답", OK)])
d.save("04-02.race-lost-update.svg")
