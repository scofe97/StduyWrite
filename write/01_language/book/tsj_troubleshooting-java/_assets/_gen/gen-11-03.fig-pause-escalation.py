# 11-03 §1 — 멈춤 에스컬레이션. 본문이 고친 자리는 System.gc() 다. 원서는 2.5초짜리
# full GC 를 압박의 적신호로 읽지만, 괄호 안이 GC 를 부른 *이유* 이고 System.gc() 는
# 코드가 명시적으로 부른 것이라 원인 범주가 다르다. 처방도 갈린다 — 힙 튜닝이 아니라
# 그 호출을 없애거나 -XX:+DisableExplicitGC 다. 그래서 막대를 한 줄로 늘어놓지 않고
# Allocation Failure 계열과 System.gc() 를 축에서 갈라, 압박의 근거로 읽을 흐름을
# 앞줄에만 둔다. focal 은 5.32초 — 압박 계열의 끝이자 본문이 심각으로 읽은 자리.
# 타입 스펙: type-bar — 범주별 수치 비교. 막대 길이가 멈춤 시간이고 줄이 원인 범주다.
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, INFO, PAPER2, RULE, KR, MONO

W, H = 800, 576

d = D(W, H, "TROUBLESHOOTING JAVA · 11-03 §1",
      "멈춤이 길어지는 흐름과, 거기 끼어든 다른 원인",
      "GC 멈춤 에스컬레이션 막대 그림. 괄호 안은 GC 를 부른 이유이고 이것이 원인 범주를 가른다. "
      "Allocation Failure 계열은 할당할 자리가 없어 JVM 이 트리거한 것이라 25ms 에서 110ms, 250ms, "
      "5.32초로 길어지는 흐름이 메모리 압박의 근거가 된다. 반면 System.gc() 는 코드가 명시적으로 "
      "부른 것이라 이 흐름에 속하지 않는다. 처방도 힙 튜닝이 아니라 그 호출을 없애거나 "
      "-XX:+DisableExplicitGC 로 막는 것이다.",
      lead="괄호 안이 원인 범주입니다 — System.gc() 는 압박의 증거가 아닙니다")

BX = 300
BW = 356
MAXV = 5.321
import math
Y0, ROW = 148, 46


def bar(y, gc, secs, cause, colour, focal=False):
    d.t(44, y + 20, gc, 12, INK, MONO, "start")
    d.t(150, y + 20, cause, 12, colour, MONO, "start")
    # 제곱근 축척 — 선형이면 25ms 가 2px 라 에스컬레이션이 안 보인다
    w = max(8, BW * math.sqrt(secs / MAXV))
    d.tone(BX, y + 4, w, 24, colour, 3, "2A" if focal else "1C", 1.4 if focal else 1.0)
    d.t(BX + w + 12, y + 21, f"{secs:.3f}s", 12, colour, MONO, "start", 600 if focal else 400)


# ── 압박 계열 — Allocation Failure
d.t(44, Y0 - 14, "메모리 압박의 근거 — JVM 이 트리거한 수집", 12, SOFT, KR, "start", 600)
ROWS = [
    ("GC(45)", 0.025, "Allocation Failure", OK),
    ("GC(46)", 0.027, "Allocation Failure", OK),
    ("GC(48)", 0.110, "Allocation Failure", WARN),
    ("GC(49)", 0.250, "Allocation Failure", WARN),
    ("GC(52)", 5.321, "Allocation Failure", ACC),
]
for i, (gc, v, cause, c) in enumerate(ROWS):
    bar(Y0 + i * ROW, gc, v, cause, c, focal=(c is ACC))

YEND = Y0 + len(ROWS) * ROW

# 흐름 표시 — 이 다섯이 한 추세다
d.arrow([(738, Y0 + 16), (738, YEND - 26)], ACC, "acc", 1.3)
d.t(748, (Y0 + YEND) / 2 - 8, "길어지는", 11, ACC, KR, "start")
d.t(748, (Y0 + YEND) / 2 + 8, "추세", 11, ACC, KR, "start")

# ── 가르는 선
d.line(44, YEND + 6, 756, YEND + 6, RULE, 1.0)
d.t(44, YEND + 30, "원인 범주가 다름 — 코드가 명시적으로 부른 수집", 12, SOFT, KR, "start", 600)

# ── System.gc() — 다른 범주
YS = YEND + 44
bar(YS, "GC(50)", 2.567, "System.gc()", INFO)
d.t(44, YS + 48, "처방이 갈립니다 — 힙 튜닝이 아니라 호출 제거 또는 -XX:+DisableExplicitGC",
    12, INFO, KR, "start")
d.t(44, YS + 70, "라이브러리가 이 호출을 숨기고 있을 수 있어 코드 검색만으로는 안 나옵니다",
    12, MUTED, KR, "start")

# ── 임계 한 줄
d.t(44, YS + 94, "막대 길이는 제곱근 축척 · 50ms 는 휴리스틱 · G1 기본 목표는 MaxGCPauseMillis=200", 12, SOFT, KR, "start")

d.legend(H - 40, [("압박 계열의 끝 — 심각", ACC), ("다른 원인 범주", INFO)])
d.save(os.path.join(os.path.dirname(__file__), "..", "11-03.fig-pause-escalation.svg"))
print("ok pause-escalation")
