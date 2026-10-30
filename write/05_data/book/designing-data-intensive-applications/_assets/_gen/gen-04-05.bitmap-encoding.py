# 04-05 §2 — 컬럼 값 시퀀스의 비트맵 인코딩과 run-length 압축 및 비트 연산 필터링.
# 사실 출처: 본문 §2(L45~L54), DDIA Figure 4-8(Compressed, bitmap-indexed storage of a single column). 행 값은 Figure 4-8 앞 8행, 질의 값 (30, 74)는 예시. 옛 값은 distinct 30·31·69 라 해 놓고 32 를 넣은 모순이 있어 2026-10-30 교체
# 타입 스펙: type-data-flow
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
PY = 104
LEG = 412
H = LEG + 56

d = D(W, H, "04-05 · BITMAP ENCODING", "비트맵 인코딩 압축과 비트 단위 쿼리 필터링",
      "distinct 값이 적은 컬럼을 값별 1비트 비트맵으로 변환하고 희소 비트맵을 run-length 인코딩으로 압축하며 질의를 비트 연산으로 고속 처리한다.",
      "컬럼 시퀀스 · distinct 비트맵 분해 · Run-Length 압축 · 비트 OR 질의")

X0 = 24
BOX_W = 832

# 1구간: 원본 product_sk 컬럼 시퀀스
S1_Y = PY
S1_H = 64
d.box(X0, S1_Y, BOX_W, S1_H, PAPER2, RULE, 0.9)
d.chip(X0 + 40, S1_Y + 20, "1단계", SOFT, 11)
d.t(X0 + 84, S1_Y + 24, "product_sk 컬럼 값 시퀀스", 13, INK, KR, "start", 600)
d.t(X0 + BOX_W - 20, S1_Y + 24, "원서 Figure 4-8 앞 8행 (distinct 값 30 · 69 · 74)", 11.5, SOFT, KR, "end")
d.line(X0 + 12, S1_Y + 36, X0 + BOX_W - 12, S1_Y + 36, RULE, 0.8)

# 8개 행 셀 표시
row_vals = ["69", "69", "69", "69", "74", "30", "30", "30"]
CW_CELL = 52
C_GAP = 8
C_START = X0 + 116

for i, val in enumerate(row_vals):
    cx = C_START + i * (CW_CELL + C_GAP)
    d.box(cx, S1_Y + 40, CW_CELL, 18, PAPER, RULE, 0.8)
    d.t(cx + CW_CELL / 2, S1_Y + 53, f"r{i}:{val}", 11, INK, MONO, "middle", 600)

# 아래로 흐름 화살표
d.arrow([(W / 2, S1_Y + S1_H + 2), (W / 2, S1_Y + S1_H + 14)], SOFT, "soft", 1.2)

# 2구간: 값별 비트맵 분해 및 Run-Length 인코딩
S2_Y = S1_Y + S1_H + 16
S2_H = 126
d.box(X0, S2_Y, BOX_W, S2_H, PAPER2, ACC, 1.2)
d.chip(X0 + 40, S2_Y + 20, "2단계", ACC, 11)
d.t(X0 + 84, S2_Y + 24, "distinct 값별 비트맵 및 RLE 압축 (행당 1비트)", 13, INK, KR, "start", 600)
d.t(X0 + BOX_W - 20, S2_Y + 24, "희소 비트맵은 연속 0·1 개수(run-length)로 압축", 11.5, SOFT, KR, "end")
d.line(X0 + 12, S2_Y + 36, X0 + BOX_W - 12, S2_Y + 36, RULE, 0.8)

bm_data = [
    ("val = 30", [0, 0, 0, 0, 0, 1, 1, 1], "0이 5개 · 1이 3개"),
    ("val = 69", [1, 1, 1, 1, 0, 0, 0, 0], "1이 4개 · 0이 4개"),
    ("val = 74", [0, 0, 0, 0, 1, 0, 0, 0], "0이 4개 · 1이 1개 · 0이 3개"),
]

for idx, (label, bits, rle_desc) in enumerate(bm_data):
    by = S2_Y + 44 + idx * 26
    d.t(X0 + 64, by + 14, label, 11.5, INK, MONO, "middle", 600)
    for bi, b in enumerate(bits):
        bcx = C_START + bi * (CW_CELL + C_GAP)
        b_col = OK if b == 1 else PAPER
        d.box(bcx, by, CW_CELL, 20, b_col, OK if b == 1 else RULE, 1.0)
        d.t(bcx + CW_CELL / 2, by + 14, str(b), 11.5, INK if b == 1 else SOFT, MONO, "middle", 600)
    d.t(X0 + BOX_W - 16, by + 14, f"RLE: {rle_desc}", 11, ACC, KR, "end")

# 아래로 흐름 화살표
d.arrow([(W / 2, S2_Y + S2_H + 2), (W / 2, S2_Y + S2_H + 14)], SOFT, "soft", 1.2)

# 3구간: 비트 OR 연산 질의 필터링
S3_Y = S2_Y + S2_H + 16
S3_H = 76
d.box(X0, S3_Y, BOX_W, S3_H, PAPER2, OK, 1.2)
d.chip(X0 + 40, S3_Y + 20, "3단계", OK, 11)
d.t(X0 + 84, S3_Y + 24, "질의 실행: WHERE product_sk IN (30, 74)", 13, INK, KR, "start", 600)
d.t(X0 + BOX_W - 20, S3_Y + 24, "두 비트맵 로드 후 비트 단위 OR 계산", 11.5, OK, KR, "end", 600)
d.line(X0 + 12, S3_Y + 36, X0 + BOX_W - 12, S3_Y + 36, RULE, 0.8)

# 결과 비트맵 (행 4~7 매칭)
res_bits = [0, 0, 0, 0, 1, 1, 1, 1]
d.t(X0 + 64, S3_Y + 58, "결과 비트", 11.5, OK, KR, "middle", 600)
for bi, b in enumerate(res_bits):
    rcx = C_START + bi * (CW_CELL + C_GAP)
    r_col = OK if b == 1 else PAPER
    d.box(rcx, S3_Y + 44, CW_CELL, 22, r_col, OK if b == 1 else RULE, 1.2)
    d.t(rcx + CW_CELL / 2, S3_Y + 59, f"{b} (일치)" if b == 1 else "0", 11, INK if b == 1 else SOFT, KR if b == 1 else MONO, "middle", 600)

d.t(X0 + BOX_W - 16, S3_Y + 58, "행 4 · 5 · 6 · 7 일치", 12, OK, KR, "end", 600)

d.legend(LEG, [("일치 비트 (1값 매칭)", OK), ("RLE 연속 압축 정보", ACC), ("불일치 비트 (0값)", SOFT)])
d.save("04-05.bitmap-encoding.svg")
