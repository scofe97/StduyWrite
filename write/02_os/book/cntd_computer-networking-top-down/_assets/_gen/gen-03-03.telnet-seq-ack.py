# 03-03 §3 — 원문 Figure 3.30. 문자 'C' 하나에 세 세그먼트가 오간다. 세 번째는 서버 메아리에 대한 확인이다.
# 초기 번호 42·79 와 각 세그먼트의 seq·ack 는 원문 값 그대로다.
# 타입 스펙: type-sequence — 참여자 레인 + 시간축 왕복. 응답은 점선, 헤드라인 하나만 강조색.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, INFO, RULE, KR, MONO

def _kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None, lx=0):
        x1, x2 = s.LX[a], s.LX[b]; dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2 + lx
        s.t(mx, y - 9, label, 11, c, _kr(label), "middle", 600)
        if sub: s.t(mx, y + 17, sub, 11, MUTED, KR)

W, H = 1000, 560
d = SeqKR(W, H, "COMPUTER NETWORKING TOP-DOWN · 03-03 §3",
          "문자 하나에 세그먼트 셋",
          "원문 Figure 3.30. 클라이언트 초기 번호 42, 서버 79. 두 번째 세그먼트가 확인 응답과 메아리를 겸하고, 세 번째가 그 메아리를 확인한다.",
          "seq 는 이 세그먼트 첫 바이트의 번호이고 ack 는 다음에 기대하는 바이트의 번호입니다")

d.lanes([("클라이언트", "ISN = 42"), ("서버", "ISN = 79")], y0=104, lane_w=210)
d.rails(400)

d.state("클라이언트", "waiting for byte 79", 168, INFO)
d.state("서버", "waiting for byte 42", 204, INFO)

d.msg("클라이언트", "서버", "seq=42  ack=79  data='C'", 262, MUTED,
      sub="받은 것이 없으니 79 를 기다립니다")
d.msg("서버", "클라이언트", "seq=79  ack=43  data='C'", 322, ACC, mk="acc",
      sub="확인 응답과 메아리를 함께 — 피기배킹")
d.msg("클라이언트", "서버", "seq=43  ack=80  (데이터 없음)", 382, MUTED, dash="5 4",
      sub="서버의 메아리 'C' 를 받았다는 확인 — 80 을 기다립니다")

d.t(20, 442, "세 번째 세그먼트는 데이터가 없는데도 순서 번호를 갖습니다. 헤더에 그 필드가 있으므로 어떤 번호든 가져야 하기 때문입니다.",
     11, MUTED, KR, "start")
d.t(20, 464, "번호가 바이트를 세므로 'C' 한 글자를 보낸 뒤 다음 순서 번호가 42 에서 43 으로 하나만 올라갑니다.",
     11, MUTED, KR, "start")
d.t(20, 486, "데이터가 양쪽으로 한 번씩 흐르므로 확인도 둘 필요합니다. 하나는 메아리에 얹혀 가고 하나는 홀로 갑니다.",
     11, MUTED, KR, "start")

d.legend(H - 44, [("확인 응답을 얹은 세그먼트", ACC), ("연결 직후 상태", INFO), ("나머지", MUTED)])
d.save("03-03.telnet-seq-ack.svg")
