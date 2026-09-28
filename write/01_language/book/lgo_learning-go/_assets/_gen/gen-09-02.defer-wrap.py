# 09-02.defer-wrap — 이름 붙은 반환 값 err 를 defer 클로저가 함수 끝에서 한 번 감싸는 순서
# 본문 요구(09-02 §4 「defer 로 같은 감싸기를 한 곳에 모읍니다」): DoSomeThings 는 오류를 감싸지 않고 return "", err 로 돌아간다.
#           함수가 끝나기 직전 defer 클로저가 이름 붙은 결과 변수 err 가 nil 이 아닌지 보고, fmt.Errorf("in DoSomeThings: %w", err) 로
#           다시 대입한다. 호출자는 감싼 오류를 받는다.
# 타입 스펙: type-sequence — 레인 3개(호출한 쪽 · DoSomeThings 본문 · defer 클로저), 시간은 위→아래, 메시지는 수평 화살표.
#           09-03.panic-recover 와 같은 방식. stride: 행 간격 60. focal 은 defer 클로저가 err 를 다시 대입하는 칩 하나.
# 사실 출처: Learning Go 2판 9장 「Wrapping Errors with defer」, go1.25.1 로컬 실행(2026-09-27) — in DoSomeThings: negative.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, BAD, INFO, PAPER2, KR, MONO

W, H = 984, 540
LANE_W = 232
LX = {"call": 152, "body": 492, "def": 832}
Y0, STRIDE = 104, 60


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


d = D(W, H, "SEQUENCE · 09-02 §4",
      "defer 가 함수 끝에서 err 를 한 번 감쌉니다",
      "DoSomeThings 를 부른 한 번을 시간순으로 그린 시퀀스. doThing2 가 오류를 돌려주면 본문은 감싸지 않고 return \"\", err 로 끝난다. "
      "함수가 돌아가기 직전 defer 클로저가 이름 붙은 결과 변수 err 가 nil 이 아님을 보고 fmt.Errorf 로 감싸 다시 대입한다. "
      "호출한 쪽은 in DoSomeThings: 가 붙은 오류를 받는다. doThing2 를 실패 지점으로 고른 것은 설명을 위한 예다.",
      lead="위에서 아래로 시간이 흐릅니다. 감싸는 코드는 defer 클로저 한 곳에만 있습니다.")

names = [("call", "호출한 쪽", "DoSomeThings(v1, v2)"), ("body", "DoSomeThings 본문", "(_ string, err error)"), ("def", "defer 클로저", "if err != nil")]
for key, title, sub in names:
    x = LX[key]
    d.box(x - LANE_W // 2, Y0, LANE_W, 48)
    d.t(x, Y0 + 20, title, 14, INK, kr(title), "middle", 600)
    d.t(x, Y0 + 38, sub, 12, MUTED, kr(sub), "middle")
    d.line(x, Y0 + 56, x, 460, RULE, 1.0, "3 6")


def msg(a, b, label, y, c=MUTED, mk="soft", sub=None):
    x1, x2 = LX[a], LX[b]
    dr = 1 if x2 > x1 else -1
    d.arrow([(x1 + 8 * dr, y), (x2 - 10 * dr, y)], c, mk, 1.5)
    d.t((x1 + x2) / 2, y - 10, label, 13, c if c != MUTED else INK, kr(label), "middle", 600)
    if sub:
        d.t((x1 + x2) / 2, y + 20, sub, 12, MUTED, kr(sub), "middle")


def chip(key, y, txt, c, w=232, focal=False):
    x = LX[key]
    d.o.append(f'<rect x="{x - w // 2}" y="{y - 14}" width="{w}" height="28" rx="4" fill="#0D1117"/>')
    d.tone(x - w // 2, y - 14, w, 28, c, 4, "22" if focal else "14", 1.4 if focal else 1.0)
    d.t(x, y + 5, txt, 12, c, kr(txt), "middle", 600)


y = Y0 + 96
msg("call", "body", "DoSomeThings(v1, v2)", y)
y += STRIDE
chip("body", y, "doThing2(val2) → err", BAD)
y += STRIDE
msg("body", "def", 'return "", err · 함수 끝', y, BAD, "bad", sub="감싸지 않은 채")
y += STRIDE
chip("def", y, "err = fmt.Errorf(…%w)", ACC, w=232, focal=True)
y += STRIDE
msg("def", "call", "in DoSomeThings: + 원래 오류", y, OK, "ok", sub="이름 붙은 err 가 그대로 반환됨")

d.legend(484, [("오류 경로", BAD), ("한 곳에서 감쌈", ACC), ("호출자가 받는 값", OK)])
d.save("09-02.defer-wrap.svg")
print("ok 09-02 defer-wrap")
