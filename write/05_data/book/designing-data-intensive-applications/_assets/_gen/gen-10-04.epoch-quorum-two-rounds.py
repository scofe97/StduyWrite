# 10-04 §2 — 에포크 번호 기반 리더 유일성과 두 번의 쿼럼 투표(선출·복제) 및 쿼럼 교집합 안전성 보장.
# 사실 출처: 10-04 §2(L40~L53), 원서 Ch.10 "From single-leader replication to consensus"(PDF p.43~46)
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, OK, WARN, KR, MONO

W = 880
LEG = 454
H = LEG + 56

d = D(W, H, "10-04 · §2 EPOCH AND TWO-ROUND QUORUM VOTING", "에포크 번호와 2라운드 쿼럼 투표 체계",
      "단조 증가 에포크 번호로 리더 유일성을 보장하고, 선거 쿼럼과 복제 쿼럼의 교집합으로 커밋 일관성을 지킨다.",
      "단조 증가 에포크(term) · 1라운드 리더 선출 쿼럼 · 2라운드 로그 항목 복제 쿼럼 · 쿼럼 교집합 안전성")

# 좌측 패널: Round 1 — 리더 선출
P1_X, P1_Y, P1_W, P1_H = 24, 102, 406, 246
d.box(P1_X, P1_Y, P1_W, P1_H, PAPER2, RULE, 1.0)
d.chip(P1_X + 38, P1_Y + 22, "Round 1", INFO, 11, pad=5)
d.t(P1_X + 230, P1_Y + 26, "리더 선출 (선거 쿼럼)", 13, INK, KR, "middle", 600)
d.line(P1_X + 12, P1_Y + 42, P1_X + P1_W - 12, P1_Y + 42, RULE, 0.6)
d.t(P1_X + P1_W / 2, P1_Y + 58, "후보 노드가 에포크(term e+1)로 투표 요청", 11, MUTED, KR, "middle")

# 좌측 3개 노드 (폭 116)
N1_Y = 170
d.tone(40, N1_Y, 116, 56, INFO, 4, "14", 1.0)
d.t(98, N1_Y + 20, "Node 1 (후보)", 11, INK, KR, "middle", 600)
d.t(98, N1_Y + 38, "term e+1 제안", 11, INFO, KR, "middle")

d.tone(168, N1_Y, 116, 56, OK, 4, "14", 1.0)
d.t(226, N1_Y + 20, "Node 2 (팔로워)", 11, INK, KR, "middle", 600)
d.t(226, N1_Y + 38, "투표 찬성 (✓ vote)", 11, OK, KR, "middle")

d.box(296, N1_Y, 116, 56, PAPER, RULE, 0.8, r=4)
d.t(354, N1_Y + 20, "Node 3 (팔로워)", 11, MUTED, KR, "middle", 600)
d.t(354, N1_Y + 38, "미응답 또는 지연", 11, MUTED, KR, "middle")

# 좌측 메시지 화살표
d.path("M 156 186 L 168 186", INFO, 1.2, m="info")
d.path("M 168 202 L 156 202", OK, 1.2, m="ok")
d.path("M 284 194 L 296 194", MUTED, 1.0, m="ar", dash="2 2")

# 좌측 결과 박스
d.box(40, 242, 372, 44, PAPER, RULE, 0.8, r=4)
d.t(226, 260, "선거 쿼럼: {Node 1, Node 2} (과반수 2/3 달성)", 11, INK, KR, "middle", 600)
d.t(226, 276, "Node 1 리더 승격 · 에포크 e+1 단독 리더십 확립", 11, INFO, KR, "middle")
d.t(226, 304, "Raft 규칙: 후보 로그가 자신보다 오래되면 투표 거부", 11, MUTED, KR, "middle")
d.t(226, 322, "Paxos 규칙: 리더 선출 후 이전 미완성 제안 동기화", 11, MUTED, KR, "middle")

# 우측 패널: Round 2 — 로그 복제 및 커밋
P2_X, P2_Y, P2_W, P2_H = 450, 102, 406, 246
d.box(P2_X, P2_Y, P2_W, P2_H, PAPER2, RULE, 1.0)
d.chip(P2_X + 38, P2_Y + 22, "Round 2", OK, 11, pad=5)
d.t(P2_X + 230, P2_Y + 26, "로그 복제 (커밋 쿼럼)", 13, INK, KR, "middle", 600)
d.line(P2_X + 12, P2_Y + 42, P2_X + P2_W - 12, P2_Y + 42, RULE, 0.6)
d.t(P2_X + P2_W / 2, P2_Y + 58, "리더가 명령 수신 후 과반수 복제 시 커밋", 11, MUTED, KR, "middle")

# 우측 3개 노드 (폭 116)
d.tone(466, N1_Y, 116, 56, ACC, 4, "14", 1.2)
d.t(524, N1_Y + 20, "Node 1 (리더)", 11, INK, KR, "middle", 600)
d.t(524, N1_Y + 38, "[cmd] 항목 복제", 11, ACC, KR, "middle")

d.tone(594, N1_Y, 116, 56, OK, 4, "14", 1.0)
d.t(652, N1_Y + 20, "Node 2 (팔로워)", 11, INK, KR, "middle", 600)
d.t(652, N1_Y + 38, "복제 확인 (✓ ack)", 11, OK, KR, "middle")

d.box(722, N1_Y, 116, 56, PAPER, RULE, 0.8, r=4)
d.t(780, N1_Y + 20, "Node 3 (팔로워)", 11, MUTED, KR, "middle", 600)
d.t(780, N1_Y + 38, "네트워크 단절", 11, MUTED, KR, "middle")

# 우측 메시지 화살표
d.path("M 582 186 L 594 186", ACC, 1.2, m="acc")
d.path("M 594 202 L 582 202", OK, 1.2, m="ok")
d.path("M 710 194 L 722 194", MUTED, 1.0, m="ar", dash="2 2")

# 우측 결과 박스
d.box(466, 242, 372, 44, PAPER, RULE, 0.8, r=4)
d.t(652, 260, "복제 쿼럼: {Node 1, Node 2} (과반수 2/3 달성)", 11, INK, KR, "middle", 600)
d.t(652, 276, "[cmd] 항목 커밋 확정 · 팔로워 상태 머신 반영", 11, OK, KR, "middle")
d.t(652, 304, "과반수 응답 전에는 미커밋 유지로 안전 확보", 11, MUTED, KR, "middle")
d.t(652, 322, "선형화 읽기: 리더가 아직 최신인지 쿼럼 확인 후 응답", 11, MUTED, KR, "middle")

# 하단 패널: 쿼럼 교집합 안전성 보장
d.tone(24, 362, 832, 74, ACC, 6, "14", 1.2)
d.t(440, 384, "안전성의 핵심: 쿼럼 교집합 보장 (Quorum Overlap)", 13, ACC, KR, "middle", 600)
d.t(440, 404, "선거 쿼럼 Q1 ∩ 복제 쿼럼 Q2 ≥ 1개 노드 (과반수끼리는 반드시 겹침)", 11, INK, KR, "middle")
d.t(440, 422, "새 리더 선출 시 쿼럼 노드 중 최소 하나는 직전 커밋 로그 보유 → 커밋 소실 방지", 11, MUTED, KR, "middle")

# 범례
d.legend(LEG, [
    ("쿼럼 교집합 안전성 (focal)", ACC),
    ("선거 쿼럼 투표", INFO),
    ("복제 쿼럼 커밋", OK),
    ("단절·미응답 노드", MUTED)
])

d.save("10-04.epoch-quorum-two-rounds.svg")
