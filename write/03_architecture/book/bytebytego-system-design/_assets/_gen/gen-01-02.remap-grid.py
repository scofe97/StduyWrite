# 타입 스펙: type-dp-security-matrix — UserID 1~6 이 mod 2 와 mod 3 에서 각각 어느 샤드로 가는지와 그 사이에 옮겨 가는 행을 보이는 격자(격자 문법을 비교 행렬로 사용). 초점은 기존 샤드 사이에서도 옮겨 가는 UserID 3.
# 사실 출처: 추출본 v1.txt 2024~2028행(hash-based sharding, UserID mod 2 → 1·3 과 2·4). mod 3 열과 이동 판정은 본문 계산식(id mod 2 와 id mod 3 의 나머지 비교). PostgreSQL 18 문서 5.12 해시 파티션(modulus · remainder).
# Layout conventions: §2 공식 — left_pad 12, comp_col_w 188, role_col_w 96, role_col_gap 8, header_h 52, header_y 96, row_h 44 · stride 48. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

LEFT, COMP_W, GAP0, COL_W, COL_GAP, HDR_Y, HDR_H, ROW0, ROW_H, STRIDE = 12, 188, 12, 96, 8, 96, 52, 164, 44, 48
ids = [1, 2, 3, 4, 5, 6]
W = LEFT + COMP_W + GAP0 + 6 * COL_W + 5 * COL_GAP + 48
H = ROW0 + 2 * STRIDE + ROW_H + 20 + 44
d = D(W, H, "BYTEBYTEGO · 01-02 §2",
      "샤드 수를 2에서 3으로 바꾸면 행이 옮겨 간다",
      "UserID 6개 중 4개의 샤드가 바뀌고, 그중 3 과 4 는 이미 있던 샤드 사이를 오갑니다",
      "샤드 번호 = UserID 를 샤드 수로 나눈 나머지")

d.box(LEFT, HDR_Y, COMP_W, HDR_H, PAPER2, RULE, 0.9, 6)
d.t(LEFT + COMP_W / 2, HDR_Y + 22, "UserID", 12, INK, MONO, "middle", 600)
d.t(LEFT + COMP_W / 2, HDR_Y + 40, "× 샤드 수", 12, MUTED, KR)

def cx(j):
    return LEFT + COMP_W + GAP0 + j * (COL_W + COL_GAP)

for j, i in enumerate(ids):
    d.box(cx(j), HDR_Y, COL_W, HDR_H, PAPER2, "rgba(191,192,192,0.45)", 0.9, 6)
    d.t(cx(j) + COL_W / 2, HDR_Y + 32, str(i), 16, INK, MONO, "middle", 600)

rows = [("mod 2", "샤드 둘"), ("mod 3", "샤드 셋"), ("행이 옮겨 가는가", "")]
for r, (name, hint) in enumerate(rows):
    y = ROW0 + r * STRIDE
    d.box(LEFT, y, COMP_W, ROW_H, PAPER2, RULE, 0.8, 4)
    if hint:
        d.t(LEFT + 12, y + 18, name, 12, INK, MONO, "start", 600)
        d.t(LEFT + 12, y + 35, hint, 12, MUTED, KR, "start")
    else:
        d.t(LEFT + 12, y + 27, name, 12, INK, KR, "start", 600)
    for j, i in enumerate(ids):
        x = cx(j)
        a, b = i % 2, i % 3
        if r == 0:
            d.tone(x, y, COL_W, ROW_H, INFO, 4, "10", 0.9)
            d.t(x + COL_W / 2, y + 27, f"샤드 {a}", 12, INFO, KR, "middle", 600)
        elif r == 1:
            d.tone(x, y, COL_W, ROW_H, INFO, 4, "10", 0.9)
            d.t(x + COL_W / 2, y + 27, f"샤드 {b}", 12, INFO, KR, "middle", 600)
        else:
            moved = a != b
            focal = (i == 3)
            if focal:
                d.tone(x, y, COL_W, ROW_H, ACC, 4, "14", 1.4)
                d.t(x + COL_W / 2, y + 19, "이동", 12, ACC, KR, "middle", 600)
                d.t(x + COL_W / 2, y + 36, f"{a} → {b}", 12, ACC, MONO, "middle")
            else:
                c = WARN if moved else OK
                d.tone(x, y, COL_W, ROW_H, c, 4, "10", 0.9)
                d.t(x + COL_W / 2, y + 19, "이동" if moved else "그대로", 12, c, KR, "middle", 600)
                d.t(x + COL_W / 2, y + 36, f"{a} → {b}", 12, MUTED, MONO, "middle")

d.legend(H - 44, [("샤드 번호", INFO), ("그대로", OK), ("옮겨 감", WARN), ("기존 샤드 사이 이동", ACC)])
d.save("01-02.remap-grid.svg")
