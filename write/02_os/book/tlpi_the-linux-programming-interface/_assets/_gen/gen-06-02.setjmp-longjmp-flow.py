# 06-02 §4 비로컬 점프 — setjmp 와 longjmp 를 통한 스택 되감기 흐름
# 근거: TLPI 6.8 Listing 6-5 (proc/longjmp.c), 인자를 하나 주고 실행한 경우(./longjmp x) 의 출력 "We jumped back from f2()"
# 값 근거: 반환값 0 과 2 는 Listing 6-5 의 case 0·case 2, longjmp(env, 2) 는 f2() 의 호출이다.
# 타입 스펙: type-sequence — main, f1, f2 사이의 호출과 longjmp 에 의한 일괄 복귀
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 940, 700
X_MAIN, X_F1, X_F2 = 150, 455, 760
d = D(W, H, "TLPI · 06-02 §4",
      "setjmp 와 longjmp 의 비로컬 점프 흐름",
      "main() 이 setjmp 로 자리를 잡고 f1(), f2() 를 차례로 부른 뒤, f2() 의 longjmp 가 두 프레임을 건너뛰어 main() 으로 돌아오는 순서",
      "인자를 하나 주고 실행한 경우(./longjmp x)입니다. 이때 setjmp 는 두 번째 반환에서 2 를 돌려줍니다.")


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


Y_TOP = 104
for x, name, sub in ((X_MAIN, "main()", "setjmp 로 자리를 잡음"), (X_F1, "f1()", "중간 함수"), (X_F2, "f2()", "longjmp 를 부름")):
    d.box(x - 100, Y_TOP, 200, 48, PAPER2, RULE, 1.0, 6)
    d.t(x, Y_TOP + 21, name, 14, INK, MONO, "middle", 600)
    d.t(x, Y_TOP + 39, sub, 12, MUTED, KR)

Y_BOT = 624
for x in (X_MAIN, X_F1, X_F2):
    d.line(x, Y_TOP + 48, x, Y_BOT, RULE, 1.0, "3 5")

# 활성화 막대
d.box(X_MAIN - 6, 164, 12, 456, PAPER2, ACC, 1.2, 2)
d.box(X_F1 - 5, 256, 10, 184, PAPER2, INFO, 1.0, 2)
d.box(X_F2 - 5, 326, 10, 114, PAPER2, WARN, 1.0, 2)


def selfmsg(x, label, y, c, mk, sub):
    d.path(f"M {x + 6} {y - 10} L {x + 46} {y - 10} L {x + 46} {y + 10} L {x + 8} {y + 10}", c, 1.4, m=mk)
    d.t(x + 56, y - 2, label, 12, c, kr(label), "start", 600)
    d.t(x + 56, y + 16, sub, 12, MUTED, KR, "start")


selfmsg(X_MAIN, "setjmp(env) → 0", 188, ACC, "acc", "SP·PC 를 env 에 저장")
d.chip(X_MAIN + 118, 232, "case 0 : f1() 호출", OK, 12, 7)

d.arrow([(X_MAIN + 6, 276), (X_F1 - 5, 276)], INFO, "info", 1.4)
d.t((X_MAIN + X_F1) / 2, 266, "f1(argc)", 12, INFO, MONO, "middle", 600)
d.t((X_MAIN + X_F1) / 2, 296, "f1 프레임 생성", 12, MUTED, KR, "middle")

d.arrow([(X_F1 + 5, 346), (X_F2 - 5, 346)], WARN, "warn", 1.4)
d.t((X_F1 + X_F2) / 2, 336, "f2()", 12, WARN, MONO, "middle", 600)
d.t((X_F1 + X_F2) / 2, 366, "f2 프레임 생성", 12, MUTED, KR, "middle")

selfmsg(X_F2, "longjmp(env, 2)", 412, BAD, "bad", "비로컬 점프")

d.arrow([(X_F2 - 5, 468), (X_MAIN + 6, 468)], BAD, "bad", 1.8, dash="4 3")
d.t((X_MAIN + X_F2) / 2, 456, "스택 되감기 · f2, f1 프레임 파기", 12, BAD, KR, "middle", 600)
d.t((X_MAIN + X_F2) / 2, 490, "SP·PC 를 env 에 저장한 값으로", 12, MUTED, KR, "middle")
d.chip(X_F1, 530, "f1 프레임 파기", BAD, 12, 7)
d.chip(X_F2, 530, "f2 프레임 파기", BAD, 12, 7)

selfmsg(X_MAIN, "setjmp(env) → 2", 568, BAD, "bad", "두 번째 반환 · val 값")
d.chip(X_MAIN + 142, 606, "case 2 : f2() 에서 돌아옴", ACC, 12, 7)

d.legend(H - 40, [("정상 호출 (f1, f2)", INFO), ("비로컬 점프", BAD), ("setjmp 자리", ACC), ("프레임 파기", SOFT)])
d.save("06-02.setjmp-longjmp-flow.svg")
print("ok 06-02.setjmp-longjmp-flow.svg")
