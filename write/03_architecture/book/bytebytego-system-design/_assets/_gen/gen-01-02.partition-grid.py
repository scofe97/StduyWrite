# 타입 스펙: type-dp-security-matrix — 같은 user 테이블을 열로 자른 결과와 행으로 자른 결과를 실제 컬럼·행으로 나란히 보이는 격자(격자 문법을 비교 행렬로 사용). 초점은 열을 나눠도 양쪽에 남는 UserID.
# 사실 출처: 추출본 v1.txt 1996~2051행과 쪽 82 그림(User Table 의 UserID 1~4 · Bob · Alice · Ted · Lisa, 컬럼 UserID · Name · Status · Desc · Photo, 수직 분할 뒤 User Table · User Extension Table, 수평 분할 hash = UserID mod 2, range = UserID 1·2 | 3·4). 수직 분할의 UserID 복사본은 쪽 82 그림에서 두 테이블 모두 UserID 를 가짐.
# Layout conventions: §2 공식 — 열 폭 132 · 간격 8, 행 stride 36(셀 높이 32), 그룹 사이 간격 24. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W = 960
LEFT, CW, GAP, GG = 12, 132, 8, 24
names = ["Bob", "Alice", "Ted", "Lisa"]
H = 736
d = D(W, H, "BYTEBYTEGO · 01-02 §1",
      "같은 user 테이블을 열로, 행으로 자른 결과",
      "열로 자르면 행 수는 그대로 4이고 UserID 가 두 테이블에 남고, 행으로 자르면 열은 그대로이고 행이 조각으로 갈립니다",
      "user(UserID · Name · Status · Desc · Photo) · 행 4개 · 수평 분할의 샤드도 열 다섯 개")

# 패널 A — 수직 분할
y = 96
d.t(LEFT, y + 12, "수직 분할 · 열을 나눔", 13, INK, KR, "start", 600)
y += 28
g1 = ["UserID", "Name", "Status"]
g2 = ["UserID", "Desc", "Photo"]
x1 = LEFT
x2 = LEFT + 3 * CW + 2 * GAP + GG
d.t(x1 + (3 * CW + 2 * GAP) / 2, y + 12, "user", 12, INFO, MONO, "middle", 600)
d.t(x2 + (3 * CW + 2 * GAP) / 2, y + 12, "user_extension", 12, WARN, MONO, "middle", 600)
y += 24
for gx, cols, c in ((x1, g1, INFO), (x2, g2, WARN)):
    for j, col in enumerate(cols):
        x = gx + j * (CW + GAP)
        focal = (gx == x2 and j == 0)
        if focal:
            d.tone(x, y, CW, 32, ACC, 4, "14", 1.4)
        else:
            d.tone(x, y, CW, 32, c, 4, "10", 0.9)
        d.t(x + CW / 2, y + 21, col, 12, ACC if focal else INK, MONO, "middle", 600)
y += 40
for i in range(4):
    yy = y + i * 36
    vals1 = [str(i + 1), names[i], ""]
    vals2 = [str(i + 1), "", ""]
    for gx, vals, c in ((x1, vals1, INFO), (x2, vals2, WARN)):
        for j, v in enumerate(vals):
            x = gx + j * (CW + GAP)
            focal = (gx == x2 and j == 0)
            if focal:
                d.tone(x, yy, CW, 32, ACC, 4, "14", 1.4)
            else:
                d.box(x, yy, CW, 32, PAPER2, RULE, 0.8, 4)
            if v:
                d.t(x + CW / 2, yy + 21, v, 12, ACC if focal else INK, MONO if v.isdigit() else KR, "middle")
yA_end = y + 3 * 36 + 32

# 패널 B — 수평 분할 두 가지
y = yA_end + 32
d.t(LEFT, y + 12, "수평 분할 · 행을 나눔 (샤딩)", 13, INK, KR, "start", 600)
y += 28
variants = [
    ("해시 · UserID mod 2", [("나머지 1", [(1, "Bob"), (3, "Ted")], INFO), ("나머지 0", [(2, "Alice"), (4, "Lisa")], WARN)]),
    ("범위 · UserID 구간", [("1 ~ 2", [(1, "Bob"), (2, "Alice")], INFO), ("3 ~ 4", [(3, "Ted"), (4, "Lisa")], WARN)]),
]
COLS = ["UserID", "Name", "Status", "Desc", "Photo"]
SW = 84
VW = 5 * SW + 4 * GAP
for v, (title, shards) in enumerate(variants):
    vx = LEFT + v * (VW + 24)
    d.t(vx, y + 12, title, 12, MUTED, KR, "start", 600)
    yy = y + 24
    for lab, rows, c in shards:
        d.t(vx, yy + 12, lab, 12, c, KR, "start", 600)
        yy += 20
        for j, col in enumerate(COLS):
            x = vx + j * (SW + GAP)
            d.tone(x, yy, SW, 32, c, 4, "10", 0.9)
            d.t(x + SW / 2, yy + 21, col, 12, INK, MONO, "middle", 600)
        yy += 36
        for uid, nm in rows:
            for j, val in enumerate((str(uid), nm, "", "", "")):
                x = vx + j * (SW + GAP)
                d.box(x, yy, SW, 32, PAPER2, c, 0.9, 4)
                if val:
                    d.t(x + SW / 2, yy + 21, val, 12, INK, MONO if j == 0 else KR, "middle")
            yy += 36
        yy += 8
yB_end = y + 24 + 2 * (20 + 36 + 2 * 36 + 8)

d.legend(yB_end + 4, [("첫 조각", INFO), ("둘째 조각", WARN), ("두 테이블에 남는 UserID", ACC)])
d.save("01-02.partition-grid.svg")
