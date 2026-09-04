# 06-04 §2 — pods verified 가 나머지 두 모드보다 메모리를 얼마나 더 쓰는가.
# 원문 근거: "For a cluster with 25,000 pods and 1,000 services, CoreDNS will consume about 160 MiB in
#            pods verified mode, and 80 MiB with pods insecure or pods disabled. For a cluster with
#            50,000 pods and 2,000 services, those numbers are 264 MiB and 106 MiB, respectively.
#            Memory use is linear with the number of pods and services."
#            네 값 전부 원서 수치이고 이 도식이 지어낸 값은 없다.
# 타입 스펙: type-bar — 범주별 이산 수치의 비교가 논지이고, 두 계열을 묶어 세운다.
#           축약: 스펙의 plot 여백은 1000×500 기준인데 이 저장소의 D() 머리글이 위 90px 을 쓰므로
#                 plot 을 아래로 밀고 캔버스를 늘린다. y축은 스펙대로 0 에서 시작한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, RULE, INFO, KR, MONO

W, H = 1000, 600
d = D(W, H, "LEARNING COREDNS · 06-04 §2",
      "pods 모드에 따른 CoreDNS 메모리",
      "원서가 실측으로 든 네 값이다. 세로축은 인스턴스 하나가 쓰는 메모리이고, "
      "verified 는 파드를 전부 캐시해야 해서 나머지 두 모드의 두 배 안팎을 쓴다.",
      "막대 넷 모두 원서가 적은 수치입니다")

CATS = [("파드 25,000", "서비스 1,000", 160, 80), ("파드 50,000", "서비스 2,000", 264, 106)]
PX0, PY0, PY1 = 140, 130, 430
YMAX = 280
PITCH, BW, GAP = 330, 120, 24


def py(v):
    return PY1 - v * (PY1 - PY0) / YMAX


for g in (0, 70, 140, 210, 280):
    d.line(PX0, py(g), 940, py(g), RULE, 0.8)
    d.t(PX0 - 14, py(g) + 4, str(g), 12, SOFT, MONO, "end")
d.t(PX0 - 14, py(280) - 20, "MiB", 12, SOFT, MONO, "end")
d.line(PX0, PY0, PX0, PY1, RULE, 1.0)

for i, (c1, c2, verified, other) in enumerate(CATS):
    cx = PX0 + 120 + i * PITCH
    for j, (val, color, label) in enumerate(((verified, ACC, "verified"), (other, INFO, "insecure · disabled"))):
        x = cx - BW - GAP / 2 + j * (BW + GAP)
        y = py(val)
        if color is ACC:
            d.tone(x, y, BW, PY1 - y, ACC, 4, "16", 1.4)
        else:
            d.o.append(f'<rect x="{x}" y="{y}" width="{BW}" height="{PY1 - y}" rx="4" '
                       f'fill="{INFO}16" stroke="{INFO}" stroke-width="1.2"/>')
        d.t(x + BW / 2, y + 20, f"{val} MiB", 12, color, MONO)
    d.t(cx, PY1 + 26, c1, 13, INK, KR, "middle", 600)
    d.t(cx, PY1 + 46, c2, 12, MUTED, KR)

d.t(20, 500, "두 점을 이으면 verified 는 객체 1,000개당 약 4 MiB, 나머지는 1 MiB 다 — 한계 비용이 네 배다", 13, MUTED, KR, "start")
d.t(20, 524, "나머지 두 모드의 선은 앞 편의 추정식 (파드 + 서비스) / 1000 + 54 와 정확히 같다", 13, MUTED, KR, "start")

d.legend(548, [("pods verified", ACC), ("insecure · disabled", INFO)])
d.save("06-04.pods-memory.svg")
