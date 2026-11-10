# 00-01 §3 — -mtime 의 숫자가 "나이를 24시간으로 나눈 몫"에 걸린다는 것.
# 근거(find(1), GNU findutils 4.9.0): 숫자 인자는 "+n for greater than n, -n for less than n, n for
#       exactly n". -atime n: "any fractional part is ignored, so to match -atime +1, a file has to
#       have been accessed at least two days ago." -mtime 은 이 규칙을 그대로 따른다.
# 실행(debian:12, touch -d 로 1h · 23h · 25h · 47h · 49h · 73h 전 파일 생성):
#       -mtime -1 → 1h 23h / -mtime 1 → 25h 47h / -mtime +1 → 49h 73h / -mtime +0 → 25h 47h 49h 73h
# 타입 스펙: type-gantt — 가로축이 파일 나이(시간)이고 행마다 조건 하나가 잡는 구간을 막대로 둔다.
#           accent 는 48시간에서 시작하는 -mtime +1 막대 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 468
d = D(W, H, "LEARNING MODERN LINUX · 00-01 §3",
      "-mtime 은 나이를 24시간으로 나눈 몫과 비교한다",
      "가로축은 파일이 마지막으로 바뀐 뒤 지난 시간이다. 나이를 24시간으로 나눈 몫이 0, 1, 2, 3 구간을 "
      "만들고, -mtime -1 은 몫 0, -mtime 1 은 몫 1, -mtime +1 은 몫 2 이상을 잡는다. 25시간 · 47시간 된 "
      "파일은 하루를 넘겼지만 몫이 1 이라 -mtime +1 에 걸리지 않는다.",
      "touch -d 로 만든 파일 여섯: 1h · 23h · 25h · 47h · 49h · 73h 전")

X0, PX = 192, 6          # 1시간 = 6px, 24시간 = 144px
XE = X0 + 96 * PX        # 768
def hx(h): return X0 + h * PX

# 축 눈금
for h, lab in ((0, "지금"), (24, "24h 전"), (48, "48h 전"), (72, "72h 전"), (96, "96h 전")):
    d.t(hx(h), 108, lab, 12, MUTED, KR, "middle")
    d.line(hx(h), 116, hx(h), 376, RULE, 0.8, "3 5")

# 파일 점
d.t(24, 144, "파일 나이", 12, MUTED, KR, "start")
for h, anchor in ((1, "start"), (23, "end"), (25, "start"), (47, "end"), (49, "start"), (73, "start")):
    x = hx(h)
    d.o.append(f'<circle cx="{x}" cy="140" r="4" fill="{INFO}"/>')
    d.t(x + (8 if anchor == "start" else -8), 144, f"{h}h", 12, INK, MONO, anchor)

# 몫 구간
d.t(24, 182, "24시간으로 나눈 몫", 12, MUTED, KR, "start")
for q in range(4):
    d.box(hx(q * 24) + 2, 164, 140, 28, PAPER2, RULE, 0.9, 4)
    d.t(hx(q * 24) + 72, 183, f"몫 {q}", 12, INK, KR)

# 조건 막대
rows = [("-mtime -1", 0, 24, False, "1h · 23h", "몫 < 1", MUTED),
        ("-mtime 1", 24, 48, False, "25h · 47h", "몫 = 1", MUTED),
        ("-mtime +1", 48, 96, True, "49h · 73h", "몫 > 1", ACC),
        ("-mtime +0", 24, 96, True, "25h · 47h · 49h · 73h", "몫 > 0", MUTED)]
for i, (lab, a, b, open_, hit, cond, c) in enumerate(rows):
    y = 216 + i * 40
    d.t(24, y + 25, lab, 13, INK if c is not ACC else ACC, MONO, "start", 600)
    x1, x2 = hx(a) + 2, hx(b) - 2
    d.box(x1, y + 8, x2 - x1, 24, PAPER, PAPER, 0, 4)   # 눈금선이 막대 글자를 가로지르지 않게 덮는다
    if c is ACC:
        d.tone(x1, y + 8, x2 - x1, 24, ACC, 4, "2E", 1.4)
    else:
        d.tone(x1, y + 8, x2 - x1, 24, MUTED, 4, "1F", 1.0)
    d.t((x1 + x2) / 2, y + 25, hit, 12, INK, MONO)
    if open_:
        d.arrow([(x2 + 2, y + 20), (x2 + 28, y + 20)], c, "acc" if c is ACC else "ar", 1.4)
        d.t(x2 + 36, y + 25, cond, 12, c, KR, "start")
    else:
        d.t(x2 + 12, y + 25, cond, 12, c, KR, "start")

d.t(24, 404, "하루를 넘긴 25h · 47h 는 몫이 1 이라 -mtime +1 밖", 12, MUTED, KR, "start")
d.legend(424, [("조건이 잡는 구간", MUTED), ("48시간부터 잡는 +1", ACC), ("파일", INFO)])
d.save("00-01.mtime-sign.svg")
print("ok 00-01.mtime-sign.svg")
