# 01-03.ibgp-full-mesh — 풀메시 그래프 + AS 경계
# 본문: "트리가 아니라 풀메시", "점선 상자 하나가 AS 하나"
#        안쪽은 iBGP 풀메시, 밖으로 나가는 자리만 eBGP
# 타입 스펙: type-dependency.md — 모든 쌍이 이어진 그래프는 삼각으로 놓아야 변이 겹치지 않는다.
#           type-nested.md 의 경계 링을 AS 하나로.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER2, KR, MONO

W, H = 1000, 612
d = D(W, H, "CALICO · iBGP FULL MESH",
      "안쪽은 iBGP 풀메시, 밖으로 나가는 자리만 eBGP",
      "화살표는 한 방향으로 그렸지만 이웃 관계는 쌍방이다 — 점선 상자 하나가 AS 하나다",
      lead="이웃 관계는 쌍방이다 · 점선 상자 하나가 AS 하나")

BW, BH = 168, 96
EXT = (132, 300)
N1, N2, N3 = (430, 254), (818, 254), (624, 432)
RING = (296, 190, 664, 316)

def node(cx, cy, title, sub, tag, c=None):
    x, y = cx - BW // 2, cy - BH // 2
    d.box(x, y, BW, BH, PAPER2, c or RULE, 1.1, 6)
    d.t(cx, cy - 16, title, 13, c or INK, KR, "middle", 600)
    d.t(cx, cy + 4, ddx.fit(sub, 11, BW - 18, sub), 11, MUTED,
        MONO if all(ord(ch) < 128 or ch == '/' for ch in sub) else KR)
    d.t(cx, cy + 26, ddx.fit(tag, 10, BW - 14, tag), 10, SOFT, KR)

ddx.band(d, 104, 560, "중계가 없으니 모두가 모두와 직접 맺어야 한다")
rx, ry, rw, rh = RING
d.o.append(f'<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="8" '
           f'fill="{INFO}06" stroke="{INFO}" stroke-width="1.2" stroke-dasharray="7 6"/>')
ddx.ring_label(d, rx, ry, "AS 64512 — 클러스터 전체가 덩어리 하나", 11, INFO)

node(*EXT, "회사 라우터", "AS 65001", "남의 조직")
node(*N1, "노드 1", "10.244.1.0/24", "경계 · eBGP 도 한다", INFO)
node(*N2, "노드 2", "10.244.2.0/24", "iBGP 이웃")
node(*N3, "노드 3", "10.244.3.0/24", "iBGP 이웃")

# 풀메시 — 세 쌍 모두. 방향은 하나로 그리되 관계는 쌍방이다.
for (ax, ay), (bx, by) in [(N1, N2), (N1, N3), (N2, N3)]:
    if ay == by:
        d.line(ax + BW // 2 + 8, ay, bx - BW // 2 - 8, by, OK, 1.5)
    else:
        d.line(ax + (BW // 2 - 30) * (1 if bx > ax else -1), ay + BH // 2 + 6,
               bx + (BW // 2 - 30) * (1 if ax > bx else -1), by - BH // 2 - 6, OK, 1.5)
d.chip(624, 246, "iBGP · 세 쌍 모두", OK, 12)

d.path(f"M {EXT[0]+BW//2+8} {EXT[1]} L {N1[0]-BW//2-10} {N1[1]+22}", ACC, 1.8, m="acc")
d.t(286, 282, "eBGP", 12, ACC, MONO, "middle", 600)
d.t(286, 336, "밖으로 나가는 자리", 11, ACC, KR, "end")

d.t(36, 534, "안에서는 번호가 같아 목록이 자라지 않으니 고리를 알아볼 수 없다 — 그래서 재전달을 "
             "아예 금지하고, 중계가 없으니 풀메시가 된다", 12, MUTED, KR, "start")
d.legend(576, [("AS 경계", INFO), ("iBGP 풀메시", OK), ("밖으로 나가는 한 줄", ACC)])
d.save("01-03.ibgp-full-mesh.svg")
print("ok ibgp-full-mesh")
