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
    def state(s, a, txt, y, c):
        # 레일 점선이 반투명 칩의 글자를 관통하지 않게, 같은 자리에 불투명 바탕을 먼저 깐다
        x = s.LX[a]; w = len(txt) * 7.0 + 18
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" fill="{PAPER}"/>')
        super().state(a, txt, y, c)

W, H = 920, 636
d = SeqKR(W, H, "PACKET ANALYSIS WITH WIRESHARK · 03-01 §5",
          "종료는 네 번 오갑니다",
          "normal-connection.pcap 의 packet#5·7·8·9. 서버가 먼저 FIN 을 보내 능동 종료가 되고, 클라이언트는 #7 로 ACK 를 보낸 뒤 애플리케이션이 close() 를 불러 #8 이 나갈 때까지 CLOSE_WAIT 에 머무른다. 번호는 모두 원문 종료 절의 패킷 목록 스크린샷에 찍힌 값이다.",
          "가운데 구간이 애플리케이션의 몫입니다 — 여기서 소켓을 안 닫으면 CLOSE_WAIT 가 쌓입니다")

d.lanes([("클라이언트", "122.167.84.137"), ("서버", "10.0.0.221")], y0=104, lane_w=280)
d.rails(524)

d.state("클라이언트", "ESTABLISHED", 176, OK)
d.state("서버", "ESTABLISHED", 176, OK)

d.msg("서버", "클라이언트", "FIN, ACK", 224, INFO, "info", sub="packet#5 · SEQ=2581725299 · ACK=3613047130")
d.state("서버", "FIN_WAIT-1", 256, INFO)

d.msg("클라이언트", "서버", "ACK", 300, MUTED, "ar", sub="packet#7 · SEQ=3613047130 · ACK=2581725300")
d.state("클라이언트", "CLOSE_WAIT", 332, ACC)
d.state("서버", "FIN_WAIT-2", 332, INFO)

d.selfmsg("클라이언트", "socket.close()", 380, ACC,
          sub="애플리케이션의 몫 · 안 부르면 갇힘")

d.msg("클라이언트", "서버", "FIN, ACK", 428, MUTED, "ar", sub="packet#8 · SEQ=3613047130 · ACK=2581725300")
d.state("클라이언트", "LAST_ACK", 460, OK)
d.state("서버", "TIME_WAIT", 460, INFO)

d.msg("서버", "클라이언트", "ACK", 508, MUTED, "ar", sub="packet#9 · SEQ=2581725300 · ACK=3613047131")
d.state("클라이언트", "CLOSED", 556, OK)
d.state("서버", "2×MSL 뒤 CLOSED", 556, INFO)

# CLOSE_WAIT 는 패킷이 아니라 #7 과 #8 사이의 시간 — 클라이언트 레인 왼쪽 괄호
BX = d.LX["클라이언트"] - 64
d.line(BX, 316, BX, 420, ACC, 1.4)
d.line(BX, 316, BX + 12, 316, ACC, 1.4); d.line(BX, 420, BX + 12, 420, ACC, 1.4)
d.t(BX - 8, 362, "CLOSE_WAIT", 11, ACC, MONO, "end", 600)
d.t(BX - 8, 380, "패킷 없는 시간", 11, MUTED, KR, "end")

d.legend(H - 48, [("애플리케이션이 닫아야 하는 구간", ACC), ("능동 종료 쪽 상태", INFO), ("정상 상태", OK)])
d.save("03-01.close-sequence.svg")
