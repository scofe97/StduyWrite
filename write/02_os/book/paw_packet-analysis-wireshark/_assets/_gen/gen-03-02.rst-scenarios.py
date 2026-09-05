# 03-02 §1 — RST 가 나오는 두 자리. 원문의 RST-02(서버 미기동)와 RST-01(SYN-ACK 뒤 RST)을
# 같은 레인 위에 위아래로 쌓아 대조한다.
# 타입 스펙: type-sequence — 주체 둘 사이의 시간순 메시지. 두 시나리오를 구분선으로 나눠 쌓고,
#           headline(bad)은 각 시나리오에서 연결을 끊는 RST 다.
#           프리미티브의 Seq.msg 가 한글 라벨을 MONO 로 하드코딩하므로 계약대로 서브클래스로 감싼다.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO

def _kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]; dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 11, c, _kr(label), "middle", 600)
        if sub: s.t(mx, y + 17, sub, 11, MUTED, KR)

W, H = 920, 632
d = SeqKR(W, H, "PACKET ANALYSIS WITH WIRESHARK · 03-02 §1",
          "RST 가 나오는 두 자리",
          "위는 서버가 떠 있지 않아 첫 SYN 에 바로 RST 가 돌아오는 흔한 경우이고, 아래는 handshake 두 번이 끝난 뒤 ACK 대신 RST 가 오는 비정상 경우다. 어느 위치에서 끊겼는지가 원인을 가른다.",
          "몇 번째 패킷에서 RST 가 나왔는지가 원인 후보를 좁힙니다")

d.lanes([("클라이언트", "connect()"), ("서버", "LISTEN 여부")], y0=104, lane_w=280)
d.rails(516)

# 시나리오 A — 서버 미기동
d.t(24, 184, "A · 서버가 떠 있지 않음", 12, SOFT, KR, "start", 600)
d.t(24, 202, "원문 RST-02-ServerSocketCLOSED.pcap", 11, MUTED, MONO, "start")
d.msg("클라이언트", "서버", "SYN", 236, INFO, "info", sub="연결을 시도합니다")
d.msg("서버", "클라이언트", "RST, ACK", 288, BAD, "bad", sub="포트에 LISTEN 이 없어 거부됩니다")
d.state("클라이언트", "connection refused", 328, BAD)

d.line(24, 364, W - 48, 364, RULE, 0.8, "4 6")

# 시나리오 B — handshake 뒤 RST
d.t(24, 396, "B · handshake 뒤에 RST", 12, SOFT, KR, "start", 600)
d.t(24, 414, "원문 RST-01.pcap · 정상적으로 보여선 안 되는 패킷", 11, MUTED, MONO, "start")
d.msg("클라이언트", "서버", "SYN", 448, INFO, "info")
d.msg("서버", "클라이언트", "SYN, ACK", 484, INFO, "info")
d.msg("클라이언트", "서버", "RST", 516, BAD, "bad", sub="ACK 가 와야 할 자리입니다")

d.legend(H - 56, [("연결을 끊는 패킷", BAD), ("정상 handshake 패킷", INFO)])
d.save("03-02.rst-scenarios.svg")
