# 04-01.layout-packet-paths — 같은 요청이 세 레이아웃에서 밖으로 나갈 때 출발지가 갈린다
# 본문 요구: "노드를 넘는 Pod 사이 통신은 셋 다 같습니다 … 갈리는 것은 클러스터 밖으로 나갈 때 …
#           Flat 은 Pod IP 그대로, Island 는 노드 IP 로 바뀌고, Isolated 는 경로 자체가 없어 프록시"
# 타입 스펙: type-swimlane — 레인 하나가 레이아웃 하나, 칸은 Pod → 노드 → 밖의 DB 순서.
#           같은 패킷(Pod 10.1.3.7)을 레인마다 다시 그려 출발지가 어디서 바뀌는지를 칸 차이로 보인다.
#           손으로 쓴 SVG 를 2026-09-15 생성기로 옮겼다.
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 532
d = D(W, H, "THREE LAYOUTS · WHAT THE OUTSIDE SEES",
      "같은 요청이 세 레이아웃에서 다르게 다닌다",
      "클러스터 안 Pod 사이 통신은 세 레이아웃이 모두 같고, 클러스터 밖으로 나갈 때 출발지 주소가 달라진다.",
      lead="안에서는 셋이 같고, 밖으로 나갈 때 DB 가 보는 출발지 주소가 갈린다")

# 공통 띠 — 클러스터 안
d.box(32, 104, 936, 56, PAPER2, INFO, 1.2, 8)
d.t(52, 138, "클러스터 안 · Pod 사이", 13, INFO, KR, "start", 600)
d.t(948, 138, "10.1.3.7 → 10.1.9.4 · 받는 쪽 출발지 10.1.3.7 · 셋 공통", 12, MUTED, KR, "end")

# 레인 머리
CX = {"lay": 112, "pod": 276, "node": 508, "db": 780}
HY = 200
d.t(CX["lay"], HY, "레이아웃", 12, SOFT, KR, "middle", 600)
d.t(CX["pod"], HY, "Pod", 12, SOFT, KR, "middle", 600)
d.t(CX["node"], HY, "노드", 12, SOFT, KR, "middle", 600)
d.t(CX["db"], HY, "클러스터 밖 DB 가 본 출발지", 12, SOFT, KR, "middle", 600)

LANE_Y0, STRIDE, BH = 216, 84, 52
POD_W, NODE_W, DB_W = 144, 168, 200


def cell(cx, y, w, text, c, fill=PAPER2, sub=None, mono=False, focal=False, dash=None, stroke=None):
    x = cx - w // 2
    if focal:
        d.tone(x, y, w, BH, ACC, 6, "14", 1.4)
    else:
        ds = f' stroke-dasharray="{dash}"' if dash else ""
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{BH}" rx="6" fill="{fill}" stroke="{stroke or c}" stroke-width="1.1"{ds}/>')
    fam = MONO if mono else KR
    if sub:
        d.t(cx, y + 22, text, 13, c, fam, "middle", 600)
        d.t(cx, y + 40, sub, 12, MUTED, KR)
    else:
        d.t(cx, y + 31, text, 13, c, fam, "middle", 600)


ROWS = [("ISOLATED", BAD), ("ISLAND", ACC), ("FLAT", OK)]
for i, (name, c) in enumerate(ROWS):
    y = LANE_Y0 + i * STRIDE
    if i: d.line(32, y - 16, 968, y - 16, RULE, 0.8)
    d.t(CX["lay"], y + 31, name, 12, c, MONO, "middle", 600)
    cell(CX["pod"], y, POD_W, "10.1.3.7", INK, mono=True, stroke=RULE)
    a1, b1 = CX["pod"] + POD_W // 2 + 8, CX["node"] - NODE_W // 2 - 10
    a2, b2 = CX["node"] + NODE_W // 2 + 8, CX["db"] - DB_W // 2 - 10
    my = y + BH // 2
    if name == "ISOLATED":
        d.path(f"M {a1} {my} L {b1} {my}", BAD, 1.5, m="bad", dash="6 5")
        cell(CX["node"], y, NODE_W, "노드에서 막힘", BAD, fill=PAPER)
        d.t(CX["db"], my + 5, "경로 없음 · 프록시 별도", 13, MUTED, KR)
    elif name == "ISLAND":
        d.arrow([(a1, my), (b1, my)], ACC, "acc", 1.5)
        cell(CX["node"], y, NODE_W, "출발지 교체", ACC, focal=True)
        d.arrow([(a2, my), (b2, my)], ACC, "acc", 1.5)
        cell(CX["db"], y, DB_W, "192.168.1.20", ACC, sub="노드 IP", mono=True)
    else:
        d.arrow([(a1, my), (b1, my)], OK, "ok", 1.5)
        cell(CX["node"], y, NODE_W, "그대로 전달", OK)
        d.arrow([(a2, my), (b2, my)], OK, "ok", 1.5)
        cell(CX["db"], y, DB_W, "10.1.3.7", OK, sub="Pod IP 그대로", mono=True)

d.legend(484, [("막힌 경로", BAD), ("출발지가 바뀌는 자리", ACC), ("주소가 보존되는 경로", OK), ("클러스터 안 공통", INFO)])
d.save("04-01.layout-packet-paths.svg")
print("ok layout-packet-paths")
