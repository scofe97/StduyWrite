# 10-02 §3 — PACELC 조건 분기와 파티션(P) 및 정상 운영(E) 시 분산 시스템 트레이드오프.
# 사실 출처: 10-02 §3(L64~L87), DDIA 2판 Ch.10 "PACELC" (PDF p.19), Abadi (2012)
# 타입 스펙: type-flowchart
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
CY_ROOT = 120
CY_DEC = 194
Y_SUB = 264
Y_CARDS = 330
H_CARDS = 146
Y_SUM = 498
H_SUM = 50
LEG = Y_SUM + H_SUM + 28
H = LEG + 48

d = D(W, H, "10-02 · §3 PACELC BRANCHES", "PACELC 조건 분기와 시스템 트레이드오프",
      "파티션 상황(P)의 A vs C와 정상 상황(E)의 L vs C 선택에 따른 분산 시스템 분류 흐름도.",
      "운영 상태 분기 · 파티션 시 가용성 vs 일관성 · 평시 지연 vs 일관성 · 현실 DB 분류")

# 1. 루트 노드: 분산 시스템 운영 상태 판별
d.box(W / 2 - 130, CY_ROOT - 18, 260, 36, fill=PAPER2, stroke=INFO, sw=1.1, r=18)
d.t(W / 2, CY_ROOT + 4, "분산 시스템 운영 상태 판별", 12.5, INK, KR, "middle", 600)

d.arrow([(W / 2, CY_ROOT + 18), (W / 2, CY_DEC - 28)], MUTED, "ar", 1.2)

# 2. 메인 조건 분기 다이아몬드: 네트워크 파티션 발생 여부?
DW, DH = 240, 56
d.o.append(f'<path d="M {W/2} {CY_DEC - DH/2} L {W/2 + DW/2} {CY_DEC} '
           f'L {W/2} {CY_DEC + DH/2} L {W/2 - DW/2} {CY_DEC} Z" '
           f'fill="{PAPER2}" stroke="{RULE}" stroke-width="1.2"/>')
d.t(W / 2, CY_DEC + 4, "네트워크 파티션 발생 상태?", 12, INK, KR, "middle", 600)

# 좌측 분기 화살표: P (파티션 발생)
CX_P = 218
d.arrow([(W / 2 - DW / 2, CY_DEC), (CX_P, CY_DEC), (CX_P, Y_SUB)], WARN, "warn", 1.3)
d.chip(CX_P, (CY_DEC + Y_SUB) / 2, "파티션 발생 (P)", WARN, 11)

# 우측 분기 화살표: E (정상 운영)
CX_E = 662
d.arrow([(W / 2 + DW / 2, CY_DEC), (CX_E, CY_DEC), (CX_E, Y_SUB)], INFO, "info", 1.3)
d.chip(CX_E, (CY_DEC + Y_SUB) / 2, "정상 운영 (Else / E)", INFO, 11)


# 3. 좌측 P 국면 선택 박스
d.box(CX_P - 130, Y_SUB, 260, 40, fill=PAPER2, stroke=WARN, sw=1.1, r=6)
d.t(CX_P, Y_SUB + 18, "장애 상황: 가용성(A) vs 일관성(C)", 12, WARN, KR, "middle", 600)
d.t(CX_P, Y_SUB + 33, "CAP 정리와 동일한 선택지", 11, MUTED, KR, "middle")

# 좌측 하위 분기 화살표
d.arrow([(CX_P - 60, Y_SUB + 40), (CX_P - 60, Y_CARDS)], ACC, "acc", 1.2)
d.arrow([(CX_P + 60, Y_SUB + 40), (CX_P + 60, Y_CARDS)], OK, "ok", 1.2)


# 4. 우측 E 국면 선택 박스
d.box(CX_E - 130, Y_SUB, 260, 40, fill=PAPER2, stroke=INFO, sw=1.1, r=6)
d.t(CX_E, Y_SUB + 18, "평시 상황: 지연(L) vs 일관성(C)", 12, INFO, KR, "middle", 600)
d.t(CX_E, Y_SUB + 33, "CAP이 무시한 일상적 트레이드오프", 11, MUTED, KR, "middle")

# 우측 하위 분기 화살표
d.arrow([(CX_E - 60, Y_SUB + 40), (CX_E - 60, Y_CARDS)], ACC, "acc", 1.2)
d.arrow([(CX_E + 60, Y_SUB + 40), (CX_E + 60, Y_CARDS)], OK, "ok", 1.2)


# 5. 하위 4개 카드 (PA, PC, EL, EC)
CW_CARD = 196
X_PA = 24
X_PC = 230
X_EL = 454
X_EC = 660

# [PA] 카드
d.box(X_PA, Y_CARDS, CW_CARD, H_CARDS, fill=PAPER2, stroke=ACC, sw=1.1, r=6)
d.chip(X_PA + 32, Y_CARDS + 20, "PA", ACC, 11)
d.t(X_PA + CW_CARD / 2 + 14, Y_CARDS + 24, "가용성(A) 우선", 12.5, INK, KR, "middle", 600)
d.line(X_PA + 10, Y_CARDS + 36, X_PA + CW_CARD - 10, Y_CARDS + 36, RULE, 0.8)
d.t(X_PA + 14, Y_CARDS + 54, "• 독립 연산 처리 허용", 11.5, INK, KR, "start")
d.t(X_PA + 14, Y_CARDS + 72, "• 선형성 포기 · 데이터 분기", 11, MUTED, KR, "start")
d.tone(X_PA + 10, Y_CARDS + 86, CW_CARD - 20, 48, ACC, 4, "12", 0.8)
d.t(X_PA + CW_CARD / 2, Y_CARDS + 104, "대표 시스템", 11, ACC, KR, "middle", 600)
d.t(X_PA + CW_CARD / 2, Y_CARDS + 122, "DynamoDB · Cassandra · MySQL", 11, INK, KR, "middle")

