# 02-01 §10 — 16MB/s 로 두 캐시를 채우는 데 걸리는 시간.
# 타입 스펙: type-line — 시간이라는 연속 축 위의 누적량 두 계열.
#           원서 p.19: 디스크 2,000 reads/s × 8KB = 16MB/s, DRAM 128GB 2시간 넘게, 플래시 600GB 10시간 넘게.
#           계산: 128,000MB / 16MB/s = 8,000s ≈ 2.2h, 600,000MB / 16 = 37,500s ≈ 10.4h (1GB = 1,000MB).
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, RULE, KR, MONO

W, H = 928, 480
X0, Y0, PW, PH = 112, 120, 712, 248
XMAX, YMAX = 12, 600
RATE = 16 * 3600 / 1000            # GB/h

def px(v): return X0 + PW * v / XMAX
def py(v): return Y0 + PH - PH * v / YMAX

d = DK(W, H, "SYSTEMS PERFORMANCE · 02-01 §10",
       "16MB/s 로는 캐시가 몇 시간에 걸쳐 데워진다",
       "회전 디스크가 랜덤 읽기로 초당 2,000번 × 8KB 만 공급할 때, DRAM 128GB 와 플래시 600GB 가 차오르는 시간을 계산해 그렸다.",
       "원서 p.19 의 스토리지 어플라이언스 · 1GB = 1,000MB 로 계산")

for v in (0, 128, 300, 600):
    d.line(X0, py(v), X0 + PW, py(v), RULE, 0.8)
    d.t(X0 - 12, py(v) + 4, f"{v}GB", 12, SOFT, MONO, "end")
for v in range(0, 13, 2):
    d.t(px(v), Y0 + PH + 22, f"{v}h", 12, SOFT, MONO, "middle")
d.t(X0 + PW, Y0 + PH + 44, "cold 시작부터 경과 시간 →", 12, SOFT, KR, "end")
d.line(X0, Y0, X0, Y0 + PH, MUTED, 1.0)

t_dram, t_flash = 128 / RATE, 600 / RATE
for cap, t, c, sw in ((600, t_flash, ACC, 2.0), (128, t_dram, INFO, 1.8)):   # 같은 기울기라 DRAM 을 위에 그린다
    pts = [(0, 0), (t, cap), (XMAX, cap)]
    s = " ".join(f"{px(a):.1f},{py(b):.1f}" for a, b in pts)
    d.o.append(f'<polyline points="{s}" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linejoin="round"/>')
    d.o.append(f'<circle cx="{px(t):.1f}" cy="{py(cap):.1f}" r="4" fill="{c}"/>')
    d.line(px(t), py(cap), px(t), Y0 + PH, c, 0.8, "3 4")
d.t(px(t_dram) + 12, py(128) + 24, f"DRAM 128GB · {t_dram:.1f}h", 13, INFO, KR, "start", 600)
d.t(px(XMAX), py(600) - 12, f"플래시 600GB · {t_flash:.1f}h", 13, ACC, KR, "end", 600)

d.legend(Y0 + PH + 60, [("DRAM 캐시", INFO), ("플래시 캐시", ACC)])
d.save("02-01.cache-warmup.svg")
