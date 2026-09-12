# 04-02 §5 — 원문의 망 중립성 곁상자. 명령 이전의 위반 사례 둘(2005·2007)과 FCC 명령의 세 시점(2015·2017·2024)을 시간 위에 놓는다.
# 연도와 사건은 본문에 적힌 그대로다. 간격은 실제 연도에 비례한다 — 눈금 간격이 곧 논지라 폭 1000 을 쓴다.
# 타입 스펙: type-timeline — 사건이 시간 위에 놓인다. 기준선 위 원, 라벨은 위아래로 번갈아, 이정표에 focal.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 520
BY = 280
def xp(year): return 100 + (year - 2004) * 40

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 04-02 §5",
      "밝은 선은 그어졌다 지워졌다 다시 그어졌습니다",
      "원문 망 중립성 곁상자의 사건들. 명령 이전의 위반 사례 둘과, 2015년 FCC 명령이 2017년에 뒤집혔다가 2024년에 상당 부분 복원되기까지.",
      "간격은 실제 연도에 비례합니다")

d.line(xp(2004), BY, xp(2025), BY, MUTED, 1.0)
for y in range(2005, 2026, 5):
    d.line(xp(y), BY - 6, xp(y), BY + 6, MUTED, 1.0)
    d.t(xp(y), BY + 26, str(y), 12, MUTED, MONO)

EV = [(2005, False, "ISP 가 경쟁 VoIP 를 막다가 중단", "명령 이전의 위반 사례", "start", 108),
      (2007, True,  "TCP RST 를 위조해 BitTorrent 차단", "명령 이전의 위반 사례", "middle", None),
      (2015, False, "FCC 명령 — 차단·스로틀링·유료 우선처리 금지", "세 밝은 선", "middle", None),
      (2017, True,  "명령이 뒤집힘", "2017년 명령", "middle", None),
      (2024, False, "상당 부분 복원 · 통신 서비스로 재분류", "광대역 = 통신 서비스", "end", 952)]

for year, above, lab, sub, anchor, lx in EV:
    x = xp(year)
    focal = year == 2015
    c = ACC if focal else MUTED
    r = 6 if focal else 4
    ly = BY - 44 if above else BY + 60
    d.line(x, BY - r - 2 if above else BY + r + 2, x, ly + 6 if above else ly - 16, RULE, 1.0)
    tx = lx if lx else x
    d.t(tx, ly - 8 if above else ly + 4, lab, 13, ACC if focal else INK, KR, anchor, 600)
    d.t(tx, ly + 10 if above else ly + 22, sub, 12, SOFT, KR, anchor)
    d.o.append(f'<circle cx="{x}" cy="{BY}" r="{r}" fill="{c}"/>')

d.t(24, 420, "스케줄링은 순서를 정하는 힘이고, 그 힘을 누가 쥐느냐는 기술이 아니라 정책과 법이 정합니다.", 13, MUTED, KR, "start")
d.t(24, 442, "원문의 말대로 미국에서도 다른 곳에서도 망 중립성의 마지막 장은 아직 쓰이지 않았습니다.", 13, SOFT, KR, "start")

d.legend(H - 44, [("밝은 선이 그어진 해", ACC), ("사건", MUTED)])
d.save("04-02.net-neutrality.svg")
