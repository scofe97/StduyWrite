# 27-01 §2 — 이벤트 루프가 SLOW 핸들러에서 sleep(2) 로 서 있으면, 0.3초 뒤에 도착한 TIME 요청은 그 핸들러가 끝난 뒤에야 답을 받는다(지연 1,709 ms).
# 본문 근거: 이 노트 「2. 루프를 세우는 블로킹 호출」 의 「루프 안 블로킹 호출의 대가」 소절.
# 검증 근거: Linux 7.2.12 에서 evsrv.c 의 SLOW 요청 진행 중 0.3초 뒤 들어온 TIME 이 1,709 ms 뒤에 답함(macOS 1,708 ms, 2026-11-08 macOS 재실행 1,702 ms).
#            응답 시각 약 2,009 ms 는 300 ms + 1,709 ms 로 계산한 값이다.
# 공식 근거: select(2) — 준비됨은 막히지 않고 I/O 를 할 수 있다는 뜻. 핸들러가 도는 동안 루프는 다음 select() 를 부르지 못한다.
# 타입 스펙: type-gantt — 시간 축 0~2,100 ms, 두 행(이벤트 루프·클라이언트 B), focal 막대는 B 의 응답 대기.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 340
X0, X1, TMAX = 200, 840, 2100          # 타임라인 영역, 최대 시간(ms)
ROW0, ROWH = 128, 56


def tx(ms):
    return X0 + ms * (X1 - X0) / TMAX


d = D(W, H, "OSTEP · 27-01 §2",
      "SLOW 핸들러가 끝날 때까지 TIME 요청은 기다린다",
      "시간 축은 0 ms 에서 2,100 ms 까지다. 이벤트 루프 행에서는 SLOW 핸들러가 sleep(2) 로 0 ms 부터 2,000 ms 까지 서 있다. "
      "클라이언트 B 는 300 ms 에 TIME 요청을 보냈지만 루프가 다음 이벤트를 꺼내지 못해, 약 2,009 ms 에 응답을 받았고 대기는 1,709 ms 였다.",
      "핸들러 하나가 자는 동안 루프의 모든 요청이 밀립니다")

# 시간 축
d.line(X0, 108, X1, 108, RULE, 0.8)
for ms in (0, 500, 1000, 1500, 2000):
    d.line(tx(ms), 104, tx(ms), 112, RULE, 0.8)
    d.t(tx(ms), 98, f"{ms:,} ms", 12, MUTED, MONO)

rows = [("이벤트 루프(evsrv)", 0), ("클라이언트 B", 1)]
for name, i in rows:
    y = ROW0 + i * ROWH
    d.t(20, y + 25, name, 13, INK, KR, "start", 600)

# 루프 행: SLOW 핸들러 0~2,000 ms, TIME 핸들러는 그 직후
y = ROW0 + 8
d.tone(tx(0), y, tx(2000) - tx(0), 28, SOFT, 4, "26", 1.1)
d.t(tx(0) + 12, y + 19, "SLOW 핸들러 · sleep(2)", 13, INK, KR, "start", 600)
d.tone(tx(2000), y, 8, 28, INFO, 2, "40", 1.1)
d.t(tx(2000) + 16, y + 19, "TIME", 12, MUTED, KR, "start")

# B 행: 300 ms 에 요청, 2,009 ms 에 응답
y = ROW0 + ROWH + 8
d.tone(tx(300), y, tx(2009) - tx(300), 28, ACC, 4, "26", 1.4)
d.t(tx(300) + 12, y + 19, "TIME 응답 대기 · 1,709 ms", 13, ACC, KR, "start", 600)

# 도착·응답 시각 표시선
for ms in (300, 2009):
    d.line(tx(ms), ROW0 + ROWH - 4, tx(ms), ROW0 + 2 * ROWH + 4, MUTED, 0.9, "4 4")
d.t(tx(300) - 6, ROW0 + 2 * ROWH + 24, "300 ms · TIME 도착", 12, MUTED, KR, "end")
d.t(tx(2009) + 6, ROW0 + 2 * ROWH + 24, "약 2,009 ms · 응답", 12, MUTED, KR, "end")

d.legend(284, [("루프가 서 있는 구간", SOFT), ("TIME 핸들러", INFO), ("B 가 기다린 구간", ACC)])
d.save("27-01.slow-timeline.svg")
print("ok 27-01 slow-timeline")
