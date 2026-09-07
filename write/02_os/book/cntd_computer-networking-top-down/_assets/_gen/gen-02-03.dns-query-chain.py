# 02-03 §6 — 원문 Figure 2.17. 이름 하나를 푸는 데 오가는 여덟 개의 메시지.
# 호스트→로컬만 재귀이고 나머지 셋은 반복이라, 로컬 서버가 세 번 모두 스스로 물으러 간다.
# 타입 스펙: type-sequence — 참여자 레인 + 시간축 왕복. 응답은 점선, 마지막 성공만 강조색.
#
# dd.py 의 Seq.msg 는 라벨을 MONO 로 중점에 찍는다. 여기서는 둘을 고쳤다.
#  (1) 한글 라벨이면 KR 로 그린다 (MONO CJK 는 폭 계산이 어긋난다).
#  (2) 라벨 x 를 옮길 수 있게 했다 — 로컬 서버가 두세 칸 건너 물으므로 중점이 남의 레인 위에 앉는다.
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

W, H = 1000, 660
d = SeqKR(W, H, "COMPUTER NETWORKING TOP-DOWN · 02-03 §6",
          "이름 하나에 메시지 여덟 개",
          "원문 Figure 2.17. cse.nyu.edu 가 gaia.cs.umass.edu 의 주소를 얻는 과정. 질의 넷과 응답 넷이 오간다.",
          "첫 질의만 재귀입니다 — 나머지 셋은 로컬 서버가 직접 물으러 갑니다")

d.lanes([("cse.nyu.edu", "요청 호스트"), ("dns.nyu.edu", "로컬 DNS"),
         ("root", "루트 서버"), ("edu TLD", "TLD 서버"), ("dns.umass.edu", "권한 서버")],
        y0=104, lane_w=168)
d.rails(556)

d.msg("cse.nyu.edu", "dns.nyu.edu", "gaia.cs.umass.edu ?", 190, INFO, sub="재귀 — 대신 구해다 달라")

d.msg("dns.nyu.edu", "root", "query", 250, lx=-60)
d.msg("root", "dns.nyu.edu", "edu TLD 주소 목록", 288, MUTED, dash="5 4", lx=-60)

d.msg("dns.nyu.edu", "edu TLD", "query", 348, lx=-118)
d.msg("edu TLD", "dns.nyu.edu", "dns.umass.edu 주소", 386, MUTED, dash="5 4", lx=-118)

d.msg("dns.nyu.edu", "dns.umass.edu", "query", 446, lx=-176)
d.msg("dns.umass.edu", "dns.nyu.edu", "gaia 의 IP 주소", 484, MUTED, dash="5 4", lx=-176)

d.msg("dns.nyu.edu", "cse.nyu.edu", "answer", 538, ACC, mk="acc", dash="5 4")

d.t(20, 592, "가운데 여섯 개가 반복 질의입니다 — 루트도 TLD 도 답을 대신 구해다 주지 않고 다음 단계의 주소만 돌려줍니다.",
     11, MUTED, KR, "start")
d.t(20, 614, "TLD 가 권한 서버를 바로 모르고 중간 서버를 한 단계 더 거치면 메시지가 열 개가 됩니다.",
     11, MUTED, KR, "start")

d.legend(H - 28, [("최종 응답", ACC), ("재귀 질의", INFO), ("반복 질의와 응답", MUTED)])
d.save("02-03.dns-query-chain.svg")
