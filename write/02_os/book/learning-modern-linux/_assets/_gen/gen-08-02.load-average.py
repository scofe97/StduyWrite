# 08-02 §2 — 같은 부하 평균 1 이 CPU 수에 따라 다른 뜻이 된다.
# 원문("Monitoring"): uptime 출력 주석 — "then (in the load average section) three gauges: the 1-minute,
#       5-minute, and 15-minute average. These averages are the number of jobs in the run queue or waiting
#       for disk I/O; the numbers are normalized and indicate how busy the CPUs are."
# 1차 자료(procps-ng uptime(1)): "System load averages is the average number of processes that are either
#       in a runnable or uninterruptable state. ... Load averages are not normalized for the number of
#       CPUs in a system, so a load average of 1 means a single CPU system is loaded all the time while
#       on a 4 CPU system it means it was idle 75% of the time."
# 주의: 앞 두 막대는 man page 문장을 그대로 옮긴 값이고, 세 번째 막대(4 CPU · load 4)는 그 둘에서
#       유도한 값이다. 유도임을 legend 와 본문에 밝힌다.
# 타입 스펙: type-bar — 범주별 수치(CPU 사용률)를 막대 길이로 비교한다. 막대 길이가 비율에 정비례하고
#           수치를 막대 끝에 적는다. 축약: 1·5·15분 세 게이지의 시간 축은 본문 산문이 맡는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, WARN, RULE, KR, MONO

W, H = 880, 520
BAR_X, BAR_MAX, BAR_H, STRIDE, Y0 = 268, 420, 34, 62, 148
ROWS = [
    ("CPU 1개 · load 1", 100, "쉬는 틈 없이 걸려 있다", INFO, False),
    ("CPU 4개 · load 1", 25, "75% 는 유휴다", ACC, True),
    ("CPU 4개 · load 4", 100, "여기가 1개짜리의 load 1 과 같다", SOFT, False),
]

d = D(W, H, "LEARNING MODERN LINUX · 08-02 §2",
      "같은 숫자 1 이 시스템마다 다른 뜻이다",
      "부하 평균은 CPU 수로 나누어 정규화되지 않으므로, 값 하나만 보고 바쁨을 판정할 수 없다. "
      "막대는 그 값이 뜻하는 CPU 사용률이다.",
      "값을 읽기 전에 그 기계의 CPU 수를 먼저 알아야 합니다")

for i, (name, pct, note, col, focal) in enumerate(ROWS):
    y = Y0 + i * STRIDE
    w = BAR_MAX * pct / 100
    if focal:
        d.tone(BAR_X, y, w, BAR_H, ACC, 4, "2E", 1.3)
    else:
        d.o.append(f'<rect x="{BAR_X}" y="{y}" width="{w}" height="{BAR_H}" rx="4" fill="{col}3A"/>')
    d.t(24, y + 15, name, 13.5, ACC if focal else INK, MONO, "start", 600)
    d.t(24, y + 33, note, 11.5, MUTED, KR, "start")
    d.t(BAR_X + w + 14, y + 23, f"{pct}%", 13.5, col, MONO, "start", 600)

d.line(BAR_X, Y0 + 3 * STRIDE - 14, BAR_X + BAR_MAX + 40, Y0 + 3 * STRIDE - 14, RULE, 1)
d.t(BAR_X, Y0 + 3 * STRIDE + 6, "가로축은 CPU 사용률입니다", 11, SOFT, KR, "start")

NY = 356
d.t(24, NY, "uptime 이 내놓는 세 값은 1분 · 5분 · 15분 평균이고, 실행 큐에 있거나 디스크 I/O 를 "
            "기다리는 작업의 수입니다.", 12, MUTED, KR, "start")
d.t(24, NY + 24, "저자는 그 수가 정규화되어 있다고 적지만, procps-ng 의 uptime(1) 은 CPU 수로 정규화하지 "
                 "않는다고 못 박습니다.", 12, INK, KR, "start")
d.t(24, NY + 48, "그래서 0.2 라는 값 하나로는 아무것도 판정할 수 없고, 다른 값과 견주며 시간에 걸쳐 "
                 "추적하라고 저자도 덧붙입니다.", 12, MUTED, KR, "start")

d.legend(H - 56, [("man page 가 뜻을 못 박은 자리", ACC), ("man page 가 든 다른 예", INFO),
                  ("앞의 둘에서 유도한 값", SOFT)])
d.save("08-02.load-average.svg")
print("ok 08-02.load-average")
