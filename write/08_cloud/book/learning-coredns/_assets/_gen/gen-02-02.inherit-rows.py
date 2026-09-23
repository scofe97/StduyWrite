# 02-02 §2 — NAME 과 TTL 을 생략한 칸은 가장 최근에 지정된 값을 물려받는다.
# 원문 근거: "If you omit the name, ... the record is attached to the most recently specified domain name",
#            "If you omit the TTL, the record inherits the most recently specified TTL" (원서 Example 2-3 의 TTL 예제).
#            단 파일에 $TTL 이 있으면 TTL 은 그 값을 쓴다(RFC 2308 §4) — 본문 §2 가 그 전제를 적는다.
# 예시 네 줄은 본문 §2 두 번째 코드 블록 그대로다.
# 2026-09-23 신설: 적대적 검증이 "상속이 핵심인 절에 도식이 없다"고 지적했다.
# 타입 스펙: type-layers — 줄마다 같은 다섯 칸 띠를 위에서 아래로 쌓는다.
#           축약: 띠가 추상 계층이 아니라 파일의 줄 순서이고, 빈 칸은 바로 윗 띠에서 값을 끌어온다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 480
d = D(W, H, "LEARNING COREDNS · 02-02 §2",
      "빈칸은 윗줄에서 내려온다",
      "존 파일 네 줄을 다섯 칸으로 펼친 그림이다. 둘째 줄은 NAME 을, 넷째 줄은 NAME 과 TTL 을 생략했고, "
      "그 칸은 바로 윗줄에 적힌 값을 물려받는다. CLASS 는 모든 줄이 IN 으로 적었다.",
      "점선 칸은 파일에 적히지 않은 값입니다")

COLS = [("NAME", 140), ("TTL", 120), ("CLASS", 96), ("TYPE", 96), ("RDATA", 180)]
X0, GAP = 104, 12
xs = []
x = X0
for _, w in COLS:
    xs.append(x); x += w + GAP
ROW_H, ROW_STEP, Y0 = 44, 76, 140

# 줄마다 (값, 물려받았나)
rows = [
    [("@", 0), ("3600", 0), ("IN", 0), ("A", 0), ("10.0.0.1", 0)],
    [("@", 1), ("1h", 0), ("IN", 0), ("A", 0), ("10.0.0.2", 0)],
    [("www", 0), ("1h30m", 0), ("IN", 0), ("A", 0), ("10.0.0.3", 0)],
    [("www", 1), ("1h30m", 1), ("IN", 0), ("A", 0), ("10.0.0.4", 0)],
]

for (name, w), cx in zip(COLS, xs):
    d.t(cx + w / 2, Y0 - 16, name, 11, SOFT, MONO)

for r, row in enumerate(rows):
    y = Y0 + r * ROW_STEP
    d.t(20, y + 28, f"{r + 1}번째 줄", 12, MUTED, KR, "start")
    for c, ((val, inh), (_, w)) in enumerate(zip(row, COLS)):
        cx = xs[c]
        if inh:
            d.o.append(f'<rect x="{cx}" y="{y}" width="{w}" height="{ROW_H}" rx="6" fill="{ACC}0F" '
                       f'stroke="{ACC}" stroke-width="1.2" stroke-dasharray="4 4"/>')
            d.t(cx + w / 2, y + 27, val, 14, ACC, MONO, "middle", 600)
            # 바로 윗 칸에서 내려오는 화살표
            d.arrow([(cx + w / 2, y - ROW_STEP + ROW_H + 4), (cx + w / 2, y - 4)], ACC, "acc", 1.3)
        else:
            d.box(cx, y, w, ROW_H, PAPER2, RULE, 1.0, 6)
            d.t(cx + w / 2, y + 27, val, 14, INK, MONO, "middle", 600)

d.legend(432, [("생략해 윗줄에서 물려받은 값", ACC)])
d.save("02-02.inherit-rows.svg")
