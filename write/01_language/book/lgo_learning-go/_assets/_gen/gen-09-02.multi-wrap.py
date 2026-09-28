# 09-02.multi-wrap — %w 셋으로 묶은 오류는 가지가 셋인 트리라서 errors.Unwrap 은 nil, errors.Is 는 가지를 찾아간다
# 본문 요구(09-02 §2 「직접 만든 타입은 Unwrap() []error 를 구현합니다」): fmt.Errorf 에 %w 를 여러 개 넘기거나 errors.Join 을 쓰면
#           Unwrap() []error 를 구현한 오류가 된다. 이런 오류를 errors.Unwrap 에 넘기면 nil 이 돌아오고, errors.Is(err, err2) 는 true 다.
# 타입 스펙: type-tree — root 1 · 자식 3(leaf). root 폭 400, 자식 폭 256·간격 36, 층 간격 168, 직교 연결선.
#           오른쪽 위에 Unwrap 판정 칩, 가운데 자식 아래에 Is 판정 칩. focal 은 nil 을 돌려주는 Unwrap 칩 하나.
# 사실 출처: Learning Go 2판 9장 「Wrapping Multiple Errors」, go1.25.1 로컬 실행(2026-09-27) —
#           first: first error, second: second error, third: third error · errors.Is(err, err2) true · errors.Unwrap(err) nil.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, PAPER2, KR, MONO

W, H = 984, 524
RX, RY, RW, RH = 292, 132, 400, 76
CY, CW, CH, CG = 300, 256, 64, 36
CX0 = (W - (3 * CW + 2 * CG)) // 2          # 72
BUS_Y = RY + RH + 46                        # 254

d = D(W, H, "TREE · 09-02 §2",
      "%w 여럿으로 묶은 오류는 가지가 셋입니다",
      "fmt.Errorf 에 %w 를 셋 넘겨 만든 오류는 err1·err2·err3 를 가지로 둔 트리다. 이 오류는 Unwrap() []error 를 구현하므로 "
      "errors.Unwrap 에 넘기면 감싼 오류 하나가 아니라 nil 이 돌아온다. errors.Is(err, err2) 는 가지를 따라 내려가 err2 를 찾아 true 를 돌려준다.",
      lead="errors.Join 으로 묶어도 같은 모양입니다. 가지가 여럿이면 errors.Unwrap 은 답하지 않습니다.")

d.tone(RX, RY, RW, RH, INFO, 6, "14", 1.1)
d.t(RX + RW // 2, RY + 28, 'fmt.Errorf("first: %w, second: %w, …")', 13, INFO, MONO, "middle", 600)
d.t(RX + RW // 2, RY + 52, "Unwrap() []error 를 구현", 12, MUTED, KR, "middle")

d.line(RX + RW // 2, RY + RH, RX + RW // 2, BUS_Y, SOFT, 1.2)
cx = [CX0 + k * (CW + CG) + CW // 2 for k in range(3)]
d.line(cx[0], BUS_Y, cx[2], BUS_Y, SOFT, 1.2)
kids = [("err1", "first error"), ("err2", "second error"), ("err3", "third error")]
for k, (name, msg) in enumerate(kids):
    x = CX0 + k * (CW + CG)
    d.arrow([(cx[k], BUS_Y), (cx[k], CY - 4)], SOFT, "soft", 1.2)
    if k == 1:
        d.tone(x, CY, CW, CH, OK, 6, "14", 1.1)
    else:
        d.box(x, CY, CW, CH)
    d.t(x + CW // 2, CY + 26, name, 14, OK if k == 1 else INK, MONO, "middle", 600)
    d.t(x + CW // 2, CY + 46, msg, 12, MUTED, MONO, "middle")

d.tone(716, RY + 18, 236, 40, ACC, 4, "22", 1.4)
d.t(716 + 118, RY + 43, "errors.Unwrap(err) → nil", 12, ACC, MONO, "middle", 600)

d.tone(cx[1] - 128, CY + CH + 32, 256, 40, OK, 4, "14", 1.0)
d.t(cx[1], CY + CH + 57, "errors.Is(err, err2) → true", 12, OK, MONO, "middle", 600)
d.arrow([(cx[1], CY + CH + 30), (cx[1], CY + CH + 4)], OK, "ok", 1.2)

d.legend(468, [("묶은 오류", INFO), ("Is 가 찾은 가지", OK), ("Unwrap 이 답하지 않음", ACC)])
d.save("09-02.multi-wrap.svg")
print("ok 09-02 multi-wrap")
