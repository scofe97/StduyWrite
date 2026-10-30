# 06-04 §1 — 멀티리전 다중 리더 복제 아키텍처와 데이터센터 간 비동기 복제.
# 사실 출처: 06-04 §1(L27~L37), DDIA 2판 6장 Figure 6-5 "Multi-leader replication across datacenters"
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
H = 550
LEG = H - 48

d = D(W, H, "06-04 · MULTI-LEADER REPLICATION", "멀티리전 다중 리더 복제 구조",
      "각 리전 리더가 로컬 쓰기를 즉각 처리하고, 인터리전 링크를 통해 비동기 양방향 복제하는 아키텍처.",
      "로컬 쓰기 처리 · 리전 내부 팔로워 복제 · 인터리전 비동기 복제 · 지연 은닉과 일관성 대가")

Y_BOX = 104
H_BOX = 276

# 1. 좌측: 리전 A 데이터센터
X_A = 24
W_A = 344
d.box(X_A, Y_BOX, W_A, H_BOX, PAPER2, RULE, 0.9)
d.t(X_A + 16, Y_BOX + 24, "리전 A (Region A)", 12, SOFT, KR, "start", 600)

# 리전 A 클라이언트
d.box(X_A + 16, Y_BOX + 42, 116, 52, PAPER, RULE, 0.8)
d.t(X_A + 74, Y_BOX + 64, "클라이언트 A", 12, INK, KR, "middle", 600)
d.t(X_A + 74, Y_BOX + 82, "로컬 쓰기 요청", 12, MUTED, KR, "middle")

# 리전 A 리더
d.tone(X_A + 184, Y_BOX + 42, 144, 52, ACC, 6, "22", 1.2)
d.t(X_A + 256, Y_BOX + 64, "리더 노드 A", 13, INK, KR, "middle", 600)
d.t(X_A + 256, Y_BOX + 82, "쓰기를 로컬에서 처리", 12, ACC, KR, "middle")

# 클라이언트 A -> 리더 A 화살표 (길이 46px)
d.arrow([(X_A + 134, Y_BOX + 68), (X_A + 180, Y_BOX + 68)], ACC, "acc", 1.4)

# 리전 A 팔로워들
d.box(X_A + 20, Y_BOX + 140, 140, 50, PAPER, INFO, 1.0)
d.t(X_A + 90, Y_BOX + 162, "팔로워 A1", 12, INK, KR, "middle", 600)
d.t(X_A + 90, Y_BOX + 180, "로컬 읽기 서빙", 12, INFO, KR, "middle")

d.box(X_A + 184, Y_BOX + 140, 140, 50, PAPER, INFO, 1.0)
d.t(X_A + 254, Y_BOX + 162, "팔로워 A2", 12, INK, KR, "middle", 600)
d.t(X_A + 254, Y_BOX + 180, "로컬 읽기 서빙", 12, INFO, KR, "middle")

# 리더 A -> 팔로워들 내부 복제 화살표 (Manhattan 직교)
d.arrow([(X_A + 220, Y_BOX + 94), (X_A + 220, Y_BOX + 116), (X_A + 90, Y_BOX + 116), (X_A + 90, Y_BOX + 136)], INFO, "info", 1.2)
d.arrow([(X_A + 280, Y_BOX + 94), (X_A + 280, Y_BOX + 136)], INFO, "info", 1.2)

# 리전 A 특성 스트립
d.tone(X_A + 16, Y_BOX + 214, W_A - 32, 42, OK, 4, "12", 1.0)
d.t(X_A + W_A / 2, Y_BOX + 240, "로컬 쓰기 처리로 인터리전 지연 은닉", 12, OK, KR, "middle", 600)


# 2. 우측: 리전 B 데이터센터
X_B = 512
W_B = 344
d.box(X_B, Y_BOX, W_B, H_BOX, PAPER2, RULE, 0.9)
d.t(X_B + 16, Y_BOX + 24, "리전 B (Region B)", 12, SOFT, KR, "start", 600)

