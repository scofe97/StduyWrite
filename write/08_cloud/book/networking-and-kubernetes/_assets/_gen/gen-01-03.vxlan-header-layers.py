# 01-03.vxlan-header-layers — 중첩 헤더 + 가시 범위
# 본문: "라우터는 겉의 IP 헤더만 읽고 그 안은 들여다보지 않는다. 페이로드 해석은 자기 일이 아니다."
#        각 층이 자기 헤더만 보고 나머지를 화물로 취급한다는 성질이
#        한 층의 것을 다른 층의 화물로 위장시키는 수단이 된다
# 타입 스펙: type-layers.md — 층은 위에서 아래로 쌓고, 가시 범위는 대괄호로 끊는다.
#           높이 범위 40~72px 안에서 고정, stride 는 4 의 배수.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 592
d = D(W, H, "VXLAN · WHAT THE ROUTER READS",
      "라우터가 보는 것과 안에 든 것",
      "각 층은 자기 헤더만 보고 그 안은 화물로 취급한다 — 그래서 프레임을 화물로 위장시킬 수 있다",
      lead="각 층은 자기 헤더만 보고 그 안은 화물로 취급한다")

PX, PW = 48, 392                                   # 단면 패널
LAYERS = [(200, 48, "바깥 IP 헤더", "노드 A -> 노드 B", INFO),
          (252, 44, "UDP", "목적지 포트 4789", INFO),
          (300, 44, "VXLAN", "VNI · 논리 네트워크 번호", SOFT),
          (348, 72, "Pod A 의 L2 프레임", "Ethernet + IP + 데이터", ACC)]
BX = PX + PW + 16                                  # 대괄호 x
CH_CX, CH_W, CH_H = 786, 204, 84
CH_CY = [216, 328, 440]

ddx.band(d, 104, 536, "봉투를 열 권한이 아니라 열 이유가 없다 — 라우터의 일은 겉의 IP 까지다")
d.t(PX, 168, "봉함된 패킷의 단면", 12, SOFT, KR, "start", 600)

for y, h, title, sub, c in LAYERS:
    focal = (c == ACC)
    d.o.append(f'<rect x="{PX}" y="{y}" width="{PW}" height="{h}" rx="5" '
               f'fill="{c}{"12" if focal else "0E"}" stroke="{c}" stroke-width="{1.4 if focal else 1.1}"/>')
    d.t(PX + 16, y + (h // 2) + 1, ddx.fit(title, 12, 180, title), 12, c, KR, "start", 600)
    d.t(PX + PW - 16, y + (h // 2) + 1, ddx.fit(sub, 11, 200, sub), 11, MUTED,
        MONO if all(ord(ch) < 128 or ch in "->" for ch in sub) else KR, "end")

ddx.bracket(d, BX, 200, 296, "라우터가 읽는 부분", INFO)
ddx.bracket(d, BX, 300, 420, "여기부터 화물 — 안 본다", SOFT)

for cy, (t, s) in zip(CH_CY, [("라우터", "평범한 UDP 트래픽으로 본다"),
                              ("그래서 통과한다", "IP 라우팅 그대로"),
                              ("Pod B 가 받는다", "옆방에서 온 것과 구별 못 한다")]):
    x, y = CH_CX - CH_W // 2, cy - CH_H // 2
    c = OK if t.startswith("Pod B") else None
    d.box(x, y, CH_W, CH_H, PAPER2, c or RULE, 1.1, 6)
    d.t(CH_CX, cy - 8, t, 13, c or INK, KR, "middle", 600)
    d.t(CH_CX, cy + 14, ddx.fit(s, 11, CH_W - 20, s), 11, MUTED, KR)
for a, b in zip(CH_CY, CH_CY[1:]):
    d.path(f"M {CH_CX} {a+CH_H//2+6} L {CH_CX} {b-CH_H//2-10}", MUTED, 1.4, m="ar")

d.t(36, 508, "목적지에서 껍데기를 벗기면 원래 프레임이 그대로 나오고, 받는 Pod 는 그것이 "
             "옆자리에서 왔는지 다른 노드에서 왔는지 구별하지 못한다", 12, MUTED, KR, "start")
d.legend(552, [("라우터가 읽는다", INFO), ("도착", OK), ("화물 — 안 열린다", ACC)])
d.save("01-03.vxlan-header-layers.svg")
print("ok vxlan-header-layers")
