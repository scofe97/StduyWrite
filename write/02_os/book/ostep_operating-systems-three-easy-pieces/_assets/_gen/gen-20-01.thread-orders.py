# 20-01 「같은 프로그램, 세 가지 실행 순서」 — 스레드 두 개를 만들어 A 와 B 를 찍는 프로그램은 스케줄러 선택에 따라 출력 순서가 달라진다.
# 본문 근거: 이 노트 「3. 스레드 생성과 실행 순서」.
# 값 근거: OSTEP 26장 그림 26.3(스레드 추적 1), 그림 26.4(추적 2), 그림 26.5(추적 3)의 행 순서를 그대로 옮겼다.
# 공식 근거: OSTEP 26장 §26.2 — 만든 순서와 실행 순서는 무관하며 스케줄러가 정한다. 그림 26.5 에서는 스레드 2 가 먼저 돌아 B 가 A 보다 먼저 찍힌다.
# 타입 스펙: type-swimlane — 세로가 시간(아래로 흐름), 가로 세 열이 main·스레드 1·스레드 2. 세 추적을 나란히 맞대 열 안 행 위치로 순서 차이를 보인다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, PAPER2, ACC, OK, WARN, INFO, KR, MONO

W, H = 984, 520
d = D(W, H, "SWIMLANE · 20-01 §3",
      "스레드 둘을 만든 직후의 실행 순서는 세 가지가 모두 가능하다",
      "추적 1 은 main 이 스레드 둘을 만들고 기다린 뒤 스레드 1 이 A, 스레드 2 가 B 를 찍는다. "
      "추적 2 는 스레드 1 을 만든 직후 스레드 1 이 먼저 A 를 찍고, 이어 만든 스레드 2 가 B 를 찍은 뒤 main 이 기다리기 시작한다. "
      "추적 3 은 스레드 2 가 스레드 1 보다 먼저 돌아 B 가 A 보다 먼저 찍힌다.",
      lead="위에서 아래로 시간이 흐릅니다. 열은 왼쪽부터 main, 스레드 1, 스레드 2 입니다.")

TW = 304
GAP = 20
COLW = 96
ROWH = 28
TOPY = 148


def trace(k, title, rows):
    x0 = 12 + k * (TW + GAP)
    d.t(x0 + TW / 2, 100, title, 14, INK, KR, "middle", 600)
    for j, n in enumerate(("main", "스레드 1", "스레드 2")):
        cx = x0 + j * (COLW + 8)
        d.box(cx, 112, COLW, 24, PAPER2, RULE, 1.0, 4)
        d.t(cx + COLW / 2, 129, n, 13, MUTED, KR, "middle", 600)
        d.line(cx + COLW / 2, 140, cx + COLW / 2, TOPY + ROWH * len(rows) + 4, RULE, 0.8, "3 4")
    for i, (col, txt, c) in enumerate(rows):
        cx = x0 + col * (COLW + 8)
        y = TOPY + i * ROWH
        d.tone(cx, y, COLW, 24, c, 4, "1e" if c == ACC else "16", 1.0)
        d.t(cx + COLW / 2, y + 17, txt, 13, c, KR, "middle", 600 if c == ACC else 400)


M, A, B = INFO, ACC, ACC
rows1 = [(0, "begin 출력", M), (0, "T1 생성", M), (0, "T2 생성", M), (0, "T1 기다림", M),
         (1, "A 출력", A), (1, "반환", M), (0, "T2 기다림", M), (2, "B 출력", B), (2, "반환", M), (0, "end 출력", M)]
rows2 = [(0, "begin 출력", M), (0, "T1 생성", M), (1, "A 출력", A), (1, "반환", M), (0, "T2 생성", M),
         (2, "B 출력", B), (2, "반환", M), (0, "T1 기다림", M), (0, "T2 기다림", M), (0, "end 출력", M)]
rows3 = [(0, "begin 출력", M), (0, "T1 생성", M), (0, "T2 생성", M), (2, "B 출력", B), (2, "반환", M),
         (0, "T1 기다림", M), (1, "A 출력", A), (1, "반환", M), (0, "T2 기다림", M), (0, "end 출력", M)]
trace(0, "추적 1 — 만든 순서대로", rows1)
trace(1, "추적 2 — 만들자마자 실행", rows2)
trace(2, "추적 3 — 스레드 2 가 먼저", rows3)

d.legend(H - 40, [("생성·기다림·반환", INFO), ("출력 A·B", ACC)])
d.save("20-01.thread-orders.svg")
print("ok 20-01 thread-orders")
