# 01-01 §2 — IP 와 MAC 이 서로 다른 높이에서 맡는 일.
# 타입 스펙: type-layers — 위아래로 쌓인 두 층이 각각 주소 · 장비 · 유효 범위라는
#           같은 슬롯을 갖고, 층 사이 경계가 "구간을 넘는가"를 가른다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, INFO, KR, MONO

W, H = 880, 384
d = D(W, H, "NETWORK FUNDAMENTALS LAB · 01-01 §2",
      "주소가 둘인 이유",
      "L3 와 L2 두 층이 각각 맡는 주소 · 장비 · 유효 범위. 모든 IP 통신은 아래층 프레임에 실려 나간다.",
      "위층은 구간을 넘어 목적지를 찾고, 아래층은 구간 안에서 건넨다")

X0, BW, BH = 24, 832, 96
Y3, Y2 = 104, 248

layers = [
    (Y3, INFO, "L3 · IP 계층", "IP 주소", "라우터", "구간을 넘어 목적지를 찾는다", "10.10.10.1 — 봉투에 적힌 주소"),
    (Y2, ACC, "L2 · 이더넷 계층", "MAC 주소", "스위치", "같은 구간 안에서만 유효하다", "aa:c1:ab:… — 옆방까지 건네는 손"),
]

for y, c, name, addr, dev, scope, ex in layers:
    d.tone(X0, y, BW, BH, c, 8, "10", 1.3)
    d.t(X0 + 20, y + 30, name, 15, c, KR, "start", 600)
    d.t(X0 + 20, y + 56, f"{addr} · {dev}", 12, INK, KR, "start")
    d.t(X0 + 20, y + 78, ex, 12, MUTED, KR, "start")
    d.t(X0 + BW - 20, y + 56, scope, 12, c, KR, "end", 600)

# 층 사이 — 실려 나간다
d.path(f"M {X0 + 120} {Y3 + BH} V {Y2 - 4}", MUTED, 1.4, m="ar")
d.t(X0 + 136, Y3 + BH + 30, "모든 IP 통신은 결국 L2 프레임에 실린다", 12, SOFT, KR, "start")

d.t(X0, 368, "IP 는 아는데 MAC 을 모르면? — 그 물음이 01장 ARP 다", 12, ACC, KR, "start", 600)
d.save("01-01.two-addresses.svg")
