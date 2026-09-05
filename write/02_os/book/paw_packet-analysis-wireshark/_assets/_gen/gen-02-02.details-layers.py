# 02-02 §5 — Packet Details 창이 한 프레임을 어떤 계층 순서로 펼치는가.
# 타입 스펙: type-layers — 위아래로 쌓인 추상 수준. 맨 위 frame 은 Wireshark 만의 메타 계층이고
#           그 아래부터가 실제 TCP/IP 스택이다. focal 은 그 사실이 드러나는 frame 층 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 528
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 02-02 §5",
      "Packet Details 가 펼치는 계층",
      "선택한 프레임이 다섯 줄로 펼쳐진다. 맨 위 frame 은 선 위에 존재하지 않는 Wireshark 의 메타 계층이고, 그 아래부터가 실제로 전송된 헤더다.",
      "맨 윗줄은 프로토콜이 아닙니다 — Wireshark 가 캡처 시각과 길이를 담아 얹은 층입니다")

LX, LW, LH, Y0 = 96, 852, 64, 108
layers = [
    ("메타", "Frame",        "캡처 시각 · 프레임 길이 · 인터페이스", True),
    ("L2",  "Ethernet II",  "eth.dst · eth.src · 유니캐스트/브로드캐스트", False),
    ("L3",  "IPv4 또는 IPv6", "ip.src · ip.dst · TTL · 프로토콜 번호", False),
    ("L4",  "TCP 또는 UDP",  "포트 · 시퀀스 · Wireshark 의 SEQ/ACK 분석", False),
    ("L7",  "응용 프로토콜",  "표준 포트로 판별해 RFC 형식으로 표시", False),
]

for i, (tag, name, sub, focal) in enumerate(layers):
    y = Y0 + i * LH
    if focal:
        d.o.append(f'<rect x="{LX}" y="{y}" width="{LW}" height="{LH}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(LX, y, LW, LH, PAPER2 if i % 2 == 0 else PAPER, RULE, 1.0, 6)
    d.t(LX + 20, y + 38, tag, 11, ACC if focal else SOFT, MONO, "start", 600)
    d.t(LX + 76, y + 39, name, 15, ACC if focal else INK, KR, "start", 600)
    d.t(LX + LW - 20, y + 39, sub, 12, MUTED, KR, "end")

d.t(12, Y0 + 12, "Wireshark", 11, SOFT, KR, "start")
d.t(12, Y0 + 30, "가 얹은 층", 11, SOFT, KR, "start")
d.path(f"M 52 {Y0 + 44} V {Y0 + len(layers) * LH - 44}", SOFT, 1.2, m="soft")
d.t(12, Y0 + len(layers) * LH - 26, "선을 실제로", 11, SOFT, KR, "start")
d.t(12, Y0 + len(layers) * LH - 8, "지나간 헤더", 11, SOFT, KR, "start")

d.legend(Y0 + len(layers) * LH + 24, [("Wireshark 만의 계층", ACC)])
d.save("02-02.details-layers.svg")
