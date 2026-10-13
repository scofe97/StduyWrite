# 타입 스펙: type-state — NAND 플래시 page 한 개의 상태 전이(free → valid → stale → free). stale 에서 free 로 가는 길은 block 단위 지우기 하나뿐이다.
# 사실 출처: Coding for SSDs 3부 3.1(https://codecapsule.com/2014/02/12/coding-for-ssds-part-3-pages-blocks-and-the-flash-translation-layer/ — "Pages cannot be overwritten", "it is only possible to erase whole blocks at once", FTL 의 논리 블록 매핑)
#   · 2부 1.1 과 Table 1(https://codecapsule.com/2014/02/12/coding-for-ssds-part-2-architecture-of-an-ssd-and-benchmarking/ — page 2~16 KB · block 128·256 page 는 일반값, SLC 쓰기 250 µs · 지우기 1500 µs 는 Table 1 의 SLC 열, 2014 년 표).
#   추출본 v1.txt 1241~1244행(쓸 때마다 물리 page 를 찾아 매핑을 기록).
# Layout conventions: 상태 상자 폭 200·높이 72, x=40·360·680(stride 320), y=132. 전이 화살표는 상자 사이 수평, 지우기는 아래로 ㄷ자. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 920, 348
d = D(W, H, "BYTEBYTEGO · 04-01 §1",
      "플래시 page 한 개의 일생",
      "page 는 덮어쓸 수 없어서 갱신은 새 free page 에 쓰고, 옛 page 는 block 째 지울 때까지 stale 로 남습니다",
      "SLC 기준 쓰기 250 µs · 지우기 1500 µs")

BW, BH, Y = 200, 72, 132
XS = (40, 360, 680)
states = [
    ("free", "비어 있음", OK),
    ("valid", "최신 데이터", INFO),
    ("stale", "옛 데이터", WARN),
]
for x, (name, sub, c) in zip(XS, states):
    d.tone(x, Y, BW, BH, c, 8, "12", 1.2)
    d.t(x + BW / 2, Y + 32, name, 16, c, MONO, "middle", 600)
    d.t(x + BW / 2, Y + 54, sub, 13, MUTED, KR)

YC = Y + BH // 2
# free → valid : program
d.arrow([(XS[0] + BW + 4, YC), (XS[1] - 6, YC)], INFO, "info", 1.6)
d.t((XS[0] + BW + XS[1]) / 2, YC - 28, "program", 13, INFO, MONO, "middle", 600)
d.t((XS[0] + BW + XS[1]) / 2, YC - 10, "250 µs", 12, MUTED, MONO)
# valid → stale : 같은 주소를 갱신
d.arrow([(XS[1] + BW + 4, YC), (XS[2] - 6, YC)], WARN, "warn", 1.6)
d.t((XS[1] + BW + XS[2]) / 2, YC - 28, "같은 LBA 갱신", 13, WARN, KR, "middle", 600)
d.t((XS[1] + BW + XS[2]) / 2, YC - 10, "새 page 에 쓰기", 12, MUTED, KR)
# stale → free : block erase (ㄷ자)
EY = Y + BH + 56
d.arrow([(XS[2] + BW / 2, Y + BH + 4), (XS[2] + BW / 2, EY), (XS[0] + BW / 2, EY), (XS[0] + BW / 2, Y + BH + 6)], ACC, "acc", 1.8)
d.t(XS[1] + BW / 2, EY - 12, "block erase", 14, ACC, MONO, "middle", 600)
d.t(XS[1] + BW / 2, EY + 22, "block 하나 · 1500 µs (SLC)", 12, MUTED, KR)

d.legend(H - 44, [("free", OK), ("valid", INFO), ("stale", WARN), ("지우기", ACC)])
d.save("04-01.ssd-page-states.svg")
