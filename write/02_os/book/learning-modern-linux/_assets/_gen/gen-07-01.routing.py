# 07-01 §8 — 라우팅 테이블 한 장이 패킷의 다음 걸음을 정한다.
# 원문("Routing"): "Part of the network stack in Linux is concerned with routing—that is, deciding on a
#       per-packet basis where to send a packet. The destination could be a process on the same machine,
#       or it could be an IP address on a different machine."
#       "iptables, a widely used tool that allows you to manipulate the routing tables—for example, to
#       reroute packets on certain conditions or implement a firewall—uses netfilter to intercept and
#       manipulate packets."
#       칸 설명 — Destination("0.0.0.0 means it's unspecified or unknown, potentially sending it to the
#       gateway"), Gateway("For packets not on the same network, the gateway address"),
#       Genmask("The subnet mask used"), Flags("UG means the network is up and is a gateway"),
#       Iface("The network interface the packet is going to use").
#       실측 출력 — route -n 3행과 ip route 3행이 같은 표의 두 표기다.
# 타입 스펙: type-flowchart — 패킷 하나가 목적지에 따라 갈라지는 판정. accent 는 아무 줄에도
#           맞지 않을 때 가는 곳. 축약: iptables/netfilter 는 원문이 개요만 주므로 띠로만 표시.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 616
d = D(W, H, "LEARNING MODERN LINUX · 07-01 §8",
      "표의 어느 줄에도 맞지 않으면 게이트웨이로 간다",
      "route -n 과 ip route 는 같은 표의 두 표기다. 목적지가 표의 어느 줄에 드느냐가 "
      "그 패킷의 다음 걸음을 정한다.",
      "0.0.0.0 은 명시되지 않았다는 뜻이라 게이트웨이로 갑니다")

PX, PY, PW, PH = 32, 164, 216, 68
d.box(PX, PY, PW, PH, PAPER2, INFO, 1.2, 8)
d.t(PX + PW / 2, PY + 30, "패킷 하나", 15, INFO, KR, "middle", 600)
d.t(PX + PW / 2, PY + 52, "목적지 IP 를 들고 있다", 11.5, MUTED, KR)

RX, RW = 296, 552
rows = [
    ("192.168.178.0/24", "같은 네트워크 안", "U · wlp1s0 로 직접", OK, 0),
    ("169.254.0.0/16", "링크 로컬", "U · wlp1s0 로 직접", OK, 0),
    ("default (0.0.0.0)", "그 밖의 모든 곳", "UG · 192.168.178.1 로", ACC, 1),
]
RY0, RH2 = 164, 68
for i, (dest, when, act, col, focal) in enumerate(rows):
    y = RY0 + i * (RH2 + 12)
    if focal:
        d.o.append(f'<rect x="{RX}" y="{y}" width="{RW}" height="{RH2}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.5"/>')
    else:
        d.box(RX, y, RW, RH2, PAPER2, col, 1.2, 8)
    d.t(RX + 18, y + 28, dest, 13, col, MONO, "start", 600)
    d.t(RX + 18, y + 50, when, 11.5, MUTED, KR, "start")
    d.t(RX + RW - 18, y + 40, act, 12, INK if not focal else ACC, MONO, "end")
    d.path(f"M {PX + PW} {PY + 34} L {(PX + PW + RX) / 2} {PY + 34} "
           f"L {(PX + PW + RX) / 2} {y + 34} L {RX - 8} {y + 34}",
           col, 1.4, m="acc" if focal else "ok")

MY = 400
d.t(PX, MY - 12, "같은 표의 두 표기", 12.5, SOFT, KR, "start", 600)
for i, (title, lines) in enumerate([
        ("route -n", ["Destination  Gateway        Genmask",
                      "0.0.0.0      192.168.178.1  0.0.0.0        UG",
                      "192.168.178.0  0.0.0.0      255.255.255.0  U"]),
        ("ip route", ["default via 192.168.178.1 dev wlp1s0",
                      "169.254.0.0/16 dev wlp1s0 scope link",
                      "192.168.178.0/24 dev wlp1s0 proto kernel"])]):
    x = PX + i * 424
    d.box(x, MY, 392, 92, PAPER, RULE, 1.0, 6)
    d.t(x + 16, MY + 24, title, 12.5, INK, MONO, "start", 600)
    for j, ln in enumerate(lines):
        d.t(x + 16, MY + 46 + j * 18, ln, 10, SOFT, MONO, "start")

d.tone(PX, 512, W - 64, 44, MUTED)
d.t(PX + 20, 540,
    "이 표를 조작하는 도구가 iptables 이고, 그것이 패킷을 가로채는 데 쓰는 것이 netfilter 입니다.",
    12, MUTED, KR, "start")

d.legend(576, [("패킷", INFO), ("직접 보내는 줄", OK), ("아무 줄에도 안 맞을 때", ACC)])
d.save("07-01.routing.svg")
print("ok 07-01.routing")
