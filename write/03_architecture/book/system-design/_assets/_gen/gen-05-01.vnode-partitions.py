# 타입 스펙: type-gantt — 같은 해시 공간 0~99 에서 서버 구간을 막대로 펴고, 토큰 1개일 때 s1 이 빠진 뒤 · 가상 노드 3개씩일 때 · 그 s1 이 빠진 뒤를 세 줄로 쌓아 구간 길이를 견준다.
# 사실 출처: 토큰 1개일 때 s1 제거로 s2 구간이 s0·s3 의 두 배가 되는 구조는 추출본 v2.txt 1416~1421행(원문 그림은 상대 크기만 보임),
#   가상 노드 구조(서버마다 여러 위치, 첫 가상 노드가 가리키는 서버)는 v2.txt 1430~1445행. 위치 값과 구간 길이는 설명용 예시이며 합계·편차는 python3 로 계산했다.
#   예시 위치(가상 노드 12개): 5=s0 · 12=s2 · 20=s1 · 28=s3 · 33=s0 · 41=s1 · 52=s2 · 60=s3 · 68=s1 · 77=s0 · 85=s3 · 94=s2
# Layout conventions: 축 x(p)=140+8p(p=0~100), 행 stride 92(y=132·224·316), 막대 높이 44, 막대 아래 값 줄 +72. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, MUTED, INK, RULE, KR, MONO

X0, U = 140, 8


def X(p):
    return X0 + p * U


def std_pct(vals):
    m = sum(vals) / len(vals)
    return (sum((v - m) ** 2 for v in vals) / len(vals)) ** 0.5 / m * 100


# 토큰 1개: s1 이 빠진 뒤의 구간. 15~40 은 s1 이 맡던 구간이다.
ONE = [(0, 15, "s0", False), (15, 40, "s2", True), (40, 65, "s2", False), (65, 90, "s3", False), (90, 100, "s0", False)]
# 가상 노드 3개씩: 위치 → 서버. 위치 p 의 서버는 (앞 위치, p] 구간을 맡는다. 마지막 위치 뒤(94~100)는 첫 위치 5 의 서버가 이어받는다.
POS = [(5, "s0"), (12, "s2"), (20, "s1"), (28, "s3"), (33, "s0"), (41, "s1"), (52, "s2"), (60, "s3"), (68, "s1"), (77, "s0"), (85, "s3"), (94, "s2")]
V12 = []
prev = 0
for p, s in POS:
    V12.append((prev, p, s, s == "s1"))
    prev = p
V12.append((94, 100, "s0", False))
# s1 이 빠지면 각 구간은 시계 방향 다음 위치의 서버가 이어받는다.
AFTER = []
for i, (a, b, s, g) in enumerate(V12):
    if s != "s1":
        AFTER.append((a, b, s, False))
        continue
    nxt = V12[(i + 1) % len(V12)][2]
    AFTER.append((a, b, nxt, True))


def totals(segs):
    out = {}
    for a, b, s, _ in segs:
        out[s] = out.get(s, 0) + (b - a)
    return out


T_ONE, T_V12, T_AFT = totals(ONE), totals(V12), totals(AFTER)
assert T_ONE == {"s0": 25, "s2": 50, "s3": 25}
assert T_V12 == {"s0": 25, "s1": 24, "s2": 27, "s3": 24}
assert T_AFT == {"s0": 33, "s2": 35, "s3": 32}
S_ONE, S_AFT = round(std_pct(list(T_ONE.values()))), round(std_pct(list(T_AFT.values())))
assert (S_ONE, S_AFT) == (35, 4)

W, H = 1000, 464
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 05-01 §4",
      "토큰이 하나면 s1 의 구간이 s2 한 곳으로 몰리고 가상 노드는 흩어 준다",
      "같은 s1 제거에서 구간 길이 25·50·25 의 편차가 평균의 35% 인데 33·35·32 는 4% 다.",
      "강조 막대는 s1 이 맡던 구간이고 글자는 그 구간을 지금 맡은 서버")

d.line(X(0), 108, X(100), 108, RULE, 1.0)
for p in (0, 50, 100):
    d.line(X(p), 104, X(p), 112, MUTED, 1.0)
    d.t(X(p), 98, "100 = 0" if p == 100 else str(p), 12, MUTED, MONO, "middle")

ROWS = (
    ("토큰 1개", "s1 제거 뒤", ONE,
     f"구간 길이 s0 25 · s2 50 · s3 25   표준 편차 평균의 {S_ONE}%"),
    ("가상 노드", "서버마다 3개", V12,
     "구간 길이 s0 25 · s1 24 · s2 27 · s3 24"),
    ("가상 노드", "s1 제거 뒤", AFTER,
     f"구간 길이 s0 33 · s2 35 · s3 32   표준 편차 평균의 {S_AFT}%"),
)
ROW0, STRIDE = 132, 92
for i, (a1, a2, segs, under) in enumerate(ROWS):
    ry = ROW0 + i * STRIDE
    by = ry + 8
    d.t(16, by + 20, a1, 13, INK, KR, "start", 600)
    d.t(16, by + 38, a2, 13, MUTED, KR, "start")
    for a, b, s, hot in segs:
        c = ACC if hot else INFO
        d.tone(X(a) + 1, by, (b - a) * U - 2, 44, c, 4, "14", 1.4 if hot else 1.0)
        d.t(X(a) + 6, by + 28, s, 13, c, MONO, "start", 600)
    d.t(X(0), by + 72, under, 13, MUTED, KR, "start")

d.legend(H - 44, [("서버 구간", INFO), ("s1 이 맡던 구간", ACC)])
d.save("05-01.vnode-partitions.svg")
