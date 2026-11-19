# 21-01 「스레드 하나가 지나는 다섯 단계」 — 만든다·기다린다·막는다·알린다·빌드한다를 단계마다 같은 칸(함수·받치는 개념·맡는 절)으로 보인다.
# 본문 근거: 이 노트 「스레드 API 한 바퀴」 표와 1~5절.
# 값 근거: 개념 도식이라 값은 없다. 함수 이름은 OSTEP 27장에 나오는 것만 쓴다.
# 공식 근거: OSTEP 27장 §27.1~27.5 — 생성 pthread_create, 완료 pthread_join, 락 pthread_mutex_lock·unlock, 조건 변수 pthread_cond_wait·signal, 컴파일 -pthread.
# 타입 스펙: type-process — semantic-patterns 의 「Stage framework with semantic slots」. 주체 없이 단계 칸마다 같은 슬롯(함수·개념·절)이 반복되고 화살표는 읽는 순서만 나른다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INK, MUTED, SOFT, RULE, PAPER, PAPER2, OK, INFO, WARN, KR, MONO

W, H = 880, 372
d = D(W, H, "OSTEP · 21-01 OVERVIEW",
      "스레드 하나가 지나는 다섯 단계",
      "pthread 라이브러리의 함수를 만든다, 기다린다, 막는다, 알린다, 빌드한다의 다섯 단계로 묶어 보인다. "
      "단계마다 함수 하나, 그 함수가 받치는 개념, 그 내용을 다루는 절이 같은 칸에 놓인다.")

X0, CW, GAP, Y0, CH = 24, 148, 24, 100, 188
stages = [
    ("1 만든다", "pthread_create", "시작 함수 · void *", "1절", INFO),
    ("2 기다린다", "pthread_join", "반환값 · 스택 수명", "2절", INFO),
    ("3 막는다", "pthread_mutex_lock", "임계 구역 · 상호 배제", "3절", WARN),
    ("4 알린다", "pthread_cond_wait", "조건 변수 · 락의 짝", "4절", ACC),
    ("5 빌드한다", "-pthread", "링크 옵션 · 지침", "5절", OK),
]
for i, (title, api, concept, sec, c) in enumerate(stages):
    x = X0 + i * (CW + GAP)
    d.tone(x, Y0, CW, CH, c)
    d.t(x + CW / 2, Y0 + 28, title, 14, INK, KR, "middle", 600)
    d.line(x + 12, Y0 + 44, x + CW - 12, Y0 + 44, RULE, 0.6)
    d.t(x + 12, Y0 + 68, "함수", 12, MUTED, KR, "start")
    d.t(x + 12, Y0 + 90, api, 11, INK, MONO, "start")
    d.t(x + 12, Y0 + 120, "받치는 개념", 12, MUTED, KR, "start")
    d.t(x + 12, Y0 + 142, concept, 12, INK, KR, "start")
    d.chip(x + CW / 2, Y0 + CH - 20, sec + " 에서 다룸", c, 12, 8)
    if i < len(stages) - 1:
        ay = Y0 + CH / 2
        d.arrow([(x + CW, ay), (x + CW + GAP, ay)], MUTED, "ar", 1.4)

d.legend(H - 56, [("생성과 대기", INFO), ("락", WARN), ("조건 변수", ACC), ("빌드", OK)])
d.save("21-01.chapter-overview.svg")
print("ok 21-01 chapter-overview")
