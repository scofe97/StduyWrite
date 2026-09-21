# 02-05.what-changes-where — 장치를 지날 때마다 무엇이 바뀌는가 (NAT 전후 대조)
# 본문 요구: §3 은 TTL 감소와 사설 주소 유지를 따로 말하고 §5 는 MASQUERADE 를 따로 말한다.
#           그 셋이 '한 패킷이 장치를 지나며 서로 다른 자리에서 바뀌는 필드'라는 사실이 한 장에 없었다.
# 2026-08-29 교정: 처음 판은 src IP 를 한 줄로만 두고 MASQUERADE 적용값을 적었는데,
#           §3 본문은 "POSTROUTING 칸은 아직 비어 있다"고 적고 있어 도식과 본문이 어긋났다.
#           src IP 를 NAT 없음 / MASQUERADE 두 줄로 갈라 전후를 함께 보인다.
# 타입 스펙: type-dp-security-matrix.md 의 값 대조 행 — 02-01.netfilter-hooks-flow 와 같은 문법.
#           브리지 열이 통째로 비는 것이 논점 중 하나다(스위치는 아무것도 안 바꾼다).
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 772
d = D(W, H, "WHAT CHANGES WHERE · BEFORE / AFTER NAT",
      "장치마다 바뀌는 필드가 다르고, MASQUERADE 는 한 칸만 더 바꾼다",
      "ns1 에서 옆 노드까지 가는 동안 목적지 MAC 과 TTL 이 각각 다른 자리에서 바뀝니다. "
      "출발지 IP 는 NAT 가 없으면 끝까지 그대로이고, MASQUERADE 를 걸면 POSTROUTING 에서만 바뀝니다.",
      lead="브리지는 아무것도 안 바꾸고, MASQUERADE 는 POSTROUTING 한 칸만 바꾼다")

BW, BH, GAP, GUT = 118, 88, 12, 140
CX = [211 + i * (BW + GAP) for i in range(6)]
NODE_CY = 288
# 행 간격 72 — '변경 지점' 라벨(11px)이 위 행 칸 바닥에 닿지 않게 통로를 28px 로 둔다(이전 58 은 14px)
ROWS = [("dst MAC", 420), ("src IP", 492), ("+ MASQUERADE", 564), ("TTL", 636)]
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

ddx.band(d, 104, 700, "브리지 열 · 바뀌는 칸 없음 · 스위치는 프레임만 옮김")
d.o.append(f'<rect x="{CX[1]-BW//2-8}" y="216" width="{BW+16}" height="452" rx="8" '
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
for key, i in sorted(CHANGED):              # set 순회는 해시 시드마다 순서가 달라 SVG 가 byte-identical 이 아니었다
    y = dict(ROWS)[key]
    dy = CELL_H // 2 + 18 if key == LAST else -(CELL_H // 2 + 8)
    d.t(CX[i], y + dy, "변경 지점", 11, ACC, KR)

# NAT 전후 두 줄과 필드별 결정 주체는 본문 §3 이 맡는다
d.legend(716, [("바뀌는 자리", ACC), ("아무것도 안 바뀌는 장치", SOFT)])
d.save("02-05.what-changes-where.svg")
print("ok what-changes-where")
