# 06-02 §2 — 리더 장애 시 자동 failover 3단계와 4대 위험 요소(미복제 쓰기 폐기·외부 불일치·split brain·타임아웃).
# 사실 출처: 06-02 §2(L34~L50), 원서 Ch.6 "Leader failure: Failover"
# 타입 스펙: type-process
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
H = 590
LEG = H - 56

d = D(W, H, "06-02 §2 · LEADER FAILOVER & PITFALLS", "리더 failover 세 단계와 네 가지 위험 요소",
      "리더 장애 판정, 새 리더 선출, 시스템 재구성의 failover 3단계와 미복제 쓰기 폐기, 외부 불일치, split brain, 타임아웃 딜레마를 보인다.",
      "장애 판정 · 최신 팔로워 승격 · 클라이언트 재구성 · 4대 위험 요소와 펜싱")

# --- Section A: failover 3단계 절차 ---
d.box(24, 104, W - 48, 172, PAPER2, RULE, 0.9)
d.chip(86, 124, "절차 단계", INFO, 11)
d.t(140, 128, "자동 failover 3단계 절차", 13, INK, KR, "start", 600)

s_w = 244
s_h = 120
s_y = 142

# Stage 1: 장애 판정
x0 = 36
d.box(x0, s_y, s_w, s_h, PAPER, RULE, 0.8)
d.t(x0 + s_w / 2, s_y + 22, "1 · 장애 판정", 13, INK, KR, "middle", 600)
d.t(x0 + s_w / 2, s_y + 40, "타임아웃으로 판정", 12, MUTED, KR, "middle")
d.line(x0 + 12, s_y + 48, x0 + s_w - 12, s_y + 48, RULE, 0.8)
d.t(x0 + s_w / 2, s_y + 68, "노드끼리 메시지 주고받음", 12, INK, KR, "middle")
d.t(x0 + s_w / 2, s_y + 86, "30초 무응답 시 결함 간주", 12, MUTED, KR, "middle")
d.t(x0 + s_w / 2, s_y + 104, "계획 유지보수는 안전 인계", 12, SOFT, KR, "middle")

# Stage 2: 새 리더 선출 (FOCAL)
x1 = 318
d.tone(x1, s_y, s_w, s_h, ACC, 6, "18", 1.4)
d.t(x1 + s_w / 2, s_y + 22, "2 · 새 리더 선출", 13, INK, KR, "middle", 600)
d.t(x1 + s_w / 2, s_y + 40, "최신 레플리카 승격", 12, ACC, KR, "middle")
d.line(x1 + 12, s_y + 48, x1 + s_w - 12, s_y + 48, ACC, 0.8)
d.t(x1 + s_w / 2, s_y + 68, "과반 선거 또는 컨트롤러 임명", 12, INK, KR, "middle", 600)
d.t(x1 + s_w / 2, s_y + 86, "최신 LSN 보유 팔로워 선택", 12, ACC, KR, "middle")
d.t(x1 + s_w / 2, s_y + 104, "데이터 손실 최소화", 12, SOFT, KR, "middle")

# Stage 3: 시스템 재구성
x2 = 600
d.box(x2, s_y, s_w, s_h, PAPER, RULE, 0.8)
d.t(x2 + s_w / 2, s_y + 22, "3 · 시스템 재구성", 13, INK, KR, "middle", 600)
d.t(x2 + s_w / 2, s_y + 40, "라우팅 전환 및 강등", 12, MUTED, KR, "middle")
d.line(x2 + 12, s_y + 48, x2 + s_w - 12, s_y + 48, RULE, 0.8)
d.t(x2 + s_w / 2, s_y + 68, "클라이언트 쓰기 라우팅 갱신", 12, INK, KR, "middle")
d.t(x2 + s_w / 2, s_y + 86, "팔로워 복제 수신처 재설정", 12, MUTED, KR, "middle")
d.t(x2 + s_w / 2, s_y + 104, "옛 리더는 복귀하면 팔로워로", 12, SOFT, KR, "middle")

# 단계 연결 화살표
d.arrow([(x0 + s_w + 4, s_y + s_h / 2), (x1 - 4, s_y + s_h / 2)], SOFT, "soft", 1.3)
d.arrow([(x1 + s_w + 4, s_y + s_h / 2), (x2 - 4, s_y + s_h / 2)], SOFT, "soft", 1.3)

