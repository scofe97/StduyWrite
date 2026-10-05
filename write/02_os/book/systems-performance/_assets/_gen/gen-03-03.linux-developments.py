# 03-03 §3 — 원서 3.4.1 목록에서 영역마다 대표 항목만 골라 첫 도입 버전 위에 놓는다.
# 타입 스펙: type-timeline — 사건(기능 도입)을 축 위에 놓는다.
#           축약: 가로축은 시간이 아니라 버전 순서다. 시리즈(2.5 · 2.6 · 3.x · 4.x · 5.x)마다 폭이 다르고,
#           시리즈 안에서는 minor 번호에 비례한다(눈금 정직성 — 시리즈 경계에 점선과 라벨). 영역마다 한 줄, stride 72.
#           focal 은 BPF 줄(3.0 JIT → 5.3 bounded loops).
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 676
SEG = {"2.5": (184, 56, 80), "2.6": (248, 176, 40), "3": (432, 196, 20), "4": (636, 204, 21), "5": (848, 120, 9)}
def X(v):
    p = v.split(".")
    key = "2.5" if v.startswith("2.5") else "2.6" if v.startswith("2.6") else p[0]
    x0, w, n = SEG[key]
    minor = int(p[2]) if key in ("2.5", "2.6") else int(p[1])
    return x0 + w * minor / n
ROW0, ST = 168, 72

d = DK(W, H, "SYSTEMS PERFORMANCE · 03-03 §3",
       "Linux 성능 발전 — 영역별 첫 도입 버전",
       "원서 3.4.1 의 목록에서 영역마다 대표 항목만 골라 첫 도입 버전 위에 놓았다. 가로축은 시간이 아니라 버전 순서이고 시리즈마다 폭이 다르다. 맨 아래 BPF 줄은 3.0 의 JIT 부터 5.3 의 bounded loop 까지 이어진다.",
       "가로축은 버전 순서입니다 — 시리즈마다 간격이 다릅니다")

ROWS = [("스케줄링", [("CFS", "2.6.23"), ("CFS bandwidth", "3.2"), ("SCHED_DEADLINE", "3.14"), ("thermal pressure", "5.7")], None),
        ("메모리", [("huge pages", "2.5.36"), ("THP", "2.6.38"), ("NUMA balancing", "3.8"), ("PSI", "4.20")], None),
        ("I/O", [("CFQ", "2.6.6"), ("multiqueue", "3.13"), ("BFQ · Kyber", "4.12"), ("io_uring", "5.1")], None),
        ("네트워크", [("TFO", "3.6"), ("DCTCP", "3.18"), ("BBR", "4.9"), ("MPTCP", "5.6")], None),
        ("관측", [("tracepoints", "2.6.28", "u", "end"), ("perf", "2.6.31"), ("uprobes", "3.5", "u", "start"), ("flame graphs", "5.8")], None),
        ("BPF", [("JIT", "3.0"), ("eBPF", "3.18"), ("tracepoints", "4.7"), ("cgroups", "4.10"), ("bounded loops", "5.3")], ACC)]

AXY = ROW0 + len(ROWS) * ST - 24
# 시리즈 경계
for key, lab in (("2.5", "2.5"), ("2.6", "2.6"), ("3", "3.0"), ("4", "4.0"), ("5", "5.0")):
    x0 = SEG[key][0]
    d.line(x0, ROW0 - 40, x0, AXY, RULE, 0.8, "3 6")
    d.t(x0 + 4, AXY + 20, lab, 12, SOFT, MONO, "start")
d.t(SEG["5"][0] + SEG["5"][1], AXY + 20, "5.8", 12, SOFT, MONO, "end")
d.line(SEG["2.5"][0], AXY, SEG["5"][0] + SEG["5"][1], AXY, MUTED, 1.0)

for r, (area, evs, c) in enumerate(ROWS):
    y = ROW0 + r * ST
    col = c if c else INFO
    d.t(SEG["2.5"][0] - 20, y + 5, area, 14, c if c else INK, KR, "end", 600)
    d.line(SEG["2.5"][0], y, SEG["5"][0] + SEG["5"][1], y, RULE, 1.0)
    for k, ev in enumerate(evs):
        name, v = ev[0], ev[1]
        x = X(v)
        d.o.append(f'<circle cx="{x:.1f}" cy="{y}" r="{5 if c else 4}" fill="{col}"/>')
        up = (ev[2] == "u") if len(ev) > 2 else k % 2 == 0
        anchor = ev[3] if len(ev) > 3 else ("end" if x > 900 else ("start" if x < 260 else "middle"))
        if anchor == "start" and len(ev) <= 3: x = x - 6
        d.t(x, y - 12 if up else y + 22, f"{name} {v}", 12, col, MONO, anchor, 600 if c else 400)

d.legend(AXY + 40, [("BPF 의 확장", ACC), ("영역별 대표 발전", INFO)])
d.save("03-03.linux-developments.svg")
