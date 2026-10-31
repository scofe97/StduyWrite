# 11-03 §4 — MapReduce 태스크 실패 시 DFS 중간 파일 기반 격리와 독립 재실행 흐름.
# 사실 출처: 11-03 §4(L77~L96), 원서 Ch.11 "Handling faults"(PDF p.16~17: 부분 출력 삭제 후 다른 머신에서 재실행, 태스크 단위 재시도). 샤드 이름 m1~m3 은 원서 p.21 Figure 11-1.
# 타입 스펙: type-process
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
LEG = 414
H = LEG + 48

d = D(W, H, "11-03 · §4 MAPREDUCE FAULT TOLERANCE", "태스크 실패 격리와 독립 재실행 흐름",
      "하드웨어 결함이나 Spot 인스턴스 선점으로 태스크가 실패하면 부분 출력을 삭제한 뒤 해당 태스크만 DFS 입력에서 단독 재실행하며, 이미 성공한 다른 태스크는 영향을 받지 않는다.",
      "DFS 입력 불변성 · 무상태 매퍼 멱등 재실행 · 부분 출력 삭제 · 다른 태스크 영향 없는 단독 재시작")

# 상단 공통 전제 배너
d.tone(24, 102, W - 48, 34, INFO, 4, "14", 1.0)
d.t(W / 2, 124, "배치 재실행 의미론: DFS 입력 불변성 + 무상태 매퍼 + 부분 출력 삭제 후 실패 태스크만 독립 재시작", 12, INK, KR, "middle", 600)

# 좌측: DFS 입력 샤드 (Shard m1, m2, m3)
IN_X, IN_W = 24, 120
d.box(IN_X, 148, IN_W, 250, PAPER2, RULE, 1.0)
d.t(IN_X + IN_W / 2, 168, "DFS 입력 샤드", 12, INFO, KR, "middle", 600)
d.line(IN_X + 10, 174, IN_X + IN_W - 10, 174, RULE, 0.6)

# Shard 1 (y=182, h=34, center 199)
d.box(IN_X + 12, 182, IN_W - 24, 34, PAPER, INFO, 0.8)
d.t(IN_X + IN_W / 2, 204, "샤드 m1", 12, INK, KR, "middle", 600)

# Shard 2 (y=256, h=34, center 273)
d.box(IN_X + 12, 256, IN_W - 24, 34, PAPER, INFO, 0.8)
d.t(IN_X + IN_W / 2, 278, "샤드 m2", 12, INK, KR, "middle", 600)

# Shard 3 (y=348, h=34, center 365)
d.box(IN_X + 12, 348, IN_W - 24, 34, PAPER, INFO, 0.8)
d.t(IN_X + IN_W / 2, 370, "샤드 m3", 12, INK, KR, "middle", 600)

# 중앙: 매퍼 태스크 실행 영역 (X=168, W=524)
T_X, T_W = 168, 524

# Row 1: 태스크 1 (정상 실행)
R1_Y, R1_H = 148, 68
d.box(T_X, R1_Y, T_W, R1_H, PAPER2, OK, 0.9)
d.chip(T_X + 38, R1_Y + 18, "Task 1", OK, 11, pad=4)
d.t(T_X + 130, R1_Y + 22, "매퍼 1 (Node A)", 12, INK, KR, "middle", 600)
d.t(T_X + 204, R1_Y + 48, "레코드 매핑 처리 → 중간 파일 저장", 11, MUTED, KR, "start")
d.box(T_X + 400, R1_Y + 34, 112, 24, PAPER, OK, 0.8)
d.t(T_X + 456, R1_Y + 50, "정상 완료 유지", 11, OK, KR, "middle", 600)

# Row 2: 태스크 2 (실패 후 재실행) - focal
R2_Y, R2_H = 224, 98
d.tone(T_X, R2_Y, T_W, R2_H, ACC, 6, "14", 1.4)
d.chip(T_X + 38, R2_Y + 18, "Task 2", ACC, 11, pad=4)
d.t(T_X + 130, R2_Y + 22, "매퍼 2 (Node B)", 12, ACC, KR, "middle", 600)

