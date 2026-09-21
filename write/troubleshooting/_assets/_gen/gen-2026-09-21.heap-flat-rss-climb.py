# 2026-09-14 E(힙은 평평한데) 문항 · 원인 분석 — 사건.
# 논지는 "두 선이 갈린다"이다. 힙은 평평한데 커널이 세는 값만 올라 한도에 닿고, 재시작 뒤 같은 모양이 되풀이된다.
# 타입 스펙: type-line — 시간에 따른 연속 추세. 두 계열의 간격이 벌어지는 것이 곧 JVM 바깥의 몫이다.
#           type-bar 는 시점 하나의 구간 분해만 보이고 "되풀이"가 사라져 기각.
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dd import D, ACC, OK, BAD, INFO, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 508
d = D(W, H, "TROUBLESHOOTING DRILL · 2026-09-14 E",
      "한 선은 평평하고 다른 선만 한도로 올라갑니다",
      "힙 사용량은 며칠 내내 최대 힙의 40~50% 에 머물렀다. 커널이 세는 값만 조금씩 올라 컨테이너 한도에 닿고, "
      "그 순간 SIGKILL 이 떨어진다. 재시작하면 몇 시간을 버티고 같은 모양이 되풀이된다.",
      lead="두 선의 간격이 곧 JVM 이 세지 않는 몫입니다")

X0, X1, YB, TOP = 96, 904, 396, 128          # 그림판
GB = (YB - TOP) / 4.5                        # 0 ~ 4.5 GB


def Y(gb):
    return round(YB - gb * GB)


def X(h):                                     # 0 ~ 18 시간
    return round(X0 + (X1 - X0) * h / 18.0)


# 축과 눈금
d.line(X0, YB, X1, YB, RULE, 0.8)
for gb in (1, 2, 3, 4):
    d.line(X0, Y(gb), X1, Y(gb), RULE, 0.5, "3,4")
    d.t(X0 - 12, Y(gb) + 4, f"{gb} GB", 11, MUTED, MONO, "end")
for h in (0, 6, 12, 18):
    d.t(X(h), YB + 22, f"{h}h", 11, MUTED, MONO)

# 컨테이너 한도 4 GB
d.line(X0, Y(4.0), X1, Y(4.0), BAD, 1.2, "6,4")
d.chip(X1 - 92, Y(4.0) - 16, "컨테이너 한도", BAD, 11)

# 최대 힙 2.8 GB
d.line(X0, Y(2.8), X1, Y(2.8), MUTED, 1.0, "2,4")
d.chip(X0 + 96, Y(2.8) - 16, "최대 힙 2.8 GB", MUTED, 11)

# 힙 사용량 — 평평
HEAP = [(0, 1.2), (3, 1.3), (6, 1.2), (8, 1.35), (8.2, 1.2), (12, 1.3), (14, 1.2),
        (14.2, 1.3), (18, 1.25)]
for a, b in zip(HEAP, HEAP[1:]):
    d.line(X(a[0]), Y(a[1]), X(b[0]), Y(b[1]), OK, 1.8)

# 커널이 세는 값 — 톱니로 오르고 한도에서 끊긴다
RSS = [(0, 2.2), (4, 2.9), (8, 4.0), (8.01, 2.3), (12, 3.2), (14, 4.0), (14.01, 2.3),
        (18, 3.4)]
for a, b in zip(RSS, RSS[1:]):
    d.line(X(a[0]), Y(a[1]), X(b[0]), Y(b[1]), ACC, 1.8)

for h in (8, 14):
    d.box(X(h) - 10, Y(4.0) - 10, 20, 20, PAPER, BAD, 1.3, 10)
    d.t(X(h), Y(4.0) + 5, "×", 12, BAD, MONO)
d.t(X(8) + 16, Y(4.0) - 20, "SIGKILL · OOMKilled", 12, BAD, KR, "start", 600)

d.t(X(1), Y(1.2) - 16, "힙 사용량", 12, OK, KR, "start", 600)
d.t(X(1), Y(2.2) + 24, "커널이 세는 값 · working set", 12, ACC, KR, "start", 600)
d.t(X0, 440, "두 선의 간격이 벌어지는 구간 — NMT 합계도 이 간격을 다 설명하지 못했다", 12, MUTED, KR, "start")

d.legend(452, [("힙 사용량", OK), ("커널이 세는 값", ACC), ("한도와 그 결과", BAD), ("최대 힙 선", MUTED)])
d.save(os.path.join(os.path.dirname(__file__), "..", "2026-09-21.heap-flat-rss-climb.svg"))
print("ok")
