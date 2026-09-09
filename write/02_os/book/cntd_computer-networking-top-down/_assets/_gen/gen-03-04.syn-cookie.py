# 03-04 §3 — 정상 핸드셰이크에서 서버가 자원을 잡는 시점과, SYN 쿠키가 그 시점을 없애는 방식.
# 각 단계에 담기는 값은 원문 3.5.6 과 곁상자 서술 그대로다.
# 타입 스펙: type-sequence — 참여자 레인 + 시간축 왕복. 자원 할당 시점 하나에 강조색.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, WARN, INFO, RULE, KR, MONO

def _kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None, lx=0):
        x1, x2 = s.LX[a], s.LX[b]; dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2 + lx
        s.t(mx, y - 9, label, 11, c, _kr(label), "middle", 600)
        if sub: s.t(mx, y + 17, sub, 11, MUTED, KR)

W, H = 1000, 660
d = SeqKR(W, H, "COMPUTER NETWORKING TOP-DOWN · 03-04 §3",
          "자원을 언제 잡느냐가 갈림길입니다",
          "정상 3-way 핸드셰이크는 2단계에서 서버가 버퍼와 변수를 잡는다. SYN 쿠키는 그 시점을 없애고 3단계에서 검산으로 대신한다.",
          "SYN 플러드가 통하는 자리가 정확히 2단계의 자원 할당입니다")

d.lanes([("클라이언트", "connect()"), ("서버 — 기본", "자원을 먼저 잡음"), ("서버 — SYN 쿠키", "아무것도 안 잡음")],
        y0=104, lane_w=200)
d.rails(500)

d.msg("클라이언트", "서버 — 기본", "SYN  seq=client_isn", 182, lx=-40)
d.state("서버 — 기본", "alloc buffers + vars", 220, WARN)
d.msg("서버 — 기본", "클라이언트", "SYNACK  seq=server_isn  ack=client_isn+1", 268, MUTED, dash="5 4", lx=-40)
d.msg("클라이언트", "서버 — 기본", "ACK  ack=server_isn+1", 322, OK, mk="ok", lx=-40,
      sub="여기까지 안 오면 반쯤 열린 연결이 남습니다")

d.msg("클라이언트", "서버 — SYN 쿠키", "SYN", 396, lx=-90)
d.state("서버 — SYN 쿠키", "isn = hash(ips, ports, secret)", 434, ACC)
d.msg("서버 — SYN 쿠키", "클라이언트", "SYNACK  seq=cookie", 470, MUTED, dash="5 4", lx=-90)
d.msg("클라이언트", "서버 — SYN 쿠키", "ACK  ack=cookie+1", 512, ACC, mk="acc", lx=-90,
      sub="같은 해시를 다시 계산해 검산한 뒤에야 소켓을 만듭니다")

d.t(20, 566, "서버가 상태를 기억하는 대신 다시 계산할 수 있게 만든 설계입니다. 들고 있어야 할 정보를 상대에게 들려 보내고 돌아올 때 검산합니다.",
     11, MUTED, KR, "start")
d.t(20, 588, "ACK 가 안 오면 원래의 가짜 SYN 은 아무 해도 끼치지 않습니다 — 자원을 할당한 적이 없기 때문입니다.",
     11, MUTED, KR, "start")

d.legend(H - 44, [("쿠키를 검산하는 자리", ACC), ("공격이 노리는 자리", WARN), ("정상 완료", OK)])
d.save("03-04.syn-cookie.svg")
