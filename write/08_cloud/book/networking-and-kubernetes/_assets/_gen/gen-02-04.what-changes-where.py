# 02-04.what-changes-where — 장치를 지날 때마다 무엇이 바뀌는가 (NAT 전후 대조)
# 본문 요구: §3 은 TTL 감소와 사설 주소 유지를 따로 말하고 §5 는 MASQUERADE 를 따로 말한다.
#           그 셋이 '한 패킷이 장치를 지나며 서로 다른 자리에서 바뀌는 필드'라는 사실이 한 장에 없었다.
# 2026-08-29 교정: 처음 판은 src IP 를 한 줄로만 두고 MASQUERADE 적용값을 적었는데,
#           §3 본문은 "POSTROUTING 칸은 아직 비어 있다"고 적고 있어 도식과 본문이 어긋났다.
#           src IP 를 NAT 없음 / MASQUERADE 두 줄로 갈라 전후를 함께 보인다.
# 타입 스펙: type-dp-security-matrix.md 의 값 대조 행 — 02-01.netfilter-hooks-flow 와 같은 문법.
#           브리지 열이 통째로 비는 것이 논점 중 하나다(스위치는 아무것도 안 바꾼다).
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 784
d = D(W, H, "WHAT CHANGES WHERE · BEFORE / AFTER NAT",
      "장치마다 바뀌는 필드가 다르고, MASQUERADE 는 한 칸만 더 바꾼다",
      "ns1 에서 옆 노드까지 가는 동안 목적지 MAC 과 TTL 이 각각 다른 자리에서 바뀝니다. "
      "출발지 IP 는 NAT 가 없으면 끝까지 그대로이고, MASQUERADE 를 걸면 POSTROUTING 에서만 바뀝니다.",
      lead="브리지는 아무것도 안 바꾸고, MASQUERADE 는 POSTROUTING 한 칸만 바꾼다")

BW, BH, GAP, GUT = 118, 88, 12, 140
CX = [211 + i * (BW + GAP) for i in range(6)]
NODE_CY = 288
ROWS = [("dst MAC", 420), ("src IP", 478), ("+ MASQUERADE", 536), ("TTL", 594)]
CELL_H = 44

NODES = [("ns1 이 보냄", "veth1"), ("br0 통과", "L2 스위치"), ("ubuntu FORWARD", "라우팅 판단"),
         ("POSTROUTING", "nat 자리"), ("eth0 로 나감", "새 ARP"), ("ubuntu2 받음", "끝")]
VALS = {
 "dst MAC": ["br0 의 MAC", "br0 의 MAC", "다음 홉 결정", "그대로", "ubuntu2 의 MAC", "ubuntu2 의 MAC"],
 "src IP": ["10.10.1.11"] * 6,
 "+ MASQUERADE": ["10.10.1.11", "10.10.1.11", "10.10.1.11",
                         "192.168.139.208", "그대로", "그대로"],
 "TTL": ["64", "64", "63", "63", "63", "63"],
}
CHANGED = {("dst MAC", 4), ("+ MASQUERADE", 3), ("TTL", 2)}

ddx.band(d, 104, 656, "브리지 열에는 바뀌는 칸이 하나도 없다 — 스위치는 프레임을 옮길 뿐이다")
d.o.append(f'<rect x="{CX[1]-BW//2-8}" y="216" width="{BW+16}" height="412" rx="8" '
           f'fill="none" stroke="{SOFT}" stroke-width="1.0" stroke-dasharray="6 5"/>')

for cx, (l, s) in zip(CX, NODES):
    d.box(cx - BW // 2, NODE_CY - BH // 2, BW, BH, PAPER2, RULE, 1.1, 6)
    d.t(cx, NODE_CY - 10, ddx.fit(l, 11, BW - 14, l), 11, INK,
        MONO if all(ord(ch) < 128 or ch == '_' for ch in l) else KR, "middle", 600)
    d.t(cx, NODE_CY + 14, ddx.fit(s, 11, BW - 12, s), 11, MUTED, KR)
for a, b in zip(CX, CX[1:]):
    d.path(f"M {a+BW//2+5} {NODE_CY} L {b-BW//2-7} {NODE_CY}", MUTED, 1.4, m="ar")

for key, y in ROWS:
    d.t(GUT, y + 4, ddx.fit(key, 11, GUT - 4, key), 11,
        ACC if "MASQ" in key else SOFT, MONO, "end")
    for i, cx in enumerate(CX):
        hit = (key, i) in CHANGED
        c = ACC if hit else RULE
        d.o.append(f'<rect x="{cx-BW//2}" y="{y-CELL_H//2}" width="{BW}" height="{CELL_H}" rx="5" '
                   f'fill="{ACC+"14" if hit else PAPER}" stroke="{c}" stroke-width="{1.4 if hit else 1.0}"/>')
        v = VALS[key][i]
        d.t(cx, y + 4, ddx.fit(v, 11, BW - 12, f"{key}{i}"), 11, ACC if hit else MUTED,
            MONO if all(ord(ch) < 128 or ch in '.:' for ch in v) else KR)

# 마지막 행의 주석을 위에 두면 바로 윗 행에 붙은 것처럼 읽힌다 — 아래로 내린다
LAST = ROWS[-1][0]
for key, i in CHANGED:
    y = dict(ROWS)[key]
    dy = CELL_H // 2 + 18 if key == LAST else -(CELL_H // 2 + 8)
    d.t(CX[i], y + dy, "여기서 바뀐다", 11, ACC, KR)

d.t(36, 690, "가운데 두 줄이 같은 경로의 NAT 전후입니다. 위는 사설 주소가 끝까지 가고, 아래는 "
             "POSTROUTING 에서 노드 주소로 바뀝니다.", 12, MUTED, KR, "start")
d.t(36, 712, "TTL 은 라우팅이, 목적지 MAC 은 송신 직전 ARP 가 정합니다. IP 헤더의 목적지만 끝까지 손대지 않습니다.",
    12, MUTED, KR, "start")
d.legend(726, [("바뀌는 자리", ACC), ("아무것도 안 바뀌는 장치", SOFT)])
d.save("02-04.what-changes-where.svg")
print("ok what-changes-where")
