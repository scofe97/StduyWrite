# 타입 스펙: type-treemap — 면적 = 비중. 대규모 데이터센터 비용을 네 조각으로 나눈 부분-전체.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §6.6.1 —
#   호스트 45% · 인프라 25% · 전기료 15% · 네트워킹 15% 와 3~4 년 교체 주기 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, KR, MONO

W, H = 940, 524
d = D(W, H, "SECTION 6.6.1 · WHERE THE MONEY GOES",
      "네트워킹은 가장 큰 비용이 아닙니다",
      "대규모 데이터센터 비용에서 네트워킹은 15 퍼센트다. 그런데도 전체 비용을 낮추고 성능을 끌어올리는 열쇠는 네트워킹 혁신이라고 원문이 못박는다.",
      "비율은 원문 §6.6.1 의 수치 그대로입니다")

TX, TY, TW, TH = 24, 116, 560, 280
HOST_W = 252
d.tone(TX, TY, HOST_W - 4, TH, ACC, 6, "1E", 1.5)
d.t(TX + (HOST_W - 4) / 2, TY + TH / 2 - 20, "호스트", 14, ACC, KR, "middle", 600)
d.t(TX + (HOST_W - 4) / 2, TY + TH / 2 + 8, "45 %", 22, ACC, MONO, "middle", 600)
d.t(TX + (HOST_W - 4) / 2, TY + TH / 2 + 34, "3 ~ 4 년마다 교체합니다", 11, MUTED, KR)

RX, RW = TX + HOST_W, TW - HOST_W
for name, pct, h, sub, c in [("인프라", "25 %", 128, "변압기 · UPS · 발전기 · 냉각", INFO),
                             ("전기료", "15 %", 76, "끌어 쓰는 전력", MUTED),
                             ("네트워킹", "15 %", 76, "스위치 · 라우터 · 부하 분산기 · 외부 회선", OK)]:
    y = TY + (0 if name == "인프라" else (128 if name == "전기료" else 204))
    d.tone(RX, y, RW, h - 4, c, 6, "14", 1.1)
    d.t(RX + RW / 2, y + 26, name, 12, c, KR, "middle", 600)
    d.t(RX + RW / 2, y + 48, pct, 16, c, MONO, "middle", 600)
    d.t(RX + RW / 2, y + 68, sub, 10, MUTED, KR)

AX, AW = 624, 292
d.box(AX, 116, AW, 132, PAPER2, RULE, 1.0)
d.t(AX + 16, 140, "일벌은 호스트입니다", 11, INK, KR, "start", 600)
d.line(AX + 16, 150, AX + AW - 16, 150, RULE, 0.8)
for i, s in enumerate(["피자 상자를 닮은 블레이드입니다",
                       "랙 하나에 보통 20 ~ 40 대를 쌓습니다",
                       "CPU · 메모리 · 디스크를 갖습니다"]):
    d.t(AX + 16, 174 + i * 22, "·  " + s, 11, MUTED, KR, "start")

d.box(AX, 264, AW, 132, PAPER2, RULE, 1.0)
d.t(AX + 16, 288, "랙 꼭대기에 TOR 스위치", 11, INK, KR, "start", 600)
d.line(AX + 16, 298, AX + AW - 16, 298, RULE, 0.8)
for i, s in enumerate(["랙 안 호스트와 다른 스위치를 잇습니다",
                       "호스트는 40 또는 100 Gbps 로 붙습니다",
                       "호스트마다 내부 IP 주소를 받습니다"]):
    d.t(AX + 16, 322 + i * 22, "·  " + s, 11, MUTED, KR, "start")

d.line(24, 424, W - 48, 424, RULE, 0.8)
d.t(24, 446, "데이터센터 설계는 기업 기밀입니다. 2024 년 기준 대규모 데이터센터 건설 비용은 수억 달러에서 10 억 달러를 넘습니다.",
     11, MUTED, KR, "start")
d.t(24, 464, "장비 비용은 일회성 구매와 전력 같은 운영비를 같은 잣대로 보려고 상각한 값입니다.", 11, MUTED, KR, "start")

d.legend(484, [("가장 큰 몫", ACC), ("설비", INFO), ("성능의 열쇠", OK), ("전력", MUTED)])

out = pathlib.Path(__file__).resolve().parent.parent / "06-05.datacenter-cost.svg"
d.save(out)
print("→", out)
