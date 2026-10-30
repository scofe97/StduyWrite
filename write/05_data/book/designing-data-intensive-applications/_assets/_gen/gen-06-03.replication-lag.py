# 06-03 §1 — read-scaling 아키텍처에서 쓰기는 리더로 집중되고 읽기는 비동기 팔로워로 분산되며 복제 지연에 따라 stale 읽기가 발생하는 데이터 흐름.
# 사실 출처: 06-03 §1(L26~L33), 원서 Ch.6 p.15~16
# 타입 스펙: type-data-flow
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
PY = 120
PH = 312
LEG = PY + PH + 22
H = LEG + 52

d = D(W, H, "06-03 · §1 READ-SCALING ARCHITECTURE", "read-scaling 아키텍처와 복제 지연",
      "쓰기 집중 처리와 비동기 팔로워 분산 읽기 환경에서 복제 지연으로 인한 낡은 데이터 반환 구조",
      "단일 리더 쓰기 수용 · 비동기 복제 로그 전파 · 팔로워 읽기 분산 · eventual consistency")

# 1. 상단 좌측: 쓰기 클라이언트
d.box(36, 132, 200, 74, PAPER2, ACC, 1.2)
d.chip(136, 148, "쓰기 클라이언트", ACC, 11)
d.t(136, 174, "INSERT / UPDATE", 11, INK, MONO, "middle", 600)
d.t(136, 192, "단일 리더로 쓰기 전송", 11, SOFT, KR, "middle")

# 2. 상단 중앙: 리더 노드
d.box(306, 126, 268, 78, PAPER2, ACC, 1.4)
d.chip(440, 144, "리더 (Leader)", ACC, 11)
d.t(440, 170, "단일 쓰기 수용 노드", 12, INK, KR, "middle", 600)
d.t(440, 192, "최신 쓰기 보유", 11, OK, KR, "middle")

# 화살표: 쓰기 클라이언트 -> 리더
d.arrow([(236, 169), (304, 169)], ACC, "acc", 1.4)
d.t(270, 160, "쓰기 전송", 11, ACC, KR, "middle")

# 3. 중단 좌측: 팔로워 1 (정상 복제)
d.box(66, 244, 344, 76, PAPER2, OK, 1.1)
d.chip(238, 262, "팔로워 1 (정상 복제)", OK, 11)
d.t(238, 286, "지연 1초 미만 · 눈에 안 띔", 11, INK, KR, "middle")
d.t(238, 306, "리더와 같은 값", 11, OK, KR, "middle")

# 4. 중단 우측: 팔로워 2 (지연 노드)
d.box(470, 244, 344, 76, PAPER2, WARN, 1.2)
d.chip(642, 262, "팔로워 2 (뒤처짐)", WARN, 11)
d.t(642, 286, "용량 근처·네트워크 문제로 수 초~수 분", 11, WARN, KR, "middle")
d.t(642, 306, "일부 쓰기 미반영", 11, BAD, KR, "middle")

# 복제 직교 화살표 (orthogonal step: no diagonal)
# 리더 -> 팔로워 1 (정상 비동기 복제)
d.arrow([(370, 204), (370, 228), (238, 228), (238, 242)], OK, "ok", 1.4)
d.t(304, 222, "비동기 복제", 11, OK, KR, "middle")

# 리더 -> 팔로워 2 (지연 복제)
d.arrow([(510, 204), (510, 228), (642, 228), (642, 242)], WARN, "warn", 1.4, dash="4 4")
d.t(576, 222, "복제 지연 발생", 11, WARN, KR, "middle")

# 5. 하단 좌측: 읽기 분산 질의 및 최신 결과
d.box(66, 356, 344, 76, PAPER2, INFO, 1.0)
d.chip(238, 374, "읽기 분산 · 최신 판독", INFO, 11)
d.t(238, 398, "같은 질의 → 최신 값", 12, OK, KR, "middle", 600)
d.t(238, 416, "리더와 일치하는 최신 데이터 반환", 11, SOFT, KR, "middle")

# 6. 하단 우측: 읽기 분산 질의 및 stale 결과
d.box(470, 356, 344, 76, PAPER2, BAD, 1.2)
d.chip(642, 374, "읽기 분산 · stale 판독", BAD, 11)
d.t(642, 398, "같은 질의 → 낡은 값", 12, BAD, KR, "middle", 600)
d.t(642, 416, "미반영 지연으로 낡은 데이터 반환", 11, SOFT, KR, "middle")

# 하단 화살표 (gap = 36px, >= 30px)
d.arrow([(238, 320), (238, 354)], OK, "ok", 1.3)
d.arrow([(642, 320), (642, 354)], BAD, "bad", 1.3)

d.legend(LEG, [("쓰기 처리", ACC), ("정상 복제", OK), ("복제 지연", WARN), ("최신 판독", INFO), ("stale 판독", BAD)])
d.save("06-03.replication-lag.svg")
