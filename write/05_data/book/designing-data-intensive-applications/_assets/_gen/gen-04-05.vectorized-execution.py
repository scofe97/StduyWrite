# 04-05 §4 — 벡터화 처리(vectorized processing) 파이프라인과 SIMD 비트 연산.
# 사실 출처: 본문 §4(L67~L76), DDIA Figure 4-9(A bitwise AND between two bitmaps lends itself to vectorization). 배치는 Figure 4-8·4-9 의 5~12번째 행(product_sk = 30, store_sk = 3). store_sk 의 3 아닌 값은 원서에 없어 · 로 둠. 2026-10-30 검증에서 지어낸 69·32 배치를 교체
# 타입 스펙: type-process
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
PY = 104
LEG = 412
H = LEG + 56

d = D(W, H, "04-05 · VECTORIZED EXECUTION", "벡터화 쿼리 실행과 SIMD 비트 연산",
      "컬럼 데이터를 수천 개 단위의 배치로 묶어 사전 정의된 연산자로 넘기고 SIMD 비트 연산으로 행을 걸러 CPU 시간을 절감한다.",
      "컬럼 배치 입력 · 동등 비교 연산자 · SIMD 비트 AND · 일치 행 버퍼")

X0 = 24
BOX_W = 832

# 1단계: 입력 컬럼 벡터 배치 (product_sk, store_sk)
S1_Y = PY
S1_H = 74
d.box(X0, S1_Y, BOX_W, S1_H, PAPER2, RULE, 0.9)
d.chip(X0 + 44, S1_Y + 20, "1단계", INFO, 11)
d.t(X0 + 94, S1_Y + 24, "입력 컬럼 벡터 배치 (Vector Batches)", 13, INK, KR, "start", 600)
d.t(X0 + BOX_W - 20, S1_Y + 24, "행 루프 대신 컬럼 값 묶음을 한꺼번에 전달", 11.5, SOFT, KR, "end")
d.line(X0 + 12, S1_Y + 36, X0 + BOX_W - 12, S1_Y + 36, RULE, 0.8)

# 두 컬럼 배치 나란히 표시
BW_SUB = 394
d.box(X0 + 16, S1_Y + 42, BW_SUB, 24, PAPER, RULE, 0.8)
d.t(X0 + 26, S1_Y + 58, "product_sk 배치", 11.5, INFO, MONO, "start", 600)
d.t(X0 + BW_SUB + 6, S1_Y + 58, "[ 74, 30, 30, 30, 30, 29, 31, 31 ]", 11, INK, MONO, "end")

d.box(X0 + 422, S1_Y + 42, BW_SUB, 24, PAPER, RULE, 0.8)
d.t(X0 + 432, S1_Y + 58, "store_sk 배치 (·=3 아님)", 11.5, INFO, MONO, "start", 600)
d.t(X0 + 422 + BW_SUB - 10, S1_Y + 58, "[  3,  ·,  3,  3,  ·,  ·,  ·,  · ]", 11, INK, MONO, "end")

# 화살표 아래로 (수직)
d.arrow([(X0 + 16 + BW_SUB / 2, S1_Y + S1_H + 2), (X0 + 16 + BW_SUB / 2, S1_Y + S1_H + 14)], SOFT, "soft", 1.2)
d.arrow([(X0 + 422 + BW_SUB / 2, S1_Y + S1_H + 2), (X0 + 422 + BW_SUB / 2, S1_Y + S1_H + 14)], SOFT, "soft", 1.2)

# 2단계: 사전 정의된 연산자 실행 및 중간 비트맵 산출
S2_Y = S1_Y + S1_H + 16
S2_H = 74
d.box(X0, S2_Y, BOX_W, S2_H, PAPER2, ACC, 1.2)
d.chip(X0 + 44, S2_Y + 20, "2단계", ACC, 11)
d.t(X0 + 94, S2_Y + 24, "벡터 동등 비교 연산자 (Equality Operators)", 13, INK, KR, "start", 600)
d.t(X0 + BOX_W - 20, S2_Y + 24, "각 연산자가 1비트 단위 결과 비트맵 배치 생성", 11.5, SOFT, KR, "end")
d.line(X0 + 12, S2_Y + 36, X0 + BOX_W - 12, S2_Y + 36, RULE, 0.8)

