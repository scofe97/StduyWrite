# 07-01 §7 — 없는 이름을 물었을 때 일반 응답과 dnssec 플러그인의 black lies 응답이 다른 자리.
# 근거: draft-valsorda-dnsop-black-lies-00 "The answer MUST have RCODE NOERROR, as opposed to NXDOMAIN",
#       CoreDNS plugin/dnssec/black_lies.go — NextDomain = "\\000." + QName, NXDOMAIN·NODATA 이면
#       filter14(state.QType(), zoneBitmap, mt) 로 zoneBitmap 14종에서 물은 유형만 뺀다.
#       예시 이름 nope.cluster.local 은 설명용이다.
# 타입 스펙: type-dp-security-matrix — 응답 방식(행) × 응답 칸(열)에서 같은 부재가 다르게 적힌다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 440
d = D(W, H, "LEARNING COREDNS · 07-01 §7",
      "없는 이름에 NSEC 하나를 지어 답한다",
      "nope.cluster.local 의 AAAA 를 물었다고 하자. black lies 는 NXDOMAIN 대신 NOERROR 로 답하고, 질의 이름을 소유자로 둔 NSEC 을 즉석에서 지어 서명한다. "
      "CoreDNS 는 고정 비트맵 열넷에서 물은 유형만 뺀다.",
      "주황 칸이 CoreDNS 가 초안 예시와 다르게 채우는 자리입니다")

COLS = [(20, 170, "응답 방식"), (200, 110, "RCODE"), (320, 260, "NSEC 소유자 · 다음 이름"), (590, 270, "유형 비트맵")]
rows = [
    (("서명 없는 응답", ""), "NXDOMAIN", ("—", ""), ("—", "")),
    (("초안 예시", "draft black lies"), "NOERROR", ("nope.cluster.local.", "\\000.nope.cluster.local."), ("RRSIG NSEC", "그 밖엔 아무것도 없음")),
    (("CoreDNS 구현", "dnssec 플러그인"), "NOERROR", ("nope.cluster.local.", "\\000.nope.cluster.local."), ("A TXT SRV … 열셋", "물은 AAAA 만 뺌")),
]

for x, w, head in COLS:
    d.t(x + 10, 118, head, 12, SOFT, KR, "start", 600)

for i, (who, rc, nsec, bm) in enumerate(rows):
    y = 132 + i * 80
    x, w, _ = COLS[0]
    d.box(x, y, w, 66, PAPER2, RULE, 1.0, 6)
    d.t(x + 12, y + 28 if who[1] else y + 38, who[0], 13, INK, KR, "start", 600)
    if who[1]:
        d.t(x + 12, y + 50, who[1], 12, MUTED, KR if any("가" <= c <= "힣" for c in who[1]) else MONO, "start")
    x, w, _ = COLS[1]
    d.box(x, y, w, 66, PAPER2, RULE, 1.0, 6)
    d.t(x + 12, y + 38, rc, 13, INK, MONO, "start", 600)
    for k, (a, b) in ((2, nsec), (3, bm)):
        x, w, _ = COLS[k]
        foc = (i == 2 and k == 3)
        if foc:
            d.tone(x, y, w, 66, ACC, 6, "12", 1.4)
        else:
            d.box(x, y, w, 66, PAPER2, RULE, 1.0, 6)
        if b:
            d.t(x + 12, y + 28, a, 13, ACC if foc else INK, KR if "열셋" in a else MONO, "start", 600)
            d.t(x + 12, y + 50, b, 12, MUTED, KR if any("가" <= c <= "힣" for c in b) else MONO, "start")
        else:
            d.t(x + 12, y + 38, a, 13, SOFT, KR, "start", 600)

d.t(20, 386, "예시 이름은 설명용 · 서명 한 번으로 부재를 증명해 존 전체 이름을 몰라도 된다", 13, MUTED, KR, "start")

d.legend(400, [("구현이 초안 예시와 다른 칸", ACC)])
d.save("07-01.black-lies.svg")
