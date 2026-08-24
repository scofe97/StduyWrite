# 02-01 §시스템 콜 경로 — 층수 차이가 곧 오버헤드 차이
# 본문: "VM 에서는 syscall 이 게스트 커널 → 하이퍼바이저 → 물리 CPU 의 세 층을 거치지만,
#        컨테이너에서는 호스트 커널 하나만 거쳐 물리 CPU 에 닿습니다. 이 층수 차이가 곧
#        오버헤드 차이입니다 — 대신 VM 은 그 층 덕분에 격리가 더 강합니다."
# 타입 스펙: type-layers.md — 층이 몇 겹인가가 요점이므로 두 스택을 나란히 세워 겹 수를 센다.
#           관례대로 층 높이를 일정하게 두고 왼쪽 여백에 방향 표시를 둔다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 682
d = D(W, H, "KUBERNETES IN ACTION · 02-01",
      "syscall 이 물리 CPU 까지 몇 겹을 지나는가",
      "VM 의 syscall 은 게스트 커널과 하이퍼바이저를 지나 물리 CPU 에 닿고, 컨테이너의 "
      "syscall 은 호스트 커널 하나만 지난다. 이 겹 수 차이가 그대로 오버헤드 차이다.",
      lead="대신 VM 은 그 겹 덕분에 격리가 더 강하다 — 겹이 값이자 비용이다")

LAYER_H, GAP = 68, 10
LX, RX, SW = 270, 700, 380

ddx.band(d, 104, 626, "겹이 많을수록 오버헤드가 크고 격리가 강하다 — 둘은 같은 축의 양끝이다")

def stack(cx, title, layers, tag):
    d.t(cx, 190, title, 13, INK, KR, "middle", 600)
    for i, (idx, name, sub, c) in enumerate(layers):
        y = 212 + i * (LAYER_H + GAP)
        d.o.append(f'<rect x="{cx-SW//2}" y="{y}" width="{SW}" height="{LAYER_H}" rx="6" '
                   f'fill="{c}12" stroke="{c}" stroke-width="1.1"/>')
        d.t(cx - SW // 2 + 16, y + 27, idx, 9, SOFT, MONO, "start")
        d.t(cx, y + 28, ddx.fit(name, 14, SW - 80, name), 14, c, KR, "middle", 600)
        d.t(cx, y + 50, ddx.fit(sub, 10, SW - 40, name), 10, SOFT, KR)
    d.chip(cx, 212 + len(layers) * (LAYER_H + GAP) + 14, tag, MUTED, 11)

stack(LX, "VM — 세 겹을 지난다", [
    ("APP", "App (VM 안)", "syscall 을 낸다", INFO),
    ("L1", "게스트 커널", "가상 CPU 명령으로 바꾼다", BAD),
    ("L2", "하이퍼바이저", "가상 → 물리로 중개한다", BAD),
    ("HW", "물리 CPU", "여기서 실제로 실행된다", MUTED)], "지나는 겹 3")

stack(RX, "컨테이너 — 한 겹만 지난다", [
    ("APP", "App (컨테이너 안)", "격리돼 있지만 그냥 프로세스다", INFO),
    ("L1", "호스트 커널 (공유)", "물리 CPU 에서 바로 실행된다", OK),
    ("HW", "물리 CPU", "여기서 실제로 실행된다", MUTED)], "지나는 겹 1")

for cx, n in ((LX, 4), (RX, 3)):
    for i in range(n - 1):
        y = 212 + i * (LAYER_H + GAP) + LAYER_H
        d.path(f"M {cx} {y+2} L {cx} {y+GAP-2}", MUTED, 1.4, m="ar")

# VM 스택 4단 + 칩이 547 까지 내려온다
d.t(36, 578, "CPU 가상화가 없다는 것이 컨테이너가 가벼운 이유이고, CPU 가상화가 있다는 것이 "
             "VM 이 강하게 격리되는 이유다.", 12, MUTED, KR, "start")
d.t(36, 602, "같은 사실의 양면이라 한쪽만 골라 가질 수 없다.", 12, MUTED, KR, "start")
d.legend(642, [("앱", INFO), ("VM 이 더 지나는 겹", BAD), ("컨테이너가 공유하는 커널", OK)])
d.save("02-01-syscall-path.svg")
print("ok syscall-path")
