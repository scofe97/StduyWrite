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

W, H = 880, 464
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

oval(CX - 140, 108, 280, 44, "CPU 가상 주소 접근")
dia(CX, 216, 300, 68, "TLB 매핑 존재 여부")
d.arrow([(CX, 152), (CX, 182)], MUTED, "ar", 1.2)

step(CX - 140, 316, 280, 64, "물리 주소 직접 획득", "온칩 조회 한 번 (히트)", OK)
d.arrow([(CX, 250), (CX, 316)], OK, "ok", 1.2)
d.t(CX + 14, 288, "히트 (Hit)", 12, OK, KR, "start")

step(RX - 148, 188, 296, 64, "페이지 테이블 탐색", "다단계 주소 계산 (미스)", ACC)
d.arrow([(CX + 150, 216), (RX - 148, 216)], ACC, "acc", 1.4)
d.t((CX + 150 + RX - 148) / 2, 206, "미스 (Miss)", 12, ACC, KR)

step(RX - 148, 316, 296, 64, "TLB 매핑 갱신", "다음 접근은 빠른 경로로", ACC)
d.arrow([(RX, 252), (RX, 316)], ACC, "acc", 1.2)
d.arrow([(RX - 148, 348), (CX + 140, 348)], ACC, "acc", 1.2)

d.legend(412, [("빠른 경로 (히트)", OK), ("느린 경로와 캐시 갱신 (미스)", ACC)])
d.save("02-01.tlb-lookup.svg")
print("ok 02-01.tlb-lookup")
