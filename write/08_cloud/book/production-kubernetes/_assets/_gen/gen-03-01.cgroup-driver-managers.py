# 타입 스펙: type-architecture
# 03-01.cgroup-driver-managers — cgroupfs 드라이버와 systemd 드라이버에서 cgroup 을 쓰는 관리자 수
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dd import D, INK, MUTED, SOFT, INFO, OK, WARN, KR, MONO

W, H = 1000, 468
d = D(W, H, "CGROUP DRIVER · 03-01",
      "cgroup 관리자가 둘이 되는 경우와 하나인 경우",
      "systemd 가 init 인 노드에서 kubelet 과 런타임의 cgroup 드라이버에 따라 자원을 보는 시각이 갈립니다",
      lead="kubelet 과 런타임이 cgroupfs 를 쓰면 systemd 와 나란히 관리자가 둘이 됩니다")

CARD_W, CARD_H = 190, 60
LX, RX, PW = 20, 520, 460
Y_TOP, Y_MID, Y_BAR, BAR_H = 138, 262, 372, 44


def card(x, y, name, sub, c, mono=False):
    d.tone(x, y, CARD_W, CARD_H, c, 6, "10", 1.2)
    d.t(x + CARD_W / 2, y + 26, name, 13, c, MONO if mono else KR, "middle", 600)
    d.t(x + CARD_W / 2, y + 47, sub, 12, MUTED)


def bar(x, w, c):
    d.tone(x, Y_BAR, w, BAR_H, c, 6, "10", 1.2)
    d.t(x + w / 2, Y_BAR + 27, "cgroup 파일시스템", 13, c, KR, "middle", 600)


# 왼쪽 — cgroupfs 드라이버
d.t(LX, 112, "cgroupfs 드라이버 — 관리자 둘", 14, INK, KR, "start", 600)
x1, x2 = LX + 24, LX + 24 + CARD_W + 24
card(x1, Y_TOP, "systemd", "루트 cgroup 관리자", INFO, True)
card(x2, Y_TOP, "kubelet · 런타임", "cgroup 을 직접 씀", WARN)
bar(LX + 24, 2 * CARD_W + 24, INFO)
for cx in (x1 + CARD_W / 2, x2 + CARD_W / 2):
    d.arrow([(cx, Y_TOP + CARD_H + 2), (cx, Y_BAR - 3)], MUTED, "ar", 1.5)
d.chip(LX + PW / 2, Y_MID, "자원 시각 둘", WARN, 12)

# 오른쪽 — systemd 드라이버
d.t(RX, 112, "systemd 드라이버 — 관리자 하나", 14, INK, KR, "start", 600)
cx = RX + PW / 2
card(cx - CARD_W / 2, Y_TOP, "kubelet · 런타임", "드라이버를 systemd 로 지정", INFO)
card(cx - CARD_W / 2, Y_MID - 22, "systemd", "unit 마다 cgroup 하나", INFO, True)
bar(cx - CARD_W / 2, CARD_W, INFO)
d.arrow([(cx, Y_TOP + CARD_H + 2), (cx, Y_MID - 25)], MUTED, "ar", 1.5)
d.arrow([(cx, Y_MID - 22 + CARD_H + 2), (cx, Y_BAR - 3)], MUTED, "ar", 1.5)
d.chip(cx + 120, (Y_MID - 22 + CARD_H + Y_BAR) / 2, "자원 시각 하나", OK, 12)

d.legend(428, [("cgroup 관리자", INFO), ("cgroup 을 직접 쓰는 쪽", WARN), ("시각이 하나로 모임", OK)])
d.save(str(Path(__file__).resolve().parent.parent / "03-01.cgroup-driver-managers.svg"))
print("ok 03-01.cgroup-driver-managers")
