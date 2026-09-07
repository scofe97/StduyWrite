# 타입 스펙: type-bar — 세 고전 암호의 열쇠 공간을 같은 축에서 비교한다. 로그 축임을 축 라벨에 밝힌다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §8.2.1 (책 562~563쪽) —
#   카이사르 25 가지, 단일문자 26! (10^26 규모), 이름 둘로 일곱 자리가 확정되면 10^9 배 줄어든다는 서술 그대로.
#   19! 값은 그 서술을 이 기계에서 검산한 것이다.
import sys, pathlib, math
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, WARN, BAD, KR, MONO

W, H = 940, 684
d = D(W, H, "SECTION 8.2.1 · CLASSICAL CIPHERS",
      "열쇠 공간을 키워도 통계가 깨뜨립니다",
      "가로 막대는 열쇠 후보의 개수를 상용로그로 잰 것이다. 셋째 막대가 무너진 자리를 보여 준다.",
      "25 · 26! · 10^9 배 감소는 원문 서술이고 19! 은 검산값입니다")

BARS = [
    ("카이사르", "이동량 k 하나", 25, "25 가지 — 손으로도 다 해 봅니다", BAD),
    ("단일문자", "26 자리의 순열", math.factorial(26), "약 4.03×10^26 — 전수 조사는 불가능합니다", INFO),
    ("이름 둘이 새면", "일곱 자리가 확정된 뒤", math.factorial(19), "약 1.22×10^17 — 10^9 배 줄었습니다", ACC),
]
X0, BY, BH, STRIDE = 216, 180, 44, 84
MAXL = math.log10(math.factorial(26))
SPAN = 560

for i, (name, sub, val, note, c) in enumerate(BARS):
    y = BY + i * STRIDE
    w = max(24, SPAN * math.log10(val) / MAXL)
    d.t(X0 - 16, y + 20, name, 12, c, KR, "end", 600)
    d.t(X0 - 16, y + 38, sub, 11, SOFT, KR, "end")
    d.tone(X0, y, w, BH, c, 5, "22" if c is ACC else "16", 1.4 if c is ACC else 1.1)
    d.t(X0 + 12, y + BH + 20, note, 11, MUTED, KR, "start")

AY = BY + len(BARS) * STRIDE + 8
d.line(X0, AY, X0 + SPAN, AY, RULE, 1.0)
for k in (0, 5, 10, 15, 20, 25):
    x = X0 + SPAN * k / MAXL
    d.line(x, AY - 4, x, AY + 4, RULE, 0.8)
    d.t(x, AY + 20, f"10^{k}", 10, SOFT, MONO)
d.t(X0 + SPAN / 2, AY + 44, "열쇠 후보의 개수 (상용로그 축)", 11, SOFT, KR)

PY = AY + 68
d.box(24, PY, 892, 96, PAPER2, RULE, 1.0)
d.t(44, PY + 28, "크기가 안전을 만들지 않습니다", 12, INK, KR, "start", 600)
d.line(44, PY + 40, 896, PY + 40, RULE, 0.8)
for i, ln in enumerate([
    "영어에서 e 와 t 가 글자 출현의 13퍼센트와 9퍼센트를 차지하고 in · it · the · ion · ing 이 자주 붙어 나옵니다.",
    "본문에 bob 과 alice 가 있다고 짐작만 해도 26 자리 중 일곱이 확정됩니다. 둘째 막대가 셋째로 내려앉습니다.",
]):
    d.t(44, PY + 64 + i * 20, ln, 11, MUTED, KR, "start")

d.legend(PY + 116, [("통계 없이도 깨짐", BAD), ("전수 조사로는 못 깸", INFO), ("통계가 깨뜨린 뒤", ACC)])
out = pathlib.Path(__file__).resolve().parent.parent / "08-01.classical-ciphers.svg"
d.save(out); print("→", out.name)
