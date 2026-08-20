# 02-01.netns-veth-bridge — 한 장치가 두 네임스페이스에 걸친다
# 본문 요구: "veth 는 두 네임스페이스에 양 끝을 걸친 한 장치다"
# 타입 스펙: type-nested.md 의 경계 링 둘. 링 사이를 잇는 변 하나를 굵게 그어
#           '두 장치가 이어진 것'이 아니라 '한 장치의 두 끝'임을 자리로 말한다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 592
d = D(W, H, "NETNS · veth PAIR · BRIDGE",
      "veth 는 두 네임스페이스에 양 끝을 걸친 한 장치다",
      "왼쪽 링과 오른쪽 링을 잇는 굵은 선 하나가 장치 하나다. 두 장치가 연결된 것이 아니라 한 장치의 두 끝이다.",
      lead="링 둘을 잇는 굵은 선 하나가 장치 하나다 — 두 장치가 아니라 한 장치의 두 끝")

BW, BH = 176, 100
POD = (40, 236, 300, 152)
HOST = (384, 236, 576, 152)
V1, V2, BR, NIC = (190, 312), (472, 312), (668, 312), (864, 312)
OUT = (864, 470)

def box(cx, cy, t, s, tag, c=None, w=BW):
    d.box(cx - w // 2, cy - BH // 2, w, BH, PAPER2, c or RULE, 1.1, 6)
    d.t(cx, cy - 20, ddx.fit(t, 12, w - 16, t), 12, c or INK,
        MONO if all(ord(ch) < 128 or ch == '@' for ch in t) else KR, "middle", 600)
    d.t(cx, cy + 2, ddx.fit(s, 11, w - 14, s), 11, MUTED, KR)
    d.t(cx, cy + 26, ddx.fit(tag, 10, w - 12, tag), 10, SOFT, KR)

ddx.band(d, 104, 544, "Pod 가 늘면 veth 가 하나씩 늘어 브리지에 붙는다")
for (rx, ry, rw, rh), lab, c in [(POD, "Pod 네트워크 네임스페이스 — 자기 스택 한 벌", INFO),
                                 (HOST, "호스트 네트워크 네임스페이스", WARN)]:
    d.o.append(f'<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="8" '
               f'fill="{c}06" stroke="{c}" stroke-width="1.2" stroke-dasharray="7 6"/>')
    ddx.ring_label(d, rx, ry, lab, 11, c, off=16)

box(*V1, "veth1@veth2", "Pod 안에서는 eth0", "한쪽 끝", ACC, 220)
box(*V2, "veth2@veth1", "master br0", "반대쪽 끝", ACC)
box(*BR, "br0", "veth 를 모으는 스위치", "붙는 자리")
box(*NIC, "노드 NIC", "바깥으로 나가는 문", "여기부터 물리")
box(*OUT, "다른 노드", "같은 클러스터의 이웃", "Pod 간 통신 상대", INFO)

# 링 둘을 관통하는 한 장치
# 링 사이 좁은 틈에 라벨을 두면 양쪽 박스를 덮는다 — 두 링 아래로 감싸 내린다
UY = 428
d.path(f"M 250 {V1[1]+BH//2+4} L 250 {UY} L 430 {UY} L 430 {V2[1]+BH//2+4}", ACC, 2.6)
d.t(340, UY + 24, "한 장치의 두 끝 — 이름만 둘이다", 12, ACC, KR, "middle", 600)
for a, b in [(V2, BR), (BR, NIC)]:
    d.path(f"M {a[0]+BW//2+6} {a[1]} L {b[0]-BW//2-10} {b[1]}", MUTED, 1.5, m="ar")
d.path(f"M {NIC[0]} {NIC[1]+BH//2+6} L {OUT[0]} {OUT[1]-BH//2-10}", MUTED, 1.5, m="ar")
d.t(NIC[0] + 14, (NIC[1] + OUT[1]) // 2 + 4, "송신", 11, MUTED, KR, "start")

d.t(36, 500, "한쪽 끝은 Pod 안에서 eth0 로 보이고 다른 쪽 끝은 호스트에서 cali·veth 로 보인다 — "
             "이름이 둘이라 장치가 둘인 것처럼 읽히지만 하나다", 12, MUTED, KR, "start")
d.legend(560, [("Pod 네임스페이스", INFO), ("호스트 네임스페이스", WARN), ("한 장치", ACC)])
d.save("02-01.netns-veth-bridge.svg")
print("ok netns-veth-bridge")
