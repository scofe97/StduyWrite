# 01-01 §6 — 지연시간으로 최대 speedup 을 계산한다(원서 그림 1.3), IOPS 로는 같은 계산이 안 된다.
# 타입 스펙: type-gantt — 막대 길이가 곧 시간(ms)이고, 한 쿼리의 구간이 on-CPU 와 디스크 대기로 나뉜다.
#           축약: 날짜 축 대신 0~100 ms 눈금을 쓰고, 마지막 행은 막대 없이 IOPS 판단 칩만 둔다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER2, RULE, KR, MONO

W, H = 920, 456
TX, SCALE = 216, 6.8                  # 시간축 시작 · 1 ms 당 px
Y0, ROW, BH = 144, 56, 32

def tx(ms): return TX + ms * SCALE

d = DK(W, H, "SYSTEMS PERFORMANCE · 01-01 §6 · FIG 1.3",
       "100 ms 쿼리에서 디스크 대기 80 ms 를 없애면",
       "원서 그림 1.3. DB 쿼리 지연 100 ms 가운데 80 ms 는 디스크 읽기를 기다리며 off-CPU 로 블록된 시간이다. 디스크 읽기를 없애면 20 ms 가 남아 최대 5배 빨라진다. IOPS 는 유형과 크기가 섞여 같은 계산을 못 한다.",
       "남는 on-CPU 20 ms 가 개선의 상한을 정합니다")

# 눈금
YA = Y0 - 20
for ms in range(0, 101, 20):
    d.line(tx(ms), YA + 6, tx(ms), Y0 - 4, RULE, 1.0)
    d.t(tx(ms), YA, f"{ms} ms", 12, SOFT, MONO, "end" if ms == 100 else "middle")

def label(i, txt, c=INK):
    d.t(TX - 16, Y0 + i * ROW + 21, txt, 13, c, KR, "end", 600)

# 1 — 쿼리 전체
y = Y0
label(0, "DB 쿼리 지연")
d.box(tx(0), y, tx(100) - tx(0), BH, PAPER2, MUTED, 1.0, 4)
d.t(tx(50), y + 21, "100 ms", 13, INK, MONO, "middle", 600)
# 2 — 스레드
y = Y0 + ROW
label(1, "스레드")
d.tone(tx(0), y, tx(20) - tx(0), BH, INFO, 4)
d.t(tx(10), y + 21, "on-CPU 20", 12, INFO, MONO, "middle")
d.tone(tx(20), y, tx(100) - tx(20), BH, ACC, 4)
d.t(tx(60), y + 21, "off-CPU · 디스크 읽기 대기 80 ms", 13, ACC, KR, "middle", 600)
# 3 — 디스크 읽기 제거 뒤
y = Y0 + 2 * ROW
label(2, "디스크 읽기 제거 뒤", OK)
d.tone(tx(0), y, tx(20) - tx(0), BH, OK, 4)
d.t(tx(10), y + 21, "20 ms", 12, OK, MONO, "middle")
d.t(tx(20) + 24, y + 21, "100 ÷ 20 = 최대 5배", 14, OK, KR, "start", 600)

# 4 — IOPS 로는
y = Y0 + 3 * ROW + 24
label(3.4, "IOPS 로 본다면", WARN)
cx = [tx(0) + 96, tx(0) + 316, tx(0) + 536]
for x, txt in zip(cx, ["IOPS 80% 감소", "I/O 하나 크기 10배", "성능 영향 판단 불가"]):
    d.box(x - 96, y, 192, BH, PAPER2, WARN, 1.0, 4)
    d.t(x, y + 21, txt, 13, WARN, KR, "middle")
d.arrow([(cx[0] + 98, y + 16), (cx[1] - 100, y + 16)], WARN, "warn", 1.4)
d.arrow([(cx[1] + 98, y + 16), (cx[2] - 100, y + 16)], WARN, "warn", 1.4)

d.legend(y + BH + 32, [("디스크 대기 — 없앨 수 있는 몫", ACC), ("남는 on-CPU", INFO), ("개선 뒤", OK), ("IOPS 의 한계", WARN)])
d.save("01-01.latency-speedup.svg")
