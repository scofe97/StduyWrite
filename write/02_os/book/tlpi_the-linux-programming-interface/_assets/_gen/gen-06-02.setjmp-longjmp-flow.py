# 06-02 §4 비로컬 점프 — setjmp 와 longjmp 를 통한 스택 언와인딩 흐름
# 근거: TLPI 6.8 Listing 6-5 (proc/longjmp.c), 06.txt 1234-1317
# 타입 스펙: type-sequence — main, f1, f2 간의 함수 호출과 longjmp 에 의한 일괄 복귀 및 반환값 변화
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 940, 530
d = D(W, H, "TLPI · 06-02 §4",
      "setjmp 와 longjmp 의 비로컬 점프 흐름",
      "중첩 함수 호출(main → f1 → f2)에서 longjmp(env, 2)를 통해 중간 프레임을 풀고 setjmp 위치로 직접 복귀하는 시퀀스",
      "초기 반환값 0으로 정상 흐름을 타고, longjmp 복귀 시 val(2)을 반환받아 에러 처리 케이스로 분기하는 구조")

# 세 참여자 레인 X 좌표
X_MAIN = 140
X_F1   = 430
X_F2   = 720

# 참여자 헤더 박스
actors = [
    (X_MAIN, "main()", "setjmp(env) 타깃 설정 · switch 분기"),
    (X_F1,   "f1()",   "중간 함수 (호출 스택 누적)"),
    (X_F2,   "f2()",   "에러 발생 지점 · longjmp(env, 2) 호출"),
]

Y_TOP = 104
for x, name, sub in actors:
    d.box(x - 90, Y_TOP, 180, 44, PAPER2, RULE, 1.0, 6)
    d.t(x, Y_TOP + 19, name, 13, INK, KR, "middle", 600)
    d.t(x, Y_TOP + 35, sub, 10, MUTED, KR)

# 수직 레일 (라이프라인)
Y_BOT = 464
for x in (X_MAIN, X_F1, X_F2):
    d.line(x, Y_TOP + 44, x, Y_BOT, RULE, 1.0, "3 4")

# 활성화 막대 (Activation bars)
d.box(X_MAIN - 6, 160, 12, 290, PAPER2, ACC, 1.2, 2)   # main 활성화
d.box(X_F1 - 5,   236, 10, 104, PAPER2, INFO, 1.0, 2)  # f1 활성화 (y=236 ~ 340)
d.box(X_F2 - 5,   282, 10, 58,  PAPER2, WARN, 1.0, 2)  # f2 활성화 (y=282 ~ 340)

# 1. main 내 setjmp(env) 최초 호출
d.selfmsg = lambda x, lab, y, c=MUTED, sub=None: (
    d.path(f"M {x+6} {y-10} L {x+46} {y-10} L {x+46} {y+10} L {x+8} {y+10}", c, 1.4, m="ar"),
    d.t(x+54, y-3, lab, 11, c, MONO, "start"),
    d.t(x+54, y+13, sub, 10, MUTED, KR, "start") if sub else None
)
d.selfmsg(X_MAIN, "setjmp(env) == 0", 172, ACC, "SP · PC 저장 / 초기 반환값 0")
d.chip(X_MAIN + 115, 202, "case 0 실행", OK, 11, 6)

# 2. main -> f1(argc) 호출
d.arrow([(X_MAIN + 6, 238), (X_F1 - 5, 238)], INFO, "info", 1.4)
d.t((X_MAIN + X_F1)/2, 228, "f1(argc) 호출", 11, INFO, KR, "middle", 500)
d.t((X_MAIN + X_F1)/2, 250, "스택 프레임 f1 생성", 10, MUTED, KR, "middle")

# 3. f1 -> f2() 호출
d.arrow([(X_F1 + 5, 284), (X_F2 - 5, 284)], WARN, "warn", 1.4)
d.t((X_F1 + X_F2)/2, 274, "f2() 호출", 11, WARN, KR, "middle", 500)
d.t((X_F1 + X_F2)/2, 296, "스택 프레임 f2 생성", 10, MUTED, KR, "middle")

# 4. f2 내 longjmp(env, 2) 실행
d.path(f"M {X_F2+5} 308 L {X_F2+45} 308 L {X_F2+45} 328 L {X_F2+7} 328", BAD, 1.4, m="bad")
d.t(X_F2 + 52, 316, "longjmp(env, 2)", 11, BAD, MONO, "start")
d.t(X_F2 + 52, 332, "에러 감지 / 비로컬 점프", 10, MUTED, KR, "start")

# 5. 비로컬 점프 (f2 -> main 으로 직접 복귀, 중간 스택 언와인딩)
d.arrow([(X_F2 - 5, 360), (X_MAIN + 6, 360)], BAD, "bad", 1.8, dash="4 3")
d.t((X_MAIN + X_F2)/2, 350, "스택 언와인딩 (f2, f1 프레임 일괄 파기)", 11, BAD, KR, "middle", 600)
d.t((X_MAIN + X_F2)/2, 372, "SP · PC 를 env 저장 값으로 복원", 10, MUTED, KR, "middle")

# 프레임 파기 표시 (활성화 막대 끝단 아래에 깔끔하게 배치)
d.chip(X_F1, 386, "f1 프레임 파기", BAD, 10, 5)
d.chip(X_F2, 386, "f2 프레임 파기", BAD, 10, 5)

# 6. main 에서 두 번째 반환 처리
d.selfmsg(X_MAIN, "setjmp(env) == 2", 412, BAD, "가짜 반환 / val 값 2 반환")
d.chip(X_MAIN + 120, 442, "case 2 실행 (에러 복구)", ACC, 11, 6)

d.legend(496, [
    ("정상 호출 (f1·f2)", INFO),
    ("비로컬 점프 (longjmp)", BAD),
    ("setjmp 타깃 / 분기", ACC),
    ("스택 언와인딩", MUTED)
])

d.save("06-02.setjmp-longjmp-flow.svg")
print("ok 06-02.setjmp-longjmp-flow.svg")
