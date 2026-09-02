# 06-06 §3 — 필수 라이브러리를 검사하는 단계 (원문 Micro-Frontend-Specific Operations 첫 문단).
# 검사 대상과 두 갈래의 처리는 원문 서술 그대로다 — 알리거나, 빌드를 막고 프로세스를 실패시킨다.
# 타입 스펙: type-flowchart — 조건에 따라 갈라지는 판단 논리. 마름모가 판단, 사각형이 결과.
#           축약: 06-04.ci-by-split 의 배치를 승계하되 아니오 갈래만 결과가 둘이라 형제 상자를 붙였다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, PAPER2, RULE, KR, MONO

W = 1240
SX, SY, SW, SH = 400, 108, 440, 72
B1X, B1Y, B1W, B1H = 400, 232, 440, 80
DCX, DCY, DHW, DHH = 620, 400, 220, 60
LX, LW = 100, 400
RX, RW, RGAP = 620, 280, 40
RY = 520
BH2 = 96
LEGEND_Y = RY + BH2 + 40
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 06-06 §3",
      "필수 라이브러리를 검사하는 단계",
      "아키텍처 팀이 필수로 표시한 라이브러리가 아티팩트에 들어 있는지 파이프라인이 확인한다. 색이 붙은 것이 통과를 막는 선택지다.",
      "마름모가 판단이고 사각형이 그 결과입니다")

d.box(SX, SY, SW, SH, PAPER2, RULE, 1.0, 10)
d.t(W / 2, SY + 30, "조각 파이프라인이 돈다", 13, INK, KR, "middle", 600)
d.t(W / 2, SY + 52, "artifact build", 9, MUTED, MONO)
d.arrow([(W / 2, SY + SH), (W / 2, B1Y - 2)], MUTED, "ar", 1.4)

d.box(B1X, B1Y, B1W, B1H, PAPER2, RULE, 1.0, 6)
d.t(W / 2, B1Y + 34, "package.json 을 검사한다", 12.5, INK, KR, "middle", 600)
d.t(W / 2, B1Y + 58, "필수로 표시된 디자인 시스템 · 분석 · 관측 라이브러리", 10, MUTED)
d.arrow([(W / 2, B1Y + B1H), (W / 2, DCY - DHH - 2)], MUTED, "ar", 1.4)

d.path(f"M {DCX} {DCY - DHH} L {DCX + DHW} {DCY} L {DCX} {DCY + DHH} L {DCX - DHW} {DCY} Z", MUTED, 1.2)
d.t(DCX, DCY + 5, "알맞은 버전이 들어 있나", 13, INK, KR, "middle", 600)

# 예 — 왼쪽
d.arrow([(DCX - DHW, DCY), (LX + LW / 2, DCY), (LX + LW / 2, RY - 2)], OK, "ok", 1.4)
d.t(LX + LW / 2 + 24, DCY - 12, "그렇다", 10, OK, KR, "start")
d.o.append(f'<rect x="{LX}" y="{RY}" width="{LW}" height="{BH2}" rx="6" fill="{OK}12" stroke="{OK}" stroke-width="1.3"/>')
d.t(LX + LW / 2, RY + 38, "다음 단계로 넘어간다", 12.5, OK, KR, "middle", 600)
d.t(LX + LW / 2, RY + 62, "조직 전체에 걸쳐 아티팩트 무결성이 확인된다", 10, MUTED)

# 아니오 — 오른쪽 둘
kids = [("팀에 알린다", "고칠 기회를 준다", False), ("빌드를 막는다", "프로세스를 실패시킨다", True)]
for i, (title, sub, focal) in enumerate(kids):
    kx = RX + i * (RW + RGAP)
    d.arrow([(DCX + DHW, DCY), (kx + RW / 2, DCY), (kx + RW / 2, RY - 2)], MUTED, "ar", 1.3)
    if focal:
        d.o.append(f'<rect x="{kx}" y="{RY}" width="{RW}" height="{BH2}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(kx, RY, RW, BH2, PAPER2, RULE, 1.0, 6)
    d.t(kx + RW / 2, RY + 38, title, 12.5, ACC if focal else INK, KR, "middle", 600)
    d.t(kx + RW / 2, RY + 62, sub, 10, MUTED)
d.t(RX + RW + RGAP / 2, DCY - 12, "아니다", 10, MUTED)

d.legend(LEGEND_Y, [("통과를 막는 선택지", ACC), ("검사를 통과한 길", OK)])
d.save("06-06.mandatory-library.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H, " 우측끝:", RX + 2 * RW + RGAP)
