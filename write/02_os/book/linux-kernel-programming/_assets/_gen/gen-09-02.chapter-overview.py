# 09-02 전체 지도 — 무엇을 부를지 고르는 일과, 커널이 뒤에서 늘 하고 있는 일.
# 타입 스펙: type-process — 다섯 절이 "고른다 → 커널이 회수한다 → 언제 발동하나 → 무엇이 바뀌었나" 로 이어진다.
#           축약: 주체(lane)가 없는 단계 지도라 lane 축을 빼고 단계 카드만 남겼다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER2, RULE, KR, MONO

W, H = 976, 448
X0, CW, STRIDE, CY, CH = 24, 176, 184, 116, 180

d = DK(W, H, "LINUX KERNEL PROGRAMMING · 09-02",
       "무엇을 부를지, 커널은 무엇을 하는지",
       "09-02 가 다루는 다섯 절. 앞 세 노트가 늘어놓은 할당 계층 중 무엇을 언제 쓰는지를 먼저 정리하고, 그다음 커널이 자유 메모리를 유지하려고 늘 돌리고 있는 회수 기계를 본다.",
       "고르는 기준은 둘입니다 — 얼마나 필요한가와 어떤 타입인가")

CARDS = [
    ("§1", "API 선택", "양과 타입 두 축으로", "고릅니다", "kmalloc 우선", ACC),
    ("§2", "memory reclaim", "자유 페이지를 늘", "확보해 둡니다", "kswapd", INFO),
    ("§3", "zone watermark", "min · low · high 가", "발동 시점을 정합니다", "/proc/zoneinfo", INFO),
    ("§4", "MGLRU", "세대를 여럿 두어", "더 세밀하게 고릅니다", "CONFIG_LRU_GEN", INFO),
    ("§5", "DAMON", "접근 패턴을 sampling", "으로 지켜봅니다", "damo", INFO),
]

for i, (tag, name, l1, l2, out, c) in enumerate(CARDS):
    x = X0 + i * STRIDE
    if c is ACC:
        d.tone(x, CY, CW, CH, ACC, 8, "12", 1.4)
    else:
        d.box(x, CY, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 16, CY + 30, tag, 13, c, MONO, "start", 600)
    d.t(x + CW - 16, CY + 30, name, 14, INK if c is not ACC else ACC, KR, "end", 600)
    d.line(x + 16, CY + 46, x + CW - 16, CY + 46, RULE, 0.8)
    d.t(x + 16, CY + 76, l1, 13, MUTED, KR, "start")
    d.t(x + 16, CY + 98, l2, 13, MUTED, KR, "start")
    d.chip(x + CW / 2, CY + 144, out, c, 13)

for i in range(4):
    x = X0 + i * STRIDE + CW
    d.arrow([(x + 4, CY + CH / 2), (x + STRIDE - CW - 6, CY + CH / 2)],
            ACC if i == 0 else MUTED, "acc" if i == 0 else "ar", 1.4)

d.t(X0, 336, "§1 은 내가 고르는 쪽이고 §2~§5 는 커널이 알아서 하는 쪽입니다. 둘이 만나는 자리가 할당 실패입니다.", 13, MUTED, KR, "start")
d.t(X0, 360, "이 회수 기술들이 충분히 못 거두면 다음 노트(09-03)의 OOM killer 가 옵니다.", 13, SOFT, KR, "start")

d.legend(H - 56, [("내가 고르는 자리", ACC), ("커널이 알아서 하는 쪽", INFO)])
d.save("09-02.chapter-overview.svg")
print("ok 09-02.chapter-overview")
