# 02-04.netns-lab-topology — 실습으로 지은 배선
# 본문 요구: §2 "네임스페이스 둘, veth 쌍 둘, 브리지 하나". 그리고 실측으로 확인한 것 —
#           veth 두 끝이 서로의 인덱스를 가리키고(veth1@if3 ↔ veth1-br@if4),
#           브리지에 물리는 것은 바깥쪽 끝 하나뿐이며, 안쪽 끝은 기본 netns 에서 안 보인다.
#           본문의 코드블록 ASCII 배선도를 대체한다(계약: ASCII 초안을 남기지 않는다).
# 타입 스펙: type-architecture.md — 구성요소와 연결이고, 신뢰 경계 대신 네임스페이스 경계를
#           dashed zone 으로 묶는다(zone 3개 = 상한). 연결은 전부 순수 수평·수직이라
#           대각선도 elbow 도 없다. focal 1곳은 br0 — 이 배선을 성립시키는 자리.
#           이 책에서 architecture 는 0회 사용이었고 nested 가 33% 였다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 656
d = D(W, H, "NETNS LAB · TOPOLOGY",
      "실습으로 지은 배선 — 네임스페이스 둘을 브리지 하나로 잇는다",
      "네트워크 네임스페이스 둘에 veth 쌍의 안쪽 끝을 하나씩 넣고, 바깥쪽 끝 둘을 브리지에 물린다. "
      "veth 의 두 끝은 서로의 인덱스를 가리키며, 안쪽 끝은 기본 네임스페이스에서 보이지 않는다.",
      lead="veth 쌍이 경계를 가로지르고, 브리지가 바깥쪽 끝들을 한 스위치에 모은다")

NW, NH = 160, 72
NS_Y, BASE_Y, ETH_Y = 212, 404, 504
LX, RX, MX = 220, 780, 500

def zone(x0, y0, x1, y1, label, c):
    d.o.append(f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" rx="8" '
               f'fill="{c}08" stroke="{c}" stroke-width="1.2" stroke-dasharray="7 6"/>')
    ddx.ring_label(d, x0, y0, label, 11, c, off=16)

def node(cx, cy, name, sub, tag, focal=False):
    x, y = cx - NW // 2, cy - NH // 2
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{NW}" height="{NH}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
        tc = ACC
    else:
        d.box(x, y, NW, NH, PAPER2, RULE, 1.1, 6); tc = INK
    d.t(cx, cy - 18, ddx.fit(name, 13, NW - 16, name), 13, tc, MONO, "middle", 600)
    d.t(cx, cy + 2, ddx.fit(sub, 12, NW - 14, sub), 12, MUTED, MONO)
    d.t(cx, cy + 24, ddx.fit(tag, 11, NW - 12, tag), 11, SOFT, KR)

# 경계를 먼저(z-order: zone → 연결 → 노드)
zone(60, 144, 380, 264, "ns1", INFO)
zone(620, 144, 940, 264, "ns2", INFO)
zone(60, 336, 940, 556, "기본 네임스페이스", SOFT)

# 연결 — 전부 같은 x 또는 같은 y 라 직선이면 충분하다
for cx in (LX, RX):
    d.line(cx, NS_Y + NH // 2, cx, BASE_Y - NH // 2, INFO, 2.0)
    d.t(cx + 14, 312, "veth 쌍", 12, INFO, KR, "start")
d.line(LX + NW // 2, BASE_Y, MX - NW // 2, BASE_Y, MUTED, 1.5)
d.line(MX + NW // 2, BASE_Y, RX - NW // 2, BASE_Y, MUTED, 1.5)
d.line(MX, BASE_Y + NH // 2, MX, ETH_Y - NH // 2, MUTED, 1.5)

node(LX, NS_Y, "veth1", "10.10.1.11/24", "안쪽 끝 · index 4")
node(RX, NS_Y, "veth2", "10.10.1.12/24", "안쪽 끝 · index 7")
node(LX, BASE_Y, "veth1-br", "@if4", "바깥쪽 끝 · index 3")
node(RX, BASE_Y, "veth2-br", "@if7", "바깥쪽 끝 · index 6")
node(MX, BASE_Y, "br0", "10.10.1.1/24", "브리지 — L2 스위치", focal=True)
node(MX, ETH_Y, "eth0", "192.168.139.208/24", "바깥 · ubuntu2 방향")

d.t(36, 592, "브리지에 물리는 것은 바깥쪽 끝 하나뿐이라 bridge link 에 두 줄만 나온다. "
             "안쪽 끝은 경계 안에 남아 기본 네임스페이스의 ip link 에 보이지 않는다.", 12, MUTED, KR, "start")
d.legend(608, [("네임스페이스 경계", INFO), ("브리지 — 프레임이 여기서 갈린다", ACC)])
d.save("02-04.netns-lab-topology.svg")
print("ok netns-lab-topology")
