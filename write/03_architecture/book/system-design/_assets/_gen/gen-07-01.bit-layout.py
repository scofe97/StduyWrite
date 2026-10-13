# 타입 스펙: type-dp-security-matrix — 격자 문법을 비트 칸으로 쓴다. 64칸 한 줄이 1 · 41 · 5 · 5 · 12 칸 묶음으로 갈리고 묶음 아래에 이름 · 비트 수 · 시프트를 붙인다.
# 사실 출처: twitter-archive/snowflake 태그 snowflake-2010 IdWorker.scala L25(twepoch), L27~L31(비트 수 5 · 5 · 12), L33~L36(시프트 12 · 17 · 22), 추출본 v2.txt 2015~2022행(부호 1 · 시각 41 · 센터 5 · 머신 5 · 순번 12).
#   최댓값은 2^41 − 1 = 2199023255551, 2^5 − 1 = 31, 2^12 − 1 = 4095 로 계산.
# Layout conventions: 칸 폭 12 · 64칸 x0=96(768px) · 칸 높이 48 y=132, 지시선 y=184 부터, 이름 줄 y=224·268·312. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, INK, SOFT, PAPER, KR, MONO

W, H = 960, 436
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 07-01 §5",
      "64비트를 1 · 41 · 5 · 5 · 12 칸으로 나눈다",
      "위쪽 41비트가 밀리초 시각이라 정수로 비교하면 시각순이고, 아래쪽 22비트가 만든 곳과 같은 밀리초 안의 순번을 나른다.",
      "왼쪽이 63번 비트 · 오른쪽이 0번 비트")

X0, CW, Y0, CH = 96, 12, 132, 48
GROUPS = (
    ("부호", 1, SOFT, "63번 비트", "항상 0"),
    ("타임스탬프", 41, ACC, "<< 22", "최대 2199023255551 ms"),
    ("데이터센터 ID", 5, INFO, "<< 17", "0 ~ 31"),
    ("머신 ID", 5, INFO, "<< 12", "0 ~ 31"),
    ("시퀀스", 12, OK, "<< 0", "0 ~ 4095"),
)
LABEL_Y = {0: 224, 1: 224, 2: 268, 3: 312, 4: 224}
x = X0
for i, (name, n, c, sh, rng) in enumerate(GROUPS):
    w = n * CW
    d.tone(x, Y0, w, CH, c, 3, "14" if c == ACC else "10", 1.4 if c == ACC else 1.0)
    for k in range(1, n):
        d.line(x + k * CW, Y0 + 12, x + k * CW, Y0 + CH - 12, c + "55", 0.8)
    d.t(x + w / 2, Y0 - 8, str(n), 13, c, MONO, "middle", 600)
    cx = x + w / 2
    ly = LABEL_Y[i]
    d.line(cx, Y0 + CH + 4, cx, ly - 18, c, 1.0)
    anchor = "start" if i == 0 else "middle"
    tx = X0 if i == 0 else cx
    d.t(tx, ly, name, 14, INK, KR, anchor, 600)
    d.t(tx, ly + 20, f"{sh} · {rng}", 12, MUTED, MONO, anchor)
    x += w
d.legend(H - 56, [("시각", ACC), ("만든 곳", INFO), ("순번", OK), ("부호", SOFT)])
d.save("07-01.bit-layout.svg")
