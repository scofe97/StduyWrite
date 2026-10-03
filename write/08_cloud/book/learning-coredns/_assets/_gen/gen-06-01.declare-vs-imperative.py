# 06-01 §2 — 프로세스가 죽었을 때 명령형 구현은 모르고, 선언형 구현은 알아채 다시 띄운다.
# 본문 근거: 이 노트 §2 「선언형 API 는 결과를 약속합니다」 의 저자 예(가상의 프로세스 실행 API).
#            원서 영문을 대조하지 못해 영문 인용은 싣지 않는다. 가로축은 시각이 아니라 사건 순서다.
# 타입 스펙: type-gantt — 같은 사건(프로세스 죽음) 뒤 두 막대가 끊기느냐 이어지느냐가 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, RULE, OK, BAD, WARN, KR, MONO

W, H = 880, 440
d = D(W, H, "LEARNING COREDNS · 06-01 §2",
      "프로세스가 죽은 뒤 누가 알아채는가",
      "명령형 API 는 명령을 실행하고 끝나므로 프로세스가 죽어도 모른다. 선언형 API 는 바라는 상태를 받아 두고 "
      "감시하다가 죽으면 다시 띄운다. 가로축은 시각이 아니라 사건의 순서다.",
      "주황 막대가 선언형만 하는 일입니다")

TX, TW = 220, 620
COLS = ["요청", "실행 중", "프로세스 죽음", "그 뒤"]
P = TW / 4


def X(c):
    return TX + P * c


for i, nm in enumerate(COLS):
    d.t(X(i) + P / 2, 118, nm, 12, BAD if i == 2 else SOFT, KR)
d.line(TX, 128, TX + TW, 128, RULE, 1.0)


def bar(c0, c1, y, color, label, op="16"):
    d.box(X(c0) + 4, y, X(c1) - X(c0) - 8, 30, PAPER, "none", 0, 4)
    d.tone(X(c0) + 4, y, X(c1) - X(c0) - 8, 30, color, 4, op, 1.2)
    d.t(X(c0) + 16, y + 20, label, 12, color, KR, "start")


lanes = [(156, "명령형", "실행하고 끝"), (246, "선언형", "항상 떠 있어야 한다")]
for y, nm, sub in lanes:
    d.t(20, y + 12, nm, 14, INK, KR, "start", 600)
    d.t(20, y + 32, sub, 12, MUTED, KR, "start")

bar(0, 2, 156, OK, "실행 중")
bar(2, 4, 156, BAD, "죽은 채 · 서버는 모른다")

bar(0, 2, 246, OK, "실행 중")
bar(2, 2.5, 246, WARN, "감지")
bar(2.5, 4, 246, ACC, "다시 띄움 · 실행 중")

d.line(X(2), 140, X(2), 300, BAD, 1.2, "4 4")

d.path(f"M {X(2) + 4} 296 L {X(2) + 4} 304 L {X(4) - 4} 304 L {X(4) - 4} 296", ACC, 1.4)
d.t((X(2) + X(4)) / 2, 324, "의도를 담은 자원이 남아 있는 한 되풀이", 13, ACC, KR, "middle", 600)

d.t(20, 368, "그래서 선언형 API 를 의도 기반 API 라고도 부른다", 13, MUTED, KR, "start")

d.legend(388, [("돌고 있음", OK), ("죽은 채 방치", BAD), ("선언형이 메우는 구간", ACC)])
d.save("06-01.declare-vs-imperative.svg")
