# 타입 스펙: type-architecture — GatewayClass(인프라 제공자) → Gateway(클러스터 운영자) → HTTPRoute(앱 개발자) → Service 네 객체와 참조 필드 세 개. 배정된 계층 타입 이름이 스펙 목록에 없어 구성요소·연결 타입으로 바꿨다. 포커스는 Gateway 한 칸.
# 사실 출처: Cilium Up and Running 7장 cil7.txt 줄 585-587(역할 셋), 619(io.cilium/gateway-controller), 646(my-gateway), 686(http-app-1), 817·859(172.18.255.200), 663-668(HTTP 80). docs.cilium.io v1.20 gateway-api(GatewayClass 목록)
import sys
sys.path.insert(0, ".")
from dd import D, ACC, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 330
BW, BH, GAP, X0, Y0 = 204, 128, 36, 24, 140
XS = [X0 + i * (BW + GAP) for i in range(4)]

d = D(W, H, "CILIUM UP AND RUNNING · 07-02", "Gateway API 객체와 역할",
      "세 객체가 역할별로 나뉘어 Service 까지 이어진다", "세 객체가 역할별로 나뉘어 Service 까지 이어진다")

cols = [
    ("인프라 제공자", "GatewayClass", "cilium", ["io.cilium/gateway-controller"], False),
    ("클러스터 운영자", "Gateway", "my-gateway", ["HTTP 80", "172.18.255.200"], True),
    ("앱 개발자", "HTTPRoute", "http-app-1", ["/details", "magic: foo"], False),
    ("백엔드", "Service", "details · productpage", ["9080"], False),
]
for x, (role, kind, name, facts, focal) in zip(XS, cols):
    d.chip(x + BW / 2, Y0 - 20, role, SOFT, 12)
    if focal:
        d.tone(x, Y0, BW, BH, ACC, r=6, op="14", sw=1.4)
    else:
        d.box(x, Y0, BW, BH, PAPER2, RULE, 0.9)
    col = ACC if focal else INK
    d.t(x + BW / 2, Y0 + 28, kind, 13, col, MONO, "middle", 600)
    d.t(x + BW / 2, Y0 + 54, name, 13, INK, KR if any("가" <= c <= "힣" for c in name) else MONO)
    for i, f in enumerate(facts):
        d.t(x + BW / 2, Y0 + 82 + i * 20, f, 11, MUTED, MONO)

ay = Y0 + BH + 40
cx = [x + BW / 2 for x in XS]
OFF = 30
# (출발 칸, 도착 칸, 라벨): 출발은 칸 아래에서 내려와 도착 칸 아래로 올라간다
for s, e, lab in [(1, 0, "gatewayClassName"), (2, 1, "parentRefs"), (2, 3, "backendRefs")]:
    sx = cx[s] - OFF if e < s else cx[s] + OFF
    ex = cx[e] + OFF if e < s else cx[e] - OFF
    d.arrow([(sx, Y0 + BH), (sx, ay), (ex, ay), (ex, Y0 + BH + 5)], MUTED, "ar", 1.5)
    d.t((sx + ex) / 2, ay - 8, lab, 11, MUTED, MONO)
d.save("07-02.chapter-overview.svg")