# 리전 B 리더
d.tone(X_B + 16, Y_BOX + 42, 144, 52, ACC, 6, "22", 1.2)
d.t(X_B + 88, Y_BOX + 64, "리더 노드 B", 13, INK, KR, "middle", 600)
d.t(X_B + 88, Y_BOX + 82, "쓰기를 로컬에서 처리", 12, ACC, KR, "middle")

# 리전 B 클라이언트
d.box(X_B + 212, Y_BOX + 42, 116, 52, PAPER, RULE, 0.8)
d.t(X_B + 270, Y_BOX + 64, "클라이언트 B", 12, INK, KR, "middle", 600)
d.t(X_B + 270, Y_BOX + 82, "로컬 쓰기 요청", 12, MUTED, KR, "middle")

# 클라이언트 B -> 리더 B 화살표 (길이 46px)
d.arrow([(X_B + 210, Y_BOX + 68), (X_B + 164, Y_BOX + 68)], ACC, "acc", 1.4)

# 리전 B 팔로워들
d.box(X_B + 20, Y_BOX + 140, 140, 50, PAPER, INFO, 1.0)
d.t(X_B + 90, Y_BOX + 162, "팔로워 B1", 12, INK, KR, "middle", 600)
d.t(X_B + 90, Y_BOX + 180, "로컬 읽기 서빙", 12, INFO, KR, "middle")

d.box(X_B + 184, Y_BOX + 140, 140, 50, PAPER, INFO, 1.0)
d.t(X_B + 254, Y_BOX + 162, "팔로워 B2", 12, INK, KR, "middle", 600)
d.t(X_B + 254, Y_BOX + 180, "로컬 읽기 서빙", 12, INFO, KR, "middle")

# 리더 B -> 팔로워들 내부 복제 화살표 (Manhattan 직교)
d.arrow([(X_B + 64, Y_BOX + 94), (X_B + 64, Y_BOX + 136)], INFO, "info", 1.2)
d.arrow([(X_B + 124, Y_BOX + 94), (X_B + 124, Y_BOX + 116), (X_B + 254, Y_BOX + 116), (X_B + 254, Y_BOX + 136)], INFO, "info", 1.2)

# 리전 B 특성 스트립
d.tone(X_B + 16, Y_BOX + 214, W_B - 32, 42, OK, 4, "12", 1.0)
d.t(X_B + W_B / 2, Y_BOX + 240, "인터리전 링크 단절 시에도 독립 동작", 12, OK, KR, "middle", 600)


# 3. 중앙: 인터리전 비동기 양방향 복제 링크
X_MID = (X_A + W_A + X_B) / 2
d.t(X_MID, Y_BOX + 46, "비동기 복제", 12, ACC, KR, "middle", 600)
d.t(X_MID, Y_BOX + 98, "인터리전 링크", 12, SOFT, KR, "middle")

# A -> B 비동기 복제 화살표
d.arrow([(X_A + W_A - 12, Y_BOX + 60), (X_B + 12, Y_BOX + 60)], ACC, "acc", 1.4, dash="4 3")
# B -> A 비동기 복제 화살표
d.arrow([(X_B + 12, Y_BOX + 76), (X_A + W_A - 12, Y_BOX + 76)], ACC, "acc", 1.4, dash="4 3")


# 4. 하단 트레이드오프 비교 카드
Y_BOT = 400
H_BOT = 48

d.box(24, Y_BOT, 400, H_BOT, PAPER2, OK, 1.1)
d.t(44, Y_BOT + 29, "성능·내성 장점", 12, OK, KR, "start", 600)
d.t(148, Y_BOT + 29, "인터리전 지연 은닉 · 리전 장애에도 독립 동작", 12, INK, KR, "start")

d.box(456, Y_BOT, 400, H_BOT, PAPER2, WARN, 1.1)
d.t(476, Y_BOT + 29, "일관성 한계 대가", 12, WARN, KR, "start", 600)
d.t(590, Y_BOT + 29, "잔액 음수 방지 및 유일성 제약 미보장", 12, INK, KR, "start")


# 범례
d.legend(LEG, [("리더 (로컬 쓰기)", ACC), ("팔로워 (읽기 서빙)", INFO), ("지연 은닉·독립성", OK), ("약한 일관성 한계", WARN)])
d.save("06-04.multi-leader.svg")
