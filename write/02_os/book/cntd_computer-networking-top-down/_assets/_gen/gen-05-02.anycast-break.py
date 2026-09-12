# 05-02 §5 — 애니캐스트가 상태 있는 서비스에서 깨지는 장면.
# 원문 5.4.3: "with IP anycast ... the packets from the same TCP connection may be routed to
#       different web server instances" — CDN 이 애니캐스트를 대체로 쓰지 않는 이유.
# 노트의 읽기: 주소 203.0.113.9 는 문서용 대역(RFC 5737)에서 고른 예시다. 원문은 인스턴스가
#       갈린다는 사실만 적고 RST 까지는 적지 않는다 — RST 는 03-04 의 규칙을 이어 붙인 것이다.
# 타입 스펙: type-sequence — 참여자 레인 + 시간축. 경로가 바뀌는 순간의 앞뒤를 한 축에 놓는다.
#       축약: 3방향 핸드셰이크는 03-04 의 몫이라 SYN 한 줄로 줄였다.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, WARN, BAD, RULE, PAPER, KR, MONO


def _kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO


class SeqKR(Seq):
    def lanes(s, names, y0=104, lane_w=210):
        s.LX = {}; n = len(names)
        span = (s.w - 48 - 24) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 44, "#161B22", RULE, 1.0)
            s.t(x, y0 + 20, nm, 12, INK, KR, "middle", 600)
            s.t(x, y0 + 37, sub, 12, MUTED, _kr(sub))
        s.lane_top = y0 + 44
        return s.LX

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None, lx=0):
        x1, x2 = s.LX[a], s.LX[b]; dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2 + lx
        s.t(mx, y - 9, label, 13, c, _kr(label), "middle", 600)
        if sub: s.t(mx, y + 17, sub, 12, MUTED, KR)

    def selfmsg(s, a, label, y, c=MUTED, sub=None):
        x = s.LX[a]
        s.path(f"M {x + 10} {y - 10} L {x + 58} {y - 10} L {x + 58} {y + 10} L {x + 13} {y + 10}", c, 1.4, m="ar")
        s.t(x + 68, y - 4, label, 13, c, _kr(label), "start", 600)
        if sub: s.t(x + 68, y + 14, sub, 12, MUTED, KR, "start")

    def state(s, a, txt, y, c):
        x = s.LX[a]
        w = sum(12.0 if "가" <= ch <= "힣" else 7.6 for ch in txt) + 18
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 4, txt, 12, c, _kr(txt))


W, H = 1000, 700
d = SeqKR(W, H, "COMPUTER NETWORKING TOP-DOWN · 05-02 §5",
          "경로가 바뀌면 연결이 깨집니다",
          "같은 주소를 도쿄와 LA 두 인스턴스가 광고하는 동안 BGP 가 더 나은 경로로 갈아타면, "
          "같은 TCP 연결의 다음 세그먼트가 상태를 갖지 않은 서버에 도착해 리셋된다.",
          "주소는 하나인데 그 주소를 가진 기계가 바뀝니다")

U, R, T, L = "사용자", "경로 위 라우터", "도쿄 인스턴스", "LA 인스턴스"
d.lanes([(U, "198.51.100.7"), (R, "BGP 가 고른 길"), (T, "203.0.113.9"), (L, "203.0.113.9")],
        y0=104, lane_w=204)
d.rails(580)

d.msg(U, R, "SYN  → 203.0.113.9:443", 196, MUTED, sub="목적지 주소는 끝까지 하나입니다")
d.msg(R, T, "지금 최선인 경로로", 248, MUTED)
d.state(T, "이 연결의 상태를 갖습니다", 288, OK)

d.selfmsg(R, "BGP 갱신 — LA 광고가 이깁니다", 348, WARN,
          sub="같은 접두어의 광고 여럿 중 하나를 다시 고릅니다")

d.msg(U, R, "같은 연결의 다음 세그먼트", 420, MUTED, sub="사용자 쪽은 아무것도 바뀌지 않았습니다")
d.msg(R, L, "바뀐 경로로", 472, WARN, mk="warn")
d.state(L, "이 4튜플을 모릅니다", 512, BAD)

d.msg(L, U, "RST", 560, ACC, mk="acc", lx=-40)

d.t(20, 612, "연결은 양 끝 호스트의 메모리에만 있습니다(03-03 §1). LA 서버는 그 메모리를 나눠 갖지 않습니다.",
    13, MUTED, KR, "start")
d.t(20, 634, "그래서 맞는 소켓이 없는 세그먼트에 03-04 의 규칙대로 리셋을 돌려줍니다. 질의 하나로 끝나는 DNS 는 이 장면을 만나지 않습니다.",
    13, MUTED, KR, "start")

d.legend(H - 44, [("상태를 가진 쪽", OK), ("경로가 바뀝니다", WARN),
                  ("상태가 없는 쪽", BAD), ("연결이 깨집니다", ACC)])
d.save("05-02.anycast-break.svg")
print("ok 05-02.anycast-break")
