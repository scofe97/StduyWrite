# 01-01 §8 — 기록 시스템에서 파생 데이터가 만들어지고, 파생 데이터는 잃어도 원본에서 다시 만든다.
# 옛 도식은 두 상자 사이에 원본·재생성 화살표 둘을 걸고 아래 문장 석 줄을 달았다. 문장(같은 PostgreSQL 이라도…)은
#   §9 도구의 중립성 본문이 맡는다. 여기서는 흐름과 재생성 방향만 남긴다.
# 타입 스펙: type-data-flow
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, KR, MONO

W = 880
AX, AW = 16, 248
BX, BW = 616, 248
NY, NH = 104, 240
PX_, PW_, PH_ = 372, 136, 48
MIDY = NY + NH / 2
CHIP_Y0, CHIP_STR, CHIP_H = NY + 72, 40, 32
RET_Y = NY + NH + 36
LEG = RET_Y + 40
H = LEG + 56

A_CHIPS = ["정본", "가장 먼저 기록", "정규화"]
B_CHIPS = ["캐시", "검색 인덱스", "구체화 뷰", "역정규화"]

d = D(W, H, "01-01 · RECORD VS DERIVED", "기록 시스템과 파생 데이터",
      "기록 시스템에서 파이프라인을 거쳐 파생 데이터가 만들어지고, 파생 데이터는 잃어도 같은 경로로 원본에서 다시 만들 수 있다. 재생성 경로가 핵심 논점이다.",
      "원본은 기록 시스템, 파생 데이터는 다시 만들 수 있는 사본")

d.box(AX, NY, AW, NH, PAPER2, INFO, 1.2)
d.t(AX + 16, NY + 30, "기록 시스템", 15, INK, KR, "start", 600)
d.t(AX + 16, NY + 50, "system of record", 11, MUTED, MONO, "start")
for j, txt in enumerate(A_CHIPS):
    y = CHIP_Y0 + j * CHIP_STR
    d.box(AX + 16, y, AW - 32, CHIP_H, PAPER, RULE, 0.9)
    d.t(AX + 32, y + 21, txt, 13, INK, KR, "start")

d.box(BX, NY, BW, NH, PAPER2, RULE, 1.0)
d.t(BX + 16, NY + 30, "파생 데이터 시스템", 15, INK, KR, "start", 600)
d.t(BX + 16, NY + 50, "derived data system", 11, MUTED, MONO, "start")
for j, txt in enumerate(B_CHIPS):
    y = CHIP_Y0 + j * CHIP_STR
    d.box(BX + 16, y, BW - 32, CHIP_H, PAPER, RULE, 0.9)
    d.t(BX + 32, y + 21, txt, 13, INK, KR, "start")

d.box(PX_, MIDY - PH_ / 2, PW_, PH_, PAPER2, RULE, 1.0)
d.t(PX_ + PW_ / 2, MIDY + 5, "데이터 파이프라인", 13, INK, KR, "middle", 600)
d.arrow([(AX + AW + 8, MIDY), (PX_ - 8, MIDY)], MUTED, "ar", 1.6)
d.arrow([(PX_ + PW_ + 8, MIDY), (BX - 8, MIDY)], MUTED, "ar", 1.6)

# 재생성 — 파생 쪽에서 원본 쪽으로 ㄷ자로 돌아간다(모두 직각)
bx, ax = BX + BW / 2, AX + AW / 2
d.arrow([(bx, NY + NH + 4), (bx, RET_Y), (ax, RET_Y), (ax, NY + NH + 8)], ACC, "acc", 1.8, "5 4")
lw = 148
d.box((bx + ax) / 2 - lw / 2, RET_Y - 14, lw, 28, PAPER, PAPER, 0, 6)   # 점선이 라벨 밑으로 비치지 않게 바탕을 먼저 깐다
d.tone((bx + ax) / 2 - lw / 2, RET_Y - 14, lw, 28, ACC, 6, "26", 1.4)
d.t((bx + ax) / 2, RET_Y + 5, "원본에서 재생성", 13, INK, KR, "middle", 600)

d.legend(LEG, [("기록 시스템", INFO), ("재생성 경로", ACC)])
d.save("01-01.record-vs-derived.svg")
