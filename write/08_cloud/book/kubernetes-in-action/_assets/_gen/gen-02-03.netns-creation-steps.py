# 02-03 §네트워크 네임스페이스 만들기 — 다섯 단계
# 본문: "각 네트워크 인터페이스는 정확히 한 네임스페이스에만 속합니다. 만들어서 → 옮기고 →
#        이름 바꾸고 → 그 안에서 프로세스를 실행합니다."
#       마지막에 프로세스는 그 네임스페이스의 eth0·lo 두 개만 본다.
# 타입 스펙: type-swimlane.md — 단계마다 *상태가 바뀌는* 것이 요점이라 절차 목록이 아니라 단계별 상태를 그린다.
#           두 네임스페이스를 두 열로 고정해 두고 인터페이스가 어느 열에 있는지만 바뀌게 하면,
#           '이동' 이 그림에서 실제로 움직임으로 보인다.
#           두 네임스페이스가 레인이고 다섯 단계가 행이다. ③ 에서 인터페이스 둘이 왼쪽 레인에서
#           오른쪽 레인으로 건너가는 화살표가 이 절차의 전부라, 정본이 "레인 경계를 넘는 화살표가
#           가장 중요한 간선" 이라 한 조건에 맞는다. 레인이 팀이 아니라 네임스페이스이고 세로로
#           서 있다는 점이 정본과 다르다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 700
d = D(W, H, "KUBERNETES IN ACTION · 02-03",
      "인터페이스는 한 네임스페이스에만 속한다 — 그래서 옮긴다",
      "기본 네임스페이스에 두 개를 만들고, 새 네임스페이스로 옮기고, 표준 이름으로 바꾼 뒤, "
      "그 안에서 프로세스를 실행한다. 프로세스는 그 두 개만 본다.",
      lead="네트워크 인터페이스만 봐서는 컨테이너인지 VM 인지 베어메탈인지 구별할 수 없다")

# 설명이 들어갈 열(40~311)을 왼쪽에 먼저 확보하고 그 오른쪽부터 두 네임스페이스를 둔다.
# 설명을 상자 위에 겹쳐 쓰면 가려서 안 읽힌다.
LX, RX, CW = 470, 800, 260
ROW_Y = [216, 302, 388, 474, 560]
BH = 62

ddx.band(d, 104, 644, "왼쪽 열에 있던 두 개가 오른쪽 열로 넘어가는 것이 이 절차의 전부다")

d.t(LX, 196, "기본 네임스페이스 (호스트)", 11, SOFT, KR)
d.t(RX, 196, "새 네임스페이스 (컨테이너용)", 11, SOFT, KR)

STEPS = [
    ("①", "기본 네임스페이스에 두 개를 만든다",
     ["eth0", "lo", "ethAA", "loAA"], [], None),
    ("②", "새 네임스페이스를 만든다 — 아직 비어 있다",
     ["eth0", "lo", "ethAA", "loAA"], [], "비어 있음"),
    ("③", "ethAA·loAA 를 새 네임스페이스로 옮긴다",
     ["eth0", "lo"], ["ethAA", "loAA"], None),
    ("④", "새 네임스페이스에서 표준 이름으로 바꾼다",
     ["eth0", "lo"], ["eth0", "lo"], None),
    ("⑤", "그 안에서 프로세스를 실행한다",
     ["eth0", "lo"], ["eth0", "lo"], "프로세스는 이 둘만 본다"),
]

def cell(cx, cy, items, c, note=None):
    d.box(cx - CW // 2, cy - BH // 2, CW, BH, PAPER2, c, 1.1, 6)
    if items:
        n = len(items)
        w = (CW - 24 - (n - 1) * 8) // n
        for i, nm in enumerate(items):
            x = cx - CW // 2 + 12 + i * (w + 8)
            new = nm in ("ethAA", "loAA")
            cc = ACC if new else c
            d.o.append(f'<rect x="{x}" y="{cy-16}" width="{w}" height="32" rx="4" '
                       f'fill="{cc}18" stroke="{cc}" stroke-width="1.0"/>')
            d.t(x + w // 2, cy + 5, nm, 10, cc, MONO)
    if note:
        d.t(cx, cy + 5, note, 11, SOFT, KR)

for (num, desc, left, right, note), y in zip(STEPS, ROW_Y):
    d.chip(56, y - 14, num, ACC, 11)
    d.t(84, y - 10, ddx.fit(desc, 11, 240, desc), 11, INK, KR, "start", 600)
    if note and right:
        d.t(84, y + 12, note, 10, SOFT, KR, "start")
    cell(LX, y, left, INFO)
    if right or note:
        cell(RX, y, right, OK, note if not right else None)

d.path(f"M {LX+CW//2+6} {ROW_Y[2]} L {RX-CW//2-10} {ROW_Y[2]}", ACC, 1.8, m="acc")
# 칩은 두 열 사이 코리도어(600~670) 한가운데에 — 열을 옮기면 이 값도 따라 옮긴다.
# 칩이 상자 *안*에 완전히 들어가면 dd-lint 는 잡지 않는다(테두리를 넘어야 잡는다).
d.chip((LX + CW // 2 + RX - CW // 2) // 2, ROW_Y[2], "이동", ACC, 11)

d.t(36, 604, "이름은 네임스페이스마다 고유하기만 하면 되므로, 옮긴 뒤 표준 이름 eth0·lo 로 바꿀 수 있다.",
     12, MUTED, KR, "start")
d.legend(660, [("기본 네임스페이스", INFO), ("새 네임스페이스", OK), ("새로 만들어 옮기는 것", ACC)])
d.save("02-03-netns-creation-steps.svg")
print("ok netns-creation-steps")
