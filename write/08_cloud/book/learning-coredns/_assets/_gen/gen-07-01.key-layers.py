# 07-01 §6 — 부모 존에서 레코드까지의 서명 계층. 왜 키가 둘인지가 이 계층에서 나온다.
# 원문 근거: "keys used frequently to sign a lot of records (like the ZSK) need to be 'rolled
#            over' on a regular basis, but our parent zone needs to include information about our
#            keys in their zone, too. It would be a hassle to let our parent zone know each time
#            we rolled over our ZSK. So we introduce another key pair, the KSK, which is used
#            only to sign keys (hence, less data) and therefore doesn't need to be rolled over as
#            frequently. Those are the keys our parent zone knows about."
# 주기 수치: NIST SP 800-81-2 체크리스트 30 — "The recommended rollover frequency for the KSK is
#            once every 1 to 2 years, whereas the ZSK should be rolled over every 1 to 3 months".
#            그 문서는 2026-03-19 철회되고 SP 800-81r3 로 대체됐다.
# 타입 스펙: type-layers — 위로 갈수록 갈아 끼우는 비용이 크고 아래로 갈수록 자주 갈아야 하는
#           계층이다. 부모 존이 아는 층(KSK)이 초점이라 그 한 층만 주황으로 둔다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 560
d = D(W, H, "LEARNING COREDNS · 07-01 §6",
      "부모 존에서 레코드까지, 갈아 끼우는 비용",
      "위로 갈수록 갈아 끼우는 데 남의 손이 필요하고 아래로 갈수록 자주 갈아야 한다. "
      "부모 존이 아는 층을 KSK 하나로 좁힌 것이 두 키로 나눈 이유다.",
      "주황이 부모 존이 아는 층입니다")

SX, SW, RH = 170, 690, 68
ROWS = [
    ("L1", "부모 존", "DS 레코드로 우리 키를 가리킨다", "갱신에 부모와의 협의가 필요", False),
    ("L2", "KSK", "존 안의 키만 서명한다", "원서 인용 · 1~2년마다", True),
    ("L3", "ZSK", "나머지 레코드 전부를 서명한다", "원서 인용 1~3개월 · ECDSA 는 12~24개월", False),
    ("L4", "존 레코드", "RRSIG 이 붙는 대상", "서명이 만료되기 전에 다시 서명", False),
]

for i, (tag, name, mid, right, focal) in enumerate(ROWS):
    y = 130 + i * RH
    if focal:
        d.tone(SX, y, SW, RH, ACC, 0, "12", 1.4)
    else:
        d.box(SX, y, SW, RH, PAPER2 if i % 2 else PAPER, RULE, 1.0, 0)
    d.t(SX + 18, y + 26, tag, 9, ACC if focal else SOFT, MONO, "start", 600)
    d.t(SX + 18, y + 48, name, 15, ACC if focal else INK, KR, "start", 600)
    d.t(SX + 150, y + 42, mid, 12, MUTED, KR, "start")
    d.t(SX + SW - 18, y + 42, right, 11, ACC if focal else MUTED, KR, "end")

# 왼쪽 방향 표시 — 스택 바깥
d.t(58, 152, "ROLLOVER", 8, SOFT, MONO, "start")
d.t(58, 172, "잦아진다", 11, MUTED, KR, "start")
d.arrow([(40, 188), (40, 384)], MUTED, "ar", 1.4)
d.t(58, 296, "갈아 끼우는", 11, SOFT, KR, "start")
d.t(58, 314, "비용은 반대로", 11, SOFT, KR, "start")
d.t(58, 332, "위로 갈수록", 11, SOFT, KR, "start")
d.t(58, 350, "커진다", 11, SOFT, KR, "start")

d.box(20, 424, 840, 78, PAPER, RULE, 0.8)
d.t(36, 448, "원서가 인용한 권고는 이제 옛것이다", 12, INK, KR, "start", 600)
d.t(36, 470, "NIST SP 800-81-2 는 2026-03-19 철회되고 SP 800-81r3 로 전부 대체됐다", 11, MUTED, KR, "start")
d.t(36, 490, "개정판은 KSK·ZSK 를 나눈 주기를 버리고 서명 키 최대 수명 1~3년 하나로 두며, RRSIG 유효 기간 5~7일을 강조한다",
     11, MUTED, KR, "start")

d.legend(516, [("부모 존이 아는 층", ACC)])
d.save("07-01.key-layers.svg")
