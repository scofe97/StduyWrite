# 06-03 §2 인자·환경 크기 한도 — execve() 가 한도를 계산하고 두 경우에 E2BIG 로 실패시키는 판단 흐름. 두 검사의 선후는 man page 에 없다(도식의 순서는 설명용 배치).
# 본문 근거: 이 노트 「2. main 외부에서의 인자 접근과 크기 상한」의 「인자와 환경 목록의 저장 위치와 ARG_MAX 상한」.
# 값 근거: 합계 한도 = 소프트 RLIMIT_STACK 의 1/4, 6MB(_STK_LIM 8MB 의 3/4) 이하, 32페이지 이상, 문자열 하나는 32페이지 이하(MAX_ARG_STRLEN).
# 공식 근거: execve(2) 「Limits on size of arguments and environment」·ERRORS 의 E2BIG (Linux man-pages 6.19 조회 2026-11-19).
# 타입 스펙: type-flowchart — 판단 분기. 마름모는 판단(출구 둘, 모든 출구에 라벨), 사각형은 단계와 결과. 코랄은 한도를 정하는 핵심 단계에만 쓴다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INK, MUTED, SOFT, RULE, PAPER, PAPER2, OK, WARN, INFO, KR, MONO

W, H = 880, 700
d = D(W, H, "TLPI · 06-03 §2",
      "인자와 환경이 한도를 넘으면 execve() 는 E2BIG 로 실패한다",
      "execve() 는 호출 시점의 소프트 RLIMIT_STACK 으로 합계 한도를 정한다. 합계가 한도를 넘거나 문자열 하나가 32페이지를 넘으면 E2BIG 로 실패하고, 넘지 않으면 새 프로그램이 시작된다.")

CX = 300


def step(y, h, title, sub=None, c=None):
    if c:
        d.tone(CX - 170, y, 340, h, c, 6, "14", 1.4 if c == ACC else 1.1)
    else:
        d.box(CX - 170, y, 340, h, PAPER2, RULE, 1.0, 6)
    if sub:
        d.t(CX, y + 22, title, 13, c or INK, KR, "middle", 600)
        d.t(CX, y + 42, sub, 12, MUTED, MONO if sub.isascii() else KR)
    else:
        d.t(CX, y + h / 2 + 5, title, 13, c or INK, KR, "middle", 600)


def diamond(cy, l1, l2, hw=170, hh=46):
    d.o.append(f'<polygon points="{CX},{cy-hh} {CX+hw},{cy} {CX},{cy+hh} {CX-hw},{cy}" fill="{PAPER2}" stroke="{MUTED}" stroke-width="1.1"/>')
    d.t(CX, cy - 2, l1, 12, INK, KR, "middle", 600)
    d.t(CX, cy + 16, l2, 12, INK, MONO if l2.isascii() else KR, "middle", 600)


step(96, 56, "execve() 호출", "그 시점의 소프트 RLIMIT_STACK 을 읽음", INFO)
d.arrow([(CX, 152), (CX, 172)], MUTED, "ar", 1.4)
step(172, 56, "합계 한도 = RLIMIT_STACK ÷ 4", "새 프로그램의 스택 몫을 남겨 둠", ACC)
d.arrow([(CX, 228), (CX, 252)], MUTED, "ar", 1.4)
step(252, 56, "한도를 6MB 이하, 32페이지 이상으로 맞춤", "6MB = _STK_LIM(8MB) 의 3/4", INFO)
d.arrow([(CX, 308), (CX, 332)], MUTED, "ar", 1.4)

C1, C2 = 380, 500
diamond(C1, "인자 + 환경 합계가", "한도 이하인가")
d.arrow([(CX, C1 + 46), (CX, C2 - 46)], OK, "ok", 1.4)
d.chip(CX + 22, (C1 + 46 + C2 - 46) / 2, "예", OK, 12, 8)
diamond(C2, "문자열 하나가", "32페이지 이하인가")
d.arrow([(CX, C2 + 46), (CX, 590)], OK, "ok", 1.4)
d.chip(CX + 22, (C2 + 46 + 590) / 2, "예", OK, 12, 8)
d.tone(CX - 170, 590, 340, 40, OK)
d.t(CX, 615, "새 프로그램 시작 · 스택 위에 문자열 복사", 13, INK, KR, "middle", 600)

# E2BIG
EX = 720
d.tone(EX - 110, C1 + 20, 220, 80, WARN)
d.t(EX, C1 + 52, "execve() 실패", 13, WARN, KR, "middle", 600)
d.t(EX, C1 + 72, "-1 을 돌려주고 errno 는 E2BIG", 12, MUTED, KR)
d.arrow([(CX + 170, C1), (EX, C1), (EX, C1 + 18)], WARN, "warn", 1.4)
d.chip((CX + 170 + EX) / 2, C1, "아니오", WARN, 12, 8)
d.arrow([(CX + 170, C2), (EX, C2), (EX, C1 + 102)], WARN, "warn", 1.4)
d.chip((CX + 170 + EX) / 2, C2, "아니오", WARN, 12, 8)

d.legend(H - 56, [("단계", INFO), ("한도 계산", ACC), ("통과", OK), ("실패", WARN)])
d.save("06-03.arg-size-limit.svg")
print("ok 06-03 arg-size-limit")
