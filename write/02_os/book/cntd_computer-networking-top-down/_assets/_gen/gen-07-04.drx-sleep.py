# 타입 스펙: type-gantt — 작업과 국면을 시간축 위에. 막대 길이가 곧 그 상태로 머문 구간이다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §7.3.6 Figure 7.38 —
#   t0~t5 의 사건 순서와 지연이 t5-t3 이라는 결론은 원문 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, WARN, KR, MONO

W, H = 940, 600
d = D(W, H, "SECTION 7.3.6 · DISCONTINUOUS RECEPTION",
      "짧게 자다가 길게 자고, 그만큼 늦게 깹니다",
      "무전기를 계속 켜 두지 않으려면 잠들어야 한다. 깊이 잘수록 전력은 아끼지만 도착한 패킷이 오래 기다린다.",
      "사건 순서와 지연 정의는 원문 Figure 7.38 의 것입니다")

X0, X1 = 176, 872
TMAX = 100.0


def fx(t):
    return X0 + (X1 - X0) * t / TMAX


BARS = [
    ("활성", OK, [(0, 12), (88, 100)]),
    ("짧은 DRX 주기", INFO, [(12, 20), (21, 29), (30, 38)]),
    ("긴 DRX 주기", ACC, [(40, 62), (64, 86)]),
]
BY, BH, STRIDE = 132, 34, 54
for i, (name, c, spans) in enumerate(BARS):
    y = BY + i * STRIDE
    d.t(164, y + 22, name, 11, c, KR, "end", 600)
    for a, b in spans:
        d.tone(fx(a), y, fx(b) - fx(a), BH, c, 4, "22", 1.3)

AY = BY + len(BARS) * STRIDE + 6
d.line(X0, AY, X1, AY, RULE, 1.0)
EVENTS = [(2, "t0", "기지국에서 수신 · 활동 타이머 시작"),
          (12, "t1", "타이머 만료 · 짧은 잠으로"),
          (40, "t2", "긴 잠으로"),
          (62, "t3", "패킷 도착 · 기지국이 버퍼링"),
          (88, "t4", "긴 주기 끝 · 깨어남"),
          (94, "t5", "전송 수신 · 타이머 재시작")]
for t, lab, desc in EVENTS:
    x = fx(t)
    d.line(x, BY - 8, x, AY, SOFT, 0.9, "3 5")
    d.t(x, BY - 16, lab, 10, SOFT, MONO)
for i, (t, lab, desc) in enumerate(EVENTS):
    col = i % 2
    row = i // 2
    d.t(24 + col * 460, AY + 34 + row * 20, f"{lab}  {desc}", 10, MUTED, KR, "start")

LY = AY + 100
d.line(fx(62), LY, fx(94), LY, WARN, 1.8)
d.line(fx(62), LY - 8, fx(62), LY + 8, WARN, 1.8)
d.line(fx(94), LY - 8, fx(94), LY + 8, WARN, 1.8)
d.t((fx(62) + fx(94)) / 2, LY + 26, "잠 때문에 늘어난 지연 = t5 − t3", 11, WARN, KR, "middle", 600)

PY = LY + 46
d.box(24, PY, 880, 84, PAPER2, RULE, 1.0)
d.t(44, PY + 26, "숫자로 보면 잠을 안 잘 이유가 없습니다", 12, INK, KR, "start", 600)
for i, ln in enumerate([
    "LTE 무전기는 보내거나 받거나 기다릴 때 1,000 에서 3,500 mW 를 쓰고, 꺼져 있을 때는 15 mW 미만입니다.",
    "인기 앱을 돌리는 4G·5G 기기에서 통신이 쓰는 에너지가 전체의 20 에서 50 퍼센트를 넘습니다.",
]):
    d.t(44, PY + 52 + i * 20, ln, 11, MUTED, KR, "start")

d.legend(PY + 104, [("깨어 있음", OK), ("짧은 잠", INFO), ("긴 잠", ACC), ("늘어난 지연", WARN)])

out = pathlib.Path(__file__).resolve().parent.parent / "07-04.drx-sleep.svg"
d.save(out)
print("→", out)
