# 07-01 §3 키 범위 샤딩 — 데이터 밀도에 맞춘 불균등 백과사전식 키 범위 할당과 정렬 저장.
# 사실 출처: 07-01 본문 §3(L50~L58), DDIA 2판 7장 Figure 7-2 "A print encyclopedia is sharded by key range" (PDF 8쪽).
# 권 이름은 Figure 7-2 책등 글자 그대로(1 A-ak—Bayes, 2 Bayeu—Ceanothus, 3 Ceara—Deluc, 12 Trudeau—Zywiec). 4~11권은 생략 표시만 둔다.
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
CH = 120
H = 172 + CH + 16 + 84 + 82
LEG = H - 48

d = D(W, H, "07-01 · §3 KEY RANGE SHARDING", "백과사전식 키 범위 샤딩과 적응형 경계",
      "데이터 분포에 맞추어 불균등한 키 범위를 샤드에 할당하고 내부를 정렬 저장하여 효율적인 범위 스캔을 지원한다.",
      "알파벳 키 구간 할당 · 데이터 밀도 적응형 경계 · 샤드 내 정렬 저장(SSTable·B-tree) · 효율적인 범위 스캔")

# 1. 상단 연속 키 공간 바 (keyspace strip)
BY = 104
BH = 52
d.box(36, BY, W - 72, BH, PAPER2, RULE, 1.0)
d.t(48, BY + 18, "전체 키 공간 (A-ak .. Zywiec, 12권)", 12, SOFT, KR, "start", 600)

# 키 공간 분할 세그먼트 4개 (불균등 분할 시각화)
seg_def = [
    (52, 160, "A-ak .. Bayes", "A·B 구간 (고밀도)", INFO),
    (220, 160, "Bayeu .. Ceanothus", "B·C 구간 (중간)", INFO),
    (388, 160, "Ceara .. Deluc", "C·D 구간 (중간)", INFO),
    (650, W - 36 - 16 - 650, "Trudeau .. Zywiec", "T~Z 구간", ACC),
]

for sx, sw, srange, sdesc, scol in seg_def:
    d.tone(sx, BY + 26, sw, 20, scol, 3, "16", 0.9)
    d.t(sx + sw / 2, BY + 39, srange, 11, INK, MONO, "middle")
d.t(599, BY + 40, "… 4~11권 …", 11, MUTED, KR, "middle")

# 2. 대표 샤드 4개 카드 (Volume 1, 2, 3, 12)
CW = 192
GAP = 13
X0 = 36
Y_CARDS = 172

cards = [
    ("샤드 1", "A-ak .. Bayes", "제1권 (Volume 1)",
     [("A·B 두 글자 구간", "")],
     INFO),
    ("샤드 2", "Bayeu .. Ceanothus", "제2권 (Volume 2)",
     [("B~C 사이 좁은 구간", "")],
     INFO),
    ("샤드 3", "Ceara .. Deluc", "제3권 (Volume 3)",
     [("C~D 사이 좁은 구간", "")],
     INFO),
    ("샤드 12", "Trudeau .. Zywiec", "제12권 (Volume 12)",
     [("T~Z 일곱 글자 구간", "")],
     ACC),
]

for i, (c_chip, c_range, c_title, items, c_col) in enumerate(cards):
    cx = X0 + i * (CW + GAP)
    is_focal = (c_col == ACC)

    if is_focal:
        d.box(cx, Y_CARDS, CW, CH, PAPER2, ACC, 1.4)
    else:
        d.box(cx, Y_CARDS, CW, CH, PAPER2, RULE, 0.9)

    d.chip(cx + CW / 2, Y_CARDS + 18, c_chip, c_col, 11)
    d.tone(cx + 12, Y_CARDS + 36, CW - 24, 24, c_col, 4, "14", 0.9)
    d.t(cx + CW / 2, Y_CARDS + 52, c_range, 11.5, INK, MONO, "middle")

    d.t(cx + CW / 2, Y_CARDS + 76, c_title, 12, INK if is_focal else c_col, KR, "middle", 600)
    d.line(cx + 12, Y_CARDS + 86, cx + CW - 12, Y_CARDS + 86, RULE, 0.8)

    for j, (top_t, bot_t) in enumerate(items):
        iy = Y_CARDS + 96 + j * 26
        d.t(cx + 16, iy + 10, "·", 12, c_col, KR, "start")
        d.t(cx + 26, iy + 10, top_t, 11.5, INK, KR, "start")

# 3. 하단 기능 블록 (범위 스캔 & 경계 관리)
Y_BOT = Y_CARDS + CH + 16
HBOT = 84

# 좌측: 범위 스캔 특성
d.tone(36, Y_BOT, 452, HBOT, OK, 6, "10", 1.0)
d.t(52, Y_BOT + 22, "샤드 내부 정렬 · 범위 스캔", 12.5, OK, KR, "start", 600)
d.box(52, Y_BOT + 32, 420, 24, PAPER, OK, 0.8)
d.t(62, Y_BOT + 48, "타임스탬프 키 · 특정 달 측정값 전체", 11.5, INK, KR, "start")
d.t(52, Y_BOT + 72, "B-tree 또는 SSTable · 범위 쿼리 한 번", 11.5, MUTED, KR, "start")

# 우측: 경계 관리 시스템
d.box(500, Y_BOT, 344, HBOT, PAPER2, RULE, 0.9)
d.t(516, Y_BOT + 22, "샤드 경계 관리 방식", 12.5, INK, KR, "start", 600)
d.tone(516, Y_BOT + 34, 150, 40, OK, 4, "12", 0.8)
d.t(591, Y_BOT + 49, "수동 경계 설정", 11.5, OK, KR, "middle", 600)
d.t(591, Y_BOT + 65, "Vitess · MySQL", 11, MUTED, MONO, "middle")

d.tone(678, Y_BOT + 34, 150, 40, OK, 4, "12", 0.8)
d.t(753, Y_BOT + 49, "자동 경계 관리", 11.5, OK, KR, "middle", 600)
d.t(753, Y_BOT + 65, "HBase · CockroachDB", 11, MUTED, MONO, "middle")

# 하단 범례
d.legend(LEG, [
    ("고밀도 샤드 (좁은 구간)", INFO),
    ("저밀도 샤드 (넓은 구간)", ACC),
    ("범위 스캔 · 경계 관리", OK),
])

d.save("07-01.key-range-sharding.svg")
