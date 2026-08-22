# 04-02.kube-proxy-iptables-chains — ClusterIP 가 Pod 주소로 바뀌기까지
# 본문 요구: 네 단계 — 도착 / 진입 체인 / 서비스 체인 / 엔드포인트 둘로 갈림
# 타입 스펙: type-flowchart.md — 마지막에서 둘로 갈리므로 체인 셋 + 부채꼴 둘.
#           목적지가 실제로 바뀌는 자리에만 focal.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 632
d = D(W, H, "kube-proxy · ClusterIP TO POD",
      "ClusterIP 로 온 패킷이 실제 Pod 주소로 바뀌기까지의 체인",
      "앞의 세 체인은 어디로 갈지만 고르고, 목적지를 실제로 바꾸는 것은 마지막 엔드포인트 체인이다.",
      lead="앞의 셋은 고르기만 하고, 목적지를 바꾸는 것은 마지막 하나다")

BW, BH, GAP = 160, 108, 28
EP_W = 296
CX = [40 + BW // 2 + i * (BW + GAP) for i in range(3)]           # 120 308 496
EP_X, EP_Y = 812, (280, 430)
CY = 300

def box(cx, cy, t, s, tag, c=None, focal=False, w=BW):
    x, y = cx - w // 2, cy - BH // 2
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{BH}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>'); tc = ACC
    else:
        d.box(x, y, w, BH, PAPER2, c or RULE, 1.1, 6); tc = c or INK
    d.t(cx, cy - 22, ddx.fit(t, 13, w - 18, t), 13, tc, KR, "middle", 600)
    d.t(cx, cy + 0, ddx.fit(s, 11, w - 16, s), 11, MUTED,
        MONO if all(ord(ch) < 128 or ch in ':.…-' for ch in s) else KR)
    d.t(cx, cy + 26, ddx.fit(tag, 10, w - 14, tag), 10, SOFT, KR)

ddx.band(d, 104, 568, "확률 규칙은 서비스 체인에 있고, 주소를 바꾸는 DNAT 는 그 아래에 있다")
for cx, s in zip(CX + [EP_X], ["① 도착", "② 진입 체인", "③ 서비스 체인", "④ 엔드포인트 체인"]):
    d.t(cx, 196, s, 12, SOFT, KR, "middle", 600)

box(CX[0], CY, "패킷", "10.96.0.10:53", "kube-dns ClusterIP", INFO)
box(CX[1], CY, "진입 체인", "KUBE-SERVICES", "밖 출발지면 MASQ 표시")
box(CX[2], CY, "서비스 체인", "KUBE-SVC-TCOU7…", "확률 규칙이 여기")
box(EP_X, EP_Y[0], "엔드포인트 A", "DNAT 10.0.1.141:53", "먼저 평가되는 규칙", focal=True, w=EP_W)
box(EP_X, EP_Y[1], "엔드포인트 B", "DNAT 다른 CoreDNS", "앞에서 안 걸린 나머지", focal=True, w=EP_W)

for i, lab in enumerate(["도착", "매칭"]):
    a, b = CX[i] + BW // 2, CX[i + 1] - BW // 2
    d.path(f"M {a+6} {CY} L {b-10} {CY}", MUTED, 1.5, m="ar")
    d.t((a + b) // 2, CY - 16, ddx.fit(lab, 10, GAP - 4, lab), 10, MUTED, KR)
# 부채꼴 — 통로가 88px 뿐이라 줄기를 세우면 라벨 자리가 없어진다. 서비스 체인의
# 오른쪽 변 두 지점에서 따로 나간다. 엔드포인트 A(280)는 체인 상자의 y 범위
# (246~354) 안이라 곧은 가로 한 줄이면 되고, B 만 x=620 에서 한 번 꺾는다.
# 라벨은 화살촉 x(654)에 오른쪽을 맞춰 세로 구간(620·y 340~430)을 비껴 앉는다.
A_X, B_X = CX[2] + BW // 2 + 6, EP_X - EP_W // 2 - 10
d.path(f"M {A_X} {EP_Y[0]} L {B_X} {EP_Y[0]}", ACC, 1.5, m="acc")
d.path(f"M {A_X} {CY+40} L 620 {CY+40} L 620 {EP_Y[1]} L {B_X} {EP_Y[1]}", ACC, 1.5, m="acc")
d.t(B_X, EP_Y[0] - 12, ddx.fit("확률 0.5", 10, B_X - A_X - 4, "fan 확률 0.5"), 10, ACC, KR, "end")
d.t(B_X, EP_Y[1] + 16, ddx.fit("나머지 전부", 10, B_X - A_X - 4, "fan 나머지 전부"), 10, ACC, KR, "end")

d.t(36, 540, "확률은 서비스 체인이 고르고, 고른 뒤 목적지를 실제로 바꾸는 것은 엔드포인트 체인의 DNAT 다",
     12, MUTED, KR, "start")
d.legend(584, [("들어오는 주소", INFO), ("목적지가 바뀌는 자리", ACC)])
d.save("04-02.kube-proxy-iptables-chains.svg")
print("ok kube-proxy-iptables-chains")
