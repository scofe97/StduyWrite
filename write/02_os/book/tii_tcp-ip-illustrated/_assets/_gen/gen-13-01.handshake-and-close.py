# 13-01 §2·§3 — 원서 그림 13-1(정상 수립·종료)을 그림 13-5(Wireshark 캡처)의 실제 값으로 채운다.
# 값 출처: 원문 13.2.4 — 클라이언트 ISN 685506836 · 창 65535, 서버 ISN 1479690171 · ACK 685506837 · 창 64,240,
#   셋째 세그먼트 ACK 1479690172. 4.4초 뒤 클라이언트 FIN seq 685506837, 서버 ACK 685506838,
#   서버 FIN seq 1479690172(PSH 켜짐, 클라이언트 FIN 을 다시 확인), 마지막 ACK 1479690173.
# 타입 스펙: type-sequence — 주체 둘 사이의 시간순 메시지 7개(예산 12 이내). 응답은 점선 대신 같은 실선으로 두되
#           세 국면(수립 · 4.4초 정지 · 종료)을 왼쪽 괄호로 묶는다. focal 은 수립을 끝내는 셋째 세그먼트 하나.
#           프리미티브 Seq.msg 가 한글 라벨을 MONO 로 하드코딩하므로 계약대로 서브클래스로 감싼다.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, INFO, WARN, PAPER, PAPER2, RULE, KR, MONO

def _kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]; dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 12, c, _kr(label), "middle", 600)
        if sub: s.t(mx, y + 17, sub, 11, MUTED, _kr(sub))

W, H = 920, 616
d = SeqKR(W, H, "TCP/IP ILLUSTRATED VOL.1 · 13-01 §2 · §3",
          "연결 하나의 일곱 세그먼트 — 원서 캡처의 실제 값",
          "원서 그림 13-1 의 수립·종료 흐름을 그림 13-5 캡처 값으로 채웠다. 위 세 세그먼트가 3-way handshake 로 양쪽 ISN 을 교환하고, "
          "4.4초 뒤 아래 네 세그먼트가 한 방향씩 닫는다. ACK 번호는 언제나 상대가 다음에 보낼 번호이고 SYN·FIN 은 번호 하나씩을 차지한다.",
          "열 때 셋, 닫을 때 넷 — 각 FIN 은 ACK 를 받아야 끝납니다")

d.lanes([("클라이언트 · 능동 열기", "192.168.35.130"), ("서버 · 수동 열기", "10.0.0.2:80")], y0=100, lane_w=300)
d.rails(588)

C, S = "클라이언트 · 능동 열기", "서버 · 수동 열기"
d.msg(C, S, "SYN", 196, INFO, "info", sub="seq 685506836 · win 65535 · 옵션")
d.msg(S, C, "SYN, ACK", 248, INFO, "info", sub="seq 1479690171 · ack 685506837 · win 64240")
d.msg(C, S, "ACK", 300, ACC, "acc", sub="ack 1479690172 · 수립 완료")
d.msg(C, S, "FIN, ACK", 400, WARN, "warn", sub="seq 685506837 · ack 1479690172")
d.msg(S, C, "ACK", 452, WARN, "warn", sub="ack 685506838 · 한 방향 닫힘")
d.msg(S, C, "FIN, PSH, ACK", 504, WARN, "warn", sub="seq 1479690172 · ack 685506838")
d.msg(C, S, "ACK", 556, WARN, "warn", sub="ack 1479690173 · 양방향 닫힘")

# 국면 괄호
bx = 40
for y0, y1, lab, c in ((180, 320, "수립", INFO), (336, 368, "4.4초", SOFT), (384, 576, "종료", WARN)):
    d.path(f"M {bx + 8} {y0} H {bx} V {y1} H {bx + 8}", c, 1.2)
    d.t(bx - 4, (y0 + y1) / 2 + 4, lab, 12, c, KR, "end", 600)
d.line(d.LX[C] + 20, 352, d.LX[S] - 20, 352, RULE, 0.8, "2 4")

d.save("13-01.handshake-and-close.svg")
