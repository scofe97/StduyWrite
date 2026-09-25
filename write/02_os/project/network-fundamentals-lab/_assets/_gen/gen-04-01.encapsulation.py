# 04-01 학습 목표 뒤 — VXLAN 캡슐의 안과 밖.
# 타입 스펙: type-nested — 바깥 프레임이 안쪽 프레임을 통째로 담는 포함 관계가 본체다.
#           단계도 흐름도 아니고 "무엇이 무엇 안에 들어 있는가" 라서 nested 를 쓴다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, INFO, OK, KR, MONO

W, H = 880, 424
d = D(W, H, "NETWORK FUNDAMENTALS LAB · 04-01",
      "VXLAN 캡슐의 안과 밖",
      "원래 이더넷 프레임이 UDP 와 IP 로 감싸여 라우팅된 망을 여행한다. 중간 라우터는 바깥만 보고 안쪽은 모른다.",
      "바깥은 라우팅되는 L3 세계, 안쪽은 호스트들이 믿는 L2 세계")

# 바깥 — underlay
OX, OY, OW, OH = 24, 112, 832, 172
d.tone(OX, OY, OW, OH, INFO, 10, "08", 1.3)
d.t(OX + 20, OY + 28, "outer — underlay 를 여행하는 UDP 패킷", 14, INFO, KR, "start", 600)

FH, FY = 40, OY + 44
fields = [("EthII", 96), ("IP 10.7.x", 132), ("UDP :4789", 132), ("VXLAN vni", 124)]
fx = OX + 20
for name, w in fields:
    d.box(fx, FY, w, FH, PAPER2, RULE, 1.0, 6)
    d.t(fx + w / 2, FY + 25, name, 12, MUTED, MONO)
    fx += w + 10

# 안쪽 — overlay
IX, IY, IW, IH = OX + 20, FY + FH + 14, 792, 66
d.tone(IX, IY, IW, IH, OK, 8, "10", 1.3)
d.t(IX + 16, IY + 24, "inner — 원래 프레임 그대로", 13, OK, KR, "start", 600)

ifx = IX + 16
for name, w in [("EthII", 92), ("IP 192.168.100.x", 188), ("payload", 120)]:
    d.box(ifx, IY + 34, w, 24, PAPER2, RULE, 1.0, 4)
    d.t(ifx + w / 2, IY + 51, name, 11, MUTED, MONO)
    ifx += w + 10

d.t(IX + IW - 16, IY + 51, "ARP·브로드캐스트도 여기 실린다", 12, OK, KR, "end", 600)

# 아래 — 누가 무엇을 보나
ROW, CW2, CH2, GAP2 = 308, 404, 62, 24
d.box(OX, ROW, CW2, CH2, PAPER2, RULE, 1.0, 8)
d.t(OX + 18, ROW + 26, "중간 라우터", 13, INK, KR, "start", 600)
d.t(OX + 18, ROW + 48, "UDP 패킷 하나로만 본다 — 안은 모른다", 12, MUTED, KR, "start")

d.o.append(f'<rect x="{OX + CW2 + GAP2}" y="{ROW}" width="{CW2}" height="{CH2}" rx="8" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(OX + CW2 + GAP2 + 18, ROW + 26, "목적지 VTEP", 13, ACC, KR, "start", 600)
d.t(OX + CW2 + GAP2 + 18, ROW + 48, "vni 가 자기 것일 때만 껍질을 벗긴다", 12, MUTED, KR, "start")

d.t(24, 404, "outer 50바이트가 캡슐의 비용이다 — 14 + 20 + 8 + 8", 12, SOFT, KR, "start")
d.save("04-01.encapsulation.svg")
