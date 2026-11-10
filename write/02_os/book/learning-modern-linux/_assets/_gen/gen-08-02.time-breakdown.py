# 08-02 §3 — 네 명령의 CPU 시간(user+sys)과 real 을 같은 시간 축에 찍는다. 두 점 사이 거리가 기다린 시간이다.
# 실측: debian:12 컨테이너 bash `time` (2026-11-10).
#   ls -R /usr &> /dev/null       real 0.021 user 0.002 sys 0.019
#   sleep 1                       real 1.001 user 0.000 sys 0.001
#   bash 반복문 30만 회           real 0.511 user 0.508 sys 0.001
#   dd bs=1 count=400000          real 0.093 user 0.030 sys 0.063
# 1차 자료: GNU time(1) — U "CPU-seconds that the process used directly (in user mode)",
#           S "CPU-seconds used by the system on behalf of the process (in kernel mode)".
# 타입 스펙: type-bar — dumbbell. 가로 방향만 쓰고 행마다 두 점(CPU 시간·real)을 선으로 잇는다.
#           값 범위가 0.001~1초로 세 자릿수를 넘어 로그 축을 쓴다. 로그 축에는 0 이 없으므로 축 아래에 밝힌다.
import math
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, RULE, KR, MONO

W, H = 920, 452
X0, PW = 300, 560
LO, HI = 0.0005, 2.0
STRIDE, Y0 = 64, 128


def px(v):
    return X0 + PW * (math.log10(v) - math.log10(LO)) / (math.log10(HI) - math.log10(LO))


ROWS = [
    ("ls -R /usr", "user 0.002 · sys 0.019", 0.021, 0.021, False),
    ("sleep 1", "user 0.000 · sys 0.001", 0.001, 1.001, True),
    ("bash 반복문 30만 회", "user 0.508 · sys 0.001", 0.509, 0.511, False),
    ("dd bs=1 40만 회", "user 0.030 · sys 0.063", 0.093, 0.093, False),
]

d = D(W, H, "LEARNING MODERN LINUX · 08-02 §3",
      "CPU 시간과 real 사이의 거리",
      "네 명령의 user+sys 와 real 을 로그 시간 축에 찍었다. 두 점이 겹치면 CPU 위에서 시간을 썼고, "
      "멀면 그만큼 CPU 밖에서 기다렸다.",
      "단일 스레드라면 real − (user+sys) 가 기다린 시간입니다")

AXT, AXB = Y0 - 24, Y0 + 4 * STRIDE - 20
for v, lab in ((0.001, "0.001"), (0.01, "0.01"), (0.1, "0.1"), (1, "1")):
    x = px(v)
    d.line(x, AXT, x, AXB, "rgba(245,245,243,0.08)", 0.8)
    d.t(x, AXB + 18, lab, 11, SOFT, MONO)
d.line(X0, AXB, X0 + PW, AXB, "rgba(245,245,243,0.25)", 1)
d.t(X0 + PW + 4, AXB + 18, "초", 11, SOFT, KR, "start")

for i, (name, sub, cpu, real, focal) in enumerate(ROWS):
    y = Y0 + i * STRIDE
    c = ACC if focal else INFO
    d.t(24, y - 2, name, 13, ACC if focal else INK, MONO, "start", 600)
    d.t(24, y + 16, sub, 12, MUTED, MONO, "start")
    x1, x2 = px(cpu), px(real)
    if x2 - x1 > 2:
        d.line(x1, y + 4, x2, y + 4, c, 2.4)
    d.o.append(f'<circle cx="{x2}" cy="{y + 4}" r="7" fill="#0D1117" stroke="{c}" stroke-width="2"/>')
    d.o.append(f'<circle cx="{x1}" cy="{y + 4}" r="4" fill="{c}"/>')
    gap = real - cpu
    d.t(x2 + 14, y + 8, f"대기 {gap:.3f}s", 12, c, KR, "start", 600 if focal else 400)

d.t(24, AXB + 18, "로그 축 · 0 은 표시 불가", 11, SOFT, KR, "start")
d.legend(H - 48, [("CPU 시간 user+sys (채운 점)", INFO), ("real (빈 점)", INFO), ("대기가 큰 명령", ACC)])
d.save("08-02.time-breakdown.svg")
print("ok 08-02.time-breakdown")
