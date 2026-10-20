# 타입 스펙: type-bar
# 사실 출처: NPG Ch.13 Histograms and Summaries (Listing 13-22), 실제 50,000회 실행 측정 결과
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, INFO, KR, MONO

W, H = 960, 580
d = D(W, H, "BAR · HISTOGRAM BUCKETS",
      "RequestDuration 히스토그램의 버킷별 누적 관측수 분포",
      "프로메테우스 히스토그램은 이하(le) 조건을 만족하는 누적 개수를 기록합니다",
      "실제 실행 측정값: 전체 50,000건 중 99% 이상이 0.3µs 이하 구간에 집중")

# Plot area
bx0, bw_max = 240, 560
by0, bh, bgap = 105, 24, 6

buckets = [
    ('le="0.1µs" (1e-7)', 36515, OK),
    ('le="0.2µs" (2e-7)', 47010, OK),
    ('le="0.3µs" (3e-7)', 49542, OK),
    ('le="0.4µs" (4e-7)', 49685, INFO),
    ('le="0.5µs" (5e-7)', 49779, INFO),
    ('le="1µs" (1e-6)',   49877, INFO),
    ('le="2.5µs"',        49918, INFO),
    ('le="5µs"',          49938, INFO),
    ('le="7.5µs"',        49952, INFO),
    ('le="10µs"',         49958, INFO),
    ('le="100µs"',        49991, ACC),
    ('le="1ms"',          49998, ACC),
    ('le="10ms"',         50000, ACC),
    ('le="+Inf"',         50000, ACC),
]

# Gridlines at 0, 10k, 20k, 30k, 40k, 50k
for v in [0, 10000, 20000, 30000, 40000, 50000]:
    gx = bx0 + int((v / 50000.0) * bw_max)
    d.line(gx, by0 - 8, gx, by0 + len(buckets) * (bh + bgap) - bgap + 6, RULE, 0.7)
    d.t(gx, by0 - 12, f"{v:,}", 11, SOFT, MONO, "middle")

for idx, (label, count, col) in enumerate(buckets):
    cy = by0 + idx * (bh + bgap)
    bar_w = int((count / 50000.0) * bw_max)
    
    # Bucket label
    d.t(bx0 - 14, cy + 16, label, 11, INK, MONO, "end")
    
    # Bar background
    d.box(bx0, cy, bw_max, bh, fill="#161B22", stroke=RULE, sw=0.5, r=3)
    
    # Bar fill
    d.tone(bx0, cy, bar_w, bh, col, r=3, op="30", sw=1.0)
    
    # Count text
    pct = (count / 50000.0) * 100.0
    txt = f"{count:,} ({pct:.1f}%)"
    tx_pos = bx0 + bar_w - 8 if bar_w > 90 else bx0 + bar_w + 8
    anchor = "end" if bar_w > 90 else "start"
    tcol = INK if bar_w > 90 else col
    d.t(tx_pos, cy + 16, txt, 11, tcol, MONO, anchor, 600)

d.legend(525, [
    ("지연 집중 구간 (0.1~0.3µs)", OK),
    ("꼬리 지연 구간 (0.4~10µs)", INFO),
    ("최대 및 +Inf 기본 버킷", ACC),
])

out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "13-03.histogram-bucket-distribution.svg"))
d.save(out_path)
print("saved:", out_path)
