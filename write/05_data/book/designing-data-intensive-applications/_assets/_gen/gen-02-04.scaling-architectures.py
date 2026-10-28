# 02-04 §2 — 세 아키텍처의 구성요소와 연결. 본문 세 항목(shared-memory·shared-disk·shared-nothing)의 구조와 한계만 그린다.
# 옛 도식의 선형 확장성 정의 단, 확장성 원칙 목록, cloud native 줄은 뺐다. §1·§3 본문이 맡는다.
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
PY, PH = 140, 236
LEG = PY + PH + 44
H = LEG + 56

d = D(W, H, "02-04 · ARCHITECTURES", "세 가지 확장 아키텍처",
      "shared-memory는 한 머신을 키우고, shared-disk는 노드들이 디스크를 공유하며, shared-nothing은 노드마다 CPU·RAM·디스크를 가지고 네트워크로 조율한다.",
      "자원을 어떻게 나누고 이어 붙이는가")

COLS = [16, 304, 592]
HEAD = [("shared-memory", "수직 확장 · scale up"), ("shared-disk", "공유 디스크 배열"), ("shared-nothing", "수평 확장 · scale out")]
for x, (a, b) in zip(COLS, HEAD):
    d.t(x + 136, 108, a, 15, INK, MONO, "middle", 600)
    d.t(x + 136, 128, b, 12, MUTED, KR)
    d.box(x, PY, 272, PH, PAPER, ACC if x == 592 else RULE, 1.4 if x == 592 else 0.9)

# shared-memory — 한 머신 안에 CPU·RAM·디스크
d.box(32, 172, 240, 152, PAPER2, INFO, 1.2)
d.t(152, 192, "한 머신", 12, MUTED, KR)
d.box(44, 204, 104, 40, PAPER, RULE, 1.0); d.t(96, 229, "CPU 코어", 13, INK, KR)
d.box(156, 204, 104, 40, PAPER, RULE, 1.0); d.t(208, 229, "RAM 공유", 13, INK, KR)
d.box(44, 256, 216, 40, PAPER, RULE, 1.0); d.t(152, 281, "디스크", 13, INK, KR)

# shared-disk — 노드 셋이 공유 디스크 하나에 연결
for i, nx in enumerate([308, 396, 484]):
    d.box(nx, 172, 72, 88, PAPER2, INFO, 1.2)
    d.t(nx + 36, 194, f"노드 {i + 1}", 13, INK, KR, "middle", 600)
    d.t(nx + 36, 220, "CPU", 12, MUTED, MONO)
    d.t(nx + 36, 240, "RAM", 12, MUTED, MONO)
    d.arrow([(nx + 36, 264), (nx + 36, 292)], MUTED, "ar", 1.4)
d.box(308, 296, 248, 44, PAPER2, INFO, 1.2)
d.t(432, 323, "공유 디스크 (NAS·SAN)", 13, INK, KR)

# shared-nothing — 노드마다 CPU·RAM·디스크, 일반 네트워크로 조율
for i, nx in enumerate([604, 692, 780]):
    d.box(nx, 172, 72, 88, PAPER2, OK, 1.2)
    d.t(nx + 36, 194, f"노드 {i + 1}", 13, INK, KR, "middle", 600)
    d.t(nx + 36, 216, "CPU", 12, MUTED, MONO)
    d.t(nx + 36, 232, "RAM", 12, MUTED, MONO)
    d.t(nx + 36, 248, "디스크", 12, MUTED, KR)
    d.line(nx + 36, 260, nx + 36, 296, MUTED, 1.4)
d.line(640, 296, 816, 296, MUTED, 1.4)
d.chip(728, 324, "일반 네트워크", MUTED, 12)

d.t(152, 364, "비용이 선형보다 빠르게 증가", 12, WARN, KR)
d.t(432, 364, "경합·락 오버헤드로 한계", 12, WARN, KR)
d.t(728, 364, "선형 확장 잠재력", 12, OK, KR)

d.legend(LEG, [("핵심 — 수평 확장", ACC), ("한계가 있는 구조", WARN), ("확장 잠재력", OK), ("머신·노드·디스크", INFO)])
d.save("02-04.scaling-architectures.svg")