# 실패 단계 (BAD)
d.box(T_X + 14, R2_Y + 38, 226, 26, PAPER, BAD, 0.9)
d.t(T_X + 127, R2_Y + 55, "Spot 선점/장애로 중단 (FAIL)", 11, BAD, KR, "middle", 600)

# 복구 및 재실행 단계 (ACC)
d.path(f"M {T_X + 240} {R2_Y + 51} L {T_X + 262} {R2_Y + 51}", ACC, 1.2, m="acc")

d.box(T_X + 262, R2_Y + 38, 250, 52, PAPER, ACC, 1.0)
d.t(T_X + 387, R2_Y + 55, "부분 출력 삭제 후 Node D 에서 재실행", 11, INK, KR, "middle", 600)
d.t(T_X + 387, R2_Y + 76, "샤드 m2 재읽기 → 중간 파일 정상 생성 완료", 11, OK, KR, "middle")

# Row 3: 태스크 3 (정상 실행)
R3_Y, R3_H = 330, 68
d.box(T_X, R3_Y, T_W, R3_H, PAPER2, OK, 0.9)
d.chip(T_X + 38, R3_Y + 18, "Task 3", OK, 11, pad=4)
d.t(T_X + 130, R3_Y + 22, "매퍼 3 (Node C)", 12, INK, KR, "middle", 600)
d.t(T_X + 204, R3_Y + 48, "레코드 매핑 처리 → 중간 파일 저장", 11, MUTED, KR, "start")
d.box(T_X + 400, R3_Y + 34, 112, 24, PAPER, OK, 0.8)
d.t(T_X + 456, R3_Y + 50, "정상 완료 유지", 11, OK, KR, "middle", 600)

# 우측: 후속 셔플 단계 (X=716, W=140)
OUT_X, OUT_W = 716, 140
d.box(OUT_X, 148, OUT_W, 250, PAPER2, INFO, 1.0)
d.t(OUT_X + OUT_W / 2, 170, "다음 단계: 정렬·셔플", 12, INFO, KR, "middle", 600)
d.line(OUT_X + 10, 180, OUT_X + OUT_W - 10, 180, RULE, 0.6)

d.t(OUT_X + OUT_W / 2, 215, "모든 매퍼 출력 완료", 11, INK, KR, "middle")
d.t(OUT_X + OUT_W / 2, 235, "(m1 · m2 · m3 출력 준비)", 11, MUTED, KR, "middle")
d.box(OUT_X + 10, 260, OUT_W - 20, 48, PAPER, OK, 0.8)
d.t(OUT_X + OUT_W / 2, 280, "리듀서 셔플 복사", 11, OK, KR, "middle", 600)
d.t(OUT_X + OUT_W / 2, 298, "네트워크 전송 개시", 11, MUTED, KR, "middle")

# 수평 직교 연결선 (Strictly horizontal)
# Shards -> Tasks
d.path(f"M {IN_X + IN_W} 199 L {T_X} 199", INFO, 1.3, m="info")
d.path(f"M {IN_X + IN_W} 273 L {T_X} 273", INFO, 1.3, m="info")
d.path(f"M {IN_X + IN_W} 365 L {T_X} 365", INFO, 1.3, m="info")

# Tasks -> Right Column
d.path(f"M {T_X + T_W} 182 L {OUT_X} 182", OK, 1.3, m="ok")
d.path(f"M {T_X + T_W} 273 L {OUT_X} 273", OK, 1.3, m="ok")
d.path(f"M {T_X + T_W} 364 L {OUT_X} 364", OK, 1.3, m="ok")

# 범례
d.legend(LEG, [
    ("실패 재실행 (focal)", ACC),
    ("정상 산출물", OK),
    ("불변 입력 샤드", INFO),
    ("노드 장애 중단", BAD),
])

d.save("11-03.task-failure-retry.svg")
