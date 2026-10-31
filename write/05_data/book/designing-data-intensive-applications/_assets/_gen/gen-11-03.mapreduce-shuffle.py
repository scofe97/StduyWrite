# 11-03 §5 — MapReduce 5단계 셔플과 분산 정렬 데이터 흐름(DDIA Fig 11-1).
# 사실 출처: 11-03 §5(L86~L108), 원서 Ch.11 Figure 11-1(PDF p.21~22)
# 타입 스펙: type-data-flow
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
LEG = 472
H = LEG + 48

d = D(W, H, "11-03 · §5 MAPREDUCE SHUFFLE ARCHITECTURE", "MapReduce 5단계 셔플과 분산 정렬 데이터 흐름",
      "매퍼가 키 해시 기반으로 로컬 파티션 파일을 생성하고 정렬하면, 리듀서가 네트워크를 통해 복사해 병합 정렬(MergeSort)한 뒤 키별 이터레이터로 집계 결과를 출력한다.",
      "HDFS 샤드 입력 · 키 해시 파티셔닝과 로컬 정렬 · 클러스터 전역 네트워크 복사(셔플) · MergeSort 병합 · 리듀서 이터레이터 및 DFS 저장")

# 상단 공통 전제 배너
d.tone(24, 102, W - 48, 34, INFO, 4, "14", 1.0)
d.t(W / 2, 124, "MapReduce 셔플 5단계: 키 해시 파티셔닝(1) → 네트워크 복사(2) → MergeSort 병합(3) → 리듀서 호출(4) → DFS 저장(5)", 12, INK, KR, "middle", 600)

# 좌측 영역: 매퍼 태스크 및 로컬 파티션 (X=24, W=236)
M_X, M_Y, M_W, M_H = 24, 146, 236, 316
d.box(M_X, M_Y, M_W, M_H, PAPER2, RULE, 1.0)
d.chip(M_X + 34, M_Y + 18, "1단계", INFO, 11, pad=4)
d.t(M_X + 70, M_Y + 22, "매퍼 태스크 (로컬 정렬)", 12, INFO, KR, "start", 600)
d.line(M_X + 10, M_Y + 34, M_X + M_W - 10, M_Y + 34, RULE, 0.6)

# Mapper 1 (Y=188, H=80)
d.box(M_X + 10, 188, M_W - 20, 80, PAPER, INFO, 0.9)
d.chip(M_X + 36, 204, "m1", WARN, 11, pad=3)
d.t(M_X + 112, 208, "매퍼 1 (Map Task 1)", 11, INK, KR, "middle", 600)
d.box(M_X + 14, 226, M_W - 28, 34, PAPER2, RULE, 0.7)
d.t(M_X + M_W / 2, 244, "[m1, r1]  [m1, r2]  [m1, r3]", 11, INK, MONO, "middle")

# Mapper 2 (Y=276, H=80)
d.box(M_X + 10, 276, M_W - 20, 80, PAPER, INFO, 0.9)
d.chip(M_X + 36, 292, "m2", WARN, 11, pad=3)
d.t(M_X + 112, 296, "매퍼 2 (Map Task 2)", 11, INK, KR, "middle", 600)
d.box(M_X + 14, 314, M_W - 28, 34, PAPER2, RULE, 0.7)
d.t(M_X + M_W / 2, 332, "[m2, r1]  [m2, r2]  [m2, r3]", 11, INK, MONO, "middle")

# Mapper 3 (Y=364, H=80)
d.box(M_X + 10, 364, M_W - 20, 80, PAPER, INFO, 0.9)
d.chip(M_X + 36, 380, "m3", WARN, 11, pad=3)
d.t(M_X + 112, 384, "매퍼 3 (Map Task 3)", 11, INK, KR, "middle", 600)
d.box(M_X + 14, 402, M_W - 28, 34, PAPER2, RULE, 0.7)
d.t(M_X + M_W / 2, 420, "[m3, r1]  [m3, r2]  [m3, r3]", 11, INK, MONO, "middle")

d.t(M_X + M_W / 2, 454, "키 해시 파티션별 로컬 정렬 파일", 11, MUTED, KR, "middle")

# 중앙 셔플 라벨
d.tone(274, 146, 172, 34, ACC, 4, "14", 1.2)
d.t(360, 168, "2단계: 네트워크 복사 (셔플)", 11, ACC, KR, "middle", 600)

# 우측 영역: 리듀서 태스크 및 HDFS 출력 (X=460, W=396)
R_X, R_Y, R_W, R_H = 460, 146, 396, 316
d.box(R_X, R_Y, R_W, R_H, PAPER2, RULE, 1.0)
d.chip(R_X + 38, R_Y + 18, "3~5단계", OK, 11, pad=4)
d.t(R_X + 80, R_Y + 22, "리듀서 병합 및 DFS 출력", 12, OK, KR, "start", 600)
d.line(R_X + 10, R_Y + 34, R_X + R_W - 10, R_Y + 34, RULE, 0.6)

