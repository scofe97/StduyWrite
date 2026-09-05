# 03-01 §5 — 연결 종료. 원문 normal-connection.pcap 의 packet#5·7·8·9 와 그 시퀀스 값만 쓴다.
# 서버가 먼저 FIN 을 보내는 경우이므로 서버가 능동 종료, 클라이언트가 수동 종료다.
# 타입 스펙: type-sequence — 주체 둘 사이의 시간순 메시지. 레인 옆 칩이 그 시점의 TCP 상태이고,
#           headline(accent)은 수동 종료 쪽이 갇힐 수 있는 구간의 시작 하나.
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

W, H = 920, 608
d = SeqKR(W, H, "PACKET ANALYSIS WITH WIRESHARK · 03-01 §5",
          "종료는 네 번 오갑니다",
          "normal-connection.pcap 의 packet#5·7·8·9. 서버가 먼저 FIN 을 보내 능동 종료가 되고, 클라이언트는 ACK 를 보낸 뒤 자기 FIN 을 보낼 때까지 CLOSE_WAIT 에 머무른다.",
          "가운데 구간이 애플리케이션의 몫입니다 — 여기서 소켓을 안 닫으면 CLOSE_WAIT 가 쌓입니다")

d.lanes([("클라이언트", "122.167.84.137"), ("서버", "10.0.0.221")], y0=104, lane_w=280)
d.rails(472)

d.state("클라이언트", "ESTABLISHED", 176, OK)
d.state("서버", "ESTABLISHED", 176, OK)

d.msg("서버", "클라이언트", "FIN, ACK", 224, INFO, "info", sub="packet#5 · SEQ=2581725299")
d.state("서버", "FIN_WAIT-1", 256, INFO)

d.msg("클라이언트", "서버", "ACK", 300, MUTED, "ar", sub="packet#7 · 서버 SEQ 를 확인합니다")
d.state("클라이언트", "CLOSE_WAIT", 332, ACC)
d.state("서버", "FIN_WAIT-2", 332, INFO)

d.selfmsg("클라이언트", "socket.close()", 380, ACC,
          sub="여기가 애플리케이션의 몫 — 안 부르면 갇힙니다")

d.msg("클라이언트", "서버", "FIN, ACK", 428, MUTED, "ar", sub="packet#8 · SEQ=3613047130")
d.msg("서버", "클라이언트", "ACK", 472, MUTED, "ar", sub="packet#9 · 클라이언트 SEQ 를 확인합니다")

d.state("클라이언트", "LAST_ACK → CLOSED", 512, OK)
d.state("서버", "TIME_WAIT", 512, INFO)

d.legend(H - 64, [("애플리케이션이 닫아야 하는 구간", ACC), ("능동 종료 쪽 상태", INFO), ("정상 상태", OK)])
d.save("03-01.close-sequence.svg")