# --- Section B: failover 4대 위험 요소 ---
d.box(24, 292, W - 48, 226, PAPER2, RULE, 0.9)
d.chip(104, 312, "4대 위험 요소", WARN, 11)
d.t(170, 316, "failover 과정에서 어긋나는 네 가지 함정", 13, INK, KR, "start", 600)

p_w = 190
p_h = 166
p_y = 336

# Pitfall 1: 미복제 쓰기 폐기
px0 = 36
d.tone(px0, p_y, p_w, p_h, BAD, 6, "14", 1.1)
d.t(px0 + p_w / 2, p_y + 24, "1. 미복제 쓰기 폐기", 12, INK, KR, "middle", 600)
d.chip(px0 + p_w / 2, p_y + 48, "내구성 상실", BAD, 11)
d.line(px0 + 12, p_y + 64, px0 + p_w - 12, p_y + 64, BAD, 0.7)
d.t(px0 + p_w / 2, p_y + 88, "비동기 복제 미수신 쓰기", 12, INK, KR, "middle")
d.t(px0 + p_w / 2, p_y + 110, "옛 리더 복귀 시 폐기", 12, BAD, KR, "middle")
d.t(px0 + p_w / 2, p_y + 132, "확정 통보된 쓰기 유실", 12, MUTED, KR, "middle")

# Pitfall 2: 외부 불일치
px1 = 242
d.tone(px1, p_y, p_w, p_h, WARN, 6, "14", 1.1)
d.t(px1 + p_w / 2, p_y + 24, "2. 외부 불일치", 12, INK, KR, "middle", 600)
d.chip(px1 + p_w / 2, p_y + 48, "GitHub 사고", WARN, 11)
d.line(px1 + 12, p_y + 64, px1 + p_w - 12, p_y + 64, WARN, 0.7)
d.t(px1 + p_w / 2, p_y + 88, "뒤처진 MySQL 승격 사고", 12, INK, KR, "middle")
d.t(px1 + p_w / 2, p_y + 110, "autoincrement PK 재사용", 12, WARN, KR, "middle")
d.t(px1 + p_w / 2, p_y + 132, "Redis 불일치 · 데이터 노출", 12, MUTED, KR, "middle")

# Pitfall 3: split brain
px2 = 448
d.tone(px2, p_y, p_w, p_h, BAD, 6, "14", 1.1)
d.t(px2 + p_w / 2, p_y + 24, "3. split brain", 12, INK, KR, "middle", 600)
d.chip(px2 + p_w / 2, p_y + 48, "이중 리더 충돌", BAD, 11)
d.line(px2 + 12, p_y + 64, px2 + p_w - 12, p_y + 64, BAD, 0.7)
d.t(px2 + p_w / 2, p_y + 88, "두 노드 동시 쓰기 수용", 12, INK, KR, "middle")
d.t(px2 + p_w / 2, p_y + 110, "데이터 손실·손상", 12, BAD, KR, "middle")
d.t(px2 + p_w / 2, p_y + 132, "펜싱(fencing)으로 차단", 12, MUTED, KR, "middle")

# Pitfall 4: 타임아웃 딜레마
px3 = 654
d.tone(px3, p_y, p_w, p_h, WARN, 6, "14", 1.1)
d.t(px3 + p_w / 2, p_y + 24, "4. 타임아웃 딜레마", 12, INK, KR, "middle", 600)
d.chip(px3 + p_w / 2, p_y + 48, "시간 트레이드오프", WARN, 11)
d.line(px3 + 12, p_y + 64, px3 + p_w - 12, p_y + 64, WARN, 0.7)
d.t(px3 + p_w / 2, p_y + 88, "길면 장애 복구 지연", 12, INK, KR, "middle")
d.t(px3 + p_w / 2, p_y + 110, "짧으면 불필요한 failover", 12, WARN, KR, "middle")
d.t(px3 + p_w / 2, p_y + 132, "이미 힘든 상황 악화", 12, MUTED, KR, "middle")

d.legend(LEG, [("핵심 선출 (focal)", ACC), ("정상 절차", INFO), ("치명적 손실", BAD), ("운영 위험", WARN)])
d.save("06-02.failover-logs.svg")
