# 08-01 전체 지도 — 물리 메모리를 실제로 떼어 주는 엔진 하나와 그 엔진의 약점.
# 타입 스펙: type-process — 일곱 절이 "엔진이 무엇인가 → 어떻게 조직하나 → 어떻게 떼나 → 무엇을 잃나 → 어떻게 부르나" 로 이어진다.
#           축약: 주체(lane)가 없는 단계 지도라 lane 축을 빼고 단계 카드만 남겼다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, OK, BAD, PAPER2, RULE, KR, MONO

W, H = 976, 472
X0, CW, STRIDE, CY, CH = 24, 176, 184, 116, 180

d = DK(W, H, "LINUX KERNEL PROGRAMMING · 08-01",
       "물리 메모리를 떼어 주는 엔진 하나",
       "08-01 이 다루는 일곱 절. 리눅스에서 물리 메모리를 실제로 (de)할당하는 길은 페이지 할당자 하나뿐이다. buddy system 으로 자유 청크를 order 별 freelist 에 조직하고, 모자라면 상위 청크를 쪼개 준다. 그 대가가 내부 단편화다.",
       "slab 도 결국 여기서 메모리를 받습니다 — 우회로가 없습니다")

CARDS = [
    ("§1", "1차 엔진", "물리 메모리를 떼는", "유일한 길입니다", "BSA", INFO),
    ("§2", "freelist", "order 별 이중 연결", "리스트 배열입니다", "MAX_ORDER", INFO),
    ("§3", "분할 · 병합", "모자라면 상위 청크를", "둘로 쪼갭니다", "buddy block", INFO),
    ("§4·7", "내부 단편화", "2의 거듭제곱이 아니면", "절반까지 버립니다", "alloc_pages_exact", BAD),
    ("§5·6", "API · GFP", "첫 인자가 sleep 해도", "되는지를 정합니다", "GFP_KERNEL", ACC),
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

d.t(X0, 356, "§1~§3 이 엔진의 동작이고 §4 가 그 대가입니다. §5·§6 은 그 엔진을 실제로 부르는 법입니다.", 13, MUTED, KR, "start")
d.t(X0, 380, "GFP 플래그를 잘못 고르면 머신이 멈추거나 커널이 죽습니다 — 그래서 마지막 카드가 논점입니다.", 13, SOFT, KR, "start")

d.legend(H - 56, [("잘못 고르면 죽는 자리", ACC), ("이 엔진의 대가", BAD), ("나머지 절", INFO)])
d.save("08-01.chapter-overview.svg")
print("ok 08-01.chapter-overview")
