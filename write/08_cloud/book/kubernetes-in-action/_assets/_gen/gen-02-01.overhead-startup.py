# 02-01 §오버헤드·시작 시간 — 게스트 OS 가 있고 없고
# 본문: "게스트 OS 에 쓸 자원이 통째로 남으므로 더 많은 앱을 촘촘히 올릴 수 있습니다."
#       "VM 은 앱을 띄우기 전에 게스트 OS 를 먼저 부팅해야 하지만, 컨테이너는 그 부팅 단계가
#        없습니다 ... VM 이 수십 초 걸릴 부팅을 컨테이너는 초 이하로 끝냅니다."
# 타입 스펙: 본문에 비율 수치가 없으므로 막대 차트를 쓰면 없는 정밀도를 지어내게 된다.
#           대신 같은 크기의 자리를 세는 칸 그림으로 둔다 — 자리 개수는 본문이 말하는
#           사실이고("VM 은 앱 2개가 한계"), 눈으로 셀 수 있다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 752
d = D(W, H, "KUBERNETES IN ACTION · 02-01",
      "게스트 OS 가 자리도 먹고 시간도 먹는다",
      "VM 은 앱마다 게스트 OS 를 하나씩 얹으므로 같은 서버에 들어가는 앱 수가 줄고, 앱을 "
      "띄우기 전에 그 OS 를 부팅하는 단계가 먼저 온다. 컨테이너에는 둘 다 없다.",
      lead="오토스케일링·장애 복구처럼 새 인스턴스를 빨리 띄워야 할 때 이 차이가 벌어진다")

SLOT_W, SLOT_H, GAP = 300, 52, 8
LX, RX = 250, 690

ddx.band(d, 104, 696, "자리 개수와 단계 개수 — 둘 다 게스트 OS 하나 때문에 갈린다")

d.t(40, 186, "① 같은 서버의 자리를 무엇이 차지하나", 12, SOFT, KR, "start", 600)

def stack(cx, title, slots):
    d.t(cx, 224, title, 13, INK, KR, "middle", 600)
    for i, (label, c) in enumerate(slots):
        y = 244 + i * (SLOT_H + GAP)
        d.o.append(f'<rect x="{cx-SLOT_W//2}" y="{y}" width="{SLOT_W}" height="{SLOT_H}" rx="5" '
                   f'fill="{c}18" stroke="{c}" stroke-width="1.1"/>')
        d.t(cx, y + 32, ddx.fit(label, 11, SLOT_W - 20, label), 11, c, KR)

stack(LX, "VM 두 개로 돌릴 때", [
    ("게스트 OS 1 — 오버헤드", BAD), ("App A", OK),
    ("게스트 OS 2 — 오버헤드", BAD), ("App B", OK),
    ("호스트 OS", MUTED)])
stack(RX, "컨테이너로 돌릴 때", [
    ("App A", OK), ("App B", OK), ("App C", OK), ("App D", OK),
    ("호스트 OS — 하나뿐", MUTED)])

d.chip(LX, 562, "같은 자리에 앱은 둘", BAD, 11)
d.chip(RX, 562, "같은 자리에 앱은 넷", OK, 11)

d.t(40, 600, "② 앱이 뜨기까지 거치는 단계", 12, SOFT, KR, "start", 600)
BX = 200
ROWS = [("VM", [("게스트 OS 부팅 — 수십 초", BAD, 360), ("앱 시작", OK, 150)], "부팅이 먼저다"),
        ("컨테이너", [("앱 시작 — 초 이하", OK, 150)], "부팅 단계가 없다")]
for i, (name, steps, note) in enumerate(ROWS):
    y = 620 + i * 32
    d.t(BX - 16, y + 16, name, 11, INK, KR, "end", 600)
    x = BX
    for label, c, w in steps:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="24" rx="4" '
                   f'fill="{c}18" stroke="{c}" stroke-width="1.0"/>')
        d.t(x + w // 2, y + 16, ddx.fit(label, 10, w - 12, label), 10, c, KR)
        x += w
    d.t(x + 14, y + 16, note, 10, SOFT, KR, "start")

d.legend(712, [("게스트 OS 가 먹는 몫", BAD), ("앱에 돌아가는 몫", OK)])
d.save("02-01-overhead-startup.svg")
print("ok overhead-startup")
