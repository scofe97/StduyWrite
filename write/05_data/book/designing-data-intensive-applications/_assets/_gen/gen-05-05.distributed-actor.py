# 05-05 §3 — 분산 actor 프레임워크의 노드 경계와 location transparency 구조.
# 사실 출처: 05-05 본문 §3(L72~L74) · 원서 Distributed actor frameworks(PDF p.32) — 로컬 상태(공유 안 함), 한 번에 메시지 하나, 같은·다른 노드에 같은 메시지 전달 메커니즘, 다른 노드면 바이트로 인코딩, 메시지 손실을 이미 가정해 location transparency 가 RPC 보다 잘 맞음.
# 원서·본문에 actor 역할(주문·결제·알림)·메일박스·TCP·직렬화 라이브러리 이름이 없어 도식에도 두지 않는다.
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, OK, BAD, WARN, KR, MONO

W = 880
LEG = 472
H = LEG + 56

d = D(W, H, "05-05 §3 · DISTRIBUTED ACTOR ARCHITECTURE", "분산 actor 프레임워크와 location transparency",
      "액터는 로컬 상태와 한 번에 메시지 하나씩 처리하며, 분산 환경에서 같은 노드든 다른 노드든 같은 메시지 전달 메커니즘을 쓰고 다른 노드면 바이트로 인코딩해 보낸다.",
      "같은 노드 전달 vs 다른 노드 바이트 인코딩과 location transparency")

# ==========================================
# 1. 노드 1 (Node 1 · 로컬 호스트, x=24..408)
# ==========================================
d.box(24, 96, 384, 292, PAPER, RULE, 1.0, r=8)
d.box(36, 102, 160, 20, PAPER2, RULE, 0.8, r=4)
d.t(116, 116, "NODE 1 · LOCAL HOST", 9, SOFT, MONO, "middle")

# Actor A (주문 액터)
d.box(36, 132, 164, 112, PAPER2, INFO, 1.2, r=6)
d.t(118, 154, "Actor A", 13, INK, KR, "middle", 600)
d.box(44, 168, 148, 28, PAPER, RULE, 0.8, r=4)
d.t(118, 186, "로컬 상태 (공유 안 함)", 12, MUTED, KR, "middle")
d.box(44, 202, 148, 30, PAPER, INFO, 0.8, r=4)
d.t(118, 222, "한 번에 메시지 하나", 12, INFO, KR, "middle")

# Actor B (결제 액터 · 동일 노드)
d.box(232, 132, 164, 112, PAPER2, INFO, 1.2, r=6)
d.t(314, 154, "Actor B", 13, INK, KR, "middle", 600)
d.box(240, 168, 148, 28, PAPER, RULE, 0.8, r=4)
d.t(314, 186, "로컬 상태 (공유 안 함)", 12, MUTED, KR, "middle")
d.box(240, 202, 148, 30, PAPER, INFO, 0.8, r=4)
d.t(314, 222, "한 번에 메시지 하나", 12, INFO, KR, "middle")

# 로컬 인메모리 화살표 (Actor A → Actor B)
d.arrow([(200, 218), (232, 218)], OK, "ok", 1.4)
d.t(216, 206, "로컬", 12, OK, KR, "middle")

# 노드 1 내부 인메모리 해설 바
d.box(36, 260, 360, 36, PAPER2, RULE, 0.8, r=4)
d.t(216, 282, "같은 노드: 바이트 인코딩 없이 전달", 12, OK, KR, "middle")

# 노드 1 하단 직렬화 어댑터 (원격 전송용)
d.box(36, 312, 360, 60, PAPER2, ACC, 1.0, r=4)
d.t(110, 336, "프레임워크", 12, INK, KR, "middle", 600)
d.t(110, 356, "send(Actor C, msg)", 11, MUTED, MONO, "middle")
d.box(192, 320, 192, 44, PAPER, ACC, 0.8, r=4)
d.t(288, 338, "바이트 인코딩", 12, ACC, KR, "middle", 600)
d.t(288, 354, "메시지를 바이트로", 11, MUTED, MONO, "middle")

# Actor A → 프레임워크 수직 화살표
d.arrow([(118, 244), (118, 312)], MUTED, "ar", 1.2)

# ==========================================
# 2. 노드 2 (Node 2 · 원격 호스트, x=472..856)
# ==========================================
d.tone(472, 96, 384, 292, ACC, 8, "08", 1.2)
d.box(484, 102, 160, 20, PAPER2, ACC, 0.8, r=4)
d.t(564, 116, "NODE 2 · REMOTE HOST", 9, ACC, MONO, "middle")

# 노드 2 원격 수신 디코더
d.box(484, 312, 180, 60, PAPER, ACC, 0.9, r=4)
d.t(574, 338, "바이트 디코딩", 12, ACC, KR, "middle", 600)
d.t(574, 354, "바이트 스트림 → 메시지 객체", 12, MUTED, KR, "middle")

# Actor C (알림 액터 · 원격 노드)
d.box(680, 132, 164, 112, PAPER2, ACC, 1.4, r=6)
d.t(762, 154, "Actor C", 13, ACC, KR, "middle", 600)
d.box(688, 168, 148, 28, PAPER, RULE, 0.8, r=4)
d.t(762, 186, "로컬 상태 (공유 안 함)", 12, MUTED, KR, "middle")
d.box(688, 202, 148, 30, PAPER, ACC, 0.8, r=4)
d.t(762, 222, "한 번에 메시지 하나", 12, ACC, KR, "middle")

# 노드 2 내부 인메모리 해설 바
d.box(484, 260, 360, 36, PAPER2, RULE, 0.8, r=4)
d.t(664, 282, "다른 노드: 디코딩한 뒤 수신 actor 에 전달", 12, MUTED, KR, "middle")

# 디코더 → Actor C 수직 화살표
d.arrow([(500, 312), (500, 218), (680, 218)], ACC, "acc", 1.4)

# ==========================================
# 3. 노드 간 네트워크 전송 화살표 (Focal ACC)
# ==========================================
d.arrow([(384, 342), (484, 342)], ACC, "acc", 1.8)
d.t(434, 332, "네트워크", 12, ACC, KR, "middle")

# ==========================================
# 4. 하단 Location Transparency 배너
# ==========================================
d.box(24, 404, 832, 48, PAPER2, INFO, 1.0, r=6)
d.t(148, 432, "location transparency", 13, INFO, MONO, "middle", 600)
d.t(510, 432, "같은 메시지 전달 방식 · 단일 프로세스에서도 메시지 손실을 가정해 RPC 보다 잘 맞음", 12, INK, KR, "middle")

d.legend(LEG, [
    ("같은 노드 전달", OK),
    ("원격 전송 (location transparency)", ACC),
    ("actor 로컬 상태", INFO)
])
d.save("05-05.distributed-actor.svg")
