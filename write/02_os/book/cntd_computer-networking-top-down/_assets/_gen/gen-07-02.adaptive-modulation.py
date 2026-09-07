# 타입 스펙: type-gantt — 축 위의 구간을 막대 길이로. 여기서는 시간축 대신 SNR 축을 쓴다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §7.2.2 Figure 7.17 아래 서술 —
#   BER 10^-4 목표에서 SNR 13 과 17 을 경계로 변조 방식이 갈린다는 값은 원문 그대로.
#   원문 그림의 BER 곡선 모양은 옮기지 않고, 본문이 명시한 경계값만 그린다.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, KR, MONO

W, H = 940, 528
d = D(W, H, "SECTION 7.2.2 · ADAPTIVE MODULATION",
      "채널이 나쁘면 덜 욕심냅니다",
      "같은 오류율 목표 아래에서 쓸 수 있는 변조 방식이 SNR 구간마다 다르다. 그래서 변조는 고정이 아니다.",
      "경계값 13 과 17 은 원문이 BER 10⁻⁴ 목표에서 든 값입니다")

X0, X1 = 208, 880
SMAX = 25.0


def fx(s):
    return X0 + (X1 - X0) * s / SMAX


BANDS = [
    ("4-QAM", 0.0, 13.0, INFO, "심볼당 2 비트"),
    ("16-QAM", 13.0, 17.0, OK, "심볼당 4 비트"),
    ("64-QAM", 17.0, 25.0, ACC, "심볼당 6 비트"),
]
BY, BH, STRIDE = 136, 36, 60
for i, (name, a, b, c, note) in enumerate(BANDS):
    y = BY + i * STRIDE
    d.t(196, y + 23, name, 12, c, KR, "end", 600)
    xa, xb = fx(a), fx(b)
    d.tone(xa, y, xb - xa, BH, c, 4, "22", 1.3)
    d.t((xa + xb) / 2, y + 23, note, 11, c, KR)

AY = BY + len(BANDS) * STRIDE + 4
d.line(X0, AY, X1, AY, RULE, 1.0)
for k in range(6):
    s = k * 5.0
    x = fx(s)
    d.line(x, AY, x, AY + 6, RULE, 1.0)
    d.t(x, AY + 22, f"{int(s)}", 10, SOFT, MONO)
d.t((X0 + X1) / 2, AY + 44, "수신 SNR (dB)", 11, MUTED, KR)
for s in (13.0, 17.0):
    d.line(fx(s), BY - 10, fx(s), AY, ACC, 1.0, "4 5")
    d.t(fx(s), BY - 18, f"{int(s)} dB", 10, ACC, MONO)

PY = AY + 62
d.box(24, PY, 880, 84, PAPER2, RULE, 1.0)
d.t(44, PY + 26, "항상 높은 차수를 쓰면 되지 않는 이유", 12, INK, KR, "start", 600)
for i, ln in enumerate([
    "차수가 높을수록 성상도의 점이 촘촘해져 잡음과 측정 오차가 더 자주 이웃 심볼로 넘어갑니다.",
    "그래서 송수신기는 SNR 과 BER 을 재서 서로에게 알리고, 변조 방식 변경을 맞춰야 합니다.",
]):
    d.t(44, PY + 52 + i * 20, ln, 11, MUTED, KR, "start")

d.legend(PY + 104, [("낮은 SNR 구간", INFO), ("중간 구간", OK), ("높은 SNR 구간과 경계값", ACC)])

out = pathlib.Path(__file__).resolve().parent.parent / "07-02.adaptive-modulation.svg"
d.save(out)
print("→", out)
