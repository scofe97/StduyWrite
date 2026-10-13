# 타입 스펙: type-gantt — page 네 개를 쓰는 데 걸리는 시간. 채널 한 개는 250 µs 막대 넷이 이어지고, 채널 네 개는 막대 넷이 같은 구간에 겹친다(막대 길이 = 구간).
# 사실 출처: Coding for SSDs 4부 6.2 "Multiple levels of parallelism"(https://codecapsule.com/2014/02/12/coding-for-ssds-part-4-advanced-functionalities-and-internal-parallelism/ — 채널은 독립적이고 동시에 접근, "Channel-level parallelism")
#   · 2부 Table 1(SLC 쓰기 250 µs, 2014 년 표). 채널 4개와 page 4개는 계산을 위한 가정이고 제품 사양이 아니다. 1000 = 4 × 250.
# Layout conventions: 라벨 열 x=24~200, 시간축 x=216~792(250 µs = 144 px), 행 stride 40(막대 높이 28), 그룹 사이 간격 20. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 920, 408
d = D(W, H, "BYTEBYTEGO · 04-01 §1",
      "page 네 개를 쓰는 시간",
      "채널 한 개는 하나씩 이어서 쓰고, 채널이 네 개면 네 page 를 같은 구간에 씁니다. 이상적인 병렬을 가정한 계산 예입니다",
      "page 쓰기 250 µs (SLC)")

AX0, UNIT = 216, 144          # 0 µs 의 x 와 250 µs 당 픽셀
BH = 28
# 시간축 눈금
for k, us in enumerate((0, 250, 500, 750, 1000)):
    x = AX0 + k * UNIT
    d.line(x, 104, x, 356, RULE, 0.6, "3 6")
    d.t(x, 100, f"{us}", 12, MUTED, MONO, "middle")
d.t(AX0 + 4 * UNIT + 24, 100, "µs", 12, MUTED, MONO, "start")

# 그룹 A: 채널 1개
YA = 124
d.t(24, YA + 16, "채널 1개", 13, INK, KR, "start", 600)
d.t(24, YA + 36, "4 × 250 µs", 12, MUTED, MONO, "start")
for k in range(4):
    x = AX0 + k * UNIT
    d.tone(x + 2, YA, UNIT - 4, BH, INFO, 4, "22", 1.1)
    d.t(x + UNIT / 2, YA + 19, f"page {k}", 12, INFO, MONO, "middle", 600)
d.t(AX0 + 4 * UNIT + 16, YA + 19, "= 1000 µs", 12, INFO, MONO, "start", 600)

# 그룹 B: 채널 4개
YB = 200
for k in range(4):
    y = YB + k * 40
    d.t(24, y + 20, f"채널 {k}", 13, INK, KR, "start", 600 if k == 0 else 400)
    d.tone(AX0 + 2, y, UNIT - 4, BH, ACC, 4, "14", 1.4)
    d.t(AX0 + UNIT / 2, y + 19, f"page {k}", 12, ACC, MONO, "middle", 600)
d.t(AX0 + UNIT + 16, YB + 19, "250 µs 에 끝남", 12, ACC, KR, "start", 600)

d.legend(H - 44, [("채널 한 개", INFO), ("채널 네 개", ACC)])
d.save("04-01.ssd-channel-parallel.svg")
