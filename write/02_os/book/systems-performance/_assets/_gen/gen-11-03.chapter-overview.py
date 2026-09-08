# 11-03 전체 지도 — 커널 하나를 나눠 쓸 때 생기는 일.
# 타입 스펙: type-layers — 다섯 절이 맞교환 → 구현 → 오버헤드 → 제어 → 관측으로 이어지는 지도다.
#           축약: OSI 층이 아니므로 인덱스 태그를 절 번호로 채운다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 928, 560
BX, BW, BH, Y0, STRIDE = 96, 736, 64, 108, 72

d = DK(W, H, "SYSTEMS PERFORMANCE · 11-03",
       "OS 가상화를 보는 다섯 갈래",
       "11-03 이 다루는 다섯 절. 커널이 하나뿐이라는 사실이 장점과 단점을 동시에 만들고, 그것이 나머지 절 전체를 규정한다.",
       "커널이 하나라는 사실 하나가 이 편의 모든 것을 정합니다")

BANDS = [
    ("§1", "장단점", "빠른 공유와 잃는 격리", "커널이 하나라서", ACC),
    ("§2", "구현", "namespace(격리) + cgroup(제한)", "커널엔 컨테이너가 없다", None),
    ("§3", "오버헤드", "가벼운 실행 · 멀티테넌트 경합", "경합이 진짜 문제", None),
    ("§4", "자원 제어", "shares · bandwidth · bursting", "우선순위와 한계", None),
    ("§5", "관측", "호스트는 다 보고 게스트는 헷갈린다", "호스트 통계가 새어 나온다", None),
]

for i, (tag, name, sub, role, c) in enumerate(BANDS):
    y = Y0 + i * STRIDE
    if c: d.tone(BX, y, BW, BH, c, 8)
    else: d.box(BX, y, BW, BH, PAPER2, RULE, 1.0, 8)
    d.t(BX - 24, y + 38, tag, 13, c if c else SOFT, MONO, "end", 600)
    d.t(BX + 20, y + 28, name, 14, c if c else INK, KR, "start", 600)
    d.t(BX + 20, y + 48, sub, 13, MUTED, KR, "start")
    d.t(BX + BW - 20, y + 38, role, 13, c if c else SOFT, KR, "end")

d.t(BX - 60, Y0 + 4, "전제", 13, SOFT, KR, "middle")
d.arrow([(BX - 60, Y0 + 16), (BX - 60, Y0 + 4 * STRIDE + BH - 8)], SOFT, "soft", 1.2, "4 6")
d.t(BX - 60, Y0 + 4 * STRIDE + BH + 16, "귀결", 13, SOFT, KR, "middle")

d.t(BX, Y0 + 5 * STRIDE + 18, "게스트는 커널 경합을 더 만나면서 동시에 그것을 분석할 능력을 잃습니다", 13, MUTED, KR, "start")

d.legend(Y0 + 5 * STRIDE + 44, [("나머지를 규정하는 절", ACC), ("나머지 절", MUTED)])
d.save("11-03.chapter-overview.svg")
