# 04-01 §5 — 원문 Figure 4.6 의 세 스위칭 방식. 셋이 각각 다른 자리에서 막힌다.
# 각 방식의 한계(B/2 · 버스 속도 · 같은 출력 포트)는 원문 4.2.2 의 서술 그대로다.
# 타입 스펙: type-architecture — 구성 요소와 그 사이 관계. zone 으로 세 방식을 묶고 막히는 자리에 강조를 준다.
#           같은 노트의 §3 도식과 타입이 같지만 대상이 다르다 — 하나는 라우터 해부, 하나는 패브릭 세 방식이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 596
ZW, ZY, ZH = 306, 128, 296
ZX = [24, 348, 672]
NW, NH = 74, 34

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 04-01 §5",
      "세 방식은 각각 다른 데서 막힙니다",
      "원문 Figure 4.6 의 세 스위칭 패브릭. 공유하는 자원이 무엇이냐가 상한을 정한다.",
      "강조된 자리가 그 방식의 병목입니다")

TITLES = [("메모리를 거쳐", "가장 이른 방식", "처리량 < B / 2", WARN),
          ("버스를 거쳐", "라벨로 골라 받음", "한 번에 패킷 하나", WARN),
          ("크로스바", "교차점을 열고 닫음", "같은 출력 포트로 몰릴 때만", ACC)]

for zx, (t1, t2, limit, c) in zip(ZX, TITLES):
    d.o.append(f'<rect x="{zx}" y="{ZY}" width="{ZW}" height="{ZH}" rx="8" fill="{INK}05" '
               f'stroke="{RULE}" stroke-width="1" stroke-dasharray="4 4"/>')
    d.t(zx + 16, ZY - 8, t1, 12, INK, KR, "start", 600)
    d.t(zx + ZW - 16, ZY - 8, t2, 12, SOFT, KR, "end")
    for i in range(3):
        y = ZY + 42 + i * 54
        d.box(zx + 18, y, NW, NH, PAPER2, RULE, 1.0, 5)
        d.t(zx + 18 + NW / 2, y + 22, f"in {i+1}", 12, SOFT, MONO)
        d.box(zx + ZW - 18 - NW, y, NW, NH, PAPER2, RULE, 1.0, 5)
        d.t(zx + ZW - 18 - NW / 2, y + 22, f"out {i+1}", 12, SOFT, MONO)
    d.tone(zx + 16, ZH + ZY - 56, ZW - 32, 40, c, 5, "14", 1.2)
    d.t(zx + ZW / 2, ZH + ZY - 30, limit, 12, c, MONO)

# 메모리 — 공유 메모리 한 덩어리를 거친다
mx = ZX[0] + ZW / 2
MW, CI, CO = 64, 124, 230                       # 메모리 폭 · 수집선 · 분배선 (직각 배선)
YM = ZY + 42 + 54 + NH / 2
d.tone(mx - MW / 2, ZY + 84, MW, 68, WARN, 5, "14", 1.4)
d.t(mx, ZY + 114, "메모리", 12, WARN, KR)
d.t(mx, ZY + 132, "쓰기+읽기", 12, SOFT, KR)
Y_TOP, Y_BOT = ZY + 42 + NH / 2, ZY + 42 + 2 * 54 + NH / 2
d.line(CI, Y_TOP, CI, Y_BOT, MUTED, 1.0)
d.line(CO, Y_TOP, CO, Y_BOT, MUTED, 1.0)
for i in range(3):
    y = ZY + 42 + i * 54 + NH / 2
    d.line(ZX[0] + 18 + NW + 2, y, CI, y, MUTED, 1.0)
    d.line(CO, y, ZX[0] + ZW - 18 - NW - 2, y, MUTED, 1.0)
d.path(f"M {CI} {YM} L {mx - MW / 2 - 4} {YM}", MUTED, 1.0, m="ar")
d.path(f"M {mx + MW / 2 + 4} {YM} L {CO - 2} {YM}", MUTED, 1.0, m="ar")

# 버스 — 세로 한 줄
bx = ZX[1] + ZW / 2
d.path(f"M {bx} {ZY+40} L {bx} {ZY+206}", WARN, 2.4)
d.t(bx + 8, ZY + 30, "공유 버스", 12, WARN, KR, "start")
for i in range(3):
    y = ZY + 42 + i * 54 + NH / 2
    d.path(f"M {ZX[1]+18+NW+4} {y} L {bx-4} {y}", MUTED, 1.0, m="ar")
    d.path(f"M {bx+4} {y} L {ZX[1]+ZW-18-NW-6} {y}", MUTED, 1.0, m="ar")

# 크로스바 — 격자와 닫힌 교차점 둘
cx0, cy0 = ZX[2] + 110, ZY + 52
for i in range(3):
    d.line(cx0, cy0 + i * 54, cx0 + 96, cy0 + i * 54, RULE, 1.0)
    d.line(cx0 + i * 44, cy0 - 12, cx0 + i * 44, cy0 + 120, RULE, 1.0)
for gx, gy, c in ((0, 0, ACC), (1, 1, ACC)):
    d.o.append(f'<circle cx="{cx0 + gx*44}" cy="{cy0 + gy*54}" r="5" fill="{ACC}"/>')
d.t(cx0 + 48, cy0 + 142, "동시에 둘이 건넙니다", 12, ACC, KR)

d.t(24, 470, "메모리와 버스는 자원 하나를 모두가 나눠 쓰므로 한 번에 하나만 건널 수 있습니다.",
     11, MUTED, KR, "start")
d.t(24, 492, "크로스바는 쓰는 버스가 다르면 나란히 건널 수 있어 논블로킹입니다. 다만 같은 출력 포트로 가는 둘은 하나가 입력에서 기다립니다.",
     11, MUTED, KR, "start")

d.legend(H - 48, [("나란히 건너는 자리", ACC), ("한 번에 하나뿐인 자원", WARN), ("포트", MUTED)])
d.save("04-01.switching-fabrics.svg")
