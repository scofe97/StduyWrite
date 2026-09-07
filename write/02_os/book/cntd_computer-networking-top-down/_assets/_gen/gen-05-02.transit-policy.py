# 타입 스펙: type-venn — 내 백본을 지나도 되는 트래픽의 조건은 합집합이고, 바깥이 곧 무임승차다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §5.4.5 상용 ISP 의 rule of thumb
# 기하 주의: 원의 세로 범위는 cy±R 이므로, 바깥 영역 라벨은 그 밖(y < cy-R)에 두어야 원 위에 얹히지 않는다.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, BAD, OK, KR, MONO

W, H = 1000, 660
CX1, CX2, CY, R = 425, 565, 315, 115
BOX = (200, 150, 590, 330)          # x, y, w, h
assert CY - R > BOX[1] + 30, "바깥 라벨을 둘 세로 여백이 없다"

d = D(W, H, "SECTION 5.4.5 · TRANSIT POLICY",
      "나르는 조건은 합집합입니다",
      "상용 ISP 가 따르는 경험칙을 집합으로 그린 것. 출발지나 목적지 중 하나가 내 고객이면 나르고, 둘 다 아니면 내 망을 공짜로 쓰는 셈이라 나르지 않는다.",
      "광고하지 않으면 아무도 그 길로 보내지 않습니다 — 정책은 광고로 집행됩니다")

d.o.append(f'<rect x="{BOX[0]}" y="{BOX[1]}" width="{BOX[2]}" height="{BOX[3]}" rx="12" '
           f'fill="{BAD}08" stroke="{BAD}" stroke-width="1.2" stroke-dasharray="6 5"/>')
d.t(220, 180, "이 바깥은 무임승차입니다", 12, BAD, KR, "start", 600)
d.t(220, 200, "A 와 C 사이의 통과 트래픽을 내 백본이 왜 나릅니까", 11, BAD, KR, "start")

d.o.append(f'<circle cx="{CX1}" cy="{CY}" r="{R}" fill="{OK}18" stroke="{OK}" stroke-width="1.5"/>')
d.o.append(f'<circle cx="{CX2}" cy="{CY}" r="{R}" fill="{INFO}18" stroke="{INFO}" stroke-width="1.5"/>')

for cx, c, top, bot in ((368, OK, "출발지가", "내 고객"), (495, ACC, "둘 다", "내 고객"),
                        (622, INFO, "목적지가", "내 고객")):
    d.t(cx, CY - 6, top, 12, c, KR, "middle", 600)
    d.t(cx, CY + 14, bot, 12, c, KR, "middle", 600)

d.t(495, 452, "원 안쪽 세 영역은 모두 나릅니다", 11, ACC, KR)

# 다중 접속 액세스 ISP 인 X 가 하는 일
d.box(806, 160, 176, 216, PAPER2, RULE, 1.0, 9)
d.t(894, 188, "X 의 선택", 12, INK, KR, "middle", 600)
d.line(822, 202, 966, 202, RULE, 0.9)
for i, (txt, c) in enumerate([("B 와 C 두 제공자에", MUTED), ("동시에 붙어 있습니다", MUTED),
                              ("", None), ("X-C-Y 경로를 알아도", MUTED), ("B 에게 알리지 않습니다", ACC),
                              ("", None), ("그래서 B 는 Y 행을", MUTED), ("X 로 보내지 않습니다", MUTED)]):
    if txt:
        d.t(822, 228 + i * 20, txt, 11, c, KR, "start")

d.t(30, 538, "AS 사이에는 경로의 비용이라는 개념이 사실상 없습니다. AS 홉 수 말고는 값이 없고, 그마저도 로컬 선호도에 밀립니다.", 11, MUTED, KR, "start")
d.t(30, 558, "그래서 정책이 성능을 이기는 일이 흔합니다. 더 긴 경로여도 조건을 만족하는 쪽이 선택됩니다.", 11, MUTED, KR, "start")

d.legend(582, [("출발지 조건", OK), ("목적지 조건", INFO), ("나르지 않는 영역", BAD)])

out = pathlib.Path(__file__).resolve().parent.parent / "05-02.transit-policy.svg"
d.save(out)
print("→", out)
