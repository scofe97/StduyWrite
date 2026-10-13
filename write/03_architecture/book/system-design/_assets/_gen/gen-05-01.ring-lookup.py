# 타입 스펙: type-gantt — 링을 0 에서 끊어 가로축으로 펴고(선택표에 링 타입이 없어 막대 길이가 곧 구간인 gantt 로 축약), 서버마다 맡는 구간을 막대로, 키는 그 막대 위의 점으로 그린다.
# 사실 출처: 시계 방향 조회·키 넷이 서버 넷에 하나씩 붙는 결과(key0→server 0 · key1→server 1 · key2→server 2 · key3→server 3)는 추출본 v2.txt 1389~1393행·PDF 77쪽 그림.
#   위치 값 0~99 · s0=15 · s1=40 · s2=65 · s3=90 · k0=95 · k1=30 · k2=55 · k3=80 은 설명용 예시다(원문 그림에는 숫자가 없고 순서만 k0 s0 k1 s1 k2 s2 k3 s3).
# Layout conventions: 축 x(p)=140+8p(p=0~100), 행 stride 64(y=148·212·276·340), 막대 높이 32. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, INFO, MUTED, INK, PAPER, RULE, KR, MONO

X0, U = 140, 8


def X(p):
    return X0 + p * U


SERV = (("s0", 15), ("s1", 40), ("s2", 65), ("s3", 90))
OWN = {"s0": [(0, 15), (90, 100)], "s1": [(15, 40)], "s2": [(40, 65)], "s3": [(65, 90)]}
KEYS = (("k0", 95, "s0"), ("k1", 30, "s1"), ("k2", 55, "s2"), ("k3", 80, "s3"))
# 시계 방향 첫 서버: 키 위치보다 큰 첫 서버 위치, 없으면 맨 앞 서버.
for _, kp, owner in KEYS:
    first = next((n for n, sp in SERV if sp >= kp), SERV[0][0])
    assert first == owner

W, H = 1000, 472
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 05-01 §2",
      "키는 시계 방향 첫 서버에 붙고 끝을 넘으면 0 으로 이어진다",
      "해시 공간 0~99 를 한 줄로 펴면 k1~k3 은 오른쪽 이웃 서버로, k0 은 끝을 지나 s0 으로 간다.",
      "예시 위치: 서버 s0=15 · s1=40 · s2=65 · s3=90 / 키 k0=95 · k1=30 · k2=55 · k3=80")

# 축
d.line(X(0), 108, X(100), 108, RULE, 1.0)
for p in (0, 15, 40, 65, 90, 100):
    d.line(X(p), 104, X(p), 112, MUTED, 1.0)
    d.t(X(p), 98, "100 = 0" if p == 100 else str(p), 12, MUTED, MONO, "middle")

ROW0, STRIDE = 148, 64
for i, (name, sp) in enumerate(SERV):
    ry = ROW0 + i * STRIDE
    by = ry + 16
    total = sum(b - a for a, b in OWN[name])
    d.t(16, by + 14, name, 14, INK, MONO, "start", 600)
    d.t(16, by + 32, f"구간 {total}", 13, MUTED, KR, "start")
    for a, b in OWN[name]:
        d.tone(X(a), by, (b - a) * U, 32, INFO, 4, "14", 1.0)
    # 서버 위치 표식과 이름
    d.line(X(sp), by - 4, X(sp), by + 36, OK, 3.0)
    d.t(X(sp), by + 52, f"{name} · {sp}", 12, OK, MONO, "middle", 600)

for k, kp, owner in KEYS:
    j = [n for n, _ in SERV].index(owner)
    by = ROW0 + j * STRIDE + 16
    cy = by + 16
    wrap = kp > 90
    c = ACC if wrap else MUTED
    d.o.append(f'<circle cx="{X(kp)}" cy="{cy}" r="7" fill="{PAPER}" stroke="{INK}" stroke-width="1.6"/>')
    d.t(X(kp), by - 6, f"{k} · {kp}", 12, INK, MONO, "middle", 600)
    sp = dict(SERV)[owner]
    if not wrap:
        d.arrow([(X(kp) + 10, cy), (X(sp) - 6, cy)], c, "ar", 1.5)
    else:
        lane = 132
        d.arrow([(X(kp) + 10, cy), (X(100) + 16, cy), (X(100) + 16, lane), (X(sp), lane), (X(sp), by - 6)], ACC, "acc", 1.6)
        d.t(X(40), lane - 6, "끝을 지나 0 으로 이어짐", 13, ACC, KR, "start", 600)

d.legend(H - 44, [("서버가 맡는 구간", INFO), ("서버 위치", OK), ("시계 방향 조회", MUTED), ("끝을 넘어 이어진 조회", ACC)])
d.save("05-01.ring-lookup.svg")
