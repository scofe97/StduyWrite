# 02-04 §3 — CDN 의 두 배치 철학. 같은 경로 위에서 클러스터를 어디에 놓느냐가 갈린다.
# 규모(수천 곳 대 수십 곳)와 각각의 대가는 원문 2.5.3 의 서술 그대로다.
# 타입 스펙: type-architecture — 구성 요소와 그 사이 관계. zone 으로 두 철학을 묶고 클러스터 위치에 강조를 준다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 596
NW, NH = 152, 58
XS = [126, 322, 518, 714, 900]
# cluster_i 는 CHAIN 에서 클러스터가 놓이는 칸. Enter Deep 은 원문 그대로 *접속 ISP* 안이다
# ("deploying server clusters in access ISPs all over the world").
ZONES = [("ENTER DEEP · Akamai · 수천 곳", 146, 1), ("BRING HOME · Limelight 등 · 수십 곳", 350, 3)]

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 02-04 §3",
      "어디까지 들어갈 것인가",
      "같은 경로 위에서 CDN 클러스터를 접속 ISP 안에 두느냐 IXP 에 두느냐. 깊이 들어갈수록 사용자에게 가깝고 운영할 곳이 많아진다.",
      "강조된 상자가 클러스터가 놓이는 자리입니다")

CHAIN = ["사용자", "접속 ISP", "지역 ISP", "IXP", "콘텐츠 원본"]

for zi, (zname, zy, cluster_i) in enumerate(ZONES):
    d.box(20, zy - 4, W - 44, 148, PAPER2, RULE, 0.8, 6)
    d.t(32, zy + 18, zname, 11, SOFT, MONO, "start")
    ny = zy + 42
    for i, (x, name) in enumerate(zip(XS, CHAIN)):
        focal = (i == cluster_i)
        if focal:
            d.tone(x - NW / 2, ny, NW, NH, ACC, 6, "14", 1.4)
        else:
            d.box(x - NW / 2, ny, NW, NH, PAPER, RULE, 1.0, 6)
        d.t(x, ny + 26, name, 12, ACC if focal else INK, KR, "middle", 600)
        if focal:
            d.t(x, ny + 46, "CDN 클러스터", 11, ACC, KR)
        if i < len(XS) - 1:
            d.path(f"M {x + NW / 2 + 4} {ny + NH / 2} L {XS[i + 1] - NW / 2 - 10} {ny + NH / 2}", MUTED, 1.2, m="ar")
    tail = "사용자와 서버 사이 링크·라우터가 가장 적습니다" if zi == 0 else "운영할 곳이 적은 대신 지연이 더 큽니다"
    d.t(32, zy + 136, tail, 11, SOFT, KR, "start")

d.t(20, 526, "두 철학은 같은 목표를 놓고 분산의 정도를 다르게 고른 것입니다. 깊이 들어갈수록 병목을 만날 링크가 줄지만 유지·관리가 어려워집니다.",
     11, MUTED, KR, "start")

d.legend(H - 40, [("클러스터가 놓이는 자리", ACC), ("경로 위의 나머지", MUTED)])
d.save("02-04.cdn-placement.svg")
