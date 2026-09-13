# 08-02 §3·§4 — kmalloc 이 요청 크기를 보고 어디서 메모리를 떼어 오는가.
# 본문이 요구한 형태: "12바이트 요청은 kmalloc-16 에서 16바이트" + "8192바이트 초과는 그대로 페이지 할당자로 위임".
# 타입 스펙: type-flowchart — 조건에 따라 갈라지는 판단 논리. 갈림길은 8KB 하나뿐이다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, OK, WARN, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 976, 648
MX, MW = 336, 304
CX = MX + MW / 2

d = DK(W, H, "LINUX KERNEL PROGRAMMING · 08-02 §3·§4",
       "8KB 하나로 길이 갈립니다",
       "kmalloc 은 8바이트부터 8192바이트까지의 kmalloc-N 캐시에서 best-fit 으로 준다. 요청이 8KB 를 넘으면 slab 이 처리하지 않고 그대로 페이지 할당자로 넘기므로, 그 순간부터는 페이지 할당자의 내부 단편화와 4MB 상한을 그대로 물려받는다.",
       "8KB 를 넘는 순간 slab 의 이점이 사라집니다")

d.box(MX, 120, MW, 56, PAPER2, RULE, 1.0, 8)
d.t(CX, 154, "kmalloc(size, gfp)", 13, INFO, MONO, "middle", 600)

d.box(MX, 208, MW, 56, PAPER2, RULE, 1.0, 8)
d.t(CX, 242, "size 가 8192바이트 이하인가?", 13, WARN, KR, "middle", 600)
d.arrow([(CX, 176), (CX, 202)], MUTED, "ar", 1.4)

# 왼쪽 — slab 이 처리한다
LX, LW = 24, 280
d.tone(LX, 320, LW, 176, OK, 8, "12", 1.1)
d.t(LX + 16, 350, "kmalloc-N 캐시에서 best-fit", 13, OK, KR, "start", 600)
d.t(LX + 16, 378, "8 · 16 · 32 · … · 4k · 8k", 12, MUTED, MONO, "start")
d.t(LX + 16, 406, "12바이트 요청 → kmalloc-16", 13, MUTED, KR, "start")
d.t(LX + 16, 430, "16바이트를 받고 4바이트를 버립니다", 13, MUTED, KR, "start")
d.t(LX + 16, 462, "물리 연속 · cacheline 정렬 보장", 13, OK, KR, "start")
d.path(f"M {MX} 236 L {LX + LW / 2} 236 L {LX + LW / 2} 314", OK, 1.5, m="ok")
d.chip((MX + LX + LW) / 2, 236, "예", OK, 13)

# 오른쪽 — 페이지 할당자로 넘어간다
RX, RW = 672, 280
d.tone(RX, 320, RW, 176, ACC, 8, "12", 1.4)
d.t(RX + 16, 350, "페이지 할당자로 그대로 위임", 13, ACC, KR, "start", 600)
d.t(RX + 16, 378, "__alloc_pages()", 12, MUTED, MONO, "start")
d.t(RX + 16, 406, "order 로 올려 2의 거듭제곱을 줍니다", 13, MUTED, KR, "start")
d.t(RX + 16, 430, "내부 단편화를 그대로 물려받습니다", 13, MUTED, KR, "start")
d.t(RX + 16, 462, "한 번에 최대 4MB — 2^(MAX_ORDER-1)", 13, ACC, KR, "start")
d.path(f"M {MX + MW} 236 L {RX + RW / 2} 236 L {RX + RW / 2} 314", ACC, 1.5, m="acc")
d.chip((MX + MW + RX) / 2, 236, "아니오", ACC, 13)

d.t(24, 536, "Raspberry Pi 같은 ARM 에서는 kmalloc-N 이 64바이트부터 시작합니다. 12바이트를 요청해도 64바이트를 받습니다.", 13, MUTED, KR, "start")
d.t(24, 560, "4MB 가 상한이라고 해서 요청하면 늘 받는 것은 아닙니다. 그 시점 freelist 에 물리 연속 4MB 청크가 남아 있어야 합니다.", 13, SOFT, KR, "start")

d.legend(H - 56, [("호출 지점", INFO), ("slab 이 처리하는 길", OK), ("갈림길", WARN), ("페이지 할당자로 넘어가는 길", ACC)])
d.save("08-02.kmalloc-cache-pick.svg")
print("ok 08-02.kmalloc-cache-pick")
