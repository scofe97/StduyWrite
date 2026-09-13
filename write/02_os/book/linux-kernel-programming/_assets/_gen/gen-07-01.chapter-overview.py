# 07-01 전체 지도 — 주소는 어디에 놓이고, 어떻게 생겼고, 어떻게 물리로 바뀌는가.
# 타입 스펙: type-process — 네 절이 "공간을 나눈다 → 주소를 해석한다 → 물리로 바꾼다" 로 이어진다.
#           축약: 주체(lane)가 없는 단계 지도라 lane 축을 빼고 단계 카드만 남겼다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, OK, PAPER2, RULE, KR, MONO

W, H = 928, 472
X0, CW, STRIDE, CY, CH = 24, 192, 228, 116, 180

d = DK(W, H, "LINUX KERNEL PROGRAMMING · 07-01",
       "주소가 물리 메모리에 닿기까지",
       "07-01 이 다루는 네 절. 유저와 커널이 한 주소 공간을 나눠 쓰는 VM split 에서 시작해, 64비트 주소가 비트맵이라는 사실을 거쳐, MMU 가 페이지 테이블을 걸어 물리 주소를 얻는 데까지 간다.",
       "주소는 절대값이 아니라 MMU 가 읽는 비트맵이라는 것이 이 편의 한 문장입니다")

CARDS = [
    ("§1", "VM split", "유저와 커널이 한 공간을", "User:Kernel 로 나눈다", "PAGE_OFFSET", INFO),
    ("§2", "가상 주소", "절대값이 아니라", "MMU 가 읽는 비트맵이다", "UVA · KVA", INFO),
    ("§3", "MMU 변환", "페이지 테이블을 걸어", "물리 프레임을 찾는다", "PGD→PUD→PMD→PTE", ACC),
    ("§4", "64비트 split", "48비트로 128TB : 128TB", "가운데는 거대한 hole 이다", "non-canonical", INFO),
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

d.t(X0, 356, "§1 이 공간을 가르고 §2 가 주소의 생김새를 밝히면, §3 의 변환이 그 둘 위에서 성립합니다.", 13, MUTED, KR, "start")
d.t(X0, 380, "§4 는 §1 의 32비트 예시를 64비트 실물 수치로 다시 세우는 자리입니다.", 13, SOFT, KR, "start")

d.legend(H - 56, [("이 편의 논점", ACC), ("나머지 절", INFO)])
d.save("07-01.chapter-overview.svg")
print("ok 07-01.chapter-overview")
