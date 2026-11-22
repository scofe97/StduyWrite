# 03-01 「fork 두 번의 프로세스 트리」 — fork() 를 두 번 이어 부르면 프로세스가 1개 → 2개 → 4개로 늘고, A 가 B·D 의 부모, B 가 C 의 부모가 된다.
# 본문 근거: 이 노트 「1. fork 로 프로세스 복제하기」 의 fork 두 번 ### 와 「정답 10」.
# 값 근거: 개념 도식이라 값은 없다.
# 공식 근거: fork(2) — 호출한 프로세스를 복제해 새 프로세스를 만든다. OSTEP 5장 §5.1.
# 타입 스펙: type-tree — 시작·첫 fork() 뒤·둘째 fork() 뒤 세 시점을 가로로 펼쳐 부모→자식 트리와 세대(1·2·3세대)를 보인다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, INFO, PAPER2, KR, MONO

W, H = 920, 540
d = D(W, H, "OSTEP · 03-01 §1",
      "fork() 두 번: 1개 → 2개 → 4개, A 는 B 와 D 의 부모, B 는 C 의 부모",
      "fork 를 두 번 이어 부르면 프로세스가 1개에서 2개, 4개로 늘고 A 가 B 와 D 의 부모, B 가 C 의 부모가 되는 프로세스 트리. "
      "시작 시점에 프로세스 A 가 있고, 첫째 fork() 에서 A 가 자식 B 를 만들어 2개가 된다. "
      "둘째 fork() 는 A 와 B 가 각각 불러 A 가 자식 D 를, B 가 자식 C 를 만들어 4개가 된다. "
      "네 프로세스 A B C D 는 각각 hello 를 한 번씩 찍어 모두 네 번 찍히며, 순서는 스케줄러가 정한다.",
      lead="세 시점을 왼쪽에서 오른쪽으로 따라가며 누가 누구의 자식인지 봅니다.")

# 레이아웃 상수 (4의 배수)
NW, NH = 148, 52
ROW_Y0, ROW_STRIDE = 160, 76
CODE_X, CODE_Y, CODE_W, CODE_H = 20, 216, 168, 168
COL_X = [204, 428, 652]
OUT_X, OUT_W, OUT_H = 832, 68, 32


def ry(r):
    return ROW_Y0 + r * ROW_STRIDE


def rcy(r):
    return ry(r) + NH // 2


