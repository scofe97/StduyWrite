# 타입 스펙: type-process — 같은 로그 상자를 요청 네 번에 반복해 그리고, 줄마다(도착 · 로그 · 판정) 타임스탬프가 쌓이고 오래된 것이 제거되는 것을 항목으로 보인다.
# 사실 출처: 추출본 v2.txt 1076~1088행(분당 2건 · 1:00:01 허용 · 1:00:30 허용 · 1:00:50 로그 3 > 2 거절하지만 타임스탬프는 남음 · 1:01:40 에 [1:00:40,1:01:40) 밖 두 개 제거 후 크기 2 허용), PDF 쪽 60 그림.
#   창 시작 시각은 도착 시각 − 1분으로 계산했다(0:59:01 · 0:59:30 · 0:59:50 · 1:00:40).
# Layout conventions: 행 이름 열 x=24, 요청 칸 폭 184 · 간격 16(x=140 부터 stride 200), 머리 y=100 높이 52, 로그 y=164 높이 116(줄 stride 24), 판정 y=296. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, INFO, KR, MONO

W, H = 960, 404
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 04-01 §6",
      "로그는 거절된 요청의 시각도 남긴다",
      "분당 2건 한도의 이동 윈도 로그에서 1:00:01 과 1:00:30 은 허용되고, 1:00:50 은 로그 크기 3 으로 거절되지만 타임스탬프가 남으며, 1:01:40 에는 창 밖의 두 항목이 제거되어 크기 2 로 허용된다.",
      "한도 분당 2건")

X0, CW, STRIDE = 140, 184, 200
HY, LY, JY = 100, 164, 300
LH = 116

# (도착, 창 시작, [(타임스탬프, 상태)], 판정 문구, 판정 색)
# 상태: n 일반 · r 거절돼도 남음 · x 제거됨 · w 이번 요청
FRAMES = (
    ("1:00:01", "0:59:01", (("1:00:01", "w"),), "허용 · 로그 1", OK),
    ("1:00:30", "0:59:30", (("1:00:01", "n"), ("1:00:30", "w")), "허용 · 로그 2", OK),
    ("1:00:50", "0:59:50", (("1:00:01", "n"), ("1:00:30", "n"), ("1:00:50", "r")), "거절 · 로그 3", BAD),
    ("1:01:40", "1:00:40", (("1:00:01", "x"), ("1:00:30", "x"), ("1:00:50", "n"), ("1:01:40", "w")), "허용 · 로그 2", OK),
)

for y, tag in ((HY + 24, "도착"), (LY + 60, "로그"), (JY + 26, "판정")):
    d.t(24, y, tag, 14, SOFT, KR, "start", 600)

for i, (t, ws, items, res, rc) in enumerate(FRAMES):
    x = X0 + STRIDE * i
    d.t(x + CW / 2, HY + 24, t, 14, INK, MONO, "middle", 600)
    d.t(x + CW / 2, HY + 46, f"창 시작 {ws}", 13, MUTED, KR)
    d.box(x, LY, CW, LH, PAPER2, RULE, 1.0, 6)
    for k, (ts, st) in enumerate(items):
        y = LY + 28 + 24 * k
        if st == "r":
            d.tone(x + 12, y - 18, CW - 24, 24, ACC, 4, "14", 1.4)
            col = ACC
        elif st == "x":
            col = SOFT
            d.line(x + 20, y - 4, x + 84, y - 4, BAD, 1.4)
        elif st == "w":
            col = INK
        else:
            col = MUTED
        d.t(x + 24, y, ts, 13, col, MONO, "start", 600 if st in ("w", "r") else 400)
    d.chip(x + CW / 2, JY + 20, res, rc, 13)

d.legend(H - 56, [("허용", OK), ("거절 · 제거", BAD), ("거절돼도 남은 항목", ACC)])
d.save("04-01.sliding-log-frames.svg")
