# 07-01 §5 — EDNS0 옵션을 싣는 쪽과 푸는 쪽. 두 플러그인이 같은 옵션을 두고 방향만 반대다.
# 원문 근거: "By using the rewrite plug-in with EDNS0 rules, upstream name servers can receive
#            information about the deployment location and modify their responses, as needed."
#            / metadata_edns0: "It provides the reverse of the rewrite edns0 function. That is,
#            it will unpack an EDNS0 option into a metadata value, allowing it to be logged or
#            reused in a different rewrite."
# 타입 스펙: type-swimlane — 두 배치(엣지·상류)가 레인이고, 레인을 건너는 EDNS0 옵션이
#           이 그림에서 가장 중요한 엣지다. 핸드오프는 직교 경로로만 놓는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, OK, INFO, KR, MONO

W, H = 880, 570
d = D(W, H, "LEARNING COREDNS · 07-01 §5",
      "EDNS0 를 싣는 쪽과 푸는 쪽",
      "엣지 배치의 CoreDNS 가 요청에 EDNS0 옵션을 붙이고, 상류의 CoreDNS 가 그것을 풀어 "
      "metadata 로 발행한다. rewrite edns0 와 metadata_edns0 는 같은 옵션의 반대 방향이다.",
      "주황이 레인을 건너는 EDNS0 옵션입니다")

LX, LW, LH = 150, 710, 130
LANES = [("EDGE", "집·지사의 CoreDNS", 120), ("UPSTREAM", "클라우드의 CoreDNS", 280)]

for nm, sub, y in LANES:
    d.box(LX, y, LW, LH, PAPER, RULE, 0.8, 6)
    d.t(20, y + 36, nm, 9, SOFT, MONO, "start", 600)
    d.t(20, y + 58, sub, 12, MUTED, KR, "start")

SW2, SG, SX0 = 210, 20, 170
XS = [SX0 + i * (SW2 + SG) for i in range(3)]


def step(x, y, t1, t2, c=INK, tone=None):
    if tone:
        d.tone(x, y, SW2, 70, tone, 6, "12", 1.4)
    else:
        d.box(x, y, SW2, 70, PAPER2, RULE, 1.0)
    d.t(x + SW2 / 2, y + 28, t1, 13, c, KR, "middle", 600)
    d.t(x + SW2 / 2, y + 49, t2, 10, MUTED, MONO)


step(XS[0], 150, "클라이언트 질의를 받는다", "example.com A")
step(XS[1], 150, "옵션을 실어 붙인다", "rewrite edns0 local set", ACC, ACC)
step(XS[2], 150, "암호화해 넘긴다", "forward · DNS over TLS")

step(XS[0], 310, "옵션이 붙은 질의 도착", "0xffed · 0xffee")
step(XS[1], 310, "풀어서 발행한다", "metadata_edns0", ACC, ACC)
step(XS[2], 310, "다른 플러그인이 쓴다", "log · rewrite")

d.arrow([(XS[0] + SW2, 185), (XS[1] - 2, 185)], MUTED, "ar", 1.4)
d.arrow([(XS[1] + SW2, 185), (XS[2] - 2, 185)], MUTED, "ar", 1.4)
d.arrow([(XS[0] + SW2, 345), (XS[1] - 2, 345)], MUTED, "ar", 1.4)
d.arrow([(XS[1] + SW2, 345), (XS[2] - 2, 345)], MUTED, "ar", 1.4)

# 레인을 건너는 핸드오프 — 이 그림의 본체
d.path(f"M {XS[2] + SW2 / 2} 220 L {XS[2] + SW2 / 2} 265 L {XS[0] + SW2 / 2} 265 L {XS[0] + SW2 / 2} 308",
       ACC, 1.8, m="acc")
d.t(440, 258, "EDNS0 옵션이 레인을 건넌다", 11, ACC, KR)

d.box(20, 432, 840, 56, PAPER, RULE, 0.8)
d.t(36, 456, "같은 옵션을 두고 방향만 반대다", 12, ACC, KR, "start", 600)
d.t(36, 478, "rewrite edns0 는 싣고 metadata_edns0 는 푼다 · 후자는 저장소 밖 플러그인이라 재빌드가 필요하다",
     11, MUTED, KR, "start")

d.legend(508, [("옵션을 다루는 두 플러그인", ACC), ("레인 안의 처리", MUTED)])
d.save("07-01.edns0-roundtrip.svg")
