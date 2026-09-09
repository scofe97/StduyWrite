# 01-01 §3 — 마이크로서비스가 푼 것과 새로 만든 것.
# 본문 논지: 저자의 장부는 이득 둘 · 값 하나인데, 그 장부에 *없던* 항목이 경계였다.
#           §3 표는 축별 비교를 이미 담으므로 도식은 표가 못 담는 것 — "장부 밖 항목" — 만 그린다.
# 타입 스펙: type-dp-security-matrix — 격자 문법을 장부 대조로 쓴다(선택 표의 "윗줄과 아랫줄이
#           같은 모양으로 이어진다" 용법). 아래 한 행이 장부에 없던 항목이며 focal 이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, WARN, OK, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 600
d = D(W, H, "BUILDING MICRO-FRONTENDS · 01-01 §3",
      "저자의 장부 — 이득 둘, 값 하나, 그리고 빠진 한 줄",
      "이득과 값은 저자가 명시한 항목이다. 마지막 행은 장부에 없던 항목이며 §3 실패의 원인이다.",
      "위 세 행이 저자가 적은 장부입니다. 맨 아래 행은 적히지 않았고, 그래서 값을 안 낸 채 지나갑니다")

X0, LW, VW, GAP = 40, 300, 604, 16      # 라벨 열 + 값 열
ROW_H, R0, STRIDE = 84, 116, 96
EXTRA = 40          # MISSING 행 앞 여백 — 장부 경계선과 그 라벨이 들어갈 자리

rows = [
    ("GAIN",  "인지 부하의 감소", OK,
     "서비스가 더 작고 단순한 문제를 맡는다", "모놀리스를 통째로 들여다보지 않는다"),
    ("GAIN",  "부분 확장", OK,
     "일부만 따로, 서비스마다 알맞은 방식으로", "모놀리스의 획일적 모델과 갈리는 자리"),
    ("COST",  "자동화 · 관측성 · 모니터링", WARN,
     "분산을 통제하려면 상당한 투자가 필요하다", "안 내면 분산은 이득이 아니라 부채가 된다"),
    ("MISSING", "경계를 어디에 긋는가", ACC,
     "장부에 없다 — 그래서 값을 안 낸 채 지나간다", "잘못 그으면 강결합 → 큰 진흙 공"),
]

for i, (tag, name, c, line1, line2) in enumerate(rows):
    y = R0 + i * STRIDE + (EXTRA if tag == "MISSING" else 0)
    focal = (tag == "MISSING")
    # 라벨 칸
    d.o.append(f'<rect x="{X0}" y="{y}" width="{LW}" height="{ROW_H}" rx="6" '
               f'fill="{c}12" stroke="{c}" stroke-width="{1.4 if focal else 1.1}"/>')
    d.t(X0 + 18, y + 26, tag, 9, c, MONO, "start")
    d.t(X0 + 18, y + 54, name, 14, c, KR, "start", 600)
    # 값 칸
    vx = X0 + LW + GAP
    if focal:
        d.o.append(f'<rect x="{vx}" y="{y}" width="{VW}" height="{ROW_H}" rx="6" '
                   f'fill="{ACC}08" stroke="{ACC}" stroke-width="1.4" stroke-dasharray="7 5"/>')
    else:
        d.box(vx, y, VW, ROW_H, PAPER2, RULE, 1.0, 6)
    d.t(vx + 20, y + 34, line1, 12, INK if not focal else ACC, KR, "start")
    d.t(vx + 20, y + 58, line2, 10, MUTED, KR, "start")

# 장부 경계 — 위 세 행까지가 "적힌 것"이다
LEDGER_BOT = R0 + 3 * STRIDE - 12 + 6
d.line(X0 - 12, LEDGER_BOT, X0 + LW + GAP + VW + 12, LEDGER_BOT, SOFT, 1.0, "4 4")
d.t(X0 - 12, LEDGER_BOT + 22, "여기부터는 장부에 없다", 10, SOFT, KR, "start")

d.legend(544, [("이득", OK), ("낸 값", WARN), ("장부에 없던 항목", ACC)])
d.save("01-01.gain-cost-ledger.svg")
print("h 필요:", 544 + 22 + 16, " 실제:", H)
