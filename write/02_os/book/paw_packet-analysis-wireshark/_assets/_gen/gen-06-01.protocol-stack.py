# 06-01 §4 — 802.11 이 이더넷 자리에 들어앉는 방식. 원문: "802.11 QoS 데이터 프레임 위에
# LLC 헤더가 따라오며, 이것이 monitor 모드에서 기대되는 모습이다."
# 타입 스펙: type-layers — 위아래로 쌓인 추상 수준. focal 은 이더넷 대신 들어앉은 층 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 584
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 06-01 §4",
      "802.11 이 들어앉는 자리",
      "유선 캡처에서 이더넷이 있던 자리에 802.11 MAC 과 LLC 가 들어온다. 위층은 그대로이므로 IP 이상은 유선 캡처와 같게 읽힌다.",
      "monitor 모드가 아니면 어댑터가 이 두 층을 가짜 이더넷 헤더로 바꿔 올려 줍니다")

LX, LW, LH, Y0 = 96, 852, 64, 108
layers = [
    ("L7", "응용 프로토콜",      "HTTP · DNS — 유선과 같습니다", False),
    ("L4", "TCP 또는 UDP",      "유선과 같습니다", False),
    ("L3", "IPv4 또는 IPv6",     "유선과 같습니다", False),
    ("L2b", "LLC",              "802.11 프레임 뒤에 따라옵니다", False),
    ("L2a", "802.11 MAC",       "이더넷이 있던 자리 · wlan", True),
    ("L1", "802.11 PHY",        "802.11a/b/… · radiotap 헤더", False),
]
for i, (tag, name, sub, focal) in enumerate(layers):
    y = Y0 + i * LH
    if focal:
        d.o.append(f'<rect x="{LX}" y="{y}" width="{LW}" height="{LH}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(LX, y, LW, LH, PAPER2 if i % 2 == 0 else PAPER, RULE, 1.0, 6)
    d.t(LX + 20, y + 38, tag, 9, ACC if focal else SOFT, MONO, "start", 600)
    d.t(LX + 76, y + 39, name, 15, ACC if focal else INK, KR, "start", 600)
    d.t(LX + LW - 20, y + 39, sub, 12, MUTED, KR, "end")

d.t(12, Y0 + 12, "유선과", 11, SOFT, KR, "start")
d.t(12, Y0 + 30, "같은 층", 11, SOFT, KR, "start")
d.path(f"M 52 {Y0 + 44} V {Y0 + len(layers) * LH - 44}", SOFT, 1.2, m="soft")
d.t(12, Y0 + len(layers) * LH - 26, "무선에서만", 11, SOFT, KR, "start")
d.t(12, Y0 + len(layers) * LH - 8, "바뀌는 층", 11, SOFT, KR, "start")

d.legend(Y0 + len(layers) * LH + 24, [("이더넷 대신 들어앉는 층", ACC)])
d.save("06-01.protocol-stack.svg")
