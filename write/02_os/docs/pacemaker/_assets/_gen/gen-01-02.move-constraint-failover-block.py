# 수동 ban 제약 잔류로 인한 Failover 차단 흐름 — t1 ban 부터 t4 제약 해제까지.
# 사실 출처: pcs(8) pcs-0.11 resource ban/clear, Pacemaker Explained 2.1 §7.1.1 score(-INFINITY = must avoid), crm_resource_ban.c 제약 ID
# 타입 스펙: type-process
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dd import D, ACC, MUTED, SOFT, INK, BAD, OK, WARN, PAPER2, RULE, KR, MONO

W, H = 880, 440
d = D(W, H, "PACEMAKER · LOCATION CONSTRAINT",
      "수동 이동 제약 잔류로 인한 절체 차단 흐름",
      "pcs resource ban 이 생성한 cli-ban 제약(-INFINITY)을 해제하지 않으면 현재 노드 장애 시 정상 노드로의 자동 절체가 차단된다.",
      lead="남은 ban 제약은 장애 절체 경로를 차단한다")

BX = [36, 244, 452, 660]; BW = 184; BH1 = 104; BH2 = 92
Y1 = 124; Y2 = 256

titles = ["t1 ban 실행", "t2 노드 장애", "t3 절체 차단 (장애)", "t4 제약 해제"]
colors = [OK, WARN, BAD, OK]

for x, t, c in zip(BX, titles, colors):
    d.t(x, 108, t, 13, c, KR, "start", 600)

# ---- 상단 박스: 노드 및 리소스 런타임 상태 ----
# t1
d.box(BX[0], Y1, BW, BH1, PAPER2, RULE, 0.9, 6)
d.t(BX[0] + 12, Y1 + 24, "ban R1 node1", 12, INK, MONO, "start", 600)
d.t(BX[0] + 12, Y1 + 48, "node1: R1 밀려남", 12, MUTED, KR, "start")
d.t(BX[0] + 12, Y1 + 70, "node2: R1 가동 (OK)", 12, OK, KR, "start")
d.t(BX[0] + 12, Y1 + 90, "node2 로 이동 완료", 12, MUTED, KR, "start")

# t2
d.box(BX[1], Y1, BW, BH1, PAPER2, RULE, 0.9, 6)
d.t(BX[1] + 12, Y1 + 24, "node2 다운 (Crash)", 12, BAD, KR, "start", 600)
d.t(BX[1] + 12, Y1 + 48, "node1: 정상 가동 중", 12, OK, KR, "start")
d.t(BX[1] + 12, Y1 + 70, "R1 정지 감지", 12, WARN, KR, "start")
d.t(BX[1] + 12, Y1 + 90, "절체 연산 시작", 12, MUTED, KR, "start")

# t3 (Focal)
d.tone(BX[2], Y1, BW, BH1, ACC, 6)
d.t(BX[2] + 12, Y1 + 24, "R1 Stopped (장애)", 12, BAD, KR, "start", 600)
d.t(BX[2] + 12, Y1 + 48, "node1: 절체 거부", 12, BAD, KR, "start")
d.t(BX[2] + 12, Y1 + 70, "score: -INFINITY", 12, BAD, MONO, "start")
d.t(BX[2] + 12, Y1 + 90, "정상 노드 배치 불가", 12, ACC, KR, "start")

# t4
d.box(BX[3], Y1, BW, BH1, PAPER2, RULE, 0.9, 6)
d.t(BX[3] + 12, Y1 + 24, "clear R1", 12, INK, MONO, "start", 600)
d.t(BX[3] + 12, Y1 + 48, "제약 삭제 완료", 12, MUTED, KR, "start")
d.t(BX[3] + 12, Y1 + 70, "node1: R1 재기동", 12, OK, KR, "start")
d.t(BX[3] + 12, Y1 + 90, "서비스 정상 복구", 12, OK, KR, "start")

# 상단 박스 사이 수평 화살표
for i in range(3):
    d.arrow([(BX[i] + BW, Y1 + 52), (BX[i + 1] - 4, Y1 + 52)], MUTED, "ar", 1.2)

# ---- 하단 박스: CIB 제약 조건 상태 ----
# t1 CIB
d.box(BX[0], Y2, BW, BH2, PAPER2, RULE, 0.9, 6)
d.t(BX[0] + 12, Y2 + 24, "cli-ban-R1-on-node1", 12, WARN, MONO, "start", 600)
d.t(BX[0] + 12, Y2 + 48, "node1 -INFINITY 생성", 12, WARN, KR, "start")
d.t(BX[0] + 12, Y2 + 70, "lifetime 없으면 무기한", 12, MUTED, KR, "start")

# t2 CIB
d.box(BX[1], Y2, BW, BH2, PAPER2, RULE, 0.9, 6)
d.t(BX[1] + 12, Y2 + 24, "cli-ban 제약 잔류", 12, WARN, MONO, "start", 600)
d.t(BX[1] + 12, Y2 + 48, "제약 미해제 상태", 12, WARN, KR, "start")
d.t(BX[1] + 12, Y2 + 70, "node1 진입 차단 유지", 12, MUTED, KR, "start")

# t3 CIB
d.box(BX[2], Y2, BW, BH2, PAPER2, RULE, 0.9, 6)
d.t(BX[2] + 12, Y2 + 24, "절체 계산 실패", 12, BAD, KR, "start", 600)
d.t(BX[2] + 12, Y2 + 48, "node1 점수 -INFINITY", 12, BAD, KR, "start")
d.t(BX[2] + 12, Y2 + 70, "서비스 중단 지속", 12, MUTED, KR, "start")

# t4 CIB
d.box(BX[3], Y2, BW, BH2, PAPER2, RULE, 0.9, 6)
d.t(BX[3] + 12, Y2 + 24, "제약 CIB 삭제", 12, OK, KR, "start", 600)
d.t(BX[3] + 12, Y2 + 48, "기본 배치 정책 복원", 12, OK, KR, "start")
d.t(BX[3] + 12, Y2 + 70, "정상 가용성 확보", 12, OK, KR, "start")

# 상하 박스 연결 점선 화살표
for x in BX:
    d.arrow([(x + BW / 2, Y1 + BH1), (x + BW / 2, Y2 - 4)], SOFT, "soft", 1.0, "3 3")

d.legend(H - 44, [("정상 가동 · 복구", OK), ("임시 제약 잔류", WARN), ("장애 · 절체 불가", BAD), ("주목: 절체 차단 지점", ACC)])
d.save(os.path.join(os.path.dirname(__file__), "..", "01-02.move-constraint-failover-block.svg"))
print("ok move-constraint-failover-block")
