# 06-04 §4 — 분할 방식이 CI 단계를 가른다 (원문 Continuous Integration Strategies 마지막 문단).
# 두 갈래의 문구는 원문 서술 그대로다. 오른쪽 아래 경고 상자가 저자가 "유지하고 발전시키기 어렵다"고 적은 결말이다.
# 타입 스펙: type-flowchart — 조건에 따라 갈라지는 판단 논리. 마름모가 판단, 사각형이 결과.
#           축약: 05-02.error-behaviour 의 두 갈래 배치를 승계했다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, WARN, PAPER2, RULE, KR, MONO

W = 1240
SX, SY, SW, SH = 380, 108, 480, 76
DCX, DCY, DHW, DHH = 620, 268, 200, 62
BW, BH = 460, 92
LX, RX = 80, 700
Y1, Y2 = 420, 552
LEGEND_Y = Y2 + BH + 40
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 06-04 §4",
      "분할 방식이 CI 단계를 가른다",
      "마름모가 판단이고 사각형이 그 결과다. 색이 붙은 갈래가 E2E 를 돌릴 자리를 옮겨야 하는 쪽이다.",
      "조각에 유일한 CI 구현은 없고 아키텍처 접근이 단계를 정합니다")

# 시작
d.box(SX, SY, SW, SH, PAPER2, RULE, 1.0, 10)
d.t(W / 2, SY + 32, "CI 파이프라인의 단계를 정한다", 13, INK, KR, "middle", 600)
d.t(W / 2, SY + 54, "project · company standards · architecture", 9, MUTED, MONO)
d.arrow([(W / 2, SY + SH), (W / 2, DCY - DHH - 2)], MUTED, "ar", 1.4)

# 판단
d.path(f"M {DCX} {DCY - DHH} L {DCX + DHW} {DCY} L {DCX} {DCY + DHH} L {DCX - DHW} {DCY} Z", MUTED, 1.2)
d.t(DCX, DCY + 5, "수평 분할인가", 13, INK, KR, "middle", 600)

# 갈래 선
d.arrow([(DCX - DHW, DCY), (LX + BW / 2, DCY), (LX + BW / 2, Y1 - 2)], MUTED, "ar", 1.4)
d.t(LX + BW / 2 + 40, DCY - 12, "아니다 · 수직 분할", 10, MUTED, KR, "start")
d.arrow([(DCX + DHW, DCY), (RX + BW / 2, DCY), (RX + BW / 2, Y1 - 2)], ACC, "acc", 1.4)
d.t(RX + BW / 2 + 24, DCY - 12, "그렇다", 10, ACC, KR, "start")

def box(x, y, title, sub, kind):
    c = {"n": None, "acc": ACC, "warn": WARN}[kind]
    if c:
        d.o.append(f'<rect x="{x}" y="{y}" width="{BW}" height="{BH}" rx="6" fill="{c}12" stroke="{c}" stroke-width="1.4"/>')
    else:
        d.box(x, y, BW, BH, PAPER2, RULE, 1.0, 6)
    d.t(x + BW / 2, y + 38, title, 12.5, c or INK, KR, "middle", 600)
    d.t(x + BW / 2, y + 62, sub, 10, MUTED)

box(LX, Y1, "SPA 단계와 닮는다", "온디맨드 환경이 되면 배포 전에 E2E 를 돈다", "n")
d.arrow([(LX + BW / 2, Y1 + BH), (LX + BW / 2, Y2 - 2)], MUTED, "ar", 1.3)
box(LX, Y2, "테스트가 끝나면 환경을 끈다", "임시 환경을 남기지 않는다", "n")

box(RX, Y1, "E2E 를 스테이징이나 프로덕션에서", "특정 작업의 알맞은 시점을 더 고민한다", "acc")
d.arrow([(RX + BW / 2, Y1 + BH), (RX + BW / 2, Y2 - 2)], MUTED, "ar", 1.3)
box(RX, Y2, "그러지 않으면", "모든 파이프라인이 전체 조합을 알아야 한다 · 유지하기 어렵다", "warn")

d.legend(LEGEND_Y, [("E2E 자리를 옮겨야 하는 갈래", ACC), ("그 갈래를 피하지 않았을 때", WARN)])
d.save("06-04.ci-by-split.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H, " 우측끝:", RX + BW)
