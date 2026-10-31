# 10-04 §3 — 공유 로그(전체 순서 브로드캐스트)의 신뢰 전달·전체 순서와 결정론적 상태 머신 복제(SMR) 수렴 흐름.
# 사실 출처: 10-04 §3(L56~L67), 원서 Ch.10 "Shared logs as consensus" & "Using shared logs"(PDF p.37~38, 41~43)
# 타입 스펙: type-data-flow
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, OK, WARN, KR, MONO

W = 880
LEG = 454
H = LEG + 56

d = D(W, H, "10-04 · §3 TOTAL ORDER BROADCAST AND STATE MACHINE REPLICATION", "공유 로그와 결정론적 상태 머신 복제 흐름",
      "신뢰 가능한 전달과 전체 순서를 보장하는 공유 로그를 통해 모든 복제본이 동일한 최종 상태에 도달한다.",
      "클라이언트 동시 제안 · 공유 로그 전체 순서 고정 · 복제본 결정론적 순차 실행 · 복제본 간 상태 수렴")

# 1. 1단계: 클라이언트 동시 쓰기 제안
C1_X, C1_Y, C1_W, C1_H = 24, 102, 164, 246
d.box(C1_X, C1_Y, C1_W, C1_H, PAPER2, RULE, 1.0)
d.chip(C1_X + 26, C1_Y + 20, "제안", WARN, 11, pad=4)
d.t(C1_X + 100, C1_Y + 24, "클라이언트 요청", 12, INK, KR, "middle", 600)
d.line(C1_X + 10, C1_Y + 38, C1_X + C1_W - 10, C1_Y + 38, RULE, 0.6)
d.t(C1_X + C1_W / 2, C1_Y + 52, "동시 비동기 쓰기 요청", 11, MUTED, KR, "middle")

# 요청 3개 박스 (y=162, 206, 250)
d.box(34, 162, 144, 38, PAPER, RULE, 0.8, r=4)
d.t(106, 185, "Client 1: set x=1", 11, INK, MONO, "middle")

d.box(34, 206, 144, 38, PAPER, RULE, 0.8, r=4)
d.t(106, 229, "Client 2: set y=2", 11, INK, MONO, "middle")

d.box(34, 250, 144, 38, PAPER, RULE, 0.8, r=4)
d.t(106, 273, "Client 3: set x=3", 11, INK, MONO, "middle")

d.t(C1_X + C1_W / 2, 320, "네트워크 순서 비결정론", 11, MUTED, KR, "middle")

# 2. 2단계: 공유 로그 (Total Order Broadcast)
C2_X, C2_Y, C2_W, C2_H = 224, 102, 216, 246
d.tone(C2_X, C2_Y, C2_W, C2_H, ACC, 6, "14", 1.4)
d.chip(C2_X + 28, C2_Y + 20, "순서", ACC, 11, pad=4)
d.t(C2_X + 120, C2_Y + 24, "공유 로그 (TOB)", 12, ACC, KR, "middle", 600)
d.line(C2_X + 10, C2_Y + 38, C2_X + C2_W - 10, C2_Y + 38, RULE, 0.6)
d.t(C2_X + C2_W / 2, C2_Y + 52, "신뢰 전달 + 전체 순서 고정", 11, INK, KR, "middle")

# 로그 3개 항목
d.box(236, 162, 192, 38, PAPER, RULE, 0.8, r=4)
d.t(332, 177, "[1] set x = 1", 11, INK, MONO, "middle", 600)
d.t(332, 191, "1번 슬롯 결정 (합의 값)", 11, ACC, KR, "middle")

d.box(236, 206, 192, 38, PAPER, RULE, 0.8, r=4)
d.t(332, 221, "[2] set y = 2", 11, INK, MONO, "middle", 600)
d.t(332, 235, "2번 슬롯 결정 (전체 순서)", 11, MUTED, KR, "middle")

d.box(236, 250, 192, 38, PAPER, RULE, 0.8, r=4)
d.t(332, 265, "[3] set x = 3", 11, INK, MONO, "middle", 600)
d.t(332, 279, "3번 슬롯 결정 (최종 갱신)", 11, MUTED, KR, "middle")

d.t(C2_X + C2_W / 2, 320, "첫 항목 = 단일 값 합의", 11, MUTED, KR, "middle")

# 화살표 1단계 -> 2단계
d.path("M 184 181 L 222 181", INFO, 1.2, m="info")
d.path("M 184 225 L 222 225", INFO, 1.2, m="info")
d.path("M 184 269 L 222 269", INFO, 1.2, m="info")

