# 05-03 B5 — 같은 DISCOVER 가 라우터의 두 다리를 지나며 바뀌는 네 칸, 그리고 giaddr 로 서버가 범위를 고르는 분기.
# 값은 2026-09-23 학습자 캡처(b5-router-segb.pcap · b5-router-sega.pcap) 그대로다. 아래 분기의 둘째 줄은 가정이다.
# 타입 스펙: type-flowchart — 위는 한 메시지의 전후(t1 → t2), 아래는 giaddr 값에 따른 두 갈래.
#           focal 은 giaddr 칸 하나(클라이언트 쪽 다리 주소가 적히는 자리).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, INFO, PAPER2, RULE, KR, MONO

def kr(s): return KR if any("가" <= c <= "힣" for c in str(s)) else MONO

W, H = 940, 640
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 05-03 B5",
      "라우터의 두 다리에서 본 같은 DISCOVER",
      "seg-b 쪽 eth1 에서 받은 브로드캐스트 DISCOVER 를 릴레이가 목적지 MAC·출발지 IP·목적지 IP·giaddr 네 칸을 바꿔 seg-a 쪽 eth0 으로 서버에 유니캐스트한다. 서버는 giaddr 가 속한 서브넷의 범위에서 주소를 고른다. giaddr 에 서버 쪽 다리 주소를 적었다면 클라이언트는 자기 세그먼트와 다른 서브넷 주소를 받아 게이트웨이에도 닿지 못한다.",
      "릴레이가 바꾼 칸은 파랑, giaddr 는 주황 — 이 한 칸이 서버의 범위 선택을 정합니다")

# 위: 전후 카드 두 장
CW, CH, Y1 = 380, 196, 104
LX, RX = 24, W - 24 - CW
rows = [("eth.dst", "ff:ff:ff:ff:ff:ff", "서버 MAC"),
        ("ip.src", "0.0.0.0", "10.56.0.30"),
        ("ip.dst", "255.255.255.255", "10.55.0.20"),
        ("giaddr", "0.0.0.0", "10.56.0.30")]
for x, head, sub, col in ((LX, "eth1 · seg-b 에서 받은 것", "클라이언트의 원본 브로드캐스트", 1),
                          (RX, "eth0 · seg-a 로 보낸 것", "릴레이가 다시 쓴 유니캐스트", 2)):
    d.box(x, Y1, CW, CH, PAPER2, RULE, 1, 8)
    d.t(x + 20, Y1 + 30, head, 14, INK, KR, "start", 600)
    d.t(x + 20, Y1 + 52, sub, 12, MUTED, KR, "start")
    for i, r in enumerate(rows):
        y = Y1 + 88 + i * 28
        changed = col == 2
        c = (ACC if r[0] == "giaddr" else INFO) if changed else MUTED
        d.t(x + 20, y, r[0], 12, SOFT, MONO, "start")
        d.t(x + 130, y, r[col], 13, c, kr(r[col]), "start", 600 if changed else 400)
AY = Y1 + CH / 2
d.arrow([(LX + CW + 6, AY), (RX - 6, AY)], MUTED, "ar", 1.4)
d.t(W / 2, AY - 12, "릴레이", 13, INK, KR, "middle", 600)
d.t(W / 2, AY + 20, "dhcp-relay 설정", 11, MUTED, KR)

# 아래: giaddr 에 따른 두 갈래
Y2, BH = 356, 88
d.t(24, Y2 - 18, "서버가 giaddr 로 범위를 고른다", 13, MUTED, KR, "start", 600)
branches = [("실제", "giaddr 10.56.0.30", "범위 10.56.0.0/24", "10.56.0.138", "게이트웨이 10.56.0.30 · 같은 서브넷", OK),
            ("가정", "giaddr 10.55.0.30", "범위 10.55.0.0/24", "10.55.0.x", "게이트웨이 10.56.0.30 · 서브넷 밖", BAD)]
SW, GAP2 = 196, 22
for j, (tag, g, rng, addr, gw, c) in enumerate(branches):
    y = Y2 + j * (BH + 22)
    steps = [(g, tag), (rng, "서버 선택"), (addr, "클라이언트가 받는 주소"), (gw, "첫 홉")]
    for k, (val, cap) in enumerate(steps):
        x = 24 + k * (SW + GAP2)
        last = k == 3
        if last: d.tone(x, y, SW, BH, c, 6)
        else: d.box(x, y, SW, BH, PAPER2, ACC if (k == 0 and j == 0) else RULE, 1.4 if (k == 0 and j == 0) else 1, 6)
        d.t(x + SW / 2, y + 34, cap, 11, MUTED, KR)
        d.t(x + SW / 2, y + 60, val, 12 if last else 13, c if last else INK, kr(val), "middle", 600)
        if k < 3:
            d.arrow([(x + SW + 4, y + BH / 2), (x + SW + GAP2 - 4, y + BH / 2)], MUTED, "ar", 1.4)

d.legend(H - 44, [("릴레이가 바꾼 칸", INFO), ("giaddr", ACC), ("통신 가능", OK), ("첫 홉부터 막힘", BAD)])
d.save("05-03.relay-two-legs.svg")
