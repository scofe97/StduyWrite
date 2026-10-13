# 타입 스펙: type-process — 서버 추가와 제거 두 경우를 행으로, 기준 위치 → 시계 반대 방향 첫 서버 → 옮길 범위 → 받는 서버를 열로 두고 칸마다 §2 예시의 실제 위치 값을 적는다.
# 사실 출처: 추가는 새 서버 위치에서 시계 반대 방향으로 서버를 만날 때까지(s4 → s3), 제거는 제거된 서버 위치에서 시계 반대 방향으로(s1 → s0)이며 그 사이 키가 옮겨 간다는 규칙은
#   추출본 v2.txt 1453~1461행·PDF 81~82쪽 그림. 위치 10·15·40·90 과 길이 20·25 는 §2 예시에서 계산한 값이다.
# Layout conventions: 카드 폭 192·높이 100, x stride 208(140·348·556·764), 행 stride 132(y=140·272). 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, MUTED, INK, KR, MONO

SP = {"s0": 15, "s1": 40, "s2": 65, "s3": 90}
SIZE = 100


def length(lo, hi):
    return (hi - lo) % SIZE


# 추가: s4 를 10 에 놓으면 반시계 첫 서버는 s3(90), 그 범위의 키는 시계 방향 다음 서버 s0 이 맡던 키다.
ADD_LEN = length(SP["s3"], 10)
# 제거: s1(40) 에서 반시계 첫 서버는 s0(15), 그 범위의 키는 시계 방향 다음 서버 s2 로 간다.
REM_LEN = length(SP["s0"], SP["s1"])
assert (ADD_LEN, REM_LEN) == (20, 25)

W, H = 1000, 436
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 05-01 §5",
      "옮길 범위는 바뀐 서버에서 시계 반대 방향 첫 서버까지다",
      "s4 를 더하면 (90, 10] 의 20 이, s1 을 빼면 (15, 40] 의 25 가 이웃 서버로 간다.",
      "열은 범위를 찾는 순서이고 괄호는 앞 위치를 제외하고 뒤 위치를 포함한 구간")

COLS = ("바뀐 서버", "반시계 첫 서버", "옮길 범위", "키를 받는 서버")
X0, CW, CH, STRIDE = 140, 192, 100, 208
for j, name in enumerate(COLS):
    d.t(X0 + j * STRIDE + CW / 2, 120, name, 13, MUTED, KR, "middle", 600)

CARDS = (
    ("서버 추가", (("s4", "위치 10"), ("s3", "위치 90"), (f"(90, 10]", f"길이 {ADD_LEN}"), ("s4", "s0 에서 받음"))),
    ("서버 제거", (("s1", "위치 40"), ("s0", "위치 15"), (f"(15, 40]", f"길이 {REM_LEN}"), ("s2", "s1 에서 받음"))),
)
Y0, RSTRIDE = 140, 132
for i, (name, cells) in enumerate(CARDS):
    y = Y0 + i * RSTRIDE
    d.t(16, y + 56, name, 14, INK, KR, "start", 600)
    for j, (a, b) in enumerate(cells):
        x = X0 + j * STRIDE
        focal = i == 0 and j == 2
        c = ACC if focal else INFO
        d.tone(x, y, CW, CH, c, 6, "12", 1.4 if focal else 1.0)
        d.t(x + 14, y + 44, a, 18, INK, MONO, "start", 600)
        d.t(x + 14, y + 76, b, 13, MUTED, KR, "start")
        if j < 3:
            d.arrow([(x + CW + 2, y + CH // 2), (x + STRIDE - 6, y + CH // 2)], MUTED, "ar", 1.5)

d.legend(H - 44, [("범위를 찾는 단계", INFO), ("가장 짚는 칸", ACC)])
d.save("05-01.affected-range.svg")
