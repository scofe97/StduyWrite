# 타입 스펙: type-gantt — 축 위의 구간을 막대 길이로. 여기서는 시간축 대신 주파수축을 쓴다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §7.2.1 (책 471쪽) Figure 7.3(b) 서술과
#   §7.3.2 Figure 7.23 의 2.4 GHz 채널 배치. 802.11n 전송률은 원문의 [Intel 2024] 인용 값
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, BAD, KR, MONO

W, H = 940, 528
d = D(W, H, "SECTION 7.2.1 · SIGNAL BANDWIDTH",
      "22 MHz 라고 적고 2 MHz 를 그렸습니다",
      "무선에서 대역폭은 신호가 차지하는 주파수 폭이다. 원문이 든 예의 두 끝 값은 그 폭과 맞지 않는다.",
      "주파수 값은 원문 471쪽 서술과 Figure 7.23 에서 그대로 옮겼습니다")

X0, X1 = 208, 880
GHZ0, GHZ1 = 2.40, 2.50
PX = (X1 - X0) / ((GHZ1 - GHZ0) * 1000.0)          # 픽셀 / MHz


def fx(ghz):
    return X0 + (ghz - GHZ0) * 1000.0 * PX


BARS = [
    ("원문이 적은 두 끝 값", 2.427, 2.429, BAD, "2 MHz"),
    ("22 MHz 라 부른 폭", 2.426, 2.448, ACC, "22 MHz · 채널 6"),
    ("견줌 — 채널 1", 2.401, 2.423, INFO, "22 MHz"),
]
BY, BH, STRIDE = 132, 32, 56
for i, (label, a, b, c, note) in enumerate(BARS):
    y = BY + i * STRIDE
    d.t(196, y + 21, label, 11, MUTED, KR, "end")
    xa, xb = fx(a), fx(b)
    d.tone(xa, y, max(xb - xa, 3), BH, c, 4, "22", 1.3)
    d.t(xb + 12, y + 21, note, 11, c, KR, "start", 600)
    if xb - xa < 40:
        d.t((xa + xb) / 2, y - 8, f"{a:.3f} ~ {b:.3f}", 10, SOFT, MONO)
    else:
        d.t(xa, y - 8, f"{a:.3f}", 10, SOFT, MONO)
        d.t(xb, y - 8, f"{b:.3f}", 10, SOFT, MONO)

AY = BY + len(BARS) * STRIDE + 8
d.line(X0, AY, X1, AY, RULE, 1.0)
for k in range(6):
    g = GHZ0 + k * 0.02
    x = fx(g)
    d.line(x, AY, x, AY + 6, RULE, 1.0)
    d.t(x, AY + 22, f"{g:.2f}", 10, SOFT, MONO)
d.t(X1, AY + 42, "GHz", 10, SOFT, MONO, "end")

PY = AY + 58
d.box(24, PY, 880, 96, PAPER2, RULE, 1.0)
d.t(44, PY + 26, "Hz 로 재는 대역폭과 bps 로 재는 전송률은 다른 말입니다", 12, INK, KR, "start", 600)
LINES = [
    "폭이 넓을수록 초당 보낼 수 있는 비트가 늘지만, 둘의 관계는 단순 비례가 아닙니다.",
    "원문의 예 — 20 MHz 폭 802.11n 채널은 최대 72.2 Mbps, 40 MHz 폭은 최대 150 Mbps.",
]
for j, ln in enumerate(LINES):
    d.t(44, PY + 52 + j * 20, ln, 11, MUTED, KR, "start")

d.legend(PY + 116, [("원문이 적은 구간", BAD), ("서술이 가리키는 실제 폭", ACC), ("견줌용 채널", INFO)])

out = pathlib.Path(__file__).resolve().parent.parent / "07-01.bandwidth-two-senses.svg"
d.save(out)
print("→", out)
