# 08-01 §4 — 같은 질의 하나를 log 와 dnstap 이 각각 무엇으로 남기는가.
# 원문 근거: "Logging a message for each query received imposes some overhead on a DNS server ...
#            query logging also includes mostly information about the query received but not much
#            about the response to that query ... dnstap was developed to address both of these
#            issues, and provides a mechanism for logging complete response data very efficiently"
#            / "The socket is not created by CoreDNS; instead, a different program creates it"
# 타입 스펙: type-swimlane — 두 도구가 레인이고, 같은 질의가 각 레인에서 다른 산출물이 된다.
#           레인을 건너는 것은 없고 대신 같은 입력이 갈라지는 것이 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, OK, KR, MONO

W, H = 880, 560
d = D(W, H, "LEARNING COREDNS · 08-01 §4",
      "log 와 dnstap 이 같은 질의를 다르게 남긴다",
      "질의 하나가 두 도구에서 서로 다른 산출물이 된다. log 는 사람이 읽는 한 줄을, "
      "dnstap 은 기계가 읽는 이진 프레임을 남기고 소켓 밖으로 넘긴다.",
      "주황이 full 을 붙였을 때만 실리는 것입니다")

LX, LW, LH = 150, 710, 132
LANES = [("LOG", "사람이 읽는다", 118), ("DNSTAP", "기계가 읽는다", 274)]
for nm, sub, y in LANES:
    d.box(LX, y, LW, LH, PAPER, RULE, 0.8, 6)
    d.t(20, y + 38, nm, 9, SOFT, MONO, "start", 600)
    d.t(20, y + 60, sub, 12, MUTED, KR, "start")

SW, SG, SX0 = 210, 20, 170
XS = [SX0 + i * (SW + SG) for i in range(3)]


def step(x, y, t1, t2, c=INK, tone=None):
    if tone:
        d.tone(x, y, SW, 72, tone, 6, "12", 1.4)
    else:
        d.box(x, y, SW, 72, PAPER2, RULE, 1.0)
    d.t(x + SW / 2, y + 28, t1, 13, c, KR, "middle", 600)
    d.t(x + SW / 2, y + 50, t2, 11, MUTED, MONO)


step(XS[0], 148, "질의마다 한 줄", "텍스트 · 부하가 붙는다")
step(XS[1], 148, "응답 정보는 적다", "rcode · rflags · rsize")
step(XS[2], 148, "표준 출력으로", "사람이 눈으로 읽는다")

step(XS[0], 304, "와이어 형식 프레임", "이진 · 값이 낮다")
step(XS[1], 304, "응답 전체가 실린다", "full 을 붙였을 때", ACC, ACC)
step(XS[2], 304, "소켓 밖으로", "CoreDNS 가 만들지 않는다")

for row_y in (184, 340):
    d.arrow([(XS[0] + SW, row_y), (XS[1] - 2, row_y)], MUTED, "ar", 1.4)
    d.arrow([(XS[1] + SW, row_y), (XS[2] - 2, row_y)], MUTED, "ar", 1.4)

d.box(20, 426, 840, 62, PAPER, RULE, 0.8)
d.t(36, 450, "같은 질의 한 건이 두 레인으로 갈라진다 — 둘은 배타적이지 않다", 12, INK, KR, "start", 600)
d.t(36, 472, "사람이 볼 것은 좁게 건 log 로, 나중에 분석할 것은 dnstap 으로 — 다만 그러면 값도 두 번 낸다",
     11, MUTED, KR, "start")

d.legend(508, [("full 이 더하는 것", ACC), ("기본으로 실리는 것", MUTED)])
d.save("08-01.dnstap-lanes.svg")