# Reducer 1 (Y=188, H=80)
d.box(R_X + 10, 188, R_W - 20, 80, PAPER, OK, 0.9)
d.t(R_X + 90, 206, "리듀서 1 (r1 몫 복사)", 11, INK, KR, "middle", 600)
d.box(R_X + 16, 218, 168, 40, PAPER2, RULE, 0.7)
d.t(R_X + 100, 232, "[m1,r1] [m2,r1] [m3,r1]", 10, INK, MONO, "middle")
d.t(R_X + 100, 248, "MergeSort 동일 키 병합", 11, OK, KR, "middle")
d.path(f"M {R_X + 184} 238 L {R_X + 220} 238", OK, 1.2)
d.box(R_X + 220, 218, 60, 40, PAPER2, OK, 0.8)
d.t(R_X + 250, 242, "Reducer", 11, INK, MONO, "middle", 600)
d.path(f"M {R_X + 280} 238 L {R_X + 316} 238", WARN, 1.2)
d.chip(R_X + 342, 238, "DFS r1", WARN, 11, pad=4)

# Reducer 2 (Y=276, H=80)
d.box(R_X + 10, 276, R_W - 20, 80, PAPER, OK, 0.9)
d.t(R_X + 90, 294, "리듀서 2 (r2 몫 복사)", 11, INK, KR, "middle", 600)
d.box(R_X + 16, 306, 168, 40, PAPER2, RULE, 0.7)
d.t(R_X + 100, 320, "[m1,r2] [m2,r2] [m3,r2]", 10, INK, MONO, "middle")
d.t(R_X + 100, 336, "MergeSort 동일 키 병합", 11, OK, KR, "middle")
d.path(f"M {R_X + 184} 326 L {R_X + 220} 326", OK, 1.2)
d.box(R_X + 220, 306, 60, 40, PAPER2, OK, 0.8)
d.t(R_X + 250, 330, "Reducer", 11, INK, MONO, "middle", 600)
d.path(f"M {R_X + 280} 326 L {R_X + 316} 326", WARN, 1.2)
d.chip(R_X + 342, 326, "DFS r2", WARN, 11, pad=4)

# Reducer 3 (Y=364, H=80)
d.box(R_X + 10, 364, R_W - 20, 80, PAPER, OK, 0.9)
d.t(R_X + 90, 382, "리듀서 3 (r3 몫 복사)", 11, INK, KR, "middle", 600)
d.box(R_X + 16, 394, 168, 40, PAPER2, RULE, 0.7)
d.t(R_X + 100, 408, "[m1,r3] [m2,r3] [m3,r3]", 10, INK, MONO, "middle")
d.t(R_X + 100, 424, "MergeSort 동일 키 병합", 11, OK, KR, "middle")
d.path(f"M {R_X + 184} 414 L {R_X + 220} 414", OK, 1.2)
d.box(R_X + 220, 394, 60, 40, PAPER2, OK, 0.8)
d.t(R_X + 250, 418, "Reducer", 11, INK, MONO, "middle", 600)
d.path(f"M {R_X + 280} 414 L {R_X + 316} 414", WARN, 1.2)
d.chip(R_X + 342, 414, "DFS r3", WARN, 11, pad=4)

d.t(R_X + R_W / 2, 454, "키당 1회 이터레이터 호출 → DFS 출력 기록", 11, MUTED, KR, "middle")

# 네트워크 셔플 직교 연결선 (9개 경로)
X_OUT = M_X + M_W   # 260
X_IN = R_X + 10     # 470

# 1) Mapper 1 -> Reducers
# m1 -> r1 (수평)
d.path(f"M {X_OUT} 230 L {X_IN} 230", ACC, 1.3, m="acc")
# m1 -> r2 (직교 꺾임)
d.path(f"M {X_OUT} 242 L 350 242 L 350 318 L {X_IN} 318", ACC, 1.1, m="acc")
# m1 -> r3 (직교 꺾임)
d.path(f"M {X_OUT} 250 L 330 250 L 330 406 L {X_IN} 406", ACC, 1.1, m="acc")

# 2) Mapper 2 -> Reducers
# m2 -> r1 (직교 꺾임)
d.path(f"M {X_OUT} 318 L 370 318 L 370 238 L {X_IN} 238", ACC, 1.1, m="acc")
# m2 -> r2 (수평)
d.path(f"M {X_OUT} 326 L {X_IN} 326", ACC, 1.3, m="acc")
# m2 -> r3 (직교 꺾임)
d.path(f"M {X_OUT} 338 L 390 338 L 390 414 L {X_IN} 414", ACC, 1.1, m="acc")

# 3) Mapper 3 -> Reducers
# m3 -> r1 (직교 꺾임)
d.path(f"M {X_OUT} 406 L 410 406 L 410 246 L {X_IN} 246", ACC, 1.1, m="acc")
# m3 -> r2 (직교 꺾임)
d.path(f"M {X_OUT} 418 L 430 418 L 430 334 L {X_IN} 334", ACC, 1.1, m="acc")
# m3 -> r3 (수평)
d.path(f"M {X_OUT} 426 L {X_IN} 426", ACC, 1.3, m="acc")

# 범례
d.legend(LEG, [
    ("네트워크 셔플 (focal)", ACC),
    ("리듀서 병합·실행", OK),
    ("매퍼 파티셔닝·정렬", INFO),
    ("HDFS 분할 샤드", WARN),
])

d.save("11-03.mapreduce-shuffle.svg")
