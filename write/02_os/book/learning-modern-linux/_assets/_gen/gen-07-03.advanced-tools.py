# 07-03 §7 — 고급 도구가 각각 스택의 어느 층을 보는가.
# 원문("Advanced Network Topics"): whois("a client for the whois directory service that you can use to
#       look up registration and user information"), DHCP("a network protocol that enables automatic
#       assignment of an IP address to a host. It's a client/server setup that removes the need for
#       manually configuring network devices" · dhcpdump 로 패킷을 훑는다),
#       NTP("for synchronizing clocks of computers over a network" · ntpq -p · "Usually, NTP works in the
#       background, managed by systemd and other daemons"),
#       tshark/wireshark("If you want to do low-level network traffic analysis—that is, you want to see
#       exactly the packets across the stack"),
#       socat("Establishes two bidirectional byte streams and enables the transferring of data between
#       the endpoint"), geoiplookup("Allows you to map an IP to a geographic region"),
#       Tunnels("An easy-to-use alternative to VPNs ... Enabled by such tools as inlets"),
#       BitTorrent("A peer-to-peer system that groups files into a package called a torrent").
# 타입 스펙: type-layers — 07-01 §2 에서 세운 네 층을 다시 세우고 그 위에 도구를 얹는다. 같은 뼈대를
#           마지막에 한 번 더 쓰는 것이 이 장을 닫는 방법이다. accent 는 층을 가로지르는 도구 하나.
#           축약: 각 층의 프로토콜 설명은 앞 두 노트에 있으므로 도구 이름만 얹었다.
# 주의: DHCP 와 NTP 는 애플리케이션 계층이다. 원문이 UDP 절에서 "There are a number of
#       application-level protocols, such as NTP and DHCP ... as well as DNS, that use UDP" 라고
#       명시하므로 L7 에 놓는다. UDP 를 쓴다는 사실이 그것을 전송 계층으로 만들지 않는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 700
d = D(W, H, "LEARNING MODERN LINUX · 07-03 §7",
      "고급 도구도 결국 네 층 어딘가를 본다",
      "저자가 고급으로 묶은 것들을 07-01 에서 세운 네 층 위에 얹은 것. 하나만 층을 가로지르는데, "
      "그것이 이 장 전체를 한 화면에 보이는 도구다.",
      "tshark 한 화면에 네 층이 다 있습니다")

LX, LW, LH, GAP, Y0 = 32, 560, 78, 10, 168
layers = [
    ("애플리케이션 · L7", "whois · DHCP(dhcpdump) · NTP(ntpq)", "등록 정보 · IP 자동 배정 · 시계 동기화", WARN),
    ("전송 · L4", "socat · 터널(inlets)", "양방향 바이트 스트림 · VPN 의 대안", OK),
    ("인터넷 · L3", "geoiplookup · BitTorrent", "IP 를 지리에 대응 · 개인 간 전송", INFO),
    ("링크 · L2", "ip link 로 고른 인터페이스", "캡처가 시작되는 자리", MUTED),
]
for i, (name, tools, note, col) in enumerate(layers):
    y = Y0 + i * (LH + GAP)
    d.box(LX, y, LW, LH, PAPER2, col, 1.2, 8)
    d.t(LX + 18, y + 26, name, 13.5, col, KR, "start", 600)
    d.t(LX + 18, y + 48, tools, 12, INK, MONO, "start")
    d.t(LX + 18, y + 68, note, 11, MUTED, KR, "start")

TX = LX + LW + 16
TH = 4 * (LH + GAP) - GAP
d.o.append(f'<rect x="{TX}" y="{Y0}" width="{W - TX - 32}" height="{TH}" rx="8" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.5"/>')
d.t(TX + (W - TX - 32) / 2, Y0 + 40, "tshark", 17, ACC, MONO, "middle", 600)
d.t(TX + (W - TX - 32) / 2, Y0 + 64, "wireshark", 12, ACC, MONO)
d.t(TX + (W - TX - 32) / 2, Y0 + 104, "네 층을", 12, ACC, KR)
d.t(TX + (W - TX - 32) / 2, Y0 + 124, "한꺼번에", 12, ACC, KR)
d.t(TX + (W - TX - 32) / 2, Y0 + 144, "가로지릅니다", 12, ACC, KR)
d.t(TX + (W - TX - 32) / 2, Y0 + 184, "-i 로 인터페이스를", 10.5, MUTED, KR)
d.t(TX + (W - TX - 32) / 2, Y0 + 202, "고르고 필터로", 10.5, MUTED, KR)
d.t(TX + (W - TX - 32) / 2, Y0 + 220, "층을 좁힙니다", 10.5, MUTED, KR)
d.t(TX + (W - TX - 32) / 2, Y0 + 258, "tcpdump 로도", 10.5, MUTED, KR)
d.t(TX + (W - TX - 32) / 2, Y0 + 276, "같은 일을 합니다", 10.5, MUTED, KR)

BY = Y0 + TH + 20
d.tone(LX, BY, W - 64, 84, ACC)
d.t(LX + 20, BY + 26, "출력 한 줄에 네 층이 다 있습니다", 13, INK, KR, "start", 600)
d.t(LX + 20, BY + 48,
    "192.168.178.40 → 185.199.109.153 이 인터넷 계층이고, 47618 → 443 이 전송 계층이며,",
    11.5, MUTED, MONO, "start")
d.t(LX + 20, BY + 68,
    "GET / HTTP/1.1 이 애플리케이션 계층, -i wlp1s0 이 링크 계층입니다.",
    11.5, MUTED, MONO, "start")

d.legend(BY + 112, [("사용자를 만나는 층", WARN), ("포트가 있는 층", OK),
                    ("주소가 정해지는 층", INFO), ("층을 가로지르는 도구", ACC)])
d.save("07-03.advanced-tools.svg")
print("ok 07-03.advanced-tools")
