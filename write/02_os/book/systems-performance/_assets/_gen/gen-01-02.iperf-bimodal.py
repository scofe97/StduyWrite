# 01-02 §5 — iperf(1) 초당 처리량 10개 구간이 두 모드로 갈리고, 10초 평균이 두 모드를 가린다(원서 1.8 출력).
# 타입 스펙: type-line — 연속된 초 구간 위의 추세가 논지다. 점 10개(4~12 범위), y 축은 0 에서 시작한다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, WARN, PAPER2, RULE, KR, MONO

W, H = 960, 540
X0, PX = 136, 88                 # 첫 점 x · 점 간격
YB, PY = 424, 40                 # 0 Gbits/s 의 y · 1 Gbit/s 당 px

VALS = [4.88, 4.77, 4.82, 4.79, 4.79, 3.63, 3.21, 3.26, 3.28, 3.22]
def px(k): return X0 + k * PX
def py(v): return YB - v * PY

d = DK(W, H, "SYSTEMS PERFORMANCE · 01-02 §5 · SEC 1.8",
       "iperf 초당 처리량의 두 모드",
       "원서 1.8 의 iperf -c ... -i 1 -t 10 출력. 처음 5초는 약 4.8 Gbits/s, 그 뒤는 약 3.2 Gbits/s 로 처리량에 모드가 둘이다. 10초 평균 4.06 Gbits/s 는 어느 모드에도 없는 값이다.",
       "평균 하나만 보면 두 모드가 사라집니다")

# 모드 띠
d.tone(px(0) - 20, py(4.95), px(4) - px(0) + 40, py(4.7) - py(4.95), INFO, 4, "14", 1.0)
d.t(px(2), py(4.95) - 10, "약 4.8 Gbits/s 모드", 13, INFO, KR, "middle", 600)
d.tone(px(6) - 20, py(3.35), px(9) - px(6) + 40, py(3.15) - py(3.35), INFO, 4, "14", 1.0)
d.t((px(6) + px(9)) / 2, py(3.15) + 24, "약 3.2 Gbits/s 모드", 13, INFO, KR, "middle", 600)

# 격자 · 축
for v in (0, 2, 4, 6):
    d.line(X0 - 24, py(v), px(9) + 24, py(v), RULE, 1.0 if v == 0 else 0.6)
    d.t(X0 - 32, py(v) + 4, f"{v}", 12, SOFT, MONO, "end")
d.t(X0 - 32, py(6) - 16, "Gbits/s", 12, SOFT, MONO, "end")
for k in range(10):
    d.t(px(k), YB + 22, f"{k}-{k + 1}", 12, SOFT, MONO, "middle")
d.t(px(9) + 24, YB + 44, "초 구간", 12, SOFT, KR, "end")

# 평균선
d.line(X0 - 24, py(4.06), px(9) + 24, py(4.06), WARN, 1.4, "6 5")
d.t(px(9) + 24, py(4.06) - 8, "10초 평균 4.06", 13, WARN, KR, "end", 600)

# 선
pts = " ".join(f"{px(k)},{py(v):.1f}" for k, v in enumerate(VALS))
d.o.append(f'<polyline points="{pts}" fill="none" stroke="{ACC}" stroke-width="1.8" stroke-linejoin="round"/>')
for k, v in enumerate(VALS):
    d.o.append(f'<circle cx="{px(k)}" cy="{py(v):.1f}" r="4" fill="{ACC}"/>')

d.legend(YB + 60, [("초당 평균 처리량", ACC), ("모드", INFO), ("10초 평균", WARN)])
d.save("01-02.iperf-bimodal.svg")
