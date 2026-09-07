# 타입 스펙: type-dp-security-matrix — 같은 격자에 두 입력을 놓고 열별 합이 같아지는 자리를 보인다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §8.3.1 Figure 8.8 (책 575쪽) —
#   두 문자열과 ASCII 값, 체크섬 B2 C1 D2 AC 는 원문 그대로이며 이 기계에서 재현했다.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, BAD, KR, MONO

W, H = 1000, 660
d = D(W, H, "SECTION 8.3.1 · WHY A CHECKSUM IS NOT ENOUGH",
      "다른 차용증이 같은 체크섬을 냅니다",
      "네 바이트씩 묶어 더하는 방식이라 자리만 바꾸면 열별 합이 그대로다. 그래서 위조를 못 막는다.",
      "두 문자열과 체크섬 값은 원문 Figure 8.8 의 것입니다")

MSGS = [("IOU100.99BOB", "49 4F 55 31|30 30 2E 39|39 42 4F 42", OK, "밥이 보낸 원본"),
        ("IOU900.19BOB", "49 4F 55 39|30 30 2E 31|39 42 4F 42", BAD, "밥에게 훨씬 비싼 위조본")]
X0, CW, CH = 232, 88, 44
Y0, GROUP = 172, 176
for gi, (text, rows, c, note) in enumerate(MSGS):
    gy = Y0 + gi * GROUP
    d.t(24, gy + 24, text, 13, c, MONO, "start", 600)
    d.t(24, gy + 46, note, 11, SOFT, KR, "start")
    for ri, row in enumerate(rows.split("|")):
        for ci, b in enumerate(row.split()):
            x, y = X0 + ci * CW, gy + ri * 34
            d.box(x, y, CW - 8, 30, PAPER2, RULE, 0.9, 4)
            d.t(x + (CW - 8) / 2, y + 20, b, 11, INK, MONO)
    d.t(X0 - 16, gy + 20, "묶음 1", 10, SOFT, KR, "end")
    d.t(X0 - 16, gy + 54, "묶음 2", 10, SOFT, KR, "end")
    d.t(X0 - 16, gy + 88, "묶음 3", 10, SOFT, KR, "end")
    d.line(X0, gy + 106, X0 + 4 * CW - 8, gy + 106, RULE, 1.0)
    for ci, b in enumerate("B2 C1 D2 AC".split()):
        x = X0 + ci * CW
        d.tone(x, gy + 114, CW - 8, 32, ACC, 4, "20", 1.3)
        d.t(x + (CW - 8) / 2, gy + 135, b, 12, ACC, MONO, "middle", 600)
    d.t(X0 + 4 * CW + 12, gy + 135, "열별 합", 11, ACC, KR, "start")

PY = 528
d.box(24, PY, 952, 60, PAPER2, RULE, 1.0)
d.t(44, PY + 26, "암호 해시 함수가 더 요구하는 것", 12, INK, KR, "start", 600)
d.t(44, PY + 48, "H(x) = H(y) 인 서로 다른 x 와 y 를 찾는 것이 계산상 불가능해야 합니다. 위 체크섬은 이 요구를 어깁니다.",
    11, MUTED, KR, "start")

d.legend(600, [("원본", OK), ("위조본", BAD), ("같아진 체크섬", ACC)])
out = pathlib.Path(__file__).resolve().parent.parent / "08-02.hash-vs-checksum.svg"
d.save(out); print("→", out.name)