# 3. 3단계: 결정론적 상태 머신 복제본
C3_X, C3_Y, C3_W, C3_H = 476, 102, 204, 246
d.box(C3_X, C3_Y, C3_W, C3_H, PAPER2, RULE, 1.0)
d.chip(C3_X + 26, C3_Y + 20, "SMR", INFO, 11, pad=4)
d.t(C3_X + 116, C3_Y + 24, "상태 머신 복제", 12, INK, KR, "middle", 600)
d.line(C3_X + 10, C3_Y + 38, C3_X + C3_W - 10, C3_Y + 38, RULE, 0.6)
d.t(C3_X + C3_W / 2, C3_Y + 52, "동일 순서 결정론적 실행", 11, MUTED, KR, "middle")

# 복제본 3개
d.box(488, 162, 180, 38, PAPER, RULE, 0.8, r=4)
d.t(578, 177, "복제본 A (Replica 1)", 11, INK, KR, "middle", 600)
d.t(578, 191, "[1]→[2]→[3] 순차 실행", 11, INFO, KR, "middle")

d.box(488, 206, 180, 38, PAPER, RULE, 0.8, r=4)
d.t(578, 221, "복제본 B (Replica 2)", 11, INK, KR, "middle", 600)
d.t(578, 235, "[1]→[2]→[3] 순차 실행", 11, INFO, KR, "middle")

d.box(488, 250, 180, 38, PAPER, RULE, 0.8, r=4)
d.t(578, 265, "복제본 C (Replica 3)", 11, INK, KR, "middle", 600)
d.t(578, 279, "[1]→[2]→[3] 순차 실행", 11, INFO, KR, "middle")

d.t(C3_X + C3_W / 2, 320, "시작 상태 + 실행 순서 일치", 11, MUTED, KR, "middle")

# 화살표 2단계 -> 3단계
d.path("M 442 181 L 474 181", OK, 1.2, m="ok")
d.path("M 442 225 L 474 225", OK, 1.2, m="ok")
d.path("M 442 269 L 474 269", OK, 1.2, m="ok")

# 4. 4단계: 수렴된 최종 상태
C4_X, C4_Y, C4_W, C4_H = 716, 102, 140, 246
d.tone(C4_X, C4_Y, C4_W, C4_H, OK, 6, "14", 1.2)
d.chip(C4_X + 26, C4_Y + 20, "일치", OK, 11, pad=4)
d.t(C4_X + 84, C4_Y + 24, "수렴 상태", 12, OK, KR, "middle", 600)
d.line(C4_X + 10, C4_Y + 38, C4_X + C4_W - 10, C4_Y + 38, RULE, 0.6)
d.t(C4_X + C4_W / 2, C4_Y + 52, "전체 복제본 동일", 11, INK, KR, "middle")

# 수렴 데이터 박스
d.box(728, 162, 116, 126, PAPER, RULE, 0.8, r=4)
d.t(786, 182, "최종 상태", 11, MUTED, KR, "middle")
d.t(786, 206, "x = 3", 13, OK, MONO, "middle", 600)
d.t(786, 228, "y = 2", 13, OK, MONO, "middle", 600)
d.t(786, 252, "완전한 상태 일치", 11, INK, KR, "middle")
d.t(786, 270, "(x=1 은 덮어씀)", 11, MUTED, KR, "middle")

d.t(C4_X + C4_W / 2, 320, "단일 시스템처럼 동작", 11, MUTED, KR, "middle")

# 화살표 3단계 -> 4단계
d.path("M 682 225 L 714 225", OK, 1.2, m="ok")

# 하단 패널: SMR 핵심 원리와 실전 응용
d.box(24, 362, 832, 74, PAPER2, RULE, 1.0)
d.t(440, 384, "상태 머신 복제(SMR) 핵심 원리와 실전 응용", 13, INK, KR, "middle", 600)
d.t(440, 404, "동일한 초기 상태에서 동일한 로그 항목을 같은 순서로 결정론적 실행 시 모든 복제본은 동일한 상태 도달", 11, INK, KR, "middle")
d.t(440, 422, "응용: 단일 리더 복제 · 분산 KV 스토어 · 이벤트 소싱 · 직렬화 트랜잭션 · 스트림 처리", 11, MUTED, KR, "middle")

# 범례
d.legend(LEG, [
    ("공유 로그 전체 순서 (focal)", ACC),
    ("결정론적 상태 머신 복제", INFO),
    ("수렴 일치 상태", OK),
    ("동시 쓰기 제안", WARN)
])

d.save("10-04.total-order-broadcast-smr.svg")
