# 07-01 §5 — 32비트를 어디에서 자르느냐가 네트워크와 호스트를 가른다.
# 원문("IPv4"): "IPv4 defines unique 32-bit numbers identifying a host or process acting as an endpoint
#       in a TCP/IP communication. One way to write IPv4 addresses is to split up the 32-bit into four
#       8-bit segments separated by a period, each segment in the 0 to 255 range, called an octet."
#       저자의 예 63.32.106.149 → 00111111 / 00100000 / 01101010 / 10010101.
# 원문(CIDR): "The first part represents the network address. ... The second part defines how many bits
#       (and with that, IP addresses) fall within the address range—for example, /24."
#       "the first 24 bits (or three octets) represent the network, and the last 8 bits ... are the IP
#       addresses available for the 256 hosts (2^8). The first IP address in this CIDR range is 10.0.0.0,
#       and the last IP address is 10.0.0.255. Strictly speaking, only the addresses 10.0.0.1 to
#       10.0.0.254 can be assigned to hosts since the .0 and .255 addresses are reserved for special
#       purposes. In addition, we can say that the netmask is 255.255.255.0."
# 타입 스펙: type-nested — 큰 것 안에 작은 것이 드는 포함 관계. 32비트 전체 안에 네트워크 부분이
#           들고, 남은 자리가 호스트 몫이다. accent 는 자르는 선 그 자체.
#           축약: 옥텟 이진 표기는 저자의 예 하나만 적었다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 596
d = D(W, H, "LEARNING MODERN LINUX · 07-01 §5",
      "자르는 위치 하나가 네트워크와 호스트를 정한다",
      "IPv4 주소는 32비트 하나다. CIDR 의 뒷부분이 그 32비트를 어디에서 자를지 정하고, "
      "왼쪽이 네트워크 몫, 오른쪽이 호스트 몫이 된다.",
      "저자는 이 계산을 다 외울 필요는 없다고 적습니다")

# 위 — 옥텟 넷
OX, OW, OGAP, OY = 44, 188, 8, 160
d.t(OX, OY - 12, "32비트를 8비트씩 넷으로 — 저자의 예 63.32.106.149", 12, MUTED, KR, "start", 600)
for i, (dec, binv) in enumerate([("63", "00111111"), ("32", "00100000"),
                                 ("106", "01101010"), ("149", "10010101")]):
    x = OX + i * (OW + OGAP)
    d.box(x, OY, OW, 68, PAPER2, INFO, 1.2, 6)
    d.t(x + OW / 2, OY + 28, dec, 17, INFO, MONO, "middle", 600)
    d.t(x + OW / 2, OY + 52, binv, 12, MUTED, MONO)
    if i < 3:
        d.t(x + OW + OGAP / 2, OY + 34, ".", 17, MUTED, MONO)

# 아래 — 10.0.0.0/24 의 자르기
CY = 290
d.t(OX, CY - 12, "10.0.0.0/24 — 앞 24비트가 네트워크", 12, MUTED, KR, "start", 600)
NETW = (OW + OGAP) * 3 - OGAP
d.o.append(f'<rect x="{OX}" y="{CY}" width="{NETW}" height="72" rx="6" '
           f'fill="{OK}14" stroke="{OK}" stroke-width="1.3"/>')
d.t(OX + NETW / 2, CY + 30, "네트워크 — 24비트", 14, OK, KR, "middle", 600)
d.t(OX + NETW / 2, CY + 54, "10 . 0 . 0", 13, INK, MONO)

HX = OX + (OW + OGAP) * 3
d.box(HX, CY, OW, 72, PAPER2, WARN, 1.3, 6)
d.t(HX + OW / 2, CY + 30, "호스트 — 8비트", 13, WARN, KR, "middle", 600)
d.t(HX + OW / 2, CY + 54, "2^8 = 256 개", 12.5, INK, MONO)

d.path(f"M {HX - OGAP / 2} {CY - 6} L {HX - OGAP / 2} {CY + 78}", ACC, 2.0, dash="5 4")
d.t(HX - OGAP / 2, CY + 96, "/24 가 정하는 자리", 12, ACC, KR, "middle", 600)

BY = 412
cards = [
    ("첫 주소", "10.0.0.0", "예약", MUTED),
    ("배정 가능", "10.0.0.1 ~ 10.0.0.254", "254 개", ACC),
    ("마지막 주소", "10.0.0.255", "예약", MUTED),
    ("넷마스크", "255.255.255.0", "앞 24비트", OK),
]
CW2 = (W - 88 - 24) / 4
for i, (name, val, note, col) in enumerate(cards):
    x = OX + i * (CW2 + 8)
    focal = (col is ACC)
    if focal:
        d.o.append(f'<rect x="{x}" y="{BY}" width="{CW2}" height="76" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, BY, CW2, 76, PAPER2, col, 1.1, 6)
    d.t(x + CW2 / 2, BY + 24, name, 12, col, KR, "middle", 600)
    d.t(x + CW2 / 2, BY + 46, val, 11, INK, MONO)
    d.t(x + CW2 / 2, BY + 66, note, 11, MUTED, KR)

d.legend(524, [("주소 전체", INFO), ("네트워크 몫", OK),
               ("호스트 몫", WARN), ("실제로 쓸 수 있는 것", ACC)])
d.save("07-01.ipv4-cidr.svg")
print("ok 07-01.ipv4-cidr")
