# 11-01 전체 지도 — 클라우드가 푸는 문제와 새로 만드는 문제.
# 타입 스펙: type-layers — 다섯 절이 유연함에서 공유의 대가로 옮겨 가는 관심의 층 지도다.
#           축약: OSI 층이 아니므로 인덱스 태그를 절 번호로 채운다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 928, 560
BX, BW, BH, Y0, STRIDE = 96, 736, 64, 108, 72

d = DK(W, H, "SYSTEMS PERFORMANCE · 11-01",
       "클라우드를 보는 다섯 갈래",
       "11-01 이 다루는 다섯 절. 앞 세 절이 클라우드가 주는 유연함을, 뒤 두 절이 그 대가인 공유의 문제를 다룬다.",
       "옛 문제를 풀면서 새 문제를 만듭니다 — 유연함의 대가가 공유입니다")

BANDS = [
    ("§1", "인스턴스 유형", "튜너블이 된 하드웨어", "골라 쓰고 바꾼다", None),
    ("§2", "수평 확장", "작은 인스턴스를 병렬로", "잘게 나눠 맞춘다", None),
    ("§3", "용량 계획", "자동 스케일링과 그 함정", "부하에 반응해 늘린다", None),
    ("§4", "스토리지", "휘발성 로컬 · 영속 네트워크", "네트워크를 건너 느려진다", None),
    ("§5", "멀티테넌시 · Kubernetes", "noisy neighbor · 오케스트레이션", "공유가 경합을 부른다", ACC),
]

for i, (tag, name, sub, role, c) in enumerate(BANDS):
    y = Y0 + i * STRIDE
    if c: d.tone(BX, y, BW, BH, c, 8)
    else: d.box(BX, y, BW, BH, PAPER2, RULE, 1.0, 8)
    d.t(BX - 24, y + 38, tag, 13, c if c else SOFT, MONO, "end", 600)
    d.t(BX + 20, y + 28, name, 14, c if c else INK, KR, "start", 600)
    d.t(BX + 20, y + 48, sub, 13, MUTED, KR, "start")
    d.t(BX + BW - 20, y + 38, role, 13, c if c else SOFT, KR, "end")

d.t(BX - 60, Y0 + 4, "유연함", 13, SOFT, KR, "middle")
d.arrow([(BX - 60, Y0 + 16), (BX - 60, Y0 + 4 * STRIDE + BH - 8)], SOFT, "soft", 1.2, "4 6")
d.t(BX - 60, Y0 + 4 * STRIDE + BH + 16, "대가", 13, SOFT, KR, "middle")

d.t(BX, Y0 + 5 * STRIDE + 18, "가상화 유형 자체(하드웨어·OS·경량)는 11-02~11-04 가 다룹니다", 13, MUTED, KR, "start")

d.legend(Y0 + 5 * STRIDE + 44, [("공유의 대가를 다루는 절", ACC), ("나머지 절", MUTED)])
d.save("11-01.chapter-overview.svg")
