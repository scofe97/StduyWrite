# 07-02 §4 — Protocol Hierarchy 창이 실제로 보여 주는 것. 원문 스크린샷의 값을 그대로 옮긴다.
# 값 출처: 원서 7장 Wireshark protocol hierarchy 절의 화면 (총 프레임 166,495개).
# 타입 스펙: type-tree — 창 자체가 트리다. 부모의 비율이 자식들로 갈라지는 모양을 그대로 세운다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, WARN, PAPER2, RULE, KR, MONO

W, H = 936, 540
COLX = [24, 168, 312, 456, 620]
COLW = [128, 128, 128, 148, 292]
NH = 38

d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 07-02 §4",
      "한 캡처의 프로토콜 계층",
      "원문 스크린샷의 값을 그대로 옮긴 것. 총 166,495 프레임이 이더넷에서 시작해 갈라지며, 백분율은 전체 프레임 대비다. 눈에 걸리는 것은 UDP 의 절반 가까이를 차지한 한 줄이다.",
      "무엇이 도는지 모르는 서버에서 가장 먼저 여는 창입니다")

LEAF_Y = [120 + i * 46 for i in range(7)]

def node(col, y, name, pct, cnt, c=None, w=None):
    x, ww = COLX[col], (w or COLW[col])
    if c: d.tone(x, y, ww, NH, c, 6)
    else: d.box(x, y, ww, NH, PAPER2, RULE, 1.0, 6)
    d.t(x + 12, y + 17, name, 11, c if c else INK, KR, "start", 600)
    d.t(x + 12, y + 32, f"{pct} · {cnt}", 11, MUTED, MONO, "start")
    return x, y, ww

def elbow(p, ch):
    px, py, pw = p; cx, cy, cw = ch
    mid = px + pw + (cx - (px + pw)) / 2
    d.arrow([(px + pw, py + NH / 2), (mid, py + NH / 2), (mid, cy + NH / 2), (cx - 4, cy + NH / 2)],
            MUTED, "ar", 1.1)

udp_y, tcp_y = (LEAF_Y[0] + LEAF_Y[4]) / 2, (LEAF_Y[5] + LEAF_Y[6]) / 2
ip_y = (udp_y + tcp_y) / 2

frame = node(0, ip_y, "Frame", "100.00%", "166,495")
eth = node(1, ip_y, "Ethernet", "100.00%", "166,495")
ip4 = node(2, ip_y, "IPv4", "99.85%", "166,243")
udp = node(3, udp_y, "UDP", "51.42%", "85,607")
tcp = node(3, tcp_y, "TCP", "48.43%", "80,630")

elbow(frame, eth); elbow(eth, ip4); elbow(ip4, udp); elbow(ip4, tcp)

UDP_KIDS = [("Packet Cable Lawful Intercept", "48.11%", "80,108", ACC),
            ("QUIC", "3.09%", "5,141", None),
            ("Domain Name Service", "0.17%", "283", None),
            ("Network Time Protocol", "0.02%", "28", None),
            ("Hypertext Transfer Protocol", "0.01%", "14", None)]
TCP_KIDS = [("Secure Sockets Layer", "27.83%", "46,335", None),
            ("Hypertext Transfer Protocol", "0.12%", "194", None)]

for i, (n, p, c, col) in enumerate(UDP_KIDS):
    elbow(udp, node(4, LEAF_Y[i], n, p, c, col))
for i, (n, p, c, col) in enumerate(TCP_KIDS):
    elbow(tcp, node(4, LEAF_Y[5 + i], n, p, c, col))

d.t(24, 452, "UDP 의 절반 가까이가 한 줄에 몰려 있고 그 아래에 Malformed Packet 2.80% 가 딸려 있습니다 — 해석기가 잘못 짚었는지부터 확인합니다",
     11, MUTED, KR, "start")

d.legend(H - 60, [("먼저 확인할 줄", ACC)])
d.save("07-02.protocol-hierarchy.svg")
