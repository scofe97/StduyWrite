# 03-01 §3 — 3-way handshake. 원문 normal-connection.pcap 의 실제 시퀀스·윈도우 값만 쓴다.
# 타입 스펙: type-sequence — 주체 둘 사이의 시간순 메시지. 레인 옆 칩이 그 시점의 TCP 상태이고,
#           headline(accent)은 연결이 성립하는 마지막 ACK 하나.
#           프리미티브의 Seq.msg 가 한글 라벨을 MONO 로 하드코딩하므로 계약대로 서브클래스로 감싼다.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, INFO, PAPER, PAPER2, RULE, KR, MONO

def _kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]; dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 11, c, _kr(label), "middle", 600)
        if sub: s.t(mx, y + 17, sub, 11, MUTED, KR)

W, H = 920, 512
d = SeqKR(W, H, "PACKET ANALYSIS WITH WIRESHARK · 03-01 §3",
          "3-way handshake 의 실제 값",
          "normal-connection.pcap 의 세 패킷. 각 메시지 아래가 그 패킷이 실은 시퀀스·확인·윈도우 값이고, 레인 옆 칩이 그 시점의 상태다. 확인 번호는 언제나 상대 시퀀스 + 1 이다.",
          "ACK 번호가 상대 SEQ+1 인 것이 이 세 줄에서 두 번 반복됩니다")

d.lanes([("클라이언트", "122.167.84.137"), ("서버", "10.0.0.221")], y0=104, lane_w=280)
d.rails(408)

d.state("클라이언트", "CLOSED", 176, MUTED)
d.state("서버", "LISTEN", 176, MUTED)

d.msg("클라이언트", "서버", "SYN", 224, INFO, "info",
      sub="SEQ=3613047129 · WIN=65535 · SACK_PERM=1")
d.state("클라이언트", "SYN_SENT", 256, INFO)

d.msg("서버", "클라이언트", "SYN, ACK", 300, INFO, "info",
      sub="SEQ=2581725269 · ACK=3613047130 · WIN=26847")
d.state("서버", "SYN_RECEIVED", 332, INFO)

d.msg("클라이언트", "서버", "ACK", 376, ACC, "acc",
      sub="SEQ=3613047130 · ACK=2581725270 · WIN=4105")

d.state("클라이언트", "ESTABLISHED", 424, OK)
d.state("서버", "ESTABLISHED", 424, OK)

d.legend(452, [("연결 성립", ACC), ("성립 이전", INFO), ("성립 이후", OK)])
d.save("03-01.three-way-handshake.svg")
