# 타입 스펙: type-flowchart — 단계가 이어지다 판단에서 갈리고, 한쪽이 처음으로 되돌아간다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §8.2.1 Figure 8.5 (책 564~565쪽) —
#   64비트 블록 · 8비트 여덟 조각 · 조각마다 8비트 대 8비트 표 · 자리 뒤섞기 · n 회차 · 회차의 목적은 원문 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, WARN, KR, MONO

W, H = 940, 660
d = D(W, H, "SECTION 8.2.1 · BLOCK CIPHER ROUNDS",
      "표로는 못 드는 것을 함수가 흉내 냅니다",
      "64비트 사상을 표로 들면 2^64 항목이 필요하다. 대신 작은 표 여덟 개와 뒤섞기를 여러 번 돌린다.",
      "조각 수와 표 크기와 회차의 목적은 원문 Figure 8.5 의 것입니다")

CX, BW, BH = 240, 320, 52
STEPS = [
    (140, "64비트 블록", "입력", INFO),
    (216, "8비트 조각 여덟 개로 나눔", "64 = 8 × 8", MUTED),
    (292, "조각마다 8비트 → 8비트 표", "T1 … T8 · 다룰 만한 크기", OK),
    (368, "여덟 조각을 64비트로 합침", "", MUTED),
    (444, "64 자리를 뒤섞음", "permute", MUTED),
]
for y, name, sub, c in STEPS:
    d.box(CX - BW / 2, y, BW, BH, PAPER2, RULE, 1.0, 7)
    d.t(CX, y + (24 if sub else 32), name, 12, c, KR, "middle", 600)
    if sub:
        d.t(CX, y + 42, sub, 11, SOFT, MONO)
for a, b in zip(STEPS, STEPS[1:]):
    d.arrow([(CX, a[0] + BH + 2), (CX, b[0] - 4)], MUTED, "ar", 1.3)

DY = 528
d.tone(CX - 132, DY, 264, 52, ACC, 7, "18", 1.4)
d.t(CX, DY + 22, "n 회차를 다 돌았습니까", 12, ACC, KR, "middle", 600)
d.t(CX, DY + 42, "rounds", 10, SOFT, MONO)
d.arrow([(CX, STEPS[-1][0] + BH + 2), (CX, DY - 4)], MUTED, "ar", 1.3)

d.path(f"M {CX - 136} {DY + 26} L 76 {DY + 26} L 76 {STEPS[1][0] + 26} L {CX - BW / 2 - 4} {STEPS[1][0] + 26}",
       ACC, 1.4, m="acc", dash="6 5")
d.t(80, DY - 12, "아니면 다시", 11, ACC, KR, "start")
d.arrow([(CX + 136, DY + 26), (CX + 232, DY + 26)], OK, "ok", 1.4)
d.t(CX + 244, DY + 30, "64비트 암호문", 12, OK, KR, "start", 600)

PX, PW = 592, 324
d.box(PX, 140, PW, 176, PAPER2, RULE, 1.0)
d.t(PX + 20, 168, "회차를 두는 이유", 12, INK, KR, "start", 600)
d.line(PX + 20, 180, PX + PW - 20, 180, RULE, 0.8)
for i, ln in enumerate([
    "입력 비트 하나가 출력 비트 대부분에",
    "영향을 주게 하기 위해서입니다.",
    "",
    "한 회차만 돌면 입력 비트 하나가",
    "64 개 출력 중 여덟 개에만 닿습니다.",
]):
    if ln:
        d.t(PX + 20, 206 + i * 22, ln, 11, MUTED, KR, "start")

d.box(PX, 340, PW, 148, PAPER2, RULE, 1.0)
d.t(PX + 20, 368, "열쇠는 무엇인가", 12, INK, KR, "start", 600)
d.line(PX + 20, 380, PX + PW - 20, 380, RULE, 0.8)
for i, ln in enumerate([
    "여덟 개의 순열 표입니다.",
    "뒤섞기 함수는 공개로 둡니다.",
    "",
    "DES 64/56 · AES 128/128·192·256",
]):
    if ln:
        d.t(PX + 20, 406 + i * 22, ln, 11, OK if i == 3 else MUTED, KR if i != 3 else MONO, "start")

d.legend(600, [("입력과 출력", INFO), ("작은 표로 대신함", OK), ("되돌아가는 판단", ACC)])
out = pathlib.Path(__file__).resolve().parent.parent / "08-01.block-cipher.svg"
d.save(out); print("→", out.name)
