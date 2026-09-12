# 2026-09-10 E 문항 · 문제 소개 — 어떤 구조에서 일어난 일인가.
# 논지는 "요청 하나가 어느 스레드 위에서 도나"이지 교착이 아니다.
# 서로를 기다리는 인과는 원인 분석 절의 pinning-deadlock 이 맡는다.
# 타입 스펙: type-architecture — 구성요소와 연결. 두 층으로 가상/캐리어 관계를 보인다.
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 800, 412
d = D(W, H, "TROUBLESHOOTING DRILL · 2026-09-10 E",
      "요청 하나가 도는 자리",
      "JDK 21 로 올리며 요청 처리를 가상 스레드로 바꿨다. 요청마다 가상 스레드가 하나 생기고, "
      "그것이 실제로 돌려면 아래층의 캐리어 스레드에 올라타야 한다.",
      lead="위층은 수만 개까지 늘지만 아래층은 코어 수만큼입니다")

d.box(48, 118, 704, 92, PAPER2, RULE, 1.0, 8)
d.t(62, 140, "가상 스레드 — 요청 하나에 하나", 12, SOFT, KR, "start", 600)
for i in range(7):
    x = 70 + i * 96
    d.box(x, 154, 78, 40, PAPER2, RULE, 0.9, 5)
    d.t(x + 39, 179, f"요청 {i+1}", 12, INK, KR, "middle")
d.t(730, 179, "…", 13, SOFT, MONO, "middle")

for i in range(4):
    d.arrow([(109 + i * 192, 210), (109 + i * 192, 246)], MUTED, "ar", 1.2)
d.t(W // 2, 232, "올라타야 실제로 돕니다", 12, MUTED, KR, "middle")

d.box(48, 250, 704, 92, PAPER2, RULE, 1.0, 8)
d.t(62, 272, "캐리어 스레드 — 코어 수만큼 · ForkJoinPool", 12, SOFT, KR, "start", 600)
for i in range(4):
    x = 88 + i * 168
    d.tone(x, 286, 140, 40, ACC, 5)
    d.t(x + 70, 311, f"worker {i+1}", 12, ACC, MONO, "middle")

d.t(W // 2, 374, "블로킹할 때마다 내려와 자리를 내주는 것이 이 구조의 존재 이유입니다",
    13, MUTED, KR, "middle")

d.save(os.path.join(os.path.dirname(__file__), "..", "2026-09-10.carrier-topology.svg"))
print("ok")
