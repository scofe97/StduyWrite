# 07-01 §3 — NIC 가 바이트와 물리 신호 사이를 오가고, 이름이 위치에서 나온다.
# 원문("Network interface controller"): "The NIC provides the physical connectivity to a network through
#       either a wired standard—for example, the IEEE 802.3-2018 standard for Ethernet—or one of the many
#       wireless standards from the IEEE 802.11 family. Once part of a network, the NIC turns the digital
#       representation of the bytes you want to send into electrical or electromagnetic signals. The
#       reverse is true for the receive path, where the NIC turns whatever physical signals it receives
#       into bits and bytes that the software can deal with."
#       MAC 주소 — "a unique 48-bit identifier for hardware, used to identify your machine (to be precise,
#       the network interface). The MAC address encodes the manufacturer (of the interface) via the
#       organizationally unique identifier (OUI), usually occupying the first 24 bits."
#       이름 규칙 — "it's a wireless interface (wl) in PCI bus 1 (p1) and slot 0 (s0). This naming makes
#       the interface names more predictable. In other words, if you had two old-style interfaces (say,
#       eth0 and eth1), there was no guarantee that a reboot or adding a new card wouldn't cause Linux to
#       rename those interfaces."
#       MTU — 루프백 65,536 · 이더넷 기본 1,500(역사적 이유) · 점보 프레임 9,000.
# 타입 스펙: type-architecture — 구성요소와 그 사이의 연결. accent 는 이름이 왜 그렇게 생겼는지,
#           곧 예측 가능성을 위해 위치에서 이름을 끌어온 자리. 축약: 드라이버 계층은 상자 하나로 뭉쳤다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 620
d = D(W, H, "LEARNING MODERN LINUX · 07-01 §3",
      "NIC 가 바이트를 신호로 바꾸고, 이름은 위치에서 나온다",
      "링크 계층은 바이트와 전선과 전자기파와 드라이버의 세계다. 그 경계에 NIC 가 서 있고, "
      "인터페이스 이름은 그 NIC 가 꽂힌 자리를 그대로 적은 것이다.",
      "MAC 주소는 기계가 아니라 인터페이스를 식별합니다")

SW, SH, SY = 232, 96, 168
soft = (32, "소프트웨어", "비트와 바이트", "커널 드라이버가 다루는 형태", INFO)
d.box(soft[0], SY, SW, SH, PAPER2, soft[4], 1.2, 8)
d.t(soft[0] + SW / 2, SY + 32, soft[1], 15, soft[4], KR, "middle", 600)
d.t(soft[0] + SW / 2, SY + 56, soft[2], 12, INK, KR)
d.t(soft[0] + SW / 2, SY + 78, soft[3], 11, MUTED, KR)

NX = 324
d.box(NX, SY, SW, SH, PAPER2, OK, 1.3, 8)
d.t(NX + SW / 2, SY + 32, "NIC", 15, OK, KR, "middle", 600)
d.t(NX + SW / 2, SY + 56, "IEEE 802.3 유선", 11.5, MUTED, MONO)
d.t(NX + SW / 2, SY + 76, "IEEE 802.11 무선", 11.5, MUTED, MONO)

PX = 616
d.box(PX, SY, SW, SH, PAPER2, INFO, 1.2, 8)
d.t(PX + SW / 2, SY + 32, "물리 매체", 15, INFO, KR, "middle", 600)
d.t(PX + SW / 2, SY + 56, "전기 신호 · 전자기파", 12, INK, KR)
d.t(PX + SW / 2, SY + 78, "선과 공기", 11, MUTED, KR)

d.path(f"M {soft[0] + SW} {SY + 34} L {NX - 8} {SY + 34}", OK, 1.5, m="ok")
d.t((soft[0] + SW + NX) / 2, SY + 24, "보내는 길", 11, OK, KR)
d.path(f"M {NX + SW} {SY + 34} L {PX - 8} {SY + 34}", OK, 1.5, m="ok")
d.path(f"M {PX - 8} {SY + 74} L {NX + SW} {SY + 74}", MUTED, 1.5, m="ar")
d.t((NX + SW + PX) / 2, SY + 92, "받는 길", 11, MUTED, KR)
d.path(f"M {NX - 8} {SY + 74} L {soft[0] + SW} {SY + 74}", MUTED, 1.5, m="ar")

MY = 304
d.box(32, MY, 400, 108, PAPER2, RULE, 1.0, 8)
d.t(52, MY + 28, "MAC 주소 — 48비트", 14, INK, KR, "start", 600)
d.o.append(f'<rect x="52" y="{MY + 42}" width="180" height="26" rx="4" '
           f'fill="{INFO}22" stroke="{INFO}" stroke-width="1.1"/>')
d.t(142, MY + 60, "OUI — 앞 24비트", 11, INFO, KR)
d.o.append(f'<rect x="236" y="{MY + 42}" width="176" height="26" rx="4" '
           f'fill="{MUTED}18" stroke="{MUTED}" stroke-width="1.1"/>')
d.t(324, MY + 60, "나머지 24비트", 11, MUTED, KR)
d.t(52, MY + 88, "38:de:ad:37:32:0f — 제조사가 앞쪽에 인코딩됩니다", 11.5, SOFT, MONO, "start")

d.o.append(f'<rect x="456" y="{MY}" width="392" height="108" rx="8" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(476, MY + 28, "이름이 위치에서 나오는 이유", 14, ACC, KR, "start", 600)
for i, (part, mean) in enumerate([("wl", "무선 인터페이스"), ("p1", "PCI 버스 1"), ("s0", "슬롯 0")]):
    x = 476 + i * 124
    d.o.append(f'<rect x="{x}" y="{MY + 42}" width="108" height="26" rx="4" '
               f'fill="{ACC}20" stroke="{ACC}" stroke-width="1.1"/>')
    d.t(x + 54, MY + 60, part, 12, ACC, MONO, "middle", 600)
    d.t(x + 54, MY + 84, mean, 11.5, MUTED, KR)

BY = 444
d.tone(32, BY, W - 64, 62, MUTED)
d.t(52, BY + 26, "옛 이름 eth0 · eth1 은 재부팅하거나 카드를 꽂으면 바뀔 수 있었습니다",
    12.5, INK, KR, "start", 600)
d.t(52, BY + 48,
    "MTU 는 루프백이 65,536 이고 이더넷 기본이 1,500 입니다. 9,000 짜리 점보 프레임도 쓸 수 있습니다.",
    11.5, MUTED, KR, "start")

d.legend(536, [("소프트웨어와 물리 매체", INFO), ("경계에 선 하드웨어", OK),
               ("예측 가능하게 만든 이름", ACC)])
d.save("07-01.link-layer.svg")
print("ok 07-01.link-layer")
