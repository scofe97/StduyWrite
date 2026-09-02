# 06-05 §2 — E2E 를 돌릴 자리를 정하는 판단 (원문 End-to-End Testing 앞부분).
# 갈래의 문구는 원문 서술 그대로다. 오른쪽 두 결과가 온디맨드 역량이 없을 때의 권고안과 최후의 수단이다.
# 타입 스펙: type-flowchart — 조건에 따라 갈라지는 판단 논리. 마름모가 판단, 사각형이 결과.
#           축약: 06-04.ci-by-split 의 두 갈래 배치를 승계하되, 오른쪽 갈래만 결과가 둘이라 형제 상자를 붙였다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, WARN, PAPER2, RULE, KR, MONO

W = 1400
SX, SY, SW, SH = 460, 108, 480, 76
DCX, DCY, DHW, DHH = 700, 258, 230, 62
BW, BH = 460, 96
LX, RX, Y1 = 100, 840, 400
CW2, CGAP, CY2 = 220, 20, 552
CAVEAT_Y = CY2 + 96 + 32
LEGEND_Y = CAVEAT_Y + 32
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 06-05 §2",
      "E2E 를 돌릴 자리를 정한다",
      "마름모가 판단이고 사각형이 그 결과다. 색이 붙은 것이 온디맨드 역량이 없을 때의 권고안이다.",
      "회사가 가진 역량이 시점을 정합니다")

d.box(SX, SY, SW, SH, PAPER2, RULE, 1.0, 10)
d.t(W / 2, SY + 32, "E2E 를 돌릴 자리를 정한다", 13, INK, KR, "middle", 600)
d.t(W / 2, SY + 54, "flow from start to finish", 9, MUTED, MONO)
d.arrow([(W / 2, SY + SH), (W / 2, DCY - DHH - 2)], MUTED, "ar", 1.4)

d.path(f"M {DCX} {DCY - DHH} L {DCX + DHW} {DCY} L {DCX} {DCY + DHH} L {DCX - DHW} {DCY} Z", MUTED, 1.2)
d.t(DCX, DCY + 5, "온디맨드 환경을 만들 수 있나", 13, INK, KR, "middle", 600)

d.arrow([(DCX - DHW, DCY), (LX + BW / 2, DCY), (LX + BW / 2, Y1 - 2)], MUTED, "ar", 1.4)
d.t(LX + BW / 2 + 24, DCY - 12, "그렇다", 10, MUTED, KR, "start")
d.arrow([(DCX + DHW, DCY), (RX + BW / 2, DCY), (RX + BW / 2, Y1 - 2)], MUTED, "ar", 1.4)
d.t(RX + BW / 2 - 24, DCY - 12, "아니다", 10, MUTED, KR, "end")

d.box(LX, Y1, BW, BH, PAPER2, RULE, 1.0, 6)
d.t(LX + BW / 2, Y1 + 38, "배포 전에 돈다", 12.5, INK, KR, "middle", 600)
d.t(LX + BW / 2, Y1 + 62, "런타임에 만들고 끝나면 허문다", 10, MUTED)

d.box(RX, Y1, BW, BH, PAPER2, RULE, 1.0, 6)
d.t(RX + BW / 2, Y1 + 38, "배포하거나 승격한 뒤 기존 환경에서", 12.5, INK, KR, "middle", 600)
d.t(RX + BW / 2, Y1 + 62, "여기서 다시 갈린다", 10, MUTED)

kids = [
    (RX, "피처 플래그가 있다면", "프로덕션에서 테스트한다", ACC),
    (RX + CW2 + CGAP, "없다면", "가진 환경을 쓴다 · 최후의 수단", WARN),
]
for kx, title, sub, c in kids:
    d.arrow([(RX + BW / 2, Y1 + BH), (RX + BW / 2, CY2 - 24), (kx + CW2 / 2, CY2 - 24), (kx + CW2 / 2, CY2 - 2)], MUTED, "ar", 1.2)
    d.o.append(f'<rect x="{kx}" y="{CY2}" width="{CW2}" height="96" rx="6" fill="{c}12" stroke="{c}" stroke-width="1.4"/>')
    d.t(kx + CW2 / 2, CY2 + 34, title, 11.5, c, KR, "middle", 600)
    d.t(kx + CW2 / 2, CY2 + 58, sub, 9.5, MUTED)

# 값과 난제는 프로덕션 테스트 쪽의 것이므로 그 갈래 아래에만 둔다
d.t(RX + CW2 + CGAP / 2, CAVEAT_Y,
    "여러 환경을 유지할 필요가 없어 인프라와 유지보수와 개발자 자원을 아끼지만 서드파티 API 연동이 난제로 남는다",
    10, SOFT)

d.legend(LEGEND_Y, [("온디맨드가 없을 때의 권고안", ACC), ("최후의 수단", WARN)])
d.save("06-05.where-to-test.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H, " 우측끝:", RX + CW2 + CGAP + CW2)
