# 09-03.panic-recover — div60(0) 의 panic 이 defer 안의 recover 로 붙잡혀 반복문이 이어지는 순서
# 본문 요구(09-03 §2 「recover — defer 안에서 panic 을 붙잡습니다」): 60 / 0 에서 panic 이 나면 div60 의 나머지는 건너뛰고
#           등록된 defer 만 실행된다. defer 안의 recover 가 값을 돌려받아 찍고, div60 은 정상 반환해 main 의 반복문이 6 으로 이어진다.
# 타입 스펙: type-sequence — 레인 3개(main 반복문 · div60(0) · defer 클로저), 시간은 위→아래, 메시지는 수평 화살표.
#           07-02.no-dispatch 와 같은 방식. stride: 행 간격 60. focal 은 recover 가 panic 값을 받는 자기 호출 하나.
# 사실 출처: Learning Go 2판 9장 「panic and recover」 div60 예제, go1.25.1 실행(2026-09-27) — 60 · 30 · runtime error: integer divide by zero · 10.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, BAD, INFO, PAPER2, KR, MONO

W, H = 984, 600
LANE_W = 232
LX = {"main": 152, "div": 492, "def": 832}
Y0, STRIDE = 104, 60


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


d = D(W, H, "SEQUENCE · 09-03 §2",
      "div60(0) 에서 panic 이 붙잡히는 순서",
      "반복문의 셋째 값 0 으로 div60 을 부른 한 번을 시간순으로 그린 시퀀스. 60 / 0 에서 panic 이 나면 div60 의 나머지는 실행되지 않고 등록된 defer 만 돈다. "
      "defer 안의 recover 가 panic 값 runtime error: integer divide by zero 를 돌려받아 찍으면 panic 은 멈추고, div60 은 정상으로 돌아가 반복문이 6 으로 이어진다.",
      lead="위에서 아래로 시간이 흐릅니다. recover 는 defer 안에서만 panic 을 붙잡습니다.")

names = [("main", "main 의 반복문", "1 · 2 · 0 · 6"), ("div", "div60(0)", "fmt.Println(60 / i)"), ("def", "defer 클로저", "recover()")]
for key, title, sub in names:
    x = LX[key]
    d.box(x - LANE_W // 2, Y0, LANE_W, 48)
    d.t(x, Y0 + 20, title, 14, INK, kr(title), "middle", 600)
    d.t(x, Y0 + 38, sub, 12, MUTED, kr(sub), "middle")
    d.line(x, Y0 + 56, x, 520, RULE, 1.0, "3 6")


def msg(a, b, label, y, c=MUTED, mk="soft", sub=None):
    x1, x2 = LX[a], LX[b]
    dr = 1 if x2 > x1 else -1
    d.arrow([(x1 + 8 * dr, y), (x2 - 10 * dr, y)], c, mk, 1.5)
    d.t((x1 + x2) / 2, y - 10, label, 13, c if c != MUTED else INK, kr(label), "middle", 600)
    if sub:
        d.t((x1 + x2) / 2, y + 20, sub, 12, MUTED, kr(sub), "middle")


def chip(key, y, txt, c, w=208, focal=False):
    x = LX[key]
    d.o.append(f'<rect x="{x - w // 2}" y="{y - 14}" width="{w}" height="28" rx="4" fill="#0D1117"/>')
    d.tone(x - w // 2, y - 14, w, 28, c, 4, "22" if focal else "14", 1.4 if focal else 1.0)
    d.t(x, y + 5, txt, 12, c, kr(txt), "middle", 600)


y = Y0 + 96
msg("main", "div", "div60(0)", y, sub="앞 두 번은 60 · 30 출력")
y += STRIDE
chip("div", y, "60 / 0 → panic", BAD)
y += STRIDE
msg("div", "def", "나머지는 건너뛰고 defer 실행", y, BAD, "bad")
y += STRIDE
chip("def", y, "recover() → 값 받음 · 출력", ACC, w=232, focal=True)
y += STRIDE
msg("def", "main", "panic 멈춤 · div60 정상 반환", y, OK, "ok")
y += STRIDE
chip("main", y, "div60(6) → 10", OK)

d.legend(548, [("panic 경로", BAD), ("recover 가 붙잡음", ACC), ("정상 흐름", OK)])
d.save("09-03.panic-recover.svg")
print("ok 09-03 panic-recover")
