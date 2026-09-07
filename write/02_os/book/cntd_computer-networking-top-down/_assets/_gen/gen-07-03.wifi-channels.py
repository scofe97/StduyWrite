# 타입 스펙: type-gantt — 축 위의 구간을 막대 길이로. 여기서는 시간축 대신 주파수축을 쓴다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §7.3.2 Figure 7.23(a) —
#   2.4 GHz 대역의 채널 11 개와 각 20 MHz 폭, 그리고 1·6·11 이라는 결론은 원문 그대로.
#   채널 중심 주파수는 그림의 눈금(2.40~2.48 GHz)과 5 MHz 간격에서 산출했다.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, BAD, KR, MONO

W, H = 940, 600
d = D(W, H, "SECTION 7.3.2 · WIFI CHANNELS IN 2.4 GHZ",
      "열한 채널 중 셋만 서로 겹치지 않습니다",
      "채널은 5 MHz 간격으로 놓이는데 폭은 20 MHz 다. 그래서 번호가 가까운 채널끼리는 서로 간섭한다.",
      "채널 수와 폭, 그리고 1·6·11 이라는 결론은 원문 Figure 7.23(a) 의 것입니다")

X0, X1 = 128, 872
F0, F1 = 2.398, 2.486
PXMHZ = (X1 - X0) / ((F1 - F0) * 1000.0)


def fx(ghz):
    return X0 + (ghz - F0) * 1000.0 * PXMHZ


CENTERS = {k: 2.407 + 0.005 * k for k in range(1, 12)}
BY, RH, STRIDE = 122, 16, 20
PICK = {1, 6, 11}
for k in range(1, 12):
    y = BY + (k - 1) * STRIDE
    c = ACC if k in PICK else MUTED
    d.t(116, y + 12, str(k), 10, c, MONO, "end", 600 if k in PICK else 400)
    lo, hi = CENTERS[k] - 0.010, CENTERS[k] + 0.010
    d.tone(fx(lo), y, fx(hi) - fx(lo), RH, c, 3, "22" if k in PICK else "10", 1.2 if k in PICK else 0.8)

AY = BY + 11 * STRIDE + 8
d.line(X0, AY, X1, AY, RULE, 1.0)
for k in range(5):
    g = 2.40 + k * 0.02
    x = fx(g)
    d.line(x, AY, x, AY + 6, RULE, 1.0)
    d.t(x, AY + 22, f"{g:.2f}", 10, SOFT, MONO)
d.t(X1, AY + 42, "GHz", 10, SOFT, MONO, "end")
d.t(112, BY - 14, "채널 번호", 10, SOFT, KR, "end")

PY = AY + 58
d.box(24, PY, 430, 118, PAPER2, RULE, 1.0)
d.t(44, PY + 26, "원문이 적은 기준 — 넷 이상 떨어지면", 12, BAD, KR, "start", 600)
for i, ln in enumerate([
    "1·5·9 도 조건을 만족합니다.",
    "그런 세 채널 조합이 모두 10 가지 나옵니다.",
    "그래서 1·6·11 이 유일하다는 말과 안 맞습니다.",
]):
    d.t(44, PY + 52 + i * 20, "·  " + ln, 11, MUTED, KR, "start")

d.box(474, PY, 430, 118, PAPER2, RULE, 1.0)
d.t(494, PY + 26, "다섯 이상 떨어지면", 12, ACC, KR, "start", 600)
for i, ln in enumerate([
    "간격 5 채널은 25 MHz 라 폭 20 MHz 를 넘습니다.",
    "1 에서 11 사이에서 조건을 만족하는 조합은",
    "1·6·11 하나뿐입니다.",
]):
    d.t(494, PY + 52 + i * 20, "·  " + ln, 11, MUTED, KR, "start")

d.legend(PY + 138, [("겹치지 않는 세 채널", ACC), ("나머지 채널", MUTED), ("원문의 기준으로는 유일하지 않음", BAD)])

out = pathlib.Path(__file__).resolve().parent.parent / "07-03.wifi-channels.svg"
d.save(out)
print("→", out)
