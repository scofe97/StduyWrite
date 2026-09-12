# 04-01 §1 — 원문 Figure 4.2·4.3. 포워딩 테이블을 누가 채우는가. 전통 방식은 라우터마다 라우팅 알고리즘이 돌고,
# SDN 은 물리적으로 분리된 원격 컨트롤러가 계산해 내려보낸다. 데이터 평면은 두 방식이 완전히 같다 — 원문 서술 그대로다.
# 타입 스펙: type-architecture — 구성 요소와 그 사이 관계. zone 둘로 두 방식을 대비하고 컨트롤러에만 focal 을 준다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 640
ZY, ZH, ZW = 112, 392, 464
ZX = [24, 512]
RW, RH, RY = 128, 104, 300

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 04-01 §1",
      "포워딩 테이블을 누가 채우는가",
      "원문 Figure 4.2·4.3. 전통 방식은 라우터마다 라우팅 알고리즘이 돌고, SDN 은 원격 컨트롤러가 테이블을 계산해 내려보낸다. 데이터 평면은 둘이 같다.",
      "달라지는 것은 제어 평면의 자리뿐입니다")

for zx, title in zip(ZX, ("전통적 방식 — 제어 평면이 라우터마다 안에 있습니다", "SDN — 원격 컨트롤러가 계산해 내려보냅니다")):
    d.o.append(f'<rect x="{zx}" y="{ZY}" width="{ZW}" height="{ZH}" rx="8" fill="{INK}05" stroke="{RULE}" stroke-width="1" stroke-dasharray="4 4"/>')
    d.t(zx + 16, ZY - 8, title, 12, SOFT, KR, "start")

def router(cx, i, sdn):
    x = cx - RW / 2
    d.box(x, RY, RW, RH, PAPER2, RULE, 1.0, 6)
    d.t(cx, RY + 24, f"라우터 {i}", 13, INK, KR, "middle", 600)
    if sdn:
        d.chip(cx, RY + 54, "포워딩 테이블", MUTED, 12)
        d.t(cx, RY + 86, "포워딩만 합니다", 12, SOFT, KR)
    else:
        d.chip(cx, RY + 50, "라우팅 알고리즘", INFO, 12)
        d.chip(cx, RY + 80, "포워딩 테이블", MUTED, 12)

# 왼쪽 — 라우터끼리 라우팅 메시지를 주고받는다
LC = [108, 256, 404]
for i, cx in enumerate(LC):
    router(cx, i + 1, False)
for a, b in ((LC[0], LC[1]), (LC[1], LC[2])):
    d.path(f"M {a + RW / 2 + 3} {RY + 50} L {b - RW / 2 - 6} {RY + 50}", INFO, 1.3, m="info")
d.t(256, 268, "라우팅 메시지를 주고받아 각자 자기 테이블을 계산합니다", 12, INFO, KR)
d.t(256, 200, "제어 평면과 데이터 평면이", 12, MUTED, KR)
d.t(256, 220, "한 상자 안에 함께 있습니다", 12, MUTED, KR)

# 오른쪽 — 원격 컨트롤러가 내려보낸다
RC = [596, 744, 892]
CTX, CTY, CTW, CTH = 592, 160, 304, 64
d.tone(CTX, CTY, CTW, CTH, ACC, 6, "14", 1.4)
d.t(744, CTY + 26, "원격 컨트롤러", 14, ACC, KR, "middle", 600)
d.t(744, CTY + 48, "테이블을 계산해 내려보냅니다 · 소프트웨어", 12, SOFT, KR)
for i, cx in enumerate(RC):
    router(cx, i + 1, True)
d.path(f"M 744 {CTY + CTH + 2} L 744 {RY - 8}", INFO, 1.3, m="info", dash="5 4")
for cx in (RC[0], RC[2]):
    d.path(f"M 744 {CTY + CTH + 2} L 744 262 L {cx} 262 L {cx} {RY - 8}", INFO, 1.3, m="info", dash="5 4")
d.t(756, 250, "포워딩 테이블 배포", 12, INFO, KR, "start")

d.t(24, 540, "데이터 평면은 두 방식이 완전히 같습니다. 달라지는 것은 포워딩 테이블을 누가 계산하느냐뿐입니다.", 13, MUTED, KR, "start")
d.t(24, 562, "5장이 이 물음을 이어받습니다 — 라우팅 알고리즘은 05-01, 원격 컨트롤러는 05-03 에서.", 13, SOFT, KR, "start")

d.legend(H - 44, [("원격 컨트롤러 — 이 절의 논점", ACC), ("제어 평면 · 테이블 계산", INFO), ("데이터 평면 · 포워딩", MUTED)])
d.save("04-01.two-planes.svg")
