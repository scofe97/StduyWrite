# 09-03.panic-unwind — panic 이 나면 현재 함수가 끝나고 defer 가 호출 사슬을 거슬러 실행된 뒤 프로그램이 끝나는 순서
# 본문 요구(09-03 §1 「panic — 런타임이 다음에 할 일을 모를 때 멈춥니다」): 원문은 panic 이 나면 현재 함수가 곧바로 끝나고
#           그 함수의 defer 들이, 이어서 호출한 함수의 defer 들이 main 에 이를 때까지 실행된 뒤 메시지와 스택 트레이스를 찍고
#           끝난다고 말한다. main → f → g 사슬은 설명을 위한 예다.
# 타입 스펙: type-sequence — 레인 3개(main · f · g), 시간은 위→아래, 메시지는 수평 화살표. 09-03.panic-recover 와 같은 방식.
#           stride: 행 간격 56. focal 은 프로그램이 끝나는 마지막 칩 하나.
# 사실 출처: Learning Go 2판 9장 「panic and recover」.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, BAD, INFO, PAPER2, KR, MONO

W, H = 984, 684
LANE_W = 232
LX = {"main": 152, "f": 492, "g": 832}
Y0, STRIDE = 104, 56


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


d = D(W, H, "SEQUENCE · 09-03 §1",
      "panic 은 defer 를 거슬러 실행하고 끝납니다",
      "main 이 f 를, f 가 g 를 부른 호출 사슬에서 g 가 panic 을 낸 경우. g 는 곧바로 끝나고 g 의 defer 가 실행된다. "
      "이어 f 의 나머지는 건너뛰고 f 의 defer 가, 마지막으로 main 의 defer 가 실행된다. recover 가 없으면 프로그램은 메시지와 스택 트레이스를 찍고 끝난다.",
      lead="main → f → g 는 설명을 위한 예입니다. recover 가 없을 때의 순서입니다.")

for key, title, sub in [("main", "main", "defer A"), ("f", "f()", "defer B"), ("g", "g()", "defer C")]:
    x = LX[key]
    d.box(x - LANE_W // 2, Y0, LANE_W, 48)
    d.t(x, Y0 + 20, title, 14, INK, MONO, "middle", 600)
    d.t(x, Y0 + 38, sub, 12, MUTED, MONO, "middle")
    d.line(x, Y0 + 56, x, 604, RULE, 1.0, "3 6")


def msg(a, b, label, y, c=MUTED, mk="soft"):
    x1, x2 = LX[a], LX[b]
    dr = 1 if x2 > x1 else -1
    d.arrow([(x1 + 8 * dr, y), (x2 - 10 * dr, y)], c, mk, 1.5)
    d.t((x1 + x2) / 2, y - 10, label, 13, c if c != MUTED else INK, kr(label), "middle", 600)


def chip(key, y, txt, c, w=216, focal=False):
    x = LX[key]
    d.o.append(f'<rect x="{x - w // 2}" y="{y - 14}" width="{w}" height="28" rx="4" fill="#0D1117"/>')
    d.tone(x - w // 2, y - 14, w, 28, c, 4, "22" if focal else "14", 1.4 if focal else 1.0)
    d.t(x, y + 5, txt, 12, c, kr(txt), "middle", 600)


y = Y0 + 92
msg("main", "f", "f()", y)
y += STRIDE
msg("f", "g", "g()", y)
y += STRIDE
chip("g", y, "panic · g 의 나머지 건너뜀", BAD, w=224)
y += STRIDE
chip("g", y, "defer C 실행", INFO)
y += STRIDE
msg("g", "f", "panic 이 거슬러 올라감", y, BAD, "bad")
y += STRIDE
chip("f", y, "f 의 나머지 건너뜀 · defer B", INFO, w=232)
y += STRIDE
msg("f", "main", "panic 이 거슬러 올라감", y, BAD, "bad")
y += STRIDE
chip("main", y, "defer A → 스택 트레이스 · 종료", ACC, w=232, focal=True)

d.legend(628, [("panic 경로", BAD), ("defer 실행", INFO), ("프로그램 종료", ACC)])
d.save("09-03.panic-unwind.svg")
print("ok 09-03 panic-unwind")
