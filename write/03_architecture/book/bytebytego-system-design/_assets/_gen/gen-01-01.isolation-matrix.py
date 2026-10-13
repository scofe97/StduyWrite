# 타입 스펙: type-dp-security-matrix — 격리 수준 4행 × 이상 현상 4열의 가능·차단 격자(격자 문법을 비교 행렬로 사용). 초점 칸 하나는 표준에서는 가능하지만 PostgreSQL 이 막는 자리.
# 사실 출처: PostgreSQL 18 문서 13.2 표 13.1 "Transaction Isolation Levels"(https://www.postgresql.org/docs/18/transaction-iso.html), 기본값은 같은 문서 13.2.1 "Read Committed is the default isolation level in PostgreSQL"
#   · MySQL 9.7 문서 17.7.2.1 "The default isolation level for InnoDB is REPEATABLE READ"(https://dev.mysql.com/doc/refman/9.7/en/innodb-transaction-isolation-levels.html). 추출본 v1.txt 164~210행.
# Layout conventions: §2 공식 — left_pad 12, comp_col_w 208, role_col_w 148, role_col_gap 16, header_h 52, 단 header_y 는 dd.py 제목 줄 때문에 96, row_h 44 · stride 48 (행 라벨이 두 줄이라 36→44).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

LEFT, COMP_W, GAP0, ROLE_W, ROLE_GAP, HDR_Y, HDR_H, ROW0, ROW_H, STRIDE = 12, 208, 12, 148, 16, 96, 52, 164, 44, 48
roles = [("더티 리드", "미커밋 값 읽기"), ("반복 불가 읽기", "같은 행 값이 바뀜"), ("팬텀 읽기", "행 집합이 바뀜"), ("직렬화 이상", "직렬 순서가 없음")]
rows = [
    ("READ UNCOMMITTED", ""),
    ("READ COMMITTED", "PostgreSQL 기본"),
    ("REPEATABLE READ", "InnoDB 기본"),
    ("SERIALIZABLE", ""),
]
# 표준 기준 값. 1=가능, 0=차단. sub 는 PostgreSQL 이 표준보다 더 막는 자리.
cells = [
    [(1, "PostgreSQL 은 차단"), (1, ""), (1, ""), (1, "")],
    [(0, ""), (1, ""), (1, ""), (1, "")],
    [(0, ""), (0, ""), (1, "PostgreSQL 은 차단"), (1, "")],
    [(0, ""), (0, ""), (0, ""), (0, "")],
]
FOCAL = (2, 2)

W = LEFT + COMP_W + GAP0 + 4 * ROLE_W + 3 * ROLE_GAP + 48
H = ROW0 + 3 * STRIDE + ROW_H + 20 + 44
d = D(W, H, "BYTEBYTEGO · 01-01 §1",
      "격리 수준마다 막아 주는 이상 현상",
      "아래로 갈수록 막는 것이 늘고, 가능 칸이 가장 늦게 사라지는 열이 직렬화 이상입니다",
      "SQL 표준 기준 · PostgreSQL 18 문서 표 13.1")

d.box(LEFT, HDR_Y, COMP_W, HDR_H, PAPER2, RULE, 0.9, 6)
d.t(LEFT + COMP_W / 2, HDR_Y + 22, "격리 수준", 12, INK, KR, "middle", 600)
d.t(LEFT + COMP_W / 2, HDR_Y + 40, "× 이상 현상", 12, MUTED, KR)

def rx(j):
    return LEFT + COMP_W + GAP0 + j * (ROLE_W + ROLE_GAP)

for j, (nm, sub) in enumerate(roles):
    d.box(rx(j), HDR_Y, ROLE_W, HDR_H, PAPER2, "rgba(191,192,192,0.45)", 0.9, 6)
    d.t(rx(j) + ROLE_W / 2, HDR_Y + 22, nm, 12, INK, KR, "middle", 600)
    d.t(rx(j) + ROLE_W / 2, HDR_Y + 40, sub, 12, MUTED, KR)

for i, (name, hint) in enumerate(rows):
    y = ROW0 + i * STRIDE
    d.box(LEFT, y, COMP_W, ROW_H, PAPER2, RULE, 0.8, 4)
    if hint:
        d.t(LEFT + 12, y + 18, name, 12, INK, MONO, "start", 600)
        d.t(LEFT + 12, y + 35, hint, 12, MUTED, KR, "start")
    else:
        d.t(LEFT + 12, y + 27, name, 12, INK, MONO, "start", 600)
    for j in range(4):
        possible, sub = cells[i][j]
        x = rx(j)
        c = WARN if possible else OK
        label = "가능" if possible else "차단"
        if (i, j) == FOCAL:
            d.tone(x, y, ROLE_W, ROW_H, ACC, 4, "14", 1.4)
            d.t(x + ROLE_W / 2, y + 19, label, 12, ACC, KR, "middle", 600)
            d.t(x + ROLE_W / 2, y + 36, sub, 12, ACC, KR)
        else:
            d.tone(x, y, ROLE_W, ROW_H, c, 4, "10", 0.9)
            if sub:
                d.t(x + ROLE_W / 2, y + 19, label, 12, c, KR, "middle", 600)
                d.t(x + ROLE_W / 2, y + 36, sub, 12, MUTED, KR)
            else:
                d.t(x + ROLE_W / 2, y + 27, label, 12, c, KR, "middle", 600)

d.legend(H - 44, [("가능", WARN), ("차단", OK), ("PostgreSQL 이 팬텀까지 막는 칸", ACC)])
d.save("01-01.isolation-matrix.svg")
