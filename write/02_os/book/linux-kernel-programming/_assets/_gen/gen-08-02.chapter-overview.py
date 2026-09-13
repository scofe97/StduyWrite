# 08-02 전체 지도 — 페이지보다 작은 조각을 다루는 계층과, 그래도 남는 낭비.
# 타입 스펙: type-process — 여덟 절이 "왜 얹었나 → 어떻게 부르나 → 어디서 오나 → 얼마나 버리나 → 어떻게 잡나" 로 이어진다.
#           축약: 주체(lane)가 없는 단계 지도라 lane 축을 빼고 단계 카드만 남겼다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER2, RULE, KR, MONO

W, H = 976, 448
X0, CW, STRIDE, CY, CH = 24, 176, 184, 116, 180

d = DK(W, H, "LINUX KERNEL PROGRAMMING · 08-02",
       "페이지보다 작은 조각을 위한 계층",
       "08-02 가 다루는 여덟 절. 페이지 할당자에 12바이트를 요청하면 4KB 를 통째로 받는다. slab 할당자는 그 낭비를 줄이려고 페이지 할당자 위에 얹힌 계층이고, 동시에 자주 쓰는 커널 객체를 미리 캐시해 두는 자리이기도 하다.",
       "slab 을 써도 낭비는 남습니다 — 그것을 재는 법이 이 편의 절반입니다")

CARDS = [
    ("§1", "두 존재 이유", "객체를 미리 캐시하고", "작은 낭비를 줄입니다", "SLUB", INFO),
    ("§2", "kmalloc · kfree", "커널에서 가장 자주", "불리는 할당 API 입니다", "kzalloc", INFO),
    ("§3·4", "kmalloc-N", "8바이트부터 8KB 까지", "best-fit 으로 줍니다", "최대 4MB", INFO),
    ("§5·6", "낭비 측정", "임계값을 넘는 순간", "낭비가 치솟습니다", "ksize()", ACC),
    ("§7·8", "devm_ · 구현", "드라이버 detach 때", "자동으로 풀립니다", "devres", INFO),
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
            ACC if i == 2 else MUTED, "acc" if i == 2 else "ar", 1.4)

d.t(X0, 336, "§1~§4 가 계층의 동작이고 §5·§6 이 그 계층을 써도 남는 낭비를 재는 법입니다.", 13, MUTED, KR, "start")
d.t(X0, 360, "slab 을 쓴다고 안심하지 말고 ksize() 로 실제 할당된 양을 확인하라는 것이 이 편의 교훈입니다.", 13, SOFT, KR, "start")

d.legend(H - 56, [("이 편의 논점", ACC), ("나머지 절", INFO)])
d.save("08-02.chapter-overview.svg")
print("ok 08-02.chapter-overview")