# 시점 머리글 (시작 → 첫 fork() 뒤 → 둘째 fork() 뒤 → 출력)
headers = [
    (COL_X[0] + NW // 2, "시작", "프로세스 1개", MUTED),
    (COL_X[1] + NW // 2, "첫 fork() 뒤", "프로세스 2개", MUTED),
    (COL_X[2] + NW // 2, "둘째 fork() 뒤", "프로세스 4개", MUTED),
    (OUT_X + OUT_W // 2, "출력", "모두 4번", OK),
]
for cx, ttl, sub, sub_c in headers:
    d.t(cx, 116, ttl, 13, INK, KR, "middle", 600)
    d.t(cx, 136, sub, 12, sub_c, KR, "middle", 400)

# 머리글 사이 시점 흐름 화살표
d.arrow([(COL_X[0] + NW + 12, 112), (COL_X[1] - 12, 112)], SOFT, "soft", 1.2)
d.arrow([(COL_X[1] + NW + 12, 112), (COL_X[2] - 12, 112)], SOFT, "soft", 1.2)
d.arrow([(COL_X[2] + NW - 12, 112), (OUT_X + 4, 112)], SOFT, "soft", 1.2)
d.line(COL_X[0], 146, OUT_X + OUT_W, 146, RULE, 0.8)

# 1) 연결선을 노드보다 먼저 그린다 (type-tree z-order 규칙)
# 같은 프로세스 실행 이어감 (점선)
d.arrow([(COL_X[0] + NW + 2, rcy(0)), (COL_X[1] - 2, rcy(0))], SOFT, "soft", 1.2, "4 4")
d.arrow([(COL_X[1] + NW + 2, rcy(0)), (COL_X[2] - 2, rcy(0))], SOFT, "soft", 1.2, "4 4")
d.arrow([(COL_X[1] + NW + 2, rcy(2)), (COL_X[2] - 2, rcy(2))], SOFT, "soft", 1.2, "4 4")

# 부모 → 자식 직교 분기 (실선)
# A(시작) → B(첫째 fork)
x_drop1 = COL_X[0] + NW + 16
d.arrow([(COL_X[0] + NW + 2, rcy(0)), (x_drop1, rcy(0)), (x_drop1, rcy(2)), (COL_X[1] - 2, rcy(2))], MUTED, "ar", 1.6)
d.t((x_drop1 + COL_X[1]) // 2, rcy(2) - 32, "첫째", 12, INK, KR, "middle", 600)
d.t((x_drop1 + COL_X[1]) // 2, rcy(2) - 16, "fork()", 12, MUTED, MONO, "middle", 600)

# A(첫 fork 뒤) → D(둘째 fork)
x_drop2 = COL_X[1] + NW + 16
d.arrow([(COL_X[1] + NW + 2, rcy(0)), (x_drop2, rcy(0)), (x_drop2, rcy(1)), (COL_X[2] - 2, rcy(1))], MUTED, "ar", 1.6)
d.t((x_drop2 + COL_X[2]) // 2, rcy(1) - 32, "둘째", 12, INK, KR, "middle", 600)
d.t((x_drop2 + COL_X[2]) // 2, rcy(1) - 16, "fork()", 12, MUTED, MONO, "middle", 600)

# B(첫 fork 뒤) → C(둘째 fork)
d.arrow([(COL_X[1] + NW + 2, rcy(2)), (x_drop2, rcy(2)), (x_drop2, rcy(3)), (COL_X[2] - 2, rcy(3))], MUTED, "ar", 1.6)
d.t((x_drop2 + COL_X[2]) // 2, rcy(3) - 32, "둘째", 12, INK, KR, "middle", 600)
d.t((x_drop2 + COL_X[2]) // 2, rcy(3) - 16, "fork()", 12, MUTED, MONO, "middle", 600)

# 각 프로세스 → hello 출력 화살표
for r in range(4):
    d.arrow([(COL_X[2] + NW + 2, rcy(r)), (OUT_X - 2, rcy(r))], OK, "ok", 1.3)

# 2) 왼쪽 대상 코드 상자
d.box(CODE_X, CODE_Y, CODE_W, CODE_H, PAPER2, RULE, 1.0)
d.t(CODE_X + 14, CODE_Y + 26, "대상 코드", 13, INK, KR, "start", 600)
d.line(CODE_X + 12, CODE_Y + 38, CODE_X + CODE_W - 12, CODE_Y + 38, RULE, 0.8)
code_lines = [
    ("1", "fork();", INK),
    ("2", "fork();", INK),
    ("3", 'printf("hello\\n");', OK),
]
for idx, (ln, stmt, c) in enumerate(code_lines):
    y_ln = CODE_Y + 66 + idx * 32
    d.t(CODE_X + 14, y_ln, ln, 12, SOFT, MONO, "start", 400)
    d.t(CODE_X + 28, y_ln, stmt, 12, c, MONO, "start", 600 if c == OK else 400)

# 3) 프로세스 노드
def pnode(col, row, title, sub, c=None):
    x, y = COL_X[col], ry(row)
    if c:
        d.tone(x, y, NW, NH, c, 6, "14", 1.4 if c == ACC else 1.1)
    else:
        d.box(x, y, NW, NH, PAPER2, RULE, 1.0)
    d.t(x + NW // 2, y + 22, title, 13, c or INK, KR, "middle", 600)
    d.t(x + NW // 2, y + 41, sub, 12, MUTED, KR, "middle", 400)


# 시작
pnode(0, 0, "A (1세대)", "처음부터 있던 프로세스")

# 첫 fork() 뒤
pnode(1, 0, "A (1세대)", "계속 실행")
pnode(1, 2, "B (2세대)", "A 의 자식", INFO)

# 둘째 fork() 뒤
pnode(2, 0, "A (1세대)", "계속 실행")
pnode(2, 1, "D (2세대)", "A 의 자식", INFO)
pnode(2, 2, "B (2세대)", "A 의 자식", INFO)
pnode(2, 3, "C (3세대)", "B 의 자식 (A 의 손자)", ACC)

# 출력 (hello x 4)
for r in range(4):
    y_out = rcy(r) - OUT_H // 2
    d.tone(OUT_X, y_out, OUT_W, OUT_H, OK, 6, "14", 1.1)
    d.t(OUT_X + OUT_W // 2, rcy(r) + 4, "hello", 12, OK, MONO, "middle", 600)

# 아래 설명 줄 및 범례
d.t(20, 472, "hello 한 번씩 모두 4번 · 찍히는 순서는 스케줄러가 정함", 12, MUTED, KR, "start")
d.legend(H - 44, [("2세대 (A 의 자식)", INFO), ("3세대 (B 의 자식 · 손자)", ACC), ("hello 출력", OK)])
d.save("03-01.fork-twice-tree.svg")
print("ok 03-01 fork-twice-tree")
