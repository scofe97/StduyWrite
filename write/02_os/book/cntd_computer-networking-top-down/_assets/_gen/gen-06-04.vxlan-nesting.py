# 타입 스펙: type-nested — 담기는 관계. 바깥 상자가 안쪽 상자를 통째로 페이로드로 삼는다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §6.5.2 Figure 6.30 —
#   서니베일과 방갈로르 세그먼트, VTEP 두 끝, 24 비트 VNI 와 1600 만이라는 수치 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, KR, MONO

W, H = 1000, 530
d = D(W, H, "SECTION 6.5.2 · VXLAN",
      "이더넷 프레임을 UDP 에 담아 IP 로 나릅니다",
      "서니베일의 호스트가 방갈로르의 MAC 주소로 보낸 이더넷 프레임이, VTEP 두 끝 사이 터널을 지나 그대로 도착한다.",
      "구성과 수치는 원문 §6.5.2 · Figure 6.30 그대로입니다")

d.box(40, 116, 240, 108, PAPER2, f"{OK}55", 1.2, 7)
d.t(160, 142, "서니베일 이더넷", 11, OK, KR, "middle", 600)
d.t(160, 166, "호스트 A", 12, INK, KR, "middle", 600)
d.t(160, 190, "목적지 MAC 은 호스트 B", 10, MUTED, KR)
d.t(160, 210, "VTEP x", 11, OK, MONO)

d.box(720, 116, 240, 108, PAPER2, f"{OK}55", 1.2, 7)
d.t(840, 142, "방갈로르 이더넷", 11, OK, KR, "middle", 600)
d.t(840, 166, "호스트 B", 12, INK, KR, "middle", 600)
d.t(840, 190, "원래 프레임 그대로 받습니다", 10, MUTED, KR)
d.t(840, 210, "VTEP y", 11, OK, MONO)

d.tone(304, 116, 392, 108, INFO, 7, "0E", 1.1)
d.t(500, 142, "IP 망 — 안에 무엇이 든지 모릅니다", 11, INFO, KR, "middle", 600)
d.t(500, 178, "VTEP y 를 목적지로 하는", 11, MUTED, KR)
d.t(500, 198, "평범한 IP 데이터그램 하나로 보입니다", 11, MUTED, KR)

d.path("M 284 170 L 300 170", OK, 1.4, m="ok")
d.path("M 700 170 L 716 170", OK, 1.4, m="ok")

NEST = [
    (40, 264, 920, 168, "IP 데이터그램 — 목적지는 VTEP y", INFO),
    (80, 300, 840, 116, "UDP 데이터그램", INFO),
    (120, 336, 760, 64, "VXLAN 헤더 + 원래 이더넷 프레임 전체", ACC),
]
for x, y, w, h, label, c in NEST:
    d.tone(x, y, w, h, c, 7, "1E" if c is ACC else "10", 1.5 if c is ACC else 1.1)
    d.t(x + w / 2, y + 24, label, 11, c, KR, "middle", 600)
d.t(500, 380, "출발지 MAC A · 목적지 MAC B 가 그대로 들어 있습니다", 11, MUTED, KR)

d.line(24, 452, W - 48, 452, RULE, 0.8)
d.t(24, 472, "VXLAN 헤더의 24 비트 VNI 가 확장 LAN 마다 1600 만 개의 VXLAN 을 식별합니다. "
             "802.1Q VLAN 이 12 비트 식별자로 4,096 개에 묶인 것과 대비됩니다.", 11, MUTED, KR, "start")

d.legend(490, [("바깥이 통째로 삼키는 것", ACC), ("감싸는 계층", INFO), ("두 이더넷 세그먼트", OK)])

out = pathlib.Path(__file__).resolve().parent.parent / "06-04.vxlan-nesting.svg"
d.save(out)
print("→", out)
