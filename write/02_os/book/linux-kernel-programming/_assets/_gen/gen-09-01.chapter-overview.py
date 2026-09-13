# 09-01 전체 지도 — 전용 캐시를 직접 만드는 길과, slab 이 못 주는 큰 버퍼를 얻는 길.
# 타입 스펙: type-process — 일곱 절이 "전용 캐시를 만든다 → 실제 크기를 잰다 → 커널과 협조한다 → 더 큰 것을 얻는다" 로 이어진다.
#           축약: 주체(lane)가 없는 단계 지도라 lane 축을 빼고 단계 카드만 남겼다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER2, RULE, KR, MONO

W, H = 976, 472
X0, CW, STRIDE, CY, CH = 24, 176, 184, 116, 180

d = DK(W, H, "LINUX KERNEL PROGRAMMING · 09-01",
       "내 캐시를 만들고, 더 큰 것을 얻는 법",
       "09-01 이 다루는 일곱 절. 커널은 모듈 작성자에게도 slab 계층 API 를 열어 주어 전용 캐시를 만들 수 있게 한다. 그리고 slab 이 못 주는 4MB 초과 버퍼는 vmalloc 이 가상 연속으로 내준다.",
       "둘 다 slab 을 아는 사람만 쓸 수 있는 길입니다")

CARDS = [
    ("§1~3", "3단계 수명주기", "만들고 · 쓰고 ·", "부수는 순서입니다", "kmem_cache_*", INFO),
    ("§4", "실제 객체 크기", "328 을 요청해도", "448 을 받습니다", "slab_size", ACC),
    ("§5", "shrinker", "압박이 오면 커널이", "풀라고 부릅니다", "register_shrinker", INFO),
    ("§6", "vmalloc", "물리 연속을 포기하고", "훨씬 큰 것을 받습니다", "VMALLOC_START", INFO),
    ("§7", "kvmalloc", "먼저 kmalloc, 실패하면", "vmalloc 으로 넘깁니다", "kvfree()", INFO),
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

# 카드 사이 간격이 화살촉을 담기에 좁다 — 읽는 방향은 카드 아래 레일 하나로 보인다.
RAIL = CY + CH + 24
RIGHT = X0 + (len(CARDS) - 1) * STRIDE + CW
d.t(X0, RAIL + 5, "읽는 순서", 12, SOFT, KR, "start")
d.arrow([(X0 + 72, RAIL), (RIGHT, RAIL)], SOFT, "soft", 1.2, "4 6")

d.t(X0, 356, "§1~§5 는 전용 캐시 쪽이고 §6·§7 은 slab 자체를 벗어나는 쪽입니다. 가르는 기준은 물리 연속이 필요한가입니다.", 13, MUTED, KR, "start")
d.t(X0, 380, "전용 캐시를 만들어도 요청한 크기가 그대로 오지는 않습니다 — §4 가 그것을 재는 자리입니다.", 13, SOFT, KR, "start")

d.legend(H - 56, [("요청과 실제가 갈리는 자리", ACC), ("나머지 절", INFO)])
d.save("09-01.chapter-overview.svg")
print("ok 09-01.chapter-overview")
