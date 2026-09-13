# 07-01 §3 — 가상 주소가 물리 주소가 되기까지, 어디서 빠른 경로로 빠지고 어디서 fault 가 나는가.
# 본문이 요구한 형태: 다섯 단계 가운데 3번이 "하드웨어 최적화 — 빠른 경로로 건너뛸 수 있습니다" 라는 분기다.
# 타입 스펙: type-flowchart — 조건에 따라 갈라지는 판단 논리. 아래로 내려가는 것이 느린 경로다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, OK, WARN, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 928, 672
MX, MW = 232, 280
RX, RW = 576, 328
CX = MX + MW / 2

d = DK(W, H, "LINUX KERNEL PROGRAMMING · 07-01 §3",
       "빠른 경로로 빠지거나, 테이블을 걷거나",
       "MMU 의 주소 변환. CPU 캐시와 TLB 는 변환을 건너뛰는 빠른 경로이고, 둘 다 빗나가야 MMU 가 페이지 테이블을 PGD·PUD·PMD·PTE 순으로 걷는다. 걷다 실패하면 fault 가 나는데, 버그인 fault 와 정상인 fault 가 갈린다.",
       "아래로 내려갈수록 비쌉니다 — 페이지 테이블 walk 는 가장 마지막 수단입니다")

def node(y, h, title, sub, c, focal=False):
    if focal:
        d.tone(MX, y, MW, h, ACC, 8, "12", 1.4)
    else:
        d.box(MX, y, MW, h, PAPER2, RULE, 1.0, 8)
    d.t(CX, y + (26 if sub else h / 2 + 5), title, 13, ACC if focal else (c if c else INK), KR, "middle", 600)
    if sub:
        d.t(CX, y + 46, sub, 13, MUTED, KR)

def exit_box(y, h, title, sub, sub2, c):
    d.tone(RX, y, RW, h, c, 8, "12", 1.1)
    d.t(RX + 16, y + 26, title, 13, c, KR, "start", 600)
    if sub:
        d.t(RX + 16, y + 46, sub, 13, MUTED, KR, "start")
    if sub2:
        d.t(RX + 16, y + 66, sub2, 13, MUTED, KR, "start")

Y = [116, 204, 292, 380, 484]
node(Y[0], 56, "가상 주소에 접근한다", None, None)
node(Y[1], 56, "CPU 캐시에 있나?", None, WARN)
node(Y[2], 56, "TLB 에 변환이 있나?", None, WARN)
node(Y[3], 72, "MMU 가 페이지 테이블을 걷는다", "PGD → PUD → PMD → PTE", None, True)
node(Y[4], 56, "물리 주소가 주소 라인에 실린다", None, OK)

# 아래로 내려가는 느린 경로
for i, (y0, h0) in enumerate([(Y[0], 56), (Y[1], 56), (Y[2], 56), (Y[3], 72)]):
    top = y0 + h0
    c = ACC if i == 3 else MUTED
    d.arrow([(CX, top + 4), (CX, Y[i + 1] - 6)], c, "acc" if i == 3 else "ar", 1.4)
    if i in (1, 2):
        d.chip(CX - 64, top + 16, "아니오", SOFT, 13)

# 오른쪽으로 빠지는 빠른 경로
exit_box(Y[1], 56, "캐시 안에서 끝난다", "변환 자체가 필요 없습니다", None, OK)
exit_box(Y[2], 56, "캐시된 물리 주소를 쓴다", "테이블을 걷지 않고 건너뜁니다", None, OK)
exit_box(Y[3], 72, "변환에 실패한다", "unmapped — 버그입니다. SIGSEGV 로 죽습니다", "미할당 — demand paging 이 프레임을 답니다", BAD)

for i, y0 in enumerate([Y[1], Y[2], Y[3]]):
    h0 = 72 if i == 2 else 56
    mid = y0 + h0 / 2
    c = BAD if i == 2 else OK
    d.arrow([(MX + MW + 4, mid), (RX - 6, mid)], c, "bad" if i == 2 else "ok", 1.4)
    d.chip((MX + MW + RX) / 2, mid - 22, "예" if i < 2 else "실패", c, 13)

d.t(24, Y[1] + 34, "cache hit", 12, SOFT, MONO, "start")
d.t(24, Y[2] + 34, "TLB hit", 12, SOFT, MONO, "start")
d.t(24, Y[3] + 30, "page table", 12, SOFT, MONO, "start")
d.t(24, Y[3] + 48, "walk", 12, SOFT, MONO, "start")

d.t(24, 560, "베이스 테이블 주소는 가상이 아니라 물리 주소입니다(x86 은 CR3, ARM 은 TTBR0/TTBR1).", 13, MUTED, KR, "start")
d.t(24, 582, "가상이면 그것을 변환하려고 또 테이블을 걸어야 해 무한 재귀가 됩니다.", 13, SOFT, KR, "start")

d.legend(H - 56, [("빠른 경로", OK), ("분기", WARN), ("느린 경로 — 이 절의 논점", ACC), ("fault", BAD)])
d.save("07-01.mmu-translation.svg")
print("ok 07-01.mmu-translation")
