# 02-04.what-changes-where — 장치를 지날 때마다 무엇이 바뀌는가
# 본문 요구: §3 은 TTL 감소와 사설 주소 유지를 따로 말하고, §5 는 MASQUERADE 를 따로 말한다.
#           그 셋이 '한 패킷이 장치를 지나며 서로 다른 자리에서 바뀌는 세 필드'라는 사실은
#           절 어디에도 한 그림으로 없다. 노드-노드 통신에서 어디서 뭘 고치는지를 편다.
# 타입 스펙: type-dp-security-matrix.md 의 값 대조 행 — 02-01.netfilter-hooks-flow 와 같은 문법이다.
#           같은 종류의 내용에 같은 문법을 쓰는 편이 두 그림을 이어 읽게 한다.
#           브리지 열이 통째로 비는 것이 이 그림의 논점 중 하나다(스위치는 아무것도 안 바꾼다).
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 700
d = D(W, H, "WHAT CHANGES WHERE",
      "장치마다 바뀌는 필드가 다르다 — 세 자리에서 하나씩",
      "ns1 에서 옆 노드까지 가는 동안 목적지 MAC 과 출발지 IP 와 TTL 이 각각 다른 자리에서 바뀝니다. "
      "브리지를 지날 때는 아무것도 바뀌지 않습니다.",
      lead="브리지는 아무것도 안 바꾸고, 라우팅과 NAT 와 송신이 하나씩 바꾼다")

BW, BH, GAP, GUT = 132, 88, 14, 88
CX = [170 + i * (BW + GAP) for i in range(6)]
NODE_CY = 288
ROWS = [("dst MAC", 428), ("src IP", 490), ("TTL", 552)]
CELL_H = 44

NODES = [("ns1 이 보냄", "veth1"), ("br0 통과", "L2 스위치"), ("ubuntu FORWARD", "라우팅 판단"),
         ("POSTROUTING", "nat · MASQUERADE"), ("eth0 로 나감", "새 ARP"), ("ubuntu2 받음", "끝")]
VALS = {
 "dst MAC": ["br0 의 MAC", "br0 의 MAC", "다음 홉 결정", "그대로", "ubuntu2 의 MAC", "ubuntu2 의 MAC"],
 "src IP":  ["10.10.1.11", "10.10.1.11", "10.10.1.11", "192.168.139.208", "그대로", "그대로"],
 "TTL":     ["64", "64", "63", "63", "63", "63"],
}
CHANGED = {("dst MAC", 4), ("src IP", 3), ("TTL", 2)}

ddx.band(d, 104, 640, "브리지 열에는 바뀌는 칸이 하나도 없다 — 스위치는 프레임을 옮길 뿐이다")

# 브리지 열을 흐리게 감싸 '아무 일도 없음'을 자리로 보인다
d.o.append(f'<rect x="{CX[1]-BW//2-8}" y="216" width="{BW+16}" height="368" rx="8" '
           f'fill="none" stroke="{SOFT}" stroke-width="1.0" stroke-dasharray="6 5"/>')

for cx, (l, s) in zip(CX, NODES):
    d.box(cx - BW // 2, NODE_CY - BH // 2, BW, BH, PAPER2, RULE, 1.1, 6)
    d.t(cx, NODE_CY - 10, ddx.fit(l, 11, BW - 14, l), 11, INK,
        MONO if all(ord(ch) < 128 or ch == '_' for ch in l) else KR, "middle", 600)
    d.t(cx, NODE_CY + 14, ddx.fit(s, 10, BW - 12, s), 10, MUTED, KR)
for a, b in zip(CX, CX[1:]):
    d.path(f"M {a+BW//2+5} {NODE_CY} L {b-BW//2-7} {NODE_CY}", MUTED, 1.4, m="ar")

for key, y in ROWS:
    d.t(GUT, y + 4, key, 11, SOFT, MONO, "end")
    for i, cx in enumerate(CX):
        hit = (key, i) in CHANGED
        c = ACC if hit else RULE
        d.o.append(f'<rect x="{cx-BW//2}" y="{y-CELL_H//2}" width="{BW}" height="{CELL_H}" rx="5" '
                   f'fill="{ACC+"14" if hit else PAPER}" stroke="{c}" stroke-width="{1.4 if hit else 1.0}"/>')
        v = VALS[key][i]
        d.t(cx, y + 4, ddx.fit(v, 10, BW - 12, f"{key}{i}"), 10, ACC if hit else MUTED,
            MONO if all(ord(ch) < 128 or ch in '.:' for ch in v) else KR)

for key, i in sorted(CHANGED, key=lambda t: t[1]):
    y = dict(ROWS)[key]
    d.t(CX[i], y - CELL_H // 2 - 8, "여기서 바뀐다", 10, ACC, KR)

d.t(36, 604, "세 필드가 각각 다른 자리에서 바뀝니다 — TTL 은 라우팅이, 출발지 IP 는 NAT 이, "
             "목적지 MAC 은 송신 직전 ARP 가 정합니다.", 12, MUTED, KR, "start")
d.t(36, 626, "IP 헤더의 목적지만 처음부터 끝까지 손대지 않습니다.", 12, MUTED, KR, "start")
d.legend(656, [("바뀌는 자리", ACC), ("아무것도 안 바뀌는 장치", SOFT)])
d.save("02-04.what-changes-where.svg")
print("ok what-changes-where")
