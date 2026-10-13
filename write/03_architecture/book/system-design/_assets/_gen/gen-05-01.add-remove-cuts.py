# 타입 스펙: type-gantt — 같은 가로축 위에 구간 주인을 세 번 쌓는다(기준 · s4 추가 · s1 제거). 키 점은 세 줄에서 같은 자리에 있고 바뀌는 것은 막대(구간)의 주인뿐이다.
# 사실 출처: 서버 4→5 일 때 key0 만 server 4 로, server 1 제거 때 key1 만 server 2 로 가는 결과는 추출본 v2.txt 1398~1409행·PDF 78~79쪽 그림.
#   위치 값(s0=15 · s1=40 · s2=65 · s3=90 · s4=10 · k0=95 · k1=30 · k2=55 · k3=80)은 §2 와 같은 설명용 예시다.
# Layout conventions: 축 x(p)=140+8p(p=0~100), 행 stride 84(y=132·216·300), 막대 높이 40. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, MUTED, INK, PAPER, RULE, KR, MONO

X0, U = 140, 8


def X(p):
    return X0 + p * U


KEYS = (("k0", 95), ("k1", 30), ("k2", 55), ("k3", 80))
BASE = [(0, 15, "s0"), (15, 40, "s1"), (40, 65, "s2"), (65, 90, "s3"), (90, 100, "s0")]
ADD = [(0, 10, "s4"), (10, 15, "s0"), (15, 40, "s1"), (40, 65, "s2"), (65, 90, "s3"), (90, 100, "s4")]
REM = [(0, 15, "s0"), (15, 40, "s2"), (40, 65, "s2"), (65, 90, "s3"), (90, 100, "s0")]


def owner(rows, p):
    return next(o for a, b, o in rows if a <= p < b)


# 키가 어느 줄에서 주인이 바뀌는지 계산해 확인한다.
assert [k for k, p in KEYS if owner(ADD, p) != owner(BASE, p)] == ["k0"]
assert [k for k, p in KEYS if owner(REM, p) != owner(BASE, p)] == ["k1"]

W, H = 1000, 408
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 05-01 §3",
      "서버를 더하거나 빼면 이웃 구간의 키 하나만 주인이 바뀐다",
      "s4 를 10 에 더하면 k0 만 s0 에서 s4 로, s1 을 빼면 k1 만 s1 에서 s2 로 간다.",
      "키 점의 자리는 그대로이고 막대의 주인이 바뀌는 구간만 강조")

d.line(X(0), 108, X(100), 108, RULE, 1.0)
for p in (0, 10, 15, 40, 65, 90, 100):
    d.line(X(p), 104, X(p), 112, MUTED, 1.0)
    d.t(X(p), 98, "100 = 0" if p == 100 else str(p), 12, MUTED, MONO, "middle")

CUTS = (
    ("기준", "서버 4대", BASE, BASE),
    ("s4 추가", "k0 → s4", ADD, BASE),
    ("s1 제거", "k1 → s2", REM, BASE),
)
ROW0, STRIDE = 132, 84
for i, (name, sub, segs, ref) in enumerate(CUTS):
    ry = ROW0 + i * STRIDE
    by = ry + 12
    d.t(16, by + 18, name, 14, INK, KR, "start", 600)
    d.t(16, by + 38, sub, 13, MUTED, KR if any("가" <= ch <= "힣" for ch in sub) else MONO, "start")
    for a, b, o in segs:
        # 같은 구간에서 기준 줄의 주인과 다르면 바뀐 구간이다.
        changed = owner(ref, (a + b) / 2) != o
        c = ACC if changed else INFO
        d.tone(X(a) + 1, by, (b - a) * U - 2, 40, c, 4, "14", 1.4 if changed else 1.0)
        d.t(X(a) + 8, by + 26, o, 13, c, MONO, "start", 600)
    for k, p in KEYS:
        d.o.append(f'<circle cx="{X(p)}" cy="{by + 20}" r="7" fill="{PAPER}" stroke="{INK}" stroke-width="1.6"/>')
        if i == 0:
            d.t(X(p), by - 6, f"{k} · {p}", 12, INK, MONO, "middle", 600)

d.legend(H - 44, [("키 위치", INK), ("구간 주인 그대로", INFO), ("주인이 바뀐 구간", ACC)])
d.save("05-01.add-remove-cuts.svg")
