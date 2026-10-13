# 타입 스펙: type-dp-security-matrix — 격자 문법을 비교 행렬로 쓴다. 행은 갱신 경로의 노드, 열은 갱신 전·후 캐시 목록이고 칩 하나가 목록 항목 하나다. focal 은 beer 칩.
# 사실 출처: 추출본 v2.txt 3797~3806행(노드 하나를 직접 갱신하면 조상 전부를 루트까지 갱신 · beer 10 → 30) · PDF 216쪽 그림 13-13.
#   데이터는 같은 책의 노드별 캐시 예시(PDF 210쪽 그림 13-8: best 35 · bet 29 · bee 20 · be 15 · buy 14 · beer 10)이고, 갱신 후 목록은 beer 를 30 으로 놓고 다시 순위를 매긴 계산값이다.
#   b: [best 35, beer 30, bet 29, bee 20, be 15] (buy 14 는 여섯째로 밀려남) · be: [best 35, beer 30, bet 29, bee 20, be 15] · bee: [beer 30, bee 20] · beer: [beer 30].
# Layout conventions: 행 stride 64(y=164 부터 4 행), 이름 열 x=24, 갱신 전 x=120, 갱신 후 x=544, 칩 높이 28, 칩 간격 8. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, BAD, MUTED, INK, SOFT, KR, MONO

W, H = 1000, 460
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 13-01 §7",
      "beer 하나를 10 에서 30 으로 올리면 루트까지 올라가며 조상의 목록을 다시 쓴다",
      "질의의 노드와 그 조상이 상위 목록에 beer 를 품고 있어서 순서가 바뀌고, b 의 목록에서는 buy 14 가 밀려난다.",
      "예시 질의 · best 35 · bet 29 · bee 20 · be 15 · buy 14 · beer 10 → 30 · k = 5")

BEFORE = {
    "b": ("best 35", "bet 29", "bee 20", "be 15", "buy 14"),
    "be": ("best 35", "bet 29", "bee 20", "be 15", "beer 10"),
    "bee": ("bee 20", "beer 10"),
    "beer": ("beer 10",),
}
AFTER = {
    "b": ("best 35", "beer 30", "bet 29", "bee 20", "be 15"),
    "be": ("best 35", "beer 30", "bet 29", "bee 20", "be 15"),
    "bee": ("beer 30", "bee 20"),
    "beer": ("beer 30",),
}
X_NAME, X_BEFORE, X_AFTER, Y0, ST = 24, 120, 544, 164, 64
CH = 28


def chips(x, y, items, dropped=()):
    cx = x
    for it in items:
        w = len(it) * 7.8 + 16
        if it.startswith("beer"):
            c = ACC
        elif it in dropped:
            c = BAD
        else:
            c = INFO
        d.tone(cx, y, w, CH, c, 4, "14", 1.2 if c != INFO else 1.0)
        d.t(cx + w / 2, y + 19, it, 12, INK, MONO, "middle", 600 if c == ACC else 400)
        cx += w + 8


d.t(X_NAME, 132, "노드", 13, SOFT, KR, "start", 600)
d.t(X_BEFORE, 132, "갱신 전 목록", 13, SOFT, KR, "start", 600)
d.t(X_AFTER, 132, "갱신 후 목록", 13, SOFT, KR, "start", 600)
d.line(24, 144, W - 24, 144, MUTED, 0.8)

for i, n in enumerate(("b", "be", "bee", "beer")):
    y = Y0 + i * ST
    d.t(X_NAME, y + 20, n, 14, INK, MONO, "start", 600)
    chips(X_BEFORE, y, BEFORE[n], dropped=("buy 14",))
    chips(X_AFTER, y, AFTER[n])
    d.arrow([(X_AFTER - 36, y + 14), (X_AFTER - 8, y + 14)], MUTED, "ar", 1.4)
    if i < 3:
        d.line(24, y + 48, W - 24, y + 48, "rgba(191,192,192,0.12)", 0.8)

d.legend(H - 56, [("목록 항목", INFO), ("바뀌는 질의", ACC), ("밀려나는 항목", BAD)])
d.save("13-01.node-update.svg")
