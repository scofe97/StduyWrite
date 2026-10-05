# 13-01 §3 — half-close 를 실제로 떠 본 캡처(OrbStack Ubuntu, 커널 7.0.14, 2026-10-04)를 원서 그림 13-2 의 모양으로 그린다.
# 캡처 사실: 클라이언트가 17바이트를 보내고 shutdown(SHUT_WR) → FIN. 서버는 recv() 가 b"" 를 돌려줄 때까지 읽고
#   13바이트 응답을 보낸다. 이 응답 세그먼트가 클라이언트 FIN 에 대한 ACK 를 겸한다(ack = FIN seq + 1).
#   그 뒤 서버 close() → FIN, 클라이언트 ACK. 핸드셰이크 세 줄은 생략했다.
# 타입 스펙: type-sequence — 주체 둘 사이의 시간순 메시지 7개. 레인 바깥쪽 글자가 그 시점의 소켓 호출이다.
#           focal 은 반쯤 닫힌 연결 위로 서버가 보내는 13바이트 응답 하나 — half-close 의 존재 이유.
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

W, H = 920, 600
d = SeqKR(W, H, "TCP/IP ILLUSTRATED VOL.1 · 13-01 §3",
          "half-close — FIN 을 보낸 뒤에도 받는다",
          "클라이언트가 요청 17바이트를 보내고 shutdown(SHUT_WR) 으로 쓰기 방향만 닫았다. 서버는 FIN 을 EOF 로 읽은 뒤에도 같은 연결로 13바이트를 돌려보내고, "
          "그 세그먼트가 클라이언트 FIN 의 ACK 를 겸한다. 서버가 close() 해 두 번째 FIN 이 확인되면 연결이 완전히 닫힌다. 레인 바깥 글자는 그 순간의 소켓 호출이다.",
          "FIN 은 '나는 더 안 보낸다' 이지 '더 받지 않는다' 가 아닙니다")

C, S = "클라이언트", "서버"
d.lanes([(C, "127.0.0.1:37270"), (S, "127.0.0.1:8099")], y0=100, lane_w=300)
d.rails(552)
xc, xs = d.LX[C], d.LX[S]

def call(side, y, txt, c=SOFT):
    if side == C: d.t(xc - 24, y + 4, txt, 12, c, MONO, "end")
    else: d.t(xs + 24, y + 4, txt, 12, c, MONO, "start")

d.msg(C, S, "데이터 17바이트", 192, INFO, "info", sub="PSH, ACK")
call(C, 192, "sendall()")
call(S, 192, "recv() → 17B")
d.msg(S, C, "ACK", 244, MUTED, "ar")
d.msg(C, S, "FIN, ACK", 296, WARN, "warn", sub="쓰기 방향만 닫힘")
call(C, 296, "shutdown(SHUT_WR)", WARN)
call(S, 296, "recv() → b''", WARN)
d.msg(S, C, "데이터 13바이트", 348, ACC, "acc", sub="PSH, ACK · FIN 확인을 겸함")
call(S, 348, "sendall()")
call(C, 348, "recv() → 13B")
d.msg(C, S, "ACK", 400, MUTED, "ar")
d.msg(S, C, "FIN, ACK", 452, WARN, "warn", sub="반대 방향도 닫힘")
call(S, 452, "close()", WARN)
call(C, 452, "recv() → b''", WARN)
d.msg(C, S, "ACK", 504, MUTED, "ar", sub="연결 종료")

d.legend(H - 56, [("반쯤 닫힌 연결 위의 응답", ACC), ("FIN 과 EOF", WARN), ("데이터", INFO)])
d.save("13-01.half-close.svg")
