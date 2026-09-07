# 타입 스펙: type-process — 소수 둘이 왼쪽에서 들어가 열쇠 쌍으로 나오는 한 방향 다섯 단계.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §8.2.2 RSA (책 569~570쪽) —
#   다섯 단계와 p=5·q=7·n=35·z=24·e=5·d=29 는 원문 예제 그대로이며 이 기계에서 재현했다.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, KR, MONO

W, H = 1000, 560
d = D(W, H, "SECTION 8.2.2 · RSA KEY GENERATION",
      "소수 둘에서 열쇠 쌍이 나옵니다",
      "다섯 단계가 전부다. 마지막에 공개할 쌍과 숨길 쌍이 갈린다.",
      "단계와 예제 수치는 원문 §8.2.2 의 것입니다")

BW, BH, BY = 176, 148, 148
XS = [24, 216, 408, 600, 792]
STEPS = [
    ("1", "큰 소수 둘", "p, q 를 고릅니다", "p = 5\nq = 7", INFO),
    ("2", "곱과 z", "n = pq\nz = (p−1)(q−1)", "n = 35\nz = 24", INFO),
    ("3", "e 고르기", "n 보다 작고\nz 와 서로소", "e = 5", INFO),
    ("4", "d 찾기", "ed mod z = 1", "d = 29\n5·29−1 = 144", INFO),
    ("5", "쌍 두 개", "공개 (n, e)\n비밀 (n, d)", "(35, 5)\n(35, 29)", ACC),
]
for x, (no, name, rule, val, c) in zip(XS, STEPS):
    if c is ACC:
        d.tone(x, BY, BW, BH, c, 7, "18", 1.4)
    else:
        d.box(x, BY, BW, BH, PAPER2, RULE, 1.0, 7)
    d.t(x + BW / 2, BY + 26, no, 10, SOFT, MONO)
    d.t(x + BW / 2, BY + 48, name, 12, c, KR, "middle", 600)
    d.line(x + 16, BY + 60, x + BW - 16, BY + 60, RULE, 0.8)
    for i, ln in enumerate(rule.split("\n")):
        d.t(x + BW / 2, BY + 82 + i * 18, ln, 11, MUTED, KR)
    for i, ln in enumerate(val.split("\n")):
        d.t(x + BW / 2, BY + 122 + i * 18, ln, 11, OK, MONO)
for a, b in zip(XS, XS[1:]):
    d.arrow([(a + BW + 2, BY + BH / 2), (b - 4, BY + BH / 2)], MUTED, "ar", 1.3)

EY = 336
d.box(24, EY, 952, 108, PAPER2, RULE, 1.0)
d.t(44, EY + 28, "쓰는 법은 거듭제곱 하나씩입니다", 12, INK, KR, "start", 600)
d.line(44, EY + 40, 956, EY + 40, RULE, 0.8)
d.t(44, EY + 68, "c = m^e mod n", 13, OK, MONO, "start", 600)
d.t(216, EY + 68, "앨리스가 암호화합니다 (m < n)", 11, MUTED, KR, "start")
d.t(44, EY + 92, "m = c^d mod n", 13, ACC, MONO, "start", 600)
d.t(216, EY + 92, "밥이 개인키로 복호합니다", 11, MUTED, KR, "start")
d.t(596, EY + 68, "l → 12 → 17 → 12", 11, SOFT, MONO, "start")
d.t(596, EY + 92, "e →  5 → 10 →  5", 11, SOFT, MONO, "start")

d.legend(464, [("계산 단계", INFO), ("공개할 쌍과 숨길 쌍", ACC), ("예제 값", OK)])
out = pathlib.Path(__file__).resolve().parent.parent / "08-02.rsa-keygen.svg"
d.save(out); print("→", out.name)
