# 07-03 전체 지도 — 물리 RAM 을 커널이 어떻게 조직하고, 그것을 어떻게 가상 주소로 덮는가.
# 타입 스펙: type-process — 다섯 절이 "계층을 세운다 → 뱅크를 나눈다 → 구획을 나눈다 → 덮는다 → 추적한다" 로 이어진다.
#           축약: 주체(lane)가 없는 단계 지도라 lane 축을 빼고 단계 카드만 남겼다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, OK, PAPER2, RULE, KR, MONO

W, H = 976, 472
X0, CW, STRIDE, CY, CH = 24, 176, 184, 116, 180

d = DK(W, H, "LINUX KERNEL PROGRAMMING · 07-03",
       "물리 RAM 을 커널이 나누는 법",
       "07-03 이 다루는 다섯 절. 커널은 부팅 시 물리 RAM 을 노드·존·페이지 프레임 3단계로 조직하고, 그 전부를 PAGE_OFFSET 부터 커널 VAS 에 1:1 로 덮은 뒤, 페이지마다 struct page 하나로 추적한다.",
       "가상 메모리 3부작의 마지막 — 여기까지가 할당 API 의 토대입니다")

CARDS = [
    ("§1", "3단계 계층", "노드 · 존 ·", "페이지 프레임", "pg_data_t", INFO),
    ("§2", "노드 · NUMA", "RAM 뱅크를 추상화하고", "가까운 것부터 씁니다", "numactl", INFO),
    ("§3", "존", "하드웨어 제약이", "구획을 가릅니다", "/proc/buddyinfo", INFO),
    ("§4", "direct-map", "모든 RAM 을 커널", "VAS 에 1:1 로 덮습니다", "PAGE_OFFSET", ACC),
    ("§5", "sparsemem", "페이지마다 구조체", "하나로 추적합니다", "PFN", INFO),
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

d.t(X0, 356, "§1~§3 은 물리 쪽에서 RAM 을 나누고, §4 가 그것을 가상 주소로 덮습니다 — 두 세계가 여기서 만납니다.", 13, MUTED, KR, "start")
d.t(X0, 380, "§5 는 그렇게 덮은 페이지를 커널이 무엇으로 세는지를 다룹니다.", 13, SOFT, KR, "start")

d.legend(H - 56, [("가상과 물리가 만나는 자리", ACC), ("나머지 절", INFO)])
d.save("07-03.chapter-overview.svg")
print("ok 07-03.chapter-overview")
