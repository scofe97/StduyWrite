# 타입 스펙: type-tree — 키 1~12 를 버킷 넷으로 나눈 두 서버의 머클 트리 둘을 나란히 두고, 루트에서 내려가며 다른 해시를 따라 키 7~9 한 버킷에 닿는다.
# 사실 출처: 추출본 v2.txt 1813~1840행(키 공간 1~12 · 버킷 4 · 키 해시 → 버킷당 해시 → 루트까지 · 루트부터 비교해 다른 쪽만 내려감),
#   PDF 102~103쪽 그림의 값: 서버 1 버킷 해시 6901·6773·8601·7812, 중간 3545·4603, 루트 5357 / 서버 2 7975·2960·9213, 나머지 같음.
#   키 해시: 1→2343 2→1456 3→9865 5→2145 6→7456 7→9654 8→1356(서버 2 는 없음) 9→4358 10→3542 11→8705 12→3697. 버킷 2 의 첫 칸은 그림에서 비어 있다.
# Layout conventions: 트리 폭 440(x 원점 24·496), 레벨 stride 88(y=132·220·308·396). 버킷 폭 104·stride 112. 비교 띠 y=544. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 640
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 06-02 §4",
      "루트의 해시가 다르면 다른 가지로만 내려가 한 버킷에 닿는다",
      "다섯 번 비교하면 어긋난 버킷이 키 7~9 뿐임을 알고, 그 세 키만 맞춘다.",
      "해시 값은 비교를 보이기 위한 예시 값")

BUCKETS = (
    ("키 1~3", ("1 → 2343", "2 → 1456", "3 → 9865")),
    ("키 4~6", ("", "5 → 2145", "6 → 7456")),
    ("키 7~9", ("7 → 9654", "8 → 1356", "9 → 4358")),
    ("키 10~12", ("10 → 3542", "11 → 8705", "12 → 3697")),
)
TREES = (
    (24, "서버 1", ("6901", "6773", "8601", "7812"), ("3545", "4603"), "5357", "8 → 1356"),
    (496, "서버 2", ("6901", "6773", "7975", "7812"), ("3545", "2960"), "9213", None),
)
DIFF_LEAF = 2


def hnode(cx, y, val, diff):
    x = cx - 44
    if diff:
        d.tone(x, y, 88, 40, ACC, 6, "12", 1.4)
    else:
        d.box(x, y, 88, 40, PAPER2, MUTED, 1.0, 6)
    d.t(cx, y + 26, val, 14, ACC if diff else INK, MONO, "middle", 600)


for X0, name, bh, mid, root, key8 in TREES:
    d.t(X0, 108, name, 15, INK, KR, "start", 600)
    cxs = [X0 + 52 + 112 * k for k in range(4)]
    mcx = [(cxs[0] + cxs[1]) // 2, (cxs[2] + cxs[3]) // 2]
    rcx = X0 + 220
    other = TREES[1] if X0 == 24 else TREES[0]
    # 가지 선
    for k in range(4):
        d.line(cxs[k], 308 + 40, cxs[k], 396, RULE if k != DIFF_LEAF else ACC, 1.2 if k == DIFF_LEAF else 0.9)
    for j in range(2):
        yb = 264 + 22 + 22
        for k in (2 * j, 2 * j + 1):
            d.line(cxs[k], 308, cxs[k], 288, ACC if k == DIFF_LEAF else RULE, 1.2 if k == DIFF_LEAF else 0.9)
        if j == 1:
            d.line(cxs[2], 288, mcx[1], 288, ACC, 1.2)
            d.line(mcx[1], 288, cxs[3], 288, RULE, 0.9)
        else:
            d.line(cxs[0], 288, cxs[1], 288, RULE, 0.9)
        d.line(mcx[j], 288, mcx[j], 260, ACC if j == 1 else RULE, 1.2 if j == 1 else 0.9)
        d.line(mcx[j], 220, mcx[j], 200, ACC if j == 1 else RULE, 1.2 if j == 1 else 0.9)
    d.line(mcx[0], 200, rcx, 200, RULE, 0.9)
    d.line(rcx, 200, mcx[1], 200, ACC, 1.2)
    d.line(rcx, 200, rcx, 172, ACC, 1.2)
    hnode(rcx, 132, root, True)
    hnode(mcx[0], 220, mid[0], False)
    hnode(mcx[1], 220, mid[1], True)
    for k in range(4):
        hnode(cxs[k], 308, bh[k], k == DIFF_LEAF)
    for k, (rng, lines) in enumerate(BUCKETS):
        bx = X0 + 112 * k
        leaf_diff = k == DIFF_LEAF
        if leaf_diff:
            d.tone(bx, 396, 104, 88, ACC, 6, "12", 1.4)
        else:
            d.box(bx, 396, 104, 88, PAPER2, RULE, 0.9, 6)
        for r, txt in enumerate(lines):
            col = INK
            if leaf_diff and r == 1:
                col = ACC
                if key8 is None:
                    txt = "8 → 없음"
            d.t(bx + 12, 420 + 22 * r, txt, 12, col, MONO, "start", 600 if (leaf_diff and r == 1) else 400)
        d.t(bx + 52, 506, rng, 12, MUTED, KR, "middle")

# 비교 순서
d.t(24, 548, "비교 순서", 13, SOFT, KR, "start", 600)
STEPS = (("5357 ≠ 9213", ACC), ("3545 = 3545", MUTED), ("4603 ≠ 2960", ACC), ("8601 ≠ 7975", ACC), ("7812 = 7812", MUTED))
x = 168
for k, (txt, c) in enumerate(STEPS):
    d.chip(x, 544, txt, c, 12)
    if k < len(STEPS) - 1:
        d.arrow([(x + 56, 544), (x + 72, 544)], MUTED, "ar", 1.2)
    x += 132
d.chip(868, 544, "키 7~9 만 동기화", OK, 12)
d.arrow([(x - 76, 544), (788, 544)], MUTED, "ar", 1.2)

d.legend(H - 56, [("같은 해시", MUTED), ("다른 해시", ACC), ("동기화 대상", OK)])
d.save("06-02.merkle-walk.svg")
