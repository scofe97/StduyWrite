# 03-01.stack-count-evolution — 세대마다 TCP/IP 스택이 몇 개였나
# 본문 요구: "운영체제가 하나면 TCP/IP 스택도 하나이고 … 팀마다 자기 게스트 OS와 네트워크
#           스택 … 컨테이너마다 자기 네트워크 스택을 가지면서도 게스트 OS 없이" — 절 제목이
#           곧 축이므로 행을 그 축으로 두고 세대를 열로 놓는다.
# 타입 스펙: 비교 행렬. 공식 없는 타입이라 stride 로 배치.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, WARN, INFO, PAPER2, KR, MONO

W, H = 1000, 560
d = D(W, H, "BARE METAL → VM → CONTAINER",
      "세대마다 TCP/IP 스택이 몇 개였나",
      "스택이 하나뿐이라 포트를 나눠 쓰던 시절에서, 게스트 OS 없이 컨테이너마다 스택을 갖는 데까지의 변화.",
      lead="포트 충돌은 스택이 하나였기 때문이고, 그 뒤 세대는 스택 수를 늘려 그것을 풀었다")

LX, LW, CX, CW, RH, GAP = 32, 176, [224, 480, 736], 240, 64, 8
ROWS_Y = [172 + i * (RH + GAP) for i in range(4)]      # 172 244 316 388
GENS = ["베어메탈", "하이퍼바이저", "컨테이너"]
AXES = ["운영체제", "TCP/IP 스택", "8080 포트", "남는 문제"]
CELLS = [
    ["호스트 OS 하나", "게스트 OS 여러 개", "게스트 OS 없음"],
    ["1개", "게스트마다 1개", "컨테이너마다 1개"],
    ["앱 하나만 차지", "A팀도 B팀도 8080", "컨테이너마다 따로"],
    ["라이브러리 · 배포", "라이브러리 · 배포", "이 자리를 겨냥한다"],
]
FOCAL = (1, 2)   # 스택 행 × 컨테이너 열 — 절 제목이 묻는 값

for cx, g in zip(CX, GENS):
    d.t(cx + CW // 2, 148, g, 12, SOFT, KR, "middle", 600)

for r, (y, axis) in enumerate(zip(ROWS_Y, AXES)):
    d.box(LX, y, LW, RH, PAPER2, RULE, 0.9, 6)
    d.t(LX + 16, y + 38, ddx.fit(axis, 12, LW - 32, axis), 12, MUTED, KR, "start", 600)
    for c, cx in enumerate(CX):
        txt = CELLS[r][c]
        if (r, c) == FOCAL:
            d.tone(cx, y, CW, RH, ACC, 6, "12", 1.4); col = ACC
        else:
            col = WARN if (r == 2 and c == 0) else INFO
            d.box(cx, y, CW, RH, PAPER2, RULE, 0.9, 6)
        d.t(cx + CW // 2, y + 38, ddx.fit(txt, 12, CW - 24, txt), 12, col, KR)

d.t(LX + 4, 484, "컨테이너는 스택을 여럿 갖는 이점은 남기고 게스트 OS 라는 값은 치르지 않는다 — 그 자리가 이 절의 결론이다",
    12, MUTED, KR, "start")
d.legend(496, [("사실", INFO), ("충돌이 나던 자리", WARN), ("절 제목이 묻는 값", ACC)])
d.save("03-01.stack-count-evolution.svg")
print("ok stack-count-evolution")
