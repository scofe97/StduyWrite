# 타입 스펙: type-layers — 건너뛰기 목록 세 층(L3·L2·L1)에서 값 18 을 찾는 경로. 층이 위로 갈수록 성긴 색인이라는 점이 층 문법에 가장 가깝고, 층 안에 노드를 놓고 탐색 경로를 화살표로 얹은 것이 스펙 대비 확장이다(스펙은 층 안 노드를 두지 않음).
# 사실 출처: 추출본 v1.txt 1846~1852행과 PDF 쪽 77 그림의 Skip List(1·9·31 / 1·4·9·18·31 / 1·2·4·6·9·13·18·25·31), Redis 8.10.2 src/t_zset.c L20-L40(정렬 집합은 해시 테이블과 건너뛰기 목록을 함께 쓰고 구현은 Pugh 의 건너뛰기 목록 알고리즘을 따름),
#   Redis 8.10.2 src/t_zset.c L645-L662 zslGetRank(헤더에서 시작해 각 층에서 다음 노드가 목표 이하인 동안 오른쪽으로 이동하고, 이동을 마친 노드가 목표와 같으면 그 층에서 끝냄),
#   redis.conf 8.10.2 L2331-L2332(zset-max-listpack-entries 128 이하이면 listpack 으로 저장). 이동 횟수는 그 규칙으로 센 값이다: L3 에서 헤더→1→9 로 2번, L2 에서 9→18 로 1번이라 3번, 맨 아래 층만 따르면 헤더→1→2→4→6→9→13→18 로 7번. 층 모양은 그림의 예시이고 Redis 는 노드마다 층 수를 무작위로 정한다.
# Layout conventions: 층 높이 72·폭 900(x=12), 층 stride 80, 헤더 칸 폭 52(x=92), 노드 폭 60·높이 32·가로 stride 80(x=176+80k), 노드 y = 층 y + 20. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 424
d = D(W, H, "BYTEBYTEGO · 02-01 §4",
      "건너뛰기 목록은 위 층에서 성기게 건너뛰고 아래로 내려온다",
      "값 18 까지 이동 세 번이면 닿고, 맨 아래 줄만 따르면 일곱 번입니다",
      "정렬 집합이 쓰는 건너뛰기 목록")

BOTTOM = [1, 2, 4, 6, 9, 13, 18, 25, 31]
LAYERS = [("L3", [1, 9, 31]), ("L2", [1, 4, 9, 18, 31]), ("L1", BOTTOM)]
COUNT = {"L3": "이동 2회", "L2": "이동 1회", "L1": "선형 7회"}
HX, HW = 92, 52
X0, NW, NH, NS = 176, 60, 32, 80
LY0, LH, LS = 108, 72, 80
VISITED = {"L3": {1, 9}, "L2": {9}}
STOP = {"L3": 31}
FOUND = ("L2", 18)


def cx(v):
    return X0 + BOTTOM.index(v) * NS + NW / 2


def ny(layer_i):
    return LY0 + layer_i * LS + 20


for i, (tag, vals) in enumerate(LAYERS):
    y = LY0 + i * LS
    d.box(12, y, 900, LH, PAPER2, RULE, 0.8, 6)
    d.t(24, y + 28, tag, 12, SOFT, MONO, "start", 600)
    d.t(24, y + 52, COUNT[tag], 12, MUTED, KR, "start")
    if tag == "L3":
        d.tone(HX, ny(i), HW, NH, INFO, 5, "14", 1.0)
        d.t(HX + HW / 2, ny(i) + 21, "head", 12, INFO, MONO, "middle", 600)
    else:
        d.box(HX, ny(i), HW, NH, PAPER, RULE, 0.8, 5)
        d.t(HX + HW / 2, ny(i) + 21, "head", 12, MUTED, MONO)
    for v in vals:
        x = cx(v) - NW / 2
        if (tag, v) == FOUND:
            d.tone(x, ny(i), NW, NH, ACC, 5, "14", 1.4)
            d.t(cx(v), ny(i) + 21, str(v), 13, ACC, MONO, "middle", 600)
        elif v in VISITED.get(tag, ()):
            d.tone(x, ny(i), NW, NH, INFO, 5, "14", 1.0)
            d.t(cx(v), ny(i) + 21, str(v), 13, INFO, MONO, "middle", 600)
        elif STOP.get(tag) == v:
            d.tone(x, ny(i), NW, NH, WARN, 5, "14", 1.0)
            d.t(cx(v), ny(i) + 21, str(v), 13, WARN, MONO, "middle", 600)
        else:
            d.box(x, ny(i), NW, NH, PAPER, RULE, 0.8, 5)
            d.t(cx(v), ny(i) + 21, str(v), 13, MUTED, MONO)

# 탐색 경로: L3 에서 헤더 → 1 → 9, 다음 노드 31 은 18 보다 커서 9 에서 한 층 내려와 L2 에서 9 → 18
y3, y2, y1 = ny(0) + NH / 2, ny(1) + NH / 2, ny(2) + NH / 2
d.arrow([(HX + HW + 2, y3), (cx(1) - NW / 2 - 4, y3)], INFO, "info", 1.6)
d.arrow([(cx(1) + NW / 2 + 2, y3), (cx(9) - NW / 2 - 4, y3)], INFO, "info", 1.6)
d.arrow([(cx(9) + NW / 2 + 2, y3), (cx(31) - NW / 2 - 4, y3)], WARN, "warn", 1.4, dash="5 4")
d.arrow([(cx(9), ny(0) + NH + 2), (cx(9), ny(1) - 4)], INFO, "info", 1.6)
d.arrow([(cx(9) + NW / 2 + 2, y2), (cx(18) - NW / 2 - 4, y2)], ACC, "acc", 1.6)
# 맨 아래 층만 따르는 길: 헤더 → 1 → 2 → 4 → 6 → 9 → 13 → 18
chain = ["head"] + [1, 2, 4, 6, 9, 13, 18]
for a, b in zip(chain, chain[1:]):
    xa = HX + HW + 2 if a == "head" else cx(a) + NW / 2 + 2
    d.arrow([(xa, y1), (cx(b) - NW / 2 - 4, y1)], MUTED, "ar", 1.2, dash="3 3")

d.legend(H - 44, [("거쳐 간 노드", INFO), ("18 보다 커서 멈춤", WARN), ("찾은 노드", ACC), ("맨 아래 줄만 따르는 길", MUTED)])
d.save("02-01.skiplist-search.svg")
