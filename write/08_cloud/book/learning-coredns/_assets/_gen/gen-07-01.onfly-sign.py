# 07-01 §7 — 합성한 레코드가 서명되어 캐시에 얹히기까지. 캐시가 이 방식의 실질적 조건이다.
# 원문 근거: "CoreDNS will sign generated resource records on the fly with the configured keys."
#            / "After the dnssec plug-in generates a signature for a particular synthesized
#            resource record, it stores that signature so that it won't need to recalculate the
#            same signature later. The default is 10,000 signatures."
# 타입 스펙: type-process — 단계가 순서대로 이어지고 캐시 적중이 한 단계를 건너뛴다.
#           우회 경로는 카드 위 통로로 빼 축 정렬을 지킨다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, OK, KR, MONO

W, H = 880, 560
d = D(W, H, "LEARNING COREDNS · 07-01 §7",
      "합성 레코드가 서명되어 캐시에 얹히기까지",
      "kubernetes 플러그인이 만든 레코드에는 미리 서명해 둘 파일이 없다. dnssec 플러그인이 "
      "요청 시점에 서명을 만들고, 만든 서명을 캐시에 두어 같은 계산을 반복하지 않는다.",
      "주황이 이 방식을 실용적으로 만드는 자리입니다")

CW, CG, X0, CY, CH = 190, 24, 30, 150, 90
XS = [X0 + i * (CW + CG) for i in range(4)]
CARDS = [
    ("01", "레코드를 합성한다", "kubernetes 플러그인"),
    ("02", "캐시를 먼저 본다", "cache_capacity 10000"),
    ("03", "없으면 서명을 만든다", "ZSK 또는 CSK 개인 키"),
    ("04", "RRSIG 을 붙여 응답", "DO 비트를 세운 질의에"),
]

# 캐시 적중 우회 — 카드 위 통로
d.path(f"M {XS[1] + CW / 2} {CY} L {XS[1] + CW / 2} 112 L {XS[3] + CW / 2} 112 L {XS[3] + CW / 2} {CY - 2}",
       OK, 1.6, m="ok")
d.t((XS[1] + XS[3]) / 2 + CW / 2, 104, "캐시에 있으면 03 을 건너뛴다", 11, OK, KR)

for i in range(3):
    d.arrow([(XS[i] + CW, CY + CH / 2), (XS[i + 1] - 2, CY + CH / 2)], MUTED, "ar", 1.4)

for i, (n, t1, t2) in enumerate(CARDS):
    x = XS[i]
    if i == 1:
        d.tone(x, CY, CW, CH, ACC, 8, "12", 1.4)
    else:
        d.box(x, CY, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 16, CY + 26, n, 11, ACC if i == 1 else SOFT, MONO, "start", 600)
    d.t(x + 16, CY + 54, t1, 14, ACC if i == 1 else INK, KR, "start", 600)
    d.t(x + 16, CY + 76, t2, 11, MUTED, MONO, "start")

# 캐시 저장소
d.tone(XS[1], 310, CW * 2 + CG, 76, ACC, 8, "0E", 1.4)
d.t(XS[1] + (CW * 2 + CG) / 2, 338, "서명 캐시", 15, ACC, KR, "middle", 600)
d.t(XS[1] + (CW * 2 + CG) / 2, 360, "기본 10,000개 · 같은 서명을 다시 계산하지 않는다", 11, MUTED, KR)

d.arrow([(XS[1] + CW / 2, CY + CH), (XS[1] + CW / 2, 308)], ACC, "acc", 1.4)
d.t(XS[1] + CW / 2 + 12, 268, "조회", 11, ACC, KR, "start")
d.arrow([(XS[2] + CW / 2, 308), (XS[2] + CW / 2, CY + CH + 2)], ACC, "acc", 1.4)
d.t(XS[2] + CW / 2 + 12, 268, "저장", 11, ACC, KR, "start")

d.box(20, 404, 840, 78, PAPER, RULE, 0.8)
d.t(36, 428, "정적 존과 다른 점", 12, INK, KR, "start", 600)
d.t(36, 450, "미리 서명하면 개인 키를 오프라인에 둘 수 있지만, 즉석 서명은 서버가 키를 계속 들고 있어야 한다",
     11, MUTED, KR, "start")
d.t(36, 470, "그래서 서명이 작은 ECDSA 를 권한다 — 계산과 응답 크기가 함께 줄어든다", 11, MUTED, KR, "start")

d.legend(500, [("캐시가 붙는 자리", ACC), ("캐시 적중 시 경로", OK)])
d.save("07-01.onfly-sign.svg")