# 좌측 연산자: product == 69
d.box(X0 + 16, S2_Y + 42, BW_SUB, 24, PAPER, RULE, 0.8)
d.t(X0 + 26, S2_Y + 58, "연산자 == 30", 11.5, ACC, MONO, "start", 600)
d.t(X0 + BW_SUB + 6, S2_Y + 58, "비트맵 A: [ 0, 1, 1, 1, 1, 0, 0, 0 ]", 11, ACC, MONO, "end")

# 우측 연산자: store == 3
d.box(X0 + 422, S2_Y + 42, BW_SUB, 24, PAPER, RULE, 0.8)
d.t(X0 + 432, S2_Y + 58, "연산자 == 3", 11.5, ACC, MONO, "start", 600)
d.t(X0 + 422 + BW_SUB - 10, S2_Y + 58, "비트맵 B: [ 1, 0, 1, 1, 0, 0, 0, 0 ]", 11, ACC, MONO, "end")

# 두 연산자에서 아래 3단계로 직각(elbow) 화살표
d.arrow([(X0 + 16 + BW_SUB / 2, S2_Y + S2_H + 2), (X0 + 16 + BW_SUB / 2, S2_Y + S2_H + 8), (W / 2 - 40, S2_Y + S2_H + 8), (W / 2 - 40, S2_Y + S2_H + 14)], SOFT, "soft", 1.2)
d.arrow([(X0 + 422 + BW_SUB / 2, S2_Y + S2_H + 2), (X0 + 422 + BW_SUB / 2, S2_Y + S2_H + 8), (W / 2 + 40, S2_Y + S2_H + 8), (W / 2 + 40, S2_Y + S2_H + 14)], SOFT, "soft", 1.2)

# 3단계: SIMD 비트 단위 AND 연산 및 최종 결과
S3_Y = S2_Y + S2_H + 16
S3_H = 114
d.box(X0, S3_Y, BOX_W, S3_H, PAPER2, OK, 1.4)
d.chip(X0 + 44, S3_Y + 20, "3단계", OK, 11)
d.t(X0 + 94, S3_Y + 24, "SIMD 비트 AND 연산 및 조건 일치 행 확정", 13, INK, KR, "start", 600)
d.t(X0 + BOX_W - 20, S3_Y + 24, "SIMD 로 여러 비트를 한꺼번에 AND", 11.5, OK, KR, "end", 600)
d.line(X0 + 12, S3_Y + 36, X0 + BOX_W - 12, S3_Y + 36, RULE, 0.8)

# 최종 결과 비트맵
d.tone(X0 + 16, S3_Y + 44, BOX_W - 32, 28, OK, 4, "18", 1.0)
d.t(X0 + 26, S3_Y + 62, "bitwise AND 결과", 11.5, OK, KR, "start", 600)
d.t(W / 2, S3_Y + 62, "[ 0, 0, 1, 1, 0, 0, 0, 0 ]", 12, INK, MONO, "middle", 600)
d.t(X0 + BOX_W - 28, S3_Y + 62, "셋째 · 넷째 값 일치", 12, OK, KR, "end", 600)

# CPU 하드웨어 최적화 이점
d.box(X0 + 16, S3_Y + 78, BOX_W - 32, 26, PAPER, RULE, 0.8)
d.t(X0 + 26, S3_Y + 95, "CPU 효율 핵심", 11, SOFT, KR, "start", 600)
d.t(X0 + 140, S3_Y + 95, "순차 메모리 접근 (캐시 미스↓)", 11, INK, KR, "start")
d.t(X0 + 340, S3_Y + 95, "타이트한 루프 (분기 예측 실패↓)", 11, INK, KR, "start")
d.t(X0 + 550, S3_Y + 95, "SIMD 명령어 병렬 처리", 11, OK, KR, "start")
d.t(X0 + BOX_W - 28, S3_Y + 95, "압축 데이터 직접 연산", 11, ACC, KR, "end")

d.legend(LEG, [("컬럼 벡터 입력", INFO), ("중간 결과 비트맵", ACC), ("SIMD 비트 연산 결과", OK), ("하드웨어 효율 요소", SOFT)])
d.save("04-05.vectorized-execution.svg")
