# 02-01 §4 — 가상 주소가 물리 주소가 되는 두 갈래.
# 원문("Memory Management"): "Every time the CPU accesses a process's virtual page, the CPU would in
#       principle have to translate the virtual address a process uses to the corresponding physical
#       address. To speed up this process—which can be multi-level and hence slow—modern CPU
#       architectures support a lookup on-chip called translation lookaside buffer (TLB). The TLB is
#       effectively a small cache that, in case of a miss, causes the CPU to go via the process page
#       table(s) to calculate the physical address of a page and update the TLB with it."
#       페이지 기본 크기는 전통적으로 4 KB 였고 커널 v2.6.3 부터 huge page 를 지원한다.
# 타입 스펙: type-flowchart — 조건에 따라 갈라지는 판단 논리. accent 는 느린 쪽 경로 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 640
d = D(W, H, "LEARNING MODERN LINUX · 02-01 §4",
      "가상 주소가 물리 주소가 되는 두 갈래",
      "CPU 가 프로세스의 가상 페이지에 닿을 때마다 밟는 경로. TLB 에 있으면 한 걸음이고, "
      "없으면 페이지 테이블을 여러 단계 타고 내려간 뒤 TLB 를 갱신한다.",
      "빠르게 만드는 장치가 아니라 느린 경로를 줄이는 장치입니다")


def oval(x, y, w, h, txt, c=MUTED):
    d.box(x, y, w, h, PAPER2, c, 1.1, r=20)
    d.t(x + w / 2, y + h / 2 + 5, txt, 13, INK)


def step(x, y, w, h, txt, sub=None, c=RULE):
    d.box(x, y, w, h, PAPER2, c, 1.0, r=6)
    d.t(x + w / 2, y + (24 if sub else h / 2 + 5), txt, 13, INK)
    if sub:
        d.t(x + w / 2, y + 44, sub, 12, MUTED, KR)


def dia(cx, cy, w, h, txt):
    d.o.append(f'<path d="M {cx} {cy - h / 2} L {cx + w / 2} {cy} '
               f'L {cx} {cy + h / 2} L {cx - w / 2} {cy} Z" '
               f'fill="{PAPER2}" stroke="{RULE}" stroke-width="1.0"/>')
    d.t(cx, cy + 5, txt, 13, INK)


CX, RX = 268, 640

oval(CX - 140, 108, 280, 44, "CPU 가 가상 페이지에 접근")
dia(CX, 216, 300, 68, "TLB 에 그 매핑이 있나")
d.arrow([(CX, 152), (CX, 182)], MUTED, "ar", 1.2)

step(CX - 140, 316, 280, 64, "물리 주소를 바로 얻는다", "온칩 조회 한 번", OK)
d.arrow([(CX, 250), (CX, 316)], OK, "ok", 1.2)
d.t(CX + 14, 288, "있다", 12, OK, KR, "start")

step(RX - 148, 188, 296, 64, "페이지 테이블을 따라 계산", "여러 단계라 그만큼 느리다", ACC)
d.arrow([(CX + 150, 216), (RX - 148, 216)], ACC, "acc", 1.4)
d.t((CX + 150 + RX - 148) / 2, 206, "없다", 12, ACC, KR)

step(RX - 148, 316, 296, 64, "TLB 를 그 값으로 갱신", "다음 접근은 위쪽 경로로", ACC)
d.arrow([(RX, 252), (RX, 316)], ACC, "acc", 1.2)
d.arrow([(RX - 148, 348), (CX + 140, 348)], ACC, "acc", 1.2)

d.box(60, 420, 760, 120, PAPER, RULE, 1.0, 6)
d.t(80, 448, "페이지는 물리 메모리와 가상 메모리를 같은 크기로 자른 조각입니다", 13, INK, KR, "start", 600)
for _k, _line in enumerate([
        "전통적으로 기본 크기는 4 KB 였고, 커널 v2.6.3 부터 huge page 를 지원합니다.",
        "여러 가상 페이지가 각자의 페이지 테이블을 거쳐 같은 물리 페이지를 가리킬 수 있습니다.",
        "64비트 리눅스는 프로세스당 128 TB 의 가상 주소 공간과 약 64 TB 의 물리 메모리를 허용합니다."]):
    d.t(80, 472 + _k * 22, _line, 12, MUTED if _k < 2 else SOFT, KR, "start")

d.legend(564, [("빠른 경로", OK), ("느린 경로와 그 뒤처리", ACC)])
d.save("02-01.tlb-lookup.svg")
print("ok 02-01.tlb-lookup")