# [PC] 카드
d.box(X_PC, Y_CARDS, CW_CARD, H_CARDS, fill=PAPER2, stroke=OK, sw=1.1, r=6)
d.chip(X_PC + 32, Y_CARDS + 20, "PC", OK, 11)
d.t(X_PC + CW_CARD / 2 + 14, Y_CARDS + 24, "일관성(C) 우선", 12.5, INK, KR, "middle", 600)
d.line(X_PC + 10, Y_CARDS + 36, X_PC + CW_CARD - 10, Y_CARDS + 36, RULE, 0.8)
d.t(X_PC + 14, Y_CARDS + 54, "• 연결 불가 노드 요청 차단", 11.5, INK, KR, "start")
d.t(X_PC + 14, Y_CARDS + 72, "• 가용성 희생 · 선형성 유지", 11, MUTED, KR, "start")
d.tone(X_PC + 10, Y_CARDS + 86, CW_CARD - 20, 48, OK, 4, "12", 0.8)
d.t(X_PC + CW_CARD / 2, Y_CARDS + 104, "대표 시스템", 11, OK, KR, "middle", 600)
d.t(X_PC + CW_CARD / 2, Y_CARDS + 122, "ZooKeeper · PostgreSQL 동기", 11, INK, KR, "middle")

# [EL] 카드
d.box(X_EL, Y_CARDS, CW_CARD, H_CARDS, fill=PAPER2, stroke=ACC, sw=1.1, r=6)
d.chip(X_EL + 32, Y_CARDS + 20, "EL", ACC, 11)
d.t(X_EL + CW_CARD / 2 + 14, Y_CARDS + 24, "지연(L) 우선", 12.5, INK, KR, "middle", 600)
d.line(X_EL + 10, Y_CARDS + 36, X_EL + CW_CARD - 10, Y_CARDS + 36, RULE, 0.8)
d.t(X_EL + 14, Y_CARDS + 54, "• 단일 복제본 즉시 응답", 11.5, INK, KR, "start")
d.t(X_EL + 14, Y_CARDS + 72, "• 최종 일관성 · RTT 회피", 11, MUTED, KR, "start")
d.tone(X_EL + 10, Y_CARDS + 86, CW_CARD - 20, 48, ACC, 4, "12", 0.8)
d.t(X_EL + CW_CARD / 2, Y_CARDS + 104, "대표 시스템", 11, ACC, KR, "middle", 600)
d.t(X_EL + CW_CARD / 2, Y_CARDS + 122, "DynamoDB · Cassandra · MySQL", 11, INK, KR, "middle")

# [EC] 카드
d.box(X_EC, Y_CARDS, CW_CARD, H_CARDS, fill=PAPER2, stroke=OK, sw=1.1, r=6)
d.chip(X_EC + 32, Y_CARDS + 20, "EC", OK, 11)
d.t(X_EC + CW_CARD / 2 + 14, Y_CARDS + 24, "일관성(C) 우선", 12.5, INK, KR, "middle", 600)
d.line(X_EC + 10, Y_CARDS + 36, X_EC + CW_CARD - 10, Y_CARDS + 36, RULE, 0.8)
d.t(X_EC + 14, Y_CARDS + 54, "• 복수 노드 동기화 확인", 11.5, INK, KR, "start")
d.t(X_EC + 14, Y_CARDS + 72, "• 네트워크 왕복 지연 감수", 11, MUTED, KR, "start")
d.tone(X_EC + 10, Y_CARDS + 86, CW_CARD - 20, 48, OK, 4, "12", 0.8)
d.t(X_EC + CW_CARD / 2, Y_CARDS + 104, "대표 시스템", 11, OK, KR, "middle", 600)
d.t(X_EC + CW_CARD / 2, Y_CARDS + 122, "ZooKeeper · PostgreSQL 동기", 11, INK, KR, "middle")


# 6. 하단 종합 카드
d.box(24, Y_SUM, W - 48, H_SUM, fill=PAPER2, stroke=RULE, sw=0.9, r=6)
d.t(38, Y_SUM + 20, "실제 시스템 조합", 11.5, SOFT, KR, "start", 600)
d.t(38, Y_SUM + 36, "• PA/EL: DynamoDB · Cassandra · MySQL 비동기  |  PC/EC: ZooKeeper · PostgreSQL 동기", 11.5, INK, KR, "start")


# 범례
d.legend(LEG, [
    ("장애 상황 분기 (P)", WARN),
    ("정상 운영 분기 (E)", INFO),
    ("가용성·지연 우선 (A·L)", ACC),
    ("일관성 보장 우선 (C)", OK),
])

d.save("10-02.pacelc-branches.svg")
