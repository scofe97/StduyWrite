# 03-04 §2 — 세우기부터 허물기까지 양쪽 호스트의 상태를 한 흐름에 놓는다. 클라이언트가 능동 열기·먼저 닫기를 맡는 경우다.
# 상태 이름과 뜻은 RFC 9293 §3.3.2, 클라이언트 쪽 순서는 원문 Figure 3.39 와 같다. 서버 쪽은 RFC 의 상태도를 따른다.
# 본문 근거(§2 「양쪽 상태를 한 흐름에 놓으면」): SYN → SYN_SENT/SYN_RCVD, SYNACK → 클라이언트 ESTABLISHED, ACK → 서버 ESTABLISHED,
#   FIN → FIN_WAIT_1/CLOSE_WAIT, ACK → FIN_WAIT_2, FIN → LAST_ACK, ACK → TIME_WAIT/CLOSED, 2×MSL 뒤 CLOSED.
# 타입 스펙: type-sequence — 참여자 레인 + 시간축 왕복. 상태는 레인 옆 칩으로.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, WARN, INFO, RULE, KR, MONO

def _kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None, subc=None):
        x1, x2 = s.LX[a], s.LX[b]; dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 11, c, _kr(label), "middle", 600)
        if sub: s.t(mx, y + 17, sub, 11, subc or MUTED, KR)

W, H = 1000, 860
d = SeqKR(W, H, "COMPUTER NETWORKING TOP-DOWN · 03-04 §2",
          "양쪽 상태를 한 흐름에 놓으면",
          "클라이언트가 능동 열기와 먼저 닫기를 맡는 경우. 세 번 교환해 세우고 네 번 교환해 허물며, 세그먼트 하나가 오갈 때마다 어느 한쪽의 상태가 바뀐다.",
          "칩이 그 시점의 상태입니다. TIME_WAIT 는 먼저 닫은 쪽에만 생깁니다")

C, S_ = "클라이언트", "서버"
d.lanes([(C, "능동 열기 · 먼저 닫음"), (S_, "수동 열기 · 나중에 닫음")], y0=104, lane_w=230)
d.rails(732)

d.state(C, "CLOSED", 172, MUTED)
d.state(S_, "LISTEN", 172, INFO)

d.state(C, "SYN_SENT", 206, INFO)
d.msg(C, S_, "SYN  seq=client_isn", 236, INFO, mk="info")
d.state(S_, "SYN_RCVD", 266, INFO)

d.msg(S_, C, "SYNACK  seq=server_isn  ack=client_isn+1", 302, INFO, mk="info")
d.state(C, "ESTABLISHED", 332, OK)

d.msg(C, S_, "ACK  ack=server_isn+1", 366, INFO, mk="info", sub="이 세그먼트부터 데이터를 실을 수 있음")
d.state(S_, "ESTABLISHED", 410, OK)

d.t((d.LX[C] + d.LX[S_]) / 2, 452, "… 데이터 교환 …", 11, OK, KR, "middle", 600)

d.state(C, "FIN_WAIT_1", 488, WARN)
d.msg(C, S_, "FIN", 518, WARN, mk="warn")
d.state(S_, "CLOSE_WAIT", 548, WARN)

d.msg(S_, C, "ACK", 582, WARN, mk="warn", sub="서버 애플리케이션이 close() 할 때까지 CLOSE_WAIT 에 머뭄")
d.state(C, "FIN_WAIT_2", 626, WARN)

d.msg(S_, C, "FIN", 660, WARN, mk="warn")
d.state(S_, "LAST_ACK", 690, WARN)
d.state(C, "TIME_WAIT", 690, ACC)

d.msg(C, S_, "ACK", 722, ACC, mk="acc")
d.state(S_, "CLOSED", 752, MUTED)
d.state(C, "CLOSED", 752, MUTED)
d.t(d.LX[C] + 78, 756, "2×MSL 뒤", 11, ACC, KR, "start")

d.legend(H - 44, [("세우는 동안", INFO), ("데이터 교환", OK), ("허무는 동안", WARN), ("TIME_WAIT — 먼저 닫은 쪽만", ACC)])
d.save("03-04.tcp-states-both.svg")
print("ok tcp-states-both")
