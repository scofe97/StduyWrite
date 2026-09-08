# 03-01 §4 — 첫 SYN 만 듣는 소켓으로 간다. 그 뒤의 세그먼트는 연결된 소켓으로 곧장 간다.
# 원문 3.2: "the Web server has a different socket for each connection" · 최초 연결 요청 세그먼트만
#       환영 소켓으로 가고, 그 뒤로 만들어진 연결 소켓이 4튜플로 식별된다.
#   accept(2): "extracts the first connection request on the queue of pending connections for the
#       listening socket, sockfd, creates a new connected socket ... The original socket sockfd is
#       unaffected by this call."
# 노트의 읽기: 2026-09-08 학습자가 "22번 포트는 하나인데 여러 세션이 어떻게 붙나, 서버 포트는
#       누가 할당하나" 라고 물어 추가한 도식. 같은 절의 03-01.listen-vs-connected 는 연결이 다
#       맺어진 뒤의 *정적 모양* 이고, 이 도식은 같은 소켓들을 *시간 순서* 로 본다 — 커널이 4튜플로
#       연결된 소켓을 먼저 찾고 없을 때만 듣는 소켓으로 보내는 갈림길.
# 타입 스펙: type-sequence — 참여자 레인 + 시간축. 연결마다 한 번인 구간은 LOOP 프래그먼트로 묶고,
#       헤드라인(강조색)은 "듣는 소켓을 거치지 않고 곧장 간다" 하나뿐이다.
#       축약: SYN 뒤의 SYN-ACK·ACK 두 세그먼트는 03-04 의 몫이라 그리지 않는다. 클라이언트 B 는
#       레인을 늘리지 않고 LOOP 가 한 번 더 돈다는 산문으로 대신한다.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, INFO, RULE, PAPER, KR, MONO

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
    def fragment(s, op, guard, x, y, w, h):
        # type-sequence 의 combined fragment. 다크 스킨 값은 스펙 "Dark mode" 줄 그대로.
        s.box(x, y, w, h, "rgba(245,245,245,0.04)", "rgba(245,245,245,0.22)", 1.0, 4)
        s.box(x, y, 40, 16, PAPER, "rgba(245,245,245,0.22)", 1.0, 2)
        s.t(x + 20, y + 12, op, 8, SOFT, MONO)
        # 가드는 탭 오른쪽 같은 줄에 둔다 — 탭 아래(x+12)에 두면 첫 생명선(x=129)이 글자를 관통한다.
        s.t(x + 72, y + 12, guard, 12, SOFT, KR, "start")

W, H = 1000, 684
d = SeqKR(W, H, "COMPUTER NETWORKING TOP-DOWN · 03-01 §4",
          "첫 SYN 만 듣는 소켓으로 갑니다",
          "커널은 도착한 세그먼트의 4튜플로 연결된 소켓을 먼저 찾고, 없을 때만 듣는 소켓으로 보낸다. "
          "그 일은 연결마다 첫 SYN 한 번뿐이다.",
          "체인이 아니라 갈림길입니다")

A, K, L, C = "클라이언트 A", "서버 커널", "듣는 소켓", "연결된 소켓 A"
d.lanes([(A, "1.1.1.1"), (K, "4튜플로 먼저 찾는다"), (L, "*:80 LISTEN"), (C, "accept() 가 만든다")],
        y0=104, lane_w=210)
d.rails(564)

# ── 연결마다 한 번 — LOOP 프래그먼트 ─────────────────────────
FX, FY, FW, FH = 72, 176, 864, 268
d.fragment("LOOP", "[연결마다 한 번]", FX, FY, FW, FH)

d.selfmsg(A, "connect()", 240, MUTED, sub="출발지 포트는 OS 가 고릅니다")
d.msg(A, K, "SYN  1.1.1.1:26145 → *:80", 292, MUTED, sub="맞는 4튜플이 없습니다")
d.msg(K, L, "듣는 소켓으로", 344, INFO, mk="info", sub="목적지 두 값만으로 찾습니다")
d.msg(L, C, "accept()", 396, OK, mk="ok", sub="SYN 의 출발지로 채운 새 소켓")
d.state(L, "여전히 *:80 LISTEN", 428, INFO)
d.state(C, "1.1.1.1:26145 → *:80", 428, OK)

# ── 그 뒤의 모든 세그먼트 ─────────────────────────────────
d.msg(A, K, "데이터  1.1.1.1:26145 → *:80", 492, MUTED, sub="연결된 소켓 A 와 일치")
d.msg(K, C, "곧장 연결된 소켓으로", 544, ACC, mk="acc", sub="듣는 소켓은 거치지 않습니다", lx=92)

d.t(20, 592, "클라이언트 B 가 오면 LOOP 가 한 번 더 돌아 fd=7 이 생기고, 그 뒤 B 의 세그먼트도 자기 소켓으로 곧장 갑니다.",
    12, MUTED, KR, "start")
d.t(20, 612, "SYN 뒤의 SYN-ACK 과 ACK 은 03-04 의 몫이라 여기서는 생략했습니다.",
    12, MUTED, KR, "start")

d.legend(H - 44, [("연결마다 한 번뿐인 길", INFO), ("accept() 가 만든 소켓", OK), ("그 뒤 모든 세그먼트의 길", ACC)])
d.save("03-01.first-syn-only.svg")
print("ok 03-01.first-syn-only")
